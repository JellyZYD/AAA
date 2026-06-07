from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any, Literal


ActionType = Literal[
    "OPEN_LONG",
    "OPEN_SHORT",
    "CLOSE_LONG",
    "CLOSE_SHORT",
    "HOLD",
    "WATCH_ONLY",
    "RISK_BLOCKED",
]

RiskMode = Literal["strict", "signal", "aggressive"]
PatternName = Literal[
    "swing_reversal",
    "breakout",
    "failed_breakout",
    "trend_failure",
    "donchian_atr",
    "tsmom_vol",
    "vol_breakout",
    "carry_tsmom",
    "quality_tsmom",
    "ensemble_trend",
    "trend_pullback",
]
Side = Literal["long", "short", "both"]


@dataclass(frozen=True)
class InstrumentSpec:
    symbol: str
    name: str
    exchange: str
    ak_symbol: str
    multiplier: float
    tick_size: float
    margin_rate: float
    fee_rate: float = 0.0001
    min_volume: int = 1

    def margin(self, price: float, qty: int = 1) -> float:
        return float(price) * self.multiplier * self.margin_rate * qty

    def notional(self, price: float, qty: int = 1) -> float:
        return float(price) * self.multiplier * qty


@dataclass(frozen=True)
class BacktestSettings:
    objective: str = "max_return"
    train_ratio: float = 0.7
    slippage_ticks: int = 1
    min_trades_for_champion: int = 3


@dataclass(frozen=True)
class LLMSettings:
    provider: str = "openai_compatible"
    base_url: str | None = None
    api_key: str | None = None
    model: str | None = None
    timeout_seconds: float = 30.0


@dataclass(frozen=True)
class AlertSettings:
    provider: str = "wecom"
    dry_run: bool = False
    wecom_webhook_url: str | None = None
    qq_app_id: str | None = None
    qq_app_secret: str | None = None
    qq_target_id: str | None = None
    qq_target_type: str = "group"
    qq_api_base: str = "https://api.sgroup.qq.com"
    qq_token_base: str = "https://bots.qq.com"


@dataclass(frozen=True)
class Settings:
    capital: float = 8500
    max_margin_budget: float = 8000
    max_risk_per_trade: float = 1700
    poll_interval_minutes: int = 15
    data_root: str = "data"
    reports_root: str = "reports"
    timeframes: tuple[str, ...] = ("15m", "30m", "60m", "1d")
    symbols: tuple[str, ...] = ("SP", "SR", "CJ", "UR", "FG", "C", "RB", "RM", "HC", "SA", "CS")
    instruments: dict[str, InstrumentSpec] = field(default_factory=dict)
    backtest: BacktestSettings = field(default_factory=BacktestSettings)
    llm: LLMSettings = field(default_factory=LLMSettings)
    alert: AlertSettings = field(default_factory=AlertSettings)


@dataclass(frozen=True)
class Pivot:
    kind: Literal["high", "low"]
    index: int
    confirm_index: int
    timestamp: datetime
    confirm_timestamp: datetime
    price: float


@dataclass(frozen=True)
class StrategyParams:
    pattern: PatternName
    side: Side = "both"
    timeframe: str = "15m"
    swing_window: int = 3
    min_swing_pct: float = 0.006
    breakout_pct: float = 0.002
    range_lookback: int = 24
    stop_loss_pct: float = 0.015
    max_hold_bars: int = 64
    cooldown_bars: int = 4
    risk_mode: RiskMode = "strict"
    news_weight: float = 0.2
    atr_period: int = 14
    atr_mult: float = 2.5
    exit_lookback: int = 12
    momentum_lookback: int = 48
    vol_lookback: int = 48
    score_threshold: float = 0.4
    trend_quality_threshold: float = 0.25

    @property
    def strategy_id(self) -> str:
        values = [
            self.pattern,
            self.side,
            self.timeframe,
            f"w{self.swing_window}",
            f"sw{self.min_swing_pct:g}",
            f"br{self.breakout_pct:g}",
            f"lb{self.range_lookback}",
            f"sl{self.stop_loss_pct:g}",
            f"mh{self.max_hold_bars}",
            f"cd{self.cooldown_bars}",
            f"atr{self.atr_period}",
            f"am{self.atr_mult:g}",
            f"ex{self.exit_lookback}",
            f"mom{self.momentum_lookback}",
            f"vol{self.vol_lookback}",
            f"th{self.score_threshold:g}",
            f"tq{self.trend_quality_threshold:g}" if self.pattern in {"quality_tsmom", "ensemble_trend", "trend_pullback"} else "",
            self.risk_mode,
        ]
        return "|".join(str(v) for v in values if v != "")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "StrategyParams":
        allowed = cls.__dataclass_fields__.keys()
        return cls(**{k: v for k, v in data.items() if k in allowed})


@dataclass(frozen=True)
class StrategyAction:
    index: int
    timestamp: datetime
    action: ActionType
    price: float
    reason: str
    stop_price: float | None = None
    confidence: float = 0.5
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        out = asdict(self)
        out["timestamp"] = self.timestamp.isoformat()
        return out


@dataclass(frozen=True)
class Trade:
    symbol: str
    contract: str
    side: Literal["LONG", "SHORT"]
    entry_time: datetime
    exit_time: datetime
    entry_price: float
    exit_price: float
    qty: int
    gross_pnl: float
    fees: float
    net_pnl: float
    entry_reason: str
    exit_reason: str
    margin: float

    def to_dict(self) -> dict[str, Any]:
        out = asdict(self)
        out["entry_time"] = self.entry_time.isoformat()
        out["exit_time"] = self.exit_time.isoformat()
        return out


@dataclass(frozen=True)
class BacktestResult:
    symbol: str
    timeframe: str
    strategy_id: str
    params: dict[str, Any]
    net_pnl: float
    total_return: float
    max_drawdown: float
    win_rate: float
    profit_factor: float
    trade_count: int
    avg_trade: float
    max_loss_trade: float
    consecutive_losses: int
    train_net_pnl: float | None = None
    test_net_pnl: float | None = None
    overfit_flag: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class NewsEvent:
    symbol: str
    timestamp: datetime
    title: str
    source: str = "manual"
    direction: Literal["bullish", "bearish", "neutral"] = "neutral"
    confidence: float = 0.0
    horizon_days: int = 10
    impact_score: float = 0.0
    similar_events: str = ""
    raw: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        out = asdict(self)
        out["timestamp"] = self.timestamp.isoformat()
        return out


@dataclass(frozen=True)
class Signal:
    symbol: str
    contract: str
    timestamp: datetime
    action: ActionType
    price: float
    confidence: float
    trigger_price: float | None
    invalid_price: float | None
    reason: str
    news_evidence: str
    risk_check: str
    strategy_rank: int | None = None
    strategy_id: str | None = None

    def to_dict(self) -> dict[str, Any]:
        out = asdict(self)
        out["timestamp"] = self.timestamp.isoformat()
        return out
