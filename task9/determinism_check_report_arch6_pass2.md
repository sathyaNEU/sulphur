# determinism-check report, task9, pass 2, 2026-11-08

## Verdict
DETERMINISTIC (no SOLUTION_WRONG)
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection (dependence structure; censored-outcome loss given default secondary), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no
Judged: target.zip 076bb4b7e87400b3 (carried the pass 1 fixes: 3.2 ageing, 3.4 LGD over every comparable default, LEIs from 2015, estimator band in the critical components). The main session since added one optional pin to 3.4 (a defaulted loan leaves the pool) and a metadata-only fix, and is rebuilding; no figure moves. That rebuild was not re-judged.

## Why
Read word for word, MP-RN-2 forces the call: five-year chance of any loss below 1.0 per cent (2.1), lower chance wins if both pass (2.2), dependence "as far as the record shows" (4.2). Rebuilt independently, the house-year dependence is the only structure the record identifies: Ostvale 0.54 per cent passes, Kestrel Lane 1.32 per cent fails. Every defensible rival lands on Ostvale or is ruled out by named data.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Defaults | 578 | 578 | yes |
| Company-years | 16,712 | 16,769 (16,571 variant) | close, no effect on call |
| Houses K / O | 5 / 45 (80 total) | 5 / 45 (80) | yes |
| Economy factor | 0.109 | 0.107 | yes |
| Pair rate other houses | 0.25% | 0.247% | yes |
| Pair rate same house/sector/year | 0.84% | 0.824% | yes |
| Same house, different years | 0.114 vs 0.120 | 0.115 vs 0.118 | yes |
| Sector / house-year | 0.059 / 0.503 | 0.067 / 0.479 | yes within noise |
| LGD | 39.9% (n=364) | 39.85% | yes |
| 5-yr chance at 15.0% | K 1.33, O 0.54 | K 1.318, O 0.538 (600k paths) | yes |
| Year-end chances | K .02 .12 .36 .76 1.33; O .00 .02 .08 .24 .54 | K .03 .13 .36 .75 1.32; O .00 .02 .08 .24 .54 | yes within 0.01 |
| Subordination 1/0.5/0.25 | K 15.6/17.0/18.3; O 14.1/15.1/16.1 | K 15.58/16.99/18.33; O 14.09/15.11/16.08 | yes |
| No house term | K 0.14, O 0.44 | K 0.14, O 0.45 | yes |

## Competing answers that survived
All land on Ostvale or are ruled out:
- No house term: buys Kestrel; contradicted by same-house-year pair excess (0.69 to 0.84 vs 0.12 to 0.25).
- House-year share 0.30 to 0.50: K 0.78 to 1.83, O 0.51 to 0.57; Ostvale always passes and is lower.
- Fund-year or lasting fund effect: both pass, Ostvale lower, same buy; worse fit.
- LGD 38.0: 0.95 / 0.34, same buy. LGD 43 (unsupported by the file): neither passes.
- Parameter uncertainty in the economy factor: K 1.43 / O 0.80 flat-prior average, Ostvale passes.
- Defaulted loan re-defaulting: 2.86 / 1.99 neither; not defensible under 3.4, now closed by the added pin.
Residual: "Kestrel fails" holds at LGD 39.3 to 40.1, not at the naive 38.0 (3.4 now filed to avoid that).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / categories | 10+ / 2+ | 13 (6 CSV, 3 PDF, 3 XLSX, 1 JSON) | yes |
| Large messy CSVs | 20,000 rows; 10-20 pages | Lenderbase 73,066 rows; Dealtrail 8,858 rows | yes |
| Distractors | 2+ in metadata, unlabelled | EURIBOR curve, PHL cashflows; unlabelled | yes |
| Deliverables | 1-3, in golden | docx + csv, golden.zip holds exactly these | yes |
| Asks / rounding | stated | stated (two decimals, one decimal) | yes |
| Answer shape | many cells downstream of deep step | per-note chances, subordination grid, year table, chart | yes |
| Realism | no LLM look | judge found none; not independently swept here | not assessed |

## Gate G reconciliation
Judge matches the design note: the field's one-factor copula on economy and sector is rung 0 and buys Kestrel (0.14 / 0.44 to 0.45, the design note's figures); the house-year co-movement is the deep step. Mechanism and family agree with the declared design. The declared distractors are not the surface read. No landed-call finding: the textbook route reaches the wrong call, not the golden.

## Gate H line
domain: pass, layers: pass, decisive_step: analytical, chain: 5 inferences (conform; trace to sponsor house; pair evidence of same-house-year excess; house-year random effect; closed-cohort LGD and tranche simulation), judgment: dependence structure identified from joint-default pair evidence plus censored LGD; one_fact: "Companies held by the same sponsor house default together in the same years." (leaves trace, estimate, PD fit and simulation still to do; removes discovery, a moderate weakness).

## Stump power (Gate F)
Strong. The one-factor plus sector copula passes every check a solver runs and buys Kestrel. Getting to Ostvale needs the house link, pair evidence, a house-year term and a closed-cohort LGD. The likeliest legitimate failures are a missed house link or an LGD or re-default error giving "neither". The one-fact hint's discovery removal is a moderate weakness only.

## Findings, ranked
1. Optional: rubric tolerance on two-decimal chances (K 1.15 to 1.33, O 0.51 to 0.57 across sound estimators) and subordination (about 0.3 of par). Critical components already state the band.
2. Optional, now applied: defaulted-loan pin in 3.4. Rebuild unjudged but no figure moves.
3. Company-years 16,712 vs 16,769 (about 57 off): name the conformation convention if convenient; no effect on call.

## Next action for the author
Finish the rebuild, confirm figures unchanged, and proceed to READY; no re-judge needed.
