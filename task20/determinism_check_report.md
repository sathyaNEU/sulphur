# determinism-check report, task20, 2026-11-11

## Verdict
DETERMINISTIC on the structural chain, with two open forks (bridge order on ask 3; the range-calibration method on the range top and so on the call). No SOLUTION_WRONG: the load-bearing figures reproduce.
**Disposition:** FIX_NOW
**Stumping type:** mechanism: forecasting (with decomposition_attribution), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Thread: one general-purpose sonnet medium thread, spawned by the main session on my brief. It wrote own_derivation.md before opening graded_blocks.md (it says so in the verdict). Scratch: /tmp/determinism-check-task20-220603/ (own_derivation.md, verdict.md).

## Why
The short call comes from a chain the thread rebuilt independently and the files force: company regional mix (10-K) against a panel 79% Southeast and West, licensed descriptors, first-delivered completion factors, the private-label penetration table carried to the quarter. Its rebuilt chain gave 1.27% = USD 1,412.0 million against the golden's 1,412.5, record RMSE 0.72 against 0.70.

Two things the golden does not close:
1. Range method. The thread's own derivation, calibrating the range by regression error (RMSE 1.15 to 1.5), gave a centre near 1,425 and a range of about 1,390 to 1,455. The top sits above the street, so the same data supports "no position". The prompt leaves the range method open, and the golden's 0.90-point half-width rests on the structural chain's 0.70 RMSE. The design note's claim that every reasonable rival keeps the top between 1,420.1 and 1,439.7 is not borne out by this run. The rivals that skip the regional reweight but keep the private-label term (lic+PL 1,434.7, age+PL 1,438.8) have tops near 1,459. Governing label: margin_or_boundary_fragility, with the call fork under underspecified_objective.
2. Bridge order (ask 3). The prompt never fixes the order of the adjustments. The licensed step reads -1.68 on the delivered panel and about -1.31 after completion; the golden's band is -1.62 to -1.00. The delivered-panel and comparable-cards points (-14.67, +25.74) are also order dependent. Governing label: underspecified_objective.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Street mean / median | 1,450.0 / 1,448.4 | 1,449.98 / 1,448.4 | yes |
| Licensed share of M0412 spend | 14.71% | 14.73% | yes |
| Completion factors | ~0.82/0.96/0.995 | 0.826/0.965/0.9955 | yes |
| Completion lift, quarter spend | +1.27% | ~+1.3% | yes |
| Structural chain growth / net sales | 1.30% / 1,412.5 | 1.27% / 1,412.0 | yes |
| Record RMSE, FY22 Q1 to FY25 Q3 | 0.70 | 0.72 (bias -0.1) | yes |
| Regression on panel's own mix | 6.26% / 1,481.6 | 1,465 to 1,481 | yes |
| Hurried RMSE / Q3 FY25 miss | 1.50 / 3.31 | 1.47 to 1.60 / 2.6 to 3.3 | yes |
| Licensed step in bridge | -1.32 | -1.68 delivered base; ~-1.31 after completion | order dependent |
| PL share carried to Q4 | 17.00 | 16.9 | yes |
| Regional growth NE/SE/MW/W | -1.45/16.98/0.44/10.30 | -1.4/16.7/0.0/9.8 (age not matched) | broadly |

## Competing answers that survived
- Range calibrated by regression RMSE 1.15 to 1.5 on the PL-adjusted models: centre ~1,425, range ~1,390 to 1,455. Top above the street, so "no position". Closing rule: none shipped; the structural chain is the golden's method but the prompt does not pin it.
- Bridge in a different order: licensed -1.68 against golden band -1.62 to -1.00 (outside). Closing rule: none; the order is the answer block's, not the prompt's.
- Private-label carry (average against last step, 16.9 against 17.0): inside the band, does not move the call.

## Spec gates (checked by me on the unzipped bundle and metadata.json)
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Usable files | 10 or more | 10 | yes |
| File categories | 2 or more | spreadsheet (csv, xlsx), text (txt, pdf) | yes |
| Large messy CSVs | 20,000+ rows, and one of 10 to 20 pages | panel 110,040 rows; descriptor detail 2,820 rows (about 56 printed pages) | yes |
| Distractors in metadata.json | 2 or more, unlabelled in the ZIP | appmetric_bmh_app_daily.csv, kestrel_web_visits_bmh_weekly.csv; no label in the ZIP | yes |
| Distractors relevant, unused | yes | web visits reproduce nothing graded; the thread named neither as carrying a result | yes |
| Deliverables | 1 to 3, all in the golden | xlsx and docx, both in golden/ | yes |
| Asks | multi-dimensional, units stated, no rounding dictated | 5 asks, units in the sentence, no rounding in the prompt | yes |
| Answer shape | one of fourteen, 4 or more results | forecast with bands plus a bridge and a record; 9 results in the note | yes |
| Golden ZIP | exactly the requested files | golden/ holds the two files (golden.zip not opened) | yes |
| Realism / LLM tell | none | not checked beyond the thread's hygiene PASS | not assessed |

## Gate G reconciliation
Thread: mechanism forecasting (decomposition_attribution), stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. The note's hidden factor record (KS-06 exit, regional skew, private-label fall) agrees: all constructed, all across the data in every quarter, none a sole defect. KS-06 and the licensed shops are filed rather than hidden. No conflict on mechanism or family.
Conflicts with the note:
- The note's closure claim (rivals keep the top at 1,420.1 to 1,439.7) fails against the thread's regression-calibrated range, whose top is ~1,455.
- The thread's single-sentence help (private-label fall plus regional skew) rescues about 2 of 7; the note's `Largest single hint:` says 1 of 9, which is not contradicted at the third.
- Declared distractors: neither was named as carrying a result.

## Stump power (Gate F)
Hurried read (regression on the panel's own mix, 1,481.6, or the desk's Q3 model, 1,473.9) goes long or beyond the street, and the thread confirmed the Q3 FY25 miss of about 3 points is visible. Results the thread reached with standard method: licensed share, completion, same-age comparable growth (R1 to R3), and it found the private-label term and the regional skew itself. The note's careful-but-hurried column leaves R4 to R9 missed; the thread, doing careful work, found both corrections, so the runs may earn more than the note's 3 of 9.

## Findings, ranked
1. Range top is method dependent (regression-calibrated ~1,455 against structural 1,425): the call is not closed against a defensible rival.
2. Bridge order unpinned; licensed step -1.68 against band -1.62 to -1.00.
3. Effort grades: thread gave quick 2, careful 4, thorough 7 of 7. Careful at 4/7 is more than a third, where the note's table has 3/9 and separates the columns. Result count differs (7 against 9). Flag for the main thread's effort test.
4. The note's regional and private-label factors are well spread, not deciding-units-only; no one_thing finding.

## Gate H line
domain: pass; layers: pass; results: 7 graded across 5 areas (thread's count; the note lists 9); one_thing: none; effort: quick 2, careful 4, thorough 7 of 7 (careful above a third); one_fact: "the panel holds no private-label cards and their share is falling, and the panel skews to the fast regions" rescues about 2 of 7 (count of one-fact sentences: 1, within the third).

## Next action for the author
In the answer block and rubric, state the bridge order and grade each adjustment order-independently (or widen the licensed and baseline bands), and pin the range method (say that the structural chain's record is the one the range is built from, and add the regression-calibrated 1,455 top to the fork table with a shipped fact that rules it out, or widen the call's closure). Panel and files stay byte-identical. Re-judge once after the fix. Do not edit the prompt unless the fork cannot be closed in the blocks.
