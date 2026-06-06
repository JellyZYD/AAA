from __future__ import annotations

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Iterable

import httpx
import pandas as pd

from .models import LLMSettings, NewsEvent


COMMODITY_KEYWORDS: dict[str, dict[str, list[str]]] = {
    "SP": {"bullish": ["限产", "罢工", "进口减少", "库存下降"], "bearish": ["累库", "需求疲弱", "进口增加"]},
    "SR": {"bullish": ["减产", "干旱", "霜冻", "出口限制"], "bearish": ["增产", "进口增加", "抛储"]},
    "CJ": {"bullish": ["减产", "灾害", "库存低"], "bearish": ["丰产", "消费弱"]},
    "UR": {"bullish": ["装置检修", "出口增加", "农需启动"], "bearish": ["复产", "库存高", "需求弱"]},
    "FG": {"bullish": ["冷修", "地产刺激", "去库"], "bearish": ["复产", "累库", "地产弱"]},
    "C": {"bullish": ["减产", "天气", "收储"], "bearish": ["丰产", "进口", "拍卖"]},
    "RB": {"bullish": ["限产", "基建", "地产刺激"], "bearish": ["减产不及", "需求弱", "库存高"]},
    "RM": {"bullish": ["菜籽减产", "进口受阻", "压榨下降"], "bearish": ["进口增加", "库存高"]},
    "HC": {"bullish": ["制造业回暖", "限产"], "bearish": ["出口下降", "库存高"]},
    "SA": {"bullish": ["装置检修", "光伏需求", "去库"], "bearish": ["投产", "累库", "需求弱"]},
    "CS": {"bullish": ["玉米上涨", "开机下降"], "bearish": ["玉米下跌", "库存高"]},
}

PRODUCT_TERMS: dict[str, list[str]] = {
    "SP": ["纸浆", "漂针浆", "木浆", "浆价"],
    "SR": ["白糖", "糖价", "食糖", "原糖"],
    "CJ": ["红枣", "枣"],
    "UR": ["尿素", "氮肥"],
    "FG": ["玻璃", "浮法", "玻璃厂"],
    "C": ["玉米"],
    "RB": ["螺纹", "螺纹钢", "钢筋"],
    "RM": ["菜粕", "菜籽粕"],
    "HC": ["热卷", "热轧"],
    "SA": ["纯碱", "碱厂"],
    "CS": ["玉米淀粉", "淀粉"],
}


class KeywordEventAnalyzer:
    def analyze(self, symbol: str, headlines: Iterable[str], source: str = "keyword") -> list[NewsEvent]:
        now = datetime.now()
        rules = COMMODITY_KEYWORDS.get(symbol, {"bullish": [], "bearish": []})
        events: list[NewsEvent] = []
        for title in headlines:
            if not _mentions_product(symbol, title):
                continue
            score = 0
            direction = "neutral"
            if any(word in title for word in rules.get("bullish", [])):
                score += 1
                direction = "bullish"
            if any(word in title for word in rules.get("bearish", [])):
                score -= 1
                direction = "bearish" if score < 0 else direction
            if score == 0:
                continue
            events.append(
                NewsEvent(
                    symbol=symbol,
                    timestamp=now,
                    title=title,
                    source=source,
                    direction=direction,  # type: ignore[arg-type]
                    confidence=min(0.75, 0.45 + abs(score) * 0.15),
                    horizon_days=10,
                    impact_score=max(-1.0, min(1.0, score * 0.35)),
                    similar_events="keyword rule match",
                )
            )
        return events


class LLMEventAnalyzer:
    def __init__(self, settings: LLMSettings) -> None:
        self.settings = settings

    def analyze(self, symbol: str, headlines: Iterable[str]) -> list[NewsEvent]:
        titles = [title.strip() for title in headlines if title.strip()]
        if not titles:
            return []
        if not self.settings.base_url or not self.settings.api_key or not self.settings.model:
            return KeywordEventAnalyzer().analyze(symbol, titles, source="keyword-fallback")
        prompt = {
            "symbol": symbol,
            "task": "Analyze Chinese commodity futures news for trend impact. Return JSON only.",
            "schema": [
                {
                    "title": "original headline",
                    "direction": "bullish|bearish|neutral",
                    "confidence": "0..1",
                    "horizon_days": "integer",
                    "impact_score": "-1..1",
                    "similar_events": "short Chinese explanation",
                    "reason": "short Chinese explanation",
                }
            ],
            "headlines": titles,
        }
        url = self.settings.base_url.rstrip("/") + "/chat/completions"
        payload = {
            "model": self.settings.model,
            "messages": [
                {"role": "system", "content": "You are a cautious commodity futures event analyst. Return valid JSON only."},
                {"role": "user", "content": json.dumps(prompt, ensure_ascii=False)},
            ],
            "temperature": 0.1,
        }
        try:
            with httpx.Client(timeout=self.settings.timeout_seconds) as client:
                response = client.post(url, headers={"Authorization": f"Bearer {self.settings.api_key}"}, json=payload)
                response.raise_for_status()
                content = response.json()["choices"][0]["message"]["content"]
        except Exception:
            return KeywordEventAnalyzer().analyze(symbol, titles, source="keyword-fallback")
        return self._parse(symbol, titles, content)

    def analyze_many(self, symbols: Iterable[str], headlines: Iterable[str]) -> list[NewsEvent]:
        titles = [title.strip() for title in headlines if title.strip()]
        symbols_list = [symbol for symbol in symbols]
        if not titles or not symbols_list:
            return []
        if not self.settings.base_url or not self.settings.api_key or not self.settings.model:
            events: list[NewsEvent] = []
            keyword = KeywordEventAnalyzer()
            for symbol in symbols_list:
                events.extend(keyword.analyze(symbol, titles, source="keyword-fallback"))
            return events
        prompt = {
            "symbols": symbols_list,
            "task": "Analyze these Chinese futures/commodity headlines. Return only events that materially affect one configured symbol.",
            "schema": [
                {
                    "symbol": "one of symbols",
                    "title": "original headline",
                    "direction": "bullish|bearish|neutral",
                    "confidence": "0..1",
                    "horizon_days": "integer",
                    "impact_score": "-1..1",
                    "similar_events": "short Chinese explanation",
                    "reason": "short Chinese explanation",
                }
            ],
            "headlines": titles,
        }
        url = self.settings.base_url.rstrip("/") + "/chat/completions"
        payload = {
            "model": self.settings.model,
            "messages": [
                {"role": "system", "content": "You are a cautious Chinese commodity futures event analyst. Return valid JSON only."},
                {"role": "user", "content": json.dumps(prompt, ensure_ascii=False)},
            ],
            "temperature": 0.1,
        }
        try:
            with httpx.Client(timeout=min(self.settings.timeout_seconds, 20.0)) as client:
                response = client.post(url, headers={"Authorization": f"Bearer {self.settings.api_key}"}, json=payload)
                response.raise_for_status()
                content = response.json()["choices"][0]["message"]["content"]
            return self._parse_many(symbols_list, titles, content)
        except Exception:
            events = []
            keyword = KeywordEventAnalyzer()
            for symbol in symbols_list:
                events.extend(keyword.analyze(symbol, titles, source="keyword-fallback"))
            return events

    def _parse(self, symbol: str, titles: list[str], content: str) -> list[NewsEvent]:
        try:
            parsed = json.loads(_extract_json(content))
            if isinstance(parsed, dict):
                parsed = parsed.get("events", parsed.get("data", []))
            if not isinstance(parsed, list):
                return KeywordEventAnalyzer().analyze(symbol, titles, source="keyword-fallback")
        except Exception:
            return KeywordEventAnalyzer().analyze(symbol, titles, source="keyword-fallback")
        now = datetime.now()
        events: list[NewsEvent] = []
        for item in parsed:
            direction = str(item.get("direction", "neutral")).lower()
            if direction not in {"bullish", "bearish", "neutral"}:
                direction = "neutral"
            events.append(
                NewsEvent(
                    symbol=symbol,
                    timestamp=now,
                    title=str(item.get("title", ""))[:300],
                    source="llm",
                    direction=direction,  # type: ignore[arg-type]
                    confidence=float(_clamp(item.get("confidence", 0), 0, 1)),
                    horizon_days=int(_clamp(item.get("horizon_days", 10), 1, 90)),
                    impact_score=float(_clamp(item.get("impact_score", 0), -1, 1)),
                    similar_events=str(item.get("similar_events", ""))[:500],
                    raw=dict(item),
                )
            )
        return events

    def _parse_many(self, symbols: list[str], titles: list[str], content: str) -> list[NewsEvent]:
        try:
            parsed = json.loads(_extract_json(content))
            if isinstance(parsed, dict):
                parsed = parsed.get("events", parsed.get("data", []))
            if not isinstance(parsed, list):
                return []
        except Exception:
            return []
        now = datetime.now()
        allowed = set(symbols)
        events: list[NewsEvent] = []
        for item in parsed:
            symbol = str(item.get("symbol", "")).upper()
            title = str(item.get("title", ""))[:300]
            if symbol not in allowed or not title:
                continue
            direction = str(item.get("direction", "neutral")).lower()
            if direction not in {"bullish", "bearish", "neutral"}:
                direction = "neutral"
            events.append(
                NewsEvent(
                    symbol=symbol,
                    timestamp=now,
                    title=title,
                    source="llm",
                    direction=direction,  # type: ignore[arg-type]
                    confidence=float(_clamp(item.get("confidence", 0), 0, 1)),
                    horizon_days=int(_clamp(item.get("horizon_days", 10), 1, 90)),
                    impact_score=float(_clamp(item.get("impact_score", 0), -1, 1)),
                    similar_events=str(item.get("similar_events", ""))[:500],
                    raw=dict(item),
                )
            )
        return events


def load_manual_events(path: str | Path) -> list[NewsEvent]:
    event_path = Path(path)
    if not event_path.exists():
        return []
    df = pd.read_csv(event_path)
    events: list[NewsEvent] = []
    for _, row in df.iterrows():
        events.append(
            NewsEvent(
                symbol=str(row["symbol"]),
                timestamp=pd.to_datetime(row["timestamp"]).to_pydatetime(),
                title=str(row.get("title", "")),
                source=str(row.get("source", "manual")),
                direction=str(row.get("direction", "neutral")),  # type: ignore[arg-type]
                confidence=float(row.get("confidence", 0.5)),
                horizon_days=int(row.get("horizon_days", 10)),
                impact_score=float(row.get("impact_score", 0.0)),
                similar_events=str(row.get("similar_events", "")),
            )
        )
    return events


def fetch_shmet_headlines(symbol: str = "全部") -> pd.DataFrame:
    try:
        import akshare as ak
    except Exception as exc:
        raise RuntimeError("AkShare is required for SHMET news. Install optional data dependencies.") from exc
    df = ak.futures_news_shmet(symbol=symbol)
    if df.empty:
        return pd.DataFrame(columns=["timestamp", "title", "source"])
    out = df.rename(columns={"发布时间": "timestamp", "内容": "title"}).copy()
    out["timestamp"] = pd.to_datetime(out["timestamp"])
    out["source"] = "shmet"
    out["url"] = ""
    return out[["timestamp", "title", "source"]]


def fetch_major_headlines(limit: int = 30) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    try:
        import akshare as ak
    except Exception:
        return pd.DataFrame(columns=["timestamp", "title", "source", "url"])

    now = datetime.now()
    for day_offset in (0, 1):
        date_text = (now - timedelta(days=day_offset)).strftime("%Y%m%d")
        try:
            cctv = ak.news_cctv(date=date_text)
            if not cctv.empty:
                df = cctv.rename(columns={"date": "timestamp"}).copy()
                df["title"] = df["title"].astype(str) + " " + df.get("content", "").astype(str).str.slice(0, 160)
                df["source"] = "cctv"
                df["url"] = ""
                frames.append(df[["timestamp", "title", "source", "url"]])
                break
        except Exception:
            pass

    try:
        cx = ak.stock_news_main_cx()
        if not cx.empty:
            df = cx.rename(columns={"summary": "title"}).copy()
            df["timestamp"] = now
            df["source"] = "caixin"
            if "url" not in df.columns:
                df["url"] = ""
            frames.append(df[["timestamp", "title", "source", "url"]])
    except Exception:
        pass

    if not frames:
        return pd.DataFrame(columns=["timestamp", "title", "source", "url"])
    out = pd.concat(frames, ignore_index=True)
    out["timestamp"] = pd.to_datetime(out["timestamp"], errors="coerce").fillna(pd.Timestamp(now))
    out["title"] = out["title"].astype(str).str.replace(r"\s+", " ", regex=True).str.strip()
    out = out[out["title"].str.len() > 0]
    out = out.drop_duplicates(subset=["title"]).head(limit).reset_index(drop=True)
    return out


def classify_headline_frame(df: pd.DataFrame, symbols: Iterable[str], analyzer: LLMEventAnalyzer) -> list[NewsEvent]:
    events: list[NewsEvent] = []
    if df.empty:
        return events
    classified = analyzer.analyze_many(symbols, df["title"].astype(str).tolist())
    for event in classified:
        if event.direction == "neutral" or abs(event.impact_score) < 0.05:
            continue
        matched = _match_headline_row(df, event.title)
        timestamp = pd.to_datetime(matched["timestamp"]).to_pydatetime() if matched is not None else event.timestamp
        source = str(matched.get("source", event.source)) if matched is not None else event.source
        events.append(NewsEvent(**{**event.__dict__, "timestamp": timestamp, "source": source}))
    return events


def _match_headline_row(df: pd.DataFrame, title: str):
    if df.empty:
        return None
    for _, row in df.iterrows():
        raw_title = str(row["title"])
        if title == raw_title or title in raw_title or raw_title in title:
            return row
    return None


def event_bias(events: pd.DataFrame, symbol: str, timestamp: pd.Timestamp) -> float:
    if events.empty:
        return 0.0
    df = events[events["symbol"] == symbol].copy()
    if df.empty:
        return 0.0
    event_ts = pd.to_datetime(df["timestamp"], errors="coerce")
    if getattr(event_ts.dt, "tz", None) is not None:
        event_ts = event_ts.dt.tz_localize(None)
    df["timestamp"] = event_ts
    ts = pd.Timestamp(timestamp)
    if ts.tzinfo is not None:
        ts = ts.tz_convert(None)
    active = df[(df["timestamp"] <= ts) & (df["timestamp"] >= ts - pd.Timedelta(days=90))]
    if active.empty:
        return 0.0
    score = 0.0
    for _, row in active.tail(8).iterrows():
        age_days = max(0.0, (ts - row["timestamp"]).total_seconds() / 86400)
        horizon = max(1.0, float(row.get("horizon_days", 10)))
        if age_days > horizon:
            continue
        decay = 1 - age_days / horizon
        direction = row.get("direction", "neutral")
        sign = 1 if direction == "bullish" else -1 if direction == "bearish" else 0
        score += sign * float(row.get("confidence", 0.0)) * float(row.get("impact_score", 0.0)) * decay
    return max(-1.0, min(1.0, score))


def _extract_json(text: str) -> str:
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = stripped.strip("`")
        if stripped.startswith("json"):
            stripped = stripped[4:]
    start = stripped.find("[")
    end = stripped.rfind("]")
    if start >= 0 and end > start:
        return stripped[start : end + 1]
    return stripped


def _clamp(value: Any, low: float, high: float) -> float:
    try:
        number = float(value)
    except Exception:
        number = low
    return max(low, min(high, number))


def _mentions_product(symbol: str, title: str) -> bool:
    return any(term in title for term in PRODUCT_TERMS.get(symbol, [symbol]))
