# task1 determinism check, pass 2 (build stage 4 re-judge)

Working copy: the current `target.zip` and `golden.zip` unzipped fresh; every figure below is recomputed from the shipped files by the Step-by-Step's own method. Gates A to E only. Pass 1 is left in `determinism_check_report.md` (a pass is never overwritten); its summary is the last paragraph here.

## Verdict

**DETERMINISTIC, with SOLUTION_WRONG on the blocks only.** The seven bands hold in every fork run: 306 runs of 33 listed ways and two extra ones, each under up to nine ways of carrying the response, plus the further forks below. Across the listed ways the returns run Pinterest iOS 1.58 to 1.69, Google iOS 1.35 to 1.46, Meta iOS 1.03 to 1.10, Google Android 0.96 to 1.07, AppLovin Android 0.94 to 1.05, Snapchat iOS 0.60 to 0.66, TikTok iOS 0.58 to 0.65. Each of the three shortcuts that moves a band is refuted by a figure I recomputed from the shipped files. What is left is in the answer blocks: one band the literal rebuild misses by a cent, one sentence of step 7 that reads three ways, a few band edges that listed ways cross, and three statements of the closing passage that do not recompute as written.

## Disposition

**FIX_NOW** (answer-block edits only: band edges, two stated conventions, wording of the closing passage). Nothing in `prompt.txt` or the pack needs to change. No re-judge is needed for these edits unless a golden figure moves.

## Evidence: figures recomputed

| Figure | Blocks (band) | Recomputed | Result |
|---|---|---|---|
| Consumer accounts; refunded purchases | 713,534; 1,070 | 713,534; 1,070 | reproduced |
| Monthly charges, report against records | GP 242,783 / 165,641; AS 304,732 / 214,666 | same | reproduced |
| Set to renew, next charge after last open | 13,351; 15,494 | 13,351; 15,494 | reproduced |
| Monthly trials charged; annual trials charged | 0.087, 0.088; 0.105, 0.108 of 9,397 and 11,032 (989; 1,190) | 0.0874, 0.0884; 0.1052, 0.1079; 989; 1,190 | reproduced |
| Continuation | 0.888 on both stores | 0.8873 (Google Play), 0.8882 (App Store) on calendar months | reproduced to 0.001 (fix 8) |
| CC1 AppLovin Android outside the records | 34.8 (34.5 to 35.4) | 34.77 with my fitted rates, 34.82 with the blocks' rounded rates | inside band |
| Share outside the records, plan channels | 13.6 to 34.8; in proportion 16.1 to 18.6 | 13.4 to 34.8; 16.2 to 18.7 | within 0.2 points |
| Web checkout check | 390 subscribers, EUR 40.15, rule 36.50, in proportion 12.23 | 391 set to renew (390 with a charge before the last open); 40.15 per 391; rule 36.41 per 391 or 36.50 per 390; in proportion about 11 to 12 | reproduced in substance (fix 8) |
| Named share of iOS installs | 26.2 to 28.9 | 26.2 to 28.9 | reproduced |
| Accounts with no channel; paid; at the named value | 124,321; EUR 927,121; 1.43 times | 124,321; 927,073; 1.43 | reproduced |
| CC2 Meta iOS all installs | 9.08 (8.83 to 9.31); named 14.32; hurried 11.23 | 9.09; 14.32; 11.25 | inside band |
| Apple Search Ads check | 10,068; 11.71; pricing 11.58; named value 16.18 | 10,068; 11.71; 11.58; 16.19 | reproduced |
| Google Android elasticity, budget and spend | 0.70; 1.02 | 0.698; 1.02 (all seven installs slopes and all seven value slopes match the workbook to two decimals) | reproduced |
| Moved weeks, Google Android | 15 raised, 18 lowered; 1.36, 1.41, 1.82 | 15; 18; 1.36, 1.41, 1.82 (each move left out; 1.36, 1.40, 1.78 with each week left out) | reproduced |
| CC3 iOS revenue at plan spend | 1,219,000 (1,169,000 to 1,240,000) | 1,186,000 / 1,205,000 / 1,221,000 (three readings of step 7, below) | inside band |
| CC4 stretch adds | 340,000 (326,000 to 368,000) | 330,000 / 336,000 / 340,000 | inside band |

Per channel, steps 6 and 7 executed as written (8 channels, 104 weeks, Thursday month, weekly value series priced by first-48-hour value at the 52-week worth, both levels calibrated). "The share term left at its two-year average" reads three ways:

| Channel | Blocks: return, stretch, per install, next euro | Mean of the log share (the literal reading) | Share at the two-year ratio (return) | Share term averaged in levels over the 104 weeks |
|---|---|---|---|---|
| Pinterest iOS | 1.66, 1.29, 10.93, 0.92 | 1.63, 1.27, **11.02**, 0.90 | 1.65 | 1.67, 1.30, **11.02**, 0.93 |
| Google iOS | 1.43, 1.24, 9.87, 0.76 | 1.39, 1.21, 9.86, 0.74 | 1.41 | 1.43, 1.24, 9.86, 0.76 |
| Meta iOS | 1.07, 0.95, 8.81, 0.57 | 1.05, 0.93, 8.84, 0.56 | 1.06 | 1.08, 0.95, 8.84, 0.57 |
| Google Android | 1.03, 0.93, 9.72, 0.55 | 1.00, 0.90, 9.72, 0.53 | 1.02 | 1.04, 0.93, 9.72, 0.55 |
| AppLovin Android | 1.03, 0.87, 5.27, 0.71 | 0.99, 0.83, 5.26, 0.68 | 1.01 | 1.03, 0.86, 5.26, 0.70 |
| Snapchat iOS | 0.64, 0.61, 7.53, 0.39 | 0.62, 0.59, 7.52, 0.38 | 0.63 | 0.64, 0.60, 7.52, 0.39 |
| TikTok iOS | 0.61, 0.58, 6.22, 0.36 | 0.59, 0.56, 6.24, 0.35 | 0.61 | 0.61, 0.58, 6.24, 0.36 |

All seven bands match in every column. Every figure is inside its stated band except Pinterest's per install (11.02 against 10.53 to 11.01, fix 1). The blocks' levels are reproduced to within 0.01 on each return only by the last column, which the sentence does not say (fix 2). The golden CSV, the workbook's first sheet and the blocks carry one set of figures.

## Evidence: the three kinds of claim in the closing passage

### 1. The listed defensible ways (33 run, each under up to nine carries: calibrated or as fitted, with or without smearing, share at its mean log, its ratio or its level average)

No way moves a band. Figures of listed ways that land outside a stated band:

| Way | Figure | Value | Band | Under which carry |
|---|---|---|---|---|
| The golden method itself and 15 of the listed ways | Pinterest per install | 11.02 to 11.05 | 10.53 to 11.01 | most carries |
| Apple Search Ads' own ratio, as one number (0.724) | Pinterest per install | 11.11 to 11.16 | 10.53 to 11.01 | all |
| same | Google iOS per install | 9.98 to 10.05 | 9.59 to 9.97 | all |
| same | CC3 | 1,243,000 to 1,247,000 | 1,169,000 to 1,240,000 | level average |
| Apple Search Ads' own ratio, value by value | Pinterest per install | 11.04 to 11.09 | 10.53 to 11.01 | all |
| Each channel's own month pattern | Google Android next euro | 0.49 | 0.50 to 0.57 | mean log |
| same | Snapchat stretch; CC4 | 0.57; 325,000 | 0.58 to 0.63; from 326,000 | as fitted, mean log |
| Installs fitted on the 52 complete weeks | CC4 | 321,000 to 325,000 | from 326,000 | mean log |
| same | Pinterest next euro | 0.86 | 0.87 to 1.03 | as fitted, mean log |
| Last 78 weeks | CC4 | 320,000 to 322,000 | from 326,000 | mean log |
| One value slope across channels | Snapchat stretch | 0.57 | 0.58 to 0.63 | as fitted, mean log |
| A postback placed four days back | Pinterest next euro | 0.86 | 0.87 to 1.03 | as fitted, mean log |
| Budget alone | Google iOS stretch | 1.16 | 1.17 to 1.27 | as fitted |
| Delivery share from the complete weeks, budget conversion only | Snapchat return; stretch | 0.60; 0.57 | 0.61 to 0.66; 0.58 to 0.63 | as fitted, mean log |
| Delivery share from the complete weeks, share term from those weeks too | AppLovin Android return; stretch | 0.94; 0.78 to 0.79 | 0.96 to 1.07; 0.81 to 0.90 | mean log |
| same | Google Android return; stretch | 0.96 to 0.97; 0.87 | 0.98 to 1.08; 0.88 to 0.96 | mean log |
| same | Google iOS return; CC4 | 1.35; 321,000 to 323,000 | 1.36 to 1.46; from 326,000 | mean log |

Apart from the shared Pinterest figure, inside every band under every carry: one fit across both stores, the two-rate continuation, the 30-day cadence, the fit without its last two months, refunds netted from the renewals, annual trials at the monthly share, the two rates fitted together, the web subscribers' continuation (0.892; CC1 35.26), eight or four groups (by the sessions bucket, by the trial and purchase bits, by eighths or quarters of the value), cells of fifty or more, the accounts with no channel's own value by value, the plan's seven channels alone, without the launch quarter, the complete weeks' own values, a trend or a second-year level, spend instrumented by the budget. CC1 runs 34.57 to 35.26 and CC2 9.07 to 9.27 across all of them, inside their bands. Not run: calendar-month cadence, App Store days as UTC, refunds on the refund's day, one tilt per source.

### 2. The four ways said to be refuted

| Way | Refuting figure, blocks | Recomputed | Sound on the files alone? | Its figures against the bands |
|---|---|---|---|---|
| A week's month from its Monday | plan spend changes on 10 weeks, each the first whose Thursday is in a new month; on 4 the Monday is in the old month | 10; all 10; 4 | Yes: the plan files its own weeks by the Thursday | Inside: returns 1.62 1.40 1.05 0.99 0.99 0.63 0.59 (mean log), all 28 in band; at the level average only Google Android's next euro leaves (0.58 against 0.50 to 0.57). "Sit outside the bands" is not true of this way (fix 7b); harmless. |
| Both equations in levels, or in levels on the logs | miss 8.7 and 10.3 per cent against 4.0 over 286 moved weeks, more on every channel | 286 weeks in 72 moves; 8.5 to 8.6 and 9.9 to 10.3 against 4.0; more on all 8 channels | Yes | Levels: Pinterest return 1.71, CC4 319,000 out. On the logs: Google Android 0.96 to 0.97, CC4 304,000 out. Same seven bands. |
| One price ratio for all first-48-hour values | prices Apple Search Ads' 10,068 unnamed installs at 10.72 against 11.71 | 10.73 against 11.71 (one cell, ratio 0.503) | Yes | Meta per install 9.13, Snapchat per install 7.92, CC4 375,000 to 387,000 out. Same seven bands. The neighbour with cells by value and one ratio (0.699) prices Apple Search Ads at 11.32 and sits inside every band; it is in neither list and needs no action. |
| Annual trials left out | stores report 989 and 1,190 annual first charges beyond the records | 989; 1,190 | Yes | CC1 33.6, AppLovin per install 5.17 out. Same seven bands. |

None of the four is still defensible on my reading, and none moves a band.

### 3. Robustness

| Statement | Recomputed |
|---|---|
| Each channel's two budget slopes moved a fifth | No band moves in four combinations; nearest Google Android 0.92 (installs slope up, value slope down) |
| Unnamed installs' price ratio moved a fifth | No band moves; Meta iOS 0.93 to 1.196 (0.004 under the scale line at the level average) |
| Stores' fitted rates moved a fifth | No band moves: trial shares 0.98 to 1.04 on AppLovin; one minus the continuation 0.96 to 1.07; the whole fitted excess 0.92 to 1.10 |
| Delivery share moved 9.6 per cent | 9.6 per cent reproduced (AppLovin Android's widest quarter). Holds when only the budget conversion moves (at the level average Google Android 0.99 to 1.09, AppLovin 0.97 to 1.10). With the share term moved as well it does not: Google Android 0.88 and AppLovin Android 0.88 at the mean log, about 0.91 and 0.92 at the level average, because a return moves 1.0 to 1.3 per cent per one per cent of share at fixed spend (fix 7c) |
| Each shortcut keeps its channel in the wrong band however the response is carried | AppLovin 0.77 to 0.81 (stated 0.77 to 0.81); Meta 1.29 to 1.33 (1.30 to 1.33); Google Android 0.79 to 0.85 (0.79 to 0.85) |
| Singly or together, 7 different wrong sets | 7 of 7 distinct; all three together Meta 1.35, Google Android 0.80, AppLovin 0.74, as the Final Recommendation states |
| "The fit on spend passes a hold-out of weeks" | Random fifth of weeks held out, 20 draws: mean miss 11.0 per cent for the spend fit, 4.2 for the budget fit |

## Further forks run (not in the passage)

| # | Fork | Returns (Pin, GiOS, Meta, GA, AL, Snap, TikTok) | Call | Figures leaving a band |
|---|---|---|---|---|
| 1 | 365 days and install week from `install_time` | identical to three decimals | same | none: no charge falls between the two clocks; 23 accounts change week |
| 2 | Postback 3.5 days back | 1.63 1.39 1.05 1.00 0.99 0.62 0.59 | same | none |
| 3 | Poisson for installs | 1.63 1.39 1.05 0.99 0.99 0.62 0.59 | same | none new |
| 4 | Named cells under 10, 20, 30, 50, 100 installs pooled | Pinterest per install 10.98, 10.97, 10.96, 10.96, 10.95 | same | none; closes the Pinterest gap (fix 1) |
| 5 | Delivery share and share term from the last 52 weeks | 1.62 1.43 1.04 1.04 1.04 0.60 0.60 (mean log); 1.66 1.48 1.06 1.06 1.07 0.61 0.62 (level average) | same | Snapchat 0.59 to 0.60 and stretch 0.56 to 0.57; Google iOS 1.48 and stretch 1.28 (fix 6) |
| 6 | From the last 26 weeks; the last 13 | Google Android 1.09 to 1.14, Google iOS 1.48 to 1.54, Snapchat 0.56 to 0.61, AppLovin 0.99 to 1.06 | same | several; shown for the margin, a quarter is not a forecasting base |
| 7 | Share trend carried to mid-2027 (log share trends: Google Android +0.054 a year, t 2.3; AppLovin +0.062, t 2.5; Google iOS +0.060, t 2.7; Snapchat -0.073, t -3.6) | 1.62 to 1.66, 1.58 to 1.62, 1.00 to 1.03, 1.13 to 1.17, 1.11 to 1.16, 0.54 to 0.55, 0.64 to 0.66 | same | the outermost variant; nearest Google Android 0.033 under the scale line |
| 8 | Weekly value series by eight groups | 1.60 1.40 1.06 1.00 1.00 0.63 0.60 | same | none |
| 9 | Weekly value series by the trial and purchase bits alone | 1.58 1.40 1.06 0.97 0.98 0.63 0.59 | same | Google Android return 0.97, per install 9.40, next euro 0.58 to 0.60; coarser than the value step 6 names |
| 10 | No value response (value per install held flat) | 1.50 1.41 1.08 0.92 0.96 0.63 0.61 | same | many; a shortcut, same bands |
| 11 | No month pattern | 1.58 1.42 1.06 0.96 0.98 0.64 0.60 | same | several; ruled out, the month pattern's F(11, 797) is 55 |
| 12 | One ratio with cells by value | 1.61 1.39 1.05 1.00 0.99 0.62 0.60 | same | none |
| 13 | Blocks' rounded rates against fitted | 1.63 1.39 1.05 1.00 0.99 0.62 0.59 | same | none new |
| 14 | Test campaigns' spend, reinstalls, Apple Search Ads as a placed channel, annual renewals | not forks: policy 2.1, 2.2, 1.2; an annual renewal falls after day 365 | | |

Nearest approach to a line among the listed ways: AppLovin Android 0.969 (delivery share from the complete weeks, as fitted, share at its ratio), 0.069 above 0.90; 0.936 to 0.941 if that way also takes the share term from those weeks.

### Rivals

| Rival | Lands | Ruled out by |
|---|---|---|
| Records trued up in proportion, store month by store month | AppLovin Android 0.77 to 0.81, cut | AppLovin's 391 web subscribers set to renew, every charge on file: EUR 40.15 each after the last open inside twelve months, the fitted rule 36.4 to 36.5, in proportion about 11 to 12 |
| Every postback at the named installs' value | Meta iOS 1.29 to 1.33, scale | The 124,321 accounts with no channel paid EUR 927,073, that pricing gives 1.43 times it; Apple Search Ads' 10,068 untracked installs paid 11.71 against 16.19 |
| Response fitted on spend | Google Android 0.84 to 0.85, cut | Google Android's 33 moved weeks, each move left out: raised over lowered 1.36 actual, 1.41 from the budget fit, 1.82 from the spend fit; over all 286 moved weeks the spend fit misses by 14.0 per cent against 4.0 |
| No response model, the 52 complete weeks' value over spend | Google Android 0.80, cut (AppLovin 0.92, Meta 1.16) | The plan gives Google Android EUR 5,794 a week against 9,406 in those weeks, and the same moved weeks show installs rising 0.70 per cent per one per cent of budget; the asks (stretch spend, one more euro) presuppose a response |
| Strongest rigorous rival: spend instrumented by the budget | 1.61 to 1.66, 1.37 to 1.42, 1.04 to 1.08, 1.01 to 1.05, 0.99 to 1.03, 0.62 to 0.64, 0.60 to 0.62 | same seven bands, every figure inside its band |

## Gates B, D, E

Clean. The lines (0.90, 1.20), the three bands, the return, the install, the 365 days, VAT, the commission and the fee, the prices, the marginal return's "every week raised in the same proportion" and the brand sheet's exclusion are in the policy PDF (one page, text and table extracted); the 48-hour window and the 24 to 48 hours to the postback are in the JSON; the plan's Thursday blocks are in the plan; the budget moves are in the `Changes` sheet (286 weeks under both the planned-weeks and the back-to-base reading). Every term of the Final Recommendation appears in an input. Each ask carries its unit and pins one answer; the prompt names no method and no file.

## The eight fixes of pass 1

| Pass 1 fix | Status |
|---|---|
| 1 Google Android and AppLovin Android bands | Closed: the literal rebuild is inside all eight of their bands under each reading (Google Android 1.00 to 1.04, AppLovin 0.99 to 1.03) |
| 2 Four rules of steps 6 and 7 | Three closed (Thursday month, the weekly value series, Apple Search Ads in the shared pattern: all slopes now reproduce). The share rule is stated but reads three ways (fix 2 below). Google Android, AppLovin Android and Pinterest iOS now land at 1.04, 1.03 and 1.67 against 1.03, 1.03 and 1.66 under the level average, and at 1.00, 0.99 and 1.63 under the literal mean log |
| 3 CC4 band against the group variants | Closed: eight groups 339,000 to 350,000, four groups 344,000 to 354,000; one price is now listed as refuted |
| 4 The clock | Closed by the pack: the two clocks give the same figures |
| 5 Annual trials | Closed |
| 6 A ratio per first-48-hour value | Closed |
| 7 The 1.36 as a ratio of totals | Closed |
| 8 "Closest to a line" | Not closed: 0.077 does not recompute (fix 7a below) |

## Fix (location: solution, all of it)

1. **Pinterest iOS per install, band top (item 3).** Step 5 states no rule for thin cells. Without one Pinterest's unnamed installs price at 7.88 (all installs 10.15) and the per-install figure is 11.02, and 11.02 to 11.05 across the listed ways for the stores' excess, against a band of 10.53 to 11.01. The workbook's 7.83 and 10.12 come back only when a named cell under about 10 to 20 installs takes the pooled value (then 10.97 to 10.98). Add that sentence to step 5 with the threshold used, or raise the top to 11.05 (11.16 if fix 4 keeps the Apple Search Ads ways as they are). Clearance: the true-up in proportion gives 11.65 and the named value 13.51; the spend fit's 10.93 is inside already.
2. **Step 7, "the share term left at its two-year average": name the average.** Read as the average of the term (the slope times the mean log share) the step gives 1.63 1.39 1.05 1.00 0.99 0.62 0.59, CC3 1,186,000 and CC4 330,000. The stated figures come back (each return within 0.01, CC3 1,221,000, CC4 340,000, installs a week within 0.6 per cent of the workbook's) only when the share raised to its slope is averaged over the 104 weeks. All readings are inside the bands, so this is one sentence, but it is the one a rebuild has to guess.
3. **Low band edges under the mean-log reading crossed with listed ways.** CC4: 320,000 to 325,000 (installs fitted on the 52 complete weeks, the last 78 weeks, own month pattern) against a band from 326,000; lower to 320,000 (the true-up in proportion gives 297,000 to 307,000). Google Android next euro 0.49 (own month pattern) against 0.50: lower to 0.49. Snapchat stretch 0.57 and return 0.60 against 0.58 and 0.61: lower to 0.57 and 0.60 (the shortcuts give 0.53, 0.73 and 0.66 on the stretch). Pinterest next euro 0.86 against 0.87: lower to 0.86. Google iOS stretch 1.16 (budget alone, as fitted) against 1.17: lower to 1.16.
4. **"Apple Search Ads' own ratio" in the defensible list.** As one number (0.724 against the adding-up 0.699) it gives Google iOS per install 9.98 to 10.05 (band top 9.97), Pinterest per install 11.11 to 11.16 and, at the golden's level, CC3 1,243,000 to 1,247,000 (band top 1,240,000), and it prices the accounts with no channel 3.5 per cent over what they paid. Say "value by value" (then only Pinterest's per install leaves, 11.04 to 11.09, covered by fix 1 at 11.10) or strike it from the list.
5. **"The delivery share from the complete weeks" in the defensible list.** Say it changes the budget conversion only. If the share term is taken from those weeks as well, the mean-log carry gives AppLovin Android 0.94 and stretch 0.78 to 0.79 (bands from 0.96 and 0.81), Google Android 0.96 to 0.97 and stretch 0.87 (from 0.98 and 0.88), Google iOS 1.35 (from 1.36). Widening instead would put AppLovin's low edge at 0.94, which takes in the spend fit's AppLovin figure (0.93 to 0.95), so the wording is the cheaper repair.
6. **The delivery share of the most recent 52 weeks is a defensible forecasting base the bands do not cover.** The share trends on four channels (fork 7 above). It gives Snapchat 0.59 to 0.60 and stretch 0.56 to 0.57 (bands from 0.61 and 0.58) and, at the level average, Google iOS 1.48 and stretch 1.28 (band tops 1.46 and 1.27). Widen those four edges (0.59, 0.56, 1.48, 1.28), or add it to the refuted ways with a figure that refutes it; I found none. No band of the policy moves under any window (first 52, last 52, last 26, last 13 weeks, or the trend carried to mid-2027).
7. **Closing passage, three statements that do not recompute.** (a) "The closest any comes to a line is AppLovin Android at 0.077": I get 0.069 for a listed way (delivery share from the complete weeks, as fitted, share at its ratio, AppLovin 0.969). (b) "Four ways ... sit outside the bands": the Monday month sits inside (all 28 figures at the mean log; only Google Android's next euro, 0.58 against 0.57, at the level average); say three of the four sit outside. (c) "with the delivery share moved by the 9.6 per cent": true only when the budget conversion alone moves; with the share term moved too Google Android and AppLovin Android come to 0.88 at the mean log. Say what was moved, or cite the windows of fix 6, under which no band moves.
8. **Small Step-by-Step figures.** Step 3 says "by store and period" without the period; the workbook uses 30.4375-day periods from 4 November 2024, and on calendar months I get a Google Play continuation of 0.887, shares of 13.4 to 34.8 and 16.2 to 18.7, and EUR 927,073. Name the period. Step 4's web check mixes bases: 40.15 is per the 391 accounts set to renew and 36.50 per the 390 with a charge before the last open (one base gives 40.15 and 36.41, or 40.25 and 36.50). The levels equations miss by 8.5 to 8.6 per cent on my rebuild against the 8.7 stated.

## Pass 1

Pass 1 (same day, the earlier cut) returned DETERMINISTIC with SOLUTION_WRONG and FIX_NOW: the seven bands held in 30 forks and against four rivals, but the literal rebuild put Google Android outside three of its four bands, steps 6 and 7 left four rules to be guessed (the week's month, the weeks of the value fit, the share's treatment, Apple Search Ads in the month pattern), CC4's band excluded group variants the passage called defensible, the figures reproduced only on the `created_at` clock, step 4 gave no rate for annual trials, step 5 did not say the ratio was per first-48-hour value, the 1.36 was not described as a ratio of totals, and the closing "closest to a line" figure did not recompute. Seven of those eight are closed in this cut (table above); the eighth is fix 7a.
