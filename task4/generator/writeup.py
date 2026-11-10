"""figures.json and submission.md, every figure emitted from analysis.py on the shipped pack (never typed)."""
import numpy as np

import analysis as A
import golden as GD

r10 = GD.r10


def figures(pk, g):
    a = g["assess"]
    R = {k: (m, lm, A.chosen(A.assess(pk, m, lim=lm))) for k, (m, lm) in A.routes(pk).items()}
    gp = A.payloads(pk, "shipper")
    car = A.assess(pk, R["careful but hurried"][0], lim=R["careful but hurried"][1])
    inp = g["inputs"]
    m = g["model"]
    rr = A.speed_ratio(pk)
    d0, d1 = m["dwell"]

    def hours(c):
        r = pk.routes[c]
        return sum(r["legs"]) / (A.plan_speed(pk, c) * rr) + d0 + d1 * (inp[c]["n_drops"] - 1)
    fridge = sorted(c for c in pk.short if inp[c]["epto"] == 1.0)
    dev = {k: {c: A.assess(pk, mm, lim=lm)[c]["kwh"] - a[c]["kwh"] for c in pk.short} for k, (mm, lm, _) in R.items()}
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
        "payload_term_last_drop": round(A.slope_per_100(R["the load to the last drop"][0]), 1),
        "payload_term_no_trailer": round(A.slope_per_100(R["no trailer weight"][0]), 1),
        "payload_term_careful": round(A.slope_per_100(R["careful but hurried"][0]), 1),
        "tare_term": round(g["tare_term"], 1),
        "loss_pct": round(100 * g["fade"], 1),
        "loss_pct_age_only": round(100 * A.fade(pk, "age"), 1),
        "usable_y1": int(round(g["usable_y1"])),
        "limit": int(round(g["limit"])),
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
        "pilot_speed_max": int(round(max(d["v"] for d in pk.days))),
        "fridge_set": fridge,
        "fridge_kw": round(g["tru_kw"], 1),
        "fridge_kwh": {c: int(round(g["tru_kw"] * hours(c))) for c in fridge},
        "fridge_kwh_each": int(round(np.mean([g["tru_kw"] * hours(c) for c in fridge]))),
        "fridge_hours": {c: round(hours(c), 1) for c in fridge},
        "reefer_not_drawing": sorted(c for c in pk.short if inp[c]["reefer"] == 1.0 and inp[c]["epto"] == 0.0),
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
        "dev_lo": {k: int(round(min(v.values()))) for k, v in dev.items()},
        "dev_hi": {k: int(round(max(v.values()))) for k, v in dev.items()},
        "dev": {k: {c: int(round(x)) for c, x in v.items()} for k, v in dev.items()},
        "rival_maxdev": int(np.ceil(max(abs(A.assess(pk, mm, lim=lm)[c]["kwh"] - a[c]["kwh"])
                                        for k, (mm, lm) in A.rivals(pk).items() if k != "within-duty fit"
                                        for c in pk.short))),
        "fe_slope": round(A.fe_slope_se(pk, gp)[0], 1),
        "fe_se": round(A.fe_slope_se(pk, gp)[1], 2),
        "golden_se": round(A.golden_se(pk, gp), 2),
        "margin_min": int(np.floor(min(abs(a[c]["kwh"] - g["limit"]) for c in a))),
        "conventions": {"fes_sections": [2.1, 2.2, 2.3, 4.1, 4.2, 4.3], "usable_quoted": 540, "share_pct": 85,
                        "per_km": 100, "capacity_ref_c": 20, "design_t": -5, "payload_band": [2.0, 2.4],
                        "loss_band": [3.6, 4.0], "energy_band": 10, "ratio_band": [0.75, 0.79], "kw": 400},
    }
    cal = A.calibration(pk)
    f["calibration_slope"] = {"%s %s" % k: round(v[1], 2) for k, v in sorted(cal.items())
                              if k[0] in {d["shipper"] for d in pk.days}}
    est = [v for k, v in f["calibration_slope"].items() if 0.0 < v < 0.9 and not k.startswith("BMJ")]
    f["clerk_slope_lo"], f["clerk_slope_hi"] = min(est), max(est)
    return f


def write(path, pk, g, f):
    E = f["energy"]
    go, no = f["call_set"], f["stay_diesel"]
    rs, rc = f["route_set"], f["route_count"]
    order = sorted(pk.short)
    ins = lambda k: sorted(set(rs[k]) - set(go))
    outs = lambda k: sorted(set(go) - set(rs[k]))
    flip = lambda k: ", ".join(["%s in" % x for x in ins(k)] + ["%s out" % x for x in outs(k)])
    cd = f["combination_and_drops"]
    L_lines = "\n".join("   - %s: design day %d kWh, %s" % (c, E[c], "electric" if c in go else "stays diesel")
                        for c in order)
    rng = lambda cs: "%d to %d kWh" % (min(E[c] for c in cs), max(E[c] for c in cs))
    car = "careful but hurried"
    cdev = f["dev"][car]
    fr = f["fridge_set"]
    txt = """## Tags

**Domain:** General Statistics & Data Science, Regression, classification & model diagnostics (fleet electrification, a road haulier's battery-electric duty assignment).
**Analytical objective:** Forecasting & Predictive Modeling.

## Final Recommendation

**Order {n} battery-electric tractors, for {goset}; {noset} stay on diesel.** The {n} need {gor} on the January design day against a limit of **{lim} kWh** (85 per cent of the {uy1} kWh a 540 kWh battery keeps after its first year), and the nearest diesel duty needs {nearno}; this rejects the {ccar} that a pilot model carried per km and per departing tonne, at the year's speed ratio and with the trailers never read, would order: it prices V03 and V11 at {c03} and {c11} kWh because it carries their loads to the last drop on a payload term of {pcar}, when their loads come off along the run.

## Supplementary Questions

### ev_duty_assessment_2027.xlsx
1. Sheet Assessment, one row per shortlisted duty in duty order, with shipper, delivery, the three legs and round trip km, climb, planning load, design-day energy (nearest 10 kWh; any figure within 10 kWh of the one below is acceptable), share of the first-year usable battery and whether it goes electric; below the rows the usable battery after the first year ({uy1} kWh), the limit ({lim} kWh), the tractors to order ({n}) and the duties.
{lines}
2. Sheet Energy model: the coefficients, with one tonne of payload adding **{pt} kWh per 100 loaded km** (any figure from 2.0 to 2.4 is acceptable), a tonne of combination tare {tt} kWh per 100 km on every leg, the ePTO fridge unit {kw} kW, and the cold-form comparison on January and February 2026 held out.
3. Sheet Payload calibration: each pilot shipper's weighed load against its declared weight on the Värnamo weighbridge, by note period, and the load each declaration is taken to.
4. Sheet Trailers and drops: each shortlisted duty's combination weight with the 2027 tractor, its trailers' refrigeration unit, its stops and the share of the loaded run its load rides.
5. Sheet Battery: the pilot batteries' first-year permanent loss, **{loss} per cent** (3.6 to 4.0 acceptable), the usable battery after the first year {uy1} kWh and the limit {lim} kWh.
6. Sheet Speed: each duty's routing-tool speed and its speed on a -5 C day ({rr} of it).
7. Sheet Routes: each shortcut's payload figure, loss, limit and order beside the assessment's.

### tractor_order_memo.pdf
8. One page to the management group: the order ({n} tractors, {goset}) first, the fourteen duties with design-day energy and verdict, the estimates that move the order (payload {pt} kWh per tonne per 100 km, the combination's weight on every leg, the drops, the ePTO fridge units, the {loss} per cent first-year loss, the duties' speed on a -5 C day) and what each shortcut would order instead.

## Critical Components

1. One tonne of payload adds **{pt} kWh per 100 loaded km** (2.0 to 2.4) once each pilot day's declared weight is taken to the weighed load it stands for, the load is taken off at each drop and the combination's tare is carried on every km (**{pdec}** on the declarations, {pld} with every load carried to the last drop, {pnt} with the trailer left out).
2. The pilot batteries lose **{loss} per cent** of their usable energy for good in their first year, so the 2027 tractor keeps **{uy1} kWh** and the limit is **{lim} kWh**.
3. Only the ePTO fridge units run from the tractor's battery, about **{kw} kW** from depot out to depot in: {frs} pull them and need about {fk} kWh each for it on the design day; {rnd}'s diesel units draw nothing.
4. On a -5 C day the pilot drove at **{rr}** of the routing tool's speed (**{ry}** over the year), so the Värnamo duties, planned at {pvl} to {pvh} km/h, run at {dvl} to {dvh} km/h.
5. With the 2027 tractor V02 and V14 haul double-deck combinations of **{c02}** and **{c14} t** against the pilot's **{pc} t** average, and V03's and V11's loads ride **{s03}** and **{s11}** of their loaded km.

## Step-by-Step

1. Cleaned bev_daily_summary_2025-03_2026-10.csv (a day uploaded twice kept once, ambient dropouts filled from the Jönköping station plus the mean offset) and joined tms_consignments_jonkoping_2025-2026.csv on registration and date, the day's notes summed: {days} pilot duty-days, each with its speed, the trailer it pulled, its drops and its hours from first departure to last arrival.
2. Planning loads from weighbridge_varnamo_2024-11_2026-10.csv per FES-2 4.2: the last weighing of each CMR, VMO-nn read as Vnn, gross less tare, November 2025 to October 2026.
3. Took each pilot day's declared weight to its expected weighed load at its shipper and note period, read from the Värnamo weighings (the clerks' weighed load rises {slo} to {shi} t per declared tonne); on the declarations a tonne costs {pdec}.
4. Joined each day's trailer to fleet_register_2026.xlsx (sheet Trailers) and the tractor's own tare: the pilot's combinations run {pclo} to {pchi} t, and a tonne of tare costs {tt} kWh per 100 km on every leg against the payload's {pt} on the loaded run. Each shortlisted duty's combination is the quotation's {t27} t tractor plus the mean tare of the trailers it pulled at Värnamo; left out, the pilot's average combination stands in for every duty and the order is {cnt} ({fnt}).
5. Took each note's weight off at its stop's km on route_register_2026.xlsx (sheet Stops), from the day's notes: the load rides {s03} of V03's loaded km and {s11} of V11's (tms_consignments_varnamo_2025-11_2026-10.csv). Carried to the last drop the payload term falls to {pld} and the order is {cld} ({fld}).
6. Read the trailers' Equipment codes: only the SR-60e ePTO unit runs from the tractor (AX-40 AGen has its own axle generator, SR-60 D and D+SB their own diesel). On the pilot's dairy duty the ePTO days draw **{kw} kW** more for as long as the duty is out; V24 and V30 pull ePTO units, {rnd} diesel ones. Without the fridge term the order is {cnf} ({fnf}); with every reefer drawing it is {car_} ({far}).
7. Chose the cold form out of sample (one rate below 16 C under-forecasts January and February 2026's sub-zero days by {bt1n} per cent; a further rate below 0 C {bt2}) and took the battery loss net of the cold: **{loss} per cent** ({lage} by age alone).
8. Added the square of the day's speed and set each duty's design-day speed from its routing-tool driving time times the pilot's actual-to-planned ratio at -5 C ({rr}). At the routing tool's speed the order is {cpl}; at the year's ratio ({ry}) {cmn} ({fmn}); with no speed term {cns} ({fns}).
9. Forecast each duty at -5 C, its planning load, its design-day speed, its combination, its drops and its fridge unit: {goset} at {gor}; {noset} at {nor}.
10. Order {n} tractors. Declared payloads order {cdec} ({fdec}), one cold rate {cone} ({fone}), no first-year loss {cnol} ({fnol}).

No other order survives: the declarations dilute the payload term, a combination's tare costs on every leg, a multi-drop load does not ride the whole loaded run, only the ePTO units draw on the battery, the one-rate cold form fails its own holdout, FES-2 2.3 charges the first year's loss, and a winter day runs slower than the routing tool's plan or the year's ratio. Every route that takes all the steps (knots at 14, 18, -2 or 2 C, a quadratic, temperature bins, the station's temperature, either year alone, the calibration on the last twelve months, each temperature-controlled loss fit, speed as a straight line, every form of the speed ratio, one coefficient for tare and payload, the fridge unit by driving hours or by km, the drops at equal shares) orders the same {n}, with every energy within {rmax} kWh of those above; a within-duty fit also orders the same {n}, but its payload slope ({fe}, standard error {fese} against {gse}) rests on the dairy duty alone.
""".format(
        n=f["call_count"], goset=", ".join(go), noset=", ".join(no), lim=f["limit"], uy1=f["usable_y1"],
        gor=rng(go), nor=rng(no), nearno="%d kWh" % min(E[c] for c in no), ccar=rc[car],
        c03=f["careful_energy"]["V03"], c11=f["careful_energy"]["V11"], pcar=f["payload_term_careful"],
        lines=L_lines, pt=f["payload_term"], tt=f["tare_term"], kw=f["fridge_kw"], loss=f["loss_pct"],
        rr=f["speed_ratio_design"], ry=f["speed_ratio_year"], pdec=f["payload_term_declared"],
        pld=f["payload_term_last_drop"], pnt=f["payload_term_no_trailer"], frs=" and ".join(fr),
        fk=int(round(np.mean([f["fridge_kwh"][c] for c in fr]))), rnd=", ".join(f["reefer_not_drawing"]),
        pvl=f["plan_speed_lo"], pvh=f["plan_speed_hi"], dvl=f["design_speed_lo"], dvh=f["design_speed_hi"],
        c02=cd["V02 combination t"], c14=cd["V14 combination t"], pc=f["pilot_combination_t"],
        s03="%.2f" % cd["V03 load share"], s11="%.2f" % cd["V11 load share"], days=f["duty_days"], slo=f["clerk_slope_lo"],
        shi=f["clerk_slope_hi"], pclo=f["pilot_combination_lo"], pchi=f["pilot_combination_hi"],
        t27=f["tractor_2027_t"], cnt=rc["no trailer weight"], fnt=flip("no trailer weight"),
        cld=rc["the load to the last drop"], fld=flip("the load to the last drop"), cnf=rc["no fridge draw"],
        fnf=flip("no fridge draw"), car_=rc["every reefer draws"], far=flip("every reefer draws"),
        bt1n=f["backtest_one_rate_abs"], bt2="%+.1f" % f["backtest_two_rates"], lage=f["loss_pct_age_only"],
        cpl=rc["the routing tool's speed"], cmn=rc["the year's mean speed ratio"],
        fmn=flip("the year's mean speed ratio"), cns=rc["no speed term"], fns=flip("no speed term"),
        cdec=rc["declared weights"], fdec=flip("declared weights"), cone=rc["one cold rate"],
        fone=flip("one cold rate"), cnol=rc["no first-year loss"], fnol=flip("no first-year loss"),
        rmax=f["rival_maxdev"], fe=f["fe_slope"], fese=f["fe_se"], gse=f["golden_se"])
    open(path, "w", encoding="utf-8").write(txt)
