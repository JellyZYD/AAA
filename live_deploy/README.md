# qihuo live deployment

这个目录是备用部署包，包含源码、配置、本地行情缓存、回测结果和 champion 策略。现在仓库根目录也已经可以直接部署；如果只上传这个目录，也可以按下面方式运行。

## 安装

```bash
bash scripts/install.sh
cp .env.example .env
nano .env
python -m qihuo_signal env-check
python -m qihuo_signal alert-test
```

## 运行

```bash
python -m qihuo_signal poll --once
python -m qihuo_signal news-poll
bash scripts/run_live_loop.sh
```

`run_live_loop.sh` 默认每 15 分钟执行一次：更新行情、检测信号、抓取新闻并通过企业微信推送。新闻消息只显示 3 条重大新闻标题和最多 5 条品种影响。可以用 `QIHUO_LOOP_INTERVAL_SECONDS=300 bash scripts/run_live_loop.sh` 改成 5 分钟一次。
