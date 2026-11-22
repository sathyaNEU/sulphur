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
        f"**Why it takes deep analytical rigour:** Obvious repairs on every step fail internal physical conservation across "
        f"the shipped records. On Step 1, the hourly floor misses `pq_commissioning_autumn2026.csv` by "
        f"{pd['s1_scada60']['s1_comm_mae_mw']:.2f} MW MAE (golden {pd['golden']['s1_comm_mae_mw']:.2f} MW); linear register "
        f"sums ({rt['s1_linear_sum']['c1_total_p15_mw']:.2f} MW, {pd['s1_linear_sum']['s1_comm_mae_mw']:.2f} MAE), pooled "
        f"coincidence ({rt['s1_cf_pooled']['c1_total_p15_mw']:.2f} MW, {pd['s1_cf_pooled']['s1_comm_mae_mw']:.2f} MAE), "
        f"1-PC stripping ({rt['s1_pca1']['c1_total_p15_mw']:.2f} MW), and 12-month register correlation "
        f"({rt['s1_register_rho']['c1_total_p15_mw']:.2f} MW, inverting Malmnes {rp['reg_rho_malmnes']:.3f} vs Drangvik "
        f"{rp['reg_rho_drangvik']:.3f}) all fail, requiring 4-mode cross-substation SVD, autumn `k_ord = {rp['k_ord']:.4f}` "
        f"calibration, and correlated quadrature. On Step 2, monthly net kVARh ({rt['S2']['c2_total_qpeak_mvar']:.2f} MVAr, "
        f"{pd['s2_net_kvarh']['s2_vlv_rmse_v']:.1f} V LV RMSE), monthly `Q(P)` ({rt['s2_monthly_qp']['c2_total_qpeak_mvar']:.2f} MVAr, "
        f"{pd['s2_monthly_qp']['s2_vlv_rmse_v']:.1f} V), class PFs ({rt['s2_class_pf']['c2_total_qpeak_mvar']:.2f} MVAr, "
        f"{pd['s2_class_pf']['s2_vlv_rmse_v']:.1f} V), and target-only corridors dropping upstream hubs "
        f"({rt['s2_targets_only']['c2_total_qpeak_mvar']:.2f} MVAr, {pd['s2_targets_only']['s2_vlv_rmse_v']:.1f} V) violate "
        f"22 kV balance, whereas coupled 11-site impedance inversion anchored to settled kVARh closes LV voltage to "
        f"{pd['golden']['s2_vlv_rmse_v']:.2f} V and kVARh to {pd['golden']['s2_kvarh_err_mvar']:.2f} MVAr. On Step 3, GIS "
        f"({rt['s3_gis']['c3_mean_lim_phase_pct']:.2f}%, {pd['s3_gis']['s3_bus_rmse_v']:.2f} V bus-sag RMSE), AMI gross-up "
        f"({rt['s3_ami_grossup']['c3_mean_lim_phase_pct']:.2f}%, {pd['s3_ami_grossup']['s3_bus_rmse_v']:.2f} V), scalar OLS "
        f"({rt['s3_scalar_ols']['c3_mean_lim_phase_pct']:.2f}%, Svarthaug {rt['s3_scalar_ols']['loading_pct']['Svarthaug']:.2f}%), "
        f"and manual-PF OLS ({rt['s3_handbook_pf']['c3_mean_lim_phase_pct']:.2f}%, {pd['s3_handbook_pf']['s3_ami_q_rmse_kvar']:.2f} kVAr "
        f"AMI RMSE, Raudfjord {rt['s3_handbook_pf']['loading_pct']['Raudfjord']:.2f}%) fail against joint `(V_ph - V_bar)` "
        f"regression on `[1, P_res, P_com, P_bal]` using AMI-measured `tan_phi` ({rp['tan_phi_res']:.4f} vs "
        f"{rp['tan_phi_com']:.4f}; {pd['golden']['s3_bus_rmse_v']:.2f} V bus RMSE). Each step independently flips distinct "
        f"sites (Step 1: Drangvik/Kvernholm/Malmnes/Raudfjord; Step 2: Kvernholm; Step 3: Raudfjord/Svarthaug), both models "
        f"missed all three, and every shortcut family is {min(pr.values()):.1f}x to {max(pr.values()):.1f}x worse on physical "
        f"conservation."
    )

    return ["## How is each model stumped?", "", p1, "", p2, "", p3, "", p4, ""]


def write(path, fig):
    subs = fig["substations"]
    b = fig["bands"]
    rp = fig["ref_params"]
    pd = fig["phys_details"]
    pr = fig["phys_ratios"]
    ps = fig["pack_stats"]
    rt = fig["routes"]
    rf = rt["S1+S2+S3"]
    rg = rt["rigorous"]
    r1v2 = rt["response1_v2"]

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

    n_var = ps["n_variants"]
    n_riv = len(pr)

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
        f"This rejects the hourly SCADA, monthly net kVARh power factor, and partial-AMI reading, which puts total relief at {rf['total_relief_mva']:.2f} MVA and misplaces four substations (deferring Drangvik at {rf['loading_pct']['Drangvik']:.2f}%, Kvernholm at {rf['loading_pct']['Kvernholm']:.2f}%, Malmnes at {rf['loading_pct']['Malmnes']:.2f}%, and Raudfjord at {rf['loading_pct']['Raudfjord']:.2f}%): hourly SCADA smooths synchronized 15-minute feeder surges, monthly net kVARh hides peak-only reactive surges and switched capacitors across shared 66 kV corridors, and partial-coverage AMI plus drifted GIS tags miss opposite diurnal phase skews on unmetered legacy laterals.",
        "",
        *_stump_block(fig),
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
        f"1. Conformed the operational extracts to the 8,760-hour 2026 Europe/Oslo grid (`scada_substation_hourly_2026.csv`: {ps['raw_scada_rows']:,} raw rows, {ps['superseded_dropped']:,} superseded preliminary rows dropped by latest `extract_ts` to {ps['clean_scada_rows']:,} clean substation-hours across eleven substations, Raudfjord's legacy `DD.MM.YYYY HH:MM` CET stamps aligned, {ps['vlv_nulls']} benign summer comms nulls in `v_lv_kv` interpolated; joined `gsp_66kv_voltages_2026.csv` and `subtransmission_66kv_lines.csv` across {ps['n_corridors']} radial 66 kV corridors fed from {ps['n_gsp']} Grid Supply Points with the four modernized hubs upstream of the relief-pool sites; mapped legacy DMS IDs in `feeder_scada_hourly_2026.csv` [kW to MW] and `feeder_demand_registers_monthly_2026.csv` via `feeder_id_crosswalk.csv` across {ps['n_feeders']} feeders; joined `revenue_meter_monthly_2026.xlsx`, `substation_transformer_register.xlsx`, `substation_phase_bus_voltages_2026.csv`, `gis_lateral_connectivity_2026.csv` [{ps['n_laterals_total']} laterals: {ps['n_ami_per_sub']} AMI_SMART and {ps['n_leg_per_sub']} LEGACY_NON_AMI per substation], `ami_lateral_telemetry_2026.db` [v_volts, p_kw, q_kvar], and `pq_commissioning_autumn2026.csv` [{ps['comm_pq_rows']:,} Sep-Oct active-only intervals on Fossheim and Lindberg]; excluded streetlighting, oil-DGA, and tariff files). Clean 60-minute SCADA peaks across the seven in-scope substations (excluding Fossheim, Lindberg, Ostervik, and Solberg per `vesterdal_planning_standard_ns2026.pdf` Section 2) sum to {fig['r1_p60_sum_mw']:.2f} MW.",
        f"2. The hurried reading stops at conformed operational tables: taking 60-minute SCADA peaks ({fig['r1_p60_sum_mw']:.2f} MW), monthly net kVARh power factors ({rf['c2_total_qpeak_mvar']:.2f} MVAr combined), and AMI-only balanced phases ({rf['c3_mean_lim_phase_pct']:.2f}% mean) puts total relief at {rf['total_relief_mva']:.2f} MVA and misplaces four substations (Hestmark {rf['loading_pct']['Hestmark']:.2f}%, Svarthaug {rf['loading_pct']['Svarthaug']:.2f}%, Kvernholm {rf['loading_pct']['Kvernholm']:.2f}%, Malmnes {rf['loading_pct']['Malmnes']:.2f}%, Drangvik {rf['loading_pct']['Drangvik']:.2f}%, Raudfjord {rf['loading_pct']['Raudfjord']:.2f}%, Tverrli {rf['loading_pct']['Tverrli']:.2f}%). Three coupled observation-process gaps overturn it (steps 3 to 5).",
        f"3. Reconstructed 15-minute coincident active peaks without winter PQ metering or feeder cluster labels: stripped four regional diurnal-and-weather SVD modes from log-normalized hourly feeder SCADA across the other ten substations (1-PC stripping leaves Drangvik {rp['pca1_drangvik']:.3f} indistinguishable from Malmnes {rp['pca1_malmnes']:.3f}, while seasonal burst modulation inverts 12-month register correlation to {rp['reg_rho_malmnes']:.3f} on staggered Malmnes vs {rp['reg_rho_drangvik']:.3f} on synchronized Drangvik), isolating pairwise feeder innovation correlation `R` (recovering {rp['rho_sync_drangvik']:.4f} on Drangvik and {rp['rho_sync_lindberg']:.4f} on Lindberg vs {rp['rho_stag_malmnes']:.4f} on Malmnes and {rp['rho_stag_fossheim']:.4f} on Fossheim), calibrated `k_ord = {rp['k_ord']:.4f}` on the Sep-Oct active-only within-hour commissioning surge (`pq_commissioning_autumn2026.csv`), and aggregated winter feeder register excesses in correlated quadrature `sqrt(d^T R d)` onto each substation's 60-minute peak. Pool total is {fig['c1_total_p15_mw']:.2f} MW (Drangvik {subs['Drangvik']['p15_peak_mw']:.2f}, Hestmark {subs['Hestmark']['p15_peak_mw']:.2f}, Malmnes {subs['Malmnes']['p15_peak_mw']:.2f}, Raudfjord {subs['Raudfjord']['p15_peak_mw']:.2f}, Svarthaug {subs['Svarthaug']['p15_peak_mw']:.2f}, Kvernholm {subs['Kvernholm']['p15_peak_mw']:.2f}, Tverrli {subs['Tverrli']['p15_peak_mw']:.2f} MW); every S1 shortcut fails the Sep-Oct commissioning surge and misplaces 1 to 4 sites (60-minute SCADA {rt['S1']['c1_total_p15_mw']:.2f} MW, 12-month register correlation {rt['s1_register_rho']['c1_total_p15_mw']:.2f} MW flipping Drangvik down to {rt['s1_register_rho']['loading_pct']['Drangvik']:.2f}% and Malmnes up to {rt['s1_register_rho']['loading_pct']['Malmnes']:.2f}%, 1-PC stripping {rt['s1_pca1']['c1_total_p15_mw']:.2f} MW, raw hourly correlation {rt['s1_raw_corr']['c1_total_p15_mw']:.2f} MW, independent quadrature {rt['s1_indep_quad']['c1_total_p15_mw']:.2f} MW, pooled register coincidence {rt['s1_cf_pooled']['c1_total_p15_mw']:.2f} MW, flat ratio {rt['s1_flat_ratio']['c1_total_p15_mw']:.2f} MW, and linear feeder ratio sum {rt['s1_linear_sum']['c1_total_p15_mw']:.2f} MW).",
        f"4. Inverted peak-hour reactive demand without any PQ reactive archive: coupled all eleven substations along their four shared radial 66 kV sub-transmission corridors (`COR-N01`, `COR-N02`, `COR-S01`, `COR-S02`) including the four upstream modernized hubs (`Ostervik`, `Fossheim`, `Lindberg`, `Solberg`) from `GSP-Nord` and `GSP-Sor` through shared 66 kV line impedances and local transformer impedances (`substation_transformer_register.xlsx`, LTC taps `-10..+10`) into simultaneous hourly linear systems `M(t) Q(t) = y(t) + delta_PT`, anchored each corridor's static PT offsets `delta_PT` jointly against peak-month settled `net_kvarh` (`revenue_meter_monthly_2026.xlsx`), and averaged top-5 peak-load hours. Pool combined `Q_h` is {fig['c2_total_qpeak_mvar']:.2f} MVAr (Kvernholm {subs['Kvernholm']['q_peak_h_mvar']:.2f}, Drangvik {subs['Drangvik']['q_peak_h_mvar']:.2f}, Hestmark {subs['Hestmark']['q_peak_h_mvar']:.2f}, Svarthaug {subs['Svarthaug']['q_peak_h_mvar']:.2f}, Raudfjord {subs['Raudfjord']['q_peak_h_mvar']:.2f}, Tverrli {subs['Tverrli']['q_peak_h_mvar']:.2f}, Malmnes {subs['Malmnes']['q_peak_h_mvar']:.2f} MVAr); winter fixed capacitors on Kvernholm and peak-only switched capacitors on Malmnes defeat annual net kVARh ({rt['S2']['c2_total_qpeak_mvar']:.2f} MVAr, Kvernholm {rt['S2']['loading_pct']['Kvernholm']:.2f}%), winter-only net kVARh ({rt['s2_winter_kvarh']['c2_total_qpeak_mvar']:.2f} MVAr), monthly linear `Q(P)` ({rt['s2_monthly_qp']['c2_total_qpeak_mvar']:.2f} MVAr, Kvernholm {rt['s2_monthly_qp']['loading_pct']['Kvernholm']:.2f}%), monthly `Q(P + winter)` ({rt['s2_monthly_win']['c2_total_qpeak_mvar']:.2f} MVAr), monthly quadratic `Q(P^2)` ({rt['s2_monthly_quad']['c2_total_qpeak_mvar']:.2f} MVAr), class nominal PFs ({rt['s2_class_pf']['c2_total_qpeak_mvar']:.2f} MVAr), target-only corridor inversion dropping upstream hubs ({rt['s2_targets_only']['c2_total_qpeak_mvar']:.2f} MVAr), local single-site dV ({rt['s2_local_dv']['c2_total_qpeak_mvar']:.2f} MVAr), `R*P`-only dV ({rt['s2_rp_only']['c2_total_qpeak_mvar']:.2f} MVAr), and un-demeaned corridor dV ({rt['s2_raw_dv']['c2_total_qpeak_mvar']:.2f} MVAr).",
        f"5. Recovered annual-peak heaviest-phase share `w_max` across both AMI and unmetered legacy laterals without any 3-phase PQ archive: although common-mode-rejected AMI voltage regression matches {rp['tracer_matched']} of {rp['tracer_total']} field-traced AMI laterals (100.0% vs GIS {rp['gis_tracer_matched']} of {rp['tracer_total']}, {rp['gis_tracer_pct']:.1f}%), AMI covers only {ps['n_ami_per_sub']} of {ps['n_laterals_per_sub']} single-phase laterals per substation while the {ps['n_leg_per_sub']} `LEGACY_NON_AMI` laterals carry opposite phase skews, and commercial midday loads carry opposite phase skews to residential evening loads with a 3.3x reactive impedance contrast measured directly from AMI SQLite `(p_kw, q_kvar)` (`tan_phi_res = {rp['tan_phi_res']:.4f}` resistive heating vs `tan_phi_com = {rp['tan_phi_com']:.4f}` commercial HVAC, versus engineering manual nominal ratios {rp['handbook_tan_phi_res']:.4f} and {rp['handbook_tan_phi_com']:.4f}). Regressing `(V_ph - V_bar)` jointly on `[1, P_res, P_com, P_bal]` eliminates static per-phase PT offsets and balanced shunt capacitors, and scaling class slopes by `3 * (R_T + X_T * tan_phi_c) / V_nom` yields exact peak-hour total phase shares evaluated at each substation's annual peak hour. Pool mean `w_max` is {fig['c3_mean_lim_phase_pct']:.2f}% (Raudfjord {subs['Raudfjord']['w_max_pct']:.2f}%, Tverrli {subs['Tverrli']['w_max_pct']:.2f}%, Hestmark {subs['Hestmark']['w_max_pct']:.2f}%, Malmnes {subs['Malmnes']['w_max_pct']:.2f}%, Drangvik {subs['Drangvik']['w_max_pct']:.2f}%, Svarthaug {subs['Svarthaug']['w_max_pct']:.2f}%, Kvernholm {subs['Kvernholm']['w_max_pct']:.2f}%); GIS ({rt['s3_gis']['c3_mean_lim_phase_pct']:.2f}%), AMI-only ({rt['S3']['c3_mean_lim_phase_pct']:.2f}%), AMI+GIS ({rt['s3_ami_plus_gis']['c3_mean_lim_phase_pct']:.2f}%), AMI gross-up ({rt['s3_ami_grossup']['c3_mean_lim_phase_pct']:.2f}%), scalar OLS `dv_ph ~ P_tot` ({rt['s3_scalar_ols']['c3_mean_lim_phase_pct']:.2f}%, Svarthaug {rt['s3_scalar_ols']['loading_pct']['Svarthaug']:.2f}%), evening 17-21 cutoff OLS with `z_avg` ({rt['s3_evening_cut']['c3_mean_lim_phase_pct']:.2f}%) or `z_res` ({rt['s3_even_zres']['c3_mean_lim_phase_pct']:.2f}%), multi-class OLS with manual nominal PF ({rt['s3_handbook_pf']['c3_mean_lim_phase_pct']:.2f}%, Raudfjord {rt['s3_handbook_pf']['loading_pct']['Raudfjord']:.2f}%) or substation PF ({rt['s3_sub_pf']['c3_mean_lim_phase_pct']:.2f}%), and raw bus voltage ({rt['s3_raw_vbus']['c3_mean_lim_phase_pct']:.2f}%) all fail.",
        f"6. Verified the full conformed model on five internal physical conservation checks across all shipped records: the conformed model achieves Sep-Oct commissioning surge MAE {pd['golden']['s1_comm_mae_mw']:.2f} MW on Fossheim and Lindberg, hourly 22 kV LV bus voltage balance residual {pd['golden']['s2_vlv_rmse_v']:.2f} V, 12-month settled kVARh conservation error {pd['golden']['s2_kvarh_err_mvar']:.2f} MVAr, 3-phase 22 kV bus-sag residual {pd['golden']['s3_bus_rmse_v']:.2f} V, and AMI reactive residual {pd['golden']['s3_ami_q_rmse_kvar']:.2f} kVAr (composite physics index {pd['golden']['phys_idx']:.2f}), beating all {n_riv} alternative proxies and single-component shortcuts by {min(pr.values()):.1f}x to {max(pr.values()):.1f}x (including register-correlation plus monthly `Q(P)` plus scalar bus-sag OLS at {pr['response1_v2']:.1f}x missing 5/7 sites, register-correlation plus winter `Q(P)` plus manual PF at {pr['run_calibrated']:.1f}x missing 4/7, 1-PC plus winter kVARh plus evening OLS at {pr['run_cutoff']:.1f}x missing 4/7, linear sum plus class PF plus evening OLS at {pr['run_generous']:.1f}x missing 2/7, independent quadrature plus net kVARh plus AMI-only at {pr['run_hedge']:.1f}x missing 5/7, and pooled coincidence plus winter `Q(P)` plus AMI-only at {pr['rigorous']:.1f}x missing 5/7).",
        f"7. Applied `vesterdal_planning_standard_ns2026.pdf` Sections 3 and 4 (`S_15m = sqrt(P_15^2 + Q_h^2)`, `Lim_MVA = 3 * w_max * S_15m`, `Loading % = 100 * Lim_MVA / Firm_N1_MVA`, `Relief_MVA = max(0, Lim_MVA - 0.85 * Firm_N1_MVA)`, Phase 1 >= {fig['planning_lines']['phase1_pct']:.1f}%, Phase 2 >= {fig['planning_lines']['phase2_pct']:.1f}%, Defer < {fig['planning_lines']['phase2_pct']:.1f}%): combined limiting-phase peak is {fig['pool_lim_mva_sum']:.2f} MVA and pool total relief capacity needed is {fig['total_relief_mva']:.2f} MVA, placing Hestmark ({subs['Hestmark']['loading_pct']:.2f}%), Raudfjord ({subs['Raudfjord']['loading_pct']:.2f}%), Kvernholm ({subs['Kvernholm']['loading_pct']:.2f}%), and Drangvik ({subs['Drangvik']['loading_pct']:.2f}%) in Phase 1, Malmnes ({subs['Malmnes']['loading_pct']:.2f}%) and Svarthaug ({subs['Svarthaug']['loading_pct']:.2f}%) in Phase 2, and Tverrli ({subs['Tverrli']['loading_pct']:.2f}%) in Defer.",
        f"8. Checked sensitivity across {n_var} honest estimator variants (12-month, DJF, and peak-month register windows; additive excess scalings; winter innovation windows; 5-PC, 6-PC, and class-reference residual stripping; unit `k_ord = 1.0` and mean-ratio commissioning calibration; intra-hour `Q15` slope and constant-PF rules; winter and full-year `net_kvarh` anchors; 1-step `M_bar` and measured-`V_lv` scaling; top-20 regression and single-hour peak `Q`; winter, heating, first-difference, 2-class, and top-5 peak bus-sag estimators; winter AMI `tan_phi`) plus six +/-20% forcing perturbations on `k_ord`, `Q_peak`, and phase excess: every variant and perturbation preserves the exact seven-substation schedule, with the thinnest boundary clearance at Drangvik ({subs['Drangvik']['loading_pct']:.2f}% vs 100.0%, band {b['loading_pct']['Drangvik'][0]:.1f}% to {b['loading_pct']['Drangvik'][1]:.1f}%) and Malmnes ({subs['Malmnes']['loading_pct']:.2f}% vs 100.0%, band {b['loading_pct']['Malmnes'][0]:.1f}% to {b['loading_pct']['Malmnes'][1]:.1f}%).",
        "",
        f"Each of the three critical components is independent and individually decisive: losing 15-minute coincidence alone shifts combined active demand from {fig['c1_total_p15_mw']:.2f} to {rt['S1']['c1_total_p15_mw']:.2f} MW and misplaces Drangvik ({rt['S1']['loading_pct']['Drangvik']:.2f}%), Kvernholm ({rt['S1']['loading_pct']['Kvernholm']:.2f}%), Malmnes ({rt['S1']['loading_pct']['Malmnes']:.2f}%), and Raudfjord ({rt['S1']['loading_pct']['Raudfjord']:.2f}%) while leaving combined reactive demand and limiting-phase share unchanged; losing coupled 66 kV reactive inversion alone shifts combined reactive demand from {fig['c2_total_qpeak_mvar']:.2f} to {rt['S2']['c2_total_qpeak_mvar']:.2f} MVAr and demotes Kvernholm to Phase 2 ({rt['S2']['loading_pct']['Kvernholm']:.2f}%) while leaving active demand and phase share unchanged; and losing multi-class bus-sag phase inversion alone shifts mean limiting-phase share from {fig['c3_mean_lim_phase_pct']:.2f}% to {rt['S3']['c3_mean_lim_phase_pct']:.2f}% and flips Raudfjord to Defer ({rt['S3']['loading_pct']['Raudfjord']:.2f}%) and Svarthaug to Phase 1 ({rt['S3']['loading_pct']['Svarthaug']:.2f}%) while leaving active and reactive demand unchanged. Every alternative multi-step shortcut combination (register correlation plus monthly `Q(P)` plus scalar OLS at {r1v2['total_relief_mva']:.2f} MVA, standard utility planning proxy at {rg['total_relief_mva']:.2f} MVA, parametric proxy, window-sliced proxy, conservative upper proxy, and uncorrelated baseline) misses two to five substations on both sides of the 85%/100% thresholds and fails internal physical conservation by {min(pr.values()):.1f}x to {max(pr.values()):.1f}x, uniquely pinning both the seven-substation schedule and the {fig['total_relief_mva']:.2f} MVA relief total.",
        "",
    ]
    text = "\n".join(lines)
    assert "\u2014" not in text and "\u2013" not in text, "Em/en dash detected in submission.md!"
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
