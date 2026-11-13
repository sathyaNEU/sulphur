"""task23 architecture 1: the records each organisation keeps, cut from the simulated landfill (world.py). Every
frame here is what the producing system would export: its own clock, its own units and codes, its own gaps."""
import datetime as dt
import math

import numpy as np
import pandas as pd

import params as P
import world as WD

MI = WD.month_index


def _holidays(y):
    def nth(month, weekday, n):
        d = dt.date(y, month, 1)
        while d.weekday() != weekday:
            d += dt.timedelta(1)
        return d + dt.timedelta(7 * (n - 1))

    def last(month, weekday):
        d = dt.date(y, month + 1, 1) - dt.timedelta(1) if month < 12 else dt.date(y, 12, 31)
        while d.weekday() != weekday:
            d -= dt.timedelta(1)
        return d
    return {dt.date(y, 1, 1), last(5, 0), dt.date(y, 7, 4), nth(9, 0, 1), nth(11, 3, 4), dt.date(y, 12, 25)}


# ------------------------------------------------------------------ scale tickets
OLD_CODES = {"MSW": ["MSW-COM", "MSW-RES", "MSW-TS"], "CD": ["CD-MIX"], "BIO": ["SLDG"], "SOIL": ["CVR-SOIL"],
             "SPEC": ["SPW-ASB", "SPW-OTH"]}
NEW_CODES = {"MSW": ["MSW"], "CD": ["C&D"], "BIO": ["BIOSOLIDS"], "SOIL": ["ADC-SOIL"], "SPEC": ["SPECIAL"]}
CODE_SWITCH = dt.date(2021, 7, 1)
HAULERS = {"MSW": [("Ridgeline Hauling", 0.31), ("North Fork Sanitation", 0.22), ("Harbor Point Waste", 0.19),
                   ("Kelloway County Transfer", 0.24), ("PUBLIC", 0.04)],
           "CD": [("Brennan Demolition", 0.30), ("Sound Roll-Off Co", 0.42), ("PUBLIC", 0.28)],
           "BIO": [("Kelloway Water Reclamation", 1.0)],
           "SOIL": [("Tamarack Excavating", 0.55), ("Kelloway County Roads", 0.45)],
           "SPEC": [("Westbay Abatement", 0.6), ("PUBLIC", 0.4)]}
LOAD_T = {("MSW", "Kelloway County Transfer"): (21.5, 2.2), ("MSW", "PUBLIC"): (0.45, 0.3), ("MSW", None): (9.6, 2.1),
          ("CD", None): (5.2, 2.0), ("CD", "PUBLIC"): (0.7, 0.5), ("BIO", None): (17.5, 2.5), ("SOIL", None): (16.0, 2.8),
          ("SPEC", None): (2.4, 1.1), ("SPEC", "PUBLIC"): (0.3, 0.2)}
TONS_PER_TONNE = 1.0 / 0.90718474
OUTAGES = [(dt.date(2025, 8, 11), dt.date(2025, 8, 22)), (dt.date(2026, 3, 2), dt.date(2026, 3, 6))]


def tickets(W):
    r = W.streams["tickets"]
    rows = []
    no = 2114301
    d = dt.date(2021, 1, 4)
    end = P.DATA_END.date()
    vehicles = {}
    while d <= end:
        y, m = d.year, d.month
        i = MI(y, m)
        hol = _holidays(y)
        wd = d.weekday()
        if wd == 6 or d in hol:
            d += dt.timedelta(1)
            continue
        # the month's operating days and their weights (Saturdays at about 45 per cent)
        first = dt.date(y, m, 1)
        days = [first + dt.timedelta(k) for k in range(WD.days_in_month(y, m))]
        wts = {dd: (0.45 if dd.weekday() == 5 else 1.0) for dd in days if dd.weekday() != 6 and dd not in hol}
        wsum = sum(wts.values())
        for c in P.CELLS:
            for mat in P.SHARE:
                t_month = W.tonnes[c][mat][i]
                if t_month <= 0:
                    continue
                t_day = t_month * wts[d] / wsum * math.exp(r.normal(0, 0.12))
                tons_day = t_day * TONS_PER_TONNE
                hl = HAULERS[mat]
                names = [h for h, _ in hl]
                pr = np.array([p for _, p in hl])
                while tons_day > 0.05:
                    h = names[r.choice(len(names), p=pr / pr.sum())]
                    mu, sd = LOAD_T.get((mat, h), LOAD_T[(mat, None)])
                    load = max(0.08, r.normal(mu, sd))
                    load = min(load, tons_day + 0.3)
                    tons_day -= load
                    key = (h, mat)
                    if key not in vehicles:
                        vehicles[key] = ["%s%03d" % ("".join(x[0] for x in h.split()[:2]).upper(), k)
                                         for k in r.choice(np.arange(100, 999), size=int(r.integers(4, 18)), replace=False)]
                    veh = "" if h == "PUBLIC" else str(r.choice(vehicles[key]))
                    tare_lb = {"MSW": 31000, "CD": 26000, "BIO": 29500, "SOIL": 27500, "SPEC": 18000}[mat]
                    if h == "PUBLIC":
                        tare_lb = 4800
                    tare_lb = int(round(r.normal(tare_lb, tare_lb * 0.06), -1))
                    net_lb = int(round(load * 2000, -1))
                    hh = int(np.clip(r.normal(11.2, 2.4), 6.6, 16.8))
                    mm_ = int(r.integers(0, 60))
                    codes = OLD_CODES[mat] if d < CODE_SWITCH else NEW_CODES[mat]
                    code = codes[0] if len(codes) == 1 else str(r.choice(codes))
                    cellcode = "C%d" % c
                    if d < dt.date(2022, 9, 12) and (wd == 5 or h == "PUBLIC") and r.random() < 0.55:
                        cellcode = ""
                    if any(a <= d <= b for a, b in OUTAGES):
                        cellcode = ""
                    rows.append([no, d, "%02d:%02d" % (hh, mm_), h, veh, code, tare_lb + net_lb, tare_lb, net_lb,
                                 round(net_lb / 2000.0, 2), cellcode, ""])
                    no += 1 + (1 if r.random() < 0.004 else 0)
        d += dt.timedelta(1)
    df = pd.DataFrame(rows, columns=["ticket_no", "ticket_date", "time_in", "hauler", "vehicle_id", "material_code",
                                     "gross_lb", "tare_lb", "net_lb", "net_tons", "disposal_area", "status"])
    df = df.sort_values(["ticket_date", "time_in", "ticket_no"], kind="stable").reset_index(drop=True)
    df["ticket_no"] = np.arange(len(df)) + 2114301 + np.cumsum((W.streams["tickets"].random(len(df)) < 0.003).astype(int))
    # voided tickets: a tare keyed wrong, voided and reissued a few minutes later with the right weights
    vi = np.where(W.streams["tickets"].random(len(df)) < 0.0055)[0]
    extra = []
    for k in vi:
        row = df.iloc[k].copy()
        bad = row.copy()
        bad["status"] = "VOID"
        if W.streams["tickets"].random() < 0.5:
            bad["tare_lb"] = int(row["tare_lb"] - 10000)
        else:
            bad["tare_lb"] = int(row["tare_lb"] + 9000)
        bad["net_lb"] = int(bad["gross_lb"] - bad["tare_lb"])
        bad["net_tons"] = round(bad["net_lb"] / 2000.0, 2)
        extra.append(bad)
        df.at[df.index[k], "status"] = "REISSUE"
    df = pd.concat([df, pd.DataFrame(extra)], ignore_index=True)
    df = df.sort_values(["ticket_date", "time_in", "status"], kind="stable").reset_index(drop=True)
    return df


# ------------------------------------------------------------------ the operations daily log
def daily_log(W):
    r = W.streams["log"]
    rows = []
    d = dt.date(2024, 1, 2)
    lift5 = 1
    while d <= P.DATA_END.date():
        if d.weekday() == 6 or d in _holidays(d.year):
            d += dt.timedelta(1)
            continue
        cell = 4 if d < dt.date(2025, 2, 3) else 5
        if cell == 5:
            lift5 = 1 + int((d - dt.date(2025, 2, 3)).days / 210)
        lift = "4-L9" if cell == 4 else "5-L%d" % lift5
        i0 = W.hour_index(dt.datetime(d.year, d.month, d.day, 6))
        rain = float(W.rain[i0:i0 + 12].sum())
        wind = float(W.wind[i0:i0 + 12].max())
        notes = []
        if rain > 6:
            notes.append(str(r.choice(["heavy rain, tipping pad muddy", "rain all shift, litter fence checked",
                                       "wet, dozer on mats"])))
        if wind > 10:
            notes.append(str(r.choice(["high wind, face reduced", "wind, litter crew out", "gusty, tarp held down"])))
        if r.random() < 0.025:
            notes.append(str(r.choice(["compactor down 3 h, hydraulic hose", "scale B offline AM", "fire watch on face",
                                       "survey crew on 5-L%d" % lift5, "leachate seep repaired, east toe"])))
        cover = "soil" if (d.weekday() == 5 or r.random() < 0.25) else "tarp"
        rows.append([d, "C%d" % cell, lift, cover, round(float(np.clip(r.normal(0.42, 0.18), 0, 1.4)), 2)
                     if r.random() < 0.08 else 0.0, round(rain, 1), "; ".join(notes)])
        d += dt.timedelta(1)
    return pd.DataFrame(rows, columns=["log_date", "active_cell", "working_lift", "daily_cover", "interim_cover_ac",
                                       "rain_6to18_mm", "supervisor_notes"])


# ------------------------------------------------------------------ the gas plant historian
def scada(W):
    r = W.streams["scada"]
    t0 = dt.datetime(2023, 1, 1, 0)
    t1 = P.DATA_END
    loc = []
    cur = t0.replace(tzinfo=P.TZ)
    # the historian logs local wall-clock hours (America/Los_Angeles), one row per wall-clock hour it saw
    utc = dt.datetime(2023, 1, 1, 8, tzinfo=P.UTC)
    end = dt.datetime(2026, 11, 1, 7, tzinfo=P.UTC)
    while utc <= end:
        loc.append(utc)
        utc += dt.timedelta(hours=1)
    n = len(loc)
    coll_m = sum(W.coll[c] for c in P.CELLS)                    # t CH4 per month
    ch4_m = np.zeros(WD.NM)
    for i in range(WD.NM):
        num = sum(W.coll[c][i] for c in P.CELLS)
        if num > 0:
            ch4_m[i] = sum(W.coll[c][i] * w for c, w in ((1, 46.5), (2, 47.5), (3, 48.6), (4, 52.8), (5, 54.0))) / num
    rows = []
    eng_down = {1: set(), 2: set()}
    # overhauls and trips
    for e in (1, 2):
        for y in (2023, 2024, 2025, 2026):
            s = dt.datetime(y, int(r.integers(2, 11)), int(r.integers(1, 26)), 7, tzinfo=P.UTC)
            for h in range(int(r.integers(80, 190))):
                eng_down[e].add(s + dt.timedelta(hours=h))
        for _ in range(int(r.integers(40, 60))):
            s = loc[int(r.integers(0, n - 30))]
            for h in range(int(r.integers(1, 9))):
                eng_down[e].add(s + dt.timedelta(hours=h))
    cal_hours = set(loc[k] for k in range(0, n, 24 * 14) for _ in [0])      # analyzer calibration, fortnightly
    for k, u in enumerate(loc):
        lt = u.astimezone(P.TZ)
        std = (u - dt.timedelta(hours=8)).replace(tzinfo=None)
        hi = W.hour_index(std)
        i = MI(std.year, std.month)
        out = hi in W.blower_out
        ch4_t_h = coll_m[i] / max(1.0, W.hrs_in_month[i] - W.out_hours[i]) * (1 + 0.04 * (W.mod["intermediate"][hi] - 1)) \
            * math.exp(r.normal(0, 0.03))
        if out:
            ch4_t_h = 0.0
        ch4_pct = ch4_m[i] + r.normal(0, 0.35)
        lfg_scfm = ch4_t_h * 1000.0 / P.KG_PER_SCF / 60.0 / (ch4_pct / 100.0)
        e_cap = 545.0
        e1 = 0.0 if (u in eng_down[1] or out) else min(e_cap, lfg_scfm * 0.5) * (1 + r.normal(0, 0.01))
        e2 = 0.0 if (u in eng_down[2] or out) else min(e_cap, lfg_scfm * 0.5) * (1 + r.normal(0, 0.01))
        fl = max(0.0, lfg_scfm - e1 - e2)
        kw1 = e1 * ch4_pct / 100 * 5.95 if e1 > 0 else 0.0
        kw2 = e2 * ch4_pct / 100 * 5.95 if e2 > 0 else 0.0
        fl_pct = ch4_pct + r.normal(0, 0.2)
        if u in cal_hours:
            fl_pct = 0.0
        rows.append([lt.strftime("%Y-%m-%d %H:%M"), "PDT" if lt.dst() else "PST", round(fl, 1), round(fl_pct, 2),
                     round(1480 + r.normal(0, 25) if fl > 30 else 95 + r.normal(0, 8)), round(e1, 1),
                     round(ch4_pct + r.normal(0, 0.15), 2) if e1 > 0 else "", round(kw1), round(e2, 1),
                     round(ch4_pct + r.normal(0, 0.15), 2) if e2 > 0 else "", round(kw2),
                     round(-0.4 + r.normal(0, 0.2), 1) if out else
                     round(-28.5 * (1 + 1.5 * (W.coll_factor[i] / max(1e-9, 1 - W.out_hours[i] / (WD.DIM[i] * 24)) - 1))
                           + r.normal(0, 1.6), 1)])
    df = pd.DataFrame(rows, columns=["timestamp_local", "tz", "flare_flow_scfm", "flare_ch4_pct", "flare_temp_f",
                                     "eng1_fuel_scfm", "eng1_ch4_pct", "eng1_kw", "eng2_fuel_scfm", "eng2_ch4_pct",
                                     "eng2_kw", "header_vac_inwc"])
    return df


# ------------------------------------------------------------------ wells: register and monthly readings
def register(W):
    r = W.streams["wells"]
    rows = []
    for k, w in enumerate(W.wells):
        e0, n0 = {1: (1218400, 742300), 2: (1219150, 742100), 3: (1219900, 741800), 4: (1220700, 741500)}[w["cell"]]
        rows.append(dict(well_id=w["id"], type="VW", cell=("" if (w["cell"] == 4 and k % 23 == 7) else w["cell"]),
                         installed=w["install"], decommissioned=None, total_depth_ft=w["depth"],
                         screen_top_ft=w["screen_top"], screen_bottom_ft=w["screen_bot"], casing_in=6,
                         northing_ft=int(n0 + r.normal(0, 350)), easting_ft=int(e0 + r.normal(0, 380)),
                         pump_installed=w["pump"], notes=""))
    for j, h in enumerate(["HC-4A", "HC-4B", "HC-4C", "HC-4D", "HC-4E", "HC-4F"]):
        rows.append(dict(well_id=h, type="HC", cell=4, installed=dt.date(2014 + j // 2, 3 + 3 * (j % 2), 1),
                         decommissioned=None, total_depth_ft=None, screen_top_ft=None, screen_bottom_ft=None,
                         casing_in=8, northing_ft=int(741500 + r.normal(0, 300)), easting_ft=int(1220700 + r.normal(0, 300)),
                         pump_installed=None, notes="converted to leachate injection line INJ-4%s 2023-04" % "ABCDEF"[j]))
    return pd.DataFrame(rows)


def readings(W):
    r = W.streams["wells"]
    rows = []
    for w in W.wells:
        inst = w["install"]
        for i in range(MI(2019, 1), MI(2026, 11)):
            y, m = WD.month_of_index(i)
            if dt.date(y, m, 28) < inst:
                continue
            if r.random() < 0.035:      # a missed visit
                continue
            day = int(np.clip(r.normal(10 + 3 * w["cell"], 3), 1, 27))
            vd = dt.date(y, m, day)
            while vd.weekday() > 4:
                vd += dt.timedelta(1)
            cw = W.coll_well[w["id"]][i]                       # t CH4 in the month
            ch4_scfm = cw * 1000.0 / P.KG_PER_SCF / (WD.DIM[i] * 1440.0)
            o2 = abs(r.normal(0.35, 0.3))
            if r.random() < 0.03:
                o2 = r.uniform(2.5, 6.0)
            ch4 = w["ch4"] - (o2 - 0.35) * 4.2 + r.normal(0, 0.9)
            co2 = ch4 * r.uniform(0.70, 0.80)
            flow = ch4_scfm / (ch4 / 100.0) * math.exp(r.normal(0, 0.09))
            sub = W.sub[w["id"]][i]
            depth_liq = ""
            if m in (1, 4, 7, 10):
                scr = w["screen_bot"] - w["screen_top"]
                lvl = w["screen_bot"] - sub * scr if sub > 0.005 else None
                if lvl is None:
                    depth_liq = "DRY" if r.random() < 0.7 else round(w["depth"] + r.uniform(0.3, 2.5), 1)
                else:
                    depth_liq = round(lvl + r.normal(0, 0.4), 1)
            temp = w["temp"] + (6.0 if (w["cell"] == 4 and w["wet"] and i >= MI(2023, 6)) else 0.0) + r.normal(0, 2.2)
            rows.append([w["id"], vd, round(ch4, 1), round(co2, 1), round(o2, 1), round(100 - ch4 - co2 - o2, 1),
                         round(temp, 0), round(-r.uniform(2, 14), 1), round(flow, 1), int(np.clip(r.normal(55, 18), 5, 100)),
                         depth_liq, str(r.choice(P.TECHS))])
    df = pd.DataFrame(rows, columns=["well_id", "visit_date", "ch4_pct", "co2_pct", "o2_pct", "balance_pct", "temp_f",
                                     "static_inwc", "adj_flow_scfm", "valve_pct", "depth_to_liquid_ft", "tech"])
    return df.sort_values(["visit_date", "well_id"], kind="stable").reset_index(drop=True)


# ------------------------------------------------------------------ CMMS work orders
def work_orders(W):
    r = W.streams["wo"]
    rows = []
    wo = 48210
    d = dt.date(2022, 1, 3)
    cells4 = [w for w in W.wells if w["cell"] == 4]
    pilot = [w for w in W.wells if w["pump"] is not None]
    for w in pilot:
        rows.append([0, P.PILOT_DATE - dt.timedelta(days=int(r.integers(1, 4))), P.PILOT_DATE, w["id"], "INSTALL",
                     "Install pneumatic pump and air line, pilot dewatering", "GCCS"])
    types = [("WELLHEAD", "Replace wellhead flex hose and sample port"), ("WELLHEAD", "Rebuild control valve"),
             ("PM", "Monthly wellfield tuning route"), ("PM", "Liquid level survey, quarterly"),
             ("FLARE", "Flare UV scanner fault, reset"), ("FLARE", "Flare thermocouple replaced"),
             ("ENGINE", "Engine oil change and spark plugs"), ("ENGINE", "Engine trip on high jacket water temp"),
             ("BLOWER", "Blower bearing grease and vibration check"), ("CONDENSATE", "Condensate sump pump replaced"),
             ("HEADER", "Header lateral settled, regraded"), ("LEACHATE", "Injection line INJ-4C flushed"),
             ("LEACHATE", "Injection pump seal leak")]
    while d <= P.DATA_END.date():
        for _ in range(int(r.poisson(2.1))):
            t, desc = types[int(r.integers(0, len(types)))]
            asset = "EW-%s" % str(r.choice([w["id"][3:] for w in W.wells])) if t == "WELLHEAD" else \
                {"FLARE": "FL-1", "ENGINE": str(r.choice(["ENG-1", "ENG-2"])), "BLOWER": str(r.choice(["BL-1", "BL-2"])),
                 "CONDENSATE": "CS-2", "HEADER": "HDR-4", "LEACHATE": "LCS-4", "PM": "WELLFIELD"}.get(t, "SITE")
            opened = d + dt.timedelta(days=int(r.integers(0, 6)))
            closed = opened + dt.timedelta(days=int(r.integers(0, 9)))
            rows.append([0, opened, closed, asset, t, desc, "GCCS" if t not in ("LEACHATE",) else "LEACHATE"])
        d += dt.timedelta(days=7)
    for w in cells4:
        if w["wet"] and r.random() < 0.18:
            dd = dt.date(2024, 1, 1) + dt.timedelta(days=int(r.integers(0, 900)))
            rows.append([0, dd, dd + dt.timedelta(days=int(r.integers(1, 20))), w["id"], "WELLHEAD",
                         "Well watered in, no flow at full vacuum; tech to check", "GCCS"])
    df = pd.DataFrame(rows, columns=["wo_no", "opened", "completed", "asset", "work_type", "description", "shop"])
    df = df.sort_values(["opened", "asset"], kind="stable").reset_index(drop=True)
    df["wo_no"] = np.arange(len(df)) * 3 + 48210 + np.cumsum((r.random(len(df)) < 0.2).astype(int))
    # the extract holds what the maintenance system had on the day it was pulled: an order still open then has no
    # completion date, and nothing opened after it is there
    pull = dt.date.fromisoformat(P.PULLED["workorders"])
    df = df[df["opened"] <= pull].copy()
    df["completed"] = [c if c <= pull else None for c in df["completed"]]
    return df.reset_index(drop=True)


def recirc_log(W):
    r = W.streams["misc"]
    rows = []
    for c, lines in ((4, ["INJ-4A", "INJ-4B", "INJ-4C", "INJ-4D", "INJ-4E", "INJ-4F"]), (5, ["INJ-5A", "INJ-5B", "INJ-5C"])):
        start = P.RECIRC[c]
        for i in range(MI(start.year, start.month), MI(2026, 11)):
            y, m = WD.month_of_index(i)
            for ln in lines:
                if r.random() < 0.07:
                    continue
                days = int(np.clip(r.normal(17, 5), 2, WD.days_in_month(y, m)))
                if i == MI(start.year, start.month):
                    days = min(days, WD.days_in_month(y, m) - start.day + 1)
                gal = int(round(days * r.uniform(9000, 16000) * (0.8 if c == 5 else 1.0), -2))
                rows.append([c, ln, "%04d-%02d" % (y, m), days, gal])
    return pd.DataFrame(rows, columns=["cell", "injection_line", "month", "days_injecting", "gallons"])


# ------------------------------------------------------------------ the on-site weather station
def weather(W):
    r = W.streams["misc"]
    n = W.hour_index(P.DATA_END) + 1
    ts = W.hours[:n]
    baro = W.pressure[:n] - 17.8
    resite = W.hour_index(dt.datetime(2023, 6, 21, 10))
    baro[resite:] -= 0.6
    rain = W.rain[:n].copy()
    clog0 = W.hour_index(dt.datetime(2021, 11, 14, 0))
    rain[clog0:clog0 + 24 * 9] = 0.0
    df = pd.DataFrame({"timestamp_lst": [t.strftime("%Y-%m-%dT%H:%M-08:00") for t in ts],
                       "baro_hpa": np.round(baro, 1), "air_temp_c": np.round(W.air_t[:n], 1),
                       "rh_pct": np.round(W.rh[:n]).astype(int), "wind_ms": np.round(W.wind[:n], 1),
                       "wind_dir_deg": np.round(W.wind_dir[:n]).astype(int), "rain_mm": rain,
                       "solar_wm2": np.round(W.solar[:n]).astype(int), "soil_temp_10cm_c": np.round(W.soil_t[:n], 1)})
    drop = r.random(n) < 0.004
    for k in range(3):
        s = int(r.integers(1000, n - 200))
        drop[s:s + int(r.integers(5, 40))] = True
    return df[~drop].reset_index(drop=True)


# ------------------------------------------------------------------ automated chambers
CHAMBERS = {"AC-1": dict(cell=4, cover="intermediate", start=dt.datetime(2025, 3, 12, 11), scale=1.35),
            "AC-2": dict(cell=3, cover="final", start=dt.datetime(2025, 3, 12, 14), scale=1.0),
            "AC-3": dict(cell=5, cover="active", start=dt.datetime(2026, 2, 4, 10), scale=1.20)}


def chambers(W):
    r = W.streams["chambers"]
    rows = []
    n_end = W.hour_index(P.DATA_END)
    rain6 = np.convolve(W.rain, np.ones(6), mode="full")[:W.n_hours]
    for cid, ch in CHAMBERS.items():
        c = ch["cell"]
        h0 = W.hour_index(ch["start"])
        gaps = np.zeros(W.n_hours, dtype=bool)
        for _ in range(int(r.integers(3, 6))):
            s = int(r.integers(h0 + 200, n_end - 400))
            gaps[s:s + int(r.integers(12, 160))] = True
        lid0 = int(r.integers(h0 + 1500, n_end - 600))
        for h in range(h0, n_end + 1):
            if gaps[h]:
                continue
            i = W._mi[h]
            mean_e = W.E[c][i] * 1e6 / P.CELLS[c]["area"] / WD.DIM[i]     # g/m2/d, the cell's surface emission
            T = W.soil_t[h]
            Tm = W.month_soil_t()[i]
            temp_f = (1 - 0.18 * (T - Tm) / 4.0)
            f = ch["scale"] * mean_e * W.mod[ch["cover"]][h] * temp_f * math.exp(-0.05 * rain6[h]) \
                * math.exp(r.normal(0, 0.16))
            flag = "OK"
            if lid0 <= h < lid0 + 130:
                f = abs(r.normal(0.4, 0.3))
                flag = "CHK"
            if c == 3:
                f = max(0.02, f + r.normal(0, 0.06))
            utc = (W.hours[h] + dt.timedelta(hours=8))
            rows.append([utc.strftime("%Y-%m-%d %H:%M:%SZ"), cid, round(f, 3), round(T + r.normal(0, 0.15), 1),
                         round(float(np.clip(0.24 + 0.012 * rain6[h] + r.normal(0, 0.01), 0.08, 0.48)), 3), flag])
    return pd.DataFrame(rows, columns=["utc", "chamber", "flux_g_m2_d", "soil_temp_c", "soil_vwc", "qc"])


# ------------------------------------------------------------------ measurement campaigns (the state's tracer, the division's drone)
def _eligible(W, d, h0, h1, lag, wmin, wmax):
    i0 = W.hour_index(dt.datetime(d.year, d.month, d.day, h0))
    i1 = i0 + (h1 - h0)
    if W.rain[i0 - lag:i1].any():
        return None
    w = W.wind[i0:i1]
    if w.min() < wmin or w.max() > wmax:
        return None
    return i0, i1


def _first_window(W, a, b, h0, h1, lag, wmin, wmax, avoid=()):
    d = a
    while True:
        if d.weekday() < 5 and d not in avoid:
            e = _eligible(W, d, h0, h1, lag, wmin, wmax)
            if e and d >= a:
                return d, e
        d += dt.timedelta(1)
        if d > b + dt.timedelta(days=21):
            raise RuntimeError("no window")


TCM_WINDOWS = [(dt.date(2025, 3, 10), dt.date(2025, 3, 31)), (dt.date(2025, 5, 12), dt.date(2025, 6, 2)),
               (dt.date(2025, 8, 4), dt.date(2025, 8, 25)), (dt.date(2025, 10, 13), dt.date(2025, 11, 3)),
               (dt.date(2026, 2, 23), dt.date(2026, 3, 16)), (dt.date(2026, 4, 20), dt.date(2026, 5, 11)),
               (dt.date(2026, 5, 25), dt.date(2026, 6, 15)), (dt.date(2026, 6, 29), dt.date(2026, 7, 10))]
DRONE_WINDOWS = [(dt.date(2024, 5, 6), dt.date(2024, 6, 14)), (dt.date(2024, 8, 5), dt.date(2024, 9, 13)),
                 (dt.date(2024, 11, 4), dt.date(2024, 12, 13)), (dt.date(2025, 2, 3), dt.date(2025, 3, 14)),
                 (dt.date(2025, 5, 5), dt.date(2025, 6, 13)), (dt.date(2025, 8, 4), dt.date(2025, 9, 12)),
                 (dt.date(2025, 11, 3), dt.date(2025, 12, 12)), (dt.date(2026, 2, 2), dt.date(2026, 3, 13)),
                 (dt.date(2026, 5, 4), dt.date(2026, 6, 12)), (dt.date(2026, 8, 3), dt.date(2026, 9, 11))]


def campaigns(W):
    r = W.streams["campaigns"]
    rows = []
    for k, (a, b) in enumerate(TCM_WINDOWS):
        dual = a.year == 2026
        # a two-tracer campaign needs steadier wind than a single-tracer one
        d, (i0, i1) = _first_window(W, a, b, 10, 15, 3, 3.0 if dual else 2.5, 7.0 if dual else 8.0)
        tot = W.E_hour[i0:i1].mean() * 1000.0                     # kg per hour
        c4 = W.E_hour_cell[4][i0:i1].mean() * 1000.0
        c5 = W.E_hour_cell[5][i0:i1].mean() * 1000.0
        e_tot = tot * math.exp(r.normal(0, 0.07))
        e4 = c4 * math.exp(r.normal(0, 0.09)) if dual else None
        e5 = c5 * math.exp(r.normal(0, 0.12)) if dual else None
        rows.append(dict(campaign="FRL-%d-%02d" % (d.year, k % 4 + 1), date=d, start_local="%02d:%02d" % (10, int(r.integers(5, 40))),
                         end_local="%02d:%02d" % (14, int(r.integers(10, 55))), tracers="C2H2 + N2O" if dual else "C2H2",
                         transects=int(r.integers(9, 17)), mean_distance_km=round(float(r.uniform(1.2, 2.8)), 1),
                         wind_ms=round(float(W.wind[i0:i1].mean()), 1), wind_dir_deg=int(W.wind_dir[i0:i1].mean()),
                         air_temp_c=round(float(W.air_t[i0:i1].mean()), 1),
                         site_kg_h=round(e_tot), site_sd_kg_h=round(e_tot * float(r.uniform(0.11, 0.15))),
                         cell4_kg_h=round(e4) if dual else None, cell4_sd_kg_h=round(e4 * float(r.uniform(0.12, 0.17))) if dual else None,
                         cell5_kg_h=round(e5) if dual else None, cell5_sd_kg_h=round(e5 * float(r.uniform(0.15, 0.22))) if dual else None,
                         _i0=i0, _i1=i1))
    return pd.DataFrame(rows)


def drone(W):
    r = W.streams["drone"]
    rows = []
    for k, (a, b) in enumerate(DRONE_WINDOWS):
        d, _ = _first_window(W, a, b, 11, 14, 3, 3.0, 9.0)
        # the flight's own hours on the local clock, then the station's standard-time hours they cover
        off = dt.datetime(d.year, d.month, d.day, 10, 0) + dt.timedelta(minutes=int(r.integers(5, 170)))
        land = off + dt.timedelta(minutes=int(r.integers(125, 176)))
        lst = lambda t: (t.replace(tzinfo=P.TZ).astimezone(P.UTC) - dt.timedelta(hours=8)).replace(tzinfo=None)
        i0 = W.hour_index(lst(off).replace(minute=0))
        i1 = W.hour_index(lst(land).replace(minute=0)) + 1
        tot = W.E_hour[i0:i1].mean() * 1000.0
        est = tot * math.exp(r.normal(0, 0.13))
        rows.append(dict(flight="DMB-%02d" % (k + 1), date=d, takeoff=off.strftime("%H:%M"),
                         landing=land.strftime("%H:%M"), wind_ms=round(float(W.wind[i0:i1].mean()), 1),
                         wind_dir_deg=int(W.wind_dir[i0:i1].mean()), passes=int(r.integers(6, 11)),
                         flux_kg_h=round(est), unc_pct=int(r.integers(22, 31)), pilot=P.ENGINEER, _i0=i0, _i1=i1))
    return pd.DataFrame(rows)


# ------------------------------------------------------------------ the 2019 cover oxidation study
def ox_plots(W):
    r = W.streams["study"]
    rows = []
    visits = [dt.date(2019, 2, 26), dt.date(2019, 5, 21), dt.date(2019, 8, 13), dt.date(2019, 11, 5)]
    plan = [(2, "final", 8), (3, "final", 10), (4, "intermediate", 14), (4, "active", 12)]
    pid = 0
    for c, cover, k in plan:
        for j in range(k):
            pid += 1
            het = math.exp(r.normal(0, 0.95 if cover == "active" else 0.75))
            for v, vd in enumerate(visits):
                vd2 = vd + dt.timedelta(days=int(r.integers(0, 3)))
                i = MI(vd2.year, vd2.month)
                u_mean = W.U[c][i] * 1e6 / P.CELLS[c]["area"] / WD.DIM[i]
                if cover == "active":
                    u_mean *= 1.0
                if cover == "intermediate":
                    u_mean *= 3.4
                hi = W.hour_index(dt.datetime(vd2.year, vd2.month, vd2.day, 11))
                T = float(W.soil_t[hi:hi + 4].mean())
                J = u_mean * het * math.exp(r.normal(0, 0.25))
                V = W.vox(cover, T)
                f = V / (V + J)
                surf = J * (1 - f) * math.exp(r.normal(0, 0.08))
                dA = -58.2 + r.normal(0, 1.2)
                dE = dA + 25.0 * f + r.normal(0, 0.55)
                fo = (dE - dA) / 25.0
                note = ""
                if r.random() < 0.04:
                    dE, fo, note = None, None, "isotope run failed"
                rows.append(["P%02d" % pid, c, cover, vd2, round(surf, 2), round(T, 1),
                             None if dE is None else round(dE, 2), round(dA, 2),
                             None if fo is None else round(max(0.0, fo), 3), note])
    return pd.DataFrame(rows, columns=["plot_id", "cell", "cover", "visit_date", "surface_flux_g_m2_d", "soil_temp_c",
                                       "d13c_emitted_permil", "d13c_anoxic_permil", "fraction_oxidized", "notes"])


# ------------------------------------------------------------------ distractors
def groundwater(W):
    r = W.streams["gw"]
    rows = []
    wells = ["MW-%02d" % k for k in range(1, 25)]
    analytes = [("Chloride", "mg/L", 18, 0.4), ("Ammonia-N", "mg/L", 0.6, 0.8), ("Iron", "mg/L", 2.1, 0.7),
                ("Manganese", "mg/L", 0.35, 0.8), ("Arsenic", "ug/L", 3.2, 0.5), ("Vinyl chloride", "ug/L", 0.1, 1.2),
                ("Benzene", "ug/L", 0.12, 1.1), ("TDS", "mg/L", 240, 0.3), ("Specific conductance", "uS/cm", 410, 0.3)]
    for y in range(2019, 2027):
        for q, mth in enumerate((2, 5, 8, 11)):
            if dt.date(y, mth, 20) > P.DATA_END.date():
                continue
            for wl in wells:
                d = dt.date(y, mth, int(r.integers(8, 24)))
                for a, u, base, sd in analytes:
                    v = base * math.exp(r.normal(0, sd)) * (1.6 if wl in ("MW-07", "MW-11") and a in ("Chloride", "TDS") else 1.0)
                    q_ = ""
                    if a in ("Vinyl chloride", "Benzene") and v < 0.2:
                        v, q_ = 0.2, "U"
                    rows.append([wl, d, a, round(v, 3), u, q_, "Northcoast Analytical"])
    return pd.DataFrame(rows, columns=["well", "sample_date", "analyte", "result", "units", "qualifier", "lab"])


def leachate(W):
    r = W.streams["leach"]
    rows = []
    for i in range(MI(2019, 1), MI(2026, 11)):
        y, m = WD.month_of_index(i)
        wet = 1.0 + 0.8 * (m in (11, 12, 1, 2, 3))
        rows.append(["%04d-%02d" % (y, m), int(round(2.1e6 * wet * math.exp(r.normal(0, 0.15)), -3)),
                     round(3400 * math.exp(r.normal(0, 0.25)), 0), round(1500 * math.exp(r.normal(0, 0.3)), 0),
                     round(680 * math.exp(r.normal(0, 0.2)), 0), round(1650 * math.exp(r.normal(0, 0.15)), 0),
                     round(7.3 + r.normal(0, 0.15), 2)])
    return pd.DataFrame(rows, columns=["month", "leachate_hauled_gal", "cod_mg_l", "bod5_mg_l", "nh3n_mg_l",
                                       "chloride_mg_l", "ph"])


def sem(W):
    r = W.streams["sem"]
    rows = []
    for y in range(2023, 2027):
        for mth in (3, 6, 9, 12):
            if dt.date(y, mth, 15) > P.DATA_END.date():
                continue
            d = dt.date(y, mth, int(r.integers(5, 25)))
            for c in (3, 4, 5):
                if c == 5 and dt.date(y, mth, 1) < dt.date(2025, 3, 1):
                    continue
                for g in range(int(80 if c != 3 else 40)):
                    base = {3: 6, 4: 45, 5: 70}[c]
                    v = base * math.exp(r.normal(0, 1.1))
                    rows.append([d, "C%d" % c, "%s-%03d" % ("ABCDEFGH"[g % 8], g), round(v, 1),
                                 "EXC" if v > 500 else "", str(r.choice(P.TECHS))])
    return pd.DataFrame(rows, columns=["survey_date", "cell", "grid_point", "ch4_ppm_inst", "flag", "tech"])


def odor(W):
    r = W.streams["odor"]
    rows = []
    d = dt.date(2024, 1, 1)
    places = ["Fernhallow Rd", "Tolland Creek Estates", "SR-9 at Mile 14", "Larch Hill Dr", "Brask Lake boat launch",
              "Kessel Rd", "Pine Hollow Ln"]
    while d <= P.DATA_END.date():
        if r.random() < 0.18:
            hi = W.hour_index(dt.datetime(d.year, d.month, d.day, 7))
            rows.append([d, "%02d:%02d" % (int(r.integers(5, 22)), int(r.integers(0, 60))), str(r.choice(places)),
                         int(W.wind_dir[hi]), str(r.choice(["garbage smell", "gas smell near road", "sour odor at dusk",
                                                           "strong odor this morning", "smell inside house"])),
                         str(r.choice(["inspected, no odor found", "odor confirmed, face covered", "logged",
                                       "called back, resolved"]))])
        d += dt.timedelta(1)
    return pd.DataFrame(rows, columns=["date", "time", "location", "wind_dir_deg_7am", "description", "response"])
