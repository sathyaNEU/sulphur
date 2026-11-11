"""Read the pack as a solver has to: from the files under target/ alone, cleaned and conformed.

Time is put on one clock (local wall-clock hours since Monday 3 August 2026, 00:00); the telephony export is in UTC
and crosses the end of daylight saving time. Tracking numbers are brought to one form. Each channel's codes are
mapped to the ten reason families through the division's code lists.
"""
import datetime as dt
import os

import numpy as np
import openpyxl
import pandas as pd

import pack as PK
import params as P

EPOCH = pd.Timestamp(dt.datetime.combine(P.START, dt.time()))
DST_UTC = pd.Timestamp("2026-10-25 01:00:00")


def norm(s):
    s = s.fillna("").astype(str).str.replace(" ", "", regex=False).str.upper()
    return s.where(~s.str.fullmatch(r"\d{11}"), "QP" + s)


def hours(ts):
    return (pd.to_datetime(ts) - EPOCH) / pd.Timedelta(hours=1)


def utc_hours(ts):
    t = pd.to_datetime(ts.str.replace("T", " ", regex=False).str.replace("Z", "", regex=False))
    loc = t + pd.to_timedelta(np.where(t < DST_UTC, 2, 1), unit="h")
    return (loc - EPOCH) / pd.Timedelta(hours=1)


def load(target):
    f = {k: os.path.join(target, v) for k, v in PK.FILES.items()}
    D = {}
    intents = pd.read_csv(f["intents"], dtype=str).fillna("")
    wrap = pd.read_csv(f["wrapup"], dtype=str).fillna("")
    cats = pd.read_csv(f["categories"], dtype=str).fillna("")
    fam_of_intent = dict(zip(intents.intent, intents.reason_family))
    fam_of_wrap = dict(zip(wrap.wrapup_code, wrap.reason_family))

    cons = pd.read_csv(f["cons"], dtype=str).fillna("")
    cons["due"] = ((pd.to_datetime(cons.promised_date) - EPOCH) / pd.Timedelta(days=1)).astype(int)
    cons["cls"] = cons.outcome_class.map({"ON_TIME": "ON", "LATE_1": "L1", "LATE_2PLUS": "L2", "EXCEPTION": "EX"}).fillna("")
    D["cons"] = cons.set_index("tracking_no")[["depot", "due", "cls"]]

    a = pd.read_csv(f["assistant"], dtype=str).fillna("")
    D["assistant_rows"] = len(a)
    a = a.drop_duplicates("conversation_id")
    D["assistant_distinct"] = len(a)
    a = a.copy()
    a["trk"] = norm(a.tracking_no)
    a["fam"] = a.intent.map(fam_of_intent).fillna("")
    a = a[(a.trk != "") & (a.fam != "")].copy()
    a["start"] = hours(a.started_at); a["end"] = hours(a.ended_at)
    a["v3"] = a.build.str.startswith("3.")
    a = a.join(D["cons"], on="trk")
    a = a.sort_values(["trk", "start"]).reset_index(drop=True)
    D["A"] = a

    c = pd.read_csv(f["calls"], dtype=str).fillna("")
    D["call_rows"] = len(c)
    c = c[c.direction == "IN"]
    c = c[c.leg == "1"].copy()
    c["start"] = utc_hours(c.start_utc)
    c["trk"] = norm(c.tracking_keyed)
    c["fam"] = c.wrapup_code.map(fam_of_wrap).fillna("")
    c["wait"] = c.queue_wait_s.astype(float)
    c["keyed"] = c.trk != ""
    D["P"] = c.reset_index(drop=True)

    h = pd.read_csv(f["chat"], dtype=str).fillna("")
    h["trk"] = norm(h.tracking_no)
    h["start"] = hours(h.started_at)
    D["C"] = h[h.trk != ""].reset_index(drop=True)

    k = pd.read_csv(f["cases"], dtype=str).fillna("")
    k["trk"] = norm(k.tracking_no)
    k["start"] = hours(k.created_at)
    k["closed"] = hours(k.closed_at)
    k["customer"] = k.origin.isin(["WEB_FORM", "EMAIL"])
    k["week"] = (k.start // 168).astype(int)
    k["day"] = (k.start // 24).astype(int)
    D["K"] = k.reset_index(drop=True)

    wb = openpyxl.load_workbook(f["backlog"], data_only=True)
    rows = list(wb["Open by age"].iter_rows(values_only=True))[1:]
    b = pd.DataFrame(rows, columns=["snap", "queue", "who", "age", "open"])
    b["snap"] = pd.to_datetime(b.snap)
    b["age0"] = pd.to_numeric(b.age, errors="coerce").fillna(42).astype(int)
    D["backlog"] = b
    fl = pd.DataFrame(list(wb["Weekly flow"].iter_rows(values_only=True))[1:], columns=["week", "queue", "who", "opened", "closed"])
    fl["week"] = pd.to_datetime(fl.week)
    D["flow"] = fl

    n = pd.read_csv(f["network"])
    n["due"] = ((pd.to_datetime(n.due_date) - EPOCH) / pd.Timedelta(days=1)).astype(int)
    D["net"] = n

    wb = openpyxl.load_workbook(f["plan"], data_only=True)
    vol = list(wb["Volumes"].iter_rows(values_only=True))
    D["plan_parcels"] = np.array([r[-1] for r in vol[1:]], dtype=float)
    sv = list(wb["Service levels"].iter_rows(values_only=True))[1:]
    D["plan_service"] = np.array([r[1:5] for r in sv], dtype=float) / 100.0
    nt = list(wb["Notifications"].iter_rows(values_only=True))[1:]
    D["alerts_from"] = {r[0].split()[0]: int((pd.Timestamp(r[1]) - EPOCH) / pd.Timedelta(days=1)) for r in nt}

    wb = openpyxl.load_workbook(f["acd"], data_only=True)
    D["acd"] = pd.DataFrame(list(wb["Handled calls"].iter_rows(values_only=True))[1:], columns=["week", "queue", "inbound", "transferred", "outbound"])
    return D
