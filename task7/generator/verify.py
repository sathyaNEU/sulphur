"""task7 architecture 10: the pack read back as an analyst assembles it, from the shipped files only (no world object):
the roster deduplicated and re-keyed through replaced thermostats, the six providers' reports on one footing and one
clock, the research sample's meters mapped through exchanges to accounts and devices, the appraisal roll matched to the
co-op's addresses, the events and their runs, the 4CP intervals and the weather."""
import csv
import datetime as dt
import os
import re

import numpy as np
from openpyxl import load_workbook

STEP = 15
AMI_FROM = 13 * 60
UTC_OFFSET = 5                    # Central daylight time is UTC-5 all summer


class Pack:
    pass


def rows(path):
    with open(path, newline="", encoding="utf-8") as fh:
        rd = csv.reader(fh)
        head = next(rd)
        for r in rd:
            yield dict(zip(head, r))


def date(s):
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%Y%m%d"):
        try:
            return dt.datetime.strptime(s, fmt).date()
        except ValueError:
            pass
    raise ValueError(s)


def norm_addr(a):
    a = a.upper().strip()
    a = re.sub(r"\bFARM TO MARKET\b", "FM", a)
    a = re.sub(r"\bFM RD\b", "FM", a)
    a = re.sub(r"\bCR\b", "COUNTY ROAD", a)
    for ab, full in (("ST", "STREET"), ("DR", "DRIVE"), ("LN", "LANE"), ("TRL", "TRAIL"), ("CT", "COURT"), ("RD", "ROAD"),
                     ("CV", "COVE")):
        a = re.sub(r"\b%s$" % ab, full, a)
    return re.sub(r"\s+", " ", a)


def load(target):
    P = Pack()
    # events and their places in runs of consecutive event days
    wb = load_workbook(os.path.join(target, "peak_partners_event_log_2024_2026.xlsx"), read_only=True)
    ev = []
    for r in list(wb["events"].iter_rows(values_only=True))[1:]:
        d = r[1].date() if isinstance(r[1], dt.datetime) else r[1]
        ev.append(dict(code=r[0], date=d, kind="alert" if r[2] == "4CP alert" else "test"))
    ev.sort(key=lambda e: e["date"])
    alert_days = {e["date"] for e in ev if e["kind"] == "alert"}
    for e in ev:
        run, k = 0, 1
        while e["kind"] == "alert" and (e["date"] - dt.timedelta(days=k)) in alert_days:
            run += 1
            k += 1
        e["run"] = min(run, 5)
    P.events = ev
    P.ev_by_date = {e["date"]: e for e in ev}
    P.settings = {}
    for r in list(wb["provider settings"].iter_rows(values_only=True))[1:]:
        hs, ms = map(int, r[2].split(":"))
        he, me = map(int, r[3].split(":"))
        P.settings[r[0]] = dict(s=hs * 60 + ms, e=he * 60 + me, pre=int(r[4]), d=int(r[5]))
    P.providers = list(P.settings)
    # the providers' quotes for 2027
    wb = load_workbook(os.path.join(target, "provider_quotes_summer_2027.xlsx"), read_only=True)
    P.quote = {}
    for r in list(wb["quotes"].iter_rows(values_only=True))[1:]:
        hs, ms = map(int, str(r[6]).split(":"))
        he, me = map(int, str(r[7]).split(":"))
        P.quote[r[0]] = dict(price=float(r[1]), new={"app": int(r[3] or 0), "retail": int(r[4] or 0), "mail": int(r[5] or 0)},
                             set=dict(s=hs * 60 + ms, e=he * 60 + me, pre=int(r[8]), d=int(r[9])))
    # the 4CP intervals of 2024 to 2026 (interval ending, local) and whether the co-op called its alert that day
    P.cps = []
    for r in rows(os.path.join(target, "ercot_4cp_intervals_2016_2026.csv")):
        y = int(r["Year"])
        if y < 2024:
            continue
        d = date(r["Date"])
        h, m = map(int, r["Interval Ending (CPT)"].split(":"))
        P.cps.append(dict(date=d, start=h * 60 + m - STEP, called=d in alert_days))
    # hourly weather, interpolated to any minute
    temp = {}
    for r in rows(os.path.join(target, "weather_kcdr_hourly_2024_2026.csv")):
        temp.setdefault(date(r["date"]), {})[int(r["hour_ending"])] = float(r["temp_f"])
    P.temp = temp
    # the transmission rate
    P.rate = 54.80
    # members: accounts, addresses, meters and their exchanges
    P.acct_addr, P.meter_acct = {}, {}
    for r in rows(os.path.join(target, "member_accounts_2026.csv")):
        a = int(r["account_number"])
        P.acct_addr[a] = (norm_addr(r["service_address"]), r["city"].upper())
        P.meter_acct[int(r["meter_number"])] = (a, None)
        if r["prior_meter_number"]:
            P.meter_acct[int(r["prior_meter_number"])] = (a, date(r["meter_set_date"]))
    # the appraisal roll: living area and year built by address
    cad = {}
    for r in rows(os.path.join(target, "calder_cad_residential_2026.csv")):
        cad[(norm_addr(r["situs_address"]), r["situs_city"].upper())] = (int(r["living_area_sf"]), int(r["yr_blt"]))
    P.home = {}
    for a, key in P.acct_addr.items():
        if key in cad:
            P.home[a] = cad[key]
    # the roster: one row per programme id; the provider's ids, current and before a swap
    dev = {}
    for r in rows(os.path.join(target, "peak_partners_roster_2026-10-30.csv")):
        pid = r["program_id"]
        if pid in dev:
            continue
        dev[pid] = dict(pid=pid, acct=int(r["account_number"]), p=r["provider"], did=r["device_id"],
                        joined=date(r["enrolled_on"]), left=date(r["unenrolled_on"]) if r["unenrolled_on"] else None,
                        ch={"Provider app": "app", "Co-op mailer": "mail", "Retail instant rebate": "retail"}[r["channel"]],
                        prev=r["previous_device_id"] or None,
                        changed=date(r["device_changed_on"]) if r["device_changed_on"] else None)
    P.dev = dev
    by_did = {}
    for v in dev.values():
        by_did[v["did"]] = v["pid"]
        if v["prev"]:
            by_did[v["prev"]] = v["pid"]
    P.by_did = by_did
    # the test events' halves
    P.assign = {}
    for r in rows(os.path.join(target, "mv_event_assignments_2024_2026.csv")):
        P.assign[(r["event_id"], r["program_id"])] = r["group"] == "call"
    # the providers' reports: (date, programme id) -> (received, override minute local or None); None received when the
    # provider leaves an unreached device out of its report
    P.rep = {}
    P.lists_offline = {}

    def put(p, d, did, received, ov):
        pid = by_did.get(did)
        if pid is None:
            return
        P.rep[(d, pid)] = (received, ov)

    def utc_min(s):
        t = dt.datetime.strptime(s.replace("Z", "").replace("T", " "), "%Y-%m-%d %H:%M:%S") - dt.timedelta(hours=UTC_OFFSET)
        return t.hour * 60 + t.minute + t.second / 60.0
    for r in rows(os.path.join(target, "corvane_event_report_2024_2026.csv")):
        d = (dt.datetime.strptime(r["event_start_utc"], "%Y-%m-%dT%H:%M:%SZ") - dt.timedelta(hours=UTC_OFFSET)).date()
        put("Corvane", d, r["device_serial"], r["ack"] == "Y", utc_min(r["opt_out_utc"]) if r["opt_out_utc"] else None)
    for r in rows(os.path.join(target, "lumivale_dr_events_cedar_brake.csv")):
        ov = None
        if r["override_time"]:
            h, m = map(int, r["override_time"].split(":"))
            ov = h * 60 + m + 0.5
        put("Lumivale", date(r["date"]), r["thermostat_id"], r["delivery"] == "delivered", ov)
    for r in rows(os.path.join(target, "ardena_event_outcomes.csv")):
        ov = None
        if r["OptOutTimestamp"]:
            t = dt.datetime.strptime(r["OptOutTimestamp"], "%m/%d/%Y %H:%M:%S")
            ov = t.hour * 60 + t.minute + t.second / 60.0
        put("Ardena", date(r["EventDate"]), r["DeviceID"], r["Outcome"] != "Offline", ov)
    s_on = P.settings["Ondera"]["s"]
    for r in rows(os.path.join(target, "ondera_events_cbec.csv")):
        put("Ondera", date(r["event_date"]), r["device"], True,
            s_on + int(r["override_minute"]) + 0.5 if r["override_minute"] != "" else None)
    for r in rows(os.path.join(target, "kitebrook_events_2024_2026.csv")):
        put("Kitebrook", date(r["EVENT_DATE"]), r["DEVICE"], True, utc_min(r["OVERRIDE_UTC"]) if r["OVERRIDE_UTC"] else None)
    for r in rows(os.path.join(target, "pinecrest_home_events.csv")):
        ov = None
        if r["opt_out_time"]:
            t = dt.datetime.strptime(r["opt_out_time"], "%Y-%m-%dT%H:%M:%S")
            ov = t.hour * 60 + t.minute + t.second / 60.0
        put("Pinecrest Home", date(r["date"]), r["device_id"], r["opted_out"] in ("true", "false"), ov)
    P.lists_offline = {"Corvane": True, "Lumivale": True, "Ardena": True, "Ondera": False, "Kitebrook": False,
                       "Pinecrest Home": False}
    # the research sample's 15-minute loads by account and day (kW over each interval)
    ami = {}
    with open(os.path.join(target, "ami_15min_reads_peak_partners_2024_2026.csv"), newline="", encoding="utf-8") as fh:
        rd = csv.reader(fh)
        head = next(rd)
        for r in rd:
            m, d = int(r[0]), date(r[1])
            a, set_on = P.meter_acct.get(m, (None, None))
            if a is None:
                continue
            if (a, d) in ami:
                continue
            ami[(a, d)] = np.array([float(x) * 4 if x != "" else np.nan for x in r[2:]])
    P.ami = ami
    P.ami_mins = np.arange(AMI_FROM, AMI_FROM + 32 * STEP, STEP)
    P.ami_accts = sorted({a for a, _ in ami})
    return P


def temp_at(P, d, minute):
    """the station's temperature at a minute, between the hourly readings (hour ending h is read at h:00 - 30)"""
    t = P.temp[d]
    x = (minute + 30) / 60.0
    h0 = int(np.floor(x))
    f = x - h0
    a = t.get(max(1, min(24, h0)), t[24])
    b = t.get(max(1, min(24, h0 + 1)), t[24])
    return a + (b - a) * f


def active(v, d):
    return v["joined"] <= d and (v["left"] is None or v["left"] > d)
