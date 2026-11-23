"""task9 architecture 6: independent recomputation of every graded figure from target/ alone, plus LibreOffice
Calc formula evaluation check on the golden workbook. Nothing here imports any generator module."""
import csv
import datetime as dt
import glob
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile
from collections import defaultdict

import numpy as np
import pandas as pd
from openpyxl import load_workbook
from scipy.optimize import minimize_scalar
from scipy.stats import norm

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
G = os.path.join(TASK, "golden")
D0 = dt.date(2024, 7, 1)
GAP = 13
N = {"pass": 0, "fail": 0}
SNAP26 = ("2025-12-22", "2026-03-23", "2026-06-22", "2026-09-21")
SNAP27 = ("2026-12-21", "2027-03-22", "2027-06-21", "2027-09-20", "2027-12-20")


def ok(label, cond, detail=""):
    N["pass" if cond else "fail"] += 1
    print(("PASS  " if cond else "FAIL  ") + label + ("" if cond else "  %s" % (detail,)))


def wk(d):
    if isinstance(d, (dt.datetime, pd.Timestamp)):
        d = d.date()
    if isinstance(d, str):
        d = dt.date.fromisoformat(d[:10])
    return (d - D0).days // 7


def iso(s):
    y, n = s.split("-W")
    return wk(dt.date.fromisocalendar(int(y), int(n), 1))


def sheet(path, name):
    ws = load_workbook(path, read_only=True, data_only=True)[name]
    rows = list(ws.iter_rows(values_only=True))
    return pd.DataFrame(rows[1:], columns=rows[0])


def main():
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    reg = pd.read_csv(os.path.join(T, "gms_model_registry.csv")).set_index("model_family")
    fams = sorted(reg.index)
    sched = dict(zip(reg["scheduler_job_family"], reg.index))
    custom = {c: (0 if pd.isna(v) or not str(v).strip() else len(str(v).split(";")))
              for c, v in reg["custom_training_components"].items()}

    book = pd.read_csv(os.path.join(T, "gms_scored_book_by_family.csv"))
    book = book[book["snapshot_date"] == "2026-09-21"].set_index("model_family")["scored_merchants"].astype(float)
    wt = book / book.sum()

    # Manifests (deduplicated on run_id)
    runs = {}
    for line in open(os.path.join(T, "training_scheduler_runs_2024_2026.jsonl")):
        m = json.loads(line)
        runs.setdefault(m["run_id"], m)
    prod = defaultdict(dict)
    for m in runs.values():
        if m["kind"] == "production":
            prod[sched[m["job_family"]]][iso(m["iso_week"])] = m
    TT = max(max(v) for v in prod.values()) + 1
    window, last_cold, warm_eff = {}, {}, {}
    for c in fams:
        lens = [iso(m["window_last_week"]) - iso(m["window_first_week"]) + 1 for m in prod[c].values()]
        window[c] = max(set(x for x in lens if x > 26), key=lens.count)
        last_cold[c] = max(t for t, m in prod[c].items() if m["parent_model_id"] is None)
        warm_eff[c] = min(t for t, m in prod[c].items() if bool(m["options"]["warm_start"]))

    # Panel (later load_id wins; Tolka Pay remapped)
    remap = {}
    with open(os.path.join(T, "tolka_pay_merchant_id_migration.csv")) as fh:
        for r in csv.DictReader(fh):
            remap[r["old_merchant_id"]] = r["new_merchant_id"]
    best = {}
    for p in sorted(glob.glob(os.path.join(T, "gms_monitoring_panel_scores_*.csv"))):
        with open(p) as fh:
            for r in csv.DictReader(fh):
                key = (remap.get(r["merchant_id"], r["merchant_id"]), r["score_date"])
                if key not in best or r["load_id"] > best[key][0]:
                    best[key] = (r["load_id"], r["model_family"], float(r["score"]))
    idx, Z = {c: {} for c in fams}, {}
    for (mid, d), (_, c, s) in best.items():
        idx[c].setdefault(mid, len(idx[c]))
    for c in fams:
        Z[c] = np.full((len(idx[c]), TT), np.nan)
    for (mid, d), (_, c, s) in best.items():
        Z[c][idx[c][mid], wk(d)] = s
    ok("panel merchant count matches figures.json",
       sum(len(v) for v in idx.values()) == fig["base"]["panel_merchants"],
       (sum(len(v) for v in idx.values()), fig["base"]["panel_merchants"]))

    # Instruments
    preg = pd.read_csv(os.path.join(T, "mrm_instrument_pair_register_2026.csv"))
    ps = pd.read_csv(os.path.join(T, "mrm_instrument_pair_scores_2026.csv"),
                     dtype={"pair_id": str, "merchant_id": str})
    ps["d"] = ps["score_b"] - ps["score_a"]
    pv = ps.groupby("pair_id")["d"].var(ddof=0)
    preg["v"] = preg["pair_id"].map(pv)
    preg["t"] = preg["refresh_date"].map(wk)
    inst = preg.groupby(["model_family", "pair_kind"])["v"].mean().unstack()

    # Labelled rows (warehouse + 2027 plan)
    wr = pd.read_csv(os.path.join(T, "warehouse_labelled_rows_weekly.csv"))
    rows = defaultdict(dict)
    for r in wr.itertuples(index=False):
        rows[r.model_family][wk(r.label_week)] = float(r.labelled_rows)
    pl = sheet(os.path.join(T, "labelled_row_plan_2027.xlsx"), "Labelled rows")
    for r in pl.to_dict("records"):
        for c in fams:
            rows[c][wk(r["label_week"])] = float(r[c])

    # S2: Continuous optimization for recency decay lambda_f per family from 16 2026 bootstrap pairs
    def w_probs(c, t, lam):
        W = window[c]
        n = np.array([rows[c][u] for u in range(t - W + 1, t + 1)], float)
        ages = np.arange(W - 1, -1, -1, dtype=float)
        wtot = (lam ** ages) * n
        return wtot / wtot.sum(), n

    def bfactor(c, t, lam):
        p, n = w_probs(c, t, lam)
        return 2.0 * float(np.sum((p ** 2) / n))

    def tfactor(c, t0, t1, lam):
        p0, n0 = w_probs(c, t0, lam)
        p1, n1 = w_probs(c, t1, lam)
        W = window[c]
        h = t1 - t0
        return float(np.sum((p0[:h] ** 2) / n0[:h]) + np.sum((p1[W - h:] ** 2) / n1[W - h:]) +
                     np.sum(((p1[:W - h] - p0[h:]) ** 2) / n0[h:]))

    s27 = [(wk(SNAP27[i]), wk(SNAP27[i + 1])) for i in range(4)]
    lam_hat, r2_hat, tur_q = {}, {}, {}
    for c in fams:
        b = preg[(preg["model_family"] == c) & (preg["pair_kind"] == "bootstrap")].sort_values("t")
        bt = b["t"].to_numpy(int)
        yv = np.maximum(b["v"].to_numpy(float) - inst.loc[c, "replicate"], 0.5)
        def obj_lam(l):
            bf = np.array([bfactor(c, int(t), l) for t in bt])
            log_c = float(np.mean(np.log(yv) - np.log(bf)))
            return float(np.sum((np.log(yv) - (log_c + np.log(bf))) ** 2))
        res = minimize_scalar(obj_lam, bounds=(0.75, 1.0), method="bounded")
        lam_hat[c] = float(res.x)
        bf = np.array([bfactor(c, int(t), lam_hat[c]) for t in bt])
        r2_hat[c] = math.exp(float(np.mean(np.log(yv) - np.log(bf))))
        tur_q[c] = [r2_hat[c] * tfactor(c, a, b_, lam_hat[c]) for a, b_ in s27]
    tur_pts = math.sqrt(sum(wt[c] * np.mean(tur_q[c]) for c in fams))
    ok("S2 training data (independent continuous opt) matches figures.json",
       abs(tur_pts - fig["points"]["training data"]) < 0.03, (tur_pts, fig["points"]["training data"]))

    # S1: Continuous optimization for anchored warm-start decay phi_f (minus data curve), plus cold-era check
    opt13 = {}
    cold_curvs = []
    for c in fams:
        t0 = max(last_cold[c] + 13, 66)
        X = Z[c]
        D = np.array([np.nanmean((X[:, t0 + h:TT] - X[:, t0:TT - h]) ** 2) for h in range(1, 26)])
        dc = np.array([r2_hat[c] * np.mean([tfactor(c, t, t + h, lam_hat[c]) for t in range(t0, TT - h)])
                       for h in range(1, 26)])
        Dn = D - dc
        h = np.arange(1, 26, dtype=float)
        wgt = 1.0 / (Dn ** 2)
        rep = inst.loc[c, "replicate"]
        def obj_phi(phi):
            A = rep / (1.0 - phi ** 2)
            g_ = 1.0 - phi ** h
            b_ = float(np.sum(wgt * h * (Dn - A * g_)) / np.sum(wgt * h * h))
            return float(np.sum(wgt * (Dn - b_ * h - A * g_) ** 2))
        res = minimize_scalar(obj_phi, bounds=(0.45, 0.985), method="bounded")
        phi = float(res.x)
        opt13[c] = rep / (1.0 - phi ** 2) * (1.0 - phi ** GAP)
        # Cold-start curvature check
        ec = warm_eff[c]
        Dc = np.array([np.nanmean((X[:, h_:ec] - X[:, :ec - h_]) ** 2) for h_ in range(1, 15)])
        p2 = np.polyfit(np.arange(1, 15), Dc, 2)
        cold_curvs.append(float(p2[0] * 196.0 / Dc[-1]))
    opt_pts = math.sqrt(sum(wt[c] * opt13[c] for c in fams))
    ok("S1 optimisation noise (independent continuous opt) matches figures.json",
       abs(opt_pts - fig["points"]["optimisation noise"]) < 0.03, (opt_pts, fig["points"]["optimisation noise"]))
    ok("Cold-start linearity independently verified (mean curvature near zero)",
       abs(float(np.mean(cold_curvs))) < 0.05, float(np.mean(cold_curvs)))

    # S3: Pinned-view adoption lag + 2026 release_shadow same-group merchant correlations
    cal = sheet(os.path.join(T, "platform_change_calendar.xlsx"), "Changes")
    past_rows = []
    for ref, test in (("PC-24-031", lambda m: m["runtime_image"].endswith("4.1.0")),
                      ("PC-24-047", lambda m: bool(m["options"]["warm_start"])),
                      ("PC-25-012", lambda m: m["options"]["precision"] == "bf16")):
        sub = cal[cal["change_ref"] == ref].set_index("model_family")
        for c in fams:
            p_w = iso(sub.loc[c, "planned_week"])
            d_w = wk(sub.loc[c, "completed_on"])
            seq = [test(prod[c][t]) for t in range(TT)]
            eff = seq.index(True)
            off = [t for t in range(eff, TT) if not seq[t]]
            rv = 0
            if off:
                a = off[0]
                b_ = next((t for t in range(a, TT) if seq[t]), TT)
                rv = max(0, min(b_, eff + 26) - a)
            past_rows.append((custom[c], p_w, d_w, eff, rv / 26.0))
    cs = np.array([r[0] for r in past_rows], float)
    lags = np.array([max(r[3] - r[2], 1) for r in past_rows], float)
    slip = float(np.mean([r[2] - r[1] for r in past_rows]))
    rev = float(np.mean([r[4] for r in past_rows]))
    X_m = np.vstack([np.ones_like(cs), cs]).T
    beta = np.linalg.lstsq(X_m, np.log(lags), rcond=None)[0]
    sg = float(np.std(np.log(lags) - X_m @ beta, ddof=2))

    pin_cal = cal[cal["change_ref"] == "PC-26-058"].set_index("model_family")
    wk27 = np.arange(wk("2026-12-28"), wk("2027-12-20") + 1)  # 52 assessment-year Mondays (Standard 2.2)
    assert len(wk27) == 52
    cov = {}
    for c in fams:
        mu = beta[0] + beta[1] * custom[c]
        p_w = iso(pin_cal.loc[c, "planned_week"])
        dt_w = wk27 - (p_w + slip)
        cov[c] = {int(t): (float(norm.cdf((math.log(x) - mu) / sg)) * (1.0 - rev) if x > 0 else 0.0)
                  for t, x in zip(wk27, dt_w)}
    cc_pin = 100.0 * float(np.mean([v for c in fams for v in cov[c].values()]))
    ok("Pinned feature views share independently matches figures.json",
       abs(cc_pin - fig["cc_pin"]) < 0.1, (cc_pin, fig["cc_pin"]))

    # Same-group release_shadow correlations
    rl_log = pd.read_csv(os.path.join(T, "feature_platform_release_log.csv")).set_index("release_id")
    rel_ps = ps[ps["pair_id"].isin(set(preg[preg["pair_kind"] == "release_shadow"]["pair_id"]))]
    ser = {pid: grp.set_index("merchant_id")["d"] for pid, grp in rel_ps.groupby("pair_id")}
    coh_f = {}
    for c in fams:
        g_rl = preg[(preg["model_family"] == c) & (preg["pair_kind"] == "release_shadow")].sort_values("t")
        vecs = [(str(rl_log.loc[runs[row.run_a]["excluded_release"], "feature_groups_changed"]).strip(), ser[row.pair_id])
                for row in g_rl.itertuples(index=False)]
        sc_ = []
        for i1 in range(len(vecs)):
            for i2 in range(i1 + 1, len(vecs)):
                if vecs[i1][0] == vecs[i2][0]:
                    common = vecs[i1][1].index.intersection(vecs[i2][1].index)
                    sc_.append(float(np.corrcoef(vecs[i1][1].loc[common], vecs[i2][1].loc[common])[0, 1]))
        coh_f[c] = float(np.mean(sc_))

    rm = sheet(os.path.join(T, "feature_platform_roadmap_2027.xlsx"), "2027 roadmap")
    rm["t"] = rm["target_refresh"].map(wk)
    rel_q = {c: [] for c in fams}
    for a, b_ in s27:
        sub_r = rm[(rm["t"] > a) & (rm["t"] <= b_)]
        for c in fams:
            hits = [row for row in sub_r.itertuples(index=False) if c in str(row.model_families_touched).split(";")]
            plive = [1.0 - cov[c][int(row.t)] for row in hits]
            v = sum(p_ * inst.loc[c, "release_shadow"] for p_ in plive)
            for i1 in range(len(hits)):
                for i2 in range(i1 + 1, len(hits)):
                    if str(hits[i1].feature_groups).strip() == str(hits[i2].feature_groups).strip():
                        v += 2.0 * min(plive[i1], plive[i2]) * coh_f[c] * inst.loc[c, "release_shadow"]
            rel_q[c].append(v)
    rel_pts = math.sqrt(sum(wt[c] * np.mean(rel_q[c]) for c in fams))
    ok("S3 feature releases (independent) matches figures.json",
       abs(rel_pts - fig["points"]["feature releases"]) < 0.03, (rel_pts, fig["points"]["feature releases"]))

    # Forced sources & combined Q1..Q4 + year
    ret_pts = math.sqrt(sum(wt[c] * inst.loc[c, "retune_shadow"] * GAP / 4.0 for c in fams))
    lab_pts = math.sqrt(sum(wt[c] * inst.loc[c, "label_freeze"] * GAP for c in fams))
    ok("Retunes independently matches figures.json", abs(ret_pts - fig["points"]["retunes"]) < 0.02, (ret_pts, fig["points"]["retunes"]))
    ok("Label revisions independently matches figures.json", abs(lab_pts - fig["points"]["label revisions"]) < 0.02, (lab_pts, fig["points"]["label revisions"]))

    tot_q = []
    for qi in range(4):
        ms_q = sum(wt[c] * (opt13[c] + tur_q[c][qi] + rel_q[c][qi] +
                            inst.loc[c, "retune_shadow"] * GAP / 4.0 + inst.loc[c, "label_freeze"] * GAP)
                   for c in fams)
        tot_q.append(math.sqrt(ms_q))
    tot_yr = math.sqrt(float(np.mean([x ** 2 for x in tot_q])))
    for qi in range(4):
        ok("Combined Q%d independently matches figures.json" % (qi + 1),
           abs(tot_q[qi] - fig["tot_q%d" % (qi + 1)]) < 0.03, (tot_q[qi], fig["tot_q%d" % (qi + 1)]))
    ok("Combined 2027 year independently matches figures.json",
       abs(tot_yr - fig["tot_yr"]) < 0.03, (tot_yr, fig["tot_yr"]))

    # Evaluate golden workbook formulas with LibreOffice Calc and verify EVERY formula evaluates cleanly with 0 errors!
    wb_path = os.path.join(G, "garrane_score_stability_sources_2027.xlsx")
    tmp = tempfile.mkdtemp(prefix="verify-calc-")
    try:
        subprocess.run(["libreoffice", "--headless", "--convert-to", "xlsx", "--outdir", tmp, wb_path],
                       check=True, capture_output=True, text=True)
        eval_wb = load_workbook(os.path.join(tmp, os.path.basename(wb_path)), data_only=True)
        errs = []
        for sname in eval_wb.sheetnames:
            ws = eval_wb[sname]
            for row in ws.iter_rows(values_only=True):
                for v in row:
                    if isinstance(v, str) and any(tok in v for tok in ("#REF!", "#DIV/0!", "#VALUE!", "#NAME?", "#N/A", "Err:")):
                        errs.append((sname, v))
        ok("Golden workbook evaluates cleanly in LibreOffice Calc with 0 formula errors", not errs, errs[:5])
        ws1 = eval_wb["2027 placements"]
        wb_map = {ws1.cell(r, 1).value.lower(): (ws1.cell(r, 3).value, ws1.cell(r, 4).value) for r in range(5, 10)}
        for name, val in fig["points"].items():
            ok("Workbook evaluated %s matches figures.json" % name,
               abs(float(wb_map[name][0]) - val) < 0.02, (wb_map[name][0], val))
        for qi in range(4):
            ok("Workbook evaluated combined Q%d matches figures.json" % (qi + 1),
               abs(float(ws1.cell(12 + qi, 3).value) - fig["tot_q%d" % (qi + 1)]) < 0.02,
               (ws1.cell(12 + qi, 3).value, fig["tot_q%d" % (qi + 1)]))
        ok("Workbook evaluated combined 2027 year matches figures.json",
           abs(float(ws1.cell(16, 3).value) - fig["tot_yr"]) < 0.02, (ws1.cell(16, 3).value, fig["tot_yr"]))
        ok("Workbook evaluated pinned share matches figures.json",
           abs(float(ws1.cell(19, 2).value) - fig["cc_pin"]) < 0.1, (ws1.cell(19, 2).value, fig["cc_pin"]))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print("verify: %d PASS, %d FAIL" % (N["pass"], N["fail"]))
    sys.exit(1 if N["fail"] else 0)


if __name__ == "__main__":
    main()
