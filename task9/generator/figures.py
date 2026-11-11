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
    "the build window a week narrower at each end": dict(hot_set="scan:-1"),
    "another seed for the draws": dict(seed=P.SEED + 101),
}
RECORD_RIVALS = {"DC-3's ages from the mean deploy lag": dict(lag="mean")}
CAREFUL = dict(frailty=False, spread="bootstrap", hot="ramp", hot_set="firmware", migrate_rule="batch")
ROUTES = {
    "ages from the inventory": dict(ages="first_seen"),
    "the hot batch at its recent rate": dict(hot="flat"),
    "the hot batch inside its family": dict(hot="family"),
    "the firmware release as the batch": dict(hot_set="firmware"),
    "the five vaults as the batch": dict(hot_set="vaults"),
    "one curve per family over every vault": dict(frailty=False),
    "every removal in the age curve": dict(events="all"),
    "Poisson counts at the fitted values": dict(spread="poisson"),
    "every batch vault on the batch's share": dict(migrate_rule="batch"),
    "the build window a week wider at each end": dict(hot_set="scan:1"),
    "careful but hurried": CAREFUL,
    "careful, each vault at its own level": dict(CAREFUL, frailty=True),
    "careful, the batch by build week": dict(CAREFUL, hot_set="scan"),
    "careful, each vault decided on its own replacements": dict(CAREFUL, migrate_rule="vault"),
}
PERTURB = {
    "the batch's hazard level 20 per cent lower": dict(hot_scale=0.8),
    "the batch's forward growth 20 per cent slower": dict(ramp_slow=1.2),
    "both together": dict(hot_scale=0.8, ramp_slow=1.2),
}
MARGIN = dict(count=0.06, rate=0.006, share=0.08)


def summarize(A, rec, sims=SIMS, backtest=True):
    rows, counts, mean = A.simulate(P.FORECAST_Q, sims=sims, draws=(A.spread != "poisson"))

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
    out["by_family_q"] = {f: {q: float(total(lambda r: r["family"] == f and r["q"] == q).mean()) for q in P.FORECAST_Q}
                          for f in AN.FAMS + ["X-24"]}
    out["by_family_band"] = {}
    for f in AN.FAMS + ["X-24"]:
        x = total(lambda r: r["family"] == f)
        out["by_family_band"][f] = [float(np.percentile(x, P.BAND[0])), float(np.percentile(x, P.BAND[1]))]
    out["by_dc_band"] = {}
    for dc in AN.DCS:
        x = total(lambda r: r["dc"] == dc)
        out["by_dc_band"][dc] = [float(np.percentile(x, P.BAND[0])), float(np.percentile(x, P.BAND[1]))]
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
    out["migrate"] = bool(len(D["migrate"]) > 0)
    out["p_pays"] = D["p_pays"]
    out["frac24"] = D["frac_mean"]
    out["flip_doubling"] = D["flip_doubling"]
    out["hot_drives"] = D["hot_drives"]
    out["hot_batch"] = {"drives": int(D["hot_drives"]), "rate": float(out["hot_rate"])}
    out["total_width"] = out["total_band"][1] - out["total_band"][0]
    out["vaults"] = D["vaults"]
    out["migrate_vaults"] = D["migrate"]
    out["rec"] = {"migrate": list(D["migrate"]), "flip": float(D["flip_doubling"])}
    w = getattr(A, "hot_window", None)
    out["hot_window"] = ["%d-W%02d" % w[0].isocalendar()[:2], "%d-W%02d" % w[1].isocalendar()[:2]] if w else None
    if backtest:
        cov, cells = AN.backtest(rec, sims=sims, **A.kwargs)
        out["coverage"] = cov
        out["backtest_cells"] = len(cells)
        out["backtest_detail"] = cells
    return out


def quick(rec):
    """Ten minutes: the close-out's last quarter, each family's replacement rate per drive in service carried at today's
    drives for four quarters; the spare order at a quarter of that; the hot vaults' last-quarter rate held for two
    years against the break-even."""
    d = rec.d
    a, b = AN.qbounds("2026Q3")
    end = pd.Timestamp(P.END)
    lo = np.maximum(d.entry.values.astype("datetime64[D]"), np.datetime64(a.date()))
    hi = np.minimum(d.exit.values.astype("datetime64[D]"), np.datetime64(b.date()))
    ex = np.clip((hi - lo).astype(float), 0, None) / 365.25
    ev = (d.event & (d.removal_date >= a) & (d.removal_date < b)).values
    live = ((d.exit >= end) & ~(d.event & (d.removal_date <= end))).values
    out = dict(by_family={}, by_dc={})
    for f in AN.FAMS:
        m = (d.family == f).values
        rate = ev[m].sum() / max(ex[m].sum(), 1e-9)
        out["by_family"][f] = float(rate * live[m].sum())
    for dc in AN.DCS:
        m = (d.dc == dc).values
        rate = ev[m].sum() / max(ex[m].sum(), 1e-9)
        out["by_dc"][dc] = float(rate * live[m].sum())
    out["total"] = float(sum(out["by_dc"].values()))
    out["path"] = {q: out["total"] / 4 for q in P.FORECAST_Q}
    out["dc3"] = out["by_dc"]["DC-3"]
    om = (d.family == "OM-6").values
    out["om6"] = float(ev[om].sum() / max(ex[om].sum(), 1e-9) * live[om].sum())
    out["spares"] = {f: max(int(np.ceil(v / 4)) - P.SPARES_ON_HAND.get(f, 0), 0) for f, v in out["by_family"].items()}
    out["spares"]["X-24"] = 0
    hv = d[(d.family == "HX-8") & (d.dc == "DC-2")]
    m = ((d.family == "HX-8") & (d.dc == "DC-2")).values
    r = ev[m].sum() / max(ex[m].sum(), 1e-9)
    frac = 1 - np.exp(-2 * r)
    be = P.COSTS["migrate_vault"] / (P.VAULT_DRIVES * P.COSTS["failure_handling"])
    out["rec"] = {"migrate": sorted(hv[hv.exit >= end].vault_id.unique().tolist()) if frac > be else [], "flip": None}
    out["frac24"] = float(frac)
    out["hot_batch"] = {"drives": int(live[m].sum()), "rate": float(r)}
    out["hot_count"] = float(r * live[m].sum())
    return out


def compute(tgt, sims=SIMS):
    rec = Record(tgt)
    F = {"record": dict(drives=int(len(rec.d)), migrated=rec.migrated, deploy_lag=rec.deploy_lag,
                        age_sources=rec.d.age_source.value_counts().to_dict(), hot_drives_seen=int(rec.hot_flags(P.END).sum()),
                        hot_scan=dict(llr=float(rec.hot_scan["llr"]), window=[str(x.date()) for x in rec.hot_scan["window"]]),
                        hot_scan_at_cut=None)}
    rec.hot_flags(P.BACKTEST_CUT)
    F["record"]["hot_scan_at_cut"] = dict(llr=float(rec.hot_scan["llr"]), window=rec.hot_scan["window"])
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
        kest = rec.d[(rec.d.family == "HX-8") & rec.d.build.notna() & (rec.d.install_date > pd.Timestamp(P.REC_START))]
        r2 = Record(tgt, lag_days=float(np.mean((kest.install_date - kest.build).dt.days)))
        Ar = AN.Analysis(r2)
        Ar.kwargs = {}
        riv[name] = summarize(Ar, r2, sims)
    F["rivals"] = riv
    routes = {}
    for name, kw in ROUTES.items():
        Ar = AN.Analysis(rec, **kw)
        Ar.kwargs = kw
        routes[name] = summarize(Ar, rec, sims)
    F["routes"] = routes
    F["quick"] = quick(rec)
    hist_q = ["2024Q4", "2025Q1", "2025Q2", "2025Q3", "2025Q4", "2026Q1", "2026Q2", "2026Q3"]
    act = AN.quarter_actuals(rec, hist_q)
    F["history"] = {q: int(sum(v for (qq, _), v in act.items() if qq == q)) for q in hist_q}
    pert = {}
    for name, kw in PERTURB.items():
        Ar = AN.Analysis(rec, **kw)
        Ar.kwargs = kw
        pert[name] = summarize(Ar, rec, sims, backtest=False)
    F["perturbations"] = pert
    F["bands"] = bands(g, riv)
    F["stated"] = stated(F)
    return F


def _band(vals, margin, rel=True):
    lo, hi = min(vals), max(vals)
    if rel:
        return [lo * (1 - margin), hi * (1 + margin)]
    return [lo - margin, hi + margin]


def bands(g, riv):
    allv = [g] + list(riv.values())
    b = {}
    for k in ("total", "hot_count", "om6"):
        b[k] = _band([v[k] for v in allv], MARGIN["count"])
    b["dc3"] = _band([v["dc3"] for v in allv], 0.08)
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
    b["hot_batch"] = {"drives": _band([v["hot_batch"]["drives"] for v in allv], 0.04),
                      "rate": _band([v["hot_batch"]["rate"] for v in allv], MARGIN["rate"], rel=False)}
    b["total_width"] = _band([v["total_width"] for v in allv], 0.15)
    b["frac24"] = _band([v["frac24"] for v in allv], 0.05, rel=False)
    b["rec_flip"] = b["flip_doubling"]
    return b


STATED_KEYS = ("dc3", "hot_batch", "hot_count", "om6", "path", "path_range", "total_band", "total_width", "total", "coverage",
               "spares", "rec", "frac24", "by_dc", "by_family", "hot_window", "flip_doubling", "p_pays", "hot_rate", "path_band",
               "vaults")


def stated(F):
    """The golden's figures at the precision the answer blocks state them (the effort.json goldens are these)."""
    g = F["gold"]
    r0 = lambda v: int(round(v))
    out = {"dc3": r0(g["dc3"]), "hot_count": r0(g["hot_count"]), "om6": r0(g["om6"]), "total": r0(g["total"]),
           "path": {q: r0(v) for q, v in g["path"].items()},
           "path_band": {q: [r0(x) for x in v] for q, v in g["path_band"].items()},
           "total_band": [r0(x) for x in g["total_band"]], "total_width": r0(g["total_band"][1]) - r0(g["total_band"][0]),
           "hot_batch": {"drives": r0(g["hot_batch"]["drives"]), "rate": round(g["hot_batch"]["rate"], 4)},
           "coverage": round(g["coverage"], 3), "spares": {f: int(v) for f, v in g["spares"].items()},
           "rec": {"migrate": list(g["rec"]["migrate"]), "flip": round(g["rec"]["flip"], 1)}, "frac24": round(g["frac24"], 3),
           "path_range": dict({q: r0(v) for q, v in g["path"].items()}, width=r0(g["total_band"][1]) - r0(g["total_band"][0])),
           "vaults": {v: dict(s, mean=r0(s["mean"]), p_pays=round(s["p_pays"], 3)) for v, s in g["vaults"].items()},
           "by_dc": {k: r0(v) for k, v in g["by_dc"].items()}, "by_family": {k: r0(v) for k, v in g["by_family"].items()},
           "hot_window": g["hot_window"], "flip_doubling": round(g["flip_doubling"], 1), "p_pays": round(g["p_pays"], 3),
           "hot_rate": round(g["hot_rate"], 4)}
    return out


def write(F, path):
    out = dict(stated(F))
    out.update({k: F[k] for k in ("record", "gold", "rivals", "routes", "quick", "perturbations", "bands", "history")})
    out["stated_text"] = F.get("stated_text", [])
    json.dump(out, open(path, "w"), indent=1, sort_keys=True, default=float)
