"""task7 architecture 11: the pack's data files, each written the way the system that keeps it writes it."""
import csv
import datetime as dt
import os

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Font

import postprocess
import world as W

MDT = dt.timezone(dt.timedelta(hours=-6))
MST = dt.timezone(dt.timedelta(hours=-7))
UTC = dt.timezone.utc
ORG = "Hollins Creek Electric Association"
SUBST = {"Prairie Hollow": "PHW", "Larkin Ridge": "LKR", "Stonebrook": "STB"}
STREETS = ["Juniper", "Sage", "Buckskin", "Yucca", "Pronghorn", "Kestrel", "Bluestem", "Wagon Wheel", "Saddle", "Cottonwood",
           "Prairie Star", "Thunderhead", "Antelope", "Meadowlark", "Rimrock", "Sandstone", "Larkspur", "Aspen", "Coyote",
           "Plum Creek", "Elk Ridge", "Granite", "Clover", "Windmill", "Silver Sage", "Ponderosa", "Red Hawk", "Big Sky"]
SUFFIX = ["St", "Dr", "Ln", "Ct", "Way", "Cir", "Trl", "Pl", "Ave"]
MAKES = {7.2: [("Voltlane", "HC32"), ("Ampwright", "Home 32")], 9.6: [("Voltlane", "HC40"), ("Corrin", "Wallbox 40")],
         11.5: [("Ampwright", "Home 48"), ("Corrin", "Wallbox 48"), ("Voltlane", "HC48")]}


def write_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        wr = csv.writer(fh, lineterminator="\r\n")
        wr.writerow(header)
        for r in rows:
            wr.writerow(r)


def ids(w, rng):
    """service points, meters, transformer locations, charger serials, accounts and addresses"""
    loc = []
    used = set()
    for t in w.tx:
        a = W.AREAS[t["area"]]["prefix"]
        while True:
            k = "%s-%04d" % (a, int(rng.integers(1000, 9999)))
            if k not in used:
                used.add(k)
                break
        loc.append(k)
    w.loc = loc
    H = len(w.homes)
    sp = rng.choice(np.arange(3100000, 3999999), size=H, replace=False)
    w.sp = ["%d" % s for s in sp]
    mt = rng.choice(np.arange(410000000, 489999999), size=H + len(w.exchanged) + 5, replace=False)
    w.meter = ["%d" % m for m in mt[:H]]
    w.new_meter = {}
    k = H
    for hi in sorted(w.exchanged):
        w.new_meter[hi] = "%d" % mt[k]
        k += 1
    w.acct = ["%07d" % a for a in rng.choice(np.arange(1100000, 1899999), size=H, replace=False)]
    seen = set()
    w.addr = []
    for hi, h in enumerate(w.homes):
        while True:
            a = "%d %s %s" % (int(rng.integers(100, 9800)), STREETS[int(rng.integers(0, len(STREETS)))],
                              SUFFIX[int(rng.integers(0, len(SUFFIX)))])
            if a not in seen:
                seen.add(a)
                break
        w.addr.append(a)
    # charger serials (a swapped charger gets a second serial from its swap date)
    w.serial, w.serial2, w.make = [], {}, []
    for ci, c in enumerate(w.chargers):
        mk, md = MAKES[c["power"]][int(rng.integers(0, len(MAKES[c["power"]])))]
        w.make.append((mk, md))
        w.serial.append("%s-%s%06d" % (mk[:2].upper(), md[-2:], int(rng.integers(0, 999999))))
        if c["swap"] is not None:
            w.serial2[ci] = "%s-%s%06d" % (mk[:2].upper(), md[-2:], int(rng.integers(0, 999999)))


def serial_on(w, ci, d):
    c = w.chargers[ci]
    if c["swap"] is not None and d >= c["swap"]:
        return w.serial2[ci]
    return w.serial[ci]


def ami_files(w, rng, target):
    """the meter data system's hourly export, one file per substation: hour-ending columns, local time, net kWh"""
    tot = (w.B + w.U + w.A).astype(np.float64)
    H = len(w.homes)
    hourly = tot[:, :W.NDAY * W.Q].reshape(H, W.NDAY, 24, 4).mean(axis=3)       # kW averaged over the hour = kWh in it
    rows = {a: [] for a in SUBST}
    counts = {}
    est_total = 0
    for hi, h in enumerate(w.homes):
        area = h["area"]
        ex = w.exchanged.get(hi)
        exh = int(rng.integers(8, 16))
        for d in range(W.NDAY):
            day = W.JUL1 + dt.timedelta(days=d)
            v = hourly[hi, d].copy()
            miss = rng.random(24) < 0.006
            if rng.random() < 0.004:
                s = int(rng.integers(0, 20))
                miss[s:s + int(rng.integers(3, 6))] = True
            est = 0
            if miss.any() and not miss.all():
                good = np.where(~miss)[0]
                v[miss] = np.interp(np.where(miss)[0], good, v[good])
                est = int(miss.sum())
                est_total += est
            vals = ["%.3f" % x for x in v]
            status = "E" if est else "A"
            if ex is not None and day == ex:
                old = vals[:exh] + [""] * (24 - exh)
                new = [""] * exh + vals[exh:]
                rows[area].append([w.meter[hi], day.isoformat(), "KWH", status, est] + old)
                rows[area].append([w.new_meter[hi], day.isoformat(), "KWH", status, est] + new)
            else:
                m = w.new_meter[hi] if (ex is not None and day > ex) else w.meter[hi]
                rows[area].append([m, day.isoformat(), "KWH", status, est] + vals)
    # a re-sent block in each export: forty meter-days delivered twice
    for area, rr in rows.items():
        k0 = int(rng.integers(0, len(rr) - 400))
        rr[k0 + 200:k0 + 200] = [list(x) for x in rr[k0:k0 + 40]]
        hdr = ["meter_no", "read_date", "uom", "day_status", "estimated_hours"] + ["he%02d" % k for k in range(1, 25)]
        name = "mdm_hourly_%s_2026-07-01_2026-08-31.csv" % SUBST[area].lower()
        write_csv(os.path.join(target, name), hdr, rr)
        counts[name] = len(rr)
    counts["estimated_hours"] = est_total
    return counts


def sessions_file(w, rng, target):
    """Quillpoint's charging-session export: every enrolled charger's sessions, June to September 2024 to 2026, in UTC"""
    rows = []
    sid = 7000000
    for ci, c in enumerate(w.chargers):
        for (d, plug, dep, e, pm, dm), a in zip(w.sess[ci], w.act[ci]):
            if a is None:
                continue
            p = c["power"]
            base = dt.datetime(d.year, d.month, d.day, tzinfo=MDT)
            pin = base + dt.timedelta(minutes=pm)
            st = base + dt.timedelta(minutes=15 * a["start"])
            en = st + dt.timedelta(minutes=e / p * 60)
            unp = base + dt.timedelta(minutes=dm)
            if unp < en:
                unp = en + dt.timedelta(minutes=int(rng.integers(1, 9)))
            mode = {"managed": "QP_STAGGER", "t2300": "CHARGER_SCHEDULE", "t2330": "CHARGER_SCHEDULE",
                    "t0000": "CHARGER_SCHEDULE", "ready": "VEHICLE_SCHEDULE", "now": "IMMEDIATE"}[a["mode"]]
            ready = ""
            if a["ready"] is not None:
                ready = (base + dt.timedelta(minutes=15 * a["ready"])).strftime("%H:%M")
            sid += int(rng.integers(1, 4))
            rows.append(["QS%d" % sid, serial_on(w, ci, d), pin.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
                         st.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"), en.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
                         unp.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"), "%.2f" % e, "%.1f" % (p * float(rng.uniform(0.97, 1.0))),
                         mode, ready])
            if rng.random() < 0.008:                       # plugged in again for a few minutes, nothing drawn
                t0 = unp + dt.timedelta(minutes=int(rng.integers(20, 300)))
                sid += 1
                rows.append(["QS%d" % sid, serial_on(w, ci, d), t0.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"), "", "",
                             (t0 + dt.timedelta(minutes=int(rng.integers(3, 25)))).astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
                             "0.00", "0.0", mode, ready])
    rows.sort(key=lambda r: (r[2], r[1]))
    # a re-sent batch: one night's sessions delivered twice in the 2026 export
    k = [i for i, r in enumerate(rows) if r[2].startswith("2026-08-1")]
    if k:
        rows[k[-1] + 1:k[-1] + 1] = [list(r) for r in rows[k[0]:k[0] + 120]]
    hdr = ["session_id", "charger_serial", "plugged_in_utc", "charge_start_utc", "charge_end_utc", "unplugged_utc", "energy_kwh",
           "peak_kw", "control_mode", "ready_by_local"]
    write_csv(os.path.join(target, "quillpoint_sessions_2024-06_2026-09.csv"), hdr, rows)
    return len(rows)


DECLARED = {"t2300": "Charger timer 23:00", "t2330": "Charger timer 23:30", "t0000": "Charger timer 00:00",
            "ready": "Car's departure schedule", "now": "When I plug in"}


def roster_file(w, rng, target):
    rows = []
    for ci, c in enumerate(w.chargers):
        hi = c["home"]
        mk, md = w.make[ci]
        status = "Active" if c["left"] is None else "Closed"
        closed = c["left"].isoformat() if c["left"] is not None else ""
        decl = DECLARED[c["declared"]]
        rows.append([w.acct[hi], w.sp[hi], w.serial[ci], mk, md, "%.1f" % c["power"], c["enrol"].isoformat(),
                     "Replaced" if c["swap"] is not None else status,
                     c["swap"].isoformat() if c["swap"] is not None else closed, "", decl])
        if c["swap"] is not None:
            rows.append([w.acct[hi], w.sp[hi], w.serial2[ci], mk, md, "%.1f" % c["power"], c["swap"].isoformat(), status, closed,
                         w.serial[ci], decl])
    # a re-imported block: some members' rows twice, the second time with the account number unpadded
    extra = []
    for k in rng.choice(len(rows), size=14, replace=False):
        r = list(rows[int(k)])
        r[0] = str(int(r[0]))
        extra.append(r)
    rows += extra
    rows.sort(key=lambda r: (r[6], r[2]))
    hdr = ["member_account", "service_point", "charger_serial", "make", "model", "rated_kw", "enrolled_on", "status",
           "status_date", "replaces_serial", "usual_charging_at_enrolment"]
    write_csv(os.path.join(target, "ev_overnight_roster_2026-11-02.csv"), hdr, rows)
    return len(rows)


def assignment_file(w, target):
    rows = []
    for ci, c in enumerate(w.chargers):
        on = max(W.RAND_DAY, c["enrol"])
        rows.append([w.serial[ci], "Stagger" if c["arm"] == "managed" else "Own schedule", on.isoformat(),
                     "2025-05 split" if c["enrol"] < W.RAND_DAY else "at enrolment"])
    rows.sort(key=lambda r: r[0])
    write_csv(os.path.join(target, "pilot_assignment_2025.csv"), ["charger_serial", "pilot_half", "assigned_on", "assignment"], rows)


def gis_file(w, rng, target):
    """the GIS export: each service point's current meter and the transformer location it is drawn on"""
    lag = w.splits[-1]                    # the last split's transfers not yet posted to the GIS
    rows = []
    for hi, h in enumerate(w.homes):
        t = h["tx"]
        if hi in lag["moved"]:
            t = lag["parent"]
        m = w.new_meter.get(hi, w.meter[hi])
        tt = w.tx[t]
        rows.append([w.sp[hi], m, w.addr[hi], "PRAIRIE HOLLOW" if tt["area"] == "Prairie Hollow" else "HOLLINS CREEK", w.loc[t],
                     SUBST[tt["area"]], "%s-%d" % (SUBST[tt["area"]], 1 + (t % 4)), "ABC"[t % 3]])
    rows.sort(key=lambda r: r[0])
    write_csv(os.path.join(target, "gis_service_points_2026-10-30.csv"),
              ["service_point", "meter_no", "premise_address", "city", "transformer_location", "substation", "feeder", "phase"], rows)


def exchange_file(w, rng, target):
    rows = []
    for hi in sorted(w.exchanged):
        d = w.exchanged[hi]
        rows.append([w.sp[hi], w.meter[hi], w.new_meter[hi], d.isoformat(), "%02d:%02d" % (int(rng.integers(8, 16)), int(rng.integers(0, 60))),
                     str(rng.choice(["Failed register", "Comms failure", "Damaged glass", "Recall batch 22-7"]))])
    write_csv(os.path.join(target, "ami_meter_exchanges_2026.csv"),
              ["service_point", "old_meter_no", "new_meter_no", "exchanged_on", "time_local", "reason"], rows)


def register_file(w, rng, target):
    rows = []
    lagging = set(w.replaced[:3])
    for t in w.tx:
        kva = t["kva"]
        year = t["year"]
        if t["idx"] in lagging:
            kva = t["old_kva"]
        elif "replaced_on" in t:
            year = 2026
        mf = str(rng.choice(["Ermco", "Howard", "Central Moloney", "Eaton"]))
        rows.append([w.loc[t["idx"]], SUBST[t["area"]], "Pole-mount" if t["mount"] == "pole" else "Pad-mount", "1",
                     ("%g" % kva), year, mf, "%s%07d" % (mf[:2].upper(), int(rng.integers(0, 9999999)))])
    rows.sort(key=lambda r: r[0])
    write_csv(os.path.join(target, "transformer_register_2026.csv"),
              ["transformer_location", "substation", "mount", "phases", "kva", "installed", "manufacturer", "unit_serial"], rows)


def work_orders(w, rng, target):
    wb = Workbook()
    ws = wb.active
    ws.title = "Completed work orders"
    ws.append(["work_order", "type", "transformer_location", "service_point", "detail", "completed_on", "crew"])
    rows = []
    for x in w.replaced:
        t = w.tx[x]
        rows.append(["WO-%d" % int(rng.integers(260000, 269999)), "Transformer change-out", w.loc[x], "",
                     "Replaced %g kVA with %g kVA" % (t["old_kva"], t["kva"]), t["replaced_on"], str(rng.choice(["Line 2", "Line 4"]))])
    for sp in w.splits:
        rows.append(["WO-%d" % int(rng.integers(260000, 269999)), "New transformer", w.loc[sp["child"]], "",
                     "Set %g kVA %s-mount" % (w.tx[sp["child"]]["kva"], w.tx[sp["child"]]["mount"]), sp["on"], "Line 3"])
        for hi in sp["moved"]:
            rows.append(["WO-%d" % int(rng.integers(260000, 269999)), "Service transfer", w.loc[sp["child"]], w.sp[hi],
                         "Service moved from %s" % w.loc[sp["parent"]], sp["on"] + dt.timedelta(days=int(rng.integers(0, 3))), "Line 3"])
    for k in range(60):
        typ = str(rng.choice(["Pole replacement", "Vegetation", "Meter base repair", "Streetlight", "Underground locate"]))
        rows.append(["WO-%d" % int(rng.integers(250000, 269999)), typ, w.loc[int(rng.integers(0, len(w.tx)))], "",
                     "", dt.date(2025, 3, 1) + dt.timedelta(days=int(rng.integers(0, 600))), str(rng.choice(["Line 1", "Line 2", "Line 4", "Contract"]))])
    rows.sort(key=lambda r: r[5])
    for r in rows:
        ws.append(r)
    for c in ws[1]:
        c.font = Font(bold=True)
    for col, wd in zip("ABCDEFG", (11, 22, 20, 14, 34, 13, 10)):
        ws.column_dimensions[col].width = wd
    for row in ws.iter_rows(min_row=2, min_col=6, max_col=6):
        for c in row:
            c.number_format = "yyyy-mm-dd"
    path = os.path.join(target, "distribution_work_orders_2025_2026.xlsx")
    wb.save(path)
    postprocess.normalize_ooxml(path, "Glenda Thompson", "Sandra Bernard", "2025-03-03T15:12:00Z", "2026-10-29T17:44:00Z",
                                "Completed work orders", excel=True, company=ORG)


def monitors_file(w, rng, target):
    """the 48 monitored transformers' 15-minute load, interval-ending, local time"""
    tot = (w.B + w.U + w.A).astype(np.float64)
    rows = []
    for x in w.monitored:
        hs = [hi for hi, h in enumerate(w.homes) if h["tx"] == x]
        kw = tot[hs, :W.NDAY * W.Q].sum(0) * 1.012 + 0.06
        pf = np.clip(0.975 - 0.024 * (kw / max(kw.max(), 1)) + rng.normal(0, 0.004, kw.size), 0.92, 0.99)
        kva = np.abs(kw) / pf                      # apparent power has no sign; solar exports show as negative kW
        gap = rng.random(kw.size) < 0.004
        for d in range(W.NDAY):
            day = (W.JUL1 + dt.timedelta(days=d)).isoformat()
            sl = slice(d * W.Q, (d + 1) * W.Q)
            rows.append([w.loc[x], day, "kW"] + ["" if g else "%.1f" % v for v, g in zip(kw[sl], gap[sl])])
            rows.append([w.loc[x], day, "kVA"] + ["" if g else "%.1f" % v for v, g in zip(kva[sl], gap[sl])])
    hdr = ["transformer_location", "date", "quantity"] + ["%02d:%02d" % divmod(15 * (k + 1), 60) for k in range(W.Q)]
    write_csv(os.path.join(target, "transformer_monitors_15min_2026-07_08.csv"), hdr, rows)
    return len(rows)


def weather_file(w, rng, target):
    rows = []
    for year in (2024, 2025, 2026):
        wx = w.wx[year]
        for k, d in enumerate(wx["days"]):
            for h in range(24):
                t = wx["hourly"][k * 24 + h]
                rh = float(np.clip(70 - 1.1 * (t - 55) + rng.normal(0, 6), 8, 98))
                rows.append(["HCEA-WX1", d.isoformat(), "%02d:00" % h, "%.1f" % t, "%.0f" % rh])
    write_csv(os.path.join(target, "weather_station_hourly_2024-2026.csv"),
              ["station", "date_lst", "hour_lst", "dry_bulb_f", "rel_humidity_pct"], rows)


def quote_file(w, target):
    wb = Workbook()
    ws = wb.active
    ws.title = "2027 proposal"
    ws.append(["product", "what it does each night", "fee per enrolled charger per year (USD)", "what the association provides"])
    ws.append(["Quillpoint Stagger",
               "Starts each session at a random time, drawn evenly over the quarter-hours from the later of plug-in and 23:00 "
               "to the latest start that still finishes by the member's ready-by time; the session then charges without a "
               "break. The same as the pilot's managed half.", W.FEE["stagger"], "The enrolled chargers"])
    ws.append(["Quillpoint Sequence",
               "On each transformer, charges the enrolled chargers one at a time from the later of plug-in and 23:00, in the "
               "order of their ready-by times (the one plugged in first where two share a ready-by time), each starting when "
               "every charger before it in that order has finished; a charger that could not otherwise finish by its ready-by "
               "time starts at its latest start, alongside whichever are charging.",
               W.FEE["sequence"], "The enrolled chargers and the transformer each one is on"])
    ws.append([])
    ws.append(["Fees are quoted on the chargers enrolled on the EV Overnight rate on 1 November 2026, for calendar 2027."])
    ws.append(["Members cannot pause a managed session; the ready-by time is set in the Quillpoint app."])
    ws.append(["Both products start a session only on the quarter-hour."])
    for c in ws[1]:
        c.font = Font(bold=True)
    for col, wd in zip("ABCD", (20, 90, 18, 34)):
        ws.column_dimensions[col].width = wd
    path = os.path.join(target, "quillpoint_proposal_2027.xlsx")
    wb.save(path)
    postprocess.normalize_ooxml(path, "Joshua Baker", "Joshua Baker", "2026-10-14T19:02:00Z", "2026-10-27T16:48:00Z",
                                "Hollins Creek EA: 2027 managed charging proposal", excel=True, company="Quillpoint")


def registrations_file(w, rng, target):
    rows = []
    zips = ["80601", "80603", "80621", "80640", "80642", "80643", "80651"]
    for z in zips:
        n = float(rng.uniform(60, 240))
        for y in range(2019, 2027):
            for q in (1, 2, 3, 4):
                if y == 2026 and q == 4:
                    continue
                n *= float(rng.uniform(1.04, 1.11))
                rows.append([z, "%dQ%d" % (y, q), int(n * 0.72), int(n * 0.28)])
    write_csv(os.path.join(target, "state_ev_registrations_by_zip_2019-2026.csv"), ["zip", "quarter", "bev", "phev"], rows)


def solar_file(w, rng, target):
    rows = []
    for hi, h in enumerate(w.homes):
        if h["pv"]:
            rows.append([w.sp[hi], "%.1f" % h["pv"], "%.1f" % (h["pv"] * 0.82),
                         str(rng.choice(["Net metering", "Net metering", "Net metering (legacy)"])),
                         (dt.date(2017, 1, 1) + dt.timedelta(days=int(rng.integers(0, 3400)))).isoformat()])
    rows.sort(key=lambda r: r[4])
    write_csv(os.path.join(target, "net_metering_interconnections_2026.csv"),
              ["service_point", "dc_kw", "ac_kw", "program", "interconnected_on"], rows)


def write_all(w, target):
    rng = np.random.default_rng(W.SEED + 11)
    ids(w, rng)
    counts = {}
    counts.update(ami_files(w, rng, target))
    counts["sessions"] = sessions_file(w, rng, target)
    counts["roster"] = roster_file(w, rng, target)
    assignment_file(w, target)
    gis_file(w, rng, target)
    exchange_file(w, rng, target)
    register_file(w, rng, target)
    work_orders(w, rng, target)
    counts["monitor_rows"] = monitors_file(w, rng, target)
    weather_file(w, rng, target)
    quote_file(w, target)
    registrations_file(w, rng, target)
    solar_file(w, rng, target)
    return counts
