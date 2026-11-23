"""Core physical grid simulator, estimators, rival shortcuts, frontier run routes, and corelib spec for task26 (v4).

Architecture v4 (zero-in-scope-PQ physics with 3-hub autumn+winter commissioning validation):
  - Ships active-only 15-min commissioning data on 3 excluded modernized hubs across Sep, Oct, and Dec
    (pq_commissioning_2026.csv on Fossheim [11 feeders, staggered], Solberg [7 feeders, mixed], and
    Lindberg [8 feeders, synchronized]: sub_p15_mw only, no Q, no Pa/Pb/Pc, zero in-scope PQ data).
  - Bounded duty-cycle 15-min feeder pulses ensure monthly max(P_15) - max(P_60) obeys correlated quadrature
    k_ord * sqrt(d^T R d) directly with the natural register excess d_i = M_15,i - P_60,i across all 9
    commissioning site-months (< 0.6 MW MAE vs 3.5x-15x worse for every rival including twin-ratio calibration).
  - Four radial 66 kV corridors (COR-N01, COR-N02, COR-S01, COR-S02) place the four modernized hubs UPSTREAM of the
    seven relief-pool substations, so filtering excluded hubs early breaks coupled 66 kV reactive inversion.
  - S1 (unit): seasonal burst duty-cycle modulation on staggered sites inverts 12-month register correlation
    (Malmnes ~+0.90 vs Drangvik ~+0.45) and defeats 1-PC stripping, while stripping 4 regional diurnal-weather modes
    recovers exact pairwise feeder innovation correlation R_ij (~0.83 vs ~0.06) for correlated quadrature.
  - S2 (what): seasonally staged winter fixed caps on Kvernholm flatten monthly net_kvarh while peak-only (>0.85 Pmax)
    inductive loading surges to +19 MVAr; peak-only (>0.87 Pmax) switched caps on Malmnes clamp peak Q near 0 MVAr
    while off-peak winter net_kvarh rises steeply with P; defeats all monthly/local reactive proxies.
  - S3 (who): opposite-phase diurnal class skew (evening residential vs midday commercial) plus a 3.3x reactive
    impedance contrast (AMI-metered tan_phi_res = 0.125 vs tan_phi_com = 0.620 vs handbook 0.329/0.484) and a
    self-confirming 20/40 partial-AMI rollout (80/80 tracer match hiding opposite legacy skew) defeats all AMI/GIS/scalar routes.

Run:
    python3 task26/generator/core.py --detail --forcing
"""
import itertools
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, ".agents", "skills", "stumping"))
import corelib  # noqa: E402

SEED = 2635
N_DAYS = 365
N_HOURS = 8760
N_QH = N_HOURS * 4
MONTH_DAYS = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
HOUR_MONTH = np.concatenate([np.full(d * 24, m, dtype=int) for m, d in enumerate(MONTH_DAYS)])
WINTER_MONTHS = (0, 1, 10, 11)
WINTER_HOURS = np.isin(HOUR_MONTH, WINTER_MONTHS)
HEATING_MONTHS = (0, 1, 2, 9, 10, 11)
HEATING_HOURS = np.isin(HOUR_MONTH, HEATING_MONTHS)
COMM_MONTHS = (8, 9, 11)  # Sep, Oct, Dec commissioning window (autumn + winter, active-only on 3 excluded hubs!)
COMM_HOURS = np.isin(HOUR_MONTH, COMM_MONTHS)

TARGETS = ("Drangvik", "Hestmark", "Kvernholm", "Malmnes", "Raudfjord", "Svarthaug", "Tverrli")
REFS = ("Fossheim", "Lindberg", "Ostervik", "Solberg")
PQ_COMM_SITES = ("Fossheim", "Lindberg", "Solberg")
ALL_SUBS = TARGETS + REFS

V_NOM_LV = 22.0
V_NOM_HV = 66.0
TAP_STEP = 0.0125
TAP_MIN = -10
TAP_MAX = 10
LINE_P2 = 85.0
LINE_P1 = 100.0

# 40 single-phase laterals per substation: 20 AMI_SMART (12 res, 8 com) + 20 LEGACY_NON_AMI (12 res, 8 com)
N_LATERALS = 40
N_AMI_LAT = 20
N_LEG_LAT = 20

# True per-class reactive ratios for single-phase laterals (measured directly from AMI SQLite p_kw, q_kvar)
TRUE_TAN_PHI_RES = 0.125   # PF = 0.9923 (resistive Norwegian electric space heating)
TRUE_TAN_PHI_COM = 0.620   # PF = 0.8500 (inductive commercial HVAC/chillers/heat pumps)

# Engineering manual nominal PFs (handbook constants shipped in engineering_manual_class_pf.csv)
CLASS_NOMINAL_PF = {
    "residential_heat": 0.95,   # tan_phi = 0.3287
    "commercial_mixed": 0.90,   # tan_phi = 0.4843
    "industrial_batch": 0.87,
    "maritime_port":    0.88,
}

# Four radial 66 kV corridors (neutral regional IDs; modernized hubs sit UPSTREAM of relief-pool sites!)
CORRIDORS = {
    "COR-N01": {"gsp": "GSP-Nord", "segs": [
        ("GSP-Nord", "Ostervik", 13.5, 0.112, 0.370),
        ("Ostervik", "Drangvik", 10.0, 0.118, 0.375),
        ("Drangvik", "Malmnes",  10.0, 0.122, 0.380),
    ]},
    "COR-N02": {"gsp": "GSP-Nord", "segs": [
        ("GSP-Nord",  "Fossheim",  12.0, 0.112, 0.370),
        ("Fossheim",  "Raudfjord", 10.0, 0.118, 0.375),
        ("Raudfjord", "Svarthaug", 10.0, 0.122, 0.380),
    ]},
    "COR-S01": {"gsp": "GSP-Sor", "segs": [
        ("GSP-Sor",  "Lindberg",  13.5, 0.112, 0.370),
        ("Lindberg", "Hestmark",   8.5, 0.118, 0.375),
        ("Hestmark", "Kvernholm",  9.5, 0.122, 0.380),
    ]},
    "COR-S02": {"gsp": "GSP-Sor", "segs": [
        ("GSP-Sor", "Solberg", 12.0, 0.115, 0.370),
        ("Solberg", "Tverrli", 13.0, 0.122, 0.380),
    ]},
}

SUB_CFG = {
    # S1-opened (SYNCED industrial cluster, steady burstiness -> LOW 12-mo register_rho, HIGH stripped R_ij -> Phase 1 ~107.6%)
    "Drangvik": dict(
        firm_mva=45.4, r_ohm=0.088, x_ohm=1.14, pt_offset_kv=0.34, pt_ph_off=(0.16, -0.10, -0.06),
        seasonal_mod=0.0, ramp_thr=0.80,
        feeders=[
            ("industrial_batch", 5.2, 0.52, 1),
            ("industrial_batch", 5.0, 0.52, 1),
            ("industrial_batch", 4.8, 0.51, 1),
            ("maritime_port",    4.6, 0.50, 1),
            ("maritime_port",    4.4, 0.49, 1),
            ("commercial_mixed", 4.4, 0.18, 0),
            ("residential_heat", 5.2, 0.16, 0),
        ],
        q_alpha=0.42, q_peak_extra=12.8, c_fixed=4.0, c_win_fixed=2.8, c_sw_peak=0.0,
        res_ph_w=(0.56, 0.22, 0.22), com_ph_w=(0.20, 0.50, 0.30),
        ami_res_w=(0.34, 0.33, 0.33), ami_com_w=(0.34, 0.33, 0.33),
        gis_ph_w=(0.35, 0.33, 0.32),
    ),
    # Forced Phase 1 anchor (~139%)
    "Hestmark": dict(
        firm_mva=34.0, r_ohm=0.082, x_ohm=1.08, pt_offset_kv=-0.36, pt_ph_off=(-0.15, 0.11, 0.04),
        seasonal_mod=0.0, ramp_thr=0.85,
        feeders=[
            ("industrial_batch", 10.0, 0.38, 2),
            ("industrial_batch",  8.5, 0.36, 2),
            ("maritime_port",     6.5, 0.32, 0),
            ("commercial_mixed",  6.0, 0.18, 0),
            ("residential_heat",  7.5, 0.16, 0),
        ],
        q_alpha=0.45, q_peak_extra=8.0, c_fixed=4.5, c_win_fixed=2.5, c_sw_peak=0.0,
        res_ph_w=(0.60, 0.20, 0.20), com_ph_w=(0.18, 0.52, 0.30),
        ami_res_w=(0.34, 0.33, 0.33), ami_com_w=(0.34, 0.33, 0.33),
        gis_ph_w=(0.36, 0.32, 0.32),
    ),
    # S2-opened UP (peak-only >0.85 Pmax inductive surge +17.5 MVAr; c_win_fixed=2.8 flattens monthly Q_m -> Phase 1 ~108%)
    "Kvernholm": dict(
        firm_mva=31.2, r_ohm=0.092, x_ohm=1.18, pt_offset_kv=0.38, pt_ph_off=(0.14, -0.17, 0.03),
        seasonal_mod=0.30, ramp_thr=0.85,
        feeders=[
            ("industrial_batch", 6.0, 0.26, 0),
            ("maritime_port",    5.4, 0.24, 0),
            ("commercial_mixed", 5.6, 0.18, 0),
            ("commercial_mixed", 4.6, 0.18, 0),
            ("residential_heat", 6.6, 0.16, 0),
        ],
        q_alpha=0.36, q_peak_extra=17.5, c_fixed=3.5, c_win_fixed=2.8, c_sw_peak=0.0,
        res_ph_w=(0.48, 0.26, 0.26), com_ph_w=(0.30, 0.36, 0.34),
        ami_res_w=(0.34, 0.33, 0.33), ami_com_w=(0.34, 0.33, 0.33),
        gis_ph_w=(0.35, 0.33, 0.32),
    ),
    # Staggered industrial site (distinct from 11-feeder Fossheim) + peak-only (>0.87 Pmax) switched cap -> Phase 2 ~93.0%; flipped UP by S1 & S2 rivals!
    "Malmnes": dict(
        firm_mva=42.6, r_ohm=0.088, x_ohm=1.14, pt_offset_kv=-0.36, pt_ph_off=(-0.13, 0.15, -0.02),
        seasonal_mod=0.62, ramp_thr=0.85,
        feeders=[
            ("industrial_batch", 5.2, 0.47, 0),
            ("industrial_batch", 5.0, 0.47, 0),
            ("industrial_batch", 4.8, 0.46, 0),
            ("maritime_port",    4.6, 0.45, 0),
            ("maritime_port",    4.4, 0.44, 0),
            ("commercial_mixed", 4.4, 0.18, 0),
            ("residential_heat", 5.2, 0.16, 0),
        ],
        q_alpha=0.66, q_peak_extra=0.0, c_fixed=1.8, c_win_fixed=0.0, c_sw_peak=19.0,
        res_ph_w=(0.54, 0.23, 0.23), com_ph_w=(0.20, 0.50, 0.30),
        ami_res_w=(0.34, 0.33, 0.33), ami_com_w=(0.34, 0.33, 0.33),
        gis_ph_w=(0.34, 0.33, 0.33),
    ),
    # S3-opened UP (strong residential EVENING peak -> Phase 1 ~110%; midday com Phase B=62% breaks scalar/cutoff/handbook/AMI!)
    "Raudfjord": dict(
        firm_mva=44.5, r_ohm=0.095, x_ohm=1.22, pt_offset_kv=-0.32, pt_ph_off=(0.17, -0.08, -0.09),
        seasonal_mod=0.25, ramp_thr=0.85,
        feeders=[
            ("residential_heat", 12.2, 0.16, 0),
            ("residential_heat", 10.8, 0.16, 0),
            ("commercial_mixed",  5.2, 0.18, 0),
            ("commercial_mixed",  4.4, 0.18, 0),
            ("industrial_batch",  2.4, 0.22, 0),
        ],
        q_alpha=0.40, q_peak_extra=4.5, c_fixed=3.5, c_win_fixed=2.0, c_sw_peak=0.0,
        res_ph_w=(0.60, 0.20, 0.20), com_ph_w=(0.13, 0.62, 0.25),
        ami_res_w=(0.34, 0.33, 0.33), ami_com_w=(0.34, 0.33, 0.33),
        gis_ph_w=(0.35, 0.33, 0.32),
    ),
    # S3-opened OPPOSITE (strong residential EVENING peak -> balanced w ~33.9%, Phase 2 ~93%; com Phase C=70% + AMI/GIS C skew push P2 -> P1!)
    "Svarthaug": dict(
        firm_mva=33.6, r_ohm=0.090, x_ohm=1.16, pt_offset_kv=0.35, pt_ph_off=(-0.10, -0.07, 0.17),
        seasonal_mod=0.25, ramp_thr=0.85,
        feeders=[
            ("residential_heat", 12.0, 0.16, 0),
            ("residential_heat", 10.4, 0.16, 0),
            ("commercial_mixed",  5.2, 0.18, 0),
            ("commercial_mixed",  4.4, 0.18, 0),
            ("industrial_batch",  2.4, 0.22, 0),
        ],
        q_alpha=0.42, q_peak_extra=4.5, c_fixed=3.5, c_win_fixed=2.0, c_sw_peak=0.0,
        res_ph_w=(0.37, 0.37, 0.26), com_ph_w=(0.15, 0.15, 0.70),
        ami_res_w=(0.29, 0.29, 0.42), ami_com_w=(0.27, 0.27, 0.46),
        gis_ph_w=(0.23, 0.23, 0.54),
    ),
    # Forced Defer anchor (~66%)
    "Tverrli": dict(
        firm_mva=40.5, r_ohm=0.098, x_ohm=1.24, pt_offset_kv=-0.40, pt_ph_off=(0.12, 0.04, -0.16),
        seasonal_mod=0.30, ramp_thr=0.85,
        feeders=[
            ("industrial_batch", 5.2, 0.29, 0),
            ("maritime_port",    4.8, 0.27, 0),
            ("commercial_mixed", 5.2, 0.18, 0),
            ("residential_heat", 6.5, 0.16, 0),
            ("residential_heat", 4.5, 0.16, 0),
        ],
        q_alpha=0.45, q_peak_extra=5.0, c_fixed=4.0, c_win_fixed=2.5, c_sw_peak=0.0,
        res_ph_w=(0.56, 0.22, 0.22), com_ph_w=(0.20, 0.50, 0.30),
        ami_res_w=(0.34, 0.33, 0.33), ami_com_w=(0.34, 0.33, 0.33),
        gis_ph_w=(0.34, 0.33, 0.33),
    ),
    # 4 Modernized upstream hubs (excluded from 2027-2029 relief pool; Fossheim, Lindberg, Solberg ship active-only Sep/Oct/Dec PQ!)
    # Fossheim: 11 feeders (9 staggered industrial/maritime + com + res), distinct count & ratio (~0.31) from 7-feeder Malmnes (~0.43)
    "Fossheim": dict(
        firm_mva=54.0, r_ohm=0.086, x_ohm=1.12, pt_offset_kv=0.36, pt_ph_off=(0.15, -0.09, -0.06),
        seasonal_mod=0.55, ramp_thr=0.85,
        feeders=[
            ("industrial_batch", 3.4, 0.47, 0),
            ("industrial_batch", 3.3, 0.47, 0),
            ("industrial_batch", 3.2, 0.46, 0),
            ("industrial_batch", 3.1, 0.46, 0),
            ("industrial_batch", 3.0, 0.45, 0),
            ("maritime_port",    3.2, 0.46, 0),
            ("maritime_port",    3.1, 0.45, 0),
            ("maritime_port",    3.0, 0.45, 0),
            ("maritime_port",    2.9, 0.44, 0),
            ("commercial_mixed", 4.6, 0.18, 0),
            ("residential_heat", 5.4, 0.16, 0),
        ],
        q_alpha=0.60, q_peak_extra=0.0, c_fixed=3.0, c_win_fixed=0.0, c_sw_peak=14.0,
        res_ph_w=(0.50, 0.25, 0.25), com_ph_w=(0.28, 0.44, 0.28),
        ami_res_w=(0.34, 0.33, 0.33), ami_com_w=(0.34, 0.33, 0.33),
        gis_ph_w=(0.35, 0.33, 0.32),
    ),
    # Lindberg: 8 feeders (6 synchronized industrial/maritime cluster -> ratio ~0.84, widens indep_quad gap > 3.2x!)
    "Lindberg": dict(
        firm_mva=62.0, r_ohm=0.084, x_ohm=1.10, pt_offset_kv=-0.36, pt_ph_off=(-0.14, 0.10, 0.04),
        seasonal_mod=0.0, ramp_thr=0.85,
        feeders=[
            ("industrial_batch", 5.0, 0.55, 3),
            ("industrial_batch", 4.9, 0.55, 3),
            ("industrial_batch", 4.8, 0.54, 3),
            ("maritime_port",    4.6, 0.53, 3),
            ("maritime_port",    4.5, 0.53, 3),
            ("maritime_port",    4.4, 0.52, 3),
            ("commercial_mixed", 4.4, 0.18, 0),
            ("residential_heat", 5.2, 0.16, 0),
        ],
        q_alpha=0.62, q_peak_extra=0.0, c_fixed=3.0, c_win_fixed=0.0, c_sw_peak=23.0,
        res_ph_w=(0.48, 0.26, 0.26), com_ph_w=(0.28, 0.42, 0.30),
        ami_res_w=(0.34, 0.33, 0.33), ami_com_w=(0.34, 0.33, 0.33),
        gis_ph_w=(0.34, 0.33, 0.33),
    ),
    "Ostervik": dict(
        firm_mva=48.0, r_ohm=0.088, x_ohm=1.14, pt_offset_kv=0.36, pt_ph_off=(-0.12, 0.14, -0.02),
        seasonal_mod=0.25, ramp_thr=0.85,
        feeders=[
            ("residential_heat", 7.8, 0.16, 0),
            ("residential_heat", 6.4, 0.16, 0),
            ("commercial_mixed", 5.8, 0.18, 0),
            ("commercial_mixed", 5.0, 0.18, 0),
            ("industrial_batch", 5.0, 0.24, 0),
        ],
        q_alpha=0.48, q_peak_extra=22.0, c_fixed=4.0, c_win_fixed=3.0, c_sw_peak=0.0,
        res_ph_w=(0.39, 0.39, 0.22), com_ph_w=(0.25, 0.25, 0.50),
        ami_res_w=(0.25, 0.25, 0.50), ami_com_w=(0.25, 0.25, 0.50),
        gis_ph_w=(0.23, 0.23, 0.54),
    ),
    # Solberg: 7 feeders (3 synchronized + 2 staggered industrial/maritime -> intermediate ratio ~0.62)
    "Solberg": dict(
        firm_mva=50.0, r_ohm=0.090, x_ohm=1.16, pt_offset_kv=-0.34, pt_ph_off=(0.13, -0.15, 0.02),
        seasonal_mod=0.25, ramp_thr=0.85,
        feeders=[
            ("industrial_batch", 5.0, 0.46, 4),
            ("industrial_batch", 4.8, 0.46, 4),
            ("industrial_batch", 4.6, 0.45, 4),
            ("maritime_port",    4.6, 0.44, 0),
            ("maritime_port",    4.4, 0.43, 0),
            ("commercial_mixed", 4.5, 0.18, 0),
            ("residential_heat", 5.2, 0.16, 0),
        ],
        q_alpha=0.48, q_peak_extra=8.0, c_fixed=4.5, c_win_fixed=3.0, c_sw_peak=0.0,
        res_ph_w=(0.42, 0.29, 0.29), com_ph_w=(0.30, 0.37, 0.33),
        ami_res_w=(0.34, 0.33, 0.33), ami_com_w=(0.34, 0.33, 0.33),
        gis_ph_w=(0.34, 0.33, 0.33),
    ),
}


def _alloc_counts(n, weights):
    raw = np.array(weights, dtype=float) * n
    cnt = np.floor(raw).astype(int)
    rem = n - int(cnt.sum())
    for idx in np.argsort(-(raw - cnt))[:rem]:
        cnt[idx] += 1
    out = []
    for ph, c in enumerate(cnt):
        out.extend([ph] * int(c))
    return np.array(out, dtype=int)


def _rem_alloc(tot_arr, ami_arr, n_leg):
    c_tot = np.bincount(tot_arr, minlength=3)
    c_ami = np.bincount(ami_arr, minlength=3)
    diff = np.maximum(0, c_tot - c_ami)
    while diff.sum() < n_leg:
        diff[np.argmax(c_tot - c_ami - diff)] += 1
    while diff.sum() > n_leg:
        diff[np.argmax(diff)] -= 1
    out = []
    for ph, c in enumerate(diff):
        out.extend([ph] * int(c))
    return np.array(out, dtype=int)


def simulate():
    """Simulate the full 2026 physical distribution grid across all 11 substations."""
    rng = np.random.default_rng(SEED)
    hrs = np.arange(N_HOURS)
    doy = hrs // 24
    hod = hrs % 24
    dow = (doy + 3) % 7  # 2026-01-01 is Thursday
    is_wknd = (dow >= 5).astype(float)

    temp_base = 7.0 - 9.2 * np.cos(2.0 * np.pi * (doy - 17) / 365.0)
    ar_w = np.zeros(N_DAYS)
    for d in range(1, N_DAYS):
        ar_w[d] = 0.78 * ar_w[d - 1] + rng.normal(0.0, 2.2)
    temp_d = temp_base + ar_w[doy]
    temp_d -= 6.5 * np.exp(-0.5 * ((doy - 16) / 2.2) ** 4)
    temp_d -= 4.8 * np.exp(-0.5 * ((doy - 344) / 2.6) ** 4)
    hdd = np.maximum(0.0, 17.5 - temp_d) / 24.0

    diur = {
        "residential_heat": (0.46 + 0.60 * np.exp(-0.5 * ((hod - 19.2) / 2.2) ** 2)
                             + 0.12 * np.exp(-0.5 * ((hod - 7.5) / 1.8) ** 2)) * (0.44 + 0.92 * hdd) * (1.0 + 0.08 * is_wknd),
        "commercial_mixed": (0.24 + 0.92 * np.exp(-0.5 * ((hod - 13.5) / 3.1) ** 2)) * (1.0 - 0.46 * is_wknd) * (0.86 + 0.22 * hdd),
        "industrial_batch": (0.50 + 0.58 * np.exp(-0.5 * ((hod - 12.0) / 4.2) ** 4)) * (1.0 - 0.34 * is_wknd) * (0.90 + 0.18 * hdd),
        "maritime_port":    (0.54 + 0.52 * np.exp(-0.5 * ((hod - 15.5) / 4.2) ** 4)) * (1.0 - 0.22 * is_wknd) * (0.88 + 0.22 * hdd),
    }
    for k in diur:
        diur[k] = diur[k] / float(diur[k].max())

    gsp_v = {}
    base_g = 69.3 + 0.18 * np.cos(2.0 * np.pi * (doy - 17) / 365.0) - 0.10 * (hdd - hdd.mean())
    for gi, gid in enumerate(("GSP-Nord", "GSP-Sor")):
        grng = np.random.default_rng([SEED, 50, gi])
        u = np.zeros(N_HOURS)
        for t in range(1, N_HOURS):
            u[t] = 0.88 * u[t - 1] + grng.normal(0.0, 0.08)
        gsp_v[gid] = base_g + u

    m_arr = np.arange(12)
    seas_curve = 1.0 + 0.54 * np.cos(2.0 * np.pi * (m_arr - 0) / 12.0)

    world = {"gsp_v": gsp_v, "corridors": CORRIDORS, "class_pf": dict(CLASS_NOMINAL_PF), "subs": {}}

    for s_i, s in enumerate(ALL_SUBS):
        cfg = SUB_CFG[s]
        srng = np.random.default_rng([SEED, 100, s_i])
        nf = len(cfg["feeders"])

        clusters = sorted({fc[3] for fc in cfg["feeders"] if fc[3] > 0})
        cl_h = {c: srng.normal(0.0, 1.0, N_HOURS) for c in clusters}
        cl_15 = {c: srng.normal(0.0, 1.0, (N_HOURS, 4)) for c in clusters}

        f_p60 = np.zeros((nf, N_HOURS))
        f_p15 = np.zeros((nf, N_HOURS, 4))
        f_meta = []
        smod = cfg["seasonal_mod"]

        for fi, (fcls, base_mw, sigma_0, cid) in enumerate(cfg["feeders"]):
            if cid > 0:
                h_shk = np.sqrt(0.86) * cl_h[cid] + np.sqrt(0.14) * srng.normal(0.0, 1.0, N_HOURS)
                g_15 = np.sqrt(0.86) * cl_15[cid] + np.sqrt(0.14) * srng.normal(0.0, 1.0, (N_HOURS, 4))
            else:
                h_shk = srng.normal(0.0, 1.0, N_HOURS)
                g_15 = srng.normal(0.0, 1.0, (N_HOURS, 4))
            # Bounded duty-cycle within-hour burst pulse (zero mean across 4 quarters, physical rated-step ceiling)
            u_15 = np.tanh(1.15 * g_15)
            z_15 = u_15 - u_15.mean(axis=1, keepdims=True)
            sig_h = sigma_0 * ((1.0 - smod) + smod * seas_curve[HOUR_MONTH]) if sigma_0 > 0.30 else np.full(N_HOURS, sigma_0)
            p_hr = base_mw * diur[fcls] * np.exp(0.012 * h_shk)
            f_p15[fi] = np.maximum(0.05, p_hr[:, None] * (1.0 + sig_h[:, None] * z_15))
            f_p60[fi] = f_p15[fi].mean(axis=1)
            f_meta.append(dict(feeder_id=f"{s[:3].upper()}-F{fi+1:02d}", fcls=fcls, cid=cid))

        sub_p15 = f_p15.sum(axis=0)
        sub_p60 = sub_p15.mean(axis=1)
        feeder_m15 = np.column_stack([f_p15[:, HOUR_MONTH == m, :].max(axis=(1, 2)) for m in range(12)])
        feeder_p60_m = np.column_stack([f_p60[:, HOUR_MONTH == m].max(axis=1) for m in range(12)])

        p_cls = {c: np.zeros(N_HOURS) for c in ("residential_heat", "commercial_mixed", "industrial_batch", "maritime_port")}
        for fi, fm in enumerate(f_meta):
            p_cls[fm["fcls"]] += f_p60[fi]

        p_norm = sub_p60 / float(sub_p60.max())
        ind_ramp = 1.0 / (1.0 + np.exp(-32.0 * (p_norm - cfg["ramp_thr"])))
        sw_cap = cfg["c_sw_peak"] / (1.0 + np.exp(-36.0 * (p_norm - 0.87)))
        win_cap = cfg["c_win_fixed"] * WINTER_HOURS.astype(float)
        q_hourly = (cfg["q_alpha"] * sub_p60 + cfg["q_peak_extra"] * ind_ramp
                    - cfg["c_fixed"] - win_cap - sw_cap + srng.normal(0.0, 0.14, N_HOURS))
        q_15 = q_hourly[:, None] + 0.20 * (sub_p15 - sub_p60[:, None]) + srng.normal(0.0, 0.04, (N_HOURS, 4))
        q_hourly = q_15.mean(axis=1)
        sub_net_kvarh_m = np.array([q_hourly[HOUR_MONTH == m].sum() * 1000.0 for m in range(12)])
        sub_kwh_m = np.array([sub_p60[HOUR_MONTH == m].sum() * 1000.0 for m in range(12)])

        w_res = np.array(cfg["res_ph_w"], dtype=float)
        w_com = np.array(cfg["com_ph_w"], dtype=float)
        dw_res = w_res - (1.0 / 3.0)
        dw_com = w_com - (1.0 / 3.0)

        p_bal_h = p_cls["industrial_batch"] + p_cls["maritime_port"]
        sub_p_ph_h = (w_res[:, None] * p_cls["residential_heat"][None, :]
                      + w_com[:, None] * p_cls["commercial_mixed"][None, :]
                      + (1.0 / 3.0) * p_bal_h[None, :])
        q_ex_ph_h = (TRUE_TAN_PHI_RES * dw_res[:, None] * p_cls["residential_heat"][None, :]
                     + TRUE_TAN_PHI_COM * dw_com[:, None] * p_cls["commercial_mixed"][None, :])

        lat_cls = ["residential_heat"] * 12 + ["commercial_mixed"] * 8 + ["residential_heat"] * 12 + ["commercial_mixed"] * 8
        lat_is_ami = np.array([True] * N_AMI_LAT + [False] * N_LEG_LAT)
        lat_true_ph = np.zeros(N_LATERALS, dtype=int)
        lat_true_ph[0:12] = _alloc_counts(12, cfg["ami_res_w"])
        lat_true_ph[12:20] = _alloc_counts(8, cfg["ami_com_w"])
        res_tot_cnt = _alloc_counts(24, cfg["res_ph_w"])
        com_tot_cnt = _alloc_counts(16, cfg["com_ph_w"])
        lat_true_ph[20:32] = _rem_alloc(res_tot_cnt, lat_true_ph[0:12], 12)
        lat_true_ph[32:40] = _rem_alloc(com_tot_cnt, lat_true_ph[12:20], 8)

        grng = np.random.default_rng([SEED, 300, s_i])
        if s in ("Svarthaug", "Ostervik"):
            lat_gis_ph = lat_true_ph.copy()
            lat_gis_ph[20:] = grng.permutation(_alloc_counts(N_LEG_LAT, cfg["gis_ph_w"]))
            for idx in grng.choice(N_AMI_LAT, size=6, replace=False):
                lat_gis_ph[idx] = (lat_true_ph[idx] + int(grng.integers(1, 3))) % 3
        else:
            lat_gis_ph = grng.permutation(_alloc_counts(N_LATERALS, cfg["gis_ph_w"]))
            matches = np.where(lat_gis_ph[:N_AMI_LAT] == lat_true_ph[:N_AMI_LAT])[0]
            mismatches = np.where(lat_gis_ph[:N_AMI_LAT] != lat_true_ph[:N_AMI_LAT])[0]
            while len(mismatches) < 6 and len(matches) > 0:
                idx = int(grng.choice(matches))
                lat_gis_ph[idx] = (lat_true_ph[idx] + int(grng.integers(1, 3))) % 3
                matches = np.where(lat_gis_ph[:N_AMI_LAT] == lat_true_ph[:N_AMI_LAT])[0]
                mismatches = np.where(lat_gis_ph[:N_AMI_LAT] != lat_true_ph[:N_AMI_LAT])[0]

        lat_p_ami = np.zeros((N_AMI_LAT, N_HOURS))
        lat_q_ami = np.zeros((N_AMI_LAT, N_HOURS))
        lat_mwh = np.zeros(N_LATERALS)
        for li in range(N_LATERALS):
            lcls = lat_cls[li]
            base_frac = srng.uniform(0.032, 0.048) if lcls == "residential_heat" else srng.uniform(0.048, 0.072)
            p_kw = p_cls[lcls] * 1000.0 * base_frac * np.exp(srng.normal(0.0, 0.08, N_HOURS))
            lat_mwh[li] = float(p_kw.sum() / 1000.0)
            if li < N_AMI_LAT:
                lat_p_ami[li] = p_kw
                tphi = TRUE_TAN_PHI_RES if lcls == "residential_heat" else TRUE_TAN_PHI_COM
                lat_q_ami[li] = p_kw * (tphi + srng.normal(0.0, 0.005, N_HOURS))

        p15_flat = sub_p15.ravel()
        pk_q_idx = int(np.argmax(p15_flat))
        pk_h_15 = pk_q_idx // 4
        true_p15_peak = float(p15_flat[pk_q_idx])
        true_q_peak_h = float(q_hourly[pk_h_15])
        true_q15_at_peak = float(q_15.ravel()[pk_q_idx])
        true_s15_tot = float(np.sqrt(true_p15_peak ** 2 + true_q15_at_peak ** 2))
        true_w_max = float((sub_p_ph_h[:, pk_h_15] / sub_p60[pk_h_15]).max())
        true_lim_mva = float(3.0 * true_w_max * true_s15_tot)
        true_loading_pct = float(100.0 * true_lim_mva / cfg["firm_mva"])

        world["subs"][s] = dict(
            cfg=cfg, f_meta=f_meta, f_p60=f_p60, f_p15=f_p15,
            sub_p15=sub_p15, sub_p60=sub_p60, p_cls=p_cls,
            feeder_m15=feeder_m15, feeder_p60_m=feeder_p60_m,
            q_hourly=q_hourly, q_15=q_15,
            sub_kwh_m=sub_kwh_m, sub_net_kvarh_m=sub_net_kvarh_m,
            sub_p_ph_h=sub_p_ph_h, q_ex_ph_h=q_ex_ph_h,
            lat_cls=lat_cls, lat_is_ami=lat_is_ami, lat_true_ph=lat_true_ph,
            ami_true_ph=lat_true_ph[:N_AMI_LAT].copy(), lat_gis_ph=lat_gis_ph,
            lat_p_ami=lat_p_ami, lat_q_ami=lat_q_ami, lat_mwh=lat_mwh,
            comm_p15=(sub_p15[COMM_HOURS, :].copy() if s in PQ_COMM_SITES else None),
            truth=dict(
                p15_peak=true_p15_peak, p60_peak=float(sub_p60.max()),
                q_peak_h=true_q_peak_h, q15_at_peak=true_q15_at_peak,
                s15_tot=true_s15_tot, w_max=true_w_max,
                lim_mva=true_lim_mva, loading_pct=true_loading_pct,
                relief_mva=max(0.0, true_lim_mva - 0.85 * cfg["firm_mva"]),
                pk_h=pk_h_15, pk_h_60=int(np.argmax(sub_p60)),
            ),
        )

    for c_id, c_info in CORRIDORS.items():
        v_cur = gsp_v[c_info["gsp"]].copy()
        subs_in_cor = [seg[1] for seg in c_info["segs"]]
        for seg_idx, (_frm, s, l_km, r_km, x_km) in enumerate(c_info["segs"]):
            downstream = subs_in_cor[seg_idx:]
            p_flow = sum(world["subs"][d]["sub_p60"] for d in downstream)
            q_flow = sum(world["subs"][d]["q_hourly"] for d in downstream)
            dv_66 = (l_km * r_km * p_flow + l_km * x_km * q_flow) / V_NOM_HV
            v_cur = v_cur - dv_66

            sd = world["subs"][s]
            cfg = sd["cfg"]
            srng = np.random.default_rng([SEED, 200, ALL_SUBS.index(s)])
            dv_tx = (cfg["r_ohm"] * sd["sub_p60"] + cfg["x_ohm"] * sd["q_hourly"]) / V_NOM_LV
            ideal_ratio = (22.25 + dv_tx) / v_cur
            nom_ratio = V_NOM_LV / V_NOM_HV
            tap_step_int = np.clip(np.round(((ideal_ratio / nom_ratio) - 1.0) / TAP_STEP), TAP_MIN, TAP_MAX).astype(int)
            tau = nom_ratio * (1.0 + TAP_STEP * tap_step_int)
            v_lv_true = v_cur * tau - dv_tx
            v_lv_meas = v_lv_true - cfg["pt_offset_kv"] + srng.normal(0.0, 0.008, N_HOURS)

            p_ex = sd["sub_p_ph_h"] - (sd["sub_p60"][None, :] / 3.0)
            dv_ph_load = -(3.0 / V_NOM_LV) * (cfg["r_ohm"] * p_ex + cfg["x_ohm"] * sd["q_ex_ph_h"])

            u_bg = srng.normal(0.0, 0.0025, (3, N_HOURS))
            for ph in range(3):
                for t in range(1, N_HOURS):
                    u_bg[ph, t] = 0.45 * u_bg[ph, t - 1] + 0.893 * u_bg[ph, t]
            u_bg -= u_bg.mean(axis=0, keepdims=True)
            pt_ph = np.array(cfg["pt_ph_off"], dtype=float)[:, None]
            pt_ph -= pt_ph.mean()
            v_bus_ph = v_lv_meas[None, :] + pt_ph + dv_ph_load + u_bg

            lat_v_ami = np.zeros((N_AMI_LAT, N_HOURS))
            for l_i in range(N_AMI_LAT):
                ph = sd["ami_true_ph"][l_i]
                r_lat = srng.uniform(0.005, 0.011)
                lat_v_ami[l_i] = (230.0 / V_NOM_LV) * v_bus_ph[ph] - r_lat * sd["lat_p_ami"][l_i] + srng.normal(0.0, 0.16, N_HOURS)

            sd["corridor"] = c_id
            sd["gsp"] = c_info["gsp"]
            sd["v_hv_true"] = v_cur.copy()
            sd["v_lv_meas"] = v_lv_meas
            sd["tap_step_int"] = tap_step_int
            sd["v_bus_ph"] = v_bus_ph
            sd["lat_v_ami"] = lat_v_ami

    return world


# --- ESTIMATORS (read strictly from pack-available arrays in world!) ---

def _infer_feeder_corr_matrices(world, opts=None):
    opts = opts or {}
    mode = opts.get("s1_mode", "golden")
    innov = opts.get("s1_innov", "pca4")
    win = opts.get("s1_corr_win", "all")
    eff_mode = mode if mode in ("raw_corr", "register_rho", "pca1", "pca2") else innov
    cache = world.setdefault("_R_cache", {})
    ckey = (eff_mode, win)
    if ckey in cache:
        return cache[ckey]
    wmask = WINTER_HOURS if win == "winter" else np.ones(N_HOURS, dtype=bool)
    if eff_mode == "raw_corr":
        out = {s: np.clip(np.corrcoef(world["subs"][s]["f_p60"][:, wmask]), 0.0, 1.0) for s in ALL_SUBS}
        cache[ckey] = out
        return out
    if eff_mode == "register_rho":
        out = {}
        for s in ALL_SUBS:
            sd = world["subs"][s]
            rat = sd["feeder_m15"] / np.maximum(sd["feeder_p60_m"], 0.1)
            R = np.corrcoef(rat)
            np.fill_diagonal(R, 1.0)
            out[s] = np.clip(R, 0.0, 1.0)
        cache[ckey] = out
        return out
    if eff_mode.startswith("pca"):
        npc = int(eff_mode[3:])
        all_log = {}
        for s in ALL_SUBS:
            L = np.log(np.maximum(world["subs"][s]["f_p60"] / world["subs"][s]["f_p60"].mean(axis=1, keepdims=True), 1e-4))
            L -= L.mean(axis=1, keepdims=True)
            all_log[s] = L
        out = {}
        for s in ALL_SUBS:
            other = np.vstack([all_log[s2] for s2 in ALL_SUBS if s2 != s])
            _, _, Vt = np.linalg.svd(other[:, wmask], full_matrices=False)
            F = Vt[:npc]
            Y = all_log[s][:, wmask]
            E = Y - (Y @ F.T) @ F
            R = np.corrcoef(E)
            np.fill_diagonal(R, 1.0)
            out[s] = np.clip(R, 0.0, 1.0)
        cache[ckey] = out
        return out
    by_c = {}
    for s in ALL_SUBS:
        sd = world["subs"][s]
        for fi, fm in enumerate(sd["f_meta"]):
            arr = sd["f_p60"][fi]
            by_c.setdefault(fm["fcls"], []).append((s, fi, arr / float(arr.mean())))
    csum = {c: np.sum([x[2] for x in v], axis=0) for c, v in by_c.items()}
    ccnt = {c: len(v) for c, v in by_c.items()}
    out = {}
    for s in ALL_SUBS:
        sd = world["subs"][s]
        nf = len(sd["f_meta"])
        innov_arr = np.zeros((nf, int(wmask.sum())))
        for fi, fm in enumerate(sd["f_meta"]):
            c = fm["fcls"]
            norm = sd["f_p60"][fi] / float(sd["f_p60"][fi].mean())
            same = [sd["f_p60"][j] / float(sd["f_p60"][j].mean()) for j, fm2 in enumerate(sd["f_meta"]) if fm2["fcls"] == c]
            ref_p = (csum[c] - np.sum(same, axis=0)) / max(ccnt[c] - len(same), 1)
            res = (norm - ref_p) if eff_mode == "ref_diff" else (np.log(np.maximum(norm, 1e-4)) - np.log(np.maximum(ref_p, 1e-4)))
            innov_arr[fi] = res[wmask]
        R = np.corrcoef(innov_arr)
        np.fill_diagonal(R, 1.0)
        out[s] = np.clip(R, 0.0, 1.0)
    cache[ckey] = out
    return out


def _quad_excess(sd, R_mat, m_list, form="add_raw", indep=False):
    nf = len(sd["f_meta"])
    idx_h = np.where(np.isin(HOUR_MONTH, m_list))[0]
    pk_h = int(idx_h[np.argmax(sd["sub_p60"][idx_h])])
    d = np.zeros(nf)
    for i in range(nf):
        if form == "add_raw":
            d[i] = max(0.0, float(np.mean([sd["feeder_m15"][i, m] - sd["feeder_p60_m"][i, m] for m in m_list])))
        elif form == "mult":
            rel = float(np.mean([(sd["feeder_m15"][i, m] - sd["feeder_p60_m"][i, m]) / sd["feeder_p60_m"][i, m] for m in m_list]))
            d[i] = max(0.0, rel) * float(sd["f_p60"][i, pk_h])
        else:
            ex = float(np.mean([sd["feeder_m15"][i, m] - sd["feeder_p60_m"][i, m] for m in m_list]))
            sc = float(sd["f_p60"][i, pk_h]) / float(np.mean([sd["feeder_p60_m"][i, m] for m in m_list]))
            d[i] = max(0.0, ex * sc)
    if indep:
        return float(np.sqrt(np.sum(d ** 2)))
    return float(np.sqrt(max(0.0, float(d @ R_mat @ d))))


def _comm_month_obs_ex(sd, m):
    """Exact monthly coincident 15-minute peak excess: max(P_15) - max(P_60) in commissioning month m."""
    mh = (HOUR_MONTH == m)
    cm = mh[COMM_HOURS]
    p60_m = float(sd["sub_p60"][mh].max())
    p15_m = float(sd["comm_p15"][cm].max())
    return p15_m - p60_m, p60_m


def _s1_estimate_all(world, opts):
    mode = opts.get("s1_mode", "golden")
    R_mats = _infer_feeder_corr_matrices(world, opts)
    k_opt = opts.get("s1_kord", "comm_cal")
    form = opts.get("s1_form", "add_raw")
    indep = (mode == "indep_quad")
    if k_opt == "unit":
        k_ord = 1.0
    else:
        obs_c, raw_c = [], []
        for r in PQ_COMM_SITES:
            sd = world["subs"][r]
            for m in COMM_MONTHS:
                obs_ex, _ = _comm_month_obs_ex(sd, m)
                rq = _quad_excess(sd, R_mats[r], [m], form=form, indep=indep)
                obs_c.append(obs_ex)
                raw_c.append(rq)
        k_ord = float(sum(obs_c) / sum(raw_c)) if k_opt == "comm_cal" else float(np.mean([o / q for o, q in zip(obs_c, raw_c)]))

    # Commissioning ratios directly on monthly max(P_15) - max(P_60) across all 9 site-months
    flat_vals, cf_vals = [], []
    site_reg_rat = {}
    for r in PQ_COMM_SITES:
        sd = world["subs"][r]
        r_rats = []
        for m in COMM_MONTHS:
            obs_ex, p60_m = _comm_month_obs_ex(sd, m)
            reg_ex = float(np.sum(np.maximum(0.0, sd["feeder_m15"][:, m] - sd["feeder_p60_m"][:, m])))
            flat_vals.append((p60_m + obs_ex) / p60_m)
            cf_vals.append(obs_ex / max(reg_ex, 1e-6))
            r_rats.append(obs_ex / max(reg_ex, 1e-6))
        site_reg_rat[r] = float(np.mean(r_rats))
    comm_flat = float(np.mean(flat_vals))
    comm_cf = float(np.mean(cf_vals))

    # Mean off-diagonal raw correlation per substation for nearest-PQ-site twin matching
    raw_R = _infer_feeder_corr_matrices(world, {"s1_mode": "raw_corr"})
    def _mean_off(R):
        n = R.shape[0]
        return float(R[~np.eye(n, dtype=bool)].mean())
    raw_rho = {s: _mean_off(raw_R[s]) for s in ALL_SUBS}

    out = {}
    for s in ALL_SUBS:
        sd = world["subs"][s]
        p60_pk = float(sd["sub_p60"].max())
        pk_h = int(np.argmax(sd["sub_p60"]))
        pk_m = int(HOUR_MONTH[pk_h])
        mopt = opts.get("s1_months", "winter")
        m_list = list(WINTER_MONTHS) if mopt == "winter" else ([0, 1, 11] if mopt == "djf" else (list(range(12)) if mopt == "all" else [pk_m]))
        if mode == "scada60":
            out[s] = p60_pk
        elif mode == "flat_ratio":
            out[s] = p60_pk * comm_flat
        elif mode == "cf_pooled":
            d_mean = float(np.mean([np.sum(np.maximum(0.0, sd["feeder_m15"][:, m] - sd["feeder_p60_m"][:, m])) for m in m_list]))
            out[s] = p60_pk + comm_cf * d_mean
        elif mode == "twin_ratio":
            cands = [r for r in PQ_COMM_SITES if r != s]
            twin = min(cands, key=lambda r: abs(raw_rho[r] - raw_rho[s]))
            d_mean = float(np.mean([np.sum(np.maximum(0.0, sd["feeder_m15"][:, m] - sd["feeder_p60_m"][:, m])) for m in m_list]))
            out[s] = p60_pk + site_reg_rat[twin] * d_mean
        elif mode == "linear_sum":
            d_mean = float(np.mean([np.sum(np.maximum(0.0, sd["feeder_m15"][:, m] - sd["feeder_p60_m"][:, m])) for m in m_list]))
            out[s] = p60_pk + d_mean
        elif mode == "rigorous_cf60":
            cf60 = p60_pk / float(sd["f_p60"].max(axis=1).sum())
            out[s] = cf60 * float(sd["feeder_m15"].max(axis=1).sum())
        else:
            rq = _quad_excess(sd, R_mats[s], m_list, form=form, indep=indep)
            out[s] = p60_pk + k_ord * rq
    return out, k_ord, comm_flat, comm_cf, R_mats, site_reg_rat, raw_rho


def _s2_estimate_all(world, opts):
    mode = opts.get("s2_mode", "golden")
    cpf = world.get("class_pf", CLASS_NOMINAL_PF)
    out_qh = {}
    q_hourly_hat = {}
    if mode in ("net_kvarh", "winter_kvarh", "class_nominal", "monthly_qp", "monthly_qp_winter", "monthly_quad"):
        for s in ALL_SUBS:
            sd = world["subs"][s]
            p60 = sd["sub_p60"]
            pk_h = int(np.argmax(p60))
            p_m = np.array([p60[HOUR_MONTH == m].mean() for m in range(12)])
            q_m = np.array([sd["sub_net_kvarh_m"][m] / (1000.0 * int((HOUR_MONTH == m).sum())) for m in range(12)])
            if mode == "net_kvarh":
                ep, eq = float(sd["sub_kwh_m"].sum()), float(sd["sub_net_kvarh_m"].sum())
                pf = ep / np.sqrt(ep ** 2 + eq ** 2)
                out_qh[s] = float(p60[pk_h] * np.tan(np.arccos(np.clip(pf, 0.5, 0.9999))) * (1.0 if eq >= 0 else -1.0))
                q_hourly_hat[s] = np.full(N_HOURS, eq / (1000.0 * N_HOURS))
            elif mode == "winter_kvarh":
                ep = float(sum(sd["sub_kwh_m"][m] for m in WINTER_MONTHS))
                eq = float(sum(sd["sub_net_kvarh_m"][m] for m in WINTER_MONTHS))
                tphi = eq / max(ep, 1.0)
                q_h_arr = p60 * tphi
                out_qh[s] = float(q_h_arr[pk_h])
                q_hourly_hat[s] = q_h_arr
            elif mode == "class_nominal":
                q_h_arr = sum(sd["f_p60"][i] * np.tan(np.arccos(cpf[fm["fcls"]])) for i, fm in enumerate(sd["f_meta"]))
                out_qh[s] = float(q_h_arr[pk_h])
                q_hourly_hat[s] = q_h_arr
            elif mode == "monthly_qp":
                b, a = np.polyfit(p_m, q_m, 1)
                q_h_arr = a + b * p60
                out_qh[s] = float(q_h_arr[pk_h])
                q_hourly_hat[s] = q_h_arr
            elif mode == "monthly_qp_winter":
                win_m = np.isin(np.arange(12), WINTER_MONTHS).astype(float)
                X = np.column_stack([np.ones(12), p_m, win_m])
                beta, *_ = np.linalg.lstsq(X, q_m, rcond=None)
                q_h_arr = beta[0] + beta[1] * p60 + beta[2] * WINTER_HOURS.astype(float)
                out_qh[s] = float(q_h_arr[pk_h])
                q_hourly_hat[s] = q_h_arr
            else:
                c2, c1, c0 = np.polyfit(p_m, q_m, 2)
                q_h_arr = c0 + c1 * p60 + c2 * (p60 ** 2)
                out_qh[s] = float(q_h_arr[pk_h])
                q_hourly_hat[s] = q_h_arr
        return out_qh, q_hourly_hat

    for cid, c_info in world["corridors"].items():
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

        if mode == "targets_only_corridor":
            p_sub_eff = p_sub.copy()
            for i, s in enumerate(subs):
                if s not in TARGETS:
                    p_sub_eff[i] = 0.0
        else:
            p_sub_eff = p_sub

        dv_rp = np.zeros((m, N_HOURS))
        for i in range(m):
            for e in range(i + 1):
                dv_rp[i] += (r_segs[e] * p_sub_eff[e:].sum(axis=0)) / V_NOM_HV
        x_sh = np.zeros((m, m))
        for i in range(m):
            for j in range(m):
                x_sh[i, j] = sum(x_segs[:min(i, j) + 1]) / V_NOM_HV
        if mode == "targets_only_corridor":
            for j, s in enumerate(subs):
                if s not in TARGETS:
                    x_sh[:, j] = 0.0

        if mode in ("local_dv", "rp_only"):
            for i, s in enumerate(subs):
                sd = world["subs"][s]
                v_hv_a = v_gsp if mode == "local_dv" else (v_gsp - dv_rp[i])
                dv = v_hv_a * tau[i] - vlv[i]
                q_unc = (V_NOM_LV * dv - r_tx[i] * p_sub[i]) / x_tx[i]
                pk_h = int(np.argmax(p_sub[i]))
                pk_m = int(HOUR_MONTH[pk_h])
                hm = (HOUR_MONTH == pk_m) & ~np.isnan(vlv[i])
                q_bar = float(sd["sub_net_kvarh_m"][pk_m]) / (1000.0 * int((HOUR_MONTH == pk_m).sum()))
                q_hat = q_unc - float(np.nanmean(q_unc[hm])) + q_bar
                top20 = np.argsort(p_sub[i])[-20:]
                c = np.polyfit(p_sub[i, top20], q_hat[top20], 1)
                out_qh[s] = float(c[0] * p_sub[i, pk_h] + c[1])
                q_hourly_hat[s] = q_hat
            continue

        v_scale = vlv if opts.get("s2_vscale") == "vlv" else np.full_like(vlv, V_NOM_LV)
        y = v_gsp[None, :] * tau - vlv - tau * dv_rp - (r_tx[:, None] * p_sub) / v_scale
        valid_h = ~np.any(np.isnan(y), axis=0)

        anc = opts.get("s2_anchor", "peak_month")
        if anc == "peak_month":
            pk_m = int(HOUR_MONTH[int(np.argmax(p_sub.sum(axis=0)))])
            amask = (HOUR_MONTH == pk_m) & valid_h
            q_bar_m = np.array([world["subs"][s]["sub_net_kvarh_m"][pk_m] / (1000.0 * int((HOUR_MONTH == pk_m).sum())) for s in subs])
        elif anc == "winter":
            amask = WINTER_HOURS & valid_h
            q_bar_m = np.array([sum(world["subs"][s]["sub_net_kvarh_m"][mm] for mm in WINTER_MONTHS) / (1000.0 * int(WINTER_HOURS.sum())) for s in subs])
        else:
            amask = valid_h
            q_bar_m = np.array([world["subs"][s]["sub_net_kvarh_m"].sum() / (1000.0 * N_HOURS) for s in subs])

        M_all = tau[:, None, :] * x_sh[:, :, None] + np.eye(m)[:, :, None] * (x_tx[:, None] / np.where(np.isnan(v_scale), V_NOM_LV, v_scale))[:, None, :]
        M_inv = np.linalg.inv(np.transpose(M_all, (2, 0, 1)))
        y_clean = np.where(np.isnan(y), 0.0, y)
        if mode == "raw_dv_no_demean":
            Q_hat = (M_inv @ y_clean.T[:, :, None]).squeeze(-1).T
        elif opts.get("s2_solve") == "mbar_only":
            M_bar = tau[:, amask].mean(axis=1)[:, None] * x_sh + np.diag(x_tx / np.nanmean(v_scale[:, amask], axis=1))
            Q_hat = q_bar_m[:, None] + np.linalg.inv(M_bar) @ (y_clean - y_clean[:, amask].mean(axis=1, keepdims=True))
        else:
            q_y_a = (M_inv[amask] @ y_clean[:, amask].T[:, :, None]).squeeze(-1).mean(axis=0)
            delta_pt = np.linalg.solve(M_inv[amask].mean(axis=0), q_bar_m - q_y_a)
            Q_hat = (M_inv @ (y_clean + delta_pt[:, None]).T[:, :, None]).squeeze(-1).T

        agg = opts.get("s2_peak_agg", "top5")
        for i, s in enumerate(subs):
            pk_h = int(np.argmax(p_sub[i]))
            if agg == "single":
                out_qh[s] = float(Q_hat[i, pk_h])
            elif agg == "top5":
                out_qh[s] = float(np.mean(Q_hat[i, np.argsort(p_sub[i])[-5:]]))
            else:
                top20 = np.argsort(p_sub[i])[-20:]
                c = np.polyfit(p_sub[i, top20], Q_hat[i, top20], 1)
                out_qh[s] = float(c[0] * p_sub[i, pk_h] + c[1])
            q_hourly_hat[s] = Q_hat[i]
    return out_qh, q_hourly_hat


def _identify_ami_phases(sd):
    if "_ami_ph" in sd:
        return sd["_ami_ph"]
    v_bus = sd["v_bus_ph"] * (230.0 / V_NOM_LV)
    v_cm = v_bus.mean(axis=0, keepdims=True)
    v_t = v_bus - v_cm
    idx_h = np.where(WINTER_HOURS)[0]
    r_v = sd["lat_v_ami"] - v_cm
    d_vt = np.diff(v_t[:, idx_h], axis=1)
    d_rv = np.diff(r_v[:, idx_h], axis=1)
    d_lp = np.diff(sd["lat_p_ami"][:, idx_h], axis=1)
    ph_id = np.zeros(sd["lat_v_ami"].shape[0], dtype=int)
    for li in range(ph_id.shape[0]):
        y, xp = d_rv[li], d_lp[li]
        rss = []
        for ph in range(3):
            X = np.column_stack([d_vt[ph], xp])
            b, *_ = np.linalg.lstsq(X, y, rcond=None)
            rss.append(float(np.sum(y ** 2)) if b[0] <= 0.1 else float(np.sum((y - X @ b) ** 2)))
        ph_id[li] = int(np.argmin(rss))
    sd["_ami_ph"] = ph_id
    return ph_id


def _measure_ami_tan_phi(world, win="heating"):
    mask = WINTER_HOURS if win == "winter" else HEATING_HOURS
    num = {"residential_heat": 0.0, "commercial_mixed": 0.0}
    den = {"residential_heat": 0.0, "commercial_mixed": 0.0}
    for s in ALL_SUBS:
        sd = world["subs"][s]
        ami_cls = [sd["lat_cls"][i] for i in range(len(sd["lat_cls"])) if sd["lat_is_ami"][i]]
        for li, c in enumerate(ami_cls):
            p = sd["lat_p_ami"][li, mask]
            q = sd["lat_q_ami"][li, mask]
            num[c] += float(np.dot(p, q))
            den[c] += float(np.dot(p, p))
    return {c: num[c] / den[c] for c in num}


def _ami_q_rmse(world, tphi_by_cls=None, tphi_by_sub=None):
    errs = []
    for s in TARGETS:
        sd = world["subs"][s]
        ami_cls = [sd["lat_cls"][i] for i in range(len(sd["lat_cls"])) if sd["lat_is_ami"][i]]
        for li, c in enumerate(ami_cls):
            p = sd["lat_p_ami"][li, WINTER_HOURS]
            q = sd["lat_q_ami"][li, WINTER_HOURS]
            tp = tphi_by_cls[c] if tphi_by_cls is not None else tphi_by_sub[s]
            errs.append(float(np.sqrt(np.mean((q - p * tp) ** 2))))
    return float(np.mean(errs))


def _s3_estimate_all(world, opts, qh_for_subpf=None):
    mode = opts.get("s3_mode", "golden")
    cpf = world.get("class_pf", CLASS_NOMINAL_PF)
    tphi_ami = _measure_ami_tan_phi(world, win=opts.get("s3_ami_win", "heating"))
    tphi_hb = {c: float(np.tan(np.arccos(cpf[c]))) for c in ("residential_heat", "commercial_mixed")}
    out_w = {}
    bus_resid_rms = {}

    for s in ALL_SUBS:
        sd = world["subs"][s]
        cfg = sd["cfg"]
        p60 = sd["sub_p60"]
        pk_h = int(np.argmax(p60))
        v_ex = sd["v_bus_ph"] - sd["v_bus_ph"].mean(axis=0, keepdims=True)
        p_res = sd["p_cls"]["residential_heat"]
        p_com = sd["p_cls"]["commercial_mixed"]
        p_bal = sd["p_cls"]["industrial_batch"] + sd["p_cls"]["maritime_port"]

        if mode == "balanced":
            out_w[s] = 1.0 / 3.0
            bus_resid_rms[s] = float(np.sqrt(np.mean((v_ex - v_ex.mean(axis=1, keepdims=True)) ** 2)))
            continue
        if mode in ("gis", "ami_only_bal", "ami_grossup", "ami_plus_gis"):
            ami_ph = _identify_ami_phases(sd) if mode != "gis" else None
            ami_idx = np.where(sd["lat_is_ami"])[0]
            ami_pos = {int(orig_i): a_i for a_i, orig_i in enumerate(ami_idx)}
            ami_kw_per_mwh = {}
            for c in ("residential_heat", "commercial_mixed"):
                a_list = [a_i for a_i, orig_i in enumerate(ami_idx) if sd["lat_cls"][orig_i] == c]
                o_list = [int(orig_i) for orig_i in ami_idx if sd["lat_cls"][orig_i] == c]
                ami_kw_per_mwh[c] = float(sd["lat_p_ami"][a_list, pk_h].sum() / sd["lat_mwh"][o_list].sum())
            all_kw = np.array([
                sd["lat_p_ami"][ami_pos[i], pk_h] if i in ami_pos else sd["lat_mwh"][i] * ami_kw_per_mwh[sd["lat_cls"][i]]
                for i in range(len(sd["lat_cls"]))
            ])
            if mode == "gis":
                ph_ids = sd["lat_gis_ph"]
                bal = max(0.0, p60[pk_h] * 1000.0 - all_kw.sum())
                ph_kw = np.array([all_kw[ph_ids == ph].sum() + bal / 3.0 for ph in range(3)])
            elif mode == "ami_only_bal":
                bal = max(0.0, p60[pk_h] * 1000.0 - sd["lat_p_ami"][:, pk_h].sum())
                ph_kw = np.array([sd["lat_p_ami"][ami_ph == ph, pk_h].sum() + bal / 3.0 for ph in range(3)])
            elif mode == "ami_grossup":
                scale = float(len(sd["lat_cls"])) / float(len(ami_idx))
                ami_s = sd["lat_p_ami"][:, pk_h].sum()
                sp_tot = min(p60[pk_h] * 1000.0, ami_s * scale)
                bal = p60[pk_h] * 1000.0 - sp_tot
                ph_kw = np.array([sd["lat_p_ami"][ami_ph == ph, pk_h].sum() * (sp_tot / ami_s) + bal / 3.0 for ph in range(3)])
            else:
                ph_ids = sd["lat_gis_ph"].copy()
                ph_ids[ami_idx] = ami_ph
                bal = max(0.0, p60[pk_h] * 1000.0 - all_kw.sum())
                ph_kw = np.array([all_kw[ph_ids == ph].sum() + bal / 3.0 for ph in range(3)])
            out_w[s] = float(ph_kw.max() / ph_kw.sum())
            z_avg = cfg["r_ohm"] + cfg["x_ohm"] * 0.35
            dw_c = ph_kw / ph_kw.sum() - 1.0 / 3.0
            v_pred = -(3.0 * z_avg / V_NOM_LV) * dw_c[:, None] * p60[None, :]
            res = (v_ex - v_pred) - (v_ex - v_pred).mean(axis=1, keepdims=True)
            bus_resid_rms[s] = float(np.sqrt(np.mean(res ** 2)))
            continue

        if mode in ("scalar_ols", "evening_cutoff_ols", "evening_cutoff_zres"):
            if mode in ("evening_cutoff_ols", "evening_cutoff_zres"):
                hod = np.arange(N_HOURS) % 24
                mask = (hod >= 17) & (hod <= 21)
            else:
                mask = np.ones(N_HOURS, dtype=bool)
            p_m = p60[mask] - p60[mask].mean()
            sl = (v_ex[:, mask] @ p_m) / float(np.dot(p_m, p_m))
            if mode == "evening_cutoff_zres":
                z_use = cfg["r_ohm"] + cfg["x_ohm"] * tphi_ami["residential_heat"]
            else:
                wt_r = p_res.sum() / (p_res.sum() + p_com.sum())
                z_use = cfg["r_ohm"] + cfg["x_ohm"] * (wt_r * tphi_ami["residential_heat"] + (1.0 - wt_r) * tphi_ami["commercial_mixed"])
            coeff = 3.0 * z_use / V_NOM_LV
            w_ph = (1.0 / 3.0) - sl / coeff
            out_w[s] = float(w_ph.max())
            v_pred = sl[:, None] * p60[None, :]
            res = (v_ex - v_pred) - (v_ex - v_pred).mean(axis=1, keepdims=True)
            bus_resid_rms[s] = float(np.sqrt(np.mean(res ** 2)))
            continue

        if mode == "raw_vbus_no_pt":
            top10 = np.argsort(p60)[-10:]
            z_res = cfg["r_ohm"] + cfg["x_ohm"] * tphi_ami["residential_heat"]
            w_h = (1.0 / 3.0) - v_ex[:, top10] / ((3.0 * z_res / V_NOM_LV) * p60[None, top10])
            out_w[s] = float(np.mean(w_h.max(axis=0)))
            bus_resid_rms[s] = float(np.sqrt(np.mean(v_ex ** 2)))
            continue

        if mode == "handbook_pf":
            tp_r, tp_c = tphi_hb["residential_heat"], tphi_hb["commercial_mixed"]
        elif mode == "sub_pf":
            q_s = abs(qh_for_subpf[s]) if qh_for_subpf else abs(sd["sub_net_kvarh_m"].sum() / max(sd["sub_kwh_m"].sum(), 1.0)) * p60[pk_h]
            tp_sub = max(0.05, q_s / max(p60[pk_h], 1.0))
            tp_r = tp_c = tp_sub
        else:
            tp_r, tp_c = tphi_ami["residential_heat"], tphi_ami["commercial_mixed"]

        est = opts.get("s3_est", "all")
        if est == "winter":
            mask = WINTER_HOURS
        elif est == "heating":
            mask = HEATING_HOURS
        else:
            mask = np.ones(N_HOURS, dtype=bool)

        if est == "diff":
            X = np.column_stack([np.diff(p_res), np.diff(p_com), np.diff(p_bal)])
            Y = np.diff(v_ex, axis=1).T
            B, *_ = np.linalg.lstsq(X, Y, rcond=None)
            b_res, b_com = B[0], B[1]
        elif est == "two_class":
            X = np.column_stack([np.ones(int(mask.sum())), p_res[mask], p_com[mask]])
            Y = v_ex[:, mask].T
            B, *_ = np.linalg.lstsq(X, Y, rcond=None)
            b_res, b_com = B[1], B[2]
        else:
            X = np.column_stack([np.ones(int(mask.sum())), p_res[mask], p_com[mask], p_bal[mask]])
            Y = v_ex[:, mask].T
            B, *_ = np.linalg.lstsq(X, Y, rcond=None)
            b_res, b_com = B[1], B[2]

        c_res = 3.0 * (cfg["r_ohm"] + cfg["x_ohm"] * tp_r) / V_NOM_LV
        c_com = 3.0 * (cfg["r_ohm"] + cfg["x_ohm"] * tp_c) / V_NOM_LV
        dw_res_hat = -b_res / c_res
        dw_com_hat = -b_com / c_com
        dw_res_hat -= dw_res_hat.mean()
        dw_com_hat -= dw_com_hat.mean()

        if est == "top5_pk":
            top5 = np.argsort(p60)[-5:]
            ws = [float(((1.0 / 3.0) + (dw_res_hat * p_res[h] + dw_com_hat * p_com[h]) / p60[h]).max()) for h in top5]
            out_w[s] = float(np.mean(ws))
        else:
            w_pk = (1.0 / 3.0) + (dw_res_hat * p_res[pk_h] + dw_com_hat * p_com[pk_h]) / p60[pk_h]
            out_w[s] = float(w_pk.max())

        v_pred = b_res[:, None] * p_res[None, :] + b_com[:, None] * p_com[None, :]
        res = (v_ex - v_pred) - (v_ex - v_pred).mean(axis=1, keepdims=True)
        bus_resid_rms[s] = float(np.sqrt(np.mean(res ** 2)))

    if mode == "handbook_pf":
        ami_q_err = _ami_q_rmse(world, tphi_by_cls=tphi_hb)
    elif mode == "sub_pf":
        ami_q_err = _ami_q_rmse(world, tphi_by_sub={s: max(0.05, abs(qh_for_subpf[s]) / max(world["subs"][s]["sub_p60"].max(), 1.0)) for s in ALL_SUBS})
    else:
        ami_q_err = _ami_q_rmse(world, tphi_by_cls=tphi_ami)
    return out_w, bus_resid_rms, tphi_ami, ami_q_err


def evaluate(world, opts=None):
    """Run all three estimation stages and compute internal physics falsification diagnostics."""
    opts = opts or {}
    p15_all, k_ord, comm_flat, comm_cf, R_mats, site_reg_rat, raw_rho = _s1_estimate_all(world, opts)
    qh_all, q_hr_hat = _s2_estimate_all(world, opts)
    w_all, bus_rms, tphi_ami, ami_q_err = _s3_estimate_all(world, opts, qh_for_subpf=qh_all)

    m_k = float(opts.get("mult_kord", 1.0))
    m_q = float(opts.get("mult_q", 1.0))
    m_w = float(opts.get("mult_w_excess", 1.0))
    q15_rule = opts.get("q15_rule", "const_q")

    out = {}
    for s in ALL_SUBS:
        sd = world["subs"][s]
        cfg = sd["cfg"]
        p60_pk = float(sd["sub_p60"].max())
        p15 = p60_pk + m_k * (p15_all[s] - p60_pk)
        q_h = qh_all[s] * m_q
        if q15_rule == "const_q":
            q15 = q_h
        elif q15_rule == "ami_slope":
            q15 = q_h + 0.20 * (p15 - p60_pk)
        else:
            q15 = q_h * (p15 / p60_pk)
        s15 = float(np.sqrt(p15 ** 2 + q15 ** 2))
        w_max = (1.0 / 3.0) + m_w * (w_all[s] - 1.0 / 3.0)
        lim = float(3.0 * w_max * s15)
        load = float(100.0 * lim / cfg["firm_mva"])
        rel = float(max(0.0, lim - 0.85 * cfg["firm_mva"]))
        out[s] = dict(p15=p15, q_h=q_h, q15=q15, s15_tot=s15, w_max=w_max,
                      lim_mva=lim, loading_pct=load, relief_mva=rel)

    # 1. S1 9-point commissioning MAE (MW) directly on monthly max(P_15) - max(P_60) across Fossheim, Lindberg, Solberg x Sep/Oct/Dec
    comm_err = []
    mode = opts.get("s1_mode", "golden")
    form = opts.get("s1_form", "add_raw")
    for r in PQ_COMM_SITES:
        sd = world["subs"][r]
        cands = [r2 for r2 in PQ_COMM_SITES if r2 != r]
        twin = min(cands, key=lambda r2: abs(raw_rho[r2] - raw_rho[r]))
        for m in COMM_MONTHS:
            true_ex, p60_m = _comm_month_obs_ex(sd, m)
            reg_ex = float(np.sum(np.maximum(0.0, sd["feeder_m15"][:, m] - sd["feeder_p60_m"][:, m])))
            if mode == "scada60":
                est_ex = 0.0
            elif mode == "flat_ratio":
                est_ex = p60_m * (comm_flat - 1.0)
            elif mode == "cf_pooled":
                est_ex = comm_cf * reg_ex
            elif mode == "twin_ratio":
                est_ex = site_reg_rat[twin] * reg_ex
            elif mode == "linear_sum":
                est_ex = reg_ex
            elif mode == "rigorous_cf60":
                cf60 = p60_m / float(sd["f_p60"][:, HOUR_MONTH == m].max(axis=1).sum())
                est_ex = cf60 * float(sd["feeder_m15"][:, m].sum()) - p60_m
            else:
                rq = _quad_excess(sd, R_mats[r], [m], form=form, indep=(mode == "indep_quad"))
                est_ex = k_ord * rq
            comm_err.append(abs(est_ex - true_ex))
    s1_comm_mae = float(np.mean(comm_err))

    # 2. S2 internal physics balance: hourly LV voltage balance RMSE (mV) + 12-month kVARh conservation (MVAr)
    s2_v_errs, s2_m_errs = [], []
    for cid, c_info in world["corridors"].items():
        v_gsp = world["gsp_v"][c_info["gsp"]]
        segs = c_info["segs"]
        subs = [seg[1] for seg in segs]
        v_cur = v_gsp.copy()
        for si, (_f, s, l_km, r_km, x_km) in enumerate(segs):
            ds = subs[si:]
            pf = sum(world["subs"][d]["sub_p60"] for d in ds)
            qf = sum(q_hr_hat[d] for d in ds)
            v_cur = v_cur - (l_km * r_km * pf + l_km * x_km * qf) / V_NOM_HV
            sd = world["subs"][s]
            cfg = sd["cfg"]
            tau = (V_NOM_LV / V_NOM_HV) * (1.0 + TAP_STEP * sd["tap_step_int"])
            v_pred = v_cur * tau - (cfg["r_ohm"] * sd["sub_p60"] + cfg["x_ohm"] * q_hr_hat[s]) / V_NOM_LV
            valid = ~np.isnan(sd["v_lv_meas"])
            err = (sd["v_lv_meas"][valid] - v_pred[valid]) - float(np.mean(sd["v_lv_meas"][valid] - v_pred[valid]))
            if s in TARGETS:
                s2_v_errs.append(float(np.sqrt(np.mean(err ** 2))) * 1000.0)
                m_err = np.mean([abs(float(q_hr_hat[s][HOUR_MONTH == mm].mean()) - sd["sub_net_kvarh_m"][mm] / (1000.0 * int((HOUR_MONTH == mm).sum()))) for mm in range(12)])
                s2_m_errs.append(float(m_err))
    s2_vlv_mv = float(np.mean(s2_v_errs))
    s2_mvar_err = float(np.mean(s2_m_errs))
    s3_bus_mv = float(np.mean([bus_rms[s] * 1000.0 for s in TARGETS]))

    # Dimensionless physical-balance residual index (observes_target=False)
    phys_idx = (s1_comm_mae / 0.35) + (s2_vlv_mv / 8.0) + (s2_mvar_err / 0.40) + (s3_bus_mv / 2.5) + (ami_q_err / 2.5)

    return out, dict(
        k_ord=k_ord, comm_flat=comm_flat, comm_cf=comm_cf, site_reg_rat=site_reg_rat,
        tan_phi_res=tphi_ami["residential_heat"], tan_phi_com=tphi_ami["commercial_mixed"],
        s1_comm_mae=s1_comm_mae, s2_vlv_mv=s2_vlv_mv, s2_mvar_err=s2_mvar_err,
        s3_bus_mv=s3_bus_mv, s3_amiq=ami_q_err, phys_idx=phys_idx,
    )


def _agg_components(res):
    c1 = sum(res[s]["p15"] for s in TARGETS)
    c2 = sum(res[s]["q_h"] for s in TARGETS)
    c3 = 100.0 * sum(res[s]["w_max"] for s in TARGETS) / len(TARGETS)
    return c1, c2, c3


# --- HONEST VARIANT BATTERY (27 variants across all 3 stumps + Q15) ---

FAMILY = [
    ("golden", {}),
    ("S1 all-12 months", {"s1_months": "all"}),
    ("S1 DJF 3-month", {"s1_months": "djf"}),
    ("S1 peak month only", {"s1_months": "peak_m"}),
    ("S1 scaled additive", {"s1_form": "add"}),
    ("S1 multiplicative excess", {"s1_form": "mult"}),
    ("S1 winter innov corr", {"s1_corr_win": "winter"}),
    ("S1 5-PC strip", {"s1_innov": "pca5"}),
    ("S1 6-PC strip", {"s1_innov": "pca6"}),
    ("S1 ref_log strip", {"s1_innov": "ref_log"}),
    ("S1 ref_diff strip", {"s1_innov": "ref_diff"}),
    ("S1 unit k_ord=1.0", {"s1_kord": "unit"}),
    ("S1 mean-ratio comm k_ord", {"s1_kord": "mean"}),
    ("Q15 ami_slope", {"q15_rule": "ami_slope"}),
    ("Q15 const_pf", {"q15_rule": "const_pf"}),
    ("S2 winter anchor", {"s2_anchor": "winter"}),
    ("S2 full-year anchor", {"s2_anchor": "full_year"}),
    ("S2 1-step M_bar", {"s2_solve": "mbar_only"}),
    ("S2 meas V_lv", {"s2_vscale": "vlv"}),
    ("S2 fit20 peak Q", {"s2_peak_agg": "fit20"}),
    ("S2 single-hr peak Q", {"s2_peak_agg": "single"}),
    ("S3 winter bus-sag", {"s3_est": "winter"}),
    ("S3 heating bus-sag", {"s3_est": "heating"}),
    ("S3 diff bus-sag", {"s3_est": "diff"}),
    ("S3 2-class bus-sag", {"s3_est": "two_class"}),
    ("S3 top-5 peak w_max", {"s3_est": "top5_pk"}),
    ("S3 winter AMI tan_phi", {"s3_ami_win": "winter"}),
]

HURRIED = {
    "S1": {"s1_mode": "scada60"},
    "S2": {"s2_mode": "net_kvarh"},
    "S3": {"s3_mode": "ami_only_bal"},
}

DIRECT = {"s1_mode": "scada60", "s2_mode": "net_kvarh", "s3_mode": "balanced"}
RIGOROUS = {"s1_mode": "cf_pooled", "s2_mode": "monthly_qp_winter", "s3_mode": "ami_only_bal"}
RESPONSE1_V2 = {"s1_mode": "register_rho", "s2_mode": "monthly_qp", "s3_mode": "scalar_ols"}

RUN_ROUTES_OPTS = {
    "generous":   {"s1_mode": "linear_sum", "s2_mode": "class_nominal", "s3_mode": "evening_cutoff_zres"},
    "calibrated": {"s1_mode": "register_rho", "s2_mode": "monthly_qp_winter", "s3_mode": "handbook_pf"},
    "hedge":      {"s1_mode": "indep_quad", "s2_mode": "net_kvarh", "s3_mode": "ami_only_bal"},
    "cutoff":     {"s1_mode": "pca1", "s2_mode": "winter_kvarh", "s3_mode": "evening_cutoff_ols"},
}

RIVAL_OPTS = {
    "s1_scada60": {"s1_mode": "scada60"},
    "s1_register_rho": {"s1_mode": "register_rho"},
    "s1_pca1": {"s1_mode": "pca1"},
    "s1_pca2": {"s1_mode": "pca2"},
    "s1_raw_corr": {"s1_mode": "raw_corr"},
    "s1_indep_quad": {"s1_mode": "indep_quad"},
    "s1_cf_pooled": {"s1_mode": "cf_pooled"},
    "s1_twin_ratio": {"s1_mode": "twin_ratio"},
    "s1_flat_ratio": {"s1_mode": "flat_ratio"},
    "s1_linear_sum": {"s1_mode": "linear_sum"},
    "s2_net_kvarh": {"s2_mode": "net_kvarh"},
    "s2_winter_kvarh": {"s2_mode": "winter_kvarh"},
    "s2_monthly_qp": {"s2_mode": "monthly_qp"},
    "s2_monthly_win": {"s2_mode": "monthly_qp_winter"},
    "s2_monthly_quad": {"s2_mode": "monthly_quad"},
    "s2_class_pf": {"s2_mode": "class_nominal"},
    "s2_targets_only": {"s2_mode": "targets_only_corridor"},
    "s2_local_dv": {"s2_mode": "local_dv"},
    "s2_rp_only": {"s2_mode": "rp_only"},
    "s2_raw_dv": {"s2_mode": "raw_dv_no_demean"},
    "s3_gis": {"s3_mode": "gis"},
    "s3_ami_only": {"s3_mode": "ami_only_bal"},
    "s3_ami_plus_gis": {"s3_mode": "ami_plus_gis"},
    "s3_ami_grossup": {"s3_mode": "ami_grossup"},
    "s3_scalar_ols": {"s3_mode": "scalar_ols"},
    "s3_evening_cut": {"s3_mode": "evening_cutoff_ols"},
    "s3_even_zres": {"s3_mode": "evening_cutoff_zres"},
    "s3_handbook_pf": {"s3_mode": "handbook_pf"},
    "s3_sub_pf": {"s3_mode": "sub_pf"},
    "s3_raw_vbus": {"s3_mode": "raw_vbus_no_pt"},
    "direct": DIRECT,
    "rigorous": RIGOROUS,
    "response1_v2": RESPONSE1_V2,
    "run_generous": RUN_ROUTES_OPTS["generous"],
    "run_calibrated": RUN_ROUTES_OPTS["calibrated"],
    "run_hedge": RUN_ROUTES_OPTS["hedge"],
    "run_cutoff": RUN_ROUTES_OPTS["cutoff"],
    "reflex": {"s1_mode": "scada60", "s2_mode": "net_kvarh", "s3_mode": "ami_only_bal"},
}


def build_spec(world=None):
    """Build the full corelib spec from world arrays (works on both simulated world and cut pack_world)."""
    w = world if world is not None else simulate()
    gold_res, gold_p = evaluate(w, {})
    fam_res = [evaluate(w, opts)[0] for _, opts in FAMILY]

    lat_res = {}
    for r in range(1, 4):
        for comb in itertools.combinations(("S1", "S2", "S3"), r):
            opts = {}
            for k in comb:
                opts.update(HURRIED[k])
            lat_res["+".join(comb)] = evaluate(w, opts)[0]

    rivals = {}
    rival_diag = {}
    for rname, ropts in RIVAL_OPTS.items():
        rr, rp = evaluate(w, ropts)
        rivals[rname] = rr
        rival_diag[rname] = rp

    dir_res = rivals["direct"]
    rig_res = rivals["rigorous"]
    r1_res = rivals["response1_v2"]
    run_res = {rn: rivals[f"run_{rn}"] for rn in ("generous", "calibrated", "hedge", "cutoff")}

    g_c1, g_c2, g_c3 = _agg_components(gold_res)
    g_rel = sum(gold_res[s]["relief_mva"] for s in TARGETS)
    fam_c1 = [_agg_components(fr)[0] for fr in fam_res]
    fam_c2 = [_agg_components(fr)[1] for fr in fam_res]
    fam_c3 = [_agg_components(fr)[2] for fr in fam_res]
    fam_rel = [sum(fr[s]["relief_mva"] for s in TARGETS) for fr in fam_res]

    spec = {
        "task": "task26",
        "call": "lines",
        "members": {
            s: {
                "lines": [LINE_P2, LINE_P1],
                "truth": w["subs"][s]["truth"]["loading_pct"],
                "golden": gold_res[s]["loading_pct"],
                "family": [fr[s]["loading_pct"] for fr in fam_res],
                "routes": {
                    "direct": dir_res[s]["loading_pct"],
                    "rigorous": rig_res[s]["loading_pct"],
                    "response1_v2": r1_res[s]["loading_pct"],
                },
            }
            for s in TARGETS
        },
        "stumps": {
            "S1": {
                "axis": "unit", "opens": "Drangvik", "steps_left": 5, "precedents": ["L22", "L24", "L58"],
                "said_out_loud": "Substation 15-minute active peaks depend on cross-feeder synchronization hidden under seasonal register modulation and shared customer-class hourly shapes.",
                "sides": {"over": {s: rivals["s1_linear_sum"][s]["loading_pct"] for s in TARGETS}},
            },
            "S2": {
                "axis": "what", "opens": "Kvernholm", "steps_left": 5, "precedents": ["L16", "L43", "L44", "L48"],
                "said_out_loud": "Peak-hour reactive demand is hidden behind winter fixed capacitors and peak-only switched capacitors and must be inverted simultaneously along all four 66 kV corridors including upstream modernized hubs.",
                "sides": {"over": {s: rivals["s2_local_dv"][s]["loading_pct"] for s in TARGETS}},
            },
            "S3": {
                "axis": "who", "opens": "Raudfjord", "steps_left": 5, "precedents": ["L28", "L56", "L57"],
                "said_out_loud": "Evening-peak heaviest-phase load share across AMI and unmetered legacy laterals must be inverted from multi-class three-phase bus voltage-sag regression using AMI-metered per-class reactive impedance ratios.",
                "sides": {"over": {s: rivals["s3_even_zres"][s]["loading_pct"] for s in TARGETS}},
            },
        },
        "lattice": {k: {s: v[s]["loading_pct"] for s in TARGETS} for k, v in lat_res.items()},
        "falsification": {
            "check": "Composite physical-balance residual index (Sep/Oct/Dec 3-hub active commissioning surge + 66kV/LV voltage balance + 12-mo kVARh conservation + 3-phase bus-sag RMSE + AMI q_kvar consistency)",
            "observes_target": False,
            "truth": 0.0,
            "golden": gold_p["phys_idx"],
            "rivals": {k: rival_diag[k]["phys_idx"] for k in RIVAL_OPTS},
        },
        "run_routes": {rn: {s: rv[s]["loading_pct"] for s in TARGETS} for rn, rv in run_res.items()},
        "figures": [
            {
                "id": "C1_total_p15_mw", "block": "component", "weight": 1.0,
                "golden": g_c1, "family": fam_c1,
                "lattice": {k: _agg_components(v)[0] for k, v in lat_res.items()},
                "routes": {"rigorous": _agg_components(rig_res)[0], "response1_v2": _agg_components(r1_res)[0],
                           **{rn: _agg_components(rv)[0] for rn, rv in run_res.items()}},
            },
            {
                "id": "C2_total_qpeak_mvar", "block": "component", "weight": 1.0,
                "golden": g_c2, "family": fam_c2,
                "lattice": {k: _agg_components(v)[1] for k, v in lat_res.items()},
                "routes": {"rigorous": _agg_components(rig_res)[1], "response1_v2": _agg_components(r1_res)[1],
                           **{rn: _agg_components(rv)[1] for rn, rv in run_res.items()}},
            },
            {
                "id": "C3_mean_lim_phase_pct", "block": "component", "weight": 1.0,
                "golden": g_c3, "family": fam_c3,
                "lattice": {k: _agg_components(v)[2] for k, v in lat_res.items()},
                "routes": {"rigorous": _agg_components(rig_res)[2], "response1_v2": _agg_components(r1_res)[2],
                           **{rn: _agg_components(rv)[2] for rn, rv in run_res.items()}},
            },
            {
                "id": "A_total_relief_mva", "block": "ask", "weight": 2.0,
                "golden": g_rel, "family": fam_rel,
                "lattice": {k: sum(v[s]["relief_mva"] for s in TARGETS) for k, v in lat_res.items()},
                "routes": {"rigorous": sum(rig_res[s]["relief_mva"] for s in TARGETS),
                           "response1_v2": sum(r1_res[s]["relief_mva"] for s in TARGETS),
                           **{rn: sum(rv[s]["relief_mva"] for s in TARGETS) for rn, rv in run_res.items()}},
            },
            *[
                {
                    "id": f"A_{s}_loading_pct", "block": "ask", "weight": 1.0, "member": s,
                    "routes": {"response1_v2": r1_res[s]["loading_pct"], **{rn: rv[s]["loading_pct"] for rn, rv in run_res.items()}},
                }
                for s in TARGETS
            ],
        ],
    }
    return spec, w, gold_res, lat_res, dir_res, rig_res, gold_p, rivals, rival_diag


def main(argv=None):
    argv = argv or sys.argv[1:]
    spec, w, gold_res, _lat, _dir, _rig, gold_p, rivals, rival_diag = build_spec()
    rc = corelib.run(spec)

    if "--detail" in argv:
        print("\n--- Detail (golden vs truth, physics diagnostics, RESPONSE1_V2) ---")
        print(f"k_ord={gold_p['k_ord']:.4f}  tan_phi_res={gold_p['tan_phi_res']:.4f}  tan_phi_com={gold_p['tan_phi_com']:.4f}  "
              f"comm_mae={gold_p['s1_comm_mae']:.3f} MW  vlv_rmse={gold_p['s2_vlv_mv']:.1f} V  "
              f"kvarh_err={gold_p['s2_mvar_err']:.2f} MVAr  bus_rmse={gold_p['s3_bus_mv']:.1f} V  "
              f"ami_q={gold_p['s3_amiq']:.2f} kVAr  phys_idx={gold_p['phys_idx']:.2f}")
        for s in TARGETS:
            t = w["subs"][s]["truth"]
            g = gold_res[s]
            print(f"  {s:10s}: truth={t['loading_pct']:6.2f}%  gold={g['loading_pct']:6.2f}%  "
                  f"P15={g['p15']:5.2f}({t['p15_peak']:5.2f})  Q={g['q_h']:+6.2f}({t['q_peak_h']:+6.2f})  "
                  f"w={100*g['w_max']:5.2f}%({100*t['w_max']:5.2f}%)  rel={g['relief_mva']:5.2f}")
        figs, _ = corelib._figures(spec, spec["lattice"])
        gcall = corelib._calls(spec, {s: gold_res[s]["loading_pct"] for s in TARGETS})
        r1_score, _ = corelib._route_score(spec, figs, "response1_v2", gcall)
        print(f"RESPONSE1_V2 exact rubric score: {r1_score:.1f}/100")

    if "--forcing" in argv:
        gcall = corelib._calls(spec, {s: gold_res[s]["loading_pct"] for s in TARGETS})
        ok = True
        print("\n--- Forcing +/-20% perturbations ---")
        for name, opts in [
            ("k_ord -20%", {"mult_kord": 0.8}), ("k_ord +20%", {"mult_kord": 1.2}),
            ("Q_peak -20%", {"mult_q": 0.8}), ("Q_peak +20%", {"mult_q": 1.2}),
            ("phase_excess -20%", {"mult_w_excess": 0.8}), ("phase_excess +20%", {"mult_w_excess": 1.2}),
        ]:
            pr, _ = evaluate(w, opts)
            pcall = corelib._calls(spec, {s: pr[s]["loading_pct"] for s in TARGETS})
            holds = (pcall == gcall)
            ok = ok and holds
            print(f"  {name:18s}: {'HOLD' if holds else 'FLIP'} | " + " ".join(f"{s[:4]}={pr[s]['loading_pct']:.1f}" for s in TARGETS))
        print("FORCING:", "PASS" if ok else "FAIL")
        if not ok:
            rc = 1
    sys.exit(rc)


if __name__ == "__main__":
    main()
