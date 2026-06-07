from __future__ import annotations

import tempfile
import unittest

import pandas as pd

from qihuo_signal.config import load_settings
from qihuo_signal.models import StrategyParams
from qihuo_signal.polling import SignalPoller, closed_bars_only
from qihuo_signal.storage import LocalStore


class RecordingProvider:
    def __init__(self) -> None:
        self.updated_timeframes: tuple[str, ...] | None = None

    def update_recent(self, settings, store, timeframes=None) -> None:
        self.updated_timeframes = tuple(timeframes or ())


class PollingTests(unittest.TestCase):
    def test_intraday_live_signals_ignore_unsettled_latest_bar(self) -> None:
        bars = pd.DataFrame(
            {
                "timestamp": pd.to_datetime(
                    ["2026-06-05 09:15:00", "2026-06-05 09:30:00", "2026-06-05 09:45:00"]
                ),
                "open": [1, 1, 1],
                "high": [1, 1, 1],
                "low": [1, 1, 1],
                "close": [1, 1, 1],
            }
        )

        before_grace = closed_bars_only(bars, "15m", now=pd.Timestamp("2026-06-05 09:45:30"))
        after_grace = closed_bars_only(bars, "15m", now=pd.Timestamp("2026-06-05 09:46:01"))

        self.assertEqual(before_grace["timestamp"].max(), pd.Timestamp("2026-06-05 09:30:00"))
        self.assertEqual(after_grace["timestamp"].max(), pd.Timestamp("2026-06-05 09:45:00"))

    def test_daily_live_signals_wait_until_day_bar_close(self) -> None:
        bars = pd.DataFrame(
            {
                "timestamp": pd.to_datetime(["2026-06-04", "2026-06-05"]),
                "open": [1, 1],
                "high": [1, 1],
                "low": [1, 1],
                "close": [1, 1],
            }
        )

        before_close = closed_bars_only(bars, "1d", now=pd.Timestamp("2026-06-05 14:59:00"))
        after_close = closed_bars_only(bars, "1d", now=pd.Timestamp("2026-06-05 15:16:00"))

        self.assertEqual(before_close["timestamp"].max(), pd.Timestamp("2026-06-04"))
        self.assertEqual(after_close["timestamp"].max(), pd.Timestamp("2026-06-05"))

    def test_poll_updates_timeframes_used_by_live_profile(self) -> None:
        settings = load_settings("missing-test-config.yaml")
        settings = settings.__class__(
            **{
                **settings.__dict__,
                "symbols": ("RB",),
                "instruments": {"RB": settings.instruments["RB"]},
            }
        )
        params = StrategyParams(pattern="breakout", timeframe="60m")
        profile = {
            "walk_forward": {
                "RB": {
                    "status": "active",
                    "best": {
                        "params": params.to_dict(),
                        "strategy_id": params.strategy_id,
                    },
                }
            }
        }
        provider = RecordingProvider()
        with tempfile.TemporaryDirectory() as tmp:
            store = LocalStore(tmp)
            store.write_profiles(profile)
            poller = SignalPoller(settings, store, provider=provider)
            poller.poll_once()

        self.assertEqual(provider.updated_timeframes, ("60m",))


if __name__ == "__main__":
    unittest.main()
