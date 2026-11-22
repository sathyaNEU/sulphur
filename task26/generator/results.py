"""Compute every owed figure strictly from the cut pack under target/, re-prove corelib.run(spec) on the
shipped files, and emit figures.json and effort.json (v3).

    python3 task26/generator/results.py
"""
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), ".claude", "skills", "stumping"))
import corelib  # noqa: E402
import analysis as A  # noqa: E402
import core as C  # noqa: E402

TARGETS = C.TARGETS
REFS = C.REFS
ALL_SUBS = C.ALL_SUBS


def phase_label(loading_pct):
    if loading_pct >= C.LINE_P1:
        return "Phase 1 (2027)"
    if loading_pct >= C.LINE_P2:
        return "Phase 2 (2028-2029)"
    return "Defer"


def schedule_list(res):
    return [f"{s}: {phase_label(res[s]['loading_pct'])}" for s in TARGETS]


def band_of(gold_val, fam_vals, step):
    lo = min(fam_vals + [gold_val])
    hi = max(fam_vals + [gold_val])
    room = corelib.BAND_ROOM * (hi - lo)
    q = 1.0 / step
    return [round(math.floor((lo - room) * q + 1e-9) / q, 6),
            round(math.ceil((hi + room) * q - 1e-9) / q, 6)]


def run(target_dir):
    pack_world, stats = A.load_pack(target_dir)

    # Attach target truth solely for corelib's golden-vs-truth call check; every estimated figure comes 100% from pack_world!
    sim_world = C.simulate()
    for s in TARGETS:
        pack_world["subs"][s]["truth"] = sim_world["subs"][s]["truth"]

    spec, _w, gold_res, lat_res, dir_res, rig_res, gold_p, rivals, rival_diag = C.build_spec(pack_world)
    code = corelib.run(spec)
    assert code == 0, "corelib failed on cut pack!"

    fam_res = [(name, opts, C.evaluate(pack_world, opts)[0]) for name, opts in C.FAMILY]
    fam_only = [r for _, _, r in fam_res]

    # Quick pass: raw uncleaned SCADA CSV without deduplication, net_kvarh, balanced 33.3%
    raw_world, _ = A.load_pack(target_dir, include_superseded=True, interpolate_nulls=True)
    for s in TARGETS:
        raw_world["subs"][s]["truth"] = sim_world["subs"][s]["truth"]
    quick_res, quick_p = C.evaluate(raw_world, C.DIRECT)
    quick_p60_sum = round(sum(float(raw_world["subs"][s]["sub_p60"].max()) for s in TARGETS), 2)

    r1_p60_by_sub = {s: round(float(pack_world["subs"][s]["sub_p60"].max()), 2) for s in TARGETS}
    r1_p60_sum = round(sum(float(pack_world["subs"][s]["sub_p60"].max()) for s in TARGETS), 2)

    # Verify AMI phase-ID accuracy on the 80 field-traced AMI laterals (20 x 4 modernized sites)
    ref_tracer_matched = 0
    ref_tracer_total = 0
    gis_tracer_matched = 0
    for r in REFS:
        sd = pack_world["subs"][r]
        pred = C._identify_ami_phases(sd)
        ami_gis = sd["lat_gis_ph"][sd["lat_is_ami"]]
        ref_tracer_matched += int((pred == sd["ami_true_ph"]).sum())
        gis_tracer_matched += int((ami_gis == sd["ami_true_ph"]).sum())
        ref_tracer_total += len(sd["ami_true_ph"])

    # Innovation correlation summary: stripped pca4 vs inverted 12-month register_rho on Lindberg/Fossheim & Drangvik/Malmnes
    R_gold = C._infer_feeder_corr_matrices(pack_world, {})
    R_reg = C._infer_feeder_corr_matrices(pack_world, {"s1_mode": "register_rho"})
    R_p1 = C._infer_feeder_corr_matrices(pack_world, {"s1_mode": "pca1"})

    def _off5(R):
        sub = R[:5, :5]
        return float(sub[~np.eye(5, dtype=bool)].mean())

    rho_sync_lb = _off5(R_gold["Lindberg"])
    rho_stag_fh = _off5(R_gold["Fossheim"])
    rho_sync_dr = _off5(R_gold["Drangvik"])
    rho_stag_ml = _off5(R_gold["Malmnes"])
    reg_rho_dr = _off5(R_reg["Drangvik"])
    reg_rho_ml = _off5(R_reg["Malmnes"])
    reg_rho_lb = _off5(R_reg["Lindberg"])
    reg_rho_fh = _off5(R_reg["Fossheim"])
    pca1_dr = _off5(R_p1["Drangvik"])
    pca1_ml = _off5(R_p1["Malmnes"])

    g_c1, g_c2, g_c3 = C._agg_components(gold_res)
    f_c1 = [C._agg_components(fr)[0] for fr in fam_only]
    f_c2 = [C._agg_components(fr)[1] for fr in fam_only]
    f_c3 = [C._agg_components(fr)[2] for fr in fam_only]

    c1_band = band_of(g_c1, f_c1, 0.1)
    c2_band = band_of(g_c2, f_c2, 0.1)
    c3_band = band_of(g_c3, f_c3, 0.01)

    load_bands = {s: band_of(gold_res[s]["loading_pct"], [fr[s]["loading_pct"] for fr in fam_only], 0.1) for s in TARGETS}
    mva_bands = {s: band_of(gold_res[s]["lim_mva"], [fr[s]["lim_mva"] for fr in fam_only], 0.05) for s in TARGETS}
    p15_bands = {s: band_of(gold_res[s]["p15"], [fr[s]["p15"] for fr in fam_only], 0.05) for s in TARGETS}
    qh_bands = {s: band_of(gold_res[s]["q_h"], [fr[s]["q_h"] for fr in fam_only], 0.05) for s in TARGETS}
    w_bands = {s: band_of(100.0 * gold_res[s]["w_max"], [100.0 * fr[s]["w_max"] for fr in fam_only], 0.05) for s in TARGETS}
    rel_tot_gold = sum(gold_res[s]["relief_mva"] for s in TARGETS)
    rel_tot_band = band_of(rel_tot_gold, [sum(fr[s]["relief_mva"] for s in TARGETS) for fr in fam_only], 0.1)

    phys_idx = {"golden": round(gold_p["phys_idx"], 2)}
    phys_details = {"golden": {
        "s1_comm_mae_mw": round(gold_p["s1_comm_mae"], 3),
        "s2_vlv_rmse_v": round(gold_p["s2_vlv_mv"], 2),
        "s2_kvarh_err_mvar": round(gold_p["s2_mvar_err"], 3),
        "s3_bus_rmse_v": round(gold_p["s3_bus_mv"], 2),
        "s3_ami_q_rmse_kvar": round(gold_p["s3_amiq"], 2),
        "phys_idx": round(gold_p["phys_idx"], 2),
    }}
    for rname, rdiag in rival_diag.items():
        phys_idx[rname] = round(rdiag["phys_idx"], 2)
        phys_details[rname] = {
            "s1_comm_mae_mw": round(rdiag["s1_comm_mae"], 3),
            "s2_vlv_rmse_v": round(rdiag["s2_vlv_mv"], 2),
            "s2_kvarh_err_mvar": round(rdiag["s2_mvar_err"], 3),
            "s3_bus_rmse_v": round(rdiag["s3_bus_mv"], 2),
            "s3_ami_q_rmse_kvar": round(rdiag["s3_amiq"], 2),
            "phys_idx": round(rdiag["phys_idx"], 2),
        }
    phys_ratios = {k: round(v / gold_p["phys_idx"], 1) for k, v in phys_idx.items() if k != "golden"}

    # Exact corelib rubric scores for all routes including RESPONSE1_V2 and all 4 run_routes!
    figs_cl, _ = corelib._figures(spec, spec["lattice"])
    gcall_cl = corelib._calls(spec, {s: gold_res[s]["loading_pct"] for s in TARGETS})
    route_scores = {"golden": 100.0}
    for rn in ("rigorous", "response1_v2"):
        sc_val, _ = corelib._route_score(spec, figs_cl, rn, gcall_cl)
        route_scores[rn] = round(float(sc_val), 1)
    for rn in ("generous", "calibrated", "hedge", "cutoff"):
        call_ok = (corelib._calls(spec, spec["run_routes"][rn]) == gcall_cl)
        route_scores[rn] = round(float(corelib._score(figs_cl, call_ok, lambda f, rr=rn: f["routes"][rr])), 1)
    for k in ("S1", "S2", "S3", "S1+S2", "S1+S3", "S2+S3", "S1+S2+S3"):
        call_ok = (corelib._calls(spec, spec["lattice"][k]) == gcall_cl)
        route_scores[k] = round(float(corelib._score(figs_cl, call_ok, lambda f, kk=k: f["values"][kk])), 1)

    # Forcing +/- 20% perturbations on cut pack
    pert_defs = [
        ("k_ord -20%", {"mult_kord": 0.80}),
        ("k_ord +20%", {"mult_kord": 1.20}),
        ("Q_peak -20%", {"mult_q": 0.80}),
        ("Q_peak +20%", {"mult_q": 1.20}),
        ("phase_excess -20%", {"mult_w_excess": 0.80}),
        ("phase_excess +20%", {"mult_w_excess": 1.20}),
    ]
    forcing_rows = []
    for pname, popts in pert_defs:
        pr, _ = C.evaluate(pack_world, popts)
        forcing_rows.append(dict(
            input=pname,
            answer=schedule_list(pr),
            loading_pct={s: round(pr[s]["loading_pct"], 2) for s in TARGETS},
            holds=(schedule_list(pr) == schedule_list(gold_res)),
        ))

    subs_out = {}
    for s in ALL_SUBS:
        sd = pack_world["subs"][s]
        g = gold_res[s]
        firm = float(sd["cfg"]["firm_mva"])
        subs_out[s] = dict(
            in_pool=(s in TARGETS),
            corridor=sd["corridor"],
            gsp=sd["gsp"],
            firm_n1_mva=round(firm, 1),
            p60_peak_mw=round(float(sd["sub_p60"].max()), 2),
            p15_peak_mw=round(g["p15"], 2),
            q_peak_h_mvar=round(g["q_h"], 2),
            q15_at_peak_mvar=round(g["q15"], 2),
            s15_tot_mva=round(g["s15_tot"], 2),
            w_max_pct=round(100.0 * g["w_max"], 2),
            lim_mva=round(g["lim_mva"], 2),
            loading_pct=round(g["loading_pct"], 2),
            relief_mva=round(g["relief_mva"], 2),
            p60_peak_mw_raw=float(sd["sub_p60"].max()),
            p15_peak_mw_raw=float(g["p15"]),
            q_peak_h_mvar_raw=float(g["q_h"]),
            w_max_pct_raw=float(100.0 * g["w_max"]),
            lim_mva_raw=float(g["lim_mva"]),
            loading_pct_raw=float(g["loading_pct"]),
            relief_mva_raw=float(g["relief_mva"]),
            phase=phase_label(g["loading_pct"]) if s in TARGETS else "Modernized (Excluded)",
        )
        if s in C.PQ_COMM_SITES:
            subs_out[s]["comm_obs_surge_mw"] = round(float((sd["comm_p15"].max(axis=1) - sd["sub_p60"][C.COMM_HOURS]).max()), 2)
            rq = C._quad_excess(sd, R_gold[s], list(C.COMM_MONTHS))
            subs_out[s]["comm_est_surge_mw"] = round(float(gold_p["k_ord"] * rq), 2)

    all_routes = {
        "golden": (gold_res, gold_p),
        "S1": (lat_res["S1"], rival_diag["s1_scada60"]),
        "S2": (lat_res["S2"], rival_diag["s2_net_kvarh"]),
        "S3": (lat_res["S3"], rival_diag["s3_ami_only"]),
        "S1+S2": (lat_res["S1+S2"], C.evaluate(pack_world, {**C.HURRIED["S1"], **C.HURRIED["S2"]})[1]),
        "S1+S3": (lat_res["S1+S3"], C.evaluate(pack_world, {**C.HURRIED["S1"], **C.HURRIED["S3"]})[1]),
        "S2+S3": (lat_res["S2+S3"], C.evaluate(pack_world, {**C.HURRIED["S2"], **C.HURRIED["S3"]})[1]),
        "S1+S2+S3": (lat_res["S1+S2+S3"], rival_diag["reflex"]),
    }
    for rname, rres in rivals.items():
        if rname not in all_routes:
            all_routes[rname] = (rres, rival_diag[rname])

    routes_out = {}
    for rname, (rres, rdiag) in all_routes.items():
        rc1, rc2, rc3 = C._agg_components(rres)
        routes_out[rname] = dict(
            answer=schedule_list(rres),
            wrong_count=sum(a != b for a, b in zip(schedule_list(rres), schedule_list(gold_res))),
            c1_total_p15_mw=round(rc1, 2),
            c2_total_qpeak_mvar=round(rc2, 2),
            c3_mean_lim_phase_pct=round(rc3, 2),
            total_relief_mva=round(sum(rres[s]["relief_mva"] for s in TARGETS), 2),
            loading_pct={s: round(rres[s]["loading_pct"], 2) for s in TARGETS},
            lim_mva={s: round(rres[s]["lim_mva"], 2) for s in TARGETS},
            phys_idx=round(rdiag["phys_idx"], 2),
            phys_ratio=round(rdiag["phys_idx"] / gold_p["phys_idx"], 1),
        )

    variants_out = []
    for vname, _vopts, vres in fam_res:
        vc1, vc2, vc3 = C._agg_components(vres)
        variants_out.append(dict(
            name=vname,
            answer=schedule_list(vres),
            holds=(schedule_list(vres) == schedule_list(gold_res)),
            c1_total_p15_mw=round(vc1, 2),
            c2_total_qpeak_mvar=round(vc2, 2),
            c3_mean_lim_phase_pct=round(vc3, 2),
            total_relief_mva=round(sum(vres[s]["relief_mva"] for s in TARGETS), 2),
            loading_pct={s: round(vres[s]["loading_pct"], 2) for s in TARGETS},
            lim_mva={s: round(vres[s]["lim_mva"], 2) for s in TARGETS},
        ))

    load_table_gold = {s: round(gold_res[s]["loading_pct"], 2) for s in TARGETS}
    mva_relief_gold = {f"MVA_{s}": round(gold_res[s]["lim_mva"], 2) for s in TARGETS}
    mva_relief_gold["Total_Relief_MVA"] = round(rel_tot_gold, 2)
    mva_relief_bands = {f"MVA_{s}": mva_bands[s] for s in TARGETS}
    mva_relief_bands["Total_Relief_MVA"] = rel_tot_band

    phase1_subs = [s for s in TARGETS if gold_res[s]["loading_pct"] >= C.LINE_P1]
    phase2_subs = [s for s in TARGETS if C.LINE_P2 <= gold_res[s]["loading_pct"] < C.LINE_P1]
    defer_subs = [s for s in TARGETS if gold_res[s]["loading_pct"] < C.LINE_P2]

    fig = dict(
        task="task26",
        architecture="v3",
        as_of="2027-01-20",
        seed=C.SEED,
        targets=list(TARGETS),
        refs=list(REFS),
        comm_pq_sites=list(C.PQ_COMM_SITES),
        planning_lines=dict(
            phase2_pct=C.LINE_P2, phase1_pct=C.LINE_P1, limiting_factor=3, tap_step_pct=1.25,
            isp_minutes=15, hours_per_year=C.N_HOURS, tap_step_frac=C.TAP_STEP,
            v_nom_lv_kv=C.V_NOM_LV, v_nom_hv_kv=C.V_NOM_HV, v_lat_nom_v=230.0,
            kw_per_mw=1000, min_bus_slope=0.1, relief_ceiling_frac=0.85, year=2026,
            n_ami_per_sub=C.N_AMI_LAT, n_leg_per_sub=C.N_LEG_LAT, n_laterals_per_sub=C.N_LATERALS,
        ),
        pack_stats=dict(
            raw_scada_rows=stats["raw_scada_rows"],
            clean_scada_rows=C.N_HOURS * len(ALL_SUBS),
            superseded_dropped=stats["superseded_dropped"],
            vlv_nulls=stats["vlv_nulls"],
            comm_pq_rows=stats["comm_pq_rows"],
            n_feeders=sum(len(pack_world["subs"][s]["f_meta"]) for s in ALL_SUBS),
            n_corridors=stats["n_corridors"],
            n_gsp=stats["n_gsp"],
            n_ami_per_sub=C.N_AMI_LAT,
            n_leg_per_sub=C.N_LEG_LAT,
            n_laterals_per_sub=C.N_LATERALS,
            n_laterals_total=C.N_LATERALS * len(ALL_SUBS),
            n_ami_total=C.N_AMI_LAT * len(ALL_SUBS),
            n_variants=len(C.FAMILY),
        ),
        ref_params=dict(
            rho_sync_lindberg=round(rho_sync_lb, 4),
            rho_stag_fossheim=round(rho_stag_fh, 4),
            rho_sync_drangvik=round(rho_sync_dr, 4),
            rho_stag_malmnes=round(rho_stag_ml, 4),
            reg_rho_drangvik=round(reg_rho_dr, 4),
            reg_rho_malmnes=round(reg_rho_ml, 4),
            reg_rho_lindberg=round(reg_rho_lb, 4),
            reg_rho_fossheim=round(reg_rho_fh, 4),
            pca1_drangvik=round(pca1_dr, 4),
            pca1_malmnes=round(pca1_ml, 4),
            k_ord=round(gold_p["k_ord"], 4),
            k_ord_raw=float(gold_p["k_ord"]),
            tan_phi_res=round(gold_p["tan_phi_res"], 4),
            tan_phi_com=round(gold_p["tan_phi_com"], 4),
            tan_phi_res_raw=float(gold_p["tan_phi_res"]),
            tan_phi_com_raw=float(gold_p["tan_phi_com"]),
            handbook_tan_phi_res=round(float(np.tan(np.arccos(pack_world["class_pf"]["residential_heat"]))), 4),
            handbook_tan_phi_com=round(float(np.tan(np.arccos(pack_world["class_pf"]["commercial_mixed"]))), 4),
            comm_flat=round(gold_p["comm_flat"], 4),
            comm_cf=round(gold_p["comm_cf"], 4),
            tracer_matched=ref_tracer_matched,
            tracer_total=ref_tracer_total,
            gis_tracer_matched=gis_tracer_matched,
            gis_tracer_pct=round(100.0 * gis_tracer_matched / ref_tracer_total, 1),
        ),
        phys_idx=phys_idx,
        phys_details=phys_details,
        phys_ratios=phys_ratios,
        route_scores=route_scores,
        r1_p60_sum_mw=r1_p60_sum,
        r1_p60_by_sub=r1_p60_by_sub,
        c1_total_p15_mw=round(g_c1, 2),
        c1_band=c1_band,
        c2_total_qpeak_mvar=round(g_c2, 2),
        c2_band=c2_band,
        c3_mean_lim_phase_pct=round(g_c3, 2),
        c3_band=c3_band,
        r5_phys_idx=phys_idx["golden"],
        r6_loading_pct=load_table_gold,
        r6_loading_bands=load_bands,
        r7_mva_and_relief=mva_relief_gold,
        r7_mva_and_relief_bands=mva_relief_bands,
        r8_schedule=schedule_list(gold_res),
        pool_lim_mva_sum=round(sum(gold_res[s]["lim_mva"] for s in TARGETS), 2),
        total_relief_mva=round(rel_tot_gold, 2),
        total_relief_band=rel_tot_band,
        schedule_groups=dict(phase1=phase1_subs, phase2=phase2_subs, defer=defer_subs),
        bands=dict(
            p15_mw=p15_bands,
            q_peak_mvar=qh_bands,
            w_max_pct=w_bands,
            lim_mva=mva_bands,
            loading_pct=load_bands,
            c1_total_p15_mw=c1_band,
            c2_total_qpeak_mvar=c2_band,
            c3_mean_lim_phase_pct=c3_band,
            total_relief_mva=rel_tot_band,
        ),
        substations=subs_out,
        routes=routes_out,
        variants=variants_out,
        forcing=forcing_rows,
    )

    def _r6_val(res):
        return {s: round(res[s]["loading_pct"], 2) for s in TARGETS}

    def _r7_val(res):
        d = {f"MVA_{s}": round(res[s]["lim_mva"], 2) for s in TARGETS}
        d["Total_Relief_MVA"] = round(sum(res[s]["relief_mva"] for s in TARGETS), 2)
        return d

    reflex = lat_res["S1+S2+S3"]
    E = {
        "weights": {"recommendation": 14.0, "components": 24.0, "asks": 55.0, "instruction": 7.0},
        "results": [
            {
                "id": "R1",
                "name": "conformed 2026 SCADA, GSP, corridor, feeder, meter, asset, and AMI extracts",
                "graded_as": "Step-by-Step",
                "figure": "r1_p60_sum_mw",
                "depends": [],
                "golden": r1_p60_sum,
                "band": [round(r1_p60_sum - 0.05, 2), round(r1_p60_sum + 0.05, 2)],
                "passes": {
                    "quick": quick_p60_sum,
                    "careful": r1_p60_sum,
                    "thorough": r1_p60_sum,
                },
            },
            {
                "id": "R2",
                "name": "pool 15-minute coincident active demand via 4-mode stripped innovation correlation (MW)",
                "graded_as": "Component 1",
                "figure": "c1_total_p15_mw",
                "depends": ["R1"],
                "precedent": ["L22", "L24", "L58"],
                "golden": round(g_c1, 2),
                "band": c1_band,
                "partly": [round(c1_band[0] - 2.0, 2), round(c1_band[1] + 2.0, 2)],
                "passes": {
                    "quick": round(C._agg_components(quick_res)[0], 2),
                    "careful": round(C._agg_components(reflex)[0], 2),
                    "thorough": round(g_c1, 2),
                },
            },
            {
                "id": "R3",
                "name": "pool peak-hour reactive demand via coupled 4-corridor 66 kV impedance inversion including upstream hubs (MVAr)",
                "graded_as": "Component 2",
                "figure": "c2_total_qpeak_mvar",
                "depends": ["R1"],
                "precedent": ["L16", "L43", "L44", "L48"],
                "golden": round(g_c2, 2),
                "band": c2_band,
                "partly": [round(c2_band[0] - 4.0, 2), round(c2_band[1] + 4.0, 2)],
                "passes": {
                    "quick": round(C._agg_components(quick_res)[1], 2),
                    "careful": round(C._agg_components(reflex)[1], 2),
                    "thorough": round(g_c2, 2),
                },
            },
            {
                "id": "R4",
                "name": "pool average peak limiting-phase share via multi-class bus-sag regression with AMI class tan_phi (%)",
                "graded_as": "Component 3",
                "figure": "c3_mean_lim_phase_pct",
                "depends": ["R1"],
                "precedent": ["L28", "L56", "L57"],
                "golden": round(g_c3, 2),
                "band": c3_band,
                "partly": [round(c3_band[0] - 0.3, 2), round(c3_band[1] + 0.3, 2)],
                "passes": {
                    "quick": round(C._agg_components(quick_res)[2], 2),
                    "careful": round(C._agg_components(reflex)[2], 2),
                    "thorough": round(g_c3, 2),
                },
            },
            {
                "id": "R5",
                "name": "internal physical-balance residual index across commissioning surge, 66 kV/LV voltages, monthly kVARh, 3-ph bus sag, and AMI q_kvar",
                "graded_as": "Step-by-Step",
                "figure": "r5_phys_idx",
                "depends": ["R2", "R3", "R4"],
                "precedent": ["L28", "L51"],
                "golden": phys_idx["golden"],
                "band": [0.0, 4.5],
                "partly": [4.5, 7.5],
                "passes": {
                    "quick": round(quick_p["phys_idx"], 2),
                    "careful": phys_idx["reflex"],
                    "thorough": phys_idx["golden"],
                },
            },
            {
                "id": "R6",
                "name": "Firm N-1 loading percentage by target substation",
                "graded_as": "Asks 1 to 7",
                "figure": "r6_loading_pct",
                "depends": ["R2", "R3", "R4"],
                "precedent": ["L22", "L48", "L56"],
                "golden": load_table_gold,
                "bands": load_bands,
                "passes": {
                    "quick": _r6_val(quick_res),
                    "careful": _r6_val(reflex),
                    "thorough": load_table_gold,
                },
            },
            {
                "id": "R7",
                "name": "Limiting-phase peak MVA by substation and total relief capacity (MVA)",
                "graded_as": "Asks 8 to 15",
                "figure": "r7_mva_and_relief",
                "depends": ["R2", "R3", "R4"],
                "precedent": ["L16", "L32", "L56"],
                "golden": mva_relief_gold,
                "bands": mva_relief_bands,
                "passes": {
                    "quick": _r7_val(quick_res),
                    "careful": _r7_val(reflex),
                    "thorough": mva_relief_gold,
                },
            },
            {
                "id": "R8",
                "name": "2027-2029 firm-capacity relief schedule across seven target substations",
                "graded_as": "Recommendation",
                "figure": "r8_schedule",
                "depends": ["R6"],
                "precedent": ["L22", "L48", "L56"],
                "ordered": True,
                "golden": schedule_list(gold_res),
                "passes": {
                    "quick": schedule_list(quick_res),
                    "careful": schedule_list(reflex),
                    "thorough": schedule_list(gold_res),
                },
            },
        ],
        "hints": [
            {
                "sentence": "Stripping four regional diurnal-weather SVD modes across other substations removes shared class profiles and reveals true pairwise feeder innovation correlation R_ij (inverted relative to 12-month register correlation), allowing correlated quadrature calibrated on Sep-Oct active commissioning surges.",
                "rescues": ["R2"],
            },
            {
                "sentence": "Because winter fixed capacitors flatten monthly net kVARh on inductive peaks while peak-only switched capacitors clamp peak Q without lowering monthly winter averages, peak reactive demand must be inverted simultaneously along all four 66 kV corridors including upstream modernized hubs and anchored against monthly net kVARh.",
                "rescues": ["R3"],
            },
            {
                "sentence": "Because AMI covers only 20 of 40 laterals while opposite-phase diurnal commercial and residential loads have a 3.3x reactive impedance contrast (AMI tan_phi 0.125 residential vs 0.620 commercial), evening-peak heaviest-phase share must be inverted by multi-class three-phase bus-sag regression weighted by AMI-metered class impedance.",
                "rescues": ["R4"],
            },
        ],
        "routes": [
            {"name": "golden", "answer": schedule_list(gold_res), "golden": True},
            {"name": "S1 lost alone (SCADA 60m)", "answer": schedule_list(lat_res["S1"])},
            {"name": "S2 lost alone (net kVARh PF)", "answer": schedule_list(lat_res["S2"])},
            {"name": "S3 lost alone (AMI-only balanced)", "answer": schedule_list(lat_res["S3"])},
            {"name": "S1+S2 lost", "answer": schedule_list(lat_res["S1+S2"])},
            {"name": "S1+S3 lost", "answer": schedule_list(lat_res["S1+S3"])},
            {"name": "S2+S3 lost", "answer": schedule_list(lat_res["S2+S3"])},
            {"name": "reflex route (S1+S2+S3 lost)", "answer": schedule_list(reflex)},
            {"name": "direct route", "answer": schedule_list(dir_res)},
            {"name": "rigorous standard route", "answer": schedule_list(rig_res)},
            {"name": "response1_v2 (register_rho + monthly_qp + scalar_ols)", "answer": schedule_list(rivals["response1_v2"])},
            {"name": "run_generous", "answer": schedule_list(rivals["run_generous"])},
            {"name": "run_calibrated", "answer": schedule_list(rivals["run_calibrated"])},
            {"name": "run_hedge", "answer": schedule_list(rivals["run_hedge"])},
            {"name": "run_cutoff", "answer": schedule_list(rivals["run_cutoff"])},
        ],
        "forcing": {
            "kind": "set",
            "golden_answer": schedule_list(gold_res),
            "golden_family": [{"name": v["name"], "answer": v["answer"]} for v in variants_out],
            "shortcuts": [
                {"name": "S1 lost alone", "answer": schedule_list(lat_res["S1"])},
                {"name": "S2 lost alone", "answer": schedule_list(lat_res["S2"])},
                {"name": "S3 lost alone", "answer": schedule_list(lat_res["S3"])},
                {"name": "reflex route", "answer": schedule_list(reflex)},
                {"name": "rigorous standard route", "answer": schedule_list(rig_res)},
                {"name": "response1_v2", "answer": schedule_list(rivals["response1_v2"])},
                {"name": "run_generous", "answer": schedule_list(rivals["run_generous"])},
                {"name": "run_calibrated", "answer": schedule_list(rivals["run_calibrated"])},
                {"name": "run_hedge", "answer": schedule_list(rivals["run_hedge"])},
                {"name": "run_cutoff", "answer": schedule_list(rivals["run_cutoff"])},
            ],
            "perturbations": [{"input": r["input"], "answer": r["answer"]} for r in forcing_rows],
        },
        "factorial": {
            "golden_answer": schedule_list(gold_res),
            "reflex_route": {"answer": schedule_list(reflex)},
            "judgments": [
                {
                    "id": "S1",
                    "name": "4-mode regional-stripped hourly feeder innovation correlation R_ij into correlated quadrature",
                    "kind": "stump",
                    "precedent": ["L22", "L24", "L58"],
                    "dropped": {
                        "answer": schedule_list(lat_res["S1"]),
                        "results_moved": ["R2", "R5", "R6", "R7", "R8"],
                    },
                    "alone": {
                        "answer": schedule_list(lat_res["S2+S3"]),
                        "results_rescued": ["R2"],
                    },
                },
                {
                    "id": "S2",
                    "name": "coupled 4-corridor 66 kV radial impedance inversion including upstream modernized hubs anchored against monthly net kVARh",
                    "kind": "stump",
                    "precedent": ["L16", "L43", "L44", "L48"],
                    "dropped": {
                        "answer": schedule_list(lat_res["S2"]),
                        "results_moved": ["R3", "R5", "R6", "R7", "R8"],
                    },
                    "alone": {
                        "answer": schedule_list(lat_res["S1+S3"]),
                        "results_rescued": ["R3"],
                    },
                },
                {
                    "id": "S3",
                    "name": "multi-class 3-phase LV bus voltage-sag regression with AMI-metered class reactive impedance ratios",
                    "kind": "stump",
                    "precedent": ["L28", "L56", "L57"],
                    "dropped": {
                        "answer": schedule_list(lat_res["S3"]),
                        "results_moved": ["R4", "R5", "R6", "R7", "R8"],
                    },
                    "alone": {
                        "answer": schedule_list(lat_res["S1+S2"]),
                        "results_rescued": ["R4"],
                    },
                },
                {
                    "id": "J4",
                    "name": "Layer 1 extract conformance (superseded extract_ts, DST/date parsing, crosswalk, units)",
                    "kind": "reflex",
                    "precedent": ["R01", "R13"],
                },
                {
                    "id": "J5",
                    "name": "file triage and distractor exclusion",
                    "kind": "reflex",
                    "precedent": ["R02"],
                },
                {
                    "id": "J6",
                    "name": "NS-2026 planning threshold assignment (85% / 100%, 3x limiting phase)",
                    "kind": "reflex",
                    "precedent": ["R18"],
                },
            ],
        },
    }
    return pack_world, fig, E, spec


if __name__ == "__main__":
    target_dir = os.path.join(os.path.dirname(HERE), "target")
    _, fig, E, spec = run(target_dir)
    corelib.run(spec)
    json.dump(fig, open(os.path.join(HERE, "figures.json"), "w"), indent=1, sort_keys=True, default=float)
    json.dump(E, open(os.path.join(HERE, "effort.json"), "w"), indent=1, sort_keys=True, default=float)
    print("Wrote figures.json and effort.json")
