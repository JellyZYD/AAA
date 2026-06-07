from __future__ import annotations

import json
import unittest
from pathlib import Path

import pandas as pd

from qihuo_signal.backtest import Backtester
from qihuo_signal.config import load_settings
from qihuo_signal.models import StrategyParams
from qihuo_signal.refine import _perturb
from qihuo_signal.storage import LocalStore
from qihuo_signal.strategy import StrategyEngine, detect_pivots
from qihuo_signal.walkforward import WalkForwardRow, _load_candidates, _summarize_symbol, _train_score


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

    def test_donchian_atr_can_open_long(self) -> None:
        bars = bars_from_closes([100, 101, 100, 102, 101, 100, 111, 114, 116, 115])
        params = StrategyParams(
            pattern="donchian_atr",
            side="long",
            timeframe="15m",
            range_lookback=5,
            breakout_pct=0.0,
            atr_period=3,
            atr_mult=2.0,
            exit_lookback=3,
            max_hold_bars=20,
            risk_mode="signal",
        )
        actions = StrategyEngine().generate_actions(bars, params, symbol="RB")
        self.assertIn("OPEN_LONG", [action.action for action in actions])

    def test_tsmom_vol_can_open_short(self) -> None:
        bars = bars_from_closes([120, 119, 118, 116, 114, 112, 110, 107, 104, 101, 99, 96])
        params = StrategyParams(
            pattern="tsmom_vol",
            side="short",
            timeframe="15m",
            momentum_lookback=4,
            vol_lookback=4,
            score_threshold=0.1,
            atr_period=3,
            atr_mult=2.0,
            max_hold_bars=20,
            risk_mode="signal",
        )
        actions = StrategyEngine().generate_actions(bars, params, symbol="RB")
        self.assertIn("OPEN_SHORT", [action.action for action in actions])

    def test_quality_tsmom_can_open_short_when_trend_path_is_clean(self) -> None:
        bars = bars_from_closes([120, 119, 118, 116, 114, 112, 110, 107, 104, 101, 99, 96])
        params = StrategyParams(
            pattern="quality_tsmom",
            side="short",
            timeframe="15m",
            momentum_lookback=4,
            vol_lookback=4,
            score_threshold=0.1,
            trend_quality_threshold=0.5,
            atr_period=3,
            atr_mult=2.0,
            max_hold_bars=20,
            risk_mode="signal",
        )
        actions = StrategyEngine().generate_actions(bars, params, symbol="RB")
        self.assertIn("OPEN_SHORT", [action.action for action in actions])

    def test_vol_breakout_can_open_long_after_compression(self) -> None:
        bars = bars_from_closes([100, 101, 100, 101, 100, 100, 100, 100, 100, 100, 105, 106])
        params = StrategyParams(
            pattern="vol_breakout",
            side="long",
            timeframe="15m",
            range_lookback=5,
            breakout_pct=0.0,
            atr_period=3,
            atr_mult=2.0,
            exit_lookback=3,
            vol_lookback=3,
            score_threshold=1.2,
            max_hold_bars=20,
            risk_mode="signal",
        )
        actions = StrategyEngine().generate_actions(bars, params, symbol="RB")
        self.assertIn("OPEN_LONG", [action.action for action in actions])

    def test_confirmed_breakout_uses_volume_and_momentum_confirmation(self) -> None:
        bars = bars_from_closes([100, 101, 100, 101, 100, 100, 100, 100, 100, 101, 105, 107, 109])
        bars.loc[:, "volume"] = [1000] * 10 + [1800, 1600, 1500]
        params = StrategyParams(
            pattern="confirmed_breakout",
            side="long",
            timeframe="15m",
            range_lookback=5,
            breakout_pct=0.0,
            atr_period=3,
            atr_mult=2.0,
            exit_lookback=3,
            momentum_lookback=3,
            vol_lookback=3,
            score_threshold=1.5,
            volume_threshold=1.1,
            max_hold_bars=20,
            risk_mode="signal",
        )
        actions = StrategyEngine().generate_actions(bars, params, symbol="RB")
        self.assertIn("OPEN_LONG", [action.action for action in actions])

    def test_carry_tsmom_uses_lagged_carry_to_open_long(self) -> None:
        bars = bars_from_closes([100, 100, 101, 101, 102, 104, 106, 108, 110, 112, 114, 116])
        bars["carry_signal"] = 0.05
        params = StrategyParams(
            pattern="carry_tsmom",
            side="long",
            timeframe="1d",
            momentum_lookback=3,
            vol_lookback=3,
            score_threshold=0.1,
            atr_period=3,
            atr_mult=2.0,
            max_hold_bars=20,
            risk_mode="signal",
        )
        actions = StrategyEngine().generate_actions(bars, params, symbol="RB")
        self.assertIn("OPEN_LONG", [action.action for action in actions])

    def test_ensemble_trend_requires_confirmed_long_breakout(self) -> None:
        bars = bars_from_closes([100, 100, 101, 101, 102, 103, 106, 110, 114, 119, 123, 128, 133])
        params = StrategyParams(
            pattern="ensemble_trend",
            side="long",
            timeframe="15m",
            range_lookback=5,
            breakout_pct=0.0,
            momentum_lookback=3,
            vol_lookback=3,
            score_threshold=0.05,
            trend_quality_threshold=0.2,
            atr_period=3,
            atr_mult=2.0,
            exit_lookback=3,
            max_hold_bars=20,
            risk_mode="signal",
        )

        actions = StrategyEngine().generate_actions(bars, params, symbol="RB")

        self.assertIn("OPEN_LONG", [action.action for action in actions])

    def test_ensemble_trend_requires_confirmed_short_breakout(self) -> None:
        bars = bars_from_closes([130, 130, 129, 128, 126, 123, 119, 114, 109, 104, 99, 94, 90])
        params = StrategyParams(
            pattern="ensemble_trend",
            side="short",
            timeframe="15m",
            range_lookback=5,
            breakout_pct=0.0,
            momentum_lookback=3,
            vol_lookback=3,
            score_threshold=0.05,
            trend_quality_threshold=0.2,
            atr_period=3,
            atr_mult=2.0,
            exit_lookback=3,
            max_hold_bars=20,
            risk_mode="signal",
        )

        actions = StrategyEngine().generate_actions(bars, params, symbol="RB")

        self.assertIn("OPEN_SHORT", [action.action for action in actions])

    def test_trend_pullback_can_open_long_after_pullback_breakout(self) -> None:
        bars = bars_from_closes([100, 102, 104, 106, 108, 110, 107, 105, 109, 112, 116, 119])
        params = StrategyParams(
            pattern="trend_pullback",
            side="long",
            timeframe="15m",
            range_lookback=6,
            breakout_pct=0.0,
            momentum_lookback=3,
            vol_lookback=3,
            score_threshold=0.02,
            trend_quality_threshold=0.2,
            atr_period=3,
            atr_mult=2.0,
            exit_lookback=3,
            max_hold_bars=20,
            risk_mode="signal",
        )

        actions = StrategyEngine().generate_actions(bars, params, symbol="RB")

        self.assertIn("OPEN_LONG", [action.action for action in actions])

    def test_trend_pullback_can_open_short_after_pullback_breakdown(self) -> None:
        bars = bars_from_closes([120, 118, 116, 114, 111, 108, 111, 113, 109, 105, 101, 98])
        params = StrategyParams(
            pattern="trend_pullback",
            side="short",
            timeframe="15m",
            range_lookback=6,
            breakout_pct=0.0,
            momentum_lookback=3,
            vol_lookback=3,
            score_threshold=0.02,
            trend_quality_threshold=0.2,
            atr_period=3,
            atr_mult=2.0,
            exit_lookback=3,
            max_hold_bars=20,
            risk_mode="signal",
        )

        actions = StrategyEngine().generate_actions(bars, params, symbol="RB")

        self.assertIn("OPEN_SHORT", [action.action for action in actions])

    def test_refine_perturbations_include_seed(self) -> None:
        params = StrategyParams(pattern="donchian_atr", timeframe="1d", range_lookback=16, atr_period=10, atr_mult=3.0)
        candidates = _perturb(params)
        self.assertTrue(candidates)
        self.assertEqual(candidates[0].strategy_id, params.strategy_id)

    def test_walk_forward_train_score_penalizes_losses(self) -> None:
        from qihuo_signal.models import BacktestResult, Settings

        params = StrategyParams(pattern="tsmom_vol").to_dict()
        good = BacktestResult("RB", "1d", "good", params, 1000, 0.1, -500, 0.5, 2.0, 10, 100, -100, 1)
        bad = BacktestResult("RB", "1d", "bad", params, -1000, -0.1, -500, 0.5, 2.0, 10, -100, -500, 5)
        self.assertGreater(_train_score(good, Settings()), _train_score(bad, Settings()))

    def test_walk_forward_summary_weights_win_rate_by_trades(self) -> None:
        settings = load_settings("missing-test-config.yaml")
        params = StrategyParams(pattern="donchian_atr", timeframe="15m", risk_mode="signal")
        candidates = pd.DataFrame(
            [{"params_json": json.dumps(params.to_dict(), ensure_ascii=False), "strategy_id": params.strategy_id}]
        )
        rows = [
            WalkForwardRow("RB", 1, "15m", "donchian_atr", params.strategy_id, 0, 0, 0, 0, 0, 0, 0.0, 0, "a", "b"),
            WalkForwardRow("RB", 2, "15m", "donchian_atr", params.strategy_id, 0, 0, 0, 0, 100, -50, 0.5, 20, "b", "c"),
            WalkForwardRow("RB", 3, "15m", "donchian_atr", params.strategy_id, 0, 0, 0, 0, 100, -50, 0.8, 5, "c", "d"),
        ]

        summary = _summarize_symbol(
            "RB",
            candidates,
            bars_from_closes([100 + (i % 3) for i in range(120)]),
            rows,
            settings,
            Backtester(settings),
            None,
        )

        self.assertAlmostEqual(summary.avg_test_win_rate, 14 / 25)

    def test_walk_forward_candidates_are_static_without_prior_results(self) -> None:
        settings = load_settings("missing-test-config.yaml")
        settings = settings.__class__(
            **{
                **settings.__dict__,
                "symbols": ("RB",),
                "instruments": {"RB": settings.instruments["RB"]},
                "timeframes": ("15m",),
            }
        )

        candidates = _load_candidates(Path("missing-reports"), LocalStore("missing-data"), settings, max_per_symbol=2)

        self.assertFalse(candidates.empty)
        self.assertEqual(set(candidates["symbol"]), {"RB"})
        self.assertTrue((candidates["robust_score"] == 0.0).all())


if __name__ == "__main__":
    unittest.main()
