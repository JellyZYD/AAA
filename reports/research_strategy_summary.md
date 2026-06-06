# 策略研究与本地回测进展

生成时间：2026-06-06

## 外部依据

- Time-series momentum：Moskowitz、Ooi、Pedersen 在国际期货中系统研究了时间序列动量，核心思想是用资产自身过去收益判断方向，并常配合波动率标准化。
  - https://w4.stern.nyu.edu/facdir/lpederse/papers/TimeSeriesMomentum.pdf
- 长期趋势跟踪证据：Hurst、Ooi、Pedersen 的百年趋势跟踪研究显示，跨资产趋势跟踪在长历史、多宏观环境中有正收益和分散化价值。
  - https://research.cbs.dk/en/publications/a-century-of-evidence-on-trend-following-investing/
- Donchian/Turtle 类通道突破：商品期货趋势系统常用 Donchian 通道突破、ATR 止损和通道/跟踪止盈来捕捉大趋势。
  - https://www.turtelli.com/insider-knowledge/turtle-trading-for-beginners/what-is-the-best-turtle-trading-strategy

## 已实现候选

- `donchian_atr`：用前 N 根 K 线高低点做 Donchian 通道，突破开仓，ATR 倍数初始止损并跟踪止损，短通道/最长持仓退出。
- `tsmom_vol`：用过去收益除以同窗口波动率得到趋势强度分数，超过阈值开多，低于负阈值开空，ATR 跟踪止损，动量归零或最长持仓退出。

两者都只使用当前已完成 K 线和此前窗口，没有逐根 K 线未来函数。

## 当前本地回测规模

- 回测结果表：约 2.38 万条策略结果。
- 新增策略覆盖：
  - `donchian_atr`：约 6920 条。
  - `tsmom_vol`：约 2640 条。
- 已跑全品种轻量搜索；并对 SA、HC、FG 等日线 Donchian/ATR 做了部分加深搜索。

## 新增策略当前领先结果

| 品种 | 策略 | 周期 | 净收益 | 胜率 | 利润因子 | 交易数 | 最大回撤 | 样本外净收益 |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| SA 纯碱 | Donchian/ATR | 1d | 79454 | 54.1% | 2.93 | 37 | -25604 | 4609 |
| HC 热卷 | Donchian/ATR | 1d | 44364 | 50.0% | 1.73 | 82 | -16856 | 15849 |
| FG 玻璃 | Donchian/ATR | 1d | 47396 | 44.1% | 1.92 | 93 | -13481 | 6622 |
| RB 螺纹钢 | TSMOM/Vol | 1d | 49329 | 44.2% | 1.69 | 199 | -14472 | 2792 |
| SR 白糖 | TSMOM/Vol | 1d | 39703 | 41.7% | 2.19 | 72 | -8039 | 1534 |

## 小资金实盘判断

按总收益排序，SA 日线 Donchian/ATR 目前最强，但最大回撤超过 2.5 万，不适合 8500 本金直接按“冠军收益”实盘。

当前更适合实盘信号的仍应使用 `safe_winrate` 画像：它会过滤大回撤，按每个品种的资金安全范围内高胜率策略发信号。新增策略已经进入该画像：

- RM：Donchian/ATR 30m，胜率约 66.7%，最大回撤约 -819。
- HC：Donchian/ATR 1d，胜率约 69.0%，最大回撤约 -3500。
- SA：Donchian/ATR 60m，胜率约 68.2%，最大回撤约 -1534。
- SP/SR/FG/CS：部分由 TSMOM/Vol 替代旧策略。

## 下一步

- 对 `safe_winrate` 中已入选的新策略做局部参数扰动，而不是继续大网格盲搜。
- 加滚动窗口验证，过滤只在某个单段行情里爆发的参数。
- 对日线强收益策略做“小资金可交易版本”：强制最大回撤、止损金额、保证金占用进入约束。
