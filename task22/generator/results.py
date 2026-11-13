"""task22 architecture 2 (redesigned after the review of 2026-11-13): the graded results computed from the cut pack
under the golden and each pass's route, figures.json (what the answer blocks state) and effort.json (what effort.py
scores), with the routes, the stump factorial, the variant battery, the one-fact hints and the forcing on both sides.

The careful but hurried pass is the route both platform runs took on this world (runs/arch2_run1.md, arch2_run2.md):
every move they made unprompted set right (the soil-aware gas temperature R71, degree-day calendarization R72, the
station repairs R74, the changeout pace R73) and the three judgments they did not make left hurried (every fall in use
booked as gas taken without authorization, rebated homes aside; no cold-day test; every corrector's volume taken as
recorded)."""
import json
import os

import numpy as np

import analysis as A
import params as P

ROUTES = {
    "golden": {},
    "careful": dict(cal="fit", temp="soil", div="all", z="rec"),
    "quick": dict(cal="billed", temp="none", div="none", drs="raw", z="rec"),
}
# the golden family: each rival method a careful analyst could defend, run on the cut pack
FAMILY = [("each read spread on a base-and-degree-day fit of its district's sendout", dict(cal="fit")),
          ("the outdoor gas temperature tied to the commercial correctors' gas temperature", dict(temp="evc")),
          ("supercompressibility from Hall and Yarborough", dict(z="hy")),
          ("supercompressibility fitted on the EVC-II stations' own records", dict(z="fit")),
          ("the three rivals together", dict(cal="fit", temp="evc", z="hy"))]
# the variant battery: every modelled transport rebuilt the ways the field does it (determinism-check section 1)
BATTERY = [(z, cal, temp) for z in ("dak", "hy", "fit") for cal in ("shape", "fit") for temp in ("soil", "evc")]
# the detection's conventions, each at the values a careful analyst would defend
DETECTION = [("collapse cut %.2f" % c, dict(cut=c)) for c in (0.35, 0.45)] + \
            [("home in May at %.2f of the household's own weather response" % h, dict(home_cut=h)) for h in (0.6, 0.8)] + \
            [("cold-day slope over %.1f of the household's own" % d, dict(df_cut=d)) for d in (0.2, 0.4)] + \
            [("switchover at or below %d F" % t, dict(df_tmax=t)) for t in (5, 15)] + \
            [("summer base cut %.1f" % s, dict(summer_cut=s)) for s in (0.3, 0.5)] + \
            [("runs of four low months", dict(run=4))] + \
            [("vacancy at %d months" % v, dict(vacant_months=v)) for v in (1, 3)]
SHORTCUTS = [("every fall in use booked as gas taken without authorization (the dual-fuel homes aside)",
              dict(div="allx")),
             ("every lost heating response booked as a furnace tap, no cold-day test", dict(div="nodf")),
             ("every corrector's volume taken as recorded", dict(z="rec")),
             ("the careful but hurried route (all three)", ROUTES["careful"]),
             ("every fall booked and every corrector as recorded, the gas temperature on the study's air line",
              dict(ROUTES["careful"], temp="logger_air")),
             ("every fall booked and every corrector as recorded, reads spread evenly over their days",
              dict(ROUTES["careful"], cal="uniform")),
             ("every fall in use booked as gas taken without authorization (rebated homes aside)", dict(div="all")),
             ("no gas taken without authorization subtracted", dict(div="none")),
             ("each faulty station day at the station's interpolated share of the gate", dict(drs="share"))]
PERTURB = [("gas temperature's air coefficient -20%", dict(k_scale=0.8)),
           ("gas temperature's air coefficient +20%", dict(k_scale=1.2)),
           ("indoor gas temperature -2 F", dict(in_shift=-2.0)), ("indoor gas temperature +2 F", dict(in_shift=2.0)),
           ("damage reports -20%", dict(dmg_scale=0.8)), ("damage reports +20%", dict(dmg_scale=1.2)),
           ("own use -20%", dict(own_scale=0.8)), ("own use +20%", dict(own_scale=1.2)),
           ("unauthorized volumes -20%", dict(div_scale=0.8)), ("unauthorized volumes +20%", dict(div_scale=1.2))]
HINTS = [("Four of the station correctors and every customer corrector correct for pressure and temperature only; at 25 "
          "to 58 psig the gas is not an ideal gas.", dict(z="dak")),
         ("A household away for the winter is back at its own weather response in May; a tap or a bypass is not.",
          dict(div="nodf")),
         ("A dual-fuel heat pump leaves the furnace the whole load on the coldest days, read period by read period.",
          dict(div="allx")),
         ("Gas in a buried service runs near the soil's temperature, and the 2025-26 snow kept the soil warm.",
          dict(temp="soil")),
         ("Spread each read period's gas over its days the way the district's own regulator station took it.",
          dict(cal="shape"))]
# the factorial's judgments: (id, name, kind, precedent, dropped from the golden, set right on the reflex route)
JUDGMENTS = [("J1", "a household away for the winter told from a tap by its heating response in May", "stump",
              ["L47", "N36"], dict(div="allx"), dict(div="nodf")),
             ("J2", "a dual-fuel heat pump told from a furnace tap by its cold-day response", "stump",
              ["N36"], dict(div="nodf"), dict(div="allx")),
             ("J3", "every corrector put on the real-gas basis (supercompressibility)", "stump",
              ["L28"], dict(z="rec"), dict(z="dak")),
             ("J4", "the gas temperature in the buried services on the soil", "reflex", ["R71"],
              dict(temp="logger_air"), None),
             ("J5", "the cycle reads carried to months on a weather shape", "reflex", ["R72"], dict(cal="uniform"), None),
             ("J6", "the stations' faulty days rebuilt from the gate", "reflex", ["R74", "R39"], dict(drs="raw"), None)]

R1_CELLS = [("RS", "inflow", "Riverside, gas in, twelve months to September 2026"),
            ("CH", "inflow", "College Hill, gas in, twelve months to September 2026"),
            ("EI", "evc", "East Industrial, corrector customers, twelve months to September 2026")]
R1_MONTH = [("LV", "2025-12", "inflow", "Lakeview, gas in, December 2025")]
R3_DIST = ["RS", "LV", "SQ", "EI", "HV", "EG", "CH", "DT"]
R5_DIST = ["EG", "EI", "SQ", "OT"]


def names(codes):
    return [P.DNAME[c] for c in codes]


def accounts_of(F, prem, first_month):
    """The accounts holding a premise from the month its use fell to the end of the twelve months."""
    a = F["accounts"]
    a = a[a["PremiseID"] == prem]
    m0 = A.pd.Period(first_month, "M").start_time.date()
    out = []
    for r in a.itertuples():
        e = r.EndDate if not A.pd.isna(r.EndDate) else P.SIM1
        if A.pd.isna(r.StartDate):
            continue
        if r.StartDate <= P.W1 and e >= max(m0, P.W0):
            out.append(int(r.AccountID))
    return out


def figures(R, F):
    mon = R["monthly"].set_index(["district", "month"])
    agg = R["agg"]
    div = R["diversion"]
    f = {}
    r1 = {lab: round(float(agg.loc[c, col]), 0) for c, col, lab in R1_CELLS}
    for c, m, col, lab in R1_MONTH:
        r1[lab] = round(float(mon.loc[(c, m), col]), 1)
    f["R1_basis"] = r1
    n = int(len(div)) if len(div) else 0
    accs = sorted({a for r in div.itertuples() for a in accounts_of(F, int(r.PremiseID), r.first_month)}) if n else []
    f["R2_unauthorized"] = {"premises": n, "accounts": len(accs)}
    f["R3_leak_pct"] = {P.DNAME[c]: round(float(agg.loc[c, "leak_pct"]), 2) for c in R3_DIST}
    f["R4_designated"] = names(R["designated"])
    f["R5_unauthorized_mcf"] = {"%s, Mcf" % P.DNAME[c]: round(float(div[div["district"] == c]["mcf_window"].sum())
                                                              if n else 0.0, 0) for c in R5_DIST}
    f["R6_changeout"] = names(R["changeout"])
    return f


BANDS = {
    "R1_basis": lambda k, v: (v * 0.985, v * 1.015) if "December" in k else (v * 0.997, v * 1.003),
    "R2_unauthorized": lambda k, v: (v - 1, v + 1),
    "R3_leak_pct": lambda k, v: (v - 0.10, v + 0.10),
    "R5_unauthorized_mcf": lambda k, v: (v * 0.75, v * 1.25),
}
PARTLY = {
    "R1_basis": lambda k, v: (v * 0.97, v * 1.03) if "December" in k else (v * 0.994, v * 1.006),
    "R2_unauthorized": lambda k, v: (v - 3, v + 3),
    "R3_leak_pct": lambda k, v: (v - 0.20, v + 0.20),
    "R5_unauthorized_mcf": lambda k, v: (v * 0.5, v * 1.5),
}
# id, name, figure, graded as, depends, independent input, precedent ids
META = [
    ("R1", "each district's gas in and its corrector customers on one real-gas basis at base conditions", "R1_basis",
     "Ask 1", [], "the regulator station correctors, the customer correctors and the city gate", ["L28"]),
    ("R2", "the premises where gas was taken without authorization, and their accounts", "R2_unauthorized",
     "Component 1", [], "each premise's reads against its own weather response a year earlier", ["L47", "N36"]),
    ("R3", "each district's leak loss in the twelve months to September 2026, per cent of its gas in", "R3_leak_pct",
     "Component 2", ["R1", "R2"], "", ["L47", "N36", "L28"]),
    ("R4", "the districts that enter the 2027-2029 main replacement program", "R4_designated", "Recommendation",
     ["R3"], "", ["L47", "N36", "L28"]),
    ("R5", "the gas taken without authorization, by district", "R5_unauthorized_mcf", "Ask 2", [],
     "each premise's reads against its own weather response a year earlier", ["L47", "N36"]),
    ("R6", "the districts where the 2027 meter changeout goes", "R6_changeout", "Recommendation 2", [],
     "the loggers, the soil station and the register", None),
]


def basis_table(F, cache):
    """Each station's recorded factor over the pressure-and-temperature factor, and each district's gas in and
    corrector customers in the twelve months, as recorded and on the real-gas basis."""
    _, med = A.pt_only_stations(F)
    st = F["stations"].set_index("Station")
    rec = A.stations_daily(F, "rebuild", "rec")
    gol = A.stations_daily(F, "rebuild", "dak")
    ev_r = A.evc_daily(F, "rec")[0]
    ev_g = A.evc_daily(F, "dak")[0]
    W = A.WIN
    rows = []
    for s in st.index:
        rows.append(dict(station=s, district=st.at[s, "PressureDistrict"], corrector=st.at[s, "Corrector"],
                         psig=int(st.at[s, "OutletPressurePsig"]), factor=round(float(med[s]), 5)))
    dist = {}
    for c in P.DCODES:
        dist[P.DNAME[c]] = dict(gas_in_recorded=round(float(rec[c][W].sum()), 0),
                                gas_in_real=round(float(gol[c][W].sum()), 0),
                                corrector_recorded=round(float(ev_r.get(c, np.zeros(A.ND))[W].sum()), 0),
                                corrector_real=round(float(ev_g.get(c, np.zeros(A.ND))[W].sum()), 0))
    return dict(stations=rows, districts=dist)


def run_all(F):
    cache = {}
    out = {k: A.run(F, o, cache) for k, o in ROUTES.items()}
    fam = [(n, A.run(F, o, cache)) for n, o in FAMILY]
    bat = [("supercompressibility %s, reads %s, gas temperature %s" % v, A.run(F, dict(z=v[0], cal=v[1], temp=v[2]),
                                                                         cache)) for v in BATTERY]
    det = [(n, A.run(F, o, cache)) for n, o in DETECTION]
    sc = [(n, A.run(F, o, cache)) for n, o in SHORTCUTS]
    pt = [(n, A.run(F, o, cache)) for n, o in PERTURB]
    hints = []
    for sent, o in HINTS:
        oo = dict(ROUTES["careful"])
        oo.update(o)
        hints.append((sent, A.run(F, oo, cache)))
    jud = []
    for jid, name, kind, prec, drop, fix in JUDGMENTS:
        d = A.run(F, drop, cache)
        a = None
        if fix is not None:
            oo = dict(ROUTES["careful"])
            oo.update(fix)
            a = A.run(F, oo, cache)
        jud.append((jid, name, kind, prec, d, a))
    return out, fam, bat, det, sc, pt, hints, jud, cache


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


def moved(G, f):
    return [rid for rid, _, fig, *_ in META if grade(fig, G[fig], f[fig]) != "right"]


def write(F, gen_out):
    out, fam, bat, det, sc, pt, hints, jud, cache = run_all(F)
    G = figures(out["golden"], F)
    Cf = figures(out["careful"], F)
    Qf = figures(out["quick"], F)
    res = []
    for rid, name, fig, graded, dep, indep, prec in META:
        g = G[fig]
        r = dict(id=rid, name=name, graded_as=graded, figure=fig, depends=dep, independent=indep, golden=g)
        if isinstance(g, dict):
            r["bands"] = {k: [round(x, 2) for x in BANDS[fig](k, v)] for k, v in g.items()}
            r["partly_share"] = 0.5
        r["passes"] = {"quick": Qf[fig], "careful": Cf[fig], "thorough": g}
        if prec:
            r["precedent"] = prec
        res.append(r)
    hint_rows = []
    for sent, R in hints:
        h = figures(R, F)
        resc = [rid for rid, _, fig, *_ in META if grade(fig, G[fig], h[fig]) == "right"
                and grade(fig, G[fig], Cf[fig]) != "right"]
        hint_rows.append(dict(sentence=sent, rescues=resc))
    routes = [dict(name="the golden", answer=G["R4_designated"], golden=True)]
    for n, R in sc:
        routes.append(dict(name=n, answer=names(R["designated"])))
    factorial = dict(golden_answer=G["R4_designated"], reflex_route=dict(answer=Cf["R4_designated"]), judgments=[])
    for jid, name, kind, prec, d, a in jud:
        fd = figures(d, F)
        row = dict(id=jid, name=name, kind=kind, precedent=prec,
                   dropped=dict(answer=fd["R4_designated"], results_moved=moved(G, fd)))
        if a is not None:
            fa = figures(a, F)
            row["alone"] = dict(answer=fa["R4_designated"],
                                results_rescued=[rid for rid, _, fig, *_ in META
                                                 if grade(fig, G[fig], fa[fig]) == "right"
                                                 and grade(fig, G[fig], Cf[fig]) != "right"])
        factorial["judgments"].append(row)
    forcing = dict(kind="set", line="leak loss over 1.0 per cent of the gas delivered into the district",
                   golden_answer=G["R4_designated"],
                   golden_family=[dict(name=n, answer=names(R["designated"])) for n, R in fam],
                   shortcuts=[dict(name=n, answer=names(R["designated"])) for n, R in sc],
                   perturbations=[dict(input=n, answer=names(R["designated"])) for n, R in pt])
    battery = dict(count=len(bat), answers=sorted({json.dumps(names(R["designated"])) for _, R in bat}),
                   changeout_answers=sorted({json.dumps(names(R["changeout"])) for _, R in bat}),
                   variants=[dict(name=n, answer=names(R["designated"]), changeout=names(R["changeout"]),
                                  leak={P.DNAME[c]: round(float(R["agg"].loc[c, "leak_pct"]), 3) for c in P.DCODES})
                             for n, R in bat],
                   detection=[dict(name=n, answer=names(R["designated"]),
                                   premises=int(len(R["diversion"])), changeout=names(R["changeout"])) for n, R in det])
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
                                   battery_leak=[round(float(R["agg"].loc[c, "leak_pct"]), 3) for _, R in bat],
                                   perturbed_leak=[round(float(R["agg"].loc[c, "leak_pct"]), 3) for _, R in pt])
    E = dict(results=res, hints=hint_rows, routes=routes, factorial=factorial, forcing=forcing, battery=battery,
             changeout_forcing=changeout_forcing, margins=margins,
             weights={"recommendation": 14, "components": 24, "asks": 55, "instruction": 7})
    G0 = out["golden"]
    dv = G0["diversion"]
    golden_set = set(dv["PremiseID"]) if len(dv) else set()
    extra = dict(golden_monthly=G0["monthly"].round(3).to_dict(orient="records"),
                 tpar={k: float(v) for k, v in G0["tpar"].items()},
                 careful_designated=names(out["careful"]["designated"]),
                 careful_changeout=names(out["careful"]["changeout"]),
                 shortcut_sets={n: names(R["designated"]) for n, R in sc},
                 shortcut_changeouts={n: names(R["changeout"]) for n, R in sc},
                 leak_table={n: {P.DNAME[c]: round(float(R["agg"].loc[c, "leak_pct"]), 2) for c in P.DCODES}
                             for n, R in [("golden", G0), ("careful", out["careful"])] + sc + fam},
                 ur_table={n: {P.DNAME[c]: round(float(R["agg"].loc[c, "ur_pct"]), 2) for c in P.DCODES}
                           for n, R in [("golden", G0), ("careful", out["careful"])] + sc + fam},
                 agg_golden={P.DNAME[c]: {k: round(float(G0["agg"].loc[c, k]), 1) for k in
                                          ("inflow", "billed", "under", "evc", "own", "dmg", "div", "leak")}
                             for c in P.DCODES},
                 agg_careful={P.DNAME[c]: {k: round(float(out["careful"]["agg"].loc[c, k]), 1) for k in
                                           ("inflow", "billed", "under", "evc", "own", "dmg", "div", "leak")}
                              for c in P.DCODES},
                 diversion_premises=[dict(r, accounts=accounts_of(F, int(r["PremiseID"]), r["first_month"]))
                                     for r in dv.to_dict(orient="records")],
                 careful_diversion_premises=int(len(out["careful"]["diversion"])),
                 basis=basis_table(F, cache),
                 pt_only_stations=A.pt_only_stations(F)[0],
                 station_factor={k: round(float(v), 5) for k, v in A.pt_only_stations(F)[1].items()},
                 p_atm=A.p_atm(F))
    # every fall in use the screen finds on the golden's own path, by what it was
    dg = A.run(F, dict(div="diag"), cache)["diversion"]
    nb = dg["kind"].ne("bypass")
    reb_ = dg["rebated"] & nb
    extra["collapses"] = dict(
        total=int(len(dg)),
        bypasses=int((~nb).sum()),
        furnace_taps=int((dg["kind"].eq("furnace tap") & ~dg["dual_fuel"] & ~reb_).sum()),
        absences=int((dg["kind"].eq("absence") & ~reb_).sum()),
        dual_fuel_test=int((dg["kind"].eq("furnace tap") & dg["dual_fuel"] & ~reb_).sum()),
        dual_fuel_rebated=int((reb_ & dg["kind"].ne("turnover")).sum()),
        turnover=int((dg["kind"].eq("turnover") & ~reb_).sum()))
    cc_ = extra["collapses"]
    cc_["dual_fuel"] = cc_["dual_fuel_test"] + cc_["dual_fuel_rebated"]
    assert cc_["bypasses"] + cc_["furnace_taps"] + cc_["absences"] + cc_["dual_fuel"] + cc_["turnover"] == cc_["total"]
    extra["falls_not_theft"] = dg[~dg["PremiseID"].isin(golden_set)].sort_values(["district", "PremiseID"]) \
        .to_dict(orient="records")
    extra["careful_booked_by_district"] = out["careful"]["diversion"].groupby("district").size().to_dict()
    extra["booked_every_fall_golden_path"] = int(len(A.run(F, dict(div="all"), cache)["diversion"]))
    figs = dict(G)
    figs["monthly_rows"] = int(len(G0["monthly"]))
    figs["rule1_line"] = P.LEAK_LINE
    figs["rule2_line"] = P.CHANGEOUT_LINE
    figs["rule2_min_meters"] = P.CHANGEOUT_MIN_METERS
    extra["bands_stated"] = dict(month_pct=1.5, year_pct=0.3, share_pts=0.10, count=1, mcf_pct=25)
    bdd = extra["basis"]["districts"]
    extra["basis_totals"] = dict(
        station_gap=round(sum(v["gas_in_real"] - v["gas_in_recorded"] for v in bdd.values()), 0),
        corrector_total=round(sum(v["corrector_real"] for v in bdd.values()), 0),
        corrector_gap=round(sum(v["corrector_real"] - v["corrector_recorded"] for v in bdd.values()), 0),
        ei_gap=round(bdd["East Industrial"]["corrector_real"] - bdd["East Industrial"]["corrector_recorded"], 0),
        ptz_factor_min=min(s["factor"] for s in extra["basis"]["stations"] if s["corrector"] == "EVC-II"),
        ptz_factor_max=max(s["factor"] for s in extra["basis"]["stations"] if s["corrector"] == "EVC-II"),
        pt_factor_mean=round(sum(s["factor"] for s in extra["basis"]["stations"] if s["corrector"] == "EVC-I") /
                             max(1, sum(1 for s in extra["basis"]["stations"] if s["corrector"] == "EVC-I")), 5))
    figs["_extra"] = extra
    json.dump(figs, open(os.path.join(gen_out, "figures.json"), "w"), indent=1, default=str)
    json.dump(E, open(os.path.join(gen_out, "effort.json"), "w"), indent=1, default=str)
    return figs, E, out, cache
