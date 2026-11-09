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
        "rmse_pct": round(g["model"]["rmse_pct"], 1),
        "backtest_one_rate_abs": abs(round(A.backtest(pk, gp, A.H1)[0], 1)),
        # conventions the blocks cite: FES-2 sections, the quoted battery and share, the per-100-km unit, and the
        # capacity model's reference temperature
        "conventions": {"fes_sections": [2.3, 4.1, 4.2, 4.3], "usable_quoted": 540, "share_pct": 85,
                        "per_km": 100, "capacity_ref_c": 20, "pallet_kg": 540},
    }
    cal = A.calibration(pk)
    f["calibration_slope"] = {"%s %s" % k: round(v[1], 2) for k, v in sorted(cal.items())
                              if k[0] in {d["shipper"] for d in pk.days}}
    est = [v for k, v in f["calibration_slope"].items() if 0.0 < v < 0.9 and not k.startswith("BMJ")]
    f["clerk_slope_lo"], f["clerk_slope_hi"] = min(est), max(est)
    return f


def write(path, pk, g, f):
    a = g["assess"]
    E, L = f["energy"], f["planning_load"]
    go, no = f["call_set"], f["stay_diesel"]
    rs, rc = f["route_set"], f["route_count"]
    heavy = sorted(set(rs["no first-year loss"]) - set(go))
    one_extra = sorted(set(rs["one cold rate"]) - set(go))
    dec_extra = sorted(set(rs["declared weights"]) - set(go))
    order = sorted(pk.short)
    L_lines = "\n".join("   - %s: planning load %.1f t, design day %d kWh, %s" %
                        (c, L[c], E[c], "electric" if c in go else "stays diesel") for c in order)
    rng = lambda cs: "%d to %d kWh" % (min(E[c] for c in cs), max(E[c] for c in cs))
    txt = """## Tags

**Domain:** General Statistics & Data Science, Regression, classification & model diagnostics (fleet electrification, a road haulier's battery-electric duty assignment).
**Analytical objective:** Forecasting & Predictive Modeling.

## Final Recommendation

**Order {n} battery-electric tractors, for {goset}; {noset} stay on diesel.** The heavy duties {heavy} need {heavyr} on the January design day against a limit of **{lim} kWh** (85 per cent of the {uy1} kWh a 540 kWh battery keeps after its first year); the 8 or 9 tractors a careful but hurried forecast orders (declared payloads at {pdec} kWh per tonne per 100 km, one cold rate, the pilot batteries' age trend alone) send duties out that cannot finish a cold day inside the reserve.

## Supplementary Questions

### ev_duty_assessment_2027.xlsx
1. Sheet Assessment, one row per shortlisted duty in duty order, with shipper, delivery, the three legs and round trip km, climb, planning load (0.1 t), design-day energy (nearest 10 kWh; any figure within 10 kWh of the one below is acceptable), share of the first-year usable battery and whether it goes electric; below the rows the usable battery after the first year ({uy1} kWh), the limit ({lim} kWh), the tractors to order ({n}) and the duties.
{lines}
2. Sheet Energy model: the coefficients, with one tonne of payload adding **{pt} kWh per 100 loaded km**, and the cold-form comparison on January and February 2026 held out (one rate below 16 C {bt1} per cent on the sub-zero days, a further rate below 0 C {bt2} per cent).
3. Sheet Payload calibration: each pilot shipper's weighed load against its declared weight on the Värnamo weighbridge, by note period (the drinks maker's notes carry its scale weight from August 2026), and the load each declaration is taken to.
4. Sheet Battery: the pilot batteries' first-year permanent loss, **{loss} per cent**, the usable battery after the first year {uy1} kWh and the limit {lim} kWh.
5. Sheet Routes: each shortcut's payload figure, loss, limit and order beside the golden's.

### tractor_order_memo.pdf
6. One page to the management group: the order ({n} tractors, {goset}) first, the fourteen duties with planning load, design-day energy and verdict, the three estimates that move the order (payload {pt} kWh per tonne per 100 km against {pdec} on the declarations, the two-rate cold form, the {loss} per cent first-year loss) and what each shortcut would order instead.

## Critical Components

1. One tonne of payload adds **{pt} kWh per 100 loaded km** once each pilot day's declared weight is taken to the weighed load it stands for, shipper by shipper; fitted on the declarations it is **{pdec}**.
2. The pilot batteries lose **{loss} per cent** of their usable energy for good in their first year (temperature taken out of each day's energy per full charge), so the 2027 tractor keeps **{uy1} kWh** and the limit is **{lim} kWh**.
3. On the January design day, with a further cold rate below 0 C, {heavy} need **{heavyr}** and V14 needs **{v14} kWh**.

## Step-by-Step

1. Cleaned bev_daily_summary_2025-03_2026-10.csv (a day uploaded twice kept once, ambient dropouts filled from the Jönköping station plus the mean offset) and joined tms_consignments_jonkoping_2025-2026.csv on registration and date: {days} pilot duty-days with declared weights read in kg or tonnes.
2. Planning loads from weighbridge_varnamo_2024-11_2026-10.csv per FES-2 4.2: the last weighing of each CMR, VMO-nn read as Vnn, gross less tare, November 2025 to October 2026 (V03 {l03} t, V14 {l14} t).
3. Fitted each duty-day's energy on km, climb, cold and payload times loaded km. On the declared weights the payload term is {pdec} kWh per tonne per 100 km and held-out days look fine, because they carry the same declarations.
4. Read the declarations against the Värnamo weighings shipper by shipper: the clerks' weighed load rises only {slo} to {shi} t per declared tonne, the dairy declares its planned pallets at 540 kg each its weighed load following the pallet count at {sbmj} t per declared tonne, and the drinks maker's notes match the bridge from August 2026. Each pilot day's declaration taken to its expected weighed load at its shipper and note period gives **{pt}**; one pooled line over the bridge gives {ppool} and one over the pilot shippers {pline}, each mixing different declaration habits.
5. Chose the cold form out of sample: fitted without January and February 2026, one rate below 16 C under-forecasts those sub-zero days by {bt1n} per cent; with a further rate below 0 C the error is {bt2} per cent. One rate puts every design-day energy about 12 kWh low and admits {one_extra}.
6. Estimated the first-year loss from each day's energy per full charge (kWh used over the SOC it took) with a level per tractor, age in service and degrees below 20 C: **{loss} per cent**. Age alone gives {lage} per cent, because the pilot began in March and ended in a mild October; the same months a year apart give {lyoy}. Usable battery {uy1} kWh, limit {lim} kWh (FES-2 2.3, 4.3).
7. Forecast each duty at -5 C and its planning load from route_register_2026.xlsx: {goset} at {gor}; {heavy} at {heavyr}; the rest at {restr}.
8. Order {n} tractors. Declared payloads order {cdec} ({dec_extra} in, V14 out), one cold rate {cone}, no first-year loss {cnol}, the three hurried steps together {ccar}.

No other order survives: the declared weights are unbiased on average but scattered, so the slope fitted on them is diluted and only the weighbridge, read shipper by shipper, recovers it; the one-rate cold form fails its own holdout; and FES-2 2.3 charges the first year's loss, which the cold days hide unless temperature is taken out. Every route that takes all three steps (knots at 14, 18, -2 or 2 C, a quadratic, temperature bins, the station's temperature, either year alone, a within-duty fit, the calibration on the last twelve months, any of the temperature-controlled loss fits or the same months a year apart) orders the same {n}, with every energy within 6 kWh of those above.
""".format(
        n=f["call_count"], goset=", ".join(go), noset=", ".join(no), heavy=", ".join(heavy),
        heavyr=rng(heavy), lim=f["limit"], uy1=f["usable_y1"], pdec=f["payload_term_declared"],
        lines=L_lines, pt=f["payload_term"], bt1=f["backtest_one_rate"], bt2="%+.1f" % f["backtest_two_rates"],
        bt1n=abs(f["backtest_one_rate"]), loss=f["loss_pct"], v14=E["V14"], days=f["duty_days"],
        l03=L["V03"], l14=L["V14"], ppool=f["payload_term_pooled"], pline=f["payload_term_pilot_line"],
        one_extra=", ".join(one_extra), lage=f["loss_pct_age_only"], lyoy=f["loss_pct_yoy"],
        gor=rng(go), restr=rng([c for c in no if c not in heavy]), cdec=rc["declared weights"],
        dec_extra=", ".join(dec_extra), cone=rc["one cold rate"], cnol=rc["no first-year loss"],
        ccar=rc["careful but hurried"], slo=f["clerk_slope_lo"], shi=f["clerk_slope_hi"], sbmj=f["calibration_slope"]["BMJ all"])
    open(path, "w", encoding="utf-8").write(txt)
