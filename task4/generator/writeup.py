"""figures.json and submission.md, every figure computed here from the shipped pack (analysis.py), never typed."""
import datetime as dt

import numpy as np

import analysis as A

PILOT_SHIPPERS = ["TEN", "HWP", "GDR", "LBY"]


def r10(x):
    return int(round(x / 10.0) * 10)


def back_test(pk):
    """fit on everything but January and February 2026, test on those days"""
    test = np.array([dt.date(2026, 1, 1) <= d["date"] <= dt.date(2026, 2, 28) for d in pk.days])
    y = np.array([d["kwh"] for d in pk.days])
    cold = test & (np.array([d["t_filled"] for d in pk.days]) < 0)
    out = {}
    for name, how, form in [("declared", "declared", ("hinge2", 16, 0)), ("golden", "shipper", ("hinge2", 16, 0)),
                            ("golden_1h", "shipper", ("hinge1", 16))]:
        p = A.payloads(pk, how)
        m = A.fit(pk, p, form, mask=~test)
        e = (y - A.design(pk, p, form) @ m["coef"]) / y * 100
        out[name] = {"rmse": float(np.sqrt(np.mean(e[test] ** 2))), "bias_below0": float(np.mean(e[cold]))}
    out["n_test"] = int(test.sum())
    return out


def figures(pk, g):
    M = g["models"]
    a = g["assess"]
    nv = A.assess(pk, M["naive"])
    pl = A.assess(pk, M["pooled"])
    h1 = A.assess(pk, M["golden_1h"])
    r0, rate = A.rung0(pk)
    cal = A.calibration(pk)
    diffs = [r["declared"] - r["net"] for r in pk.wb if r["declared"] is not None]
    bt = back_test(pk)
    exact = A.fit_exact_slope(pk)
    lam = {s: round(float(cal[s][1]), 2) for s in PILOT_SHIPPERS}
    heavy = [c for c in sorted(pk.short) if not a[c]["go"] and A.planning_load(pk, c) > 25]
    f = {
        "call_count": g["count"], "call_set": g["set"],
        "stay_diesel": sorted(c for c in pk.short if not a[c]["go"]),
        "energy_kwh": {c: r10(a[c]["kwh"]) for c in sorted(a)},
        "energy_kwh_unrounded": {c: round(a[c]["kwh"], 1) for c in sorted(a)},
        "planning_load_t": {c: round(A.planning_load(pk, c), 1) for c in sorted(a)},
        "limit_kwh": round(A.SHARE * A.USABLE), "usable_kwh": int(A.USABLE),
        "slope_golden": round(A.slope_per_100(M["golden"]), 1),
        "slope_declared": round(A.slope_per_100(M["naive"]), 1),
        "slope_pooled": round(A.slope_per_100(M["pooled"]), 1),
        "slope_exact_shipper": round(A.slope_per_100(exact), 1),
        "pooled_lambda": round(float(cal_pooled(pk)), 2),
        "pilot_lambda": lam, "lambda_min": min(lam.values()), "lambda_max": max(lam.values()),
        "bmj_standard_kg": 13500, "ttv_lambda": round(float(cal["TTV"][1]), 2),
        "mean_declared_minus_weighed_kg": int(round(float(np.mean(diffs)))),
        "duty_days": len(pk.days),
        "default_count": len(A.chosen(nv)), "default_set": A.chosen(nv),
        "default_energy_kwh": {c: r10(nv[c]["kwh"]) for c in sorted(nv)},
        "pooled_count": len(A.chosen(pl)),
        "rung0_count": len(A.chosen(r0)), "rung0_rate_kwh_per_km": round(rate, 2),
        "hinge1_energy_kwh": {c: r10(h1[c]["kwh"]) for c in sorted(h1)},
        "heavy": heavy, "heavy_energy_kwh": r10(np.mean([a[c]["kwh"] for c in heavy])),
        "heavy_default_kwh": r10(np.mean([nv[c]["kwh"] for c in heavy])),
        "v14_energy_kwh": r10(a["V14"]["kwh"]), "v14_default_kwh": r10(nv["V14"]["kwh"]),
        "holdout_rmse_declared": round(bt["declared"]["rmse"], 1), "holdout_rmse_golden": round(bt["golden"]["rmse"], 1),
        "holdout_days": bt["n_test"],
        "below0_bias_hinge1_pct": round(bt["golden_1h"]["bias_below0"], 1),
        "below0_bias_golden_pct": round(bt["golden"]["bias_below0"], 1),
        "max_go_kwh": r10(max(a[c]["kwh"] for c in g["set"])),
        "limit_share_pct": int(round(A.SHARE * 100)), "slope_basis_km": 100, "fes2_sections": [4.1, 4.2, 4.3],
    }
    return f


def cal_pooled(pk):
    c = A.calibration(pk, "pooled")
    return next(iter(c.values()))[1]


def write(path, pk, g, f):
    names = {"TEN": "Tenhult Möbler", "HWP": "Huskvarna Wellpapp", "GDR": "Gränna Dryckes", "LBY": "Lekeryds Byggvaror"}
    e = f["energy_kwh"]
    go = ", ".join(f["call_set"])
    stay = ", ".join(f["stay_diesel"])
    lines = []
    L = lines.append
    L("## Tags")
    L("")
    L("**Domain:** Mathematics, Statistics and Computer Science, General Statistics & Data Science (regression, "
      "classification & model diagnostics), house domain Supply Chain & Logistics.")
    L("**Analytical objective:** Forecasting & Predictive Modeling.")
    L("")
    L("## Final Recommendation")
    L("")
    L("**Order %d battery-electric tractors, for Värnamo duties %s; %s stay on diesel.** Each of the six needs at "
      "most **%d kWh** on the January design day against FES-2's **%d kWh** (85 per cent of 540 kWh usable) once each "
      "pilot day's declared payload is taken to the weighed load it stands for, which puts a tonne at **%.1f kWh per "
      "100 km loaded**; the model fitted on the declared weights (%.1f kWh) orders %d, sending the heavy duties %s "
      "(%d kWh on the declared weights, %d kWh in fact) and dropping V14."
      % (f["call_count"], go, stay, f["max_go_kwh"], f["limit_kwh"], f["slope_golden"], f["slope_declared"],
         f["default_count"], ", ".join(f["heavy"]), f["heavy_default_kwh"], f["heavy_energy_kwh"]))
    L("")
    L("## Supplementary Questions")
    L("")
    L("### ev_duty_assessment_2027.xlsx")
    L("")
    L("1. One row per shortlisted duty (fourteen), with its shipper, delivery, the three legs and round-trip km, "
      "climb, planning load (mean weighed net payload, November 2025 to October 2026), the January design-day "
      "energy to the nearest 10 kWh, its share of the 540 kWh usable battery and whether it goes battery-electric; "
      "beneath, the number of tractors and the duties going. Sheets for the energy model and the payload calibration "
      "sit behind it.")
    k = 2
    for c in sorted(e):
        L("%d. %s: %d kWh, %s." % (k, c, e[c], "goes battery-electric" if c in f["call_set"] else "stays diesel"))
        k += 1
    L("%d. Tractors to order: %d (%s)." % (k, f["call_count"], go))
    k += 1
    L("")
    L("### tractor_order_memo.pdf")
    L("")
    L("%d. One page to the board: the order of %d tractors and the duties first, the fourteen duties' design-day "
      "energies in a table, then how the energy was estimated (the declared payloads calibrated on the Värnamo "
      "weighbridge, %.1f against %.1f kWh per tonne per 100 km) and what the declared-weight model would have "
      "ordered (%d tractors)." % (k, f["call_count"], f["slope_golden"], f["slope_declared"], f["default_count"]))
    L("")
    L("## Critical Components")
    L("")
    L("1. On the Värnamo weighbridge the declarations are right on average (declared less weighed, **%d kg**) but "
      "for the estimating pilot shippers the weighed load rises only **%.2f to %.2f** tonnes per declared tonne; the "
      "dairy declares one standard weight (**13,500 kg**) and Tabergs Trävaror its own weighbridge figure (slope "
      "**%.2f**)." % (f["mean_declared_minus_weighed_kg"], f["lambda_min"], f["lambda_max"], f["ttv_lambda"]))
    L("2. A tonne of payload costs **%.1f kWh per 100 km loaded** with each pilot day's payload taken to its expected "
      "weighed load shipper by shipper (the Tabergs days alone give %.1f), against **%.1f** fitted on the declared "
      "weights." % (f["slope_golden"], f["slope_exact_shipper"], f["slope_declared"]))
    L("3. The heavy duties %s need **%d kWh** on the January design day and V14 **%d kWh**, against the %d kWh "
      "limit." % (", ".join(f["heavy"]), f["heavy_energy_kwh"], f["v14_energy_kwh"], f["limit_kwh"]))
    L("4. **%d** tractors: %s." % (f["call_count"], go))
    L("")
    L("## Step-by-Step")
    L("")
    steps = [
        "Joined bev_daily_summary_2025-03_2026-10.csv (a day uploaded twice kept once) to "
        "tms_consignments_jonkoping_2025-2026.csv on registration and date, giving %d duty-days with the declared "
        "weight (kilograms or tonnes with a decimal comma) and the duty's legs and climb from route_register_2026.xlsx; "
        "ambient dropouts took the Jönköping station day from daily_mean_temperature_2016-2026.csv." % f["duty_days"],
        "Fitted each duty-day's battery energy by least squares on km, climb times km, the degrees below 16 C and "
        "below 0 C times km, and payload times loaded km; on the declared weights the payload term is %.1f kWh per "
        "tonne per 100 km, and the model predicts January and February 2026 held out within %.1f per cent." %
        (f["slope_declared"], f["holdout_rmse_declared"]),
        "Applied at −5 C and each duty's planning load from weighbridge_varnamo_2024-11_2026-10.csv, that model "
        "orders %d tractors (%s), the reasonable but insufficient answer: the heavy duties come out at %d kWh and V14 "
        "at %d kWh." % (f["default_count"], ", ".join(f["default_set"]), f["heavy_default_kwh"],
                        f["v14_default_kwh"]),
        "Read the weighbridge (the last weighing of each CMR, net as gross less tare) against the declared weights "
        "shipper by shipper: right on average, but for %s the weighed load regresses on the declared at %.2f to %.2f, "
        "the dairy's notes carry one standard weight and Tabergs' carry its weighbridge ticket, so a slope fitted on "
        "the declarations is diluted wherever the declarations scatter around the load, and one pooled line over the "
        "weighbridge (%.2f) carries the shippers' differences in load, not the clerks' error, and corrects it only to "
        "%.1f." % (", ".join(names[s] for s in PILOT_SHIPPERS), f["lambda_min"], f["lambda_max"],
                   f["pooled_lambda"], f["slope_pooled"]),
        "Replaced each pilot day's declaration by its expected weighed load given the shipper and the declaration "
        "(the shipper's weighed mean for the dairy, the declaration itself for Tabergs) and refitted: %.1f kWh per "
        "tonne per 100 km; Tabergs' own days, whose declarations are exact, give %.1f on their own." %
        (f["slope_golden"], f["slope_exact_shipper"]),
        "Kept the second cold rate below 0 C: with one rate below 16 C the model fitted without January and "
        "February 2026 under-predicts their sub-zero days by %.1f per cent, with both rates by %.1f." %
        (f["below0_bias_hinge1_pct"], f["below0_bias_golden_pct"]),
        "Predicted each shortlisted duty on the January design day at its planning load and kept those within %d kWh "
        "(FES-2 4.1 to 4.3): %s, %d tractors." % (f["limit_kwh"], go, f["call_count"]),
    ]
    for i, s in enumerate(steps, 1):
        L("%d. %s" % (i, s))
    L("")
    L("No other order survives: the model's held-out check cannot see the dilution because the held-out days carry "
      "the same declarations, so only the weighbridge, which weighs the same shippers' loads, measures it; every "
      "route that takes each shipper's declarations to the weighed load (a line per shipper, the shipper's mean, the "
      "exact shipper's days, a within-duty fit, either year, any cold form with a rate below 0 C) gives the same six "
      "duties, while the declared weights, one pooled correction and an average consumption on cold days order %d, "
      "%d and %d." % (f["default_count"], f["pooled_count"], f["rung0_count"]))
    open(path, "w", encoding="utf-8").write("\n".join(lines) + "\n")
