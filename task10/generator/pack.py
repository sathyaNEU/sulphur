"""task10 architecture 6: the pack under target/, written from the clean truth the way Wealdmoor's systems record it.

The SCADA historian's half-hourly export of the Halverton zone's nine primaries across the May 2024 asset ID
migration (UTC, quality flags, comms gaps, a month the export re-sent), the DSO's flexibility dispatch log (UK local
time, re-issued and cancelled instructions), the control room's 11 kV switching log, the reference weather station's
hourly observations, the primary register, the 11 kV feeder and open point schedule, the load growth register, two governing documents and three
files a planner would weigh and the assessment does not use."""
import csv
import datetime as dt
import io
import os

import numpy as np
import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill

import postprocess as PP
import world as W

ORG = "Wealdmoor Power Networks plc"
F_SCADA = "primary_demand_halfhourly_2023-2026.csv"
F_EVENTS = "flexibility_events_2023-2026.csv"
F_SWITCH = "control_room_switching_log_2023-2026.csv"
F_WX = "halverton_weather_hourly_2023-2026.csv"
F_REG = "primary_substation_register.xlsx"
F_FDR = "network_feeders_11kv.xlsx"
F_GROW = "load_growth_register_2026-27.xlsx"
F_GUIDE = "capacity_assessment_guideline_2026.pdf"
F_AWARD = "flexibility_contract_awards_2027-28.pdf"
F_CI = "customer_interruptions_2025-26.xlsx"
F_COND = "primary_transformer_condition_2026.xlsx"
F_DUOS = "duos_charging_statement_2027-28.pdf"
FILES = [F_SCADA, F_EVENTS, F_SWITCH, F_WX, F_REG, F_FDR, F_GROW, F_GUIDE, F_AWARD, F_CI, F_COND, F_DUOS]
DISTRACTORS = [F_CI, F_COND, F_DUOS]
EXPORT = dt.datetime(2026, 11, 3, 8, 14, tzinfo=dt.timezone.utc)
# the three exports carry no save stamp of their own: each file's time is when its system wrote it
EXPORTED = {F_SCADA: dt.datetime(2026, 11, 3, 8, 14, 37, tzinfo=dt.timezone.utc),
            F_EVENTS: dt.datetime(2026, 11, 2, 16, 47, 22, tzinfo=dt.timezone.utc),
            F_SWITCH: dt.datetime(2026, 11, 2, 17, 5, 51, tzinfo=dt.timezone.utc),
            F_WX: dt.datetime(2026, 11, 1, 6, 12, 5, tzinfo=dt.timezone.utc)}
MIGRATION = dt.datetime(2024, 5, 14, tzinfo=dt.timezone.utc)
UTC = dt.timezone.utc

ZONE_NAME = {"A": "Ashcombe Road CMZ", "C": "Charlecote Way CMZ", "F": "Fenwick Street CMZ", "H": "Hartwell Common CMZ"}
PROVIDER_SPELLINGS = {"Corvane": ["Corvane Flex Ltd", "Corvane Flex Ltd", "Corvane Flex Ltd", "CORVANE FLEX LTD", "Corvane Flex"],
                      "Quillon": ["Quillon Energy Services Ltd", "Quillon Energy Services Ltd", "Quillon Energy Services Ltd",
                                  "Quillon Energy Services", "QUILLON ENERGY SERVICES LTD"]}
NEW_POINT = {p["key"]: "%s.P_TOT.MW" % p["code"] for p in W.PRIMARIES}
PF = {"res": 0.972, "com": 0.951, "mix": 0.963}


SCADA_STREAM = 34   # the historian's outages and gaps


def write_csv(path, header, rows):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n")
    w.writerow(header)
    w.writerows(rows)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(buf.getvalue())


def uk_label(t):
    """A half-hour's end on the UK clock, as the historian's export writes it (the spring-forward hour never appears)."""
    from zoneinfo import ZoneInfo
    return t.astimezone(ZoneInfo("Europe/London")).strftime("%Y-%m-%d %H:%M")


def iso_z(t):
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


# ------------------------------------------------------------------------------------------------ SCADA export
def scada_rows(T, stream=SCADA_STREAM):
    """The historian's export, November to March of each winter: each month's extract appended in turn (time, then point within the month), legacy
    point names until the asset ID migration on 14 May 2024, quality G, S (held by the historian through a comms
    outage at the last good value) and B (a CT circuit fault at Ravenhurst Park, zeros), short gaps where the outstation
    did not report, and the December 2024 extract re-sent with its first day overlapping November's."""
    rng = np.random.default_rng([W.SEED, stream])
    recs = []
    for w, d0, d1 in W.WINTERS:
        stamps = T["stamps"][w]
        for p in W.PRIMARIES:
            vals = T["metered"][(p["key"], w)]
            pf = PF[p["kind"]]
            q = rng.normal(0, 0.012, len(vals))
            mvar = vals * np.tan(np.arccos(np.clip(pf + q, 0.9, 0.995)))
            qual = np.array(["G"] * len(vals), dtype=object)
            mw = vals.copy()
            # the evenings the DSO had flexibility scheduled at this primary: the outstation was polled on a second
            # route for the service window, so the historian lost none of those half-hours
            watched = np.zeros(len(vals), bool)
            for e in T["events"]:
                if e["zone"] == p["key"] and e["winter"] == w:
                    ix = W.window_indices(stamps, e["day"])
                    watched[max(ix[0] - 3, 0):ix[-1] + 7] = True
            # comms outages: the historian holds the last good value, flagged S, for 2 to 9 half-hours
            for _ in range(int(rng.integers(5, 10))):
                while True:
                    i0 = int(rng.integers(1, len(vals) - 12))
                    n = int(rng.integers(2, 10))
                    if not watched[i0:i0 + n].any():
                        break
                mw[i0:i0 + n] = mw[i0 - 1]
                mvar[i0:i0 + n] = mvar[i0 - 1]
                qual[i0:i0 + n] = "S"
            # gaps the outstation never filled (rows absent from the export)
            drop = np.zeros(len(vals), bool)
            for _ in range(int(rng.integers(3, 8))):
                while True:
                    i0 = int(rng.integers(0, len(vals) - 6))
                    n = int(rng.integers(1, 6))
                    if not watched[i0:i0 + n].any():
                        break
                drop[i0:i0 + n] = True
            if p["key"] == "E" and w == "2024/25":
                i0 = 48 * 70 + 19
                mw[i0:i0 + 31] = 0.0
                mvar[i0:i0 + 31] = 0.0
                qual[i0:i0 + 31] = "B"
            for i, t in enumerate(stamps):
                if drop[i]:
                    continue
                if t <= dt.datetime(d0.year, 11, 1, tzinfo=UTC):   # the winter export starts on 1 November
                    continue
                name = p["legacy"] if t < MIGRATION else NEW_POINT[p["key"]]
                recs.append((t, p["key"], name, mw[i], mvar[i], qual[i]))
    # one row per point and half-hour, written in month extracts: time within the month, points in register order
    recs.sort(key=lambda r: (r[0].year, r[0].month, r[0], ORDER[r[1]]))
    out = []
    for t, k, name, mw, mvar, q in recs:
        out.append([name, uk_label(t), "%.3f" % mw, "%.3f" % mvar, q])
    # the December 2024 extract re-sent: it starts with 30 November's half-hours, already exported in November
    dec = [i for i, r in enumerate(out) if r[1].startswith("2024-12-01 00:30")]
    nov30 = [r for r in out if r[1].startswith("2024-11-30") or r[1] == "2024-12-01 00:00"]
    i0 = dec[0]
    out = out[:i0] + nov30 + out[i0:]
    return out


ORDER = {p["key"]: i for i, p in enumerate(W.PRIMARIES)}


def write_scada(T, target):
    rows = scada_rows(T)
    write_csv(os.path.join(target, F_SCADA), ["point", "interval_end_uk_local", "value_mw", "value_mvar", "quality"], rows)
    return len(rows)


# --------------------------------------------------------------------------------------------- dispatch log
def event_rows(T):
    """The DSO's flexibility dispatch log: an instruction issued day-ahead (UK local time), a revision on the
    morning where the provider declared reduced availability or the DSO cancelled, one row per instruction and
    revision, superseded rows kept."""
    rng = np.random.default_rng([W.SEED, 47])
    evs = sorted(T["events"], key=lambda e: (e["day"], ORDER[e["zone"]]))
    out = []
    seq = {"2023/24": 873, "2024/25": 1146, "2025/26": 1389}
    for e in evs:
        w = e["winter"]
        seq[w] += int(rng.integers(1, 4))
        ref = "WPN-FLX-%s-%04d" % (w[2:4] + w[5:7], seq[w])
        issued = dt.datetime.combine(e["day"] - dt.timedelta(days=1 if e["day"].weekday() > 0 else 3),
                                     dt.time(int(rng.integers(12, 15)), int(rng.integers(0, 60))))
        prov = PROVIDER_SPELLINGS[e["provider"]][int(rng.integers(0, 5))]
        zone = ZONE_NAME[e["zone"]]
        code = W.BY[e["zone"]]["code"]
        sd = e["day"].strftime("%d/%m/%Y")
        if e["status"] == "Cancelled" or e["revised_mw"]:
            out.append([ref, "1", issued.strftime("%d/%m/%Y %H:%M"), zone, code, prov, sd, "16:00", "19:30",
                        "%.1f" % e["mw"], "Superseded"])
            rev = dt.datetime.combine(e["day"], dt.time(int(rng.integers(7, 11)), int(rng.integers(0, 60))))
            if e["status"] == "Cancelled":
                out.append([ref, "2", rev.strftime("%d/%m/%Y %H:%M"), zone, code, prov, sd, "16:00", "19:30",
                            "0.0", "Cancelled"])
            else:
                out.append([ref, "2", rev.strftime("%d/%m/%Y %H:%M"), zone, code, prov, sd, "16:00", "19:30",
                            "%.1f" % e["revised_mw"], "Completed"])
        else:
            out.append([ref, "1", issued.strftime("%d/%m/%Y %H:%M"), zone, code, prov, sd, "16:00", "19:30",
                        "%.1f" % e["mw"], "Completed"])
    return out


def write_events(T, target):
    rows = event_rows(T)
    write_csv(os.path.join(target, F_EVENTS),
              ["instruction_ref", "revision", "issued_uk_local", "zone", "primary_asset", "provider", "service_date",
               "window_start_uk_local", "window_end_uk_local", "scheduled_mw", "status"], rows)
    return len(rows)


# ------------------------------------------------------------------------------------------------ weather
def weather_rows(T):
    """Hourly observations at Halverton weather station in the station network's export layout (end of the
    observation hour, UTC), with the hours the logger lost left out."""
    rng = np.random.default_rng([W.SEED, 59])
    qrng = np.random.default_rng([W.SEED, 61])
    out = []
    for w, d0, d1 in W.WINTERS:
        days, _ = T["temps"][w]
        for d, hv in zip(days, T["hourly"][w]):
            for hr in range(24):
                if rng.random() < 0.004:
                    continue
                t = dt.datetime.combine(d, dt.time(hr, 0), UTC)
                ws = max(0, int(round(rng.gamma(2.2, 4.1))))
                rh = int(min(100, max(48, round(87 - 1.6 * (hv[hr] - 4) + rng.normal(0, 5)))))
                if qrng.random() < 0.021:
                    # the raw reading, superseded by the quality-controlled one after the station's checks
                    raw = hv[hr] + float(qrng.choice([-1, 1])) * float(qrng.uniform(0.3, 2.4))
                    out.append(["03861", t.strftime("%Y-%m-%d %H:%M"), "%.1f" % raw, str(ws), str(rh), "0"])
                out.append(["03861", t.strftime("%Y-%m-%d %H:%M"), "%.1f" % hv[hr], str(ws), str(rh), "1"])
    return out


def write_weather(T, target):
    rows = weather_rows(T)
    write_csv(os.path.join(target, F_WX), ["src_id", "ob_end_time", "air_temperature", "wind_speed", "rltv_hum",
                                            "version_num"], rows)
    return len(rows)


# --------------------------------------------------------------------------------------------- workbooks
HEAD_FONT = Font(name="Calibri", bold=True, size=11)
HEAD_FILL = PatternFill("solid", fgColor="DDEBF7")


def sheet(ws, header, rows, widths):
    ws.append(header)
    for c in ws[1]:
        c.font = HEAD_FONT
        c.fill = HEAD_FILL
        c.alignment = Alignment(vertical="center", wrap_text=True)
    for r in rows:
        ws.append(r)
    for i, wdt in enumerate(widths):
        ws.column_dimensions[openpyxl.utils.get_column_letter(i + 1)].width = wdt
    ws.freeze_panes = "A2"


def save_book(wb, path, creator, last_by, created, modified):
    wb.save(path)
    z = lambda t: t.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    PP.normalize_ooxml(path, creator, last_by, z(created), z(modified), excel=True, company=ORG)


def aware(s):
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))


# transformer nameplates: (ONAN, ONAF) MVA per unit; the guideline's firm capacity is the smaller unit's winter cyclic
# rating, cyclic factor 1.21 on its ONAF rating, at a power factor of 0.95
NAMEPLATE = {"A": ((12, 20), (12, 20)), "B": ((15, 23), (15, 23)), "C": ((12, 20), (12, 20)), "D": ((12, 20), (15, 23)),
             "E": ((10, 15), (10, 15)), "F": ((15, 27), (15, 27)), "G": ((15, 24), (15, 24)), "H": ((10, 15), (12, 16)),
             "I": ((10, 17), (10, 17))}
CYCLIC = {"A": 1.2105, "B": 1.19, "C": 1.1842, "D": 1.1053, "E": 1.2281, "F": 1.1891, "G": 1.1842, "H": 1.2491, "I": 1.2074}
COMMISSIONED = {"A": 1979, "B": 1988, "C": 1974, "D": 1983, "E": 1996, "F": 1981, "G": 1991, "H": 1977, "I": 2002}
GSP = "Halverton 132/33 kV"


def firm_from_nameplate(k):
    onaf = min(u[1] for u in NAMEPLATE[k])
    return round(onaf * CYCLIC[k] * 0.95, 1)


def dfes_rates(k):
    r = W.BY[k]["dfes"]
    adj = {"A": (-0.1, 0.1), "B": (0.0, 0.0), "C": (0.1, -0.1), "D": (0.0, 0.0), "E": (-0.2, 0.2), "F": (0.1, -0.1),
           "G": (0.0, 0.0), "H": (-0.1, 0.1), "I": (0.1, -0.1)}[k]
    return round(r + adj[0], 1), round(r + adj[1], 1)


def write_register(target):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Primaries"
    rows = []
    for p in sorted(W.PRIMARIES, key=lambda q: q["code"]):
        k = p["key"]
        (a1, f1), (a2, f2) = NAMEPLATE[k]
        rows.append([p["code"], p["name"], GSP, "33/11 kV", p["legacy"], NEW_POINT[k], 2,
                     "%d/%d" % (a1, f1), "%d/%d" % (a2, f2), COMMISSIONED[k]])
    sheet(ws, ["Asset code", "Primary substation", "Grid supply point", "Voltage", "SCADA point (to 13/05/2024)",
               "SCADA point (from 14/05/2024)", "Transformers", "T1 rating ONAN/ONAF (MVA)", "T2 rating ONAN/ONAF (MVA)",
               "Year commissioned"], rows,
          [12, 22, 20, 10, 32, 24, 13, 18, 18, 12])
    ws2 = wb.create_sheet("DFES 2026")
    rows2 = []
    for p in sorted(W.PRIMARIES, key=lambda q: q["name"]):
        r1, r2 = dfes_rates(p["key"])
        rows2.append([p["code"], p["name"], r1, r2])
    sheet(ws2, ["Asset code", "Primary substation", "Underlying peak growth 2026/27 (%)",
                "Underlying peak growth 2027/28 (%)"], rows2, [12, 22, 22, 22])
    ws2.append([])
    ws2.append(["Distribution Future Energy Scenarios 2026, best view, published 30 June 2026."])
    save_book(wb, os.path.join(target, F_REG), "Network Planning", "Clifford Evans",
              aware("2025-11-18T09:41:12Z"), aware("2026-09-08T15:22:47Z"))


# 11 kV feeders and open points
FEEDERS_PER = {"A": 8, "B": 7, "C": 8, "D": 6, "E": 6, "F": 9, "G": 7, "H": 6, "I": 6}
NOPS = W.NOPS


def feeder_table():
    rng = np.random.default_rng([W.SEED, 71])
    feeders = []
    used = set()
    abbrev = {"A": "ASHC", "B": "TOLL", "C": "CHAR", "D": "DUNM", "E": "RAVN", "F": "FENW", "G": "WEXL", "H": "HART", "I": "KEST"}
    streets = ["Mill Lane", "Station Road", "Church Street", "Park Avenue", "Queens Road", "Victoria Street", "Oak Drive",
               "Kingsway", "Bridge Street", "Meadow Way", "Holly Close", "Grange Road", "Albert Street", "Canal Side",
               "Hill Top", "The Crescent", "Moor Lane", "Orchard Road", "Spring Bank", "Elm Grove", "Market Street",
               "Brook Lane", "Westfield", "Ladysmith Road", "Nelson Street", "Priory Road", "Croft Lane", "Willow Bank",
               "Tannery Row", "Gas Street", "Foundry Lane", "Chapel Fold", "Rope Walk", "Quarry Hill", "Saxon Way",
               "Cobden Street", "Wharf Road", "Beacon View", "Linnet Close", "Sandpit Lane", "Fairfield Road", "Low Green",
               "Turnpike", "Coppice Drive", "Fern Bank", "Mount Pleasant", "Dyers Lane", "Forge Close", "Glebe Road",
               "Ivy Terrace", "Kiln Lane", "Larch Rise", "Malt House", "North Parade", "Pinfold", "Reservoir Road",
               "Stoneyfield", "Tithe Barn", "Union Street", "Vicarage Lane", "Watermead", "Yew Tree Walk", "Bank Top",
               "Cross Lane", "Dene Road", "Every Street", "Furnace Road", "Gorse Hill", "Hawthorn Way", "Island Road"]
    # each feeder takes its own street: the order is drawn once for the zone, on a stream of its own
    order = list(np.random.default_rng([W.SEED, 72]).permutation(len(streets)))
    for p in W.PRIMARIES:
        k = p["key"]
        for n in range(FEEDERS_PER[k]):
            while True:
                fid = "C%06d" % int(rng.integers(102000, 989999))
                if fid not in used:
                    used.add(fid)
                    break
            dom = int(rng.integers(650, 2400)) if p["kind"] == "res" else int(rng.integers(150, 1100))
            nondom = int(rng.integers(8, 70)) if p["kind"] == "res" else int(rng.integers(40, 260))
            rng.integers(0, len(streets))   # the old per-feeder draw, kept so the other draws do not move
            name = "%s %s" % (p["name"].upper(), streets[int(order.pop(0))].upper())
            feeders.append(dict(fid=fid, legacy="%s/F%02d" % (abbrev[k], n + 1), key=k, name=name, dom=dom,
                                nondom=nondom, rating=int(rng.choice([300, 350, 400, 400, 450]))))
    return feeders


def write_feeders(target):
    feeders = feeder_table()
    byk = {}
    for f in feeders:
        byk.setdefault(f["key"], []).append(f)
    rng = np.random.default_rng([W.SEED, 73])
    nop_rows = []
    for nop, a, b in NOPS:
        fa = byk[a][int(rng.integers(0, len(byk[a])))]
        fb = byk[b][int(rng.integers(0, len(byk[b])))]
        nop_rows.append([nop, fa["fid"], W.BY[a]["code"], fb["fid"], W.BY[b]["code"],
                         int(rng.choice([200, 250, 250, 300])), "Normally open"])
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Feeders"
    rows = []
    for f in sorted(feeders, key=lambda x: (x["key"], x["legacy"])):
        rows.append([f["fid"], f["legacy"], W.BY[f["key"]]["code"], f["name"], f["dom"], f["nondom"], f["rating"]])
    sheet(ws, ["Feeder ID", "Circuit (legacy)", "Primary asset code", "Feeder name", "Domestic customers",
               "Non-domestic customers", "Cable rating (A)"], rows, [11, 15, 16, 42, 16, 18, 14])
    ws2 = wb.create_sheet("Open points")
    sheet(ws2, ["Open point", "Feeder ID (side 1)", "Primary (side 1)", "Feeder ID (side 2)", "Primary (side 2)",
                "Switch rating (A)", "Normal state"], sorted(nop_rows), [11, 16, 14, 16, 14, 14, 14])
    save_book(wb, os.path.join(target, F_FDR), "Network Records", "Network Records",
              aware("2024-06-03T10:02:44Z"), aware("2026-08-19T13:37:05Z"))
    return feeders, nop_rows


# ------------------------------------------------------------------------------------- control room switching log
ENGINEERS = ["JT", "MB", "SK", "AD", "RP", "LW", "CH"]


def switching_rows(T, nop_rows):
    """The control room's 11 kV switching log for the Halverton zone: one row per operation, the transfer of a feeder
    section across a normally-open point logged when it is made and again when the network is put back to normal,
    with the load the control engineer read off the feeder ammeters at the time."""
    rng = np.random.default_rng([W.SEED, 83])
    clock = np.random.default_rng([W.SEED, 84])    # the minute the engineer logged each operation, a few either side
    side = {r[0]: {r[2]: r[1], r[4]: r[3]} for r in nop_rows}     # open point -> primary code -> feeder ID
    out = []
    n = 4100
    for s in T["switching"]:
        if s["mw_at_start"] <= 0:
            continue
        t0 = s["start"] + dt.timedelta(minutes=int(clock.integers(-8, 9)))
        t1 = s["end"] + dt.timedelta(minutes=int(clock.integers(-8, 9)))
        frm, to = W.BY[s["frm"]], W.BY[s["to"]]
        f_from, f_to = side[s["nop"]][frm["code"]], side[s["nop"]][to["code"]]
        eng = ENGINEERS[int(rng.integers(0, len(ENGINEERS)))]
        n += int(rng.integers(3, 40))
        amps = int(round(s["mw_at_start"] * 1000 / (1.732 * 11 * 0.97)))
        out.append(["SW-%05d" % n, uk_label(t0), eng, s["nop"], "Closed",
                    f_from, frm["code"], f_to, to["code"], "%.2f" % s["mw_at_start"], str(amps), s["reason"]])
        eng2 = ENGINEERS[int(rng.integers(0, len(ENGINEERS)))]
        n += int(rng.integers(1, 30))
        out.append(["SW-%05d" % n, uk_label(t1), eng2, s["nop"], "Opened (normal)",
                    f_from, frm["code"], f_to, to["code"], "", "", "Network restored to normal"])
    return out


def write_switching(T, target, nop_rows):
    rows = switching_rows(T, nop_rows)
    write_csv(os.path.join(target, F_SWITCH),
              ["log_ref", "operation_time_uk_local", "control_engineer", "open_point", "operation", "section_from_feeder",
               "section_from_primary", "section_to_feeder", "section_to_primary", "load_transferred_mw", "feeder_amps",
               "reason"], rows)
    return len(rows)


# load growth register
APPLICANT_TYPES = ["Housing development (heat pumps)", "EV charging hub", "Commercial unit", "School extension",
                   "Heat pump retrofit scheme", "Data hall", "Supermarket", "Care home", "Industrial unit",
                   "Leisure centre electrification", "Bus depot charging"]


def write_growth(target, feeders):
    """The connections team's register: offers, acceptances and energisations by 11 kV feeder; rows for connections
    the assessment does not count (withdrawn, quoted only, energised before April 2026, due after October 2027) and a
    few re-entered references, older rows on the circuit's legacy name."""
    rng = np.random.default_rng([W.SEED, 79])
    byk = {}
    for f in feeders:
        byk.setdefault(f["key"], []).append(f)
    rows = []
    refs = set()

    def ref(acc):
        """the application's reference, numbered in the year it went in (about four months before acceptance)"""
        while True:
            rng.choice([2024, 2025, 2025, 2026])   # the old year draw, kept so the other draws do not move
            r = "LCG-%d-%05d" % ((acc - dt.timedelta(days=120)).year, int(rng.integers(10000, 99999)))
            if r not in refs:
                refs.add(r)
                return r

    sites = ["Land at %s Farm", "%s Business Park", "%s Retail Park", "Former %s Works", "%s Quarter", "%s Fields",
             "%s Wharf", "%s Gardens", "Plot 4, %s Way"]
    names = ["Hollins", "Marsh", "Ferrers", "Coldwell", "Ashby", "Thorne", "Kelham", "Radford", "Sowerby", "Linden",
             "Bramley", "Calder", "Netherton", "Oakham", "Pelham", "Whitlow", "Elsdon", "Garside"]
    for p in W.PRIMARIES:
        k = p["key"]
        target_kw = int(round(W.REGISTER_MW[k] * 1000))
        n = int(rng.integers(2, 5))
        cuts = np.sort(rng.choice(np.arange(60, target_kw - 60), n - 1, replace=False)) if target_kw > 300 else []
        parts = np.diff(np.concatenate([[0], cuts, [target_kw]])).astype(int)
        for part in parts:
            f = byk[k][int(rng.integers(0, len(byk[k])))]
            acc = dt.date(2025, 1, 1) + dt.timedelta(days=int(rng.integers(0, 560)))
            plan = max(acc + dt.timedelta(days=150), dt.date(2026, 4, 1)) + dt.timedelta(days=int(rng.integers(0, 420)))
            plan = min(plan, dt.date(2027, 10, 15))
            energised = plan if plan < dt.date(2026, 10, 28) else None
            status = "Energised" if energised else "Accepted"
            r = ref(acc)
            rows.append([r, APPLICANT_TYPES[int(rng.integers(0, len(APPLICANT_TYPES)))],
                         sites[int(rng.integers(0, len(sites)))] % names[int(rng.integers(0, len(names)))],
                         f["fid"], int(part), status, acc.strftime("%d/%m/%Y"), plan.strftime("%d/%m/%Y"),
                         energised.strftime("%d/%m/%Y") if energised else ""])
            if rng.random() < 0.18:   # re-entered when the planned date moved: same reference, later date, same kW
                plan2 = plan + dt.timedelta(days=int(rng.integers(20, 60)))
                if plan2 < dt.date(2027, 11, 1) and not energised:
                    rows[-1][5] = "Superseded"
                    rows.append([r, rows[-1][1], rows[-1][2], f["fid"], int(part), "Accepted", rows[-1][6],
                                 plan2.strftime("%d/%m/%Y"), ""])
        # connections the assessment does not count
        for _ in range(int(rng.integers(2, 5))):
            f = byk[k][int(rng.integers(0, len(byk[k])))]
            kind = rng.choice(["Withdrawn", "Quoted", "Early", "Late"])
            kw = int(rng.integers(120, 1800))
            acc = dt.date(2024, 3, 1) + dt.timedelta(days=int(rng.integers(0, 700)))
            fid = f["legacy"] if acc < dt.date(2024, 5, 14) else f["fid"]
            if kind == "Withdrawn":
                rows.append([ref(acc), APPLICANT_TYPES[int(rng.integers(0, len(APPLICANT_TYPES)))],
                             sites[int(rng.integers(0, len(sites)))] % names[int(rng.integers(0, len(names)))],
                             fid, kw, "Withdrawn", acc.strftime("%d/%m/%Y"), "", ""])
            elif kind == "Quoted":
                rows.append([ref(acc), APPLICANT_TYPES[int(rng.integers(0, len(APPLICANT_TYPES)))],
                             sites[int(rng.integers(0, len(sites)))] % names[int(rng.integers(0, len(names)))],
                             fid, kw, "Quoted", "", "", ""])
            elif kind == "Early":
                en = dt.date(2024, 6, 1) + dt.timedelta(days=int(rng.integers(0, 640)))
                en = min(en, dt.date(2026, 3, 20))
                rows.append([ref(en - dt.timedelta(days=200)), APPLICANT_TYPES[int(rng.integers(0, len(APPLICANT_TYPES)))],
                             sites[int(rng.integers(0, len(sites)))] % names[int(rng.integers(0, len(names)))],
                             fid, kw, "Energised", (en - dt.timedelta(days=200)).strftime("%d/%m/%Y"),
                             en.strftime("%d/%m/%Y"), en.strftime("%d/%m/%Y")])
            else:
                pl = dt.date(2027, 11, 20) + dt.timedelta(days=int(rng.integers(0, 400)))
                # accepted before the register's last save (30 October 2026), never after it
                acc_l = min(pl - dt.timedelta(days=500), dt.date(2026, 10, 23) - dt.timedelta(days=pl.toordinal() % 61))
                rows.append([ref(acc_l), APPLICANT_TYPES[int(rng.integers(0, len(APPLICANT_TYPES)))],
                             sites[int(rng.integers(0, len(sites)))] % names[int(rng.integers(0, len(names)))],
                             f["fid"], kw, "Accepted", acc_l.strftime("%d/%m/%Y"),
                             pl.strftime("%d/%m/%Y"), ""])
    # a plot is numbered on its own site plan; the number is read from the application's reference, not drawn
    for r in rows:
        if r[2].startswith("Plot 4, "):
            r[2] = "Plot %d, %s" % (1 + int(r[0][-5:]) % 23, r[2][len("Plot 4, "):])
    rng.shuffle(rows)
    rows.sort(key=lambda r: r[0])
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Register"
    sheet(ws, ["Reference", "Applicant type", "Site", "11 kV feeder", "Design demand (kW)", "Status",
               "Offer accepted", "Planned energisation", "Energised on"], rows, [16, 30, 30, 13, 16, 12, 14, 18, 14])
    save_book(wb, os.path.join(target, F_GROW), "Connections", "Connections",
              aware("2024-07-09T08:30:11Z"), aware("2026-10-30T16:05:38Z"))
    return rows


def write_interruptions(target, feeders):
    rng = np.random.default_rng([W.SEED, 83])
    rows = []
    for f in sorted(feeders, key=lambda x: x["fid"]):
        cust = f["dom"] + f["nondom"]
        n = int(rng.poisson(1.4))
        ci = int(sum(rng.integers(int(cust * 0.2), cust + 1) for _ in range(n)))
        cml = int(ci * rng.gamma(2.0, 38.0)) if ci else 0
        rows.append([f["fid"], W.BY[f["key"]]["code"], f["name"], cust, n, ci, cml,
                     round(ci / cust * 100, 1) if cust else 0.0, round(cml / cust, 1) if cust else 0.0])
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "CI and CML 2025-26"
    sheet(ws, ["Feeder ID", "Primary asset code", "Feeder name", "Customers", "Interruptions (3 min and over)",
               "Customers interrupted", "Customer minutes lost", "CI per 100 customers", "CML per customer"], rows,
          [11, 16, 42, 11, 18, 16, 18, 16, 14])
    ws.append([])
    ws.append(["Regulatory year 1 April 2025 to 31 March 2026; excludes exceptional events."])
    save_book(wb, os.path.join(target, F_CI), "Performance Reporting", "Performance Reporting",
              aware("2026-05-12T11:20:09Z"), aware("2026-06-02T09:48:31Z"))


def write_condition(target):
    rng = np.random.default_rng([W.SEED, 89])
    rows = []
    for p in sorted(W.PRIMARIES, key=lambda q: q["code"]):
        for tx in ("T1", "T2"):
            made = COMMISSIONED[p["key"]] - int(rng.integers(0, 2))   # built in the year of commissioning or the one before
            age = 2026 - made
            h2 = int(rng.gamma(4.0, 6 + age / 2))
            ch4 = int(rng.gamma(4.0, 3 + age / 5))
            c2h2 = round(float(rng.exponential(0.6)), 1)
            c2h4 = int(rng.gamma(3.0, 2 + age / 8))
            co = int(rng.gamma(6.0, 30 + 4 * age))
            moist = round(float(rng.normal(8 + age / 5, 1.6)), 1)
            hi = int(min(5, max(1, round(1 + (age - 20) / 8.5 + rng.normal(0, 0.4)))))
            rows.append([p["code"], p["name"], tx, made,
                         (dt.date(2026, 2, 1) + dt.timedelta(days=int(rng.integers(0, 150)))).strftime("%d/%m/%Y"),
                         h2, ch4, c2h2, c2h4, co, moist, "HI%d" % hi])
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Oil and condition"
    sheet(ws, ["Asset code", "Primary substation", "Unit", "Manufactured", "Oil sample date", "H2 (ppm)", "CH4 (ppm)",
               "C2H2 (ppm)", "C2H4 (ppm)", "CO (ppm)", "Moisture (ppm)", "Health index"], rows,
          [12, 22, 7, 13, 15, 10, 10, 11, 11, 10, 14, 13])
    save_book(wb, os.path.join(target, F_COND), "Asset Management", "Asset Management",
              aware("2026-03-02T14:12:40Z"), aware("2026-07-21T10:33:18Z"))


def write_data(T, target):
    os.makedirs(target, exist_ok=True)
    n_scada = write_scada(T, target)
    n_ev = write_events(T, target)
    n_wx = write_weather(T, target)
    write_register(target)
    feeders, nops = write_feeders(target)
    n_sw = write_switching(T, target, nops)
    grow = write_growth(target, feeders)
    write_interruptions(target, feeders)
    write_condition(target)
    return dict(scada_rows=n_scada, event_rows=n_ev, weather_rows=n_wx, switching_rows=n_sw, feeders=feeders, nops=nops,
                growth=grow)
