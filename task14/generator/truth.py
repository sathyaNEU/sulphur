"""task14: the true measure from the simulated world (never shipped, never read by the golden): register spans as 2.2
defines them, the rent truly payable on each day (2.3), the dwellings as they are. checks.py compares the golden to it."""
import numpy as np
import pandas as pd

import measure as MS
import world as WD


def spans(W):
    T = W.T
    df = pd.DataFrame({"tid": np.arange(W.n_t), "dw": T["dwelling"], "start": T["start"], "refund": T["refund"],
                       "bonded": T["bonded"]})
    df = df[df["bonded"]].sort_values(["dw", "start"], kind="stable")
    nxt = df.groupby("dw")["start"].shift(-1)
    end = df["refund"] - 1
    df["end"] = np.where(nxt.notna() & (nxt - 1 < end), nxt - 1, end)
    return df


def rents_on(W, tids, n):
    CH = W.CH
    ch = pd.DataFrame({"t": CH["tenancy"], "d": CH["date"], "r": CH["rent"]})
    ch = ch[ch["d"] <= n].sort_values(["t", "d"]).groupby("t")["r"].last()
    r = W.T["rent0"][tids].astype(float).copy()
    s = pd.Series(np.arange(len(tids)), index=tids)
    hit = ch.index.intersection(s.index)
    r[s.loc[hit].values] = ch.loc[hit].values
    return r


def in_place(S, n):
    m = S[(S["start"] <= n) & (S["end"] >= n)]
    m = m.sort_values(["dw", "start"]).drop_duplicates("dw", keep="last")
    return m.set_index("dw")["tid"]


def measure(W, S, t2, t1):
    A, B = in_place(S, t1), in_place(S, t2)
    c = A.index.intersection(B.index)
    a, b = A.loc[c].values, B.loc[c].values
    r1, r2 = rents_on(W, a, t1), rents_on(W, b, t2)
    reg = np.array([W.dw["region"][d] for d in c])
    same = a == b
    out = {"NAT": 100 * (r2.sum() / r1.sum() - 1), "same": 100 * (r2[same].sum() / r1[same].sum() - 1),
           "relet": 100 * (r2[~same].sum() / r1[~same].sum() - 1), "n_relet": int((~same).sum())}
    for gi, g in enumerate(MS.REGIONS):
        k = reg == gi
        out[g] = 100 * (r2[k].sum() / r1[k].sum() - 1)
    return out


def truth():
    W = WD.build()
    WD.index_changes(W)
    S = spans(W)
    out = {"sep26": measure(W, S, MS.quarter_end(2026, 3), MS.quarter_end(2025, 3)),
           "dec26": measure(W, S, MS.day(2026, 12, 31), MS.day(2025, 12, 31)),
           "series": {"%dQ%d" % (y, q): measure(W, S, MS.quarter_end(y, q), MS.quarter_end(y - 1, q))["NAT"]
                      for (y, q) in MS.quarters()},
           "held": int(len(in_place(S, MS.quarter_end(2026, 3))))}
    return out
