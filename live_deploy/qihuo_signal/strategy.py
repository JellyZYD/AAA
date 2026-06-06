from __future__ import annotations

import math
from collections.abc import Callable
from dataclasses import replace
from typing import Any

import pandas as pd

from .events import event_bias
from .models import Pivot, StrategyAction, StrategyParams


RiskFilter = Callable[[StrategyAction, pd.Series], tuple[bool, str]]


def detect_pivots(bars: pd.DataFrame, window: int = 3, min_swing_pct: float = 0.006) -> list[Pivot]:
    if bars.empty or len(bars) < window * 2 + 3:
        return []
    df = bars.reset_index(drop=True)
    highs = df["high"].astype(float)
    lows = df["low"].astype(float)
    pivots: list[Pivot] = []
    for i in range(window, len(df) - window):
        hi_slice = highs.iloc[i - window : i + window + 1]
        lo_slice = lows.iloc[i - window : i + window + 1]
        high = float(highs.iloc[i])
        low = float(lows.iloc[i])
        span_low = float(lo_slice.min())
        span_high = float(hi_slice.max())
        if high >= float(hi_slice.max()) and span_low > 0 and (high - span_low) / span_low >= min_swing_pct:
            pivots.append(
                Pivot(
                    "high",
                    i,
                    i + window,
                    pd.Timestamp(df.at[i, "timestamp"]).to_pydatetime(),
                    pd.Timestamp(df.at[i + window, "timestamp"]).to_pydatetime(),
                    high,
                )
            )
        if low <= float(lo_slice.min()) and low > 0 and (span_high - low) / low >= min_swing_pct:
            pivots.append(
                Pivot(
                    "low",
                    i,
                    i + window,
                    pd.Timestamp(df.at[i, "timestamp"]).to_pydatetime(),
                    pd.Timestamp(df.at[i + window, "timestamp"]).to_pydatetime(),
                    low,
                )
            )
    filtered: list[Pivot] = []
    for pivot in sorted(pivots, key=lambda p: (p.index, p.kind)):
        if filtered and pivot.kind == filtered[-1].kind and pivot.index - filtered[-1].index <= window + 1:
            last = filtered[-1]
            more_extreme = (pivot.kind == "high" and pivot.price > last.price) or (
                pivot.kind == "low" and pivot.price < last.price
            )
            if more_extreme:
                filtered[-1] = pivot
            continue
        filtered.append(pivot)
    return sorted(filtered, key=lambda p: (p.confirm_index, p.index, p.kind))


class StrategyEngine:
    def generate_actions(
        self,
        bars: pd.DataFrame,
        params: StrategyParams,
        symbol: str,
        events: pd.DataFrame | None = None,
        risk_filter: RiskFilter | None = None,
    ) -> list[StrategyAction]:
        if bars.empty:
            return []
        df = bars.sort_values("timestamp").reset_index(drop=True)
        if params.pattern in {"swing_reversal", "trend_failure"}:
            return self._generate_swing_actions(df, params, symbol, events, risk_filter)
        if params.pattern == "breakout":
            return self._generate_breakout_actions(df, params, symbol, events, risk_filter)
        if params.pattern == "failed_breakout":
            return self._generate_failed_breakout_actions(df, params, symbol, events, risk_filter)
        if params.pattern == "donchian_atr":
            return self._generate_donchian_atr_actions(df, params, symbol, events, risk_filter)
        if params.pattern == "tsmom_vol":
            return self._generate_tsmom_vol_actions(df, params, symbol, events, risk_filter)
        if params.pattern == "vol_breakout":
            return self._generate_vol_breakout_actions(df, params, symbol, events, risk_filter)
        if params.pattern == "carry_tsmom":
            return self._generate_carry_tsmom_actions(df, params, symbol, events, risk_filter)
        raise ValueError(f"unknown pattern: {params.pattern}")

    def _generate_swing_actions(
        self,
        df: pd.DataFrame,
        params: StrategyParams,
        symbol: str,
        events: pd.DataFrame | None,
        risk_filter: RiskFilter | None,
    ) -> list[StrategyAction]:
        pivots = detect_pivots(df, params.swing_window, params.min_swing_pct)
        by_confirm: dict[int, list[Pivot]] = {}
        for pivot in pivots:
            by_confirm.setdefault(pivot.confirm_index, []).append(pivot)

        confirmed: list[Pivot] = []
        actions: list[StrategyAction] = []
        position = 0
        stop_price: float | None = None
        entry_index = -1
        cooldown = 0
        entry_reason = ""

        for i, row in df.iterrows():
            confirmed.extend(by_confirm.get(i, []))
            if cooldown > 0:
                cooldown -= 1
            ts = pd.Timestamp(row["timestamp"])
            close = float(row["close"])
            high = float(row["high"])
            low = float(row["low"])
            bias = event_bias(events, symbol, ts) if events is not None else 0.0

            if position == 1:
                action = None
                if stop_price is not None and low <= stop_price:
                    action = self._action(i, ts, "CLOSE_LONG", stop_price, "long stop hit", stop_price, 0.5, bias)
                elif i - entry_index >= params.max_hold_bars:
                    action = self._action(i, ts, "CLOSE_LONG", close, "long max hold reached", stop_price, 0.45, bias)
                elif self._short_setup(confirmed, close, params, trend_failure=params.pattern == "trend_failure"):
                    action = self._action(i, ts, "CLOSE_LONG", close, "long exit: bearish structure confirmed", stop_price, 0.62, bias)
                if action is not None:
                    actions.append(action)
                    position = 0
                    stop_price = None
                    cooldown = params.cooldown_bars
                    entry_reason = ""
                continue

            if position == -1:
                action = None
                if stop_price is not None and high >= stop_price:
                    action = self._action(i, ts, "CLOSE_SHORT", stop_price, "short stop hit", stop_price, 0.5, bias)
                elif i - entry_index >= params.max_hold_bars:
                    action = self._action(i, ts, "CLOSE_SHORT", close, "short max hold reached", stop_price, 0.45, bias)
                elif self._long_setup(confirmed, close, params, trend_failure=params.pattern == "trend_failure"):
                    action = self._action(i, ts, "CLOSE_SHORT", close, "short exit: bullish structure confirmed", stop_price, 0.62, bias)
                if action is not None:
                    actions.append(action)
                    position = 0
                    stop_price = None
                    cooldown = params.cooldown_bars
                    entry_reason = ""
                continue

            if cooldown > 0:
                continue

            long_setup = self._long_setup(confirmed, close, params, trend_failure=params.pattern == "trend_failure")
            short_setup = self._short_setup(confirmed, close, params, trend_failure=params.pattern == "trend_failure")
            if params.side in {"long", "both"} and long_setup:
                pivot_stop = self._last_pivot(confirmed, "low").price * (1 - params.breakout_pct)
                setup_stop = max(pivot_stop, close * (1 - params.stop_loss_pct))
                action = self._action(i, ts, "OPEN_LONG", close, long_setup, setup_stop, 0.64, bias)
                if self._passes_risk(action, row, risk_filter, actions):
                    actions.append(action)
                    position = 1
                    stop_price = setup_stop
                    entry_index = i
                    entry_reason = long_setup
                continue
            if params.side in {"short", "both"} and short_setup:
                pivot_stop = self._last_pivot(confirmed, "high").price * (1 + params.breakout_pct)
                setup_stop = min(pivot_stop, close * (1 + params.stop_loss_pct))
                action = self._action(i, ts, "OPEN_SHORT", close, short_setup, setup_stop, 0.64, bias)
                if self._passes_risk(action, row, risk_filter, actions):
                    actions.append(action)
                    position = -1
                    stop_price = setup_stop
                    entry_index = i
                    entry_reason = short_setup
                continue

        return actions

    def _generate_breakout_actions(
        self,
        df: pd.DataFrame,
        params: StrategyParams,
        symbol: str,
        events: pd.DataFrame | None,
        risk_filter: RiskFilter | None,
    ) -> list[StrategyAction]:
        actions: list[StrategyAction] = []
        position = 0
        stop_price: float | None = None
        entry_index = -1
        cooldown = 0
        for i, row in df.iterrows():
            if i < params.range_lookback:
                continue
            if cooldown > 0:
                cooldown -= 1
            ts = pd.Timestamp(row["timestamp"])
            close = float(row["close"])
            high = float(row["high"])
            low = float(row["low"])
            prior = df.iloc[i - params.range_lookback : i]
            range_high = float(prior["high"].max())
            range_low = float(prior["low"].min())
            bias = event_bias(events, symbol, ts) if events is not None else 0.0

            if position == 1:
                if stop_price is not None and low <= stop_price:
                    actions.append(self._action(i, ts, "CLOSE_LONG", stop_price, "breakout long stop", stop_price, 0.5, bias))
                    position = 0
                    cooldown = params.cooldown_bars
                elif close < range_low * (1 - params.breakout_pct) or i - entry_index >= params.max_hold_bars:
                    actions.append(self._action(i, ts, "CLOSE_LONG", close, "breakout long exit", stop_price, 0.55, bias))
                    position = 0
                    cooldown = params.cooldown_bars
                continue
            if position == -1:
                if stop_price is not None and high >= stop_price:
                    actions.append(self._action(i, ts, "CLOSE_SHORT", stop_price, "breakout short stop", stop_price, 0.5, bias))
                    position = 0
                    cooldown = params.cooldown_bars
                elif close > range_high * (1 + params.breakout_pct) or i - entry_index >= params.max_hold_bars:
                    actions.append(self._action(i, ts, "CLOSE_SHORT", close, "breakout short exit", stop_price, 0.55, bias))
                    position = 0
                    cooldown = params.cooldown_bars
                continue
            if cooldown > 0:
                continue
            if params.side in {"long", "both"} and close > range_high * (1 + params.breakout_pct):
                stop = max(range_low, close * (1 - params.stop_loss_pct))
                action = self._action(i, ts, "OPEN_LONG", close, "range breakout long", stop, 0.58, bias)
                if self._passes_risk(action, row, risk_filter, actions):
                    actions.append(action)
                    position = 1
                    stop_price = stop
                    entry_index = i
            elif params.side in {"short", "both"} and close < range_low * (1 - params.breakout_pct):
                stop = min(range_high, close * (1 + params.stop_loss_pct))
                action = self._action(i, ts, "OPEN_SHORT", close, "range breakout short", stop, 0.58, bias)
                if self._passes_risk(action, row, risk_filter, actions):
                    actions.append(action)
                    position = -1
                    stop_price = stop
                    entry_index = i
        return actions

    def _generate_failed_breakout_actions(
        self,
        df: pd.DataFrame,
        params: StrategyParams,
        symbol: str,
        events: pd.DataFrame | None,
        risk_filter: RiskFilter | None,
    ) -> list[StrategyAction]:
        actions: list[StrategyAction] = []
        position = 0
        stop_price: float | None = None
        entry_index = -1
        cooldown = 0
        for i, row in df.iterrows():
            if i < params.range_lookback:
                continue
            if cooldown > 0:
                cooldown -= 1
            ts = pd.Timestamp(row["timestamp"])
            close = float(row["close"])
            high = float(row["high"])
            low = float(row["low"])
            prior = df.iloc[i - params.range_lookback : i]
            range_high = float(prior["high"].max())
            range_low = float(prior["low"].min())
            bias = event_bias(events, symbol, ts) if events is not None else 0.0

            if position == 1:
                if stop_price is not None and low <= stop_price:
                    actions.append(self._action(i, ts, "CLOSE_LONG", stop_price, "failed-break long stop", stop_price, 0.5, bias))
                    position = 0
                    cooldown = params.cooldown_bars
                elif close > range_high * (1 + params.breakout_pct) or i - entry_index >= params.max_hold_bars:
                    actions.append(self._action(i, ts, "CLOSE_LONG", close, "failed-break long exit", stop_price, 0.52, bias))
                    position = 0
                    cooldown = params.cooldown_bars
                continue
            if position == -1:
                if stop_price is not None and high >= stop_price:
                    actions.append(self._action(i, ts, "CLOSE_SHORT", stop_price, "failed-break short stop", stop_price, 0.5, bias))
                    position = 0
                    cooldown = params.cooldown_bars
                elif close < range_low * (1 - params.breakout_pct) or i - entry_index >= params.max_hold_bars:
                    actions.append(self._action(i, ts, "CLOSE_SHORT", close, "failed-break short exit", stop_price, 0.52, bias))
                    position = 0
                    cooldown = params.cooldown_bars
                continue
            if cooldown > 0:
                continue
            if params.side in {"short", "both"} and high > range_high * (1 + params.breakout_pct) and close < range_high:
                stop = high * (1 + params.breakout_pct)
                action = self._action(i, ts, "OPEN_SHORT", close, "upside breakout failed; fade short", stop, 0.57, bias)
                if self._passes_risk(action, row, risk_filter, actions):
                    actions.append(action)
                    position = -1
                    stop_price = stop
                    entry_index = i
            elif params.side in {"long", "both"} and low < range_low * (1 - params.breakout_pct) and close > range_low:
                stop = low * (1 - params.breakout_pct)
                action = self._action(i, ts, "OPEN_LONG", close, "downside breakout failed; fade long", stop, 0.57, bias)
                if self._passes_risk(action, row, risk_filter, actions):
                    actions.append(action)
                    position = 1
                    stop_price = stop
                    entry_index = i
        return actions

    def _generate_donchian_atr_actions(
        self,
        df: pd.DataFrame,
        params: StrategyParams,
        symbol: str,
        events: pd.DataFrame | None,
        risk_filter: RiskFilter | None,
    ) -> list[StrategyAction]:
        df = df.copy()
        df["_atr"] = self._atr(df, params.atr_period)
        actions: list[StrategyAction] = []
        position = 0
        stop_price: float | None = None
        entry_index = -1
        cooldown = 0
        min_index = max(params.range_lookback, params.exit_lookback, params.atr_period)

        for i, row in df.iterrows():
            if i < min_index:
                continue
            if cooldown > 0:
                cooldown -= 1
            ts = pd.Timestamp(row["timestamp"])
            close = float(row["close"])
            high = float(row["high"])
            low = float(row["low"])
            atr = float(row["_atr"]) if pd.notna(row["_atr"]) else 0.0
            if atr <= 0:
                continue
            prior = df.iloc[i - params.range_lookback : i]
            exit_prior = df.iloc[i - params.exit_lookback : i]
            channel_high = float(prior["high"].max())
            channel_low = float(prior["low"].min())
            exit_high = float(exit_prior["high"].max())
            exit_low = float(exit_prior["low"].min())
            bias = event_bias(events, symbol, ts) if events is not None else 0.0

            if position == 1:
                stop_price = max(stop_price or -math.inf, close - params.atr_mult * atr)
                if low <= stop_price:
                    actions.append(self._action(i, ts, "CLOSE_LONG", stop_price, "donchian long ATR trailing stop", stop_price, 0.55, bias))
                    position = 0
                    cooldown = params.cooldown_bars
                elif close < exit_low or i - entry_index >= params.max_hold_bars:
                    actions.append(self._action(i, ts, "CLOSE_LONG", close, "donchian long channel exit", stop_price, 0.56, bias))
                    position = 0
                    cooldown = params.cooldown_bars
                continue
            if position == -1:
                stop_price = min(stop_price or math.inf, close + params.atr_mult * atr)
                if high >= stop_price:
                    actions.append(self._action(i, ts, "CLOSE_SHORT", stop_price, "donchian short ATR trailing stop", stop_price, 0.55, bias))
                    position = 0
                    cooldown = params.cooldown_bars
                elif close > exit_high or i - entry_index >= params.max_hold_bars:
                    actions.append(self._action(i, ts, "CLOSE_SHORT", close, "donchian short channel exit", stop_price, 0.56, bias))
                    position = 0
                    cooldown = params.cooldown_bars
                continue
            if cooldown > 0:
                continue

            if params.side in {"long", "both"} and close > channel_high * (1 + params.breakout_pct):
                stop = close - params.atr_mult * atr
                action = self._action(i, ts, "OPEN_LONG", close, "donchian channel breakout long", stop, 0.61, bias)
                if self._passes_risk(action, row, risk_filter, actions):
                    actions.append(action)
                    position = 1
                    stop_price = stop
                    entry_index = i
            elif params.side in {"short", "both"} and close < channel_low * (1 - params.breakout_pct):
                stop = close + params.atr_mult * atr
                action = self._action(i, ts, "OPEN_SHORT", close, "donchian channel breakout short", stop, 0.61, bias)
                if self._passes_risk(action, row, risk_filter, actions):
                    actions.append(action)
                    position = -1
                    stop_price = stop
                    entry_index = i
        return actions

    def _generate_tsmom_vol_actions(
        self,
        df: pd.DataFrame,
        params: StrategyParams,
        symbol: str,
        events: pd.DataFrame | None,
        risk_filter: RiskFilter | None,
    ) -> list[StrategyAction]:
        df = df.copy()
        df["_atr"] = self._atr(df, params.atr_period)
        one_bar_returns = df["close"].pct_change()
        lookback_return = df["close"].pct_change(params.momentum_lookback)
        period_vol = one_bar_returns.rolling(params.vol_lookback, min_periods=params.vol_lookback).std()
        period_vol = period_vol * math.sqrt(max(1, params.momentum_lookback))
        df["_ts_score"] = lookback_return / period_vol.where(period_vol > 0)

        actions: list[StrategyAction] = []
        position = 0
        stop_price: float | None = None
        entry_index = -1
        cooldown = 0
        min_index = max(params.momentum_lookback, params.vol_lookback, params.atr_period)

        for i, row in df.iterrows():
            if i < min_index:
                continue
            if cooldown > 0:
                cooldown -= 1
            ts = pd.Timestamp(row["timestamp"])
            close = float(row["close"])
            high = float(row["high"])
            low = float(row["low"])
            atr = float(row["_atr"]) if pd.notna(row["_atr"]) else 0.0
            score = float(row["_ts_score"]) if pd.notna(row["_ts_score"]) else 0.0
            if atr <= 0:
                continue
            bias = event_bias(events, symbol, ts) if events is not None else 0.0

            if position == 1:
                stop_price = max(stop_price or -math.inf, close - params.atr_mult * atr)
                if low <= stop_price:
                    actions.append(self._action(i, ts, "CLOSE_LONG", stop_price, "tsmom long ATR trailing stop", stop_price, 0.53, bias))
                    position = 0
                    cooldown = params.cooldown_bars
                elif score <= 0 or i - entry_index >= params.max_hold_bars:
                    actions.append(self._action(i, ts, "CLOSE_LONG", close, "tsmom long momentum faded", stop_price, 0.55, bias))
                    position = 0
                    cooldown = params.cooldown_bars
                continue
            if position == -1:
                stop_price = min(stop_price or math.inf, close + params.atr_mult * atr)
                if high >= stop_price:
                    actions.append(self._action(i, ts, "CLOSE_SHORT", stop_price, "tsmom short ATR trailing stop", stop_price, 0.53, bias))
                    position = 0
                    cooldown = params.cooldown_bars
                elif score >= 0 or i - entry_index >= params.max_hold_bars:
                    actions.append(self._action(i, ts, "CLOSE_SHORT", close, "tsmom short momentum faded", stop_price, 0.55, bias))
                    position = 0
                    cooldown = params.cooldown_bars
                continue
            if cooldown > 0:
                continue

            if params.side in {"long", "both"} and score >= params.score_threshold:
                stop = close - params.atr_mult * atr
                action = self._action(i, ts, "OPEN_LONG", close, f"positive volatility-scaled momentum score {score:.2f}", stop, 0.59, bias)
                if self._passes_risk(action, row, risk_filter, actions):
                    actions.append(action)
                    position = 1
                    stop_price = stop
                    entry_index = i
            elif params.side in {"short", "both"} and score <= -params.score_threshold:
                stop = close + params.atr_mult * atr
                action = self._action(i, ts, "OPEN_SHORT", close, f"negative volatility-scaled momentum score {score:.2f}", stop, 0.59, bias)
                if self._passes_risk(action, row, risk_filter, actions):
                    actions.append(action)
                    position = -1
                    stop_price = stop
                    entry_index = i
        return actions

    def _generate_vol_breakout_actions(
        self,
        df: pd.DataFrame,
        params: StrategyParams,
        symbol: str,
        events: pd.DataFrame | None,
        risk_filter: RiskFilter | None,
    ) -> list[StrategyAction]:
        df = df.copy()
        df["_atr"] = self._atr(df, params.atr_period)
        atr_pct = df["_atr"] / df["close"].where(df["close"] > 0)
        channel_width = (
            df["high"].rolling(params.range_lookback, min_periods=params.range_lookback).max()
            - df["low"].rolling(params.range_lookback, min_periods=params.range_lookback).min()
        ) / df["close"].where(df["close"] > 0)
        df["_atr_ratio"] = atr_pct.shift(1) / atr_pct.shift(1).rolling(params.vol_lookback, min_periods=params.vol_lookback).median()
        df["_width_ratio"] = channel_width.shift(1) / channel_width.shift(1).rolling(
            params.vol_lookback, min_periods=params.vol_lookback
        ).median()

        actions: list[StrategyAction] = []
        position = 0
        stop_price: float | None = None
        entry_index = -1
        cooldown = 0
        min_index = max(params.range_lookback, params.exit_lookback, params.atr_period, params.vol_lookback)

        for i, row in df.iterrows():
            if i < min_index:
                continue
            if cooldown > 0:
                cooldown -= 1
            ts = pd.Timestamp(row["timestamp"])
            close = float(row["close"])
            high = float(row["high"])
            low = float(row["low"])
            atr = float(row["_atr"]) if pd.notna(row["_atr"]) else 0.0
            atr_ratio = float(row["_atr_ratio"]) if pd.notna(row["_atr_ratio"]) else math.inf
            width_ratio = float(row["_width_ratio"]) if pd.notna(row["_width_ratio"]) else math.inf
            if atr <= 0:
                continue
            prior = df.iloc[i - params.range_lookback : i]
            exit_prior = df.iloc[i - params.exit_lookback : i]
            channel_high = float(prior["high"].max())
            channel_low = float(prior["low"].min())
            exit_high = float(exit_prior["high"].max())
            exit_low = float(exit_prior["low"].min())
            compressed = atr_ratio <= params.score_threshold and width_ratio <= max(params.score_threshold, 0.75)
            bias = event_bias(events, symbol, ts) if events is not None else 0.0

            if position == 1:
                stop_price = max(stop_price or -math.inf, close - params.atr_mult * atr)
                if low <= stop_price:
                    actions.append(self._action(i, ts, "CLOSE_LONG", stop_price, "vol breakout long ATR trailing stop", stop_price, 0.55, bias))
                    position = 0
                    cooldown = params.cooldown_bars
                elif close < exit_low or i - entry_index >= params.max_hold_bars:
                    actions.append(self._action(i, ts, "CLOSE_LONG", close, "vol breakout long channel exit", stop_price, 0.56, bias))
                    position = 0
                    cooldown = params.cooldown_bars
                continue
            if position == -1:
                stop_price = min(stop_price or math.inf, close + params.atr_mult * atr)
                if high >= stop_price:
                    actions.append(self._action(i, ts, "CLOSE_SHORT", stop_price, "vol breakout short ATR trailing stop", stop_price, 0.55, bias))
                    position = 0
                    cooldown = params.cooldown_bars
                elif close > exit_high or i - entry_index >= params.max_hold_bars:
                    actions.append(self._action(i, ts, "CLOSE_SHORT", close, "vol breakout short channel exit", stop_price, 0.56, bias))
                    position = 0
                    cooldown = params.cooldown_bars
                continue
            if cooldown > 0 or not compressed:
                continue

            if params.side in {"long", "both"} and close > channel_high * (1 + params.breakout_pct):
                stop = close - params.atr_mult * atr
                reason = f"volatility compression breakout long; ATR ratio {atr_ratio:.2f}, width ratio {width_ratio:.2f}"
                action = self._action(i, ts, "OPEN_LONG", close, reason, stop, 0.62, bias)
                if self._passes_risk(action, row, risk_filter, actions):
                    actions.append(action)
                    position = 1
                    stop_price = stop
                    entry_index = i
            elif params.side in {"short", "both"} and close < channel_low * (1 - params.breakout_pct):
                stop = close + params.atr_mult * atr
                reason = f"volatility compression breakout short; ATR ratio {atr_ratio:.2f}, width ratio {width_ratio:.2f}"
                action = self._action(i, ts, "OPEN_SHORT", close, reason, stop, 0.62, bias)
                if self._passes_risk(action, row, risk_filter, actions):
                    actions.append(action)
                    position = -1
                    stop_price = stop
                    entry_index = i
        return actions

    def _generate_carry_tsmom_actions(
        self,
        df: pd.DataFrame,
        params: StrategyParams,
        symbol: str,
        events: pd.DataFrame | None,
        risk_filter: RiskFilter | None,
    ) -> list[StrategyAction]:
        if "carry_signal" not in df.columns:
            return []
        df = df.copy()
        df["_atr"] = self._atr(df, params.atr_period)
        one_bar_returns = df["close"].pct_change()
        lookback_return = df["close"].pct_change(params.momentum_lookback)
        period_vol = one_bar_returns.rolling(params.vol_lookback, min_periods=params.vol_lookback).std()
        period_vol = period_vol * math.sqrt(max(1, params.momentum_lookback))
        df["_ts_score"] = lookback_return / period_vol.where(period_vol > 0)
        df["_carry_signal"] = pd.to_numeric(df["carry_signal"], errors="coerce").shift(1)

        actions: list[StrategyAction] = []
        position = 0
        stop_price: float | None = None
        entry_index = -1
        cooldown = 0
        min_index = max(params.momentum_lookback, params.vol_lookback, params.atr_period) + 1

        for i, row in df.iterrows():
            if i < min_index:
                continue
            if cooldown > 0:
                cooldown -= 1
            ts = pd.Timestamp(row["timestamp"])
            close = float(row["close"])
            high = float(row["high"])
            low = float(row["low"])
            atr = float(row["_atr"]) if pd.notna(row["_atr"]) else 0.0
            score = float(row["_ts_score"]) if pd.notna(row["_ts_score"]) else 0.0
            carry = float(row["_carry_signal"]) if pd.notna(row["_carry_signal"]) else 0.0
            if atr <= 0 or carry == 0:
                continue
            bias = event_bias(events, symbol, ts) if events is not None else 0.0

            if position == 1:
                stop_price = max(stop_price or -math.inf, close - params.atr_mult * atr)
                if low <= stop_price:
                    actions.append(self._action(i, ts, "CLOSE_LONG", stop_price, "carry tsmom long ATR trailing stop", stop_price, 0.53, bias))
                    position = 0
                    cooldown = params.cooldown_bars
                elif score <= 0 or carry < 0 or i - entry_index >= params.max_hold_bars:
                    actions.append(self._action(i, ts, "CLOSE_LONG", close, "carry tsmom long factor faded", stop_price, 0.55, bias))
                    position = 0
                    cooldown = params.cooldown_bars
                continue
            if position == -1:
                stop_price = min(stop_price or math.inf, close + params.atr_mult * atr)
                if high >= stop_price:
                    actions.append(self._action(i, ts, "CLOSE_SHORT", stop_price, "carry tsmom short ATR trailing stop", stop_price, 0.53, bias))
                    position = 0
                    cooldown = params.cooldown_bars
                elif score >= 0 or carry > 0 or i - entry_index >= params.max_hold_bars:
                    actions.append(self._action(i, ts, "CLOSE_SHORT", close, "carry tsmom short factor faded", stop_price, 0.55, bias))
                    position = 0
                    cooldown = params.cooldown_bars
                continue
            if cooldown > 0:
                continue

            if params.side in {"long", "both"} and score >= params.score_threshold and carry > 0:
                stop = close - params.atr_mult * atr
                reason = f"positive momentum {score:.2f} with backwardation carry {carry:.2%}"
                action = self._action(i, ts, "OPEN_LONG", close, reason, stop, 0.61, bias)
                if self._passes_risk(action, row, risk_filter, actions):
                    actions.append(action)
                    position = 1
                    stop_price = stop
                    entry_index = i
            elif params.side in {"short", "both"} and score <= -params.score_threshold and carry < 0:
                stop = close + params.atr_mult * atr
                reason = f"negative momentum {score:.2f} with contango carry {carry:.2%}"
                action = self._action(i, ts, "OPEN_SHORT", close, reason, stop, 0.61, bias)
                if self._passes_risk(action, row, risk_filter, actions):
                    actions.append(action)
                    position = -1
                    stop_price = stop
                    entry_index = i
        return actions

    def _long_setup(
        self,
        confirmed: list[Pivot],
        close: float,
        params: StrategyParams,
        trend_failure: bool = False,
    ) -> str:
        lows = [p for p in confirmed if p.kind == "low"]
        highs = [p for p in confirmed if p.kind == "high"]
        if len(lows) < 2 or not highs:
            return ""
        l1, l2 = lows[-2], lows[-1]
        required = l1.price * (1 + params.min_swing_pct)
        if trend_failure:
            required = l1.price * (1 - params.min_swing_pct * 0.5)
        if l2.price < required:
            return ""
        between = [h for h in highs if l1.index < h.index < l2.index]
        if not between:
            between = [h for h in highs if h.index < l2.index]
        if not between:
            return ""
        trigger = max(h.price for h in between)
        if close > trigger * (1 + params.breakout_pct):
            return f"bullish structure: second low {l2.price:.2f} held above {l1.price:.2f}, broke {trigger:.2f}"
        return ""

    def _short_setup(
        self,
        confirmed: list[Pivot],
        close: float,
        params: StrategyParams,
        trend_failure: bool = False,
    ) -> str:
        lows = [p for p in confirmed if p.kind == "low"]
        highs = [p for p in confirmed if p.kind == "high"]
        if len(highs) < 2 or not lows:
            return ""
        h1, h2 = highs[-2], highs[-1]
        required = h1.price * (1 - params.min_swing_pct)
        if trend_failure:
            required = h1.price * (1 + params.min_swing_pct * 0.5)
        if h2.price > required:
            return ""
        between = [l for l in lows if h1.index < l.index < h2.index]
        if not between:
            between = [l for l in lows if l.index < h2.index]
        if not between:
            return ""
        trigger = min(l.price for l in between)
        if close < trigger * (1 - params.breakout_pct):
            return f"bearish structure: second high {h2.price:.2f} stayed below {h1.price:.2f}, broke {trigger:.2f}"
        return ""

    def _last_pivot(self, confirmed: list[Pivot], kind: str) -> Pivot:
        for pivot in reversed(confirmed):
            if pivot.kind == kind:
                return pivot
        raise ValueError(f"no {kind} pivot")

    def _atr(self, df: pd.DataFrame, period: int) -> pd.Series:
        high = df["high"].astype(float)
        low = df["low"].astype(float)
        close = df["close"].astype(float)
        prev_close = close.shift(1)
        true_range = pd.concat(
            [
                high - low,
                (high - prev_close).abs(),
                (low - prev_close).abs(),
            ],
            axis=1,
        ).max(axis=1)
        return true_range.rolling(period, min_periods=period).mean()

    def _action(
        self,
        index: int,
        timestamp: pd.Timestamp,
        action: str,
        price: float,
        reason: str,
        stop_price: float | None,
        confidence: float,
        news_bias: float,
    ) -> StrategyAction:
        adjusted = confidence + max(-0.2, min(0.2, news_bias * 0.2))
        if action.endswith("SHORT"):
            adjusted = confidence + max(-0.2, min(0.2, -news_bias * 0.2))
        return StrategyAction(
            index=index,
            timestamp=timestamp.to_pydatetime(),
            action=action,  # type: ignore[arg-type]
            price=float(price),
            reason=reason,
            stop_price=float(stop_price) if stop_price is not None else None,
            confidence=max(0.0, min(1.0, adjusted)),
            details={"news_bias": news_bias},
        )

    def _passes_risk(
        self,
        action: StrategyAction,
        row: pd.Series,
        risk_filter: RiskFilter | None,
        actions: list[StrategyAction],
    ) -> bool:
        if risk_filter is None:
            return True
        ok, reason = risk_filter(action, row)
        if ok:
            return True
        blocked = replace(action, action="RISK_BLOCKED", reason=reason, confidence=min(action.confidence, 0.3))
        actions.append(blocked)
        return False


def build_param_grid(
    timeframes: tuple[str, ...],
    fast: bool = False,
    sides: tuple[str, ...] = ("both",),
    patterns: tuple[str, ...] | None = None,
) -> list[StrategyParams]:
    selected_patterns = list(
        patterns
        or (
            "swing_reversal",
            "breakout",
            "failed_breakout",
            "trend_failure",
            "donchian_atr",
            "tsmom_vol",
            "vol_breakout",
            "carry_tsmom",
        )
    )
    windows = [2, 3] if fast else [2, 3, 4]
    swing_pcts = [0.004, 0.008] if fast else [0.003, 0.006, 0.01]
    breakout_pcts = [0.0015, 0.003] if fast else [0.001, 0.0025, 0.005]
    range_lookbacks = [16, 32] if fast else [16, 24, 48]
    max_holds = [32, 64] if fast else [24, 48, 96]
    atr_periods = [10, 14] if fast else [10, 14, 20]
    atr_mults = [2.0, 3.0] if fast else [1.8, 2.5, 3.2]
    exit_lookbacks = [8, 16] if fast else [8, 12, 24]
    momentum_lookbacks = [24, 48] if fast else [24, 48, 96]
    vol_lookbacks = [24, 48] if fast else [24, 48, 96]
    score_thresholds = [0.4, 0.8] if fast else [0.3, 0.6, 0.9]
    compression_thresholds = [0.75, 0.9] if fast else [0.65, 0.8, 0.95]
    risk_modes = ["strict", "signal", "aggressive"]
    params: list[StrategyParams] = []
    for timeframe in timeframes:
        for pattern in selected_patterns:
            for side in sides:
                for risk_mode in risk_modes:
                    if pattern in {"swing_reversal", "trend_failure"}:
                        for window in windows:
                            for swing_pct in swing_pcts:
                                for breakout_pct in breakout_pcts:
                                    for max_hold in max_holds:
                                        params.append(
                                            StrategyParams(
                                                pattern=pattern,  # type: ignore[arg-type]
                                                side=side,  # type: ignore[arg-type]
                                                timeframe=timeframe,
                                                swing_window=window,
                                                min_swing_pct=swing_pct,
                                                breakout_pct=breakout_pct,
                                                max_hold_bars=max_hold,
                                                risk_mode=risk_mode,  # type: ignore[arg-type]
                                            )
                                        )
                    else:
                        if pattern in {"breakout", "failed_breakout"}:
                            for lookback in range_lookbacks:
                                for breakout_pct in breakout_pcts:
                                    for max_hold in max_holds:
                                        params.append(
                                            StrategyParams(
                                                pattern=pattern,  # type: ignore[arg-type]
                                                side=side,  # type: ignore[arg-type]
                                                timeframe=timeframe,
                                                range_lookback=lookback,
                                                breakout_pct=breakout_pct,
                                                max_hold_bars=max_hold,
                                                risk_mode=risk_mode,  # type: ignore[arg-type]
                                            )
                                        )
                        elif pattern in {"donchian_atr", "vol_breakout"}:
                            for lookback in range_lookbacks:
                                for breakout_pct in breakout_pcts:
                                    for atr_period in atr_periods:
                                        for atr_mult in atr_mults:
                                            for exit_lookback in exit_lookbacks:
                                                for max_hold in max_holds:
                                                    thresholds = compression_thresholds if pattern == "vol_breakout" else [0.4]
                                                    for threshold in thresholds:
                                                        params.append(
                                                            StrategyParams(
                                                                pattern=pattern,  # type: ignore[arg-type]
                                                                side=side,  # type: ignore[arg-type]
                                                                timeframe=timeframe,
                                                                range_lookback=lookback,
                                                                breakout_pct=breakout_pct,
                                                                atr_period=atr_period,
                                                                atr_mult=atr_mult,
                                                                exit_lookback=exit_lookback,
                                                                max_hold_bars=max_hold,
                                                                vol_lookback=48,
                                                                score_threshold=threshold,
                                                                risk_mode=risk_mode,  # type: ignore[arg-type]
                                                            )
                                                        )
                        elif pattern in {"tsmom_vol", "carry_tsmom"}:
                            if pattern == "carry_tsmom" and timeframe != "1d":
                                continue
                            for momentum_lookback in momentum_lookbacks:
                                for vol_lookback in vol_lookbacks:
                                    for threshold in score_thresholds:
                                        for atr_period in atr_periods:
                                            for atr_mult in atr_mults:
                                                for max_hold in max_holds:
                                                    params.append(
                                                        StrategyParams(
                                                            pattern=pattern,  # type: ignore[arg-type]
                                                            side=side,  # type: ignore[arg-type]
                                                            timeframe=timeframe,
                                                            momentum_lookback=momentum_lookback,
                                                            vol_lookback=vol_lookback,
                                                            score_threshold=threshold,
                                                            atr_period=atr_period,
                                                            atr_mult=atr_mult,
                                                            max_hold_bars=max_hold,
                                                            risk_mode=risk_mode,  # type: ignore[arg-type]
                                                        )
                                                    )
    return params
