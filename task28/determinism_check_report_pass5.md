Manifest MD5s: prompt.txt=4b10b0cc7528dc0c3b63afbc52d99eae | target.zip=08ade1a3eb73b373d2c1ea16095dcccb | submission.md=3ea174f513104de25f6a8fd1f446ac0b

# Holistic Audit v4 (Determinism Mode) Report: task28 (Pass 5)

- **Workspace:** `/tmp/holistic-task28-determinism-s6m8jeer` (15 freshly unzipped input files, isolated `python3 -I` execution)
- **Audit scope:** Step 0 (Pre-flight), Part A (Solution Correctness), Part B (Determinism), and Gates A to E (Parts C and D excluded in determinism mode)
- **Verdict:** `NOT_DETERMINISTIC`
- **Disposition:** `SEND_BACK`

## v4 Part A / Part B Output Summary

- `correctness`: `incorrect` (Modes 1, 2, and 4 reproduce cleanly within stated bands and all 15 input-cleaning/raw-monitoring checks match exactly, but Mode 3 fails exact maximum-likelihood self-rebuilding: global MLE of the author's own Step 5 equation achieves strictly better log-likelihood `NLL = 12,630.15` vs author `12,633.58`, `2*dNLL = 6.86`, and yields `C3 = 962.6 h` vs author `406.0 h`, blowing the author's stated figures and uncertainty bands on C3, TR06, TR07, plant-wide total, overhaul total, summer Q3 total, plant-wide MWh, and overhaul MWh)
- `figures_checked`: `24`
- `mismatches`: `9` (Mode 3 C3 `struct_2027_h`: 962.6 h vs 406.0 h; TR06 struct: 630.9 h vs 406.0 h; TR06 total: 801.6 h vs 585.5 h; TR07 struct: 331.8 h vs 0.0 h; TR07 total: 1,828.4 h vs 1,486.9 h; Plant-wide 2027 total: 5,051.6 h vs 4,510.8 h; Overhaul-train 2027 total: 4,320.6 h vs 3,777.7 h; Plant-wide Q3 total: 2,313.2 h vs 2,167.7 h; Plant-wide energy penalty: 1,986.5 MWh vs 1,692.5 MWh and Overhaul-train energy penalty: 1,719.0 MWh vs 1,424.1 MWh, counting the two MWh asks together as the explicit second prompt quantity, or 10 counting Plant and Overhaul MWh separately)
- `decision_reproduces`: `no` (The 5-of-8 OVERHAUL/MONITOR train slate `{TR07, TR08, TR06, TR02, TR01}` vs `{TR04, TR05, TR03}` reproduces across all 3-emission-vector point estimators, though TR06's 95% profile-likelihood CI straddles 400.0 h; however, the prompt's explicit second main question on resulting energy penalty in MWh shifts by +295 to +301 MWh outside both stated MWh bands, and Annex B's required descending `total_2027_h` ordering flips TR06 above TR08)
- `determinism`: `not_pinned`
- `unpinned_forks`: `2` (Primary: Mode 3 continuous kinetic LCA likelihood ridge trading off `tau_min(TR06)` vs `pi_s(TR06)` and `e_bio[D3]` vs `pi_s(TR07)`, unpinned by any shipped file or native-unit F3 check, spanning `C3 = 314.1 to 1,046.2 h` and overhaul MWh `1,374 to 1,770 MWh`; Secondary/Gate C margin fragility: TR06's 400.0 h overhaul cutoff at `pi_s = 2.21%` sits inside its own 95% profile-likelihood CI `[1.70%, >8.5%]` where `pi_s = 1.70%` / `349 h` MONITOR has `2*dNLL = 3.80 < 3.84`)

---

## Step 0: Pre-flight Verification

1. **Golden present:** PASS. Final Recommendation, Supplementary Questions, Critical Components, and Step-by-Step all provide concrete computed values.
2. **Inputs belong to this task:** PASS. All 15 shipped files belong to Estacao Dessalinizadora de Alvor (Barlavento Dessalinizacao Municipal, E.M., western Algarve), covering trains `TR01` through `TR08` (legacy tags `LINE-A` through `LINE-H`), North Bay (`TR01..TR04`) and South Bay (`TR05..TR08`), full non-leap calendar year 2026 (`8,760 h`, `35,040` 15-minute intervals, `2,190` 4-hour shift blocks per train), and the 2027 operating plan under Engineering Protocol `SWRO-Q27` (`BDM-ENG-Q27-2026`).
3. **Giveaways check (Part B step 7):** PASS. Full-text, PDF-layout, and XLSX-XML sweeps across all 15 files confirm zero giveaways, zero scripts, zero hidden sheets (`Weekly_Storage_2026` is the only sheet in `algarve_reservoir_levels_2026.xlsx`), and zero occurrences of author decisive totals or methodology terms.
4. **Gate B vocabulary check:** PASS for action vocabulary. Every distinctive term in `FINAL_RECOMMENDATION` (`Barlavento`, `SWRO`, `pressure-vessel`, `overhaul`, `SWRO-Q27`, `400`, `OVERHAUL`, `MONITOR`, `MWh`, `energy penalty`, `permeate boron`, `scaling`, `structural`, `TDS`, `TR01..TR08`) is grounded in `swro_integrity_standard_q27.pdf` and `lims_qa_certificate_2026.pdf`.

---

## Part A: Independent Derivation and Correctness Audit

### A.1 Data Conformance and Anomaly Audit (Part B step 6)
All 15 shipped files were audited directly in code (`work/audit_data.py`):
- `permeate_boron_composites_2026.csv`: 15,456 raw rows -> 15,024 unique `sample_id` after keeping maximum `qa_revision` (432 `qa_revision=2` rows supersede rev 1 per SWRO-Q27 Clause 4.2 and LIMS QA Certificate Clause 2.2); 7,729 South Bay `ug/L` + `DD/MM/YYYY` rows and 7,727 North Bay `mg/L` + `YYYY-MM-DD` rows; 0 join mismatches with `autosampler_schedule_2026.csv` (2,920 rows, 720 legacy tags, exact `70,080` total bottle hours = `8 * 8,760`). One cleaned assay is `-0.011759 mg/L` (expected Gaussian ICP-OES repeatability noise near zero; retaining vs clamping to 0 changes nothing).
- `intake_chemistry_15m_2026.csv` and `ro_feed_header_15m_2026.csv`: 849 and 829 exact value-identical duplicate frames dropped (0 conflicting values across duplicates) -> exact `280,320` clean rows each (`8 * 35,040`). Burn-in exclusion of the first 32 intervals (`2026-01-01T00:00Z` through `07:45Z`) is explicitly mandated by Clause 2.2.
- `train_hydraulics_hourly_2026.csv`: 174 exact `RETRY_OK` duplicate rows dropped -> `70,080` clean rows (`35,040` South Bay `L/s` rows converted via `3.6 * L/s` per Clause 4.2).
- `bay_permeate_tds_hourly_2026.csv`: 55 exact `RETRY_OK` duplicate rows dropped -> `17,520` clean rows. Verified `max |bay_permeate_flow_m3_h - 0.45 * sum(Q_feed)| = 5.45e-5 m3/h` (exact uniform 45% recovery per Clause 2.4).
- `shift_diagnostics_2026.csv` (17,520 rows) and `cip_wash_log_2026.csv` (308 rows: 153 `CIP_ALK_pH11`, 155 `CIP_ACID_pH2`, 161 legacy tags, 16 late-Dec 2025 carryover washes = exact 1 acid + 1 alk per train): all timestamps parse cleanly via explicit `+00:00`/`+01:00` Europe/Lisbon offsets (including the 29 March 2026 DST transition) onto the exact 4-hour UTC grid (`0` off-grid timestamps, `0` duplicates).
- `operating_plan_2027.csv`: exact `scheduled_output_2027_km3 / baseline_output_2026_km3 == dispatch_duty_ratio_2027` (`max diff = 2.22e-16`), and seasonal factors match Annex A.2 verbatim.
- `mibel_iberian_power_spot_2026.csv` (8,760 rows) and `algarve_reservoir_levels_2026.xlsx` (52 rows): confirmed out-of-scope regional context distractors (SWRO-Q27 Clause 4.3 pins energy penalties strictly in physical MWh using fixed kWh/h factors, not EUR spot prices).

### A.2 Independent Derivation vs Author Values (Deciding Figures Table)

Independent derivations (`work/repro_m1_m2_fast.py`, `work/repro_m3_m4_fast.py`, `work/check_final_details.py`) used:
- **Mode 1:** Per-train mass-flux OLS (`M_k = Q_bar_k * C_k = alpha_{u,q} * Q_bar_k + mu_{J,u} + e_k`), removing `(Q_bar_k * 0.004)^2` lab repeatability variance, fitting discrete 1-hour AR(1) flux moments `(V4, C4, V8, C8)` via inverse-variance WLS (`AR1_WLS_var`) and verified by exact banded-Cholesky Gaussian MLE (`Banded_MLE`).
- **Mode 2:** Variable-flow cumulative volume `Phi(t) = cumsum(0.25 * Q_15m)` via linearly interpolated 15-minute flow (which achieves pooled conductivity RMS `0.34043 mS/cm` at the `0.340` probe floor vs `0.415` step-left and `0.491` step-right), fitting unconstrained two-path bimodal mixing (`V_main` allowed up to `2,000 m3`, no artificial 1,600 m3 cap) and verified by unconstrained 81-bin non-parametric NNLS deconvolution (`RMS = 0.34042 mS/cm`).
- **Mode 3:** Multi-start exact maximum likelihood (`L-BFGS-B` with analytic gradients verified against finite differences to `check_grad = 6.87e-4` on `NLL ~ 13,000`) of the exact continuous kinetic 3-emission-vector latent-class model (`w_bio = pi_bio * (1 - exp(-dt_alk / tau_bio))`, `w_MS = pi_s + pi_min * (1 - exp(-dt_acid / tau_min))`), with no unstated `tau_min` upper cap and converged to `ftol = 1e-14`.
- **Mode 4:** Quarterly flow-share OLS means + heteroscedastic Gaussian variance-component MLE removing `3.5^2` inline probe variance (`Var(r_bay) = 3.5^2 + sum w_{u,t}^2 * sigma_u^2`), verified by joint GLS+MLE and temporal AR(1) Gaussian MLE (`rho = 0.35`).

| # | Deciding Figure / Answer | Independent Exact MLE | Author Value (Author Band) | Diff | Verdict |
|---|---|---|---|---|---|
| 1 | Overhaul slate (5 of 8) | TR07, TR06, TR08, TR02, TR01 | TR07, TR08, TR06, TR02, TR01 | Slate same; #2/#3 rank flips | Partial (rank flips) |
| 2 | Monitor slate (3 of 8) | TR04, TR05, TR03 | TR04, TR05, TR03 | Exact match | Agree |
| 3 | C1: Plant boron 2027 (h) | 1,177.1 (Banded MLE: 1,158.7) | 1,192.4 (1,026.1 to 1,225.0) | -15.3 (-1.3%) | Agree (in band) |
| 4 | C2: Plant scaling 2027 (h) | 1,645.4 (NNLS: 1,641.4) | 1,646.0 (1,552.8 to 1,649.7) | -0.6 (-0.04%) | Agree (exact) |
| 5 | **C3: Plant structural 2027 (h)** | **962.6** | **406.0 (358.4 to 493.6)** | **+556.6 (+137%)** | **MISMATCH (outside band)** |
| 6 | C4: Plant TDS 2027 (h) | 1,266.5 | 1,266.4 (1,244.3 to 1,416.1) | +0.1 (+0.01%) | Agree (exact) |
| 7 | **TR07 total 2027 (h)** | **1,828.4** (St=331.8) | **1,486.9 (1,412.9 to 1,645.8)** | **+341.5** | **MISMATCH (outside band)** |
| 8 | TR08 total 2027 (h) | 711.5 | 712.5 (649.0 to 727.1) | -1.0 | Agree (in band) |
| 9 | **TR06 total 2027 (h)** | **801.6** (St=630.9) | **585.5 (536.0 to 650.6)** | **+216.1** | **MISMATCH (outside band)** |
| 10 | TR02 total 2027 (h) | 529.3 | 528.5 (490.2 to 539.2) | +0.8 | Agree (in band) |
| 11 | TR01 total 2027 (h) | 449.9 | 464.4 (438.5 to 473.0) | -14.5 | Agree (in band) |
| 12 | TR04 total 2027 (h) | 286.2 | 285.2 (272.5 to 294.5) | +1.0 | Agree (in band) |
| 13 | TR05 total 2027 (h) | 236.5 | 234.7 (221.6 to 294.5) | +1.8 | Agree (in band) |
| 14 | TR03 total 2027 (h) | 208.3 | 213.1 (198.8 to 222.6) | -4.8 | Agree (in band) |
| 15 | **Plant-wide total 2027 (h)** | **5,051.6** | **4,510.8 (4,344.5 to 4,660.5)** | **+540.8** | **MISMATCH (outside band)** |
| 16 | **Overhaul subtotal 2027 (h)** | **4,320.6** | **3,777.7 (3,641.4 to 3,867.8)** | **+542.9** | **MISMATCH (outside band)** |
| 17 | **Plant-wide Q3 2027 (h)** | **2,313.2** | **2,167.7 (2,104.4 to 2,255.7)** | **+145.5** | **MISMATCH (outside band)** |
| 18 | **Plant-wide energy (MWh)** | **1,986.49** | **1,692.51 (1,622.7 to 1,739.8)** | **+293.98 (+17.4%)** | **MISMATCH (outside band)** |
| 19 | **Overhaul energy (MWh)** | **1,718.98** | **1,424.11 (1,366.8 to 1,471.4)** | **+294.87 (+20.7%)** | **MISMATCH (outside band)** |
| 20 | **TR06 structural 2027 (h)** | **630.9** (`pi_s=6.33%`) | **406.0** (`pi_s=4.07%`) | **+224.9** | **MISMATCH** |
| 21 | **TR07 structural 2027 (h)** | **331.8** (`pi_s=3.25%`) | **0.0** (`pi_s=0.00%`) | **+331.8** | **MISMATCH** |
| 22 | TR03 structural 2027 (h) | 0.0 (`pi_s=0.00%`) | 0.0 (`pi_s=0.00%`) | 0.0 | Agree |
| 23 | Direct monitoring raw 2027 (h) | 8,891.0 (all 8 trains exact) | 8,891.0 | 0.0 | Agree (exact) |
| 24 | Flat-2026 TR01 / TR02 drop | 333.3 / 378.5 (< 400) | 344.3 / 377.8 (< 400) | Both < 400 | Agree |

Note: Plugging the author's own Mode 3 figure (`406.0 h`) into our independent Modes 1, 2, and 4 immediately yields Plant total `4,494.9 h`, Overhaul total `3,763.9 h`, Q3 `2,163.7 h`, Plant energy `1,685.87 MWh`, and Overhaul energy `1,418.36 MWh`, all squarely inside the author's stated bands. Every single mismatch traces 100% to Mode 3.

### A.3 Forensic Dissection of the Mode 3 Disagreement (Part A Step 4)
We tested every candidate explanation in code (`work/forensic_m3.py`, `work/forensic_m3_part2.py`, `work/forensic_m3_part3.py`, `work/forensic_m3_profile.py`, `work/verify_everything.py`):
1. **The author's Step 5 equation does NOT reproduce `406.0 h` under exact MLE (Self-Rebuilding Step-by-Step FAIL):**
   - Fitting the exact model stated in Step 5 (`w_bio = pi_bio * (1 - exp(-dt_alk / tau_bio))`, `w_MS = pi_s + pi_min * (1 - exp(-dt_acid / tau_min))`, shared 3 emission vectors) by converged multi-start `L-BFGS-B` reaches **`NLL = 12,630.153`** with `Clean = [0.0146, 0.0103, 0.0093]`, `Bio = [0.6950, 0.9720, 0.0000]`, `MS = [0.8138, 0.2649, 0.5514]`, `TR06 pi_s = 6.33%` (`tau_min = 609.8 h`, `630.9 h` in 2027), and `TR07 pi_s = 3.25%` (`tau_min = 141.6 h`, `331.8 h` in 2027), giving **`C3 = 962.6 h`**.
   - Evaluating the author's stated emissions (`Clean [0.014, 0.010, 0.010]`, `Bio [0.703, 0.868, 0.043]`, `MS [0.821, 0.235, 0.589]`) gives **`NLL = 12,633.58`** (with `tau_min <= 300 h`) or **`12,633.48`** (unconstrained `tau`), which is **3.43 log-likelihood units WORSE (`2*dNLL = 6.86`)** than global MLE.
   - Native-unit `F3` (fine-age post-acid `D3` trajectory check across `0-16 h`, `16-120 h`, `>= 120 h`) does NOT reject global MLE: 3-pool MAE is **`0.223 pp`** for global MLE (`C3 = 962.6 h`) vs **`0.222 pp`** for author-emissions `tau <= 300` (`C3 = 406.0 h`), and on 24-cell (8 trains x 3 age bins) MAE global MLE is actually **better** (`0.710 pp` vs `0.757 pp`).
2. **Exact mechanism that produced the author's `406.0 h` (two unstated, unfiled non-MLE constraints):**
   - **Unstated active ceiling `tau_min <= 300 h`:** On `TR06`, observed `(D1 & D3)` rises slowly across the entire 480 h CIP cycle (`2.6%` at 0-16 h, `1.8%` at 16-40 h, `3.3%` at 40-80 h, `4.9%` at 80-120 h, `5.4%` at 120-180 h, `6.4%` at 180-260 h, `6.9%` at 260-360 h, `8.5%` at 360-600 h) without plateauing. Fixing the author's emissions and sweeping the upper bound on `tau_min` shows `TR06` hits the wall at every cap: `tau <= 120 h` gives `pi_s = 2.80%` (279 h); `tau <= 200 h` gives `3.51%` (350 h); **`tau <= 300 h` hits `tm = 300.0 h` and gives `4.08%` (`406.0 h`)**; `tau <= 500 h` hits `500.0 h` (`4.66%`, 464 h); unconstrained `tau` lands at `563.6 h` (`4.76%`, 474 h). No shipped document specifies `tau_min <= 300 h`.
   - **Premature EM stopping / unstated emission regularization:** Running alternating EM with `tau in [4, 300]` from standard initialization yields at **iter 5** `NLL = 12,634.64`, `C3 = 404.2 h` (`TR06 = 384.6`, `TR07 = 18.7`); at **iter 10** `NLL = 12,633.07`, `em_bio = [0.701, 0.865, 0.032]`, `TR03 tau_min = 22.9 h`, `TR06 = 402.6 h` (`4.04%`, `tm = 300.0`), `TR07 = 7.9 h`, `C3 = 410.5 h`; at **iter 20** `NLL = 12,632.11`, `C3 = 455.0 h`; at **iter 40** `NLL = 12,631.26`, `C3 = 587.2 h` (`TR06 = 456.5`, `TR07 = 130.7`), crawling down the flat ridge (`dNLL < 0.09/iter`) toward the true MLE `12,630.15` (`962.6 h`).
3. **Every standard regularized, BIC-pruned, two-step, or alternative-kinetic MLE STILL exceeds the author's stated C3 and MWh bands:**
   - Weak Jeffreys `Beta(1.5, 1.5)` emission MAP (preventing `e_bio[D3] = 0` boundary collapse): `pure_NLL = 12,630.51`, `em_bio = [0.697, 0.939, 0.017]`, `TR06 = 583.9 h`, `TR07 = 174.6 h`, **`C3 = 758.5 h`** (+264.9 h above band; Overhaul MWh `1,614.5`).
   - Laplace `Beta(2, 2)` MAP: `pure_NLL = 12,630.89`, `TR06 = 562.3 h`, `TR07 = 114.2 h`, **`C3 = 676.6 h`** (+183.0 h above band; Overhaul MWh `1,570.2`).
   - Strong `Beta(3, 3)` MAP: `pure_NLL = 12,631.65`, `TR06 = 534.1 h`, `TR07 = 38.2 h`, **`C3 = 572.4 h`** (+78.8 h above band; Overhaul MWh `1,514.0`).
   - BIC-pruned `TR06`-only MLE (`pi_s = 0` forced on all other 7 trains, since TR07 LRT `2*dNLL = 1.30` is insignificant): **`C3 = 607.2 h`** (free `tau`, `tm = 661.1 h`, `NLL = 12,630.80`; Overhaul MWh `1,532.7`) and **`516.2 h`** (`tau <= 300`, `NLL = 12,630.93`; Overhaul MWh `1,483.6`).
   - Two-step static per-train 3-class LCA emissions + kinetic MLE (free `tau`): `NLL = 12,634.29`, **`C3 = 509.0 h`** (`TR06 tm = 649.3 h`; Overhaul MWh `1,479.7`).
   - Step 9's own four named alternative kinetic curves fit by converged MLE: Volume-Exp **`954.4 h`**, Michaelis-Menten **`889.9 h`**, Weibull `k=1.2` **`1,046.2 h`**, Weibull `k=0.9` **`902.4 h`**. All four sit +396 to +553 h above the author's claimed upper bound `493.6 h`.
   - **Outcome classification:** **Both author error** (Step 5 fails exact MLE self-rebuilding and Step 9 misstates the range of its own named kinetic variants) **AND unpinned data-level fork** carried into Part B (equally defensible MLE, MAP, BIC-pruned, and 2-step estimators span `314.1 to 1,046.2 h` on C3 and `1,374 to 1,770 MWh` on overhaul energy penalty).

### A.4 Internal Consistency Across the Four Answer Blocks (Part A Step 5)
- Arithmetic across Final Recommendation, Supplementary Questions, Critical Components, and Step-by-Step is internally consistent to rounding (`<= 0.1 h` on train/plant/Q3 sums and `<= 0.05 MWh` on energy conversions; `+/-20%` independent mode perturbations reproduce `min_OV = 414.6 h` vs author `414.5 h` and `max_MON = 307.7 h` vs author `307.6 h`).
- Direct monitoring claims in Final Recommendation and Step 2 reproduce identically (`8,891.0 h`; TR01 `201.3`, TR02 `224.0`, TR03 `2,691.8`, TR04 `355.4`, TR05 `958.2`, TR06 `1,433.5`, TR07 `2,656.2`, TR08 `370.6`).
- Mode 1, Mode 2, and Mode 4 shortcut/rival ablation claims in Steps 3, 4, 6, and closing paragraph reproduce cleanly.
- **Internal consistency failure:** Step 5's stated model does NOT reproduce `406.0 h` under converged MLE (`962.6 h` instead), and Step 9's stated 29-variant bands (`358.4 to 493.6 h` C3; `1,366.8 to 1,471.4 MWh` overhaul; `1,622.7 to 1,739.8 MWh` plant-wide) fail to contain converged MLE of Step 5's own model or Step 9's four named post-CIP kinetic variants.

---

## Part B: Determinism Analysis and Fork Table

### B.1 Committed Recommendation and Deciding Steps
- **Committed calls:** (1) Overhaul `{TR07, TR08, TR06, TR02, TR01}` and monitor `{TR04, TR05, TR03}` under SWRO-Q27 Clause 3.1 (`>= 400.0 h`); (2) Report projected 2027 excess desalination energy penalty (`1,424.1 MWh` overhaul / `1,692.5 MWh` plant-wide) plus train-level forecasts sorted descending in `barlavento_train_diagnostics_2027.csv`.
- **Deciding steps separating golden from raw/textbook rivals:**
  - S1 (Mass-flux heteroscedastic boron AR(1) deconvolution): opens `TR01` (`221.3 -> 464.4 h`) while keeping `TR04` monitored (`285.2 h` vs `755.5 h` under i.i.d. `sqrt(m)` scaling).
  - S2 (Variable-flow cumulative-volume two-path hydraulic mixing): opens `TR02` (`197.9 -> 528.5 h`) while keeping `TR05` monitored (`234.7 h` vs `438-446 h` under 1-plug/fixed-lag).
  - S3 (Continuous post-CIP kinetic latent-class deconvolution): clears `TR03` (`2,846-3,300 -> 213.1 h`) while retaining `TR06` (`>= 400 h`).
  - S4 (Shared-bay permeate TDS heteroscedastic variance-component MLE): opens `TR08` (`318.5 -> 712.5 h`) while keeping `TR05` monitored (`234.7 h` vs `980.1 h` under equal-variance pooling).

### B.2 Comprehensive Coded Fork Table (26 Alternatives Run in Code)

Baseline non-perturbed modes use author M1/M2/M4 when isolating M3 forks, or author M3 when isolating M1/M2/M4 forks, to isolate each fork cleanly.

| # | Decision Point / Fork | Mode / Scope | Computed Mode / Key Output | Leaves Author Band? | Flips Overhaul Call or Explicit MWh / Rank? | Pin Status (File & Computed Refutation) |
|---|---|---|---|---|---|---|
| 1 | Exact Banded-Cholesky Gaussian flux MLE | M1 Estimator | C1 = 1,158.7 h (TR01: 222.7, tot 437.5 h) | No (in 1,026.1-1,225.0) | No | Pinned (in band, same call) |
| 2 | Inverse-variance WLS `(V4,C4,V8,C8)` AR(1) | M1 Weights | C1 = 1,177.1 h (TR01: 235.0, tot 449.8 h) | No | No | Pinned (in band, same call) |
| 3 | Unweighted OLS `(V4,C4,V8,C8)` AR(1) | M1 Weights | C1 = 1,148.9 h (TR01: 248.3) | No | No | Pinned (in band, same call) |
| 4 | Continuous OU (1-hour block avg, WLS-rel vs WLS-var) | M1 Process | C1 = 1,045.0 h (rel) / 1,011.4 h (var; TR01: 208.3, tot 423.1 h) | Marginal (-14.7 h on var) | No (TR01 >= 423 h) | Note: Clause 2.1 pins 1-hour block (rules out instantaneous OU 2,337.2 h); widen lower band by 15 h |
| 5 | Huber flux regression / 0.5% trim / quarterly `mu_J` | M1 Robustness | C1 = 1,176.3 / 1,161.9 / 1,173.1 h | No | No | Pinned (all in band) |
| 6 | 4h-only `(V4,C4)` / Lab noise off (`0.000` vs `0.004`) | M1 Scope/Const | C1 = 1,193.2 / 1,194.0 h | No | No | Pinned (`lims_qa_certificate_2026.pdf` pins `0.004 mg/L`; in band either way) |
| 7 | Homoscedastic `a + c/Q` AR(1) (Strong Rival) | M1 Rival | C1 = 524.2 h (TR01: 81.2 -> drops TR01 to 296.0 h) | Yes | **Flips TR01** | **Refuted by data:** `permeate_boron_composites_2026.csv` shows constant flux SD (`TR01`: 29.51 low-Q vs 30.07 high-Q) and strong concentration heteroscedasticity (`0.0729` low-Q vs `0.0447` high-Q) |
| 8 | Flux i.i.d. `sqrt(m)` scaling (Strong Rival) | M1 Rival | C1 = 2,702.5 h (TR04: 581.9 -> flips TR04 to 755.3 h) | Yes | **Flips TR04** | **Refuted by data:** `TR04` has `V4/V8 = 1.065` and `r4 = 0.684` (vs i.i.d. `V4/V8 = 2.00`, `r4 = 0.00`) |
| 9 | Unconstrained 81-bin non-parametric NNLS RTD | M2 Functional Form | C2 = 1,641.4 h (TR02: 406.6, TR05: 177.7), RMS = 0.34042 | No (in 1,552.8-1,649.7) | No | Pinned (identical to parametric 2-path `1,645.7 h`) |
| 10 | Flow integration (`linear_trapz` / `step_left` / `midpoint` / `step_right`) | M2 Integration | C2 = 1,633.5 / 1,558.9 / 1,552.8 / 1,456.1 h | Only `step_right` | No (`TR02 >= 460 h`) | Pinned by conductivity RMS: `linear_interp` hits `0.3404 mS/cm` floor vs `0.415` step-left and `0.491` step-right |
| 11 | Conductivity loss L1 / Nearest TEP lookup | M2 Loss/Interp | C2 = 1,646.1 h (L1) / 1,654.4 h (nearest) | +4.7 h on nearest | No | Pinned (negligible 0.3% shift, same call) |
| 12 | Fixed lag CCF / 1D single-plug `V_eff` / `V_nom` (Strong Rivals) | M2 Rivals | Fixed: TR02 386.2, TR05 446.4; 1-plug: TR05 438.0; `V_nom`: TR02 247.7 | Yes | **Flips TR02/TR05** | **Refuted by data:** Conservative seawater conductivity RMS is `1.196` (fixed lag), `0.662` (1-plug), `0.979` (`V_nom`), `1.910` (same-time) vs `0.3404 mS/cm` two-path/NNLS floor |
| 13 | **Exact converged 3-em kinetic LCA MLE (free `tau`, `L-BFGS-B`)** | **M3 Optimizer / Cap** | **C3 = 962.6 h (TR06 630.9, TR07 331.8); Overhaul MWh = 1,719.0; Plant MWh = 1,986.5** | **YES (+469 h C3; +248 MWh)** | **YES (explicit MWh ask +295 MWh; TR06 > TR08 rank flips)** | **NO PIN FOUND:** Strictly higher log-likelihood (`NLL = 12,630.15` vs author `12,633.58`, `2*dNLL = 6.86`) and identical F3 (`0.223` vs `0.222 pp`) |
| 14 | **Exact converged MLE of Step 9 curves (Vol-Exp / MM / Weibull 1.2 / 0.9 / Midpoint +2h)** | **M3 Curve Form** | **C3 = 954.4 / 889.9 / 1,046.2 / 902.4 / 848.3 h (Overhaul MWh 1,685-1,770)** | **YES (+355 to +553 h C3)** | **YES (explicit MWh ask; TR06 > TR08 rank)** | **NO PIN FOUND:** All five converged MLEs achieve `NLL = 12,629.2-12,632.8` (beating author `12,633.58`) |
| 15 | **Weak MAP emission smoothing (`Beta(1.5,1.5)` / `Beta(2,2)` / `Beta(3,3)`)** | **M3 Regularization** | **C3 = 758.5 / 676.6 / 572.4 h (Overhaul MWh 1,514-1,615)** | **YES (+79 to +265 h C3)** | **YES (explicit MWh ask; TR06 > TR08 on Beta 1.5)** | **NO PIN FOUND:** Prevents `e_bio[D3]=0` collapse yet still exceeds author C3 and MWh bands (`pure_NLL = 12,630.5-12,631.7`) |
| 16 | **BIC-pruned TR06-only MLE (`pi_s=0` on other 7 trains, free `tau` vs `tau<=300`)** | **M3 Model Selection** | **C3 = 607.2 h (free) / 516.2 h (`tau<=300`); Overhaul MWh = 1,532.7 / 1,483.6** | **YES (+23 to +114 h C3)** | **YES (explicit MWh ask; TR06 > TR08 on free `tau`)** | **NO PIN FOUND:** `TR07 pi_s` is insignificant (`2*dNLL = 1.30`), yet TR06's unconstrained `tau_min = 661.1 h` still drives C3 and MWh above bands |
| 17 | **Two-step static 3-class LCA emissions -> kinetic MLE (per-train vs pooled; free `tau` vs `tau<=300`)** | **M3 Two-step / Cap** | **C3 = 509.0 / 429.9 (per-train) and 384.4 / 314.1 h (pooled)** | **YES (314.1 to 509.0 h)** | **YES (explicit MWh 1,374-1,480)** | **NO PIN FOUND:** No file pins `tau_min <= 300 h` or per-train vs pooled static emission initialization |
| 18 | **Profile-likelihood 95% CI on `TR06 pi_s` (Gate C margin fragility)** | **M3 Identifiability** | **`TR06 pi_s = 1.70%` (169.4 h struct -> TR06 total 349 h MONITOR) has `2*dNLL = 3.80 < 3.84`; 400 h boundary (`2.21%`) has `2*dNLL = 2.83`** | **YES** | **Straddles TR06 400.0 h cutoff inside 95% CI** | **NO PIN FOUND (Gate C noise fragility):** Flat `pi_s` / `tau_min` ridge on TR06 (`tau_min` 174 to 2,387 h) puts MONITOR inside the 95% profile CI |
| 19 | Factorial Noisy-OR co-occurring Bio & MS | M3 Structure | `NLL = 12,641.31`; `TR06 = 6.83%`, `TR07 = 3.77%`, `C3 ~ 1,065 h` | Yes | MWh ask & rank | Refuted vs mutex by `dNLL = +11.16` (mutex fits substantially better) |
| 20 | 4-emission-vector kinetic LCA (`e_min != e_str`, Strong Rival) | M3 Emission Share | `NLL = 12,625.60`, `F3 = 0.267 pp`; `TR03 = 563.2 h` -> **flips TR03 to 776 h OVERHAUL** | Yes | **Flips TR03** | **Weakly refuted by BIC & boundary collapse:** `2*dNLL = 9.10` on 3 extra df is rejected by BIC (`dBIC = +20.21`), collapses `e_str[D2] = 0.000`, and overpredicts TR03 `0-16 h` D3 (`6.89%` vs `4.17%`) |
| 21 | Unconditioned 3-class LCA / Static 120h 4-class EM / 3-of-3 MV (Strong Rivals) | M3 Rivals | Uncond: TR03 3,353 h; Static 120h: TR03 3,599 h; 3-of-3: TR06 drops to 347.2 h | Yes | **Flips TR03 / TR06** | **Refuted by data:** F3 (3-pool MAE) is `2.269 pp` (uncond) and `1.174 pp` (static 120h) vs `0.222 pp` kinetic; 3-of-3 ignores conditional independence of imperfect sensors |
| 22 | Mode 4 Joint GLS+MLE / OLS-sq / WLS-sq / Huber mean / No-meter | M4 Estimator | C4 = 1,278.9 / 1,306.5 / 1,262.2 / 1,244.4 / 1,346.5 h | No (in 1,244.3-1,416.1) | No | Pinned (all in band; `lims_qa_certificate_2026.pdf` + `scada_bay_config_2026.json` pin `3.5 mg/L`) |
| 23 | Mode 4 Temporal AR(1) Gaussian MLE (`rho = 0.35`) | M4 Autocorrelation | C4 = 1,302.2 h (`TR05: 4.3, TR08: 393.6, TR07: 570.3`) | No (in 1,244.3-1,416.1) | No | Pinned (accounting for lag-1 bay residual autocorr `0.33` keeps C4 squarely in band) |
| 24 | Mode 4 Unconstrained quarterly-sigma MLE vs annual sigma | M4 Variance Window | C4 = 1,601.2 h (`TR05: 214.4 -> tot 448.4 h`) | Yes | **Flips TR05** | **Refuted by data (LRT):** Quarterly vs annual sigma LRT is insignificant (`North: 7.02, 12 df, p = 0.856`; `South: 14.92, 12 df, p = 0.246`) and suffers boundary collapse (`TR05 = 0.05` in Q4, `TR06 = 1.03` in Q2). Note: clarify Step 9 wording ("quarterly MLE") |
| 25 | Mode 4 Equal-variance bay pooling / Direct bay exceedances (Strong Rivals) | M4 Rivals | Equal-var: TR08 drops to 371.5 h, TR05 blows up to 978.1 h; Direct bay: TR08 drops to 318.5 h | Yes | **Flips TR08/TR05** | **Refuted by data:** South Bay flow-share quartile SD MAE is `0.173 mg/L` (heteroscedastic MLE) vs `1.149 mg/L` (equal-var pooling); common-bay shock LRT is insignificant (`1.33`, `p = 0.25`) |
| 26 | Flat 2026 totals vs Annex A 2027 forecast | Horizon / Annex A | Flat 2026 drops TR01 to 333-344 h and TR02 to 378 h | Yes | **Flips TR01/TR02** | **Pinned by prompt & SWRO-Q27 Annex A:** Prompt asks for 2027 projected rates; Annex A.1-A.2 and `operating_plan_2027.csv` specify exact quarterly scaling equations |

---

## Gates A to E Assessment

- **Gate A (Solution correct given shipped files):** **FAIL.** Modes 1, 2, and 4 are correct and cleanly reproduced, and raw/rival claims reproduce accurately. However, Mode 3 (`406.0 h`, `TR06 = 406.0 h`, `TR07 = 0.0 h`) does NOT reproduce from exact MLE of Step 5's own continuous kinetic LCA model (`NLL = 12,630.15` vs author `12,633.58`; global MLE gives `C3 = 962.6 h`, `+556.6 h` / `+137%`, shifting Plant MWh from `1,692.5` to `1,986.5 MWh` and Overhaul MWh from `1,424.1` to `1,719.0 MWh`), and Step 9's stated uncertainty bands fail to cover converged MLE of Step 9's own four named post-CIP kinetic curves (`890 to 1,046 h`).
- **Gate B (Every decisive fact present in shipped files):** **FAIL (unstated Mode 3 constraints).** All protocol definitions, thresholds, units, repeatability SDs, recovery factor, clocks, Annex A factors, and recommendation vocabulary are properly grounded in the 15 shipped files. However, the two numerical constraints required to obtain the author's `406.0 h` Mode 3 answer (`tau_min <= 300 h` ceiling actively binding on TR06 + early EM stopping / strong emission prior near `em_bio = [0.703, 0.868, 0.043]`) appear nowhere in any shipped file.
- **Gate C (Answer uniquely forced; operationalization and margin robustness):** **FAIL.** Two unpinned Mode 3 defects exist in `shift_diagnostics_2026.csv`:
  1. Across equally defensible, F3-passing (`0.222-0.226 pp`) 3-emission-vector kinetic estimators (converged MLE, weak Jeffreys/Laplace MAP, BIC-pruned TR06-only MLE, 2-step static-em MLE, and Step 9's own Weibull/MM/Vol-Exp kinetic variants), `C3` spans `314.1 to 1,046.2 h` (3.3x), directly shifting the prompt's explicit second deciding ask (`MWh` energy penalty) across `1,374 to 1,770 MWh` (overhaul) and `1,643 to 2,038 MWh` (plant-wide), and flipping Annex B's `TR06` vs `TR08` descending sort rank.
  2. `TR06`'s 400.0 h overhaul criterion (`pi_s >= 2.21%`) lies inside `TR06`'s own 95% profile-likelihood confidence interval (`pi_s = 1.70%`, `TR06 = 349 h` MONITOR, has `2*dNLL = 3.80 < 3.84`; `2.21%` has `2*dNLL = 2.83`) due to collinearity between `pi_s(TR06)` and `tau_min(TR06)` (which never plateaus within the 480 h CIP cycle).
- **Gate D (Analytical hardness, not ambiguity):** **PARTIAL FAIL.** Modes 1, 2, and 4 are clean, fair, physics-pinned analytical stumps. Mode 3's conceptual stump (continuous post-CIP kinetics clearing fast-regrowing TR03 while preserving structural TR06) is sound, but its numerical output in the shipped `shift_diagnostics_2026.csv` turns on unstated optimizer caps and early EM termination rather than analytical skill.
- **Gate E (Prompt unambiguous on decision, not method):** **PASS.** The prompt cleanly specifies the two-part decision (which trains need 2027 vessel overhauls and the resulting energy penalty in MWh) and deliverable types without leaking methods or file names; `swro_integrity_standard_q27.pdf` pins the exact overhaul rule, quarterly boundaries, Annex A formulas, Section 4 MWh rates (both plant-wide and overhaul subtotals), and Annex B CSV columns.

---

## Exact Fix Required (SEND_BACK)

Answer-block edits alone (`FIX_NOW`) cannot resolve a 3.3x flat likelihood ridge in Mode 3 (`C3` spanning `314 to 1,046 h` and `MWh` spanning `396 MWh`) where `TR06`'s 95% profile CI straddles the 400.0 h threshold. The pack data (`shift_diagnostics_2026.csv` inside `target.zip`) and generator verification must be updated as follows:

1. **Fix (`target/shift_diagnostics_2026.csv` Mode 3 DGP for `TR06`, `TR07`, and `Bio-Fouling` emissions):**
   - **Sharpen `TR06` identifiability:** Generate `TR06` with a clearly plateauing mineral-crust time constant (`tau_min` around `50 to 80 h`, well inside the ~480 h CIP cycle rather than `~600 h`, or reduced `pi_min` on `TR06`) and a clearly separated structural prevalence (`pi_s` around `5.0% to 6.0%`, ~500 to 600 h in 2027) so that unconstrained `tau_min(TR06)` never drifts past 300 h, `TR06` never hits an artificial ceiling, and `TR06`'s 95% profile-likelihood lower bound stays strictly above the `400.0 h` overhaul threshold (`2*dNLL > 6` at `400.0 h`).
   - **Eliminate the `e_bio[D3]` / `pi_s(TR07)` ridge:** Give `Bio-Fouling` clean sensor separation (`e_bio[D3]` genuinely near `0.01` to `0.02` with high `D2` and clean early post-acid `0-16 h` drop on `TR07` using a faster `tau_min(TR07)` around `60 to 90 h`) so that **exact unconstrained converged MLE (`L-BFGS-B` with analytic gradients, `gtol <= 1e-8`, no `tau_min <= 300 h` cap, no early EM stop)** cleanly recovers `pi_s(TR07) ~ 0.0%` (`< 0.3%`), `pi_s(TR03) = 0.0%`, and a tight `pi_s(TR06)` that agrees across exact MLE, Laplace/Jeffreys MAP, BIC-pruned MLE, 2-step static-em MLE, and all four Step 9 alternative kinetic curves (Volume-Exp, Michaelis-Menten, Weibull `k=1.2`, Weibull `k=0.9`) inside a narrow `+/-10% to 15%` band on `C3` and `< +/-40 MWh` on energy penalties (with invariant TR06 vs TR08 rank order if `TR06` stays clearly below or clearly above `TR08`).
2. **Fix (`submission.md` Step 3, Step 5, Step 9, and uncertainty bands after pack rebuild):**
   - Compute Mode 3 golden figures and all 29 uncertainty variants using **converged exact MLE** (no active `tau` cap and no early EM termination) and verify in code that every named variant in Step 9 (including Mode 1 `OU_1h_WLSvar` 1-hour block average and exact `Banded_MLE`) sits inside the reported bands.
   - In Step 3, state the exact WLS moment weighting used on `(V4, C4, V8, C8)` so Mode 1 point figures self-rebuild to 0.1 h.
   - In Step 9, clarify "quarterly MLE for bay TDS" (either quarterly means + annual variance, or remove unconstrained quarterly-sigma MLE which LRT rejects at `p = 0.25 / 0.86` and which collapses `TR05` sigma to `0.05 mg/L` in Q4).
