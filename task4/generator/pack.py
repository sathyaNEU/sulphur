"""The pack under target/, written from the simulated brewery's own events: the RFID reads of tagged kegs, every
delivery visit as the driver's handheld kept it, the depot gate counters, the washer, the fills, the keg register,
the stocktakes, the reps' keg counts at pubs, repairs, the recovery agent's finds, the ERP database (accounts,
routes, dispense lines, deposits), the weather and the 2027 plans. Mess is the process's own: drivers key empties by
eye (other brewers' kegs among them, a blank now and then), handhelds re-sync a visit twice, readers miss tags, a
counter goes down and is keyed next day, accounts are renumbered when a pub changes hands, sizes are written three
ways."""
import csv
import datetime as dt
import math
import os
import sqlite3
from collections import defaultdict

import numpy as np
import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill

import params as P

FILES = {
    "rfid": "keg_rfid_reads_2025-06_2026-11.csv",
    "visits": "delivery_visits_2025-01_2026-11.csv",
    "gate": "depot_gate_counts_2023-12_2026-11.csv",
    "washer": "washer_log_2023-12_2026-11.csv",
    "fills": "filling_log_2023-12_2026-11.csv",
    "repairs": "keg_repair_jobs_2023-12_2026-11.csv",
    "audits": "rep_keg_counts_2025-2026.csv",
    "weather": "weather_daily_2016-01_2026-11.csv",
    "register": "keg_register_2026-11-30.xlsx",
    "stocktake": "keg_stocktakes_30nov_2024-2026.xlsx",
    "recovery": "kegtrace_recoveries_2024-2026.xlsx",
    "plan": "plan_2027.xlsx",
    "erp": "wrenfold_erp_extract_2026-12-01.sqlite",
    "exchange": "nke_statements_2024-01_2026-11.pdf",
    "standard": "keg_fleet_standard_issue3.pdf",
    "quote": "lindqvist_quotation_LF-26-1187.pdf",
    "agreement": "maplestead_listing_agreement_2026-10.docx",
    "cask": "cask_register_2026-11-30.xlsx",
    "packline": "packaging_line_oee_2025-2026.csv",
}
DISTRACTORS = ["cask", "packline"]


def serial(k):
    return "WB%d-%06d" % (k.size, 100000 + k.id)


def tag_of(k):
    return "E2801170%08X" % (0x2A000000 + k.id * 7919 % 0x0FFFFFF)


def sizecode(s, rng):
    u = rng.random()
    return str(s) if u < 0.55 else ("%dL" % s if u < 0.9 else "K%d" % s)


def _w(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(header)
        wr.writerows(rows)
    return len(rows)


def account_of(o, d):
    """an outlet's account number on a date: a pub that changed hands is opened again under a new number"""
    if o.renumbered and d >= o.renumbered:
        return "W%05d" % (int(o.id[1:]) + 50000)
    return o.id


# ------------------------------------------------------------------------------------------------- big records
def rfid(w, path):
    rng = np.random.default_rng(P.SEED + 11)
    byid = w.kegs
    rows = []
    retag = {}
    for k in byid:
        if k.tag and rng.random() < 0.018:
            retag[k.id] = (dt.date(2025, 1, 1) + dt.timedelta(days=int(rng.integers(30, 650))),
                           "E2801191%08X" % (0x3B000000 + k.id * 104729 % 0x0FFFFFF))
    w.retag = retag
    outlets = {o.id: o for o in w.outlets}
    for d, kid, point, loc in w.ev["read"]:
        if d < P.RFID0:
            continue
        k = byid[kid]
        t = retag.get(kid)
        tag = t[1] if t and d >= t[0] else tag_of(k)
        if point == "DELIVER":
            o = outlets[loc]
            hh = 7 + int(rng.integers(0, 8))
            where = account_of(o, d)
            reader = "HH-%s-%02d" % (o.depot, int(rng.integers(1, 15)))
        elif point == "FILL":
            hh = 6 + int(rng.integers(0, 16))
            where = "BRG-RACK"
            reader = "RK-%d" % (1 if k.size != 20 else 2)
        else:
            hh = 6 + int(rng.integers(0, 16))
            where = "BRG-WASH"
            reader = "WS-%d" % (1 if k.size != 20 else 2)
        ts = dt.datetime(d.year, d.month, d.day, hh, int(rng.integers(0, 60)), int(rng.integers(0, 60)))
        rows.append((ts.strftime("%Y-%m-%d %H:%M:%S"), tag, point, where, reader))
        if rng.random() < 0.021:
            ts2 = ts + dt.timedelta(seconds=int(rng.integers(1, 9)))
            rows.append((ts2.strftime("%Y-%m-%d %H:%M:%S"), tag, point, where, reader))
    rows.sort()
    return _w(path, ["read_time", "tag_epc", "read_point", "location", "reader_id"], rows)


def visits(w, path):
    rng = np.random.default_rng(P.SEED + 12)
    outlets = {o.id: o for o in w.outlets}
    rows = []
    n = 0
    seq = defaultdict(int)
    for d, oid, dep, deliv, coll, foreign in w.ev["visit"]:
        if d < P.VISITS0:
            continue
        o = outlets[oid]
        seq[(d, dep)] += 1
        n += 1
        vid = "DV%s%s%04d" % (d.strftime("%y%m%d"), dep[0], seq[(d, dep)])
        route = "%s-%02d" % (dep, 1 + (int(oid[1:]) * 7) % (14 if dep in ("BRG", "LDS") else 9))
        rec = [vid, d.isoformat(), dep, route, account_of(o, d)]
        for s in P.SIZES:
            rec.append(deliv[s])
        for s in P.SIZES:
            seen = coll[s] + foreign[s]
            if seen and rng.random() < 0.03:
                rec.append("")
                continue
            err = 0
            if seen >= 3 and rng.random() < 0.10:
                err = int(rng.choice([-1, -1, 1]))
            rec.append(max(0, seen + err))
        rec.append("" if rng.random() < 0.9 else ["ullage collected", "cellar locked, left at door", "two empties left",
                                                   "signed by staff"][int(rng.integers(0, 4))])
        rows.append(rec)
        if rng.random() < 0.006:
            rows.append(list(rec))
    hdr = ["visit_id", "visit_date", "depot", "route", "account", "fulls_50", "fulls_30", "fulls_20",
           "empties_50", "empties_30", "empties_20", "driver_note"]
    return _w(path, hdr, rows)


def gate(w, path):
    rng = np.random.default_rng(P.SEED + 13)
    agg = defaultdict(lambda: [0, 0])
    for d, oid, dep, deliv, coll, foreign in w.ev["visit"]:
        for s in P.SIZES:
            a = agg[(d, dep, s)]
            a[0] += deliv[s]
            a[1] += coll[s] + foreign[s]
    rows = []
    carry = {}
    for d in _days(P.H0, P.ASOF):
        for dep in P.DEPOTS:
            out_day = d.weekday() == 6
            for s in P.SIZES:
                f, e = agg.get((d, dep, s), [0, 0])
                key = (dep, s)
                if key in carry:
                    cf, ce = carry.pop(key)
                    rows.append((d.isoformat(), dep, sizecode(s, rng), f + cf, e + ce, "MANUAL", "includes %s" %
                                 (d - dt.timedelta(days=1)).isoformat()))
                    continue
                if not out_day and rng.random() < 0.006 and (f or e):
                    carry[key] = (f, e)
                    rows.append((d.isoformat(), dep, sizecode(s, rng), "", "", "OUTAGE", "counter down, keyed next day"))
                    continue
                if f == 0 and e == 0 and out_day:
                    continue
                rows.append((d.isoformat(), dep, sizecode(s, rng), f, e, "OK", ""))
    return _w(path, ["count_date", "depot", "keg_size", "fulls_out", "empties_in", "counter_status", "remark"], rows)


def washer(w, path):
    rng = np.random.default_rng(P.SEED + 14)
    rows = []
    for d, s, washed, foreign, damaged, condemned, r_depot, r_exch, r_rec, r_rep in w.ev["washer"]:
        line = "W2" if s == 20 else "W1"
        tot = (washed, foreign, damaged - condemned, condemned)
        a = [int(rng.binomial(x, 0.55)) for x in tot]
        b = [x - y for x, y in zip(tot, a)]
        for shift, v in (("A", a), ("B", b)):
            presented = sum(v)
            if presented == 0:
                continue
            rows.append((d.isoformat(), shift, line, s, presented, v[0], v[1], v[2], v[3]))
    hdr = ["wash_date", "shift", "line", "keg_size_l", "presented", "washed_ok", "rejected_not_ours",
           "rejected_to_repair", "condemned_at_inspection"]
    return _w(path, hdr, rows)


def fills(w, path):
    agg = defaultdict(int)
    for d, kid, s, sku in w.ev["fill"]:
        agg[(d, sku, s)] += 1
    rows = []
    for (d, sku, s), n in sorted(agg.items()):
        line = "FL2" if s == 20 else "FL1"
        rows.append((d.isoformat(), line, sku, P.FOUNDRY_NAMES.get(sku, w.sku_info[sku][1] if sku in w.sku_info else sku),
                     s, n, round(n * s / 100.0, 2)))
    return _w(path, ["fill_date", "filler", "beer_code", "beer", "keg_l", "kegs_filled", "hl_filled"], rows)


def repairs(w, path):
    rng = np.random.default_rng(P.SEED + 15)
    rows = []
    faults = ["spear seal leak", "dented chime", "neck damage", "valve stuck", "failed pressure test", "contaminated"]
    for i, (d, kid, back) in enumerate(w.ev["repair"]):
        k = w.kegs[kid]
        rows.append(("RJ%06d" % (i + 1), serial(k), k.size, d.isoformat(), faults[int(rng.integers(0, 6))],
                     "REPAIRED", back.isoformat() if back <= P.ASOF else ""))
    for j, (d, kid) in enumerate(w.ev["condemn"]):
        k = w.kegs[kid]
        rows.append(("RJ%06d" % (len(w.ev["repair"]) + j + 1), serial(k), k.size, d.isoformat(),
                     ["corroded body", "split chime", "failed pressure test"][int(rng.integers(0, 3))],
                     "CONDEMNED", d.isoformat()))
    rows.sort(key=lambda r: (r[3], r[0]))
    return _w(path, ["job", "keg_serial", "size_l", "received", "fault", "outcome", "back_to_washer"], rows)


def audits(w, path):
    rng = np.random.default_rng(P.SEED + 16)
    outlets = {o.id: o for o in w.outlets}
    reps = ["A. Hodgson", "R. Patel", "S. Whitworth", "D. Marsden", "C. Lund", "M. Shah"]
    rows = []
    for d, oid, c in w.ev["audit"]:
        o = outlets[oid]
        rec = [d.isoformat(), account_of(o, d), reps[int(rng.integers(0, len(reps)))]]
        for s in P.SIZES:
            f, t, e = c[s]
            rec += [f, t, e]
        rows.append(rec)
    hdr = ["count_date", "account", "counted_by", "full_50", "on_tap_50", "empty_50", "full_30", "on_tap_30",
           "empty_30", "full_20", "on_tap_20", "empty_20"]
    return _w(path, hdr, rows)


def weather(w, path):
    rng = np.random.default_rng(P.SEED + 17)
    rows = []
    names = {"LDS": "Leeds Weather Centre", "YRK": "York (Linton)", "SHF": "Sheffield (Weston Park)"}
    for st, arr in w.weather.station.items():
        for i, d in enumerate(w.weather.days):
            if rng.random() < 0.008:
                rows.append((d.isoformat(), names[st], "", ""))
                continue
            tmax = float(arr[i])
            rain = round(float(max(0.0, rng.gamma(0.55, 3.6) - 0.6)), 1)
            rows.append((d.isoformat(), names[st], "%.1f" % tmax, "%.1f" % rain))
    rows.sort()
    return _w(path, ["date", "station", "tmax_c", "rain_mm"], rows)


def packline(w, path):
    rng = np.random.default_rng(P.SEED + 18)
    rows = []
    for d in _days(dt.date(2025, 1, 6), P.ASOF):
        if d.weekday() >= 5:
            continue
        for line, fmt, rate in (("CAN1", "440ml can", 9000), ("BTL1", "500ml bottle", 6000)):
            planned = 7.5 * 60
            down = float(max(0, rng.normal(48, 25)))
            run = planned - down
            good = int(run * rate / 60 * float(rng.uniform(0.86, 0.97)))
            rows.append((d.isoformat(), line, fmt, round(planned), round(run), good, int(good * rng.uniform(0.004, 0.02)),
                         round(run / planned * good / (run * rate / 60) * 100, 1)))
    return _w(path, ["prod_date", "line", "format", "planned_min", "run_min", "good_units", "rejects", "oee_pct"], rows)


def _days(a, b):
    d = a
    while d <= b:
        yield d
        d += dt.timedelta(days=1)


# ------------------------------------------------------------------------------------------------- workbooks
HEAD = Font(bold=True)
FILL = PatternFill("solid", fgColor="DDE4EE")


def _sheet(ws, header, rows, widths=None):
    ws.append(header)
    for c in ws[1]:
        c.font = HEAD
        c.fill = FILL
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for r in rows:
        ws.append(list(r))
    if widths:
        for i, wd in enumerate(widths):
            ws.column_dimensions[openpyxl.utils.get_column_letter(i + 1)].width = wd
    ws.freeze_panes = "A2"


def register(w, path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Kegs"
    rows = []
    for k in w.kegs:
        if k.lot == "NEW":
            continue
        lot = w.lots[k.lot]
        st, sd = k.status, k.status_date
        rows.append((serial(k), k.size, k.lot, lot["bought"], tag_of(k) if k.tag else "", st,
                     sd if sd else None))
    _sheet(ws, ["serial", "size_l", "lot", "in_service", "tag_epc", "status", "status_date"], rows,
           [14, 8, 10, 12, 22, 14, 12])
    for r in ws.iter_rows(min_row=2, min_col=4, max_col=4):
        for c in r:
            c.number_format = "dd/mm/yyyy"
    for r in ws.iter_rows(min_row=2, min_col=7, max_col=7):
        for c in r:
            c.number_format = "dd/mm/yyyy"
    ws2 = wb.create_sheet("Lots")
    _sheet(ws2, ["lot", "size_l", "in_service", "kegs_bought", "maker", "tagged"],
           [(lot, v["size"], v["bought"], v["n"], "Lindqvist Fass" if v["bought"].year >= 2016 else "Northfield Kegs",
             "yes" if v["tagged"] else "no") for lot, v in w.lots.items()], [10, 8, 12, 12, 18, 8])
    ws3 = wb.create_sheet("Tag changes")
    _sheet(ws3, ["serial", "old_tag_epc", "new_tag_epc", "changed"],
           [(serial(w.kegs[kid]), tag_of(w.kegs[kid]), new, d) for kid, (d, new) in sorted(w.retag.items())],
           [14, 22, 22, 12])
    wb.save(path)


def stocktake(w, path):
    wb = openpyxl.Workbook()
    first = True
    for d in sorted(w.engine.sites):
        ws = wb.active if first else wb.create_sheet()
        first = False
        ws.title = "30 Nov %d" % d.year
        counts = w.engine.sites[d]
        sites = []
        for (site, cond, s), n in counts.items():
            if (site, cond) not in sites:
                sites.append((site, cond))
        rows = []
        for site, cond in sites:
            rows.append((site, cond) + tuple(counts.get((site, cond, s), 0) for s in P.SIZES))
        _sheet(ws, ["site", "condition", "50 l", "30 l", "20 l"], rows, [40, 18, 9, 9, 9])
        ws.append([])
        ws.append(["Counted on site at the close of %s; kegs at pubs and with other parties are not counted." %
                   d.strftime("%-d %B %Y")])
    wb.save(path)


def recovery(w, path):
    rng = np.random.default_rng(P.SEED + 19)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Returned"
    rows = []
    for d, kid, s in w.ev["back_recovery"]:
        k = w.kegs[kid]
        found = ["scrap metal dealer", "closed premises", "another brewer's yard", "festival site", "private address"][
            int(rng.choice(5, p=[0.38, 0.27, 0.2, 0.08, 0.07]))]
        sr = serial(k)
        if rng.random() < 0.3:
            sr = sr.replace("WB%d-" % k.size, "WB %d ").replace(" %d ", " %d " % k.size) if False else "WB %d %s" % (
                k.size, sr.split("-")[1])
        rows.append((d - dt.timedelta(days=int(rng.integers(3, 15))), sr, "%d L" % k.size, found, d))
    rows.sort(key=lambda r: r[4])
    _sheet(ws, ["found", "serial_as_read", "size", "where_found", "delivered_to_brighouse"], rows, [12, 16, 8, 24, 14])
    ws2 = wb.create_sheet("Monthly summary")
    agg = defaultdict(lambda: defaultdict(int))
    for d, kid, s in w.ev["back_recovery"]:
        agg[(d.year, d.month)][s] += 1
    _sheet(ws2, ["month", "50 l", "30 l", "20 l", "invoice_gbp"],
           [("%d-%02d" % ym, v[50], v[30], v[20], round(sum(v.values()) * 14.5, 2)) for ym, v in sorted(agg.items())],
           [10, 8, 8, 8, 12])
    wb.save(path)


def plan(w, plans, path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Maplestead pubs"
    rows = []
    for e in plans["estate"]:
        for code, r in e["lines"].items():
            rows.append((e["pub"], P.DEPOTS[e["depot"]], e["start"], code, w.sku_info[code][1], w.sku_info[code][2], r))
    _sheet(ws, ["pub", "depot", "first_delivery_week", "beer_code", "beer", "keg_l", "expected_kegs_per_week"], rows,
           [8, 22, 14, 8, 16, 7, 12])
    ws2 = wb.create_sheet("New Foundry taps")
    _sheet(ws2, ["account", "tap_from", "expected_kegs_per_week"],
           [(t["outlet"], t["start"], t["rate"]) for t in plans["foundry_taps"]], [10, 12, 12])
    ws3 = wb.create_sheet("Foundry range")
    _sheet(ws3, ["beer_code", "beer", "on_sale_from", "on_sale_to", "kegs_per_brew"],
           [(s, P.FOUNDRY_NAMES[s], a, b, P.FOUNDRY_LOT_2027) for s, (a, b) in plans["foundry_windows"].items()],
           [8, 26, 12, 12, 10])
    ws4 = wb.create_sheet("Foundry brews")
    rows = []
    for s, br in plans["foundry_brews"].items():
        for d, n in sorted(br.items()):
            rows.append((d, s, n, d + dt.timedelta(days=P.FOUNDRY_LEAD)))
    rows.sort()
    _sheet(ws4, ["brew_date", "beer_code", "kegs", "racking_date"], rows, [12, 8, 7, 12])
    ws5 = wb.create_sheet("Volume plan")
    _sheet(ws5, ["beer_code", "beer", "2026_hl_actual_to_nov", "2027_hl_plan", "note"], plans["volume"],
           [8, 22, 14, 12, 40])
    wb.save(path)


def cask(w, path):
    rng = np.random.default_rng(P.SEED + 20)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Casks"
    rows = []
    for i in range(5200):
        kind = "firkin (72 pt)" if rng.random() < 0.82 else "kilderkin (144 pt)"
        yr = int(rng.integers(1998, 2024))
        st = "ACTIVE" if rng.random() < 0.86 else ("WRITTEN_OFF" if rng.random() < 0.7 else "SCRAPPED")
        rows.append(("CK%05d" % (i + 1), kind, "steel" if yr < 2012 or rng.random() < 0.4 else "plastic", yr, st))
    _sheet(ws, ["cask_no", "type", "material", "year", "status"], rows, [10, 18, 9, 7, 13])
    wb.save(path)


# ------------------------------------------------------------------------------------------------- database
def erp(w, plans, path):
    rng = np.random.default_rng(P.SEED + 21)
    if os.path.exists(path):
        os.remove(path)
    con = sqlite3.connect(path)
    c = con.cursor()
    c.execute("""CREATE TABLE accounts (account TEXT PRIMARY KEY, trading_name TEXT, channel TEXT, pub_group TEXT,
                 depot TEXT, postcode_district TEXT, opened TEXT, closed TEXT, deposit_terms TEXT, season TEXT)""")
    c.execute("""CREATE TABLE account_changes (old_account TEXT, new_account TEXT, effective TEXT, reason TEXT)""")
    c.execute("""CREATE TABLE products (beer_code TEXT PRIMARY KEY, beer TEXT, style TEXT, keg_l INTEGER,
                 abv REAL, range TEXT, list_price_gbp REAL)""")
    c.execute("""CREATE TABLE delivery_schedule (account TEXT, depot TEXT, weekday TEXT, frequency TEXT,
                 valid_from TEXT, valid_to TEXT)""")
    c.execute("""CREATE TABLE dispense_lines (account TEXT, line_no INTEGER, beer_code TEXT, keg_l INTEGER, taps INTEGER,
                 installed TEXT, removed TEXT)""")
    c.execute("""CREATE TABLE deposit_ledger (account TEXT, month TEXT, keg_l INTEGER, kegs_charged INTEGER,
                 kegs_refunded INTEGER, balance_kegs INTEGER, balance_gbp REAL)""")
    c.execute("""CREATE TABLE depots (depot TEXT PRIMARY KEY, name TEXT, trunk_days TEXT)""")
    pc = {"BRG": ["HD6", "HX3", "HD5", "HX5", "HD2"], "LDS": ["LS6", "LS11", "LS28", "LS15", "LS9", "WF3"],
          "YRK": ["YO1", "YO10", "YO24", "YO26", "HG1", "YO61"], "SHF": ["S1", "S10", "S11", "S6", "S35", "S60"]}
    first = ["Royal", "Black", "Fleece", "Plough", "Woolpack", "Station", "Shoulder", "Cross Keys", "Rose", "Fox",
             "White Hart", "Bay Horse", "Malt", "Miners", "Railway", "Anchor", "Bridge", "Swan", "Grove", "Crown"]
    second = ["Inn", "Arms", "Tavern", "Hotel", "Bar", "Club", "Kitchen", "House"]
    WD = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
 
    for o in w.outlets:
        if o.estate or o.opened > P.ASOF:
            continue
        nm = "%s %s" % (first[int(rng.integers(0, len(first)))], second[int(rng.integers(0, len(second)))])
        if o.channel == "CLUB":
            nm = ["Cricket Club", "Golf Club", "Sports & Social", "Rugby Club", "Bowling Club", "Working Men's Club"][
                int(rng.integers(0, 6))]
            nm = "%s %s" % (["Ossett", "Elland", "Batley", "Ripon", "Pudsey", "Thirsk", "Penistone", "Otley"][
                int(rng.integers(0, 8))], nm)
        terms = "DEPOSIT" if o.channel == "FREE" else "EXEMPT"
        closed = o.closed.isoformat() if o.closed and o.closed <= P.ASOF else None
        seas = "APR-OCT" if o.seasonal else "ALL YEAR"
        dist = pc[o.depot][int(rng.integers(0, len(pc[o.depot])))]
        if o.renumbered and o.renumbered <= P.ASOF:
            c.execute("INSERT INTO accounts VALUES (?,?,?,?,?,?,?,?,?,?)",
                      (o.id, nm, o.channel, o.group, o.depot, dist, o.opened.isoformat(), o.renumbered.isoformat(),
                       terms, seas))
            new = account_of(o, o.renumbered)
            c.execute("INSERT INTO accounts VALUES (?,?,?,?,?,?,?,?,?,?)",
                      (new, nm, o.channel, o.group, o.depot, dist, o.renumbered.isoformat(), closed, terms, seas))
            c.execute("INSERT INTO account_changes VALUES (?,?,?,?)",
                      (o.id, new, o.renumbered.isoformat(), "change of licensee"))
            accts = [(o.id, o.opened, o.renumbered), (new, o.renumbered, o.closed)]
        else:
            c.execute("INSERT INTO accounts VALUES (?,?,?,?,?,?,?,?,?,?)",
                      (o.id, nm, o.channel, o.group, o.depot, dist, o.opened.isoformat(), closed, terms, seas))
            accts = [(o.id, o.opened, o.closed)]
        for acc, a, b in accts:
            for wd in o.days:
                c.execute("INSERT INTO delivery_schedule VALUES (?,?,?,?,?,?)",
                          (acc, o.depot, WD[wd], "weekly" if o.interval == 7 else "twice weekly", a.isoformat(),
                           b.isoformat() if b and b <= P.ASOF else None))
        for i, ln in enumerate(o.lines):
            inst = max(o.opened, dt.date(2015, 1, 1)) + dt.timedelta(days=int(rng.integers(0, 60)))
            c.execute("INSERT INTO dispense_lines VALUES (?,?,?,?,?,?,?)",
                      (account_of(o, P.ASOF), i + 1, "FOUNDRY" if ln.foundry else ln.sku, ln.size, ln.taps,
                       inst.isoformat(), closed))
    for code, name, size, style, tk, xm in P.SKUS:
        c.execute("INSERT INTO products VALUES (?,?,?,?,?,?,?)",
                  (code, name, style, size, {"PIL": 4.4, "GLD": 3.8, "PAL": 4.2, "IPA": 5.6, "HER": 4.8, "BLK": 4.1}[code],
                   "core", {50: 128.0, 30: 96.0}[size]))
    for s in sorted(P.FOUNDRY_NAMES):
        c.execute("INSERT INTO products VALUES (?,?,?,?,?,?,?)",
                  (s, P.FOUNDRY_NAMES[s], "small batch", 20, round(float(rng.uniform(4.0, 6.8)), 1), "Foundry",
                   88.0))
    for dp, name in P.DEPOTS.items():
        c.execute("INSERT INTO depots VALUES (?,?,?)",
                  (dp, name, ",".join(WD[i] for i in P.TRUNK_WEEKDAYS[dp])))
    dep = {50: 30.0, 30: 25.0, 20: 20.0}
    outlets = {o.id: o for o in w.outlets}
    led = defaultdict(lambda: [0, 0])
    for d, oid, depot, deliv, coll, foreign in w.ev["visit"]:
        o = outlets[oid]
        if o.channel != "FREE" or d < P.DEPOSIT_DAY:
            continue
        for s in P.SIZES:
            if deliv[s] or coll[s]:
                x = led[(account_of(o, d), "%d-%02d" % (d.year, d.month), s)]
                x[0] += deliv[s]
                x[1] += min(coll[s] + foreign[s], deliv[s] + coll[s])
    bal = defaultdict(int)
    for (acc, m, s), (ch, rf) in sorted(led.items(), key=lambda t: (t[0][0], t[0][2], t[0][1])):
        bal[(acc, s)] += ch - rf
        c.execute("INSERT INTO deposit_ledger VALUES (?,?,?,?,?,?,?)",
                  (acc, m, s, ch, rf, bal[(acc, s)], round(bal[(acc, s)] * dep[s], 2)))
    con.commit()
    c.execute("VACUUM")
    con.close()
