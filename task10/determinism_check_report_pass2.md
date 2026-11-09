# determinism-check report (pass 2), task10, 2026-11-09

## Verdict
NOT_DETERMINISTIC (no SOLUTION_WRONG: the golden figures reproduce)
**Disposition:** SEND_BACK
**Stumping type:** mechanism: decomposition_attribution (with statistical_rigor and cold-day forecasting), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Thread: one general-purpose/sonnet/medium judge on a fresh unzip of target.zip (sha256 203d2bf4...), derivation written before graded_blocks.md was opened. The earlier report was not shown to it. The coordinator edited one sentence of the brief (the colder-day ask opens "should that winter bring days colder than the design day"); the thread judged the current prompt.txt. Artifacts: /tmp/determinism-check-task10-1794182959/verdict.md and own_derivation.md.

## Why
1. Ask 6 at minus 4.5 C is margin-fragile. Fenwick Street exceeds firm capacity there by only 0.05 MW (pre-flex 36.97 less a net credit of about 6.4 MW, against 30.5). It flips to a 0.39 to 0.87 MW shortfall under a quadratic temperature correction, under delivery fitted on 2025/26 events only, or both, and is +0.14 under a provider-pooled fit. Nothing shipped picks between these. The answer is "Ashcombe, Fenwick, Hartwell" or "Ashcombe, Hartwell" depending on an unfiled method choice (Gate C, margin_or_boundary_fragility). The minus 6.0 C answer (all four; Charlecote +0.35 to +0.70) holds across every variant run.
2. The main call rests on an unfiled attribution reading. Guideline section 6 credits "the reduction in the primary's demand that its provider will deliver"; no shipped text says load is transferred across an open point or excluded from the credit. The plain reading is the fall at the primary. A surviving rival (gross fall, temperature-dependent delivery, no netting) credits 6.5, 4.0, 11.0 and 5.5 MW and gives Ashcombe Road only (23.5 against 23.0, Hartwell 17.5 against 17.8). The golden's "No other conclusion survives" rebuts the flat 0.9 average and the double-count, but not this rival.
3. Smaller: Ashcombe's gross design-day margin is a whole-MW rounding hazard (30 - 7 = 23, equal to firm), and the rounding of the "how far exceeds" figure is not fixed by the prompt (3.3 and 2.4 give 3 and 2 either way).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Neighbour rise at 17:30/18:00 (Tollbrook, Wexley, Kestwick) | 1.4, 1.4, 0.8 MW | +1.32, +1.47, +0.75 (joint regression, window-confined, none at Charlecote's neighbours) | yes |
| Net delivery per MW at minus 3.0 C (Ashcombe, Charlecote, Fenwick, Hartwell) | 0.4, 0.5, 0.5, 0.4 | 0.39, 0.50, 0.51, 0.36 (gross 0.69, 0.50, 0.79, 0.73) | yes (netting reading) |
| Credited MW | 4, 4, 7, 3 | 3.7, 4.0, 7.1, 2.7 | yes |
| Pre-flex 2027/28 design-day demand | 30, 25, 36, 23 (after + credit) | 30.05, 25.01, 35.98, 22.94 | yes |
| After-flex against firm | 26 v 23.0; 21 v 22.5; 29 v 30.5; 20 v 17.8 | 26.3, 21.0, 28.9, 20.2 | yes |
| Excess on design day | 3 MW, 2 MW | 3.3, 2.4 | yes |
| Minus 4.5 C set | Ashcombe, Fenwick, Hartwell | Ashcombe +4.6 to +5.7, Hartwell +3.4 to +4.0, Charlecote -0.3 to -0.6, Fenwick +0.05 (flips) | partial: Fenwick fragile |
| Minus 6.0 C set | all four | all four, Charlecote +0.35 to +0.70 | yes |
| Cleaning | weather v1 over v0, 2 SCADA names, duplicates, B zeros | 310 weather hours, 441 duplicate rows, 31 B zero rows, stale S runs | yes |

## Competing answers that survived
- Fork A, Fenwick Street at minus 4.5 C: in (linear, both winters) or out (quadratic, or 2025/26 events only). Closure shipped: none.
- Fork B, main call: reinforce Ashcombe Road and Hartwell Common (netted) or Ashcombe Road only (gross, temperature-dependent). Closure shipped: section 6 wording is silent on transfers; the golden's closing paragraph does not rebut the second.
- Fork C: rounding of the excess figure (benign here).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Usable files | 10+ | 11 | yes |
| File categories | 2+ | spreadsheet (5), csv/text (3), pdf (3) | yes |
| Large messy CSVs | one 20,000+ rows, one 10 to 20 pages | demand 196,201 rows; weather 13,373 lines (events log 373 lines, about 8 pages, not needed) | yes |
| Distractors in metadata.json | 2+, unlabelled in ZIP | 3 (interruptions, transformer condition, DUoS); none labelled in the ZIP; unused, per the thread | yes |
| Distractor arithmetic | none answers a graded quantity | thread found none does | yes |
| Deliverables | 1 to 3, all in the golden | 2 (xlsx, pptx), both present in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | per-zone table plus chart plus excess plus two cold-day sets; whole MW and one decimal stated; excess rounding covered only by "whole MW" | yes, with note |
| Answer shape with many gradable cells | yes | per-zone grid (4 zones by delivery, credit, after, firm) | yes |
| Golden ZIP exactly the requested files | yes | golden/ holds the two files | yes |
| Realism | no LLM look | thread: real-looking artifacts; minor date incoherence in the load growth register (offers accepted after the autumn 2026 assessment; no figure moves) | yes, with note |

I did not open the golden deliverables beyond confirming their presence; the ledger above comes from the thread and the graded blocks.

## Gate G reconciliation
Thread: mechanism decomposition_attribution, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note: estimand_identification, "separating two explanations for one pattern" (a moved section versus provider reduction), no planted decoy, no replay, not semantics, not rule application. The two agree on type. The thread calls it borderline because the netting hinges on reading the neighbour rise as a transfer, and the design note's own statement that nothing filed says how the provider's reduction is measured is the same gap the thread scored as an unclosed fork. The declared distractors are not named as the surface read. The thread's intermediate route (temperature-aware, un-netted: Ashcombe only) is not on the design note's ladder as a landed call and is not rebutted by data.

Gate G line: mechanism: decomposition_attribution; stumping_family: analytical_non_defect; surface_read_dependency: no; sole_data_defect: no (matches the design note; borderline on the unfiled netting reading).

## Stump power (Gate F)
Strong. Crediting contracted MW, the 0.86 to 0.91 average event delivery, or even 100 per cent clears Ashcombe and Hartwell and reinforces nobody in scope. The real work is the temperature-dependent delivery, the extrapolated cold-day correction (cold days all being flexibility days), and the cross-primary spillover. The netting's "one fact" ("neighbours pick up part of the fall, net it out") still leaves the regression and extrapolation. Not a textbook-method landing.

Gate H line: domain: pass; layers: pass; decisive_step: analytical; chain: 4 inferences (temperature-corrected extrapolated base demand; delivery per MW as a function of daily mean; attribution of the fall net of open-point spillover; re-evaluation of credit and demand at colder days), judgment: spillover attribution plus temperature-dependent delivery regression; one_fact: "the neighbour primaries pick up part of each zone's fall across the open points, so net it out" (leaves the temperature regression and extrapolation, so not routine).

## Findings, ranked
1. Fork B: the netting is not forced by any filed text, and the gross temperature-aware route gives a different call (Ashcombe Road only). This changes the main recommendation.
2. Fork A: Fenwick Street at minus 4.5 C is a 0.05 MW exceedance that flips under reasonable method choices (new ask 6 is the fragile cell).
3. The closing "No other conclusion survives" omits the gross temperature-dependent rival.
4. Excess rounding unstated (benign); Ashcombe whole-MW display hazard (30 - 7 = 23 against firm 23.0); register date incoherence (cosmetic).

## Next action for the author
Run `/fix-determinism task10` on the thread's Fix, in one pass: (1) move the minus 4.5 C test point or the Fenwick Street margin so every in-scope primary clears or misses by at least 1 MW under linear and quadratic corrections and under either winter's delivery, or keep only the minus 6.0 C test; (2) close the netting reading in the filed guideline or award text without naming the method (for example, credit is the reduction in total demand across the primaries the zone's feeders reach through open points, or load picked up elsewhere is not credited), and extend the closing paragraph to rebut the gross temperature-dependent route; (3) fix the rounding of the excess figure in the prompt. This invalidates the current prompt and pack, so the runs must be redone after the fix. The judge allows one re-judge.
