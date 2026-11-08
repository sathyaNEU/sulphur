# determinism-check report, task7, 2026-11-08

Note: this is the re-judge pass (stage 4, after the first pass's NOT_DETERMINISTIC); it overwrites the first-pass report. The thread's full verdict is at /tmp/determinism-check-task7-r21794167305/verdict.md.

## Verdict
DETERMINISTIC, with SOLUTION_WRONG on two non-load-bearing wording points.
**Disposition:** FIX_NOW (solution text only: no pack change, no prompt change, no model rerun)
**Stumping type:** mechanism: statistical_rigor (contaminated comparison group from a concurrent intervention, plus a per-measure projection), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Executing plan 4.2 and 4.4, the method note and the pilot rules word for word, then dropping each passed-over building from its service-visit season, gives saving rates of 16.03, 5.88 and 1.94 per cent (16, 6, 2). Grant per tonne is 90, 90 and 220, so fund insulation and heating optimisation and not heating controls. The first pass's fork (the saving-rate estimator unpinned) is closed: every defensible rival except one lands on the same call and the same rounded figures. Main call and supplementary answers 1 to 7 reproduce. The defects are wording: "tuned burners / service team" appears in no shipped file, and Step 3's "difference 0.2%" does not reproduce.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Responses / drawn / works done | 2,791 / 1,256 / 1,218 | same (38 withdrawn) | yes |
| Passed-over with a service visit | 1,056 of 1,535 | same | yes |
| Works buildings with a visit | 0 | 0 | yes |
| Visit effect | about 7% for good | ratio 0.93 after visit, 0.95 to 0.97 in the visit season | yes |
| Lottery rates | 13 / 2 / below 0 | 12.94 / 2.49 / -1.83 | yes (HO at the 2.5 rounding edge, rejected path only) |
| Rates vs not-yet-visited | 16 / 6 / 2 | 16.03 / 5.88 / 1.94 (HO per season 5.6 to 6.5, flat) | yes |
| Fade vs all passed-over, HO | about 4 to under 2 points | 4.2 to 1.7 | yes |
| Break-even rates | 11.6 / 4.6 / 3.7 | 11.64 / 4.60 / 3.72 | yes |
| Applications | 156 / 230 / 484 | same | yes |
| Grant by measure | 2.5M / 0.75M / 0.85M | 2,495,300 / 752,690 / 846,980 | yes |
| Lifetime tonnes | 28,580 / 8,170 / 3,800 | 28,584 / 8,174 / 3,800 | yes |
| Grant per tonne | 90 / 90 / 220 | 87.3 / 92.1 / 222.9 | yes |
| HO grant per tonne on lottery rates | 280 | 276 | yes |
| 386 funded rows, grant | 3.25M | 3,247,990 | yes |
| 2019 share in by 12 June | 38% / 58% | 37.9% / 58.3% | yes |
| Closed round | about 8M / 90,000 | 7.88M / 89,464 | yes |
| Pooled-share rival | 7M / 80,000 | 6.69M / 75,718 | yes |
| 2025/26 CO2 | about 3,500 | 3,558; 3,903 on 2018/19 use | yes |
| Step 3 "draw balances 2018/19, difference 0.2%" | 0.2% | works vs passed-over mean -1.2% to -1.4% | NO (not load-bearing) |

## Competing answers that survived
1. Visit season kept in the comparison: rates 16/5/1, grant per tonne 90 / 110 / 450, 2025/26 saving about 3,000 t. The call is unchanged but several rounded figures move. The data rule it out (the visit season is only partly treated, 0.95 to 0.97 against 0.93), but plan 4.2 does not say "drop from the visit season", so this rests on analyst judgment. Closure: Fix 3 states it in Step 6. Judge rates it low to medium risk; because the files do not file the sentence, I flag it as the one fork closed only in the answer text.
2. Closed-round scaling: a share pooled over the funded measures gives 7M / 80,000; pooled over all three, about 5M / 60,000. The data pick measure-specific shares (2019 timing 38 / 58 / 80 per cent by day 23; the 2026 mix differs). Open method, data-separated, allowed. Margins comfortable.
3. 2025/26 CO2: the committee letter pins "on the gas its buildings would have used that season without the works", ruling out the 2018/19 base (about 4,000). Use times rate without the (1 - rate) division gives about 3,350, which also rounds to 3,500.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Usable files | 10 or more | 17 | yes |
| File categories | 2 or more | CSV (7), xlsx (4), PDF (5), docx (1): spreadsheet and text | yes |
| Large CSV | 20,000 rows or more | gas_meter_reads 387,978 rows | yes |
| Long messy CSV | 10 to 20 printed pages or more | benchmarking_notices 37,239 rows (also meter_points 28,497) | yes |
| Distractors in metadata.json | 2 or more, none labelled in the ZIP | 4 (electricity_customers, solar_cadastre, federal_funding_overview, municipal_heat_plan), unlabelled | yes |
| Distractors unused yet weighable | per judge | unused; judge found no surface read carried by them | yes |
| Deliverables | 1 to 3, all in golden | 2 (pptx, xlsx), per submission.md | yes |
| Asks multi-dimensional, unit and rounding stated | yes | per-measure rows, 386 application rows, round scale-up; rounding stated in prompt | yes |
| Answer shape | identifiable, cells downstream of deep step | measure table plus per-application grid plus closed-round projection | yes |
| Golden ZIP exactly the requested files | yes | not opened here (golden.zip not inspected; judge isolation) | not checked |
| Reads as a real work product, no LLM tells | yes | judge: hygiene PASS, plausible stamps and properties, no authoring disclosure | yes |

## Gate G reconciliation
Thread: statistical_rigor, analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note (read after the thread returned): Layer 2 `estimand_identification / causal_design`, the clean comparison when the randomised comparison group was treated after the draw by a second programme; domain test is each measure's saving rate on weather-normalised gas use; the note's one-fact hint ("the service team tuned the passed-over buildings' burners") matches the thread's one-fact sentence. No mismatch. No declared distractor was named as the surface read carrying the task. One caution for the main thread: the judge notes the visit reads could be read by a reviewer as a planted hidden confounder (clean-data test: without the visit effect the task is routine); it rates this borderline-low and routes it to platform runs. Also the "tuned burners" language is in the design note and answer blocks but in no shipped file (Fix 1).

## Stump power (Gate F)
Good. The plain lottery comparison executes plan 4.2 literally, files 13 / 2 / below 0 and funds insulation only, with heating optimisation at 280 a tonne; the works-only before and after (24 / 15 / 11) funds all three. Reaching 16 / 6 / 2 takes five steps: rebuild the season series; notice the heating-optimisation fade; attribute it to visits rather than works age; rebuild the comparison; scale the closed round per measure. Residual softness: a solver who checks the trend per season will probably investigate, and the one-fact sentence would make the saving-rate step routine for a solver who is told it (not in any shipped file). The field's named method (the lottery comparison) is the opponent's first move, here at rung 0 to 1, which fits the library's reading; the main thread weighs the rest against the design note's ladder.

## Deep reasoning (Gate H)
`domain: pass`, `layers: pass` (Layer 1: meter exchanges, rollovers, corrections, shared off-boundary reads, calorific and z conversion, weather normalisation, none decisive; Layer 2: treatment effect against a contaminated control plus a stratified projection), `decisive_step: analytical`, `chain: 5 inferences, judgment: comparison-group contamination and heterogeneity in response timing`, `one_fact: "the passed-over buildings were service-visited; drop each from its visit season"`. Mild H5 risk, as above.

## Findings, ranked
1. Wording defect, Gate B shape (unreachable vocabulary): "tuned burners" and "service team" in FINAL_RECOMMENDATION, Step 5 and Critical Component 1 appear in no shipped file; the finding itself (service-visit reads, about 7% step-down) is in the data.
2. Step 3 "difference 0.2%" does not reproduce (works vs passed-over mean 2018/19 use is -1.2% to -1.4%, within noise; the design uses each building's own 2018/19 base).
3. Fork 1 (visit season kept, 16/5/1) closed only by the analyst's judgment; state the reason in Step 6.
4. Borderline-low risk that a reviewer reads the visit reads as a planted confounder.

## Next action for the author
Edit the generator's answer-block text in one pass: (1) say "service visits (read_reason 'service visit') from August 2019, each followed by about a 7% step-down" and drop or mark as interpretation the "tuned burners / service team" language; (2) replace "difference 0.2%" in Step 3 with the reproducing figure; (3) state in Step 6 that the visit season is dropped because the event study shows it only partly treated. Then run the one targeted re-judge of the FIX_NOW.

## Targeted re-judge of the FIX_NOW (2026-11-08)

One isolated thread (Sonnet, medium) read the bundle copied to /tmp/determinism-check-task7-f1794168334/ and the
rebuilt answer blocks, with this pass's fix list and reproduced figures quoted. Verdict: DETERMINISTIC; the three
fixes reproduce (the visits stated as service-visit reads followed by lower use, with no works building visited; the
draw balance; the visit season only partly treated, which closes the 16, 5 and 1 reading). Its three refinements were
applied in the generator, with the pack and prompt unchanged: the balance stated as within 1.5 per cent (it holds as
means of use and as geometric means per square metre), the visit season's step as 3 to 6 per cent by visit season
against about 7 per cent the season after, and step 9's reason for the 2018/19-base figure stated from the data. No
further pass: a FIX_NOW is re-judged once.
