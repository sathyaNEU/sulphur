# determinism-check report, task9, 2026-11-13 (judge thread: Gates A to E only)

## Verdict
DETERMINISTIC, with SOLUTION_WRONG on a figure basis (see Findings). Not fully recomputed: the VR90 composite (65.3, 45.4, the 8.3 / 5.5 / 3.1 / 0.76 per-cause adds, the 3,520 starts) was only checked for magnitude and arithmetic, not rebuilt end to end.
**Disposition:** FIX_NOW (restate the Critical Component 1 figures on one basis; no pack change). Pending a full rebuild of the VR90 model by the author's own checks.
**Stumping type:** not run (out of scope).

## Why
Shortfalls, the cause ranking's bands, the polisher routing and the slurry-loop mechanism reproduce from the shipped files, and the ranked bands do not overlap. The VR90 yield chain rests on a modelling build I could only sanity-check. One basis inconsistency in Critical Component 1 and one framing fork (cause 1 as a joint cause) are noted.

## Recomputation ledger
| Figure | Claimed (band) | Judge recomputed | Reproduced |
|---|---|---|---|
| VX40 shortfall, final insertion, start_time dates | 25.2 (24.0 to 26.8) | 658.00 - 632.76 = 25.25 | yes |
| VP12 shortfall | 34.8 (32.2 to 36.0) | 1290.39 - 1255.55 = 34.84 | yes |
| Alt: first insertion only / all insertions, VX40 | in band | 25.56 / 25.33 | inside band |
| Alt: first insertion / all insertions, VP12 | in band | 33.41 / 33.11 | inside band |
| CM3 bin 5 per VX40 wafer, Q1 (by sort date) | 18.4 | 18.4 | yes (by polish date: 19.9) |
| CM3 bin 5 during slowed P-02A (polish time, 2 Jun to 10 Aug and 24 Aug on) | 47.8 | 47.8 (51.0 and 44.4 pooled) | yes, on polish date |
| CM3 bin 5 June to Sept by sort date (alt) | n/a | 31.9 | basis fork, see Findings |
| CM2 bin 5 Q1 / slowed | 10.1 / 11.7 | 10.2 (sort date), 9.6 (polish date) / 11.7 | yes, mixed basis |
| Standby pump 10 to 24 Aug 2026, CM3 / CM1 (polish time) | "fell back" | 12.9 / 18.5 (spring-level) | yes |
| CM1 slowed 36.9, CM4 about 20.4 vs Q1 14.5 and 11.8 | rises with distance | CM2 +1.5, CM4 +8.6, CM1 +22.4, CM3 +28 (64, 148, 231, 318 m) | yes, monotone |
| Cause sum | 10.6+7.3+4.3+2.1+0.9 | 25.2 | arithmetic yes |
| Bands of ranked causes | 10.6 (10.0-13.0), 7.3 (6.7-9.0), 4.3 (3.7-5.6), 2.1 (1.5-3.0) | adjacent bands do not overlap | ranking forced |
| Clear-of-bin-8 yield of blocks, Q1, VX40 2x2 = 0.737, 1x1 = 0.913; VP12 3x3 = 0.717, 1x1 = 0.952 | VR90 random-defect survival 75.4 per cent, cluster factor 0.66 | interpolated to 3.8 VX40-die or 7.3 VP12-die about 0.75 to 0.76; clearly not Poisson | approx yes |
| Starts: 412,000 / (0.992 x 0.981) / (184 x yield) | 3,520 at 65.3; 5,070 at 45.4 | 3,523; 5,068 | yes |
| Rival 52.1 via same arithmetic | 4,416 starts | consistent | arithmetic only |
| VR90 slurry-loop gain rough check (VX40 excess about 3.3 per cent of die, area x3.8) | 8.3 points | about 6 to 8 points | magnitude only |
| 65.3, 45.4, 8.3, 5.5, 3.1, 0.76, 1.72x, 1,420 cleans | stated bands | not rebuilt | NOT recomputed |

## Competing answers that survived
1. Window basis of "before" and "during" bin 5 means (Critical Component 1): Q1 baseline by sort date (18.4) against slowed-window by polish date (47.8). A consistent polish-date baseline gives 19.9 and 9.6; a sort-date June to Sept mean gives 31.9. Not graded against a band; the claim's text needs one basis.
2. Cause 1 as a single joint cause (DP2B SH-300-C with CM3 R8 tune, 10.6) versus two separate causes (showerhead, recipe tune). The prompt does not say how many causes there are. The files back the joint reading (DP2B wafers on CM3 show no excess, which rules out independent attribution), so I rate this closed by data, but a rival split into five rows would change ranks and the 1.4 figure; worth a pinned sentence in the note.
3. VR90 polisher mix: ECN-2026-0480 only says "bay dispatch rules used for VX40 and VP12"; those split lots across all four polishers (CM3 favoured after DP2). The CM1/CM3 routing is derivable only from ILD0-VR recipe lines appearing solely in CM1 and CM3 exports (and CM3 R7/R8 split). Derivable, but it is the single inference all VR90 results lean on; no band covers a CM-mix rival (CM2/CM4 would remove the far-tap loss).
4. Plan as filed already returns CM3 to R7 on 23 Nov (ECN-2026-0466, plan section 3), yet the Final Recommendation lists CM3's standard recipe as a fix to make; the VR90 "alone" adds list omits it (0.76 for SH-300-B only). Consistent, but the recommendation reads as if the plan lacks it.

## Spec gates
Not in scope for this pass (determinism only); file spot check: 29 files, formats csv, xlsx, sqlite, pdf, txt, jsonl, yaml; fab2_yield.sqlite unzips fine.

## Findings, ranked
1. (Gate A, solution) Critical Component 1 mixes baselines (sort date Q1 vs polish-date slow window). Restate on polish time (CM3 19.9 to 47.8, CM2 9.6 to 11.7) or give the window.
2. (Gate A/C) The VR90 chain (65.3, 45.4, per-cause adds, 1,420 wafers) is not shown here to reproduce; bands are tight (about 2 points on 65.3 and 45.4) and rely on area-scaling choices (bin 5 per die area, bin 6 by gate oxide area, bin 3/4 per die) plus a cluster-factor fit; rivals 61.5 and 62.8 sit outside the band and are excluded only by the block-yield data, which does support the author (non-Poisson clearly visible above).
3. (Gate C/E) Cause 1 is a joint cause; pin its framing in the note.
4. (Gate E) Prompt says "sorted" date but does not pin which clock or insertion; all variants tried land inside both shortfall bands.

## Next action for the author
Rewrite Critical Component 1 on one date basis, then run your own full VR90 rebuild (`effort.py`/generator) and re-issue; no pack change required.
