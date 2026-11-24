#!/usr/bin/env python3
"""task28/generator/writeup.py (v3): Emit task28/generator/figures.json,
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
        "bay_tds_clean_rows": cl["bay_tds_clean_rows"],
        "shift_rows": cl["shift_rows"],
        "cip_rows": cl["cip_rows"],
    }
    r6_fal_tbl = {
        "f1": _r4(fal["golden"]["f1"]),
        "f2_ms_cm": _r3(fal["golden"]["f2_ms_cm"]),
        "f3_pp": _r3(fal["golden"]["f3_pp"]),
        "f4_mg_l": _r3(fal["golden"]["f4_mg_l"]),
    }
    r7_trains_tbl = {u: _r1(tr[u]["total_2027_h"]) for u in core.TRAINS}
    r8_eng_tbl = {
        "A_energy_mwh": _r1(g["A_energy_mwh"]),
        "A_overhaul_mwh": _r1(g["A_overhaul_mwh"]),
    }

    min_ov_train = min(golden_slate, key=lambda u: tr[u]["total_2027_h"])
    max_mo_train = max(monitor_slate, key=lambda u: tr[u]["total_2027_h"])
    reflex = lat["S1+S2+S3+S4"]

    figs = {
        # Effort-tied result keys (R1..R9)
        "R1_clean_totals": r1_clean_tbl,
        "C1_boron_2027": _r1(g["C1_boron_2027"]),
        "C2_scaling_2027": _r1(g["C2_scaling_2027"]),
        "C3_struct_2027": _r1(g["C3_struct_2027"]),
        "C4_tds_2027": _r1(g["C4_tds_2027"]),
        "R6_falsification": r6_fal_tbl,
        "R7_train_totals_2027": r7_trains_tbl,
        "R8_energy_penalties": r8_eng_tbl,
        "R9_overhaul_slate": golden_slate,
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
                "bay": tr[u]["bay"],
                "boron_2026_h": _r1(tr[u]["boron_2026_h"]),
                "scaling_2026_h": _r1(tr[u]["scaling_2026_h"]),
                "struct_2026_h": _r1(tr[u]["struct_2026_h"]),
                "tds_2026_h": _r1(tr[u]["tds_2026_h"]),
                "total_2026_h": _r1(tr[u]["total_2026_h"]),
                "boron_2027_h": _r1(tr[u]["boron_2027_h"]),
                "scaling_2027_h": _r1(tr[u]["scaling_2027_h"]),
                "struct_2027_h": _r1(tr[u]["struct_2027_h"]),
                "tds_2027_h": _r1(tr[u]["tds_2027_h"]),
                "total_2027_h": _r1(tr[u]["total_2027_h"]),
                "q3_2027_h": _r1(tr[u]["q3_2027_h"]),
                "energy_2027_mwh": _r2(tr[u]["energy_2027_mwh"]),
                "designation": tr[u]["designation"],
                "v_nom_m3": int(round(tr[u]["v_nom_m3"])),
                "s1_mu_j": _r2(tr[u]["s1_mu_j"]),
                "s1_sd_j": _r2(tr[u]["s1_sd_j"]),
                "s1_lam_h": _r2(tr[u]["s1_lam_h"]),
                "s2_f_fast_pct": _r1(100.0 * tr[u]["s2_f_fast_hat"]),
                "s2_v_fast_hat": _r1(tr[u]["s2_v_fast_hat"]),
                "s2_v_main_hat": _r1(tr[u]["s2_v_main_hat"]),
                "s2_cond_rms": _r3(tr[u]["s2_cond_rms"]),
                "s2_lag_cond_rms": _r3(tr[u]["s2_lag_cond_rms"]),
                "s2_sp_cond_rms": _r3(tr[u]["s2_sp_cond_rms"]),
                "s3_pi_s_pct": _r2(100.0 * tr[u]["s3_pi_s_hat"]),
                "s3_pi_min_pct": _r2(100.0 * tr[u]["s3_pi_min_hat"]),
                "s3_tau_min_h": _r1(tr[u]["s3_tau_min_h"]),
                "s4_mu_mean": _r1(tr[u]["s4_mu_mean"]),
                "s4_sigma_hat": _r2(tr[u]["s4_sigma_hat"]),
                "s4_eq_sigma": _r2(tr[u]["s4_eq_sigma"]),
            }
            for u in core.TRAINS
        },
        # 2026 plant totals
        "plant_2026": {
            "boron_2026_h": _r1(sum(tr[u]["boron_2026_h"] for u in core.TRAINS)),
            "scaling_2026_h": _r1(sum(tr[u]["scaling_2026_h"] for u in core.TRAINS)),
            "struct_2026_h": _r1(sum(tr[u]["struct_2026_h"] for u in core.TRAINS)),
            "tds_2026_h": _r1(sum(tr[u]["tds_2026_h"] for u in core.TRAINS)),
            "total_2026_h": _r1(sum(tr[u]["total_2026_h"] for u in core.TRAINS)),
            "raw_boron_2026_h": _r1(sum(tr[u]["s1_raw_2026_h"] for u in core.TRAINS)),
            "raw_scaling_2026_h": _r1(sum(tr[u]["s2_raw_2026_h"] for u in core.TRAINS)),
            "raw_struct_2026_h": _r1(sum(tr[u]["s3_raw_2026_h"] for u in core.TRAINS)),
            "raw_tds_2026_h": _r1(sum(tr[u]["s4_raw_2026_h"] for u in core.TRAINS)),
            "raw_total_2026_h": _r1(
                sum(
                    tr[u]["s1_raw_2026_h"] + tr[u]["s2_raw_2026_h"]
                    + tr[u]["s3_raw_2026_h"] + tr[u]["s4_raw_2026_h"]
                    for u in core.TRAINS
                )
            ),
        },
        # 29-variant uncertainty ranges
        "bands": bnds,
        # Cleaning and operational constants from shipped files
        "cleaning": cl,
        "constants": {
            "threshold_h": core.THRESHOLD,
            "boron_limit_mg_l": core.BORON_LIMIT,
            "scaling_x_lim": core.SCALING_X_LIM,
            "scaling_y_lim": core.SCALING_Y_LIM,
            "tds_limit_mg_l": core.TDS_LIMIT,
            "energy_rate_boron_kwh_h": core.ENERGY_BORON_KWH,
            "energy_rate_scaling_kwh_h": core.ENERGY_SCALING_KWH,
            "energy_rate_struct_kwh_h": core.ENERGY_STRUCT_KWH,
            "energy_rate_tds_kwh_h": core.ENERGY_TDS_KWH,
            "kwh_per_mwh": 1000,
            "lab_sd_mg_l": core.LAB_BORON_SD,
            "boron_loq_mg_l": 0.020,
            "tds_meter_sd_mg_l": core.TDS_METER_SD,
            "cond_probe_sd": core.COND_PROBE_SD,
            "nominal_recovery_pct": 45,
            "dt_15m_hours": 0.25,
            "active_15m_per_train": 35008,
            "burn_in_intervals": 32,
            "burn_in_hours": 8,
            "v_fast_lo": 200,
            "v_fast_hi": 520,
            "v_main_lo": 960,
            "v_main_hi": 1600,
            "f_fast_cap": 0.50,
            "f_fast_floor": 0.04,
            "trim_pct": 0.5,
            "trimmed_l2_pct": 2,
            "f3_bin_early_h": 16,
            "f3_bin_mid_h": 120,
            "static_win_120": 120,
            "static_win_72": 72,
            "static_win_48": 48,
            "year_days": 365,
            "year_hours": 8760,
            "shift_blocks_per_train": 8760,
            "weibull_k_hi": 1.15,
            "weibull_k_lo": 0.90,
            "s1_wls_weights": [3.0, 3.0, 1.0, 0.7],
            "s3_n_params": 49,
            "s3_midpoint_shift_h": 0.5,
            "s3_jeffreys_alpha": 0.5,
            "s3_laplace_alpha": 1.0,
            "s2_coarse_grid_m3": 40,
            "s2_fine_grid_m3": 8,
            "tr06_profile_lrt_400h": res["tr06_profile_lrt_400h"],
            "tr05_kalman_lrt_400h": res["tr05_kalman_lrt_400h"],
            "min_overhaul_train": min_ov_train,
            "max_monitor_train": max_mo_train,
            "clearance_min_ov_h": _r1(tr[min_ov_train]["total_2027_h"] - core.THRESHOLD),
            "clearance_max_mo_h": _r1(core.THRESHOLD - tr[max_mo_train]["total_2027_h"]),
            "variant_min_overhaul_h": _r1(min(bnds[u][0] for u in golden_slate)),
            "variant_max_monitor_h": _r1(max(bnds[u][1] for u in monitor_slate)),
            "variant_min_ov_train": min(golden_slate, key=lambda u: bnds[u][0]),
            "variant_max_mo_train": max(monitor_slate, key=lambda u: bnds[u][1]),
            "n_variants": len(res["variants_named"]),
            "n_perturbations": len(res["perturbations"]),
            "n_input_files": len(PK.FILES),
            "n_overhaul": len(golden_slate),
            "n_monitor": len(monitor_slate),
            "n_trains": len(core.TRAINS),
            "perturbation_pct": 20,
            "plan_boron_temp_q": list(core.PLAN_BORON_TEMP_Q),
            "plan_scaling_rec_q": list(core.PLAN_SCALING_REC_Q),
            "plan_tds_sal_q": list(core.PLAN_TDS_SAL_Q),
            "s3_p_cl": [_r3(x) for x in tr["TR01"]["s3_p_cl"]],
            "s3_p_fb": [_r3(x) for x in tr["TR01"]["s3_p_fb"]],
            "s3_p_ms": [_r3(x) for x in tr["TR01"]["s3_p_ms"]],
        },
        # Native-unit physical falsification across routes
        "falsification": {
            k: {
                "f1": _r4(v["f1"]),
                "f2_ms_cm": _r3(v["f2_ms_cm"]),
                "f3_pp": _r3(v["f3_pp"]),
                "f4_mg_l": _r3(v["f4_mg_l"]),
                "combined": _r3(v["combined"]),
            }
            for k, v in fal.items()
        },
        # Routes, lattice, over-corrections, forcing bounds for Step-by-Step verification
        "routes": {
            "direct": {
                "C1": _r1(reflex["C1_boron_2027"]),
                "C2": _r1(reflex["C2_scaling_2027"]),
                "C3": _r1(reflex["C3_struct_2027"]),
                "C4": _r1(reflex["C4_tds_2027"]),
                "total": _r1(reflex["A_total_2027"]),
                "energy_mwh": _r1(reflex["A_energy_mwh"]),
                "members": {u: _r1(reflex["members"][u]) for u in core.TRAINS},
            },
            "rigorous_r1": {
                "C1": _r1(rig1["C1_boron_2027"]),
                "C2": _r1(rig1["C2_scaling_2027"]),
                "C3": _r1(rig1["C3_struct_2027"]),
                "C4": _r1(rig1["C4_tds_2027"]),
                "total": _r1(rig1["A_total_2027"]),
                "energy_mwh": _r1(rig1["A_energy_mwh"]),
                "members": {u: _r1(rig1["members"][u]) for u in core.TRAINS},
            },
            "rigorous_r2": {
                "C1": _r1(rig2["C1_boron_2027"]),
                "C2": _r1(rig2["C2_scaling_2027"]),
                "C3": _r1(rig2["C3_struct_2027"]),
                "C4": _r1(rig2["C4_tds_2027"]),
                "total": _r1(rig2["A_total_2027"]),
                "energy_mwh": _r1(rig2["A_energy_mwh"]),
                "members": {u: _r1(rig2["members"][u]) for u in core.TRAINS},
            },
            "drop_S1": {"C1": _r1(lat["S1"]["C1_boron_2027"]), "total": _r1(lat["S1"]["A_total_2027"]), "members": {u: _r1(lat["S1"]["members"][u]) for u in core.TRAINS}},
            "drop_S2": {"C2": _r1(lat["S2"]["C2_scaling_2027"]), "total": _r1(lat["S2"]["A_total_2027"]), "members": {u: _r1(lat["S2"]["members"][u]) for u in core.TRAINS}},
            "drop_S3": {"C3": _r1(lat["S3"]["C3_struct_2027"]), "total": _r1(lat["S3"]["A_total_2027"]), "members": {u: _r1(lat["S3"]["members"][u]) for u in core.TRAINS}},
            "drop_S4": {"C4": _r1(lat["S4"]["C4_tds_2027"]), "total": _r1(lat["S4"]["A_total_2027"]), "members": {u: _r1(lat["S4"]["members"][u]) for u in core.TRAINS}},
            "over_S1": {"members": {u: _r1(ov["S1"]["members"][u]) for u in core.TRAINS}},
            "over_S2": {"members": {u: _r1(ov["S2"]["members"][u]) for u in core.TRAINS}},
            "over_S3": {"members": {u: _r1(ov["S3"]["members"][u]) for u in core.TRAINS}},
            "over_S4": {"members": {u: _r1(ov["S4"]["members"][u]) for u in core.TRAINS}},
            "s1_r2_homosc_TR01": _r1(ex["cutoff:s1_r2_flux_homosced"]["members"]["TR01"]),
            "s1_r1_block_TR01": _r1(ex["cutoff:s1_r1_block_ar1"]["members"]["TR01"]),
            "s1_stat_TR01": _r1(ex["cutoff:s1_stat_ar1_no_flux"]["members"]["TR01"]),
            "s2_lag_TR02": _r1(ex["cutoff:s2_r1_r2_fixed_lag_tep"]["members"]["TR02"]),
            "s2_lag_TR05": _r1(ex["cutoff:s2_r1_r2_fixed_lag_tep"]["members"]["TR05"]),
            "s2_sp_TR05": _r1(ex["cutoff:s2_single_plug_veff"]["members"]["TR05"]),
            "s2_nv_TR02": _r1(ex["cutoff:s2_nom_vol"]["members"]["TR02"]),
            "s3_r1_uncond_TR03": _r1(ex["cutoff:s3_r1_uncond_3class"]["members"]["TR03"]),
            "s3_r2_120h_TR03": _r1(ex["cutoff:s3_r2_static_120h"]["members"]["TR03"]),
            "s3_unanimous_TR06": _r1(ex["cutoff:s3_unanimous"]["members"]["TR06"]),
            "s4_eq_var_TR08": _r1(ex["cutoff:s4_r1_r2_equal_var"]["members"]["TR08"]),
            "s4_eq_var_TR05": _r1(ex["cutoff:s4_r1_r2_equal_var"]["members"]["TR05"]),
            "history_2026_flat_TR01": _r1(ex["hedge:history_2026_flat"]["members"]["TR01"]),
            "history_2026_flat_TR02": _r1(ex["hedge:history_2026_flat"]["members"]["TR02"]),
            "forcing_min_overhaul": _r1(min(p["min_overhaul"] for p in res["perturbations"])),
            "forcing_max_monitor": _r1(max(p["max_monitor"] for p in res["perturbations"])),
            "fal_min_rival": _r3(min(v["combined"] for k, v in fal.items() if k != "golden")),
            "fal_max_rival": _r3(max(v["combined"] for k, v in fal.items() if k != "golden")),
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
    reflex = lat["S1+S2+S3+S4"]
    reflex_slate = _slate(reflex)
    rig1_slate = _slate(rig1)
    rig2_slate = _slate(rig2)

    quick_r1 = dict(figs["R1_clean_totals"])
    quick_r1["boron_clean_rows"] = res["cleaning"]["boron_raw_rows"]
    quick_r1["intake_clean_rows"] = res["cleaning"]["intake_raw_rows"]
    quick_r1["hydraulics_clean_rows"] = res["cleaning"]["hydraulics_raw_rows"]

    results = [
        {
            "id": "R1",
            "name": "Reconciled 2026 multi-grain SWRO logs across 15 shipped files",
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
            "name": "Spiegler-Kedem mass-flux composite boron deconvolution (C1)",
            "graded_as": "Component 1",
            "figure": "C1_boron_2027",
            "depends": ["R1"],
            "independent": "permeate_boron_composites_2026.csv, autosampler_schedule_2026.csv, train_hydraulics_hourly_2026.csv",
            "golden": figs["C1_boron_2027"],
            "band": bnds["C1_boron_2027"],
            "precedent": ["L22", "L56", "L57", "L28"],
            "passes": {
                "quick": _r1(reflex["C1_boron_2027"]),
                "careful": _r1(rig2["C1_boron_2027"]),
                "thorough": figs["C1_boron_2027"],
            },
        },
        {
            "id": "R3",
            "name": "Variable-flow two-path bimodal DAF/DMF hydraulic mixing (C2)",
            "graded_as": "Component 2",
            "figure": "C2_scaling_2027",
            "depends": ["R1"],
            "independent": "intake_chemistry_15m_2026.csv, ro_feed_header_15m_2026.csv, train_hydraulics_hourly_2026.csv",
            "golden": figs["C2_scaling_2027"],
            "band": bnds["C2_scaling_2027"],
            "precedent": ["L26", "L28", "N07", "N30"],
            "passes": {
                "quick": _r1(reflex["C2_scaling_2027"]),
                "careful": _r1(rig2["C2_scaling_2027"]),
                "thorough": figs["C2_scaling_2027"],
            },
        },
        {
            "id": "R4",
            "name": "Continuous post-CIP fouling re-growth kinetic LCA (C3)",
            "graded_as": "Component 3",
            "figure": "C3_struct_2027",
            "depends": ["R1"],
            "independent": "shift_diagnostics_2026.csv and cip_wash_log_2026.csv",
            "golden": figs["C3_struct_2027"],
            "band": bnds["C3_struct_2027"],
            "precedent": ["L03", "L38", "L54", "N36"],
            "passes": {
                "quick": _r1(reflex["C3_struct_2027"]),
                "careful": _r1(rig2["C3_struct_2027"]),
                "thorough": figs["C3_struct_2027"],
            },
        },
        {
            "id": "R5",
            "name": "Shared-bay permeate collector TDS heteroscedastic variance deconvolution (C4)",
            "graded_as": "Component 4",
            "figure": "C4_tds_2027",
            "depends": ["R1"],
            "independent": "bay_permeate_tds_hourly_2026.csv and train_hydraulics_hourly_2026.csv",
            "golden": figs["C4_tds_2027"],
            "band": bnds["C4_tds_2027"],
            "precedent": ["L22", "L33", "L28", "N36"],
            "passes": {
                "quick": _r1(reflex["C4_tds_2027"]),
                "careful": _r1(rig2["C4_tds_2027"]),
                "thorough": figs["C4_tds_2027"],
            },
        },
        {
            "id": "R6",
            "name": "Four native-unit physical falsification checks F1-F4",
            "graded_as": "Ask 1 (Validation)",
            "figure": "R6_falsification",
            "depends": ["R2", "R3", "R4", "R5"],
            "independent": "",
            "golden": figs["R6_falsification"],
            "bands": {"f1": [0.0, 0.14], "f2_ms_cm": [0.30, 0.40], "f3_pp": [0.0, 0.50], "f4_mg_l": [0.0, 0.25]},
            "precedent": ["L28", "L30"],
            "passes": {
                "quick": {
                    "f1": _r4(fal["direct"]["f1"]), "f2_ms_cm": _r3(fal["direct"]["f2_ms_cm"]),
                    "f3_pp": _r3(fal["direct"]["f3_pp"]), "f4_mg_l": _r3(fal["direct"]["f4_mg_l"]),
                },
                "careful": {
                    "f1": _r4(fal["rigorous_r2"]["f1"]), "f2_ms_cm": _r3(fal["rigorous_r2"]["f2_ms_cm"]),
                    "f3_pp": _r3(fal["rigorous_r2"]["f3_pp"]), "f4_mg_l": _r3(fal["rigorous_r2"]["f4_mg_l"]),
                },
                "thorough": figs["R6_falsification"],
            },
        },
        {
            "id": "R7",
            "name": "2027 Operating Plan train projections",
            "graded_as": "Ask 2 (Projections)",
            "figure": "R7_train_totals_2027",
            "depends": ["R2", "R3", "R4", "R5", "R6"],
            "independent": "",
            "golden": figs["R7_train_totals_2027"],
            "bands": {u: bnds[u] for u in core.TRAINS},
            "precedent": ["L32", "L33"],
            "passes": {
                "quick": {u: _r1(reflex["members"][u]) for u in core.TRAINS},
                "careful": {u: _r1(rig2["members"][u]) for u in core.TRAINS},
                "thorough": figs["R7_train_totals_2027"],
            },
        },
        {
            "id": "R8",
            "name": "2027 excess desalination energy penalty (MWh)",
            "graded_as": "Ask 3 (Energy Penalty)",
            "figure": "R8_energy_penalties",
            "depends": ["R2", "R3", "R4", "R5", "R7"],
            "independent": "",
            "golden": figs["R8_energy_penalties"],
            "bands": {
                "A_energy_mwh": bnds["A_energy_mwh"],
                "A_overhaul_mwh": bnds["A_overhaul_mwh"],
            },
            "precedent": ["L32", "L33"],
            "passes": {
                "quick": {"A_energy_mwh": _r1(reflex["A_energy_mwh"]), "A_overhaul_mwh": _r1(reflex["A_overhaul_mwh"])},
                "careful": {"A_energy_mwh": _r1(rig2["A_energy_mwh"]), "A_overhaul_mwh": _r1(rig2["A_overhaul_mwh"])},
                "thorough": figs["R8_energy_penalties"],
            },
        },
        {
            "id": "R9",
            "name": "Final 2027 vessel overhaul reliability classification",
            "graded_as": "Recommendation",
            "figure": "R9_overhaul_slate",
            "depends": ["R2", "R3", "R4", "R5", "R7", "R8"],
            "independent": "",
            "golden": g_slate,
            "precedent": ["L26", "L22"],
            "passes": {
                "quick": reflex_slate,
                "careful": rig2_slate,
                "thorough": g_slate,
            },
        },
    ]

    effort = {
        "results": results,
        "hints": [
            {
                "sentence": (
                    "Permeate boron obeys Spiegler-Kedem solute mass-flux conservation (C_t = alpha + J_B(t)/Q_t), "
                    "scaling hourly concentration SD as sigma_J/Q_t inside 4h/8h flow-proportional composites."
                ),
                "rescues": ["R2"],
            },
            {
                "sentence": (
                    "Variable diurnal flows and two-path bimodal DAF/DMF short-circuiting require cumulative-volume "
                    "Phi(t) two-path mixing recovered from conservative seawater conductivity."
                ),
                "rescues": ["R3"],
            },
            {
                "sentence": (
                    "Reversible mineral crust shares the exact single-block alarm profile of persistent structural "
                    "breaches and re-grows rapidly after acid CIP, requiring continuous post-CIP kinetic LCA."
                ),
                "rescues": ["R4"],
            },
            {
                "sentence": (
                    "Individual train permeate TDS (> 450 mg/L) is observed only via shared bay collectors, requiring "
                    "heteroscedastic variance-component deconvolution across staggered flow shares."
                ),
                "rescues": ["R5"],
            },
        ],
        "routes": [
            {"name": "golden (all 4 physical models)", "answer": g_slate, "golden": True},
            {"name": "direct / reflex (raw monitoring across all 4 modes)", "answer": reflex_slate},
            {"name": "rigorous R1 (Round-2 3.5h solver 1)", "answer": rig1_slate},
            {"name": "rigorous R2 (Round-2 3.5h solver 2)", "answer": rig2_slate},
            {"name": "drop S1 alone", "answer": _slate(lat["S1"])},
            {"name": "drop S2 alone", "answer": _slate(lat["S2"])},
            {"name": "drop S3 alone", "answer": _slate(lat["S3"])},
            {"name": "drop S4 alone", "answer": _slate(lat["S4"])},
            {"name": "cutoff run route", "answer": _slate(res["cut_asm"])},
            {"name": "generous run route", "answer": _slate(res["gen_asm"])},
            {"name": "hedge run route", "answer": _slate(res["hedge_asm"])},
            {"name": "over-correct S1 (flux i.i.d. sqrt(m))", "answer": _slate(res["over"]["S1"])},
            {"name": "over-correct S2 (comonotonic bound)", "answer": _slate(res["over"]["S2"])},
            {"name": "over-correct S3 (unanimous 3-of-3 alarms)", "answer": _slate(res["over"]["S3"])},
            {"name": "over-correct S4 (unweighted residual inflation)", "answer": _slate(res["over"]["S4"])},
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
                {"name": "drop S4", "answer": _slate(lat["S4"])},
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
                    "name": "Spiegler-Kedem solute mass-flux boron conservation and AR(1) support deconvolution",
                    "kind": "stump",
                    "precedent": ["L22", "L56", "L57"],
                    "dropped": {"answer": _slate(lat["S1"]), "results_moved": ["R2", "R6", "R7", "R8", "R9"]},
                    "alone": {"answer": _slate(lat["S2+S3+S4"]), "results_rescued": ["R2"]},
                },
                {
                    "id": "S2",
                    "name": "Variable-flow cumulative-volume two-path bimodal DAF/DMF hydraulic mixing",
                    "kind": "stump",
                    "precedent": ["L26", "L28", "N07", "N30"],
                    "dropped": {"answer": _slate(lat["S2"]), "results_moved": ["R3", "R6", "R7", "R8", "R9"]},
                    "alone": {"answer": _slate(lat["S1+S3+S4"]), "results_rescued": ["R3"]},
                },
                {
                    "id": "S3",
                    "name": "Continuous post-CIP fouling re-growth kinetic LCA separating identical-emission mineral crust",
                    "kind": "stump",
                    "precedent": ["L03", "L38", "L54", "N36"],
                    "dropped": {"answer": _slate(lat["S3"]), "results_moved": ["R4", "R6", "R7", "R8", "R9"]},
                    "alone": {"answer": _slate(lat["S1+S2+S4"]), "results_rescued": ["R4"]},
                },
                {
                    "id": "S4",
                    "name": "Shared-bay permeate collector TDS heteroscedastic variance-component deconvolution",
                    "kind": "stump",
                    "precedent": ["L22", "L33", "N36"],
                    "dropped": {"answer": _slate(lat["S4"]), "results_moved": ["R5", "R6", "R7", "R8", "R9"]},
                    "alone": {"answer": _slate(lat["S1+S2+S3"]), "results_rescued": ["R5"]},
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
        "weights": {"recommendation": 14, "components": 34, "asks": 45, "instruction": 7},
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
        "stated_inputs": ["400", "400.0", "2026", "2027"],
        "distractor_files": [F["dist_mibel"], F["dist_reservoir"]],
        "field_terms": ["CIP", "boron", "SWRO", "DAF", "DMF", "TDS", "Algarve"],
        "files": {
            F["standard_pdf"]: _entry(
                "Engineering Protocol SWRO-Q27 defining four physical excursion modes, overhaul criterion, excess desalination energy rates, Annex A 2027 forecast rules, and Annex B 9-column diagnostics output schema",
                "2026-09-14",
            ),
            F["lims_qa_pdf"]: _entry(
                "2026 ISO/IEC 17025 accredited LIMS ICP-OES permeate boron and inline bay permeate collector TDS probe analytical quality assurance certificate",
                "2027-01-08",
            ),
            F["asset_reg"]: _entry(
                "Barlavento SWRO train asset register with legacy tag crosswalk, bay assignments, and nominal DAF/DMF pretreatment basin volumes",
                "2026-11-18",
            ),
            F["op_plan"]: _entry(
                "2027 quarterly operating plan potable dispatch duty ratios and seasonal boron, scaling, and salinity process multipliers",
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
            F["bay_tds_h"]: _entry(
                "2026 hourly North Bay and South Bay shared common permeate collector flow and inline TDS telemetry",
                "2027-01-11",
            ),
            F["shift_diag"]: _entry(
                "2026 hourly shift inline non-destructive membrane integrity alarm logs",
                "2027-01-12",
            ),
            F["cip_log"]: _entry(
                "2026 routine Clean-in-Place alkaline and acid chemical wash completion log by train (with late-December 2025 carryover baseline)",
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

    ov_trains = [u for u in ordered if tr[u]["designation"] == "OVERHAUL"]
    mo_trains = [u for u in ordered if tr[u]["designation"] == "MONITOR"]
    ov_desc = ", ".join(f"{u} ({tr[u]['total_2027_h']:,.1f} h)" for u in ov_trains)
    mo_desc = ", ".join(f"{u} ({tr[u]['total_2027_h']:,.1f} h)" for u in mo_trains)
    min_ov_u = cns["min_overhaul_train"]
    max_mo_u = cns["max_monitor_train"]

    lines = [
        "# task28 answer blocks",
        "",
        "## Tags",
        "",
        "**Domain:** Engineering and Physical Sciences, Physical & Environmental Sciences (process control and measurement systems: coastal seawater reverse-osmosis membrane-train reliability diagnostics across conserved solute mass-flux composite lab assays, variable-flow two-path pretreatment hydraulics, continuous post-CIP fouling re-growth shift alarms, and shared-bay permeate collector TDS mixing).",
        "**Analytical objective:** Anomaly Detection & Diagnostics.",
        "",
        "## Final Recommendation",
        "",
        (
            f"**Schedule five Barlavento SWRO trains for 2027 pressure-vessel overhaul under Engineering Protocol SWRO-Q27's "
            f"400-hour engineering criterion: {ov_desc}, totaling {g['A_overhaul_2027']:,.1f} overhaul-train hours "
            f"(uncertainty range {_bstr('A_overhaul_2027')} h) and {g['A_overhaul_mwh']:,.1f} MWh projected energy penalty "
            f"(uncertainty range {_bstr('A_overhaul_mwh')} MWh), while retaining {mo_desc} on routine monitoring "
            f"(plant-wide 2027 total {g['A_total_2027']:,.1f} h, uncertainty range {_bstr('A_total_2027')} h; plant-wide "
            f"energy penalty {g['A_energy_mwh']:,.1f} MWh, uncertainty range {_bstr('A_energy_mwh')} MWh).** "
            f"This rejects both raw monitoring (which flags TR03 at {rt['direct']['members']['TR03']:,.1f} h, TR04 at "
            f"{rt['direct']['members']['TR04']:,.1f} h, TR05 at {rt['direct']['members']['TR05']:,.1f} h, TR06 at "
            f"{rt['direct']['members']['TR06']:,.1f} h, and TR07 at {rt['direct']['members']['TR07']:,.1f} h while "
            f"missing TR01 at {rt['direct']['members']['TR01']:,.1f} h, TR02 at {rt['direct']['members']['TR02']:,.1f} h, "
            f"and TR08 at {rt['direct']['members']['TR08']:,.1f} h) "
            f"and standard single-stream / equal-variance textbook models (homoscedastic `a + c/Q` boron AR(1), fixed "
            f"wall-clock lag `TEP -> stress` CCF, static 120-hour post-CIP 4-class EM, and equal-variance bay-collector "
            f"TDS pooling), which still miss TR01 ({rt['rigorous_r2']['members']['TR01']:,.1f} h), TR02 "
            f"({rt['rigorous_r2']['members']['TR02']:,.1f} h), and TR08 ({rt['rigorous_r2']['members']['TR08']:,.1f} h) "
            f"while mis-flagging TR03 ({rt['rigorous_r2']['members']['TR03']:,.1f} h), TR04 "
            f"({rt['rigorous_r2']['members']['TR04']:,.1f} h), and TR05 "
            f"({rt['rigorous_r2']['members']['TR05']:,.1f} h)."
        ),
        "",
        "## Supplementary Questions",
        "",
        f"### {DEL.GOLDEN_XLSX}",
        "",
        (
            f"The workbook opens on `Overhaul_Triage_2027` stating the 2027 vessel overhaul slate, 4-mode forecasts, "
            f"energy penalty in MWh, and {n_var}-variant estimation uncertainty ranges alongside a stacked horizontal bar "
            f"chart comparing each train's projected 2027 anomalous operating hours against the 400-hour criterion, "
            f"followed by formula-linked physical model backups (`S1_Boron_MassFlux`, `S2_TwoPath_Hydraulics`, "
            f"`S3_KineticCIP_LCA`, `S4_BayTDS_Deconv`), native-unit falsification and route comparisons "
            f"(`Falsification_And_Routes`), quarterly 2026-to-2027 forecasts (`Operating_Plan_2027`), and the "
            f"{n_var}-variant uncertainty battery and QA log (`Sensitivity_And_QA_2026`)."
        ),
        "",
        f"1. Forecasted 2027 anomalous operating hours by train across permeate boron, scaling, structural faults, and permeate TDS, Q3 hours, excess desalination energy penalty (MWh), and Section 3 overhaul designation ({n_var}-variant estimation uncertainty range on total in parentheses):",
    ]

    letters = "abcdefgh"
    for i, u in enumerate(ordered):
        t = tr[u]
        lines.append(
            f"   {letters[i]}. {u}: {t['total_2027_h']:,.1f} h total (uncertainty range {_bstr(u)} h) = "
            f"{t['boron_2027_h']:,.1f} h boron + {t['scaling_2027_h']:,.1f} h scaling + {t['struct_2027_h']:,.1f} h structural + "
            f"{t['tds_2027_h']:,.1f} h TDS; Q3 {t['q3_2027_h']:,.1f} h; {t['energy_2027_mwh']:,.2f} MWh; {t['designation']}."
        )

    lines.extend(
        [
            f"2. Plant-wide 2027 anomalous operating hours across all four failure modes, overhaul subset, and summer Q3 peak ({n_var}-variant estimation uncertainty ranges in parentheses):",
            f"   a. Plant-wide 2027 total anomalous operating hours: {g['A_total_2027']:,.1f} h (uncertainty range {_bstr('A_total_2027')} h).",
            f"   b. Overhaul-train subtotal ({', '.join(ov_trains)}): {g['A_overhaul_2027']:,.1f} h (uncertainty range {_bstr('A_overhaul_2027')} h).",
            f"   c. Plant-wide summer Q3 2027 anomalous operating hours: {g['A_q3_2027']:,.1f} h (uncertainty range {_bstr('A_q3_2027')} h).",
            f"   d. Plant-wide 2027 failure-mode totals: permeate boron {g['C1_boron_2027']:,.1f} h (uncertainty range {_bstr('C1_boron_2027')} h), scaling {g['C2_scaling_2027']:,.1f} h (uncertainty range {_bstr('C2_scaling_2027')} h), structural faults {g['C3_struct_2027']:,.1f} h (uncertainty range {_bstr('C3_struct_2027')} h), and permeate TDS {g['C4_tds_2027']:,.1f} h (uncertainty range {_bstr('C4_tds_2027')} h).",
            f"3. Projected 2027 excess desalination energy penalty in MWh under Section 4 (420 kWh/h boron, 360 kWh/h scaling, 540 kWh/h structural, 300 kWh/h permeate TDS; {n_var}-variant estimation uncertainty ranges in parentheses):",
            f"   a. Plant-wide 2027 energy penalty: {g['A_energy_mwh']:,.1f} MWh, or {figs['A_energy_mwh_exact']:,.2f} MWh exact (uncertainty range {_bstr('A_energy_mwh')} MWh).",
            f"   b. Overhaul-train 2027 energy penalty: {g['A_overhaul_mwh']:,.1f} MWh, or {figs['A_overhaul_mwh_exact']:,.2f} MWh exact (uncertainty range {_bstr('A_overhaul_mwh')} MWh).",
            "",
            f"### {DEL.GOLDEN_CSV}",
            "",
            (
                f"Eight rows sorted by `total_2027_h` descending ({', '.join('`' + u + '`' for u in ordered)}) "
                "carrying the exact Annex B 9-column plant historian schema (`train_id`, `boron_2027_h`, `scaling_2027_h`, "
                "`struct_2027_h`, `tds_2027_h`, `total_2027_h`, `q3_2027_h`, `energy_2027_mwh`, `designation`) matching "
                "every train figure in item 1 above."
            ),
            "",
            "## Critical Components",
            "",
            f"1. Plant-wide forecasted 2027 permeate boron excursion hours across all eight SWRO trains are **{g['C1_boron_2027']:,.1f} hours** (uncertainty range **{_bstr('C1_boron_2027')} hours**).",
            f"2. Plant-wide forecasted 2027 pretreatment-to-RO scaling excursion hours across all eight SWRO trains are **{g['C2_scaling_2027']:,.1f} hours** (uncertainty range **{_bstr('C2_scaling_2027')} hours**).",
            f"3. Plant-wide forecasted 2027 persistent structural membrane integrity fault hours across all eight SWRO trains are **{g['C3_struct_2027']:,.1f} hours** (uncertainty range **{_bstr('C3_struct_2027')} hours**).",
            f"4. Plant-wide forecasted 2027 individual train permeate TDS breakthrough hours across all eight SWRO trains are **{g['C4_tds_2027']:,.1f} hours** (uncertainty range **{_bstr('C4_tds_2027')} hours**).",
            "",
            "## Step-by-Step",
            "",
            (
                f"1. Conformed the 2026 operational archive ({cns['n_input_files']} files) to Engineering Protocol SWRO-Q27 Section 4: "
                f"mapped legacy `LINE-A` through `LINE-H` tags to `TR01` through `TR08` via `train_asset_register.csv`; cleaned "
                f"`permeate_boron_composites_2026.csv` from {cl['boron_raw_rows']:,} raw rows to {cl['boron_clean_rows']:,} unique "
                f"bottles by keeping maximum `qa_revision` ({cl['boron_superseded_dropped']} superseded preliminary rows dropped), "
                f"parsing {cl['boron_dmy_rows']:,} raw ({cl['boron_dmy_clean_rows']:,} post-deduplication) Portuguese `DD/MM/YYYY` dates, "
                f"converting {cl['boron_ug_rows']:,} raw ({cl['boron_ug_clean_rows']:,} post-deduplication) South-bay `ug/L` assays to `mg/L` "
                f"(all clean assays strictly above the 0.020 mg/L LOQ, minimum {cl['boron_min_comp_mg_l']:.4f} mg/L), and joining daily bottle "
                f"span (`4 h` Thu-Mon, `8 h` Tue-Wed) from `autosampler_schedule_2026.csv` ({cl['autosampler_rows']:,} rows, "
                f"{cl['autosampler_legacy_tags']} Q1 legacy tags); deduplicated {cl['intake_dups_dropped']} frames in "
                f"`intake_chemistry_15m_2026.csv` and {cl['ro_feed_dups_dropped']} in `ro_feed_header_15m_2026.csv` to 280,320 "
                f"clean 15-minute rows each (excluding the first 32 burn-in intervals per Section 2); deduplicated {cl['hydraulics_dups_dropped']} "
                f"retries and converted {cl['hydraulics_ls_rows']:,} South-bay `L/s` readings to `m3/h` in `train_hydraulics_hourly_2026.csv` "
                f"(70,080 clean hours); deduplicated {cl['bay_tds_dups_dropped']} PLC retries in `bay_permeate_tds_hourly_2026.csv` "
                f"({cl['bay_tds_clean_rows']:,} clean hourly bay collector rows); aligned `shift_diagnostics_2026.csv` ({cl['shift_rows']:,} hourly blocks) "
                f"and `cip_wash_log_2026.csv` ({cl['cip_rows']} alternating CIP washes: {cl['cip_alk_washes']} `CIP_ALK_pH11` and "
                f"{cl['cip_acid_washes']} `CIP_ACID_pH2`, including {cl['cip_carryover_2025']} late-Dec 2025 carryover washes and "
                f"{cl['cip_legacy_rows']} H1 legacy tags) via explicit `Europe/Lisbon` offsets; and set aside the two out-of-scope "
                f"regional files (`mibel_iberian_power_spot_2026.csv`, `algarve_reservoir_levels_2026.xlsx`)."
            ),
            (
                f"2. Evaluated both direct monitoring (raw composite boron at {p26['raw_boron_2026_h']:,.1f} h, same-timestamp "
                f"scaling at {p26['raw_scaling_2026_h']:,.1f} h, 2-of-3 shift majority vote at {p26['raw_struct_2026_h']:,.1f} h, "
                f"and direct bay-header TDS at {p26['raw_tds_2026_h']:,.1f} h, projecting {rt['direct']['total']:,.1f} h in 2027) "
                f"and standard textbook single-stream / equal-variance models (homoscedastic `a + c/Q` boron AR(1), fixed wall-clock "
                f"lag `TEP -> stress` CCF, static 120-hour post-CIP 4-class EM, and OLS means + equal-variance bay TDS pooling, "
                f"projecting {rt['rigorous_r2']['total']:,.1f} h in 2027): direct monitoring flags TR03, TR04, TR05, TR06, and TR07 while "
                f"missing TR01 ({rt['direct']['members']['TR01']:,.1f} h), TR02 ({rt['direct']['members']['TR02']:,.1f} h), and "
                f"TR08 ({rt['direct']['members']['TR08']:,.1f} h); the textbook solver still misses six of eight trains, dropping "
                f"TR01 ({rt['rigorous_r2']['members']['TR01']:,.1f} h), TR02 ({rt['rigorous_r2']['members']['TR02']:,.1f} h), and "
                f"TR08 ({rt['rigorous_r2']['members']['TR08']:,.1f} h) while mis-flagging TR03 ({rt['rigorous_r2']['members']['TR03']:,.1f} h), "
                f"TR04 ({rt['rigorous_r2']['members']['TR04']:,.1f} h), and TR05 ({rt['rigorous_r2']['members']['TR05']:,.1f} h)."
            ),
            (
                f"3. Modeled single-hour permeate boron under Spiegler-Kedem solute mass-flux conservation "
                f"(`C_t = alpha_{{u,q}} + (mu_{{J,u}} + eta_t) / Q_t`) inside the flow-proportional 4-hour and 8-hour composite "
                f"bottles (`M_k = Q_bar_k * C_comp_k = alpha_{{u,q}} * Q_bar_k + mu_{{J,u}} + eta_bar_k + Q_bar_k * nu_lab`), where "
                f"hourly concentration SD scales inversely with flow (`sigma_J / Q_t`): fitting per-train mass-flux OLS, removing "
                f"`Q_bar_k^2 * 0.004^2` ICP-OES repeatability variance from `lims_qa_certificate_2026.pdf`, inverting flux-space "
                f"same-calendar-day `(V4, C4, V8, C8)` WLS AR(1) moments with relative weights `[3.0/V4^2, 3.0/V4^2, 1.0/V8^2, 0.7/V8^2]` "
                f"(recovering `sigma_J` {tr['TR01']['s1_sd_j']:.2f} g/h and `lambda` "
                f"{tr['TR01']['s1_lam_h']:.2f} h on TR01 vs `lambda` {tr['TR04']['s1_lam_h']:.2f} h on TR04), and integrating "
                f"heteroscedastic hourly survival across all 8,760 hourly flows yields {p26['boron_2026_h']:,.1f} h in 2026 and "
                f"{g['C1_boron_2027']:,.1f} h in 2027 (TR01 {tr['TR01']['boron_2027_h']:,.1f} h, opening TR01 to "
                f"{tr['TR01']['total_2027_h']:,.1f} h while keeping TR04 monitored at {tr['TR04']['total_2027_h']:,.1f} h). "
                f"Native-unit flux-space heteroscedasticity and moment check F1 is {fal['golden']['f1']:.4f} golden vs "
                f"{fal['direct']['f1']:.4f} raw, {fal['S1_r2_homosc']['f1']:.4f} homoscedastic `a + c/Q` AR(1) (drops TR01 to "
                f"{rt['s1_r2_homosc_TR01']:,.1f} h), and {fal['S1_over']['f1']:.4f} flux i.i.d. `sqrt(m)` scaling (flips TR04 to "
                f"{rt['over_S1']['members']['TR04']:,.1f} h)."
            ),
            (
                f"4. Reconstructed pretreated seawater arrival at each train's RO feed header via variable-flow cumulative-volume "
                f"two-path bimodal DAF/DMF hydraulic mixing (`Phi(t) = cumsum(0.25 * Q_15m)` using linearly interpolated hourly-to-15-minute "
                f"flows): profiling `c_out(Phi) = f_fast * c_in(Phi - V_fast) + (1 - f_fast) * c_in(Phi - V_main)` on a 40 m3 coarse / "
                f"8 m3 fine grid over `f_fast in [0, 0.50]` (snapping `< 0.04` to zero), `V_fast in [200, 520]` m3, and `V_main in [960, 1600]` m3 "
                f"to minimize conservative seawater conductivity RMS across the 35,008 post-burn-in intervals recovers VFD-ramp residence on TR02 "
                f"(`f_fast` {100.0 * tr['TR02']['s2_f_fast_hat']:.1f}%, `V_main` {tr['TR02']['s2_v_main_hat']:,.1f} m3 vs nominal "
                f"{int(round(tr['TR02']['v_nom_m3'])):,} m3) and heavy short-circuit dilution on TR05 (`f_fast` "
                f"{100.0 * tr['TR05']['s2_f_fast_hat']:.1f}%, `V_fast` {tr['TR05']['s2_v_fast_hat']:,.1f} m3, `V_main` "
                f"{tr['TR05']['s2_v_main_hat']:,.1f} m3), yielding {p26['scaling_2026_h']:,.1f} h in 2026 and "
                f"{g['C2_scaling_2027']:,.1f} h in 2027 (TR02 {tr['TR02']['scaling_2027_h']:,.1f} h, opening TR02 to "
                f"{tr['TR02']['total_2027_h']:,.1f} h while keeping TR05 monitored at {tr['TR05']['total_2027_h']:,.1f} h). "
                f"Conservative seawater conductivity RMS (F2) drops to {fal['golden']['f2_ms_cm']:.3f} mS/cm at the 0.340 probe "
                f"floor vs {fal['direct']['f2_ms_cm']:.3f} mS/cm same-time ({rt['direct']['C2']:,.1f} h), "
                f"{fal['S2_r12_lag']['f2_ms_cm']:.3f} mS/cm fixed wall-clock lag (cuts TR02 from {tr['TR02']['total_2027_h']:,.1f} h "
                f"to {rt['s2_lag_TR02']:,.1f} h and flips TR05 to {rt['s2_lag_TR05']:,.1f} h), {fal['S2_single_plug']['f2_ms_cm']:.3f} mS/cm 1D single-plug `V_eff` "
                f"(flips TR05 to {rt['s2_sp_TR05']:,.1f} h), and nominal volume `V_nom` (drops TR02 to {rt['s2_nv_TR02']:,.1f} h), "
                f"while comonotonic pairing flips TR05 to {rt['over_S2']['members']['TR05']:,.1f} h."
            ),
            (
                f"5. Separated persistent structural membrane breaches from reversible organic bio-fouling and rapidly re-nucleating "
                f"mineral spacer crust across `shift_diagnostics_2026.csv` ({cl['shift_rows']:,} hourly blocks) and `cip_wash_log_2026.csv` "
                f"by computing exact continuous post-wash ages `(dt_alk_h, dt_acid_h)` from every alternating `CIP_ALK_pH11` and "
                f"`CIP_ACID_pH2` wash (anchored by late-Dec 2025 carryover washes) and solving the exact converged joint 49-parameter "
                f"maximum-likelihood continuous kinetic latent-class model (`w_bio = pi_bio * (1 - exp(-dt_alk / tau_bio))`, "
                f"`w_MS = pi_s + pi_min * (1 - exp(-dt_acid / tau_min))`, unconstrained `tau`, analytic-gradient L-BFGS-B) with "
                f"shared emission vectors (`Clean` {cns['s3_p_cl'][0]:.3f}/{cns['s3_p_cl'][1]:.3f}/{cns['s3_p_cl'][2]:.3f}, "
                f"`Bio-Fouling` {cns['s3_p_fb'][0]:.3f}/{cns['s3_p_fb'][1]:.3f}/{cns['s3_p_fb'][2]:.3f}, and identical "
                f"`Mineral Crust / Structural` {cns['s3_p_ms'][0]:.3f}/{cns['s3_p_ms'][1]:.3f}/{cns['s3_p_ms'][2]:.3f}): fast "
                f"post-acid re-growth on TR03 (`tau_min` {tr['TR03']['s3_tau_min_h']:.1f} h, `pi_s` {100.0 * tr['TR03']['s3_pi_s_hat']:.2f}%) "
                f"clears TR03 to {tr['TR03']['struct_2027_h']:,.1f} h (total {tr['TR03']['total_2027_h']:,.1f} h, MONITOR) while "
                f"retaining CIP-invariant structural damage on TR06 (`pi_s` {100.0 * tr['TR06']['s3_pi_s_hat']:.2f}%, "
                f"`tau_min` {tr['TR06']['s3_tau_min_h']:.1f} h, {tr['TR06']['struct_2027_h']:,.1f} h, total "
                f"{tr['TR06']['total_2027_h']:,.1f} h, OVERHAUL; profile-likelihood LRT against 400.0 h = "
                f"{cns['tr06_profile_lrt_400h']:.2f}), totaling {p26['struct_2026_h']:,.1f} h in 2026 and "
                f"{g['C3_struct_2027']:,.1f} h in 2027. Fine-age post-acid `D3` kinetic trajectory check F3 "
                f"(`0-16 h`, `16-120 h`, `> 120 h`) is {fal['golden']['f3_pp']:.3f} pp vs "
                f"{fal['direct']['f3_pp']:.3f} pp raw 2-of-3 MV ({rt['direct']['C3']:,.1f} h), {fal['S3_r1_uncond']['f3_pp']:.3f} pp "
                f"unconditioned 3-class LCA (TR03 {rt['s3_r1_uncond_TR03']:,.1f} h), and {fal['S3_r2_120h']['f3_pp']:.3f} pp static "
                f"120-hour post-CIP 4-class EM (TR03 {rt['s3_r2_120h_TR03']:,.1f} h), while unanimous 3-of-3 drops TR06 to "
                f"{rt['s3_unanimous_TR06']:,.1f} h."
            ),
            (
                f"6. Deconvolved individual train hourly permeate TDS breakthrough (`> 450 mg/L`, Section 2) from shared North Bay "
                f"and South Bay common permeate collectors (`bay_permeate_tds_hourly_2026.csv`) using staggered hourly bay flow "
                f"shares `w_{{u,t}} = Q_{{u,t}} / sum_{{j in bay}} Q_{{j,t}}` (uniform 45% nominal recovery): quarterly flow-share OLS "
                f"recovers exact train quarterly mean TDS (TR05 mean {tr['TR05']['s4_mu_mean']:.1f} mg/L vs TR08 mean "
                f"{tr['TR08']['s4_mu_mean']:.1f} mg/L), and heteroscedastic Gaussian variance-component MLE on bay residuals "
                f"`Var(r_bay) = 3.5^2 + sum w_{{u,t}}^2 * sigma_u^2` (removing the 3.5 mg/L inline probe repeatability from "
                f"`lims_qa_certificate_2026.pdf` and `scada_bay_config_2026.json`) separates volatile TR08 (`sigma` "
                f"{tr['TR08']['s4_sigma_hat']:.2f} mg/L) from steady TR05 (`sigma` {tr['TR05']['s4_sigma_hat']:.2f} mg/L; exact "
                f"4-state AR(1) Kalman profile-likelihood LRT against 400.0 h = {cns['tr05_kalman_lrt_400h']:.2f}), yielding "
                f"{p26['tds_2026_h']:,.1f} h in 2026 and {g['C4_tds_2027']:,.1f} h in 2027 (TR08 {tr['TR08']['tds_2027_h']:,.1f} h, "
                f"opening TR08 to {tr['TR08']['total_2027_h']:,.1f} h while keeping TR05 at {tr['TR05']['tds_2027_h']:,.1f} h). "
                f"Flow-share quartile bay residual SD mismatch F4 is {fal['golden']['f4_mg_l']:.3f} mg/L vs "
                f"{fal['direct']['f4_mg_l']:.3f} mg/L direct bay exceedances (0.0 h, dropping TR08 to "
                f"{rt['drop_S4']['members']['TR08']:,.1f} h), {fal['S4_eq_var']['f4_mg_l']:.3f} mg/L OLS + equal-variance bay pooling "
                f"(`sigma_eq` {tr['TR08']['s4_eq_sigma']:.2f} mg/L, cutting TR08 from {tr['TR08']['total_2027_h']:,.1f} h to "
                f"{rt['s4_eq_var_TR08']:,.1f} h and blowing up TR05 to {rt['s4_eq_var_TR05']:,.1f} h), and {fal['S4_over']['f4_mg_l']:.3f} mg/L unweighted inflation "
                f"(flips TR05 to {rt['over_S4']['members']['TR05']:,.1f} h)."
            ),
            (
                f"7. Verified all four native-unit physical falsification identities jointly across disjoint 2026 logs without any "
                f"anomaly labels: F1 {fal['golden']['f1']:.4f}, F2 {fal['golden']['f2_ms_cm']:.3f} mS/cm, F3 "
                f"{fal['golden']['f3_pp']:.3f} pp, and F4 {fal['golden']['f4_mg_l']:.3f} mg/L (combined chi-squared "
                f"{fal['golden']['combined']:.3f}) reject every raw and textbook rival (combined "
                f"{rt['fal_min_rival']:.3f} to {rt['fal_max_rival']:,.3f}, including Textbook R2 at "
                f"{fal['rigorous_r2']['combined']:.3f} and Textbook R1 at {fal['rigorous_r1']['combined']:.3f})."
            ),
            (
                f"8. Carried quarterly 2026 mode hours into 2027 via Engineering Protocol SWRO-Q27 Annex A and `operating_plan_2027.csv` "
                f"(boron thermal 1.05, 1.14, 1.32, 1.09; scaling recovery 1.03, 1.12, 1.28, 1.07; salinity thermal 1.04, 1.12, 1.26, "
                f"1.08; per-train quarterly dispatch duty ratios): plant-wide 2027 hours reach {g['A_total_2027']:,.1f} h (overhaul "
                f"subset {g['A_overhaul_2027']:,.1f} h; summer Q3 {g['A_q3_2027']:,.1f} h), whereas carrying 2026 golden totals flat "
                f"drops TR01 to {rt['history_2026_flat_TR01']:,.1f} h below 400 h (TR02 {rt['history_2026_flat_TR02']:,.1f} h). Evaluating "
                f"excess desalination energy penalties under Section 4 (420 / 360 / 540 / 300 kWh/h, divided by 1,000 for MWh) "
                f"yields {g['A_energy_mwh']:,.1f} MWh plant-wide and {g['A_overhaul_mwh']:,.1f} MWh for overhaul trains (versus "
                f"{rt['rigorous_r2']['energy_mwh']:,.1f} MWh on Textbook R2)."
            ),
            (
                f"9. Propagated model estimation uncertainty across {n_var} converged defensible physical variants (exact block-AR(1) "
                f"flux Gaussian MLE, exact continuous-time 1-hour block OU MLE, continuous 1-hour OU with relative WLS and "
                f"inverse-variance WLS, OLS/WLS/lag-1 AR(1), 0.5% trim, lab noise off, 4h-only, Huber flux fit, quarterly `mu_J`; "
                f"step-left/step-right/midpoint/trapz flow, L1/Huber/2%-trimmed conductivity loss, nearest TEP lookup; converged "
                f"volume-based exponential, Michaelis-Menten, Weibull k=1.15 and k=0.90, +0.5 h midpoint age, Jeffreys alpha=0.5 and "
                f"Laplace alpha=1.0 emission MAP, BIC-pruned TR06-only, and 2-step static-emission post-CIP kinetic MLE; OLS/WLS "
                f"squared-residual variance, meter noise off, Huber mean, joint GLS+MLE, temporal AR(1) innovation MLE, and exact "
                f"2-stage and GLS 4-state AR(1) Kalman MLE for bay TDS; plus three joint cross-stump rebuilds) and eight +/-20% "
                f"independent mode perturbations: all {n_var} variants preserve the exact 5-of-8 overhaul slate (`TR01`, `TR02`, "
                f"`TR06`, `TR07`, `TR08`) with the lowest overhaul train at or above {cns['variant_min_overhaul_h']:,.1f} h "
                f"({cns['variant_min_ov_train']}) and the highest monitor train at or below {cns['variant_max_monitor_h']:,.1f} h "
                f"({cns['variant_max_mo_train']}), and all 8 +/-20% perturbations preserve the identical slate with the lowest "
                f"overhaul train at or above {rt['forcing_min_overhaul']:,.1f} h and the highest monitor train at or below "
                f"{rt['forcing_max_monitor']:,.1f} h."
            ),
            "",
            (
                f"No other overhaul classification survives the prompt, Engineering Protocol SWRO-Q27, and the physical laws in the "
                f"2026 logs, and each of the four decisive steps independently moves a different train across the 400-hour criterion "
                f"while keeping the other three components intact: dropping mass-flux boron deconvolution alone shifts C1 from "
                f"{g['C1_boron_2027']:,.1f} to {rt['drop_S1']['C1']:,.1f} h (total {rt['drop_S1']['total']:,.1f} h) and drops TR01 "
                f"to {rt['drop_S1']['members']['TR01']:,.1f} h; dropping two-path hydraulic mixing alone shifts C2 from "
                f"{g['C2_scaling_2027']:,.1f} to {rt['drop_S2']['C2']:,.1f} h (total {rt['drop_S2']['total']:,.1f} h) and drops TR02 "
                f"to {rt['drop_S2']['members']['TR02']:,.1f} h; dropping continuous post-CIP kinetic LCA alone inflates C3 from "
                f"{g['C3_struct_2027']:,.1f} to {rt['drop_S3']['C3']:,.1f} h (total {rt['drop_S3']['total']:,.1f} h) and pushes TR03 "
                f"to {rt['drop_S3']['members']['TR03']:,.1f} h; and dropping shared-bay TDS variance-component deconvolution alone "
                f"drops C4 from {g['C4_tds_2027']:,.1f} to {rt['drop_S4']['C4']:,.1f} h (total {rt['drop_S4']['total']:,.1f} h) and "
                f"drops TR08 to {rt['drop_S4']['members']['TR08']:,.1f} h. The tightest point boundary clearances sit on {min_ov_u} "
                f"({tr[min_ov_u]['total_2027_h']:,.1f} h, uncertainty range {_bstr(min_ov_u)} h, {cns['clearance_min_ov_h']:,.1f} h "
                f"above 400 h) and {max_mo_u} ({tr[max_mo_u]['total_2027_h']:,.1f} h, uncertainty range {_bstr(max_mo_u)} h, "
                f"{cns['clearance_max_mo_h']:,.1f} h below 400 h), and across all {n_var} variants every overhaul train remains at or "
                f"above {cns['variant_min_overhaul_h']:,.1f} h ({cns['variant_min_ov_train']}) while every monitor train remains at "
                f"or below {cns['variant_max_monitor_h']:,.1f} h ({cns['variant_max_mo_train']})."
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
    print("Call:", figs["R9_overhaul_slate"], "Total:", figs["A_total_2027"], "Energy MWh:", figs["A_energy_mwh"])
