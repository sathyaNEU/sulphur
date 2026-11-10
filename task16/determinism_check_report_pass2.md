# Verdict, task16 pass 2

Order of work kept: own_derivation.md was written to disk from prompt and target/ only, before graded_blocks.md was opened.

- **Verdict:** DETERMINISTIC SOLUTION_WRONG (minor, in point values only; every band still closes the rivals I ran)
- **Disposition:** FIX_NOW. Re-state three point values or notes in the solution blocks (below); prompt and pack stay byte-identical, no model rerun.

**Why:** The call (name B) is forced under every structure I could defend. Once pooled dev loss is replaced by expert-item dev loss (bench = 1.007 x E + 0.0078, resid 0.006, 28 sha-matched scored runs; pooled dev has 2,000 vendor-labelled items) and the route costs are read from same-total contrasts, B leads C by 0.03 to 0.044. Weakest points: B's point 0.624 leans on a width-512 gain the pack does not show, and the headline contractor cost 0.0010 is the weaker of the author's two readings. The stated bands cover both. Gates A to E pass with those caveats (taxonomy: none).

**Evidence (recomputed, all from target/):**
| Item | My value | Golden (band) | Result |
|---|---|---|---|
| Trial w128 exp128k+map384k, 3 seeds | 0.6855 shift, 0.6848 regression, 0.6838 ratio (seed values 0.682, 0.684, 0.689) | 0.685 (0.680-0.690) | Reproduces; band closes calibration and seed forks |
| Map cost per tenth, same total 128k, w128 lr2e-3 (vs exp128k 0.6622) | 0.0114 at 50% (exp64k+map64k), 0.0113 at 75% (exp32k+map96k) | 0.0105 (0.0095-0.0125) | Reproduces; linear in fraction |
| Contractor cost per tenth | 0.0024 at 50%, 0.0018 at 75% | 0.0010 (0.0005-0.0032) | Band covers; point is the weaker reading (author's own alt reading gives 0.0020) |
| 512k expert, w128 lr2e-3 | level(512k) = trial less 7.5 x map cost = 0.600 to 0.607; exp64k+map448k run gives 0.602 to 0.609; Neff-weight single curves fitted to all w128 lr2e-3 runs give 0.597 to 0.607 | 0.607 (0.595-0.613) | Inside band. Ladder-only straight line (0.55-0.575) excluded by data: the 256k and 512k totals sit above it |
| B (w512, exp128k+ctr128k, lr5e-4) | w256 same labels 0.632 (bench); w128 0.634; w512 shows no gain over w256 at 128k expert (0.666 vs 0.652-0.655), so my direct estimate is 0.633-0.646 | 0.624 (0.615-0.650) | Point is 0.01-0.02 below any observed neighbour; band closes my range; the stated 80% range 0.609-0.638 is too low by my estimate |
| C | 0.598-0.613 under single-curve fits, 0.664-0.668 under additive-cost + diminishing-return structure | 0.668 (0.648-0.689) | Band excludes the single-curve rival; excluded by data (the single curves miss the 512k-total trial by 0.02, same side) |
| A (w1024), D | A 0.65-0.70 (only a TIMEOUT run, 0.864 vs 0.854 w512 at 70%); D 0.665-0.69 | A 0.663 (0.65-0.72), D 0.678 (0.66-0.697) | Closed by bands; their order is correctly not claimed |

Competing answers: C wins only under single-curve or Neff-weight fits that misfit the 512k-total runs by 0.02 to 0.03; ranking on logged pooled dev loss names C (about 0.55, below every scored run). B stays ahead of A (about 0.67) and D. I found no surviving rival for the recommendation. B vs C margin is 0.03 to 0.044 on the structure the data supports; on a no-interaction saturating-map reading it narrows to a tie (C about 0.642, B about 0.64), which the same-total contrasts reject because map cost is linear in fraction.

Residual forks, all inside the stated bands: calibration form (0.684 to 0.686), seed averaging, "a training set" size for the per-tenth costs (cost is size-constant in the data, so benign), A's learning rate, ctr+map interaction (no run combines them), 80% range width (bands 0.010-0.040 half-width).

**Files/Hygiene:** PASS, no exclusion-level finding. 16 files: csv (11), xlsx, md, sh, yaml; no README, no authoring language. Three logger dialects, duplicate uploads, killed/failed runs, superseded shard CTR-0019, lost dump are genuine process noise. Large csv: tracking_metrics (190k rows), dev_item_loss (8000 x 128). Distractors present (slurm, gpu probe, folk classes). Temporal: contractor lot registered 19-22 Oct, ctr trials started 26 Oct onward, so they used the re-registered shard. Not public data.

**Stump power:** Moderate to good. Four traps do the work: pooled dev loss contaminated by vendor labels (surface read, flips C to first), stale ladder learning rates (about 0.03 at w128), the bend past the 128k expert pool (straight-line ladder gives 0.55 vs 0.607), and untested w1024 and ctr+map combos. A careful solver who tests expert-item loss and same-total contrasts still has to choose an extrapolation form, so partial credit is graded.

**Stumping type:** `mechanism: forecasting` (with method_or_model_selection), `stumping_family: mixed` (analytical core, one surface-read layer), `surface_read_dependency: no` (primary), `sole_data_defect: no`. The dev-loss contamination is real but is one of several results; on clean data the extrapolation, cost decomposition and width/lr questions would still stump.

**Deep reasoning:** `domain: pass` (swap test: learning-curve forecasting with label-route costs is native to ML-for-seabed-mapping), `layers: pass` (layer 1: three logger dialects, sha-joins, duplicates, mixed-label dev split; layer 2: calibration, cost decomposition, bend forecast, backtest, interval), `results: 6 graded across 5 areas` (assembly, measurement, decomposition, forecasting, validation, uncertainty), `one_thing: none`, `effort: quick 1, careful 3, thorough 5 of 6`, `one_fact: "the dev set is part vendor-labelled, score on expert items" rescues 2 of 6` (calibration and trial figure, plus part of the ranking). Weight sits in the cost decomposition and the bend; a careful but hurried run likeliest loses the 512k figure, filing about 0.55 to 0.57 from the ladder straight line (or about 0.597 from an all-run curve, just under the band).

**Fix:** solution only. (1) Soften B's width step: either carry w512 as w256-like (B about 0.632-0.64) or widen B's stated range to about 0.609-0.650 and say the width step at 512 is extrapolated. (2) Use 0.0020 (the same-total reading, matches my 0.0018-0.0024) as the contractor headline, keeping the 0.0005-0.0032 band. (3) In the Step 5 text, say the cost constancy across totals is supported by same-total contrasts (0.0114 and 0.0113 at 128k), which is what pins the bend. Pack and prompt unchanged.

Cross-batch fingerprint: could not be run (no other deliverables inside the permitted directory); not assessed.
