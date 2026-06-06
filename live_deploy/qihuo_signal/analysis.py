from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from .backtest import select_champions
from .models import Settings
from .storage import LocalStore


def analyze_results(store: LocalStore, settings: Settings, reports_root: str | Path) -> tuple[Path, dict[str, dict]]:
    results = store.read_backtest_results()
    reports = Path(reports_root)
    reports.mkdir(parents=True, exist_ok=True)
    existing_profiles = store.read_profiles()
    champions = select_champions(results, settings)
    profiles = select_profiles(results, settings)
    if "refined_robust" in existing_profiles:
        profiles["refined_robust"] = existing_profiles["refined_robust"]
    store.write_champions(champions)
    store.write_profiles(profiles)
    report_path = reports / "backtest_report.md"
    report_path.write_text(render_report(results, champions, settings, profiles), encoding="utf-8")
    json_path = reports / "champions.json"
    json_path.write_text(json.dumps(champions, ensure_ascii=False, indent=2), encoding="utf-8")
    profiles_path = reports / "strategy_profiles.json"
    profiles_path.write_text(json.dumps(profiles, ensure_ascii=False, indent=2), encoding="utf-8")
    write_summary_tables(results, profiles, reports)
    return report_path, champions


def render_report(
    results: pd.DataFrame,
    champions: dict[str, dict],
    settings: Settings,
    profiles: dict[str, dict[str, dict]] | None = None,
) -> str:
    lines = [
        "# 期货策略回测报告",
        "",
        f"- 初始资金: {settings.capital:.0f}",
        f"- 保证金预算: {settings.max_margin_budget:.0f}",
        f"- 回测目标: {settings.backtest.objective}",
        "",
    ]
    if results.empty:
        lines += ["没有回测结果。请先运行 `qihuo backtest --search`。", ""]
        return "\n".join(lines)

    df = results.copy()
    top = df.sort_values("net_pnl", ascending=False).head(20)
    lines += [
        "## Top 20 策略",
        "",
        "|排名|品种|周期|净收益|回撤|胜率|交易数|样本外|过拟合|策略|",
        "|---:|---|---|---:|---:|---:|---:|---:|---|---|",
    ]
    for rank, (_, row) in enumerate(top.iterrows(), 1):
        lines.append(
            "|{rank}|{symbol}|{timeframe}|{net:.2f}|{dd:.2f}|{win:.1%}|{trades}|{test}|{overfit}|`{strategy}`|".format(
                rank=rank,
                symbol=row["symbol"],
                timeframe=row["timeframe"],
                net=float(row["net_pnl"]),
                dd=float(row["max_drawdown"]),
                win=float(row["win_rate"]),
                trades=int(row["trade_count"]),
                test=_fmt(row.get("test_net_pnl")),
                overfit="Y" if bool(row.get("overfit_flag", False)) else "",
                strategy=str(row["strategy_id"]),
            )
        )

    lines += ["", "## Champion 策略", ""]
    for symbol in settings.symbols:
        champion = champions.get(symbol)
        if not champion:
            lines.append(f"- {symbol}: 未找到回测结果。")
            continue
        best = champion["best"]
        status = "启用" if champion["status"] == "active" else "观察"
        lines.append(
            f"- {symbol}: {status}，净收益 {_fmt(best.get('net_pnl'))}，样本外 {_fmt(best.get('test_net_pnl'))}，"
            f"交易数 {best.get('trade_count')}，策略 `{best.get('strategy_id')}`。"
        )

    if profiles:
        lines += ["", "## 策略画像", ""]
        labels = {"max_return": "最高收益", "max_winrate": "最高胜率", "balanced": "均衡评分"}
        for profile, items in profiles.items():
            lines.append(f"### {labels.get(profile, profile)}")
            for symbol in settings.symbols:
                best = items.get(symbol, {}).get("best")
                if not best:
                    lines.append(f"- {symbol}: 无。")
                    continue
                lines.append(
                    f"- {symbol}: 净收益 {_fmt(best.get('net_pnl'))}，胜率 {float(best.get('win_rate') or 0):.1%}，"
                    f"交易 {best.get('trade_count')}，样本外 {_fmt(best.get('test_net_pnl'))}，"
                    f"`{best.get('strategy_id')}`。"
                )

    lines += ["", "## 改进建议", ""]
    lines.extend(_suggestions(df, champions))
    return "\n".join(lines) + "\n"


def select_profiles(results: pd.DataFrame, settings: Settings) -> dict[str, dict[str, dict]]:
    profiles = {"max_return": {}, "max_winrate": {}, "balanced": {}, "capital_safe": {}, "safe_winrate": {}}
    if results.empty:
        return profiles
    df = results.copy()
    if "params_json" in df.columns:
        df["params"] = df["params_json"].apply(json.loads)
    df["overfit_flag"] = df.get("overfit_flag", False).astype(bool)
    valid = df[(df["net_pnl"] > 0) & (~df["overfit_flag"])].copy()
    if valid.empty:
        return profiles
    valid["test_net_pnl"] = valid["test_net_pnl"].fillna(0)
    for col in ["net_pnl", "test_net_pnl", "win_rate", "max_drawdown", "trade_count"]:
        valid[col] = pd.to_numeric(valid[col], errors="coerce").fillna(0)
    valid["balanced_score"] = (
        valid["net_pnl"]
        + valid["test_net_pnl"] * 1.5
        + valid["win_rate"] * settings.capital
        - valid["max_drawdown"].abs() * 0.35
    )
    for symbol in settings.symbols:
        group = valid[valid["symbol"] == symbol]
        if group.empty:
            continue
        profiles["max_return"][symbol] = {"best": _clean(group.sort_values("net_pnl", ascending=False).iloc[0].to_dict())}
        win_group = group[group["trade_count"] >= 20]
        if not win_group.empty:
            row = win_group.sort_values(["win_rate", "net_pnl"], ascending=[False, False]).iloc[0].to_dict()
            profiles["max_winrate"][symbol] = {"best": _clean(row)}
        safe_group = group[(group["trade_count"] >= 20) & (group["max_drawdown"].abs() <= settings.capital)]
        if not safe_group.empty:
            row = safe_group.sort_values("balanced_score", ascending=False).iloc[0].to_dict()
            profiles["capital_safe"][symbol] = {"best": _clean(row)}
            win_row = safe_group.sort_values(["win_rate", "net_pnl"], ascending=[False, False]).iloc[0].to_dict()
            profiles["safe_winrate"][symbol] = {"best": _clean(win_row)}
        balanced_group = safe_group if not safe_group.empty else group[group["trade_count"] >= 20]
        if not balanced_group.empty:
            row = balanced_group.sort_values("balanced_score", ascending=False).iloc[0].to_dict()
            profiles["balanced"][symbol] = {"best": _clean(row)}
    return profiles


def write_summary_tables(results: pd.DataFrame, profiles: dict[str, dict[str, dict]], reports: Path) -> None:
    if results.empty:
        return
    df = results.copy()
    df["overfit_flag"] = df.get("overfit_flag", False).astype(bool)
    for col in ["net_pnl", "test_net_pnl", "win_rate", "max_drawdown", "profit_factor", "trade_count"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    valid = df[(df["net_pnl"] > 0) & (~df["overfit_flag"]) & (df["trade_count"] >= 20)].copy()
    cols = [
        "symbol",
        "timeframe",
        "net_pnl",
        "max_drawdown",
        "win_rate",
        "profit_factor",
        "trade_count",
        "test_net_pnl",
        "strategy_id",
    ]
    valid.sort_values("net_pnl", ascending=False).head(100)[cols].to_csv(
        reports / "top_return.csv", index=False, encoding="utf-8-sig"
    )
    valid.sort_values(["win_rate", "net_pnl"], ascending=[False, False]).head(100)[cols].to_csv(
        reports / "top_winrate.csv", index=False, encoding="utf-8-sig"
    )
    rows = []
    for profile, items in profiles.items():
        for symbol, item in items.items():
            best = item.get("best", {})
            rows.append({"profile": profile, "symbol": symbol, **best})
    if rows:
        pd.DataFrame(rows).to_csv(reports / "profiles_summary.csv", index=False, encoding="utf-8-sig")


def _suggestions(df: pd.DataFrame, champions: dict[str, dict]) -> list[str]:
    suggestions: list[str] = []
    if df.empty:
        return ["- 暂无。"]
    if (df["trade_count"] < 3).mean() > 0.5:
        suggestions.append("- 大量参数交易次数不足，扩大历史样本或降低突破/摆动阈值后再比较。")
    if (df["overfit_flag"].astype(bool)).mean() > 0.25:
        suggestions.append("- 过拟合比例偏高，优先提高突破确认幅度、延长冷却时间，并按样本外收益过滤。")
    weak_symbols = [symbol for symbol, item in champions.items() if item.get("status") != "active"]
    if weak_symbols:
        suggestions.append(f"- {', '.join(weak_symbols)} 暂无稳定 champion，盘中只观察，不发开仓信号。")
    top = df.sort_values("net_pnl", ascending=False).head(20)
    if not top.empty and (top["max_drawdown"].abs() > top["net_pnl"].abs().clip(lower=1) * 1.5).any():
        suggestions.append("- 部分高收益策略回撤相对收益过大，实盘前应测试更紧止损或降低持仓最长时间。")
    if not suggestions:
        suggestions.append("- 当前 top 策略没有明显结构性问题，下一步重点扩大真实行情和新闻事件样本。")
    return suggestions


def _fmt(value) -> str:
    if value is None:
        return "-"
    try:
        if pd.isna(value):
            return "-"
        return f"{float(value):.2f}"
    except Exception:
        return str(value)


def _clean(row: dict) -> dict:
    out = {}
    for key, value in row.items():
        if isinstance(value, float) and value == float("inf"):
            out[key] = "inf"
        elif pd.isna(value) if not isinstance(value, (dict, list)) else False:
            out[key] = None
        else:
            out[key] = value
    return out
