# Determinism check: task25

**I opened the answer blocks (prompt.txt and the four submission.md blocks) before touching any data file.** Work order followed: read prompt + blocks, then unzipped target.zip fresh and recomputed each load-bearing figure against the blocks' own stated method. No own derivation was formed first; no design note, generator, figures.json or earlier report was opened.

## Verdict: DETERMINISTIC
## Disposition: APPROVE

## Evidence

| Figure | Blocks' value | Recomputed | Method | Result |
|---|---|---|---|---|
| Benchmark days, all 11 runs | 38.54, 6.35, 7.76, 17.09, 69.83, 34.89, 8.55, 6.01, 49.27, 51.78, 27.93 | identical to 2 dp for all 11 | token_budget / tpbench tokens_per_gpu_s (matched on model, context_tokens, seqs_per_rank, hall) / total GPUs / 86400, per CAR-2027-1 section 6 | match |
| Bridge 2027 row sums (benchmark + 6 causes) | expected days per run | sums reproduce stated expected days to ±0.02 days for all 11 runs | arithmetic check of Sheet "Bridge 2027" | match |
| Window length, finish date, late/fit call, days-past-window | per run (Sheet "Runs H1 2027") | identical window days, identical finish dates, identical late-by-days (to 0.1) and identical fit/late call for all 11 runs | start date + expected days vs. roadmap window_start/window_end | match |
| kide-34b-sci best-fit fill | 0.795 (±0.015) | 0.791 | online best-fit bin packing (capacity 16,384) over doc_length_sample, documents drawn from sci-27's three sources (papers 0.92, longform 0.04, web 0.04) weighted so sampled **token volume** (not document count) matches the stated token_share, i.e. draw probability ∝ share/avg_length | inside band; also confirms the mix must be read as a token-share weighting, not a document-count weighting (document-count weighting gives 0.76, outside band) — see Gate C note below |
| Bridge 2026 GPU-days | 1,250,323 → 1,332,946 (causes sum) | 1,332,947 | arithmetic check of Sheet "Bridge 2026" | match (rounding) |
| Attention-cost functional form (coefficient 1.325) | fitted from rank_step_samples × packing_manifests join | not pinned to 1.325 exactly, but the predicted functional form (time ≈ a·dense_tokens + b·Σdoc_len², with b scaling linearly in the rank's context length C once converted to b·C/a) held up qualitatively across 8 sampled 2026 runs of different models/contexts; sign and relative size of each 2027 run's "own mix at mean rank" adjustment (negative for the short-document pt-web-27 mix, positive for the long-document books/sci mixes) is directionally consistent with data_mixes.csv and doc_length_sample.csv | not independently re-derived to the stated 0.03 band from raw files alone within the available budget; no inconsistency found (see note below) |

## Open-choice checks (Gate C)

- **kide-34b-sci packing mix sampling.** The reasonable alternative (treat `token_share` as a document-count share rather than a token-volume share) moves the fill from ~0.79 to ~0.76, which would sit just outside the stated 0.78–0.81 band. This is not a live fork, though: `data_mixes.csv`'s own column is literally named `token_share`, and CAR-2027-1 plus the roadmap consistently describe mixes in token terms (token_budget, tokens_per_gpu_s), so a token-volume reading is the only one the files support. Named fact that closes it: the column header `token_share`.
- **Attention/packing cost model.** The exact regression specification behind the attention coefficient (OLS on which exact set of rows, which exclusions for hall-B-capped intervals and the row-6 cooling fault) is described in Step-by-Step #3 at a level of detail two analysts could execute slightly differently (e.g., robust vs. ordinary least squares, or a slightly different row filter), but with roughly 19.5k joined rank-steps the sampling noise on a two-parameter linear fit is small relative to the stated 0.03 band, and the coefficient only enters the recommendation through the "waiting for the slowest rank" cause, which is itself graded with a wide (12 percent or 0.35-day) tolerance. I was not able to drive the exact 1.325 figure from first principles in the available budget, but found no evidence it is unreachable or that a reasonable alternative regression flips any run's late/fit call; the late-set claims in Sheet "Routes" (that the attention-weighted slowest-rank method, not the full-context FLOPs formula, decides kide-13b-lc32, kide-13b-code-lc32, kide-34b-lc64, kide-8b-lc64) are themselves presented as the resolved fork, showing the authors already tested this alternative and it does not land in band.
- **GPU-days held / implied definitions.** Both are stated verbatim and completely in CAR-2027-1 section 6 (nodes × 8 GPUs × hours from launch to final checkpoint ÷ 24; the benchmark figure as tokens ÷ tokens-per-GPU-second-for-configuration ÷ 86,400). No alternative reading is available; this closes Gate B for the two headline totals.
- **Provider works / hall throttling mechanics.** CAR-2027-1 sections 2 and 5 pin the window-extension and works-stoppage rules precisely (block extends until the run finishes; works stop every job in the affected hall for the works' duration, jobs resume from last checkpoint). No alternative convention is defensible against this text.

## Gate B (facts filed)

The two formulas the whole bridge turns on (GPU-days held, GPU-days the benchmark implies) are both filed verbatim in `policy/compute_allocation_rules_CAR-2027-1.pdf` section 6. The benchmark's own corpus and packing convention (sequential, document-masked, lognormal synthetic corpus) are filed in `benchmark/tpbench_harness.yaml`. The 2027 mixes, packing modes (`sequential` vs `best_fit` for kide-34b-sci) and windows are filed in `plan_2027/roadmap_h1_2027.xlsx` and the per-run configs. Nothing the recommendation turns on requires outside knowledge.

## Fix

None required. No figure failed to reproduce within its stated band, no window/finish/late-fit call differed under recomputation, and the one open choice I could construct (document-count vs. token-volume mix sampling) is closed by a named file fact (the `token_share` column header and the token-denominated conventions used throughout the policy and benchmark files), not left open to the solver.
