from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

import pandas as pd

from .models import BacktestResult, NewsEvent, Signal


class LocalStore:
    """Parquet-first storage with optional DuckDB mirrors for fast local queries."""

    def __init__(self, root: str | Path = "data") -> None:
        self.root = Path(root)
        self.parquet_root = self.root / "parquet"
        self.bars_root = self.parquet_root / "bars"
        self.events_root = self.parquet_root / "events"
        self.signals_root = self.parquet_root / "signals"
        self.backtest_root = self.root / "backtests"
        self.duckdb_path = self.root / "qihuo.duckdb"

    def initialize(self) -> None:
        for path in [
            self.bars_root,
            self.events_root,
            self.signals_root,
            self.backtest_root,
        ]:
            path.mkdir(parents=True, exist_ok=True)
        if not self.duckdb_path.exists():
            self.rebuild_duckdb()

    def bars_path(self, symbol: str, timeframe: str) -> Path:
        return self.bars_root / f"{symbol}_{timeframe}.parquet"

    def write_bars(self, symbol: str, timeframe: str, bars: pd.DataFrame, append: bool = True) -> Path:
        self.initialize()
        df = normalize_bars(bars)
        df["symbol"] = symbol
        df["timeframe"] = timeframe
        path = self.bars_path(symbol, timeframe)
        if append and path.exists() and path.stat().st_size > 0:
            try:
                old = pd.read_parquet(path)
                df = pd.concat([old, df], ignore_index=True)
            except Exception:
                pass
        subset = ["symbol", "timeframe", "timestamp"]
        if "contract" in df.columns:
            subset.append("contract")
        df = df.drop_duplicates(subset=subset, keep="last").sort_values("timestamp").reset_index(drop=True)
        df.to_parquet(path, index=False)
        self._sync_bars_duckdb(symbol, timeframe, df)
        return path

    def read_bars(self, symbol: str, timeframe: str) -> pd.DataFrame:
        path = self.bars_path(symbol, timeframe)
        if not path.exists():
            return pd.DataFrame()
        return pd.read_parquet(path).sort_values("timestamp").reset_index(drop=True)

    def available_bars(self) -> list[tuple[str, str]]:
        if not self.bars_root.exists():
            return []
        out: list[tuple[str, str]] = []
        for path in self.bars_root.glob("*.parquet"):
            stem = path.stem
            if "_" not in stem:
                continue
            symbol, timeframe = stem.rsplit("_", 1)
            out.append((symbol, timeframe))
        return sorted(out)

    def write_events(self, events: Iterable[NewsEvent], append: bool = True) -> Path:
        self.initialize()
        rows = [event.to_dict() for event in events]
        path = self.events_root / "events.parquet"
        if not rows:
            return path
        df = pd.DataFrame(rows)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        if "raw" in df.columns:
            df["raw_json"] = df["raw"].apply(lambda value: json.dumps(value or {}, ensure_ascii=False, sort_keys=True))
            df = df.drop(columns=["raw"])
        if append and path.exists() and path.stat().st_size > 0:
            try:
                old = pd.read_parquet(path)
                df = pd.concat([old, df], ignore_index=True)
            except Exception:
                pass
        df = df.drop_duplicates(subset=["symbol", "timestamp", "title"], keep="last")
        df = df.sort_values(["symbol", "timestamp"]).reset_index(drop=True)
        df.to_parquet(path, index=False)
        self._replace_table("events", df)
        return path

    def read_events(self, symbol: str | None = None) -> pd.DataFrame:
        path = self.events_root / "events.parquet"
        if not path.exists() or path.stat().st_size == 0:
            return pd.DataFrame()
        try:
            df = pd.read_parquet(path)
        except Exception:
            return pd.DataFrame()
        if symbol is not None and not df.empty:
            df = df[df["symbol"] == symbol]
        if df.empty or "timestamp" not in df.columns:
            return df.reset_index(drop=True)
        return df.sort_values("timestamp").reset_index(drop=True)

    def write_backtest_results(self, results: Iterable[BacktestResult]) -> Path:
        self.initialize()
        rows = [result.to_dict() for result in results]
        path = self.backtest_root / "results.parquet"
        df = pd.DataFrame(rows)
        if not df.empty:
            df["params_json"] = df["params"].apply(json.dumps, ensure_ascii=False, sort_keys=True)
            df = df.drop(columns=["params"])
            df = df.drop_duplicates(subset=["symbol", "timeframe", "strategy_id"], keep="last")
            df = df.sort_values("net_pnl", ascending=False).reset_index(drop=True)
        df.to_parquet(path, index=False)
        self._replace_table("backtest_results", df)
        return path

    def read_backtest_results(self) -> pd.DataFrame:
        path = self.backtest_root / "results.parquet"
        if not path.exists():
            return pd.DataFrame()
        return pd.read_parquet(path)

    def write_champions(self, champions: dict[str, dict]) -> Path:
        self.initialize()
        path = self.backtest_root / "champions.json"
        path.write_text(json.dumps(champions, ensure_ascii=False, indent=2), encoding="utf-8")
        return path

    def read_champions(self) -> dict[str, dict]:
        path = self.backtest_root / "champions.json"
        if not path.exists():
            return {}
        return json.loads(path.read_text(encoding="utf-8"))

    def write_profiles(self, profiles: dict[str, dict[str, dict]]) -> Path:
        self.initialize()
        path = self.backtest_root / "profiles.json"
        path.write_text(json.dumps(profiles, ensure_ascii=False, indent=2), encoding="utf-8")
        return path

    def read_profiles(self) -> dict[str, dict[str, dict]]:
        path = self.backtest_root / "profiles.json"
        if not path.exists():
            return {}
        return json.loads(path.read_text(encoding="utf-8"))

    def append_signals(self, signals: Iterable[Signal]) -> Path:
        self.initialize()
        rows = [signal.to_dict() for signal in signals]
        path = self.signals_root / "signals.parquet"
        if not rows:
            return path
        df = pd.DataFrame(rows)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        if path.exists():
            df = pd.concat([pd.read_parquet(path), df], ignore_index=True)
        df = df.drop_duplicates(subset=["symbol", "contract", "timestamp", "action", "strategy_id"], keep="last")
        df = df.sort_values("timestamp").reset_index(drop=True)
        df.to_parquet(path, index=False)
        self._replace_table("signals", df)
        return path

    def read_signals(self) -> pd.DataFrame:
        path = self.signals_root / "signals.parquet"
        if not path.exists():
            return pd.DataFrame()
        return pd.read_parquet(path).sort_values("timestamp").reset_index(drop=True)

    def rebuild_duckdb(self) -> None:
        try:
            import duckdb
        except Exception:
            return
        self.root.mkdir(parents=True, exist_ok=True)
        try:
            with duckdb.connect(str(self.duckdb_path)) as con:
                con.execute("SELECT 1")
                self._rebuild_table_from_paths(con, "bars", self.bars_root.glob("*.parquet") if self.bars_root.exists() else [])
                self._rebuild_table_from_paths(con, "events", self.events_root.glob("*.parquet") if self.events_root.exists() else [])
                self._rebuild_table_from_paths(con, "signals", self.signals_root.glob("*.parquet") if self.signals_root.exists() else [])
                result_path = self.backtest_root / "results.parquet"
                self._rebuild_table_from_paths(con, "backtest_results", [result_path] if result_path.exists() else [])
        except Exception:
            return

    def _rebuild_table_from_paths(self, con, table: str, paths: Iterable[Path]) -> None:
        frames = []
        for path in paths:
            if path.exists() and path.stat().st_size > 0:
                try:
                    frame = pd.read_parquet(path)
                    if not frame.empty and len(frame.columns) > 0:
                        frames.append(frame)
                except Exception:
                    continue
        if not frames:
            return
        df = pd.concat(frames, ignore_index=True)
        con.register("rebuild_df", df)
        con.execute(f"CREATE OR REPLACE TABLE {table} AS SELECT * FROM rebuild_df")

    def _sync_bars_duckdb(self, symbol: str, timeframe: str, df: pd.DataFrame) -> None:
        try:
            import duckdb
        except Exception:
            return
        try:
            with duckdb.connect(str(self.duckdb_path)) as con:
                con.execute(
                    """
                    CREATE TABLE IF NOT EXISTS bars (
                        timestamp TIMESTAMP, open DOUBLE, high DOUBLE, low DOUBLE, close DOUBLE,
                        volume DOUBLE, hold DOUBLE, settle DOUBLE, contract VARCHAR,
                        source VARCHAR, symbol VARCHAR, timeframe VARCHAR
                    )
                    """
                )
                con.execute("DELETE FROM bars WHERE symbol = ? AND timeframe = ?", [symbol, timeframe])
                con.register("bars_df", df)
                con.execute("INSERT INTO bars SELECT * FROM bars_df")
        except Exception:
            return

    def _replace_table(self, table: str, df: pd.DataFrame) -> None:
        try:
            import duckdb
        except Exception:
            return
        try:
            with duckdb.connect(str(self.duckdb_path)) as con:
                con.register("replace_df", df)
                con.execute(f"CREATE OR REPLACE TABLE {table} AS SELECT * FROM replace_df")
        except Exception:
            return


def normalize_bars(bars: pd.DataFrame) -> pd.DataFrame:
    if bars.empty:
        return pd.DataFrame(
            columns=["timestamp", "open", "high", "low", "close", "volume", "hold", "settle", "contract", "source"]
        )
    rename = {
        "date": "timestamp",
        "datetime": "timestamp",
        "日期": "timestamp",
        "时间": "timestamp",
        "开盘": "open",
        "最高": "high",
        "最低": "low",
        "收盘": "close",
        "成交量": "volume",
        "持仓量": "hold",
        "结算价": "settle",
        "合约": "contract",
        "合约代码": "contract",
    }
    df = bars.rename(columns={k: v for k, v in rename.items() if k in bars.columns}).copy()
    required = ["timestamp", "open", "high", "low", "close"]
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"bars missing required columns: {missing}")
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    for col in ["open", "high", "low", "close", "volume", "hold", "settle"]:
        if col not in df.columns:
            df[col] = 0.0
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)
    if "contract" not in df.columns:
        df["contract"] = ""
    if "source" not in df.columns:
        df["source"] = "unknown"
    return df[["timestamp", "open", "high", "low", "close", "volume", "hold", "settle", "contract", "source"]]
