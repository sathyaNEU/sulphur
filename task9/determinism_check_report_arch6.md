# determinism-check report, task9, 2026-11-08

## Verdict
DETERMINISTIC on the call (buy Ostvale); headline two-decimal figures not exactly reproducible.
**Disposition:** FIX_NOW
**Stumping type:** mechanism: statistical_rigor / method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no
Judge ran against the pack before the prompt/pack rebuild (target.zip 2e83c33f..., now 150c10c4..., figures unchanged); the prompt was corrected to the 1 per cent bar and 1/0.5/0.25 targets, one-decimal subordination. Those two items I flagged are closed.

## Why
Ostvale wins under nearly every variant run. A model without the sponsor-house-year factor ranks Kestrel lower (judge: 0.34 vs 0.86), so the stump is real. Two literal-reading forks move every two-decimal figure: loss given default scope (MP-RN-2 3.4 read literally is the mean over all closed workouts, 37.96; the golden's 39.9 on closed 2008-2019 defaults is a filed-nowhere judgment) and whether years since buyout advances over the five years (MP-RN-2 3.2 silent).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Defaults | 578 | 578 | yes |
| Company-years | 16,712 | 16,793 | close (81 off) |
| Houses | 80; K 5, O 45 | same | yes |
| Pair rate same house/sector/year | 0.84% | 0.83% | yes |
| Pair rate other houses | 0.25% | 0.247% | yes |
| LGD | 39.9 (n=364) | 39.85; all closed 37.96 | yes / rival 38.0 |
| Dependence (econ/sector/house-year) | 0.109/0.059/0.503 | 0.124/0.061/0.49 | near |
| 5-yr loss at 15% | K 1.33, O 0.54 | K 1.45-1.49, O 0.62-0.64 (same dependence, ageing, LGD 39.9) | call yes, values no |
| Subordination 1/0.5/0.25% | K 15.6/17.0/18.3; O 14.1/15.1/16.1 | K 15.9/17.2/18.5; O 14.3/15.3/16.3 | within 0.3, not to 0.1 |
| No house-year factor | K 0.14, O 0.44 | K 0.34, O 0.86 | ordering yes |
Year-end chances not separately checked.

## Competing answers that survived
- LGD 38.0 (literal 3.4): Kestrel 1.05 (ageing) or 0.90 (frozen). Frozen: both pass, still buy Ostvale, but "Kestrel fails the test" and K figures change.
- Years-since-buyout frozen, LGD 39.9: K 1.30 / O 0.78, same call.
- Judge's own dependence (0.124/0.061/0.40), LGD 39.9, frozen: K 1.47 / O 1.02, Ostvale fails, answer becomes "neither". The only call-flipping variant; house-year share is estimable only to about 0.40-0.52 from pair evidence. Margin concern, not a proven fork.
Shipped rule closing them: none for ageing or LGD scope.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Usable files / categories | 10+ / 2+ | 13 / CSV, PDF, XLSX, JSON (spreadsheet, text, code-like json) | yes |
| Large messy CSVs | 20,000 rows and a 10-20 page CSV | lenderbase 73,066 rows; dealtrail 8,858 rows; lei 4,485 | yes |
| Distractors in metadata.json | 2+, not labelled in ZIP | euribor curve, PHL cashflows xlsx; not labelled in ZIP | yes (judge flagged ECB, sector json as candidates, ECB is used for FX) |
| Distractor weighs but unused | yes | yes, principal-loss test only | yes |
| Deliverables | 1-3, all in golden | 2 (docx, csv); golden.zip holds exactly them | yes |
| Asks multi-dimensional, unit and rounding stated | yes | yes | yes |
| Answer shape | gradable cells downstream of deep step | per-note chances, subordination grid, 10-row year table, chart | yes |
| Realism / LLM-look | not checked in this pass (judge saw no hygiene problem) | | not assessed |
Stale item: the pack was rebuilt after the judge ran; unzip-level file list unchanged, so spec gates carry.

## Gate G reconciliation
Judge: mechanism statistical_rigor / method_or_model_selection, family analytical_non_defect, surface_read no, sole_data_defect no. Design note (read after verdict) names the field's one-factor Gaussian copula as rung 0 (golden K 0.14 / O 0.44 vs real answer) and the house-year co-movement as the deep step; consistent. The easy route is the field's named method and lands on Kestrel with the wrong call, so no landed-call finding. The declared distractors (EURIBOR, PHL cashflows) are not the surface read. The design note's `Strategy label: UNTESTED`.

## Gate H line
domain: pass, layers: pass, decisive_step: analytical, chain: 4 inferences (conform and trace to sponsor house; show same-house same-year clustering beyond economy and sector; fit and select the house-year component; simulate with censoring-aware LGD), judgment: dependence structure and censoring-aware loss; one_fact: "defaults cluster by sponsor house in the same year" (solver still must link, fit, simulate, so not routine).

## Stump power (Gate F)
Good if solvers do not look for sponsor concentration; a solver who thinks "sponsor concentration" will go looking, so not a sure stump. Easy route passes its own checks and buys Kestrel.

## Findings, ranked
1. Ageing convention unpinned (MP-RN-2 3.2): moves K/O five-year chances by about 0.2 to 0.25 points. Fix: add one sentence to MP-RN-2 3.2 saying years since buyout advance each year (pack change, rerun needed) or add rubric tolerance.
2. LGD scope (3.4 literal 37.96 vs golden 39.9): not filed; the golden's censoring judgment is the intended analysis but a literal reading gives a different Kestrel verdict at frozen ageing. Fix: file the censoring reason in the standard or data note as a data fact (open workouts concentrated in recent defaults), or let the rubric accept 38.0 and soften "Kestrel fails" in the blocks.
3. Ostvale pass margin thin under frozen ageing with high house-year share (one variant gives "neither"). Fix: widen the margin in the generator (house-year share or Kestrel/Ostvale concentration) or pin ageing so that variant is closed; confirm by running the rival in checks.py.
4. Two-decimal values and one-decimal subordination not reproducible by an independent fit (up to 0.15 pt chances, 0.3 par). Fix: tolerance bands in the rubric (Kestrel 1.0-1.7, Ostvale 0.4-0.9).
5. Minor: company-years 16,712 vs 16,793 (81 off); name the conformation rule that gives 16,712 in the solution steps.

## Next action for the author
Pin years-since-buyout ageing in MP-RN-2 3.2 and make the LGD censoring rule recoverable from the files, rebuild, and re-judge once.
