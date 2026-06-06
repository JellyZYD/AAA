# 期货策略回测报告

- 初始资金: 8500
- 保证金预算: 8000
- 回测目标: max_return

## Top 20 策略

|排名|品种|周期|净收益|回撤|胜率|交易数|样本外|过拟合|策略|
|---:|---|---|---:|---:|---:|---:|---:|---|---|
|1|SA|1d|79529.20|-16154.83|45.5%|44|-2845.87|Y|`donchian_atr|both|1d|w3|sw0.006|br0.0015|lb16|sl0.015|mh64|cd4|atr14|am3|ex8|mom48|vol48|th0.4|signal`|
|2|SA|1d|79454.28|-25603.92|54.1%|37|4609.01||`donchian_atr|both|1d|w3|sw0.006|br0.0015|lb16|sl0.015|mh64|cd4|atr10|am3|ex16|mom48|vol48|th0.4|signal`|
|3|SA|1d|76106.69|-17288.05|47.7%|44|-3203.46|Y|`donchian_atr|both|1d|w3|sw0.006|br0.0015|lb16|sl0.015|mh64|cd4|atr10|am3|ex8|mom48|vol48|th0.4|signal`|
|4|SA|1d|73172.42|-24590.27|52.6%|38|4660.33||`donchian_atr|both|1d|w3|sw0.006|br0.0015|lb16|sl0.015|mh64|cd4|atr14|am3|ex16|mom48|vol48|th0.4|signal`|
|5|RB|1d|62294.75|-13268.69|30.2%|149|-6451.06|Y|`trend_failure|both|1d|w2|sw0.008|br0.003|lb24|sl0.015|mh32|cd4|signal`|
|6|RB|1d|62294.75|-13268.69|30.2%|149|-6451.06|Y|`trend_failure|both|1d|w2|sw0.008|br0.003|lb24|sl0.015|mh32|cd4|strict`|
|7|RB|1d|62294.75|-13268.69|30.2%|149|-6451.06|Y|`trend_failure|both|1d|w2|sw0.008|br0.003|lb24|sl0.015|mh32|cd4|aggressive`|
|8|HC|1d|61348.06|-21676.72|27.6%|105|11221.25||`trend_failure|both|1d|w2|sw0.008|br0.0015|lb24|sl0.015|mh64|cd4|signal`|
|9|HC|1d|61348.06|-21676.72|27.6%|105|11221.25||`trend_failure|both|1d|w2|sw0.008|br0.0015|lb24|sl0.015|mh64|cd4|strict`|
|10|HC|1d|61348.06|-21676.72|27.6%|105|11221.25||`trend_failure|both|1d|w2|sw0.008|br0.0015|lb24|sl0.015|mh64|cd4|aggressive`|
|11|RB|1d|58794.68|-14082.94|28.7%|157|-7423.42|Y|`trend_failure|both|1d|w2|sw0.008|br0.0015|lb24|sl0.015|mh32|cd4|aggressive`|
|12|RB|1d|58794.68|-14082.94|28.7%|157|-7423.42|Y|`trend_failure|both|1d|w2|sw0.008|br0.0015|lb24|sl0.015|mh32|cd4|signal`|
|13|RB|1d|58794.68|-14082.94|28.7%|157|-7423.42|Y|`trend_failure|both|1d|w2|sw0.008|br0.0015|lb24|sl0.015|mh32|cd4|strict`|
|14|SR|1d|58727.66|-16491.47|24.1%|116|-11328.65|Y|`swing_reversal|both|1d|w2|sw0.008|br0.0015|lb24|sl0.015|mh64|cd4|aggressive`|
|15|SR|1d|58727.66|-16491.47|24.1%|116|-11328.65|Y|`swing_reversal|both|1d|w2|sw0.008|br0.0015|lb24|sl0.015|mh64|cd4|signal`|
|16|SR|1d|58727.66|-16491.47|24.1%|116|-11328.65|Y|`swing_reversal|both|1d|w2|sw0.008|br0.0015|lb24|sl0.015|mh64|cd4|strict`|
|17|SR|1d|58454.44|-18422.40|22.7%|110|-12425.74|Y|`swing_reversal|both|1d|w2|sw0.008|br0.003|lb24|sl0.015|mh64|cd4|strict`|
|18|SR|1d|58454.44|-18422.40|22.7%|110|-12425.74|Y|`swing_reversal|both|1d|w2|sw0.008|br0.003|lb24|sl0.015|mh64|cd4|signal`|
|19|SR|1d|58454.44|-18422.40|22.7%|110|-12425.74|Y|`swing_reversal|both|1d|w2|sw0.008|br0.003|lb24|sl0.015|mh64|cd4|aggressive`|
|20|SA|1d|53066.67|-18085.95|49.0%|51|-1248.41|Y|`donchian_atr|both|1d|w3|sw0.006|br0.0015|lb16|sl0.015|mh32|cd4|atr14|am3|ex8|mom48|vol48|th0.4|signal`|

## Champion 策略

- SP: 启用，净收益 50270.13，样本外 8688.59，交易数 32，策略 `swing_reversal|both|1d|w3|sw0.008|br0.003|lb24|sl0.015|mh64|cd4|strict`。
- SR: 启用，净收益 39703.04，样本外 1534.05，交易数 72，策略 `tsmom_vol|both|1d|w3|sw0.006|br0.002|lb24|sl0.015|mh64|cd4|atr10|am3|ex12|mom48|vol48|th0.4|strict`。
- CJ: 启用，净收益 48234.19，样本外 6333.54，交易数 61，策略 `trend_failure|both|1d|w3|sw0.008|br0.003|lb24|sl0.015|mh32|cd4|signal`。
- UR: 启用，净收益 21397.21，样本外 362.77，交易数 51，策略 `failed_breakout|both|1d|w3|sw0.006|br0.003|lb32|sl0.015|mh32|cd4|strict`。
- FG: 启用，净收益 47396.08，样本外 6622.22，交易数 93，策略 `donchian_atr|both|1d|w3|sw0.006|br0.0015|lb16|sl0.015|mh64|cd4|atr14|am3|ex8|mom48|vol48|th0.4|signal`。
- C: 启用，净收益 22435.99，样本外 14186.96，交易数 154，策略 `trend_failure|both|1d|w3|sw0.004|br0.003|lb24|sl0.015|mh32|cd4|strict`。
- RB: 启用，净收益 49328.80，样本外 2792.13，交易数 199，策略 `tsmom_vol|both|1d|w3|sw0.006|br0.002|lb24|sl0.015|mh64|cd4|atr10|am2|ex12|mom24|vol24|th0.4|strict`。
- RM: 启用，净收益 19993.04，样本外 5094.26，交易数 93，策略 `swing_reversal|both|1d|w2|sw0.008|br0.0015|lb24|sl0.015|mh64|cd4|strict`。
- HC: 启用，净收益 61348.06，样本外 11221.25，交易数 105，策略 `trend_failure|both|1d|w2|sw0.008|br0.0015|lb24|sl0.015|mh64|cd4|aggressive`。
- SA: 启用，净收益 79454.28，样本外 4609.01，交易数 37，策略 `donchian_atr|both|1d|w3|sw0.006|br0.0015|lb16|sl0.015|mh64|cd4|atr10|am3|ex16|mom48|vol48|th0.4|signal`。
- CS: 启用，净收益 15706.95，样本外 18.02，交易数 87，策略 `failed_breakout|both|1d|w3|sw0.006|br0.003|lb16|sl0.015|mh32|cd4|strict`。

## 策略画像

### 最高收益
- SP: 净收益 50270.13，胜率 28.1%，交易 32，样本外 8688.59，`swing_reversal|both|1d|w3|sw0.008|br0.003|lb24|sl0.015|mh64|cd4|strict`。
- SR: 净收益 39703.04，胜率 41.7%，交易 72，样本外 1534.05，`tsmom_vol|both|1d|w3|sw0.006|br0.002|lb24|sl0.015|mh64|cd4|atr10|am3|ex12|mom48|vol48|th0.4|strict`。
- CJ: 净收益 48234.19，胜率 14.8%，交易 61，样本外 6333.54，`trend_failure|both|1d|w3|sw0.008|br0.003|lb24|sl0.015|mh32|cd4|signal`。
- UR: 净收益 21397.21，胜率 21.6%，交易 51，样本外 362.77，`failed_breakout|both|1d|w3|sw0.006|br0.003|lb32|sl0.015|mh32|cd4|strict`。
- FG: 净收益 47396.08，胜率 44.1%，交易 93，样本外 6622.22，`donchian_atr|both|1d|w3|sw0.006|br0.0015|lb16|sl0.015|mh64|cd4|atr14|am3|ex8|mom48|vol48|th0.4|signal`。
- C: 净收益 22435.99，胜率 34.4%，交易 154，样本外 14186.96，`trend_failure|both|1d|w3|sw0.004|br0.003|lb24|sl0.015|mh32|cd4|aggressive`。
- RB: 净收益 49328.80，胜率 44.2%，交易 199，样本外 2792.13，`tsmom_vol|both|1d|w3|sw0.006|br0.002|lb24|sl0.015|mh64|cd4|atr10|am2|ex12|mom24|vol24|th0.4|strict`。
- RM: 净收益 19993.04，胜率 15.1%，交易 93，样本外 5094.26，`swing_reversal|both|1d|w2|sw0.008|br0.0015|lb24|sl0.015|mh64|cd4|signal`。
- HC: 净收益 61348.06，胜率 27.6%，交易 105，样本外 11221.25，`trend_failure|both|1d|w2|sw0.008|br0.0015|lb24|sl0.015|mh64|cd4|aggressive`。
- SA: 净收益 79454.28，胜率 54.1%，交易 37，样本外 4609.01，`donchian_atr|both|1d|w3|sw0.006|br0.0015|lb16|sl0.015|mh64|cd4|atr10|am3|ex16|mom48|vol48|th0.4|signal`。
- CS: 净收益 15706.95，胜率 34.5%，交易 87，样本外 18.02，`failed_breakout|both|1d|w3|sw0.006|br0.003|lb16|sl0.015|mh32|cd4|strict`。
### 最高胜率
- SP: 净收益 1087.33，胜率 51.7%，交易 29，样本外 252.32，`tsmom_vol|both|30m|w3|sw0.006|br0.002|lb24|sl0.015|mh32|cd4|atr14|am3|ex12|mom24|vol48|th0.8|strict`。
- SR: 净收益 22805.42，胜率 52.0%，交易 50，样本外 919.80，`tsmom_vol|both|1d|w3|sw0.006|br0.002|lb24|sl0.015|mh64|cd4|atr10|am3|ex12|mom24|vol48|th0.8|strict`。
- CJ: 净收益 4185.25，胜率 65.0%，交易 20，样本外 2076.97，`trend_failure|both|15m|w3|sw0.004|br0.003|lb24|sl0.015|mh32|cd4|strict`。
- UR: 净收益 6069.30，胜率 63.6%，交易 22，样本外 2434.41，`breakout|both|15m|w3|sw0.006|br0.0015|lb16|sl0.015|mh32|cd4|strict`。
- FG: 净收益 2073.04，胜率 65.2%，交易 23，样本外 301.15，`tsmom_vol|both|30m|w3|sw0.006|br0.002|lb24|sl0.015|mh32|cd4|atr14|am3|ex12|mom48|vol24|th0.8|strict`。
- C: 净收益 892.26，胜率 60.9%，交易 23，样本外 605.84，`breakout|both|60m|w3|sw0.006|br0.0015|lb16|sl0.015|mh32|cd4|strict`。
- RB: 净收益 1049.32，胜率 59.1%，交易 22，样本外 104.17，`trend_failure|both|15m|w2|sw0.004|br0.0015|lb24|sl0.015|mh32|cd4|aggressive`。
- RM: 净收益 4058.70，胜率 66.7%，交易 24，样本外 186.56，`donchian_atr|both|30m|w3|sw0.006|br0.0015|lb16|sl0.015|mh32|cd4|atr14|am3|ex16|mom48|vol48|th0.4|strict`。
- HC: 净收益 24986.85，胜率 69.0%，交易 29，样本外 8991.68，`donchian_atr|both|1d|w3|sw0.006|br0.001|lb24|sl0.015|mh24|cd4|atr14|am3.2|ex24|mom48|vol48|th0.4|strict`。
- SA: 净收益 4426.92，胜率 68.2%，交易 22，样本外 2657.00，`donchian_atr|both|60m|w3|sw0.006|br0.0015|lb16|sl0.015|mh64|cd4|atr14|am3|ex8|mom48|vol48|th0.4|strict`。
- CS: 净收益 542.98，胜率 48.3%，交易 29，样本外 12.66，`tsmom_vol|both|30m|w3|sw0.006|br0.002|lb24|sl0.015|mh32|cd4|atr14|am3|ex12|mom48|vol24|th0.8|strict`。
### 均衡评分
- SP: 净收益 49457.02，胜率 26.7%，交易 60，样本外 4227.32，`breakout|both|1d|w3|sw0.006|br0.0015|lb16|sl0.015|mh32|cd4|strict`。
- SR: 净收益 39703.04，胜率 41.7%，交易 72，样本外 1534.05，`tsmom_vol|both|1d|w3|sw0.006|br0.002|lb24|sl0.015|mh64|cd4|atr10|am3|ex12|mom48|vol48|th0.4|strict`。
- CJ: 净收益 18187.27，胜率 41.9%，交易 31，样本外 11735.70，`failed_breakout|short|1d|w3|sw0.006|br0.003|lb16|sl0.015|mh32|cd4|strict`。
- UR: 净收益 6717.71，胜率 50.0%，交易 40，样本外 5386.93，`tsmom_vol|both|30m|w3|sw0.006|br0.002|lb24|sl0.015|mh64|cd4|atr14|am3|ex12|mom24|vol24|th0.4|strict`。
- FG: 净收益 27719.01，胜率 28.0%，交易 107，样本外 11786.66，`failed_breakout|short|1d|w3|sw0.006|br0.0015|lb16|sl0.015|mh32|cd4|aggressive`。
- C: 净收益 22435.99，胜率 34.4%，交易 154，样本外 14186.96，`trend_failure|both|1d|w3|sw0.004|br0.003|lb24|sl0.015|mh32|cd4|signal`。
- RB: 净收益 45192.11，胜率 37.7%，交易 69，样本外 3798.11，`trend_failure|short|1d|w2|sw0.008|br0.003|lb24|sl0.015|mh32|cd4|strict`。
- RM: 净收益 13960.16，胜率 32.9%，交易 76，样本外 3431.77，`failed_breakout|long|1d|w3|sw0.006|br0.003|lb16|sl0.015|mh32|cd4|aggressive`。
- HC: 净收益 39134.98，胜率 45.9%，交易 122，样本外 9012.21，`tsmom_vol|both|1d|w3|sw0.006|br0.002|lb24|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|strict`。
- SA: 净收益 27284.12，胜率 25.0%，交易 44，样本外 13612.33，`failed_breakout|long|1d|w3|sw0.006|br0.0015|lb32|sl0.015|mh32|cd4|aggressive`。
- CS: 净收益 15706.95，胜率 34.5%，交易 87，样本外 18.02，`failed_breakout|both|1d|w3|sw0.006|br0.003|lb16|sl0.015|mh32|cd4|strict`。
### capital_safe
- SP: 净收益 49457.02，胜率 26.7%，交易 60，样本外 4227.32，`breakout|both|1d|w3|sw0.006|br0.0015|lb16|sl0.015|mh32|cd4|strict`。
- SR: 净收益 39703.04，胜率 41.7%，交易 72，样本外 1534.05，`tsmom_vol|both|1d|w3|sw0.006|br0.002|lb24|sl0.015|mh64|cd4|atr10|am3|ex12|mom48|vol48|th0.4|strict`。
- CJ: 净收益 18187.27，胜率 41.9%，交易 31，样本外 11735.70，`failed_breakout|short|1d|w3|sw0.006|br0.003|lb16|sl0.015|mh32|cd4|strict`。
- UR: 净收益 6717.71，胜率 50.0%，交易 40，样本外 5386.93，`tsmom_vol|both|30m|w3|sw0.006|br0.002|lb24|sl0.015|mh64|cd4|atr14|am3|ex12|mom24|vol24|th0.4|strict`。
- FG: 净收益 27719.01，胜率 28.0%，交易 107，样本外 11786.66，`failed_breakout|short|1d|w3|sw0.006|br0.0015|lb16|sl0.015|mh32|cd4|aggressive`。
- C: 净收益 22435.99，胜率 34.4%，交易 154，样本外 14186.96，`trend_failure|both|1d|w3|sw0.004|br0.003|lb24|sl0.015|mh32|cd4|signal`。
- RB: 净收益 45192.11，胜率 37.7%，交易 69，样本外 3798.11，`trend_failure|short|1d|w2|sw0.008|br0.003|lb24|sl0.015|mh32|cd4|strict`。
- RM: 净收益 13960.16，胜率 32.9%，交易 76，样本外 3431.77，`failed_breakout|long|1d|w3|sw0.006|br0.003|lb16|sl0.015|mh32|cd4|aggressive`。
- HC: 净收益 39134.98，胜率 45.9%，交易 122，样本外 9012.21，`tsmom_vol|both|1d|w3|sw0.006|br0.002|lb24|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|strict`。
- SA: 净收益 27284.12，胜率 25.0%，交易 44，样本外 13612.33，`failed_breakout|long|1d|w3|sw0.006|br0.0015|lb32|sl0.015|mh32|cd4|aggressive`。
- CS: 净收益 15706.95，胜率 34.5%，交易 87，样本外 18.02，`failed_breakout|both|1d|w3|sw0.006|br0.003|lb16|sl0.015|mh32|cd4|strict`。
### safe_winrate
- SP: 净收益 1087.33，胜率 51.7%，交易 29，样本外 252.32，`tsmom_vol|both|30m|w3|sw0.006|br0.002|lb24|sl0.015|mh32|cd4|atr14|am3|ex12|mom24|vol48|th0.8|strict`。
- SR: 净收益 22805.42，胜率 52.0%，交易 50，样本外 919.80，`tsmom_vol|both|1d|w3|sw0.006|br0.002|lb24|sl0.015|mh64|cd4|atr10|am3|ex12|mom24|vol48|th0.8|strict`。
- CJ: 净收益 4185.25，胜率 65.0%，交易 20，样本外 2076.97，`trend_failure|both|15m|w3|sw0.004|br0.003|lb24|sl0.015|mh32|cd4|strict`。
- UR: 净收益 6069.30，胜率 63.6%，交易 22，样本外 2434.41，`breakout|both|15m|w3|sw0.006|br0.0015|lb16|sl0.015|mh32|cd4|strict`。
- FG: 净收益 2073.04，胜率 65.2%，交易 23，样本外 301.15，`tsmom_vol|both|30m|w3|sw0.006|br0.002|lb24|sl0.015|mh32|cd4|atr14|am3|ex12|mom48|vol24|th0.8|strict`。
- C: 净收益 892.26，胜率 60.9%，交易 23，样本外 605.84，`breakout|both|60m|w3|sw0.006|br0.0015|lb16|sl0.015|mh32|cd4|strict`。
- RB: 净收益 1049.32，胜率 59.1%，交易 22，样本外 104.17，`trend_failure|both|15m|w2|sw0.004|br0.0015|lb24|sl0.015|mh32|cd4|aggressive`。
- RM: 净收益 4058.70，胜率 66.7%，交易 24，样本外 186.56，`donchian_atr|both|30m|w3|sw0.006|br0.0015|lb16|sl0.015|mh32|cd4|atr14|am3|ex16|mom48|vol48|th0.4|strict`。
- HC: 净收益 24986.85，胜率 69.0%，交易 29，样本外 8991.68，`donchian_atr|both|1d|w3|sw0.006|br0.001|lb24|sl0.015|mh24|cd4|atr14|am3.2|ex24|mom48|vol48|th0.4|strict`。
- SA: 净收益 4426.92，胜率 68.2%，交易 22，样本外 2657.00，`donchian_atr|both|60m|w3|sw0.006|br0.0015|lb16|sl0.015|mh64|cd4|atr14|am3|ex8|mom48|vol48|th0.4|strict`。
- CS: 净收益 542.98，胜率 48.3%，交易 29，样本外 12.66，`tsmom_vol|both|30m|w3|sw0.006|br0.002|lb24|sl0.015|mh32|cd4|atr14|am3|ex12|mom48|vol24|th0.8|strict`。

## 改进建议

- 当前 top 策略没有明显结构性问题，下一步重点扩大真实行情和新闻事件样本。
