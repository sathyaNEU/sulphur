#!/usr/bin/env python3
"""task28/generator/core.py (v2): Barlavento SWRO Desalination Plant (Algarve, Portugal)
Level 5 Anomaly Detection & Diagnostics Core (Physical & Environmental Sciences /
process-control-measurement-systems).

Simulates 8 parallel seawater reverse-osmosis (SWRO) membrane trains (TR01..TR08)
across 2026 (365 days = 8,760 hours = 35,040 fifteen-minute intervals = 2,190 four-hour
diagnostic blocks per train) and diagnoses which trains reach Engineering Protocol
SWRO-Q27's 400-hour 2027 vessel overhaul criterion and the resulting excess desalination
energy penalty in MWh (420 / 360 / 540 kWh/h divided by 1,000).

Three genuinely independent, unannounced physical observation-process stumps engineered to
defeat not only raw/hurried monitoring, but also full 2.5-hour frontier textbook models
(stationary Gaussian AR(1) flow-weighted composite MLE, 1D single-plug cumulative-volume
V_eff conductivity CCF, 120h post-CIP 2-class Dawid-Skene, and 3-state pooled-CIP D3=0 EM):

  S1 (unit) - support_effect + conservation_residual_attribution:
              Fickian solution-diffusion flow-concentration coupling inside 4h/8h
              flow-proportional lab boron composite bottles:
                C_t = alpha_{u,q} + beta_u / Q_t + eps_t  ->  C_comp = alpha_{u,q} + beta_u / Q_bar_k + eps_bar_k^(Q)
              Flow-weighting induces Jensen AM/HM dilution bias AND bimodal low-flow spikes.
              Stationary Gaussian AR(1) flow-weighted composite MLE (ignoring beta_u / Q_t)
              under-counts flux-sensitive TR01 (drops < 400 h) AND mistakes deterministic
              diurnal beta/Q swings on tight-sigma TR04 for huge random sigma_1h (flips TR04 > 400 h).
              Over-correction (i.i.d. sqrt(m) residual scaling) also flips TR04 > 400 h.

  S2 (when) - asynchronous_measurement_covariance + non_additive_aggregation + conservation_residual_attribution:
              Two-path bimodal DAF/DMF hydraulic short-circuiting (parallel fast bypass f_u at
              V_fast + main baffled zone 1-f_u at V_main):
                c_out(Phi) = f_u c_in(Phi - V_fast) + (1 - f_u) c_in(Phi - V_main) + noise
                X_arr(Phi) = f_u x_in(Phi - V_fast) + (1 - f_u) x_in(Phi - V_main)
              Because 1 - f_u > f_u, 1D single-plug cumulative-volume conductivity CCF (argmax_k)
              locks onto the majority path V_main (getting reassuring r ~ 0.76-0.80) while leaving
              ~1.15 mS/cm residual RMS: misses fast-bypass-coupled TR02 (drops < 400 h) AND
              evaluates unmixed x_in instead of diluted X_arr on TR05 (flips TR05 > 400 h).
              Over-correction (comonotonic pairing) also flips TR05 > 400 h.

  S3 (what) - rival_process_by_state_dependence + latent_structure_estimation:
              4-state dual-recipe chemical CIP invariance across 192 multinomial cells
              (8 trains x 3 regimes [Pre-CIP, Post-CIP_ALK, Post-CIP_ACID] x 8 alarm triples):
                Clean, Organic Bio-Fouling (F_bio: cleared ~72% by CIP_ALK only, quiet D3),
                Mineral Crust Fouling (F_min: cleared ~76% by CIP_ACID only, triggers D3 ~ 0.44),
                Persistent Structural Breach (S: survives BOTH CIP_ALK and CIP_ACID).
              Both 120h post-CIP 2-class Dawid-Skene AND 3-state pooled-CIP (D3=0 fouling) EM
              misclassify TR03's reversible mineral crust as persistent structural damage (flips
              TR03 > 400 h). Over-correction (uninverted raw D3 or post-acid raw D3) drops
              structurally damaged TR06 < 400 h.

Pure Python standard library only, seeded, ending on sys.exit(corelib.run(spec)).
"""
import bisect
import math
import os
import random
import sys

sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..",
        "..",
        ".agents",
        "skills",
        "stumping",
    ),
)
import corelib

SEED = 2802
TRAINS = ["TR01", "TR02", "TR03", "TR04", "TR05", "TR06", "TR07", "TR08"]
THRESHOLD = 400.0  # Protocol SWRO-Q27 Clause 3.1: >= 400 forecasted 2027 anomalous hours

# Protocol SWRO-Q27 physical excursion limits (filed in swro_integrity_standard_q27.pdf)
BORON_LIMIT = 0.50       # mg/L single-hour permeate boron limit
SCALING_X_LIM = 1.50     # RO-header arrived pretreated algal-TEP index limit
SCALING_Y_LIM = 1.50     # RO-feed supersaturation-oxidant stress index limit

# Protocol SWRO-Q27 Clause 4.3 mode-specific excess desalination energy penalty rates (kWh/h; /1000 -> MWh)
ENERGY_BORON_KWH = 420.0
ENERGY_SCALING_KWH = 360.0
ENERGY_STRUCT_KWH = 540.0
# Backward-compatible aliases
TARIFF_BORON = ENERGY_BORON_KWH
TARIFF_SCALING = ENERGY_SCALING_KWH
TARIFF_STRUCT = ENERGY_STRUCT_KWH

# 2026 calendar quarters (exact hours: Q1=90d, Q2=91d, Q3=92d, Q4=92d -> 365d = 8760h)
Q_DAYS = [90, 91, 92, 92]
Q_HOURS = [d * 24 for d in Q_DAYS]
Q_STARTS_H = [0, 2160, 4344, 6552, 8760]

# Filed 2027 Operating Plan (operating_plan_2027.csv & Protocol SWRO-Q27 Annex B)
PLAN_BORON_TEMP_Q = [1.05, 1.14, 1.32, 1.09]
PLAN_SCALING_REC_Q = [1.03, 1.12, 1.28, 1.07]
PLAN_SCHED_RATIO = {
    "TR01": [1.08, 1.14, 1.22, 1.10],
    "TR02": [1.08, 1.15, 1.24, 1.10],
    "TR03": [1.06, 1.10, 1.18, 1.08],
    "TR04": [1.06, 1.10, 1.16, 1.08],
    "TR05": [1.06, 1.12, 1.18, 1.08],
    "TR06": [1.08, 1.14, 1.22, 1.10],
    "TR07": [1.10, 1.16, 1.25, 1.12],
    "TR08": [1.05, 1.08, 1.12, 1.06],
}

# Physical world parameters per train
# S1: C_t = b_alpha + s_q + b_beta / Q_t + eps_t (AR1 with sd=b_sd, corr scale=b_lam)
#     Flow Q_t: smooth diurnal solar/demand profile (q_mode='trough' smooth night turndown or 'cos' broad diurnal)
# S2: Two-path DAF/DMF basin: f_fast at v_fast + (1-f_fast) at v_main; x_in has mean x_mu, sd x_sd;
#     y_out has mean y_mu and couples to fast stream (rho_fast) and main stream (rho_main)
# S3: 4 latent states: Clean, Organic Bio-Fouling (pi_fbio, cleared by CIP_ALK),
#     Mineral Crust Fouling (pi_fmin, cleared by CIP_ACID), Persistent Structural (pi_struct)
WORLD = {
    "TR01": dict(  # OPENED BY S1 (flux coupling + AR1 -> raw, stat_ar1 (R1/R2), AND flux_no_deconv ALL drop < 400!)
        q_mode="trough", q_hi=600.0, q_drop=415.0, q_tc=3.5, q_tw=2.15,
        b_alpha=0.200, b_beta=54.0, b_sd=0.064, b_lam=0.80,
        v_nom=1200.0, f_fast=0.28, v_fast=400.0, v_main=940.0, x_sd=1.00, x_mu=-0.22, y_mu=-0.22, rho_fast=0.25, rho_main=0.55,
        pi_fbio=0.025, pi_fmin=0.015, pi_struct=0.0060, c_alk=0.75, c_acid=0.78,
    ),
    "TR02": dict(  # OPENED BY S2 (two-path f=0.46 fast bypass -> single_plug (R1/R2), hurried, fixed_lag, nom_vol ALL drop < 400!)
        q_mode="cos", q_hi=640.0, q_drop=360.0, q_tc=2.0, q_tw=2.5,
        b_alpha=0.260, b_beta=18.0, b_sd=0.044, b_lam=2.20,
        v_nom=1480.0, f_fast=0.46, v_fast=440.0, v_main=1400.0, x_sd=0.58, x_mu=1.10, y_mu=0.11, rho_fast=0.98, rho_main=0.00,
        pi_fbio=0.008, pi_fmin=0.006, pi_struct=0.0060, c_alk=0.75, c_acid=0.78,
    ),
    "TR03": dict(  # OPENED BY S3 (heavy mineral crust pi_fmin=0.145 + bio-fouling -> R1 pooled-CIP 3-state EM & R2 120h DS both flip > 400!)
        q_mode="cos", q_hi=620.0, q_drop=340.0, q_tc=2.5, q_tw=2.5,
        b_alpha=0.265, b_beta=16.0, b_sd=0.044, b_lam=2.40,
        v_nom=1180.0, f_fast=0.30, v_fast=380.0, v_main=920.0, x_sd=1.00, x_mu=-0.24, y_mu=-0.24, rho_fast=0.20, rho_main=0.55,
        pi_fbio=0.095, pi_fmin=0.145, pi_struct=0.0060, c_alk=0.75, c_acid=0.78,
    ),
    "TR04": dict(  # S1 OVER-CORRECTION & STAT-AR1 GUARD (large beta=66, smooth b_lam=8.5 -> over_iid & flux_iid BOTH flip > 400!)
        q_mode="cos", q_hi=700.0, q_drop=480.0, q_tc=2.0, q_tw=2.5,
        b_alpha=0.132, b_beta=66.0, b_sd=0.044, b_lam=8.50,
        v_nom=1220.0, f_fast=0.26, v_fast=410.0, v_main=960.0, x_sd=1.00, x_mu=-0.22, y_mu=-0.22, rho_fast=0.20, rho_main=0.55,
        pi_fbio=0.025, pi_fmin=0.018, pi_struct=0.0065, c_alk=0.75, c_acid=0.78,
    ),
    "TR05": dict(  # S2 SINGLE-PLUG (R1/R2) & OVER-CORRECTION GUARD (two-path f=0.45 dilutes x_in -> single_plug flips > 400!)
        q_mode="cos", q_hi=650.0, q_drop=370.0, q_tc=1.5, q_tw=2.5,
        b_alpha=0.260, b_beta=20.0, b_sd=0.046, b_lam=2.10,
        v_nom=1160.0, f_fast=0.45, v_fast=420.0, v_main=1360.0, x_sd=1.60, x_mu=-0.28, y_mu=0.02, rho_fast=0.00, rho_main=0.95,
        pi_fbio=0.025, pi_fmin=0.015, pi_struct=0.0065, c_alk=0.75, c_acid=0.78,
    ),
    "TR06": dict(  # S3 OVER-CORRECTION GUARD (high persistent structural fault pi_struct=0.049 -> uninverted raw D3 drops < 400!)
        q_mode="cos", q_hi=630.0, q_drop=350.0, q_tc=2.2, q_tw=2.5,
        b_alpha=0.265, b_beta=18.0, b_sd=0.044, b_lam=2.50,
        v_nom=1240.0, f_fast=0.30, v_fast=390.0, v_main=960.0, x_sd=1.00, x_mu=-0.24, y_mu=-0.24, rho_fast=0.20, rho_main=0.55,
        pi_fbio=0.025, pi_fmin=0.020, pi_struct=0.0490, c_alk=0.75, c_acid=0.78,
    ),
    "TR07": dict(  # HIGH-AGING TEXTURE TRAIN (forced OVERHAUL on every route, moved outside band by every stump)
        q_mode="trough", q_hi=590.0, q_drop=410.0, q_tc=3.5, q_tw=2.25,
        b_alpha=0.205, b_beta=54.0, b_sd=0.068, b_lam=0.88,
        v_nom=1420.0, f_fast=0.44, v_fast=420.0, v_main=1360.0, x_sd=0.60, x_mu=1.12, y_mu=0.14, rho_fast=0.96, rho_main=0.00,
        pi_fbio=0.140, pi_fmin=0.135, pi_struct=0.0280, c_alk=0.75, c_acid=0.78,
    ),
    "TR08": dict(  # NEWER LOW-BURDEN TEXTURE TRAIN (forced MONITOR on every route)
        q_mode="cos", q_hi=610.0, q_drop=320.0, q_tc=2.0, q_tw=2.5,
        b_alpha=0.255, b_beta=14.0, b_sd=0.042, b_lam=2.80,
        v_nom=1120.0, f_fast=0.24, v_fast=360.0, v_main=900.0, x_sd=1.00, x_mu=-0.26, y_mu=-0.26, rho_fast=0.15, rho_main=0.50,
        pi_fbio=0.020, pi_fmin=0.015, pi_struct=0.0060, c_alk=0.75, c_acid=0.78,
    ),
}

# S3 true emission probabilities across 3 inline shift alarm channels:
#   D1 = salt_passage_alarm, D2 = stage_dp_alarm, D3 = acoustic_bypass_alarm
P_CLEAN = (0.014, 0.015, 0.008)
P_FBIO = (0.78, 0.88, 0.015)   # Organic biofilm: high D1 & D2, quiet D3; cleared ~75% by CIP_ALK
P_FMIN = (0.28, 0.90, 0.52)    # Mineral crust: high D2 + acoustic chatter D3, low D1; cleared ~78% by CIP_ACID
P_STRUCT = (0.90, 0.14, 0.48)  # Mechanical O-ring/seal breach: high D1 & moderate D3, low D2; invariant across BOTH CIPs

BITS = [((b >> 2) & 1, (b >> 1) & 1, b & 1) for b in range(8)]
D3_MASK = [b & 1 for b in range(8)]


def _indep_dist(p):
    out = []
    for d1, d2, d3 in BITS:
        v = (p[0] if d1 else 1.0 - p[0]) * (p[1] if d2 else 1.0 - p[1]) * (p[2] if d3 else 1.0 - p[2])
        out.append(v)
    return out


def _norm_sf(z):
    return 0.5 * math.erfc(z / math.sqrt(2.0))


def _q_of_hour(h):
    if h < Q_STARTS_H[1]:
        return 0
    if h < Q_STARTS_H[2]:
        return 1
    if h < Q_STARTS_H[3]:
        return 2
    return 3


def _ar1_fg(phi, m):
    if phi <= 1e-9:
        return 1.0 / m, 0.0
    if phi >= 1.0 - 1e-9:
        return 1.0, 1.0
    s = 0.0
    pk = phi
    for d in range(1, m):
        s += (m - d) * pk
        pk *= phi
    F = (m + 2.0 * s) / (m * m)
    g = (1.0 - phi ** m) / (1.0 - phi)
    G = phi * g * g / (m * m)
    return F, G


def _ou_fg(lam, m):
    """Continuous-time OU composite ratios normalized to 1-hour operating-block variance (Clause 2.1)."""
    def _f_raw(k):
        x = k / max(lam, 1e-6)
        if x < 1e-5:
            return 1.0, 1.0
        em = math.exp(-x)
        return 2.0 * (x - 1.0 + em) / (x * x), ((1.0 - em) ** 2) / (x * x)

    f1, _ = _f_raw(1.0)
    fm, gm = _f_raw(float(m))
    return fm / max(f1, 1e-9), gm / max(f1, 1e-9)


def _sample_cat(rng, probs):
    u = rng.random()
    acc = 0.0
    for i, p in enumerate(probs):
        acc += p
        if u <= acc:
            return i
    return len(probs) - 1


def interp_monotone(xs_query, xs_grid, ys_grid):
    """Piecewise-linear interpolation on strictly increasing xs_grid (clamped at ends)."""
    n = len(xs_grid)
    x0 = xs_grid[0]
    xn = xs_grid[-1]
    y0 = ys_grid[0]
    yn = ys_grid[-1]
    out = [0.0] * len(xs_query)
    j = 0
    for idx, xq in enumerate(xs_query):
        if xq <= x0:
            out[idx] = y0
            continue
        if xq >= xn:
            out[idx] = yn
            continue
        while j + 1 < n and xs_grid[j + 1] < xq:
            j += 1
        while j > 0 and xs_grid[j] > xq:
            j -= 1
        xa = xs_grid[j]
        xb = xs_grid[j + 1]
        w = (xq - xa) / (xb - xa)
        out[idx] = ys_grid[j] + w * (ys_grid[j + 1] - ys_grid[j])
    return out


def _solve_linear_system(A, b):
    """Gaussian elimination with partial pivoting for small dense systems."""
    n = len(b)
    M = [list(A[i]) + [b[i]] for i in range(n)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(M[r][col]))
        if abs(M[piv][col]) < 1e-12:
            return [0.0] * n
        M[col], M[piv] = M[piv], M[col]
        d = M[col][col]
        for j in range(col, n + 1):
            M[col][j] /= d
        for r in range(n):
            if r == col:
                continue
            f = M[r][col]
            if f != 0.0:
                for j in range(col, n + 1):
                    M[r][j] -= f * M[col][j]
    return [M[i][n] for i in range(n)]


def simulate_world(seed=SEED):
    """Simulate full 2026 physical processes for all 8 SWRO trains."""
    rng = random.Random(seed)
    n_h = 8760
    n_15 = n_h * 4
    n_sh = n_h // 4
    season_b = [-0.014, 0.002, 0.024, -0.006]
    season_s = [-0.14, 0.02, 0.24, -0.04]

    e_clean = _indep_dist(P_CLEAN)
    e_fbio = _indep_dist(P_FBIO)
    e_fmin = _indep_dist(P_FMIN)
    e_struct = _indep_dist(P_STRUCT)

    # Common coastal seawater salinity/conductivity front on 15-min grid
    cond_base = [0.0] * n_15
    c_slow = 0.0
    c_med = 0.0
    c_fast = 0.0
    for i in range(n_15):
        t_h = i * 0.25
        c_slow = 0.992 * c_slow + 0.14 * rng.gauss(0.0, 1.0)
        c_med = 0.905 * c_med + 0.65 * rng.gauss(0.0, 1.0)
        c_fast = 0.60 * c_fast + 0.72 * rng.gauss(0.0, 1.0)
        tidal = 0.75 * math.sin(2.0 * math.pi * t_h / 12.42) + 0.45 * math.cos(2.0 * math.pi * t_h / 24.84)
        cond_base[i] = 52.0 + tidal + c_slow + c_med + c_fast

    trains_data = {}
    for ui, u in enumerate(TRAINS):
        p = WORLD[u]

        # 1. Realistic smooth diurnal solar-aligned feed flow Q_h (no flat clamp!)
        q_flow_h = [0.0] * n_h
        u_f = 0.0
        q_mode = p["q_mode"]
        q_hi = p["q_hi"]
        q_drop = p["q_drop"]
        q_tc = p["q_tc"]
        q_tw = p["q_tw"]
        for h in range(n_h):
            hod = h % 24
            doy = h // 24
            u_f = 0.80 * u_f + 12.0 * rng.gauss(0.0, 1.0)
            seas = 20.0 * math.cos(2.0 * math.pi * (doy - 210.0) / 365.0)
            if q_mode == "trough":
                dh = ((hod - q_tc + 12.0) % 24.0) - 12.0
                trough = q_drop * math.exp(-0.5 * (dh / q_tw) ** 2)
                q_raw = q_hi - trough + seas + u_f + rng.gauss(0.0, 6.0)
            else:
                q_raw = (
                    q_hi
                    - q_drop * 0.5 * (1.0 + math.cos(2.0 * math.pi * (hod - q_tc) / 24.0))
                    + seas
                    + u_f
                    + rng.gauss(0.0, 8.0)
                )
            q_flow_h[h] = max(155.0, min(840.0, q_raw))

        # 2. S1: Hourly permeate boron C_t = b_alpha + s_q + b_beta / Q_t + eps_t
        phi_b = math.exp(-1.0 / p["b_lam"])
        s_in = p["b_sd"] * math.sqrt(max(1e-12, 1.0 - phi_b * phi_b))
        eps_b = rng.gauss(0.0, p["b_sd"])
        b_1h = [0.0] * n_h
        truth_boron_q = [0.0, 0.0, 0.0, 0.0]
        for h in range(n_h):
            q = _q_of_hour(h)
            eps_b = phi_b * eps_b + s_in * rng.gauss(0.0, 1.0)
            val = p["b_alpha"] + season_b[q] + p["b_beta"] / q_flow_h[h] + eps_b
            b_1h[h] = val
            if val > BORON_LIMIT:
                truth_boron_q[q] += 1.0

        # Flow-proportional 4h (Thu-Mon) and 8h (Tue-Wed) composite lab bottles
        # 2026-01-01 is Thursday (dow=3)
        comp_day = []
        comp_m = []
        comp_q = []
        comp_slot = []
        comp_val = []
        comp_qbar = []
        for day in range(365):
            dow = (3 + day) % 7
            m = 8 if dow in (1, 2) else 4
            n_slots = 24 // m
            q_idx = _q_of_hour(day * 24)
            for s in range(n_slots):
                h0 = day * 24 + s * m
                wsum = 0.0
                vsum = 0.0
                for h in range(h0, h0 + m):
                    w = q_flow_h[h]
                    wsum += w
                    vsum += w * b_1h[h]
                obs = vsum / wsum + rng.gauss(0.0, 0.004)
                comp_day.append(day)
                comp_m.append(m)
                comp_q.append(q_idx)
                comp_slot.append(s + 1)
                comp_val.append(obs)
                comp_qbar.append(wsum / m)

        # 3. S2: 15-min cumulative volume Phi(t) + two-path DAF/DMF short-circuit hydraulics
        q_15 = [0.0] * n_15
        phi_15 = [0.0] * n_15
        acc = 0.0
        for i in range(n_15):
            hf = i * 0.25
            h0 = int(hf)
            w = hf - h0
            h1 = h0 + 1 if h0 + 1 < n_h else n_h - 1
            qv = q_flow_h[h0] * (1.0 - w) + q_flow_h[h1] * w
            q_15[i] = qv
            acc += qv * 0.25
            phi_15[i] = acc

        # Intake conductivity & standardized algal-TEP precursor x_in on volume grid
        c_in_15 = [0.0] * n_15
        x_in_15 = [0.0] * n_15
        c_loc = 0.0
        x_st = 0.0
        x_sd = p["x_sd"]
        x_mu = p["x_mu"]
        y_mu = p["y_mu"]
        for i in range(n_15):
            dv = q_15[i] * 0.25
            a_c = math.exp(-dv / 260.0)
            c_loc = a_c * c_loc + math.sqrt(max(1e-12, 1.0 - a_c * a_c)) * 0.72 * rng.gauss(0.0, 1.0)
            c_in_15[i] = cond_base[i] + c_loc

            a_x = math.exp(-dv / 110.0)
            x_st = a_x * x_st + math.sqrt(max(1e-12, 1.0 - a_x * a_x)) * rng.gauss(0.0, 1.0)
            q_idx = _q_of_hour(i // 4)
            # Mild seasonal algal bloom baseline
            x_in_15[i] = x_mu + 0.35 * season_s[q_idx] + x_sd * x_st

        # True two-path arrival at RO feed header
        f_fast = p["f_fast"]
        v_fast = p["v_fast"]
        v_main = p["v_main"]
        xq_fast = [phi_15[i] - v_fast for i in range(n_15)]
        xq_main = [phi_15[i] - v_main for i in range(n_15)]
        c_fast_al = interp_monotone(xq_fast, phi_15, c_in_15)
        c_main_al = interp_monotone(xq_main, phi_15, c_in_15)
        x_fast_al = interp_monotone(xq_fast, phi_15, x_in_15)
        x_main_al = interp_monotone(xq_main, phi_15, x_in_15)

        # Normalize fast/main standardized anomalies for clean y_out coupling
        r_f = p["rho_fast"]
        r_m = p["rho_main"]
        r_rem = math.sqrt(max(0.04, 1.0 - r_f * r_f - r_m * r_m))
        c_out_15 = [0.0] * n_15
        y_out_15 = [0.0] * n_15
        truth_scaling_q = [0.0, 0.0, 0.0, 0.0]
        y_ind = 0.0
        for i in range(n_15):
            q_idx = _q_of_hour(i // 4)
            c_mix = f_fast * c_fast_al[i] + (1.0 - f_fast) * c_main_al[i]
            c_out_15[i] = c_mix + rng.gauss(0.0, 0.34)

            x_arr = f_fast * x_fast_al[i] + (1.0 - f_fast) * x_main_al[i]
            zf = (x_fast_al[i] - (x_mu + 0.35 * season_s[q_idx])) / x_sd
            zm = (x_main_al[i] - (x_mu + 0.35 * season_s[q_idx])) / x_sd
            y_ind = 0.72 * y_ind + math.sqrt(1.0 - 0.72 * 0.72) * rng.gauss(0.0, 1.0)
            yv = y_mu + 0.75 * season_s[q_idx] + r_f * zf + r_m * zm + r_rem * y_ind
            y_out_15[i] = yv
            if i >= 32 and x_arr > SCALING_X_LIM and yv > SCALING_Y_LIM:
                truth_scaling_q[q_idx] += 0.25

        # 4. S3: 4-hour shift alarms + Dual-Recipe CIP schedule (CIP_ALK_pH11 vs CIP_ACID_pH2)
        # Schedule ~22 CIP washes per train across the year (approx 60% ALK, 40% ACID, spaced 14-18 days)
        cip_events = []  # list of (block_idx, recipe_str)
        b_cur = 50 + (ui * 11) % 35
        wash_idx = 0
        while b_cur < n_sh - 35:
            # Mix ALK and ACID: ~60% ALK, ~40% ACID (alternating pattern A, A, C, A, C, ...)
            recipe = "CIP_ACID_pH2" if (wash_idx % 5 in (2, 4)) else "CIP_ALK_pH11"
            cip_events.append((b_cur, recipe))
            wash_idx += 1
            b_cur += rng.randint(84, 108)  # 14 to 18 days

        # Regime per 4h block: 0 = Pre-CIP baseline, 1 = Post-CIP_ALK (<120h), 2 = Post-CIP_ACID (<120h)
        # Because washes are >= 84 blocks (336h) apart, 30-block (120h) windows never overlap!
        regime_sh = [0] * n_sh
        for cb, rec in cip_events:
            code = 1 if rec == "CIP_ALK_pH11" else 2
            for k in range(cb, min(n_sh, cb + 30)):
                regime_sh[k] = code

        pat_sh = [0] * n_sh
        truth_struct_q = [0.0, 0.0, 0.0, 0.0]
        cnt_reg = [[0] * 8 for _ in range(3)]  # 3 regimes x 8 alarm triples
        pi_s = p["pi_struct"]
        for b in range(n_sh):
            reg = regime_sh[b]
            pf_bio = p["pi_fbio"] * (1.0 - p["c_alk"]) if reg == 1 else p["pi_fbio"]
            pf_min = p["pi_fmin"] * (1.0 - p["c_acid"]) if reg == 2 else p["pi_fmin"]
            p0 = max(0.01, 1.0 - pf_bio - pf_min - pi_s)
            st = _sample_cat(rng, [p0, pf_bio, pf_min, pi_s])
            if st == 0:
                pat = _sample_cat(rng, e_clean)
            elif st == 1:
                pat = _sample_cat(rng, e_fbio)
            elif st == 2:
                pat = _sample_cat(rng, e_fmin)
            else:
                pat = _sample_cat(rng, e_struct)
                truth_struct_q[_q_of_hour(b * 4)] += 4.0
            pat_sh[b] = pat
            cnt_reg[reg][pat] += 1

        trains_data[u] = {
            "v_nom": p["v_nom"],
            "f_fast_true": f_fast,
            "v_fast_true": v_fast,
            "v_main_true": v_main,
            "q_flow_h": q_flow_h,
            "comp_day": comp_day,
            "comp_m": comp_m,
            "comp_q": comp_q,
            "comp_slot": comp_slot,
            "comp_val": comp_val,
            "comp_qbar": comp_qbar,
            "c_in_15": c_in_15,
            "x_in_15": x_in_15,
            "c_out_15": c_out_15,
            "y_out_15": y_out_15,
            "cip_events": cip_events,
            "regime_sh": regime_sh,
            "pat_sh": pat_sh,
            "cnt_reg": cnt_reg,
            "truth_boron_q": truth_boron_q,
            "truth_scaling_q": truth_scaling_q,
            "truth_struct_q": truth_struct_q,
        }

    return {"trains": trains_data}


# ==============================================================================
# S1 ESTIMATORS (Boron: Flow-Coupled Solution-Diffusion + Composite Deconvolution)
# ==============================================================================
def _comp_moments(res, comp_m, comp_day, lab_var=0.004 ** 2, trim_frac=0.0):
    stats = {}
    for m in (4, 8):
        idxs = [i for i, cm in enumerate(comp_m) if cm == m]
        vals = [res[i] for i in idxs]
        if trim_frac > 0.0:
            sv = sorted(vals)
            k = max(1, int(len(sv) * trim_frac))
            lo, hi = sv[k], sv[-k - 1]
            vals_v = [v for v in vals if lo <= v <= hi]
        else:
            vals_v = vals
        nv = len(vals_v)
        mv = sum(vals_v) / nv
        vm = sum((v - mv) ** 2 for v in vals_v) / max(1, nv - 1)
        pa, pb = [], []
        for k in range(len(idxs) - 1):
            i1, i2 = idxs[k], idxs[k + 1]
            if i2 == i1 + 1 and (comp_day[i2] - comp_day[i1]) <= 1:
                pa.append(res[i1])
                pb.append(res[i2])
        np_ = len(pa)
        ma = sum(pa) / np_
        mb = sum(pb) / np_
        cm = sum((pa[k] - ma) * (pb[k] - mb) for k in range(np_)) / np_
        stats[m] = (max(1e-7, vm - lab_var), max(0.0, cm))
    return stats


def _fit_ar1_moments(v4, c4, v8, c8, kernel="ar1", obj="wls", use_8h=True):
    lam_grid = [0.25 * ((30.0 / 0.25) ** (k / 199.0)) for k in range(200)]
    best_loss = 1e18
    best = (2.0, math.sqrt(max(v4, 1e-6)), 0.7, 0.5)
    obs = [v4, c4, v8, c8] if use_8h else [v4, c4]
    if obj == "wls":
        wts = [3.0 / (v4 * v4), 3.0 / (v4 * v4), 1.0 / (v8 * v8), 0.7 / (v8 * v8)] if use_8h else [1.0 / (v4 * v4), 1.0 / (v4 * v4)]
    elif obj == "ols":
        wts = [1.0, 1.0, 1.0, 1.0] if use_8h else [1.0, 1.0]
    else:  # lag1_only
        wts = [1.0 / (v4 * v4), 5.0 / (v4 * v4), 0.2 / (v8 * v8), 0.5 / (v8 * v8)] if use_8h else [1.0 / (v4 * v4), 5.0 / (v4 * v4)]

    for lam in lam_grid:
        if kernel == "ar1":
            phi = math.exp(-1.0 / lam)
            F4, G4 = _ar1_fg(phi, 4)
            F8, G8 = _ar1_fg(phi, 8)
        else:
            F4, G4 = _ou_fg(lam, 4)
            F8, G8 = _ou_fg(lam, 8)
        mod = [F4, G4, F8, G8] if use_8h else [F4, G4]
        num = sum(w * o * m for w, o, m in zip(wts, obs, mod))
        den = sum(w * m * m for w, m in zip(wts, mod))
        s2 = max(1e-9, num / max(den, 1e-12))
        loss = sum(w * (o - s2 * m) ** 2 for w, o, m in zip(wts, obs, mod))
        if loss < best_loss:
            best_loss = loss
            best = (lam, math.sqrt(s2), F8 / max(F4, 1e-9), G4 / max(F4, 1e-9))
    return best


def _fit_flux_ols(comp_val, comp_q, comp_qbar, weights=None, robust=False):
    """Fit C_comp = alpha_0..3 + beta * (1 / Q_bar) by WLS/OLS (or Huber IRLS)."""
    n = len(comp_val)
    invq = [1.0 / q for q in comp_qbar]
    w = [1.0] * n if weights is None else list(weights)
    iters = 6 if robust else 1
    coef = [0.3, 0.3, 0.3, 0.3, 20.0]
    for _ in range(iters):
        A = [[0.0] * 5 for _ in range(5)]
        b = [0.0] * 5
        for i in range(n):
            wi = w[i]
            qi = comp_q[i]
            xi = invq[i]
            yi = comp_val[i]
            A[qi][qi] += wi
            A[qi][4] += wi * xi
            A[4][qi] += wi * xi
            A[4][4] += wi * xi * xi
            b[qi] += wi * yi
            b[4] += wi * xi * yi
        coef = _solve_linear_system(A, b)
        if robust:
            res = [comp_val[i] - (coef[comp_q[i]] + coef[4] * invq[i]) for i in range(n)]
            med = sorted(abs(r) for r in res)[n // 2]
            delta = max(0.015, 1.345 * 1.4826 * med)
            w = [1.0 if abs(r) <= delta else delta / abs(r) for r in res]
    alphas = coef[:4]
    beta = max(0.0, coef[4])
    res = [comp_val[i] - (alphas[comp_q[i]] + beta * invq[i]) for i in range(n)]
    return alphas, beta, res


def estimate_s1(
    data,
    mode="golden",
    kernel="ar1",
    obj="wls",
    trim_frac=0.0,
    lab_noise=True,
    use_8h=True,
    flux_fit="ols",
):
    """Estimate 2026 quarterly boron excursion hours (> 0.50 mg/L on 1h support) per train."""
    lab_var = (0.004 ** 2) if lab_noise else 0.0
    out = {}

    for u in TRAINS:
        td = data["trains"][u]
        cv = td["comp_val"]
        cq = td["comp_q"]
        cm = td["comp_m"]
        cd = td["comp_day"]
        qb = td["comp_qbar"]
        qh_flow = td["q_flow_h"]

        # Observed 1/Q_bar slope (used in F1 falsification check!)
        obs_alphas, obs_beta, obs_res = _fit_flux_ols(cv, cq, qb)
        obs_st = _comp_moments(obs_res, cm, cd, lab_var=lab_var, trim_frac=0.0)
        obs_v8_v4 = obs_st[8][0] / max(obs_st[4][0], 1e-9)
        obs_r1_4 = obs_st[4][1] / max(obs_st[4][0], 1e-9)

        # Stationary quarterly means (ignoring beta/Q_t)
        q_mu = []
        for q in range(4):
            vs = [cv[i] for i in range(len(cv)) if cq[i] == q]
            q_mu.append(sum(vs) / len(vs))
        stat_res = [cv[i] - q_mu[cq[i]] for i in range(len(cv))]
        stat_st = _comp_moments(stat_res, cm, cd, lab_var=lab_var, trim_frac=trim_frac)

        if mode == "hurried":
            # Raw composite exceedance fraction
            qh_out = []
            for q in range(4):
                vs = [cv[i] for i in range(len(cv)) if cq[i] == q]
                qh_out.append((sum(1 for v in vs if v > BORON_LIMIT) / len(vs)) * Q_HOURS[q])
            out[u] = dict(
                q=qh_out, beta_hat=0.0, beta_obs=obs_beta, sd1=math.sqrt(stat_st[4][0]),
                lam=99.0, v8_v4_pred=1.0, r1_4_pred=1.0, v8_v4_obs=obs_v8_v4, r1_4_obs=obs_r1_4,
            )

        elif mode == "cutoff_4h":
            qh_out = []
            for q in range(4):
                vs = [cv[i] for i in range(len(cv)) if cq[i] == q and cm[i] == 4]
                qh_out.append((sum(1 for v in vs if v > BORON_LIMIT) / len(vs)) * Q_HOURS[q])
            out[u] = dict(
                q=qh_out, beta_hat=0.0, beta_obs=obs_beta, sd1=math.sqrt(stat_st[4][0]),
                lam=99.0, v8_v4_pred=1.0, r1_4_pred=1.0, v8_v4_obs=obs_v8_v4, r1_4_obs=obs_r1_4,
            )

        elif mode == "rigorous_stat_ar1":
            # RESPONSE 1 & RESPONSE 2 EXACT ROUND-1 SOLVER:
            # Per-train stationary Gaussian AR(1) composite deconvolution WITHOUT beta/Q_t coupling!
            lam, sd1, v8v4_p, r14_p = _fit_ar1_moments(
                stat_st[4][0], stat_st[4][1], stat_st[8][0], stat_st[8][1], kernel="ar1", obj="wls"
            )
            qh_out = [_norm_sf((BORON_LIMIT - q_mu[q]) / sd1) * Q_HOURS[q] for q in range(4)]
            out[u] = dict(
                q=qh_out, beta_hat=0.0, beta_obs=obs_beta, sd1=sd1, lam=lam,
                v8_v4_pred=v8v4_p, r1_4_pred=r14_p, v8_v4_obs=obs_v8_v4, r1_4_obs=obs_r1_4,
            )

        elif mode == "linear_q_no_deconv":
            # Regresses linearly on Q_bar (not 1/Q) and skips AR(1) support deconvolution
            n = len(cv)
            A = [[0.0] * 5 for _ in range(5)]
            b = [0.0] * 5
            for i in range(n):
                qi = cq[i]
                xi = qb[i]
                yi = cv[i]
                A[qi][qi] += 1.0
                A[qi][4] += xi
                A[4][qi] += xi
                A[4][4] += xi * xi
                b[qi] += yi
                b[4] += xi * yi
            cf = _solve_linear_system(A, b)
            res_l = [cv[i] - (cf[cq[i]] + cf[4] * qb[i]) for i in range(n)]
            sd_c = math.sqrt(max(1e-7, sum(r * r for r in res_l) / (n - 5)))
            qh_out = [0.0, 0.0, 0.0, 0.0]
            for h in range(8760):
                q = _q_of_hour(h)
                mu_h = cf[q] + cf[4] * qh_flow[h]
                qh_out[q] += _norm_sf((BORON_LIMIT - mu_h) / sd_c)
            out[u] = dict(
                q=qh_out, beta_hat=0.45 * obs_beta, beta_obs=obs_beta, sd1=sd_c, lam=99.0,
                v8_v4_pred=1.0, r1_4_pred=1.0, v8_v4_obs=obs_v8_v4, r1_4_obs=obs_r1_4,
            )

        elif mode == "flux_only_no_deconv":
            # Fits 1/Q_bar correctly, but uses raw composite residual SD instead of 1h deconvolution!
            alphas, beta, res = _fit_flux_ols(cv, cq, qb)
            st = _comp_moments(res, cm, cd, lab_var=lab_var)
            sd_c = math.sqrt(st[4][0])
            qh_out = [0.0, 0.0, 0.0, 0.0]
            for h in range(8760):
                q = _q_of_hour(h)
                mu_h = alphas[q] + beta / qh_flow[h]
                qh_out[q] += _norm_sf((BORON_LIMIT - mu_h) / sd_c)
            out[u] = dict(
                q=qh_out, beta_hat=beta, beta_obs=obs_beta, sd1=sd_c, lam=99.0,
                v8_v4_pred=1.0, r1_4_pred=1.0, v8_v4_obs=obs_v8_v4, r1_4_obs=obs_r1_4,
            )

        elif mode == "over_iid":
            # Over-correction: i.i.d. sqrt(m) inflation on stationary composite variance (ignoring flux + autocorrelation)
            sd1 = math.sqrt(4.0 * stat_st[4][0])
            qh_out = [_norm_sf((BORON_LIMIT - q_mu[q]) / sd1) * Q_HOURS[q] for q in range(4)]
            out[u] = dict(
                q=qh_out, beta_hat=0.0, beta_obs=obs_beta, sd1=sd1, lam=0.01,
                v8_v4_pred=0.5, r1_4_pred=0.0, v8_v4_obs=obs_v8_v4, r1_4_obs=obs_r1_4,
            )

        elif mode == "over_flux_iid":
            # Fits 1/Q_bar correctly, but over-corrects residual AR(1) by i.i.d. sqrt(4)
            alphas, beta, res = _fit_flux_ols(cv, cq, qb)
            st = _comp_moments(res, cm, cd, lab_var=lab_var)
            sd1 = math.sqrt(4.0 * st[4][0])
            qh_out = [0.0, 0.0, 0.0, 0.0]
            for h in range(8760):
                q = _q_of_hour(h)
                mu_h = alphas[q] + beta / qh_flow[h]
                qh_out[q] += _norm_sf((BORON_LIMIT - mu_h) / sd1)
            out[u] = dict(
                q=qh_out, beta_hat=beta, beta_obs=obs_beta, sd1=sd1, lam=0.01,
                v8_v4_pred=0.5, r1_4_pred=0.0, v8_v4_obs=obs_v8_v4, r1_4_obs=obs_r1_4,
            )

        else:  # golden (or honest variant)
            if flux_fit == "wls_span":
                wts = [1.0 if m == 4 else 1.4 for m in cm]
                alphas, beta, res = _fit_flux_ols(cv, cq, qb, weights=wts, robust=False)
            elif flux_fit == "huber":
                alphas, beta, res = _fit_flux_ols(cv, cq, qb, robust=True)
            else:
                alphas, beta, res = _fit_flux_ols(cv, cq, qb)
            st = _comp_moments(res, cm, cd, lab_var=lab_var, trim_frac=trim_frac)
            lam, sd1, v8v4_p, r14_p = _fit_ar1_moments(
                st[4][0], st[4][1], st[8][0], st[8][1], kernel=kernel, obj=obj, use_8h=use_8h
            )
            qh_out = [0.0, 0.0, 0.0, 0.0]
            for h in range(8760):
                q = _q_of_hour(h)
                mu_h = alphas[q] + beta / qh_flow[h]
                qh_out[q] += _norm_sf((BORON_LIMIT - mu_h) / sd1)
            out[u] = dict(
                q=qh_out, alphas=alphas, beta_hat=beta, beta_obs=obs_beta, sd1=sd1, lam=lam,
                v8_v4_pred=v8v4_p, r1_4_pred=r14_p, v8_v4_obs=obs_v8_v4, r1_4_obs=obs_r1_4,
            )
    return out


# ==============================================================================
# S2 ESTIMATORS (Scaling: Two-Path Bimodal Hydraulic Short-Circuiting)
# ==============================================================================
def _build_phi_hat(q_flow_h, flow_interp="linear"):
    n_h = len(q_flow_h)
    n_15 = n_h * 4
    q_15 = [0.0] * n_15
    phi = [0.0] * n_15
    acc = 0.0
    for i in range(n_15):
        hf = i * 0.25
        h0 = int(hf)
        w = hf - h0
        h1 = h0 + 1 if h0 + 1 < n_h else n_h - 1
        if flow_interp == "linear":
            qv = q_flow_h[h0] * (1.0 - w) + q_flow_h[h1] * w
        elif flow_interp == "step":
            qv = q_flow_h[h0]
        else:  # midpoint
            h_mid = min(n_h - 1, int(hf + 0.125))
            qv = q_flow_h[h_mid]
        q_15[i] = qv
        acc += qv * 0.25
        phi[i] = acc
    return phi, q_15


def _eval_loss(diff, loss_fn="l2"):
    if loss_fn == "l2":
        return sum(d * d for d in diff) / len(diff)
    if loss_fn == "l1":
        return sum(abs(d) for d in diff) / len(diff)
    if loss_fn == "huber":
        s = 0.0
        for d in diff:
            ad = abs(d)
            s += 0.5 * d * d if ad <= 0.8 else 0.8 * (ad - 0.4)
        return s / len(diff)
    # trimmed_l2 (2%)
    sq = sorted(d * d for d in diff)
    k = max(1, int(len(sq) * 0.02))
    sub = sq[:-k]
    return sum(sub) / len(sub)


def _profile_two_path(phi, c_in, c_out, loss_fn="l2"):
    """Profile-estimate (f_fast, V_fast, V_main) from conservative seawater conductivity."""
    n_15 = len(phi)
    # Subsample stride 16 for fast coarse 2D search
    idx_c = list(range(32, n_15, 16))
    co_c = [c_out[i] for i in idx_c]

    # Precompute shifted c_in on coarse grid
    v1_grid = list(range(160, 561, 30))
    v2_grid = list(range(760, 1521, 40))
    cache1 = {}
    for v1 in v1_grid:
        xq = [phi[i] - v1 for i in idx_c]
        cache1[v1] = interp_monotone(xq, phi, c_in)
    cache2 = {}
    for v2 in v2_grid:
        xq = [phi[i] - v2 for i in idx_c]
        cache2[v2] = interp_monotone(xq, phi, c_in)

    best_mse = 1e18
    best = (0.0, 400.0, 960.0)
    for v2 in v2_grid:
        c2 = cache2[v2]
        # Single-plug (f = 0) baseline at v2
        m0 = sum((co_c[k] - c2[k]) ** 2 for k in range(len(co_c))) / len(co_c)
        if m0 < best_mse:
            best_mse = m0
            best = (0.0, 400.0, float(v2))
        for v1 in v1_grid:
            c1 = cache1[v1]
            # Closed-form optimal f in [0, 0.49] minimizing sum((co - c2 - f*(c1 - c2))^2)
            num = 0.0
            den = 0.0
            for k in range(len(co_c)):
                dc = c1[k] - c2[k]
                num += (co_c[k] - c2[k]) * dc
                den += dc * dc
            f_hat = max(0.0, min(0.49, num / max(den, 1e-12)))
            mse = 0.0
            for k in range(len(co_c)):
                r = co_c[k] - (f_hat * c1[k] + (1.0 - f_hat) * c2[k])
                mse += r * r
            mse /= len(co_c)
            if mse < best_mse:
                best_mse = mse
                best = (f_hat, float(v1), float(v2))

    # Fine refinement on stride 6 around coarse optimum
    idx_f = list(range(32, n_15, 6))
    co_f = [c_out[i] for i in idx_f]
    f0, v10, v20 = best
    v1_fine = [v for v in range(max(120, int(v10) - 36), min(600, int(v10) + 37), 8)] if f0 > 0.05 else [400]
    v2_fine = [v for v in range(max(700, int(v20) - 48), min(1580, int(v20) + 49), 10)]
    c1_f = {v1: interp_monotone([phi[i] - v1 for i in idx_f], phi, c_in) for v1 in v1_fine}
    c2_f = {v2: interp_monotone([phi[i] - v2 for i in idx_f], phi, c_in) for v2 in v2_fine}

    best_loss = 1e18
    for v2 in v2_fine:
        c2 = c2_f[v2]
        for v1 in v1_fine:
            c1 = c1_f[v1]
            num = 0.0
            den = 0.0
            for k in range(len(co_f)):
                dc = c1[k] - c2[k]
                num += (co_f[k] - c2[k]) * dc
                den += dc * dc
            f_hat = max(0.0, min(0.49, num / max(den, 1e-12)))
            if f_hat < 0.04:
                f_hat = 0.0
            diff = [co_f[k] - (f_hat * c1[k] + (1.0 - f_hat) * c2[k]) for k in range(len(co_f))]
            lv = _eval_loss(diff, loss_fn)
            if lv < best_loss:
                best_loss = lv
                best = (f_hat, float(v1), float(v2))

    # Compute exact full-grid RMS at fitted (f_hat, v1_hat, v2_hat)
    f_hat, v1_hat, v2_hat = best
    c1_all = interp_monotone([p - v1_hat for p in phi], phi, c_in)
    c2_all = interp_monotone([p - v2_hat for p in phi], phi, c_in)
    rms = math.sqrt(
        sum((c_out[i] - (f_hat * c1_all[i] + (1.0 - f_hat) * c2_all[i])) ** 2 for i in range(32, n_15)) / (n_15 - 32)
    )
    return f_hat, v1_hat, v2_hat, rms


def _profile_single_plug(phi, c_in, c_out):
    """Response 1 & Response 2's exact Round-1 S2 solver: 1D single-plug V_eff scan!"""
    n_15 = len(phi)
    idx_c = list(range(32, n_15, 6))
    co_c = [c_out[i] for i in idx_c]
    best_mse = 1e18
    best_v = 900.0
    for vc in range(200, 1561, 20):
        ca = interp_monotone([phi[i] - vc for i in idx_c], phi, c_in)
        mse = sum((co_c[k] - ca[k]) ** 2 for k in range(len(co_c))) / len(co_c)
        if mse < best_mse:
            best_mse = mse
            best_v = float(vc)
    # Fine 5 m3 scan
    best_mse = 1e18
    v0 = best_v
    for vc in range(max(150, int(v0) - 25), min(1600, int(v0) + 26), 5):
        ca = interp_monotone([phi[i] - vc for i in idx_c], phi, c_in)
        mse = sum((co_c[k] - ca[k]) ** 2 for k in range(len(co_c))) / len(co_c)
        if mse < best_mse:
            best_mse = mse
            best_v = float(vc)
    ca_all = interp_monotone([p - best_v for p in phi], phi, c_in)
    rms = math.sqrt(sum((c_out[i] - ca_all[i]) ** 2 for i in range(32, n_15)) / (n_15 - 32))
    return best_v, rms


def estimate_s2(data, mode="golden", flow_interp="linear", loss_fn="l2"):
    """Estimate 2026 quarterly scaling excursion hours per train."""
    out = {}
    for u in TRAINS:
        td = data["trains"][u]
        c_in = td["c_in_15"]
        x_in = td["x_in_15"]
        c_out = td["c_out_15"]
        y_out = td["y_out_15"]
        n_15 = len(c_in)

        if mode == "hurried":
            qh = [0.0, 0.0, 0.0, 0.0]
            for i in range(32, n_15):
                if x_in[i] > SCALING_X_LIM and y_out[i] > SCALING_Y_LIM:
                    qh[_q_of_hour(i // 4)] += 0.25
            rms = math.sqrt(sum((c_out[i] - c_in[i]) ** 2 for i in range(32, n_15)) / (n_15 - 32))
            out[u] = dict(q=qh, f_hat=0.0, v1_hat=0.0, v2_hat=0.0, c_rms=rms)

        elif mode == "fixed_lag":
            best_lag = 0
            best_mse = 1e18
            for lag in range(0, 29):
                mse = sum((c_out[i] - c_in[i - lag]) ** 2 for i in range(32, n_15, 6)) / ((n_15 - 32) / 6.0)
                if mse < best_mse:
                    best_mse = mse
                    best_lag = lag
            qh = [0.0, 0.0, 0.0, 0.0]
            for i in range(32, n_15):
                if x_in[i - best_lag] > SCALING_X_LIM and y_out[i] > SCALING_Y_LIM:
                    qh[_q_of_hour(i // 4)] += 0.25
            rms = math.sqrt(sum((c_out[i] - c_in[i - best_lag]) ** 2 for i in range(32, n_15)) / (n_15 - 32))
            out[u] = dict(q=qh, f_hat=0.0, v1_hat=0.0, v2_hat=float(best_lag * 115), c_rms=rms)

        elif mode == "single_plug":
            # RESPONSE 1 & RESPONSE 2'S EXACT ROUND-1 S2 SOLVER!
            phi, _ = _build_phi_hat(td["q_flow_h"], flow_interp)
            v_hat, rms = _profile_single_plug(phi, c_in, c_out)
            x_al = interp_monotone([p - v_hat for p in phi], phi, x_in)
            qh = [0.0, 0.0, 0.0, 0.0]
            for i in range(32, n_15):
                if x_al[i] > SCALING_X_LIM and y_out[i] > SCALING_Y_LIM:
                    qh[_q_of_hour(i // 4)] += 0.25
            out[u] = dict(q=qh, f_hat=0.0, v1_hat=0.0, v2_hat=v_hat, c_rms=rms)

        elif mode == "nom_vol":
            phi, _ = _build_phi_hat(td["q_flow_h"], "linear")
            vn = td["v_nom"]
            c_al = interp_monotone([p - vn for p in phi], phi, c_in)
            x_al = interp_monotone([p - vn for p in phi], phi, x_in)
            qh = [0.0, 0.0, 0.0, 0.0]
            for i in range(32, n_15):
                if x_al[i] > SCALING_X_LIM and y_out[i] > SCALING_Y_LIM:
                    qh[_q_of_hour(i // 4)] += 0.25
            rms = math.sqrt(sum((c_out[i] - c_al[i]) ** 2 for i in range(32, n_15)) / (n_15 - 32))
            out[u] = dict(q=qh, f_hat=0.0, v1_hat=0.0, v2_hat=vn, c_rms=rms)

        elif mode == "over_comonotonic":
            qh = [0.0, 0.0, 0.0, 0.0]
            for q in range(4):
                i0 = max(32, Q_STARTS_H[q] * 4)
                i1 = Q_STARTS_H[q + 1] * 4
                nx = sum(1 for i in range(i0, i1) if x_in[i] > SCALING_X_LIM)
                ny = sum(1 for i in range(i0, i1) if y_out[i] > SCALING_Y_LIM)
                qh[q] = min(nx, ny) * 0.25
            rms = math.sqrt(sum((c_out[i] - c_in[i]) ** 2 for i in range(32, n_15)) / (n_15 - 32))
            out[u] = dict(q=qh, f_hat=0.0, v1_hat=0.0, v2_hat=0.0, c_rms=rms)

        else:  # golden or honest two-path variant
            phi, _ = _build_phi_hat(td["q_flow_h"], flow_interp)
            f_hat, v1_hat, v2_hat, rms = _profile_two_path(phi, c_in, c_out, loss_fn=loss_fn)
            x1 = interp_monotone([p - v1_hat for p in phi], phi, x_in)
            x2 = interp_monotone([p - v2_hat for p in phi], phi, x_in)
            qh = [0.0, 0.0, 0.0, 0.0]
            for i in range(32, n_15):
                xa = f_hat * x1[i] + (1.0 - f_hat) * x2[i]
                if xa > SCALING_X_LIM and y_out[i] > SCALING_Y_LIM:
                    qh[_q_of_hour(i // 4)] += 0.25
            out[u] = dict(q=qh, f_hat=f_hat, v1_hat=v1_hat, v2_hat=v2_hat, c_rms=rms)
    return out


# ==============================================================================
# S3 ESTIMATORS (Structural Faults: 4-State Dual-Recipe CIP Invariance)
# ==============================================================================
def _build_regime_counts(data, post_blocks=30):
    """Build 8 trains x 3 regimes (Pre, Post-ALK, Post-ACID) x 8 alarm-triple count table."""
    cnt = {}
    for u in TRAINS:
        td = data["trains"][u]
        n_sh = len(td["pat_sh"])
        reg = [0] * n_sh
        for cb, rec in td["cip_events"]:
            code = 1 if rec == "CIP_ALK_pH11" else 2
            for k in range(cb, min(n_sh, cb + post_blocks)):
                reg[k] = code
        c_u = [[0] * 8 for _ in range(3)]
        for b, pat in enumerate(td["pat_sh"]):
            c_u[reg[b]][pat] += 1
        cnt[u] = c_u
    return cnt


def _obs_cip_drops(cnt):
    """Observed pre-to-post drops for (1,1,0) and (D3=1) separately after CIP_ALK vs CIP_ACID."""
    res = {}
    for u in TRAINS:
        c = cnt[u]
        s0 = max(1, sum(c[0]))
        s1 = max(1, sum(c[1]))
        s2 = max(1, sum(c[2]))
        p0 = [x / s0 for x in c[0]]
        p1 = [x / s1 for x in c[1]]
        p2 = [x / s2 for x in c[2]]
        d3_0 = sum(p0[b] * D3_MASK[b] for b in range(8))
        d3_1 = sum(p1[b] * D3_MASK[b] for b in range(8))
        d3_2 = sum(p2[b] * D3_MASK[b] for b in range(8))
        res[u] = dict(
            drop_110_alk=p0[6] - p1[6],
            drop_110_acid=p0[6] - p2[6],
            drop_d3_alk=d3_0 - d3_1,
            drop_d3_acid=d3_0 - d3_2,
        )
    return res


def _fit_4state_dual_cip_em(cnt, shared_clear=True, allow_cross_clear=False, n_iter=350):
    """4-state dual-recipe CIP-invariant EM across 192 multinomial cells (8 trains x 3 regimes x 8 patterns)."""
    p0 = [0.015, 0.015, 0.009]
    p_bio = [0.76, 0.86, 0.02]
    p_min = [0.28, 0.88, 0.50]
    p_str = [0.88, 0.16, 0.62]

    pi_bio = {u: 0.05 for u in TRAINS}
    pi_min = {u: 0.05 for u in TRAINS}
    pi_str = {u: 0.015 for u in TRAINS}
    # Retention ratios post-CIP (r_alk in [0.05, 0.60] for F_bio after ALK; r_acid in [0.05, 0.60] for F_min after ACID)
    r_bio_alk = {u: 0.25 for u in TRAINS}
    r_min_acid = {u: 0.22 for u in TRAINS}
    r_bio_acid = {u: 1.00 for u in TRAINS}
    r_min_alk = {u: 1.00 for u in TRAINS}

    n_reg = {u: [sum(cnt[u][rg]) for rg in range(3)] for u in TRAINS}

    for _ in range(n_iter):
        e = [_indep_dist(p0), _indep_dist(p_bio), _indep_dist(p_min), _indep_dist(p_str)]
        W = [[0.0] * 8 for _ in range(4)]

        # Sufficient statistics per train and regime
        w_st = {u: [[0.0] * 4 for _ in range(3)] for u in TRAINS}
        for u in TRAINS:
            for rg in range(3):
                fb = pi_bio[u] * (r_bio_alk[u] if rg == 1 else (r_bio_acid[u] if rg == 2 else 1.0))
                fm = pi_min[u] * (r_min_alk[u] if rg == 1 else (r_min_acid[u] if rg == 2 else 1.0))
                fs = pi_str[u]
                fc = max(1e-6, 1.0 - fb - fm - fs)
                pis = [fc, fb, fm, fs]
                for b in range(8):
                    c = cnt[u][rg][b]
                    if c == 0:
                        continue
                    probs = [pis[s] * e[s][b] for s in range(4)]
                    tot = sum(probs) + 1e-18
                    for s in range(4):
                        g = c * probs[s] / tot
                        W[s][b] += g
                        w_st[u][rg][s] += g

        # M-step: train prevalences and clearing ratios
        tot_bio_pre = tot_bio_alk = tot_min_pre = tot_min_acid = 0.0
        tot_n_pre = tot_n_alk = tot_n_acid = 0.0
        for u in TRAINS:
            n0, n1, n2 = n_reg[u]
            n_all = n0 + n1 + n2
            pi_str[u] = max(1e-4, min(0.45, (w_st[u][0][3] + w_st[u][1][3] + w_st[u][2][3]) / n_all))
            if not allow_cross_clear:
                pb_hat = max(1e-4, min(0.65, (w_st[u][0][1] + w_st[u][2][1]) / max(1, n0 + n2)))
                pm_hat = max(1e-4, min(0.65, (w_st[u][0][2] + w_st[u][1][2]) / max(1, n0 + n1)))
            else:
                pb_hat = max(1e-4, min(0.65, w_st[u][0][1] / max(1, n0)))
                pm_hat = max(1e-4, min(0.65, w_st[u][0][2] / max(1, n0)))
            pi_bio[u] = pb_hat
            pi_min[u] = pm_hat
            if not shared_clear:
                r_bio_alk[u] = max(0.05, min(0.65, (w_st[u][1][1] / max(1, n1)) / max(pb_hat, 1e-5)))
                r_min_acid[u] = max(0.05, min(0.65, (w_st[u][2][2] / max(1, n2)) / max(pm_hat, 1e-5)))
                if allow_cross_clear:
                    r_bio_acid[u] = max(0.65, min(1.00, (w_st[u][2][1] / max(1, n2)) / max(pb_hat, 1e-5)))
                    r_min_alk[u] = max(0.65, min(1.00, (w_st[u][1][2] / max(1, n1)) / max(pm_hat, 1e-5)))
            tot_bio_pre += w_st[u][0][1] + w_st[u][2][1]
            tot_bio_alk += w_st[u][1][1]
            tot_min_pre += w_st[u][0][2] + w_st[u][1][2]
            tot_min_acid += w_st[u][2][2]
            tot_n_pre += n0
            tot_n_alk += n1
            tot_n_acid += n2

        if shared_clear:
            rb_sh = max(0.05, min(0.65, (tot_bio_alk / max(1.0, tot_n_alk)) / max(tot_bio_pre / max(1.0, tot_n_pre + tot_n_acid), 1e-5)))
            rm_sh = max(0.05, min(0.65, (tot_min_acid / max(1.0, tot_n_acid)) / max(tot_min_pre / max(1.0, tot_n_pre + tot_n_alk), 1e-5)))
            for u in TRAINS:
                r_bio_alk[u] = rb_sh
                r_min_acid[u] = rm_sh

        # M-step: emissions
        def _upd(w_vec, lo, hi):
            sw = max(sum(w_vec), 1e-9)
            return [max(lo[k], min(hi[k], sum(w_vec[b] * BITS[b][k] for b in range(8)) / sw)) for k in range(3)]

        p0 = _upd(W[0], [0.002, 0.002, 0.002], [0.08, 0.08, 0.06])
        p_bio = _upd(W[1], [0.35, 0.45, 0.002], [0.98, 0.98, 0.12])
        p_min = _upd(W[2], [0.05, 0.50, 0.18], [0.65, 0.98, 0.85])
        p_str = _upd(W[3], [0.50, 0.02, 0.25], [0.99, 0.45, 0.95])

    # Compute predicted regime drops per train for F3 falsification check!
    e = [_indep_dist(p0), _indep_dist(p_bio), _indep_dist(p_min), _indep_dist(p_str)]
    preds = {}
    for u in TRAINS:
        ps = []
        for rg in range(3):
            fb = pi_bio[u] * (r_bio_alk[u] if rg == 1 else (r_bio_acid[u] if rg == 2 else 1.0))
            fm = pi_min[u] * (r_min_alk[u] if rg == 1 else (r_min_acid[u] if rg == 2 else 1.0))
            fs = pi_str[u]
            fc = max(1e-6, 1.0 - fb - fm - fs)
            pis = [fc, fb, fm, fs]
            dist = [sum(pis[s] * e[s][b] for s in range(4)) for b in range(8)]
            ps.append(dist)
        d3 = [sum(ps[rg][b] * D3_MASK[b] for b in range(8)) for rg in range(3)]
        preds[u] = dict(
            drop_110_alk=ps[0][6] - ps[1][6],
            drop_110_acid=ps[0][6] - ps[2][6],
            drop_d3_alk=d3[0] - d3[1],
            drop_d3_acid=d3[0] - d3[2],
        )
    return pi_str, pi_bio, pi_min, p0, p_bio, p_min, p_str, preds


def _fit_r1_pooled_cip_3state(cnt, n_iter=250):
    """RESPONSE 1'S EXACT ROUND-1 S3 SOLVER:
    Pools CIP_ALK + CIP_ACID identically into 1 post-CIP window and fits a 3-state
    (Clean / single Fouling with D3=0 / Persistent Structural) conditionally-independent EM!
    """
    p0 = [0.015, 0.015, 0.009]
    p1 = [0.80, 0.86, 0.00]
    p2 = [0.85, 0.55, 0.55]
    pi_f_pre = {u: 0.08 for u in TRAINS}
    pi_f_post = {u: 0.03 for u in TRAINS}
    pi_s = {u: 0.02 for u in TRAINS}

    cnt_pre = {u: cnt[u][0] for u in TRAINS}
    cnt_post = {u: [cnt[u][1][b] + cnt[u][2][b] for b in range(8)] for u in TRAINS}
    n_pre = {u: sum(cnt_pre[u]) for u in TRAINS}
    n_post = {u: sum(cnt_post[u]) for u in TRAINS}

    for _ in range(n_iter):
        e = [_indep_dist(p0), _indep_dist(p1), _indep_dist(p2)]
        W = [[0.0] * 8 for _ in range(3)]
        for u in TRAINS:
            w1_pr = w1_po = w2_all = 0.0
            for c_vec, pf, is_po in ((cnt_pre[u], pi_f_pre[u], False), (cnt_post[u], pi_f_post[u], True)):
                pc = max(1e-6, 1.0 - pf - pi_s[u])
                pis = [pc, pf, pi_s[u]]
                for b in range(8):
                    c = c_vec[b]
                    if c == 0:
                        continue
                    probs = [pis[s] * e[s][b] for s in range(3)]
                    tot = sum(probs) + 1e-18
                    for s in range(3):
                        g = c * probs[s] / tot
                        W[s][b] += g
                        if s == 1:
                            if is_po:
                                w1_po += g
                            else:
                                w1_pr += g
                        elif s == 2:
                            w2_all += g
            pi_s[u] = max(1e-4, min(0.50, w2_all / (n_pre[u] + n_post[u])))
            pi_f_pre[u] = max(1e-4, min(0.80, w1_pr / n_pre[u]))
            pi_f_post[u] = min(0.95 * pi_f_pre[u], max(1e-4, min(0.80, w1_po / n_post[u])))

        def _upd(wv, lo, hi):
            sw = max(sum(wv), 1e-9)
            return [max(lo[k], min(hi[k], sum(wv[b] * BITS[b][k] for b in range(8)) / sw)) for k in range(3)]

        p0 = _upd(W[0], [0.002, 0.002, 0.002], [0.10, 0.10, 0.08])
        p1 = _upd(W[1], [0.35, 0.45, 0.0], [0.98, 0.98, 0.001])  # Response 1's D3=0 fouling assumption!
        p2 = _upd(W[2], [0.25, 0.20, 0.15], [0.99, 0.98, 0.95])

    # Pooled-CIP model predicts IDENTICAL post-CIP drops for ALK and ACID, and ZERO D3 drop!
    e = [_indep_dist(p0), _indep_dist(p1), _indep_dist(p2)]
    preds = {}
    for u in TRAINS:
        d_pre = [
            max(1e-6, 1.0 - pi_f_pre[u] - pi_s[u]) * e[0][b] + pi_f_pre[u] * e[1][b] + pi_s[u] * e[2][b]
            for b in range(8)
        ]
        d_post = [
            max(1e-6, 1.0 - pi_f_post[u] - pi_s[u]) * e[0][b] + pi_f_post[u] * e[1][b] + pi_s[u] * e[2][b]
            for b in range(8)
        ]
        drop_110 = d_pre[6] - d_post[6]
        drop_d3 = sum((d_pre[b] - d_post[b]) * D3_MASK[b] for b in range(8))
        preds[u] = dict(drop_110_alk=drop_110, drop_110_acid=drop_110, drop_d3_alk=drop_d3, drop_d3_acid=drop_d3)
    return pi_s, p2, preds


def _fit_2class_ds(cnt_map, n_iter=200):
    """2-class conditional-independence Dawid-Skene EM (Response 2's Round-1 S3 solver!)."""
    p0 = [0.015, 0.015, 0.008]
    p1 = [0.78, 0.72, 0.25]
    pi = {u: 0.06 for u in TRAINS}
    for _ in range(n_iter):
        e0 = _indep_dist(p0)
        e1 = _indep_dist(p1)
        W0 = [0.0] * 8
        W1 = [0.0] * 8
        for u in TRAINS:
            w1_u = 0.0
            n_u = sum(cnt_map[u])
            for b in range(8):
                c = cnt_map[u][b]
                if c == 0:
                    continue
                a0 = (1.0 - pi[u]) * e0[b]
                a1 = pi[u] * e1[b]
                g1 = a1 / (a0 + a1 + 1e-18)
                W0[b] += c * (1.0 - g1)
                W1[b] += c * g1
                w1_u += c * g1
            pi[u] = max(1e-4, min(0.80, w1_u / max(1, n_u)))
        s0 = max(sum(W0), 1e-9)
        s1 = max(sum(W1), 1e-9)
        p0 = [max(0.002, min(0.15, sum(W0[b] * BITS[b][k] for b in range(8)) / s0)) for k in range(3)]
        p1 = [max(0.05, min(0.99, sum(W1[b] * BITS[b][k] for b in range(8)) / s1)) for k in range(3)]
    return pi, p1


def estimate_s3(data, mode="golden", post_blocks=30, shared_clear=True, allow_cross_clear=False):
    """Estimate 2026 quarterly persistent structural membrane fault hours per train."""
    cnt = _build_regime_counts(data, post_blocks=post_blocks)
    obs_drops = _obs_cip_drops(cnt)
    out = {}

    if mode == "hurried":
        # 2-of-3 shift majority vote
        for u in TRAINS:
            td = data["trains"][u]
            qh = [0.0, 0.0, 0.0, 0.0]
            for b, pat in enumerate(td["pat_sh"]):
                if pat in (3, 5, 6, 7):
                    qh[_q_of_hour(b * 4)] += 4.0
            out[u] = dict(
                q=qh, pi_s=sum(qh) / 8760.0,
                preds=dict(drop_110_alk=0.0, drop_110_acid=0.0, drop_d3_alk=0.0, drop_d3_acid=0.0),
                obs=obs_drops[u],
            )

    elif mode == "post_cip_mv":
        for u in TRAINS:
            c_po = [cnt[u][1][b] + cnt[u][2][b] for b in range(8)]
            rate = sum(c_po[b] for b in (3, 5, 6, 7)) / max(1, sum(c_po))
            out[u] = dict(
                q=[rate * Q_HOURS[q] for q in range(4)], pi_s=rate,
                preds=dict(drop_110_alk=0.0, drop_110_acid=0.0, drop_d3_alk=0.0, drop_d3_acid=0.0),
                obs=obs_drops[u],
            )

    elif mode == "post_cip_ds2":
        # RESPONSE 2'S EXACT ROUND-1 S3 SOLVER: 120h post-CIP 2-class Dawid-Skene!
        c_po = {u: [cnt[u][1][b] + cnt[u][2][b] for b in range(8)] for u in TRAINS}
        pi, p1 = _fit_2class_ds(c_po)
        for u in TRAINS:
            out[u] = dict(
                q=[pi[u] * Q_HOURS[q] for q in range(4)], pi_s=pi[u],
                preds=dict(drop_110_alk=0.0, drop_110_acid=0.0, drop_d3_alk=0.0, drop_d3_acid=0.0),
                obs=obs_drops[u],
            )

    elif mode == "ds2_all":
        c_all = {u: [cnt[u][0][b] + cnt[u][1][b] + cnt[u][2][b] for b in range(8)] for u in TRAINS}
        pi, p1 = _fit_2class_ds(c_all)
        for u in TRAINS:
            out[u] = dict(
                q=[pi[u] * Q_HOURS[q] for q in range(4)], pi_s=pi[u],
                preds=dict(drop_110_alk=0.0, drop_110_acid=0.0, drop_d3_alk=0.0, drop_d3_acid=0.0),
                obs=obs_drops[u],
            )

    elif mode == "r1_pooled_cip_3state":
        # RESPONSE 1'S EXACT ROUND-1 S3 SOLVER: 3-state pooled-CIP EM with D3=0 fouling!
        pi_s, p2, preds = _fit_r1_pooled_cip_3state(cnt)
        for u in TRAINS:
            out[u] = dict(q=[pi_s[u] * Q_HOURS[q] for q in range(4)], pi_s=pi_s[u], p2=p2, preds=preds[u], obs=obs_drops[u])

    elif mode == "over_raw_d3_post_acid":
        # Over-correction: uses baseline-subtracted raw D3 after CIP_ACID without sensitivity inversion (drops TR06 < 400!)
        d3_rates = {}
        for u in TRAINS:
            c2 = cnt[u][2]
            d3_rates[u] = sum(c2[b] * D3_MASK[b] for b in range(8)) / max(1, sum(c2))
        floor = min(d3_rates.values()) * 0.55
        for u in TRAINS:
            rate = max(0.0, d3_rates[u] - floor)
            out[u] = dict(
                q=[rate * Q_HOURS[q] for q in range(4)], pi_s=rate,
                preds=dict(drop_110_alk=0.0, drop_110_acid=0.0, drop_d3_alk=0.0, drop_d3_acid=0.0),
                obs=obs_drops[u],
            )

    elif mode == "unanimous":
        for u in TRAINS:
            td = data["trains"][u]
            qh = [0.0, 0.0, 0.0, 0.0]
            for b, pat in enumerate(td["pat_sh"]):
                if pat == 7:
                    qh[_q_of_hour(b * 4)] += 4.0
            out[u] = dict(
                q=qh, pi_s=sum(qh) / 8760.0,
                preds=dict(drop_110_alk=0.0, drop_110_acid=0.0, drop_d3_alk=0.0, drop_d3_acid=0.0),
                obs=obs_drops[u],
            )

    else:  # golden or honest 4-state dual-recipe variant
        pi_str, pi_bio, pi_min, p0, p_bio, p_min, p_str, preds = _fit_4state_dual_cip_em(
            cnt, shared_clear=shared_clear, allow_cross_clear=allow_cross_clear
        )
        for u in TRAINS:
            out[u] = dict(
                q=[pi_str[u] * Q_HOURS[q] for q in range(4)],
                pi_s=pi_str[u], pi_bio=pi_bio[u], pi_min=pi_min[u],
                p0=p0, p_bio=p_bio, p_min=p_min, p_str=p_str,
                preds=preds[u], obs=obs_drops[u],
            )
    return out


# ==============================================================================
# ASSEMBLY (2027 Operating Plan + Mode-Specific Excess Energy MWh)
# ==============================================================================
def assemble(r1, r2, r3, forward=True):
    members = {}
    c1_tot = c2_tot = c3_tot = 0.0
    q3_tot = 0.0
    energy_mwh_tot = 0.0
    per_train_energy = {}

    for u in TRAINS:
        sr = PLAN_SCHED_RATIO[u] if forward else [1.0, 1.0, 1.0, 1.0]
        bt = PLAN_BORON_TEMP_Q if forward else [1.0, 1.0, 1.0, 1.0]
        sc = PLAN_SCALING_REC_Q if forward else [1.0, 1.0, 1.0, 1.0]
        b27 = [r1[u]["q"][q] * bt[q] * sr[q] for q in range(4)]
        s27 = [r2[u]["q"][q] * sc[q] * sr[q] for q in range(4)]
        st27 = [r3[u]["q"][q] * sr[q] for q in range(4)]

        hb = sum(b27)
        hs = sum(s27)
        hst = sum(st27)
        members[u] = hb + hs + hst
        c1_tot += hb
        c2_tot += hs
        c3_tot += hst
        q3_tot += b27[2] + s27[2] + st27[2]
        em = (hb * ENERGY_BORON_KWH + hs * ENERGY_SCALING_KWH + hst * ENERGY_STRUCT_KWH) / 1000.0
        per_train_energy[u] = em
        energy_mwh_tot += em

    ov_set = [u for u in TRAINS if members[u] >= THRESHOLD]
    ov_hours = sum(members[u] for u in ov_set)
    ov_mwh = sum(per_train_energy[u] for u in ov_set)
    return {
        "members": members,
        "C1_boron_2027": c1_tot,
        "C2_scaling_2027": c2_tot,
        "C3_struct_2027": c3_tot,
        "A_total_2027": c1_tot + c2_tot + c3_tot,
        "A_overhaul_2027": ov_hours,
        "A_q3_2027": q3_tot,
        "A_energy_mwh": energy_mwh_tot,
        "A_overhaul_mwh": ov_mwh,
    }


def falsification_score(data, r1, r2, r3):
    """Native-unit physical conservation & chemical invariance checks (ZERO anomaly labels):
      F1: Solute-flux 1/Q_bar slope error + residual composite moment error (V8/V4 & r1(4))
      F2: Conservative seawater conductivity RMS across 280,320 intervals (mS/cm)
      F3: Stratified CIP_ALK vs CIP_ACID pattern-drop mismatch on (1,1,0) and D3=1 (pp)
    """
    f1_vals = []
    for u in TRAINS:
        beta_err = abs(r1[u]["beta_hat"] - r1[u]["beta_obs"]) / 50.0  # normalized to ~0.0-1.0
        mom_err = abs(r1[u]["v8_v4_pred"] - r1[u]["v8_v4_obs"]) + abs(r1[u]["r1_4_pred"] - r1[u]["r1_4_obs"])
        f1_vals.append(beta_err + mom_err)
    f1 = sum(f1_vals) / len(f1_vals)

    f2 = sum(r2[u]["c_rms"] for u in TRAINS) / len(TRAINS)

    # F3: fleet-mean absolute mismatch across all 4 recipe-stratified shifts (pp)
    f3_parts = []
    for key in ("drop_110_alk", "drop_110_acid", "drop_d3_alk", "drop_d3_acid"):
        err = abs(sum(r3[u]["preds"][key] - r3[u]["obs"][key] for u in TRAINS) / len(TRAINS))
        f3_parts.append(100.0 * err)
    f3 = sum(f3_parts)
    return f1, f2, f3


def build_spec(seed=SEED):
    data = simulate_world(seed)

    # Ground truth assembly
    truth_r1 = {u: {"q": data["trains"][u]["truth_boron_q"]} for u in TRAINS}
    truth_r2 = {u: {"q": data["trains"][u]["truth_scaling_q"]} for u in TRAINS}
    truth_r3 = {u: {"q": data["trains"][u]["truth_struct_q"]} for u in TRAINS}
    truth_asm = assemble(truth_r1, truth_r2, truth_r3)

    # Golden
    r1_g = estimate_s1(data, mode="golden")
    r2_g = estimate_s2(data, mode="golden")
    r3_g = estimate_s3(data, mode="golden")
    gold_asm = assemble(r1_g, r2_g, r3_g)

    # Hurried / Direct
    r1_h = estimate_s1(data, mode="hurried")
    r2_h = estimate_s2(data, mode="hurried")
    r3_h = estimate_s3(data, mode="hurried")

    # ROUND-1 FRONTIER SOLVERS AS PRICED RIGOROUS RIVALS!
    # Response 1 exact architecture: stationary AR(1) composite MLE + 1D single-plug V_eff + 3-state pooled-CIP D3=0 EM
    r1_stat = estimate_s1(data, mode="rigorous_stat_ar1")
    r2_sp = estimate_s2(data, mode="single_plug")
    r3_r1 = estimate_s3(data, mode="r1_pooled_cip_3state")
    rig_r1_asm = assemble(r1_stat, r2_sp, r3_r1)

    # Response 2 exact architecture: stationary AR(1) composite MLE + 1D single-plug V_eff + 120h post-CIP 2-class DS
    r3_r2 = estimate_s3(data, mode="post_cip_ds2")
    rig_r2_asm = assemble(r1_stat, r2_sp, r3_r2)

    # Over-corrections (strictly two-sided on all 3 stumps!)
    r1_over = estimate_s1(data, mode="over_iid")
    r2_over = estimate_s2(data, mode="over_comonotonic")
    r3_over = estimate_s3(data, mode="over_raw_d3_post_acid")
    over_s1 = assemble(r1_over, r2_g, r3_g)
    over_s2 = assemble(r1_g, r2_over, r3_g)
    over_s3 = assemble(r1_g, r2_g, r3_over)

    # Full 7-corner stump drop lattice (using direct/hurried drop; plus we test dropping to R1's textbook too!)
    lattice_asm = {
        "S1": assemble(r1_h, r2_g, r3_g),
        "S2": assemble(r1_g, r2_h, r3_g),
        "S3": assemble(r1_g, r2_g, r3_h),
        "S1+S2": assemble(r1_h, r2_h, r3_g),
        "S1+S3": assemble(r1_h, r2_g, r3_h),
        "S2+S3": assemble(r1_g, r2_h, r3_h),
        "S1+S2+S3": assemble(r1_h, r2_h, r3_h),
    }

    # 21 Honest Physical Estimator Variants (must ALL hold the exact 4-of-8 slate!)
    s1_vars = [
        estimate_s1(data, mode="golden", kernel="ou", obj="wls"),
        estimate_s1(data, mode="golden", kernel="ar1", obj="ols"),
        estimate_s1(data, mode="golden", kernel="ar1", obj="lag1"),
        estimate_s1(data, mode="golden", kernel="ar1", obj="wls", trim_frac=0.005),
        estimate_s1(data, mode="golden", kernel="ar1", obj="wls", lab_noise=False),
        estimate_s1(data, mode="golden", kernel="ar1", obj="wls", use_8h=False),
        estimate_s1(data, mode="golden", kernel="ar1", obj="wls", flux_fit="wls_span"),
        estimate_s1(data, mode="golden", kernel="ar1", obj="wls", flux_fit="huber"),
    ]
    s2_vars = [
        estimate_s2(data, mode="golden", flow_interp="step", loss_fn="l2"),
        estimate_s2(data, mode="golden", flow_interp="midpoint", loss_fn="l2"),
        estimate_s2(data, mode="golden", flow_interp="linear", loss_fn="l1"),
        estimate_s2(data, mode="golden", flow_interp="linear", loss_fn="huber"),
        estimate_s2(data, mode="golden", flow_interp="linear", loss_fn="trimmed_l2"),
    ]
    s3_vars = [
        estimate_s3(data, mode="golden", post_blocks=30, shared_clear=False),
        estimate_s3(data, mode="golden", post_blocks=30, shared_clear=True, allow_cross_clear=True),
        estimate_s3(data, mode="golden", post_blocks=24),  # 96h
        estimate_s3(data, mode="golden", post_blocks=36),  # 144h
        estimate_s3(data, mode="golden", post_blocks=31),  # <=120h inclusive
    ]
    variants = []
    for v1 in s1_vars:
        variants.append(assemble(v1, r2_g, r3_g))
    for v2 in s2_vars:
        variants.append(assemble(r1_g, v2, r3_g))
    for v3 in s3_vars:
        variants.append(assemble(r1_g, r2_g, v3))
    variants.append(assemble(s1_vars[0], s2_vars[1], s3_vars[0]))
    variants.append(assemble(s1_vars[7], s2_vars[3], s3_vars[2]))
    variants.append(assemble(s1_vars[3], s2_vars[4], s3_vars[3]))

    # Run routes & extra cutoff/hedge settings (including EVERY Round-1 frontier route!)
    gen_asm = assemble(r1_over, r2_over, r3_r2)
    r1_hedge = {u: {**r1_g[u], "q": [0.8 * r1_h[u]["q"][q] + 0.2 * r1_g[u]["q"][q] for q in range(4)], "beta_hat": 0.2 * r1_g[u]["beta_hat"]} for u in TRAINS}
    r2_hedge = {u: {**r2_g[u], "q": [0.8 * r2_h[u]["q"][q] + 0.2 * r2_g[u]["q"][q] for q in range(4)], "c_rms": 0.8 * r2_h[u]["c_rms"] + 0.2 * r2_g[u]["c_rms"]} for u in TRAINS}
    r3_hedge = {u: {**r3_g[u], "q": [0.8 * r3_h[u]["q"][q] + 0.2 * r3_g[u]["q"][q] for q in range(4)], "preds": {k: 0.2 * r3_g[u]["preds"][k] for k in r3_g[u]["preds"]}} for u in TRAINS}
    hedge_asm = assemble(r1_hedge, r2_hedge, r3_hedge)

    r1_c4 = estimate_s1(data, mode="cutoff_4h")
    r1_linq = estimate_s1(data, mode="linear_q_no_deconv")
    r1_fnd = estimate_s1(data, mode="flux_only_no_deconv")
    r1_fiid = estimate_s1(data, mode="over_flux_iid")
    r2_fl = estimate_s2(data, mode="fixed_lag")
    r2_nv = estimate_s2(data, mode="nom_vol")
    r3_cpmv = estimate_s3(data, mode="post_cip_mv")
    r3_ds2_all = estimate_s3(data, mode="ds2_all")
    r3_un = estimate_s3(data, mode="unanimous")

    cut_asm = assemble(r1_c4, r2_fl, r3_cpmv)

    extra_routes = {
        "cutoff:r1_round1_full": rig_r1_asm,
        "cutoff:r2_round1_full": rig_r2_asm,
        "cutoff:s1_stationary_ar1_mle": assemble(r1_stat, r2_g, r3_g),
        "cutoff:s1_4h_only": assemble(r1_c4, r2_g, r3_g),
        "cutoff:s1_linear_q_no_deconv": assemble(r1_linq, r2_g, r3_g),
        "cutoff:s1_flux_no_deconv": assemble(r1_fnd, r2_g, r3_g),
        "cutoff:s1_flux_iid_over": assemble(r1_fiid, r2_g, r3_g),
        "cutoff:s2_single_plug_veff": assemble(r1_g, r2_sp, r3_g),
        "cutoff:s2_fixed_lag": assemble(r1_g, r2_fl, r3_g),
        "cutoff:s2_nom_vol": assemble(r1_g, r2_nv, r3_g),
        "cutoff:s3_r1_pooled_cip_3state": assemble(r1_g, r2_g, r3_r1),
        "cutoff:s3_r2_post_cip_ds2": assemble(r1_g, r2_g, r3_r2),
        "cutoff:s3_post_cip_mv": assemble(r1_g, r2_g, r3_cpmv),
        "cutoff:s3_ds2_all": assemble(r1_g, r2_g, r3_ds2_all),
        "cutoff:s3_unanimous": assemble(r1_g, r2_g, r3_un),
        "hedge:history_2026_flat": assemble(r1_g, r2_g, r3_g, forward=False),
    }

    # Native-unit falsification floor
    f2_floor = 0.335

    def _comb_fal(x1, x2, x3):
        a, b, c = falsification_score(data, x1, x2, x3)
        return a * 10.0 + max(0.0, b - f2_floor) * 15.0 + c * 2.5, (a, b, c)

    fal_g, fal_g_parts = _comb_fal(r1_g, r2_g, r3_g)
    fal_rivals = {}
    fal_detail = {"golden": (fal_g, fal_g_parts)}
    for label, (x1, x2, x3) in [
        ("direct", (r1_h, r2_h, r3_h)),
        ("rigorous_r1", (r1_stat, r2_sp, r3_r1)),
        ("rigorous_r2", (r1_stat, r2_sp, r3_r2)),
        ("generous", (r1_over, r2_over, r3_r2)),
        ("hedge", (r1_hedge, r2_hedge, r3_hedge)),
        ("cutoff", (r1_c4, r2_fl, r3_cpmv)),
        ("S1_stat_ar1", (r1_stat, r2_g, r3_g)),
        ("S2_single_plug", (r1_g, r2_sp, r3_g)),
        ("S3_r1_pooled", (r1_g, r2_g, r3_r1)),
        ("S1_lost", (r1_h, r2_g, r3_g)),
        ("S2_lost", (r1_g, r2_h, r3_g)),
        ("S3_lost", (r1_g, r2_g, r3_h)),
        ("S1_over", (r1_over, r2_g, r3_g)),
        ("S2_over", (r1_g, r2_over, r3_g)),
        ("S3_over", (r1_g, r2_g, r3_over)),
    ]:
        sc, parts = _comb_fal(x1, x2, x3)
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
                "direct": lattice_asm["S1+S2+S3"]["members"][u],
                "rigorous": rig_r1_asm["members"][u],  # Response 1's EXACT 2.5-hour model!
            },
        }

    stumps_spec = {
        "S1": {
            "axis": "unit",
            "opens": "TR01",
            "said_out_loud": (
                "Permeate boron obeys solution-diffusion flux coupling (alpha + beta/Q_t) inside "
                "4h/8h flow-proportional composites, biasing stationary AR(1) MLE by Jensen AM/HM dilution."
            ),
            "steps_left": 4,
            "precedents": ["L22", "L56", "L57"],
            "sides": {"over": over_s1["members"]},
        },
        "S2": {
            "axis": "when",
            "opens": "TR02",
            "said_out_loud": (
                "Aging DAF/DMF basins split flow across a fast short-circuit bypass and a main "
                "baffled path, breaking 1D single-plug cumulative-volume conductivity alignment."
            ),
            "steps_left": 4,
            "precedents": ["L26", "L28", "N07", "N30"],
            "sides": {"over": over_s2["members"]},
        },
        "S3": {
            "axis": "what",
            "opens": "TR03",
            "said_out_loud": (
                "Alkaline CIP washes clear organic bio-fouling while acid CIP washes clear mineral "
                "crust that also triggers acoustic chatter D3; persistent structural faults survive both."
            ),
            "steps_left": 4,
            "precedents": ["L03", "L38", "L54", "N36"],
            "sides": {"over": over_s3["members"]},
        },
    }

    lattice_spec = {k: v["members"] for k, v in lattice_asm.items()}
    run_routes_spec = {
        "generous": gen_asm["members"],
        "calibrated": {
            "none": (
                "No shipped file observes 1-hour boron grab samples, true mixed-parcel scaling "
                "incidents, or destructive membrane autopsies; forcing rests on F1-F3 physical identities."
            )
        },
        "hedge": hedge_asm["members"],
        "cutoff": cut_asm["members"],
    }
    for k, v in extra_routes.items():
        run_routes_spec[k] = v["members"]

    def _non_member_fig(fid, block, sentence=None):
        return {
            "id": fid,
            "block": block,
            "sentence": sentence or fid,
            "golden": gold_asm[fid],
            "family": [v[fid] for v in variants],
            "lattice": {k: lattice_asm[k][fid] for k in lattice_asm},
            "routes": {
                "rigorous": rig_r1_asm[fid],
                "generous": gen_asm[fid],
                "hedge": hedge_asm[fid],
                "cutoff": cut_asm[fid],
            },
        }

    figures_spec = [
        _non_member_fig("C1_boron_2027", "component"),
        _non_member_fig("C2_scaling_2027", "component"),
        _non_member_fig("C3_struct_2027", "component"),
    ]
    for u in TRAINS:
        figures_spec.append({"id": f"A_{u}", "block": "ask", "member": u})
    figures_spec.append(_non_member_fig("A_total_2027", "ask", "Ask2_totals"))
    figures_spec.append(_non_member_fig("A_overhaul_2027", "ask", "Ask2_overhaul"))
    figures_spec.append(_non_member_fig("A_q3_2027", "ask", "Ask2_q3"))
    figures_spec.append(_non_member_fig("A_energy_mwh", "ask", "Ask3_energy_total"))
    figures_spec.append(_non_member_fig("A_overhaul_mwh", "ask", "Ask3_energy_overhaul"))

    spec = {
        "task": "task28",
        "call": "lines",
        "members": members_spec,
        "stumps": stumps_spec,
        "lattice": lattice_spec,
        "falsification": {
            "check": (
                "Three native-unit physical conservation & invariance checks (zero anomaly labels): "
                "F1 composite solute-flux 1/Q_bar slope + residual V8/V4 & r1(4); "
                "F2 two-path conservative seawater conductivity RMS (mS/cm); "
                "F3 stratified CIP_ALK vs CIP_ACID pattern drops on (1,1,0) and D3=1 (pp)."
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
        "over": {"S1": over_s1, "S2": over_s2, "S3": over_s3},
        "fal_detail": fal_detail,
        "r1_g": r1_g,
        "r2_g": r2_g,
        "r3_g": r3_g,
        "variants": variants,
    }
    return spec, diag


def run_forcing_perturbations(diag):
    """Test +/-20% independent perturbations on each mode's golden 2026 hours."""
    r1_g, r2_g, r3_g = diag["r1_g"], diag["r2_g"], diag["r3_g"]
    g_slate = sorted(u for u in TRAINS if diag["gold_asm"]["members"][u] >= THRESHOLD)
    out = []
    for mode_name, idx in [("S1_boron", 1), ("S2_scaling", 2), ("S3_struct", 3)]:
        for mult in (0.80, 1.20):
            x1 = {u: {**r1_g[u], "q": [v * mult for v in r1_g[u]["q"]]} for u in TRAINS} if idx == 1 else r1_g
            x2 = {u: {**r2_g[u], "q": [v * mult for v in r2_g[u]["q"]]} for u in TRAINS} if idx == 2 else r2_g
            x3 = {u: {**r3_g[u], "q": [v * mult for v in r3_g[u]["q"]]} for u in TRAINS} if idx == 3 else r3_g
            asm = assemble(x1, x2, x3)
            sl = sorted(u for u in TRAINS if asm["members"][u] >= THRESHOLD)
            ov_min = min(asm["members"][u] for u in g_slate)
            mo_max = max(asm["members"][u] for u in TRAINS if u not in g_slate)
            out.append(
                {
                    "input": f"{mode_name}_{int(round((mult - 1.0) * 100)):+d}pct",
                    "holds": sl == g_slate,
                    "answer": sl,
                    "min_overhaul": round(ov_min, 1),
                    "max_monitor": round(mo_max, 1),
                }
            )
    return out


if __name__ == "__main__":
    spec, diag = build_spec(SEED)
    print("=== task28 v2 Core Diagnostic (Seed %d) ===" % SEED)
    g = diag["gold_asm"]
    t = diag["truth_asm"]
    r1 = diag["rig_r1_asm"]
    r2 = diag["rig_r2_asm"]
    dir_a = diag["lattice_asm"]["S1+S2+S3"]
    print(f"{'Train':5s} {'Truth':>7s} {'Golden':>7s} {'B27':>6s} {'S27':>6s} {'St27':>6s} | {'Direct':>7s} {'R1_2.5h':>8s} {'R2_2.5h':>8s}")
    for u in TRAINS:
        sr = PLAN_SCHED_RATIO[u]
        b27 = sum(diag["r1_g"][u]["q"][q] * PLAN_BORON_TEMP_Q[q] * sr[q] for q in range(4))
        s27 = sum(diag["r2_g"][u]["q"][q] * PLAN_SCALING_REC_Q[q] * sr[q] for q in range(4))
        st27 = sum(diag["r3_g"][u]["q"][q] * sr[q] for q in range(4))
        print(
            f"{u:5s} {t['members'][u]:7.1f} {g['members'][u]:7.1f} {b27:6.1f} {s27:6.1f} {st27:6.1f} | "
            f"{dir_a['members'][u]:7.1f} {r1['members'][u]:8.1f} {r2['members'][u]:8.1f}"
        )
    print(
        f"Plant 2027: C1={g['C1_boron_2027']:.1f} C2={g['C2_scaling_2027']:.1f} C3={g['C3_struct_2027']:.1f} "
        f"Total={g['A_total_2027']:.1f} Overhaul={g['A_overhaul_2027']:.1f} Q3={g['A_q3_2027']:.1f} "
        f"Energy={g['A_energy_mwh']:.1f} MWh OvEnergy={g['A_overhaul_mwh']:.1f} MWh"
    )
    print("Falsification (comb, F1, F2, F3):")
    for k, (sc, parts) in diag["fal_detail"].items():
        print(f"  {k:16s}: {sc:7.3f}  (F1={parts[0]:.4f}, F2={parts[1]:.3f} mS/cm, F3={parts[2]:.3f} pp)")
    print("Rival calls:")
    for k, asm in list(diag["extra_routes"].items()) + [(f"OVER_{s}", diag["over"][s]) for s in ("S1", "S2", "S3")]:
        sl = [u for u in TRAINS if asm["members"][u] >= THRESHOLD]
        print(f"  {k:32s}: {sl}")
    pert = run_forcing_perturbations(diag)
    print("Forcing +/-20% perturbations:")
    for pt in pert:
        print(f"  {pt['input']:20s}: holds={pt['holds']} min_ov={pt['min_overhaul']:.1f} max_mo={pt['max_monitor']:.1f}")
    sys.exit(corelib.run(spec))
