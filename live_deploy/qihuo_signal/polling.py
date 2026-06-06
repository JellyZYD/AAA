from __future__ import annotations

import json
import time
from datetime import datetime

import pandas as pd

from .alerts import AlertSender, format_signal
from .data_sources import AkShareProvider, SelectedContract
from .models import InstrumentSpec, Settings, Signal, StrategyAction, StrategyParams
from .storage import LocalStore
from .strategy import StrategyEngine


class SignalPoller:
    def __init__(
        self,
        settings: Settings,
        store: LocalStore,
        provider=None,
        alert_sender: AlertSender | None = None,
        profile: str = "live",
    ) -> None:
        self.settings = settings
        self.store = store
        self.provider = provider
        self.alert_sender = alert_sender
        self.profile = profile
        self.engine = StrategyEngine()

    def poll_once(self, include_watch: bool = False, update_data: bool = True) -> list[Signal]:
        if update_data and self.provider is not None:
            self.provider.update_recent(self.settings, self.store, timeframes=("15m",))
        champions = self._load_profile()
        events = self.store.read_events()
        signals: list[Signal] = []
        for rank, symbol in enumerate(self.settings.symbols, 1):
            spec = self.settings.instruments[symbol]
            champion = champions.get(symbol)
            if not champion or (champion.get("status") and champion.get("status") != "active"):
                if include_watch:
                    signals.append(self._watch_signal(symbol, spec, champion, "no active champion"))
                continue
            best = champion["best"]
            params_raw = best.get("params") or json.loads(best.get("params_json", "{}"))
            params = StrategyParams.from_dict(params_raw)
            bars = self.store.read_bars(symbol, params.timeframe)
            if bars.empty or len(bars) < 80:
                if include_watch:
                    signals.append(self._watch_signal(symbol, spec, champion, "not enough local bars"))
                continue
            risk_filter = self._risk_filter(spec, params)
            actions = self.engine.generate_actions(bars, params, symbol=symbol, events=events, risk_filter=risk_filter)
            recent = [action for action in actions if action.index >= len(bars) - 2]
            if not recent:
                if include_watch:
                    signals.append(self._watch_signal(symbol, spec, champion, "no new action"))
                continue
            action = recent[-1]
            selected = self._select_contract(spec)
            signal = self._to_signal(symbol, selected, action, best, rank)
            signals.append(signal)
        self.store.append_signals(signals)
        if self.alert_sender is not None:
            for signal in signals:
                if signal.action != "HOLD" or include_watch:
                    self.alert_sender.send(format_signal(signal))
        return signals

    def run_forever(self) -> None:
        while True:
            self.poll_once(include_watch=False, update_data=True)
            time.sleep(self.settings.poll_interval_minutes * 60)

    def _risk_filter(self, spec: InstrumentSpec, params: StrategyParams):
        def check(action: StrategyAction, row: pd.Series) -> tuple[bool, str]:
            margin = spec.margin(action.price)
            stop_risk = 0.0 if action.stop_price is None else abs(action.price - action.stop_price) * spec.multiplier
            if params.risk_mode == "signal":
                return True, f"signal mode; margin {margin:.0f}, stop risk {stop_risk:.0f}"
            aggressive_limit = max(self.settings.max_risk_per_trade * 1.5, self.settings.capital * 0.35)
            if params.risk_mode == "aggressive" and margin <= self.settings.capital and stop_risk <= aggressive_limit:
                return True, f"aggressive mode; margin {margin:.0f}, stop risk {stop_risk:.0f}"
            if (
                params.risk_mode == "strict"
                and margin <= self.settings.max_margin_budget
                and stop_risk <= self.settings.max_risk_per_trade
            ):
                return True, f"strict mode; margin {margin:.0f}, stop risk {stop_risk:.0f}"
            return False, f"not tradable: margin {margin:.0f}, stop risk {stop_risk:.0f} exceeds configured budget"

        return check

    def _select_contract(self, spec: InstrumentSpec) -> SelectedContract:
        if self.provider is not None and hasattr(self.provider, "select_trade_contract"):
            return self.provider.select_trade_contract(spec)
        return SelectedContract(spec.symbol, spec.ak_symbol, "continuous fallback")

    def _load_profile(self) -> dict:
        profiles = self.store.read_profiles()
        profile = self.profile
        if profile == "live":
            profile = "walk_forward" if profiles and "walk_forward" in profiles else "safe_winrate"
        profile = "refined_robust" if profile == "robust" else profile
        profile = "walk_forward" if profile == "walkforward" else profile
        if profiles and profile in profiles:
            return profiles[profile]
        champions = self.store.read_champions()
        if champions:
            return champions
        return {}

    def _to_signal(self, symbol: str, selected: SelectedContract, action: StrategyAction, best: dict, rank: int) -> Signal:
        risk = action.reason if action.action == "RISK_BLOCKED" else f"margin checked; contract selection: {selected.reason}"
        news_bias = action.details.get("news_bias", 0.0)
        news = "无明显事件" if abs(news_bias) < 0.05 else f"事件偏置 {news_bias:.2f}"
        return Signal(
            symbol=symbol,
            contract=selected.contract,
            timestamp=action.timestamp,
            action=action.action,
            price=action.price,
            confidence=action.confidence,
            trigger_price=action.price,
            invalid_price=action.stop_price,
            reason=action.reason,
            news_evidence=news,
            risk_check=risk,
            strategy_rank=rank,
            strategy_id=best.get("strategy_id"),
        )

    def _watch_signal(self, symbol: str, spec: InstrumentSpec, champion: dict | None, reason: str) -> Signal:
        return Signal(
            symbol=symbol,
            contract=spec.ak_symbol,
            timestamp=datetime.now(),
            action="WATCH_ONLY",
            price=0.0,
            confidence=0.0,
            trigger_price=None,
            invalid_price=None,
            reason=reason,
            news_evidence="无",
            risk_check="no trade",
            strategy_rank=None,
            strategy_id=(champion or {}).get("best", {}).get("strategy_id"),
        )
