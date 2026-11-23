# task9: which sources of score movement Garrane Risk puts on a remediation plan or escalates for 2027

Architecture 6 of the cleared slot (Level-5 upgrade, 2026-11-23). Upgraded from architecture 5 after platform pair 3 (`runs/arch5_pair3_response_1.md`, `runs/arch5_pair3_response_2.md`, `runs/holistic_audit_v3_pair3_2026-11-23.md`) scored 0.60 / 0.60 (mean 0.60, failing the strict under-60 bar) with depth flag `concentrated` (30 of 40 lost points on warm-start noise decay alone, while uniform training-window overlap was solved by 4 of 4 responses across pairs 2 and 3 and pinned-view adoption lag was solved by both pair-3 responses). Keeps the proven Garrane Risk world, natural prompt voice, and proven warm-start decay stump (S1), replaces the solved uniform overlap with unfiled exponential recency weighting inverted from 16 seasonal 2026 bootstrap pairs per family (S2), and adds positive merchant-level cross-release covariance within feature groups measured from 2026 paired release-shadow vectors and carried to 2027 multi-phase roadmap sprints (S3). Also closes both residual Holistic Audit v3 determinism notes without leaking: Standard section 2.2 pins the 52 assessment-year Mondays (closing the ISO-vs-pair-year window fork), and strictly linear cold-start gap curves D_cold(h) across 29 to 55 cold weeks rule out mean-reverting merchant change directly from the data. Every figure in `## Stump core` is `generator/core.py`'s verbatim output on seed 9605 (`CORE PASS level 5`, zero waivers), and cut-pack figures are verified by `generator/results.py`, `checks.py`, and `verify.py`.

## Draw

Subdomain: General Statistics & Data Science (Machine Learning Research), Interpretability
Analysis type: Root-Cause Analysis
Answer shape: a bridge: the mean-square movement of a merchant's score between consecutive quarter-end snapshots attributed to five model-side sources, carried into 2027's four snapshot pairs and full assessment year, with each source placed in a filed governance band
Weight: modeling (three independent variance-component inversions on three distinct records: warm-start decay from anchored lag curves, recency decay from seasonal bootstrap variance swings, and within-group release covariance from merchant-level shadow vectors)
Data-native sentence: every production score carries all sources at once while each instrument reruns a single controlled step, so no file holds a source's movement at the thirteen-week decision gap, and the three records that identify the missing dynamics (warm-era and cold-era score lag curves anchored to replicate pairs, 16 seasonal 2026 weighted bootstrap pairs against weekly warehouse row waves, and merchant-level paired release-shadow score deltas against 2027's multi-phase feature sprints and rollout manifests) each require a dedicated statistical inversion.
People: Iona Cairns, Julie-Anne Inglis, Peadar Clarke, Richard McLeer, Marie O'Reilly, Shauneen Miley, Tamara O'Rooney, Kira O'Bryan, Dennis MacCurtin, Clare Graham, Malachy Renehan, Cillian Sealy, Cassie Gilbride, Ruth Tinney (`guard.py names --geo Ireland --seed 9505`)

Guard: `guard.py check task9` WARN only (0 BLOCK) on 2026-11-23 against the registered card; `skeleton.py check task9` WARN only (0 BLOCK), severity none against every card, the client's corpus and the slot's lineage (nearest driver similarity 0.03). three_rules.strategy_risk (grain_or_unit): answered under `Not semantics` below. template.chain_near (task25): answered under `## Template check`. skeleton.lesson_closed_near (inherited_noise_persistence): answered under `Closed strategies` below.

Forward call: the bands and combined model-side movements are set for the four quarter-end snapshot pairs closing in 2027 (22 March, 21 June, 20 September, 20 December 2027), none of which the record holds.

Deliverables: a workbook and a few slides; no written document.

## Stump screen

Screened on paper and in `generator/core.py` against all twenty tests (`references/stump-screen.md`). Eleven candidates screened, three genuinely independent stumps kept across three axes (what, when, unit).

| Candidate trap | The assumption a run waves through (precedent) | The second record that refutes it | Tests failed | Kept |
|---|---|---|---|---|
| A (S1): warm-started refits inherit prior randomness with decaying persistence phi_f in [0.65, 0.79], where replicate pairs measure one fresh draw and D_warm(h) bends sharply over h=1..8 while cold-era D_cold(h) is strictly linear | warm-started refit noise accumulates linearly across 13 refits because no decay rate is listed (L39, L65, N34; measured 4/4 in pairs 2 and 3) | settled warm-era gap curves D_warm(h) anchored to replicate pairs (positive gap-0 intercept 48+ pts^2; D_warm(1) check) plus strictly linear cold-era curves D_cold(h) over 29-55 cold weeks | none | kept (S1, axis what) |
| B (S2): 52/104-week training windows apply unfiled exponential recency weighting lambda_f in [0.905, 0.942] (filed as WHAT in Standard 1.6 and manifest options), identified by phase-lagged anti-phase swings across 16 seasonal 2026 bootstrap pairs per family against weekly labelled row counts | because no decay rate is listed in the registry or manifests, use equal-weight window turnover (entering+leaving)/(2N) (L28, L22, N21) | 16 dated 2026 weighted bootstrap pairs per family compared against warehouse_labelled_rows_weekly.csv (uniform log-RMSE 3.8x worse; high-vs-low trailing-volume bootstrap contrast 10.88 pts^2 vs ~0 under uniform) | none | kept (S2, axis when) |
| C (S3): sequential feature releases modifying the same feature group move the same merchants in the same direction (positive merchant-level correlation c_f in [0.72, 0.84]), invisible in scalar per-release MSE and 2026 weekly panel OLS (2026 releases spaced 27w apart per group), but decisive across 2027's multi-phase feature-group sprints alongside actual pinned-view adoption | after verifying flat scalar MSE across feature groups and R^2 > 0.97 on weekly panel OLS, sum unpinned releases as orthogonal independent shocks (N44, L58, L28; literally what pair-3 Response 1 and 2 did) | merchant-level signed score-delta vectors (score_b - score_a) across all 141 same-group pairs in mrm_instrument_pair_scores_2026.csv (141/141 strictly positive, mean 0.783, min 0.702 vs -0.001 across 2,580 cross-group pairs) | none | kept (S3, axis unit) |
| D: pinned feature views take-up lag vs calendar completion dates | scheduled changes take effect on planned dates (R73) | training scheduler manifests vs platform_change_calendar.xlsx | 2 (solved by both pair-3 responses once prompt said expected to actually run) | kept as supporting step feeding S3 and Ask 3 (not a stump) |
| E: uniform training-window overlap (in+out)/(2N) vs raw bootstrap | raw bootstrap spread equals quarterly turnover | warehouse rows + window lengths | 2 (solved by 4 of 4 live responses across pairs 2 and 3) | dropped as stump; superseded by S2 recency weighting |
| F: week-level macro shocks in training rows (row vs week bootstrap) | rows are independent | weekly residuals | 1 (too close to closed card #9 on clustered outcomes) | dropped |
| G: positive-event count K vs total rows N decoupling | exposure basis scales with rows | outcome counts | 1 (closed card #19 on outcome clock) | dropped |
| H: stationary HPO bounce on retunes or MA(q) correlated label revisions | independent weekly steps | gap curves | 10 (injects bend into D_warm and D_cold, coupling S1 to other sources) | dropped |
| I: serialized per-owner rollout queue congestion for pinned views | rollouts independent across families | owner column | 1 (closed card #41 on queue/capacity replay) | dropped |
| J: warm-started bootstrap contraction (1 - phi_f)^2 | bootstrap equals uncontracted variance | replicate pairs | 10 (couples S2 directly to S1 persistence phi_f) | dropped |
| K: replicate pairs run only on quiet weeks or simple families | replicate weeks stand for all weeks | replicate schedule | 4 and 14 (shallow hidden factor) | dropped |

## Deep reasoning

Task type: interpretability (feature attribution, probing, mechanistic analysis), serving Root-Cause Analysis in General Statistics & Data Science; the task attributes prediction churn in a deployed weekly retrained scoring system across its five model-side variance components.
Domain test: every graded result is a statistical variance-component quantity of model evaluation: the autocovariance of warm-started SGD/refit noise across successive training runs, the sample-weight-adjusted variance of two estimators fitted on overlapping exponentially weighted rolling windows, and the cross-event merchant-level score-change covariance across sequential feature-group updates. Swap the nouns for a warehouse or clinic and warm-started parameter persistence, weighted bootstrap variance inversion against weekly labelled row waves, and merchant-level release-shadow score-delta vectors lose all meaning.
Swap: replacing Garrane Merchant Score model families with stores, plants, or clinic wards destroys the task because warm-started SGD/GBDT refit persistence, exponentially recency-weighted training-window bootstraps, and paired release-shadow feature-group score vectors exist only in iteratively retrained machine learning scoring systems.
Where the weight sits: R2 (S1 optimisation noise), R3 (S2 recency-weighted training data), and R4 (S3 same-group feature-release covariance alongside pinned adoption). Each requires its own multi-step inversion across 14 model families on distinct primary records, with zero shared shortcut.
Layer 1: four re-sent weekly panel refreshes (later load_id supersedes), Tolka Pay merchant ID migration crosswalk (4,568 IDs), scheduler vs registry family code mapping, manifest rows / train_rows rename across the runtime rollout, nine retried duplicate manifest lines, ISO weeks alongside Monday dates, and panel attrition. Every single hygiene step is resolved by reflex and verified neutral (`checks.py` R2 asserts leaving any one undone keeps every graded figure inside its band).
Not one thing: dropping S1 alone puts optimisation noise in escalation (12.13 vs 6.86) and leaves training data and releases in remediation; dropping S2 alone puts training data on monitor (3.65 vs 6.83) and leaves noise and releases in remediation; dropping S3 alone puts feature releases on monitor (4.70 vs 7.06) and leaves noise and training data in remediation. No single stump lost leaves the run above 50 on `corelib` (44, 44, 49) or `effort.py` (40, 40, 40).
One-fact test: the strongest single-sentence hint rescues only its own source (1 of 10 results in `effort.py`, adding +12 points on `corelib` from 20 to 32, well under the 33.3 one-third ceiling), leaving the other two open sources, all four quarter-pair combined figures, and the final call wrong.
Clean-data test: on perfectly cleaned files with every clause of Standard v2 read literally, the rigorous standard shortcut (literally matching pair-3 Response 1: linear 13-refit warm-start carry, uniform-window turnover, empirical pinned-view adoption, orthogonal release sum after confirming flat scalar group MSE) produces a self-consistent analysis that misplaces all three open sources (noise escalated 12.13, training data monitor 3.65, releases monitor 4.62) and earns 20 on `corelib` and 26.7 on `effort.py`.
Not semantics: every field, unit, threshold, and Standard clause (1.4, 1.5, 1.6, 2.2, 3.1-3.3, 4.1) read literally still leaves the three core quantities unstated (no phi_f, no lambda_f, no cross-release correlation c_f is listed anywhere); identifying them requires empirical statistical estimation from the raw panel, dated bootstrap series, and merchant-level shadow vectors.
Not rule application: Standard v2 defines WHAT each quantity and band is and specifies zero estimation procedures. Applying the 5.5 and 8.0 band lines to any unadjusted shortcut yields a wrong call.
Estimand: Model Stability Standard v2 sections 1 to 6 and Schedule C: section 1 defines the five model-side sources and records warm-start carry (1.4), pinned-view insulation (1.5), and exponential recency weighting on 52/104-week windows with weighted bootstrap resampling (1.6); section 2 pins the 2027 roadmap and row plan (2.1) and defines an assessment year's weekly refreshes as the 52 Mondays of its four closing snapshot pairs (2.2); section 3 defines single-source movement (3.1, 3.2) and combined model-side movement per pair and across the year (3.3); section 4 sets the bands (under 5.5 monitor, 5.5 to under 8 remediation plan, 8 or more escalation).
No decoy: no memo, report, or dashboard ranks sources or plants a misleading claim; every instrument accurately measures its own single-step perturbation.
No replay: no result re-derives a published figure; no stated number is broken.
Pinned: 22 estimation variants in `core.py` plus 2 pack-level rivals and 15 admitted forks in `results.py` (39 variants in all) file one identical call and stay >= 0.65 points from both band lines; every shortcut and over-correction is refuted by the 3-part native points-squared 2026 internal record check (5.3 to 28.5 vs 0.53 for the committed model).
Run forecast: R2 method shortcut (linear 13-refit carry when phi is unlisted, L39/L65/N34); R3 method shortcut (uniform (entering+leaving)/(2N) when lambda is unlisted, L28/L22/N21); R4 narrow look at broad data and method shortcut (scalar pair MSE verified flat, releases summed orthogonally without inspecting merchant-level cross-release correlation, N44/L58/L28); R6 self-confirming check (weekly panel OLS with family fixed effects or residual closure); R7-R10 method shortcut and unfinished chain carried into combined quarter-pair figures and bands.
Strategy label: own (three independent statistical inverse problems on warm-start persistence, unfiled recency decay, and within-group cross-event unit covariance)
Depth level: 5: three genuinely independent, two-sided stumps on three axes (what, when, unit), opening three distinct open members (optimisation, turnover, releases) and producing 7 distinct wrong calls across the lattice (3 among single drops), with zero waivers on `corelib` and `effort.py`.
Lesson: three independent statistical inference gaps in deployed model stability attribution: (S1) inherited warm-start refit noise must be inverted from anchored warm-era gap curves (with cold-era linearity verifying non-mean-reverting entity change); (S2) unfiled exponential recency decay in rolling training windows is identified from phase-lagged seasonal variance swings of weighted bootstrap replicates against weekly labelled row volumes; and (S3) sequential multi-phase updates to the same feature group carry positive cross-event merchant covariance invisible to scalar per-release MSE checks and weekly panel regressions.

## Results chain

Figures from the cut pack (`generator/results.py` on `target/`, `figures.json`); `core.py` on the world agrees within 0.03 points on every figure.

| ID | Result (checkable) | Area | Pinned by | Band | Hurried analyst | Depends on | Graded as |
|---|---|---|---|---|---|---|---|
| R1 | cleaned panel, manifests, instruments and forced baseline sources: 25,007 unique panel merchants (28,854 before Tolka Pay mapping), retunes 4.29 points (monitor) and label revisions 9.82 points (escalation) | assembly-reconciliation | panel CSVs, migration crosswalk, registry, manifests, retune shadows, label-freeze pairs | exact merchant count; retunes 4.24 to 4.34, labels 9.76 to 9.90 | narrow look at broad data: quick pass skips migration map; careful pass nails R1 by reflex | - | Ask 1 (forced sources), Step-by-Step |
| R2 | optimisation noise alone between consecutive 2027 quarter-end snapshots: 6.86 points (remediation plan) | modeling | settled warm-era gap curves D_warm(h) anchored to replicate pairs, with cold-era D_cold(h) linearity (29-55 weeks, mean curvature -0.010) ruling out mean-reverting merchant change | 6.56 to 7.25 points | method shortcut: accumulates warm-start refit noise linearly over 13 refits (12.13 points, escalation) when no decay rate is listed (L39, L65, N34) | R1 (independent: warm/cold panel lag curves and replicate pairs) | Component 1, Ask 1 |
| R3 | training data alone between consecutive 2027 quarter-end snapshots: 6.83 points (remediation plan) | modeling | 16 dated 2026 weighted bootstrap pairs per family inverted against warehouse_labelled_rows_weekly.csv (lambda 0.906 to 0.942; 3.8x lower log-RMSE than uniform), carried to labelled_row_plan_2027.xlsx | 6.70 to 6.87 points | method shortcut: applies uniform-window turnover (entering+leaving)/(2N) (3.65 points, monitor) when Standard 1.6 lists no decay rate, or raw bootstrap (10.21, escalation) (L28, L22, N21) | R1 (independent: 2026 bootstrap pairs and warehouse/plan weekly rows) | Component 2, Ask 1 |
| R4 | feature releases alone between consecutive 2027 quarter-end snapshots: 7.06 points (remediation plan) | missingness-measurement | merchant-level pairwise same-group correlation across 141 2026 release_shadow pairs (mean 0.783, min 0.702 vs -0.001 across 2,580 diff-group pairs), combined with actual pinned-view adoption on 2027 sprint roadmap | 6.84 to 7.17 points | method shortcut and narrow look at broad data: verifies flat scalar release MSE across groups and sums unpinned 2027 releases orthogonally (4.62-4.70 points, monitor; 1.96 on plan dates) (N44, L58, L28) | R1 (independent: paired release_shadow score vectors, release log, 2027 roadmap, rollout manifests) | Component 3, Ask 1 |
| R5 | share of 2027 assessment-year weekly retrains expected to actually run on pinned feature views: 34.8 per cent | forecasting | log-linear take-up lag on custom_training_components fitted on three completed rollouts (PC-24-031, PC-24-047, PC-25-012) and evaluated over the 52 assessment-year Mondays (Standard 2.2) | 32.4 to 38.3 per cent | dismissed own evidence on quick pass (83.4 per cent on calendar planned dates); solved on careful pass (supporting step) | R1 (independent: past rollout manifests and calendar) | Ask 3 |
| R6 | three-part 2026 internal-record variance discrepancy check (D_warm(1), seasonal bootstrap contrast, same-group release covariance): 0.53 points squared vs 5.32 to 28.52 for every shortcut | validation | 2026 warm panel D_warm(1) = 47.14, 2026 high-vs-low trailing-volume bootstrap contrast = 10.88, 2026 same-group release-shadow covariance = 4.80 | 0.00 to 1.50 points squared | self-confirming check and method shortcut: checks weekly panel OLS with family fixed effects or residual balance closure, missing all three discrepancies (28.52 points squared) (L28, N44) | R2, R3, R4 | Step-by-Step |
| R7 | H1 2027 combined model-side movement: Q1 16.89 points, Q2 17.07 points | decomposition-attribution | Standard section 3.3 sum of five sources' pair mean-square movements over Q1 and Q2 2027 | Q1 16.76 to 17.03, Q2 16.85 to 17.19 | method shortcut carried through: shortcut H1 combined movement sits outside band on all single drops and reflex (17.51, 17.66) (L39, L28, N44) | R1, R2, R3, R4 | Ask 2 |
| R8 | H2 2027 combined model-side movement: Q3 15.52 points, Q4 14.69 points | decomposition-attribution | Standard section 3.3 sum of five sources' pair mean-square movements over Q3 and Q4 2027 | Q3 15.22 to 15.69, Q4 14.48 to 14.90 | method shortcut carried through: shortcut H2 combined movement sits outside band (17.11, 16.67) (L39, L28, N44) | R1, R2, R3, R4 | Ask 2 |
| R9 | full-year 2027 combined model-side movement: 16.07 points | synthesis | Standard section 3.3 root of mean of the four pairs' combined model-side mean-square movements | 15.87 to 16.26 points | method shortcut carried through: shortcut annual combined movement overshoots to 17.24 points (L39, L28, N44) | R1, R2, R3, R4 | Ask 2 |
| R10 | 2027 source placements: label revisions escalation; feature releases, optimisation noise and training data remediation plans; retunes monitor | synthesis | Standard section 4.1 band thresholds (5.5 and 8.0 points) applied to each source's 2027 movement | exact five-source band set | method shortcut carried through: escalates optimisation noise while placing training data and feature releases on monitor (L39, L28, N44) | R1, R2, R3, R4 | Recommendation |

Carry-forward: optimisation noise (R2) falls with S1 alone (Component 1); training data (R3) falls with S2 alone (Component 2); feature releases (R4) falls with S3 alone (Component 3). Each critical component is strictly independent: losing any one stump leaves the other two components earned.

## Hidden factor record

| Factor | Real or constructed | Only in deciding units | Found by | Fix depth | Verdict |
|---|---|---|---|---|---|
| warm-started weekly refits inherit prior optimisation randomness with decaying persistence phi_f in [0.65, 0.79] | constructed, how warm-started neural/GBDT retraining behaves | no: all 14 families since warm-start adoption, scaling with epochs_per_refresh | carry filed as WHAT (Standard 1.4); decay identified only by modelling warm-era D_warm(h) anchored to replicate pairs and verified against linear cold-era D_cold(h) | modelling: anchored saturating curve fit across 14 families, verified on D_warm(1) | keep |
| 52-week and 104-week rolling training windows apply unfiled exponential recency weighting lambda_f in [0.905, 0.942] | constructed, how recency-weighted retraining and weighted bootstraps behave | no: all 14 warm-era families across all 16 dated 2026 bootstrap pairs | recency weighting filed as WHAT (Standard 1.6 & manifest options); lambda_f identified only by inverting seasonal bootstrap variance swings against warehouse weekly row waves | modelling: non-linear inversion of (lambda_f, row2_f) from 224 dated bootstrap pairs, carried via weighted overlap formula to 2027 plan spans | keep |
| sequential feature releases on the same feature group move the same merchants in the same direction (positive correlation c_f in [0.72, 0.84]) | constructed, how repeated enhancements to a risk-signal group shift high-exposure merchants | no: all 14 families and all 12 feature groups across all 141 same-group 2026 release-shadow pairs | invisible in scalar MSE tables and 2026 weekly panel OLS (2026 releases spaced 27w apart); found only by correlating merchant-level signed score-delta vectors across paired shadow runs | modelling: pairwise merchant delta correlations by group from 1.4M-row pair scores file, combined with empirical pinned-view adoption probabilities across 2027 sprint roadmap | keep |

## Effort test

| Result | Quick pass | Careful but hurried | Thorough |
|---|---|---|---|
| R1 cleaned panel, manifests, instruments and forced baseline sources (retunes and labels) | Missed | Right | Right |
| R2 what optimisation noise alone moves a score between snapshots (warm-start decay) | Missed | Missed | Right |
| R3 what training data alone moves a score between snapshots (recency-weighted turnover) | Missed | Missed | Right |
| R4 what feature releases alone move a score between snapshots (within-group covariance) | Missed | Missed | Right |
| R5 share of 2027 assessment-year weekly retrains expected on pinned feature views | Missed | Right | Right |
| R6 three-part 2026 internal-record variance discrepancy check | Missed | Missed | Right |
| R7 H1 2027 combined model-side movement (Q1 and Q2 snapshot pairs) | Missed | Missed | Right |
| R8 H2 2027 combined model-side movement (Q3 and Q4 snapshot pairs) | Missed | Missed | Right |
| R9 full-year 2027 combined model-side movement | Missed | Missed | Right |
| R10 each source's band for 2027 | Missed | Missed | Right |
| Roughly | 0 of 10 | 2 of 10 | 10 of 10 |

Measured by: `.agents/skills/stumping/effort.py` on `generator/effort.json`, written by `generator/results.py` from the cut pack (quick 9.0, careful but hurried 26.7, thorough 100.0; `corelib` on the cut pack: S1/S2/S3 lost alone 44/44/49, reflex 20, rigorous 20, all four run routes 14)
Largest single hint: each one-sentence hint rescues 1 of 10 results (R2, R3, or R4 alone; `corelib` adds +12 from 20 to 32, well under the 33.3 ceiling)
Pair estimate: 26.7 (effort.py careful but hurried pass on the cut pack; corelib prices the reflex and rigorous standard routes at 20 and every single-stump loss at 44 to 49)

## Stump core

Unobserved part: single-source 13-week score movement in 2027 across five model-side sources when no file isolates any source at a 13-week gap and phi_f, lambda_f, and within-group cross-release correlation c_f are never filed.
Instruments: 870 controlled 2026 instrument pairs (replicate, 16 dated weighted bootstraps per family, retune shadows, release shadows with merchant-level score vectors, label-freeze pairs), 126-week warm and cold panel lag curves, warehouse weekly labelled rows, and three completed platform rollouts.
Referee: no referee slice ships; forcing is established by the 3-part 2026 internal-record variance discrepancy check in native points squared (golden 0.53 vs 5.32 to 28.52 for every rival).
Strongest standard route: linear 13-refit warm-start carry, uniform-window turnover, empirical pinned-view adoption, and orthogonal feature releases after verifying flat scalar MSE (matching pair-3 Response 1 literally; earns 20 on corelib, 26.7 on effort.py).
Said out loud: each stump names one statistical inversion (warm-start decay from anchored lag curves, recency decay from seasonal bootstrap variance swings, within-group merchant correlation from paired release-shadow vectors) with 4 dependent estimation steps remaining once stated.
Worth: S1 5.28 points (32.8x family spread), S2 3.19 points (31.0x family spread), S3 2.36 points (15.0x family spread).
Regimes: cold-start 26-week uniform era (29 to 55 weeks/family, strictly linear) versus warm-start 52/104-week recency-weighted era; 2026 semi-annual spaced releases (27w apart per group) versus 2027 quarterly multi-phase feature-group sprints under PC-26-058 rollout.
Sharp: all 39 variants file one call and sit >= 0.65 points from both 5.5 and 8.0 lines; every stump is two-sided across both thresholds.
Earns: corelib golden 100, S1/S2/S3 lost alone 44/44/49, S1/S2/S3 fixed alone 32/32/32, reflex 20, rigorous 20, all four run routes 14; effort.py quick 9.0, careful 26.7, single-stump-lost 40, thorough 100.0.

From `python3 task9/generator/core.py` (seed 9605), pasted verbatim:

| Member | Line | Golden | Family spread | Reflex route | Direct | Rigorous | Opened by |
|---|---|---|---|---|---|---|---|
| labels | 5.5/8 | 9.806 | 0.0234 | 9.806 | 9.806 | 9.806 | forced |
| optimisation | 5.5/8 | 6.834 | 0.161 | 12.12 | 12.12 | 12.12 | S1 |
| releases | 5.5/8 | 7.06 | 0.158 | 4.697 | 1.961 | 4.618 | S3 |
| retunes | 5.5/8 | 4.292 | 0.000676 | 4.292 | 4.292 | 4.292 | forced |
| turnover | 5.5/8 | 6.835 | 0.103 | 3.649 | 10.21 | 3.649 | S2 |

| Run route | Call | labels | optimisation | releases | retunes | turnover |
|---|---|---|---|---|---|---|
| calibrated | wrong | 9.806 | 8.686 | 2.338 | 4.292 | 4.133 |
| cutoff | wrong | 9.806 | 8.686 | 5.157 | 4.292 | 9.036 |
| generous | wrong | 9.806 | 17.14 | 11.27 | 4.292 | 9.036 |
| hedge | wrong | 9.806 | 12.12 | 1.961 | 4.292 | 3.649 |

| Figure | Block | Golden | Band | S1 lost | S2 lost | S3 lost | Reflex route |
|---|---|---|---|---|---|---|---|
| CC1 optimisation noise alone, points | components | 6.834 | 6.604 to 7.021 | flips | - | - | lost |
| CC2 training data alone, points | components | 6.835 | 6.704 to 6.869 | - | flips | - | lost |
| CC3 feature releases alone, points | components | 7.06 | 6.847 to 7.18 | - | - | flips | lost |
| optimisation points | asks | 6.834 | 6.604 to 7.021 | moves | - | - | lost |
| turnover points | asks | 6.835 | 6.704 to 6.869 | - | moves | - | lost |
| releases points | asks | 7.06 | 6.847 to 7.18 | - | - | moves | lost |
| labels points | asks | 9.806 | 9.777 to 9.812 | - | - | - | earned |
| retunes points | asks | 4.292 | 4.292 to 4.293 | - | - | - | earned |
| Q1 combined model-side RMS | asks | 16.88 | 16.78 to 16.96 | moves | moves | moves | lost |
| Q2 combined model-side RMS | asks | 17.06 | 16.87 to 17.15 | moves | moves | moves | lost |
| Q3 combined model-side RMS | asks | 15.5 | 15.23 to 15.66 | moves | moves | moves | lost |
| Q4 combined model-side RMS | asks | 14.67 | 14.4 to 14.81 | moves | moves | - | lost |
| 2027 combined model-side RMS | asks | 16.06 | 15.89 to 16.15 | moves | moves | moves | lost |
| pinned views share | asks | 34.83 | 32.47 to 38.2 | - | - | - | earned |

| Route | Call | Earns on the rubric |
|---|---|---|
| golden | right | 100 |
| S1 lost alone | wrong | 44 |
| S2 lost alone | wrong | 44 |
| S3 lost alone | wrong | 49 |
| S1 fixed alone | wrong | 32 |
| S2 fixed alone | wrong | 32 |
| S3 fixed alone | wrong | 32 |
| reflex route (every stump lost) | wrong | 20 |
| rigorous standard route | wrong | 20 |
| calibrated run route | wrong | 14 |
| cutoff run route | wrong | 14 |
| generous run route | wrong | 14 |
| hedge run route | wrong | 14 |

PASS  shape                                    5 members, 3 stumps (two or more of each)
PASS  golden files the truth's call            golden (2, 1, 1, 0, 1), truth (2, 1, 1, 0, 1)
PASS  variant battery                          22 variants, the call holds under every one
PASS  lattice complete                         every stump alone, all together, all but one
PASS  reflex route misses the call             open members: optimisation, releases, turnover
PASS  stump S1                                 dropped alone moves its member optimisation (worth 5.28, 32.8 times the family's spread 0.161); fixed alone on the reflex route still misses
PASS  stump S2                                 dropped alone moves its member turnover (worth 3.19, 31.0 times the family's spread 0.103); fixed alone on the reflex route still misses
PASS  stump S3                                 dropped alone moves its member releases (worth 2.36, 15.0 times the family's spread 0.158); fixed alone on the reflex route still misses
PASS  no easier route on an open member        the direct and the rigorous standard routes land wrong on every open member
PASS  distinct wrong answers                   7 distinct wrong calls across the lattice, 3 among the single drops
PASS  falsification check                      golden off by 0.216; rivals off by S1 linear carry 12.3, S2 uniform window 13.8, S3 orthogonal releases 5.01, direct 27.6, rigorous (Response 1) 28.3
PASS  run routes listed                        the four routes the runs take are implemented: calibrated, cutoff, generous, hedge
PASS  run routes land wrong                    each files a wrong call: calibrated (2, 2, 0, 0, 0); cutoff (2, 2, 0, 0, 2); generous (2, 2, 2, 0, 2); hedge (2, 2, 0, 0, 0); with 8 further settings, every one wrong
PASS  both sides of the line                   the shortcuts and the run routes miss above and below the golden's classes
PASS  stump S1 two-sided                       lost alone and over-corrected alone both file a wrong call (over: (2, 0, 1, 0, 1))
PASS  stump S2 two-sided                       lost alone and over-corrected alone both file a wrong call (over: (2, 1, 1, 0, 2))
PASS  stump S3 two-sided                       lost alone and over-corrected alone both file a wrong call (over: (2, 1, 2, 0, 1))
PASS  stumps on different axes                 axes: unit, what, when
PASS  graded figures listed                    3 critical components (two to five) and 11 ask figures (two or more) in 10 sentences, each one criterion
PASS  every graded figure banded by the battery each figure's band holds its twelve or more variants
PASS  one stump lost, the run stays under the bar a run that loses only S1 earns 44, S2 earns 44, S3 earns 49 (50 or under each; the review reads its strongest run)
PASS  the reflex route on the rubric           every stump lost earns 20 (30 or under; 9 of it is instruction-following); figures it still lands: labels points, retunes points, pinned views share; sentences it lands whole: forced sources
PASS  one stump fixed alone earns more, a third at most S1 fixed alone earns 32; S2 fixed alone earns 32; S3 fixed alone earns 32
PASS  critical components independent          each falls with one stump alone: CC1 optimisation noise alone, points with S1, CC2 training data alone, points with S2, CC3 feature releases alone, points with S3
PASS  the rigorous standard route on the rubric it earns 20 (50 or under)
PASS  the calibrated route on the rubric       it earns 14 (50 or under; the review reads the strongest run)
PASS  the cutoff route on the rubric           it earns 14 (50 or under; the review reads the strongest run)
PASS  the generous route on the rubric         it earns 14 (50 or under; the review reads the strongest run)
PASS  the hedge route on the rubric            it earns 14 (50 or under; the review reads the strongest run)
PASS  open members opened by different stumps  3: optimisation by S1; turnover by S2; releases by S3
CORE PASS level 5  task9

## Stump factorial

Reflex route: every file cleaned and every Standard clause read literally; retunes (4.29) and label revisions (9.82) scaled by snapshot-pair frequency; actual pinned-view adoption lag fitted from the three past rollouts (34.8 per cent); warm-start noise accumulated linearly across 13 refits (12.13, escalation); uniform-window turnover applied when no recency decay rate is listed (3.65, monitor); unpinned 2027 releases summed orthogonally after confirming flat scalar per-release MSE across groups (4.70, monitor). It misplaces all three open sources and scores 20 on `corelib` and 26.7 on `effort.py`.

| Judgment | Kind | Hurried choice | Evidence | Dropped alone from the golden | Fixed alone on the reflex route | One routine step once told |
|---|---|---|---|---|---|---|
| S1 warm-started refit noise decays from refit to refit, identified from anchored warm-era gap curves (with cold-era linearity verifying non-mean-reverting merchant change) | stump | linear 13-refit carry (half or full replicate pair per refit) | L39, L65, N34 | optimisation noise 12.13 (escalation); other four sources hold; call wrong | optimisation 6.86 (plan); training data & releases still monitor; R2 rescued only | no (four dependent steps) |
| S2 long training windows apply unfiled exponential recency weighting inverted from seasonal swings across 16 2026 bootstrap pairs per family against weekly labelled rows | stump | uniform-window turnover (entering+leaving)/(2N) | L28, L22, N21 | training data 3.65 (monitor); other four sources hold; call wrong | training data 6.83 (plan); optimisation & releases still wrong; R3 rescued only | no (four dependent steps) |
| S3 sequential feature releases modifying the same feature group move the same merchants in the same direction, adding positive within-group cross-release covariance across 2027 sprints | stump | orthogonal sum of unpinned releases | N44, L58, L28 | feature releases 4.70 (monitor); other four sources hold; call wrong | feature releases 7.06 (plan); optimisation & training data still wrong; R4 rescued only | no (four dependent steps) |
| J4 retunes and label revisions scaled by snapshot-pair frequency | reflex | - | R20 | same call | - | - |
| J5 actual pinned-view adoption lag fitted from three completed rollouts | reflex | - | R73 | same call | - | - |
| J6 re-sent refreshes, Tolka Pay migration crosswalk, scheduler family codes and duplicate manifests resolved | reflex | - | R01 | same call | - | - |

Level: 5: three necessary, independent, two-sided stumps on three axes, none sufficient alone, producing 7 distinct wrong calls across the lattice (3 among single drops).

## Open members

| Member | Golden margin | Family spread | Reflex route | Direct route | Opened by |
|---|---|---|---|---|---|
| optimisation noise | 6.86 points, remediation plan (1.36 above 5.5, 1.14 below 8.0) | 0.180 | wrong: 12.13, escalation | wrong: 12.13, escalation | S1 |
| training data | 6.83 points, remediation plan (1.33 above 5.5, 1.17 below 8.0) | 0.095 | wrong: 3.65, monitor | wrong: 10.21, escalation | S2 |
| feature releases | 7.06 points, remediation plan (1.56 above 5.5, 0.94 below 8.0) | 0.158 | wrong: 4.70, monitor | wrong: 1.96, monitor | S3 |
| label revisions | 9.82 points, escalation (1.82 above 8.0) | 0.024 | right: 9.82 | right: 9.82 | forced |
| retunes | 4.29 points, monitor (1.21 below 5.5) | 0.001 | right: 4.29 | right: 4.29 | forced |

Direct route: raw bootstrap face value for training data (10.21, escalation), linear 13-refit carry for optimisation noise (12.13, escalation), calendar planned weeks with orthogonal releases (1.96, monitor), and forced retunes (4.29) and label revisions (9.82). `core.py` runs it as `direct`; it lands wrong on all three open members.

## Data provenance

Source: generated by the build's simulator of Garrane Risk's weekly retraining platform (`generator/core.py`, `pack.py`, `docs.py`); nothing public is used.
Behaves like the real thing: simulates 14 merchant-risk model families over 126 weekly Mondays (1 July 2024 to 23 November 2026) with cold-start 26-week uniform eras (29 to 55 weeks per family) followed by warm-start 52/104-week exponentially recency-weighted eras, seasonal + multi-week promo waves in labelled rows, four-week retune cadences, 24 semi-annual 2026 feature releases (spaced 27 weeks apart per group across 12 feature groups), merchant-level latent sensitivity per feature group, weekly label revisions, non-mean-reverting merchant own drift, panel attrition, three completed platform rollouts with custom-component adoption lags and reverts, and 870 instrument pairs in 2026 (including 16 dated weighted bootstrap pairs per family).
Genuine patterns: (1) family-specific seasonal cycles and volume waves in weekly labelled rows; (2) smaller books carry noisier estimates; (3) cold-start era with 26-week uniform windows and higher independent refit noise before warm-start adoption; (4) adoption lags scaling with custom_training_components plus temporary reverts; (5) semi-annual feature-group refreshes in 2026 shifting into quarterly multi-phase feature-group sprints in 2027; (6) merchant attrition across the panel.
Problems by process: four re-sent weekly panel refreshes after late label loads, Tolka Pay acquirer merchant ID migration crosswalk, scheduler vs registry family code schemes, manifest rows / train_rows rename across runtime 4.1.0, nine duplicate retried manifest lines, ISO weeks beside Monday dates, and panel attrition.
License: proprietary, fictional organisation (generated).
Used as is: not applicable.
Breadth: 29 files across CSV, JSONL, XLSX, and PDF: 10 quarterly panel CSVs (2.85 million cleaned merchant-week rows across 25,007 merchants), 41 MB instrument pair scores file (870 pairs), 1.3 MB scheduler JSONL, warehouse weekly rows, registry, release and retune logs, three operational workbooks, two governing PDFs, and three unlabelled distractors (weekly discrimination/calibration metrics, feature PSI drift, training compute by run).

## Template check

Chain signature: assembly-reconciliation, missingness-measurement, modeling, modeling, forecasting, validation, decomposition-attribution, synthesis.
Question form: where (where each model-side source belongs for 2027: monitor, a remediation plan or escalation), alongside combined quarter-pair and annual model-side movements and pinned-views retrain share.
Nearest build: task25 (bridge with weight on modeling) by chain signature only; task25 rebuilds throughput across operating conditions with none of the three variance-component inversions here (warm-start lag-curve persistence, seasonal bootstrap recency decay inversion, merchant-level shadow-vector within-group covariance). Nearest driver cosine similarity across the entire corpus is 0.03.

## Frontier check

Precedents: R2 careful Missed on L39, L65, N34 (linear 13-refit warm-start carry when decay rate is unfiled, confirmed directly by 4/4 live runs on arch 5 pairs 2 and 3); R3 careful Missed on L28, L22, N21 (uniform-window turnover when recency decay rate is unfiled); R4 careful Missed on N44, L58, L28 (orthogonal sum after scalar group MSE check without inspecting cross-release merchant correlations, confirmed directly by pair-3 Response 1's scalar group-MSE check); R6 careful Missed on L28, N44; R7, R8, R9, and final band placements careful Missed on L39, L28, N44 carried through. R1 and R5 are Right on careful pass.
Shallow path checks: R2 linear carry closes the 13-week residual budget and passes weekly panel OLS with family fixed effects (whose intercepts absorb the noise level), refuted by warm-era gap-curve concavity (intercept 48+ pts^2) and D_warm(1) discrepancy (12.62 pts^2 vs 0.53); R3 uniform turnover closes the budget and passes static mean bootstrap checks, refuted by 16-date seasonal bootstrap log-RMSE (3.8x worse) and high-vs-low volume contrast discrepancy (13.99 pts^2 vs 0.53); R4 orthogonal releases passes flat scalar group MSE and 2026 weekly panel OLS (R^2 > 0.97, slope 1.00 because 2026 same-group pairs are 27w apart), refuted by 141/141 strictly positive same-group merchant correlations in mrm_instrument_pair_scores_2026.csv (5.32 pts^2 discrepancy vs 0.53).
Assumption made false: (1) warm-start refit noise carries linearly across 13 weeks without decaying (false in every warm family; verified against linear cold-era curves); (2) unfiled recency weighting can be approximated by equal-weight (in+out)/(2N) turnover (false in every warm 52/104w family; refuted by 16 seasonal bootstrap pairs); (3) sequential feature releases touching the same feature group are orthogonal across merchants (false across all 141 same-group pairs in 2026).
Forcing: across 22 core variants, 2 pack rivals, and 15 admitted forks (39 variants total), every single variant files the exact same five placements and stays >= 0.65 points from both 5.5 and 8.0 lines. Moving any source's variance +/-20 per cent holds every band (`checks.py` and `effort.py` assert all 10 perturbations). Every stump is strictly two-sided: S1 hurried 12.13 (Escalation) / over 4.76 (Monitor); S2 hurried 3.65 (Monitor) / over 9.04-10.21 (Escalation); S3 hurried 4.70 (Monitor) / over 11.10 (Escalation).
Noun swap: `skeleton.py check task9` PASS/WARN (0 BLOCK), severity none against every card, lineage entry, and client skeleton; swapping nouns breaks warm-start refit persistence, weighted bootstrap variance inversion, and merchant-level release-shadow vectors.
Closed strategies: the three deciding lessons are `inherited_noise_persistence` (S1), `recency_weighted_training_turnover` (S2), and `shared_group_event_covariance` (S3); none is on the client's 45 closed strategies page. `inherited_noise_persistence` sits next to the closed card "Outcomes cluster, so item-level intervals are far too narrow" only through serial dependence: nothing here is a confidence interval or clustered standard error; the estimand is a point variance component at lag 13 inverted from an anchored lag curve. Neither `recency_weighted_training_turnover` (inverting an unfiled exponential sample-weight decay from seasonal resample variance swings) nor `shared_group_event_covariance` (cross-event unit-level covariance from paired shadow vectors across multi-phase feature-group sprints) touches any closed card.
Decisive steps: S1 owns "optimisation noise alone moves a merchant's score 6.86 points between consecutive quarter-end snapshots in 2027" (Component 1, workbook sheet 1 & 4; 4 steps left once named); S2 owns "training data alone moves a merchant's score 6.83 points" (Component 2, workbook sheet 1 & 5; 4 steps left once named); S3 owns "feature releases alone move a merchant's score 7.06 points" (Component 3, workbook sheet 1 & 6; 4 steps left once named). Independence: dropping any one stump leaves the other two components inside their bands and produces 3 distinct single-drop calls and 7 distinct wrong calls across the lattice.
Run routes: calibrated (cut-8 gap intercept + unnetted uniform turnover + declared slip + orthogonal releases) earns 14; cutoff (cut-8 + 13w cutoff bootstrap + custom-component threshold + orthogonal releases) earns 14; generous (full replicate pair per refit + net bootstrap face + aligned releases + worst lag) earns 14; hedge (linear half-pair + uniform turnover + plan dates + orthogonal releases) earns 14. Eight further run-route settings all file wrong calls on both sides of the band lines.
Validation handles: zero validation handles ship in the pack. No file observes any 2027 outcome, no file isolates single-source 13-week movement, no file lists phi_f, lambda_f, or c_f, and no referee slice ships; forcing rests on the 3-part 2026 internal record falsification check (D_warm(1), seasonal bootstrap contrast, same-group release-shadow covariance).
Forward window: none of the three open sources is a 2026 average restated. Training data runs on 2027's planned weekly labelled row waves (`labelled_row_plan_2027.xlsx`), feature releases shift from 2026's 24 semi-annual spaced releases into 2027's 28 multi-phase quarterly feature-group sprints filtered by the 2027 PC-26-058 pinned-view rollout curve (`feature_platform_roadmap_2027.xlsx`), and warm-start noise operates across 2027's warm-started schedule.

## Semantic fork table

| ID | Term or convention | Readings | Golden | Ruled out by |
|---|---|---|---|---|
| SF1 | a source's movement | book-weighted RMS score change between consecutive quarter-end snapshots from the source alone; MAD; variance | RMS points | Standard section 3.1 and 3.2 |
| SF2 | book weighting | latest closed quarter-end snapshot (21 Sep 2026); Dec 2027 planned book; equal family weights | 21 Sep 2026 snapshot | Standard section 3.1; Dec 2027 planned book is in variant battery (same call); equal weights ruled out by section 3.1 |
| SF3 | 2027 weekly refreshes | 52 Mondays belonging to the four closing snapshot pairs (28 Dec 2026 to 20 Dec 2027); calendar 2027 Mondays (4 Jan to 27 Dec) | 52 assessment-year Mondays | Standard section 2.2 (explicitly closes Holistic Audit v3 window fork) |
| SF4 | bands and boundaries | Monitor < 5.5, Remediation 5.5 to < 8.0, Escalation >= 8.0 | as filed | Standard section 4.1; all 39 variants stay >= 0.65 pts from both lines |
| SF5 | combined model-side movement | root of sum of five sources' pair MS (and root of mean of four pairs' combined MS for the year); sum of RMS | RMS across five sources | Standard section 3.3 |
| SF6 | warm-start noise carry (S1) | anchored AR(1) decay on D_warm(h) - D_data(h) (with cold-era D_cold(h) verifying linear non-mean-reverting own change); linear 13-refit carry (half or full replicate pair); raw replicate pair; unanchored raw bend; gap-8 line intercept | anchored AR(1) decay (6.86) | Standard 1.4 rules out raw replicate (4.76); warm-era bend & D_warm(1) check rule out linear carry (12.13, 17.15); cold-era linearity (mean curv -0.010 across 29-55 wks) rules out mean-reverting merchant change; replicate pairs rule out raw unanchored bend and gap-8 line |
| SF7 | gap-curve horizon, weights, start week, data subtraction | 18/20/25 lags, lag-2 start, 2026-only (weighted), flat weights on full settled weeks, with/without subtracting D_data(h), 4 settled-week start rules | 25 lags, 1/D^2 weights, settled warm weeks, D_data subtracted | all admitted variants sit in 6.57 to 7.25 and keep the call; subtracting vs not subtracting D_data shifts opt13 by only ~0.12 pts (proving S1/S2 independence); unweighted flat fit on short 48w 2026-only slice is ruled out by noisy tail variance |
| SF8 | recency weighting in training windows (S2) | exponential recency decay inverted from 16 2026 bootstrap pairs (family, window, pooled; log-OLS, WLS, OLS); alternative smooth monotone kernels (power-law, linear ramp); uniform (entering+leaving)/(2N); raw/net bootstrap face value | per-family log-OLS exponential (6.83) | Standard 1.6 pins exponential recency weighting; all 5 exponential estimators sit in 6.70 to 6.87; power-law (7.29) and linear ramp (6.22) also stay in Remediation while exponential wins log-RMSE (0.049 vs 0.188 uniform); uniform (3.65) and raw bootstrap (10.21) fail the 16-date seasonal contrast check (13.99 vs 0.53 pts^2) |
| SF9 | bootstrap seed netting | net of replicate pair variance; gross bootstrap | net of replicate | manifests show bootstrap pairs draw independent seeds in addition to resampled rows |
| SF10 | feature-release cross-event correlation (S3) | per-family or pooled empirical same-group correlation from 2026 release_shadow vectors with 0 cross-group correlation; orthogonal sum (c=0); all releases perfectly aligned (c=1); same rho on cross-group pairs | per-family empirical same-group correlation (7.06) | pooled same-group coherence sits inside band (same call); orthogonal sum (4.70) fails 141/141 positive same-group pairs (mean 0.783, min 0.702; 5.32 vs 0.53 pts^2 check); full alignment (11.10) contradicts 2,580 cross-group pairs averaging -0.001 |
| SF11 | pinned feature views adoption timing | empirical take-up lag from three past rollouts (log-linear, linear, grouped, family-own, pooled, no-revert, plug-in median); calendar planned weeks; environment-release slip only; never pinned | log-linear lag on custom components with reverts (34.8%) | prompt specifies "expected to actually run" and calendar legend defines completed_on as environment release; all empirical take-up forms (with and without reverts) sit in 32.4 to 38.3 per cent and keep releases in 6.84 to 7.17; calendar planned dates (83.4%) and slip-only (79.5%) contradict 42 past family rollouts |
| SF12 | 2027 roadmap and row plan | filed 2027 workbooks as-is; 2026 carried forward | filed 2027 workbooks | Standard section 2.1 |
| SF13 | retunes and label revisions | 13/4 retunes and 13 label revisions per snapshot pair | 3.25 retunes, 13 labels | retune log 4-week cadence and weekly label-freeze pairs |
| SF14 | panel hygiene (Layer 1) | later load_id supersedes, Tolka Pay ID crosswalk applied, deduplicated run_id | cleaned panel | leaving any one hygiene step undone keeps every graded figure inside its stated band (`checks.py` R2) |
| SF15 | panel weighting rival | 21 Sep 2026 scored book; 5x monitoring panel active at 21 Sep 2026 | scored book | Standard section 3.1; 5x panel count keeps every figure inside its band |

## Pinning list

| Constant | Golden value | Home |
|---|---|---|
| band thresholds | 5.5 and 8.0 points | gms_model_stability_standard_2026.pdf, section 4.1 |
| snapshot gap and 2027 dates | every 13th Monday; closing 22 Mar, 21 Jun, 20 Sep, 20 Dec 2027 | acquirer_agreement_schedule_c_tier_stability.pdf, C2.1 |
| assessment-year weekly refreshes | 52 Mondays (28 Dec 2026 to 20 Dec 2027) | gms_model_stability_standard_2026.pdf, section 2.2 |
| combined model-side movement | root of summed five-source MS per pair and year | gms_model_stability_standard_2026.pdf, section 3.3 |
| warm-start carry, pinned insulation, recency weighting WHAT | warm-start carries noise; pinned views insulate releases; 52/104w use exponential recency weighting & weighted bootstraps | gms_model_stability_standard_2026.pdf, sections 1.4, 1.5, 1.6 |
| scored book weights | 21 Sep 2026 scored merchants by family | gms_scored_book_by_family.csv; Standard section 3.1 |
| training windows & options | 26w uniform (cold) -> 52w/104w recency_decay (warm) | training_scheduler_runs_2024_2026.jsonl; gms_model_registry.csv |
| weekly labelled rows | historical warehouse + 2027 filed plan | warehouse_labelled_rows_weekly.csv; labelled_row_plan_2027.xlsx |
| past & 2027 feature releases | 24 semi-annual 2026 releases (2/group, 27w apart); 28 2027 sprint releases | feature_platform_release_log.csv; feature_platform_roadmap_2027.xlsx |
| pinned rollout planned weeks & past rollouts | PC-26-058 planned weeks; PC-24-031, PC-24-047, PC-25-012 | platform_change_calendar.xlsx |
| custom components, epochs, groups read | per family | gms_model_registry.csv |
| warm-start persistence phi_f | fitted 0.64 to 0.82 | measured: panel scores + replicate pairs (spread 6.56 to 7.25) |
| recency decay lambda_f | fitted 0.906 to 0.942 | measured: 224 dated 2026 bootstrap pairs + warehouse rows (spread 6.70 to 6.87) |
| within-group release correlation c_f | measured mean 0.783 (min 0.702, n=141) vs diff-group -0.001 | measured: mrm_instrument_pair_scores_2026.csv + release log (spread 6.84 to 7.17) |
| pinned-view adoption lag & revert share | log-linear on custom components (LOO validated) | measured: scheduler manifests + change calendar (spread 32.4 to 38.3%) |

Variant battery: 39 variants (22 estimation variants in `generator/core.py` plus 2 pack-level rivals and 15 admitted forks in `generator/results.py`): every variant files one answer and stays inside its stated band.

## Closure table

| Axis | Closure |
|---|---|
| 1 | Population: every scored merchant weighted by 21 Sep 2026 family book; monitoring panel is 1 in 5 per family |
| 2 | Unit of account: RMS score points (0 to 1,000 scale); variances in points squared; pinned share in per cent |
| 3 | Attribution window: single-source movement and five-source combined movement across consecutive 13-week quarter-end snapshots |
| 4 | As-of dating: records extracted week of 23 Nov 2026; latest closed snapshot 21 Sep 2026 |
| 5 | Version basis: later load_id supersedes on re-sent refreshes; deduplicated run_id in scheduler manifests |
| 6 | Denominator: 52 assessment-year Mondays x 14 families (728 family-weeks) for pinned share; 4 snapshot pairs for annual RMS |
| 7 | Weighting: scored merchants at 21 Sep 2026 for score movements; equal family-week weight for retrain share |
| 8 | Window length: 4 closing snapshot pairs of 2027; settled warm weeks for warm lag curves; pre-warm cold weeks (29-55w) for cold linearity |
| 9 | Boundary inclusivity: 5.5 is remediation plan, 8.0 is escalation; all 39 variants stay >= 0.65 points from both lines |
| 10 | Rounding path: full precision throughout; points stated to 2 decimals, shares to 1 decimal, bands rounded outward |
| 11 | Tie-break: none needed |
| 12 | Maturity and censoring: all three past rollouts completed inside record; attrited merchants scored through last active week |
| 13 | Order of operations: clean record -> baseline instruments -> S1/S2/S3 independent inversions -> 2026 falsification -> pair & annual combined RMS -> bands |
| 14 | Row order: invariant to file row order |
| 15 | Duplicate resolution: later load_id supersedes; duplicate retried run_id dropped |
| 16 | Identity normalisation: Tolka Pay crosswalk applied; scheduler job_family mapped to registry model_family |
| 17 | Netting against gross: bootstrap pair variance netted of replicate variance; warm lag curve optionally netted of smooth data curve (S1 invariant within 0.12 pts) |
| 18 | Dimensional units: points, points squared, per cent, Monday ISO dates |
| 19 | Code and status semantics: run kind (production, replicate, bootstrap, retune_shadow, release_shadow, label_freeze); sample_weights (uniform vs recency_decay); completed_on = environment release |
| 20 | Integerisation: none; counts as recorded |
| 21 | Clause scope: bands apply per source (Standard 4.1); combined movement sums all five sources' MS (Standard 3.3) |
| 22 | Forward window contents: 2027 roadmap sprints, 2027 labelled-row plan, empirical PC-26-058 pinned adoption over 52 Mondays from 28 Dec 2026 |

## Literal reader

Standard v2 read literally pins every WHAT convention: five model-side sources (1.2), warm-start carry (1.4), pinned-view insulation (1.5), exponential recency weighting on 52/104-week windows with weighted bootstrap resampling (1.6), 2027 roadmap and row plan (2.1), 52 assessment-year Mondays (2.2), single-source and combined RMS definitions (3.1-3.3), and 5.5 / 8.0 bands (4.1). None of these clauses names an estimator, decay parameter, correlation coefficient, or adoption lag. Every one of those parameters is uniquely forced by the shipped 2024-2026 data and confirmed by the 3-part 2026 internal record check.

Stump-vocabulary sweep, ruled in main thread: governing PDFs state only the five source names, snapshot calendar, and WHAT definitions (sections 1.4, 1.5, 1.6, 2.2, 3.1-3.3, 4.1); zero decay parameters, half-lives, correlations, lag-curve methods, or mean-reversion hints appear anywhere in the shipped pack (`checks.py` never-filed check asserts 0 hits).

## Prompt contract

A rewrite keeps: the Garrane Merchant Score name, the opening where-question over the three bands (monitor, remediation plan, escalation), each source's 2027 snapshot-pair movement and band, combined model-side movement for each of 2027's four quarter-end snapshot pairs and the year, expected share of 2027 weekly retrains actually run on pinned feature views, and a workbook opening on the call plus a few slides leading with the call. It never adds: method/instrument names (bootstrap, replicate, warm start, recency, lambda, phi, covariance, correlation, lag curve, adoption lag), file names, warnings, rounding rules, counts, or persona.

## Build brief

World: Garrane Risk (Dublin), Garrane Merchant Score (0 to 1,000, four Schedule C tiers at 400/500/600, 12% covenant cap), 14 model families, 126 weekly Mondays (1 July 2024 to 23 November 2026), seed 9605 (`generator/core.py`).
Frozen: SEED 9605, `core.py` constants and world/simulate draws, 3 independent stumps (S1 warm-start decay phi_f in [0.65, 0.79] + linear cold-era D_cold over >=24 weeks; S2 exponential recency decay lambda_f in [0.905, 0.942] inverted from 16 dated 2026 bootstrap pairs/family; S3 within-group release coherence c_f in [0.72, 0.84] from 24 semi-annual 2026 releases spaced 27w apart per group carried to 28 2027 multi-phase sprint releases alongside empirical PC-26-058 pinned adoption), 22 core variants, 7-subset lattice, 4 run routes + 8 extra settings, 3-part native points-squared 2026 falsification check, and `CORE PASS level 5` with zero waivers.
Files: 29 files in `target/` (10 quarterly panel CSVs, roster, Tolka Pay crosswalk, book snapshot CSV, scheduler JSONL with sample_weights option, warehouse weekly rows, 870-pair instrument register and scores CSVs, registry, release log, retune log, 2026 covenant monitor, 3 operational XLSX files, 2 LibreOffice-exported PDFs, 3 unlabelled distractors).
Goldens: `golden/garrane_score_stability_sources_2027.xlsx` (9 formula-driven sheets opening on the 2027 committee call, LibreOffice Calc verified) and `golden/garrane_stability_review_2027.pptx` (5 executive 16:9 committee slides leading with the call), plus `submission.md` (4 platform blocks recomputed verbatim from `figures.json`).
Free: formatting, prose voice, sheet layout, chart palette, and operational naming outside the frozen numeric tables and Standard v2 WHAT clauses.
Never filed: any phi_f, lambda_f, half-life, correlation, covariance, or mean-reversion statement; any frozen-model rescore; any slid-window or multi-week rerun; any pre-computed variance attribution or ranking table; any data dictionary or field notes.

## Architecture 5 record (superseded 2026-11-23)

Pair 2 scored 0.72 / 0.52 (mean 0.62, ECF credit on derived shares and tiers); after trimming derived asks, pair 3 scored 0.60 / 0.60 (mean 0.60, borderline fail, depth 4 concentrated 30/40 on warm-start noise decay, with uniform training-window overlap solved 4/4 across pairs 2 and 3 and pinned adoption solved by both pair-3 runs). All pair 1-3 responses, rubrics, triages, and Holistic Audits v2/v3 are archived under `task9/runs/`. Upgraded to Level-5 architecture 6 on 2026-11-23.

## Tried and rejected

- Keeping uniform training-window overlap `(entering + leaving)/(2N)` as a stump: rejected because 4 of 4 frontier runs solved it cleanly (`runs/arch5_pair2_*`, `runs/arch5_pair3_*`).
- Week-level macro shocks in training data (row vs week bootstrap): rejected (too close to closed card #9 on clustered outcomes).
- Positive-event count K vs total rows N decoupling: rejected (closed card #19 on outcome clock).
- Stationary HPO bounce on retunes or MA(q) correlated label revisions: rejected because both inject non-linear bend into D_warm(h) and D_cold(h), coupling S1 to other sources and undermining cold-era linearity proof.
- Warm-started bootstrap contraction `(1 - phi_f)^2`: rejected because it couples S2 directly to S1 persistence phi_f.
- Adding an explicit "merchants' own change does not mean-revert" sentence to Standard v2: rejected as leaky; replaced with empirical cold-start linearity across 29-55 cold weeks per family.
- Including derived ratios (model-side shares, merchants' own share, tier changes) in graded asks: rejected because Holistic Audit v3 granted 30 pts of ECF credit on derived ratios in pair 2; kept strictly as non-graded Standard sections 5 and 6 workbook context.
