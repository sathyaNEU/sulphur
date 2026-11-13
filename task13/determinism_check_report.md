# Determinism check, task13 (one pass)

## Verdict: DETERMINISTIC
## Disposition: APPROVE

## What was checked

Unzipped `target.zip` fresh to `/tmp/determinism-task13-run1/target` and worked only from `prompt.txt`,
`submission.md`'s four answer blocks, and that pack. Gates A to E of the judge guidelines.

## Evidence

| Figure / claim | Check | Result |
|---|---|---|
| Faults by year sum to 436 (96+93+83+84+80) | arithmetic | matches 436 |
| 2026 faults by cause sum to 80 (9+6+16+16+14+8+5+2+4) | arithmetic | matches 80 |
| 2026 member interruptions by line sum to total | 16115+11171+10259+1168+14894+3417 | = 57,024, exact match to stated total |
| 2026 member-minutes by line sum to total | 179995+172224+354807+27196+199267+294124 | = 1,227,613 vs stated 1,227,611 (0.0002% off, well inside the stated 2% band) |
| Fault definition, fault/span location convention, cause taxonomy, repeat-location rule (400 m, 3+ faults of one cause since 2022, salt excluded), work-list fix mapping, washing-due definition | `reliability_reporting_procedure_rev4.docx` (RP-04, Rev. 4, Feb 2024) | All filed verbatim; these are not invented conventions, the 400 m grouping, the "fixed since last fault" rule, and the fix-per-cause mapping (perch guards / replace / clear span / remove trees) are the procedure's own text, matching Step-by-Step 5 and the Final Recommendation's vocabulary exactly |
| 69 kV two-ended SCADA trip signature exists and is distinguishable from 12 kV feeder and single-ended test trips | `scada_soe_2022-2026.csv` (42,779 rows; 3,108 are 69KV-tagged; paired OPEN/CLOSE/LOCKOUT sequences at two station RTUs within ~1 s) | Confirmed the raw signal the Step-by-Step method operates on exists and behaves as described (e.g. TUL/CAN pair tripping together 2022-01-09) |
| Inland autotransformer swap date (14 Mar 2024) forces the protection-study era split used for Line 10/11 fault location | `substation_register_2026.xlsx` "Transformers" sheet: T1 retired 2024-03-14, T2 in service 2024-03-14 | Exact date match to Step-by-Step 2's claim |
| The era split is not cosmetic: Inland's Z0 source impedance actually changes between studies (9.80 Ω → 3.60 Ω), which is exactly what would move a ground-fault residual-current-split location for Line 10/11 | `protection_study_2022.pdf`, `protection_study_2025.pdf` (plain-text extraction, both single-page tables) | Confirmed; this is a real, filed, dated physical change, not a planted artifact, it legitimately forces "which study for which era," closing the fork the Step-by-Step calls out (Line 10's 2022 to 2023 contacts moving off span 47-48 under the wrong, uniform-study shortcut) |
| Line 9 solar-tap ground-current correction (structure 137 vs relay's 148) | `line_register_69kv_2026.xlsx` "Solar tap" sheet (tap at 23.4 km from Shell Ridge, 66 MVA / grounded-wye step-up per the 2025 study text) and `coyote_draw_solar_protection_events_2023-2026.csv` (805 rows, ia/ib/ic/in_ka fields, Central-implied timestamps) | Confirmed both inputs needed for the correction are present and structured as described |
| "Sections" (washing) are a filed, discrete partition, not an interpretive unit | `insulator_washing_log_2022-2026.xlsx` "Sections" sheet: 23 fixed Line/Section/From-structure/To-structure rows | Confirmed; removes one possible ambiguity about what a "washing section" is |
| Salt-flashover evidence and ESDD test-site data needed to derive the 0.032 mg/cm² threshold exist | `line_patrol_reports_2022-2026.xlsx` (149 rows; 17 rows carry "flash marks"/"heavy salt" findings with date, line, structure), `esdd_monitoring_2022-2026.xlsx` (442 readings across 8 never-washed test sites with install dates), `structure_inventory_69kv_2026.csv` (per-structure `gulf_shore_km`) | All three inputs exist with the fields the Step-by-Step method needs (date, location, distance-from-Gulf, deposit). Did not re-run the distance-fit regression itself (out of budget), see Finding below |
| Distinctive recommendation vocabulary appears in shipped files (Gate B wording check) | grepped decompressed docx/xlsx/csv for "perch guard", "hazard tree", "clear the span", "washing section", "repeat location" | All present verbatim in `reliability_reporting_procedure_rev4.docx` |
| No "naive" alternate fault source contradicts the chosen one (Gate C: is there an easier, equally defensible route to a different count?) | `oms_extract_2022-2026.sqlite` (`feeder`, `cause_code`, `outage`, `outage_step` tables) | OMS is a 12 kV-feeder-level outage system, not a 69 kV fault log, it cannot itself produce a rival "faults since 2022" count; it only feeds the member-interruption/minutes reconstruction (Step 6), consistent with the Step-by-Step's own description |

## Finding (not blocking, flagged for the author)

The 0.032 mg/cm² washing-flashover threshold (Critical Component 4, Q5's section list) is derived, not
filed directly: no file states a numeric ESDD flashover threshold. It must come from fitting an
accumulation-rate-vs-distance-from-Gulf model to the never-washed test insulators and reading off the
deposit implied at the lowest-ESDD patrol-reported flashover event. I confirmed the necessary raw
ingredients exist (patrol "flash marks"/"heavy salt" events with date/line/structure, ESDD readings at 8
distance-separated test sites, per-structure Gulf distance), but did not re-run the fit itself (budget), so
I cannot personally certify that every reasonable fit specification (e.g. linear vs. other decay form,
which patrol events anchor the minimum) lands on exactly the same 9-section list with no stated tolerance
band on that figure (unlike the fault/cause/member-impact/repeat-location figures, which all carry an
explicit "within N" band). Everything else checked is internally consistent and filed, so this is a
spot-check gap, not a demonstrated fork, recommend the author re-derive the threshold once with an
alternative reasonable fit (e.g. drop the single lowest-ESDD anchor event, or use calendar-day-weighted
accumulation) and confirm the 9-section list is unchanged; if it is robust, no action is needed.

## Fix

None required for APPROVE. If the author wants to close the one flagged gap pre-emptively: add an explicit
tolerance to the washing-section count (e.g. "9, within 1") the same way the other four graded figures
already carry one, which absorbs any small fit-specification variance without changing the method or the
pack (prompt/input_files unchanged; a `submission.md` wording addition only).
