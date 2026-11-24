Manifest MD5s: `prompt.txt=4b10b0cc7528dc0c3b63afbc52d99eae`, `target.zip=6581943c0876883531a9952acc403c5e`, `submission.md=e8a12e7787a2cf666bd8bbc8b94b8edf`

# Holistic Audit v4 Determinism Check Report (Pass 6): task28

**Verdict:** `NOT_DETERMINISTIC`
**Disposition:** `SEND_BACK`

```
correctness: minor_mismatch
figures_checked: 52
mismatches: 1
decision_reproduces: true
determinism: not_pinned
unpinned_forks: 1
```

---

## Executive Summary

Task 28 is a strong, physically grounded four-mode SWRO reliability diagnostic task whose core engineering findings, four physical mechanisms (Spiegler-Kedem solute mass-flux boron deconvolution, variable-flow bimodal DAF/DMF pretreatment mixing, continuous post-CIP kinetic latent-class structural fault separation, and shared-bay permeate TDS variance-component deconvolution), raw monitoring contrasts, and 5-of-8 point overhaul slate (`TR07`, `TR06`, `TR08`, `TR02`, `TR01` = OVERHAUL; `TR04`, `TR05`, `TR03` = MONITOR) reproduce cleanly from the 15 shipped files.

However, independent coded verification and profile-likelihood identifiability testing uncovered **one Gate C (`margin_or_boundary_fragility`) failure on `TR05`** that requires a surgical pack/generator repair (`SEND_BACK`), alongside **one direct Part A Step 5 internal consistency contradiction in `submission.md`** and **band undercoverage on C1 and C4**:

1. **Gate C Failure (`margin_or_boundary_fragility` on `TR05`, S4 Bay TDS):**
   - South Bay collector residuals in `bay_permeate_tds_hourly_2026.csv` exhibit strong hourly AR(1) autocorrelation (`acf(1) = 0.3411`, `acf(2) = 0.1119`, `acf(3) = 0.0284`, `rho = 0.3535`, `LRT(rho > 0) > 1,000`). The author's golden S4 estimator treats the 8,760 hourly residuals as i.i.d. (`sigma_TR05 = 16.22 mg/L`, `TR05 TDS = 10.4 h`, `TR05 total = 326.7 h`).
   - Because `TR05` has the highest quarterly mean TDS in South Bay (`387.1 mg/L` annual; `405.0 mg/L` Q2; `399.0 mg/L` Q3, only 45 to 51 mg/L below the 450 mg/L breakthrough threshold) and contributes under 5% of South Bay residual variance while already carrying `316.2 h` of non-TDS hours (`159.3 h` boron + `156.9 h` scaling), `TR05` has only `83.8 h` of TDS headroom (`critical sigma_5 = 21.65 mg/L`).
   - **Gate C Condition (b) (statistical estimation noise straddles 400.0 h):** Profile-likelihood testing of `H0: TR05 >= 400.0 h` yields **`2*dNLL = 1.060` (`p = 0.303`, 95% CI `[316.2, 489.8 h]`) even under the author's own i.i.d. S4 MLE**, **`2*dNLL = 0.240` (`p = 0.624`) under GLS-Kalman exact 4-state AR(1) MLE**, and **`2*dNLL = 0.058` (`p = 0.810`, 95% CI `[316.2, ~615 h]`) under 2-stage exact 4-state AR(1) Kalman MLE** (where `TR05` already rises to `377.0 h`). By contrast, every other boundary train is cleanly statistically separated from 400.0 h (`TR01 LRT = 7.64, p = 0.0057`; `TR04 LRT = 28.94, p = 7.5e-8`; `TR06 LRT = 9.30, p = 0.0023`; `TR08 LRT = 61.66, p < 1e-14`).
   - **Gate C Condition (a) (defensible multi-stump combinations flip `TR05` to OVERHAUL):** While every single-stump defensible variant keeps `TR05 < 400.0 h` (peaking at `376.1 h` under author's 1-step AR(1) innovation MLE and `377.0 h` under 2-stage exact Kalman MLE), combining author-endorsed defensible variants from Step-by-Step #9 across stumps flips `TR05 >= 400.0 h` (6-of-8 slate): e.g., `S1 Exact Block-AR(1) MLE` (`167.6 h`) + `S2 Nearest TEP lookup` (`176.9 h`) + `S3 Exact Kinetic MLE` (`0.0 h`) + `S4 1-step AR(1) innov MLE` (`60.0 h`) = **`404.5 h`** (`405.3 h` with 2-stage exact Kalman MLE); `S1 4h-only WLS` (`183.8 h`) + `S2 golden` (`156.9 h`) + `S3 golden` (`0.0 h`) + `S4 1-step AR(1) innov MLE` (`60.0 h`) = **`400.7 h`** (`401.5 h` with 2-stage Kalman). Even the strictly top-tier linear-interpolation joint exact MLE (`S1 Block-AR(1) MLE + S2 Cont L2 + S3 Exact MLE + S4 2-stage Kalman MLE`) pushes `TR05` to **`386.2 h`** (13.8 h below 400.0 h, deep inside `LRT = 0.058` noise).
2. **Part A Step 5 Internal Consistency Contradiction in `submission.md`:**
   - `Supplementary Questions #1g` reports `TR05: 326.7 h total (uncertainty range 282.5 to 376.1 h)` (reproduced in code under `F4_AR1_innov_MLE`: `376.1 h`).
   - `Step-by-Step #9` contradicts this directly by stating: *"all 36 variants and all 8 perturbations preserve the exact 5-of-8 overhaul slate ..., keeping the lowest overhaul train at or above 424.0 h and **the highest monitor train at or below 362.2 h**."* Code confirms `424.0 h` (TR01 at -20% S1) and `362.2 h` (TR04 at +20% S2) cover only the 8 `+/-20%` perturbations, omitting that the 36-variant battery itself reaches `376.1 h` on `TR05`.
   - Similarly, the closing paragraph cites `TR04 (332.3 h, uncertainty range 313.3 to 339.6 h, 67.7 h below 400 h)` as the tightest MONITOR boundary clearance while ignoring `TR05`'s `376.1 h` upper uncertainty bound (only `23.9 h` below 400.0 h).
3. **Minor Band Undercoverage Against Gold-Standard Exact MLEs (C1 and C4):**
   - `S1 Exact Continuous-Time 1h-Block OU MLE` achieves slightly better log-likelihood than discrete 1h AR(1) MLE (`NLL = 54,128.16` vs `54,128.22`) and yields `C1 = 1,155.6 h` (`43.7 h` below author's `[1,199.3, 1,398.2]` band) and `TR01 = 427.8 h` (`25.1 h` below `[452.9, 499.8]`), while preserving the 5-of-8 slate.
   - `S4 Exact 2-Stage 4-State AR(1) Kalman MLE` yields `C4 = 1,258.9 h` (`13.5 h` above author's `[1,069.3, 1,245.4]` band), while `S4 GLS-Kalman Exact 4-State AR(1) MLE` yields `C4 = 1,192.0 h` (inside band).

---

## Step 0: Pre-Flight

1. **Golden present:** PASS. Final Recommendation, Supplementary Questions, Critical Components, and Step-by-Step Solution are complete and populated with explicit computed figures.
2. **Inputs belong to this task:** PASS. All 15 files under `inputs/` match Barlavento Dessalinizacao Municipal, E.M. (`Estacao Dessalinizadora de Alvor`), trains `TR01` through `TR08` (legacy `LINE-A` through `LINE-H`), calendar year 2026 observations, Engineering Protocol SWRO-Q27 (`BDM-ENG-Q27-2026`), LIMS QA Certificate (`LAB-QA-2026-B08`), and `operating_plan_2027.csv`.

---

## Part A: Solution Correctness

### A.1 Data Audit and Cleaning Verification

All 15 input files were audited programmatically (including PDF visual/OCR inspection of all pages and tables of `swro_integrity_standard_q27.pdf` and `lims_qa_certificate_2026.pdf`, JSON structure of `scada_bay_config_2026.json`, and full XLSX sheet inspection of `algarve_reservoir_levels_2026.xlsx`):

- `permeate_boron_composites_2026.csv`: 15,456 raw rows -> 15,024 unique `sample_id` bottles keeping `max(qa_revision)` (432 revision-1 rows superseded by revision-2; zero duplicate `(sample_id, qa_revision)` pairs; zero nulls; exact match to `autosampler_schedule_2026.csv` 2,920 train-days totaling 15,024 bottles). Note: `7,729` Portuguese `DD/MM/YYYY` dates and `7,729` `ug/L` rows are the **pre-deduplication** raw counts (post-deduplication clean counts are `7,512` each). `permeate_boron_composites_2026.csv` contains 16 readings `<= 0 mg/L` (min `-0.1551 mg/L`: 12 on TR01, 4 on TR08) and 30 readings `< 0.020 mg/L` LIMS LOQ (23 on TR01, 7 on TR08), tested as cleaning forks in Part B.
- `autosampler_schedule_2026.csv`: 2,920 rows (720 Q1 legacy tags `LINE-A..H`), 2,088 4h days (Thu-Mon, 6 bottles/day) and 832 8h days (Tue-Wed, 3 bottles/day). Summer correlation checks prove UTC alignment beats `Europe/Lisbon` alignment on all 8 trains (`corr(C, 1/Q)` strictly higher and flux residual SD strictly lower on UTC across `TR01..TR08`).
- `train_hydraulics_hourly_2026.csv`: 70,254 raw rows, 174 exact `RETRY_OK` duplicates (`max unique flow per (ts, train) = 1`), 70,080 clean hourly rows, 35,040 South-bay `L/s` readings converted via `3.6 m3/h per L/s`.
- `intake_chemistry_15m_2026.csv` and `ro_feed_header_15m_2026.csv`: 281,169 raw (849 exact retries dropped) and 281,149 raw (829 exact retries dropped) -> 280,320 clean 15-minute rows each (35,040 per train; first 32 burn-in intervals excluded per Clause 2.2).
- `bay_permeate_tds_hourly_2026.csv`: 17,575 raw rows, 55 exact `RETRY_OK` duplicates dropped -> 17,520 clean hourly rows (8,760 per bay; zero direct collector readings `> 450 mg/L`; `max |bay_permeate_flow - 0.45 * sum(feed_flow)| = 5.6e-5 m3/h`).
- `shift_diagnostics_2026.csv` and `cip_wash_log_2026.csv`: 70,080 hourly blocks and 551 washes (276 `CIP_ALK_pH11`, 275 `CIP_ACID_pH2`, 283 legacy tags, 16 late-Dec 2025 carryover washes giving 1 acid + 1 alk pre-2026 anchor per train), all with explicit UTC/Lisbon offsets.
- `operating_plan_2027.csv`: 32 train-quarter rows matching Annex A factors identically (`max |scheduled/baseline - dispatch_duty_ratio| = 2.2e-16`).
- Out-of-scope regional files: `mibel_iberian_power_spot_2026.csv` (8,760 hourly EUR/MWh prices) and `algarve_reservoir_levels_2026.xlsx` (single visible sheet `Weekly_Storage_2026`, 53 rows, zero hidden tabs or comments). Neither is referenced by Protocol SWRO-Q27.

### A.2 Independent First-Principles Derivation vs Author Values

Before implementing the author's specific WLS weights or discrete grid, all four modes were derived independently from first principles using exact maximum-likelihood / continuous physical estimators:
- **Independent Model A (Exact MLEs + i.i.d. S4):** S1 Exact Block-Averaged Discrete AR(1) Kalman MLE + S2 Continuous L2 2-Path Mixing (linear Q) + S3 Converged 49-Param Kinetic LCA MLE + S4 Heteroscedastic Gaussian MLE.
- **Independent Model B (All-4 Gold-Standard Exact MLEs incl. S4 AR(1) GLS-Kalman):** Same S1, S2, S3 + S4 GLS-Iterated Exact 4-State AR(1) Kalman MLE.
- **Step-by-Step Self-Rebuild:** Exact implementation of author's Step-by-Step recipes (S1 same-day WLS `[3/V4^2, 3/V4^2, 1/V8^2, 0.7/V8^2]`, S2 8 m3 discrete grid `[200,520]x[960,1600]` with `<0.04` snap, S3 exact converged 49-param analytic-gradient L-BFGS-B, S4 quarterly OLS + heteroscedastic MLE).

| Deciding Quantity | Indep. Model A (i.i.d. S4) | Indep. Model B (GLS-Kalman S4) | Step-by-Step Self-Rebuild | Author Point Value | Author 36-Var Band | Agreement |
|---|---|---|---|---|---|---|
| **Overhaul Slate (>= 400 h)** | TR07,TR06,TR08,TR02,TR01 | TR07,TR06,TR08,TR02,TR01 | TR07,TR06,TR08,TR02,TR01 | TR07,TR06,TR08,TR02,TR01 | Fixed 5-of-8 | Agree |
| **C1: Plant 2027 Boron (h)** | 1,321.6 | 1,321.6 | 1,375.2 | **1,375.5** | 1,199.3 to 1,398.2 | Agree (0.3 h) |
| **C2: Plant 2027 Scaling (h)** | 1,722.0 | 1,722.0 | 1,724.5 | **1,724.5** | 1,645.1 to 1,729.5 | Exact (0.0 h) |
| **C3: Plant 2027 Structural (h)** | 975.8 | 975.8 | 975.8 | **974.2** | 800.8 to 1,089.0 | Agree (1.6 h) |
| **C4: Plant 2027 TDS (h)** | 1,077.0 | 1,192.0 | 1,077.0 | **1,077.0** | 1,069.3 to 1,245.4 | Exact (0.0 h) |
| **Plant Total 2027 (h)** | 5,096.4 | 5,211.5 | 5,152.5 | **5,151.2** | 4,975.1 to 5,319.6 | Agree (1.3 h) |
| **Overhaul Subtotal 2027 (h)** | 4,191.4 | 4,292.5 | 4,257.1 | **4,255.8** | 4,082.4 to 4,387.9 | Agree (1.3 h) |
| **Summer Q3 2027 (h)** | 2,147.2 | 2,188.6 | 2,163.4 | **2,163.0** | 2,098.2 to 2,225.2 | Agree (0.4 h) |
| **Plant Energy Penalty (MWh)** | 2,026.7 | 2,061.2 | 2,048.4 | **2,047.72** | 1,954.1 to 2,109.7 | Agree (0.7 MWh) |
| **Overhaul Energy (MWh)** | 1,696.2 | 1,719.6 | 1,711.2 | **1,710.46** | 1,616.8 to 1,750.1 | Agree (0.7 MWh) |
| TR07 Total 2027 (h) | 1,467.6 | 1,564.1 | 1,495.0 | **1,491.6** | 1,392.1 to 1,673.5 | Agree (3.4 h) |
| TR06 Total 2027 (h) | 934.2 | 923.5 | 932.5 | **932.3** | 846.5 to 968.3 | Agree (0.2 h) |
| TR08 Total 2027 (h) | 738.5 | 732.4 | 745.9 | **745.9** | 671.6 to 759.1 | Exact (0.0 h) |
| TR02 Total 2027 (h) | 597.1 | 615.1 | 605.1 | **605.1** | 573.9 to 618.2 | Exact (0.0 h) |
| TR01 Total 2027 (h) | 454.1 | 457.4 | 480.0 | **480.9** | 452.9 to 499.8 | Agree (0.9 h) |
| TR04 Total 2027 (h) | 325.7 | 319.0 | 331.7 | **332.3** | 313.3 to 339.6 | Agree (0.6 h) |
| TR05 Total 2027 (h) | 335.8 | 369.4 | 326.7 | **326.7** | 282.5 to 376.1 | Exact (0.0 h) |
| TR03 Total 2027 (h) | 243.5 | 230.6 | 236.4 | **236.4** | 216.9 to 299.3 | Exact (0.0 h) |

### A.3 Verification of Raw Monitoring, Rivals, Falsification, and Internal Consistency

- **Raw monitoring claims (all verified exact to 0.0 h):** 2026 raw boron `108.0 h` (2027 `152.2 h`), same-time scaling `611.2 h` (2027 `845.6 h`), 2-of-3 shift MV `7,483.0 h` (2027 `8,453.4 h`), bay collector TDS `0.0 h`; per-train 2027 raw totals `TR01 191.5, TR02 241.7, TR03 3,216.2, TR04 429.4, TR05 993.5, TR06 1,910.6, TR07 2,129.7, TR08 338.6`, plant `9,451.2 h`. All 8 match author claims to 0.0 h.
- **Rival & ablation claims:**
  - S1 homoscedastic `a + c/Q` AR(1) drops TR01 to `351.1 h` (author `352.9 h`); flux i.i.d. `sqrt(m)` flips TR04 to `1,172.1 h` pooled / `1,052.6 h` 4h-basis.
  - S2 `V_nom` drops TR02 to `301.9 h` (exact); fixed lag CCF gives TR02 `435.6 h` (exact) and TR05 `561.4 h` (author `561.5 h`); 1D `V_eff` flips TR05 to `539.9 h` (author `537.8 h`); comonotonic flips TR05 to `947.1 h` (author `947.2 h`); conductivity RMS `same 1.857`, `lag_CCF 1.088`, `1D 0.619` vs `golden 0.341 mS/cm` (exact).
  - S3 unconditioned 3-class LCA pushes TR03 to `3,688.4 h` (exact); 3-of-3 unanimous drops TR06 to `330.7 h` (exact); TR06 profile-likelihood LRT against `400.0 h` reproduces **`9.30`** (`9.2972`, exact to 2 decimals).
  - S4 equal-variance pooling gives South `sigma_eq = 37.18 mg/L` (author `37.21`), blowing up TR05 to `1,007.2 h` (author `1,008.9 h`) and cutting TR08 to `432.6 h` (author `433.1 h`); F4 quartile residual SD mismatch reproduces **`0.151 mg/L`** golden vs **`0.453 mg/L`** equal-variance (exact to 3 decimals).
  - Flat 2026 carry-forward drops TR01 to `356.3 h` (author `356.9 h`, `< 400 h`) while TR02 is `442.5 h` (author `443.0 h`).
- **Internal consistency audit across all four answer blocks:**
  - All per-train mode sums, plant sums, overhaul sums, Q3 sums, and Section 4 energy calculations agree across Final Recommendation, Supplementary Questions, Critical Components, and Step-by-Step within standard 0.1 h / 0.01 MWh unrounded-sum rounding (`TR08` rounded modes sum to `745.8` vs `745.9`, `TR05` `326.6` vs `326.7`, `Sum SC` `1,724.3` vs `1,724.5`, `Sum MWh` `2,047.73` vs `2,047.72`, `Sum OV MWh` `1,710.47` vs `1,710.46`).
  - **MISMATCH #1 (Cross-block contradiction):** `Supplementary Questions #1g` reports `TR05: 326.7 h total (uncertainty range 282.5 to 376.1 h)` (confirmed in code: `F4_AR1_innov_MLE` gives `TR05 = 376.1 h`). Yet `Step-by-Step #9` explicitly asserts: *"all 36 variants and all 8 perturbations preserve the exact 5-of-8 overhaul slate (`TR01`, `TR02`, `TR06`, `TR07`, `TR08`), keeping the lowest overhaul train at or above 424.0 h and **the highest monitor train at or below 362.2 h**."* The `362.2 h` figure is solely the `+20%` S2 perturbation on `TR04` (`141.0 + 149.6*1.2 + 41.7 = 362.2 h`), directly contradicting `TR05`'s `376.1 h` upper range in Supplementary #1g.
  - **Minor self-rebuilding omissions in Step-by-Step:** Step-by-Step #3 omits that lag-1 flux covariances `(C4, C8)` use same-calendar-day bottle pairs (`1,375.2 h`) rather than all contiguous cross-midnight pairs (`1,341.1 h`); Step-by-Step #4 omits linear hourly-to-15m flow interpolation and the `8 m3` profiling grid step (continuous optimization gives `1,723.2 h`).

---

## Part B: Determinism, Coded Fork Battery, and Statistical Identifiability

### B.1 Committed Recommendation and Deciding Steps

The committed recommendation schedules 5 trains for 2027 pressure-vessel overhaul (`TR07, TR06, TR08, TR02, TR01` >= 400.0 h) and retains 3 trains on routine monitoring (`TR04, TR05, TR03` < 400.0 h), with plant-wide excess energy penalty `2,047.7 MWh` (`1,710.5 MWh` overhaul subset). Four independent physical modeling steps each move a distinct train across the 400.0 h line (`S1` opens `TR01` while keeping `TR04` monitored; `S2` opens `TR02` while keeping `TR05` monitored; `S3` clears `TR03` while keeping `TR06` overhauled; `S4` opens `TR08` while keeping `TR05` monitored).

### B.2 Comprehensive Coded Fork Table (47 Alternatives Across All Decision Points)

Every open decision point across cleaning/LOQ, S1, S2, S3, S4, and multi-stump joint combinations was coded and run from shipped files (holding non-varied modes at author baseline for single-stump rows, and varying all modes simultaneously for joint rows):

| # | Domain / Fork Description | Key Mode / Metric (h) | In Author Band? | TR01 | TR04 | TR05 | TR08 | Slate Preserved? | Pin / Ruling Evidence |
|---|---|---|---|---|---|---|---|---|---|
| 1 | F0.1: Floor negative boron readings at `0.0 mg/L` (16 rows) | C1 = 1,369.4 | Yes | 475.1 | 331.8 | 327.2 | 745.9 | Yes | Invariant (note) |
| 2 | F0.1: Censor `< 0.020 mg/L` LOQ to `LOQ/2 = 0.010` (30 rows) | C1 = 1,369.5 | Yes | 475.1 | 331.8 | 327.2 | 745.9 | Yes | Invariant (note) |
| 3 | F0.1: Drop `< 0.020 mg/L` LOQ bottles (30 rows) | C1 = 1,353.9 | Yes | 460.2 | 331.8 | 327.2 | 745.9 | Yes | Invariant (note) |
| 4 | F0.2: Boron dates joined on `Europe/Lisbon` instead of UTC | Worse fit 8/8 | - | - | - | - | - | - | Pinned by data (UTC higher R^2 & lower SD 8/8) |
| 5 | F1.1: S1 Exact Block-Averaged Discrete AR(1) Kalman MLE | C1 = 1,321.6 | Yes | 454.4 | 327.2 | 334.9 | 739.7 | Yes | Invariant (note) |
| 6 | F1.2: S1 WLS using all contiguous pairs (cross-midnight) | C1 = 1,342.2 | Yes | 481.4 | 329.1 | 329.0 | 745.9 | Yes | Invariant (note) |
| 7 | F1.3: S1 Exact Continuous-Time 1h-Block OU Kalman MLE | **C1 = 1,155.6** | **No (-43.7 h)** | **427.8** | 320.3 | 311.7 | 734.0 | Yes | **Band undercoverage** (NLL 54,128.16 vs 54,128.22); slate holds |
| 8 | F1.3: S1 Continuous 1h-Block OU WLS (same-day pairs) | C1 = 1,212.5 | Yes | 456.2 | 323.6 | 303.8 | 736.5 | Yes | Invariant (note) |
| 9 | F1.3: S1 Continuous 1h-Block OU WLS (all contiguous pairs) | **C1 = 1,177.9** | **No (-21.4 h)** | 458.0 | 321.4 | 305.7 | 734.0 | Yes | Band undercoverage; slate holds |
| 10 | F1.4: S1 Equal relative weights `[1/V4^2, 1/V4^2, 1/V8^2, 1/V8^2]` | C1 = 1,333.9 | Yes | 532.5 | 335.5 | 295.4 | 745.9 | Yes | Invariant (note) |
| 11 | F1.4: S1 Unweighted OLS moments `[1, 1, 1, 1]` | C1 = 1,329.1 | Yes | 479.3 | 334.0 | 324.6 | 745.9 | Yes | Invariant (note) |
| 12 | F1.4: S1 Inverse asymptotic-variance WLS | C1 = 1,341.5 | Yes | 466.5 | 329.0 | 336.8 | 743.0 | Yes | Invariant (note) |
| 13 | F1.4: S1 4h-only `(V4, C4)` (all contiguous pairs) | C1 = 1,354.3 | Yes | 453.7 | 323.9 | 351.1 | 741.0 | Yes | Single-stump holds; flips TR05 if combined w/ S4 AR(1) |
| 14 | F1.4: S1 `(V4, V8)` variance ratio only (ignores C4, C8) | C1 = 1,479.9 | No (+81.7 h) | 605.6 | 319.1 | 300.9 | 745.9 | Yes | Inferior (drops lag-1 info); slate holds |
| 15 | F1.5: S1 Quarterly `mu_{J,u,q}` (8 regressors) | C1 = 1,347.9 | Yes | 483.9 | 328.0 | 328.9 | 745.9 | Yes | F-test p>0.13 all trains; invariant |
| 16 | F1.5: S1 Monthly `alpha_{u,m}` / Harmonic `alpha_u(doy)` | 1,339.2 / 1,232.8 | Yes / Yes | 482.2 / 461.0 | 323.5 / 327.4 | 330.3 / 303.7 | 745.9 | Yes | Invariant (note) |
| 17 | F1.7: S1 Lab noise off / Proportional `0.80%` RSD | 1,391.7 / 1,384.7 | Yes / Yes | 480.5 / 480.4 | 333.9 / 332.9 | 330.5 / 329.1 | 745.9 | Yes | Invariant (note) |
| 18 | F1.8: S1 Free additive conc noise `sigma_0^2*Q^2 + sigma_J^2` | LRT 0.02-0.19 | Yes | - | - | - | - | Yes | Pinned by data (p > 0.65 everywhere) |
| 19 | F1.9: S1 Huber flux fit / Span-WLS flux fit / 0.5% trim | 1,369.7 / 1,368.3 / 1,194.3 | Yes / Yes / No | 480.6 / 473.7 / 453.8 | 331.1 / 334.2 / 309.0 | 326.2 / 329.3 / 300.2 | 745.9 | Yes | Invariant (note) |
| 20 | F2.1: S2 Continuous L2 optimization (unbounded `Vm`, no grid/snap) | C2 = 1,723.2 | Yes | 480.9 | 330.8 | 327.9 | 744.8 | Yes | Invariant (RMS 0.3406) |
| 21 | F2.2: S2 L1 MAE / Huber / 2%-trimmed conductivity loss | 1,722.9 / 1,723.5 / 1,723.4 | Yes (all 3) | 479.7-480.9 | 331.1-331.4 | 327.0-328.2 | 745.0 | Yes | Invariant (RMS 0.3406-0.3407) |
| 22 | F2.3: S2 1D Gaussian dispersion vs 2-path + dispersion | RMS 0.718 vs 0.341 | - | - | - | - | - | - | Pinned by data (TR05 1D disp RMS 0.718 vs 0.341) |
| 23 | F2.4: S2 Nearest-neighbor TEP volume lookup | C2 = 1,718.5 | Yes | 471.1 | 332.3 | 346.6 | 745.9 | Yes | Single-stump holds; flips TR05 if combined w/ S1+S4 |
| 24 | F2.5: S2 Flow upsampling: `trapz` / `step_left` / `midpoint` | 1,711.9 / 1,663.4 / 1,661.5 | Yes (all 3) | 476.0-478.7 | 329.4-330.5 | 325.4-329.8 | 740.0 | Yes | Invariant (linear cumsum wins RMS 0.3406 vs 0.348-0.395) |
| 25 | F2.5: S2 Flow upsampling: `step_right` (next-hour flow) | C2 = 1,567.9 | No (RMS 0.452) | 466.3 | 323.9 | 322.3 | 730.0 | Yes | Ruled out by RMS 0.452 vs 0.341; slate holds |
| 26 | F2.6: S2 Boundary inclusivity `>= 1.50` vs `> 1.50` | C2 = 1,723.2 | Yes | 480.9 | 330.8 | 327.9 | 744.8 | Yes | Zero points on boundary |
| 27 | F3.1: S3 Age boundary: `+0.5 h` / `+1.0 h` / `side='left'` | 963.0 / 950.5 / 916.9 | Yes (all 3) | 480.9 | 332.3 | 326.7 | 745.9 | Yes | `dt=0` wins NLL (`48470.87` vs `48506.67` left) |
| 28 | F3.1: S3 Volume-based exp / Michaelis-Menten | 955.2 / 881.7 | Yes / Yes | 480.9 | 332.3 | 326.7 | 745.9 | Yes | Exp wins NLL (`48470.87` vs `48473.73 / 48477.51`); slate holds |
| 29 | F3.1: S3 Weibull `k=0.90` / `k=1.15` / free `k=1.019` | 932.9 / 1,091.0 / 984.0 | Yes / Border / Yes | 480.9 | 332.3 | 326.7 | 745.9 | Yes | Free `k=1.019` (LRT vs k=1 = 0.08); `TR03 <= 299.8` |
| 30 | F3.1: S3 Jeffreys MAP (0.5) / Laplace MAP (1.0) / Posterior sum | 971.4 / 967.1 / 975.2 | Yes (all 3) | 480.9 | 332.3 | 326.7 | 745.9 | Yes | Invariant (note) |
| 31 | F3.2: S3 Independent co-occurring Bio & MS (Noisy-OR 4-state) | C3 = 1,064.8 | Yes | 480.9 | 332.3 | 326.7 | 745.9 | Yes | Rejected by data (`dNLL = +94.78`); slate holds |
| 32 | F3.3: S3 4 distinct emission vectors (free Struct vs Mineral) | C3 = 1,018.8 | Yes | 480.9 | 332.3 | 326.7 | 745.9 | Yes | Not sig (`LRT=4.06`, 3 df, p=0.25); slate holds |
| 33 | F4.1: S4 OLS sq-resid / WLS sq-resid / Joint GLS+MLE (i.i.d.) | 1,083.1 / 1,077.0 / 1,074.8 | Yes (all 3) | 479.9-480.9 | 332.3-333.6 | 324.5-333.4 | 745.8-758.8 | Yes | Invariant (note) |
| 34 | F4.3: S4 Huber mean / Probe noise off (`0 mg/L`) | 1,070.7 / 1,167.2 | Yes / Yes | 470.0 / 489.6 | 336.2 / 339.6 | 326.8 / 336.7 | 754.2 / 759.0 | Yes | Invariant (note) |
| 35 | F4.2: S4 1-step AR(1) innovation MLE (`rho = 0.341`) | C4 = 1,246.2 | Border (+0.8 h) | 482.5 | 328.6 | **376.1** | 701.0 | Yes | Single-stump holds (23.9 h margin); **LRT(TR05>=400)=0.063** |
| 36 | F4.2: S4 Exact 2-stage 4-state AR(1) Kalman MLE (`rho = 0.354`) | **C4 = 1,258.9** | **No (+13.5 h)** | 483.3 | 328.4 | **377.0** | 707.0 | Yes | **Band undercoverage**; **LRT(TR05>=400)=0.058 (p=0.810)** |
| 37 | F4.2: S4 Exact GLS-Kalman 4-state AR(1) MLE (`rho = 0.354`) | C4 = 1,192.0 | Yes | 484.2 | 325.6 | **360.2** | 739.8 | Yes | **LRT(TR05>=400)=0.240 (p=0.624)** |
| 38 | F4.2: S4 Exact Per-Train-`rho_u` 4-state Kalman MLE | C4 = 1,250.2 | No (+4.8 h) | 483.3 | 328.4 | **370.2** | 737.7 | Yes | Valid AR(1) MLE (`LRT=2.80` vs common rho) |
| 39 | F4.4: S4 Per-quarter `sigma_{u,q}` (12 extra df/bay) | C4 = 1,403.4 | No | 470.3 | 326.7 | **562.3** | 707.2 | **No** | Ruled out by data (`LRT=14.25` South, 12 df, p=0.285; BIC rejects) |
| 40 | F4.5: S4 Unconstrained common bay covariance `c_cov` | C4 = 1,325.2 | No | 406.9 | 315.4 | **481.4** | 850.3 | **No** | Ruled out (`LRT=0.204`, p=0.65; negative `c=-129.5`; constrained `c>=0` holds) |
| 41 | F4.6: S4 Mean structure: Annual / Harmonic / Monthly | 1,221.7 / 1,150.8 / 1,474.7 | Yes / Yes / No | 480.9 | 332.3 | 330.0 / 328.8 / **400.0** | 866.9 / 735.4 / 771.3 | Yes / Yes / **No** | Quarterly wins BIC by +131.9 to +837.9 (South) & +219.5 to +1,067.9 (North) |
| 42 | F4.6: S4 Student-t heteroscedastic MLE | North df=81, South df=2597 | Yes | 480.9 | 332.3 | 326.7 | 745.9 | Yes | Pure Gaussian confirmed |
| 43 | **Joint A (All 4 Gold-Standard MLEs):** S1 Block-AR(1) MLE + S2 Cont L2 + S3 Exact MLE + S4 GLS-Kalman | Plant 5,211.5 | Yes | 457.4 | 319.0 | **369.4** | 732.4 | Yes | Holds, but TR05 sits inside `LRT = 0.240` noise |
| 44 | **Joint B (All 4 Exact MLEs, 2-stg Kalman):** S1 Block-AR(1) MLE + S2 Cont L2 + S3 Exact MLE + S4 2-stg Kalman | Plant 5,278.4 | Yes | 456.5 | 321.8 | **386.2** | 699.6 | Yes | **13.8 h margin on TR05**, inside `LRT = 0.058` noise |
| 45 | **Joint C (Author-endorsed variants):** S1 4h-only WLS + S2 8m3 + S3 MLE + S4 1-step AR(1) innov | Plant 5,300+ | - | 455.3 | 320.2 | **400.7** | 696.0 | **NO (FLIPS TR05)** | **NO PIN FOUND** (both variants endorsed in Step-by-Step #9) |
| 46 | **Joint D (Author-endorsed variants):** S1 Exact MLE + S2 Nearest TEP + S3 MLE + S4 1-step AR(1) innov / 2-stg Kalman | Plant 5,270+ | - | 446.2 | 323.5 | **404.5 / 405.3** | 694.7 / 700.7 | **NO (FLIPS TR05)** | **NO PIN FOUND** (all 3 choices endorsed or more rigorous than author) |
| 47 | **Joint E (Author-endorsed variants):** S1 InvAsymp WLS + S2 Nearest TEP + S3 MLE + S4 2-stg Kalman | Plant 5,310+ | - | 459.1 | 325.1 | **407.2** | 704.0 | **NO (FLIPS TR05)** | **NO PIN FOUND** |

### B.3 Boundary Statistical Identifiability (Profile-Likelihood LRT Against 400.0 h)

To test Gate C Condition (b) (whether any train's classification across `400.0 h` sits inside estimation noise), exact profile-likelihood ratio tests `2 * (NLL_constrained_at_400h - NLL_MLE)` were computed for every boundary train on its deciding stump:

| Train | Golden 2027 (h) | Designation | Deciding Stump / Model | Critical Parameter for 400.0 h | MLE Parameter | Profile LRT (`2*dNLL`) | p-value | 95% Profile CI (Train Total h) | Statistically Identified? |
|---|---|---|---|---|---|---|---|---|---|
| **TR01** | 480.9 | OVERHAUL | S1 Block-AR(1) Kalman MLE | `sigma_J = 59.68 g/h` | `66.08 g/h` | **7.64** | 0.0057 | `[420.2, 515.3]` | **YES** (strictly > 400 h) |
| **TR04** | 332.3 | MONITOR | S1 Block-AR(1) Kalman MLE | `sigma_J = 38.20 g/h` | `33.80 g/h` | **28.94** | 7.5e-8 | `[317.7, 347.6]` | **YES** (strictly < 400 h) |
| **TR06** | 932.3 | OVERHAUL | S3 49-Param Kinetic MLE | `pi_s = 0.02722` | `0.08065` | **9.30** | 0.0023 | Strictly > 400 h | **YES** (matches author 9.30) |
| **TR08** | 745.9 | OVERHAUL | S4 Bay TDS MLE | `sigma_8 = 33.95 mg/L` | `51.80 mg/L` | **61.66** | < 1e-14 | `[641.8, 842.1]` | **YES** (strictly > 400 h) |
| **TR03** | 236.4 | MONITOR | S3 Kinetic MLE | `pi_s = 0.01690` | `0.00000` | 1.34 (cond.) | 0.25 | All 12 S3 models `<= 299.8 h` | **YES** (model-robust >100 h) |
| **TR05** | **326.7** | **MONITOR** | **S4 i.i.d. MLE** | `sigma_5 = 21.65 mg/L` | `16.22 mg/L` | **1.060** | **0.3031** | **`[316.2, 489.8]`** | **NO (STRADDLES 400 h)** |
| **TR05** | **360.2** | **MONITOR** | **S4 GLS-Kalman AR(1) MLE** | `sigma_5 = 22.72 mg/L` | `20.46 mg/L` | **0.240** | **0.6239** | **Straddles 400 h** | **NO (STRADDLES 400 h)** |
| **TR05** | **377.0** | **MONITOR** | **S4 2-Stage Kalman AR(1) MLE** | `sigma_5 = 21.65 mg/L` | `20.50 mg/L` | **0.058** | **0.8097** | **`[316.2, ~615.0]`** | **NO (STRADDLES 400 h)** |

**Diagnosis:** While `TR01`, `TR02`, `TR03`, `TR04`, `TR06`, `TR07`, and `TR08` are decisively pinned on the correct side of `400.0 h`, **`TR05` fails Gate C on BOTH prongs**: (a) valid multi-stump combinations of author-endorsed / exact-MLE estimators straddle `400.0 h` (`326.7 h` to `407.2 h`, flipping the 5-of-8 slate to 6-of-8), and (b) the data in `bay_permeate_tds_hourly_2026.csv` cannot statistically separate `TR05 < 400 h` from `TR05 >= 400 h` (`LRT = 0.058` to `1.060`, `p = 0.30` to `0.81`). The author cited `TR06`'s `LRT = 9.30` in Step-by-Step #5 to demonstrate statistical identifiability across 400.0 h, but did not check `TR05`'s S4 profile LRT.

### B.4 Data Anomalies and Giveaways

- **Data anomalies:** Every operational anomaly (432 QA revision-1 boron duplicates, 720 Q1 schedule legacy tags, 283 CIP legacy tags, 16 late-Dec 2025 carryover washes, 849/829/174/55 exact telemetry retries, South-bay `L/s` and `ug/L` + `DD/MM/YYYY` exports, 32 burn-in intervals) has an explicit governing policy in Protocol SWRO-Q27 or LIMS QA Certificate `LAB-QA-2026-B08`. The 16 negative and 30 `< LOQ` boron readings have no explicit censoring rule in the certificate, but all three lab conventions (keep raw, floor at 0 / `LOQ/2`, drop `< LOQ`) leave C1 within `[1,353.9, 1,375.5]` and preserve the slate.
- **Giveaways:** ZERO. None of the 15 input files states the overhaul slate, any decisive figure, a copy of a deliverable, or solution code.

---

## Gates A to E Assessment

- **Gate A (Solution Correctness & Internal Consistency): FAIL (`minor_mismatch`)**
  - All 8 train point values, 4 critical component point values, energy penalties, raw monitoring contrasts, and rival comparisons reproduce accurately from the shipped files at the right grain (all 4 modes verified independently).
  - **Defect:** Direct internal contradiction between `Supplementary Questions #1g` (`TR05` 36-variant upper range = `376.1 h`) and `Step-by-Step #9` (*"keeping ... the highest monitor train at or below 362.2 h"* across all 36 variants and 8 perturbations). Also minor unstated self-rebuilding details (S1 same-day lag pairs; S2 linear flow interpolation + `8 m3` grid step) and pre-dedup (`7,729`) vs post-dedup (`7,512`) assay counts in Step-by-Step #1.
- **Gate B (Every Decisive Fact & Action Vocabulary Grounded): PASS**
  - Every threshold (`0.50 mg/L`, `1.50 & 1.50`, `450 mg/L`, `400.0 h`), energy rate (`420 / 360 / 540 / 300 kWh/h`), probe repeatability (`0.004 mg/L`, `3.5 mg/L`), Annex A projection factor, Annex B 9-column CSV schema, and every distinctive vocabulary term in `FINAL_RECOMMENDATION` appears explicitly in the shipped PDFs, JSON, and CSVs.
- **Gate C (Uniquely Forced, No Defensible Alternative / Margin Robustness): FAIL (`margin_or_boundary_fragility` on `TR05`)**
  - S1 (`TR01` vs `TR04`), S2 (`TR02`), S3 (`TR03` vs `TR06`), and S4 (`TR08`) are cleanly forced by physical falsification identities (F1-F4) and strong statistical separation (`LRT >= 7.64`, `p <= 0.0057`).
  - **`TR05` fails Gate C** under both (a) multi-stump combinations of valid/author-endorsed estimators (`S1 Exact MLE + S2 Nearest TEP + S3 MLE + S4 AR(1) innov/Kalman MLE = 404.5-405.3 h`; `S1 4h-only + S4 AR(1) innov = 400.7 h`, flipping `TR05` to `OVERHAUL`) and (b) statistical sampling/estimation noise (`LRT(TR05 >= 400.0 h) = 1.060, p = 0.303` i.i.d.; `0.240, p = 0.624` GLS-Kalman; `0.058, p = 0.810` 2-stage Kalman; 95% profile CI `[316.2, 489.8 h]` i.i.d. and `[316.2, ~615 h]` Kalman).
  - Additionally, two gold-standard exact MLEs fall outside the stated critical-component bands (`Exact Continuous-OU 1h-Block MLE` `C1 = 1,155.6 h` vs `[1,199.3, 1,398.2]`; `Exact 2-Stage 4-State AR(1) Kalman MLE` `C4 = 1,258.9 h` vs `[1,069.3, 1,245.4]`).
- **Gate D (Analytical Hardness, Not Semantics): PASS**
  - Difficulty comes purely from four genuine statistical/physical modeling challenges (flow-proportional mass-flux heteroscedasticity, bimodal variable-flow residence mixing, post-CIP continuous regrowth kinetics, and heteroscedastic shared-collector variance deconvolution), not from wording ambiguity or planted traps.
- **Gate E (Prompt Unambiguous on Decision, Not Method): PASS**
  - `prompt.txt` cleanly pins the decision ("Which Barlavento SWRO trains need vessel overhauls in 2027 ... and what is the resulting energy penalty in MWh?") and deliverables (engineering workbook with per-train forecasts, uncertainty ranges, plant-wide and summer Q3 totals, chart, 2026-to-2027 backup, plus matching historian CSV) without leaking methods, formulas, or rounding rules.

---

## Required Fixes (`SEND_BACK`)

1. **Pack / Generator Fix (Required to close Gate C `margin_or_boundary_fragility` on `TR05`):**
   - **Location:** `task28` data generator (`TR05` baseline parameters in S4 South Bay TDS and/or S1/S2 non-TDS baseline hours on `TR05`).
   - **Exact change:** Increase `TR05`'s statistical clearance below the `400.0 h` overhaul threshold without weakening the S4 equal-variance pooling stump (where `TR05`'s high mean TDS still blows up `TR05` well above `400.0 h` when pooled with volatile `TR08`). Concretely, either:
     - (a) Lower `TR05`'s non-TDS 2027 hours (S1 Boron and/or S2 Scaling) by ~50 to 60 h (from `316.2 h` to `~255-265 h`, giving `TR05` `~135-145 h` of TDS headroom instead of `83.8 h`), **and/or**
     - (b) Reduce `TR05`'s quarterly mean TDS in `bay_permeate_tds_hourly_2026.csv` by ~8 to 10 mg/L (from `387.1 mg/L` to `~378 mg/L`, still `+25 mg/L` above `TR08`'s `353.1 mg/L` so equal-variance pooling still flips `TR05` well past `500+ h`, while shrinking `TR05`'s AR(1) Kalman TDS to `< 15 h`) and/or reduce S4 AR(1) autocorrelation if unrequired.
   - **Verification bar after rebuild:** Confirm in code that on `TR05`: (i) profile-likelihood `LRT(TR05 >= 400.0 h) >= 6.0` (`p < 0.015`) under **both** i.i.d. MLE and exact 4-state AR(1) Kalman / GLS-Kalman MLE; (ii) **all** cross-stump combinations of defensible variants (including `S1 Exact Block-AR(1) MLE + S2 Nearest TEP + S3 Exact MLE + S4 Exact Kalman MLE` and `S1 4h-only + S4 AR(1) innov MLE`) keep `TR05 <= 360 h`; and (iii) the equal-variance S4 rival still flips `TR05` decisively above `400.0 h` (`> 500 h`).
2. **Answer Block Fixes (`submission.md`):**
   - **Step-by-Step #9:** Reconcile the maximum MONITOR train bound across all variants AND `+/-20%` perturbations so it matches the exact maximum across all trains in `Supplementary Questions #1` (currently `362.2 h` contradicts `TR05`'s `376.1 h`). Update the closing-paragraph tightest boundary clearance statement to check both point clearances and upper/lower uncertainty bounds across all 8 trains.
   - **Uncertainty Bands (Final Recommendation, Supplementary Questions, Critical Components, Step-by-Step #9):** Include **Exact Continuous-Time 1h-Block OU MLE** in the S1 variant battery and **Exact 4-State AR(1) Kalman MLE (both 2-stage and GLS-Kalman)** in the S4 variant battery so that C1, C4, and per-train bands enclose every gold-standard exact MLE.
   - **Step-by-Step #1, #3, #4 (self-rebuilding precision):** State explicitly whether the `7,729` count in Step #1 refers to raw pre-dedup rows (`7,512` post-dedup), specify same-day vs cross-midnight lag-1 bottle pairs in Step #3, and note linear hourly-to-15m flow interpolation and the profiling grid step in Step #4.
