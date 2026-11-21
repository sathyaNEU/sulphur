"""Compute every owed figure strictly from the cut pack under target/, re-prove corelib.run(spec) on the
shipped files, and emit figures.json and effort.json.

    python3 task26/generator/results.py
"""
import itertools
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

    # Also build corelib spec on the cut pack (for target truth verification, compare against pack_world +
    # simulator truth only inside corelib's 'truth' check; all estimated quantities come 100% from pack_world!)
    sim_world = C.simulate()
    for s in TARGETS:
        pack_world["subs"][s]["truth"] = sim_world["subs"][s]["truth"]

    # Run corelib on pack_world
    spec, _w, gold_res, lat_res, dir_res, rig_res, ref_p = C.build_spec(pack_world)
    code = corelib.run(spec)
    assert code == 0, "corelib failed on cut pack!"

    fam_res = [(name, opts, C.evaluate(pack_world, opts)[0]) for name, opts in C.FAMILY]
    fam_only = [r for _, _, r in fam_res]

    # Quick pass: raw uncleaned SCADA CSV without deduplication, net_kvarh, balanced 33.3%
    raw_world, _ = A.load_pack(target_dir, include_superseded=True, interpolate_nulls=True)
    for s in TARGETS:
        raw_world["subs"][s]["truth"] = sim_world["subs"][s]["truth"]
    quick_res, _ = C.evaluate(raw_world, C.DIRECT)
    quick_p60_sum = round(sum(float(raw_world["subs"][s]["sub_p60"].max()) for s in TARGETS), 2)

    # Clean R1 SCADA 60-min peak sum
    r1_p60_by_sub = {s: round(float(pack_world["subs"][s]["sub_p60"].max()), 2) for s in TARGETS}
    r1_p60_sum = round(sum(float(pack_world["subs"][s]["sub_p60"].max()) for s in TARGETS), 2)

    # Verify phase-ID accuracy on the 144 field-traced reference laterals
    ref_tracer_matched = 0
    ref_tracer_total = 0
    gis_tracer_matched = 0
    for r in REFS:
        sd = pack_world["subs"][r]
        probs = C._identify_phases(sd, {})
        pred = np.argmax(probs, axis=1)
        ref_tracer_matched += int((pred == sd["lat_true_ph"]).sum())
        gis_tracer_matched += int((sd["lat_gis_ph"] == sd["lat_true_ph"]).sum())
        ref_tracer_total += len(sd["lat_true_ph"])

    # Compute exact bands from the 21-variant battery
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

    # Extra rivals for referee & routes table
    flat_res, _ = C.evaluate(pack_world, {"s1_mode": "flat_ratio"})
    rawdv_res, _ = C.evaluate(pack_world, {"s2_mode": "raw_dv_no_demean"})
    cf_zone_res, _ = C.evaluate(pack_world, {"s1_mode": "cf_zone"})
    cf_pooled_res, _ = C.evaluate(pack_world, {"s1_mode": "cf_pooled"})
    lin_sum_res, _ = C.evaluate(pack_world, {"s1_mode": "linear_sum"})

    def _ref_mae(res):
        return float(np.mean([abs(res[r]["loading_pct"] - pack_world["subs"][r]["truth"]["loading_pct"]) for r in REFS]))

    ref_mae = {
        "golden": round(_ref_mae(gold_res), 2),
        "direct": round(_ref_mae(dir_res), 2),
        "rigorous": round(_ref_mae(rig_res), 2),
        "s1_scada60": round(_ref_mae(lat_res["S1"]), 2),
        "s1_flat_ratio": round(_ref_mae(flat_res), 2),
        "s1_cf_zone": round(_ref_mae(cf_zone_res), 2),
        "s1_cf_pooled": round(_ref_mae(cf_pooled_res), 2),
        "s1_linear_sum": round(_ref_mae(lin_sum_res), 2),
        "s2_net_kvarh": round(_ref_mae(lat_res["S2"]), 2),
        "s2_raw_dv_no_demean": round(_ref_mae(rawdv_res), 2),
        "s3_gis_phase": round(_ref_mae(lat_res["S3"]), 2),
    }

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

    # Build per-substation golden table
    subs_out = {}
    for s in ALL_SUBS:
        sd = pack_world["subs"][s]
        g = gold_res[s]
        firm = float(sd["cfg"]["firm_mva"])
        subs_out[s] = dict(
            in_pool=(s in TARGETS),
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
            phase=phase_label(g["loading_pct"]) if s in TARGETS else "Modernized (Excluded)",
        )
        if s in REFS:
            t = sd["truth"]
            subs_out[s]["truth_p15_mw"] = round(t["p15_peak"], 2)
            subs_out[s]["truth_q_peak_mvar"] = round(t["q_peak_h"], 2)
            subs_out[s]["truth_w_max_pct"] = round(100.0 * t["w_max"], 2)
            subs_out[s]["truth_lim_mva"] = round(t["lim_mva"], 2)
            subs_out[s]["truth_loading_pct"] = round(t["loading_pct"], 2)
            subs_out[s]["truth_loading_pct_1dp"] = round(t["loading_pct"], 1)
            subs_out[s]["abs_loading_err_pp"] = round(abs(g["loading_pct"] - t["loading_pct"]), 2)

    # All routes summary
    all_routes = {
        "golden": gold_res,
        "S1": lat_res["S1"],
        "S2": lat_res["S2"],
        "S3": lat_res["S3"],
        "S1+S2": lat_res["S1+S2"],
        "S1+S3": lat_res["S1+S3"],
        "S2+S3": lat_res["S2+S3"],
        "S1+S2+S3": lat_res["S1+S2+S3"],
        "direct": dir_res,
        "rigorous": rig_res,
        "s1_flat_ratio": flat_res,
        "s1_cf_zone": cf_zone_res,
        "s1_cf_pooled": cf_pooled_res,
        "s1_linear_sum": lin_sum_res,
        "s2_raw_dv_no_demean": rawdv_res,
    }
    routes_out = {}
    for rname, rres in all_routes.items():
        rc1, rc2, rc3 = C._agg_components(rres)
        routes_out[rname] = dict(
            answer=schedule_list(rres),
            c1_total_p15_mw=round(rc1, 2),
            c2_total_qpeak_mvar=round(rc2, 2),
            c3_mean_lim_phase_pct=round(rc3, 2),
            total_relief_mva=round(sum(rres[s]["relief_mva"] for s in TARGETS), 2),
            loading_pct={s: round(rres[s]["loading_pct"], 2) for s in TARGETS},
            lim_mva={s: round(rres[s]["lim_mva"], 2) for s in TARGETS},
            ref_mae_pp=round(_ref_mae(rres), 2),
        )

    # Variants summary
    variants_out = []
    for vname, vopts, vres in fam_res:
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

    # Corelib rubric pricing on cut pack
    rubric = corelib.score_spec(spec) if hasattr(corelib, "score_spec") else {}

    # Top-level figure keys directly tied by effort.json (R1..R8)
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
        as_of="2027-01-20",
        seed=C.SEED,
        targets=list(TARGETS),
        refs=list(REFS),
        planning_lines=dict(
            phase2_pct=C.LINE_P2, phase1_pct=C.LINE_P1, limiting_factor=3, tap_step_pct=1.25,
            isp_minutes=15, hours_per_year=C.N_HOURS, tap_step_frac=C.TAP_STEP,
            v_nom_lv_kv=C.V_NOM_LV, v_nom_hv_kv=C.V_NOM_HV, v_lat_nom_v=230.0,
            kw_per_mw=1000, min_bus_slope=0.1, relief_ceiling_frac=0.85, year=2026,
        ),
        pack_stats=dict(
            raw_scada_rows=stats["raw_scada_rows"],
            clean_scada_rows=C.N_HOURS * len(ALL_SUBS),
            superseded_dropped=stats["superseded_dropped"],
            vlv_nulls=stats["vlv_nulls"],
            n_feeders=sum(len(pack_world["subs"][s]["f_meta"]) for s in ALL_SUBS),
            n_laterals_per_sub=C.N_LATERALS,
            n_laterals_total=C.N_LATERALS * len(ALL_SUBS),
            n_variants=len(C.FAMILY),
        ),
        ref_params=dict(
            rho_park=round(ref_p["rho_park"], 4),
            rho_indep=round(ref_p["rho_indep"], 4),
            k_ord=round(ref_p["k_ord"], 4),
            dq_dp=round(ref_p["dq_dp"], 4),
            flat_ratio=round(ref_p["flat_ratio"], 4),
            cf_park=round(ref_p["cf_park"], 4),
            cf_nonpark=round(ref_p["cf_nonpark"], 4),
            cf_pooled=round(ref_p["cf_pooled"], 4),
            tracer_matched=ref_tracer_matched,
            tracer_total=ref_tracer_total,
            gis_tracer_matched=gis_tracer_matched,
            gis_tracer_pct=round(100.0 * gis_tracer_matched / ref_tracer_total, 1),
        ),
        ref_mae=ref_mae,
        ref_ratios={k: round(v / ref_mae["golden"], 1) for k, v in ref_mae.items() if k != "golden"},
        # R1..R8 top-level keys tied to effort.json
        r1_p60_sum_mw=r1_p60_sum,
        r1_p60_by_sub=r1_p60_by_sub,
        c1_total_p15_mw=round(g_c1, 2),
        c1_band=c1_band,
        c2_total_qpeak_mvar=round(g_c2, 2),
        c2_band=c2_band,
        c3_mean_lim_phase_pct=round(g_c3, 2),
        c3_band=c3_band,
        r5_ref_mae_pp=ref_mae["golden"],
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
        rubric=rubric,
    )

    # Helper to construct R6/R7 dict values for any route
    def _r6_val(res):
        return {s: round(res[s]["loading_pct"], 2) for s in TARGETS}

    def _r7_val(res):
        d = {f"MVA_{s}": round(res[s]["lim_mva"], 2) for s in TARGETS}
        d["Total_Relief_MVA"] = round(sum(res[s]["relief_mva"] for s in TARGETS), 2)
        return d

    reflex = lat_res["S1+S2+S3"]
    # Build effort.json (8 results R1..R8 matching DESIGN_NOTE.md and effort.py contract)
    E = {
        "weights": {"recommendation": 14.0, "components": 24.0, "asks": 55.0, "instruction": 7.0},
        "results": [
            {
                "id": "R1",
                "name": "conformed 2026 SCADA, feeder, meter, asset, and AMI extracts",
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
                "name": "pool 15-minute coincident active demand (MW)",
                "graded_as": "Component 1",
                "figure": "c1_total_p15_mw",
                "depends": ["R1"],
                "precedent": ["L22", "N01", "L28"],
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
                "name": "pool peak-hour reactive demand inverted from voltage drop (MVAr)",
                "graded_as": "Component 2",
                "figure": "c2_total_qpeak_mvar",
                "depends": ["R1"],
                "precedent": ["L38", "N27", "L22"],
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
                "name": "pool average peak limiting-phase share (%)",
                "graded_as": "Component 3",
                "figure": "c3_mean_lim_phase_pct",
                "depends": ["R1"],
                "precedent": ["N09", "L38", "L28"],
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
                "name": "referee validation MAE on Fossheim, Lindberg, Ostervik, and Solberg (pct pts)",
                "graded_as": "Step-by-Step",
                "figure": "r5_ref_mae_pp",
                "depends": ["R2", "R3", "R4"],
                "precedent": ["L28", "L51", "L03"],
                "golden": ref_mae["golden"],
                "band": [0.0, 3.5],
                "partly": [3.5, 5.5],
                "passes": {
                    "quick": round(_ref_mae(quick_res), 2),
                    "careful": round(_ref_mae(reflex), 2),
                    "thorough": ref_mae["golden"],
                },
            },
            {
                "id": "R6",
                "name": "Firm N-1 loading percentage by target substation",
                "graded_as": "Asks 1 to 7",
                "figure": "r6_loading_pct",
                "depends": ["R2", "R3", "R4"],
                "precedent": ["L38", "N27", "N09"],
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
                "precedent": ["L32", "L38", "N09"],
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
                "precedent": ["L22", "L38", "N09"],
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
                "sentence": "Substation SCADA archives 60-minute fixed-clock energy blocks while feeder 15-minute max-demand registers lack timestamps and aggregate in correlated quadrature.",
                "rescues": ["R2"],
            },
            {
                "sentence": "Monthly net kVARh cancels nighttime leading shunt-capacitor injection against winter-peak lagging reactive power, hiding peak inductive load until inverted from transformer voltage drop demeaned against monthly net kVARh.",
                "rescues": ["R3"],
            },
            {
                "sentence": "GIS single-phase lateral tags drifted after storm re-phasing, so each lateral's physical phase must be identified from common-mode-rejected AMI-to-bus voltage differentials.",
                "rescues": ["R4"],
            },
        ],
        "routes": [
            {"name": "golden", "answer": schedule_list(gold_res), "golden": True},
            {"name": "S1 lost alone (SCADA 60m)", "answer": schedule_list(lat_res["S1"])},
            {"name": "S2 lost alone (net kVARh PF)", "answer": schedule_list(lat_res["S2"])},
            {"name": "S3 lost alone (GIS phase tags)", "answer": schedule_list(lat_res["S3"])},
            {"name": "S1+S2 lost", "answer": schedule_list(lat_res["S1+S2"])},
            {"name": "S1+S3 lost", "answer": schedule_list(lat_res["S1+S3"])},
            {"name": "S2+S3 lost", "answer": schedule_list(lat_res["S2+S3"])},
            {"name": "reflex route (S1+S2+S3 lost)", "answer": schedule_list(reflex)},
            {"name": "direct route", "answer": schedule_list(dir_res)},
            {"name": "rigorous standard route", "answer": schedule_list(rig_res)},
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
            ],
            "perturbations": [{"input": r["input"], "answer": r["answer"]} for r in forcing_rows],
        },
        "factorial": {
            "golden_answer": schedule_list(gold_res),
            "reflex_route": {"answer": schedule_list(reflex)},
            "judgments": [
                {
                    "id": "S1",
                    "name": "correlated quadrature of feeder 15-min excesses onto 60-min SCADA peaks",
                    "kind": "stump",
                    "precedent": ["L22", "N01", "L28"],
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
                    "name": "hourly reactive power inverted from transformer HV/LV voltage drop demeaned against monthly net kVARh",
                    "kind": "stump",
                    "precedent": ["L38", "N27", "L28"],
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
                    "name": "physical lateral phase identification from common-mode-rejected AMI-to-bus voltage differentials",
                    "kind": "stump",
                    "precedent": ["N09", "L38", "L28"],
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
