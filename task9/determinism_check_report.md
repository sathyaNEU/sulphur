# task9 determinism check, pass 2 (re-judge after the Holistic Audit v2 closures)

The earlier pass (before the audit's closures) is in git history under this file name.
The pack was unzipped fresh from `target.zip`. Read: `prompt.txt`, the four graded blocks of `submission.md`, and
the standard and Schedule C as extracted text. Every figure below was recomputed on the shipped files.

- **Verdict:** DETERMINISTIC
- **Disposition:** FIX_NOW. Step 4 refuses two rivals (full accumulation, and the straight line through gaps 8 to
  26) with an argument and no figure; the edits add the figures, which I computed from the files. One optional
  sentence pins how step 6 counts the 2026 sources. These are edits to the answer blocks only: what solvers see does
  not change, and no rerun is needed.
- **Why:** each of the three audit forks is now closed by a filed sentence plus a figure from the files.
  - Section 1.5 refuses 10.27 for feature releases.
  - The ask's "expected to actually run" and the manifests' first-use lags refuse the calendar's 90.9 and 87.1.
  - Section 1.4 refuses the 3.57 endpoint. The bend in the score history refuses full accumulation, and the
    replicate pairs refuse the free fit.
  - Every defensible variant I ran stays inside its band, and every placement holds.

## Evidence: figures recomputed against the blocks

| Figure | Blocks (band) | Recomputed | Note |
|---|---|---|---|
| Panel merchants / identifiers / merchant-weeks | 29,580 / 34,148 / 3,360,865 | same | later load kept, Tolka map |
| Manifest lines / runs / production refits | 2,473 / 2,464 / 1,764 | same | |
| Bootstrap, replicate pair variance (book wt, 21 Sep 2026) | 259.89, 12.73 | 259.89, 12.73 | variance of the paired differences (ddof 0); mean square gives 260.12, 12.74 |
| Label revisions | 9.98 (9.92 to 10.05) | 9.98 (9.99 as mean square) | 13 x 7.667; label-freeze runs hold labels as of the prior week |
| Retunes | 4.47 (4.41 to 4.52) | 4.47 | 13/4 x 6.153; retune log cadence is 4 weeks in every family |
| Training data (CC1) | 6.62 (6.35 to 7.44) | 6.62 | window overlap, 104/52-week windows, plan rows |
| Optimisation noise (CC2) | 6.89 (6.05 to 7.40), p 0.79 to 0.95 | 6.89, p 0.7925 to 0.9475 | constrained curve, inverse-square weights, grid as stated |
| Free fit / implied replicate | 8.77 / 17.44 | 8.77 / 17.44 | |
| Line gaps 8 to 26; flat fit no floor | 5.96; 6.15 | 5.96; 6.15 | |
| Slip / first use after completion / fitted medians | 1.21; 3 to 31, median 14; 6.3 and 28.8 | 1.214; 3 to 31, 14; 6.31 and 28.76 | ISO-week counting |
| Reverted share | 4.4 | 4.4 | |
| Pinned share (ask 2) | 55.0 (53.2 to 60.0) | 55.01 | |
| Calendar planned / completed | 90.9 / 87.1 | 90.93 / 87.09 | |
| Feature releases | 6.65 (6.34 to 6.84) | 6.653 | release shadows, 24 roadmap releases, pinned weeks netted |
| FR left whole / on calendar | 10.27 / 4.00, 4.46 | 10.269 / 4.001, 4.457 | |
| Record gap 1 / gap 13 MSC, settled weeks | 42.34 / 509.15 | 42.34 / 509.15 | |
| Merchants' own share | 43.9 (41.9 to 47.0) | 43.4 to 44.9 by counting reading | see the optional fix |
| 2026 panel tier rate | 14.8 | 14.82 | |
| Tier 2027 / with four removed | 14.0 (13.7 to 14.6) / 9.7 (9.4 to 10.3) | 13.9 to 14.4 / 9.6 to 10.1 | all readings and starts in band |

## Forks run (Gate C)

| # | Choice | Alternative and its answer | Ruling |
|---|---|---|---|
| 1 | Releases on pinned weeks (audit fork 1) | left whole: FR 10.27, escalation | refused by standard 1.5, read literally |
| 2 | Pinned share basis (audit fork 2) | calendar planned 90.9 / completed 87.1: FR 4.00 / 4.46, monitor | refused by the ask's "actually run", the calendar legend (completed_on is the release to the environment) and the manifests' first use 3 to 31 weeks later |
| 3 | Take-up model form | log-linear, linear, by group, by family, pooled, empirical, plug-in median, with or without reverts: 54.8 to 59.6; FR 6.38 to 6.74 | same bands |
| 4 | Slip counted to the next Monday rather than the ISO week | 54.79; FR 6.665 | same bands |
| 5 | Lag measured from the planned week, no slip | 55.07; FR 6.655 | same bands |
| 6 | Retrain window: calendar-year Mondays of 2027 | 56.8 | in band |
| 7 | Share weighted by book, not family-weeks | 59.90 | in band (top 60.0); also ruled out by "share of weekly retrains" |
| 8 | Release effect scaled by feature groups changed | shadow variance by groups: 24.63 / 24.43 / 24.55 | refused by data: no scaling |
| 9 | FR at the settled weeks' release level | 9.67 | refused by standard 2.1 |
| 10 | Optimisation endpoint (audit fork 3) | 3.57, monitor | refused by standard 1.4 |
| 11 | Full accumulation (persistence 1) | 9.10 / 12.87, escalation | refused by data: all 14 families' lines have a positive intercept (35.6 pts sq through gaps 8 to 26, book wt), where persistence 1 puts every source through the origin. Weighted misfit at p = 1 is 3.4 to 34 (median) times the fitted curve's. In the cold era (DIGI, SUBS, TIXE, ELEC, TRVL) the curve is near linear. **Not in the blocks** |
| 12 | Free fit | 8.77, escalation | refused: implied replicate 17.44 against 12.73 measured |
| 13 | Straight-line intercept | gaps 1 to 26: 4.45 (monitor); 4 to 26: 5.21; 8 to 26: 5.96; 14 to 26: 6.90; 20 to 26: 7.50 | refused by data: the intercept moves with its first gap, so the curve is still bending, and a late-gap intercept estimates the ceiling, not the gap-13 value (p^13 up to 0.50). The fitted curve put through the same line on gaps 8 to 26 returns 5.51 against its own 6.89. **Not in the blocks** |
| 14 | Gap-fit variants | 20 or 30 gaps 6.85 / 6.94; flat 7.00; start at the last cold retrain +1 week 6.73 / 6.60; first warm 6.39 / 6.57; bf16 first use 6.77 / 6.18; bf16 +13 6.91 / 6.86 | same bands |
| 15 | The 6 Oct 2025 floor (a constant no file holds; the last bf16 first use is 24 Nov 2025) | no floor: optimisation 6.87 / 6.15 flat, own share 43.6 to 44.9, tier 14.2 to 14.4 / 9.8 to 10.1 | same bands, so closed |
| 16 | All weeks from July 2024 | optimisation 4.72 (monitor); own share 49.2 | refused by the manifests' cold-started refits (warm_start false) and the 26-week windows before the settled weeks |
| 17 | Training data: bootstrap at face | 15.72, escalation | refused by the record: weekly MSC is 42.34 against the route's 270.43 (step 7) |
| 18 | Training data: gross of seed, latest bootstrap pair, planned Dec 2027 book | 6.77 / 6.60 / 6.54 | same bands |
| 19 | Merchants' own as a share of the record | 39.2 | refused by standard 5.2's denominator |
| 20 | Label-freeze pair read as the whole gap | 2.77 | refused by the manifests: labels_as_of is the prior week |
| 21 | Tier weights, panel or book; denominator record or rebuilt | 14.12 to 14.13 / 9.91 | same bands |

## Rival figures in the Step-by-Step and what refuses them

Each of these is paired with a filed section or a figure:

- 15.72 (step 7: 270.43 against 42.34).
- 3.57 (section 1.4).
- 8.77 (17.44 against 12.73).
- 90.9 and 87.1, and 4.00 and 4.46 (the manifests' first-use lags).
- 10.27 (section 1.5).
- 9.67 (section 2.1).
- 39.2 (section 5.2).
- 4.8 and 50.0 (ten families' own change floored at zero).
- 49.2 (cold retrains and rollouts).
- The Final Recommendation's 15.72 and 9.10.

Two are refused by an argument only. The full sums (9.10, 12.87) are refused by "the bend itself, which no
persistence of 1 produces", and the line through gaps 8 to 26 (5.96, below the band floor of 6.05) by "while the
curve is still bending". Both refusals hold on the files (forks 11 and 13), but the blocks carry no figure for
either. The blocks themselves name 5.96 as the thinnest margin.

## Filed facts and the asks (Gates B, D, E)

- **Filed terms.** Everything the call uses is filed:
  - The bands are in 4.1; movement and its weights in 3.1 and 3.2; shares in 5.1 and 5.2; the tier test in 6.1 and
    Schedule C.
  - The pinned views and planned weeks are in the calendar; the roadmap's 24 releases, the plan rows and the book
    are filed.
- **The asks.** Each ask pins one answer:
  - Ask 2 is now worded as actual use, so the calendar reading no longer fits it.
  - "Share of weekly retrains" is counted in family-weeks.
  - The unit is per cent in the blocks; the prompt says "share" without a unit, which is a format question and not
    a fork.
- **Recommendation terms.** Monitor, remediation plan and escalation all appear in 4.1.

## Fix (location: solution)

1. **Step 4, full sums.** After "The full sums are refused by the bend itself, which no persistence of 1 produces",
   add: "every family's line through gaps 8 to 26 meets gap 0 above zero (35.6 points squared, book weighted),
   where a persistence of 1 puts every source through the origin, and the weighted misfit at a persistence of 1 is
   3.4 to 34 times the fitted curve's."
2. **Step 4, straight line.** Replace "a straight line through gaps 8 to 26 starts at 5.96 while the curve is still
   bending" with: "a straight line's intercept moves with its first gap (4.45 from gap 1, 5.96 from gap 8, 7.50
   from gap 20), so the curve is still bending, and the fitted curve put through the same line on gaps 8 to 26
   returns 5.51 against its own 6.89."
3. **Optional, step 6.** "As they stood" does not say how retunes and feature releases are counted. One sentence
   would pin it, for example: retunes as logged in each thirteen-week gap, releases by first scored refresh in each
   gap. The per-gap reading gives 43.4, a per-thirteen-week rate gives 44.9, and the blocks give 43.9; all are
   inside 41.9 to 47.0, and the tier figures stay inside their bands.

Not findings: the blocks' pair variances are variances of the paired differences, and a mean-square reading gives
label revisions 9.99, inside its band. The book-weighted pinned share sits 0.1 under the band top, and the ask's
wording rules that weighting out anyway.

## Disposition taken (main thread, 22 November 2026)

FIX_NOW applied in the generator, blocks only (`results.py` `bend`, `writeup.py` steps 4 and 6, asserted in `checks.py` and `verify.py`); the pack and the goldens rebuilt byte-identical. Findings 1 and 2 are in step 4 as figures computed on the cut pack: the line through gaps 8 to 26 meets gap 0 at 35.6 points squared book weighted and at 14.3 or more in every family; the misfit of a line through the origin is 3.4 times the fitted curve's or more, 34 at the median family (the range runs to 148, so the suggested '3.4 to 34' was written as a floor and a median); the line's start is 4.45, 5.96 and 7.50 from gaps 1, 8 and 20, and the fitted curve read the same way on gaps 8 to 26 returns 5.50 against its 6.89. Finding 3 is in step 6: retunes at one every fourth week and feature releases at the mean count a thirteen-week gap of the settled weeks holds. No second judge pass (`/fix-determinism` step 6).
