#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
if [ -d .venv ]; then
  . .venv/bin/activate
fi

while true; do
  date
  python -m qihuo_signal update || true
  python -m qihuo_signal poll --once || true
  python -m qihuo_signal news-poll || true
  sleep "${QIHUO_LOOP_INTERVAL_SECONDS:-900}"
done
