# determinism-check report, task10, 2026-11-10 (pass r3, final cut)

## Verdict
DETERMINISTIC (no SOLUTION_WRONG remains after the prescribed solution-side edits)
**Disposition:** FIX_NOW at the time of the judged verdict (solution-side only); the fix has since been applied, so the build is clear to proceed with no model rerun.
**Stumping type:** mechanism: method_or_model_selection (with decomposition_attribution for the rebound and forecasting for the backtest), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Judged: thread r3, /tmp/determinism-check-task10-r3/verdict.md, on target.zip sha256 1ee96fa6. Order statement: the thread kept the order (own_derivation.md written from the bundle alone, graded_blocks.md opened only afterwards). I did not spawn it: this runtime has no Agent tool, so the main session spawned it from my r2 brief with refreshed paths.

Applied after the verdict, exactly as its Fix section prescribes, no golden figure moved: nine-days-in-ten bands widened (Ashcombe Road 26.1 to 27.0, Charlecote Way 21.3 to 22.2, Fenwick Street 30.7 to 31.8, Hartwell Common 20.1 to 21.1); backtest band 0.10 to 0.29; a sentence in Supplementary 5 that Ashcombe Road's level is that of the half-hour to 20:00; a sentence in Step 9 that Fenwick Street's call needs the scatter carried in proportion; "the mean of the absolute misses" in Supplementary 7. The final cut is target.zip sha256 d84ca1b2 (verified), which differs from the judged 1ee96fa6 only in control_room_switching_log_2023-2026.csv (references in time order, ammeter readings, two holiday reasons), which no figure reads. I could not re-run the thread on the final cut and did not diff the two zips myself; that rests on the coordinator's statement.

## Why
The call is forced by the files read literally: guideline WPN-NP-G-014 (sections 2 to 7, Appendix A firm capacity), the award notice (contracted MW, 16:00 to 19:30 window) and the SCADA, dispatch, weather, register and growth files. An independent derivation reached the same set: reinforce Ashcombe Road, Fenwick Street and Hartwell Common; Charlecote Way stays inside firm (about 21.7 against 22.5). Every central figure reproduced inside its band. The one soft spot was band width on the nine-days-in-ten level, because a gross-residual treatment of the scatter lands 0.1 to 0.4 MW higher than the golden; that is what the widening closed.

## Recomputation ledger (r3 thread)
| Figure | Claimed (band at judgement) | Judge recomputed | Reproduced |
|---|---|---|---|
| Demand before flexibility, Ashcombe / Charlecote / Fenwick / Hartwell (MW) | 30.1 / 24.9 / 35.5 / 22.9 (plus or minus 0.3) | 30.3 / 24.9 / 35.6 / 23.0 | yes, all four |
| Delivered 17:30 to 18:00 (MW) | 8.1 / 4.0 / 5.4 / 2.9 | 8.1 / 3.9 / 5.2 / 2.8 | yes, all four |
| Off the peak (MW) | 4.2 / 4.0 / 5.4 / 2.9 | 4.3 / 3.9 / 5.2 / 2.8 | yes, all four |
| Expected peak with flexibility (MW) | 25.9 / 20.8 / 30.1 / 20.0 | 26.1 / 21.0 / 30.3 / 20.2 | yes, all four |
| Nine days in ten (MW) | 26.5 / 21.7 / 31.2 / 20.6 | gross-residual version: Fenwick 31.6, Hartwell 21.0; Charlecote 21.7 to 21.8; Ashcombe 20:00 recomputation not rerun | yes after widening (old Hartwell and Fenwick bands were 0.1 to 0.2 tight) |
| Backtest mean miss (MW) | 0.19 | 0.20 (0.22 without temperature term, 0.28 full calls only, 0.58 delivered equals scheduled) | yes (band now 0.10 to 0.29) |
| Cold-day delivery share at minus 3 C | 0.39 Corvane / 0.54 Quillon | 0.376 to 0.387 / 0.522 to 0.524 | yes |
| Rebound, first half-hour | 0.32 / 0.26 | 0.34 to 0.37 / 0.29 to 0.33 | yes within stated bands (Corvane at the top edge) |
| Scatter | about 16 per cent (12 to 22) | 13 to 23 per cent by zone | yes |
| Peak half-hour | ending 18:00 | ends 18:00 on 447 of 450 days at every zone primary | yes |

## Competing answers that survived
None changes the committed set. Forks the three threads ran, with the answer each gives:

r3 thread
1. Weather day by hours ending 01:00 to 24:00 versus end date equal to the day: demand moves 0.05 MW or less. Inside bands.
2. Cancelled or superseded instruction counted as a scheduled day versus final live only: demand 30.08 versus 30.32, 24.84 versus 24.89, 35.43 versus 35.58, 22.88 versus 23.00. Inside bands (the filed guideline is literally silent here; absorbed by the band).
3. Switching-day exclusion off: Ashcombe 30.32 to 30.49, the others unchanged. Marginal, 0.09 over the old top of band 30.4.
4. Growth by planned versus energised date: identical sets.
5. Hurried all-days regression with no exclusions: 27.0 / 22.8 / 32.6 / 21.2 MW. Wrong method, ruled out by the bands.
6. Delivery as a share of scheduled MW: Ashcombe 10.3 MW and peak 19.8 MW, Ashcombe left out; ruled out by data (delivery stops at a cold-dependent share of the contract, scheduling more delivers no more).
7. Scatter: point-estimate delivery gives Fenwick 30.3 to 30.5 (not committed); absolute scatter carried unchanged gives Fenwick under 30.4 (not committed); proportional gives 31.2 (committed). Proportional is data-pinned: sd of delivery in MW rises with contract size (Fenwick 0.25, 0.37, 0.56 MW across 2.5, 3.5, 4.5 MW contracts; Hartwell 0.15, 0.16, 0.31).
8. Backtest fits: 0.20 with temperature term, 0.22 without, 0.28 on full calls only (3 full calls at Ashcombe, thin), 0.58 delivered equals scheduled. Covered by the new band.

r2 thread (pack before the guideline section 6 rewording)
1. What flexibility credited means. The guideline as then worded read literally (only the half-hours ending 17:30 and 18:00 credited) puts the peaks at 29.1 / 24.3 / 34.4 / 22.1 MW and Charlecote Way needs reinforcement, so the call changes from three zones to four. The golden reading (whole window, load back after) gives three. This was the one reading that moves the headline and was closed by data, not by a filed sentence; the generator then reworded guideline section 6 so the service is delivered through its window. The r3 thread found no such fork on the reworded pack.
2. Fenwick scatter proportional (31.2) versus unchanged (30.4): same answer as r3 fork 7.
3. Ashcombe delivered at 2.8 times the largest contract seen: share of contract versus absolute plateau (about 3 MW). Pooled fit favours share of contract (rmse 0.228 against 0.282). The plateau moves figures but not the call.
4. Weather correction: straight line 26.6 / 23.4 / 33.3 / 20.8 corrected; quadratic on mild days 26.0 / 22.6 / 32.4 / 20.3 (unstable, ruled out by the rebuilt cold days). The note says two more rival fits were added to the band family after r2.
5 to 8. Cancelled days (0.04 to 0.22 MW), GMT day labelling (under 0.07 C), register handling, backtest scope (0.20 to 0.26): all inside bands.

r1 thread (brief carried the graded blocks inline, so weaker evidence on Gate C; older answers)
Coverage-count band (37 of 50) failed three of four cold-cut or transfer-day variants (34, 29, 45, 33); a quadratic demand fit landed below the band. Those blocks were replaced; the final blocks no longer carry a coverage count.

## Spec gates (final bundle, fresh unzip at /tmp/determinism-check-task10-final/target/)
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Usable files | 10 or more | 12 | yes |
| File categories | 2 or more | spreadsheet (4 CSV, 5 xlsx) and text (3 PDF) | yes |
| Large CSV | 20,000 rows or more | primary_demand_halfhourly: 196,213 rows, 10.3 MB | yes |
| Second large messy CSV, 10 to 20 printed pages | present | flexibility_events: 697 rows, 86 KB (r2 thread estimated about 15 pages); weather also 13,372 rows | yes (page count is an estimate, not printed) |
| Distractors in metadata.json | 2 or more, none labelled in the ZIP | 3: customer_interruptions, primary_transformer_condition, duos_charging_statement; file names carry no label | yes |
| Distractors unused yet relevant | unused by solution | thread found nothing in them needed; none answers a graded quantity | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, pptx); golden.zip holds exactly those two | yes |
| Asks multi-dimensional, unit and rounding stated | yes | per-zone rows across five figures, a bridge, a backtest; prompt gives MW to one decimal and the miss to two | yes |
| Answer shape | identifiable, many gradable cells | zone grid plus bridge plus backtest | yes |
| Reads as real, not LLM generated | yes | thread found business-realistic process-made mess, no authoring leakage, dates coherent; metadata.json lists all files as constructed (CC0), outside the ZIP | yes |

Prompt is one paragraph of 734 characters with no em dashes. Hygiene (thread): PASS, no exclusion-level finding.

## Gate G reconciliation
Thread: `mechanism: method_or_model_selection; stumping_family: analytical_non_defect; surface_read_dependency: no; sole_data_defect: no`. The design note's Deep reasoning section frames the same thing as a forecast with method shortcut, unfinished chain and uncertainty failures on honest numbers, and says it is not semantics and not rule application (the guideline files only the WHAT). These agree in substance (the thread leads with method selection, the note with forecasting); neither is a surface-read rejection. The declared distractors are not named as the surface read carrying the task. The thread's remark that the golden is not earned by the textbook route: the demand step and the backtest are earned by a careful run, so pricing sits on the delivery block, which matches the note's own R1 and R3 "earned" cells.

## Gate H line
Thread: `domain: pass | layers: pass | results: 9 graded across 6 areas | one_thing: none | effort: quick 2, careful 5, thorough 9 of 9 | one_fact: "delivery is a temperature-dependent share of the contract, not of what was scheduled" rescues about 2 to 3 of 9`.
Note: one fact ("a provider can deliver no more than a share of its contracted megawatts on a cold evening, however many are scheduled") rescues 2 of 11 results (R2a and R2); the come-back sentence rescues R4a alone and the spread sentence R6a alone. Effort test in the note: quick 10.9, careful 38.4, thorough 100 (effort.py). Comparison: the two one_fact counts agree (2 to 3 against 2, both about a quarter or less, under the third bound). The thread counts 9 results and the note 11, and the thread's careful 5 of 9 is a judgment call, not an effort.py figure; the note's careful pass scores lower. The thread's wrong figure for the hurried run: Ashcombe Road at about 19.8 MW expected peak, or 8.1 MW delivered read straight as 8.1 off the peak. Note: the r2 thread rated the same sentence at about 4 of 8, borderline, on the pre-fix blocks.

## Stump power (Gate F)
Real and spread across delivery, off-peak, expected peak, nine-in-ten and the bridge. The delivery pattern shows in every zone and winter and needs modelling because scheduling and cold are collinear, so it is not a shallow hidden factor. The rebound only changes Ashcombe Road's peak and the scatter scaling decides Fenwick Street; they are separate steps. Weak spots: the demand step and the backtest are earned by a careful run, and the textbook-route points count as Right in the careful column.

## Findings, ranked
1. Nine-in-ten bands were 0.1 to 0.4 MW tight against a gross-residual rival (fixed by widening).
2. Fenwick Street's commit rests on proportional scatter (expected 30.1 to 30.3 against firm 30.5); the other two scatter readings leave it uncommitted. It is data-pinned (sd in MW rises with contract size) and now stated in Step 9.
3. Guideline is literally silent on whether a cancelled instruction counts as a scheduled day; absorbed by the band (up to 0.24 MW).
4. Switching-day exclusion on Ashcombe sits 0.09 over the old band top.
5. The Ashcombe 20:00 recomputation was not rerun by the r3 thread.

## Residual risk, plain words
- Fenwick Street is the fragile call: committed only because the scatter is carried in proportion to the contract. A platform run that carries the record's absolute scatter will leave it out and will still be a defensible-looking run, though the data (sd rising with contract size) argues against it.
- Ashcombe Road's delivered MW is an extrapolation to a contract 2.8 times the largest seen; an absolute-plateau reading gives about 3 MW. The call still holds, but the delivered, off-peak and level cells would be lost by a solver taking that route.
- The final cut and the widened blocks were not themselves re-judged: the r3 verdict covers the pre-widening blocks and the 1ee96fa6 pack. The edits are the thread's own prescription and the zip difference is a file no figure reads, but that is a reasoned assumption, not a measurement.
- Charlecote Way's margin is about 0.7 to 0.8 MW inside firm; thin but clean.
- The page count of the dispatch log is an estimate from row count, not a print.
- I could not confirm that the r1 and r2 pack hashes; r1 and r2 verdicts do not record them. r3 judged 1ee96fa6; the final cut is d84ca1b2.

## Pass history
| Pass | Pack | Verdict | Disposition | Notes |
|---|---|---|---|---|
| r1 | earlier pack (hash not recorded) | DETERMINISTIC, SOLUTION_WRONG on the coverage count | FIX_NOW | brief carried the blocks inline; coverage band and quadratic rival outside bands |
| r2 | rebuilt pack (hash not recorded) | DETERMINISTIC, SOLUTION_WRONG (wording, bands) | FIX_NOW | guideline section 6 reading risk (Charlecote Way flips to reinforce under the two-half-hour reading); component 1 band and Charlecote rounding |
| r3 | 1ee96fa6 | DETERMINISTIC | FIX_NOW (solution side only) | bands and sentences, applied; no golden figure moved |
| final cut | d84ca1b2 | not re-judged | n/a | differs only in switching log presentation |

## Next action for the author
Proceed to stage 5: run the free gates once on the d84ca1b2 cut and the widened submission.md, and note in the platform triage that a run which leaves Fenwick Street out has carried the scatter unchanged.
