"""Emit task26/submission.md strictly from generator/figures.json following submission-writeup/SKILL.md:
- Tags (2 lines at top)
- Final Recommendation (2 sentences max: bold call answering both parts of the main ask, plus what it rejects and why)
- Supplementary Questions (grouped by deliverable file, 3 numbered multi-faceted asks with a/b/c member lines, no tables)
- Critical Components (3 one-liners: pure answer + unit + band, zero method clauses, strictly independent)
- Step-by-Step (8 numbered steps + closing unnumbered independence/uniqueness passage)
Zero em/en dashes; every figure drawn strictly from figures.json.
"""


def write(path, fig):
    subs = fig["substations"]
    b = fig["bands"]
    rp = fig["ref_params"]
    rm = fig["ref_mae"]
    rr = fig["ref_ratios"]
    ps = fig["pack_stats"]
    rt = fig["routes"]
    rf = rt["S1+S2+S3"]
    rg = rt["rigorous"]

    def _join_and(items):
        if len(items) <= 1:
            return "".join(items)
        if len(items) == 2:
            return f"{items[0]} and {items[1]}"
        return ", ".join(items[:-1]) + f", and {items[-1]}"

    ordered = sorted(fig["targets"], key=lambda s: -subs[s]["loading_pct"])
    p1_str = _join_and([
        f"{s} ({subs[s]['loading_pct']:.2f}% Firm N-1, {subs[s]['relief_mva']:.2f} MVA)"
        if i == 0 else f"{s} ({subs[s]['loading_pct']:.2f}%, {subs[s]['relief_mva']:.2f} MVA)"
        for i, s in enumerate(s for s in ordered if subs[s]["phase"] == "Phase 1 (2027)")
    ])
    p2_str = _join_and([
        f"{s} ({subs[s]['loading_pct']:.2f}%, {subs[s]['relief_mva']:.2f} MVA)"
        for s in ordered if subs[s]["phase"] == "Phase 2 (2028-2029)"
    ])
    df_str = _join_and([
        f"{s} ({subs[s]['loading_pct']:.2f}%)"
        for s in ordered if subs[s]["phase"] == "Defer"
    ])

    letters = "abcdefg"
    ask1_lines = []
    ask3_lines = []
    for ch, s in zip(letters, ordered):
        r = subs[s]
        lb = b["loading_pct"][s]
        mb = b["lim_mva"][s]
        pb = b["p15_mw"][s]
        qb = b["q_peak_mvar"][s]
        wb = b["w_max_pct"][s]
        ask1_lines.append(
            f"   {ch}. {s}: {r['lim_mva']:.2f} MVA ({mb[0]:.2f} to {mb[1]:.2f}), "
            f"{r['loading_pct']:.2f}% Firm N-1 ({lb[0]:.1f}% to {lb[1]:.1f}%), "
            f"{r['relief_mva']:.2f} MVA relief, {r['phase']}."
        )
        ask3_lines.append(
            f"   {ch}. {s}: {r['p15_peak_mw']:.2f} MW ({pb[0]:.2f} to {pb[1]:.2f}), "
            f"{r['q_peak_h_mvar']:.2f} MVAr ({qb[0]:.2f} to {qb[1]:.2f}), "
            f"{r['w_max_pct']:.2f}% ({wb[0]:.2f}% to {wb[1]:.2f}%)."
        )

    fh_r = subs["Fossheim"]
    lb_r = subs["Lindberg"]
    os_r = subs["Ostervik"]
    sb_r = subs["Solberg"]

    lines = [
        "# task26 answer blocks",
        "",
        "## Tags",
        "",
        "**Domain:** Engineering and Physical Sciences, Energy Systems & Utilities (distribution losses and energy balance: 66/22 kV substation 15-minute limiting-phase peak loading conformed from hourly SCADA, monthly feeder demand registers, transformer voltage drop, and lateral AMI voltage logs).",
        "**Analytical objective:** Data Extraction & Conformation (ETL / Pipeline Build).",
        "",
        "## Final Recommendation",
        "",
        f"**Schedule Phase 1 (2027) firm-capacity relief at {p1_str}; Phase 2 (2028-2029) relief at {p2_str}; and defer {df_str}, for {fig['total_relief_mva']:.2f} MVA of total relief capacity (band {fig['total_relief_band'][0]:.1f} to {fig['total_relief_band'][1]:.1f} MVA).** "
        f"This rejects the hourly SCADA, monthly net kVARh power factor, and GIS phase-tag reading, which puts total relief at {rf['total_relief_mva']:.2f} MVA and misplaces five substations (sending Svarthaug to Phase 1 at {rf['loading_pct']['Svarthaug']:.2f}% while deferring Drangvik, Kvernholm, Malmnes, and Raudfjord): hourly SCADA smooths 15-minute feeder peaks, monthly net kVARh cancels nighttime leading capacitors against winter-peak lagging load, and GIS phase tags miss unrecorded lateral re-phasing.",
        "",
        "## Supplementary Questions",
        "",
        "### vesterdal_relief_schedule_2027_2029.xlsx",
        "",
        "The workbook opens on `Relief_Schedule` stating the 2027-2029 relief schedule (one row per in-scope substation sorted by Firm N-1 loading percentage with the pool summary totals/average and a horizontal bar chart of each site's Firm N-1 loading percentage), followed by supporting component, reference-validation, routes-comparison, and variant-battery sheets.",
        "",
        "1. Estimated 2026 peak 15-minute limiting-phase apparent load (MVA), Firm N-1 loading percentage, relief capacity needed (MVA), and assigned 2027-2029 relief phase for each in-scope substation (21-variant band in parentheses):",
        *ask1_lines,
        "2. Pool summary across the seven in-scope substations (21-variant band in parentheses):",
        f"   a. Combined 2026 peak 15-minute active demand: {fig['c1_total_p15_mw']:.2f} MW ({fig['c1_band'][0]:.1f} to {fig['c1_band'][1]:.1f} MW).",
        f"   b. Combined 2026 peak-hour reactive demand: {fig['c2_total_qpeak_mvar']:.2f} MVAr ({fig['c2_band'][0]:.1f} to {fig['c2_band'][1]:.1f} MVAr).",
        f"   c. Unweighted average peak limiting-phase share: {fig['c3_mean_lim_phase_pct']:.2f}% ({fig['c3_band'][0]:.2f}% to {fig['c3_band'][1]:.2f}%).",
        f"   d. Total relief capacity needed: {fig['total_relief_mva']:.2f} MVA ({fig['total_relief_band'][0]:.1f} to {fig['total_relief_band'][1]:.1f} MVA).",
        "",
        "### vesterdal_substation_conformed_2026.csv",
        "",
        "Seven rows, one per in-scope substation sorted by Firm N-1 loading percentage, holding each site's Firm N-1 rating, 60-minute SCADA peak, estimated 2026 appropriation filing figures, and assigned relief phase.",
        "",
        "3. Underlying 2026 peak 15-minute active demand (MW), peak-hour reactive demand (MVAr), and peak limiting-phase share (%) driving each in-scope substation's loading (21-variant band in parentheses):",
        *ask3_lines,
        "",
        "## Critical Components",
        "",
        f"1. Combined 2026 peak 15-minute active demand across the seven in-scope substations is **{fig['c1_total_p15_mw']:.2f} MW** (band **{fig['c1_band'][0]:.1f} to {fig['c1_band'][1]:.1f} MW**).",
        f"2. Combined 2026 peak-hour reactive demand across the seven in-scope substations is **{fig['c2_total_qpeak_mvar']:.2f} MVAr** (band **{fig['c2_band'][0]:.1f} to {fig['c2_band'][1]:.1f} MVAr**).",
        f"3. Unweighted average 2026 peak limiting-phase share across the seven in-scope substations is **{fig['c3_mean_lim_phase_pct']:.2f}%** (band **{fig['c3_band'][0]:.2f}% to {fig['c3_band'][1]:.2f}%**).",
        "",
        "## Step-by-Step",
        "",
        f"1. Conformed the operational extracts to the 8,760-hour 2026 Europe/Oslo grid (`scada_substation_hourly_2026.csv`: {ps['raw_scada_rows']:,} raw rows, {ps['superseded_dropped']:,} superseded preliminary rows dropped by latest `extract_ts` to {ps['clean_scada_rows']:,} clean substation-hours across eleven substations, Raudfjord's legacy `DD.MM.YYYY HH:MM` CET stamps aligned, {ps['vlv_nulls']} benign summer comms nulls in `v_lv_kv` interpolated; legacy DMS IDs in `feeder_scada_hourly_2026.csv` [kW to MW] and `feeder_demand_registers_monthly_2026.csv` mapped via `feeder_id_crosswalk.csv` across {ps['n_feeders']} feeders; joined `revenue_meter_monthly_2026.xlsx`, `substation_transformer_register.xlsx`, `substation_phase_bus_voltages_2026.csv`, `gis_lateral_connectivity_2026.csv` [{ps['n_laterals_total']} laterals], and `ami_lateral_telemetry_2026.db`; excluded streetlighting, oil-DGA, and tariff files). Clean 60-minute SCADA peaks across the seven in-scope substations (Fossheim, Lindberg, Ostervik, and Solberg modernized and excluded per `vesterdal_planning_standard_ns2026.pdf` Section 2) sum to {fig['r1_p60_sum_mw']:.2f} MW.",
        f"2. The hurried reading stops at those conformed operational tables: taking 60-minute SCADA peaks ({fig['r1_p60_sum_mw']:.2f} MW), monthly net kVARh power factors ({rf['c2_total_qpeak_mvar']:.2f} MVAr combined), and GIS phase tags ({rf['c3_mean_lim_phase_pct']:.2f}% mean) puts total relief at {rf['total_relief_mva']:.2f} MVA and misplaces five substations (Hestmark {rf['loading_pct']['Hestmark']:.2f}%, Svarthaug {rf['loading_pct']['Svarthaug']:.2f}%, Malmnes {rf['loading_pct']['Malmnes']:.2f}%, Kvernholm {rf['loading_pct']['Kvernholm']:.2f}%, Raudfjord {rf['loading_pct']['Raudfjord']:.2f}%, Drangvik {rf['loading_pct']['Drangvik']:.2f}%, Tverrli {rf['loading_pct']['Tverrli']:.2f}%). Three physical effects overturn it (steps 3 to 5).",
        f"3. Reconstructed 15-minute coincident active peaks from `pq_archive_15min_2026.csv` on Fossheim, Lindberg, Ostervik, and Solberg (winter months Jan, Feb, Nov, Dec): calibrated shared industrial-park feeder intra-hour correlation `rho_park = {rp['rho_park']:.4f}`, independent correlation `rho_indep = {rp['rho_indep']:.4f}`, intra-hour reactive slope `dQ/dP = {rp['dq_dp']:.4f}`, and MW-weighted order-statistic factor `k_ord = {rp['k_ord']:.4f}`, then aggregated each target substation's winter relative feeder excesses `((M15 - P60_m) / P60_m) * P60(h_peak)` in correlated quadrature by `industrial_park_zone` (`substation_transformer_register.xlsx`) onto its 60-minute SCADA peak. Pool total is {fig['c1_total_p15_mw']:.2f} MW (Hestmark {subs['Hestmark']['p15_peak_mw']:.2f}, Drangvik {subs['Drangvik']['p15_peak_mw']:.2f}, Malmnes {subs['Malmnes']['p15_peak_mw']:.2f}, Kvernholm {subs['Kvernholm']['p15_peak_mw']:.2f}, Svarthaug {subs['Svarthaug']['p15_peak_mw']:.2f}, Raudfjord {subs['Raudfjord']['p15_peak_mw']:.2f}, Tverrli {subs['Tverrli']['p15_peak_mw']:.2f} MW); the 60-minute shortcut gives {rt['S1']['c1_total_p15_mw']:.2f} MW and defers Drangvik ({rt['S1']['loading_pct']['Drangvik']:.2f}%), linear summation of feeder 15m/60m ratios at peak hour overshoots to {rt['s1_linear_sum']['c1_total_p15_mw']:.2f} MW ({rt['s1_linear_sum']['total_relief_mva']:.2f} MVA relief), zone-matched register coincidence (`CF_park = {rp['cf_park']:.4f}`, `CF_nonpark = {rp['cf_nonpark']:.4f}`) gives {rt['s1_cf_zone']['c1_total_p15_mw']:.2f} MW ({rt['s1_cf_zone']['total_relief_mva']:.2f} MVA relief), pooled register coincidence (`CF = {rp['cf_pooled']:.4f}`) gives {rt['s1_cf_pooled']['c1_total_p15_mw']:.2f} MW ({rt['s1_cf_pooled']['total_relief_mva']:.2f} MVA relief), and a flat reference 15m/60m ratio overshoots to {rt['s1_flat_ratio']['c1_total_p15_mw']:.2f} MW ({rt['s1_flat_ratio']['total_relief_mva']:.2f} MVA relief).",
        f"4. Inverted peak-hour reactive demand from hourly transformer voltage drop `dV = V_hv * (22/66) * (1 + 0.0125 * tap_step) - V_lv` and nameplate impedance `Q_uncal = (22.0 * dV - R_ohm * P_60) / X_ohm`, demeaned over each substation's peak month against monthly mean `net_kvarh / (1000 * hours_in_month)` from `revenue_meter_monthly_2026.xlsx` to eliminate each PT's calibration offset while preserving diurnal reactive swings, averaged over top-5 active-load hours (`Q_h`), and projected to 15-minute peak via `Q_15 = Q_h + dQ/dP * (P_15 - P_60)`. Pool combined `Q_h` is {fig['c2_total_qpeak_mvar']:.2f} MVAr (Kvernholm {subs['Kvernholm']['q_peak_h_mvar']:.2f}, Hestmark {subs['Hestmark']['q_peak_h_mvar']:.2f}, Svarthaug {subs['Svarthaug']['q_peak_h_mvar']:.2f}, Tverrli {subs['Tverrli']['q_peak_h_mvar']:.2f}, Raudfjord {subs['Raudfjord']['q_peak_h_mvar']:.2f}, Drangvik {subs['Drangvik']['q_peak_h_mvar']:.2f}, Malmnes {subs['Malmnes']['q_peak_h_mvar']:.2f} MVAr); monthly net kVARh implies {rt['S2']['c2_total_qpeak_mvar']:.2f} MVAr and drops Kvernholm to Phase 2 ({rt['S2']['loading_pct']['Kvernholm']:.2f}%), raw un-demeaned `dV` gives {rt['s2_raw_dv_no_demean']['c2_total_qpeak_mvar']:.2f} MVAr ({rt['s2_raw_dv_no_demean']['total_relief_mva']:.2f} MVA relief), and class nominal power factors (`engineering_manual_class_pf.csv`) give {rg['c2_total_qpeak_mvar']:.2f} MVAr.",
        f"5. Identified each single-phase lateral's physical phase by subtracting hourly 3-phase LV bus mean common mode from 230 V-scaled bus phase voltages (`substation_phase_bus_voltages_2026.csv`) and AMI lateral voltages (`ami_lateral_telemetry_2026.db`), regressing winter hourly first differences on each candidate phase differential and differenced lateral `kW` (requiring positive bus-voltage slope > 0.1), and summing identified lateral kW by phase plus one-third of balanced 3-phase load (`sub_p60 * 1000 - sum(lat_kw)`) over top-5 peak hours. Pool mean `w_max` is {fig['c3_mean_lim_phase_pct']:.2f}% (Raudfjord {subs['Raudfjord']['w_max_pct']:.2f}%, Tverrli {subs['Tverrli']['w_max_pct']:.2f}%, Hestmark {subs['Hestmark']['w_max_pct']:.2f}%, Kvernholm {subs['Kvernholm']['w_max_pct']:.2f}%, Drangvik {subs['Drangvik']['w_max_pct']:.2f}%, Malmnes {subs['Malmnes']['w_max_pct']:.2f}%, Svarthaug {subs['Svarthaug']['w_max_pct']:.2f}%); GIS phase tags give {rt['S3']['c3_mean_lim_phase_pct']:.2f}%, demoting Raudfjord to Phase 2 ({rt['S3']['loading_pct']['Raudfjord']:.2f}%) and promoting Svarthaug to Phase 1 ({rt['S3']['loading_pct']['Svarthaug']:.2f}%).",
        f"6. Validated the full pipeline blind on all four modernized non-target reference substations (Fossheim, Lindberg, Ostervik, and Solberg) against `pq_archive_15min_2026.csv` and `commissioning_phase_log_2025.csv`: physical phase-ID matches {rp['tracer_matched']} of {rp['tracer_total']} field-traced laterals (100.0%) against GIS {rp['gis_tracer_matched']} of {rp['tracer_total']} ({rp['gis_tracer_pct']:.1f}%), and mean absolute Firm N-1 loading error across Fossheim ({fh_r['loading_pct']:.2f}% estimated vs {fh_r['truth_loading_pct']:.2f}% measured), Lindberg ({lb_r['loading_pct']:.2f}% vs {lb_r['truth_loading_pct']:.2f}%), Ostervik ({os_r['loading_pct']:.2f}% vs {os_r['truth_loading_pct']:.2f}%), and Solberg ({sb_r['loading_pct']:.2f}% vs {sb_r['truth_loading_pct']:.2f}%) is {rm['golden']:.2f} percentage points, beating every rival by {min(rr.values()):.1f}x to {max(rr.values()):.1f}x (zone-matched register coincidence {rm['s1_cf_zone']:.2f}, pooled register coincidence {rm['s1_cf_pooled']:.2f}, linear feeder ratio sum {rm['s1_linear_sum']:.2f}, flat 15m/60m ratio {rm['s1_flat_ratio']:.2f}, net kVARh PF {rm['s2_net_kvarh']:.2f}, un-demeaned `dV` {rm['s2_raw_dv_no_demean']:.2f}, GIS phase tags {rm['s3_gis_phase']:.2f}, 60-min SCADA {rm['s1_scada60']:.2f}, rigorous standard shortcut {rm['rigorous']:.2f}, direct route {rm['direct']:.2f}).",
        f"7. Applied `vesterdal_planning_standard_ns2026.pdf` Sections 3 and 4 (`S_15m = sqrt(P_15^2 + Q_15^2)`, `Lim_MVA = 3 * w_max * S_15m`, `Loading % = 100 * Lim_MVA / Firm_N1_MVA`, `Relief_MVA = max(0, Lim_MVA - 0.85 * Firm_N1_MVA)`, Phase 1 >= {fig['planning_lines']['phase1_pct']:.1f}%, Phase 2 >= {fig['planning_lines']['phase2_pct']:.1f}%, Defer < {fig['planning_lines']['phase2_pct']:.1f}%): combined limiting-phase peak is {fig['pool_lim_mva_sum']:.2f} MVA and pool total relief capacity needed is {fig['total_relief_mva']:.2f} MVA, placing Hestmark ({subs['Hestmark']['loading_pct']:.2f}%), Raudfjord ({subs['Raudfjord']['loading_pct']:.2f}%), and Kvernholm ({subs['Kvernholm']['loading_pct']:.2f}%) in Phase 1, Malmnes ({subs['Malmnes']['loading_pct']:.2f}%), Drangvik ({subs['Drangvik']['loading_pct']:.2f}%), and Svarthaug ({subs['Svarthaug']['loading_pct']:.2f}%) in Phase 2, and Tverrli ({subs['Tverrli']['loading_pct']:.2f}%) in Defer.",
        f"8. Rebuilt the pipeline across all {ps['n_variants']} honest modeling variants (all-year and peak-month windows, additive excess scaling, median correlation and `k_ord`, monthly-only `k_ord`, constant `Q_15` and constant PF, winter and full-year voltage-drop anchors, measured `V_lv` scaling, single-hour and top-50 regression peak Q, 6-month heating-season / level / soft-posterior / single-hour phase-ID, and multi-stump combinations) plus six +/-20% perturbations on fitted inputs: every single variant and every perturbation files the identical seven-substation schedule, setting the bands stated above.",
        "",
        f"No other schedule survives the files. Leaving any single decisive step out alone breaks the schedule: dropping S1 alone puts total relief at {rt['S1']['total_relief_mva']:.2f} MVA and defers Drangvik ({rt['S1']['loading_pct']['Drangvik']:.2f}%); dropping S2 alone puts total relief at {rt['S2']['total_relief_mva']:.2f} MVA and demotes Kvernholm to Phase 2 ({rt['S2']['loading_pct']['Kvernholm']:.2f}%); dropping S3 alone puts total relief at {rt['S3']['total_relief_mva']:.2f} MVA, demotes Raudfjord to Phase 2 ({rt['S3']['loading_pct']['Raudfjord']:.2f}%), and promotes Svarthaug to Phase 1 ({rt['S3']['loading_pct']['Svarthaug']:.2f}%). "
        f"Dropping steps in pairs lands on distinct wrong schedules as well (S1+S2 gives {rt['S1+S2']['total_relief_mva']:.2f} MVA and misplaces Drangvik at {rt['S1+S2']['loading_pct']['Drangvik']:.2f}% and Kvernholm at {rt['S1+S2']['loading_pct']['Kvernholm']:.2f}%; S1+S3 gives {rt['S1+S3']['total_relief_mva']:.2f} MVA and misplaces all five open substations; S2+S3 gives {rt['S2+S3']['total_relief_mva']:.2f} MVA and misplaces Kvernholm, Raudfjord, and Svarthaug), dropping all three gives {rf['total_relief_mva']:.2f} MVA with five substations misplaced, and the rigorous standard shortcut (hourly coincidence times feeder 15-minute registers, class nominal power factors, and GIS phase tags) gives {rg['total_relief_mva']:.2f} MVA and misplaces all five open substations (Drangvik {rg['loading_pct']['Drangvik']:.2f}%, Malmnes {rg['loading_pct']['Malmnes']:.2f}%, Svarthaug {rg['loading_pct']['Svarthaug']:.2f}%, Kvernholm {rg['loading_pct']['Kvernholm']:.2f}%, Raudfjord {rg['loading_pct']['Raudfjord']:.2f}%). "
        f"Every shortcut (including zone-matched register coincidence, pooled register coincidence, and linear feeder ratio summation) fails the blind four-site reference check on Fossheim, Lindberg, Ostervik, and Solberg by {min(rr.values()):.1f}x to {max(rr.values()):.1f}x while every honest modeling variant and forcing perturbation preserves the exact seven-substation schedule.",
        "",
    ]
    text = "\n".join(lines)
    assert "\u2014" not in text and "\u2013" not in text, "em/en dash found in submission.md"
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
