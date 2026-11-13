"""The simulation's own truth, for the checks only (never shipped): the year's loss and the fleet at the stocktakes,
and the 2027 summer run at normal weather with the plans (the kegs in circulation in each size's busiest week, the
original fleet still usable then, the Maplestead pubs' kegs, the Foundry cold store, the busiest delivery week)."""
import datetime as dt
from collections import defaultdict

import pandas as pd

import build as B
import params as P


def truth(w, plans):
    out = {}
    st = {d: s for d, s in w.ev["stock"]}

    def lr(d):
        s = st[d]
        return ({z: s[z].get("LOST", 0) + s[z].get("RECOVERY", 0) for z in P.SIZES},
                {z: sum(v for k, v in s[z].items() if k not in ("LOST", "RECOVERY", "SCRAP")) for z in P.SIZES})
    l1, u1 = lr(dt.date(2025, 11, 30))
    l2, u2 = lr(P.ASOF)
    out["loss"] = {z: l2[z] - l1[z] for z in P.SIZES}
    out["fleet"] = u2
    tr = B.truth(w, plans)
    rows = []
    for d, c, orig, est, fgf in tr["daily"]:
        for z in P.SIZES:
            v = c[z]
            rows.append((d, z, sum(v.values()) - v.get("BREWERY", 0), orig[z], est[z], fgf[z]))
    df = pd.DataFrame(rows, columns=["d", "s", "inuse", "orig", "est", "fgf"])
    df["wk"] = pd.to_datetime(df.d).dt.to_period("W-SUN")
    wk = df.groupby(["s", "wk"]).mean(numeric_only=True)
    f = pd.DataFrame(tr["ev"]["fill"], columns=["d", "id", "size", "sku"])
    f["d"] = pd.to_datetime(f.d)
    dl = pd.DataFrame(tr["ev"]["deliver"], columns=["d", "id", "o", "size", "sku"])
    dl["wk"] = pd.to_datetime(dl.d).dt.to_period("W-SUN")
    for z in P.SIZES:
        x = wk.loc[z]
        i = x.inuse.idxmax()
        ss = f[(f["size"] == z) & (f.d >= "2027-05-03") & (f.d <= "2027-09-26")]
        flt = 2 * len(ss) / (21 * 6)
        dws = dl[dl["size"] == z].groupby("wk").size()
        season = [p for p in dws.index if pd.Timestamp("2027-05-03") <= p.start_time <= pd.Timestamp("2027-09-20")]
        out[str(z)] = {"week": str(i.end_time.date()), "inuse": float(x.loc[i].inuse), "orig": float(x.loc[i].orig),
                       "estate": float(x.loc[i].est), "store": float(x.loc[i].fgf), "float": flt,
                       "need": float(x.loc[i].inuse + flt), "buy": float(x.loc[i].inuse + flt - x.loc[i].orig),
                       "deliv": int(dws[season].max())}
    return out
