# Determinism check, pass 3 (architecture 8): Holistic Audit v4, Step 0, Part A and Part B

In-house replay, determinism mode, 2026-11-24, branch `task1-arch8-redesign`. Cut seen: prompt.txt
6ff254e53804b9204fd1f29a67dd920f, target.zip f4049ea8cb8e1f093e06abd50e203724, submission.md
c00684871c99e28ba04e08ed88d4af54 (14 input files; prompt not yet rewritten). No runs yet: Part B step 3's reading of
the runs and step 5 wait for the holistic pass.

**Verdict: DETERMINISTIC. Disposition: FIX_NOW** (three answer-block edits, nothing solvers see).

## Step 0

Golden present (all four fields carry computed values). Inputs belong to the task: Zancada, ES/IT/PT, the seven plan
channels, every file the Step-by-Step names is in the pack.

## Part A

Every figure derived from the shipped files first (own code in the workspace's `work/`), then compared.

| Figure | Mine | Author | Agree |
|---|---|---|---|
| Consumer accounts / staff+test out | 748,034 / 163 | 748,034 / 163 | yes |
| Refunded purchases | 1,171 | 1,171 | yes |
| GP renewals reported vs recorded | 167,359 vs 98,516 | same | yes |
| App Store renewals reported vs recorded | 181,074 vs 95,544 | same | yes |
| First monthly / annual charges beyond records (GP, AS) | 303, 409 / 153, 149 (only with refunded first charges kept on the records side) | 303, 409 / 153, 149 | yes, see Fix 1 |
| Renew-candidates with a charge on file (GP, AS) | 7,257, 8,510 | 7,257, 8,510 | yes |
| Trial candidates monthly/annual (GP; AS) | 24,411/8,761; 29,586/11,126 | same | yes |
| Trial-end share charged, monthly/annual (GP; AS) | 0.0124/0.0175; 0.0138/0.0134 | 0.012/0.017; 0.014/0.013 | yes |
| Continuation (GP, AS) | 0.9825, 0.9830 | 0.982, 0.983 | yes |
| AppLovin Android payments per 100, records / imputed (CC1) | 20.84 / 42.43 | 20.8 / 42.3 (41.3 to 43.2) | yes |
| AppLovin Android 12m net revenue per install, records / imputed | 2.658 / 4.182 | 2.66 / 4.17 | yes |
| Web referee: 201 subscribers, net EUR after last open | 201, 23.21 | 201, 23.21 | yes |
| Accounts with no channel, 52 weeks; networks' / organic | 138,896; 110,619 / 28,277 | same | yes |
| Named share of iOS networks | 26.3% to 27.6% | 26.3 to 27.6 | yes |
| Revenue ratios Meta/TikTok/Snap/Google/Pinterest/organic | 0.377/0.513/0.593/0.717/0.591/0.913 | 0.377/0.514/0.592/0.720/0.592/0.914 | yes |
| Payment ratios Meta, Google | 0.211, 0.639 | 0.211, 0.641 | yes |
| Meta iOS payments per 100 (CC2) | 33.0 | 33.0 (29.3 to 39.7) | yes |
| Payments per 100: Snap, Pinterest, TikTok, Google iOS, Google Android | 47.7, 53.6, 41.1, 60.4, 71.5 | 47.5, 53.4, 41.0, 60.5, 71.3 | yes (inside ranges) |
| Billed share of budgets, 104 weeks | 77.3% to 81.5% | 77.3 to 81.5 | yes |
| Moves on the Changes sheet / weeks | 72 / 286 | 72 / 286 | yes |
| Plan installs (CC3) | 232,809 | 232,900 (220,400 to 238,400) | yes |
| Plan 12m net revenue | EUR 1,284,897 | EUR 1,283,000 | yes |
| Returns Meta/TikTok/Snap/Google iOS/Pinterest/Google Android/AppLovin | 1.035/1.079/1.462/1.073/1.442/1.072/1.053 | 1.034/1.079/1.457/1.075/1.440/1.070/1.050 | yes |
| Bands | Snapchat iOS, Pinterest iOS scale; the other five hold; none cut | same | yes |

correctness: correct. decision_reproduces: yes. mismatches: none on a graded figure. Internal consistency: the
recommendation follows policy 3.1; 42.3, 33.0 and 232,900 are stated alike in the supplementary answers and the
components; sum of return x plan spend over the seven channels is about EUR 1,283,400, consistent with 1,283,000.
One block claim does not hold as written (Fix 2: the spend fit's quoted figure is not the one that moves a band). Fix 1 is a missing sentence and Fix 3 a metric to state.

Shortcut claims checked: the plan's spend read as a budget billed in full, in the fit's own prediction, gives
287,186 installs and Google iOS 1.398 here (blocks 287,400 and 1.391). Meta iOS 1.314, TikTok iOS 1.377, Google
Android 1.389 and AppLovin Android 1.370 all go to scale, matching the independence paragraph's plan-spend row
(blocks 1.314, 1.396, 1.390 and 1.348). Run over the record's own budgets at a share of one, the same equation
adds up to 140.4% to 152.6% of each plan channel's installs counted, as the blocks say (Apple Search Ads, not a
plan channel, 153.7%). A whole budget was billed in 2 to 9 of 104 weeks. The recorded GP monthly charges raised by
GP's charges over the recorded ones put AppLovin Android at 0.772 by period and 0.825 over the whole record (blocks
0.776 and 0.829), both cuts. On the 201 web subscribers the same scaling puts EUR 10.43 and 15.31 (blocks 10.47
and 15.36) against the EUR 23.21 they were charged.

Mismatches (incidental, no band moves): the best quarter's billed share is 82.5% to 94.7% on calendar quarters
here against the blocks' 79.5% to 87.9% (the blocks do not say how a quarter is cut). The leave-one-move-out misses
are 11.6% against 2.0% here, the blocks' 12.8% against 3.3% (Fix 3).

Not computed (no budget left for them, and none can change the verdict because each is a rejected route's
figure): the unnamed step's shortcut, "the gap the fully named channels show" (Meta iOS 1.541), and so the
Final Recommendation's three-shortcut figures (Google iOS 1.401, Meta iOS 1.882, AppLovin Android 0.863) and the
independence rows that use it; the every-fourth-week hold-out (9.9% against 20.2%); Google iOS's raised-over-lowered
installs (8.074, 8.208, 10.261); the source-sharing tests (55.73 and others); the summed-markets fit (TikTok iOS
1.273); and the straight-line and exponential F tests (3.6 and 39.6).

## Part B

**Committed call:** Snapchat iOS and Pinterest iOS scale, the other five hold, none cut. **Deciding steps** (three):
the renewals the stores report beyond the records; the value of the iOS installs the attribution export cannot
name; the plan's spend read as billed spend against a budget.

**Pins found**

- Store excess. Of 297,532 store charges on file, none falls after the account's last open (App Store 0 of 153,852,
  Google Play 0 of 143,680), against 9,323 of 61,883 web charges, and web records match the settlements file within
  42 payments a cell (61,883 vs 61,702). The early periods carry no excess (period 0: 0 and 0; period 1: 95 and
  135), so no subscriber from before the records absorbs it. The fitted continuation takes in the stores' excess
  (67,890 of 67,829; 84,274 of 84,419).
- Unnamed installs. The cell-level pro-rata split (every account with no channel in a market, week and conversion
  value worth the cell's mean, whatever its source) moves the call: Meta iOS goes to 52.4 payments per 100 and
  EUR 6.068 per install against 4.490. Run through the response fit, that gives Meta iOS 1.399, a scale (TikTok
  iOS 1.179, Pinterest iOS 1.543, Snapchat iOS 1.543, Google iOS 1.045). The files refute it. Adding the five
  networks' value terms to a model with a free value per conversion value (24 parameters) gives F(5,127) = 22.0. On
  a common value scaffold, six source ratios against one give F(5,150) = 24.9. Unattributed installs from different
  sources are worth different amounts at the same value.
- Plan spend. The plan's header says "weekly spend, EUR, as the platforms bill it", and policy 2.1 says "as the
  platform bills it". An OLS fit of installs on billed spend moves the call: Google Android 0.876, cut. It is
  refuted twice (the plan-as-budget reading, row 22 and its billed-in-full variant, is refuted under Part A's
  shortcut checks: 140% to 153% of the record's installs, a whole budget billed in 2 to 9 weeks of 104). The weekly budget adds to billed spend at F(8,797) = 684.3. The leave-one-move-out test over the
  72 logged moves misses by 11.6% on the spend fit against 2.0% on the budget-and-share fit (the blocks say 12.8%
  against 3.3%). The most rigorous standard neighbour, spend instrumented by budget, files the golden's seven bands
  with 232,571 installs.

**Fork list run** (bands against the golden's; returns marked ~ are the golden's return scaled by the 52-week
revenue per install, not re-run through the response fit)

| # | Fork | Figure it gives | Call |
|---|---|---|---|
| 1 | Records as they stand | AppLovin Android 20.8 per 100, ~0.669 | cut; refuted (store charges stop at last open) |
| 2 | Recorded GP monthly charges raised by GP's charges over the recorded ones, by period / whole record | AppLovin 0.772 / 0.825 (26.7 / 29.7 per 100) | cut; refuted: web referee scaled 10.43 / 15.31 against 23.21 charged, and no store charge after the last open |
| 3 | Continuation by store and country | c 0.981 to 0.985; AppLovin 42.40 | same |
| 4 | 30-day cadence | c 0.9805, 0.9815; AppLovin 42.34 | same |
| 5 | One trial-end share for every candidate (no sessions spread) | AppLovin 42.53 | same |
| 6 | Reconciliation without refunded first charges on the records side | first-charge share 0.029/0.031; AppLovin 42.89 | same, inside range |
| 7 | Pro-rata split of accounts with no channel by cell | Meta 52.4 per 100, 1.399 | **scale; refuted** F(5,127) = 22.0 |
| 8 | Common value scaffold, six ratios | Meta ratio 0.347 | same |
| 9 | Every postback dated back 3 days | Meta 34.7, ~1.065; Google iOS ~1.104 | same |
| 10 | Every postback dated back 4 days | Meta 33.6 | same |
| 11 | Ratios fitted unweighted | Meta 32.3, ~1.001; TikTok ~1.041 | same |
| 12 | Fallback at 50 named installs, not 20 | Meta 33.0 | same |
| 13 | Ratios by market (ES, IT, PT fits) | Meta 32.9 / 27.2 / 37.5, mix about 32.8 | same |
| 14 | Installs and value on billed spend (OLS) | 227,864 installs; Google Android 0.876, TikTok 1.170, Pinterest 1.240 | **Google Android cut; refuted** F(8,797) = 684.3, LOMO 11.6% vs 2.0% |
| 15 | Spend instrumented by budget | 232,571 installs | same |
| 16 | Budget alone, share term left out | 231,600 installs | same |
| 17 | Billed share from the last 52 weeks | 229,937 installs | same |
| 18 | One-week carryover (lagged log budget) | 231,470; Pinterest 1.308 | same |
| 19 | Quadratic in log budget | 232,499 | same |
| 20 | Value per install held at the 52-week figure | TikTok 1.119, Google Android 0.986 | same |
| 21 | A week's month from its Monday | 233,151 | same |
| 22 | Plan figures read as budgets, billed at the record's share | 195,884; AppLovin 0.888 | cut; refuted by the plan header and policy 2.1 |
| 23 | Plan figures read as a budget billed in full (own prediction, share 1) | 287,186; Google iOS 1.398, five hold channels go to scale | refuted: share-1 equation adds up to 140% to 153% of the record's installs; budgets billed in full in 2 to 9 weeks of 104 |

Constants no file holds, each run as a fork: the 30.4375-day period (row 4), the 3-or-4-day postback dating (the
SKAN file's 24 to 48 hours after a 48-hour window grounds it; rows 9 and 10), the 20-install fallback (row 12), the
1/accounts weights (row 11), the Thursday month (row 21). None moves a band.

**Data anomalies** (step 6): 897 twice-delivered postbacks and 1,984 redownloads are dropped. 237 re-sent web rows,
503 sandbox rows, 17,572 reinstall rows and 5,905 duplicate install ids are policy 2.2 or plain dedup. The
negative unnamed cells are 16 or fewer per network and total -8 installs. None moves a graded figure.

**Giveaways** (step 7): none. "hold" appears in the budget workbook only as budget hold-backs; no file states a
return, band or graded figure.

determinism: pinned. unpinned_forks: none. Rows 1, 2, 7, 14, 22 and 23 move the call; each is refuted by a figure
computed from the shipped files. Rows 7 and 14 are not in the blocks' account as band movers (Fix 2).

## Fix (solution only)

1. Step 4 (or step 3): say that the refunded first charges stay on the records' side when the records are set
   against the stores. That is the only way the 303/409 and 153/149 first charges and the 0.012/0.014 shares
   reproduce. Step 1 as written takes them out, which gives 705/927 and 0.029/0.031. AppLovin Android then reads
   42.9, inside its range, so the call holds.
2. "Each simpler way ... files a wrong band": the spend fit is quoted at Google iOS 1.114, which is a hold, the
   golden's own band. Name the band it actually moves: Google Android at 0.876 in this pass, a cut. Add the
   cell-level pro-rata split of the accounts with no channel (Meta iOS 52.4 payments per 100 and a return of
   1.399, a scale) with the figure that refutes it: the network value terms on top of a free value per conversion
   value, F(5,127) = 22.0.
3. Step 6: state how "misses the installs by" is measured. On the aggregate installs of each move's weeks, averaged
   over the 72 moves, this pass gets 11.6% (spend) against 2.0% (budget and share), not 12.8% against 3.3%.
