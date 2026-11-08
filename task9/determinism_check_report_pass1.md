# determinism-check report, task9 (architecture 7), 2026-11-08, pass 1 on target.zip bed0980b

## Verdict
DETERMINISTIC (the call, buy neither, is forced; no SOLUTION_WRONG).
**Disposition:** FIX_NOW
**Stumping type:** mechanism: method_or_model_selection (dependence structure and recovery link, with censoring), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Process note: my runtime had no Agent tool, so the main session spawned the one isolated judge thread (general-purpose, sonnet, medium) from my brief (/tmp/determinism-check-task9-1794165705/judge_brief.md). Its verdict is /tmp/determinism-check-task9-1794165705/verdict.md. No second thread was run.

## Why
Read literally, MP-RN-2 2.1, 2.2, 4.1 and 4.2 send the solver to the Lenderbase and Dealtrail record, where the sponsor house's year clusters both defaults and recoveries. Every estimator that ties recovery to the house-year (1.5 to 4.0 per cent Kestrel Lane, 2.3 to 7.8 Ostvale) keeps both notes above 1 per cent. The rivals that buy Kestrel Lane (no house factor 0.1, one average loss 0.7, economy-linked recovery 0.2) or Ostvale (co-defaults counted among the note's own loans, 0.1 and 0.8) are ruled out by named data (whole-book counts, median 13 at risk, against Ostvale's 2 per house), not by taste. One term-sheet inconsistency (below) is the FIX_NOW item. It does not move the call.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Lenderbase rows, loans | 73,066 rows | 73,066 rows, 4,819 loans | yes |
| Defaults (D + Defaulted) | 578 | 345 + 233 = 578; workouts 578 (500 closed, 78 open) | yes |
| Houses | 80 | 80 (435 funds to 80 managers) | yes |
| KLCP tape | 98 loans, 7 houses, EUR 1,879 m | 98, 7 houses of 14, EUR 1,879.5 m | yes |
| Ostvale tape | 100 loans, 66 houses, EUR 1,853 m | 100, 66 houses of at most 2, EUR 1,852.9 m | yes |
| Kestrel Class A | 15.0 per cent subordination | 1,597.5 = 85.0 per cent of par | yes |
| Ostvale Class A | 13.0 per cent subordination | 1,575.0 = 85.0 per cent of par (reads 15.0) | NO, internal clash |
| House clustering (0.84 vs 0.25 per cent) | as stated | crude: 665 same-house-year pairs vs about 193 expected; direction and size consistent | direction only |
| Recovery by co-defaults (74.9 / 44.1) | as stated | 68.5, 56.6, 44.3, 43.4 across 0, 1, 2, 3+ (cruder match, unweighted) | gradient only |
| Probit, copula loadings, log-likelihoods, 3.9 / 7.8, 5.7 / 8.2, 20/22 and 17/18, CSV year-ends | as stated | not rebuilt | unverified (band logic only) |

## Competing answers that survived
1. Ostvale Class A is EUR 1,575.0 m (85.0 per cent of par, reads as 15.0 per cent subordination) while the clause and the golden say 13.0. Reading 15.0 lowers Ostvale's chance and changes asks 4, 5 and 6 (offered subordination, chart line, CSV column). The call holds. This is the FIX_NOW fork. The main session reports it is already fixing it (both term sheets now size Class A as par less the stated enhancement); the rebuilt cut is to be re-judged once.
2. One-decimal point figures (asks 2, 3, 4, 6) come from one estimator, while the submission itself states sound estimators span 1.5 to 4.0 and 2.3 to 7.8. These asks are deterministic within that band; the call and the ordering (Ostvale above Kestrel) hold throughout. Judged against the band and the call as instructed: not a flipping fork, but a grading-tolerance risk for the decimals.
3. Open workouts: 4.1 includes them, the golden fits on closed 2008 to 2019 cohorts. Licensed choice; a fit on every closed workout still gives 3.1 and 4.8, same call. Not a flip.
4. Own-loan co-default counting (0.1 / 0.8, buys Ostvale): excluded by data (V4 whole-book grain) and by the same default recovering differently by holder, not by a filed sentence. Accepted as the stump, not a fork.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Usable files | 10 or more | 13 | yes |
| Categories | 2 or more | spreadsheet (csv, xlsx), text (pdf, json) | yes |
| Large messy CSVs | 20,000 rows; 10 to 20 printed pages | Lenderbase 73,066 rows (11.5 MB); Dealtrail 8,858 rows and LEI 4,485 rows (many pages) | yes |
| Distractors in metadata.json | 2 or more, unlabelled in ZIP | euribor_forward_curve, phl_matching_portfolio_cashflows named; no labels in the ZIP. Judge also saw sector codes and ECB rates (only 31 Dec row used) as unused-ish files | yes |
| Distractors unused yet weighable | arithmetically plausible, ruled out by a shipped fact | the test is on principal loss alone (Euribor curve, benefit cashflows); no graded quantity answered by them | yes |
| Deliverables | 1 to 3, all in golden | 2 requested (docx, csv); golden.zip holds exactly those 2 | yes |
| Asks | multi-dimensional, unit and rounding stated | five-year chances, ECL, subordinations, chart, 10-row year table; unit and rounding in the prompt | yes |
| Answer shape | gradable cells downstream of deep step | per-note chances, ECL, two subordinations each, tail curve, 10 CSV cells | yes |
| Golden realism, no LLM or build tells | none | judge saw no authoring language in PDFs; dates coherent; fictional entities | yes (golden docx not independently read by me) |

## Gate G reconciliation
Gate G line: judge `mechanism: method_or_model_selection (dependence structure and recovery link, with censoring)`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. Design note: decisive step is a severity conditioned on a latent shared shock at the owner's whole-book grain (strategy label WORKS IN FORM, variance beyond sampling noise and correlated defaults), no decoy, no replay, not semantics. These match in substance: both name model selection for the recovery link and the grain of the shock. The judge did not name a declared distractor (Euribor curve, benefit cashflows) as the surface read. No mismatch. Gate G passes.

Gate H line: judge `domain: pass`, `layers: pass` (L1 mess: mixed codes, resubmissions, name-only joins, 0-1 vs percent recoveries, owner tracing; L2 dependence and recovery modelling), `decisive_step: analytical`, `chain: 5 inferences`, `one_fact: "defaults and recoveries cluster by sponsor house-year"` shortens but does not make routine. Design note's domain test, analyst test (strong analyst files Kestrel Lane at 0.7, field copula at 0.1) and one-fact test (the hint still leaves grain, latent shock, censoring and joint simulation) agree. The judge did not class the decisive step analytical merely because the golden is the field's standard method. The golden is not the standard method (the field's copula buys Kestrel Lane).

## Stump power (Gate F)
High on paper, per the judge. Two reasonable wrong buys exist (copula with one average loss buys Kestrel Lane; own-loan co-default table buys Ostvale), and only the whole-book latent house-year shock with censoring handled keeps both over 1 per cent. Caveat: MP-RN-2 4.2's sentence that recoveries are correlated narrows the field; the shock to correlate with is left to the data. The main session weighs this against the design note's ladder; no solver was run.

## Findings, ranked
1. FIX_NOW: Ostvale term sheet Class A (EUR 1,575.0 m, 85.0 per cent of par) contradicts the stated 13.0 per cent enhancement. Main session reports the generator fix is in progress; the rebuilt cut needs one re-judge.
2. Point figures in asks 2, 3, 4 and 6 sit inside an estimator band; a sound run may mismatch the decimals while right on the call. Consider whether rubric tolerance can be stated (the build cannot pin the estimator without spending the stump).
3. Not reproduced by the judge: the simulation, probit, copula loadings, exact clustering rates and the 74.9 / 44.1 levels (gradient and direction only). The author's figures_check.py is the source for these; they remain unverified in this pass.
4. Minor: file mtimes read Feb 2027, harmless.

## Next action for the author
Finish the generator fix so Ostvale's Class A equals par less 13.0 per cent (and Kestrel's less 15.0), rebuild, recheck that the golden figures (7.8 and the ask 4 to 6 values) still hold on the corrected sizing, then re-judge the rebuilt cut once.
