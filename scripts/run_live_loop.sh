#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
if [ -d .venv ]; then
  . .venv/bin/activate
fi

interval_seconds="${QIHUO_LOOP_INTERVAL_SECONDS:-900}"

while true; do
  date
  python -m qihuo_signal update || true
  python -m qihuo_signal poll --once || true
  python -m qihuo_signal news-poll || true
  sleep "$interval_seconds"
done
