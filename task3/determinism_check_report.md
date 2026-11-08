# determinism-check report, task3, 2026-11-08

## Verdict
DETERMINISTIC (no SOLUTION_WRONG)
**Disposition:** APPROVE once one wording item is applied (see Findings 1). No re-judge needed.
**Stumping type:** mechanism: decomposition_attribution (two offsetting trends) with statistical_rigor, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Note: the isolated thread judged the pack as first spawned (golden CSV with storm_rain_in and paved_fraction_pct columns, prompt without column wording). The author then changed the prompt and golden CSV and rebuilt. Closure of those items is checked by me against the shipped files, not re-judged (one thread only).

## Why
Section 4.2 and 4.3 of the standard pin the design flow (1 per cent annual chance, first ten years, full record plus the county's other records) and 4.5 picks the cheapest alternative that reaches it. Unadjusted log-Pearson III gives 5,085 cfs (A); the storm-paired, today's-watershed fit gives about 10,570 (above A's 7,460, below B's 13,380), so B. All 15 window and threshold variants stayed 10,290 to 11,250 with the same top four. The post-1990-storms rival (4,488 cfs, A) is closed by 4.3's "full length of the gauge's record".

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Kendall tau, 70 peaks (annual_peak_flows.csv) | 0.02, p 0.79 | 0.022, p 0.788 | yes |
| LP3 1% flow as recorded | 5,090 | 5,085 | yes (rounding) |
| Paved fraction 1956 / 2025 (parcels xlsx) | 6 / 30 | 6.2 / 30.5 | yes |
| Log-peak slope per unit paved fraction, 312 storms | 2.96 | 2.95 | yes |
| Rise 1960 to 2025 at fixed storm | about 2.0x | 2.04x | yes |
| Adjusted LP3 1% flow | 10,570 | 10,568 | yes |
| Adjusted top four | 1968, 1983, 1978, 1962 | same (1968 = 7,805) | yes |
| Recorded top four | 1990, 1983, 1968, 1978 | same | yes |

## Competing answers that survived
- None that change the call. Storms-since-1991 only (about 4,490, A) and since 1996 (4,765, A) are ruled out by 4.3 (design note SF13). Projecting paving to 2030 gives about 11,500, still B. A 5-day window falls to 9,500 or below, not a sound pairing, still between A and B on the 3-day-and-under readings the golden claims.
- Rain-gauge mflag codes and the RG-01 to RG-02 handover are undocumented in the pack; data supports one reading and the slope barely moves (SF1, SF2 in the design note, asserted in checks.py).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Usable files / categories | 10+, 2+ | 10 files; docx, csv, xlsx | yes |
| Large CSVs | 20,000+ rows and a 10-20 page CSV | rain gauge 25,720, daily discharge 25,660; peaks above base 1,138 rows (about 20 printed pages) | yes (page count estimated from rows) |
| metadata.json distractors | 2+, nothing in ZIP labels one | 4 named (daily discharge, inspection, cross sections, grab samples); none labelled in ZIP | yes |
| Distractors unused yet weigh | none answers a graded quantity | daily discharge max is 657 cfs mean flow, cannot reproduce 3,880 or 5,000+ peaks | yes |
| Deliverables | 1-3, all in golden | 2 (docx, csv), both in golden.zip, which holds exactly those two | yes |
| Ask shape | multi-dimensional, unit and rounding stated | 70-row table plus ranked top four plus chart; cfs, nearest ten | yes |
| Prompt names table content | gradable cells | "row per water year giving its recorded peak and the peak the estimate uses"; golden CSV has exactly water_year, peak_date, recorded_peak_cfs, estimate_peak_cfs. Prompt does not name the date column, a minor extra | yes |
| LLM-read / realism | none | judge found no authoring leakage; I did not re-sweep the golden docx prose | provisional |
| Real-world licence/source | recorded | metadata says constructed, fictional, CC0 | yes (not verifiable from bundle) |

## Gate G reconciliation
Thread: mechanism decomposition_attribution with statistical_rigor, analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note: judgment "separating two explanations for one flat record by a like-for-like comparison", strategy WORKS IN FORM, hidden by two offsetting effects, one-fact test "the watershed has urbanized" does not rescue. Match. The declared distractors (daily discharge, inspection, cross sections, grab samples) are not named as the surface read; the thread named the impervious-parcels file as a strong cue, but that file is a solving input, not a declared distractor. The design note's own run forecast (field-method run files A at 5,090) agrees with the thread.

Gate H line: domain: pass (flood-frequency with non-stationarity and rainfall-runoff response), layers: pass (L1 gauge change, Monday accumulations, duplicate 2009/2010 export, split and re-keyed parcels; L2 offsetting-trend attribution), decisive_step: analytical, chain: 5 inferences (trend test, paved history, storm-paired response at fixed storm, adjust to 2025, refit and compare), one_fact: none that makes it routine.

## Stump power (Gate F)
Moderate to good. Easy route (stationary LP3, or peaks regressed on paving or time, 5,090 to 5,870) lands A. Concern: a solver who reads the parcels file will suspect urbanisation; the stump rests on separating it from the storms' fall by pairing two unkeyed records, which the thread calls a modeling judgment. No part of the decisive step is a textbook one-shot method; the LP3 fit is rung 0-1. Main thread to weigh against the ladder.

## Findings, ranked
1. LOW, OPEN: submission.md's closing "No other conclusion survives" paragraph still does not name the storms-since-1991 rival (about 4,490 cfs, A) as closed by 4.3. The coordinator says it was applied, but the current submission.md (saved 16:22) has no 1991, 4,49 or 4.3 text in the closing paragraph (step 1 cites 4.3 only). Apply that sentence; it is wording only, no figure or file changes, no re-judge.
2. LOW, CLOSED: unnamed table columns. The prompt now describes the table as recorded peak plus the peak the estimate uses, and the golden CSV carries exactly water_year, peak_date, recorded_peak_cfs, estimate_peak_cfs; submission.md line 22 matches. Verified against the shipped prompt, golden CSV (70 data rows) and submission.
3. LOW, ACCEPTED: undocumented rain-gauge flags and handover; one data-supported reading, slope moves little; recorded as SF1 and SF2 in the design note and asserted in checks.py (not opened by me beyond the design note table).
4. INFO: the judged pack was the pre-fix build; the post-fix prompt and golden CSV were not re-judged, per the one-thread rule.

## Next action for the author
Add one sentence to the closing paragraph of submission.md naming the storms-since-1991 rival (about 4,490 cfs, Alternative A) and that section 4.3's full-length-of-the-record rule rules it out; rebuild if the submission is copied elsewhere; then proceed to READY.
