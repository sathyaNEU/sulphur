"""An independent recomputation of task6's graded figures from the shipped bundle alone (target/, figures.json and
submission.md), on its own code path: pandas over the span export, each trace's root found by walking parents, the
weights from the balancer's export, its own reading of each December incident's cause (the first fifteen-minute bin,
from three hours before the declaration, where a named service's own handling ran 1.4 times its median at the same
hour on December's other days, held for the next bin too), the exclusions, the SLIs, the incident minutes, the
start order and shares, and the linearised intervals. Returns a list of disagreements; empty is a pass.

    python3 verify.py [task_dir]"""
import datetime as dt
import json
import os
import re
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DEC0 = pd.Timestamp("2026-12-01")
H = 744


def half_up(x, q):
    from decimal import Decimal, ROUND_HALF_UP
    return float(Decimal(repr(float(x))).quantize(Decimal(q), rounding=ROUND_HALF_UP))


def lisbon_utc(local):
    t = pd.Timestamp(local)
    yr = t.year
    def last_sun(m):
        d = pd.Timestamp(yr, m, 31)
        return d - pd.Timedelta(days=(d.weekday() + 1) % 7)
    start, end = last_sun(3) + pd.Timedelta(hours=1), last_sun(10) + pd.Timedelta(hours=1)
    u = t - pd.Timedelta(hours=1)
    return u if start <= u < end else t


def run(task_dir):
    tgt = os.path.join(task_dir, "target")
    F = json.load(open(os.path.join(HERE, "figures.json")))
    bad = []
    cat = pd.read_excel(os.path.join(tgt, "service_catalogue_2026.xlsx"), sheet_name="Services")
    by_trace = dict(zip(cat["Tracing service name"], cat["Service"]))
    by_tg = dict(zip(cat["Load balancer target group (from 1 Jul 2026)"], cat["Service"]))
    comp = dict(zip(cat["Service"], cat["Status page component"]))
    from docx import Document
    d = Document(os.path.join(tgt, "PR-SLO-3_service_level_objectives_2026.docx"))
    thr, bud = {}, {}
    for row in d.tables[0].rows[1:]:
        c = [x.text for x in row.cells]
        thr[c[0]], bud[c[0]] = float(c[2].replace(",", "")), float(c[3].rstrip("%"))
    svcs = list(thr)

    sp = pd.read_parquet(os.path.join(tgt, "trace_spans_2026-12.parquet"))
    sp = sp.drop_duplicates("span_id")
    sp = sp[sp["span_name"] != "GET /healthz"].copy()
    sp["svc"] = sp["service_name"].map(by_trace)
    sp["t"] = (sp["start_time_unix_nano"] - DEC0.value) / 1e9
    sp["ms"] = (sp["end_time_unix_nano"] - sp["start_time_unix_nano"]) / 1e6
    sp["h"] = np.floor(sp["t"] / 3600).astype(int)
    srv = sp[sp["span_kind"] == "SPAN_KIND_SERVER"].copy()
    roots = srv[(srv["parent_span_id"] == "") & (srv["h"] >= 0) & (srv["h"] < H)]
    root_of = roots.set_index("trace_id")[["svc", "h"]]
    kroot = roots.groupby(["svc", "h"]).size()

    lb = pd.read_csv(os.path.join(tgt, "lb_target_group_requests_2026-H2.csv"))
    lb["t"] = pd.to_datetime(lb["TimePeriodStart"].str.replace("Z", ""))
    lb = lb[lb["t"] >= DEC0].copy()
    lb["svc"] = lb["TargetGroupName"].map(by_tg)
    lb["h"] = ((lb["t"] - DEC0).dt.total_seconds() // 3600).astype(int)
    N = lb.set_index(["svc", "h"])["RequestCount"].astype(float)

    dec = srv[(srv["h"] >= 0) & (srv["h"] < H)].copy()
    dec = dec.join(root_of.rename(columns={"svc": "rsvc", "h": "rh"}), on="trace_id")
    own_k = dec.groupby(["svc", "h"]).size()
    def wt(r):
        if pd.isna(r.rsvc):
            return N[(r.svc, r.h)] / own_k[(r.svc, r.h)]
        return N[(r.rsvc, int(r.rh))] / kroot[(r.rsvc, int(r.rh))]
    dec["w"] = [wt(r) for r in dec.itertuples()]
    dec["slow"] = dec["ms"] > dec["svc"].map(thr)

    # own handling: the span less the union of its client children
    cl = sp[sp["span_kind"] == "SPAN_KIND_CLIENT"][["parent_span_id", "t", "ms"]].copy()
    cl["e"] = cl["t"] + cl["ms"] / 1000
    cov = {}
    for pid, grp in cl.sort_values("t").groupby("parent_span_id"):
        tot, a_, b_ = 0.0, None, None
        for s_, e_ in zip(grp["t"], grp["e"]):
            if a_ is None or s_ > b_:
                if a_ is not None:
                    tot += b_ - a_
                a_, b_ = s_, e_
            else:
                b_ = max(b_, e_)
        cov[pid] = tot + (b_ - a_)
    dec["own"] = np.maximum(0.001, dec["ms"] - dec["span_id"].map(cov).fillna(0) * 1000)

    # the incidents
    st = json.load(open(os.path.join(tgt, "status_page_history_2026.json")))
    posts = [(set(p["components"]), lisbon_utc(p["created_at"])) for p in st["incidents"]]
    ops = {}
    for c in st["component_status_changes"]:
        if c["status"] == "operational":
            ops.setdefault(c["component"], []).append(lisbon_utc(c["at"]))
    tl = pd.read_csv(os.path.join(tgt, "incident_timeline_2026.csv"))
    added = tl[tl["event"] == "service added"]
    named_at = {(r.incident_id, by_trace[r.detail]): pd.Timestamp(r.at_utc) for r in added.itertuples()}
    inc = pd.read_csv(os.path.join(tgt, "incidents_2026.csv"))
    incs = []
    for r in inc.itertuples():
        decl = pd.Timestamp(r.declared_at_utc)
        names = [by_trace[x] for x in r.services.split(";")]
        m = [p for p in posts if p[0] & {comp[x] for x in names} and
             pd.Timedelta(0) <= p[1] - decl.floor("min") <= pd.Timedelta(minutes=15)]
        if not m:
            continue
        end = max(min(t for t in ops[c] if t > m[0][1]) for c in m[0][0])
        incs.append({"id": r.incident_id, "declared": decl, "end": end,
                     "named": [(x, named_at[(r.incident_id, x)]) for x in names]})
    decinc = [x for x in incs if x["declared"] >= DEC0]

    # each December incident's cause: the earliest held rise of a named service's own handling over its load
    dec["lo"] = np.log(dec["own"])
    quiet = pd.Series(True, index=range(H))
    for x in decinc:
        a_ = int((x["declared"] - DEC0).total_seconds() // 3600) - 3
        b_ = int((x["end"] - DEC0).total_seconds() // 3600) + 1
        quiet.loc[max(0, a_):min(H - 1, b_)] = False
    cause = {}
    for x in decinc:
        t0 = (x["declared"] - DEC0).total_seconds() - 3 * 3600
        t1 = (x["end"] - DEC0).total_seconds()
        firsts = {}
        for s, _ in x["named"]:
            best = None
            for name, g in dec[dec["svc"] == s].groupby("span_name"):
                hm = g[g["h"].map(quiet)].groupby("h")["lo"].agg(["median", "size"])
                hm = hm[hm["size"] >= 3]
                if len(hm) < 30:
                    continue
                ld = np.log(np.array([N[(s, h)] for h in hm.index]) + 1)
                cf = np.polyfit(ld, hm["median"].values, 2)
                w = g[(g["t"] >= t0) & (g["t"] < t1)].sort_values("t")
                if len(w) < 24:
                    continue
                res = w["lo"].values - np.polyval(cf, np.log(np.array([N[(s, h)] for h in w["h"]]) + 1))
                # one changepoint: the split of the time-ordered residuals that best separates two means, kept when the
                # later mean sits 1.4 times above the earlier and 1.3 times above the load curve
                n_ = len(res)
                tv = w["t"].values
                if n_ >= 40:
                    c_ = np.concatenate([[0.0], np.cumsum(res)])
                    ks_ = np.arange(20, n_ - 19)
                    ks_ = ks_[(tv[-1] - tv[np.minimum(ks_, n_ - 1)]) >= 1800]
                    if len(ks_):
                        m1_ = c_[ks_] / ks_
                        m2_ = (c_[-1] - c_[ks_]) / (n_ - ks_)
                        j_ = int(np.argmax(ks_ * (n_ - ks_) / n_ * (m2_ - m1_) ** 2))
                        if m2_[j_] - m1_[j_] >= np.log(2.0) and m2_[j_] >= np.log(1.75):
                            tt = tv[ks_[j_]]
                            best = tt if best is None else min(best, tt)
            if best is not None:
                firsts[s] = best
        cause[x["id"]] = min(firsts, key=firsts.get) if firsts else None
    if cause != F["root_cause"]:
        bad.append("root causes %s against %s" % (cause, F["root_cause"]))

    # exclusions and SLIs
    keep = pd.Series(True, index=dec.index)
    for x in decinc:
        for s, t in x["named"]:
            if s != cause.get(x["id"]):
                a_ = (max(x["declared"], t) - DEC0).total_seconds()
                b_ = (x["end"] - DEC0).total_seconds()
                keep &= ~((dec["svc"] == s) & (dec["t"] >= a_) & (dec["t"] < b_))
    k = dec[keep]
    num = (k["w"] * k["slow"]).groupby(k["svc"]).sum()
    den = k.groupby("svc")["w"].sum()
    # December's hours before the export's first span: each service's requests there at the share over threshold its
    # held, incident-free hours show in the same tenth of hourly load
    cut = int(np.floor(dec["t"].min() / 3600))
    quiet = np.ones(H, dtype=bool)
    for x in decinc:
        a_ = int((x["declared"] - DEC0).total_seconds() // 3600) - 3
        b_ = int((x["end"] - DEC0).total_seconds() // 3600) + 1
        quiet[max(0, a_):min(H, b_ + 1)] = False
    hourly = k.assign(o=k["w"] * k["slow"]).groupby(["svc", "h"]).agg(o=("o", "sum"), c=("w", "sum"))
    terms = {}
    for s in svcs:
        n_s = np.array([N.get((s, h_), 0.0) for h_ in range(H)])
        x_s = np.log(n_s + 1)
        O = np.zeros(H); C = np.zeros(H)
        if s in hourly.index.get_level_values(0):
            hs = hourly.loc[s]
            O[hs.index.values] = hs["o"].values; C[hs.index.values] = hs["c"].values
        fit = (np.arange(H) >= cut) & quiet & (C > 0)
        edges = np.quantile(x_s[fit], np.linspace(0, 1, 11))
        band = np.clip(np.searchsorted(edges, x_s, side="right") - 1, 0, 9)
        gone = np.arange(H) < cut
        pb = np.array([O[fit & (band == j)].sum() / max(C[fit & (band == j)].sum(), 1e-9) for j in range(10)])
        Mb = np.array([n_s[gone & (band == j)].sum() for j in range(10)])
        Cb = np.array([C[fit & (band == j)].sum() for j in range(10)])
        num[s] = num[s] + float((Mb * pb).sum())
        den[s] = den[s] + float(Mb.sum())
        terms[s] = (pb[band], (Mb / np.maximum(Cb, 1e-9))[band], fit, float(Mb.sum()))
    sli = 100 * num / den
    for s in svcs:
        if "%.1f" % half_up(sli[s], "0.1") != F["sli"][s]:
            bad.append("%s SLI %.3f against %s" % (s, sli[s], F["sli"][s]))
    over = [s for s in svcs if half_up(sli[s], "0.1") > bud[s]]
    if over != F["over"]:
        bad.append("over %s against %s" % (over, F["over"]))
    order = sorted(over, key=lambda s: -num[s])
    tot = num.sum()
    cells = {"order": ", ".join(order), "together": "%d" % half_up(100 * num[over].sum() / tot, "1"),
             "beyond": "{:,}".format(int(half_up(sum(num[s] - bud[s] / 100 * den[s] for s in over) / 10000, "1")) * 10000)}
    for s in order:
        cells["share %s" % s] = "%d" % half_up(100 * num[s] / tot, "1")
    if cells != F["programme_cells"]:
        bad.append("programme %s against %s" % (cells, F["programme_cells"]))

    # the intervals: linearised over strata of root service and hour, traces as units
    for s in over:
        R = sli[s] / 100
        ks = k[k["svc"] == s].copy()
        ph, Ah, fit, M = terms[s]
        sl = ks["slow"].astype(float).values
        hh = ks["h"].values
        ks["z"] = (sl - R) + np.where(fit[hh], Ah[hh] * (sl - ph[hh]), 0.0)
        zt = ks.groupby("trace_id")["z"].sum()
        X = ks["w"].sum() + M
        rr = roots[["trace_id", "svc", "h"]].copy()
        rr["z"] = rr["trace_id"].map(zt).fillna(0.0)
        rr["n"] = rr.groupby(["svc", "h"])["trace_id"].transform("size")
        rr["N"] = [N[(a, b)] for a, b in zip(rr["svc"], rr["h"])]
        rr["u"] = rr["N"] / rr["n"] * rr["z"] / X
        V = 0.0
        for (_, _), g in rr.groupby(["svc", "h"]):
            n = len(g)
            if n < 2:
                continue
            f = min(1.0, n / max(g["N"].iloc[0], 1))
            V += (1 - f) * n / (n - 1) * ((g["u"] - g["u"].mean()) ** 2).sum()
        orph = ks[ks["rsvc"].isna()]
        if len(orph) > 1:
            u = orph["w"] * orph["z"] / X
            V += len(u) / (len(u) - 1) * ((u - u.mean()) ** 2).sum()
        se = 100 * np.sqrt(V)
        lo, hi = half_up(sli[s] - 1.6448536269514722 * se, "0.01"), half_up(sli[s] + 1.6448536269514722 * se, "0.01")
        if abs(lo - F["ci_cells"]["%s lo" % s]) > 0.011 or abs(hi - F["ci_cells"]["%s hi" % s]) > 0.011:
            bad.append("%s interval %.2f to %.2f against %s to %s" % (s, lo, hi, F["ci_cells"]["%s lo" % s],
                                                                    F["ci_cells"]["%s hi" % s]))

    # incident minutes by half, Lisbon halves
    h1_end = pd.Timestamp("2026-06-30 23:00")
    for s in svcs:
        iv = sorted((max(x["declared"], t), x["end"]) for x in incs for s_, t in x["named"] if s_ == s
                    and max(x["declared"], t) < x["end"])
        merged = []
        for a_, b_ in iv:
            if merged and a_ <= merged[-1][1]:
                merged[-1][1] = max(merged[-1][1], b_)
            else:
                merged.append([a_, b_])
        m = [0.0, 0.0]
        for a_, b_ in merged:
            for i, (lo_, hi_) in enumerate(((pd.Timestamp("2026-01-01"), h1_end), (h1_end, pd.Timestamp("2027-01-01")))):
                x0, x1 = max(a_, lo_), min(b_, hi_)
                if x1 > x0:
                    m[i] += (x1 - x0).total_seconds() / 60
        got = ["%d" % half_up(v, "1") for v in m]
        if got != F["minutes"][s]:
            bad.append("%s minutes %s against %s" % (s, got, F["minutes"][s]))

    # every figure the answer blocks state is one the figure set carries
    sub = open(os.path.join(task_dir, "submission.md")).read()
    for s in svcs:
        if "%s: SLI %s against a budget of %s" % (s, F["sli"][s], F["budget"][s]) not in sub:
            bad.append("submission lacks %s's SLI line" % s)
    return bad


if __name__ == "__main__":
    td = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(HERE)
    b = run(td)
    print("verify: %s" % ("PASS" if not b else "FAIL\n  " + "\n  ".join(b)))
    sys.exit(1 if b else 0)
