# task9 determinism check (Gates A to E), final cut

Pack: `target.zip` md5 990022e599555db61c7c2c45d86d8b90, unzipped fresh and recomputed with my own code
(scripts under the session scratchpad, `scripts/`). Inputs read: `prompt.txt`, the four answer blocks of
`submission.md`, the 23 shipped files, Gates A to E.

Not done, by my definition: I did not open `golden/`, `golden.zip`, `DESIGN_NOTE.md`, `generator/` (including
`verify.py` and `figures.json`) or `metadata.json`. So the two checks the launch message asked for on the golden
side (figures agreeing between `submission.md`, the workbook and the CSV; the golden ZIP holding exactly what the
prompt asks for) are NOT covered here and stay with `figures_check.py` and the build's own gates. The month by
group values I recomputed are listed at the end so the CSV can be compared against them.

## Verdict

**DETERMINISTIC, with SOLUTION_WRONG.** The list (stock, promise, price, trend on; history, seller, match off)
is forced: every sound alternative I ran keeps it, and every rival that changes it is refused by a figure from
the shipped files. The blocks need repair in six places: two stated ranges and two critical-component bands are
left by a sound neighbour of the blocks' own method, the regression rival is dismissed by a sentence its own
figures contradict, and four figures cannot be rebuilt from the rule the Step-by-Step writes down.

## Disposition

**FIX_NOW** (answer-block edits only), with one item flagged for a check at source that I could not make
(R1 below): if that check fails, R1 becomes a pack change and a re-judge.

Fix location: **solution**.

## Evidence: figures recomputed by the blocks' own method

| Figure | Blocks | Recomputed | Status |
|---|---|---|---|
| Step 1 counts (339,465 / 5,040; 889,961 / 1,332 / 888,629 / 8,000; 67 = 63 + 1 + 3; 1,633 gaps; 105 episodes) | as stated | identical | reproduced |
| Conversion Q2, Q3; Q3 sessions | 12.29, 11.76, 123.0M | 12.286, 11.761, 123.02M | reproduced |
| Status unhealthy share, Q3 (per cent) | 10.20, 5.58, 14.17, 1.61, 9.33, 23.43, 0.80 | identical | reproduced |
| Share served a default over normal (per cent) | 4.03, 5.58, 10.59, 1.61, 8.58, 1.39, 0.80 | 4.04, 5.58, 10.59, 1.61, 8.58, 1.39, 0.80 | reproduced (stock, see F4) |
| Seller: runs failed, served default, normal service | 23.39, 2.60, 1.21 | 23.39, 2.60, 1.21 | reproduced |
| Full effect, points a session | 2.54, 0.57, 1.11, 1.32, 0.84, 1.77, 2.31 | 2.542, 0.573, 1.113, 1.319, 0.843, 1.768, 2.311 | reproduced |
| Origin share (app, web) before and after 9 June | 61, 46; 44, 32 | 60.7, 45.9; 44.3, 31.6 | reproduced |
| Trend and stock as reported, Jan to May and Jul to Sep | 0.50, 0.27; 2.51, 2.48 | 0.503, 0.268; 2.513, 2.484 | reproduced |
| Component loss an eligible session; eligible share | 1.13, 1.02, 0.93; 56, 45, 50 | 1.130, 1.018, 0.925; 55.5, 45.2, 50.4 | reproduced |
| Badge failed renders Q2, Q3 | 2.37, 7.58 | 2.37, 7.58 | reproduced |
| Component costs | 0.035, 0.049, 0.008 | 0.0347, 0.0490, 0.0076 | reproduced |
| Seven costs | 0.102, 0.067, 0.167, 0.029, 0.072, 0.025, 0.019 | 0.1026, 0.0667, 0.1671, 0.0288, 0.0723, 0.0246, 0.0186 | reproduced; stock 0.103 by the written rule (F4) |
| All groups; listed groups | 0.48; 0.41 | 0.4808; 0.4087 | reproduced |
| Months | 0.49, 0.63, 0.32 | 0.4905, 0.6264, 0.3231 | reproduced |
| CC1 trend full effect | 0.84 (0.80 to 0.91) | 0.843 | reproduced; band left by fork 3 |
| CC2 seller over normal | 1.39 (1.37 to 1.46) | 1.393 | reproduced |
| CC3 badge | 0.035 (0.031 to 0.036) | 0.0347 | reproduced |
| CC4 April call; mart | 0.405 (0.385 to 0.419); 0.411, s.e. 0.016 | 0.4052; 0.4115, 0.0157 | reproduced; band left by fork 3 |
| April rivals | 0.260, 0.800, 0.286, 0.280 | 0.260, 0.789, 0.286, 0.274 | two reproduce only under F3's netting |
| Hurried products (step 2, Final Recommendation) | 0.267, 0.032, 0.080, 0.021, 0.039, 0.217, 0.009 | 0.255, 0.031, 0.073, 0.021, 0.038, 0.196, 0.009 as reported | not reproduced as described (F3) |
| Status regression (closing paragraph) | 0.159, -0.054, 0.136, 0.013, 0.195, 0.162, 0.024; s.e. 0.002 to 0.046 | identical; those are conventional s.e. | reproduced; the conclusion drawn is wrong (F1) |
| Q2-level baseline reading | 0.096, 0.062, 0.153, 0.025, 0.064, 0.025, 0.014 | 0.097, 0.062, 0.153, 0.025, 0.064, 0.024, 0.014 | reproduced |
| Seller persistence | 34.4 after a failed run, 20.7 after a scored one | 34.4; 20.1 over Q3 runs, 20.7 only when the previous run is also in Q3 | rule guessed (F6) |

## Fork list (each alternative run on the shipped files)

Bands: stock 0.081 to 0.124, promise 0.062 to 0.069, price 0.152 to 0.175, history 0.027 to 0.030, trend 0.066
to 0.081, seller 0.023 to 0.027, match 0.017 to 0.022. "Same list" means stock, promise, price, trend.

| # | Choice | Alternative | Result | Ruling |
|---|---|---|---|---|
| 1 | Effect pooling | pooled over devices; by market and device; precision weights (three ways); mean of tests' own ratios; origin share over each test | trend 0.071 to 0.076, price 0.163 to 0.169; all in band, same list | closed |
| 2 | Netting for the default on test days | not netted | trend 0.070, price 0.161, total 0.47; in band, same list | closed |
| 3 | **Which tests** | the quarter's own three tests a group (July to September); or the four since the cache change | Jul to Sep: trend full effect **0.716**, trend **0.0614**, price **0.1806**, April call **0.438**. Jun to Sep: 0.739, 0.0634, 0.1759, 0.427. Same list | **band defect**: leaves SQ1 trend and price, CC1 and CC4. First half and from April stay in band (trend 0.076, 0.071) |
| 4 | Which tests | the latest test alone (September) | trend full effect 0.547, trend **0.047, off the list** | refused by figure: one test's s.e. on the full effect is 0.149 (cost 0.047 plus or minus 0.013, cannot place the line); the nine tests agree (Cochran Q 7.9 on 8 df; pooled 0.86 plus or minus 0.04). The blocks do not say so (F5) |
| 5 | Stock snapshot age | fresh, whole interval old | 0.090, 0.117; in band | closed (filed 15 minutes, convention banded) |
| 6 | Trend counters back | at once, two hours; default from 5 or 7 hours | 0.0707 to 0.0740; in band | closed |
| 7 | Trend default clock | default while the lag itself exceeds 6 hours (`peak_lag_minutes` shape, no extra window) | 0.0674; in band by 0.001, same list | closed, thin on the band floor |
| 8 | Seller weights | quarter traffic; equal weights | 0.0249 (CC2 1.41); equal weights 0.21 and lists seller | equal weights refused: `seller_search_traffic_monthly_2026.csv` is filed and charter 3.3 is over sessions |
| 9 | Seller validity boundary | four or six nights | 0.030, 0.021 | refused: `feature_store.yaml` 120 hours, effective 00:00 |
| 10 | Seller normal service | default in full | 0.046, off the list | blocks state it; charter 3.2 |
| 11 | Seller exposure | status share on the full effect | 0.41 to 0.44, lists seller | refused: `feature_store.yaml` validity; 3,255 of 8,000 sellers have a run on a night |
| 12 | Price exposure | failed hours for expired hours | price 0.227, April 0.79 against the mart's 0.411 | refused by the April slice |
| 13 | Component loss | pooled over devices; per session of its own test; per rendered eligible session (holdout's own failed renders netted) | promise 0.0667, 0.0667, 0.0675; badge 0.0347 to 0.0355 | closed; the last sits on CC3's band top |
| 14 | Component exposure | failed renders over the rate with the value present (2.1, 2.0, 2.2 per cent measured); over the Q2 rate; in full | promise 0.066, 0.064; in full 0.079, price 0.176, history 0.038 | first two in band; in full refused by the measured base rate |
| 15 | Request-time share weights | by requests instead of sessions | promise 5.575 both ways, history 1.613 against 1.614 | closed |
| 16 | Grain | quarter-level product of effect at mix and share; components likewise | within 0.0003 everywhere | closed |
| 17 | Window | local calendar days | within 0.0003 | closed |
| 18 | Baseline | Q2 level as normal service | trend 0.064, history 0.025, match 0.014, same list | refused by charter 3.2, as the blocks say |
| 19 | Dedupe | first load kept | Q3 untouched (reloads are 19 to 25 May, trend and match) | closed |
| 20 | Lowest sound combination for trend | fork 3 with counters back at once; and also not netted | 0.0599; 0.0549; same list | margin to the line 0.005 to 0.011, not the 0.0137 step 9 states |
| 21 | **Strongest rival: regression of the mart on the replayed shares** (market by device and day, weekday, month and promotion effects, day-clustered) | see R1 | stock 0.101, promise -0.078, price 0.142, history 0.033, **trend 0.194**, seller 0.139, match 0.023; total 0.55 | list by point estimate: stock, price, trend, seller. Refused for the list by figures (R1); **its trend figure is not refused by the blocks** |

Constants: 0.05 (charter 4.1), 2, 36, 6 and 120 hours, 15 minutes, 04:00, the hourly window (`feature_store.yaml`,
`feature_registry.csv`), the cache key, lifetime and write rule, the readers of each group and the render
components (`search_pipeline.yaml`), 10 per cent held (sqlite), the region split (`serving_regions.csv`). All
filed. The two unfiled conventions (half a sync interval; one window after catch-up) are banded and the bands hold
their alternatives (forks 5 and 6). Gate B: every term of the recommendation is in the charter, the registry or
the pipeline file. Gates D and E: each ask pins one answer with its unit through charter 3.1 to 3.4 and 4.1.

## R1. The strongest rival, and what the mart says about trend

The route's own predicted cost, tested against `mart_search_conversion_daily_2026.csv` over January to September:

- All groups together: coefficient 1.02 (s.e. 0.08, day-clustered). The route as a whole fits.
- By group: stock 0.99 (0.14), price 0.84 (0.12), match 1.22 (0.16), and **trend 2.60 (0.45)**; 2.31 (0.47) with
  week effects, 2.81 (0.47) on Q3 alone, 2.76 (0.40) with every other group fixed at the route. Wald test that all
  seven equal the route: p = 0.003.
- On the 23 Q3 days with trend's default share over 15 per cent, conversion plus the route's cost is 11.99; on the
  33 days under 3 per cent it is 12.34; the first half's level is 12.32.

So the pack's observational record puts trend near 0.19 points (0.18 to 0.20), not 0.072, and the total near 0.55.
Trend stays on the list, so the call does not move. The figures it would move are trend, both totals and August.

What refuses it, from the shipped files: the loss on those days does not pass through the ranker's reading of
trend. In trend's own tests the **held arm**, whose pages built at origin never had trend, loses 1.94 (s.e. 0.76)
points per unit of trend's default share that day, where the route expects 0.44; the control arms of the other
groups' tests lose 2.12 (0.50). And a ranker effect of 2.3 points a session would make the Q3 trend tests report
about 0.84 points where they report 0.27 (full effect 0.72, s.e. 0.09). Charter 3.3 prices the group "in normal
service to every service that reads it", and `search_pipeline.yaml` gives trend one reader. On that reading the
golden stands.

Two things remain:

1. The blocks dismiss the regression with "cannot tell a twentieth of a point from nothing" beside standard errors
   of 0.002 to 0.046. Those are conventional standard errors, and by them trend (0.195, s.e. 0.016), seller
   (0.162, s.e. 0.031) and stock, price and match are all told apart from nothing, and seller sits 3.6 standard
   errors over the line. The sentence contradicts its own figures. With day-clustered errors (0.003 to 0.091)
   promise (-0.054, s.e. 0.091) and seller (0.162, s.e. 0.070) cannot be placed against 0.05, which is the true
   reason the regression cannot draw the list; trend still can be told apart, and needs the held-arm figure.
2. **Check at source (I could not open the generator):** what the world puts on click-stream lag days beyond
   trend's effect through the ranker. It is about 1.5 points per session at trend's default, roughly 0.13 points
   over the quarter, larger than trend's whole stated cost. If it is a separate loss that co-occurs with lag, the
   block edit F1 closes it. If the world charges it to trend's default (so the tests under-report by construction),
   or if it is unintended, the golden's trend figure and totals are not what the pack's outcome record supports,
   charter 3.2 ("sources refresh on schedule") gives a reviewer a second reading, and the repair is in the pack.

## Fixes (all in `submission.md` unless R1's check fails)

- **F1, closing paragraph, the regression sentence.** Replace "with standard errors of 0.002 to 0.046, lists
  stock, price, trend and seller and cannot tell a twentieth of a point from nothing" with the day-clustered errors
  (0.003 to 0.091), the ruling that promise and seller cannot be placed against the line (1.1 and 1.6 standard
  errors from it), and the refusal of its trend figure: the held arm of trend's own tests loses 1.94 points per
  unit of trend's default share (s.e. 0.76) where the route expects 0.44, so the regression loads on trend a loss
  that does not pass through a reader of the group.
- **F2, Supplementary 1, Critical Components 1 and 4, step 9.** The quarter's own tests are a sound subset beside
  "the first half's or those from April" and leave four bands: trend 0.0614 (floor 0.066), price 0.1806 (top
  0.175), CC1 0.716 (floor 0.80), CC4 0.438 (top 0.419). Either widen them (trend floor to 0.055 to hold fork 20,
  price top to 0.181, CC1 floor to 0.71, CC4 top to 0.44; the hurried figures 0.036 to 0.039, 0.42 and 0.26 to 0.29
  stay outside) or name the subset in the closing paragraph and refuse it by the figure (Cochran Q 7.9 on 8 df,
  three tests give 0.72 plus or minus 0.09 against 0.86 plus or minus 0.04). Step 9's "the nearest any comes to
  the line is 0.0137 points (promise)" is then wrong: trend comes to 0.005 to 0.011. Total and listed total stay
  inside their ranges (0.485, 0.414).
- **F3, step 2, Final Recommendation, step 4, step 6.** The hurried figures read two ways. Step 2's effect vector
  (2.54, 0.57, 0.55, 1.32, 0.42, 0.85, 1.12) is netted for the replayed default; the tests as reported are 2.50,
  0.56, 0.52, 1.31, 0.40, 0.84, 1.12. Its product (0.267, 0.080, 0.217 for stock, price, seller) is neither vector
  times the stated shares (0.259, 0.078, 0.199 and 0.255, 0.073, 0.196): it uses effects netted for the status
  share (2.62, 0.56, 0.93). The same netting sits behind "seller at 0.443" in step 4 (the stated 1.77 times 23.43
  is 0.414) and behind 0.800 and 0.280 in step 6 (0.789 and 0.274 otherwise). Add one sentence that the hurried
  reading nets each test for the status record's share on its own days, and list that vector; or restate the
  products. The rejected list is the same either way.
- **F4, step 4, stock.** The written rule (default from 112.5 minutes after the stop until 7.5 after the resume)
  gives 4.04 per cent and 0.1026, which rounds to 0.103. The stated 4.03 and 0.102 come out only when a gap
  shorter than 112.5 minutes never reaches the default (4.027, 0.1023). Add that sentence. Inside the band either
  way.
- **F5, closing paragraph.** State the refusal of the latest test alone on the full route (trend 0.047, the one
  alternative that changes the list): one test's standard error on the full effect is 0.149 and the nine agree.
- **F6, closing paragraph, seller persistence.** "20.7 per cent after a scored run" holds only for runs whose
  previous run is also in the quarter; over the quarter's runs it is 20.1. Say which, or print 20.1.

## For the CSV comparison (recomputed, points; stock by the written rule)

| Month | stock | promise | price | history | trend | seller | match | all |
|---|---|---|---|---|---|---|---|---|
| July | 0.1069 | 0.0292 | 0.2786 | 0.0038 | 0.0356 | 0.0167 | 0.0197 | 0.4905 |
| August | 0.1217 | 0.0790 | 0.1850 | 0.0675 | 0.1219 | 0.0310 | 0.0202 | 0.6264 |
| September | 0.0788 | 0.0922 | 0.0358 | 0.0150 | 0.0592 | 0.0262 | 0.0160 | 0.3231 |

Not verified: step 9's count of 157 sets (I ran about forty single and paired alternatives).
