"""The seed sweep behind architecture 7's world (generator/common.py's settings): for each seed, every service's
December SLI under each weighting and each incident attribution on the world's own kept spans (no pack is cut), and
the margins the design needs (the golden list; partner-gateway, fares and notifications each over only with both the
root weights and the right attribution; journey-search and accounts within on every route; the 26 December incident
out-slowed by accounts on the latency share). Seed 2711 was chosen from 2700 to 2829.

    python3 seed_sweep.py 2700 2830 > sweep.jsonl"""
import json
import sys
import warnings

import numpy as np

warnings.filterwarnings("ignore")
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
import common as K   # noqa: E402
import world as W    # noqa: E402

H = W.H
GOLD = ["fares", "places", "seat-map", "partner-gateway", "notifications"]


def sec(d, h, m, s=0):
    return W._sec(d, h, m, s)


def analyse(w, verbose=True):
    sp = w.sp
    srv = sp["kind"] == "SERVER"
    inwin = (sp["t0"] >= 0) & (sp["t0"] < H * 3600)
    root = srv & (sp["parent"] == -1)
    rs, rh = {}, {}
    for t, s, t0 in zip(sp["trace"][root], sp["svc"][root], sp["t0"][root]):
        rs[t] = s
        rh[t] = int(t0 // 3600)
    Kr = {e: np.bincount((sp["t0"][root & inwin & (sp["svc"] == e)] // 3600).astype(int), minlength=H) for e in K.EDGE}
    N = {s: w.N[s][W.DEC0:W.DEC0 + H].astype(float) for s in K.SVC}
    posts_end = {x["id"]: max(sec(*p[2]) for p in x["posts"]) for x in K.DEC_INCIDENTS}
    kids = {}
    for k in np.nonzero(sp["kind"] == "CLIENT")[0]:
        kids.setdefault(int(sp["parent"][k]), []).append((float(sp["t0"][k]), float(sp["t0"][k]) + sp["ms"][k] / 1000))
    self_ms = np.array(sp["ms"], dtype=float)
    for k in np.nonzero(srv)[0]:
        ch = kids.get(int(sp["sid"][k]))
        if not ch:
            continue
        ch.sort()
        tot, cur = 0.0, None
        for a_, b_ in ch:
            if cur is None or a_ > cur[1]:
                if cur:
                    tot += cur[1] - cur[0]
                cur = [a_, b_]
            else:
                cur[1] = max(cur[1], b_)
        tot += cur[1] - cur[0]
        self_ms[k] = max(0.0, sp["ms"][k] - tot * 1000)
    data = {}
    for s in K.SVC:
        sel = np.nonzero(srv & inwin & (sp["svc"] == s))[0]
        tr = sp["trace"][sel]
        t0 = sp["t0"][sel]
        h = (t0 // 3600).astype(int)
        slow = (sp["ms"][sel] > K.THRESHOLD[s]).astype(float)
        e = [rs.get(x) for x in tr]
        he = [rh.get(x, -1) for x in tr]
        w_root = np.array([N[ee][hh] / Kr[ee][hh] if ee is not None and 0 <= hh < H and Kr[ee][hh] > 0 else np.nan
                           for ee, hh in zip(e, he)])
        Kh = np.bincount(h, minlength=H).astype(float)
        w_own = N[s][h] / np.maximum(Kh[h], 1)
        w_root = np.where(np.isnan(w_root), w_own, w_root)
        data[s] = dict(t0=t0, h=h, slow=slow, w_root=w_root, w_own=w_own, op=sp["op"][sel], self=self_ms[sel],
                       tr=tr)
    # incident-free hours, for the load curves
    busy = np.zeros(H, dtype=bool)
    for x in K.DEC_INCIDENTS:
        a_ = sec(*x["onset"]) // 3600
        b_ = posts_end[x["id"]] // 3600
        busy[max(0, a_ - 1):min(H, b_ + 2)] = True
    truth = {x["id"]: x["fault"] for x in K.DEC_INCIDENTS}
    first = {x["id"]: x["named"][0][0] for x in K.DEC_INCIDENTS}
    last = {x["id"]: x["named"][-1][0] for x in K.DEC_INCIDENTS}
    ev = {}
    for x in K.DEC_INCIDENTS:
        a_, b_ = sec(*x["declared"]), posts_end[x["id"]]
        rows = []
        for svc, _t in x["named"]:
            d = data[svc]
            m = (d["t0"] >= a_) & (d["t0"] < b_)
            over = float((d["w_root"][m] * d["slow"][m]).sum())
            over_k = float(d["slow"][m].sum())
            rate = over / max(float(d["w_root"][m].sum()), 1)
            # per operation: excess of the window's median self time over a load curve fitted on incident-free hours
            best = (1.0, "")
            for op in np.unique(d["op"]):
                mo = d["op"] == op
                hh = d["h"][mo]
                med = {}
                for hv in np.unique(hh):
                    v = d["self"][mo][hh == hv]
                    if len(v) >= 3:
                        med[hv] = np.median(v)
                xs = np.array([np.log(N[svc][hv] + 1) for hv in med if not busy[hv]])
                ys = np.array([np.log(med[hv]) for hv in med if not busy[hv]])
                if len(xs) < 30:
                    continue
                cf = np.polyfit(xs, ys, 2)
                mw = m & mo
                if mw.sum() < 5:
                    continue
                pred = np.exp(np.polyval(cf, np.log(N[svc][d["h"][mw]] + 1)))
                ratio = float(np.exp(np.median(np.log(np.maximum(d["self"][mw], 1e-3)) - np.log(pred))))
                if ratio > best[0]:
                    best = (ratio, op)
            rows.append((svc, over, over_k, rate, best[0], best[1], int(m.sum())))
        ev[x["id"]] = rows
    most = {i: max(r, key=lambda z: z[1])[0] for i, r in ev.items()}
    mostk = {i: max(r, key=lambda z: z[2])[0] for i, r in ev.items()}
    rate = {i: max(r, key=lambda z: z[3])[0] for i, r in ev.items()}
    loadx = {i: max(r, key=lambda z: z[4])[0] for i, r in ev.items()}
    schemes = {"golden": truth, "first": first, "last": last, "most": most, "mostk": mostk, "rate": rate,
               "loadx": loadx, "none": None}
    res = {}
    for name, att in schemes.items():
        excl = {s: [] for s in K.SVC}
        if att is not None:
            for x in K.DEC_INCIDENTS:
                for svc, t in x["named"]:
                    if svc != att[x["id"]]:
                        excl[svc].append((sec(*t), posts_end[x["id"]]))
        for wname in ("w_root", "w_own", "unw"):
            out = {}
            for s in K.SVC:
                d = data[s]
                keep = np.ones(len(d["t0"]), dtype=bool)
                for a_, b_ in excl[s]:
                    keep &= ~((d["t0"] >= a_) & (d["t0"] < b_))
                ww = np.ones(len(d["t0"])) if wname == "unw" else d[wname]
                out[s] = 100 * (ww[keep] * d["slow"][keep]).sum() / ww[keep].sum()
            res[(name, wname)] = out
    hits = {k: sum(v[i] == truth[i] for i in truth) for k, v in schemes.items() if v is not None and k != "golden"}
    if False:
        print("attribution hits of %d: %s" % (len(truth), hits))
        for i, rows in ev.items():
            print("  %s fault %-15s " % (i, truth[i]) + "; ".join(
                "%s w%.0f k%.0f r%.3f lx%.2f(%s) n%d" % r for r in rows))
        cols = [("golden", "w_root"), ("golden", "w_own"), ("none", "w_root"), ("first", "w_root"), ("last", "w_root"),
                ("most", "w_root"), ("mostk", "w_root"), ("rate", "w_root"), ("loadx", "w_root"), ("most", "w_own")]
        print("%-16s %4s | %s" % ("service", "bud", " ".join("%-10s" % ("/".join(c)[:10]) for c in cols)))
        for s in K.SVC:
            print("%-16s %4.1f | %s" % (s, K.BUDGET[s], " ".join(
                "%-10s" % ("%.2f%s" % (res[c][s], "*" if round(res[c][s] + 1e-9, 1) > K.BUDGET[s] else "")) for c in cols)))
        for c in cols:
            print("over %-16s %s" % ("/".join(c), [s for s in K.SVC if round(res[c][s] + 1e-9, 1) > K.BUDGET[s]]))
    return res, ev, data, hits


def main(lo, hi):
    for seed in range(lo, hi):
        res, ev, data, hits = analyse(W.World(seed=seed), verbose=False)
        g = res[("golden", "w_root")]
        over = [s for s in K.SVC if round(g[s] + 1e-9, 1) > K.BUDGET[s]]
        i5 = {r[0]: r[3] for r in ev[[x["id"] for x in K.DEC_INCIDENTS if x["fault"] == "notifications"][0]]}
        rec = {"seed": seed, "gold": over == GOLD,
               "margin": round(min(abs(g[s] - (K.BUDGET[s] + 0.05)) for s in K.SVC), 3),
               "pg": round(g["partner-gateway"], 3),
               "pg_x": round(max(res[("first", "w_root")]["partner-gateway"], res[("last", "w_root")]["partner-gateway"]), 3),
               "fares": round(g["fares"], 3),
               "fa_x": round(max(res[("first", "w_root")]["fares"], res[("last", "w_root")]["fares"]), 3),
               "notif": round(g["notifications"], 3),
               "no_x": round(max(res[("most", "w_root")]["notifications"], res[("rate", "w_root")]["notifications"],
                                 res[("loadx", "w_root")]["notifications"]), 3),
               "own": {s: round(res[("golden", "w_own")][s], 3) for s in ("fares", "partner-gateway", "notifications")},
               "i5_rate_acc_minus_notif": round(i5["accounts"] - i5["notifications"], 3), "hits": hits}
        print(json.dumps(rec), flush=True)


if __name__ == "__main__":
    main(int(sys.argv[1]), int(sys.argv[2]))
