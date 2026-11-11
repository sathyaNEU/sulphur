"""The files under target/, written the way each of Niittylä's systems exports them: the fuel-card provider's
statement, the dispatch log, the planner's block register, the vehicle register with its fuel cards, the electric
buses' telematics summary, the charging system's sessions (UTC), the weather station's daily series, the workshop's
work orders, the 2027 fleet plan, and two ordinary files the task never needs (tyre and brake costs, the depot's
electricity invoices). Each carries the mess its own process makes and nothing placed for a result."""
import datetime as dt
import os
import sys

import numpy as np
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

import params as P
import sim

FILES = {
    "fuel": "fuel_card_transactions_2024-01_2026-10.csv",
    "dispatch": "depot_dispatch_log_2024-01_2026-10.csv",
    "blocks": "block_register_2026.xlsx",
    "vehicles": "vehicle_register_2026.xlsx",
    "ebus": "ebus_telematics_daily_2025-03_2026-10.csv",
    "sessions": "depot_charging_sessions_2025-03_2026-10.csv",
    "weather": "weather_vehkasalo_daily_2016_2026.csv",
    "workshop": "workshop_orders_2024-01_2026-10.csv",
    "standard": "depot_electrification_standard_DES-1.pdf",
    "agreement": "charging_connection_agreement_2025.pdf",
    "quote": "ebus_quotation_2027.pdf",
    "plan": "fleet_plan_2027.xlsx",
    "tyres": "tyre_and_brake_costs_2025.xlsx",
    "power": "depot_electricity_invoices_2025-01_2026-10.csv",
}
DISTRACTORS = ["tyres", "power"]
STATIONS = {9001: ("VLO Niittylä varikko", "depot"), 1123: ("Tankki Oy Vehkasalo Kehätie", "street"),
            1187: ("Tankki Oy Ristinmäki", "street"), 1409: ("Huoltamo Lehtinen Asematie", "street")}
PRODUCT = {("depot", "DIESEL"): "DIESEL", ("depot", "HVO"): "HVO", ("depot", "ADBLUE"): "ADBLUE",
           ("street", "DIESEL"): "Diesel B7", ("street", "HVO"): "HVO100", ("street", "ADBLUE"): "AdBlue 20 l"}


def dst(d):
    """Finnish summer time: from the last Sunday of March 01:00 UTC to the last Sunday of October 01:00 UTC"""
    def last_sunday(y, m):
        x = dt.date(y, m, 31) if m in (3, 10) else None
        while x.weekday() != 6:
            x -= dt.timedelta(days=1)
        return x
    return last_sunday(d.year, 3) <= d < last_sunday(d.year, 10)


def to_utc(d, minute):
    """local date and minutes from midnight (may exceed 1440) to a UTC datetime"""
    local = dt.datetime(d.year, d.month, d.day) + dt.timedelta(minutes=int(minute))
    off = 3 if dst(local.date()) else 2
    return local - dt.timedelta(hours=off)


def hhmm(minute):
    m = int(minute) % 1440
    return "%02d:%02d" % (m // 60, m % 60)


def local_stamp(d, minute):
    t = dt.datetime(d.year, d.month, d.day) + dt.timedelta(minutes=int(minute))
    return t.strftime("%Y-%m-%d %H:%M")


# ----------------------------------------------------------------------------------------------- csv
def write_fuel(w, path, rng):
    buses = {b["fleet_no"]: b for b in w["buses"]}
    reg_of = {b["fleet_no"]: b["reg"] for b in w["buses"]}
    spares = [c["card"] for c in w["cards"] if c["kind"].startswith("spare")]
    # the odometer each bus carries, advanced by its actual kilometres day by day
    odo = {b["fleet_no"]: float(rng.integers(180000, 760000)) if b["drive"] == "diesel" else float(rng.integers(300, 900))
           for b in w["buses"]}
    km_by_day = {}
    for r in w["roster"]:
        km_by_day[(r["fleet_no"], r["date"])] = r["km"] * float(rng.normal(1.015, 0.010))
    # advance odometers in date order, and read them off at each fill
    fills = sorted(w["fills"], key=lambda f: (f["date"], f["minute"], f["fleet_no"]))
    rows = []
    receipt = {sid: int(rng.integers(100000, 400000)) for sid in STATIONS}
    month_price = {}
    tid = 51000000 + int(rng.integers(0, 90000))
    last_odo_typed = {}
    cur = None
    day_km_done = set()
    for f in fills:
        d = f["date"]
        if cur != d:
            # advance every bus's odometer by the kilometres of the days up to and including today
            for (fn, dd), km in km_by_day.items():
                if dd <= d and (fn, dd) not in day_km_done:
                    odo[fn] += km
                    day_km_done.add((fn, dd))
            cur = d
        fn = f["fleet_no"]
        where = f["where"]
        sid = 9001 if where == "depot" else int(rng.choice([1123, 1187, 1409], p=[.5, .3, .2]))
        prod = PRODUCT[(where, f["product"])]
        key = (d.year, d.month, f["product"], where)
        if key not in month_price:
            base = {"DIESEL": 1.72, "HVO": 2.18, "ADBLUE": 0.88}[f["product"]]
            month_price[key] = base * (1 + 0.09 * np.sin(2 * np.pi * (d.year * 12 + d.month) / 19.0)) * (1.05 if where == "street" else 1.0) \
                * (1 + rng.normal(0, 0.012))
        price = month_price[key] * (1 + rng.normal(0, 0.004))
        card = sim.card_for(w["cards"], fn, d)
        entered = ""
        if where == "depot" and f["product"] == "ADBLUE":
            card = str(rng.choice(spares))
            entered = str(fn)
            if rng.uniform() < 0.005:
                s = list(entered)
                i = int(rng.integers(1, 3))
                s[i], s[i + 1] = s[i + 1], s[i]
                entered = "".join(s)
        u = rng.uniform()
        true_odo = int(odo[fn])
        if u < 0.90:
            typed = str(true_odo)
        elif u < 0.94:
            typed = ""
        elif u < 0.97:
            typed = str(last_odo_typed.get(fn, true_odo - int(rng.integers(300, 900))))
        else:
            s = list(str(true_odo))
            i = int(rng.integers(0, len(s) - 1))
            s[i], s[i + 1] = s[i + 1], s[i]
            typed = "".join(s)
        if f["product"] == "ADBLUE" and rng.uniform() < 0.5:
            typed = ""
        if typed and typed != "":
            last_odo_typed[fn] = int(typed) if typed.isdigit() else true_odo
        receipt[sid] += int(rng.integers(1, 5))
        tid += int(rng.integers(1, 4))
        litres = round(float(f["litres"]), 2)
        if prod == "AdBlue 20 l":
            litres = 20.0
        rows.append({"statement_line": tid, "card_no": card, "transaction_time": local_stamp(d, f["minute"]),
                     "station_id": sid, "station_name": STATIONS[sid][0], "product": prod, "litres": litres,
                     "unit_price_eur": round(price, 3), "amount_eur": round(litres * price, 2),
                     "odometer_km": typed, "vehicle_entered": entered, "receipt_no": "%d-%d" % (sid, receipt[sid])})
    df = pd.DataFrame(rows)
    df = df.sort_values(["transaction_time", "statement_line"]).reset_index(drop=True)
    # the provider's statement closes at the end of October: a fill after midnight on the last night falls in November's
    df = df[df["transaction_time"] <= "2026-10-31 23:59"].reset_index(drop=True)
    df.to_csv(path, index=False)
    return len(df)


def write_dispatch(w, path, rng):
    reg_of = {b["fleet_no"]: b["reg"] for b in w["buses"]}
    byc = {b["code"]: b for b in w["blocks"]}
    rows = []
    drivers = {}
    for r in w["roster"]:
        d = r["date"]
        b = byc[r["code"]]
        code = b["old_code"] if d < P.NEW_CODES_FROM else b["code"]
        veh = reg_of[r["fleet_no"]] if d < dt.date(2024, 3, 1) else str(r["fleet_no"])
        key = (r["code"], d.weekday())
        if key not in drivers or rng.uniform() < 0.25:
            drivers[key] = "K%04d" % int(rng.integers(1100, 1480))
        remark = ""
        if rng.uniform() < 0.004:
            remark = str(rng.choice(["late departure, driver change", "diversion Keskuskatu roadworks", "replacement bus from 13:10",
                                     "school day extra trip", "reduced timetable (snow)"]))
        rows.append({"operating_date": d.isoformat(), "block": code, "vehicle": veh, "driver": drivers[key],
                     "planned_km": r["km"], "depot_departure": hhmm(b["dep"]), "depot_return": hhmm(b["ret"]),
                     "remark": remark})
    df = pd.DataFrame(rows).sort_values(["operating_date", "block"]).reset_index(drop=True)
    df.to_csv(path, index=False)
    return len(df)


def write_ebus(w, path, rng):
    rows = []
    for r in w["ebus_days"]:
        d = r["date"]
        amb = round(r["t"] + 0.6 + float(rng.normal(0, 0.7)), 1)
        if rng.uniform() < 0.03:
            amb = ""
        moving = round(r["hours"] * float(rng.uniform(0.62, 0.74)), 2)
        rows.append({"vehicle": r["fleet_no"], "date": d.isoformat(), "distance_km": round(r["km"] * float(rng.normal(1.0, 0.008)), 1),
                     "energy_used_kwh": round(r["energy"] * (1 + float(rng.normal(0, 0.01))), 1),
                     "hvac_kwh": round(r["hvac"] * (1 + float(rng.normal(0, 0.02))), 1),
                     "soc_start_pct": int(r["soc0"]), "soc_end_pct": int(round(r["soc1"])),
                     "ambient_mean_c": amb, "moving_h": moving, "idle_h": round(r["hours"] - moving, 2),
                     "max_speed_kmh": int(rng.integers(52, 84)) if r["code"][0] != "M" or True else 0})
    df = pd.DataFrame(rows)
    # the portal uploaded four days twice after its outage of May 2026
    dup = df[(df["date"] >= "2026-05-11") & (df["date"] <= "2026-05-14")]
    df = pd.concat([df, dup]).sort_values(["date", "vehicle"]).reset_index(drop=True)
    df.to_csv(path, index=False)
    return len(df)


def write_sessions(w, path, rng):
    # the charging system numbers every session on every outlet, the workshop's two outlets included, so the
    # exported bus sessions carry gaps in the numbering
    gaps = np.cumsum(rng.integers(1, 4, size=len(w["sessions"]) + 1))
    sess_no = lambda sid: int(140000 + gaps[sid])
    rows = []
    for s in w["sessions"]:
        d = s["date"]
        start = s["start"]
        hours_needed = s["recharge_kwh"] / (P.CHARGER_KW * 0.97)
        end = min(start + int(hours_needed * 60) + int(rng.integers(5, 40)), s["plug_out"] - 2)
        rows.append({"session_id": "S%07d" % sess_no(s["sid"]), "outlet": s["outlet"], "vehicle": s["fleet_no"],
                     "plug_in_utc": to_utc(d, s["plug_in"]).strftime("%Y-%m-%dT%H:%M:%SZ"),
                     "charge_start_utc": to_utc(d, start).strftime("%Y-%m-%dT%H:%M:%SZ"),
                     "charge_end_utc": to_utc(d, end).strftime("%Y-%m-%dT%H:%M:%SZ"),
                     "plug_out_utc": to_utc(d, s["plug_out"]).strftime("%Y-%m-%dT%H:%M:%SZ"),
                     "energy_kwh": round(s["kwh"], 1), "soc_in_pct": int(round(s["soc_in"])), "soc_out_pct": int(s["soc_out"])})
    df = pd.DataFrame(rows).sort_values("plug_in_utc").reset_index(drop=True)
    df.to_csv(path, index=False)
    return len(df)


def write_weather(w, path, rng):
    rows = []
    for d, t in sorted(w["temps"].items()):
        ta = t["airport"]
        spread = float(rng.uniform(3, 9))
        rows.append({"date": d.isoformat(), "t_mean_airport_c": "" if ta is None else ta,
                     "t_min_airport_c": "" if ta is None else round(ta - spread * 0.55, 1),
                     "t_max_airport_c": "" if ta is None else round(ta + spread * 0.45, 1),
                     "t_mean_keskusta_c": t["city"], "precip_mm": round(max(0.0, float(rng.gamma(0.6, 2.4)) - 0.8), 1)})
    pd.DataFrame(rows).to_csv(path, index=False)
    return len(rows)


DESC = {"brakes": ["Brake pads front, rotors measured", "Brake pads rear", "Brake fluid, ABS sensor", "Handbrake adjustment"],
        "tyres": ["Tyre change (winter)", "Tyre change (summer)", "Puncture repair rear left", "Wheel alignment"],
        "doors": ["Door 2 sensor", "Door 1 cylinder", "Door seals", "Ramp motor"],
        "electrical": ["Battery 24 V replaced", "Destination sign controller", "Tachograph calibration", "Alternator"],
        "body": ["Mirror replaced", "Rear bumper repair", "Windscreen chip", "Wheel arch corrosion"],
        "engine": ["Oil service", "EGR valve", "Turbo hose", "Coolant leak", "Injector 3"],
        "exhaust": ["DPF regeneration", "AdBlue dosing unit", "NOx sensor", "SCR fault"],
        "hvac": ["Cabin heater service", "Compressor clutch", "Blower motor", "Thermostat"],
        "service": ["Periodic service A", "Periodic service B", "Annual inspection", "Lubrication"],
        "hv-battery check": ["HV battery insulation check", "HV coolant top-up", "Cell balancing report", "HV isolation test"]}


def write_workshop(w, path, rng):
    rows = []
    for o in sorted(w["workshop"], key=lambda o: (o["opened"], o["wo"])):
        desc = o["note"] or str(rng.choice(DESC[o["category"]]))
        rows.append({"work_order": o["wo"], "vehicle": o["fleet_no"], "opened": o["opened"].isoformat(),
                     "closed": o["closed"].isoformat(), "category": o["category"], "labour_h": o["hours"], "description": desc})
    pd.DataFrame(rows).to_csv(path, index=False)
    return len(rows)


def write_power(w, path, rng):
    """the depot's electricity invoices: the whole connection (workshop, offices, lighting, charging)"""
    rows = []
    d = dt.date(2025, 1, 1)
    sess = pd.DataFrame(w["sessions"])
    sess["ym"] = [(s.year, s.month) for s in sess["date"]]
    charge = sess.groupby("ym")["kwh"].sum().to_dict()
    while d <= dt.date(2026, 10, 1):
        doy = d.timetuple().tm_yday
        base = 38000 + 14000 * np.cos(2 * np.pi * (doy - 15) / 365.25) + float(rng.normal(0, 1800))
        ch = charge.get((d.year, d.month), 0.0)
        kwh = base + ch
        price = 0.118 + 0.02 * np.cos(2 * np.pi * (doy - 15) / 365.25) + float(rng.normal(0, 0.004))
        rows.append({"invoice_month": "%04d-%02d" % (d.year, d.month), "meter": "VLO-NIITTYLA-1", "energy_kwh": int(round(kwh)),
                     "peak_kw": int(round(max(220, 180 + ch / 300 + float(rng.normal(0, 25))))),
                     "energy_eur": round(kwh * price, 2), "network_eur": round(2650 + 0.9 * max(220, 180 + ch / 300), 2)})
        d = (d.replace(day=28) + dt.timedelta(days=4)).replace(day=1)
    pd.DataFrame(rows).to_csv(path, index=False)
    return len(rows)


# ----------------------------------------------------------------------------------------------- xlsx
def _head(ws, row, fill="DDE4EE"):
    for c in ws[row]:
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor=fill)
        c.alignment = Alignment(wrap_text=True, vertical="top")


def _widths(ws, widths):
    for i, wd in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = wd


LINE_NAMES = {1: "Keskusta - Niittylä", 2: "Rautatieasema - Ristinmäki", 3: "Keskusta - Sairaala - Honkala", 4: "Lehtola - Keskusta - Kalliola",
              5: "Keskusta - Vehkaniemi", 6: "Asema - Yliopisto - Keskusta", 7: "Keskusta - Mäntylä", 8: "Keskusta - Satama - Lehtola",
              9: "Honkala - Keskusta - Rinteelä", 10: "Keskusta - Kaupunginsairaala", 11: "Niittylä - Keskusta - Vehkaniemi", 12: "Rinteelä - Asema",
              14: "Keskusta - Peltokangas", 15: "Keskusta - Haukilahti", 16: "Asema - Koivuranta", 17: "Keskusta - Ruokola", 18: "Keskusta - Lintuniemi",
              19: "Asema - Kuusimäki", 21: "Keskusta - Saarela", 22: "Keskusta - Harjula",
              31: "Vehkasalo - Pihlajavesi", 32: "Vehkasalo - Kivijärvi", 33: "Vehkasalo - Taipale", 34: "Vehkasalo - Mustalahti", 35: "Vehkasalo - Ahvenlampi",
              36: "Vehkasalo - Rautakylä", 37: "Vehkasalo - Nurmela", 38: "Vehkasalo - Kalliokoski"}


def write_blocks(w, path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Blocks"
    ws.append(["Block", "Code to 10.8.2025", "Day type", "Lines", "Trips", "Scheduled km (from 11.8.2025)",
               "Scheduled km (to 10.8.2025)", "Depot departure", "Depot return", "Hours out", "Climb m/km", "Zone"])
    _head(ws, 1)
    for b in sorted(w["blocks"], key=lambda b: b["code"]):
        ws.append([b["code"], b["old_code"], {"M": "Mon-Fri", "L": "Sat", "S": "Sun/holiday"}[b["daytype"]],
                   ", ".join(str(l) for l in b["lines"]), b["trips"], b["km"], b["km_old"], hhmm(b["dep"]), hhmm(b["ret"]),
                   b["hours"], b["climb"], b["zone"]])
    _widths(ws, [8, 16, 11, 10, 7, 14, 14, 11, 11, 9, 10, 6])
    ws.freeze_panes = "A2"
    ws2 = wb.create_sheet("Lines")
    ws2.append(["Line", "Route", "Zone", "Length km (one way)"])
    _head(ws2, 1)
    rng = np.random.default_rng(P.SEED + 77)
    for ln, name in LINE_NAMES.items():
        zone = 1 if ln <= 12 else (2 if ln < 30 else 3)
        ws2.append([ln, name, zone, round(float(rng.uniform(5, 9) if zone == 1 else rng.uniform(9, 16) if zone == 2 else rng.uniform(22, 48)), 1)])
    _widths(ws2, [6, 34, 6, 14])
    wb.save(path)


def write_vehicles(w, path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Vehicles"
    ws.append(["Fleet no", "Registration", "Make and model", "Drive", "Year", "Length m", "Seats", "Fuel tank l",
               "Traction battery kWh (usable, new)", "Cabin heating", "In service from", "Withdrawn"])
    _head(ws, 1)
    for b in sorted(w["buses"], key=lambda b: b["fleet_no"]):
        ws.append([b["fleet_no"], b["reg"], b["make_model"], b["drive"], b["year"], b["length_m"], b["seats"], b["tank_l"],
                   b["battery_kwh"], b["heater"], b["in_service_from"], b["retired"]])
    for row in ws.iter_rows(min_row=2):
        for c in (row[10], row[11]):
            c.number_format = "yyyy-mm-dd"
    _widths(ws, [9, 13, 22, 9, 6, 9, 6, 10, 14, 44, 13, 12])
    ws.freeze_panes = "A2"
    ws2 = wb.create_sheet("Fuel cards")
    ws2.append(["Card no", "Vehicle (fleet no)", "Valid from", "Valid to", "Type"])
    _head(ws2, 1)
    for c in sorted(w["cards"], key=lambda c: (c["fleet_no"] or 9999, c["valid_from"])):
        ws2.append([c["card"], c["fleet_no"], c["valid_from"], c["valid_to"], "vehicle card" if c["kind"] == "vehicle" else "night shift %s" % c["kind"]])
    for row in ws2.iter_rows(min_row=2):
        for c in (row[2], row[3]):
            c.number_format = "yyyy-mm-dd"
    _widths(ws2, [18, 12, 12, 12, 16])
    wb.save(path)


def write_plan(w, path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Weekday blocks 2027"
    ws.append(["Priority", "Block", "Lines", "Scheduled km", "Depot departure", "Depot return", "Zone", "Note"])
    _head(ws, 1)
    notes = {1: "centre lines, low-emission zone from 2027", 2: "", 3: ""}
    for b in sorted([b for b in w["blocks"] if b["daytype"] == "M"], key=lambda b: b["priority"]):
        ws.append([b["priority"], b["code"], ", ".join(str(l) for l in b["lines"]), b["km"], hhmm(b["dep"]), hhmm(b["ret"]),
                   b["zone"], notes[b["zone"]] if b["priority"] in (1, 19, 35) else ""])
    _widths(ws, [9, 8, 10, 12, 12, 12, 6, 40])
    ws.freeze_panes = "A2"
    ws2 = wb.create_sheet("Charging")
    ws2.append(["Item", "Status", "Note"])
    _head(ws2, 1)
    for r in (["Outlets, 150 kW, cabinets C1 to C3", "6 in use since 2/2025", "pilot buses 1201 to 1206"],
              ["Outlets, 150 kW, cabinets C4 to C16", "ordered, in use by 8/2027", "26 further outlets, the 2027 to 2029 rollout"],
              ["Workshop outlets, 22 kW AC", "2, bay 3", "buses under repair"],
              ["Connection capacity", "per the 2025 connection agreement", "reinforcement applied for, earliest 2028"],
              ["Depot layout", "charging lane B, 32 bays", ""]):
        ws2.append(r)
    _widths(ws2, [36, 32, 44])
    ws3 = wb.create_sheet("Timetable 2027")
    ws3.append(["Change", "From", "Note"])
    _head(ws3, 1)
    for r in (["Winter timetable 2027", "2027-01-11", "weekday blocks as the 2026 autumn timetable"],
              ["Summer timetable 2027", "2027-06-07", "to be planned in spring"],
              ["Line 8 to Satama hourly", "2027-01-11", "within block kilometres as listed"],
              ["Buses 1201 to 1206 move to Kauppala depot", "2027-01-11", "for Kauppala's regional and school lines; the city's 2027 terms exclude fuel-fired heaters"]):
        ws3.append(r)
    _widths(ws3, [30, 12, 44])
    wb.save(path)


def write_tyres(w, path, rng):
    wb = Workbook()
    ws = wb.active
    ws.title = "2025"
    ws.append(["Fleet no", "Tyres EUR", "Brake pads EUR", "Brake rotors EUR", "Km 2025", "EUR per 1000 km"])
    _head(ws, 1)
    roster = pd.DataFrame(w["roster"])
    roster = roster[(roster["date"] >= dt.date(2025, 1, 1)) & (roster["date"] <= dt.date(2025, 12, 31))]
    km = roster.groupby("fleet_no")["km"].sum().to_dict()
    for b in sorted(w["buses"], key=lambda b: b["fleet_no"]):
        k = km.get(b["fleet_no"], 0)
        if k == 0:
            continue
        ty = float(rng.uniform(2600, 5200)) * k / 60000
        bp = float(rng.uniform(900, 2100)) * k / 60000
        br = float(rng.uniform(0, 2400)) * k / 60000
        ws.append([b["fleet_no"], round(ty), round(bp), round(br), int(k), round((ty + bp + br) / k * 1000, 1)])
    _widths(ws, [9, 11, 14, 15, 10, 14])
    wb.save(path)


def write_tables(w, target):
    rng = np.random.default_rng(P.SEED + 11)
    F = {k: os.path.join(target, v) for k, v in FILES.items()}
    n = {}
    n["fuel"] = write_fuel(w, F["fuel"], np.random.default_rng(P.SEED + 12))
    n["dispatch"] = write_dispatch(w, F["dispatch"], np.random.default_rng(P.SEED + 13))
    n["ebus"] = write_ebus(w, F["ebus"], np.random.default_rng(P.SEED + 14))
    n["sessions"] = write_sessions(w, F["sessions"], np.random.default_rng(P.SEED + 15))
    n["weather"] = write_weather(w, F["weather"], np.random.default_rng(P.SEED + 16))
    n["workshop"] = write_workshop(w, F["workshop"], np.random.default_rng(P.SEED + 17))
    n["power"] = write_power(w, F["power"], np.random.default_rng(P.SEED + 18))
    write_blocks(w, F["blocks"])
    write_vehicles(w, F["vehicles"])
    write_plan(w, F["plan"])
    write_tyres(w, F["tyres"], np.random.default_rng(P.SEED + 19))
    return n
