#!/usr/bin/env python3
"""Vesterdal Nett AS 66/22 kV substation peak-loading simulator & v2 decision core.

Three genuinely multi-step observation-process stumps on three distinct axes:
  - S1 (unit):    Sub-hourly 15-min active peak from hourly SCADA + monthly un-timestamped feeder
                  15-min registers, with NO feeder-level 15-min PQ and NO industrial-park labels.
                  Must strip regional diurnal+weather common mode across substations to isolate
                  stochastic feeder innovations, infer pairwise correlation R_ij (distinguishing
                  synchronized industrial clusters from staggered feeders of identical customer
                  class), and aggregate in correlated quadrature calibrated on 4 modernized sites.
  - S2 (what):    Peak-hour lagging reactive demand hidden behind fixed/switched capacitors AND
                  missing substation HV bus telemetry. Must couple all substations sharing each
                  radial 66 kV sub-transmission corridor (from GSP-Nord / GSP-Sor through shared
                  66 kV line impedances R_66, X_66) into simultaneous hourly linear systems
                  M(t) Q(t) = y(t) + delta_PT, jointly demeaned against monthly settled net kVARh
                  to eliminate each substation's PT calibration offset.
  - S3 (who):     Heaviest-loaded phase share w_max where GIS phase tags have drifted AND only
                  20 of 36 single-phase laterals carry AMI telemetry (matching 80/80 = 100% of
                  the commissioning tracer log, creating a self-confirming partial-coverage trap),
                  while the 16 non-AMI legacy laterals carry distinct/opposite phase skews. Must
                  invert total per-phase load from load-driven 3-phase LV bus voltage sag slope
                  d(V_ph - V_bar)/dP_tot calibrated on the 4 modernized sites' 3-phase PQ archive
                  (eliminating both static per-phase PT offsets and balanced shunt capacitors).

Run directly to verify Level 5 core proof and +/-20% forcing stability:
    python3 task26/generator/core.py --detail --forcing
"""
import itertools
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, ".claude", "skills", "stumping"))
import corelib  # noqa: E402

SEED = int(os.environ.get("CORE_SEED", 2622))
N_DAYS = 365
N_HOURS = N_DAYS * 24           # 8,760 hours in 2026
N_QH = N_HOURS * 4              # 35,040 quarter-hours (15-min ISPs)
V_NOM_LV = 22.0                 # 22 kV secondary distribution bus
V_NOM_HV = 66.0                 # 66 kV sub-transmission bus
TAP_STEP = 0.0125               # 1.25% per LTC tap step
LINE_P2 = 85.0                  # % of Firm N-1 MVA -> Phase 2 (2028-2029)
LINE_P1 = 100.0                 # % of Firm N-1 MVA -> Phase 1 (2027)
MONTH_DAYS = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
HOUR_MONTH = np.concatenate([np.full(d * 24, m, dtype=int) for m, d in enumerate(MONTH_DAYS)])
WINTER_MONTHS = (0, 1, 10, 11)
WINTER_HOURS = np.isin(HOUR_MONTH, WINTER_MONTHS)
HEATING_MONTHS = (0, 1, 2, 9, 10, 11)
HEATING_HOURS = np.isin(HOUR_MONTH, HEATING_MONTHS)

TARGETS = ("Drangvik", "Hestmark", "Kvernholm", "Malmnes", "Raudfjord", "Svarthaug", "Tverrli")
REFS = ("Fossheim", "Lindberg", "Ostervik", "Solberg")
ALL_SUBS = TARGETS + REFS

# Disjoint radial 66 kV sub-transmission corridors (neutral regional IDs off GSP-Nord and GSP-Sor)
CORRIDORS = {
    "COR-N01": {"gsp": "GSP-Nord", "segs": [
        ("GSP-Nord", "Ostervik", 4.0, 0.115, 0.385),
        ("Ostervik", "Fossheim", 38.0, 0.125, 0.405),
    ]},
    "COR-S01": {"gsp": "GSP-Sor", "segs": [
        ("GSP-Sor", "Lindberg", 5.0, 0.115, 0.385),
        ("Lindberg", "Solberg", 36.0, 0.125, 0.405),
    ]},
    "COR-N02": {"gsp": "GSP-Nord", "segs": [
        ("GSP-Nord", "Drangvik", 16.0, 0.120, 0.395),
        ("Drangvik", "Malmnes", 34.0, 0.125, 0.405),
    ]},
    "COR-N03": {"gsp": "GSP-Nord", "segs": [
        ("GSP-Nord", "Raudfjord", 10.0, 0.118, 0.390),
        ("Raudfjord", "Svarthaug", 24.0, 0.122, 0.400),
    ]},
    "COR-S02": {"gsp": "GSP-Sor", "segs": [
        ("GSP-Sor", "Hestmark", 7.0, 0.115, 0.385),
        ("Hestmark", "Kvernholm", 22.0, 0.122, 0.400),
        ("Kvernholm", "Tverrli", 28.0, 0.125, 0.405),
    ]},
}

SUB_CFG = {
    # S1-opened (SYNCHRONIZED cluster -> Phase 1 ~106.3%): identical feeder count, class mix, peak_mw, and cv_sub to Malmnes
    "Drangvik": dict(
        firm_mva=44.6, r_ohm=0.088, x_ohm=1.14, pt_offset_kv=0.34, pt_ph_off=(0.18, -0.11, -0.07),
        feeders=[
            ("industrial_batch", 5.2, 0.35, 1),
            ("industrial_batch", 5.0, 0.34, 1),
            ("industrial_batch", 4.8, 0.35, 1),
            ("maritime_port",    4.6, 0.34, 1),
            ("maritime_port",    4.4, 0.33, 1),
            ("commercial_mixed", 4.0, 0.14, 0),
            ("residential_heat", 3.6, 0.12, 0),
        ],
        q_alpha=0.64, q_peak_extra=9.5, c_fixed=17.0, c_switched_peak=0.0,
        sp_ami_share=0.32, sp_leg_share=0.26,
        ami_ph_w=(0.350, 0.330, 0.320), leg_ph_w=(0.440, 0.285, 0.275), gis_ph_w=(0.355, 0.325, 0.320),
    ),
    # Forced Phase 1 (>105% on every route, moved outside band by all 3 stumps)
    "Hestmark": dict(
        firm_mva=36.2, r_ohm=0.082, x_ohm=1.08, pt_offset_kv=-0.36, pt_ph_off=(-0.16, 0.12, 0.04),
        feeders=[
            ("industrial_batch", 14.5, 0.24, 2),
            ("industrial_batch", 12.0, 0.23, 2),
            ("commercial_mixed",  4.2, 0.12, 0),
            ("residential_heat",  3.8, 0.08, 0),
            ("residential_heat",  3.0, 0.08, 0),
        ],
        q_alpha=0.58, q_peak_extra=6.2, c_fixed=15.5, c_switched_peak=0.0,
        sp_ami_share=0.30, sp_leg_share=0.24,
        ami_ph_w=(0.380, 0.315, 0.305), leg_ph_w=(0.448, 0.285, 0.267), gis_ph_w=(0.355, 0.325, 0.320),
    ),
    # S2-opened: heavy fixed-cap winter inductive load (Q_peak ~18.7 MVAr -> Phase 1 ~107.4%)
    "Kvernholm": dict(
        firm_mva=37.4, r_ohm=0.095, x_ohm=1.22, pt_offset_kv=-0.68, pt_ph_off=(0.14, -0.19, 0.05),
        feeders=[
            ("industrial_batch", 9.6, 0.10, 3),
            ("industrial_batch", 8.2, 0.09, 3),
            ("commercial_mixed", 6.2, 0.08, 0),
            ("residential_heat", 5.6, 0.07, 0),
        ],
        q_alpha=0.92, q_peak_extra=16.5, c_fixed=25.0, c_switched_peak=0.0,
        sp_ami_share=0.30, sp_leg_share=0.25,
        ami_ph_w=(0.360, 0.325, 0.315), leg_ph_w=(0.415, 0.296, 0.289), gis_ph_w=(0.355, 0.325, 0.320),
    ),
    # Two-sided S1 & S2 corridor/switched-cap boundary (STAGGERED + switched winter cap -> Phase 2 ~95.9%)
    "Malmnes": dict(
        firm_mva=42.0, r_ohm=0.092, x_ohm=1.18, pt_offset_kv=-0.32, pt_ph_off=(-0.15, 0.06, 0.09),
        feeders=[
            ("industrial_batch", 5.2, 0.35, 0),
            ("industrial_batch", 5.0, 0.34, 0),
            ("industrial_batch", 4.8, 0.35, 0),
            ("maritime_port",    4.6, 0.34, 0),
            ("maritime_port",    4.4, 0.33, 0),
            ("commercial_mixed", 4.0, 0.14, 0),
            ("residential_heat", 3.6, 0.12, 0),
        ],
        q_alpha=0.40, q_peak_extra=2.6, c_fixed=3.0, c_switched_peak=10.5,
        sp_ami_share=0.31, sp_leg_share=0.25,
        ami_ph_w=(0.350, 0.330, 0.320), leg_ph_w=(0.428, 0.296, 0.276), gis_ph_w=(0.352, 0.326, 0.322),
    ),
    # S3-opened (+): AMI balanced (35.5%), legacy non-AMI piled onto Phase A (61%) -> Phase 1 ~119.1%
    "Raudfjord": dict(
        firm_mva=35.4, r_ohm=0.102, x_ohm=1.28, pt_offset_kv=0.35, pt_ph_off=(-0.22, 0.13, 0.09),
        feeders=[
            ("residential_heat", 7.8, 0.10, 0),
            ("residential_heat", 7.2, 0.10, 0),
            ("commercial_mixed", 6.4, 0.12, 0),
            ("industrial_batch", 6.6, 0.13, 0),
        ],
        q_alpha=0.54, q_peak_extra=6.4, c_fixed=13.5, c_switched_peak=0.0,
        sp_ami_share=0.34, sp_leg_share=0.38,
        ami_ph_w=(0.355, 0.325, 0.320), leg_ph_w=(0.610, 0.205, 0.185), gis_ph_w=(0.352, 0.328, 0.320),
    ),
    # S3-opened (-): AMI leans Phase C (54%), legacy non-AMI compensates on A & B -> Phase 2 ~91.3%
    "Svarthaug": dict(
        firm_mva=37.2, r_ohm=0.098, x_ohm=1.24, pt_offset_kv=-0.34, pt_ph_off=(0.15, 0.08, -0.23),
        feeders=[
            ("residential_heat", 8.2, 0.10, 0),
            ("residential_heat", 7.4, 0.10, 0),
            ("commercial_mixed", 7.0, 0.12, 0),
            ("industrial_batch", 6.8, 0.13, 0),
        ],
        q_alpha=0.60, q_peak_extra=8.0, c_fixed=15.5, c_switched_peak=0.0,
        sp_ami_share=0.36, sp_leg_share=0.36,
        ami_ph_w=(0.235, 0.225, 0.540), leg_ph_w=(0.455, 0.415, 0.130), gis_ph_w=(0.255, 0.265, 0.480),
    ),
    # Forced Defer (far end of COR-T3 -> local_dv & rp_only blow it up to Phase 1, golden ~73.9%)
    "Tverrli": dict(
        firm_mva=47.0, r_ohm=0.096, x_ohm=1.20, pt_offset_kv=0.32, pt_ph_off=(-0.14, 0.17, -0.03),
        feeders=[
            ("residential_heat", 6.0, 0.12, 0),
            ("commercial_mixed", 5.8, 0.15, 0),
            ("industrial_batch", 6.2, 0.22, 4),
            ("industrial_batch", 5.4, 0.21, 4),
        ],
        q_alpha=0.78, q_peak_extra=12.5, c_fixed=20.0, c_switched_peak=0.0,
        sp_ami_share=0.34, sp_leg_share=0.30,
        ami_ph_w=(0.370, 0.320, 0.310), leg_ph_w=(0.475, 0.270, 0.255), gis_ph_w=(0.355, 0.325, 0.320),
    ),
    # Ref 1: Lindberg (COR-R2 near GSP-Sor, 5 km): 8 feeders (4 ind + 2 mar SYNCHRONIZED + 1 comm + 1 res)
    # Identical feeder count, class mix, peak_mw, and cv_sub to Fossheim -> only cluster=5 vs 0 differs
    "Lindberg": dict(
        firm_mva=56.0, r_ohm=0.080, x_ohm=1.05, pt_offset_kv=0.64, pt_ph_off=(-0.24, 0.14, 0.10),
        feeders=[
            ("industrial_batch", 5.4, 0.36, 5),
            ("industrial_batch", 5.2, 0.35, 5),
            ("industrial_batch", 5.0, 0.36, 5),
            ("industrial_batch", 4.8, 0.35, 5),
            ("maritime_port",    4.6, 0.35, 5),
            ("maritime_port",    4.4, 0.34, 5),
            ("commercial_mixed", 3.5, 0.14, 0),
            ("residential_heat", 3.1, 0.12, 0),
        ],
        q_alpha=0.76, q_peak_extra=12.0, c_fixed=21.0, c_switched_peak=0.0,
        sp_ami_share=0.28, sp_leg_share=0.36,
        ami_ph_w=(0.345, 0.330, 0.325), leg_ph_w=(0.600, 0.205, 0.195), gis_ph_w=(0.350, 0.328, 0.322),
    ),
    # Ref 2: Fossheim (COR-R1 far end, 42 km): 8 feeders (4 ind + 2 mar STAGGERED + 1 comm + 1 res) + switched cap
    "Fossheim": dict(
        firm_mva=50.0, r_ohm=0.090, x_ohm=1.16, pt_offset_kv=-0.66, pt_ph_off=(0.24, -0.15, -0.09),
        feeders=[
            ("industrial_batch", 5.4, 0.36, 0),
            ("industrial_batch", 5.2, 0.35, 0),
            ("industrial_batch", 5.0, 0.36, 0),
            ("industrial_batch", 4.8, 0.35, 0),
            ("maritime_port",    4.6, 0.35, 0),
            ("maritime_port",    4.4, 0.34, 0),
            ("commercial_mixed", 3.5, 0.14, 0),
            ("residential_heat", 3.1, 0.12, 0),
        ],
        q_alpha=0.44, q_peak_extra=2.5, c_fixed=3.2, c_switched_peak=12.0,
        sp_ami_share=0.28, sp_leg_share=0.36,
        ami_ph_w=(0.350, 0.330, 0.320), leg_ph_w=(0.600, 0.205, 0.195), gis_ph_w=(0.352, 0.326, 0.322),
    ),
    # Ref 3: Ostervik (COR-R1 near GSP-Nord, 4 km): 4 mild independent feeders, AMI leans Phase C, legacy balances
    "Ostervik": dict(
        firm_mva=48.0, r_ohm=0.086, x_ohm=1.12, pt_offset_kv=-0.64, pt_ph_off=(0.22, -0.09, -0.13),
        feeders=[
            ("residential_heat", 8.2, 0.06, 0),
            ("residential_heat", 7.8, 0.06, 0),
            ("commercial_mixed", 8.0, 0.06, 0),
            ("industrial_batch", 7.6, 0.07, 0),
        ],
        q_alpha=0.80, q_peak_extra=13.5, c_fixed=20.5, c_switched_peak=0.0,
        sp_ami_share=0.34, sp_leg_share=0.34,
        ami_ph_w=(0.235, 0.225, 0.540), leg_ph_w=(0.455, 0.415, 0.130), gis_ph_w=(0.460, 0.275, 0.265),
    ),
    # Ref 4: Solberg (COR-R2 far end, 41 km): 3 synchronized industrial + 4 spiky independent, heavy Q, AMI leans C
    "Solberg": dict(
        firm_mva=46.0, r_ohm=0.086, x_ohm=1.10, pt_offset_kv=0.66, pt_ph_off=(-0.20, 0.24, -0.04),
        feeders=[
            ("industrial_batch", 5.2, 0.28, 6),
            ("industrial_batch", 5.0, 0.28, 6),
            ("industrial_batch", 4.8, 0.27, 6),
            ("maritime_port",    5.0, 0.30, 0),
            ("commercial_mixed", 4.8, 0.24, 0),
            ("commercial_mixed", 4.6, 0.22, 0),
            ("residential_heat", 4.4, 0.16, 0),
        ],
        q_alpha=0.82, q_peak_extra=13.5, c_fixed=22.0, c_switched_peak=0.0,
        sp_ami_share=0.34, sp_leg_share=0.34,
        ami_ph_w=(0.235, 0.225, 0.540), leg_ph_w=(0.455, 0.415, 0.130), gis_ph_w=(0.460, 0.275, 0.265),
    ),
}

CLASS_NOMINAL_PF = {
    "industrial_batch": 0.87,
    "maritime_port":    0.89,
    "commercial_mixed": 0.92,
    "residential_heat": 0.95,
}
N_AMI_LAT = 20
N_LEG_LAT = 16
N_LATERALS = N_AMI_LAT + N_LEG_LAT
RHO_CLUSTER = 0.88
RHO_INDEP = 0.00
TAN_PHI_UNBAL = 0.42


def _diurnal_and_season(rng):
    """Norwegian coastal 2026 temperature-driven seasonal and diurnal base shapes (8,760 hours)."""
    h = np.arange(N_HOURS)
    doy = h / 24.0
    hod = h % 24
    dow = (h // 24) % 7
    is_wkdy = (dow < 5).astype(float)

    season = 0.74 + 0.26 * np.cos(2.0 * np.pi * (doy - 18.0) / 365.0)
    cold_snap = (0.18 * np.exp(-0.5 * ((doy - 19.5) / 6.5) ** 4)
                 + 0.10 * np.exp(-0.5 * ((doy - 341.0) / 5.5) ** 4))
    weather_ar = np.zeros(N_DAYS)
    for d in range(1, N_DAYS):
        weather_ar[d] = 0.80 * weather_ar[d - 1] + rng.normal(0.0, 0.010)
    daily_w = np.repeat(weather_ar, 24)

    res_diurn = 0.62 + 0.16 * np.exp(-0.5 * ((hod - 8.0) / 2.2) ** 2) + 0.34 * np.exp(-0.5 * ((hod - 17.5) / 2.8) ** 4)
    com_diurn = (0.48 + 0.50 * np.exp(-0.5 * ((hod - 14.5) / 3.4) ** 4)) * (0.78 + 0.22 * is_wkdy)
    ind_diurn = (0.64 + 0.34 * np.exp(-0.5 * ((hod - 15.5) / 3.6) ** 4)) * (0.86 + 0.14 * is_wkdy)
    mar_diurn = 0.60 + 0.38 * np.exp(-0.5 * ((hod - 16.0) / 3.6) ** 4)

    shapes = {
        "residential_heat": np.clip((season + cold_snap + daily_w) * res_diurn, 0.25, 1.45),
        "commercial_mixed": np.clip((0.80 + 0.20 * season + 0.85 * cold_snap + 0.5 * daily_w) * com_diurn, 0.25, 1.40),
        "industrial_batch": np.clip((0.78 + 0.22 * season + 0.90 * cold_snap + 0.4 * daily_w) * ind_diurn, 0.35, 1.40),
        "maritime_port":    np.clip((0.80 + 0.20 * season + 0.85 * cold_snap + 0.5 * daily_w) * mar_diurn, 0.30, 1.40),
    }
    for k in shapes:
        shapes[k] = shapes[k] / np.quantile(shapes[k], 0.998)
    return shapes


def simulate():
    """Simulate the full 2026 physical grid (15-min P, hourly Q, radial 66 kV corridors, 3-ph bus sag, AMI laterals)."""
    rng = np.random.default_rng([SEED, 1])
    shapes = _diurnal_and_season(rng)
    gsp_v = {
        "GSP-Nord": V_NOM_HV * (1.022 - 0.015 * (shapes["residential_heat"] - 0.7) + rng.normal(0.0, 0.003, N_HOURS)),
        "GSP-Sor":  V_NOM_HV * (1.018 - 0.016 * (shapes["residential_heat"] - 0.7) + rng.normal(0.0, 0.003, N_HOURS)),
    }
    world = {"subs": {}, "shapes": shapes, "gsp_v": gsp_v, "corridors": CORRIDORS}

    for s_idx, s in enumerate(ALL_SUBS):
        cfg = SUB_CFG[s]
        srng = np.random.default_rng([SEED, 100, s_idx])
        n_f = len(cfg["feeders"])

        sub_common_h = srng.normal(0.0, 1.0, N_HOURS)
        sub_common_q = srng.normal(0.0, 1.0, (N_HOURS, 4))
        sub_common_q -= sub_common_q.mean(axis=1, keepdims=True)
        clusters = sorted({g for (_, _, _, g) in cfg["feeders"] if g > 0})
        cl_h_shocks = {g: srng.normal(0.0, 1.0, N_HOURS) for g in clusters}
        cl_q_shocks = {}
        for g in clusters:
            z = srng.normal(0.0, 1.0, (N_HOURS, 4))
            z -= z.mean(axis=1, keepdims=True)
            cl_q_shocks[g] = z

        f_p15 = np.zeros((n_f, N_HOURS, 4))
        f_p60 = np.zeros((n_f, N_HOURS))
        f_meta = []
        for f_i, (fcls, peak_mw, cv_sub, pgrp) in enumerate(cfg["feeders"]):
            h_ind = srng.normal(0.0, 1.0, N_HOURS)
            if pgrp > 0:
                h_shk = np.sqrt(RHO_CLUSTER) * cl_h_shocks[pgrp] + np.sqrt(1.0 - RHO_CLUSTER) * h_ind
            else:
                h_shk = np.sqrt(RHO_INDEP) * sub_common_h + np.sqrt(1.0 - RHO_INDEP) * h_ind
            f_noise = np.exp(0.009 * h_shk)
            p60 = peak_mw * shapes[fcls] * f_noise

            z_ind = srng.normal(0.0, 1.0, (N_HOURS, 4))
            z_ind -= z_ind.mean(axis=1, keepdims=True)
            if pgrp > 0:
                z_tot = np.sqrt(RHO_CLUSTER) * cl_q_shocks[pgrp] + np.sqrt(1.0 - RHO_CLUSTER) * z_ind
            else:
                z_tot = np.sqrt(RHO_INDEP) * sub_common_q + np.sqrt(1.0 - RHO_INDEP) * z_ind
            z_tot = np.clip(z_tot, -3.0, 3.0)
            z_tot -= z_tot.mean(axis=1, keepdims=True)
            z_tot = z_tot / np.std(z_tot)
            burst = cv_sub * 0.48 * p60[:, None] * z_tot
            burst -= burst.mean(axis=1, keepdims=True)
            p15 = np.maximum(0.1 * p60[:, None], p60[:, None] + burst)
            p60_exact = p15.mean(axis=1)
            f_p15[f_i] = p15
            f_p60[f_i] = p60_exact
            f_meta.append(dict(feeder_id=f"{s[:3].upper()}-F{f_i+1:02d}", fcls=fcls,
                               peak_mw=peak_mw, cv_sub=cv_sub, sync_cluster=pgrp))

        sub_p15 = f_p15.sum(axis=0)
        sub_p60 = sub_p15.mean(axis=1)
        peak_h_p15 = int(np.argmax(sub_p15.max(axis=1)))
        peak_q_idx = int(np.argmax(sub_p15[peak_h_p15]))
        true_p15_peak = float(sub_p15[peak_h_p15, peak_q_idx])
        peak_h_p60 = int(np.argmax(sub_p60))
        scada_p60_peak = float(sub_p60[peak_h_p60])

        p_norm = sub_p60 / np.quantile(sub_p60, 0.995)
        peak_ind_term = cfg["q_peak_extra"] / (1.0 + np.exp(-12.0 * (p_norm - 0.74)))
        sw_on = 1.0 / (1.0 + np.exp(-25.0 * (p_norm - 0.68)))
        q_hourly = (cfg["q_alpha"] * sub_p60 + peak_ind_term
                    - cfg["c_fixed"] - cfg["c_switched_peak"] * sw_on
                    + srng.normal(0.0, 0.16, N_HOURS))
        dp15 = sub_p15 - sub_p60[:, None]
        q_noise_15 = srng.normal(0.0, 0.15, (N_HOURS, 4))
        q_noise_15 -= q_noise_15.mean(axis=1, keepdims=True)
        q_15 = q_hourly[:, None] + 0.30 * dp15 + q_noise_15

        sub_s15 = np.sqrt(sub_p15 ** 2 + q_15 ** 2)
        s_peak_flat = int(np.argmax(sub_s15))
        s_peak_h, s_peak_q = divmod(s_peak_flat, 4)
        true_s15_tot = float(sub_s15[s_peak_h, s_peak_q])
        true_q_peak_h = float(q_hourly[s_peak_h])
        true_q15_at_peak = float(q_15[s_peak_h, s_peak_q])

        def _assign_ph(n_lat, w_tuple):
            cnts = [int(round(n_lat * w)) for w in w_tuple]
            cnts[2] = n_lat - cnts[0] - cnts[1]
            arr = [0] * cnts[0] + [1] * cnts[1] + [2] * cnts[2]
            srng.shuffle(arr)
            return np.array(arr, dtype=int)

        ami_true_ph = _assign_ph(N_AMI_LAT, cfg["ami_ph_w"])
        leg_true_ph = _assign_ph(N_LEG_LAT, cfg["leg_ph_w"])
        lat_true_ph = np.concatenate([ami_true_ph, leg_true_ph])
        lat_is_ami = np.array([True] * N_AMI_LAT + [False] * N_LEG_LAT)

        n_gis_ami = [int(round(N_AMI_LAT * w)) for w in cfg["gis_ph_w"]]
        n_gis_ami[2] = N_AMI_LAT - n_gis_ami[0] - n_gis_ami[1]
        n_gis_leg = [int(round(N_LEG_LAT * w)) for w in cfg["gis_ph_w"]]
        n_gis_leg[2] = N_LEG_LAT - n_gis_leg[0] - n_gis_leg[1]

        def _drift_gis(true_arr, target_cnts, min_mis):
            g = true_arr.copy()
            for pf in range(3):
                while int((g == pf).sum()) > target_cnts[pf]:
                    need = [p for p in range(3) if int((g == p).sum()) < target_cnts[p]]
                    g[int(srng.choice(np.where(g == pf)[0]))] = need[0]
            cm = int((g != true_arr).sum())
            if cm < min_mis:
                same = {p: list(np.where((g == p) & (true_arr == p))[0]) for p in range(3)}
                while cm < min_mis and all(len(same[p]) >= 1 for p in range(3)):
                    ia, ib, ic = same[0].pop(), same[1].pop(), same[2].pop()
                    g[ia], g[ib], g[ic] = 1, 2, 0
                    cm += 3
            return g

        lat_gis_ph = np.concatenate([_drift_gis(ami_true_ph, n_gis_ami, 5), _drift_gis(leg_true_ph, n_gis_leg, 5)])

        ami_tot_kw = cfg["sp_ami_share"] * sub_p60 * 1000.0
        leg_tot_kw = cfg["sp_leg_share"] * sub_p60 * 1000.0
        raw_lat = np.zeros((N_LATERALS, N_HOURS))
        lat_cls = [""] * N_LATERALS
        for blk_start, _blk_len, ph_arr in ((0, N_AMI_LAT, ami_true_ph), (N_AMI_LAT, N_LEG_LAT, leg_true_ph)):
            for ph in range(3):
                ph_pos = np.where(ph_arr == ph)[0]
                for rank_i, local_i in enumerate(ph_pos):
                    l_i = blk_start + int(local_i)
                    lcls = "residential_heat" if (rank_i % 4 != 0) else "commercial_mixed"
                    lat_cls[l_i] = lcls
                    base_sz = srng.lognormal(0.0, 0.14)
                    raw_lat[l_i] = base_sz * shapes[lcls] * np.exp(srng.normal(0.0, 0.030, N_HOURS))

        for ph in range(3):
            idx = np.where(ami_true_ph == ph)[0]
            raw_lat[idx] *= (cfg["ami_ph_w"][ph] * ami_tot_kw[s_peak_h]) / raw_lat[idx, s_peak_h].sum()
        lat_p_ami = raw_lat[:N_AMI_LAT] * (ami_tot_kw / raw_lat[:N_AMI_LAT].sum(axis=0))[None, :]

        for ph in range(3):
            idx = N_AMI_LAT + np.where(leg_true_ph == ph)[0]
            raw_lat[idx] *= (cfg["leg_ph_w"][ph] * leg_tot_kw[s_peak_h]) / raw_lat[idx, s_peak_h].sum()
        lat_p_leg = raw_lat[N_AMI_LAT:] * (leg_tot_kw / raw_lat[N_AMI_LAT:].sum(axis=0))[None, :]

        lat_p_all = np.vstack([lat_p_ami, lat_p_leg])
        lat_mwh = lat_p_all.sum(axis=1) / 1000.0
        bal_3ph_kw = (1.0 - cfg["sp_ami_share"] - cfg["sp_leg_share"]) * sub_p60 * 1000.0

        sub_p_ph_h = np.zeros((3, N_HOURS))
        for ph in range(3):
            sub_p_ph_h[ph] = (lat_p_all[lat_true_ph == ph].sum(axis=0) + bal_3ph_kw / 3.0) / 1000.0
        ph_share_h = sub_p_ph_h / sub_p60[None, :]
        sub_p15_ph = ph_share_h[:, :, None] * sub_p15[None, :, :]

        true_w_max = float(ph_share_h[:, s_peak_h].max())
        true_lim_mva = float(3.0 * true_w_max * true_s15_tot)
        true_loading_pct = float(100.0 * true_lim_mva / cfg["firm_mva"])

        feeder_m15 = np.zeros((n_f, 12))
        feeder_p60_m = np.zeros((n_f, 12))
        sub_kwh_m = np.zeros(12)
        sub_net_kvarh_m = np.zeros(12)
        for m in range(12):
            hm = HOUR_MONTH == m
            sub_kwh_m[m] = sub_p60[hm].sum() * 1000.0
            sub_net_kvarh_m[m] = q_hourly[hm].sum() * 1000.0
            for f_i in range(n_f):
                feeder_m15[f_i, m] = f_p15[f_i, hm, :].max()
                feeder_p60_m[f_i, m] = f_p60[f_i, hm].max()

        world["subs"][s] = dict(
            cfg=cfg, f_meta=f_meta,
            f_p60=f_p60, sub_p60=sub_p60, feeder_m15=feeder_m15, feeder_p60_m=feeder_p60_m,
            sub_kwh_m=sub_kwh_m, sub_net_kvarh_m=sub_net_kvarh_m,
            lat_gis_ph=lat_gis_ph, lat_cls=lat_cls, lat_is_ami=lat_is_ami, lat_mwh=lat_mwh,
            lat_p_ami=lat_p_ami,
            sub_p15=sub_p15, sub_p15_ph=sub_p15_ph, sub_p_ph_h=sub_p_ph_h,
            q_hourly=q_hourly, q_15=q_15, sub_s15=sub_s15,
            lat_true_ph=lat_true_ph, ami_true_ph=ami_true_ph,
            truth=dict(
                p15_peak=true_p15_peak, p60_peak=scada_p60_peak,
                q_peak_h=true_q_peak_h, q15_at_peak=true_q15_at_peak,
                s15_tot=true_s15_tot, w_max=true_w_max,
                lim_mva=true_lim_mva, loading_pct=true_loading_pct,
                relief_mva=max(0.0, true_lim_mva - 0.85 * cfg["firm_mva"]),
                s_peak_h=s_peak_h,
            ),
        )

    for c_id, c_info in CORRIDORS.items():
        v_cur = gsp_v[c_info["gsp"]].copy()
        subs_in_cor = [seg[1] for seg in c_info["segs"]]
        for seg_idx, (_frm, s, l_km, r_km, x_km) in enumerate(c_info["segs"]):
            downstream = subs_in_cor[seg_idx:]
            p_flow = sum(world["subs"][d]["sub_p60"] for d in downstream)
            q_flow = sum(world["subs"][d]["q_hourly"] for d in downstream)
            r_seg, x_seg = l_km * r_km, l_km * x_km
            dv_66 = (r_seg * p_flow + x_seg * q_flow) / V_NOM_HV
            v_cur = v_cur - dv_66

            sd = world["subs"][s]
            cfg = sd["cfg"]
            srng = np.random.default_rng([SEED, 200, ALL_SUBS.index(s)])
            dv_tx = (cfg["r_ohm"] * sd["sub_p60"] + cfg["x_ohm"] * sd["q_hourly"]) / V_NOM_LV
            ideal_ratio = (22.35 + dv_tx) / v_cur
            nom_ratio = V_NOM_LV / V_NOM_HV
            tap_step_int = np.clip(np.round(((ideal_ratio / nom_ratio) - 1.0) / TAP_STEP), -8, 8).astype(int)
            tau = nom_ratio * (1.0 + TAP_STEP * tap_step_int)
            v_lv_true = v_cur * tau - dv_tx
            v_lv_meas = v_lv_true - cfg["pt_offset_kv"] + srng.normal(0.0, 0.011, N_HOURS)

            z_eff = cfg["r_ohm"] + cfg["x_ohm"] * TAN_PHI_UNBAL
            p_ex = sd["sub_p_ph_h"] - (sd["sub_p60"][None, :] / 3.0)
            dv_ph_load = -(3.0 * z_eff / V_NOM_LV) * p_ex

            u_bg = srng.normal(0.0, 0.032, (3, N_HOURS))
            for ph in range(3):
                for t in range(1, N_HOURS):
                    u_bg[ph, t] = 0.55 * u_bg[ph, t - 1] + 0.835 * u_bg[ph, t]
            u_bg -= u_bg.mean(axis=0, keepdims=True)
            pt_ph = np.array(cfg["pt_ph_off"], dtype=float)[:, None]
            pt_ph -= pt_ph.mean()
            v_bus_ph = v_lv_meas[None, :] + pt_ph + dv_ph_load + u_bg

            lat_v_ami = np.zeros((N_AMI_LAT, N_HOURS))
            for l_i in range(N_AMI_LAT):
                ph = sd["ami_true_ph"][l_i]
                r_lat = srng.uniform(0.008, 0.018)
                lat_v_ami[l_i] = (230.0 / V_NOM_LV) * v_bus_ph[ph] - r_lat * sd["lat_p_ami"][l_i] + srng.normal(0.0, 0.20, N_HOURS)

            sd["corridor"] = c_id
            sd["gsp"] = c_info["gsp"]
            sd["v_hv_true"] = v_cur.copy()
            sd["v_lv_meas"] = v_lv_meas
            sd["tap_step_int"] = tap_step_int
            sd["v_bus_ph"] = v_bus_ph
            sd["lat_v_ami"] = lat_v_ami

    return world


def _infer_feeder_corr_matrices(world, opts):
    """Strip regional diurnal+weather common mode from hourly feeder SCADA to isolate pairwise innovation correlation."""
    mode_k = "raw_corr" if opts.get("s1_mode") == "raw_corr" else opts.get("s1_innov", "pca4")
    win_k = opts.get("s1_corr_win", "all")
    cache = world.setdefault("_R_cache", {})
    ckey = (mode_k, win_k)
    if ckey in cache:
        return cache[ckey]

    win_mask = WINTER_HOURS if win_k == "winter" else np.ones(N_HOURS, dtype=bool)
    method = opts.get("s1_innov", "pca4")
    if opts.get("s1_mode") == "raw_corr":
        out = {s: np.clip(np.corrcoef(world["subs"][s]["f_p60"][:, win_mask]), 0.0, 1.0) for s in ALL_SUBS}
        cache[ckey] = out
        return out

    if method.startswith("pca"):
        n_pc = int(method[3:])
        all_log = {}
        for s in ALL_SUBS:
            sd = world["subs"][s]
            L = np.log(np.maximum(sd["f_p60"] / sd["f_p60"].mean(axis=1, keepdims=True), 1e-4))
            L -= L.mean(axis=1, keepdims=True)
            all_log[s] = L
        R_mats = {}
        for s in ALL_SUBS:
            other_L = np.vstack([all_log[s2] for s2 in ALL_SUBS if s2 != s])
            _, _, Vt = np.linalg.svd(other_L[:, win_mask], full_matrices=False)
            F = Vt[:n_pc]
            Y = all_log[s][:, win_mask]
            E = Y - (Y @ F.T) @ F
            R = np.corrcoef(E)
            np.fill_diagonal(R, 1.0)
            R_mats[s] = np.clip(R, 0.0, 1.0)
        cache[ckey] = R_mats
        return R_mats

    by_cls = {}
    for s in ALL_SUBS:
        sd = world["subs"][s]
        for fi, fm in enumerate(sd["f_meta"]):
            arr = sd["f_p60"][fi]
            by_cls.setdefault(fm["fcls"], []).append((s, fi, arr / float(np.mean(arr))))
    cls_sum = {c: np.sum([x[2] for x in lst], axis=0) for c, lst in by_cls.items()}
    cls_cnt = {c: len(lst) for c, lst in by_cls.items()}
    R_mats = {}
    for s in ALL_SUBS:
        sd = world["subs"][s]
        nf = len(sd["f_meta"])
        innov = np.zeros((nf, int(win_mask.sum())))
        for fi, fm in enumerate(sd["f_meta"]):
            c = fm["fcls"]
            norm = sd["f_p60"][fi] / float(np.mean(sd["f_p60"][fi]))
            same_sub_norm = [sd["f_p60"][j] / float(np.mean(sd["f_p60"][j]))
                             for j, fm2 in enumerate(sd["f_meta"]) if fm2["fcls"] == c]
            n_other = cls_cnt[c] - len(same_sub_norm)
            ref_prof = (cls_sum[c] - np.sum(same_sub_norm, axis=0)) / max(n_other, 1)
            if method == "ref_diff":
                res = norm - ref_prof
            else:
                res = np.log(np.maximum(norm, 1e-4)) - np.log(np.maximum(ref_prof, 1e-4))
            innov[fi] = res[win_mask]
        R = np.corrcoef(innov)
        np.fill_diagonal(R, 1.0)
        R_mats[s] = np.clip(R, 0.0, 1.0)
    cache[ckey] = R_mats
    return R_mats


def _raw_quad_excess_month(sd, R_mat, m_list, form="mult", indep_only=False):
    nf = len(sd["f_meta"])
    hm_all = np.isin(HOUR_MONTH, m_list)
    idx_h = np.where(hm_all)[0]
    p60_pk_h = int(idx_h[np.argmax(sd["sub_p60"][idx_h])])
    deltas = np.zeros(nf)
    for i in range(nf):
        if form == "mult":
            rel = float(np.mean([(sd["feeder_m15"][i, m] - sd["feeder_p60_m"][i, m]) / sd["feeder_p60_m"][i, m]
                                 for m in m_list]))
            deltas[i] = max(0.0, rel) * float(sd["f_p60"][i, p60_pk_h])
        elif form == "add_raw":
            ex_m = float(np.mean([sd["feeder_m15"][i, m] - sd["feeder_p60_m"][i, m] for m in m_list]))
            deltas[i] = max(0.0, ex_m)
        else:
            ex_m = float(np.mean([sd["feeder_m15"][i, m] - sd["feeder_p60_m"][i, m] for m in m_list]))
            scale = float(sd["f_p60"][i, p60_pk_h]) / float(np.mean([sd["feeder_p60_m"][i, m] for m in m_list]))
            deltas[i] = max(0.0, ex_m * scale)
    if indep_only:
        return float(np.sqrt(np.sum(deltas ** 2)))
    return float(np.sqrt(max(0.0, float(deltas @ R_mat @ deltas))))


def _fit_ref_params(world, R_mats, opts):
    """Calibrate k_ord, dQ/dP, tan_phi_u, and rival baselines strictly on the 4 modernized reference substations."""
    m_opt = opts.get("s1_months", "winter")
    win_mask = WINTER_HOURS if m_opt in ("winter", "djf") else np.ones(N_HOURS, dtype=bool)
    dq_dp_list = []
    for r in REFS:
        sd = world["subs"][r]
        dp_sub = (sd["sub_p15"][win_mask, :] - sd["sub_p15"][win_mask, :].mean(axis=1, keepdims=True)).ravel()
        dq_sub = (sd["q_15"][win_mask, :] - sd["q_15"][win_mask, :].mean(axis=1, keepdims=True)).ravel()
        dq_dp_list.append(float(np.dot(dp_sub, dq_sub) / np.dot(dp_sub, dp_sub)))
    dq_dp = float(np.mean(dq_dp_list))

    if m_opt == "djf":
        cal_months = [0, 1, 11]
    elif m_opt == "winter":
        cal_months = list(WINTER_MONTHS)
    else:
        cal_months = list(range(12))
    form = opts.get("s1_form", "mult")
    indep_only = (opts.get("s1_mode") == "indep_quad")
    obs_l, raw_l, rats = [], [], []
    obs_ann, raw_ann = [], []
    for r in REFS:
        sd = world["subs"][r]
        for m in cal_months:
            hm = HOUR_MONTH == m
            obs_ex = float(sd["sub_p15"][hm, :].max() - sd["sub_p60"][hm].max())
            rq = _raw_quad_excess_month(sd, R_mats[r], [m], form=form, indep_only=indep_only)
            if rq > 1e-6:
                obs_l.append(obs_ex); raw_l.append(rq); rats.append(obs_ex / rq)
        obs_a = float(sd["sub_p15"].max() - sd["sub_p60"].max())
        rq_a = _raw_quad_excess_month(sd, R_mats[r], cal_months, form=form, indep_only=indep_only)
        if rq_a > 1e-6:
            obs_l.append(obs_a); raw_l.append(rq_a); rats.append(obs_a / rq_a)
            obs_ann.append(obs_a); raw_ann.append(rq_a)

    k_opt = opts.get("s1_kord")
    if k_opt == "median":
        k_ord = float(np.median(rats))
    elif k_opt == "mean_ratio":
        k_ord = float(np.mean(rats))
    elif k_opt == "annual_only":
        k_ord = float(sum(obs_ann) / sum(raw_ann))
    elif k_opt == "unit":
        k_ord = 1.0
    elif k_opt == "monthly_only":
        step = len(cal_months) + 1
        k_ord = float(sum(v for i, v in enumerate(obs_l) if (i + 1) % step != 0)
                      / sum(v for i, v in enumerate(raw_l) if (i + 1) % step != 0))
    else:
        k_ord = float(sum(obs_l) / sum(raw_l))

    flat_ratio = float(np.mean([world["subs"][r]["sub_p15"].max() / world["subs"][r]["sub_p60"].max() for r in REFS]))
    cf_vals = []
    for r in REFS:
        sd = world["subs"][r]
        pk_m = int(HOUR_MONTH[int(np.argmax(sd["sub_p60"]))])
        cf_vals.append(float(sd["sub_p15"].max() / sd["feeder_m15"][:, pk_m].sum()))
    cf_pooled = float(np.mean(cf_vals))

    X_ols, y_ols = [], []
    for r in REFS:
        sd = world["subs"][r]
        for m in range(12):
            hm = HOUR_MONTH == m
            r_sum = float(sd["feeder_m15"][:, m].sum())
            h_sum = float(sd["feeder_p60_m"][:, m].sum())
            H = float(sd["sub_p60"][hm].max())
            p15_m = float(sd["sub_p15"][hm, :].max())
            D = p15_m / (H * (r_sum / h_sum))
            r_ind = sum(sd["feeder_m15"][i, m] for i, fm in enumerate(sd["f_meta"]) if fm["fcls"] == "industrial_batch") / r_sum
            r_res = sum(sd["feeder_m15"][i, m] for i, fm in enumerate(sd["f_meta"]) if fm["fcls"] == "residential_heat") / r_sum
            r_mar = sum(sd["feeder_m15"][i, m] for i, fm in enumerate(sd["f_meta"]) if fm["fcls"] == "maritime_port") / r_sum
            X_ols.append([1.0, r_ind, r_res, r_mar, len(sd["f_meta"])])
            y_ols.append(D)
    beta_class_ols, *_ = np.linalg.lstsq(np.array(X_ols), np.array(y_ols), rcond=None)

    s3_mask = WINTER_HOURS if opts.get("s3_cal_win", "all") == "winter" else np.ones(N_HOURS, dtype=bool)
    num_t, den_t = 0.0, 0.0
    for r in REFS:
        sd = world["subs"][r]
        cfg = sd["cfg"]
        p_ph = sd["sub_p15_ph"].mean(axis=2)[:, s3_mask]
        p_ex = p_ph - p_ph.mean(axis=0, keepdims=True)
        v_ex = sd["v_bus_ph"][:, s3_mask] - sd["v_bus_ph"][:, s3_mask].mean(axis=0, keepdims=True)
        p_dm = p_ex - p_ex.mean(axis=1, keepdims=True)
        v_dm = v_ex - v_ex.mean(axis=1, keepdims=True)
        y_adj = -(v_dm + (3.0 * cfg["r_ohm"] / V_NOM_LV) * p_dm)
        x_reg = (3.0 * cfg["x_ohm"] / V_NOM_LV) * p_dm
        num_t += float(np.sum(x_reg * y_adj))
        den_t += float(np.sum(x_reg * x_reg))
    tan_phi_u = num_t / den_t

    return dict(
        k_ord=k_ord, dq_dp=dq_dp, flat_ratio=flat_ratio, cf_pooled=cf_pooled,
        beta_class_ols=beta_class_ols, tan_phi_u=tan_phi_u,
    )


def _estimate_s1(sd, R_mat, ref_p, opts):
    mode = opts.get("s1_mode", "golden")
    p60_pk = float(sd["sub_p60"].max())
    pk_h = int(np.argmax(sd["sub_p60"]))
    pk_m = int(HOUR_MONTH[pk_h])
    if mode == "scada60":
        return p60_pk
    if mode == "flat_ratio":
        return p60_pk * ref_p["flat_ratio"]
    if mode == "cf_pooled":
        return ref_p["cf_pooled"] * float(sd["feeder_m15"][:, pk_m].sum())
    if mode == "linear_sum":
        hm = HOUR_MONTH == pk_m
        f_m_max = sd["f_p60"][:, hm].max(axis=1)
        return float(np.sum(sd["f_p60"][:, pk_h] * (sd["feeder_m15"][:, pk_m] / np.maximum(f_m_max, 0.1))))
    if mode == "rigorous_cf60":
        cf60 = p60_pk / float(sd["f_p60"].max(axis=1).sum())
        return cf60 * float(sd["feeder_m15"].max(axis=1).sum())
    if mode == "class_ols":
        best_p = 0.0
        for m in range(12):
            hm = HOUR_MONTH == m
            r_sum = float(sd["feeder_m15"][:, m].sum())
            h_sum = float(sd["feeder_p60_m"][:, m].sum())
            H = float(sd["sub_p60"][hm].max())
            r_ind = sum(sd["feeder_m15"][i, m] for i, fm in enumerate(sd["f_meta"]) if fm["fcls"] == "industrial_batch") / r_sum
            r_res = sum(sd["feeder_m15"][i, m] for i, fm in enumerate(sd["f_meta"]) if fm["fcls"] == "residential_heat") / r_sum
            r_mar = sum(sd["feeder_m15"][i, m] for i, fm in enumerate(sd["f_meta"]) if fm["fcls"] == "maritime_port") / r_sum
            D = float(np.dot(ref_p["beta_class_ols"], [1.0, r_ind, r_res, r_mar, len(sd["f_meta"])]))
            best_p = max(best_p, H * (r_sum / h_sum) * D)
        return best_p
    months_opt = opts.get("s1_months", "winter")
    if months_opt == "djf":
        m_list = [0, 1, 11]
    elif months_opt == "winter":
        m_list = list(WINTER_MONTHS)
    elif months_opt == "all":
        m_list = list(range(12))
    else:
        m_list = [pk_m]
    rq = _raw_quad_excess_month(sd, R_mat, m_list, form=opts.get("s1_form", "mult"), indep_only=(mode == "indep_quad"))
    return p60_pk + ref_p["k_ord"] * rq


def _estimate_s2_all(world, opts):
    mode = opts.get("s2_mode", "golden")
    out_qh = {}
    if mode in ("net_kvarh", "class_nominal"):
        for s in ALL_SUBS:
            sd = world["subs"][s]
            p60 = sd["sub_p60"]
            pk_h = int(np.argmax(p60))
            if mode == "net_kvarh":
                e_p, e_q = float(sd["sub_kwh_m"].sum()), float(sd["sub_net_kvarh_m"].sum())
                pf = e_p / np.sqrt(e_p ** 2 + e_q ** 2)
                out_qh[s] = float(p60[pk_h] * np.tan(np.arccos(np.clip(pf, 0.5, 0.9999))) * (1.0 if e_q >= 0 else -1.0))
            else:
                out_qh[s] = float(sum(sd["f_p60"][i, pk_h] * np.tan(np.arccos(CLASS_NOMINAL_PF[fm["fcls"]]))
                                      for i, fm in enumerate(sd["f_meta"])))
        return out_qh

    for c_id, c_info in world["corridors"].items():
        v_gsp = world["gsp_v"][c_info["gsp"]]
        segs = c_info["segs"]
        subs = [seg[1] for seg in segs]
        m = len(subs)
        r_segs = [seg[2] * seg[3] for seg in segs]
        x_segs = [seg[2] * seg[4] for seg in segs]

        p_sub = np.vstack([world["subs"][s]["sub_p60"] for s in subs])
        vlv = np.vstack([world["subs"][s]["v_lv_meas"] for s in subs])
        taps = np.vstack([world["subs"][s]["tap_step_int"] for s in subs])
        tau = (V_NOM_LV / V_NOM_HV) * (1.0 + TAP_STEP * taps)
        r_tx = np.array([world["subs"][s]["cfg"]["r_ohm"] for s in subs])
        x_tx = np.array([world["subs"][s]["cfg"]["x_ohm"] for s in subs])

        dv_rp_66 = np.zeros((m, N_HOURS))
        for i in range(m):
            for e in range(i + 1):
                dv_rp_66[i] += (r_segs[e] * p_sub[e:].sum(axis=0)) / V_NOM_HV

        x_shared = np.zeros((m, m))
        for i in range(m):
            for j in range(m):
                x_shared[i, j] = sum(x_segs[:min(i, j) + 1]) / V_NOM_HV

        if mode in ("local_dv", "rp_only"):
            for i, s in enumerate(subs):
                sd = world["subs"][s]
                v_hv_assumed = v_gsp if mode == "local_dv" else (v_gsp - dv_rp_66[i])
                dv = v_hv_assumed * tau[i] - vlv[i]
                q_unc = (V_NOM_LV * dv - r_tx[i] * p_sub[i]) / x_tx[i]
                pk_h = int(np.argmax(p_sub[i]))
                pk_m = int(HOUR_MONTH[pk_h])
                hm = HOUR_MONTH == pk_m
                q_bar = float(sd["sub_net_kvarh_m"][pk_m]) / (1000.0 * int(hm.sum()))
                q_hat = q_unc - float(np.nanmean(q_unc[hm])) + q_bar
                valid = np.where(~np.isnan(q_hat))[0]
                top50 = valid[np.argsort(p_sub[i, valid])[-50:]]
                c = np.polyfit(p_sub[i, top50], q_hat[top50], 1)
                out_qh[s] = float(c[0] * p_sub[i, pk_h] + c[1])
            continue

        v_scale = vlv if opts.get("s2_vscale") == "vlv" else np.full_like(vlv, V_NOM_LV)
        y = v_gsp[None, :] * tau - vlv - tau * dv_rp_66 - (r_tx[:, None] * p_sub) / v_scale

        win_anchor = opts.get("s2_anchor", "peak_month")
        if win_anchor == "peak_month":
            pk_m = int(HOUR_MONTH[int(np.argmax(p_sub.sum(axis=0)))])
            amask = HOUR_MONTH == pk_m
            q_bar_m = np.array([world["subs"][s]["sub_net_kvarh_m"][pk_m] / (1000.0 * int(amask.sum())) for s in subs])
        elif win_anchor == "winter":
            amask = WINTER_HOURS
            q_bar_m = np.array([sum(world["subs"][s]["sub_net_kvarh_m"][mm] for mm in WINTER_MONTHS) / (1000.0 * int(amask.sum())) for s in subs])
        else:
            amask = np.ones(N_HOURS, dtype=bool)
            q_bar_m = np.array([world["subs"][s]["sub_net_kvarh_m"].sum() / (1000.0 * N_HOURS) for s in subs])

        valid_a = amask & (~np.isnan(y).any(axis=0))
        tau_bar = tau[:, valid_a].mean(axis=1)
        vs_bar = v_scale[:, valid_a].mean(axis=1)
        M_bar = tau_bar[:, None] * x_shared + np.diag(x_tx / vs_bar)
        M_bar_inv = np.linalg.inv(M_bar)

        y_fill = np.where(np.isnan(y), np.nanmean(y, axis=1, keepdims=True), y)
        vs_fill = np.where(np.isnan(v_scale), V_NOM_LV, v_scale)

        if mode == "raw_dv_no_demean":
            Q_hat = M_bar_inv @ y_fill
        elif opts.get("s2_solve", "exact_iter") == "mbar_only":
            Q_hat = q_bar_m[:, None] + M_bar_inv @ (y_fill - y[:, valid_a].mean(axis=1, keepdims=True))
        else:
            M_all = tau[:, None, :] * x_shared[:, :, None] + np.eye(m)[:, :, None] * (x_tx[:, None] / vs_fill)[:, None, :]
            M_inv = np.linalg.inv(np.transpose(M_all, (2, 0, 1)))
            q_y_a = (M_inv[valid_a] @ y_fill[:, valid_a].T[:, :, None]).squeeze(-1).mean(axis=0)
            delta_pt = np.linalg.solve(M_inv[valid_a].mean(axis=0), q_bar_m - q_y_a)
            Q_hat = (M_inv @ (y_fill + delta_pt[:, None]).T[:, :, None]).squeeze(-1).T

        agg = opts.get("s2_peak_agg", "fit50")
        for i, s in enumerate(subs):
            pk_h = int(np.argmax(p_sub[i]))
            if agg == "single":
                out_qh[s] = float(Q_hat[i, pk_h])
            elif agg == "top5":
                top5 = np.argsort(p_sub[i])[-5:]
                out_qh[s] = float(np.mean(Q_hat[i, top5]))
            else:
                top50 = np.argsort(p_sub[i])[-50:]
                c = np.polyfit(p_sub[i, top50], Q_hat[i, top50], 1)
                out_qh[s] = float(c[0] * p_sub[i, pk_h] + c[1])
    return out_qh


def _identify_ami_phases(sd):
    """Identify the true physical phase of the 20 AMI_SMART laterals via common-mode-rejected bus voltage differences."""
    if "_ami_ph_cache" in sd:
        return sd["_ami_ph_cache"]
    v_bus = sd["v_bus_ph"] * (230.0 / V_NOM_LV)
    v_cm = v_bus.mean(axis=0, keepdims=True)
    v_tilde = v_bus - v_cm
    idx_h = np.where(WINTER_HOURS)[0]
    r_v = sd["lat_v_ami"] - v_cm
    d_vt = np.diff(v_tilde[:, idx_h], axis=1)
    d_rv = np.diff(r_v[:, idx_h], axis=1)
    d_lp = np.diff(sd["lat_p_ami"][:, idx_h], axis=1)
    n_ami = sd["lat_v_ami"].shape[0]
    ph_id = np.zeros(n_ami, dtype=int)
    for l_i in range(n_ami):
        y, xp = d_rv[l_i], d_lp[l_i]
        rss = []
        for ph in range(3):
            X = np.column_stack([d_vt[ph], xp])
            b, *_ = np.linalg.lstsq(X, y, rcond=None)
            rss.append(float(np.sum(y ** 2)) if b[0] <= 0.1 else float(np.sum((y - X @ b) ** 2)))
        ph_id[l_i] = int(np.argmin(rss))
    sd["_ami_ph_cache"] = ph_id
    return ph_id


def _est_all_lat_peak_kw(sd, pk_h):
    """Estimate peak-hour kW for all 36 laterals strictly from shipped AMI hourly kW + GIS annual_billed_mwh."""
    ami_idx = np.where(sd["lat_is_ami"])[0]
    kw_per_mwh = {}
    for cls in set(sd["lat_cls"]):
        c_ami = [i for i in range(len(ami_idx)) if sd["lat_cls"][ami_idx[i]] == cls]
        if c_ami:
            kw_s = float(sd["lat_p_ami"][c_ami, pk_h].sum())
            mwh_s = float(sd["lat_mwh"][ami_idx[c_ami]].sum())
            kw_per_mwh[cls] = kw_s / max(mwh_s, 1e-6)
    fallback = float(sd["lat_p_ami"][:, pk_h].sum() / max(float(sd["lat_mwh"][ami_idx].sum()), 1e-6))
    out = np.zeros(len(sd["lat_mwh"]))
    ami_pos = {int(g): loc for loc, g in enumerate(ami_idx)}
    for l_i in range(len(out)):
        if l_i in ami_pos:
            out[l_i] = float(sd["lat_p_ami"][ami_pos[l_i], pk_h])
        else:
            out[l_i] = float(sd["lat_mwh"][l_i]) * kw_per_mwh.get(sd["lat_cls"][l_i], fallback)
    return out


def _estimate_s3(sd, ref_p, opts):
    mode = opts.get("s3_mode", "golden")
    cfg = sd["cfg"]
    p60 = sd["sub_p60"]
    pk_h = int(np.argmax(p60))
    if mode == "balanced":
        return 1.0 / 3.0
    if mode == "gis":
        ph_ids = sd["lat_gis_ph"]
        lat_kw = _est_all_lat_peak_kw(sd, pk_h)
        bal_kw = max(0.0, p60[pk_h] * 1000.0 - float(lat_kw.sum()))
        ph_kw = np.array([lat_kw[ph_ids == ph].sum() + bal_kw / 3.0 for ph in range(3)])
        return float(ph_kw.max() / ph_kw.sum())
    if mode == "ami_only_bal":
        ami_ph = _identify_ami_phases(sd)
        top5 = np.argsort(p60)[-5:]
        ws = []
        for h in top5:
            rem_kw = p60[h] * 1000.0 - sd["lat_p_ami"][:, h].sum()
            ph_kw = np.array([sd["lat_p_ami"][ami_ph == ph, h].sum() + rem_kw / 3.0 for ph in range(3)])
            ws.append(float(ph_kw.max() / ph_kw.sum()))
        return float(np.mean(ws))
    if mode == "ami_grossup":
        ami_ph = _identify_ami_phases(sd)
        top5 = np.argsort(p60)[-5:]
        scale = len(sd["lat_mwh"]) / float(sd["lat_p_ami"].shape[0])
        ws = []
        for h in top5:
            ami_sum = sd["lat_p_ami"][:, h].sum()
            est_sp_tot = min(p60[h] * 1000.0, ami_sum * scale)
            rem_kw = p60[h] * 1000.0 - est_sp_tot
            ph_kw = np.array([sd["lat_p_ami"][ami_ph == ph, h].sum() * (est_sp_tot / ami_sum) + rem_kw / 3.0 for ph in range(3)])
            ws.append(float(ph_kw.max() / ph_kw.sum()))
        return float(np.mean(ws))
    if mode == "ami_plus_gis":
        ami_ph = _identify_ami_phases(sd)
        comb_ph = sd["lat_gis_ph"].copy()
        comb_ph[sd["lat_is_ami"]] = ami_ph
        lat_kw = _est_all_lat_peak_kw(sd, pk_h)
        bal_kw = max(0.0, p60[pk_h] * 1000.0 - float(lat_kw.sum()))
        ph_kw = np.array([lat_kw[comb_ph == ph].sum() + bal_kw / 3.0 for ph in range(3)])
        return float(ph_kw.max() / ph_kw.sum())

    v_ex = sd["v_bus_ph"] - sd["v_bus_ph"].mean(axis=0, keepdims=True)
    z_eff = cfg["r_ohm"] + cfg["x_ohm"] * ref_p["tan_phi_u"]
    coeff = 3.0 * z_eff / V_NOM_LV

    if mode == "raw_vbus_no_pt":
        top10 = np.argsort(p60)[-10:]
        p_ex_hat = -v_ex[:, top10] / coeff
        w_h = (1.0 / 3.0) + p_ex_hat / p60[None, top10]
        return float(np.mean(w_h.max(axis=0)))

    s3_est = opts.get("s3_est", "lin_slope_all")
    if s3_est == "lin_slope_all":
        p_dm = p60 - p60.mean()
        slopes = (v_ex @ p_dm) / float(np.dot(p_dm, p_dm))
        w_ph = (1.0 / 3.0) - slopes / coeff
        return float(w_ph.max())
    if s3_est == "lin_slope_win":
        idx = np.where(WINTER_HOURS)[0]
        p_dm = p60[idx] - p60[idx].mean()
        slopes = (v_ex[:, idx] @ p_dm) / float(np.dot(p_dm, p_dm))
        w_ph = (1.0 / 3.0) - slopes / coeff
        return float(w_ph.max())
    if s3_est == "lin_slope_heat":
        idx = np.where(HEATING_HOURS)[0]
        p_dm = p60[idx] - p60[idx].mean()
        slopes = (v_ex[:, idx] @ p_dm) / float(np.dot(p_dm, p_dm))
        w_ph = (1.0 / 3.0) - slopes / coeff
        return float(w_ph.max())
    if s3_est == "diff_slope":
        dp = np.diff(p60)
        dv = np.diff(v_ex, axis=1)
        slopes = (dv @ dp) / float(np.dot(dp, dp))
        w_ph = (1.0 / 3.0) - slopes / coeff
        return float(w_ph.max())
    if s3_est == "ami_plus_vbus_resid":
        # Hybrid: subtract identified AMI lateral voltage drop on heating hours, invert legacy residual from slope
        ami_ph = _identify_ami_phases(sd)
        idx = np.where(HEATING_HOURS)[0]
        p_ami_ph = np.array([sd["lat_p_ami"][ami_ph == ph][:, idx].sum(axis=0) / 1000.0 for ph in range(3)])
        p_ami_ex = p_ami_ph - p_ami_ph.mean(axis=0, keepdims=True)
        v_rem = v_ex[:, idx] + coeff * p_ami_ex
        p_rem = p60[idx] - p_ami_ph.sum(axis=0)
        p_dm = p_rem - p_rem.mean()
        sl_rem = (v_rem @ p_dm) / float(np.dot(p_dm, p_dm))
        pk_pos = int(np.where(idx == pk_h)[0][0])
        p_leg_ex_pk = (-sl_rem / coeff) * p_rem[pk_pos]
        p_tot_ph_pk = (p60[pk_h] / 3.0) + p_ami_ex[:, pk_pos] + p_leg_ex_pk
        return float(p_tot_ph_pk.max() / p60[pk_h])

    # intercept_top10: subtract OLS PT-offset intercept, invert top-10 peak hours
    p_dm = p60 - p60.mean()
    slopes = (v_ex @ p_dm) / float(np.dot(p_dm, p_dm))
    pt_hat = v_ex.mean(axis=1) - slopes * p60.mean()
    pt_hat -= pt_hat.mean()
    idx = np.argsort(p60)[-10:]
    w_h = (1.0 / 3.0) - (v_ex[:, idx] - pt_hat[:, None]) / (coeff * p60[None, idx])
    return float(np.mean(w_h.max(axis=0)))


def evaluate(world, opts=None):
    opts = opts or {}
    R_mats = _infer_feeder_corr_matrices(world, opts)
    ref_p = _fit_ref_params(world, R_mats, opts)
    q_h_all = _estimate_s2_all(world, opts)
    m_kord = float(opts.get("mult_kord", 1.0))
    m_q = float(opts.get("mult_q", 1.0))
    m_w = float(opts.get("mult_w_excess", 1.0))
    out = {}
    for s in ALL_SUBS:
        sd = world["subs"][s]
        cfg = sd["cfg"]
        p60_pk = float(sd["sub_p60"].max())
        p15_raw = _estimate_s1(sd, R_mats[s], ref_p, opts)
        p15 = p60_pk + m_kord * (p15_raw - p60_pk)
        q_h = q_h_all[s] * m_q
        q15_rule = opts.get("q15_rule", "ref_slope")
        if q15_rule == "ref_slope":
            q15 = q_h + ref_p["dq_dp"] * (p15 - p60_pk)
        elif q15_rule == "const_q":
            q15 = q_h
        else:
            q15 = q_h * (p15 / p60_pk)
        s15_tot = float(np.sqrt(p15 ** 2 + q15 ** 2))
        w_raw = _estimate_s3(sd, ref_p, opts)
        w_max = (1.0 / 3.0) + m_w * (w_raw - 1.0 / 3.0)
        lim_mva = float(3.0 * w_max * s15_tot)
        loading_pct = float(100.0 * lim_mva / cfg["firm_mva"])
        relief_mva = float(max(0.0, lim_mva - 0.85 * cfg["firm_mva"]))
        out[s] = dict(p15=p15, q_h=q_h, q15=q15, s15_tot=s15_tot, w_max=w_max,
                      lim_mva=lim_mva, loading_pct=loading_pct, relief_mva=relief_mva)
    return out, ref_p


HURRIED = {
    "S1": {"s1_mode": "scada60"},
    "S2": {"s2_mode": "net_kvarh"},
    "S3": {"s3_mode": "gis"},
}
DIRECT = {"s1_mode": "scada60", "s2_mode": "net_kvarh", "s3_mode": "balanced"}
RIGOROUS = {"s1_mode": "cf_pooled", "s2_mode": "class_nominal", "s3_mode": "ami_only_bal"}
FRONTIER_COMBO = {"s1_mode": "class_ols", "s2_mode": "local_dv", "s3_mode": "ami_only_bal"}

FAMILY = [
    ("golden", {}),
    ("S1 excess on all 12 months", {"s1_months": "all"}),
    ("S1 excess on peak month only", {"s1_months": "peak_m"}),
    ("S1 DJF 3-month winter window", {"s1_months": "djf"}),
    ("S1 DJF 3-month annual-only k_ord", {"s1_months": "djf", "s1_kord": "annual_only"}),
    ("S1 additive feeder excess scaling", {"s1_form": "add"}),
    ("S1 raw additive feeder excess", {"s1_form": "add_raw"}),
    ("S1 innovation corr on winter hours", {"s1_corr_win": "winter"}),
    ("S1 5-PC regional factor stripping", {"s1_innov": "pca5"}),
    ("S1 6-PC regional factor stripping", {"s1_innov": "pca6"}),
    ("S1 class-mean log-ratio innovations", {"s1_innov": "ref_log"}),
    ("S1 class-mean linear-diff innovations", {"s1_innov": "ref_diff"}),
    ("S1 annual-only 4-site k_ord", {"s1_kord": "annual_only"}),
    ("S1 unweighted mean k_ord", {"s1_kord": "mean_ratio"}),
    ("S1 median order-stat scaling", {"s1_kord": "median"}),
    ("S1 monthly-only order-stat scaling", {"s1_kord": "monthly_only"}),
    ("S1 uncalibrated unit k_ord (1.0)", {"s1_kord": "unit"}),
    ("Q15 held constant at hourly peak Q", {"q15_rule": "const_q"}),
    ("Q15 scaled at constant peak-hour PF", {"q15_rule": "const_pf"}),
    ("S2 corridor anchor over winter", {"s2_anchor": "winter"}),
    ("S2 corridor anchor over full year", {"s2_anchor": "full_year"}),
    ("S2 coupled solve using M_bar (1-step)", {"s2_solve": "mbar_only"}),
    ("S2 voltage drop using measured V_lv", {"s2_vscale": "vlv"}),
    ("S2 peak Q from top-5 mean", {"s2_peak_agg": "top5"}),
    ("S3 bus-sag slope over winter hours", {"s3_est": "lin_slope_win"}),
    ("S3 bus-sag slope over heating season", {"s3_est": "lin_slope_heat"}),
    ("S3 bus-sag slope on hourly diffs", {"s3_est": "diff_slope"}),
    ("S3 hybrid AMI-subtracted bus-sag slope", {"s3_est": "ami_plus_vbus_resid"}),
    ("S3 PT intercept + top-10 inversion", {"s3_est": "intercept_top10"}),
    ("S3 tan_phi_u calibrated on winter hours", {"s3_cal_win": "winter"}),
    ("cross: all-year S1 + winter S2 + diff S3", {"s1_months": "all", "s2_anchor": "winter", "s3_est": "diff_slope"}),
]


def _agg_components(res):
    return (sum(res[s]["p15"] for s in TARGETS),
            sum(res[s]["q_h"] for s in TARGETS),
            100.0 * float(np.mean([res[s]["w_max"] for s in TARGETS])))


def _band(x):
    return 2 if x >= LINE_P1 else (1 if x >= LINE_P2 else 0)


def _bname(x):
    return "P1" if x >= LINE_P1 else ("P2" if x >= LINE_P2 else "Def")


def build_spec(world=None):
    """Build the corelib specification dictionary on either simulated world or disk-loaded pack_world."""
    world = world or simulate()
    gold_res, ref_p = evaluate(world, {})
    dir_res, _ = evaluate(world, DIRECT)
    rig_res, _ = evaluate(world, RIGOROUS)
    frt_res, _ = evaluate(world, FRONTIER_COMBO)
    fam_res = [evaluate(world, o)[0] for _, o in FAMILY]

    sids = ("S1", "S2", "S3")
    lat_res = {}
    for n in (1, 2, 3):
        for combo in itertools.combinations(sids, n):
            o = {}
            for s in combo:
                o.update(HURRIED[s])
            lat_res["+".join(combo)] = evaluate(world, o)[0]

    def _ref_mae(res):
        return float(np.mean([abs(res[r]["loading_pct"] - world["subs"][r]["truth"]["loading_pct"]) for r in REFS]))

    rivals = {
        "direct": dir_res,
        "rigorous": rig_res,
        "frontier_combo": frt_res,
        "s1_scada60": lat_res["S1"],
        "s1_linear_sum": evaluate(world, {"s1_mode": "linear_sum"})[0],
        "s1_rigorous_cf60": evaluate(world, {"s1_mode": "rigorous_cf60"})[0],
        "s1_cf_pooled": evaluate(world, {"s1_mode": "cf_pooled"})[0],
        "s1_flat_ratio": evaluate(world, {"s1_mode": "flat_ratio"})[0],
        "s1_class_ols": evaluate(world, {"s1_mode": "class_ols"})[0],
        "s1_indep_quad": evaluate(world, {"s1_mode": "indep_quad"})[0],
        "s1_raw_corr": evaluate(world, {"s1_mode": "raw_corr"})[0],
        "s2_net_kvarh": lat_res["S2"],
        "s2_class_pf": evaluate(world, {"s2_mode": "class_nominal"})[0],
        "s2_local_dv": evaluate(world, {"s2_mode": "local_dv"})[0],
        "s2_rp_only": evaluate(world, {"s2_mode": "rp_only"})[0],
        "s2_raw_dv_no_demean": evaluate(world, {"s2_mode": "raw_dv_no_demean"})[0],
        "s3_gis_phase": lat_res["S3"],
        "s3_ami_only_bal": evaluate(world, {"s3_mode": "ami_only_bal"})[0],
        "s3_ami_grossup": evaluate(world, {"s3_mode": "ami_grossup"})[0],
        "s3_ami_plus_gis": evaluate(world, {"s3_mode": "ami_plus_gis"})[0],
        "s3_raw_vbus_no_pt": evaluate(world, {"s3_mode": "raw_vbus_no_pt"})[0],
    }

    members = {
        s: {
            "lines": [LINE_P2, LINE_P1],
            "truth": world["subs"][s]["truth"]["loading_pct"],
            "golden": gold_res[s]["loading_pct"],
            "family": [fr[s]["loading_pct"] for fr in fam_res],
            "routes": {"direct": dir_res[s]["loading_pct"], "rigorous": rig_res[s]["loading_pct"]},
        } for s in TARGETS
    }
    lattice = {k: {s: r[s]["loading_pct"] for s in TARGETS} for k, r in lat_res.items()}
    g_c1, g_c2, g_c3 = _agg_components(gold_res)
    f_c1, f_c2, f_c3 = zip(*[_agg_components(fr) for fr in fam_res])
    r_c1, r_c2, r_c3 = _agg_components(rig_res)
    l_c = {k: _agg_components(r) for k, r in lat_res.items()}
    figures = [
        {"id": "C1_total_p15_mw", "block": "component", "golden": g_c1, "family": list(f_c1),
         "lattice": {k: l_c[k][0] for k in lat_res}, "routes": {"rigorous": r_c1}},
        {"id": "C2_total_qpeak_mvar", "block": "component", "golden": g_c2, "family": list(f_c2),
         "lattice": {k: l_c[k][1] for k in lat_res}, "routes": {"rigorous": r_c2}},
        {"id": "C3_mean_lim_phase_pct", "block": "component", "golden": g_c3, "family": list(f_c3),
         "lattice": {k: l_c[k][2] for k in lat_res}, "routes": {"rigorous": r_c3}},
    ]
    for s in TARGETS:
        figures.append({"id": f"Load_{s}", "block": "ask", "member": s})
    for s in TARGETS:
        figures.append({"id": f"MVA_{s}", "block": "ask", "golden": gold_res[s]["lim_mva"],
                        "family": [fr[s]["lim_mva"] for fr in fam_res],
                        "lattice": {k: lat_res[k][s]["lim_mva"] for k in lat_res},
                        "routes": {"rigorous": rig_res[s]["lim_mva"]}})
    figures.append({"id": "Total_Relief_MVA", "block": "ask",
                    "golden": sum(gold_res[s]["relief_mva"] for s in TARGETS),
                    "family": [sum(fr[s]["relief_mva"] for s in TARGETS) for fr in fam_res],
                    "lattice": {k: sum(lat_res[k][s]["relief_mva"] for s in TARGETS) for k in lat_res},
                    "routes": {"rigorous": sum(rig_res[s]["relief_mva"] for s in TARGETS)}})

    spec = {
        "task": "task26: Vesterdal Nett 66/22 kV substation relief schedule (v2)",
        "call": "lines",
        "members": members,
        "stumps": {
            "S1": {
                "axis": "unit", "opens": "Drangvik", "steps_left": 4, "precedents": ["L22", "L40"],
                "said_out_loud": "Hourly SCADA smooths 15-min bursts and feeder registers lack timestamps or zone labels; strip regional diurnal+weather common mode to infer stochastic feeder correlation R_ij and combine in correlated quadrature.",
            },
            "S2": {
                "axis": "what", "opens": "Kvernholm", "steps_left": 5, "precedents": ["L38", "L44"],
                "said_out_loud": "Substation HV voltages are unmeasured and capacitors cancel peak lagging Q in monthly net kVARh; solve simultaneous coupled 66 kV corridor impedance systems from GSPs demeaned against monthly net kVARh.",
            },
            "S3": {
                "axis": "who", "opens": "Raudfjord", "steps_left": 4, "precedents": ["L28", "L39"],
                "said_out_loud": "GIS phase tags drifted and AMI covers only 20 of 36 single-phase laterals while non-AMI legacy laterals carry distinct skew; invert total phase share from PT-free 3-phase LV bus voltage-sag slope calibrated on modernized sites.",
            },
        },
        "lattice": lattice,
        "referee": {
            "slice": "Four modernized non-target reference substations (Fossheim, Lindberg, Ostervik, Solberg)",
            "covers_target": False,
            "truth": 0.0,
            "golden": _ref_mae(gold_res),
            "rivals": {k: _ref_mae(v) for k, v in rivals.items()},
        },
        "figures": figures,
    }
    return spec, world, gold_res, lat_res, dir_res, rig_res, ref_p, rivals


def main():
    detail = "--detail" in sys.argv
    forcing = "--forcing" in sys.argv
    spec, world, gold_res, lat_res, dir_res, rig_res, ref_p, rivals = build_spec()
    rc = corelib.run(spec)
    if detail:
        print(f"\nSEED={SEED} | tan_phi_u={ref_p['tan_phi_u']:.4f} k_ord={ref_p['k_ord']:.4f} dq_dp={ref_p['dq_dp']:.4f}")
        print("\n=== ALL SUBSTATIONS (TRUTH vs GOLDEN vs FRONTIER_COMBO) ===")
        frt_res = rivals["frontier_combo"]
        for s in ALL_SUBS:
            tr, g, fc = world["subs"][s]["truth"], gold_res[s], frt_res[s]
            print(f"  {s:10s}: truth={tr['loading_pct']:5.1f}%({_bname(tr['loading_pct']):3s}) gold={g['loading_pct']:5.1f}%({_bname(g['loading_pct']):3s}) "
                  f"frontier={fc['loading_pct']:5.1f}%({_bname(fc['loading_pct']):3s}) | "
                  f"P15={g['p15']:5.2f}({tr['p15_peak']:5.2f}) Q={g['q_h']:5.2f}({tr['q_peak_h']:5.2f}) w={100*g['w_max']:4.1f}%({100*tr['w_max']:4.1f}%)")
        print("\n=== ALL 21 RIVAL ROUTES ON 4-SITE REFEREE & TARGET SCHEDULE ===")
        gmae = spec["referee"]["golden"]
        gcall = tuple(_band(gold_res[s]["loading_pct"]) for s in TARGETS)
        print(f"  {'golden':20s}: MAE={gmae:5.2f} ( 1.0x)  rel={sum(gold_res[s]['relief_mva'] for s in TARGETS):5.2f}  "
              + " ".join(f"{s[:4]}={_bname(gold_res[s]['loading_pct'])}" for s in TARGETS))
        for k, r in sorted(rivals.items(), key=lambda kv: spec["referee"]["rivals"][kv[0]]):
            m = spec["referee"]["rivals"][k]
            rcall = tuple(_band(r[s]["loading_pct"]) for s in TARGETS)
            n_wrong = sum(a != b for a, b in zip(gcall, rcall))
            print(f"  {k:20s}: MAE={m:5.2f} ({m/gmae:4.1f}x)  rel={sum(r[s]['relief_mva'] for s in TARGETS):5.2f}  wrong={n_wrong}/7  "
                  + " ".join(f"{s[:4]}={_bname(r[s]['loading_pct'])}" for s in TARGETS))
    if forcing:
        gcall = tuple(_band(gold_res[s]["loading_pct"]) for s in TARGETS)
        print("\n=== FORCING (+/-20%) ===")
        all_hold = True
        for lbl, o in [
            ("k_ord -20%", {"mult_kord": 0.80}), ("k_ord +20%", {"mult_kord": 1.20}),
            ("Q_peak -20%", {"mult_q": 0.80}), ("Q_peak +20%", {"mult_q": 1.20}),
            ("w_ex -20%", {"mult_w_excess": 0.80}), ("w_ex +20%", {"mult_w_excess": 1.20}),
        ]:
            pr, _ = evaluate(world, o)
            ok = tuple(_band(pr[s]["loading_pct"]) for s in TARGETS) == gcall
            all_hold &= ok
            print(f"  {lbl:14s}: {'HOLD' if ok else 'MOVE'}  " + " ".join(f"{s[:4]}={pr[s]['loading_pct']:.1f}" for s in TARGETS))
        print("FORCING:", "PASS" if all_hold else "FAIL")
        if not all_hold:
            rc = 1
    sys.exit(rc)


if __name__ == "__main__":
    main()
