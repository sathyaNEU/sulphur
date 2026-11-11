# determinism-check report, task14, pass 2, 2026-11-11

Scope: pass 2 judged the pack and blocks as they stood in /tmp/determinism-check-task14-pass2b/ (target/ copy, prompt.txt, graded_blocks.md from submission.md after the register realism rebuild). The thread kept the order (own_derivation.md before graded_blocks.md). After the verdict was written, the main session applied the thread's three solution-only fixes in the generator without touching target/ or prompt.txt (design note, last Tried-and-rejected line): the back series band widened to 0.3, the December re-letting term sized in the Step-by-Step with the analog method's back-test, the continuing share's construction stated. This report records the verdict on the blocks the thread read; the fixed blocks have not been judged, and the one re-judge is spent.

## Verdict
DETERMINISTIC (Gates A to E hold on asks 1 to 5 and the structure of 7; the solution is not wrong). No SOLUTION_WRONG.
**Disposition:** FIX_NOW as the thread filed it (solution text only, no rerun). The three fixes are now applied but unjudged; see Findings 1 and 2 for what remains open.
**Stumping type:** mechanism: forecasting plus measurement-model correction (method selection on honest sources), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The definition (PS-2026-07, 2.2 to 2.5) and the files force the dwelling-level construction. The Rent Survey shows register rents 5 to 6 per cent below reported rents for small-landlord tenancies, growing with tenancy age, so the register-only reading (4.2 September, peak 6.4) is ruled out by named data and the survey-corrected reading (4.0, peak 7.5) is the one the files support. Counts, group figures, September and the operator rule all reproduce independently. The soft points are the back series' tolerance (fixed after) and the December central (3.1, band 0.1), where a competent analog forecast lands at 3.4.

## Recomputation ledger
(Golden figures are those the thread read; Penmarra 68,993 and 14,963 in the judged blocks.)
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Tenancies in place 30 Sep 2026, Penmarra | 68,993 | 68,995 | yes |
| By region (HC, HN, HE, HS, KC, MV, WS) | 12,737 / 11,099 / 11,242 / 8,982 / 8,951 / 8,045 / 7,937 | 12,738 / 11,099 / 11,242 / 8,982 / 8,951 / 8,046 / 7,937 | yes, within 1 |
| Dwellings re-let, Penmarra | 14,963 | 14,913 | yes (0.33 per cent, band 2) |
| Re-let by region | 2,985 / 3,959 / 2,144 / 1,525 / 1,728 / 1,333 / 1,289 | 2,976 / 3,955 / 2,139 / 1,512 / 1,719 / 1,327 / 1,285 | yes, all under 1 per cent |
| Re-let on property_id alone | 9,978 | 9,978 | exact |
| Register share of continuing tenancies with a rise | 20.6 | 20.6 | exact |
| Continuing tenancies, rent up | 2.5 | 2.54 | yes |
| Share of continuing with a rise | 62.4 | 63.9 (survey 60.7 small landlords, 84.5 operators); 62.4 only with the 59.0 version | yes, inside 2.0 (construction stated after) |
| Re-let dwellings, rent up | 9.4 | 9.56 | yes |
| Sep 2026 national / regions | 4.0; 4.4 4.4 3.9 4.1 3.7 3.2 3.9 | 4.06; 4.50 4.46 4.01 4.06 3.64 3.37 3.95 | yes (Midvale 0.17 off, band 0.25) |
| Contributions to Sep (continuing / re-let) | 1.94 / 2.06 | 1.99 / 2.08 | yes |
| National series 2022Q1 to 2026Q3 | 3.3 ... 7.5 ... 4.0 | 3.12 ... 7.48 ... 4.06 | 14 of 19 inside the then 0.15 band; 2022Q1 (0.18), 2022Q3 (0.30), 2022Q4 (0.24), 2026Q1 (0.20) outside; band now 0.3 |
| Register-only series | n/a | 4.2 at Sep, peak 6.4 | confirms the rival |
| Operator rule | LL15069488 1 Dec at CPI + 1.0 (6.2, 4.4, 6.1); LL36031376 1 Nov, 1,942 lodged at 2.7 | same in register; CPI file 5.2, 3.4, 5.1, 2.2 | yes |
| December 2026 national | 3.1 (3.0 to 3.2) | not reproduced to the band: analog 3.3 to 3.6 (central 3.4), run-rate extrapolation 3.7 to 3.8 | partly |

## Competing answers that survived
- December central: the golden's own named rivals 3.4 and 3.5 and the thread's analog (27 November reading plus prior-year Nov-to-Dec deltas of 0.39, 0.22, 0.30, adjusted for halved operator reviews and easing going rents) sit outside 3.0 to 3.2. The golden rules them out on named data (operator reviews halving, going rents easing, repeat-letting growth 5.4 to 4.2 per cent annualised), but the re-letting term is a model output, so 3.3 to 3.4 stays defensible. The design note's own analog reads 3.6 where the thread's reads 3.4, so the analog is itself a fork in how the deltas are adjusted. After the fix the steps size the term (about 1,190 December re-lettings at a 2.8 per cent margin against 10.1 and 8.1 in 2024 and 2025) and back-test the analog at up to 0.24 against the projection's 0.1. That is a rule-out by back-test, not by the files alone, and has not been re-judged.
- Back series 2022Q1, Q3, Q4 and 2026Q1: a survey-to-register ratio correction lands 0.18 to 0.30 off; band widened to 0.3 after, which is now loose enough to admit the register-only series' nearer quarters (3.17 vs 3.3, 3.90 vs 4.5 fails; 4.48 vs 5.3 fails), so the widening still excludes the register-only rival by 2022Q3 onward.
- Raw rents with decimal slips left in, blank effective dates read as event date, the published survey index (4.0 at September only, misses 2022 to 2024 by 0.2 to 0.7): all inside the band or ruled out by named data.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Usable files | 10 or more | 12 | yes |
| File categories | 2 or more | csv and xlsx (spreadsheet), pdf (text): 2 | yes |
| Large messy files | CSV of 20,000 rows or more, and a CSV of 10 to 20 printed pages or more | bond events 247,228 rows, legacy register 239,776, rent survey 116,926 | yes |
| Distractors in metadata.json, none labelled in the ZIP | 2 or more | 3 (house price index, building consents, published rents index workbook); neutral file names | yes |
| Distractors unused yet weighable | unused, ruled out by a shipped fact | thread found none carrying a result; the published index equals 4.0 at September only and is ruled out by the 2022 to 2024 quarters | yes, with a watch (Finding 5) |
| Deliverables | 1 to 3, all in the golden | 2 (xlsx, pptx), both in golden/, nothing extra | yes |
| Asks | multi-dimensional, units stated, no rounding dictated | prompt 803 characters, units stated, no rounding instruction | yes |
| Answer shape, 4 or more checkable results | one of the fourteen | forecast path with range and drivers plus a bridge; 9 results in the note | yes |
| Golden reads as a real work product | no LLM tells | golden workbook has a "Routes" sheet listing the rival constructions and their figures | watch (Finding 6) |

## Gate G reconciliation
Thread: mechanism forecasting plus measurement-model correction, family analytical_non_defect, surface_read_dependency no, sole_data_defect no. The register's unrecorded rises are constructed, but data-wide (every small-landlord tenancy, every year and region) and need a fitted correction against the survey. The design note's hidden factor record agrees: six factors, all "no" under only-in-deciding-units, fix depth modelling. Reconciled: Gate G PASS. One caution the note should keep: the thread rates the register understatement "shallow_hidden_factor risk only partially, mitigated".

## Gate H line
domain: pass; layers: pass; results: 7 graded across 6 areas (note: 9 results, 7 areas); one_thing: partial risk (register understatement), not decisive; effort: quick 2 of 7, careful 4 of 7, thorough 7 of 7 (note: 0 of 9, 4 of 9, 9 of 9); one_fact: "the register records only some rises; use the Survey's reported rents" rescues 3 of 7 (series, answers 4 and 5), the note counts 3 of 9 for its own largest hint.

## Stump power (Gate F)
Strong. A register-only run gives 4.2, peak 6.4, continuing 1.6, 20.6 per cent rising, re-let +13.4 and misses asks 1, 4, 5, 7 and the recommendation; counts (asks 2, 3) are earned by careful address work. Results the thread reached with the field's standard method and no judgment the data had to settle: the counts (R1, R2), the re-letting priced at the earlier day's rent (R4). The December point needs the operator-review rule and a forecast; the hurried run files 3.5 to 4.0.

## Findings, ranked
1. December central (R7, band 0.1): the thread's analog lands at 3.4, outside the band. The back-test sizing added after the judge is the only closing argument, and the note's own analog (3.6) differs from the thread's (3.4), so the analog method is itself unpinned. Not re-judged. The thread's alternative was a wider band (3.1 to 3.4 accepted); the main thread chose to keep 0.1.
2. Back series: 4 of 19 quarters were outside the 0.15 band for an honest correction; widened to 0.3 after. Unjudged.
3. Continuing share (62.4) reproduces only with the 59.0 small-landlord version; the construction is now stated. Unjudged.
4. One-fact count: the thread counts 3 of 7 (43 per cent), the note 3 of 9. R8 depends on R3 (September contributions), so the sentence may rescue R3, R4, R5 and R8, 4 of 9 (44 per cent), over a third. The main thread should settle whether R8 falls with R3 before the effort test is signed.
5. Distractor: the published rents index matches the graded September 4.0, ruled out only by the back quarters; acceptable but close.
6. Golden "Routes" sheet lists the rival constructions and their results (a tell of how the task was built, golden only, not shipped to solvers); consider moving it out of the golden for realism.
7. Effort grades: quick 2 of 7 against the note's 0 of 9 (28 per cent, under a third); careful pass 4 of 7 against 4 of 9 (the thread's careful run earns more of the smaller denominator).

## Next action for the author
Decide R7's band: either widen the December central to the width the unfixed analog forecast spans (3.1 to 3.4) or confirm in the generator that the sized re-letting term plus the back-test closes the 3.4 and 3.6 analogs on named data, then settle whether R8 falls with R3 for the one-fact count. No re-judge is licensed; the main thread weighs these against the effort test.
