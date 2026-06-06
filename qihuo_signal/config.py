from __future__ import annotations

import os
import shutil
import json
import re
from dataclasses import replace
from pathlib import Path
from typing import Any

import yaml

from .models import AlertSettings, BacktestSettings, InstrumentSpec, LLMSettings, Settings


DEFAULT_INSTRUMENTS: dict[str, InstrumentSpec] = {
    "SP": InstrumentSpec("SP", "纸浆", "SHFE", "SP0", multiplier=10, tick_size=2, margin_rate=0.12),
    "SR": InstrumentSpec("SR", "白糖", "CZCE", "SR0", multiplier=10, tick_size=1, margin_rate=0.10),
    "CJ": InstrumentSpec("CJ", "红枣", "CZCE", "CJ0", multiplier=5, tick_size=5, margin_rate=0.12),
    "UR": InstrumentSpec("UR", "尿素", "CZCE", "UR0", multiplier=20, tick_size=1, margin_rate=0.10),
    "FG": InstrumentSpec("FG", "玻璃", "CZCE", "FG0", multiplier=20, tick_size=1, margin_rate=0.12),
    "C": InstrumentSpec("C", "玉米", "DCE", "C0", multiplier=10, tick_size=1, margin_rate=0.10),
    "RB": InstrumentSpec("RB", "螺纹钢", "SHFE", "RB0", multiplier=10, tick_size=1, margin_rate=0.12),
    "RM": InstrumentSpec("RM", "菜粕", "CZCE", "RM0", multiplier=10, tick_size=1, margin_rate=0.10),
    "HC": InstrumentSpec("HC", "热卷", "SHFE", "HC0", multiplier=10, tick_size=1, margin_rate=0.12),
    "SA": InstrumentSpec("SA", "纯碱", "CZCE", "SA0", multiplier=20, tick_size=1, margin_rate=0.12),
    "CS": InstrumentSpec("CS", "玉米淀粉", "DCE", "CS0", multiplier=10, tick_size=1, margin_rate=0.10),
}


def _as_tuple(value: Any, default: tuple[str, ...]) -> tuple[str, ...]:
    if value is None:
        return default
    if isinstance(value, str):
        return (value,)
    return tuple(str(v) for v in value)


def load_settings(path: str | Path | None = None) -> Settings:
    load_env_file()
    config_path = Path(path or os.getenv("QIHUO_CONFIG", "config.yaml"))
    raw: dict[str, Any] = {}
    if config_path.exists():
        raw = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}

    defaults = Settings(instruments=DEFAULT_INSTRUMENTS)
    backtest_raw = raw.get("backtest", {}) or {}
    llm_raw = raw.get("llm", {}) or {}
    alert_raw = raw.get("alert", {}) or {}

    llm = LLMSettings(
        provider=str(llm_raw.get("provider", defaults.llm.provider)),
        base_url=_normalize_llm_base_url(
            _env_first(
                "LLM_BASE_URL",
                "OPENAI_BASE_URL",
                "TEACHER_OPENAI_BASE_URL",
                "ANTHROPIC_BASE_URL",
                default=llm_raw.get("base_url"),
            )
        ),
        api_key=_env_first("LLM_API_KEY", "OPENAI_API_KEY", "ANTHROPIC_AUTH_TOKEN", default=llm_raw.get("api_key")),
        model=_env_first("LLM_MODEL", "TEACHER_MODEL", "ANTHROPIC_MODEL", default=llm_raw.get("model")),
        timeout_seconds=float(llm_raw.get("timeout_seconds", defaults.llm.timeout_seconds)),
    )
    alert = AlertSettings(
        provider=str(os.getenv("ALERT_PROVIDER", alert_raw.get("provider", defaults.alert.provider))),
        dry_run=str(
            _env_first(
                "ALERT_DRY_RUN",
                "WECOM_DRY_RUN",
                "QQ_BOT_DRY_RUN",
                default=str(alert_raw.get("dry_run", defaults.alert.dry_run)),
            )
        ).lower()
        in {"1", "true", "yes", "on"},
        wecom_webhook_url=_env_first(
            "WECOM_WEBHOOK_URL",
            "WECHAT_WORK_WEBHOOK_URL",
            "QYWX_WEBHOOK_URL",
            default=alert_raw.get("wecom_webhook_url"),
        ),
        qq_app_id=os.getenv("QQ_BOT_APP_ID", alert_raw.get("qq_app_id")),
        qq_app_secret=os.getenv("QQ_BOT_APP_SECRET", alert_raw.get("qq_app_secret")),
        qq_target_id=os.getenv("QQ_BOT_TARGET_ID", alert_raw.get("qq_target_id")),
        qq_target_type=os.getenv("QQ_BOT_TARGET_TYPE", alert_raw.get("qq_target_type", defaults.alert.qq_target_type)),
        qq_api_base=os.getenv("QQ_BOT_API_BASE", alert_raw.get("qq_api_base", defaults.alert.qq_api_base)),
        qq_token_base=os.getenv("QQ_BOT_TOKEN_BASE", alert_raw.get("qq_token_base", defaults.alert.qq_token_base)),
    )

    symbols = _as_tuple(raw.get("symbols"), defaults.symbols)
    instruments = {k: v for k, v in DEFAULT_INSTRUMENTS.items() if k in symbols}
    custom_instruments = raw.get("instruments", {}) or {}
    for symbol, spec_raw in custom_instruments.items():
        base = instruments.get(symbol, DEFAULT_INSTRUMENTS.get(symbol))
        if base is None:
            continue
        instruments[symbol] = replace(
            base,
            multiplier=float(spec_raw.get("multiplier", base.multiplier)),
            tick_size=float(spec_raw.get("tick_size", base.tick_size)),
            margin_rate=float(spec_raw.get("margin_rate", base.margin_rate)),
            fee_rate=float(spec_raw.get("fee_rate", base.fee_rate)),
            min_volume=int(spec_raw.get("min_volume", base.min_volume)),
        )

    return Settings(
        capital=float(raw.get("capital", defaults.capital)),
        max_margin_budget=float(raw.get("max_margin_budget", defaults.max_margin_budget)),
        max_risk_per_trade=float(raw.get("max_risk_per_trade", defaults.max_risk_per_trade)),
        poll_interval_minutes=int(raw.get("poll_interval_minutes", defaults.poll_interval_minutes)),
        data_root=str(raw.get("data_root", defaults.data_root)),
        reports_root=str(raw.get("reports_root", defaults.reports_root)),
        timeframes=_as_tuple(raw.get("timeframes"), defaults.timeframes),
        symbols=symbols,
        instruments=instruments,
        backtest=BacktestSettings(
            objective=str(backtest_raw.get("objective", defaults.backtest.objective)),
            train_ratio=float(backtest_raw.get("train_ratio", defaults.backtest.train_ratio)),
            slippage_ticks=int(backtest_raw.get("slippage_ticks", defaults.backtest.slippage_ticks)),
            min_trades_for_champion=int(
                backtest_raw.get("min_trades_for_champion", defaults.backtest.min_trades_for_champion)
            ),
        ),
        llm=llm,
        alert=alert,
    )


def write_default_config(path: str | Path = "config.yaml", overwrite: bool = False) -> Path:
    target = Path(path)
    if target.exists() and not overwrite:
        return target
    source = Path(__file__).resolve().parent.parent / "config.example.yaml"
    shutil.copyfile(source, target)
    return target


def _env_first(*names: str, default: Any = None) -> Any:
    for name in names:
        value = os.getenv(name)
        if value:
            return value
    return default


def load_env_file(path: str | Path = ".env", override: bool = False) -> None:
    env_path = Path(path)
    if not env_path.exists():
        return
    try:
        text = env_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = env_path.read_text(encoding="utf-8-sig")

    _load_jsonish_env(text, override=override)
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or line in {"{", "}", "},"}:
            continue
        if line.startswith("export "):
            line = line[7:].strip()
        match = re.match(r'^"?([A-Za-z_][A-Za-z0-9_]*|AppID|AppSecret)"?\s*[:=]\s*(.+?)\s*,?$', line)
        if not match:
            continue
        key, value = match.group(1), match.group(2).strip()
        value = _strip_env_value(value)
        mapped_key = _map_env_key(key)
        if override or mapped_key not in os.environ:
            os.environ[mapped_key] = value


def _load_jsonish_env(text: str, override: bool) -> None:
    stripped = text.strip()
    if not stripped.startswith("{"):
        return
    try:
        data = json.loads(stripped)
    except Exception:
        return
    env_data = data.get("env", data) if isinstance(data, dict) else {}
    if not isinstance(env_data, dict):
        return
    for key, value in env_data.items():
        mapped_key = _map_env_key(str(key))
        if value is not None and (override or mapped_key not in os.environ):
            os.environ[mapped_key] = str(value)


def _strip_env_value(value: str) -> str:
    value = value.strip()
    if value.endswith(","):
        value = value[:-1].strip()
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        value = value[1:-1]
    return value


def _map_env_key(key: str) -> str:
    mapping = {
        "AppID": "QQ_BOT_APP_ID",
        "AppSecret": "QQ_BOT_APP_SECRET",
        "QQ_APP_ID": "QQ_BOT_APP_ID",
        "QQ_APP_SECRET": "QQ_BOT_APP_SECRET",
        "QQ_GROUP_OPENID": "QQ_BOT_TARGET_ID",
        "QQ_GROUP_ID": "QQ_BOT_TARGET_ID",
        "QQ_CHANNEL_ID": "QQ_BOT_TARGET_ID",
        "WECHAT_WORK_WEBHOOK": "WECOM_WEBHOOK_URL",
        "WECHAT_WORK_WEBHOOK_URL": "WECOM_WEBHOOK_URL",
        "QYWX_WEBHOOK_URL": "WECOM_WEBHOOK_URL",
    }
    return mapping.get(key, key)


def _normalize_llm_base_url(value: Any) -> Any:
    if not value:
        return value
    text = str(value).rstrip("/")
    if text.endswith("/anthropic"):
        return text[: -len("/anthropic")] + "/v1"
    return text
