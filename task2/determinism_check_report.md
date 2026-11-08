# Determinism check report: task2 (architecture 4)

Judge thread: isolated Sonnet at medium, 2026-11-08, on the bundle unzipped from target.zip (sha 38cfe50a) and the
submission's graded blocks; the brief at /tmp/determinism-check-task2-r1/judge_brief.md.

- **Verdict:** DETERMINISTIC (the main call and the graded gold forced; the grade-tonnage cells carry a method
  tolerance).
- **Disposition:** FIX_NOW, answer blocks only. Applied 2026-11-08: Supplementary answer 3 now states the band an
  affine correction to the same block variance moves each row by (tonnes 14, grade 6, gold 11 per cent, computed in
  writeup.py from the rungs), and names answer 4 (the gold above 2.5 g/t, nearest 50,000 oz) as the graded figure. No
  pack, prompt or graded figure moved. Re-judged once on the fixed block (below).
- **Gate G:** method_or_model_selection (change of support), analytical_non_defect, surface_read_dependency no,
  sole_data_defect no.
- **Gate H:** domain pass, layers pass, decisive_step analytical, chain 4 inferences, one_fact none.
- **Minor fork noted, closed by the prompt:** "can commit" read as expected-cost minimisation (Tier B beats Tier C
  by about AUD 1M at 147 koz); the prompt's gold to the nearest 50,000 oz and term sheet 2.2 (a tier is the floor)
  pin the coverage reading.
- **Stump power (the judge's read):** moderate to good; term sheet 1.2 states the selection block (the WHAT, which the
  decision needs), so a strong run may reach a support correction and still needs the declustering, the variogram
  and the variance ratio.

## The judge's verdict, verbatim

## Verdict
DETERMINISTIC (main call and ask 4 forced; ask 3's tonnes and grade cells carry a method tolerance, see Evidence).

## Disposition
FIX_NOW. Give the grade-tonnage cells (tonnes and grade at each cut-off, ask 3 and the Comparison/Grade-tonnage sheets) a stated tolerance in the solution and rubric. The pack and prompt stay byte-identical, so no model rerun is needed.

## Why
The term sheet (cl. 1.2) fixes the estimand: ore is a 5 m x 5 m x 2.5 m block at 2.5 g/t or more, and the tier thresholds are 75, 125 and 200 koz (cl. 2.1). The mine-plan PDF supplies the grid shift. Every route that carries the composites to block support lands at 136 to 162 koz, which is inside Tier B and rounds to 150,000 oz. The two wrong routes (declustered composites, 229 to 231 koz, Tier C; kriged blocks, 96 koz, Tier A) skip the volume-variance step and are rejected on the data, not on a semantic reading. No gate A to E failure found.

## Evidence
Recomputed from target/ only.

| Item | Golden | Mine | Source |
|---|---|---|---|
| Collars on mine grid (MGA less 339,250 E / 6,601,480 N) | stated | applied to 297 MGA collars; the 192 pre-2022 collars are already on the mine grid | collars CSV, mine plan PDF |
| Stage 5 composites (2.5 m flitches, inside outlines) | 10,837 | 10,845 (8 short composites differ; immaterial) | assays, flitches CSV |
| Composite mean, as drilled / declustered (25 m cells by flitch) | 1.38 / 1.18 | 1.376 / 1.181 | |
| Stage 5 tonnes (zone densities from bulk density and weathering logs) | 20.6 Mt | 20.62 Mt | |
| Declustered composites above 2.5 g/t | 231 koz | 228.7 koz (1.82 Mt at 3.90 g/t) | reproduced within 1% |
| Raw composites above 2.5 g/t | 350 koz | 355 koz | reproduced within 1.5% |
| Block-support gold above 2.5 g/t at variance ratio 0.54 | 147 koz | 147.6 koz (lognormal), 140.7 koz (affine) | reproduced |
| Variance ratio | 0.54 | about 0.5 to 0.57 from my own downhole and cross-hole experimental variograms (nugget about 0.34 of sill, short structure) | |

I did not rebuild the kriged model (96 koz) or the cross-validation slope. Neither is needed for the call. I saw nothing in the variogram that contradicts the golden's 0.54.

- **Assay conventions that look like forks but are not.** Using the screen-fire re-assay, the original assay or their average moves the composite mean by 0.001 g/t (1.3765 against 1.3756). The two labs show no CRM bias (ratio 1.00 to 1.005), and only two assays are below detection ("<0.02"). The ppm and g/t labels are the same unit. None of these decides anything.
- **Sensitivity of the call to the variance ratio f** (lognormal / affine):

  | f | koz above 2.5 g/t |
  |---|---|
  | 0.45 | 124 / 123 |
  | 0.54 | 148 / 141 |
  | 0.60 | 162 / 155 |
  | 0.70 | 183 / 176 |

  The answer stays at 150,000 oz for f of about 0.47 to 0.67. The raw-sill trap (raw variogram plateau 1.8 against declustered variance 1.25) does not bite, because f is a relative quantity. The declustered-weighted variogram plateaus near 1.1 to 1.25, consistent with the declustered variance. The margin is clean but only about 22 to 28 koz either side, which is moderate.
- **Surviving minor forks.**
  1. Ask 3 (and the Comparison sheet's grade-tonnage table). Tonnes and grade above 2.5 g/t are method-dependent: 1.21 Mt at 3.62 g/t (affine) against 1.34 Mt at 3.42 g/t (lognormal), a gap of about 10% in tonnes. Ounces agree (141 against 148 koz). At 1.5 g/t the gold is 326 against 364 koz, at 2.0 g/t 212 against 228 koz, and at 3.0 g/t 99 against 96 koz. Only the 2.5 g/t gold is pinned to the nearest 50 koz, so a row-by-row match to one estimator is not forced.
  2. "Can commit" read as expected-cost minimisation instead of coverage. With 145 AUD/oz shortfall and a 5 AUD/t charge saving from B to C, Tier B beats C by about 1M AUD at 147 koz and 1.34 Mt. Tier C would win by about 1.7M AUD at 162 koz and 1.44 Mt. The prompt's "that gold is to the nearest 50,000 ounces" pins the coverage reading, so I treat this as low risk and note it.
- **Distractors.** The Stage 4 survey pickup lies at mine east 920 to 990, west of Stage 5 (east 1012 and above), so it has no effect. The metallurgical bottle rolls bear on payable gold, not contained gold. Neither moves the answer.
- **Decisive facts present in files.** Block definition and cut-off (term sheet cl. 1.2), tiers (cl. 2.1), grid shift (mine plan), flitch outlines (flitches CSV), densities and weathering (CSVs). No external fact is needed. The golden's "indirect lognormal" vocabulary appears nowhere in the pack, but it labels a method, not the committed action (Tier B).

## Files/Hygiene
PASS. 11 files in 4 formats (7 CSV, 2 PDF, 1 xlsx, 1 png; the PDFs and the xlsx are small real-looking documents). The assays file (43,150 rows, ppm and g/t units, two labs, re-assays) and the 25 m / 12.5 m collar file with a mixed grid carry plausible mess. The PDFs read as company documents, and I found no authoring or provenance leakage, no timeline conflict and no tool banners. The term sheet is dated 22 Oct 2026, the mine plan 3 Nov 2026, the election date 15 Dec 2026 and the survey 2026-09, which is coherent. The distractors (QAQC, bottle rolls, Stage 4 survey, drilling plan PNG) are unlabelled. I cannot check cross-batch duplication from inside this folder. No exclusion-level finding.

## Stump power
Moderate to good. The reflexive analyses fail in different directions: declustered composites give Tier C (229 koz), and a kriged block model gives Tier A (96 koz, unbiased in cross-validation, which makes it look validated). Only a volume-variance (change-of-support) correction on honest data lands at 150 koz. The weakness is that term sheet cl. 1.2 states the 5 x 5 x 2.5 m selection unit outright, and models know kriging smooths, so a strong run may reach the support correction. It still needs the declustering, the variogram and a variance-ratio judgment. The least ambiguous lever, if too easy in live runs, is to widen the infill contrast, not to add hints.

## Stumping type
mechanism: method_or_model_selection (change of support / volume-variance relation); stumping_family: analytical_non_defect; surface_read_dependency: no; sole_data_defect: no.
No reported figure in the pack is wrong and nothing is overturned by catching a defect. On clean data the task would still stump on the estimator choice, which the pack does not gate through any inserted error.

## Deep reasoning
domain: pass, layers: pass (Layer 1: mixed MGA/mine grids, ppm and g/t from two labs, re-assays, detection limits, clustered infill; Layer 2: change of support to the selection block), decisive_step: analytical, chain: 4 inferences (cell-declustering of the infill-biased composites, variogram with nugget and short structure, block variance by volume-variance relation, support-corrected grade-tonnage against the tiers), judgment: variogram-based dispersion variance and which estimator represents block-selected grade, one_fact: none that fully rescues it. "Correct for change of support" would narrow it but still leaves the declustering, variogram and variance-ratio work, so the task is not a one-fact stump.
The field's own analysis (volume-variance and recoverable-resource estimation) decides the answer. The easy routes are the declustered composite curve (231 koz, Tier C) and the kriged block model (96 koz, Tier A).

## Fix
solution (rubric tolerance only). State in the answer blocks and rubric that the tonnes and grade cells above 2.5 g/t are method-dependent, with the gold at 2.5 g/t the committed value. Tolerate about 10% on tonnes and grade, and about 5% on ounces at the other cut-offs, so a lognormal or affine support correction both score. Make no prompt or pack change.

## Re-judge of the FIX_NOW (one pass, 2026-11-08)

Isolated Sonnet thread on the fixed answer 3 (brief judge_brief_r2.md): **DETERMINISTIC, APPROVE.** The affine rows
against the lognormal rows at the golden's variance ratio differ by at most 13.2 per cent in tonnes (1.5 g/t), 5.6 per
cent in grade (2.5 g/t) and 10.5 per cent in gold (1.5 g/t), all inside the stated bands (14, 6, 11); at 2.5 g/t both
corrections give Tier B and round to 150,000 oz (147.6 and 140.7 koz); the declustered composites (229 koz, Tier C)
and the kriged model (96 koz, Tier A) fall far outside the tolerance. Nothing else in the graded blocks is a fork.
