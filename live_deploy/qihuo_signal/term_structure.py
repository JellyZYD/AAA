from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import datetime
from typing import Iterable

import pandas as pd

from .models import Settings
from .storage import LocalStore, normalize_bars


REALTIME_NAMES = {
    "SP": "纸浆",
    "SR": "白糖",
    "CJ": "红枣",
    "UR": "尿素",
    "FG": "玻璃",
    "C": "玉米",
    "RB": "螺纹钢",
    "RM": "菜粕",
    "HC": "热轧卷板",
    "SA": "纯碱",
    "CS": "玉米淀粉",
}


@dataclass(frozen=True)
class TermFetchStats:
    symbol: str
    contracts_tried: int
    contracts_loaded: int
    rows: int
    start: str | None
    end: str | None


def fetch_and_store_term_structure(
    provider,
    settings: Settings,
    store: LocalStore,
    symbols: Iterable[str] | None = None,
    start_year: int = 2023,
    end_year: int | None = None,
) -> list[TermFetchStats]:
    end_year = end_year or datetime.now().year + 1
    stats: list[TermFetchStats] = []
    for symbol in symbols or settings.symbols:
        frame, tried, loaded = build_historical_term_structure(provider.ak, symbol, start_year, end_year)
        store.write_term_structure(symbol, frame, append=False)
        stats.append(
            TermFetchStats(
                symbol=symbol,
                contracts_tried=tried,
                contracts_loaded=loaded,
                rows=len(frame),
                start=str(frame["timestamp"].min().date()) if not frame.empty else None,
                end=str(frame["timestamp"].max().date()) if not frame.empty else None,
            )
        )
    return stats


def build_historical_term_structure(ak, symbol: str, start_year: int, end_year: int) -> tuple[pd.DataFrame, int, int]:
    contract_rows: list[pd.DataFrame] = []
    tried = 0
    loaded = 0
    for contract in _contract_codes(symbol, start_year, end_year):
        tried += 1
        try:
            raw = ak.futures_zh_daily_sina(symbol=contract)
            bars = normalize_bars(raw)
        except Exception:
            continue
        if bars.empty:
            continue
        bars["contract"] = contract
        bars["contract_month"] = _contract_month(contract)
        price = bars["settle"].where(bars["settle"] > 0, bars["close"])
        bars["term_price"] = pd.to_numeric(price, errors="coerce")
        bars = bars[(bars["term_price"] > 0) & (bars["hold"] > 0)].copy()
        if bars.empty:
            continue
        contract_rows.append(bars[["timestamp", "contract", "contract_month", "term_price", "volume", "hold"]])
        loaded += 1
    if not contract_rows:
        return pd.DataFrame(), tried, loaded
    contracts = pd.concat(contract_rows, ignore_index=True)
    contracts = contracts.drop_duplicates(subset=["timestamp", "contract"], keep="last")
    rows = []
    for timestamp, group in contracts.groupby("timestamp", sort=True):
        liquid = group.sort_values("hold", ascending=False).head(2).copy()
        if len(liquid) < 2:
            continue
        by_expiry = liquid.sort_values("contract_month")
        front = by_expiry.iloc[0]
        second = by_expiry.iloc[1]
        front_price = float(front["term_price"])
        second_price = float(second["term_price"])
        days_between = max(30.0, float((pd.Timestamp(second["contract_month"]) - pd.Timestamp(front["contract_month"])).days))
        term_spread = second_price / front_price - 1.0
        annualized_carry = term_spread * 365.0 / days_between
        main = liquid.iloc[0]
        second_main = liquid.iloc[1]
        rows.append(
            {
                "timestamp": pd.Timestamp(timestamp),
                "front_contract": str(front["contract"]),
                "second_contract": str(second["contract"]),
                "front_price": front_price,
                "second_price": second_price,
                "front_hold": float(front["hold"]),
                "second_hold": float(second["hold"]),
                "main_contract": str(main["contract"]),
                "second_main_contract": str(second_main["contract"]),
                "main_hold": float(main["hold"]),
                "second_main_hold": float(second_main["hold"]),
                "term_liquidity": float(front["hold"]) + float(second["hold"]),
                "term_spread": term_spread,
                "annualized_carry": annualized_carry,
                "carry_signal": -annualized_carry,
                "days_between_contracts": days_between,
                "source": "akshare:futures_zh_daily_sina_contracts",
            }
        )
    frame = pd.DataFrame(rows)
    if frame.empty:
        return frame, tried, loaded
    for col in ["term_spread", "annualized_carry", "carry_signal"]:
        frame[col] = pd.to_numeric(frame[col], errors="coerce").replace([math.inf, -math.inf], pd.NA)
    return frame.dropna(subset=["carry_signal"]).sort_values("timestamp").reset_index(drop=True), tried, loaded


def fetch_realtime_term_structure(provider, symbol: str) -> pd.DataFrame:
    name = REALTIME_NAMES.get(symbol, symbol)
    raw = provider.ak.futures_zh_realtime(symbol=name)
    df = raw.copy()
    if df.empty:
        return df
    df["timestamp"] = pd.to_datetime(df["tradedate"].astype(str) + " " + df["ticktime"].astype(str), errors="coerce")
    df["price"] = pd.to_numeric(df["trade"], errors="coerce")
    df["hold"] = pd.to_numeric(df["position"], errors="coerce")
    df["volume"] = pd.to_numeric(df["volume"], errors="coerce")
    df = df[df["symbol"].astype(str).str.match(r"^[A-Z]+\\d{4}$", na=False)]
    return df.sort_values("hold", ascending=False).reset_index(drop=True)


def _contract_codes(symbol: str, start_year: int, end_year: int) -> list[str]:
    return [f"{symbol}{year % 100:02d}{month:02d}" for year in range(start_year, end_year + 1) for month in range(1, 13)]


def _contract_month(contract: str) -> pd.Timestamp:
    digits = "".join(ch for ch in contract if ch.isdigit())
    if len(digits) < 4:
        raise ValueError(f"cannot parse contract month: {contract}")
    yy = int(digits[:2])
    mm = int(digits[2:4])
    year = 2000 + yy if yy < 80 else 1900 + yy
    return pd.Timestamp(year=year, month=mm, day=1)
