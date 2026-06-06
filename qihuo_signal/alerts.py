from __future__ import annotations

import time
from dataclasses import dataclass

import httpx

import pandas as pd

from .models import AlertSettings, Signal
from .models import NewsEvent


class AlertSender:
    def send(self, text: str) -> None:
        raise NotImplementedError


class ConsoleAlertSender(AlertSender):
    def send(self, text: str) -> None:
        print(text)


@dataclass
class WeComWebhookAlertSender(AlertSender):
    settings: AlertSettings

    def send(self, text: str) -> None:
        if self.settings.dry_run:
            print(text)
            return
        if not self.settings.wecom_webhook_url:
            raise RuntimeError("WeCom webhook is missing. Set WECOM_WEBHOOK_URL in .env.")
        payload = {"msgtype": "text", "text": {"content": text[:3500]}}
        with httpx.Client(timeout=20) as client:
            response = client.post(self.settings.wecom_webhook_url, json=payload)
            response.raise_for_status()
            data = response.json()
        if data.get("errcode") not in (0, None):
            raise RuntimeError(f"WeCom webhook send failed: {data}")


@dataclass
class QQOfficialAlertSender(AlertSender):
    settings: AlertSettings
    _token: str | None = None
    _token_expire_at: float = 0.0

    def send(self, text: str) -> None:
        if self.settings.dry_run:
            print(text)
            return
        if not self.settings.qq_app_id or not self.settings.qq_app_secret or not self.settings.qq_target_id:
            raise RuntimeError("QQ bot settings are incomplete. Set QQ_BOT_APP_ID, QQ_BOT_APP_SECRET, QQ_BOT_TARGET_ID.")
        token = self._access_token()
        headers = {"Authorization": f"QQBot {token}", "Content-Type": "application/json"}
        if self.settings.qq_target_type == "channel":
            url = f"{self.settings.qq_api_base.rstrip('/')}/channels/{self.settings.qq_target_id}/messages"
            payload = {"content": text}
        else:
            url = f"{self.settings.qq_api_base.rstrip('/')}/v2/groups/{self.settings.qq_target_id}/messages"
            payload = {"content": text, "msg_type": 0, "msg_seq": int(time.time())}
        with httpx.Client(timeout=20) as client:
            response = client.post(url, headers=headers, json=payload)
            response.raise_for_status()

    def _access_token(self) -> str:
        now = time.time()
        if self._token and now < self._token_expire_at - 60:
            return self._token
        url = f"{self.settings.qq_token_base.rstrip('/')}/app/getAppAccessToken"
        payload = {"appId": self.settings.qq_app_id, "clientSecret": self.settings.qq_app_secret}
        with httpx.Client(timeout=20) as client:
            response = client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
        token = data.get("access_token") or data.get("accessToken")
        if not token:
            raise RuntimeError(f"QQ token response missing access token: {data}")
        expires = int(data.get("expires_in") or data.get("expiresIn") or 3600)
        self._token = token
        self._token_expire_at = now + expires
        return token


def build_alert_sender(settings: AlertSettings, dry_run: bool | None = None) -> AlertSender:
    if dry_run is not None:
        settings = AlertSettings(**{**settings.__dict__, "dry_run": dry_run})
    if settings.provider in {"wecom", "wechat_work", "qywx"}:
        return WeComWebhookAlertSender(settings)
    if settings.provider == "qq_official":
        return QQOfficialAlertSender(settings)
    return ConsoleAlertSender()


def format_signal(signal: Signal) -> str:
    return (
        f"期货信号 {signal.action}\n"
        f"品种/合约: {signal.symbol} {signal.contract}\n"
        f"时间: {signal.timestamp:%Y-%m-%d %H:%M}\n"
        f"价格: {signal.price:.2f}\n"
        f"触发/失效: {_fmt(signal.trigger_price)} / {_fmt(signal.invalid_price)}\n"
        f"置信度: {signal.confidence:.2f}\n"
        f"理由: {signal.reason}\n"
        f"新闻: {signal.news_evidence or '无'}\n"
        f"风险: {signal.risk_check}\n"
        f"策略: {signal.strategy_rank or '-'} {signal.strategy_id or '-'}"
    )


def format_news_events(events: list[NewsEvent], title: str = "期货新闻影响") -> str:
    if not events:
        return f"{title}\n当前没有识别到对可交易品种的强相关事件。"
    lines = [title, f"识别事件数: {len(events)}"]
    for event in events[:20]:
        direction = {"bullish": "利多", "bearish": "利空", "neutral": "中性"}.get(event.direction, event.direction)
        lines.extend(
            [
                "",
                f"{event.symbol} {direction} 置信度 {event.confidence:.2f} 影响 {event.impact_score:.2f}",
                f"标题: {event.title[:180]}",
                f"周期: 约 {event.horizon_days} 天",
                f"相似/理由: {event.similar_events[:180] or event.raw.get('reason', '')}",
            ]
        )
    if len(events) > 20:
        lines.append(f"\n其余 {len(events) - 20} 条已入库。")
    return "\n".join(lines)


def format_news_digest(events: list[NewsEvent], major_headlines: pd.DataFrame, title: str = "期货实时新闻") -> str:
    lines = [title]
    if not major_headlines.empty:
        lines.append("\n重大新闻摘要:")
        for _, row in major_headlines.head(8).iterrows():
            source = str(row.get("source", "news"))
            headline = str(row.get("title", ""))[:180]
            lines.append(f"- [{source}] {headline}")
    else:
        lines.append("\n重大新闻摘要: 暂无可用新闻源。")

    if events:
        lines.append("\n对可交易品种的影响:")
        for event in events[:20]:
            direction = {"bullish": "利多", "bearish": "利空", "neutral": "中性"}.get(event.direction, event.direction)
            reason = event.similar_events[:160] or str(event.raw.get("reason", ""))[:160]
            lines.append(
                f"- {event.symbol} {direction} 置信度 {event.confidence:.2f} 影响 {event.impact_score:.2f}: "
                f"{event.title[:120]} | {reason}"
            )
    else:
        lines.append("\n对可交易品种的影响: 当前没有识别到强相关事件。")
    return "\n".join(lines)


def _fmt(value: float | None) -> str:
    return "-" if value is None else f"{value:.2f}"
