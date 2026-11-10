"""Write the data files of the pack from the clean truth, with the mess the haulier's systems produce: the Varnamo
weighbridge log, the battery-electric tractors' daily summaries, the Jonkoping TMS consignments, the route, fleet and
shipper registers, the 2027 shortlist, the daily temperatures, and the two files the call never reads (the Varnamo
fuel card statement and the workshop log)."""
import csv
import datetime as dt
import math

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

import params as P
import sim

FILES = {
    "weighbridge": "weighbridge_varnamo_2024-11_2026-10.csv",
    "bev": "bev_daily_summary_2025-03_2026-10.csv",
    "tms": "tms_consignments_jonkoping_2025-2026.csv",
    "tmsv": "tms_consignments_varnamo_2025-11_2026-10.csv",
    "routes": "route_register_2026.xlsx",
    "fleet": "fleet_register_2026.xlsx",
    "shippers": "shipper_register_2026.xlsx",
    "plan": "fleet_plan_2027.xlsx",
    "temps": "daily_mean_temperature_2016-2026.csv",
    "standard": "fleet_electrification_standard_FES-2.pdf",
    "quote": "quotation_bev_tractors_2027.pdf",
    "fuel": "fuel_card_statement_varnamo_2025-2026.csv",
    "workshop": "workshop_log_2025-2026.csv",
}
DISTRACTORS = ["fuel", "workshop"]
OTHER_TOWNS = ["Jönköping", "Växjö", "Halmstad", "Borås", "Ljungby", "Helsingborg", "Malmö", "Göteborg", "Kalmar",
               "Norrköping", "Linköping", "Karlshamn", "Hässleholm", "Lund", "Falkenberg", "Vetlanda", "Örebro",
               "Eskilstuna", "Kungsbacka", "Landskrona", "Trelleborg", "Ystad", "Nybro", "Tranås", "Värnamo",
               "Mölndal", "Skövde", "Laholm", "Olofström", "Älmhult", "Markaryd", "Hultsfred"]
LETTERS = "ABCDEFGHJKLMNOPRSTUWXYZ"


def reg(rng):
    s = "".join(LETTERS[int(rng.integers(0, len(LETTERS)))] for _ in range(3))
    tail = "%02d" % int(rng.integers(10, 99))
    last = LETTERS[int(rng.integers(0, len(LETTERS)))] if rng.random() < 0.35 else str(int(rng.integers(0, 10)))
    return "%s %s%s" % (s, tail, last)


def fleet(w):
    rng = np.random.default_rng(P.SEED + 30)
    bev = {t: reg(rng) for t in P.PILOT_TRACTORS}
    diesel_j = {"D-1%02d" % k: reg(rng) for k in range(1, 6)}
    diesel_v = {"D-2%02d" % k: reg(rng) for k in range(1, 47)}
    trailers = {t: reg(rng) for t in sorted(w["trailers"])}
    tare = {t: int(round(8150 + 950 * rng.random(), -1)) for t in diesel_v}
    tare.update({t: int(round(8150 + 950 * rng.random(), -1)) for t in diesel_j})
    ttare = {t: w["trailers"][t]["tare"] for t in trailers}
    return bev, diesel_j, diesel_v, trailers, tare, ttare


def write_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f, lineterminator="\r\n")
        wr.writerow(header)
        wr.writerows(rows)
    return len(rows)


def write_weighbridge(w, path, fl):
    bev, dj, dv, trailers, tare, ttare = fl
    rng = np.random.default_rng(P.SEED + 31)
    tlist = sorted(trailers)
    duty_tr = {c: "D-2%02d" % int(c[1:]) for c in ["V%02d" % k for k in range(1, 47)]}
    rows = []
    onb = {}
    n = 400100
    for x in sorted(w["depart"], key=lambda r: (r["date"], r["hour"], r["duty"])):
        d = x["date"]
        tr = duty_tr[x["duty"]]
        if rng.random() < 0.03:   # a spare tractor on the duty
            tr = "D-2%02d" % int(rng.integers(1, 47))
        tl = x["trailer"]
        rng.integers(0, len(tlist))
        net = int(round(x["payload"] * 1000 / 20)) * 20
        t_kg = tare[tr] + ttare[tl]
        duty = x["duty"] if d >= P.TMS_UPGRADE else "VMO-%s" % x["duty"][1:]
        dec = "" if rng.random() < 0.012 else str(x["declared"])
        cmr = "%s%07d" % (x["shipper"], int(rng.integers(1000000, 9999999)))
        onb[id(x)] = (dec, dv[tr])
        hh = x["hour"]
        stamp = dt.datetime.combine(d, dt.time(0)) + dt.timedelta(hours=hh)
        if rng.random() < 0.021:   # first weighing over an axle limit, part reload, weighed again
            first = net + int(round(rng.normal(900, 300) / 20)) * 20
            n += 1
            rows.append([n, stamp.strftime("%Y-%m-%d %H:%M"), "VMO-1", dv[tr], trailers[tl], duty, x["shipper"], cmr,
                         dec, t_kg + first, t_kg, "axle 2 over"])
            stamp += dt.timedelta(minutes=int(rng.integers(18, 55)))
        n += 1
        rows.append([n, stamp.strftime("%Y-%m-%d %H:%M"), "VMO-1", dv[tr], trailers[tl], duty, x["shipper"], cmr, dec,
                     t_kg + net, t_kg, ""])
    return write_csv(path, ["weighing_no", "weighed_at", "bridge", "tractor_reg", "trailer_reg", "duty", "shipper",
                            "cmr_no", "declared_kg", "gross_kg", "tare_kg", "remark"], rows), onb


def write_bev(w, path, fl):
    bev = fl[0]
    rng = np.random.default_rng(P.SEED + 32)
    rows = []
    swap = {}
    for x in w["pilot"]:
        d = x["date"]
        tr = x["tractor"]
        trips = x["trips"]
        km = sum(t["km"] for t in trips) * (1 + rng.normal(0, 0.006))
        e = sum(t["kwh"] for t in trips)
        tm = float(np.mean([t["t"] for t in trips]))
        off = 2 if dt.date(d.year, 3, 31) - dt.timedelta(days=(dt.date(d.year, 3, 31).weekday() + 1) % 7) <= d < \
            dt.date(d.year, 10, 31) - dt.timedelta(days=(dt.date(d.year, 10, 31).weekday() + 1) % 7) else 1
        t0 = dt.datetime.combine(d, dt.time(0)) + dt.timedelta(hours=trips[0]["start_h"] - off)
        t1 = dt.datetime.combine(d, dt.time(0)) + dt.timedelta(hours=trips[-1]["end_h"] - off)
        drive = sum(t["km"] / t["speed"] for t in trips)
        soc0 = 96 + int(rng.integers(0, 5))
        soc1 = soc0 - 100 * e / x["cap"]
        tmin = min(t["t"] for t in trips) - abs(rng.normal(1.0, 0.5))
        tmax = max(t["t"] for t in trips) + abs(rng.normal(0.8, 0.4))
        drop = rng.random() < 0.045
        row = [bev[tr], tr, d.isoformat(), t0.strftime("%Y-%m-%dT%H:%M:%SZ"), t1.strftime("%Y-%m-%dT%H:%M:%SZ"),
               "%.1f" % km, "%.1f" % e, soc0, "%.0f" % soc1, "" if drop else "%.1f" % tm,
               "" if drop else "%.1f" % tmin, "" if drop else "%.1f" % tmax, "%.2f" % drive,
               "%.1f" % (100 * e / km)]
        upload = t1 + dt.timedelta(minutes=int(rng.integers(3, 40)))
        rows.append(row + [upload.strftime("%Y-%m-%dT%H:%M:%SZ")])
        if rng.random() < 0.016:   # the modem reconnected and the day was uploaded again
            rows.append(row + [(upload + dt.timedelta(hours=int(rng.integers(2, 20)))).strftime("%Y-%m-%dT%H:%M:%SZ")])
    return write_csv(path, ["registration", "fleet_no", "operating_date", "first_departure_utc", "last_arrival_utc",
                            "distance_km", "energy_used_kwh", "soc_start_pct", "soc_end_pct", "ambient_mean_c",
                            "ambient_min_c", "ambient_max_c", "driving_time_h", "consumption_kwh_per_100km",
                            "uploaded_utc"], rows)


def fmt_weight(rng, kg, code, day=None):
    r = rng.random()
    scale = code in P.SCALE_FROM and day is not None and day >= P.SCALE_FROM[code]
    if code in P.STD_LOAD or P.SHIPPERS[code][2] == "exact" or scale:
        return "%d" % kg if r < 0.7 else "%s kg" % format(kg, ",").replace(",", " ")
    if r < 0.55:
        return "%d" % kg
    if r < 0.85:
        return "%s kg" % format(kg, ",").replace(",", " ")
    return ("%.2f t" % (kg / 1000)).replace(".", ",")


GOODS = {"TEN": "Möbler", "HWP": "Wellpappförpackningar", "BMJ": "Mejeriprodukter, kyl", "VGL": "Planglas",
         "GDR": "Drycker", "LBY": "Byggvaror", "TTV": "Trävaror", "GST": "Stål", "SKB": "Ballast", "HIL": "Metallprodukter",
         "VIS": "Isolering", "BPL": "Plastprodukter", "RPA": "Lastpallar", "FGU": "Gummiprodukter", "RTR": "Trävaror",
         "ANE": "Elektronik", "KCY": "Cyklar", "GLF": "Livsmedel, kyl", "HFG": "Frukt och grönt, kyl"}


def split_declared(rng, code, dec, shares):
    """a departure's declared weight over its consignments: one note per drop, written from the order lines"""
    n = len(shares)
    if n == 1:
        return [dec]
    if code in P.STD_LOAD:
        pal = dec // P.STD_LOAD[code]
        cut = [int(round(pal * s)) for s in shares[:-1]]
        cut = [max(1, c) for c in cut]
        return [c * P.STD_LOAD[code] for c in cut] + [(pal - sum(cut)) * P.STD_LOAD[code]]
    w = np.array(shares) * (1 + rng.normal(0, 0.06, n))
    w = w / w.sum()
    parts = [int(round(dec * x / 10)) * 10 for x in w[:-1]]
    return parts + [dec - sum(parts)]


def tms_rows(rng, n0, day, dcode, vreg, treg, ship, towns, dec, shares, pal, fmt_day, pref):
    rows = []
    parts = split_declared(rng, ship, dec, shares)
    pals = [max(1, int(round(pal * s))) for s in shares]
    if ship in P.STD_LOAD:
        pals = [p // P.STD_LOAD[ship] for p in parts]
    for k, (town, part) in enumerate(zip(towns, parts)):
        rows.append(["%s%d" % (pref, n0 + k + 1), day.isoformat(), dcode, vreg, treg, ship, P.SHIPPERS[ship][1], town,
                     max(pals[k], 1), fmt_weight(rng, part, ship, fmt_day), GOODS[ship]])
    return rows


def write_tms(w, path, fl):
    bev, dj = fl[0], fl[1]
    trl = fl[3]
    rng = np.random.default_rng(P.SEED + 33)
    xr = np.random.default_rng(P.SEED + 39)
    by_day = {}
    for x in w["pilot"]:
        by_day.setdefault(x["date"], {})[x["duty"]] = x
    rows = []
    n = 2500000
    dlist = sorted(dj)
    for day in P.workdays(P.PILOT_START, P.PILOT_END):
        spare = list(dlist)
        rng.shuffle(spare)
        for dcode in sorted(P.PILOT):
            ship, legs, climb, town = P.PILOT[dcode]
            drops = P.DROPS.get(dcode)
            towns = [d[0] for d in drops] if drops else [town]
            x = by_day.get(day, {}).get(dcode)
            if x is not None:
                vreg, dec, pal, tl, shares = bev[x["tractor"]], x["declared"], x["pallets"], x["trailer"], x["shares"]
            else:
                mu, sd = P.SHIPPERS[ship][3], P.SHIPPERS[ship][4]
                pay = float(np.clip(rng.normal(mu, sd), 0.4 * mu, 1.6 * mu))
                dec = sim.declare(rng, ship, pay, day)
                pal = int(round(pay / 0.52 + rng.normal(0, 1.2)))
                vreg = dj[spare.pop()]
                pool = w["pools"][dcode]
                tl = pool[int(xr.integers(0, len(pool)))]
                shares = sim.drop_shares(xr, drops)
            if ship in P.STD_LOAD:   # the notes' pallets are the load plan's, which the declared weight counts
                pal = dec // P.STD_LOAD[ship]
            new = tms_rows(rng, n, day, dcode, vreg, trl[tl], ship, towns, dec, shares, max(pal, 8), day, "FR")
            n += len(new) + int(xr.integers(0, 4))   # the TMS numbers notes across every depot
            rows += new
    return write_csv(path, ["consignment_no", "collection_date", "duty", "vehicle_reg", "trailer_reg", "shipper",
                            "collection_site", "delivery_town", "pallets", "declared_weight", "goods"], rows)


def write_tmsv(w, path, fl, dec_on_bridge):
    """the Varnamo terminal's consignments, November 2025 to October 2026, one row per note"""
    bev, dj, dv, trl = fl[0], fl[1], fl[2], fl[3]
    rng = np.random.default_rng(P.SEED + 40)
    rows = []
    n = 6100000
    for x in sorted(w["depart"], key=lambda r: (r["date"], r["hour"], r["duty"])):
        if not (P.LAST12[0] <= x["date"] <= P.LAST12[1]):
            continue
        code = x["duty"]
        if code in P.SHORT:
            drops = P.DROPS.get(code)
            last = P.SHORT[code][2]
        else:
            drops = w["others"][code][3]
            last = OTHER_TOWNS[int(code[1:]) % len(OTHER_TOWNS)]
        towns = [d[0] for d in drops] if drops else [last]
        if drops and not drops[0][0]:
            towns = [OTHER_TOWNS[(int(code[1:]) * 7 + 3 * k + 1) % len(OTHER_TOWNS)] for k in range(len(drops) - 1)] + [last]
        duty = code if x["date"] >= P.TMS_UPGRADE else "VMO-%s" % code[1:]
        vreg = dec_on_bridge[id(x)][1]
        pal = int(round(x["payload"] / 0.52 + rng.normal(0, 1.2)))
        new = tms_rows(rng, n, x["date"], duty, vreg, trl[x["trailer"]], x["shipper"], towns, x["declared"],
                       x["shares"], max(pal, 4), x["date"], "VR")
        n += len(new) + int(rng.integers(0, 3))
        rows += new
    return write_csv(path, ["consignment_no", "collection_date", "duty", "vehicle_reg", "trailer_reg", "shipper",
                            "collection_site", "delivery_town", "pallets", "declared_weight", "goods"], rows)


def _sheet(ws, header, rows, widths=None):
    ws.append(header)
    for c in ws[1]:
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="DDE3EA")
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for r in rows:
        ws.append(r)
    for i, wd in enumerate(widths or [14] * len(header), 1):
        ws.column_dimensions[get_column_letter(i)].width = wd
    ws.freeze_panes = "A2"


def write_routes(w, path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Duties"
    rows = []
    for dcode in sorted(P.PILOT):
        ship, legs, climb, town = P.PILOT[dcode]
        rows.append([dcode, "", "Jönköping (Torsvik)", ship, P.SHIPPERS[ship][1], town, legs[0], legs[1], legs[2],
                     sum(legs), climb, "Mon-Fri", round(sum(legs) / P.PILOT_V[dcode], 2)])
    rng = np.random.default_rng(P.SEED + 34)
    vrng = np.random.default_rng(P.SEED + 38)
    for k in range(1, 47):
        c = "V%02d" % k
        if c in w["short"]:
            ship, legs, climb, m = w["short"][c][:4]
            town = P.SHORT[c][2]
        else:
            ship, legs, climb, _ = w["others"][c]
            town = OTHER_TOWNS[k % len(OTHER_TOWNS)]
        vplan = P.SHORT_V[c] if c in P.SHORT_V else float(66 + 16 * vrng.random())
        rows.append([c, "VMO-%02d" % k, "Värnamo terminal", ship, P.SHIPPERS[ship][1], town, legs[0], legs[1],
                     legs[2], sum(legs), climb, "Mon-Fri", round(sum(legs) / vplan, 2)])
    _sheet(ws, ["Duty", "Duty (before 13 Apr 2026)", "Depot", "Shipper", "Collection", "Delivery", "Depot to collection km",
                "Collection to delivery km", "Delivery to depot km", "Round trip km", "Climb m per 100 km (routing tool)", "Runs",
                "Driving time h (routing tool)"],
           rows, [8, 14, 20, 9, 14, 14, 12, 12, 12, 11, 11, 9, 12])
    # the routing tool's stop list: each duty's stops on its loaded run, km from the collection
    st = []
    for r in rows:
        c, town, b = r[0], r[5], r[7]
        if c in P.DROPS:
            drops = P.DROPS[c]
            towns = [d[0] for d in drops]
        elif c in w["others"] and w["others"][c][3]:
            drops = w["others"][c][3]
            towns = [OTHER_TOWNS[(int(c[1:]) * 7 + 3 * k + 1) % len(OTHER_TOWNS)] for k in range(len(drops) - 1)] + [town]
        else:
            drops, towns = [("", 1.0, 1.0)], [town]
        for k, (d, tw) in enumerate(zip(drops, towns)):
            st.append([c, k + 1, tw, int(round(b * d[2])) if k < len(drops) - 1 else b])
    ws2 = wb.create_sheet("Stops")
    _sheet(ws2, ["Duty", "Stop", "Town", "Km from collection (routing tool)"], st, [8, 6, 16, 14])
    wb.save(path)


def write_fleet(w, path, fl):
    bev, dj, dv, trailers, tare, ttare = fl
    wb = Workbook()
    ws = wb.active
    ws.title = "Tractors"
    rows = []
    for t in P.PILOT_TRACTORS:
        rows.append([t, bev[t], "Battery-electric 6x2 tractor", 2024, "Jönköping", "2025-02-17", "battery 600 kWh "
                     "installed, %d kWh usable" % P.PILOT_USABLE, P.PILOT_TRACTOR_TARE[t]])
    for t in sorted(dj):
        rows.append([t, dj[t], "Diesel 6x2 tractor, Euro VI", 2019 + int(t[-1]) % 4, "Jönköping", "", "", tare[t]])
    for t in sorted(dv):
        rows.append([t, dv[t], "Diesel 6x2 tractor, Euro VI", 2018 + int(t[-2:]) % 6, "Värnamo", "", "", tare[t]])
    _sheet(ws, ["Fleet no", "Registration", "Type", "Model year", "Depot", "In service", "Battery", "Tare kg"], rows,
           [9, 12, 30, 10, 12, 11, 30, 9])
    ws2 = wb.create_sheet("Trailers")
    tr = w["trailers"]
    _sheet(ws2, ["Fleet no", "Registration", "Body code", "Type", "Equipment", "Model year", "Depot", "Tare kg"],
           [[t, trailers[t], tr[t]["body"], tr[t]["text"], "; ".join(tr[t]["equip"]), tr[t]["year"], tr[t]["depot"],
             tr[t]["tare"]] for t in sorted(tr)], [9, 12, 9, 36, 40, 10, 11, 9])
    wb.save(path)


def write_shippers(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Shippers"
    rng = np.random.default_rng(P.SEED + 35)
    rows = []
    for code in sorted(P.SHIPPERS):
        name, town = P.SHIPPERS[code][0], P.SHIPPERS[code][1]
        org = "55%04d-%04d" % (int(rng.integers(1000, 9999)), int(rng.integers(1000, 9999)))
        if "ek. för." in name:
            org = "7%05d-%04d" % (int(rng.integers(10000, 99999)), int(rng.integers(1000, 9999)))
        depots = "Jönköping, Värnamo" if code in ("TEN", "HWP", "BMJ", "VGL", "GDR", "LBY") else "Värnamo"
        rows.append([code, name, org, town, depots, "30 days", "Full loads"])
    _sheet(ws, ["Code", "Shipper", "Org. no", "Site", "Served from", "Payment terms", "Service"], rows,
           [7, 28, 13, 14, 20, 12, 12])
    wb.save(path)


def write_plan(w, path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Shortlist 2027"
    rows = []
    for c in sorted(w["short"]):
        ship = w["short"][c][0]
        rows.append([c, ship, P.SHIPPERS[ship][0], P.SHORT[c][2], 5, "Värnamo terminal charger bank (from Dec 2026)"])
    _sheet(ws, ["Duty", "Shipper", "Shipper name", "Delivery", "Days a week 2027", "Charging"], rows,
           [8, 8, 28, 14, 10, 40])
    wb.save(path)


def write_temps(w, path):
    rows = []
    for d in sorted(w["temps"]):
        j, v = w["temps"][d]
        rows.append([d.isoformat(), "Jönköping", "%.1f" % j])
        rows.append([d.isoformat(), "Värnamo", "%.1f" % v])
    return write_csv(path, ["date", "station", "temperature (C)"], rows)


def write_fuel(w, path, fl):
    dv = fl[2]
    rng = np.random.default_rng(P.SEED + 36)
    rows = []
    d = dt.date(2025, 1, 2)
    stations = ["Värnamo Terminalvägen", "Gislaved", "Ljungby E4", "Jönköping Ljungarum", "Halmstad Kistinge",
                "Helsingborg Berga", "Växjö Norremark"]
    n = 0
    while d <= dt.date(2026, 10, 30):
        if d.weekday() < 5:
            for t in sorted(dv):
                if rng.random() < 0.42:
                    n += 1
                    lit = max(80.0, rng.normal(260, 70))
                    price = 17.9 + 1.4 * math.sin(n / 4000.0) + rng.normal(0, 0.15)
                    rows.append(["C%05d" % (1000 + int(t[-2:])), dv[t], d.isoformat(),
                                 "%02d:%02d" % (int(rng.integers(14, 19)), int(rng.integers(0, 60))),
                                 stations[int(rng.integers(0, len(stations)))], "Diesel MK1", "%.2f" % lit,
                                 "%.2f" % price, "%.2f" % (lit * price)])
        d += dt.timedelta(days=1)
    return write_csv(path, ["card_no", "vehicle_reg", "date", "time", "station", "product", "litres", "price_sek_l",
                            "amount_sek"], rows)


def write_workshop(w, path, fl):
    bev, dj, dv = fl[0], fl[1], fl[2]
    rng = np.random.default_rng(P.SEED + 37)
    rows = []
    jobs = ["Service A", "Service B", "Tyres, drive axle", "Tyres, steer axle", "Brake pads", "Annual inspection",
            "Tail lift repair", "Windscreen", "Air dryer", "Cab heater"]
    allv = [(t, bev[t]) for t in sorted(bev)] + [(t, dj[t]) for t in sorted(dj)] + [(t, dv[t]) for t in sorted(dv)]
    n = 0
    for fno, r in allv:
        d = dt.date(2025, 1, 1) + dt.timedelta(days=int(rng.integers(0, 60)))
        while d <= dt.date(2026, 10, 30):
            n += 1
            job = jobs[int(rng.integers(0, len(jobs)))]
            if fno.startswith("BEV") and job in ("Service A", "Service B"):
                job = "Service, battery-electric"
            hours = round(max(0.5, rng.normal(3.0, 1.5)), 1)
            rows.append(["WO-%05d" % (20000 + n), d.isoformat(), fno, r, job, hours,
                         int(round(hours * 1150 + rng.normal(2500, 1800), -1)),
                         "Värnamo" if fno.startswith("D-2") else "Jönköping"])
            d += dt.timedelta(days=int(rng.integers(35, 120)))
    rows.sort(key=lambda x: (x[1], x[0]))
    return write_csv(path, ["work_order", "date", "fleet_no", "registration", "job", "labour_h", "cost_sek",
                            "workshop"], rows)


def write_tables(w, target):
    import os
    F = {k: os.path.join(target, v) for k, v in FILES.items()}
    fl = fleet(w)
    n = {}
    n["weighbridge"], onb = write_weighbridge(w, F["weighbridge"], fl)
    n["bev"] = write_bev(w, F["bev"], fl)
    n["tms"] = write_tms(w, F["tms"], fl)
    n["tmsv"] = write_tmsv(w, F["tmsv"], fl, onb)
    write_routes(w, F["routes"])
    write_fleet(w, F["fleet"], fl)
    write_shippers(F["shippers"])
    write_plan(w, F["plan"])
    n["temps"] = write_temps(w, F["temps"])
    n["fuel"] = write_fuel(w, F["fuel"], fl)
    n["workshop"] = write_workshop(w, F["workshop"], fl)
    return n
