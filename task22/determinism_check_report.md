# determinism-check report, task22, 2026-11-12

## Verdict
DETERMINISTIC (judge thread's call; see Findings #1 for why this verdict rests on an incomplete Gate A check)
**Disposition:** APPROVE, as returned by the judge thread, with a caveat the judge itself raised under Fix: the
final per-feeder MWh figures (R4 technical losses, R5 non-technical loss, R9 the sweep four) were not independently
rebuilt end to end. Given that caveat covers exactly the numbers the main recommendation and three of four
Supplementary asks turn on, this should be read as APPROVE-pending-verification, not a clean sign-off.
**Stumping type:** mechanism: method_or_model_selection (supporting: assembly_and_reconciliation, missingness_and_measurement), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The judge found every decisive definition and window pinned literally in a shipped file (`rfp_2026-14_revenue_protection_scope.pdf` A.2-A.3 for the NTL formula, population and window; `fy2027_budget_instructions_electric_fund.pdf` for the 2027 basis), and verified seven supporting mechanisms exactly against the data: the 7.75%/8.22% line-loss figures, the 2019 study's 4.83% APT-3 figure, the 0.745/0.660 large-load diversity ratios (recomputed directly), the APT-2 stuck-transducer run, the CHL-3 storm telemetry gap and its emergency-tie switching, and the shape (not the exact customer counts) of the April 21 2026 NTH-4/NTH-3 transfer. It did not independently recompute the technical-loss physics model or the final NTL MWh ranking (CHL-2 1,312 / APT-4 1,127 / CHL-3 715 / NTH-4 699 / NTH-3 502 / APT-3 458) against the 388,753-row historian, 364,954-row CIS extract and 219,001-row IDR file, calling this an "open verification item" rather than a defect, since nothing it did check contradicted the solution. The main recommendation (which four feeders) and Supplementary asks 1, 3 and 6 all turn on exactly that un-rebuilt figure set.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Line loss 7.75% (12mo-Sep2024) / 8.22% (12mo-Sep2026) | ask 4 | Yes, verbatim from `annual_line_loss_report_2019-2026.xlsx` | Yes |
| 2019 study APT-3 technical-loss % = 4.83% | Step 5 | Yes, Table 2 of `loss_evaluation_study_2019_hester.pdf` | Yes |
| Grow diversity ratio 0.745 | Step 8 | Yes, recomputed from `idr_large_power_interval` (547.77/735 kW) | Yes, exact |
| Cold-store diversity ratio 0.660 | Step 8 | Yes, recomputed from `idr_large_power_interval` (891.00/1,350 kW) | Yes, exact |
| CHL-3 storm telemetry gap window | Step 2 | Yes, `COMM FAIL` block Jan 23 22:00-Feb 3 06:00 in the historian | Yes, to the hour |
| APT-2 stuck transducer, August 2025 | Step 1 | Yes, 52 identical consecutive hours from Aug 18 2025 in the historian | Yes |
| April 21 2026 NTH-4/NTH-3 lateral transfer (the mechanism) | Step 3 | Yes, switching orders crosswalked to GIS devices | Yes, shape only |
| NTH-4 373/441 customers (the exact counts) | ask 2 | No, not walked through the 9,023-row service-point tree | Not checked |
| APT-3 technical losses 1,777.8 MWh / fourteen feeders 13,037.7 MWh | Critical Component 1 | No, not rebuilt end to end | Not checked |
| NTL ranking, all six named feeders (CHL-2 1,312 ... APT-3 458) | Final Recommendation, ask 3, Critical Component 1 | No, not rebuilt end to end | Not checked |
| 2027 connection peak demand (931.4 / 541.2 / 521.6 kW) | ask 5 | Partially (the diversity ratios feeding it, yes; the final kW figures themselves, not reconfirmed) | Partial |
| 2027 technical losses (APT-4 1,731.4 / APT-3 1,686.7 / fourteen 13,492.4 MWh) | ask 6 | No | Not checked |

## Competing answers that survived
None found by the judge beyond the three shortcut routes the solution itself stress-tests (today's-GIS feeder label, the storm gap averaged, the 2019 study's stale percentages), each of which the solution shows produces a different wrong four. No additional fork was raised. The fourth/fifth-place margin (NTH-4 699.4 MWh, band 624.4-774.4, vs NTH-3 501.8, band 426.8-576.8) does not overlap on the judge's reading, a thin-but-clean gap rather than a contested one — but this reading rests on the unverified final MWh figures above, not on an independent rebuild of the gap.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count / categories | 10+ usable files, 2+ categories | 22 files: 8 xlsx, 8 csv, 6 pdf (3 categories: spreadsheet, tabular text, document) | Pass |
| Large messy CSVs | 1 CSV 20,000+ rows, 1 CSV 10-20 printed pages | `cis_meter_reads` 364,954 rows, `historian_feeder_breakers` 388,753 rows, `bmpa_delivery_point_interval` 111,073 rows, `idr_large_power_interval` 219,001 rows (all 20k+); `oms_outage_events` 890 rows / 7 cols ≈ 18 printed pages | Pass |
| Distractors declared outside ZIP, unlabeled inside | 2+ named in metadata.json, none labeled in ZIP | 3 named: `oms_outage_events`, `bmpa_wholesale_rate_schedule_w1_2026.pdf`, `delmont_municipal_airport_daily` — none labeled in the ZIP per judge's hygiene pass | Pass |
| Distractors unused but relevant | each looks relevant, carries no result | outage events (grid reliability-adjacent), wholesale rate schedule (billing-adjacent), airport weather (load-driver-adjacent) — none appears in the Results chain's "Pinned by" column | Pass |
| Deliverables | 1-3, all present in golden, no format family required | 2 requested (spreadsheet, PDF memo), both present in `golden/` as `dpl_feeder_energy_balance_2023-10_2026-09.xlsx` and `revenue_protection_2027_memo.pdf` | Pass |
| Asks multi-dimensional, unit stated, no rounding instruction in prompt | per spec | `prompt.txt` has no rounding instruction; submission.md's Supplementary Questions state MWh/kW/per cent/points units and bands throughout | Pass |
| Answer shape | one of fourteen | a reconciled table / bridge (the energy balance reconciling two totals, with the line-loss bridge on top); 9 checkable results (R1-R9) in the design note | Pass |
| Golden ZIP contents | exactly the requested files/formats | 2 files, matching the prompt's spreadsheet + one-page PDF memo | Pass |
| Not LLM-looking, real work product | per spec | judge's hygiene pass: PASS, no LLM-authorship tell found, no benchmark/authoring disclosure | Pass |

## Gate G reconciliation
Judge: mechanism `method_or_model_selection` (primary), `assembly_and_reconciliation` and `missingness_and_measurement` as supporting layers; `stumping_family: analytical_non_defect`; `surface_read_dependency: no`; `sole_data_defect: no`.

Design note: the Results chain's hurried-analyst failures are dismissed own evidence (R1, R2, R8), method shortcut (R4, R7), stopped at the first story (R6), unfinished chain (R5, R9) — no rule_application, no data_semantics, no planted defect anywhere in the chain, and the note's own Gate-G-adjacent language ("no decoy... no replay... not rule application... not semantics") matches the judge's `surface_read_dependency: no` finding. No reconciliation gap on Gate G; the judge's classification lines up with the design note's own account of where the difficulty sits.

## Gate H reconciliation
Judge's Deep reasoning line: `domain: pass`, `layers: pass`, `results: 6 graded across 4+ areas`, `one_thing: none`, `effort: quick ~1-2 of 6, careful ~3-4 of 6, thorough 6 of 6`, `one_fact: "today's GIS reflects current topology; replay the switching log" rescues ~1 of 4 feeder-ranking swaps (roughly a quarter to a third of results)`.

Design note's own Effort test (computed by `effort.py` on `generator/effort.json`, the generator's own golden and hurried routes on the cut pack, not a solver): 9 results (R1-R9), quick ~0.5/9, careful ~1/9, thorough 9/9; largest single hint rescues 1/9; pair estimate 20.8.

Two findings worth the author's attention:

1. **Result count mismatch and a careful-pass gap that reads much higher than the note's table.** The judge counted 6 graded results where the design note's chain has 9 (R1-R9); more importantly the judge's own careful-but-hurried estimate (3-4 of 6, roughly 50-67 per cent) sits far above the note's careful-pass figure (1/9, about 11 per cent) and close to its thorough column (6 of 6 = 9 of 9 by the note's count). Per the Gate H reconciliation rule, this is exactly the pattern that predicts a send-back: "the thread's effort grades leave the quick pass at more than a third of the results, or the careful pass level with the thorough one." However, the judge's own effort grading here is not itself a rebuild of the hurried routes against the data (it inferred "right/missed" from which mechanisms it had traced, not from actually running the shortcut computations and checking they land on a different four), so this reading is lower-confidence than the note's `effort.py`-computed figures, which are arithmetic on the generator's own implementations, not an estimate. Flagging the discrepancy rather than treating the judge's effort line as authoritative over the note's.
2. **One-fact count is consistent.** Both the judge ("rescues about a quarter to a third of results") and the note ("rescues 1 of 9") agree the single best hint clears only one of the three deciding corrections (the switching-log replay), leaving the storm-gap rebuild and the technical-loss repositioning untouched. No H5 concern.

No `one_thing` finding: the judge's own derivation (`own_derivation.md`) independently traced three separately-grounded mechanisms (GIS-vintage technical-loss recompute, switching-log replay, storm-gap substation-balance fill), matching the note's "Not one thing" claim that three corrections each move a different one of the four feeders. No hidden factor the judge found was dismissed by the note as merely routine; the note's Hidden factor record marks each relevant factor's fix depth as "modelling" or "modelling (a network replay)," not "routine," consistent with the judge's own account of needing a genuine rebuild rather than a one-sentence fix. No distractor was named by the judge as carrying a result.

## Stump power (Gate F)
Judge: strong, citing the same three independently-grounded shortcuts the design note names (stale 2019 study percentage, today's-GIS feeder label, storm-gap averaging), each flipping one feeder in the final four. This matches the design note's own Frontier check (shallow path checks, forcing table) closely. No too-easy signal raised.

## Findings, ranked
1. **Process violation: the judge thread did not keep the mandatory derive-first order, and its own report says so.** It opened `graded_blocks.md` in the same tool batch that first listed `target/`, before writing an independent derivation, and explicitly discloses this at the top of both `verdict.md` and `own_derivation.md`. This is the exact failure mode the determinism-check contract calls out by name (a pass that has seen the committed answers cannot be surprised by a filed sentence). No second thread was spawned to correct this, per the no-retry guardrail, so the verdict below should be read with that caveat attached rather than treated as a from-scratch confirmation.
2. **Gate A is incomplete on the figures that matter most.** The judge verified every supporting mechanism (clocks, diversity ratios, telemetry gaps, switching-order dates) but did not rebuild the technical-loss physics model or the final NTL MWh ranking for any of the six named feeders — the exact numbers behind the Final Recommendation and Supplementary asks 1, 3 and 6. The judge's own Fix section flags this as the highest-value next step, specifically the 373/441 vs 438 NTH-4 customer-count dispute and the APT-3 1,777.8-vs-838.1 MWh technical-loss figure. Until one of these is independently rebuilt, the DETERMINISTIC verdict rests on "nothing contradicted it" rather than "it reproduces."
3. **Effort-grading discrepancy (see Gate H reconciliation above):** the judge's careful-pass estimate is much more generous than the note's `effort.py`-computed figure, though the judge's number is a qualitative read, not a rebuild, so it is reported as a flag, not a correction to the note.
4. Spec gates, Gate G and the rest of Gate H all reconcile cleanly against the design note and metadata.json; no finding there.

## Next action for the author
Before treating this as a clean APPROVE, independently rebuild one of the two figures the judge left unverified: either the APT-3 technical-loss recompute (1,777.8 MWh vs the 2019 study's 838.1) from the GIS segments and `distribution_engineering_tables.xlsx`, or the NTH-4/NTH-3 customer-count walk (373/441 vs today's-GIS 438) through the service-point tree via the crosswalk. If both reproduce, the APPROVE stands on firmer ground than the current pass gives it; if either does not, re-invoke `/fix-determinism` on the specific finding rather than re-running this check from scratch.
