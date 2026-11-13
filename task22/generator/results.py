"""task22 architecture 2: the graded results computed from the cut pack under the golden and each pass's route,
figures.json (what the answer blocks state) and effort.json (what effort.py scores), with the routes, the one-fact
hints and the forcing on both sides."""
import json
import os

import numpy as np

import analysis as A
import params as P

ROUTES = {
    "golden": {},
    "careful": dict(cal="uniform", temp="logger_air", div="all", plan="plan"),
    "quick": dict(cal="billed", temp="none", div="none", drs="raw", plan="plan"),
}
FAMILY = [("the golden: each read spread on its district's daily sendout, gas temperature tied to the soil", {}),
          ("reads spread on a base-and-degree-day fit of each district's sendout", dict(cal="fit")),
          ("gas temperature tied to the commercial correctors' gas temperature", dict(temp="evc")),
          ("both rivals together", dict(cal="fit", temp="evc"))]
SHORTCUTS = [("the logger study's straight line on the airport's air", dict(temp="logger_air")),
             ("the 2019 consultant's monthly mean air temperature", dict(temp="monthly_air")),
             ("each read spread evenly over its days", dict(cal="uniform")),
             ("bills taken in the month they were read", dict(cal="billed")),
             ("no diversion subtracted", dict(div="none")),
             ("every collapse in use booked as diversion", dict(div="all")),
             ("the careful but hurried route", ROUTES["careful"])]
PERTURB = [("gas temperature's air coefficient -20%", dict(k_scale=0.8)),
           ("gas temperature's air coefficient +20%", dict(k_scale=1.2)),
           ("indoor gas temperature -2 F", dict(in_shift=-2.0)), ("indoor gas temperature +2 F", dict(in_shift=2.0)),
           ("damage reports -20%", dict(dmg_scale=0.8)), ("damage reports +20%", dict(dmg_scale=1.2)),
           ("own use -20%", dict(own_scale=0.8)), ("own use +20%", dict(own_scale=1.2)),
           ("diversion volumes -20%", dict(div_scale=0.8)), ("diversion volumes +20%", dict(div_scale=1.2))]
HINTS = [("Gas in a buried service runs near the soil's temperature, and the 2025-26 snow kept the soil warm; the "
          "commercial correctors log what the gas actually was.", dict(temp="soil")),
         ("Spread each read period's gas over its days the way the district's own regulator station took it.",
          dict(cal="shape")),
         ("A snowbird's winter use keeps some heating and comes back in summer; a bypass or a furnace tap does not.",
          dict(div="golden")),
         ("Past changeouts finished at the pace access allowed, slowest where the meter is inside.", dict(plan="pace"))]

R1_CELLS = [("RS", "2026-01", "Riverside, January 2026"), ("LV", "2025-12", "Lakeview, December 2025")]
R2_CELLS = [("CH", "2026-01", "College Hill, January 2026"), ("NE", "2026-03", "North End, March 2026"),
            ("OT", "2025-10", "Old Town, October 2025"), ("HV", "2025-10", "Halvorsen, October 2025")]
R3_MCF = ["RS", "LV"]
R3_PCT = ["CH", "AP", "HV"]
R4_DIST = ["EG", "EI", "SQ"]
R5_DIST = ["RS", "LV", "SQ", "HV", "EG", "EI", "CH"]


def names(codes):
    return [P.DNAME[c] for c in codes]


def figures(R):
    mon = R["monthly"].set_index(["district", "month"])
    agg = R["agg"]
    div = R["diversion"]
    f = {}
    f["R1_gas_in"] = {lab: round(float(mon.loc[(c, m), "inflow"]), 1) for c, m, lab in R1_CELLS}
    f["R1_gas_in"]["fourteen districts, twelve months to September 2026"] = round(float(agg["inflow"].sum()), 0)
    f["R2_billed_months"] = {lab: round(float(mon.loc[(c, m), "billed"]), 1) for c, m, lab in R2_CELLS}
    r3 = {"%s, Mcf" % P.DNAME[c]: round(float(agg.loc[c, "under"]), 0) for c in R3_MCF}
    r3.update({"%s, per cent" % P.DNAME[c]: round(float(agg.loc[c, "ur_pct"]), 2) for c in R3_PCT})
    f["R3_under"] = r3
    n = int(len(div)) if len(div) else 0
    r4 = {"accounts": n}
    for c in R4_DIST:
        r4["%s, Mcf" % P.DNAME[c]] = round(float(div[div["district"] == c]["mcf_window"].sum()) if n else 0.0, 0)
    f["R4_diversion"] = r4
    f["R5_leak_pct"] = {P.DNAME[c]: round(float(agg.loc[c, "leak_pct"]), 2) for c in R5_DIST}
    f["R6_designated"] = names(R["designated"])
    f["R7_changeout"] = names(R["changeout"])
    f["R8_done_before_season"] = int(round(R["plan"]["done"]))
    return f


BANDS = {
    "R1_gas_in": lambda k, v: (v * 0.985, v * 1.015) if "twelve" not in k else (v * 0.997, v * 1.003),
    "R2_billed_months": lambda k, v: (v * 0.98, v * 1.02),
    "R3_under": lambda k, v: (v * 0.94, v * 1.06) if k.endswith("Mcf") else (v - 0.20, v + 0.20),
    "R4_diversion": lambda k, v: (v - 1, v + 1) if k == "accounts" else (v * 0.75, v * 1.25),
    "R5_leak_pct": lambda k, v: (v - 0.10, v + 0.10),
    "R8_done_before_season": lambda k, v: (v * 0.96, v * 1.04),
}
PARTLY = {
    "R1_gas_in": lambda k, v: (v * 0.97, v * 1.03) if "twelve" not in k else (v * 0.994, v * 1.006),
    "R2_billed_months": lambda k, v: (v * 0.96, v * 1.04),
    "R3_under": lambda k, v: (v * 0.88, v * 1.12) if k.endswith("Mcf") else (v - 0.40, v + 0.40),
    "R4_diversion": lambda k, v: (v - 3, v + 3) if k == "accounts" else (v * 0.5, v * 1.5),
    "R5_leak_pct": lambda k, v: (v - 0.20, v + 0.20),
    "R8_done_before_season": lambda k, v: (v * 0.92, v * 1.08),
}
META = [
    ("R1", "each district's gas in at its regulator stations, faulty days rebuilt from the gate", "R1_gas_in",
     "Ask 1", [], "the regulator station correctors and the city gate", None),
    ("R2", "the volume billed for each district's meters, carried to calendar months", "R2_billed_months",
     "Component 4", [], "the cycle reads and the regulator stations' daily volumes", ["N20"]),
    ("R3", "the under-registration of the meters that do not compensate for gas temperature", "R3_under",
     "Component 1", [], "the loggers, the soil station and the commercial correctors", ["L22", "L37", "N04"]),
    ("R4", "the accounts that took gas without authorization, and their volume", "R4_diversion", "Component 3", [],
     "each account's reads against its own weather response a year earlier", ["L26"]),
    ("R5", "each district's leak loss in the twelve months to September 2026, per cent of its gas in",
     "R5_leak_pct", "Component 2", ["R1", "R2", "R3", "R4"], "", ["L22", "L26", "N20"]),
    ("R6", "the districts that enter the 2027-2029 main replacement program", "R6_designated", "Recommendation",
     ["R5"], "", ["L22", "L26", "N20"]),
    ("R7", "the districts where the 2027 meter changeout goes", "R7_changeout", "Ask 2", ["R3"], "",
     ["L22", "L37", "N04"]),
    ("R8", "the scheduled 2027 changeouts done before the 2027-28 heating season", "R8_done_before_season",
     "Ask 3", [], "the 2024-25 work orders and the 2027 plan", ["N22", "N03"]),
]


def run_all(F):
    cache = {}
    out = {k: A.run(F, o, cache) for k, o in ROUTES.items()}
    fam = [(n, A.run(F, o, cache)) for n, o in FAMILY]
    sc = [(n, A.run(F, o, cache)) for n, o in SHORTCUTS]
    pt = [(n, A.run(F, o, cache)) for n, o in PERTURB]
    hints = []
    for sent, o in HINTS:
        oo = dict(ROUTES["careful"])
        oo.update(o)
        hints.append((sent, A.run(F, oo, cache)))
    return out, fam, sc, pt, hints, cache


def _inside(v, band):
    return band[0] <= v <= band[1]


def grade(key, golden, val):
    if isinstance(golden, list):
        if sorted(golden) == sorted(val):
            return "right"
        share = len(set(golden) & set(val)) / max(1, len(set(golden) | set(val)))
        return "partly" if share >= 0.5 else "missed"
    if isinstance(golden, dict):
        ins = [_inside(val[k], BANDS[key](k, golden[k])) for k in golden]
        if all(ins):
            return "right"
        return "partly" if np.mean(ins) >= 0.5 else "missed"
    if _inside(val, BANDS[key](key, golden)):
        return "right"
    return "partly" if _inside(val, PARTLY[key](key, golden)) else "missed"


def write(F, gen_out):
    out, fam, sc, pt, hints, cache = run_all(F)
    G = figures(out["golden"])
    Cf = figures(out["careful"])
    Qf = figures(out["quick"])
    res = []
    for rid, name, fig, graded, dep, indep, prec in META:
        g = G[fig]
        r = dict(id=rid, name=name, graded_as=graded, figure=fig, depends=dep, independent=indep, golden=g)
        if isinstance(g, dict):
            r["bands"] = {k: [round(x, 2) for x in BANDS[fig](k, v)] for k, v in g.items()}
            r["partly_share"] = 0.5
        elif not isinstance(g, list):
            r["band"] = [round(x, 2) for x in BANDS[fig](fig, g)]
            r["partly"] = [round(x, 2) for x in PARTLY[fig](fig, g)]
        r["passes"] = {"quick": Qf[fig], "careful": Cf[fig], "thorough": g}
        if prec:
            r["precedent"] = prec
        res.append(r)
    hint_rows = []
    for sent, R in hints:
        h = figures(R)
        resc = [rid for rid, _, fig, *_ in META if grade(fig, G[fig], h[fig]) == "right"
                and grade(fig, G[fig], Cf[fig]) != "right"]
        hint_rows.append(dict(sentence=sent, rescues=resc))
    routes = [dict(name="the golden", answer=G["R6_designated"], golden=True)]
    for n, R in sc:
        routes.append(dict(name=n, answer=names(R["designated"])))
    forcing = dict(kind="set", line="leak loss over 1.0 per cent of the gas delivered into the district",
                   golden_family=[dict(name=n, answer=names(R["designated"])) for n, R in fam],
                   perturbations=[dict(input=n, answer=names(R["designated"])) for n, R in pt])
    changeout_forcing = dict(golden_family=[dict(name=n, answer=names(R["changeout"])) for n, R in fam],
                             perturbations=[dict(input=n, answer=names(R["changeout"])) for n, R in pt],
                             shortcuts=[dict(name=n, answer=names(R["changeout"])) for n, R in sc])
    margins = {}
    agg = out["golden"]["agg"]
    for c in P.DCODES:
        margins[P.DNAME[c]] = dict(leak_pct=round(float(agg.loc[c, "leak_pct"]), 3),
                                   ur_pct=round(float(agg.loc[c, "ur_pct"]), 3) if np.isfinite(agg.loc[c, "ur_pct"]) else None,
                                   ntc_meters=int(agg.loc[c, "ntc_meters"]),
                                   family_leak=[round(float(R["agg"].loc[c, "leak_pct"]), 3) for _, R in fam],
                                   perturbed_leak=[round(float(R["agg"].loc[c, "leak_pct"]), 3) for _, R in pt])
    E = dict(results=res, hints=hint_rows, routes=routes, forcing=forcing, changeout_forcing=changeout_forcing,
             margins=margins, weights={"recommendation": 14, "components": 24, "asks": 55, "instruction": 7})
    extra = dict(golden_monthly=out["golden"]["monthly"].round(3).to_dict(orient="records"),
                 tpar={k: float(v) for k, v in out["golden"]["tpar"].items()},
                 plan=out["golden"]["plan"], careful_designated=names(out["careful"]["designated"]),
                 careful_changeout=names(out["careful"]["changeout"]),
                 shortcut_sets={n: names(R["designated"]) for n, R in sc},
                 shortcut_changeouts={n: names(R["changeout"]) for n, R in sc},
                 leak_table={n: {P.DNAME[c]: round(float(R["agg"].loc[c, "leak_pct"]), 2) for c in P.DCODES}
                             for n, R in [("golden", out["golden"]), ("careful", out["careful"])] + sc + fam},
                 ur_table={n: {P.DNAME[c]: round(float(R["agg"].loc[c, "ur_pct"]), 2) for c in P.DCODES}
                           for n, R in [("golden", out["golden"]), ("careful", out["careful"])] + sc + fam},
                 diversion_accounts=out["golden"]["diversion"].to_dict(orient="records"),
                 careful_diversion_accounts=int(len(out["careful"]["diversion"])),
                 careful_r2_ch=Cf["R2_billed_months"]["College Hill, January 2026"])
    figs = dict(G)
    figs["monthly_rows"] = int(len(out["golden"]["monthly"]))
    figs["rule1_line"] = P.LEAK_LINE
    figs["rule2_line"] = P.CHANGEOUT_LINE
    figs["rule2_min_meters"] = P.CHANGEOUT_MIN_METERS
    figs["_extra"] = extra
    json.dump(figs, open(os.path.join(gen_out, "figures.json"), "w"), indent=1, default=str)
    json.dump(E, open(os.path.join(gen_out, "effort.json"), "w"), indent=1, default=str)
    return figs, E, out, cache
