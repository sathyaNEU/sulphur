#!/usr/bin/env python3
"""task26 architecture 1, the core: Vesterdal Nett AS 66/22 kV substation 2027-2029 relief schedule.

Vesterdal Nett AS schedules firm-capacity relief across seven 66/22 kV distribution substations (Drangvik, Hestmark,
Kvernholm, Malmnes, Raudfjord, Svarthaug, Tverrli) against two planning lines: 85% of Firm N-1 MVA rating (Phase 2,
2028-2029 staged relief) and 100% of Firm N-1 MVA rating (Phase 1, 2027 urgent relief). No single record holds each
substation's 2026 peak 15-minute limiting-phase equivalent apparent load (MVA):

  S1 (unit)  Substation and feeder SCADA archive 60-minute fixed-clock energy blocks (:00-:00), while feeder demand
             registers hold monthly non-coincident 15-minute peak MW without timestamps. Sub-hourly surges across
             independent feeders aggregate in quadrature (not by hourly coincidence factor), whereas shared-park
             industrial feeders correlate inside the hour.
  S2 (what)  Monthly revenue meters hold only net kVARh, where nighttime leading shunt-capacitor injection cancels
             winter-peak lagging motor/heat-pump reactive demand (making monthly PF look ~0.99). Hourly HV/LV bus
             voltages and LTC tap steps across transformer impedance (R_T, X_T) recover diurnal Q(t) once demeaned
             against monthly net kVARh to eliminate each substation's PT voltage offset.
  S3 (who)   Transformer thermal limits bind on the heaviest-loaded phase (3 * max phase load). GIS phase tags for
             single-phase laterals have drifted (~24% error across all substations after years of storm re-phasing),
             and residential vs commercial laterals peak at different hours. Common-mode-rejected lateral-to-bus
             voltage differentials (controlling for local lateral load drop) recover each lateral's physical phase.

Two modernized substations (Lindberg, Ostervik) with continuous 15-minute three-phase revenue PQ metering and a 2025
field phase-tracer commissioning survey serve as the referee slice and are outside the 2027-2029 capital pool.

Run:  python3 task26/generator/core.py            corelib verdict
      python3 task26/generator/core.py --detail   world, routes, referee, and variants
      python3 task26/generator/core.py --forcing  perturbation forcing table
"""
import itertools
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".claude", "skills", "stumping"))
import corelib  # noqa: E402

SEED = int(os.environ.get("CORE_SEED", 2617))
N_DAYS = 365
N_HOURS = N_DAYS * 24           # 8,760 hours in 2026
N_QH = N_HOURS * 4              # 35,040 quarter-hours (15-min ISPs)
V_NOM_LV = 22.0                 # 22 kV secondary distribution bus
V_NOM_HV = 66.0                 # 66 kV sub-transmission bus
TAP_STEP = 0.0125               # 1.25% per LTC tap step
LINE_P2 = 85.0                  # % of Firm N-1 MVA -> Phase 2 (2028-2029)
LINE_P1 = 100.0                 # % of Firm N-1 MVA -> Phase 1 (2027 urgent)

MONTH_DAYS = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
HOUR_MONTH = np.concatenate([np.full(d * 24, m, dtype=int) for m, d in enumerate(MONTH_DAYS)])
WINTER_MONTHS = (0, 1, 10, 11)
WINTER_HOURS = np.isin(HOUR_MONTH, WINTER_MONTHS)
HEATING_MONTHS = (0, 1, 2, 9, 10, 11)
HEATING_HOURS = np.isin(HOUR_MONTH, HEATING_MONTHS)

TARGETS = ("Drangvik", "Hestmark", "Kvernholm", "Malmnes", "Raudfjord", "Svarthaug", "Tverrli")
REFS = ("Lindberg", "Ostervik")
ALL_SUBS = TARGETS + REFS

# Substation physical & network parameters (realistic Norwegian 66/22 kV zone substations)
SUB_CFG = {
    # S1-opened (diverse spiky): 6 independent spiky feeders -> quadrature lift ~+13%;
    # Golden ~92% (Phase 2); S1 lost (60m) drops to ~81% (Defer); Rigorous CF60*sum(M15) jumps to ~104% (Phase 1).
    "Drangvik": dict(
        firm_mva=42.5, r_ohm=0.088, x_ohm=1.14, pt_offset_kv=0.34,
        feeders=[
            ("industrial_batch", 5.8, 0.28, 0),
            ("industrial_batch", 5.4, 0.29, 0),
            ("maritime_port",    5.6, 0.30, 0),
            ("maritime_port",    5.2, 0.27, 0),
            ("commercial_mixed", 5.0, 0.23, 0),
            ("residential_heat", 4.8, 0.15, 0),
        ],
        q_alpha=0.40, q_peak_extra=3.0, c_fixed=10.0, c_switched_peak=0.0,
        sp_share=0.58, true_ph_w=(0.390, 0.310, 0.300), gis_ph_w=(0.355, 0.325, 0.320),
    ),
    # Forced Phase 1 (high loading across EVERY route > 103%, yet moved outside band by all 3 stumps!)
    "Hestmark": dict(
        firm_mva=36.2, r_ohm=0.082, x_ohm=1.08, pt_offset_kv=-0.36,
        feeders=[
            ("industrial_batch", 14.5, 0.24, 1),
            ("industrial_batch", 12.0, 0.23, 1),
            ("commercial_mixed",  4.2, 0.12, 0),
            ("residential_heat",  3.8, 0.08, 0),
            ("residential_heat",  3.0, 0.08, 0),
        ],
        q_alpha=0.58, q_peak_extra=6.2, c_fixed=15.5, c_switched_peak=0.0,
        sp_share=0.54, true_ph_w=(0.410, 0.302, 0.288), gis_ph_w=(0.355, 0.325, 0.320),
    ),
    # S2-opened (fixed bus caps + heavy winter inductive motor/heat-pump load):
    # Monthly net kVARh ~ 0 (net PF ~0.99), class nominal PF ~0.90, true peak PF ~0.71 ->
    # Golden ~108% (Phase 1); S2 lost (net PF) drops to ~92% (Phase 2); Rigorous drops to ~97% (Phase 2).
    # S1 lost alone & S3 lost alone keep it > 101%; +/-20% forcing perturbations all HOLD Phase 1!
    "Kvernholm": dict(
        firm_mva=37.0, r_ohm=0.095, x_ohm=1.22, pt_offset_kv=0.38,
        feeders=[
            ("industrial_batch", 9.6, 0.10, 2),
            ("industrial_batch", 8.2, 0.09, 2),
            ("commercial_mixed", 6.2, 0.08, 0),
            ("residential_heat", 5.6, 0.07, 0),
        ],
        q_alpha=0.88, q_peak_extra=14.2, c_fixed=23.2, c_switched_peak=0.0,
        sp_share=0.55, true_ph_w=(0.385, 0.312, 0.303), gis_ph_w=(0.355, 0.325, 0.320),
    ),
    # S2-opened (OPPOSITE direction! modern switched capacitors + VFD commercial):
    # True peak PF ~0.985 vs class nominal PF ~0.89 -> Golden ~92% (Phase 2);
    # Direct drops <85% (Defer); Rigorous (class PF + CF60*sum(M15)) jumps >105% (Phase 1).
    "Malmnes": dict(
        firm_mva=38.0, r_ohm=0.092, x_ohm=1.18, pt_offset_kv=-0.32,
        feeders=[
            ("industrial_batch", 7.2, 0.22, 0),
            ("maritime_port",    6.8, 0.24, 0),
            ("commercial_mixed", 6.5, 0.19, 0),
            ("commercial_mixed", 6.0, 0.18, 0),
            ("residential_heat", 5.5, 0.12, 0),
        ],
        q_alpha=0.40, q_peak_extra=2.8, c_fixed=3.2, c_switched_peak=9.5,
        sp_share=0.56, true_ph_w=(0.385, 0.315, 0.300), gis_ph_w=(0.352, 0.326, 0.322),
    ),
    # S3-opened (storm-rephased unbalance hidden by balanced GIS!):
    # GIS says 35.2% max phase; true physical phase-ID shows 49.0% single-phase -> overall ~44.5%!
    # Golden ~108% (Phase 1); S3 lost (GIS) drops to ~85% (Phase 2); Rigorous drops to ~93% (Phase 2).
    # S1 lost alone & S2 lost alone keep it > 102%; +/-20% forcing perturbations all HOLD Phase 1!
    "Raudfjord": dict(
        firm_mva=36.0, r_ohm=0.102, x_ohm=1.28, pt_offset_kv=0.35,
        feeders=[
            ("residential_heat", 7.8, 0.10, 0),
            ("residential_heat", 7.2, 0.10, 0),
            ("commercial_mixed", 6.4, 0.12, 0),
            ("industrial_batch", 6.6, 0.13, 0),
        ],
        q_alpha=0.44, q_peak_extra=3.6, c_fixed=10.2, c_switched_peak=0.0,
        sp_share=0.72, true_ph_w=(0.490, 0.262, 0.248), gis_ph_w=(0.352, 0.328, 0.320),
    ),
    # S3-opened (OPPOSITE direction! field crews rebalanced laterals off Phase C, GIS still says 48%):
    # Golden ~92% (Phase 2); S3 lost (GIS) jumps to ~121% (Phase 1); Direct drops to ~82% (Defer);
    # Rigorous (GIS!) jumps to ~132% (Phase 1). S1/S2 lost stay inside 85%-100%!
    "Svarthaug": dict(
        firm_mva=33.8, r_ohm=0.098, x_ohm=1.24, pt_offset_kv=-0.34,
        feeders=[
            ("residential_heat", 8.2, 0.10, 0),
            ("residential_heat", 7.4, 0.10, 0),
            ("commercial_mixed", 7.0, 0.12, 0),
            ("industrial_batch", 6.8, 0.13, 0),
        ],
        q_alpha=0.46, q_peak_extra=3.8, c_fixed=10.8, c_switched_peak=0.0,
        sp_share=0.72, true_ph_w=(0.350, 0.330, 0.320), gis_ph_w=(0.255, 0.265, 0.480),
    ),
    # Forced Defer (low loading under EVERY route < 75%, yet all 3 stumps move its MVA outside band!)
    "Tverrli": dict(
        firm_mva=46.0, r_ohm=0.096, x_ohm=1.20, pt_offset_kv=0.32,
        feeders=[
            ("residential_heat", 6.0, 0.12, 0),
            ("commercial_mixed", 5.8, 0.15, 0),
            ("industrial_batch", 6.2, 0.22, 3),
            ("industrial_batch", 5.4, 0.21, 3),
        ],
        q_alpha=0.56, q_peak_extra=5.2, c_fixed=12.0, c_switched_peak=0.0,
        sp_share=0.64, true_ph_w=(0.420, 0.298, 0.282), gis_ph_w=(0.355, 0.325, 0.320),
    ),
    # Referee 1: modernized industrial-concentrated substation (full 15m PQ + field phase-tracer audit)
    "Lindberg": dict(
        firm_mva=54.0, r_ohm=0.080, x_ohm=1.05, pt_offset_kv=0.62,
        feeders=[
            ("industrial_batch", 15.0, 0.29, 4),
            ("industrial_batch", 13.0, 0.28, 4),
            ("commercial_mixed",  4.0, 0.10, 0),
            ("residential_heat",  3.5, 0.08, 0),
        ],
        q_alpha=0.72, q_peak_extra=9.5, c_fixed=19.2, c_switched_peak=0.0,
        sp_share=0.56, true_ph_w=(0.440, 0.288, 0.272), gis_ph_w=(0.350, 0.328, 0.322),
    ),
    # Referee 2: modernized diverse urban/maritime substation (full 15m PQ + field phase-tracer audit)
    "Ostervik": dict(
        firm_mva=48.0, r_ohm=0.086, x_ohm=1.12, pt_offset_kv=-0.62,
        feeders=[
            ("industrial_batch", 5.6, 0.14, 0),
            ("maritime_port",    5.6, 0.14, 0),
            ("maritime_port",    5.4, 0.13, 0),
            ("commercial_mixed", 5.6, 0.12, 0),
            ("residential_heat", 5.2, 0.09, 0),
            ("residential_heat", 4.8, 0.09, 0),
        ],
        q_alpha=0.68, q_peak_extra=8.8, c_fixed=15.5, c_switched_peak=0.0,
        sp_share=0.62, true_ph_w=(0.365, 0.325, 0.310), gis_ph_w=(0.445, 0.285, 0.270),
    ),
}

CLASS_NOMINAL_PF = {
    "industrial_batch": 0.87,
    "maritime_port":    0.89,
    "commercial_mixed": 0.92,
    "residential_heat": 0.95,
}
N_LATERALS = 36
RHO_PARK = 0.72
RHO_INDEP = 0.06


def _diurnal_and_season(rng):
    """Norwegian coastal 2026 temperature-driven seasonal and diurnal base shapes (8,760 hours)."""
    h = np.arange(N_HOURS)
    doy = h / 24.0
    hod = h % 24
    dow = (h // 24) % 7
    is_wkdy = (dow < 5).astype(float)

    season = 0.74 + 0.26 * np.cos(2.0 * np.pi * (doy - 18.0) / 365.0)
    cold_snap = 0.14 * np.exp(-0.5 * ((doy - 19.5) / 2.2) ** 2) + 0.11 * np.exp(-0.5 * ((doy - 341.0) / 2.5) ** 2)
    weather_ar = np.zeros(N_DAYS)
    for d in range(1, N_DAYS):
        weather_ar[d] = 0.78 * weather_ar[d - 1] + rng.normal(0.0, 0.032)
    daily_w = np.repeat(weather_ar, 24)

    res_diurn = 0.62 + 0.16 * np.exp(-0.5 * ((hod - 8.0) / 2.2) ** 2) + 0.34 * np.exp(-0.5 * ((hod - 18.0) / 2.6) ** 2)
    com_diurn = (0.48 + 0.50 * np.exp(-0.5 * ((hod - 13.0) / 3.2) ** 2)) * (0.78 + 0.22 * is_wkdy)
    ind_diurn = (0.64 + 0.34 * np.exp(-0.5 * ((hod - 16.5) / 4.0) ** 2)) * (0.86 + 0.14 * is_wkdy)
    mar_diurn = 0.60 + 0.38 * np.exp(-0.5 * ((hod - 17.0) / 3.8) ** 2)

    shapes = {
        "residential_heat": np.clip((season + cold_snap + daily_w) * res_diurn, 0.25, 1.35),
        "commercial_mixed": np.clip((0.82 + 0.18 * season + 0.6 * cold_snap + 0.5 * daily_w) * com_diurn, 0.25, 1.30),
        "industrial_batch": np.clip((0.86 + 0.14 * season + 0.5 * cold_snap + 0.4 * daily_w) * ind_diurn, 0.35, 1.30),
        "maritime_port":    np.clip((0.84 + 0.16 * season + 0.6 * cold_snap + 0.5 * daily_w) * mar_diurn, 0.30, 1.30),
    }
    for k in shapes:
        shapes[k] = shapes[k] / np.quantile(shapes[k], 0.998)
    return shapes


def simulate():
    """Simulate the full 2026 physical grid (15-min P, hourly Q, HV/LV voltages & taps, lateral voltages & phases)."""
    rng = np.random.default_rng([SEED, 1])
    shapes = _diurnal_and_season(rng)
    world = {"subs": {}, "shapes": shapes}

    v_tx_common = V_NOM_HV * (1.015 - 0.018 * (shapes["residential_heat"] - 0.7) + rng.normal(0.0, 0.004, N_HOURS))

    for s_idx, s in enumerate(ALL_SUBS):
        cfg = SUB_CFG[s]
        srng = np.random.default_rng([SEED, 100, s_idx])
        n_f = len(cfg["feeders"])

        sub_common_q = srng.normal(0.0, 1.0, (N_HOURS, 4))
        sub_common_q -= sub_common_q.mean(axis=1, keepdims=True)
        park_groups = sorted({g for (_, _, _, g) in cfg["feeders"] if g > 0})
        park_shocks = {}
        for g in park_groups:
            z = srng.normal(0.0, 1.0, (N_HOURS, 4))
            z -= z.mean(axis=1, keepdims=True)
            park_shocks[g] = z

        f_p15 = np.zeros((n_f, N_HOURS, 4))
        f_p60 = np.zeros((n_f, N_HOURS))
        f_meta = []
        for f_i, (fcls, peak_mw, cv_sub, pgrp) in enumerate(cfg["feeders"]):
            f_noise = np.exp(srng.normal(0.0, 0.025, N_HOURS))
            p60 = peak_mw * shapes[fcls] * f_noise
            z_ind = srng.normal(0.0, 1.0, (N_HOURS, 4))
            z_ind -= z_ind.mean(axis=1, keepdims=True)
            if pgrp > 0:
                z_tot = np.sqrt(RHO_PARK) * park_shocks[pgrp] + np.sqrt(1.0 - RHO_PARK) * z_ind
            else:
                z_tot = np.sqrt(RHO_INDEP) * sub_common_q + np.sqrt(1.0 - RHO_INDEP) * z_ind
            # Bounded physical duty-cycle burst (equipment cannot exceed motor/crane nameplate rating!)
            z_tot = np.tanh(z_tot / 1.9) * 1.9
            z_tot -= z_tot.mean(axis=1, keepdims=True)
            z_tot = z_tot / np.std(z_tot)
            burst = cv_sub * 0.56 * p60[:, None] * z_tot
            burst -= burst.mean(axis=1, keepdims=True)
            p15 = np.maximum(0.1 * p60[:, None], p60[:, None] + burst)
            p60_exact = p15.mean(axis=1)
            f_p15[f_i] = p15
            f_p60[f_i] = p60_exact
            f_meta.append(dict(feeder_id=f"{s[:3].upper()}-F{f_i+1:02d}", fcls=fcls,
                               peak_mw=peak_mw, cv_sub=cv_sub, park_group=pgrp))

        sub_p15 = f_p15.sum(axis=0)            # (N_HOURS, 4)
        sub_p60 = sub_p15.mean(axis=1)         # (N_HOURS,)
        peak_h_p15 = int(np.argmax(sub_p15.max(axis=1)))
        peak_q_idx = int(np.argmax(sub_p15[peak_h_p15]))
        true_p15_peak = float(sub_p15[peak_h_p15, peak_q_idx])
        peak_h_p60 = int(np.argmax(sub_p60))
        scada_p60_peak = float(sub_p60[peak_h_p60])

        # Reactive power Q(h) and 15-min Q15(h, q)
        p_norm = sub_p60 / np.quantile(sub_p60, 0.995)
        peak_ind_term = cfg["q_peak_extra"] * np.maximum(0.0, (p_norm - 0.55) / 0.45) ** 1.4
        sw_on = 1.0 / (1.0 + np.exp(-25.0 * (p_norm - 0.68)))
        q_hourly = (cfg["q_alpha"] * sub_p60 + peak_ind_term
                    - cfg["c_fixed"] - cfg["c_switched_peak"] * sw_on
                    + srng.normal(0.0, 0.22, N_HOURS))
        dp15 = sub_p15 - sub_p60[:, None]
        q_15 = q_hourly[:, None] + 0.30 * dp15
        true_q_peak_h = float(q_hourly[peak_h_p15])
        true_q15_at_peak = float(q_15[peak_h_p15, peak_q_idx])

        sub_s15 = np.sqrt(sub_p15 ** 2 + q_15 ** 2)
        s_peak_flat = int(np.argmax(sub_s15))
        s_peak_h, s_peak_q = divmod(s_peak_flat, 4)
        true_s15_tot = float(sub_s15[s_peak_h, s_peak_q])

        # Hourly HV/LV bus voltages and LTC taps
        v_hv = v_tx_common + srng.normal(0.0, 0.12, N_HOURS)
        dv_phys = (cfg["r_ohm"] * sub_p60 + cfg["x_ohm"] * q_hourly) / V_NOM_LV
        ideal_ratio = (22.35 + dv_phys) / v_hv
        nom_ratio = V_NOM_LV / V_NOM_HV
        tap_step_int = np.clip(np.round(((ideal_ratio / nom_ratio) - 1.0) / TAP_STEP), -8, 8).astype(int)
        tau = nom_ratio * (1.0 + TAP_STEP * tap_step_int)
        v_lv_true = v_hv * tau - dv_phys
        v_hv_meas = v_hv + srng.normal(0.0, 0.014, N_HOURS)
        v_lv_meas = v_lv_true - cfg["pt_offset_kv"] + srng.normal(0.0, 0.012, N_HOURS)

        # Per-phase bus voltages & 36 single-phase laterals
        u_raw = srng.normal(0.0, 0.14, (3, N_HOURS))
        for ph in range(3):
            for t in range(1, N_HOURS):
                u_raw[ph, t] = 0.55 * u_raw[ph, t - 1] + 0.835 * u_raw[ph, t]
        u_diff = u_raw - u_raw.mean(axis=0, keepdims=True)
        v_bus_ph = v_lv_meas[None, :] + u_diff

        n_true = [int(round(N_LATERALS * w)) for w in cfg["true_ph_w"]]
        n_true[2] = N_LATERALS - n_true[0] - n_true[1]
        ph_list = [0] * n_true[0] + [1] * n_true[1] + [2] * n_true[2]
        srng.shuffle(ph_list)
        lat_true_ph = np.array(ph_list, dtype=int)

        n_gis = [int(round(N_LATERALS * w)) for w in cfg["gis_ph_w"]]
        n_gis[2] = N_LATERALS - n_gis[0] - n_gis[1]
        lat_gis_ph = lat_true_ph.copy()
        for ph_from in range(3):
            while int((lat_gis_ph == ph_from).sum()) > n_gis[ph_from]:
                need = [p for p in range(3) if int((lat_gis_ph == p).sum()) < n_gis[p]]
                cands = np.where(lat_gis_ph == ph_from)[0]
                lat_gis_ph[int(srng.choice(cands))] = need[0]
        cur_mis = int((lat_gis_ph != lat_true_ph).sum())
        if cur_mis < 8:
            same_by_ph = {p: list(np.where((lat_gis_ph == p) & (lat_true_ph == p))[0]) for p in range(3)}
            while cur_mis < 8 and all(len(same_by_ph[p]) >= 1 for p in range(3)):
                ia, ib, ic = same_by_ph[0].pop(), same_by_ph[1].pop(), same_by_ph[2].pop()
                lat_gis_ph[ia], lat_gis_ph[ib], lat_gis_ph[ic] = 1, 2, 0
                cur_mis += 3

        sp_total_kw = cfg["sp_share"] * sub_p60 * 1000.0
        raw_lat = np.zeros((N_LATERALS, N_HOURS))
        lat_cls = []
        for l_i in range(N_LATERALS):
            lcls = "residential_heat" if (l_i % 3 != 0) else "commercial_mixed"
            lat_cls.append(lcls)
            base_sz = srng.lognormal(0.0, 0.18)
            raw_lat[l_i] = base_sz * shapes[lcls] * np.exp(srng.normal(0.0, 0.035, N_HOURS))
        for ph in range(3):
            idx = np.where(lat_true_ph == ph)[0]
            cur_at_pk = raw_lat[idx, s_peak_h].sum()
            raw_lat[idx] *= (cfg["true_ph_w"][ph] * sp_total_kw[s_peak_h]) / cur_at_pk
        lat_p_hourly = raw_lat * (sp_total_kw / raw_lat.sum(axis=0))[None, :]

        lat_v_hourly = np.zeros((N_LATERALS, N_HOURS))
        for l_i in range(N_LATERALS):
            ph = lat_true_ph[l_i]
            r_lat = srng.uniform(0.008, 0.018)
            lat_v_hourly[l_i] = (230.0 / V_NOM_LV) * v_bus_ph[ph] - r_lat * lat_p_hourly[l_i] + srng.normal(0.0, 0.28, N_HOURS)

        bal_3ph_kw = (1.0 - cfg["sp_share"]) * sub_p60 * 1000.0
        true_ph_kw_at_pk = np.array([lat_p_hourly[lat_true_ph == ph, s_peak_h].sum() + bal_3ph_kw[s_peak_h] / 3.0
                                     for ph in range(3)])
        true_w_max = float(true_ph_kw_at_pk.max() / true_ph_kw_at_pk.sum())
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
            v_hv_meas=v_hv_meas, v_lv_meas=v_lv_meas, tap_step_int=tap_step_int,
            v_bus_ph=v_bus_ph, lat_gis_ph=lat_gis_ph, lat_cls=lat_cls,
            lat_p_hourly=lat_p_hourly, lat_v_hourly=lat_v_hourly,
            f_p15=f_p15, sub_p15=sub_p15, q_hourly=q_hourly, q_15=q_15, sub_s15=sub_s15,
            lat_true_ph=lat_true_ph,
            truth=dict(
                p15_peak=true_p15_peak, p60_peak=scada_p60_peak,
                q_peak_h=true_q_peak_h, q15_at_peak=true_q15_at_peak,
                s15_tot=true_s15_tot, w_max=true_w_max,
                lim_mva=true_lim_mva, loading_pct=true_loading_pct,
                relief_mva=max(0.0, true_lim_mva - 0.85 * cfg["firm_mva"]),
                s_peak_h=s_peak_h,
            ),
        )
    return world


def _raw_quad_excess_month(sd, rho_park, rho_indep, m_list, form="mult"):
    """Correlated quadrature of feeder intra-hour excesses (MW) evaluated at peak hour of m_list."""
    n_f = len(sd["f_meta"])
    hm_all = np.isin(HOUR_MONTH, m_list)
    idx_h = np.where(hm_all)[0]
    p60_pk_h = int(idx_h[np.argmax(sd["sub_p60"][idx_h])])
    deltas = np.zeros(n_f)
    for i in range(n_f):
        if form == "mult":
            rel = float(np.mean([(sd["feeder_m15"][i, m] - sd["feeder_p60_m"][i, m]) / sd["feeder_p60_m"][i, m]
                                 for m in m_list]))
            deltas[i] = max(0.0, rel) * float(sd["f_p60"][i, p60_pk_h])
        else:
            ex_m = float(np.mean([sd["feeder_m15"][i, m] - sd["feeder_p60_m"][i, m] for m in m_list]))
            scale = float(sd["f_p60"][i, p60_pk_h]) / float(np.mean([sd["feeder_p60_m"][i, m] for m in m_list]))
            deltas[i] = max(0.0, ex_m * scale)
    var_sum = 0.0
    for i in range(n_f):
        var_sum += deltas[i] ** 2
        for j in range(i + 1, n_f):
            gi, gj = sd["f_meta"][i]["park_group"], sd["f_meta"][j]["park_group"]
            rho = rho_park if (gi > 0 and gi == gj) else rho_indep
            var_sum += 2.0 * rho * deltas[i] * deltas[j]
    return float(np.sqrt(max(0.0, var_sum)))


def _fit_ref_params(world, opts):
    """Estimate sub-hourly correlation, order-stat scaling, and dQ/dP from the two modernized reference substations."""
    win_mask = WINTER_HOURS if opts.get("s1_months", "winter") == "winter" else np.ones(N_HOURS, dtype=bool)
    park_corrs, indep_corrs, dq_dp_list = [], [], []

    for r in REFS:
        sd = world["subs"][r]
        n_f = len(sd["f_meta"])
        dp_f = sd["f_p15"][:, win_mask, :] - sd["f_p60"][:, win_mask, None]
        corr = np.corrcoef(dp_f.reshape(n_f, -1))
        for i in range(n_f):
            for j in range(i + 1, n_f):
                gi, gj = sd["f_meta"][i]["park_group"], sd["f_meta"][j]["park_group"]
                (park_corrs if (gi > 0 and gi == gj) else indep_corrs).append(float(corr[i, j]))
        dp_sub = (sd["sub_p15"][win_mask, :] - sd["sub_p60"][win_mask, None]).ravel()
        dq_sub = (sd["q_15"][win_mask, :] - sd["q_hourly"][win_mask, None]).ravel()
        dq_dp_list.append(float(np.dot(dp_sub, dq_sub) / np.dot(dp_sub, dp_sub)))

    rho_park = float(np.mean(park_corrs))
    rho_indep = float(np.median(indep_corrs)) if opts.get("s1_pool_rho") else float(np.mean(indep_corrs))
    dq_dp = float(np.mean(dq_dp_list))

    # Calibrate order-statistic ratio k_ord across peaks on REFS (MW-weighted ratio of sums by default)
    cal_months = list(WINTER_MONTHS) if opts.get("s1_months", "winter") == "winter" else list(range(12))
    form = opts.get("s1_form", "mult")
    obs_list, raw_list, ratios = [], [], []
    for r in REFS:
        sd = world["subs"][r]
        for m in cal_months:
            hm = HOUR_MONTH == m
            obs_ex = float(sd["sub_p15"][hm, :].max() - sd["sub_p60"][hm].max())
            raw_q = _raw_quad_excess_month(sd, rho_park, rho_indep, [m], form=form)
            if raw_q > 1e-6:
                obs_list.append(obs_ex)
                raw_list.append(raw_q)
                ratios.append(obs_ex / raw_q)
        # Also include the annual peak calibration pair on each reference substation
        obs_ann = float(sd["sub_p15"].max() - sd["sub_p60"].max())
        raw_ann = _raw_quad_excess_month(sd, rho_park, rho_indep, cal_months, form=form)
        if raw_ann > 1e-6:
            obs_list.append(obs_ann)
            raw_list.append(raw_ann)
            ratios.append(obs_ann / raw_ann)
    if opts.get("s1_kord") == "median":
        k_ord = float(np.median(ratios))
    elif opts.get("s1_kord") == "monthly_only":
        # Exclude the 2 annual rows (every (len(cal_months)+1)-th entry)
        step = len(cal_months) + 1
        mo_o = [v for idx, v in enumerate(obs_list) if (idx + 1) % step != 0]
        mo_r = [v for idx, v in enumerate(raw_list) if (idx + 1) % step != 0]
        k_ord = float(sum(mo_o) / sum(mo_r))
    else:
        k_ord = float(sum(obs_list) / sum(raw_list))
    flat_ratio = float(np.mean([sd["sub_p15"].max() / sd["sub_p60"].max() for sd in (world["subs"][r] for r in REFS)]))
    return dict(rho_park=rho_park, rho_indep=rho_indep, k_ord=k_ord, dq_dp=dq_dp, flat_ratio=flat_ratio)


def _estimate_s1(sd, ref_p, opts):
    mode = opts.get("s1_mode", "golden")
    p60_pk = float(sd["sub_p60"].max())
    if mode == "scada60":
        return p60_pk
    if mode == "flat_ratio":
        return p60_pk * ref_p["flat_ratio"]
    if mode == "rigorous_cf60":
        cf60 = p60_pk / float(sd["f_p60"].max(axis=1).sum())
        return cf60 * float(sd["feeder_m15"].max(axis=1).sum())
    months_opt = opts.get("s1_months", "winter")
    if months_opt == "winter":
        m_list = list(WINTER_MONTHS)
    elif months_opt == "all":
        m_list = list(range(12))
    else:
        pk_h = int(np.argmax(sd["sub_p60"]))
        m_list = [int(HOUR_MONTH[pk_h])]
    raw_q = _raw_quad_excess_month(sd, ref_p["rho_park"], ref_p["rho_indep"], m_list, form=opts.get("s1_form", "mult"))
    return p60_pk + ref_p["k_ord"] * raw_q


def _estimate_s2(sd, opts):
    mode = opts.get("s2_mode", "golden")
    cfg = sd["cfg"]
    p60 = sd["sub_p60"]
    pk_h = int(np.argmax(p60))
    pk_m = int(HOUR_MONTH[pk_h])
    p_pk = float(p60[pk_h])

    if mode == "net_kvarh":
        e_p = float(sd["sub_kwh_m"].sum())
        e_q = float(sd["sub_net_kvarh_m"].sum())
        pf = e_p / np.sqrt(e_p ** 2 + e_q ** 2)
        return float(p_pk * np.tan(np.arccos(np.clip(pf, 0.5, 0.9999))) * (1.0 if e_q >= 0 else -1.0))
    if mode == "class_nominal":
        q_sum = 0.0
        for i, fm in enumerate(sd["f_meta"]):
            pf_c = CLASS_NOMINAL_PF[fm["fcls"]]
            q_sum += float(sd["f_p60"][i, pk_h]) * np.tan(np.arccos(pf_c))
        return float(q_sum)
    if mode == "raw_dv_no_demean":
        tau = (V_NOM_LV / V_NOM_HV) * (1.0 + TAP_STEP * sd["tap_step_int"])
        dv = sd["v_hv_meas"] * tau - sd["v_lv_meas"]
        q_hat = (V_NOM_LV * dv - cfg["r_ohm"] * p60) / cfg["x_ohm"]
        top5 = np.argsort(p60)[-5:]
        return float(np.mean(q_hat[top5]))

    tau = (V_NOM_LV / V_NOM_HV) * (1.0 + TAP_STEP * sd["tap_step_int"])
    dv = sd["v_hv_meas"] * tau - sd["v_lv_meas"]
    v_scale = sd["v_lv_meas"] if opts.get("s2_vscale") == "vlv" else V_NOM_LV
    q_uncal = (v_scale * dv - cfg["r_ohm"] * p60) / cfg["x_ohm"]

    win_anchor = opts.get("s2_anchor", "peak_month")
    if win_anchor == "peak_month":
        hm = HOUR_MONTH == pk_m
        q_bar_net = float(sd["sub_net_kvarh_m"][pk_m]) / (1000.0 * int(hm.sum()))
        q_hat = q_uncal - float(np.mean(q_uncal[hm])) + q_bar_net
    elif win_anchor == "winter":
        wm = WINTER_HOURS
        q_bar_net = float(sum(sd["sub_net_kvarh_m"][m] for m in WINTER_MONTHS)) / (1000.0 * int(wm.sum()))
        q_hat = q_uncal - float(np.mean(q_uncal[wm])) + q_bar_net
    else:
        q_bar_net = float(sd["sub_net_kvarh_m"].sum()) / (1000.0 * N_HOURS)
        q_hat = q_uncal - float(np.mean(q_uncal)) + q_bar_net

    agg = opts.get("s2_peak_agg", "top5")
    if agg == "single":
        return float(q_hat[pk_h])
    elif agg == "top5":
        top5 = np.argsort(p60)[-5:]
        return float(np.mean(q_hat[top5]))
    else:
        top50 = np.argsort(p60)[-50:]
        c = np.polyfit(p60[top50], q_hat[top50], 1)
        return float(c[0] * p_pk + c[1])


def _identify_phases(sd, opts):
    v_bus = sd["v_bus_ph"] * (230.0 / V_NOM_LV)
    v_cm = v_bus.mean(axis=0, keepdims=True)
    v_tilde = v_bus - v_cm
    use_win = WINTER_HOURS if opts.get("s3_win", "winter") == "winter" else HEATING_HOURS
    idx_h = np.where(use_win)[0]
    r_v = sd["lat_v_hourly"] - v_cm
    if opts.get("s3_diff", "diff") == "diff":
        d_vt = np.diff(v_tilde[:, idx_h], axis=1)
        d_rv = np.diff(r_v[:, idx_h], axis=1)
        d_lp = np.diff(sd["lat_p_hourly"][:, idx_h], axis=1)
    else:
        d_vt = v_tilde[:, idx_h] - v_tilde[:, idx_h].mean(axis=1, keepdims=True)
        d_rv = r_v[:, idx_h] - r_v[:, idx_h].mean(axis=1, keepdims=True)
        d_lp = sd["lat_p_hourly"][:, idx_h] - sd["lat_p_hourly"][:, idx_h].mean(axis=1, keepdims=True)

    probs = np.zeros((N_LATERALS, 3))
    for l_i in range(N_LATERALS):
        y, x_p = d_rv[l_i], d_lp[l_i]
        rss = np.zeros(3)
        for ph in range(3):
            X = np.column_stack([d_vt[ph], x_p])
            beta, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
            rss[ph] = float(np.sum(y ** 2)) if beta[0] <= 0.1 else float(np.sum((y - X @ beta) ** 2))
        if opts.get("s3_assign", "hard") == "soft":
            n_t = len(y)
            ll = -0.5 * n_t * np.log(rss / n_t)
            ll -= ll.max()
            w = np.exp(np.clip(ll, -50, 0))
            probs[l_i] = w / w.sum()
        else:
            probs[l_i, int(np.argmin(rss))] = 1.0
    return probs


def _estimate_s3(sd, opts):
    mode = opts.get("s3_mode", "golden")
    p60 = sd["sub_p60"]
    pk_h = int(np.argmax(p60))
    if mode == "balanced":
        return 1.0 / 3.0
    bal_3ph_kw = (1.0 - sd["cfg"]["sp_share"]) * p60 * 1000.0
    if mode == "gis":
        ph_ids = sd["lat_gis_ph"]
        ph_kw = np.array([sd["lat_p_hourly"][ph_ids == ph, pk_h].sum() + bal_3ph_kw[pk_h] / 3.0 for ph in range(3)])
        return float(ph_kw.max() / ph_kw.sum())
    probs = _identify_phases(sd, opts)
    if opts.get("s3_peak_agg", "top5") == "single":
        ph_kw = probs.T @ sd["lat_p_hourly"][:, pk_h] + bal_3ph_kw[pk_h] / 3.0
        return float(ph_kw.max() / ph_kw.sum())
    top5 = np.argsort(p60)[-5:]
    return float(np.mean([(probs.T @ sd["lat_p_hourly"][:, h] + bal_3ph_kw[h] / 3.0).max()
                          / (probs.T @ sd["lat_p_hourly"][:, h] + bal_3ph_kw[h] / 3.0).sum() for h in top5]))


def evaluate(world, opts=None):
    opts = opts or {}
    ref_p = _fit_ref_params(world, opts)
    m_kord = float(opts.get("mult_kord", 1.0))
    m_q = float(opts.get("mult_q", 1.0))
    m_w = float(opts.get("mult_w_excess", 1.0))
    out = {}
    for s in ALL_SUBS:
        sd = world["subs"][s]
        cfg = sd["cfg"]
        p60_pk = float(sd["sub_p60"].max())
        p15_raw = _estimate_s1(sd, ref_p, opts)
        p15 = p60_pk + m_kord * (p15_raw - p60_pk)
        q_h = _estimate_s2(sd, opts) * m_q
        q15_rule = opts.get("q15_rule", "ref_slope")
        if q15_rule == "ref_slope":
            q15 = q_h + ref_p["dq_dp"] * (p15 - p60_pk)
        elif q15_rule == "const_q":
            q15 = q_h
        else:
            q15 = q_h * (p15 / p60_pk)
        s15_tot = float(np.sqrt(p15 ** 2 + q15 ** 2))
        w_raw = _estimate_s3(sd, opts)
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
RIGOROUS = {"s1_mode": "rigorous_cf60", "s2_mode": "class_nominal", "s3_mode": "gis"}

FAMILY = [
    ("golden", {}),
    ("S1 excess on all 12 months", {"s1_months": "all"}),
    ("S1 excess on peak month only", {"s1_months": "peak_m"}),
    ("S1 additive feeder excess scaling", {"s1_form": "add"}),
    ("S1 median independent correlation", {"s1_pool_rho": True}),
    ("S1 median order-stat scaling", {"s1_kord": "median"}),
    ("S1 monthly-only order-stat scaling", {"s1_kord": "monthly_only"}),
    ("Q15 held constant at hourly peak Q", {"q15_rule": "const_q"}),
    ("Q15 scaled at constant peak-hour PF", {"q15_rule": "const_pf"}),
    ("S2 voltage drop anchored over winter", {"s2_anchor": "winter"}),
    ("S2 voltage drop anchored over full year", {"s2_anchor": "full_year"}),
    ("S2 voltage drop using measured V_lv", {"s2_vscale": "vlv"}),
    ("S2 peak Q from single peak hour", {"s2_peak_agg": "single"}),
    ("S2 peak Q from top-50 linear regression", {"s2_peak_agg": "fit50"}),
    ("S3 phase-ID on 6-month heating season", {"s3_win": "heating_6m"}),
    ("S3 phase-ID on demeaned voltage levels", {"s3_diff": "level"}),
    ("S3 phase-ID soft posterior probabilities", {"s3_assign": "soft"}),
    ("S3 peak phase share from single peak hour", {"s3_peak_agg": "single"}),
    ("cross: all-year S1 + winter S2 + 6m-heating S3", {"s1_months": "all", "s2_anchor": "winter", "s3_win": "heating_6m"}),
    ("cross: additive S1 + const_q + single-hour S2/S3", {"s1_form": "add", "q15_rule": "const_q", "s2_peak_agg": "single", "s3_peak_agg": "single"}),
    ("cross: peak-month S1 + const_pf + soft S3", {"s1_months": "peak_m", "q15_rule": "const_pf", "s3_assign": "soft"}),
]


def _agg_components(res):
    c1 = sum(res[s]["p15"] for s in TARGETS)
    c2 = sum(res[s]["q_h"] for s in TARGETS)
    c3 = 100.0 * float(np.mean([res[s]["w_max"] for s in TARGETS]))
    return c1, c2, c3


def build_spec(world=None):
    world = world or simulate()
    gold_res, ref_p = evaluate(world, {})
    dir_res, _ = evaluate(world, DIRECT)
    rig_res, _ = evaluate(world, RIGOROUS)
    fam_res = [evaluate(world, o)[0] for _, o in FAMILY]

    sids = ("S1", "S2", "S3")
    lat_res = {}
    for n in (1, 2, 3):
        for combo in itertools.combinations(sids, n):
            o = {}
            for s in combo:
                o.update(HURRIED[s])
            lat_res["+".join(combo)] = evaluate(world, o)[0]

    members = {}
    for s in TARGETS:
        members[s] = {
            "lines": [LINE_P2, LINE_P1],
            "truth": world["subs"][s]["truth"]["loading_pct"],
            "golden": gold_res[s]["loading_pct"],
            "family": [fr[s]["loading_pct"] for fr in fam_res],
            "routes": {
                "direct": dir_res[s]["loading_pct"],
                "rigorous": rig_res[s]["loading_pct"],
            },
        }

    lattice = {k: {s: r[s]["loading_pct"] for s in TARGETS} for k, r in lat_res.items()}

    def _ref_mae(res):
        return float(np.mean([abs(res[r]["loading_pct"] - world["subs"][r]["truth"]["loading_pct"]) for r in REFS]))

    ref_spec = {
        "slice": "Lindberg and Ostervik (two modernized non-target substations with continuous 15-min 3-phase PQ metering and 2025 field phase-tracer survey): mean absolute loading error (pct points)",
        "covers_target": False,
        "truth": 0.0,
        "golden": _ref_mae(gold_res),
        "rivals": {
            "direct": _ref_mae(dir_res),
            "rigorous": _ref_mae(rig_res),
            "s1_scada60": _ref_mae(lat_res["S1"]),
            "s2_net_kvarh": _ref_mae(lat_res["S2"]),
            "s3_gis_phase": _ref_mae(lat_res["S3"]),
            "s2_raw_dv_no_demean": _ref_mae(evaluate(world, {"s2_mode": "raw_dv_no_demean"})[0]),
            "s1_flat_ratio": _ref_mae(evaluate(world, {"s1_mode": "flat_ratio"})[0]),
        },
    }

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
        figures.append({
            "id": f"MVA_{s}", "block": "ask",
            "golden": gold_res[s]["lim_mva"],
            "family": [fr[s]["lim_mva"] for fr in fam_res],
            "lattice": {k: lat_res[k][s]["lim_mva"] for k in lat_res},
            "routes": {"rigorous": rig_res[s]["lim_mva"]},
        })
    figures.append({
        "id": "Total_Relief_MVA", "block": "ask",
        "golden": sum(gold_res[s]["relief_mva"] for s in TARGETS),
        "family": [sum(fr[s]["relief_mva"] for s in TARGETS) for fr in fam_res],
        "lattice": {k: sum(lat_res[k][s]["relief_mva"] for s in TARGETS) for k in lat_res},
        "routes": {"rigorous": sum(rig_res[s]["relief_mva"] for s in TARGETS)},
    })

    stumps = {
        "S1": {
            "axis": "unit",
            "opens": "Drangvik",
            "said_out_loud": "Substation SCADA archives 60-minute fixed-clock energy blocks while feeder 15-minute max-demand registers lack timestamps, and sub-hourly surges across independent feeders aggregate in quadrature rather than by hourly coincidence.",
            "steps_left": 4,
            "precedents": ["L22", "N01", "L28"],
        },
        "S2": {
            "axis": "what",
            "opens": "Kvernholm",
            "said_out_loud": "Monthly net kVARh cancels nighttime leading shunt-capacitor injection against winter-peak lagging reactive load, so hourly reactive power must be inverted from transformer HV/LV voltage drop and LTC tap steps demeaned against monthly net kVARh.",
            "steps_left": 4,
            "precedents": ["L38", "N27", "L28"],
        },
        "S3": {
            "axis": "who",
            "opens": "Raudfjord",
            "said_out_loud": "GIS single-phase lateral tags drifted after storm re-phasing, so each lateral's physical phase must be identified from common-mode-rejected AMI-to-bus voltage differentials controlling for local load drop and summed at the peak hour.",
            "steps_left": 4,
            "precedents": ["N09", "L38", "L28"],
        },
    }

    spec = {
        "task": "task26 architecture 1",
        "call": "lines",
        "members": members,
        "stumps": stumps,
        "lattice": lattice,
        "referee": ref_spec,
        "figures": figures,
    }
    return spec, world, gold_res, lat_res, dir_res, rig_res, ref_p


def _band(x):
    return 2 if x >= LINE_P1 else (1 if x >= LINE_P2 else 0)


def _band_name(x):
    return "Phase1-2027" if x >= LINE_P1 else ("Phase2-2028-29" if x >= LINE_P2 else "Defer")


def main():
    spec, world, gold_res, lat_res, dir_res, rig_res, ref_p = build_spec()
    code = corelib.run(spec)
    if "--detail" in sys.argv:
        print("\n=== REFERENCE PARAMETERS ===")
        print(ref_p)
        print("\n=== TRUTH vs GOLDEN vs ROUTES ===")
        for s in ALL_SUBS:
            tr = world["subs"][s]["truth"]
            g, d, r = gold_res[s], dir_res[s], rig_res[s]
            print(f"{s:10s}  truth={tr['loading_pct']:5.1f}% ({_band_name(tr['loading_pct']):14s})  "
                  f"gold={g['loading_pct']:5.1f}% ({_band_name(g['loading_pct']):14s})  "
                  f"dir={d['loading_pct']:5.1f}%  rig={r['loading_pct']:5.1f}%  "
                  f"| P15={g['p15']:5.2f}({tr['p15_peak']:5.2f}) "
                  f"Qh={g['q_h']:5.2f}({tr['q_peak_h']:5.2f}) "
                  f"w={100*g['w_max']:4.1f}%({100*tr['w_max']:4.1f}%)")
        print("\n=== LATTICE CALLS ===")
        for k, res in sorted(lat_res.items()):
            print(f"  {k:10s}: " + ", ".join(f"{s[:4]}={_band_name(res[s]['loading_pct'])[:6]}({res[s]['loading_pct']:.1f})" for s in TARGETS))
        print("\n=== REFEREE SLICE (Lindberg & Ostervik MAE pct pts) ===")
        print(f"  golden MAE: {spec['referee']['golden']:.3f}")
        for rk, rv in sorted(spec["referee"]["rivals"].items()):
            print(f"  {rk:22s}: {rv:.3f} ({rv/max(spec['referee']['golden'],1e-9):.1f}x golden)")
    if "--forcing" in sys.argv:
        gcall = tuple(_band(gold_res[s]["loading_pct"]) for s in TARGETS)
        print("\n=== FORCING PERTURBATIONS (+/- 20% on each fitted input) ===")
        all_hold = True
        for label, o in [
            ("k_ord -20%", {"mult_kord": 0.80}), ("k_ord +20%", {"mult_kord": 1.20}),
            ("Q_peak -20%", {"mult_q": 0.80}), ("Q_peak +20%", {"mult_q": 1.20}),
            ("phase excess -20%", {"mult_w_excess": 0.80}), ("phase excess +20%", {"mult_w_excess": 1.20}),
        ]:
            pr, _ = evaluate(world, o)
            pcall = tuple(_band(pr[s]["loading_pct"]) for s in TARGETS)
            ok = pcall == gcall
            all_hold &= ok
            print(f"  {label:20s}: {'HOLD' if ok else 'MOVE'}  " +
                  ", ".join(f"{s[:4]}={pr[s]['loading_pct']:.1f}" for s in TARGETS))
        print("FORCING:", "PASS" if all_hold else "FAIL")
        if not all_hold:
            return 1
    return code


if __name__ == "__main__":
    sys.exit(main())
