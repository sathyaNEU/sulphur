# determinism-check report, task5 (arch2 pass2), 2026-11-08

## Verdict
DETERMINISTIC (no SOLUTION_WRONG). One minor open fork on the 90 per cent interval method.
**Disposition:** FIX_NOW
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Thread: one sonnet judge, brief at /tmp/determinism-check-task5-13564/judge_brief.md, verdict at /tmp/determinism-check-task5-13564/verdict.md (target.zip sha256 prefix 13a7d9af90ef518c). Spawned by the main session because my runtime has no Agent tool.

## Why
The shipped files force the five-municipality call (5802, 5803, 5805, 5807, 5809). Regulation Section 4 defines vacancy as nobody living there on any day and says the register does not decide. Each dwelling's hourly record read against its own typical day splits 396 vacant (max excess 0.671 kWh) from 7,624 lived-in (min 1.343), and the split holds under every night window, mean or median baseline, and the UTC/Oslo shift tried. The rivals fail on named data: consumption floor gives none, the morning/evening rise gives 326 vacant and two municipalities, register-empty gives all ten.
The one open item: the email asks for a 90 per cent interval "taking the counted dwellings as so many chances" but never names the interval. Wilson and Jeffreys move one-decimal endpoints by up to 0.1 (5802 5.6, 5803 5.3, 5805 4.8, 5809 4.0 on Wilson). Qualification does not move.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Counted dwellings | 8,020 | 8,020 (matrikkel, Bolig, tatt_i_bruk by 1 Nov) | yes |
| Vacant | 396 | 396 | yes |
| Vacant by municipality | 66,38,63,33,28,34,31,36,30,37 | same | yes |
| Shares | 4.0,7.3,6.4,3.8,6.5,4.6,8.2,3.2,5.4,4.7 | same | yes |
| Exact 90% intervals (Tverrvika, Hesteby, Ørnevik) | wholly above 5.0 | 5.5-9.5, 5.2-7.9, 6.0-10.9 | yes |
| Rise rival | 326 vacant, 70 timers | 326, 70 | yes |
| Floor medians | 22.8 vs 20.4 kWh/day | same | yes |
| Register 1 Nov | 7,186 with someone, 834 nobody, 13,599 persons | same | yes |
| Over/undercoverage, net bias, county | 118 (1.6), 556 (66.7), 5.5 | same, all ten municipalities too | yes |

## Competing answers that survived
- Interval method (exact binomial vs Wilson vs Jeffreys): endpoints differ by 0.1 at one decimal in answer 2 and in the chart; call unchanged. The design note (SF24) says the ministry's letter files the exact binomial convention, but the shipped email does not name it. This is the single FIX_NOW item.
- Thin margins (Fjordeid 30 vs 28 needed, Snøholt 37 vs 40 needed) are clean counts after a wide gap, not contested.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Usable files / categories | 10+ / 2+ | 15 / csv, parquet, xlsx, eml, pdf | yes |
| Large messy files | CSV 20,000+ rows, CSV 10 to 20 pages+ | daily values 113,759 rows; cadastre 8,926 and register 13,778 rows | yes |
| Distractors in metadata.json only | 2+ | 6 listed; nothing in the ZIP labels one | yes |
| Distractors unused yet weighable | yes | spot prices, outages, land register x2, business and shareholder registers unused; the daily CSV lures a level method | yes |
| Deliverables | 1 to 3, all in golden | 2 (docx, xlsx), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | ten municipalities x share, interval, coverage errors; one decimal stated | yes |
| Answer shape | gradable cells downstream of deep step | ten-row grid plus county row | yes |
| Golden exactly the requested files | yes | 2 files, requested formats | yes |
| Realism / no LLM look | yes | judge found no authoring language in the pack; I did not review the golden prose | partial, not audited by me |

## Gate G reconciliation
Judge: mechanism method_or_model_selection, family analytical_non_defect, surface_read no, sole_data_defect no. The design note (analyst test, domain test, one-fact test) declares the same classification: the rise lands on two municipalities and the floor on none. No match gap. The declared distractors (prices, outages, registers) are not named by the judge as carrying the task; only the daily CSV serves as a lure, which is intended. Gate G itself: no shipped artifact ranks the municipalities on the decision wrongly.

## Gate H line (judge)
domain: pass; layers: pass; decisive_step: analytical; chain: 5 inferences (join and clean hours; reject level; reject rise; day-relative deviation with a gap-justified cut; binomial interval vs threshold), judgment: classifier selection justified by the separation gap and the register; one_fact: "Some empty dwellings run a heating timer, so judge occupancy by whether days differ from each other, not by level or morning/evening rise."
My reading: this is a classifier-selection judgment, not a rule the files spell out, and no filed sentence names the timer (the regulation, email and register do not). It is not a bare inserted defect, since no reported number is wrong and the 70 timers are a property of heating behaviour. The risk is that the judge rates the rescue sentence strong: once told about timers the rest is "mostly routine" (H5 weak), and the 70 timers are a planted subgroup, which is banned kind 3 if the main thread reads them as an inserted problem. The design note argues the one-fact test fails because after the hint the solver must still build the baseline, set each day at its night, choose a statistic and cut, handle outages and roll the register back. Weigh against the ladder; I record it borderline-to-pass.

## Stump power (Gate F)
Real and data-driven. A solver that conforms everything and stops at the household's rise gets a clean bimodal split that agrees with the register and files two municipalities; a floor reader files none. Reaching the golden needs a check of whether each cluster is internally consistent day to day. A strong run that profiles day-to-day variation, or notices 326 vs 396, can solve it, so some runs will land. The expected failure is stopping at the rise method.

## Findings, ranked
1. FIX_NOW: the interval method is unnamed in the shipped files (email says "chances" only); one-decimal endpoints move by 0.1 under Wilson or Jeffreys.
2. Watch: Gate H rescue sentence (timers) is short and the post-hint chain is mostly routine; planted-subgroup reading is the banned-kind-3 risk.
3. Not audited by me: golden realism.

## Next action for the author
Name the interval in a shipped file, as the exact binomial (Clopper-Pearson) 90 per cent interval on the counted dwellings, in the ministry email or prompt, without touching the pack's data or the main call; then close SF24 as asserted in checks.py and weigh the Gate H watch item against the ladder. Per the stage rule, a FIX_NOW is re-judged once.
