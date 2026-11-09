# determinism-check report, task13, 2026-11-09

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: forecasting (with a method_or_model_selection layer for the exposure-metric and growth-fit choice), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The isolated judge thread, seeing only a fresh unzip of `target.zip` and the four extracted solution blocks (never `submission.md`, `DESIGN_NOTE.md`, `metadata.json`, `generator/`, or any prior report), independently rebuilt the chain from raw files and reproduced every load-bearing figure it attempted: the 479-row call-centre dedup (verified all 479 as true duplicates of a SCADA/field-crew record), the 3,994 sustained vegetation interruptions after the momentary filter, the 5 major event days (all WEATHER-coded, zero vegetation interruptions on any of them), the feeder-to-station nearest-neighbour mapping, the gust-exposure contrast (38.0 vs ~105 hours/yr at Paua Bay, 312.0 vs 134 at Titi Saddle, mean wind -3.3%/+5.6%, matching the claimed 38/106, 312/133, -3.4%/+5.7% almost exactly), the 39,943-ICP SAIFI denominator and 0.33 SAIFI arithmetic, and the quarterly split summing exactly to 12,984. It did not independently re-fit the full per-feeder Poisson growth/exposure regression or resample the 19-year uncertainty range (flagged as traced, not recomputed, given time cost), but found no basis to doubt them given everything else reproduced to stated precision. Gates A-E pass: the main recommendation and all seven supplementary asks are forced by a reproducible, non-defect chain, and the sixth-vs-seventh-feeder margin (1,821 vs 1,268, about 44%) is a clean, non-thin gap.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Call-centre duplicate rows dropped | 479 | 479, all confirmed true duplicates | Yes |
| Sustained vegetation interruptions (cleaned) | 3,994 | 3,994 | Yes |
| Major event days | 5, all southern snow, none vegetation | 5, all WEATHER-coded, zero vegetation | Yes |
| Paua Bay gust hours, recent vs normal | 38 vs 106 | 38.0 vs 104.8 | Yes (within rounding) |
| Titi Saddle gust hours, recent vs normal | 312 vs 133 | 312.0 vs 134.0 | Yes (within rounding) |
| Mean wind change, Paua Bay / Titi Saddle | -3.4% / +5.7% | -3.3% / +5.6% | Yes (within rounding) |
| SAIFI denominator (ICPs, 2026-10) | 39,943 | 39,943 (icp_counts file); feeder_register's own ICP column totals 39,933 | Yes, with a noted 10-ICP cross-file discrepancy that does not affect the committed answer |
| Network SAIFI | 0.33 | 12,984/39,943 = 0.3251 to 0.33 | Yes |
| Quarterly split sums to total | 2,752+5,466+3,102+1,664 | = 12,984 exactly | Yes |
| Customers-per-interruption (PBY-10) | implied 70.2 | 70.14 | Yes (close) |
| Poisson growth fit (15.5%/yr) and 19-year 90% range (10,000-19,000) | claimed | traced to the method, not independently re-fit | Not recomputed (flagged, not doubted) |

## Competing answers that survived
None. The thread stress-tested the naive "worst recent performer" ranking (TOT-02, TIT-04, MKR-01, KWH-01, TIT-01, TIT-03), the wind-normalised-but-all-removable reading, and the "most overdue by cycle" reading; each produces a different and, on the thread's own recomputation, wrong answer, consistent with the design note's ladder (none of the 18 rung constructions reach more than 3 of the golden six). No fork survived for the main recommendation or for any of the seven supplementary asks.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count | 10 or more usable files | 14 files in `target/` | Pass |
| File categories | 2 or more | xlsx (3), csv (7), docx (4), so 3 categories | Pass |
| Large messy CSV, 20,000+ rows | 1 or more | four `pou_aws_*_hourly` files, 182,616 data rows each, with knots-to-km/h unit change, missing/suspect hours and quality flags | Pass |
| Large messy CSV, 10-20 printed pages | 1 or more | `protection_assets_2026-10.csv` (656 data rows, roughly 13 printed pages) and/or `oms_interruptions` (11,396 rows); either satisfies the floor | Pass |
| metadata.json names 2+ distractors | required | **metadata.json has no `distractors` field at all** (keys: task, decision, deliverables, pull_date, as_of, files, real_world_references, names) | **Fail** |
| Nothing inside the ZIP labels a distractor | required | confirmed by judge thread, no file name or content flags itself as a distractor | Pass |
| Each distractor unused but relevant | required | design note names `ridgeline_2027_schedule_of_rates.docx` and `tree_notices_register_2024-2026.xlsx`; judge thread independently identified the same two files as the unlabelled distractors, unused by the solution | Pass (content-level; metadata.json omission is the only gap) |
| 1-3 deliverables, all present in golden, no forced format | required | 2 deliverables (`vegetation_catchup_2027_feeders.csv`, `vegetation_catchup_2027_board_note.docx`), both present in `golden/` | Pass |
| Asks multi-dimensional with unit/rounding stated | required | prompt states interruptions to one decimal, customer interruptions whole, range to nearest 1,000, SAIFI to two decimals, inside the asking sentence | Pass |
| Identifiable answer shape, every cell downstream of the deep step | required | ranked list under a cap (shape 01 per card); ask-sheet in the design note shows every cell riding the deep step | Pass |
| Golden ZIP holds exactly the requested files | required | `golden/` holds exactly the two deliverables named in the prompt | Pass |
| Nothing LLM-generated, every golden reads as real | required | judge thread flagged no LLM-authored tells; realistic mess (cause-code recode, feeder rename, unit change, duplicate logging, job-closed vs crew-finished dates) | Pass |

## Gate G reconciliation
Thread: `mechanism: forecasting` (plus a `method_or_model_selection` layer for the exposure-metric and growth-fit choice), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`.
Design note / card: `stump_class` / guard answer files this as `decomposition_attribution` (the Gate G mechanism is "the assignment of a correctly recorded rise to its drivers: wind against corridor growth against corridor density"), `analyst_test` names the same naive ranking (TOT-02 etc., avoiding 5,770) the thread reproduced, `domain_test` names the same deciding quantity (vegetation SAIFI by feeder, modelled from tree-contact rates against storm exposure and the vegetation cycle).

This is a label mismatch, not a direction mismatch: the thread named `forecasting`/`method_or_model_selection` where the design note names `decomposition_attribution`, but both labels sit in the client's FINE-numbers, non-banned family, and both agree `surface_read_dependency: no` / the recent counts are genuine, correctly recorded history, never a defect to catch. The thread did not name the declared distractors (the schedule of rates, the tree notices register) as load-bearing or as the surface read carrying the task; it independently identified the same two files as unused distractors that the design note names, which is the healthy outcome (the distractor is not carrying the stump). The one substantive thing the thread under-covered relative to the design note is the second analytical judgment, the corridor-rate-vs-growth decomposition (SF-level: "a catch-up removes only the growth since trim") being load-bearing in its own right, not just a byproduct of the exposure-normalisation forecast; it folded this into "method selection" rather than treating it as its own decomposition step. This does not change the determinism or Gate G verdict (both readings land in `analytical_non_defect`, `surface_read_dependency: no`), so it is a reporting nuance, not a finding that predicts a send-back.

Gate H: thread's line, `domain: pass`, `layers: pass`, `decisive_step: analytical`, `chain: 6+ inferences, judgment: exposure-covariate selection and forward projection under a verified weather-regime difference`, `one_fact: none`, matches the design note's H1-H5 argument closely: same domain test, same two layers (cause-code recode / unit change / dedup as Layer 1; exposure-normalised Poisson fit with climatological-normal projection as Layer 2), same decisive-step classification (`analytical`), same chain length (design note counts 5 dependent inferences plus 2 modelling judgments; thread counts 6+ with judgment named), and the same one-fact test answer (no single sentence rescues it). No Gate H mismatch.

## Stump power (Gate F)
The thread assesses this as a genuine, non-trivial stump: a capable analyst who cleans the OMS log correctly, applies every counting rule, and ranks on recent tree-caused customer interruptions produces a clean, self-consistent, wrong answer, because nothing in the filed documents announces that the three recent years are a regional weather anomaly; discovering this requires pulling four independent ~20-year hourly weather records and testing an exposure metric against the vegetation record, which a strong model can plausibly skip since the obvious high-signal variable (already cause-coded) looks sufficient and passes its own internal checks. This matches the design note's own stump-power argument (the "reflex" and "back-test" sections of the Survivor anatomy: the easy route validates on its own terms, and the field's major-event-day treatment, which only removes the snow days, offers no warning). The design note's ladder additionally documents that the decisive construction is robust across 26 valid-looking rival constructions and 18 skip-a-step rungs, none of which reach more than 3 of the golden six, which is independent (author-side) evidence for the same stump-power conclusion the isolated thread reached blind.

## Findings, ranked
1. (Spec gate, FIX_NOW-level, metadata hygiene only) `metadata.json` names no distractors at all; it has no `distractors` field, though the ZIP-level content (confirmed independently by both the design note and the isolated judge thread) does carry two usable, unlabelled, unused distractors (`ridgeline_2027_schedule_of_rates.docx`, `tree_notices_register_2024-2026.xlsx`). This is an omission in the authoring record, not a change to what solvers see; it does not affect the analytic surface and can be closed by adding a `distractors` field to `metadata.json` outside the ZIP.
2. (Reporting nuance, no action required) The judge thread's Gate G mechanism label (`forecasting` / `method_or_model_selection`) differs from the design note's declared mechanism (`decomposition_attribution`), but both are non-banned, `surface_read_dependency: no` classifications and agree on every substantive fact (the naive six, the correct six, the totals, the margin). No send-back implication.
3. (Noted, non-decisive) `feeder_register_2026.xlsx`'s own ICP column totals 39,933 against the `icp_counts_by_feeder` file's 39,943 used for the SAIFI denominator; the programme terms (section 5) pin the ICPs at the latest month-end, which is the `icp_counts` file, so this is harmless cross-file mess that does not affect any committed answer. No action required.

## Next action for the author
Add a `distractors` field to `task13/metadata.json` naming `ridgeline_2027_schedule_of_rates.docx` and `tree_notices_register_2024-2026.xlsx` (outside the ZIP, as the spec requires); no other change is needed, and no re-judge or model rerun is required since nothing solvers see changes.
