"""Emit task26/submission.md strictly from generator/figures.json (four graded answer blocks + Tags, zero em dashes)."""


def write(path, fig):
    subs = fig["substations"]
    b = fig["bands"]
    rp = fig["ref_params"]
    rm = fig["ref_mae"]
    rr = fig["ref_ratios"]
    ps = fig["pack_stats"]
    rf = fig["routes"]["S1+S2+S3"]
    rg = fig["routes"]["rigorous"]
    dr = fig["routes"]["direct"]

    ordered = sorted(fig["targets"], key=lambda s: -subs[s]["loading_pct"])
    p1_str = ", ".join(f"{s} ({subs[s]['loading_pct']:.1f}%, {subs[s]['lim_mva']:.2f} MVA, {subs[s]['relief_mva']:.2f} MVA relief)"
                       for s in ordered if subs[s]["phase"] == "Phase 1 (2027)")
    p2_str = ", ".join(f"{s} ({subs[s]['loading_pct']:.1f}%, {subs[s]['lim_mva']:.2f} MVA, {subs[s]['relief_mva']:.2f} MVA relief)"
                       for s in ordered if subs[s]["phase"] == "Phase 2 (2028-2029)")
    df_str = ", ".join(f"{s} ({subs[s]['loading_pct']:.1f}%, {subs[s]['lim_mva']:.2f} MVA, {subs[s]['relief_mva']:.2f} MVA relief)"
                       for s in ordered if subs[s]["phase"] == "Defer")

    sub_rows = []
    for s in ordered:
        r = subs[s]
        lb = b["loading_pct"][s]
        mb = b["lim_mva"][s]
        pb = b["p15_mw"][s]
        qb = b["q_peak_mvar"][s]
        wb_ = b["w_max_pct"][s]
        sub_rows.append(
            f"| {s} | {r['firm_n1_mva']:.1f} | {r['p15_peak_mw']:.2f} ({pb[0]:.2f} to {pb[1]:.2f}) | "
            f"{r['q_peak_h_mvar']:.2f} ({qb[0]:.2f} to {qb[1]:.2f}) | {r['w_max_pct']:.2f}% ({wb_[0]:.2f}% to {wb_[1]:.2f}%) | "
            f"{r['lim_mva']:.2f} ({mb[0]:.2f} to {mb[1]:.2f}) | {r['loading_pct']:.2f}% ({lb[0]:.1f}% to {lb[1]:.1f}%) | "
            f"{r['relief_mva']:.2f} | {r['phase']} |"
        )
    sub_table = "\n".join(sub_rows)

    lb_r = subs["Lindberg"]
    os_r = subs["Ostervik"]

    lines = [
        "# Vesterdal Nett AS 2027-2029 Substation Firm-Capacity Relief Schedule",
        "",
        "## Final Recommendation",
        "",
        f"Under Network Planning Standard NS-2026 (Phase 1 urgent relief >= {fig['planning_lines']['phase1_pct']:.1f}% Firm N-1 MVA, "
        f"Phase 2 staged relief >= {fig['planning_lines']['phase2_pct']:.1f}% and < {fig['planning_lines']['phase1_pct']:.1f}%, Defer < {fig['planning_lines']['phase2_pct']:.1f}%, "
        f"with relief capacity sized above the {fig['planning_lines']['phase2_pct']:.1f}% Firm N-1 planning ceiling), the seven in-scope 66/22 kV substations are scheduled as follows:",
        "",
        f"- **Phase 1 (2027 urgent relief):** {p1_str}.",
        f"- **Phase 2 (2028-2029 staged relief):** {p2_str}.",
        f"- **Defer (post-2029):** {df_str}.",
        f"- **Pool Total Relief Capacity Needed:** **{fig['total_relief_mva']:.2f} MVA** (21-variant band {fig['total_relief_band'][0]:.1f} to {fig['total_relief_band'][1]:.1f} MVA).",
        "",
        f"Lindberg ({lb_r['truth_loading_pct_1dp']:.1f}% measured vs {lb_r['loading_pct']:.1f}% estimated) and Ostervik "
        f"({os_r['truth_loading_pct_1dp']:.1f}% measured vs {os_r['loading_pct']:.1f}% estimated) were modernized in 2023-2024 and are excluded from the 2027-2029 relief pool per NS-2026 Section 2. "
        f"Every single one of the {ps['n_variants']} honest modeling variants and all six +/-20% perturbations on fitted inputs file this exact seven-substation schedule. "
        f"By contrast, the reflex shortcut (60-minute SCADA peak, monthly net kVARh power factor, and GIS phase tags) misplaces five substations and puts total relief at {rf['total_relief_mva']:.2f} MVA, "
        f"while the rigorous standard shortcut (hourly coincidence times feeder 15-min registers, class nominal power factors, and GIS phase tags) misplaces all five open substations and puts total relief at {rg['total_relief_mva']:.2f} MVA.",
        "",
        "## Supplementary Questions",
        "",
        "Conformed 2026 peak metrics across all seven in-scope substations (each figure shown with its 21-variant band):",
        "",
        "| Substation | Firm N-1 (MVA) | Peak 15-Min Active (MW) | Peak-Hour Reactive (MVAr) | Peak Limiting-Phase Share (%) | Peak 15-Min Lim-Phase (MVA) | Firm N-1 Loading (%) | Relief Needed (MVA) | Assigned Phase |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---|",
        sub_table,
        "",
        f"- **Pool combined 2026 peak 15-minute active demand:** **{fig['c1_total_p15_mw']:.2f} MW** (band {fig['c1_band'][0]:.1f} to {fig['c1_band'][1]:.1f} MW; raw 60-min SCADA peaks sum to {fig['r1_p60_sum_mw']:.2f} MW).",
        f"- **Pool combined 2026 peak-hour reactive demand:** **{fig['c2_total_qpeak_mvar']:.2f} MVAr** (band {fig['c2_band'][0]:.1f} to {fig['c2_band'][1]:.1f} MVAr; monthly net kVARh implies {rf['c2_total_qpeak_mvar']:.2f} MVAr and class nominal PFs imply {rg['c2_total_qpeak_mvar']:.2f} MVAr).",
        f"- **Pool average peak limiting-phase share:** **{fig['c3_mean_lim_phase_pct']:.2f}%** (band {fig['c3_band'][0]:.2f}% to {fig['c3_band'][1]:.2f}%; GIS phase tags give {rf['c3_mean_lim_phase_pct']:.2f}%).",
        f"- **Pool total relief capacity needed:** **{fig['total_relief_mva']:.2f} MVA** (band {fig['total_relief_band'][0]:.1f} to {fig['total_relief_band'][1]:.1f} MVA).",
        "",
        "Deliverables cut strictly from these conformed figures: `vesterdal_relief_schedule_2027_2029.xlsx` (opening on `Relief_Schedule` with the final schedule, pool totals, and embedded horizontal loading chart, plus supporting sheets) and `vesterdal_substation_conformed_2026.csv` (one conformed row per in-scope substation).",
        "",
        "## Critical Components",
        "",
        f"1. **Component 1 (15-Minute Coincident Active Peak Conformation):** Pool combined 2026 peak 15-minute active demand is **{fig['c1_total_p15_mw']:.2f} MW** (band {fig['c1_band'][0]:.1f} to {fig['c1_band'][1]:.1f} MW), reconstructed by correlated quadrature aggregation of monthly non-coincident feeder 15-minute excesses calibrated on Lindberg and Ostervik (rho_park = {rp['rho_park']:.4f}, rho_indep = {rp['rho_indep']:.4f}, k_ord = {rp['k_ord']:.4f}). Leaving this step out alone drops combined active demand to {fig['routes']['S1']['c1_total_p15_mw']:.2f} MW and flips Drangvik from Phase 2 ({subs['Drangvik']['loading_pct']:.1f}%) to Defer ({fig['routes']['S1']['loading_pct']['Drangvik']:.1f}%).",
        f"2. **Component 2 (Peak-Hour Reactive Power Inversion with PT Demeaning):** Pool combined 2026 peak-hour reactive demand is **{fig['c2_total_qpeak_mvar']:.2f} MVAr** (band {fig['c2_band'][0]:.1f} to {fig['c2_band'][1]:.1f} MVAr), inverted from hourly HV/LV bus voltage drop across transformer nameplate resistance and reactance with LTC tap steps ({fig['planning_lines']['tap_step_pct']:.2f}% per step) and demeaned against monthly net kVARh to remove each substation's PT offset. Leaving this step out alone drops combined reactive demand to {fig['routes']['S2']['c2_total_qpeak_mvar']:.2f} MVAr and flips Kvernholm from Phase 1 ({subs['Kvernholm']['loading_pct']:.1f}%) to Phase 2 ({fig['routes']['S2']['loading_pct']['Kvernholm']:.1f}%).",
        f"3. **Component 3 (Physical Lateral Phase Identification):** Pool average peak limiting-phase share is **{fig['c3_mean_lim_phase_pct']:.2f}%** (band {fig['c3_band'][0]:.2f}% to {fig['c3_band'][1]:.2f}%), recovered by regressing common-mode-rejected hourly AMI lateral voltage differentials on three-phase substation bus voltage differentials controlling for local lateral load drop (matching {rp['tracer_matched']} of {rp['tracer_total']} field-traced laterals on Lindberg and Ostervik vs GIS {rp['gis_tracer_matched']} of {rp['tracer_total']}, {rp['gis_tracer_pct']:.1f}%). Leaving this step out alone drops the pool average to {fig['routes']['S3']['c3_mean_lim_phase_pct']:.2f}%, flips Raudfjord from Phase 1 ({subs['Raudfjord']['loading_pct']:.1f}%) to Phase 2 ({fig['routes']['S3']['loading_pct']['Raudfjord']:.1f}%), and flips Svarthaug from Phase 2 ({subs['Svarthaug']['loading_pct']:.1f}%) to Phase 1 ({fig['routes']['S3']['loading_pct']['Svarthaug']:.1f}%).",
        "",
        "## Step-by-Step",
        "",
        f"1. **Conform Multi-System Operational Extracts (R1):** Load `scada_substation_hourly_2026.csv` ({ps['raw_scada_rows']:,} raw rows), deduplicate superseded preliminary batches (`extract_ts` latest wins, dropping {ps['superseded_dropped']:,} preliminary rows to obtain {ps['clean_scada_rows']:,} clean substation-hours across 9 substations), align both Europe/Oslo CET/CEST ISO-8601 timestamps and Raudfjord's legacy `DD.MM.YYYY HH:MM` CET standard stamps to the exact 8,760-hour calendar-year 2026 Europe/Oslo grid, and linearly interpolate {ps['vlv_nulls']} benign off-peak summer comms nulls in `v_lv_kv`. Map legacy DMS feeder IDs across `feeder_scada_hourly_2026.csv` (converting kW to MW) and `feeder_demand_registers_monthly_2026.csv` using `feeder_id_crosswalk.csv` ({ps['n_feeders']} feeders total). Load monthly revenue kWh and net kVARh from `revenue_meter_monthly_2026.xlsx`, transformer ratings and impedances from `substation_transformer_register.xlsx`, hourly 3-phase LV bus voltages from `substation_phase_bus_voltages_2026.csv`, GIS tags from `gis_lateral_connectivity_2026.csv` ({ps['n_laterals_total']} laterals), and heating-season hourly AMI voltages and loads from `ami_lateral_telemetry_2026.db`. Exclude unused maintenance, streetlighting, and tariff files. Clean annual 60-minute SCADA peaks across the seven target substations sum to {fig['r1_p60_sum_mw']:.2f} MW.",
        f"2. **Reconstruct 15-Minute Coincident Active Peaks via Correlated Quadrature (R2):** On modernized substations Lindberg and Ostervik (`pq_archive_15min_2026.csv`), compute intra-hour feeder deviations `dP_15 - P_60` during winter months (Jan, Feb, Nov, Dec) to estimate shared industrial-park feeder correlation `rho_park = {rp['rho_park']:.4f}`, independent feeder correlation `rho_indep = {rp['rho_indep']:.4f}`, and intra-hour reactive slope `dQ/dP = {rp['dq_dp']:.4f}`. Calibrate the order-statistic scaling ratio `k_ord = {rp['k_ord']:.4f}` as the MW-weighted ratio of observed substation 15-minute peak excess to raw correlated quadrature across Lindberg and Ostervik winter monthly and annual peaks. For each target substation, compute each feeder's winter-average relative 15-minute excess `((M15 - P60_m) / P60_m) * P60(h_peak)`, combine feeders in correlated quadrature using `industrial_park_zone` from `substation_transformer_register.xlsx`, and add `k_ord * raw_quad` to the annual 60-minute SCADA peak. Pool total = {fig['c1_total_p15_mw']:.2f} MW (Drangvik {subs['Drangvik']['p15_peak_mw']:.2f}, Hestmark {subs['Hestmark']['p15_peak_mw']:.2f}, Kvernholm {subs['Kvernholm']['p15_peak_mw']:.2f}, Malmnes {subs['Malmnes']['p15_peak_mw']:.2f}, Raudfjord {subs['Raudfjord']['p15_peak_mw']:.2f}, Svarthaug {subs['Svarthaug']['p15_peak_mw']:.2f}, Tverrli {subs['Tverrli']['p15_peak_mw']:.2f} MW).",
        f"3. **Invert Peak-Hour Reactive Demand from Transformer Voltage Drop and Net kVARh (R3):** For each substation and hour, compute tap-adjusted secondary voltage ratio `tau = (22/66) * (1 + 0.0125 * tap_step)`, voltage drop `dV = V_hv * tau - V_lv`, and uncalibrated hourly reactive power `Q_uncal = (22.0 * dV - R_ohm * P_60) / X_ohm`. Because inductive potential transformers carry individual calibration offsets, demean `Q_uncal` over the substation's peak month against the monthly mean net reactive power `net_kvarh / (1000 * hours_in_month)` from `revenue_meter_monthly_2026.xlsx`, eliminating PT offset algebraically while preserving diurnal reactive swings. Average demeaned `Q_hat` over the substation's top-5 active-load hours to obtain peak-hour reactive demand `Q_h`, and project to the 15-minute peak via `Q_15 = Q_h + dQ/dP * (P_15 - P_60)`. Pool combined `Q_h` = {fig['c2_total_qpeak_mvar']:.2f} MVAr (Kvernholm {subs['Kvernholm']['q_peak_h_mvar']:.2f}, Hestmark {subs['Hestmark']['q_peak_h_mvar']:.2f}, Svarthaug {subs['Svarthaug']['q_peak_h_mvar']:.2f}, Tverrli {subs['Tverrli']['q_peak_h_mvar']:.2f}, Raudfjord {subs['Raudfjord']['q_peak_h_mvar']:.2f}, Drangvik {subs['Drangvik']['q_peak_h_mvar']:.2f}, Malmnes {subs['Malmnes']['q_peak_h_mvar']:.2f} MVAr).",
        f"4. **Identify Physical Single-Phase Lateral Connectivity and Peak Limiting-Phase Share (R4):** Convert 3-phase LV bus voltages from kV to 230 V phase-to-neutral scale, subtract the hourly 3-phase mean common-mode bus voltage from both bus phases and AMI lateral voltages, and take hourly first differences over winter months. For each lateral, regress differenced common-mode-rejected lateral voltage on each candidate bus phase differential (`A`, `B`, `C`) and differenced lateral active load `dP_kW` (requiring positive bus-voltage slope > 0.1), assigning the physical phase with minimum residual sum of squares. Sum identified single-phase lateral kW by phase plus one-third of balanced three-phase load (`sub_p60 * 1000 - sum(lat_kw)`) over the top-5 peak hours to obtain `w_max`. Pool mean = {fig['c3_mean_lim_phase_pct']:.2f}% (Raudfjord {subs['Raudfjord']['w_max_pct']:.2f}%, Tverrli {subs['Tverrli']['w_max_pct']:.2f}%, Hestmark {subs['Hestmark']['w_max_pct']:.2f}%, Kvernholm {subs['Kvernholm']['w_max_pct']:.2f}%, Drangvik {subs['Drangvik']['w_max_pct']:.2f}%, Malmnes {subs['Malmnes']['w_max_pct']:.2f}%, Svarthaug {subs['Svarthaug']['w_max_pct']:.2f}%).",
        f"5. **Validate Against Modernized Reference Substations (R5):** Test the end-to-end pipeline blind on Lindberg and Ostervik against their measured 15-minute PQ archives (`pq_archive_15min_2026.csv`) and 2025 field phase-tracer commissioning log (`commissioning_phase_log_2025.csv`). Physical phase-ID matches {rp['tracer_matched']} of {rp['tracer_total']} laterals (100.0%) compared to GIS's {rp['gis_tracer_matched']} of {rp['tracer_total']} ({rp['gis_tracer_pct']:.1f}%). Mean absolute Firm N-1 loading error across Lindberg ({lb_r['loading_pct']:.2f}% vs {lb_r['truth_loading_pct']:.2f}%) and Ostervik ({os_r['loading_pct']:.2f}% vs {os_r['truth_loading_pct']:.2f}%) is **{rm['golden']:.2f} pct pts**, outperforming every shortcut by {min(rr.values()):.1f}x to {max(rr.values()):.1f}x: raw un-demeaned dV {rm['s2_raw_dv_no_demean']:.2f} ({rr['s2_raw_dv_no_demean']:.1f}x), flat 15m/60m ratio {rm['s1_flat_ratio']:.2f} ({rr['s1_flat_ratio']:.1f}x), net kVARh PF {rm['s2_net_kvarh']:.2f} ({rr['s2_net_kvarh']:.1f}x), rigorous standard route {rm['rigorous']:.2f} ({rr['rigorous']:.1f}x), GIS phase tags {rm['s3_gis_phase']:.2f} ({rr['s3_gis_phase']:.1f}x), 60-min SCADA {rm['s1_scada60']:.2f} ({rr['s1_scada60']:.1f}x), and direct route {rm['direct']:.2f} ({rr['direct']:.1f}x).",
        f"6. **Synthesize Apparent Peak Loading, Relief Capacity, Schedule, and Robustness Battery (R6 to R8):** Compute `S_15m = sqrt(P_15^2 + Q_15^2)`, `Lim_MVA = 3 * w_max * S_15m`, `Loading % = 100 * Lim_MVA / Firm_N1_MVA`, and `Relief_MVA = max(0, Lim_MVA - 0.85 * Firm_N1_MVA)` per NS-2026 Section 3, then assign tiers per Section 4 (`>= 100.0%` Phase 1, `>= 85.0%` Phase 2, `< 85.0%` Defer). Re-run across all {ps['n_variants']} honest modeling variants (all-year/peak-month windows, additive excess scaling, median correlation and `k_ord`, monthly-only `k_ord`, constant `Q_15` / constant PF, winter/annual voltage-drop anchors, measured `V_lv` scaling, single-hour / top-50 regression peak Q, 6-month heating-season / level / soft-posterior / single-hour phase-ID, and multi-stump combinations) plus six +/-20% forcing perturbations: every variant and every perturbation files the identical 7-substation schedule, establishing the bands reported above.",
        "",
        "## Tags",
        "",
        "- Domain: Energy Systems & Utilities (`distribution-losses-energy-balance`)",
        "- Objective: Data Extraction & Conformation (ETL / Pipeline Build)",
        "- Answer shape: schedule-capacity (2027-2029 substation firm-capacity relief schedule)",
        "- Deliverables: `vesterdal_relief_schedule_2027_2029.xlsx`, `vesterdal_substation_conformed_2026.csv`",
        "",
    ]
    text = "\n".join(lines)
    assert "\u2014" not in text and "\u2013" not in text, "em/en dash found in submission.md"
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
