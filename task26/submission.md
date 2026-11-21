# task26 answer blocks

## Tags

**Domain:** Engineering and Physical Sciences, Energy Systems & Utilities (distribution losses and energy balance: 66/22 kV substation 15-minute limiting-phase peak loading conformed from hourly SCADA, monthly feeder demand registers, transformer voltage drop, and lateral AMI voltage logs).
**Analytical objective:** Data Extraction & Conformation (ETL / Pipeline Build).

## Final Recommendation

**Schedule Phase 1 (2027) firm-capacity relief at Hestmark (146.07% Firm N-1, 22.11 MVA), Raudfjord (110.61%, 9.22 MVA), and Kvernholm (108.61%, 8.74 MVA); Phase 2 (2028-2029) relief at Malmnes (94.99%, 3.80 MVA), Drangvik (94.49%, 4.04 MVA), and Svarthaug (92.73%, 2.61 MVA); and defer Tverrli (68.43%), for 50.51 MVA of total relief capacity (band 48.3 to 52.1 MVA).** This rejects the hourly SCADA, monthly net kVARh power factor, and GIS phase-tag reading, which puts total relief at 19.50 MVA and misplaces five substations (sending Svarthaug to Phase 1 at 114.59% while deferring Drangvik, Kvernholm, Malmnes, and Raudfjord): hourly SCADA smooths 15-minute feeder peaks, monthly net kVARh cancels nighttime leading capacitors against winter-peak lagging load, and GIS phase tags miss unrecorded lateral re-phasing.

## Supplementary Questions

### vesterdal_relief_schedule_2027_2029.xlsx

The workbook opens on `Relief_Schedule` stating the 2027-2029 relief schedule (one row per in-scope substation sorted by Firm N-1 loading percentage with the pool summary totals/average and a horizontal bar chart of each site's Firm N-1 loading percentage), followed by supporting component, reference-validation, routes-comparison, and variant-battery sheets.

1. Estimated 2026 peak 15-minute limiting-phase apparent load (MVA), Firm N-1 loading percentage, relief capacity needed (MVA), and assigned 2027-2029 relief phase for each in-scope substation (21-variant band in parentheses):
   a. Hestmark: 52.88 MVA (51.90 to 53.50), 146.07% Firm N-1 (143.4% to 147.8%), 22.11 MVA relief, Phase 1 (2027).
   b. Raudfjord: 39.82 MVA (39.60 to 40.10), 110.61% Firm N-1 (110.0% to 111.4%), 9.22 MVA relief, Phase 1 (2027).
   c. Kvernholm: 40.19 MVA (39.65 to 41.05), 108.61% Firm N-1 (107.2% to 110.9%), 8.74 MVA relief, Phase 1 (2027).
   d. Malmnes: 36.10 MVA (35.75 to 36.40), 94.99% Firm N-1 (94.1% to 95.8%), 3.80 MVA relief, Phase 2 (2028-2029).
   e. Drangvik: 40.16 MVA (39.65 to 40.65), 94.49% Firm N-1 (93.4% to 95.7%), 4.04 MVA relief, Phase 2 (2028-2029).
   f. Svarthaug: 31.34 MVA (31.15 to 31.60), 92.73% Firm N-1 (92.2% to 93.4%), 2.61 MVA relief, Phase 2 (2028-2029).
   g. Tverrli: 31.48 MVA (31.10 to 31.75), 68.43% Firm N-1 (67.6% to 69.1%), 0.00 MVA relief, Defer.
2. Pool summary across the seven in-scope substations (21-variant band in parentheses):
   a. Combined 2026 peak 15-minute active demand: 229.71 MW (228.4 to 231.0 MW).
   b. Combined 2026 peak-hour reactive demand: 60.72 MVAr (60.0 to 63.9 MVAr).
   c. Unweighted average peak limiting-phase share: 37.69% (37.67% to 37.77%).
   d. Total relief capacity needed: 50.51 MVA (48.3 to 52.1 MVA).

### vesterdal_substation_conformed_2026.csv

Seven rows, one per in-scope substation sorted by Firm N-1 loading percentage, holding each site's Firm N-1 rating, 60-minute SCADA peak, estimated 2026 appropriation filing figures, and assigned relief phase.

3. Underlying 2026 peak 15-minute active demand (MW), peak-hour reactive demand (MVAr), and peak limiting-phase share (%) driving each in-scope substation's loading (21-variant band in parentheses):
   a. Hestmark: 44.55 MW (44.15 to 45.00), 13.53 MVAr (13.40 to 14.05), 37.36% (37.30% to 37.55%).
   b. Raudfjord: 29.02 MW (28.90 to 29.20), 6.34 MVAr (6.20 to 6.75), 44.54% (44.50% to 44.70%).
   c. Kvernholm: 31.08 MW (30.95 to 31.25), 19.19 MVAr (18.80 to 20.50), 36.42% (36.10% to 36.50%).
   d. Malmnes: 33.58 MW (33.35 to 33.85), 2.47 MVAr (2.40 to 2.80), 35.65% (35.60% to 35.85%).
   e. Drangvik: 36.01 MW (35.70 to 36.40), 6.24 MVAr (6.15 to 6.30), 36.39% (36.30% to 36.45%).
   f. Svarthaug: 29.87 MW (29.75 to 29.95), 6.56 MVAr (6.35 to 7.40), 34.05% (34.00% to 34.20%).
   g. Tverrli: 25.60 MW (25.40 to 25.80), 6.38 MVAr (6.30 to 6.75), 39.43% (39.35% to 39.70%).

## Critical Components

1. Combined 2026 peak 15-minute active demand across the seven in-scope substations is **229.71 MW** (band **228.4 to 231.0 MW**).
2. Combined 2026 peak-hour reactive demand across the seven in-scope substations is **60.72 MVAr** (band **60.0 to 63.9 MVAr**).
3. Unweighted average 2026 peak limiting-phase share across the seven in-scope substations is **37.69%** (band **37.67% to 37.77%**).

## Step-by-Step

1. Conformed the operational extracts to the 8,760-hour 2026 Europe/Oslo grid (`scada_substation_hourly_2026.csv`: 82,680 raw rows, 3,840 superseded preliminary rows dropped by latest `extract_ts` to 78,840 clean substation-hours across nine substations, Raudfjord's legacy `DD.MM.YYYY HH:MM` CET stamps aligned, 48 benign summer comms nulls in `v_lv_kv` interpolated; legacy DMS IDs in `feeder_scada_hourly_2026.csv` [kW to MW] and `feeder_demand_registers_monthly_2026.csv` mapped via `feeder_id_crosswalk.csv` across 42 feeders; joined `revenue_meter_monthly_2026.xlsx`, `substation_transformer_register.xlsx`, `substation_phase_bus_voltages_2026.csv`, `gis_lateral_connectivity_2026.csv` [324 laterals], and `ami_lateral_telemetry_2026.db`; excluded streetlighting, oil-DGA, and tariff files). Clean 60-minute SCADA peaks across the seven in-scope substations (Lindberg and Ostervik modernized and excluded per `vesterdal_planning_standard_ns2026.pdf` Section 2) sum to 208.24 MW.
2. The hurried reading stops at those conformed operational tables: taking 60-minute SCADA peaks (208.24 MW), monthly net kVARh power factors (-14.22 MVAr combined), and GIS phase tags (36.33% mean) puts total relief at 19.50 MVA and misplaces five substations (Hestmark 111.23%, Svarthaug 114.59%, Malmnes 82.44%, Kvernholm 81.75%, Raudfjord 81.28%, Drangvik 75.91%, Tverrli 55.06%). Three physical effects overturn it (steps 3 to 5).
3. Reconstructed 15-minute coincident active peaks from `pq_archive_15min_2026.csv` on Lindberg and Ostervik (winter months Jan, Feb, Nov, Dec): calibrated shared industrial-park feeder intra-hour correlation `rho_park = 0.7101`, independent correlation `rho_indep = 0.0447`, intra-hour reactive slope `dQ/dP = 0.3000`, and MW-weighted order-statistic factor `k_ord = 1.0459`, then aggregated each target substation's winter relative feeder excesses `((M15 - P60_m) / P60_m) * P60(h_peak)` in correlated quadrature by `industrial_park_zone` (`substation_transformer_register.xlsx`) onto its 60-minute SCADA peak. Pool total is 229.71 MW (Hestmark 44.55, Drangvik 36.01, Malmnes 33.58, Kvernholm 31.08, Svarthaug 29.87, Raudfjord 29.02, Tverrli 25.60 MW); the 60-minute shortcut gives 208.24 MW and defers Drangvik (82.95%), while a flat reference 15m/60m ratio overshoots to 244.50 MW (66.54 MVA relief).
4. Inverted peak-hour reactive demand from hourly transformer voltage drop `dV = V_hv * (22/66) * (1 + 0.0125 * tap_step) - V_lv` and nameplate impedance `Q_uncal = (22.0 * dV - R_ohm * P_60) / X_ohm`, demeaned over each substation's peak month against monthly mean `net_kvarh / (1000 * hours_in_month)` from `revenue_meter_monthly_2026.xlsx` to eliminate each PT's calibration offset while preserving diurnal reactive swings, averaged over top-5 active-load hours (`Q_h`), and projected to 15-minute peak via `Q_15 = Q_h + dQ/dP * (P_15 - P_60)`. Pool combined `Q_h` is 60.72 MVAr (Kvernholm 19.19, Hestmark 13.53, Svarthaug 6.56, Tverrli 6.38, Raudfjord 6.34, Drangvik 6.24, Malmnes 2.47 MVAr); monthly net kVARh implies -14.22 MVAr and drops Kvernholm to Phase 2 (92.39%), raw un-demeaned `dV` gives 66.67 MVAr (56.57 MVA relief), and class nominal power factors (`engineering_manual_class_pf.csv`) give 97.22 MVAr.
5. Identified each single-phase lateral's physical phase by subtracting hourly 3-phase LV bus mean common mode from 230 V-scaled bus phase voltages (`substation_phase_bus_voltages_2026.csv`) and AMI lateral voltages (`ami_lateral_telemetry_2026.db`), regressing winter hourly first differences on each candidate phase differential and differenced lateral `kW` (requiring positive bus-voltage slope > 0.1), and summing identified lateral kW by phase plus one-third of balanced 3-phase load (`sub_p60 * 1000 - sum(lat_kw)`) over top-5 peak hours. Pool mean `w_max` is 37.69% (Raudfjord 44.54%, Tverrli 39.43%, Hestmark 37.36%, Kvernholm 36.42%, Drangvik 36.39%, Malmnes 35.65%, Svarthaug 34.05%); GIS phase tags give 36.33%, demoting Raudfjord to Phase 2 (86.98%) and promoting Svarthaug to Phase 1 (123.22%).
6. Validated the full pipeline blind on modernized non-target reference substations Lindberg and Ostervik against `pq_archive_15min_2026.csv` and `commissioning_phase_log_2025.csv`: physical phase-ID matches 72 of 72 field-traced laterals (100.0%) against GIS 54 of 72 (75.0%), and mean absolute Firm N-1 loading error across Lindberg (106.15% estimated vs 110.07% measured) and Ostervik (83.07% vs 82.35%) is 2.32 percentage points, beating every rival by 3.8x to 13.0x (un-demeaned `dV` 8.92, flat 15m/60m ratio 9.87, net kVARh PF 10.52, rigorous standard shortcut 11.73, GIS phase tags 13.16, 60-min SCADA 13.51, direct route 30.08).
7. Applied `vesterdal_planning_standard_ns2026.pdf` Sections 3 and 4 (`S_15m = sqrt(P_15^2 + Q_15^2)`, `Lim_MVA = 3 * w_max * S_15m`, `Loading % = 100 * Lim_MVA / Firm_N1_MVA`, `Relief_MVA = max(0, Lim_MVA - 0.85 * Firm_N1_MVA)`, Phase 1 >= 100.0%, Phase 2 >= 85.0%, Defer < 85.0%): combined limiting-phase peak is 271.96 MVA and pool total relief capacity needed is 50.51 MVA, placing Hestmark (146.07%), Raudfjord (110.61%), and Kvernholm (108.61%) in Phase 1, Malmnes (94.99%), Drangvik (94.49%), and Svarthaug (92.73%) in Phase 2, and Tverrli (68.43%) in Defer.
8. Rebuilt the pipeline across all 21 honest modeling variants (all-year and peak-month windows, additive excess scaling, median correlation and `k_ord`, monthly-only `k_ord`, constant `Q_15` and constant PF, winter and full-year voltage-drop anchors, measured `V_lv` scaling, single-hour and top-50 regression peak Q, 6-month heating-season / level / soft-posterior / single-hour phase-ID, and multi-stump combinations) plus six +/-20% perturbations on fitted inputs: every single variant and every perturbation files the identical seven-substation schedule, setting the bands stated above.

No other schedule survives the files. Leaving any single decisive step out alone breaks the schedule: dropping S1 alone puts total relief at 30.01 MVA and defers Drangvik (82.95%); dropping S2 alone puts total relief at 39.24 MVA and demotes Kvernholm to Phase 2 (92.39%); dropping S3 alone puts total relief at 42.46 MVA, demotes Raudfjord to Phase 2 (86.98%), and promotes Svarthaug to Phase 1 (123.22%). Dropping steps in pairs lands on distinct wrong schedules as well (S1+S2 gives 20.23 MVA and misplaces Drangvik at 81.45% and Kvernholm at 87.97%; S1+S3 gives 27.00 MVA and misplaces all five open substations; S2+S3 gives 31.78 MVA and misplaces Kvernholm, Raudfjord, and Svarthaug), dropping all three gives 19.50 MVA with five substations misplaced, and the rigorous standard shortcut (hourly coincidence times feeder 15-minute registers, class nominal power factors, and GIS phase tags) gives 64.88 MVA and misplaces all five open substations (Drangvik 106.79%, Malmnes 107.31%, Svarthaug 134.10%, Kvernholm 96.42%, Raudfjord 94.86%). Every shortcut fails the blind reference check on Lindberg and Ostervik by 3.8x to 13.0x while every honest modeling variant and forcing perturbation preserves the exact seven-substation schedule.
