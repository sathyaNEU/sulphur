"""figures.json and submission.md, every figure emitted from analysis.py on the shipped pack (never typed)."""
import numpy as np

import analysis as A
import params as P

R1_TOL, E_TOL, LOSS_BAND, HEAT_HALF, GAP_TOL, NIGHT_TOL, COND_HALF = 0.7, 10, (2.7, 5.0), 0.4, 1.0, 0.3, 0.7


def heat_band(heater_kw):
    """the heaters' heat is graded within half a kW of the golden's figure at its rounding"""
    return (round(round(heater_kw, 1) - HEAT_HALF, 1), round(round(heater_kw, 1) + HEAT_HALF, 1))


def cond_band(cond_kw):
    """the conditioning draw at the design night is graded within 0.7 kW of the golden's figure at its rounding (the
    temperature attributions, the knot and the base term span 2.9 to 3.5 kW)"""
    return (round(round(cond_kw, 1) - COND_HALF, 1), round(round(cond_kw, 1) + COND_HALF, 1))


def r10(x):
    return int(round(x / 10.0) * 10)


def cond_rivals(pk):
    """the conditioning draw at the design night under every reading a careful fit could take, kW"""
    se = A.session_frame(pk)
    out = {}
    for name, kw in (("evening", {"tcol": "t_evening"}), ("morning", {"tcol": "t_morning"}), ("sensor", {"tcol": "t_sensor"}),
                     ("knot_0", {"T0": 0.0}), ("knot_10", {"T0": 10.0})):
        sub = se.dropna(subset=[kw.get("tcol", "t_night")])
        out[name] = round(A.charging_model(pk, se=sub, **kw)[4], 2)
    return out


def figures(pk, g):
    car = A.careful(pk)
    qk = A.quick(pk)
    routes = A.routes(pk, g)
    pilot = sorted(c for c, n in g["parts"]["days"].items() if c in pk.weekday and n >= 30)
    others = [c for c in pk.weekday if c not in pilot]
    rates = g["rates"]
    taken = g["taken"]
    # the year's diesel litres on the assigned blocks, from the rates and the dispatch log's kilometres
    disp = pk.dispatch[(pk.dispatch["date"] >= A.REF[0]) & (pk.dispatch["date"] <= A.REF[1])]
    km_year = disp.groupby("code")["planned_km"].sum().to_dict()
    litres = sum(rates[c] / 100.0 * km_year.get(c, 0.0) for c in taken)
    loss_forms = {f: round(100 * A.capacity_loss(pk, f)[0], 2) for f in ("curved", "linear", "sqrt", "log")}
    bb, rmse, n = A.bridge(pk, g["parts"]["e_block"], g["parts"]["days"], rates)
    bh, rmse_h, _ = A.bridge(pk, g["parts"]["e_block"], g["parts"]["days"], rates, with_hours=True)
    Eh, _ = A.design_energies(pk, "golden", rates, bridge_hours=True)
    Eall, _ = A.design_energies(pk, "golden", rates, own_min_days=10 ** 6)
    short_km = [c for c in pk.weekday if pk.blocks[c]["km_old"] <= 225]
    rank_all = sorted(pk.weekday, key=lambda c: rates[c])
    rank_short = sorted(short_km, key=lambda c: rates[c])
    f = {
        "call_count": len(taken),
        "call_set": sorted(taken),
        "stay_diesel": sorted(c for c in pk.weekday if c not in taken),
        "qualifying_count": len(g["qualifying"]),
        "refused_block": g["refused"],
        "refused_short_kwh": int(round(g["short"] / 10.0) * 10),
        "diesel": {c: round(rates[c], 1) for c in pk.weekday},
        "diesel_min": round(min(rates[c] for c in pk.weekday), 1),
        "diesel_max": round(max(rates[c] for c in pk.weekday), 1),
        "pilot_blocks": pilot,
        "pilot_diesel_mean": round(float(np.mean([rates[c] for c in pilot])), 1),
        "others_diesel_mean": round(float(np.mean([rates[c] for c in others])), 1),
        "pilot_gap": round(float(np.mean([rates[c] for c in others]) - np.mean([rates[c] for c in pilot])), 1),
        "pilot_ranks_all": sorted(rank_all.index(c) + 1 for c in pilot),
        "pilot_ranks_short": sorted(rank_short.index(c) + 1 for c in pilot),
        "short_km_blocks": len(short_km),
        "heater_kw": round(g["heater_kw"], 1),
        "heater_lph": round(g["parts"]["heater_lph"], 2),
        "heater_T0": g["parts"]["heater_T0"],
        "heater_kwh_per_l": round(A.HEATER_KWH_PER_L, 2),
        "heater_fault_check": [[fn, a.isoformat(), b.isoformat(), nd, round(v, 1)] for fn, a, b, nd, v in g["faults"]],
        "pilot_hvac_kw_design": round(g["parts"]["h_pilot"], 1),
        "heat_new_kw": round(g["parts"]["heat_new"], 1),
        "energy": {c: r10(g["E"][c]) for c in pk.weekday},
        "energy_bridge_hours": {c: r10(Eh[c]) for c in pk.weekday},
        "energy_bridge_all": {c: r10(Eall[c]) for c in pk.weekday},
        "verdict": {c: "yes" if g["verdict"][c] else "no" for c in pk.weekday},
        "loss_pct": round(100 * g["loss"], 1),
        "loss_forms": loss_forms,
        "usable_y1": round(pk.usable_2027 * (1 - g["loss"]), 1),
        "limit_kwh": round(g["limit"], 1),
        "eta": round(g["eta"], 3),
        "ratio_pooled": round(g["ratio_pooled"], 3),
        "cond_kw": round(g["cond_kw"], 1),
        "cond_base_kw": round(g["cond_fit"][0], 2),
        "cond_slope_kw": round(g["cond_fit"][1], 3),
        "cond_t0": g["cond_fit"][2],
        "cond_rivals": cond_rivals(pk),
        "cond_mult_eta15": round(A.charging_ratio_by_cold(pk)[0], 3),
        "cond_rmse": round(g["cond_fit"][3], 2),
        "cond_mult_rmse": round(A.charging_ratio_by_cold(pk)[1], 2),
        "session_min_rise": 30,
        "night_mwh": round(g["grid_kwh"] / 1000.0, 1),
        "demand_mwh": round(g["demand_kwh"] / 1000.0, 1),
        "demand_recharge_mwh": round(sum(g["E"][c] / g["eta"] for c in g["qualifying"]) / 1000.0, 1),
        "demand_cond_mwh": round((g["demand_kwh"] - sum(g["E"][c] / g["eta"] for c in g["qualifying"])) / 1000.0, 1),
        "demand_battery_mwh": round(sum(g["E"][c] for c in g["qualifying"]) / 1000.0, 1),
        "demand_pooled_mwh": round(sum(g["E"][c] / g["ratio_pooled"] for c in g["qualifying"]) / 1000.0, 1),
        "night_capacity_mwh": round(pk.supply * 10 / 1000.0, 2),
        "careful_demand_mwh": round(car["demand_kwh"] / 1000.0, 1),
        "night_battery_mwh": round(sum(g["E"][c] for c in taken) / 1000.0, 1),
        "window_h_min": round(min((A.window(pk, c)[1] - A.window(pk, c)[0]) / 60.0 for c in g["qualifying"]), 1),
        "window_h_max": round(max((A.window(pk, c)[1] - A.window(pk, c)[0]) / 60.0 for c in g["qualifying"]), 1),
        "supply_kw": int(pk.supply),
        "bridge": {"a": round(float(bb[0]), 4), "b": round(float(bb[1]), 5), "rmse": round(rmse, 3), "blocks": n},
        "bridge_hours": {"a": round(float(bh[0]), 4), "b": round(float(bh[1]), 5), "c": round(float(bh[2]), 4), "rmse": round(rmse_h, 3)},
        "diesel_litres_assigned": int(round(litres / 1000.0) * 1000),
        "careful_count": len(car["taken"]),
        "careful_set": sorted(car["taken"]),
        "careful_energy": {c: r10(car["E"][c]) for c in pk.weekday},
        "careful_heat_kw": round(car["parts"]["heat_used"], 1),
        "careful_loss_pct": round(100 * car["loss"], 1),
        "careful_qualifying": len(car["qualifying"]),
        "quick_count": len(qk["taken"]),
        "quick_rate": round(qk["rate"], 2),
        "routes": {k: len(v) for k, v in routes.items()},
        "route_sets": {k: sorted(v) for k, v in routes.items()},
        "weather_offset": round(pk.temp_offset, 2),
        "stay_diesel_count": 48 - len(taken),
        "weekday_blocks": 48,
        "per_km": 100,
        "des_sections": [2.1, 2.2, 2.3, 2.4, 3.2, 3.3, 4.1, 4.2, 4.3],
        "careful_pooled_count": len(routes["the sessions' pooled ratio for the night (the battery's conditioning left out)"]),
        "sheet_count": 4,
        "slide_count": 3,
        "pilot_bus_count": 6,
        "pilot_block_count": 9,
        "short_km_threshold": 225,
        "other_block_count": 39,
        "conventions": {"share_pct": 85, "design_t": -15, "usable_quoted": int(pk.usable_2027), "charger_kw": 150,
                        "night_period": "21:00-07:00", "ref_year": "2025-11-01 to 2026-10-31", "energy_tol": E_TOL,
                        "diesel_tol": R1_TOL, "loss_band": list(LOSS_BAND), "heat_band": list(heat_band(g["heater_kw"])), "gap_tol": GAP_TOL,
                        "night_tol": NIGHT_TOL, "heater_rating_kw": 35, "heater_rating_lph": 3.9,
                        "cond_band": list(cond_band(g["cond_kw"]))},
    }
    return f


def _rows(pk, g, f):
    out = []
    for c in sorted(pk.weekday, key=lambda c: pk.priority[c]):
        out.append("%s (priority %d): %s l/100 km, %d kWh, %s%s" % (c, pk.priority[c], f["diesel"][c], f["energy"][c], f["verdict"][c],
                                                                     ", assigned" if c in f["call_set"] else ""))
    return out


def write(path, pk, g, f):
    cs = ", ".join(f["call_set"])
    rt = f["routes"]
    L = []
    L.append("# task4: Niittylä's 2027 battery-electric bus order\n")
    L.append("## Tags\n")
    L.append("**Domain:** General Statistics & Data Science, Regression, classification & model diagnostics (a bus operator's depot "
             "electrification: forecasting each block's battery energy for buses that have never run it).\n")
    L.append("**Analytical objective:** Forecasting & Predictive Modeling.\n")
    L.append("## Final Recommendation\n")
    L.append("Order %d battery-electric buses for the weekday blocks %s; the other %d weekday blocks stay on diesel until the "
             "connection is reinforced. Not the %d that carrying the pilot's own fit to the blocks it never ran and charging the "
             "night at the sessions' average ratio would order (the pilot ran thrifty blocks, and on a -15 C night every plugged-in "
             "bus also takes about %.1f kW through its charger to keep its battery warm), and not the %d blocks that pass the "
             "design-day limit on their own: the night period's %d kW recharges %d of them in the plan's priority order, and %s, "
             "next on the list, cannot be recharged together with them under any schedule.\n"
             % (f["call_count"], cs, 48 - f["call_count"], f["careful_count"], f["cond_kw"], f["qualifying_count"], f["supply_kw"],
                f["call_count"], f["refused_block"]))
    L.append("## Supplementary Questions\n")
    L.append("### niittyla_ebus_order_2027.xlsx\n")
    L.append("The workbook has four sheets: Order (the count, the blocks, the limit, the loss, the night's figures), Blocks (one row "
             "per weekday block in the plan's priority order: block, lines, zone, scheduled km, hours out, diesel l/100 km, design-day "
             "energy kWh, qualifies, assigned 2027, pilot block), Night (each qualifying block's return, departure, charging window, "
             "recharge and conditioning at the connection point, and whether it is assigned, with the next block on the list and its "
             "shortfall) and Model (the pilot's per-km energy by block with its electric days and diesel figure, the bridge, the "
             "heating figures, the charging split). The slides (niittyla_ebus_order_2027.pptx) carry the order, a bar chart of the "
             "48 energies against the limit in priority order, and what the figures rest on.\n")
    L.append("1. Estimated diesel use per weekday block over November 2025 to October 2026, litres per 100 scheduled km to one decimal "
             "(workbook sheet Blocks, column \"Diesel l/100 km\"; graded within %.1f l/100 km): %s. The 48 figures run from %.1f to "
             "%.1f; each block's figure is the litres on the fuel-card statement between the fills of every bus that ran it, "
             "spread over the blocks the dispatch log shows between those fills, so a block that shared its buses' fills with "
             "other blocks gets its own rate and not its buses' average.\n"
             % (R1_TOL, "; ".join("%s %.1f" % (c, f["diesel"][c]) for c in sorted(pk.weekday)), f["diesel_min"], f["diesel_max"]))
    L.append("2. Forecast design-day energy per weekday block for a 2027 bus, kWh to the nearest 10, from the company's own "
             "operating records: the pilot buses' energy per km outside heating, carried to every block by its diesel use, and the "
             "heating the 2027 model takes from its battery on a -15 C day (sheet Blocks, \"Design-day energy kWh\"; graded within %d "
             "kWh): %s.\n" % (E_TOL, "; ".join("%s %d" % (c, f["energy"][c]) for c in sorted(pk.weekday))))
    L.append("3. Whether each weekday block's forecast qualifies under DES-1 4.1, its design-day energy against %d kWh (85 per cent of %d kWh "
             "usable after the first winter): %s. %d blocks qualify; the %d assigned are those the night period recharges in "
             "priority order (sheet Blocks, \"Qualifies\" and \"Assigned 2027\").\n"
             % (round(g["limit"]), round(f["usable_y1"]), "; ".join("%s %s" % (c, f["verdict"][c]) for c in sorted(pk.weekday)),
                f["qualifying_count"], f["call_count"]))
    L.append("4. The estimated share of usable battery the company's own electric buses lose for good in their first twelve months in service: "
             "%.1f per cent (sheet Order; graded within the band %.1f to %.1f, which every age form a fit could take spans, a straight "
             "line in age included; no reading inside it moves a verdict or the order). Usable battery for planning %d kWh, limit %d "
             "kWh.\n" % (f["loss_pct"], LOSS_BAND[0], LOSS_BAND[1], round(f["usable_y1"]), round(g["limit"])))
    L.append("5. The forecast energy the charging installation would draw at the connection point on the design night with the bus of every "
             "qualifying block on charge: %.1f MWh for the %d qualifying blocks (sheet Night; graded within %.1f MWh), each bus's "
             "recharge over the chargers' efficiency and the steady draw it takes beside it to keep its battery warm over its %.1f to "
             "%.1f hours on charge. The night period's %d kW gives at most %.2f MWh between 21:00 and 07:00, which is why the plan's "
             "list is cut at %d buses.\n"
             % (f["demand_mwh"], f["qualifying_count"], NIGHT_TOL, f["window_h_min"], f["window_h_max"], f["supply_kw"],
                f["night_capacity_mwh"], f["call_count"]))
    L.append("## Critical Components\n")
    L.append("1. The pilot ran the thrifty blocks: the nine blocks the six electric buses ran on weekdays average **%.1f** litres of diesel "
             "per 100 km against **%.1f** for the other 39 (a gap of **%.1f** l/100 km, graded within %.1f); among the %d weekday blocks of "
             "225 km or less on the 2024 timetable (the pilot buses' range) they sit in the thriftiest half, and none of the nine is among the "
             "ten thriftiest of the 48 or among its hardest sixteen. Kilometres, climb and timetable speed do not carry that gap (the bridge from "
             "diesel use to the pilot's energy per km, fitted over the %d blocks an electric bus ran with their diesel figures, has "
             "a slope of %.4f kWh per km per l/100 km and a residual of %.3f kWh per km), so a fit carried on those covariates "
             "forecasts the hard blocks light; the diesel figures carry every block's difficulty to the design day.\n"
             % (f["pilot_diesel_mean"], f["others_diesel_mean"], f["pilot_gap"], GAP_TOL, f["short_km_blocks"], f["bridge"]["blocks"],
                f["bridge"]["b"], f["bridge"]["rmse"]))
    L.append("2. The pilot buses' fuel-fired cabin heaters supplied about **%.1f kW** of heat on a -15 C day (graded within the band %.1f "
             "to %.1f kW): %.2f litres of HVO an hour, from the electric buses' HVO fills on the fuel-card statement tank to tank "
             "against the days' hours and temperatures, at the heater's rating of 35 kW for 3.9 l/h. The 2027 model heats "
             "electrically with resistive boosters below -10 C, so on the design day it draws that heat from the battery on top "
             "of the %.1f kW the pilot's HVAC drew: %.1f kW of heating an hour out, %d to %d kWh a block.\n"
             % (f["heater_kw"], f["conventions"]["heat_band"][0], f["conventions"]["heat_band"][1], f["heater_lph"], f["pilot_hvac_kw_design"], f["heat_new_kw"],
                r10(min(pk.blocks[c]["hours"] for c in pk.weekday) * f["heater_kw"]), r10(max(pk.blocks[c]["hours"] for c in pk.weekday) * f["heater_kw"])))
    L.append("3. On the design night every plugged-in bus takes about **%.1f kW** through its charger beside the recharge (graded within "
             "the band %.1f to %.1f kW, which every reading of the night's temperature and of the cold's knot spans), for as long as "
             "it is on charge between 21:00 and 07:00: each session's metered energy splits into the battery's gain (its "
             "state-of-charge points times the capacity its own day shows) over the chargers' efficiency and a steady draw over the "
             "session's hours on charge inside the night period that rises as the night's mean falls below a few degrees (the "
             "battery held at its charging temperature). The sessions' pooled ratio of gain to metered energy, %.3f, averages that "
             "draw over a year of mostly mild nights; at -15 C it understates each qualifying bus's night by about %d kWh and puts "
             "%d buses through the night where %d fit.\n"
             % (f["cond_kw"], f["conventions"]["cond_band"][0], f["conventions"]["cond_band"][1], f["ratio_pooled"],
                r10((f["demand_mwh"] - f["demand_pooled_mwh"]) * 1000.0 / f["qualifying_count"]), f["careful_pooled_count"], f["call_count"]))
    L.append("## Step-by-Step\n")
    steps = [
        "Clean and join the operating records: the dispatch log's block codes before 11 August 2025 to the register's current "
        "codes and its early-2024 registrations to fleet numbers; the fuel-card statement's cards to vehicles by the register's "
        "validity dates, the night shift's spare cards by the fleet number typed at the pump; the telematics days the portal "
        "uploaded twice dropped; blank ambient readings filled from the airport station (the town station less its %.2f C offset "
        "where the airport has its April 2023 gap); the charging sessions' UTC stamps put on local time (summer time included) "
        "and each session given its evening." % f["weather_offset"],
        "Diesel use per block (ask 1): for each diesel bus, consecutive diesel fills on the statement with a second swipe within "
        "twelve minutes merged into one fill; the litres of each fill are the fuel burnt on the bus-days the dispatch log shows "
        "between that fill and the one before, by departure time; over November 2025 to October 2026 the litres of every interval "
        "are regressed on the scheduled kilometres each block contributed to it, jointly over every block the intervals touch "
        "(the weekend blocks included, since a bus's fills span both), giving one rate per block (%.1f to %.1f "
        "l/100 km). Charging each fill to the block the bus ran on the day of the fill, or giving every block its commonest bus's "
        "yearly rate, puts most blocks several litres off because the buses rotate over the blocks." % (f["diesel_min"], f["diesel_max"]),
        "The pilot's record: the nine weekday blocks with 30 or more electric bus-days sit in the middle of the 48 by diesel use (none among "
        "the ten thriftiest, none among the hardest sixteen) and in the thriftiest half of the %d blocks of 225 km or less on the 2024 "
        "timetable (the planner picked the blocks from the fuel figures and the buses' range), averaging %.1f "
        "against %.1f l/100 km for the rest (component 1). Beside them the electric buses ran three short stand-in blocks and the "
        "weekend blocks, which give the bridge its reach over harder blocks." % (f["short_km_blocks"],
                                                                                   f["pilot_diesel_mean"], f["others_diesel_mean"]),
        "The pilot's energy model: on each electric bus-day the energy outside heating and cooling (energy used less HVAC) per "
        "kilometre, by block, weighted by kilometres; the HVAC draw per hour out in 1 C bins of the day's ambient. The HVAC draw "
        "flattens at about %.1f kW below -10 C on the pilot buses, because the vehicle register's fuel-fired heater (35 kW, 3.9 l/h) "
        "carries the rest of the cabin's heat below about %.0f C: the electric buses' HVO fills on the statement, tank to tank over "
        "the days between, fit %.2f l/h at -15 C, %.1f kW of heat (component 2; the two buses whose heater the workshop log shows "
        "out in early 2026 drew the extra heat from the battery, %s kWh per litre against the rating's %.2f). The 2027 model has "
        "no fuel heater and runs its boosters below -10 C, so its heating on the design day is %.1f kW an hour out." %
        (f["pilot_hvac_kw_design"], f["heater_T0"], f["heater_lph"], f["heater_kw"],
         " and ".join(str(v[4]) for v in f["heater_fault_check"]), f["heater_kwh_per_l"], f["heat_new_kw"]),
        "The bridge and the energies (ask 2): the per-km energy of the %d blocks an electric bus ran regressed on their diesel rates "
        "(a = %.4f, b = %.5f, residual %.3f kWh per km); for each weekday block the design-day energy is its scheduled km times the "
        "bridged per-km energy (the block's own electric figure where it has 30 or more electric days) plus its hours out times "
        "%.1f kW. Adding the hours per km to the bridge, or bridging every block, moves no energy by more than one 10 kWh bin. "
        "Carrying the pilot's fit on kilometres, climb and timetable speed instead puts the hard blocks light and lets %d blocks "
        "qualify." %
        (f["bridge"]["blocks"], f["bridge"]["a"], f["bridge"]["b"], f["bridge"]["rmse"], f["heat_new_kw"], f["careful_qualifying"]),
        "The limit (asks 3 and 4): each electric bus-day's energy over its state-of-charge drop is the capacity the battery system "
        "shows; on age in service with a cold term and a level per bus, a form with a fast early loss and a steady loss after it "
        "(curved %.2f, square root %.2f, log %.2f per cent; a straight line in age, which runs under the first months' fast "
        "loss, %.2f) gives %.1f per cent in the first twelve months, %d kWh usable on the 2027 model and a limit of %d kWh; %d "
        "blocks pass it, and every one of those forms, and the quoted 480 kWh itself, leaves every verdict where it is." %
        (f["loss_forms"]["curved"], f["loss_forms"]["sqrt"], f["loss_forms"]["log"], f["loss_forms"]["linear"], f["loss_pct"],
         round(f["usable_y1"]), round(g["limit"]), f["qualifying_count"]),
        "The charging split (component 3): on every session with a state-of-charge rise of %d points or more, the charger's metered "
        "energy regressed on the battery's gain and on the hours plugged in inside the night period, the latter alone and times the "
        "night's cold below a knot profiled on half degrees (%.1f C), the night's temperature the mean of the evening's and the "
        "next morning's at the airport station; on this fit the efficiency is %.3f and the draw %.2f kW plus %.3f kW a degree, "
        "%.1f kW at -15 C. Taking the evening's or the morning's temperature alone, the bus's own sensor, or the knot at 0 or 10 C "
        "keeps the draw inside its band and the order at %d; a loss that scales with the recharge instead of the hours fits the "
        "sessions worse and lands the same order." %
        (f["session_min_rise"], f["cond_t0"], f["eta"], f["cond_base_kw"], f["cond_slope_kw"], f["cond_kw"], f["call_count"]),
        "The night (ask 5 and the order): each qualifying block's bus is on charge from its return to its departure inside the "
        "night period, taking its recharge at up to 150 kW less its own steady draw and %.1f kW beside it throughout; the %d "
        "qualifying blocks need %.1f MWh at the connection point, against at most %.2f MWh the night period's %d kW gives. Taken in "
        "the fleet plan's priority order, the list is cut at %s, the %dth, which the night cannot recharge together with the %d "
        "above it under any schedule (the night's maximum flow over the blocks' windows falls short of it; a least-slack "
        "schedule recharges the %d). The six pilot buses go to Kauppala with the 2027 timetable (the fleet plan), so they draw "
        "nothing at Niittylä. Summing the per-block verdicts orders %d; the night at the sessions' pooled ratio orders %d; on "
        "battery energy alone %d. With the quoted capacity in place of the first winter's usable no block changes side, so the "
        "loss is reported for the limit it sets and moves no verdict." %
        (f["cond_kw"], f["qualifying_count"], f["demand_mwh"], f["night_capacity_mwh"], f["supply_kw"], f["refused_block"],
         f["call_count"] + 1, f["call_count"], f["call_count"],
         rt["the per-block verdicts summed, the night's supply ignored"],
         rt["the sessions' pooled ratio for the night (the battery's conditioning left out)"],
         rt["the night scheduled on battery energy (charging losses and conditioning ignored)"]),
        "Why no other conclusion survives: the pilot's fit carried on the timetable's covariates with the night at the pooled "
        "ratio orders %d (%d without the night's supply) and the pilot's cold-day consumption times kilometres orders %d; on "
        "that pass the bridge put right alone orders %d and the battery's conditioning put right alone %d, a different set; "
        "leaving out only the heaters' share orders %d, and the pilot's record carried as it stands %d. "
        "Only the bridge, the heaters' share and the conditioning together, with the first winter's loss and the night's "
        "capacity, land %d." %
        (f["careful_count"], f["routes"]["the careful pass without the night's supply"], f["quick_count"],
         rt["the sessions' pooled ratio for the night (the battery's conditioning left out)"],
         rt["the pilot's fit carried on kilometres, climb and speed (the diesel bridge left out)"],
         rt["the pilot's cold response read as the new buses' (the fuel heaters' share left out)"],
         rt["the pilot's own record carried as it stands (no bridge, no heaters' share, the pooled ratio)"], f["call_count"]),
    ]
    for i, s_ in enumerate(steps, 1):
        L.append("%d. %s\n" % (i, s_))
    open(path, "w", encoding="utf-8").write("\n".join(L))
