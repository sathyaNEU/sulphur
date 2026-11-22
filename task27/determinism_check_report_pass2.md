# Determinism Audit Report (Pass 2) - task27

- **Verdict:** DETERMINISTIC
- **Disposition:** APPROVE (no repair or model rerun required; all Gates A to E pass cleanly, every committed figure reproduces exactly across all four blocks, and zero unrefuted forks flip the 5-cause slate or breach stated bands; one harmless 4th-decimal parenthetical polish in Step 6 is noted below as optional).
- **Fix:** none (optional non-blocking polish in `solution` Step 6: `same-shuttle unrolled 0.0214 c-days` -> `same-shuttle unrolled 0.0217 c-days`, or `global unrolled 0.0214 c-days`, since `2.27172 - 0.02172 = 2.25000` exact while `0.02137` is the global unrolled non-BIP mean across all 13,896 unrolled rail boxes; changing it moves zero committed integers).

---

## 1. Gate A: Full Independent Recomputation from `target.zip`

Recomputed strictly from a fresh unzip of `task27/target.zip` into `/tmp/determinism-task27-p2/target/` using only Charter RC-2027 (`weserfrucht_remediation_charter_rc2027.pdf`) and the rules stated in `submission.md` Step-by-Step. Every committed figure matches identically across Final Recommendation, Supplementary Questions, Critical Components, and Step-by-Step.

### Committed Cause-Level, Aggregate, Corridor, Q3, and Critical Component Figures

| Metric / Component | Recomputed Exact | Recomputed Rounded | Submission Value | Stated Band | Match / Band |
|---|---:|---:|---:|---|---|
| `vessel_berth` 2027 (2026) | 4,530.26 (4,107.34) | 4,530 (4,107) | 4,530 (4,107) | exact | EXACT (REMEDIATE) |
| `vessel_berth` share / EUR | 20.534% / EUR 883,402 | 20.53% / EUR 0.883M | 20.53% / EUR 0.883M | exact | EXACT |
| `coldstore_dock` 2027 (2026) **[C1]** | 3,366.62 (2,732.06) | 3,367 (2,732) | 3,367 (2,732) | 3,086 to 3,386 | EXACT / IN BAND (REMEDIATE) |
| `coldstore_dock` share / EUR | 15.260% / EUR 959,488 | 15.26% / EUR 0.959M | 15.26% / EUR 0.959M | - | EXACT |
| `drayage_carrier` 2027 (2026) | 3,212.97 (3,324.42) | 3,213 (3,324) | 3,213 (3,324) | 3,167 to 3,240 | EXACT / IN BAND (REMEDIATE) |
| `drayage_carrier` share / EUR | 14.563% / EUR 514,074 | 14.56% / EUR 0.514M | 14.56% / EUR 0.514M | - | EXACT |
| `reefer_plug` 2027 (2026) | 3,149.51 (3,283.79) | 3,150 (3,284) | 3,150 (3,284) | 3,135 to 3,385 | EXACT / IN BAND (REMEDIATE) |
| `reefer_plug` share / EUR | 14.276% / EUR 661,397 | 14.28% / EUR 0.661M | 14.28% / EUR 0.661M | - | EXACT |
| `empty_depot` 2027 (2026) **[C3]** | 3,053.49 (2,006.05) | 3,053 (2,006) | 3,053 (2,006) | 3,015 to 3,125 | EXACT / IN BAND (REMEDIATE) |
| `empty_depot` share / EUR | 13.840% / EUR 702,302 | 13.84% / EUR 0.702M | 13.84% / EUR 0.702M | - | EXACT |
| `phyto_insp` 2027 (2026) | 2,057.65 (1,513.84) | 2,058 (1,514) | 2,058 (1,514) | 1,940 to 2,208 | EXACT / IN BAND (MONITOR) |
| `phyto_insp` share / EUR | 9.327% / EUR 534,988 | 9.33% / EUR 0.535M | 9.33% / EUR 0.535M | - | EXACT |
| `rail_handoff` 2027 (2026) **[C2]** | 1,734.06 (1,875.46) | 1,734 (1,875) | 1,734 (1,875) | 1,628 to 1,819 | EXACT / IN BAND (MONITOR) |
| `rail_handoff` share / EUR | 7.860% / EUR 303,460 | 7.86% / EUR 0.303M | 7.86% / EUR 0.303M | - | EXACT |
| `edi_docs` 2027 (2026) | 957.48 (869.56) | 957 (870) | 957 (870) | exact | EXACT (MONITOR) |
| `edi_docs` share / EUR | 4.340% / EUR 134,048 | 4.34% / EUR 0.134M | 4.34% / EUR 0.134M | exact | EXACT |
| Total 2027 network c-days (2026) | 22,062.03 (19,712.53) | 22,062 (19,713) | 22,062 (19,713) | 22,001 to 22,131 | EXACT / IN BAND |
| Total 2027 REMEDIATE c-days | 17,312.85 | 17,313 | 17,313 | 17,252 to 17,354 | EXACT / IN BAND |
| Total 2027 EUR exposure | EUR 4,693,157.90 | EUR 4.693M | EUR 4.693M | EUR 4.654M to 4.725M | EXACT / IN BAND |
| Avoidable 2027 EUR (REMEDIATE) | EUR 3,720,662.47 | EUR 3.721M | EUR 3.721M | EUR 3.681M to 3.739M | EXACT / IN BAND |
| Bremerhaven (BHV) 2027 | 10,647.32 | 10,647 | 10,647 | 10,599 to 10,704 | EXACT / IN BAND |
| Hamburg (HAM) 2027 | 8,215.91 | 8,216 | 8,216 | 8,187 to 8,252 | EXACT / IN BAND |
| Third Quarter (Q3) 2027 | 8,579.53 | 8,580 | 8,580 | 8,547 to 8,686 | EXACT / IN BAND |

### Step-by-Step Intermediate Figures Verification (Steps 1 to 8)

- **Step 1 (Lifecycle reconciliation):** 24,495 raw rows -> 190 VOID excluded, 305 superseded version-1 rows dropped -> 24,000 settled containers, 19,712.5303 c-days (`carrier_dispute_closeout_2026.xlsx` claimed total = 19,712.53). Stage-sum vs `excess_cdays_total` max diff = `0.000002` c-days; raw timestamp-recomputed stage vs CSV stage max diff = `0.0000119` c-days (1-second timestamp rounding = `1/86400 = 0.0000116`, rounds to `0.00001`). **Reproduced.**
- **Step 2 (Direct TMS read):** Projected 2027 direct TMS totals: `vessel_berth` 4,530.26 (4,530), `reefer_plug` 4,754.18 (4,754), `drayage_carrier` 4,411.28 (4,411), `rail_handoff` 2,797.24 (2,797), `coldstore_dock` 1,357.39 (1,357), `empty_depot` 946.72 (947), `edi_docs` 957.48 (957), `phyto_insp` 495.14 (495). **Reproduced.**
- **Step 3 (Warehouse stock-flow):** `warehouse_pallet_movements_2026.csv` 179,544 raw rows, 4,260 superseded revisions dropped (175,284 remaining), 66,670 European `DD.MM.YYYY` dates parsed, 21,622 legacy store codes mapped via `entity_crosswalk_2026.csv`, 61,598 `CASE` lines converted via `sku_thermal_catalog.csv` (0.0 fractional pallet deviation), tying to `coldstore_inventory_daily_2026.csv` with **0.0 pallets error** across all 1,460 DC-days. **Reproduced.**
- **Step 4 (S1 chamber saturation):** Aggregate DC util spans 69.045% to 79.013% (69.0 to 79.0%). 1,930 containers face >= 95% EOD destination chamber util on discharge date; matched against same-vessel `< 92%` twins (0 unmatched), mean jump = **+20.1037 h** (+20.10 h), shift = **1,616.6732 c-days** (1,616.67; `< 95%` twins yield 1,616.3429 c-days and identical rounded 2027 outputs `3,366` / `3,150` within 1 c-day; `3,366.29` rounds to 3,366 vs 3,367 at `<92%`, both well inside band). **Reproduced.**
- **Step 5 (S2 CHED siblings and T-24h lock):** 309 CHED-lot notices in `bip_inspection_notices_2026.jsonl`, 1,095 shuttles in `rail_shuttle_departures_2026.csv`. 517 unsampled CHED rail siblings netted against same-shuttle unrolled non-BIP peers shift **191.3890 c-days** (191.39), leaving sibling-only `rail_handoff` at **2,620.28** (2,620, still wrongly REMEDIATE). 426 CHED rail boxes have `lead_hrs < 24.0 h` (122 sampled + 304 unsampled; 0 boxes in `[24.0, 25.0) h`). **Reproduced.**
- **Step 6 (S2 empty-wagon mass conservation):** OLS of `train_total_gross_tonnes` on `train_wagon_count`, `booked_wf_slots`, `locked_all`, and `non_bip_shortfall` (`R^2 = 0.999688`) yields **-28.0089 t/locked slot** (-28.01 t, SE 0.56, t = -50.4) and **-3.1499 t** (-3.15 t) for `non_bip_shortfall` vs booked (**+0.6481 t**, +0.65 t, vs loaded), matching the **28.5207 t** (28.52 t) mean loaded reefer gross mass in `customs_consignment_bol_2026.csv`. Every rolled non-BIP box (1,110 total) exceeds its same-shuttle unrolled mean by **2.250000 c-days** (`std = 0.000000`), reallocating `426 x 2.25 =` **958.50 c-days** (`191.39 + 958.50 = 1,149.89 c-days`). *Minor non-blocking polish note:* Step 6 writes `(2.25 c-days per box, measured as rolled 2.2717 minus same-shuttle unrolled 0.0214 c-days)`; `0.021367` (`0.0214`) is the global mean across all 13,896 unrolled non-BIP rail boxes, whereas the same-shuttle unrolled mean paired to the 1,110 rolled boxes is `0.021720` (`0.0217`, giving `2.27172 - 0.02172 = 2.25000` exact; using global `0.0214` yields `958.65`, moving 2027 `rail_handoff` and `phyto_insp` by 0.2 c-days with zero integer change). **Reproduced.**
- **Step 7 (S3 empty-depot portal quotas):** `depot_turnin_log_2026.csv` 25,302 raw rows -> 433 superseded dropped -> 24,869 rows, 5,590 legacy carrier codes mapped, 869 turn-aways -> **96.5057%** (96.51%) physical gate acceptance. `depot_portal_requests_2026.csv` has **5,273** quota-closed rejections across 366 closed line-days. 2,809 containers unloaded on quota-closed line-days (25 unpaired falling back to DC open-quota mean) show **+10.6117 h** (+10.61 h) excess return delay = **1,242.0147 c-days** (1,242.01; `5,273 / 1,242.0147 = 4.25` rejections/c-day, `5,273 / 2,809 = 1.88` rejections/container). **Reproduced.**
- **Step 8 (2027 schedule, counterfactuals, stresses):** All single- and pair-dropped counterfactuals (`Drop S1`: coldstore_dock 1,357; `Drop S2`: rail_handoff 2,797; `Drop S3`: empty_depot 947; all three pairs) reproduce identically. `-20%` stress on `reefer_plug` = `2,519.6 -> 2,520`; `+20%` stress on S2 rollover = `2,318.1 -> 2,318`. Unprojected 2026 actuals leave `empty_depot` at `2,006` (MONITOR). **Reproduced.**

---

## 2. Gate C: Comprehensive Fork Battery (44 Individual Forks + 576 Joint Combinations)

Every class of open choice was enumerated and executed directly on the unzipped files.

### Part A: Unrefuted / Licensed Variants (All Preserve Exact 5-Cause Slate and Land Inside Every Stated Band)

| Fork Tested | Slate | CD | RP | RH | PH | ED | DC | Tot27 | Rem27 | EUR Tot / Rem | BHV / HAM / Q3 | Band Status |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|
| 00. Golden baseline | SAME | 3,367 | 3,150 | 1,734 | 2,058 | 3,053 | 3,213 | 22,062 | 17,313 | 4.693 / 3.721 | 10,647 / 8,216 / 8,580 | ALL IN BAND |
| 01. Exact `value_2027/value_2026` (vs CSV `multiplier_2027`) | SAME | 3,367 | 3,150 | 1,734 | 2,058 | 3,053 | 3,213 | 22,062 | 17,313 | 4.693 / 3.721 | 10,647 / 8,216 / 8,580 | ALL IN BAND |
| 02. Empirical 2026 line shares (vs plan 26/25/26/23%) | SAME | 3,367 | 3,150 | 1,734 | 2,058 | 3,061 | 3,213 | 22,070 | 17,320 | 4.695 / 3.722 | 10,651 / 8,218 / 8,584 | ALL IN BAND |
| 03. Round integer c-days before EUR valuation | SAME | 3,367 | 3,150 | 1,734 | 2,058 | 3,053 | 3,213 | 22,062 | 17,313 | 4.693 / 3.721 | 10,647 / 8,216 / 8,580 | ALL IN BAND |
| 04. Q3 by `discharge_ts` in Europe/Berlin (CET/CEST) | SAME | 3,367 | 3,150 | 1,734 | 2,058 | 3,053 | 3,213 | 22,062 | 17,313 | 4.693 / 3.721 | 10,647 / 8,216 / 8,580 | ALL IN BAND |
| 05. Q3 `rail_handoff` by shuttle date, rest discharge | SAME | 3,367 | 3,150 | 1,734 | 2,058 | 3,053 | 3,213 | 22,062 | 17,313 | 4.693 / 3.721 | 10,647 / 8,216 / 8,575 | ALL IN BAND |
| 06. Q3 `rail_handoff` + `phyto_insp` (RAIL) by shuttle | SAME | 3,367 | 3,150 | 1,734 | 2,058 | 3,053 | 3,213 | 22,062 | 17,313 | 4.693 / 3.721 | 10,647 / 8,216 / 8,567 | ALL IN BAND |
| 07. Q3 all RAIL boxes by shuttle date, TRUCK discharge | SAME | 3,367 | 3,150 | 1,734 | 2,058 | 3,053 | 3,213 | 22,062 | 17,313 | 4.693 / 3.721 | 10,647 / 8,216 / 8,564 | ALL IN BAND |
| 10. S1 control `< 95%` (complement vs `< 92%`) | SAME | 3,366 | 3,150 | 1,734 | 2,058 | 3,053 | 3,213 | 22,062 | 17,313 | 4.693 / 3.721 | 10,647 / 8,216 / 8,579 | ALL IN BAND |
| 11. S1 control `< 90%` | SAME | 3,367 | 3,149 | 1,734 | 2,058 | 3,053 | 3,213 | 22,062 | 17,313 | 4.693 / 3.721 | 10,647 / 8,216 / 8,580 | ALL IN BAND |
| 12. S1 cutoff `>= 94%` vs `< 92%` | SAME | 3,370 | 3,146 | 1,734 | 2,058 | 3,053 | 3,213 | 22,063 | 17,313 | 4.694 / 3.721 | 10,648 / 8,216 / 8,580 | ALL IN BAND |
| 13. S1 cutoff `>= 93%` vs `< 92%` | SAME | 3,373 | 3,144 | 1,734 | 2,058 | 3,053 | 3,213 | 22,063 | 17,314 | 4.694 / 3.721 | 10,648 / 8,216 / 8,580 | ALL IN BAND |
| 15. S1 join on discharge date CET/CEST | SAME | 3,367 | 3,150 | 1,734 | 2,058 | 3,053 | 3,213 | 22,062 | 17,313 | 4.693 / 3.721 | 10,647 / 8,216 / 8,580 | ALL IN BAND |
| 16. S1 join on `customs_doc_ts_utc` date | SAME | 3,351 | 3,163 | 1,734 | 2,058 | 3,053 | 3,213 | 22,059 | 17,310 | 4.691 / 3.719 | 10,646 / 8,216 / 8,577 | ALL IN BAND |
| 19. S1 mid-day `(BOD+EOD)/2` util `>= 95%` | SAME | 3,187 | 3,294 | 1,734 | 2,058 | 3,053 | 3,213 | 22,027 | 17,278 | 4.672 / 3.700 | 10,623 / 8,207 / 8,554 | ALL IN BAND |
| 20. S1 same-vessel MEDIAN twins (vs mean) | SAME | 3,367 | 3,150 | 1,734 | 2,058 | 3,053 | 3,213 | 22,062 | 17,313 | 4.693 / 3.721 | 10,647 / 8,216 / 8,580 | ALL IN BAND |
| 21. S1 Vessel FE OLS constant jump (`>= 95%`) | SAME | 3,355 | 3,158 | 1,734 | 2,058 | 3,053 | 3,213 | 22,059 | 17,310 | 4.692 / 3.719 | 10,646 / 8,215 / 8,577 | ALL IN BAND |
| 23. S1 Port-day matched twins (and same-vessel+DC twins) | SAME | 3,367 | 3,150 | 1,734 | 2,058 | 3,053 | 3,213 | 22,062 | 17,313 | 4.693 / 3.721 | 10,647 / 8,216 / 8,580 | ALL IN BAND |
| 24. S2 lock cutoff `< 22h` | SAME | 3,367 | 3,150 | 1,806 | 1,952 | 3,053 | 3,213 | 22,029 | 17,313 | 4.678 / 3.721 | 10,639 / 8,202 / 8,575 | ALL IN BAND |
| 25. S2 lock cutoff `< 23h` | SAME | 3,367 | 3,150 | 1,747 | 2,039 | 3,053 | 3,213 | 22,056 | 17,313 | 4.691 / 3.721 | 10,641 / 8,216 / 8,576 | ALL IN BAND |
| 26. S2 lock cutoff `< 26h` | SAME | 3,367 | 3,150 | 1,715 | 2,086 | 3,053 | 3,213 | 22,071 | 17,313 | 4.697 / 3.721 | 10,648 / 8,224 / 8,580 | ALL IN BAND |
| 27. S2 lock cutoff `< 28h` | SAME | 3,367 | 3,150 | 1,696 | 2,113 | 3,053 | 3,213 | 22,080 | 17,313 | 4.701 / 3.721 | 10,653 / 8,227 / 8,582 | ALL IN BAND |
| 28. S2 global unrolled peer netting (vs same-shuttle) | SAME | 3,367 | 3,150 | 1,734 | 2,058 | 3,053 | 3,213 | 22,062 | 17,313 | 4.693 / 3.721 | 10,647 / 8,216 / 8,580 | ALL IN BAND |
| 29. S2 gross unsampled CHED (no sibling netting) | SAME | 3,367 | 3,150 | 1,724 | 2,073 | 3,053 | 3,213 | 22,067 | 17,313 | 4.695 / 3.721 | 10,650 / 8,218 / 8,581 | ALL IN BAND |
| 30. S2 weighbridge-scaled (`28.01/28.52 = 98.21%`) | SAME | 3,367 | 3,150 | 1,750 | 2,034 | 3,053 | 3,213 | 22,055 | 17,313 | 4.690 / 3.721 | 10,644 / 8,213 / 8,577 | ALL IN BAND |
| 31. S2 gross rollover (`2.2717` vs net `2.25`) | SAME | 3,367 | 3,150 | 1,725 | 2,070 | 3,053 | 3,213 | 22,066 | 17,313 | 4.695 / 3.721 | 10,649 / 8,217 / 8,581 | ALL IN BAND |
| 32. S2 rollover assigned to locked boxes (vs rolled boxes) | SAME | 3,367 | 3,150 | 1,734 | 2,058 | 3,053 | 3,213 | 22,062 | 17,313 | 4.693 / 3.721 | 10,647 / 8,216 / 8,580 | ALL IN BAND |
| 33. S2 include sampled CHED rail excess (netted) | SAME | 3,367 | 3,150 | 1,734 | 2,058 | 3,053 | 3,213 | 22,062 | 17,313 | 4.693 / 3.721 | 10,647 / 8,216 / 8,580 | ALL IN BAND |
| 34. S3 drop 25 unpaired boxes (no DC fallback) | SAME | 3,367 | 3,150 | 1,734 | 2,058 | 3,026 | 3,228 | 22,050 | 17,301 | 4.689 / 3.717 | 10,639 / 8,213 / 8,573 | ALL IN BAND |
| 35. S3 same-port same-day open lines (vs DC-day) | SAME | 3,367 | 3,150 | 1,734 | 2,058 | 3,054 | 3,213 | 22,062 | 17,313 | 4.693 / 3.721 | 10,647 / 8,215 / 8,578 | ALL IN BAND |
| 36. S3 same-DC+port+day open lines | SAME | 3,367 | 3,150 | 1,734 | 2,058 | 3,116 | 3,178 | 22,090 | 17,341 | 4.702 / 3.730 | 10,660 / 8,227 / 8,602 | ALL IN BAND |
| 38. S3 same-DC same-day MEDIAN contrast | SAME | 3,367 | 3,150 | 1,734 | 2,058 | 3,058 | 3,210 | 22,064 | 17,315 | 4.694 / 3.721 | 10,649 / 8,216 / 8,581 | ALL IN BAND |
| 39. S3 DC-day FE OLS (unclipped 3,043 / clipped 3,016) | SAME | 3,367 | 3,150 | 1,734 | 2,058 | 3,016 | 3,235 | 22,046 | 17,297 | 4.688 / 3.716 | 10,641 / 8,212 / 8,571 | ALL IN BAND |
| 40a. S3 Port-day FE OLS unclipped (also DC+car+day FE 3,047/3,020) | SAME | 3,367 | 3,150 | 1,734 | 2,058 | 3,041 | 3,220 | 22,057 | 17,308 | 4.691 / 3.719 | 10,645 / 8,214 / 8,576 | ALL IN BAND |

### Part B: Joint Simultaneous S1 x S2 x S3 Grids

- **Core estimator-family joint grid (144 simultaneous combinations:** 6 S1 estimators x 4 S2 estimators x 6 S3 estimators at the empirically identified 95% / 24h / `rej >= 1` physical boundaries): **0 / 144 slate flips and 0 / 144 out-of-band figures across all 15 metrics** (`tot27` 22,036-22,067, `rem27` 17,294-17,313, `EUR tot` 4.683-4.695M, `EUR rem` 3.714-3.721M, `BHV` 10,635-10,650, `HAM` 8,209-8,218, `Q3` 8,566-8,581).
- **Wide simultaneous stress grid (576 combinations:** adding `mid_util`, `cut_93`/`94`, `<22h`/`<28h`, `drop_unpaired`, `dc_port_day`): **0 / 576 slate flips** and **0 / 576 OOB on all eight individual causes, REMEDIATE total, avoidable EUR, BHV, and HAM** (only 7-13 triple-extreme combinations combining refuted `<22h` + `mid_util` + lower-tail-clipped FE dip 1-23 c-days below `tot27`/`Q3`).

### Part C: Rivals Crossing 2,500 or Leaving a Band - Native-Unit Empirical Refutations

| Rival / Excluded Fork | Result (vs Band / 2,500) | Native-Unit Refutation or Explicit Charter Rule (File + Figure) |
|---|---|---|
| **R1. S1 Total-DC regression rival** (`coldstore_inventory_daily_2026.csv` only) | `coldstore_dock` 1,750-2,080 (**FLIPS** to MONITOR) | Refuted by `warehouse_pallet_movements_2026.csv` + `dc_chamber_register_2026.csv` + `sku_thermal_catalog.csv` (0.0 pallets error across 1,460 DC-days): opposing chamber correlations (`corr(Z02,Z07)=-0.448`, `corr(Z02,Z13)=-0.472`, `corr(Z07,Z13)=-0.513`) mask Z02/Z07 spikes to 99.3% inside flat 69.0-79.0% DC totals. Same-vessel **and same-DC** cross-chamber twins (`1,926/1,930` matched) show **+20.11 h** jump (`min +13.50 h`) at `>= 95%`, vs `+0.017 h` in `[0.94, 0.95)`. |
| **R2. S1 BOD util / `pgr` date / `>= 96%` / linear `tyd` OLS** | `coldstore_dock` 3,020 / 2,837 / 2,913 / 3,528 (OOB, SAME slate) | Refuted in `container_milestones_2026.csv` + `terminal_yard_daily_2026.csv`: (a) `BOD>=95% & EOD<95%` (330 boxes) = **+0.04 h**, while `EOD>=95% & BOD<95%` (360 boxes) = **+19.58 h** (`min +14.08 h`); (b) `pgr>=95% & dis<95%` (411 boxes) = **+0.03 h**, while `dis>=95% & pgr<95%` (526 boxes) = **+19.98 h**; (c) `[0.95,0.96)` (475 boxes) = **+19.36 h** vs `+0.017 h` in `[0.94,0.95)`; (d) unsaturated yard dwell vs `reefer_yard_util_pct` is flat (`0.29-0.34 h` <=88%) then spikes nonlinearly (`19.03 h` >95%), refuting linear `tyd` control (`port+date FE` recovers `20.10 h`, `3,355`). |
| **R3. S2 Direct CHED sibling-only rival** (or sampled-only locks) | `rail_handoff` 2,620 (**FLIPS** to REMEDIATE) | Refuted by `rail_shuttle_departures_2026.csv` weighbridge OLS (`R^2=0.9997`): locked `<24h` CHED slots drop train mass by **-28.01 t/slot** (SE 0.56, t=-50.4; port FE `-28.09`, loco FE `-28.12`), matching `28.52 t` mean loaded reefer mass in `customs_consignment_bol_2026.csv`. Separating sampled vs unsampled locks gives **-28.65 t** (SE 2.42) and **-27.79 t** (SE 0.98) respectively, and binned lead-time OLS shows a sharp step at 24h (`[23,24)h = -30.17 t` vs `[25,26)h = +5.80 t`). |
| **R4. S3 Gate-only rival / `depot_arr_date` / `unload+1` / `rej>=2` / sparse carrier cell / clipped port-day FE** | `empty_depot` 947 (**FLIPS**), 2,350 (**FLIPS**), 2,518, 3,010, 3,566, 3,014 | Refuted in `depot_portal_requests_2026.csv` + `container_milestones_2026.csv`: (a) `q_u0=True` (2,809 boxes) jumps **+10.61 h**; (b) `q_u0=False & q_arr=True` (375 boxes) jumps **+0.013 h** (zero) while `q_u0=True & q_arr=False` (793 boxes) jumps **+10.59 h**; (c) `q_u0=False & q_u1=True` (326 boxes) jumps **+0.005 h** while `q_u0=True & q_u1=False` (599 boxes) jumps **+10.50 h**; (d) `rej==1` (37 boxes) jumps **+10.16 h** (`min +6.79 h` vs max `+1.16 h` at `rej==0`); (e) `(dc, carrier, date)` leaves 23.9% (670/2,809) unpaired causing annual-mean fallback bias (`dc+carrier+date FE OLS` gives `3,047` unclipped / `3,020` clipped, in band); (f) `port+date FE OLS` unclipped is `3,041` (in band; only asymmetric lower-tail clipping of a constant beta creates a 1 c-day Jensen dip to `3,014.24`). |
| **R5. Unnetted over-corrections** (S1-over, S2-over, S3-over) | `reefer_plug` 1,895-2,474; `phyto_insp` 2,911-4,196; `drayage_carrier` 1,824-2,163 (**FLIPS**) | Refuted by native baselines: same-vessel unsaturated yard dwell (`0.29-19.03 h`), 684 non-BIP rolled slots (`non_bip_shortfall = +0.65 t` vs loaded, refuting empty wagons), and `5,273 / 1,242.01 = 4.25x` portal retry multiplicity (`1.88` rejections/container). |
| **R6. Charter-barred scope & formula forks** (VOID/v1 retention, Jan-2027 tail drop, documentary settlement scaling, Q3 by ETA/unload, `coldstore_dock * port_vol`) | `tot26` 20,200; Jan-27 drop `tot27` 21,535 (SAME slate); `coldstore_dock` 3,706; Q3 8,384 / 9,368 | Explicitly barred by `weserfrucht_remediation_charter_rc2027.pdf` Sec 2.1 (exclude VOID, highest `extract_version`), Sec 3.1 (do not use documentary settlements), Sec 4.2 (discharge or planned shuttle date for Q3; all 24,000 containers discharged in 2026, confirmed by `carrier_dispute_closeout_2026.xlsx` 19,712.53 total as of 12 Jan 2027 and `depot_portal_requests_2026.csv` running through `2027-01-14`), and Annex C Table 3 (`coldstore_dock` scales by DC zone load only). |

---

## 3. Gates B, D, E, and Self-Rebuilding Check

- **Gate B (Filed Facts & Action Vocabulary): PASS.** All governing thresholds (`2,500`), free-time allowances, canonical `cause_id`s, Schedule B daily EUR tariffs, Annex C equations, `import_plan_2027.csv` multipliers, and distractor exclusions (bunker fuel, LKW-Maut tolls outside Schedule B per Charter Sec 4.1) are present in the shipped files (PDF layout and XLSX XML verified). Every distinctive term of the committed recommendation (`Mandatory Remediation`, `Charter RC-2027`, `2,500`, all eight `cause_id`s, `Routine Monitoring`, `detention`, `demurrage`) appears verbatim in the shipped pack, and all physical mechanism terms (`chamber`, `thermal`, `CHED`, `wagon`, `standby`, `portal`, `quota`) appear in shipped filenames, headers, or Charter text.
- **Gates D & E (Analytical Hardness & Prompt Clarity): PASS.** `prompt.txt` demands one committed remediation call under Charter RC-2027's 2,500 container-day threshold, pins every supplementary quantity and unit (2027 and 2026 cause totals, 2027 network and remediation totals, overall and designated EUR exposure, BHV/HAM/Q3 2027 totals, CSV/XLSX/PPTX deliverables), avoids method dictation and hints, and contains zero semantic ambiguity.
- **Self-Rebuilding Completeness: PASS.** Every committed figure across all four blocks rebuilt cleanly using only Charter RC-2027 and the rules written in Step-by-Step, with zero guessed rules and zero cross-block contradictions (only the minor 4th-decimal parenthetical note in Step 6 noted above).
