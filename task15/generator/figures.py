"""figures.json (every figure the answer blocks state) and effort.json (each pass's figure at each result), both
from golden.results() on the cut pack; the bands come from the rival routes run on the same pack."""
import json
import os

import numpy as np

import golden as GD

HERE = os.path.dirname(os.path.abspath(__file__))
FMT = GD.FORMATS
ORDER = {"Super": 0, "Kvarter": 1, "To Go": 2}


def r100(x):
    return int(round(x / 100.0) * 100)


def r1(x):
    return round(float(x), 1)


def split(parts, gap, keys):
    """Parts rounded to a tenth so that they add to the gap as printed; the rest takes what rounding leaves."""
    g = r1(gap)
    out = {k: r1(parts[k]) for k in keys}
    out["rest"] = r1(g - sum(out[k] for k in keys))
    out["gap"] = g
    return out


def saving_bands(R):
    """R8: each format's band is the span of the golden and every defensible rival (the estimator clipped or not,
    the grouping by trading type or by format within it, the margin part on sales, units or the 2025 turned-away
    margin, the pilot stores' rate as a ratio of totals or a mean of their own rates, a line in the weekend share,
    the margin part read off the recorded gross margin, the openings left in), widened by a twentieth either side
    and by at least 1,000 DKK."""
    vals = {f: [R["G"]["format_saving"][f]] + [r["format_saving"][f] for r in R["rivals"].values()] for f in FMT}
    out = {}
    for f in FMT:
        lo, hi = min(vals[f]), max(vals[f])
        pad = max(1000.0, 0.05 * max(abs(lo), abs(hi)))
        out[f] = [r100(lo - pad), r100(hi + pad)]
    return out, {f: [r100(min(v)), r100(max(v))] for f, v in vals.items()}


def range_bands(R, variants):
    """R9: each range end's band holds the golden's resampling and the variants run here (another seed, a longer
    run, the stores that kept AutoOrdre held fixed), at least 5,000 DKK either side of the golden end."""
    out = {}
    for f in FMT:
        for j, end in enumerate(["lo", "hi"]):
            g = R["G"]["range"][f][j]
            vs = [g] + [v[f][j] for v in variants]
            lo = min(min(vs) - 1500, g - 5000)
            hi = max(max(vs) + 1500, g + 5000)
            out[f + "_" + end] = [r100(lo), r100(hi)]
    return out


def build(R):
    G, C, Q, H = R["G"], R["C"], R["Q"], R["H"]
    F = {}
    F["pilot_growth_pct"] = r1(100 * H["pilot"]["growth"])
    F["other_growth_pct"] = r1(100 * H["other"]["growth"])
    F["gap_sales_pp"] = r1(H["gap_sales_pp"])
    F["pilot_waste_change_pct"] = r1(100 * H["pilot"]["wchange"])
    F["other_waste_change_pct"] = r1(100 * H["other"]["wchange"])
    F["gap_waste_pp"] = r1(H["gap_waste_pp"])
    F["headline_gaps"] = {"sales": F["gap_sales_pp"], "waste": F["gap_waste_pp"]}
    F["pilot_sales_2026_dkk"] = r100(H["pilot"]["sales1"])
    F["pilot_sales_2025_dkk"] = r100(H["pilot"]["sales0"])
    F["other_sales_2026_dkk"] = r100(H["other"]["sales1"])
    F["other_sales_2025_dkk"] = r100(H["other"]["sales0"])
    F["pilot_waste_2026_dkk"] = r100(H["pilot"]["waste1"])
    F["pilot_waste_2025_dkk"] = r100(H["pilot"]["waste0"])
    F["other_waste_2026_dkk"] = r100(H["other"]["waste1"])
    F["other_waste_2025_dkk"] = r100(H["other"]["waste0"])
    F["duplicate_rows_2025"] = int(R["T"]["n_dup25"])
    sd, wd = G["decomp"]["sales"], G["decomp"]["waste"]
    F["sales_split"] = split(sd, sd["gap"], ["forecast", "competitors", "format_mix"])
    F["waste_split"] = split(wd, wd["gap"], ["forecast", "competitors", "format_mix"])
    F["sales_split_parts"] = {k: F["sales_split"][k] for k in ["forecast", "competitors", "format_mix"]}
    F["waste_split_parts"] = {k: F["waste_split"][k] for k in ["forecast", "competitors", "format_mix"]}
    F["sales_split_residual_forecast"] = r1(sd["gap"] - sd["competitors"] - sd["format_mix"])
    F["waste_split_residual_forecast"] = r1(wd["gap"] - wd["competitors"] - wd["format_mix"])
    F["growth_by_format_pct"] = {f: r1(100 * v) for f, v in G["decomp"]["growth_by_format"].items()}
    F["waste_change_by_format_pct"] = {f: r1(100 * v) for f, v in G["decomp"]["waste_change_by_format"].items()}
    lu, lc = G["lost_units"], C["lost_units"]
    F["lost_units"] = {"pilot_2026": r100(lu["pilot_pilot"]), "pilot_2025": r100(lu["pilot_base"])}
    F["lost_units_other"] = {"other_2026": r100(lu["other_pilot"]), "other_2025": r100(lu["other_base"])}
    F["lost_units_plain"] = {"pilot_2026": r100(lc["pilot_pilot"]), "pilot_2025": r100(lc["pilot_base"])}
    clip = R["rivals"]["clip_type"]["lost_units"]
    F["lost_units_clipped"] = {"pilot_2026": r100(clip["pilot_pilot"]), "pilot_2025": r100(clip["pilot_base"])}
    sp = G["sp"]
    isp = sp["pilot"]
    F["lost_share_pilot_2026_pct"] = r1(100 * lu["pilot_pilot"] / (sp.loc[isp, "units_pilot"].sum() + lu["pilot_pilot"]))
    F["lost_share_pilot_2025_pct"] = r1(100 * lu["pilot_base"] / (sp.loc[isp, "units_base"].sum() + lu["pilot_base"]))
    chk = R["check"]
    F["check_plain_over_pct"] = r1(100 * chk["plain_over"])
    F["check_plain_over_small_pct"] = r1(100 * chk["plain_over_small"])
    F["check_os_over_pct"] = r1(100 * chk["os_over"])
    F["check_os_over_small_pct"] = r1(100 * chk["os_over_small"])
    F["check_clip_over_pct"] = r1(100 * chk["clip_over"])
    F["check_days"] = int(chk["days"])
    F["competitor_effect_pct"] = {str(s): r1(100 * e["effect"]) for s, e in sorted(G["eff"].items())}
    rw, rm = G["rates"]["waste"], G["rates"]["margin"]
    F["waste_rate_pct"] = {"weekend": r1(100 * rw["weekend"]), "commuter": r1(100 * rw["commuter"])}
    F["margin_rate_pct"] = {"weekend": round(100 * rm["weekend"], 2), "commuter": round(100 * rm["commuter"], 2)}
    F["weekend_cut"] = round(float(G["cut"]), 2)
    typ = sp["type"]
    F["n_commuter"] = {f: int(((sp["format"] == f) & (typ == "commuter")).sum()) for f in FMT}
    F["n_stores"] = {f: int((sp["format"] == f).sum()) for f in FMT}
    F["n_commuter_pilot"] = {f: int(((sp["format"] == f) & (typ == "commuter") & isp).sum()) for f in FMT}
    F["n_pilot"] = {f: int(((sp["format"] == f) & isp).sum()) for f in FMT}
    F["shadow_ratio"] = {"commuter": round(float(R["shadow_type"]["commuter"]), 2),
                         "weekend": round(float(R["shadow_type"]["weekend"]), 2)}
    F["shadow_ratio_range"] = {"commuter": [2.0, 2.6], "weekend": [0.85, 1.0]}
    F["saving"] = {f: r100(G["format_saving"][f]) for f in FMT}
    F["range"] = {f: [r100(G["range"][f][0]), r100(G["range"][f][1])] for f in FMT}
    F["range_ends"] = dict([(f + "_lo", F["range"][f][0]) for f in FMT] + [(f + "_hi", F["range"][f][1]) for f in FMT])
    F["licence"] = {f: int(GD.LICENCE[f]) for f in FMT}
    F["switch"] = G["switch"]
    F["keep"] = [f for f in FMT if f not in G["switch"]]
    F["margin_over_licence"] = {f: r100(G["format_saving"][f] - GD.LICENCE[f]) for f in FMT}
    F["routes"] = {nm: {"saving": {f: r100(r["format_saving"][f]) for f in FMT}, "switch": r["switch"]}
                   for nm, r in R["routes"].items()}
    F["rivals"] = {nm: {"saving": {f: r100(r["format_saving"][f]) for f in FMT}, "switch": r["switch"]}
                   for nm, r in R["rivals"].items()}
    F["careful"] = {"saving": {f: r100(C["format_saving"][f]) for f in FMT}, "switch": C["switch"],
                    "range": {f: [r100(C["range"][f][0]), r100(C["range"][f][1])] for f in FMT}}
    F["quick"] = {"saving": {f: r100(Q["format_saving"][f]) for f in FMT}, "switch": Q["switch"],
                  "dashboard_rate_pct": r1(100 * Q["rates"]["dashboard"])}
    F["careful_waste_rate_by_format_pct"] = {f: r1(100 * v) for f, v in C["rates"]["waste"].items()}
    F["by_format_waste_rate_pct"] = {f: r1(100 * v) for f, v in R["routes"]["by_format"]["rates"]["waste"].items()}
    P = G["P"]
    F["pilot_store_saving"] = {str(s): {"format": P.loc[s, "format"], "type": P.loc[s, "type"],
                                        "waste_saving": r100(P.loc[s, "waste_saving"]),
                                        "margin_change": r100(P.loc[s, "margin_change"]),
                                        "saving_26wk": r100(P.loc[s, "saving"])} for s in P.index}
    b8, span8 = saving_bands(R)
    F["saving_band"] = b8
    F["saving_rival_span"] = span8
    F["range_band"] = R["range_bands"]
    F["recorded_route_spread"] = R["placebo"]
    wb_ = sp.groupby("format")["waste_base"].sum() / sp.groupby("format")["sales_base"].sum()
    F["waste_to_sales_2025_pct"] = {f: r1(100 * wb_[f]) for f in FMT}
    F["n_stores_total"] = int(len(sp))
    F["opening_stores"] = [int(s) for s in sorted(G["eff"])]
    F["pilot_opening_stores"] = [int(s) for s in sorted(G["eff"]) if s in set(sp.index[sp["pilot"]])]
    F["pilot_weeks"] = [10, 35]
    F["pilot_waste_fall_pct"] = r1(-100 * H["pilot"]["wchange"])
    Pw = G["P"][G["P"]["type"] == "weekend"]
    mg = Pw.groupby("format")[["margin_change", "sales_base", "waste_base"]].mean()
    F["weekend_pilot_super_over_kvarter"] = {"margin": r1(mg.loc["Super", "margin_change"] / mg.loc["Kvarter", "margin_change"]),
                                             "sales": r1(mg.loc["Super", "sales_base"] / mg.loc["Kvarter", "sales_base"]),
                                             "waste": r1(mg.loc["Super", "waste_base"] / mg.loc["Kvarter", "waste_base"])}
    Rf = R["routes"]["recorded_fxt"]["P"]
    F["store_2158_margin_change"] = {"recorded": r100(Rf.loc[2158, "margin_change"]), "turned_away": r100(G["P"].loc[2158, "margin_change"])}
    F["store_2158_margin_shortfall"] = {"store": 2158, "recorded": abs(F["store_2158_margin_change"]["recorded"]),
                                        "turned_away": abs(F["store_2158_margin_change"]["turned_away"])}
    n_sp = int(((G["sp"]["format"] == "Super") & G["sp"]["pilot"]).sum())
    F["super_margin_noise_per_year"] = {"recorded": r100(2 * R["placebo"]["Super"]["recorded_sd"] / np.sqrt(n_sp)),
                                        "turned_away": r100(2 * R["placebo"]["Super"]["turned_away_sd"] / np.sqrt(n_sp))}
    F["weekend_pilot_saving_share"] = {
        fm: {"of_sales_pct": round(100 * Pw.loc[Pw["format"] == fm, "saving"].sum() / Pw.loc[Pw["format"] == fm, "sales_base"].sum(), 2),
             "of_waste_pct": r1(100 * Pw.loc[Pw["format"] == fm, "saving"].sum() / Pw.loc[Pw["format"] == fm, "waste_base"].sum())}
        for fm in FMT if (Pw["format"] == fm).any()}
    F["agreement_clauses"] = [4.1, 4.2, 4.3]
    F["range_level_pct"] = 80
    F["resamples"] = 400
    lcl = F["lost_units_clipped"]
    ss, ws, hg = F["sales_split_parts"], F["waste_split_parts"], F["headline_gaps"]
    F["bands"] = {
        "gap_sales": [r1(hg["sales"] - 0.1), r1(hg["sales"] + 0.1)],
        "gap_waste": [r1(hg["waste"] - 0.2), r1(hg["waste"] + 0.2)],
        "lost_units": {k: [r100(min(F["lost_units"][k], lcl[k]) * 0.96), r100(max(F["lost_units"][k], lcl[k]) * 1.05)]
                       for k in F["lost_units"]},
        "check_plain_over": [8.0, 14.0],
        "competitor_effect": {k: [r1(v - 2.0), r1(v + 2.0)] for k, v in F["competitor_effect_pct"].items()},
        "sales_split": {"forecast": [-1.05, -0.55], "competitors": [r1(ss["competitors"] - 0.2), r1(ss["competitors"] + 0.2)],
                        "format_mix": [r1(ss["format_mix"] - 0.2), r1(ss["format_mix"] + 0.2)]},
        "waste_split": {"forecast": [r1(ws["forecast"] - 0.8), r1(ws["forecast"] + 0.8)],
                        "competitors": [r1(ws["competitors"] - 0.2), r1(ws["competitors"] + 0.2)],
                        "format_mix": [r1(ws["format_mix"] - 0.4), r1(ws["format_mix"] + 0.4)]},
        "waste_rate": {"weekend": [16.0, 24.0], "commuter": [-4.5, 5.0]},
        "saving": b8,
        "range": R["range_bands"],
    }
    return F


def effort(R, F):
    G, C, Q = R["G"], R["C"], R["Q"]
    results = []
    hg = F["gap_sales_pp"], F["gap_waste_pp"]
    results.append(dict(id="R1", name="the pilot stores' two headline gaps against the other stores", graded_as="Ask 1",
                        figure="headline_gaps", depends=[], independent="",
                        golden={"sales": hg[0], "waste": hg[1]},
                        bands={"sales": F["bands"]["gap_sales"], "waste": F["bands"]["gap_waste"]},
                        passes={p: {"sales": hg[0], "waste": hg[1]} for p in ("quick", "careful", "thorough")}))
    lu, lp, lcl = F["lost_units"], F["lost_units_plain"], F["lost_units_clipped"]
    b2 = F["bands"]["lost_units"]
    results.append(dict(id="R2", name="the units the pilot stores' empty shelves turned away, pilot weeks and the same weeks of 2025",
                        graded_as="Component 1", figure="lost_units", depends=["R1"],
                        independent="the daily record's closing stock and last-sale times and the hourly profile",
                        golden=lu, bands=b2, passes={"quick": {"pilot_2026": 0, "pilot_2025": 0}, "careful": lp, "thorough": lu}))
    g3 = F["check_plain_over_pct"]
    results.append(dict(id="R3", name="the turned-away estimate checked on the days the shelf did not run out",
                        graded_as="Component 2", figure="check_plain_over_pct", depends=[], independent="the in-stock days",
                        golden=g3, band=F["bands"]["check_plain_over"],
                        passes={"quick": {"value": None, "grade": "missed", "why": "no turned-away estimate is made, so none is checked"},
                                "careful": {"value": None, "grade": "missed", "why": "the plain estimate is used unchecked; the in-stock days are never read back"},
                                "thorough": g3}))
    ce = F["competitor_effect_pct"]
    results.append(dict(id="R4", name="each competitor opening's effect on its store's trade", graded_as="Component 4",
                        figure="competitor_effect_pct", depends=[], independent="the ambient weekly sales",
                        golden=ce, bands=F["bands"]["competitor_effect"], partly_share=0.5,
                        passes={"quick": {k: 0.0 for k in ce},
                                "careful": {str(s): r1(100 * e["effect"]) for s, e in sorted(C["eff"].items())},
                                "thorough": ce}))
    ss = F["sales_split_parts"]
    cs = split(C["decomp"]["sales"], C["decomp"]["sales"]["gap"], ["forecast", "competitors", "format_mix"])
    keys5 = ["forecast", "competitors", "format_mix"]
    b5 = F["bands"]["sales_split"]
    results.append(dict(id="R5", name="the sales growth gap split into its causes", graded_as="Ask 1",
                        figure="sales_split_parts", depends=["R1", "R4"], independent="",
                        golden=ss, bands=b5, partly_share=0.6,
                        passes={"quick": {"forecast": F["gap_sales_pp"], "competitors": 0.0, "format_mix": 0.0},
                                "careful": {k: cs[k] for k in keys5}, "thorough": ss}))
    ws = F["waste_split_parts"]
    cw = split(C["decomp"]["waste"], C["decomp"]["waste"]["gap"], ["forecast", "competitors", "format_mix"])
    results.append(dict(id="R6", name="the waste gap split into its causes", graded_as="Ask 2", figure="waste_split_parts",
                        depends=["R1"], independent="",
                        golden=ws, bands=F["bands"]["waste_split"],
                        passes={"quick": {"forecast": F["gap_waste_pp"], "competitors": 0.0, "format_mix": 0.0},
                                "careful": {k: cw[k] for k in ["forecast", "competitors", "format_mix"]}, "thorough": ws}))
    g7 = F["waste_rate_pct"]
    results.append(dict(id="R7", name="what the forecast's saving depends on in a store: its trading week",
                        graded_as="Component 3", figure="waste_rate_pct", depends=[],
                        independent="the stores' own weekly trade and the shadow forecasts",
                        golden=g7, bands=F["bands"]["waste_rate"],
                        passes={"quick": {"value": None, "grade": "missed", "why": "one saving rate from the dashboard for every store"},
                                "careful": {"value": None, "grade": "missed", "why": "each format's rate read off its own pilot stores; the trading week never enters"},
                                "thorough": g7}))
    g8 = F["saving"]
    results.append(dict(id="R8", name="each format's expected yearly saving per store", graded_as="Ask 3",
                        figure="saving", depends=["R2", "R4", "R7"], independent="",
                        golden=g8, bands=F["saving_band"], partly_share=0.6,
                        passes={"quick": F["quick"]["saving"], "careful": F["careful"]["saving"], "thorough": g8}))
    g9 = F["range_ends"]
    c9 = dict([(f + "_lo", F["careful"]["range"][f][0]) for f in FMT] + [(f + "_hi", F["careful"]["range"][f][1]) for f in FMT])
    results.append(dict(id="R9", name="the 80 per cent range on each format's saving", graded_as="Ask 3", figure="range_ends",
                        depends=["R8"], independent="", golden=g9, bands=F["range_band"], partly_share=0.65,
                        passes={"quick": {"value": None, "grade": "missed", "why": "a point figure from the dashboard, no range"},
                                "careful": c9, "thorough": g9}))
    results.append(dict(id="R10", name="the formats to switch for 2027", graded_as="Recommendation", figure="switch",
                        depends=["R8"], independent="", golden=G["switch"],
                        passes={"quick": {"value": Q["switch"], "grade": "missed",
                                          "why": "switches To Go as well, whose stores the forecast does not pay for; the call is one set"},
                                "careful": {"value": C["switch"], "grade": "missed",
                                            "why": "switches To Go and keeps the Kvarter stores on AutoOrdre; the call is one set"},
                                "thorough": G["switch"]}))
    hints = [
        {"sentence": "the plain turned-away estimate overstates small counts, as the days the shelf did not run out show",
         "rescues": ["R2", "R3"]},
        {"sentence": "the new forecast reads every store's week like a big weekend store's, so its saving follows a store's trading week, not its format",
         "rescues": ["R7"]},
        {"sentence": "two discounters opened near pilot stores during the pilot", "rescues": []},
    ]
    routes = [{"name": "the golden", "answer": sorted(G["switch"], key=ORDER.get), "golden": True},
              {"name": "careful but hurried", "answer": sorted(C["switch"], key=ORDER.get)},
              {"name": "the dashboard", "answer": sorted(Q["switch"], key=ORDER.get)}]
    for nm, r in R["routes"].items():
        routes.append({"name": nm, "answer": sorted(r["switch"], key=ORDER.get)})
    return {"results": results, "hints": hints, "routes": routes,
            "weights": {"recommendation": 14, "components": 24, "asks": 55, "instruction": 7}}


def extras(R, T, reps=400):
    """The range variants for R9's bands and the recorded-margin route's spread on the stores that kept AutoOrdre."""
    G = R["G"]
    sp, eff = G["sp"], G["eff"]
    variants = []
    for kw in [dict(seed=12), dict(seed=13, reps=800), dict(scheme="pilot_only")]:
        k = dict(reps=reps, key="type", mscale="sales_base", seed=11)
        k.update(kw)
        lo, hi, _ = GD.bootstrap_formats(T, sp, eff, **k)
        variants.append({f: (float(lo[f]), float(hi[f])) for f in FMT})
    R["range_variants"] = variants
    R["range_bands"] = range_bands(R, variants)
    R["placebo"] = GD.placebo_spread(T, sp, eff)
    return R


def write(R, out_dir=HERE):
    F = build(R)
    E = effort(R, F)
    F = json.loads(json.dumps(F, default=_conv))
    E = json.loads(json.dumps(E, default=_conv))
    json.dump(F, open(os.path.join(out_dir, "figures.json"), "w"), indent=1, ensure_ascii=False)
    json.dump(E, open(os.path.join(out_dir, "effort.json"), "w"), indent=1, ensure_ascii=False)
    return F, E


def _conv(o):
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    raise TypeError(type(o))
