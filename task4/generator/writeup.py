"""figures.json and submission.md, every figure emitted from analysis.py on the shipped pack (never typed)."""
import numpy as np

import analysis as A
import golden as GD

r10 = GD.r10


def figures(pk, g):
    a = g["assess"]
    R = {k: (m, lm, A.chosen(A.assess(pk, m, lim=lm))) for k, (m, lm) in A.routes(pk).items()}
    gp = A.payloads(pk, "shipper")
    car = A.assess(pk, *R["careful but hurried"][:1], lim=R["careful but hurried"][1])
    f = {
        "call_count": g["count"],
        "call_set": g["set"],
        "stay_diesel": sorted(c for c in pk.short if not a[c]["go"]),
        "energy": {c: r10(a[c]["kwh"]) for c in sorted(a)},
        "energy_raw": {c: round(a[c]["kwh"], 1) for c in sorted(a)},
        "planning_load": {c: round(A.planning_load(pk, c), 1) for c in sorted(pk.short)},
        "verdict": {c: "yes" if a[c]["go"] else "no" for c in sorted(a)},
        "payload_term": round(A.slope_per_100(g["model"]), 1),
        "payload_term_declared": round(A.slope_per_100(R["declared weights"][0]), 1),
        "payload_term_pooled": round(A.slope_per_100(R["one pooled correction"][0]), 1),
        "payload_term_pilot_line": round(A.slope_per_100(R["one line over the pilot shippers"][0]), 1),
        "loss_pct": round(100 * g["fade"], 1),
        "loss_pct_age_only": round(100 * A.fade(pk, "age"), 1),
        "loss_pct_yoy": round(100 * A.fade(pk, "yoy"), 1),
        "usable_y1": int(round(g["usable_y1"])),
        "limit": int(round(g["limit"])),
        "limit_no_loss": 459,
        "backtest_one_rate": round(A.backtest(pk, gp, A.H1)[0], 1),
        "backtest_two_rates": round(A.backtest(pk, gp, A.H2)[0], 1),
        "duty_days": len(pk.days),
        "route_count": {k: len(v[2]) for k, v in R.items()},
        "route_set": {k: v[2] for k, v in R.items()},
        "careful_count": len(R["careful but hurried"][2]),
        "careful_energy": {c: r10(car[c]["kwh"]) for c in sorted(car)},
        "rmse_pct": round(g["model"]["rmse_pct"], 2),
        "rmse_nospeed_pct": round(R["no speed term"][0]["rmse_pct"], 2),
        "backtest_one_rate_abs": abs(round(A.backtest(pk, gp, A.H1)[0], 1)),
        "speed_ratio_design": round(A.speed_ratio(pk), 2),
        "speed_ratio_year": round(A.speed_ratio(pk, how="mean"), 2),
        "speed_kwh_per_10kmh": round(100 * g["model"]["coef"][4] * (2 * 68 * 10 + 100) / 1000, 1),
        "plan_speed": {c: int(round(A.plan_speed(pk, c))) for c in sorted(pk.short)},
        "design_speed": {c: int(round(A.plan_speed(pk, c) * A.speed_ratio(pk))) for c in sorted(pk.short)},
        "plan_speed_lo": int(round(min(A.plan_speed(pk, c) for c in pk.short))),
        "plan_speed_hi": int(round(max(A.plan_speed(pk, c) for c in pk.short))),
        "design_speed_lo": int(round(min(A.plan_speed(pk, c) for c in pk.short) * A.speed_ratio(pk))),
        "design_speed_hi": int(round(max(A.plan_speed(pk, c) for c in pk.short) * A.speed_ratio(pk))),
        "pilot_speed_max": int(round(max(d["v"] for d in pk.days))),
        "nospeed_shift_lo": int(round(min(g["assess"][c]["kwh"] - A.assess(pk, *[R["no speed term"][0]],
                                                                          lim=R["no speed term"][1])[c]["kwh"]
                                          for c in pk.short))),
        "nospeed_shift_hi": int(round(max(g["assess"][c]["kwh"] - A.assess(pk, *[R["no speed term"][0]],
                                                                          lim=R["no speed term"][1])[c]["kwh"]
                                          for c in pk.short))),
        "rival_maxdev": int(np.ceil(max(abs(A.assess(pk, m, lim=lm)[c]["kwh"] - g["assess"][c]["kwh"])
                                        for k, (m, lm) in A.rivals(pk).items() for c in pk.short))),
        # conventions the blocks cite: FES-2 sections, the quoted battery and share, the per-100-km unit, and the
        # capacity model's reference temperature
        "conventions": {"fes_sections": [2.3, 4.1, 4.2, 4.3], "usable_quoted": 540, "share_pct": 85,
                        "per_km": 100, "capacity_ref_c": 20, "pallet_kg": 540, "design_t": -5, "speed_step_kmh": 10, "payload_band": [1.9, 2.1], "loss_band": [3.6, 4.0]},
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
    nsp_extra = sorted(set(rs["no speed term"]) - set(go))
    pln_out = sorted(set(go) - set(rs["the routing tool's speed"]))
    mean_out = sorted(set(go) - set(rs["the year's mean speed ratio"]))
    dec_extra = sorted(set(rs["declared weights"]) - set(go))
    nol_extra = sorted(set(rs["no first-year loss"]) - set(go))
    L_lines = "\n".join("   - %s: design day %d kWh, %s" % (c, E[c], "electric" if c in go else "stays diesel")
                        for c in order)
    rng = lambda cs: "%d to %d kWh" % (min(E[c] for c in cs), max(E[c] for c in cs))
    near = nsp_extra
    rest = [c for c in no if c not in near]
    txt = """## Tags

**Domain:** General Statistics & Data Science, Regression, classification & model diagnostics (fleet electrification, a road haulier's battery-electric duty assignment).
**Analytical objective:** Forecasting & Predictive Modeling.

## Final Recommendation

**Order {n} battery-electric tractors, for {goset}; {noset} stay on diesel.** {near} need {nearr} on the January design day against a limit of **{lim} kWh** (85 per cent of the {uy1} kWh a 540 kWh battery keeps after its first year); the {cnsp} tractors a forecast in proportion to distance orders, even with the payloads, the cold and the battery loss right, prices the Värnamo duties at the pilot's slower speeds, {sl} to {sh} kWh too low.

## Supplementary Questions

### ev_duty_assessment_2027.xlsx
1. Sheet Assessment, one row per shortlisted duty in duty order, with shipper, delivery, the three legs and round trip km, climb, planning load, design-day energy (nearest 10 kWh; any figure within 10 kWh of the one below is acceptable), share of the first-year usable battery and whether it goes electric; below the rows the usable battery after the first year ({uy1} kWh), the limit ({lim} kWh), the tractors to order ({n}) and the duties.
{lines}
2. Sheet Energy model: the coefficients, with one tonne of payload adding **{pt} kWh per 100 loaded km** (any figure from 1.9 to 2.1 is acceptable), and the cold-form comparison on January and February 2026 held out.
3. Sheet Payload calibration: each pilot shipper's weighed load against its declared weight on the Värnamo weighbridge, by note period, and the load each declaration is taken to.
4. Sheet Battery: the pilot batteries' first-year permanent loss, **{loss} per cent** (3.6 to 4.0 acceptable), the usable battery after the first year {uy1} kWh and the limit {lim} kWh.
5. Sheet Speed: each duty's routing-tool speed and its speed on a -5 C day ({rr} of it).
6. Sheet Routes: each shortcut's payload figure, loss, limit and order beside the assessment's.

### tractor_order_memo.pdf
7. One page to the management group: the order ({n} tractors, {goset}) first, the fourteen duties with design-day energy and verdict, the four estimates that move the order (payload {pt} kWh per tonne per 100 km, the two-rate cold form, the {loss} per cent first-year loss, the duties' speed on a -5 C day) and what each shortcut would order instead.

## Critical Components

1. The Värnamo duties run at {pvl} to {pvh} km/h on the routing tool against at most {pmax} km/h on any pilot day; at the pilot's actual-to-planned ratio on a -5 C day ({rr}, against {ry} over the year) they drive at {dvl} to {dvh} km/h, and each 10 km/h there costs about **{p10} kWh per 100 km**.
2. One tonne of payload adds **{pt} kWh per 100 loaded km** (1.9 to 2.1) once each pilot day's declared weight is taken to the weighed load it stands for, shipper by shipper (**{pdec}** on the declarations).
3. The pilot batteries lose **{loss} per cent** of their usable energy for good in their first year, so the 2027 tractor keeps **{uy1} kWh** and the limit is **{lim} kWh**.
4. On the January design day {near} need **{nearr}** and V14 needs **{v14} kWh**.

## Step-by-Step

1. Cleaned bev_daily_summary_2025-03_2026-10.csv (a day uploaded twice kept once, ambient dropouts filled from the Jönköping station plus the mean offset) and joined tms_consignments_jonkoping_2025-2026.csv on registration and date: {days} pilot duty-days, each with its average speed (distance over driving time).
2. Planning loads from weighbridge_varnamo_2024-11_2026-10.csv per FES-2 4.2: the last weighing of each CMR, VMO-nn read as Vnn, gross less tare, November 2025 to October 2026.
3. Took each pilot day's declared weight to its expected weighed load at its shipper and note period, read from the Värnamo weighings (the clerks' weighed load rises {slo} to {shi} t per declared tonne): **{pt}** kWh per tonne per 100 km against {pdec} on the declarations.
4. Chose the cold form out of sample (one rate below 16 C under-forecasts January and February 2026's sub-zero days by {bt1n} per cent; a further rate below 0 C {bt2}) and took the battery loss net of the cold: **{loss} per cent** ({lage} by age alone).
5. Added the day's average speed to the energy model (air drag, on the square of speed): the pilot fit improves only from {rmse0} to {rmse1} per cent, and a model without it validates on held-out pilot days, because the pilot never drives as fast as the Värnamo duties.
6. Set each Värnamo duty's design-day speed from route_register_2026.xlsx's routing-tool driving time times the pilot's actual-to-planned speed ratio at -5 C ({rr}; {ry} over the year). Without a speed term the order is {cnsp} ({nspx} in); at the routing tool's speed {cpln} ({plnx} out); at the year's ratio {cmean} ({meanx} out).
7. Forecast each duty at -5 C, its planning load and its design-day speed: {goset} at {gor}; {near} at {nearr}; the rest at {restr}.
8. Order {n} tractors. Declared payloads order {cdec} ({decx} in, V14 out), one cold rate {cone}, no first-year loss {cnol} ({nolx} in).

No other order survives: the declared weights dilute the payload term, the one-rate cold form fails its own holdout, FES-2 2.3 charges the first year's loss, and the Värnamo duties drive faster than any pilot day but slower than the routing tool promises on a winter day, so a forecast at the pilot's speeds, at the routing tool's or at the year's average ratio each orders another number. Every route that takes all four steps (knots at 14, 18, -2 or 2 C, a quadratic, temperature bins, the station's temperature, either year alone, a within-duty fit, the calibration on the last twelve months, each temperature-controlled loss fit, speed as a straight line, and the ratio's slope below 8 or 12 C, on the temperature or over days within 2.5 C of -5) orders the same {n}, with every energy within {rmax} kWh of those above.
""".format(
        n=f["call_count"], goset=", ".join(go), noset=", ".join(no), near=", ".join(near), nearr=rng(near),
        lim=f["limit"], uy1=f["usable_y1"], cnsp=rc["no speed term"], sl=f["nospeed_shift_lo"],
        sh=f["nospeed_shift_hi"], lines=L_lines, pt=f["payload_term"], loss=f["loss_pct"],
        rr=f["speed_ratio_design"], ry=f["speed_ratio_year"], pvl=f["plan_speed_lo"], pvh=f["plan_speed_hi"],
        pmax=f["pilot_speed_max"], dvl=f["design_speed_lo"], dvh=f["design_speed_hi"], p10=f["speed_kwh_per_10kmh"],
        pdec=f["payload_term_declared"], v14=E["V14"], days=f["duty_days"], slo=f["clerk_slope_lo"],
        shi=f["clerk_slope_hi"], bt1n=f["backtest_one_rate_abs"], bt2="%+.1f" % f["backtest_two_rates"],
        lage=f["loss_pct_age_only"], rmse0=f["rmse_nospeed_pct"], rmse1=f["rmse_pct"], nspx=", ".join(nsp_extra),
        cpln=rc["the routing tool's speed"], plnx=", ".join(pln_out), cmean=rc["the year's mean speed ratio"],
        meanx=", ".join(mean_out), gor=rng(go), restr=rng(rest), cdec=rc["declared weights"],
        decx=", ".join(dec_extra), cone=rc["one cold rate"], cnol=rc["no first-year loss"],
        nolx=", ".join(nol_extra), rmax=f["rival_maxdev"])
    open(path, "w", encoding="utf-8").write(txt)
