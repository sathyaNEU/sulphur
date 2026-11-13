# Determinism check, task9, pass 3 (re-judge, fresh unzip in /tmp/determinism-task9-r4/target/)

**Verdict:** DETERMINISTIC (one unbanded figure to tidy).
**Disposition:** FIX_NOW (answer-block wording only; nothing solvers see changes).

## Evidence (recomputed from the shipped files by the blocks' own method)

| Figure | Block value (band) | Recomputed | Status |
|---|---|---|---|
| VX40 shortfall, final insertion, Q1 vs Jun-Sep (sort end time) | 25.2 (24.0-26.8) | 25.25 (658.0 vs 632.75) | reproduced |
| VP12 shortfall | 34.8 (32.2-36.0) | 34.80 (1290.36 vs 1255.57) | reproduced |
| Fork: window on start_time not end_time | | 25.25 / 34.84 | in band |
| Fork: first insertion only | | 25.57 / 33.36 | in band |
| Fork: all insertions averaged | | 25.33 / 33.06 | in band |
| Bin 5 per VX40 wafer, CM3, pre-2 Jun / post excl. standby fortnight (CM1 clock -4 min, CM3 German locale parsed) | 18.4 / 47.8 | 18.4 / 47.8 | reproduced (41.9 if the standby fortnight is left in, which the block names and excludes) |
| Bin 5, CM2 pre / post | 10.1 / 11.7 | 10.1 / 11.7 (standby 10.0) | reproduced |
| Edge pattern: DP2B off CM3 fails bin 3 (57.9), other chambers on CM3 fail bin 4 (43.1), DP2B on CM3 clean (0.67/0.41) after 12 May | as in blocks | as stated | reproduced |
| DP2B-on-CM3 share of VX40 wafers | 9.5 per cent (no band) | 9.2 (polished Jun-Sep), 10.9 to 11.4 (other windows) | window-dependent, see Fix |
| Starts: 412,000 / (0.992 x 0.981) / (184 x yield) | 3,520 at 65.3 per cent; 5,070 at 45.4 per cent | 3,524; 5,068 | reproduced from the plan |
| VR90 product of survivals 0.754 x 0.897 x 0.989 x 0.996 x 0.981 | 65.3 | 65.4 | arithmetic consistent |
| Cause costs 10.6 + 7.3 + 4.3 + 2.1 + 0.9 | 25.2 | 25.2 | adds to the VX40 shortfall |
| 4-die block (2 x 2, 1 x 4) clear of bin 8, Q1 VX40 | cluster, slower than Poisson | 0.739 / 0.738 vs Poisson 0.700 | supports the block-yield reading |
| Clean interval: flake at 196,000 RF s; per-wafer standard-equivalent RF at 21 per cent deep with 1.72x = 0.79 x 90 + 0.21 x 186 x 1.72 = 138 s | 1,420 (1,300-1,550) | 196,000 / 138 = 1,420; monitors on ET1B and ET3A at 196k s or more carry about 50 adders against about 10 elsewhere | reproduced |

Not rebuilt in full (one pass, about 25 calls): the T3 metals and gate-oxide fit (98.9, 4.3, the 3.1 and 1.6 point gains), the scratch survival 89.7 on VR90 die, the as-filed 45.4 and the per-cause "alone" gains other than the arithmetic above. These rest on model fits and were not checked beyond consistency.

## Forks run

- Poisson die-area formula from VX40 die yield gives 61.5, and a cluster factor of 2 gives 62.8. Both fall outside the 64.3-66.4 band, but the files rule them out by a named fact (block clear-yield at 4 die is 0.739, not Poisson 0.700).
- 2 x 2 tile unscaled to VR90 area gives about 0.739 against 0.754, so about 64.0 against 65.3. This sits 0.3 under the band floor of 64.3. The block says "at VR90's own die area" (320 against 337 mm2), which closes it, and an area-scaled tile (power 0.95) gives about 65.0, in band. Marginal, not a fork.
- CM1 and CM3 dispatch share for VR90 ("bay rules used today", ECN-2026-0480): no rule is filed, so it comes from VX40's history. CM3 share of VX40 CM1+CM3 wafers runs 0.45 to 0.80 by month, 0.51 in Q1 and about 0.58 over the full record. By my sizing the share changes the slurry-loop gain by under 1 point, inside its 7.5-9.7 band, but I did not run the full VR90 model. Worth the author confirming that the as-filed 43.7-46.4 band holds for a share of 0.5 and of 0.6.
- Far-polisher consumables reading gives a loop gain of 5.0. It is outside the 7.5-9.7 band and ruled out by named facts (the excess vanishes on the standby pump and rises with tap distance in the line list).
- Scaling the clean by RF time alone gives 1,840 wafers. It is ruled out by the monitors flaking earlier wherever CT-DEEP-07 ran.
- Splitting cause 1 into a showerhead and a recipe cause: neither alone removes the loss (cells above), so the one-cause ranking is forced by the data.

## Gates B, D and E

Every decisive fact has a shipped home: the plan PDF (starts, conditions, 1.9 per cent design-limited fallout, back-end yields, 184 gross die), the product data sheet (gate oxide areas), the facilities change log (51.5 to 38 Hz, standby pump), the ECN register, the line list (distances), and the recipe change log. The recommendation's terms (pre-gate clean, SH-300-B, P-02A setpoint, ET1B and ET3A, wet clean) all appear. The asks name their unit and period, and no hedge is possible. The shortfall asks do not say "final insertion", but the first-insertion alternative stays inside both bands.

## Fix (solution, answer blocks only)

1. Critical Component 2: "9.5 per cent of VX40 wafers" has no band or window, and I recompute 9.2 (polished Jun-Sep) to 11.4 (sorted Jun-Sep, or polished since 6 Apr). Either state the window that gives 9.5 and a band, or drop the figure.
2. Optional: state in Step 7 that the VR90 CM1/CM3 split is taken from VX40's observed split (no rule is filed), and confirm the as-filed 45.4 band holds for a CM3 share of 0.5 and 0.6.
