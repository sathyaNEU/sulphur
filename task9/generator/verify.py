"""task9 (architecture 10): an independent recompute of the graded figures from the installed pack, by other code:
plain pandas parsing of both export generations, rivals' levels joined by merge_asof, each trade's cost adjusted for
the market by first-order duration rather than full repricing, and the replay summed per segment. Every figure must land
inside figures.json's bands. Exit 1 on any FAIL.
"""
import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TGT = os.path.join(TASK, "target")
sys.path.insert(0, HERE)
import pack as PK  # noqa: E402
import params as P  # noqa: E402

H = 30
OFF = {("IG", "liquid"): 1.2, ("IG", "medium"): 2.4, ("IG", "thin"): 4.8, ("HY", "liquid"): 4.2, ("HY", "medium"): 8.4,
       ("HY", "thin"): 15.6}


def load():
    a = pd.read_csv(os.path.join(TGT, PK.F["rfq1"]))
    b = pd.read_csv(os.path.join(TGT, PK.F["rfq2"]))
    a = a.rename(columns={"RFQ_ID": "rfq", "MSG_VERSION": "ver", "CUSIP": "cusip", "CLIENT_CODE": "client", "QTY": "q",
                          "DESK_RESPONSE_PX": "quote", "DESK_REF_MID": "ref", "COVER_PX": "cover"})
    a["ts"] = pd.to_datetime(a.RECEIVED_ET).dt.tz_localize(P.ZONE)
    a["side"] = a.CLIENT_SIDE.map({"BUY": 1, "SELL": -1})
    a["st"] = a.STATUS.map({"Done": "D", "Covered": "C", "Traded Away": "TA", "Done Not Traded": "DNT", "Passed": "P"})
    b = b.rename(columns={"rfq_ref": "rfq", "msg_version": "ver", "security_id": "cusip", "response_price": "quote",
                          "ref_mid": "ref", "cover_price": "cover", "outcome": "st"})
    b["ts"] = pd.to_datetime(b.received_utc, utc=True).dt.tz_convert(P.ZONE)
    b["q"] = b.quantity_000 * 1000
    b["side"] = b.dir.map({"CB": 1, "CS": -1})
    cols = ["rfq", "ver", "ts", "cusip", "client", "side", "q", "quote", "ref", "st", "cover"]
    R = pd.concat([a[cols], b[cols]]).drop_duplicates()
    R = R.sort_values("ver").groupby("rfq").tail(1).sort_values("ts").reset_index(drop=True)
    return R


def main():
    F = json.load(open(os.path.join(HERE, "figures.json")))
    bands, g = F["bands"], F["gold"]
    R = load()
    sm = pd.read_csv(os.path.join(TGT, PK.F["master"]))
    key = dict(zip(sm.cusip, sm.cusip))
    key.update({r: c for c, r in zip(sm.cusip, sm.registered_cusip) if isinstance(r, str)})
    R["k"] = R.cusip.map(key)
    R["date"] = R.ts.dt.tz_localize(None).dt.normalize()
    cl = pd.read_csv(os.path.join(TGT, PK.F["clients"]))
    R["ty"] = R.client.map(dict(zip(cl.client_code, cl.client_type.map({v: k for k, v in PK.TYPE_NAME.items()}))))
    bk = pd.read_csv(os.path.join(TGT, PK.F["buckets"]))
    bk["k"] = bk.cusip.map(key)
    R["quarter"] = R.date.dt.to_period("Q").astype(str)
    R = R.merge(bk[["quarter", "k", "liquidity_bucket"]].drop_duplicates(["quarter", "k"]), on=["quarter", "k"], how="left")
    rt = pd.read_csv(os.path.join(TGT, PK.F["ratings"]), parse_dates=["effective_date"])
    iss = dict(zip(sm.cusip, sm.issuer))
    R["issuer"] = R.k.map(iss)
    R = R.sort_values("date")
    rt = rt.sort_values("effective_date")
    R = pd.merge_asof(R, rt.rename(columns={"effective_date": "date"}), on="date", by="issuer", direction="backward")
    R["band"] = np.where(R.rating.isin(list(P.IG)), "IG", "HY")
    R["seg"] = R.band + "|" + R.liquidity_bucket + "|" + R.ty
    # schedules
    xl = pd.ExcelFile(os.path.join(TGT, PK.F["schedule"]))

    def sched(df):
        df = df.iloc[3:].dropna(subset=[df.columns[0]])
        df = df[df.iloc[:, 0].isin(["IG", "HY"])]
        return {"%s|%s|%s" % (r.iloc[0], r.iloc[1], {v: k for k, v in PK.TYPE_NAME.items()}[r.iloc[2]]): float(r.iloc[3])
                for _, r in df.iterrows()}
    v = [sched(pd.read_excel(xl, s, header=None)) for s in ("v1", "v2", "v3")]
    dr = sched(pd.read_excel(os.path.join(TGT, PK.F["draft"]), header=None))
    R["h_act"] = np.select([R.date < "2024-07-01", R.date < "2025-03-03"], [R.seg.map(v[0]), R.seg.map(v[1])], R.seg.map(v[2]))
    R["h_cur"] = R.seg.map(v[2])
    R["h_new"] = R.seg.map(dr)
    R["d"] = R.side * (R.quote - R.ref) * 100
    # rivals' levels: the cover on a win, the nearest later print on a loss
    tp = pd.read_csv(os.path.join(TGT, PK.F["tape"]), dtype={"qty": str})
    gone = set(tp.orig_seq.dropna().astype(int))
    tp = tp[(tp.msg_type != "X") & ~tp.msg_seq.isin(gone) & (tp.contra == "C")].copy()
    tp["k"] = tp.cusip.map(key)
    tp["ts"] = pd.to_datetime(tp.exec_date + " " + tp.exec_time).dt.tz_localize(P.ZONE)
    tp["qn"] = pd.to_numeric(tp.qty, errors="coerce")
    R["r"] = np.where(R.st == "D", R.side * (R.cover - R.ref) * 100, np.nan)
    lost = R[R.st.isin(["C", "TA"])].copy()
    lost["rs"] = np.where(lost.side > 0, "S", "B")
    lost["capq"] = np.where(lost.band == "IG", P.CAP["IG"], P.CAP["HY"])
    out = []
    for (kk, rs), grp in lost.groupby(["k", "rs"]):
        t2 = tp[(tp.k == kk) & (tp.rpt_side == rs)].sort_values("ts")
        if t2.empty:
            continue
        grp = grp.sort_values("ts")
        m = pd.merge_asof(grp, t2[["ts", "price", "qn", "qty"]].rename(columns={"ts": "pts"}), left_on="ts", right_on="pts",
                          direction="forward", tolerance=pd.Timedelta(seconds=180))
        okq = (m.qty.str.endswith("+").fillna(False) & (m.q > m.capq)) | (np.abs(m.qn - m.q) < 0.5)
        m = m[okq & m.price.notna()]
        out.append(m[["rfq", "price"]])
    mt = pd.concat(out).drop_duplicates("rfq")
    R = R.merge(mt, on="rfq", how="left")
    R.loc[R.price.notna(), "r"] = (R.side * (R.price - R.ref) * 100)[R.price.notna()]
    dq = R.side * (R.quote - R.ref) * 100
    R.loc[R.st.isin(["C", "TA"]) & (R.r > dq + 1e-9), "r"] = np.nan     # a loss to a worse print is no match
    # costs: the evaluation 30 days on, net of the Treasury's move and the median spread move of other issuers' bonds of
    # the same rating, both to first order in modified duration
    ev = pd.read_csv(os.path.join(TGT, PK.F["eval"]))
    ev["k"] = ev.cusip.map(key)
    E = ev.pivot_table(index="eval_date", columns="k", values="eval_mid")
    days = pd.to_datetime(E.index)
    tix = {d: i for i, d in enumerate(days)}
    curve = pd.DataFrame({t: pd.read_csv(os.path.join(TGT, t + ".csv"), index_col=0).iloc[:, 0] for t in
                          ["DGS1", "DGS2", "DGS3", "DGS5", "DGS7", "DGS10", "DGS20", "DGS30"]})
    curve.index = pd.to_datetime(curve.index)
    curve = curve.apply(pd.to_numeric, errors="coerce").ffill().reindex(days).ffill() / 100.0
    ten = np.array([1, 2, 3, 5, 7, 10, 20, 30.0])
    smi = sm.set_index("cusip")
    mat_d = pd.to_datetime(smi.maturity.reindex(E.columns)).values
    cpn = smi.coupon_pct.reindex(E.columns).values / 100.0
    yrs = (mat_d[None, :] - days.values[:, None]) / np.timedelta64(1, "D") / 365.25
    yrs = np.maximum(yrs, 1 / 365)
    tsy = np.vstack([np.interp(np.clip(yrs[t], 1, 30), ten, curve.values[t]) for t in range(len(days))])

    def px(y, c, m):
        n = np.maximum(np.ceil(m * 2 - 1e-9), 1)
        acc = n - m * 2
        r = y / 2
        ann = np.where(np.abs(r) > 1e-12, (1 - (1 + r) ** (-n)) / r, n)
        return (c * 50 * ann + 100 * (1 + r) ** (-n)) * (1 + r) ** acc - c * 50 * acc
    Ev = E.values
    lo, hi = np.full(Ev.shape, -0.05), np.full(Ev.shape, 0.6)
    for _ in range(60):                                       # bisection for each evaluated yield
        mid = (lo + hi) / 2
        up = px(mid, cpn[None, :], yrs) > Ev
        lo = np.where(up, mid, lo)
        hi = np.where(up, hi, mid)
    yld = (lo + hi) / 2
    spr = np.where(np.isnan(Ev), np.nan, yld - tsy)
    h = 1e-4
    dmod = (px(yld - h, cpn[None, :], yrs) - px(yld + h, cpn[None, :], yrs)) / (2 * h * px(yld, cpn[None, :], yrs))
    iss_of = smi.issuer.reindex(E.columns).values
    rt2 = rt.sort_values("effective_date")
    long = pd.DataFrame({"t": np.repeat(np.arange(1, len(days)), len(E.columns)),
                         "j": np.tile(np.arange(len(E.columns)), len(days) - 1),
                         "ds": np.diff(spr, axis=0).ravel()})
    long = long.dropna()
    long["issuer"] = iss_of[long.j.values]
    long["date"] = days[long.t.values]
    long = pd.merge_asof(long.sort_values("date"), rt2.rename(columns={"effective_date": "date"}), on="date", by="issuer")
    med = {}
    for (t, r), grp in long.groupby(["t", "rating"]):
        for i in grp.issuer.unique():
            x = grp.ds[grp.issuer != i]
            med[(t, r, i)] = float(np.median(x)) if len(x) else 0.0
    R["t0"] = R.date.map(tix)
    R = R[R.t0.notna()].copy()
    R["t0"] = R.t0.astype(int)
    R["t1"] = np.minimum(R.t0 + H, len(days) - 1)
    col = {c: j for j, c in enumerate(E.columns)}
    R["j"] = R.k.map(col)
    e1 = Ev[R.t1.values, R.j.values].copy()
    for ix in np.where(np.isnan(e1))[0]:
        c = Ev[R.t0.values[ix]:R.t1.values[ix] + 1, R.j.values[ix]]
        c = c[~np.isnan(c)]
        e1[ix] = c[-1] if len(c) else R.ref.values[ix]
    rate_move = np.zeros(len(R))
    for n_, (t0, t1, j, r, i) in enumerate(zip(R.t0.values, R.t1.values, R.j.values, R.rating.values, R.issuer.values)):
        rate_move[n_] = sum(med.get((t, r, i), 0.0) for t in range(t0 + 1, t1 + 1))
    dT = tsy[R.t1.values, R.j.values] - tsy[R.t0.values, R.j.values]
    d0 = np.nan_to_num(dmod[R.t0.values, R.j.values], nan=5.0)
    p0 = np.nan_to_num(Ev[R.t0.values, R.j.values], nan=100.0)
    mkt = -d0 * p0 * (dT + rate_move)
    R["cost"] = R.side * ((e1 - R.ref) - mkt) * 100
    R["traded"] = R.st.isin(["D", "C", "TA"])
    R["won"] = R.st == "D"
    R["off"] = [OFF[(a, bb)] for a, bb in zip(R.band, R.liquidity_bucket)]
    base = (R.date >= P.BASE_FROM) & (R.date <= P.BASE_TO)
    sc = (R[base].groupby("seg").size() / R.groupby("seg").size()).fillna(0)
    d = np.nan_to_num(R.d.values)
    dc = d * R.h_cur / R.h_act
    dp = d * R.h_new / R.h_act
    known = R.traded & R.r.notna()
    wc = known & ((dc < R.r) | (R.won & (dc <= R.r + 1e-9)))
    wp = known & ((dp < R.r) | (R.won & (dp <= R.r + 1e-9)))
    R["pc"] = np.where(wc, (dc - R.cost - R.off) * R.q / 1e4, 0) * R.seg.map(sc)
    R["pp"] = np.where(wp, (dp - R.cost - R.off) * R.q / 1e4, 0) * R.seg.map(sc)
    cur, prop = R.pc.sum(), R.pp.sum()
    res = []

    def ok(name, cond, detail):
        res.append((bool(cond), name, detail))
    ok("the current schedule's 2027 P&L inside its band", bands["current"][0] <= cur <= bands["current"][1],
       "%.2f in [%.2f, %.2f]" % (cur / 1e6, bands["current"][0] / 1e6, bands["current"][1] / 1e6))
    ok("the draft's 2027 P&L inside its band", bands["proposed"][0] <= prop <= bands["proposed"][1],
       "%.2f in [%.2f, %.2f]" % (prop / 1e6, bands["proposed"][0] / 1e6, bands["proposed"][1] / 1e6))
    br = (R.groupby("seg").pp.sum() - R.groupby("seg").pc.sum())
    lose = sorted(s for s in F["segments"] if br.get(s, 0) < 0)
    ok("the changed segments that lose money", set(lose) - set(F.get("lose_either", [])) == set(g["lose"]) - set(F.get("lose_either", [])),
       "%s against %s" % (lose, g["lose"]))
    inb = [s for s in F["segments"] if bands["bridge"][s][0] <= br.get(s, 0) <= bands["bridge"][s][1]]
    ok("each changed segment's difference inside its band", len(inb) >= len(F["segments"]) - 1,
       "%d of %d" % (len(inb), len(F["segments"])))
    sh = {s: float(wp[R.seg == s].sum() / (R.seg == s).sum()) for s in F["segments"]}
    ins = [s for s in F["segments"] if bands["share"][s][0] <= sh[s] <= bands["share"][s][1]]
    ok("each changed segment's win share inside its band", len(ins) == len(F["segments"]), "%d of %d" % (len(ins), len(F["segments"])))
    wcst = {s: float(np.average(R.cost[(R.seg == s) & wc], weights=R.q[(R.seg == s) & wc]) * 100) for s in F["segments"]}
    inc = [s for s in F["segments"] if bands["won_cost"][s][0] <= wcst[s] <= bands["won_cost"][s][1]]
    ok("the cost a million on the trades the current schedule wins inside its band", len(inc) >= len(F["segments"]) - 1,
       "%d of %d; outside %s" % (len(inc), len(F["segments"]), {s: (round(wcst[s]), [round(x) for x in bands["won_cost"][s]])
                                                               for s in F["segments"] if s not in inc}))
    am = wp & ~wc
    acst = {s: float(np.average(R.cost[(R.seg == s) & am], weights=R.q[(R.seg == s) & am]) * 100) for s in F["segments"]
            if ((R.seg == s) & am).any()}
    ina = [s for s in acst if bands["add_cost"][s][0] <= acst[s] <= bands["add_cost"][s][1]]
    ok("the cost a million on the trades the draft adds inside its band", len(ina) >= len(acst) - 1, "%d of %d" % (len(ina), len(acst)))
    for p, name, dd in res:
        print("%-5s %-60s %s" % ("PASS" if p else "FAIL", name, dd))
    print("verify: %d of %d PASS" % (sum(p for p, _, _ in res), len(res)))
    return 0 if all(p for p, _, _ in res) else 1


if __name__ == "__main__":
    sys.exit(main())
