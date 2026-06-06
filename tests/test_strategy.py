from __future__ import annotations

import unittest

import pandas as pd

from qihuo_signal.models import StrategyParams
from qihuo_signal.strategy import StrategyEngine, detect_pivots


def bars_from_closes(closes: list[float]) -> pd.DataFrame:
    rows = []
    for i, close in enumerate(closes):
        prev = closes[i - 1] if i else close
        high = max(prev, close) + 1
        low = min(prev, close) - 1
        rows.append(
            {
                "timestamp": pd.Timestamp("2024-01-01") + pd.Timedelta(minutes=15 * i),
                "open": prev,
                "high": high,
                "low": low,
                "close": close,
                "volume": 1000,
                "hold": 1000,
                "settle": close,
                "contract": "RB0",
                "source": "test",
            }
        )
    return pd.DataFrame(rows)


class StrategyTests(unittest.TestCase):
    def test_pivot_confirmation_is_delayed(self) -> None:
        bars = bars_from_closes([100, 104, 110, 105, 101, 106, 108, 103, 99, 102])
        pivots = detect_pivots(bars, window=1, min_swing_pct=0.01)
        self.assertTrue(pivots)
        for pivot in pivots:
            self.assertGreaterEqual(pivot.confirm_index, pivot.index + 1)

    def test_swing_strategy_can_open_long(self) -> None:
        bars = bars_from_closes([100, 96, 92, 98, 105, 101, 95, 99, 106, 112, 118, 116, 121])
        params = StrategyParams(
            pattern="swing_reversal",
            timeframe="15m",
            swing_window=1,
            min_swing_pct=0.01,
            breakout_pct=0.001,
            max_hold_bars=20,
        )
        actions = StrategyEngine().generate_actions(bars, params, symbol="RB")
        self.assertIn("OPEN_LONG", [action.action for action in actions])

    def test_swing_strategy_can_open_short(self) -> None:
        bars = bars_from_closes([100, 106, 112, 105, 98, 103, 108, 101, 94, 90, 86, 88, 82])
        params = StrategyParams(
            pattern="swing_reversal",
            timeframe="15m",
            swing_window=1,
            min_swing_pct=0.01,
            breakout_pct=0.001,
            max_hold_bars=20,
        )
        actions = StrategyEngine().generate_actions(bars, params, symbol="RB")
        self.assertIn("OPEN_SHORT", [action.action for action in actions])


if __name__ == "__main__":
    unittest.main()

