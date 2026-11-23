# Determinism Audit Report: task9 (arch6)

- **Verdict:** DETERMINISTIC
- **Disposition:** APPROVE (no edits required to prompt, input pack, or answer blocks; no model rerun required).
- **Fix:** none.

## Summary of Gates A to E and Block Rebuild Check

- **Gate A (Correctness given shipped files): PASS.** Following `Step-by-Step` literally on a fresh unzip of `target.zip` (`/tmp/determinism-task9-arch6/target/`) reproduces every committed figure across `Final Recommendation`, `Supplementary Questions`, `Critical Components`, and `Step-by-Step` to within 0.00 to 0.01 points (and 0.0 percentage points on the pinned share), with exact internal agreement across all four answer blocks. File-grain checks confirm zero discrepancy between `training_scheduler_runs_2024_2026.jsonl` (`rows`/`train_rows`) and `warehouse_labelled_rows_weekly.csv` window sums, and zero discrepancy between the cleaned monitoring panel and `covenant_tier_change_monitor_2026.csv` or Schedule C C1.1 tier boundaries.
- **Gate B (Filed facts and distinctive terms): PASS.** Every governing definition, threshold (`< 5.5` monitor, `5.5 to < 8` remediation plan, `>= 8` escalation), calendar snapshot date (`22 Dec 2025` through `20 Dec 2027`), assessment-year 52-Monday clock (`28 Dec 2026` to `20 Dec 2027`), latest quarter-end book-weight rule (`21 Sep 2026`, `125,031` merchants), warm-start carryover, live vs pinned view rule, exponential recency weighting on 52/104-week windows, and every distinctive term in `Final Recommendation` appears verbatim in the shipped PDFs, XLSX tables, CSVs, and JSONL logs. Distractor files (`feature_drift_psi_weekly.csv`, `gms_model_performance_weekly.csv`, `training_compute_by_run.csv`) introduce zero contradictions.
- **Gate C (Uniquely forced, blind fork audit): PASS.** Across 38 modeling, weighting, calendar, statistical, and hygiene forks spanning all classes, every licensed variant lands inside every stated band and produces the identical five-source placement call (`Escalation`: label revisions; `Remediation plan`: feature releases, optimisation noise, training data; `Monitor`: retunes). Every rival that leaves a band or flips a placement is refuted either by an explicit rule in `gms_model_stability_standard_2026.pdf` / `acquirer_agreement_schedule_c_tier_stability.pdf` or by an empirical statistic computed directly from the 2026 shipped files. Every source clears the 5.5 and 8.0 band thresholds by at least 0.94 points (at least 0.70 points across all variants) and holds under +/-20 per cent variance perturbations.
- **Gates D and E (Unambiguous asks, stated units, no semantic lottery): PASS.** `prompt.txt` demands one committed band placement per model-side source and states exact units for every ask (score points per source and combined for Q1 to Q4 and the year; share of 2027 weekly retrains on pinned feature views), while Standard sections 1 to 4 pin every operative metric and clock definition without prescribing method.
- **Block self-rebuild check: PASS.** All graded figures rebuild directly from the formulas and rules stated in `Step-by-Step` and the governing Standard, with zero internal inconsistencies across the four answer blocks.

## Evidence 1: Recomputed Figures vs Committed Answer Blocks

| Metric | Block Value | Stated Band | Recomputed | Status |
|---|---|---|---|---|
| Label revisions (2027 annual, forced) | 9.82 pts (Escalation) | 9.76 to 9.90 | 9.82 pts (96.34 pts^2) | Exact, in band |
| Feature releases (CC3, 2027 annual) | 7.06 pts (Remediation) | 6.84 to 7.17 | 7.06 pts (7.0602) | Exact, in band |
| Optimisation noise (CC1, 2027 annual) | 6.86 pts (Remediation) | 6.56 to 7.25 | 6.86 pts (wkavg/var) / 6.85 (pool) | Exact, in band |
| Training data (CC2, 2027 annual) | 6.83 pts (Remediation) | 6.70 to 6.87 | 6.83 pts (6.8269) | Exact, in band |
| Retunes (2027 annual, forced) | 4.29 pts (Monitor) | 4.24 to 4.34 | 4.29 pts (18.42 pts^2) | Exact, in band |
| Combined model-side Q1 (21 Dec 2026 to 22 Mar 2027) | 16.89 pts | 16.76 to 17.03 | 16.89 pts | Exact, in band |
| Combined model-side Q2 (22 Mar to 21 Jun 2027) | 17.07 pts | 16.85 to 17.19 | 17.07 pts | Exact, in band |
| Combined model-side Q3 (21 Jun to 20 Sep 2027) | 15.52 pts | 15.22 to 15.69 | 15.52 pts (15.51-15.52) | Exact, in band |
| Combined model-side Q4 (20 Sep to 20 Dec 2027) | 14.69 pts | 14.48 to 14.90 | 14.69 pts (14.68-14.69) | Exact, in band |
| Combined model-side Full Year 2027 | 16.07 pts | 15.87 to 16.26 | 16.07 pts (16.0721) | Exact, in band |
| Pinned feature views share (52 Mondays, 14 families) | 34.8% | 32.4 to 38.3% | 34.8% (34.83%) | Exact, in band |

### Supporting Step-by-Step Figures Verified

- **Step 1 hygiene & book:** 2,933,990 raw panel rows -> 2,845,101 cleaned merchant-weeks; 4 re-sent refreshes (`2024-12-09`, `2025-08-11`, `2026-04-20`, `2026-08-03`); 28,854 raw merchant IDs -> 25,007 unique merchants via Tolka Pay migration (3,847 rows); 2,867 JSONL lines -> 2,858 distinct runs (9 identical duplicate `run_id`s), 1,764 production refits; 870 register pairs (84 replicate, 224 bootstrap, 168 retune shadow, 282 release shadow, 112 label freeze); 21 Sep 2026 book = 125,031 scored merchants. All exact.
- **Step 3 diagnostics:** Replicate book-weighted variance = 22.62 pts^2 (single replicate 4.76 pts; 13x half-replicate 12.13 pts; 13x full replicate 17.15 pts). Warm lag 8 to 25 linear intercept = 75.48 pts^2 (min family 41.35 vs 75.5 and 41.3 stated). Cold era length = 29 to 55 weeks; cold lag 1 to 14 relative quadratic curvature = -0.0115, range -0.054 to +0.020 (vs -0.010, -0.053 to +0.018; warm lag 1 to 14 curvature is -0.169, 15x stronger, with increments decaying from 42.8 to 29.3 pts^2/wk vs flat 29.1 to 30.0 in cold era). Anchored `phi` = 0.64 to 0.82 (variance-based `D_warm`, 0.64 to 0.81 pooled); no-data-subtraction anchored fit = 6.68 pts; unanchored raw warm fit = 9.20 pts (implied replicate 33.12 vs 22.62 measured). All reproduced.
- **Step 4 diagnostics:** Raw bootstrap = 10.21 pts; net of replicate = 9.04 pts; uniform-window turnover = 3.61 to 3.65 pts; fitted `lambda_f` = 0.906 to 0.942; mean log-RMSE = 0.0494 (exponential) vs 0.1881 (uniform) and 0.4947 (lag-0 `1/n_t`). All reproduced.
- **Step 5 diagnostics:** Leave-one-rollout-out 39-week validation: runtime 35.7 vs 36.1%, warm start 37.5 vs 35.4%, bf16 34.6 vs 37.3% (all exact to 0.1%); calendar planned pinned share = 83.4%, environment-slip alone = 79.5%. Single-release variance = 6.15 pts^2; 141 same-group pairs all positive (mean corr 0.783, min 0.702); 2,580 cross-group pairs mean corr -0.001; orthogonal releases = 4.70 pts (1.96 planned); all-aligned releases = 11.10 pts. All exact.
- **Step 6 internal 2026 record check (native pts^2):** (i) `D_warm(1)` observed = 47.14 vs committed implied 47.06; (ii) 8-week trailing-volume bootstrap net-variance contrast observed = 10.88 vs committed implied 10.38 to 10.43 (uniform = -0.67); (iii) same-group release-shadow covariance observed = 4.80 vs committed implied 4.79 (orthogonal = 0.00). Total absolute discrepancy = 0.53 to 0.58 (committed), 12.62 to 12.67 (drop S1 via `D_warm(13)/13`), 13.99 to 14.07 (drop S2), 5.32 to 5.37 (drop S3), 27.84 (direct), 28.51 to 28.52 (rigorous shortcut). All reproduced.
- **Step 7 non-graded Sec 5-6 context:** Merchants' own share of 2027 movement = 44.9% (44.7% stated); empirical rescaled Schedule C tier-change rates = 14.4% scheduled vs 10.1% with designated sources removed (14.5% vs 10.1% stated, crossing cleanly below the 12% cap).

## Evidence 2: Blind Fork Audit (38 Forks Run Across All Classes)

All 5-source calls are denoted `E/R/R/R/M` for Label revisions / Feature releases / Optimisation noise / Training data / Retunes.

| # | Class | Fork Tested | Computed Figure(s) | In Band? | Call | Adjudication / Refutation |
|---|---|---|---|---|---|---|
| 1 | Population/Weighting | Dec 2027 planned book weights (`Book` sheet) | opt 6.84, td 6.75, rel 7.04, lab 9.79, ret 4.29, yr 16.01, pin 35.4% | Yes (all 7) | E/R/R/R/M | Covered by bands; Standard Sec 3.1 pins latest closed snapshot |
| 2 | Population/Weighting | Monitoring panel counts at 2026-09-21 | opt 6.85, td 6.82, rel 7.06, lab 9.81, ret 4.29, yr 16.06, pin 35.5% | Yes (all 7) | E/R/R/R/M | Covered by bands |
| 3 | Population/Weighting | Equal 1/14 weights across families | opt 7.04, td 8.28, rel 7.23, lab 9.85, ret 4.28, yr 16.90, pin 34.8% | No (td, rel, yr) | E/R/R/E/M | Disallowed by Standard Sec 3.1 (must weight by scored merchants) |
| 4 | Population/Weighting | Book-weighted pinned share (2026-09-21 book) | pin 35.3% | Yes | E/R/R/R/M | Covered by pinned band (32.4 to 38.3%) |
| 5 | Pair Dispersion | Sample variance `ddof=1` across pair merchants | opt 6.86, td 6.83, rel 7.06, lab 9.82, ret 4.29 | Yes (all 5) | E/R/R/R/M | Covered by bands |
| 6 | Pair Dispersion | Uncentered mean-square difference `mean(diff^2)` | opt 6.86, td 6.83, rel 7.06, lab 9.82, ret 4.29 | Yes (all 5) | E/R/R/R/M | Covered by bands |
| 7 | Calendar/Window | Settled start `max(first_warm + 13w, Oct 2025)` | opt 6.85 | Yes | E/R/R/R/M | Covered by band |
| 8 | Calendar/Window | Settled start `last_cold + 13w` (no Oct floor) | opt 6.76 | Yes | E/R/R/R/M | Covered by band |
| 9 | Calendar/Window | Settled start `last_cold + 26w` | opt 6.83 | Yes | E/R/R/R/M | Covered by band |
| 10 | Calendar/Window | Settled start 2026 only (`2026-01-05+`) | opt 6.95 | Yes | E/R/R/R/M | Covered by band |
| 11 | Calendar/Window | Calendar 2027 Mondays (`01-04` to `12-27`) for pinned share | pin 36.6% | Yes | E/R/R/R/M | Covered by band; Standard Sec 2.2 pins `2026-12-28` to `2027-12-20` |
| 12 | Calendar/Window | Roadmap `quarter` column instead of `target_refresh` date | rel 6.65; Q2 16.62 | No (rel, Q2) | E/R/R/R/M | Invalid calendar alignment: `FR-27-08` (29 Mar) ships 7 days after 22 Mar Q1 snapshot (violates Schedule C C2.1 / Standard Sec 3.2) |
| 13 | Calendar/Window | Projected exact 28-day retune counts per Q (`[3,3,3,4]` etc.) | Q1 16.89, Q2 17.07, Q3 15.50, Q4 14.69, yr 16.07 | Yes (all 5) | E/R/R/R/M | Covered by bands |
| 14 | Step 3 (Opt Noise) | Lag horizons `1..13`, `1..18`, `1..20`, `1..22` | opt 6.83, 6.85, 6.85, 6.86 | Yes | E/R/R/R/M | Covered by band |
| 15 | Step 3 (Opt Noise) | Lag-2 start (`h = 2..25`) | opt 6.73; Q1-Q4/yr all in band | Yes | E/R/R/R/M | Covered by bands |
| 16 | Step 3 (Opt Noise) | Weights `1/D_warm^2`, `1/y`, flat OLS (`w=1`) | opt 6.84, 6.84, 6.96; Q1-Q4/yr all in band | Yes | E/R/R/R/M | Covered by bands |
| 17 | Step 3 (Opt Noise) | Anchored fit WITHOUT subtracting `D_data(h)` | opt 6.68; Q1-Q4/yr all in band | Yes | E/R/R/R/M | Covered by bands (confirms S1 independence from S2) |
| 18 | Step 3 (Opt Noise) | `D_warm(h)` week-averaged MSD / week-averaged variance / balanced survivors / pooled single `phi` | opt 6.86, 6.86, 6.91, 6.80 | Yes | E/R/R/R/M | Covered by band |
| 19 | Step 3 Rival | Unanchored raw warm-curve fit (free `A, phi, b`) | opt 9.20 | No | E/R/E/R/M | Empirically refuted: implies replicate variance 33.12 vs 22.62 measured in 84 replicate pairs |
| 20 | Step 3 Rival | Linear accumulation (`13*rep/2` or `13*rep`) or single replicate | opt 12.13 / 17.15 / 4.76 | No | E/R/E or M/R/M | Empirically refuted: `D_warm(1)` discrepancy 12.62; warm lag 8-25 intercept 75.5 (min 41.3); cold era linear (curv -0.011 vs warm -0.169) |
| 21 | Step 4 (Train Data) | Grouped `lambda` by window length (52w/104w) or single pooled `lambda` | td 6.82, 6.81 | Yes | E/R/R/R/M | Covered by band |
| 22 | Step 4 (Train Data) | Fitting objectives: linear OLS, relative WLS, ratio scale, arith-mean scale | td 6.84, 6.82, 6.83, 6.83 | Yes | E/R/R/R/M | Covered by band |
| 23 | Step 4 (Train Data) | Free intercept `c0` in `Var_boot(t) = c0 + row2*S(t, lam)` | td 6.77 (`bw_c0 = 25.15` vs `bw_rep = 22.62`) | Yes | E/R/R/R/M | Covered by band and confirms replicate noise sits inside bootstrap pairs |
| 24 | Step 4 Rival | No replicate netting on bootstrap (`c0 = 0`) | td 7.34 | No | E/R/R/R/M | Call unchanged; refuted structurally (independent seeds `same_seed=0`) and empirically (13/14 families worse fit, raw log-RMSE 0.0542 vs 0.0382, paired `t=3.28`, `p=0.0060`) |
| 25 | Step 4 Rival | Alternative kernels: Gaussian, power-law `(a+1)/(a+4)/(a+10)`, linear ramp | td 6.30, 7.82/7.51/7.31, 5.77 | No | E/R/R/R/M | Call unchanged; disallowed by Standard Sec 1.6 ("exponential recency weighting") and strictly worse log-RMSE (0.0555 to 0.0771 vs 0.0494) |
| 26 | Step 4 Rival | Uniform window turnover (`lambda=1`) or unscaled raw/net bootstrap | td 3.61-3.65 / 10.21 / 9.04 | No | E/R/R/M or E/M | Refuted by Standard Sec 1.6, 3.8x worse log-RMSE (0.1881 vs 0.0494), and 2026 contrast (-0.67 vs 10.88 observed) |
| 27 | Step 5 (Releases) | Direct empirical cov, pooled corr, per-(family, group) var/cov, include cross-group cov | rel 7.06, 7.07, 7.06, 7.06 | Yes | E/R/R/R/M | Covered by band |
| 28 | Step 5 (Releases) | Independent live probabilities `P_live(t_i)*P_live(t_j)` instead of `P_live(max)` | rel 6.92; Q1-Q4/yr all in band | Yes | E/R/R/R/M | Covered by bands |
| 29 | Step 5 Rival | Orthogonal releases (`c=0`, model live or planned dates) | rel 4.70 / 1.96 | No | E/M/R/R/M | Empirically refuted: 141/141 same-group pairs have corr > 0 (mean 0.783, min 0.702); cov 0.00 vs 4.80 observed |
| 30 | Step 5 Rival | Perfectly aligned across all groups (`c=1` all pairs) | rel 11.10 | No | E/E/R/R/M | Empirically refuted: 2,580 cross-group pairs average corr -0.001 |
| 31 | Step 5 (Pinned) | Linear OLS lag (Normal CDF) / Direct `log(total_lag) ~ c` / Grouped by `n_comp` | pin 34.6%, 34.8%, 34.8%; rel 7.02, 7.06, 7.05 | Yes | E/R/R/R/M | Covered by bands |
| 32 | Step 5 (Pinned) | Family-own mean lag & slip / Pooled lag (ignore `n_comp`) / Plug-in medians | pin 34.7%, 35.0%, 35.6%; rel 6.94, 7.12, 7.05 | Yes | E/R/R/R/M | Covered by bands |
| 33 | Step 5 (Pinned) | Weibull AFT MLE / Gamma log-link MLE / Non-parametric empirical residual CDF | pin 34.5%, 34.7%, 34.8%; rel 7.05, 7.06, 7.05 | Yes | E/R/R/R/M | Covered by bands |
| 34 | Step 5 (Pinned) | Add `epochs_per_refresh` covariate / Rollout fixed-effects avg / Convolved slip dist | pin 34.8%, 34.8%, 34.8%; rel 7.07, 7.06, 7.06 | Yes | E/R/R/R/M | Covered by bands |
| 35 | Step 5 (Pinned) | No reverts (`rev=0`) / All-post-adoption reverts / Per-family revert rates | pin 37.2%, 36.5%, 34.6%; rel 6.90, 6.95, 7.05; Q1-Q4/yr in band | Yes | E/R/R/R/M | Covered by bands |
| 36 | Hygiene Edge Case | Skip Tolka Pay ID migration | opt 6.85 | Yes | E/R/R/R/M | Covered by band |
| 37 | Hygiene Edge Case | Keep earlier `load_id` or average duplicate `load_id`s on re-sent refreshes | opt 6.81, 6.84 | Yes | E/R/R/R/M | Covered by band |
| 38 | Hygiene Edge Case | Skip JSONL `run_id` deduplication | pin 34.8%, rel 7.06 | Yes | E/R/R/R/M | Covered by bands |

## Non-Blocking Audit Notes

1. **Instrument shadow JSONL `seed` field:** In `training_scheduler_runs_2024_2026.jsonl`, `retune_shadow`, `release_shadow`, and `label_freeze` log distinct `seed` integers for `run_a` and `run_b`, yet their observed pair variances in `mrm_instrument_pair_scores_2026.csv` (`5.67`, `6.15`, `7.41` pts^2) are 3x to 4x smaller than `replicate` (`22.62` pts^2), proving directly from the data that those isolated shadow counterfactuals carry no replicate variance (subtracting `22.62` yields negative variances). Conversely, `bootstrap` (`104.34` pts^2) empirically carries full `rep_f` variance (`free_c0 = 25.15` vs `22.62`, `p = 0.0060`). No fork is opened.
2. **Step 6 contrast window:** Step 6 describes contrast `(ii)` (`10.88` pts^2) as the high-minus-low trailing-volume bootstrap net-variance contrast; an 8-week trailing-volume split reproduces `10.88` exactly (`10.8755`). Because Step 6 is a supporting internal diagnostic (not a graded prompt ask) and every trailing window length (4w, 8w, 13w, 26w) produces the same decisive rejection of the uniform-window rival, no edit is needed.
