# determinism-check report, task15, pass 3, 2026-11-10

Judged cut: the graded_blocks.md of run 20261110T0502 (scratch /tmp/determinism-check-task15-20261110T0502/). The answer blocks in submission.md were repaired after the verdict, as its Fix lines ask; that repair is not judged here.

## Verdict
DETERMINISTIC (no SOLUTION_WRONG), as the thread gave it.
**Disposition:** FIX_NOW (as the thread gave it): widen one allowance and pin the ratio-of-means definition in the blocks; pack and prompt untouched.
**Stumping type:** mechanism: decomposition_attribution (with method_or_model_selection and forecasting), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no
The thread kept the derive-first order: own_derivation.md was written before graded_blocks.md was opened.

## Why
Every stated figure reproduces from the bundle. The committed pair (WI3554, WI3559) is first and second under every sound variant, with the third line 3 to 6 points behind. The heads are method-dependent but all four bands contain every sound variant. The variants outside the bands (yield-level response, rain without Kerang's waterings, one response for all lines) are each ruled out by named data. Gates A to E pass.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Mean index, 24 nominations | 113.0 | 113.02 (all 27 quoted indices exact) | yes |
| Mean returned (ratio of means, protocol s7) | 101.6 | 101.62 | yes |
| Gap | 11.4 | 11.40 | yes |
| Nominations meeting 107.0 | 5 | 5 | yes |
| Standards' lodging series / index | 37.0 / 17.0 | 36.96 / 17.04 | yes |
| Byaduk series | 5.54 t/ha, 500 mm | 5.54, 500.4 | yes |
| Lodging cost within line and trial | 0.172 | 0.174 (0.178 index sites) | yes (within band) |
| Heads (index, move, lodging, remainder) | 3.4 / 5.5 / 2.1 / 0.4 | 2.2 / 5.7 / 2.2 / 1.2 (EB fit); 2.6 / 5.4 / 2.2 / 1.2 (ratio of means) | inside all bands |
| 28 candidate expected yields | table | mean abs diff 1.9, max 6.6 (WI3585); others within 4.5 | inside allowances |
| Top two | 113.4, 109.5; next 103.4 | 114.8, 109.0; next 103.2 | yes |
| Expected lodging WI3554 / WI3559 / WI3571 / WI3585 | 28 / 27 / 48 / 71 | 26 / 25 / 48 / 72 | inside |
| Kerang 2025 water; abandoned plots | 222 mm irrigation; 22 | match | yes |

## Competing answers that survived
1. Returned relative yield as ratio of means (101.6, gap 11.4) against mean of per-trial ratios (102.1, gap 10.9). Protocol s7 governs, but Supplementary 1 carries no band. Minor.
2. WI3585 under an unshrunk own-trial fit: 104.4 against golden 92.0 (diff 12.4, allowance 9.0). The only line outside its allowance in any variant. The blocks' "lands inside every range" for unshrunk fits is not reproduced for this line. Minor.
3. "Its index" for two-season candidates is taken over six trials by the nominations' practice; the blocks do not say so.
4. "Yield level" in step 3 is not defined as the trial mean. With Byaduk's own yield as the level, the series regression favours that regressor (self-referencing artefact).
Not surviving (ruled out by named data): yield-level response (move 3.3 to 3.7, remainder 3.3 to 4.8), rain only (move 7.0, Kerang yield 5.30 against 2.76), one response for all lines (move 7.25, remainder -2.4), lodging from harvested plots only (WI3585 103.8, ruled out by handbook s5 and abandoned plots 81% lodged).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Usable files | 10 or more | 18 | yes |
| Categories | 2 or more | 4 (csv, xlsx, pdf, docx) | yes |
| Large messy CSVs | 20,000 rows plus a 10 to 20 page CSV | plot_harvest_2019_2025 21,903 rows; PlotHarvest_2014_2018 12,971 rows (header repeats, kg/ha); trial_entry_lists 14,795 | yes (second file's printed length not measured by me, taken from the thread's "messy" finding) |
| Distractors in metadata.json | 2 or more, unlabelled in ZIP | 3 (grain_quality, disease_nursery, seed_store_inventory); thread found none labelled; seed never binding | yes |
| Distractor relevance | unused but weighty | thread: texture/irrelevant, none carries a result | yes |
| Deliverables | 1 to 3, all in golden | 3 (xlsx, docx, png); golden.zip holds exactly these | yes |
| Asks | multi-dimensional, unit and rounding | prompt states one decimal / whole percent | yes |
| Answer shape | one of fourteen, 4+ results | bridge plus ranked list with ranges (decomposition + forecast); 9 results | yes |
| Realism | no LLM look | thread found no authoring leakage; not re-audited by me | yes (on thread) |

## Gate G reconciliation
Thread: analytical_non_defect, no surface-read dependence, no sole defect. Design note's Hidden factor record lists five factors, all marked "not only in deciding units" and modelling-depth (season-water response, lodging pressure, selection on noisy means, abandoned plots, shared season swing). Consistent: no factor found in one look and fixed by one routine step, and the quoted index is correct by its definition. The thread's residual weakness (yield-level definition) is a wording gap, not a planted defect.

## Stump power (Gate F) and Gate H
domain: pass | layers: pass | results: 10 graded across 6 areas | one_thing: none | effort: quick 3, careful 6, thorough 9 of 10 | one_fact: "season water includes Kerang's waterings and abandoned plots keep their lodging" rescues about 3 of 10.
Reconciliation with the note: the note's effort table has quick at 2 of 9 (R1, R9) and careful about 4 to 5 of 9 with R3, R4, R6, R8 missed; the thread puts careful at 6 of 10, so careful is somewhat higher than the note, and the thread's yield-level run reaching the right pair (R8) is the gap. The thread's likeliest careful-run losses are the move and remainder heads (about 3.5 and 3.5 from a yield-level response against 5.5 and 0.4) and WI3585 (about 104 against 92). Quick at 3 of 10 is within a third. The thread's best sentence (3 of 10) matches the note's "Largest single hint" (3 of 9). The note's claim that the pair is robust is confirmed, which means R8 is earned by hurried runs; the price of the task rests on the heads, the 28 yields and the ranges.

## Findings, ranked
1. Pin returned relative yield as ratio of means (protocol s7) in Supplementary 1, and state that 102.1 / 10.9 is not accepted.
2. WI3585 allowance about 13, or soften "inside every range" for unshrunk fits.
3. Define "yield level" as the trial mean yield, fitted on programme plus series data.
4. State that a two-season candidate's index is over all its Stage 3 trials at the three sites.
5. Careful column is a little higher than the note's (R8 earned by a yield-level run): weigh against the effort test.

## Next action for the author
Apply the four wording/band repairs in the blocks (reported already done in the generator), rebuild, and run the single re-judge, which writes the canonical determinism_check_report.md.
