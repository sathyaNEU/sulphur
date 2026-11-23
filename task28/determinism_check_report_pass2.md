# Determinism Check Report: task28 (Pass 2)

- **Verdict:** DETERMINISTIC
- **Disposition:** APPROVE (all Pass 1 `FIX_NOW` items closed cleanly; Gates A through E pass with zero open forks and zero remaining defects).
- **Fix location:** `none`

## Why

Every point estimate, physical falsification metric (F1, F2, F3), quarterly Q3 total, Schedule B EUR exposure, and 2026 screening discrepancy rate in `task28/submission.md` now rebuilds directly from a fresh extraction of `task28/target.zip` (confirmed byte-identical to `/tmp/determinism-task28-pass2/target/`) using only the explicit base-model specifications written in Steps 1 through 7, with zero guessing. All 22 defensible estimator, interpolation, boundary, and window forks across S1, S2, and S3 (including every Pass 1 exit/edge fork: S2 step-left, OU kriging, PCHIP, nearest 15-minute parcel, cubic spline, and S3 shared + inclusive `<=120h`) sit strictly inside every widened 26-variant band in `submission.md` (C1, C2, C3, plant total, overhaul subtotal, Q3 total, plant and overhaul Schedule B EUR, and all 8 individual train totals) while preserving the exact 4-of-8 overhaul slate (**OVERHAUL: TR07, TR06, TR01, TR02; MONITOR: TR04, TR03, TR05, TR08**). Every shortcut and rival route (including the strongest standard rival: pooled AR(1) + fixed wall-clock CCF lag + 2-class conditional-independence Dawid-Skene EM, `7,213.2 h`) remains widely separated from the widened bands and quantitatively refuted on F1, F2, and F3 / 128-cell LRT. The realism updates in `target.zip` (`intake_tep_z_index`, standardized Clause 2.2 baseline, `calendar_hours_2026`, `baseline_output_2026_km3`, `scheduled_output_2027_km3`, `dispatch_duty_ratio_2027`, and `post_cip_monitoring_cycle_hours`) are internally consistent to machine precision (`2.2e-16`), fully synchronized with `submission.md`, and open zero new forks.

## Evidence

### 1. Literal Step-by-Step Rebuild Verification (Gate A, Zero Guessing)

| Quantity | Blocks Value | Blocks 26-Variant Band | Literal Pass 2 Rebuild | Status |
|---|---|---|---|---|
| Overhaul Call (>= 400.0 h) | TR07, TR06, TR01, TR02 | 4 of 8 | TR07, TR06, TR01, TR02 | Exact match |
| Monitor Call (< 400.0 h) | TR04, TR03, TR05, TR08 | 4 of 8 | TR04, TR03, TR05, TR08 | Exact match |
| C1: Plant 2027 Permeate Boron | 1,328.7 h (2026: 947.0 h) | 1,053.9 - 1,390.7 h | 1,328.76 h (2026: 946.99 h) | Exact match (0.06 h) |
| S1 Correlation Scales & F1 | TR01 1.15 h, TR04 15.57 h; F1 0.0479 | Point | TR01 1.15 h, TR04 15.57 h; F1 0.0485 | Exact match |
| C2: Plant 2027 Scaling | 1,652.7 h (2026: 1,235.2 h) | 1,539.4 - 1,836.6 h | 1,652.72 h (2026: 1,235.25 h) | Exact match (0.02 h) |
| S2 Effective Volumes & F2 | TR02 692.0 m3, TR05 1,022.0 m3; F2 0.523 | Point | TR02 692.0 m3, TR05 1,022.0 m3; F2 0.5234 | Exact match |
| C3: Plant 2027 Structural | 1,106.9 h (2026: 979.3 h) | 1,042.6 - 1,251.1 h | 1,107.09 h (2026: 979.44 h) | Match (0.19 h, BFGS vs EM) |
| S3 Sensitivities & F3 | (0.887, 0.553, 0.429); F3 0.455 pp (Maj2 2.741 pp) | Point | (0.887, 0.553, 0.429); F3 0.453 pp (Maj2 2.741 pp) | Exact match |
| Plant-Wide 2027 Total | 4,088.4 h | 3,787.7 - 4,300.8 h | 4,088.56 h | Match (0.16 h) |
| Overhaul-Train 2027 Subtotal | 2,926.4 h | 2,707.5 - 3,064.2 h | 2,926.51 h | Match (0.11 h) |
| Plant-Wide Q3 2027 Total | 1,766.5 h | 1,630.7 - 1,850.5 h | 1,766.52 h (all 8 trains within 0.1 h) | Exact match |
| Plant Schedule B Exposure | EUR 1,750.8k (1,750,781.22) | EUR 1,624.1k - 1,841.9k | EUR 1,750,884.11 (0.006% EM/BFGS tol) | Match |
| Overhaul Schedule B Exposure | EUR 1,253.5k (1,253,546.01) | EUR 1,161.3k - 1,319.1k | EUR 1,253,616.93 (0.006% EM/BFGS tol) | Match |
| 2026 Screening Discrepancy | 120.8% (3,713.0 vs 3,161.5 h) | 112.3% - 125.4% | 120.83% (3,713.0 vs 3,161.67 h) | Exact match |
| TR07 (B / S / St; Q3) | 1,291.9 (535.6 / 503.6 / 252.6; 555.6) | 1,187.9 - 1,343.6 h | 1,291.91 (535.62 / 503.60 / 252.69; 555.6) | Exact match |
| TR06 (B / S / St; Q3) | 613.4 (68.9 / 118.5 / 426.0; 214.5) | 589.8 - 661.0 h | 613.46 (68.87 / 118.52 / 426.07; 214.5) | Exact match |
| TR01 (B / S / St; Q3) | 514.8 (285.2 / 183.0 / 46.6; 242.9) | 448.7 - 536.2 h | 514.78 (285.23 / 183.02 / 46.53; 242.9) | Exact match |
| TR02 (B / S / St; Q3) | 506.3 (60.7 / 376.3 / 69.4; 233.5) | 480.6 - 544.3 h | 506.36 (60.67 / 376.26 / 69.43; 233.5) | Exact match |
| TR04 (B / S / St; Q3) | 318.8 (124.3 / 142.6 / 51.9; 165.9) | 306.2 - 341.9 h | 318.77 (124.26 / 142.60 / 51.91; 165.9) | Exact match |
| TR03 (B / S / St; Q3) | 305.7 (59.2 / 160.8 / 85.7; 126.4) | 287.0 - 336.1 h | 305.75 (59.20 / 160.79 / 85.77; 126.4) | Exact match |
| TR05 (B / S / St; Q3) | 271.0 (157.8 / 12.9 / 100.3; 118.1) | 230.3 - 285.5 h | 271.08 (157.80 / 12.93 / 100.34; 118.2) | Exact match |
| TR08 (B / S / St; Q3) | 266.4 (37.1 / 155.0 / 74.3; 109.6) | 245.9 - 284.6 h | 266.45 (37.11 / 155.00 / 74.34; 109.6) | Exact match |

### 2. Pass 2 Fork Verification Against Widened 26-Variant Bands (Gate C)

Every one of the 22 defensible forks tested on Pass 2 preserves the exact 4-of-8 overhaul slate and lands **strictly inside** every graded band (C1, C2, C3, Plant total, Overhaul subtotal, Q3 total, Plant/Overhaul Schedule B EUR, and all 8 individual train totals):

| Fork | C1 (h) | C2 (h) | C3 (h) | Plant Total (h) | Call | All Graded Bands? |
|---|---:|---:|---:|---:|---|---|
| S2: Step-left flow integration + L2 | 1,328.8 | 1,560.3 | 1,107.1 | 3,996.1 | Unchanged | ALL IN |
| S2: Step-right flow integration + L2 | 1,328.8 | 1,603.4 | 1,107.1 | 4,039.3 | Unchanged | ALL IN |
| S2: Linear-trapezoidal flow + L2 | 1,328.8 | 1,648.4 | 1,107.1 | 4,084.3 | Unchanged | ALL IN |
| S2: Midpoint-trapezoidal flow + L2 | 1,328.8 | 1,561.4 | 1,107.1 | 3,997.2 | Unchanged | ALL IN |
| S2: Gaussian OU kriging on `intake_tep_z_index` | 1,328.8 | 1,690.7 | 1,107.1 | 4,126.5 | Unchanged | ALL IN |
| S2: PCHIP interpolation on `intake_tep_z_index` | 1,328.8 | 1,744.5 | 1,107.1 | 4,180.4 | Unchanged | ALL IN |
| S2: Nearest 15-min parcel on `intake_tep_z_index` | 1,328.8 | 1,800.3 | 1,107.1 | 4,236.1 | Unchanged | ALL IN |
| S2: Cubic spline on `intake_tep_z_index` | 1,328.8 | 1,814.7 | 1,107.1 | 4,250.6 | Unchanged | ALL IN |
| S3: Shared CIP clearing, tied D3, `<120h` | 1,328.8 | 1,652.7 | 1,184.3 | 4,165.8 | Unchanged | ALL IN |
| S3: Shared CIP clearing, tied D3, `<=120h` (31 blocks) | 1,328.8 | 1,652.7 | 1,231.5 | 4,213.0 | Unchanged | ALL IN |
| S3: Per-train CIP clearing, tied D3, `<=120h` | 1,328.8 | 1,652.7 | 1,104.4 | 4,085.9 | Unchanged | ALL IN |
| S3: Per-train CIP clearing, free D3 floor, `<120h` | 1,328.8 | 1,652.7 | 1,055.1 | 4,036.5 | Unchanged | ALL IN |
| S3: Per-train CIP clearing, `96h` / `144h` window | 1,328.8 | 1,652.7 | 1,179.7 / 1,151.4 | 4,161.2 / 4,132.9 | Unchanged | ALL IN |
| S3: Shared CIP clearing, `144h` window | 1,328.8 | 1,652.7 | 1,191.0 | 4,172.5 | Unchanged | ALL IN |
| S1: AR(1) OLS / WLS-N | 1,311.7 / 1,354.5 | 1,652.7 | 1,107.1 | 4,071.5 / 4,114.3 | Unchanged | ALL IN |
| S1: Continuous OU (1h-block avg, OLS / WLS-N) | 1,063.4 / 1,099.3 | 1,652.7 | 1,107.1 | 3,823.2 / 3,859.1 | Unchanged | ALL IN |
| S1: AR(1) 4-hour-only / 0.5% trimmed / lab noise OFF | 1,364.9 / 1,253.8 / 1,357.2 | 1,652.7 | 1,107.1 | 4,124.7 / 4,013.6 / 4,117.0 | Unchanged | ALL IN |

Rival separation remains intact across every widened band: C2 lower bound (`1,539.4 h`) stays `292.5 h` above fixed wall-clock CCF (`1,246.9 h`, F2 RMS `1.776` vs `0.523 mS/cm`) and upper bound (`1,836.6 h`) stays `3,469.4 h` below comonotonic pairing (`5,306.0 h`); C3 upper bound (`1,251.1 h`) stays `895.0 h` below post-CIP majority vote (`2,146.1 h`) and `3,568.0 h` below 2-class conditional-independence Dawid-Skene (`4,819.1 h`, 128-cell LRT `2*dNLL = 169.8 / 99.7`, `p < 1e-20`); C1 band (`1,053.9 to 1,390.7 h`) remains cleanly separated from raw composites (`285.6 h`, F1 `1.0045`) and i.i.d. scaling (`6,093.0 h`, F1 `0.4955`), while pooled AR(1) (`F1 = 0.2248-0.2293`) is refuted by moment conservation and flips both TR01 and TR04.

### 3. Gates B, D, E and Realism Sync

All 8 terminology/schema consistency checks pass (`standardized intake algal-TEP precursor index > 1.50` in SWRO-Q27 Clause 2.2, `intake_tep_z_index` in `intake_chemistry_15m_2026.csv` and `submission.md`, zero stale `mg/L eq` strings, `calendar_hours_2026` / `baseline_output_2026_km3` / `scheduled_output_2027_km3` / `dispatch_duty_ratio_2027` in `operating_plan_2027.csv` with exact ratio match `2.2e-16` and Annex B `R_duty`, and `post_cip_monitoring_cycle_hours: 120` in `scada_bay_config_2026.json`). Gates A through E all pass cleanly.

## Fix

None.
