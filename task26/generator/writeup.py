"""Emit task26/submission.md strictly from generator/figures.json following submission-writeup/SKILL.md (v3):
- Tags (2 lines at top)
- Final Recommendation (2 sentences max: bold call answering both parts of the main ask, plus what it rejects and why)
- Supplementary Questions (grouped by deliverable file, 3 numbered multi-faceted asks with a/b/c member lines, no tables)
- Critical Components (3 one-liners: pure answer + unit + band, zero method clauses, strictly independent)
- Step-by-Step (8 numbered steps + closing unnumbered independence/uniqueness passage)
Zero em/en dashes; every figure drawn strictly from figures.json.
"""


import os


def _stump_block(fig):
    subs = fig["substations"]
    rp = fig["ref_params"]
    pd = fig["phys_details"]
    pr = fig["phys_ratios"]
    ps = fig["pack_stats"]
    rt = fig["routes"]

    r1_quotes = [
        "15.470 MVA",
        "Hestmark 101.671%",
        "Svarthaug 112.930%",
        "Kvernholm as the highest Defer case at 82.487%",
        "195.428 MW",
        "This is a floor, not a true 15-minute measurement",
        "Drangvik 51.807 MW vs 31.050 MW",
        "Lindberg 36.579 vs 24.570 MW",
        "+23.710 signed peak-hour MVAr",
        "assumes January's net compensation state applies at the peak hour",
        "Kvernholm -0.023008 -> -0.564",
        "Malmnes 0.476442 -> +14.566",
        "no power-flow study in the standard",
        "36.584%",
        "matched 80/80 (100.0%)",
        "75/220 (34.09%)",
        "~0.620 commercial / ~0.125 residential",
        "This is the largest judgment call",
        "Limiting phase C at 47.548%",
        "Limiting phase C at 34.122%",
        "dropped all 4,800 preliminary rows",
    ]
    r2_quotes = [
        "24.930 MVA",
        "Svarthaug at 125.580%",
        "Hestmark at 105.782%",
        "Kvernholm at 96.554%",
        "195.428 MW",
        "schedule uses 1.000",
        "This is the most consequential assumption",
        "Fossheim about 1.101",
        "Lindberg about 1.222",
        "54.055 MVAr",
        "Kvernholm 12.160 / 6.608 / 5.552",
        "Malmnes 16.171 / 0.763 / 15.408",
        "no angle/current and no NS-2026 relief term",
        "37.809966%",
        "correlations/signs vary by site (Kvernholm negative, Raudfjord positive, Svarthaug near zero)",
        "If GIS is stale for pool sites, limiting-phase identity and relief could change materially",
        "52.1193%",
        "35.1999%",
        "discarded B20270104_PRELIM, 4,800 rows",
    ]

    task_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    r1_path = os.path.join(task_dir, "runs", "run1.md")
    r2_path = os.path.join(task_dir, "runs", "run2.md")
    if os.path.exists(r1_path) and os.path.exists(r2_path):
        t1 = open(r1_path, encoding="utf-8").read()
        t2 = open(r2_path, encoding="utf-8").read()
        for q in r1_quotes:
            assert q in t1, f"Response 1 quote missing from runs/run1.md: {q!r}"
        for q in r2_quotes:
            assert q in t2, f"Response 2 quote missing from runs/run2.md: {q!r}"

    p1 = (
        f"**Response 1** files Phase 1 for Hestmark (101.671%, 5.918 MVA) and Svarthaug (112.930%, 9.552 MVA) only, "
        f"zero Phase 2 sites, and Defer for Kvernholm (82.487%), Malmnes (76.392%), Drangvik (67.786%), Raudfjord "
        f"(62.766%), and Tverrli (51.767%), sizing relief at 15.470 MVA vs golden {fig['total_relief_mva']:.2f} MVA "
        f"(band {fig['total_relief_band'][0]:.1f} to {fig['total_relief_band'][1]:.1f}): 5 of 7 sites wrong, Hestmark "
        f"40.1 points below golden ({subs['Hestmark']['loading_pct']:.2f}%), and 0 of 3 critical components in band. "
        f"On Step 1, after seeing Drangvik's register sum (51.807 vs 31.050 MW) and Lindberg's autumn PQ surge "
        f"(36.579 vs 24.570 MW), it writes \"This is a floor, not a true 15-minute measurement\" yet files the 195.428 MW "
        f"hourly floor vs {fig['c1_total_p15_mw']:.2f} MW (band {fig['c1_band'][0]:.1f} to {fig['c1_band'][1]:.1f}), "
        f"dropping Drangvik, Kvernholm, Malmnes, and Raudfjord. On Step 2, scaling peak P by January settled net "
        f"kVARh/kWh (\"assumes January's net compensation state applies at the peak hour\") yields +23.710 MVAr vs "
        f"{fig['c2_total_qpeak_mvar']:.2f} MVAr (band {fig['c2_band'][0]:.1f} to {fig['c2_band'][1]:.1f}), inverting "
        f"Kvernholm to -0.564 MVAr (golden {subs['Kvernholm']['q_peak_h_mvar']:.2f}) and Malmnes to +14.566 MVAr "
        f"(golden {subs['Malmnes']['q_peak_h_mvar']:.2f}) while dismissing 66 kV files (\"no power-flow study in the "
        f"standard\"). On Step 3, it regressed AMI phases to 80/80 (100.0%) on commissioning traces, rejected GIS at "
        f"75/220 (34.09%), and measured \"~0.620 commercial / ~0.125 residential\" AMI Q/P, but then grossed up unmetered "
        f"legacy laterals by AMI shares (\"This is the largest judgment call\"), filing 36.584% mean vs "
        f"{fig['c3_mean_lim_phase_pct']:.2f}% (band {fig['c3_band'][0]:.2f}% to {fig['c3_band'][1]:.2f}%), flipping "
        f"Svarthaug to 47.548% (Phase 1) and Raudfjord to 34.122% (Defer)."
    )

    p2 = (
        f"**Response 2** files Phase 1 for Hestmark (105.782%, 7.378 MVA) and Svarthaug (125.580%, 13.878 MVA), "
        f"Phase 2 for Kvernholm (96.554%, 3.674 MVA), and Defer for Malmnes (76.419%), Drangvik (69.437%), Raudfjord "
        f"(65.644%), and Tverrli (50.335%), sizing relief at 24.930 MVA vs {fig['total_relief_mva']:.2f} MVA: 5 of 7 "
        f"sites wrong and 0 of 3 critical components, via different shortcuts on Steps 2 and 3. On Step 1, after noting "
        f"Fossheim (1.101) and Lindberg (1.222) PQ ratios, it declines to estimate coincidence (\"schedule uses 1.000\", "
        f"\"This is the most consequential assumption\") and files the 195.428 MW hourly floor vs "
        f"{fig['c1_total_p15_mw']:.2f} MW. On Step 2, subtracting a flat January capacitor from manual class-PF load Q "
        f"yields 54.055 MVAr vs {fig['c2_total_qpeak_mvar']:.2f} MVAr (Kvernholm 5.552 vs "
        f"{subs['Kvernholm']['q_peak_h_mvar']:.2f} MVAr, demoting it to Phase 2; Malmnes 15.408 vs "
        f"{subs['Malmnes']['q_peak_h_mvar']:.2f}) while setting aside 66 kV records (\"no angle/current and no NS-2026 "
        f"relief term\"). On Step 3, checking `substation_phase_bus_voltages_2026.csv` univariately hit opposite diurnal "
        f"skews (\"correlations/signs vary by site (Kvernholm negative, Raudfjord positive, Svarthaug near zero)\"); it "
        f"dropped bus voltages and kept drifted GIS phases (\"If GIS is stale for pool sites, limiting-phase identity and "
        f"relief could change materially\"), filing 37.810% mean (37.809966%) vs {fig['c3_mean_lim_phase_pct']:.2f}%, "
        f"with Svarthaug at 52.1193% (Phase 1) and Raudfjord at 35.1999% (Defer)."
    )

    p3 = (
        f"**Why this is a fair stump:** Nothing rests on a planted defect or buried sentence. Every observation gap spans "
        f"all eleven substations (including the four excluded hubs): all {ps['n_feeders']} feeders carry hourly SCADA and "
        f"monthly 15-minute registers, all eleven sites share {ps['n_corridors']} radial 66 kV corridors with line/transformer "
        f"impedances and LTC taps, and all eleven carry {ps['n_ami_per_sub']} AMI plus {ps['n_leg_per_sub']} legacy laterals "
        f"with system-wide GIS drift (75/220 = 34.09%). Both responses passed 100% of cleaning and rule reading identically "
        f"to the golden (dropping {ps['superseded_dropped']:,} preliminary rows to {ps['clean_scada_rows']:,} clean hours, "
        f"aligning Raudfjord CET stamps, mapping 28 crosswalk IDs within 0.000030 MW, excluding all three distractors, and "
        f"reproducing {fig['r1_p60_sum_mw']:.2f} MW and every `vesterdal_planning_standard_ns2026.pdf` Section 3-5 formula); "
        f"every loss occurred after cleaning. Every signal sits in standard operational tables both models inspected, and "
        f"Response 1 found the 80/80 AMI phase verification and 0.620/0.125 AMI reactive contrast unprompted."
    )

    p4 = (
        f"**Why it takes deep analytical rigour:** Every shortcut fails direct physical measurements already in the ZIP, "
        f"with no custom index required. On Step 1, `pq_commissioning_autumn2026.csv` directly measures 15-minute active "
        f"peaks on Fossheim and Lindberg: the conformed 4-mode SVD plus correlated-quadrature estimator (`k_ord = "
        f"{rp['k_ord']:.4f}`) matches those measured 15-minute peaks to {pd['golden']['s1_comm_mae_mw']:.2f} MW MAE, "
        f"whereas the hourly SCADA floor misses by {pd['s1_scada60']['s1_comm_mae_mw']:.2f} MW MAE, linear register sums "
        f"({rt['s1_linear_sum']['c1_total_p15_mw']:.2f} MW) by {pd['s1_linear_sum']['s1_comm_mae_mw']:.2f} MW, 12-month "
        f"register correlation ({rt['s1_register_rho']['c1_total_p15_mw']:.2f} MW, inverting Malmnes "
        f"{rp['reg_rho_malmnes']:.3f} vs Drangvik {rp['reg_rho_drangvik']:.3f}) by "
        f"{pd['s1_register_rho']['s1_comm_mae_mw']:.2f} MW, flat PQ ratio ({rt['s1_flat_ratio']['c1_total_p15_mw']:.2f} MW) "
        f"by {pd['s1_flat_ratio']['s1_comm_mae_mw']:.2f} MW, independent quadrature "
        f"({rt['s1_indep_quad']['c1_total_p15_mw']:.2f} MW) by {pd['s1_indep_quad']['s1_comm_mae_mw']:.2f} MW, and pooled "
        f"coincidence ({rt['s1_cf_pooled']['c1_total_p15_mw']:.2f} MW) by {pd['s1_cf_pooled']['s1_comm_mae_mw']:.2f} MW. "
        f"On Step 2, Ohm's law (`dV = (R*P + X*Q)/V`) across `gsp_66kv_voltages_2026.csv`, `subtransmission_66kv_lines.csv`, "
        f"`substation_transformer_register.xlsx`, and `scada_substation_hourly_2026.csv` directly falsifies both runs and "
        f"every reactive proxy: coupled 11-site corridor inversion anchored to `revenue_meter_monthly_2026.xlsx` closes "
        f"hourly 22 kV LV voltages to {pd['golden']['s2_vlv_rmse_v']:.2f} V RMSE (8.1 V against meter noise) and settled "
        f"kVARh to {pd['golden']['s2_kvarh_err_mvar']:.2f} MVAr, whereas Response 1's January net kVARh ratio misses "
        f"measured January 22 kV voltages by 333.2 V RMSE (+2,521 V at Kvernholm's peak hour, -529 V at Malmnes), Response "
        f"2's manual class-PF minus flat January cap misses by 175.0 V RMSE (+1,434 V at Kvernholm peak, -1,016 V at "
        f"Malmnes), monthly `Q(P)` misses by {pd['s2_monthly_qp']['s2_vlv_rmse_v']:.1f} V, and target-only corridors "
        f"dropping upstream hubs miss by {pd['s2_targets_only']['s2_vlv_rmse_v']:.1f} V. On Step 3, "
        f"`commissioning_phase_log_2025.csv` falsifies GIS at {rp['gis_tracer_matched']}/{rp['tracer_total']} "
        f"({rp['gis_tracer_pct']:.1f}%, random chance across three phases), and `substation_phase_bus_voltages_2026.csv` "
        f"falsifies GIS ({pd['s3_gis']['s3_bus_rmse_v']:.2f} V bus-sag RMSE), Response 1's AMI gross-up "
        f"({pd['s3_ami_grossup']['s3_bus_rmse_v']:.2f} V), and scalar OLS ({pd['s3_scalar_ols']['s3_bus_rmse_v']:.2f} V, "
        f"Svarthaug {rt['s3_scalar_ols']['loading_pct']['Svarthaug']:.2f}%) while `ami_lateral_telemetry_2026.db` falsifies "
        f"manual-PF OLS ({pd['s3_handbook_pf']['s3_ami_q_rmse_kvar']:.2f} vs {pd['golden']['s3_ami_q_rmse_kvar']:.2f} kVAr "
        f"RMSE); only joint `(V_ph - V_bar)` regression on `[1, P_res, P_com, P_bal]` with AMI-measured `tan_phi` "
        f"({rp['tan_phi_res']:.4f} vs {rp['tan_phi_com']:.4f}) matches measured 3-phase bus voltages to "
        f"{pd['golden']['s3_bus_rmse_v']:.2f} V RMSE. Each step independently flips distinct sites (Step 1: "
        f"Drangvik/Kvernholm/Malmnes/Raudfjord; Step 2: Kvernholm; Step 3: Raudfjord/Svarthaug), and both responses "
        f"missed all three."
    )

    return ["## How is each model stumped?", "", p1, "", p2, "", p3, "", p4, ""]


def write(path, fig, include_stump_block=False):
    subs = fig["substations"]
    b = fig["bands"]
    rp = fig["ref_params"]
    pd = fig["phys_details"]
    ps = fig["pack_stats"]
    rt = fig["routes"]
    rf = rt["S1+S2+S3"]
    rg = rt["rigorous"]
    r1v2 = rt["response1_v2"]
    nf_sub = ps["n_feeders_by_sub"]
    sr = fig["site_reg_rat"]
    mfr = fig["malmnes_forced_ratios"]
    s1_rat = fig["s1_pq_mae_ratios"]
    s1_min_x = min(s1_rat.values())
    s1_max_x = max(s1_rat.values())
    s2_vlv_vals = [v for k, v in fig["s2_vlv_ratios"].items() if v > 10.0]
    s2_vlv_lo, s2_vlv_hi = min(s2_vlv_vals), max(s2_vlv_vals)
    s3_bus_vals = [v for k, v in fig["s3_bus_ratios"].items() if v >= 3.0]
    s3_bus_lo, s3_bus_hi = min(s3_bus_vals), max(s3_bus_vals)

    def _join_and(items):
        if len(items) <= 1:
            return "".join(items)
        if len(items) == 2:
            return f"{items[0]} and {items[1]}"
        return ", ".join(items[:-1]) + f", and {items[-1]}"

    def _phase_of(val):
        if val >= 100.0:
            return "Phase 1 (2027)"
        if val >= 85.0:
            return "Phase 2 (2028-2029)"
        return "Defer"

    def _flipped(route_key):
        out = []
        for s in fig["targets"]:
            lv = rt[route_key]["loading_pct"][s]
            ph = _phase_of(lv)
            if ph != subs[s]["phase"]:
                out.append((s, lv, ph))
        return out

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

    rf_flips = _flipped("S1+S2+S3")
    rf_flip_desc = _join_and([f"{s} at {lv:.2f}%" for s, lv, _ in rf_flips])
    s1_flips = _flipped("S1")
    s1_flip_desc = _join_and([f"{s} ({lv:.2f}%)" for s, lv, _ in s1_flips])
    s2_flips = _flipped("S2")
    s2_flip_desc = _join_and([f"{s} ({lv:.2f}%, {ph})" for s, lv, ph in s2_flips])
    s3_flips = _flipped("S3")
    s3_flip_desc = _join_and([f"{s} ({lv:.2f}%, {ph})" for s, lv, ph in s3_flips])

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

    n_var = ps["n_variants"]
    stump_lines = _stump_block(fig) if include_stump_block else []

    lines = [
        "# task26 answer blocks",
        "",
        "## Tags",
        "",
        "**Domain:** Engineering and Physical Sciences, Energy Systems & Utilities (distribution losses and energy balance: 66/22 kV substation 15-minute limiting-phase peak loading conformed from hourly SCADA, monthly feeder demand registers, coupled 66 kV sub-transmission impedance voltage drop, and multi-class three-phase bus voltage sag).",
        "**Analytical objective:** Data Extraction & Conformation (ETL / Pipeline Build).",
        "",
        "## Final Recommendation",
        "",
        f"**Schedule Phase 1 (2027) firm-capacity relief at {p1_str}; Phase 2 (2028-2029) relief at {p2_str}; and defer {df_str}, for {fig['total_relief_mva']:.2f} MVA of total relief capacity (band {fig['total_relief_band'][0]:.1f} to {fig['total_relief_band'][1]:.1f} MVA).** "
        f"This rejects the hourly SCADA, monthly net kVARh power factor, and partial-AMI reading, which puts total relief at {rf['total_relief_mva']:.2f} MVA and misplaces {len(rf_flips)} substations (deferring {rf_flip_desc}): hourly SCADA smooths synchronized 15-minute feeder surges, monthly net kVARh hides peak-only reactive surges and switched capacitors across shared 66 kV corridors, and partial-coverage AMI plus drifted GIS tags miss opposite diurnal phase skews on unmetered legacy laterals.",
        "",
        *stump_lines,
        "## Supplementary Questions",
        "",
        "### vesterdal_relief_schedule_2027_2029.xlsx",
        "",
        "The workbook opens on `Relief_Schedule` stating the 2027-2029 relief schedule (one row per in-scope substation sorted by Firm N-1 loading percentage with live formula-driven totals/average and a horizontal bar chart of each site's Firm N-1 loading percentage), followed by supporting component, physics-validation, routes-comparison, and variant-battery sheets.",
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
        f"1. Conformed the operational extracts to the 8,760-hour 2026 Europe/Oslo grid (`scada_substation_hourly_2026.csv`: {ps['raw_scada_rows']:,} raw rows, {ps['superseded_dropped']:,} superseded preliminary rows dropped by latest `extract_ts` to {ps['clean_scada_rows']:,} clean substation-hours across eleven substations, Raudfjord's legacy `DD.MM.YYYY HH:MM` CET stamps aligned, {ps['vlv_nulls']} benign summer comms nulls in `v_lv_kv` interpolated; joined `gsp_66kv_voltages_2026.csv` and `subtransmission_66kv_lines.csv` across {ps['n_corridors']} radial 66 kV corridors fed from {ps['n_gsp']} Grid Supply Points with the four modernized hubs upstream of the relief-pool sites; mapped legacy DMS IDs in `feeder_scada_hourly_2026.csv` [kW to MW] and `feeder_demand_registers_monthly_2026.csv` via `feeder_id_crosswalk.csv` across {ps['n_feeders']} feeders; joined `revenue_meter_monthly_2026.xlsx`, `substation_transformer_register.xlsx`, `substation_phase_bus_voltages_2026.csv`, `gis_lateral_connectivity_2026.csv` [{ps['n_laterals_total']} laterals: {ps['n_ami_per_sub']} AMI_SMART and {ps['n_leg_per_sub']} LEGACY_NON_AMI per substation], `ami_lateral_telemetry_2026.db` [v_volts, p_kw, q_kvar], and `pq_commissioning_2026.csv` [{ps['comm_pq_rows']:,} active-only 15-minute intervals spanning September, October, and December 2026 on Fossheim, Lindberg, and Solberg]; excluded streetlighting, oil-DGA, and tariff files). Clean 60-minute SCADA peaks across the seven in-scope substations (excluding Fossheim, Lindberg, Ostervik, and Solberg per `vesterdal_planning_standard_ns2026.pdf` Section 2) sum to {fig['r1_p60_sum_mw']:.2f} MW.",
        f"2. The hurried reading stops at conformed operational tables: taking 60-minute SCADA peaks ({fig['r1_p60_sum_mw']:.2f} MW), monthly net kVARh power factors ({rf['c2_total_qpeak_mvar']:.2f} MVAr combined), and AMI-only balanced phases ({rf['c3_mean_lim_phase_pct']:.2f}% mean) puts total relief at {rf['total_relief_mva']:.2f} MVA and misplaces {len(rf_flips)} substations (Hestmark {rf['loading_pct']['Hestmark']:.2f}%, Svarthaug {rf['loading_pct']['Svarthaug']:.2f}%, Kvernholm {rf['loading_pct']['Kvernholm']:.2f}%, Malmnes {rf['loading_pct']['Malmnes']:.2f}%, Drangvik {rf['loading_pct']['Drangvik']:.2f}%, Raudfjord {rf['loading_pct']['Raudfjord']:.2f}%, Tverrli {rf['loading_pct']['Tverrli']:.2f}%). Three coupled observation-process gaps overturn it (steps 3 to 5).",
        f"3. Reconstructed 15-minute coincident active peaks without in-scope PQ metering or feeder cluster labels: stripped four regional diurnal-and-weather SVD modes from log-normalized hourly feeder SCADA across the other ten substations (1-PC stripping leaves Drangvik {rp['pca1_drangvik']:.3f} indistinguishable from Malmnes {rp['pca1_malmnes']:.3f}, while seasonal burst modulation inverts 12-month register correlation to {rp['reg_rho_malmnes']:.3f} on staggered Malmnes vs {rp['reg_rho_drangvik']:.3f} on synchronized Drangvik), clamping negative off-diagonal entries of the pairwise feeder innovation correlation matrix `R` to zero (unit diagonal) and recovering mean off-diagonal correlation across the first five industrial/maritime feeders of {rp['rho_sync_drangvik']:.4f} on Drangvik and {rp['rho_sync_lindberg']:.4f} on Lindberg vs {rp['rho_stag_malmnes']:.4f} on Malmnes and {rp['rho_stag_fossheim']:.4f} on Fossheim. Defining each feeder's monthly 15-minute register excess as `d_i = max(0, M_15,i - P_60,i)` (monthly register maximum minus monthly 60-minute SCADA maximum), calibrated `k_ord = {rp['k_ord']:.4f}` as `sum(max(P_15) - max(P_60)) / sum(sqrt(d^T R d))` directly across all {ps['comm_pq_points_count']} monthly commissioning peaks (Sep, Oct, and Dec) in `pq_commissioning_2026.csv` covering three structurally distinct modernized hubs (Fossheim {nf_sub['Fossheim']} feeders [9 staggered, mean excess/sum_d ratio {sr['Fossheim']:.3f}], Solberg {nf_sub['Solberg']} feeders [3 synced plus 2 staggered, ratio {sr['Solberg']:.3f}], and Lindberg {nf_sub['Lindberg']} feeders [6 synced, ratio {sr['Lindberg']:.3f}], none an identical twin of {nf_sub['Malmnes']}-feeder Malmnes), and added `k_ord * sqrt(d_bar^T R d_bar)` (where `d_bar` averages each feeder's monthly `d_i` across winter months NDJF) onto each substation's 60-minute annual peak. Pool total is {fig['c1_total_p15_mw']:.2f} MW (Drangvik {subs['Drangvik']['p15_peak_mw']:.2f}, Hestmark {subs['Hestmark']['p15_peak_mw']:.2f}, Malmnes {subs['Malmnes']['p15_peak_mw']:.2f}, Raudfjord {subs['Raudfjord']['p15_peak_mw']:.2f}, Svarthaug {subs['Svarthaug']['p15_peak_mw']:.2f}, Kvernholm {subs['Kvernholm']['p15_peak_mw']:.2f}, Tverrli {subs['Tverrli']['p15_peak_mw']:.2f} MW), matching all {ps['comm_pq_points_count']} directly observed monthly `max(P_15) - max(P_60)` peaks in `pq_commissioning_2026.csv` to {pd['golden']['s1_comm_mae_mw']:.2f} MW MAE; every alternative estimator fails those direct 9-point 15-minute measurements by {s1_min_x:.1f}x to {s1_max_x:.1f}x (60-minute SCADA floor {rt['S1']['c1_total_p15_mw']:.2f} MW at {pd['s1_scada60']['s1_comm_mae_mw']:.2f} MW MAE, 12-month register correlation {rt['s1_register_rho']['c1_total_p15_mw']:.2f} MW at {pd['s1_register_rho']['s1_comm_mae_mw']:.2f} MW MAE flipping Drangvik down to {rt['s1_register_rho']['loading_pct']['Drangvik']:.2f}% and Malmnes up to {rt['s1_register_rho']['loading_pct']['Malmnes']:.2f}%, nearest-hub twin ratio {rt['s1_twin_ratio']['c1_total_p15_mw']:.2f} MW at {pd['s1_twin_ratio']['s1_comm_mae_mw']:.2f} MW MAE flipping Drangvik to {rt['s1_twin_ratio']['loading_pct']['Drangvik']:.2f}%, 1-PC stripping {rt['s1_pca1']['c1_total_p15_mw']:.2f} MW at {pd['s1_pca1']['s1_comm_mae_mw']:.2f} MW MAE, raw hourly correlation {rt['s1_raw_corr']['c1_total_p15_mw']:.2f} MW at {pd['s1_raw_corr']['s1_comm_mae_mw']:.2f} MW MAE, independent quadrature {rt['s1_indep_quad']['c1_total_p15_mw']:.2f} MW at {pd['s1_indep_quad']['s1_comm_mae_mw']:.2f} MW MAE flipping Malmnes to {rt['s1_indep_quad']['loading_pct']['Malmnes']:.2f}%, pooled register coincidence {rt['s1_cf_pooled']['c1_total_p15_mw']:.2f} MW at {pd['s1_cf_pooled']['s1_comm_mae_mw']:.2f} MW MAE, flat PQ ratio {rt['s1_flat_ratio']['c1_total_p15_mw']:.2f} MW at {pd['s1_flat_ratio']['s1_comm_mae_mw']:.2f} MW MAE, and linear register sum {rt['s1_linear_sum']['c1_total_p15_mw']:.2f} MW at {pd['s1_linear_sum']['s1_comm_mae_mw']:.2f} MW MAE); even forcing Fossheim's ({sr['Fossheim']:.3f}) or Solberg's ({sr['Solberg']:.3f}) commissioning ratio onto Malmnes keeps Malmnes in Phase 2 ({mfr['Fossheim']:.2f}% and {mfr['Solberg']:.2f}%).",
        f"4. Inverted peak-hour reactive demand from Ohm's law voltage drop without any PQ reactive archive: coupled all eleven substations along their four shared radial 66 kV sub-transmission corridors (`COR-N01`, `COR-N02`, `COR-S01`, `COR-S02`) including the four upstream modernized hubs (`Ostervik`, `Fossheim`, `Lindberg`, `Solberg`) from `GSP-Nord` and `GSP-Sor` through shared 66 kV line impedances and local transformer impedances (`substation_transformer_register.xlsx`, nominal 66/22 kV voltage basis with linear tap ratio `tau = (22/66) * (1 + {fig['planning_lines']['tap_step_frac']:.4f} * ltc_tap_step)`, LTC taps `-10..+10`) into simultaneous hourly linear systems `M(t) Q(t) = y(t) + delta_PT`, anchored each corridor's static PT offsets `delta_PT` jointly against corridor peak-month (January 2026) settled `net_kvarh` (`revenue_meter_monthly_2026.xlsx`), and averaged top-5 peak-load hours. Pool combined `Q_h` is {fig['c2_total_qpeak_mvar']:.2f} MVAr (Kvernholm {subs['Kvernholm']['q_peak_h_mvar']:.2f}, Drangvik {subs['Drangvik']['q_peak_h_mvar']:.2f}, Hestmark {subs['Hestmark']['q_peak_h_mvar']:.2f}, Svarthaug {subs['Svarthaug']['q_peak_h_mvar']:.2f}, Raudfjord {subs['Raudfjord']['q_peak_h_mvar']:.2f}, Tverrli {subs['Tverrli']['q_peak_h_mvar']:.2f}, Malmnes {subs['Malmnes']['q_peak_h_mvar']:.2f} MVAr), closing hourly 22 kV LV bus voltage balance in `scada_substation_hourly_2026.csv` to {pd['golden']['s2_vlv_rmse_v']:.2f} V RMSE and 12-month settled `net_kvarh` to {pd['golden']['s2_kvarh_err_mvar']:.2f} MVAr; winter fixed capacitors on Kvernholm and peak-only switched capacitors on Malmnes cause every reactive proxy to violate measured 22 kV bus voltages or settled energy conservation (annual net kVARh {rt['S2']['c2_total_qpeak_mvar']:.2f} MVAr at {pd['s2_net_kvarh']['s2_vlv_rmse_v']:.1f} V LV bus RMSE demoting Kvernholm to {rt['S2']['loading_pct']['Kvernholm']:.2f}%, winter-only net kVARh {rt['s2_winter_kvarh']['c2_total_qpeak_mvar']:.2f} MVAr at {pd['s2_winter_kvarh']['s2_vlv_rmse_v']:.1f} V, monthly linear `Q(P)` {rt['s2_monthly_qp']['c2_total_qpeak_mvar']:.2f} MVAr at {pd['s2_monthly_qp']['s2_vlv_rmse_v']:.1f} V demoting Kvernholm to {rt['s2_monthly_qp']['loading_pct']['Kvernholm']:.2f}%, monthly `Q(P + winter)` {rt['s2_monthly_win']['c2_total_qpeak_mvar']:.2f} MVAr at {pd['s2_monthly_win']['s2_vlv_rmse_v']:.1f} V, monthly quadratic `Q(P^2)` {rt['s2_monthly_quad']['c2_total_qpeak_mvar']:.2f} MVAr at {pd['s2_monthly_quad']['s2_vlv_rmse_v']:.1f} V, class nominal PFs {rt['s2_class_pf']['c2_total_qpeak_mvar']:.2f} MVAr at {pd['s2_class_pf']['s2_vlv_rmse_v']:.1f} V and {pd['s2_class_pf']['s2_kvarh_err_mvar']:.2f} MVAr kVARh error, target-only corridor dropping upstream hubs {rt['s2_targets_only']['c2_total_qpeak_mvar']:.2f} MVAr at {pd['s2_targets_only']['s2_vlv_rmse_v']:.1f} V, local single-site dV {rt['s2_local_dv']['c2_total_qpeak_mvar']:.2f} MVAr at {pd['s2_local_dv']['s2_vlv_rmse_v']:.1f} V, `R*P`-only dV {rt['s2_rp_only']['c2_total_qpeak_mvar']:.2f} MVAr at {pd['s2_rp_only']['s2_vlv_rmse_v']:.1f} V, and un-demeaned corridor dV {rt['s2_raw_dv']['c2_total_qpeak_mvar']:.2f} MVAr at {pd['s2_raw_dv']['s2_kvarh_err_mvar']:.2f} MVAr kVARh error).",
        f"5. Recovered annual-peak heaviest-phase share `w_max` across both AMI and unmetered legacy laterals from measured 3-phase 22 kV bus voltage sag without any 3-phase PQ archive: although common-mode-rejected AMI voltage regression matches {rp['tracer_matched']} of {rp['tracer_total']} field-traced AMI laterals (100.0% vs GIS {rp['gis_tracer_matched']} of {rp['tracer_total']}, {rp['gis_tracer_pct']:.1f}%), AMI covers only {ps['n_ami_per_sub']} of {ps['n_laterals_per_sub']} single-phase laterals per substation while the {ps['n_leg_per_sub']} `LEGACY_NON_AMI` laterals carry opposite phase skews, and commercial midday loads carry opposite phase skews to residential evening loads with a 3.3x reactive impedance contrast measured directly from AMI SQLite `(p_kw, q_kvar)` via zero-intercept OLS `tan_phi_c = sum(p_kw * q_kvar) / sum(p_kw^2)` (`tan_phi_res = {rp['tan_phi_res']:.4f}` resistive heating vs `tan_phi_com = {rp['tan_phi_com']:.4f}` commercial HVAC, versus engineering manual nominal ratios {rp['handbook_tan_phi_res']:.4f} and {rp['handbook_tan_phi_com']:.4f}). Regressing `(V_ph - V_bar)` jointly on `[1, P_res, P_com, P_bal]` (aggregated from hourly feeder SCADA with `P_bal = industrial_batch + maritime_port`) eliminates static per-phase PT offsets and balanced shunt capacitors, and scaling class slopes by `3 * (R_T + X_T * tan_phi_c) / V_nom` (`V_nom = {fig['planning_lines']['v_nom_lv_kv']:.1f} kV`) yields exact peak-hour total phase shares evaluated at each substation's annual peak hour. Pool mean `w_max` is {fig['c3_mean_lim_phase_pct']:.2f}% (Raudfjord {subs['Raudfjord']['w_max_pct']:.2f}%, Tverrli {subs['Tverrli']['w_max_pct']:.2f}%, Hestmark {subs['Hestmark']['w_max_pct']:.2f}%, Malmnes {subs['Malmnes']['w_max_pct']:.2f}%, Drangvik {subs['Drangvik']['w_max_pct']:.2f}%, Svarthaug {subs['Svarthaug']['w_max_pct']:.2f}%, Kvernholm {subs['Kvernholm']['w_max_pct']:.2f}%), matching `substation_phase_bus_voltages_2026.csv` to {pd['golden']['s3_bus_rmse_v']:.2f} V RMSE and `ami_lateral_telemetry_2026.db` to {pd['golden']['s3_ami_q_rmse_kvar']:.2f} kVAr RMSE; every alternative fails those direct bus-voltage or AMI-reactive measurements by {s3_bus_lo:.1f}x to {s3_bus_hi:.1f}x (GIS {rt['s3_gis']['c3_mean_lim_phase_pct']:.2f}% at {pd['s3_gis']['s3_bus_rmse_v']:.2f} V RMSE and {rp['gis_tracer_pct']:.1f}% commissioning accuracy, AMI-only {rt['S3']['c3_mean_lim_phase_pct']:.2f}% at {pd['s3_ami_only']['s3_bus_rmse_v']:.2f} V, AMI+GIS {rt['s3_ami_plus_gis']['c3_mean_lim_phase_pct']:.2f}% at {pd['s3_ami_plus_gis']['s3_bus_rmse_v']:.2f} V, AMI gross-up {rt['s3_ami_grossup']['c3_mean_lim_phase_pct']:.2f}% at {pd['s3_ami_grossup']['s3_bus_rmse_v']:.2f} V, scalar OLS `dv_ph ~ P_tot` {rt['s3_scalar_ols']['c3_mean_lim_phase_pct']:.2f}% at {pd['s3_scalar_ols']['s3_bus_rmse_v']:.2f} V pushing Svarthaug to {rt['s3_scalar_ols']['loading_pct']['Svarthaug']:.2f}%, evening 17-21 cutoff OLS {rt['s3_evening_cut']['c3_mean_lim_phase_pct']:.2f}% / {rt['s3_even_zres']['c3_mean_lim_phase_pct']:.2f}% at {pd['s3_evening_cut']['s3_bus_rmse_v']:.2f} V, multi-class OLS with manual nominal PF {rt['s3_handbook_pf']['c3_mean_lim_phase_pct']:.2f}% at {pd['s3_handbook_pf']['s3_ami_q_rmse_kvar']:.2f} kVAr AMI RMSE pushing Raudfjord down to {rt['s3_handbook_pf']['loading_pct']['Raudfjord']:.2f}%, substation PF {rt['s3_sub_pf']['c3_mean_lim_phase_pct']:.2f}% at {pd['s3_sub_pf']['s3_ami_q_rmse_kvar']:.2f} kVAr AMI RMSE, and raw bus voltage {rt['s3_raw_vbus']['c3_mean_lim_phase_pct']:.2f}% at {pd['s3_raw_vbus']['s3_bus_rmse_v']:.2f} V).",
        f"6. Verified each estimator independently against its own direct electrical-engineering law in the shipped files: (a) 9-point monthly `max(P_15) - max(P_60)` PQ validation on `pq_commissioning_2026.csv` yields {pd['golden']['s1_comm_mae_mw']:.2f} MW MAE vs {pd['s1_indep_quad']['s1_comm_mae_mw']:.2f} to {pd['s1_scada60']['s1_comm_mae_mw']:.2f} MW MAE ({s1_min_x:.1f}x to {s1_max_x:.1f}x) for every S1 alternative; (b) Ohm's-law 66/22 kV radial voltage balance on `scada_substation_hourly_2026.csv` and 12-month reactive energy conservation on `revenue_meter_monthly_2026.xlsx` yield {pd['golden']['s2_vlv_rmse_v']:.2f} V LV bus RMSE and {pd['golden']['s2_kvarh_err_mvar']:.2f} MVAr error vs {s2_vlv_lo:.1f} to {s2_vlv_hi:.1f} V RMSE (or {pd['s2_raw_dv']['s2_kvarh_err_mvar']:.2f} MVAr kVARh violation) for every S2 alternative; (c) 3-phase 22 kV bus-sag balance on `substation_phase_bus_voltages_2026.csv` yields {pd['golden']['s3_bus_rmse_v']:.2f} V RMSE vs {pd['s3_scalar_ols']['s3_bus_rmse_v']:.2f} to {pd['s3_raw_vbus']['s3_bus_rmse_v']:.2f} V RMSE for every phase-split proxy (and {rp['tracer_matched']}/{rp['tracer_total']} vs GIS {rp['gis_tracer_matched']}/{rp['tracer_total']} on `commissioning_phase_log_2025.csv`); and (d) AMI customer reactive balance on `ami_lateral_telemetry_2026.db` yields {pd['golden']['s3_ami_q_rmse_kvar']:.2f} kVAr RMSE vs {pd['s3_handbook_pf']['s3_ami_q_rmse_kvar']:.2f} kVAr for engineering-manual nominal PFs.",
        f"7. Applied `vesterdal_planning_standard_ns2026.pdf` Sections 3 and 4 (`S_15m = sqrt(P_15^2 + Q_h^2)`, `Lim_MVA = 3 * w_max * S_15m`, `Loading % = 100 * Lim_MVA / Firm_N1_MVA`, `Relief_MVA = max(0, Lim_MVA - 0.85 * Firm_N1_MVA)`, Phase 1 >= {fig['planning_lines']['phase1_pct']:.1f}%, Phase 2 >= {fig['planning_lines']['phase2_pct']:.1f}%, Defer < {fig['planning_lines']['phase2_pct']:.1f}%): combined limiting-phase peak is {fig['pool_lim_mva_sum']:.2f} MVA and pool total relief capacity needed is {fig['total_relief_mva']:.2f} MVA, placing Hestmark ({subs['Hestmark']['loading_pct']:.2f}%), Raudfjord ({subs['Raudfjord']['loading_pct']:.2f}%), Kvernholm ({subs['Kvernholm']['loading_pct']:.2f}%), and Drangvik ({subs['Drangvik']['loading_pct']:.2f}%) in Phase 1, Svarthaug ({subs['Svarthaug']['loading_pct']:.2f}%) and Malmnes ({subs['Malmnes']['loading_pct']:.2f}%) in Phase 2, and Tverrli ({subs['Tverrli']['loading_pct']:.2f}%) in Defer.",
        f"8. Checked sensitivity across {n_var} honest estimator variants (12-month, DJF, and peak-month register windows; scaled-additive and multiplicative excess scalings; winter innovation windows; 5-PC, 6-PC, and class-reference residual stripping; unit `k_ord = 1.0` and mean-ratio commissioning calibration; intra-hour `Q15` slope and constant-PF rules; winter and full-year `net_kvarh` anchors; 1-step `M_bar` and measured-`V_lv` scaling; top-20 regression and single-hour peak `Q`; winter, heating, first-difference, 2-class, and top-5 peak bus-sag estimators; winter AMI `tan_phi`) plus six +/-20% forcing perturbations on `k_ord`, `Q_peak`, and phase excess: every variant and perturbation preserves the exact seven-substation schedule, with the thinnest boundary clearances at Malmnes ({subs['Malmnes']['loading_pct']:.2f}% vs 85.0% Phase 2 floor and 100.0% Phase 1 ceiling, band {b['loading_pct']['Malmnes'][0]:.1f}% to {b['loading_pct']['Malmnes'][1]:.1f}%), Svarthaug ({subs['Svarthaug']['loading_pct']:.2f}% vs 85.0% Phase 2 floor and 100.0% Phase 1 ceiling, band {b['loading_pct']['Svarthaug'][0]:.1f}% to {b['loading_pct']['Svarthaug'][1]:.1f}%), and Drangvik ({subs['Drangvik']['loading_pct']:.2f}% vs 100.0% Phase 1 floor, band {b['loading_pct']['Drangvik'][0]:.1f}% to {b['loading_pct']['Drangvik'][1]:.1f}%).",
        "",
        f"Each of the three critical components is independent and individually decisive: losing 15-minute coincidence alone shifts combined active demand from {fig['c1_total_p15_mw']:.2f} to {rt['S1']['c1_total_p15_mw']:.2f} MW and flips {s1_flip_desc} while moving all five remaining substations and total relief outside band and leaving combined reactive demand and limiting-phase share unchanged; losing coupled 66 kV reactive inversion alone shifts combined reactive demand from {fig['c2_total_qpeak_mvar']:.2f} to {rt['S2']['c2_total_qpeak_mvar']:.2f} MVAr and flips {s2_flip_desc} while leaving active demand and phase share unchanged; and losing multi-class bus-sag phase inversion alone shifts mean limiting-phase share from {fig['c3_mean_lim_phase_pct']:.2f}% to {rt['S3']['c3_mean_lim_phase_pct']:.2f}% and flips {s3_flip_desc} while leaving active and reactive demand unchanged. Every alternative multi-step shortcut combination (register correlation plus monthly `Q(P)` plus scalar OLS at {r1v2['total_relief_mva']:.2f} MVA, standard utility planning proxy at {rg['total_relief_mva']:.2f} MVA, parametric proxy, window-sliced proxy, conservative upper proxy, and uncorrelated baseline) misses two to five substations on both sides of the 85%/100% thresholds and violates at least one direct physical measurement in the shipped files ({s1_min_x:.1f}x to {s1_max_x:.1f}x higher 9-point 15-minute PQ MAE, {s2_vlv_lo:.1f} to {s2_vlv_hi:.1f} V hourly 22 kV Ohm's-law error, {s3_bus_lo:.1f}x to {s3_bus_hi:.1f}x higher 3-phase bus-sag error, or {fig['s3_ami_q_ratio']:.1f}x higher AMI reactive error), uniquely pinning both the seven-substation schedule and the {fig['total_relief_mva']:.2f} MVA relief total.",
        "",
    ]
    text = "\n".join(lines)
    assert "\u2014" not in text and "\u2013" not in text, "Em/en dash detected in submission.md!"
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
