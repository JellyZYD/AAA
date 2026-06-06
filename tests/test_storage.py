from __future__ import annotations

import tempfile
import unittest

from qihuo_signal.config import load_settings
from qihuo_signal.data_sources import SyntheticProvider
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


if __name__ == "__main__":
    unittest.main()

