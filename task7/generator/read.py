"""Read the cut pack back into the arrays core.py's estimators take: the enrolled A/C switches as the register lists
them, each paging group's step on each feeder at each trial command, the per-day reach of every switch to an on-air
transmitter of its own paging system, the replaced-unit flag from the rebates and the permits, the cooling index and
the study homes' responses. Everything here is parsed from the shipped files; nothing comes from the generator."""
import csv
import datetime as dt
import os
import re
import zipfile
from collections import defaultdict

import numpy as np
from openpyxl import load_workbook

CDT = dt.timezone(dt.timedelta(hours=-5))
UTC = dt.timezone.utc
ABBR = {"STREET": "ST", "AVENUE": "AVE", "DRIVE": "DR", "LANE": "LN", "COURT": "CT", "PLACE": "PL", "ROAD": "RD",
        "NORTH": "N", "SOUTH": "S", "EAST": "E", "WEST": "W"}
QUAL_EQUIP = {"Central air conditioner", "Central heat pump (air source)"}
QUAL_WORK = {"REPLACE A/C CONDENSING UNIT", "REPLACE CONDENSING UNIT AND COIL", "HEAT PUMP CHANGE-OUT, SPLIT SYSTEM"}
NICK = {"HQ tower": "VHF-01", "MF sub stick": "VHF-02", "Hal sub VHF": "VHF-03", "Halverson VHF": "VHF-03",
        "TCP Larkin": "TCP-104", "TCP Sandhill": "TCP-117", "TCP Ostrander": "TCP-121", "TCP Pruett": "TCP-133",
        "TCP Bluestem": "TCP-109"}
KETTLE_RIDGE, HALVERSON_FILL = (-31.0, 12.0), (3.0, 25.0)


def rows(path):
    with open(path, newline="") as fh:
        return list(csv.DictReader(fh))


def norm(a):
    t = " ".join(a.upper().replace(".", " ").replace(",", " ").split())
    return " ".join(ABBR.get(w, w) for w in t.split())


def key_address(a, normalise=True):
    """The address join key: the full normalisation, a partial one (upper case and abbreviations only, the odd
    period and doubled space left in), or none."""
    if normalise is True:
        return norm(a)
    if normalise == "partial":
        return " ".join(ABBR.get(w, w) for w in a.upper().split(" "))
    return a


def held_mask(v):
    """A historian dropout holds the last good reading: three or more equal readings in a row, all but the first held."""
    n = len(v)
    out = np.zeros(n, bool)
    i = 0
    while i < n:
        j = i
        while j + 1 < n and v[j + 1] == v[i]:
            j += 1
        if j - i + 1 >= 3:
            out[i + 1:j + 1] = True
        i = j + 1
    return out


def read(target, window=5, hold=True, renamed=True, old_numbers=True, normalise=True, dated=True):
    """hold, renamed, old_numbers, normalise, dated: the golden's handling of each piece of the record's mess (each
    False is that item mishandled, for the neutrality checks)."""
    T = lambda name: os.path.join(target, name)
    # ---- the switch register: active A/C switches ----
    reg = [r for r in rows(T("lm_switch_register.csv")) if r["load_controlled"] == "Central air conditioner" and r["status"] == "Active"]
    feeders = sorted({r["feeder"] for r in rows(T("scada_point_list.csv"))})
    fidx = {c: i for i, c in enumerate(feeders)}
    pts = rows(T("scada_point_list.csv"))
    district_of = {}
    tag_feeder = []
    for p in pts:
        district_of[p["feeder"]] = p["district"]
        ins = dt.datetime.strptime(p["in_service"], "%Y-%m-%d %H:%M") if " " in p["in_service"] else \
            dt.datetime.strptime(p["in_service"], "%Y-%m-%d")
        ret = dt.datetime.strptime(p["retired"], "%Y-%m-%d %H:%M") if p["retired"] else None
        tag_feeder.append((p["point"], p["feeder"], ins.replace(tzinfo=CDT), ret.replace(tzinfo=CDT) if ret else None))
    dnames = ["Larkin", "Medora Flats", "Halverson", "Pruett"]
    dist = np.array([dnames.index(district_of[c]) for c in feeders])
    n_s = len(reg)
    sf = np.array([fidx[r["feeder"]] for r in reg])
    x = np.array([float(r["grid_x_km"]) for r in reg])
    y = np.array([float(r["grid_y_km"]) for r in reg])
    inst = [dt.date.fromisoformat(r["install_date"]) for r in reg]
    yr = np.array([d.year for d in inst])
    vhf = np.array([r["receiver"].startswith("VHF") for r in reg])
    grp = np.array([int(r["paging_group"].split("-")[1]) - 1 for r in reg])
    # ---- the encoder log: the trial's event days and each shed's first transmit ----
    first = {}
    for r in rows(T("paging_encoder_log_2026.csv")):
        if r["command"] != "SHED" or not r["group"].startswith("AC-"):
            continue
        t = dt.datetime.strptime(r["tx_time_local"], "%m/%d/%Y %H:%M:%S").replace(tzinfo=CDT)
        if not (15 <= t.hour < 19):
            continue                                   # the May address checks went out in the morning
        g = int(r["group"].split("-")[1]) - 1
        k = (t.date(), g)
        first[k] = min(first.get(k, t), t)
    days = sorted({d for d, _ in first})
    n_events = len(days)
    disp = np.zeros((n_events, 16), bool)
    for (d, g) in first:
        disp[days.index(d), g] = True
    # ---- SCADA: each feeder's minutes on each event day, de-duplicated, held readings out ----
    tags = defaultdict(list)
    for tag, fc, ins, ret in tag_feeder:
        tags[tag].append((fc, ins, ret))
    series = defaultdict(dict)
    with open(T("scada_feeder_1min_2026.csv"), newline="") as fh:
        rd = csv.reader(fh)
        next(rd)
        for t, tag, kw in rd:
            tl = dt.datetime.strptime(t, "%Y-%m-%d %H:%M:%S").replace(tzinfo=UTC).astimezone(CDT)
            fc = None
            for c, ins, ret in tags[tag]:
                if tl >= ins and (ret is None or tl < ret):
                    fc = c
            if not renamed and not re.fullmatch(r"[A-Z]{3}\.F\d\d\.KW_3PH", tag):
                continue                               # a point whose tag does not read as a feeder
            key = (fc, tl.date())
            m = (tl.hour - 15) * 60 + tl.minute
            if m not in series[key]:
                series[key][m] = float(kw)
    arr = {}
    for key, mm in series.items():
        if key[0] is None:
            continue
        v = np.array([mm.get(m, np.nan) for m in range(300)])
        arr[key] = (v, held_mask(v) if hold else np.zeros(300, bool))
    n_feed = len(feeders)
    obs_e, obs_g, obs_f, step = [], [], [], []
    for e, d in enumerate(days):
        for g in np.flatnonzero(disp[e]):
            t0 = first[(d, int(g))]
            M = (t0.hour - 15) * 60 + t0.minute
            for f, fc in enumerate(feeders):
                v, h = arr.get((fc, d), (np.full(300, np.nan), np.zeros(300, bool)))
                B = [i for i in range(M - window, M) if not h[i]]
                A = [i for i in range(M, M + window) if not h[i]]
                obs_e.append(e)
                obs_g.append(int(g))
                obs_f.append(f)
                step.append(float(np.mean(v[B]) - np.mean(v[A])))
    load = np.zeros(n_feed)
    for f, fc in enumerate(feeders):
        vals = np.concatenate([arr[(fc, d)][0][:45][~arr[(fc, d)][1][:45]] for d in days if (fc, d) in arr])
        load[f] = np.nanmean(vals)
    # ---- the cooling index ----
    idx = {dt.date.fromisoformat(r["date"]): float(r["cooling_index"]) for r in rows(T("sunflower_basin_cooling_index_2026.csv"))}
    wx = np.array([idx[d] for d in days])
    # ---- transmitters: which were on the air for each event's sheds; every listed one for 2027 ----
    wb = load_workbook(T("paging_transmitters.xlsx"), data_only=True)
    ws = wb["Paging sites"]
    sites = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] is None:
            continue
        on = row[6].date() if isinstance(row[6], dt.datetime) else row[6]
        off = row[7].date() if isinstance(row[7], dt.datetime) else row[7]
        sites.append(dict(id=row[0], system=row[2], x=float(row[4]), y=float(row[5]), on=on, off=off))
    wb2 = load_workbook(T("radio_shop_outage_log_2026.xlsx"), data_only=True)
    outs = []
    for row in wb2["2026"].iter_rows(min_row=2, values_only=True):
        if row[0] is None:
            continue
        outs.append((NICK[row[0]], row[1], row[2]))
    on_air = np.zeros((n_events, len(sites)), bool)
    for e, d in enumerate(days):
        w0 = dt.datetime(d.year, d.month, d.day, 16, 0)
        w1 = dt.datetime(d.year, d.month, d.day, 18, 0)
        for j, s in enumerate(sites):
            ok = s["on"] <= d and (s["off"] is None or s["off"] > d)
            for sid, a, b in outs:
                if sid == s["id"] and a < w1 and b > w0:
                    ok = False
            on_air[e, j] = ok
    sx = np.array([s["x"] for s in sites])
    sy = np.array([s["y"] for s in sites])
    sv = np.array([s["system"] == "VHF" for s in sites])
    listed = np.array([s["off"] is None for s in sites])
    D = np.sqrt((x[:, None] - sx[None, :]) ** 2 + (y[:, None] - sy[None, :]) ** 2)
    own = np.where(vhf[:, None], sv[None, :], ~sv[None, :])
    reach = np.empty((n_events, n_s))
    for e in range(n_events):
        reach[e] = np.where(own & on_air[e][None, :], D, 1e9).min(1)
    now = np.where(own & listed[None, :], D, 1e9).min(1)
    static_any = np.where(listed[None, :], D, 1e9).min(1)
    dv_now = np.where(sv[None, :] & listed[None, :], D, 1e9).min(1)
    dc_now = np.where(~sv[None, :] & listed[None, :], D, 1e9).min(1)
    d_new_v = np.minimum(dv_now, np.hypot(x - KETTLE_RIDGE[0], y - KETTLE_RIDGE[1]))
    d_new_c = np.minimum(dc_now, np.hypot(x - HALVERSON_FILL[0], y - HALVERSON_FILL[1]))
    # ---- the replaced-unit flag: a qualifying rebate or permit dated after the switch went in ----
    by_no, by_old, by_addr = {}, {}, {}
    for i, r in enumerate(reg):
        by_no[r["premise_no"]] = i
        if r["old_premise_no"]:
            by_old[r["old_premise_no"]] = i
        by_addr[(key_address(r["service_address"], normalise), r["city"].upper() if normalise else r["city"])] = i
    flag = np.zeros(n_s, bool)
    for r in rows(T("hvac_rebates_2012_2026.csv")):
        if r["equipment"] not in QUAL_EQUIP:
            continue
        old_ok = old_numbers is True or (old_numbers == "before" and dt.date.fromisoformat(r["equipment_installed"]) < dt.date(2021, 4, 1))
        i = by_no.get(r["premise_no"], by_old.get(r["premise_no"]) if old_ok else None)
        if i is not None and (not dated or dt.date.fromisoformat(r["equipment_installed"]) > inst[i]):
            flag[i] = True
    for r in rows(T("county_mechanical_permits_2010_2026.csv")):
        if r["work"] not in QUAL_WORK:
            continue
        i = by_addr.get((key_address(r["site_address"], normalise), r["city"].upper() if normalise else r["city"]))
        if i is not None and (not dated or dt.date.fromisoformat(r["issued"]) > inst[i]):
            flag[i] = True
    # ---- the study homes: each shed day's response against its own morning, scaled by the held-out homes ----
    homes = rows(T("study_homes.csv"))
    hid = sorted(h["home_id"] for h in homes)
    meter = {h["home_id"]: h["interval_meter"] for h in homes}
    arm = {(r["home_id"], dt.date.fromisoformat(r["event_date"])): r["arm"] for r in rows(T("study_event_assignments_2026.csv"))}
    kwh = defaultdict(dict)
    with open(T("study_meters_hourly_2026.csv"), newline="") as fh:
        rd = csv.reader(fh)
        next(rd)
        for m, t, v in rd:
            d = dt.date.fromisoformat(t[:10])
            kwh[(m, d)][int(t[11:13])] = float(v)
    n_st = len(hid)
    s_resp = np.zeros((n_events, n_st))
    s_tr = np.zeros((n_events, n_st), bool)
    for e, d in enumerate(days):
        pre = np.array([kwh[(meter[h], d)][13] + kwh[(meter[h], d)][14] for h in hid])
        sh = np.array([kwh[(meter[h], d)][16] + kwh[(meter[h], d)][17] for h in hid])
        tr = np.array([arm[(h, d)] == "shed" for h in hid])
        ratio = sh[~tr].sum() / pre[~tr].sum()
        s_tr[e] = tr
        s_resp[e] = np.where(tr, (pre * ratio - sh) / (2.0 * wx[e]), 0.0)
    age = 2026 - yr
    batch_age = np.array([age[grp == g].mean() for g in range(16)])
    wd = dict(n_s=n_s, n_feed=n_feed, n_events=n_events, dist=dist, sf=sf, x=x, y=y, yr=yr, vhf=vhf, age=age, grp=grp,
              disp=disp, obs=(np.array(obs_e), np.array(obs_g), np.array(obs_f)), step=np.array(step), load=load, w=wx,
              wx=wx, reach=reach, now=now, static_any=static_any, d_new_v=d_new_v, d_new_c=d_new_c, flag=flag,
              study=(s_resp, s_tr), batch_age=batch_age)
    extra = dict(feeders=feeders, days=days, first=first, reg=reg, inst=inst, sites=sites, on_air=on_air, series=arr,
                 hid=hid, idx=idx)
    return wd, extra


def steps_for_window(wd, extra, before, after=None):
    """The same arrays with each step re-measured: the mean of `after` minutes from the transmit minute less the mean of
    the `before` minutes before it, held readings out."""
    after = before if after is None else after
    days, feeders, first, arr = extra["days"], extra["feeders"], extra["first"], extra["series"]
    obs_e, obs_g, obs_f = wd["obs"]
    step = np.empty(len(obs_e))
    for i, (e, g, f) in enumerate(zip(obs_e, obs_g, obs_f)):
        d = days[e]
        t0 = first[(d, int(g))]
        M = (t0.hour - 15) * 60 + t0.minute
        v, h = arr[(feeders[f], d)]
        B = [j for j in range(M - before, M) if not h[j]]
        A = [j for j in range(M, M + after) if not h[j]]
        step[i] = float(np.mean(v[B]) - np.mean(v[A]))
    return dict(wd, step=step)
