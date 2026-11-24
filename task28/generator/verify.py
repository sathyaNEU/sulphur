#!/usr/bin/env python3
"""Independent end-to-end verifier for task28 (v3).

Reads ONLY target.zip, golden.zip, and submission.md (never imports core.py, pack.py, analysis.py,
or reads figures.json / DESIGN_NOTE.md). Recomputes every graded figure across all 4 physical modes
from scratch using numpy/scipy and verifies exact agreement with golden CSV, golden XLSX
(evaluated via LibreOffice Calc), and submission.md.
"""
import csv
import datetime as dt
import json
import math
import os
import shutil
import subprocess
import tempfile
import zipfile

import numpy as np
import openpyxl
from scipy.optimize import minimize
from scipy.special import erfc

TASK_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UTC = dt.timezone.utc
START = dt.datetime(2026, 1, 1, 0, 0, 0, tzinfo=UTC)
D0 = dt.date(2026, 1, 1)


def _norm_sf(z):
    return 0.5 * erfc(np.asarray(z, dtype=float) / math.sqrt(2.0))


def _ar1_fg(phi, m):
    s = sum((m - d) * (phi ** d) for d in range(1, m))
    f_m = (m + 2.0 * s) / (m * m)
    g_m = 0.0
    for i in range(m):
        for j in range(m):
            g_m += phi ** (m + j - i)
    g_m /= (m * m)
    return f_m, g_m


def _indep_dist(p):
    p1, p2, p3 = p
    out = np.empty(8, dtype=float)
    for k in range(8):
        b1, b2, b3 = (k >> 2) & 1, (k >> 1) & 1, k & 1
        out[k] = (p1 if b1 else 1.0 - p1) * (p2 if b2 else 1.0 - p2) * (p3 if b3 else 1.0 - p3)
    return out


def _parse_date(s):
    s = s.strip()
    if "/" in s:
        d, m, y = s.split("/")
        return dt.date(int(y), int(m), int(d))
    return dt.date.fromisoformat(s[:10])


def _parse_ts(s):
    s = s.strip()
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    return dt.datetime.fromisoformat(s).astimezone(UTC)


def main():
    work = tempfile.mkdtemp(prefix="verify-t28-v3-")
    try:
        tdir = os.path.join(work, "target")
        gdir = os.path.join(work, "golden")
        os.makedirs(tdir)
        os.makedirs(gdir)
        with zipfile.ZipFile(os.path.join(TASK_DIR, "target.zip")) as z:
            z.extractall(tdir)
        with zipfile.ZipFile(os.path.join(TASK_DIR, "golden.zip")) as z:
            z.extractall(gdir)

        # 1. Asset register, SCADA config, and 2027 Operating Plan
        tag_map = {}
        trains = []
        bays = {"North": [], "South": []}
        with open(os.path.join(tdir, "train_asset_register.csv"), encoding="utf-8") as f:
            for r in csv.DictReader(f):
                u = r["train_id"].strip()
                trains.append(u)
                tag_map[u] = u
                tag_map[r["legacy_tag"].strip()] = u
                bays[r["plant_bay"].strip()].append(u)

        cfg = json.load(open(os.path.join(tdir, "scada_bay_config_2026.json"), encoding="utf-8"))
        tds_meter_sd = float(cfg["inline_sensor_qa"]["bay_collector_tds_repeatability_mg_l"])

        q_map = {"2027-Q1": 0, "2027-Q2": 1, "2027-Q3": 2, "2027-Q4": 3}
        sr = {u: [0.0] * 4 for u in trains}
        bt = [0.0] * 4
        sc = [0.0] * 4
        ts_f = [0.0] * 4
        qh = [0] * 4
        with open(os.path.join(tdir, "operating_plan_2027.csv"), encoding="utf-8") as f:
            for r in csv.DictReader(f):
                u = r["train_id"].strip()
                q = q_map[r["quarter"].strip()]
                sr[u][q] = float(r["dispatch_duty_ratio_2027"])
                bt[q] = float(r["boron_thermal_factor_2027"])
                sc[q] = float(r["scaling_recovery_factor_2027"])
                ts_f[q] = float(r["salinity_thermal_factor_2027"])
                qh[q] = int(r["calendar_hours_2026"])

        q_edges = [0]
        for h in qh:
            q_edges.append(q_edges[-1] + h)
        q_of_h = np.zeros(sum(qh), dtype=int)
        for q in range(4):
            q_of_h[q_edges[q]:q_edges[q + 1]] = q
        q_of_15 = np.repeat(q_of_h, 4)

        # 2. Hourly SCADA feed flow
        q_flow = {u: np.full(8760, np.nan) for u in trains}
        cache_h = {}
        with open(os.path.join(tdir, "train_hydraulics_hourly_2026.csv"), encoding="utf-8") as f:
            rd = csv.reader(f)
            next(rd)
            for row in rd:
                ts, u = row[0], row[1]
                idx = cache_h.get(ts)
                if idx is None:
                    idx = int((_parse_ts(ts) - START).total_seconds() // 3600)
                    cache_h[ts] = idx
                if np.isnan(q_flow[u][idx]):
                    q_flow[u][idx] = float(row[2]) * (3.6 if row[3].strip() == "L/s" else 1.0)

        # 3. S1: Spiegler-Kedem mass-flux conservation + flux-space AR(1) 4h/8h deconvolution
        span = {}
        with open(os.path.join(tdir, "autosampler_schedule_2026.csv"), encoding="utf-8") as f:
            for r in csv.DictReader(f):
                span[(tag_map[r["train_code"].strip()], (_parse_date(r["schedule_date"]) - D0).days)] = int(r["bottle_span_hours"])

        best_b = {}
        with open(os.path.join(tdir, "permeate_boron_composites_2026.csv"), encoding="utf-8") as f:
            for r in csv.DictReader(f):
                sid = r["sample_id"].strip()
                rev = int(r["qa_revision"])
                u = tag_map[r["train_code"].strip()]
                day = (_parse_date(r["collection_date"]) - D0).days
                slot = int(r["carousel_slot"]) - 1
                val = float(r["boron_conc"]) / (1000.0 if r["unit"].strip() == "ug/L" else 1.0)
                if sid not in best_b or rev > best_b[sid][0]:
                    best_b[sid] = (rev, u, day, slot, val)

        lam_grid = np.exp(np.linspace(math.log(0.25), math.log(30.0), 220))
        b26 = {}
        for u in trains:
            rows_u = sorted([x for x in best_b.values() if x[1] == u], key=lambda x: (x[2], x[3]))
            ms = np.array([span[(u, x[2])] for x in rows_u], dtype=int)
            ds = np.array([x[2] for x in rows_u], dtype=int)
            vs = np.array([x[4] for x in rows_u], dtype=float)
            h0s = np.array([x[2] * 24 + x[3] * span[(u, x[2])] for x in rows_u], dtype=int)
            qs = q_of_h[h0s]
            qbars = np.array([float(np.mean(q_flow[u][h0:h0 + m])) for h0, m in zip(h0s, ms)], dtype=float)

            ym = qbars * vs
            X = np.zeros((len(vs), 5), dtype=float)
            for q in range(4):
                X[qs == q, q] = qbars[qs == q]
            X[:, 4] = 1.0
            coef, *_ = np.linalg.lstsq(X, ym, rcond=None)
            alphas = coef[:4]
            mu_j = float(coef[4])
            res_j = ym - X @ coef
            nv_j = (qbars ** 2) * (0.004 ** 2)

            st = {}
            for m in (4, 8):
                idx = np.where(ms == m)[0]
                vm = max(1e-7, float(np.var(res_j[idx], ddof=1)) - float(np.mean(nv_j[idx])))
                pa, pb = [], []
                for k in range(len(idx) - 1):
                    i1, i2 = int(idx[k]), int(idx[k + 1])
                    if i2 == i1 + 1 and ds[i2] == ds[i1]:
                        pa.append(res_j[i1])
                        pb.append(res_j[i2])
                pa, pb = np.array(pa), np.array(pb)
                cm = float(np.mean(pa * pb))
                st[m] = (vm, cm)
            v4, c4 = st[4]
            v8, c8 = st[8]
            obs = [v4, c4, v8, c8]
            wts = [3.0 / (v4 * v4), 3.0 / (v4 * v4), 1.0 / (v8 * v8), 0.7 / (v8 * v8)]
            best_loss, best_sd = 1e30, 15.0
            for lam in lam_grid:
                phi = math.exp(-1.0 / float(lam))
                f4, g4 = _ar1_fg(phi, 4)
                f8, g8 = _ar1_fg(phi, 8)
                mod = [f4, g4, f8, g8]
                s2 = max(1e-9, sum(w * o * m for w, o, m in zip(wts, obs, mod)) / sum(w * m * m for w, m in zip(wts, mod)))
                loss = sum(w * (o - s2 * m) ** 2 for w, o, m in zip(wts, obs, mod))
                if loss < best_loss:
                    best_loss, best_sd = loss, math.sqrt(s2)
            mu_h = alphas[q_of_h] + mu_j / q_flow[u]
            sd_h = best_sd / q_flow[u]
            p_h = _norm_sf((0.50 - mu_h) / np.maximum(sd_h, 1e-6))
            b26[u] = [float(np.sum(p_h[q_of_h == q])) for q in range(4)]

        # 4. S2: Variable-flow cumulative-volume two-path DAF/DMF hydraulic mixing
        c_in = {u: np.full(35040, np.nan) for u in trains}
        x_in = {u: np.full(35040, np.nan) for u in trains}
        c_out = {u: np.full(35040, np.nan) for u in trains}
        y_out = {u: np.full(35040, np.nan) for u in trains}
        cache_15 = {}
        with open(os.path.join(tdir, "intake_chemistry_15m_2026.csv"), encoding="utf-8") as f:
            rd = csv.reader(f)
            next(rd)
            for row in rd:
                ts, u = row[0], row[1]
                idx = cache_15.get(ts)
                if idx is None:
                    idx = int((_parse_ts(ts) - START).total_seconds() // 900)
                    cache_15[ts] = idx
                if np.isnan(c_in[u][idx]):
                    c_in[u][idx] = float(row[2])
                    x_in[u][idx] = float(row[3])
        with open(os.path.join(tdir, "ro_feed_header_15m_2026.csv"), encoding="utf-8") as f:
            rd = csv.reader(f)
            next(rd)
            for row in rd:
                ts, u = row[0], row[1]
                idx = cache_15[ts]
                if np.isnan(c_out[u][idx]):
                    c_out[u][idx] = float(row[2])
                    y_out[u][idx] = float(row[3])

        s26 = {}
        hours = np.arange(8760, dtype=float)
        t15_h = np.arange(35040, dtype=float) / 4.0
        sl = slice(32, None)
        q_sl = q_of_15[sl]
        vf_grid = np.arange(200.0, 521.0, 40.0)
        vm_grid = np.arange(960.0, 1601.0, 40.0)
        for u in trains:
            q15 = np.interp(t15_h, hours, q_flow[u])
            phi = np.cumsum(0.25 * q15)
            phi_sl = phi[sl]
            y_c = c_out[u][sl]
            cf_c = {vf: np.interp(phi_sl - vf, phi, c_in[u]) for vf in vf_grid}
            cm_c = {vm: np.interp(phi_sl - vm, phi, c_in[u]) for vm in vm_grid}
            best = (1e30, 0.0, 360.0, 1280.0)
            for vf in vf_grid:
                cf = cf_c[vf]
                for vm in vm_grid:
                    if vm - vf < 350.0:
                        continue
                    cm = cm_c[vm]
                    d = cf - cm
                    f_h = max(0.0, min(0.50, float(np.dot(y_c - cm, d)) / max(float(np.dot(d, d)), 1e-9)))
                    mse = float(np.mean((y_c - (cm + f_h * d)) ** 2))
                    if mse < best[0]:
                        best = (mse, f_h, float(vf), float(vm))
            _, _, vf0, vm0 = best
            vf_f = np.arange(max(160.0, vf0 - 40.0), min(560.0, vf0 + 41.0), 8.0)
            vm_f = np.arange(max(860.0, vm0 - 40.0), min(1640.0, vm0 + 41.0), 8.0)
            cf_fm = {vf: np.interp(phi_sl - vf, phi, c_in[u]) for vf in vf_f}
            cm_fm = {vm: np.interp(phi_sl - vm, phi, c_in[u]) for vm in vm_f}
            for vf in vf_f:
                cf = cf_fm[vf]
                for vm in vm_f:
                    if vm - vf < 300.0:
                        continue
                    cm = cm_fm[vm]
                    d = cf - cm
                    f_h = max(0.0, min(0.50, float(np.dot(y_c - cm, d)) / max(float(np.dot(d, d)), 1e-9)))
                    mse = float(np.mean((y_c - (cm + f_h * d)) ** 2))
                    if mse < best[0]:
                        best = (mse, f_h, float(vf), float(vm))
            _, f_hat, vf_hat, vm_hat = best
            if f_hat < 0.04:
                f_hat = 0.0
            x_arr = f_hat * np.interp(phi_sl - vf_hat, phi, x_in[u]) + (1.0 - f_hat) * np.interp(phi_sl - vm_hat, phi, x_in[u])
            hit = (x_arr > 1.50) & (y_out[u][sl] > 1.50)
            s26[u] = [float(0.25 * np.sum(hit & (q_sl == q))) for q in range(4)]

        # 5. S3: Continuous post-CIP fouling re-growth kinetic LCA (1-hour cadence, exact converged joint MLE)
        triples_all = np.zeros((8, 8760), dtype=np.int32)
        u_idx = {u: i for i, u in enumerate(trains)}
        sh_cache = {}
        with open(os.path.join(tdir, "shift_diagnostics_2026.csv"), encoding="utf-8") as f:
            rd = csv.reader(f)
            next(rd)
            for row in rd:
                ts, u = row[0], row[1]
                h = sh_cache.get(ts)
                if h is None:
                    h = int(round((_parse_ts(ts) - START).total_seconds() / 3600.0))
                    sh_cache[ts] = h
                triples_all[u_idx[u], h] = (int(row[3]) << 2) | (int(row[4]) << 1) | int(row[5])

        cip_by_u = {u: [] for u in trains}
        with open(os.path.join(tdir, "cip_wash_log_2026.csv"), encoding="utf-8") as f:
            for r in csv.DictReader(f):
                u = tag_map[r["train_code"].strip()]
                h_ev = int(round((_parse_ts(r["wash_completed_lisbon"]) - START).total_seconds() / 3600.0))
                cip_by_u[u].append((h_ev, r["chemical_stage"].strip()))

        dt_alk_all = np.zeros((8, 8760), dtype=float)
        dt_acid_all = np.zeros((8, 8760), dtype=float)
        for ui, u in enumerate(trains):
            evs = sorted(cip_by_u[u], key=lambda x: x[0])
            cur_alk = max(h_ev for h_ev, rec in evs if h_ev < 0 and rec == "CIP_ALK_pH11")
            cur_acid = max(h_ev for h_ev, rec in evs if h_ev < 0 and rec == "CIP_ACID_pH2")
            ev_map = {h_ev: rec for h_ev, rec in evs if h_ev >= 0}
            for h in range(8760):
                if h in ev_map:
                    if ev_map[h] == "CIP_ALK_pH11":
                        cur_alk = h
                    else:
                        cur_acid = h
                dt_alk_all[ui, h] = float(h - cur_alk)
                dt_acid_all[ui, h] = float(h - cur_acid)

        # Static 3-class EM warm start + per-train 5-D warm start + exact converged joint 49-D L-BFGS-B MLE
        p_cl = np.array([0.02, 0.01, 0.01])
        p_fb = np.array([0.65, 0.85, 0.02])
        p_ms = np.array([0.80, 0.20, 0.65])
        pi3 = np.full((8, 3), [0.75, 0.12, 0.13])
        d1_all = ((triples_all >> 2) & 1).astype(float)
        d2_all = ((triples_all >> 1) & 1).astype(float)
        d3_all = (triples_all & 1).astype(float)
        for _ in range(60):
            E = np.vstack([_indep_dist(p_cl), _indep_dist(p_fb), _indep_dist(p_ms)])
            num_c, den_c = np.zeros((3, 3)), np.zeros(3)
            for ui in range(8):
                tr_i = triples_all[ui]
                lik = pi3[ui][:, None] * E[:, tr_i]
                post = lik / np.maximum(np.sum(lik, axis=0, keepdims=True), 1e-15)
                pi3[ui] = np.mean(post, axis=1)
                for c in range(3):
                    den_c[c] += float(np.sum(post[c]))
                    num_c[c] += [float(np.sum(post[c] * d1_all[ui])), float(np.sum(post[c] * d2_all[ui])), float(np.sum(post[c] * d3_all[ui]))]
            p_cl = np.clip(num_c[0] / max(den_c[0], 1.0), 0.001, 0.20)
            p_fb = np.clip(num_c[1] / max(den_c[1], 1.0), 0.001, 0.999)
            p_ms = np.clip(num_c[2] / max(den_c[2], 1.0), 0.001, 0.999)

        em_init = np.vstack([p_cl, p_fb, p_ms])
        E_init = np.vstack([_indep_dist(p_cl), _indep_dist(p_fb), _indep_dist(p_ms)])
        t_lo, t_hi = math.log(0.1), math.log(5000.0)
        init_pars = np.zeros((8, 5), dtype=float)
        for ui in range(8):
            tr_i = triples_all[ui]
            e0, e1, e2 = E_init[0, tr_i], E_init[1, tr_i], E_init[2, tr_i]
            da, dc = dt_alk_all[ui], dt_acid_all[ui]
            bnds_u = [(0.0, 0.48), (0.0, 0.48), (0.0, 0.35), (t_lo, t_hi), (t_lo, t_hi)]

            def _nll_u(x):
                pb, pm, ps, ltb, ltm = x
                ub = da / math.exp(ltb)
                um = dc / math.exp(ltm)
                eb, em_v = np.exp(-ub), np.exp(-um)
                gb, gm = 1.0 - eb, 1.0 - em_v
                wb, wms = pb * gb, ps + pm * gm
                wc = 1.0 - wb - wms
                if np.any(wc <= 1e-6):
                    return 1e12, np.zeros(5)
                lik = wc * e0 + wb * e1 + wms * e2
                nll = -float(np.sum(np.log(lik)))
                inv_l = -1.0 / lik
                d_wb, d_wms = inv_l * (e1 - e0), inv_l * (e2 - e0)
                g = np.array([
                    float(np.sum(d_wb * gb)),
                    float(np.sum(d_wms * gm)),
                    float(np.sum(d_wms)),
                    float(np.sum(d_wb * (pb * (-ub * eb)))),
                    float(np.sum(d_wms * (pm * (-um * em_v)))),
                ])
                return nll, g

            best_u = None
            p2t = max(0.02, float(pi3[ui, 2]))
            for s_ps, s_tm in ((0.002, 27.0), (0.002, 54.0), (min(0.12, p2t * 0.5), 45.0)):
                x0 = [min(0.47, max(1e-4, float(pi3[ui, 1]) * 1.15)), min(0.47, max(1e-4, max(0.01, p2t - s_ps))), s_ps, math.log(45.0), math.log(s_tm)]
                r = minimize(_nll_u, x0, jac=True, bounds=bnds_u, method="L-BFGS-B", options={"ftol": 1e-13, "gtol": 1e-8})
                if best_u is None or r.fun < best_u.fun:
                    best_u = r
            init_pars[ui] = best_u.x

        bits = np.array([[(k >> 2) & 1, (k >> 1) & 1, k & 1] for k in range(8)], dtype=float)
        tr_flat = triples_all.ravel()

        def _joint_nll(theta):
            em = theta[:9].reshape(3, 3)
            P1 = em[:, None, :] * bits[None, :, :] + (1.0 - em[:, None, :]) * (1.0 - bits[None, :, :])
            E = np.prod(P1, axis=2)
            dE = np.empty((3, 8, 3), dtype=float)
            dE[:, :, 0] = (2.0 * bits[:, 0] - 1.0)[None, :] * P1[:, :, 1] * P1[:, :, 2]
            dE[:, :, 1] = (2.0 * bits[:, 1] - 1.0)[None, :] * P1[:, :, 0] * P1[:, :, 2]
            dE[:, :, 2] = (2.0 * bits[:, 2] - 1.0)[None, :] * P1[:, :, 0] * P1[:, :, 1]
            pars = theta[9:].reshape(8, 5)
            pb, pm, ps, ltb, ltm = pars[:, 0], pars[:, 1], pars[:, 2], pars[:, 3], pars[:, 4]
            ub = dt_alk_all / np.exp(ltb)[:, None]
            um = dt_acid_all / np.exp(ltm)[:, None]
            eb, em_v = np.exp(-ub), np.exp(-um)
            gb, gm = 1.0 - eb, 1.0 - em_v
            wb, wms = pb[:, None] * gb, ps[:, None] + pm[:, None] * gm
            wc = 1.0 - wb - wms
            if np.any(wc <= 1e-6):
                return 1e12, np.zeros_like(theta)
            e0, e1, e2 = E[0, triples_all], E[1, triples_all], E[2, triples_all]
            lik = wc * e0 + wb * e1 + wms * e2
            nll = -float(np.sum(np.log(lik)))
            inv_l = -1.0 / lik
            grad = np.zeros_like(theta)
            d_wb, d_wms = inv_l * (e1 - e0), inv_l * (e2 - e0)
            gp = np.empty((8, 5), dtype=float)
            gp[:, 0] = np.sum(d_wb * gb, axis=1)
            gp[:, 1] = np.sum(d_wms * gm, axis=1)
            gp[:, 2] = np.sum(d_wms, axis=1)
            gp[:, 3] = np.sum(d_wb * (pb[:, None] * (-ub * eb)), axis=1)
            gp[:, 4] = np.sum(d_wms * (pm[:, None] * (-um * em_v)), axis=1)
            grad[9:] = gp.ravel()
            w_all = np.vstack([(inv_l * wc).ravel(), (inv_l * wb).ravel(), (inv_l * wms).ravel()])
            g_E = np.vstack([np.bincount(tr_flat, weights=w_all[c], minlength=8) for c in range(3)])
            grad[:9] = np.einsum("ck,ckj->cj", g_E, dE).ravel()
            return nll, grad

        bnds_j = [
            (1e-4, 0.25), (1e-4, 0.25), (1e-4, 0.25),
            (0.20, 0.9999), (0.30, 0.9999), (1e-4, 0.35),
            (0.30, 0.9999), (1e-4, 0.60), (0.20, 0.9999),
        ] + [(0.0, 0.48), (0.0, 0.48), (0.0, 0.35), (t_lo, t_hi), (t_lo, t_hi)] * 8
        opt_j = minimize(
            _joint_nll, np.concatenate([em_init.ravel(), init_pars.ravel()]),
            jac=True, bounds=bnds_j, method="L-BFGS-B",
            options={"ftol": 1e-14, "gtol": 1e-8, "maxiter": 1000, "maxcor": 25},
        )
        pi_s = opt_j.x[9:].reshape(8, 5)[:, 2]
        st26 = {u: [float(pi_s[ui] * qh[q]) for q in range(4)] for ui, u in enumerate(trains)}

        # 6. S4: Shared-bay permeate collector TDS heteroscedastic variance-component deconvolution
        bay_tds = {b: np.full(8760, np.nan) for b in ("North", "South")}
        with open(os.path.join(tdir, "bay_permeate_tds_hourly_2026.csv"), encoding="utf-8") as f:
            rd = csv.reader(f)
            next(rd)
            for row in rd:
                idx = cache_h[row[0]]
                b = row[1]
                if np.isnan(bay_tds[b][idx]):
                    bay_tds[b][idx] = float(row[3])

        t26 = {}
        mv = tds_meter_sd ** 2
        for bname, members in bays.items():
            q_mat = np.column_stack([q_flow[u] for u in members])
            w_mat = q_mat / np.sum(q_mat, axis=1, keepdims=True)
            y = bay_tds[bname]
            X = np.zeros((8760, 16), dtype=float)
            for q in range(4):
                m = q_of_h == q
                X[m, 4 * q:4 * q + 4] = w_mat[m]
            coef, *_ = np.linalg.lstsq(X, y, rcond=None)
            mu_q_mat = coef.reshape(4, 4)
            r2 = (y - X @ coef) ** 2
            w2 = w_mat ** 2

            def _nll_v(lv):
                s2 = np.exp(lv)
                v = mv + w2 @ s2
                nll = 0.5 * float(np.sum(np.log(v) + r2 / v))
                grad = 0.5 * s2 * (w2.T @ ((1.0 - r2 / v) / v))
                return nll, grad

            opt = minimize(_nll_v, np.full(4, math.log(900.0)), jac=True, bounds=[(math.log(25.0), math.log(15000.0))] * 4, method="L-BFGS-B", options={"ftol": 1e-13, "gtol": 1e-10})
            sd_vec = np.sqrt(np.exp(opt.x))
            for ti, u in enumerate(members):
                t26[u] = [float(qh[q] * _norm_sf((450.0 - mu_q_mat[q, ti]) / max(sd_vec[ti], 1e-6))) for q in range(4)]

        # 7. Project 2026 -> 2027 via Annex A & compute Clause 4.3 energy penalty (MWh)
        recomp = {}
        for u in trains:
            b27 = [b26[u][q] * bt[q] * sr[u][q] for q in range(4)]
            s27 = [s26[u][q] * sc[q] * sr[u][q] for q in range(4)]
            st27 = [st26[u][q] * sr[u][q] for q in range(4)]
            t27 = [t26[u][q] * ts_f[q] * sr[u][q] for q in range(4)]
            tot = sum(b27) + sum(s27) + sum(st27) + sum(t27)
            q3 = b27[2] + s27[2] + st27[2] + t27[2]
            e_mwh = (sum(b27) * 420.0 + sum(s27) * 360.0 + sum(st27) * 540.0 + sum(t27) * 300.0) / 1000.0
            recomp[u] = {
                "boron": sum(b27), "scaling": sum(s27), "struct": sum(st27), "tds": sum(t27),
                "total": tot, "q3": q3, "energy": e_mwh,
                "desig": "OVERHAUL" if tot >= 400.0 else "MONITOR",
            }

        # 8. Compare against golden CSV, Calc-evaluated golden XLSX, and submission.md
        csv_rows = list(csv.DictReader(open(os.path.join(gdir, "barlavento_train_diagnostics_2027.csv"), encoding="utf-8")))
        assert len(csv_rows) == 8
        for r in csv_rows:
            u = r["train_id"]
            rc = recomp[u]
            assert r["designation"] == rc["desig"], f"Designation mismatch on {u}: {r['designation']} vs {rc['desig']}"
            assert abs(float(r["boron_2027_h"]) - rc["boron"]) < 0.25, f"Boron mismatch {u}"
            assert abs(float(r["scaling_2027_h"]) - rc["scaling"]) < 0.25, f"Scaling mismatch {u}"
            assert abs(float(r["struct_2027_h"]) - rc["struct"]) < 0.25, f"Struct mismatch {u}"
            assert abs(float(r["tds_2027_h"]) - rc["tds"]) < 0.25, f"TDS mismatch {u}"
            assert abs(float(r["total_2027_h"]) - rc["total"]) < 0.30, f"Total mismatch {u}"
            assert abs(float(r["q3_2027_h"]) - rc["q3"]) < 0.25, f"Q3 mismatch {u}"
            assert abs(float(r["energy_2027_mwh"]) - rc["energy"]) < 0.15, f"Energy mismatch {u}"

        prof = "file://" + os.path.join(work, "lo_prof")
        xlsx_in = os.path.join(gdir, "barlavento_swro_overhaul_plan_2027.xlsx")
        subprocess.run(
            ["soffice", "--headless", f"-env:UserInstallation={prof}", "--convert-to", "xlsx", "--outdir", work, xlsx_in],
            check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        wb = openpyxl.load_workbook(os.path.join(work, "barlavento_swro_overhaul_plan_2027.xlsx"), data_only=True)
        ws = wb["Overhaul_Triage_2027"]
        c1 = sum(recomp[u]["boron"] for u in trains)
        c2 = sum(recomp[u]["scaling"] for u in trains)
        c3 = sum(recomp[u]["struct"] for u in trains)
        c4 = sum(recomp[u]["tds"] for u in trains)
        tot_all = c1 + c2 + c3 + c4
        e_all = sum(recomp[u]["energy"] for u in trains)
        assert abs(float(ws["C16"].value) - c1) < 0.30
        assert abs(float(ws["D16"].value) - c2) < 0.30
        assert abs(float(ws["E16"].value) - c3) < 0.30
        assert abs(float(ws["F16"].value) - c4) < 0.30
        assert abs(float(ws["G16"].value) - tot_all) < 0.40
        assert abs(float(ws["I16"].value) - e_all) < 0.20

        import re as _re
        sub_txt = open(os.path.join(TASK_DIR, "submission.md"), encoding="utf-8").read()
        checks_sub = [
            ("C1", r"boron excursion hours across all eight SWRO trains are \*\*([\d,]+\.\d+) hours\*\*", c1, 0.5),
            ("C2", r"scaling excursion hours across all eight SWRO trains are \*\*([\d,]+\.\d+) hours\*\*", c2, 0.5),
            ("C3", r"structural membrane integrity fault hours across all eight SWRO trains are \*\*([\d,]+\.\d+) hours\*\*", c3, 0.5),
            ("C4", r"permeate TDS breakthrough hours across all eight SWRO trains are \*\*([\d,]+\.\d+) hours\*\*", c4, 0.5),
            ("Total", r"Plant-wide 2027 total anomalous operating hours:\s*([\d,]+\.\d+)\s*h", tot_all, 0.8),
            ("Energy", r"Plant-wide 2027 energy penalty:\s*([\d,]+\.\d+)\s*MWh", e_all, 0.4),
        ]
        for lbl, pat, target_v, tol in checks_sub:
            m = _re.search(pat, sub_txt)
            assert m, f"Missing {lbl} pattern in submission.md"
            sub_v = float(m.group(1).replace(",", ""))
            assert abs(sub_v - target_v) <= tol, f"submission.md {lbl}={sub_v} vs verify={target_v:.2f} (tol {tol})"

        ov_slate = sorted(u for u in trains if recomp[u]["desig"] == "OVERHAUL")
        print(f"VERIFY PASS (task28 v3.2): slate={ov_slate} C1={c1:.1f} C2={c2:.1f} C3={c3:.1f} C4={c4:.1f} Total={tot_all:.1f} h Energy={e_all:.1f} MWh")
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
