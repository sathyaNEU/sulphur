"""Write the data files of the pack from the clean truth: the handheld stop log, the run-day log, the district
register, the 2027 volume plan, the 2027 rate card, the 2027 delivery calendar and the three files the call never
reads (the fuel card statement, the customer contact log, the van fleet register)."""
import csv
import datetime as dt
import hashlib
import math
import os

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

import params as P
import sim

FILES = {
    "stops": "delivery_stops_2025-2026.csv",
    "rundays": "van_run_log_2025-2026.csv",
    "register": "district_register_2026.xlsx",
    "plan": "volume_plan_2027.xlsx",
    "rates": "fleet_rate_card_2027.xlsx",
    "calendar": "delivery_calendar_2027.csv",
    "offer": "owenduff_offer_brackloon_2027.pdf",
    "standard": "network_planning_standard_NPS-3.pdf",
    "fuel": "fuel_card_statement_2025-2026.csv",
    "contacts": "customer_contacts_2026.csv",
    "fleet": "van_fleet_register_2026.xlsx",
}
DISTRACTORS = ["fuel", "contacts", "fleet"]


def hhmmss(h):
    s = int(round(h * 3600))
    return "%02d:%02d:%02d" % (s // 3600, (s % 3600) // 60, s % 60)


def hhmm(h):
    s = int(round(h * 60))
    return "%02d:%02d" % (s // 60, s % 60)


def district_on(code, ref, d):
    if code in P.SPLIT and d >= P.SPLIT_DATE:
        a, _, b, _ = P.SPLIT[code]
        return a if int(hashlib.sha1(ref.encode()).hexdigest(), 16) % 2 else b
    return code


def handheld(run, d):
    # each run's handheld was swapped once, at the summer service
    base = 3100 + 11 * list(P.RUNS).index(run)
    return "HH%04d" % (base + (1 if d >= dt.date(2025, 7, 14) else 0))


def write_stops(w, path):
    rng = np.random.default_rng(P.SEED + 1)
    rows = []
    for rd in w["rundays"]:
        d = rd["date"]
        for i, s in enumerate(rd["stops"], 1):
            kind = {"DEL": "DELIVERY", "FAIL": "FAILED_ATTEMPT", "COL": "COLLECTION", "BREAK": "BREAK"}[s["kind"]]
            dist = "" if s["district"] is None else district_on(s["district"], s["ref"], d)
            dep = hhmmss(s["dep"])
            if kind != "BREAK" and rng.random() < P.MISSING_DEP:
                dep = ""
            delivered = s["parcels"] if s["kind"] == "DEL" else 0
            failed = s["parcels"] if s["kind"] == "FAIL" else 0
            sync_h = s["dep"] + 0.002 + rng.exponential(0.01)
            row = [d.isoformat(), rd["run"], rd["van"], handheld(rd["run"], d), i, kind, dist, s["ref"], delivered,
                   failed, s["collect"], hhmmss(s["arr"]), dep, "%s %s" % (d.isoformat(), hhmmss(sync_h))]
            rows.append(row)
            if kind != "BREAK" and rng.random() < P.DUP_RATE:
                late = rd["in"] + 0.05 + rng.exponential(0.3)
                rows.append(row[:-1] + ["%s %s" % (d.isoformat(), hhmmss(min(late, 23.9)))])
    with open(path, "w", newline="", encoding="utf-8") as fh:
        cw = csv.writer(fh)
        cw.writerow(["run_date", "run_code", "van_reg", "handheld_id", "stop_seq", "stop_type", "district_code",
                     "customer_ref", "parcels_delivered", "parcels_failed", "items_collected", "arrived_local",
                     "departed_local", "synced_at_local"])
        cw.writerows(rows)
    return len(rows)


def write_rundays(w, path):
    """the fleet app's export: a row per van run; the app re-exported some days after a sync fault (the same rows
    twice), the van's odometer is blank where the driver skipped the closing reading, and the run names were
    re-keyed with an ampersand when the fleet app was upgraded on 2 March 2026"""
    rng = np.random.default_rng(P.SEED + 3)
    odo = {}
    rows = []
    for rd in w["rundays"]:
        o = odo.get(rd["van"], 41200 + 900 * len(odo))
        km = int(round(rd["km"]))
        stops = [s for s in rd["stops"] if s["kind"] != "BREAK"]
        name = P.RUNS[rd["run"]]
        if rd["date"] >= dt.date(2026, 3, 2):
            name = name.replace(" and ", " & ")
        row = [rd["date"].isoformat(), rd["run"], name, rd["van"], rd["driver"], hhmm(rd["out"]), hhmm(rd["in"]), o,
               "" if rng.random() < 0.01 else o + km, len(stops),
               sum(s["parcels"] for s in stops if s["kind"] == "DEL"), int(P.BREAK_H * 60)]
        rows.append(row)
        if rng.random() < 0.006:
            rows.append(list(row))
        odo[rd["van"]] = o + km + int(km * 0.02)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        cw = csv.writer(fh)
        cw.writerow(["run_date", "run_code", "run_name", "van_reg", "driver_ref", "depot_out", "depot_in",
                     "odometer_out_km", "odometer_in_km", "stops", "parcels_delivered", "break_min"])
        cw.writerows(rows)
    return len(rows)


HEAD = Font(bold=True)
FILL = PatternFill("solid", fgColor="DDE4EE")


def _sheet(ws, header, rows, widths=None):
    ws.append(header)
    for c in ws[1]:
        c.font, c.fill = HEAD, FILL
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for r in rows:
        ws.append(r)
    for i, wd in enumerate(widths or [], 1):
        ws.column_dimensions[get_column_letter(i)].width = wd
    ws.freeze_panes = "A2"


def write_register(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Districts"
    rows = []
    for c, v in P.D.items():
        if c in P.SPLIT:
            for code, name in ((P.SPLIT[c][0], P.SPLIT[c][1]), (P.SPLIT[c][2], P.SPLIT[c][3])):
                rows.append([code, name, "Mayo", round(v[1] + (0.004 if code.endswith("N") else -0.004), 4),
                             round(v[2], 4), v[6], P.RUNS[v[6]], "2026-04-01", ""])
            continue
        county = "Galway" if c in ("LEE", "LET", "CLI") else "Mayo"
        rows.append([c, v[0], county, round(v[1], 4), round(v[2], 4), v[6], P.RUNS[v[6]], "2023-01-09", ""])
    _sheet(ws, ["district_code", "district_name", "county", "centroid_lat", "centroid_lon", "run_code", "run_name",
                "in_register_from", "in_register_to"], rows, [12, 20, 10, 12, 12, 9, 28, 14, 14])
    ws2 = wb.create_sheet("Code changes")
    a, an, b, bn = P.SPLIT["CBR"]
    _sheet(ws2, ["old_code", "old_name", "new_code", "new_name", "effective_from", "basis"],
           [["CBR", "Castlebar town", a, an, "2026-04-01", "N5 line: north of the N5 and the Westport road"],
            ["CBR", "Castlebar town", b, bn, "2026-04-01", "N5 line: south of the N5 and the Westport road"]],
           [10, 16, 10, 16, 14, 44])
    ws3 = wb.create_sheet("Depot")
    _sheet(ws3, ["site", "address", "lat", "lon", "loading_from"],
           [[P.DEPOT[0], "Unit 4, Breaffy Business Park, Castlebar, Co. Mayo", P.DEPOT[1], P.DEPOT[2], "06:30"]],
           [18, 48, 10, 10, 12])
    wb.save(path)


def plan_parcels(code, month):
    """the commercial team's 2027 forecast of parcels delivered, district by month, rounded to tens"""
    v = P.D[code]
    days = len([d for d in P.delivery_days(dt.date(2027, 1, 1), dt.date(2027, 12, 31)) if d.month == month])
    stops = v[7] * v[10] * P.SEASON[month] * days
    # parcels per stop including the stops that hand nothing over
    per_stop = (1 - P.COLLECT_RATE - P.FAIL_RATE) * v[8]
    return int(round(stops * per_stop / 10.0)) * 10


def write_plan(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Parcels by district"
    rows = []
    codes = [c for c in P.D if c not in P.SPLIT] + [P.SPLIT["CBR"][0], P.SPLIT["CBR"][2]]
    for c in codes:
        base = "CBR" if c in (P.SPLIT["CBR"][0], P.SPLIT["CBR"][2]) else c
        name = P.SPLIT["CBR"][1] if c == P.SPLIT["CBR"][0] else (P.SPLIT["CBR"][3] if c == P.SPLIT["CBR"][2] else P.D[c][0])
        m = [plan_parcels(base, k) for k in range(1, 13)]
        if base == "CBR":
            m = [int(round(x / 20.0)) * 10 for x in m]
        rows.append([c, name] + m + [sum(m)])
    _sheet(ws, ["district_code", "district_name"] + [dt.date(2027, k, 1).strftime("%b-27") for k in range(1, 13)] +
           ["2027"], rows, [12, 20] + [8] * 13)
    ws2 = wb.create_sheet("Basis")
    _sheet(ws2, ["item", "note"], [
        ["Prepared", "Commercial planning, 19 October 2026, for the 2027 budget"],
        ["Parcels", "Parcels delivered to customers in each district, by delivery month, rounded to tens"],
        ["Growth", "District trading trends to September 2026 carried into 2027 with the spring range extension"],
        ["Not included", "Click-and-collect orders taken at the Castlebar counter"]], [16, 90])
    wb.save(path)


def write_rates(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Van-hour rate 2027"
    rows = [[k, v] for k, v in P.RATE_PARTS] + [["All-in van-hour rate, EUR", P.RATE_2027]]
    _sheet(ws, ["component", "EUR per van-hour"], rows, [60, 18])
    ws["A6"] = "Applies to every van-hour from depot out to depot in. Approved with the 2027 budget assumptions, 30 September 2026."
    ws2 = wb.create_sheet("2026 for comparison")
    _sheet(ws2, ["component", "EUR per van-hour"], [["Driver, with employer's PRSI and pension", 30.10],
                                                    ["Van lease and insurance", 9.60],
                                                    ["Fuel, tyres and servicing at the fleet's average running", 17.40],
                                                    ["All-in van-hour rate, EUR", 57.10]], [60, 18])
    wb.save(path)


def write_calendar(path):
    days = set(P.delivery_days(dt.date(2027, 1, 1), dt.date(2027, 12, 31)))
    hol = P.holidays(2027)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        cw = csv.writer(fh)
        cw.writerow(["date", "weekday", "delivery_day", "note"])
        d = dt.date(2027, 1, 1)
        while d.year == 2027:
            note = "public holiday" if d in hol else ""
            cw.writerow([d.isoformat(), d.strftime("%a"), "Y" if d in days else "N", note])
            d += dt.timedelta(days=1)


def write_fuel(w, path):
    rng = np.random.default_rng(P.SEED + 7)
    stations = ["Applegreen Castlebar", "Maxol Westport", "Circle K Ballina", "Top Oil Belmullet", "Texaco Claremorris",
                "Emo Swinford", "Inver Clifden"]
    rows = []
    for rd in w["rundays"]:
        if rng.random() < 0.38:
            litres = round(float(rng.uniform(35, 70)), 2)
            price = round(1.62 + 0.04 * math.sin(rd["date"].toordinal() / 40.0), 3)
            rows.append([rd["date"].isoformat(), hhmm(rd["in"] - rng.uniform(0.1, 0.6)), rd["van"],
                         "FC-%s" % rd["van"][-5:], stations[int(rng.integers(len(stations)))], "DIESEL", litres,
                         price, round(litres * price, 2)])
    with open(path, "w", newline="", encoding="utf-8") as fh:
        cw = csv.writer(fh)
        cw.writerow(["txn_date", "txn_time", "van_reg", "card_ref", "site", "product", "litres", "eur_per_litre", "amount_eur"])
        cw.writerows(rows)


def write_contacts(w, path):
    rng = np.random.default_rng(P.SEED + 9)
    reasons = ["Where is my order", "Delivered damaged", "Missed delivery, rebook", "Change delivery address",
               "Return collection", "Wrong item", "Driver feedback, positive", "Access to farmyard"]
    rows, n = [], 0
    for rd in w["rundays"]:
        if rd["date"].year != 2026:
            continue
        for s in rd["stops"]:
            if s["kind"] == "BREAK" or rng.random() > 0.012:
                continue
            n += 1
            dist = district_on(s["district"], s["ref"], rd["date"])
            rows.append(["C26-%05d" % n, (rd["date"] + dt.timedelta(days=int(rng.integers(0, 3)))).isoformat(),
                         s["ref"], dist, reasons[int(rng.integers(len(reasons)))],
                         ["phone", "email", "web chat"][int(rng.integers(3))], ["closed", "closed", "open"][int(rng.integers(3))]])
    with open(path, "w", newline="", encoding="utf-8") as fh:
        cw = csv.writer(fh)
        cw.writerow(["contact_id", "contact_date", "customer_ref", "district_code", "reason", "channel", "status"])
        cw.writerows(rows)


def write_fleet(w, path):
    vans = sorted({(rd["run"], rd["van"]) for rd in w["rundays"]})
    wb = Workbook()
    ws = wb.active
    ws.title = "Vans"
    rows = []
    for i, (r, v) in enumerate(vans):
        rows.append([v, ["Ford Transit 350 L3H2", "Renault Master L3H2", "Ford Transit 350 L2H2"][i % 3],
                     "3,500 kg", ["2022-03-01", "2023-01-16", "2024-06-03"][i % 3], "Fleetbridge Leasing", r,
                     ["2027-02-28", "2027-12-31", "2028-05-31"][i % 3]])
    _sheet(ws, ["van_reg", "model", "gross_vehicle_weight", "on_fleet_from", "lessor", "usual_run", "lease_end"], rows,
           [14, 24, 12, 14, 20, 10, 12])
    wb.save(path)


def write_tables(w, target):
    F = {k: os.path.join(target, v) for k, v in FILES.items()}
    n = {"stops": write_stops(w, F["stops"]), "rundays": write_rundays(w, F["rundays"])}
    write_register(F["register"])
    write_plan(F["plan"])
    write_rates(F["rates"])
    write_calendar(F["calendar"])
    write_fuel(w, F["fuel"])
    write_contacts(w, F["contacts"])
    write_fleet(w, F["fleet"])
    return n
