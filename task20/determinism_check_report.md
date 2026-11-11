# determinism-check report, task20, 2026-11-11

## Verdict
DETERMINISTIC on the estimate, the lower range edge and the call; open forks on the Ask 3 bridge lines and the Ask 2 count. No SOLUTION_WRONG.
**Disposition:** FIX_NOW (rubric/golden bands only; no pack or prompt change)
**Stumping type:** mechanism: decomposition_attribution (with forecasting of the private-label share and deposits), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

One thread (sonnet, medium) ran on judge_brief.md and kept the order: own_derivation.md was written before graded_blocks.md was opened. It ran under the main session's spawn, not mine (my runtime had no Agent tool).

## Why
The thread built its own chain from the files and got USD 1,430.8 million (-1.2%), range about 1,412 to 1,450, short. Its sensitivity grid (private-label share 16.2 to 17.2, bridge residual 0 to 1.0, deposit lag 8 or 9 weeks, wholesale 13 to 26) stayed at or under about 1,447, below the street (mean 1,484.0, median 1,482.4, lowest broker 1,472.7). The call is forced. The unpinned parts are what Ask 3 means by "each step" (its definition and order) and the Ask 2 count.

## Recomputation ledger (first pass, own_derivation.md, against the stated bands)
| Figure | Golden (band) | Thread's first pass | Inside band |
|---|---|---|---|
| Net sales | 1,439.5 (1,430.4 to 1,455.2) | 1,430.8 | yes, by 0.4 |
| Growth | -0.63% | -1.23% | yes (-1.26 to +0.45) |
| Range low | 1,418.6 (1,406.3 to 1,430.1) | about 1,412 | yes |
| Range high | 1,460.3 (1,453.8 to 1,481.9) | about 1,450 | NO, 3.8 below the band |
| Call | short | short | yes |
| Latest weeks completed | +1.21 (0.91 to 1.87) | +1.6 on retail | yes |
| Licensed shops and cafes out | -0.57 (-1.04 to -0.27) | about -0.6 | yes |
| Company regional mix | -4.48 (-5.36 to -2.96) | -4.6 | yes |
| Private-label share carried | 17.00 (16.60 to 17.80) | 16.7 | yes |
| Bank-card share | -5.83 (-6.36 to -4.17) | -5.2 | yes |
| Revenue on delivery | -7.33 (-9.75 to -6.45) | -7.7 | yes |
| Wholesale run rate | 17.7 (16.7 to 19.5) | 18.2 | yes |
| Wholesale step | -2.47 (-3.41 to -2.17) | -2.4 | yes |
| Delivered panel, every issuer | -8.90 (-9.20 to -8.60) | not stated (started with KS-06 dropped) | not tested |
| Issuers in both years, cards of the same age | +27.74 (27.08 to 28.21) | not reproduced as a step (age-matched +21.0% against +20.45% unmatched) | no (definition and order differ) |
| Closing deposits | 318.9 (307.8 to 326.7) | not computed as a balance; lag method implies about 8.5 weeks | not tested |
| Record: RMSE 1.12 (0.89 to 1.59), Q3 miss 1.04 (0.38 to 1.69), 13 of 15 inside | | not computed; its own rolling check gave 8 of 9 (FY23 Q3 to FY25 Q3), miss FY24 Q1 | not tested; the count is unbanded |

Reproduced from the bundle: street mean and median, base 1,448.6, wholesale 52.5, deposits 210.6, made-to-order share 38.9% against 29.0%, fiscal 2024 region weights, Larkhill's Q3 per-card 11.83 (exact), wholesale median of the last 8 quarters 17.7.

## Competing answers that survived
1. **Ask 3 order and definition.** The bridge values depend on the order and on which steps are named. Starting from the delivered panel with KS-06 (-8.90) or from common issuers changes the first lines entirely. Rule that would close it: grade by named step with bands that hold in either order, plus the start-to-end reconciliation.
2. **Ask 2 count.** "13 of 15 inside" has no band, and the past-quarter range convention is not filed (the golden uses in-sample RMSE; a rolling record gives other counts). The delivery history only covers August 2025 onward. Rule: band the count (for example 12 to 14) and state the convention.
3. **Range top.** A defensible rival record gives a top of about 1,450, below the stated 1,453.8 floor. The call does not change.
4. **Street figure.** Mean or median is not pinned. The call is the same either way.
5. **Wholesale repeat.** Repeating 52.5 gives 1,465 to 1,475, still short. The data (other Q4s at 14 to 16, FY25 Q1 to Q3 at 17.5 to 19.1) rule it out, so named data closes it.

## Spec gates (checked by me on the unzipped bundle)
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Usable files | 10 or more | 10 | yes |
| Categories | 2 or more | CSV, xlsx, PDF, txt (3 categories: spreadsheet, text, plus the document) | yes |
| Large CSVs | one of 20,000 rows or more, one of 10 to 20 printed pages or more | panel 110,040 rows; descriptor detail 3,481 rows, well past 10 pages | yes |
| Distractors in metadata.json | 2 or more, unlabelled in the ZIP | appmetric_bmh_app_daily.csv and kestrel_web_visits_bmh_weekly.csv; no label in the file names | yes |
| Distractors weigh but are unused | | the thread found both unused; web visits hold up through the holiday while purchases per visit fall | yes |
| Deliverables | 1 to 3 | 2 (xlsx, docx); golden.zip holds exactly these | yes |
| Asks and units | multi-dimensional, units stated, no rounding instruction | the prompt states USD million, points of growth and 80 per cent | yes |
| Answer shape | four or more checkable results | forecast with bands, record and bridge, 9 results in the note | yes |
| Realism | not LLM-looking | the thread found no authoring language; the 10-K excerpt is a labelled compiled desk copy | yes |

## Gate G reconciliation
`mechanism: decomposition_attribution`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. This matches the note's chain (modeling, decomposition, validation, forecasting). The note's `## Hidden factor record` says the December made-to-order event recurs every year (lifts of 10, 14, 0, 3 and 60%). The thread's descriptor read shows the made-to-order share steady at 25.3 to 26.2% for five years, then 27.6% in November and 35.1% in December and January. That puts the large event only in the deciding quarter. This is the exposure under the house rule ("a constructed factor sitting only in the deciding units is refused"). The note's "no" for only-in-deciding-units needs checking against the generator's lifts, because the 0 and 3% years are immaterial. The build survives only because region mix, tender share, issuer set, completion, licensed growth and wholesale each carry weight across the chain, and the thread rates it borderline-pass.

## Gate H
domain: pass; layers: pass; results: 8 to 9 graded across 6 areas; one_thing: borderline, shallow_hidden_factor risk (the December event; neither deep step alone flips the call, because either alone leaves the range across the street); effort (the thread's grades, not measured): quick 2, careful 5, thorough 8 of 8; one_fact: "the December custom orders are still undelivered deposits" rescues 3 of 8 (estimate, deposit step, call).

## Stump power (Gate F)
Mixed. The 10-K excerpt names revenue recognition, licensed shops and the private-label decline, and the bulletin names the issuer change and provisional weeks, so a careful run will list the corrections. The quantification is what stumps. The deposit balance and window, wholesale at run rate, and the record are where a hurried run loses. Skipping deposits gives about 1,541.8 or a range of 1,452.6 to 1,497.8 across the street. Keeping last year's wholesale gives 1,475.

The textbook parts (region re-weight, tender share, completion) were reached by the thread in one look and sit within their bands. These are results the runs will earn: R1 (apart from the age-matched step), R2, R3 and the licensed and completion lines.

## Findings, ranked
1. Reconcile the note with the thread on the effort test. The thread has careful at 5 of 8 against the note's 4 of 9, and the one-fact at 3 of 8 against the note's 1 of 9. Both exceed the note's claims and neither breaks the third-of-results line outright. The careful count is above a third, so the main thread must weigh it against the note's table.
2. Ask 3 values are order and definition dependent (fork 1).
3. The Ask 2 count is unbanded and the past-quarter convention is unfiled (fork 2).
4. The Ask 1 range-top band floor (1,453.8) excludes a defensible rival record (top about 1,450). This is Gate C on that result. Widen the floor down to about 1,449.
5. The December event's recurrence (see Gate G) needs the generator's lifts checked.

## Next action for the author
Edit the answer blocks and golden bands, with no data or prompt change: band the Ask 3 lines order-independently with the reconciling sum, band the Ask 2 count (12 to 14 of 15) and state the convention, name the street convention (mean 1,484.0; median 1,482.4 gives the same call), widen the Ask 1 top band down to about 1,449, and confirm the December event lifts in the generator.
