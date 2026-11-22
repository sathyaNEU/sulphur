"""task9 architecture 5: an independent recomputation of the golden from the shipped files.

    python3 task9/generator/verify.py

Nothing here imports the generator. The pack is read with the csv and json modules and pandas, the workbooks with
openpyxl, and each step is written again from the answer blocks' own description: the panel on one merchant key
(the later load kept, Tolka Pay's old ids mapped), each instrument's pair variance by family, the bootstrap pairs'
per-row noise carried to the rows each 2027 snapshot pair turns over, the gap curve over the settled warm weeks fitted
with a saturating term tied to the replicate pairs (a bounded continuous minimiser where the golden searches a grid),
the take-up lag on custom components from the three past rollouts carried to the pinned views, the roadmap's releases
on the weeks a family is not on them, the shares, the remainder and the tier changes. Every graded figure is then held
against figures.json and the golden workbook's first sheet."""
import csv
import datetime as dt
import glob
import json
import math
import os
import sys
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
    reg = pd.read_csv(os.path.join(T, "gms_model_registry.csv")).set_index("model_family")
    fams = sorted(reg.index)
    sched = dict(zip(reg["scheduler_job_family"], reg.index))
    custom = {c: (0 if pd.isna(v) else len(str(v).split(";"))) for c, v in reg["custom_training_components"].items()}

    book = pd.read_csv(os.path.join(T, "gms_scored_book_by_family.csv"))
    book = book[book["snapshot_date"] == "2026-09-21"].set_index("model_family")["scored_merchants"].astype(float)
    wt = book / book.sum()

    # the manifests, retried lines dropped
    runs = {}
    for line in open(os.path.join(T, "training_scheduler_runs_2024_2026.jsonl")):
        m = json.loads(line)
        runs.setdefault(m["run_id"], m)
    prod = defaultdict(dict)
    for m in runs.values():
        if m["kind"] == "production":
            prod[sched[m["job_family"]]][iso(m["iso_week"])] = m
    TT = max(max(v) for v in prod.values()) + 1
    window, last_cold = {}, {}
    for c in fams:
        lens = [iso(m["window_last_week"]) - iso(m["window_first_week"]) + 1 for m in prod[c].values()]
        window[c] = max(set(x for x in lens if x > 26), key=lens.count)
        last_cold[c] = max(t for t, m in prod[c].items() if m["parent_model_id"] is None)

    # the panel: one key per merchant, the later load where a refresh was re-sent
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
    ok("the panel holds 29,580 merchants on one key", sum(len(v) for v in idx.values()) == 29580,
       sum(len(v) for v in idx.values()))

    # the instruments: the mean over each kind's pairs of the variance of the score difference
    preg = pd.read_csv(os.path.join(T, "mrm_instrument_pair_register_2026.csv"))
    ps = pd.read_csv(os.path.join(T, "mrm_instrument_pair_scores_2026.csv"))
    ps["d"] = ps["score_a"] - ps["score_b"]
    pv = ps.groupby("pair_id")["d"].var(ddof=0)
    preg["v"] = preg["pair_id"].map(pv)
    inst = preg.groupby(["model_family", "pair_kind"])["v"].mean().unstack()
    bn = preg[preg["pair_kind"] == "bootstrap"].assign(
        n=lambda x: x["run_a"].map(lambda r: runs[r].get("train_rows", runs[r].get("rows")))).groupby("model_family")["n"].mean()

    # labelled rows by week, the warehouse then the plan
    wr = pd.read_csv(os.path.join(T, "warehouse_labelled_rows_weekly.csv"))
    rows = defaultdict(dict)
    for r in wr.itertuples(index=False):
        rows[r.model_family][wk(r.label_week)] = float(r.labelled_rows)
    pl = sheet(os.path.join(T, "labelled_row_plan_2027.xlsx"), "Labelled rows")
    for r in pl.to_dict("records"):
        for c in fams:
            rows[c][wk(r["label_week"])] = float(r[c])

    def window_rows(c, t):
        return np.array([rows[c][u] for u in range(t - window[c] + 1, t + 1)])

    def change_var(c, t0, t1):
        """Per unit of per-row noise: the variance of (mean of window at t1) less (mean of window at t0)."""
        a, b = window_rows(c, t0), window_rows(c, t1)
        h = t1 - t0
        na, nb = a.sum(), b.sum()
        shared = a[h:].sum()
        return a[:h].sum() / na ** 2 + b[-h:].sum() / nb ** 2 + shared * (1 / na - 1 / nb) ** 2

    s26 = [(wk(SNAP26[i]), wk(SNAP26[i + 1])) for i in range(3)]
    s27 = [(wk(SNAP27[i]), wk(SNAP27[i + 1])) for i in range(4)]
    face = (inst["bootstrap"] - inst["replicate"]).clip(lower=0)
    per_row = face / 2.0 * bn
    tur26 = {c: per_row[c] * np.mean([change_var(c, a, b) for a, b in s26]) for c in fams}
    tur27 = {c: per_row[c] * np.mean([change_var(c, a, b) for a, b in s27]) for c in fams}

    # the gap curve over the settled warm weeks, the saturating term tied to the replicate pairs
    opt13, slope, phi_, A_, d13, d1 = {}, {}, {}, {}, {}, {}
    for c in fams:
        t0 = max(last_cold[c] + 13, 66)
        X = Z[c]
        D = np.array([np.nanmean((X[:, t0 + h:TT] - X[:, t0:TT - h]) ** 2) for h in range(1, 27)])
        d13[c], d1[c] = D[12], D[0]
        h = np.arange(1, 27)
        rep = inst.loc[c, "replicate"]
        wgt = 1 / D ** 2

        def sse(phi):
            A = rep / (1 - phi ** 2)
            g = 1 - phi ** h
            b = np.sum(wgt * h * (D - A * g)) / np.sum(wgt * h * h)
            return float(np.sum(wgt * (D - b * h - A * g) ** 2))
        grid = np.linspace(0.5, 0.985, 98)
        start = grid[int(np.argmin([sse(p) for p in grid]))]
        res = minimize_scalar(sse, bounds=(max(0.5, start - 0.01), min(0.985, start + 0.01)), method="bounded",
                              options={"xatol": 1e-6})
        phi = res.x
        A = rep / (1 - phi ** 2)
        g = 1 - phi ** h
        slope[c] = np.sum(wgt * h * (D - A * g)) / np.sum(wgt * h * h)
        phi_[c], A_[c] = phi, A
        opt13[c] = A * (1 - phi ** GAP)

    # take-up of pinned views from the three past rollouts, carried by custom components
    cal = sheet(os.path.join(T, "platform_change_calendar.xlsx"), "Changes")
    test = {"PC-24-031": lambda m: m["runtime_image"] == "garrane-train:4.1.0",
            "PC-24-047": lambda m: m["options"]["warm_start"] is True,
            "PC-25-012": lambda m: m["options"]["precision"] == "bf16"}
    lag, cus, slip, rev = [], [], [], []
    for ref, on in test.items():
        c_ = cal[cal["change_ref"] == ref].set_index("model_family")
        for c in fams:
            seq = [on(prod[c][t]) for t in range(TT)]
            first = seq.index(True)
            done = wk(c_.loc[c, "completed_on"])
            plan = iso(c_.loc[c, "planned_week"])
            lag.append(max(first - done, 1))
            cus.append(custom[c])
            slip.append(done - plan)
            off = [t for t in range(first, min(first + 26, TT)) if not seq[t]]
            rev.append(len(off) / 26.0)
    beta = np.polyfit(cus, np.log(lag), 1)
    resid = np.log(lag) - np.polyval(beta, cus)
    sg = math.sqrt(np.sum(resid ** 2) / (len(resid) - 2))
    mslip, mrev = float(np.mean(slip)), float(np.mean(rev))
    pin = cal[cal["change"].str.startswith("Pinned feature views")].set_index("model_family")
    weeks = np.arange(wk("2026-12-28") - 1, wk("2027-12-20") + 1)       # the golden's grid of 2027 weeks
    cov = {}
    for c in fams:
        x = weeks - (iso(pin.loc[c, "planned_week"]) + mslip)
        mu = np.polyval(beta, custom[c])
        cdf = np.where(x > 0, norm.cdf((np.log(np.maximum(x, 1e-9)) - mu) / sg), 0.0)
        cov[c] = cdf * (1 - mrev)
    cc3 = 100.0 * np.mean([cov[c][1:] for c in fams])

    # feature releases: the roadmap's on the weeks a family is not on pinned views, 2026's as recorded
    rm = sheet(os.path.join(T, "feature_platform_roadmap_2027.xlsx"), "2027 roadmap")
    rel27, rel26 = {}, {}
    rl = pd.read_csv(os.path.join(T, "feature_platform_release_log.csv"))
    for c in fams:
        hits = [wk(r["target_refresh"]) for r in rm.to_dict("records") if c in str(r["model_families_touched"]).split(";")]
        rel27[c] = inst.loc[c, "release_shadow"] * sum(1 - cov[c][t - weeks[0]] for t in hits) / 4.0
        t0 = max(last_cold[c] + 13, 66)
        ev = np.zeros(TT)
        for r in rl.itertuples(index=False):
            if c in str(r.model_families_touched).split(";"):
                ev[wk(r.first_scored_refresh)] += 1
        cs = np.cumsum(ev)
        s = np.arange(t0, TT - GAP)
        rel26[c] = inst.loc[c, "release_shadow"] * float(np.mean(cs[s + GAP] - cs[s]))
    ret13 = {c: inst.loc[c, "retune_shadow"] * GAP / 4.0 for c in fams}
    lab13 = {c: inst.loc[c, "label_freeze"] * GAP for c in fams}

    comp = {"optimisation noise": opt13, "training data": tur27, "retunes": ret13, "feature releases": rel27,
            "label revisions": lab13}
    agg = {k: sum(wt[c] * v[c] for c in fams) for k, v in comp.items()}
    pts = {k: math.sqrt(v) for k, v in agg.items()}
    side = sum(agg.values())
    share = {k: 100 * v / side for k, v in agg.items()}
    own = {c: max(d13[c] - (opt13[c] + tur26[c] + ret13[c] + lab13[c] + rel26[c]), 0.0) for c in fams}
    own_a = sum(wt[c] * own[c] for c in fams)
    own_share = 100 * own_a / (own_a + side)
    band = {k: ("escalation" if p >= 8 else "a remediation plan" if p >= 5.5 else "monitor") for k, p in pts.items()}

    # tier changes: each family's 2026 rate scaled by the root of its movement ratio
    cuts = np.array([400.0, 500.0, 600.0])
    fr26 = {}
    for c in fams:
        v = []
        for a, b in s26:
            m = ~np.isnan(Z[c][:, b]) & ~np.isnan(Z[c][:, a])
            v.append(np.mean(np.searchsorted(cuts, Z[c][m, a], side="right") != np.searchsorted(cuts, Z[c][m, b], side="right")))
        fr26[c] = np.mean(v)
    v26 = {c: opt13[c] + tur26[c] + ret13[c] + rel26[c] + lab13[c] + own[c] for c in fams}
    v27 = {c: opt13[c] + tur27[c] + ret13[c] + rel27[c] + lab13[c] + own[c] for c in fams}
    gone = {c: sum(comp[k][c] for k in comp if band[k] != "monitor") for c in fams}
    fr_s = 100 * sum(wt[c] * fr26[c] * math.sqrt(v27[c] / v26[c]) for c in fams)
    fr_r = 100 * sum(wt[c] * fr26[c] * math.sqrt(max(v27[c] - gone[c], 0) / v26[c]) for c in fams)

    # against figures.json and the golden workbook
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    for k in pts:
        ok("%s points %.3f against figures.json %.3f" % (k, pts[k], fig["points"][k]), abs(pts[k] - fig["points"][k]) < 0.03)
        ok("%s share %.2f against figures.json %.2f" % (k, share[k], fig["share"][k]), abs(share[k] - fig["share"][k]) < 0.3)
        ok("%s band" % k, band[k] == fig["band_of"][k], (band[k], fig["band_of"][k]))
    ok("pinned-views share %.2f against %.2f" % (cc3, fig["cc3"]), abs(cc3 - fig["cc3"]) < 0.1)
    ok("merchants' own share %.2f against %.2f" % (own_share, fig["own_share"]), abs(own_share - fig["own_share"]) < 0.3)
    ok("tier changes %.2f against %.2f" % (fr_s, fig["fr_sched"]), abs(fr_s - fig["fr_sched"]) < 0.1)
    ok("tier changes removed %.2f against %.2f" % (fr_r, fig["fr_removed"]), abs(fr_r - fig["fr_removed"]) < 0.1)
    ok("weekly variance on the record %.2f against %.2f" % (sum(wt[c] * d1[c] for c in fams), fig["falsification"]["record"]),
       abs(sum(wt[c] * d1[c] for c in fams) - fig["falsification"]["record"]) < 0.05)
    ok("the fit's weekly variance %.2f against %.2f" % (
        sum(wt[c] * (slope[c] + A_[c] * (1 - phi_[c])) for c in fams), fig["falsification"]["golden"]),
       abs(sum(wt[c] * (slope[c] + A_[c] * (1 - phi_[c])) for c in fams) - fig["falsification"]["golden"]) < 0.3)
    for k in pts:
        ok("%s inside the stated band" % k, fig["stated"]["points_" + {"optimisation noise": "optimisation",
           "training data": "turnover", "retunes": "retunes", "feature releases": "releases",
           "label revisions": "labels"}[k]][0] <= pts[k] <= fig["stated"]["points_" + {"optimisation noise": "optimisation",
           "training data": "turnover", "retunes": "retunes", "feature releases": "releases",
           "label revisions": "labels"}[k]][1])
    ws = load_workbook(os.path.join(G, "garrane_score_stability_sources_2027.xlsx"), read_only=True,
                       data_only=True)["2027 placements"]
    got = {r[0].lower(): r for r in ws.iter_rows(min_row=5, max_row=9, values_only=True)}
    for k in pts:
        r = got[k]
        ok("workbook %s: %s points, %s per cent" % (k, r[1], r[2]),
           abs(r[1] - round(fig["points"][k], 2)) < 1e-9 and abs(r[2] - round(fig["share"][k], 1)) < 1e-9)
    print("verify: %d pass, %d fail" % (N["pass"], N["fail"]))
    return 1 if N["fail"] else 0


if __name__ == "__main__":
    sys.exit(main())
