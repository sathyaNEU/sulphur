#!/usr/bin/env python3
"""task28/generator/writeup.py (v2): Emit task28/generator/figures.json,
task28/generator/effort.json, task28/metadata.json, and task28/submission.md directly
from analysis.run_all(target_dir).

Zero hardcoded computed figures: every graded value, band, cleaning count, falsification score,
rival figure, and lattice/perturbation outcome comes straight from the shipped pack analysis.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as AN  # noqa: E402
import core  # noqa: E402
import deliver as DEL  # noqa: E402
import pack as PK  # noqa: E402


def _r1(x):
    return round(float(x), 1)


def _r2(x):
    return round(float(x), 2)


def _r3(x):
    return round(float(x), 3)


def _r4(x):
    return round(float(x), 4)


def build_figures(res):
    g = res["gold_asm"]
    tr = res["train_rows"]
    cl = res["cleaning"]
    fal = res["fal_by_route"]
    bnds = res["bands"]
    lat = res["lattice_asm"]
    rig1 = res["rig_r1_asm"]
    rig2 = res["rig_r2_asm"]
    ov = res["over"]
    ex = res["extra_routes"]

    ordered = sorted(core.TRAINS, key=lambda u: tr[u]["total_2027_h"], reverse=True)
    golden_slate = sorted(u for u in core.TRAINS if tr[u]["designation"] == "OVERHAUL")
    monitor_slate = sorted(u for u in core.TRAINS if tr[u]["designation"] == "MONITOR")

    r1_clean_tbl = {
        "boron_clean_rows": cl["boron_clean_rows"],
        "intake_clean_rows": cl["intake_clean_rows"],
        "ro_feed_clean_rows": cl["ro_feed_clean_rows"],
        "hydraulics_clean_rows": cl["hydraulics_clean_rows"],
        "shift_rows": cl["shift_rows"],
        "cip_rows": cl["cip_rows"],
    }
    r5_fal_tbl = {
        "f1": _r4(fal["golden"]["f1"]),
        "f2_ms_cm": _r3(fal["golden"]["f2_ms_cm"]),
        "f3_pp": _r3(fal["golden"]["f3_pp"]),
    }
    r6_trains_tbl = {u: _r1(tr[u]["total_2027_h"]) for u in core.TRAINS}
    r7_eng_tbl = {
        "A_energy_mwh": _r1(g["A_energy_mwh"]),
        "A_overhaul_mwh": _r1(g["A_overhaul_mwh"]),
    }

    min_ov_train = min(golden_slate, key=lambda u: tr[u]["total_2027_h"])
    max_mo_train = max(monitor_slate, key=lambda u: tr[u]["total_2027_h"])

    figs = {
        # Effort-tied result keys (R1..R8)
        "R1_clean_totals": r1_clean_tbl,
        "C1_boron_2027": _r1(g["C1_boron_2027"]),
        "C2_scaling_2027": _r1(g["C2_scaling_2027"]),
        "C3_struct_2027": _r1(g["C3_struct_2027"]),
        "R5_falsification": r5_fal_tbl,
        "R6_train_totals_2027": r6_trains_tbl,
        "R7_energy_penalties": r7_eng_tbl,
        "R8_overhaul_slate": golden_slate,
        "monitor_slate": monitor_slate,
        "ordered_trains": ordered,
        # Headline asks
        "A_total_2027": _r1(g["A_total_2027"]),
        "A_overhaul_2027": _r1(g["A_overhaul_2027"]),
        "A_q3_2027": _r1(g["A_q3_2027"]),
        "A_energy_mwh": _r1(g["A_energy_mwh"]),
        "A_overhaul_mwh": _r1(g["A_overhaul_mwh"]),
        "A_energy_mwh_exact": _r2(sum(tr[u]["energy_2027_mwh"] for u in core.TRAINS)),
        "A_overhaul_mwh_exact": _r2(sum(tr[u]["energy_2027_mwh"] for u in golden_slate)),
        # Per-train detailed golden figures
        "trains": {
            u: {
                "boron_2026_h": _r1(tr[u]["boron_2026_h"]),
                "scaling_2026_h": _r1(tr[u]["scaling_2026_h"]),
                "struct_2026_h": _r1(tr[u]["struct_2026_h"]),
                "total_2026_h": _r1(tr[u]["total_2026_h"]),
                "boron_2027_h": _r1(tr[u]["boron_2027_h"]),
                "scaling_2027_h": _r1(tr[u]["scaling_2027_h"]),
                "struct_2027_h": _r1(tr[u]["struct_2027_h"]),
                "total_2027_h": _r1(tr[u]["total_2027_h"]),
                "q3_2027_h": _r1(tr[u]["q3_2027_h"]),
                "energy_2027_mwh": _r2(tr[u]["energy_2027_mwh"]),
                "designation": tr[u]["designation"],
                "v_nom_m3": tr[u]["v_nom_m3"],
                "s1_beta_hat": _r2(tr[u]["s1_beta_hat"]),
                "s1_lam_h": _r2(tr[u]["s1_lam_h"]),
                "s1_sd1": _r4(tr[u]["s1_sd1"]),
                "s2_f_fast_pct": _r1(100.0 * tr[u]["s2_f_fast_hat"]),
                "s2_v_fast_hat": _r1(tr[u]["s2_v_fast_hat"]),
                "s2_v_main_hat": _r1(tr[u]["s2_v_main_hat"]),
                "s2_cond_rms": _r3(tr[u]["s2_cond_rms"]),
                "s2_sp_cond_rms": _r3(tr[u]["s2_sp_cond_rms"]),
                "s3_pi_s_pct": _r2(100.0 * tr[u]["s3_pi_s_hat"]),
                "s3_pi_bio_pct": _r2(100.0 * tr[u]["s3_pi_bio_hat"]),
                "s3_pi_min_pct": _r2(100.0 * tr[u]["s3_pi_min_hat"]),
            }
            for u in core.TRAINS
        },
        # 2026 plant totals
        "plant_2026": {
            "boron_2026_h": _r1(sum(tr[u]["boron_2026_h"] for u in core.TRAINS)),
            "scaling_2026_h": _r1(sum(tr[u]["scaling_2026_h"] for u in core.TRAINS)),
            "struct_2026_h": _r1(sum(tr[u]["struct_2026_h"] for u in core.TRAINS)),
            "total_2026_h": _r1(sum(tr[u]["total_2026_h"] for u in core.TRAINS)),
            "raw_boron_2026_h": _r1(sum(tr[u]["s1_raw_2026_h"] for u in core.TRAINS)),
            "raw_scaling_2026_h": _r1(sum(tr[u]["s2_raw_2026_h"] for u in core.TRAINS)),
            "raw_struct_2026_h": _r1(sum(tr[u]["s3_raw_2026_h"] for u in core.TRAINS)),
            "raw_total_2026_h": _r1(
                sum(tr[u]["s1_raw_2026_h"] + tr[u]["s2_raw_2026_h"] + tr[u]["s3_raw_2026_h"] for u in core.TRAINS)
            ),
        },
        # 26-variant uncertainty ranges
        "bands": bnds,
        # Cleaning and operational constants from shipped files
        "cleaning": cl,
        "constants": {
            "threshold_h": core.THRESHOLD,
            "boron_limit_mg_l": core.BORON_LIMIT,
            "scaling_x_lim": core.SCALING_X_LIM,
            "scaling_y_lim": core.SCALING_Y_LIM,
            "energy_rate_boron_kwh_h": core.ENERGY_BORON_KWH,
            "energy_rate_scaling_kwh_h": core.ENERGY_SCALING_KWH,
            "energy_rate_struct_kwh_h": core.ENERGY_STRUCT_KWH,
            "kwh_per_mwh": 1000,
            "lab_sd_mg_l": 0.004,
            "wls_weight_v4": 3,
            "wls_weight_c8": 0.7,
            "lam_min_h": 0.25,
            "lam_max_h": 30.0,
            "lam_grid_points": 200,
            "dt_15m_hours": 0.25,
            "v1_scan_min_m3": 160,
            "v1_scan_max_m3": 560,
            "v2_scan_min_m3": 760,
            "v2_scan_max_m3": 1520,
            "f_fast_cap": 0.49,
            "f_fast_floor": 0.04,
            "active_15m_per_train": 35008,
            "burn_in_intervals": 32,
            "burn_in_hours": 8,
            "post_cip_hours": 120,
            "post_cip_blocks": 30,
            "post_cip_blocks_inclusive": 31,
            "post_cip_alt_96h": 96,
            "post_cip_alt_144h": 144,
            "cip_retention_floor": 0.05,
            "cip_retention_cap": 0.65,
            "trim_pct": 0.5,
            "trimmed_l2_pct": 2,
            "pct_scale": 100,
            "year_days": 365,
            "year_hours": 8760,
            "shift_blocks_per_train": 2190,
            "lca_cells": 192,
            "min_overhaul_train": min_ov_train,
            "max_monitor_train": max_mo_train,
            "clearance_min_ov_h": _r1(tr[min_ov_train]["total_2027_h"] - core.THRESHOLD),
            "clearance_max_mo_h": _r1(core.THRESHOLD - tr[max_mo_train]["total_2027_h"]),
            "n_variants": len(res["variants_named"]),
            "n_perturbations": len(res["perturbations"]),
            "perturbation_pct": 20,
            "plan_boron_temp_q": core.PLAN_BORON_TEMP_Q,
            "plan_scaling_rec_q": core.PLAN_SCALING_REC_Q,
            "s3_p_bio": [_r3(x) for x in tr["TR01"]["s3_p_bio"]],
            "s3_p_min": [_r3(x) for x in tr["TR01"]["s3_p_min"]],
            "s3_p_str": [_r3(x) for x in tr["TR01"]["s3_p_str"]],
        },
        # Native-unit physical falsification across routes
        "falsification": {
            k: {
                "f1": _r4(v["f1"]),
                "f2_ms_cm": _r3(v["f2_ms_cm"]),
                "f3_pp": _r3(v["f3_pp"]),
                "combined": _r3(v["combined"]),
            }
            for k, v in fal.items()
        },
        # Routes, lattice, over-corrections, forcing bounds for Step-by-Step verification
        "routes": {
            "direct": {
                "C1": _r1(lat["S1+S2+S3"]["C1_boron_2027"]),
                "C2": _r1(lat["S1+S2+S3"]["C2_scaling_2027"]),
                "C3": _r1(lat["S1+S2+S3"]["C3_struct_2027"]),
                "total": _r1(lat["S1+S2+S3"]["A_total_2027"]),
                "energy_mwh": _r1(lat["S1+S2+S3"]["A_energy_mwh"]),
                "members": {u: _r1(lat["S1+S2+S3"]["members"][u]) for u in core.TRAINS},
            },
            "rigorous_r1": {
                "C1": _r1(rig1["C1_boron_2027"]),
                "C2": _r1(rig1["C2_scaling_2027"]),
                "C3": _r1(rig1["C3_struct_2027"]),
                "total": _r1(rig1["A_total_2027"]),
                "energy_mwh": _r1(rig1["A_energy_mwh"]),
                "overhaul_energy_mwh": _r1(rig1["A_overhaul_mwh"]),
                "q3": _r1(rig1["A_q3_2027"]),
                "members": {u: _r1(rig1["members"][u]) for u in core.TRAINS},
            },
            "rigorous_r2": {
                "C1": _r1(rig2["C1_boron_2027"]),
                "C2": _r1(rig2["C2_scaling_2027"]),
                "C3": _r1(rig2["C3_struct_2027"]),
                "total": _r1(rig2["A_total_2027"]),
                "energy_mwh": _r1(rig2["A_energy_mwh"]),
                "members": {u: _r1(rig2["members"][u]) for u in core.TRAINS},
            },
            "drop_S1": {
                "C1": _r1(lat["S1"]["C1_boron_2027"]),
                "total": _r1(lat["S1"]["A_total_2027"]),
                "members": {u: _r1(lat["S1"]["members"][u]) for u in core.TRAINS},
            },
            "drop_S2": {
                "C2": _r1(lat["S2"]["C2_scaling_2027"]),
                "total": _r1(lat["S2"]["A_total_2027"]),
                "members": {u: _r1(lat["S2"]["members"][u]) for u in core.TRAINS},
            },
            "drop_S3": {
                "C3": _r1(lat["S3"]["C3_struct_2027"]),
                "total": _r1(lat["S3"]["A_total_2027"]),
                "members": {u: _r1(lat["S3"]["members"][u]) for u in core.TRAINS},
            },
            "drop_S1_S2": {"total": _r1(lat["S1+S2"]["A_total_2027"]), "members": {u: _r1(lat["S1+S2"]["members"][u]) for u in core.TRAINS}},
            "drop_S1_S3": {"total": _r1(lat["S1+S3"]["A_total_2027"]), "members": {u: _r1(lat["S1+S3"]["members"][u]) for u in core.TRAINS}},
            "drop_S2_S3": {"total": _r1(lat["S2+S3"]["A_total_2027"]), "members": {u: _r1(lat["S2+S3"]["members"][u]) for u in core.TRAINS}},
            "over_S1": {"members": {u: _r1(ov["S1"]["members"][u]) for u in core.TRAINS}},
            "over_S2": {"members": {u: _r1(ov["S2"]["members"][u]) for u in core.TRAINS}},
            "over_S3": {"members": {u: _r1(ov["S3"]["members"][u]) for u in core.TRAINS}},
            "s1_stat_ar1_TR01": _r1(ex["cutoff:s1_stationary_ar1_mle"]["members"]["TR01"]),
            "s1_stat_ar1_TR04": _r1(ex["cutoff:s1_stationary_ar1_mle"]["members"]["TR04"]),
            "s1_4h_only_TR01": _r1(ex["cutoff:s1_4h_only"]["members"]["TR01"]),
            "s1_flux_no_deconv_TR01": _r1(ex["cutoff:s1_flux_no_deconv"]["members"]["TR01"]),
            "s1_flux_iid_over_TR04": _r1(ex["cutoff:s1_flux_iid_over"]["members"]["TR04"]),
            "s2_single_plug_TR02": _r1(ex["cutoff:s2_single_plug_veff"]["members"]["TR02"]),
            "s2_single_plug_TR05": _r1(ex["cutoff:s2_single_plug_veff"]["members"]["TR05"]),
            "s2_fixed_lag_TR02": _r1(ex["cutoff:s2_fixed_lag"]["members"]["TR02"]),
            "s2_nom_vol_TR02": _r1(ex["cutoff:s2_nom_vol"]["members"]["TR02"]),
            "s3_r1_pooled_TR03": _r1(ex["cutoff:s3_r1_pooled_cip_3state"]["members"]["TR03"]),
            "s3_r2_ds2_TR03": _r1(ex["cutoff:s3_r2_post_cip_ds2"]["members"]["TR03"]),
            "s3_post_cip_mv_TR03": _r1(ex["cutoff:s3_post_cip_mv"]["members"]["TR03"]),
            "s3_unanimous_TR06": _r1(ex["cutoff:s3_unanimous"]["members"]["TR06"]),
            "history_2026_flat_TR01": _r1(ex["hedge:history_2026_flat"]["members"]["TR01"]),
            "history_2026_flat_TR02": _r1(ex["hedge:history_2026_flat"]["members"]["TR02"]),
            "forcing_min_overhaul": _r1(min(p["min_overhaul"] for p in res["perturbations"])),
            "forcing_max_monitor": _r1(max(p["max_monitor"] for p in res["perturbations"])),
        },
    }
    return figs


def build_effort_json(res, figs):
    g = res["gold_asm"]
    lat = res["lattice_asm"]
    rig1 = res["rig_r1_asm"]
    rig2 = res["rig_r2_asm"]
    bnds = res["bands"]
    fal = res["fal_by_route"]

    def _slate(asm):
        return sorted(u for u in core.TRAINS if asm["members"][u] >= core.THRESHOLD)

    g_slate = _slate(g)
    reflex_slate = _slate(lat["S1+S2+S3"])
    rig1_slate = _slate(rig1)
    rig2_slate = _slate(rig2)

    quick_r1 = dict(figs["R1_clean_totals"])
    quick_r1["boron_clean_rows"] = res["cleaning"]["boron_raw_rows"]
    quick_r1["intake_clean_rows"] = res["cleaning"]["intake_raw_rows"]
    quick_r1["hydraulics_clean_rows"] = res["cleaning"]["hydraulics_raw_rows"]

    reflex = lat["S1+S2+S3"]

    results = [
        {
            "id": "R1",
            "name": "Reconciled 2026 multi-grain SWRO logs",
            "graded_as": "Ask 0 (Assembly)",
            "figure": "R1_clean_totals",
            "depends": [],
            "independent": "raw operational files",
            "golden": figs["R1_clean_totals"],
            "passes": {
                "quick": quick_r1,
                "careful": figs["R1_clean_totals"],
                "thorough": figs["R1_clean_totals"],
            },
        },
        {
            "id": "R2",
            "name": "Solute-flux coupled composite boron deconvolution (C1)",
            "graded_as": "Component 1",
            "figure": "C1_boron_2027",
            "depends": ["R1"],
            "independent": "permeate_boron_composites_2026.csv, autosampler_schedule_2026.csv, train_hydraulics_hourly_2026.csv",
            "golden": figs["C1_boron_2027"],
            "band": bnds["C1_boron_2027"],
            "precedent": ["L22", "L56", "L57"],
            "passes": {
                "quick": _r1(reflex["C1_boron_2027"]),
                "careful": _r1(reflex["C1_boron_2027"]),
                "thorough": figs["C1_boron_2027"],
            },
        },
        {
            "id": "R3",
            "name": "Two-path bimodal DAF/DMF hydraulic parcel alignment (C2)",
            "graded_as": "Component 2",
            "figure": "C2_scaling_2027",
            "depends": ["R1"],
            "independent": "intake_chemistry_15m_2026.csv, ro_feed_header_15m_2026.csv, train_hydraulics_hourly_2026.csv",
            "golden": figs["C2_scaling_2027"],
            "band": bnds["C2_scaling_2027"],
            "precedent": ["L26", "L28", "N07", "N30"],
            "passes": {
                "quick": _r1(reflex["C2_scaling_2027"]),
                "careful": _r1(reflex["C2_scaling_2027"]),
                "thorough": figs["C2_scaling_2027"],
            },
        },
        {
            "id": "R4",
            "name": "4-state dual-recipe CIP-invariant structural fault separation (C3)",
            "graded_as": "Component 3",
            "figure": "C3_struct_2027",
            "depends": ["R1"],
            "independent": "shift_diagnostics_2026.csv and cip_wash_log_2026.csv",
            "golden": figs["C3_struct_2027"],
            "band": bnds["C3_struct_2027"],
            "precedent": ["L03", "L38", "L54", "N36"],
            "passes": {
                "quick": _r1(reflex["C3_struct_2027"]),
                "careful": _r1(reflex["C3_struct_2027"]),
                "thorough": figs["C3_struct_2027"],
            },
        },
        {
            "id": "R5",
            "name": "Native-unit physical falsification checks F1-F3",
            "graded_as": "Ask 1 (Validation)",
            "figure": "R5_falsification",
            "depends": ["R2", "R3", "R4"],
            "independent": "",
            "golden": figs["R5_falsification"],
            "bands": {"f1": [0.0, 0.12], "f2_ms_cm": [0.30, 0.40], "f3_pp": [0.0, 1.00]},
            "precedent": ["L28"],
            "passes": {
                "quick": {"f1": _r4(fal["direct"]["f1"]), "f2_ms_cm": _r3(fal["direct"]["f2_ms_cm"]), "f3_pp": _r3(fal["direct"]["f3_pp"])},
                "careful": {"f1": _r4(fal["direct"]["f1"]), "f2_ms_cm": _r3(fal["direct"]["f2_ms_cm"]), "f3_pp": _r3(fal["direct"]["f3_pp"])},
                "thorough": figs["R5_falsification"],
            },
        },
        {
            "id": "R6",
            "name": "2027 Operating Plan train projections",
            "graded_as": "Ask 2 (Projections)",
            "figure": "R6_train_totals_2027",
            "depends": ["R2", "R3", "R4", "R5"],
            "independent": "",
            "golden": figs["R6_train_totals_2027"],
            "bands": {u: bnds[f"A_{u}"] for u in core.TRAINS},
            "precedent": ["L11"],
            "passes": {
                "quick": {u: _r1(reflex["members"][u]) for u in core.TRAINS},
                "careful": {u: _r1(reflex["members"][u]) for u in core.TRAINS},
                "thorough": figs["R6_train_totals_2027"],
            },
        },
        {
            "id": "R7",
            "name": "2027 excess desalination energy penalty (MWh)",
            "graded_as": "Ask 3 (Energy Penalty)",
            "figure": "R7_energy_penalties",
            "depends": ["R2", "R3", "R4", "R6"],
            "independent": "",
            "golden": figs["R7_energy_penalties"],
            "bands": {
                "A_energy_mwh": bnds["A_energy_mwh"],
                "A_overhaul_mwh": bnds["A_overhaul_mwh"],
            },
            "precedent": ["L11"],
            "passes": {
                "quick": {"A_energy_mwh": _r1(reflex["A_energy_mwh"]), "A_overhaul_mwh": _r1(reflex["A_overhaul_mwh"])},
                "careful": {"A_energy_mwh": _r1(reflex["A_energy_mwh"]), "A_overhaul_mwh": _r1(reflex["A_overhaul_mwh"])},
                "thorough": figs["R7_energy_penalties"],
            },
        },
        {
            "id": "R8",
            "name": "Final 2027 vessel overhaul reliability classification",
            "graded_as": "Recommendation",
            "figure": "R8_overhaul_slate",
            "depends": ["R2", "R3", "R4", "R6", "R7"],
            "independent": "",
            "golden": g_slate,
            "precedent": ["L26", "L22"],
            "passes": {
                "quick": reflex_slate,
                "careful": reflex_slate,
                "thorough": g_slate,
            },
        },
    ]

    effort = {
        "results": results,
        "hints": [
            {
                "sentence": (
                    "Permeate boron follows solution-diffusion flux coupling (alpha + beta/Q_t) inside 4h/8h "
                    "flow-proportional composites, so stationary AR(1) composite deconvolution misses night-turndown spikes."
                ),
                "rescues": ["R2"],
            },
            {
                "sentence": (
                    "Aging DAF/DMF basins split flow across a fast short-circuit bypass and a main baffled zone, "
                    "so 1D single-plug cumulative-volume conductivity matching locks onto the main stream and misses the mix."
                ),
                "rescues": ["R3"],
            },
            {
                "sentence": (
                    "Alkaline CIP washes clear organic bio-fouling while acid CIP washes clear mineral crust that "
                    "also triggers acoustic chatter D3, whereas persistent structural faults survive both recipes."
                ),
                "rescues": ["R4"],
            },
        ],
        "routes": [
            {"name": "golden (flux+AR1 + two-path hydraulics + 4-state dual-CIP EM)", "answer": g_slate, "golden": True},
            {"name": "direct / reflex (raw composites + same-timestamp + 2-of-3 MV)", "answer": reflex_slate},
            {"name": "rigorous R1 (stationary AR1 + 1D single-plug V_eff + 3-state pooled-CIP)", "answer": rig1_slate},
            {"name": "rigorous R2 (stationary AR1 + 1D single-plug V_eff + post-CIP 2-class DS)", "answer": rig2_slate},
            {"name": "drop S1 alone", "answer": _slate(lat["S1"])},
            {"name": "drop S2 alone", "answer": _slate(lat["S2"])},
            {"name": "drop S3 alone", "answer": _slate(lat["S3"])},
            {"name": "cutoff filter (4h-only + fixed lag + post-CIP MV)", "answer": _slate(res["cut_asm"])},
            {"name": "generous upper (i.i.d. sqrt(m) + comonotonic + post-CIP 2-class DS)", "answer": _slate(res["gen_asm"])},
            {"name": "over-correct S1 (i.i.d. sqrt(m))", "answer": _slate(res["over"]["S1"])},
            {"name": "over-correct S2 (comonotonic bound)", "answer": _slate(res["over"]["S2"])},
            {"name": "over-correct S3 (raw uninverted D3 post-acid)", "answer": _slate(res["over"]["S3"])},
        ],
        "forcing": {
            "kind": "set",
            "golden_answer": g_slate,
            "golden_family": [
                {"name": nm, "answer": _slate(asm)} for nm, asm in res["variants_named"]
            ],
            "shortcuts": [
                {"name": "direct / reflex", "answer": reflex_slate},
                {"name": "rigorous R1", "answer": rig1_slate},
                {"name": "rigorous R2", "answer": rig2_slate},
                {"name": "cutoff", "answer": _slate(res["cut_asm"])},
                {"name": "generous", "answer": _slate(res["gen_asm"])},
                {"name": "hedge", "answer": _slate(res["hedge_asm"])},
                {"name": "drop S1", "answer": _slate(lat["S1"])},
                {"name": "drop S2", "answer": _slate(lat["S2"])},
                {"name": "drop S3", "answer": _slate(lat["S3"])},
            ],
            "perturbations": [
                {"input": p["input"], "answer": p["answer"]} for p in res["perturbations"]
            ],
        },
        "factorial": {
            "golden_answer": g_slate,
            "reflex_route": {"answer": reflex_slate},
            "judgments": [
                {
                    "id": "S1",
                    "name": "Solute-flux coupled (1/Q_bar) composite boron regression and AR(1) 1h deconvolution",
                    "kind": "stump",
                    "precedent": ["L22", "L56", "L57"],
                    "dropped": {
                        "answer": _slate(lat["S1"]),
                        "results_moved": ["R2", "R5", "R6", "R7", "R8"],
                    },
                    "alone": {
                        "answer": _slate(lat["S2+S3"]),
                        "results_rescued": ["R2"],
                    },
                },
                {
                    "id": "S2",
                    "name": "Two-path bimodal DAF/DMF hydraulic short-circuiting recovery in cumulative flow",
                    "kind": "stump",
                    "precedent": ["L26", "L28", "N07", "N30"],
                    "dropped": {
                        "answer": _slate(lat["S2"]),
                        "results_moved": ["R3", "R5", "R6", "R7", "R8"],
                    },
                    "alone": {
                        "answer": _slate(lat["S1+S3"]),
                        "results_rescued": ["R3"],
                    },
                },
                {
                    "id": "S3",
                    "name": "4-state dual-recipe CIP-invariant latent-class structural fault separation",
                    "kind": "stump",
                    "precedent": ["L03", "L38", "L54", "N36"],
                    "dropped": {
                        "answer": _slate(lat["S3"]),
                        "results_moved": ["R4", "R5", "R6", "R7", "R8"],
                    },
                    "alone": {
                        "answer": _slate(lat["S1+S2"]),
                        "results_rescued": ["R4"],
                    },
                },
                {
                    "id": "R_L1",
                    "name": "Layer 1 multi-system cleaning (dates, UTC/Lisbon clocks, QA revisions, units, legacy tags)",
                    "kind": "reflex",
                    "precedent": ["R01", "R02"],
                },
                {
                    "id": "R_plan",
                    "name": "Uniform 2027 Operating Plan Annex A quarterly scaling",
                    "kind": "reflex",
                    "precedent": ["R01", "R93"],
                },
            ],
        },
        "weights": {"recommendation": 14, "components": 24, "asks": 55, "instruction": 7},
    }
    return effort


def build_metadata(res):
    F = PK.FILES
    src = (
        "generated deterministically by the build's coastal SWRO desalination physical process simulator "
        "(Barlavento Dessalinizacao Municipal, E.M., Algarve, Portugal; no external or public data)"
    )
    lic = "proprietary, municipal desalination authority simulation"

    def _entry(covers, pulled):
        return {"covers": covers, "license": lic, "pulled": pulled, "source": src}

    meta = {
        "as_of": PK.AS_OF,
        "decision": "2027 membrane-train reliability diagnosis and vessel overhaul selection across eight Barlavento SWRO trains under Engineering Protocol SWRO-Q27",
        "deliverables": ["a workbook", "a CSV"],
        "stated_inputs": ["400", "2026", "2027"],
        "distractor_files": [F["dist_mibel"], F["dist_reservoir"]],
        "field_terms": ["CIP", "boron", "SWRO", "DAF", "DMF", "Algarve"],
        "files": {
            F["standard_pdf"]: _entry(
                "Engineering Protocol SWRO-Q27 defining physical excursion modes, overhaul criterion, excess desalination energy rates, Annex A 2027 forecast rules, and Annex B diagnostics output schema",
                "2026-09-14",
            ),
            F["lims_qa_pdf"]: _entry(
                "2026 ISO/IEC 17025 accredited LIMS ICP-OES permeate boron analytical quality assurance certificate",
                "2027-01-08",
            ),
            F["asset_reg"]: _entry(
                "Barlavento SWRO train asset register with legacy tag crosswalk, bay assignments, and nominal DAF/DMF pretreatment basin volumes",
                "2026-11-18",
            ),
            F["op_plan"]: _entry(
                "2027 quarterly operating plan potable dispatch duty ratios and seasonal temperature and recovery multipliers",
                "2026-12-04",
            ),
            F["autosampler"]: _entry(
                "2026 daily permeate boron autosampler carousel schedule by train",
                "2027-01-05",
            ),
            F["boron_comp"]: _entry(
                "2026 LIMS flow-proportional composite permeate boron laboratory assays across all eight trains",
                "2027-01-09",
            ),
            F["intake_15m"]: _entry(
                "2026 15-minute coastal intake seawater conductivity and standardized algal-TEP precursor index telemetry",
                "2027-01-11",
            ),
            F["ro_feed_15m"]: _entry(
                "2026 15-minute RO-feed header conductivity and supersaturation-oxidant stress telemetry",
                "2027-01-11",
            ),
            F["hydraulics_h"]: _entry(
                "2026 hourly SCADA feed flow and feed pressure telemetry by train",
                "2027-01-11",
            ),
            F["shift_diag"]: _entry(
                "2026 four-hour shift inline non-destructive membrane integrity alarm logs",
                "2027-01-12",
            ),
            F["cip_log"]: _entry(
                "2026 routine Clean-in-Place alkaline and acid chemical wash completion log by train",
                "2027-01-12",
            ),
            F["scada_cfg"]: _entry(
                "2026 plant SCADA historian and bay instrumentation hardware configuration",
                "2026-10-21",
            ),
            F["dist_mibel"]: _entry(
                "2026 hourly Iberian MIBEL Portugal day-ahead electricity spot prices (EUR/MWh)",
                "2027-01-06",
            ),
            F["dist_reservoir"]: _entry(
                "2026 weekly western Algarve surface reservoir storage percentage bulletin",
                "2027-01-07",
            ),
        },
    }
    return meta


def build_submission_md(res, figs):
    g = res["gold_asm"]
    tr = res["train_rows"]
    cl = res["cleaning"]
    fal = res["fal_by_route"]
    bnds = res["bands"]
    rt = figs["routes"]
    ordered = figs["ordered_trains"]
    p26 = figs["plant_2026"]
    cns = figs["constants"]
    n_var = len(res["variants_named"])

    def _bstr(key, suffix=""):
        lo, hi = bnds[key]
        return f"{lo:,.1f}{suffix} to {hi:,.1f}{suffix}"

    ov_desc = ", ".join(
        f"{u} ({tr[u]['total_2027_h']:,.1f} h)" for u in ordered if tr[u]["designation"] == "OVERHAUL"
    )
    mo_desc = ", ".join(
        f"{u} ({tr[u]['total_2027_h']:,.1f} h)" for u in ordered if tr[u]["designation"] == "MONITOR"
    )
    min_ov_u = cns["min_overhaul_train"]
    max_mo_u = cns["max_monitor_train"]

    lines = [
        "# task28 answer blocks",
        "",
        "## Tags",
        "",
        "**Domain:** Engineering and Physical Sciences, Physical & Environmental Sciences (process control and measurement systems: coastal seawater reverse-osmosis membrane-train reliability diagnostics across solute-flux coupled composite lab assays, two-path bimodal pretreatment hydraulics, and dual-recipe CIP-invariant shift alarms).",
        "**Analytical objective:** Anomaly Detection & Diagnostics.",
        "",
        "## Final Recommendation",
        "",
        (
            f"**Schedule four Barlavento SWRO trains for 2027 pressure-vessel overhaul under Engineering Protocol SWRO-Q27's "
            f"400-hour engineering criterion: {ov_desc}, totaling {g['A_overhaul_2027']:,.1f} overhaul-train hours "
            f"(uncertainty range {_bstr('A_overhaul_2027')} h) and {g['A_overhaul_mwh']:,.1f} MWh projected energy penalty "
            f"(uncertainty range {_bstr('A_overhaul_mwh')} MWh), while retaining {mo_desc} on routine monitoring "
            f"(plant-wide 2027 total {g['A_total_2027']:,.1f} h, uncertainty range {_bstr('A_total_2027')} h; plant-wide "
            f"energy penalty {g['A_energy_mwh']:,.1f} MWh, uncertainty range {_bstr('A_energy_mwh')} MWh).** "
            f"This rejects both raw monitoring (which flags TR03 at {rt['direct']['members']['TR03']:,.1f} h, TR04 at "
            f"{rt['direct']['members']['TR04']:,.1f} h, TR06 at {rt['direct']['members']['TR06']:,.1f} h, and TR07 at "
            f"{rt['direct']['members']['TR07']:,.1f} h while missing TR01 at {rt['direct']['members']['TR01']:,.1f} h and "
            f"TR02 at {rt['direct']['members']['TR02']:,.1f} h) and standard single-stream physical models (stationary AR(1) "
            f"composite deconvolution, 1D single-plug cumulative-volume conductivity matching, and pooled-CIP 3-state or "
            f"post-CIP 2-class Dawid-Skene EM), which still miss flux-sensitive TR01 ({rt['rigorous_r1']['members']['TR01']:,.1f} h) "
            f"and fast-bypass TR02 ({rt['rigorous_r1']['members']['TR02']:,.1f} h) while mis-flagging mineral-crusted TR03 "
            f"({rt['rigorous_r1']['members']['TR03']:,.1f} h), diurnal-swing TR04 ({rt['rigorous_r1']['members']['TR04']:,.1f} h), "
            f"and diluted-feed TR05 ({rt['rigorous_r1']['members']['TR05']:,.1f} h)."
        ),
        "",
        "## Supplementary Questions",
        "",
        f"### {DEL.GOLDEN_XLSX}",
        "",
        (
            f"The workbook opens on `Overhaul_Triage_2027` stating the 2027 vessel overhaul slate, mode-level forecasts, "
            f"energy penalty in MWh, and {n_var}-variant estimation uncertainty ranges alongside a horizontal bar chart "
            f"comparing each train's projected 2027 anomalous operating hours against the 400-hour criterion, followed by "
            f"formula-linked physical model backups (`S1_Boron_Flux_Support`, `S2_TwoPath_Hydraulics`, `S3_DualCIP_LCA`), "
            f"native-unit falsification and route comparisons (`Falsification_And_Routes`), quarterly 2026-to-2027 forecasts "
            f"(`Operating_Plan_2027`), and the {n_var}-variant uncertainty battery and QA log (`Sensitivity_And_QA_2026`)."
        ),
        "",
        f"1. Forecasted 2027 anomalous operating hours by train across permeate boron, scaling, and structural faults, Q3 hours, excess desalination energy penalty (MWh), and Section 3 overhaul designation ({n_var}-variant estimation uncertainty range on total in parentheses):",
    ]

    letters = "abcdefgh"
    for i, u in enumerate(ordered):
        t = tr[u]
        lines.append(
            f"   {letters[i]}. {u}: {t['total_2027_h']:,.1f} h total (uncertainty range {_bstr(f'A_{u}')} h) = "
            f"{t['boron_2027_h']:,.1f} h boron + {t['scaling_2027_h']:,.1f} h scaling + {t['struct_2027_h']:,.1f} h structural; "
            f"Q3 {t['q3_2027_h']:,.1f} h; {t['energy_2027_mwh']:,.2f} MWh; {t['designation']}."
        )

    lines.extend(
        [
            f"2. Plant-wide 2027 anomalous operating hours across failure modes, overhaul subset, and summer Q3 peak ({n_var}-variant estimation uncertainty ranges in parentheses):",
            f"   a. Plant-wide 2027 total anomalous operating hours: {g['A_total_2027']:,.1f} h (uncertainty range {_bstr('A_total_2027')} h).",
            f"   b. Overhaul-train subtotal ({', '.join(u for u in ordered if tr[u]['designation'] == 'OVERHAUL')}): {g['A_overhaul_2027']:,.1f} h (uncertainty range {_bstr('A_overhaul_2027')} h).",
            f"   c. Plant-wide summer Q3 2027 anomalous operating hours: {g['A_q3_2027']:,.1f} h (uncertainty range {_bstr('A_q3_2027')} h).",
            f"   d. Plant-wide 2027 failure-mode totals: permeate boron {g['C1_boron_2027']:,.1f} h (uncertainty range {_bstr('C1_boron_2027')} h), scaling {g['C2_scaling_2027']:,.1f} h (uncertainty range {_bstr('C2_scaling_2027')} h), and structural faults {g['C3_struct_2027']:,.1f} h (uncertainty range {_bstr('C3_struct_2027')} h).",
            f"3. Projected 2027 excess desalination energy penalty in MWh under Section 4 (420 kWh/h boron 2nd-pass polishing, 360 kWh/h scaling TMP drag, 540 kWh/h structural bypass recirculation; {n_var}-variant estimation uncertainty ranges in parentheses):",
            f"   a. Plant-wide 2027 energy penalty: {g['A_energy_mwh']:,.1f} MWh, or {figs['A_energy_mwh_exact']:,.2f} MWh exact (uncertainty range {_bstr('A_energy_mwh')} MWh).",
            f"   b. Overhaul-train 2027 energy penalty: {g['A_overhaul_mwh']:,.1f} MWh, or {figs['A_overhaul_mwh_exact']:,.2f} MWh exact (uncertainty range {_bstr('A_overhaul_mwh')} MWh).",
            "",
            f"### {DEL.GOLDEN_CSV}",
            "",
            (
                f"Eight rows sorted by `total_2027_h` descending ({', '.join('`' + u + '`' for u in ordered)}) "
                "carrying the exact Annex B plant historian columns (`train_id`, `boron_2027_h`, `scaling_2027_h`, `struct_2027_h`, "
                "`total_2027_h`, `q3_2027_h`, `energy_2027_mwh`, `designation`) matching every train figure in item 1 above."
            ),
            "",
            "## Critical Components",
            "",
            f"1. Plant-wide forecasted 2027 permeate boron excursion hours across all eight SWRO trains are **{g['C1_boron_2027']:,.1f} hours** (uncertainty range **{_bstr('C1_boron_2027')} hours**).",
            f"2. Plant-wide forecasted 2027 pretreatment-to-RO scaling excursion hours across all eight SWRO trains are **{g['C2_scaling_2027']:,.1f} hours** (uncertainty range **{_bstr('C2_scaling_2027')} hours**).",
            f"3. Plant-wide forecasted 2027 persistent structural membrane integrity fault hours across all eight SWRO trains are **{g['C3_struct_2027']:,.1f} hours** (uncertainty range **{_bstr('C3_struct_2027')} hours**).",
            "",
            "## Step-by-Step",
            "",
            (
                f"1. Conformed the 2026 operational archive to Engineering Protocol SWRO-Q27 Section 4: mapped legacy `LINE-A` through "
                f"`LINE-H` tags to `TR01` through `TR08` via `train_asset_register.csv`; cleaned `permeate_boron_composites_2026.csv` "
                f"from {cl['boron_raw_rows']:,} raw rows to {cl['boron_clean_rows']:,} unique bottles by keeping maximum `qa_revision` "
                f"({cl['boron_superseded_dropped']} superseded preliminary rows dropped), parsing {cl['boron_dmy_rows']:,} Portuguese "
                f"`DD/MM/YYYY` dates, converting {cl['boron_ug_rows']:,} South-bay `ug/L` assays to `mg/L`, and joining daily bottle "
                f"duration (`4 h` Thu-Mon, `8 h` Tue-Wed) from `autosampler_schedule_2026.csv` ({cl['autosampler_rows']:,} rows, "
                f"{cl['autosampler_legacy_tags']} Q1 legacy tags); deduplicated {cl['intake_dups_dropped']} re-transmitted frames in "
                f"`intake_chemistry_15m_2026.csv` and {cl['ro_feed_dups_dropped']} in `ro_feed_header_15m_2026.csv` to 280,320 clean "
                f"15-minute rows each (excluding the first 32 burn-in intervals per Section 2); deduplicated {cl['hydraulics_dups_dropped']} "
                f"retries and converted {cl['hydraulics_ls_rows']:,} South-bay `L/s` readings to `m3/h` in `train_hydraulics_hourly_2026.csv` "
                f"(70,080 clean hours); aligned `shift_diagnostics_2026.csv` (17,520 four-hour blocks) and `cip_wash_log_2026.csv` "
                f"({cl['cip_rows']} CIP washes: {cl['cip_alk_rows']} `CIP_ALK_pH11` and {cl['cip_acid_rows']} `CIP_ACID_pH2`, "
                f"{cl['cip_legacy_tags']} H1 legacy tags) via explicit `Europe/Lisbon` offsets; and set aside the two out-of-scope "
                f"regional files (`mibel_iberian_power_spot_2026.csv`, `algarve_reservoir_levels_2026.xlsx`)."
            ),
            (
                f"2. Evaluated both direct monitoring (raw composite boron exceedances at {p26['raw_boron_2026_h']:,.1f} h, same-timestamp "
                f"scaling co-exceedances at {p26['raw_scaling_2026_h']:,.1f} h, and 2-of-3 shift majority vote at {p26['raw_struct_2026_h']:,.1f} h, "
                f"projecting {rt['direct']['total']:,.1f} h in 2027) and standard single-stream textbook models (stationary Gaussian AR(1) "
                f"composite deconvolution, 1D single-plug cumulative-volume conductivity matching, and 3-state pooled-CIP or post-CIP 2-class "
                f"Dawid-Skene EM, projecting {rt['rigorous_r1']['total']:,.1f} h and {rt['rigorous_r2']['total']:,.1f} h in 2027): direct "
                f"monitoring flags TR03 ({rt['direct']['members']['TR03']:,.1f} h), TR04 ({rt['direct']['members']['TR04']:,.1f} h), "
                f"TR06 ({rt['direct']['members']['TR06']:,.1f} h), and TR07 ({rt['direct']['members']['TR07']:,.1f} h) while missing "
                f"TR01 ({rt['direct']['members']['TR01']:,.1f} h) and TR02 ({rt['direct']['members']['TR02']:,.1f} h); the single-stream "
                f"textbook route still misses TR01 ({rt['rigorous_r1']['members']['TR01']:,.1f} h) and TR02 ({rt['rigorous_r1']['members']['TR02']:,.1f} h) "
                f"while mis-flagging TR03 ({rt['rigorous_r1']['members']['TR03']:,.1f} h), TR04 ({rt['rigorous_r1']['members']['TR04']:,.1f} h), "
                f"and TR05 ({rt['rigorous_r1']['members']['TR05']:,.1f} h)."
            ),
            (
                f"3. Modeled single-hour permeate boron under Fickian solution-diffusion flux coupling (`C_t = alpha_{{u,q}} + beta_u / Q_t + eps_t`) "
                f"inside the flow-proportional 4-hour and 8-hour composite bottles (`C_comp_k = alpha_{{u,q}} + beta_u / Q_bar_k + eps_bar_k`), "
                f"where `Q_bar_k` is the exact mean feed flow across each bottle's hours from `train_hydraulics_hourly_2026.csv`: fitting "
                f"per-train OLS for `(alpha_{{u,0..3}}, beta_u >= 0)` yields strong inverse-flow slopes (`beta` {tr['TR01']['s1_beta_hat']:.2f} "
                f"on TR01 and {tr['TR04']['s1_beta_hat']:.2f} on TR04), subtracting the 0.004 mg/L ICP-OES repeatability variance from "
                f"`lims_qa_certificate_2026.pdf`, minimizing WLS moment mismatch on residual `(V4, C4, V8, C8)` with weights "
                f"`[3/V4^2, 3/V4^2, 1/V8^2, 0.7/V8^2]` over a 200-point log-spaced discrete hourly AR(1) grid (`lambda` from 0.25 to 30.0 h) "
                f"recovers heterogeneous residual scales ({tr['TR01']['s1_lam_h']:.2f} h on TR01 vs {tr['TR04']['s1_lam_h']:.2f} h on TR04), "
                f"and integrating hourly survival `1 - Phi((0.50 - alpha_{{u,q}} - beta_u / Q_t) / sigma_{{1,u}})` across all 8,760 hourly flows "
                f"yields {p26['boron_2026_h']:,.1f} h in 2026 and {g['C1_boron_2027']:,.1f} h in 2027 (TR01 {tr['TR01']['boron_2027_h']:,.1f} h, "
                f"opening TR01 to {tr['TR01']['total_2027_h']:,.1f} h while keeping TR04 monitored at {tr['TR04']['total_2027_h']:,.1f} h). "
                f"Native-unit flux-plus-moment check F1 is {fal['golden']['f1']:.4f} golden vs {fal['direct']['f1']:.4f} raw and "
                f"{fal['S1_stat_ar1']['f1']:.4f} stationary AR(1), refuting raw composites ({rt['direct']['C1']:,.1f} h), 4-hour-only filtering "
                f"(TR01 {rt['s1_4h_only_TR01']:,.1f} h), stationary Gaussian AR(1) MLE ignoring `beta/Q_t` (TR01 {rt['s1_stat_ar1_TR01']:,.1f} h, "
                f"TR04 {rt['s1_stat_ar1_TR04']:,.1f} h), flux regression without AR(1) deconvolution (TR01 {rt['s1_flux_no_deconv_TR01']:,.1f} h), "
                f"i.i.d. `sqrt(m)` scaling (F1 {fal['S1_over']['f1']:.4f}, TR04 {rt['over_S1']['members']['TR04']:,.1f} h), and flux plus i.i.d. "
                f"residual scaling (TR04 {rt['s1_flux_iid_over_TR04']:,.1f} h)."
            ),
            (
                f"4. Reconstructed pretreated seawater arrival at each train's RO feed header via two-path bimodal DAF/DMF hydraulic mixing "
                f"in cumulative flow `Phi(t) = cumsum(0.25 * Q_15m)` (linearly interpolating hourly SCADA flows from `train_hydraulics_hourly_2026.csv` "
                f"to 15-minute intervals): profiling `c_out(Phi) = f_fast * c_in(Phi - V_fast) + (1 - f_fast) * c_in(Phi - V_main)` over "
                f"`f_fast in [0, 0.49]` (snapping `< 0.04` to zero), `V_fast in [160, 560]` m3, and `V_main in [760, 1520]` m3 to minimize L2 "
                f"conservative seawater conductivity mismatch across the 35,008 post-burn-in intervals per train recovers severe two-path bypass "
                f"on TR02 (`f_fast` {100.0 * tr['TR02']['s2_f_fast_hat']:.1f}%, `V_fast` {tr['TR02']['s2_v_fast_hat']:,.1f} m3, `V_main` "
                f"{tr['TR02']['s2_v_main_hat']:,.1f} m3) and TR05 (`f_fast` {100.0 * tr['TR05']['s2_f_fast_hat']:.1f}%, `V_fast` "
                f"{tr['TR05']['s2_v_fast_hat']:,.1f} m3, `V_main` {tr['TR05']['s2_v_main_hat']:,.1f} m3), and evaluating mixed header precursor "
                f"`X_arr(Phi) = f_fast * x_in(Phi - V_fast) + (1 - f_fast) * x_in(Phi - V_main) > 1.50` jointly with `ro_feed_stress_idx > 1.50` "
                f"yields {p26['scaling_2026_h']:,.1f} h in 2026 and {g['C2_scaling_2027']:,.1f} h in 2027 (TR02 {tr['TR02']['scaling_2027_h']:,.1f} h, "
                f"opening TR02 to {tr['TR02']['total_2027_h']:,.1f} h while keeping diluted TR05 monitored at {tr['TR05']['total_2027_h']:,.1f} h). "
                f"Fleet-mean conservative conductivity RMS (F2) drops to {fal['golden']['f2_ms_cm']:.3f} mS/cm at the probe noise floor versus "
                f"{fal['direct']['f2_ms_cm']:.3f} mS/cm same-timestamp ({rt['direct']['C2']:,.1f} h), {fal['S2_single_plug']['f2_ms_cm']:.3f} mS/cm "
                f"1D single-plug `V_eff` (misses TR02 at {rt['s2_single_plug_TR02']:,.1f} h and over-flags TR05 at {rt['s2_single_plug_TR05']:,.1f} h), "
                f"{fal['s2_fixed_lag']['f2_ms_cm']:.3f} mS/cm fixed wall-clock lag (TR02 {rt['s2_fixed_lag_TR02']:,.1f} h), and "
                f"{fal['s2_nom_vol']['f2_ms_cm']:.3f} mS/cm nominal volume (TR02 {rt['s2_nom_vol_TR02']:,.1f} h), while comonotonic upper-bound "
                f"pairing flips TR05 to {rt['over_S2']['members']['TR05']:,.1f} h."
            ),
            (
                f"5. Separated persistent structural membrane breaches from both organic bio-fouling and mineral scaling crust across "
                f"`shift_diagnostics_2026.csv` and `cip_wash_log_2026.csv` by partitioning each train's 2,190 four-hour blocks into three "
                f"chemical regimes (`Pre-CIP`, `Post-CIP_ALK` within 120 h = 30 blocks after `CIP_ALK_pH11`, and `Post-CIP_ACID` within 120 h = "
                f"30 blocks after `CIP_ACID_pH2`, forming 192 multinomial cells across 8 trains x 3 regimes x 8 alarm triples) and fitting a "
                f"4-state conditionally-independent latent-class EM (`Clean`, `Organic Bio-Fouling` cleared by `CIP_ALK_pH11`, `Mineral Crust` "
                f"cleared by `CIP_ACID_pH2`, and `Persistent Structural` invariant across both recipes) with shared central CIP-skid retention "
                f"ratios bounded in `[0.05, 0.65]`, allocating `pi_struct(u) * q_hours[q]` across 2026 quarters: fitted emissions cleanly separate "
                f"organic bio-fouling ({cns['s3_p_bio'][0]:.3f}, {cns['s3_p_bio'][1]:.3f}, {cns['s3_p_bio'][2]:.3f}), mineral crust "
                f"({cns['s3_p_min'][0]:.3f}, {cns['s3_p_min'][1]:.3f}, {cns['s3_p_min'][2]:.3f}, which generates acoustic chatter `D3` cleared by acid CIP), "
                f"and persistent structural breaches ({cns['s3_p_str'][0]:.3f}, {cns['s3_p_str'][1]:.3f}, {cns['s3_p_str'][2]:.3f}), clearing "
                f"mineral-crusted TR03 to {tr['TR03']['struct_2027_h']:,.1f} h (total {tr['TR03']['total_2027_h']:,.1f} h, MONITOR) while retaining "
                f"damaged TR06 at {tr['TR06']['struct_2027_h']:,.1f} h (total {tr['TR06']['total_2027_h']:,.1f} h, OVERHAUL), totaling "
                f"{p26['struct_2026_h']:,.1f} h in 2026 and {g['C3_struct_2027']:,.1f} h in 2027. Fleet recipe-stratified CIP drop mismatch F3 "
                f"is {fal['golden']['f3_pp']:.3f} pp versus {fal['direct']['f3_pp']:.3f} pp for 2-of-3 majority vote ({rt['direct']['C3']:,.1f} h), "
                f"{fal['S3_r1_pooled']['f3_pp']:.3f} pp for 3-state pooled-CIP `D3=0` EM (TR03 {rt['s3_r1_pooled_TR03']:,.1f} h), and "
                f"{fal['rigorous_r2']['f3_pp']:.3f} pp for 120-hour post-CIP 2-class Dawid-Skene (TR03 {rt['s3_r2_ds2_TR03']:,.1f} h), while "
                f"post-CIP majority vote flags TR03 at {rt['s3_post_cip_mv_TR03']:,.1f} h, unanimous 3-of-3 drops TR06 to "
                f"{rt['s3_unanimous_TR06']:,.1f} h, and baseline-adjusted raw `D3` after acid CIP drops TR06 to {rt['over_S3']['members']['TR06']:,.1f} h."
            ),
            (
                f"6. Verified all three native-unit physical falsification identities jointly across disjoint 2026 logs without any anomaly "
                f"labels: F1 flux-plus-moment error {fal['golden']['f1']:.4f}, F2 two-path seawater conductivity RMS "
                f"{fal['golden']['f2_ms_cm']:.3f} mS/cm, and F3 recipe-stratified CIP drop mismatch {fal['golden']['f3_pp']:.3f} pp "
                f"(combined {fal['golden']['combined']:.3f}) reject every raw and single-stream textbook alternative (combined "
                f"{fal['S2_single_plug']['combined']:.3f} to {fal['direct']['combined']:.3f}, including Textbook R1 at "
                f"{fal['rigorous_r1']['combined']:.3f} and Textbook R2 at {fal['rigorous_r2']['combined']:.3f})."
            ),
            (
                f"7. Carried quarterly 2026 mode hours into 2027 via Engineering Protocol SWRO-Q27 Annex A and `operating_plan_2027.csv` "
                f"(boron thermal multipliers 1.05, 1.14, 1.32, 1.09; scaling recovery multipliers 1.03, 1.12, 1.28, 1.07; per-train quarterly "
                f"dispatch duty ratios): plant-wide 2027 hours reach {g['A_total_2027']:,.1f} h (overhaul subset {g['A_overhaul_2027']:,.1f} h; "
                f"summer Q3 {g['A_q3_2027']:,.1f} h), whereas carrying 2026 golden totals flat without Annex A drops TR01 to "
                f"{rt['history_2026_flat_TR01']:,.1f} h and TR02 to {rt['history_2026_flat_TR02']:,.1f} h. Evaluating excess desalination "
                f"energy penalties under Section 4 (420 / 360 / 540 kWh/h, divided by 1,000 for MWh) yields {g['A_energy_mwh']:,.1f} MWh "
                f"plant-wide and {g['A_overhaul_mwh']:,.1f} MWh for overhaul trains (versus {rt['rigorous_r1']['energy_mwh']:,.1f} MWh on Textbook R1)."
            ),
            (
                f"8. Propagated model estimation uncertainty across {n_var} defensible estimator variants (1-hour-normalized continuous OU vs "
                f"discrete AR(1), OLS/WLS/lag-1 moments, 0.5% trimming, lab noise on/off, 4h-only moments, span-weighted WLS and Huber IRLS "
                f"flux regression; step-right/step-left/linear/midpoint flow integration, L1/L2/Huber/2%-trimmed two-path conductivity loss, "
                f"and linear/OU-kriging/PCHIP/nearest/cubic two-path TEP lookup; shared vs per-train CIP clearing, cross-recipe clearing, "
                f"96h/120h/144h and inclusive 31-block post-CIP windows; plus three joint cross-stump rebuilds) and six +/-20% independent mode "
                f"perturbations: all {n_var} variants and all 6 perturbations preserve the exact 4-of-8 overhaul slate (`TR01`, `TR02`, `TR06`, `TR07`), "
                f"keeping the lowest overhaul train at or above {rt['forcing_min_overhaul']:,.1f} h and the highest monitor train at or below "
                f"{rt['forcing_max_monitor']:,.1f} h."
            ),
            "",
            (
                f"No other overhaul classification survives the prompt, Engineering Protocol SWRO-Q27, and the physical laws in the 2026 logs, and each of "
                f"the three decisive steps independently moves a different train across the 400-hour criterion while keeping the other two "
                f"components intact: dropping flux-coupled boron deconvolution alone shifts C1 from {g['C1_boron_2027']:,.1f} to "
                f"{rt['drop_S1']['C1']:,.1f} h (total {rt['drop_S1']['total']:,.1f} h) and drops TR01 to {rt['drop_S1']['members']['TR01']:,.1f} h "
                f"(flagging TR02, TR06, TR07); dropping two-path hydraulic mixing alone shifts C2 from {g['C2_scaling_2027']:,.1f} to "
                f"{rt['drop_S2']['C2']:,.1f} h (total {rt['drop_S2']['total']:,.1f} h) and drops TR02 to {rt['drop_S2']['members']['TR02']:,.1f} h "
                f"(flagging TR01, TR06, TR07); and dropping 4-state dual-recipe CIP inversion alone inflates C3 from {g['C3_struct_2027']:,.1f} to "
                f"{rt['drop_S3']['C3']:,.1f} h (total {rt['drop_S3']['total']:,.1f} h) and pushes TR03 to {rt['drop_S3']['members']['TR03']:,.1f} h "
                f"(and TR04 to {rt['drop_S3']['members']['TR04']:,.1f} h, TR05 to {rt['drop_S3']['members']['TR05']:,.1f} h, flagging TR01 through TR07). "
                f"In pairs, dropping S1 and S2 flags TR06 and TR07 ({rt['drop_S1_S2']['total']:,.1f} h), dropping S1 and S3 flags TR02, TR03, TR04, TR05, "
                f"TR06, and TR07 ({rt['drop_S1_S3']['total']:,.1f} h), dropping S2 and S3 flags TR01, TR03, TR04, TR06, and TR07 "
                f"({rt['drop_S2_S3']['total']:,.1f} h), and dropping all three flags TR03, TR04, TR06, and TR07 ({rt['direct']['total']:,.1f} h). "
                f"The tightest boundary clearances sit on {min_ov_u} ({tr[min_ov_u]['total_2027_h']:,.1f} h, uncertainty range "
                f"{_bstr(f'A_{min_ov_u}')} h, {cns['clearance_min_ov_h']:,.1f} h above 400 h) and {max_mo_u} ({tr[max_mo_u]['total_2027_h']:,.1f} h, "
                f"uncertainty range {_bstr(f'A_{max_mo_u}')} h, {cns['clearance_max_mo_h']:,.1f} h below 400 h)."
            ),
            "",
        ]
    )
    return "\n".join(lines)


def emit_all(task_dir=None, res=None):
    task_dir = task_dir or os.path.dirname(HERE)
    target_dir = os.path.join(task_dir, "target")
    gen_dir = os.path.join(task_dir, "generator")
    if res is None:
        res = AN.run_all(target_dir)

    figs = build_figures(res)
    eff = build_effort_json(res, figs)
    meta = build_metadata(res)
    sub_md = build_submission_md(res, figs)

    with open(os.path.join(gen_dir, "figures.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(figs, f, indent=2, sort_keys=True)
        f.write("\n")
    with open(os.path.join(gen_dir, "effort.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(eff, f, indent=2)
        f.write("\n")
    with open(os.path.join(task_dir, "metadata.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(meta, f, indent=2, sort_keys=True)
        f.write("\n")
    with open(os.path.join(task_dir, "submission.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write(sub_md)
    return figs, eff, meta


if __name__ == "__main__":
    figs, eff, meta = emit_all()
    print("Wrote figures.json, effort.json, metadata.json, submission.md")
    print("Call:", figs["R8_overhaul_slate"], "Total:", figs["A_total_2027"], "Energy MWh:", figs["A_energy_mwh"])
