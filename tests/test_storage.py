from __future__ import annotations

import tempfile
import unittest

import pandas as pd

from qihuo_signal.config import load_settings
from qihuo_signal.data_sources import SyntheticProvider
from qihuo_signal.models import Signal
from qihuo_signal.storage import LocalStore


class StorageTests(unittest.TestCase):
    def test_bars_round_trip(self) -> None:
        settings = load_settings("missing-test-config.yaml")
        with tempfile.TemporaryDirectory() as tmp:
            store = LocalStore(tmp)
            bars = SyntheticProvider(bars=30).fetch_bars(settings.instruments["RB"], "15m")
            store.write_bars("RB", "15m", bars, append=False)
            loaded = store.read_bars("RB", "15m")
            self.assertEqual(len(loaded), len(bars))
            self.assertEqual(loaded.iloc[0]["symbol"], "RB")

    def test_daily_bars_merge_term_structure(self) -> None:
        settings = load_settings("missing-test-config.yaml")
        with tempfile.TemporaryDirectory() as tmp:
            store = LocalStore(tmp)
            bars = SyntheticProvider(bars=120).fetch_bars(settings.instruments["RB"], "1d")
            store.write_bars("RB", "1d", bars, append=False)
            term = pd.DataFrame(
                {
                    "timestamp": pd.to_datetime(bars["timestamp"].head(3)),
                    "front_contract": ["RB2401", "RB2401", "RB2401"],
                    "second_contract": ["RB2405", "RB2405", "RB2405"],
                    "front_price": [100.0, 101.0, 102.0],
                    "second_price": [99.0, 100.0, 101.0],
                    "term_spread": [-0.01, -0.0099, -0.0098],
                    "annualized_carry": [-0.03, -0.03, -0.03],
                    "carry_signal": [0.03, 0.03, 0.03],
                    "term_liquidity": [1000, 1100, 1200],
                }
            )
            store.write_term_structure("RB", term, append=False)
            loaded = store.read_bars("RB", "1d")
            self.assertIn("carry_signal", loaded.columns)
            self.assertEqual(float(loaded.iloc[0]["carry_signal"]), 0.03)

    def test_append_signals_updates_duckdb_table(self) -> None:
        try:
            import duckdb
        except Exception:
            self.skipTest("duckdb not installed")
        with tempfile.TemporaryDirectory() as tmp:
            store = LocalStore(tmp)
            signal = Signal(
                symbol="RB",
                contract="RB0",
                timestamp=pd.Timestamp("2026-01-01 10:00").to_pydatetime(),
                action="OPEN_LONG",
                price=3300,
                confidence=0.6,
                trigger_price=3300,
                invalid_price=3250,
                reason="test",
                news_evidence="none",
                risk_check="ok",
                strategy_rank=1,
                strategy_id="test-strategy",
            )
            store.append_signals([signal])
            with duckdb.connect(str(store.duckdb_path)) as con:
                count = con.execute("SELECT count(*) FROM signals").fetchone()[0]
            self.assertEqual(count, 1)


if __name__ == "__main__":
    unittest.main()
