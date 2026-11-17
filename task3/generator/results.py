"""Every owed figure, computed on the shipped files: figures.json (what the answer blocks and the goldens state)
and effort.json (each result's golden, band and the three passes, the stump factorial, the forcing on both sides),
with the core's spec rebuilt on the cut pack and re-priced by corelib."""
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(REPO, ".claude", "skills", "stumping"))
import core as C  # noqa: E402
import analysis as A  # noqa: E402
import corelib  # noqa: E402
import effort as EF  # noqa: E402

KEYS = ["S1", "S2", "S3", "S1+S2", "S1+S3", "S2+S3", "S1+S2+S3"]
ALONE = {"S1": "S2+S3", "S2": "S1+S3", "S3": "S1+S2"}
LOST = {"S1": "each station's tips scaled by the one factor that closes its storage gauge account",
        "S2": "each station carried to its source areas by the ratio of their yearly rainfall",
        "S3": "the tips of hail and graupel storms taken as rain where they stand"}
ROUTE_NAME = {k: "; ".join(LOST[s] for s in k.split("+")) for k in KEYS}
C1 = "C1 the Valfosca bucket's under-read at 100 mm an hour (per cent)"
C2 = "C2 burst factor, Rio Marden against Pradalt"
C3 = "C3 hail storms' 60-minute maximum the tips miss, Costarossa (per cent)"
STUMPS = {
    "S1": dict(axis="what", opens="Rio Gelt", steps_left=4, precedents=["N21", "L28"],
               said_out_loud="The tipping buckets lose water while they tip, more the harder it rains."),
    "S2": dict(axis="who", opens="Rio Marden", steps_left=4, precedents=["N26", "N01"],
               said_out_loud="A source's cloudbursts are not its gauge's, and they do not scale with its yearly rainfall."),
    "S3": dict(axis="when", opens="Rio Bianc", steps_left=4, precedents=["N30", "L26"],
               said_out_loud="On hail days the funnel holds the ice and the bucket tips its melt after the storm has gone."),
}
DEC = {"storms": 2, "depth": 1, C1: 1, C2: 2, C3: 1}


def dec(fid):
    return DEC[fid] if fid in DEC else DEC[fid.split(" ", 1)[0]]


def stated(fid, x):
    return round(float(x), dec(fid))


def floor_of(fid):
    return A.COUNT_FLOOR if fid.startswith("storms") else A.DEPTH_FLOOR if fid.startswith("depth") else A.OWN_FLOOR


def band_of(fid, g, fam, seasons=18):
    """the battery's range, never tighter than what two honest rebuilds differ by, stated outward at the figure's
    precision"""
    lo, hi = A.band(float(g), [float(x) for x in fam], floor_of(fid))
    top = max([float(x) for x in fam] + [float(g)])
    if fid.startswith("storms"):
        hi = max(hi, (top + A.TOP_STORMS / seasons) * (1.0 + A.TOP_SHARE))
    elif fid.startswith("depth"):
        hi = max(hi, top + A.TOP_MM)
    f = 10.0 ** dec(fid)
    return [round(math.floor(lo * f + 1e-9) / f, dec(fid)), round(math.ceil(hi * f - 1e-9) / f, dec(fid))]


def call_of(v, names):
    c = A.classes(v, names)
    return sorted("%s: class %d" % (s, c[s]) for s in names)


def values(X, v, own):
    """one route's figures by id: the seven counts, the seven depths and the three stumps' own figures"""
    out = {"storms " + s: v[s] for s in X["names"]}
    out.update({"depth " + s: v.even[s] for s in X["names"]})
    out.update(own)
    return out


def figures(X):
    P, names, gold, fam, lat = X["P"], X["names"], X["gold"], X["fam"], X["lat"]
    c1, c2, c3 = X["c1"], X["c2"], X["c3"]
    own = lambda k=(): {C1: c1["lost"] if "S1" in k else c1["g"], C2: c2["lost"] if "S2" in k else c2["g"],
                        C3: c3["lost"] if "S3" in k else c3["g"]}
    gf = values(X, gold, own())
    lf = {k: values(X, lat[k], own(k.split("+"))) for k in KEYS}
    df = values(X, X["direct"], {C1: 0.0, C2: 1.0, C3: 0.0})
    famv = {fid: [v[fid.split(" ", 1)[1]] if fid.startswith("storms") else v.even[fid.split(" ", 1)[1]] for v in fam]
            for fid in gf if fid not in (C1, C2, C3)}
    famv.update({C1: c1["fam"], C2: c2["fam"], C3: c3["fam"]})
    fids = list(gf)
    val = {fid: stated(fid, gf[fid]) for fid in fids}
    carried = X["crude_all"][A.CARRIED] + X["more"]["hail"]     # outside the battery and not refused by the files: inside every band
    wide = {fid: famv[fid] + [v[fid.split(" ", 1)[1]] if fid.startswith("storms") else v.even[fid.split(" ", 1)[1]] for v in carried]
            for fid in gf if fid not in (C1, C2, C3)}
    wide.update({C1: c1["fam"] + c1["wide"], C2: c2["fam"], C3: c3["fam"] + c3["wide"] + c3["more"]})
    n18 = min(P.S[c].seasons for c in P.codes)
    band = {fid: band_of(fid, gf[fid], wide[fid], n18) for fid in fids}
    cls = X["classes"]
    fig = {"call": call_of(gold, names), "classes": cls,
           "by_class": {str(k): sorted((s for s in names if cls[s] == k), key=lambda s: -gold[s]) for k in (3, 2, 1)},
           "figure": val, "figure_band": band,
           "storms": {s: val["storms " + s] for s in names}, "storms_band": {s: band["storms " + s] for s in names},
           "depth": {s: val["depth " + s] for s in names}, "depth_band": {s: band["depth " + s] for s in names},
           "under_read_valfosca_pct": val[C1], "under_read_valfosca_band": band[C1],
           "burst_factor_marden": val[C2], "burst_factor_marden_band": band[C2],
           "hail_gap_costarossa_pct": val[C3], "hail_gap_costarossa_band": band[C3],
           "trigger": {s: P.M[s]["T"] for s in names}, "station": {s: P.S[P.M[s]["station"]].name for s in names},
           "crossing_id": {s: P.M[s]["id"] for s in names}, "road_km": {s: P.M[s]["km"] for s in names},
           "storm_count": {s: int(round(gold[s] * P.S[P.M[s]["station"]].seasons)) for s in names},
           "margin": {s: round(gold[s] - (3.0 if cls[s] == 3 else 1.0 if cls[s] == 2 else 1.0), 2) for s in names}}
    routes = {"golden": gold, "direct": X["direct"], "radar": X["radar"], "mapped": X["mapped"], "carried": X["carried"]}
    routes.update({k: lat[k] for k in KEYS})
    fig["routes"] = {k: {s: {"storms": round(v[s], 2), "class": A.classes(v, names)[s],
                             "depth": round(v.even[s], 1) if hasattr(v, "even") and s in getattr(v, "even", {}) else None}
                         for s in names} for k, v in routes.items()}
    fig["route_calls"] = {k: call_of(v, names) for k, v in routes.items()}
    fig["route_figures"] = {k: {fid: stated(fid, x[fid]) for fid in fids} for k, x in list(lf.items()) + [("direct", df)]}
    fig["distinct_wrong_calls"] = len({tuple(call_of(lat[k], names)) for k in KEYS})
    cnt = lambda v: {str(k): sum(1 for s in names if A.classes(v, names)[s] == k) for k in (3, 2, 1)}
    fig["route_class_counts"] = {k: cnt(v) for k, v in routes.items()}
    fig["stated"] = dict(rate_mm_h=100, rates=[10, 25, 50, 100, 150], program=[2027, 2031], lines=["1.0", "3.0"],
                         total_step_minutes=[5, 10, 15], moved_pct=20, radar_pixel_km=1, block_minutes=10)
    fig["variants"] = len(fam)
    fig["carried_variants"] = len(carried)
    fig["family_calls_all_golden"] = all(call_of(v, names) == fig["call"] for v in fam)
    fig["variant_range"] = {s: [round(min(v[s] for v in fam), 2), round(max(v[s] for v in fam), 2)] for s in names}
    near = min((abs(v[s] - l), s) for v in fam for s in names for l in A.LINES)
    fig["nearest_variant"] = {"distance": round(near[0], 2), "crossing": near[1]}
    at_st = lambda v: {k: {"route": d["route"], "station": d["station"], "pct": int(round(100.0 * d["route"] / d["station"])),
                           "scatter": round(d["scatter"], 2)} for k, d in v.station.items()}
    for key in ("mapped", "radar"):          # the two routes that count the radar's own depths
        v = X[key]
        fig[key + "_route"] = {"storms": {s: round(v[s], 2) for s in names}, "depth": {s: round(v.even[s], 1) for s in names},
                               "classes": A.classes(v, names), "at_mm": 12, "station": at_st(v)}
    cg = {label: Q.estimate() for label, Q in X["conv"].items()}
    cnt = lambda v, s_: int(round(v[s_] * P.S[P.M[s_]["station"]].seasons))
    fig["window"] = {"readings": {label: {s_: cnt(v, s_) for s_ in names} for label, v in cg.items()},
                     "storms_moved": max(abs(cnt(v, s_) - cnt(X["gold"], s_)) for v in cg.values() for s_ in names),
                     "crossings_moved": max(sum(cnt(v, s_) != cnt(X["gold"], s_) for s_ in names) for v in cg.values()),
                     "depth_moved_mm": round(max(abs(v.even[s_] - X["gold"].even[s_]) for v in cg.values() for s_ in names), 2),
                     "classes_hold": all(A.classes(v, names) == cls for v in cg.values())}
    fig["more"] = {k: {"classes_hold": all(A.classes(v, names) == cls for v in vs), "variants": len(vs),
                       "storms": {s: [round(min(v[s] for v in vs), 2), round(max(v[s] for v in vs), 2)] for s in names}}
                   for k, vs in X["more"].items()}
    fig["crude"] = {k: {"storms": {s: round(v[s], 2) for s in names}, "call_holds": call_of(v, names) == fig["call"]}
                    for k, v in X["crude"].items()}
    # the stations
    code = X["code"]
    kap = X["kap"]
    st = {}
    for c, d in X["stations"].items():
        k = kap[c]
        st[d["name"]] = dict(code=c, bucket_mm=P.S[c].bucket, gauge=P.S[c].model, rows=d["rows"], resent=d["resent"],
                             tests=d["tests"], tips=d["tips"], storms=d["events"], hail_storms=d["hail"],
                             intervals=d["intervals"], seasons=d["seasons"], storage_mm=round(d["storage"], 1),
                             tipped_mm=round(d["tipped"], 1), account_factor=round(d["factor"], 3),
                             resid_factor=round(d["resid_factor"], 2), resid_rate=round(d["resid_rate"], 2),
                             resid_r=round(d["resid_r"], 2), loss_h_per_mm=round(k, 6),
                             under_read={str(r): round(A.under_read(k, "recip", float(r)), 1) for r in (10, 25, 50, 100, 150)},
                             one_factor_pct=round(100.0 * (1.0 - 1.0 / d["factor"]), 2),
                             late_hail_pct=round(d["late_hail"], 1), late_rain_pct=round(d["late_rain"], 2),
                             optical_log_sd=round(d["optical_log_sd"], 2),
                             hail_gap_pct=round(d["hail_gap"], 1), in_season=d["in_season"],
                             gaps_3_to_6h=d["gaps_3_to_6h"], gaps_6_to_8h=d["gaps_6_to_8h"])
    fig["stations"] = st
    fig["account_factor"] = {n: d["account_factor"] for n, d in st.items()}
    rr = lambda d: {("%.1f" % b): [round(x, 2) for x in v] for b, v in d.items()}
    fig["account_residual"] = {"kept": rr(X["steps"]["kept"]), "refused": {k: rr(v) for k, v in X["steps"]["refused"].items()},
                               "golden": {("%.1f" % b): round(x, 2) for b, x in X["steps"]["golden"].items()},
                               "ratio": {k: [math.floor(v[0] * 100) / 100.0, math.ceil(v[1] * 100) / 100.0] for k, v in X["steps"]["ratio"].items()},
                               "small_bucket": "%.1f" % X["steps"]["small"],
                               "held_max": math.ceil(X["steps"]["held_max"] * 100) / 100.0,
                               "refused_min": math.floor(X["steps"]["refused_min"] * 100) / 100.0,
                               "k_limit": A.K_LIMIT,
                               "power_exponent": [round(min(X["steps"]["power"]), 3), round(max(X["steps"]["power"]), 3)],
                               "refused_calls_hold": {k: all(call_of(v, names) == fig["call"] for v in vs) for k, vs in X["crude_all"].items()},
                               "refused_range": {k: {s: [round(min(v[s] for v in vs), 2), round(max(v[s] for v in vs), 2)] for s in names}
                                                 for k, vs in X["crude_all"].items()}}
    fig["sources"] = {n: dict(station=P.S[P.M[n]["station"]].name, burst_factor=round(d["factor"], 3), normal_ratio=round(d["map"], 3),
                              pairs=d["pairs"], cells=d["cells"], q90_halves_pct=round(d["q90_halves"], 1),
                              geo_halves_pct=round(d["geo_halves"], 1), slope=round(d["slope"], 3), slope_rev=round(d["slope_rev"], 3),
                              top=round(d["top"], 3), top_rev=round(d["top_rev"], 3),
                              ways={w: round(x, 3) for w, x in d["ways"].items()},
                              halves={k: [round(v[0], 2), round(v[1], 2)] for k, v in d["halves"].items()},
                              weighed_over_station=round(d["weighed_over_station"], 2) if "weighed_over_station" in d else None,
                              normal_mm=P.M[n]["normal"], trigger=P.M[n]["T"])
                      for n, d in X["site"].items()}
    r = X["referee"]
    trip = lambda t: dict(top=round(t[0], 2), depth=round(t[1], 2), storms=int(round(t[2])))
    fig["referee"] = dict(seasons=r["seasons"], gauges=len(P.research), rank=int(round(A.EVEN * r["seasons"])), seen=trip((r["seen_top"], r["seen_depth"], r["seen_count"])),
                          golden=trip(r["golden"]), rivals={k: trip(v) for k, v in r["rivals"].items()},
                          others={k: trip(v) for k, v in r["others"].items()},
                          source_over_bucket_raw=round(X["reads_raw"][0], 3), hail_multiplier=round(X["reads"][1], 3))
    fig["radar_bias"] = round(X["radar"].bias, 3)
    fig["perturbations"] = [{"input": k, "call_holds": call_of(v, names) == fig["call"], "storms": {s: round(v[s], 2) for s in names},
                             "nearest": round(min(abs(v[s] - l) for s in names for l in A.LINES), 2)} for k, v in X["moved"].items()]
    fig["regulation"] = dict(lines=[1.0, 3.0], gap_hours=6, window_minutes=60, season=["1 May", "31 October"], times_a_season=int(A.EVEN),
                             revision=4, sections=["2.1", "2.2", "2.3", "3.1", "3.2", "4.1"])
    fig["counts"] = dict(stations=len(P.S), crossings=len(names), seasons=P.S[code["Valfosca"]].seasons,
                         first_year=int(min(P.S[code["Valfosca"]].year)), last_year=int(max(P.S[code["Valfosca"]].year)),
                         tip_rows=int(sum(d["rows"] for d in X["stations"].values())),
                         intervals=int(sum(d["intervals"] for d in X["stations"].values())),
                         radar_rows=P.radar_rows, radar_years=[P.radar_years[0], P.radar_years[-1]],
                         weigh_years=[P.weigh_years[0], P.weigh_years[-1]], even_rank=int(round(A.EVEN * P.S[code["Valfosca"]].seasons)),
                         resent_rows=int(sum(d["resent"] for d in X["stations"].values())),
                         test_tips=int(sum(d["tests"] for d in X["stations"].values())))
    return fig, dict(gf=gf, lf=lf, df=df, famv=famv, wide=wide, fids=fids)


def spec_of(X, fig, R):
    """the core's spec rebuilt on the cut pack, each figure with the band the answer blocks state"""
    names, gold, fam, lat = X["names"], X["gold"], X["fam"], X["lat"]
    C.build(C.SEED)
    members = {s: dict(lines=list(A.LINES), truth=float(C.CROSSINGS[s]["truth"]), golden=float(gold[s]),
                       family=[float(v[s]) for v in fam],
                       routes=dict(direct=float(X["direct"][s]), rigorous=float(X["mapped"][s]),
                                   index=float(lat["S1+S2+S3"][s]), carried=float(X["carried"][s]))) for s in names}
    n = len(fam)
    pad = lambda v: (list(v) * (n // len(v) + 1))[:max(n, 12)]
    figs = []
    for fid, lost_key, rig in ((C1, "S1", X["c1"]["lost"]), (C2, "S2", 1.0), (C3, "S3", 0.0)):
        figs.append(dict(id=fid, block="component", golden=float(R["gf"][fid]), family=pad(R["famv"][fid]),
                         band=fig["figure_band"][fid], lattice={k: float(R["lf"][k][fid]) for k in KEYS},
                         routes=dict(rigorous=float(rig))))
    for s in names:
        figs.append(dict(id=s, block="ask", member=s, band=fig["figure_band"]["storms " + s]))
    for s in names:
        fid = "depth " + s
        figs.append(dict(id="depth on the line, " + s, block="ask", golden=float(R["gf"][fid]), family=[float(x) for x in R["famv"][fid]],
                         band=fig["figure_band"][fid], lattice={k: float(R["lf"][k][fid]) for k in KEYS},
                         routes=dict(rigorous=float(X["mapped"].even[s]))))
    r = X["referee"]
    ref = dict(slice="the Rio Scuro research valley: weighing gauges at four sources over %d seasons; the mean 60-minute "
                     "depth of each source's five largest storms a season, mean of the four (mm)" % r["seasons"],
               covers_target=False, truth=r["seen_top"], golden=r["golden"][0], rivals={k: v[0] for k, v in r["rivals"].items()})
    return dict(task="task3 architecture 8, cut pack", call="lines", members=members, stumps=STUMPS,
                lattice={k: {s: float(lat[k][s]) for s in names} for k in KEYS}, referee=ref, figures=figs)


def result_values(fv, call, factors):
    return {"R1": factors, "R2": fv[C1], "R3": fv[C2], "R4": fv[C3],
            "R5": {k.split(" ", 1)[1]: fv[k] for k in fv if k.startswith("storms ")},
            "R6": {k.split(" ", 1)[1]: fv[k] for k in fv if k.startswith("depth ")}, "R7": call}


def effort(X, fig, R):
    names, lat = X["names"], X["lat"]
    st = lambda f: {fid: stated(fid, f[fid]) for fid in R["fids"]}
    fac = fig["account_factor"]
    gold = result_values(fig["figure"], fig["call"], fac)
    quick = result_values(st(R["df"]), call_of(X["direct"], names), None)
    careful = result_values(st(R["lf"]["S1+S2+S3"]), call_of(lat["S1+S2+S3"], names), fac)
    fb = fig["figure_band"]
    meta = [
        ("R1", "each station's storage gauge total over its tipped total, visit interval by visit interval", "Step-by-Step",
         "account_factor", [], "", {}, []),
        ("R2", "what Valfosca's bucket fails to record at a true 100 mm an hour (per cent)", "Component 1",
         "under_read_valfosca_pct", [], "the tip logs' rates and the visit book's storage gauge reads", dict(band=fb[C1]), ["N21", "L28"]),
        ("R3", "Rio Marden's burst factor against Pradalt", "Component 2", "burst_factor_marden", [],
         "the radar extract's pixel pairs", dict(band=fb[C2]), ["N26", "N01"]),
        ("R4", "the share of the hail storms' 60-minute maximum the tips miss at Costarossa (per cent)", "Component 3",
         "hail_gap_costarossa_pct", [], "the detector's blocks against the tips of the same storms", dict(band=fb[C3]), ["N30", "L26"]),
        ("R5", "the triggering storms a season to expect at each crossing", "Ask 1", "storms", ["R2", "R3", "R4"], "",
         dict(bands={s: fb["storms " + s] for s in names}, partly_share=0.5), ["N21", "N26", "L26"]),
        ("R6", "the 60-minute depth each source area reaches five times a season (mm)", "Ask 2", "depth", ["R2", "R3", "R4"], "",
         dict(bands={s: fb["depth " + s] for s in names}, partly_share=0.5), ["N21", "N26", "L26"]),
        ("R7", "each crossing's class", "Recommendation", "call", ["R5"], "", {}, ["N21", "N26", "L26"]),
    ]
    res = []
    for rid, name, graded, key, dep, indep, extra, prec in meta:
        r = {"id": rid, "name": name, "graded_as": graded, "figure": key, "depends": dep, "independent": indep,
             "golden": gold[rid], "passes": {"quick": quick[rid], "careful": careful[rid], "thorough": gold[rid]},
             "precedent": prec}
        r.update(extra)
        res.append(r)
    by = {r["id"]: r for r in res}

    def grades(f, call):
        v = result_values(st(f), call, fac)
        return {rid: EF.grade(v[rid], by[rid])[0] for rid in by}
    g_lost = {k: grades(R["lf"][k], call_of(lat[k], names)) for k in KEYS}
    nm = {"S1": "what the bucket loses rises with the rate, so the loss is fitted on the tips' rates through the storage "
                "gauge account and put back minute by minute",
          "S2": "a source area's bursts against its station's are measured on the radar's pixel pairs as a ratio, and the "
                "yearly rainfall does not carry them",
          "S3": "on hail days the tips have the storm's water and the detector has its minutes"}
    judgments = []
    for s in ("S1", "S2", "S3"):
        ak = ALONE[s]
        judgments.append({"id": s, "name": nm[s], "kind": "stump", "precedent": STUMPS[s]["precedents"],
                          "dropped": {"answer": call_of(lat[s], names), "results_moved": [r for r, x in g_lost[s].items() if x != "right"]},
                          "alone": {"answer": call_of(lat[ak], names), "results_rescued": [r for r, x in g_lost[ak].items() if x == "right" and r != "R1"]}})
    judgments += [
        {"id": "J4", "name": "the tips, the detector, the visit book and the radar brought to one clock", "kind": "reflex", "precedent": ["R01", "R46"]},
        {"id": "J5", "name": "re-sent logger rows counted once and the technicians' tip tests left out", "kind": "reflex", "precedent": ["R01"]},
        {"id": "J6", "name": "the largest total over every 60 consecutive minutes, a storm counted once", "kind": "reflex", "precedent": ["R06"]},
        {"id": "J7", "name": "the season, the storm separation, the lines and the eighteen-season mean as the regulation files them",
         "kind": "reflex", "precedent": []},
        {"id": "J8", "name": "each station's tips set against its storage gauge, visit interval by visit interval", "kind": "reflex", "precedent": ["R93"]},
        {"id": "J9", "name": "a hold-out of seasons and a bootstrap of seasons on whatever route is built", "kind": "reflex", "precedent": ["R03", "R04"]}]
    F = {"golden_answer": fig["call"], "reflex_route": {"answer": call_of(lat["S1+S2+S3"], names)}, "judgments": judgments}
    routes = [{"name": "the golden", "answer": fig["call"], "golden": True}]
    routes += [{"name": ROUTE_NAME[k], "answer": call_of(lat[k], names)} for k in KEYS]
    routes.append({"name": "the tips as they stand counted against the triggering depths", "answer": call_of(X["direct"], names)})
    routes.append({"name": "the radar product adjusted to the gauges and counted at the source pixel", "answer": call_of(X["radar"], names)})
    routes.append({"name": "the radar's depths mapped on the research valley's weighing gauges and counted at the source pixel",
                   "answer": call_of(X["mapped"], names)})
    routes.append({"name": "the research valley's gauges read as a calibration of the bucket and carried to every crossing",
                   "answer": call_of(X["carried"], names)})
    label = lambda w: "loss %s, pooled by %s, tips %s, rate on %d-minute totals, burst factor %s, hail %s" % w
    forcing = {"kind": "set", "golden_answer": fig["call"],
               "golden_family": [{"name": "the golden", "answer": fig["call"]}] +
                                [{"name": label(w), "answer": call_of(v, names)} for w, v in zip(X["ways"], X["fam"])],
               "shortcuts": [{"name": r["name"], "answer": r["answer"]} for r in routes[1:]],
               "perturbations": [{"input": k, "answer": call_of(v, names)} for k, v in X["moved"].items()]}
    hints = [{"sentence": STUMPS[s]["said_out_loud"], "rescues": [r for r, x in g_lost[ALONE[s]].items() if x == "right" and r != "R1"]}
             for s in ("S1", "S2", "S3")]
    return {"results": res, "hints": hints, "factorial": F, "forcing": forcing, "routes": routes,
            "weights": {"recommendation": 18, "components": 20, "asks": 53, "instruction": 9}}, g_lost


def run(target):
    X = A.run(target)
    fig, R = figures(X)
    spec = spec_of(X, fig, R)
    rows, level = corelib.check(spec)
    earn = corelib.earnings(spec)
    key = lambda k: corelib._key(k.split("+"))
    fig["rubric"] = {"level": level, "fails": [r[0] + ": " + r[2] for r in rows if r[1] == "FAIL"],
                     "one_lost": {s: round(earn["earn"][key(s)], 1) for s in ("S1", "S2", "S3")},
                     "fixed_alone": {s: round(earn["earn"][key(ALONE[s])], 1) for s in ("S1", "S2", "S3")},
                     "reflex": round(earn["earn"][key("S1+S2+S3")], 1), "rigorous": round(earn["rigorous"], 1)}
    fig["truth"] = {s: round(float(C.CROSSINGS[s]["truth"]), 3) for s in X["names"]}
    E, g_lost = effort(X, fig, R)
    fig["result_grades"] = g_lost
    return X, fig, E, spec


if __name__ == "__main__":
    import json
    X, fig, E, spec = run(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target"))
    corelib.run(spec)
    print(json.dumps({k: fig[k] for k in ("call", "rubric", "perturbations", "nearest_variant", "result_grades", "referee")}, indent=1, default=float)[:6000])
    for fid in fig["figure"]:
        print("%-76s %8s  %s" % (fid, fig["figure"][fid], fig["figure_band"][fid]))
