"""Emit task26/submission.md strictly from generator/figures.json following submission-writeup/SKILL.md (v2):
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
    fc = rt["frontier_combo"]

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
    n_var = ps["n_variants"]

    lines = [
        "# task26 answer blocks",
        "",
        "## Tags",
        "",
        "**Domain:** Engineering and Physical Sciences, Energy Systems & Utilities (distribution losses and energy balance: 66/22 kV substation 15-minute limiting-phase peak loading conformed from hourly SCADA, monthly feeder demand registers, coupled 66 kV corridor impedance voltage drop, and three-phase bus voltage sag).",
        "**Analytical objective:** Data Extraction & Conformation (ETL / Pipeline Build).",
        "",
        "## Final Recommendation",
        "",
        f"**Schedule Phase 1 (2027) firm-capacity relief at {p1_str}; Phase 2 (2028-2029) relief at {p2_str}; and defer {df_str}, for {fig['total_relief_mva']:.2f} MVA of total relief capacity (band {fig['total_relief_band'][0]:.1f} to {fig['total_relief_band'][1]:.1f} MVA).** "
        f"This rejects the hourly SCADA, monthly net kVARh power factor, and GIS phase-tag reading, which puts total relief at {rf['total_relief_mva']:.2f} MVA and misplaces five substations (promoting Svarthaug to Phase 1 at {rf['loading_pct']['Svarthaug']:.2f}% while demoting Drangvik, Kvernholm, Malmnes, and Raudfjord): hourly SCADA smooths synchronized 15-minute feeder surges, monthly net kVARh cancels shunt capacitors across coupled 66 kV corridors, and partial-coverage AMI and drifted GIS records miss non-AMI legacy lateral phase skew.",
        "",
        "## Supplementary Questions",
        "",
        "### vesterdal_relief_schedule_2027_2029.xlsx",
        "",
        "The workbook opens on `Relief_Schedule` stating the 2027-2029 relief schedule (one row per in-scope substation sorted by Firm N-1 loading percentage with the pool summary totals/average and a horizontal bar chart of each site's Firm N-1 loading percentage), followed by supporting component, reference-validation, routes-comparison, and variant-battery sheets.",
        "",
        f"1. Estimated 2026 peak 15-minute limiting-phase apparent load (MVA), Firm N-1 loading percentage, relief capacity needed (MVA), and assigned 2027-2029 relief phase for each in-scope substation ({n_var}-variant band in parentheses):",
        *ask1_lines,
        f"2. Pool summary across the seven in-scope substations ({n_var}-variant band in parentheses):",
        f"   a. Combined 2026 peak 15-minute active demand: {fig['c1_total_p15_mw']:.2f} MW ({fig['c1_band'][0]:.1f} to {fig['c1_band'][1]:.1f} MW).",
        f"   b. Combined 2026 peak-hour reactive demand: {fig['c2_total_qpeak_mvar']:.2f} MVAr ({fig['c2_band'][0]:.1f} to {fig['c2_band'][1]:.1f} MVAr).",
        f"   c. Unweighted average peak limiting-phase share: {fig['c3_mean_lim_phase_pct']:.2f}% ({fig['c3_band'][0]:.2f}% to {fig['c3_band'][1]:.2f}%).",
        f"   d. Total relief capacity needed: {fig['total_relief_mva']:.2f} MVA ({fig['total_relief_band'][0]:.1f} to {fig['total_relief_band'][1]:.1f} MVA).",
        "",
        "### vesterdal_substation_conformed_2026.csv",
        "",
        "Seven rows, one per in-scope substation sorted by Firm N-1 loading percentage, holding each site's Firm N-1 rating, 60-minute SCADA peak, estimated 2026 appropriation filing figures, and assigned relief phase.",
        "",
        f"3. Underlying 2026 peak 15-minute active demand (MW), peak-hour reactive demand (MVAr), and peak limiting-phase share (%) driving each in-scope substation's loading ({n_var}-variant band in parentheses):",
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
        f"1. Conformed the operational extracts to the 8,760-hour 2026 Europe/Oslo grid (`scada_substation_hourly_2026.csv`: {ps['raw_scada_rows']:,} raw rows, {ps['superseded_dropped']:,} superseded preliminary rows dropped by latest `extract_ts` to {ps['clean_scada_rows']:,} clean substation-hours across eleven substations, Raudfjord's legacy `DD.MM.YYYY HH:MM` CET stamps aligned, {ps['vlv_nulls']} benign summer comms nulls in `v_lv_kv` interpolated; joined `gsp_66kv_voltages_2026.csv` and `subtransmission_66kv_lines.csv` across {ps['n_corridors']} radial 66 kV corridors fed from {ps['n_gsp']} Grid Supply Points; mapped legacy DMS IDs in `feeder_scada_hourly_2026.csv` [kW to MW] and `feeder_demand_registers_monthly_2026.csv` via `feeder_id_crosswalk.csv` across {ps['n_feeders']} feeders; joined `revenue_meter_monthly_2026.xlsx`, `substation_transformer_register.xlsx`, `substation_phase_bus_voltages_2026.csv`, `gis_lateral_connectivity_2026.csv` [{ps['n_laterals_total']} laterals: {ps['n_ami_per_sub']} AMI_SMART and {ps['n_leg_per_sub']} LEGACY_NON_AMI per substation], and `ami_lateral_telemetry_2026.db`; excluded streetlighting, oil-DGA, and tariff files). Clean 60-minute SCADA peaks across the seven in-scope substations (Fossheim, Lindberg, Ostervik, and Solberg modernized and excluded per `vesterdal_planning_standard_ns2026.pdf` Section 2) sum to {fig['r1_p60_sum_mw']:.2f} MW.",
        f"2. The hurried reading stops at those conformed operational tables: taking 60-minute SCADA peaks ({fig['r1_p60_sum_mw']:.2f} MW), monthly net kVARh power factors ({rf['c2_total_qpeak_mvar']:.2f} MVAr combined), and GIS phase tags ({rf['c3_mean_lim_phase_pct']:.2f}% mean) puts total relief at {rf['total_relief_mva']:.2f} MVA and misplaces five substations (Hestmark {rf['loading_pct']['Hestmark']:.2f}%, Svarthaug {rf['loading_pct']['Svarthaug']:.2f}%, Raudfjord {rf['loading_pct']['Raudfjord']:.2f}%, Kvernholm {rf['loading_pct']['Kvernholm']:.2f}%, Drangvik {rf['loading_pct']['Drangvik']:.2f}%, Malmnes {rf['loading_pct']['Malmnes']:.2f}%, Tverrli {rf['loading_pct']['Tverrli']:.2f}%). Three coupled observation-process effects overturn it (steps 3 to 5).",
        f"3. Reconstructed 15-minute coincident active peaks without feeder-level 15-minute PQ logs or park-zone labels: stripped the four regional diurnal-and-weather common factors (top-4 leave-this-substation-out SVD modes of log-normalized hourly feeder SCADA across the other ten substations) to isolate each substation's stochastic feeder innovations and pairwise correlation matrix `R` (recovering mean off-diagonal correlation {rp['rho_sync_lindberg']:.4f} on Lindberg's six synchronized feeders vs {rp['rho_stag_fossheim']:.4f} on Fossheim's six staggered feeders of identical customer-class mix), calibrated the MW-weighted order-statistic scaling `k_ord = {rp['k_ord']:.4f}` and winter intra-hour reactive slope `dQ/dP = {rp['dq_dp']:.4f}` against substation main-bay `pq_archive_15min_2026.csv` on the four modernized sites, and combined each substation's winter feeder register relative excesses in correlated quadrature `sqrt(d^T R d)` onto its 60-minute peak. Pool total is {fig['c1_total_p15_mw']:.2f} MW (Hestmark {subs['Hestmark']['p15_peak_mw']:.2f}, Drangvik {subs['Drangvik']['p15_peak_mw']:.2f}, Malmnes {subs['Malmnes']['p15_peak_mw']:.2f}, Kvernholm {subs['Kvernholm']['p15_peak_mw']:.2f}, Svarthaug {subs['Svarthaug']['p15_peak_mw']:.2f}, Raudfjord {subs['Raudfjord']['p15_peak_mw']:.2f}, Tverrli {subs['Tverrli']['p15_peak_mw']:.2f} MW); the 60-minute shortcut gives {rt['S1']['c1_total_p15_mw']:.2f} MW and defers Drangvik ({rt['S1']['loading_pct']['Drangvik']:.2f}%) and Malmnes ({rt['S1']['loading_pct']['Malmnes']:.2f}%), raw unstripped feeder correlation gives {rt['s1_raw_corr']['c1_total_p15_mw']:.2f} MW and promotes Malmnes to Phase 1 ({rt['s1_raw_corr']['loading_pct']['Malmnes']:.2f}%), independent quadrature gives {rt['s1_indep_quad']['c1_total_p15_mw']:.2f} MW and promotes Malmnes ({rt['s1_indep_quad']['loading_pct']['Malmnes']:.2f}%), class-share OLS gives {rt['s1_class_ols']['c1_total_p15_mw']:.2f} MW and demotes Drangvik ({rt['s1_class_ols']['loading_pct']['Drangvik']:.2f}%), pooled register coincidence (`CF = {rp['cf_pooled']:.4f}`) gives {rt['s1_cf_pooled']['c1_total_p15_mw']:.2f} MW, and linear feeder ratio summation overshoots to {rt['s1_linear_sum']['c1_total_p15_mw']:.2f} MW.",
        f"4. Inverted peak-hour reactive demand despite missing zone-substation HV voltage sensors and fixed/switched shunt capacitors: coupled all substations sharing each radial 66 kV sub-transmission corridor from `GSP-Nord` and `GSP-Sor` (`gsp_66kv_voltages_2026.csv`, `subtransmission_66kv_lines.csv`) through their shared upstream 66 kV line impedances and local transformer impedances (`substation_transformer_register.xlsx`) into simultaneous hourly linear systems `M(t) Q(t) = y(t) + delta_PT`, anchored each corridor's static PT offsets `delta_PT` jointly against peak-month settled `net_kvarh` (`revenue_meter_monthly_2026.xlsx`), fitted top-50 high-load hours to evaluate `Q_h` at peak active load, and projected 15-minute reactive demand via `Q_15 = Q_h + dQ/dP * (P_15 - P_60)`. Pool combined `Q_h` is {fig['c2_total_qpeak_mvar']:.2f} MVAr (Kvernholm {subs['Kvernholm']['q_peak_h_mvar']:.2f}, Drangvik {subs['Drangvik']['q_peak_h_mvar']:.2f}, Hestmark {subs['Hestmark']['q_peak_h_mvar']:.2f}, Tverrli {subs['Tverrli']['q_peak_h_mvar']:.2f}, Svarthaug {subs['Svarthaug']['q_peak_h_mvar']:.2f}, Raudfjord {subs['Raudfjord']['q_peak_h_mvar']:.2f}, Malmnes {subs['Malmnes']['q_peak_h_mvar']:.2f} MVAr); monthly net kVARh implies {rt['S2']['c2_total_qpeak_mvar']:.2f} MVAr and demotes Kvernholm ({rt['S2']['loading_pct']['Kvernholm']:.2f}%) and Drangvik ({rt['S2']['loading_pct']['Drangvik']:.2f}%), local single-site dV assuming `V_hv = V_gsp` explodes to {rt['s2_local_dv']['c2_total_qpeak_mvar']:.2f} MVAr ({rt['s2_local_dv']['total_relief_mva']:.2f} MVA relief), subtracting 66 kV `R*P` without `X*Q` coupling explodes to {rt['s2_rp_only']['c2_total_qpeak_mvar']:.2f} MVAr ({rt['s2_rp_only']['total_relief_mva']:.2f} MVA relief), un-demeaned corridor dV demotes Kvernholm ({rt['s2_raw_dv_no_demean']['loading_pct']['Kvernholm']:.2f}%), and nominal class power factors promote Malmnes ({rt['s2_class_pf']['loading_pct']['Malmnes']:.2f}%).",
        f"5. Recovered total heaviest-phase load share `w_max` across both AMI and non-AMI laterals: although common-mode-rejected AMI voltage regression matches {rp['tracer_matched']} of {rp['tracer_total']} field-traced AMI laterals (100.0% vs GIS {rp['gis_tracer_matched']} of {rp['tracer_total']}, {rp['gis_tracer_pct']:.1f}%), AMI covers only {ps['n_ami_per_sub']} of {ps['n_laterals_per_sub']} single-phase laterals per substation while the {ps['n_leg_per_sub']} `LEGACY_NON_AMI` laterals carry unmeasured opposite or concentrated phase skews (`pq_archive_15min_2026.csv` refutes AMI-only by {rr['s3_ami_only_bal']:.1f}x, AMI+GIS by {rr['s3_ami_plus_gis']:.1f}x, and 36/20 gross-up by {rr['s3_ami_grossup']:.1f}x). Calibrated effective unbalanced reactive slope `tan_phi_u = {rp['tan_phi_u']:.4f}` on the four modernized sites' three-phase main-bay PQ archive (`sub_pa_mw`, `sub_pb_mw`, `sub_pc_mw`) and inverted each substation's total per-phase load share from the PT-offset-free linear slope of `(V_ph - V_bar)` on total active load `P_tot` (canceling balanced three-phase capacitors and static per-phase PT offsets). Pool mean `w_max` is {fig['c3_mean_lim_phase_pct']:.2f}% (Raudfjord {subs['Raudfjord']['w_max_pct']:.2f}%, Tverrli {subs['Tverrli']['w_max_pct']:.2f}%, Hestmark {subs['Hestmark']['w_max_pct']:.2f}%, Kvernholm {subs['Kvernholm']['w_max_pct']:.2f}%, Drangvik {subs['Drangvik']['w_max_pct']:.2f}%, Malmnes {subs['Malmnes']['w_max_pct']:.2f}%, Svarthaug {subs['Svarthaug']['w_max_pct']:.2f}%); GIS tags ({rt['S3']['c3_mean_lim_phase_pct']:.2f}%), AMI-only ({rt['s3_ami_only_bal']['c3_mean_lim_phase_pct']:.2f}%), AMI+GIS ({rt['s3_ami_plus_gis']['c3_mean_lim_phase_pct']:.2f}%), and AMI gross-up ({rt['s3_ami_grossup']['c3_mean_lim_phase_pct']:.2f}%) all demote Raudfjord to Phase 2 and promote Svarthaug to Phase 1, while raw un-regressed bus voltage deviation gives {rt['s3_raw_vbus_no_pt']['c3_mean_lim_phase_pct']:.2f}% ({rt['s3_raw_vbus_no_pt']['total_relief_mva']:.2f} MVA relief).",
        f"6. Validated the full pipeline blind on all four modernized non-target reference substations (Fossheim, Lindberg, Ostervik, and Solberg) against `pq_archive_15min_2026.csv`: mean absolute Firm N-1 loading error across Fossheim ({fh_r['loading_pct']:.2f}% estimated vs {fh_r['truth_loading_pct']:.2f}% measured), Lindberg ({lb_r['loading_pct']:.2f}% vs {lb_r['truth_loading_pct']:.2f}%), Ostervik ({os_r['loading_pct']:.2f}% vs {os_r['truth_loading_pct']:.2f}%), and Solberg ({sb_r['loading_pct']:.2f}% vs {sb_r['truth_loading_pct']:.2f}%) is {rm['golden']:.2f} percentage points, beating all twenty-one rival routes by {min(rr.values()):.1f}x to {max(rr.values()):.1f}x (raw feeder correlation {rm['s1_raw_corr']:.2f}, class nominal PF {rm['s2_class_pf']:.2f}, independent quadrature {rm['s1_indep_quad']:.2f}, pooled coincidence {rm['s1_cf_pooled']:.2f}, class-share OLS {rm['s1_class_ols']:.2f}, un-demeaned corridor dV {rm['s2_raw_dv_no_demean']:.2f}, flat 15m/60m ratio {rm['s1_flat_ratio']:.2f}, net kVARh PF {rm['s2_net_kvarh']:.2f}, linear feeder sum {rm['s1_linear_sum']:.2f}, rigorous standard shortcut {rm['rigorous']:.2f}, 60-min SCADA {rm['s1_scada60']:.2f}, AMI+GIS {rm['s3_ami_plus_gis']:.2f}, R*P-only corridor dV {rm['s2_rp_only']:.2f}, GIS phase tags {rm['s3_gis_phase']:.2f}, AMI-only balanced {rm['s3_ami_only_bal']:.2f}, raw bus voltage {rm['s3_raw_vbus_no_pt']:.2f}, local GSP dV {rm['s2_local_dv']:.2f}, AMI gross-up {rm['s3_ami_grossup']:.2f}, direct route {rm['direct']:.2f}, and combined class-OLS + local-dV + AMI-only shortcut {rm['frontier_combo']:.2f}).",
        f"7. Applied `vesterdal_planning_standard_ns2026.pdf` Sections 3 and 4 (`S_15m = sqrt(P_15^2 + Q_15^2)`, `Lim_MVA = 3 * w_max * S_15m`, `Loading % = 100 * Lim_MVA / Firm_N1_MVA`, `Relief_MVA = max(0, Lim_MVA - 0.85 * Firm_N1_MVA)`, Phase 1 >= {fig['planning_lines']['phase1_pct']:.1f}%, Phase 2 >= {fig['planning_lines']['phase2_pct']:.1f}%, Defer < {fig['planning_lines']['phase2_pct']:.1f}%): combined limiting-phase peak is {fig['pool_lim_mva_sum']:.2f} MVA and pool total relief capacity needed is {fig['total_relief_mva']:.2f} MVA, placing Hestmark ({subs['Hestmark']['loading_pct']:.2f}%), Raudfjord ({subs['Raudfjord']['loading_pct']:.2f}%), Kvernholm ({subs['Kvernholm']['loading_pct']:.2f}%), and Drangvik ({subs['Drangvik']['loading_pct']:.2f}%) in Phase 1, Malmnes ({subs['Malmnes']['loading_pct']:.2f}%) and Svarthaug ({subs['Svarthaug']['loading_pct']:.2f}%) in Phase 2, and Tverrli ({subs['Tverrli']['loading_pct']:.2f}%) in Defer.",
        f"8. Rebuilt the pipeline across all {n_var} honest modeling variants (all-year, DJF 3-month, and peak-month windows, scaled and raw additive feeder excess, winter-hour innovation correlation, 5-PC / 6-PC / class-mean log-ratio / class-mean linear-diff regional stripping, annual-only / unweighted / median / monthly-only / unit `k_ord`, constant `Q_15` and constant PF, winter and full-year corridor anchors, 1-step `M_bar` solve, measured `V_lv` scaling, top-5 mean peak Q, winter/heating/first-difference/PT-intercept bus-sag slopes, hybrid AMI-subtracted bus-sag slope, winter `tan_phi_u` calibration, and multi-stump cross-variants) plus six +/-20% perturbations on fitted inputs: every single variant and every perturbation files the identical seven-substation schedule, setting the bands stated above.",
        "",
        f"No other schedule survives the files. Leaving any single decisive step out alone breaks the schedule: dropping S1 alone puts total relief at {rt['S1']['total_relief_mva']:.2f} MVA and defers Drangvik ({rt['S1']['loading_pct']['Drangvik']:.2f}%) and Malmnes ({rt['S1']['loading_pct']['Malmnes']:.2f}%); dropping S2 alone puts total relief at {rt['S2']['total_relief_mva']:.2f} MVA and demotes Kvernholm ({rt['S2']['loading_pct']['Kvernholm']:.2f}%) and Drangvik ({rt['S2']['loading_pct']['Drangvik']:.2f}%) to Phase 2; dropping S3 alone puts total relief at {rt['S3']['total_relief_mva']:.2f} MVA, demotes Raudfjord to Phase 2 ({rt['S3']['loading_pct']['Raudfjord']:.2f}%), and promotes Svarthaug to Phase 1 ({rt['S3']['loading_pct']['Svarthaug']:.2f}%). "
        f"Dropping steps in pairs lands on distinct wrong schedules as well (S1+S2 gives {rt['S1+S2']['total_relief_mva']:.2f} MVA and misplaces Drangvik, Kvernholm, and Malmnes; S1+S3 gives {rt['S1+S3']['total_relief_mva']:.2f} MVA and misplaces Drangvik, Malmnes, Raudfjord, and Svarthaug; S2+S3 gives {rt['S2+S3']['total_relief_mva']:.2f} MVA and misplaces Drangvik, Kvernholm, Raudfjord, and Svarthaug), dropping all three gives {rf['total_relief_mva']:.2f} MVA with five substations misplaced, the rigorous standard shortcut gives {rg['total_relief_mva']:.2f} MVA and misplaces all five open substations (Drangvik {rg['loading_pct']['Drangvik']:.2f}%, Kvernholm {rg['loading_pct']['Kvernholm']:.2f}%, Malmnes {rg['loading_pct']['Malmnes']:.2f}%, Raudfjord {rg['loading_pct']['Raudfjord']:.2f}%, Svarthaug {rg['loading_pct']['Svarthaug']:.2f}%), and combining class-share OLS, local GSP voltage drop, and AMI-only phase balance blows total relief to {fc['total_relief_mva']:.2f} MVA and misplaces Drangvik ({fc['loading_pct']['Drangvik']:.2f}%), Svarthaug ({fc['loading_pct']['Svarthaug']:.2f}%), and Tverrli ({fc['loading_pct']['Tverrli']:.2f}%). "
        f"All twenty-one shortcut routes fail both the seven-substation schedule and the blind four-site reference validation on Fossheim, Lindberg, Ostervik, and Solberg by {min(rr.values()):.1f}x to {max(rr.values()):.1f}x while every honest modeling variant and +/-20% forcing perturbation preserves the exact seven-substation schedule.",
        "",
    ]
    text = "\n".join(lines)
    assert "\u2014" not in text and "\u2013" not in text, "em/en dash found in submission.md"
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
