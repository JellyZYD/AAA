# 期货策略回测报告

- 初始资金: 8500
- 保证金预算: 8000
- 回测目标: max_return

## Top 20 策略

|排名|品种|周期|净收益|回撤|胜率|交易数|样本外|过拟合|策略|
|---:|---|---|---:|---:|---:|---:|---:|---|---|
|1|RB|1d|62294.75|-13268.69|30.2%|149|-6451.06|Y|`trend_failure|both|1d|w2|sw0.008|br0.003|lb24|sl0.015|mh32|cd4|strict`|
|2|RB|1d|62294.75|-13268.69|30.2%|149|-6451.06|Y|`trend_failure|both|1d|w2|sw0.008|br0.003|lb24|sl0.015|mh32|cd4|signal`|
|3|RB|1d|62294.75|-13268.69|30.2%|149|-6451.06|Y|`trend_failure|both|1d|w2|sw0.008|br0.003|lb24|sl0.015|mh32|cd4|aggressive`|
|4|HC|1d|61348.06|-21676.72|27.6%|105|11221.25||`trend_failure|both|1d|w2|sw0.008|br0.0015|lb24|sl0.015|mh64|cd4|strict`|
|5|HC|1d|61348.06|-21676.72|27.6%|105|11221.25||`trend_failure|both|1d|w2|sw0.008|br0.0015|lb24|sl0.015|mh64|cd4|aggressive`|
|6|HC|1d|61348.06|-21676.72|27.6%|105|11221.25||`trend_failure|both|1d|w2|sw0.008|br0.0015|lb24|sl0.015|mh64|cd4|signal`|
|7|RB|1d|58794.68|-14082.94|28.7%|157|-7423.42|Y|`trend_failure|both|1d|w2|sw0.008|br0.0015|lb24|sl0.015|mh32|cd4|strict`|
|8|RB|1d|58794.68|-14082.94|28.7%|157|-7423.42|Y|`trend_failure|both|1d|w2|sw0.008|br0.0015|lb24|sl0.015|mh32|cd4|aggressive`|
|9|RB|1d|58794.68|-14082.94|28.7%|157|-7423.42|Y|`trend_failure|both|1d|w2|sw0.008|br0.0015|lb24|sl0.015|mh32|cd4|signal`|
|10|SR|1d|58727.66|-16491.47|24.1%|116|-11328.65|Y|`swing_reversal|both|1d|w2|sw0.008|br0.0015|lb24|sl0.015|mh64|cd4|signal`|
|11|SR|1d|58727.66|-16491.47|24.1%|116|-11328.65|Y|`swing_reversal|both|1d|w2|sw0.008|br0.0015|lb24|sl0.015|mh64|cd4|aggressive`|
|12|SR|1d|58727.66|-16491.47|24.1%|116|-11328.65|Y|`swing_reversal|both|1d|w2|sw0.008|br0.0015|lb24|sl0.015|mh64|cd4|strict`|
|13|SR|1d|58454.44|-18422.40|22.7%|110|-12425.74|Y|`swing_reversal|both|1d|w2|sw0.008|br0.003|lb24|sl0.015|mh64|cd4|signal`|
|14|SR|1d|58454.44|-18422.40|22.7%|110|-12425.74|Y|`swing_reversal|both|1d|w2|sw0.008|br0.003|lb24|sl0.015|mh64|cd4|strict`|
|15|SR|1d|58454.44|-18422.40|22.7%|110|-12425.74|Y|`swing_reversal|both|1d|w2|sw0.008|br0.003|lb24|sl0.015|mh64|cd4|aggressive`|
|16|HC|1d|51246.25|-20801.78|30.0%|100|10299.72||`trend_failure|both|1d|w2|sw0.008|br0.003|lb24|sl0.015|mh64|cd4|signal`|
|17|HC|1d|51246.25|-20801.78|30.0%|100|10299.72||`trend_failure|both|1d|w2|sw0.008|br0.003|lb24|sl0.015|mh64|cd4|aggressive`|
|18|HC|1d|51246.25|-20801.78|30.0%|100|10299.72||`trend_failure|both|1d|w2|sw0.008|br0.003|lb24|sl0.015|mh64|cd4|strict`|
|19|HC|1d|51174.77|-13167.58|25.5%|94|10854.83||`swing_reversal|both|1d|w3|sw0.004|br0.003|lb24|sl0.015|mh32|cd4|signal`|
|20|HC|1d|51174.77|-13167.58|25.5%|94|10854.83||`swing_reversal|both|1d|w3|sw0.004|br0.003|lb24|sl0.015|mh32|cd4|strict`|

## Champion 策略

- SP: 启用，净收益 50270.13，样本外 8688.59，交易数 32，策略 `swing_reversal|both|1d|w3|sw0.008|br0.003|lb24|sl0.015|mh64|cd4|strict`。
- SR: 启用，净收益 28456.96，样本外 1741.93，交易数 97，策略 `trend_failure|short|1d|w2|sw0.004|br0.003|lb24|sl0.015|mh32|cd4|aggressive`。
- CJ: 启用，净收益 48234.19，样本外 6333.54，交易数 61，策略 `trend_failure|both|1d|w3|sw0.008|br0.003|lb24|sl0.015|mh32|cd4|signal`。
- UR: 启用，净收益 21397.21，样本外 362.77，交易数 51，策略 `failed_breakout|both|1d|w3|sw0.006|br0.003|lb32|sl0.015|mh32|cd4|strict`。
- FG: 启用，净收益 29976.32，样本外 15661.45，交易数 149，策略 `failed_breakout|both|1d|w3|sw0.006|br0.003|lb16|sl0.015|mh32|cd4|aggressive`。
- C: 启用，净收益 22435.99，样本外 14186.96，交易数 154，策略 `trend_failure|both|1d|w3|sw0.004|br0.003|lb24|sl0.015|mh32|cd4|aggressive`。
- RB: 启用，净收益 45192.11，样本外 3798.11，交易数 69，策略 `trend_failure|short|1d|w2|sw0.008|br0.003|lb24|sl0.015|mh32|cd4|strict`。
- RM: 启用，净收益 19993.04，样本外 5094.26，交易数 93，策略 `swing_reversal|both|1d|w2|sw0.008|br0.0015|lb24|sl0.015|mh64|cd4|aggressive`。
- HC: 启用，净收益 61348.06，样本外 11221.25，交易数 105，策略 `trend_failure|both|1d|w2|sw0.008|br0.0015|lb24|sl0.015|mh64|cd4|aggressive`。
- SA: 启用，净收益 27284.12，样本外 13612.33，交易数 44，策略 `failed_breakout|long|1d|w3|sw0.006|br0.0015|lb32|sl0.015|mh32|cd4|aggressive`。
- CS: 启用，净收益 15706.95，样本外 18.02，交易数 87，策略 `failed_breakout|both|1d|w3|sw0.006|br0.003|lb16|sl0.015|mh32|cd4|strict`。

## 策略画像

### 最高收益
- SP: 净收益 50270.13，胜率 28.1%，交易 32，样本外 8688.59，`swing_reversal|both|1d|w3|sw0.008|br0.003|lb24|sl0.015|mh64|cd4|strict`。
- SR: 净收益 28456.96，胜率 28.9%，交易 97，样本外 1741.93，`trend_failure|short|1d|w2|sw0.004|br0.003|lb24|sl0.015|mh32|cd4|aggressive`。
- CJ: 净收益 48234.19，胜率 14.8%，交易 61，样本外 6333.54，`trend_failure|both|1d|w3|sw0.008|br0.003|lb24|sl0.015|mh32|cd4|signal`。
- UR: 净收益 21397.21，胜率 21.6%，交易 51，样本外 362.77，`failed_breakout|both|1d|w3|sw0.006|br0.003|lb32|sl0.015|mh32|cd4|strict`。
- FG: 净收益 29976.32，胜率 27.5%，交易 149，样本外 15661.45，`failed_breakout|both|1d|w3|sw0.006|br0.003|lb16|sl0.015|mh32|cd4|signal`。
- C: 净收益 22435.99，胜率 34.4%，交易 154，样本外 14186.96，`trend_failure|both|1d|w3|sw0.004|br0.003|lb24|sl0.015|mh32|cd4|aggressive`。
- RB: 净收益 45192.11，胜率 37.7%，交易 69，样本外 3798.11，`trend_failure|short|1d|w2|sw0.008|br0.003|lb24|sl0.015|mh32|cd4|strict`。
- RM: 净收益 19993.04，胜率 15.1%，交易 93，样本外 5094.26，`swing_reversal|both|1d|w2|sw0.008|br0.0015|lb24|sl0.015|mh64|cd4|signal`。
- HC: 净收益 61348.06，胜率 27.6%，交易 105，样本外 11221.25，`trend_failure|both|1d|w2|sw0.008|br0.0015|lb24|sl0.015|mh64|cd4|strict`。
- SA: 净收益 27284.12，胜率 25.0%，交易 44，样本外 13612.33，`failed_breakout|long|1d|w3|sw0.006|br0.0015|lb32|sl0.015|mh32|cd4|aggressive`。
- CS: 净收益 15706.95，胜率 34.5%，交易 87，样本外 18.02，`failed_breakout|both|1d|w3|sw0.006|br0.003|lb16|sl0.015|mh32|cd4|strict`。
### 最高胜率
- SP: 净收益 29447.44，胜率 38.1%，交易 21，样本外 5630.45，`swing_reversal|short|1d|w3|sw0.004|br0.003|lb24|sl0.015|mh32|cd4|strict`。
- SR: 净收益 28456.96，胜率 28.9%，交易 97，样本外 1741.93，`trend_failure|short|1d|w2|sw0.004|br0.003|lb24|sl0.015|mh32|cd4|aggressive`。
- CJ: 净收益 4185.25，胜率 65.0%，交易 20，样本外 2076.97，`trend_failure|both|15m|w3|sw0.004|br0.003|lb24|sl0.015|mh32|cd4|strict`。
- UR: 净收益 6069.30，胜率 63.6%，交易 22，样本外 2434.41，`breakout|both|15m|w3|sw0.006|br0.0015|lb16|sl0.015|mh32|cd4|aggressive`。
- FG: 净收益 5222.62，胜率 50.0%，交易 20，样本外 1727.93，`trend_failure|short|60m|w3|sw0.004|br0.0015|lb24|sl0.015|mh32|cd4|aggressive`。
- C: 净收益 892.26，胜率 60.9%，交易 23，样本外 605.84，`breakout|both|60m|w3|sw0.006|br0.0015|lb16|sl0.015|mh32|cd4|strict`。
- RB: 净收益 1049.32，胜率 59.1%，交易 22，样本外 104.17，`trend_failure|both|15m|w2|sw0.004|br0.0015|lb24|sl0.015|mh32|cd4|signal`。
- RM: 净收益 1552.49，胜率 60.0%，交易 20，样本外 636.29，`trend_failure|both|15m|w3|sw0.004|br0.0015|lb24|sl0.015|mh32|cd4|signal`。
- HC: 净收益 2123.83，胜率 52.2%，交易 23，样本外 1376.46，`trend_failure|both|60m|w3|sw0.004|br0.003|lb24|sl0.015|mh32|cd4|strict`。
- SA: 净收益 1735.13，胜率 48.0%，交易 25，样本外 1019.92，`breakout|both|60m|w3|sw0.006|br0.0015|lb32|sl0.015|mh32|cd4|aggressive`。
- CS: 净收益 493.42，胜率 42.9%，交易 21，样本外 106.58，`trend_failure|both|60m|w3|sw0.008|br0.0015|lb24|sl0.015|mh32|cd4|strict`。
### 均衡评分
- SP: 净收益 49457.02，胜率 26.7%，交易 60，样本外 4227.32，`breakout|both|1d|w3|sw0.006|br0.0015|lb16|sl0.015|mh32|cd4|strict`。
- SR: 净收益 32.19，胜率 18.3%，交易 60，样本外 672.23，`failed_breakout|long|1d|w3|sw0.006|br0.003|lb32|sl0.015|mh64|cd4|strict`。
- CJ: 净收益 18187.27，胜率 41.9%，交易 31，样本外 11735.70，`failed_breakout|short|1d|w3|sw0.006|br0.003|lb16|sl0.015|mh32|cd4|strict`。
- UR: 净收益 13252.23，胜率 25.7%，交易 35，样本外 1244.49，`swing_reversal|short|1d|w2|sw0.004|br0.003|lb24|sl0.015|mh32|cd4|strict`。
- FG: 净收益 27719.01，胜率 28.0%，交易 107，样本外 11786.66，`failed_breakout|short|1d|w3|sw0.006|br0.0015|lb16|sl0.015|mh32|cd4|aggressive`。
- C: 净收益 22435.99，胜率 34.4%，交易 154，样本外 14186.96，`trend_failure|both|1d|w3|sw0.004|br0.003|lb24|sl0.015|mh32|cd4|aggressive`。
- RB: 净收益 45192.11，胜率 37.7%，交易 69，样本外 3798.11，`trend_failure|short|1d|w2|sw0.008|br0.003|lb24|sl0.015|mh32|cd4|strict`。
- RM: 净收益 13960.16，胜率 32.9%，交易 76，样本外 3431.77，`failed_breakout|long|1d|w3|sw0.006|br0.003|lb16|sl0.015|mh64|cd4|aggressive`。
- HC: 净收益 36524.55，胜率 30.9%，交易 55，样本外 5543.02，`swing_reversal|long|1d|w2|sw0.004|br0.003|lb24|sl0.015|mh32|cd4|strict`。
- SA: 净收益 27284.12，胜率 25.0%，交易 44，样本外 13612.33，`failed_breakout|long|1d|w3|sw0.006|br0.0015|lb32|sl0.015|mh32|cd4|aggressive`。
- CS: 净收益 15706.95，胜率 34.5%，交易 87，样本外 18.02，`failed_breakout|both|1d|w3|sw0.006|br0.003|lb16|sl0.015|mh32|cd4|strict`。
### capital_safe
- SP: 净收益 49457.02，胜率 26.7%，交易 60，样本外 4227.32，`breakout|both|1d|w3|sw0.006|br0.0015|lb16|sl0.015|mh32|cd4|strict`。
- SR: 净收益 32.19，胜率 18.3%，交易 60，样本外 672.23，`failed_breakout|long|1d|w3|sw0.006|br0.003|lb32|sl0.015|mh64|cd4|strict`。
- CJ: 净收益 18187.27，胜率 41.9%，交易 31，样本外 11735.70，`failed_breakout|short|1d|w3|sw0.006|br0.003|lb16|sl0.015|mh32|cd4|strict`。
- UR: 净收益 13252.23，胜率 25.7%，交易 35，样本外 1244.49，`swing_reversal|short|1d|w2|sw0.004|br0.003|lb24|sl0.015|mh32|cd4|strict`。
- FG: 净收益 27719.01，胜率 28.0%，交易 107，样本外 11786.66，`failed_breakout|short|1d|w3|sw0.006|br0.0015|lb16|sl0.015|mh32|cd4|aggressive`。
- C: 净收益 22435.99，胜率 34.4%，交易 154，样本外 14186.96，`trend_failure|both|1d|w3|sw0.004|br0.003|lb24|sl0.015|mh32|cd4|aggressive`。
- RB: 净收益 45192.11，胜率 37.7%，交易 69，样本外 3798.11，`trend_failure|short|1d|w2|sw0.008|br0.003|lb24|sl0.015|mh32|cd4|strict`。
- RM: 净收益 13960.16，胜率 32.9%，交易 76，样本外 3431.77，`failed_breakout|long|1d|w3|sw0.006|br0.003|lb16|sl0.015|mh64|cd4|aggressive`。
- HC: 净收益 36524.55，胜率 30.9%，交易 55，样本外 5543.02，`swing_reversal|long|1d|w2|sw0.004|br0.003|lb24|sl0.015|mh32|cd4|strict`。
- SA: 净收益 27284.12，胜率 25.0%，交易 44，样本外 13612.33，`failed_breakout|long|1d|w3|sw0.006|br0.0015|lb32|sl0.015|mh32|cd4|aggressive`。
- CS: 净收益 15706.95，胜率 34.5%，交易 87，样本外 18.02，`failed_breakout|both|1d|w3|sw0.006|br0.003|lb16|sl0.015|mh32|cd4|strict`。
### safe_winrate
- SP: 净收益 29447.44，胜率 38.1%，交易 21，样本外 5630.45，`swing_reversal|short|1d|w3|sw0.004|br0.003|lb24|sl0.015|mh32|cd4|strict`。
- SR: 净收益 32.19，胜率 18.3%，交易 60，样本外 672.23，`failed_breakout|long|1d|w3|sw0.006|br0.003|lb32|sl0.015|mh64|cd4|strict`。
- CJ: 净收益 4185.25，胜率 65.0%，交易 20，样本外 2076.97，`trend_failure|both|15m|w3|sw0.004|br0.003|lb24|sl0.015|mh32|cd4|strict`。
- UR: 净收益 6069.30，胜率 63.6%，交易 22，样本外 2434.41，`breakout|both|15m|w3|sw0.006|br0.0015|lb16|sl0.015|mh32|cd4|aggressive`。
- FG: 净收益 5222.62，胜率 50.0%，交易 20，样本外 1727.93，`trend_failure|short|60m|w3|sw0.004|br0.0015|lb24|sl0.015|mh32|cd4|aggressive`。
- C: 净收益 892.26，胜率 60.9%，交易 23，样本外 605.84，`breakout|both|60m|w3|sw0.006|br0.0015|lb16|sl0.015|mh32|cd4|strict`。
- RB: 净收益 1049.32，胜率 59.1%，交易 22，样本外 104.17，`trend_failure|both|15m|w2|sw0.004|br0.0015|lb24|sl0.015|mh32|cd4|signal`。
- RM: 净收益 1552.49，胜率 60.0%，交易 20，样本外 636.29，`trend_failure|both|15m|w3|sw0.004|br0.0015|lb24|sl0.015|mh32|cd4|signal`。
- HC: 净收益 2123.83，胜率 52.2%，交易 23，样本外 1376.46，`trend_failure|both|60m|w3|sw0.004|br0.003|lb24|sl0.015|mh32|cd4|strict`。
- SA: 净收益 1735.13，胜率 48.0%，交易 25，样本外 1019.92，`breakout|both|60m|w3|sw0.006|br0.0015|lb32|sl0.015|mh32|cd4|aggressive`。
- CS: 净收益 493.42，胜率 42.9%，交易 21，样本外 106.58，`trend_failure|both|60m|w3|sw0.008|br0.0015|lb24|sl0.015|mh32|cd4|strict`。

## 改进建议

- 当前 top 策略没有明显结构性问题，下一步重点扩大真实行情和新闻事件样本。
