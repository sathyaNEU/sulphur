Manifest MD5s: `prompt.txt` = `87d87a3a4f60b8c80dd1ca85e4a4f09b` | `target.zip` = `af46269ad25af6a97feac06037864f68` | `submission.md` = `0ee70e42d00b4d66be31fa8bbcc4ae38`

# Holistic Audit v4 (Determinism Mode) Report: `task27` (Pass 2)

- **Verdict:** `DETERMINISTIC`
- **Disposition:** `APPROVE`
- **Audit Scope:** Pass 2 fresh Holistic Audit v4 Step 0, Part A, and Part B, plus Gates A to E supplement after `target.zip` refresh (`af46269ad25af6a97feac06037864f68`; `prompt.txt` and `submission.md` unchanged). Parts C and D remain deferred to `holistic` mode after platform runs are saved.
- **Workspace:** `/tmp/holistic-task27-determinism-3urqekjw` (17 freshly unzipped input files audited in isolation via `python3 -I` scripts under `work/`).

## Holistic Audit v4 Part A / Part B Summary Lines

- `correctness: correct`
- `figures_checked: 37 (committed FUND/DEFER slate, 6 corridor 2027 BCRs, 6 corridor avoidable EUR, funded capital/unspent/avoidable/portfolio BCR, network avoidable EUR, C1/C2/C3 totals and peak-corridor shares, direct CHED rail siblings, 2026 and 2027 attributed carrier-controllable c-days, raw TMS naive BCRs, Layer 1 record counts, all 8 timestamp/free-time windows including zero-excess EDI and dock rows, stock-flow conservation controls, raw diagnostic gaps)`
- `mismatches: 0 material mismatches (same benign 0.1 display-rounding note on 7,436.9 + 4,304.4 + 7,171.5 = 18,912.8 vs unrounded sum 18,912.7; zero numerical regressions from target.zip refresh)`
- `decision_reproduces: yes`
- `determinism: pinned`
- `unpinned_forks: none (0/38 honest forks and 0/14 +/-15% stress tests flip the FUND/DEFER slate; 0/38 honest forks show greedy vs exact 0-1 integer knapsack divergence)`

---

## Step 0: Pre-flight & Refresh Delta Verification

1. **Golden present (`PASS`):** Final recommendation, all three supplementary answers, all three critical components, and the six-step solution are intact and complete.
2. **Inputs belong to this task (`PASS`):** All 17 files under `/tmp/holistic-task27-determinism-3urqekjw/inputs/` match Weserfrucht Import GmbH Charter RC-2027 Rev 3 (`WF-SCG-RC2027-Rev3`), calendar year 2026 (plus clean January 2027 portal/gate tail through 2027-01-18), and the EUR 1.75 million 2027 budget.
3. **Verification of Pass 2 `target.zip` Refreshes (`PASS`, zero regressions):**
   - **Charter PDF (`weserfrucht_remediation_charter_rc2027.pdf`, 10 pages, full PyMuPDF extraction):**
     - **Section 2.3 (pages 3-4):** Polished operational prose ("actively building stock" vs "drawing down stock"; "lock enforcement varies around train assembly rather than acting as a single uniform network deadline"; "longer port-to-DC loops leave less daily dispatch slack") preserves every governance pin cleanly without prescribing a single econometric equation or opening any ambiguity on what C1, C2 (excluding direct CHED rail siblings), or C3 measure.
     - **Annex D (page 9):** Tightened prose preserves the explicit exclusion of `carrier_dispute_closeout_2026.xlsx` from operational attribution and 2027 funding eligibility ("accounting reference for 2026 invoice reconciliation only and must not be substituted for empirical operational root-cause attribution when sizing 2027 corridor remediation investments").
     - All other governing clauses (Section 1.3 revision/VOID rules, Table 2 free-time windows, Table 3 cause taxonomy, Section 2.2 carrier-controllable scope, Section 3.1 Schedule B tariffs and bunker/Maut exclusion, Section 3.2 Annex C equations, Section 4.1 EUR 1.75M descending-BCR indivisible-package rule, Annex A conservation controls, Annex B full double precision, Annex C.1 two-sided verification standard, Section 5 13-column CSV schema) remain completely intact.
   - **Below-free-time elapsed durations on zero-excess EDI & DC dock rows (`container_milestones_2026.csv`):**
     - `excess_edi_cdays == 0` (`n = 23,175`): `customs_doc_ts_utc - discharge_ts_utc` now spans `1.80h` to `5.85h` (`p25 = 2.81h`, `median = 3.82h`, strictly `<= 6h` free time, `0` negative durations, `max_diff = 0.000011` c-days).
     - `excess_dc_dock_cdays == 0` (`n = 20,394`): `unload_complete_ts_cet - dc_gate_in_ts_cet` now spans `1.20h` to `3.85h` (`p25 = 1.85h`, `median = 2.52h`, strictly `<= 4h` free time, `0` negative durations, `max_diff = 0.000012` c-days).
     - All 8 lifecycle stages verify `max(0, elapsed_hours - free_time) / 24 == excess_*_cdays` with `0` negative durations and `max_diff <= 0.000012` c-days.
     - Zero timezone or conservation regression: `unload_complete_ts_cet` stays strictly within `07:00` to `21:00` local time (`0` date diffs between `Europe/Berlin` and UTC), and portal queue conservation holds identically (`24,000` unloads = `24,000` confirmed bookings, `min Q = 0`, `max Q = 79`, `end Q = 0` across all 12 `(port, line)` pools).
   - **Distractor cleanup (`german_toll_maut_rates_2026_2027.xlsx` & `north_sea_bunker_fuel_index_2026.csv`):**
     - `Port_DC_Autobahn_Distances` in `german_toll_maut_rates_2026_2027.xlsx` now aligns exactly with `haul_distance_km` in `remediation_program_budgets_2027.csv` across all 6 active corridors (`BHV-HAN 155`, `BHV-OSN 175`, `BHV-KAS 295`, `HAM-HAN 150`, `HAM-MAG 255`, `WHV-OSN 165` km), removing the minor cross-file distance discrepancy observed earlier.
     - `north_sea_bunker_fuel_index_2026.csv` (104 weekly rows across Rotterdam and Hamburg) exhibits smooth variation without artificial price floors and remains explicitly excluded by Charter Section 3.1.

---

## Part A: Fresh Independent Reproduction (Zero Regressions)

| Quantity / Control | Pass 2 Independent Value | Author Value / Band | Status |
|---|---|---|---|
| Settled containers / raw / VOID / superseded / vessels | 24,000 / 24,525 / 190 / 335 / 480 | 24,000 / 24,525 / 190 / 335 / 480 | Exact match |
| All-8-cause total excess c-days | 49,447.7663 | 49,447.77 | Exact match |
| WMS cleaned / raw / superseded / German dates / CASE rows (mod 0) | 175,207 / 179,359 / 4,152 / 66,421 / 62,067 | 175,207 / 179,359 / 4,152 / 66,421 / 62,067 | Exact match |
| 12-chamber cold-store conservation max residual (1,460 DC-days) | 0.000000 pallets (whole-DC 70.657% to 77.642%) | Zero residual (70.7% to 77.6%) | Exact match |
| Depot turn-in log raw / superseded / max Stage-8 diff | 25,252 / 445 / 0.000003 c-days | 25,252 / 445 / reconciled | Exact match |
| Portal queue conservation (`Europe/Berlin` & UTC, 383 days) | 24,000 unloads = 24,000 bookings; end Q = 0 | Exact conservation | Exact match |
| Raw S1 filling-vs-draining gap (84%-94%) / Raw S3 open-portal gap | +27.7255h / +53.6855h | +27.73h / +53.69h | Exact match |
| Direct non-sampled CHED rail sibling holds (global baseline) | 895.0671 c-days | 895.1 c-days | Exact match |
| Naive TMS 2027 BCR top 3 (`BHV-KAS`, `HAM-MAG`, `BHV-HAN`) | 2.176, 2.136, 2.012 | 2.176, 2.136, 2.012 | Exact match |
| **C1 (Cold-Store Pull-Back 2026)** | **7,437.5 c-days** (`BHV-KAS` 3,104.9) | **7,436.9** (band 7,172.8 to 7,643.9) | **Agree (+0.01%)** |
| **C2 (BIP Rail Rollover 2026)** | **4,280.9 c-days** (`HAM-MAG` 2,367.9) | **4,304.4** (band 4,086.4 to 4,436.0) | **Agree (-0.55%)** |
| **C3 (Empty-Depot Backlog 2026)** | **7,172.5 c-days** (`BHV-HAN` 3,231.2) | **7,171.5** (band 6,741.5 to 7,279.7) | **Agree (+0.01%)** |
| **WHV-OSN 2027 BCR (FUND)** | **1.141** (EUR 639,100.15; 4,591.5 d) | **1.139** (band 1.109 to 1.159) | **Agree (in band)** |
| **BHV-OSN 2027 BCR (FUND)** | **1.094** (EUR 612,424.33; 3,891.5 d) | **1.100** (band 1.084 to 1.123) | **Agree (in band)** |
| **HAM-HAN 2027 BCR (FUND)** | **1.096** (EUR 641,317.49; 4,453.0 d) | **1.086** (band 1.072 to 1.114) | **Agree (in band)** |
| **HAM-MAG 2027 BCR (DEFER)** | **0.997** (EUR 563,041.71; 3,878.6 d) | **0.988** (band 0.974 to 1.020) | **Agree (in band)** |
| **BHV-HAN 2027 BCR (DEFER)** | **0.944** (EUR 542,743.72; 3,727.1 d) | **0.949** (band 0.920 to 1.061) | **Agree (in band)** |
| **BHV-KAS 2027 BCR (DEFER)** | **0.898** (EUR 511,711.14; 3,480.5 d) | **0.901** (band 0.885 to 0.920) | **Agree (in band)** |
| Funded Slate / Capital / Avoidable EUR | **WHV-OSN, BHV-OSN, HAM-HAN** / EUR 1,705,000 / EUR 1,892,841.96 | **WHV-OSN, BHV-OSN, HAM-HAN** / EUR 1,705,000 / EUR 1,889,111.37 | **Agree (+0.20%)** |

---

## Part B: Fresh Fork Battery, Rivals, Stress Tests, & Hygiene

### B.1 Honest Fork Battery (38 Distinct Specifications Executed in Code)

Across all 38 freshly executed honest specifications spanning S1 (OLS, Gamma-IRLS, non-parametric bins, spline, Huber, Port-day FE, Corridor-week FE, hinges 0.76/0.80, opening util, `net_flow >= 0`, refreshed `customs_date` join with 738 date diffs, additive split), S2 (Poisson-ID logistic, Port OLS, Pooled OLS, hard-step cuts, observed `locked_obs` Poisson-ID and OLS, `rolled_days` target, corridor/full/zero CHED sibling baselines), S3 (DC-7d-week, DC-ISO-week, DC-day, Port-day, Corridor-week, Huber, non-parametric `Q_days` bins, haul-distance parametric, lagged `Q_sod`, mid-day `Q_mid`, active-days denominator, additive split), joint simultaneous alternatives (`JOINT_Sp_Pois_DCd`, `JOINT_NP_ObsP_PD`, `JOINT_Add_ObsO_Add`), and intermediate rounding:

- **Funding slate flips:** **0 / 38** (100% select `WHV-OSN`, `BHV-OSN`, `HAM-HAN` as `FUND` and `HAM-MAG`, `BHV-HAN`, `BHV-KAS` as `DEFER`).
- **Greedy vs Exact 0-1 Integer Knapsack disagreements:** **0 / 38**.
- **Key highlighted Pass 2 fork checkpoints:**
  - `Primary`: `#3 BHV-OSN (1.094)` vs `#4 HAM-MAG (0.997)`, gap `+0.097`.
  - `S1_CustomsDate` (exercising refreshed EDI timestamps): `C1 = 7,368.9`, `#3 HAM-HAN (1.100)` vs `#4 HAM-MAG (0.999)`, gap `+0.101`.
  - `S2_ObsPois`: `C2 = 4,421.1` (in band), `#3 HAM-HAN (1.082)` vs `#4 HAM-MAG (0.985)`, gap `+0.096`.
  - `S2_ObsOLS`: `C2 = 4,583.9`, `#3 HAM-HAN (1.063)` vs `#4 HAM-MAG (0.967)`, gap `+0.096` (non-blocking note unchanged from Pass 1).
  - `S3_NPBins`: `C3 = 7,141.9` (in band), `#3 BHV-OSN (1.094)` vs `#4 HAM-MAG (0.996)`, gap `+0.097`.
  - `S3_DistParam` (budgets/Maut unified km): `C3 = 6,832.2`, `#3 BHV-OSN (1.097)` vs `#4 BHV-HAN (1.033)`, gap `+0.065`.
  - `JOINT_Sp_Pois_DCd`: `C1 = 7,413.2`, `C2 = 4,280.9`, `C3 = 7,161.9`, `#3 HAM-HAN (1.096)` vs `#4 HAM-MAG (0.998)`, gap `+0.098` (all 9 metrics in band).
  - `JOINT_NP_ObsP_PD`: `C1 = 7,423.1`, `C2 = 4,421.1`, `C3 = 7,172.8`, `#3 HAM-HAN (1.076)` vs `#4 HAM-MAG (0.984)`, gap `+0.092` (all 9 metrics in band).
  - `JOINT_Add_ObsO_Add` (extreme edge): `C1 = 7,002.6`, `C2 = 4,583.9`, `C3 = 6,632.2`, `#3 HAM-HAN (1.086)` vs `#4 BHV-HAN (1.000)`, gap `+0.086`.
  - Minimum `#3 - #4` BCR gap across all 38 forks (including `S2_SibZero` which drops direct CHED siblings): `+0.0157` (and `+0.049` to `+0.101` across all Charter-compliant honest specs).

### B.2 Rivals, Stress Tests, Vocabulary, & Giveaways

- **Single-mechanism omission reversals confirmed identically on refreshed inputs:**
  - Naive TMS: `BHV-KAS (2.176)`, `HAM-MAG (2.136)`, `BHV-HAN (2.012)` (3/3 wrong).
  - Drop S1: flips to `BHV-KAS (1.842)`, `BHV-OSN (1.562)`, `WHV-OSN (1.461)`.
  - Drop S2 (+ direct CHED siblings): flips to `HAM-MAG (1.720)`, `HAM-HAN (1.501)`, `WHV-OSN (1.175)`.
  - Drop S3: flips to `BHV-HAN (1.690)`, `WHV-OSN (1.412)`, `BHV-OSN (1.226)`.
- **Parameter stress tests (`+/-15%` across C1, C2, C3, 2027 volume growth delta, and all three Schedule B tariffs; 14 scenarios):** **0 / 14 flips**.
- **Gate B vocabulary grep across all 17 refreshed files:** **0 missing terms** (100% of operational and action terms in Final Recommendation appear verbatim in the refreshed package).
- **Giveaways sweep across all 17 refreshed files:** **0 giveaway hits**.

---

## Gates A through E Supplement (Pass 2)

- **Gate A (Solution Correctness):** **PASS** (zero regressions; all 8 timestamp windows including realistic below-free-time EDI/dock durations reconcile within `1.2e-5` c-days; all conservation checks and attribution figures reproduce cleanly).
- **Gate B (Every Decisive Fact Present & Grounded Vocabulary):** **PASS** (refreshed Charter Section 2.3 and Annex D retain every required rule and definition cleanly; unified corridor distances across budgets CSV and Maut XLSX; 0 missing action terms).
- **Gate C (Uniquely Forced & Margin-Robust):** **PASS** (0/38 honest fork flips, 0/14 stress flips, 0/38 greedy-vs-knapsack discrepancies; every call-flipping rival refuted by Charter rules and Annex C.1 diagnostics).
- **Gate D (Analytical Hardness, Not Semantics):** **PASS** (prompt and Charter objectives align; refreshed prose removes mechanical hints without introducing semantic ambiguity).
- **Gate E (Unambiguous Prompt on Decision, Open on Method):** **PASS** (prompt unchanged; pins the funding decision, BCRs, three non-carrier volumes, and three deliverables while leaving estimation methods open).

---

## Fix

- **Fix:** None required (`DETERMINISTIC` / `APPROVE`). The refreshed `target.zip` (`af46269ad25af6a97feac06037864f68`) improves surface realism cleanly with zero correctness or determinism regressions; `task27` is cleared for platform submission.
- **Carry-forward non-blocking notes for future Part C rubric grading:** (1) Do not penalize intra-tier rank swaps between funded `#2/#3` (`BHV-OSN` vs `HAM-HAN`) or deferred `#4/#5` (`HAM-MAG` vs `BHV-HAN`) when `FUND`/`DEFER` decisions match and corridor BCRs sit within defensible bands; (2) Note that `locked_obs` Poisson-ID MLE lands inside the stated C2 band (`4,421.1`) while unweighted `locked_obs` OLS reaches `4,583.9` with zero funding flip.
