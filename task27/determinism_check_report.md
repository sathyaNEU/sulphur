Manifest MD5s: `prompt.txt` = `87d87a3a4f60b8c80dd1ca85e4a4f09b` | `target.zip` = `0ffcae3e4f8de53a1cccff371b1e0428` | `submission.md` = `0ee70e42d00b4d66be31fa8bbcc4ae38`

# Holistic Audit v4 (Determinism Mode) Report: `task27`

- **Verdict:** `DETERMINISTIC`
- **Disposition:** `APPROVE`
- **Audit Scope:** Holistic Audit v4 Step 0, Part A, and Part B, plus Gates A to E supplement (pre-platform determinism pass; Parts C and D are deferred to `holistic` mode after platform runs are saved).
- **Workspace:** `/tmp/holistic-task27-determinism-cfyfh2es` (17 shipped input files verified in isolation via `python3 -I` scripts under `work/`).

## Holistic Audit v4 Part A / Part B Summary Lines

- `correctness: correct`
- `figures_checked: 37 (committed FUND/DEFER slate, 6 corridor 2027 BCRs, 6 corridor avoidable EUR, funded budget/unspent/avoidable/portfolio BCR, network avoidable EUR, C1/C2/C3 totals and peak-corridor shares, direct CHED rail siblings, 2026 and 2027 attributed carrier-controllable c-days, raw TMS naive BCRs, Layer 1 record counts and stock-flow conservation controls, raw diagnostic gaps)`
- `mismatches: 0 material mismatches (1 benign 0.1 display-rounding note on 7,436.9 + 4,304.4 + 7,171.5 = 18,912.8 vs unrounded sum 18,912.7; all model-estimated figures sit within 0.01% to 0.55% of independent first-principles derivations and inside stated 21-variant bands)`
- `decision_reproduces: yes`
- `determinism: pinned`
- `unpinned_forks: none (0/41 honest forks and 0/14 +/-15% stress tests flip the FUND/DEFER slate; 0/41 honest forks show greedy vs exact 0-1 integer knapsack divergence)`

---

## Step 0: Pre-flight

1. **Golden present (`PASS`):** Final recommendation, all three supplementary answers, all three critical components, and the six-step solution are present and state concrete computed values (no placeholder prose).
2. **Inputs belong to this task (`PASS`):** All 17 files in `inputs/` belong coherently to Weserfrucht Import GmbH under Charter RC-2027 Rev 3 (`WF-SCG-RC2027-Rev3`, effective 18 November 2026), covering calendar year 2026 (plus clean January 2027 empty-return tail through 2027-01-18), 3 North Sea ports (`BHV`, `HAM`, `WHV`), 4 inland cold-store DCs (`HAN`, `OSN`, `KAS`, `MAG`), 6 corridors (`BHV-HAN`, `BHV-KAS`, `BHV-OSN`, `HAM-HAN`, `HAM-MAG`, `WHV-OSN`), 4 ocean lines (`LINE_A` to `LINE_D`), Nordbahn Intermodal rail shuttles, EU TRACES-NT BIP notices, and the EUR 1.75 million 2027 carrier-remediation budget.

---

## Part A: Solution Correctness

### A.1 Independent Layer 1 Cleaning & Physical Conservation Verification

All 17 input files were parsed directly from `/tmp/holistic-task27-determinism-cfyfh2es/inputs/` (including full PDF text and table extraction of `weserfrucht_remediation_charter_rc2027.pdf` via PyMuPDF and full sheet/formula extraction of both `.xlsx` workbooks via `openpyxl`) before comparing against the author's claims:

| Control / File | Independent Code Computation | Author Value | Status |
|---|---|---|---|
| `container_milestones_2026.csv` raw rows | 24,525 | 24,525 | Exact match |
| `record_status = VOID` excluded (0 overlap with SETTLED) | 190 | 190 | Exact match |
| Superseded `extract_version` removed (retain max per `container_id`) | 335 | 335 | Exact match |
| Settled 2026 containers / vessels / corridors / ocean lines | 24,000 / 480 / 6 / 4 (18,500 RAIL, 5,500 TRUCK) | 24,000 / 480 / 6 / 4 | Exact match |
| Sum of 8 `excess_*_cdays` vs `excess_cdays_total` & timestamps | 49,447.7663 c-days (max timestamp diff 1.2e-5) | 49,447.77 c-days | Exact match |
| Raw TMS 3 carrier-channel stages sum (Stage 3 + Stage 5 + Stage 7) | 16,181.913 + 10,617.769 + 14,569.195 = 41,368.878 | 41,368.88 (implied) | Exact match |
| Naive TMS 2027 BCR top 3 (`BHV-KAS`, `HAM-MAG`, `BHV-HAN`) | 2.1765, 2.1363, 2.0116 | 2.176, 2.136, 2.012 | Exact match |
| `warehouse_pallet_movements_2026.csv` raw / superseded removed | 179,359 / 4,152 (175,207 cleaned) | 179,359 / 4,152 | Exact match |
| WMS German `DD.MM.YYYY` dates / `CASE` rows / legacy stores mapped | 66,421 / 62,067 (max mod remainder 0) / 21,523 | 66,421 / 62,067 / 21,523 | Exact match |
| 12-chamber conservation vs `coldstore_inventory_daily_2026.csv` | Max abs residual = 0.0 pallets across all 1,460 DC-days | Exact zero residual | Exact match |
| Whole-DC occupancy range vs chamber utilization range | 70.657% to 77.642% (chambers: 44.352% to 98.696%) | 70.7% to 77.6% | Exact match |
| `depot_turnin_log_2026.csv` raw / superseded / legacy carriers mapped | 25,252 / 445 / 5,530 (max diff vs Stage 8 = 2.5e-6) | 25,252 / 445 / 5,530 | Exact match |
| `depot_portal_requests_2026.csv` queue conservation (383 days to 2027-01-18) | 24,000 unloads = 24,000 confirmed; min Q = 0; end Q = 0 | Exact conservation | Exact match |
| `customs_consignment_bol_2026.csv` / `bip_inspection_notices_2026.jsonl` / `rail_shuttle_departures_2026.csv` | 24,000 BOL (6,700 CHED lots) / 1,250 BIP lots / 732 shuttles | 1,250 BIP lots / 732 shuttles | Exact match |
| Direct non-sampled CHED rail sibling holds above baseline (`0.025043` c-days) | 962.1336 - 2,678 x 0.025043 = 895.067 c-days | 895.1 c-days | Exact match |
| Raw S1 filling-vs-draining gap at 84% to 94% chamber util | +27.7255 hours (39.377h vs 11.652h) | +27.73 hours | Exact match |
| S2 continuous notice lead hours (`scheduled_departure - exam_notice`) | 1.50h to 72.00h (zero dead zones) | 1.5h to 72h | Exact match |
| Raw S3 open-portal high-queue (`>=0.8`) vs low-queue (`<0.15`) gap (2026 mean denom) | +53.6855 hours | +53.69 hours | Exact match |
| `WHV-OSN` unconstrained `LINE_C` + `LINE_D` share | 72.324% | 72.3% | Exact match |

### A.2 Independent Derivation of Deciding Attribution & 2027 Corridor Figures

Because Charter RC-2027 Section 2.3 explicitly leaves the econometric functional form open (requiring empirical estimation from the 2026 logs verified by two-sided residual diagnostics under Annex C.1), we derived C1, C2, and C3 from first principles using multiple independent standard estimators (non-parametric bins, splines, Gamma-ID IRLS, within-vessel OLS, Poisson-ID count MLE, observed booked-slot locking, DC-week/DC-day/Port-day FE) and compared our primary independent reproduction (Vessel FE convex non-negative S1 + Profiled Poisson-ID logistic S2 + DC-7d-week FE S3) and joint alternative models against the author's figures and stated 21-variant bands:

| Deciding Quantity | Independent Derivation (Primary) | Independent Alt Range (Core Honest Specs) | Author Value | Author 21-Variant Band | Status |
|---|---|---|---|---|---|
| **Funded Slate (EUR 1.75M cap)** | **WHV-OSN, BHV-OSN, HAM-HAN** | Identical (41/41 honest forks) | **WHV-OSN, BHV-OSN, HAM-HAN** | Zero flips | **Agree** |
| **Deferred Slate** | **HAM-MAG, BHV-HAN, BHV-KAS** | Identical (41/41 honest forks) | **HAM-MAG, BHV-HAN, BHV-KAS** | Zero flips | **Agree** |
| Funded Capital / Contingency Reserve | EUR 1,705,000.00 / EUR 45,000.00 | Identical (41/41) | EUR 1,705,000.00 / EUR 45,000.00 | Fixed | **Exact match** |
| **C1 (Cold-Store Pull-Back 2026)** | **7,437.5 c-days** (`BHV-KAS` 3,104.9) | 7,251.8 to 7,524.7 (NP bins 7,423.1; Gamma-IRLS 7,434.8) | **7,436.9 c-days** (`BHV-KAS` 3,104.9) | 7,172.8 to 7,643.9 | **Agree (+0.01%)** |
| **C2 (BIP Rail Rollover 2026)** | **4,280.9 c-days** (`HAM-MAG` 2,367.9) | 4,252.6 to 4,421.1 (Pure-regime GT 4,311.6; Port OLS 4,319.1) | **4,304.4 c-days** (`HAM-MAG` 2,399.7) | 4,086.4 to 4,436.0 | **Agree (-0.55%)** |
| **C3 (Empty-Depot Backlog 2026)** | **7,172.5 c-days** (`BHV-HAN` 3,231.2; 45.4% open) | 7,141.9 to 7,226.0 (DC-day 7,161.9; Port-day 7,172.8) | **7,171.5 c-days** (`BHV-HAN` 3,231.2; 45.4% open) | 6,741.5 to 7,279.7 | **Agree (+0.01%)** |
| Direct CHED Rail Sibling Holds | **895.1 c-days** | 894.2 (corridor base) to 895.1 (global base) | **895.1 c-days** | Exact | **Exact match** |
| 2026 Attributed Carrier-Ctrl Days | 21,583.0 c-days | 21,391.9 to 21,600.0 | 21,561.1 c-days | In envelope | **Agree (+0.10%)** |
| 2027 Projected Carrier-Ctrl Days | 24,022.3 c-days | 23,804.8 to 24,034.1 | 23,995.1 c-days | In envelope | **Agree (+0.11%)** |
| **WHV-OSN 2027 BCR (FUND)** | **1.141** (EUR 639,100.15 / 560,000) | 1.125 to 1.154 | **1.139** (EUR 637,950.34 / 560,000) | 1.109 to 1.159 | **Agree (in band)** |
| **BHV-OSN 2027 BCR (FUND)** | **1.094** (EUR 612,424.33 / 560,000) | 1.084 to 1.111 | **1.100** (EUR 615,997.26 / 560,000) | 1.084 to 1.123 | **Agree (in band)** |
| **HAM-HAN 2027 BCR (FUND)** | **1.096** (EUR 641,317.49 / 585,000) | 1.073 to 1.100 | **1.086** (EUR 635,163.77 / 585,000) | 1.072 to 1.114 | **Agree (in band)** |
| **HAM-MAG 2027 BCR (DEFER)** | **0.997** (EUR 563,041.71 / 565,000) | 0.973 to 0.998 | **0.988** (EUR 558,284.17 / 565,000) | 0.974 to 1.020 | **Agree (in band)** |
| **BHV-HAN 2027 BCR (DEFER)** | **0.944** (EUR 542,743.72 / 575,000) | 0.935 to 1.051 | **0.949** (EUR 545,525.14 / 575,000) | 0.920 to 1.061 | **Agree (in band)** |
| **BHV-KAS 2027 BCR (DEFER)** | **0.898** (EUR 511,711.14 / 570,000) | 0.898 to 0.918 | **0.901** (EUR 513,592.47 / 570,000) | 0.885 to 0.920 | **Agree (in band)** |
| Funded Avoidable EUR / Portfolio BCR | EUR 1,892,841.96 / 1.110 | EUR 1,874,820 to 1,894,389 / 1.100 to 1.111 | EUR 1,889,111.37 / 1.108 | In envelope | **Agree (+0.20%)** |
| Network 2027 Avoidable EUR | EUR 3,510,338.53 | EUR 3,482,635 to 3,514,556 | EUR 3,506,513.15 | In envelope | **Agree (+0.11%)** |

### A.3 Internal Consistency & Step-by-Step Self-Rebuilding Audit

1. **Cross-block consistency (`PASS`):** Every figure stated in Final Recommendation, Supplementary Questions, Critical Components, and Step-by-Step matches identically across all four blocks:
   - Funded budgets: `560,000 + 560,000 + 585,000 = 1,705,000.00` (unspent `45,000.00`).
   - Funded avoidable EUR: `637,950.34 + 615,997.26 + 635,163.77 = 1,889,111.37`; `1,889,111.37 / 1,705,000.00 = 1.107983 -> 1.108`.
   - Network avoidable EUR: `1,889,111.37 + 558,284.17 + 545,525.14 + 513,592.47 = 3,506,513.15`.
   - Sum of 2027 carrier-controllable c-days: `4,583.5 + 3,917.2 + 4,408.9 + 3,843.7 + 3,747.5 + 3,494.3 = 23,995.1`.
   - Each corridor's BCR matches `avoidable_eur / budget_eur` to 3 decimal places (`1.139197`, `1.099995`, `1.085750`, `0.988114`, `0.948739`, `0.901039`), and every budget matches `remediation_program_budgets_2027.csv`.
   - Minimum 4-corridor subset budget: `560,000 + 560,000 + 565,000 + 570,000 = 2,255,000` (exact match).
   - Exact 0-1 integer knapsack on the author's avoidable EUR selects `('WHV-OSN', 'BHV-OSN', 'HAM-HAN')` at EUR 1,889,111.37 (leading the next-best feasible 3-corridor bundle `WHV-OSN, HAM-HAN, HAM-MAG` at EUR 1,831,398.28 by EUR 57,713.09).
   - **Minor display-rounding note (benign):** Displayed 1-decimal components `7,436.9 + 4,304.4 + 7,171.5 = 18,912.8`, whereas the displayed total is `18,912.7` (consistent with unrounded double-precision summation under Charter Annex B, confirmed by `41,368.878 - 18,912.7 - 895.1 = 21,561.08 -> 21,561.1`).
2. **Step-by-Step reproducibility & minor specification notes (`PASS`):**
   - Following Step 2 (S1) with non-negative pull-back slopes reproduces `C1 = 7,437.5` and `BHV-KAS = 3,104.93` (within 0.6 c-days of `7,436.9` and 0.03 c-days of `3,104.9`). Controlling for vessel FE and corridor baseline, the residual 84% to 94% filling-vs-draining gap collapses from `+32.35h` to `-0.06h` (and `+0.002h` under a multiplicative clean port-congestion base), matching the author's `0.08h` claim. (Note: the unadjusted pooled 84% to 94% residual gap is `-1.99h` because draining days in that band occur at +1.3 to +2.7 percentage points higher genuine port yard utilization `reefer_yard_util_pct` and higher `BHV-OSN` mix.)
   - Following Step 3 (S2) reproduces port-specific cutoffs (`BHV` 14-15.8h, `HAM` 26-27.5h, `WHV` 9-10h), mean BIP pass-through slope ~`0.65-0.68` (`0.685` at `tau=3.0`), and `C2 = 4,280.9 to 4,343.7` bracketing `4,304.4` (and matching our pure-regime out-of-sample ground-truth calculation of `4,311.6` c-days!).
   - Following Step 4 (S3) with 7-day `dc_week` FE reproduces `C3 = 7,172.5`, `BHV-HAN = 3,231.23`, open-portal share `45.44%`, and within-FE residual open-portal drain gap `+0.31h` (author: `7,171.5`, `3,231.2`, `45.4%`, `0.28h`).
   - Step 6 mentions an internal composite metric `fal_err = 36.3 vs 300.9 to 1,725.3` without giving its formula in prose; this is an internal summary label only and does not affect any deciding figure, as our independent Annex C.1 residual checks confirm the exact same massive separation between honest models and every rival.
3. **Verification of Step 6 rival & stress claims (`PASS`):**
   - Naive TMS: reproduced exact `BHV-KAS 2.176`, `HAM-MAG 2.136`, `BHV-HAN 2.012`.
   - Drop S1 alone: reproduced `BHV-KAS 1.852` (author `1.845`), funding `BHV-KAS, BHV-OSN, WHV-OSN`.
   - Drop S2 (+ direct CHED siblings): reproduced `HAM-MAG 1.714` (author `1.720`; dropping rollover C2 only gives `1.616`, still flipping to `HAM-MAG`), funding `HAM-HAN, HAM-MAG, WHV-OSN`.
   - Drop S3 alone: reproduced `BHV-HAN 1.708` (author `1.695`), funding `BHV-HAN, BHV-OSN, WHV-OSN`.
   - Partial shortcuts and over-corrections: Binary `>=92%` S1 (`C1 = 3,668-4,410`, mis-funds `BHV-KAS` at `1.334`); Fixed-24h bivariate S2 omitting consist cuts (`C2 = 7,500`, crashes `HAM-HAN` to `0.650`); Binary unload-day portal flag S3 (`C3 = 3,314`, lifts `BHV-HAN` to `1.383`); S1 over-subtract (`BHV-OSN = 0.741` vs author `0.739`); S2 over-subtract (`HAM-HAN = 0.483` vs author `0.488`).
   - Parameter stress tests: All 14 independent `+/-15%` stress tests (`C1`, `C2`, `C3`, 2027 volume growth delta, and all three Schedule B tariffs) keep the exact same funded slate (`WHV-OSN, BHV-OSN, HAM-HAN`) with positive `#3 - #4` BCR gaps ranging from `+0.015` to `+0.113`.

---

## Part B: Determinism & Forcedness

### B.1 Committed Recommendation & Deciding Step

- **Committed recommendation:** Fund **WHV-OSN**, **BHV-OSN**, and **HAM-HAN** under Charter RC-2027's EUR 1.75 million 2027 carrier-remediation budget (deploying EUR 1,705,000.00, retaining EUR 45,000.00 in Contingency Reserve), and defer **HAM-MAG**, **BHV-HAN**, and **BHV-KAS**.
- **Deciding steps:** Joint empirical separation of all three disclosed non-carrier overlap processes (S1 asymmetric convex inland cold-store chamber pull-back `C1`, S2 port-specific BIP rail booking-lock rollovers jointly controlling for Nordbahn consist/loco cuts `C2` plus direct CHED rail siblings, and S3 conserved shipping-line empty-depot portal queue backlogs including post-reopening drain tails `C3`). Missing or coarsely shortcutting any single mechanism flips the funded slate.

### B.2 Comprehensive Fork Analysis (41 Honest Forks + 14 Rivals Executed in Code)

We tested 41 distinct honest specifications/conventions across every open decision point (estimator family, functional form, thresholds/hinges, fixed effects, date/timezone alignment, stock timing, normalization denominator, direct CHED sibling baseline, additive vs proportional Gamma posterior splitting, observed booked-slot locking, haul-distance source tables, joint simultaneous alternatives, greedy vs exact integer knapsack, and intermediate rounding), plus 14 Charter-violating / naive / partial-shortcut / over-correction rivals:

| Fork ID | Dimension & Alternative Specification | C1 | C2 | C3 | WHV-OSN | BHV-OSN | HAM-HAN | HAM-MAG | BHV-HAN | BHV-KAS | Gap (#3-#4) | Flips Slate? | Knap != Greedy? | Pin / Disposition |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|:---:|---|
| `F00` | Base (Gamma-IRLS S1 + PortOLS S2 + DCwk S3) | 7,434.8 | 4,319.1 | 7,172.5 | 1.147 | 1.091 | 1.079 | 0.962 | 0.962 | 0.917 | +0.116 | No | No | Baseline |
| `F01` | S1: Vessel FE OLS (`h=0.78`, unconstrained) | 7,364.3 | 4,319.1 | 7,172.5 | 1.150 | 1.109 | 1.078 | 0.972 | 0.960 | 0.913 | +0.106 | No | No | Invariant |
| `F02` | S1: Non-parametric chamber util bins (`ref<0.72`) | 7,423.1 | 4,319.1 | 7,172.5 | 1.153 | 1.108 | 1.069 | 0.967 | 0.953 | 0.912 | +0.103 | No | No | Invariant |
| `F03` | S1: Piecewise linear spline (`0.78/0.85/0.92`) | 7,413.2 | 4,319.1 | 7,172.5 | 1.149 | 1.107 | 1.075 | 0.969 | 0.957 | 0.908 | +0.106 | No | No | Invariant |
| `F04` | S1: Huber robust Vessel FE (`delta=1.345`) | 7,410.5 | 4,319.1 | 7,172.5 | 1.148 | 1.098 | 1.078 | 0.968 | 0.962 | 0.912 | +0.110 | No | No | Invariant |
| `F05` | S1: Port-day FE (`port_id x discharge_date`) | 7,365.0 | 4,319.1 | 7,172.5 | 1.150 | 1.108 | 1.078 | 0.972 | 0.960 | 0.913 | +0.106 | No | No | Invariant |
| `F06` | S1: Corridor-week FE | 7,370.5 | 4,319.1 | 7,172.5 | 1.152 | 1.110 | 1.073 | 0.970 | 0.957 | 0.918 | +0.104 | No | No | Invariant |
| `F07` | S1: Hinge `0.76` (OLS Vessel FE) | 7,402.8 | 4,319.1 | 7,172.5 | 1.149 | 1.107 | 1.075 | 0.970 | 0.958 | 0.909 | +0.105 | No | No | Invariant |
| `F08` | S1: Hinge `0.80` (OLS Vessel FE) | 7,251.8 | 4,319.1 | 7,172.5 | 1.154 | 1.111 | 1.085 | 0.979 | 0.967 | 0.921 | +0.107 | No | No | Invariant |
| `F09` | S1: Opening-of-day chamber util (`closing - flow`) | 7,313.8 | 4,319.1 | 7,172.5 | 1.165 | 1.133 | 1.078 | 0.971 | 0.959 | 0.896 | +0.107 | No | No | Invariant (Annex A.2 pins closing) |
| `F10` | S1: Boundary `net_flow >= 0` as filling | 7,524.7 | 4,319.1 | 7,172.5 | 1.165 | 1.110 | 1.068 | 0.957 | 0.946 | 0.886 | +0.111 | No | No | Invariant (Sec 2.3 pins positive) |
| `F11` | S1: Join chamber state on `customs_doc_ts_utc` | 7,368.9 | 4,319.1 | 7,172.5 | 1.152 | 1.108 | 1.079 | 0.971 | 0.959 | 0.911 | +0.108 | No | No | Invariant |
| `F12` | S1: Additive `min(y, pred_pb)` split | 7,002.6 | 4,319.1 | 7,172.5 | 1.172 | 1.123 | 1.088 | 0.981 | 0.967 | 0.967 | +0.108 | No | No | Invariant (Jensen bias +0.60h gap) |
| `F13` | S2: Pooled OLS smooth logistic (`14/26/10`) | 7,434.8 | 4,343.7 | 7,172.5 | 1.140 | 1.088 | 1.087 | 0.975 | 0.952 | 0.909 | +0.112 | No | No | All 9 metrics IN_BAND |
| `F14` | S2: Poisson-ID smooth logistic (`15.8/27.5/9.0`) | 7,434.8 | 4,280.9 | 7,172.5 | 1.143 | 1.083 | 1.100 | 0.990 | 0.948 | 0.906 | +0.093 | No | No | Invariant |
| `F15` | S2: Poisson-ID port-specific slopes | 7,434.8 | 4,252.6 | 7,172.5 | 1.152 | 1.090 | 1.086 | 0.973 | 0.959 | 0.916 | +0.114 | No | No | Invariant |
| `F16` | S2: Hard-step cutoffs (`15/27/10`) | 7,434.8 | 4,368.5 | 7,172.5 | 1.142 | 1.086 | 1.088 | 0.974 | 0.950 | 0.905 | +0.112 | No | No | Invariant |
| `F17` | S2: Non-parametric lead-time bins by port | 7,434.8 | 4,388.1 | 7,172.5 | 1.141 | 1.089 | 1.077 | 0.961 | 0.958 | 0.912 | +0.116 | No | No | Invariant |
| `F18` | S2: Observed `locked_obs` Poisson-ID MLE | 7,434.8 | 4,421.1 | 7,172.5 | 1.138 | 1.079 | 1.085 | 0.978 | 0.944 | 0.906 | +0.100 | No | No | Invariant (C2 in band; NLL -3,470.5) |
| `F19` | S2: Observed `locked_obs` OLS (with int) | 7,434.8 | 4,583.9 | 7,172.5 | 1.138 | 1.078 | 1.066 | 0.960 | 0.941 | 0.904 | +0.106 | No | No | Invariant (see Note 2 below) |
| `F20` | S2: Regress directly on shuttle `rolled_days` | 7,434.8 | 4,392.4 | 7,172.5 | 1.139 | 1.084 | 1.086 | 0.972 | 0.951 | 0.907 | +0.112 | No | No | Invariant |
| `F21` | S2: Month + Corridor FE + `booked_wf_slots` | 7,434.8 | 4,505.3 | 7,172.5 | 1.137 | 1.078 | 1.085 | 0.961 | 0.946 | 0.902 | +0.117 | No | No | Invariant |
| `F22` | S2-sib: Corridor-specific rail baseline (`894.2`) | 7,434.8 | 4,319.1 | 7,172.5 | 1.147 | 1.091 | 1.079 | 0.962 | 0.962 | 0.917 | +0.116 | No | No | Invariant |
| `F23` | S2-sib: Full sibling rail days (`962.1`, no base) | 7,434.8 | 4,319.1 | 7,172.5 | 1.146 | 1.090 | 1.073 | 0.955 | 0.960 | 0.916 | +0.113 | No | No | Invariant |
| `F24` | S2-sib: Omit direct CHED rail siblings (`0.0`) | 7,434.8 | 4,319.1 | 7,172.5 | 1.160 | 1.107 | 1.151 | 1.060 | 0.983 | 0.936 | +0.048 | No | No | Charter Sec 2.3 pins separating |
| `F25` | S3: DC-ISO-week FE | 7,434.8 | 4,319.1 | 7,190.7 | 1.146 | 1.090 | 1.078 | 0.962 | 0.960 | 0.917 | +0.116 | No | No | Invariant |
| `F26` | S3: DC-day FE | 7,434.8 | 4,319.1 | 7,161.9 | 1.147 | 1.089 | 1.079 | 0.964 | 0.962 | 0.918 | +0.115 | No | No | Invariant |
| `F27` | S3: Port-day FE | 7,434.8 | 4,319.1 | 7,172.8 | 1.147 | 1.091 | 1.079 | 0.963 | 0.961 | 0.917 | +0.115 | No | No | Invariant |
| `F28` | S3: Corridor-week FE | 7,434.8 | 4,319.1 | 7,186.2 | 1.145 | 1.090 | 1.079 | 0.962 | 0.960 | 0.917 | +0.117 | No | No | Invariant |
| `F29` | S3: Huber robust DC-week FE | 7,434.8 | 4,319.1 | 7,226.0 | 1.133 | 1.091 | 1.079 | 0.962 | 0.962 | 0.916 | +0.117 | No | No | Invariant |
| `F30` | S3: Non-parametric `Q_days` bins x corr (`<=100`) | 7,434.8 | 4,319.1 | 7,141.9 | 1.144 | 1.092 | 1.079 | 0.962 | 0.970 | 0.917 | +0.109 | No | No | Invariant (`C3=7,141.9` in band) |
| `F31` | S3: Haul-distance parametric (`budgets` km) | 7,434.8 | 4,319.1 | 6,832.2 | 1.125 | 1.095 | 1.083 | 0.963 | 1.051 | 0.918 | +0.032 | No | No | Invariant (all in band) |
| `F32` | S3: Haul-distance parametric (`Maut` total km) | 7,434.8 | 4,319.1 | 6,925.8 | 1.128 | 1.096 | 1.082 | 0.964 | 1.028 | 0.914 | +0.054 | No | No | Invariant |
| `F33` | S3: Start-of-day lagged queue `Q_sod` | 7,434.8 | 4,319.1 | 6,161.4 | 1.200 | 1.102 | 1.094 | 0.995 | 1.073 | 0.938 | +0.021 | No | No | Annex A.2 pins `Q_eod` (`R2` .886 vs .774) |
| `F34` | S3: Mid-day average queue `Q_mid` | 7,434.8 | 4,319.1 | 7,073.6 | 1.154 | 1.091 | 1.079 | 0.964 | 0.976 | 0.917 | +0.103 | No | No | Invariant |
| `F35` | S3: Active-days `mean_daily_unloads` denom | 7,434.8 | 4,319.1 | 7,183.7 | 1.144 | 1.091 | 1.078 | 0.962 | 0.962 | 0.917 | +0.117 | No | No | Invariant (UTC vs CET = 0 date diffs) |
| `F36` | S3: Additive `min(y, pred_q)` split | 7,434.8 | 4,319.1 | 6,632.2 | 1.162 | 1.101 | 1.089 | 0.980 | 1.015 | 0.940 | +0.074 | No | No | Invariant (leaves +4.27h drain gap) |
| `F37` | **JOINT:** Spline S1 + Pois S2 + DC-day S3 | 7,413.2 | 4,280.9 | 7,161.9 | 1.145 | 1.096 | 1.096 | 0.998 | 0.945 | 0.899 | +0.098 | No | No | **All 9 metrics IN_BAND** |
| `F38` | **JOINT:** NP-bins S1 + `locked_obs` Pois S2 + Port-day S3 | 7,423.1 | 4,421.1 | 7,172.8 | 1.144 | 1.095 | 1.076 | 0.984 | 0.935 | 0.902 | +0.092 | No | No | **All 9 metrics IN_BAND** |
| `F39` | **JOINT EXTREME:** Add S1 + `locked_obs` OLS S2 + Add S3 | 7,002.6 | 4,583.9 | 6,632.2 | 1.178 | 1.121 | 1.086 | 0.996 | 1.000 | 0.977 | +0.086 | No | No | Still zero flip (+0.086 gap) |
| `F40` | Convention: Intermediate rounding (1d days / 2d EUR) | 7,434.8 | 4,319.1 | 7,172.5 | 1.147 | 1.091 | 1.079 | 0.962 | 0.962 | 0.917 | +0.116 | No | No | Charter Annex B pins full double |

### B.3 Strongest Rivals & Data/Charter Refutation

Every rival that changes the funding recommendation is cleanly refuted both by explicit Charter RC-2027 rules and by observable two-sided residual diagnostics computed directly from the shipped files (Charter Annex C.1):

| Rival ID | Rival Method | Funded Slate (vs Golden) | Quantitative Refutation from Shipped Files & Charter RC-2027 |
|---|---|---|---|
| `R03` | Naive TMS (zero separation) | `BHV-KAS (2.176), HAM-MAG (2.136), BHV-HAN (2.012)` (3/3 wrong) | Violates Charter Sec 2.2/2.3 & Annex C.1: retains `+32.35h` within-vessel S1 filling gap, `+2.188` days/locked-slot S2 spillover, and `+53.69h` S3 open-portal drain gap. |
| `R04` | Commercial dispute closeout (`carrier_dispute_closeout_2026.xlsx`) | `BHV-KAS (2.099), HAM-MAG (2.037), BHV-HAN (1.933)` (3/3 wrong) | Explicitly barred by Charter Sec 2.1 & Annex D ("accounting reference for 2026 invoice reconciliation only and must not be substituted for empirical operational root-cause attribution"). |
| `R05` | Drop S1 only (keep S2, S3, sib) | `BHV-KAS (1.852), BHV-OSN (1.570), WHV-OSN (1.466)` (flips) | Fails Annex C.1: leaves `+32.35h` within-vessel filling-vs-draining gap in 84% to 94% chamber band (`container_milestones_2026.csv` + reconstructed WMS chambers). |
| `R06` | Drop S2 only (keep S1, S3, sib) | `HAM-MAG (1.616), HAM-HAN (1.432), WHV-OSN (1.163)` (flips) | Fails Annex C.1: attributed carrier rail rollovers retain `+2.188` days per locked BIP slot (`rail_shuttle_departures_2026.csv` + `bip_inspection_notices_2026.jsonl`). |
| `R07` | Drop S3 only (keep S1, S2, sib) | `BHV-HAN (1.708), WHV-OSN (1.418), BHV-OSN (1.223)` (flips) | Fails Annex C.1: leaves `+53.69h` raw (`+52.98h` within-FE) open-portal drain gap on `Q_days >= 0.8` vs `< 0.15` (`depot_portal_requests_2026.csv`). |
| `R08` | S1 binary `>=92%` chamber cut | `BHV-KAS (1.334), WHV-OSN (1.275), HAM-HAN (1.275)` (flips) | Fails Annex C.1: leaves `+23.34h` within-vessel filling gap unremoved in 84% to 94% band while trimming `BHV-OSN` draining mean from `0.664` to `0.477`. |
| `R09` | S1 symmetric linear (`>0.78`, ignoring filling/draining hysteresis) | `BHV-KAS` jumps to `1.047` (knapsack flips; unhinged linear lifts to `1.217`) | Fails Annex C.1 on both sides: retains `+9.74h` filling gap while destroying 60% of genuine port-plug congestion on draining-heavy `BHV-OSN` (`0.265` vs clean `0.664`). |
| `R10` | S2 fixed-24h bivariate (omitting Nordbahn consist/loco cuts) | `WHV-OSN (1.117), BHV-OSN (1.053), BHV-HAN (0.864)`; crashes `HAM-HAN` to `0.650` | Fails Annex C.1 preservation: collapses genuine Nordbahn `consist_wagons_short` slope from `1.654` to `0.669` and `loco_derate_events` slope from `2.995` to `0.602`. |
| `R11` | S3 binary unload-day portal rejection flag | `BHV-HAN (1.383), WHV-OSN (1.288), BHV-OSN (1.160)` (flips) | Fails Annex C.1: `R^2` collapses from `0.8857` to `0.4816` and leaves 100% of the `+53.69h` (`+52.98h` FE) open-portal drain gap unremoved. |
| `R12` / `R13` | Broad over-subtraction (`util>=0.80` or all BIP shuttles) | Collapses `BHV-OSN` (`0.741`) or `HAM-HAN` (`0.483`) (flips) | Fails Annex C.1 preservation: wipes out 99% to 100% of genuine carrier slopes (`tyd_slope = 0.0000`, `short_slope = 0.029`, `loco_slope = -0.024`). |
| `R01` / `R02` | Keep `VOID` rows / keep superseded `extract_version` | Same slate (`WHV-OSN, BHV-OSN, HAM-HAN`), inflated BCRs | Explicitly barred by Charter Sec 1.3 (exclude VOID, retain highest `extract_version`). |
| Distractors | Add `north_sea_bunker_fuel_index_2026.csv` or `german_toll_maut_rates_2026_2027.xlsx` | N/A | Explicitly barred by Charter Sec 3.1 ("do not enter Schedule B detention and demurrage valuation or corridor remediation budgets"). |

### B.4 Non-Blocking Precision Notes (Part B "Only a note")

1. **Intra-tier rank ordering (#2 vs #3 among funded corridors; #4 vs #5 among deferred corridors):** Across honest estimators, funded `BHV-OSN` (1.084 to 1.123) and funded `HAM-HAN` (1.072 to 1.114) have overlapping bands (`F14` and our primary Poisson-ID reproduction rank `HAM-HAN` 1.096 slightly above `BHV-OSN` 1.094, while `F00`/`F01`/`F13`/`F38` rank `BHV-OSN` above `HAM-HAN`), and deferred `HAM-MAG` and `BHV-HAN` can swap #4/#5. Because both #2 and #3 are unconditionally `FUND` and both #4 and #5 are unconditionally `DEFER`, this never alters the funding decision, capital deployment, or portfolio economics. In rubric grading (Part C, holistic mode), grading should score `FUND`/`DEFER` status and each corridor's BCR against its defensible variant band rather than penalizing a `#2/#3` or `#4/#5` intra-tier swap.
2. **Observed `locked_obs = bip_total - (planned_wf_slots - booked_wf_slots)` in S2:** In `rail_shuttle_departures_2026.csv`, `planned_wf_slots - booked_wf_slots` equals zero on all 256 shuttles with `bip_total = 0` and never exceeds `bip_total` (732/732 shuttles), making `locked_obs` an exact observable count of locked BIP containers (`R^2 = 0.9888` against a smooth logistic lock curve with inflection points `BHV 15.8h`, `HAM 27.5h`, `WHV 9.0h`). Under count-appropriate **Poisson-ID MLE** (`F18`, `F38`), `locked_obs` achieves a +18.9 log-likelihood improvement over lead-time logistic proxies (`NLL = -3,470.52` vs `-3,451.93`) and yields **`C2 = 4,421.1`** (inside the author's `4,086.4 to 4,436.0` band) and all 6 corridor BCRs inside band (`F38`). Only if an analyst combines `locked_obs` with unweighted **OLS** (`F19`) does `C2` reach `4,583.9` (3.3% above `4,436.0`) and `HAM-HAN` BCR reach `1.066` (0.006 below `1.072`), still with a `+0.106` `#3 - #4` margin and zero funding flip.

### B.5 Data Anomalies & Giveaways Audit (Part B Steps 6 & 7)

- **Data anomalies (`PASS`):** Every structural anomaly has an explicit policy in Charter RC-2027 Section 1.3 and Annex A: 190 `VOID` test rows (excluded), 335 / 4,152 / 445 superseded `extract_version` rows across milestones / WMS / depot turn-in logs (retain max version), 66,421 German `DD.MM.YYYY` dates, 62,067 exact-integer `CASE` rows, and 21,523 / 5,530 legacy store / carrier codes resolved via `entity_crosswalk_2026.csv`. The only null cells across all 17 files are structurally expected (`5,758` null rail columns = exact count of raw `TRUCK` rows; `60,628` null `store_code` = exact count of raw `IN` warehouse movements; 0 nulls in `bip_inspection_notices_2026.jsonl`; 100% referential integrity across `container_id` and `ched_lot_id`). All `unload_complete_ts_cet` timestamps fall between 07:00 and 21:00 local time (05:00 to 20:00 UTC), producing zero midnight date splits between `Europe/Berlin` and UTC.
- **Giveaways (`PASS`):** Full-corpus sweep across all 17 files (including PDF text and Excel sheets) found zero giveaways: no input file states the recommendation, golden C1/C2/C3 totals, or corridor BCRs, and no file is a deliverable copy or generator script.

---

## Gates A through E Supplement

| Gate | Verdict | Evidence |
|---|---|---|
| **Gate A (Solution Correctness)** | **PASS** | All Layer 1 counts, stock-flow conservation checks (0.0 residual across 1,460 DC-days and 12 port-line pools), direct CHED rail siblings (895.1 c-days), naive BCRs (2.176 / 2.136 / 2.012), internal arithmetic, and independent S1/S2/S3 derivations (`C1 = 7,437.5`, `C2 = 4,280.9`, `C3 = 7,172.5`) reproduce the author's figures and exact funded slate with zero grain errors and zero attribution errors. |
| **Gate B (Every Decisive Fact Present & Grounded Vocabulary)** | **PASS** | Every rule, free-time window, tariff (Schedule B), projection equation (Annex C), budget/capture/multiplier parameter (`remediation_program_budgets_2027.csv`), opening stock (`dc_chamber_register_2026.csv`), and governance scope resides inside shipped tables verified via structural PDF/XLSX extraction. Full-corpus grep confirms every distinctive operational term in Final Recommendation (`WHV-OSN`, `BHV-OSN`, `HAM-HAN`, `HAM-MAG`, `BHV-HAN`, `BHV-KAS`, `BCR`, `Contingency Reserve`, `carrier-controllable`, `cold-store`, `pull-back`, `rail rollover`, `empty-depot`, `booking-portal`, `Nordbahn`, `CHED`, `BIP`, `FUND`, `DEFER`, all cause IDs) appears in shipped inputs. |
| **Gate C (Uniquely Forced & Margin-Robust)** | **PASS** | 0/41 honest forks across 12+ modeling and operationalization dimensions and 0/14 `+/-15%` parameter stress tests flip the `FUND`/`DEFER` slate; minimum `#3 - #4` BCR margin across core honest specifications is `+0.092` (`+0.032` under distance-parametric S3; `+0.086` under joint extreme additive/OLS stress). Greedy ranking matches exact 0-1 integer knapsack in 41/41 honest forks. Every call-flipping rival fails explicit Charter rules and observable Annex C.1 diagnostics. |
| **Gate D (Analytical Hardness, Not Semantics)** | **PASS** | Prompt objective and Charter RC-2027 Clause 4.1 objective align identically (no planted competing metric in the requester's voice). Every competing call arises strictly from analytical failure (skipping chamber-level stock reconstruction, ignoring filling/draining hysteresis, failing to profile port-specific BIP lock windows jointly with Nordbahn consist cuts, or failing to reconstruct conserved empty-depot queue drain tails). |
| **Gate E (Unambiguous Prompt on Decision, Open on Method)** | **PASS** | Prompt asks cleanly for the funded corridors, corridor BCRs, separated 2026 non-carrier delay volumes (cold-store pull-back, border-inspection rail rollovers, empty-depot return backlogs), and the three deliverables (`.pptx`, `.xlsx`, `.csv`), without prescribing econometric equations, cutoffs, rounding rules, or attached file names. All filing definitions and column schemas are pinned cleanly in Charter RC-2027. |

---

## Fix

- **Fix:** None required (`DETERMINISTIC` / `APPROVE`). Neither `prompt.txt`, `target.zip`, nor `submission.md` has any correctness or determinism defect requiring repair prior to platform runs.
- **Optional non-blocking notes for future rubric calibration (Part C):** (1) Allow intra-tier rank swaps between funded `#2/#3` (`BHV-OSN` vs `HAM-HAN`) and deferred `#4/#5` (`HAM-MAG` vs `BHV-HAN`) whenever all corridors carry correct `FUND`/`DEFER` status and BCRs within defensible bands; (2) Note that `locked_obs = bip_total - (planned_wf_slots - booked_wf_slots)` under Poisson-ID MLE lands inside the stated C2 band (`4,421.1`), whereas unweighted OLS on `locked_obs` reaches `4,583.9` while still preserving the exact funding slate.
