"""figures.json and submission.md, every figure emitted from analysis.py on the shipped pack (never typed)."""
import numpy as np

import analysis as A
import golden as GD

r10 = GD.r10


def lane_table(pk):
    """each pilot duty: its mean declared weight before any scale period, its shipper's mean declared weight at the
    terminal, and the mean load the terminal's line and the duty's own declarations put on it"""
    from collections import defaultdict
    gp, cp = A.payloads(pk, "lane"), A.careful_payloads(pk)
    tv = defaultdict(list)
    for r in pk.wb:
        if r["declared"] is not None and A.regime(pk, r["shipper"], r["date"]) != "ticket":
            tv[r["shipper"]].append(r["declared"])
    out = {}
    for du in sorted({d["duty"] for d in pk.days}):
        m = np.array([d["duty"] == du and A.regime(pk, d["shipper"], d["date"]) != "ticket" for d in pk.days])
        s = pk.routes[du]["shipper"]
        dec = float(np.mean([d["declared"] for d, k in zip(pk.days, m) if k])) / 1000
        out[du] = {"shipper": s, "declared": round(dec, 2), "terminal_declared": round(float(np.mean(tv[s])) / 1000, 2),
                   "share": round(dec / (float(np.mean(tv[s])) / 1000), 2), "lane": round(float(gp[m].mean()), 2),
                   "terminal_line": round(float(cp[m].mean()), 2)}
    return out


def scale_check(pk):
    """the drinks maker's duties: the weighed loads on its notes once its dock scale wrote them, against the loads
    the terminal's line and the duty's own declarations put on the same duty before"""
    gp, cp = A.payloads(pk, "lane"), A.careful_payloads(pk)
    out = {}
    for du in ("J07", "J08"):
        mt = np.array([d["duty"] == du and A.regime(pk, d["shipper"], d["date"]) == "ticket" for d in pk.days])
        mn = np.array([d["duty"] == du and A.regime(pk, d["shipper"], d["date"]) == "note" for d in pk.days])
        out[du] = {"scale_days": int(mt.sum()), "scale_mean": round(float(gp[mt].mean()), 1),
                   "terminal_line_before": round(float(cp[mn].mean()), 1), "own_before": round(float(gp[mn].mean()), 1)}
    return out


def figures(pk, g):
    a = g["assess"]
    R = {k: (m, lm, A.chosen(A.assess(pk, m, lim=lm))) for k, (m, lm) in A.routes(pk).items()}
    gp = A.payloads(pk, "lane")
    car = A.assess(pk, R["careful but hurried"][0], lim=R["careful but hurried"][1])
    inp = g["inputs"]
    m = g["model"]
    rr = A.speed_ratio(pk)
    dev = {k: {c: A.assess(pk, mm, lim=lm)[c]["kwh"] - a[c]["kwh"] for c in pk.short} for k, (mm, lm, _) in R.items()}
    lt = lane_table(pk)
    sc = scale_check(pk)
    RV = A.rivals(pk)
    loss_forms = {h: round(100 * A.fade(pk, h), 1) for h in A.LOSS_RIVALS + ("first_year",)}
    f = {
        "call_count": g["count"],
        "call_set": g["set"],
        "stay_diesel": sorted(c for c in pk.short if not a[c]["go"]),
        "energy": {c: r10(a[c]["kwh"]) for c in sorted(a)},
        "energy_raw": {c: round(a[c]["kwh"], 1) for c in sorted(a)},
        "planning_load": {c: round(A.planning_load(pk, c), 1) for c in sorted(pk.short)},
        "verdict": {c: "yes" if a[c]["go"] else "no" for c in sorted(a)},
        "payload_term": round(A.slope_per_100(m), 1),
        "payload_term_declared": round(A.slope_per_100(R["declared weights"][0]), 1),
        "payload_term_careful": round(A.slope_per_100(R["careful but hurried"][0]), 1),
        "payload_term_fe": round(A.fe_slope_se(pk, gp)[0], 1),
        "payload_term_fe_se": round(A.fe_slope_se(pk, gp)[1], 2),
        "payload_term_fe_careful": round(A.fe_slope_se(pk, A.careful_payloads(pk))[0], 1),
        "payload_term_add": round(A.slope_per_100(RV["loads: additive declaration error"][0]), 1),
        "lane": lt,
        "lane_share_lo": min(v["share"] for v in lt.values()),
        "lane_share_hi": max(v["share"] for v in lt.values()),
        "lane_share_lo_pct": int(round(100 * min(v["share"] for v in lt.values()))),
        "lane_share_hi_pct": int(round(100 * max(v["share"] for v in lt.values()))),
        "lane_gap_lo": round(min(v["terminal_line"] - v["lane"] for v in lt.values()), 1),
        "lane_gap_hi": round(max(v["terminal_line"] - v["lane"] for v in lt.values()), 1),
        "scale_check": sc,
        "tare_term": round(g["tare_term"], 1),
        "loss_pct": round(100 * g["fade"], 1),
        "loss_tau_months": int(round(12 * g["tau"])),
        "loss_pct_line": round(100 * A.careful_fade(pk), 1),
        "loss_pct_yoy": round(100 * A.fade(pk, "yoy"), 1),
        "loss_pct_age_only": round(100 * A.fade(pk, "age"), 1),
        "loss_forms": loss_forms,
        "loss_form_lo": min(loss_forms.values()),
        "loss_form_hi": max(loss_forms.values()),
        "usable_y1": int(round(g["usable_y1"])),
        "limit": int(round(g["limit"])),
        "limit_careful": int(round(R["careful but hurried"][1])),
        "backtest_one_rate": round(A.backtest(pk, gp, A.H1)[0], 1),
        "backtest_two_rates": round(A.backtest(pk, gp, A.H2)[0], 1),
        "backtest_one_rate_abs": abs(round(A.backtest(pk, gp, A.H1)[0], 1)),
        "duty_days": len(pk.days),
        "route_count": {k: len(v[2]) for k, v in R.items()},
        "route_set": {k: v[2] for k, v in R.items()},
        "careful_count": len(R["careful but hurried"][2]),
        "careful_energy": {c: r10(car[c]["kwh"]) for c in sorted(car)},
        "rmse_pct": round(m["rmse_pct"], 2),
        "speed_ratio_design": round(rr, 2),
        "speed_ratio_year": round(A.speed_ratio(pk, how="mean"), 2),
        "plan_speed_lo": int(round(min(A.plan_speed(pk, c) for c in pk.short))),
        "plan_speed_hi": int(round(max(A.plan_speed(pk, c) for c in pk.short))),
        "design_speed_lo": int(round(min(A.plan_speed(pk, c) for c in pk.short) * rr)),
        "design_speed_hi": int(round(max(A.plan_speed(pk, c) for c in pk.short) * rr)),
        "combination_t": {c: round(inp[c]["combo"], 1) for c in sorted(pk.short)},
        "pilot_combination_t": round(g["pilot_combo"], 1),
        "pilot_combination_lo": round(min(d["combo"] for d in pk.days), 1),
        "pilot_combination_hi": round(max(d["combo"] for d in pk.days), 1),
        "load_share": {c: round(inp[c]["phi"], 2) for c in sorted(pk.short) if inp[c]["n_drops"] > 1},
        "combination_and_drops": {"V02 combination t": round(inp["V02"]["combo"], 1),
                                  "V14 combination t": round(inp["V14"]["combo"], 1),
                                  "V03 load share": round(inp["V03"]["phi"], 2),
                                  "V11 load share": round(inp["V11"]["phi"], 2)},
        "tractor_2027_t": round(A.TRACTOR_2027_KG / 1000, 2),
        "dev": {k: {c: int(round(x)) for c, x in v.items()} for k, v in dev.items()},
        "rival_maxdev": int(np.ceil(max(abs(A.assess(pk, mm, lim=lm)[c]["kwh"] - a[c]["kwh"])
                                        for k, (mm, lm) in RV.items() for c in pk.short))),
        "golden_se": round(A.golden_se(pk, gp), 2),
        "margin_min": int(np.floor(min(abs(a[c]["kwh"] - g["limit"]) for c in a))),
        "conventions": {"fes_sections": [2.1, 2.2, 2.3, 4.1, 4.2, 4.3], "usable_quoted": 540, "share_pct": 85,
                        "per_km": 100, "capacity_ref_c": 20, "design_t": -5, "payload_band": list(PAY_BAND),
                        "loss_band": list(LOSS_BAND), "energy_band": 10, "ratio_band": list(RATIO_BAND)},
    }
    return f


PAY_BAND = (1.7, 2.4)
LOSS_BAND = (4.2, 5.6)
RATIO_BAND = (0.74, 0.79)


def write(path, pk, g, f):
    E = f["energy"]
    go, no = f["call_set"], f["stay_diesel"]
    rs, rc = f["route_set"], f["route_count"]
    order = sorted(pk.short)
    ins = lambda k: sorted(set(rs[k]) - set(go))
    outs = lambda k: sorted(set(go) - set(rs[k]))
    flip = lambda k: ", ".join(["%s in" % x for x in ins(k)] + ["%s out" % x for x in outs(k)]) or "no duty moves"
    cd = f["combination_and_drops"]
    L_lines = "\n".join("   - %s: design day %d kWh, %s" % (c, E[c], "electric" if c in go else "stays diesel")
                        for c in order)
    rng = lambda cs: "%d to %d kWh" % (min(E[c] for c in cs), max(E[c] for c in cs))
    car, carw = "careful but hurried", "careful, design-day speed"
    ce = f["careful_energy"]
    lt, sc = f["lane"], f["scale_check"]
    lf = f["loss_forms"]
    and_ = lambda xs: ", ".join(xs[:-1]) + " and " + xs[-1] if len(xs) > 1 else xs[0]
    txt = """## Tags

**Domain:** General Statistics & Data Science, Regression, classification & model diagnostics (fleet electrification, a road haulier's battery-electric duty assignment).
**Analytical objective:** Forecasting & Predictive Modeling.

## Final Recommendation

**Order {n} battery-electric tractors, for {goset}; {noset} stay on diesel.** The {n} need {gor} on the January design day against a limit of **{lim} kWh** (85 per cent of the {uy1} kWh a 540 kWh battery keeps after a first-year loss of {loss} per cent), and the nearest diesel duty needs {nearno}. This rejects the {ccar} ({ccarset}) that a pilot model built on the terminal's calibration line, a straight-line battery loss and the year's speed ratio would order: it prices {carout} at {carout_e} kWh against its own {limc} kWh limit. It also rejects the {ccw} that the same model orders at the design-day speed, which lets in {cwin} on a payload term of {pcar}.

## Supplementary Questions

### ev_duty_assessment_2027.xlsx
1. Sheet Assessment, one row per shortlisted duty in duty order, with shipper, delivery, the three legs and round trip km, climb, planning load, design-day energy (nearest 10 kWh; any figure within 10 kWh of the one below is acceptable), share of the first-year usable battery and whether it goes electric; below the rows the usable battery after the first year ({uy1} kWh), the limit ({lim} kWh), the tractors to order ({n}) and the duties.
{lines}
2. Sheet Energy model: the coefficients, with one tonne of payload adding **{pt} kWh per 100 loaded km** (any figure from {pb0} to {pb1} is acceptable), a tonne of combination tare {tt} kWh per 100 km on every leg, and the cold-form comparison on January and February 2026 held out.
3. Sheet Payloads: each pilot duty's mean declared weight against its shipper's at the terminal, the error each shipper's notes carry on the Värnamo weighbridge, and the load each duty's declarations are taken to; beside it the drinks maker's scale-weighed days.
4. Sheet Trailers and drops: each shortlisted duty's combination weight with the 2027 tractor, its stops and the share of the loaded run its load rides.
5. Sheet Battery: the pilot batteries' first-year permanent loss, **{loss} per cent** (any figure from {lb0} to {lb1} is acceptable), the usable battery after the first year {uy1} kWh, the limit {lim} kWh, and the loss under each age form.
6. Sheet Speed: each duty's routing-tool speed and its speed on a -5 C day.
7. Sheet Routes: each shortcut's payload figure, loss, limit and order beside the assessment's.

### tractor_order_memo.pdf
8. One page to the management group: the order ({n} tractors, {goset}) first, the fourteen duties with design-day energy and verdict, the estimates that move the order (payload {pt} kWh per tonne per 100 loaded km, the {loss} per cent first-year loss and the {lim} kWh limit, the duties' speed on a -5 C day) and what each shortcut would order instead.

## Critical Components

1. One tonne of payload adds **{pt} kWh per 100 loaded km** ({pb0} to {pb1}). The pilot's regional duties carry {shlo} to {shhi} of the loads their shippers declare at the terminal, so the terminal's weighed-on-declared line, which pulls a clerk's estimate toward the terminal's loads, puts each pilot duty {glo} to {ghi} t too heavy and the term at **{pcar}**; taking each duty's loads from its own declarations, with the error each shipper's notes carry on the weighbridge removed, gives {pt}, the within-duty fit {pfe} (the same fit on the terminal's line {pfec}), and the drinks maker's own notes confirm it: from August 2026 its declarations equal the weighbridge's net load to the bridge's 20 kg, and on J07 and J08 they average {s7} and {s8} t, against {o7} and {o8} t from the duties' own earlier declarations and {t7} and {t8} t on the line.
2. The pilot batteries lose **{loss} per cent** of their usable energy for good in their first year: most of it in the first months, settling over about {taum} months, then a steady loss. A straight line in age puts it at {lline} per cent and the same months a year apart at {lyoy}, both blind to the early loss; every curved form lands from {lflo} to {lfhi}. The 2027 tractor keeps **{uy1} kWh** and the limit is **{lim} kWh**, not {limc}.

## Step-by-Step

1. Cleaned bev_daily_summary_2025-03_2026-10.csv (a day uploaded twice kept once, ambient dropouts filled from the Jönköping station plus the mean offset) and joined tms_consignments_jonkoping_2025-2026.csv on registration and date, the day's notes summed: {days} pilot duty-days, each with its speed, the trailer it pulled and its drops.
2. Planning loads from weighbridge_varnamo_2024-11_2026-10.csv per FES-2 4.2: the last weighing of each CMR, VMO-nn read as Vnn, gross less tare, November 2025 to October 2026.
3. Compared each pilot duty's declarations with its shipper's at the terminal: the pilot's regional duties run at {shlo} to {shhi} of the terminal's loads. The clerks' estimates scatter widely around the weighed load, so the terminal's weighed-on-declared line pulls every declaration toward the terminal's loads and does not carry to the pilot. Read each shipper's declaration error on the weighbridge at each note period, removed it from the spread of each pilot duty's own declared weights, and took each declaration to its expected load on that duty. On the terminal's line the payload term is {pcar}, on the raw declarations {pdec}, on the duties' own loads **{pt}** (with the error additive, {padd}; within duty, {pfe}). The drinks maker's notes settle it: from August 2026 they carry the weighed load (they equal the weighbridge's net to its 20 kg), and on J07 and J08 they average {s7} and {s8} t, against {o7} and {o8} t from the same duties' earlier declarations and {t7} and {t8} t on the terminal's line.
4. Joined each day's trailer to fleet_register_2026.xlsx (sheet Trailers) and the tractor's own tare: the pilot's combinations run {pclo} to {pchi} t, and a tonne of tare costs {tt} kWh per 100 km on every leg. Each shortlisted duty's combination is the quotation's {t27} t tractor plus the mean tare of the trailers it pulled at Värnamo (V02 and V14's double decks {c02} and {c14} t, against the pilot's {pc} t average); left out, the order is {cnt} ({fnt}).
5. Took each note's weight off at its stop's km on route_register_2026.xlsx (sheet Stops): the load rides {s03} of V03's loaded km and {s11} of V11's (tms_consignments_varnamo_2025-11_2026-10.csv). Carried to the last drop, the order is {cld} ({fld}).
6. Chose the cold form out of sample (one rate below 16 C under-forecasts January and February 2026's sub-zero days by {bt1n} per cent; a further rate below 0 C {bt2}).
7. Fitted each day's energy per full charge on a level per tractor, the day's degrees below 20 C and an age form with an early-life loss that settles over a time scale the fit chooses (about {taum} months) and a steady loss: **{loss} per cent** in the first twelve months. A straight line in age fits far worse and gives {lline}; the same months a year apart compare ages a year on from the first months and give {lyoy}; every curved form gives {lflo} to {lfhi}. A straight-line loss alone orders {cline} ({fline}).
8. Added the square of the day's speed and set each duty's design-day speed from its routing-tool driving time times the pilot's actual-to-planned ratio at -5 C ({rr}), so the Värnamo duties, planned at {pvl} to {pvh} km/h, run at {dvl} to {dvh} km/h. At the year's ratio ({ry}) the order is {cmn} ({fmn}); at the routing tool's speed {cpl}; with no speed term {cns} ({fns}).
9. Forecast each duty at -5 C, its planning load, its design-day speed, its combination and its drops: {goset} at {gor}; {noset} at {nor}.
10. Order {n} tractors. The terminal's calibration line alone orders {ccl} ({fcl}); with the straight-line loss and the year's ratio as well, {ccar} ({fcar}); with that line and loss at the design-day speed, {ccw} ({fcw}). Declared payloads order {cdec} ({fdec}), one cold rate {cone} ({fone}), no first-year loss {cnol} ({fnol}).

No other order survives: the terminal's line does not carry to the pilot's own loads, the batteries lose most of their first year's capacity early, a winter day runs slower than the routing tool's plan or the year's ratio, a combination's tare costs on every leg and a multi-drop load does not ride the whole run. Each of the three estimates alone, put right inside the careful model, still orders wrongly ({h1} with the duties' own loads, {h2} with the curved loss, {h3} at the design-day speed). Every route that takes all the steps (knots at 14, 18, -2 or 2 C, a quadratic, temperature bins, the station's temperature, either year alone, the declaration error additive or read on the last twelve months, each day at its duty's mean declaration, the within-duty fit, every curved loss form and cold term, speed as a straight line, every form of the speed ratio, one coefficient for tare and payload, the drops at equal shares) orders the same {n}, with every energy within {rmax} kWh of those above.
""".format(
        n=f["call_count"], goset=", ".join(go), noset=", ".join(no), lim=f["limit"], uy1=f["usable_y1"],
        loss=f["loss_pct"], gor=rng(go), nor=rng(no), nearno="%d kWh" % min(E[c] for c in no),
        ccar=rc[car], ccarset=", ".join(rs[car]), carout=and_(outs(car)),
        carout_e=and_(["%d" % ce[c] for c in outs(car)]), limc=f["limit_careful"], ccw=rc[carw],
        cwin=and_(ins(carw)), pcar=f["payload_term_careful"], lines=L_lines, pt=f["payload_term"],
        pb0=f["conventions"]["payload_band"][0], pb1=f["conventions"]["payload_band"][1], tt=f["tare_term"],
        lb0=f["conventions"]["loss_band"][0], lb1=f["conventions"]["loss_band"][1], rr=f["speed_ratio_design"],
        ry=f["speed_ratio_year"], shlo=f["lane_share_lo_pct"], shhi="%d per cent" % f["lane_share_hi_pct"], glo=f["lane_gap_lo"], ghi=f["lane_gap_hi"],
        pfe=f["payload_term_fe"], pfec=f["payload_term_fe_careful"], pdec=f["payload_term_declared"],
        padd=f["payload_term_add"], s7=sc["J07"]["scale_mean"], s8=sc["J08"]["scale_mean"],
        o7=sc["J07"]["own_before"], o8=sc["J08"]["own_before"], t7=sc["J07"]["terminal_line_before"],
        t8=sc["J08"]["terminal_line_before"], taum=f["loss_tau_months"], lline=f["loss_pct_line"],
        lyoy=f["loss_pct_yoy"], lflo=f["loss_form_lo"], lfhi=f["loss_form_hi"],
        pvl=f["plan_speed_lo"], pvh=f["plan_speed_hi"], dvl=f["design_speed_lo"], dvh=f["design_speed_hi"],
        c02=cd["V02 combination t"], c14=cd["V14 combination t"], pc=f["pilot_combination_t"],
        s03="%.2f" % cd["V03 load share"], s11="%.2f" % cd["V11 load share"], days=f["duty_days"],
        pclo=f["pilot_combination_lo"], pchi=f["pilot_combination_hi"], t27=f["tractor_2027_t"],
        cnt=rc["no trailer weight"], fnt=flip("no trailer weight"), cld=rc["the load to the last drop"],
        fld=flip("the load to the last drop"), bt1n=f["backtest_one_rate_abs"], bt2="%+.1f" % f["backtest_two_rates"],
        cline=rc["a straight-line loss"], fline=flip("a straight-line loss"),
        cmn=rc["the year's mean speed ratio"], fmn=flip("the year's mean speed ratio"),
        cpl=rc["the routing tool's speed"], cns=rc["no speed term"], fns=flip("no speed term"),
        ccl=rc["the terminal's calibration line"], fcl=flip("the terminal's calibration line"),
        fcar=flip(car), fcw=flip(carw), cdec=rc["declared weights"], fdec=flip("declared weights"),
        cone=rc["one cold rate"], fone=flip("one cold rate"), cnol=rc["no first-year loss"],
        fnol=flip("no first-year loss"), h1=rc["careful, own-duty loads"], h2=rc["careful, curved loss"], h3=rc[carw],
        rmax=f["rival_maxdev"])
    open(path, "w", encoding="utf-8").write(txt)
