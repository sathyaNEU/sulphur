# determinism-check report, task4, 2026-11-09

## Verdict
**DETERMINISTIC**

**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection (secondary: binding_constraint on the 442 kWh / FES-2 threshold); stumping_family: analytical_non_defect; surface_read_dependency: no; sole_data_defect: no

## Why

The judge thread reproduced every load-bearing figure it could re-derive within a single-pass budget and found no committed answer contradicted by the shipped files. Pilot duty-day count (2334, after deduplicating 40 double-uploaded rows in `bev_daily_summary_2025-03_2026-10.csv` and joining to `tms_consignments_jonkoping_2025-2026.csv`), the shortlisted duties' routing-tool speeds (74.0-82.9 km/h against Critical Component 1's "74 to 83"), the pilot's actual-to-planned speed ratio (~0.912 year-round against the golden's 0.91, ~0.831 near -5C against the golden's 0.82), and the 540 to 520 to 442 kWh battery-arithmetic chain (quotation's 540 kWh usable, FES-2 2.3's first-year loss of 3.8 per cent giving 519.5 to 520, FES-2 4.3's 85 per cent giving 442.0) all reproduced from a specific named file. The one arithmetic point flagged for scrutiny in the spawn brief (the 520 kWh "coincidence" between the 2027 tractor's post-loss capacity and the pilot fleet's own smaller-battery usable capacity) resolved cleanly as two different battery models landing near the same rounded figure, not a conflation error. The main recommendation (order 6: V02, V05, V09, V14, V16, V18) and all fourteen duty verdicts are supported; the thread could not fully re-derive the multivariate energy-model coefficients to the kWh in its budget, but every order-determining lever it could check (speed ratio, battery arithmetic, duty-day count, weighbridge-vs-declared payload inflation by shipper) reproduced within the stated tolerances, and SOLUTION_STEPS' own documented forks (orders of 9, 8, 9 and 10 when any one of the four adjustments is dropped) are internally consistent with the design note's independently-recorded forks.

## Recomputation ledger

| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Pilot duty-days | 2334 | 2374 rows deduped (-40) joined to tms_consignments: 2334 | Yes, exact |
| Shortlisted duties' routing-tool speed | 74 to 83 km/h | 74.0-82.9 km/h | Yes |
| Pilot actual-to-planned ratio, year | 0.91 | ~0.912 | Yes |
| Pilot actual-to-planned ratio, -5 C | 0.82 | ~0.831 (binning-sensitive, matches the note's stated multi-window stress test) | Close, within the stated band |
| Battery chain: 540 to 520 to 442 kWh | 520 kWh usable, 442 kWh limit | 540x(1-0.038)=519.5 to 520; 520x0.85=442.0 | Yes, exact |
| First-year loss, 3.8 per cent | 3.8 (3.6 to 4.0) | Age-bucketed implied-capacity check shows ~4 per cent decline by month 11-12, consistent in order of magnitude; full age+cold regression not re-derived in the pass | Consistent, not fully re-derived |
| Weighbridge-vs-declared payload inflation | 1.2 on declarations, 2.1 kWh/t/100km calibrated | Shipper ratios from ~1.00 (BMJ/RPA/RTR/SKB/TTV) to ~1.06-1.07 (HIL/VGL/VIS/LBY/KCY/GDR/TEN); shipper_register_2026.xlsx confirms the needed shippers are served from both Jönköping and Värnamo | Yes, join licensed |
| Full energy-model coefficients (R3's fourteen design-day energies to the kWh) | see Assessment sheet | Order-determining levers checked; full multivariate refit not completed in the single pass | Not independently re-derived to the kWh; no contradiction found |

## Competing answers that survived

None. The thread enumerated the documented forks (no speed term -> 9; routing-tool speed taken at face value -> 3; year's mean ratio -> 5; declared payloads uncalibrated -> 8; single-rate cold form -> 9; no first-year battery loss -> 10) and found each is a genuine alternative a hurried-but-competent analyst could reach, but none is defensible as *the* answer once the files are read in full: FES-2 2.3 charges the first-year loss, FES-2 4.2 points to the weighed (not declared) planning load, the one-rate cold form fails its own January/February 2026 holdout, and the pilot's own record shows it never drives as fast as the routing tool promises. No fork survives as a rival to the committed 6-tractor order.

## Spec gates

| Gate | Required | Actual | Pass |
|---|---|---|---|
| Usable files | 10+ (system files, `__MACOSX`, empty placeholders excluded) | 12 files in `target.zip`, all usable | Pass |
| File categories | 2+ (spreadsheet, database, text, image, code; archives count by contents) | CSV x6, XLSX x4, PDF x2: spreadsheet + text/document categories, 3 formats | Pass |
| Large messy CSV, 20,000+ rows | 1 | `weighbridge_varnamo_2024-11_2026-10.csv`, 21,407 rows, used for payload calibration | Pass |
| Large messy CSV, 10-20 printed pages+ | 1 | `bev_daily_summary_2025-03_2026-10.csv` (2374 rows, duplicate-upload mess, used for R1/R3) and `fuel_card_statement_varnamo_2025-2026.csv` (9357 rows, ~150+ pages) both qualify; at least one (`bev_daily_summary`) is actually used by the solution | Pass |
| metadata.json names 2+ distractors, none labelled inside the ZIP | 2+ | `fuel_card_statement_varnamo_2025-2026.csv`, `workshop_log_2025-2026.csv`, named only in `metadata.json`; no label inside `target.zip` | Pass |
| Each distractor relevant, unused, and (at least one) a load-bearing-looking quantity ruled out by a shipped fact | required | Both are plausible BEV-fleet artifacts (diesel fuel purchases; a BEV service job log) that an analyst would open; neither visibly carries a computable alternative answer to a graded quantity that a shipped fact then overturns (e.g., no battery-health reading in the workshop log that tempts a wrong R2) | Partial -- a minor refinement, not blocking |
| 1-3 deliverables, all present in golden, no forced format family | required | `ev_duty_assessment_2027.xlsx` and `tractor_order_memo.pdf`, exactly the two requested; both present in `golden/` and `golden.zip` | Pass |
| Asks multi-dimensional with unit/rounding stated | required | Prompt states "nearest 10 kWh," "0.1 kWh," "0.1 per cent"; asks span 14 duties x multiple fields, not a stacked lookup | Pass |
| Answer shape, one of the fourteen | required | Allocation (6 tractors to 14 duties) plus its sensitivity (each shortcut's alternate order) -- a forecast-path/allocation-with-sensitivity shape | Pass |
| Golden ZIP holds exactly the requested files, in the requested formats | required | `golden.zip`: `ev_duty_assessment_2027.xlsx`, `tractor_order_memo.pdf` -- exactly 2 files, matching | Pass |
| Nothing LLM-shaped; goldens read as real work product | required | Judge's hygiene pass found no synthetic/benchmark disclosure; grepped zero hits for "synthetic"/"generated"/"benchmark" in the bundle | Pass |

## Gate G reconciliation

The judge's classification (`method_or_model_selection` + `binding_constraint`, `surface_read_dependency: no`, `sole_data_defect: no`) matches the design note's own strategy label, "WORKS IN FORM (a forecast carried to a population the fit never saw, through a covariate whose value for the new units is itself an estimate)," and its explicit "Not rule application" / "No decoy" / "No replay" lines (DESIGN_NOTE.md lines 30, 32-33). The note's Hidden factor record marks every constructed pattern (air-drag speed term, routing-tool optimism, shipper declaration error, the cold curve) as "modelling" fix depth and "no" for sitting only in the deciding units -- consistent with the judge finding no shallow hidden factor and no planted-defect flip. No reconciliation gap on Gate G.

## Gate H reconciliation

| Item | Judge thread | DESIGN_NOTE.md | Agreement |
|---|---|---|---|
| domain | pass | H1 domain test (a statistician's regression-and-extrapolation task; swap test fails for "community nurses") | Agree |
| layers | pass (messy data + genuine modeling named) | Layer 1 (re-uploads, dropouts, weight-format drift, re-keyed duty codes, etc.) and Layer 2 named explicitly | Agree |
| results / areas | >=6 graded across >=4 areas | Results chain lists R1-R5 across missingness-and-measurement, modeling, forecasting, synthesis (4 areas); Critical Components and supplementary asks add more gradable checkpoints | Agree, no discrepancy |
| one_thing | none | "Not one thing": four independent estimates each move the order on their own (speed 9/3/5, payload 8, cold 9, loss 10) | Agree |
| effort | quick ~1-2/14, careful ~6-9/14, thorough 14/14 | effort.py: quick 0.5/5, careful 2.5/5, thorough 5/5 (10%/50%/100%) | Structurally consistent (quick well under a third, careful clearly above quick and below thorough, thorough full); no "careful levels with thorough" flag |
| one_fact | the thread's candidate sentence ("the 2027 tractor's usable battery is reduced by the pilot fleet's own first-year loss before the 85% margin") rescues "at most ... roughly a third," i.e. up to ~1-2 of 5/6 results | effort.py's computed "Largest single hint" (the speed/air-drag sentence) rescues 0 of 5 | **Discrepancy, see Findings below** |

## Stump power (Gate F)

Strong. Four independently decisive adjustments (speed derating, payload calibration, cold-form holdout selection, first-year battery loss) each move the order on their own when dropped (9, 8, 9, 10 respectively against the golden's 6), matching the design note's own documented forks almost figure-for-figure. A careful-but-hurried run is likeliest to land on 8 or 9 tractors by using declared TMS weights or an undifferentiated/routing-tool speed, most likely misclassifying V03, V07, V11 or V30.

## Findings, ranked

1. **Minor, non-blocking: the judge's one-fact candidate differs from, and nominally rescues more than, the design note's computed "Largest single hint."** The note's `effort.py`-measured largest single hint (the speed/air-drag sentence) rescues 0 of 5 results; the judge thread, working without that tooling, proposed a different single sentence (about the battery-loss-before-margin order of operations) and estimated it could rescue "at most roughly a third" of results, by its own admission an informal estimate ("I was not able to fully rebuild the multivariate energy model... in the time available"). This is not a Gate H5 failure on the numbers the author already measured (0 of 5 is well under a third), and the judge's estimate is for a different sentence than the one `effort.py` found to be the single strongest -- it is reported here as a reconciliation note, not a send-back trigger, because the authoritative figure remains the note's own computed one. No action needed unless the author wants to re-verify that no single sentence beats the measured 0-of-5 hint.
2. **Minor, non-blocking: `metadata.json`'s `architecture` field (6) is stale against `pipeline.json`'s architecture 7.** This is bookkeeping outside the ZIP and does not touch any shipped file or graded answer; worth a one-line edit before the next status commit so the record matches the re-design the user describes.
3. **Minor, non-blocking: the two distractors are relevant but neither visibly produces a false-but-arithmetically-plausible answer to a graded quantity that a shipped fact then rules out** (the spec gate's stronger form: "one that answers a graded quantity reproduces arithmetically and a shipped fact rules it out"). `fuel_card_statement_varnamo_2025-2026.csv` and `workshop_log_2025-2026.csv` are both genuine, unused, on-topic fleet artifacts, which satisfies the baseline distractor requirement, but neither is a load-bearing decoy in the stronger sense. Not disqualifying on its own.

No finding reaches a gate failure. Verdict, Gate F, Gate G and Gate H all hold together between the judge thread's independent read and the design note's own construction record.

## Next action for the author

None required to ship. Optionally: (a) update `metadata.json`'s `architecture` field from 6 to 7 to match `pipeline.json` before the next status commit, and (b) if time allows before upload, have the generator confirm no single sentence beats the measured 0-of-5 "largest hint" (the judge's independent candidate suggests checking whether a battery-loss-ordering sentence could rescue more than `effort.py` currently credits it with).
