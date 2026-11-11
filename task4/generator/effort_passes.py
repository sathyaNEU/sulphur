"""effort.json: the golden, the careful but hurried route and the quick route run end to end on the cut pack,
result by result, with each result's band measured on the golden family's rivals, the precedents behind every
result the careful pass loses, the hints, the routes and the forcing on both sides."""
import json
import math

import numpy as np
import pandas as pd

import analysis as A
import golden as GD
import params as P

W = list(P.PEAK_WEEKS)
VARIANTS = {"a quadratic congestion term, its knot by fit": {"cong": "quad"},
            "the logged share flat over the day": {"ls": "flat"},
            "the 2024 and 2025 profiles averaged (2024's orders 1,092 days on)": {"src": "avg"},
            "a linear calibration on the plan's growth": {"form": "linear"},
            "the calibration through the origin": {"intercept": False},
            "the calibration on the peak weeks alone": {"cal_weeks": P.PEAK_WEEKS},
            "Huippu Sport's mix over two peaks": {"months": ("2024-11", "2024-12", "2025-11", "2025-12")},
            "the time model fitted on 2024 to 2026": {"fit_years": (2024, 2025, 2026)}}
PERTURB = {"congestion gamma -20%": {"gamma_mult": 0.8}, "congestion gamma +20%": {"gamma_mult": 1.2},
           "Huippu Sport's extra time -20%": {"hui_mult": 0.8}, "Huippu Sport's extra time +20%": {"hui_mult": 1.2},
           "the 2027 overstatement -20%": {"over_mult": 0.8}, "the 2027 overstatement +20%": {"over_mult": 1.2}}


def cells(R):
    return sorted("%s-%d" % (zz, w) for zz in A.Z_SMALL for w in W if R["evening"][(zz, w)])


def hours_tab(R):
    return {"%s-%d" % (zz, w): R["plan"][(zz, w)]["hours"] for zz in P.ZONES for w in W}


def first_issue(f):
    b = f["forecasts"]
    return b[~((b["round"] == "budget 2024") & (b["group"] == "bulky") & (b["issued"].astype(str) == "2023-10-27"))]


def r2_variants(z, f):
    o = A.overstatement_by_year(z, f, weeks=P.PEAK_WEEKS)
    by_year = o.groupby("year")[["forecast", "placed"]].sum()
    mean_ratio = float((by_year["forecast"] / by_year["placed"] - 1.0).mean())
    sp = o[o["group"] == "small parts"]
    sp_only = float(sp["forecast"].sum() / sp["placed"].sum() - 1.0)
    return {"mean of the years' ratios": mean_ratio, "small parts only": sp_only}


def quick(f, z, t, G):
    """Ten minutes: the budget as issued, the latest forecast for each week as the record, the draft's rates."""
    fc = f["forecasts"].copy()
    fc["issued"] = pd.to_datetime(fc["issued"])
    k = fc[fc["brand"] == P.BRAND_K].sort_values("issued").groupby(["group", "iso_year", "iso_week"]).tail(1)
    k = k[k["iso_year"].between(2022, 2025) & k["iso_week"].isin(P.PEAK_WEEKS)]
    pk = A.placed_by_week(f)
    pk = pk[pk["iy"].between(2022, 2025) & pk["iw"].isin(P.PEAK_WEEKS)]
    r2 = float(k["order_lines"].sum() / pk["lines"].sum() - 1.0)
    rate = {zz: A.paid_per_line(z, t, 2025, P.PEAK_WEEKS, zz) for zz in P.ZONES}
    tp = A.pilot_times(f)
    zp = z[(z["zone"] == "P2") & (z["date"] >= pd.Timestamp(P.PILOT[0])) & (z["date"] <= pd.Timestamp(P.PILOT[1]))]
    kot_t = float((zp["task_min"].sum() - tp * zp["lines_hui"].sum()) / zp["kot"].sum())
    V = A.volumes(z, f, (0.0, 0.0), (0.0, 0.0), how="copy")
    kz = A.picked_by_week(z)
    kz = kz[(kz["iy"] == 2025) & kz["iw"].isin(P.PEAK_WEEKS)]
    kp1 = float(kz[kz["zone"] == "P1"]["kot"].sum() / kz[kz["zone"].isin(A.Z_SMALL)]["kot"].sum())
    hm = A.hui_mix(f)
    plan, ev = {}, {}
    for w in W:
        days, _ = A.days_2027(w)
        for zz in P.ZONES:
            if zz == "B1":
                L = V[(P.BRAND_K, "bulky")][w] + V[(P.BRAND_H, "bulky")][w]
                plan[(zz, w)] = L * rate[zz]
                continue
            lk = V[(P.BRAND_K, "small parts")][w] * (kp1 if zz == "P1" else 1.0 - kp1)
            lh = V[(P.BRAND_H, "small parts")][w] * hm[zz]["share"]
            plan[(zz, w)] = lk * rate[zz] + lh * rate[zz] * tp / kot_t
            ev[(zz, w)] = False                      # the draft books no evening shift ("to confirm")
    own = G["own"]
    agency = {w: sum(max(0.0, plan[(zz, w)] - own[w][zz]) for zz in P.ZONES) for w in W}
    bud = A.budget_totals(f, P.BRAND_K, "small parts", 2027)
    return {"r1": G["r1"], "r2": r2, "r3": 0.0, "r4": tp - kot_t, "r5": 0.0,
            "r6": bud[47] / sum(bud[w] for w in W), "hours": {"%s-%d" % k: v for k, v in plan.items()},
            "cells": sorted("%s-%d" % k for k, v in ev.items() if v), "agency": agency}


def d_2025(z, t):
    w = t[(t["iy"] == 2025) & t["iw"].isin(P.PEAK_WEEKS) & (t["shift"] == "DAY") & (t["absence"] == "")
          & t["zone"].isin(A.Z_SMALL)]
    crew = w.groupby(["date", "zone"]).size().reset_index(name="n")
    crew["a"] = crew["zone"].map(P.AISLES)
    return float((crew["n"] / crew["a"]).mean())


def build(f, G, figs, rg):
    z = A.zone_hours(f)
    t = A.timesheet(f)
    H = A.hurried(f)
    Q = quick(f, z, t, G)
    fam = {k: A.golden(f, o) for k, o in VARIANTS.items()}
    pert = {k: A.golden(f, o) for k, o in PERTURB.items()}
    gold_cells = cells(G)
    # bands from the rivals
    r2v = dict(r2_variants(z, f))
    r2v["golden"] = G["r2"]
    hrs = {k: hours_tab(R) for k, R in fam.items()}
    gh = hours_tab(G)
    spread = max(abs(h[c] / gh[c] - 1.0) for h in hrs.values() for c in gh)
    hb = math.ceil((spread + 0.01) * 100) / 100.0
    agv = {k: R["agency"] for k, R in fam.items()}
    sp_ag = max(abs(a[w] / G["agency"][w] - 1.0) for a in agv.values() for w in W)
    ab = math.ceil((sp_ag + 0.01) * 100) / 100.0
    rivals = {"r2": {k: round(100 * v, 2) for k, v in r2v.items()},
              "r3": {k: round(R["r3"], 3) for k, R in fam.items()},
              "r4": {k: round(R["r4"], 3) for k, R in fam.items()},
              "r5_K_sp": {k: round(100 * R["r5"]["K_sp"], 2) for k, R in fam.items()},
              "r6": {k: round(100 * R["r6"], 2) for k, R in fam.items()},
              "cells": {k: cells(R) for k, R in fam.items()},
              "hours_band_pct": round(100 * hb), "agency_band_pct": round(100 * ab),
              "d_2025_peak": round(d_2025(z, t), 2),
              "lines_k_47": GD.r10(G["vol"][(P.BRAND_K, "small parts")][47]),
              "budget_k_47": int(A.budget_totals(f, P.BRAND_K, "small parts", 2027)[47])}
    def band(vals, pad, nd):
        return [round(min(vals) - pad, nd), round(max(vals) + pad, nd)]

    r2_all = list(rivals["r2"].values()) + [round(100 * A.r2_overstatement(z, dict(f, forecasts=first_issue(f))), 2)]
    bands = {"r2": band(r2_all, 1.0, 1),
             "r3": band(list(rivals["r3"].values()) + [figs["r3"]], 0.05, 2),
             "r4": band(list(rivals["r4"].values()) + [figs["r4"]], 0.03, 2),
             "r5_K_sp": band(list(rivals["r5_K_sp"].values()) + [figs["r5"]["K_sp"]], 1.0, 1),
             "r6": band(list(rivals["r6"].values()) + [figs["r6"]], 1.2, 1)}
    rivals["bands"] = bands
    gr = {"%s-%d" % (zz, w): GD.r10(G["plan"][(zz, w)]["hours"]) for zz in P.ZONES for w in W}
    res = []

    def add(rid, name, graded, figure, golden, passes, band=None, partly=None, bands=None, depends=(), indep="",
            precedent=(), partly_share=None):
        r = {"id": rid, "name": name, "graded_as": graded, "figure": figure, "golden": golden, "depends": list(depends),
             "independent": indep, "passes": passes}
        if band:
            r["band"] = band
        if partly:
            r["partly"] = partly
        if bands:
            r["bands"] = bands
        if precedent:
            r["precedent"] = list(precedent)
        if partly_share:
            r["partly_share"] = partly_share
        res.append(r)

    r1g = {k: int(v) for k, v in figs["r1"].items()}
    add("R1", "the 2025 peak's picker hours by zone", "Component 4", "r1", r1g,
        {"quick": {k: int(round(v)) for k, v in Q["r1"].items()}, "careful": r1g, "thorough": r1g},
        bands={k: [v * 0.99, v * 1.01] for k, v in r1g.items()}, indep="the two payroll exports and the WMS zone hours")
    add("R2", "the pooled year-ahead peak overstatement", "Ask 4", "r2", figs["r2"],
        {"quick": round(100 * Q["r2"], 1), "careful": round(100 * H["r2"], 1), "thorough": figs["r2"]},
        band=bands["r2"], partly=[bands["r2"][0] - 1.5, bands["r2"][1] + 1.5], indep="the forecast archive and the WMS lines")
    add("R3", "aisle congestion at 1.8 pickers an aisle", "Component 1", "r3", figs["r3"],
        {"quick": 0.0, "careful": 0.0, "thorough": figs["r3"]}, band=bands["r3"], partly=[bands["r3"][0] - 0.1, bands["r3"][1] + 0.1],
        indep="the WMS zone hours", precedent=("N01", "L15", "L26"))
    add("R4", "Huippu Sport's extra minutes a line", "Ask 5", "r4", figs["r4"],
        {"quick": round(Q["r4"], 2), "careful": round(H["r4"], 2), "thorough": figs["r4"]}, band=bands["r4"],
        partly=[bands["r4"][0] - 0.04, bands["r4"][1] + 0.04], indep="the pilot, the article lines, the item master and the slotting",
        precedent=("L25", "L14", "N04"))
    add("R5", "the 2027 budget's expected overstatement, Kotikaari small parts", "Component 2", "r5_K_sp",
        figs["r5"]["K_sp"], {"quick": 0.0, "careful": round(100 * H["r2"], 1), "thorough": figs["r5"]["K_sp"]},
        band=bands["r5_K_sp"], partly=[bands["r5_K_sp"][0] - 1.5, bands["r5_K_sp"][1] + 1.5], indep="the forecast archive",
        precedent=("L09", "N02"))
    add("R6", "week 47's share of the 2027 peak's Kotikaari small-parts lines", "Component 3", "r6", figs["r6"],
        {"quick": round(100 * Q["r6"], 1), "careful": figs["r6_budget"], "thorough": figs["r6"]}, band=bands["r6"],
        partly=[bands["r6"][0] - 1.5, bands["r6"][1] + 1.5], indep="the order imports and the 2027 budget",
        precedent=("N02", "N06"))
    hband = {c: [v * (1 - hb), v * (1 + hb)] for c, v in gr.items()}
    add("R7", "each zone's picker hours, weeks 46 to 50", "Ask 1", "hours_cells", gr,
        {"quick": {c: round(v) for c, v in Q["hours"].items()},
         "careful": {"%s-%d" % (zz, w): round(H["plan"][(zz, w)]["hours"]) for zz in P.ZONES for w in W},
         "thorough": gr}, bands=hband, depends=("R3", "R4", "R5", "R6"), precedent=("L11",), partly_share=0.5)
    rcells = {"%s-%d-%s" % (zz, w, e): figs["range"][zz][w][i] for zz in P.ZONES for w in W
              for i, e in enumerate(("lo", "hi"))}
    rband = {c: [v * 0.92, v * 1.08] for c, v in rcells.items()}
    hr_lo = {}
    for zz in P.ZONES:
        for w in W:
            v = H["plan"][(zz, w)]["hours"]
            hr_lo["%s-%d-lo" % (zz, w)] = round(v * 0.97)
            hr_lo["%s-%d-hi" % (zz, w)] = round(v * 1.03)
    add("R8", "the 80 per cent ranges", "Ask 1", "range_cells", rcells,
        {"quick": None, "careful": hr_lo, "thorough": rcells}, bands=rband, depends=("R7",), precedent=("L28",),
        partly_share=0.5)
    add("R9", "the evening-shift weeks by small-parts zone", "Recommendation", "call_cells", gold_cells,
        {"quick": Q["cells"], "careful": cells(H), "thorough": gold_cells}, depends=("R3", "R4", "R5", "R6", "R7"),
        precedent=("L11",))
    ag = {str(w): figs["agency"][w] for w in W}
    add("R10", "the agency hours to book each week", "Ask 2", "agency_cells", ag,
        {"quick": {str(w): round(Q["agency"][w]) for w in W}, "careful": {str(w): round(H["agency"][w]) for w in W},
         "thorough": ag}, bands={c: [v * (1 - ab), v * (1 + ab)] for c, v in ag.items()}, depends=("R7",),
        precedent=("L11",), partly_share=0.5)
    hints = [{"sentence": "time a line rises with the pickers logged in an aisle once the handling-class mix is held "
                          "fixed, and 2027's day shifts run at the zone limit", "rescues": ["R3"]},
             {"sentence": "2026 has 53 ISO weeks, so a budget phased by 2025's week numbers puts Black Friday in week "
                          "48 of 2027 instead of week 47", "rescues": ["R6"]},
             {"sentence": "the pilot carried only Huippu Sport's polybag apparel", "rescues": ["R4"]},
             {"sentence": "a budget's overstatement grows with the growth its commercial plan states", "rescues": ["R5"]}]
    routes = [{"name": "golden", "answer": gold_cells, "golden": True},
              {"name": "careful but hurried (the draft's route)", "answer": cells(H)},
              {"name": "quick", "answer": Q["cells"]}]
    for fx in GD.FIXES:
        routes.append({"name": "the draft's route with %s only" % GD.FIX_NAME[fx], "answer": cells(A.hurried(f, (fx,)))})
    forcing = {"kind": "set", "golden_answer": gold_cells,
               "golden_family": [{"name": k, "answer": cells(R)} for k, R in fam.items()],
               "shortcuts": [{"name": r["name"], "answer": r["answer"]} for r in routes if not r.get("golden")],
               "perturbations": [{"input": k, "answer": cells(R)} for k, R in pert.items()]}
    E = {"results": res, "hints": hints, "routes": routes, "forcing": forcing,
         "weights": {"recommendation": 14, "components": 24, "asks": 55, "instruction": 7}}
    return E, rivals, {"hours_cells": gr, "range_cells": rcells, "call_cells": gold_cells, "agency_cells": ag,
                       "r5_K_sp": figs["r5"]["K_sp"]}


def write(path, E):
    json.dump(E, open(path, "w"), indent=1, default=float)
