# Determinism Check Report (Pass 2): task26 (v4)

- **Verdict:** DETERMINISTIC
- **Disposition:** FIX_NOW (answer-block edits in `submission.md` only: correct Step 8's boundary-clearance omission of Svarthaug and state minor Step 3-5 reconstruction conventions explicitly so the Step-by-Step rebuilds every figure to 2 decimal places without guesswork; zero changes to `prompt.txt`, `target.zip`, or what solvers see; no model rerun required).

## Summary

All five determinism gates (Gates A to E) pass. Every load-bearing figure in `submission.md` (Final Recommendation, all three Critical Components, all seven substations' `P15`, `Q_h`, `w_max`, `Lim_MVA`, Firm N-1 Loading %, Relief MVA, and Phase, plus pool rollups) reproduces directly from a fresh unzip of `target.zip` to exact 2-decimal precision (`0.00` discrepancy across 47 figures). Every decisive scope rule, formula, threshold, and filing rollup is explicitly filed in `vesterdal_planning_standard_ns2026.pdf`, and all distinctive terms in the Final Recommendation appear verbatim in the shipped files. Across 32 concrete Gate C forks (including NS-2026 Section 3.1/3.2/5.1 estimand readings, S1/S2/S3 estimator neighbors, windows, scaling, PT anchors, voltage denominators, nonlinear AC DistFlow, calendar alignment, rounding order, and six +/-20% forcing perturbations), zero defensible forks flip the seven-substation relief schedule or move Total Relief outside `46.2 to 61.5 MVA`, and every rival that flips a site is refuted by direct physical measurements in the shipped files.

Disposition is `FIX_NOW` rather than `APPROVE` solely for answer-block self-containment and wording accuracy in `submission.md` (Rule 6): Step 8 omits Svarthaug (`93.13%`, band `90.7% to 97.2%`, `6.87 pp` point / `2.8 pp` band-edge clearance below `100.0%`) when listing the thinnest boundary clearances, and Step 3 omits two minor rules needed to hit `k_ord = 0.9298` and `230.12 MW` to exact 2-decimal precision (zero-clamping negative off-diagonal `R` entries and averaging `d` over NDJF before `sqrt(d^T R d)`), plus clarifying that the four cited correlation means (`0.8347 / 0.8318 / 0.0616 / 0.0877`) are over the first five bursty feeders per site.

## 1. Gate A: Recomputed Golden Figures vs `submission.md`

Fresh ETL conformance on `scada_substation_hourly_2026.csv` yields `101,160` raw rows -> `96,360` clean substation-hours after dropping `4,800` `B20270104_PRELIM` rows by latest `extract_ts`, aligning Raudfjord `CET_Standard` (`DD.MM.YYYY HH:MM`, UTC+1) to UTC (matching hourly `feeder_scada_hourly_2026.csv` sums to `2e-5 MW` and `pq_commissioning_2026.csv` 4x15m means to `7.5e-6 MW`), and interpolating `56` summer nulls in `v_lv_kv`. In-scope 60-minute SCADA peaks sum to `195.43 MW` (exact).

| Entity | P15 (MW) | Q_h (MVAr) | w_max (%) | Lim_MVA | Loading % | Relief MVA | Phase | vs Blocks |
|---|---:|---:|---:|---:|---:|---:|---|---|
| Hestmark | 41.28 (41.28) | 15.81 (15.81) | 35.27 (35.27) | 46.77 (46.77) | 137.55 (137.55) | 17.87 (17.87) | Phase 1 (2027) | Exact |
| Raudfjord | 29.71 (29.71) | 9.45 (9.45) | 52.76 (52.76) | 49.35 (49.35) | 110.89 (110.89) | 11.52 (11.52) | Phase 1 (2027) | Exact |
| Kvernholm | 26.96 (26.96) | 19.49 (19.49) | 33.82 (33.82) | 33.75 (33.75) | 108.18 (108.18) | 7.23 (7.23) | Phase 1 (2027) | Exact |
| Drangvik | 42.50 (42.50) | 18.59 (18.59) | 34.73 (34.73) | 48.33 (48.33) | 106.46 (106.46) | 9.74 (9.74) | Phase 1 (2027) | Exact |
| Svarthaug | 29.25 (29.25) | 9.52 (9.52) | 33.91 (33.91) | 31.29 (31.29) | 93.13 (93.13) | 2.73 (2.73) | Phase 2 (2028-2029) | Exact |
| Malmnes | 37.78 (37.78) | -0.69 (-0.69) | 34.98 (34.98) | 39.65 (39.65) | 93.07 (93.07) | 3.44 (3.44) | Phase 2 (2028-2029) | Exact |
| Tverrli | 22.66 (22.66) | 7.45 (7.45) | 36.75 (36.75) | 26.30 (26.30) | 64.94 (64.94) | 0.00 (0.00) | Defer | Exact |
| **Pool Rollup** | **230.12 (230.12)** | **79.63 (79.63)** | **37.46 (37.46)** | **275.43 (275.43)** | -- | **52.53 (52.53)** | **4 P1 / 2 P2 / 1 DF** | **Exact** |

Critical Components (all exact and inside bands):
- CC1 Combined peak 15-min active demand: `230.12 MW` (band `224.7 to 234.4 MW`).
- CC2 Combined peak-hour reactive demand: `79.63 MVAr` (band `78.3 to 86.1 MVAr`).
- CC3 Unweighted average peak limiting-phase share: `37.46%` (band `37.38% to 37.77%`).

Spot-checks of Step 2 hurried reading and closing single-stump ablations (all reproduced):
- Step 2 hurried baseline (`P60 + annual net kVARh + AMI-only`): `8.73 MVA` total relief; Hestmark `104.57%`, Svarthaug `91.18%`, Malmnes `82.51%`, Kvernholm `81.30%` (block `81.31%`), Drangvik `70.12%`, Raudfjord `62.72%`, Tverrli `51.21%` (4 sites misplaced).
- Lose S1 alone (`P60 + Q_gold + w_gold`): `195.43 MW`, Drangvik `83.05%` (Defer), Malmnes `75.33%` (Defer), Total Relief `25.38 MVA`.
- Lose S2 alone (`P15_gold + annual kVARh + w_gold`): Drangvik `98.11%` (P2), Kvernholm `87.66%` (P2), Malmnes `100.78%` (P1), Total Relief `39.04 MVA`.
- Lose S3 alone (`P15_gold + Q_gold + AMI-only`): `34.58%` mean `w_max`, Raudfjord `70.89%` (Defer), Svarthaug `103.62%` (P1), Total Relief `41.26 MVA`.

## 2. Direct 9-Point PQ Commissioning Validation (S1) and S2/S3 Rival Refutation

### S1: 9-Point Monthly `max(P_15) - max(P_60)` MAE Table (`pq_commissioning_2026.csv`)

Using `d_i = max(0, M_15,i - P_60,i)` across all 9 Sep/Oct/Dec site-months on Fossheim (mean `excess/sum_d = 0.3127`), Solberg (`0.5716`), and Lindberg (`0.8385`), the 70-feeder log-centered SCADA matrix has a sharp 5.0x singular-value cliff after mode 4 (`303.03, 169.28, 74.42, 12.20` vs `2.45, 2.19`, capturing `99.94%` variance in 4 modes). Every S1 rival fails the direct 9-point 15-minute PQ validation by `4.0x to 16.5x`:

| S1 Estimator / Rival | 9-pt MAE (MW) | Recomp vs Block MAE | Sum P15 (MW) | Relief (MVA) | Drangvik % | Malmnes % | Schedule Flips / Status |
|---|---:|---|---:|---:|---:|---:|---|
| Golden SVD-4 (`k_ord = 0.9298`) | **0.52** | 0.52 vs 0.52 | 230.12 | 52.53 | 106.46 | 93.07 | None (Golden) |
| 60-min SCADA floor | 8.64 | 8.64 vs 8.64 | 195.43 | 25.38 | 83.05 | 75.33 | Refuted (16.5x MAE); flips Dra, Mal |
| Linear register sum (`k = 1.0`) | 5.96 | 5.96 vs 5.96 | 258.05 | 78.70 | 112.54 | 116.23 | Refuted (11.4x MAE); flips Mal, Sva |
| Nearest-hub twin ratio (fvec, LOO) | 5.12 | 5.12 vs 5.12 | 231.22 | 53.48 | 99.65 | 98.71 | Refuted (9.8x MAE); flips Dra |
| 12-mo register corr (`rel_d = d_i/P_60,i`) | 4.06 | 4.06 vs 4.06 | 229.72* | 52.3 | 99.63* | 103.58* | Refuted (7.8x MAE; Mal 0.924 vs Dra 0.499) |
| Flat PQ ratio (`1.3074`) | 3.54 | 3.54 vs 3.52 | 255.51 | 76.67 | 102.47 | 98.48 | Refuted (6.8x MAE); flips Sva (110.89%) |
| Raw hourly corr (`k = 0.677`) | 2.86 | 2.86 vs 2.86 | 230.61 | 52.96 | 100.24 | 99.51 | Refuted (5.5x MAE); no flip |
| 1-PC stripping (`k = 0.862`) | 2.84 | 2.84 vs 2.84 | 231.81 | 54.27 | 100.45 | 99.94 | Refuted (5.4x MAE; Dra 0.400 vs Mal 0.397) |
| 2-PC stripping | 2.84 | -- | 233.43 | 55.71 | 100.57 | 100.11 | Refuted (5.4x MAE); flips Mal |
| Pooled register CF (`0.592`) | 2.82 | 2.82 vs 2.82 | 232.48 | 54.66 | 100.25 | 99.53 | Refuted (5.4x MAE); no flip |
| Independent quadrature (`R = I`, `k = 1.608`) | 2.50 | 2.50 vs 2.50 | 240.78 | 62.18 | 102.56 | 102.82 | Refuted (4.8x MAE); flips Mal |
| 3-PC stripping | 2.32 | -- | 228.63 | 51.41 | 101.64 | 97.72 | Refuted (4.4x MAE); no flip |
| 2-param OLS `a*sum_d + b*l2_d` on 9 PQ pts | 2.08 | -- | -- | -- | -- | -- | Refuted (4.0x MAE) |
| Force Fossheim ratio (`0.3127`) on Malmnes | n/a | -- | 228.12 | 50.42 | 106.46 | 88.12 | No flip (stays P2, 88.12% exact) |
| Force Solberg ratio (`0.5716`) on Malmnes | n/a | -- | 232.41 | 54.93 | 106.46 | 98.71 | No flip (stays P2, 98.71% exact) |

*Note: On `d_i` directly (unscaled), `register_rho` gives MAE `3.08 MW` (`5.9x` golden) and flips Dra `97.92%` / Mal `100.18%`; on `rel_d = d_i/P_60,i` it reproduces `Malmnes = 0.9238 (0.924)`, `Drangvik = 0.4988 (0.499)`, and `MAE = 4.06 MW` exactly.

### S2 and S3 Rival Refutation Summary

- **S2 (`scada_substation_hourly_2026.csv` + `revenue_meter_monthly_2026.xlsx`):** Golden coupled 66 kV inversion closes hourly 22 kV LV bus Ohm's-law balance to **`0.0 V` RMSE** and 12-month settled `net_kvarh` to **`0.00 MVAr`**. Every S2 rival violates LV bus voltage or energy balance severely: annual net kVARh (`256.7 V` RMSE, flips Dra/Kve/Mal), winter net kVARh (`276.2 V`, flips Dra/Kve), monthly linear `Q(P)` (`345.9 V`, flips Dra/Kve), monthly `Q(P+winter)` (`101.6 V`, flips Kve), monthly `Q(P^2)` (`792.6 V`, flips Mal), class nominal PFs (`153.3 V` & `4.10 MVAr` kVARh error, flips Kve/Mal), target-only corridor dropping upstream hubs (`90.5 V`), local single-site dV (`1,256.0 V`, flips Mal/Sva/Tve), ignoring `R*P` (`172.3 V`), and un-demeaned corridor `delta_PT = 0` (`5.13 MVAr` kVARh error).
- **S3 (`substation_phase_bus_voltages_2026.csv` + `ami_lateral_telemetry_2026.db` + `commissioning_phase_log_2025.csv`):** Golden multi-class bus-sag regression with AMI-measured `tan_phi_res = 0.1250` and `tan_phi_com = 0.6200` closes 3-phase bus-sag balance to **`2.04 V` RMSE** (exact), AMI lateral reactive power to `0.93 kVAr` (all 11) / `1.02 kVAr` (7 in-scope), and AMI CMR voltage tracing matches **`80/80` (`100.0%`)** of `commissioning_phase_log_2025.csv`. Every rival fails directly: GIS (`28/80 = 35.0%` commissioning accuracy, `35.9 V` bus RMSE), AMI-only (`34.58%` mean `w_max`, flips Raudfjord to `70.89%` and Svarthaug to `103.62%`), scalar OLS `dv ~ P_tot` (`23.4 V` bus RMSE, Svarthaug `142.0%`), evening 17-21 scalar OLS (`29.4 V` bus RMSE), manual-PF multi-class OLS (`33.6-37.3 kVAr` AMI RMSE vs `0.93-1.02`, flips Raudfjord to `86.27%`), and raw bus voltage (`114.6 V` RMS).

## 3. Gate C: Comprehensive Fork Battery (28 Concrete Forks + 6 Perturbations)

Every fork below was computed directly from `target.zip` and checked against both the 7-substation schedule and all stated bands (`P15: 224.7-234.4`, `Q: 78.3-86.1`, `w_max: 37.38-37.77`, `Relief: 46.2-61.5`, plus all 7 site loading bands):

| # | Gate C Fork | Sum P15 | Sum Q | Mean w% | Relief | Dra% | Mal% | Result / Assessment |
|---|---|---:|---:|---:|---:|---:|---:|---|
| 1 | S1: 5-PC SVD (`MAE 0.52`) | 230.15 | 79.63 | 37.46 | 52.55 | 106.49 | 93.03 | **IN_BAND**, 0 flips |
| 2 | S1: 6-PC SVD (`MAE 0.49`) | 230.35 | 79.63 | 37.46 | 52.73 | 106.79 | 92.83 | **IN_BAND**, 0 flips |
| 3 | S1: All-70 feeders SVD-4 (no LOSO, `MAE 0.55`) | 230.86 | 79.63 | 37.46 | 53.2 | 107.0 | 92.8 | **IN_BAND**, 0 flips |
| 4 | S1: Raw-P centered SVD-4 (`MAE 0.58`) | 230.58 | 79.63 | 37.46 | 52.9 | 106.3 | 93.8 | **IN_BAND**, 0 flips |
| 5 | S1: Class-reference residual (`MAE 0.52`) | 230.12 | 79.63 | 37.46 | 52.52 | 106.46 | 93.06 | **IN_BAND**, 0 flips |
| 6 | S1: `diff(log P)` SVD-4 (`MAE 0.53`) | 230.09 | 79.63 | 37.46 | 52.50 | 106.40 | 93.09 | **IN_BAND**, 0 flips |
| 7 | S1: Calendar FE (day + hr-of-wk, no SVD, `MAE 0.63`) | 230.76 | 79.63 | 37.46 | 53.1 | 107.7 | 92.2 | **IN_BAND**, 0 flips |
| 8 | S1: Unclipped `R` + `mean(sqrt(d^T R d))` | 230.15 | 79.63 | 37.46 | 52.56 | 106.47 | 93.09 | **IN_BAND**, 0 flips |
| 9 | S1: Winter-only SVD-4 (`MAE 0.55`) | 230.14 | 79.63 | 37.46 | 52.50 | 106.43 | 93.03 | **IN_BAND**, 0 flips |
| 10 | S1: Register windows (12-mo / DJF / Jan) | 226.33-231.06 | 79.63 | 37.46 | 48.82-53.40 | 105.28-106.86 | 88.46-94.65 | **IN_BAND**, 0 flips |
| 11 | S1: Multiplicative / scaled-additive excess | 232.99 | 79.63 | 37.46 | 55.30 | 108.19 | 94.18 | **IN_BAND**, 0 flips |
| 12 | S1: `k_ord` = OLS0 / mean / median / Dec / unit / LOO | 228.41-232.74 | 79.63 | 37.46 | 51.40-54.99 | 105.1-108.28 | 92.2-94.41 | **IN_BAND**, 0 flips |
| 13 | S2: Peak window top-1 / top-3 / top-7 / top-5 med | 230.12 | 78.72-82.59 | 37.46 | 52.0-53.82 | 106.3-107.00 | 93.06-93.07 | **IN_BAND**, 0 flips |
| 14 | S2: Top-20 local `Q(P)` regression at `P60_ann` | 230.12 | 84.80 | 37.46 | 54.87 | 107.04 | 93.09 | **IN_BAND**, 0 flips |
| 15 | S2: Top-10 peak hours (includes off-peak hrs 8-10) | 230.12 | 77.08 | 37.46 | 51.36 | 106.26 | 93.06 | 0 flips; only `Q` 1.2 MVAr below band (hrs 8-10 drop 15% in P, 40% in Q on Rau/Sva) |
| 16 | S2: PT anchor NDJF / all-12 / drop 56 nulls / DST | 230.12 | 79.62-79.63 | 37.46 | 52.53 | 106.46 | 93.07 | **IN_BAND**, 0 flips |
| 17 | S2: Voltage basis (`V_bar` / meas `V_gsp,V_lv` / nonlinear AC DistFlow / 1-step `M_bar`) | 230.12 | 79.63-84.52 | 37.46 | 52.53-54.85 | 106.46-107.68 | 93.06-93.08 | **IN_BAND**, 0 flips |
| 18 | S2: Floor negative `Q_h >= 0` (Malmnes `-0.69 -> 0`) | 230.12 | 80.32 | 37.46 | 52.52 | 106.46 | 93.05 | **IN_BAND**, 0 flips |
| 19 | NS-2026 Sec 3.1: `Q15` const-PF (`Q*P15/P60`) | 230.12 | 93.81* | 37.46 | 58.91 | 113.68 | 93.08 | 0 flips, all loads/Relief IN_BAND; `Q15` ruled out by NS-2026 Sec 3.1 (`Q_h`) & Sec 5.1 |
| 20 | NS-2026 Sec 3.1: `Q15` peak-regime slope (top-20) | 230.12 | -- | 37.46 | ~59.0 | 113.5 | 93.8 | 0 flips, loads/Relief IN_BAND; ruled out by NS-2026 Sec 3.1 (`Q_h`); naive top-200 crosses Mal cap step |
| 21 | S3: Bus-sag window (winter / heating / diff / 2-class) | 230.12 | 79.63 | 37.45-37.47 | 52.47-52.59 | 106.40-106.54 | 92.96-93.11 | **IN_BAND**, 0 flips |
| 22 | S3: Peak hours top-5 (`avgP` / `avgW`) / top-10 `avgP` | 230.12 | 79.63 | 37.42-37.70 | 50.66-51.9 | 106.41 | 92.90 | **IN_BAND**, 0 flips |
| 23 | S3: Winter AMI `tan_phi` / per-site AMI `tan_phi` | 230.12 | 79.63 | 37.46 | 52.53 | 106.46 | 93.07 | **IN_BAND**, 0 flips |
| 24 | S3: Measured `V_bar` denom in `3(R+X tan_phi)/V` | 230.12 | 79.63 | 37.56 | 53.0 | 106.46 | 93.18 | **IN_BAND** on CC3/loads/Relief, 0 flips (Rau `w` 53.26 vs 53.15) |
| 25 | NS-2026 Sec 3.2: `w_max` at `P15` (surge in `P_bal`) | 230.12 | 79.63 | 37.05 | 49.84 | 105.30 | 92.23 | 0 flips, all loads/Relief IN_BAND; ungrounded (no 15-min class data; ignores `d_res=0.87, d_com=0.82`) |
| 26 | NS-2026 Sec 3.2: `w_max` at `P15` (surge by class `d_i`) | 230.12 | 79.63 | 37.18 | 50.43 | 105.54 | 92.37 | 0 flips, all loads/Relief IN_BAND; ungrounded (assumes linear coincidence contradicting `R`; 6/9 PQ peaks occur outside 60-min peak hour) |
| 27 | NS-2026 Sec 3.1/3.2: Apparent-power `w_max(S)` | 230.12 | 79.63 | 37.16 | 51.48 | 107.10 | 93.06 | 0 flips, all loads/Relief IN_BAND; ruled out by Sec 3.2 active-load definition & Sec 3.1 `3*w_max*S_15m` |
| 28 | Rounding order: 2-dp rounded inputs into NS-2026 | 230.12 | 79.63 | 37.46 | 52.54 | 106.46 | 93.08 | **IN_BAND**, 0 flips |
| P1-6 | Six +/-20% perturbations (`k_ord`, `Q_peak`, `w-1/3`) | 223.19-237.06 | 63.70-95.55 | 36.63-38.28 | 46.02-59.61 | 101.66-111.29 | 89.52-96.62 | **0 schedule flips** across all 6 stress perturbations |

Note on CC3 band (`37.38% to 37.77%`): Do **not** widen the lower edge below `37.38%`, because the rejected `evening 17-21 cutoff OLS` rival sits at `37.34%`. Every physically grounded hourly S3 estimator lands inside `37.38% to 37.77%`.

## 4. Gates B, D, E, and Rule 6 (Self-Contained Step-by-Step)

- **Gate B (Filed Facts & Vocabulary): PASS.** `vesterdal_planning_standard_ns2026.pdf` explicitly specifies scope (7 in-scope sites vs 4 modernized hubs), calendar year (`2026 Europe/Oslo`), exact formulas (`S_15m = sqrt(P_15m^2 + Q_h^2)`, `Lim_MVA = 3 * w_max * S_15m`, `Loading %`, `Relief_MVA`), inclusive thresholds (`100.0%` / `85.0%`), no portfolio cap, and Section 5.1 filing rollups (including unweighted mean `w_max`). Every distinctive term in Final Recommendation (`Phase 1`, `Phase 2`, `Defer`, `Firm N-1`, all 7 site names, `Vesterdal Nett`, `2027-2029`, `relief capacity`, `MVA`, `66 kV`, `kVARh`, `AMI`, `GIS`, `LEGACY_NON_AMI`) appears verbatim in the shipped files.
- **Gates D & E (Asks & Units): PASS.** `prompt.txt` demands one committed call (2027-2029 relief timing per site and overall relief capacity in MVA) plus spreadsheet and substation-level CSV deliverables; units and filing definitions are pinned in `prompt.txt` and NS-2026 Section 5.1 with zero method hints or semantic ambiguity.
- **Rule 6 (Blocks Rebuild on Their Own): FIX_NOW findings in `submission.md` only.**
  1. **Step 8 boundary clearance wording (line 60):** Currently names only Drangvik (`106.46%`, `+6.46 pp` point / `+3.1 pp` band edge above `100.0%`) and Malmnes (`93.07%`, `-6.93 pp` point / `+1.9 pp` band edge above `85.0%`, `-3.8 pp` below `100.0%`) as "the thinnest boundary clearances," omitting **Svarthaug** (`93.13%`, band `90.7% to 97.2%`), which is tighter than Malmnes on point distance (`-6.87 pp` vs `100.0%`) and tighter than Drangvik on band-edge clearance (`-2.8 pp` vs `100.0%`).
  2. **Step 3 exact reconstruction rules (line 55):** To reproduce `k_ord = 0.9298` and `230.12 MW` to `0.00` (rather than `0.9303` / `230.15 MW`), two minor rules had to be inferred: (a) clamping negative off-diagonal entries of `R` at `0` (`R = max(0, R)`, unit diagonal), and (b) averaging each feeder's monthly `d_i` over NDJF before evaluating `sqrt(d_bar^T R d_bar)` (rather than averaging monthly `sqrt(d_m^T R d_m)`). Also clarify that the four cited correlation means (`0.8347` Drangvik, `0.8318` Lindberg, `0.0616` Malmnes, `0.0877` Fossheim) are across the first five bursty (`industrial_batch`/`maritime_port`) feeders of each site (all-feeder means are `0.4014 / 0.4464 / 0.0318 / 0.0480`).
  3. **Steps 4-5 minor formula explicitness (lines 56-57):** State Step 4's tap/voltage basis (`tau = 1 + 0.0125 * ltc_tap_step` on `V_hv / 3`, nominal `66/22 kV` bases, peak-month `2026-01` anchor) and Step 5's class grouping (`P_res`, `P_com`, `P_bal = industrial_batch + maritime_port` from hourly feeder SCADA, `V_nom = 22.0 kV`, zero-intercept OLS `tan_phi_c = sum(p*q)/sum(p^2)`).

## Fix

- **Fix Location:** `solution` (`task26/submission.md` only; do not touch `prompt.txt` or `target.zip`).
- **Exact Changes:**
  1. In **Step 8 (line 60)**, revise the boundary-clearance clause to include Svarthaug: `with the thinnest boundary clearances at Malmnes (93.07%, band 86.9% to 96.2%, +1.9 pp above the 85.0% Phase 2 floor), Svarthaug (93.13%, band 90.7% to 97.2%, -2.8 pp below the 100.0% Phase 1 ceiling), and Drangvik (106.46%, band 103.1% to 115.8%, +3.1 pp above the 100.0% Phase 1 floor).`
  2. In **Step 3 (line 55)**, state that negative off-diagonal entries of `R` are clamped at `0`, that NDJF-averaged `d_bar` enters `sqrt(d_bar^T R d_bar)`, and that `0.8347 / 0.8318 / 0.0616 / 0.0877` are the mean off-diagonal correlations across the first five industrial/maritime feeders per site.
  3. In **Steps 4 and 5 (lines 56-57)**, explicitly note the nominal `66/22 kV` linear tap equation (`tau = 1 + 0.0125 * tap`) anchored on `2026-01`, and that `P_res`, `P_com`, `P_bal` (`industrial_batch + maritime_port`) come from hourly feeder SCADA with zero-intercept OLS `tan_phi_c` and `V_nom = 22.0 kV`.
