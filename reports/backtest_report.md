# 期货策略回测报告

- 初始资金: 8500
- 保证金预算: 8000
- 回测目标: max_return

## Top 20 策略

|排名|品种|周期|净收益|回撤|胜率|交易数|样本外|过拟合|策略|
|---:|---|---|---:|---:|---:|---:|---:|---|---|
|1|SA|1d|85387.14|-19835.79|45.5%|44|1148.96||`donchian_atr|both|1d|w3|sw0.006|br0.001|lb16|sl0.015|mh64|cd4|atr10|am2.5|ex12|mom48|vol48|th0.4|signal`|
|2|SA|1d|85167.16|-19835.79|45.5%|44|128.98||`donchian_atr|both|1d|w3|sw0.006|br0.0015|lb16|sl0.015|mh64|cd4|atr10|am2.5|ex12|mom48|vol48|th0.4|signal`|
|3|SA|1d|85047.84|-13900.33|44.7%|47|-3256.46|Y|`donchian_atr|both|1d|w3|sw0.006|br0.0015|lb16|sl0.015|mh64|cd4|atr10|am2.5|ex8|mom48|vol48|th0.4|signal`|
|4|SA|1d|81709.52|-20790.88|46.5%|43|2711.48||`donchian_atr|both|1d|w3|sw0.006|br0.001|lb16|sl0.015|mh64|cd4|atr10|am2.5|ex16|mom48|vol48|th0.4|signal`|
|5|SA|1d|81489.54|-20790.88|46.5%|43|1691.50||`donchian_atr|both|1d|w3|sw0.006|br0.0015|lb16|sl0.015|mh64|cd4|atr10|am2.5|ex16|mom48|vol48|th0.4|signal`|
|6|SA|1d|80994.27|-25603.92|54.1%|37|5628.99||`donchian_atr|both|1d|w3|sw0.006|br0.001|lb16|sl0.015|mh64|cd4|atr10|am3|ex16|mom48|vol48|th0.4|signal`|
|7|SA|1d|79529.20|-16154.83|45.5%|44|-2845.87|Y|`donchian_atr|both|1d|w3|sw0.006|br0.0015|lb16|sl0.015|mh64|cd4|atr14|am3|ex8|mom48|vol48|th0.4|signal`|
|8|SA|1d|79454.28|-25603.92|54.1%|37|4609.01||`donchian_atr|both|1d|w3|sw0.006|br0.0015|lb16|sl0.015|mh64|cd4|atr10|am3|ex16|mom48|vol48|th0.4|signal`|
|9|SA|1d|76106.69|-17288.05|47.7%|44|-3203.46|Y|`donchian_atr|both|1d|w3|sw0.006|br0.0015|lb16|sl0.015|mh64|cd4|atr10|am3|ex8|mom48|vol48|th0.4|signal`|
|10|SA|1d|74784.38|-23417.70|50.0%|40|625.75||`donchian_atr|both|1d|w3|sw0.006|br0.0015|lb16|sl0.015|mh64|cd4|atr10|am3|ex12|mom48|vol48|th0.4|signal`|
|11|SA|1d|73172.42|-24590.27|52.6%|38|4660.33||`donchian_atr|both|1d|w3|sw0.006|br0.0015|lb16|sl0.015|mh64|cd4|atr14|am3|ex16|mom48|vol48|th0.4|signal`|
|12|SA|1d|71627.46|-26338.00|54.3%|35|5852.00||`donchian_atr|both|1d|w3|sw0.006|br0.001|lb16|sl0.015|mh64|cd4|atr10|am3.5|ex16|mom48|vol48|th0.4|signal`|
|13|SA|1d|70087.48|-26338.00|54.3%|35|4832.02||`donchian_atr|both|1d|w3|sw0.006|br0.0015|lb16|sl0.015|mh64|cd4|atr10|am3.5|ex16|mom48|vol48|th0.4|signal`|
|14|SA|1d|66252.39|-23471.57|42.6%|47|1744.88||`donchian_atr|both|1d|w3|sw0.006|br0.0015|lb16|sl0.015|mh64|cd4|atr14|am2.5|ex12|mom48|vol48|th0.4|signal`|
|15|SA|1d|65189.26|-21835.59|48.7%|39|181.54||`donchian_atr|both|1d|w3|sw0.006|br0.0015|lb24|sl0.015|mh64|cd4|atr10|am2.5|ex12|mom48|vol48|th0.4|signal`|
|16|HC|1d|63378.52|-10691.45|58.5%|82|13751.12||`donchian_atr|both|1d|w3|sw0.006|br0.0015|lb16|sl0.015|mh24|cd4|atr14|am3.5|ex16|mom48|vol48|th0.4|signal`|
|17|SA|1d|63275.76|-19835.79|44.7%|47|108.98||`donchian_atr|both|1d|w3|sw0.006|br0.0015|lb16|sl0.015|mh48|cd4|atr10|am2.5|ex12|mom48|vol48|th0.4|signal`|
|18|SA|1d|62736.93|-17876.29|41.2%|51|-2563.39|Y|`donchian_atr|both|1d|w3|sw0.006|br0.0015|lb8|sl0.015|mh64|cd4|atr10|am2.5|ex12|mom48|vol48|th0.4|signal`|
|19|RB|1d|62294.75|-13268.69|30.2%|149|-6451.06|Y|`trend_failure|both|1d|w2|sw0.008|br0.003|lb24|sl0.015|mh32|cd4|aggressive`|
|20|RB|1d|62294.75|-13268.69|30.2%|149|-6451.06|Y|`trend_failure|both|1d|w2|sw0.008|br0.003|lb24|sl0.015|mh32|cd4|signal`|

## Champion 策略

- SP: 启用，净收益 50270.13，样本外 8688.59，交易数 32，策略 `swing_reversal|both|1d|w3|sw0.008|br0.003|lb24|sl0.015|mh64|cd4|strict`。
- SR: 启用，净收益 39703.04，样本外 1534.05，交易数 72，策略 `tsmom_vol|both|1d|w3|sw0.006|br0.002|lb24|sl0.015|mh64|cd4|atr10|am3|ex12|mom48|vol48|th0.4|strict`。
- CJ: 启用，净收益 48234.19，样本外 6333.54，交易数 61，策略 `trend_failure|both|1d|w3|sw0.008|br0.003|lb24|sl0.015|mh32|cd4|signal`。
- UR: 启用，净收益 21397.21，样本外 362.77，交易数 51，策略 `failed_breakout|both|1d|w3|sw0.006|br0.003|lb32|sl0.015|mh32|cd4|strict`。
- FG: 启用，净收益 51337.31，样本外 11772.36，交易数 93，策略 `donchian_atr|both|1d|w3|sw0.006|br0.0015|lb16|sl0.015|mh64|cd4|atr20|am3|ex8|mom48|vol48|th0.4|signal`。
- C: 启用，净收益 22435.99，样本外 14186.96，交易数 154，策略 `trend_failure|both|1d|w3|sw0.004|br0.003|lb24|sl0.015|mh32|cd4|strict`。
- RB: 启用，净收益 51082.21，样本外 956.95，交易数 215，策略 `tsmom_vol|both|1d|w3|sw0.006|br0.002|lb24|sl0.015|mh64|cd4|atr10|am2|ex12|mom16|vol24|th0.4|strict`。
- RM: 启用，净收益 19993.04，样本外 5094.26，交易数 93，策略 `swing_reversal|both|1d|w2|sw0.008|br0.0015|lb24|sl0.015|mh64|cd4|signal`。
- HC: 启用，净收益 63378.52，样本外 13751.12，交易数 82，策略 `donchian_atr|both|1d|w3|sw0.006|br0.0015|lb16|sl0.015|mh24|cd4|atr14|am3.5|ex16|mom48|vol48|th0.4|signal`。
- SA: 启用，净收益 85387.14，样本外 1148.96，交易数 44，策略 `donchian_atr|both|1d|w3|sw0.006|br0.001|lb16|sl0.015|mh64|cd4|atr10|am2.5|ex12|mom48|vol48|th0.4|signal`。
- CS: 启用，净收益 18628.55，样本外 0.00，交易数 4，策略 `vol_breakout|both|1d|w3|sw0.006|br0.0015|lb32|sl0.015|mh64|cd4|atr10|am3|ex16|mom48|vol48|th0.75|strict`。

## 策略画像

### 最高收益
- SP: 净收益 50270.13，胜率 28.1%，交易 32，样本外 8688.59，`swing_reversal|both|1d|w3|sw0.008|br0.003|lb24|sl0.015|mh64|cd4|strict`。
- SR: 净收益 39703.04，胜率 41.7%，交易 72，样本外 1534.05，`tsmom_vol|both|1d|w3|sw0.006|br0.002|lb24|sl0.015|mh64|cd4|atr10|am3|ex12|mom48|vol48|th0.4|strict`。
- CJ: 净收益 48234.19，胜率 14.8%，交易 61，样本外 6333.54，`trend_failure|both|1d|w3|sw0.008|br0.003|lb24|sl0.015|mh32|cd4|signal`。
- UR: 净收益 21397.21，胜率 21.6%，交易 51，样本外 362.77，`failed_breakout|both|1d|w3|sw0.006|br0.003|lb32|sl0.015|mh32|cd4|strict`。
- FG: 净收益 51337.31，胜率 45.2%，交易 93，样本外 11772.36，`donchian_atr|both|1d|w3|sw0.006|br0.0015|lb16|sl0.015|mh64|cd4|atr20|am3|ex8|mom48|vol48|th0.4|signal`。
- C: 净收益 22435.99，胜率 34.4%，交易 154，样本外 14186.96，`trend_failure|both|1d|w3|sw0.004|br0.003|lb24|sl0.015|mh32|cd4|signal`。
- RB: 净收益 51082.21，胜率 44.7%，交易 215，样本外 956.95，`tsmom_vol|both|1d|w3|sw0.006|br0.002|lb24|sl0.015|mh64|cd4|atr10|am2|ex12|mom16|vol24|th0.4|strict`。
- RM: 净收益 19993.04，胜率 15.1%，交易 93，样本外 5094.26，`swing_reversal|both|1d|w2|sw0.008|br0.0015|lb24|sl0.015|mh64|cd4|aggressive`。
- HC: 净收益 63378.52，胜率 58.5%，交易 82，样本外 13751.12，`donchian_atr|both|1d|w3|sw0.006|br0.0015|lb16|sl0.015|mh24|cd4|atr14|am3.5|ex16|mom48|vol48|th0.4|signal`。
- SA: 净收益 85387.14，胜率 45.5%，交易 44，样本外 1148.96，`donchian_atr|both|1d|w3|sw0.006|br0.001|lb16|sl0.015|mh64|cd4|atr10|am2.5|ex12|mom48|vol48|th0.4|signal`。
- CS: 净收益 18628.55，胜率 75.0%，交易 4，样本外 0.00，`vol_breakout|both|1d|w3|sw0.006|br0.0015|lb32|sl0.015|mh64|cd4|atr10|am3|ex16|mom48|vol48|th0.75|strict`。
### 最高胜率
- SP: 净收益 22095.71，胜率 54.5%，交易 22，样本外 4250.61，`vol_breakout|both|1d|w3|sw0.006|br0.0015|lb16|sl0.015|mh32|cd4|atr10|am2|ex16|mom48|vol48|th0.9|aggressive`。
- SR: 净收益 25542.30，胜率 56.5%，交易 23，样本外 9416.87，`tsmom_vol|both|1d|w3|sw0.006|br0.002|lb24|sl0.015|mh64|cd4|atr10|am3.5|ex12|mom24|vol48|th1|strict`。
- CJ: 净收益 4185.25，胜率 65.0%，交易 20，样本外 2076.97，`trend_failure|both|15m|w3|sw0.004|br0.003|lb24|sl0.015|mh32|cd4|strict`。
- UR: 净收益 6069.30，胜率 63.6%，交易 22，样本外 2434.41，`breakout|both|15m|w3|sw0.006|br0.0015|lb16|sl0.015|mh32|cd4|aggressive`。
- FG: 净收益 2073.04，胜率 65.2%，交易 23，样本外 301.15，`tsmom_vol|both|30m|w3|sw0.006|br0.002|lb24|sl0.015|mh32|cd4|atr14|am3|ex12|mom48|vol24|th0.8|strict`。
- C: 净收益 892.26，胜率 60.9%，交易 23，样本外 605.84，`breakout|both|60m|w3|sw0.006|br0.0015|lb16|sl0.015|mh32|cd4|signal`。
- RB: 净收益 19351.45，胜率 60.7%，交易 28，样本外 810.98，`vol_breakout|both|1d|w3|sw0.006|br0.003|lb16|sl0.015|mh32|cd4|atr10|am2|ex8|mom48|vol48|th0.75|strict`。
- RM: 净收益 3943.60，胜率 75.0%，交易 24，样本外 596.97，`donchian_atr|both|30m|w3|sw0.006|br0.0015|lb16|sl0.015|mh24|cd4|atr20|am3.5|ex16|mom48|vol48|th0.4|signal`。
- HC: 净收益 22497.72，胜率 73.1%，交易 26，样本外 8530.67，`donchian_atr|both|1d|w3|sw0.006|br0.001|lb24|sl0.015|mh24|cd4|atr10|am3.5|ex24|mom48|vol48|th0.4|strict`。
- SA: 净收益 5161.92，胜率 72.7%，交易 22，样本外 2930.58，`donchian_atr|both|60m|w3|sw0.006|br0.0015|lb16|sl0.015|mh64|cd4|atr10|am2.5|ex8|mom48|vol48|th0.4|strict`。
- CS: 净收益 1306.11，胜率 65.0%，交易 20，样本外 259.09，`tsmom_vol|both|30m|w3|sw0.006|br0.002|lb24|sl0.015|mh32|cd4|atr14|am3.5|ex12|mom48|vol24|th1|strict`。
### 均衡评分
- SP: 净收益 49457.02，胜率 26.7%，交易 60，样本外 4227.32，`breakout|both|1d|w3|sw0.006|br0.0015|lb16|sl0.015|mh32|cd4|strict`。
- SR: 净收益 34301.00，胜率 43.5%，交易 85，样本外 10822.69，`tsmom_vol|both|1d|w3|sw0.006|br0.002|lb24|sl0.015|mh32|cd4|atr14|am3|ex12|mom48|vol24|th0.3|strict`。
- CJ: 净收益 18187.27，胜率 41.9%，交易 31，样本外 11735.70，`failed_breakout|short|1d|w3|sw0.006|br0.003|lb16|sl0.015|mh32|cd4|strict`。
- UR: 净收益 6463.11，胜率 45.7%，交易 46，样本外 6177.60，`tsmom_vol|both|30m|w3|sw0.006|br0.002|lb24|sl0.015|mh48|cd4|atr10|am2.5|ex12|mom24|vol24|th0.4|strict`。
- FG: 净收益 27719.01，胜率 28.0%，交易 107，样本外 11786.66，`failed_breakout|short|1d|w3|sw0.006|br0.0015|lb16|sl0.015|mh32|cd4|aggressive`。
- C: 净收益 22435.99，胜率 34.4%，交易 154，样本外 14186.96，`trend_failure|both|1d|w3|sw0.004|br0.003|lb24|sl0.015|mh32|cd4|aggressive`。
- RB: 净收益 45192.11，胜率 37.7%，交易 69，样本外 3798.11，`trend_failure|short|1d|w2|sw0.008|br0.003|lb24|sl0.015|mh32|cd4|strict`。
- RM: 净收益 13960.16，胜率 32.9%，交易 76，样本外 3431.77，`failed_breakout|long|1d|w3|sw0.006|br0.003|lb16|sl0.015|mh64|cd4|aggressive`。
- HC: 净收益 39134.98，胜率 45.9%，交易 122，样本外 9012.21，`tsmom_vol|both|1d|w3|sw0.006|br0.002|lb24|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|strict`。
- SA: 净收益 27284.12，胜率 25.0%，交易 44，样本外 13612.33，`failed_breakout|long|1d|w3|sw0.006|br0.0015|lb32|sl0.015|mh32|cd4|aggressive`。
- CS: 净收益 15706.95，胜率 34.5%，交易 87，样本外 18.02，`failed_breakout|both|1d|w3|sw0.006|br0.003|lb16|sl0.015|mh32|cd4|strict`。
### capital_safe
- SP: 净收益 49457.02，胜率 26.7%，交易 60，样本外 4227.32，`breakout|both|1d|w3|sw0.006|br0.0015|lb16|sl0.015|mh32|cd4|strict`。
- SR: 净收益 34301.00，胜率 43.5%，交易 85，样本外 10822.69，`tsmom_vol|both|1d|w3|sw0.006|br0.002|lb24|sl0.015|mh32|cd4|atr14|am3|ex12|mom48|vol24|th0.3|strict`。
- CJ: 净收益 18187.27，胜率 41.9%，交易 31，样本外 11735.70，`failed_breakout|short|1d|w3|sw0.006|br0.003|lb16|sl0.015|mh32|cd4|strict`。
- UR: 净收益 6463.11，胜率 45.7%，交易 46，样本外 6177.60，`tsmom_vol|both|30m|w3|sw0.006|br0.002|lb24|sl0.015|mh48|cd4|atr10|am2.5|ex12|mom24|vol24|th0.4|strict`。
- FG: 净收益 27719.01，胜率 28.0%，交易 107，样本外 11786.66，`failed_breakout|short|1d|w3|sw0.006|br0.0015|lb16|sl0.015|mh32|cd4|aggressive`。
- C: 净收益 22435.99，胜率 34.4%，交易 154，样本外 14186.96，`trend_failure|both|1d|w3|sw0.004|br0.003|lb24|sl0.015|mh32|cd4|aggressive`。
- RB: 净收益 45192.11，胜率 37.7%，交易 69，样本外 3798.11，`trend_failure|short|1d|w2|sw0.008|br0.003|lb24|sl0.015|mh32|cd4|strict`。
- RM: 净收益 13960.16，胜率 32.9%，交易 76，样本外 3431.77，`failed_breakout|long|1d|w3|sw0.006|br0.003|lb16|sl0.015|mh64|cd4|aggressive`。
- HC: 净收益 39134.98，胜率 45.9%，交易 122，样本外 9012.21，`tsmom_vol|both|1d|w3|sw0.006|br0.002|lb24|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|strict`。
- SA: 净收益 27284.12，胜率 25.0%，交易 44，样本外 13612.33，`failed_breakout|long|1d|w3|sw0.006|br0.0015|lb32|sl0.015|mh32|cd4|aggressive`。
- CS: 净收益 15706.95，胜率 34.5%，交易 87，样本外 18.02，`failed_breakout|both|1d|w3|sw0.006|br0.003|lb16|sl0.015|mh32|cd4|strict`。
### safe_winrate
- SP: 净收益 22095.71，胜率 54.5%，交易 22，样本外 4250.61，`vol_breakout|both|1d|w3|sw0.006|br0.0015|lb16|sl0.015|mh32|cd4|atr10|am2|ex16|mom48|vol48|th0.9|aggressive`。
- SR: 净收益 25542.30，胜率 56.5%，交易 23，样本外 9416.87，`tsmom_vol|both|1d|w3|sw0.006|br0.002|lb24|sl0.015|mh64|cd4|atr10|am3.5|ex12|mom24|vol48|th1|strict`。
- CJ: 净收益 4185.25，胜率 65.0%，交易 20，样本外 2076.97，`trend_failure|both|15m|w3|sw0.004|br0.003|lb24|sl0.015|mh32|cd4|strict`。
- UR: 净收益 6069.30，胜率 63.6%，交易 22，样本外 2434.41，`breakout|both|15m|w3|sw0.006|br0.0015|lb16|sl0.015|mh32|cd4|aggressive`。
- FG: 净收益 2073.04，胜率 65.2%，交易 23，样本外 301.15，`tsmom_vol|both|30m|w3|sw0.006|br0.002|lb24|sl0.015|mh32|cd4|atr14|am3|ex12|mom48|vol24|th0.8|strict`。
- C: 净收益 892.26，胜率 60.9%，交易 23，样本外 605.84，`breakout|both|60m|w3|sw0.006|br0.0015|lb16|sl0.015|mh32|cd4|signal`。
- RB: 净收益 19351.45，胜率 60.7%，交易 28，样本外 810.98，`vol_breakout|both|1d|w3|sw0.006|br0.003|lb16|sl0.015|mh32|cd4|atr10|am2|ex8|mom48|vol48|th0.75|strict`。
- RM: 净收益 3943.60，胜率 75.0%，交易 24，样本外 596.97，`donchian_atr|both|30m|w3|sw0.006|br0.0015|lb16|sl0.015|mh24|cd4|atr20|am3.5|ex16|mom48|vol48|th0.4|signal`。
- HC: 净收益 22497.72，胜率 73.1%，交易 26，样本外 8530.67，`donchian_atr|both|1d|w3|sw0.006|br0.001|lb24|sl0.015|mh24|cd4|atr10|am3.5|ex24|mom48|vol48|th0.4|strict`。
- SA: 净收益 5161.92，胜率 72.7%，交易 22，样本外 2930.58，`donchian_atr|both|60m|w3|sw0.006|br0.0015|lb16|sl0.015|mh64|cd4|atr10|am2.5|ex8|mom48|vol48|th0.4|strict`。
- CS: 净收益 1306.11，胜率 65.0%，交易 20，样本外 259.09，`tsmom_vol|both|30m|w3|sw0.006|br0.002|lb24|sl0.015|mh32|cd4|atr14|am3.5|ex12|mom48|vol24|th1|strict`。
### refined_robust
- SP: 净收益 26110.76，胜率 43.5%，交易 23，样本外 7663.77，`donchian_atr|both|1d|w3|sw0.006|br0.0015|lb16|sl0.015|mh48|cd4|atr10|am2|ex16|mom48|vol48|th0.4|strict`。
- SR: 净收益 25542.30，胜率 56.5%，交易 23，样本外 9416.87，`tsmom_vol|both|1d|w3|sw0.006|br0.002|lb24|sl0.015|mh64|cd4|atr10|am3.5|ex12|mom24|vol48|th1|strict`。
- CJ: 净收益 3034.87，胜率 40.5%，交易 37，样本外 4502.56，`tsmom_vol|both|30m|w3|sw0.006|br0.002|lb24|sl0.015|mh32|cd4|atr10|am3.5|ex12|mom24|vol48|th0.6|strict`。
- UR: 净收益 6598.80，胜率 47.7%，交易 44，样本外 4570.48，`tsmom_vol|both|30m|w3|sw0.006|br0.002|lb24|sl0.015|mh48|cd4|atr14|am3.5|ex12|mom24|vol24|th0.3|strict`。
- FG: 净收益 1493.48，胜率 48.1%，交易 27，样本外 568.37，`tsmom_vol|both|30m|w3|sw0.006|br0.002|lb24|sl0.015|mh24|cd4|atr14|am3.5|ex12|mom48|vol24|th0.8|strict`。
- C: 净收益 13972.05，胜率 45.8%，交易 168，样本外 12479.17，`tsmom_vol|both|1d|w3|sw0.006|br0.002|lb24|sl0.015|mh64|cd4|atr20|am3|ex12|mom64|vol48|th0.4|strict`。
- RB: 净收益 50342.90，胜率 42.3%，交易 142，样本外 553.57，`tsmom_vol|both|1d|w3|sw0.006|br0.002|lb24|sl0.015|mh64|cd4|atr10|am2.5|ex12|mom24|vol24|th0.4|strict`。
- RM: 净收益 3943.60，胜率 75.0%，交易 24，样本外 596.97，`donchian_atr|both|30m|w3|sw0.006|br0.0015|lb16|sl0.015|mh24|cd4|atr20|am3.5|ex16|mom48|vol48|th0.4|signal`。
- HC: 净收益 24986.85，胜率 69.0%，交易 29，样本外 8991.68，`donchian_atr|both|1d|w3|sw0.006|br0.001|lb24|sl0.015|mh24|cd4|atr14|am3.2|ex24|mom48|vol48|th0.4|strict`。
- SA: 净收益 5161.92，胜率 72.7%，交易 22，样本外 2930.58，`donchian_atr|both|60m|w3|sw0.006|br0.0015|lb16|sl0.015|mh64|cd4|atr10|am2.5|ex8|mom48|vol48|th0.4|strict`。
- CS: 净收益 1306.11，胜率 65.0%，交易 20，样本外 259.09，`tsmom_vol|both|30m|w3|sw0.006|br0.002|lb24|sl0.015|mh32|cd4|atr14|am3.5|ex12|mom48|vol24|th1|strict`。

## 改进建议

- 当前 top 策略没有明显结构性问题，下一步重点扩大真实行情和新闻事件样本。
