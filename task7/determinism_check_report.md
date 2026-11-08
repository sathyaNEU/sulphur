# determinism-check report, task7, pass 2 (fiction date 2027-01-15; run 2026-11-08)

Pass 1 returned SOLUTION_WRONG with FIX_NOW (844, 319/112/10%, 75% and 9% did not reproduce; 2,022,100 total and euro-exact CSV cells unforced; "EUR 0.2 million" off the 500k grid). Repaired: blocks re-emitted at the prompt's rounding, fitted ratios in place of band means, model figure given as EUR 0.22 million, working counts in words, no euro-exact CSV total, the five given as a set with the leader named. This pass replaces pass 1.

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Read literally, the memo and policy 4.1, 4.4 to 4.6 fix population, PD, EAD, LGD model and the expected inspection value. Carried values give EUR 0.22m (nil); the default record fitted on years since inspection by book gives EUR 2.01m. Every age-aware fit lands on EUR 2m; split and top five are stable. Gates A to E pass.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Performing facilities / exposure | 2,260 / EUR 1.84bn | 2,260 / 1,839,089,693 (INV 1,447, OWN 813) | yes |
| EL on carried values | 0.22m, nil to 500k | 221,294 | yes |
| Mean inspection/carried at default | 87.1% | 0.872 (facility level 0.871) | yes |
| Fit INV at 1 / 8 years | 93% / 76% | 93% / 76.5% | yes |
| Fit OWN at 1 / 8 years | 89% / 72% | 89% / 71.5% | yes |
| Total / INV / OWN | 2.0m / 1.25m / 0.75m | 2,010,596 / 1,227,714 / 782,882 | yes at graded rounding |
| Top five | AB322222580 leader, set of five | same set; 6th is 29.4k vs 31.9k for the 5th | yes |
| Exposure last inspected 7+ years | 26% | 25.9% | yes |
| Post-2022 defaults | over a third fresh, about one in ten stale | 36%, 9.5% | yes |
| Book effect | about 4 points | -0.052 log points, t = -7.1 | yes |
| Slope strength | "more than 20 SE" | t about -15 to -19 | overstated (optional wording fix) |

## Competing answers that survived
None to a different rounded cell on a reasonable method. Run and closed: flat mean 1.0m; 2022+ flat mean 1.5m; linear 2.0m with same split; no smearing 2.0m; fits from 2017 and 2022 same answers; pooled books 1.5m / 0.5m split (ruled out by t = -7.1); performing-property inspections (ruled out, the question is conditional on default). Only an unmotivated 2012-2016-only fit moves the split (1.5m / 0.75m); bootstrap 95% interval 1.82m to 2.29m is centred in the 2.0m bucket.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Usable files | 10+ | 16 | yes |
| Categories | 2+ | spreadsheet (csv, xlsx), text (pdf) | yes |
| Large CSVs | 20,000 rows and 10 to 20 pages | 133,156 and 121,249 rows | yes |
| Distractors | 2+ in metadata.json, unlabelled in ZIP | 4 named; names unlabelled; judge found none carry the answer | yes |
| Deliverables | 1 to 3, all in golden | 2, both present | yes |
| Asks | multi-dimensional, unit and rounding stated | yes | yes |
| Answer shape | many gradable cells | plan, two book cells, top five, 2,260-row file | yes |
| Golden ZIP exact | requested files only | exactly the pptx and csv | yes |
| Realism | no LLM tell | none seen by judge | yes |

## Gate G reconciliation
Thread: method_or_model_selection, analytical_non_defect, surface_read no, sole_data_defect no. Design note and card: method_or_model_selection, population_selection. Match; the declared distractors are not the surface read. The green back-test is true and explained, not read as a decoy. Gate H: domain pass, layers pass, decisive_step analytical, chain 5 inferences, one_fact "inspection at default falls below carried value by more the older the inspection" (still leaves record build, window, fit, book split, application); the design note's one-fact is consistent.

## Stump power (Gate F)
Good. Carried values file nil, flat mean 1.0m, recent-years mean 1.5m; only the age-aware, book-specific fit gives 2.0m. Mild risk: the memo's "value we would expect our inspection to put on the security" nudges toward a defaults-based ratio, so some runs fail only at the slope or book split, which is still analytical.

## Findings, ranked
1. None blocking. Optional: say in the blocks that the CSV column list is the author's choice; replace "more than 20 standard errors" with a figure the data supports (about 15 to 19).

## Next action for the author
Take the two optional wording notes into the blocks (no graded figure moves), then proceed to stage 5.
