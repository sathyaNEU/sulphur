# determinism-check report, task9, 2027-02-17 (run 2026-11-10; bundle sha256 prefix 29757c9b8be051ff)

## Verdict
NOT_DETERMINISTIC (governing label margin_or_boundary_fragility on the Ostvale side, shading into competing_defensible_answer). The Kestrel Lane side holds. Gates A, B, E pass; Gate C fails on Ostvale's chance of loss and on the whole-percent subordination asks.
**Disposition:** SEND_BACK. The fix changes what solvers see (standard text or prompt), so a rerun is required.
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
"Buy neither" needs both chances to exceed 1.0 per cent. Ostvale clears the line only through one fitted recovery slope (about 0.31 per unit of house-year shock) that has real estimation freedom. The golden's own rival, a link fitted on every closed workout, puts Ostvale at 0.77 per cent, which buys Ostvale. The design note closes it (SF8, SF17, closure axis 12) by saying MP-RN-2 4.1 "keeps the open workouts", but the judge read 4.1 as saying only that open workouts are included in the record. It gives no handling for an open workout with no recovery, and fitting the link on the 2008 to 2019 cohorts is a method argument (selection bias), not a filed rule. In the judge's cruder rebuild the Ostvale and Kestrel chances fall from about 1.6 to about 1.0 within two standard errors of the slope (0.22, SE 0.022; all-closed fit 0.17). The Ostvale band's low edge (1.1) sits 0.1 above the test line. This touches the recommendation and asks 1 to 6.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Defaults after conforming | 537 | 537 (= workout rows) | Yes |
| Loan-years at risk | 16,967 | 20,933 (join and window differences) | No, not pinned |
| Houses | 80 | 80 managers; 514 of 537 defaults carry one | Mostly |
| Kestrel tape / Ostvale tape | 7 houses x 14 / 2 each over about 63 houses | same | Yes |
| EUR par | term sheets | 1,854.1 and 1,922.3 | Yes |
| Same-house pair co-default | 0.61 vs 0.23 per cent | 0.42 vs 0.19 | Direction only |
| Five-sector yearly correlation | 0.63 vs 0.09; 2009 21.7 vs 4.6 | 0.62 vs 0.09; 20.1 vs 4.0 | Yes |
| Recovery, lone vs 3+ others | 74.7 / 38.3; mean loss 41.0 | 74.0 / 32.2; 40.8 | Close |
| Recovery slope on inferred shock | 0.313 | 0.22 (all-closed 0.17) | No |
| Chance of loss, Kestrel / Ostvale | 3.7 / 2.3 | 1.6 / 1.6 at slope 0.221; 3.0 / 3.3 at 0.313; 1.08 / 1.02 at 0.18; 0.75 / 0.72 at 0.15 | Qualitative only |
| Expected credit loss | 5.9 / 7.6 | 6.8 to 9.6 (crude sim) | No |

## Competing answers that survived
1. Open workouts (MP-RN-2 4.1, 3.4): link on the 2008 to 2019 closed cohorts (Ostvale 2.3, neither) vs link on all closed workouts (Ostvale 0.77, buy Ostvale). The shipped text does not say how an open workout enters.
2. Slope estimation: sound estimators span 2.3 to 4.0 (Kestrel) and 1.1 to 2.4 (Ostvale); the lower Ostvale edge is 0.1 above the line and the judge's own fits came within 0.02 to 0.08 of it.
3. Rating basis: tapes give the current rating, Lenderbase the rating at origination; the mapping is not filed.
4. Subordination asks and Table 3: tail quantiles rounded up to whole per cent; estimators spread over several points of par, so the figures rest on one fitted model. They are gradable only through the 20-variant band; the judge could not see that bands are filed.
Resolved, not forks: recovery units, duplicate submissions, mixed dates, status codes, name joins.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Usable files | 10 or more | 13 | Yes |
| Categories | 2 or more | spreadsheet (3 xlsx), text/CSV (6), PDF (3), JSON | Yes |
| Large CSV | 20,000 rows or more | lenderbase 74,356 rows (11.8 MB) | Yes |
| Second messy CSV | 10 to 20 printed pages or more | dealtrail 9,179 rows (1.5 MB), lei 4,641 rows, far over 20 pages | Yes |
| Distractors in metadata.json | 2 or more, none labelled in the ZIP | euribor curve, phl cashflows; file names and contents carry no label | Yes |
| Distractors unused yet weighable | arithmetic and a shipped fact rule it out | judge: interest excluded by 3.4; cashflows give no test figure | Yes |
| Deliverables | 1 to 3, all in golden | one docx, present in golden/ | Yes |
| Asks | multi-dimensional, unit and rounding stated | yes, in the prompt | Yes |
| Answer shape | one of the fourteen, 4 or more checkable results | allocation/defined-metric style scenario call with nine results (R1 to R9) | Yes |
| Golden = requested files | exactly | one file | Yes |
| Realism / LLM-read | none | file hygiene clean per judge; golden docx not opened by me | Not checked |
| Tolerances for rounded asks | filed bands | not verifiable from the shipped asks | Open |

## Gate G reconciliation
Judge: method_or_model_selection, analytical_non_defect, surface_read no, sole_data_defect no. Card stump_class "analytical" and the note's Hidden factor record (four constructed factors, none "only in deciding units", all marked keep) agree, so Gate G passes. Two points of tension: the judge found the five-sector loading sits wholly in the Ostvale book and the house-year effect in the Kestrel book (7 houses x 14), each visible in one group-by, which is the house rule's concern (a constructed factor in the deciding units), although the note records them across all 80 houses and 16 sectors; and the judge marks `one_thing: shallow_hidden_factor (borderline)` where the note claims difficulty throughout. Both are judgment calls for the main thread, not hard defects.

## Gate H line
domain: pass; layers: pass; results: 6 graded across 5 areas (judge) vs 9 in the note; one_thing: shallow_hidden_factor (borderline); effort: quick 1, careful 3, thorough 6 of 6 (judge) vs note 0 / 2 / 9 of 9; one_fact: "defaults and recoveries cluster in a sponsor house's year, and five sectors load on the economy" rescues about 3 of 6 (judge) vs note's Largest single hint 2 of 9.
Divergences that predict a send-back: the judge's careful pass (half) is above a third; its best single sentence rescues half, above the note's 2 of 9 and above the one-third limit; the Ostvale band's low edge (1.1) is too close to the line. The judge's quick-pass 1 of 6 is the recommendation or a component a hurried run can hit by luck, not a stated defect.

## Stump power (Gate F)
Quick routes are wrong: agencies' copula gives Kestrel Lane (0.01 vs 0.02), house route gives Ostvale, sector-only gives Kestrel Lane, pooled loading gives Ostvale. A run that stops at one strand files the wrong buy. Results a careful hurried run reaches by standard method: the house-year share (R1) and the expected loss with an average loss (R9 partly). The weakness is Gate C, not too-easy: the call rests on one fitted slope.

## Findings, ranked
1. Open-workout / link-sample fork (SF8, SF17) is closed only by a method argument, and it flips the call.
2. Ostvale band low edge 1.1 against the 1.0 line, and the judge's own fits reach 1.02 to 1.08.
3. Effort and one-fact grades exceed the note's table (careful 3 of 6, one sentence rescues 3 of 6).
4. Whole-per-cent subordination and one-decimal Table 3 cells have no filed tolerance the judge could see.
5. Rating basis mapping unfiled; loan-year count (16,967) not reproduced from the shipped files.

## Next action for the author
Edit the filed standard (or prompt) so it states how an open workout enters the recovery estimate, or which cohorts the link is fitted on, and whether tape ratings are current or at origination; or widen the Ostvale margin so both notes clear the line under the all-closed fit. Rebuild, then re-judge once.

Scratch: /tmp/determinism-check-task9-r024910/ (judge_brief.md, verdict.md).
