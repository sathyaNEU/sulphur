# determinism judge, task9, pass 2 (re-judge after repairs), 2026-11-13

Scope: Gates A to E and FIX LOCATION only. One thread, no sub-agents, no own derivation before the blocks. The pack was unzipped fresh to /tmp/determinism-task9-r3/target/ (29 files). Pass 1's report was not opened. Hygiene, Gates F to H and the design note were not read or run.

## Verdict
**NOT_DETERMINISTIC** (narrow; one fork on the plan's showerhead row, plus one unreproduced composite). Taxonomy: answer_contradicts_files.
**Disposition:** SEND_BACK. The fix touches what solvers see (one row of the plan PDF, or evidence in the pack), so prior runs are invalidated. If the author judges the "no hardware change planned" reading sufficient, the fix drops to the blocks and the finding below becomes a sentence in the note, but that is the author's call, not the files'.
**Fix location:** input_files (plan row "ILD0 deposition"), plus solution (band or arithmetic for 65.3).

## Why
Every figure in Supplementary 1, Critical Components 1 to 2 and the arithmetic behind Critical Component 5 reproduces from the shipped files. Two things do not close:

1. **Plan versus PM log (Gates B/C, Final Recommendation, Supplementary 2 cause 1 and 3).** `vr90_ramp_plan_q1_2027.pdf` §3 says "both chambers of each tool on the qualified SH-300-C (ECN-2026-0388); no hardware change planned". `equipment_pm_log.xlsx` holds exactly one showerhead swap (DP2B, 6 April 2026, B to C), and ECN-2026-0388 says SH-C replaces SH-B "at each chamber's next replacement". Read literally, the plan puts all six chambers on SH-C in Q1 2027. The golden treats DP2B as the only SH-C chamber, so SH-300-B on DP2B adds 0.76 points. Only one chamber ever ran SH-C, so whether the thick edge belongs to the SH-C part type or to DP2B's unit cannot be separated from the data. Literal reading: the 0.76, the 65.3 and the 45.4 are not forced, and no shipped file sizes the alternative.
2. **VR90 composite (Gate A/C on 65.3 and 45.4).** I could not reproduce 65.3 within its band. My independent estimate, tiling VX40 Q1 maps with 2x2 blocks (337 mm², close to VR90's 320 mm²) for those wafers polished on CM1 or CM3, gives 0.6715 clear of bins 2 to 6 and 8, times 0.981 design-limited, area-adjusted to 320 mm², about 67.2 per cent. The stated band is 64.3 to 66.4, so my tiling rival sits 0.8 above its top. The golden's extra 2 to 3 points of loss (VR90 P1 time of 76 s, deep-etch residue, dispatch to the high-scratch polishers) are plausible but are not derivable from a single named shipped figure. The remaining steps (7 and the final chain) rest on this composite.

## Evidence (recomputed on the shipped files)
| Figure | Stated (band) | Recomputed | Reproduced |
|---|---|---|---|
| VX40 shortfall, final insertion, Q1 vs Jun-Sep | 25.2 (24.0 to 26.8) | 25.25 (start_time or end_time basis); first insertion 25.56; all rows 25.33 | yes |
| VP12 shortfall | 34.8 (32.2 to 36.0) | 34.84 (start), 34.80 (end); first insertion 33.41; all rows 33.11 | yes, all alternatives in band |
| CM3 bin 5 per VX40 wafer, pre 2 June and slowed (standby aside) | 18.4 and 47.8 | 18.38 and 47.83; fail-free die basis 18.6 and 49.7 | yes |
| CM2 bin 5 | 10.1 and 11.7 (10.2 and 11.8) | 10.12, 11.74 (10.18, 11.84) | yes |
| Slurry loop cost per VX40 wafer | 7.3 (6.7 to 9.0) | raw bin 5 excess over each polisher's own pre-June mean, 8.47; times the 0.865 good-die survival that also reproduces the 6.2 below, 7.3 | yes |
| DP2B-on-CM3 share of VX40 wafers | 9.5 per cent | 9.47 per cent | yes |
| Edge cause (SH-C with R8) | 10.6 (10.0 to 13.0) | raw bin 3 and 4 excess 12.45, times 0.865 gives 10.8 | yes |
| CM3 recipe alone | 1.4 (no band) | raw net of 7.2 recovered minus 5.4 newly failing, about 1.7, about 1.5 as good die | close (Critical Component 2 and Supplementary 2 carry no band on this figure) |
| R8 thin-edge fails | 6.2 | 7.18 raw, 6.2 good | yes |
| Chemical life cost | 4.3 (3.7 to 5.6) | bin 6 excess 4.79 raw, 4.1 to 4.3 good | yes |
| Polymer cost | 2.1 (1.5 to 3.0) | bin 8 on ET1B and ET3A rises above about 196,000 RF seconds since clean (87 to 134 vs 62 to 70 on ET1B); not isolated to a single figure | direction yes, figure unverified |
| Sum | 10.6+7.3+4.3+2.1+0.9 = 25.2 | consistent with the 25.2 shortfall | yes |
| Ranking separation | bands 10.0-13.0, 6.7-9.0, 3.7-5.6, 1.5-3.0 | bands do not overlap | yes |
| Clean interval | 1,420 (1,300 to 1,550) | 196,000 RF s over (0.21 x 186 x 1.72 + 0.79 x 90.3) = 1,417; chambers ET1B and ET3A flake from the 180,000 to 196,000 bin in `etch_chamber_monitors.csv` | yes |
| Alternative, RF seconds only | 1,840 (outside band) | 196,000 / 110.4 = 1,775 | rival excluded by the monitors |
| Alternative, wafer counter | 2,400 | the plan's fleet standard; excluded by earlier flaking on ET1B and ET3A | rival excluded by the monitors |
| Plan loading | 31 lots per bench-day | summer actual 24.9 (WB-1) and 23.4 (WB-2) from `pgc_bench_controller.jsonl` (WB-2 in UTC, restart repeats dropped); Q1 24.7 and 22.6 | supports 1.6 vs 3.1 |
| Random-defect clear fraction | 75.4 per cent | VX40 2x2 blocks 0.744, VX40 1x4 0.739, VP12 2x4 0.739, VP12 1x7 0.756 | yes |
| Alternative, Poisson on die rate | 61.5 per cent overall | 0.709 clear fraction at 84.28 mm² scaling vs 0.754, about 61.4 overall | ruled out by the block maps, outside the band |
| VR90 all fixed | 65.3 (64.3 to 66.4) | tile estimate 67.2 (CM1+CM3 wafers), 66.9 on all polishers | **not reproduced, 0.8 above the band** |
| Starts with every cause fixed | 3,520 (3,470 to 3,580) | 412,000 / (184 x 0.653 x 0.992 x 0.981) = 3,524; line scrap is 0.2 per cent (13,450 started, 13,423 sorted), giving 3,531 | arithmetic yes; depends on 65.3 |
| Starts under the plan | 5,070 | 412,000 / (184 x 0.454 x 0.992 x 0.981) = 5,067 | arithmetic yes |
| Slurry, etch, chem, SH-300-B gains to VR90 (8.3, 5.5, 3.1, 0.76) and the 52.1 shortcut | as stated | not independently reproduced | open |

## Competing answers that survived
- **F1, showerhead population under the plan.** Answer A (golden): only DP2B is on SH-C, so SH-300-B on DP2B is worth 0.76 points and the plan yield is 45.4. Answer B (the plan's literal wording): all six chambers are on SH-C, so a thick-edge loss applies on more than one chamber and the fix is wider; no shipped file says whether the edge belongs to SH-C or to DP2B. Rule meant to close it: ECN-2026-0388's "at each chamber's next replacement" and "no hardware change planned", but those leave the plan's "both chambers of each tool" standing.
- **F2, number and ranking of causes.** The golden counts the showerhead and the R8 tune as one cause because they cancel on DP2B wafers off CM3. Taken as two causes (6 April and 11 May changes), raw excess is 5.3 for SH-C and 7.2 for R8, so the order becomes slurry 7.3, R8 about 6.2, SH-C about 4.6, chemical life 4.3, etch 2.1. This is closed by the data (neither fix alone removes the loss; the cancellation shows in `ild0_thickness_49pt.csv` and in the per-group table above), so it survives only as the hurried reading, not a fork. No action, provided the prompt keeps "the fix that removes it".
- **F3, VR90 all-fixed level.** Tile estimate 66.9 to 67.2 against the golden 65.3 with a band top of 66.4. If the author's model adds terms (P1 time, polymer residue at the 1,420 interval, CM1/CM3 baseline scratch), they should be shown as derived from named shipped values; otherwise widen the band or recentre it.

## Gate by gate
- **Gate A:** Supplementary 1, Critical Components 1 to 3 and the starts arithmetic reproduce; blocks agree with each other (25.2 = sum of causes, 3,520 and 5,070 follow from 65.3 and 45.4). 65.3 itself, the four VR90 per-cause gains and 52.1 are not independently reproducible here (see F3).
- **Gate B:** every decisive fact is in the pack (plan, PM log, ECN register, line list, facilities log, product data sheet with oxide areas, cost file not used). The one decisive fact that is not stated is which chambers run SH-C at VR90 start (F1).
- **Gate C:** F1 and F3 above. Margin tests: ranking bands are disjoint; Poisson, RF-seconds-only and wafer-counter rivals fall outside their bands and are ruled out by the block maps and monitors. The ET and chemical alternatives and the loading alternative (summer vs plan) are named in the blocks and closed by the plan's 31 lots a day.
- **Gate D:** difficulty comes from analysis (standby fortnight, CM1's clock 4 minutes fast, CM3 German locale and day-first dates, period in pre-cut-over lot IDs, WB-2 in UTC, final insertion per wafer all handled consistently in the recomputation).
- **Gate E:** asks are unit-bearing and pin the windows. "Which causes" does not state a count, closed by the golden's counterfactual (F2). "Wafer starts the commitment needs" is fixed by the plan (412,000 good units, 99.2 and 98.1 per cent, 184 gross die). Dispatch share between CM1 and CM3 ("bay rules used today") is not stated numerically; it moves the slurry gain by under 1 point, inside its band.

## Next action for the author
Close F1 by making the plan's ILD0 deposition row state which chambers run SH-300-C at VR90 start (or ship a record that lets a solver tell the edge belongs to the part type or to DP2B alone), then restate 65.3 and its band from named shipped values so that a 2x2 block tiling of the Q1 VX40 maps (about 67) falls inside it or is explicitly ruled out. Rebuild, re-run the gate script, and re-judge once.
