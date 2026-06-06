from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Iterable

import pandas as pd

from .models import InstrumentSpec, Settings
from .storage import LocalStore, normalize_bars


TIMEFRAME_TO_AK_PERIOD = {
    "1m": "1",
    "5m": "5",
    "15m": "15",
    "30m": "30",
    "60m": "60",
}


class MissingDependencyError(RuntimeError):
    pass


@dataclass
class SelectedContract:
    symbol: str
    contract: str
    reason: str


class AkShareProvider:
    """AkShare-backed market data provider.

    The provider deliberately imports AkShare lazily so local tests and sample
    backtests do not require network/data dependencies.
    """

    def __init__(self) -> None:
        try:
            import akshare as ak
        except Exception as exc:
            raise MissingDependencyError("AkShare is not installed. Install with: python -m pip install -e .[data]") from exc
        self.ak = ak

    def fetch_bars(self, spec: InstrumentSpec, timeframe: str) -> pd.DataFrame:
        if timeframe == "1d":
            raw = self.ak.futures_zh_daily_sina(symbol=spec.ak_symbol)
            df = normalize_bars(raw)
            df["contract"] = spec.ak_symbol
            df["source"] = "akshare:futures_zh_daily_sina"
            return df
        if timeframe not in TIMEFRAME_TO_AK_PERIOD:
            raise ValueError(f"Unsupported AkShare timeframe: {timeframe}")
        raw = self.ak.futures_zh_minute_sina(symbol=spec.ak_symbol, period=TIMEFRAME_TO_AK_PERIOD[timeframe])
        df = normalize_bars(raw)
        df["contract"] = spec.ak_symbol
        df["source"] = "akshare:futures_zh_minute_sina"
        return df

    def fetch_all(self, settings: Settings, store: LocalStore, timeframes: Iterable[str] | None = None) -> None:
        for symbol in settings.symbols:
            spec = settings.instruments[symbol]
            for timeframe in timeframes or settings.timeframes:
                bars = self.fetch_bars(spec, timeframe)
                store.write_bars(symbol, timeframe, bars, append=False)

    def update_recent(self, settings: Settings, store: LocalStore, timeframes: Iterable[str] | None = None) -> None:
        for symbol in settings.symbols:
            spec = settings.instruments[symbol]
            for timeframe in timeframes or settings.timeframes:
                bars = self.fetch_bars(spec, timeframe)
                store.write_bars(symbol, timeframe, bars, append=True)

    def select_trade_contract(self, spec: InstrumentSpec) -> SelectedContract:
        # The free Sina continuous symbol is enough for trend research. For live
        # manual trading, users should verify the currently liquid main/second
        # contract in their broker before acting.
        return SelectedContract(spec.symbol, spec.ak_symbol, "continuous symbol fallback")


class SyntheticProvider:
    """Deterministic local data for tests and first-run validation."""

    def __init__(self, start: str = "2024-01-01", bars: int = 620) -> None:
        self.start = pd.Timestamp(start)
        self.bars = bars

    def fetch_bars(self, spec: InstrumentSpec, timeframe: str) -> pd.DataFrame:
        freq = {"15m": "15min", "30m": "30min", "60m": "60min", "1d": "1D"}.get(timeframe, "15min")
        periods = self.bars if timeframe != "1d" else max(180, self.bars // 4)
        timestamps = pd.date_range(self.start, periods=periods, freq=freq)
        base = _base_price(spec.symbol)
        rows = []
        last_close = base
        for i, ts in enumerate(timestamps):
            regime = (i // max(30, periods // 8)) % 4
            drift = [0.0018, -0.0014, 0.0002, 0.0022][regime]
            cycle = math.sin(i / 9.0) * 0.004 + math.sin(i / 31.0) * 0.006
            shock = 0.0
            if i in {int(periods * 0.22), int(periods * 0.55), int(periods * 0.78)}:
                shock = [0.035, -0.045, 0.028][len([x for x in [0.22, 0.55, 0.78] if i >= int(periods * x)]) - 1]
            close = max(spec.tick_size, last_close * (1 + drift + cycle + shock))
            high = max(close, last_close) * (1 + 0.004 + abs(math.sin(i / 5.0)) * 0.004)
            low = min(close, last_close) * (1 - 0.004 - abs(math.cos(i / 7.0)) * 0.004)
            open_ = last_close
            volume = int(2000 + 1500 * abs(math.sin(i / 11.0)) + (regime + 1) * 300)
            hold = int(30000 + i * 7 + 2000 * math.sin(i / 29.0))
            rows.append(
                {
                    "timestamp": ts,
                    "open": round_to_tick(open_, spec.tick_size),
                    "high": round_to_tick(high, spec.tick_size),
                    "low": round_to_tick(low, spec.tick_size),
                    "close": round_to_tick(close, spec.tick_size),
                    "volume": volume,
                    "hold": hold,
                    "settle": round_to_tick(close, spec.tick_size),
                    "contract": spec.ak_symbol,
                    "source": "synthetic",
                }
            )
            last_close = close
        return pd.DataFrame(rows)

    def fetch_all(self, settings: Settings, store: LocalStore, timeframes: Iterable[str] | None = None) -> None:
        for symbol in settings.symbols:
            spec = settings.instruments[symbol]
            for timeframe in timeframes or settings.timeframes:
                store.write_bars(symbol, timeframe, self.fetch_bars(spec, timeframe), append=False)

    def update_recent(self, settings: Settings, store: LocalStore, timeframes: Iterable[str] | None = None) -> None:
        now = datetime.now().replace(second=0, microsecond=0)
        for symbol in settings.symbols:
            spec = settings.instruments[symbol]
            for timeframe in timeframes or ("15m",):
                current = store.read_bars(symbol, timeframe)
                if current.empty:
                    bars = self.fetch_bars(spec, timeframe).tail(200)
                else:
                    latest = pd.to_datetime(current["timestamp"]).max()
                    step = _timeframe_delta(timeframe)
                    needed = max(1, int((pd.Timestamp(now) - latest) / step))
                    bars = self.fetch_bars(spec, timeframe).tail(needed)
                    bars["timestamp"] = [latest + step * (i + 1) for i in range(len(bars))]
                store.write_bars(symbol, timeframe, bars, append=True)

    def select_trade_contract(self, spec: InstrumentSpec) -> SelectedContract:
        return SelectedContract(spec.symbol, spec.ak_symbol, "synthetic continuous contract")


def round_to_tick(price: float, tick: float) -> float:
    if tick <= 0:
        return round(price, 4)
    return round(round(price / tick) * tick, 6)


def _base_price(symbol: str) -> float:
    return {
        "SP": 5600,
        "SR": 6200,
        "CJ": 10500,
        "UR": 1900,
        "FG": 1500,
        "C": 2400,
        "RB": 3300,
        "RM": 2600,
        "HC": 3400,
        "SA": 1800,
        "CS": 2850,
    }.get(symbol, 3000)


def _timeframe_delta(timeframe: str) -> timedelta:
    if timeframe.endswith("m"):
        return timedelta(minutes=int(timeframe[:-1]))
    if timeframe.endswith("d") or timeframe == "1d":
        return timedelta(days=1)
    return timedelta(minutes=15)

