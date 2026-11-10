# determinism-check report, task3, 2026-11-10 (round 1, bundle target.zip md5 5cc1927b843a50224a47f84691d032aa)

Note: the main thread rebuilt the pack after this judge ran (River Road campaign dates and 15-minute logger steps in the inventory, Wharf Street's name). The current target.zip is md5 1c1fb1fe...; this round is recorded against 5cc1927b and a round 2 follows on the final cut. The judge thread's verdict is /tmp/determinism-check-task3-1794287274/verdict.md.

## Verdict
NOT_DETERMINISTIC (narrow). The funded pair is forced; ranks 3 and 4 and several one-decimal figures are not. Governing label: competing_defensible_answer (River Road vs Marsh Road for rank 3 and 4), with underspecified_objective on the harbor split.
**Disposition:** SEND_BACK (prompt, asks and bands change; the pack can stay).
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
- Wharf Street and Front Street lead every variant run, by 8 or more days over third place.
- River Road's transfer is fitted on a 174-tide campaign. A linear-in-flow term (sd 0.079 ft) and a linear-flow-plus-height-curvature term (sd 0.078 ft) cannot be told apart by fit. Linear gives River Road 15.9 expected days, below Marsh Road's 16.8; curvature gives 18.3 (golden 18.5, above Marsh). A rigorous solver on the plain form ranks Marsh 3rd and River 4th, the reverse of the golden. The "rank all five" ask therefore has two defensible answers.
- River Road's 2025-26 count moves with the flow form: 10 linear, 11 with curvature, 7 square root, 5 log.
- Front Street's flooding level (sensor "records water on the lane") has readings 8.61, 8.64, 8.66 ft MLLW; they give 26.2, 23.5, 21.6 expected days and 21, 20, 20 in 2025-26, and move the pair count to 30/29/27.
- The harbor split averaging over six orders and the weather-year alignment are not filed in the prompt.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| MSL anomaly 2025-26 | 0.63 | 0.628 | yes |
| Harbor days at 8.6 ft, 2025-26 | 21 | 21 | yes |
| Harbor expected days 2027-28 | 27.0 | 27.25 / 27.1 / 26.6 by alignment and MSL0 | within 0.6 |
| Harbor 90% range | 22 to 31 | 22.75 to 31 | yes |
| Raw departure (sea level twice) | 38.9 | 39.2 | yes |
| Marsh straight-line crossing | 8.51 | 8.514 | yes |
| Marsh bending crossing | 8.71 | 8.713 (break 7.46, slopes 1.01, 0.60) | yes |
| Marsh residual sd line/bend | 0.10/0.03 | 0.101/0.032 | yes |
| Marsh line error at 13 top tides | 0.18 | 0.177 | yes |
| Oyster flooding level | 9.15 | 9.164 | yes |
| River campaign mean flow | 24,600 | 24,592 | yes |
| River single-offset 2025-26 | 30 | 27 | no |
| 2025-26 Wharf/Front/Marsh/Oyster | 26/21/19/7 | 26/21/19/7 | yes |
| 2025-26 River | 10 | 10 linear (11 curved) | yes, form-dependent |
| 2027-28 Wharf | 35.0 | 35.4 (34.9 to 35.8) | within 0.8 |
| 2027-28 Front | 26.3 | 26.2 | yes |
| 2027-28 Marsh | 16.8 | 16.8 | yes |
| 2027-28 Oyster | 1.0 | 0.9 | yes |
| 2027-28 River | 18.5 | 15.9 linear, 18.3 curved, 14.6 log, 14.8 sqrt | only under curvature |
| Pair holds in weather years | 29 of 36 | 30 plain linear River; 28 to 29 curved; 27 to 30 over Front level | form-dependent |
| Harbor split sea/tides/weather | +5.8/-0.7/+1.0 | +5.65/-0.82/+1.42 | convention-dependent |

## Competing answers that survived
1. Ranks 3 and 4: River 18.5 over Marsh 16.8 (curvature in height) vs Marsh 16.8 over River 15.9 (plain linear flow). Closing rule absent from the shipped files; the fit cannot choose.
2. Front Street's level: 8.61 (first sustained wet tide, golden) vs 8.66 ft (depth-regression intercept). Changes Front's days by 2 to 5 and the pair count by 1 to 5.
3. Harbor split convention (average of six orders) not filed; weather-year alignment (calendar date, interpolated residual) not filed.
4. Pair-count 29 of 36 is unstable across 27 to 30.

## Spec gates (checked on the 5cc1927b unzip, golden.zip and metadata.json)
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Usable files | 10 or more | 15 | yes |
| File categories | 2 or more | CSV, TXT, PDF, XLSX (spreadsheet and text/document; no database, image or code) | yes |
| Large messy CSVs | one of 20,000 rows or more, one of 10 to 20 pages or more | sensor 209,260 rows; hourly 235,224; high/low 101,489 | yes |
| Distractors in metadata.json | 2 or more, none labelled in ZIP | 3 (311 requests, GHCND rain, SLR scenarios); judge found no label | yes |
| Distractor weight | unused but weighed | judge: present, not load-bearing | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, pdf); golden.zip holds exactly both | yes |
| Asks multi-dimensional, unit and rounding stated | yes | yes (one decimal, whole days) but five-way rank, split and pair count carry unfiled conventions | no (forks above) |
| Answer shape, 4 or more checkable results | yes | ranked list under a cap with sensitivity; 6 graded results | yes |
| Band separates hurried from golden, excludes no rival | yes | River band excludes the linear rival in the note (see below) | no |
| Realism | no LLM tells | judge found none; not independently checked on golden contents beyond listing | not assessed |
| Prompt | one paragraph under 1,000 characters, no method or file named | 785 characters; names no file or method | yes |

## Gate G reconciliation
Judge: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. The design note's hidden factor record (Marsh bend, River flow lift, Front lane over rim) matches: the judge found these generated across both marsh sites and the whole river reach, not only in the deciding units, and not shallow. Gate G (no shipped artifact ranks wrongly on the decision) holds: the guidelines, inventory and 311 rank nothing. Reconciled; no conflict on Gate G.

## Gate H line
domain: pass, layers: pass, results: 6 graded across 5 areas, one_thing: none, effort: quick 1, careful 3, thorough 6 of 6, one_fact: "the marsh and river transfers bend or carry flow" rescues 3 of 6.
Reconciliation with the note:
- The note counts nine results and says quick 0, careful 2.5, thorough 9 of 9, and that the best single sentence (River's flow) rescues 1 of 9. The judge's combined sentence rescues 3 of 6 (one half), more than the third allowed. Separate marsh and river sentences each rescue only R5 or R6 on the note's accounting, but a combined hint of one clause is a single fact in practice: this is the exposure the project lead flagged. Main thread to weigh.
- The note's goldens are stale against the submission: note R7 gives Wharf 32.3, Marsh 14.3, River 15.9; R5 Marsh 17; R9 30 of 36; SF11 chooses the power form. submission.md gives Wharf 35.0, Marsh 16.8, River 18.5; Marsh 19; 29 of 36; "curvature". The note's River figure 15.9 equals the judge's plain-linear rival, and the note's own River band (14.1 to 17.0) excludes the submission's 18.5. Gate C: the golden and its band disagree, and the rival lands outside the golden's value. The note must be reconciled to the final cut.
- Effort: the judge's quick 1 of 6 is above the note's 0; careful 3 of 6 is half the results, not the note's "2.5 of 9" (28 per cent); the careful and thorough levels remain separated. The careful level is above a third of results on the judge's count.
- Distractors do not carry any result (not too load-bearing).
- Stump power per result: the hurried failures that bite are the straight-line Marsh/Oyster transfer, River's single offset (27 to 30 days), the doubled sea-level departure (38.9), Front's rim/sensor-only count (44 or 15); the pair stays correct under every River and Front variant, so the stump is real for the call, but ranks 3 to 5, the one-decimal figures and the split lose on forks, not on analysis. Results the careful column reaches by textbook method: harbor expected days and Front's lane (R1, R4).
- One-fact count: 3 of 6 for the combined sentence (above the 1/3 cap).

## Stump power (Gate F)
Real weight over several results (transfers, sea-level-corrected ensemble, lane from sensor, bridge). The weak part is that the grades for River, rank 3 and 4, the pair count and the split depend on unfiled choices a strong run can make defensibly.

## Findings, ranked
1. River Road flow form: rank 3 and 4 flip (15.9 vs 18.5); the 2025-26 count ranges 5 to 11. Competing answer, SEND_BACK.
2. Front Street level not pinned to a single estimator; pair count 27 to 30.
3. Harbor split averaging rule and weather-year alignment unfiled.
4. Design note out of date against the submission (goldens, bands, SF11, nine vs six results); band excludes the golden's own River value.
5. Effort test: one combined hint rescues half the results on the judge's count.
6. Inventory vs Hensley logger mismatch (dates, interval): fixed in the rebuild per the main thread; re-judge on the final cut.
7. Cosmetic: "Wharf Street at Market Lane" vs "Wharf Street seawall": renamed in the rebuild per the main thread.
8. Submission's River single-offset figure 30 reproduced as 27: restate or drop.

## Next action for the author
Change the asks so ranks 3 and 4 are either pinned by a filed convention for River Road's flow term (or graded as a tied set with a band spanning 14 to 19 days) with the pair and five figures banded, and file the Front Street level rule, the harbor split averaging and the weather-year alignment as conventions in the guidelines; update the design note to the final cut's figures; then request round 2 on the rebuilt bundle (1c1fb1fe...).

---

# determinism-check report, task3, round 2, 2026-11-10 (bundle 521db5d2edd3226b5e4ae4fde406d10f)

Thread verdict: /tmp/determinism-check-task3-r2-8469/verdict.md. Note: the main thread has since rebuilt (target.zip 0d54ea15f6144e05bef9a00526795bfe: local-day river flows, wider bands, marsh hinge added, guidelines flood day pinned, sensor status column). This round covers the 521d bundle only; a round 3 re-judge on 0d54 follows.

## Verdict
DETERMINISTIC, plus SOLUTION_WRONG (River Road figures and the pair's years count).
**Disposition:** FIX_NOW (acted on by the rebuild; re-judge pending, no SEND_BACK on this pass).
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The funded pair (Wharf Street at Market Lane, Front Street at Ferry Lane) is forced and survives every variant the judge ran; Marsh and River are separated by named data (the bend in the Pellam Creek campaign; River's offset falling with flow). River Road's 18.7 days (band 14.1 to 19.5) did not reproduce (judge: 13.2 to 13.5 across linear, power, quadratic; 12.2 to 12.6 sqrt, log), and 28 of 36 became 32 (band 27 to 31). River 2025-26 was 9 (band floor). Marsh hinge at the 4.29 ft platform gave 12.2, under the 13.2 band floor; Oyster quadratic gave 10 days (band 7 to 9).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Harbor 2025-26 days | 21 | 21 | yes |
| MSL above epoch 2025-26 | 0.63 | 0.633 | yes |
| Raw departure double count | 38.9 | 39.1 | yes |
| Harbor expected 2027-28 | 27.0 | 26.4 (in variant spread) | yes in band |
| Harbor 90% range | 22 to 31 | 20.8 to 31.0 | low end in band |
| Wharf 32.3 / Front 25.0 | | 31.9 / 24.4 | yes in band |
| Front lane 5.20; 20 days (15+5) | | 5.200; 20 | yes |
| Marsh line 8.54, 26 d, 33.6 | | 8.54, 26, 33.0 | yes |
| Marsh bend 8.75, 17 d, 14.3 | | 8.74 quad, 8.78 hinge (12.2) | hinge outside band |
| Oyster 9.11, 8 d, 1.2 | | 9.10 to 9.18; quad 8.92, 10 d | quad outside band |
| River flow lift 0.41; mean flow 24,600 | | 0.41; 24,603 | yes |
| River 2025-26 | 12 (9 to 13) | 9 | band floor |
| River expected | 18.7 (14.1 to 19.5) | 12.2 to 13.5 | NO |
| Pair years | 28 (27 to 31) | 32 | NO |

## Competing answers that survived
- River slope-1 flow offset: about 34.5 days, would displace Front; ruled out by fit (sd 0.147 vs 0.078 ft) but not listed among the rivals run.
- Split order: unfiled in the asks; tides band crosses zero and grades little.
- Marsh logger row: sensor elevation (-1.35) above the logger's dry floor (-2.69), minor inconsistency.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Usable files / categories | 10+ / 2+ | 15 / csv, txt, xlsx, pdf | yes |
| Large messy CSVs | 20k rows and a 10-20 page one | sensor 209,260 rows; hourly 235,224 rows | yes |
| Distractors in metadata.json only | 2+ | 3 (311, ghcnd, slr), unlabelled in ZIP; judge: none carries a result (the PDF phrase "weather and river flows" hands the flow dependence, minor) | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, pdf); golden.zip holds exactly these two | yes |
| Asks unit and rounding | stated | one decimal, whole days, in the prompt | yes |
| Shape, 4+ checkable results | | ranked allocation with sensitivity; 14 graded results (judge) | yes |
| Prompt | one paragraph under 1,000 chars | 785, no method or file named | yes |
| Realism of golden / LLM look | | not re-audited this pass (golden-realism owns it) | n/a |

## Gate G reconciliation
Judge: method_or_model_selection, analytical_non_defect, surface_read no, sole_data_defect no. Matches the note's hidden factor record. Residual house-rule point: the Marsh bend and River flow lift are constructed and the judge says they sit in the deciding units; the note says Oyster bends too and River flow runs through the reach. Judge did not raise a send-back. Gate G (no shipped artifact ranks wrongly): holds.

## Gate H line
domain: pass, layers: pass, results: 14 graded across 8 areas, one_thing: none, effort: quick 3, careful 8, thorough 14 of 14, one_fact: "Marsh bends above the platform and River's offset depends on flow" rescues about 4 of 14 (within a third, 29 per cent).
Reconciliation with the note:
- The note is still stale against the final cut: it lists nine results (judge 14), River 17.1 with band 11.7 to 18.7 and R6 10 (8 to 12) where submission says 18.7 (14.1 to 19.5) and 12 (9 to 13); R9 band 27 to 33 vs 27 to 31. The note's effort table (quick 0, careful 2.5 of 9, thorough 9) differs from the judge's quick 3, careful 8, thorough 14: the judge's careful pass reaches 57 per cent of results, far above the note's 28 per cent, and the quick pass 21 per cent. Main thread to re-derive the effort table from effort.py on the 0d54 cut.
- The note's Largest single hint (River's flow, rescues 1 of 9) is lower than the judge's combined sentence (4 of 14, but still under a third). Acceptable if the note names the combined hint.
- A result whose band excluded a rival: River's band excluded the judge's own 12 to 13 recompute (Gate C on that result), and the pair-years band excluded 32. The rebuild widened these (River 12.2, 32 years); verify in round 3 that bands now span the rivals and are not too wide to separate the hurried 34 to 37 figure from golden.
- Careful column: the judge puts the harbor machinery, lane, and 8 of 14 in careful reach; results the textbook method reaches: harbor expected days and Front lane.

## Stump power (Gate F)
Good: the straight-line transfer files River and Marsh as the pair (36.7, 33.6), the doubled sea-level departure gives 38.9, and sensor-only Front gives 15. Losses are analytical.

## Findings, ranked
1. River Road 18.7 and the 28-of-36 count did not reproduce (13 and 32): addressed by the rebuild (local-day flows); confirm in round 3.
2. Marsh hinge (12.2) and Oyster quadratic (10 d) fell outside bands: addressed by wider bands; confirm.
3. Design note stale (nine results, old River figures, effort table, hint).
4. Slope-1 flow offset (34.5) not listed among rivals run; split order unfiled; tides band uninformative.
5. Marsh logger row sensor elevation above its dry floor.
6. Guidelines phrase "weather and river flows" mildly hands the River dependence.

## Next action for the author
Update DESIGN_NOTE.md to the 0d54 cut (14 results, final figures and bands, effort table from effort.py, hint count), add the slope-1 offset and the Marsh hinge to the fork table, then run the round 3 re-judge on 0d54ea15f6144e05bef9a00526795bfe.
