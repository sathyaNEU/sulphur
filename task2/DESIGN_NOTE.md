# task2 architecture 4: Mount Carrow Stage 5, the Yarrabin delivery tier

General Statistics & Data Science, exploratory data analysis and distribution assessment, Descriptive & Distribution
Analysis. Re-root of the slot after the platform landed architecture 3 (both runs on the golden at every ask,
`runs/triage.md`): one architecture per world, so a new world, dataset and shell.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task2.json` v4, registered 2026-11-08 at WARN (answered on the card:
  grain_or_unit here never decides on a field or a filed rule; method_or_model_selection repeats task3 v3, whose step
  shares nothing with this one); differentiated against mark257 and mark269; lineage carries v1 to v3.
- **Pairing:** a gold miner commits a contained-gold tier in an ore purchase agreement; ore is a 5 m by 5 m by 2.5 m
  mining block grading 2.5 g/t or more; Ironbark commits the largest tier Stage 5's ore covers.
- **Shape:** a which-tier with the grade-tonnage curve at block support, a workbook and a board deck with the chart.
- **Strategy:** own (UNTESTED in `sulfur-strategies.md`): the distribution of block averages read from point samples
  (the support effect), with declustering at rung 1 and the kriged block model as the field's estimator beside it.
- **Data-native sentence:** a gold deposit whose grades carry a large nugget and a short structure, drilled on a 25 m
  grid with 12.5 m infill where the first holes ran high, and sold by 5 m by 5 m by 2.5 m blocks at a cut-off above
  the mean: a 2.5 m composite varies about twice as much as a block, and an interpolated block estimate about a
  third less.
- **Abstraction sentence (written, then tested):** "the share of a population above a line is read at the size of
  the unit selected, not at the size measured, and not from smoothed estimates." Against every approved and
  delivered build in `guard.py mechanisms --objective descriptive-distribution`: mark253 (a count of latent levels
  under a line seen through averages) is the nearest; its averages are a unit's own noisy observations shrunk to a
  level, where here the average is spatial, over a block the samples never measured, read from the covariance with
  distance; mark274 (an instrument's bias against a reference) and mark182 (length-biased snapshots) spend other
  insights.
- **Sources** (synthetic, authored for this task, CC0; `metadata.json`): the drillhole database's collars, 1 m assays
  from two laboratories, QAQC results, bulk densities and weathering logs; the Stage 5 design by flitch; Tallowood's
  term sheet; the 2027 mine plan summary; the geology office's drilling plan (PNG); the toll mill's bottle-roll
  testwork and the Stage 4 survey pickup (distractors).
- **People:** drawn with `guard.py names --geo AU --seed 2`: Mary Fitzgerald, Elizabeth Parker, Catherine Lawson,
  Stacy Stephens.

## Default path

1. Put the collars on the mine grid, composite the 1 m assays to the 2.5 m flitches, keep the composites inside the
   Stage 5 outlines (10,837 composites from 444 holes).
2. Decluster on the 25 m grid's cells by flitch (the infill and the grade-control trial cluster where grades ran
   high): mean 1.38 g/t as drilled, 1.18 g/t declustered (the field's exploratory step).
3. Read the declustered composites' grade-tonnage curve against Stage 5's tonnes (20.6 Mt from the flitch outlines
   and the weathering zones' densities): 231 koz above 2.5 g/t.
4. Commit the largest tier the gold covers.

Ends on: Tier C
Golden: Tier B

## Stump sentence

A strong analyst who declusters the composites and reads their grade-tonnage curve puts 231 koz above 2.5 g/t and
commits Tier C, and one who kriges the blocks instead (the kriging cross-validates without bias) puts about 100 koz
there and commits Tier A; a 2.5 m composite varies about twice as much as a 5 m by 5 m by 2.5 m block and the kriged
estimates vary less than the blocks, so only the declustered distribution carried to the block variance the
variogram gives (0.54 of the composites') puts about 150,000 oz above the cut-off and commits Tier B.

## Deep reasoning

- **Task type:** exploratory data analysis distribution assessment (the distribution of block grades above a
  cut-off), serving descriptive-distribution.
- **Domain test:** the deciding quantity is the gold in the upper tail of the distribution of 5 m by 5 m by 2.5 m
  block grades; the field's estimators are the declustered sample histogram and the kriged block model.
- **Swap:** "the gold in blocks above 2.5 g/t" becomes "the revenue in stores above a sales line": there is no
  support, no nugget and no block average whose variance a covariance with distance fixes, so the correction loses
  its object.
- **Layer 1:** values under detection written "<0.01" and two laboratories' unit spellings (the laboratories'
  reports), screen fire re-assays as second rows (the high-grade protocol), core loss intervals not sampled, collars
  on the mine grid before 2022 and MGA after (the database migration), CRMs, blanks and field duplicates with one
  standard's batch out of tolerance (the QAQC programme); nothing is placed to be caught.
- **Layer 2:** estimation fit: the variance of a block average read from the composites' spatial covariance, and the
  declustered distribution carried to that variance.
- **Decisive step:** correcting the distribution to block support: the block variance from the variogram model's
  average within a 5 m by 5 m by 2.5 m block (nugget 34 per cent of the sill, structures of 12 m and 50 m), and the
  declustered composites carried to it by a lognormal-shaped correction.
- **Not semantics:** every field, unit, grid and code read correctly (the term sheet's block, the cut-off, the
  laboratories, the collar grids) still leaves the support to be corrected; a run that reads every clause takes the
  composites' or the kriged model's distribution for the blocks'.
- **Not rule application:** the term sheet defines ore by the block and its grade; nothing filed says how a block's
  grade distribution is estimated. Enumerated family (composites as drilled, declustered composites, kriged blocks in
  three neighbourhoods, support-corrected composites under two shapes, three declustering cells, three
  discretisations, two lag classes, a fitted or duplicate-fixed nugget) spreads the 2.5 g/t gold from about 100 to
  350 koz; the standing family (the support-corrected composites, every shape, cell of 25 or 30 m, discretisation,
  nugget choice) spreads it 136 to 177 koz, all Tier B; the ruling-out is loud in the data (the kriged estimates'
  spread is under the block variance the variogram gives; the composites' over it).
- **Analyst test:** a strong analyst declusters and reads the composites (231 koz, Tier C) or kriges the blocks and
  reads the kriged model (about 100 koz, Tier A), validating the kriging by cross-validation.
- **Estimand:** the term sheet 1.2 and 2.1 (ore is a 5 m by 5 m by 2.5 m block of Stage 5 at 2.5 g/t or more; the
  tier is the contained gold of the ore delivered over 2027 and 2028); the mine plan summary (Stage 5 is the design's
  flitches, all dug in 2027 and 2028).
- **No decoy:** no resource statement, block model, memo or consultant figure ships; nothing states a tonnage,
  grade or ounces for Stage 5.
- **No certified replay:** no published resource exists for the method to reproduce.
- **Chain:** (1) composite and decluster the assays (the infill and the grade-control trial sit where earlier holes
  ran high); (2) fit the variogram to the composites downhole and across holes, the trial's 5 m pattern pinning the
  short range; (3) the block variance from the model's average within a block and the declustered distribution
  carried to it; (4) the gold above 2.5 g/t against Stage 5's tonnes by weathering zone, and the tier.
- **Judgment:** the support the distribution is assessed at: the composites overstate and the kriged estimates
  understate the blocks' spread, and the block variance is read from the data's own covariance (a 34 per cent nugget
  and a 12 m structure the trial pattern shows), not assumed.
- **One-fact test:** the likeliest hint, "kriged models are smoothed", sends a run to the composites (Tier C) or to a
  support correction it still has to build (declustering, a variogram fitted to a noisy horizontal curve, the block
  average); "decluster the infill" alone lands Tier C.
- **No replay:** the call is a forward commitment for 2027 and 2028; no shipped figure is re-derived or wrong.
- **Pinned:** rivals run on the cut pack (`generator/checks.py` R6): affine against lognormal correction, 25 or 30 m
  cells, discretisation 3x3x2 to 10x10x4, lags of 10 or 12.5 m, the nugget fitted or fixed from the field duplicates,
  the re-assays as original, mean or re-assay; every one files Tier B and rounds to 150,000 oz. 20 m cells (Tier B,
  177 koz) are ruled out for the gold figure by cells smaller than the 25 m grid splitting its holes (the declustered
  mean jumps 0.05 g/t from 25 to 20 m and moves under 0.03 from 25 to 30 m). The independent verifier's own
  variogram fit (coordinate search, Monte Carlo block average) lands 148 koz.
- **Run forecast:** a run first goes wrong by a method shortcut (the declustered composites' histogram read as the
  blocks', Tier C) or a self-confirming check (the kriged block model, unbiased in cross-validation, read as the
  blocks' distribution, Tier A).
- **Strategy label:** UNTESTED (fresh ground: the support effect in a distribution assessment), screens run harder:
  declustering sits at rung 1 (the client's preferential-sampling form is the rung here, never the step).
- **Lesson:** a distribution must be assessed at the support of the unit the decision selects; a validated
  estimator can still have the wrong spread; no build on file teaches the support effect.

## Survivor anatomy

- **Actor:** the composites have rows; the property that decides (a block's grade variance) has no column and no
  row: it is a relation between composites at different distances.
- **Link:** the block variance is read through the variogram, a comparison of every pair of composites by distance
  that no key offers and no sentence invites.
- **Reflex:** the declustered histogram (rung 1) and the kriged block model (the field's estimator) each file a
  wrong tier (C and A).
- **Back-test:** the kriging validates: leave-one-hole-out cross-validation is unbiased (slope near one), and the
  kriged mean equals the declustered mean.
- **Second use:** every file the decisive step reads has its own use: the assays and collars are the resource's
  only data; the grade-control trial is the new fleet's ground test; the field duplicates are the QAQC programme's.
- **Shock:** nothing moves: the nugget and the short range are ordinary features of a gold deposit's variogram,
  never an anomaly.
- **Pins:** the WHAT is in the term sheet (the block, the cut-off, the tiers, the term) and the plan summary (Stage
  5's flitches); no sentence names a support, a variance, a correction or a model.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | 7 Dedicated organ | Verdict |
|---|---|---|---|---|---|---|---|---|
| 0 Composites as drilled | no | no | yes | no | no | no | no | readable |
| 1 Declustered composites | no | no | yes | no | yes | no | no | readable |
| 1 Kriged block model | no | no | yes | no | no | no | no | readable |
| 2 The block variance and the support correction (decisive) | no | no | no | no | no | no | no | silent |

## Semantic fork table

| Id | Term or convention | Reading A (golden) | Reading B | Golden under A | Under B | Ruled out by |
|---|---|---|---|---|---|---|
| SF1 | ore | a 5 m by 5 m by 2.5 m block at 2.5 g/t or more | a composite or sample at 2.5 g/t | Tier B | Tier C | term sheet 1.2 |
| SF2 | values under detection | half the limit | zero | Tier B | Tier B | same call |
| SF3 | screen fire re-assays | the original | the mean, or the re-assay | Tier B | Tier B | same call (asserted) |
| SF4 | declustering cell | 25 m | 30 m (20 m) | Tier B | Tier B | same call (asserted); 20 m splits the grid's holes |
| SF5 | correction shape | lognormal | affine | Tier B | Tier B | same call (asserted) |
| SF6 | block discretisation | 5x5x3 | 3x3x2, 10x10x4 | Tier B | Tier B | same call (asserted) |
| SF7 | the nugget | fitted | fixed from the field duplicates | Tier B | Tier B | same call (asserted) |

## Ladder

- **Rungs and winners:** rung 0 composites as drilled: 350 koz, Tier C; rung 1 declustered composites: 231 koz, Tier
  C; the field's estimator (ordinary kriging of the blocks, 12 to 32 composites): about 100 to 112 koz, Tier A; the
  support correction without declustering: 256 koz, Tier C; the decisive rung (declustered and corrected to block
  support): 147 koz, Tier B (truth 151 koz).
- **Margins:** the golden sits 22 koz over Tier B's 125,000 and 53 koz under Tier C's 200,000; rung 1 31 koz over
  Tier C; every kriged neighbourhood under Tier B.
- **Pricing:** (1) the residue the WHAT leaves is the block distribution, a method; (2) the move the call needs (231
  to under 200 koz) is a third of the high-grade gold, which the support effect at a 34 per cent nugget produces; (3)
  the one-group-by route (the declustered histogram) is rung 1; (4) the block variance's spread across the standing
  fits is about 4 per cent (0.53 to 0.56) against the factor of two it moves the variance; (5) the lever is a
  variance and the call a verdict on one quantity far from both edges; (8) every visible grouping (weathering zone,
  laboratory, programme) was swept and none carries the support.
- **Dominance:** each lower rung's single correction leaves it on a wrong tier (R3b and R4 in `checks.py`).

## Closure table

| Axis | Reading | Closure |
|---|---|---|
| 1 population | Stage 5's blocks | term sheet 1.1, design file |
| 2 outcome | contained gold of ore blocks | term sheet 1.2 |
| 3 window | 2027 and 2028, all of Stage 5 | term sheet 1.1, plan summary |
| 4 unit | ounces, nearest 50,000 | prompt |
| 5 comparison | the gold against each tier | term sheet 2.1 |
| 6 block | 5 m by 5 m by 2.5 m | term sheet 1.2 |
| 7 cut-off | 2.5 g/t | term sheet 1.2 |
| 8 grids | MGA less the filed shift | plan summary |
| 9 laboratories | ppm and g/t one unit | assay rows |
| 10 detection | half the limit | same call |
| 11 re-assays | the original | same call |
| 12 density | by weathering zone | density and weathering files |
| 13 tonnes | flitch outlines | design file |
| 14 compositing | to the flitch | the block's flitch |
| 15 declustering | 25 m cells by flitch | the regular grid |
| 16 variogram | fitted downhole and across holes | the data |
| 17 support | the block variance | the data (decisive) |
| 18 correction | lognormal-shaped | same call |
| 19 rounding | nearest 50,000 oz | prompt |
| 20 tie at a tier | none within 20 koz | asserted |
| 21 largest tier | the largest covered | the prompt's question, term sheet 2.2 |
| 22 as-of | 6 November 2026 | the plan summary and the election date |

## Literal reader

Executing the term sheet and the plan summary word for word gives the estimand (Stage 5's 5 m by 5 m by 2.5 m blocks
at 2.5 g/t or more, their contained gold over the term, the largest tier covered) and leaves the block distribution
to the data; every reading the data leave standing files Tier B.

## Oracles

none: no resource statement, reconciliation or block model ships; the QAQC file scores the laboratories, not the
estimate.

## Ask sheet

- **Asks:** (A1) the gold above the agreement's cut-off, nearest 50,000 oz (150,000); the workbook's grade-tonnage
  table from 1.0 to 3.0 g/t and the deck's chart against the tiers (instruction following).
- **Devices:** A1 rides the decisive step (declustered composites 250,000, kriged 100,000) and carries a second
  judgment of its own: the block ratio applies to the declustered variance; applied to the composites' variance as
  drilled (inflated by the clustered infill) the same correction keeps Tier B at 196 koz and rounds to 200,000.
- **Pair ceiling:** 28.5 (`generator/ceiling.py`: the cracker lands Tier B and misses A1, 45; the mirror on rung 1,
  12); the full includer with the mirror 56.
- **Shallow keep:** 0 per cent of ask weight kept by the default path.
- **Measured by:** generator/ceiling.py

| Ask | Golden | Default path (rung 1) | Cracker (block ratio on the as-drilled variance) | Verdict |
|---|---|---|---|---|
| A1 gold above 2.5 g/t | 150,000 | 250,000 | 200,000 | miss |

## Prompt contract

The author's rewrite keeps: the question (what contained-gold tier Ironbark can commit Stage 5 to for 2027 and
2028); `stage5_OPA_tier_board.pptx` with the chart of the gold in Stage 5's mining blocks against cut-off beside the
three tier thresholds; `stage5_high_grade_resource.xlsx` with the tonnes, grade and gold above each cut-off from 1.0
to 3.0 g/t in steps of 0.5 and the gold above the agreement's cut-off; that gold to the nearest 50,000 ounces. The
as-of is 6 November 2026.

## Pre-ship check

- The Sulfur standard re-read against the built pack: the call rests on the block support (the variogram's block
  variance and the correction), with declustering at rung 1 and the kriged model beside it (R3a, R3b, R4 asserted);
  the leak reader answered Q6 analytical; the one-fact hint lands Tier C (R5).
- Free gates on the final cut: checks 70 of 70, the verifier (its own variogram fit lands 148 koz, Tier B),
  byte-identical rebuild, precut 72 of 72, figures_check 62 of 62, leak.py REVIEW (no LEAK; the tiers filed as stated
  inputs), guard heart WARN (answered on the card) and surface exit 0.
- Stage 4: the leak reader found no step named and no ranking file; the term sheet's clause numbering and the
  metallurgical head grades fixed. The determinism judge's verdict is recorded in determinism_check_report.md.

## Tried and rejected


- The seed's own quantity (the Medicaid gap on the "would recommend" top-box rate across a state report's hospitals), every route screened at the draw: composition and patient mix settle the comparison population (WHAT screen); shrinkage of small cells repeats task253; design weighting repeats task264's lesson and task268 v2's reflex; nonresponse either fails determinacy or repeats the inverse-probability weighting of task264, task267 and task268; survey mode effects belong to Experiment & Causal Analysis; misclassification is the spent sensitivity-and-specificity family; nowcasting the late returns repeats task181; telescoping sits next to task453.
- A race-probability (BISG) regression for the equity gap (prototype `p1.py`): a strong ladder, but the same linear unmixing of a mixed population as task263, a clone of its driver.
- Traffic count factor groups for an annual average (prototype `t1.py`): count differences of one or two units at tiny margins, and the ground overlaps task474.
- The sequence effect at queues of 4 to 14 determinations with effects of 2 to 13 points (`s1.py`, `s2.py`): the two corrected estimators (the excess over reordering by counts, the held-day slope less its reordering expectation) disagreed on 1 to 3 hospitals a seed, with the closest margins 0.01 to 0.3 points; the queues were lengthened and the effect hospitals separated from the line.
- Effects of 12 to 17 points (`s4.py`, `s5.py`): the family agreed, but the day's rate without the pair as a control landed 10 or 11 of the 11 hospitals, its bias of 3 to 5 points smaller than the gap to the line; the effects were lowered to 9.5 to 12.5 with a wider day mix (`s6.py`), where it lands 9.
- Ask B as presumptive approvals with nightly re-runs replayed under fresh application numbers (D1): dropped at stage 2, because no asking sentence makes the count determinate without naming the device (a replay is a fresh application record, so "each application once" counts it, and any wording that excludes it narrates the re-run); replaced by the reason list renumbered on 1 July 2025 (D2).
- Queues of 6 to 28 a day with counsellors sitting on 55 percent of working days: the held-day route filed 28 of 31, an answer a reader distrusts on sight; queues of 8 to 32 on 48 percent of days put it at 23 with the family still closed (1.81 points).
- Effects of 9.5 to 12.5 points with the day's rate over the other determinations as a reflex: it landed the golden set (the others' count is the day's sufficient statistic), so it was moved into the family and the construction made every member agree, rather than the world bent to break it.
- Architecture 1 (each counsellor's sequence effect measured against the reordering of each working day's own determinations): spent at stage 4, both scored readers corrected the within-day contrast for the short-queue bias by permuting each day's determinations and landed the 11; a decisive step that is a named small-sample bias correction falls to a reader who knows the bias by name, however the ladder below it is tuned.
- The outcome "did not get free care in full" (a denial or any discount below 100 percent): noise in the year-round households' calendars inflated the shares at the 200 percent line, where the 2025 policy's full-care boundary sits on the eligibility line; the outcome moved to owing more than half of the balance (a denial or a 25 percent discount), whose policy boundary at 300 percent no year-round household's pay crosses.
- Households timing their applications to a low quarter (selection on the quarter): dropped in the prototype, no separation the seasons did not already give.
- Every hospital's designed share at 7.5 or 4.5 percent (the first build of this architecture): under the golden calendars 13 hospitals landed between 7.50 and 7.56 percent and 8 between 4.50 and 4.54, a cluster that confirms the golden route to a reader trying several calendars and reads as made in the chart; the designed shares were spread to irregular values, and the three set below what misassessment alone gives them (H04, H07 and H27, which then denied almost no one for documents) were raised to 4.29 to 4.68.
- Flat pay for year-round households and a fixed seasonal shape (the first builds of this architecture): a household's repeat applications carried the same three-month total to the cent, which reads as made; pay now rises unevenly from year to year and varies month to month, a household reapplies when its work takes its pay down (the season it knows) rather than on a month's luck, and the fixed-effects member falls back to a cell's month means where the cell does not identify its own calendar (the Olympic Peninsula's resort households: left unadjusted there, it had read H28 at 6.31; the reapplication change did not move that figure, the missing cell did).
- Also weighed at the re-root draw and dropped before any prototype, no reasons written down at the time: CGM, cash fills, TTR, a hungry-judges time-of-day effect, and heaping (already on file as spent in this lane).
- Architecture 2 (each household's twelve-month income rebuilt from the 2025 policy's quarter through its region's calendar for its kind of work): spent at stage 4, both scored readers read criteria 2.3's twelve months against the guide's three months times four, fitted a seasonal profile per hospital or region and kind of work and landed the 16; a decisive step that answers a gap the documents state outright falls to a reader who reads both documents, however finely the calendar has to be cut.
- Screens run at the architecture 3 draw on 2026-10-21, each set aside with its record. None cleared, so the number retires.
  - Demand censored at a stock or a capacity: task18, task108, task147, task168, task133, task141, task120 and task179 record it as spent.
  - Event times known only between periodic inspections, or at a single inspection: task476's leak starts, and the onsets set aside at task270's draw.
  - A share past a line taken from model predictions with their error added back, as in poverty mapping or an exposure model's Berkson error: task123 records it as task253's insight, task185 measured the exceedance route dead on the lever against the plug-in, and task143 records a strong analyst adding the stated validation error by reflex.
  - Realised variance against microstructure noise: task270 and task271.
  - A hot deck whose donor cells leave out the grouping variable, pulling each group's imputed earnings toward the other groups': dropping the allocated values is the filter route the partial-coverage screen kills, and reweighting the respondents within cells is task253 v1's nonresponse adjustment within classes.
  - Immortal time, and the period-analysis estimate of current survival: both are delayed entry into the risk set, task265's lesson.
  - A point-in-time count's elapsed durations turned into a year's flow: length bias, task264's size-biased sampling.
  - Recall decay across a survey's recall period: the latest month is a filter route and the decay form forks; telescoping sits next to task453.
  - Persistence beyond a panel's span by a mover-stayer chain: mover-stayer, latent Markov and second-order chains extrapolate apart.
  - Bunching below the free-care line: the counterfactual density's degree, window and bin width are open.
  - The own-children estimate of fertility, and extinct-generation old-age death rates: named methods, each with an open adjustment; the second was set aside at task271's re-root.
  - A closing auction's own impact net of the liquidity its imbalance drew: task197's design, abandoned there on the taxonomy; here, which offsetting orders were responsive is a judgment no record settles.
  - Roll-call ideal points: task269 and task270.
  - The tail of a sum of correlated parts by simulation: each unit's recorded totals are a filter route.
  - Minimum-night-flow leakage through the night-day factor: no utility task type serves Descriptive & Distribution Analysis.
  - Medication persistence, pharmacology's one Descriptive task type, set aside at task270 and task271: the reverse waiting time forks, and the new-user washout is a WHAT.
  - The Fair Assistance world itself: its quantities are filed rules once its two estimation hooks (a counsellor's sequence effect, a season inside a quarter) are spent. Its presumptive-screen incomes are the Berkson case above, and take-up through verified applicants is the transported error-rate family (task192, task267).
- Architecture 2 retired by this session's batch audit (2026-10-31), short of the survivor anatomy the approved builds share: its actor had a column (every application named the main earner's kind of work) and its link was stated outright (the criteria's twelve months against the guide's three months times four), so only the field's-method rung held; it is re-rooted, not repaired, so the portal sees one strong build.
- 2026-10-31, at the architecture 3 draw: a clinic medication refrigerator's product temperature rebuilt from the
  building system's air probe through each model's thermal response, calibrated on pilot units carrying a buffered
  probe (the card first drafted): the same insight as task482 v8 (a slow quantity carried through a lag measured on a
  short overlap), spent there at stage 4 because two records of one unit side by side are compared on reflex.
- 2026-10-31, at the architecture 3 draw: the drift-between-resets stump in a precision machining plant (inserts
  wearing between tool changes, hand checks at intervals, containment sorts): the guard banned the organisation
  family (manufacturer, task482 v16 in the last three builds) with the context artifact and the forcing event; the
  hospital pharmacy's compounding unit carries the same structure honestly.
- 2026-10-31, at the architecture 3 draw, set aside before any prototype: an assay's drift between calibrations read
  from quality control (task274's calibration-specific bias on an immunoassay sits too close); hypochlorite decaying
  between deliveries at small water works (operators' grab samples land in most low spells, so the sampled share
  files nearly the golden); a dental milling centre's burs (every crown is seated on its die before release, so the
  checks are not sparse); medication adherence, roll-call ideal points and small-area opinion (rules, spent, or an
  open model specification); low-depth genotype calls (a named reflex).
- 2026-11-01, at the build: weighing every fortieth dose: the long sets' tails were weighed and caught, so the
  weighed share and the sorts filed nearly the golden; the procedure weighs the first dose of each batch and then every
  hundredth syringe or twentieth bag, and the long sets' tails fall after the third batch's last weighed dose.
- 2026-11-01, at the build: the start fixed per set as the golden: one or two weighed doses per set make the start
  noisy and inflate the tails (piperacillin-tazobactam crossed 10 at 20.4 against a truth of zero); the golden takes
  the start as varying about its mean, and the bag sets start high so that no member of the family puts a bag near
  the line.
- 2026-11-01, at the build: a third ask, each product's mean delivered volume in each quarter: the gross and net
  weights are in the register's own headers and the specific gravity in the procedure, so a careful solver banks it;
  dropped, and Ask A moved to months, whose fill times carry no zone.
- 2026-11-01, at the build: bag sets ending lower (a start of 2.05 and a five per cent loss) to break the
  lowest-weighed-dose ordering: ampicillin crossed 10 under the golden and the family split; reverted, and the
  ordering is recorded as a WARN in the Readability screen.
- 2026-11-01, at the build: seeds where a pooled Johnson SB fit to the weighed doses files the four (27203, 27235,
  27251, 27259 of the ten screened): the seed was chosen where it does not (27267, cefazolin 2 g at 0.4); a bounded
  fit lands only when the long sets' third batches leave a visible shoulder in the weighed doses, so this is the rung
  to watch at stage 4.
- 2026-11-07, Domains Fit return (the prompt read as PH-QP-07's 10 per cent rule applied to rates, with counting asks): the prompt now asks for each product's estimated 2026 rate with its 90 per cent interval and where the limit sits against it, the chart drawing each interval; the interval's endpoints are left ungraded because they move with the method (the estimate itself ranges 131 to 205 for cefazolin 2 g across the family), only the side of the limit is graded, and it holds under every method tried (SF12). The call, the stump and every earlier figure stay as they were.
- 2026-11-08, architecture 3 (each product's out-of-tolerance rate rebuilt dose by dose on its tubing set): the
  platform's two runs both modelled the drift with the litres a set had pumped as their first move and landed the four
  products and every ask; a mechanism the weighed doses show is modelled on sight. The world is spent.
- 2026-11-08, draw stage: a lead service line inventory estimated from a random verification sample beside opt-in
  identifications: mark124 v5 spent the remainder accounting already.
- 2026-11-08, draw stage: a fraud or risk-targeting model's precision under label shift with verification-biased
  labels: mark267 spent the verification bias, and label shift alone is one insight.
- 2026-11-08, build stage: the 2.0 g/t cut-off left the kriged model 2 koz from Tier B's edge; 2.5 g/t, above the
  mean, separates the composites, the blocks and the kriged estimates into three tiers.
- 2026-11-08, build stage: without short horizontal lags the variogram's nugget was unidentified (an independent fit
  put the block variance at 0.41 and the gold in Tier A); the 2024 grade-control trial's 5 m pattern pins it. Placed
  first on a low-grade patch, its pairs understated the variance (the proportional effect) and swung the fit the
  other way; moved to a patch of typical grade.
- 2026-11-08, build stage: one graded figure that only the decisive step reaches left a landed run with every ask
  (pair 56); the cracker's second judgment is the variance the block ratio applies to (the declustered one, not the
  composites' as drilled), which moves the gold to 200,000 oz while the tier holds.
- 2026-11-08, architecture 4 on the platform: the one run filed Tier B by plain inverse-distance-squared blocks
  (159,610 oz) with no declustering, variogram or support correction, and the domain fit return read the prompt as
  summing tabulated blocks against stated tiers. Measured afterwards on the shipped pack: inverse distance files 92 to
  162 koz across powers 2 and 3, 3 to 16 composites, in three dimensions or within the flitch (nearest neighbour 217),
  and at 4 composites it reproduces the golden's tonnes, grade and gold at every cut-off, so no tier floor separates
  it. Seven re-tuned worlds (a larger short structure, flat supergene lenses 12 to 25 m across and 2 to 3 m thick on a
  1.25 m vertical grid, a smaller nugget) moved where it crosses but never removed the crossing: a smoother whose
  neighbourhood is a free knob sweeps through the true block variance, and the composite-support variogram read the
  thin lenses as nugget, biasing the golden low. The support stump is spent; the slot re-roots.

