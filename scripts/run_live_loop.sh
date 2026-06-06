#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
if [ -d .venv ]; then
  . .venv/bin/activate
fi

interval_seconds="${QIHUO_LOOP_INTERVAL_SECONDS:-900}"
# Default news digest cadence: 8 hours.
news_interval_seconds="${QIHUO_NEWS_INTERVAL_SECONDS:-28800}"
last_news_at=0

while true; do
  date
  python -m qihuo_signal update || true
  python -m qihuo_signal poll --once || true
  now="$(date +%s)"
  if [ $((now - last_news_at)) -ge "$news_interval_seconds" ]; then
    if python -m qihuo_signal news-poll; then
      last_news_at="$now"
    fi
  fi
  sleep "$interval_seconds"
done
