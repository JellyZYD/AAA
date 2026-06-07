from __future__ import annotations

import json
from dataclasses import dataclass
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Iterable

import pandas as pd

from .models import BacktestResult, InstrumentSpec, Settings, StrategyAction, StrategyParams, Trade
from .storage import LocalStore
from .strategy import StrategyEngine, build_param_grid


@dataclass
class BacktestRun:
    result: BacktestResult
    trades: list[Trade]
    equity_curve: pd.DataFrame
    actions: list[StrategyAction]


class Backtester:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.engine = StrategyEngine()

    def run(
        self,
        symbol: str,
        spec: InstrumentSpec,
        bars: pd.DataFrame,
        params: StrategyParams,
        events: pd.DataFrame | None = None,
    ) -> BacktestRun:
        bars = bars.sort_values("timestamp").reset_index(drop=True)
        risk_filter = self._risk_filter(spec, params)
        actions = self.engine.generate_actions(bars, params, symbol=symbol, events=events, risk_filter=risk_filter)
        actions_by_fill_index: dict[int, list[StrategyAction]] = {}
        for action in actions:
            if action.action == "RISK_BLOCKED":
                continue
            fill_index = action.index + 1
            if fill_index < len(bars):
                actions_by_fill_index.setdefault(fill_index, []).append(action)

        cash = self.settings.capital
        position = 0
        qty = 0
        entry_price = 0.0
        entry_time = None
        entry_reason = ""
        entry_margin = 0.0
        trades: list[Trade] = []
        equity_rows = []

        for i, row in bars.iterrows():
            close = float(row["close"])
            fill_price = self._fill_price(row)
            ts = pd.Timestamp(row["timestamp"]).to_pydatetime()
            for action in actions_by_fill_index.get(i, []):
                if action.action == "OPEN_LONG" and position == 0:
                    if not self._execution_risk_ok(spec, params, action, fill_price):
                        continue
                    position = 1
                    qty = 1
                    entry_price = fill_price
                    entry_time = ts
                    entry_reason = action.reason
                    entry_margin = spec.margin(fill_price, qty)
                    cash -= self._fees(spec, fill_price, qty)
                elif action.action == "OPEN_SHORT" and position == 0:
                    if not self._execution_risk_ok(spec, params, action, fill_price):
                        continue
                    position = -1
                    qty = 1
                    entry_price = fill_price
                    entry_time = ts
                    entry_reason = action.reason
                    entry_margin = spec.margin(fill_price, qty)
                    cash -= self._fees(spec, fill_price, qty)
                elif action.action == "CLOSE_LONG" and position == 1:
                    trade, cash = self._close_trade(
                        symbol, spec, "LONG", entry_time, ts, entry_price, fill_price, qty, cash,
                        entry_reason, action.reason, entry_margin
                    )
                    trades.append(trade)
                    position = 0
                    qty = 0
                elif action.action == "CLOSE_SHORT" and position == -1:
                    trade, cash = self._close_trade(
                        symbol, spec, "SHORT", entry_time, ts, entry_price, fill_price, qty, cash,
                        entry_reason, action.reason, entry_margin
                    )
                    trades.append(trade)
                    position = 0
                    qty = 0
            unrealized = 0.0
            if position != 0:
                unrealized = (close - entry_price) * spec.multiplier * qty * position
            equity_rows.append({"timestamp": ts, "equity": cash + unrealized})

        if position != 0 and not bars.empty:
            last = bars.iloc[-1]
            exit_price = float(last["close"])
            exit_time = pd.Timestamp(last["timestamp"]).to_pydatetime()
            side = "LONG" if position == 1 else "SHORT"
            trade, cash = self._close_trade(
                symbol, spec, side, entry_time, exit_time, entry_price, exit_price, qty, cash,
                entry_reason, "end of data close", entry_margin
            )
            trades.append(trade)
            equity_rows.append({"timestamp": exit_time, "equity": cash})

        equity_curve = pd.DataFrame(equity_rows)
        result = self._metrics(symbol, params, trades, equity_curve)
        return BacktestRun(result=result, trades=trades, equity_curve=equity_curve, actions=actions)

    def run_with_splits(
        self,
        symbol: str,
        spec: InstrumentSpec,
        bars: pd.DataFrame,
        params: StrategyParams,
        events: pd.DataFrame | None = None,
    ) -> BacktestResult:
        full = self.run(symbol, spec, bars, params, events).result
        split = max(50, int(len(bars) * self.settings.backtest.train_ratio))
        if split >= len(bars) - 20:
            return full
        train = self.run(symbol, spec, bars.iloc[:split].copy(), params, events).result
        test = self.run(symbol, spec, bars.iloc[split:].copy(), params, events).result
        overfit = full.net_pnl > 0 and test.net_pnl < 0
        return BacktestResult(
            **{
                **full.to_dict(),
                "train_net_pnl": train.net_pnl,
                "test_net_pnl": test.net_pnl,
                "overfit_flag": overfit,
            }
        )

    def _risk_filter(self, spec: InstrumentSpec, params: StrategyParams):
        def check(action: StrategyAction, row: pd.Series) -> tuple[bool, str]:
            margin = spec.margin(action.price)
            stop_risk = self._stop_risk(spec, action)
            if params.risk_mode == "signal":
                return True, "signal mode allows margin warning"
            if params.risk_mode == "aggressive":
                risk_limit = max(self.settings.max_risk_per_trade * 1.5, self.settings.capital * 0.35)
                if margin <= self.settings.capital and stop_risk <= risk_limit:
                    return True, "aggressive margin ok"
                return False, f"margin {margin:.0f} or stop risk {stop_risk:.0f} exceeds aggressive limits"
            if margin <= self.settings.max_margin_budget and stop_risk <= self.settings.max_risk_per_trade:
                return True, "strict margin/risk ok"
            return (
                False,
                f"margin {margin:.0f} or stop risk {stop_risk:.0f} exceeds strict limits "
                f"{self.settings.max_margin_budget:.0f}/{self.settings.max_risk_per_trade:.0f}",
            )

        return check

    def _stop_risk(self, spec: InstrumentSpec, action: StrategyAction, qty: int = 1) -> float:
        if action.stop_price is None:
            return 0.0
        return abs(action.price - action.stop_price) * spec.multiplier * qty

    def _execution_risk_ok(
        self,
        spec: InstrumentSpec,
        params: StrategyParams,
        action: StrategyAction,
        execution_price: float,
        qty: int = 1,
    ) -> bool:
        margin = spec.margin(execution_price, qty)
        stop_risk = 0.0
        if action.stop_price is not None:
            stop_risk = abs(execution_price - action.stop_price) * spec.multiplier * qty
        if params.risk_mode == "signal":
            return True
        if params.risk_mode == "aggressive":
            risk_limit = max(self.settings.max_risk_per_trade * 1.5, self.settings.capital * 0.35)
            return margin <= self.settings.capital and stop_risk <= risk_limit
        return margin <= self.settings.max_margin_budget and stop_risk <= self.settings.max_risk_per_trade

    def _fill_price(self, row: pd.Series) -> float:
        open_price = float(row.get("open", 0.0) or 0.0)
        if open_price > 0:
            return open_price
        return float(row["close"])

    def _fees(self, spec: InstrumentSpec, price: float, qty: int) -> float:
        notional_fee = abs(price) * spec.multiplier * qty * spec.fee_rate
        slip = self.settings.backtest.slippage_ticks * spec.tick_size * spec.multiplier * qty
        return notional_fee + slip

    def _close_trade(
        self,
        symbol: str,
        spec: InstrumentSpec,
        side: str,
        entry_time,
        exit_time,
        entry_price: float,
        exit_price: float,
        qty: int,
        cash: float,
        entry_reason: str,
        exit_reason: str,
        margin: float,
    ) -> tuple[Trade, float]:
        direction = 1 if side == "LONG" else -1
        gross = (exit_price - entry_price) * spec.multiplier * qty * direction
        fees = self._fees(spec, exit_price, qty)
        net = gross - fees
        cash += gross - fees
        trade = Trade(
            symbol=symbol,
            contract=spec.ak_symbol,
            side=side,  # type: ignore[arg-type]
            entry_time=entry_time,
            exit_time=exit_time,
            entry_price=entry_price,
            exit_price=exit_price,
            qty=qty,
            gross_pnl=gross,
            fees=fees,
            net_pnl=net,
            entry_reason=entry_reason,
            exit_reason=exit_reason,
            margin=margin,
        )
        return trade, cash

    def _metrics(self, symbol: str, params: StrategyParams, trades: list[Trade], equity_curve: pd.DataFrame) -> BacktestResult:
        pnl = sum(trade.net_pnl for trade in trades)
        wins = [trade.net_pnl for trade in trades if trade.net_pnl > 0]
        losses = [trade.net_pnl for trade in trades if trade.net_pnl <= 0]
        profit_factor = sum(wins) / abs(sum(losses)) if losses and abs(sum(losses)) > 1e-9 else float("inf") if wins else 0.0
        max_dd = 0.0
        if not equity_curve.empty:
            running = equity_curve["equity"].cummax()
            drawdowns = equity_curve["equity"] - running
            max_dd = float(drawdowns.min())
        consecutive_losses = 0
        current = 0
        for trade in trades:
            if trade.net_pnl <= 0:
                current += 1
                consecutive_losses = max(consecutive_losses, current)
            else:
                current = 0
        return BacktestResult(
            symbol=symbol,
            timeframe=params.timeframe,
            strategy_id=params.strategy_id,
            params=params.to_dict(),
            net_pnl=float(pnl),
            total_return=float(pnl / self.settings.capital),
            max_drawdown=float(max_dd),
            win_rate=float(len(wins) / len(trades)) if trades else 0.0,
            profit_factor=float(profit_factor),
            trade_count=len(trades),
            avg_trade=float(pnl / len(trades)) if trades else 0.0,
            max_loss_trade=float(min(losses)) if losses else 0.0,
            consecutive_losses=consecutive_losses,
        )


def search_strategies(
    store: LocalStore,
    settings: Settings,
    fast: bool = False,
    limit_per_symbol: int | None = None,
    sides: tuple[str, ...] = ("both",),
    patterns: tuple[str, ...] | None = None,
    append: bool = False,
) -> list[BacktestResult]:
    params_grid = build_param_grid(settings.timeframes, fast=fast, sides=sides, patterns=patterns)
    params_by_timeframe: dict[str, list[StrategyParams]] = {}
    for params in params_grid:
        params_by_timeframe.setdefault(params.timeframe, []).append(params)
    backtester = Backtester(settings)
    events = store.read_events()
    results: list[BacktestResult] = []
    for symbol in settings.symbols:
        spec = settings.instruments[symbol]
        for timeframe in settings.timeframes:
            symbol_count = 0
            bars = store.read_bars(symbol, timeframe)
            if bars.empty or len(bars) < 80:
                continue
            for params in params_by_timeframe.get(timeframe, []):
                if limit_per_symbol and symbol_count >= limit_per_symbol:
                    break
                result = backtester.run_with_splits(symbol, spec, bars, params, events)
                results.append(result)
                symbol_count += 1
    merged = _merge_existing_results(store, results) if append else results
    store.write_backtest_results(merged)
    return sorted(merged, key=lambda r: r.net_pnl, reverse=True)


def parallel_search_strategies(
    store: LocalStore,
    settings: Settings,
    fast: bool = False,
    limit_per_symbol: int | None = None,
    workers: int = 4,
    progress: bool = True,
    sides: tuple[str, ...] = ("both",),
    patterns: tuple[str, ...] | None = None,
    append: bool = False,
) -> list[BacktestResult]:
    params_grid = build_param_grid(settings.timeframes, fast=fast, sides=sides, patterns=patterns)
    params_by_timeframe: dict[str, list[StrategyParams]] = {}
    for params in params_grid:
        params_by_timeframe.setdefault(params.timeframe, []).append(params)

    events = store.read_events()
    tasks = []
    for symbol in settings.symbols:
        spec = settings.instruments[symbol]
        for timeframe in settings.timeframes:
            bars = store.read_bars(symbol, timeframe)
            if bars.empty or len(bars) < 80:
                continue
            params = params_by_timeframe.get(timeframe, [])
            if limit_per_symbol:
                params = params[:limit_per_symbol]
            tasks.append((settings, symbol, spec, timeframe, bars, [p.to_dict() for p in params], events))

    if not tasks:
        store.write_backtest_results([])
        return []

    all_results: list[BacktestResult] = _load_existing_results(store) if append else []
    max_workers = max(1, int(workers))
    if max_workers == 1:
        for task in tasks:
            all_results.extend(_search_group_worker(task))
            store.write_backtest_results(all_results)
            if progress:
                print(f"completed {len(all_results)} results")
        return sorted(all_results, key=lambda r: r.net_pnl, reverse=True)

    with ProcessPoolExecutor(max_workers=max_workers) as pool:
        futures = [pool.submit(_search_group_worker, task) for task in tasks]
        completed = 0
        for future in as_completed(futures):
            group_results = future.result()
            all_results.extend(group_results)
            completed += 1
            store.write_backtest_results(all_results)
            if progress:
                print(f"completed groups {completed}/{len(tasks)}; results {len(all_results)}", flush=True)
    return sorted(all_results, key=lambda r: r.net_pnl, reverse=True)


def _search_group_worker(task) -> list[BacktestResult]:
    settings, symbol, spec, timeframe, bars, params_rows, events = task
    backtester = Backtester(settings)
    results: list[BacktestResult] = []
    for row in params_rows:
        params = StrategyParams.from_dict(row)
        results.append(backtester.run_with_splits(symbol, spec, bars, params, events))
    return results


def _load_existing_results(store: LocalStore) -> list[BacktestResult]:
    df = store.read_backtest_results()
    if df.empty:
        return []
    rows = []
    for _, row in df.iterrows():
        data = row.to_dict()
        params = data.pop("params", None)
        params_json = data.pop("params_json", None)
        if params is None and params_json:
            params = json.loads(params_json)
        data["params"] = params or {}
        rows.append(BacktestResult(**data))
    return rows


def _merge_existing_results(store: LocalStore, new_results: list[BacktestResult]) -> list[BacktestResult]:
    merged: dict[tuple[str, str, str], BacktestResult] = {}
    for result in _load_existing_results(store) + new_results:
        merged[(result.symbol, result.timeframe, result.strategy_id)] = result
    return list(merged.values())


def select_champions(results: Iterable[BacktestResult] | pd.DataFrame, settings: Settings) -> dict[str, dict]:
    if isinstance(results, pd.DataFrame):
        df = results.copy()
        if "params_json" in df.columns:
            df["params"] = df["params_json"].apply(json.loads)
    else:
        df = pd.DataFrame([result.to_dict() for result in results])
    champions: dict[str, dict] = {}
    if df.empty:
        return champions
    df = df.sort_values(["symbol", "net_pnl"], ascending=[True, False])
    for symbol, group in df.groupby("symbol"):
        tradable = group[
            (group["net_pnl"] > 0)
            & (group["trade_count"] >= settings.backtest.min_trades_for_champion)
            & (~group.get("overfit_flag", False).astype(bool))
        ]
        if tradable.empty:
            best = group.iloc[0].to_dict()
            champions[symbol] = {"status": "observe", "reason": "no stable positive strategy", "best": _clean_row(best)}
            continue
        best = tradable.iloc[0].to_dict()
        champions[symbol] = {"status": "active", "reason": "top non-overfit positive strategy", "best": _clean_row(best)}
    return champions


def _clean_row(row: dict) -> dict:
    out = {}
    for key, value in row.items():
        if isinstance(value, float) and value == float("inf"):
            out[key] = "inf"
        elif pd.isna(value) if not isinstance(value, (dict, list)) else False:
            out[key] = None
        else:
            out[key] = value
    return out
