# qihuo-signal

本项目是一个本地期货信号实验系统：本地缓存行情，批量回测多空价格结构策略，选择实盘候选策略，然后按周期推送人工下单参考信号和新闻影响摘要。

仅用于研究和人工辅助判断，不自动下单，也不构成投资建议。

## 服务器快速部署

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

仓库根目录已经包含运行所需的源码、配置、本地行情缓存、回测结果和 champion 策略。服务器 clone 后只需要安装依赖并填好 `.env` 里的 LLM 与企业微信 webhook。

## 运行频率

- `scripts/run_live_loop.sh` 默认每 15 分钟循环一次：更新行情、检测交易信号。
- 新闻推送默认启动时执行一次，之后每 8 小时执行一次。
- 可以用环境变量修改频率，例如 `QIHUO_LOOP_INTERVAL_SECONDS=300` 表示信号每 5 分钟一次，`QIHUO_NEWS_INTERVAL_SECONDS=14400` 表示新闻每 4 小时一次。
- `python -m qihuo_signal news-poll` 是单次新闻检索和推送，不会自己循环。
- `python -m qihuo_signal poll` 的连续模式也读取 `config.yaml` 里的 `poll_interval_minutes: 15`。

## 常用命令

- `python -m qihuo_signal env-check`：检查环境变量是否完整，不打印密钥。
- `python -m qihuo_signal alert-test`：测试企业微信推送。
- `python -m qihuo_signal poll --once`：更新行情并检测一次实盘信号。
- `python -m qihuo_signal poll --once --dry-run --no-update`：只用本地缓存检测，不推送。
- `python -m qihuo_signal news-poll`：抓取 SHMET 快讯和重大新闻，精简推送“3 条重大新闻标题 + 最多 5 条品种影响”。
- `python -m qihuo_signal dashboard --host 0.0.0.0 --port 8000`：启动本地看板。

## 环境变量

`.env` 示例：

```bash
ALERT_PROVIDER=wecom
WECOM_WEBHOOK_URL=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=replace-me
ALERT_DRY_RUN=false

LLM_BASE_URL=https://example.com/v1
LLM_API_KEY=replace-me
LLM_MODEL=replace-me
```

LLM 也兼容 `OPENAI_BASE_URL` / `TEACHER_OPENAI_BASE_URL`、`OPENAI_API_KEY` / `ANTHROPIC_AUTH_TOKEN`、`TEACHER_MODEL` / `ANTHROPIC_MODEL`。

## 实盘策略

`qihuo poll` 默认使用 `--profile live`，等同于 `safe_winrate`：每个品种只选一个“历史最大回撤不超过本金、胜率最高”的策略。没有通过资金和稳定性过滤的品种只进入观察池，不发开仓信号。

当前高胜率代表：

- CJ 红枣：15m，胜率约 65.0%
- UR 尿素：15m，胜率约 63.6%
- C 玉米：60m，胜率约 60.9%
- RM 菜粕：15m，胜率约 60.0%
- RB 螺纹钢：15m，胜率约 59.1%

## 未来函数审计

- 价格结构信号没有在触发时直接使用未来 K 线。
- 摆动高低点使用 `confirm_index = pivot_index + window`，只有确认窗口结束后才允许触发。
- 突破/假突破策略只使用当前已完成 K 线和此前窗口。
- 新闻事件只在 `event.timestamp <= bar.timestamp` 时参与偏置。
- 回测里的参数选择使用完整历史结果，这属于研究中的参数选择偏差，不是逐根 K 线未来函数；实盘前应定期滚动复核。
