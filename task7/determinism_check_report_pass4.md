# determinism-check report, task7, 2026-11-08 (pass 4)

## Verdict
DETERMINISTIC (the earlier SOLUTION_WRONG-minor, an unreproduced 211 denominator, is closed by wording; no rounded figure ever moved)
**Disposition:** APPROVE (the FIX_NOW is applied; no re-judge, one thread only)
**Stumping type:** mechanism: decomposition_attribution / statistical_rigor (contagion measured against a matched baseline) feeding binding_constraint, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
One thread (verdict at /tmp/determinism-check-task7-p4/verdict.md) recomputed the call and found the own-expected-loss route (Kinloch + Ridgeway, NZ$3,000,000) is the insufficient one. The ledger, register and 2026 run force Matai's 8 dependants and Ridgeway's 1, the 13/31 event study against a healthy-payer control, and so Kinloch + Matai at NZ$3,350,000. Both fall-backs and all five envelope rows reproduced. Every reading of "were it to turn its package down" (re-solve without the borrower, swap only the package, keep the package out of the pool) gives the same set and value. No envelope has a tie; whole-package and the 50,000 rounding are clean. Margins are thin but hold: 6.5m leads by 46k, 4.5m by 31k, for any uplift above about 0.386, and every control variant tried lands at 0.395 to 0.397.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Own EL Kinloch / Ridgeway / Matai | 1,593,000 / 1,422,000 / 817,000 | 1,592,644 / 1,421,988 / 817,175 | yes |
| Dependants Matai / Ridgeway | 8 / 1 | 8 / 1 (threshold 10 to 50 per cent identical) | yes |
| Event study | 13 of 31 | 13 of 31 (thresholds 10 to 45, horizons 9 to 18 identical) | yes |
| Control | 5 of 211 | 5 of 202 to 219 across variants (uplift 0.3951 to 0.3966) | rounded outputs yes; 211 exact not landed by the judge |
| Matai package | 1,750,000 | 1,750,742 | yes |
| Ridgeway package | 1,450,000 | 1,465,366 (nearest 50,000 is 1,450,000) | yes |
| 6.0m choice | Kinloch + Matai 3,350,000 | 3,343,386; next 3,216,108 | yes |
| Fall-backs | 3,200,000 / 3,050,000 | 3,216,108 / 3,058,010 | yes |
| Envelopes 4.5 to 6.5m | 2.20 / 2.45 / 3.20 / 3.35 / 3.45m | 2,190,477 / 2,444,715 / 3,216,108 / 3,343,386 / 3,445,001 | yes |

## Competing answers that survived
- Control against the less dependent payees of the same failing payers: uplift about 0.318, 6.0m total 3,150,000 and sheet 2 changes at four envelopes. Closed after the judge: Step 4 now carries the sentence that these borrowers are no control, and design note row SF12 files the closure with the data separating it (their default rate 10.2 per cent against 2.4 per cent for payees of surviving payers; dependants' own PDs 2.0 to 2.9 per cent agree with 5 of 211), asserted in generator/checks.py. Residual: a causal reviewer could still argue the dose comparison; the data rejects it and the golden says why.
- Uncontrolled 13/31 (0.419): same sets, some totals 50,000 higher. Ruled out by the filed comparison in Step 4/SF12.
- Own-EL ranking: the rejected insufficient route, not a rival.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Usable files / categories | 10+ / 2+ | 16 / 3 (CSV x11, PDF x4, XLSX x2), light mix | yes |
| Large messy files | CSV 20,000+ rows; CSV 10 to 20 pages | transactions 281,664 rows; crosswalk 726 and 2026 run 593 rows (about 11 to 14 printed pages) | yes (second file near the floor) |
| Distractors in metadata.json | 2+, unlabelled in ZIP | 6 named, not labelled in the ZIP | yes |
| Distractor unused yet weighable | yes | appetite PDF, property index, titles, security register, companies register, regional indicators; none answers the graded quantity | yes (judge) |
| Deliverables | 1 to 3, all in golden | xlsx + docx, both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | per-borrower fall-backs plus five-row envelope curve; NZ dollars, nearest 50,000 | yes |
| Answer shape with many gradable cells downstream of deep step | yes | choice, 2 fall-back rows, 5 envelope rows, all downstream of the uplift | yes |
| Golden ZIP exactly the requested files | yes | the two requested files | yes |
| Not LLM-looking / real work product | yes | judge found no provenance leak; realism sweep not re-run here | yes (not re-tested) |

## Gate G reconciliation
Thread: mechanism decomposition_attribution / statistical_rigor into binding_constraint; stumping_family analytical_non_defect; surface_read_dependency no; sole_data_defect no. No distractor carries the task. Gate G: PASS. The thread names the difficulty as discovering that dependence exists (nothing in the prompt names it) and then choosing the control. I did not re-read the card fields beyond the design note's one-fact and SF12 rows; no mismatch seen against the one-fact test at design note line 115.
Gate H: domain pass (credit risk, IFRS 9 expected loss, workout intake); layers pass (account-number formats and crosswalk, loan versus deposit default references, then the uplift against a clean control); decisive_step analytical; chain 5 inferences, judgment = control group for payer-failure contagion; one_fact: "a Matai package also protects its dependants, who default about 40 points more often when Matai fails" still leaves ledger resolution, event study, control choice and the knapsack, so not routine.

## Stump power (Gate F)
Good on paper. The textbook own-EL route lands on NZ$3,000,000 with Ridgeway and a wrong sheet 2; discovery of the dependants is the hard part, and the control choice plus the knapsack carry the rest. The uncontrolled rate reaches the right set but misses rounded figures. The platform's two runs measure it.

## Findings, ranked
1. (Closed) 5-of-211 rule unstated: Step 4 now states it exactly (either IFRS 9 run or the register, performing at year start, first-quarter receipts, 30 per cent or more of prior calendar-year receipts, own-account transfers and Ruahine lending out, payer neither in default at start nor defaulting during the year).
2. (Closed) Same-payer low-share comparison: SF12 and Step 4 close it.
3. Residual, minor: the judge never landed exactly 211 (best readings 202 to 219) and could not test the new wording, since no second thread runs. Rounded outputs are insensitive. The design note's SF12 says 6 of 61 where the judge counted 6 of 59; neither moves the call. The author should confirm generator/checks.py asserts 5 of 211 and 6 of 61 under the stated rules.
4. Thin margins at 6.5m (46k) and 4.5m (31k) hold for any uplift above about 0.386.

## Next action for the author
Run the generator checks to confirm 5 of 211 and 6 of 61 under the stated rule, then proceed to the platform.
