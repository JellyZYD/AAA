from __future__ import annotations

import argparse
import sys

import pandas as pd
import uvicorn

from .alerts import build_alert_sender, format_news_digest, format_news_events
from .analysis import analyze_results
from .backtest import parallel_search_strategies, search_strategies
from .config import load_settings, write_default_config
from .data_sources import AkShareProvider, MissingDependencyError, SyntheticProvider
from .events import LLMEventAnalyzer, classify_headline_frame, fetch_major_headlines, fetch_shmet_headlines, load_manual_events
from .polling import SignalPoller
from .refine import refine_strategies
from .storage import LocalStore
from .walkforward import run_walk_forward


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="qihuo", description="Local futures strategy lab and signal notifier.")
    parser.add_argument("--config", default=None, help="Path to config.yaml")
    sub = parser.add_subparsers(dest="command", required=True)

    init_p = sub.add_parser("init", help="Create config and local data directories")
    init_p.add_argument("--overwrite", action="store_true")

    sub.add_parser("env-check", help="Check .env/config readiness without printing secrets")

    alert_test_p = sub.add_parser("alert-test", help="Send one test message through configured alert provider")
    alert_test_p.add_argument("--dry-run", action="store_true")

    fetch_p = sub.add_parser("fetch-history", help="Fetch full history into local Parquet/DuckDB")
    fetch_p.add_argument("--sample", action="store_true", help="Generate deterministic sample bars instead of AkShare")
    fetch_p.add_argument("--timeframe", action="append", help="Limit to one or more timeframes")

    update_p = sub.add_parser("update", help="Incrementally update recent bars")
    update_p.add_argument("--sample", action="store_true", help="Use synthetic provider")
    update_p.add_argument("--timeframe", action="append", help="Limit to one or more timeframes")

    bt_p = sub.add_parser("backtest", help="Run strategy search on local cached data")
    bt_p.add_argument("--search", action="store_true", help="Run parameter search")
    bt_p.add_argument("--fast", action="store_true", help="Use a smaller grid for quick iteration")
    bt_p.add_argument("--limit-per-symbol", type=int, default=None, help="Max params per symbol per timeframe")
    bt_p.add_argument("--timeframe", action="append", help="Limit search to one or more timeframes")
    bt_p.add_argument("--workers", type=int, default=6, help="Parallel worker processes")
    bt_p.add_argument("--side", action="append", choices=["both", "long", "short"], help="Limit strategy side")
    bt_p.add_argument(
        "--pattern",
        action="append",
        choices=[
            "swing_reversal",
            "breakout",
            "failed_breakout",
            "trend_failure",
            "donchian_atr",
            "tsmom_vol",
            "vol_breakout",
            "carry_tsmom",
        ],
        help="Limit search to one or more strategy patterns",
    )
    bt_p.add_argument("--append", action="store_true", help="Merge new results with existing results")
    bt_p.add_argument("--symbol", action="append", help="Limit search to one or more symbols")

    sub.add_parser("analyze", help="Generate report and champion strategies")

    refine_p = sub.add_parser("refine", help="Run local parameter perturbation and rolling validation")
    refine_p.add_argument(
        "--pattern",
        action="append",
        choices=["donchian_atr", "tsmom_vol", "vol_breakout", "carry_tsmom"],
        help="Pattern to refine",
    )
    refine_p.add_argument("--max-per-symbol", type=int, default=40)
    refine_p.add_argument("--rolling-windows", type=int, default=4)
    refine_p.add_argument("--top-seeds-per-symbol", type=int, default=3)

    wf_p = sub.add_parser("walk-forward", help="Run causal walk-forward validation from a static parameter grid")
    wf_p.add_argument("--folds", type=int, default=5)
    wf_p.add_argument("--max-per-symbol", type=int, default=24)
    wf_p.add_argument("--workers", type=int, default=6)

    term_p = sub.add_parser("fetch-term-structure", help="Fetch single-contract daily data and build local carry factors")
    term_p.add_argument("--symbol", action="append", help="Limit to one or more symbols")
    term_p.add_argument("--start-year", type=int, default=2023)
    term_p.add_argument("--end-year", type=int, default=None)

    poll_p = sub.add_parser("poll", help="Poll latest bars and send signals")
    poll_p.add_argument("--once", action="store_true")
    poll_p.add_argument("--dry-run", action="store_true")
    poll_p.add_argument("--sample", action="store_true", help="Use synthetic provider for update")
    poll_p.add_argument("--no-update", action="store_true", help="Do not update bars before signal generation")
    poll_p.add_argument("--include-watch", action="store_true", help="Also emit WATCH_ONLY status messages")
    poll_p.add_argument(
        "--profile",
        choices=[
            "live",
            "safe_winrate",
            "refined_robust",
            "robust",
            "walk_forward",
            "walkforward",
            "max_return",
            "max_winrate",
            "balanced",
            "capital_safe",
        ],
        default="live",
        help="Strategy profile to use for polling; live maps to walk_forward when available, robust maps to refined_robust",
    )

    dash_p = sub.add_parser("dashboard", help="Run local FastAPI dashboard")
    dash_p.add_argument("--host", default="127.0.0.1")
    dash_p.add_argument("--port", type=int, default=8000)

    news_p = sub.add_parser("import-events", help="Import manual news/event CSV")
    news_p.add_argument("path")

    classify_p = sub.add_parser("classify-news", help="Classify headline CSV with configured LLM and store events")
    classify_p.add_argument("path")
    classify_p.add_argument("--symbol", help="Symbol to use when CSV has no symbol column")
    classify_p.add_argument("--title-column", default="title")
    classify_p.add_argument("--timestamp-column", default="timestamp")

    fetch_news_p = sub.add_parser("fetch-news", help="Fetch public futures news and classify into local events")
    fetch_news_p.add_argument("--source", choices=["shmet"], default="shmet")
    fetch_news_p.add_argument("--symbol", default="全部", help="Provider-specific news category")
    fetch_news_p.add_argument("--push", action="store_true", help="Push classified news impact through alert provider")
    fetch_news_p.add_argument("--dry-run", action="store_true", help="Print alert instead of calling the webhook API")
    fetch_news_p.add_argument("--include-empty", action="store_true", help="Push a no-impact message when no events are classified")
    fetch_news_p.add_argument("--major-limit", type=int, default=5)

    news_poll_p = sub.add_parser("news-poll", help="Fetch real-time news, classify impacts, and push alert")
    news_poll_p.add_argument("--source", choices=["shmet"], default="shmet")
    news_poll_p.add_argument("--symbol", default="全部", help="Provider-specific news category")
    news_poll_p.add_argument("--dry-run", action="store_true", help="Print alert instead of calling the webhook API")
    news_poll_p.add_argument("--include-empty", action="store_true", default=True)
    news_poll_p.add_argument("--major-limit", type=int, default=5)

    args = parser.parse_args(argv)
    settings = load_settings(args.config)
    store = LocalStore(settings.data_root)

    if args.command == "init":
        config_path = write_default_config(args.config or "config.yaml", overwrite=args.overwrite)
        store.initialize()
        print(f"initialized {config_path} and {settings.data_root}")
        return 0

    if args.command == "env-check":
        checks = {
            "llm_base_url": bool(settings.llm.base_url),
            "llm_api_key": bool(settings.llm.api_key),
            "llm_model": bool(settings.llm.model),
            "qq_app_id": bool(settings.alert.qq_app_id),
            "qq_app_secret": bool(settings.alert.qq_app_secret),
            "qq_target_id": bool(settings.alert.qq_target_id),
            "wecom_webhook_url": bool(settings.alert.wecom_webhook_url),
            "qq_target_type": settings.alert.qq_target_type,
            "alert_provider": settings.alert.provider,
            "alert_dry_run": settings.alert.dry_run,
            "symbols": ",".join(settings.symbols),
            "data_root": settings.data_root,
        }
        for key, value in checks.items():
            print(f"{key}: {value}")
        if not settings.alert.qq_target_id:
            print("note: QQ_BOT_TARGET_ID is missing; this is fine when ALERT_PROVIDER=wecom.")
        return 0

    if args.command == "alert-test":
        sender = build_alert_sender(settings.alert, dry_run=True if args.dry_run else None)
        sender.send("期货信号系统测试：企业微信推送通道已连接。")
        print("alert test sent")
        return 0

    if args.command == "fetch-history":
        provider = SyntheticProvider() if args.sample else _akshare_provider()
        store.initialize()
        provider.fetch_all(settings, store, timeframes=tuple(args.timeframe) if args.timeframe else None)
        print(f"cached bars: {store.available_bars()}")
        return 0

    if args.command == "update":
        provider = SyntheticProvider() if args.sample else _akshare_provider()
        provider.update_recent(settings, store, timeframes=tuple(args.timeframe) if args.timeframe else None)
        print("updated recent bars")
        return 0

    if args.command == "backtest":
        if not args.search:
            print("Nothing to do. Use: qihuo backtest --search")
            return 2
        if args.timeframe:
            settings = settings.__class__(**{**settings.__dict__, "timeframes": tuple(args.timeframe)})
        if args.symbol:
            selected = tuple(args.symbol)
            settings = settings.__class__(
                **{
                    **settings.__dict__,
                    "symbols": selected,
                    "instruments": {symbol: settings.instruments[symbol] for symbol in selected},
                }
            )
        sides = tuple(args.side) if args.side else ("both",)
        patterns = tuple(args.pattern) if args.pattern else None
        if args.workers and args.workers > 1:
            results = parallel_search_strategies(
                store,
                settings,
                fast=args.fast,
                limit_per_symbol=args.limit_per_symbol,
                workers=args.workers,
                sides=sides,
                patterns=patterns,
                append=args.append,
            )
        else:
            results = search_strategies(
                store,
                settings,
                fast=args.fast,
                limit_per_symbol=args.limit_per_symbol,
                sides=sides,
                patterns=patterns,
                append=args.append,
            )
        print(f"backtest results: {len(results)}")
        if results:
            best = results[0]
            print(f"best: {best.symbol} {best.timeframe} net_pnl={best.net_pnl:.2f} strategy={best.strategy_id}")
        return 0

    if args.command == "analyze":
        report_path, champions = analyze_results(store, settings, settings.reports_root)
        print(f"report: {report_path}")
        active = [symbol for symbol, item in champions.items() if item.get("status") == "active"]
        print(f"active champions: {active}")
        return 0

    if args.command == "refine":
        patterns = tuple(args.pattern) if args.pattern else ("donchian_atr", "tsmom_vol")
        report_path, evaluations = refine_strategies(
            store,
            settings,
            settings.reports_root,
            patterns=patterns,
            max_per_symbol=args.max_per_symbol,
            rolling_windows=args.rolling_windows,
            top_seeds_per_symbol=args.top_seeds_per_symbol,
        )
        print(f"refinement report: {report_path}")
        print(f"refined candidates: {len(evaluations)}")
        return 0

    if args.command == "fetch-term-structure":
        from .term_structure import fetch_and_store_term_structure

        provider = _akshare_provider()
        stats = fetch_and_store_term_structure(
            provider,
            settings,
            store,
            symbols=tuple(args.symbol) if args.symbol else None,
            start_year=args.start_year,
            end_year=args.end_year,
        )
        for item in stats:
            print(
                f"{item.symbol}: rows={item.rows}, contracts={item.contracts_loaded}/{item.contracts_tried}, "
                f"range={item.start}..{item.end}"
            )
        return 0

    if args.command == "walk-forward":
        report_path, summaries = run_walk_forward(
            store,
            settings,
            settings.reports_root,
            folds=args.folds,
            max_per_symbol=args.max_per_symbol,
            workers=args.workers,
        )
        print(f"walk-forward report: {report_path}")
        print(f"walk-forward symbols: {len(summaries)}")
        return 0

    if args.command == "poll":
        provider = None if args.no_update else (SyntheticProvider() if args.sample else _akshare_provider())
        sender = build_alert_sender(settings.alert, dry_run=True if args.dry_run else None)
        poller = SignalPoller(settings, store, provider=provider, alert_sender=sender, profile=args.profile)
        if args.once:
            signals = poller.poll_once(include_watch=args.include_watch, update_data=not args.no_update)
            print(f"signals: {len(signals)}")
            return 0
        poller.run_forever()
        return 0

    if args.command == "dashboard":
        print(f"dashboard: http://{args.host}:{args.port}")
        uvicorn.run("qihuo_signal.dashboard:app", host=args.host, port=args.port, reload=False)
        return 0

    if args.command == "import-events":
        events = load_manual_events(args.path)
        store.write_events(events, append=True)
        analyzer = LLMEventAnalyzer(settings.llm)
        print(f"imported events: {len(events)}; llm provider: {analyzer.settings.provider}")
        return 0

    if args.command == "classify-news":
        df = pd.read_csv(args.path)
        if args.title_column not in df.columns:
            raise SystemExit(f"title column not found: {args.title_column}")
        if "symbol" not in df.columns and not args.symbol:
            raise SystemExit("CSV must contain a symbol column or pass --symbol")
        analyzer = LLMEventAnalyzer(settings.llm)
        events = []
        for _, row in df.iterrows():
            symbol = str(row["symbol"] if "symbol" in df.columns else args.symbol)
            classified = analyzer.analyze(symbol, [str(row[args.title_column])])
            if args.timestamp_column in df.columns:
                for event in classified:
                    events.append(
                        event.__class__(
                            **{
                                **event.__dict__,
                                "timestamp": pd.to_datetime(row[args.timestamp_column]).to_pydatetime(),
                            }
                        )
                    )
            else:
                events.extend(classified)
        store.write_events(events, append=True)
        print(f"classified events: {len(events)}")
        return 0

    if args.command == "fetch-news":
        if args.source != "shmet":
            raise SystemExit(f"unsupported source: {args.source}")
        headlines = fetch_shmet_headlines(args.symbol)
        major = fetch_major_headlines(args.major_limit)
        combined = pd.concat([headlines, major], ignore_index=True).drop_duplicates(subset=["title"])
        analyzer = LLMEventAnalyzer(settings.llm)
        events = classify_headline_frame(combined, settings.symbols, analyzer)
        store.write_events(events, append=True)
        if args.push and (events or args.include_empty):
            sender = build_alert_sender(settings.alert, dry_run=True if args.dry_run else None)
            sender.send(format_news_digest(events, major))
        print(f"fetched headlines: {len(combined)}; classified events: {len(events)}")
        return 0

    if args.command == "news-poll":
        if args.source != "shmet":
            raise SystemExit(f"unsupported source: {args.source}")
        headlines = fetch_shmet_headlines(args.symbol)
        major = fetch_major_headlines(args.major_limit)
        combined = pd.concat([headlines, major], ignore_index=True).drop_duplicates(subset=["title"])
        analyzer = LLMEventAnalyzer(settings.llm)
        events = classify_headline_frame(combined, settings.symbols, analyzer)
        store.write_events(events, append=True)
        if events or args.include_empty:
            sender = build_alert_sender(settings.alert, dry_run=True if args.dry_run else None)
            sender.send(format_news_digest(events, major, title="期货实时新闻影响"))
        print(f"fetched headlines: {len(combined)}; classified events: {len(events)}")
        return 0

    return 1


def _akshare_provider() -> AkShareProvider:
    try:
        return AkShareProvider()
    except MissingDependencyError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(2) from exc
