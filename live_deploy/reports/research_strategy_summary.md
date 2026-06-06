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
- `vol_breakout`：只在 ATR/价格和通道宽度相对过去处于压缩状态时允许通道突破开仓，用 ATR 跟踪止损和短通道退出，目标是减少普通突破在震荡期的虚假信号。
- `carry_tsmom`：用历史单合约日线构造近月/远月期限结构，远月低于近月视为正 Carry 支持做多，远月高于近月视为负 Carry 支持做空，并与时间序列动量同向时才开仓。

这些策略都只使用当前已完成 K 线和此前窗口，没有逐根 K 线未来函数。`vol_breakout` 的压缩判断使用前一根及更早的 ATR/通道宽度，突破通道也只用当前 K 线以前的高低点。`carry_tsmom` 的 Carry 因子在策略里 `shift(1)` 后使用，避免用同日收盘后才能确认的期限结构去同价成交。

## 当前本地回测规模

- 回测结果表：约 3.34 万条策略结果。
- 新增策略覆盖：
  - `donchian_atr`：约 6920 条。
  - `tsmom_vol`：约 2640 条。
  - `vol_breakout`：约 7100 条。
  - `carry_tsmom`：约 2112 条。
- 期限结构本地缓存：SP、SR、CJ、UR 覆盖到 2026-06-05；FG、C、RB、HC、SA 有部分历史；RM、CS 暂未拉到可用单合约历史，仍只使用价格策略。
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

## 局部扰动与滚动验证更新

已新增 `qihuo refine` 流程：读取当前优秀候选，做小范围参数扰动，并把历史样本分成 4 段滚动验证。评分偏向样本外收益、低回撤、滚动窗口稳定性、胜率和利润因子。

当前 `refined_robust` 画像首选如下：

| 品种 | 状态 | 策略 | 周期 | 稳健分 | 净收益 | 样本外 | 最大回撤 | 滚动胜率 |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| HC 热卷 | active | Donchian/ATR | 1d | 58352 | 24987 | 8992 | -3500 | 100% |
| C 玉米 | active | TSMOM/Vol | 1d | 52218 | 13972 | 12479 | -7807 | 100% |
| SP 纸浆 | active | Donchian/ATR | 1d | 49173 | 26111 | 7664 | -4580 | 100% |
| SR 白糖 | active | TSMOM/Vol | 1d | 45917 | 25542 | 9417 | -7580 | 75% |
| SA 纯碱 | active | Donchian/ATR | 60m | 40092 | 5162 | 2931 | -1490 | 100% |
| UR 尿素 | active | TSMOM/Vol | 30m | 38177 | 6599 | 4570 | -2285 | 100% |
| RM 菜粕 | active | Donchian/ATR | 30m | 33903 | 3944 | 597 | -1267 | 100% |
| FG 玻璃 | active | TSMOM/Vol | 30m | 21585 | 1494 | 568 | -1203 | 75% |
| CJ 红枣 | active | TSMOM/Vol | 30m | 25232 | 3035 | 4503 | -4567 | 75% |
| CS 玉米淀粉 | active | TSMOM/Vol | 30m | 24471 | 1306 | 259 | -1227 | 75% |
| RB 螺纹钢 | observe | TSMOM/Vol | 1d | 30231 | 50343 | 554 | -9326 | 100% |

结论：如果追求“最高收益”，SA 日线 Donchian/ATR 仍最高，但回撤不适合 8500 本金。若追求“小资金可执行的稳健实盘信号”，当前最强候选是 `refined_robust` 画像，其中 HC、C、SP、SR 的样本外和滚动表现最好；RB 因回撤超过本金约束，暂不建议发开仓信号。

## Walk-forward 扩展验证更新

这轮新增了 `vol_breakout` 和 `carry_tsmom`，并把 walk-forward 候选池扩展为“refined 候选 + 最新回测中 Donchian/ATR、TSMOM/Vol、Vol Breakout、Carry TSMOM 的高分候选”。每个测试窗口仍只允许用此前历史窗口选择参数，再在下一个窗口测试，因此比普通全样本回测更接近实盘。

当前 `walk_forward` 画像已经作为 `qihuo poll --profile live` 的默认优先实盘画像；如果本地没有 walk-forward profile，才回退到 `safe_winrate`。

| 品种 | 状态 | 策略 | 周期 | WF分 | 测试净收益 | 正窗口 | 最差回撤 | 平均胜率 | 交易数 |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| SR 白糖 | active | TSMOM/Vol | 1d | 44558 | 20593 | 3/4 | -6601 | 54.6% | 25 |
| HC 热卷 | active | TSMOM/Vol | 1d | 35658 | 12094 | 3/4 | -5199 | 32.4% | 71 |
| FG 玻璃 | active | Donchian/ATR | 1d | 30854 | 14634 | 2/4 | -7617 | 35.6% | 46 |
| C 玉米 | active | Vol Breakout | 60m | 27481 | 1610 | 4/4 | -623 | 77.1% | 12 |
| SP 纸浆 | active | Breakout | 1d | 26148 | 10406 | 3/4 | -8321 | 19.5% | 35 |
| CJ 红枣 | active | Vol Breakout | 1d | 24549 | 6892 | 2/4 | -1762 | 37.5% | 5 |
| CS 玉米淀粉 | active | Donchian/ATR | 15m | 22853 | 1370 | 3/4 | -282 | 77.1% | 12 |
| UR 尿素 | active | Donchian/ATR | 60m | 22127 | 3421 | 3/4 | -1713 | 50.6% | 21 |
| RM 菜粕 | active | Vol Breakout | 60m | 18665 | 1806 | 2/4 | -405 | 66.7% | 8 |
| RB 螺纹钢 | active | Donchian/ATR | 15m | 17510 | 314 | 3/4 | -439 | 56.2% | 12 |
| SA 纯碱 | active | Vol Breakout | 30m | 13217 | 1160 | 2/4 | -1780 | 67.5% | 13 |

Carry 验证结论：`carry_tsmom` 在普通样本切分中对 FG、CJ、SA、SP 有正贡献；更公平的 walk-forward 后，C 玉米日线 Carry TSMOM 通过 active 过滤，测试净收益约 5588、最差回撤约 -3329，但最终仍低于 C 的 60m `vol_breakout`。因此 Carry 因子暂时作为候选和研究因子保留，不替换当前实盘主策略。当前最适合部署的实盘画像仍是 `walk_forward`，不是单纯最高收益或单纯最高胜率。

## 下一步

- 继续补 RM、CS 以及 RB/HC/SA 后续合约历史覆盖，优先解决 AkShare 单合约代码/接口不稳定问题。
- 对 `carry_tsmom` 做更稳健的风险过滤，例如只允许 strict 风险模式、限制年化 Carry 极端值，继续用 walk-forward 过滤。
- 对新闻事件因子做只加权、不单独开仓的影响验证。
