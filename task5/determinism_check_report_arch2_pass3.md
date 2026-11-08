# determinism-check report, task5 (arch2 pass3), 2026-11-08

## Verdict
DETERMINISTIC (no SOLUTION_WRONG).
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Thread: one sonnet judge on target.zip sha256 prefix 14f7ae29ebb94bc9, brief /tmp/determinism-check-task5-arch2p3/judge_brief.md, verdict /tmp/determinism-check-task5-arch2p3/verdict.md. Spawned by the main session (my runtime has no Agent tool).

## Why
The regulation (Sections 3, 4, 6) fixes population, event and rule. The meter data split 396 vacant from 7,624 lived-in with a wide gap in the largest hourly excess over a dwelling's own typical day, so the designation does not move with the cut. Five qualify: 5802, 5803, 5805, 5807, 5809. Nearest miss Snoholt 4.68 (4.7); nothing within rounding of 5.0. The filed "exact binomial interval" closes the interval fork from pass 2: it selects Clopper-Pearson, and Wilson or Wald would differ only in a printed interval digit, never in qualification.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Counted dwellings | 8,020 | 8,020 (matrikkel Bolig, tatt_i_bruk by 1 Nov) | yes |
| Vacant dwellings | 396 (66/38/63/33/28/34/31/36/30/37) | same | yes |
| Shares | 4.0/7.3/6.4/3.8/6.5/4.6/8.2/3.2/5.4/4.7 | 4.02/7.31/6.43/3.84/6.51/4.59/8.16/3.21/5.36/4.68 | yes |
| 90% exact intervals | three wholly above 5.0 (5802, 5803, 5807) | 5.5-9.5; 5.2-7.9; 6.0-10.9; 5805 4.7-8.8; 5809 3.9-7.2 | yes |
| Register rolled to 1 Nov | 7,186 occupied, 834 empty, 13,599 persons | same (shift derivable from events; 314 to 209 unmatched) | yes |
| Over/undercoverage, net bias | per answer 4, county 118 (1.6), 556 (66.7), 5.5 | all rows | yes |

## Competing answers that survived
None. Consumption floor gives none (empty dwellings heated); register-empty gives all ten (Section 4 rules out); rise over night gives Tverrvika and Ornevik only, ruled out by named data (timer dwellings' rises overlap the lived-in range, 38% registered residents against 93%, identical days). Raw day against median day gives the same 396. Mid-p or one-sided interval is remote and moves no qualification.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Usable files / categories | 10+ / 2+ | 15 / csv, parquet, xlsx, pdf, eml | yes |
| Large messy files | CSV 20,000+ rows; CSV 10-20 pages+ | daily values CSV 113,759 rows; register CSV 13,778 rows (well over 20 printed pages) | yes |
| Distractors in metadata.json | 2+, unlabelled in ZIP | 6 named, none labelled, unused (judge confirmed) | yes |
| Distractor relevance | unused, ruled out by a shipped fact | prices, outages, titles, business and shareholder registers; outages cost a few hours, no classification change | yes |
| Deliverables | 1-3, all in golden | 2 (docx, xlsx), both covered by answers 1-5 | yes |
| Asks | multi-dimensional, unit and rounding stated | ten-municipality table, chart, coverage grid, per-dwelling sheet; per cents to one decimal | yes |
| Answer shape | gradable cells downstream of deep step | ranked/threshold table plus coverage grid | yes |
| Golden ZIP holds exactly requested files | yes | two files requested, two in golden.zip (not unpacked by me) | yes, on the listing |
| Realism | no LLM tells | judge found none; leak reader clean | yes |

## Gate G reconciliation
Thread: method_or_model_selection, analytical_non_defect, surface_read no, sole_data_defect no. Design note and pipeline.json: same (classifier choice the statistical judgment; rise rival lands on two). No match problem. The thread did not name a declared distractor as the surface read. It notes the timer cohort is an inserted structure but a second explanation for one pattern, not a wrong reported number.
Gate H: domain pass, layers pass, decisive_step analytical, chain 4 inferences (judgment: occupancy signal chosen and validated from the data), one_fact "a vacant dwelling's days repeat; judge each dwelling against its own typical day". Consistent with the design note's one-fact entry (the heated-November hint leads to the rise, which lands on two).

## Stump power (Gate F)
Good. Two reflex readings each give a specific wrong answer (floor: none; register: ten; rise: two). The thread notes a strong model that checks the rise against its own cleaned data could catch the timers, so the work is real but not trivial. Mild H5 exposure: the one-fact sentence is a method hint. The main thread should weigh this against the design note's ladder.

## Findings, ranked
1. No blocking finding. Interval fork closed by "exact binomial".
2. Mild H5 exposure as above.
3. Minor: pass 2 reported the largest vacant excess as 0.671 kWh; pass 3 states "at most 0.6", and golden Step 6 says "no vacant dwelling exceeds 0.6". If 0.671 is right the golden's wording is loose, not wrong in outcome (gap to 1.3 unchanged). Worth a one-line check by the author.
4. Optional: name "two-sided Clopper-Pearson" in Step 7.

## Next action for the author
Proceed to READY. Optionally check the 0.6 versus 0.671 wording in Step 6 and, if it is loose, correct it without moving a graded figure.
