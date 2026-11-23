#!/usr/bin/env python3
"""Independent end-to-end verifier for task28.

Reads ONLY target.zip, golden.zip, and submission.md (never imports core.py, pack.py, analysis.py,
or reads figures.json / DESIGN_NOTE.md). Recomputes every graded figure from scratch using numpy
and verifies exact agreement with golden CSV, golden XLSX (evaluated via LibreOffice Calc), and
submission.md.
"""
import csv
import datetime as dt
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

import numpy as np
import openpyxl

TASK_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UTC = dt.timezone.utc
START = dt.datetime(2026, 1, 1, 0, 0, 0, tzinfo=UTC)
D0 = dt.date(2026, 1, 1)


def _norm_sf(z):
    return 0.5 * math.erfc(z / math.sqrt(2.0))


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

        # 2. S1: Boron composite deconvolution
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

        lam_grid = [0.25 * ((30.0 / 0.25) ** (k / 219.0)) for k in range(220)]
        b26 = {}
        inc_b26 = {}
        for u in trains:
            rows_u = sorted([x for x in best_b.values() if x[1] == u], key=lambda x: (x[2], x[3]))
            ms = [span[(u, x[2])] for x in rows_u]
            qs = [int(q_of_h[x[2] * 24]) for x in rows_u]
            ds = [x[2] for x in rows_u]
            vs = [x[4] for x in rows_u]
            q_mu = [float(np.mean([vs[i] for i in range(len(vs)) if qs[i] == q])) for q in range(4)]
            inc_b26[u] = sum(
                (sum(1 for i in range(len(vs)) if qs[i] == q and vs[i] > 0.50) / sum(1 for i in range(len(vs)) if qs[i] == q)) * qh[q]
                for q in range(4)
            )
            res_u = [vs[i] - q_mu[qs[i]] for i in range(len(vs))]
            st = {}
            for m in (4, 8):
                idx = [i for i in range(len(ms)) if ms[i] == m]
                arr = np.array([res_u[i] for i in idx])
                vm = float(np.var(arr, ddof=1))
                pa, pb = [], []
                for k in range(len(idx) - 1):
                    i1, i2 = idx[k], idx[k + 1]
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
                phi = math.exp(-1.0 / lam)
                F4, G4 = _ar1_fg(phi, 4)
                F8, G8 = _ar1_fg(phi, 8)
                mod = [F4, G4, F8, G8]
                s2 = max(1e-9, sum(w * o * m for w, o, m in zip(wts, obs, mod)) / sum(w * m * m for w, m in zip(wts, mod)))
                loss = sum(w * (o - s2 * m) ** 2 for w, o, m in zip(wts, obs, mod))
                if loss < best_loss:
                    best_loss, best_sd = loss, math.sqrt(s2)
            b26[u] = [_norm_sf((0.50 - q_mu[q]) / best_sd) * qh[q] for q in range(4)]

        # 3. S2: Cumulative-flow Lagrangian alignment
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
        inc_s26 = {}
        idx_15 = np.arange(35040)
        h_f = idx_15 * 0.25
        h0 = np.floor(h_f).astype(int)
        w_f = h_f - h0
        h1 = np.minimum(h0 + 1, 8759)
        for u in trains:
            inc_s26[u] = float(np.sum((x_in[u][32:] > 1.50) & (y_out[u][32:] > 1.50)) * 0.25)
            q15 = q_flow[u][h0] * (1.0 - w_f) + q_flow[u][h1] * w_f
            phi = np.cumsum(q15 * 0.25)
            best_v, best_mse = 750.0, 1e18
            for vc in np.arange(400.0, 1450.0, 20.0):
                ca = np.interp(phi[32::8] - vc, phi, c_in[u])
                mse = float(np.mean((c_out[u][32::8] - ca) ** 2))
                if mse < best_mse:
                    best_mse, best_v = mse, float(vc)
            v0 = best_v
            best_mse = 1e18
            for vc in np.arange(max(350.0, v0 - 24.0), min(1500.0, v0 + 25.0), 4.0):
                ca = np.interp(phi[32::3] - vc, phi, c_in[u])
                mse = float(np.mean((c_out[u][32::3] - ca) ** 2))
                if mse < best_mse:
                    best_mse, best_v = mse, float(vc)
            v1 = best_v
            best_mse = 1e18
            for vc in (v1 - 4.0, v1 - 2.0, v1, v1 + 2.0, v1 + 4.0):
                ca = np.interp(phi[32:] - vc, phi, c_in[u])
                mse = float(np.mean((c_out[u][32:] - ca) ** 2))
                if mse < best_mse:
                    best_mse, best_v = mse, float(vc)
            x_al = np.interp(phi - best_v, phi, x_in[u])
            hit = (x_al[32:] > 1.50) & (y_out[u][32:] > 1.50)
            s26[u] = [float(np.sum(hit & (q_of_15[32:] == q)) * 0.25) for q in range(4)]

        # 4. S3: 3-state CIP-invariant conditionally-dependent latent class EM
        pats = {u: np.zeros(2190, dtype=int) for u in trains}
        with open(os.path.join(tdir, "shift_diagnostics_2026.csv"), encoding="utf-8") as f:
            for r in csv.DictReader(f):
                u = r["train_id"].strip()
                b = int((_parse_ts(r["block_start_lisbon"]) - START).total_seconds() // 14400)
                pats[u][b] = (int(r["salt_passage_alarm"]) << 2) | (int(r["stage_dp_alarm"]) << 1) | int(r["acoustic_bypass_alarm"])

        is_post = {u: np.zeros(2190, dtype=bool) for u in trains}
        with open(os.path.join(tdir, "cip_wash_log_2026.csv"), encoding="utf-8") as f:
            for r in csv.DictReader(f):
                u = tag_map[r["train_code"].strip()]
                cb = int((_parse_ts(r["wash_completed_lisbon"]) - START).total_seconds() // 14400)
                is_post[u][cb:min(2190, cb + 30)] = True

        bits = np.array([[(b >> 2) & 1, (b >> 1) & 1, b & 1] for b in range(8)], dtype=float)
        cnt_pre = np.zeros((8, 8))
        cnt_post = np.zeros((8, 8))
        inc_st26 = {}
        for i, u in enumerate(trains):
            inc_st26[u] = float(np.sum(np.isin(pats[u], [3, 5, 6, 7])) * 4.0)
            for b in range(8):
                cnt_pre[i, b] = np.sum((~is_post[u]) & (pats[u] == b))
                cnt_post[i, b] = np.sum(is_post[u] & (pats[u] == b))

        def _indep(p):
            return np.prod(np.where(bits == 1, p, 1.0 - p), axis=1)

        p0 = np.array([0.018, 0.018, 0.010])
        p2 = np.array([0.85, 0.55, 0.55])
        e1 = np.array([0.10, 0.001, 0.14, 0.002, 0.11, 0.001, 0.64, 0.006])
        e1 /= e1.sum()
        pi_s = np.full(8, 0.015)
        pi_fpr = np.full(8, 0.05)
        pi_fpo = np.full(8, 0.025)
        n_pr = cnt_pre.sum(axis=1)
        n_po = cnt_post.sum(axis=1)

        for _ in range(320):
            e0 = _indep(p0)
            e2 = _indep(p2)
            W0 = np.zeros(8)
            W1 = np.zeros(8)
            W2 = np.zeros(8)
            w1_pr = np.zeros(8)
            w1_po = np.zeros(8)
            w2_t = np.zeros(8)
            for i in range(8):
                p0_pr = max(1e-6, 1.0 - pi_fpr[i] - pi_s[i])
                p0_po = max(1e-6, 1.0 - pi_fpo[i] - pi_s[i])
                a = np.vstack([p0_pr * e0, pi_fpr[i] * e1, pi_s[i] * e2])
                g_pr = a / (a.sum(axis=0) + 1e-15)
                W0 += cnt_pre[i] * g_pr[0]
                W1 += cnt_pre[i] * g_pr[1]
                W2 += cnt_pre[i] * g_pr[2]
                w1_pr[i] = float(np.sum(cnt_pre[i] * g_pr[1]))
                w2_t[i] += float(np.sum(cnt_pre[i] * g_pr[2]))

                a = np.vstack([p0_po * e0, pi_fpo[i] * e1, pi_s[i] * e2])
                g_po = a / (a.sum(axis=0) + 1e-15)
                W0 += cnt_post[i] * g_po[0]
                W1 += cnt_post[i] * g_po[1]
                W2 += cnt_post[i] * g_po[2]
                w1_po[i] = float(np.sum(cnt_post[i] * g_po[1]))
                w2_t[i] += float(np.sum(cnt_post[i] * g_po[2]))
            pi_s = np.clip(w2_t / (n_pr + n_po), 1e-4, 0.50)
            pi_fpr = np.clip(w1_pr / n_pr, 1e-4, 0.85)
            pi_fpo = np.minimum(pi_fpr * 0.95, np.clip(w1_po / n_po, 1e-4, 0.85))
            p0 = np.clip((W0 @ bits) / max(W0.sum(), 1e-9), 1e-3, 0.20)
            p2 = np.clip((W2 @ bits) / max(W2.sum(), 1e-9), 0.15, 0.99)
            p3b = float(np.clip(((W0 + W1) @ bits[:, 2]) / (W0.sum() + W1.sum()), 1e-3, 0.10))
            p0[2] = p3b
            p12 = np.maximum(1e-5, np.array([W1[2 * j] + W1[2 * j + 1] for j in range(4)]) / max(W1.sum(), 1e-9))
            p12 /= p12.sum()
            for j in range(4):
                e1[2 * j] = p12[j] * (1.0 - p3b)
                e1[2 * j + 1] = p12[j] * p3b

        st26 = {u: [float(pi_s[i] * qh[q]) for q in range(4)] for i, u in enumerate(trains)}

        # 5. Project 2027 & compare against golden CSV, golden XLSX, and submission.md
        recomp = {}
        tot26 = 0.0
        miss26 = 0.0
        for u in trains:
            b27 = [b26[u][q] * bt[q] * sr[u][q] for q in range(4)]
            s27 = [s26[u][q] * sc[q] * sr[u][q] for q in range(4)]
            t27 = [st26[u][q] * sr[u][q] for q in range(4)]
            hb, hs, ht = sum(b27), sum(s27), sum(t27)
            htot = hb + hs + ht
            hq3 = b27[2] + s27[2] + t27[2]
            energy_mwh = (hb * 420.0 + hs * 360.0 + ht * 540.0) / 1000.0
            recomp[u] = dict(b=hb, s=hs, st=ht, tot=htot, q3=hq3, mwh=energy_mwh, des="OVERHAUL" if htot >= 400.0 else "MONITOR")
            tot26 += sum(b26[u]) + sum(s26[u]) + sum(st26[u])
            miss26 += abs(sum(b26[u]) - inc_b26[u]) + abs(sum(s26[u]) - inc_s26[u]) + abs(sum(st26[u]) - inc_st26[u])

        disc_pct = 100.0 * miss26 / tot26
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
            assert abs(float(row["boron_2027_h"]) - rc["b"]) < 0.15, f"CSV {u} boron mismatch"
            assert abs(float(row["scaling_2027_h"]) - rc["s"]) < 0.15, f"CSV {u} scaling mismatch"
            assert abs(float(row["struct_2027_h"]) - rc["st"]) < 0.15, f"CSV {u} struct mismatch"
            assert abs(float(row["total_2027_h"]) - rc["tot"]) < 0.15, f"CSV {u} total mismatch"
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
        assert abs(float(ws["B30"].value) * 100.0 - disc_pct) < 0.15

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
            f"{disc_pct:.1f}%",
        ):
            assert tok in sub, f"submission.md missing independently recomputed figure {tok}"

        print(
            f"VERIFY PASS  task28: C1={c1:.1f} C2={c2:.1f} C3={c3:.1f} Total={tot27:.1f} "
            f"Overhaul={ov27:.1f} Q3={q3_27:.1f} Energy={energy27:.1f} MWh "
            f"OvEnergy={ov_energy27:.1f} MWh Disc={disc_pct:.1f}%"
        )
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
