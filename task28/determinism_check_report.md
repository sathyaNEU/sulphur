# Determinism Check Report: task28 (Pass 1)

- **Verdict:** DETERMINISTIC (with SOLUTION_WRONG carve-out on answer-block bands and Step-by-Step rebuild specification)
- **Disposition:** FIX_NOW (answer-block edits in `submission.md` only: widen S2/downstream upper bands for non-linear/nearest parcel TEP lookup and add the missing base-model specification sentences in Steps 3-5; zero changes to `prompt.txt` or `target.zip`, no model rerun required).
- **Fix location:** `solution`

## Why

The main overhaul call (**OVERHAUL: TR07, TR06, TR01, TR02; MONITOR: TR04, TR03, TR05, TR08** under Standard SWRO-Q27's 400.0-hour threshold) is uniquely forced by the shipped files and survives all 36 methodological, boundary, and convention forks tested (lowest overhaul train >= 458.5 h, highest monitor train <= 338.4 h). Every decisive rule, threshold, repeatability SD, stabilization window, tariff, calendar boundary, and 2027 plan multiplier is explicitly filed in `target.zip` (Gate B passes cleanly), and `prompt.txt` pins one answer and unit for every ask without ambiguity (Gates D and E pass cleanly). The strongest standard rival (pooled AR(1) + fixed-lag CCF + 2-class conditional-independence Dawid-Skene EM, 7,213.2 h) is quantitatively refuted directly from the shipped logs across all three physical identities (F1, F2, F3 / 128-cell likelihood ratio).

Two `FIX_NOW` solution-block defects require repair in `submission.md`:
1. **Too-narrow S2 upper band (Gate C band coverage):** After recovering the exact same effective hydraulic holdup volumes `V_hat` (`692 m3` TR02 to `1,022 m3` TR05, `F2 RMS = 0.523 mS/cm`), evaluating `intake_tep_mg_l(t_dep) > 1.50` at continuous fractional departure times via standard non-linear or discrete-parcel methods leaves `submission.md`'s narrow C2 upper band (`1,672.6 h`, only `+19.9 h` above `1,652.7 h`): Gaussian OU kriging yields `1,690.7 h`, PCHIP `1,744.5 h`, nearest 15-minute parcel lookup `1,800.3 h`, and cubic spline `1,814.7 h`. None flips the 4-of-8 overhaul slate or approaches any shortcut route (`Fixed-Lag CCF = 1,246.9 h`; `Comonotonic = 5,306.0 h`), and conductivity std checks (`std(ro_cond) = 1.799` constant across fractional grid offset `d in [0, 0.5)` vs `std(ic_lin) = 1.731` and `std(ic_cub) = 1.804` with `RMS = 0.548 mS/cm`) do not refute these methods; linear interpolation attenuates threshold exceedances at mid-interval offsets (`2.25%` at `d < 0.1` vs `1.56%` at `d in [0.4, 0.5)`). Nearest and cubic lookup also clip the upper bounds of Plant total (`4,236.0 / 4,250.4` vs `4,234.9 h`), Q3 (`1,829.8` vs `1,814.0 h` for cubic), and four train totals (`TR02`, `TR03`, `TR04`, `TR08`).
2. **Step-by-Step rebuild specification gaps (self-contained rebuild check):** Several base-model rules needed to reproduce the point estimates exactly had to be inferred by trial and error rather than read from Steps 3-5 (detailed under Fix below).

## Evidence

### 1. Core and Supplementary Figures Recomputation (Gate A)

Every figure across Final Recommendation, Supplementary Questions 1-4, Critical Components 1-3, Step-by-Step, and all 7 closing ablations is internally consistent across blocks (EUR exact to the cent; train/mode hours agree within standard 0.1 h display rounding of unrounded sums) and reproduces from `/tmp/determinism-task28-pass1/target/`:

| Quantity | Blocks Value | Blocks Band | Recomputed (Base) | Status |
|---|---|---|---|---|
| Overhaul Call (>= 400.0 h) | TR07, TR06, TR01, TR02 | 4 of 8 | TR07, TR06, TR01, TR02 | Reproduced |
| Monitor Call (< 400.0 h) | TR04, TR03, TR05, TR08 | 4 of 8 | TR04, TR03, TR05, TR08 | Reproduced |
| C1: Plant 2027 Permeate Boron | 1,328.7 h | 1,053.9 - 1,390.7 h | 1,334.6 h (invSE2) / 1,310.7 (OLS) / 1,351.3 (WLS-N) | Inside band (0.4% gap on invSE2) |
| C2: Plant 2027 Scaling | 1,652.7 h | 1,560.4 - 1,672.6 h | 1,652.7 h (lin-right cumsum + L2 + linear TEP) | Exact match |
| C3: Plant 2027 Structural Faults | 1,106.9 h | 1,043.7 - 1,217.6 h | 1,107.1 h (per-train CIP, tied D3, <120h, prev) | Match (0.2 h) |
| Plant-Wide 2027 Total | 4,088.4 h | 3,787.7 - 4,234.9 h | 4,094.4 h (using invSE2 S1) / 4,088.5 h (exact S2+S3) | Inside band |
| Overhaul-Train 2027 Subtotal | 2,926.4 h | 2,707.5 - 3,028.6 h | 2,926.4 h (reconciled exact) | Reproduced |
| Plant-Wide Q3 2027 Total | 1,766.5 h | 1,630.7 - 1,814.0 h | 1,766.5 h (unweighted Q boron mean + S2 exact + S3 prev) | Reproduced |
| Plant-Wide 2027 Schedule B EUR | EUR 1,750.8k (1,750,781.22) | EUR 1,624.1k - 1,824.4k | EUR 1,750,781.22 (420/360/540 EUR/h exact sum) | Reproduced |
| Overhaul 2027 Schedule B EUR | EUR 1,253.5k (1,253,546.01) | EUR 1,161.3k - 1,304.8k | EUR 1,253,546.01 | Reproduced |
| 2026 Legacy Screening Total | 3,713.0 h (2027: 4,345.8 h) | Point | 3,713.0 h (201.0 B + 408.0 S + 3,104.0 St); 2027: 4,345.8 h | Exact match |
| 2026 Screening Discrepancy Rate | 120.8% | 113.5% - 125.4% | 120.84% (3,713.0 incumbent vs 3,161.5 true 2026) | Exact match |
| TR07 2027 Total (B / S / St) | 1,291.9 (535.6 / 503.6 / 252.6) | 1,187.9 - 1,332.3 h | 1,291.9 (534.8 / 503.6 / 252.7) | Match |
| TR06 2027 Total (B / S / St) | 613.4 (68.9 / 118.5 / 426.0) | 589.8 - 645.0 h | 615.0 (70.4 / 118.5 / 426.1) | Match |
| TR01 2027 Total (B / S / St) | 514.8 (285.2 / 183.0 / 46.6) | 448.7 - 531.0 h | 521.4 (291.7 / 183.0 / 46.7) | Inside band |
| TR02 2027 Total (B / S / St) | 506.3 (60.7 / 376.3 / 69.4) | 481.1 - 523.7 h | 506.4 (60.7 / 376.3 / 69.4) | Exact match |
| TR04 2027 Total (B / S / St) | 318.8 (124.3 / 142.6 / 51.9) | 306.2 - 328.0 h | 319.1 (124.6 / 142.6 / 51.9) | Match |
| TR03 2027 Total (B / S / St) | 305.7 (59.2 / 160.8 / 85.7) | 287.0 - 326.2 h | 305.8 (59.2 / 160.8 / 85.8) | Exact match |
| TR05 2027 Total (B / S / St) | 271.0 (157.8 / 12.9 / 100.3) | 230.4 - 283.8 h | 271.0 (157.8 / 12.9 / 100.3) | Exact match |
| TR08 2027 Total (B / S / St) | 266.4 (37.1 / 155.0 / 74.3) | 249.6 - 275.1 h | 266.4 (37.1 / 155.0 / 74.3) | Exact match |
| S2 Volumes & F2 RMS | V=692.0 (TR02) to 1,022.0 (TR05); 0.523 mS/cm | Point | V=692.0 m3 (TR02), 1,022.0 m3 (TR05); RMS=0.5234 mS/cm | Exact match |
| S3 Structural Sensitivities | (0.887, 0.553, 0.429) | Point | (0.8872, 0.5525, 0.4289) | Exact match |
| Step 1 Cleaning Counts | 15,024 B (425 drop); 280,320 x 2 (775/834); 70,080 H (178); 17,520 Sh; 178 CIP | Point | All counts match to the exact integer | Exact match |

### 2. Gate C Fork Audit (36 Forks Tested)

Every single-mode fork holds the other two modes at golden values to isolate its impact on its Critical Component, Plant total, train totals, and the 400-hour overhaul call.

| # | Fork / Variant | Mode Metric (2027 h) | Plant Total (h) | Tightest Margin (Min Ov / Max Mon) | Call Flips? | Band Status / Disposition |
|---|---|---:|---:|---|---|---|
| 1 | S1: AR(1) WLS (sample-count N) | C1 = 1,351.3 | 4,110.8 | TR02 506.4 / TR04 318.9 | No | All IN |
| 2 | S1: AR(1) WLS (inverse moment var) | C1 = 1,334.6 | 4,094.1 | TR02 506.4 / TR04 319.5 | No | All IN |
| 3 | S1: AR(1) OLS (unweighted) | C1 = 1,310.7 | 4,070.2 | TR02 506.4 / TR04 319.7 | No | All IN |
| 4 | S1: AR(1) unweighted quarterly mean | C1 = 1,354.5 | 4,114.0 | TR02 506.4 / TR04 318.9 | No | All IN |
| 5 | S1: Continuous OU (1h-block avg, WLS-N) | C1 = 1,096.1 | 3,855.6 | TR01 460.3 / TR04 314.1 | No | All IN |
| 6 | S1: Continuous OU (1h-block avg, OLS) | C1 = 1,061.8 | 3,821.3 | TR01 458.5 / TR04 314.3 | No | All IN |
| 7 | S1: Continuous OU pointwise (m->0) | C1 = 1,819.2 | 4,578.7 | TR02 535.4 / TR04 321.3 | No | Ruled out: Clause 2.1 pins 1-hour operating block |
| 8 | S1: AR(1) lag-1-only (C4/V4 + C8/V8) | C1 = 1,277.0 | 4,036.5 | TR02 506.4 / TR04 318.1 | No | C1 & Plant IN; TR01=561.5 (>531.0, drops V8/V4) |
| 9 | S1: AR(1) 4-hour-only moments (V4, C4) | C1 = 1,360.7 | 4,120.2 | TR02 506.4 / TR04 317.0 | No | All IN |
| 10 | S1: AR(1) 0.5% winsorized residuals | C1 = 1,277.9 | 4,037.4 | TR02 506.4 / TR04 310.8 | No | All IN |
| 11 | S1: AR(1) lab repeatability OFF (0.004) | C1 = 1,380.9 | 4,140.4 | TR02 506.4 / TR04 321.1 | No | All IN (though 0.004 mg/L filed in LIMS cert) |
| 12 | S1: Pooled AR(1) (rival) | C1 = 1,147.2 | 3,906.7 | TR01 363.5 / TR04 514.8 | **YES** | Refuted by F1: 0.229 vs 0.044-0.048 (~5x worse) |
| 13 | S1: i.i.d. sqrt(m) scaling (rival) | C1 = 6,093.0 | 8,852.5 | TR04 1,382.9 (flips all) | **YES** | Refuted by F1: 0.494 vs 0.044-0.048 (>10x worse) |
| 14 | S1: Raw composites (legacy) | C1 = 285.6 | 3,045.1 | TR01 252.2 (drops TR01) | **YES** | Refuted by F1: 1.006 vs 0.044-0.048 (>20x worse) |
| 15 | S2: Linear flow right-cumsum + L2 (base) | C2 = 1,652.7 | 4,088.3 | TR02 506.4 / TR04 318.8 | No | Exact match (RMS 0.5234 mS/cm) |
| 16 | S2: Linear flow trapezoidal + L2 | C2 = 1,648.4 | 4,084.0 | TR02 506.3 / TR04 319.7 | No | All IN (RMS 0.5432 mS/cm) |
| 17 | S2: Piecewise-constant step (right) | C2 = 1,603.4 | 4,039.0 | TR02 498.6 / TR04 313.2 | No | All IN (RMS 0.6642 mS/cm) |
| 18 | S2: Piecewise-constant step (left) | C2 = 1,560.3 | 3,995.9 | TR02 486.7 / TR04 312.0 | No | C2 0.1 h below 1,560.4; TR08 249.0 vs 249.6 (RMS 0.815) |
| 19 | S2: Midpoint flow (+0.5h cumsum / trap) | C2 = 1,580.2 / 1,561.4 | 4,015.8 / 3,997.0 | TR02 485.9 / TR04 312.2 | No | All IN (RMS 0.738 / 0.814 mS/cm) |
| 20 | S2: L1 / Huber / Corr / 2%-Trimmed loss | C2 = 1,652.7 (all 4) | 4,088.3 | TR02 506.4 / TR04 318.8 | No | All IN (identical V_hat and RMS 0.5234) |
| 21 | S2: Gaussian OU kriging on intake_tep | C2 = 1,690.7 | 4,126.4 | TR02 502.7 / TR04 326.0 | No | **C2 OUT (+18.1 h)**; Plant & all trains IN (**FIX_NOW**) |
| 22 | S2: PCHIP interpolation on intake_tep | C2 = 1,744.5 | 4,180.2 | TR02 522.4 / TR04 331.8 | No | **C2 OUT (+71.9 h)**; TR04 OUT (+3.8 h) (**FIX_NOW**) |
| 23 | S2: Nearest 15m parcel on intake_tep | C2 = 1,800.3 | 4,236.0 | TR01 530.0 / TR04 333.0 | No | **C2 OUT (+127.7 h)**; Plant/TR02/03/04/08 OUT (**FIX_NOW**) |
| 24 | S2: Cubic spline on intake_tep | C2 = 1,814.7 | 4,250.4 | TR01 527.9 / TR04 338.4 | No | **C2 OUT (+142.1 h)**; Plant/Q3/TR02/03/04/08 OUT (**FIX_NOW**) |
| 25 | S2: Fixed wall-clock CCF lag (rival) | C2 = 1,246.9 | 3,682.5 | TR02 372.5 (drops TR02) | **YES** | Refuted by F2: RMS 1.776 vs 0.523 mS/cm (3.4x worse) |
| 26 | S2: Steady-flow subset / Nominal vol / Same-ts | C2 = 960.4 / 575.2 / 552.1 | 3,396 / 3,011 / 2,988 | Drops TR02 (and TR01) | **YES** | Refuted by F2: RMS 1.859 / 1.991 / 2.473 vs 0.523 |
| 27 | S3: Per-train CIP, tied D3, <120h (base) | C3 = 1,107.1 | 4,088.6 | TR02 506.4 / TR04 318.8 | No | Exact match (NLL 7,405.80) |
| 28 | S3: Per-train CIP, posterior-by-quarter | C3 = 1,105.8 | 4,087.3 | TR02 506.4 / TR04 318.8 | No | All IN (shifts TR06/TR08 Q3 by -9/+10 h; Plant Q3 -1.9 h) |
| 29 | S3: Shared CIP clearing, tied D3, <120h | C3 = 1,184.3 | 4,165.8 | TR02 506.4 / TR04 323.0 | No | All IN (NLL 7,410.88) |
| 30 | S3: Free D3 bio-fouling (per-train / shared) | C3 = 1,055.1 / 1,176.4 | 4,036.6 / 4,157.9 | TR02 503.0 / TR04 318.0 | No | All IN (NLL 7,405.74 / 7,410.86) |
| 31 | S3: 96h / 144h post-CIP (per-train) | C3 = 1,187.9 / 1,151.4 | 4,169.4 / 4,132.9 | TR02 506.4 / TR04 321.9 | No | All IN (120h filed in `scada_bay_config_2026.json`) |
| 32 | S3: Shared + 96h / Shared + <=120h | C3 = 1,266.1 / 1,231.5 | 4,247.6 / 4,213.0 | TR02 511 / TR03 330.8 | No | C3 OUT (+48.5 / +13.9 h); departs from filed 120h = 30 blocks `[0,120)` |
| 33 | S3: 2-class cond-indep Dawid-Skene EM (rival) | C3 = 4,819.1 | 7,800.6 | TR03 1,465.3 / TR04 456.6 | **YES** | Refuted by LRT (`2*dNLL = 169.8 / 99.7`, `p < 1e-20`) & flat D3 post-CIP |
| 34 | S3: 2-of-3 / Post-CIP maj2 / 3-of-3 / Raw D3 | C3 = 3,508 / 2,146 / 275 / 1,179 | 6,490 / 5,127 / 3,256 / 4,160 | Flips TR03, TR04, or TR06 | **YES** | Refuted by CIP drop (`+5.0/+9.8 pp` on TR03/07) or uninverted channel sens |
| 35 | Plan/Cal: Flat 2026 (no Annex B) / Incl. 32 burn-in / TZ strip | Flat: TR01 382.3, TR02 380.5; Burn-in: C2=1,655.2; CIP-TZ strip: C3=1,118.7 | Flat flips TR01/02; others IN | Burn-in/TZ: No | Flat: **YES** | Flat & burn-in & TZ rules explicitly pinned by SWRO-Q27 Annex B, 2.2, 4.2 |
| 36 | **Strongest Standard Rival** (Pooled AR1 + Fixed-Lag CCF + 2-class DS) | B=1,147.2, S=1,246.9, St=4,819.1 | 7,213.2 | TR01 384.1, TR02 393.2 (MON); TR03 1,434.2, TR04 626.1, TR05 438.3 (OV) | **YES** | **Refuted on all 3 modes**: F1=0.229 vs 0.044; F2=1.776 vs 0.523 mS/cm; 128-cell LRT `2*dNLL=169.8` (`p<1e-29`) & invariant D3 on TR03 (`1.13%->1.16%`) and TR07 (`2.09%->1.97%`) |

### 3. Gate B, D, E Summary

- **Gate B (Filed facts & vocabulary):** All 14 files inspected (PDFs via `pypdf`, XLSX via `openpyxl`, JSON, CSVs). Every operative threshold (`0.50 mg/L`, `1.50 mg/L eq`, `1.50`, `400.0 h`), repeatability SD (`0.004 mg/L`), stabilization window (`120 h`), burn-in (`32` intervals), quarter calendar (`2160/2184/2208/2208 h`), timezone convention (`UTC` historian, `Europe/Lisbon` shift/CIP), unit conversion (`1,000 ug/L`, `3.6 m3/h`), Schedule B tariff (`420/360/540 EUR/h`), 2026 discrepancy formula, Annex B multipliers, and Annex C CSV schema are explicitly filed in `swro_integrity_standard_q27.pdf`, `lims_qa_certificate_2026.pdf`, `scada_bay_config_2026.json`, `train_asset_register.csv`, and `operating_plan_2027.csv`. All distinctive terms in `Final Recommendation` appear in the shipped files. The two distractors (`mibel_iberian_power_spot_2026.csv`, `algarve_reservoir_levels_2026.xlsx`) are cleanly out of scope under Standard SWRO-Q27.
- **Gates D & E (Asks & units):** `prompt.txt` pins one clear 400-hour overhaul call and one unambiguous unit and definition for every supplementary ask and deliverable via Standard SWRO-Q27.

## Fix

Edit `task28/submission.md` ONLY (`prompt.txt` and `target.zip` stay byte-identical; no rerun required):

1. **Widen upper bands in Final Recommendation, Supplementary Questions 1-2, and Critical Component 2** to cover standard non-linear / discrete-parcel `intake_tep_mg_l(t_dep)` lookup (`OU kriging`, `PCHIP`, `nearest`, `CubicSpline`), which preserve the exact 4-of-8 overhaul slate and remain >310 h above every rival:
   - Critical Component 2 & Supp Q2d (scaling): `1,560.4 to 1,672.6 h` -> `1,560.4 to 1,814.7 h`.
   - Plant-wide 2027 total (Final Rec & Supp Q2a): `3,787.7 to 4,234.9 h` -> `3,787.7 to 4,250.4 h`.
   - Plant-wide summer Q3 2027 total (Supp Q2c): `1,630.7 to 1,814.0 h` -> `1,630.7 to 1,829.8 h`.
   - Train total upper bounds (Supp Q1): `TR02` `523.7` -> `537.4 h`, `TR03` `326.2` -> `332.4 h`, `TR04` `328.0` -> `338.4 h`, `TR08` `275.1` -> `281.3 h`. (Overhaul subtotal `<= 3,028.6 h`, Plant Schedule B `<= EUR 1,824.4k`, Overhaul Schedule B `<= EUR 1,304.8k`, and 2026 discrepancy `113.5% to 125.4%` already contain all four variants.)
   - Note in Step 8 that the variant audit also spans nearest-parcel, PCHIP, cubic-spline, and OU-kriging evaluation of `intake_tep_mg_l(t_dep)`.
2. **Add missing base-specification sentences in Step-by-Step** so every base figure rebuilds without guessing:
   - **Step 3:** state the exact moment-matching WLS weights used on `(V4, C4, V8, C8)`, whether quarterly means are unweighted or hour-weighted, the Gaussian survival exceedance rule `1 - Phi((0.50 - mu_{u,q})/sigma_{1,u})`, and the L1 formula for F1 (`0.0479`).
   - **Step 4:** state that `Phi(t)` linearly interpolates hourly flows to 15-minute intervals via right-hand cumulative sum (`cumsum(0.25 * Q_15m)`), profiles `V_hat` on a 2 m3 grid, and evaluates `intake_cond_ms_cm` and `intake_tep_mg_l` at `t_dep` by linear interpolation.
   - **Step 5:** state that the base 3-state LCA uses per-train CIP clearing factors, ties bio-fouling `D3` to the clean `D3` floor, defines the 120-hour post-CIP regime as the 30 four-hour blocks with `0 <= (block_start - wash_completed) < 120 h`, allocates annual structural prevalence `pi_struct(u)` uniformly across 2026 quarters (`pi_struct(u) * q_hours[q]`), and states the exact F3 formula (`0.455 pp`).
