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


---

# determinism-check report, task3, round 3 (the FIX_NOW re-judge), 2026-11-10

Bundle: target.zip md5 0d54ea15f6144e05bef9a00526795bfe (unchanged since round 2's rebuild). Thread: one sonnet medium judge, scratch /tmp/determinism-check-task3-r3/, verdict at /tmp/determinism-check-task3-r3/verdict.md.

## Verdict
DETERMINISTIC (main call and supplementary answers 2 to 5 and 7 forced by the files). No SOLUTION_WRONG.
**Disposition:** FIX_NOW, solution blocks only: grade answer 6 (tides, weather) as bands with the order-average convention stated, and grade River Road's expected days on its band 11.7 to 18.7. No rerun, no prompt or input change. The main thread is restating answer 6 and the River Road component accordingly.
**Stumping type:** mechanism: forecasting (with decomposition_attribution and method_or_model_selection), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no.

## Why
The funded pair reproduces from the shipped harbor, logger, sensor and flow files. The rivals (straight-line Marsh and River transfers, drain rim, count trend, doubled sea level) are ruled out by named data and by the guidelines' definitions. The round 2 findings are closed: River Road's expected days and the pair-years count now fall inside their bands (13.5 to 13.8 against 11.7 to 18.7; 31 against 27 to 33), and the Marsh hinge and Oyster quadratic forms are no longer outside the bands.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Harbor 2025-26 days | 21 | 21 | yes |
| MSL above epoch 2025-26 | 0.63 | 0.63 | yes |
| Raw departure double count | 38.9 | 39.1 (62 on the replay) | yes |
| Harbor expected 2027-28 | 27.0 (25.9 to 27.5) | 26.9 | yes |
| Harbor 90 per cent range | 22 to 31 | 21 to 31.3 | yes in band |
| Front lane / 2025-26 days | 5.20 / 20 | 5.200 / 20 | yes |
| Wharf 2025-26; Wharf / Front expected | 26; 32.3 / 25.0 | 26; 32.3 / 24.6 | yes |
| Marsh threshold, 2025-26, expected | 8.75, 17, 14.3 | 8.74 to 8.77, 17, 14.5 | yes |
| Marsh straight line | 8.54, 26, 33.6 | 8.54, 26, 33.3 | yes |
| Oyster threshold, 2025-26, expected | 9.11, 8, 1.2 | 9.12 to 9.17, 8 (7 at 9.17), 1.4 | yes in band |
| River flow lift; campaign mean flow | 0.47 ft per 20,000 cfs; 24,900 | 0.42 ft; 24.6 to 24.9 kcfs | yes in band (component text says 0.47) |
| River 2025-26 | 10 (8 to 12) | 9 (sqrt 7, log 5 fit worse) | yes in band |
| River expected | 17.1 (11.7 to 18.7) | 13.5 to 13.8; 12.9 sqrt | in band, point not matched |
| Pair holds in weather years | 28 (27 to 33) | 31 | in band |
| Split (sea level, tides, weather) | +5.8, -0.7, +1.0 | +5.6, -1.5, +1.85 (Shapley average) | sea level yes; tides and weather inside order ranges, not at the golden's averages |

## Competing answers that survived
1. Answer 6, split order: the prompt does not say how to attribute an interacting change. Sea level is stable (+4.1 to +7.0 over the six orders); the tides sign is order-dependent (-3.0 to +1.7). Soft fork on supplementary 6 only, closed by grading the three parts as bands and stating the averaging convention in the blocks. A hard pin would need a prompt phrase ("averaged over the orders in which the three changes can be applied") and a rerun.
2. River Road expected days: the point 17.1 is the top of the judge's reproductions (13.5 to 13.8). Logger lag assumptions move the result between 9.9 (0.75 h) and 13.8 (1.25 h); the ranking does not change. Closed by grading on the band.
Weather-year alignment, logger clock and the extrapolation of the flow form move results under 0.5 day or inside the bands. No fork changes a rank or the funded pair.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Usable files / categories | 10+ / 2+ | 15 / csv, txt, xlsx, pdf | yes |
| Large messy CSVs | 20k rows plus one of 10 to 20 pages | sensor 209,260 rows; hourly heights 235,224 rows (both far past the page count) | yes |
| metadata.json distractors | 2+, none labelled in the ZIP | 3 (311 requests, GHCND rainfall, SLR scenarios), unlabelled; judge found none carrying a result. Each is unused and weighable: 311 reads as a flood count but undercounts; SLR looks like the planning value but the guidelines fix 0.70 ft; rainfall looks needed for Front Street but the harbor already separates it | yes |
| Distractor wording | no file reveals the build | judge flags none; the judge also listed hourly heights among distractors, but metadata names it evidence (it is used for the residual-at-every-hour check); not a defect | yes |
| Deliverables | 1 to 3, all in the golden, no format family | 2 (xlsx, pdf), golden.zip holds exactly these | yes |
| Asks: unit and rounding | stated | one decimal and whole days in the prompt | yes |
| Prompt | one paragraph under 1,000 characters, no method or file named | 790 characters, none named | yes |
| Answer shape | one of the fourteen, 4+ checkable results | allocation with sensitivity (ranked list under a cap); judge counts 15 graded results over 6 areas | yes |
| Asks multi-dimensional | not stacked lookups | five low points by two years, plus range, split and robustness count | yes |
| Realism / LLM-read | | not re-audited this pass (golden-realism owns it); judge found no authoring language in the PDF or xlsx; minor: series run to 31 Oct 2026 past the PDF's 16 Oct issue date | n/a |

## Gate G reconciliation
Thread: method_or_model_selection, analytical_non_defect, surface_read_dependency no, sole_data_defect no. The note's `## Hidden factor record` agrees (all five factors marked not only in the deciding units: Oyster Creek bends too, the river flow runs the whole campaign and year, every rim sits below its lane). Gate G holds: no shipped artifact ranks the pair wrongly, and the difficulty survives deleting wrong numbers because the 311, rim and trend values are not graded results. House-rule point to keep watching: the Marsh bend and River flow lift are constructed; the thread did not raise them as shallow, since each took a fitted transfer with a validated form and a second file, and neither alone decides the pair (the pair needs the harbor machinery, the lane and both transfers).

## Gate H line
domain: pass; layers: pass (L1 datums, clocks, outage, unsurveyed lane, rim decoy; L2 residual forecast, two bending or flow-dependent transfers, attribution); results: 15 graded across 6 areas (note lists 9 in 8 areas, same set grouped differently); one_thing: none; effort: quick 4, careful 9, thorough 14 of 15; one_fact: "Marsh and River do not sit on a straight line to the harbor" rescues 5 of 15 (a third); "do not let the sea level enter twice" rescues about 7 of 15 (47 per cent) but needs the weather-year build anyway.
Reconciliation with the note (now current: River 17.1 with band 11.7 to 18.7, R6 10 (8 to 12), R9 27 to 33, matching submission.md):
- Effort test mismatch. Note: quick 0 of 9, careful 2.5 of 9 (28 per cent), thorough 9. Thread: quick 4 of 15 (27 per cent), careful 9 of 15 (60 per cent). The thread's careful pass reaches more than twice the note's share; the note's table separates the passes, the thread's does not separate careful from thorough by much (9 against 14). Per the bar, a careful-hurried share above a third is a send-back risk; the main thread must weigh effort.py's computed column against this and decide whether to keep the note or redesign.
- Hint count. The note's Largest single hint (River's flow, 1 of 9) is lower than the thread's best sentence (the sea-level-twice hint, 7 of 15, or the straight-line hint, 5 of 15). The note must name the largest by the thread's count; 7 of 15 exceeds a third by a small margin and the thread called it borderline.
- Bands against rivals (Gate C). River's expected band (11.7 to 18.7) now spans the judge's 13.5 to 13.8 and still excludes the hurried 37.3; the pair-years band spans 31. Answer 6's tides band crosses zero, which makes it a weak grader; keep it a band, with sea level as the stable graded share.
- Distractor load: none carries a result.
- Largest effect on the price: the thread reached the harbor figures, the lane and the Wharf and Front counts by standard method; the results it reaches only with judgment are the Marsh and Oyster bend, River's flow term, and the split. Hurried figures: raw departure 38.9, straight-line Marsh 26 and 33.6, single-offset River 26 and 37.3, drain rim 44, count trend 10.8.

## Stump power (Gate F)
Good. The hurried failures differ per result and are analytical: doubled sea level, straight-line Marsh, single-offset River, rim as elevation, count trend, one-at-a-time bridge. A careful run still has to choose the alignment, lag and flow form and will file figures a few days off at River Road and in the split, where legitimate band-edge losses occur. The thread's estimate: a good chance both runs land under 60. Results a careful hurried run earns by the field's standard method: harbor expected days and its 2025-26 count, the Front lane, the Wharf row.

## Findings, ranked
1. Effort table: thread's careful pass 9 of 15 (60 per cent) against the note's 28 per cent; reconcile with effort.py's column before READY.
2. One-fact count: the sea-level-twice sentence rescues about 7 of 15; the note's hint line names a weaker one. Update the note or redesign.
3. Answer 6 split and River's point: grade as bands (FIX_NOW, in hand by the main thread).
4. The prompt does not fix the averaging of an order-dependent split; kept as a soft fork unless a prompt phrase is added (rerun).
5. River flow lift in the components (0.47 ft) against the thread's 0.42 ft on 20,000 cfs; inside the band but restate it as a band.

## Next action for the author
Apply the answer 6 and River Road band edits to submission.md, then reconcile the note's effort table and `Largest single hint:` with the thread's counts (careful 9 of 15, sea-level-twice 7 of 15) against effort.py before READY.
