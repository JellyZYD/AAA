# qihuo live deployment

这个目录是实盘信号部署包，包含运行所需源码、配置、`.env`、本地行情缓存、策略画像和报告。

## 1. 安装

Linux 云服务器：

```bash
cd live_deploy
bash scripts/install.sh
```

Windows 本地：

```powershell
cd live_deploy
.\scripts\install.ps1
```

## 2. 检查配置

```bash
python -m qihuo_signal env-check
```

必须至少具备：

- LLM：`LLM_BASE_URL`/`OPENAI_BASE_URL`/`ANTHROPIC_BASE_URL`，`LLM_API_KEY`/`ANTHROPIC_AUTH_TOKEN`，`LLM_MODEL`/`ANTHROPIC_MODEL`
- 企业微信：`ALERT_PROVIDER=wecom`，`WECOM_WEBHOOK_URL=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=...`

## 3. 实盘命令

只检测信号，不推送：

```bash
python -m qihuo_signal poll --once --dry-run
```

检测信号并推送 QQ：

```bash
python -m qihuo_signal poll --once
```

抓取新闻、分析对可交易品种的影响并推送 QQ：

```bash
python -m qihuo_signal news-poll
```

测试企业微信推送：

```bash
python -m qihuo_signal alert-test
```

常驻循环：

```bash
bash scripts/run_live_loop.sh
```

## 4. 默认实盘策略

`qihuo poll` 默认使用 `--profile live`，等同于 `safe_winrate`：每个品种只选一个“历史最大回撤不超过本金、胜率最高”的策略。

当前高胜率代表：

- CJ 红枣：15m，胜率约 65.0%
- UR 尿素：15m，胜率约 63.6%
- C 玉米：60m，胜率约 60.9%
- RM 菜粕：15m，胜率约 60.0%
- RB 螺纹钢：15m，胜率约 59.1%

## 5. 未来函数审计

- 价格结构信号没有在触发时直接使用未来 K 线。
- 摆动高低点使用 `confirm_index = pivot_index + window`，只有确认窗口结束后才允许触发。
- 突破/假突破策略只使用当前已完成 K 线和此前窗口。
- 新闻事件只在 `event.timestamp <= bar.timestamp` 时参与偏置。
- 回测里的参数选择使用完整历史结果，这属于研究中的参数选择偏差，不是逐根 K 线未来函数；实盘前应定期滚动复核。
- 回测成交假设是信号 K 线收盘价附近成交；实盘人工执行会有滑点，已经在回测中加入 tick 滑点，但仍需要保守看待。
