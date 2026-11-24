#!/usr/bin/env python3
"""task28/generator/core.py (v3): Barlavento SWRO Desalination Plant (Algarve, Portugal)
Level 5 v4-Hardened Anomaly Detection & Diagnostics Core (Physical & Environmental Sciences /
process-control-measurement-systems).

Simulates 8 parallel seawater reverse-osmosis (SWRO) membrane trains (TR01..TR08) across
two treatment bays (North: TR01..TR04, South: TR05..TR08) over non-leap 2026 (365 days =
8,760 hours = 35,040 fifteen-minute intervals = 2,190 four-hour diagnostic blocks per train)
and diagnoses which trains reach Engineering Protocol SWRO-Q27's 400.0-hour 2027 vessel
overhaul criterion and the resulting excess desalination energy penalty in MWh
(420 / 360 / 540 / 300 kWh/h divided by 1,000).

Four genuinely independent, unannounced, non-closed physical observation-process stumps
engineered to defeat both Round-2 3.5-hour frontier solvers (Response 1 and Response 2)
and pass Holistic Audit v4 hardened bars (v4_hardened=True, coded one_fact_shortcut per
stump, zero construction tells, tight convergence across 30+ honest variants):

  S1 (unit) - support_effect + conservation_residual_attribution:
              Spiegler-Kedem / Fickian solute mass-flux conservation inside 4h/8h
              flow-proportional lab boron composite bottles:
                C_t = alpha_{u,q} + (mu_{J,u} + eta_t) / Q_t   (eta_t ~ stationary AR(1))
                M_k = Q_bar_k * C_comp_k = alpha_{u,q} * Q_bar_k + mu_{J,u} + eta_bar_k + Q_bar_k * nu_lab
              Concentration variance scales as (sigma_J / Q_t)^2. Both Response 1's 6-block
              homoscedastic AR(1) AND Response 2's exact (a + c/Q) homoscedastic concentration
              AR(1) under-predict night low-flow boron variance on TR01 (drops < 400 h) while
              over-spreading daytime variance on TR04 (flips TR04 > 400 h). Flux-space i.i.d.
              sqrt(m) over-correction also flips TR04 > 400 h.

  S2 (when) - asynchronous_measurement_covariance + non_additive_aggregation:
              Variable-flow cumulative-volume Phi(t) two-path bimodal DAF/DMF hydraulic
              mixing across parallel fast-bypass (f_fast at V_fast) and main baffled
              (1 - f_fast at V_main) paths with identical coastal seawater TEP baseline
              across all 8 trains:
                c_out(Phi) = f_fast * c_in(Phi - V_fast) + (1 - f_fast) * c_in(Phi - V_main) + noise
                X_arr(Phi) = f_fast * X_in(Phi - V_fast) + (1 - f_fast) * X_in(Phi - V_main)
              Both Response 1 & Response 2's Round-2 fixed wall-clock lag (TEP->stress CCF/ARX)
              collapse high-swing TR02 below 400 h AND omit two-path dilution on TR05 (flipping
              TR05 > 400 h). Even 1D single-plug V_eff (one_fact_shortcut) still omits two-path
              dilution on TR05 (flipping TR05 > 400 h), while comonotonic pairing also flips TR05.

  S3 (what) - rival_process_by_state_dependence + latent_structure_estimation:
              Continuous post-CIP fouling re-accumulation kinetics across dual chemical wash
              recipes (CIP_ALK_pH11 vs CIP_ACID_pH2, with zero 120 h window hint in config)
              where reversible mineral spacer crust (F_min) shares the exact same single-block
              (D1, D2, D3) emission vector as persistent structural breaches (S):
                w_bio(t) = pi_bio * (1 - exp(-dt_alk / tau_bio))
                w_MS(t)  = pi_S + pi_min * (1 - exp(-dt_acid / tau_min))
              Response 1's unconditioned 3-class LCA cannot separate F_min from S at all
              (blows up TR03 > 1,000 h). Response 2's static 120h (or 72h/48h) post-CIP 4-class
              EM (one_fact_shortcut) misses fast mineral re-nucleation (tau_min ~ 22 h) on TR03
              (blows up TR03 > 900 h). Over-corrections (unanimous 3-of-3, raw post-acid D3)
              drop damaged TR06 below 400 h.

  S4 (who)  - unlabelled_pool_apportioned_by_varying_mix + conservation_residual_attribution:
              Shared North/South Bay common permeate collector TDS (> 450 mg/L individual train
              breakthrough) recorded only at the 4-train blended header:
                T_bay(t) = sum_{u in bay} w_{u,t} T_{u,t} + eps_meter(t),  w_{u,t} = Q_{u,t}/sum Q
              With staggered bay flow schedules, OLS recovers exact train means mu_{T,u,q}
              (TR05 has the highest mean 398 mg/L but tiny SD 16 mg/L; TR08 has moderate mean
              358 mg/L but large volatility 62 mg/L). Direct bay-header exceedances miss TR08.
              Standard OLS means + equal-train variance pooling (one_fact_shortcut) misses
              volatile TR08 (< 400 h) AND false-flags steady high-mean TR05 (> 400 h).
              Heteroscedastic Gaussian variance-component MLE on r_bay(t)^2 vs sum w_{u,t}^2 sigma_u^2
              identifies every train's volatility uniquely (Delta-BIC > 800).
"""
import math
import os
import sys

import numpy as np
from scipy.optimize import minimize
from scipy.special import erfc

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(REPO, ".agents", "skills", "stumping"))
import corelib  # noqa: E402

SEED = 2803
TRAINS = ["TR01", "TR02", "TR03", "TR04", "TR05", "TR06", "TR07", "TR08"]
BAYS = {
    "North": ["TR01", "TR02", "TR03", "TR04"],
    "South": ["TR05", "TR06", "TR07", "TR08"],
}
TRAIN_BAY = {u: ("North" if u in BAYS["North"] else "South") for u in TRAINS}
DAYS_2026 = 365
HOURS_2026 = DAYS_2026 * 24           # 8,760
STEPS_15M = DAYS_2026 * 96            # 35,040
BLOCKS_4H = DAYS_2026 * 6             # 2,190
Q_DAYS = (90, 91, 92, 92)
Q_HOURS = tuple(d * 24 for d in Q_DAYS)
Q_EDGES_H = (0, 2160, 4344, 6552, 8760)
BURN_IN_15M = 32                      # first 8 hours of Jan 1, 2026 (Clause 2.2)

# Filed engineering protocol parameters (swro_integrity_standard_q27.pdf)
THRESHOLD = 400.0                     # Clause 3.1
BORON_LIMIT = 0.50                    # Clause 2.1 (mg/L, 1-hour basis)
SCALING_X_LIM = 1.50                  # Clause 2.2 (arrived algal-TEP index)
SCALING_Y_LIM = 1.50                  # Clause 2.2 (RO-feed stress index)
TDS_LIMIT = 450.0                     # Clause 2.4 (mg/L, 1-hour basis)
LAB_BORON_SD = 0.004                  # lims_qa_certificate_2026.pdf
TDS_METER_SD = 3.5                    # scada_bay_config_2026.json / lims_qa_certificate_2026.pdf
COND_PROBE_SD = 0.34                  # inline seawater conductivity probe noise (mS/cm)

# Clause 4.3 Mode-Specific Excess Desalination Energy Penalty Rates (kWh per anomalous hour)
ENERGY_BORON_KWH = 420.0
ENERGY_SCALING_KWH = 360.0
ENERGY_STRUCT_KWH = 540.0
ENERGY_TDS_KWH = 300.0

# Annex A Uniform 2027 Operating Plan Multipliers (operating_plan_2027.csv)
PLAN_BORON_TEMP_Q = (1.05, 1.14, 1.32, 1.09)
PLAN_SCALING_REC_Q = (1.03, 1.12, 1.28, 1.07)
PLAN_TDS_SAL_Q = (1.04, 1.12, 1.26, 1.08)
PLAN_SCHED_RATIO = {
    "TR01": (1.08, 1.14, 1.22, 1.10),
    "TR02": (1.10, 1.15, 1.24, 1.12),
    "TR03": (1.06, 1.10, 1.18, 1.08),
    "TR04": (1.08, 1.12, 1.20, 1.09),
    "TR05": (1.07, 1.12, 1.21, 1.09),
    "TR06": (1.10, 1.14, 1.20, 1.11),
    "TR07": (1.11, 1.17, 1.25, 1.13),
    "TR08": (1.09, 1.14, 1.22, 1.10),
}

# S3 physical channel emission probabilities (D1=salt_passage, D2=stage_dp, D3=acoustic_bypass)
# Crucial: P_FMIN == P_STRUCT on a single 4-hour block (indistinguishable without CIP kinetics!)
P_CLEAN = (0.012, 0.008, 0.008)
P_FBIO = (0.68, 0.90, 0.008)
P_FMIN = (0.85, 0.16, 0.72)
P_STRUCT = (0.85, 0.16, 0.72)

# Per-train physical parameters across all 4 independent mechanisms
# Staggered 6-hour bay load-balancing troughs (q_tc = 3, 9, 15, 21) in both North & South bays
# ensure orthogonal flow shares w_{u,t} for S4 AND strong diurnal flow swings for S1 & S2.
WORLD = {
    "TR01": {  # OVERHAUL (~510 h): OPENED BY S1 (non-negative composites > 0.030 mg/L; worst-case OU MLE >= 445; R1 & R2 < 370!)
        "q_hi": 695.0, "q_drop": 420.0, "q_tc": 3.0, "q_tw": 2.3, "q_mode": "trough",
        "b_alpha": 0.170, "b_mu_j": 50.0, "b_sd_j": 44.5, "b_lam": 1.10,
        "v_nom": 1200.0, "f_fast": 0.18, "v_fast": 340.0, "v_main": 1340.0, "y_mu": -0.82, "y_coup": 0.95,
        "pi_bio": 0.015, "tau_bio": 60.0, "pi_min": 0.015, "tau_min": 45.0, "pi_s": 0.0000,
        "tds_mu": 362.0, "tds_sd": 37.0,
    },
    "TR02": {  # OVERHAUL (~605 h): OPENED BY S2 (moves under S1, S2, S3, S4; V_nom & R2 drop < 370!)
        "q_hi": 680.0, "q_drop": 390.0, "q_tc": 9.0, "q_tw": 3.6, "q_mode": "ramp",
        "b_alpha": 0.228, "b_mu_j": 24.0, "b_sd_j": 30.0, "b_lam": 1.0,
        "v_nom": 1050.0, "f_fast": 0.08, "v_fast": 340.0, "v_main": 1600.0, "y_mu": -1.10, "y_coup": 1.72,
        "pi_bio": 0.015, "tau_bio": 60.0, "pi_min": 0.015, "tau_min": 45.0, "pi_s": 0.0000,
        "tds_mu": 348.0, "tds_sd": 36.0,
    },
    "TR03": {  # MONITOR (~236 h): OPENED BY S3 (moves under S1, S3, S4; Truth < 395; max variant < 325!)
        "q_hi": 645.0, "q_drop": 310.0, "q_tc": 15.0, "q_tw": 2.8, "q_mode": "trough",
        "b_alpha": 0.268, "b_mu_j": 26.0, "b_sd_j": 31.0, "b_lam": 1.0,
        "v_nom": 1180.0, "f_fast": 0.36, "v_fast": 350.0, "v_main": 1280.0, "y_mu": -1.42, "y_coup": 1.38,
        "pi_bio": 0.180, "tau_bio": 55.0, "pi_min": 0.400, "tau_min": 22.0, "pi_s": 0.0000,
        "tds_mu": 371.0, "tds_sd": 35.0,
    },
    "TR04": {  # MONITOR (~335 h): S1 OVER_S1 (> 900!) trap (moves cleanly under S1, S2, S3, AND S4!)
        "q_hi": 665.0, "q_drop": 315.0, "q_tc": 21.0, "q_tw": 1.8, "q_mode": "trough",
        "b_alpha": 0.304, "b_mu_j": 15.0, "b_sd_j": 34.0, "b_lam": 7.5,
        "v_nom": 1220.0, "f_fast": 0.36, "v_fast": 360.0, "v_main": 1300.0, "y_mu": -0.50, "y_coup": 1.05,
        "pi_bio": 0.030, "tau_bio": 60.0, "pi_min": 0.025, "tau_min": 45.0, "pi_s": 0.0000,
        "tds_mu": 361.0, "tds_sd": 33.0,
    },
    "TR05": {  # MONITOR (~232 h): S2 (lag/single-plug > 440) + S4 (eq-var > 640) trap; Kalman LRT >= 8.2 against 400 h!
        "q_hi": 640.0, "q_drop": 310.0, "q_tc": 3.0, "q_tw": 2.8, "q_mode": "trough",
        "b_alpha": 0.244, "b_mu_j": 25.0, "b_sd_j": 32.0, "b_lam": 1.0,
        "v_nom": 1420.0, "f_fast": 0.48, "v_fast": 320.0, "v_main": 1460.0, "y_mu": 0.90, "y_coup": 0.58,
        "pi_bio": 0.080, "tau_bio": 60.0, "pi_min": 0.055, "tau_min": 45.0, "pi_s": 0.0000,
        "tds_mu": 371.0, "tds_sd": 9.5,
    },
    "TR06": {  # OVERHAUL (~931 h, #2 cleanly above TR08): retained by S3 (pi_s=0.075 -> ~804 h Struct; unanimous < 340!)
        "q_hi": 650.0, "q_drop": 315.0, "q_tc": 9.0, "q_tw": 2.8, "q_mode": "trough",
        "b_alpha": 0.228, "b_mu_j": 26.0, "b_sd_j": 26.0, "b_lam": 1.0,
        "v_nom": 1240.0, "f_fast": 0.34, "v_fast": 360.0, "v_main": 1320.0, "y_mu": -0.64, "y_coup": 0.88,
        "pi_bio": 0.140, "tau_bio": 60.0, "pi_min": 0.140, "tau_min": 55.0, "pi_s": 0.0750,
        "tds_mu": 350.0, "tds_sd": 31.0,
    },
    "TR07": {  # OVERHAUL (~1,493 h, #1 cleanly above TR06): high anchor moving cleanly under ALL 4 stumps & Direct >> band!
        "q_hi": 635.0, "q_drop": 315.0, "q_tc": 15.0, "q_tw": 3.2, "q_mode": "ramp",
        "b_alpha": 0.258, "b_mu_j": 38.0, "b_sd_j": 35.0, "b_lam": 0.90,
        "v_nom": 1420.0, "f_fast": 0.12, "v_fast": 360.0, "v_main": 1540.0, "y_mu": -0.30, "y_coup": 1.90,
        "pi_bio": 0.340, "tau_bio": 55.0, "pi_min": 0.040, "tau_min": 45.0, "pi_s": 0.0000,
        "tds_mu": 380.0, "tds_sd": 41.0,
    },
    "TR08": {  # OVERHAUL (~759 h, #3 cleanly below TR06): OPENED BY S4 (non-negative composites > 0.093 mg/L; R2 & dS4 < 385!)
        "q_hi": 645.0, "q_drop": 315.0, "q_tc": 21.0, "q_tw": 2.8, "q_mode": "trough",
        "b_alpha": 0.190, "b_mu_j": 34.0, "b_sd_j": 35.0, "b_lam": 1.0,
        "v_nom": 1120.0, "f_fast": 0.16, "v_fast": 340.0, "v_main": 1340.0, "y_mu": -1.15, "y_coup": 1.45,
        "pi_bio": 0.030, "tau_bio": 60.0, "pi_min": 0.025, "tau_min": 45.0, "pi_s": 0.0000,
        "tds_mu": 353.0, "tds_sd": 53.0,
    },
}


def _norm_sf(z):
    return 0.5 * erfc(np.asarray(z, dtype=float) / math.sqrt(2.0))


def _indep_dist_vec(p):
    p1, p2, p3 = p
    out = np.empty(8, dtype=float)
    for k in range(8):
        b1, b2, b3 = (k >> 2) & 1, (k >> 1) & 1, k & 1
        out[k] = (p1 if b1 else 1.0 - p1) * (p2 if b2 else 1.0 - p2) * (p3 if b3 else 1.0 - p3)
    return out


def _soft_clamp(x, lo=230.0, hi=770.0, scale=24.0):
    """True C-infinity softplus safety barrier (overflow-safe, zero flat clamps or repeated ceilings)."""
    z_lo = (x - lo) / scale
    y = lo + scale * np.where(z_lo > 20.0, z_lo, np.log1p(np.exp(np.minimum(z_lo, 20.0))))
    z_hi = (hi - y) / scale
    return hi - scale * np.where(z_hi > 20.0, z_hi, np.log1p(np.exp(np.minimum(z_hi, 20.0))))


def _q_index_hour():
    q = np.empty(HOURS_2026, dtype=np.int32)
    for qi in range(4):
        q[Q_EDGES_H[qi]:Q_EDGES_H[qi + 1]] = qi
    return q


def _q_index_15m():
    return np.repeat(_q_index_hour(), 4)


def _q_index_4h():
    return _q_index_hour()[::4]


def _ar1_fg(phi, m):
    if m == 1:
        return 1.0, phi
    if abs(1.0 - phi) < 1e-8:
        return 1.0, 1.0
    t = 0.0
    for k in range(1, m):
        t += (m - k) * (phi ** k)
    f_m = (m + 2.0 * t) / (m * m)
    g_m = 0.0
    for i in range(m):
        for j in range(m):
            g_m += phi ** (m + j - i)
    g_m /= (m * m)
    return f_m, g_m


def _ou_fg(lam, m):
    def _f_raw(h):
        x = h / lam
        if x < 1e-6:
            return 1.0 - x / 3.0
        return 2.0 * (x - 1.0 + math.exp(-x)) / (x * x)
    f1 = _f_raw(1.0)
    fm = _f_raw(float(m))
    x = m / lam
    if x < 1e-6:
        gm = 1.0 - x
    else:
        e = math.exp(-x)
        gm = ((1.0 - e) ** 2) / (x * x)
    return fm / f1, gm / f1


def simulate_world(seed=SEED):
    """Generate the complete 2026 Barlavento SWRO physical process (8 trains, 4 modes)."""
    rng = np.random.default_rng(seed)
    rng_s3 = np.random.default_rng(seed)
    n_h = HOURS_2026
    n_15 = STEPS_15M
    n_4h = BLOCKS_4H
    q_idx_h = _q_index_hour()
    q_idx_15 = _q_index_15m()
    q_idx_4h = _q_index_4h()
    hours = np.arange(n_h, dtype=float)
    hod = hours % 24.0
    doy = hours // 24.0

    # Shared coastal seawater conductivity & shared coastal algal-TEP baseline (same Algarve intake!)
    t15_h = np.arange(n_15, dtype=float) / 4.0
    tidal = (
        1.15 * np.sin(2.0 * math.pi * t15_h / 12.42)
        + 0.72 * np.cos(2.0 * math.pi * t15_h / 24.84 + 0.5)
        + 0.48 * np.sin(2.0 * math.pi * t15_h / 168.0 + 1.1)
    )
    # Synoptic conductivity AR(1)
    phi_c = math.exp(-0.25 / 1.8)
    s_c = 1.35 * math.sqrt(1.0 - phi_c * phi_c)
    c_syn = np.empty(n_15, dtype=float)
    z_c = rng.normal(0.0, 1.0, n_15)
    v = 0.0
    for i in range(n_15):
        v = phi_c * v + s_c * z_c[i]
        c_syn[i] = v
    c_coastal = 52.0 + tidal + c_syn

    # Coastal algal-TEP seasonal + storm baseline (mean ~ 0, SD ~ 1 across ALL 8 trains!)
    # Short burst scale tau_X = 0.85 h so variable-flow advection & two-path mixing separate cleanly!
    phi_x = math.exp(-0.25 / 0.85)
    s_x = 0.96 * math.sqrt(1.0 - phi_x * phi_x)
    x_coast_ar = np.empty(n_15, dtype=float)
    z_x = rng.normal(0.0, 1.0, n_15)
    v = 0.0
    for i in range(n_15):
        v = phi_x * v + s_x * z_x[i]
        x_coast_ar[i] = v
    tep_seas = 0.28 * np.cos(2.0 * math.pi * (t15_h / 24.0 - 220.0) / 365.0)
    x_coastal = x_coast_ar + tep_seas

    season_b = np.array([-0.012, 0.002, 0.022, -0.008])
    season_y = np.array([-0.14, 0.04, 0.24, -0.08])
    season_tds = np.array([-6.0, 2.0, 12.0, -4.0])

    # Pre-compute composite window layout (Thu-Mon 4h, Tue-Wed 8h; 2026-01-01 is Thu dow=3)
    comp_day_list, comp_m_list, comp_q_list, comp_slot_list, comp_h0_list = [], [], [], [], []
    for d in range(DAYS_2026):
        dow = (3 + d) % 7  # 0=Mon..6=Sun; Tue=1, Wed=2
        m = 8 if dow in (1, 2) else 4
        n_sl = 24 // m
        for sl in range(n_sl):
            h0 = d * 24 + sl * m
            comp_day_list.append(d)
            comp_m_list.append(m)
            comp_q_list.append(int(q_idx_h[h0]))
            comp_slot_list.append(sl)
            comp_h0_list.append(h0)
    comp_day = np.array(comp_day_list, dtype=np.int32)
    comp_m = np.array(comp_m_list, dtype=np.int32)
    comp_q = np.array(comp_q_list, dtype=np.int32)
    comp_slot = np.array(comp_slot_list, dtype=np.int32)
    comp_h0 = np.array(comp_h0_list, dtype=np.int32)
    n_comp = len(comp_day)

    p_cl = _indep_dist_vec(P_CLEAN)
    p_fb = _indep_dist_vec(P_FBIO)
    p_fm = _indep_dist_vec(P_FMIN)
    p_st = _indep_dist_vec(P_STRUCT)

    trains = {}
    for ui, u in enumerate(TRAINS):
        p = WORLD[u]

        # 1. Smooth, non-clamped staggered diurnal + independent load-sharing AR(1) feed flow Q_h (m3/h)
        u_f = np.empty(n_h, dtype=float)
        z_f = rng.normal(0.0, 1.0, n_h)
        s_uf = 46.0 * math.sqrt(1.0 - 0.95 * 0.95)
        v = 0.0
        for h in range(n_h):
            v = 0.95 * v + s_uf * z_f[h]
            u_f[h] = v
        seas_q = 18.0 * np.cos(2.0 * math.pi * (doy - 210.0) / 365.0)
        if p["q_mode"] == "ramp":
            # Smooth linear VFD ramp up & down across 24h (zero flat high/low dwell plateau!)
            dh = np.abs(((hod - p["q_tc"] + 12.0) % 24.0) - 12.0) / 12.0  # 0 at trough -> 1 at peak
            wave = p["q_drop"] * (1.0 - dh)
            q_raw = p["q_hi"] - wave + seas_q + u_f + rng.normal(0.0, 7.0, n_h)
        elif p["q_mode"] == "cosine":
            wave = p["q_drop"] * 0.5 * (1.0 + np.cos(2.0 * math.pi * (hod - p["q_tc"]) / 24.0))
            q_raw = p["q_hi"] - wave + seas_q + u_f + rng.normal(0.0, 7.0, n_h)
        else:
            dh = ((hod - p["q_tc"] + 12.0) % 24.0) - 12.0
            trough = p["q_drop"] * np.exp(-0.5 * (dh / p["q_tw"]) ** 2)
            q_raw = p["q_hi"] - trough + seas_q + u_f + rng.normal(0.0, 7.0, n_h)
        q_flow_h = _soft_clamp(q_raw, lo=230.0, hi=770.0, scale=24.0)

        # 2. S1: Spiegler-Kedem / Fickian mass-flux boron C_t = alpha_{u,q} + (mu_J + eta_t) / Q_t
        phi_b = math.exp(-1.0 / p["b_lam"])
        s_in = p["b_sd_j"] * math.sqrt(max(1e-12, 1.0 - phi_b * phi_b))
        eta_b = np.empty(n_h, dtype=float)
        z_b = rng.normal(0.0, 1.0, n_h)
        v = rng.normal(0.0, p["b_sd_j"])
        for h in range(n_h):
            v = phi_b * v + s_in * z_b[h]
            eta_b[h] = v
        alpha_h = p["b_alpha"] + season_b[q_idx_h]
        j_flux_h = p["b_mu_j"] + eta_b
        b_1h = alpha_h + j_flux_h / q_flow_h
        truth_boron_q = [float(np.sum((b_1h > BORON_LIMIT) & (q_idx_h == q))) for q in range(4)]

        # Flow-proportional composite lab bottles
        comp_val = np.empty(n_comp, dtype=float)
        comp_qbar = np.empty(n_comp, dtype=float)
        lab_eps = rng.normal(0.0, LAB_BORON_SD, n_comp)
        for k in range(n_comp):
            h0 = comp_h0[k]
            m = comp_m[k]
            qs = q_flow_h[h0:h0 + m]
            cs = b_1h[h0:h0 + m]
            qsum = float(np.sum(qs))
            comp_qbar[k] = qsum / m
            comp_val[k] = float(np.sum(qs * cs)) / qsum + lab_eps[k]

        # 3. S2: Variable-flow cumulative-volume two-path DAF/DMF mixing
        # Linearly interpolate hourly Q_h to 15-min grid (midpoint-aligned across each hour)
        idx_15 = np.arange(n_15, dtype=float) / 4.0
        q_15m = np.interp(idx_15, hours, q_flow_h)
        phi_15 = np.cumsum(0.25 * q_15m)

        # Train-local intake probe turbulence (same coastal mean 0.0, SD 1.0 across ALL 8 trains!)
        z_cl = rng.normal(0.0, 1.0, n_15)
        c_loc = np.empty(n_15, dtype=float)
        v = 0.0
        for i in range(n_15):
            v = 0.72 * v + 0.50 * z_cl[i]
            c_loc[i] = v
        c_in = c_coastal + c_loc

        # Shared coastal TEP + independent local intake turbulence (normalized to exact mean=0, SD=1)
        z_xl = rng.normal(0.0, 1.0, n_15)
        x_loc = np.empty(n_15, dtype=float)
        v = 0.0
        for i in range(n_15):
            v = phi_x * v + 0.55 * math.sqrt(1.0 - phi_x * phi_x) * z_xl[i]
            x_loc[i] = v
        x_in_raw = 0.84 * x_coastal + x_loc
        x_in = (x_in_raw - np.mean(x_in_raw)) / np.std(x_in_raw)

        # Two-path advection in cumulative volume Phi(t)
        f_fast = p["f_fast"]
        v_fast = p["v_fast"]
        v_main = p["v_main"]
        c_fast = np.interp(phi_15 - v_fast, phi_15, c_in)
        c_main = np.interp(phi_15 - v_main, phi_15, c_in)
        c_out = f_fast * c_fast + (1.0 - f_fast) * c_main + rng.normal(0.0, COND_PROBE_SD, n_15)

        x_fast = np.interp(phi_15 - v_fast, phi_15, x_in)
        x_main = np.interp(phi_15 - v_main, phi_15, x_in)
        x_arr = f_fast * x_fast + (1.0 - f_fast) * x_main

        # RO-feed supersaturation-oxidant stress index Y_t
        phi_y = math.exp(-0.25 / 1.5)
        s_y = 0.78 * math.sqrt(1.0 - phi_y * phi_y)
        ey = np.empty(n_15, dtype=float)
        z_y = rng.normal(0.0, 1.0, n_15)
        v = 0.0
        for i in range(n_15):
            v = phi_y * v + s_y * z_y[i]
            ey[i] = v
        y_stress = p["y_mu"] + season_y[q_idx_15] + p["y_coup"] * x_arr + ey

        post_burn = np.arange(n_15) >= BURN_IN_15M
        truth_scaling_q = [
            float(0.25 * np.sum(post_burn & (q_idx_15 == q) & (x_arr > SCALING_X_LIM) & (y_stress > SCALING_Y_LIM)))
            for q in range(4)
        ]

        # 4. S3: Continuous post-CIP fouling re-growth kinetics on 1-hour inline diagnostics (8,760 h/train)
        # Routine alternating CIP schedule (~5.5-day cadence: ~32 CIP_ALK_pH11 + ~32 CIP_ACID_pH2 per train)
        # Seed pre-2026 last washes (late Dec 2025 carry-over) so exact dt_alk_h & dt_acid_h are pinned from Jan 1 00:00Z.
        last_alk_h = -int(rng_s3.integers(24, 96))
        last_acid_h = -int(rng_s3.integers(24, 96))
        if abs(last_alk_h - last_acid_h) < 12:
            last_acid_h -= 16
        cip_events = sorted([(last_alk_h, "CIP_ALK_pH11"), (last_acid_h, "CIP_ACID_pH2")], key=lambda x: x[0])
        h_cur = int(rng_s3.integers(20, 60))
        idx_w = ui % 2
        while h_cur < n_h - 12:
            recipe = "CIP_ALK_pH11" if (idx_w % 2 == 0) else "CIP_ACID_pH2"
            cip_events.append((h_cur, recipe))
            idx_w += 1
            h_cur += int(rng_s3.integers(108, 156))  # 4.5 to 6.5 days (~64 alternating washes/train/yr)

        dt_alk_h = np.empty(n_h, dtype=float)
        dt_acid_h = np.empty(n_h, dtype=float)
        ev_map = {h: rec for h, rec in cip_events if h >= 0}
        cur_alk = last_alk_h
        cur_acid = last_acid_h
        for h in range(n_h):
            if h in ev_map:
                if ev_map[h] == "CIP_ALK_pH11":
                    cur_alk = h
                else:
                    cur_acid = h
            dt_alk_h[h] = float(h - cur_alk)
            dt_acid_h[h] = float(h - cur_acid)

        w_bio = p["pi_bio"] * (1.0 - np.exp(-dt_alk_h / p["tau_bio"]))
        w_min = p["pi_min"] * (1.0 - np.exp(-dt_acid_h / p["tau_min"]))
        w_str = np.full(n_h, p["pi_s"], dtype=float)
        w_cln = np.clip(1.0 - w_bio - w_min - w_str, 0.01, 1.0)
        w_tot = w_cln + w_bio + w_min + w_str
        probs_state = np.column_stack([w_cln, w_bio, w_min, w_str]) / w_tot[:, None]
        cdf_state = np.cumsum(probs_state, axis=1)
        u_s = rng_s3.random(n_h)
        states = (u_s[:, None] > cdf_state).sum(axis=1)  # 0=Clean,1=Bio,2=Min,3=Struct
        truth_struct_q = [float(np.sum((states == 3) & (q_idx_h == q))) for q in range(4)]

        # Emit (D1, D2, D3) triple (0..7)
        emit_table = np.vstack([p_cl, p_fb, p_fm, p_st])
        cdf_emit = np.cumsum(emit_table, axis=1)
        u_e = rng_s3.random(n_h)
        triples = (u_e[:, None] > cdf_emit[states]).sum(axis=1).astype(np.int32)
        d1 = ((triples >> 2) & 1).astype(np.int8)
        d2 = ((triples >> 1) & 1).astype(np.int8)
        d3 = (triples & 1).astype(np.int8)

        # 5. S4: Hourly individual train permeate TDS (mg/L) -> observed ONLY at shared bay header!
        rho_t = 0.35
        s_t = p["tds_sd"] * math.sqrt(1.0 - rho_t * rho_t)
        zeta_t = np.empty(n_h, dtype=float)
        z_t = rng.normal(0.0, 1.0, n_h)
        v = rng.normal(0.0, p["tds_sd"])
        for h in range(n_h):
            v = rho_t * v + s_t * z_t[h]
            zeta_t[h] = v
        tds_1h = p["tds_mu"] + season_tds[q_idx_h] + zeta_t
        truth_tds_q = [float(np.sum((tds_1h > TDS_LIMIT) & (q_idx_h == q))) for q in range(4)]

        trains[u] = {
            "q_flow_h": q_flow_h,
            "b_1h": b_1h,
            "truth_boron_q": truth_boron_q,
            "comp_day": comp_day,
            "comp_m": comp_m,
            "comp_q": comp_q,
            "comp_slot": comp_slot,
            "comp_h0": comp_h0,
            "comp_val": comp_val,
            "comp_qbar": comp_qbar,
            "c_in": c_in,
            "x_in": x_in,
            "c_out": c_out,
            "y_stress": y_stress,
            "x_arr_truth": x_arr,
            "phi_truth": phi_15,
            "truth_scaling_q": truth_scaling_q,
            "cip_events": cip_events,
            "dt_alk_h": dt_alk_h,
            "dt_acid_h": dt_acid_h,
            "triples": triples,
            "d1": d1,
            "d2": d2,
            "d3": d3,
            "states_truth": states,
            "truth_struct_q": truth_struct_q,
            "tds_1h_truth": tds_1h,
            "truth_tds_q": truth_tds_q,
        }

    # Build shared North Bay and South Bay permeate collector TDS series (8,760 hours each)
    bays = {}
    for bay_name, members in BAYS.items():
        q_mat = np.column_stack([trains[u]["q_flow_h"] for u in members])
        t_mat = np.column_stack([trains[u]["tds_1h_truth"] for u in members])
        q_tot = np.sum(q_mat, axis=1)
        w_mat = q_mat / q_tot[:, None]
        collector_tds = np.sum(w_mat * t_mat, axis=1) + rng.normal(0.0, TDS_METER_SD, n_h)
        bays[bay_name] = {
            "members": members,
            "q_tot_h": q_tot,
            "w_mat": w_mat,
            "collector_tds_h": collector_tds,
        }

    return {"seed": seed, "trains": trains, "bays": bays}


# ==============================================================================
# S1 ESTIMATORS: Spiegler-Kedem / Fickian Mass-Flux Conservation + AR(1) Support
# ==============================================================================

def _comp_moments(res, comp_m, comp_day, noise_var_vec, trim_frac=0.0):
    res = np.asarray(res, dtype=float)
    comp_m = np.asarray(comp_m, dtype=np.int32)
    comp_day = np.asarray(comp_day, dtype=np.int32)
    nv = np.asarray(noise_var_vec, dtype=float)

    def _var(arr, nv_arr):
        if trim_frac > 0.0 and len(arr) > 40:
            order = np.argsort(arr)
            k = max(1, int(len(arr) * trim_frac))
            keep = order[k:-k]
            arr = arr[keep]
            nv_arr = nv_arr[keep]
        return max(1e-10, float(np.var(arr, ddof=1)) - float(np.mean(nv_arr)))

    m4 = comp_m == 4
    m8 = comp_m == 8
    v4 = _var(res[m4], nv[m4])
    v8 = _var(res[m8], nv[m8])

    # Adjacent within-day lag-1 autocovariance
    same4 = (comp_m[:-1] == 4) & (comp_m[1:] == 4) & (comp_day[:-1] == comp_day[1:])
    same8 = (comp_m[:-1] == 8) & (comp_m[1:] == 8) & (comp_day[:-1] == comp_day[1:])
    p4 = res[:-1][same4] * res[1:][same4]
    p8 = res[:-1][same8] * res[1:][same8]
    if trim_frac > 0.0:
        for arr_name in ("p4", "p8"):
            arr = p4 if arr_name == "p4" else p8
            if len(arr) > 40:
                s = np.sort(arr)
                k = max(1, int(len(s) * trim_frac))
                if arr_name == "p4":
                    p4 = s[k:-k]
                else:
                    p8 = s[k:-k]
    c4 = float(np.mean(p4))
    c8 = float(np.mean(p8))
    return v4, c4, v8, c8


def _fit_ar1_moments(v4, c4, v8, c8, kernel="ar1", obj="wls", use_8h=True):
    best_loss = 1e30
    best_sd, best_lam = math.sqrt(max(v4, 1e-10)), 2.0
    lams = np.exp(np.linspace(math.log(0.25), math.log(30.0), 220))
    for lam in lams:
        if kernel == "ar1":
            phi = math.exp(-1.0 / lam)
            f4, g4 = _ar1_fg(phi, 4)
            f8, g8 = _ar1_fg(phi, 8)
        else:
            f4, g4 = _ou_fg(lam, 4)
            f8, g8 = _ou_fg(lam, 8)
        if obj == "wls":
            obs = [v4, c4, v8, c8] if use_8h else [v4, c4]
            mod = [f4, g4, f8, g8] if use_8h else [f4, g4]
            wts = [3.0 / max(v4 * v4, 1e-12), 3.0 / max(v4 * v4, 1e-12),
                   1.0 / max(v8 * v8, 1e-12), 0.7 / max(v8 * v8, 1e-12)] if use_8h else [1.0, 1.0]
        elif obj == "wls_var":
            obs = [v4, c4, v8, c8] if use_8h else [v4, c4]
            mod = [f4, g4, f8, g8] if use_8h else [f4, g4]
            wts = [1.0 / max(v4 * v4, 1e-12), 1.0 / max(v4 * v4, 1e-12),
                   1.0 / max(v8 * v8, 1e-12), 1.0 / max(v8 * v8, 1e-12)] if use_8h else [1.0, 1.0]
        elif obj == "ols":
            obs = [v4, c4, v8, c8] if use_8h else [v4, c4]
            mod = [f4, g4, f8, g8] if use_8h else [f4, g4]
            wts = [1.0] * len(obs)
        else:  # lag1
            obs = [v4, c4]
            mod = [f4, g4]
            wts = [1.0, 2.0]
        num = sum(w * o * m for w, o, m in zip(wts, obs, mod))
        den = sum(w * m * m for w, m in zip(wts, mod))
        s2 = max(1e-10, num / max(den, 1e-12))
        loss = sum(w * (o - s2 * m) ** 2 for w, o, m in zip(wts, obs, mod))
        if loss < best_loss:
            best_loss = loss
            best_sd = math.sqrt(s2)
            best_lam = float(lam)
    return best_sd, best_lam


def _fit_mass_flux_reg(comp_val, comp_q, comp_qbar, mode="ols", q_mu_j=False):
    """Fit M_k = Q_bar_k * C_comp_k = alpha_{u,q} * Q_bar_k + mu_{J} (+ optional quarterly mu_{J,q})."""
    y = comp_qbar * comp_val
    n = len(y)
    if q_mu_j:
        X = np.zeros((n, 8), dtype=float)
        for q in range(4):
            mask = comp_q == q
            X[mask, q] = comp_qbar[mask]
            X[mask, 4 + q] = 1.0
    else:
        X = np.zeros((n, 5), dtype=float)
        for q in range(4):
            mask = comp_q == q
            X[mask, q] = comp_qbar[mask]
        X[:, 4] = 1.0

    w = np.ones(n, dtype=float)
    if mode == "wls_span":
        # down-weight noisy 4h relative to 8h or inverse variance proxy
        pass
    for it in range(12 if mode == "huber" else 1):
        sw = np.sqrt(w)[:, None]
        coef, *_ = np.linalg.lstsq(X * sw, y * sw[:, 0], rcond=None)
        if mode == "huber":
            r = y - X @ coef
            mad = float(np.median(np.abs(r - np.median(r)))) * 1.4826 + 1e-6
            delta = 1.345 * mad
            w = np.where(np.abs(r) <= delta, 1.0, delta / np.maximum(np.abs(r), 1e-9))
    alphas = coef[:4]
    mu_j = coef[4:8] if q_mu_j else np.full(4, float(coef[4]))
    pred_m = X @ coef
    res_j = y - pred_m
    res_c = comp_val - pred_m / comp_qbar
    return alphas, mu_j, res_j, res_c


def _fit_flux_exact_mle(res_j, comp_m, comp_day, comp_qbar, lab_noise=True, kernel="ar1"):
    """Exact Gaussian composite AR(1) or continuous-time 1h-block OU MLE in conserved mass-flux space."""
    lv = (LAB_BORON_SD ** 2) if lab_noise else 0.0
    days_4, days_8 = [], []
    q4, q8 = [], []
    for d in range(DAYS_2026):
        idx = np.where(comp_day == d)[0]
        if comp_m[idx[0]] == 4:
            days_4.append(res_j[idx])
            q4.append(comp_qbar[idx])
        else:
            days_8.append(res_j[idx])
            q8.append(comp_qbar[idx])
    Y4 = np.asarray(days_4, dtype=float)
    Q4 = np.asarray(q4, dtype=float)
    Y8 = np.asarray(days_8, dtype=float)
    Q8 = np.asarray(q8, dtype=float)

    def _block_corr_ar1(phi, m, n_sl):
        C = np.empty((n_sl, n_sl), dtype=float)
        for a in range(n_sl):
            for b in range(n_sl):
                s = 0.0
                for i in range(m):
                    for j in range(m):
                        s += phi ** abs((a * m + i) - (b * m + j))
                C[a, b] = s / (m * m)
        return C

    def _block_corr_ou(lam, m, n_sl):
        def _f_raw(h):
            x = h / lam
            if x < 1e-6:
                return 1.0 - x / 3.0
            return 2.0 * (x - 1.0 + math.exp(-x)) / (x * x)
        f1 = _f_raw(1.0)
        fm_ratio = _f_raw(float(m)) / f1
        x = float(m) / lam
        g1 = (1.0 - x) if x < 1e-6 else (((1.0 - math.exp(-x)) ** 2) / (x * x))
        g1_ratio = g1 / f1
        C = np.empty((n_sl, n_sl), dtype=float)
        for a in range(n_sl):
            C[a, a] = fm_ratio
            for b in range(a + 1, n_sl):
                val = g1_ratio * math.exp(-((b - a - 1) * float(m)) / lam)
                C[a, b] = val
                C[b, a] = val
        return C

    def _nll(params):
        log_sd, log_lam = params
        sd2 = math.exp(2.0 * log_sd)
        lam = math.exp(log_lam)
        phi = math.exp(-1.0 / lam)
        nll = 0.0
        for Y, Q, m, n_sl in ((Y4, Q4, 4, 6), (Y8, Q8, 8, 3)):
            C0 = sd2 * (_block_corr_ou(lam, m, n_sl) if kernel == "ou" else _block_corr_ar1(phi, m, n_sl))
            lab_diag = lv * np.mean(Q * Q, axis=0)
            Sig = C0 + np.diag(lab_diag) + 1e-8 * np.eye(n_sl)
            sign, logdet = np.linalg.slogdet(Sig)
            if sign <= 0:
                return 1e12
            invS = np.linalg.inv(Sig)
            quad = np.einsum("ij,jk,ik->i", Y, invS, Y)
            nll += 0.5 * (len(Y) * logdet + float(np.sum(quad)))
        return nll

    res = minimize(_nll, [math.log(20.0), math.log(2.0)],
                   bounds=[(math.log(2.0), math.log(120.0)), (math.log(0.20), math.log(30.0))],
                   method="L-BFGS-B")
    return math.exp(res.x[0]), math.exp(res.x[1])


def _fit_homosced_c_flux_r2(comp_val, comp_q, comp_qbar, comp_m, comp_day, q_flow_h, q_idx_h):
    """Exact Response 2 Round-2 solver: a_q + c / Q_bar mean + HOMOSCEDASTIC concentration AR(1)."""
    n = len(comp_val)
    X = np.zeros((n, 5), dtype=float)
    for q in range(4):
        X[comp_q == q, q] = 1.0
    X[:, 4] = 1.0 / comp_qbar
    coef, *_ = np.linalg.lstsq(X, comp_val, rcond=None)
    alphas, c_slope = coef[:4], float(coef[4])
    res_c = comp_val - X @ coef
    v4, c4, v8, c8 = _comp_moments(res_c, comp_m, comp_day, np.full(n, LAB_BORON_SD ** 2))
    sd_c, lam_c = _fit_ar1_moments(v4, c4, v8, c8, kernel="ar1", obj="wls")
    # Constant homoscedastic concentration SD across all 8,760 hours!
    mu_h = alphas[q_idx_h] + c_slope / q_flow_h
    p_h = _norm_sf((BORON_LIMIT - mu_h) / max(sd_c, 1e-6))
    hq = [float(np.sum(p_h[q_idx_h == q])) for q in range(4)]
    # Heteroscedasticity correlation check F1_het
    r2_c = res_c ** 2
    invq2 = 1.0 / (comp_qbar ** 2)
    het_corr = abs(float(np.corrcoef(r2_c, invq2)[0, 1]))
    phi = math.exp(-1.0 / lam_c)
    f4, g4 = _ar1_fg(phi, 4)
    f8, _ = _ar1_fg(phi, 8)
    f1_err = het_corr + abs(f8 / max(f4, 1e-9) - v8 / max(v4, 1e-9)) + abs(g4 / max(f4, 1e-9) - c4 / max(v4, 1e-9))
    return hq, f1_err, sd_c, lam_c, het_corr


def _fit_block_ar1_r1(comp_val, comp_q, comp_m, comp_day, comp_slot, comp_h0, q_idx_h):
    """Exact Response 1 Round-2 solver: 6 four-hour block means per quarter + homoscedastic AR(1)."""
    # Estimate 6 four-hour block means per quarter using 4h bottles (identical to Response 1)
    mu_blk = np.zeros((4, 6), dtype=float)
    for q in range(4):
        for sl in range(6):
            mask = (comp_q == q) & (comp_m == 4) & (comp_slot == sl)
            mu_blk[q, sl] = float(np.mean(comp_val[mask]))
    pred = np.empty_like(comp_val)
    for k in range(len(comp_val)):
        q = comp_q[k]
        if comp_m[k] == 4:
            pred[k] = mu_blk[q, comp_slot[k]]
        else:
            sl0 = comp_slot[k] * 2
            pred[k] = 0.5 * (mu_blk[q, sl0] + mu_blk[q, sl0 + 1])
    res_c = comp_val - pred
    v4, c4, v8, c8 = _comp_moments(res_c, comp_m, comp_day, np.full(len(comp_val), LAB_BORON_SD ** 2))
    sd_c, lam_c = _fit_ar1_moments(v4, c4, v8, c8, kernel="ar1", obj="wls")
    hq = [0.0] * 4
    for q in range(4):
        n_days_q = Q_DAYS[q]
        for sl in range(6):
            hq[q] += n_days_q * 4.0 * float(_norm_sf((BORON_LIMIT - mu_blk[q, sl]) / max(sd_c, 1e-6)))
    return hq, res_c, sd_c, lam_c


def estimate_s1(data, mode="golden", kernel="ar1", obj="wls", lab_noise=True,
                trim_frac=0.0, use_8h=True, reg_mode="ols", q_mu_j=False):
    q_idx_h = _q_index_hour()
    out = {}
    for u in TRAINS:
        tr = data["trains"][u]
        cv = tr["comp_val"]
        cm = tr["comp_m"]
        cq = tr["comp_q"]
        cd = tr["comp_day"]
        cs = tr["comp_slot"]
        ch0 = tr["comp_h0"]
        qb = tr["comp_qbar"]
        qh = tr["q_flow_h"]

        if mode == "hurried":
            hq = [float(np.sum(cm[(cq == q) & (cv > BORON_LIMIT)])) for q in range(4)]
            out[u] = {"q": hq, "f1_err": 1.65, "sd_j": 0.0, "lam": 0.0, "het_corr": 0.55}
            continue

        if mode == "cutoff_4h":
            hq = [0.0] * 4
            for q in range(4):
                m4 = (cq == q) & (cm == 4)
                hq[q] = Q_HOURS[q] * float(np.mean(cv[m4] > BORON_LIMIT))
            out[u] = {"q": hq, "f1_err": 1.50, "sd_j": 0.0, "lam": 0.0, "het_corr": 0.55}
            continue

        if mode == "r1_block_ar1":
            hq, res_c, sd_c, lam_c = _fit_block_ar1_r1(cv, cq, cm, cd, cs, ch0, q_idx_h)
            het_c = abs(float(np.corrcoef(res_c ** 2, 1.0 / (qb ** 2))[0, 1]))
            flux_r = abs(float(np.corrcoef(res_c, 1.0 / qb)[0, 1]))
            out[u] = {"q": hq, "f1_err": het_c + flux_r + 0.25, "sd_j": sd_c, "lam": lam_c, "het_corr": het_c}
            continue

        if mode == "r2_flux_homosced":
            hq, f1_err, sd_c, lam_c, het_c = _fit_homosced_c_flux_r2(cv, cq, qb, cm, cd, qh, q_idx_h)
            out[u] = {"q": hq, "f1_err": f1_err, "sd_j": sd_c, "lam": lam_c, "het_corr": het_c}
            continue

        if mode == "stat_ar1_no_flux":
            # Stationary quarterly mean + homoscedastic AR(1) (no flow coupling)
            q_means = np.array([float(np.mean(cv[cq == q])) for q in range(4)])
            res_c = cv - q_means[cq]
            v4, c4, v8, c8 = _comp_moments(res_c, cm, cd, np.full(len(cv), LAB_BORON_SD ** 2))
            sd_c, lam_c = _fit_ar1_moments(v4, c4, v8, c8)
            hq = [Q_HOURS[q] * float(_norm_sf((BORON_LIMIT - q_means[q]) / max(sd_c, 1e-6))) for q in range(4)]
            het_c = abs(float(np.corrcoef(res_c ** 2, 1.0 / (qb ** 2))[0, 1]))
            flux_r = abs(float(np.corrcoef(res_c, 1.0 / qb)[0, 1]))
            out[u] = {"q": hq, "f1_err": het_c + flux_r + 0.30, "sd_j": sd_c, "lam": lam_c, "het_corr": het_c}
            continue

        # Mass-flux regression M_k = Q_bar_k * C_comp_k = alpha_q * Q_bar_k + mu_J + eta_bar_k
        alphas, mu_j, res_j, res_c = _fit_mass_flux_reg(cv, cq, qb, mode=reg_mode, q_mu_j=q_mu_j)
        nv_j = (qb ** 2) * (LAB_BORON_SD ** 2) if lab_noise else np.zeros_like(qb)
        v4, c4, v8, c8 = _comp_moments(res_j, cm, cd, nv_j, trim_frac=trim_frac)

        if mode == "flux_no_deconv":
            sd_j = math.sqrt(v4)
            lam = 1e6
        elif mode == "over_flux_iid":
            sd_j = math.sqrt(4.0 * v4)
            lam = 0.01
        elif mode == "over_c_iid":
            # i.i.d. sqrt(m) in concentration space
            v4c, _, _, _ = _comp_moments(res_c, cm, cd, np.full(len(cv), LAB_BORON_SD ** 2))
            sd_c = math.sqrt(4.0 * v4c)
            mu_h = alphas[q_idx_h] + mu_j[q_idx_h] / qh
            p_h = _norm_sf((BORON_LIMIT - mu_h) / max(sd_c, 1e-6))
            hq = [float(np.sum(p_h[q_idx_h == q])) for q in range(4)]
            out[u] = {"q": hq, "f1_err": 1.15, "sd_j": sd_c, "lam": 0.01, "het_corr": 0.45}
            continue
        elif mode == "golden_mle":
            sd_j, lam = _fit_flux_exact_mle(res_j, cm, cd, qb, lab_noise=lab_noise, kernel="ar1")
        elif mode == "golden_ou_mle":
            sd_j, lam = _fit_flux_exact_mle(res_j, cm, cd, qb, lab_noise=lab_noise, kernel="ou")
            kernel = "ou"
        else:
            sd_j, lam = _fit_ar1_moments(v4, c4, v8, c8, kernel=kernel, obj=obj, use_8h=use_8h)

        # Hourly survival in conserved mass-flux space: SD(C_t | Q_t) = sd_j / Q_t
        mu_h = alphas[q_idx_h] + mu_j[q_idx_h] / qh
        sd_h = sd_j / qh
        p_h = _norm_sf((BORON_LIMIT - mu_h) / np.maximum(sd_h, 1e-6))
        hq = [float(np.sum(p_h[q_idx_h == q])) for q in range(4)]

        # Native-unit F1 check in mass-flux space (heteroscedasticity residual + moment fit)
        het_j = abs(float(np.corrcoef(res_j ** 2, 1.0 / (qb ** 2))[0, 1]))
        if lam > 1e4:
            f4_m, g4_m, f8_m = 1.0, 1.0, 1.0
        elif lam < 0.05:
            f4_m, g4_m, f8_m = 0.25, 0.0, 0.125
        elif kernel == "ou":
            f4_m, g4_m = _ou_fg(lam, 4)
            f8_m, _ = _ou_fg(lam, 8)
        else:
            phi = math.exp(-1.0 / lam)
            f4_m, g4_m = _ar1_fg(phi, 4)
            f8_m, _ = _ar1_fg(phi, 8)
        f1_err = het_j + abs(f8_m / max(f4_m, 1e-9) - v8 / max(v4, 1e-9)) + abs(g4_m / max(f4_m, 1e-9) - c4 / max(v4, 1e-9))
        out[u] = {
            "q": hq,
            "f1_err": f1_err,
            "sd_j": sd_j,
            "lam": lam,
            "alphas": alphas.tolist(),
            "mu_j": mu_j.tolist(),
            "het_corr": het_j,
        }
    return out


# ==============================================================================
# S2 ESTIMATORS: Variable-Flow Cumulative-Volume Two-Path DAF/DMF Mixing
# ==============================================================================

def _build_phi_hat(q_flow_h, flow_interp="linear"):
    n_15 = STEPS_15M
    hours = np.arange(HOURS_2026, dtype=float)
    if flow_interp == "linear":
        q15 = np.interp(np.arange(n_15, dtype=float) / 4.0, hours, q_flow_h)
    elif flow_interp == "step_left":
        q15 = np.repeat(q_flow_h, 4)
    elif flow_interp == "step_right":
        idx = np.minimum(HOURS_2026 - 1, (np.arange(n_15) + 3) // 4)
        q15 = q_flow_h[idx]
    elif flow_interp == "midpoint":
        q15 = np.interp((np.arange(n_15, dtype=float) + 0.5) / 4.0, hours, q_flow_h)
    else:  # trapz
        q15 = np.interp(np.arange(n_15, dtype=float) / 4.0, hours, q_flow_h)
        phi = np.zeros(n_15, dtype=float)
        phi[0] = 0.25 * q15[0]
        phi[1:] = phi[0] + np.cumsum(0.125 * (q15[:-1] + q15[1:]))
        return phi
    return np.cumsum(0.25 * q15)


def _eval_loss_vec(diff, loss_fn="l2"):
    if loss_fn == "l2":
        return float(np.mean(diff * diff))
    if loss_fn == "l1":
        return float(np.mean(np.abs(diff)))
    if loss_fn == "huber":
        a = np.abs(diff)
        d = 0.85
        return float(np.mean(np.where(a <= d, 0.5 * a * a, d * (a - 0.5 * d))))
    # trimmed_l2 (2%)
    sq = np.sort(diff * diff)
    k = max(1, int(0.02 * len(sq)))
    return float(np.mean(sq[:-k]))


def _profile_two_path(phi, c_in, c_out, loss_fn="l2"):
    sl = slice(BURN_IN_15M, None)
    y = c_out[sl]
    phi_sl = phi[sl]
    # Coarse grid search over (V_fast, V_main), analytic closed-form optimal f_fast for L2!
    vf_grid = np.arange(200.0, 521.0, 40.0)
    vm_grid = np.arange(960.0, 1601.0, 40.0)
    cf_cache = {vf: np.interp(phi_sl - vf, phi, c_in) for vf in vf_grid}
    cm_cache = {vm: np.interp(phi_sl - vm, phi, c_in) for vm in vm_grid}

    best = (1e30, 0.0, 360.0, 1280.0)
    for vf in vf_grid:
        cf = cf_cache[vf]
        for vm in vm_grid:
            if vm - vf < 350.0:
                continue
            cm = cm_cache[vm]
            d = cf - cm
            den = float(np.dot(d, d))
            f = float(np.dot(y - cm, d)) / max(den, 1e-9)
            f = max(0.0, min(0.50, f))
            pred = cm + f * d
            loss = _eval_loss_vec(y - pred, loss_fn)
            if loss < best[0]:
                best = (loss, f, float(vf), float(vm))

    # Fine refinement around best (+/- 40 m3, step 8 m3)
    _, _, vf0, vm0 = best
    vf_fine = np.arange(max(160.0, vf0 - 40.0), min(560.0, vf0 + 41.0), 8.0)
    vm_fine = np.arange(max(860.0, vm0 - 40.0), min(1640.0, vm0 + 41.0), 8.0)
    cf_f = {vf: np.interp(phi_sl - vf, phi, c_in) for vf in vf_fine}
    cm_f = {vm: np.interp(phi_sl - vm, phi, c_in) for vm in vm_fine}
    for vf in vf_fine:
        cf = cf_f[vf]
        for vm in vm_fine:
            if vm - vf < 300.0:
                continue
            cm = cm_f[vm]
            d = cf - cm
            den = float(np.dot(d, d))
            f = max(0.0, min(0.50, float(np.dot(y - cm, d)) / max(den, 1e-9)))
            if loss_fn != "l2":
                # refine f on 9-point local grid for non-L2 loss
                for df in (-0.03, -0.015, 0.0, 0.015, 0.03):
                    ff = max(0.0, min(0.50, f + df))
                    loss = _eval_loss_vec(y - (cm + ff * d), loss_fn)
                    if loss < best[0]:
                        best = (loss, ff, float(vf), float(vm))
            else:
                loss = _eval_loss_vec(y - (cm + f * d), loss_fn)
                if loss < best[0]:
                    best = (loss, f, float(vf), float(vm))
    _, f_hat, vf_hat, vm_hat = best
    if f_hat < 0.04:
        f_hat = 0.0
    pred = f_hat * np.interp(phi_sl - vf_hat, phi, c_in) + (1.0 - f_hat) * np.interp(phi_sl - vm_hat, phi, c_in)
    rms = float(np.sqrt(np.mean((y - pred) ** 2)))
    return f_hat, vf_hat, vm_hat, rms


def _profile_single_plug(phi, c_in, c_out):
    sl = slice(BURN_IN_15M, None)
    y = c_out[sl]
    phi_sl = phi[sl]
    best = (1e30, 1200.0)
    for v in np.arange(160.0, 1641.0, 20.0):
        pred = np.interp(phi_sl - v, phi, c_in)
        mse = float(np.mean((y - pred) ** 2))
        if mse < best[0]:
            best = (mse, float(v))
    return best[1], math.sqrt(best[0])


def estimate_s2(data, mode="golden", flow_interp="linear", loss_fn="l2", tep_interp="linear"):
    q_idx_15 = _q_index_15m()
    sl = slice(BURN_IN_15M, None)
    q_sl = q_idx_15[sl]
    out = {}
    for u in TRAINS:
        tr = data["trains"][u]
        c_in, c_out = tr["c_in"], tr["c_out"]
        x_in, y = tr["x_in"], tr["y_stress"]
        qh = tr["q_flow_h"]

        if mode == "hurried":
            x_arr = x_in[sl]
            c_rms = float(np.sqrt(np.mean((c_out[sl] - c_in[sl]) ** 2)))
            params = (0.0, 0.0, 0.0)
        elif mode == "r1_r2_fixed_lag_tep":
            # EXACT Response 1 & Response 2 Round-2 method: direct fixed wall-clock lag CCF(X_in -> Y)
            best_r, best_lag = -1e9, 0
            y_sl = y[sl]
            for lag in range(0, 25):
                x_sh = x_in[BURN_IN_15M - lag:STEPS_15M - lag]
                r = float(np.corrcoef(x_sh, y_sl)[0, 1])
                if r > best_r:
                    best_r, best_lag = r, lag
            x_arr = x_in[BURN_IN_15M - best_lag:STEPS_15M - best_lag]
            c_sh = c_in[BURN_IN_15M - best_lag:STEPS_15M - best_lag]
            c_rms = float(np.sqrt(np.mean((c_out[sl] - c_sh) ** 2)))
            params = (0.0, 0.0, float(best_lag))
        elif mode == "fixed_lag_cond":
            best_mse, best_lag = 1e30, 0
            co_sl = c_out[sl]
            for lag in range(0, 25):
                c_sh = c_in[BURN_IN_15M - lag:STEPS_15M - lag]
                mse = float(np.mean((co_sl - c_sh) ** 2))
                if mse < best_mse:
                    best_mse, best_lag = mse, lag
            x_arr = x_in[BURN_IN_15M - best_lag:STEPS_15M - best_lag]
            c_rms = math.sqrt(best_mse)
            params = (0.0, 0.0, float(best_lag))
        elif mode == "nom_vol":
            phi = _build_phi_hat(qh, "linear")
            v_nom = WORLD[u]["v_nom"]
            x_arr = np.interp(phi[sl] - v_nom, phi, x_in)
            c_pred = np.interp(phi[sl] - v_nom, phi, c_in)
            c_rms = float(np.sqrt(np.mean((c_out[sl] - c_pred) ** 2)))
            params = (0.0, 0.0, v_nom)
        elif mode == "single_plug":
            phi = _build_phi_hat(qh, "linear")
            v_eff, c_rms = _profile_single_plug(phi, c_in, c_out)
            x_arr = np.interp(phi[sl] - v_eff, phi, x_in)
            params = (0.0, 0.0, v_eff)
        elif mode == "over_comonotonic":
            hq = []
            for q in range(4):
                m = q_sl == q
                cnt_x = int(np.sum(x_in[sl][m] > SCALING_X_LIM))
                cnt_y = int(np.sum(y[sl][m] > SCALING_Y_LIM))
                hq.append(0.25 * min(cnt_x, cnt_y))
            out[u] = {"q": hq, "c_rms": 1.85, "params": (0.0, 0.0, 0.0)}
            continue
        else:
            phi = _build_phi_hat(qh, flow_interp)
            f_hat, vf_hat, vm_hat, c_rms = _profile_two_path(phi, c_in, c_out, loss_fn=loss_fn)
            if tep_interp == "nearest":
                idx_f = np.clip(np.searchsorted(phi, phi[sl] - vf_hat), 0, STEPS_15M - 1)
                idx_m = np.clip(np.searchsorted(phi, phi[sl] - vm_hat), 0, STEPS_15M - 1)
                xf, xm = x_in[idx_f], x_in[idx_m]
            else:
                xf = np.interp(phi[sl] - vf_hat, phi, x_in)
                xm = np.interp(phi[sl] - vm_hat, phi, x_in)
            x_arr = f_hat * xf + (1.0 - f_hat) * xm
            params = (f_hat, vf_hat, vm_hat)

        y_sl = y[sl]
        hq = [
            float(0.25 * np.sum((q_sl == q) & (x_arr > SCALING_X_LIM) & (y_sl > SCALING_Y_LIM)))
            for q in range(4)
        ]
        out[u] = {"q": hq, "c_rms": c_rms, "params": params}
    return out


# ==============================================================================
# S3 ESTIMATORS: Continuous Post-CIP Fouling Kinetics + Identical F_min/S Emissions
# ==============================================================================

def _static_3class_em(triples_all, n_iter=60):
    """Fast 3-class unconditioned EM returning (p_cl, p_fb, p_ms, pi3)."""
    n_u = triples_all.shape[0]
    p_cl = np.array([0.02, 0.01, 0.01])
    p_fb = np.array([0.65, 0.85, 0.02])
    p_ms = np.array([0.80, 0.20, 0.65])
    pi3 = np.full((n_u, 3), [0.75, 0.12, 0.13])
    d1_all = ((triples_all >> 2) & 1).astype(float)
    d2_all = ((triples_all >> 1) & 1).astype(float)
    d3_all = (triples_all & 1).astype(float)
    for _ in range(n_iter):
        E = np.vstack([_indep_dist_vec(p_cl), _indep_dist_vec(p_fb), _indep_dist_vec(p_ms)])
        num_c = np.zeros((3, 3))
        den_c = np.zeros(3)
        for ui in range(n_u):
            tr_idx = triples_all[ui]
            lik = pi3[ui][:, None] * E[:, tr_idx]
            post = lik / np.maximum(np.sum(lik, axis=0, keepdims=True), 1e-15)
            pi3[ui] = np.mean(post, axis=1)
            for c in range(3):
                den_c[c] += float(np.sum(post[c]))
                num_c[c, 0] += float(np.sum(post[c] * d1_all[ui]))
                num_c[c, 1] += float(np.sum(post[c] * d2_all[ui]))
                num_c[c, 2] += float(np.sum(post[c] * d3_all[ui]))
        p_cl = np.clip(num_c[0] / max(den_c[0], 1.0), 0.001, 0.20)
        p_fb = np.clip(num_c[1] / max(den_c[1], 1.0), 0.001, 0.999)
        p_ms = np.clip(num_c[2] / max(den_c[2], 1.0), 0.001, 0.999)
    return p_cl, p_fb, p_ms, pi3


def _fit_kinetic_dual_cip(
    data,
    kinetics="exp_time",
    dt_shift=0.0,
    map_alpha=0.0,
    two_step_static=False,
    fix_ps_zero=None,
    fix_tr06_ps=None,
):
    """Exact converged 70,080-hour joint analytic-gradient L-BFGS-B MLE for 3-emission / 4-state
    continuous post-CIP fouling re-growth kinetics:
      w_bio(u, t) = pi_bio_u * g(dt_alk, tau_bio_u)
      w_MS(u, t)  = pi_S_u + pi_min_u * g(dt_acid, tau_min_u)
      w_clean     = 1 - w_bio - w_MS
    Unconstrained tau in [0.1, 5000.0] h (never active/binding); converged to ftol=1e-13, gtol=1e-8.
    """
    n_u = len(TRAINS)
    triples_all = np.vstack([data["trains"][u]["triples"] for u in TRAINS])  # (8, 8760)
    T = triples_all.shape[1]

    if kinetics == "exp_vol":
        dt_alk_all = np.empty((n_u, T), dtype=float)
        dt_acid_all = np.empty((n_u, T), dtype=float)
        for ui, u in enumerate(TRAINS):
            tr = data["trains"][u]
            q1 = tr["q_flow_h"] / 1000.0  # 10^3 m3 per hour
            evs = tr["cip_events"]
            pre_alk = max(h for h, rec in evs if h < 0 and rec == "CIP_ALK_pH11")
            pre_acid = max(h for h, rec in evs if h < 0 and rec == "CIP_ACID_pH2")
            q_mean = float(np.mean(q1))
            va = float(-pre_alk) * q_mean
            vc = float(-pre_acid) * q_mean
            ev_map = {h: rec for h, rec in evs if h >= 0}
            for h in range(T):
                if h in ev_map:
                    if ev_map[h] == "CIP_ALK_pH11":
                        va = 0.0
                    else:
                        vc = 0.0
                dt_alk_all[ui, h] = va + dt_shift * q1[h]
                dt_acid_all[ui, h] = vc + dt_shift * q1[h]
                va += q1[h]
                vc += q1[h]
    else:
        dt_alk_all = np.vstack([data["trains"][u]["dt_alk_h"] for u in TRAINS]) + dt_shift
        dt_acid_all = np.vstack([data["trains"][u]["dt_acid_h"] for u in TRAINS]) + dt_shift

    bits = np.array([[(k >> 2) & 1, (k >> 1) & 1, k & 1] for k in range(8)], dtype=float)
    tr_flat = triples_all.ravel()
    oh = np.zeros((n_u * T, 8), dtype=float)
    oh[np.arange(n_u * T), tr_flat] = 1.0

    def _gd_1d(dt, ltau):
        tau = math.exp(ltau)
        u = dt / tau
        if kinetics == "michaelis":
            den = dt + tau
            return dt / den, -(dt * tau) / (den * den)
        if kinetics == "weibull_12":
            k = 1.15
            uk = np.power(np.maximum(u, 0.0), k)
            e = np.exp(-uk)
            return 1.0 - e, -k * uk * e
        if kinetics == "weibull_09":
            k = 0.90
            uk = np.power(np.maximum(u, 0.0), k)
            e = np.exp(-uk)
            return 1.0 - e, -k * uk * e
        e = np.exp(-u)
        return 1.0 - e, -u * e

    def _gd_mat(dt_mat, ltau_vec):
        tau = np.exp(ltau_vec)[:, None]
        u = dt_mat / tau
        if kinetics == "michaelis":
            den = dt_mat + tau
            return dt_mat / den, -(dt_mat * tau) / (den * den)
        if kinetics == "weibull_12":
            k = 1.15
            uk = np.power(np.maximum(u, 0.0), k)
            e = np.exp(-uk)
            return 1.0 - e, -k * uk * e
        if kinetics == "weibull_09":
            k = 0.90
            uk = np.power(np.maximum(u, 0.0), k)
            e = np.exp(-uk)
            return 1.0 - e, -k * uk * e
        e = np.exp(-u)
        return 1.0 - e, -u * e

    # Step 1: Static 3-class EM for clean emission warm start
    p_cl0, p_fb0, p_ms0, pi3 = _static_3class_em(triples_all, n_iter=60)
    em_init = np.vstack([p_cl0, p_fb0, p_ms0])
    E_init = np.vstack([_indep_dist_vec(p_cl0), _indep_dist_vec(p_fb0), _indep_dist_vec(p_ms0)])

    t_lo, t_hi = math.log(0.1), math.log(5000.0)
    t0_scale = 22.0 if kinetics == "exp_vol" else 45.0

    # Step 2: Fast per-train 5-D analytic-gradient warm start with fixed em_init (multi-start)
    init_pars = np.zeros((n_u, 5), dtype=float)
    for ui in range(n_u):
        tr_i = triples_all[ui]
        e0, e1, e2 = E_init[0, tr_i], E_init[1, tr_i], E_init[2, tr_i]
        da, dc = dt_alk_all[ui], dt_acid_all[ui]
        ps_b = (0.0, 0.0) if (fix_ps_zero and ui in fix_ps_zero) else (
            (fix_tr06_ps, fix_tr06_ps) if (fix_tr06_ps is not None and ui == 5) else (0.0, 0.35)
        )
        bnds_u = [(0.0, 0.48), (0.0, 0.48), ps_b, (t_lo, t_hi), (t_lo, t_hi)]

        def _nll_u(x):
            pb, pm, ps, ltb, ltm = x
            gb, dgb = _gd_1d(da, ltb)
            gm, dgm = _gd_1d(dc, ltm)
            wb = pb * gb
            wms = ps + pm * gm
            wc = 1.0 - wb - wms
            if np.any(wc <= 1e-6):
                return 1e12, np.zeros(5)
            lik = wc * e0 + wb * e1 + wms * e2
            nll = -float(np.sum(np.log(lik)))
            inv_l = -1.0 / lik
            d_wb = inv_l * (e1 - e0)
            d_wms = inv_l * (e2 - e0)
            g = np.array([
                float(np.sum(d_wb * gb)),
                float(np.sum(d_wms * gm)),
                float(np.sum(d_wms)),
                float(np.sum(d_wb * (pb * dgb))),
                float(np.sum(d_wms * (pm * dgm))),
            ])
            return nll, g

        best_u = None
        p2_t = max(0.02, float(pi3[ui, 2]))
        for s_ps, s_tm in ((0.002, t0_scale * 0.6), (0.002, t0_scale * 1.2), (min(0.12, p2_t * 0.5), t0_scale)):
            ps0 = ps_b[0] if ps_b[0] == ps_b[1] else min(ps_b[1] - 1e-4, max(ps_b[0] + 1e-4, s_ps))
            x0 = [
                min(0.47, max(1e-4, float(pi3[ui, 1]) * 1.15)),
                min(0.47, max(1e-4, max(0.01, p2_t - ps0))),
                ps0,
                math.log(t0_scale),
                math.log(s_tm),
            ]
            r = minimize(_nll_u, x0, jac=True, bounds=bnds_u, method="L-BFGS-B", options={"ftol": 1e-13, "gtol": 1e-8})
            if best_u is None or r.fun < best_u.fun:
                best_u = r
        init_pars[ui] = best_u.x

    # Step 3: Exact converged joint 49-D analytic-gradient L-BFGS-B polish (unless two_step_static)
    if two_step_static:
        em_hat = em_init
        pars_hat = init_pars
        # Compute exact NLL
        P1 = em_hat[:, None, :] * bits[None, :, :] + (1.0 - em_hat[:, None, :]) * (1.0 - bits[None, :, :])
        E = np.prod(P1, axis=2)
        gb, _ = _gd_mat(dt_alk_all, pars_hat[:, 3])
        gm, _ = _gd_mat(dt_acid_all, pars_hat[:, 4])
        wb = pars_hat[:, 0:1] * gb
        wms = pars_hat[:, 2:3] + pars_hat[:, 1:2] * gm
        wc = np.maximum(1.0 - wb - wms, 1e-6)
        lik = wc * E[0, triples_all] + wb * E[1, triples_all] + wms * E[2, triples_all]
        total_ll = float(np.sum(np.log(lik)))
    else:
        def _joint_nll_grad(theta):
            em = theta[:9].reshape(3, 3)
            P1 = em[:, None, :] * bits[None, :, :] + (1.0 - em[:, None, :]) * (1.0 - bits[None, :, :])
            E = np.prod(P1, axis=2)
            dE = np.empty((3, 8, 3), dtype=float)
            dE[:, :, 0] = (2.0 * bits[:, 0] - 1.0)[None, :] * P1[:, :, 1] * P1[:, :, 2]
            dE[:, :, 1] = (2.0 * bits[:, 1] - 1.0)[None, :] * P1[:, :, 0] * P1[:, :, 2]
            dE[:, :, 2] = (2.0 * bits[:, 2] - 1.0)[None, :] * P1[:, :, 0] * P1[:, :, 1]

            pars = theta[9:].reshape(n_u, 5)
            pb, pm, ps, ltb, ltm = pars[:, 0], pars[:, 1], pars[:, 2], pars[:, 3], pars[:, 4]
            gb, dgb = _gd_mat(dt_alk_all, ltb)
            gm, dgm = _gd_mat(dt_acid_all, ltm)
            wb = pb[:, None] * gb
            wms = ps[:, None] + pm[:, None] * gm
            wc = 1.0 - wb - wms
            if np.any(wc <= 1e-6):
                return 1e12, np.zeros_like(theta)

            e0 = E[0, triples_all]
            e1 = E[1, triples_all]
            e2 = E[2, triples_all]
            lik = wc * e0 + wb * e1 + wms * e2
            nll = -float(np.sum(np.log(lik)))
            inv_l = -1.0 / lik

            grad = np.zeros_like(theta)
            d_wb = inv_l * (e1 - e0)
            d_wms = inv_l * (e2 - e0)
            g_pars = np.empty((n_u, 5), dtype=float)
            g_pars[:, 0] = np.sum(d_wb * gb, axis=1)
            g_pars[:, 1] = np.sum(d_wms * gm, axis=1)
            g_pars[:, 2] = np.sum(d_wms, axis=1)
            g_pars[:, 3] = np.sum(d_wb * (pb[:, None] * dgb), axis=1)
            g_pars[:, 4] = np.sum(d_wms * (pm[:, None] * dgm), axis=1)
            grad[9:] = g_pars.ravel()

            w_all = np.vstack([(inv_l * wc).ravel(), (inv_l * wb).ravel(), (inv_l * wms).ravel()])
            g_E = np.vstack([np.bincount(tr_flat, weights=w_all[c], minlength=8) for c in range(3)])
            grad[:9] = np.einsum("ck,ckj->cj", g_E, dE).ravel()
            if map_alpha > 0.0:
                nll -= map_alpha * float(np.sum(np.log(em) + np.log(1.0 - em)))
                grad[:9] -= map_alpha * (1.0 / em - 1.0 / (1.0 - em)).ravel()
            return nll, grad

        bnds_j = [
            (1e-4, 0.25), (1e-4, 0.25), (1e-4, 0.25),
            (0.20, 0.9999), (0.30, 0.9999), (1e-4, 0.35),
            (0.30, 0.9999), (1e-4, 0.60), (0.20, 0.9999),
        ]
        for ui in range(n_u):
            ps_b = (0.0, 0.0) if (fix_ps_zero and ui in fix_ps_zero) else (
                (fix_tr06_ps, fix_tr06_ps) if (fix_tr06_ps is not None and ui == 5) else (0.0, 0.35)
            )
            bnds_j.extend([(0.0, 0.48), (0.0, 0.48), ps_b, (t_lo, t_hi), (t_lo, t_hi)])
        x_start = np.concatenate([em_init.ravel(), init_pars.ravel()])
        res = minimize(
            _joint_nll_grad, x_start, jac=True, bounds=bnds_j, method="L-BFGS-B",
            options={"ftol": 1e-14, "gtol": 1e-8, "maxiter": 1000, "maxcor": 25},
        )
        em_hat = res.x[:9].reshape(3, 3)
        pars_hat = res.x[9:].reshape(n_u, 5)
        total_ll = -float(res.fun)

    p_cl, p_fb, p_ms = em_hat[0], em_hat[1], em_hat[2]
    pi_bio = pars_hat[:, 0]
    pi_min = pars_hat[:, 1]
    pi_s = pars_hat[:, 2]
    tau_bio = np.exp(pars_hat[:, 3])
    tau_min = np.exp(pars_hat[:, 4])

    # Native-unit F3 trajectory check across 3 fleet post-acid age bands (0-16h, 16-120h, >=120h)
    p_d3_emit = np.array([p_cl[2], p_fb[2], p_ms[2]])
    bins = [(0.0, 16.0), (16.0, 120.0), (120.0, 1e9)]
    obs_curve, pred_curve = [], []
    gb_all, _ = _gd_mat(dt_alk_all, pars_hat[:, 3])
    gm_all, _ = _gd_mat(dt_acid_all, pars_hat[:, 4])
    for lo, hi in bins:
        obs_vals, pred_vals = [], []
        for ui, u in enumerate(TRAINS):
            dt_c = data["trains"][u]["dt_acid_h"]
            m = (dt_c >= lo) & (dt_c < hi)
            if not np.any(m):
                continue
            ov_u = float(np.mean(data["trains"][u]["d3"][m])) * 100.0
            wb = pi_bio[ui] * gb_all[ui][m]
            wms = pi_s[ui] + pi_min[ui] * gm_all[ui][m]
            wc = np.maximum(1.0 - wb - wms, 1e-6)
            pv_u = float(np.mean(wc * p_d3_emit[0] + wb * p_d3_emit[1] + wms * p_d3_emit[2])) * 100.0
            obs_vals.append(ov_u)
            pred_vals.append(pv_u)
        obs_curve.append(float(np.mean(obs_vals)))
        pred_curve.append(float(np.mean(pred_vals)))
    f3_pp = float(np.mean(np.abs(np.array(obs_curve) - np.array(pred_curve))))

    return {
        "pi_s": {u: float(pi_s[i]) for i, u in enumerate(TRAINS)},
        "pi_min": {u: float(pi_min[i]) for i, u in enumerate(TRAINS)},
        "pi_bio": {u: float(pi_bio[i]) for i, u in enumerate(TRAINS)},
        "tau_min": {u: float(tau_min[i]) for i, u in enumerate(TRAINS)},
        "tau_bio": {u: float(tau_bio[i]) for i, u in enumerate(TRAINS)},
        "emissions": (p_cl.tolist(), p_fb.tolist(), p_ms.tolist()),
        "ll": total_ll,
        "f3_pp": f3_pp,
        "obs_curve": obs_curve,
        "pred_curve": pred_curve,
    }


def _fit_static_post_cip_r2(data, window_h=120.0):
    """Exact Response 2 Round-2 solver: static [0, window_h] post-ALK / post-ACID 4-state EM."""
    n_u = len(TRAINS)
    triples_all = np.vstack([data["trains"][u]["triples"] for u in TRAINS])
    dt_alk_all = np.vstack([data["trains"][u]["dt_alk_h"] for u in TRAINS])
    dt_acid_all = np.vstack([data["trains"][u]["dt_acid_h"] for u in TRAINS])
    T = triples_all.shape[1]

    reg = np.zeros((n_u, T), dtype=np.int32)
    for ui in range(n_u):
        in_alk = dt_alk_all[ui] <= window_h
        in_acid = dt_acid_all[ui] <= window_h
        reg[ui] = np.where(in_acid & (~in_alk | (dt_acid_all[ui] <= dt_alk_all[ui])), 2,
                           np.where(in_alk, 1, 0))

    p_cl = np.array([0.02, 0.01, 0.01])
    p_fb = np.array([0.65, 0.85, 0.02])
    p_ms = np.array([0.80, 0.20, 0.65])
    pi_bio = np.full(n_u, 0.14)
    pi_min = np.full(n_u, 0.08)
    pi_s = np.full(n_u, 0.05)
    r_bio, r_min = 0.25, 0.25
    d1_all = ((triples_all >> 2) & 1).astype(float)
    d2_all = ((triples_all >> 1) & 1).astype(float)
    d3_all = (triples_all & 1).astype(float)

    for _ in range(100):
        E = np.vstack([_indep_dist_vec(p_cl), _indep_dist_vec(p_fb), _indep_dist_vec(p_ms)])
        num_c = np.zeros((3, 3))
        den_c = np.zeros(3)
        r_bio_num, r_bio_den = 0.0, 0.0
        r_min_num, r_min_den = 0.0, 0.0
        for ui in range(n_u):
            tr_idx = triples_all[ui]
            rg = reg[ui]
            wb = np.where(rg == 1, pi_bio[ui] * r_bio, pi_bio[ui])
            wm = np.where(rg == 2, pi_min[ui] * r_min, pi_min[ui])
            ws = np.full(T, pi_s[ui])
            wc = np.maximum(1.0 - wb - wm - ws, 1e-6)
            l0 = wc * E[0, tr_idx]
            l1 = wb * E[1, tr_idx]
            l2m = wm * E[2, tr_idx]
            l2s = ws * E[2, tr_idx]
            ltot = np.maximum(l0 + l1 + l2m + l2s, 1e-15)
            p0, p1, p2m, p2s = l0 / ltot, l1 / ltot, l2m / ltot, l2s / ltot
            m_alk = rg == 1
            m_acd = rg == 2
            pi_bio[ui] = float(np.clip(np.mean(p1[~m_alk]), 0.005, 0.45))
            pi_min[ui] = float(np.clip(np.mean(p2m[~m_acd]), 0.000, 0.45))
            pi_s[ui] = float(np.clip(np.mean(p2s), 0.000, 0.35))
            if np.any(m_alk):
                r_bio_num += float(np.sum(p1[m_alk]))
                r_bio_den += float(np.sum(m_alk)) * pi_bio[ui]
            if np.any(m_acd):
                r_min_num += float(np.sum(p2m[m_acd]))
                r_min_den += float(np.sum(m_acd)) * pi_min[ui]
            for c, pc in enumerate((p0, p1, p2m + p2s)):
                den_c[c] += float(np.sum(pc))
                num_c[c, 0] += float(np.dot(pc, d1_all[ui]))
                num_c[c, 1] += float(np.dot(pc, d2_all[ui]))
                num_c[c, 2] += float(np.dot(pc, d3_all[ui]))
        r_bio = float(np.clip(r_bio_num / max(r_bio_den, 1e-6), 0.05, 0.65))
        r_min = float(np.clip(r_min_num / max(r_min_den, 1e-6), 0.05, 0.65))
        p_cl = np.clip(num_c[0] / max(den_c[0], 1.0), 0.001, 0.20)
        p_fb = np.clip(num_c[1] / max(den_c[1], 1.0), 0.001, 0.999)
        p_ms = np.clip(num_c[2] / max(den_c[2], 1.0), 0.001, 0.999)

    p_d3_emit = np.array([p_cl[2], p_fb[2], p_ms[2]])
    bins = [(0.0, 16.0), (16.0, 120.0), (120.0, 1e9)]
    obs_curve, pred_curve = [], []
    for lo, hi in bins:
        ov, pv = [], []
        for ui, u in enumerate(TRAINS):
            dt_c = data["trains"][u]["dt_acid_h"]
            m = (dt_c >= lo) & (dt_c < hi)
            if not np.any(m):
                continue
            ov_u = float(np.mean(data["trains"][u]["d3"][m])) * 100.0
            rg = reg[ui][m]
            wb = np.where(rg == 1, pi_bio[ui] * r_bio, pi_bio[ui])
            wms = pi_s[ui] + np.where(rg == 2, pi_min[ui] * r_min, pi_min[ui])
            wc = np.maximum(1.0 - wb - wms, 1e-6)
            pv_u = float(np.mean(wc * p_d3_emit[0] + wb * p_d3_emit[1] + wms * p_d3_emit[2])) * 100.0
            ov.append(ov_u)
            pv.append(pv_u)
        obs_curve.append(float(np.mean(ov)))
        pred_curve.append(float(np.mean(pv)))
    f3_pp = float(np.mean(np.abs(np.array(obs_curve) - np.array(pred_curve))))
    return {u: float(pi_s[i]) for i, u in enumerate(TRAINS)}, f3_pp


def _fit_uncond_3class_r1(data):
    """Exact Response 1 Round-2 solver: 3-class unconditioned LCA ignoring CIP log."""
    triples_all = np.vstack([data["trains"][u]["triples"] for u in TRAINS])
    p_cl, p_fb, p_ms, pi3 = _static_3class_em(triples_all, n_iter=100)
    p_d3 = np.array([p_cl[2], p_fb[2], p_ms[2]])
    bins = [(0.0, 16.0), (16.0, 120.0), (120.0, 1e9)]
    obs_c, pred_c = [], []
    for lo, hi in bins:
        ov, pv = [], []
        for ui, u in enumerate(TRAINS):
            dt_c = data["trains"][u]["dt_acid_h"]
            m = (dt_c >= lo) & (dt_c < hi)
            if np.any(m):
                ov_u = float(np.mean(data["trains"][u]["d3"][m])) * 100.0
                pv_u = float(np.dot(pi3[ui], p_d3)) * 100.0
                ov.append(ov_u)
                pv.append(pv_u)
        obs_c.append(float(np.mean(ov)))
        pred_c.append(float(np.mean(pv)))
    f3_pp = float(np.mean(np.abs(np.array(obs_c) - np.array(pred_c))))
    return {u: float(pi3[i, 2]) for i, u in enumerate(TRAINS)}, f3_pp


def estimate_s3(
    data,
    mode="golden",
    kinetics="exp_time",
    dt_shift=0.0,
    map_alpha=0.0,
    two_step_static=False,
    bic_prune=False,
):
    q_idx_h = _q_index_hour()
    out = {}
    if mode == "hurried":
        for u in TRAINS:
            tr = data["trains"][u]
            mv = (tr["d1"] + tr["d2"] + tr["d3"]) >= 2
            hq = [float(np.sum(mv & (q_idx_h == q))) for q in range(4)]
            out[u] = {"q": hq, "f3_pp": 5.50, "pi_s": float(np.mean(mv))}
        return out

    if mode == "r1_uncond_3class":
        pis, f3 = _fit_uncond_3class_r1(data)
        for u in TRAINS:
            out[u] = {"q": [pis[u] * Q_HOURS[q] for q in range(4)], "f3_pp": f3, "pi_s": pis[u]}
        return out

    if mode in ("r2_static_120h", "r2_static_72h", "r2_static_48h"):
        wh = {"r2_static_120h": 120.0, "r2_static_72h": 72.0, "r2_static_48h": 48.0}[mode]
        pis, f3 = _fit_static_post_cip_r2(data, window_h=wh)
        for u in TRAINS:
            out[u] = {"q": [pis[u] * Q_HOURS[q] for q in range(4)], "f3_pp": f3, "pi_s": pis[u]}
        return out

    if mode == "post_cip_mv":
        for u in TRAINS:
            tr = data["trains"][u]
            mv = ((tr["d1"] + tr["d2"] + tr["d3"]) >= 2) & (tr["dt_acid_h"] <= 120.0)
            p_rate = float(np.mean(mv[tr["dt_acid_h"] <= 120.0]))
            out[u] = {"q": [p_rate * Q_HOURS[q] for q in range(4)], "f3_pp": 4.80, "pi_s": p_rate}
        return out

    if mode == "unanimous":
        for u in TRAINS:
            tr = data["trains"][u]
            un = (tr["d1"] + tr["d2"] + tr["d3"]) == 3
            hq = [float(np.sum(un & (q_idx_h == q))) for q in range(4)]
            out[u] = {"q": hq, "f3_pp": 4.50, "pi_s": float(np.mean(un))}
        return out

    if mode == "over_raw_d3_early_acid":
        for u in TRAINS:
            tr = data["trains"][u]
            m = tr["dt_acid_h"] <= 12.0
            rate = max(0.0, float(np.mean(tr["d3"][m])) - 0.008)
            out[u] = {"q": [rate * Q_HOURS[q] for q in range(4)], "f3_pp": 2.90, "pi_s": rate}
        return out

    if bic_prune:
        fit = _fit_kinetic_dual_cip(data, kinetics=kinetics, fix_ps_zero={0, 1, 2, 3, 4, 6, 7})
    else:
        fit = _fit_kinetic_dual_cip(
            data,
            kinetics=kinetics,
            dt_shift=dt_shift,
            map_alpha=map_alpha,
            two_step_static=two_step_static,
        )
    for u in TRAINS:
        pi_s = fit["pi_s"][u]
        out[u] = {
            "q": [pi_s * Q_HOURS[q] for q in range(4)],
            "f3_pp": fit["f3_pp"],
            "pi_s": pi_s,
            "pi_min": fit["pi_min"][u],
            "tau_min": fit["tau_min"][u],
            "ll": fit["ll"],
            "emissions": fit["emissions"],
        }
    return out


# ==============================================================================
# S4 ESTIMATORS: Shared Bay Permeate Collector TDS -> Variance-Component Deconv
# ==============================================================================

def estimate_s4(data, mode="golden", var_method="mle", meter_noise=True, mean_mode="ols"):
    q_idx_h = _q_index_hour()
    mv = (TDS_METER_SD ** 2) if meter_noise else 0.0
    out = {}

    for bay_name, members in BAYS.items():
        bay = data["bays"][bay_name]
        w_mat = bay["w_mat"]               # (8760, 4)
        y = bay["collector_tds_h"]         # (8760,)
        n = len(y)

        if mode == "hurried":
            # Naive: count shared bay collector exceedances (> 450 mg/L) directly!
            hq_bay = [float(np.sum((y > TDS_LIMIT) & (q_idx_h == q))) for q in range(4)]
            for u in members:
                out[u] = {"q": hq_bay, "f4_err": 12.0, "sd_hat": float(np.std(y)), "mu_q": [float(np.mean(y))] * 4}
            continue

        # Step 1: Fit exact per-train quarterly means mu_{u,q} via OLS (or Huber) on y ~ w_{u,t} * I(q)
        X = np.zeros((n, 16), dtype=float)
        for q in range(4):
            m = q_idx_h == q
            X[m, 4 * q:4 * q + 4] = w_mat[m]
        wt = np.ones(n, dtype=float)
        for _ in range(10 if mean_mode == "huber" else 1):
            sw = np.sqrt(wt)[:, None]
            coef, *_ = np.linalg.lstsq(X * sw, y * sw[:, 0], rcond=None)
            if mean_mode == "huber":
                r = y - X @ coef
                mad = float(np.median(np.abs(r - np.median(r)))) * 1.4826 + 1e-6
                d = 1.345 * mad
                wt = np.where(np.abs(r) <= d, 1.0, d / np.maximum(np.abs(r), 1e-9))
        mu_q_mat = coef.reshape(4, 4)  # (4 quarters, 4 trains)
        res = y - X @ coef
        w2 = w_mat ** 2

        if mode in ("equal_var_pool", "r1_r2_equal_var"):
            # Seductive textbook shortcut (also S4's one_fact_shortcut!):
            # Recover exact train means mu_{u,q} via OLS, then assume pooled/equal train variance sigma^2!
            sig2_pool = max(16.0, (float(np.var(res, ddof=16)) - mv) / float(np.mean(np.sum(w2, axis=1))))
            sig2_vec = np.full(4, sig2_pool)
        elif mode == "bay_sd_direct":
            # Use raw bay residual SD directly for every train
            sig2_vec = np.full(4, max(16.0, float(np.var(res, ddof=16))))
        elif mode == "over_bay_sd_2x":
            # Over-correction: blindly multiply raw bay SD by sqrt(4) = 2 for every train (flips TR05!)
            sig2_vec = np.full(4, max(16.0, 4.0 * float(np.var(res, ddof=16))))
        else:
            # Golden heteroscedastic variance-component deconvolution
            if var_method == "ols_sq":
                # OLS of (res^2 - mv) on w2
                c_v, *_ = np.linalg.lstsq(w2, res * res - mv, rcond=None)
                sig2_vec = np.clip(c_v, 25.0, 15000.0)
            elif var_method == "wls_sq":
                # 2-step feasible GLS on res^2
                c0, *_ = np.linalg.lstsq(w2, res * res - mv, rcond=None)
                v_hat = np.maximum(mv + w2 @ np.clip(c0, 25.0, 15000.0), 10.0)
                sw = 1.0 / v_hat
                c_v, *_ = np.linalg.lstsq(w2 * sw[:, None], (res * res - mv) * sw, rcond=None)
                sig2_vec = np.clip(c_v, 25.0, 15000.0)
            elif var_method == "joint_gls_mle":
                # Joint iterative GLS mean + heteroscedastic Gaussian variance-component MLE
                sig2_vec = np.full(4, 900.0)
                for _ in range(4):
                    v_cur = mv + w2 @ sig2_vec
                    sw = 1.0 / np.sqrt(np.maximum(v_cur, 1.0))
                    coef, *_ = np.linalg.lstsq(X * sw[:, None], y * sw, rcond=None)
                    mu_q_mat = coef.reshape(4, 4)
                    res = y - X @ coef
                    r2 = res * res
                    def _nll_gls(lv):
                        s2 = np.exp(lv)
                        v = mv + w2 @ s2
                        nll = 0.5 * float(np.sum(np.log(v) + r2 / v))
                        grad = 0.5 * s2 * (w2.T @ ((1.0 - r2 / v) / v))
                        return nll, grad
                    opt = minimize(_nll_gls, np.log(sig2_vec), jac=True,
                                   bounds=[(math.log(25.0), math.log(15000.0))] * 4,
                                   method="L-BFGS-B", options={"ftol": 1e-13, "gtol": 1e-10})
                    sig2_vec = np.exp(opt.x)
            elif var_method == "ar1_mle":
                # Temporal AR(1) Gaussian innovation variance MLE accounting for lag-1 bay residual autocorr rho
                rho = float(np.clip(np.corrcoef(res[:-1], res[1:])[0, 1], 0.0, 0.85))
                e_ar = res[1:] - rho * res[:-1]
                e2 = e_ar * e_ar
                # Var(e_t) = mv*(1 + rho^2) + sum_u sigma_u^2 * (w_{t,u}^2 + rho^2 w_{t-1,u}^2 - 2*rho^2 w_{t,u} w_{t-1,u})
                # For AR(1) train TDS with same rho: Cov(zeta_t, zeta_{t-1}) = rho * sigma_u^2
                w_eff2 = (w_mat[1:] ** 2) + (rho ** 2) * (w_mat[:-1] ** 2) - 2.0 * (rho ** 2) * (w_mat[1:] * w_mat[:-1])
                mv_eff = mv * (1.0 + rho * rho)
                def _nll_ar1(lv):
                    s2 = np.exp(lv)
                    v = np.maximum(mv_eff + w_eff2 @ s2, 1.0)
                    nll = 0.5 * float(np.sum(np.log(v) + e2 / v))
                    grad = 0.5 * s2 * (w_eff2.T @ ((1.0 - e2 / v) / v))
                    return nll, grad
                opt = minimize(_nll_ar1, np.full(4, math.log(900.0)), jac=True,
                               bounds=[(math.log(25.0), math.log(15000.0))] * 4,
                               method="L-BFGS-B", options={"ftol": 1e-13, "gtol": 1e-10})
                sig2_vec = np.exp(opt.x)
            elif var_method in ("kalman_ar1_mle", "gls_kalman_mle"):
                # Exact 4-state AR(1) Kalman-filter Gaussian MLE (2-stage OLS or GLS-iterated means)
                w0, w1, w2c, w3 = w_mat[:, 0].tolist(), w_mat[:, 1].tolist(), w_mat[:, 2].tolist(), w_mat[:, 3].tolist()
                # Fast i.i.d. warm start
                r2_i = res * res
                def _nll_w(lv):
                    s2 = np.exp(lv)
                    v = mv + w2 @ s2
                    return 0.5 * float(np.sum(np.log(v) + r2_i / v)), 0.5 * s2 * (w2.T @ ((1.0 - r2_i / v) / v))
                opt_w = minimize(_nll_w, np.full(4, math.log(900.0)), jac=True,
                                 bounds=[(math.log(25.0), math.log(15000.0))] * 4,
                                 method="L-BFGS-B", options={"ftol": 1e-12, "gtol": 1e-9})
                rho0 = float(np.clip(np.corrcoef(res[:-1], res[1:])[0, 1], 0.05, 0.80))
                cur_x = list(opt_w.x) + [rho0]
                n_outer = 2 if var_method == "gls_kalman_mle" else 1
                for it_k in range(n_outer):
                    if it_k > 0:
                        # Cochrane-Orcutt AR(1) + heteroscedastic GLS re-estimation of quarterly means
                        rk = float(cur_x[4])
                        s2k = np.exp(cur_x[:4])
                        w_eff2 = (w_mat[1:] ** 2) + (rk ** 2) * (w_mat[:-1] ** 2) - 2.0 * (rk ** 2) * (w_mat[1:] * w_mat[:-1])
                        v_gls = np.maximum(mv * (1.0 + rk * rk) + w_eff2 @ s2k, 1.0)
                        sw_g = 1.0 / np.sqrt(v_gls)
                        Xg = (X[1:] - rk * X[:-1]) * sw_g[:, None]
                        yg = (y[1:] - rk * y[:-1]) * sw_g
                        coef, *_ = np.linalg.lstsq(Xg, yg, rcond=None)
                        mu_q_mat = coef.reshape(4, 4)
                        res = y - X @ coef
                    res_l = res.tolist()
                    nll_fn = _make_kalman_nll_bay(w0, w1, w2c, w3, res_l, mv)
                    opt_k = minimize(
                        nll_fn, cur_x,
                        bounds=[(math.log(25.0), math.log(15000.0))] * 4 + [(0.0, 0.90)],
                        method="L-BFGS-B", options={"ftol": 1e-10},
                    )
                    cur_x = list(opt_k.x)
                sig2_vec = np.exp(cur_x[:4])
            else:
                # Exact Gaussian heteroscedastic variance-component MLE across all 8,760 hours
                r2 = res * res
                def _nll_var(lv):
                    s2 = np.exp(lv)
                    v = mv + w2 @ s2
                    nll = 0.5 * float(np.sum(np.log(v) + r2 / v))
                    grad = 0.5 * s2 * (w2.T @ ((1.0 - r2 / v) / v))
                    return nll, grad
                opt = minimize(_nll_var, np.full(4, math.log(900.0)), jac=True,
                               bounds=[(math.log(25.0), math.log(15000.0))] * 4,
                               method="L-BFGS-B", options={"ftol": 1e-13, "gtol": 1e-10})
                sig2_vec = np.exp(opt.x)

        # Native-unit F4 check: quartile-binned bay residual SD across each train's flow share w_{u,t}
        pred_var = mv + w2 @ sig2_vec
        f4_errs = []
        for ti in range(4):
            qs = np.quantile(w_mat[:, ti], [0.0, 0.25, 0.50, 0.75, 1.0])
            for bi in range(4):
                mask = (w_mat[:, ti] >= qs[bi]) & (w_mat[:, ti] <= qs[bi + 1])
                obs_sd = math.sqrt(float(np.mean(res[mask] ** 2)))
                mod_sd = math.sqrt(float(np.mean(pred_var[mask])))
                f4_errs.append(abs(obs_sd - mod_sd))
        f4_err = float(np.mean(f4_errs))

        for ti, u in enumerate(members):
            sd_u = math.sqrt(float(sig2_vec[ti]))
            mu_qs = mu_q_mat[:, ti]
            hq = [Q_HOURS[q] * float(_norm_sf((TDS_LIMIT - mu_qs[q]) / max(sd_u, 1e-6))) for q in range(4)]
            out[u] = {"q": hq, "f4_err": f4_err, "sd_hat": sd_u, "mu_q": mu_qs.tolist()}
    return out


def _make_kalman_nll_bay(w0, w1, w2c, w3, res_l, mv):
    """Fast scalar exact 4-state AR(1) Kalman filter Gaussian negative log-likelihood."""
    n = len(res_l)
    log = math.log
    exp = math.exp

    def _nll(params):
        s0, s1, s2, s3 = exp(params[0]), exp(params[1]), exp(params[2]), exp(params[3])
        rho = float(params[4])
        r2 = rho * rho
        omr2 = 1.0 - r2
        q0, q1, q2, q3 = s0 * omr2, s1 * omr2, s2 * omr2, s3 * omr2
        p00, p01, p02, p03 = s0, 0.0, 0.0, 0.0
        p11, p12, p13 = s1, 0.0, 0.0
        p22, p23 = s2, 0.0
        p33 = s3
        x0 = x1 = x2 = x3 = 0.0
        nll = 0.0
        for t in range(n):
            a0, a1, a2, a3 = w0[t], w1[t], w2c[t], w3[t]
            if t:
                x0 *= rho
                x1 *= rho
                x2 *= rho
                x3 *= rho
                p00 = r2 * p00 + q0
                p01 *= r2
                p02 *= r2
                p03 *= r2
                p11 = r2 * p11 + q1
                p12 *= r2
                p13 *= r2
                p22 = r2 * p22 + q2
                p23 *= r2
                p33 = r2 * p33 + q3
            pw0 = p00 * a0 + p01 * a1 + p02 * a2 + p03 * a3
            pw1 = p01 * a0 + p11 * a1 + p12 * a2 + p13 * a3
            pw2 = p02 * a0 + p12 * a1 + p22 * a2 + p23 * a3
            pw3 = p03 * a0 + p13 * a1 + p23 * a2 + p33 * a3
            S = a0 * pw0 + a1 * pw1 + a2 * pw2 + a3 * pw3 + mv
            e = res_l[t] - (a0 * x0 + a1 * x1 + a2 * x2 + a3 * x3)
            invS = 1.0 / S
            nll += 0.5 * (log(S) + e * e * invS)
            k0, k1, k2, k3 = pw0 * invS, pw1 * invS, pw2 * invS, pw3 * invS
            x0 += k0 * e
            x1 += k1 * e
            x2 += k2 * e
            x3 += k3 * e
            p00 -= k0 * pw0
            p01 -= k0 * pw1
            p02 -= k0 * pw2
            p03 -= k0 * pw3
            p11 -= k1 * pw1
            p12 -= k1 * pw2
            p13 -= k1 * pw3
            p22 -= k2 * pw2
            p23 -= k2 * pw3
            p33 -= k3 * pw3
        return nll

    return _nll


def compute_tr05_kalman_lrt(data, non_tds_tr05, sched_ratio_tr05=None, tds_sal_q=None, q_hours=None):
    """Exact 4-state AR(1) Kalman profile-likelihood LRT testing H0: TR05 >= 400.0 h."""
    sr5 = sched_ratio_tr05 or PLAN_SCHED_RATIO["TR05"]
    ts_q = tds_sal_q or PLAN_TDS_SAL_Q
    qh = q_hours or Q_HOURS
    bay = data["bays"]["South"]
    w_mat = bay["w_mat"]
    y = bay["collector_tds_h"]
    q_idx = _q_index_hour()
    X = np.zeros((len(y), 16), dtype=float)
    for q in range(4):
        m = q_idx == q
        X[m, 4 * q:4 * q + 4] = w_mat[m]
    coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    mu_q = coef.reshape(4, 4)
    res_l = (y - X @ coef).tolist()
    headroom = max(1.0, THRESHOLD - non_tds_tr05)

    def _tds5(sd):
        return sum(qh[q] * float(_norm_sf((TDS_LIMIT - mu_q[q, 0]) / sd)) * ts_q[q] * sr5[q] for q in range(4))

    lo, hi = 1.0, 90.0
    for _ in range(50):
        mid = 0.5 * (lo + hi)
        if _tds5(mid) < headroom:
            lo = mid
        else:
            hi = mid
    sd_crit = 0.5 * (lo + hi)

    mv = TDS_METER_SD ** 2
    nll_fn = _make_kalman_nll_bay(
        w_mat[:, 0].tolist(), w_mat[:, 1].tolist(), w_mat[:, 2].tolist(), w_mat[:, 3].tolist(), res_l, mv
    )
    opt_u = minimize(
        nll_fn,
        [math.log(200.0), math.log(900.0), math.log(1600.0), math.log(2800.0), 0.35],
        bounds=[(math.log(25.0), math.log(15000.0))] * 4 + [(0.0, 0.90)],
        method="L-BFGS-B",
        options={"ftol": 1e-10},
    )
    opt_c = minimize(
        nll_fn,
        [math.log(sd_crit * sd_crit)] + list(opt_u.x[1:]),
        bounds=[(math.log(sd_crit * sd_crit), math.log(15000.0))] + [(math.log(25.0), math.log(15000.0))] * 3 + [(0.0, 0.90)],
        method="L-BFGS-B",
        options={"ftol": 1e-10},
    )
    return max(0.0, 2.0 * (opt_c.fun - opt_u.fun))


# ==============================================================================
# ASSEMBLY, FALSIFICATION & CORELIB V4-HARDENED SPECIFICATION
# ==============================================================================

def assemble(r1, r2, r3, r4, forward=True):
    members = {}
    c1 = c2 = c3 = c4 = q3_tot = energy_kwh = 0.0
    for u in TRAINS:
        sr = PLAN_SCHED_RATIO[u] if forward else (1.0, 1.0, 1.0, 1.0)
        bt = PLAN_BORON_TEMP_Q if forward else (1.0, 1.0, 1.0, 1.0)
        sc = PLAN_SCALING_REC_Q if forward else (1.0, 1.0, 1.0, 1.0)
        td = PLAN_TDS_SAL_Q if forward else (1.0, 1.0, 1.0, 1.0)
        b_q = [r1[u]["q"][q] * bt[q] * sr[q] for q in range(4)]
        s_q = [r2[u]["q"][q] * sc[q] * sr[q] for q in range(4)]
        st_q = [r3[u]["q"][q] * sr[q] for q in range(4)]
        t_q = [r4[u]["q"][q] * td[q] * sr[q] for q in range(4)]
        bu, su, stu, tu = sum(b_q), sum(s_q), sum(st_q), sum(t_q)
        members[u] = bu + su + stu + tu
        c1 += bu
        c2 += su
        c3 += stu
        c4 += tu
        q3_tot += b_q[2] + s_q[2] + st_q[2] + t_q[2]
        energy_kwh += (
            bu * ENERGY_BORON_KWH
            + su * ENERGY_SCALING_KWH
            + stu * ENERGY_STRUCT_KWH
            + tu * ENERGY_TDS_KWH
        )
    ov_set = [u for u in TRAINS if members[u] >= THRESHOLD]
    ov_tot = sum(members[u] for u in ov_set)
    ov_mwh = 0.0
    for u in ov_set:
        sr = PLAN_SCHED_RATIO[u] if forward else (1.0, 1.0, 1.0, 1.0)
        bt = PLAN_BORON_TEMP_Q if forward else (1.0, 1.0, 1.0, 1.0)
        sc = PLAN_SCALING_REC_Q if forward else (1.0, 1.0, 1.0, 1.0)
        td = PLAN_TDS_SAL_Q if forward else (1.0, 1.0, 1.0, 1.0)
        bu = sum(r1[u]["q"][q] * bt[q] * sr[q] for q in range(4))
        su = sum(r2[u]["q"][q] * sc[q] * sr[q] for q in range(4))
        stu = sum(r3[u]["q"][q] * sr[q] for q in range(4))
        tu = sum(r4[u]["q"][q] * td[q] * sr[q] for q in range(4))
        ov_mwh += (bu * ENERGY_BORON_KWH + su * ENERGY_SCALING_KWH + stu * ENERGY_STRUCT_KWH + tu * ENERGY_TDS_KWH) / 1000.0
    return {
        "members": members,
        "C1_boron_2027": c1,
        "C2_scaling_2027": c2,
        "C3_struct_2027": c3,
        "C4_tds_2027": c4,
        "A_total_2027": c1 + c2 + c3 + c4,
        "A_overhaul_2027": ov_tot,
        "A_q3_2027": q3_tot,
        "A_energy_mwh": energy_kwh / 1000.0,
        "A_overhaul_mwh": ov_mwh,
    }


def falsification_parts(r1, r2, r3, r4):
    f1 = float(np.mean([r1[u]["f1_err"] for u in TRAINS]))
    f2 = float(np.mean([r2[u]["c_rms"] for u in TRAINS]))
    f3 = float(r3["TR01"]["f3_pp"])
    f4 = float(np.mean([r4[u]["f4_err"] for u in TRAINS]))
    return f1, f2, f3, f4


def build_spec(seed=SEED):
    data = simulate_world(seed)

    # Truth
    t1 = {u: {"q": data["trains"][u]["truth_boron_q"]} for u in TRAINS}
    t2 = {u: {"q": data["trains"][u]["truth_scaling_q"]} for u in TRAINS}
    t3 = {u: {"q": data["trains"][u]["truth_struct_q"]} for u in TRAINS}
    t4 = {u: {"q": data["trains"][u]["truth_tds_q"]} for u in TRAINS}
    truth_asm = assemble(t1, t2, t3, t4)

    # Golden
    r1_g = estimate_s1(data, mode="golden")
    r2_g = estimate_s2(data, mode="golden")
    r3_g = estimate_s3(data, mode="golden")
    r4_g = estimate_s4(data, mode="golden")
    gold_asm = assemble(r1_g, r2_g, r3_g, r4_g)

    # Hurried / Direct
    r1_h = estimate_s1(data, mode="hurried")
    r2_h = estimate_s2(data, mode="hurried")
    r3_h = estimate_s3(data, mode="hurried")
    r4_h = estimate_s4(data, mode="hurried")

    # EXACT ROUND-2 3.5-HOUR FRONTIER SOLVERS AS PRICED RIVALS!
    # Response 1 (3h31m): 6-block homoscedastic AR(1) + fixed-lag TEP->stress + unconditioned 3-class EM + OLS equal-var TDS
    r1_r1 = estimate_s1(data, mode="r1_block_ar1")
    r2_r12 = estimate_s2(data, mode="r1_r2_fixed_lag_tep")
    r3_r1 = estimate_s3(data, mode="r1_uncond_3class")
    r4_r12 = estimate_s4(data, mode="r1_r2_equal_var")
    rig_r1_asm = assemble(r1_r1, r2_r12, r3_r1, r4_r12)

    # Response 2 (~3h): (a + c/Q) homoscedastic AR(1) + fixed-lag TEP->stress + static 120h post-CIP EM + OLS equal-var TDS
    r1_r2 = estimate_s1(data, mode="r2_flux_homosced")
    r3_r2 = estimate_s3(data, mode="r2_static_120h")
    rig_r2_asm = assemble(r1_r2, r2_r12, r3_r2, r4_r12)

    # 1-step post-hint shortcuts (Holistic Audit v4 coded one_fact_shortcut per stump!)
    r2_sp = estimate_s2(data, mode="single_plug")
    ofs_s1 = assemble(r1_r2, r2_g, r3_g, r4_g)   # Told "boron scales as 1/Q": fits a+c/Q homoscedastic AR -> misses TR01 & flips TR04!
    ofs_s2 = assemble(r1_g, r2_sp, r3_g, r4_g)   # Told "use variable-flow cumulative volume": fits 1D single-plug V_eff -> flips TR05!
    ofs_s3 = assemble(r1_g, r2_g, r3_r2, r4_g)   # Told "separate alkaline vs acid CIP": fits static 120h post-CIP EM -> flips TR03!
    ofs_s4 = assemble(r1_g, r2_g, r3_g, r4_r12)  # Told "deconvolve bay collector by flow weights": fits OLS + equal variance -> misses TR08 & flips TR05!

    # Two-sided over-corrections on all 4 stumps!
    r1_over = estimate_s1(data, mode="over_flux_iid")
    r2_over = estimate_s2(data, mode="over_comonotonic")
    r3_over = estimate_s3(data, mode="unanimous")
    r4_over = estimate_s4(data, mode="over_bay_sd_2x")
    over_s1 = assemble(r1_over, r2_g, r3_g, r4_g)
    over_s2 = assemble(r1_g, r2_over, r3_g, r4_g)
    over_s3 = assemble(r1_g, r2_g, r3_over, r4_g)
    over_s4 = assemble(r1_g, r2_g, r3_g, r4_over)

    # Full 15-corner stump drop lattice (S1, S2, S3, S4)
    from itertools import combinations
    stump_ids = ["S1", "S2", "S3", "S4"]
    lattice_asm = {}
    for k_len in range(1, 5):
        for comb in combinations(stump_ids, k_len):
            key = "+".join(comb)
            lattice_asm[key] = assemble(
                r1_h if "S1" in comb else r1_g,
                r2_h if "S2" in comb else r2_g,
                r3_h if "S3" in comb else r3_g,
                r4_h if "S4" in comb else r4_g,
            )

    # 39 Honest Converged Physical Estimator Variants (must ALL hold the exact 5-of-8 slate & rank!)
    s1_vars = [
        estimate_s1(data, mode="golden_mle"),
        estimate_s1(data, mode="golden_ou_mle"),
        estimate_s1(data, mode="golden", kernel="ou", obj="wls"),
        estimate_s1(data, mode="golden", kernel="ou", obj="wls_var"),
        estimate_s1(data, mode="golden", kernel="ar1", obj="ols"),
        estimate_s1(data, mode="golden", kernel="ar1", obj="lag1"),
        estimate_s1(data, mode="golden", kernel="ar1", obj="wls", trim_frac=0.005),
        estimate_s1(data, mode="golden", kernel="ar1", obj="wls", lab_noise=False),
        estimate_s1(data, mode="golden", kernel="ar1", obj="wls", use_8h=False),
        estimate_s1(data, mode="golden", kernel="ar1", obj="wls", reg_mode="huber"),
        estimate_s1(data, mode="golden", kernel="ar1", obj="wls", q_mu_j=True),
    ]
    s2_vars = [
        estimate_s2(data, mode="golden", flow_interp="step_left", loss_fn="l2"),
        estimate_s2(data, mode="golden", flow_interp="step_right", loss_fn="l2"),
        estimate_s2(data, mode="golden", flow_interp="midpoint", loss_fn="l2"),
        estimate_s2(data, mode="golden", flow_interp="trapz", loss_fn="l2"),
        estimate_s2(data, mode="golden", flow_interp="linear", loss_fn="l1"),
        estimate_s2(data, mode="golden", flow_interp="linear", loss_fn="huber"),
        estimate_s2(data, mode="golden", flow_interp="linear", loss_fn="trimmed_l2"),
        estimate_s2(data, mode="golden", flow_interp="linear", loss_fn="l2", tep_interp="nearest"),
    ]
    s3_vars = [
        estimate_s3(data, mode="golden", kinetics="exp_vol"),
        estimate_s3(data, mode="golden", kinetics="michaelis"),
        estimate_s3(data, mode="golden", kinetics="weibull_12"),
        estimate_s3(data, mode="golden", kinetics="weibull_09"),
        estimate_s3(data, mode="golden", kinetics="exp_time", dt_shift=0.5),
        estimate_s3(data, mode="golden", kinetics="exp_time", map_alpha=0.5),
        estimate_s3(data, mode="golden", kinetics="exp_time", map_alpha=1.0),
        estimate_s3(data, mode="golden", kinetics="exp_time", bic_prune=True),
        estimate_s3(data, mode="golden", kinetics="exp_time", two_step_static=True),
    ]
    s4_vars = [
        estimate_s4(data, mode="golden", var_method="ols_sq"),
        estimate_s4(data, mode="golden", var_method="wls_sq"),
        estimate_s4(data, mode="golden", var_method="mle", meter_noise=False),
        estimate_s4(data, mode="golden", var_method="mle", mean_mode="huber"),
        estimate_s4(data, mode="golden", var_method="joint_gls_mle"),
        estimate_s4(data, mode="golden", var_method="ar1_mle"),
        estimate_s4(data, mode="golden", var_method="kalman_ar1_mle"),
        estimate_s4(data, mode="golden", var_method="gls_kalman_mle"),
    ]
    variants = []
    for v1 in s1_vars:
        variants.append(assemble(v1, r2_g, r3_g, r4_g))
    for v2 in s2_vars:
        variants.append(assemble(r1_g, v2, r3_g, r4_g))
    for v3 in s3_vars:
        variants.append(assemble(r1_g, r2_g, v3, r4_g))
    for v4 in s4_vars:
        variants.append(assemble(r1_g, r2_g, r3_g, v4))
    # 3 joint cross-stump rebuilds (including all-exact-MLE + nearest-TEP + Kalman AR(1)!)
    variants.append(assemble(s1_vars[0], s2_vars[2], s3_vars[0], s4_vars[7]))
    variants.append(assemble(s1_vars[1], s2_vars[7], s3_vars[2], s4_vars[6]))
    variants.append(assemble(s1_vars[9], s2_vars[0], s3_vars[5], s4_vars[1]))

    # Run routes & extra rivals
    gen_asm = assemble(r1_over, r2_over, r3_r1, r4_over)
    r1_hedge = {u: {**r1_g[u], "q": [0.8 * r1_h[u]["q"][q] + 0.2 * r1_g[u]["q"][q] for q in range(4)], "f1_err": 1.3} for u in TRAINS}
    r2_hedge = {u: {**r2_g[u], "q": [0.8 * r2_h[u]["q"][q] + 0.2 * r2_g[u]["q"][q] for q in range(4)], "c_rms": 1.6} for u in TRAINS}
    r3_hedge = {u: {**r3_g[u], "q": [0.8 * r3_h[u]["q"][q] + 0.2 * r3_g[u]["q"][q] for q in range(4)], "f3_pp": 4.4} for u in TRAINS}
    r4_hedge = {u: {**r4_g[u], "q": [0.8 * r4_h[u]["q"][q] + 0.2 * r4_g[u]["q"][q] for q in range(4)], "f4_err": 9.5} for u in TRAINS}
    hedge_asm = assemble(r1_hedge, r2_hedge, r3_hedge, r4_hedge)

    r1_c4 = estimate_s1(data, mode="cutoff_4h")
    r1_stat = estimate_s1(data, mode="stat_ar1_no_flux")
    r1_fnd = estimate_s1(data, mode="flux_no_deconv")
    r2_flc = estimate_s2(data, mode="fixed_lag_cond")
    r2_nv = estimate_s2(data, mode="nom_vol")
    r3_72 = estimate_s3(data, mode="r2_static_72h")
    r3_48 = estimate_s3(data, mode="r2_static_48h")
    r3_cpmv = estimate_s3(data, mode="post_cip_mv")
    r3_un = estimate_s3(data, mode="unanimous")
    r4_bay = estimate_s4(data, mode="bay_sd_direct")
    cut_asm = assemble(r1_c4, r2_r12, r3_cpmv, r4_bay)

    extra_routes = {
        "cutoff:r1_round2_full": rig_r1_asm,
        "cutoff:r2_round2_full": rig_r2_asm,
        "cutoff:s1_r1_block_ar1": assemble(r1_r1, r2_g, r3_g, r4_g),
        "cutoff:s1_r2_flux_homosced": ofs_s1,
        "cutoff:s1_stat_ar1_no_flux": assemble(r1_stat, r2_g, r3_g, r4_g),
        "cutoff:s1_flux_no_deconv": assemble(r1_fnd, r2_g, r3_g, r4_g),
        "cutoff:s2_r1_r2_fixed_lag_tep": assemble(r1_g, r2_r12, r3_g, r4_g),
        "cutoff:s2_single_plug_veff": ofs_s2,
        "cutoff:s2_fixed_lag_cond": assemble(r1_g, r2_flc, r3_g, r4_g),
        "cutoff:s2_nom_vol": assemble(r1_g, r2_nv, r3_g, r4_g),
        "cutoff:s3_r1_uncond_3class": assemble(r1_g, r2_g, r3_r1, r4_g),
        "cutoff:s3_r2_static_120h": ofs_s3,
        "cutoff:s3_static_72h": assemble(r1_g, r2_g, r3_72, r4_g),
        "cutoff:s3_static_48h": assemble(r1_g, r2_g, r3_48, r4_g),
        "cutoff:s3_unanimous": assemble(r1_g, r2_g, r3_un, r4_g),
        "cutoff:s4_r1_r2_equal_var": ofs_s4,
        "cutoff:s4_bay_sd_direct": assemble(r1_g, r2_g, r3_g, r4_bay),
        "hedge:history_2026_flat": assemble(r1_g, r2_g, r3_g, r4_g, forward=False),
    }

    # Native-unit chi-squared goodness-of-fit statistic across all 4 physical checks (F1..F4)
    f2_floor = COND_PROBE_SD
    def _comb_fal(x1, x2, x3, x4):
        a, b, c, d = falsification_parts(x1, x2, x3, x4)
        b_ex = max(0.0, b - f2_floor)
        chi2 = (a / 0.10) ** 2 + (b_ex / 0.10) ** 2 + (c / 0.30) ** 2 + (d / 0.14) ** 2
        return chi2, (a, b, c, d)

    fal_g, fal_g_parts = _comb_fal(r1_g, r2_g, r3_g, r4_g)
    fal_rivals = {}
    fal_detail = {"golden": (fal_g, fal_g_parts)}
    for label, (x1, x2, x3, x4) in [
        ("direct", (r1_h, r2_h, r3_h, r4_h)),
        ("rigorous_r1", (r1_r1, r2_r12, r3_r1, r4_r12)),
        ("rigorous_r2", (r1_r2, r2_r12, r3_r2, r4_r12)),
        ("generous", (r1_over, r2_over, r3_r1, r4_over)),
        ("hedge", (r1_hedge, r2_hedge, r3_hedge, r4_hedge)),
        ("cutoff", (r1_c4, r2_r12, r3_cpmv, r4_bay)),
        ("S1_r2_homosc", (r1_r2, r2_g, r3_g, r4_g)),
        ("S2_r12_lag", (r1_g, r2_r12, r3_g, r4_g)),
        ("S2_single_plug", (r1_g, r2_sp, r3_g, r4_g)),
        ("S3_r1_uncond", (r1_g, r2_g, r3_r1, r4_g)),
        ("S3_r2_120h", (r1_g, r2_g, r3_r2, r4_g)),
        ("S4_eq_var", (r1_g, r2_g, r3_g, r4_r12)),
        ("S1_over", (r1_over, r2_g, r3_g, r4_g)),
        ("S2_over", (r1_g, r2_over, r3_g, r4_g)),
        ("S3_over", (r1_g, r2_g, r3_over, r4_g)),
        ("S4_over", (r1_g, r2_g, r3_g, r4_over)),
    ]:
        sc, parts = _comb_fal(x1, x2, x3, x4)
        fal_rivals[label] = sc
        fal_detail[label] = (sc, parts)

    members_spec = {}
    for u in TRAINS:
        members_spec[u] = {
            "lines": [THRESHOLD],
            "truth": truth_asm["members"][u],
            "golden": gold_asm["members"][u],
            "family": [v["members"][u] for v in variants],
            "routes": {
                "direct": lattice_asm["S1+S2+S3+S4"]["members"][u],
                "rigorous": rig_r2_asm["members"][u],  # Exact Response 2 Round-2 3.5h solver!
            },
        }

    stumps_spec = {
        "S1": {
            "axis": "unit",
            "opens": "TR01",
            "said_out_loud": (
                "Permeate boron obeys Spiegler-Kedem solute mass-flux conservation "
                "(C_t = alpha + J_B(t)/Q_t), making concentration variance scale as (sigma_J/Q_t)^2 "
                "inside 4h/8h flow-proportional composites."
            ),
            "steps_left": 4,
            "precedents": ["L22", "L56", "L57"],
            "sides": {"over": over_s1["members"]},
            "one_fact_shortcut": {
                "members": ofs_s1["members"],
                "component": ofs_s1["C1_boron_2027"],
            },
        },
        "S2": {
            "axis": "when",
            "opens": "TR02",
            "said_out_loud": (
                "Variable diurnal flows and two-path bimodal DAF/DMF short-circuiting "
                "require cumulative-volume Phi(t) two-path mixing recovered from seawater conductivity."
            ),
            "steps_left": 4,
            "precedents": ["L26", "L28", "N07", "N30"],
            "sides": {"over": over_s2["members"]},
            "one_fact_shortcut": {
                "members": ofs_s2["members"],
                "component": ofs_s2["C2_scaling_2027"],
            },
        },
        "S3": {
            "axis": "what",
            "opens": "TR03",
            "said_out_loud": (
                "Reversible mineral crust shares the exact single-block alarm profile of persistent "
                "structural breaches and re-grows rapidly after acid CIP, defeating both unconditioned "
                "LCA and static post-CIP windows."
            ),
            "steps_left": 4,
            "precedents": ["L03", "L38", "L54", "N36"],
            "sides": {"over": over_s3["members"]},
            "one_fact_shortcut": {
                "members": ofs_s3["members"],
                "component": ofs_s3["C3_struct_2027"],
            },
        },
        "S4": {
            "axis": "who",
            "opens": "TR08",
            "said_out_loud": (
                "Individual train permeate TDS breakthrough (> 450 mg/L) is observed only through "
                "shared bay collectors, requiring heteroscedastic variance-component deconvolution "
                "across staggered flow shares rather than equal-variance pooling."
            ),
            "steps_left": 4,
            "precedents": ["L22", "L33", "N36"],
            "sides": {"over": over_s4["members"]},
            "one_fact_shortcut": {
                "members": ofs_s4["members"],
                "component": ofs_s4["C4_tds_2027"],
            },
        },
    }

    lattice_spec = {k: v["members"] for k, v in lattice_asm.items()}
    run_routes_spec = {
        "generous": gen_asm["members"],
        "calibrated": {
            "none": (
                "No shipped file observes 1-hour boron grab samples, RO-header algal-TEP, "
                "destructive vessel autopsies, or individual train permeate TDS meters; "
                "forcing rests on native-unit physical identities F1 to F4."
            )
        },
        "hedge": hedge_asm["members"],
        "cutoff": cut_asm["members"],
    }
    for k, v in extra_routes.items():
        run_routes_spec[k] = v["members"]

    def _non_member_fig(fid, block, sentence=None, ecf=None):
        d = {
            "id": fid,
            "block": block,
            "sentence": sentence or fid,
            "golden": gold_asm[fid],
            "family": [v[fid] for v in variants],
            "lattice": {k: lattice_asm[k][fid] for k in lattice_asm},
            "routes": {
                "rigorous": rig_r2_asm[fid],
                "generous": gen_asm[fid],
                "hedge": hedge_asm[fid],
                "cutoff": cut_asm[fid],
            },
        }
        if ecf is not None:
            d["ecf"] = ecf
        return d

    figures_spec = [
        _non_member_fig("C1_boron_2027", "component"),
        _non_member_fig("C2_scaling_2027", "component"),
        _non_member_fig("C3_struct_2027", "component"),
        _non_member_fig("C4_tds_2027", "component"),
    ]
    for u in TRAINS:
        figures_spec.append({"id": f"A_{u}", "block": "ask", "member": u, "ecf": False})
    figures_spec.append(_non_member_fig("A_total_2027", "ask", "Ask2_totals", ecf=True))
    figures_spec.append(_non_member_fig("A_overhaul_2027", "ask", "Ask2_overhaul", ecf=False))
    figures_spec.append(_non_member_fig("A_q3_2027", "ask", "Ask2_q3", ecf=True))
    figures_spec.append(_non_member_fig("A_energy_mwh", "ask", "Ask3_energy_total", ecf=True))
    figures_spec.append(_non_member_fig("A_overhaul_mwh", "ask", "Ask3_energy_overhaul", ecf=False))

    spec = {
        "task": "task28",
        "v4_hardened": True,
        "call": "lines",
        "members": members_spec,
        "stumps": stumps_spec,
        "lattice": lattice_spec,
        "falsification": {
            "check": (
                "Four native-unit physical conservation & invariance checks (zero anomaly labels): "
                "F1 boron flux-space heteroscedasticity & 4h/8h moment identity; "
                "F2 two-path conservative seawater conductivity RMS (mS/cm); "
                "F3 post-acid CIP fine-age D3 kinetic trajectory mismatch (pp); "
                "F4 flow-share quartile bay collector TDS residual SD mismatch (mg/L)."
            ),
            "observes_target": False,
            "truth": 0.0,
            "golden": fal_g,
            "rivals": fal_rivals,
        },
        "run_routes": run_routes_spec,
        "figures": figures_spec,
    }

    diag = {
        "data": data,
        "truth_asm": truth_asm,
        "gold_asm": gold_asm,
        "rig_r1_asm": rig_r1_asm,
        "rig_r2_asm": rig_r2_asm,
        "lattice_asm": lattice_asm,
        "extra_routes": extra_routes,
        "over": {"S1": over_s1, "S2": over_s2, "S3": over_s3, "S4": over_s4},
        "ofs": {"S1": ofs_s1, "S2": ofs_s2, "S3": ofs_s3, "S4": ofs_s4},
        "fal_detail": fal_detail,
        "r1_g": r1_g, "r2_g": r2_g, "r3_g": r3_g, "r4_g": r4_g,
        "variants": variants,
    }
    return spec, diag


def run_forcing_perturbations(diag):
    """Test +/-20% independent perturbations on each of the 4 modes' golden 2026 hours."""
    r1_g, r2_g, r3_g, r4_g = diag["r1_g"], diag["r2_g"], diag["r3_g"], diag["r4_g"]
    g_slate = sorted(u for u in TRAINS if diag["gold_asm"]["members"][u] >= THRESHOLD)
    out = []
    for mode_name, idx in [("S1_boron", 1), ("S2_scaling", 2), ("S3_struct", 3), ("S4_tds", 4)]:
        for mult in (0.80, 1.20):
            x1 = {u: {**r1_g[u], "q": [v * mult for v in r1_g[u]["q"]]} for u in TRAINS} if idx == 1 else r1_g
            x2 = {u: {**r2_g[u], "q": [v * mult for v in r2_g[u]["q"]]} for u in TRAINS} if idx == 2 else r2_g
            x3 = {u: {**r3_g[u], "q": [v * mult for v in r3_g[u]["q"]]} for u in TRAINS} if idx == 3 else r3_g
            x4 = {u: {**r4_g[u], "q": [v * mult for v in r4_g[u]["q"]]} for u in TRAINS} if idx == 4 else r4_g
            asm = assemble(x1, x2, x3, x4)
            sl = sorted(u for u in TRAINS if asm["members"][u] >= THRESHOLD)
            ov_min = min(asm["members"][u] for u in g_slate)
            mo_max = max(asm["members"][u] for u in TRAINS if u not in g_slate)
            out.append({
                "input": f"{mode_name}_{int(round((mult - 1.0) * 100)):+d}pct",
                "holds": sl == g_slate,
                "answer": sl,
                "min_overhaul": round(ov_min, 1),
                "max_monitor": round(mo_max, 1),
            })
    return out


if __name__ == "__main__":
    spec, diag = build_spec(SEED)
    print("=== task28 v3 4-Stump Core Diagnostic (Seed %d) ===" % SEED)
    g = diag["gold_asm"]
    t = diag["truth_asm"]
    r1 = diag["rig_r1_asm"]
    r2 = diag["rig_r2_asm"]
    dir_a = diag["lattice_asm"]["S1+S2+S3+S4"]
    print(f"{'Train':5s} {'Truth':>7s} {'Golden':>7s} {'B27':>6s} {'S27':>6s} {'St27':>6s} {'T27':>6s} | {'Direct':>7s} {'R1_3.5h':>8s} {'R2_3.5h':>8s}")
    for u in TRAINS:
        sr = PLAN_SCHED_RATIO[u]
        b27 = sum(diag["r1_g"][u]["q"][q] * PLAN_BORON_TEMP_Q[q] * sr[q] for q in range(4))
        s27 = sum(diag["r2_g"][u]["q"][q] * PLAN_SCALING_REC_Q[q] * sr[q] for q in range(4))
        st27 = sum(diag["r3_g"][u]["q"][q] * sr[q] for q in range(4))
        t27 = sum(diag["r4_g"][u]["q"][q] * PLAN_TDS_SAL_Q[q] * sr[q] for q in range(4))
        print(
            f"{u:5s} {t['members'][u]:7.1f} {g['members'][u]:7.1f} {b27:6.1f} {s27:6.1f} {st27:6.1f} {t27:6.1f} | "
            f"{dir_a['members'][u]:7.1f} {r1['members'][u]:8.1f} {r2['members'][u]:8.1f}"
        )
    print(
        f"Plant 2027: C1={g['C1_boron_2027']:.1f} C2={g['C2_scaling_2027']:.1f} "
        f"C3={g['C3_struct_2027']:.1f} C4={g['C4_tds_2027']:.1f} "
        f"Total={g['A_total_2027']:.1f} Overhaul={g['A_overhaul_2027']:.1f} Q3={g['A_q3_2027']:.1f} "
        f"Energy={g['A_energy_mwh']:.1f} MWh OvEnergy={g['A_overhaul_mwh']:.1f} MWh"
    )
    print("Falsification (comb, F1, F2, F3, F4):")
    for k, (sc, parts) in diag["fal_detail"].items():
        print(f"  {k:16s}: {sc:7.3f}  (F1={parts[0]:.3f}, F2={parts[1]:.3f}, F3={parts[2]:.2f}pp, F4={parts[3]:.2f}mg/L)")
    print("Rival calls:")
    for k, asm in list(diag["extra_routes"].items()) + [(f"OVER_{s}", diag["over"][s]) for s in ("S1", "S2", "S3", "S4")]:
        sl = [u for u in TRAINS if asm["members"][u] >= THRESHOLD]
        print(f"  {k:32s}: {sl}")
    pert = run_forcing_perturbations(diag)
    print("Forcing +/-20% perturbations:")
    for pt in pert:
        print(f"  {pt['input']:20s}: holds={pt['holds']} min_ov={pt['min_overhaul']:.1f} max_mo={pt['max_monitor']:.1f}")
    sys.exit(corelib.run(spec))
