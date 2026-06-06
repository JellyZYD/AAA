from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

import pandas as pd

from .backtest import Backtester
from .models import BacktestResult, Settings, StrategyParams
from .storage import LocalStore


@dataclass(frozen=True)
class RefinedEvaluation:
    symbol: str
    timeframe: str
    strategy_id: str
    pattern: str
    net_pnl: float
    test_net_pnl: float
    max_drawdown: float
    win_rate: float
    profit_factor: float
    trade_count: int
    rolling_windows: int
    rolling_positive_windows: int
    rolling_positive_rate: float
    rolling_min_net_pnl: float
    rolling_avg_net_pnl: float
    robust_score: float
    params_json: str


def refine_strategies(
    store: LocalStore,
    settings: Settings,
    reports_root: str | Path,
    patterns: tuple[str, ...] = ("donchian_atr", "tsmom_vol"),
    max_per_symbol: int = 40,
    rolling_windows: int = 4,
    top_seeds_per_symbol: int = 3,
) -> tuple[Path, list[RefinedEvaluation]]:
    results = store.read_backtest_results()
    if results.empty:
        raise RuntimeError("No backtest results found. Run qihuo backtest --search first.")
    reports = Path(reports_root)
    reports.mkdir(parents=True, exist_ok=True)

    seeds = _seed_rows(results, patterns, settings, top_seeds_per_symbol, store.read_profiles())
    candidates = _candidate_params_by_symbol(seeds, patterns, max_per_symbol)
    backtester = Backtester(settings)
    events = store.read_events()

    evaluations: list[RefinedEvaluation] = []
    new_results: list[BacktestResult] = []
    for (symbol, timeframe), params_list in candidates.items():
        spec = settings.instruments[symbol]
        bars = store.read_bars(symbol, timeframe)
        if bars.empty or len(bars) < 100:
            continue
        for params in params_list:
            result = backtester.run_with_splits(symbol, spec, bars, params, events)
            rolling = _rolling_metrics(backtester, symbol, spec, bars, params, events, rolling_windows)
            evaluation = _evaluation(result, params, rolling, settings)
            evaluations.append(evaluation)
            new_results.append(result)

    if new_results:
        merged = _merge_results(results, new_results)
        store.write_backtest_results(merged)

    if evaluations:
        frame = pd.DataFrame([asdict(item) for item in evaluations]).sort_values("robust_score", ascending=False)
    else:
        frame = pd.DataFrame()
    csv_path = reports / "refined_candidates.csv"
    frame.to_csv(csv_path, index=False, encoding="utf-8-sig")
    _write_refined_profile(store, frame, settings, reports)
    report_path = reports / "refinement_report.md"
    report_path.write_text(_render_refinement_report(frame, settings), encoding="utf-8")
    return report_path, evaluations


def _seed_rows(
    results: pd.DataFrame,
    patterns: tuple[str, ...],
    settings: Settings,
    top_seeds_per_symbol: int,
    profiles: dict[str, dict[str, dict]] | None = None,
) -> list[dict]:
    df = results.copy()
    if "params_json" in df.columns:
        df["params"] = df["params_json"].apply(json.loads)
    df["pattern"] = df["params"].apply(lambda item: item.get("pattern") if isinstance(item, dict) else None)
    df["overfit_flag"] = df.get("overfit_flag", False).astype(bool)
    for col in ["net_pnl", "test_net_pnl", "win_rate", "max_drawdown", "trade_count"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    valid = df[
        (df["pattern"].isin(patterns))
        & (df["net_pnl"] > 0)
        & (~df["overfit_flag"])
        & (df["trade_count"] >= settings.backtest.min_trades_for_champion)
    ].copy()
    if valid.empty:
        return []
    valid["seed_score"] = (
        valid["net_pnl"] * 0.35
        + valid["test_net_pnl"] * 2.0
        + valid["win_rate"] * settings.capital
        - valid["max_drawdown"].abs() * 0.75
    )
    seeds: list[dict] = _profile_seed_rows(profiles or {}, patterns)
    for _, group in valid.sort_values("seed_score", ascending=False).groupby("symbol", sort=False):
        seeds.extend(group.head(top_seeds_per_symbol).to_dict("records"))
    return seeds


def _profile_seed_rows(profiles: dict[str, dict[str, dict]], patterns: tuple[str, ...]) -> list[dict]:
    seeds: list[dict] = []
    seen: set[tuple[str, str]] = set()
    for profile in ("safe_winrate", "capital_safe", "balanced", "max_return"):
        for symbol, item in profiles.get(profile, {}).items():
            best = item.get("best") or {}
            params = best.get("params") or json.loads(str(best.get("params_json") or "{}"))
            if params.get("pattern") not in patterns:
                continue
            key = (str(symbol), str(best.get("strategy_id") or StrategyParams.from_dict(params).strategy_id))
            if key in seen:
                continue
            seen.add(key)
            seeds.append({**best, "symbol": symbol, "params": params})
    return seeds


def _candidate_params_by_symbol(
    seed_rows: Iterable[dict],
    patterns: tuple[str, ...],
    max_per_symbol: int,
) -> dict[tuple[str, str], list[StrategyParams]]:
    out: dict[tuple[str, str], dict[str, StrategyParams]] = {}
    for row in seed_rows:
        params = StrategyParams.from_dict(row["params"])
        if params.pattern not in patterns:
            continue
        key = (str(row["symbol"]), params.timeframe)
        bucket = out.setdefault(key, {})
        for candidate in _perturb(params):
            bucket.setdefault(candidate.strategy_id, candidate)
    limited: dict[tuple[str, str], list[StrategyParams]] = {}
    for key, bucket in out.items():
        limited[key] = list(bucket.values())[:max_per_symbol]
    return limited


def _perturb(params: StrategyParams) -> list[StrategyParams]:
    if params.pattern == "donchian_atr":
        lookbacks = _near_int(params.range_lookback, [8, 16, 24, 32, 48, 64])
        breakouts = _near_float(params.breakout_pct, [0.0, 0.001, 0.0015, 0.0025, 0.003, 0.005])
        atr_periods = _near_int(params.atr_period, [10, 14, 20])
        atr_mults = _near_float(params.atr_mult, [1.8, 2.0, 2.5, 3.0, 3.5])
        exits = _near_int(params.exit_lookback, [6, 8, 12, 16, 24, 32])
        holds = _near_int(params.max_hold_bars, [24, 32, 48, 64, 96])
        rows = []
        for lookback in lookbacks:
            for breakout in breakouts:
                for atr_period in atr_periods:
                    for atr_mult in atr_mults:
                        for exit_lookback in exits:
                            for max_hold in holds:
                                rows.append(
                                    StrategyParams(
                                        **{
                                            **params.to_dict(),
                                            "range_lookback": lookback,
                                            "breakout_pct": breakout,
                                            "atr_period": atr_period,
                                            "atr_mult": atr_mult,
                                            "exit_lookback": exit_lookback,
                                            "max_hold_bars": max_hold,
                                        }
                                    )
                                )
        return _sort_by_distance(params, rows)
    if params.pattern == "tsmom_vol":
        momentums = _near_int(params.momentum_lookback, [16, 24, 32, 48, 64, 96])
        vols = _near_int(params.vol_lookback, [16, 24, 32, 48, 64, 96])
        thresholds = _near_float(params.score_threshold, [0.2, 0.3, 0.4, 0.6, 0.8, 1.0])
        atr_periods = _near_int(params.atr_period, [10, 14, 20])
        atr_mults = _near_float(params.atr_mult, [1.8, 2.0, 2.5, 3.0, 3.5])
        holds = _near_int(params.max_hold_bars, [24, 32, 48, 64, 96])
        rows = []
        for momentum in momentums:
            for vol in vols:
                for threshold in thresholds:
                    for atr_period in atr_periods:
                        for atr_mult in atr_mults:
                            for max_hold in holds:
                                rows.append(
                                    StrategyParams(
                                        **{
                                            **params.to_dict(),
                                            "momentum_lookback": momentum,
                                            "vol_lookback": vol,
                                            "score_threshold": threshold,
                                            "atr_period": atr_period,
                                            "atr_mult": atr_mult,
                                            "max_hold_bars": max_hold,
                                        }
                                    )
                                )
        return _sort_by_distance(params, rows)
    return [params]


def _near_int(base: int, values: list[int]) -> list[int]:
    candidates = sorted(set(values + [base]), key=lambda value: (abs(value - base), value))
    return candidates[:3]


def _near_float(base: float, values: list[float]) -> list[float]:
    candidates = sorted(set(values + [base]), key=lambda value: (abs(value - base), value))
    return candidates[:3]


def _sort_by_distance(base: StrategyParams, candidates: list[StrategyParams]) -> list[StrategyParams]:
    base_dict = base.to_dict()

    def distance(candidate: StrategyParams) -> float:
        total = 0.0
        for key, value in candidate.to_dict().items():
            base_value = base_dict.get(key)
            if isinstance(value, (int, float)) and isinstance(base_value, (int, float)):
                denom = abs(float(base_value)) or 1.0
                total += abs(float(value) - float(base_value)) / denom
        return total

    return sorted(candidates, key=lambda item: (distance(item), item.strategy_id))


def _rolling_metrics(
    backtester: Backtester,
    symbol: str,
    spec,
    bars: pd.DataFrame,
    params: StrategyParams,
    events: pd.DataFrame | None,
    windows: int,
) -> dict[str, float]:
    if windows <= 1 or len(bars) < 160:
        return {"windows": 0, "positive": 0, "positive_rate": 0.0, "min_net": 0.0, "avg_net": 0.0}
    pnls = []
    size = len(bars) // windows
    for index in range(windows):
        start = index * size
        end = len(bars) if index == windows - 1 else (index + 1) * size
        chunk = bars.iloc[start:end].copy()
        if len(chunk) < 80:
            continue
        result = backtester.run(symbol, spec, chunk, params, events).result
        pnls.append(result.net_pnl)
    if not pnls:
        return {"windows": 0, "positive": 0, "positive_rate": 0.0, "min_net": 0.0, "avg_net": 0.0}
    positive = sum(1 for pnl in pnls if pnl > 0)
    return {
        "windows": len(pnls),
        "positive": positive,
        "positive_rate": positive / len(pnls),
        "min_net": min(pnls),
        "avg_net": sum(pnls) / len(pnls),
    }


def _evaluation(
    result: BacktestResult,
    params: StrategyParams,
    rolling: dict[str, float],
    settings: Settings,
) -> RefinedEvaluation:
    test = float(result.test_net_pnl or 0.0)
    drawdown_abs = abs(float(result.max_drawdown))
    robust_score = (
        result.net_pnl * 0.30
        + test * 2.5
        + result.win_rate * settings.capital * 2.0
        + min(float(result.profit_factor), 5.0) * 1000.0
        + rolling["positive_rate"] * settings.capital * 2.0
        + min(rolling["min_net"], 0.0) * 1.5
        - drawdown_abs * 1.2
    )
    if drawdown_abs > settings.capital:
        robust_score -= (drawdown_abs - settings.capital) * 1.5
    if test <= 0:
        robust_score += test * 2.0
    return RefinedEvaluation(
        symbol=result.symbol,
        timeframe=result.timeframe,
        strategy_id=result.strategy_id,
        pattern=params.pattern,
        net_pnl=result.net_pnl,
        test_net_pnl=test,
        max_drawdown=result.max_drawdown,
        win_rate=result.win_rate,
        profit_factor=result.profit_factor,
        trade_count=result.trade_count,
        rolling_windows=int(rolling["windows"]),
        rolling_positive_windows=int(rolling["positive"]),
        rolling_positive_rate=float(rolling["positive_rate"]),
        rolling_min_net_pnl=float(rolling["min_net"]),
        rolling_avg_net_pnl=float(rolling["avg_net"]),
        robust_score=robust_score,
        params_json=json.dumps(params.to_dict(), ensure_ascii=False, sort_keys=True),
    )


def _merge_results(existing: pd.DataFrame, new_results: list[BacktestResult]) -> list[BacktestResult]:
    rows: dict[tuple[str, str, str], BacktestResult] = {}
    for _, row in existing.iterrows():
        data = row.to_dict()
        params_json = data.pop("params_json", None)
        params = data.pop("params", None)
        if params is None and params_json:
            params = json.loads(params_json)
        data["params"] = params or {}
        rows[(data["symbol"], data["timeframe"], data["strategy_id"])] = BacktestResult(**data)
    for result in new_results:
        rows[(result.symbol, result.timeframe, result.strategy_id)] = result
    return list(rows.values())


def _render_refinement_report(frame: pd.DataFrame, settings: Settings) -> str:
    lines = [
        "# 局部扰动与滚动验证报告",
        "",
        f"- 初始资金: {settings.capital:.0f}",
        f"- 候选数量: {0 if frame.empty else len(frame)}",
        "- 评分偏向: 样本外收益、低回撤、滚动窗口稳定性、胜率和利润因子。",
        "",
    ]
    if frame.empty:
        lines.append("没有生成候选。")
        return "\n".join(lines) + "\n"
    top = frame.sort_values("robust_score", ascending=False).head(30)
    lines.extend(
        [
            "## Top 30 稳健候选",
            "",
            "|排名|品种|策略|周期|稳健分|净收益|样本外|回撤|胜率|滚动胜率|滚动最差|交易数|",
            "|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for rank, (_, row) in enumerate(top.iterrows(), 1):
        lines.append(
            "|{rank}|{symbol}|{pattern}|{timeframe}|{score:.1f}|{net:.0f}|{test:.0f}|{dd:.0f}|{win:.1%}|{roll:.1%}|{roll_min:.0f}|{trades}|".format(
                rank=rank,
                symbol=row["symbol"],
                pattern=row["pattern"],
                timeframe=row["timeframe"],
                score=float(row["robust_score"]),
                net=float(row["net_pnl"]),
                test=float(row["test_net_pnl"]),
                dd=float(row["max_drawdown"]),
                win=float(row["win_rate"]),
                roll=float(row["rolling_positive_rate"]),
                roll_min=float(row["rolling_min_net_pnl"]),
                trades=int(row["trade_count"]),
            )
        )
    lines.extend(["", "## 每品种首选", ""])
    for symbol, group in frame.sort_values("robust_score", ascending=False).groupby("symbol", sort=False):
        row = group.iloc[0]
        lines.append(
            f"- {symbol}: `{row['strategy_id']}`，稳健分 {float(row['robust_score']):.1f}，"
            f"净收益 {float(row['net_pnl']):.0f}，样本外 {float(row['test_net_pnl']):.0f}，"
            f"回撤 {float(row['max_drawdown']):.0f}，滚动胜率 {float(row['rolling_positive_rate']):.1%}。"
        )
    return "\n".join(lines) + "\n"


def _write_refined_profile(store: LocalStore, frame: pd.DataFrame, settings: Settings, reports: Path) -> None:
    if frame.empty:
        return
    profiles = store.read_profiles()
    refined: dict[str, dict] = {}
    for symbol, group in frame.sort_values("robust_score", ascending=False).groupby("symbol", sort=False):
        tradable = group[
            (group["test_net_pnl"] > 0)
            & (group["trade_count"] >= 20)
            & (group["max_drawdown"].abs() <= settings.capital)
            & (group["rolling_positive_rate"] >= 0.5)
        ]
        selected = tradable.iloc[0] if not tradable.empty else group.iloc[0]
        row = selected.to_dict()
        row["params"] = json.loads(str(row.get("params_json") or "{}"))
        row["overfit_flag"] = bool(row.get("test_net_pnl", 0) <= 0)
        row["strategy_id"] = row.get("strategy_id") or StrategyParams.from_dict(row["params"]).strategy_id
        status = "active" if not tradable.empty else "observe"
        reason = "rolling-validated capital-safe candidate" if status == "active" else "best refined candidate exceeds capital safety filters"
        refined[str(symbol)] = {"status": status, "reason": reason, "best": row}
    profiles["refined_robust"] = refined
    store.write_profiles(profiles)
    profiles_path = reports / "strategy_profiles.json"
    profiles_path.write_text(json.dumps(profiles, ensure_ascii=False, indent=2), encoding="utf-8")
