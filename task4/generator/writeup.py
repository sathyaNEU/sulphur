"""figures.json and submission.md, every figure emitted from analysis.py on the shipped pack (never typed)."""
import numpy as np

import analysis as A
import params as P

R1_TOL, E_TOL, LOSS_BAND, HEAT_HALF, GAP_TOL, NIGHT_TOL = 0.7, 10, (3.8, 5.0), 0.4, 1.0, 0.3


def heat_band(heater_kw):
    """the heaters' heat is graded within half a kW of the golden's figure at its rounding"""
    return (round(round(heater_kw, 1) - HEAT_HALF, 1), round(round(heater_kw, 1) + HEAT_HALF, 1))


def r10(x):
    return int(round(x / 10.0) * 10)


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
        "night_mwh": round(g["grid_kwh"] / 1000.0, 1),
        "demand_mwh": round(g["demand_kwh"] / 1000.0, 1),
        "demand_battery_mwh": round(sum(g["E"][c] for c in g["qualifying"]) / 1000.0, 1),
        "night_capacity_mwh": round(pk.supply * 10 / 1000.0, 2),
        "careful_demand_mwh": round(car["demand_kwh"] / 1000.0, 1),
        "night_battery_mwh": round(sum(g["E"][c] for c in taken) / 1000.0, 1),
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
        "sheet_count": 4,
        "slide_count": 3,
        "pilot_bus_count": 6,
        "pilot_block_count": 9,
        "short_km_threshold": 225,
        "other_block_count": 39,
        "conventions": {"share_pct": 85, "design_t": -15, "usable_quoted": int(pk.usable_2027), "charger_kw": 150,
                        "night_period": "21:00-07:00", "ref_year": "2025-11-01 to 2026-10-31", "energy_tol": E_TOL,
                        "diesel_tol": R1_TOL, "loss_band": list(LOSS_BAND), "heat_band": list(heat_band(g["heater_kw"])), "gap_tol": GAP_TOL,
                        "night_tol": NIGHT_TOL, "heater_rating_kw": 35, "heater_rating_lph": 3.9},
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
    L = []
    L.append("# task4: Niittylä's 2027 battery-electric bus order\n")
    L.append("## Tags\n")
    L.append("**Domain:** General Statistics & Data Science, Regression, classification & model diagnostics (a bus operator's depot "
             "electrification: forecasting each block's battery energy for buses that have never run it).\n")
    L.append("**Analytical objective:** Forecasting & Predictive Modeling.\n")
    L.append("## Final Recommendation\n")
    L.append("Order %d battery-electric buses for the weekday blocks %s; the other %d weekday blocks stay on diesel until the "
             "connection is reinforced. Not the %d buses that carrying the pilot's own fit to the blocks it never ran would order "
             "(the pilot ran the thriftiest short blocks, and its battery record leaves out the cabin heat its fuel heaters "
             "supplied), and not the %d blocks that pass the design-day limit on their own: the night period's %d kW recharges %d "
             "of them in the plan's priority order, and %s, next on the list, cannot be recharged together with them under any schedule.\n"
             % (f["call_count"], cs, 48 - f["call_count"], f["careful_count"], f["qualifying_count"], f["supply_kw"], f["call_count"],
                f["refused_block"]))
    L.append("## Supplementary Questions\n")
    L.append("### niittyla_ebus_order_2027.xlsx\n")
    L.append("The workbook has four sheets: Order (the count, the blocks, the limit, the loss, the night's figures), Blocks (one row "
             "per weekday block in the plan's priority order: block, lines, zone, scheduled km, hours out, diesel l/100 km, design-day "
             "energy kWh, qualifies, assigned 2027, pilot block), Night (the assigned blocks' return, departure, charging window and "
             "energy at the connection point under a least-slack schedule, with the next block on the list and its shortfall) and "
             "Model (the pilot's per-km energy by block with its electric days and diesel figure, the bridge, the heating figures). "
             "The slides (niittyla_ebus_order_2027.pptx) carry the order, a bar chart of the 48 energies against the limit in priority "
             "order, and what the figures rest on.\n")
    L.append("1. Diesel use per weekday block over November 2025 to October 2026, litres per 100 scheduled km to one decimal "
             "(workbook sheet Blocks, column \"Diesel l/100 km\"; graded within %.1f l/100 km): %s. The 48 figures run from %.1f to "
             "%.1f; each block's figure is the litres on the fuel-card statement between the fills of every bus that ran it, "
             "spread over the blocks the dispatch log shows between those fills, so a block that shared its buses' fills with "
             "other blocks gets its own rate and not its buses' average.\n"
             % (R1_TOL, "; ".join("%s %.1f" % (c, f["diesel"][c]) for c in sorted(pk.weekday)), f["diesel_min"], f["diesel_max"]))
    L.append("2. Design-day energy per weekday block for the 2027 model, kWh to the nearest 10 (sheet Blocks, \"Design-day energy "
             "kWh\"; graded within %d kWh): %s.\n" % (E_TOL, "; ".join("%s %d" % (c, f["energy"][c]) for c in sorted(pk.weekday))))
    L.append("3. Whether each weekday block goes electric under DES-1 4.1, its design-day energy against %d kWh (85 per cent of %d kWh "
             "usable after the first winter): %s. %d blocks qualify; the %d assigned are those the night period recharges in "
             "priority order (sheet Blocks, \"Qualifies\" and \"Assigned 2027\").\n"
             % (round(g["limit"]), round(f["usable_y1"]), "; ".join("%s %s" % (c, f["verdict"][c]) for c in sorted(pk.weekday)),
                f["qualifying_count"], f["call_count"]))
    L.append("4. The share of usable battery the company's own electric buses lose for good in their first twelve months in service: "
             "%.1f per cent (sheet Order; graded within the band %.1f to %.1f that the curved age forms span). Usable battery for "
             "planning %d kWh, limit %d kWh.\n" % (f["loss_pct"], LOSS_BAND[0], LOSS_BAND[1], round(f["usable_y1"]), round(g["limit"])))
    L.append("5. Energy the depot would have to deliver at the connection point on the design night to recharge every weekday "
             "block that passes the limit: %.1f MWh for the %d qualifying blocks (sheet Night; graded within %.1f MWh), %.1f MWh "
             "into the batteries at the charging efficiency of %.2f the sessions show. The night period's %d kW delivers at most "
             "%.2f MWh between 21:00 and 07:00, which is why the plan's list is cut at %d buses (%.1f MWh at the connection point "
             "for those).\n"
             % (f["demand_mwh"], f["qualifying_count"], NIGHT_TOL, f["demand_battery_mwh"], f["eta"], f["supply_kw"],
                f["night_capacity_mwh"], f["call_count"], f["night_mwh"]))
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
    L.append("## Step-by-Step\n")
    steps = [
        "Clean and join the operating records: the dispatch log's block codes before 11 August 2025 to the register's current "
        "codes and its early-2024 registrations to fleet numbers; the fuel-card statement's cards to vehicles by the register's "
        "validity dates, the night shift's spare cards by the fleet number typed at the pump; the telematics days the portal "
        "uploaded twice dropped; blank ambient readings filled from the airport station (the town station less its %.2f C offset "
        "where the airport has its April 2023 gap); the charging sessions' UTC stamps read against the local timetable." % f["weather_offset"],
        "Diesel use per block (ask 1): for each diesel bus, consecutive diesel fills on the statement with a second swipe within "
        "twelve minutes merged into one fill; the litres of each fill are the fuel burnt on the bus-days the dispatch log shows "
        "between that fill and the one before, by departure time; over November 2025 to October 2026 the litres of every interval "
        "are regressed on the scheduled kilometres each block contributed to it, giving one rate per block (%.1f to %.1f "
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
        "Carrying the pilot's fit on kilometres, climb and timetable speed, with the pilot's own cold response read at -15 C, puts "
        "the hard blocks %d kWh light on average and orders %d." %
        (f["bridge"]["blocks"], f["bridge"]["a"], f["bridge"]["b"], f["bridge"]["rmse"], f["heat_new_kw"],
         r10(float(np.mean([g["E"][c] for c in pk.weekday])) - float(np.mean([v for v in f["careful_energy"].values()]))), f["careful_count"]),
        "The limit (asks 3 and 4): each electric bus-day's energy over its state-of-charge drop is the capacity the battery system "
        "shows; on age in service with a cold term and a level per bus, a form with a fast early loss and a steady loss after it "
        "(curved %.2f, square root %.2f, log %.2f per cent; a straight line in age %.2f) gives %.1f per cent in the first twelve "
        "months, %d kWh usable on the 2027 model and a limit of %d kWh; %d blocks pass it." %
        (f["loss_forms"]["curved"], f["loss_forms"]["sqrt"], f["loss_forms"]["log"], f["loss_forms"]["linear"], f["loss_pct"],
         round(f["usable_y1"]), round(g["limit"]), f["qualifying_count"]),
        "The night (ask 5 and the order): the %d qualifying blocks need %.1f MWh at the connection point (their energies over the "
        "charging efficiency the sessions show, %.2f), against at most %.2f MWh the night period's %d kW can deliver between 21:00 "
        "and 07:00. Taken in the fleet plan's priority order, each between its return and its departure inside the night period at "
        "up to 150 kW a bus and %d kW in all, the list is cut at %s, the %dth, which the night cannot recharge together with the "
        "%d above it under any schedule (the night's maximum flow over the blocks' windows falls short of it; a least-slack schedule "
        "recharges the %d). The six pilot buses enter neither figure: "
        "DES-1 4.3 orders one bus for each block assigned and 4.2 tests the night on the assigned blocks, so whatever they do after "
        "the new buses arrive moves neither the count nor the night. Summing the per-block verdicts orders %d; scheduling on battery "
        "energy without the charging losses orders %d. With the quoted capacity in place of the first winter's usable no block "
        "changes side, so the loss is reported for the limit it sets and moves no verdict." %
        (f["qualifying_count"], f["demand_mwh"], f["eta"], f["night_capacity_mwh"], f["supply_kw"], f["supply_kw"], f["refused_block"],
         f["call_count"] + 1, f["call_count"], f["call_count"],
         f["routes"]["the per-block verdicts summed, the night's supply ignored"],
         f["routes"]["the night scheduled on battery energy (charging losses ignored)"]),
        "Why no other conclusion survives: the pilot's own fit carried on the timetable's covariates and the pilot's cold response "
        "orders %d (%d without the night's supply) and the pilot's cold-day consumption times kilometres orders %d; putting the "
        "diesel bridge right alone orders %d and the heaters' share right alone orders %d; only both together, with the first "
        "winter's loss, the charging losses and the night's capacity, land %d." %
        (f["careful_count"], f["routes"]["the careful pass without the night's supply"], f["quick_count"],
         f["routes"]["the pilot's cold response read as the new buses' (the fuel heaters' share left out)"],
         f["routes"]["the pilot's fit carried on kilometres, climb and speed (the diesel bridge left out)"], f["call_count"]),
    ]
    for i, s in enumerate(steps, 1):
        L.append("%d. %s\n" % (i, s))
    open(path, "w", encoding="utf-8").write("\n".join(L))
