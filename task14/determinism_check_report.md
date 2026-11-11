# determinism-check report, task14, 2026-11-11 (pass 1)

Pass 1 was judged on the earlier submission.md and bundle (submission figures such as 68,905 held and 14,948 re-let, 4 asks-blocks as then filed). The design note now records a rebuild answering this pass's FIX_NOW findings (held counts 68,988 and re-let 14,968; no address carries two property identifiers; "held" became "in place"; estimators ranked on independent data; December rivals ranked by back-tests; the split moved to the forecast's drivers). A second pass runs separately on the rebuilt bundle. No target.zip existed; target/ was copied fresh to /tmp/determinism-check-task14-071154/target/. Thread outputs: verdict.md and own_derivation.md in that folder. The thread kept the order (derived first, then opened graded_blocks.md).

## Verdict
NOT_DETERMINISTIC (competing_defensible_answer / margin_or_boundary_fragility); SOLUTION_WRONG not found (direction and most structure reproduce).
**Disposition:** FIX_NOW (confined to the generator/answer blocks); SEND_BACK if December 3.1 +-0.1 must stay without a pin.
**Stumping type:** mechanism: method_or_model_selection (imputation of unrecorded rises) plus forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Registers record a rent change only when an additional bond is lodged. A literal record-only reading gives 6.35 (2023Q4), 5.37 (2025Q3), 4.09 (2026Q3), continuing +1.41 with 20.1 per cent rising, re-lets +13.6, against the golden 7.5, 5.7, 4.0, 2.5, 62.4, 9.4. The golden needs unrecorded rises imputed from the survey; the two imputation estimators (anniversary rises carried from starting rent; latest recorded rent grown at the survey rate) were not ranked by independent data (the second gives 3.9 for Sep 2026, inside the 0.15 band, out of band for 2023-24). Dwelling identity was a second fork (418 apartment addresses with two property ids: held 68,498 vs 68,905, re-lets 14,725 vs 14,948, Hallam Central 2,902 vs 2,975). December 3.1 was stated to +-0.1 but record-only nowcast with past-error correction gave 3.4 to 3.8, and the 3.4 and 3.5 rivals were rejected by argument, not a named data check.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Migrated rent/start equal legacy record | 57,124 | 57,124 of 57,124 | yes |
| Legacy exact-duplicate rows | (rule) | 441 | yes |
| LL15069488 Dec reviews 2023-25 | 6.2, 4.4, 6.1 | median 6.2, 4.4, 6.1 = CPI + 1.0 | yes |
| LL36031376 Nov reviews | 5.7, 3.9, 5.6, 2.7 (2026) | same, CPI + 0.5; 1,942 top-ups | yes |
| Continuing, Sep25 to Sep26 | 2.5 / 62.4 | 2.3 / 60.6 (survey basis) | plausible |
| National 2023Q4 / 2024Q1 / 2025Q3 / 2026Q3 | 7.5 / 7.4 / 5.7 / 4.0 | 6.35 / 6.35 / 5.37 / 4.09 (literal, record-only) | no |
| Held 30 Sep 2026 | 68,905 | 68,498 | no (outside 0.3%) |
| Re-let in year | 14,948 | 14,725 | inside 2%, HC outside |
| Re-let rise | 9.4 | 13.6 | no |
| December national | 3.1 (3.0-3.2) | about 3.4-3.8 | no |

## Competing answers that survived
- Imputation estimator for unrecorded rises: 4.0 vs 3.9 vs 3.7 for Sep 2026; unranked by independent data.
- Dwelling key: property_id first vs address; held as tenancies vs dwellings (418 collisions).
- Legacy additional-bond effective date (record date vs earlier); 32 per cent of top-ups missing rent_effective_from.
- Contribution weights for the decomposition.
- December: 3.1 vs 3.4 vs 3.5 vs about 3.8, rejected by argument only.
(The design note records each as answered in the rebuild; unverified here.)

## Spec gates
Checked against the pass-1 bundle (the 12 files in target/).
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Usable files | 10+ | 12 | yes |
| File categories | 2+ | csv, xlsx (spreadsheet) and pdf (text): 2 | yes |
| Large CSV 20,000+ rows | 1 | bond events 247,228 rows; legacy register 239,767 | yes |
| Long messy CSV 10-20 printed pages+ | 1 | rent survey 116,926 rows; legacy 239,767 | yes |
| metadata.json names 2+ distractors | 2+ | 3 (house price index, building consents, rent index survey workbook); none labelled inside the pack (grep of target/ for distractor/trap/generator found nothing) | yes |
| Distractor unused yet weighty, not answering a graded quantity | yes | judge saw them as unused; I did not independently test that the index survey workbook cannot reproduce a graded figure | not verified |
| 1-3 deliverables, all in golden | yes | 2 (xlsx, pptx); golden not re-opened this pass | yes (by submission) |
| Asks multi-dimensional, units stated, no rounding dictated | yes | prompt 756 chars, no rounding or method named | yes |
| Answer shape, 4+ checkable results | yes | national series with bands, flagged-style forecast with range and driver split; 7 asks plus recommendation | yes |
| Nothing LLM-looking; golden realism | yes | judge saw no authoring leakage; golden not read | partial |

## Gate G reconciliation
Judge: mechanism method_or_model_selection plus forecasting; stumping_family analytical_non_defect; surface_read_dependency no; sole_data_defect no. Note's Hidden factor record lists five constructed factors, all marked "no" for only-in-deciding-units, and claims "modelling" for the unlodged-rises fix. The judge found the register-misses-rises fact reachable by one cross-file look and carrying about 4 of 7 results, which is the shallow hidden factor risk, but not confined to deciding units. No shipped artifact was seen ranking candidates wrongly (no finding raised). The operators' CPI review rule is constructed, sits in two landlords and decides the December headline; the note's own record keeps it. Classification: Gate G no finding raised; Gate C/A fragility on imputation and dwelling identity (fixed in the rebuild per the note, to be re-judged).

## Stump power (Gate F)
Real and spread across conformance, imputation, re-let pricing, decomposition and nowcast. Hurried column is the record-only measure (1.4 vs 2.5 continuing, 13.6 vs 9.4 re-let, 6.35 vs 7.5 peak). The careful run likely loses continuing share, re-let rise, back series and December. The note's effort table (careful pass earns R1, R2, R4, half of R5 and R7b) is consistent with that. Results reached by standard method with no judgment: stock count and the address match (R1, R2), earned by a careful run.

## Gate H line
domain: pass; layers: pass; results: 7 asks plus recommendation across 6 areas; one_thing: shallow_hidden_factor (partial: register misses rises; operators' CPI rule for December); effort: quick 2, careful 4, thorough 7 of 7; one_fact: "the register records only some rent rises; use the survey to fill the rest" rescues about 4 of 7 (asks 1, 4, 5, 6), above one third; the operators' sentence rescues 2 of 7.

## Findings, ranked
1. Imputation estimators not independently ranked (note answers: ranked on dwellings both sources hold, within 0.2 per cent of reported rents).
2. Dwelling identity fork (note answers: no address now carries two property identifiers; "in place").
3. December rivals rejected by argument (note answers: ranked by back-tests on three earlier Decembers).
4. One-fact exceeds a third (judge 4 of 7; note answers: split moved to the forecast's drivers, claims at most 3 of 9).
5. Reconciliation with note: note's own "Largest single hint" says 3 of 9 (operators 2 of 9, unlodged rises 3 of 9 at most), the judge reads 4 of 7 for the unlodged-rises sentence; the difference is the result count and whether the split counted, both changed by the rebuild. Judge's effort grades (quick 2 of 7 vs note's quick Missed on all nine; careful 4 vs note's 3 right plus 2 partial) put the quick pass above the note's. Quick pass at 2 of 7 is under a third, so not a send-back trigger.

## Next action for the author
Run pass 2 of the judge on the rebuilt bundle and confirm the judge now reproduces the estimator ranking, the dwelling counts (68,988; 14,968) and December 3.1 without the pins being argued.
