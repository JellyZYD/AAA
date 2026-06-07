# Research-Driven Futures Strategy Plan

Generated: 2026-06-07

## Objective

Build the live signal system around strategies with a clear market reason, not around blind parameter mixing. The first live candidate should aim to catch large directional moves in Chinese commodity futures while respecting an 8,500 CNY account and an 8,000 CNY margin budget.

This is still research and signal generation, not a guarantee of profit. A strategy only becomes live-eligible if it survives causal walk-forward validation after fees, slippage, next-bar fills, closed-bar signals, margin limits, and stop-risk limits.

## Sources Checked

- Moskowitz, Ooi, Pedersen, "Time Series Momentum" (Journal of Financial Economics, 2012): documents time-series momentum across equity index, currency, commodity, and bond futures. Their core rule is to go long after positive own-past returns and short after negative own-past returns, with volatility scaling. Source: https://w4.stern.nyu.edu/facdir/lpederse/papers/TimeSeriesMomentum.pdf
- Hurst, Ooi, Pedersen, "A Century of Evidence on Trend-Following Investing" (2017): finds trend following has delivered positive average returns across long historical samples and many macro regimes. Source: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2993026
- Jin, Kearney, Li, Yang, "Intraday Time-series Momentum: Evidence from China" (Journal of Futures Markets, 2020): finds intraday time-series momentum in Chinese commodity futures, with stronger effects in high-volume/high-volatility sessions for metals. Source: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3493927
- Yang, Goncu, Pantelous, "Momentum and Reversal Strategies in Chinese Commodity Futures Markets" (2017): finds momentum/reversal can be robust, but intraday strategies can fail to cover excessive transaction costs, while lower-frequency/longer holding strategies have drawdown risk. Source: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3069253
- Ming, Song, Dong, "Revisiting time series momentum in China's commodity futures market" (Economic Modelling, 2023): identifies time-series momentum in China's commodity futures market, especially around one-month lookback horizons. Source: https://ideas.repec.org/a/eee/ecmode/v128y2023ics0264999323003346.html
- "Commodity futures price term structure implied trading strategy information" (SZSE research PDF): explains roll yield and term structure logic; backwardation can support long carry and contango can support short carry. Source: https://www.szse.cn/aboutus/research/secuities/documents/P020180328492611492675.pdf
- Recent news/sentiment research suggests commodity-specific news sentiment can affect returns and volatility, but it should be used as a weighting/risk context, not as a standalone opening trigger without historical validation. Example: https://journals.sagepub.com/doi/10.1177/21582440231152131

## Strategy Thesis

The most defensible first principle is trend following / time-series momentum, not predicting every news event. Commodity futures can trend because supply, demand, inventory, policy, and hedging pressure adjust slowly. The signal should therefore react to confirmed price behavior, while news and term structure add context.

The practical issue for this account is not finding one huge historical return; it is avoiding strategies whose drawdown is larger than the account can tolerate. Therefore the live strategy should prefer fewer, higher-quality signals over frequent 15m entries.

## Candidate Families

1. Core time-series momentum (`tsmom_vol`)
   - Reason: directly follows the best-supported futures anomaly.
   - Mechanism: own-past return divided by realized volatility, long if score is positive enough, short if negative enough.
   - Weakness: single lookback can enter late or get chopped in sideways markets.

2. Donchian/ATR trend following (`donchian_atr`)
   - Reason: breakout with ATR risk control is a classic commodity trend-following implementation.
   - Mechanism: break prior channel, exit by ATR trailing stop or channel failure.
   - Weakness: false breakouts in choppy markets.

3. Carry-filtered momentum (`carry_tsmom`)
   - Reason: term structure/roll yield can align trades with inventory/hedging pressure.
   - Mechanism: only trade when momentum and lagged carry point the same way.
   - Weakness: term-structure data quality is uneven across the user's tradable symbols.

4. Research-driven ensemble trend (`ensemble_trend`)
   - Reason: combines the above lessons without adding arbitrary indicators.
   - Mechanism:
     - short-horizon momentum must agree with long-horizon momentum;
     - volatility-scaled scores must pass a threshold;
     - trend efficiency must be high enough, meaning net price movement is not just noisy back-and-forth;
     - entry still requires a prior-range breakout confirmation;
     - exit uses ATR trailing stop, channel failure, momentum deterioration, or max holding time.
   - Expected benefit: fewer trades than raw TSMOM, lower false breakout rate than Donchian alone, and better reward/drawdown than the prior weak candidates.

## Target Metrics Before Live Use

Hard filters:
- out-of-sample / walk-forward net PnL must be positive after fees and 1-tick slippage;
- positive walk-forward windows must be at least 3 out of 4;
- net PnL / absolute max drawdown must be at least 1.2, with a preferred target above 1.5;
- worst drawdown must be below 80% of capital, with preferred live drawdown below 50% of capital;
- total test trades must be enough to avoid one lucky trade, normally at least 8 for intraday and at least 5 for daily;
- every trade must pass one-lot margin <= 8,000 CNY and stop risk <= configured per-trade risk.

Preferred target for the next iteration:
- at least 5 active symbols;
- portfolio-level active signals should not require more than one simultaneous new position unless margin allows it;
- average win rate is useful, but reward/drawdown and positive windows have higher priority than win rate alone;
- 15m strategies must prove that costs do not consume the edge. If they do not, they stay research-only.

## No-Future-Function Rules

- Strategy signals are generated only from the current completed bar and earlier bars.
- Backtest fills at next bar open, not at signal-bar close.
- Breakout channels use prior bars only, excluding the current bar.
- Pivot confirmation is delayed until the confirming bars have closed.
- Carry factors are shifted one bar before use.
- News/event timestamps must be <= the signal timestamp.
- Walk-forward candidate selection for each test window uses only earlier history.

## Implementation Decision

Keep existing `tsmom_vol`, `donchian_atr`, `vol_breakout`, and `carry_tsmom`, but add only one new research-driven candidate: `ensemble_trend`.

Remove the unproven `take_profit_atr` expansion. A fixed profit target conflicts with the trend-following goal of letting unusually large moves run. Profit taking should happen through trailing stops and trend failure, not an arbitrary ATR multiple.

## First Validation Result

Command:

```powershell
qihuo walk-forward --pattern ensemble_trend --timeframe 1d --timeframe 60m --timeframe 30m --max-per-symbol 16 --workers 8 --no-profile-write
```

Result file copied to: `reports/ensemble_walk_forward/`.

Findings:
- `ensemble_trend` did not qualify any symbol as active under the strict live filters.
- Best headline result was SP 1d with 20,132.86 CNY walk-forward test PnL, but it came from only 1 test trade and only 1 positive window out of 4. This is not robust enough.
- RM 60m had 4 positive windows out of 4 and high average win rate, but only 688.42 CNY test PnL against -1,354.81 CNY worst drawdown, so reward/drawdown failed.
- HC 1d had 3 positive windows out of 4, but 1,131.19 CNY PnL against -1,678.46 CNY drawdown also failed reward/drawdown.

Interpretation:
- Trend efficiency is useful as a market-environment filter, which is consistent with the trend-following literature's focus on clean directional movement.
- Requiring multi-horizon momentum and a long-range breakout at the same time made entries too late and too rare.
- The next candidate should keep trend efficiency as a filter, but use a smaller-risk continuation entry after a pullback in the trend direction. This is more suitable for an 8,500 CNY account because the initial stop can be closer than a late channel-breakout stop.

## Second Validation Result

New candidate: `trend_pullback`.

Rationale:
- Keep the same research-supported trend environment: volatility-scaled momentum plus trend efficiency.
- Do not chase a full long-range breakout.
- Enter only after a pullback and a smaller short-structure continuation breakout in the trend direction.
- Initial stop is anchored around the pullback extreme plus half an ATR, so the stop distance should be lower than late breakout entries.

Command:

```powershell
qihuo walk-forward --pattern trend_pullback --timeframe 1d --timeframe 60m --timeframe 30m --max-per-symbol 16 --workers 8 --no-profile-write --reports-root reports/trend_pullback_walk_forward
```

Findings:
- `trend_pullback` also did not qualify any symbol as active under the strict live filters.
- RM 60m again showed 4 positive windows out of 4 and 87.5% average win rate, but net PnL was only 688.42 CNY against -1,354.81 CNY worst drawdown.
- CS 30m improved reward/drawdown on paper with 1,194.55 CNY PnL against -122.72 CNY drawdown, but it only had 2 total test trades and 2 positive windows out of 4, so it is not a robust live candidate.
- SA 30m was positive at 1,210.64 CNY with -384.71 CNY drawdown, but only 2 positive windows out of 4.

Interpretation:
- Pullback entry can improve stop distance and reward/drawdown in selected cases, but the strict version still produces too few robust samples.
- This family should stay in the research pool, not the live pool.
- The next improvement should not loosen filters blindly. It should compare whether trend efficiency is better as a veto filter on proven existing strategies (`tsmom_vol`, `donchian_atr`, `vol_breakout`) rather than as a standalone entry model.

## Third Validation Result

New candidate: `quality_tsmom`.

Rationale:
- Keep the most research-supported signal, time-series momentum.
- Add only one veto: do not trade if the price path is too noisy for the measured trend.
- This should avoid the two earlier problems: `ensemble_trend` entered too late, and `trend_pullback` traded too rarely.

Command:

```powershell
qihuo walk-forward --pattern quality_tsmom --timeframe 1d --timeframe 60m --timeframe 30m --max-per-symbol 16 --workers 8 --no-profile-write --reports-root reports/quality_tsmom_walk_forward
```

Findings:
- `quality_tsmom` produced one strict active candidate: FG 30m.
- FG 30m: 2,041.97 CNY test PnL, -1,297.85 CNY worst drawdown, 3/4 positive windows, 72.5% average test win rate, 18 trades.
- HC 1d and SR 1d had high net PnL, but their drawdowns exceeded the small-account risk filter.
- Several 30m/60m symbols improved stability, but most still failed either positive-window count or reward/drawdown.

Interpretation:
- Trend efficiency works better as a veto on a proven momentum signal than as a standalone entry model.
- The next validation should run a combined research pool: `tsmom_vol`, `quality_tsmom`, `donchian_atr`, `vol_breakout`, and `carry_tsmom`.
- If `quality_tsmom` only improves FG, it should be added as a per-symbol champion candidate instead of replacing the whole live system.

## Combined Pool Result

Command:

```powershell
qihuo walk-forward --pattern tsmom_vol --pattern quality_tsmom --pattern donchian_atr --pattern vol_breakout --pattern carry_tsmom --timeframe 1d --timeframe 60m --timeframe 30m --max-per-symbol 16 --workers 8 --no-profile-write --reports-root reports/research_walk_forward
```

Strict active rows:

| Symbol | Pattern | Timeframe | Test PnL | Worst DD | Positive Windows | Avg Win Rate | Trades |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| HC | `tsmom_vol` | 1d | 17,756.66 | -4,818.36 | 3/4 | 54.5% | 59 |
| C | `vol_breakout` | 60m | 1,762.25 | -589.10 | 4/4 | 70.8% | 12 |
| RM | `vol_breakout` | 30m | 2,146.74 | -1,089.93 | 3/4 | 39.6% | 14 |
| SR | `vol_breakout` | 30m | 1,476.81 | -495.46 | 3/4 | 50.0% | 8 |

Interpretation:
- This combined pool improves breadth versus the previous strict profile: C and RM become active, while HC and SR remain active.
- SA loses active status in this research pool because the selected 60m/30m candidates did not satisfy positive-window and reward/drawdown filters.
- The result is not yet enough to declare a final live profile because FG's standalone `quality_tsmom` active candidate is not selected by the combined walk-forward selector. This needs a per-symbol review before changing live.

Rejected scoring experiment:
- I tested a more aggressive train-window score that heavily favored reward/drawdown. It reduced active candidates from 4 to 1 and selected poorer out-of-sample rows. I reverted that scoring change.
- Lesson: strict filters should remain at the validation/live gate; over-penalizing train selection can make the selector miss profitable trends.

## Full-Timeframe Research Pool

Command:

```powershell
qihuo walk-forward --pattern tsmom_vol --pattern quality_tsmom --pattern donchian_atr --pattern vol_breakout --pattern carry_tsmom --timeframe 1d --timeframe 60m --timeframe 30m --timeframe 15m --max-per-symbol 16 --workers 8 --no-profile-write --reports-root reports/research_walk_forward_all_tf
```

Strict active rows:

| Symbol | Pattern | Timeframe | Test PnL | Worst DD | Positive Windows | Avg Win Rate | Trades |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| HC | `tsmom_vol` | 1d | 17,756.66 | -4,818.36 | 3/4 | 54.5% | 59 |
| C | `vol_breakout` | 60m | 1,762.25 | -589.10 | 4/4 | 70.8% | 12 |
| RM | `vol_breakout` | 30m | 2,146.74 | -1,089.93 | 3/4 | 39.6% | 14 |
| SR | `vol_breakout` | 30m | 1,476.81 | -495.46 | 3/4 | 50.0% | 8 |

Interpretation:
- Adding 15m did not add any new active candidates under strict filters.
- The active set is the same as the 1d/60m/30m research pool.
- Research conclusion as of this run: HC, C, RM, and SR have the most defensible active status; FG's standalone `quality_tsmom` result is promising but not selected in the combined pool; SA needs more work before being promoted again.
