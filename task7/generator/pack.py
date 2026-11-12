"""task7 architecture 10: the pack's data files, each written as the system that keeps it writes it."""
import csv
import datetime as dt
import os

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Font

import postprocess
import world as W

CT = dt.timezone(dt.timedelta(hours=-5))          # Central daylight time, all summer
UTC = dt.timezone.utc
STREETS = ["Oak", "Mesquite", "Pecan", "Live Oak", "Cypress", "Bluebonnet", "Ranch", "Hill Country", "Lakeview", "Granite",
           "Post Oak", "Elm", "Cedar", "Sycamore", "Prairie", "Spring", "Bridle", "Quail", "Dove", "Wildflower", "Limestone",
           "Turkey Creek", "Crystal", "Deer", "Sunset", "Canyon", "Arrowhead", "Juniper", "Mockingbird", "Shady Grove"]
TYPES = [("ST", "STREET"), ("DR", "DRIVE"), ("LN", "LANE"), ("TRL", "TRAIL"), ("CT", "COURT"), ("RD", "ROAD"), ("LOOP", "LOOP"),
         ("PASS", "PASS"), ("CV", "COVE")]
CITIES_N = [("Marble Ridge", "78654"), ("Spicewood Hills", "78669"), ("Liberty Grove", "78611")]
CITIES_S = [("Calder", "78605"), ("Bertram Flats", "78605"), ("Oatmeal Creek", "78605"), ("Shovel Mountain", "78636")]
RCH = {"app": "Provider app", "mail": "Co-op mailer", "retail": "Retail instant rebate"}
MODELS = {"Corvane": ["Corvane C3", "Corvane C4 Pro"], "Lumivale": ["Lumivale One", "Lumivale Mini"],
          "Ardena": ["Ardena T2", "Ardena T2+"], "Ondera": ["Ondera Smart 5"], "Kitebrook": ["Kitebrook K7", "Kitebrook K9"],
          "Pinecrest Home": ["Pinecrest Home Smart", "Pinecrest Home Smart Lite"]}


def addresses(w, rng):
    """every parcel's situs: the appraisal district's form and the co-op's form of the same address"""
    n = len(w.parcel["south"])
    cad, coop, city = [], [], []
    for k in range(n):
        south = bool(w.parcel["south"][k])
        if south and rng.random() < 0.45:
            road = int(rng.integers(100, 480))
            num = int(rng.integers(100, 9900))
            if rng.random() < 0.7:
                cad.append("%d COUNTY ROAD %d" % (num, road))
                coop.append("%d CR %d" % (num, road))
            else:
                fm = int(rng.choice([1431, 243, 963, 2341, 3509]))
                cad.append("%d FM %d" % (num, fm))
                coop.append("%d FARM TO MARKET %d" % (num, fm) if rng.random() < 0.5 else "%d FM RD %d" % (num, fm))
        else:
            num = int(rng.integers(100, 4800))
            st = STREETS[int(rng.integers(0, len(STREETS)))]
            ab, full = TYPES[int(rng.integers(0, len(TYPES)))]
            cad.append("%d %s %s" % (num, st.upper(), full))
            coop.append("%d %s %s" % (num, st.title(), ab.title()))
        c = (CITIES_S if south else CITIES_N)[int(rng.integers(0, 3 if not south else 4))]
        city.append(c)
    # make the CAD forms unique
    seen = {}
    for k, a in enumerate(cad):
        key = (a, city[k][0])
        if key in seen:
            num = int(a.split(" ")[0]) + 2 * (seen[key] + 1)
            rest = a.split(" ", 1)[1]
            cad[k] = "%d %s" % (num, rest)
            coop[k] = "%d %s" % (num, coop[k].split(" ", 1)[1])
            seen[key] += 1
        else:
            seen[key] = 0
    w.cad_addr, w.coop_addr, w.city = cad, coop, city


def ids(w, rng):
    """account and meter numbers; the provider's own device ids, some replaced; the research sample's meter exchanges"""
    n = len(w.parcel["south"])
    w.acct = {int(h): 1000000 + int(k) * 7 + int(rng.integers(0, 7)) for k, h in enumerate(w.member)}
    w.meter = {int(h): 60000000 + int(rng.integers(0, 9999999)) for h in w.member}
    w.prog_id = {r["i"]: "PP-%05d" % (r["i"] + 1000) for r in w.dev}

    def dev_id(p, k):
        if p == "Corvane":
            return "CVN-%06X" % (0x3A0000 + k * 37)
        if p == "Lumivale":
            return "LV%09d" % (200000000 + k * 113)
        if p == "Ardena":
            return "ARD-%08x" % (0x1f000000 + k * 7919)
        if p == "Ondera":
            return "OND%07d" % (4400000 + k * 3)
        if p == "Kitebrook":
            return "KB-%05d" % (10000 + k)
        return "PH%08d" % (30000000 + k * 11)
    w.dev_id, w.dev_prev = {}, {}
    for r in w.dev:
        w.dev_id[r["i"]] = dev_id(r["p"], r["i"])
        if rng.random() < 0.04 and r["joined"] < dt.date(2025, 6, 1):
            # the thermostat was swapped for a new one; reports before the swap carry the old id
            when = r["joined"] + dt.timedelta(days=int(rng.integers(120, 700)))
            if when < dt.date(2026, 10, 1) and (r["left"] is None or when < r["left"]):
                w.dev_prev[r["i"]] = (dev_id(r["p"], r["i"] + 50000), when)
    # 15-minute meters exchanged in the research sample during 2025
    w.meter_prev = {}
    for h in w.ami_homes:
        if rng.random() < 0.03:
            w.meter_prev[h] = (60000000 + int(rng.integers(0, 9999999)), dt.date(2025, int(rng.integers(3, 11)), 15))


def write_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        wr = csv.writer(fh, lineterminator="\r\n")
        wr.writerow(header)
        for r in rows:
            wr.writerow(r)


def ami_file(w, rng, target):
    mins = np.arange(W.AMI_FROM, W.AMI_TO, W.STEP)
    cols = ["kwh_%02d%02d" % divmod(m + W.STEP, 60) for m in mins]
    rows = []
    for h in w.ami_homes:
        for d in w.ami_days:
            v = w.ami_load[(h, d)]
            m = w.meter[h]
            if h in w.meter_prev and d < w.meter_prev[h][1]:
                m = w.meter_prev[h][0]
            vals = ["%.3f" % x for x in v]
            if rng.random() < 0.004:
                for j in rng.choice(len(vals), int(rng.integers(1, 4)), replace=False):
                    vals[j] = ""
            rows.append([m, d.strftime("%Y-%m-%d")] + vals)
            if rng.random() < 0.002:
                rows.append([m, d.strftime("%Y-%m-%d")] + vals)          # the day re-sent by the head end
    rows.sort(key=lambda r: (r[1], r[0]))
    write_csv(os.path.join(target, "ami_15min_reads_peak_partners_2024_2026.csv"), ["meter_number", "read_date"] + cols, rows)
    return len(rows)


def accounts_file(w, rng, target):
    rows = []
    sub_n = ["Marble Ridge North", "Liberty Grove"]
    sub_s = ["Calder", "Shovel Mountain", "Oatmeal Creek"]
    ami = set(w.ami_homes)
    for h in w.member:
        h = int(h)
        south = bool(w.parcel["south"][h])
        typ = "15-minute" if h in ami else ("15-minute" if (not south and rng.random() < 0.08) else "hourly")
        prev, setd = "", "2019-%02d-%02d" % (int(rng.integers(3, 12)), int(rng.integers(1, 28)))
        if h in w.meter_prev:
            prev, setd = w.meter_prev[h][0], w.meter_prev[h][1].strftime("%Y-%m-%d")
        elif typ == "15-minute":
            setd = "2023-%02d-%02d" % (int(rng.integers(2, 10)), int(rng.integers(1, 28)))
        sub = (sub_s if south else sub_n)[int(rng.integers(0, 3 if south else 2))]
        rows.append([w.acct[h], w.coop_addr[h], w.city[h][0], w.city[h][1], w.meter[h], typ, setd, prev, sub,
                     "RES" if rng.random() < 0.93 else "RES-TOU"])
    write_csv(os.path.join(target, "member_accounts_2026.csv"),
              ["account_number", "service_address", "city", "zip", "meter_number", "meter_type", "meter_set_date",
               "prior_meter_number", "substation", "rate_code"], rows)


def roster_file(w, rng, target):
    rows = []
    for r in w.dev:
        prev = w.dev_prev.get(r["i"])
        rows.append([w.prog_id[r["i"]], w.acct[r["home"]], r["p"], w.dev_id[r["i"]],
                     r["joined"].strftime("%Y-%m-%d"), r["left"].strftime("%Y-%m-%d") if r["left"] else "",
                     RCH[r["ch"]], MODELS[r["p"]][int(rng.integers(0, len(MODELS[r["p"]])))],
                     prev[0] if prev else "", prev[1].strftime("%Y-%m-%d") if prev else ""])
    dup = [list(rows[int(k)]) for k in rng.choice(len(rows), 37, replace=False)]
    rows += dup                                                     # rows written twice by the 2025 re-import
    rows.sort(key=lambda x: (x[2], x[4], x[0]))
    write_csv(os.path.join(target, "peak_partners_roster_2026-10-30.csv"),
              ["program_id", "account_number", "provider", "device_id", "enrolled_on", "unenrolled_on", "channel",
               "thermostat_model", "previous_device_id", "device_changed_on"], rows)
    return len(rows)


def did_on(w, r, d):
    prev = w.dev_prev.get(r["i"])
    return prev[0] if (prev and d < prev[1]) else w.dev_id[r["i"]]


def hhmm(minute):
    return "%02d:%02d" % divmod(int(minute), 60)


def local_dt(d, minute, sec=0):
    return dt.datetime(d.year, d.month, d.day, int(minute) // 60, int(minute) % 60, sec, tzinfo=CT)


def provider_reports(w, rng, target):
    """each provider's event report, in its own layout: a row per device it dispatched (both halves of nothing: on a test
    event only the called half), with what happened"""
    counts = {}
    for p in W.PROVIDERS:
        q = W.PROG[p]
        rows = []
        for e in w.events:
            d = e["date"]
            for r in w.dev:
                if r["p"] != p:
                    continue
                out = w.out.get((e["id"], r["i"]))
                if out is None or not out[0]:
                    continue
                called, offline, ov = out
                dv = did_on(w, r, d)
                sec = int(rng.integers(0, 60))
                if p == "Corvane":
                    ref = "CBEC-%s-%s" % (d.strftime("%m%d"), "PK" if e["kind"] == "alert" else "MV")
                    st = local_dt(d, q["s"]).astimezone(UTC)
                    en = local_dt(d, q["e"]).astimezone(UTC)
                    oo = local_dt(d, ov, sec).astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ") if ov is not None else ""
                    rows.append([ref, st.strftime("%Y-%m-%dT%H:%M:%SZ"), en.strftime("%Y-%m-%dT%H:%M:%SZ"), dv,
                                 "N" if offline else "Y", oo])
                elif p == "Lumivale":
                    rows.append([d.strftime("%Y-%m-%d"), "Cedar Brake PP", dv, "not_delivered" if offline else "delivered",
                                 hhmm(ov) if ov is not None else ""])
                elif p == "Ardena":
                    out_s = "Offline" if offline else ("Opted Out" if ov is not None else "Completed")
                    ts = local_dt(d, ov, sec).strftime("%m/%d/%Y %H:%M:%S") if ov is not None else ""
                    rows.append([d.strftime("%m/%d/%Y"), "Peak" if e["kind"] == "alert" else "M&V", dv, out_s, ts])
                elif p == "Ondera":
                    if offline:
                        continue
                    rows.append([d.strftime("%Y-%m-%d"), dv, "override" if ov is not None else "ok",
                                 int(ov - q["s"]) if ov is not None else ""])
                elif p == "Kitebrook":
                    if offline:
                        continue
                    oo = local_dt(d, ov, sec).astimezone(UTC).strftime("%Y-%m-%d %H:%M:%S") if ov is not None else ""
                    rows.append([d.strftime("%Y%m%d"), dv, oo])
                else:
                    if offline:
                        continue
                    rows.append([d.strftime("%Y-%m-%d"), dv, "true" if ov is not None else "false",
                                 local_dt(d, ov, sec).strftime("%Y-%m-%dT%H:%M:%S") if ov is not None else ""])
                    if rng.random() < 0.003:
                        rows.append(list(rows[-1]))                          # re-sent with the next day's batch
        name, header = {
            "Corvane": ("corvane_event_report_2024_2026.csv",
                        ["event_ref", "event_start_utc", "event_end_utc", "device_serial", "ack", "opt_out_utc"]),
            "Lumivale": ("lumivale_dr_events_cedar_brake.csv",
                         ["date", "program", "thermostat_id", "delivery", "override_time"]),
            "Ardena": ("ardena_event_outcomes.csv", ["EventDate", "EventType", "DeviceID", "Outcome", "OptOutTimestamp"]),
            "Ondera": ("ondera_events_cbec.csv", ["event_date", "device", "status", "override_minute"]),
            "Kitebrook": ("kitebrook_events_2024_2026.csv", ["EVENT_DATE", "DEVICE", "OVERRIDE_UTC"]),
            "Pinecrest Home": ("pinecrest_home_events.csv", ["date", "device_id", "opted_out", "opt_out_time"]),
        }[p]
        write_csv(os.path.join(target, name), header, rows)
        counts[p] = len(rows)
    return counts


def assignment_file(w, target):
    rows = []
    for e in w.events:
        if e["kind"] != "test":
            continue
        for r in w.dev:
            out = w.out.get((e["id"], r["i"]))
            if out is None:
                continue
            rows.append([e["code"], w.prog_id[r["i"]], "call" if out[0] else "hold"])
    write_csv(os.path.join(target, "mv_event_assignments_2024_2026.csv"), ["event_id", "program_id", "group"], rows)
    return len(rows)


def event_log(w, rng, target):
    wb = Workbook()
    ws = wb.active
    ws.title = "events"
    ws.append(["event_id", "date", "type", "notice_sent", "providers", "notes"])
    for e in w.events:
        note = ""
        if e["kind"] == "alert" and rng.random() < 0.12:
            note = "4CP probability high in the 14:00 forecast update"
        ws.append([e["code"], e["date"], "4CP alert" if e["kind"] == "alert" else "M&V test",
                   "13:%02d" % int(rng.integers(5, 55)), "all", note])
    for c in ws[1]:
        c.font = Font(bold=True)
    ws.column_dimensions["A"].width = 10
    ws.column_dimensions["B"].width = 12
    ws.column_dimensions["C"].width = 11
    ws.column_dimensions["F"].width = 52
    for row in ws.iter_rows(min_row=2, min_col=2, max_col=2):
        for c in row:
            c.number_format = "yyyy-mm-dd"
    ws2 = wb.create_sheet("provider settings")
    ws2.append(["provider", "summers", "event start", "event end", "pre-cool (minutes)", "setback (F)"])
    for p in W.PROVIDERS:
        q = W.PROG[p]
        ws2.append([p, "2024-2026", hhmm(q["s"]), hhmm(q["e"]), q["pre"], q["d"]])
    for c in ws2[1]:
        c.font = Font(bold=True)
    for col, wd in zip("ABCDEF", (16, 11, 11, 10, 16, 11)):
        ws2.column_dimensions[col].width = wd
    path = os.path.join(target, "peak_partners_event_log_2024_2026.xlsx")
    wb.save(path)
    postprocess.normalize_ooxml(path, "Mary Hampton", "Mary Hampton", "2024-05-21T14:12:00Z", "2026-10-02T15:31:00Z",
                                "Peak Partners event log", excel=True, company="Cedar Brake Electric Cooperative")


def ercot_file(w, rng, target):
    rows = []
    for y in range(2016, 2027):
        for k, m in enumerate((6, 7, 8, 9)):
            if y in W.YEARS:
                d = w.cp_days[W.YEARS.index(y) * 4 + k]
                start = w.cp_time[d]
            else:
                d = dt.date(y, m, int(rng.integers(8, 28)))
                while d.weekday() >= 5:
                    d += dt.timedelta(days=1)
                start = int(960 + 15 * int(rng.integers(0, 3)) + (15 if y >= 2021 and rng.random() < 0.5 else 0))
            load = 62000 + (y - 2016) * 2100 + {6: 0, 7: 2400, 8: 3300, 9: -1500}[m] + int(rng.normal(0, 900))
            rows.append([y, m, d.strftime("%m/%d/%Y"), hhmm(start + 15), load])
    write_csv(os.path.join(target, "ercot_4cp_intervals_2016_2026.csv"),
              ["Year", "Month", "Date", "Interval Ending (CPT)", "ERCOT Load (MW)"], rows)


def weather_file(w, target):
    rows = []
    for d in w.days:
        i = w.di[d]
        for hr in range(1, 25):
            rows.append(["KCDR", d.strftime("%Y-%m-%d"), hr, "%.1f" % W.temp_at(w, i, hr * 60 - 30)])
    write_csv(os.path.join(target, "weather_kcdr_hourly_2024_2026.csv"), ["station", "date", "hour_ending", "temp_f"], rows)


def cad_file(w, rng, target):
    P = w.parcel
    rows = []
    for k in range(len(P["south"])):
        yb = int(P["yb"][k])
        rows.append(["R%06d" % (100000 + k * 3), w.cad_addr[k], w.city[k][0].upper(), w.city[k][1], "A1",
                     int(P["sqft"][k]), yb, yb if rng.random() < 0.8 else yb + int(rng.integers(5, 25)),
                     int(P["stories"][k]), ["R3", "R4", "R5", "R6"][int(rng.integers(0, 4))],
                     "Y" if rng.random() < 0.11 else "", "%.2f" % (rng.lognormal(-1.2, 0.9) if P["south"][k] else rng.lognormal(-1.9, 0.4)),
                     int(round(P["sqft"][k] * (140 + 60 * rng.random()) + 30000, -2))])
    rows.sort(key=lambda r: r[0])
    write_csv(os.path.join(target, "calder_cad_residential_2026.csv"),
              ["prop_id", "situs_address", "situs_city", "situs_zip", "state_cd", "living_area_sf", "yr_blt",
               "eff_yr_blt", "stories", "class_cd", "pool", "land_acres", "market_value"], rows)
    return len(rows)


def quotes_file(w, target):
    wb = Workbook()
    ws = wb.active
    ws.title = "quotes"
    ws.append(["provider", "price per enrolled device, summer 2027 (USD)", "includes member incentive",
               "new enrolments planned Jan-May 2027: provider app", "retail instant rebate", "co-op mailer",
               "event start", "event end", "pre-cool (minutes)", "setback (F)", "note"])
    notes = {"Pinecrest Home": "Retail partnership with Hill Country Home & Hardware: instant rebate and enrolment at the till",
             "Ondera": "Event schedule unchanged from 2024-2026", "Kitebrook": "Dealer installs continue in the south service area"}
    for p in W.PROVIDERS:
        q = W.PROG[p]
        n = q["new27"]
        ws.append([p, q["price"], "yes", n.get("app", 0), n.get("retail", 0), n.get("mail", 0), hhmm(q["s"]), hhmm(q["e"]),
                   q["pre"], q["d"], notes.get(p, "")])
    for c in ws[1]:
        c.font = Font(bold=True)
    for col, wd in zip("ABCDEFGHIJK", (16, 20, 11, 18, 12, 11, 10, 10, 11, 10, 60)):
        ws.column_dimensions[col].width = wd
    for row in ws.iter_rows(min_row=2, min_col=2, max_col=2):
        for c in row:
            c.number_format = "0.00"
    path = os.path.join(target, "provider_quotes_summer_2027.xlsx")
    wb.save(path)
    postprocess.normalize_ooxml(path, "Renee Henry", "Renee Henry", "2026-10-12T16:20:00Z", "2026-10-28T21:05:00Z",
                                "Provider quotes, summer 2027", excel=True, company="Cedar Brake Electric Cooperative")


def solar_file(w, rng, target):
    rows = []
    for h in w.member:
        if rng.random() < 0.055:
            rows.append([w.acct[int(h)], "%.2f" % (rng.lognormal(np.log(7.5), 0.3)), "%04d-%02d-%02d" % (
                int(rng.integers(2016, 2027)), int(rng.integers(1, 13)), int(rng.integers(1, 28))),
                ["string", "microinverter"][int(rng.integers(0, 2))], "net metered"])
    write_csv(os.path.join(target, "der_interconnections_2026.csv"),
              ["account_number", "system_kw_dc", "interconnected_on", "inverter_type", "billing"], rows)


def write_all(w, target):
    rng = np.random.default_rng(W.SEED + 1)
    for k, e in enumerate(w.events):
        yr = e["date"].year % 100
        n = sum(1 for x in w.events[: k + 1] if x["year"] == e["year"])
        e["code"] = "E%02d-%02d" % (yr, n)
    addresses(w, rng)
    ids(w, rng)
    counts = {}
    counts["ami_rows"] = ami_file(w, rng, target)
    accounts_file(w, rng, target)
    counts["roster_rows"] = roster_file(w, rng, target)
    counts["reports"] = provider_reports(w, rng, target)
    counts["assignment_rows"] = assignment_file(w, target)
    event_log(w, rng, target)
    ercot_file(w, rng, target)
    weather_file(w, target)
    counts["cad_rows"] = cad_file(w, rng, target)
    quotes_file(w, target)
    solar_file(w, rng, target)
    return counts
