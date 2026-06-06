# 部署说明

优先推荐直接 clone 仓库根目录部署：

```bash
git clone https://github.com/JellyZYD/AAA.git
cd AAA
bash scripts/install.sh
cp .env.example .env
nano .env
python -m qihuo_signal env-check
python -m qihuo_signal alert-test
bash scripts/run_live_loop.sh
```

如果使用 `live_deploy` 子目录，命令相同，只是先 `cd live_deploy`。

## `.env`

必须至少配置：

```bash
ALERT_PROVIDER=wecom
WECOM_WEBHOOK_URL=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=replace-me
ALERT_DRY_RUN=false

LLM_BASE_URL=https://example.com/v1
LLM_API_KEY=replace-me
LLM_MODEL=replace-me
```

## 频率

- `python -m qihuo_signal news-poll` 是单次新闻检索。
- `scripts/run_live_loop.sh` 默认每 15 分钟跑一次新闻检索和实盘信号。
- 新闻推送默认只显示 3 条重大新闻标题和最多 5 条品种影响。
- 修改频率：`QIHUO_LOOP_INTERVAL_SECONDS=300 bash scripts/run_live_loop.sh`。

## 默认实盘策略

`qihuo poll` 默认使用 `--profile live`，等同于 `safe_winrate`：每个品种只选一个“历史最大回撤不超过本金、胜率最高”的策略。

## 未来函数审计

- 价格结构信号没有在触发时直接使用未来 K 线。
- 摆动高低点使用 `confirm_index = pivot_index + window`，只有确认窗口结束后才允许触发。
- 突破/假突破策略只使用当前已完成 K 线和此前窗口。
- 新闻事件只在 `event.timestamp <= bar.timestamp` 时参与偏置。
- 回测参数选择使用完整历史结果，属于研究中的参数选择偏差，不是逐根 K 线未来函数。
