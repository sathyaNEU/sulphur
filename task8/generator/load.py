"""Read the shipped pack back into the arrays the estimators use. Nothing here reads the generator's world: every
array comes from the files under target/, in each board's own layout, on one schema (series as a year, centres by
national roll number, one candidate per series, centre and number)."""
import os

import numpy as np
import pandas as pd

import core as C
import pack as PK
import world as WL

YEARS, NY = C.YEARS, C.NY


def _year(s):
    return s.astype(str).str.extract(r"(\d{4})")[0].astype(int)


def read_board(target, b, roll_of):
    lay, F = WL.INFO[b]["layout"], PK.names_for(b)
    sep = ";" if lay == 2 else ","
    p = lambda k: os.path.join(target, F[k])  # noqa: E731
    # ---- mark sheets
    m = pd.read_csv(p("marks"), sep=sep, dtype=str, keep_default_na=False)
    m.columns = ["series", "centre", "cand", "status", "centre_mark", "awarded_mark"]
    n_raw = len(m)
    m = m.drop_duplicates()
    m["series"] = _year(m["series"])
    m["roll"] = m["centre"].map(roll_of)
    m["cand"] = m["cand"].astype(int)
    m["marked"] = m["status"].isin(["M", "OK", "Marked"])
    m["centre_mark"] = pd.to_numeric(m["centre_mark"], errors="coerce")
    m["awarded_mark"] = pd.to_numeric(m["awarded_mark"], errors="coerce")
    assert m["roll"].notna().all() and (m["marked"] == m["centre_mark"].notna()).all()
    assert not m.duplicated(["series", "roll", "cand"]).any()
    # ---- moderation samples
    if lay == 2:
        raw = pd.read_csv(p("samples"), sep=sep, dtype=str, keep_default_na=False)
        raw["Version"] = raw["Version"].astype(int)
        n_ver = len(raw)
        raw = raw.sort_values("Version").drop_duplicates(["Series", "RollNo"], keep="last")
        recs = []
        for r in raw.itertuples(index=False):
            for cd, a, mm in zip(r.Candidates.split("|"), r.CentreMarks.split("|"), r.ModeratorMarks.split("|")):
                recs.append((int(r.Series), int(r.RollNo), int(cd), int(a), int(mm), r.Moderator))
        s = pd.DataFrame(recs, columns=["series", "roll", "cand", "centre_mark", "moderator_mark", "moderator"])
        o = pd.DataFrame(dict(series=raw["Series"].astype(int), roll=raw["RollNo"].astype(int),
                              applied=raw["MarksApplied"].astype(int), sampled=raw["Sampled"].astype(int)))
        o["mean_diff"] = np.nan
    else:
        s = pd.read_csv(p("samples"), dtype=str, keep_default_na=False)
        s.columns = ["series", "centre", "cand", "centre_mark", "moderator_mark", "moderator"]
        s["series"] = _year(s["series"])
        s["roll"] = s["centre"].map(roll_of)
        for c in ("cand", "centre_mark", "moderator_mark"):
            s[c] = s[c].astype(int)
        o = pd.read_csv(p("outcomes"), dtype=str) if lay == 1 else pd.read_excel(p("outcomes"), dtype=str)
        o.columns = ["record", "series", "centre", "moderator", "sampled", "mean_diff", "outcome", "applied", "issued"]
        n_ver = len(o)
        o["series"] = _year(o["series"])
        o["roll"] = o["centre"].map(roll_of)
        o["when"] = pd.to_datetime(o["issued"], format="%Y-%m-%d" if lay == 1 else "%d/%m/%Y")
        o = o.sort_values(["when", "record"]).drop_duplicates(["series", "roll"], keep="last")
        for c in ("applied", "sampled"):
            o[c] = o[c].astype(int)
        o["mean_diff"] = o["mean_diff"].astype(float)
    # ---- the standardisation meetings
    sc = pd.read_csv(p("scripts"), sep=sep, dtype=str) if lay != 3 else pd.read_excel(p("scripts"), dtype=str)
    sc.columns = ["meeting", "script", "src_series", "src_centre", "src_cand", "agreed"]
    sc["meeting"], sc["src_series"] = _year(sc["meeting"]), _year(sc["src_series"])
    sc["roll"] = sc["src_centre"].astype(int) if lay == 2 else sc["src_centre"].map(roll_of)
    sc["src_cand"], sc["agreed"] = sc["src_cand"].astype(int), sc["agreed"].astype(int)
    t = pd.read_csv(p("trial"), sep=sep, dtype=str, keep_default_na=False)
    t.columns = ["meeting", "script", "moderator", "mark"]
    t["meeting"] = _year(t["meeting"])
    t["mark"] = pd.to_numeric(t["mark"], errors="coerce")
    t = t[t["mark"].notna()].copy()
    return dict(marks=m, samples=s, outcomes=o, scripts=sc, trial=t, n_raw=n_raw, n_versions=n_ver)


def load(target):
    cen = pd.read_csv(os.path.join(target, PK.FILES["centres"]), dtype=str)
    cen["roll_no"] = cen["roll_no"].astype(int)
    reg = pd.read_csv(os.path.join(target, PK.FILES["register"]), dtype=str, keep_default_na=False)
    reg["first_series"] = reg["first_series"].astype(int)
    reg["last_series"] = reg["last_series"].replace("", str(YEARS[-1])).astype(int)
    W, raw, info = {}, {}, {}
    for b in WL.BOARDS:
        cb = cen[cen["board"] == b].sort_values("roll_no")
        rolls = cb["roll_no"].to_numpy()
        roll_of = dict(zip(cb["board_centre_no"], cb["roll_no"]))
        R = read_board(target, b, roll_of)
        raw[b] = R
        ix = {r: i for i, r in enumerate(rolls)}
        nc = len(rolls)
        m = R["marks"][R["marks"]["marked"]]
        g = m.groupby(["roll", "series"]).agg(n=("cand", "size"), mbar=("centre_mark", "mean"),
                                              adj=("centre_mark", "sum"), aw=("awarded_mark", "sum")).reset_index()
        ci, ti = g["roll"].map(ix).to_numpy(), (g["series"] - YEARS[0]).to_numpy()
        ncand, mbar, adj = np.zeros((nc, NY)), np.zeros((nc, NY)), np.zeros((nc, NY))
        ncand[ci, ti], mbar[ci, ti] = g["n"], g["mbar"]
        adj[ci, ti] = (g["adj"] - g["aw"]) / g["n"]
        s = R["samples"].copy()
        s["d"] = s["centre_mark"] - s["moderator_mark"]
        gs = s.groupby(["roll", "series"]).agg(ns=("d", "size"), G=("d", "mean")).reset_index()
        ci, ti = gs["roll"].map(ix).to_numpy(), (gs["series"] - YEARS[0]).to_numpy()
        G, ns, samp = np.full((nc, NY), np.nan), np.zeros((nc, NY)), np.zeros((nc, NY), bool)
        G[ci, ti], ns[ci, ti], samp[ci, ti] = gs["G"], gs["ns"], True
        # the rota: the commonest gap between a centre's successive samples
        yrs = np.where(samp, np.array(YEARS)[None, :], 0)
        gaps = np.concatenate([np.diff(r[r > 0]) for r in yrs])
        k = int(np.bincount(gaps).argmax()) if len(gaps) else 1
        grp = np.array([int(r[r > 0][0]) % k for r in yrs])
        assert (samp == (((np.array(YEARS)[None, :] - grp[:, None]) % k) == 0)).all(), b
        # the trial: each script's consensus, its agreed mark, and the live moderation of the portfolio it copies
        t = R["trial"]
        cons = t.groupby(["meeting", "script"])["mark"].agg(["mean", "count", "var"]).reset_index()
        sc = R["scripts"].merge(cons, on=["meeting", "script"])
        sc = sc.merge(s[["series", "roll", "cand", "centre_mark", "moderator_mark", "moderator"]],
                      left_on=["src_series", "roll", "src_cand"], right_on=["series", "roll", "cand"], how="left")
        assert sc["centre_mark"].notna().all() and len(sc) == len(R["scripts"]), b
        R["joined"] = sc
        who = s.groupby(["roll", "series"])["moderator"].first().reset_index()
        R["who"] = {(ix[r], y - YEARS[0]): m for r, y, m in who.itertuples(index=False)}
        t = t.merge(cons[["meeting", "script", "mean", "count"]], on=["meeting", "script"])
        t["dev"] = t["mark"] - t["mean"]
        t["dev_loo"] = t["dev"] * t["count"] / (t["count"] - 1)
        R["dev"] = t
        nm_eff = C.SIG_M ** 2 / float((sc["var"] / sc["count"]).mean())
        W[b] = dict(P=dict(k=k, nm=nm_eff), grp=grp, G=G, adj=adj, samp=samp, ncand=ncand, mbar=mbar, ns=ns,
                    ex_x=(sc["centre_mark"] - sc["mean"]).to_numpy(float),
                    ex_y=(sc["centre_mark"] - sc["moderator_mark"]).to_numpy(float),
                    ex_gap=(sc["mean"] - sc["agreed"]).to_numpy(float), ex_year=sc["meeting"].to_numpy(int))
        info[b] = dict(rolls=rolls, names=cb["centre_name"].tolist(), counties=cb["county"].tolist(),
                       markers=float(sc["count"].mean()), cons_se=float(np.sqrt((sc["var"] / sc["count"]).mean())),
                       count_min=int(sc["count"].min()), count_max=int(sc["count"].max()),
                       scripts=len(sc), rows=len(R["marks"]), rows_raw=R["n_raw"], versions=R["n_versions"])
    # ---- the people registered with two boards in a series, read on both boards' meetings
    D = []
    two = reg.merge(reg, on="registration_no", suffixes=("_a", "_b"))
    for a, b, _ in C.DUAL:
        pr = two[(two["board_a"] == a) & (two["board_b"] == b)]
        ra, rb, la, lb, yy = [], [], [], [], []
        da, db = raw[a]["dev"], raw[b]["dev"]
        ma = da.groupby(["moderator", "meeting"])[["dev", "dev_loo"]].mean()
        mb = db.groupby(["moderator", "meeting"])[["dev", "dev_loo"]].mean()
        for r in pr.itertuples(index=False):
            for y in range(max(r.first_series_a, r.first_series_b), min(r.last_series_a, r.last_series_b) + 1):
                key = (r.registration_no, y)
                if key in ma.index and key in mb.index:
                    ra.append(ma.loc[key, "dev"]); rb.append(mb.loc[key, "dev"])
                    la.append(ma.loc[key, "dev_loo"]); lb.append(mb.loc[key, "dev_loo"]); yy.append(y)
        D.append(dict(a=a, b=b, ra=np.array(ra), rb=np.array(rb), ra_loo=np.array(la), rb_loo=np.array(lb),
                      year=np.array(yy)))
    pairs = set(zip(two["board_a"], two["board_b"])) - {(x, x) for x in WL.BOARDS}
    info["pairs"] = sorted({tuple(sorted(pq)) for pq in pairs})
    info["appointments"] = len(reg)
    info["two_board_people"] = int((reg.groupby("registration_no")["board"].nunique() > 1).sum())
    # ---- the regulator's review
    rb_, ry = C.REFEREE
    rv = pd.read_csv(os.path.join(target, PK.FILES["review"]))
    rv["d"] = rv["centre_mark"] - rv["review_mark"]
    ix = {r: i for i, r in enumerate(info[rb_]["rolls"])}
    gr = rv.groupby("roll_no")["d"].mean()
    review = np.full(len(ix), np.nan)
    review[[ix[r] for r in gr.index]] = gr.to_numpy()
    assert not np.isnan(review).any()
    info["review_rows"] = len(rv)
    return dict(B=W, D=D, review=review, boards=C.BOARDS, cache={}), info, raw


if __name__ == "__main__":
    import sys
    world, info, raw = load(sys.argv[1])
    spec, x = C.build_spec(world) if hasattr(C, "build_spec") else (None, None)
    for b in WL.BOARDS:
        print(b, info[b]["scripts"], round(info[b]["markers"], 1), round(info[b]["cons_se"], 3), world["B"][b]["P"])
