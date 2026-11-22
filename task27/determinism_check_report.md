# Determinism Audit Report: task27 (Pass 1)

- **Verdict:** DETERMINISTIC
- **Disposition:** FIX_NOW (minor `submission.md` Step-by-Step completeness and wording edits only; zero changes to `prompt.txt` or `target.zip`; no model rerun required).
- **Fix Location:** `solution`

## Summary

All five determinism gates (A through E) pass on the shipped prompt and input pack (`/tmp/determinism-task27-p1/target/`). Every committed figure across all four answer blocks of `submission.md` (all 8 causes' 2026 and 2027 container-days, 2027 shares, Schedule B EUR exposures, Charter RC-2027 designations, 2027 network total, 2027 Mandatory Remediation total, total and avoidable EUR, BHV, HAM, Q3, and Critical Components C1/C2/C3) reproduces cleanly from `target.zip`, sits inside its stated band, and reads identically across all four blocks. Across 28 single-dimension forks and an 18-combination Cartesian check of simultaneous defensible S1 x S2 x S3 estimators, every defensible alternative lands inside every stated band and preserves the exact five-cause REMEDIATE slate (`vessel_berth`, `coldstore_dock`, `empty_depot`, `reefer_plug`, `drayage_carrier`). Every rival design and over-correction that leaves a band or flips the 2,500 container-day call is refuted directly by a computed physical figure from the shipped files.

`Disposition` is set to `FIX_NOW` (not `APPROVE`) strictly under the self-rebuilding Step-by-Step requirement: three operational details needed to reproduce Step 4 and Step 6 verbatim without inference are omitted or stated slightly imprecisely in `submission.md` (`Step-by-Step` lines 51 and 53), plus two minor wording clarifications (`Step-by-Step` line 54 and `flatcar` vs `wagon` terminology).

---

## Evidence 1: Recomputed Figures vs `submission.md`

Recomputed independently from `/tmp/determinism-task27-p1/target/` following Charter RC-2027 and Step-by-Step (using EOD chamber utilization on `discharge_ts_utc` date with `<92%` same-vessel twins = `1,605.66` c-days; same-shuttle netted CHED rail siblings `176.60` + `436 x 2.25 = 981.00` locked-wagon rollover = `1,157.60` c-days; same-DC same-day open-quota peers on `unload_complete_ts_cet` date = `1,402.70` c-days; Annex C uniform 2027 projections and Schedule B tariffs):

| Metric | `submission.md` | Stated Band | Recomputed | Status |
|---|---|---|---|---|
| `vessel_berth` 2026 / 2027 | 4,099 / 4,514 (20.13%, EUR 0.880M, REMEDIATE) | exact | 4,098.76 / 4,513.91 (20.13%, EUR 0.880M) | Exact |
| `coldstore_dock` 2026 / 2027 (C1) | 2,738 / 3,392 (15.12%, EUR 0.967M, REMEDIATE) | 3,208 to 3,424 | 2,738.27 / 3,391.74 (15.12%, EUR 0.967M) | Exact / In band |
| `empty_depot` 2026 / 2027 (C3) | 2,160 / 3,353 (14.95%, EUR 0.771M, REMEDIATE) | 3,251 to 3,449 | 2,160.19 / 3,353.42 (14.95%, EUR 0.771M) | Exact / In band |
| `reefer_plug` 2026 / 2027 | 3,334 / 3,176 (14.16%, EUR 0.667M, REMEDIATE) | 3,146 to 3,334 | 3,334.27 / 3,176.30 (14.16%, EUR 0.667M) | Exact / In band |
| `drayage_carrier` 2026 / 2027 | 3,239 / 3,143 (14.02%, EUR 0.503M, REMEDIATE) | 3,084 to 3,206 | 3,238.56 / 3,143.17 (14.02%, EUR 0.503M) | Exact / In band |
| `phyto_insp` 2026 / 2027 | 1,481 / 2,025 (9.03%, EUR 0.527M, MONITOR) | 1,932 to 2,182 | 1,480.85 / 2,025.23 (9.03%, EUR 0.527M) | Exact / In band |
| `rail_handoff` 2026 / 2027 (C2) | 2,032 / 1,880 (8.38%, EUR 0.329M, MONITOR) | 1,770 to 1,947 | 2,032.44 / 1,880.24 (8.38%, EUR 0.329M) | Exact / In band |
| `edi_docs` 2026 / 2027 | 854 / 941 (4.20%, EUR 0.132M, MONITOR) | exact | 854.14 / 940.80 (4.20%, EUR 0.132M) | Exact |
| Total 2026 settled / 2027 network | 19,937 / 22,425 | 22,370 to 22,487 | 19,937.48 / 22,424.81 | Exact / In band |
| Total 2027 REMEDIATE (5 causes) | 17,579 | 17,524 to 17,631 | 17,578.54 | Exact / In band |
| Total 2027 EUR exposure | EUR 4.775M | EUR 4.747M to 4.807M | EUR 4.7754M | Exact / In band |
| Avoidable 2027 REMEDIATE EUR | EUR 3.788M | EUR 3.760M to 3.810M | EUR 3.7881M | Exact / In band |
| 2027 Bremerhaven (BHV) | 10,890 | 10,838 to 10,928 | 10,889.70 | Exact / In band |
| 2027 Hamburg (HAM) | 8,871 | 8,841 to 8,917 | 8,871.08 | Exact / In band |
| 2027 Third Quarter (Q3) | 9,517 | 9,489 to 9,584 | 9,516.95 | Exact / In band |

Additional intermediate checks verified cleanly:
- Step 1: `container_milestones_2026.csv` has 24,515 raw rows, 190 `VOID`, 325 superseded v1 rows, 24,000 settled rows, 19,937.48 c-days; timestamp recomputation matches all 8 stage columns to max diff `0.000012` c-days (1 second = `1/86400`).
- Step 2: Direct TMS stage projections reproduce `vessel_berth` 4,514, `reefer_plug` 4,766, `drayage_carrier` 4,505, `rail_handoff` 2,956, `coldstore_dock` 1,373, `empty_depot` 931.
- Step 3: `warehouse_pallet_movements_2026.csv` has 179,381 raw rows, 4,275 superseded EDI rows dropped, 66,381 `DD.MM.YYYY` dates parsed, 21,668 legacy store codes mapped, 61,948 `CASE` lines converted; reconstructed EOD chamber stock-flow ties to `coldstore_inventory_daily_2026.csv` with `0.0` pallets error across all 1,460 DC-days (total DC util `68.57%` to `78.01%`).
- Step 5-6: `278` CHED notices, `436` rail boxes with notice `<24h` before planned shuttle departure (max `23.33 h`), `213` with `>=24h` (min `25.28 h`, zero observations in `(23.33, 25.28)`), `1095/1095` exact match on `booked_wf_slots == cm_planned - bip_ge24`, mean loaded reefer gross mass `28.51 t`, 4-regressor weighbridge slope `-29.11 t/slot` (`se=0.53 t`, `R^2=0.99968`), exact `2.2500` c-days (`std=0.0000`) rollover jump across all `1,190` rolled boxes.
- Step 7: `depot_turnin_log_2026.csv` has 410 superseded rows dropped, 5,643 legacy carrier codes mapped, `96.48%` physical gate acceptance (`876` turn-aways vs `24,000` accepted); `depot_portal_requests_2026.csv` has `6,071` `quota_closed_rejections`, `3,180` containers unloaded on quota-closed line-days, `+10.59 h` (`10.5864 h`) same-DC same-day excess = `1,402.70` c-days (`1,402.6982`).
- Cross-block consistency: Every figure matches identically across Final Recommendation, Supplementary Questions, Critical Components, and Step-by-Step.

---

## Evidence 2: Fork Audit (28 Single-Dimension Forks + 18 Cartesian Combinations)

| # | Class & Fork Tested | Key 2027 Results (CD / ED / RP / DC / PI / RH / Q3) | Call / Band Outcome | Ruling (Defensible vs Refuted from Shipped Files) |
|---|---|---|---|---|
| F1 | Dedup order (`VOID` before vs after `extract_version`) | Identical (`24,000` rows, `19,937.48` c-days) | Identical / All in band | Zero containers have mixed `record_status`. |
| F2 | Exclude 536 containers whose `empty_gate_in_ts_utc` falls Jan 1-3, 2027 | 3,264 / 3,331 / 3,059 / 3,137 / 1,984 / 1,840 / Q3=9,517; Net=21,963 | Same call / Out of band | **Refuted** by `carrier_dispute_closeout_2026.xlsx`: `Annual_Closeout_Summary` totals `19,937.48` claimed c-days and `Port_Quarter_Detail` ties all 96 cells within `0.005` c-days to the full 24,000 containers (`Q4 = 3,743.27`). |
| F3a | Charter 4.2 Q3: assign ALL 8 stages of RAIL boxes by planned shuttle date | All causes identical; `Q3 = 9,587` | Same call / `Q3` +3 above `9,584` | **Refuted** by `carrier_dispute_closeout_2026.xlsx` (`Port_Quarter_Detail` ties all 96 cells to `discharge_ts_utc` quarters, `2026-Q3 = 8,229.33`) and Charter 4.2's literal scope (`for corridor-level rail transfers`, not non-rail stages like berth/yard/coldstore). |
| F3b | Charter 4.2 Q3: assign rail/phyto stages by planned shuttle date (non-rail by discharge date) | All causes identical; `Q3 = 9,518` | Same call / **All in band** | Defensible literal reading; sits cleanly inside `9,489 to 9,584`. |
| F4 | Allocate S2 rollover proportionally onto rolled non-BIP boxes instead of `bip_lt24` boxes | 3,392 / 3,353 / 3,176 / 3,143 / 2,025 / 1,880 / Q3=9,517 | Same call / **All in band** | Defensible; `0` change in rounded outputs. |
| F5 | S1: Vessel FE OLS (`20.225 h` uniform) | 3,389 / 3,353 / 3,177 / 3,143 / 2,025 / 1,880 / Q3=9,514 | Same call / **All in band** | Defensible; cleanly inside all bands. |
| F6 | S1: Same-vessel median twin (`20.234 h`) or `<95%` mean twin (`20.231 h`) | 3,392 / 3,353 / 3,176 / 3,143 / 2,025 / 1,880 / Q3=9,517 | Same call / **All in band** | Defensible; identical rounded 2027 outputs. |
| F7 | S1: `(port_id, discharge_date)` FE OLS (`20.226 h`) | 3,389 / 3,353 / 3,177 / 3,143 / 2,025 / 1,880 / Q3=9,514 | Same call / **All in band** | Defensible; cleanly inside all bands. |
| F8 | S1: Nonlinear `reefer_yard_util_pct` OLS (no vessel FE): quadratic (`20.22 h`), cubic (`19.98 h`), quartic (`20.03 h`), 2pp-binned (`20.17 h`) | CD `3,368-3,389`, RP `3,178-3,195` | Same call / **All in band** | Defensible (`R^2 = 0.949 to 0.990`); all land inside bands. |
| F9 | S1: Linear `reefer_yard_util_pct` OLS (+lifts/crane/port/month FE: `20.78 h`; yard_util only: `22.41 h`) | CD `3,443` / `3,606`; RP `3,134` / `3,006` | Same call / Out of band | **Refuted** by functional-form check on unsaturated boxes in `terminal_yard_daily_2026.csv`: `yard_h` is flat at `0.33 h` below `85%` and curves sharply to `17.44 h` above `95%` (`R^2 = 0.821` linear vs `0.982-0.990` binned/quartic). |
| F10 | S1: Chamber threshold `>=90%`, `>=94%`, `>=94.5%` (vessel twin) | CD `3,409` / `3,396` / `3,395`; RP `3,162` / `3,172` / `3,174` | Same call / **All in band** | Defensible; within-vessel diff is `0.00 h` below `95%`, so lower cutoffs stay inside bands. |
| F11 | S1: Chamber threshold `>=95.5%` or `>=96.0%` | CD `3,176` / `2,850`; RP `3,359` / `3,632` | Same call / Out of band | **Refuted** by within-vessel bin profile: `[94.5, 95.0)%` = `+0.04 h` vs `[95.0, 95.5)%` = `+19.40 h` (sharp step exactly at `95.0%`). |
| F12 | S1: Join chamber utilization on `customs_doc_ts_utc` date (EOD `>=95%`) | CD `3,379`, RP `3,186`, Q3 `9,516` | Same call / **All in band** | Defensible; cleanly inside all bands. |
| F13 | S1: Join on BOD chamber utilization `>=95%` or post-dwell `port_gate_ready` date | BOD: CD `3,055`, RP `3,457`; PGR: `cd26 = 1,094` | Same call / Out of band | **Refuted** by 2x2 data checks: `BOD>=95 & EOD<95` (`n=441`) has `+0.008 h` vs `EOD>=95 & BOD<95` (`n=298`) at `+19.74 h` (and BOD fails `coldstore_inventory_daily_2026.csv` tie by `124` pallets vs `0` for EOD); `PGR>=95 & Dis<95` (`n=441`) has `+0.014 h` vs `Dis>=95 & PGR<95` (`n=526`) at `+19.90 h`. |
| F14 | S1 Strongest Rival: Total-DC utilization regression (`coldstore_inventory_daily_2026.csv`, thresholds `>=74%` to `>=76%` or above-mean slope) | CD `1,556 to 2,255` (MONITOR) | **CALL FLIP** | **Refuted** by shipped files: opposing Z02/Z07 seasonal chambers hold total DC util flat (`68.6-78.0%`); `R^2 = 0.652` (total DC) vs `0.982` (chamber `sat95`); within-vessel total-DC slope on the `22,095` unsaturated boxes is `+0.0007 h/pp` (zero). |
| F15 | S1 Over-correction: 100% of `excess_port_yard` on `sat95` (unnetted) or unadjusted `26.45 h` diff | Unnetted: CD `4,329`, RP `2,482` (FLIP); Unadj: CD `3,848`, RP `2,827` | **CALL FLIP** / Out of band | **Refuted**: fails to net same-vessel port-yard congestion (`9.06 h` mean baseline yard dwell on `sat95` vessels vs `2.84 h` overall). |
| F16 | S2: Omit direct CHED rail siblings (move only `981` rollover) | PI `1,784`, RH `2,044` | Same call / Out of band | **Refuted** by `container_milestones_2026.csv` + `bip_inspection_notices_2026.jsonl`: all `464` unsampled CHED rail siblings have `0.0000` `excess_phyto_cdays` and `0.4019` c-days `excess_rail_cdays` (`18x` the `0.02145` non-BIP unrolled baseline; `176.60` net c-days), whereas sampled rail boxes (`0.8336`) and unsampled truck siblings (`0.3781`) log BIP holds in `excess_phyto_cdays`. |
| F17 | S2: Unnetted direct CHED siblings (all `649` or `464` unsampled) or unnetted `2.2714` rollover | PI `2,038-2,044`, RH `1,867-1,871` | Same call / **All in band** | Defensible; cleanly inside all bands. |
| F18 | S2: Lead-time cutoff `<22h` / `<26h` / `<30h` vs `<36h` | `<22-30h`: PI `1,945-2,128`, RH `1,811-1,934` (in band); `<36h`: PI `2,260`, RH `1,721` | Same call / `<36h` out | `<36h` **refuted** by exact 1,095/1,095 booking identity `booked_wf_slots == cm_planned - bip_ge24`, empty gap `(23.33 h, 25.28 h)`, and `bip_ge24` mass coeff `-0.18 t` (`se=0.79 t`). |
| F19 | S2 Strongest Rival: Direct CHED siblings only (no T-24h rollover) | PI `683`, RH `2,792` (REMEDIATE) | **CALL FLIP** | **Refuted** by weighbridge conservation on `rail_shuttle_departures_2026.csv`: `-29.11 t/slot` (`se=0.53 t`) on `bip_lt24` matches the `28.51 t` loaded reefer gross mass in `customs_consignment_bol_2026.csv`, proving empty wagons and `436 x 2.25 = 981.00` c-days of BIP-caused standby rollover. |
| F20 | S2 Over-correction: attribute all `729` / `821` / `1,190` rolled boxes to `phyto_insp` | PI `2,926` / `3,206` / `4,333` (REMEDIATE), RH `1,269` / `1,073` / `311` | **CALL FLIP** | **Refuted**: `non_bip_shortfall` (`754` slots) shows `-0.38 t` (`se=0.54 t`) relative to loaded wagons (`-4.15 t` vs booked), proving third-party cargo resale on Nordbahn cuts rather than empty BIP-locked wagons. |
| F21 | S2: Weighbridge ratio using `loaded_wf_slots` (`25.34 / 28.51 = 0.889`) | PI `1,876`, RH `1,981` | Same call / Out of band | **Refuted** algebraically: substituting `loaded_wf_slots = booked_wf_slots - bip_lt24 - non_bip_sf` shifts the `bip_lt24` slope by `+3.77 t` (measuring empty wagon vs `~24.7 t` third-party box, not vs `28.51 t` WF reefer). |
| F22 | S3: Alternative FE/peer controls (`date`, `port+date`, `dc+date`, `port+dc+date`, `carrier+date`, `dc+week`, `dc+date` median, `port+date` mean) | `b = 10.49-10.59 h`; ED `3,332-3,359`, DC `3,140-3,155` | Same call / **All in band** | Defensible; all 8 specifications land inside every stated band. |
| F23 | S3: Coarser `(dc, month)` FE (`11.07 h`) | ED `3,464`, DC `3,081` | Same call / Out of band (+15 / -3) | **Refuted** by intra-month open-quota ramp in `container_milestones_2026.csv`: open-quota `dray_h` rises 23x within June (`0.86 h` in W23 to `19.70 h` in W27) and drops 32x within August (`10.37 h` in W31 to `0.33 h` in W36), invalidating month-level pooling. |
| F24 | S3 Strongest Rival: Physical gate turn-aways only (`depot_turnin_log_2026.csv`, `s3=0`) | ED `931` (MONITOR), DC `4,505` | **CALL FLIP** | **Refuted** by `6,071` `quota_closed_rejections` in `depot_portal_requests_2026.csv` and `+10.59 h` same-DC same-day jump across `3,180` closed-day unloads (`unload=1 & dep_arr=0` `n=1,004` shows `+10.68 h` vs `unload=0 & dep_arr=1` `n=332` at `+0.009 h`). |
| F25 | S3 Over-correction: Unadjusted `18.61 h` diff or unnetted 100% of `dray_empty` on closed days | Unadj: ED `4,477`, DC `2,513`; Unnet: ED `5,690`, DC `1,832` (FLIP) | Out of band / **CALL FLIP** | **Refuted**: confounded by peak-summer open-quota drayage crunch (`21.93 h` open-quota mean in July vs `0.29 h` off-peak). |
| F26 | 2027 Projection: CSV 6-decimal `multiplier_2027` vs exact `value_2027 / value_2026` | Identical integers on all 15 metrics | Same call / **All in band** | Insensitive (max diff `<0.01` c-day). |
| F27 | 2027 Projection: Empirical 2026 line shares (`25.89/25.15/26.22/22.74%`) vs Charter Table 4 (`26/25/26/23%`) | ED `3,352` (vs `3,353`); all others identical | Same call / **All in band** | Insensitive (1 c-day shift; Charter Table 4 and `import_plan_2027.csv` pin `26/25/26/23%`). |
| F28 | Rounding: round 2027 cause c-days to integers before Schedule B EUR valuation | Total EUR `4.775M`, Avoidable EUR `3.788M` | Same call / **All in band** | Insensitive (identical to EUR `0.001M`). |
| C1-18 | Cartesian matrix of simultaneous defensible S1 (3) x S2 (2) x S3 (3) estimators | **18 / 18** combinations inside all 15 stated bands | **18 / 18** same call & **All in band** | Joint estimator robustness confirmed. |

---

## Gates B, D, and E Checks

- **Gate B (Filed facts & action vocabulary):** PASS. Every operative rule, threshold (`2,500`), tariff (Schedule B), projection equation (Annex C Table 3), 2027 parameter (Table 4 / `import_plan_2027.csv`), quarter rule (Clause 4.2), and CSV schema (Section 5) is filed in `weserfrucht_remediation_charter_rc2027.pdf` and `import_plan_2027.csv`. All distinctive terms of the committed recommendation (`Mandatory Remediation`, `Routine Monitoring`, `Charter RC-2027`, all 8 `cause_id`s, `REMEDIATE`, `MONITOR`, `detention`, `demurrage`, `Bremerhaven`, `Hamburg`, `Q3`) appear verbatim in the shipped files. Only one rationale noun (`flatcar`) returns zero hits across all 17 files (`rail_shuttle_departures_2026.csv` uses `train_wagon_count` / `wagon`).
- **Gates D and E (Asks & prompt clarity):** PASS. `prompt.txt` pins one funding decision under Charter RC-2027's 2,500 c-day threshold, specifies every requested metric and unit (container-days, euros) without method prescription, and requests three clear deliverables.

---

## Fix (`solution` only -- `FIX_NOW`)

Apply four targeted wording/completeness edits to `/home/antigravity/sathyaNEU/sulphur/task27/submission.md` (no changes to `prompt.txt`, `target.zip`, any graded figure, or any stated band):

1. **Step 4 (`submission.md`, line 51):** Explicitly state the join timing and unsaturated twin pool used to reproduce `1,905` containers and `1,605.66` c-days verbatim: change `"comparing 1,905 containers facing >= 95 percent destination chamber utilization against same-vessel unsaturated twins"` to `"comparing 1,905 containers facing >= 95 percent end-of-day (EOD) destination chamber utilization on container discharge date against same-vessel unsaturated twins (< 92 percent utilization; < 95 percent yields 1,605.83 c-days and identical rounded 2027 outputs)"`.
2. **Step 6 (`submission.md`, line 53):**
   - Include the 4th regressor needed to reproduce `-29.11` tonnes/slot (since the 3-regressor fit without it yields `-29.49` tonnes/slot): `"regressing train_total_gross_tonnes on wagon count, booked slots, post-24h locked slots, and non-BIP slot shortfall (booked - loaded - locked, measuring -4.15 t vs booked and -0.38 t vs loaded) measures -29.11 tonnes per locked slot"`.
   - Explicitly state that the final 2027 totals combine BOTH Step 5's `176.60` direct unsampled CHED rail sibling c-days (netted against same-shuttle unrolled non-BIP peers) AND Step 6's `981.00` standby rollover c-days (`1,157.60` c-days total in 2026), and note that `2.25 c-days per box` is the measured exact difference between rolled (`2.2714`) and same-shuttle unrolled (`0.0214`) rail containers.
3. **Final Recommendation & Step 6 (`submission.md`, lines 8 and 53):** Replace `"empty rail flatcars"` / `"empty-flatcar"` with `"empty rail wagons"` / `"empty-wagon"` to match `train_wagon_count` in `rail_shuttle_departures_2026.csv`.
4. **Step 7 (`submission.md`, line 54):** Clarify `"with a 4.33x retry multiplicity"` as `"6,071 portal rejections vs 1,402.70 attributed excess c-days = 4.33 rejections per attributed c-day, or 1.91 rejections per affected container; 5 unpaired boxes fall back to the DC open-quota mean"`.
