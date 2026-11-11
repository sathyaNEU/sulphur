"""task14: the effort test's passes, each a named method run end to end on the cut pack (never a solver):

  quick     the obvious reading: the online system's bonds counted by lodgement, re-lettings tied by property
            identifier, the additional bonds read as every rise, new-letting rents taken for the measure and carried
            into December
  careful   careful but hurried, calibrated to the run record and graded up: every file conformed, the premises
            parsed to unit, number and street and matched to the validated addresses, a rise model fitted on the rent
            panel, the earlier tenancy's paying rent built from it, December read off the register as it stands on
            31 December, a range from the panel resampled, the slowdown split on its own figures; three variants of
            the rent step (the panel's rises carried to every landlord; the latest recorded rent carried forward by the
            panel's rate; the recorded rent where an additional bond exists and the model otherwise), the one that
            scores highest taken as the pass
  thorough  the golden
"""
import numpy as np
import pandas as pd

import analysis as AN
import measure as MS
import project as PJ


def contributions(E, t2, t1, CL, small_from="model", ops_from="recorded", earlier="paying"):
    a, b = E.matched(t2, t1)
    r1 = E.rent_on(a, t1, CL, small_from, ops_from)
    r2 = E.rent_on(b, t2, CL, small_from, ops_from)
    same = a == b
    if earlier == "start":
        r1 = np.where(same, r1, E.rent0[a])
    elif earlier == "recorded":
        r1 = np.where(same, r1, E.recorded_rent(a, t1))
    tot = r1.sum()
    return {"same": 100 * (r2[same] - r1[same]).sum() / tot, "relet": 100 * (r2[~same] - r1[~same]).sum() / tot,
            "all": 100 * (r2.sum() / tot - 1)}


def share_rose(G, E, CL, P, how):
    """Share of continuing tenancies whose rent rose in the year to 30 September 2026."""
    a, b = E.matched(AN.SEP26, AN.SEP25)
    same = a == b
    ii = a[same]
    if how == "recorded":
        r1 = E.recorded_rent(ii, AN.SEP25)
        r2 = E.recorded_rent(ii, AN.SEP26)
        return 100 * float((r2 > r1 + 1e-9).mean())
    ya = E.last_anniv_year(ii, AN.SEP26)
    pr = np.array([P[(int(y), MS.REGIONS[int(r)])] for y, r in zip(ya, E.ri[ii])])
    if how == "panel_all":
        return 100 * float(pr.mean())
    r1 = E.recorded_rent(ii, AN.SEP25)
    r2 = E.recorded_rent(ii, AN.SEP26)
    rose_op = (r2 > r1 + 1e-9).astype(float)
    return 100 * float(np.where(E.op[ii], rose_op, pr).mean())


def flow_index(G, t2, t1):
    """New-letting rents: the median weekly rent of tenancies starting in the quarter against the same quarter a year
    before (the quick pass's reading of the measure)."""
    T = G.T
    out = {}
    for g in ["NAT"] + MS.REGIONS:
        s = T if g == "NAT" else T[T["region"] == g]
        a = s[(s["start"] > t1 - 92) & (s["start"] <= t1)]["rent0"].median()
        b = s[(s["start"] > t2 - 92) & (s["start"] <= t2)]["rent0"].median()
        out[g] = 100 * (b / a - 1)
    return out


def lodged_count(G, t):
    """Bonds lodged by day t and not refunded by it, by region (the quick pass's count)."""
    T = G.T
    m = (T["lodged"] <= t) & ~(T["refund"] <= t)
    out = {"NAT": int(m.sum())}
    for g in MS.REGIONS:
        out[g] = int((m & (T["region"] == g)).sum())
    return out


def trend(series, quarters_back=4, horizon=1):
    """A straight line through the last quarters, carried one quarter on, with its own 90 per cent prediction
    interval from the fit's residuals."""
    ys = np.array(series[-quarters_back:], float)
    x = np.arange(len(ys), dtype=float)
    b, a = np.polyfit(x, ys, 1)
    pred = a + b * (len(ys) - 1 + horizon)
    res = ys - (a + b * x)
    dof = max(len(ys) - 2, 1)
    s = np.sqrt((res ** 2).sum() / dof)
    xn = len(ys) - 1 + horizon
    se = s * np.sqrt(1 + 1 / len(ys) + (xn - x.mean()) ** 2 / ((x - x.mean()) ** 2).sum())
    from math import erf  # noqa: F401
    t90 = {1: 6.314, 2: 2.920, 3: 2.353, 4: 2.132}[dof]
    return pred, t90 * se


def run_config(G, small_from="model", ops_from="recorded", earlier="paying", share="model", december="project",
               r1="held", r6=None):
    """Every graded result under one configuration of methods, on Golden G (its own linkage)."""
    E, CL, P = G.E, G.CL, G.p
    out = {}
    out["R1"] = E.held_on(AN.SEP26) if r1 == "held" else lodged_count(G, AN.SEP26)
    r = E.measure(AN.SEP26, AN.SEP25, CL, small_from=small_from, ops_from=ops_from, earlier=earlier)
    out["R2"] = {g: r[g]["n_relet"] for g in r}
    out["R3"] = {"change": r["NAT"]["same"], "share": share_rose(G, E, CL, P, share)}
    out["R4"] = r["NAT"]["relet"]
    ser = G.series(small_from=small_from, ops_from=ops_from, earlier=earlier)
    out["R5"] = {"sep26": {g: r[g]["measure"] for g in ["NAT"] + MS.REGIONS},
                 "series": {q: v["NAT"] for q, v in ser.items()}}
    kw = dict(small_from=small_from, ops_from=ops_from, earlier=earlier)
    c26 = contributions(E, AN.SEP26, AN.SEP25, CL, **kw)
    quarters = list(ser.keys())
    # December, and the change from September to December split by group (each group's contribution, 2.5)
    if december == "project":
        d = PJ.project(E, CL, ix=G.ix, cpi=G.cpi, small_from=small_from, ops_from=ops_from)
        out["R7"] = {g: d[g] for g in ["NAT"] + MS.REGIONS}
        dpart = d["_parts"]
    elif december == "asstands":
        d = E.measure(AN.DEC26, AN.DEC25, CL, small_from=small_from, ops_from=ops_from)
        out["R7"] = {g: d[g]["measure"] for g in ["NAT"] + MS.REGIONS}
        cd = contributions(E, AN.DEC26, AN.DEC25, CL, small_from=small_from, ops_from=ops_from)
        dpart = {"continuing": cd["same"], "relet": cd["relet"]}
    else:
        if december == "trend":
            out["R7"] = {g: trend([ser[q][g] for q in quarters])[0] for g in ["NAT"] + MS.REGIONS}
        else:
            out["R7"] = {g: r[g]["measure"] for g in ["NAT"] + MS.REGIONS}
        # a figure carried or extrapolated as a whole moves both groups in proportion to their September shares
        tot = c26["same"] + c26["relet"]
        sc = out["R7"]["NAT"] / tot if tot else 1.0
        dpart = {"continuing": c26["same"] * sc, "relet": c26["relet"] * sc}
    out["R8"] = {"continuing": dpart["continuing"] - c26["same"], "relet": dpart["relet"] - c26["relet"]}
    out["R8"]["fall"] = out["R8"]["continuing"] + out["R8"]["relet"]
    out["_c26"] = {"continuing": c26["same"], "relet": c26["relet"]}
    out["_dec_parts"] = dpart
    if r6 == "trend":
        h = trend([ser[q]["NAT"] for q in quarters])[1]
        out["R6"] = {"lo": out["R7"]["NAT"] - h, "hi": out["R7"]["NAT"] + h, "half": h}
    elif r6 is not None:
        out["R6"] = {"lo": out["R7"]["NAT"] - r6, "hi": out["R7"]["NAT"] + r6, "half": r6}
    return out


def quick(G_pid):
    """The quick pass on a pid-conformed Golden: the obvious file and the raw comparison."""
    G = G_pid
    E = G.E
    out = {}
    out["R1"] = lodged_count(G, AN.SEP26)
    r = E.measure(AN.SEP26, AN.SEP25, G.CL, small_from="recorded", earlier="start")
    out["R2"] = {g: r[g]["n_relet"] for g in r}
    out["R3"] = {"change": r["NAT"]["same"], "share": share_rose(G, E, G.CL, G.p, "recorded")}
    out["R4"] = r["NAT"]["relet"]
    f26 = flow_index(G, AN.SEP26, AN.SEP25)
    series = {}
    for (y, q) in MS.quarters():
        series["%dQ%d" % (y, q)] = flow_index(G, MS.quarter_end(y, q), MS.quarter_end(y - 1, q))["NAT"]
    out["R5"] = {"sep26": f26, "series": series}
    out["R7"] = dict(f26)
    out["R6"] = {"lo": f26["NAT"], "hi": f26["NAT"], "half": 0.0}
    f25 = flow_index(G, AN.SEP25, MS.quarter_end(2024, 3))
    out["R8"] = {"continuing": 0.0, "relet": 0.0, "fall": 0.0}
    return out
