# Walk-Forward 验证报告

- 初始资金: 8500
- 方法: 每个测试窗口只用此前历史选择参数，再在下一窗口测试。
- 画像: `walk_forward`，只把总测试收益为正、正收益窗口不少于一半、测试回撤不超过本金的品种设为 active。

## 汇总

|品种|状态|策略|周期|WF分|测试净收益|正窗口|最差窗口|最差回撤|平均胜率|交易数|
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
|SP|observe|ensemble_trend|1d|43860.0|20133|1/4|0|-3467|25.0%|1|
|RM|observe|ensemble_trend|60m|25208.4|688|4/4|58|-1355|87.5%|5|
|RM|observe|ensemble_trend|1d|22231.9|6494|2/4|-865|-2413|50.0%|6|
|HC|observe|ensemble_trend|1d|18889.0|1131|3/4|-453|-1678|62.5%|5|
|CJ|observe|ensemble_trend|30m|14026.4|1262|2/4|0|-479|37.5%|3|
|SA|observe|ensemble_trend|30m|12538.1|588|2/4|-483|-703|41.7%|5|
|FG|observe|ensemble_trend|1d|11797.7|4623|1/4|-842|-2968|33.3%|7|
|RM|observe|ensemble_trend|30m|10147.8|1526|1/4|-219|-473|31.2%|6|
|SR|observe|ensemble_trend|1d|9862.0|14|2/4|-1135|-1835|50.0%|3|
|CJ|observe|ensemble_trend|60m|9188.4|-770|2/4|-911|-1291|50.0%|4|
|SR|observe|ensemble_trend|60m|7589.1|744|1/4|-325|-345|25.0%|3|
|CS|observe|ensemble_trend|30m|6913.6|372|1/4|-445|-471|25.0%|3|
|RB|observe|ensemble_trend|30m|5895.3|0|1/4|-23|-250|12.5%|3|
|HC|observe|ensemble_trend|60m|5108.9|-350|1/4|-223|-280|25.0%|3|
|CS|observe|ensemble_trend|60m|4210.5|-393|1/4|-183|-453|12.5%|5|
|RB|observe|ensemble_trend|60m|3744.9|-413|1/4|-263|-470|12.5%|4|
|SA|observe|ensemble_trend|60m|3208.3|-349|1/4|-742|-982|25.0%|4|
|UR|observe|ensemble_trend|30m|853.0|-756|1/4|-1164|-1188|12.5%|4|
|RB|observe|ensemble_trend|1d|470.1|-252|1/4|-644|-3195|7.1%|8|
|C|observe|ensemble_trend|60m|119.6|-235|0/4|-172|-302|0.0%|2|
|CS|observe|ensemble_trend|1d|-308.4|-895|1/4|-1389|-1797|12.5%|6|
|C|observe|ensemble_trend|30m|-903.3|-352|0/4|-352|-365|0.0%|1|
|HC|observe|ensemble_trend|30m|-1367.6|-380|0/4|-317|-360|0.0%|3|
|SP|observe|ensemble_trend|60m|-1622.1|-485|0/4|-485|-510|0.0%|1|
|FG|observe|ensemble_trend|60m|-3028.5|-908|0/4|-324|-624|0.0%|4|
|UR|observe|ensemble_trend|1d|-4012.5|-607|0/4|-607|-1291|0.0%|2|
|SR|observe|ensemble_trend|30m|-4095.2|-1111|0/4|-635|-925|0.0%|2|
|SA|observe|ensemble_trend|1d|-4383.6|-502|0/4|-502|-562|0.0%|1|
|FG|observe|ensemble_trend|30m|-4943.2|-1190|0/4|-924|-1344|8.3%|5|
|C|observe|ensemble_trend|1d|-5042.3|-2720|2/4|-3169|-4146|36.8%|23|
|CJ|observe|ensemble_trend|1d|-7514.5|-1429|0/4|-1429|-1479|0.0%|1|
|UR|observe|ensemble_trend|60m|-7922.2|-2638|0/4|-1507|-1752|25.0%|5|
|SP|observe|ensemble_trend|30m|-8106.4|-2145|0/4|-1610|-1660|12.5%|5|

## 每窗口明细

### SP 30m
- 窗口 1: 测试 2026-02-25 10:00:00 至 2026-03-20 09:30:00，净收益 0，回撤 0，胜率 0.0%，`ensemble_trend|both|30m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.3|strict`。
- 窗口 2: 测试 2026-03-20 10:00:00 至 2026-04-15 13:45:00，净收益 -1610，回撤 -1660，胜率 0.0%，`ensemble_trend|both|30m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 3: 测试 2026-04-15 14:15:00 至 2026-05-13 21:30:00，净收益 -485，回撤 -510，胜率 0.0%，`ensemble_trend|both|30m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 4: 测试 2026-05-13 22:00:00 至 2026-06-05 23:00:00，净收益 -50，回撤 -610，胜率 50.0%，`ensemble_trend|both|30m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am3|ex12|mom24|vol24|th0.4|tq0.2|strict`。
### CJ 60m
- 窗口 1: 测试 2025-07-30 11:15:00 至 2025-10-17 10:00:00，净收益 -911，回撤 -1291，胜率 0.0%，`ensemble_trend|both|60m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 2: 测试 2025-10-17 11:15:00 至 2025-12-29 10:00:00，净收益 95，回撤 -1025，胜率 100.0%，`ensemble_trend|both|60m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 3: 测试 2025-12-29 11:15:00 至 2026-03-20 10:00:00，净收益 0，回撤 0，胜率 0.0%，`ensemble_trend|both|60m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 4: 测试 2026-03-20 11:15:00 至 2026-06-05 15:00:00，净收益 45，回撤 -680，胜率 100.0%，`ensemble_trend|both|60m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.2|strict`。
### SR 30m
- 窗口 1: 测试 2026-02-25 10:00:00 至 2026-03-20 09:30:00，净收益 -635，回撤 -925，胜率 0.0%，`ensemble_trend|both|30m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 2: 测试 2026-03-20 10:00:00 至 2026-04-15 13:45:00，净收益 0，回撤 0，胜率 0.0%，`ensemble_trend|both|30m|w3|sw0.006|br0.0015|lb96|sl0.015|mh96|cd4|atr14|am2|ex12|mom48|vol24|th0.4|tq0.3|strict`。
- 窗口 3: 测试 2026-04-15 14:15:00 至 2026-05-13 21:30:00，净收益 -475，回撤 -495，胜率 0.0%，`ensemble_trend|both|30m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 4: 测试 2026-05-13 22:00:00 至 2026-06-05 23:00:00，净收益 0，回撤 0，胜率 0.0%，`ensemble_trend|both|30m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.8|tq0.2|strict`。
### SR 60m
- 窗口 1: 测试 2025-11-10 11:15:00 至 2025-12-26 10:00:00，净收益 1070，回撤 -285，胜率 100.0%，`ensemble_trend|both|60m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 2: 测试 2025-12-26 11:15:00 至 2026-02-24 22:00:00，净收益 -325，回撤 -345，胜率 0.0%，`ensemble_trend|both|60m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 3: 测试 2026-02-24 23:00:00 至 2026-04-15 10:00:00，净收益 0，回撤 0，胜率 0.0%，`ensemble_trend|both|60m|w3|sw0.006|br0.0015|lb96|sl0.015|mh96|cd4|atr14|am2|ex12|mom48|vol24|th0.4|tq0.2|strict`。
- 窗口 4: 测试 2026-04-15 11:15:00 至 2026-06-05 23:00:00，净收益 0，回撤 0，胜率 0.0%，`ensemble_trend|both|60m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.3|strict`。
### SP 60m
- 窗口 1: 测试 2025-11-10 11:15:00 至 2025-12-26 10:00:00，净收益 0，回撤 0，胜率 0.0%，`ensemble_trend|both|60m|w3|sw0.006|br0.0015|lb96|sl0.015|mh96|cd4|atr14|am2|ex12|mom48|vol24|th0.4|tq0.2|strict`。
- 窗口 2: 测试 2025-12-26 11:15:00 至 2026-02-24 22:00:00，净收益 0，回撤 0，胜率 0.0%，`ensemble_trend|both|60m|w3|sw0.006|br0.0015|lb96|sl0.015|mh96|cd4|atr14|am2|ex12|mom48|vol24|th0.4|tq0.2|strict`。
- 窗口 3: 测试 2026-02-24 23:00:00 至 2026-04-15 10:00:00，净收益 0，回撤 0，胜率 0.0%，`ensemble_trend|both|60m|w3|sw0.006|br0.0015|lb96|sl0.015|mh96|cd4|atr14|am2|ex12|mom48|vol24|th0.4|tq0.2|strict`。
- 窗口 4: 测试 2026-04-15 11:15:00 至 2026-06-05 23:00:00，净收益 -485，回撤 -510，胜率 0.0%，`ensemble_trend|both|60m|w3|sw0.006|br0.0015|lb96|sl0.015|mh96|cd4|atr14|am2|ex12|mom48|vol24|th0.4|tq0.3|strict`。
### CJ 1d
- 窗口 1: 测试 2020-09-25 00:00:00 至 2022-03-01 00:00:00，净收益 0，回撤 0，胜率 0.0%，`ensemble_trend|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am2|ex12|mom20|vol24|th0.4|tq0.2|strict`。
- 窗口 2: 测试 2022-03-02 00:00:00 至 2023-07-27 00:00:00，净收益 0，回撤 0，胜率 0.0%，`ensemble_trend|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am2|ex12|mom20|vol24|th0.4|tq0.2|strict`。
- 窗口 3: 测试 2023-07-28 00:00:00 至 2024-12-25 00:00:00，净收益 0，回撤 0，胜率 0.0%，`ensemble_trend|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am2|ex12|mom20|vol24|th0.4|tq0.2|strict`。
- 窗口 4: 测试 2024-12-26 00:00:00 至 2026-06-05 00:00:00，净收益 -1429，回撤 -1479，胜率 0.0%，`ensemble_trend|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am2|ex12|mom20|vol24|th0.4|tq0.2|strict`。
### SP 1d
- 窗口 1: 测试 2020-06-01 00:00:00 至 2021-11-26 00:00:00，净收益 20133，回撤 -3467，胜率 100.0%，`ensemble_trend|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am2|ex12|mom20|vol24|th0.4|tq0.2|strict`。
- 窗口 2: 测试 2021-11-29 00:00:00 至 2023-05-30 00:00:00，净收益 0，回撤 0，胜率 0.0%，`ensemble_trend|both|1d|w3|sw0.006|br0.0015|lb120|sl0.015|mh96|cd4|atr14|am2|ex12|mom40|vol24|th0.4|tq0.2|strict`。
- 窗口 3: 测试 2023-05-31 00:00:00 至 2024-11-28 00:00:00，净收益 0，回撤 0，胜率 0.0%，`ensemble_trend|both|1d|w3|sw0.006|br0.0015|lb120|sl0.015|mh96|cd4|atr14|am2|ex12|mom40|vol24|th0.4|tq0.2|strict`。
- 窗口 4: 测试 2024-11-29 00:00:00 至 2026-06-05 00:00:00，净收益 0，回撤 0，胜率 0.0%，`ensemble_trend|both|1d|w3|sw0.006|br0.0015|lb120|sl0.015|mh96|cd4|atr14|am2|ex12|mom40|vol24|th0.4|tq0.2|strict`。
### CJ 30m
- 窗口 1: 测试 2025-12-29 14:15:00 至 2026-02-05 09:30:00，净收益 0，回撤 0，胜率 0.0%，`ensemble_trend|both|30m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.3|strict`。
- 窗口 2: 测试 2026-02-05 10:00:00 至 2026-03-20 13:45:00，净收益 0，回撤 0，胜率 0.0%，`ensemble_trend|both|30m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 3: 测试 2026-03-20 14:15:00 至 2026-04-28 09:30:00，净收益 1096，回撤 -54，胜率 100.0%，`ensemble_trend|both|30m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 4: 测试 2026-04-28 10:00:00 至 2026-06-05 15:00:00，净收益 166，回撤 -479，胜率 50.0%，`ensemble_trend|both|30m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.2|strict`。
### UR 60m
- 窗口 1: 测试 2025-07-30 11:15:00 至 2025-10-17 10:00:00，净收益 -87，回撤 -447，胜率 50.0%，`ensemble_trend|both|60m|w3|sw0.006|br0.0015|lb96|sl0.015|mh96|cd4|atr14|am2|ex12|mom48|vol24|th0.4|tq0.2|strict`。
- 窗口 2: 测试 2025-10-17 11:15:00 至 2025-12-29 10:00:00，净收益 0，回撤 0，胜率 0.0%，`ensemble_trend|both|60m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 3: 测试 2025-12-29 11:15:00 至 2026-03-20 10:00:00，净收益 -1044，回撤 -1164，胜率 0.0%，`ensemble_trend|both|60m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 4: 测试 2026-03-20 11:15:00 至 2026-06-05 15:00:00，净收益 -1507，回撤 -1752，胜率 50.0%，`ensemble_trend|both|60m|w3|sw0.006|br0.0015|lb96|sl0.015|mh96|cd4|atr14|am3|ex12|mom48|vol24|th0.8|tq0.2|strict`。
### UR 30m
- 窗口 1: 测试 2025-12-29 14:15:00 至 2026-02-05 09:30:00，净收益 0，回撤 0，胜率 0.0%，`ensemble_trend|both|30m|w3|sw0.006|br0.0015|lb96|sl0.015|mh96|cd4|atr14|am2|ex12|mom48|vol24|th0.4|tq0.3|strict`。
- 窗口 2: 测试 2026-02-05 10:00:00 至 2026-03-20 13:45:00，净收益 -1164，回撤 -1188，胜率 0.0%，`ensemble_trend|both|30m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am3|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 3: 测试 2026-03-20 14:15:00 至 2026-04-28 09:30:00，净收益 752，回撤 -1112，胜率 50.0%，`ensemble_trend|both|30m|w3|sw0.006|br0.0015|lb96|sl0.015|mh96|cd4|atr14|am3|ex12|mom48|vol24|th0.4|tq0.2|strict`。
- 窗口 4: 测试 2026-04-28 10:00:00 至 2026-06-05 15:00:00，净收益 -344，回撤 -600，胜率 0.0%，`ensemble_trend|both|30m|w3|sw0.006|br0.0015|lb96|sl0.015|mh96|cd4|atr14|am3|ex12|mom48|vol24|th0.8|tq0.3|strict`。
### UR 1d
- 窗口 1: 测试 2020-12-18 00:00:00 至 2022-04-29 00:00:00，净收益 0，回撤 0，胜率 0.0%，`ensemble_trend|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am2|ex12|mom20|vol24|th0.4|tq0.2|strict`。
- 窗口 2: 测试 2022-05-05 00:00:00 至 2023-09-05 00:00:00，净收益 0，回撤 0，胜率 0.0%，`ensemble_trend|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am2|ex12|mom20|vol24|th0.4|tq0.2|strict`。
- 窗口 3: 测试 2023-09-06 00:00:00 至 2025-01-16 00:00:00，净收益 -607，回撤 -1291，胜率 0.0%，`ensemble_trend|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am2|ex12|mom20|vol24|th0.4|tq0.2|strict`。
- 窗口 4: 测试 2025-01-17 00:00:00 至 2026-06-05 00:00:00，净收益 0，回撤 0，胜率 0.0%，`ensemble_trend|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am2|ex12|mom20|vol24|th0.4|tq0.3|strict`。
### FG 60m
- 窗口 1: 测试 2025-11-10 11:15:00 至 2025-12-26 10:00:00，净收益 0，回撤 0，胜率 0.0%，`ensemble_trend|both|60m|w3|sw0.006|br0.0015|lb96|sl0.015|mh96|cd4|atr14|am2|ex12|mom48|vol24|th0.4|tq0.2|strict`。
- 窗口 2: 测试 2025-12-26 11:15:00 至 2026-02-24 22:00:00，净收益 -262，回撤 -284，胜率 0.0%，`ensemble_trend|both|60m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 3: 测试 2026-02-24 23:00:00 至 2026-04-15 10:00:00，净收益 -324，回撤 -624，胜率 0.0%，`ensemble_trend|both|60m|w3|sw0.006|br0.0015|lb96|sl0.015|mh96|cd4|atr14|am2|ex12|mom48|vol24|th0.4|tq0.2|strict`。
- 窗口 4: 测试 2026-04-15 11:15:00 至 2026-06-05 23:00:00，净收益 -322，回撤 -344，胜率 0.0%，`ensemble_trend|both|60m|w3|sw0.006|br0.0015|lb96|sl0.015|mh96|cd4|atr14|am2|ex12|mom48|vol24|th0.4|tq0.2|strict`。
### FG 30m
- 窗口 1: 测试 2026-02-25 10:00:00 至 2026-03-20 09:30:00，净收益 -924，回撤 -1344，胜率 0.0%，`ensemble_trend|both|30m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 2: 测试 2026-03-20 10:00:00 至 2026-04-15 13:45:00，净收益 -266，回撤 -386，胜率 33.3%，`ensemble_trend|both|30m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.3|strict`。
- 窗口 3: 测试 2026-04-15 14:15:00 至 2026-05-13 21:30:00，净收益 0，回撤 0，胜率 0.0%，`ensemble_trend|both|30m|w3|sw0.006|br0.0015|lb96|sl0.015|mh96|cd4|atr14|am3|ex12|mom48|vol24|th0.4|tq0.2|strict`。
- 窗口 4: 测试 2026-05-13 22:00:00 至 2026-06-05 23:00:00，净收益 0，回撤 0，胜率 0.0%，`ensemble_trend|both|30m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am3|ex12|mom24|vol24|th0.4|tq0.3|strict`。
### C 60m
- 窗口 1: 测试 2025-11-10 11:15:00 至 2025-12-26 10:00:00，净收益 -172，回撤 -302，胜率 0.0%，`ensemble_trend|both|60m|w3|sw0.006|br0.0015|lb96|sl0.015|mh96|cd4|atr14|am2|ex12|mom48|vol24|th0.4|tq0.2|strict`。
- 窗口 2: 测试 2025-12-26 11:15:00 至 2026-02-24 22:00:00，净收益 -62，回撤 -142，胜率 0.0%，`ensemble_trend|both|60m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.3|strict`。
- 窗口 3: 测试 2026-02-24 23:00:00 至 2026-04-15 10:00:00，净收益 0，回撤 0，胜率 0.0%，`ensemble_trend|both|60m|w3|sw0.006|br0.0015|lb96|sl0.015|mh96|cd4|atr14|am2|ex12|mom48|vol24|th0.4|tq0.2|strict`。
- 窗口 4: 测试 2026-04-15 11:15:00 至 2026-06-05 23:00:00，净收益 0，回撤 0，胜率 0.0%，`ensemble_trend|both|60m|w3|sw0.006|br0.0015|lb96|sl0.015|mh96|cd4|atr14|am2|ex12|mom48|vol24|th0.4|tq0.3|strict`。
### C 30m
- 窗口 1: 测试 2026-02-25 10:00:00 至 2026-03-20 09:30:00，净收益 -352，回撤 -365，胜率 0.0%，`ensemble_trend|both|30m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am3|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 2: 测试 2026-03-20 10:00:00 至 2026-04-15 13:45:00，净收益 0，回撤 0，胜率 0.0%，`ensemble_trend|both|30m|w3|sw0.006|br0.0015|lb96|sl0.015|mh96|cd4|atr14|am3|ex12|mom48|vol24|th0.4|tq0.2|strict`。
- 窗口 3: 测试 2026-04-15 14:15:00 至 2026-05-13 21:30:00，净收益 0，回撤 0，胜率 0.0%，`ensemble_trend|both|30m|w3|sw0.006|br0.0015|lb96|sl0.015|mh96|cd4|atr14|am3|ex12|mom48|vol24|th0.4|tq0.2|strict`。
- 窗口 4: 测试 2026-05-13 22:00:00 至 2026-06-05 23:00:00，净收益 0，回撤 0，胜率 0.0%，`ensemble_trend|both|30m|w3|sw0.006|br0.0015|lb96|sl0.015|mh96|cd4|atr14|am2|ex12|mom48|vol24|th0.4|tq0.3|strict`。
### RB 60m
- 窗口 1: 测试 2025-11-10 11:15:00 至 2025-12-26 10:00:00，净收益 0，回撤 0，胜率 0.0%，`ensemble_trend|both|60m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 2: 测试 2025-12-26 11:15:00 至 2026-02-24 22:00:00，净收益 -263，回撤 -276，胜率 0.0%，`ensemble_trend|both|60m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 3: 测试 2026-02-24 23:00:00 至 2026-04-15 10:00:00，净收益 -203，回撤 -243，胜率 0.0%，`ensemble_trend|both|60m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 4: 测试 2026-04-15 11:15:00 至 2026-06-05 23:00:00，净收益 54，回撤 -470，胜率 50.0%，`ensemble_trend|both|60m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.2|strict`。
### RB 30m
- 窗口 1: 测试 2026-02-25 10:00:00 至 2026-03-20 09:30:00，净收益 -23，回撤 -113，胜率 0.0%，`ensemble_trend|both|30m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 2: 测试 2026-03-20 10:00:00 至 2026-04-15 13:45:00，净收益 0，回撤 0，胜率 0.0%，`ensemble_trend|both|30m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 3: 测试 2026-04-15 14:15:00 至 2026-05-13 21:30:00，净收益 24，回撤 -250，胜率 50.0%，`ensemble_trend|both|30m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 4: 测试 2026-05-13 22:00:00 至 2026-06-05 23:00:00，净收益 0，回撤 0，胜率 0.0%，`ensemble_trend|both|30m|w3|sw0.006|br0.0015|lb96|sl0.015|mh96|cd4|atr14|am3|ex12|mom48|vol24|th0.8|tq0.2|strict`。
### RM 60m
- 窗口 1: 测试 2025-11-10 11:15:00 至 2025-12-26 10:00:00，净收益 148，回撤 -272，胜率 100.0%，`ensemble_trend|both|60m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 2: 测试 2025-12-26 11:15:00 至 2026-02-24 22:00:00，净收益 248，回撤 -432，胜率 100.0%，`ensemble_trend|both|60m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am3|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 3: 测试 2026-02-24 23:00:00 至 2026-04-15 10:00:00，净收益 235，回撤 -1355，胜率 50.0%，`ensemble_trend|both|60m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am3|ex12|mom24|vol24|th0.8|tq0.2|strict`。
- 窗口 4: 测试 2026-04-15 11:15:00 至 2026-06-05 23:00:00，净收益 58，回撤 -52，胜率 100.0%，`ensemble_trend|both|60m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am3|ex12|mom24|vol24|th0.8|tq0.2|strict`。
### FG 1d
- 窗口 1: 测试 2015-08-17 00:00:00 至 2018-04-26 00:00:00，净收益 -842，回撤 -902，胜率 0.0%，`ensemble_trend|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am2|ex12|mom20|vol24|th0.4|tq0.2|strict`。
- 窗口 2: 测试 2018-04-27 00:00:00 至 2021-01-05 00:00:00，净收益 5831，回撤 -2180，胜率 66.7%，`ensemble_trend|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am2|ex12|mom20|vol24|th0.4|tq0.2|strict`。
- 窗口 3: 测试 2021-01-06 00:00:00 至 2023-09-12 00:00:00，净收益 0，回撤 0，胜率 0.0%，`ensemble_trend|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am2|ex12|mom20|vol24|th0.4|tq0.2|strict`。
- 窗口 4: 测试 2023-09-13 00:00:00 至 2026-06-05 00:00:00，净收益 -366，回撤 -2968，胜率 66.7%，`ensemble_trend|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am2|ex12|mom20|vol24|th0.4|tq0.2|strict`。
### RM 30m
- 窗口 1: 测试 2026-02-25 10:00:00 至 2026-03-20 09:30:00，净收益 1745，回撤 -473，胜率 100.0%，`ensemble_trend|both|30m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 2: 测试 2026-03-20 10:00:00 至 2026-04-15 13:45:00，净收益 -219，回撤 -417，胜率 25.0%，`ensemble_trend|both|30m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 3: 测试 2026-04-15 14:15:00 至 2026-05-13 21:30:00，净收益 0，回撤 0，胜率 0.0%，`ensemble_trend|both|30m|w3|sw0.006|br0.0015|lb96|sl0.015|mh96|cd4|atr14|am3|ex12|mom48|vol24|th0.4|tq0.2|strict`。
- 窗口 4: 测试 2026-05-13 22:00:00 至 2026-06-05 23:00:00，净收益 0，回撤 0，胜率 0.0%，`ensemble_trend|both|30m|w3|sw0.006|br0.0015|lb96|sl0.015|mh96|cd4|atr14|am3|ex12|mom48|vol24|th0.4|tq0.2|strict`。
### HC 60m
- 窗口 1: 测试 2025-11-10 11:15:00 至 2025-12-26 10:00:00，净收益 0，回撤 0，胜率 0.0%，`ensemble_trend|both|60m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 2: 测试 2025-12-26 11:15:00 至 2026-02-24 22:00:00，净收益 -223，回撤 -236，胜率 0.0%，`ensemble_trend|both|60m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 3: 测试 2026-02-24 23:00:00 至 2026-04-15 10:00:00，净收益 -163，回撤 -233，胜率 0.0%，`ensemble_trend|both|60m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.3|strict`。
- 窗口 4: 测试 2026-04-15 11:15:00 至 2026-06-05 23:00:00，净收益 37，回撤 -280，胜率 100.0%，`ensemble_trend|both|60m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.3|strict`。
### SR 1d
- 窗口 1: 测试 2010-01-29 00:00:00 至 2014-03-11 00:00:00，净收益 -1135，回撤 -1150，胜率 0.0%，`ensemble_trend|both|1d|w3|sw0.006|br0.0015|lb120|sl0.015|mh96|cd4|atr14|am2|ex12|mom40|vol24|th0.4|tq0.2|strict`。
- 窗口 2: 测试 2014-03-12 00:00:00 至 2018-03-28 00:00:00，净收益 324，回撤 -990，胜率 100.0%，`ensemble_trend|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am3|ex12|mom20|vol24|th0.4|tq0.2|strict`。
- 窗口 3: 测试 2018-03-29 00:00:00 至 2022-04-28 00:00:00，净收益 0，回撤 0，胜率 0.0%，`ensemble_trend|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am3|ex12|mom20|vol24|th0.4|tq0.2|strict`。
- 窗口 4: 测试 2022-04-29 00:00:00 至 2026-06-05 00:00:00，净收益 825，回撤 -1835，胜率 100.0%，`ensemble_trend|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am2|ex12|mom20|vol24|th0.4|tq0.3|strict`。
### HC 30m
- 窗口 1: 测试 2026-02-25 10:00:00 至 2026-03-20 09:30:00，净收益 -63，回撤 -173，胜率 0.0%，`ensemble_trend|both|30m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am3|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 2: 测试 2026-03-20 10:00:00 至 2026-04-15 13:45:00，净收益 0，回撤 0，胜率 0.0%，`ensemble_trend|both|30m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am3|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 3: 测试 2026-04-15 14:15:00 至 2026-05-13 21:30:00，净收益 -317，回撤 -360，胜率 0.0%，`ensemble_trend|both|30m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am3|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 4: 测试 2026-05-13 22:00:00 至 2026-06-05 23:00:00，净收益 0，回撤 0，胜率 0.0%，`ensemble_trend|both|30m|w3|sw0.006|br0.0015|lb96|sl0.015|mh96|cd4|atr14|am3|ex12|mom48|vol24|th0.8|tq0.2|strict`。
### SA 60m
- 窗口 1: 测试 2025-11-10 11:15:00 至 2025-12-26 10:00:00，净收益 -742，回撤 -982，胜率 0.0%，`ensemble_trend|both|60m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 2: 测试 2025-12-26 11:15:00 至 2026-02-24 22:00:00，净收益 -302，回撤 -622，胜率 0.0%，`ensemble_trend|both|60m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am3|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 3: 测试 2026-02-24 23:00:00 至 2026-04-15 10:00:00，净收益 898，回撤 -322，胜率 100.0%，`ensemble_trend|both|60m|w3|sw0.006|br0.0015|lb96|sl0.015|mh96|cd4|atr14|am2|ex12|mom48|vol24|th0.4|tq0.2|strict`。
- 窗口 4: 测试 2026-04-15 11:15:00 至 2026-06-05 23:00:00，净收益 -202，回撤 -242，胜率 0.0%，`ensemble_trend|both|60m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.2|strict`。
### SA 30m
- 窗口 1: 测试 2026-02-25 10:00:00 至 2026-03-20 09:30:00，净收益 -483，回撤 -703，胜率 0.0%，`ensemble_trend|both|30m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.3|strict`。
- 窗口 2: 测试 2026-03-20 10:00:00 至 2026-04-15 13:45:00，净收益 913，回撤 -385，胜率 66.7%，`ensemble_trend|both|30m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 3: 测试 2026-04-15 14:15:00 至 2026-05-13 21:30:00，净收益 0，回撤 0，胜率 0.0%，`ensemble_trend|both|30m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am3|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 4: 测试 2026-05-13 22:00:00 至 2026-06-05 23:00:00，净收益 158，回撤 -80，胜率 100.0%，`ensemble_trend|both|30m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am3|ex12|mom24|vol24|th0.4|tq0.2|strict`。
### SA 1d
- 窗口 1: 测试 2021-03-25 00:00:00 至 2022-07-11 00:00:00，净收益 0，回撤 0，胜率 0.0%，`ensemble_trend|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am2|ex12|mom20|vol24|th0.4|tq0.2|strict`。
- 窗口 2: 测试 2022-07-12 00:00:00 至 2023-10-26 00:00:00，净收益 0，回撤 0，胜率 0.0%，`ensemble_trend|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am2|ex12|mom20|vol24|th0.4|tq0.2|strict`。
- 窗口 3: 测试 2023-10-27 00:00:00 至 2025-02-14 00:00:00，净收益 0，回撤 0，胜率 0.0%，`ensemble_trend|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am2|ex12|mom20|vol24|th0.4|tq0.2|strict`。
- 窗口 4: 测试 2025-02-17 00:00:00 至 2026-06-05 00:00:00，净收益 -502，回撤 -562，胜率 0.0%，`ensemble_trend|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am2|ex12|mom20|vol24|th0.4|tq0.2|strict`。
### RM 1d
- 窗口 1: 测试 2015-09-10 00:00:00 至 2018-05-15 00:00:00，净收益 2025，回撤 -2413，胜率 100.0%，`ensemble_trend|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am2|ex12|mom20|vol24|th0.4|tq0.2|strict`。
- 窗口 2: 测试 2018-05-16 00:00:00 至 2021-01-15 00:00:00，净收益 5334，回撤 -603，胜率 100.0%，`ensemble_trend|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am2|ex12|mom20|vol24|th0.4|tq0.2|strict`。
- 窗口 3: 测试 2021-01-18 00:00:00 至 2023-09-20 00:00:00，净收益 0，回撤 0，胜率 0.0%，`ensemble_trend|both|1d|w3|sw0.006|br0.0015|lb120|sl0.015|mh96|cd4|atr14|am2|ex12|mom40|vol24|th0.4|tq0.2|strict`。
- 窗口 4: 测试 2023-09-21 00:00:00 至 2026-06-05 00:00:00，净收益 -865，回撤 -1165，胜率 0.0%，`ensemble_trend|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am2|ex12|mom20|vol24|th0.4|tq0.2|strict`。
### HC 1d
- 窗口 1: 测试 2016-08-17 00:00:00 至 2019-01-22 00:00:00，净收益 33，回撤 -1678，胜率 50.0%，`ensemble_trend|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am2|ex12|mom20|vol24|th0.4|tq0.2|strict`。
- 窗口 2: 测试 2019-01-23 00:00:00 至 2021-07-07 00:00:00，净收益 1246，回撤 -1270，胜率 100.0%，`ensemble_trend|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am3|ex12|mom20|vol24|th0.4|tq0.2|strict`。
- 窗口 3: 测试 2021-07-08 00:00:00 至 2023-12-15 00:00:00，净收益 306，回撤 -1570，胜率 100.0%，`ensemble_trend|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am3|ex12|mom20|vol24|th0.4|tq0.2|strict`。
- 窗口 4: 测试 2023-12-18 00:00:00 至 2026-06-05 00:00:00，净收益 -453，回撤 -623，胜率 0.0%，`ensemble_trend|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am3|ex12|mom20|vol24|th0.4|tq0.2|strict`。
### RB 1d
- 窗口 1: 测试 2012-08-28 00:00:00 至 2016-02-05 00:00:00，净收益 392，回撤 -3195，胜率 28.6%，`ensemble_trend|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am3|ex12|mom20|vol24|th0.4|tq0.2|strict`。
- 窗口 2: 测试 2016-02-15 00:00:00 至 2019-07-12 00:00:00，净收益 -644，回撤 -659，胜率 0.0%，`ensemble_trend|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am2|ex12|mom20|vol24|th0.4|tq0.3|strict`。
- 窗口 3: 测试 2019-07-15 00:00:00 至 2022-12-16 00:00:00，净收益 0，回撤 0，胜率 0.0%，`ensemble_trend|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am3|ex12|mom20|vol24|th0.4|tq0.3|strict`。
- 窗口 4: 测试 2022-12-19 00:00:00 至 2026-06-05 00:00:00，净收益 0，回撤 0，胜率 0.0%，`ensemble_trend|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am3|ex12|mom20|vol24|th0.4|tq0.3|strict`。
### CS 60m
- 窗口 1: 测试 2025-11-10 11:15:00 至 2025-12-26 10:00:00，净收益 -162，回撤 -175，胜率 0.0%，`ensemble_trend|both|60m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.3|strict`。
- 窗口 2: 测试 2025-12-26 11:15:00 至 2026-02-24 22:00:00，净收益 55，回撤 -358，胜率 50.0%，`ensemble_trend|both|60m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 3: 测试 2026-02-24 23:00:00 至 2026-04-15 10:00:00，净收益 -103，回撤 -453，胜率 0.0%，`ensemble_trend|both|60m|w3|sw0.006|br0.0015|lb96|sl0.015|mh96|cd4|atr14|am3|ex12|mom48|vol24|th0.4|tq0.2|strict`。
- 窗口 4: 测试 2026-04-15 11:15:00 至 2026-06-05 23:00:00，净收益 -183，回撤 -280，胜率 0.0%，`ensemble_trend|both|60m|w3|sw0.006|br0.0015|lb96|sl0.015|mh96|cd4|atr14|am3|ex12|mom48|vol24|th0.4|tq0.2|strict`。
### CS 30m
- 窗口 1: 测试 2026-02-25 10:00:00 至 2026-03-20 09:30:00，净收益 -445，回撤 -471，胜率 0.0%，`ensemble_trend|both|30m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 2: 测试 2026-03-20 10:00:00 至 2026-04-15 13:45:00，净收益 0，回撤 0，胜率 0.0%，`ensemble_trend|both|30m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am3|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 3: 测试 2026-04-15 14:15:00 至 2026-05-13 21:30:00，净收益 817，回撤 -93，胜率 100.0%，`ensemble_trend|both|30m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am3|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 4: 测试 2026-05-13 22:00:00 至 2026-06-05 23:00:00，净收益 0，回撤 0，胜率 0.0%，`ensemble_trend|both|30m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am3|ex12|mom24|vol24|th0.4|tq0.2|strict`。
### C 1d
- 窗口 1: 测试 2009-04-13 00:00:00 至 2013-07-24 00:00:00，净收益 1445，回撤 -2554，胜率 57.1%，`ensemble_trend|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am3|ex12|mom20|vol24|th0.8|tq0.2|strict`。
- 窗口 2: 测试 2013-07-25 00:00:00 至 2017-11-01 00:00:00，净收益 -3169，回撤 -4146，胜率 40.0%，`ensemble_trend|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am3|ex12|mom20|vol24|th0.8|tq0.2|strict`。
- 窗口 3: 测试 2017-11-02 00:00:00 至 2022-02-16 00:00:00，净收益 921，回撤 -1601，胜率 50.0%，`ensemble_trend|both|1d|w3|sw0.006|br0.0015|lb120|sl0.015|mh96|cd4|atr14|am2|ex12|mom40|vol24|th0.4|tq0.2|strict`。
- 窗口 4: 测试 2022-02-17 00:00:00 至 2026-06-05 00:00:00，净收益 -1917，回撤 -1954，胜率 0.0%，`ensemble_trend|both|1d|w3|sw0.006|br0.0015|lb120|sl0.015|mh96|cd4|atr14|am2|ex12|mom40|vol24|th0.8|tq0.2|strict`。
### CS 1d
- 窗口 1: 测试 2017-04-07 00:00:00 至 2019-07-17 00:00:00，净收益 -1389，回撤 -1797，胜率 0.0%，`ensemble_trend|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am2|ex12|mom20|vol24|th0.4|tq0.2|strict`。
- 窗口 2: 测试 2019-07-18 00:00:00 至 2021-11-02 00:00:00，净收益 494，回撤 -990，胜率 50.0%，`ensemble_trend|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am2|ex12|mom20|vol24|th0.4|tq0.3|strict`。
- 窗口 3: 测试 2021-11-03 00:00:00 至 2024-02-19 00:00:00，净收益 0，回撤 0，胜率 0.0%，`ensemble_trend|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am2|ex12|mom20|vol24|th0.4|tq0.3|strict`。
- 窗口 4: 测试 2024-02-20 00:00:00 至 2026-06-05 00:00:00，净收益 0，回撤 0，胜率 0.0%，`ensemble_trend|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am2|ex12|mom20|vol24|th0.4|tq0.3|strict`。
