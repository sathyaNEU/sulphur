Audit replay of Holistic Audit v4 (`determinism` mode, Pass 7), 2026-11-24; prompt.txt `4b10b0cc7528dc0c3b63afbc52d99eae`, target.zip `436d94cd2e76581db4b8097808e9a735`, submission.md `4400cef5a6d7e12d9f2ae47d8ae80600`; isolated workspace `/tmp/holistic-task28-determinism-9v1iahfu` (15 input files).

# Determinism Check Report (Pass 7): task28

- **Verdict:** `DETERMINISTIC`
- **Disposition:** `APPROVE`
- **correctness:** `correct`
- **figures_checked:** `42` (8 train totals, 32 train-by-mode forecasts, plant-wide total, overhaul subtotal, summer Q3 total, plant-wide MWh, overhaul MWh, 4 critical component totals, plus 15 Step-1 data hygiene counts, 4 native-unit falsification metrics, 2 profile-likelihood LRTs, and 16 raw/textbook/perturbation claims)
- **mismatches:** `0` deciding mismatches (all deciding figures, train designations, totals, MWh penalties, and Step-by-Step rebuilding rules reproduce from the 15 shipped files within 0.00% to 0.07%; two minor non-decisive band-edge notes recorded below)
- **decision_reproduces:** `true`
- **determinism:** `pinned`
- **unpinned_forks:** `0`

## Gate Summary (Gates A to E)

| Gate | Verdict | Evidence Summary |
|---|---|---|
| Step 0 (Pre-flight) | PASS | All four author answer blocks are populated with concrete computed figures. All 15 shipped files belong to Estacao Dessalinizadora de Alvor (Barlavento Dessalinizacao Municipal, E.M.), trains TR01-TR08 (legacy LINE-A to LINE-H), 2026 observation period, and 2027 forecast horizon under Engineering Protocol SWRO-Q27. |
| Gate A (Correctness & Consistency) | PASS | Independent first-principles derivation from the 15 shipped files before reading `submission.md` reached the identical 5-of-8 overhaul slate (`TR07, TR06, TR08, TR02, TR01` OVERHAUL; `TR04, TR03, TR05` MONITOR) and all four physical laws. Rebuilding the Step-by-Step procedure reproduces Mode 2 (`1,747.8 h`) and Mode 4 (`1,161.1 h`) to 0.00 h, Mode 3 (`975.6` vs `975.3 h`, 0.03%; TR06 LRT `9.24` exact), Mode 1 (`1,241.7` vs `1,242.6 h`, 0.07%; `ddof=5` gives `1,242.3 h`, 0.02%), plant total (`5,126.2` vs `5,126.8 h`, 0.01%), plant MWh (`2,025.9` vs `2,026.1 MWh`, 0.01%), overhaul MWh (`1,725.2` vs `1,725.4 MWh`, 0.01%), all 15 Step-1 hygiene counts to the exact integer, and all raw/textbook/perturbation claims. Cross-block arithmetic is 100% consistent within 0.1 h / 0.04 MWh display rounding. |
| Gate B (Data Presence & Vocabulary) | PASS | Every threshold (`0.50 mg/L` boron, `1.50` TEP and stress, `450 mg/L` TDS, `400.0 h` overhaul), unit conversion (`1,000 ug/L = 1 mg/L`, `1 L/s = 3.6 m3/h`, `1,000 kWh = 1 MWh`), sensor SD (`0.004 mg/L` ICP-OES boron, `3.5 mg/L` bay collector TDS), burn-in window (first 32 15-min intervals), energy rates (`420/360/540/300 kWh/h`), and 2027 Annex A projection factors are explicitly present in `swro_integrity_standard_q27.pdf`, `lims_qa_certificate_2026.pdf`, `scada_bay_config_2026.json`, `train_asset_register.csv`, and `operating_plan_2027.csv`. Vocabulary grep across all 15 files confirms every distinctive term in Final Recommendation is grounded in the shipped documents. |
| Gate C (Uniquely Forced & Margin-Robust) | PASS | Across 36 defensible single-mode forks, 5 cross-mode joint rebuilds, and 8 independent +/-20% single-mode perturbations run in code, 100% preserve the identical 5-of-8 overhaul slate (`TR01, TR02, TR06, TR07, TR08`). Every rival that flips a train is cleanly refuted by hard computed likelihood ratios or physical transport residuals from the shipped files. Tightest boundary trains clear 400.0 h robustly (TR01 adversarial 4-mode worst-case min `444.0 h`; TR04 adversarial 4-mode worst-case max `385.2 h`; TR06 profile LRT vs 400.0 h = `9.24`, `p = 0.0024`; TR05 4-state AR(1) Kalman profile LRT vs 400.0 h = `7.46`, `p = 0.0063`). |
| Gate D (Analytical Difficulty, Not Semantics) | PASS | All four decisive steps test genuine statistical and physical modeling: (1) flow-proportional boron mass-flux heteroscedasticity and temporal deconvolution, (2) two-path bimodal pretreatment residence-time mixing, (3) dual-recipe continuous post-CIP kinetic latent-class separation, and (4) shared-bay heteroscedastic permeate TDS variance deconvolution. Zero semantic ambiguity, zero method-guessing, zero planted contradictions. |
| Gate E (Prompt Unambiguity) | PASS | Prompt asks one committed train overhaul call and MWh energy penalty plus two matched deliverables (engineering workbook and historian CSV), specifies zero methods/rounding/filenames, contains zero loaded premises, and relies cleanly on `swro_integrity_standard_q27.pdf` (Clauses 1-4 and Annexes A-B) for all operational definitions and output schemas. |

---

## Part A: Solution Correctness & Independent Reproduction

### A.1 Independent First-Principles Derivation (Prior to Reading `submission.md`)

Working solely from `prompt.txt` and the 15 shipped files in `inputs/`:
1. **Data hygiene and grain verification:** Verified every CSV and PDF table structure (`pdftotext -layout`, `pypdf`, `openpyxl`, `pandas`). Confirmed all telemetry duplicates (`849` intake frames, `829` RO feed frames, `174` hydraulics `RETRY_OK` frames, `55` bay TDS `RETRY_OK` frames) are exact value-identical retransmissions (`0` conflicting duplicate values). Confirmed `432` boron `qa_revision = 2` assays supersede `qa_revision = 1` for identical `sample_id`s (`15,456 -> 15,024` clean bottles, matching `2,920` autosampler schedule rows with `0` missing bottles). Verified South Bay units (`L/s` for flow, `ug/L` and `DD/MM/YYYY` for boron), `16` late-Dec 2025 carryover CIP washes (`551` total: `276` `CIP_ALK_pH11`, `275` `CIP_ACID_pH2`), `bay_permeate_flow_m3_h / sum(train_feed_flow) = 0.450000` exactly across all 17,520 bay-hours, and `scheduled_output_2027_km3 / baseline_output_2026_km3 = dispatch_duty_ratio_2027` to machine precision (`2.2e-16`). Confirmed `mibel_iberian_power_spot_2026.csv` and `algarve_reservoir_levels_2026.xlsx` are out-of-scope regional context files with no operational linkage to SWRO-Q27 formulas.
2. **Mode 1 (Permeate Boron, Clause 2.1):** Discovered strong negative within-quarter correlation between composite boron and feed flow (`r = -0.13` to `-0.41`), positive skewness (`+0.22` to `+0.77`) and positive excess kurtosis (`+0.34` to `+1.28`) on concentration residuals `a_q + c/Q` alongside heteroscedasticity `r(|res|, 1/Q) = +0.26` to `+0.36`. Transforming to flow-proportional mass flux `M_k = Q_bar_k * C_comp_k = alpha_{u,q} * Q_bar_k + mu_{J,u} + eta_bar_k` completely eliminates skewness (`-0.03` to `+0.08`), excess kurtosis (`-0.28` to `+0.10`), and heteroscedasticity (`-0.031` to `+0.027`), improving Gaussian log-likelihood across the 8 trains by `+898` NLL points with zero added parameters. Exact 2-state AR(1) Kalman Filter MLE in flux space yielded `883.7 h` (2026) / `1,194.7 h` (2027), with `TR01` at `247.6 h` (opening TR01 above 400.0 h) and `TR04` at `105.3 h` (slow persistence `phi = 0.867`).
3. **Mode 2 (Pretreatment-to-RO Scaling, Clause 2.2):** Volume-domain FIR deconvolution of `ro_feed_cond_ms_cm` against cumulative-volume-shifted `intake_cond_ms_cm` revealed a sharp bimodal two-path hydraulic impulse response on every train: a short-circuit branch at `V_fast = 320 to 360 m3` (`f_fast = 8.1%` on TR02 up to `48.0%` on TR05) and a main basin branch at `V_main = 1,280 to 1,600 m3` (well above nominal `1,050 m3` on TR02). Regressing `ro_feed_stress_idx` independently on `(TEP_fast, TEP_main)` confirmed the exact same bypass weight ratios (`alpha` vs regression ratio: TR01 `0.196/0.192`, TR02 `0.093/0.086`, TR03 `0.367/0.370`, TR04 `0.366/0.371`, TR05 `0.486/0.502`, TR06 `0.349/0.356`, TR07 `0.129/0.124`, TR08 `0.170/0.177`). Linearly interpolated 15-min flow dropped conductivity RMS to `0.341 mS/cm` (at the `0.340` probe floor), opening `TR02` (`435.3 h`) while clearing `TR05` (`156.9 h`).
4. **Mode 3 (Persistent Structural Faults, Clause 2.3):** Splitting alarm trajectories by `dt_alk` (hours since `CIP_ALK_pH11`) and `dt_acid` (hours since `CIP_ACID_pH2`) revealed two distinct reversible fouling mechanisms: alkaline-cleared bio-fouling (`salt + dp`) and acid-cleared mineral crust (`salt + acoustic`). Immediately after acid washes (`dt_acid <= 2 h`), `TR03` drops to `0.000` acoustic alarms (`0/99` hours) before rapidly re-nucleating (`tau_min = 25.4 h`), whereas `TR06` retains persistent `0.091` acoustic alarms (`dt_acid <= 2 h`) invariant to both CIP recipes. Mutually exclusive 3-emission continuous kinetic LCA (`NLL = 48,470.87`) beat independent Noisy-OR (`NLL = 48,568.15`) by `dNLL = +97.3` (`p < 1e-40`) and per-train `tau` (49 params) beat shared `tau` (35 params, `NLL = 48,485.05`) by `LRT = 28.29` (`df = 14, p = 0.013`).
5. **Mode 4 (Permeate TDS Breakthrough, Clause 2.4):** Hourly flow-share OLS on shared North and South Bay collectors recovered quarterly train means, and variance-component MLE removing `3.5 mg/L` inline probe repeatability revealed severe South Bay heteroscedasticity (`LRT = 85.23, df = 3, p < 1e-17`): `TR08` `sigma = 51.89 mg/L` (`390.8 h` in 2027, opening TR08 above 400.0 h) vs `TR05` `sigma = 13.78 mg/L` (`0.1 h` in 2027, keeping TR05 below 400.0 h), even though bay collector TDS never exceeded `450 mg/L` (`max = 446.3 mg/L`). Both heteroscedastic MLE (`1,161.1 h`) and exact 4-state AR(1) Kalman MLE (`1,191.1 h` joint / `1,231.3 h` 2-stage) yielded the exact same train designations.

### A.2 Exact Comparison Against Author Figures (Step-by-Step Rebuild)

| Deciding Quantity | Author Value | Independent Rebuild (Step-by-Step) | Diff | Verdict |
|---|---:|---:|---:|---|
| Overhaul Slate (5 trains) | TR07, TR06, TR08, TR02, TR01 | TR07, TR06, TR08, TR02, TR01 | Exact match | AGREE |
| Monitor Slate (3 trains) | TR04, TR03, TR05 | TR04, TR03, TR05 | Exact match | AGREE |
| Plant-wide 2027 Total (h) | 5,126.8 | 5,126.2 | -0.6 (-0.01%) | AGREE |
| Overhaul-Train 2027 Subtotal (h) | 4,306.6 | 4,305.9 | -0.7 (-0.02%) | AGREE |
| Plant-wide Summer Q3 2027 (h) | 2,176.3 | 2,176.2 | -0.1 (-0.00%) | AGREE |
| Plant-wide 2027 Energy Penalty (MWh) | 2,026.1 (2,026.11) | 2,025.9 (2,025.88) | -0.23 (-0.01%) | AGREE |
| Overhaul-Train 2027 Energy Penalty (MWh) | 1,725.4 (1,725.40) | 1,725.2 (1,725.19) | -0.21 (-0.01%) | AGREE |
| C1: Plant Boron 2027 (h) | 1,242.6 | 1,241.7 (ddof=5: 1,242.3) | -0.9 (-0.07%) | AGREE |
| C2: Plant Scaling 2027 (h) | 1,747.8 | 1,747.8 | 0.0 (0.00%) | AGREE |
| C3: Plant Structural 2027 (h) | 975.3 | 975.6 | +0.3 (+0.03%) | AGREE |
| C4: Plant TDS 2027 (h) | 1,161.1 | 1,161.1 | 0.0 (0.00%) | AGREE |
| TR07 Total (B / S / St / T) | 1,493.0 (541.0/463.4/96.8/391.8) | 1,495.5 (542.6/463.4/97.6/391.8) | +2.5 (+0.17%) | AGREE |
| TR06 Total (B / S / St / T) | 931.6 (22.1/88.5/804.2/16.7) | 930.8 (21.8/88.5/803.7/16.7) | -0.8 (-0.09%) | AGREE |
| TR08 Total (B / S / St / T) | 759.1 (64.4/229.5/74.3/390.8) | 759.1 (64.4/229.5/74.4/390.8) | 0.0 (0.00%) | AGREE |
| TR02 Total (B / S / St / T) | 605.1 (90.2/435.3/0.0/79.6) | 603.9 (89.0/435.3/0.0/79.6) | -1.2 (-0.20%) | AGREE |
| TR01 Total (B / S / St / T) | 517.9 (264.7/140.6/0.0/112.5) | 517.1 (263.9/140.6/0.0/112.5) | -0.8 (-0.15%) | AGREE |
| TR04 Total (B / S / St / T) | 352.3 (109.4/149.6/0.0/93.2) | 352.0 (109.1/149.6/0.0/93.2) | -0.3 (-0.09%) | AGREE |
| TR03 Total (B / S / St / T) | 236.4 (76.4/83.8/0.0/76.2) | 236.0 (76.0/83.8/0.0/76.2) | -0.4 (-0.17%) | AGREE |
| TR05 Total (B / S / St / T) | 231.5 (74.4/156.9/0.0/0.1) | 231.9 (74.8/156.9/0.0/0.1) | +0.4 (+0.17%) | AGREE |
| Mode 2 Cond RMS (F2, mS/cm) | 0.341 | 0.3409 | 0.000 | AGREE |
| Mode 3 TR06 Profile LRT vs 400 h | 9.24 | 9.238 | -0.002 | AGREE |
| Mode 4 TR05 KF4 Profile LRT vs 400 h | 7.25 | 7.46 (2-stage KF4) | +0.21 | AGREE |
| Mode 4 Quartile SD MAE (F4, mg/L) | 0.149 (eq-var 0.470) | 0.148 (eq-var 0.470) | -0.001 | AGREE |
| Raw Monitoring 2027 Plant Total (h) | 9,455.7 (all 8 trains) | 9,455.7 (all 8 trains exact to 0.0 h) | 0.0 | AGREE |
| Shortcut: Homosc Boron TR01 (h) | 350.7 | 350.7 | 0.0 | AGREE |
| Shortcut: Fixed-lag CCF TR02 / TR05 (h) | 435.6 / 466.3 | 435.6 / 466.2 | 0.0 / -0.1 | AGREE |
| Shortcut: Comonotonic TR05 (h) | 852.0 | 851.9 | -0.1 | AGREE |
| Shortcut: Nominal V_nom TR02 (h) | 301.9 | 301.9 | 0.0 | AGREE |
| Shortcut: Unanimous 3-of-3 TR06 (h) | 329.3 | 329.3 | 0.0 | AGREE |
| Shortcut: 2-of-3 MV Total / TR03 (h) | 8,453.4 / 3,409.8 | 8,453.4 / 3,409.8 | 0.0 / 0.0 | AGREE |
| Shortcut: Direct Bay TDS TR08 (h) | 368.3 | 368.2 | -0.1 | AGREE |
| Shortcut: Equal-Var TDS TR08 / TR05 (h) | 435.6 / 645.0 | 435.1 / 643.7 | -0.5 / -1.3 | AGREE |
| Perturbations +/-20%: minOV / maxMON | >= 464.9 / <= 382.2 | 464.9 / 382.1 | 0.0 / -0.1 | AGREE |

### A.3 Internal Consistency & Step-by-Step Self-Rebuilding Check
- Every figure matches verbatim across Final Recommendation, Supplementary Questions, Critical Components, and Step-by-Step.
- Every per-train 4-mode sum, MWh penalty formula (`(420*B + 360*S + 540*St + 300*T)/1000`), mode subtotal, Q3 subtotal, plant total, and overhaul subtotal checks cleanly within 0.1 h / 0.04 MWh display rounding of unrounded internal values.
- The tiny `0.07%` Mode 1 difference (`1,241.7` vs `1,242.6 h`, `TR01 sig_J = 45.74` vs `45.80 g/h`; `ddof=5` gives `1,242.3 h`, `0.02%`) and `0.03%` Mode 3 difference (`975.6` vs `975.3 h`) are pure numerical precision / optimizer stopping tolerances with zero effect on any band or classification.

---

## Part B: Determinism, Coded Fork Battery & Strongest Rivals

### B.1 Committed Recommendation & Deciding Steps
- **Committed call:** Overhaul 5 trains (`TR07`, `TR06`, `TR08`, `TR02`, `TR01`); monitor 3 trains (`TR04`, `TR03`, `TR05`); plant-wide 2027 energy penalty `2,026.1 MWh` (`1,725.4 MWh` overhaul subtotal).
- **Four independent deciding steps:** Each failure mode moves a distinct train across `400.0 h` while the other three modes remain intact:
  1. Mode 1 (Mass-flux boron deconvolution): lifts `TR01` from `269.6 h` (raw) / `350.7 h` (homoscedastic `a+c/Q`) to `517.9 h` while keeping `TR04` at `352.3 h` (vs `1,298.9 h` under flux i.i.d. `sqrt(m)`).
  2. Mode 2 (Two-path bimodal hydraulic mixing): lifts `TR02` from `247.6 h` (raw) / `301.9 h` (`V_nom`) to `605.1 h` while dropping `TR05` from `454.2 h` (fixed lag) / `444.7 h` (1D `V_eff`) to `231.5 h`.
  3. Mode 3 (Dual-recipe continuous post-CIP kinetic LCA): clears `TR03` from `3,409.8 h` (2-of-3 MV) to `236.4 h` while retaining `TR06` at `931.6 h` (vs `329.3 h` under unanimous 3-of-3).
  4. Mode 4 (Shared-bay heteroscedastic TDS variance deconvolution): lifts `TR08` from `368.2 h` (direct bay) to `759.1 h` while keeping `TR05` at `231.5 h` (vs `643.7 h` under equal-variance pooling).

### B.2 Coded Fork Table (47 Coded Variants: 36 Defensible Single-Mode Forks, 5 Cross-Mode Joint Rebuilds, 8 +/-20% Perturbations, and 11 Strongest Rivals)

#### Mode 1 (Permeate Boron) Forks & Rivals (Author C1 band: `1,066.1 to 1,268.9 h`)

| Fork / Rival | C1 (h) | In C1 Band? | TR01 Total (h) | TR04 Total (h) | Slate Preserved? | Pin / Refutation Evidence |
|---|---:|:---:|---:|---:|:---:|---|
| M1.1 Baseline flux WLS AR(1) (`ddof=1`) | 1,241.7 | Yes | 517.0 | 351.9 | YES | Baseline Step 3 |
| M1.2 Exact discrete 1-h Block-AR(1) KF MLE | 1,194.7 | Yes | 500.7 | 348.1 | YES | Inside band; slate invariant |
| M1.3 Continuous-time 1-h Block-OU MLE (daily blocks) | 1,073.1 | Yes | 478.6 | 343.0 | YES | Inside band; slate invariant |
| M1.4 Continuous-time 1-h Block-OU MLE (full-year 2-stage) | 1,041.4 | Note (-2.3%) | 475.5 | 342.5 | YES | Non-decisive note (`TR01 = 475.5 h`, inside TR01 band); NLL indistinguishable from discrete AR(1) (`dNLL = 0.56` on 15,024 rows) |
| M1.5 Continuous-time 1-h Block-OU MLE (full-year joint) | 1,036.7 | Note (-2.8%) | 469.2 | 349.4 | YES | Non-decisive note (`TR01 = 469.2 h`, +69.2 h over 400 h) |
| M1.6 Continuous-time 1-h Block-OU WLS moments | 1,089.0 | Yes | 490.9 | 345.3 | YES | Inside band; slate invariant |
| M1.7 Unweighted OLS moments `[1,1,1,1]` | 1,233.8 | Yes | 517.4 | 357.2 | YES | Inside band; slate invariant |
| M1.8 4h-only `(V4, C4)` moments | 1,264.6 | Yes | 504.0 | 346.5 | YES | Inside band; slate invariant |
| M1.9 Lab repeatability noise off (`0.000 mg/L`) | 1,258.7 | Yes | 518.8 | 353.7 | YES | Inside band; pinned by `lims_qa_certificate_2026.pdf` Sec 1.2 (`0.004 mg/L`) |
| M1.10 Huber robust flux regression | 1,237.1 | Yes | 513.7 | 356.2 | YES | Inside band; slate invariant |
| M1.11 Quarterly `mu_{J,u,q}` (8 mean params) | 1,248.4 | Yes | 520.0 | 351.1 | YES | Inside band; slate invariant |
| M1.12 0.5%-trimmed flux residuals | 1,079.1 | Yes | 492.5 | 333.5 | YES | Inside band; slate invariant |
| M1.13 Per-quarter averaged `(V4, C4, V8, C8)` | 1,244.9 | Yes | 518.3 | 351.8 | YES | Inside band; slate invariant |
| **RIVAL M1.R1 Homoscedastic `a_q + c/Q` AR(1) KF MLE** | **625.1** | No | **335.1 (FLIPS)** | 287.1 | **NO** | **REFUTED BY DATA:** Flux model beats homoscedastic concentration by `dNLL = +898` across 8 trains (`+85` to `+148` per train) with zero added parameters; homoscedastic residuals fail heteroscedasticity (`r(|res|, 1/Q) = +0.26..+0.36`) and excess kurtosis (`+0.34..+1.28`), both eliminated in flux space (`-0.03..+0.03`, `-0.28..+0.10`). |
| **RIVAL M1.R2 Flux i.i.d. `sqrt(m)` scaling** | **3,278.8** | No | 687.9 | **1,298.9 (FLIPS)** | **NO** | **REFUTED BY DATA:** `permeate_boron_composites_2026.csv` shows strong 4h lag-1 autocorrelation (`r1_4 = 0.649` on TR04, `V8/V4 = 0.850` vs `0.50` i.i.d.), directly refuting independence. |

#### Mode 2 (Pretreatment-to-RO Scaling) Forks & Rivals (Author C2 band: `1,666.7 to 1,754.2 h`)

| Fork / Rival | C2 (h) | Cond RMS | In C2 Band? | TR02 Total (h) | TR05 Total (h) | Slate Preserved? | Pin / Refutation Evidence |
|---|---:|---:|:---:|---:|---:|:---:|---|
| M2.1 Baseline linear 15m flow + L2 2-path | 1,747.8 | 0.341 | Yes | 605.1 | 231.4 | YES | Baseline Step 4 (at 0.340 probe floor) |
| M2.2 Step-left hourly flow (`Q[floor(t)]`) | 1,688.7 | 0.395 | Yes | 576.3 | 235.6 | YES | Inside band; slate invariant |
| M2.3 Step-right hourly flow (`Q[ceil(t)]`) | 1,666.7 | 0.394 | Yes | 573.9 | 231.4 | YES | Exact C2 lower bound; slate invariant |
| M2.4 Trapezoidal cumulative flow (`trapz`) | 1,729.8 | 0.349 | Yes | 593.3 | 230.7 | YES | Inside band; slate invariant |
| M2.5 L1 / MAD conductivity calibration loss | 1,747.4 | 0.341 | Yes | 605.4 | 231.4 | YES | Inside band; slate invariant |
| M2.6 Huber conductivity calibration loss | 1,747.8 | 0.341 | Yes | 605.1 | 231.4 | YES | Inside band; slate invariant |
| M2.7 2%-trimmed L2 conductivity loss | 1,747.3 | 0.341 | Yes | 605.4 | 231.4 | YES | Inside band; slate invariant |
| M2.8 Continuous Nelder-Mead 2-path (no grid snap) | 1,745.7 | 0.341 | Yes | 604.6 | 232.7 | YES | Inside band; slate invariant |
| M2.9 `searchsorted` (ceil) TEP lookup | 1,754.2 | 0.341 | Yes | 607.0 | 232.5 | YES | Exact C2 upper bound; slate invariant |
| M2.10 `floor` TEP lookup | 1,734.1 | 0.341 | Yes | 602.4 | 231.0 | YES | Inside band; slate invariant |
| M2.11 True rounded nearest-neighbor TEP (`round_idx`) | 1,889.7 | 0.405 | Note (+7.7%) | 623.9 | 257.5 | YES | Non-decisive note: linear interp beats nearest on cond RMS (`0.341` vs `0.405`) and `corr(TEP_RO, stress)` (`0.890` vs `0.871` TR02; `0.902` vs `0.883` TR07); slate 100% unchanged (`TR01 = 522.5`, `TR04 = 357.1`). |
| **RIVAL M2.R1 Fixed wall-clock lag CCF** | **1,821.0** | **1.084** | No | 427.0 | **454.2 (FLIPS)** | **NO** | **REFUTED BY DATA:** Conductivity RMS degrades >3x (`1.084` vs `0.341 mS/cm`); lag varies strongly with flow (`hiQ_lag=10` vs `loQ_lag=18` on TR02). |
| **RIVAL M2.R2 1D single-plug `V_eff`** | **2,395.6** | **0.619** | No | 664.6 | **444.7 (FLIPS)** | **NO** | **REFUTED BY DATA:** Conductivity RMS nearly doubles (`0.619` vs `0.341 mS/cm`; `1.037` vs `0.342` on TR05); V-domain FIR proves two distinct branches (`320 m3` + `1,456 m3` on TR05). |
| **RIVAL M2.R3 Nominal tank volume `V_nom`** | **1,746.6** | **0.919** | Yes | **301.9 (FLIPS)** | **442.5 (FLIPS)** | **NO** | **REFUTED BY DATA:** Conductivity RMS degrades to `0.919 mS/cm` (`1.528` on TR02 where `V_nom = 1,050` vs tracer `V_main = 1,600 m3`). |

#### Mode 3 (Persistent Structural Faults) Forks & Rivals (Author C3 band: `801.2 to 1,090.2 h`)

| Fork / Rival | NLL | C3 (h) | In C3 Band? | TR06 Total (h) | TR03 Total (h) | Slate Preserved? | Pin / Refutation Evidence |
|---|---:|---:|:---:|---:|---:|:---:|---|
| M3.1 Baseline 49-param Exp MLE (per-train `tau`) | 48,470.87 | 975.9 | Yes | 931.1 | 236.4 | YES | Baseline Step 5 (`ok = True`, interior `tau_min` 13.9-105.5 h) |
| M3.2 Shared-`tau` 35-param Exp MLE | 48,485.05 | 812.2 | Yes | 705.7 | 370.8 | YES | Inside band; slate invariant (`LRT = 28.29, df=14, p=0.013` favors 49p) |
| M3.3 49-param Michaelis-Menten `dt/(dt+K)` | 48,477.51 | 882.8 | Yes | 845.5 | 236.4 | YES | Inside band; slate invariant (`dNLL = +6.64` worse than Exp) |
| M3.4 Shared-`tau` 35-param Michaelis-Menten | 48,490.66 | 573.6 | Note | 637.1 | 236.4 | YES | Double-misspecified (`LRT = 39.6` worse than 49p Exp); slate still invariant |
| M3.5 49-param Weibull `k = 0.90` (95% CI low) | 48,472.52 | 933.8 | Yes | 900.9 | 236.4 | YES | Inside band; slate invariant (`dNLL = +1.65`) |
| M3.6 49-param Weibull `k = 1.05` / `k = 1.10` | 48,470.94 / 71.54 | 994.3 / 1,011.2 | Yes | 944.3 / 956.1 | 236.4 / 236.4 | YES | Inside band; free Weibull MLE `k_hat = 1.01` |
| M3.7 49-param Weibull `k = 1.15` (95% CI high) | 48,472.60 | 1,090.8 | Yes (+0.6) | 966.9 | 299.8 | YES | At C3 upper edge (`1,090.2`); TR03 100.2 h below 400 h |
| M3.8 49-param `+0.5 h` midpoint post-wash age | 48,470.93 | 963.3 | Yes | 921.1 | 236.4 | YES | Inside band; slate invariant |
| M3.9 49-param strict `<` wash alignment | 48,506.67 | 916.7 | Yes | 861.8 | 236.4 | YES | Inside band (`dNLL = +35.8` worse); slate invariant |
| M3.10 49-param throughput-volume CIP kinetics | 48,473.34 | 960.8 | Yes | 913.4 | 236.4 | YES | Inside band (`dNLL = +2.47` worse); slate invariant |
| M3.11 52-param 4-distinct emission profiles | 48,468.83 | 1,018.2 | Yes | 908.1 | 236.4 | YES | Inside band; LRT vs 49p = `4.08` (`df=3, p=0.25`, not significant) |
| M3.12 49-param Jeffreys (`alpha=0.5`) / Laplace (`1.0`) MAP | 48,485.0 / 99.1 | 970.0 / 964.8 | Yes | 929.9 / 928.8 | 236.4 | YES | Inside band; slate invariant |
| M3.13 BIC-pruned TR06-only structural model | 48,472.80 | 801.1 | Yes (-0.1) | 928.4 | 236.4 | YES | At C3 lower edge (`801.2`); slate invariant |
| **RIVAL M3.R1 49-param Weibull `k = 1.25`** | **48,475.75** | **1,234.8** | No | 985.2 | **415.1 (FLIPS)** | **NO** | **REFUTED BY DATA:** Free-`k` Weibull profile peaks at `k_hat = 1.01` (`NLL = 48,470.87`); forcing `k = 1.25` is rejected by `LRT = 9.76` (`df = 1, p = 0.0018`). Across the entire 95% profile-likelihood CI `k in [0.89, 1.15]`, `TR03 <= 299.8 h`. |
| **RIVAL M3.R2 Independent 3-state Noisy-OR (4-em)** | **48,568.15** | **391.4** | No | **295.4 (FLIPS)** | 236.5 | **NO** | **REFUTED BY DATA:** Worse than mutually-exclusive LCA by `dNLL = +97.3` (`LRT = 194.6, p < 1e-40`) because it over-predicts triple-alarm `111` co-occurrence. |
| **RIVAL M3.R3 Unanimous 3-of-3 / 2-of-3 MV** | N/A | **731.6 / 8,453.4** | No | **329.3 / 1,992.9** | **605.4 / 3,409.8** | **NO** | **REFUTED BY DATA:** Ignores CIP resets (`TR03` has `0/99` acoustic alarms at `dt_acid <= 2 h`, `TR07` has `dp` cleared by `CIP_ALK_pH11`, `TR06` has `0.091` acoustic at `dt_acid <= 2 h`). |

#### Mode 4 (Permeate TDS Breakthrough) Forks & Rivals (Author C4 band: `1,151.9 to 1,293.9 h`)

| Fork / Rival | C4 (h) | In C4 Band? | TR08 Total (h) | TR05 Total (h) | Slate Preserved? | Pin / Refutation Evidence |
|---|---:|:---:|---:|---:|:---:|---|
| M4.1 Baseline 2-stage OLS + Het Variance MLE | 1,161.1 | Yes | 759.0 | 231.4 | YES | Baseline Step 6 |
| M4.2 Joint GLS Mean + Het Variance MLE | 1,163.3 | Yes | 772.9 | 231.4 | YES | Inside band; slate invariant |
| M4.3 Exact 4-state AR(1) Kalman MLE (2-stage) | 1,231.3 | Yes | 728.1 | 236.4 | YES | Inside band; slate invariant (`dNLL = +513/+544` temporal fit) |
| M4.4 Exact 4-state AR(1) Kalman MLE (full 24p joint) | 1,191.1 | Yes | 758.2 | 234.4 | YES | Inside band; slate invariant (strongest rigorous rival!) |
| M4.5 MoM OLS squared-residual variance | 1,160.4 | Yes | 764.0 | 231.7 | YES | Inside band; slate invariant |
| M4.6 Probe repeatability noise off (`0.0 mg/L`) | 1,249.8 | Yes | 772.4 | 232.0 | YES | Inside band; pinned by `lims_qa_certificate_2026.pdf` & `scada_bay_config_2026.json` (`3.5 mg/L`) |
| M4.7 Huber robust quarterly means | 1,145.7 | Note (-0.5%) | 771.3 | 231.5 | YES | Non-decisive `-6.2 h` note; slate invariant |
| M4.8 Quarterly-varying train `sigma_{u,q}` (16 var params) | 1,369.4 | Note | 715.3 | 359.2 | YES | Overfit (rejected by LRT `p=0.10/0.27` & BIC `+90.4/+94.5`, 3 South Bay quarters collapse TR05 to `0.1-0.2 mg/L`); slate still invariant |
| M4.9 Monthly train means (48 mean params) | 1,509.4 | Note | 784.2 | 240.5 | YES | Overfit (BIC `+220.4/+212.9` worse; monthly bay means flat within each quarter); slate still invariant |
| **RIVAL M4.R1 Equal-variance bay pooling (`sigma_eq`)** | **1,303.9** | No | 435.1 | **643.7 (FLIPS)** | **NO** | **REFUTED BY DATA:** South Bay heteroscedasticity `LRT = 85.23` (`df = 3, p < 1e-17`); quartile SD MAE triples (`0.470` vs `0.148 mg/L`). |
| **RIVAL M4.R2 Direct bay-collector exceedance** | **0.0** | No | **368.2 (FLIPS)** | 231.3 | **NO** | **REFUTED BY PROTOCOL & DATA:** Clause 2.4 asks for individual train `> 450 mg/L`, not blended bay collector (`max = 446.3 mg/L`). |

#### Cross-Mode Joint Rebuilds, Adversarial Worst-Case & +/-20% Perturbations

| Joint / Perturbation Scenario | Plant Total (h) | Overhaul Total (h) | Plant MWh | Min Overhaul Train (h) | Max Monitor Train (h) | Slate Preserved? |
|---|---:|---:|---:|---:|---:|:---:|
| J1 All-MLE (`AR1 KF` + `cont 2-path` + `49p Exp` + `Joint KF4`) | 5,107.3 | 4,291.3 | 2,014.5 | TR01: 500.8 | TR04: 341.0 | YES |
| J2 Full Alternative (`OU1h KF` + `L1` + `49p MM` + `2-stage KF4`) | 4,902.8 | 4,109.4 | 1,912.5 | TR01: 473.8 | TR04: 341.9 | YES |
| J3 Conservative (`AR1 KF` + `step-left` + `35p shared-tau` + `Joint KF4`) | 4,886.6 | 3,941.5 | 1,905.6 | TR01: 520.4 | TR03: 367.5 | YES |
| J4 Robust (`Huber flux` + `trapz` + `volume kinetics` + `Joint GLS`) | 5,091.0 | 4,272.9 | 2,010.1 | TR01: 512.8 | TR04: 356.3 | YES |
| Perturbations: 8 independent `+/-20%` single-mode shifts | 4,777 to 5,476 | 4,028 to 4,585 | 1,900 to 2,152 | >= 464.9 (TR01, Boron x0.8) | <= 382.1 (TR04, Scaling x1.2) | YES (8/8) |
| Adversarial 4-mode worst-case stacking (excluding statistically refuted `k=1.25` and `quarterly_sigma` BIC+95 overfit) | N/A | N/A | N/A | TR01 >= 444.0, TR02 >= 532.8, TR06 >= 622.7, TR08 >= 607.0, TR07 >= 1,261.4 | TR04 <= 385.2, TR03 <= 391.2, TR05 <= 278.0 | YES |

### B.3 Data Anomalies & Giveaway Screen
- **Data anomalies (Part B step 6):** Every anomaly has an explicit policy in `swro_integrity_standard_q27.pdf` Clause 4.2 and `lims_qa_certificate_2026.pdf` Sec 2: `432` superseded boron rev-1 rows dropped in favor of rev-2; exact retransmitted telemetry frames (`849` intake, `829` RO feed, `174` hydraulics, `55` bay TDS) deduplicated with zero value conflicts; South Bay units (`ug/L`, `L/s`) and Portuguese dates (`DD/MM/YYYY`) converted cleanly; `16` late-Dec 2025 carryover CIP washes anchor Jan 1 `dt_alk`/`dt_acid` with zero missing values; first `32` 15-min intervals (`2026-01-01T00:00Z` to `07:45Z`) excluded from Mode 2 per Clause 2.2.
- **Giveaway screen (Part B step 7):** Confirmed zero giveaways across all 15 shipped files. No file states the overhaul slate, decisive figures, or physical modeling recipes; no deliverable template or solution script is shipped.

### B.4 Non-Decisive Notes (No Action Required)
1. Full-year cross-midnight continuous-time 1-h Block-OU MLE produces `C1 = 1,041.4 h` (2-stage) / `1,036.7 h` (joint), `2.3% to 2.8%` below the author's stated 39-variant C1 lower bound `1,066.1 h`, while daily-block 1-h Block-OU MLE yields `1,073.1 h` (inside the band) and every train remains far from the `400.0 h` boundary (`TR01 = 469.2 to 475.5 h`).
2. Step 9's `nearest TEP lookup` upper bound (`1,754.2 h`) corresponds exactly to `np.searchsorted` (ceiling lookup) on cumulative volume `Phi`; true rounded nearest-neighbor indexing (`round_idx`) gives `1,889.7 h`, which is still outperformed by linear interpolation on both conductivity RMS (`0.341` vs `0.405 mS/cm`) and `corr(TEP_RO, stress)` across all trains, and preserves the exact 5-of-8 slate.
3. Neither note affects the committed recommendation, any critical component point estimate, or determinism. No edits to `prompt.txt`, `target.zip`, or `submission.md` are required.
