# determinism-check report, task9 (architecture 7), 2026-11-08, pass 2 on target.zip 7c395ae0

Pass 1 (bed0980b, FIX_NOW) is determinism_check_report_pass1.md. This is the one re-judge after the fix. The main session spawned the single isolated judge (general-purpose, sonnet, medium) from my brief /tmp/determinism-check-task9-1794167282/judge_brief.md; its verdict is /tmp/determinism-check-task9-1794167282/verdict.md.

## Verdict
DETERMINISTIC (no SOLUTION_WRONG).
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection (with forecasting), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The call, buy neither, is forced. MP-RN-2 2.1, 2.2 and 4.2 require standings and recoveries correlated as far as the record shows; the record shows clustering by sponsor house and recovery tied to the house's year, not the economy's. Every house-linked estimator keeps both notes over 1 per cent. The rivals that buy Kestrel Lane (no house factor, one average loss, economy-linked recovery) or Ostvale (co-defaults counted among the note's own loans) are separated by shipped data (whole-book counts, median 13 at risk, against Ostvale's 1 to 4 per house). Pass 1's fork is closed: both notes now reconcile with par less stated enhancement.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Defaults | 578 | 578, each once, matches 578 workout rows | yes |
| Company-years at risk | 16,712 | 20,590 loan-years (different at-risk definition) | no, immaterial to the call |
| Mean closed 2008-2019 loss | 42.7 | 43.0 after unit fix | yes (noise) |
| Recovery by co-defaults, lone / 3+ | 74.9 / 44.1 | 72.3 / 44.3 (cruder house join, 79 houses) | direction and size |
| Houses; KLCP, Ostvale spread | 80; 7 houses, 66 houses | 79; 7 houses of 11 to 13 loans, about 60 to 66 houses of 1 to 4 | yes |
| Kestrel note size | 1,597.5 (85 per cent) | 1,597.6 | yes |
| Ostvale note size | 1,612.1 (87 per cent) | 1,612.1 | yes (pass 1 clash closed) |
| Kestrel five-year chance | 3.9 | 3.2 to 3.3 (40k to 150k paths) | inside band 1.5 to 4.0 |
| Ostvale five-year chance | 7.8 | 6.7 to 6.8 | inside band 2.3 to 7.8 |
| Expected credit loss K / O | 5.7 / 8.2 | 5.6 / 7.9 | yes (noise) |
| Subordination for 1 and 0.5 per cent, K / O | 20, 22 / 17, 18 | 19, 21 / 17, 18 | within one point |
| Year-end chances | as in CSV | within 0.1 to 0.6 of golden | yes (noise) |
| Rival: house factor, one average loss | 0.7 / 6.2 | 0.57 / 5.3 | buys Kestrel |
| Rival: own-loan co-defaults | 1.8 / 0.1 | 1.4 / 0.17 | buys Ostvale |

## Competing answers that survived
None that flips the call. Open workouts: fitting on all closed workouts gives 3.1 and 4.8, still neither. Own-loan counting is ruled out by named data (at-risk counts per house-year), an analytical error not a fork.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Usable files | 10 or more | 13 | yes |
| Categories | 2 or more | spreadsheet, text (csv x6, xlsx x3, pdf x3, json x1) | yes |
| Large messy CSVs | 20,000 rows; 10 to 20 pages | Lenderbase 73,066 rows; Dealtrail 8,858 and LEI 4,485 rows | yes |
| Distractors | 2 or more in metadata.json, unlabelled in ZIP | Euribor curve and PHL cashflows named; none labelled in ZIP | yes |
| Deliverables | 1 to 3, all in golden | 2; golden.zip holds exactly the docx and csv | yes |
| Asks | multi-dimensional, unit and rounding stated | yes | yes |
| Answer shape | many gradable cells downstream of deep step | chances, ECL, subordinations, chart, 10-row table | yes |
| Realism, no build tells | none | none seen by judge (golden docx not read by me) | yes |

## Gate G reconciliation
Judge: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note: severity tied to a latent shared shock at the owner's whole-book grain, no decoy, no replay, not semantics. They agree. The judge did not name a declared distractor as the surface read. No mismatch. Gate G passes.

Gate H line: domain pass; layers pass (L1 mixed units, name joins, resubmissions, owner tracing; L2 dependence and recovery modelling); decisive_step analytical; chain 5 inferences (house-year clustering, closed-cohort recovery link with censoring, shock inference at whole-book grain, joint simulation); one_fact none (the house-year hint still leaves shock inference, censoring and simulation). Matches the design note's domain, analyst and one-fact tests. The golden is not the field's standard method (the standard copula buys Kestrel Lane), so the analytical class is not an artefact of a textbook route.

## Stump power (Gate F)
Strong on paper. Three self-consistent wrong routes exist (standard copula 0.1, house factor with one average loss 0.7, own-loan co-default table buying Ostvale). No single hint makes the correct route routine. Weighed by the main session against the design note's ladder; no solver was run.

## Findings, ranked
1. Residual, not blocking: the one-decimal chances and whole-per-cent subordinations in asks 2 to 4 and 6 are estimator-dependent inside the stated bands (Kestrel 20 and 22 against the judge's 19 and 21). The rubric should accept values inside the bands where the comparison to 1 per cent is the same.
2. The judge's simulation was approximate (40k to 150k paths); the 1,000,000-path figures remain the author's own, supported by figures_check.py.
3. Company-year at-risk count differs by definition (16,712 against 20,590); immaterial to the call.

## Next action for the author
Proceed to stage 5 on target.zip 7c395ae0 (no repair required). Optionally, state a tolerance for the point estimates when editing the rubric.
