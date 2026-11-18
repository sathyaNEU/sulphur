# task9 determinism check (Gates A to E), pass 2: the re-judge after the repair

Pack: `target.zip` md5 abc02f617fed2851bdf205acb11cb4eb, unzipped fresh and recomputed with my own code
(session scratchpad, `scripts/p2/`). Read: `prompt.txt`, the four answer blocks of `submission.md`, the 23 shipped
files, Gates A to E, and my pass 1 report (`determinism_check_report.md`, left in place beside this one).

What moved in the pack since pass 1 (byte compare against the copy I judged): `promo_calendar_2026.csv` (campaign
names only; the 78 day and market pairs are the same) and `search_pipeline.yaml` (`schedule:
monthly_per_feature_group` and `run_days: 14` under the feature ablation, `run_days: 42` under the component
holdout). The other 21 files are byte-identical. **No graded figure moved**: every figure of the table below
recomputes to the pass 1 value.

Not done, by my definition: `golden/`, `golden.zip`, `DESIGN_NOTE.md`, `generator/` and `metadata.json` were not
opened. The answer to R1's check at source (what the world puts on heavy lag days) is taken from the launch
message; I did not verify it, I verified that the shipped files refuse the figure. Step 9's count of 157 sets is
not verified (about sixty single and paired alternatives run here).

## Verdict

**DETERMINISTIC**, with SOLUTION_WRONG in the narrow sense only: five sentences of the closing paragraphs do not
rebuild from the rule they state (N1 to N5). No committed figure, band or call is affected by any of them.

The list (stock, promise, price, trend on; history, seller, match off) is forced. Every sound alternative keeps
it, and every rival that changes it is refused by a figure from the shipped files, now stated in the blocks.

## Disposition

**FIX_NOW**, answer-block wording only (fix location: **solution**). Nothing solvers see changes and no graded
figure moves, so no further re-judge is owed. One judgment is left with the author (R2): the quarter's own tests
still leave four stated ranges and are refused on precision, not on a failed check.

## F1 to F6 and R1

| Item | Status | Evidence on this cut |
|---|---|---|
| F1 regression sentence | **closed** | status shares, day-clustered: 0.159, -0.054, 0.136, 0.013, 0.195, 0.162, 0.024; s.e. 0.003 to 0.091; promise, history, seller 1.1, 1.5, 1.6 s.e. from the line. All identical |
| F2 which tests | **closed by the second option** (residual R2) | every figure of the paragraph reproduces: 0.061 and 0.063, 0.181 and 0.176, 0.72 and 0.74, 0.438 and 0.427; Q 7.91 and 6.13 on 8 df; s.e. 0.087 against 0.039 and 0.092 against 0.039; 0.0614 plus or minus 0.0075 (1.52 s.e. over the line), all nine 6.71; 0.0599 and 0.0549 |
| F3 hurried netting | **closed** | step 2 vector 2.62, 0.57, 0.56, 1.32, 0.42, 0.93, 1.12 and products 0.267, 0.032, 0.080, 0.021, 0.039, 0.217, 0.009; seller 1.89 and 0.443; April 0.260, 0.800 (0.7995), 0.286, 0.280; trend 0.036. All identical |
| F4 stock rule | **closed** | with gaps that end before 112.5 minutes dropped: 4.027 per cent, 0.1023 points |
| F5 latest test alone | **closed** | trend 0.547 points a session (s.e. 0.149), cost 0.047 plus or minus 0.013, off the list on one test of nine |
| F6 seller persistence | **closed** | over the quarter's runs: 34.4 after a failed run, 20.1 after a scored one |
| R1 trend in the daily record | **closed** | see below |

## R1: the regression's trend figure is refused by figures from the shipped files

The regression on the replayed shares reproduces: stock 0.101, promise -0.079, price 0.142, history 0.033, trend
0.194, seller 0.139, match 0.023, 0.55 together; trend at 2.26 points a session at the default. It is stable to
form (one effect per campaign name: trend 0.193; clustered by market and device cell: same points).

What refuses it:

- **The randomised tests measure the thing itself.** `feature_store.yaml` serves the group default on expiry and
  on a missing value alike, and `search_pipeline.yaml` gives trend one reader (rank). Trend's nine tests put that
  default at 0.84 points a session (precision-weighted 0.857, s.e. 0.039). At 2.26 points the tests would report
  1.06 points on average and 0.81 in the third quarter; they report 0.40 and 0.27.
- **The arms.** Held arm 1.94 (s.e. 0.76) and control arm 2.04 (s.e. 0.81) points per unit of trend's default
  share, against 0.44 expected on the held users' cached pages: reproduced (see N1 for the effects). The sharper
  form of the same check, which the blocks do not print: control less held, regressed on that share, has slope
  -0.12 (s.e. 0.31); the route predicts -0.34 and a 2.26-point effect through the ranking model predicts -0.91.
  The loss on those days falls on both arms alike.
- **Charter 3.3** prices the group "in normal service to every service that reads it".
- The regression places neither promise (1.2 s.e.), history (0.6) nor seller (1.1) against the line on the
  replayed shares, so it cannot draw the list.

With the source answer in the launch message (a co-occurring seasonal loss, nothing charged to trend's default
beyond the ranking model), the golden's trend figure and totals stand. Optional: print the paired slope; the held
arm alone sits 1.97 s.e. over its 0.44 and only 1.0 s.e. from what a 2.26-point effect would leave it (1.18).

## R2 (author's judgment, not a required fix): the quarter's own tests

The blocks now say plainly that the quarter's three tests leave four stated ranges (trend 0.0614 against a floor
of 0.066, price 0.1806 against a top of 0.175, component 1 at 0.716 against 0.80, component 4 at 0.438 against
0.419) and refuse them as the estimate. The list holds (trend 0.0614, and 0.0549 at its lowest sound
combination). The refusal reproduces, but it is a precision argument: the subset fails no check.

- For it: Q 7.91 (trend) and 6.13 (price) on 8 df; a drift across the nine tests is not there (slope z -1.52 for
  trend, +1.21 for price, opposite signs); stock, with no cache term, shows a half-year contrast of the same size
  (z -1.82); the release log files "No feature change" on every monthly retrain.
- Against it: first half against the quarter is z 1.78 for trend (0.891 against 0.718) and -1.61 for price.
- A figure the blocks could add: the April slice sides with all nine. The quarter's tests call April at 0.438,
  1.7 standard errors from the mart's 0.411 (s.e. 0.016); all nine call 0.405, 0.4 from it.

If the reviewer treats "the quarter's own tests" as a licensed inclusion rule, a solver using them is marked wrong
on four figures. Widening closes that with no cost to the rejected routes (trend floor 0.055, price top 0.181,
component 1 floor 0.71, component 4 top 0.44; the hurried 0.036 to 0.039, 0.42 and 0.26 to 0.29 stay outside).
Either choice is deterministic on the call.

## Evidence: figures recomputed by the blocks' own method

| Figure | Blocks | Recomputed | Status |
|---|---|---|---|
| Step 1 counts and conversions | as stated | source files byte-identical to pass 1, where all reproduced | reproduced |
| Status unhealthy share, Q3 (per cent) | 10.20, 5.58, 14.17, 1.61, 9.33, 23.43, 0.80 | identical | reproduced |
| Served a default over normal (per cent) | 4.03, 5.58, 10.59, 1.61, 8.58, 1.39, 0.80 | 4.027, 5.575, 10.594, 1.614, 8.577, 1.393, 0.797 | reproduced |
| Seller: runs failed, served, normal | 23.39, 2.60, 1.21 | 23.39, 2.60, 1.21 | reproduced |
| Full effect, points a session | 2.54, 0.57, 1.11, 1.32, 0.84, 1.77, 2.31 | 2.542, 0.573, 1.113, 1.319, 0.843, 1.768, 2.311 | reproduced |
| Component loss, costs | 1.13, 1.02, 0.93; 0.035, 0.049, 0.008 | 1.130, 1.018, 0.925; 0.0347, 0.0490, 0.0076 | reproduced |
| Seven costs | 0.102, 0.067, 0.167, 0.029, 0.072, 0.025, 0.019 | 0.1023, 0.0667, 0.1671, 0.0288, 0.0723, 0.0246, 0.0186 | reproduced |
| All groups; listed | 0.48; 0.41 | 0.4805; 0.4084 | reproduced |
| Months | 0.49, 0.63, 0.32 | 0.4901, 0.6259, 0.3230 | reproduced |
| CC1, CC2, CC3, CC4 | 0.84, 1.39, 0.035, 0.405 | 0.843, 1.393, 0.0347, 0.4052 | reproduced, in band |
| April mart; ratio | 0.411 (0.016); 1.47 | 0.4115 (0.0157); 1.468 | reproduced |
| Margin: promise | 0.017; 0.0137 over step 9's conventions | 0.0167; 0.0137 (not netted, badge on failed renders over an earlier rate) | reproduced |
| Further readings | trend 0.83; stock 0.1048, match 0.0212; nearest 0.0166 | 0.830; 0.1048, 0.0212; 0.0166 | reproduced under one reading (N2) |
| Seller in full; independent | 2.60 and 0.046; 0.16 and 0.0029 | 2.598 and 0.0459; 0.164 and 0.0029 | reproduced |
| Second-quarter reading | 0.096, 0.062, 0.153, 0.025, 0.064, 0.025, 0.014 | 0.0963, 0.0622, 0.1534, 0.0250, 0.0642, 0.0244, 0.0137 | seller 0.024 (N3) |
| Tests pooled by market and device, precision | 0.267, 0.032, 0.079, 0.021, 0.039, 0.217, 0.009 | 0.266, 0.032, 0.078, 0.021, 0.039, 0.218, 0.009 | within 0.001, same list |
| Shards once times latest test | 0.162, 0.029, 0.046, 0.021, 0.018, 0.147, 0.008 | 0.165, 0.029, 0.045, 0.021, 0.017, 0.146, 0.011 | not rebuilt (N4), same list |
| Held share of the arms' sessions | 50.01 | 50.014 | reproduced |

## Fork list (each run on this cut)

Bands: stock 0.081 to 0.124, promise 0.062 to 0.069, price 0.152 to 0.175, history 0.027 to 0.030, trend 0.066
to 0.081, seller 0.023 to 0.027, match 0.017 to 0.022.

| # | Choice | Alternative | Result | Ruling |
|---|---|---|---|---|
| 1 | Effect pooling | over devices; market and device; precision weights three ways; mean of tests' ratios; origin share over each test | trend 0.0712 to 0.0760, price 0.163 to 0.169 | closed |
| 2 | Netting | not netted | trend 0.0703, price 0.1614, total 0.470 | closed |
| 3 | Which tests | first half; from April | trend 0.0762, 0.0713; price 0.1625, 0.1705 | closed |
| 4 | Which tests | the quarter's three; the four from June | 0.0614 and 0.0634; price 0.1806 and 0.1759; same list | refused in the blocks by Q and the standard errors (R2) |
| 5 | Which tests | the latest alone | trend 0.047, off the list | refused: plus or minus 0.013, one test of nine |
| 6 | Stock snapshot | fresh; a whole interval old; short gaps kept | 0.090; 0.117; 0.1026 | closed |
| 7 | Trend clock | back at once, two hours; from 5 or 7 hours; while the lag itself exceeds 6 hours | 0.0707 to 0.0740; 0.0674 | closed |
| 8 | Seller weights | quarter traffic; equal | 0.0249; 0.21 and listed | equal refused: the traffic file, charter 3.3 |
| 9 | Seller validity | four or six nights | 0.030, 0.021 | refused: `feature_store.yaml`, 120 hours from 00:00 |
| 10 | Seller normal service | in full; second quarter, June, first half level | 0.046; component 2 at 1.40 to 1.44; first half 1.385 | closed; first half needs N5 |
| 11 | Seller exposure | status share | 0.443, listed | refused: validity; persistence 34.4 against 20.1 |
| 12 | Price exposure | failed hours | 0.227; April 0.800 against 0.411 | refused by the April slice |
| 13 | Component loss | pooled; per session of its test; market by market; per rendered eligible session | promise 0.0667 to 0.0675 | closed |
| 14 | Component exposure | failed renders over the rate with the value present, or the second quarter's, June's, the first half's; in full | badge 0.0324 to 0.0342; in full promise 0.079 | closed; in full refused by the 2.1 per cent base rate |
| 15 | Grain | quarter-level product; day by day | within 0.0003; stock 0.1048, match 0.0212 | closed under the day's counts (N2) |
| 16 | Window; dedupe; aborted test | local days; first load; aborted test read | within 0.0003; no change; trend 0.0721 | closed |
| 17 | Baseline | second-quarter level | trend 0.064, match 0.014, same list | refused by charter 3.2 |
| 18 | Seller failures independent | five failed nights at the nightly rates | 0.164 per cent, 0.0029 | refused by persistence |
| 19 | Lowest sound trend | quarter's tests, counters back at once, not netted | 0.0599; 0.0549 | on the list |
| 20 | Strongest rival | daily regression, status and replayed shares, three forms | trend 0.193 to 0.196, total 0.55 to 0.64 | refused by figures (R1) |
| 21 | One calibration ratio from April | 1.47 on the hurried call | promise 0.047, seller 0.319 | refused as the blocks say |
| 22 | Widest sound totals | stock fresh, not netted, counters at once; stock a whole interval, two hours, from April | total 0.457 and 0.499; July 0.464 and 0.512; August 0.596 and 0.649; September 0.307 and 0.335 | all inside |
| 23 | The pack edits | campaign names; schedule and run lengths | regression with one effect per campaign: seller 0.171, history 0.012, same conclusions; run lengths equal the export's (14 and 42 days) | opens no fork |

Gates B, D and E as in pass 1: every constant is filed (0.05 in charter 4.1; 2, 36, 6 and 120 hours, 15 minutes,
04:00 and the hourly window in `feature_store.yaml` and `feature_registry.csv`; the cache key, lifetime and write
rule, the readers and the components in `search_pipeline.yaml`; the region split in `serving_regions.csv`); every
term of the recommendation is in an input; each ask pins one answer with its unit through charter 3.1 to 3.4.

## Fixes (all in `submission.md`, none touches a graded figure)

- **N1, the regression paragraph, the arms.** "The same effects" reads as market and device, weekday, month and
  promotion. The stated 1.94 (s.e. 0.76) and 2.04 come out with the promotion effect left out; with it the held
  arm is 1.84 (s.e. 0.72) and the control arm 1.95. Write "market and device, weekday and month effects", or
  print 1.84, 0.72 and 1.95. The point stands either way.
- **N2, the further readings, "every default share taken day by day".** Stock 0.1048 and match 0.0212 come out
  when a day's share is taken from the day's own counts (the status record's `unhealthy` over `observed` summed
  over the day for the request-time groups, the day's hours at the default for the stores) and the tests are
  netted for that share. The unweighted mean of the day's hourly shares gives promise **0.0539** (outside 0.062
  to 0.069, 0.0039 over the line, list kept) and history 0.0269, which contradicts "inside every stated range"
  and "nearest 0.0166". Add the rule to the clause; the mean of hourly shares is refused by the record's own
  counts and by charter 3.3 (over sessions).
- **N3, the second-quarter reading.** Seller is 0.0244 by the stated rule (1.393 less 0.011 per cent, times
  1.768): print 0.024, not 0.025.
- **N4, "each job's unhealthy share with every shard counted once, times its latest test".** Not rebuilt from the
  sentence: shares by the shards' counts (6.54, 5.58, 10.62, 1.61, 8.08, 23.39, 1.13 per cent) times the
  September test as reported at the quarter's device mix (2.53, 0.53, 0.43, 1.29, 0.21, 0.62, 0.98) give 0.165,
  0.029, 0.045, 0.021, 0.017, 0.146, 0.011 against the stated 0.162, 0.029, 0.046, 0.021, 0.018, 0.147, 0.008
  (match differs most). Same list (stock and seller). State how the share and the effect are taken, or restate.
  I did not raise this in pass 1.
- **N5, step 9, "the first half" as seller's normal level.** The run record starts on 1 January, so the first
  four nights have no five nights behind them (replayed default share 7.2, 4.0, 2.6, 1.7 per cent against 1.2
  after). With them the first-half level is 1.271 and component 2 is **1.33**, under its floor of 1.37; from 6
  January it is 1.385. Add "from the sixth night of the record".

Optional, no defect: the paired slope in R1; the April figure in R2; "trend's default share is the same in every
market and on both devices" holds to 0.005 of share once weighted by each cell's hours.

## For the CSV comparison (recomputed, points; stock by the rule as now written)

| Month | stock | promise | price | history | trend | seller | match | all |
|---|---|---|---|---|---|---|---|---|
| July | 0.1065 | 0.0292 | 0.2786 | 0.0038 | 0.0356 | 0.0167 | 0.0197 | 0.4901 |
| August | 0.1213 | 0.0790 | 0.1850 | 0.0675 | 0.1219 | 0.0310 | 0.0202 | 0.6259 |
| September | 0.0787 | 0.0922 | 0.0358 | 0.0150 | 0.0592 | 0.0262 | 0.0160 | 0.3230 |
