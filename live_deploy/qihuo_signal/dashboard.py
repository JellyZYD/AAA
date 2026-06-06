from __future__ import annotations

import json

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from .config import load_settings
from .storage import LocalStore


settings = load_settings()
store = LocalStore(settings.data_root)
app = FastAPI(title="qihuo-signal")


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    return """
    <!doctype html>
    <html lang="zh-CN">
    <head>
      <meta charset="utf-8" />
      <title>期货信号看板</title>
      <style>
        body { font-family: system-ui, "Microsoft YaHei", sans-serif; margin: 24px; color: #1f2937; }
        table { border-collapse: collapse; width: 100%; margin: 16px 0; font-size: 14px; }
        th, td { border-bottom: 1px solid #e5e7eb; padding: 8px; text-align: left; vertical-align: top; }
        th { background: #f8fafc; }
        code { font-size: 12px; }
      </style>
    </head>
    <body>
      <h1>期货信号看板</h1>
      <h2>Champion</h2>
      <div id="champions"></div>
      <h2>最近信号</h2>
      <div id="signals"></div>
      <script>
      async function load() {
        const champions = await fetch('/api/champions').then(r => r.json());
        document.getElementById('champions').innerHTML = table(Object.entries(champions).map(([symbol, item]) => ({
          symbol, status: item.status, reason: item.reason, strategy: item.best?.strategy_id,
          pnl: item.best?.net_pnl, test: item.best?.test_net_pnl
        })));
        const signals = await fetch('/api/signals').then(r => r.json());
        document.getElementById('signals').innerHTML = table(signals.slice(-50).reverse());
      }
      function table(rows) {
        if (!rows.length) return '<p>暂无数据</p>';
        const keys = Object.keys(rows[0]);
        return '<table><thead><tr>' + keys.map(k => `<th>${k}</th>`).join('') + '</tr></thead><tbody>' +
          rows.map(r => '<tr>' + keys.map(k => `<td>${String(r[k] ?? '')}</td>`).join('') + '</tr>').join('') +
          '</tbody></table>';
      }
      load();
      setInterval(load, 15000);
      </script>
    </body>
    </html>
    """


@app.get("/api/results")
def results():
    df = store.read_backtest_results()
    return json.loads(df.head(200).to_json(orient="records", force_ascii=False, date_format="iso"))


@app.get("/api/champions")
def champions():
    return store.read_champions()


@app.get("/api/signals")
def signals():
    df = store.read_signals()
    return json.loads(df.to_json(orient="records", force_ascii=False, date_format="iso"))

