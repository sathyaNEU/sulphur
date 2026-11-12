# determinism-check report, task4, 2026-11-11

Architecture 12 (Havørn Regional's 2027 rotable spares plan, watch-list withdrawals). This pass runs at /build
stage 4, licensed by the author. It supersedes every earlier architecture's report on file (the architecture-10-era
and architecture-11 reports, `determinism_check_report_pass3.md` through the prior `determinism_check_report.md`,
left untouched as history of a different slot's run) with the current cut's own report.

## Verdict
**DETERMINISTIC**
**Disposition:** APPROVE
**Stumping type:** mechanism: forecasting (plus method_or_model_selection on the Bodø queue and causal attribution
on the watch list), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The isolated judge thread derived its own answer from `target/` alone before opening the graded blocks (order of
work confirmed, `own_derivation.md` written first), then recomputed every load-bearing figure in the solution. The
main recommendation and every supplementary answer are forced from the shipped files: the reliability report's own
per-flight-hour "2027 outlook" (41/36/34 for starter-generator/brake/bleed valve) reproduces exactly from
`component_changes_2023-01_2026-11.csv` once two real grain issues are resolved (installation-completion rows with
a null `serial_off` are not a second removal; one literal duplicate row for 822-1123-002), but it is rejected by a
mechanism the files do not state anywhere: these three parts wear by landings and engine starts, not flight hours,
which the judge itself re-derived from `flight_legs_2023-01_2026-11.csv` and `fleet_register.xlsx` by comparing
removal rates per 1,000 cycles against per 1,000 flight hours across the fleet's four existing bases (which already
differ 0.29 to 1.05 hours per cycle). `flying_programme_2027.xlsx` independently gives 2027 cycles +18.5% against
flight hours -13.1%, matching the solution's "landings 19 per cent up, flight hours 13 per cent down" exactly. This
is the client's permitted forecasting shape (a correctly-read past that a genuine regime change, the Helgeland
routes, does not pin), not a catch-the-wrong-number stump. The Bodø shop queue sizing (R6/R8), the SB 61-0042
propeller-control forecast (R4) and the watch-list serial-vs-position attribution (R3/R3b) all independently
reproduced from their own files.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Trailing-12mo cycles (Nov 2025-Oct 2026) | 60,830 (implicit basis) | 60,830 | Yes, exact |
| Trailing-12mo flight hours | 28,810 (report basis) | 28,685 | Yes, within ~0.3-0.8%/month, immaterial |
| Per-part removal counts / MTBUR, Oct 2026 report | as in `reliability_report_2026-10.pdf` | matched exactly after dedup of one duplicate row and exclusion of "fitted, unit awaited" install-completion rows | Yes, exact once two grain fixes applied |
| 2027 cycles vs trailing | +19% | +18.5% from `flying_programme_2027.xlsx` | Yes |
| 2027 flight hours vs trailing | -13% | -13.1% | Yes |
| Starter-generator / brake 2027 removals | 59 / 51 | ≈56 / ≈50 by a simple ratio-scaled cycle forecast (golden uses a fitted model, inside band 55-66 / 49-55) | Yes, within band |
| SB 61-0042 bulletin incorporation | ~75% of installed units at snapshot | ~78% from `rotable_stores_snapshot_2026-11-30.xlsx`'s SB column on 816534-3 | Yes, consistent |
| Bodø shop 2027 summer queue | ~29 days (Jul-Aug) vs 13 (2026 avg) | seasonal pattern confirmed in `bodo_shop_work_orders_2023-2026.csv` + `bodo_shop_roster_2023-2026.csv` (worst observed ~9 days in Aug 2025, consistent direction) | Yes, directionally; exact replay not independently re-run to the day |
| Figure consistency across FINAL_RECOMMENDATION / CRITICAL_COMPONENTS / SUPPLEMENTARY_ANSWERS | - | no disagreement found on any cross-checked figure | Yes |

## Competing answers that survived
None disqualifying. One watch item (not a Gate C failure): the "8 of 23" watch-list withdrawal split depends on a
shrinkage/credibility estimate of each sparse serial's own removal rate (3-5 removals each) that no shipped file
specifies a method for. The judge could not, in its time budget, build a rival shrinkage estimator and show it
moves a borderline serial across the design note's 1.5-removals/year threshold, so this is reported as the single
place in the chain most likely to admit a reasonable alternative statistical choice, not as a demonstrated fork.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count / categories | 10+ usable files, 2+ categories | 13 files: 6 CSV, 4 xlsx, 3 PDF (spreadsheet, tabular/text, document categories) | Pass |
| Large messy CSVs | one 20,000+ rows, one 10-20 printed pages | `flight_legs_2023-01_2026-11.csv` 240,432 rows; `bodo_shop_work_orders_2023-2026.csv` (1,633 rows x 12 cols) and `component_changes_2023-01_2026-11.csv` (1,692 rows x 14 cols) both estimate to roughly 17-20 printed pages at typical wide-table density | Pass (page count is an estimate, not a rendered print) |
| metadata.json distractors | 2+ named, none labelled inside the ZIP | `engine_trend_monitoring_2025-2026.csv`, `pool_support_offer_2026.pdf`; neither is named as a distractor anywhere inside `target/` | Pass |
| Distractor relevance/use | unused yet relevant; one reproduces a graded quantity and a shipped fact rules it out | `pool_support_offer_2026.pdf` is a live-looking third-party pool-access cost sheet covering 13 of the 16 part numbers (plausible as a buy-vs-pool alternative) that the prompt's fill-rate/spares-holding ask does not call for; `engine_trend_monitoring_2025-2026.csv` is engine ITT/torque trend data with no tie to any of the 16 rotable part numbers. Both confirmed unused by the judge's own derivation. The stronger "arithmetically reproduces a graded figure" sub-clause was not independently verified against `pool_support_offer_2026.pdf`'s fee table within this pass's budget | Pass, with one unverified sub-clause |
| Deliverables | 1-3, all present in golden, no format family required | 2 requested (xlsx, pptx); `golden.zip` holds exactly `havorn_rotable_spares_2027.xlsx` and `havorn_rotable_spares_2027.pptx`, nothing else | Pass |
| Asks multi-dimensional, unit stated, no rounding in prompt | - | 16-part-number table with removals/ranges/spares-needed/change per ask 1-3; slide asks 4-6 name buy/cut lines, watch-list savings and serials; prompt names no rounding | Pass |
| Answer shape, 4+ checkable results | one of 14 shapes, 4+ independently checkable | buy/cut/hold allocation with its sensitivity (fill-rate sizing) plus a forecast with bands; design note's chain carries 9 results (R2-R9) across 6 areas, judge independently confirmed ~6 distinctly graded results | Pass |
| Golden ZIP contents | exactly the requested files | `havorn_rotable_spares_2027.xlsx`, `havorn_rotable_spares_2027.pptx`, nothing else | Pass |
| Realism / no LLM tells | - | judge's hygiene check: PASS, genuine MRO/engineering artifacts, schema drift, duplicate row, mixed reason-code eras; no LLM authorship tells, no benchmark/authoring disclosure, no public-data contamination (fictional carrier) | Pass |

## Gate G reconciliation
Judge: `mechanism: forecasting` (+ `method_or_model_selection`, causal attribution on the watch list),
`stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`.
Design note's `## Frontier check`: precedents cited for every careful-column loss (R2 N04/N01, R3 L03/L13, R3b L14,
R5 L12/L36, R6 L15/L16, R7 L35, R8/R9 L11); `Shallow path checks:` names the per-flight-hour outlook's own
back-test and the refuting cross-base panel fit, Palm-on-average's own 2026 fit and the refuting shop replay, and
the confirmed-failure-only watch list's own check and the refuting runs-of-serviceable-removals test;
`Assumption made false:` the flight-hour scaling assumption and the 2026-turnaround assumption, both tested from a
named file; `Forcing:` the buy/cut lines hold across all seven golden-family members and across every fitted input
moved by its spread; `Noun swap:` task20 architecture 1, severity none. These line up with the judge's own
`mechanism`/`stumping_family` line: the judge reached forecasting and honest-data method/attribution selection
independently, with no surface-read-rejection core, matching the note's claim that the per-flight-hour and
average-turnaround readings are rejected by named data, not by a planted defect.

## Stump power (Gate F)
Judge: stump power "high and spread across several independent moves" (the flight-hour-vs-landings transfer, the
average-turnaround-vs-replay choice, the pooled-vs-split SB 61-0042 cohort, the watch list's raw counts vs.
serial-driven attribution), "no single one of these, caught alone, fixes the whole deliverable."

Design note's `## Effort test`: quick 1 of 9, careful-but-hurried 3 of 9, thorough 9 of 9; pair estimate 40.6
(quick 20.8, thorough 100); largest single hint rescues 1 of 9 (R2 alone), and even then leaves the in-house spares
at 0 of 5 lines in band on the careful pass.

Judge's own Gate H line: `effort: quick ~2 of 6, careful-but-hurried ~3-4 of 6, thorough 6 of 6`; `one_fact: "use
2027 landings, not flight hours" rescues about 2 of 6`.

**Reconciliation finding (the one worth the author's attention):** the judge's own unprompted derivation reached
the landings-vs-flight-hours mechanism (R2) through a single cross-base rate comparison (cycles vs. flight hours
per 1,000, across the fleet's four existing bases) and then recovered 2027 removals for starter-generator and brake
with a simple ratio-scaled forecast that landed inside the golden's band (≈56 and ≈50 against 55-66 and 49-55) on
its own first pass, without reproducing the design note's full cross-base log-likelihood model selection. The
design note's `## Effort test` grades R2 Missed for both the quick and the careful-but-hurried column, Right only
at the thorough column, on the view that identifying the driver requires the panel fit with the likelihood-ratio
comparison (2 dlogL 23.8/17.5/18.2). The judge's unprompted result suggests the mechanism itself (landings, not
hours, drive these three parts) is closer to "modelled on sight" (a cross-base ratio comparison, the kind of
one-look group-by the house's own cautions treat as earned by a careful pass) than to a result that needs the
full statistical fit to land in band. This nudges the judge's own quick/careful shares (~2/6 and ~3-4/6 of 6) above
the design note's 1/9 and 3/9 of 9 shares (note the different denominators: 6 distinctly-graded results the judge
could independently confirm vs. the note's full 9-row chain, which also carries R6/R8/R9 downstream of R2). The
quick-pass share (~2/6 = 33%) and the one-fact share (~2/6 = 33%) both sit right at, not clearly over, the
house's "about a third" ceiling, and the careful-but-hurried share stays clearly below the thorough column in both
tellings, so this is not a Gate H failure on its own. It is the single most useful lever if the task needs
hardening later: either tighten R2's band so a simple ratio-scaled forecast (once the driver is spotted) falls
outside it, or make the driver identification itself require crossing more than one base's worth of evidence
before it resolves.

No `one_thing` finding: the judge's H line is `one_thing: none`, consistent with the design note's hidden-factor
record (six constructed factors, all marked `keep`, none sitting only in the deciding units; every one found by a
plot/group-by, runs-of-serviceable-removals, a targeted query or a replay, i.e. modelling work, not a single-sentence
giveaway). No banned_stumping_type: the judge found no surface-read-rejection core; the per-flight-hour and
average-turnaround readings are rejected by data the files carry independently of the recommended methods, which is
the note's own framing in `Shallow path checks:`.

## Findings, ranked
1. (Medium, non-blocking) The landings-vs-flight-hours mechanism (R2) may be reachable by a careful-but-hurried
   solver via a single cross-base rate comparison plus a simple ratio-scaled forecast, which already lands inside
   the golden's band for starter-generator and brake. The design note's effort test currently grades this Missed at
   the careful-but-hurried column; the judge's independent, unprompted pass reached it there. See Gate G/H
   reconciliation above for the detail and the two hardening options.
2. (Low, watch item, not a fork) The watch-list "8 of 23" split depends on an unspecified shrinkage/credibility
   choice for each sparse serial. No rival estimator was shown to flip a serial in this pass; flag for one check
   the next time the build is touched.
3. (Low, hygiene) The "distractor arithmetically reproduces a graded figure" sub-clause of the spec's distractor
   gate was not independently re-verified against `pool_support_offer_2026.pdf`'s fee table in this pass; both
   distractors are confirmed unused and plausible, but this specific sub-clause is unconfirmed rather than failed.

## Next action for the author
None required to ship architecture 12 as-is (APPROVE stands). If the build is revisited before upload, the one
concrete step worth taking is re-running `effort.py`'s careful-but-hurried pass for R2 with a simple ratio-scaled
cross-base-rate forecast (no likelihood-ratio model fit) and checking whether it lands inside R2's stated band; if
it does, either widen R2's "hurried analyst's failure" classification to reflect that it is partly earned at the
careful-but-hurried level, or narrow the band so the ratio-scaled shortcut misses it, before the next platform
round.
