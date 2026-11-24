#!/usr/bin/env python3
"""Independent end-to-end verifier for task28 (v2).

Reads ONLY target.zip, golden.zip, and submission.md (never imports core.py, pack.py, analysis.py,
or reads figures.json / DESIGN_NOTE.md). Recomputes every graded figure from scratch using numpy
and verifies exact agreement with golden CSV, golden XLSX (evaluated via LibreOffice Calc), and
submission.md.
"""
import csv
import datetime as dt
import math
import os
import shutil
import subprocess
import tempfile
import zipfile

import numpy as np
import openpyxl

TASK_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UTC = dt.timezone.utc
START = dt.datetime(2026, 1, 1, 0, 0, 0, tzinfo=UTC)
D0 = dt.date(2026, 1, 1)


def _norm_sf_vec(z):
    return np.array([0.5 * math.erfc(float(v) / math.sqrt(2.0)) for v in z], dtype=float)


def _ar1_fg(phi, m):
    s = sum((m - d) * (phi ** d) for d in range(1, m))
    F = (m + 2.0 * s) / (m * m)
    g = (1.0 - phi ** m) / (1.0 - phi)
    G = phi * g * g / (m * m)
    return F, G


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
    work = tempfile.mkdtemp(prefix="verify-t28-")
    try:
        tdir = os.path.join(work, "target")
        gdir = os.path.join(work, "golden")
        os.makedirs(tdir)
        os.makedirs(gdir)
        with zipfile.ZipFile(os.path.join(TASK_DIR, "target.zip")) as z:
            z.extractall(tdir)
        with zipfile.ZipFile(os.path.join(TASK_DIR, "golden.zip")) as z:
            z.extractall(gdir)

        # 1. Asset register & operating plan
        tag_map = {}
        trains = []
        with open(os.path.join(tdir, "train_asset_register.csv"), encoding="utf-8") as f:
            for r in csv.DictReader(f):
                u = r["train_id"].strip()
                trains.append(u)
                tag_map[u] = u
                tag_map[r["legacy_tag"].strip()] = u

        q_map = {"2027-Q1": 0, "2027-Q2": 1, "2027-Q3": 2, "2027-Q4": 3}
        sr = {u: [0.0] * 4 for u in trains}
        bt = [0.0] * 4
        sc = [0.0] * 4
        qh = [0] * 4
        with open(os.path.join(tdir, "operating_plan_2027.csv"), encoding="utf-8") as f:
            for r in csv.DictReader(f):
                u = r["train_id"].strip()
                q = q_map[r["quarter"].strip()]
                sr[u][q] = float(r["dispatch_duty_ratio_2027"])
                bt[q] = float(r["boron_thermal_factor_2027"])
                sc[q] = float(r["scaling_recovery_factor_2027"])
                qh[q] = int(r["calendar_hours_2026"])

        q_starts = [0]
        for h in qh:
            q_starts.append(q_starts[-1] + h)
        q_of_h = np.zeros(sum(qh), dtype=int)
        for q in range(4):
            q_of_h[q_starts[q]:q_starts[q + 1]] = q
        q_of_15 = np.repeat(q_of_h, 4)

        # 2. Hourly SCADA feed flow (needed for S1 flux regression AND S2 cumulative flow)
        q_flow = {u: np.full(8760, np.nan) for u in trains}
        with open(os.path.join(tdir, "train_hydraulics_hourly_2026.csv"), encoding="utf-8") as f:
            rd = csv.reader(f)
            next(rd)
            cache_h = {}
            for row in rd:
                ts, u = row[0], row[1]
                idx = cache_h.get(ts)
                if idx is None:
                    idx = int((_parse_ts(ts) - START).total_seconds() // 3600)
                    cache_h[ts] = idx
                if np.isnan(q_flow[u][idx]):
                    val = float(row[2]) * (3.6 if row[3].strip() == "L/s" else 1.0)
                    q_flow[u][idx] = val

        # 3. S1: Solute-flux (1/Q_bar) composite regression + AR(1) 1-hour support deconvolution
        span = {}
        with open(os.path.join(tdir, "autosampler_schedule_2026.csv"), encoding="utf-8") as f:
            for r in csv.DictReader(f):
                u = tag_map[r["train_code"].strip()]
                day = (_parse_date(r["schedule_date"]) - D0).days
                span[(u, day)] = int(r["bottle_span_hours"])

        best_b = {}
        with open(os.path.join(tdir, "permeate_boron_composites_2026.csv"), encoding="utf-8") as f:
            for r in csv.DictReader(f):
                sid = r["sample_id"].strip()
                rev = int(r["qa_revision"])
                u = tag_map[r["train_code"].strip()]
                day = (_parse_date(r["collection_date"]) - D0).days
                slot = int(r["carousel_slot"])
                v = float(r["boron_conc"]) / (1000.0 if r["unit"].strip() == "ug/L" else 1.0)
                if sid not in best_b or rev > best_b[sid][0]:
                    best_b[sid] = (rev, u, day, slot, v)

        lam_grid = [0.25 * ((30.0 / 0.25) ** (k / 199.0)) for k in range(200)]
        b26 = {}
        for u in trains:
            rows_u = sorted([x for x in best_b.values() if x[1] == u], key=lambda x: (x[2], x[3]))
            ms = np.array([span[(u, x[2])] for x in rows_u], dtype=int)
            qs = np.array([int(q_of_h[x[2] * 24]) for x in rows_u], dtype=int)
            ds = np.array([x[2] for x in rows_u], dtype=int)
            vs = np.array([x[4] for x in rows_u], dtype=float)
            qbars = np.array(
                [float(np.mean(q_flow[u][x[2] * 24 + (x[3] - 1) * span[(u, x[2])]: x[2] * 24 + x[3] * span[(u, x[2])]])) for x in rows_u],
                dtype=float,
            )
            X = np.zeros((len(vs), 5), dtype=float)
            for q in range(4):
                X[:, q] = (qs == q).astype(float)
            X[:, 4] = 1.0 / qbars
            coef, _, _, _ = np.linalg.lstsq(X, vs, rcond=None)
            alphas = coef[:4]
            beta = max(0.0, float(coef[4]))
            res_u = vs - (alphas[qs] + beta / qbars)

            st = {}
            for m in (4, 8):
                idx = np.where(ms == m)[0]
                arr = res_u[idx]
                vm = float(np.var(arr, ddof=1))
                pa, pb = [], []
                for k in range(len(idx) - 1):
                    i1, i2 = int(idx[k]), int(idx[k + 1])
                    if i2 == i1 + 1 and (ds[i2] - ds[i1]) <= 1:
                        pa.append(res_u[i1])
                        pb.append(res_u[i2])
                pa, pb = np.array(pa), np.array(pb)
                cm = float(np.mean((pa - pa.mean()) * (pb - pb.mean())))
                st[m] = (max(1e-7, vm - 0.004 ** 2), max(0.0, cm))
            v4, c4 = st[4]
            v8, c8 = st[8]
            obs = [v4, c4, v8, c8]
            wts = [3.0 / (v4 * v4), 3.0 / (v4 * v4), 1.0 / (v8 * v8), 0.7 / (v8 * v8)]
            best_loss, best_sd = 1e18, 0.05
            for lam in lam_grid:
                phi_b = math.exp(-1.0 / lam)
                F4, G4 = _ar1_fg(phi_b, 4)
                F8, G8 = _ar1_fg(phi_b, 8)
                mod = [F4, G4, F8, G8]
                s2 = max(1e-9, sum(w * o * m for w, o, m in zip(wts, obs, mod)) / sum(w * m * m for w, m in zip(wts, mod)))
                loss = sum(w * (o - s2 * m) ** 2 for w, o, m in zip(wts, obs, mod))
                if loss < best_loss:
                    best_loss, best_sd = loss, math.sqrt(s2)
            mu_h = alphas[q_of_h] + beta / q_flow[u]
            p_exc = _norm_sf_vec((0.50 - mu_h) / best_sd)
            b26[u] = [float(np.sum(p_exc[q_of_h == q])) for q in range(4)]

        # 4. S2: Two-path bimodal DAF/DMF cumulative-flow hydraulic alignment
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
        idx_15 = np.arange(35040)
        h_f = idx_15 * 0.25
        h0 = np.floor(h_f).astype(int)
        w_f = h_f - h0
        h1 = np.minimum(h0 + 1, 8759)
        for u in trains:
            q15 = q_flow[u][h0] * (1.0 - w_f) + q_flow[u][h1] * w_f
            phi = np.cumsum(q15 * 0.25)
            idx_c = np.arange(32, 35040, 16)
            co_c = c_out[u][idx_c]
            v1_g = list(range(160, 561, 30))
            v2_g = list(range(760, 1521, 40))
            c1_c = {v1: np.interp(phi[idx_c] - v1, phi, c_in[u]) for v1 in v1_g}
            c2_c = {v2: np.interp(phi[idx_c] - v2, phi, c_in[u]) for v2 in v2_g}
            best_mse = 1e18
            best = (0.0, 400.0, 960.0)
            for v2 in v2_g:
                c2 = c2_c[v2]
                m0 = float(np.mean((co_c - c2) ** 2))
                if m0 < best_mse:
                    best_mse, best = m0, (0.0, 400.0, float(v2))
                for v1 in v1_g:
                    c1 = c1_c[v1]
                    dc = c1 - c2
                    f_h = float(np.clip(np.dot(co_c - c2, dc) / max(float(np.dot(dc, dc)), 1e-12), 0.0, 0.49))
                    mse = float(np.mean((co_c - (f_h * c1 + (1.0 - f_h) * c2)) ** 2))
                    if mse < best_mse:
                        best_mse, best = mse, (f_h, float(v1), float(v2))
            idx_f = np.arange(32, 35040, 6)
            co_f = c_out[u][idx_f]
            f0, v10, v20 = best
            v1_f = list(range(max(120, int(v10) - 36), min(600, int(v10) + 37), 8)) if f0 > 0.05 else [400]
            v2_f = list(range(max(700, int(v20) - 48), min(1580, int(v20) + 49), 10))
            c1_f = {v1: np.interp(phi[idx_f] - v1, phi, c_in[u]) for v1 in v1_f}
            c2_f = {v2: np.interp(phi[idx_f] - v2, phi, c_in[u]) for v2 in v2_f}
            best_mse = 1e18
            for v2 in v2_f:
                c2 = c2_f[v2]
                for v1 in v1_f:
                    c1 = c1_f[v1]
                    dc = c1 - c2
                    f_h = float(np.clip(np.dot(co_f - c2, dc) / max(float(np.dot(dc, dc)), 1e-12), 0.0, 0.49))
                    if f_h < 0.04:
                        f_h = 0.0
                    mse = float(np.mean((co_f - (f_h * c1 + (1.0 - f_h) * c2)) ** 2))
                    if mse < best_mse:
                        best_mse, best = mse, (f_h, float(v1), float(v2))
            f_hat, v1_hat, v2_hat = best
            x1 = np.interp(phi - v1_hat, phi, x_in[u])
            x2 = np.interp(phi - v2_hat, phi, x_in[u])
            xa = f_hat * x1 + (1.0 - f_hat) * x2
            hit = (xa[32:] > 1.50) & (y_out[u][32:] > 1.50)
            s26[u] = [float(np.sum(hit & (q_of_15[32:] == q)) * 0.25) for q in range(4)]

        # 5. S3: 4-state dual-recipe CIP-invariant latent-class EM (192 cells)
        pats = {u: np.zeros(2190, dtype=int) for u in trains}
        with open(os.path.join(tdir, "shift_diagnostics_2026.csv"), encoding="utf-8") as f:
            for r in csv.DictReader(f):
                u = r["train_id"].strip()
                b = int((_parse_ts(r["block_start_lisbon"]) - START).total_seconds() // 14400)
                pats[u][b] = (int(r["salt_passage_alarm"]) << 2) | (int(r["stage_dp_alarm"]) << 1) | int(r["acoustic_bypass_alarm"])

        reg = {u: np.zeros(2190, dtype=int) for u in trains}
        with open(os.path.join(tdir, "cip_wash_log_2026.csv"), encoding="utf-8") as f:
            for r in csv.DictReader(f):
                u = tag_map[r["train_code"].strip()]
                cb = int((_parse_ts(r["wash_completed_lisbon"]) - START).total_seconds() // 14400)
                code = 1 if r["chemical_stage"].strip() == "CIP_ALK_pH11" else 2
                reg[u][cb:min(2190, cb + 30)] = code

        bits = np.array([[(b >> 2) & 1, (b >> 1) & 1, b & 1] for b in range(8)], dtype=float)
        cnt = np.zeros((8, 3, 8))
        for i, u in enumerate(trains):
            for rg in range(3):
                for b in range(8):
                    cnt[i, rg, b] = np.sum((reg[u] == rg) & (pats[u] == b))

        def _indep(p):
            return np.prod(np.where(bits == 1, p, 1.0 - p), axis=1)

        p0 = np.array([0.015, 0.015, 0.009])
        p_bio = np.array([0.76, 0.86, 0.02])
        p_min = np.array([0.28, 0.88, 0.50])
        p_str = np.array([0.88, 0.16, 0.62])
        pi_bio = np.full(8, 0.05)
        pi_min = np.full(8, 0.05)
        pi_str = np.full(8, 0.015)
        rb_sh = 0.25
        rm_sh = 0.22
        n_reg = cnt.sum(axis=2)

        for _ in range(350):
            e = np.vstack([_indep(p0), _indep(p_bio), _indep(p_min), _indep(p_str)])
            W = np.zeros((4, 8))
            w_st = np.zeros((8, 3, 4))
            for i in range(8):
                for rg in range(3):
                    fb = pi_bio[i] * (rb_sh if rg == 1 else 1.0)
                    fm = pi_min[i] * (rm_sh if rg == 2 else 1.0)
                    fs = pi_str[i]
                    fc = max(1e-6, 1.0 - fb - fm - fs)
                    pis = np.array([fc, fb, fm, fs])[:, None]
                    a = pis * e
                    g = a / (a.sum(axis=0, keepdims=True) + 1e-18)
                    W += g * cnt[i, rg][None, :]
                    w_st[i, rg] = (g * cnt[i, rg][None, :]).sum(axis=1)
            pi_str = np.clip(w_st[:, :, 3].sum(axis=1) / n_reg.sum(axis=1), 1e-4, 0.45)
            pi_bio = np.clip((w_st[:, 0, 1] + w_st[:, 2, 1]) / (n_reg[:, 0] + n_reg[:, 2]), 1e-4, 0.65)
            pi_min = np.clip((w_st[:, 0, 2] + w_st[:, 1, 2]) / (n_reg[:, 0] + n_reg[:, 1]), 1e-4, 0.65)
            rb_sh = float(np.clip((w_st[:, 1, 1].sum() / n_reg[:, 1].sum()) / max((w_st[:, 0, 1].sum() + w_st[:, 2, 1].sum()) / (n_reg[:, 0].sum() + n_reg[:, 2].sum()), 1e-5), 0.05, 0.65))
            rm_sh = float(np.clip((w_st[:, 2, 2].sum() / n_reg[:, 2].sum()) / max((w_st[:, 0, 2].sum() + w_st[:, 1, 2].sum()) / (n_reg[:, 0].sum() + n_reg[:, 1].sum()), 1e-5), 0.05, 0.65))
            p0 = np.clip((W[0] @ bits) / max(W[0].sum(), 1e-9), [0.002, 0.002, 0.002], [0.08, 0.08, 0.06])
            p_bio = np.clip((W[1] @ bits) / max(W[1].sum(), 1e-9), [0.35, 0.45, 0.002], [0.98, 0.98, 0.12])
            p_min = np.clip((W[2] @ bits) / max(W[2].sum(), 1e-9), [0.05, 0.50, 0.18], [0.65, 0.98, 0.85])
            p_str = np.clip((W[3] @ bits) / max(W[3].sum(), 1e-9), [0.50, 0.02, 0.25], [0.99, 0.45, 0.95])

        st26 = {u: [float(pi_str[i] * qh[q]) for q in range(4)] for i, u in enumerate(trains)}

        # 6. Project 2027 & compare against golden CSV, golden XLSX, and submission.md
        recomp = {}
        for u in trains:
            b27 = [b26[u][q] * bt[q] * sr[u][q] for q in range(4)]
            s27 = [s26[u][q] * sc[q] * sr[u][q] for q in range(4)]
            t27 = [st26[u][q] * sr[u][q] for q in range(4)]
            hb, hs, ht = sum(b27), sum(s27), sum(t27)
            htot = hb + hs + ht
            hq3 = b27[2] + s27[2] + t27[2]
            energy_mwh = (hb * 420.0 + hs * 360.0 + ht * 540.0) / 1000.0
            recomp[u] = dict(b=hb, s=hs, st=ht, tot=htot, q3=hq3, mwh=energy_mwh, des="OVERHAUL" if htot >= 400.0 else "MONITOR")

        c1 = sum(recomp[u]["b"] for u in trains)
        c2 = sum(recomp[u]["s"] for u in trains)
        c3 = sum(recomp[u]["st"] for u in trains)
        tot27 = c1 + c2 + c3
        ov27 = sum(recomp[u]["tot"] for u in trains if recomp[u]["des"] == "OVERHAUL")
        q3_27 = sum(recomp[u]["q3"] for u in trains)
        energy27 = sum(recomp[u]["mwh"] for u in trains)
        ov_energy27 = sum(recomp[u]["mwh"] for u in trains if recomp[u]["des"] == "OVERHAUL")

        # Verify golden CSV
        with open(os.path.join(gdir, "barlavento_train_diagnostics_2027.csv"), encoding="utf-8") as f:
            gcsv = list(csv.DictReader(f))
        assert len(gcsv) == 8
        for row in gcsv:
            u = row["train_id"]
            rc = recomp[u]
            assert abs(float(row["boron_2027_h"]) - rc["b"]) < 0.15, f"CSV {u} boron mismatch ({row['boron_2027_h']} vs {rc['b']:.2f})"
            assert abs(float(row["scaling_2027_h"]) - rc["s"]) < 0.15, f"CSV {u} scaling mismatch ({row['scaling_2027_h']} vs {rc['s']:.2f})"
            assert abs(float(row["struct_2027_h"]) - rc["st"]) < 0.15, f"CSV {u} struct mismatch ({row['struct_2027_h']} vs {rc['st']:.2f})"
            assert abs(float(row["total_2027_h"]) - rc["tot"]) < 0.15, f"CSV {u} total mismatch ({row['total_2027_h']} vs {rc['tot']:.2f})"
            assert abs(float(row["q3_2027_h"]) - rc["q3"]) < 0.15, f"CSV {u} q3 mismatch"
            assert abs(float(row["energy_2027_mwh"]) - rc["mwh"]) < 0.05, f"CSV {u} energy MWh mismatch"
            assert row["designation"] == rc["des"], f"CSV {u} designation mismatch"

        # Verify golden XLSX via LibreOffice Calc evaluation
        prof = "file://" + os.path.join(work, "lo-prof")
        subprocess.run(
            [
                "soffice",
                "-env:UserInstallation=" + prof,
                "--headless",
                "--convert-to",
                "xlsx",
                "--outdir",
                work,
                os.path.join(gdir, "barlavento_swro_overhaul_plan_2027.xlsx"),
            ],
            check=True,
            capture_output=True,
            timeout=120,
        )
        ewb = openpyxl.load_workbook(os.path.join(work, "barlavento_swro_overhaul_plan_2027.xlsx"), data_only=True)
        ws = ewb["Overhaul_Triage_2027"]
        assert abs(float(ws["C16"].value) - c1) < 0.15
        assert abs(float(ws["D16"].value) - c2) < 0.15
        assert abs(float(ws["E16"].value) - c3) < 0.15
        assert abs(float(ws["F16"].value) - tot27) < 0.15
        assert abs(float(ws["F17"].value) - ov27) < 0.15
        assert abs(float(ws["G16"].value) - q3_27) < 0.15
        assert abs(float(ws["H16"].value) - energy27) < 0.15
        assert abs(float(ws["H17"].value) - ov_energy27) < 0.15

        # Verify submission.md carries exact recomputed headline figures
        sub = open(os.path.join(TASK_DIR, "submission.md"), encoding="utf-8").read()
        for tok in (
            f"{c1:,.1f}",
            f"{c2:,.1f}",
            f"{c3:,.1f}",
            f"{tot27:,.1f}",
            f"{ov27:,.1f}",
            f"{q3_27:,.1f}",
            f"{energy27:,.1f}",
            f"{ov_energy27:,.1f}",
        ):
            assert tok in sub, f"submission.md missing independently recomputed figure {tok}"

        print(
            f"VERIFY PASS  task28: C1={c1:.1f} C2={c2:.1f} C3={c3:.1f} Total={tot27:.1f} "
            f"Overhaul={ov27:.1f} Q3={q3_27:.1f} Energy={energy27:.1f} MWh "
            f"OvEnergy={ov_energy27:.1f} MWh"
        )
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
