from __future__ import annotations

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
) -> list[StrategyParams]:
    patterns = ["swing_reversal", "breakout", "failed_breakout", "trend_failure"]
    windows = [2, 3] if fast else [2, 3, 4]
    swing_pcts = [0.004, 0.008] if fast else [0.003, 0.006, 0.01]
    breakout_pcts = [0.0015, 0.003] if fast else [0.001, 0.0025, 0.005]
    range_lookbacks = [16, 32] if fast else [16, 24, 48]
    max_holds = [32, 64] if fast else [24, 48, 96]
    risk_modes = ["strict", "signal", "aggressive"]
    params: list[StrategyParams] = []
    for timeframe in timeframes:
        for pattern in patterns:
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
    return params
