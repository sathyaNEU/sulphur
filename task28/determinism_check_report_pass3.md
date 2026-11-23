# Determinism Check Report (Pass 3) - task28

- **Verdict:** DETERMINISTIC
- **Disposition:** APPROVE
- **Fix location:** none

## Summary

The Pass 3 Physical & Environmental Sciences reframing of `task28` (`prompt.txt`, the 14 shipped files in `target/`, and `submission.md`) passes Gates A through E cleanly. Every load-bearing figure in `submission.md` reproduces from the shipped 2026 logs and 2027 operating plan, every operative rule, threshold, energy rate, lab repeatability SD, Annex B multiplier, Clause 4.4 formula, and Annex C CSV column (`energy_2027_mwh`) is filed literally in `target/` with zero leftover EUR, Schedule B, or regulatory-compliance contradictions, and all 36 defensible modeling forks plus 6 independent +/-20% mode perturbations preserve the exact 4-of-8 2027 overhaul slate (`TR01`, `TR02`, `TR06`, `TR07` OVERHAUL; `TR03`, `TR04`, `TR05`, `TR08` MONITOR) while sitting inside the stated 26-variant estimation uncertainty ranges.

## Gate A & B: Recomputation and Filed-Fact Verification

All 14 shipped files were inspected independently (`swro_integrity_standard_q27.pdf`, `lims_qa_certificate_2026.pdf`, `scada_bay_config_2026.json`, `train_asset_register.csv`, `operating_plan_2027.csv`, `autosampler_schedule_2026.csv`, `permeate_boron_composites_2026.csv`, `intake_chemistry_15m_2026.csv`, `ro_feed_header_15m_2026.csv`, `train_hydraulics_hourly_2026.csv`, `shift_diagnostics_2026.csv`, `cip_wash_log_2026.csv`, plus the two out-of-scope regional distractors `mibel_iberian_power_spot_2026.csv` and `algarve_reservoir_levels_2026.xlsx`).

### Data Conformance (Step 1)
- `permeate_boron_composites_2026.csv`: 15,449 raw rows -> 15,024 unique bottles after keeping max `qa_revision` (425 superseded rev-1 rows dropped); 7,725 raw (7,512 clean) Portuguese `DD/MM/YYYY` dates and South-bay `ug/L` assays; zero NAs; zero exact `0.50` ties.
- `autosampler_schedule_2026.csv`: 2,920 rows, 720 Q1 legacy tags, exact 4h Thu-Mon / 8h Tue-Wed cadence.
- `intake_chemistry_15m_2026.csv` and `ro_feed_header_15m_2026.csv`: 281,095 - 775 = 280,320 and 281,154 - 834 = 280,320 clean rows (100% exact telemetry retries), giving 35,008 post-burn-in 15-min intervals per train after dropping the first 32 burn-in intervals (Clause 2.2).
- `train_hydraulics_hourly_2026.csv`: 70,258 - 178 = 70,080 clean hours (zero conflicting retries), 35,040 clean South-bay `L/s` rows converted via `x 3.6` to `m3/h`.
- `shift_diagnostics_2026.csv` (17,520 four-hour blocks) and `cip_wash_log_2026.csv` (178 washes, 89 H1 legacy tags): all timestamps align cleanly to the 4-hour UTC block grid once parsed with explicit `Europe/Lisbon` offsets.
- `operating_plan_2027.csv`: `scheduled_output_2027_km3 / baseline_output_2026_km3` matches `dispatch_duty_ratio_2027` to machine precision (`max diff 2.2e-16`).

### Load-Bearing Figures Recomputed vs `submission.md`

| Quantity | `submission.md` | Stated Range | Recomputed (Full EM / 300-it EM) | Status |
|---|---|---|---|---|
| C1: Plant 2027 Boron (h) | 1,328.7 | 1,053.9 to 1,390.7 | 1,328.74 | Exact |
| C2: Plant 2027 Scaling (h) | 1,652.7 | 1,539.4 to 1,836.6 | 1,652.72 | Exact |
| C3: Plant 2027 Structural (h) | 1,106.9 | 1,042.6 to 1,251.1 | 1,107.11 / 1,106.90 | Reproduced (diff <= 0.018%) |
| Plant-wide 2027 Total (h) | 4,088.4 | 3,787.7 to 4,300.8 | 4,088.56 / 4,088.36 | Reproduced |
| Overhaul Subtotal (h) | 2,926.4 | 2,707.5 to 3,064.2 | 2,926.51 / 2,926.37 | Reproduced |
| Summer Q3 2027 Total (h) | 1,766.5 | 1,630.7 to 1,850.5 | 1,766.52 | Exact |
| Plant Excess Energy (MWh) | 1,750.8 (1,750.78 exact) | 1,624.1 to 1,841.9 | 1,750.89 / 1,750.77 | Reproduced |
| Overhaul Excess Energy (MWh) | 1,253.5 (1,253.55 exact) | 1,161.3 to 1,319.1 | 1,253.62 / 1,253.54 | Reproduced |
| 2026 Screening Discrepancy (%) | 120.8% | 112.3% to 125.4% | 120.83% | Exact |
| TR07 2027 Total / Q3 / MWh | 1,291.9 / 555.6 / 542.69 | 1,187.9 to 1,343.6 | 1,291.92 / 555.64 / 542.71 (OVERHAUL) | Reproduced |
| TR06 2027 Total / Q3 / MWh | 613.4 / 214.5 / 301.64 | 589.8 to 661.0 | 613.47 / 214.47 / 301.68 (OVERHAUL) | Reproduced |
| TR01 2027 Total / Q3 / MWh | 514.8 / 242.9 / 210.82 | 448.7 to 536.2 | 514.77 / 242.87 / 210.80 (OVERHAUL) | Reproduced |
| TR02 2027 Total / Q3 / MWh | 506.3 / 233.5 / 198.40 | 480.6 to 544.3 | 506.36 / 233.48 / 198.43 (OVERHAUL) | Reproduced |
| TR04 2027 Total / Q3 / MWh | 318.8 / 165.9 / 131.56 | 306.2 to 341.9 | 318.79 / 165.92 / 131.56 (MONITOR) | Reproduced |
| TR03 2027 Total / Q3 / MWh | 305.7 / 126.4 / 129.05 | 287.0 to 336.1 | 305.75 / 126.44 / 129.06 (MONITOR) | Reproduced |
| TR05 2027 Total / Q3 / MWh | 271.0 / 118.1 / 125.10 | 230.3 to 285.5 | 271.06 / 118.14 / 125.11 (MONITOR) | Reproduced |
| TR08 2027 Total / Q3 / MWh | 266.4 / 109.6 / 111.53 | 245.9 to 284.6 | 266.45 / 109.56 / 111.53 (MONITOR) | Reproduced |
| Legacy Raw 2026 / 2027 (h) | 3,713.0 / 4,345.8 | n/a | 3,712.96 / 4,345.82 (slate TR03, TR06, TR07) | Exact |
| Physical Checks F1 / F2 / F3 | 0.0479 / 0.523 / 0.455 | n/a | 0.0475 / 0.5234 mS/cm / 0.453 pp | Reproduced |

All 7 single- and multi-stump ablation totals and overhaul slates in `submission.md` Step-by-Step also reproduce exactly, as do flat 2026 carry-forward totals (`TR01 = 382.3 h`, `TR02 = 380.4 h`) and the 6 +/-20% mode perturbation bounds (lowest overhaul `431.1 h`, highest monitor `347.3 h`). Note that `1,253.546... MWh` rounds consistently to `1,253.5 MWh` at 1 decimal place and `1,253.55 MWh` at 2 decimal places.

### Filed-Fact Grounding (Gate D / Gate B)
- **400.0-hour criterion (`>= 400.0 h` OVERHAUL, `< 400.0 h` MONITOR, per-train, no quota):** `swro_integrity_standard_q27.pdf` Clause 3.1.
- **Physical limits (`> 0.50 mg/L` 1-h boron; `> 1.50` intake algal-TEP & `> 1.50` RO stress on 0.25 h parcels excluding initial 32 burn-in intervals; persistent 4-h structural faults excluding reversible CIP bio-fouling):** Clauses 2.1, 2.2, 2.3.
- **Clocks, calendar quarters, QA revision precedence, exact retry rule, and unit conversions (`1 mg/L = 1,000 ug/L`, `1 L/s = 3.6 m3/h`, `1 MWh = 1,000 kWh`):** Clauses 4.1, 4.2 + `scada_bay_config_2026.json` (`post_cip_monitoring_cycle_hours: 120`).
- **Excess desalination energy rates (`420 / 360 / 540 kWh/h`, divided by 1,000 for MWh):** Clause 4.3.
- **2026 raw monitoring screening discrepancy rate formula:** Clause 4.4.
- **ICP-OES analytical repeatability SD (`0.004 mg/L`, `0.80%` RSD at `0.50 mg/L`), bench export formats, revision rule, and 4h/8h cadence:** `lims_qa_certificate_2026.pdf` Sections 1.2, 2.1, 2.2, 3.1.
- **2027 Annex B projection multipliers (`F_thermal = 1.05, 1.14, 1.32, 1.09`; `F_recovery = 1.03, 1.12, 1.28, 1.07`; `R_duty`):** SWRO-Q27 Annex B.1-B.2 + `operating_plan_2027.csv`.
- **Deliverables & CSV schema (`train_id, boron_2027_h, scaling_2027_h, struct_2027_h, total_2027_h, q3_2027_h, energy_2027_mwh, designation`, sorted by `total_2027_h` descending):** SWRO-Q27 Annex C.1-C.2.
- **Zero unfiled binding constants:** Step 4's `[400, 1450] m3` grid bound is non-binding (widening to `[200, 2000] m3` yields identical `V_hat` on all 8 trains) and Step 5's `pi_f_post <= 0.95 * pi_f_pre` cap is non-binding (unconstrained EM clearing ratios max at `0.545`, giving identical `C3`).
- **Zero legacy EUR / Schedule B / compliance contradictions:** confirmed across `prompt.txt`, `submission.md`, and all 12 operational files (`mibel_iberian_power_spot_2026.csv` carries `EUR/MWh` solely as an out-of-scope distractor; `"energy penalties"` in SWRO-Q27 Clause 4.3 refers strictly to physical kWh/h demand).

## Gate C: Alternative Readings, Operationalization Forks, and Rivals

### Defensible Alternative Specifications Tested

| Fork Family / Variant | Slate | C1 (h) | C2 (h) | C3 (h) | Plant Tot (h) | Plant MWh | Ov MWh | Disc (%) | Inside All 17 Bands? |
|---|---|---|---|---|---|---|---|---|---|
| S1: Continuous OU WLS (1-h block, Cl. 2.1) | Same 4 | 1,077.1 | 1,652.7 | 1,107.1 | 3,837.1 | 1,645.3 | 1,175.8 | 122.1 | Yes |
| S1: Continuous OU OLS (1-h block) | Same 4 | 1,063.5 | 1,652.7 | 1,107.1 | 3,823.4 | 1,639.5 | 1,172.0 | 122.2 | Yes |
| S1: Continuous OU 4h-only (1-h block) | Same 4 | 1,104.1 | 1,652.7 | 1,107.1 | 3,864.0 | 1,656.6 | 1,185.8 | 121.9 | Yes |
| S1: OLS weights (AR1) | Same 4 | 1,312.3 | 1,652.7 | 1,107.1 | 4,072.2 | 1,744.0 | 1,246.9 | 120.9 | Yes |
| S1: Lag-1-only / 4h-only moments | Same 4 | 1,367.5 | 1,652.7 | 1,107.1 | 4,127.3 | 1,767.2 | 1,267.2 | 120.6 | Yes |
| S1: 0.5% total trim (0.25% each tail) | Same 4 | 1,213.4 | 1,652.7 | 1,107.1 | 3,973.3 | 1,702.5 | 1,219.0 | 121.4 | Yes |
| S1: Lab noise off (`sd = 0`) | Same 4 | 1,352.8 | 1,652.7 | 1,107.1 | 4,112.7 | 1,761.0 | 1,260.1 | 120.7 | Yes |
| S1: Hour-weighted `mu_{u,q}` | Same 4 | 1,325.4 | 1,652.7 | 1,107.1 | 4,085.3 | 1,749.5 | 1,252.6 | 120.8 | Yes |
| S1: Relative-equal weights | Same 4 | 1,243.9 | 1,652.7 | 1,107.1 | 4,003.7 | 1,715.3 | 1,228.8 | 121.2 | Yes |
| S1: 0.80% RSD heteroscedastic lab noise | Same 4 | 1,341.0 | 1,652.7 | 1,107.1 | 4,100.9 | 1,756.1 | 1,256.7 | 120.8 | Yes |
| S1: Continuous `lambda` optimization | Same 4 | 1,328.6 | 1,652.7 | 1,107.1 | 4,088.4 | 1,750.8 | 1,253.2 | 120.8 | Yes |
| S2: Flow step-right / step-left / midpoint | Same 4 | 1,328.7 | 1,603.4-1,654.0 | 1,107.1 | 4,039.3-4,089.9 | 1,733.1-1,751.4 | 1,242.0-1,254.4 | 120.8-121.0 | Yes |
| S2: Loss L1 / Huber / Corr / 2%-trimmed | Same 4 | 1,328.7 | 1,652.7 | 1,107.1 | 4,088.6 | 1,750.9 | 1,253.6 | 120.8 | Yes |
| S2: TEP OU-kriging / PCHIP / Nearest / Cubic | Same 4 | 1,328.7 | 1,622.7-1,816.1 | 1,107.1 | 4,058.5-4,252.0 | 1,740.1-1,809.7 | 1,246.2-1,290.6 | 119.9-121.0 | Yes |
| S2: Trapezoidal / left-hand volume; 0.5 m3 grid | Same 4 | 1,328.7 | 1,625.4-1,653.9 | 1,107.1 | 4,061.2-4,089.8 | 1,741.1-1,751.3 | 1,248.0-1,254.0 | 120.8-121.0 | Yes |
| S3: Shared CIP clearing ratio | Same 4 | 1,328.7 | 1,652.7 | 1,184.3 | 4,165.8 | 1,792.6 | 1,283.0 | 116.2 | Yes |
| S3: Free `D3` fouling floor | Same 4 | 1,328.7 | 1,652.7 | 1,058.9 | 4,040.3 | 1,724.8 | 1,238.0 | 123.9 | Yes |
| S3: Post-CIP window 96h / 144h / <=120h | Same 4 | 1,328.7 | 1,652.7 | 1,104.4-1,179.8 | 4,085.9-4,161.3 | 1,749.4-1,790.2 | 1,252.6-1,281.3 | 116.4-121.0 | Yes |
| S3: Posterior-sum quarterly alloc; cond-indep bio-fouling; unconstrained cap | Same 4 | 1,328.7 | 1,652.7 | 1,105.8-1,107.1 | 4,087.3-4,088.6 | 1,750.2-1,750.9 | 1,253.1-1,253.6 | 120.8 | Yes |

Two additional edge checks confirm closure:
- **Quarter-specific `sigma_{1,u,q}`:** preserves the exact 4-of-8 slate and lands inside every aggregate band (`C1 = 1,331.3`, `plant_tot = 4,091.1`, `plant_mwh = 1,752.0`, `disc_rate = 120.8%`), while pure quarterly sampling noise nudges two monitor trains by 1.9-2.8 h (`TR04 = 304.3`, `TR05 = 288.3`); Bartlett (`p >= 0.149`) and Levene (`p >= 0.189`) tests on all 8 trains confirm stationary variance across quarters.
- **Log-normal boron tail:** pushes `C1` to `2,148.6 h` and flips `TR04`, but is refuted directly by `permeate_boron_composites_2026.csv`: Shapiro-Wilk normality passes on linear-scale 4h residuals across all 8 of 8 trains (`p = 0.074` to `0.903`, skewness `-0.03` to `+0.11`), while log-transformed residuals fail Shapiro-Wilk on all 8 of 8 trains (`p <= 0.0001`, skewness `-0.25` to `-0.50`).

### Strongest Rivals Refuted by Native-Unit Physical Checks

| Rival Route | 2027 Slate | Key Total / Train | Physical Refutation from Shipped 2026 Logs |
|---|---|---|---|
| Legacy raw monitoring (composite + same-ts + 2-of-3) | TR03, TR06, TR07 | 4,345.8 h (TR01 161.5, TR02 168.6, TR03 949.7) | F1 = 1.0045 (vs 0.0475), F2 = 2.473 mS/cm (vs 0.523), F3 = 2.741 pp (vs 0.453) |
| Rigorous standard (Pooled AR1 + Fixed lag + 2-class DS) | TR03, TR04, TR05, TR06, TR07 | 7,068.9 h (TR01 344.9, TR02 376.9, TR03 1,409.8) | Fails all 3 checks: F1 = 0.2400 (5x worse), F2 = 1.775 mS/cm (3.4x worse), F3 = 0.727 pp and LL = -7,460.7 vs -7,405.8 (LRT = 109.8, p < 1e-20; predicts 0.277 pp D3 drop vs invariant D3) |
| S1 i.i.d. `sqrt(m)` / Log-log var extrap | All 8 / adds TR05 | TR04 1,381.8 / TR05 643.3 | F1 = 0.4916 (10x worse) / violates stationary autocorrelation decay |
| S2 Nominal holdup volume / Comonotonic bound | TR06, TR07 / adds TR05 | TR02 205.3 / TR05 1,111.2 | F2 = 1.964 mS/cm (3.8x worse) / ignores negative parcel coupling on TR05 |
| S3 Post-CIP maj2 / Unanimous 3-of-3 / Uninverted D3 | Adds TR03 / drops TR06 | TR03 781.3 / TR06 273.1 / TR06 366.1 | Fails to invert 0.429 D3 sensitivity or remove residual post-CIP bio-fouling |

## Gate E: Prompt Precision and Internal Consistency

- `prompt.txt` cleanly specifies the decision question, excess desalination energy unit (`MWh`), workbook and CSV deliverables, uncertainty ranges, comparison chart, and 2026-to-2027 model backup with 2026 monitoring divergence, without naming methods, thresholds, or files.
- All figures across `Final Recommendation`, `Supplementary Questions`, `Critical Components`, and `Step-by-Step` in `submission.md` agree exactly across blocks, with zero em-dashes and zero en-dashes in `prompt.txt`, `submission.md`, and all governing documents.
