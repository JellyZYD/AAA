# Walk-Forward 验证报告

- 初始资金: 8500
- 方法: 每个测试窗口只用此前历史选择参数，再在下一窗口测试。
- 画像: `walk_forward`，只把总测试收益为正、正收益窗口不少于一半、测试回撤不超过本金的品种设为 active。

## 汇总

|品种|状态|策略|周期|WF分|测试净收益|正窗口|最差窗口|最差回撤|平均胜率|交易数|
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
|RM|observe|trend_pullback|60m|25101.4|688|4/4|58|-1355|87.5%|5|
|CS|observe|trend_pullback|30m|16242.7|1195|2/4|0|-123|50.0%|2|
|SA|observe|trend_pullback|30m|15225.5|1211|2/4|0|-385|41.7%|4|
|CS|observe|trend_pullback|60m|12296.0|17|2/4|-162|-358|37.5%|5|
|RB|observe|trend_pullback|1d|11025.2|2461|1/4|0|-955|18.8%|4|
|RM|observe|trend_pullback|30m|10013.2|1636|1/4|-67|-680|25.0%|6|
|SR|observe|trend_pullback|60m|8044.0|744|1/4|-325|-345|25.0%|3|
|C|observe|trend_pullback|1d|7865.9|525|2/4|-635|-3754|41.7%|16|
|CJ|observe|trend_pullback|30m|7388.4|832|1/4|-264|-668|33.3%|4|
|SP|observe|trend_pullback|60m|6879.8|395|1/4|0|-485|25.0%|1|
|C|observe|trend_pullback|30m|6839.1|75|1/4|-192|-205|25.0%|2|
|FG|observe|trend_pullback|30m|5475.9|236|1/4|0|-644|12.5%|2|
|UR|observe|trend_pullback|30m|5415.6|-451|1/4|-344|-624|25.0%|3|
|FG|observe|trend_pullback|1d|5376.1|17|1/4|0|-783|25.0%|1|
|UR|observe|trend_pullback|60m|4953.8|26|1/4|-527|-830|25.0%|4|
|RB|observe|trend_pullback|30m|4773.5|-153|1/4|-176|-250|12.5%|4|
|HC|observe|trend_pullback|30m|4596.2|-544|1/4|-363|-543|25.0%|4|
|HC|observe|trend_pullback|60m|4523.0|-423|1/4|-267|-357|25.0%|4|
|SP|observe|trend_pullback|30m|3859.3|-545|1/4|-485|-755|25.0%|5|
|CJ|observe|trend_pullback|60m|3404.4|-689|1/4|-454|-680|25.0%|3|
|RB|observe|trend_pullback|60m|3390.7|-433|1/4|-283|-470|12.5%|4|
|SA|observe|trend_pullback|60m|2354.8|-409|1/4|-1105|-1149|25.0%|4|
|SR|observe|trend_pullback|1d|343.9|0|0/4|0|0|0.0%|0|
|C|observe|trend_pullback|60m|72.0|-235|0/4|-172|-302|0.0%|2|
|SP|observe|trend_pullback|1d|-1700.0|0|0/4|0|0|0.0%|0|
|SA|observe|trend_pullback|1d|-1700.0|0|0/4|0|0|0.0%|0|
|UR|observe|trend_pullback|1d|-1700.0|0|0/4|0|0|0.0%|0|
|CJ|observe|trend_pullback|1d|-1700.0|0|0/4|0|0|0.0%|0|
|FG|observe|trend_pullback|60m|-2615.0|-646|0/4|-324|-624|0.0%|3|
|HC|observe|trend_pullback|1d|-2663.3|-634|0/4|-634|-950|0.0%|1|
|SR|observe|trend_pullback|30m|-4112.9|-941|0/4|-635|-925|0.0%|2|
|RM|observe|trend_pullback|1d|-4118.1|-832|0/4|-832|-1122|0.0%|1|
|CS|observe|trend_pullback|1d|-8729.5|-2025|0/4|-1522|-1941|0.0%|6|

## 每窗口明细

### SR 60m
- 窗口 1: 测试 2025-11-10 11:15:00 至 2025-12-26 10:00:00，净收益 1070，回撤 -285，胜率 100.0%，`trend_pullback|both|60m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 2: 测试 2025-12-26 11:15:00 至 2026-02-24 22:00:00，净收益 -325，回撤 -345，胜率 0.0%，`trend_pullback|both|60m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 3: 测试 2026-02-24 23:00:00 至 2026-04-15 10:00:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|60m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.3|strict`。
- 窗口 4: 测试 2026-04-15 11:15:00 至 2026-06-05 23:00:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|60m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.3|strict`。
### SP 30m
- 窗口 1: 测试 2026-02-25 10:00:00 至 2026-03-20 09:30:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|30m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.3|strict`。
- 窗口 2: 测试 2026-03-20 10:00:00 至 2026-04-15 13:45:00，净收益 -130，回撤 -755，胜率 50.0%，`trend_pullback|both|30m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 3: 测试 2026-04-15 14:15:00 至 2026-05-13 21:30:00，净收益 -485，回撤 -510，胜率 0.0%，`trend_pullback|both|30m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 4: 测试 2026-05-13 22:00:00 至 2026-06-05 23:00:00，净收益 70，回撤 -435，胜率 50.0%，`trend_pullback|both|30m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.2|strict`。
### SR 30m
- 窗口 1: 测试 2026-02-25 10:00:00 至 2026-03-20 09:30:00，净收益 -635，回撤 -925，胜率 0.0%，`trend_pullback|both|30m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 2: 测试 2026-03-20 10:00:00 至 2026-04-15 13:45:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|30m|w3|sw0.006|br0.0015|lb96|sl0.015|mh96|cd4|atr14|am2|ex12|mom48|vol24|th0.4|tq0.3|strict`。
- 窗口 3: 测试 2026-04-15 14:15:00 至 2026-05-13 21:30:00，净收益 -305，回撤 -355，胜率 0.0%，`trend_pullback|both|30m|w3|sw0.006|br0.0015|lb96|sl0.015|mh96|cd4|atr14|am2|ex12|mom48|vol24|th0.4|tq0.2|strict`。
- 窗口 4: 测试 2026-05-13 22:00:00 至 2026-06-05 23:00:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|30m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.2|strict`。
### SP 60m
- 窗口 1: 测试 2025-11-10 11:15:00 至 2025-12-26 10:00:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|60m|w3|sw0.006|br0.0015|lb96|sl0.015|mh96|cd4|atr14|am2|ex12|mom48|vol24|th0.4|tq0.2|strict`。
- 窗口 2: 测试 2025-12-26 11:15:00 至 2026-02-24 22:00:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|60m|w3|sw0.006|br0.0015|lb96|sl0.015|mh96|cd4|atr14|am2|ex12|mom48|vol24|th0.4|tq0.2|strict`。
- 窗口 3: 测试 2026-02-24 23:00:00 至 2026-04-15 10:00:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|60m|w3|sw0.006|br0.0015|lb96|sl0.015|mh96|cd4|atr14|am2|ex12|mom48|vol24|th0.4|tq0.2|strict`。
- 窗口 4: 测试 2026-04-15 11:15:00 至 2026-06-05 23:00:00，净收益 395，回撤 -485，胜率 100.0%，`trend_pullback|both|60m|w3|sw0.006|br0.0015|lb96|sl0.015|mh96|cd4|atr14|am2|ex12|mom48|vol24|th0.4|tq0.2|strict`。
### CJ 60m
- 窗口 1: 测试 2025-07-30 11:15:00 至 2025-10-17 10:00:00，净收益 -280，回撤 -605，胜率 0.0%，`trend_pullback|both|60m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 2: 测试 2025-10-17 11:15:00 至 2025-12-29 10:00:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|60m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.3|strict`。
- 窗口 3: 测试 2025-12-29 11:15:00 至 2026-03-20 10:00:00，净收益 -454，回撤 -629，胜率 0.0%，`trend_pullback|both|60m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 4: 测试 2026-03-20 11:15:00 至 2026-06-05 15:00:00，净收益 45，回撤 -680，胜率 100.0%，`trend_pullback|both|60m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.2|strict`。
### CJ 1d
- 窗口 1: 测试 2020-09-25 00:00:00 至 2022-03-01 00:00:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am2|ex12|mom20|vol24|th0.4|tq0.2|strict`。
- 窗口 2: 测试 2022-03-02 00:00:00 至 2023-07-27 00:00:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am2|ex12|mom20|vol24|th0.4|tq0.2|strict`。
- 窗口 3: 测试 2023-07-28 00:00:00 至 2024-12-25 00:00:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am2|ex12|mom20|vol24|th0.4|tq0.2|strict`。
- 窗口 4: 测试 2024-12-26 00:00:00 至 2026-06-05 00:00:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am2|ex12|mom20|vol24|th0.4|tq0.2|strict`。
### SP 1d
- 窗口 1: 测试 2020-06-01 00:00:00 至 2021-11-26 00:00:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am2|ex12|mom20|vol24|th0.4|tq0.2|strict`。
- 窗口 2: 测试 2021-11-29 00:00:00 至 2023-05-30 00:00:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am2|ex12|mom20|vol24|th0.4|tq0.2|strict`。
- 窗口 3: 测试 2023-05-31 00:00:00 至 2024-11-28 00:00:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am2|ex12|mom20|vol24|th0.4|tq0.2|strict`。
- 窗口 4: 测试 2024-11-29 00:00:00 至 2026-06-05 00:00:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am2|ex12|mom20|vol24|th0.4|tq0.2|strict`。
### CJ 30m
- 窗口 1: 测试 2025-12-29 14:15:00 至 2026-02-05 09:30:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|30m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.3|strict`。
- 窗口 2: 测试 2026-02-05 10:00:00 至 2026-03-20 13:45:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|30m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 3: 测试 2026-03-20 14:15:00 至 2026-04-28 09:30:00，净收益 1096，回撤 -54，胜率 100.0%，`trend_pullback|both|30m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 4: 测试 2026-04-28 10:00:00 至 2026-06-05 15:00:00，净收益 -264，回撤 -668，胜率 33.3%，`trend_pullback|both|30m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.2|strict`。
### UR 60m
- 窗口 1: 测试 2025-07-30 11:15:00 至 2025-10-17 10:00:00，净收益 -527，回撤 -830，胜率 0.0%，`trend_pullback|both|60m|w3|sw0.006|br0.0015|lb96|sl0.015|mh96|cd4|atr14|am2|ex12|mom48|vol24|th0.4|tq0.2|strict`。
- 窗口 2: 测试 2025-10-17 11:15:00 至 2025-12-29 10:00:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|60m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 3: 测试 2025-12-29 11:15:00 至 2026-03-20 10:00:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|60m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 4: 测试 2026-03-20 11:15:00 至 2026-06-05 15:00:00，净收益 553，回撤 -587，胜率 100.0%，`trend_pullback|both|60m|w3|sw0.006|br0.0015|lb96|sl0.015|mh96|cd4|atr14|am2|ex12|mom48|vol24|th0.4|tq0.2|strict`。
### UR 30m
- 窗口 1: 测试 2025-12-29 14:15:00 至 2026-02-05 09:30:00，净收益 -204，回撤 -444，胜率 0.0%，`trend_pullback|both|30m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am3|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 2: 测试 2026-02-05 10:00:00 至 2026-03-20 13:45:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|30m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am3|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 3: 测试 2026-03-20 14:15:00 至 2026-04-28 09:30:00，净收益 96，回撤 -624，胜率 100.0%，`trend_pullback|both|30m|w3|sw0.006|br0.0015|lb96|sl0.015|mh96|cd4|atr14|am3|ex12|mom48|vol24|th0.4|tq0.3|strict`。
- 窗口 4: 测试 2026-04-28 10:00:00 至 2026-06-05 15:00:00，净收益 -344，回撤 -600，胜率 0.0%，`trend_pullback|both|30m|w3|sw0.006|br0.0015|lb96|sl0.015|mh96|cd4|atr14|am3|ex12|mom48|vol24|th0.4|tq0.2|strict`。
### UR 1d
- 窗口 1: 测试 2020-12-18 00:00:00 至 2022-04-29 00:00:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am2|ex12|mom20|vol24|th0.4|tq0.3|strict`。
- 窗口 2: 测试 2022-05-05 00:00:00 至 2023-09-05 00:00:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am2|ex12|mom20|vol24|th0.4|tq0.3|strict`。
- 窗口 3: 测试 2023-09-06 00:00:00 至 2025-01-16 00:00:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am2|ex12|mom20|vol24|th0.4|tq0.3|strict`。
- 窗口 4: 测试 2025-01-17 00:00:00 至 2026-06-05 00:00:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am2|ex12|mom20|vol24|th0.4|tq0.3|strict`。
### FG 60m
- 窗口 1: 测试 2025-11-10 11:15:00 至 2025-12-26 10:00:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|60m|w3|sw0.006|br0.0015|lb96|sl0.015|mh96|cd4|atr14|am2|ex12|mom48|vol24|th0.4|tq0.3|strict`。
- 窗口 2: 测试 2025-12-26 11:15:00 至 2026-02-24 22:00:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|60m|w3|sw0.006|br0.0015|lb96|sl0.015|mh96|cd4|atr14|am2|ex12|mom48|vol24|th0.4|tq0.2|strict`。
- 窗口 3: 测试 2026-02-24 23:00:00 至 2026-04-15 10:00:00，净收益 -324，回撤 -624，胜率 0.0%，`trend_pullback|both|60m|w3|sw0.006|br0.0015|lb96|sl0.015|mh96|cd4|atr14|am2|ex12|mom48|vol24|th0.4|tq0.2|strict`。
- 窗口 4: 测试 2026-04-15 11:15:00 至 2026-06-05 23:00:00，净收益 -322，回撤 -344，胜率 0.0%，`trend_pullback|both|60m|w3|sw0.006|br0.0015|lb96|sl0.015|mh96|cd4|atr14|am2|ex12|mom48|vol24|th0.4|tq0.2|strict`。
### FG 30m
- 窗口 1: 测试 2026-02-25 10:00:00 至 2026-03-20 09:30:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|30m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.3|strict`。
- 窗口 2: 测试 2026-03-20 10:00:00 至 2026-04-15 13:45:00，净收益 236，回撤 -644，胜率 50.0%，`trend_pullback|both|30m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am3|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 3: 测试 2026-04-15 14:15:00 至 2026-05-13 21:30:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|30m|w3|sw0.006|br0.0015|lb96|sl0.015|mh96|cd4|atr14|am3|ex12|mom48|vol24|th0.4|tq0.2|strict`。
- 窗口 4: 测试 2026-05-13 22:00:00 至 2026-06-05 23:00:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|30m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am3|ex12|mom24|vol24|th0.4|tq0.3|strict`。
### C 60m
- 窗口 1: 测试 2025-11-10 11:15:00 至 2025-12-26 10:00:00，净收益 -172，回撤 -302，胜率 0.0%，`trend_pullback|both|60m|w3|sw0.006|br0.0015|lb96|sl0.015|mh96|cd4|atr14|am2|ex12|mom48|vol24|th0.4|tq0.2|strict`。
- 窗口 2: 测试 2025-12-26 11:15:00 至 2026-02-24 22:00:00，净收益 -62，回撤 -142，胜率 0.0%，`trend_pullback|both|60m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.3|strict`。
- 窗口 3: 测试 2026-02-24 23:00:00 至 2026-04-15 10:00:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|60m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 4: 测试 2026-04-15 11:15:00 至 2026-06-05 23:00:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|60m|w3|sw0.006|br0.0015|lb96|sl0.015|mh96|cd4|atr14|am2|ex12|mom48|vol24|th0.4|tq0.3|strict`。
### C 30m
- 窗口 1: 测试 2026-02-25 10:00:00 至 2026-03-20 09:30:00，净收益 268，回撤 -132，胜率 100.0%，`trend_pullback|both|30m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am3|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 2: 测试 2026-03-20 10:00:00 至 2026-04-15 13:45:00，净收益 -192，回撤 -205，胜率 0.0%，`trend_pullback|both|30m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am3|ex12|mom24|vol24|th0.4|tq0.3|strict`。
- 窗口 3: 测试 2026-04-15 14:15:00 至 2026-05-13 21:30:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|30m|w3|sw0.006|br0.0015|lb96|sl0.015|mh96|cd4|atr14|am2|ex12|mom48|vol24|th0.4|tq0.2|strict`。
- 窗口 4: 测试 2026-05-13 22:00:00 至 2026-06-05 23:00:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|30m|w3|sw0.006|br0.0015|lb96|sl0.015|mh96|cd4|atr14|am2|ex12|mom48|vol24|th0.4|tq0.3|strict`。
### RB 60m
- 窗口 1: 测试 2025-11-10 11:15:00 至 2025-12-26 10:00:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|60m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 2: 测试 2025-12-26 11:15:00 至 2026-02-24 22:00:00，净收益 -283，回撤 -296，胜率 0.0%，`trend_pullback|both|60m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 3: 测试 2026-02-24 23:00:00 至 2026-04-15 10:00:00，净收益 -203，回撤 -243，胜率 0.0%，`trend_pullback|both|60m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 4: 测试 2026-04-15 11:15:00 至 2026-06-05 23:00:00，净收益 54，回撤 -470，胜率 50.0%，`trend_pullback|both|60m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.2|strict`。
### RB 30m
- 窗口 1: 测试 2026-02-25 10:00:00 至 2026-03-20 09:30:00，净收益 -176，回撤 -229，胜率 0.0%，`trend_pullback|both|30m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 2: 测试 2026-03-20 10:00:00 至 2026-04-15 13:45:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|30m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 3: 测试 2026-04-15 14:15:00 至 2026-05-13 21:30:00，净收益 24，回撤 -250，胜率 50.0%，`trend_pullback|both|30m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 4: 测试 2026-05-13 22:00:00 至 2026-06-05 23:00:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|30m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am3|ex12|mom24|vol24|th0.4|tq0.2|strict`。
### RM 60m
- 窗口 1: 测试 2025-11-10 11:15:00 至 2025-12-26 10:00:00，净收益 148，回撤 -272，胜率 100.0%，`trend_pullback|both|60m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 2: 测试 2025-12-26 11:15:00 至 2026-02-24 22:00:00，净收益 248，回撤 -432，胜率 100.0%，`trend_pullback|both|60m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am3|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 3: 测试 2026-02-24 23:00:00 至 2026-04-15 10:00:00，净收益 235，回撤 -1355，胜率 50.0%，`trend_pullback|both|60m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am3|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 4: 测试 2026-04-15 11:15:00 至 2026-06-05 23:00:00，净收益 58，回撤 -52，胜率 100.0%，`trend_pullback|both|60m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am3|ex12|mom24|vol24|th0.4|tq0.2|strict`。
### FG 1d
- 窗口 1: 测试 2015-08-17 00:00:00 至 2018-04-26 00:00:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am2|ex12|mom20|vol24|th0.4|tq0.2|strict`。
- 窗口 2: 测试 2018-04-27 00:00:00 至 2021-01-05 00:00:00，净收益 17，回撤 -783，胜率 100.0%，`trend_pullback|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am2|ex12|mom20|vol24|th0.4|tq0.2|strict`。
- 窗口 3: 测试 2021-01-06 00:00:00 至 2023-09-12 00:00:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am2|ex12|mom20|vol24|th0.4|tq0.2|strict`。
- 窗口 4: 测试 2023-09-13 00:00:00 至 2026-06-05 00:00:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am2|ex12|mom20|vol24|th0.4|tq0.2|strict`。
### RM 30m
- 窗口 1: 测试 2026-02-25 10:00:00 至 2026-03-20 09:30:00，净收益 1702，回撤 -680，胜率 66.7%，`trend_pullback|both|30m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 2: 测试 2026-03-20 10:00:00 至 2026-04-15 13:45:00，净收益 -67，回撤 -337，胜率 33.3%，`trend_pullback|both|30m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.3|strict`。
- 窗口 3: 测试 2026-04-15 14:15:00 至 2026-05-13 21:30:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|30m|w3|sw0.006|br0.0015|lb96|sl0.015|mh96|cd4|atr14|am3|ex12|mom48|vol24|th0.4|tq0.2|strict`。
- 窗口 4: 测试 2026-05-13 22:00:00 至 2026-06-05 23:00:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|30m|w3|sw0.006|br0.0015|lb96|sl0.015|mh96|cd4|atr14|am3|ex12|mom48|vol24|th0.4|tq0.2|strict`。
### HC 60m
- 窗口 1: 测试 2025-11-10 11:15:00 至 2025-12-26 10:00:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|60m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 2: 测试 2025-12-26 11:15:00 至 2026-02-24 22:00:00，净收益 -193，回撤 -223，胜率 0.0%，`trend_pullback|both|60m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 3: 测试 2026-02-24 23:00:00 至 2026-04-15 10:00:00，净收益 -267，回撤 -357，胜率 0.0%，`trend_pullback|both|60m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.3|strict`。
- 窗口 4: 测试 2026-04-15 11:15:00 至 2026-06-05 23:00:00，净收益 37，回撤 -280，胜率 100.0%，`trend_pullback|both|60m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.3|strict`。
### SR 1d
- 窗口 1: 测试 2010-01-29 00:00:00 至 2014-03-11 00:00:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|1d|w3|sw0.006|br0.0015|lb120|sl0.015|mh96|cd4|atr14|am2|ex12|mom40|vol24|th0.4|tq0.3|strict`。
- 窗口 2: 测试 2014-03-12 00:00:00 至 2018-03-28 00:00:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|1d|w3|sw0.006|br0.0015|lb120|sl0.015|mh96|cd4|atr14|am2|ex12|mom40|vol24|th0.4|tq0.3|strict`。
- 窗口 3: 测试 2018-03-29 00:00:00 至 2022-04-28 00:00:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|1d|w3|sw0.006|br0.0015|lb120|sl0.015|mh96|cd4|atr14|am2|ex12|mom40|vol24|th0.4|tq0.3|strict`。
- 窗口 4: 测试 2022-04-29 00:00:00 至 2026-06-05 00:00:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|1d|w3|sw0.006|br0.0015|lb120|sl0.015|mh96|cd4|atr14|am2|ex12|mom40|vol24|th0.4|tq0.3|strict`。
### HC 30m
- 窗口 1: 测试 2026-02-25 10:00:00 至 2026-03-20 09:30:00，净收益 137，回撤 -173，胜率 100.0%，`trend_pullback|both|30m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am3|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 2: 测试 2026-03-20 10:00:00 至 2026-04-15 13:45:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|30m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am3|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 3: 测试 2026-04-15 14:15:00 至 2026-05-13 21:30:00，净收益 -317，回撤 -360，胜率 0.0%，`trend_pullback|both|30m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am3|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 4: 测试 2026-05-13 22:00:00 至 2026-06-05 23:00:00，净收益 -363，回撤 -543，胜率 0.0%，`trend_pullback|both|30m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am3|ex12|mom24|vol24|th0.4|tq0.2|strict`。
### SA 60m
- 窗口 1: 测试 2025-11-10 11:15:00 至 2025-12-26 10:00:00，净收益 -1105，回撤 -1149，胜率 0.0%，`trend_pullback|both|60m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 2: 测试 2025-12-26 11:15:00 至 2026-02-24 22:00:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|60m|w3|sw0.006|br0.0015|lb96|sl0.015|mh96|cd4|atr14|am2|ex12|mom48|vol24|th0.4|tq0.2|strict`。
- 窗口 3: 测试 2026-02-24 23:00:00 至 2026-04-15 10:00:00，净收益 898，回撤 -322，胜率 100.0%，`trend_pullback|both|60m|w3|sw0.006|br0.0015|lb96|sl0.015|mh96|cd4|atr14|am2|ex12|mom48|vol24|th0.4|tq0.2|strict`。
- 窗口 4: 测试 2026-04-15 11:15:00 至 2026-06-05 23:00:00，净收益 -202，回撤 -242，胜率 0.0%，`trend_pullback|both|60m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.2|strict`。
### SA 1d
- 窗口 1: 测试 2021-03-25 00:00:00 至 2022-07-11 00:00:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am2|ex12|mom20|vol24|th0.4|tq0.2|strict`。
- 窗口 2: 测试 2022-07-12 00:00:00 至 2023-10-26 00:00:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am2|ex12|mom20|vol24|th0.4|tq0.2|strict`。
- 窗口 3: 测试 2023-10-27 00:00:00 至 2025-02-14 00:00:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am2|ex12|mom20|vol24|th0.4|tq0.2|strict`。
- 窗口 4: 测试 2025-02-17 00:00:00 至 2026-06-05 00:00:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am2|ex12|mom20|vol24|th0.4|tq0.2|strict`。
### SA 30m
- 窗口 1: 测试 2026-02-25 10:00:00 至 2026-03-20 09:30:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|30m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.3|strict`。
- 窗口 2: 测试 2026-03-20 10:00:00 至 2026-04-15 13:45:00，净收益 1053，回撤 -385，胜率 66.7%，`trend_pullback|both|30m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am3|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 3: 测试 2026-04-15 14:15:00 至 2026-05-13 21:30:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|30m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am3|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 4: 测试 2026-05-13 22:00:00 至 2026-06-05 23:00:00，净收益 158，回撤 -80，胜率 100.0%，`trend_pullback|both|30m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am3|ex12|mom24|vol24|th0.4|tq0.2|strict`。
### RM 1d
- 窗口 1: 测试 2015-09-10 00:00:00 至 2018-05-15 00:00:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am2|ex12|mom20|vol24|th0.4|tq0.3|strict`。
- 窗口 2: 测试 2018-05-16 00:00:00 至 2021-01-15 00:00:00，净收益 -832，回撤 -1122，胜率 0.0%，`trend_pullback|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am2|ex12|mom20|vol24|th0.4|tq0.2|strict`。
- 窗口 3: 测试 2021-01-18 00:00:00 至 2023-09-20 00:00:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am2|ex12|mom20|vol24|th0.4|tq0.2|strict`。
- 窗口 4: 测试 2023-09-21 00:00:00 至 2026-06-05 00:00:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am2|ex12|mom20|vol24|th0.4|tq0.2|strict`。
### HC 1d
- 窗口 1: 测试 2016-08-17 00:00:00 至 2019-01-22 00:00:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am2|ex12|mom20|vol24|th0.4|tq0.3|strict`。
- 窗口 2: 测试 2019-01-23 00:00:00 至 2021-07-07 00:00:00，净收益 -634，回撤 -950，胜率 0.0%，`trend_pullback|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am2|ex12|mom20|vol24|th0.4|tq0.3|strict`。
- 窗口 3: 测试 2021-07-08 00:00:00 至 2023-12-15 00:00:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am2|ex12|mom20|vol24|th0.4|tq0.2|strict`。
- 窗口 4: 测试 2023-12-18 00:00:00 至 2026-06-05 00:00:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am2|ex12|mom20|vol24|th0.4|tq0.2|strict`。
### RB 1d
- 窗口 1: 测试 2012-08-28 00:00:00 至 2016-02-05 00:00:00，净收益 2461，回撤 -955，胜率 75.0%，`trend_pullback|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am2|ex12|mom20|vol24|th0.4|tq0.2|strict`。
- 窗口 2: 测试 2016-02-15 00:00:00 至 2019-07-12 00:00:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am3|ex12|mom20|vol24|th0.4|tq0.2|strict`。
- 窗口 3: 测试 2019-07-15 00:00:00 至 2022-12-16 00:00:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am3|ex12|mom20|vol24|th0.4|tq0.2|strict`。
- 窗口 4: 测试 2022-12-19 00:00:00 至 2026-06-05 00:00:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am3|ex12|mom20|vol24|th0.4|tq0.2|strict`。
### CS 60m
- 窗口 1: 测试 2025-11-10 11:15:00 至 2025-12-26 10:00:00，净收益 -162，回撤 -175，胜率 0.0%，`trend_pullback|both|60m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.3|strict`。
- 窗口 2: 测试 2025-12-26 11:15:00 至 2026-02-24 22:00:00，净收益 55，回撤 -358，胜率 50.0%，`trend_pullback|both|60m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 3: 测试 2026-02-24 23:00:00 至 2026-04-15 10:00:00，净收益 187，回撤 -240，胜率 100.0%，`trend_pullback|both|60m|w3|sw0.006|br0.0015|lb96|sl0.015|mh96|cd4|atr14|am2|ex12|mom48|vol24|th0.4|tq0.2|strict`。
- 窗口 4: 测试 2026-04-15 11:15:00 至 2026-06-05 23:00:00，净收益 -63，回撤 -153，胜率 0.0%，`trend_pullback|both|60m|w3|sw0.006|br0.0015|lb96|sl0.015|mh96|cd4|atr14|am2|ex12|mom48|vol24|th0.4|tq0.2|strict`。
### CS 30m
- 窗口 1: 测试 2026-02-25 10:00:00 至 2026-03-20 09:30:00，净收益 377，回撤 -123，胜率 100.0%，`trend_pullback|both|30m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am2|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 2: 测试 2026-03-20 10:00:00 至 2026-04-15 13:45:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|30m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am3|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 3: 测试 2026-04-15 14:15:00 至 2026-05-13 21:30:00，净收益 817，回撤 -93，胜率 100.0%，`trend_pullback|both|30m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am3|ex12|mom24|vol24|th0.4|tq0.2|strict`。
- 窗口 4: 测试 2026-05-13 22:00:00 至 2026-06-05 23:00:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|30m|w3|sw0.006|br0.0015|lb64|sl0.015|mh64|cd4|atr14|am3|ex12|mom24|vol24|th0.4|tq0.2|strict`。
### C 1d
- 窗口 1: 测试 2009-04-13 00:00:00 至 2013-07-24 00:00:00，净收益 -23，回撤 -953，胜率 50.0%，`trend_pullback|both|1d|w3|sw0.006|br0.0015|lb120|sl0.015|mh96|cd4|atr14|am2|ex12|mom40|vol24|th0.4|tq0.2|strict`。
- 窗口 2: 测试 2013-07-25 00:00:00 至 2017-11-01 00:00:00，净收益 46，回撤 -3754，胜率 50.0%，`trend_pullback|both|1d|w3|sw0.006|br0.0015|lb120|sl0.015|mh96|cd4|atr14|am3|ex12|mom40|vol24|th0.4|tq0.2|strict`。
- 窗口 3: 测试 2017-11-02 00:00:00 至 2022-02-16 00:00:00，净收益 1137，回撤 -680，胜率 66.7%，`trend_pullback|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am2|ex12|mom20|vol24|th0.4|tq0.3|strict`。
- 窗口 4: 测试 2022-02-17 00:00:00 至 2026-06-05 00:00:00，净收益 -635，回撤 -659，胜率 0.0%，`trend_pullback|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am2|ex12|mom20|vol24|th0.4|tq0.3|strict`。
### CS 1d
- 窗口 1: 测试 2017-04-07 00:00:00 至 2019-07-17 00:00:00，净收益 -1522，回撤 -1941，胜率 0.0%，`trend_pullback|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am2|ex12|mom20|vol24|th0.4|tq0.2|strict`。
- 窗口 2: 测试 2019-07-18 00:00:00 至 2021-11-02 00:00:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am2|ex12|mom20|vol24|th0.4|tq0.3|strict`。
- 窗口 3: 测试 2021-11-03 00:00:00 至 2024-02-19 00:00:00，净收益 0，回撤 0，胜率 0.0%，`trend_pullback|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am2|ex12|mom20|vol24|th0.4|tq0.3|strict`。
- 窗口 4: 测试 2024-02-20 00:00:00 至 2026-06-05 00:00:00，净收益 -503，回撤 -516，胜率 0.0%，`trend_pullback|both|1d|w3|sw0.006|br0.0015|lb80|sl0.015|mh64|cd4|atr14|am2|ex12|mom20|vol24|th0.4|tq0.3|strict`。
