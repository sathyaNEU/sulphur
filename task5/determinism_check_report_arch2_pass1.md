# determinism-check report, task5 (architecture 2, Domains Fit repair), 2026-11-08

Bundle: target.zip sha256 prefix 5cf39da4694631c8. One judge thread (sonnet, medium), scratch /tmp/determinism-check-task5-021431/, verdict at /tmp/determinism-check-task5-021431/verdict.md. Note: no Agent tool in my runtime, so the main session spawned the thread from my judge_brief.md. The existing determinism_check_report.md and determinism_check_report_arch1_pass2.md were left untouched.

## Verdict
DETERMINISTIC (no SOLUTION_WRONG)
**Disposition:** SEND_BACK (Gate H: H5 fails, H4 weak; the spec gate on the 20,000-row CSV also fails). Borderline on H; see Next action.
**Stumping type:** mechanism: other (signal classification, tending to single_conceptual_flip, proxy swap from level to rhythm), stumping_family: analytical_non_defect (borderline), surface_read_dependency: no, sole_data_defect: no

## Why
Every committed figure reproduces from the shipped files. The regulation (Sections 3, 4, 6) and the email file the estimand, the interval basis and the three register-quality definitions, so literal execution gives the golden. No rival survives: the consumption floor (1 to 10 kWh) designates none, the register's empty dwellings designate all ten, the household-rise rule designates the five. The interval side is the same under exact, Wilson, Jeffreys and Wald (Hesteby's lower bound is 5.1 or above under all four), so grading only "wholly above 5.0" is safe. The weakness is stump depth: the daily rise is bimodal (vacant about 0.1, lived-in 0.6 or above), the same 396 results for every threshold from 0.2 to 0.6 and every window and clock variant, so once a solver tests diurnal structure nothing is left to justify.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Counted dwellings (matrikkel Bolig, tatt_i_bruk by 1 Nov) | 8,020 | 8,020 (per municipality 1640, 520, 980, 860, 430, 740, 380, 1120, 560, 790) | yes |
| Vacant by rise rule | 396 | 396 (66, 38, 63, 33, 28, 34, 31, 36, 30, 37) | yes |
| Shares | 4.0, 7.3, 6.4, 3.8, 6.5, 4.6, 8.2, 3.2, 5.4, 4.7 | same | yes |
| Qualifiers | 5802, 5803, 5805, 5807, 5809 | same | yes |
| Median daily use vacant / lived-in | 20.5 / 19.5 kWh | same | yes |
| Floor 1, 3, 5, 10 kWh max share | none qualify | 1.0, 3.7, 3.7, 4.7 | yes |
| Register rolled back to 1 Nov | 13,599 persons in counted dwellings; 834 empty | 13,808 rolled back, 13,599 in counted dwellings; 7,186 held / 834 nobody | yes |
| Over / under coverage, net bias (county) | 118 (1.6), 556 (66.7), 5.5 | 118, 556, 5.46 | yes (all ten municipalities too) |
| Intervals wholly above 5.0 | Tverrvika, Hesteby, Ørnevik | same under four methods | yes |

## Competing answers that survived
None. Floor gives none, register gives all ten (ruled out by Section 4), register-only with no household day gives Hesteby alone (ruled out by Section 4), rise-rule variants all give the five. Cross-batch check not performed (no prior-task archive supplied).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Usable files | 10 or more | 14 | yes |
| File categories | 2 or more | csv, parquet, xlsx, pdf, eml (spreadsheet, text, database-like, document) | yes |
| Large CSV, 20,000 rows or more | 1 | largest CSV is folkeregister_bosatte at 13,777 rows; the 2,720,816-row file is parquet, not CSV | NO |
| CSV of 10 to 20 printed pages or more | 1 | matrikkel (8,925 rows) and folkeregister (13,777) exceed that | yes |
| Distractors in metadata.json | 2 or more, none labelled in ZIP | 6 named; none labelled in the ZIP | yes |
| Distractors relevant yet unused | weigh, ruled out by a shipped fact | spotpriser, outage log, grunnbok, enhetsregisteret, aksjonaerregisteret: plausible context, not load-bearing | yes (judge did not name any as the surface read) |
| Deliverables | 1 to 3, all in golden | 2 (docx, xlsx), both present in golden/ | yes |
| Unit and rounding in asks | each | per cent to one decimal, stated once at the end | yes |
| Answer shape | gradable cells downstream of deep step | ten-row table, chart, ten-row register table, 8,020-row file | yes |
| Golden ZIP holds exactly requested files | exact | the two requested files | yes |
| Inputs license-clean, not fabricated | real or licensed | metadata.json states all data is constructed for the task and fictional; fits "nothing fabricated" poorly | flag |
| Submission completeness | ask 2 requires interval | answer 2 lists counts and shares but no interval bounds in the submission text (only the three wholly-above names) | flag (the interval values should sit in the golden table; not verified by me) |

## Gate G reconciliation
Judge: mechanism other (measurement/signal classification), family analytical_non_defect (borderline), surface_read_dependency no, sole_data_defect no. Design note: classification from a measured signal (estimation_fit), measurement-model judgment, WORKS IN FORM. The families agree; the weighting does not. The design note's own "Judgment" line concedes the rise is bimodal with nothing between 0.3 and 0.8 kWh, so every cut gives the same five; the judge reads that as a judgment with no justification burden, a proxy swap close to a lens flip. No declared distractor carries the task. Mismatch on depth is the finding that predicts send-back.

## Gate H line
domain: pass; layers: pass; decisive_step: data_semantics (borderline analytical); chain: 5 inferences, judgment weak; one_fact: "occupied homes show morning and evening use above their own night-time use". H4 weak, H5 fails.

## Stump power (Gate F)
Moderate to low. The textbook routes (consumption floor, register count) are cleanly refuted, which is the design's rung 0 and 1 trap, but a model that plots hourly profiles finds the rise. A model that stops at the floor and files "none" is the expected loss, and that run forecast is sound on paper. The register rollback with the November block renumberings and the exact rates in answer 4 are rule and semantics work, not the decisive chain. Main thread to weigh against the design note's ladder: the deciding step is a landable method once the hint "heated when empty" is reached.

## Findings, ranked
1. H5 fails: one sentence (morning and evening use above own night use) rescues the run; H4 has no real statistical judgment (bimodal, threshold-insensitive).
2. Spec gate: no CSV of 20,000 rows or more (the large file is parquet).
3. Metadata states the data is fully constructed and fictional, against the real-data inputs rule.
4. Interval bounds are absent from the submission's answer 2 text.
5. Cross-batch check not performed.

## Next action for the author
Decide between (a) rebuilding the occupancy step so the call needs a justified threshold or model (weak or part-fortnight rises near the cut), with the golden, regulation and email unchanged, plus shipping a 20,000-row CSV, or (b) accepting the Gate H risk and letting the platform runs decide. The judge itself called H borderline. Fix the CSV size gate either way.
