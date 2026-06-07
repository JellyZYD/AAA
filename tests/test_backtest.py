from __future__ import annotations

import tempfile
import unittest

import pandas as pd

from qihuo_signal.backtest import Backtester, search_strategies, select_champions
from qihuo_signal.config import load_settings
from qihuo_signal.data_sources import SyntheticProvider
from qihuo_signal.models import StrategyParams
from qihuo_signal.storage import LocalStore


class BacktestTests(unittest.TestCase):
    def test_backtest_runs_on_synthetic_data(self) -> None:
        settings = load_settings("missing-test-config.yaml")
        provider = SyntheticProvider(bars=180)
        bars = provider.fetch_bars(settings.instruments["RB"], "15m")
        params = StrategyParams(pattern="breakout", timeframe="15m", range_lookback=12, max_hold_bars=24)
        run = Backtester(settings).run("RB", settings.instruments["RB"], bars, params)
        self.assertEqual(run.result.symbol, "RB")
        self.assertGreaterEqual(run.result.trade_count, 0)

    def test_backtest_fills_signal_on_next_bar_open(self) -> None:
        settings = load_settings("missing-test-config.yaml")
        bars = pd.DataFrame(
            {
                "timestamp": pd.date_range("2026-01-01 09:00:00", periods=6, freq="15min"),
                "open": [100, 100, 100, 110, 111, 112],
                "high": [101, 101, 104, 105, 106, 107],
                "low": [99, 99, 99, 103, 104, 105],
                "close": [100, 100, 103, 104, 105, 106],
                "volume": [1000] * 6,
                "hold": [1000] * 6,
                "settle": [100, 100, 103, 104, 105, 106],
                "contract": ["RB0"] * 6,
                "source": ["test"] * 6,
            }
        )
        params = StrategyParams(
            pattern="breakout",
            side="long",
            timeframe="15m",
            range_lookback=2,
            breakout_pct=0.0,
            max_hold_bars=1,
            risk_mode="signal",
        )

        run = Backtester(settings).run("RB", settings.instruments["RB"], bars, params)

        self.assertTrue(run.trades)
        trade = run.trades[0]
        self.assertEqual(trade.entry_time, bars.iloc[3]["timestamp"].to_pydatetime())
        self.assertEqual(trade.entry_price, 110)
        self.assertEqual(trade.exit_time, bars.iloc[4]["timestamp"].to_pydatetime())
        self.assertEqual(trade.exit_price, 111)

    def test_search_and_champion_selection(self) -> None:
        settings = load_settings("missing-test-config.yaml")
        with tempfile.TemporaryDirectory() as tmp:
            store = LocalStore(tmp)
            provider = SyntheticProvider(bars=160)
            provider.fetch_all(settings, store, timeframes=("15m",))
            settings = settings.__class__(**{**settings.__dict__, "timeframes": ("15m",), "symbols": ("RB",)})
            results = search_strategies(store, settings, fast=True, limit_per_symbol=5)
            champions = select_champions(results, settings)
            self.assertTrue(results)
            self.assertIn("RB", champions)


if __name__ == "__main__":
    unittest.main()
