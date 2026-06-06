# qihuo-signal

本项目是一个本地期货信号实验系统：先把行情缓存到本地，再批量回测多组多空价格结构策略，选出不同目标下的策略画像，盘中按 15 分钟轮询并推送 QQ 官方机器人消息。

> 仅用于研究和人工辅助判断，不自动下单，也不构成投资建议。

## 快速开始

```powershell
python -m pip install -e .[data,test]
qihuo init
qihuo fetch-history
qihuo backtest --search --fast --timeframe 15m --timeframe 60m --timeframe 1d --side both --side long --side short --limit-per-symbol 432 --workers 6
qihuo analyze
qihuo poll --once --dry-run
qihuo dashboard
```

如果暂时不安装 AkShare，可以先用 `qihuo fetch-history --sample` 生成本地样本数据，验证回测、分析、轮询和推送链路。

## 核心命令

- `qihuo fetch-history`：拉取 AkShare 行情并写入本地 Parquet/DuckDB。
- `qihuo fetch-history --sample`：生成 deterministic 样本数据，离线验证系统。
- `qihuo update`：增量更新最近行情。
- `qihuo backtest --search`：批量搜索策略参数并保存结果，支持 `--workers` 并行和 `--append` 合并结果。
- `qihuo analyze`：生成回测报告、top CSV、champion 和多套策略画像。
- `qihuo poll`：按配置轮询行情并推送信号，默认 `--profile live`，即每个品种选资金安全范围内胜率最高的策略。
- `qihuo dashboard`：启动本地 FastAPI 看板。
- `qihuo classify-news headlines.csv --symbol RB`：用配置好的 OpenAI-compatible 模型把新闻标题转成本地事件。
- `qihuo fetch-news --source shmet`：抓取 SHMET 快讯并分类为本地事件。
- `qihuo news-poll`：抓取 SHMET 快讯，分析对可交易品种的影响，并通过 QQ 推送。

## 策略画像

- `live`：实盘默认画像，等同于 `safe_winrate`。
- `safe_winrate`：每个品种只选一个“最大回撤不超过本金、胜率最高”的策略，适合小资金盘中提醒。
- `balanced`：最大回撤不超过本金时按收益、样本外表现、胜率和回撤综合排序。
- `capital_safe`：资金安全优先的收益画像。
- `max_return`：非过拟合正收益策略里按净收益排序，不一定适合 8500 本金直接实盘。
- `max_winrate`：非过拟合正收益策略里按胜率排序，不强制回撤小于本金。

## 环境变量

LLM 使用 OpenAI-compatible 接口：

```powershell
$env:LLM_BASE_URL="https://api.openai.com/v1"
$env:LLM_API_KEY="..."
$env:LLM_MODEL="gpt-4.1-mini"
```

也兼容这组变量名：`OPENAI_BASE_URL` / `TEACHER_OPENAI_BASE_URL`、`OPENAI_API_KEY` / `ANTHROPIC_AUTH_TOKEN`、`TEACHER_MODEL` / `ANTHROPIC_MODEL`。

QQ 官方机器人：

```powershell
$env:QQ_BOT_APP_ID="..."
$env:QQ_BOT_APP_SECRET="..."
$env:QQ_BOT_TARGET_ID="..."      # 群 openid 或频道目标 id
$env:QQ_BOT_TARGET_TYPE="group"  # group 或 channel
```

默认 `poll --dry-run` 只打印消息，不调用 QQ API。
