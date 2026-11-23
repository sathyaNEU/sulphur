#!/usr/bin/env python3
"""task28/generator/core.py: Barlavento SWRO Desalination Plant (Algarve, Portugal)
Level 5 Anomaly Detection & Diagnostics Core (Physical & Environmental Sciences /
process-control-measurement-systems).

Simulates 8 parallel seawater reverse-osmosis (SWRO) membrane trains (TR01..TR08)
across 2026 (365 days = 8,760 hours = 35,040 fifteen-minute intervals = 2,190 four-hour
diagnostic blocks per train) and diagnoses which trains exceed Standard SWRO-Q27's
threshold of 400 projected 2027 anomalous operating hours for mandatory vessel overhaul.

Three independent observation-process stumps on three distinct axes:
  S1 (unit) - support_effect: 1-hour permeate boron excursion hours (> 0.50 mg/L)
              recovered from 4h weekday and 8h weekend lab composite bottles (zero 1h
              grabs) by inverting Matheron/Krige composite dispersion-autocovariance.
              Opens TR01 (short-range oscillatory spikes); over-correction (i.i.d.
              sqrt(m) scaling) flips TR04 (long-range smooth drift); log-log
              extrapolation flips TR05.
  S2 (when) - asynchronous_measurement_covariance + non_additive_aggregation:
              parcel-matched pretreatment-to-RO scaling co-excursion hours
              (intake precursor > 1.50 mg/L AND RO-feed stress > 1.50) recovered via
              Lagrangian cumulative-flow alignment Phi(t) = int Q dt with unobserved
              per-train effective hydraulic holdup volume V_eff != V_nom estimated
              from natural tidal seawater conductivity. Opens TR02 (short-circuited
              basin eta=0.50, strong positive parcel coupling); over-correction
              (comonotonic pairing) flips TR05 (negatively coupled feed-forward train).
  S3 (what) - rival_process_by_state_dependence + common_error_benchmark:
              true structural membrane/O-ring integrity fault hours separated from
              conditionally-dependent reversible bio-fouling across 3 imperfect
              non-destructive shift alarms (D1 salt passage, D2 stage dP, D3 acoustic
              bypass) using pre-CIP vs post-CIP physical invariance (zero destructive
              autopsies; CIP clears ~52% of fouling, leaving ~48% post-CIP). Opens
              TR03 (heavily bio-fouled healthy train); over-correction (raw D3
              without sensitivity inversion) flips TR06 (damaged low-fouling train).

Pure Python standard library only, seeded, ending on sys.exit(corelib.run(spec)).
"""
import bisect
import itertools
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

SEED = 2801
TRAINS = ["TR01", "TR02", "TR03", "TR04", "TR05", "TR06", "TR07", "TR08"]
THRESHOLD = 400.0  # Standard SWRO-Q27 Clause 3.1: >= 400 projected 2027 anomalous hours

# Standard SWRO-Q27 physical ceilings (filed in swro_integrity_standard_q27.pdf)
BORON_LIMIT = 0.50       # mg/L single-hour permeate boron ceiling
SCALING_X_LIM = 1.50     # intake algal-TEP precursor ceiling (mg/L eq)
SCALING_Y_LIM = 1.50     # RO-feed supersaturation-oxidant stress ceiling (index)

# Standard SWRO-Q27 Schedule B contractual cost tariffs (EUR per anomalous operating hour)
TARIFF_BORON = 420.0
TARIFF_SCALING = 360.0
TARIFF_STRUCT = 540.0

# 2026 calendar quarters (exact hours: Q1=90d, Q2=91d, Q3=92d, Q4=92d -> 365d = 8760h)
Q_DAYS = [90, 91, 92, 92]
Q_HOURS = [d * 24 for d in Q_DAYS]
Q_STARTS_H = [0, 2160, 4344, 6552, 8760]

# Filed 2027 Operating Plan (operating_plan_2027.csv & SWRO-Q27 Annex B)
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
# Realistic DAF + dual-media filter + filtered clearwell nominal volume V_nom ~ 1,100-1,440 m3
# (nominal residence time 1.5 to 6.5 hours across 200-790 m3/h tariff-driven flow!)
WORLD = {
    "TR01": dict(  # OPENED BY S1 (short-range oscillatory boron spikes -> reflex, direct & rigorous all < 400!)
        b_mu=0.347, b_sd=0.076, b_lam=1.12,
        v_nom=1200.0, eta=0.66, rho_p=0.62, xy_mu=-0.22,
        pi_foul=0.010, cip_clear=0.54, pi_struct=0.0080,
    ),
    "TR02": dict(  # OPENED BY S2 (short-circuited basin eta=0.48 + strong positive parcel coupling -> fixed_lag, steady_flow, nom_vol, reflex & rigorous all < 400!)
        b_mu=0.346, b_sd=0.060, b_lam=1.40,
        v_nom=1440.0, eta=0.48, rho_p=0.90, xy_mu=-0.16,
        pi_foul=0.005, cip_clear=0.52, pi_struct=0.0080,
    ),
    "TR03": dict(  # OPENED BY S3 (heavy reversible bio-fouling, low structural fault -> jumps > 400 without S3)
        b_mu=0.352, b_sd=0.056, b_lam=2.30,
        v_nom=1180.0, eta=0.72, rho_p=0.58, xy_mu=-0.20,
        pi_foul=0.165, cip_clear=0.52, pi_struct=0.0065,
    ),
    "TR04": dict(  # S1 OVER-CORRECTION GUARD (long-range smooth boron drift -> i.i.d. sqrt(m) flips > 400)
        b_mu=0.362, b_sd=0.055, b_lam=14.0,
        v_nom=1220.0, eta=0.76, rho_p=0.56, xy_mu=-0.22,
        pi_foul=0.025, cip_clear=0.54, pi_struct=0.0080,
    ),
    "TR05": dict(  # S2 OVER-CORRECTION GUARD (negatively coupled) + S1 LOG-LOG GUARD (short-range lam=1.45 -> loglog flips > 400!)
        b_mu=0.348, b_sd=0.068, b_lam=1.45,
        v_nom=1160.0, eta=0.88, rho_p=-0.52, xy_mu=0.00,
        pi_foul=0.025, cip_clear=0.53, pi_struct=0.0085,
    ),
    "TR06": dict(  # S3 OVER-CORRECTION GUARD (high structural fault, moderate bio-fouling -> forced on reflex, raw D3 flips < 400!)
        b_mu=0.356, b_sd=0.055, b_lam=2.40,
        v_nom=1240.0, eta=0.70, rho_p=0.58, xy_mu=-0.34,
        pi_foul=0.036, cip_clear=0.55, pi_struct=0.0345,
    ),
    "TR07": dict(  # FORCED HIGH TEXTURE (aging high-burden train; all 3 stumps move figures strongly)
        b_mu=0.382, b_sd=0.068, b_lam=1.45,
        v_nom=1360.0, eta=0.52, rho_p=0.82, xy_mu=0.05,
        pi_foul=0.220, cip_clear=0.52, pi_struct=0.0300,
    ),
    "TR08": dict(  # FORCED LOW TEXTURE (newer low-burden train; all 3 stumps still move its figures)
        b_mu=0.332, b_sd=0.060, b_lam=1.50,
        v_nom=1120.0, eta=0.82, rho_p=0.56, xy_mu=-0.24,
        pi_foul=0.020, cip_clear=0.56, pi_struct=0.0060,
    ),
}

BORON_SEASON_Q = [-0.012, 0.000, 0.018, -0.006]
SCALING_SEASON_Q = [-0.10, 0.00, 0.16, -0.06]

# S3 physical diagnostic channel emission parameters (shared across fleet)
# Clean membrane false-alarm baseline: 1.5% on D1/D2, 0.9% on D3
P_CLEAN = [0.015, 0.016, 0.009]
# True structural integrity fault (O-ring / delamination): D3 acoustic sensitivity = 0.52
# so raw D3 misses 48% of true structural faults -> strictly two-sided on TR06!
P_STRUCT = [0.88, 0.56, 0.52]
BITS = [[(b >> 2) & 1, (b >> 1) & 1, b & 1] for b in range(8)]
D3_MASK = [0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0]
MV_SET = {3, 5, 6, 7}


def _indep_e(p):
    e = [0.0] * 8
    for b in range(8):
        d1, d2, d3 = BITS[b]
        e[b] = (
            (p[0] if d1 else 1.0 - p[0])
            * (p[1] if d2 else 1.0 - p[1])
            * (p[2] if d3 else 1.0 - p[2])
        )
    return e


def _make_foul_e():
    e = [0.0] * 8
    for w, p1, p2, p3 in [(0.30, 0.28, 0.35, P_CLEAN[2]), (0.70, 0.92, 0.94, P_CLEAN[2])]:
        ep = _indep_e([p1, p2, p3])
        for b in range(8):
            e[b] += w * ep[b]
    return e


E_CLEAN_TRUE = _indep_e(P_CLEAN)
E_FOUL_TRUE = _make_foul_e()
E_STRUCT_TRUE = _indep_e(P_STRUCT)


def norm_sf(z):
    return 0.5 * math.erfc(z / math.sqrt(2.0))


def percentile(vals, p):
    sv = sorted(vals)
    n = len(sv)
    if n == 0:
        return 0.0
    idx = (p / 100.0) * (n - 1)
    lo = int(math.floor(idx))
    hi = min(n - 1, lo + 1)
    w = idx - lo
    return sv[lo] * (1.0 - w) + sv[hi] * w


def interp_uniform(xs, grid_vals, dv):
    nmax = len(grid_vals) - 2
    out = [0.0] * len(xs)
    inv_dv = 1.0 / dv
    for i, x in enumerate(xs):
        if x <= 0.0:
            out[i] = grid_vals[0]
        else:
            f = x * inv_dv
            k = int(f)
            if k > nmax:
                out[i] = grid_vals[nmax + 1]
            else:
                w = f - k
                out[i] = grid_vals[k] * (1.0 - w) + grid_vals[k + 1] * w
    return out


def interp_monotone(xq, xp, yp):
    n = len(xp)
    out = [0.0] * len(xq)
    j = 0
    xp0 = xp[0]
    xpn = xp[n - 1]
    for i, x in enumerate(xq):
        if x <= xp0:
            out[i] = yp[0]
        elif x >= xpn:
            out[i] = yp[n - 1]
        else:
            while j + 1 < n and xp[j + 1] < x:
                j += 1
            dx = xp[j + 1] - xp[j]
            if dx <= 1e-12:
                out[i] = yp[j]
            else:
                w = (x - xp[j]) / dx
                out[i] = yp[j] * (1.0 - w) + yp[j + 1] * w
    return out


def ar1_block_factors(phi, m):
    if phi <= 1e-9:
        return 1.0 / m, 0.0
    if phi >= 1.0 - 1e-9:
        return 1.0, 1.0
    s = 0.0
    p = phi
    for d in range(1, m):
        s += (m - d) * p
        p *= phi
    F = (m + 2.0 * s) / (m * m)
    geom = (1.0 - phi ** m) / (1.0 - phi)
    G = phi * (geom * geom) / (m * m)
    return F, G


def ou_block_factors(lam, m):
    if lam <= 1e-6:
        return 1e-6, 0.0
    x = m / lam
    F = 2.0 * (x - 1.0 + math.exp(-x)) / (x * x)
    G = ((1.0 - math.exp(-x)) ** 2) / (x * x)
    return F, G


def simulate_world(seed=SEED):
    rng = random.Random(seed)
    n_h = 8760
    n_15 = n_h * 4  # 35,040 fifteen-minute intervals
    dt15 = 0.25
    n_sh = n_h // 4  # 2,190 four-hour blocks

    q_h = [0] * n_h
    for q in range(4):
        for t in range(Q_STARTS_H[q], Q_STARTS_H[q + 1]):
            q_h[t] = q
    q_15 = [q_h[t // 4] for t in range(n_15)]
    q_sh = [q_h[b * 4] for b in range(n_sh)]

    c_clean_cdf = list(itertools.accumulate(E_CLEAN_TRUE))
    c_foul_cdf = list(itertools.accumulate(E_FOUL_TRUE))
    c_struct_cdf = list(itertools.accumulate(E_STRUCT_TRUE))

    data = {"q_h": q_h, "q_15": q_15, "q_sh": q_sh, "trains": {}}

    for u in TRAINS:
        wp = WORLD[u]

        # ---- MODE 1: Hourly permeate boron AR(1) + 4h weekday / 8h weekend composites ----
        phi = math.exp(-1.0 / wp["b_lam"])
        innov_sd = wp["b_sd"] * math.sqrt(max(1e-9, 1.0 - phi * phi))
        b_true_h = [0.0] * n_h
        z = rng.gauss(0.0, wp["b_sd"])
        b_mu = wp["b_mu"]
        b_true_h[0] = b_mu + BORON_SEASON_Q[q_h[0]] + z
        for t in range(1, n_h):
            z = phi * z + rng.gauss(0.0, innov_sd)
            b_true_h[t] = b_mu + BORON_SEASON_Q[q_h[t]] + z

        truth_boron_q = [0.0] * 4
        for t in range(n_h):
            if b_true_h[t] > BORON_LIMIT:
                truth_boron_q[q_h[t]] += 1.0

        comp_m, comp_q, comp_val, comp_day = [], [], [], []
        for day in range(365):
            m = 4 if (day % 7) < 5 else 8
            h0 = day * 24
            qd = q_h[h0]
            for k in range(24 // m):
                s = sum(b_true_h[h0 + k * m:h0 + (k + 1) * m]) / m
                val = s + rng.gauss(0.0, 0.004)
                comp_m.append(m)
                comp_q.append(qd)
                comp_val.append(val)
                comp_day.append(day)

        # ---- MODE 2: 15-min intake/RO-feed hydraulic Lagrangian parcel process ----
        # Strong diurnal tariff load-following flow: 200 to 790 m3/h (~4x swing!)
        phase_u = rng.uniform(0.0, 2.0 * math.pi)
        q_flow_h = [0.0] * n_h
        q_ar = 0.0
        for t in range(n_h):
            q_raw = (
                475.0
                - 245.0 * math.sin(2.0 * math.pi * (t - 9.0) / 24.0)
                + 65.0 * math.cos(2.0 * math.pi * t / 168.0 + phase_u)
                + 40.0 * math.sin(2.0 * math.pi * t / 8760.0 - 1.2)
            )
            q_ar = 0.90 * q_ar + rng.gauss(0.0, 20.0)
            v = q_raw + q_ar
            q_flow_h[t] = 200.0 if v < 200.0 else (790.0 if v > 790.0 else v)

        phi_15 = [0.0] * n_15
        q_15_true = [0.0] * n_15
        acc = 0.0
        for i in range(n_15):
            h_f = i * dt15
            h0 = int(h_f)
            w = h_f - h0
            qf = q_flow_h[h0] if h0 >= n_h - 1 else q_flow_h[h0] * (1.0 - w) + q_flow_h[h0 + 1] * w
            q_15_true[i] = qf
            acc += qf * dt15
            phi_15[i] = acc

        v_eff = wp["v_nom"] * wp["eta"]
        dv = 20.0
        n_vol = int(phi_15[-1] / dv) + 200

        a_c = math.exp(-dv / 310.0)
        sd_c = 1.85 * math.sqrt(1.0 - a_c * a_c)
        c_vol = [0.0] * n_vol
        val = 0.0
        for k in range(1, n_vol):
            val = a_c * val + rng.gauss(0.0, sd_c)
            c_vol[k] = val

        a_x = math.exp(-dv / 280.0)
        sd_x = math.sqrt(1.0 - a_x * a_x)
        x_vol = [0.0] * n_vol
        xi_vol = [0.0] * n_vol
        vx = rng.gauss(0.0, 1.0)
        vxi = rng.gauss(0.0, 1.0)
        x_vol[0], xi_vol[0] = vx, vxi
        for k in range(1, n_vol):
            vx = a_x * vx + rng.gauss(0.0, sd_x)
            vxi = a_x * vxi + rng.gauss(0.0, sd_x)
            x_vol[k] = vx
            xi_vol[k] = vxi

        phi_lag = [p - v_eff if p > v_eff else 0.0 for p in phi_15]
        phi_lag_m = [p - 25.0 if p > 25.0 else 0.0 for p in phi_lag]
        phi_lag_p = [p + 25.0 for p in phi_lag]

        c_in_raw = interp_uniform(phi_15, c_vol, dv)
        c_om = interp_uniform(phi_lag_m, c_vol, dv)
        c_o0 = interp_uniform(phi_lag, c_vol, dv)
        c_op = interp_uniform(phi_lag_p, c_vol, dv)

        c_in_15 = [52.0 + c_in_raw[i] + rng.gauss(0.0, 0.08) for i in range(n_15)]
        c_out_15 = [52.0 + 0.15 * c_om[i] + 0.70 * c_o0[i] + 0.15 * c_op[i] + rng.gauss(0.0, 0.08) for i in range(n_15)]

        x_in_raw = interp_uniform(phi_15, x_vol, dv)
        x_at_out = interp_uniform(phi_lag, x_vol, dv)
        xi_at_out = interp_uniform(phi_lag, xi_vol, dv)

        # High-velocity hydraulic loading during off-peak night ramp-up elevates DMF breakthrough
        q_boost_in = [0.42 * ((q_15_true[i] - 475.0) / 220.0) for i in range(n_15)]
        q_boost_parcel = interp_monotone(phi_lag, phi_15, q_boost_in)

        xy_mu = wp["xy_mu"]
        rho_p = wp["rho_p"]
        s_rho = math.sqrt(max(1e-9, 1.0 - rho_p * rho_p))
        x_in_15 = [0.0] * n_15
        y_out_15 = [0.0] * n_15
        truth_scaling_q = [0.0] * 4
        for i in range(n_15):
            qs = SCALING_SEASON_Q[q_15[i]]
            x_in_15[i] = xy_mu + qs + q_boost_in[i] + x_in_raw[i]
            xp_t = xy_mu + qs + q_boost_parcel[i] + x_at_out[i]
            yo = xy_mu + qs + q_boost_parcel[i] + rho_p * x_at_out[i] + s_rho * xi_at_out[i]
            y_out_15[i] = yo
            if i >= 32 and xp_t > SCALING_X_LIM and yo > SCALING_Y_LIM:
                truth_scaling_q[q_15[i]] += dt15

        # ---- MODE 3: 4-hour shift diagnostic alarms (D1, D2, D3) + CIP wash events ----
        cip_blocks = []
        b_cur = rng.randint(24, 53)
        while b_cur < n_sh:
            cip_blocks.append(b_cur)
            b_cur += rng.randint(84, 113)
        is_post_cip = [False] * n_sh
        for cb in cip_blocks:
            for j in range(cb, min(n_sh, cb + 30)):
                is_post_cip[j] = True

        pi_s = wp["pi_struct"]
        pi_f_pre = wp["pi_foul"]
        pi_f_post = wp["pi_foul"] * (1.0 - wp["cip_clear"])

        pat_sh = [0] * n_sh
        truth_struct_q = [0.0] * 4
        cnt_pre = [0.0] * 8
        cnt_post = [0.0] * 8
        for b in range(n_sh):
            pf = pi_f_post if is_post_cip[b] else pi_f_pre
            u_draw = rng.random()
            if u_draw < pi_s:
                truth_struct_q[q_sh[b]] += 4.0
                cdf = c_struct_cdf
            elif u_draw < pi_s + pf:
                cdf = c_foul_cdf
            else:
                cdf = c_clean_cdf
            p_draw = rng.random()
            pat = bisect.bisect_left(cdf, p_draw)
            if pat > 7:
                pat = 7
            pat_sh[b] = pat
            if is_post_cip[b]:
                cnt_post[pat] += 1.0
            else:
                cnt_pre[pat] += 1.0

        data["trains"][u] = {
            "comp_m": comp_m,
            "comp_q": comp_q,
            "comp_val": comp_val,
            "comp_day": comp_day,
            "truth_boron_q": truth_boron_q,
            "q_flow_h": q_flow_h,
            "v_nom": wp["v_nom"],
            "v_eff_true": v_eff,
            "c_in_15": c_in_15,
            "c_out_15": c_out_15,
            "x_in_15": x_in_15,
            "y_out_15": y_out_15,
            "truth_scaling_q": truth_scaling_q,
            "pat_sh": pat_sh,
            "is_post_cip": is_post_cip,
            "cip_blocks": cip_blocks,
            "cnt_pre": cnt_pre,
            "cnt_post": cnt_post,
            "truth_struct_q": truth_struct_q,
        }
    return data


def project_2027(bq, sq, stq, u):
    sr = PLAN_SCHED_RATIO[u]
    b27 = [bq[q] * PLAN_BORON_TEMP_Q[q] * sr[q] for q in range(4)]
    s27 = [sq[q] * PLAN_SCALING_REC_Q[q] * sr[q] for q in range(4)]
    st27 = [stq[q] * sr[q] for q in range(4)]
    return b27, s27, st27


# ==============================================================================
# S1 ESTIMATORS
# ==============================================================================
def _comp_moments(td, trim_pct=0.0):
    cm, cq, cv, cd = td["comp_m"], td["comp_q"], td["comp_val"], td["comp_day"]
    q_sum = [0.0] * 4
    q_cnt = [0] * 4
    for i in range(len(cv)):
        q = cq[i]
        q_sum[q] += cv[i]
        q_cnt[q] += 1
    q_mu = [q_sum[q] / q_cnt[q] for q in range(4)]
    resid = [cv[i] - q_mu[cq[i]] for i in range(len(cv))]

    stats = {}
    for m in (4, 8):
        idx = [i for i in range(len(cm)) if cm[i] == m]
        r = [resid[i] for i in idx]
        if trim_pct > 0.0:
            lo = percentile(r, trim_pct)
            hi = percentile(r, 100.0 - trim_pct)
            r = [lo if x < lo else (hi if x > hi else x) for x in r]
        mu_r = sum(r) / len(r)
        var_m = sum((x - mu_r) ** 2 for x in r) / (len(r) - 1)
        pa, pb = [], []
        for k in range(len(idx) - 1):
            i1, i2 = idx[k], idx[k + 1]
            if i2 == i1 + 1 and (cd[i2] - cd[i1]) <= 1:
                pa.append(resid[i1])
                pb.append(resid[i2])
        ma = sum(pa) / len(pa)
        mb = sum(pb) / len(pb)
        cov1_m = sum((pa[k] - ma) * (pb[k] - mb) for k in range(len(pa))) / len(pa)
        stats[m] = {"var": var_m, "cov1": cov1_m, "r1": cov1_m / max(var_m, 1e-12)}
    return q_mu, stats


def estimate_s1(data, mode="golden", kernel="ar1", obj="wls", trim_pct=0.0, use_m8=True, lab_noise=True):
    out = {}
    all_moments = {u: _comp_moments(data["trains"][u], trim_pct=trim_pct) for u in TRAINS}
    lab_var = (0.004 ** 2) if lab_noise else 0.0

    if mode == "pooled":
        r1_pool = sum(all_moments[u][1][4]["r1"] for u in TRAINS) / len(TRAINS)
        best_phi, best_err = 0.5, 1e9
        for k in range(350):
            phi = 0.05 + 0.93 * k / 349.0
            F4, G4 = ar1_block_factors(phi, 4)
            err = abs(G4 / F4 - r1_pool)
            if err < best_err:
                best_err, best_phi = err, phi
        F4_p, G4_p = ar1_block_factors(best_phi, 4)
        F8_p, _ = ar1_block_factors(best_phi, 8)

    lam_grid = [0.25 * ((30.0 / 0.25) ** (k / 219.0)) for k in range(220)]

    for u in TRAINS:
        td = data["trains"][u]
        q_mu, st = all_moments[u]
        v4 = max(1e-7, st[4]["var"] - lab_var)
        v8 = max(1e-7, st[8]["var"] - lab_var)
        c4 = max(0.0, st[4]["cov1"])
        c8 = max(0.0, st[8]["cov1"])

        if mode == "direct":
            q_hrs = [0.0] * 4
            for q in range(4):
                vals = [td["comp_val"][i] for i in range(len(td["comp_val"])) if td["comp_q"][i] == q]
                q_hrs[q] = (sum(1 for x in vals if x > BORON_LIMIT) / len(vals)) * Q_HOURS[q]
            out[u] = {"q": q_hrs, "sd1": math.sqrt(v4), "lam": 100.0, "v8_v4_pred": 1.0, "r1_4_pred": 1.0}
            continue

        if mode == "comp_param":
            res = [td["comp_val"][i] - q_mu[td["comp_q"][i]] for i in range(len(td["comp_val"]))]
            sd_raw = math.sqrt(sum(x * x for x in res) / (len(res) - 1))
            q_hrs = [norm_sf((BORON_LIMIT - q_mu[q]) / sd_raw) * Q_HOURS[q] for q in range(4)]
            out[u] = {"q": q_hrs, "sd1": sd_raw, "lam": 100.0, "v8_v4_pred": 1.0, "r1_4_pred": 1.0}
            continue

        if mode == "cutoff_4h":
            sd4 = math.sqrt(st[4]["var"])
            q_hrs = [norm_sf((BORON_LIMIT - q_mu[q]) / sd4) * Q_HOURS[q] for q in range(4)]
            out[u] = {"q": q_hrs, "sd1": sd4, "lam": 100.0, "v8_v4_pred": 1.0, "r1_4_pred": 1.0}
            continue

        if mode == "iid_over":
            s2_iid = 0.5 * (4.0 * v4 + 8.0 * v8)
            sd1 = math.sqrt(s2_iid)
            q_hrs = [norm_sf((BORON_LIMIT - q_mu[q]) / sd1) * Q_HOURS[q] for q in range(4)]
            out[u] = {"q": q_hrs, "sd1": sd1, "lam": 0.0, "v8_v4_pred": 0.5, "r1_4_pred": 0.0}
            continue

        if mode == "loglog":
            slope = math.log(max(v8, 1e-9) / max(v4, 1e-9)) / math.log(2.0)
            slope = max(-1.0, min(0.0, slope))
            s2_ll = v4 * (4.0 ** (-slope))
            sd1 = math.sqrt(s2_ll)
            q_hrs = [norm_sf((BORON_LIMIT - q_mu[q]) / sd1) * Q_HOURS[q] for q in range(4)]
            out[u] = {"q": q_hrs, "sd1": sd1, "lam": 0.0, "v8_v4_pred": 2.0 ** slope, "r1_4_pred": 0.0}
            continue

        if mode == "pooled":
            s2_p = 0.5 * (v4 / F4_p + v8 / F8_p)
            sd1 = math.sqrt(s2_p)
            q_hrs = [norm_sf((BORON_LIMIT - q_mu[q]) / sd1) * Q_HOURS[q] for q in range(4)]
            out[u] = {"q": q_hrs, "sd1": sd1, "lam": -1.0 / math.log(best_phi), "v8_v4_pred": F8_p / F4_p, "r1_4_pred": G4_p / F4_p}
            continue

        best_loss = 1e18
        best_res = None
        for lam in lam_grid:
            if kernel == "ar1":
                phi = math.exp(-1.0 / lam)
                F4, G4 = ar1_block_factors(phi, 4)
                F8, G8 = ar1_block_factors(phi, 8)
                F1 = 1.0
            elif kernel == "ou":
                F4, G4 = ou_block_factors(lam, 4)
                F8, G8 = ou_block_factors(lam, 8)
                F1, _ = ou_block_factors(lam, 1)
            else:
                raise ValueError(kernel)

            if obj == "r1_only":
                r1_pred = G4 / max(F4, 1e-12)
                loss = (r1_pred - c4 / v4) ** 2
                s2 = v4 / F4
            else:
                obs = [v4, c4] + ([v8, c8] if use_m8 else [])
                mod = [F4, G4] + ([F8, G8] if use_m8 else [])
                if obj == "wls":
                    w = [3.0 / (v4 * v4), 3.0 / (v4 * v4)] + ([1.0 / (v8 * v8), 0.7 / (v8 * v8)] if use_m8 else [])
                else:
                    w = [1.0] * len(obs)
                num = sum(wi * oi * mi for wi, oi, mi in zip(w, obs, mod))
                den = sum(wi * mi * mi for wi, mi in zip(w, mod))
                s2 = max(1e-9, num / max(den, 1e-12))
                loss = sum(wi * (oi - s2 * mi) ** 2 for wi, oi, mi in zip(w, obs, mod))
            if loss < best_loss:
                best_loss = loss
                best_res = (math.sqrt(s2 * F1), lam, F8 / F4, G4 / F4)

        sd1, lam_hat, v8_v4_pred, r1_4_pred = best_res
        q_hrs = [norm_sf((BORON_LIMIT - q_mu[q]) / sd1) * Q_HOURS[q] for q in range(4)]
        out[u] = {"q": q_hrs, "sd1": sd1, "lam": lam_hat, "v8_v4_pred": v8_v4_pred, "r1_4_pred": r1_4_pred}
    return out


# ==============================================================================
# S2 ESTIMATORS
# ==============================================================================
def _build_phi_hat(q_h, flow_interp="linear"):
    n_h = len(q_h)
    n_15 = n_h * 4
    dt15 = 0.25
    phi = [0.0] * n_15
    q15 = [0.0] * n_15
    acc = 0.0
    for i in range(n_15):
        if flow_interp == "step":
            qf = q_h[i // 4]
        elif flow_interp == "linear":
            h_f = i * dt15
            h0 = int(h_f)
            w = h_f - h0
            qf = q_h[h0] if h0 >= n_h - 1 else q_h[h0] * (1.0 - w) + q_h[h0 + 1] * w
        else:
            h_f = i * dt15 - 0.5
            if h_f <= 0.0:
                qf = q_h[0]
            elif h_f >= n_h - 1:
                qf = q_h[n_h - 1]
            else:
                h0 = int(h_f)
                w = h_f - h0
                qf = q_h[h0] * (1.0 - w) + q_h[h0 + 1] * w
        q15[i] = qf
        acc += qf * dt15
        phi[i] = acc
    return phi, q15


def _eval_v_loss(phi_hat, c_in, c_out, v_cand, loss_fn="l2", stride=1, trim_q=0.0):
    n = len(phi_hat)
    xq = [phi_hat[i] - v_cand for i in range(32, n, stride)]
    c_al = interp_monotone(xq, phi_hat, c_in)
    diffs = [c_out[32 + k * stride] - c_al[k] for k in range(len(xq))]
    if trim_q > 0.0:
        absd = [abs(d) for d in diffs]
        hi = percentile(absd, 100.0 - trim_q)
        diffs = [d for d in diffs if abs(d) <= hi]
    if loss_fn == "l2":
        return sum(d * d for d in diffs) / len(diffs)
    elif loss_fn == "l1":
        return sum(abs(d) for d in diffs) / len(diffs)
    elif loss_fn == "huber":
        delta = 0.5
        return sum(0.5 * d * d if abs(d) <= delta else delta * (abs(d) - 0.5 * delta) for d in diffs) / len(diffs)
    elif loss_fn == "corr":
        ys = [c_out[32 + k * stride] for k in range(len(xq))]
        mx = sum(c_al) / len(c_al)
        my = sum(ys) / len(ys)
        num = sum((c_al[k] - mx) * (ys[k] - my) for k in range(len(c_al)))
        dx = math.sqrt(sum((x - mx) ** 2 for x in c_al))
        dy = math.sqrt(sum((y - my) ** 2 for y in ys))
        return -num / max(dx * dy, 1e-12)
    raise ValueError(loss_fn)


def estimate_s2(data, mode="golden", flow_interp="linear", loss_fn="l2", trim_q=0.0):
    q_15 = data["q_15"]
    n_15 = len(q_15)
    dt15 = 0.25
    out = {}

    for u in TRAINS:
        td = data["trains"][u]
        c_in, c_out = td["c_in_15"], td["c_out_15"]
        x_in, y_out = td["x_in_15"], td["y_out_15"]
        q_h = td["q_flow_h"]
        phi_hat, q_15_hat = _build_phi_hat(q_h, flow_interp=flow_interp)

        if mode == "direct":
            x_al = x_in
            c_rms = math.sqrt(sum((c_out[i] - c_in[i]) ** 2 for i in range(32, n_15)) / (n_15 - 32))
            v_hat = 0.0
        elif mode == "fixed_lag":
            best_lag, best_rms = 0, 1e9
            for lag in range(0, 28):
                rms = math.sqrt(sum((c_out[i] - c_in[i - lag]) ** 2 for i in range(32, n_15)) / (n_15 - 32))
                if rms < best_rms:
                    best_rms, best_lag = rms, lag
            x_al = [x_in[i - best_lag] if i >= best_lag else x_in[0] for i in range(n_15)]
            c_rms = best_rms
            v_hat = best_lag * dt15 * (sum(q_h) / len(q_h))
        elif mode == "nom_vol":
            v_hat = td["v_nom"]
            xq = [p - v_hat for p in phi_hat]
            x_al = interp_monotone(xq, phi_hat, x_in)
            c_al = interp_monotone(xq, phi_hat, c_in)
            c_rms = math.sqrt(sum((c_out[i] - c_al[i]) ** 2 for i in range(32, n_15)) / (n_15 - 32))
        elif mode == "steady_flow":
            q_med = percentile(q_15_hat, 50.0)
            steady_idx = [i for i in range(32, n_15) if abs(q_15_hat[i] - q_med) <= 0.25 * q_med]
            best_lag, best_rms = 0, 1e9
            for lag in range(0, 28):
                rms = math.sqrt(sum((c_out[i] - c_in[i - lag]) ** 2 for i in steady_idx) / len(steady_idx))
                if rms < best_rms:
                    best_rms, best_lag = rms, lag
            q_hrs = [0.0] * 4
            for q in range(4):
                sq_idx = [i for i in steady_idx if q_15[i] == q]
                hits = sum(1 for i in sq_idx if x_in[i - best_lag] > SCALING_X_LIM and y_out[i] > SCALING_Y_LIM)
                q_hrs[q] = (hits / len(sq_idx)) * Q_HOURS[q]
            c_rms_all = math.sqrt(sum((c_out[i] - c_in[i - best_lag]) ** 2 for i in range(32, n_15)) / (n_15 - 32))
            out[u] = {"q": q_hrs, "v_hat": best_lag * dt15 * q_med, "c_rms": c_rms_all}
            continue
        elif mode == "comonotonic_over":
            q_hrs = [0.0] * 4
            for q in range(4):
                cnt_q = 0
                hx = 0
                hy = 0
                for i in range(32, n_15):
                    if q_15[i] == q:
                        cnt_q += 1
                        if x_in[i] > SCALING_X_LIM:
                            hx += 1
                        if y_out[i] > SCALING_Y_LIM:
                            hy += 1
                q_hrs[q] = (min(hx, hy) / cnt_q) * Q_HOURS[q]
            c_rms = math.sqrt(sum((c_out[i] - c_in[i]) ** 2 for i in range(32, n_15)) / (n_15 - 32))
            out[u] = {"q": q_hrs, "v_hat": td["v_nom"], "c_rms": c_rms}
            continue
        else:
            # Coarse-to-fine profile scan over [400, 1450] m3
            best_v, best_val = 750.0, 1e18
            for k in range(53):  # 400 to 1440 step 20 m3 at stride 8
                vc = 400.0 + 20.0 * k
                sc = _eval_v_loss(phi_hat, c_in, c_out, vc, loss_fn=loss_fn, stride=8, trim_q=trim_q)
                if sc < best_val:
                    best_val, best_v = sc, vc
            v0 = best_v
            best_val = 1e18
            for dv_off in range(-24, 25, 4):
                vf = max(350.0, min(1500.0, v0 + dv_off))
                sc = _eval_v_loss(phi_hat, c_in, c_out, vf, loss_fn=loss_fn, stride=3, trim_q=trim_q)
                if sc < best_val:
                    best_val, best_v = sc, vf
            v1 = best_v
            best_val = 1e18
            for dv_off in (-4, -2, 0, 2, 4):
                vf = max(350.0, min(1500.0, v1 + dv_off))
                sc = _eval_v_loss(phi_hat, c_in, c_out, vf, loss_fn=loss_fn, stride=1, trim_q=trim_q)
                if sc < best_val:
                    best_val, best_v = sc, vf
            v_hat = best_v
            xq = [p - v_hat for p in phi_hat]
            x_al = interp_monotone(xq, phi_hat, x_in)
            c_al = interp_monotone(xq, phi_hat, c_in)
            c_rms = math.sqrt(sum((c_out[i] - c_al[i]) ** 2 for i in range(32, n_15)) / (n_15 - 32))

        q_hrs = [0.0] * 4
        for i in range(32, n_15):
            if x_al[i] > SCALING_X_LIM and y_out[i] > SCALING_Y_LIM:
                q_hrs[q_15[i]] += dt15
        out[u] = {"q": q_hrs, "v_hat": v_hat, "c_rms": c_rms}
    return out


# ==============================================================================
# S3 ESTIMATORS
# ==============================================================================
def _fit_ds2_ci(cnt_trains):
    U = len(cnt_trains)
    n_u = [sum(row) for row in cnt_trains]
    p0 = [0.025, 0.025, 0.015]
    p1 = [0.82, 0.78, 0.25]
    pi = [0.06] * U

    for _ in range(120):
        e0 = _indep_e(p0)
        e1 = _indep_e(p1)
        w0_sum = [0.0] * 8
        w1_sum = [0.0] * 8
        for i in range(U):
            tot1 = 0.0
            for b in range(8):
                num = pi[i] * e1[b]
                den = (1.0 - pi[i]) * e0[b] + num + 1e-15
                g = num / den
                c1 = cnt_trains[i][b] * g
                c0 = cnt_trains[i][b] - c1
                tot1 += c1
                w1_sum[b] += c1
                w0_sum[b] += c0
            pi[i] = max(1e-4, min(0.99, tot1 / n_u[i]))
        s0 = max(sum(w0_sum), 1e-9)
        s1 = max(sum(w1_sum), 1e-9)
        for j in range(3):
            p0[j] = max(1e-3, min(0.995, sum(w0_sum[b] * BITS[b][j] for b in range(8)) / s0))
            p1[j] = max(1e-3, min(0.995, sum(w1_sum[b] * BITS[b][j] for b in range(8)) / s1))
    return pi, p0, p1, _indep_e(p0), _indep_e(p1)


def _fit_lca3_cip(cnt_pre, cnt_post, foul_model="tied_d3_d12", cip_mode="free_per_train", n_iter=320):
    U = len(cnt_pre)
    n_pre = [sum(row) for row in cnt_pre]
    n_post = [sum(row) for row in cnt_post]
    p0 = [0.018, 0.018, 0.010]
    p2 = [0.85, 0.55, 0.55]
    e1 = [0.10, 0.001, 0.14, 0.002, 0.11, 0.001, 0.64, 0.006]
    s_e1 = sum(e1)
    e1 = [x / s_e1 for x in e1]
    pi_s = [0.015] * U
    pi_f_pre = [0.05] * U
    pi_f_post = [0.025] * U

    for _ in range(n_iter):
        e0 = _indep_e(p0)
        e2 = _indep_e(p2)
        W0 = [0.0] * 8
        W1 = [0.0] * 8
        W2 = [0.0] * 8
        w1_pre_u = [0.0] * U
        w1_post_u = [0.0] * U
        w2_tot_u = [0.0] * U

        for i in range(U):
            p0_pr = max(1e-6, 1.0 - pi_f_pre[i] - pi_s[i])
            p0_po = max(1e-6, 1.0 - pi_f_post[i] - pi_s[i])
            for b in range(8):
                a0 = p0_pr * e0[b]
                a1 = pi_f_pre[i] * e1[b]
                a2 = pi_s[i] * e2[b]
                dn = a0 + a1 + a2 + 1e-15
                c = cnt_pre[i][b]
                c0, c1, c2 = c * a0 / dn, c * a1 / dn, c * a2 / dn
                W0[b] += c0
                W1[b] += c1
                W2[b] += c2
                w1_pre_u[i] += c1
                w2_tot_u[i] += c2

                a0 = p0_po * e0[b]
                a1 = pi_f_post[i] * e1[b]
                a2 = pi_s[i] * e2[b]
                dn = a0 + a1 + a2 + 1e-15
                c = cnt_post[i][b]
                c0, c1, c2 = c * a0 / dn, c * a1 / dn, c * a2 / dn
                W0[b] += c0
                W1[b] += c1
                W2[b] += c2
                w1_post_u[i] += c1
                w2_tot_u[i] += c2

        for i in range(U):
            pi_s[i] = max(1e-4, min(0.50, w2_tot_u[i] / (n_pre[i] + n_post[i])))

        if cip_mode == "common_clear":
            pf_pr_s = sum(w1_pre_u[i] / n_pre[i] for i in range(U))
            pf_po_s = sum(w1_post_u[i] / n_post[i] for i in range(U))
            ratio_c = max(0.15, min(0.90, pf_po_s / max(pf_pr_s, 1e-9)))
            for i in range(U):
                pi_f_pre[i] = max(1e-4, min(0.85, (w1_pre_u[i] + w1_post_u[i]) / (n_pre[i] + ratio_c * n_post[i])))
                pi_f_post[i] = ratio_c * pi_f_pre[i]
        else:
            for i in range(U):
                pr = max(1e-4, min(0.85, w1_pre_u[i] / n_pre[i]))
                po = max(1e-4, min(pr * 0.95, w1_post_u[i] / n_post[i]))
                pi_f_pre[i], pi_f_post[i] = pr, po

        for i in range(U):
            if pi_f_pre[i] + pi_s[i] > 0.995:
                pi_f_pre[i] *= 0.995 / (pi_f_pre[i] + pi_s[i])
            if pi_f_post[i] + pi_s[i] > 0.995:
                pi_f_post[i] *= 0.995 / (pi_f_post[i] + pi_s[i])

        s0 = max(sum(W0), 1e-9)
        s1 = max(sum(W1), 1e-9)
        s2 = max(sum(W2), 1e-9)
        for j in range(3):
            p0[j] = max(1e-3, min(0.20, sum(W0[b] * BITS[b][j] for b in range(8)) / s0))
            p2[j] = max(0.15, min(0.99, sum(W2[b] * BITS[b][j] for b in range(8)) / s2))

        if foul_model == "tied_d3_d12":
            p3_base = max(1e-3, min(0.10, sum((W0[b] + W1[b]) * BITS[b][2] for b in range(8)) / (s0 + s1)))
            p0[2] = p3_base
            p12 = [max(1e-5, (W1[2 * j] + W1[2 * j + 1]) / s1) for j in range(4)]
            s12 = sum(p12)
            p12 = [x / s12 for x in p12]
            e1 = [0.0] * 8
            for j in range(4):
                e1[2 * j] = p12[j] * (1.0 - p3_base)
                e1[2 * j + 1] = p12[j] * p3_base
        elif foul_model == "free_d12":
            p3_f = max(1e-3, min(0.03, sum(W1[b] * BITS[b][2] for b in range(8)) / s1))
            p12 = [max(1e-5, (W1[2 * j] + W1[2 * j + 1]) / s1) for j in range(4)]
            s12 = sum(p12)
            p12 = [x / s12 for x in p12]
            e1 = [0.0] * 8
            for j in range(4):
                e1[2 * j] = p12[j] * (1.0 - p3_f)
                e1[2 * j + 1] = p12[j] * p3_f
        elif foul_model == "indep_tied":
            p3_base = max(1e-3, min(0.10, sum((W0[b] + W1[b]) * BITS[b][2] for b in range(8)) / (s0 + s1)))
            p0[2] = p3_base
            pf_v = [
                max(1e-3, min(0.99, sum(W1[b] * BITS[b][0] for b in range(8)) / s1)),
                max(1e-3, min(0.99, sum(W1[b] * BITS[b][1] for b in range(8)) / s1)),
                p3_base,
            ]
            e1 = _indep_e(pf_v)

    return pi_s, pi_f_pre, pi_f_post, _indep_e(p0), e1, _indep_e(p2), p0, p2


def estimate_s3(data, mode="golden", foul_model="tied_d3_d12", cip_mode="free_per_train", post_window_blocks=30):
    q_sh = data["q_sh"]
    n_sh = len(q_sh)

    cnt_pre_mat = []
    cnt_post_mat = []
    post_masks = {}
    for u in TRAINS:
        td = data["trains"][u]
        if post_window_blocks == 30:
            pm = td["is_post_cip"]
        else:
            pm = [False] * n_sh
            for cb in td["cip_blocks"]:
                for j in range(cb, min(n_sh, cb + post_window_blocks)):
                    pm[j] = True
        post_masks[u] = pm
        cpr = [0.0] * 8
        cpo = [0.0] * 8
        for b in range(n_sh):
            if pm[b]:
                cpo[td["pat_sh"][b]] += 1.0
            else:
                cpr[td["pat_sh"][b]] += 1.0
        cnt_pre_mat.append(cpr)
        cnt_post_mat.append(cpo)
    cnt_all_mat = [[cnt_pre_mat[i][b] + cnt_post_mat[i][b] for b in range(8)] for i in range(len(TRAINS))]
    out = {}

    if mode == "direct":
        for i, u in enumerate(TRAINS):
            td = data["trains"][u]
            q_hrs = [0.0] * 4
            hits = 0
            for b in range(n_sh):
                if td["pat_sh"][b] in MV_SET:
                    q_hrs[q_sh[b]] += 4.0
                    hits += 1
            out[u] = {"q": q_hrs, "pi_s": hits / n_sh, "pred_drop_6": 0.0, "pred_drop_d3": 0.0}
        return out

    if mode == "ds2_ci":
        pi, p0, p1, e0, e1 = _fit_ds2_ci(cnt_all_mat)
        de = [e1[b] - e0[b] for b in range(8)]
        de2 = sum(x * x for x in de)
        d3_de = sum(de[b] * D3_MASK[b] for b in range(8))
        for i, u in enumerate(TRAINS):
            s_pr = sum(cnt_pre_mat[i])
            s_po = sum(cnt_post_mat[i])
            p_pr = [x / s_pr for x in cnt_pre_mat[i]]
            p_po = [x / s_po for x in cnt_post_mat[i]]
            pi_pr = max(0.0, min(1.0, sum((p_pr[b] - e0[b]) * de[b] for b in range(8)) / de2))
            pi_po = max(0.0, min(1.0, sum((p_po[b] - e0[b]) * de[b] for b in range(8)) / de2))
            out[u] = {
                "q": [pi[i] * Q_HOURS[q] for q in range(4)],
                "pi_s": pi[i],
                "pred_drop_6": (pi_pr - pi_po) * de[6],
                "pred_drop_d3": (pi_pr - pi_po) * d3_de,
            }
        return out

    if mode == "post_cip_mv":
        for i, u in enumerate(TRAINS):
            td = data["trains"][u]
            pm = post_masks[u]
            cnt_po = sum(1 for b in range(n_sh) if pm[b])
            hits = sum(1 for b in range(n_sh) if pm[b] and td["pat_sh"][b] in MV_SET)
            rate = hits / cnt_po
            out[u] = {"q": [rate * Q_HOURS[q] for q in range(4)], "pi_s": rate, "pred_drop_6": 0.0, "pred_drop_d3": 0.0}
        return out

    if mode == "post_cip_ds2":
        pi_po, _, _, _, _ = _fit_ds2_ci(cnt_post_mat)
        for i, u in enumerate(TRAINS):
            out[u] = {"q": [pi_po[i] * Q_HOURS[q] for q in range(4)], "pi_s": pi_po[i], "pred_drop_6": 0.0, "pred_drop_d3": 0.0}
        return out

    if mode == "unanimous":
        for i, u in enumerate(TRAINS):
            td = data["trains"][u]
            q_hrs = [0.0] * 4
            hits = 0
            for b in range(n_sh):
                if td["pat_sh"][b] == 7:
                    q_hrs[q_sh[b]] += 4.0
                    hits += 1
            out[u] = {"q": q_hrs, "pi_s": hits / n_sh, "pred_drop_6": 0.0, "pred_drop_d3": 0.0}
        return out

    if mode == "d3_raw_over":
        d3_bg = sum(cnt_all_mat[i][1] / max(cnt_all_mat[i][0] + cnt_all_mat[i][1], 1.0) for i in range(len(TRAINS))) / len(TRAINS)
        for i, u in enumerate(TRAINS):
            td = data["trains"][u]
            d3_r = sum(1 for p in td["pat_sh"] if (p & 1) == 1) / n_sh
            pi_exc = max(0.0, d3_r - d3_bg)
            out[u] = {"q": [pi_exc * Q_HOURS[q] for q in range(4)], "pi_s": pi_exc, "pred_drop_6": 0.0, "pred_drop_d3": 0.0}
        return out

    if mode == "d3_naive_ratio":
        tot_11 = sum(cnt_all_mat[i][6] + cnt_all_mat[i][7] for i in range(len(TRAINS)))
        tot_111 = sum(cnt_all_mat[i][7] for i in range(len(TRAINS)))
        se3_naive = tot_111 / max(tot_11, 1.0)
        d3_bg = sum(cnt_all_mat[i][1] / max(cnt_all_mat[i][0] + cnt_all_mat[i][1], 1.0) for i in range(len(TRAINS))) / len(TRAINS)
        for i, u in enumerate(TRAINS):
            td = data["trains"][u]
            d3_r = sum(1 for p in td["pat_sh"] if (p & 1) == 1) / n_sh
            pi_est = max(0.0, (d3_r - d3_bg) / max(se3_naive - d3_bg, 0.05))
            out[u] = {"q": [pi_est * Q_HOURS[q] for q in range(4)], "pi_s": pi_est, "pred_drop_6": 0.0, "pred_drop_d3": 0.0}
        return out

    pi_s, pi_f_pre, pi_f_post, e0, e1, e2, p0, p2 = _fit_lca3_cip(
        cnt_pre_mat, cnt_post_mat, foul_model=foul_model, cip_mode=cip_mode
    )
    d3_e10 = sum((e1[b] - e0[b]) * D3_MASK[b] for b in range(8))
    for i, u in enumerate(TRAINS):
        dp_f = pi_f_pre[i] - pi_f_post[i]
        out[u] = {
            "q": [pi_s[i] * Q_HOURS[q] for q in range(4)],
            "pi_s": pi_s[i],
            "pi_f_pre": pi_f_pre[i],
            "pi_f_post": pi_f_post[i],
            "pred_drop_6": dp_f * (e1[6] - e0[6]),
            "pred_drop_d3": dp_f * d3_e10,
            "p2": p2,
        }
    return out


# ==============================================================================
# ASSEMBLE ALL GRADED FIGURES
# ==============================================================================
def _incumbent_2026_by_train(data):
    out = {}
    for u in TRAINS:
        td = data["trains"][u]
        b_inc = 0.0
        for q in range(4):
            vals = [td["comp_val"][i] for i in range(len(td["comp_val"])) if td["comp_q"][i] == q]
            b_inc += (sum(1 for x in vals if x > BORON_LIMIT) / len(vals)) * Q_HOURS[q]
        s_inc = sum(
            0.25 for i in range(32, len(td["x_in_15"]))
            if td["x_in_15"][i] > SCALING_X_LIM and td["y_out_15"][i] > SCALING_Y_LIM
        )
        st_inc = sum(4.0 for p in td["pat_sh"] if p in MV_SET)
        out[u] = (b_inc, s_inc, st_inc)
    return out


def assemble(r1, r2, r3, inc_2026, forward=True):
    members = {}
    c1_tot = c2_tot = c3_tot = q3_tot = cost_tot = ov_hrs = ov_cost = tot_26 = miss_abs = 0.0
    for u in TRAINS:
        bq, sq, stq = r1[u]["q"], r2[u]["q"], r3[u]["q"]
        sb26, ss26, sst26 = sum(bq), sum(sq), sum(stq)
        tot_26 += sb26 + ss26 + sst26
        bi, si, sti = inc_2026[u]
        miss_abs += abs(sb26 - bi) + abs(ss26 - si) + abs(sst26 - sti)

        if forward:
            b27, s27, st27 = project_2027(bq, sq, stq, u)
        else:
            b27, s27, st27 = bq, sq, stq
        hb, hs, hst = sum(b27), sum(s27), sum(st27)
        h_tot = hb + hs + hst
        members[u] = h_tot
        c1_tot += hb
        c2_tot += hs
        c3_tot += hst
        q3_tot += b27[2] + s27[2] + st27[2]
        uc = hb * TARIFF_BORON + hs * TARIFF_SCALING + hst * TARIFF_STRUCT
        cost_tot += uc
        if h_tot >= THRESHOLD:
            ov_hrs += h_tot
            ov_cost += uc

    diag_err_pct = 100.0 * miss_abs / max(tot_26, 1.0)
    return {
        "members": members,
        "C1_boron_2027": c1_tot,
        "C2_scaling_2027": c2_tot,
        "C3_struct_2027": c3_tot,
        "A_total_2027": c1_tot + c2_tot + c3_tot,
        "A_overhaul_2027": ov_hrs,
        "A_q3_2027": q3_tot,
        "A_cost_eur_k": cost_tot / 1000.0,
        "A_overhaul_eur_k": ov_cost / 1000.0,
        "A_diag_err_pct": diag_err_pct,
    }


def falsification_score(data, r1, r2, r3):
    # F1: Mean absolute mismatch on (V8/V4, r1(4)) across 8 trains
    f1_errs = []
    for u in TRAINS:
        _, st = _comp_moments(data["trains"][u])
        v8_v4_obs = st[8]["var"] / max(st[4]["var"], 1e-9)
        r1_4_obs = st[4]["r1"]
        f1_errs.append(abs(r1[u]["v8_v4_pred"] - v8_v4_obs) + abs(r1[u]["r1_4_pred"] - r1_4_obs))
    f1 = sum(f1_errs) / len(f1_errs)

    # F2: Mean intake-to-RO-feed conservative seawater conductivity RMS mismatch (mS/cm)
    f2 = sum(r2[u]["c_rms"] for u in TRAINS) / len(TRAINS)

    # F3: Pooled fleet pre-CIP vs post-CIP drop mismatch on (D1=1,D2=1,D3=0) and D3=1 (in percentage points)
    # Pooling across all 8 trains (11,680 pre-CIP vs 5,840 post-CIP blocks) suppresses per-train binomial noise
    obs_drop_6_sum = 0.0
    obs_drop_d3_sum = 0.0
    pred_drop_6_sum = 0.0
    pred_drop_d3_sum = 0.0
    for u in TRAINS:
        td = data["trains"][u]
        sp = sum(td["cnt_pre"])
        sq = sum(td["cnt_post"])
        p_pre = [x / sp for x in td["cnt_pre"]]
        p_post = [x / sq for x in td["cnt_post"]]
        obs_drop_6_sum += p_pre[6] - p_post[6]
        obs_drop_d3_sum += sum((p_pre[b] - p_post[b]) * D3_MASK[b] for b in range(8))
        pred_drop_6_sum += r3[u].get("pred_drop_6", 0.0)
        pred_drop_d3_sum += r3[u].get("pred_drop_d3", 0.0)
    f3 = 100.0 * (abs(pred_drop_6_sum - obs_drop_6_sum) / len(TRAINS) + abs(pred_drop_d3_sum - obs_drop_d3_sum) / len(TRAINS))
    return f1, f2, f3


def build_spec(seed=SEED):
    data = simulate_world(seed)
    inc_2026 = _incumbent_2026_by_train(data)

    r1_true = {u: {"q": data["trains"][u]["truth_boron_q"]} for u in TRAINS}
    r2_true = {u: {"q": data["trains"][u]["truth_scaling_q"]} for u in TRAINS}
    r3_true = {u: {"q": data["trains"][u]["truth_struct_q"]} for u in TRAINS}
    truth_asm = assemble(r1_true, r2_true, r3_true, inc_2026)

    r1_g = estimate_s1(data, mode="golden", kernel="ar1", obj="wls")
    r2_g = estimate_s2(data, mode="golden", flow_interp="linear", loss_fn="l2")
    r3_g = estimate_s3(data, mode="golden", foul_model="tied_d3_d12", cip_mode="free_per_train")
    gold_asm = assemble(r1_g, r2_g, r3_g, inc_2026)

    r1_h = estimate_s1(data, mode="direct")
    r2_h = estimate_s2(data, mode="direct")
    r3_h = estimate_s3(data, mode="direct")

    r1_rig = estimate_s1(data, mode="pooled")
    r2_rig = estimate_s2(data, mode="fixed_lag")
    r3_rig = estimate_s3(data, mode="ds2_ci")
    rig_asm = assemble(r1_rig, r2_rig, r3_rig, inc_2026)

    r1_over = estimate_s1(data, mode="iid_over")
    r2_over = estimate_s2(data, mode="comonotonic_over")
    r3_over = estimate_s3(data, mode="d3_raw_over")

    over_s1 = assemble(r1_over, r2_g, r3_g, inc_2026)
    over_s2 = assemble(r1_g, r2_over, r3_g, inc_2026)
    over_s3 = assemble(r1_g, r2_g, r3_over, inc_2026)

    lattice_asm = {}
    for n in (1, 2, 3):
        for comb in itertools.combinations(["S1", "S2", "S3"], n):
            key = "+".join(comb)
            a1 = r1_h if "S1" in comb else r1_g
            a2 = r2_h if "S2" in comb else r2_g
            a3 = r3_h if "S3" in comb else r3_g
            lattice_asm[key] = assemble(a1, a2, a3, inc_2026)

    # 20 defensible variants across S1, S2, S3
    variants = []
    s1_vars = [
        estimate_s1(data, mode="golden", kernel="ou", obj="wls"),
        estimate_s1(data, mode="golden", kernel="ar1", obj="ols"),
        estimate_s1(data, mode="golden", kernel="ar1", obj="r1_only"),
        estimate_s1(data, mode="golden", kernel="ar1", obj="wls", trim_pct=0.5),
        estimate_s1(data, mode="golden", kernel="ar1", obj="wls", lab_noise=False),
        estimate_s1(data, mode="golden", kernel="ar1", obj="wls", use_m8=False),
    ]
    for v1 in s1_vars:
        variants.append(assemble(v1, r2_g, r3_g, inc_2026))

    s2_vars = [
        estimate_s2(data, mode="golden", flow_interp="step", loss_fn="l2"),
        estimate_s2(data, mode="golden", flow_interp="midpoint", loss_fn="l2"),
        estimate_s2(data, mode="golden", flow_interp="linear", loss_fn="l1"),
        estimate_s2(data, mode="golden", flow_interp="linear", loss_fn="huber"),
        estimate_s2(data, mode="golden", flow_interp="linear", loss_fn="corr"),
        estimate_s2(data, mode="golden", flow_interp="linear", loss_fn="l2", trim_q=2.0),
    ]
    for v2 in s2_vars:
        variants.append(assemble(r1_g, v2, r3_g, inc_2026))

    s3_vars = [
        estimate_s3(data, mode="golden", foul_model="tied_d3_d12", cip_mode="common_clear"),
        estimate_s3(data, mode="golden", foul_model="free_d12", cip_mode="free_per_train"),
        estimate_s3(data, mode="golden", foul_model="free_d12", cip_mode="common_clear"),
        estimate_s3(data, mode="golden", foul_model="tied_d3_d12", cip_mode="free_per_train", post_window_blocks=24),
        estimate_s3(data, mode="golden", foul_model="tied_d3_d12", cip_mode="free_per_train", post_window_blocks=36),
    ]
    for v3 in s3_vars:
        variants.append(assemble(r1_g, r2_g, v3, inc_2026))

    variants.append(assemble(s1_vars[0], s2_vars[2], s3_vars[0], inc_2026))
    variants.append(assemble(s1_vars[1], s2_vars[3], s3_vars[3], inc_2026))
    variants.append(assemble(s1_vars[4], s2_vars[4], s3_vars[4], inc_2026))

    # Run routes
    gen_asm = assemble(r1_over, r2_over, r3_rig, inc_2026)
    r1_hedge = {
        u: {
            "q": [0.80 * r1_h[u]["q"][q] + 0.20 * r1_g[u]["q"][q] for q in range(4)],
            "v8_v4_pred": 0.8 + 0.2 * r1_g[u]["v8_v4_pred"],
            "r1_4_pred": 0.8 + 0.2 * r1_g[u]["r1_4_pred"],
        }
        for u in TRAINS
    }
    r2_hedge = {
        u: {
            "q": [0.80 * r2_h[u]["q"][q] + 0.20 * r2_g[u]["q"][q] for q in range(4)],
            "c_rms": 0.8 * r2_h[u]["c_rms"] + 0.2 * r2_g[u]["c_rms"],
        }
        for u in TRAINS
    }
    r3_hedge = {
        u: {
            "q": [0.80 * r3_h[u]["q"][q] + 0.20 * r3_g[u]["q"][q] for q in range(4)],
            "pred_drop_6": 0.2 * r3_g[u]["pred_drop_6"],
            "pred_drop_d3": 0.2 * r3_g[u]["pred_drop_d3"],
        }
        for u in TRAINS
    }
    hedge_asm = assemble(r1_hedge, r2_hedge, r3_hedge, inc_2026)

    r1_c4 = estimate_s1(data, mode="cutoff_4h")
    r2_cst = estimate_s2(data, mode="steady_flow")
    r3_cpmv = estimate_s3(data, mode="post_cip_mv")
    cut_asm = assemble(r1_c4, r2_cst, r3_cpmv, inc_2026)

    r1_ll = estimate_s1(data, mode="loglog")
    r1_cp = estimate_s1(data, mode="comp_param")
    r2_nv = estimate_s2(data, mode="nom_vol")
    r3_cpds = estimate_s3(data, mode="post_cip_ds2")
    r3_un = estimate_s3(data, mode="unanimous")
    r3_nr = estimate_s3(data, mode="d3_naive_ratio")

    extra_routes = {
        "cutoff:s1_4h_only": assemble(r1_c4, r2_g, r3_g, inc_2026),
        "cutoff:s1_comp_param": assemble(r1_cp, r2_g, r3_g, inc_2026),
        "cutoff:s1_loglog": assemble(r1_ll, r2_g, r3_g, inc_2026),
        "cutoff:s1_pooled": assemble(r1_rig, r2_g, r3_g, inc_2026),
        "cutoff:s2_fixed_lag": assemble(r1_g, r2_rig, r3_g, inc_2026),
        "cutoff:s2_nom_vol": assemble(r1_g, r2_nv, r3_g, inc_2026),
        "cutoff:s2_steady_flow": assemble(r1_g, r2_cst, r3_g, inc_2026),
        "cutoff:s3_post_cip_mv": assemble(r1_g, r2_g, r3_cpmv, inc_2026),
        "cutoff:s3_post_cip_ds2": assemble(r1_g, r2_g, r3_cpds, inc_2026),
        "cutoff:s3_ds2_ci": assemble(r1_g, r2_g, r3_rig, inc_2026),
        "cutoff:s3_unanimous": assemble(r1_g, r2_g, r3_un, inc_2026),
        "cutoff:s3_d3_naive_ratio": assemble(r1_g, r2_g, r3_nr, inc_2026),
        "hedge:history_2026_flat": assemble(r1_g, r2_g, r3_g, inc_2026, forward=False),
    }

    f2_floors = []
    for u in TRAINS:
        td = data["trains"][u]
        phi_t, _ = _build_phi_hat(td["q_flow_h"], "linear")
        xq = [p - td["v_eff_true"] for p in phi_t]
        c_al = interp_monotone(xq, phi_t, td["c_in_15"])
        n15 = len(phi_t)
        f2_floors.append(math.sqrt(sum((td["c_out_15"][i] - c_al[i]) ** 2 for i in range(32, n15)) / (n15 - 32)))
    f2_floor = sum(f2_floors) / len(f2_floors)

    def _comb_fal(x1, x2, x3):
        a, b, c = falsification_score(data, x1, x2, x3)
        # Equalized native-unit physical discrepancy: F1*10 + (F2 - floor)*5 + F3*3
        return a * 10.0 + max(0.0, b - f2_floor) * 5.0 + c * 3.0, (a, b, c)

    fal_g, fal_g_parts = _comb_fal(r1_g, r2_g, r3_g)
    fal_rivals = {}
    fal_detail = {"golden": (fal_g, fal_g_parts)}
    for label, (x1, x2, x3) in [
        ("direct", (r1_h, r2_h, r3_h)),
        ("rigorous", (r1_rig, r2_rig, r3_rig)),
        ("generous", (r1_over, r2_over, r3_rig)),
        ("hedge", (r1_hedge, r2_hedge, r3_hedge)),
        ("cutoff", (r1_c4, r2_cst, r3_cpmv)),
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
                "rigorous": rig_asm["members"][u],
            },
        }

    stumps_spec = {
        "S1": {
            "axis": "unit",
            "opens": "TR01",
            "said_out_loud": (
                "Lab boron assays are 4-hour weekday and 8-hour weekend flow-proportional composites "
                "whose averaging collapses 1-hour variance by each train's own correlation scale."
            ),
            "steps_left": 4,
            "precedents": ["L22", "L56", "L57"],
            "sides": {"over": over_s1["members"]},
        },
        "S2": {
            "axis": "when",
            "opens": "TR02",
            "said_out_loud": (
                "Intake precursor and RO-feed stress sensors see the same seawater parcel separated by "
                "an unobserved effective hydraulic holdup volume under time-varying tariff flow."
            ),
            "steps_left": 4,
            "precedents": ["L26", "L28", "N07", "N30"],
            "sides": {"over": over_s2["members"]},
        },
        "S3": {
            "axis": "what",
            "opens": "TR03",
            "said_out_loud": (
                "Two shift alarms co-fire on reversible bio-fouling that partially clears after CIP "
                "washes while true structural membrane faults persist across CIP without autopsy labels."
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
                "No shipped file observes 1-hour boron grab samples, true parcel scaling incidents, or "
                "destructive membrane autopsies on any train or reference slice; forcing rests on the "
                "three native-unit physical falsification checks F1-F3."
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
                "rigorous": rig_asm[fid],
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
    figures_spec.append(_non_member_fig("A_cost_eur_k", "ask", "Ask3_cost_total"))
    figures_spec.append(_non_member_fig("A_overhaul_eur_k", "ask", "Ask3_cost_overhaul"))
    figures_spec.append(_non_member_fig("A_diag_err_pct", "ask", "Ask4_diag_err"))

    spec = {
        "task": "task28",
        "call": "lines",
        "members": members_spec,
        "stumps": stumps_spec,
        "lattice": lattice_spec,
        "falsification": {
            "check": (
                "Three native-unit physical conservation/invariance checks with zero anomaly labels: "
                "F1 composite dispersion & lag-1 autocorrelation (V8/V4, r1(4)); F2 intake-to-RO-feed "
                "conservative seawater conductivity RMS (mS/cm); F3 pooled pre/post-CIP invariance on (1,1,0) and D3=1 (pp)."
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
        "inc_2026": inc_2026,
        "truth_asm": truth_asm,
        "gold_asm": gold_asm,
        "rig_asm": rig_asm,
        "lattice_asm": lattice_asm,
        "extra_routes": extra_routes,
        "over": {"S1": over_s1, "S2": over_s2, "S3": over_s3},
        "fal_detail": fal_detail,
        "f2_floor": f2_floor,
        "r1_g": r1_g,
        "r2_g": r2_g,
        "r3_g": r3_g,
        "variants": variants,
    }
    return spec, diag


def run_forcing_perturbations(diag):
    r1_g, r2_g, r3_g, inc_2026 = diag["r1_g"], diag["r2_g"], diag["r3_g"], diag["inc_2026"]
    g_call = tuple(diag["gold_asm"]["members"][u] >= THRESHOLD for u in TRAINS)
    results = []
    for name, f1, f2, f3 in [
        ("S1_boron_-20%", 0.80, 1.0, 1.0),
        ("S1_boron_+20%", 1.20, 1.0, 1.0),
        ("S2_scaling_-20%", 1.0, 0.80, 1.0),
        ("S2_scaling_+20%", 1.0, 1.20, 1.0),
        ("S3_struct_-20%", 1.0, 1.0, 0.80),
        ("S3_struct_+20%", 1.0, 1.0, 1.20),
    ]:
        p1 = {u: {"q": [x * f1 for x in r1_g[u]["q"]]} for u in TRAINS}
        p2 = {u: {"q": [x * f2 for x in r2_g[u]["q"]]} for u in TRAINS}
        p3 = {u: {"q": [x * f3 for x in r3_g[u]["q"]]} for u in TRAINS}
        asm = assemble(p1, p2, p3, inc_2026)
        c = tuple(asm["members"][u] >= THRESHOLD for u in TRAINS)
        min_ov = min(asm["members"][u] for u in TRAINS if diag["gold_asm"]["members"][u] >= THRESHOLD)
        max_mo = max(asm["members"][u] for u in TRAINS if diag["gold_asm"]["members"][u] < THRESHOLD)
        results.append((name, c == g_call, min_ov, max_mo))
    return results


if __name__ == "__main__":
    spec, diag = build_spec(SEED)
    print("=== PHYSICAL DIAGNOSTICS (SEED %d) ===" % SEED)
    print("S3 fitted p2 =", [round(x, 3) for x in diag["r3_g"]["TR01"]["p2"]], "true =", P_STRUCT)
    print("Train | Truth  | Golden | Boron27 | Scal27 | Stru27 | lam_hat (true) | V_eff_hat (true) | pi_s_hat (true)")
    for u in TRAINS:
        td = diag["data"]["trains"][u]
        b27, s27, st27 = project_2027(diag["r1_g"][u]["q"], diag["r2_g"][u]["q"], diag["r3_g"][u]["q"], u)
        print(
            "%-5s | %6.1f | %6.1f | %7.1f | %6.1f | %6.1f | %6.2f (%5.2f) | %6.1f (%5.1f)    | %.4f (%.4f)"
            % (
                u,
                diag["truth_asm"]["members"][u],
                diag["gold_asm"]["members"][u],
                sum(b27),
                sum(s27),
                sum(st27),
                diag["r1_g"][u]["lam"],
                WORLD[u]["b_lam"],
                diag["r2_g"][u]["v_hat"],
                td["v_eff_true"],
                diag["r3_g"][u]["pi_s"],
                WORLD[u]["pi_struct"],
            )
        )
    print("\n=== FALSIFICATION BREAKDOWN (F2 floor %.3f mS/cm) ===" % diag["f2_floor"])
    for k, (sc, (a, b, c)) in diag["fal_detail"].items():
        print("  %-10s total=%7.3f  | F1=%.4f  F2=%.3f mS/cm  F3=%.3f pp" % (k, sc, a, b, c))
    print("\n=== EXTRA CUTOFF & OVER-CORRECTION ROUTES ===")
    gcall = corelib._calls(spec, {u: spec["members"][u]["golden"] for u in TRAINS})
    for k, v in list(diag["extra_routes"].items()) + [(f"OVER_{s}", diag["over"][s]) for s in ("S1", "S2", "S3")]:
        cc = corelib._calls(spec, v["members"])
        flagged = [TRAINS[i] for i, b in enumerate(cc) if b]
        print("  %-26s %-5s flagged=%-28s  %s" % (
            k,
            "RIGHT" if cc == gcall else "WRONG",
            ",".join(flagged),
            " ".join("%s:%.0f" % (u, v["members"][u]) for u in TRAINS),
        ))
    print("\n=== +/-20% FORCING PERTURBATIONS ===")
    for name, ok, min_ov, max_mo in run_forcing_perturbations(diag):
        print("  %-18s %-4s  min_overhaul=%.1f  max_monitor=%.1f" % (name, "HOLD" if ok else "FLIP", min_ov, max_mo))
    print()
    sys.exit(corelib.run(spec))
