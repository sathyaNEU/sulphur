# Determinism Audit Report: task28 (Stage 4, Pass 4)

- **Verdict:** DETERMINISTIC
- **Disposition:** APPROVE
- **Fix location:** none

## Summary

Independent recomputation from a fresh extraction of `task28/target.zip` (following `submission.md` Steps 1 to 8 only) reproduces every load-bearing figure in `submission.md` squarely inside its stated uncertainty band, matches the exact 4-of-8 2027 vessel overhaul slate (`TR07`, `TR06`, `TR02`, `TR01` OVERHAUL; `TR05`, `TR04`, `TR08`, `TR03` MONITOR), and preserves exact descending train ranking. Every decisive convention, threshold, energy rate, projection formula, and CSV schema is filed literally in `prompt.txt` and `swro_integrity_standard_q27.pdf` with zero leftover Clause 4.4 / EUR / Schedule B contradictions. Across 31 defensible estimation variants (plus 4 joint cross-stump combinations and 6 +/-20% mode perturbations), every variant lands inside the stated bands and preserves the identical overhaul slate with >82 h clearance at the 400.0 h threshold; every competing rival that crosses a band or flips a train is decisively refuted by native-unit physical consistency checks computed directly from the shipped 2026 logs.

## Gate A: Independent Recomputation from Shipped Files

All Step 1 data-cleaning counts reproduced identically from `target.zip`:
- `permeate_boron_composites_2026.csv`: 15,465 raw rows -> 15,024 unique bottles (441 superseded `qa_revision=1` rows dropped; 7,721 raw Portuguese `DD/MM/YYYY` dates and 7,721 raw `ug/L` South-bay assays; 7,512 each after deduplication).
- `autosampler_schedule_2026.csv`: 2,920 rows (720 Q1 legacy `LINE-A..LINE-H` tags).
- `intake_chemistry_15m_2026.csv` & `ro_feed_header_15m_2026.csv`: 802 and 832 exact re-transmitted frames dropped -> 280,320 clean 15-minute rows each (35,008 post-burn-in intervals per train after excluding the opening 32 intervals per Clause 2.2).
- `train_hydraulics_hourly_2026.csv`: 198 exact retries dropped, 35,040 South-bay `L/s` readings converted (`x 3.6`) -> 70,080 clean hourly rows.
- `shift_diagnostics_2026.csv` & `cip_wash_log_2026.csv`: 17,520 four-hour blocks and 178 CIP washes (112 `CIP_ALK_pH11`, 66 `CIP_ACID_pH2`, 88 H1 legacy tags) aligned cleanly to the 4-hour UTC block grid via explicit `Europe/Lisbon` offsets.

### Per-Train 2027 Forecasts (Recomputed vs `submission.md`)

| Train | Boron (rep / sub) | Scaling (rep / sub) | Struct (rep / sub) | Total 2027 h (rep / sub) | Stated Band (h) | In Band? | Q3 h (rep / sub) | Energy MWh (rep / sub) | Call Match |
|---|---:|---:|---:|---:|---|---|---:|---:|---|
| TR07 | 674.9 / 674.9 | 515.5 / 515.9 | 280.6 / 280.6 | 1,470.9 / 1,471.4 | 1,417.9 to 1,519.5 | YES | 512.1 / 512.1 | 620.54 / 620.71 | OVERHAUL == OVERHAUL |
| TR06 | 0.4 / 0.4 | 23.7 / 24.1 | 499.5 / 500.2 | 523.6 / 524.8 | 498.2 to 555.7 | YES | 148.5 / 149.5 | 278.43 / 278.98 | OVERHAUL == OVERHAUL |
| TR02 | 0.1 / 0.1 | 442.6 / 446.8 | 72.8 / 73.3 | 515.5 / 520.2 | 475.2 to 542.6 | YES | 227.9 / 230.4 | 198.69 / 200.46 | OVERHAUL == OVERHAUL |
| TR01 | 462.1 / 462.1 | 29.7 / 29.5 | 23.3 / 24.3 | 515.0 / 515.8 | 487.8 to 541.3 | YES | 182.7 / 183.4 | 217.32 / 217.79 | OVERHAUL == OVERHAUL |
| TR05 | 0.6 / 0.7 | 194.9 / 192.7 | 72.4 / 73.2 | 267.9 / 266.6 | 192.4 to 317.3 | YES | 101.5 / 101.0 | 109.50 / 109.17 | MONITOR == MONITOR |
| TR04 | 153.5 / 153.5 | 34.8 / 35.1 | 56.3 / 56.4 | 244.7 / 245.0 | 229.8 to 269.3 | YES | 71.7 / 71.7 | 107.44 / 107.57 | MONITOR == MONITOR |
| TR08 | 0.0 / 0.0 | 24.4 / 24.4 | 40.7 / 40.8 | 65.1 / 65.2 | 59.1 to 79.6 | YES | 20.7 / 20.8 | 30.76 / 30.83 | MONITOR == MONITOR |
| TR03 | 0.3 / 0.3 | 28.6 / 28.6 | 0.0 / 1.0 | 28.9 / 29.8 | 21.7 to 53.4 | YES | 10.4 / 10.3 | 10.43 / 10.93 | MONITOR == MONITOR |

### Plant-Wide Totals, Critical Components, and Overhaul Subtotals

| Metric | Recomputed | `submission.md` | Diff | Stated Band | Status |
|---|---:|---:|---:|---|---|
| C1: Plant-wide Boron 2027 (h) | 1,291.95 | 1,292.0 | -0.05 | 1,212.4 to 1,315.6 | IN BAND (exact) |
| C2: Plant-wide Scaling 2027 (h) | 1,294.22 | 1,297.1 | -2.88 | 1,154.1 to 1,490.0 | IN BAND (-0.22%) |
| C3: Plant-wide Structural 2027 (h) | 1,045.51 | 1,049.7 | -4.19 | 975.1 to 1,130.9 | IN BAND (-0.40%) |
| Plant-wide Total 2027 (h) | 3,631.67 | 3,638.8 | -7.13 | 3,475.3 to 3,852.2 | IN BAND (-0.20%) |
| Overhaul Subtotal 2027 (h) | 3,025.06 | 3,032.2 | -7.14 | 2,926.3 to 3,140.4 | IN BAND (-0.24%) |
| Plant-wide Summer Q3 2027 (h) | 1,275.53 | 1,279.1 | -3.57 | 1,210.9 to 1,355.5 | IN BAND (-0.28%) |
| Plant-wide Energy Penalty (MWh) | 1,573.11 | 1,576.43 | -3.32 | 1,514.4 to 1,656.5 | IN BAND (-0.21%) |
| Overhaul Energy Penalty (MWh) | 1,314.98 | 1,317.94 | -2.96 | 1,269.6 to 1,366.0 | IN BAND (-0.22%) |

### Physical Falsification Checks and Raw Monitoring Baselines Reproduced

- **Direct monitoring (raw):** Raw boron bottle-fraction exceedances 56.05 h (2026) / 76.17 h (2027), same-timestamp scaling 471.5 h (2026) / 634.2 h (2027), 2-of-3 shift majority vote 4,252.0 h (2026) / 4,787.5 h (2027), totaling 5,497.8 h in 2027 and flagging TR03 (1,521.9 h), TR04 (411.7 h), TR06 (496.9 h), TR07 (1,963.2 h) while missing TR01 (277.3 h) and TR02 (311.0 h) - exact match to `submission.md`.
- **F1 (Boron flux + support moment identity):** Golden achieves `|r_flux| = 0.000`, `|d(V8/V4)| = 0.044`, `|d(R4)| = 0.014` (sum = `0.058`, matching `0.0579` in `submission.md`).
- **F2 (Two-path seawater conductivity RMS):** Golden achieves `0.340 mS/cm` (`0.3397`) fleet mean vs `2.045 mS/cm` same-timestamp, `1.424 mS/cm` nominal volume, `1.357 mS/cm` fixed wall-clock lag, and `0.805 mS/cm` 1D single-plug `V_eff` - exact match to `submission.md`.
- **F3 (Recipe-stratified CIP drop identity):** Golden 4-state dual-recipe EM achieves `LL = -9,415.63` (`BIC = 19,202.55`), fleet-pooled CIP drop MAE `0.253 pp` (per-train-regime MAE `0.958 pp`), matching the empirical collapse of `D3` (acoustic bypass) on `TR03` after `CIP_ACID_pH2` (`8.63% -> 0.42%`, `+8.21 pp` drop) versus zero drop after `CIP_ALK_pH11` (`8.63% -> 10.24%`, `-1.61 pp`).

## Gate B: Filed Facts Verification

Every decisive convention is present verbatim in the shipped files (verified via full layout extraction of both PDFs, JSON, XLSX, and CSVs):
- **Train roster & legacy tags:** `TR01..TR08` (`LINE-A..LINE-H`), `swro_integrity_standard_q27.pdf` Clause 1.2, `train_asset_register.csv`, `scada_bay_config_2026.json`.
- **2026 UTC calendar & exact quarters:** `Q1 = 2,160 h`, `Q2 = 2,184 h`, `Q3 = 2,208 h`, `Q4 = 2,208 h`, `swro_integrity_standard_q27.pdf` Clauses 1.2 & 4.1, `operating_plan_2027.csv`.
- **Failure-mode estimands:** Clause 2.1 (permeate boron > 0.50 mg/L on 1-hour basis), Clause 2.2 (scaling > 1.50 & > 1.50 on 15-min = 0.25 h basis, opening 8 hours / 32 intervals `2026-01-01T00:00Z` through `2026-01-01T07:45Z` outside 2026 count), Clause 2.3 (persistent structural fault on 4-hour block basis; reversible CIP-cleared fouling excluded).
- **Lab & telemetry specs:** ICP-OES repeatability SD `0.004 mg/L`, bench units/dates, QA revision 2 precedence, 4h/8h flow-proportional schedule (`lims_qa_certificate_2026.pdf`, `scada_bay_config_2026.json`, `autosampler_schedule_2026.csv`); 120 h post-CIP cycle and dual recipes `CIP_ALK_pH11` / `CIP_ACID_pH2` (`scada_bay_config_2026.json`).
- **Overhaul criterion & energy rates:** 400.0 h independent per-train limit with no quota (Clause 3.1); `420 kWh/h` Boron, `360 kWh/h` Scaling, `540 kWh/h` Structural divided by 1,000 for MWh; Overhaul subtotals strictly over OVERHAUL trains; Summer Q3 sums all 8 trains & 3 modes (Clause 4.3).
- **2027 projection & output schema:** Exact multiplicative formulas and seasonal factors (`1.05/1.14/1.32/1.09` boron; `1.03/1.12/1.28/1.07` scaling; per-train `R_duty`) in Annex A & `operating_plan_2027.csv`; exact workbook deliverables and 8-column CSV schema (`train_id`, `boron_2027_h`, `scaling_2027_h`, `struct_2027_h`, `total_2027_h`, `q3_2027_h`, `energy_2027_mwh`, `designation` sorted descending by `total_2027_h`) in Annex B.
- **No contradictions / clean numbering:** Zero occurrences of `4.4`, `Schedule A`, `Schedule B`, or `EUR` pricing in `swro_integrity_standard_q27.pdf`; Annex A and Annex B numbering is clean. Distractors (`mibel_iberian_power_spot_2026.csv` in EUR/MWh and `algarve_reservoir_levels_2026.xlsx`) contain no conflicting engineering rules. Every distinctive recommendation term is grounded in the shipped inputs.

## Gate C: Alternative Readings, Rivals, and Fork Battery

### 1. Defensible Estimator Variants (All Stay Inside Stated Bands and Preserve Exact Call)

| Fork / Variant | Mode / Scope | Key Result (h or MWh) | Band Check | Call Preserved? |
|---|---|---:|---|---|
| M1-1: Continuous OU (1h-normalized) | Mode 1 (C1) | 1,245.4 h (TR01 444.4, TR04 149.1) | IN [1,212.4, 1,315.6] | YES |
| M1-2: Relative-error OLS moment weights | Mode 1 (C1) | 1,303.4 h (TR01 471.3, TR04 152.1) | IN [1,212.4, 1,315.6] | YES |
| M1-3: Unweighted raw OLS moment weights | Mode 1 (C1) | 1,291.3 h (TR01 464.8, TR04 153.2) | IN [1,212.4, 1,315.6] | YES |
| M1-4: Lab repeatability noise OFF | Mode 1 (C1) | 1,299.1 h (TR01 464.7, TR04 154.6) | IN [1,212.4, 1,315.6] | YES |
| M1-5: 0.5%-trimmed residual moments | Mode 1 (C1) | 1,227.6 h (TR01 439.9, TR04 138.9) | IN [1,212.4, 1,315.6] | YES |
| M1-6: 4h-only moments (excluding 8h) | Mode 1 (C1) | 1,277.9 h (TR01 459.2, TR04 152.4) | IN [1,212.4, 1,315.6] | YES |
| M1-7: Span-weighted WLS flux regression | Mode 1 (C1) | 1,292.7 h (TR01 454.2, TR04 151.9) | IN [1,212.4, 1,315.6] | YES |
| M1-8: Huber IRLS flux regression | Mode 1 (C1) | 1,275.6 h (TR01 451.3, TR04 148.6) | IN [1,212.4, 1,315.6] | YES |
| M1-9: Exact flow-weighted composite kernel | Mode 1 (C1) | 1,275.9 h (TR01 457.2, TR04 153.1) | IN [1,212.4, 1,315.6] | YES |
| M1-10: Uncentered lag-1 autocovariance | Mode 1 (C1) | 1,289.4 h (TR01 462.1, TR04 151.0) | IN [1,212.4, 1,315.6] | YES |
| M2-1: Trapezoidal cumulative volume | Mode 2 (C2) | 1,277.5 h (TR02 443.7, TR05 185.1) | IN [1,154.1, 1,490.0] | YES |
| M2-2: Step-left hourly flow hold | Mode 2 (C2) | 1,244.5 h (TR02 445.3, TR05 165.5) | IN [1,154.1, 1,490.0] | YES |
| M2-3: Step-right hourly flow hold | Mode 2 (C2) | 1,226.8 h (TR02 439.1, TR05 156.8) | IN [1,154.1, 1,490.0] | YES |
| M2-4: Linear midpoint hourly flow | Mode 2 (C2) | 1,224.3 h (TR02 451.9, TR05 145.6) | IN [1,154.1, 1,490.0] | YES |
| M2-5: L1 (MAE), Huber, or 2%-trimmed L2 loss | Mode 2 (C2) | 1,294.5 h (all three identical, RMS 0.3397) | IN [1,154.1, 1,490.0] | YES |
| M2-6: PCHIP two-path TEP lookup | Mode 2 (C2) | 1,376.1 h (TR02 455.7, TR05 212.5) | IN [1,154.1, 1,490.0] | YES |
| M2-7: CubicSpline two-path TEP lookup | Mode 2 (C2) | 1,432.2 h (TR02 458.5, TR05 233.8) | IN [1,154.1, 1,490.0] | YES |
| M2-8: Nearest-neighbor two-path TEP lookup | Mode 2 (C2) | 1,466.6 h (TR02 460.5, TR05 236.3) | IN [1,154.1, 1,490.0] | YES |
| M2-9: Unconstrained `f_fast` (no cap/snap) | Mode 2 (C2) | 1,294.5 h (identical to golden) | IN [1,154.1, 1,490.0] | YES |
| M2-10: Include 32 burn-in intervals (non-clause) | Mode 2 (C2) | 1,295.9 h (TR02 443.7, TR05 194.9) | IN [1,154.1, 1,490.0] | YES |
| M3-1: Strict post-CIP `(0, 30]` blocks `[1,30]` | Mode 3 (C3) | 1,047.3 h (TR03 0.0, TR06 496.9) | IN [975.1, 1,130.9] | YES |
| M3-2: Inclusive 31-block post-CIP `[0,30]` | Mode 3 (C3) | 1,053.2 h (TR03 0.0, TR06 501.2) | IN [975.1, 1,130.9] | YES |
| M3-3: 96 h post-CIP window `[0,23]` | Mode 3 (C3) | 1,039.2 h (TR03 0.0, TR06 492.1) | IN [975.1, 1,130.9] | YES |
| M3-4: 144 h post-CIP window `[0,35]` | Mode 3 (C3) | 1,113.3 h (TR03 3.4, TR06 522.5) | IN [975.1, 1,130.9] | YES |
| M3-5: Per-train CIP clearing ratios | Mode 3 (C3) | 1,006.7 h (TR03 0.0, TR06 487.8) | IN [975.1, 1,130.9] | YES |
| M3-6: Cross-recipe clearing permitted | Mode 3 (C3) | 1,048.1 h (TR03 0.0, TR06 500.4) | IN [975.1, 1,130.9] | YES |
| M3-7: Unbounded retention `(0.001, 0.999)` | Mode 3 (C3) | 1,045.5 h (neither bound binds) | IN [975.1, 1,130.9] | YES |
| M3-8: Quarterly empirical posterior allocation | Mode 3 (C3) | 1,046.4 h (max train diff +1.8 h on TR07) | IN [975.1, 1,130.9] | YES |
| M3-9: 20 random EM restarts | Mode 3 (C3) | Global max LL=-9415.63 unique (15/20 hit) | 1,045.5 h exact | YES |
| J-1: Joint OU + PCHIP + 144h shared | All 3 modes | Tot 3,734.7 h, OV 3,081.7 h, Q3 1,301.9 h, E 1,619.6 MWh | ALL 5 BANDS IN | YES |
| J-2: Joint OU + step-left + per-train CIP | All 3 modes | Tot 3,496.6 h, OV 2,947.2 h, Q3 1,222.8 h, E 1,514.7 MWh | ALL 5 BANDS IN | YES |
| J-3: Joint Huber/noLab + PCHIP + 120h | All 3 modes | Tot 3,710.8 h, OV 3,068.0 h, Q3 1,301.4 h, E 1,601.4 MWh | ALL 5 BANDS IN | YES |
| J-4: Joint AR1 + step-left + 144h shared | All 3 modes | Tot 3,649.8 h, OV 3,069.8 h, Q3 1,270.4 h, E 1,591.8 MWh | ALL 5 BANDS IN | YES |
| P-1: Energy from rounded 1-dec vs exact hours | Projection | 1,576.44 vs 1,576.43 MWh (diff 0.01 MWh) | Identical at 0.1 MWh | YES |
| P-2: Six +/-20% independent mode perturbations | Sensitivity | min OV = 423.5 h (Boron -20%), max MON = 305.1 h (Scaling +20%) | Exact 4-of-8 slate | YES |

### 2. Competing Rivals Refuted Directly by Shipped Files

| Rival Design | Result & Call Impact | Direct Refutation from Shipped Files |
|---|---|---|
| R1: Linear-Q flux + AR(1) | C1 = 462.5 h, TR01 = 126.4 h (drops TR01) | Refuted by `permeate_boron_composites_2026.csv` + `train_hydraulics_hourly_2026.csv`: encompassing `[1/Q + Q]` yields `t(1/Q)=+21.34, t(Q)=-0.08` on TR04 (low-10% Q residual bias `t=+13.49`), `t(1/Q)=+4.66` on TR01, `t(1/Q)=+4.39` on TR07; combined `Delta-BIC = +449.2` against Linear-Q (and `+133.6` against `log(Q)`). |
| R2: Stationary AR(1) without flux coupling | C1 = 548.8 h, TR01 = 96.3 h (drops TR01) | Refuted by residual correlation with `1/Q_bar`: fleet mean `|r_flux| = 0.456` (vs `0.000` golden); omits `42%` to `73%` of within-quarter composite variance explained by `1/Q_bar`. |
| R3: Flux OLS without AR(1) support deconv | C1 = 976.7 h, TR01 = 334.4 h (drops TR01) | Refuted by 4h/8h composite moment mismatch: `|d(V8/V4)| = 0.340` and `|dR4| = 0.662` (vs `0.044` and `0.014` golden). |
| R4: i.i.d. `sqrt(m)` scaling (with/without flux) | C1 = 2,183.3 / 2,914.2 h (flips TR04 > 400 h) | Refuted by lag-1 composite autocorrelation mismatch: `|dR4| = 0.338` / `0.339` (ignores persistent autocorrelation, e.g. `lambda = 7.43 h` on TR04). |
| R5: 1D single-plug `V_eff` conductivity match | TR02 scaling 177.0 h (drops TR02 to 250 h), TR05 521.6 h (flips TR05 to 596 h) | Refuted by conservative seawater conductivity RMS F2: `0.805 mS/cm` (2.37x the `0.340 mS/cm` two-path noise floor across `intake_chemistry_15m_2026.csv` and `ro_feed_header_15m_2026.csv`). |
| R6: Same-timestamp / nominal vol / fixed lag | C2 = 634.2 / 594.1 / 999.5 h (all drop TR02) | Refuted by F2 conductivity RMS: `2.045`, `1.424`, and `1.357 mS/cm` (4.0x to 6.0x the `0.340 mS/cm` noise floor). |
| R7: Comonotonic upper-bound TEP pairing | C2 = 4,267.5 h, TR05 scaling 569.3 h (total 643.2 h, flips TR05) | Violates observed arrival mixing recovered from conservative conductivity tracer. |
| R8: 3-state pooled-CIP EM (`D3=0` and `free D3`) | `D3=0`: C3 = 3,921.5 h, TR03 = 1,143.3 h (flips TR03); `free D3`: C3 = 805.4 h, TR06 = 395.4 h | Refuted by `shift_diagnostics_2026.csv` + `cip_wash_log_2026.csv`: fleet PostALK vs PostACID 8-pattern `chi2 = 52.98 (p = 3.74e-09)`, D3-only `chi2 = 28.80 (p = 8.01e-08)`; 192-cell likelihood ratio `2*dLL = 174.92 (Delta-BIC = +57.67)` vs `free D3` and `2*dLL = 240.65 (Delta-BIC = +113.62)` vs `D3=0`. |
| R9: 2-class Dawid-Skene post-CIP (pooled / ACID / ALK) | C3 = 6,497.9 / 6,029.9 / 6,732.1 h, TR03 > 1,900 h (flips TR03) | Refuted by recipe-specific CIP drop check (`F3_RMS = 3.342 pp` vs `1.294 pp` golden; predicts zero difference across CIP recipes while failing to separate residual un-cleared organic/mineral fouling). |
| R10: Raw 2-of-3 / Post-CIP 2-of-3 / Unanimous 3-of-3 / Base-adj D3 post-ACID | TR03 = 1,498.7 / 1,202.9 h or TR06 = 54.5 / 225.4 h (flips TR03 or TR06) | Refuted by `F3` (`p = 8.01e-08`) and conditional emission profiles (structural `theta_D2 = 0.170` makes 3-of-3 miss ~83% of structural blocks; raw `D3` misses ~35% of structural blocks because `theta_D3 = 0.648`). |
| R11: Flat 2026 carry-forward (no Annex A) | Drops TR01 (~392.8 h) and TR02 (~393.9 h) | Explicitly ruled out by `swro_integrity_standard_q27.pdf` Annex A and `operating_plan_2027.csv`. |

## Gates D and E: Prompt Clarity, Internal Consistency, and Self-Rebuild

- **Prompt clarity:** `prompt.txt` asks one clear, unhedged engineering question with explicit units (`MWh`) and deliverables, delegating exact formulas, thresholds, rates, and CSV schema to `swro_integrity_standard_q27.pdf`. No semantic ambiguity, no loaded premise, no planted conflicting objective.
- **Cross-section consistency:** All 23 repeated figures and uncertainty bands across Final Recommendation, Supplementary Questions, Critical Components, and Step-by-Step in `submission.md` match identically. Per-train mode sums and Q3 sums are consistent to +/-0.1 h rounding of exact unrounded values.
- **Self-rebuilding Step-by-Step:** Every step writes down the exact cleaning rules, models, search domains, weights, and projection rules needed to reproduce every committed figure inside its band without guessing hidden conventions.
- **Typography:** Zero em dashes and zero en dashes in `prompt.txt`, `submission.md`, and this report.

## Fix

- **Location:** none
- **Action:** No changes required to `prompt.txt`, `target.zip`, or `submission.md`. Approve Stage 4 determinism gate.
