# Determinism check report: task3 (architecture 3)

Judge thread: isolated Sonnet at medium, 2026-11-08, on the bundle unzipped from target.zip and the submission's
graded blocks; the brief at /tmp/determinism-check-task3-107173/judge_brief.md.

- **Verdict:** DETERMINISTIC (the main call and answers 7, 8 and 9 reproduced: OW-S peaks 4.15, 5.95, 8.11 and 9.90
  ft; MS-MW 4.95 ft; DW-17 6.81 ft).
- **Disposition:** FIX_NOW, presentation and solution text only. Applied 2026-11-08: (1) the plate's "added October
  2026" caption was already removed in the generator; the judge read an earlier unzip, and the shipped target.zip
  carries the re-cut plate (sha 11e08aae19 against the judge's 4767f783c5); (2) Step-by-Step step 2 now gives each
  observation well's own Theis fit (8,320, 8,090 and 8,260 ft2/day; checks.py R6 asserts each keeps the call); (3)
  the closing passage now states the OW-S-alone closure (it fits the sentinel's half foot of signal more closely only
  by missing MS-MW) and the DW-17 closure (a model without walls fits the record as well and reads 6 ft; Plate 3 maps
  the edges 5,000 ft apart and the walls give 7 ft). No pack, prompt or graded figure moved. Re-judged once (below).
- **Gate G:** method_or_model_selection, analytical_non_defect, surface_read_dependency no, sole_data_defect no.
- **Gate H:** domain pass, layers pass, decisive_step analytical, chain 5 inferences.
- **The judge's sensitivities, answered:** the transmissivity window it found (7,400 to 9,300 ft2/day) contains every
  fit the golden's processing gives (8,090 to 8,320); its 7,400 at OW-2 came from its cruder processing.

## The judge's verdict, verbatim

# Determinism verdict, task3 (Reidel Road, Rule WR-4)

**Verdict:** DETERMINISTIC. I reproduced the main call and supplementary answers 7, 8 and 9 independently. Two sensitivities are reported below as risks, not failures.

**Disposition:** FIX_NOW. The only repair is presentation. The PNG in the unzipped folder still carries the caption "Wells of the Reidel Road field added October 2026." (visible lower right on the plate), although the brief says it was removed. Re-cut the bundle from the final PNG. No figure moves, so no model rerun is needed. Optional lever: see the two sensitivities under Evidence.

## Why
The call is forced by the files if the solver reaches a leaky, wall-bounded aquifer calibrated on the far wells CV-02 and CV-11. That reading reproduces the golden almost exactly: 1,000 gpm peaks at 8.1 ft and 1,250 gpm at 9.9 ft against the 9.0 ft limit in Table 1 of the Rule. The tempting alternatives each land on 1,250 gpm or on none, and each is ruled out by named data. The shipped data separate them: CV-07's departure from CV-02 and CV-11 grows with Mill Street pumping, and the Theis hindcast of MS-MW is more than twice the record. I found no Gate A, B, D or E failure. Gate C holds with two margin and fork cautions (below).

## Evidence (recomputed from target/ only)
| Item | Golden | My recompute | Source |
|---|---|---|---|
| Monthly Mill Street rates (gal to gpm, units mixed, 1000 gal before 2016-07, 2019-05 run-hours month consistent) | n/a | 2025 mean TW-1 285, TW-2 224 gpm | harlow_springs_MOR csv |
| MS-MW 2025 drawdown vs CV-02/CV-11 mean (TW-1 "running" reads dropped, MP history applied) | 5 ft (4.9) | 4.95 ft | mill_street_MW csv, well register MP history, network csv |
| CV-07 departure from CV-02/CV-11, relative to 2006-08 baseline | 0.01 in 2008, -1.67 in 2025 | +0.10 (2008), -1.70 (2025) | network csv (CV-07 MP change 2013-08 applied) |
| OW-S departure | about 0.5 ft Mill Street drawdown | -0.32 ft in 2025 | network csv |
| Leaky strip model (Hantush W with no-flow images; walls 5,000 ft apart read off Plate 3, slanted; T 8,160, S 1e-3), B = 3,526 ft | MS-MW 4.9, OW-S/CV-07 fit | MS-MW 4.96, CV-07 1.74 (record 1.70), OW-S 0.54 (record 0.32) | plate PNG, register coordinates |
| Joint least-squares B over MS-MW, CV-07, OW-S (monthly 2009-2026) | 3,526 | minimum near 3,500 (summed squared error 0.102 at 3,526 vs 0.125 at 3,400 and 0.178 at 3,700) | derived |
| OW-S greatest monthly drawdown 2046, all months peak in July 2046 | 4, 6, 8, 10 ft | 4.15, 5.95, 8.11, 9.90 ft | application PDF schedules and factors, Mill Street projection (1.2 per cent growth reproduces the stated anchors) |
| DW-17 (nearest registered domestic well, about 3,040 ft from PW-1; DW-22 5,240 ft, DW-09 7,840 ft), 1,000 gpm, 2046 | 7 ft | 6.81 ft (6.63 to 6.88 for walls 4,500 to 5,500 ft apart, B refit) | register, plate |
| Rival: calibrate on OW-S alone | B 3,065, MS-MW 4.4 ft | B 3,065 gives MS-MW 4.39 ft, OW-S 0.34 ft, and 1,000/1,250 peaks of 6.45/7.91 ft | derived |
| Rival: no walls at B 3,526 | n/a | 1,000 gpm 4.79 ft, 1,250 gpm 5.90 ft at that B; the golden says the same result holds after refit | derived |
| Theis test fit (my crude re-processing, 1,005 gpm, EDT/UTC aligned, barometric correction, pre-test trend) | T 8,160, S 1.0e-3, residual 0.08 ft | per well T 8,600 (OW-1), 7,400 (OW-2), 8,600 (OW-3); joint 8,300; S about 1e-3 | transducer csv, baro csv, field readings |

I did not rebuild the test analysis to the golden's exact residual. The figures agree to within my cruder processing.

**Sensitivities and forks (not failures, but the margins are about 10 per cent):**
1. **Transmissivity window.** With B refit to MS-MW's 4.95 ft at each T, the answer 1,000 gpm holds for T of roughly 7,400 to 9,300 ft2/day.
   - T = 7,000 gives 1,000/1,250 peaks of 7.04/8.65 ft, so 1,250 gpm would be permitted.
   - T = 9,500 gives 9.14 ft at 1,000 gpm, so 700 gpm would be permitted.
   - My own per-well fits span 7,400 to 8,600, and OW-2 alone sits at the lower edge, where the 1,250 gpm peak is about 9.0 ft. The golden's 8,160 and its claim that "T from any observation well" keeps the call rest on its cleaner processing. A judge should confirm that claim from the golden's per-well fits. If OW-2's fit is below about 7,500 the 1,250 gpm margin is a coin toss.
2. **OW-S-alone calibration (B 3,065).** It fits the sentinel record better by itself (RMSE 0.144 vs 0.218 ft) and permits 1,250 gpm. It is ruled out only by MS-MW (4.4 vs 4.95 ft) and CV-07. That misfit is real (about 0.5 ft against reading noise near 0.1 ft), so the closure is defensible. It is a genuine alternative a strong solver could choose, and the files give no rule saying "calibrate on all three wells". If the golden does not already document the residual comparison, add it to the answer blocks.
3. **Supplementary question 9 (DW-17: 7 ft) depends on reading the walls from Plate 3** (no-flow edges 5,000 ft apart). A solver who skips the plate and refits gets 6 ft, as the golden's step 8 states. The prompt never mentions the plate or boundaries. Treat 6 as a surviving alternative for answer 9 only. It does not touch the main call. Consider a tolerance note in the rubric for answer 9, or have the prompt name the plate.
4. Wall slope and spacing are read off the PNG. Within plus or minus 500 ft of spacing, answer 9 still rounds to 7 and the main call is unchanged after refit.

Other points that passed: the permit term and months (April 2027 start, 2027-2046); the 56/44 TW-1/TW-2 split; the monthly factors; the largest alternative that meets 4.1 (the Rule's own tie-break, 4.2); the greatest month in the final year (4.3); the nearest domestic well (4.4). All rule terms are in the shipped Rule PDF and application PDF. The method vocabulary ("leakage factor", "Theis") appears in the answer blocks only; the prompt leaves the method open, as intended.

## Files/Hygiene
PASS, with one stale item. 13 files: csv (6), xlsx (3), pdf (3), png (1), so four formats. Two large messy CSVs (transducers 103,682 rows, network levels 1,911 rows plus mixed units and MP changes in the other tables). Distractors present and unlabelled (water-quality workbook, step test, drillers' logs for non-decisive wells, shallow CV-04/CV-09/CV-13). Real-looking operational artifacts with incidental noise (mixed units, MP changes, meter replacement, re-hung logger, timezone mixes). No authoring or benchmark disclosure found. Temporal coherence fine (application draft dated 30 October 2026, District data supplied 2 October 2026). Stale item: the PNG still shows the "added October 2026" caption, contrary to the brief. It is harmless to the figures but should be re-cut. No exclusion-level finding.

## Stump power
Strong. A competent analyst who fits the test well with Theis fails every schedule (hindcast 12 ft at MS-MW vs 5 ft record). One who calibrates against the nearest network well CV-07, or the wells' own pre-pumping baselines, gets B near 1,900 ft and every schedule under 4 ft, which files 1,250 gpm. That is the reasonable but insufficient route. The deciding insight, that CV-07 sits inside the Mill Street cone, comes from separating two explanations for one pattern (wet-year recharge vs Mill Street drawdown) and is hard to see without the cross-well departure analysis. Risk: if a solver stops at T from the test and B from the sentinel alone, the answer 1,250 gpm can be reached for a defensible-looking reason (sensitivity 2).

## Stumping type
`mechanism: method_or_model_selection` (with statistical_rigor on the far-field reference choice), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. The reported numbers are fine. The difficulty is choosing the model and the reference wells on honest data, and carrying the calibrated model twenty years forward against a limit.

## Deep reasoning
`domain: pass`, `layers: pass`, `decisive_step: analytical`, `chain: 5 inferences, judgment: separating natural level from Mill Street drawdown and calibrating a bounded leaky aquifer to it`, `one_fact: "CV-07 is inside the Mill Street cone"` (no single sentence makes the rest routine: the solver still has to rebuild the test fit, fit the leakage factor with walls, and superpose both fields to 2046).

Layer 1 is the mixed units, clocks, re-hung logger, and measuring-point and meter changes. Layer 2 is the groundwater hindcast and calibration. The easy route from CV-07 or the wells' own baselines gives under 4 ft and 1,250 gpm. Swapping the nouns (for example a river) breaks the wells and aquifer test reasoning, so the domain is used, not borrowed.

## Fix
Where: input_files (presentation only) and solution. (1) Re-cut the plate PNG without the "added October 2026" line and confirm the shipped zip contains the final PNG. (2) In the answer blocks, document the per-well T fits and the OW-S-alone residual comparison, so the closures on sensitivities 1 and 2 are visible. (3) Add a rubric tolerance or a prompt pin for answer 9 (the plate's walls), since 6 ft is an alternative for solvers who skip the plate. No change to the main call or any graded figure.

## Re-judge of the FIX_NOW (one pass, 2026-11-08)

Isolated Sonnet thread on the final bundle and the revised Step-by-Step: **DETERMINISTIC, APPROVE.** The plate no
longer carries the caption; its own per-well Theis fits (8,430, 8,110 and 8,370 ft2/day) agree with step 2's
(8,320, 8,090 and 8,260) and sit inside the window where 1,000 gpm holds, so the first pass's margin concern at OW-2
is gone; the OW-S-alone closure (B 3,065 ft, MS-MW 4.4 against the record's 4.9 ft) and the DW-17 closure (Plate 3's
mapped edges) cite shipped data. Residual note, not blocking: a solver who skips the plate reads 6 ft on answer 9
only; the rubric may carry that as a tolerance note.
