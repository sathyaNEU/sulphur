"""task9: every graded figure, computed on the cut pack by analysis.py: the golden, the rivals that set each result's
band (reasonable methods that differ), and the routes a hurried analyst takes (each one judgment taken the quick way).
"""
import json

import numpy as np
import pandas as pd

import analysis as AN
import params as P
from record import Record

SIMS = 3000
GOLD = dict()
RIVALS = {
    "an infant term fading over two months": dict(infant=2.0),
    "an infant term fading over four months": dict(infant=4.0),
    "each family's own age slope, unshrunk": dict(shrink=False),
    "the ramp read as exponential alone": dict(hot="ramp"),
    "the ramp read as linear alone": dict(hot="linear"),
    "another seed for the draws": dict(seed=P.SEED + 101),
}
RECORD_RIVALS = {"DC-3's ages from the mean deploy lag": dict(lag="mean")}
ROUTES = {
    "ages from the inventory": dict(ages="first_seen"),
    "the hot batch at its recent rate": dict(hot="flat"),
    "the hot batch inside its family": dict(hot="family"),
    "one curve per family over every vault": dict(frailty=False),
    "every removal in the age curve": dict(events="all"),
    "Poisson counts at the fitted values": dict(spread="poisson"),
    "careful but hurried": dict(frailty=False, spread="poisson", hot="ramp"),
}
MARGIN = dict(count=0.06, rate=0.006, share=0.08)


def summarize(A, rec, sims=SIMS):
    rows, counts, mean = A.simulate(P.FORECAST_Q, sims=sims, draws=(A.spread == "overdispersed"))

    def total(sel):
        idx = [j for j, r in enumerate(rows) if sel(r)]
        return counts[:, idx].sum(axis=1)
    out = {}
    t = total(lambda r: True)
    out["total"] = float(t.mean())
    out["total_band"] = [float(np.percentile(t, P.BAND[0])), float(np.percentile(t, P.BAND[1]))]
    out["path"], out["path_band"] = {}, {}
    for q in P.FORECAST_Q:
        x = total(lambda r: r["q"] == q)
        out["path"][q] = float(x.mean())
        out["path_band"][q] = [float(np.percentile(x, P.BAND[0])), float(np.percentile(x, P.BAND[1]))]
    out["by_dc"] = {dc: float(total(lambda r: r["dc"] == dc).mean()) for dc in AN.DCS}
    out["by_dc_q"] = {dc: {q: float(total(lambda r: r["dc"] == dc and r["q"] == q).mean()) for q in P.FORECAST_Q} for dc in AN.DCS}
    out["by_family"] = {f: float(total(lambda r: r["family"] == f).mean()) for f in AN.FAMS + ["X-24"]}
    out["dc3"] = out["by_dc"]["DC-3"]
    x = total(lambda r: r["dc"] == "DC-3")
    out["dc3_band"] = [float(np.percentile(x, P.BAND[0])), float(np.percentile(x, P.BAND[1]))]
    h = total(lambda r: r["hot"])
    out["hot_count"] = float(h.mean())
    out["hot_band"] = [float(np.percentile(h, P.BAND[0])), float(np.percentile(h, P.BAND[1]))]
    out["om6"] = out["by_family"]["OM-6"]
    out["hot_rate"] = float(AN.current_rate(A))
    D = AN.decisions(A, sims=sims)
    out["spares"] = {f: v["order"] for f, v in D["spares"].items()}
    out["spares_p90"] = {f: v["p90"] for f, v in D["spares"].items()}
    out["migrate"] = bool(D["frac_mean"] > D["breakeven"])
    out["p_pays"] = D["p_pays"]
    out["frac24"] = D["frac_mean"]
    out["flip_doubling"] = D["flip_doubling"]
    out["hot_drives"] = D["hot_drives"]
    cov, cells = AN.backtest(rec, sims=sims, **A.kwargs)
    out["coverage"] = cov
    out["backtest_cells"] = len(cells)
    return out


def quick(rec):
    """The close-out's last quarter, rate by data centre carried at today's drives for four quarters."""
    d = rec.d
    a, b = AN.qbounds("2026Q3")
    live = d[(d.exit_c >= pd.Timestamp(P.END)) & ~(d.event & (d.exit <= pd.Timestamp(P.END)))] if "exit_c" in d else None
    out = {}
    tot = 0.0
    for dc in AN.DCS:
        x = d[d.dc == dc]
        lo = np.maximum(x.entry.values.astype("datetime64[D]"), np.datetime64(a.date()))
        hi = np.minimum(x.exit.values.astype("datetime64[D]"), np.datetime64(b.date()))
        ex = np.clip((hi - lo).astype(float), 0, None).sum() / 365.25
        ev = int((x.event & (x.removal_date >= a) & (x.removal_date < b)).sum())
        n_live = int(((x.exit >= pd.Timestamp(P.END)) & ~(x.event & (x.removal_date <= pd.Timestamp(P.END)))).sum())
        out[dc] = ev / max(ex, 1e-9) * n_live
        tot += out[dc]
    return dict(total=tot, by_dc=out, path={q: tot / 4 for q in P.FORECAST_Q})


def compute(tgt, sims=SIMS):
    rec = Record(tgt)
    F = {"record": dict(drives=int(len(rec.d)), migrated=rec.migrated, deploy_lag=rec.deploy_lag,
                        age_sources=rec.d.age_source.value_counts().to_dict(), hot_drives_seen=int(rec.d.hot.sum()))}
    A = AN.Analysis(rec)
    A.kwargs = {}
    g = summarize(A, rec, sims)
    g["hot_weights"] = A.hot["weights"]
    g["infant_months"] = A.infant_months
    g["spur_rate"] = A.spur
    g["dispersion_k"] = A.k
    g["fleet_slope"] = A.pool["fleet_slope"]
    g["om6_frailty"] = {v: a / b for (f, v), (a, b) in A.vault_ab.items() if f == "OM-6"}
    F["gold"] = g
    riv = {}
    for name, kw in RIVALS.items():
        Ar = AN.Analysis(rec, **kw)
        Ar.kwargs = kw
        riv[name] = summarize(Ar, rec, sims)
    for name, kw in RECORD_RIVALS.items():
        r2 = Record(tgt, lag_days=float(np.mean((rec.d[(rec.d.family == "HX-8") & rec.d.build.notna() & (rec.d.install_date > pd.Timestamp(P.REC_START))].install_date
                                                 - rec.d[(rec.d.family == "HX-8") & rec.d.build.notna() & (rec.d.install_date > pd.Timestamp(P.REC_START))].build).dt.days)))
        Ar = AN.Analysis(r2)
        Ar.kwargs = {}
        riv[name] = summarize(Ar, r2, sims)
    F["rivals"] = riv
    routes = {}
    for name, kw in ROUTES.items():
        Ar = AN.Analysis(rec, **kw)
        Ar.kwargs = kw
        routes[name] = summarize(Ar, rec, sims)
    routes["the close-out's rates carried"] = quick(rec)
    F["routes"] = routes
    F["bands"] = bands(g, riv)
    return F


def _band(vals, margin, rel=True):
    lo, hi = min(vals), max(vals)
    if rel:
        return [lo * (1 - margin), hi * (1 + margin)]
    return [lo - margin, hi + margin]


def bands(g, riv):
    allv = [g] + list(riv.values())
    b = {}
    for k in ("total", "dc3", "hot_count", "om6"):
        b[k] = _band([v[k] for v in allv], MARGIN["count"])
    b["path"] = {q: _band([v["path"][q] for v in allv], MARGIN["count"]) for q in P.FORECAST_Q}
    b["path_lo"] = {q: _band([v["path_band"][q][0] for v in allv], MARGIN["count"]) for q in P.FORECAST_Q}
    b["path_hi"] = {q: _band([v["path_band"][q][1] for v in allv], MARGIN["count"]) for q in P.FORECAST_Q}
    b["total_lo"] = _band([v["total_band"][0] for v in allv], MARGIN["count"])
    b["total_hi"] = _band([v["total_band"][1] for v in allv], MARGIN["count"])
    b["hot_rate"] = _band([v["hot_rate"] for v in allv], MARGIN["rate"], rel=False)
    b["coverage"] = _band([v["coverage"] for v in allv], MARGIN["share"], rel=False)
    b["spares"] = {f: _band([v["spares"][f] for v in allv], 0.10) for f in g["spares"]}
    b["flip_doubling"] = _band([v["flip_doubling"] for v in allv], 0.10)
    b["p_pays"] = _band([v["p_pays"] for v in allv], 0.05, rel=False)
    return b


def write(F, path):
    json.dump(F, open(path, "w"), indent=1, sort_keys=True, default=float)
