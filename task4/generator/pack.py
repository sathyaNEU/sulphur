"""The data files under target/, written the way Havørn's systems export them: the flight data feed's legs, the
maintenance system's component changes, the Bodø shop's work orders and roster, the repair vendors' orders, the fleet
register, the stores snapshot, the 2027 flying programme, the stations' weather, and two files that sit beside the
work (the engine trend export and a pool provider's offer). Each carries its system's own conventions and mess."""
import csv
import datetime as dt
import os

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

import params as P
import sim

FILES = {
    "legs": "flight_legs_2023-01_2026-11.csv",
    "changes": "component_changes_2023-01_2026-11.csv",
    "shop": "bodo_shop_work_orders_2023-2026.csv",
    "roster": "bodo_shop_roster_2023-2026.csv",
    "vendor": "vendor_repair_orders_2023-2026.xlsx",
    "register": "fleet_register.xlsx",
    "pool": "rotable_stores_snapshot_2026-11-30.xlsx",
    "programme": "flying_programme_2027.xlsx",
    "weather": "station_weather_daily_2023-2026.csv",
    "report": "reliability_report_2026-10.pdf",
    "standard": "reliability_programme_and_spares_standard.pdf",
    "ecm": "engine_trend_monitoring_2025-2026.csv",
    "offer": "pool_support_offer_2026.pdf",
    "shopplan": "bodo_shop_plan_2027.xlsx",
}
DISTRACTORS = ["ecm", "offer"]
ICAO = {"BOO": "ENBO", "TOS": "ENTC", "BGO": "ENBR", "TRD": "ENVA"}
PN_ALT = {"23085-016": "23085016", "2-1577-3": "2-1577-3", "822-1081-003": "8221081-003", "816534-3": "816534-3"}


def _iso(t):
    return t.strftime("%Y-%m-%dT%H:%MZ")


def legs(w, path):
    """The flight data feed: one row a leg, block and air times in UTC, the flight date local. The feed re-sent three
    days in March 2025 (both copies kept) and lost the air times on some legs when the ACARS link dropped."""
    rng = np.random.default_rng(P.SEED + 21)
    E = w.E
    resent = {dt.date(2025, 3, 11), dt.date(2025, 3, 12), dt.date(2025, 3, 18)}
    rows = 0
    with open(path, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["flight_date", "flight_no", "aircraft", "dep", "arr", "out_utc", "off_utc", "on_utc", "in_utc"])
        batch = []
        for l in E.legs:
            gap = rng.random() < 0.004
            row = [l["date"].isoformat(), l["flight"], l["tail"], l["dep"], l["arr"], _iso(l["out"]),
                   "" if gap else _iso(l["off"]), "" if gap else _iso(l["on"]), _iso(l["in"])]
            wr.writerow(row)
            rows += 1
            if l["date"] in resent:
                batch.append(row)
            elif batch:
                for b in batch:
                    wr.writerow(b)
                    rows += 1
                batch = []
    return rows


def _sn_variant(rng, sn, d):
    """Serials as technicians typed them: the maintenance system took the label as scanned (with the 'S/N' prefix)
    from the 2024 handheld scanners until a fix in October 2024."""
    if dt.date(2024, 2, 1) <= d <= dt.date(2024, 10, 14) and rng.random() < 0.31:
        return "S/N " + sn
    if rng.random() < 0.012:
        return sn.lower()
    return sn


def reason_code(r, d):
    if d < dt.date(2024, 5, 6):
        return {"UNSCH": "U", "SCHED": "S", "CONV": "C"}[r]
    return r


def changes(w, path):
    """The maintenance system's component changes: one row a change, the unit off and the unit on. A corrected
    change is sent again as a new row with its number suffixed, the original kept."""
    rng = np.random.default_rng(P.SEED + 22)
    E = w.E
    n = 0
    with open(path, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["change_no", "change_date", "station", "aircraft", "ata", "part_no", "description", "position",
                     "serial_off", "serial_on", "reason", "defect", "tsn_off", "csn_off"])
        for c in sorted(E.changes, key=lambda x: (x["date"], x["no"])):
            p = P.PART[c["k"]]
            pn = PN_ALT.get(p["pn"], p["pn"]) if c["date"] < dt.date(2023, 9, 1) and rng.random() < 0.5 else p["pn"]
            tsn = "" if not c["known"] else "%.0f" % c["tsn"]
            csn = "" if not c["known"] else "%.0f" % c["csn"]
            row = [c["no"], c["date"].isoformat(), c["station"], c["tail"], p["ata"], pn, p["name"].upper(), c["pos"],
                   _sn_variant(rng, c["sn_off"], c["date"]) if c["sn_off"] else "", c["sn_on"],
                   reason_code(c["reason"], c["date"]), c["defect"], tsn if c["sn_off"] else "", csn if c["sn_off"] else ""]
            if rng.random() < 0.013:
                # the first entry carried a slip (the unit on typed one digit out, or the wrong position), corrected
                # the same day by a second entry under the change number with -R1
                bad = list(row)
                if c["sn_on"] and c["sn_on"][-1].isdigit() and rng.random() < 0.6:
                    bad[9] = c["sn_on"][:-1] + str((int(c["sn_on"][-1]) + 1) % 10)
                else:
                    names = sim.pos_names(c["k"])
                    bad[7] = names[(names.index(c["pos"]) + 1) % len(names)] if len(names) > 1 else c["pos"]
                wr.writerow(bad)
                row[0] = row[0] + "-R1"
                n += 1
            wr.writerow(row)
            n += 1
    return n


def shop(w, path):
    """The Bodø shop's work orders: rotable repairs and the shop's other work. A finding code was added to the form
    in March 2024; before that the finding is in the text alone."""
    E = w.E
    n = 0
    with open(path, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["work_order", "order_type", "part_no", "serial", "received", "parts_received", "work_started",
                     "completed", "finding_code", "finding", "hours_booked", "technician"])
        for j in sorted(E.shop_jobs, key=lambda x: x["wo"]):
            if j["arrive"] > P.ASOF:
                continue
            if j["type"] == "other":
                wr.writerow([j["wo"], "OTHER", "", "", j["arrive"].isoformat(), "", j["start"].isoformat(),
                             j["done"].isoformat(), "", j["text"], "%.1f" % j["hours"], j["tech"]])
                n += 1
                continue
            done = j["done"] if j["done"] and j["done"] <= P.ASOF else None
            code = ""
            if j["arrive"] >= dt.date(2024, 3, 4) and done:
                code = {"CF": "CONF", "NFF": "NFF", "BER": "BER"}[j["finding"]]
            pr = j["parts"] if j["parts"] != j["arrive"] and j["parts"] <= P.ASOF else None
            wr.writerow([j["wo"], "ROTABLE", P.PART[j["k"]]["pn"], j["sn"], j["arrive"].isoformat(),
                         pr.isoformat() if pr else "",
                         j["start"].isoformat() if j["start"] and j["start"] <= P.ASOF else "",
                         done.isoformat() if done else "", code, j["text"] if done else "",
                         "%.1f" % (j["hours"] - (j["left"] if not done else 0)) if j["start"] else "",
                         j.get("tech") or ""])
            n += 1
    return n


def roster(w, path):
    E = w.E
    with open(path, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["date", "technician", "hours_on_duty", "absence"])
        for r in E.roster:
            wr.writerow([r["date"].isoformat(), r["tech"], "%.1f" % r["hours"], r["absence"]])
    return len(E.roster)


def _sheet(ws, header, rows, widths=None, money=()):
    ws.append(header)
    for c in ws[1]:
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="DCE6F1")
        c.alignment = Alignment(vertical="top", wrap_text=True)
    for r in rows:
        ws.append(r)
    for i, wdt in enumerate(widths or [], start=1):
        ws.column_dimensions[get_column_letter(i)].width = wdt
    ws.freeze_panes = "A2"


def vendor(w, path):
    """The repair vendors' orders, as the purchasing team keeps them: one row an order, the invoice in the vendor's
    currency at the invoice date's rate. Orders still at the vendor at the export have no return date."""
    rng = np.random.default_rng(P.SEED + 23)
    E = w.E
    wb = Workbook()
    ws = wb.active
    ws.title = "Repair orders"
    rows = []
    for j in sorted(E.vendor_jobs, key=lambda x: x["order"]):
        if j["sent"] > P.ASOF:
            continue
        back = j["back"] if j["back"] <= P.ASOF else None
        p = P.PART[j["k"]]
        if j["finding"] == "SB":
            cost = p["price"] * 0.035
        elif j["finding"] == "NFF":
            cost = p["price"] * float(rng.uniform(0.025, 0.045))
        elif j["finding"] == "BER":
            cost = p["price"] * 0.02
        else:
            cost = p["price"] * float(rng.uniform(0.08, 0.19))
        ccy = j["ccy"]
        fx = 1.0 if ccy == "NOK" else P.FX[ccy] * float(rng.uniform(0.97, 1.03))
        amount = cost / fx
        text = j["text"] if back else ""
        if back and j["mod"]:
            text = (text + "; " if text else "") + "SB 61-0042 embodied"
        rows.append([j["order"], j["vendor"], p["pn"], j["sn"], j["sent"], j["at_vendor"] if j["at_vendor"] <= P.ASOF else None,
                     back, text, round(amount, 2) if back else None, ccy if back else None, round(fx, 4) if back and ccy != "NOK" else None])
    _sheet(ws, ["Order", "Repairer", "Part number", "Serial", "Shipped to repairer", "Received by repairer",
                "Returned to Bodø stores", "Repairer's finding", "Invoice amount", "Currency", "NOK per unit"],
           rows, [10, 30, 14, 10, 12, 12, 14, 60, 12, 8, 10])
    for row in ws.iter_rows(min_row=2):
        for c in (row[4], row[5], row[6]):
            c.number_format = "yyyy-mm-dd"
    ws2 = wb.create_sheet("New units")
    rows2 = []
    for b in sorted(E.purchases, key=lambda x: (x["ordered"], x["sn"])):
        if b["ordered"] > P.ASOF:
            continue
        p = P.PART[b["k"]]
        rows2.append(["PO-%s-%s" % (b["ordered"].strftime("%y%m"), b["sn"][-3:]), p["pn"], p["name"], b["sn"], b["ordered"],
                      b["delivered"] if b["delivered"] <= P.ASOF else None])
    _sheet(ws2, ["Purchase order", "Part number", "Description", "Serial", "Ordered", "Delivered to Bodø stores"],
           rows2, [16, 14, 34, 11, 12, 16])
    for row in ws2.iter_rows(min_row=2):
        row[4].number_format = row[5].number_format = "yyyy-mm-dd"
    wb.save(path)
    return len(rows)


def shop_plan(w, path):
    """The Bodø component shop's plan for 2027, issued by the shop supervisor in November: each technician's planned
    absences from December 2026 through 2027 (the staggered summer weeks, Christmas) and the bench hours the shop
    plans month by month, the contracted third-party work taken out."""
    wb = Workbook()
    ws = wb.active
    ws.title = "Roster plan"
    techs = ["SE", "KH", "MB"][:P.SHOP_TECHS]
    rows = []
    for t in techs:
        days = []
        d = dt.date(2026, 12, 1)
        while d <= dt.date(2027, 12, 31):
            if d.weekday() < 5 and d not in sim.HOL and sim.on_holiday(t, d):
                days.append(d)
            d += sim.DAY
        run = []
        for x in days + [None]:
            if run and (x is None or (x - run[-1]).days > 4):
                kind = "Summer holiday" if run[0].month in (6, 7, 8, 9) else "Christmas"
                rows.append([t, kind, run[0], run[-1], len(run)])
                run = []
            if x is not None:
                run.append(x)
    rows.sort(key=lambda r: (r[2], r[0]))
    _sheet(ws, ["Technician", "Absence", "From", "To", "Working days"], rows, [12, 16, 12, 12, 13])
    for row in ws.iter_rows(min_row=2):
        row[2].number_format = row[3].number_format = "yyyy-mm-dd"
    ws2 = wb.create_sheet("Bench hours")
    rows2 = []
    for y, m in [(2026, 12)] + [(2027, k) for k in range(1, 13)]:
        share = P.OTHER_WORK_2027 if dt.date(y, m, 1) >= P.OTHER_FROM else P.OTHER_WORK
        week = int(round(P.SHOP_HOURS * share * 5 * P.SHOP_TECHS))
        rows2.append([dt.date(y, m, 1), P.SHOP_TECHS, P.SHOP_HOURS, week,
                      round(P.SHOP_HOURS - week / (5.0 * P.SHOP_TECHS), 1)])
    _sheet(ws2, ["Month", "Technicians rostered", "Bench hours a technician on duty",
                 "Contracted third-party work (hours a week, full roster)", "Rotable bench hours a technician on duty"],
           rows2, [10, 12, 14, 22, 18])
    for row in ws2.iter_rows(min_row=2):
        row[0].number_format = "mmm yyyy"
    wb.save(path)
    return rows


def register(w, path):
    """The fleet register: aircraft, their base history and heavy checks."""
    wb = Workbook()
    ws = wb.active
    ws.title = "Fleet"
    rows = []
    for a in w.ac:
        rows.append([a["tail"], P.TYPE, a["msn"], a["delivered"], "PW123"])
    _sheet(ws, ["Registration", "Type", "MSN", "Delivered", "Engines"], rows, [13, 11, 7, 12, 9])
    for row in ws.iter_rows(min_row=2):
        row[3].number_format = "yyyy-mm-dd"
    ws2 = wb.create_sheet("Base history")
    rows = []
    for t, h in w.hist.items():
        for i, (when, b) in enumerate(h):
            to = h[i + 1][0] - sim.DAY if i + 1 < len(h) else None
            rows.append([t, b, when, to])
    _sheet(ws2, ["Registration", "Base", "From", "To"], rows, [13, 7, 12, 12])
    for row in ws2.iter_rows(min_row=2):
        row[2].number_format = row[3].number_format = "yyyy-mm-dd"
    ws3 = wb.create_sheet("Heavy checks")
    rows = []
    for t, lst in w.checks.items():
        for i, (a, b) in enumerate(lst):
            if a <= P.ASOF:
                rows.append([t, "C%d" % (1 + (i % 2)), "BOO", a, b if b <= P.ASOF else None])
            elif a <= dt.date(2027, 12, 31):
                rows.append([t, "C%d (planned)" % (1 + (i % 2)), "BOO", a, b])
    _sheet(ws3, ["Registration", "Check", "Station", "Start", "End"], rows, [13, 14, 8, 12, 12])
    for row in ws3.iter_rows(min_row=2):
        row[3].number_format = row[4].number_format = "yyyy-mm-dd"
    wb.save(path)


def pool(w, path):
    """The stores snapshot at the end of 30 November 2026: every serial of the pooled part numbers, where it is."""
    E = w.E
    wb = Workbook()
    ws = wb.active
    ws.title = "Rotables 2026-11-30"
    rows = []
    inst = {sn: key for key, sn in E.install.items() if sn}
    kit = {}
    for (s, k), lst in E.kits.items():
        for sn in lst:
            kit[sn] = s
    shop_open = {j["sn"] for j in E.queue}
    for sn, u in sorted(E.units.items(), key=lambda x: (P.PART[x[1]["k"]]["pn"], x[0])):
        p = P.PART[u["k"]]
        if u["status"] == "scrap":
            continue
        if sn in inst:
            t, k, pos = inst[sn]
            st, loc = "Installed", "%s %s" % (t, pos)
        elif sn in kit:
            st, loc = "Serviceable", "Station kit %s" % kit[sn]
        elif sn in E.pool[u["k"]]:
            st, loc = "Serviceable", "Bodø main stores"
        elif sn in shop_open:
            st, loc = "Unserviceable", "Bodø component shop"
        elif u["status"] == "order":
            st, loc = "On order", "New from manufacturer"
        elif u["status"] == "repair":
            st, loc = "Unserviceable", "At repairer"
        else:
            st, loc = "Serviceable", "Bodø main stores"
        sb = ""
        if u["k"] == "PEC":
            sb = "Incorporated" if u["mod"] else "Not incorporated"
        rows.append([p["pn"], p["name"], sn, st, loc, sb])
    _sheet(ws, ["Part number", "Description", "Serial", "Condition", "Location", "SB 61-0042"], rows,
           [14, 34, 11, 14, 26, 14])
    wb.save(path)
    return rows


def programme(w, path):
    """The 2027 flying programme, as network planning issued it: each leg's departures a week and scheduled block
    minutes by season and operating base, and the aircraft each base is planned to hold month by month."""
    wb = Workbook()
    ws = wb.active
    ws.title = "Programme 2027"
    rows = []
    for r in plan_2027(w):
        grp = "Bodø (Helgeland routes)" if r["grp"] == "HEL" else P.BASES[r["grp"]]["name"]
        rows.append([r["season"], grp, r["dep"], r["arr"], r["from"], r["to"], round(r["per_week"], 1), int(round(r["block"]))])
    _sheet(ws, ["Season", "Operated from", "From", "To", "Valid from", "Valid to", "Departures a week",
                "Block minutes"], rows, [13, 24, 7, 7, 12, 12, 16, 13])
    for row in ws.iter_rows(min_row=2):
        row[4].number_format = row[5].number_format = "yyyy-mm-dd"
    ws2 = wb.create_sheet("Aircraft by base")
    rows = []
    for m in range(1, 13):
        d = dt.date(2027, m, 15)
        cnt = P.BASE_2027_Q1 if d < P.HELGELAND else P.BASE_2027_AP
        rows.append([dt.date(2027, m, 1), cnt["BOO"], cnt["TOS"], cnt["BGO"], cnt["TRD"],
                     P.HELGELAND_N if d >= P.HELGELAND else 0])
    _sheet(ws2, ["Month", "Bodø", "Tromsø", "Bergen", "Trondheim", "of which on the Helgeland routes"],
           rows, [11, 8, 8, 8, 10, 28])
    for row in ws2.iter_rows(min_row=2):
        row[0].number_format = "mmm yyyy"
    wb.save(path)
    return rows


def plan_2027(w, draws=24):
    """The programme the replays fly: each leg's expected departures a week and its block minutes, by season, base
    and route, averaged over many draws of the 2027 flying (the aircraft each base holds, the planned checks, the
    seasons and the weekends)."""
    rng = np.random.default_rng(P.SEED + 26)
    seasons = [("Winter 26/27", dt.date(2027, 1, 1), dt.date(2027, 3, 27)),
               ("Summer 27", dt.date(2027, 3, 28), dt.date(2027, 10, 30)),
               ("Winter 27/28", dt.date(2027, 10, 31), dt.date(2027, 12, 31))]
    acc = {}
    for _ in range(draws):
        d = dt.date(2027, 1, 1)
        while d <= dt.date(2027, 12, 31):
            sname = [s for s, a, b in seasons if a <= d <= b][0]
            for a in w.ac:
                t = a["tail"]
                if sim.check_on(w.checks, t, d) is not None:
                    continue
                base = sim.base_2027(w.hist, w.movers, t, d)
                net, lm = sim.network_for(base, d, t, w.movers)
                grp = "HEL" if (d >= P.HELGELAND and w.movers.get(t) == "HEL") else base
                for dep, arr, blk in sim.rotation(rng, net, lm, sim.season(d)):
                    dep = base if dep == "BASE" else dep
                    arr = base if arr == "BASE" else arr
                    blk_eff = blk * (1.04 if d.month in (12, 1, 2) else 1.0)
                    key = (sname, grp, dep, arr)
                    c = acc.setdefault(key, [0, 0.0])
                    c[0] += 1
                    c[1] += blk_eff
            d += sim.DAY
    out = []
    for (sname, grp, dep, arr), (n, bsum) in sorted(acc.items()):
        a, b = [(x[1], x[2]) for x in seasons if x[0] == sname][0]
        if grp == "HEL":
            a = max(a, P.HELGELAND)
        weeks = ((b - a).days + 1) / 7.0
        out.append({"season": sname, "grp": grp, "dep": dep, "arr": arr, "from": a, "to": b,
                    "per_week": n / draws / weeks, "block": bsum / n})
    return out


def weather(w, path):
    """The stations' daily climate summaries as the airports' met offices publish them; a few days missing where a
    sensor was down."""
    rng = np.random.default_rng(P.SEED + 24)
    n = 0
    with open(path, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["station", "date", "tmin_c", "tmax_c"])
        for b in ("BOO", "TOS", "BGO", "TRD"):
            for i, d in enumerate(w.dates):
                if d > P.ASOF:
                    break
                if rng.random() < 0.003:
                    wr.writerow([ICAO[b], d.isoformat(), "", ""])
                else:
                    wr.writerow([ICAO[b], d.isoformat(), "%.1f" % w.wx[b]["tmin"][i], "%.1f" % w.wx[b]["tmax"][i]])
                n += 1
    return n


def ecm(w, path):
    """Engine condition trend data (the engine shop's export): take-off and cruise snapshots per engine. Nothing in the
    spares work reads it."""
    rng = np.random.default_rng(P.SEED + 25)
    n = 0
    with open(path, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["aircraft", "engine_pos", "engine_sn", "date", "phase", "itt_c", "itt_margin_c", "torque_pct",
                     "np_pct", "oat_c", "altitude_ft"])
        esn = {(a["tail"], e): "PCE-FA%04d" % int(rng.integers(1000, 9999)) for a in w.ac for e in (1, 2)}
        for a in w.ac:
            for e in (1, 2):
                drift = float(rng.uniform(-0.04, 0.02))
                margin = float(rng.uniform(28, 61))
                d = dt.date(2025, 1, 3)
                while d <= P.ASOF:
                    if rng.random() < 0.55:
                        margin += drift + float(rng.normal(0, 0.6))
                        for ph, tq, alt in (("TO", 92 + rng.normal(0, 2), 0), ("CRZ", 74 + rng.normal(0, 3), 17000 + 2000 * rng.random())):
                            oat = float(rng.normal(4 if ph == "TO" else -18, 7))
                            itt = 765 - margin + 0.9 * oat + (40 if ph == "TO" else 0) + float(rng.normal(0, 4))
                            wr.writerow([a["tail"], e, esn[(a["tail"], e)], d.isoformat(), ph, "%.0f" % itt,
                                         "%.0f" % margin, "%.1f" % tq, "%.1f" % (100 if ph == "TO" else 85),
                                         "%.0f" % oat, "%.0f" % alt])
                            n += 1
                    d += dt.timedelta(days=int(rng.integers(3, 9)))
    return n
