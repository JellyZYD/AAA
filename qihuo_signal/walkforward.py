from __future__ import annotations

import json
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import asdict, dataclass
from pathlib import Path

import pandas as pd

from .backtest import Backtester
from .models import BacktestResult, Settings, StrategyParams
from .storage import LocalStore


MIN_ACTIVE_POSITIVE_RATE = 0.75
MIN_ACTIVE_RETURN_DRAWDOWN = 1.2
MIN_ACTIVE_TEST_NET = 500.0
MAX_ACTIVE_DRAWDOWN_FRACTION = 0.8


@dataclass(frozen=True)
class WalkForwardRow:
    symbol: str
    window: int
    timeframe: str
    pattern: str
    selected_strategy_id: str
    train_score: float
    train_net_pnl: float
    train_max_drawdown: float
    train_trade_count: int
    test_net_pnl: float
    test_max_drawdown: float
    test_win_rate: float
    test_trade_count: int
    test_start: str
    test_end: str


@dataclass(frozen=True)
class WalkForwardSummary:
    symbol: str
    status: str
    selected_strategy_id: str
    pattern: str
    timeframe: str
    windows: int
    positive_windows: int
    positive_rate: float
    total_test_net_pnl: float
    avg_test_net_pnl: float
    min_window_net_pnl: float
    worst_test_drawdown: float
    avg_test_win_rate: float
    total_test_trades: int
    walk_forward_score: float
    reason: str
    params_json: str


def run_walk_forward(
    store: LocalStore,
    settings: Settings,
    reports_root: str | Path,
    folds: int = 5,
    max_per_symbol: int = 24,
    workers: int = 6,
) -> tuple[Path, list[WalkForwardSummary]]:
    reports = Path(reports_root)
    reports.mkdir(parents=True, exist_ok=True)
    candidates = _load_candidates(reports, store, settings, max_per_symbol)
    events = store.read_events()
    rows: list[WalkForwardRow] = []
    summaries: list[WalkForwardSummary] = []
    tasks = []

    for (symbol, timeframe), group in candidates.groupby(["symbol", "timeframe"], sort=False):
        bars = store.read_bars(str(symbol), str(timeframe))
        if len(bars) < folds * 40:
            continue
        tasks.append((settings, str(symbol), str(timeframe), group.copy(), bars, events, folds))

    if tasks:
        worker_count = min(max(1, int(workers)), len(tasks))
        if worker_count == 1:
            for task in tasks:
                group_rows, summary = _walk_forward_group_worker(task)
                rows.extend(group_rows)
                if summary is not None:
                    summaries.append(summary)
        else:
            with ProcessPoolExecutor(max_workers=worker_count) as pool:
                futures = [pool.submit(_walk_forward_group_worker, task) for task in tasks]
                for completed, future in enumerate(as_completed(futures), start=1):
                    group_rows, summary = future.result()
                    rows.extend(group_rows)
                    if summary is not None:
                        summaries.append(summary)
                    print(f"walk-forward completed groups {completed}/{len(tasks)}", flush=True)

    row_frame = pd.DataFrame([asdict(row) for row in rows])
    summary_frame = pd.DataFrame([asdict(item) for item in summaries]).sort_values("walk_forward_score", ascending=False)
    row_frame.to_csv(reports / "walk_forward_windows.csv", index=False, encoding="utf-8-sig")
    summary_frame.to_csv(reports / "walk_forward_summary.csv", index=False, encoding="utf-8-sig")
    _write_walk_forward_profile(store, summary_frame, reports)
    report_path = reports / "walk_forward_report.md"
    report_path.write_text(_render_report(summary_frame, row_frame, settings), encoding="utf-8")
    return report_path, summaries


def _walk_forward_group_worker(task) -> tuple[list[WalkForwardRow], WalkForwardSummary | None]:
    settings, symbol, _timeframe, candidates, bars, events, folds = task
    spec = settings.instruments.get(str(symbol))
    if spec is None:
        return [], None
    backtester = Backtester(settings)
    symbol_rows: list[WalkForwardRow] = []
    for window in range(1, folds):
        selected = _select_for_window(backtester, settings, str(symbol), spec, bars, candidates, events, folds, window)
        if selected is None:
            continue
        params, train_result, train_score, test_result, test_start, test_end = selected
        symbol_rows.append(
            WalkForwardRow(
                symbol=str(symbol),
                window=window,
                timeframe=params.timeframe,
                pattern=params.pattern,
                selected_strategy_id=params.strategy_id,
                train_score=train_score,
                train_net_pnl=train_result.net_pnl,
                train_max_drawdown=train_result.max_drawdown,
                train_trade_count=train_result.trade_count,
                test_net_pnl=test_result.net_pnl,
                test_max_drawdown=test_result.max_drawdown,
                test_win_rate=test_result.win_rate,
                test_trade_count=test_result.trade_count,
                test_start=test_start,
                test_end=test_end,
            )
        )
    if not symbol_rows:
        return [], None
    summary = _summarize_symbol(str(symbol), candidates, bars, symbol_rows, settings, backtester, events)
    return symbol_rows, summary


def _load_candidates(reports: Path, store: LocalStore, settings: Settings, max_per_symbol: int) -> pd.DataFrame:
    del reports, store
    params_grid = _static_walk_forward_params(settings.timeframes)
    rows = [
        {
            "symbol": symbol,
            "timeframe": params.timeframe,
            "pattern": params.pattern,
            "strategy_id": params.strategy_id,
            "params_json": json.dumps(params.to_dict(), ensure_ascii=False, sort_keys=True),
            "robust_score": 0.0,
        }
        for symbol in settings.symbols
        for params in params_grid
    ]
    if not rows:
        raise RuntimeError("No causal walk-forward candidates generated.")
    frame = pd.DataFrame(rows)
    frame = frame.drop_duplicates(subset=["symbol", "strategy_id"])
    frame["rank"] = frame.groupby(["symbol", "timeframe", "pattern"]).cumcount() + 1
    return frame[frame["rank"] <= max_per_symbol].copy()


def _static_walk_forward_params(timeframes: tuple[str, ...]) -> list[StrategyParams]:
    params: list[StrategyParams] = []
    for timeframe in timeframes:
        for pattern in ("swing_reversal", "trend_failure"):
            for breakout_pct in (0.0015, 0.003):
                for max_hold in (32, 64):
                    params.append(
                        StrategyParams(
                            pattern=pattern,  # type: ignore[arg-type]
                            side="both",
                            timeframe=timeframe,
                            swing_window=3,
                            min_swing_pct=0.006,
                            breakout_pct=breakout_pct,
                            max_hold_bars=max_hold,
                            risk_mode="strict",
                        )
                    )
        for pattern in ("breakout", "failed_breakout"):
            for lookback in (16, 32):
                for breakout_pct in (0.0015, 0.003):
                    for max_hold in (32, 64):
                        params.append(
                            StrategyParams(
                                pattern=pattern,  # type: ignore[arg-type]
                                side="both",
                                timeframe=timeframe,
                                range_lookback=lookback,
                                breakout_pct=breakout_pct,
                                max_hold_bars=max_hold,
                                risk_mode="strict",
                            )
                        )
        for lookback in (16, 32):
            for breakout_pct in (0.0015, 0.003):
                for atr_mult in (2.0, 3.0):
                    for max_hold in (32, 64):
                        params.append(
                            StrategyParams(
                                pattern="donchian_atr",
                                side="both",
                                timeframe=timeframe,
                                range_lookback=lookback,
                                breakout_pct=breakout_pct,
                                atr_period=14,
                                atr_mult=atr_mult,
                                exit_lookback=12,
                                max_hold_bars=max_hold,
                                risk_mode="strict",
                            )
                        )
        for momentum_lookback in (24, 48):
            for vol_lookback in (24, 48):
                for threshold in (0.4, 0.8):
                    for atr_mult in (2.0, 3.0):
                        params.append(
                            StrategyParams(
                                pattern="tsmom_vol",
                                side="both",
                                timeframe=timeframe,
                                momentum_lookback=momentum_lookback,
                                vol_lookback=vol_lookback,
                                score_threshold=threshold,
                                atr_period=14,
                                atr_mult=atr_mult,
                                max_hold_bars=64,
                                risk_mode="strict",
                            )
                        )
        for lookback in (16, 32):
            for breakout_pct in (0.0015, 0.003):
                for threshold in (0.75, 0.9):
                    for atr_mult in (2.0, 3.0):
                        for max_hold in (32, 64):
                            params.append(
                                StrategyParams(
                                    pattern="vol_breakout",
                                    side="both",
                                    timeframe=timeframe,
                                    range_lookback=lookback,
                                    breakout_pct=breakout_pct,
                                    atr_period=14,
                                    atr_mult=atr_mult,
                                    exit_lookback=16,
                                    max_hold_bars=max_hold,
                                    vol_lookback=48,
                                    score_threshold=threshold,
                                    risk_mode="strict",
                                )
                            )
        if timeframe == "1d":
            for momentum_lookback in (24, 48):
                for vol_lookback in (24, 48):
                    for threshold in (0.4, 0.8):
                        for atr_mult in (2.0, 3.0):
                            params.append(
                                StrategyParams(
                                    pattern="carry_tsmom",
                                    side="both",
                                    timeframe=timeframe,
                                    momentum_lookback=momentum_lookback,
                                    vol_lookback=vol_lookback,
                                    score_threshold=threshold,
                                    atr_period=14,
                                    atr_mult=atr_mult,
                                    max_hold_bars=64,
                                    risk_mode="strict",
                                )
                            )
    return params


def _load_backtest_candidates(store: LocalStore, settings: Settings) -> pd.DataFrame:
    results = store.read_backtest_results()
    if results.empty:
        return pd.DataFrame()
    frame = results.copy()
    frame["params"] = frame["params_json"].apply(json.loads)
    frame["pattern"] = frame["params"].apply(lambda item: item.get("pattern") if isinstance(item, dict) else None)
    frame = frame[frame["pattern"].isin({"donchian_atr", "tsmom_vol", "vol_breakout", "carry_tsmom"})].copy()
    if frame.empty:
        return pd.DataFrame()
    frame["overfit_flag"] = frame.get("overfit_flag", False).astype(bool)
    for col in ["net_pnl", "test_net_pnl", "win_rate", "profit_factor", "max_drawdown", "trade_count"]:
        frame[col] = pd.to_numeric(frame[col], errors="coerce").fillna(0.0)
    valid = frame[(frame["net_pnl"] > 0) & (~frame["overfit_flag"]) & (frame["trade_count"] >= 3)].copy()
    if valid.empty:
        return pd.DataFrame()
    valid["robust_score"] = (
        valid["net_pnl"] * 0.3
        + valid["test_net_pnl"] * 2.0
        + valid["win_rate"] * settings.capital
        + valid["profit_factor"].clip(upper=5.0) * 800.0
        - valid["max_drawdown"].abs() * 0.8
    )
    valid = valid.sort_values("robust_score", ascending=False)
    selected = valid.groupby(["symbol", "timeframe", "pattern"], sort=False).head(3)
    return selected[["symbol", "timeframe", "strategy_id", "params_json", "robust_score"]].copy()


def _select_for_window(
    backtester: Backtester,
    settings: Settings,
    symbol: str,
    spec,
    bars: pd.DataFrame,
    candidates: pd.DataFrame,
    events: pd.DataFrame | None,
    folds: int,
    window: int,
):
    best = None
    if len(bars) < folds * 40:
        return None
    test_start_i, test_end_i = _fold_bounds(len(bars), folds, window)
    train = bars.iloc[:test_start_i].copy()
    test = bars.iloc[test_start_i:test_end_i].copy()
    if len(train) < 80 or len(test) < 30:
        return None
    for _, row in candidates.iterrows():
        params = StrategyParams.from_dict(json.loads(str(row["params_json"])))
        train_result = backtester.run(symbol, spec, train, params, events).result
        score = _train_score(train_result, settings)
        if best is None or score > best[2]:
            test_result = backtester.run(symbol, spec, test, params, events).result
            test_start = str(pd.Timestamp(test.iloc[0]["timestamp"]))
            test_end = str(pd.Timestamp(test.iloc[-1]["timestamp"]))
            best = (params, train_result, score, test_result, test_start, test_end)
    return best


def _fold_bounds(length: int, folds: int, window: int) -> tuple[int, int]:
    size = length // folds
    start = window * size
    end = length if window == folds - 1 else (window + 1) * size
    return start, end


def _train_score(result: BacktestResult, settings: Settings) -> float:
    drawdown = abs(result.max_drawdown)
    score = (
        result.net_pnl * 0.5
        + result.win_rate * settings.capital * 1.5
        + min(float(result.profit_factor), 5.0) * 800
        - drawdown * 0.9
    )
    if result.trade_count < settings.backtest.min_trades_for_champion:
        score -= settings.capital * 2
    if result.net_pnl <= 0:
        score += result.net_pnl * 2
    if drawdown > settings.capital:
        score -= (drawdown - settings.capital) * 1.5
    return score


def _summarize_symbol(
    symbol: str,
    candidates: pd.DataFrame,
    bars: pd.DataFrame,
    rows: list[WalkForwardRow],
    settings: Settings,
    backtester: Backtester,
    events: pd.DataFrame | None,
) -> WalkForwardSummary:
    total = sum(row.test_net_pnl for row in rows)
    positive = sum(1 for row in rows if row.test_net_pnl > 0)
    min_net = min(row.test_net_pnl for row in rows)
    worst_dd = min(row.test_max_drawdown for row in rows)
    avg_win = sum(row.test_win_rate for row in rows) / len(rows)
    trades = sum(row.test_trade_count for row in rows)
    positive_rate = positive / len(rows)
    selected = _select_full_history_candidate(symbol, candidates, bars, settings, backtester, events)
    params, selected_score = selected
    drawdown_abs = abs(worst_dd)
    reward_drawdown = total / drawdown_abs if drawdown_abs > 1e-9 else float("inf") if total > 0 else 0.0
    drawdown_ok = drawdown_abs <= settings.capital * MAX_ACTIVE_DRAWDOWN_FRACTION
    active = (
        total >= MIN_ACTIVE_TEST_NET
        and positive_rate >= MIN_ACTIVE_POSITIVE_RATE
        and reward_drawdown >= MIN_ACTIVE_RETURN_DRAWDOWN
        and drawdown_ok
        and trades >= settings.backtest.min_trades_for_champion
    )
    score = (
        total * 2.0
        + positive_rate * settings.capital * 2.0
        + avg_win * settings.capital
        + min(min_net, 0.0) * 2.0
        - abs(worst_dd) * 1.2
    )
    reason = (
        "walk-forward positive, stable, and reward/drawdown qualified"
        if active
        else (
            "walk-forward rejected: requires positive_rate>=75%, "
            "net/max_drawdown>=1.2, net>=500, and drawdown<=80% capital"
        )
    )
    return WalkForwardSummary(
        symbol=symbol,
        status="active" if active else "observe",
        selected_strategy_id=params.strategy_id,
        pattern=params.pattern,
        timeframe=params.timeframe,
        windows=len(rows),
        positive_windows=positive,
        positive_rate=positive_rate,
        total_test_net_pnl=total,
        avg_test_net_pnl=total / len(rows),
        min_window_net_pnl=min_net,
        worst_test_drawdown=worst_dd,
        avg_test_win_rate=avg_win,
        total_test_trades=trades,
        walk_forward_score=score + selected_score * 0.1,
        reason=reason,
        params_json=json.dumps(params.to_dict(), ensure_ascii=False, sort_keys=True),
    )


def _select_full_history_candidate(
    symbol: str,
    candidates: pd.DataFrame,
    bars: pd.DataFrame,
    settings: Settings,
    backtester: Backtester,
    events: pd.DataFrame | None,
) -> tuple[StrategyParams, float]:
    best: tuple[StrategyParams, float] | None = None
    spec = settings.instruments[symbol]
    for _, row in candidates.iterrows():
        params = StrategyParams.from_dict(json.loads(str(row["params_json"])))
        if bars.empty:
            continue
        result = backtester.run(symbol, spec, bars, params, events).result
        score = _train_score(result, settings)
        if best is None or score > best[1]:
            best = (params, score)
    if best is None:
        first = candidates.iloc[0]
        return StrategyParams.from_dict(json.loads(str(first["params_json"]))), 0.0
    return best


def _write_walk_forward_profile(store: LocalStore, frame: pd.DataFrame, reports: Path) -> None:
    if frame.empty:
        return
    profiles = store.read_profiles()
    profile: dict[str, dict] = {}
    ranked = frame.copy()
    ranked["_status_rank"] = (ranked["status"] != "active").astype(int)
    selected = (
        ranked.sort_values(["symbol", "_status_rank", "walk_forward_score"], ascending=[True, True, False])
        .groupby("symbol", sort=False)
        .head(1)
    )
    for _, row in selected.iterrows():
        params = json.loads(str(row["params_json"]))
        best = row.to_dict()
        best.pop("_status_rank", None)
        best["params"] = params
        best["strategy_id"] = row["selected_strategy_id"]
        profile[str(row["symbol"])] = {"status": row["status"], "reason": row["reason"], "best": best}
    profiles["walk_forward"] = profile
    store.write_profiles(profiles)
    (reports / "strategy_profiles.json").write_text(json.dumps(profiles, ensure_ascii=False, indent=2), encoding="utf-8")


def _render_report(summary: pd.DataFrame, windows: pd.DataFrame, settings: Settings) -> str:
    lines = [
        "# Walk-Forward 验证报告",
        "",
        f"- 初始资金: {settings.capital:.0f}",
        "- 方法: 每个测试窗口只用此前历史选择参数，再在下一窗口测试。",
        "- 画像: `walk_forward`，只把总测试收益为正、正收益窗口不少于一半、测试回撤不超过本金的品种设为 active。",
        "",
    ]
    if summary.empty:
        return "\n".join(lines + ["没有可验证候选。", ""]) 
    top = summary.sort_values("walk_forward_score", ascending=False)
    lines.extend(
        [
            "## 汇总",
            "",
            "|品种|状态|策略|周期|WF分|测试净收益|正窗口|最差窗口|最差回撤|平均胜率|交易数|",
            "|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for _, row in top.iterrows():
        lines.append(
            "|{symbol}|{status}|{pattern}|{timeframe}|{score:.1f}|{net:.0f}|{pos}/{windows}|{min_net:.0f}|{dd:.0f}|{win:.1%}|{trades}|".format(
                symbol=row["symbol"],
                status=row["status"],
                pattern=row["pattern"],
                timeframe=row["timeframe"],
                score=float(row["walk_forward_score"]),
                net=float(row["total_test_net_pnl"]),
                pos=int(row["positive_windows"]),
                windows=int(row["windows"]),
                min_net=float(row["min_window_net_pnl"]),
                dd=float(row["worst_test_drawdown"]),
                win=float(row["avg_test_win_rate"]),
                trades=int(row["total_test_trades"]),
            )
        )
    lines.extend(["", "## 每窗口明细", ""])
    for (symbol, timeframe), group in windows.groupby(["symbol", "timeframe"], sort=False):
        lines.append(f"### {symbol} {timeframe}")
        for _, row in group.iterrows():
            lines.append(
                f"- 窗口 {int(row['window'])}: 测试 {row['test_start']} 至 {row['test_end']}，"
                f"净收益 {float(row['test_net_pnl']):.0f}，回撤 {float(row['test_max_drawdown']):.0f}，"
                f"胜率 {float(row['test_win_rate']):.1%}，`{row['selected_strategy_id']}`。"
            )
    return "\n".join(lines) + "\n"
