# task1 determinism check, pass 2 (run a7r2)

Working copy: `/tmp/determinism-task1-a7r2/target/` (fresh unzip, 14 files). Scripts and outputs: `/tmp/determinism-task1-a7r2/work/` (`prep.py`, `pipe.py`, `pipe5.py`, `pipe67.py`, `chain.py`, `fam2.py`, `ref4.py`, `fix5.py`, `more.py`, `resp.py`, `deliv.py`, `combo.py`, `asa.py`). Every figure below came from those scripts. Gates A to E only.

**Verdict:** DETERMINISTIC, SOLUTION_WRONG. The seven bands are forced on every route that survives a figure from the files. The thinnest is AppLovin Android at 0.912 under the year-1 ratio plug-in. Several stated ranges do not hold routes the closing passage names, or a defensible rival, and that includes **CC3**. Some refusals rest on figures that do not reproduce. So the blocks need range and wording repair.

**Disposition:** FIX_NOW. All the edits are to `submission.md` (ranges, and one wording fix). Solvers see nothing different and no rerun is needed.

## Golden replay (the Step-by-Step's own method on the shipped files)

Step 1 reproduces exactly: 748,034 consumer accounts (163 out), 335 re-sent web rows, 1,190 refunded first charges, and 85 postback halves dated before week 0. Step 3 reproduces exactly: 218,632/137,053 and 253,559/173,292 renewals; 836/935 and 369/395 first charges. Step 4 reproduces exactly: 9,281 and 9,035 candidates; trials 24,884/8,907/31,410/11,762; shares 0.034/0.030/0.041/0.034; continuation 0.971/0.970; take-in 80,056 of 80,168 (Google Play) and 78,671 of 78,841 (App Store, against 78,668). Step 5 reproduces within the third decimal: 156 market-weeks, 138,896 accounts (110,626 network, 28,270 organic), paid EUR 951,767. Step 6 reproduces exactly: Google Android slope 0.713 against 1.046 on spend.

| Figure | Blocks (range) | Recomputed | In range |
|---|---|---|---|
| CC1 AppLovin Android year value | 4.87 (4.82-4.95) | 4.869 (records 3.133) | yes |
| CC2 Meta iOS year value | 5.78 (5.40-6.34) | 5.790 (named 10.581) | yes |
| CC3 Google Android installs/wk | 611 (584-633) | 610.8 | yes |
| Return at plan: Pin / GiOS / Meta / GA / AppL / Snap / TikTok | 1.578 / 1.450 / 1.050 / 1.039 / 0.969 / 0.621 / 0.549 | 1.578 / 1.449 / 1.051 / 1.039 / 0.969 / 0.621 / 0.549 | all |
| Stretch return | 1.175 / 1.250 / 0.928 / 0.941 / 0.846 / 0.583 / 0.519 | 1.177 / 1.249 / 0.929 / 0.941 / 0.847 / 0.584 / 0.519 | all |
| Installs/wk | 325 / 624 / 789 / 611 / 932 / 643 / 750 | 324.8 / 624.0 / 788.6 / 610.8 / 931.6 / 642.5 / 750.0 | all |
| Value per install at plan | 10.20 / 9.36 / 5.64 / 9.33 / 4.94 / 5.93 / 4.79 | 10.21 / 9.36 / 5.65 / 9.33 / 4.94 / 5.93 / 4.79 | all |
| Marginal at plan | 0.746 / 0.730 / 0.556 / 0.576 / 0.616 / 0.342 / 0.327 | 0.750 / 0.733 / 0.557 / 0.576 / 0.617 / 0.343 / 0.327 | all |
| Marginal at stretch | 0.556 / 0.629 / 0.492 / 0.522 / 0.538 / 0.321 / 0.309 | 0.559 / 0.632 / 0.492 / 0.522 / 0.539 / 0.322 / 0.309 | all |
| Year value (Q4) | 9.37 / 9.47 / 5.78 / 8.60 / 4.87 / 6.10 / 4.98 | 9.38 / 9.46 / 5.79 / 8.60 / 4.87 / 6.11 / 4.97 | all |

Nearest the line: AppLovin Android at 0.969 (0.069 above 0.90) and Meta iOS at 1.051. AppLovin's figures carry the narrowest ranges (CC1 4.82 to 4.95; plan value per install 4.86 to 5.02). Pinterest's installs have the widest marginal range (0.701 to 0.888), and its installs range tops out 1.5 per cent above the figure, at 330. Across the accepted variants Pinterest's installs ran 314.7 to 326.5, all inside.

The plan's blocks change on the Thursday's month. They change on 31 May, 28 June, 30 August and 29 November 2027, which are Mondays whose Thursday falls in the next month. So step 6's "as the plan's blocks do" is true.

## Battery, each way alone, run end to end (steps 4 to 7 re-run for every variant)

Every one of these filed SSHHHCC with every figure inside its range: pooled continuation; two-rate (0.983 then 0.970/0.967); without the last two periods; 30-day; calendar months; App Store on UTC days; one share for every trial; `install_time` clock; refunds netted; dating counted from the first charge (0.9714/0.9701); minimum cell 50; light/heavy split; unweighted; by fortnight; by four-week period; weighted by one over the fitted revenue; without market-weeks under 100; 3-day only; 4-day only; eight groups (sessions buckets, or trial and purchase crossed with light/heavy); every sharing the tests admit (G with P, G with O, P with O, G/P/O, M with T, T with S); own month pattern; without the launch quarter; last 78 weeks; the value response on the complete weeks' own 12-month values; one value slope; delivery share from year 1 (AppLovin 0.991) or year 2 (0.950); spend instrumented by budget; budget alone; Monday month.

I also ran corner pairs and one way per step at once: tworate+yr2 share, pooled+last78, P30+yr1, M=T sharing+yr1, fortnight+yr2, fourweek+Monday, tworate+fourweek+yr2 and P30+M=T+budget-only. All gave SSHHHCC and stayed inside every range. AppLovin's lowest was 0.950 and Meta's highest 1.090.

The narrow CC1 range held on every step-4 variant (AppLovin's value ran 4.85 to 4.88).

## Findings (all FIX_NOW, solution only)

**F1. The unscaled prediction at a single year's delivery share. The ranges do not hold its admissible forms, and the passage refuses the whole family on a figure that does not hold.**
- The route: the installs equation's own prediction at the plan, with the share and the plan's budget both put at one year's value.
- The passage replays a one-year share over both years' budgets and finds 88.0 to 107.5 per cent (I get 88.0 to 105.2). That test favours the 104-week share by construction.
- Replayed on its own year, the ratio plug-in adds up as well as the 104-week route does: year 1 gives 97.5 to 99.8 per cent (AppLovin 98.8), year 2 gives 97.6 to 99.6 (Snapchat 99.6). The share-distribution form (each week's share averaged in) adds up to 99.4 to 99.9 at 104 weeks.
- Single-year delivery is admissible by the blocks' own battery, which takes "the delivery share from the complete weeks or the last 52" in the scaled route. Drift does not separate the years: the quarterly year-1 against year-2 tests give p of 0.084 (AppLovin), 0.117 (Snapchat) and 0.165 (Google Android). So I rule these forms in.
- Their figures:
  - Year-1 ratio plug-in: AppLovin 0.912 (hold), stretch 0.797. **CC3, Google Android installs, 581.6 (range 584 to 633).** Google Android return 0.985 (range from 0.992), stretch 0.892 (from 0.898). Google iOS installs 601.5 (from 605). AppLovin installs 881.8 (from 888).
  - Year-2 ratio plug-in: Snapchat iOS installs 612 (from 620).
  - Share-distribution form: year 1 gives AppLovin 0.920 (from 0.921). Year 2 gives AppLovin 1.008 (top 1.000), Snapchat installs 618.6 and Google iOS installs 643.3 (top 642).
  - Every one of these files SSHHHCC.
- **Fix (solution), applied to the Supplementary Questions, the CSV's brackets and the Critical Components:**
  - **CC3 and 2d, Google Android installs, to 575 to 633.**
  - 1d Google Android to 0.975 to 1.073 at the plan and 0.883 to 0.965 at the stretch.
  - 1e AppLovin to 0.903 to 1.018 and 0.789 to 0.881.
  - 2b Google iOS installs to 595 to 650.
  - 2e AppLovin installs to 873 to 965.
  - 2f Snapchat iOS installs to 605 to 669.
  - Then rewrite the passage's sentence "With the share taken from one of the two years alone the unscaled prediction is refused ..." to admit the ratio and share-distribution forms, and to refuse the geo and median plug-ins on the figure in F1b.

**F1b. The year-1 geo and median plug-ins (AppLovin cut) are refuted, but on their own-year add-up, not the passage's figure.**
- They give AppLovin 0.891 and 0.885. This reproduces the blocks exactly, with both-years add-ups of 88.9 and 88.0.
- Replayed on the year whose delivery they assume, they add up to only 95.4 and 94.4 per cent of AppLovin's installs counted. The ratio plug-in of the same year gives 98.8 and the share-distribution form 99.5.
- So they under-predict their own history by 4.6 to 5.6 per cent: the gap between a point share and the share's average effect, under an elasticity of about 1.86. Every year-1 form that reproduces its own year keeps AppLovin on hold, at 0.912 and 0.920. The call is therefore forced, but thinly on this family: 0.912 is 0.012 above the line.
- By the same criterion, the 104-week geo and median plug-ins the passage accepts (95.8 and 95.0 on their own period) are refused too. They file the same bands, so only the sentence changes.
- The refusal should quote 95.4 and 94.4 against 98.8 and 99.5, not the both-years 88.9 and 88.0. Do not rest it on drift: the quarterly tests do not reach 5 per cent.

**F2. "The first-48-hour values in eight or four groups": four groups leaves Q3 ranges.**
- Sessions pairs:
  - Google iOS marginal: 0.827 at the plan (top 0.814) and 0.726 at the stretch (top 0.712).
  - Meta iOS: 0.612 (top 0.610) and 0.549 (top 0.540).
  - Snapchat iOS: 0.385 (top 0.378) and 0.364 (top 0.357).
- Trial-by-purchase groups: Meta iOS 0.611 and 0.548; Snapchat iOS 0.384 and 0.364.
- Bands unchanged.
- **Fix:** either name the four groups in that sentence (if the build's grouping lands inside, say which), or widen:
  - 3b Google iOS to 0.596 to 0.836 at the plan and 0.502 to 0.734 at the stretch.
  - 3c Meta iOS to 0.428 to 0.618 and 0.367 to 0.555.
  - 3f Snapchat iOS to 0.268 to 0.389 and 0.248 to 0.368.

**F3. "The value response on the complete weeks' own values" is read one way, and a neighbour leaves TikTok's marginal range.**
- Fitting the value equation on the 52 complete weeks' own 12-month values lands inside.
- Fitting it on the same priced values restricted to the 52 complete weeks (a natural sample choice) gives TikTok iOS 0.283 at the plan (bottom 0.299) and 0.265 at the stretch (bottom 0.283). With 3-day dating it gives 0.288.
- **Fix:** widen 3g to 0.280 to 0.395 and 0.262 to 0.379. Or rule the priced-values version out by a figure in the closing passage.

**F4. "Weighted by the fitted revenue" read literally (weights proportional to the fitted revenue) breaks CC2 in Family 1.**
- On sessions-pair cells it gives Meta iOS 0.975 (range 0.981 to 1.151), stretch 0.862 (0.867), plan value per install 5.24 (5.26) and year value 5.37 (CC2 range 5.40 to 6.34).
- Weighted by one over the fitted revenue it lands inside (1.050, 5.78). In the main battery both readings land inside (1.016 and 1.064).
- **Fix (solution wording):** write "weighted by one over the fitted revenue" in the battery sentence and in the Family 1 sentence. If the literal weighting is what was run, widen CC2 and Supplementary 4c to 5.32 to 6.34, 1c to 0.965 to 1.151 at the plan and 0.853 to 1.018 at the stretch, and 2c's value per install to 5.18 to 6.18.

**F6. The straight line's refusal figure does not reproduce. The route is refuted by other figures, and the bands hold.**
- Installs linear in the budget, with the same month pattern and log delivery term: adding the log budget channel by channel gives F 0.21 (0.27 with the share linear, 1.96 weighted by one over the fitted value squared). The passage says 2.7 against 1.95.
- Carried through step 7, the straight line files SSHHHCC: AppLovin 0.960, Google Android 1.055 and CC3 620.6 (inside). Graded figures move out of range: Pinterest installs 334.5 (top 330), Pinterest marginal 0.542 (from 0.701), Google Android marginal 0.487 (from 0.531), Meta stretch marginal 0.576 (top 0.540), and Snapchat marginals 0.385 and 0.377.
- What refutes it from the files: with each move left out it misses the moved weeks' installs by 8.6 per cent, against 3.6 for the fitted form; held out every fourth week, 7.0 against 3.9; and it predicts Google Android's raised over lowered weeks at 1.487 against the observed 1.403 (fitted form 1.435).
- The exponential reproduces (F 32.6; its moved-weeks miss is 5.9 per cent).
- **Fix (solution):** in the response sentence of the refusals paragraph, replace "F 2.7" for the straight line with those moved-weeks figures (8.6 against 3.6 per cent; 1.487 against 1.403). If the build's 2.7 comes from a specific form, write the form down.

**F5 (wording, no figure moves).**
- Step 4's simpler way, "its store's ratio of charged to recorded", reproduces 3.70 and 0.736 only in euros (3.697). By counts it gives 3.865 and 0.770. Both are a cut. Add "in euros".
- I could not rebuild some refusal figures from the stated rules: the candidates' "one less the cancellations the app saw per charge on file" (0.912 and 0.905; my reading gives 0.794 and 0.785), the web-month fit (0.878 and 31.90; mine 0.869 and 30.55), and 352.6 and 90.1. Every refusal holds on my figures.
- Step 4 says charges are "counted from its first" in one clause and "30.4375 times j days on" after the last in another. Both give 0.971 and 0.970. Nothing graded moves.

## Refused routes, recomputed

| Route | Blocks | Recomputed | Refusal holds? |
|---|---|---|---|
| Stores' excess, scaled by period | AppL 3.70, 0.736; web subs 13.59 vs 31.79 | 3.697 (EUR basis) or 3.865 (counts), 0.736 or 0.770; 13.56 vs 31.79 | yes: puts 13.6 where the web record shows 31.79 |
| Scaled over the whole record | 0.778; 18.26 | 4.280 (counts), 0.852; 18.21 | yes (still a cut; 18.2 against 31.79) |
| Candidates carried at 0.912/0.905 | 54,435 / 51,511 | 54,545 / 51,597 | yes: about 68% of the 80,168 / 78,841 |
| Carried at 0.882 | 45,768 / 45,077 | 45,849 / 45,142 | yes |
| Unnamed valued like named | Meta 9.55, 1.734; 1.41x | 9.557, 1.736; 1.409x | yes: the identity is broken |
| Apple Search Ads' ratio | 1.561; 1.21x | 0.889 ratio: Meta 1.601; 1.25x | yes |
| Android ratio | Meta 1.280 | AppLovin's 0.625: Meta 1.282 (Google iOS 1.154) | yes: the fitted ratios are well identified (SE 0.029 to 0.047); 0.88x |
| One ratio / four social | tests 122.9, 119.3 / 74.0, 68.2 | 122.4, 119.1 / 75.2, 68.6; misses 8.96% / 7.75% against 6.33% | yes |
| Meta+TikTok+Snapchat shared | 17.5, 13.5; M=S 17.2, 13.4 | 17.7, 13.7; 17.4, 13.6 (Snapchat 0.562, out of range) | yes |
| Pairs admitted: M=T, T=S | 4.4/3.0, 4.5/3.2 | 4.3/2.9, 4.7/3.4 | admitted under one variance, inside range |
| Markets pooled | Google 0.702, Google iOS 1.237; SE 0.118 vs 0.039; miss 7.0 vs 6.4 | 0.696, 1.232; 0.117 vs 0.039; 7.05% against 6.29 to 6.34% for every accepted variant | yes, thinly; the bands are unchanged |
| Fit on spend | GA 0.851, 511; hold-out 10.0 vs 20.2; moves 13.1 vs 3.5; 1.403 / 1.434 / 1.872 | 0.851, 511; 10.1 to 11.5 vs 19.1 to 22.2; 13.5 vs 3.6 (72 moves, 286 weeks); 1.403 / 1.435 / 1.872 | yes |
| Year return carried over | 0.812; 8,910 vs 5,487 | 0.812; 8,910 vs 5,487 | yes |
| Straight line / exponential | F 2.7 and 33.0 vs 1.95; fitted form 1.1 | levels 0.21, exponential 32.6; log-log + budget 1.13 | exponential yes; straight line refuted only by the moved weeks (F6), bands hold |
| Value held flat | slopes -0.22 to -0.16, >= 6.0 SE | -0.222 to -0.158; t from -6.05 (Google Android) to -9.02 | yes |

## The two families run as they stand

- **Family 1** (sessions-split ratios):
  - The six cells, weighted by one over the accounts, unweighted, or by one over the fitted revenue, gave Meta iOS 0.993 to 1.146 and year values 5.47 to 6.31 (blocks 0.992 to 1.140 and 5.46 to 6.28).
  - All of them filed the same bands and stayed inside every range. Sessions with one over the accounts went 0.5 per cent past the blocks' span, inside the range but short of its "1 per cent beyond".
  - The literal fitted-revenue weight breaks CC2 (F4).
- **Family 2** (unscaled prediction):
  - At the 104 weeks' share (ratio, geo, median), AppLovin is 0.952, 0.937 and 0.931 (blocks 0.951, 0.936, 0.931), with add-ups of 98.2, 95.8 and 95.0. Every figure that moves lies inside its range by 1 per cent.
  - At one year's share, see F1 (ratio and share-distribution forms ruled in, ranges to widen) and F1b (geo and median refused on their own-year add-up).
- **Smearing** (Duan, factor 1.0007 to 1.0019) moves nothing.

## Independence and sensitivity

- Each simpler way alone flips only its own channel: AppLovin 0.770 (0.736 on the euro basis), Meta 1.736 and Google Android 0.851.
- Pairs:
  - Excess with unnamed: Meta 1.801, AppLovin 0.770.
  - Excess with response: Google Android 0.810, AppLovin 0.740.
  - Unnamed with response: Meta 1.825, Google Android 0.851, Snapchat 0.902, TikTok 0.904.
- All three together: Meta 1.894, Google Android 0.810, AppLovin 0.740.
- The directions match the blocks. Under the simpler excess, Meta's year value stays at 5.81 (inside), and Google Android's installs stay at 611 under the excess and unnamed ways.

## Gates B, D, E

- The decisive constants are filed: VAT, commissions, prices and the 0.90/1.20 lines in the policy PDF (2.4, 2.5, 3.1); the marginal's definition (2.6); unnamed installs counting to their channel (2.2); the postback timing and the sessions bits in the JSON; and the budgets, spend, plan and stretch.
- Every term of the recommendation appears in an input.
- Each ask pins its unit and population.
- The 30.4375-day period and the geometric continuation are conventions whose neighbours (30 days, calendar months, two-rate) land inside, so neither is a fork.
