"""task10 architecture 5: the clean truth of Wealdmoor Power Networks' Halverton zone.

Nine 33/11 kV primaries, three winters (October to March, 2023/24 to 2025/26) of half-hourly demand driven by the
reference station's daily mean temperature, four flexibility zones whose providers were scheduled day-ahead from
November 2024, each provider's own reduction falling as the event day gets colder, and the control room's
pre-planned 11 kV transfer schemes, armed for the event window at three of the zones, moving a feeder section onto
the neighbouring primary. Nothing here is written to the pack; pack.py writes what the systems record."""
import datetime as dt
import math

import numpy as np

SEED = 20261108
UTC = dt.timezone.utc

WINTERS = [("2023/24", dt.date(2023, 10, 1), dt.date(2024, 3, 31)),
           ("2024/25", dt.date(2024, 10, 1), dt.date(2025, 3, 31)),
           ("2025/26", dt.date(2025, 10, 1), dt.date(2026, 3, 31))]
BANK_HOLIDAYS = {dt.date(2023, 12, 25), dt.date(2023, 12, 26), dt.date(2024, 1, 1), dt.date(2024, 3, 29),
                 dt.date(2024, 12, 25), dt.date(2024, 12, 26), dt.date(2025, 1, 1),
                 dt.date(2025, 12, 25), dt.date(2025, 12, 26), dt.date(2026, 1, 1)}
TB = 15.5            # balance temperature of the zone's load (the truth; never filed)
T_DESIGN = -3.0      # the guideline's design condition, daily mean at Halverton weather station
WINDOW_LOCAL = (16, 0, 19, 30)
CREDIT_HH = ("17:30", "18:00")   # half-hours ending, local, in which the guideline credits flexibility
GROWTH_YEARS = 2     # 2025/26 to 2027/28

# code, name, legacy SCADA point, profile kind, firm MW (N-1 at pf 0.95), 2025/26 design-day own peak (MW),
# temperature slope b (MW per degree below TB at the peak half-hour), year-on-year level growth (MW), DFES %/yr
PRIMARIES = [
    dict(key="A", code="PS40617", name="Ashcombe Road", legacy="HALV.ASHCOMBE_RD.33-11.MW", kind="res",
         firm=23.0, d26=26.82, b=0.60, yoy=0.62, dfes=2.2),
    dict(key="B", code="PS40233", name="Tollbrook Lane", legacy="HALV.TOLLBROOK_LN.33-11.MW", kind="com",
         firm=26.0, d26=22.10, b=0.34, yoy=0.35, dfes=1.1),
    dict(key="C", code="PS41108", name="Charlecote Way", legacy="HALV.CHARLECOTE_WY.33-11.MW", kind="res",
         firm=22.5, d26=23.62, b=0.345, yoy=0.48, dfes=1.5),
    dict(key="D", code="PS40852", name="Dunmore Street", legacy="HALV.DUNMORE_ST.33-11.MW", kind="res",
         firm=21.0, d26=19.83, b=0.41, yoy=0.30, dfes=1.3),
    dict(key="E", code="PS40391", name="Ravenhurst Park", legacy="HALV.RAVENHURST_PK.33-11.MW", kind="mix",
         firm=17.5, d26=15.14, b=0.29, yoy=0.21, dfes=1.6),
    dict(key="F", code="PS41474", name="Fenwick Street", legacy="HALV.FENWICK_ST.33-11.MW", kind="res",
         firm=30.5, d26=33.61, b=0.62, yoy=0.71, dfes=1.8),
    dict(key="G", code="PS40975", name="Wexley Hill", legacy="HALV.WEXLEY_HL.33-11.MW", kind="com",
         firm=27.0, d26=22.43, b=0.37, yoy=0.33, dfes=1.2),
    dict(key="H", code="PS41236", name="Hartwell Common", legacy="HALV.HARTWELL_CMN.33-11.MW", kind="res",
         firm=17.8, d26=20.95, b=0.513, yoy=0.44, dfes=2.0),
    dict(key="I", code="PS40508", name="Kestwick Fields", legacy="HALV.KESTWICK_FLDS.33-11.MW", kind="mix",
         firm=19.5, d26=15.62, b=0.31, yoy=0.24, dfes=1.4),
]
BY = {p["key"]: p for p in PRIMARIES}

# Providers' own reduction per MW scheduled in the credited half-hours, by the event day's daily mean temperature.
PROVIDERS = {
    "Corvane": dict(legal="Corvane Flex Ltd", at0=0.533, slope=0.044),      # domestic heat pumps and batteries
    "Quillon": dict(legal="Quillon Energy Services Ltd", at0=0.600, slope=0.033),  # commercial demand response
}
# zone primary, provider, MW scheduled in 2024/25 and 2025/26, MW contracted for 2027/28, transfer share, partner
ZONES = [
    dict(key="A", provider="Corvane", mw={"2024/25": 5.0, "2025/26": 6.5}, mw28=9.5, sigma=0.060, partner="B",
         nop="NOP-1172"),
    dict(key="C", provider="Quillon", mw={"2024/25": 4.0, "2025/26": 4.5}, mw28=8.0, sigma=0.0, partner="D",
         nop="NOP-0948"),
    dict(key="F", provider="Quillon", mw={"2024/25": 5.5, "2025/26": 6.5}, mw28=14.0, sigma=0.046, partner="G",
         nop="NOP-1305"),
    dict(key="H", provider="Corvane", mw={"2024/25": 2.5, "2025/26": 3.0}, mw28=7.5, sigma=0.045, partner="I",
         nop="NOP-0761"),
]
ZBY = {z["key"]: z for z in ZONES}
SERVICE_START = {("A", "2024/25"): dt.date(2024, 11, 28), ("H", "2025/26"): dt.date(2025, 11, 10)}
# accepted connections energising before 1 November 2027, MW at the design condition, by primary
REGISTER_MW = {"A": 2.30, "B": 0.62, "C": 0.71, "D": 0.34, "E": 2.88, "F": 0.93, "G": 0.79, "H": 1.19, "I": 0.41}
RAMP = np.array([0.55, 0.86, 1.0, 1.0, 1.0, 1.0, 0.92])   # half-hours ending 16:30 ... 19:30 local


def last_sunday(year, month):
    d = dt.date(year, month + 1, 1) - dt.timedelta(days=1) if month < 12 else dt.date(year, 12, 31)
    while d.weekday() != 6:
        d -= dt.timedelta(days=1)
    return d


def uk_offset_hours(t_utc):
    """BST from 01:00 UTC on the last Sunday of March to 01:00 UTC on the last Sunday of October."""
    y = t_utc.year
    start = dt.datetime.combine(last_sunday(y, 3), dt.time(1, 0), UTC)
    end = dt.datetime.combine(last_sunday(y, 10), dt.time(1, 0), UTC)
    return 1 if start <= t_utc < end else 0


ANCHORS = {
    ("res", False): [(0.5, .48), (3, .42), (5.5, .44), (7, .62), (8, .70), (9.5, .64), (12.5, .62), (14.5, .64),
                     (15.5, .74), (16, .82), (16.5, .89), (17, .95), (17.5, .99), (18, 1.0), (18.5, .97), (19, .92),
                     (19.5, .85), (20, .77), (21, .69), (22, .61), (23, .54), (24, .49)],
    ("res", True): [(0.5, .50), (3, .43), (6, .43), (8, .55), (10, .68), (12.5, .66), (15, .67), (16, .76),
                    (17, .86), (17.5, .91), (18, .93), (18.5, .91), (19, .86), (20, .74), (22, .60), (24, .51)],
    ("com", False): [(0.5, .36), (5, .34), (7, .50), (8, .72), (9, .88), (10, .96), (11, .99), (12, 1.0), (13, .99),
                     (14, .97), (15, .93), (16, .86), (17, .78), (17.5, .74), (18, .69), (19, .60), (20, .52),
                     (22, .42), (24, .37)],
    ("com", True): [(0.5, .35), (6, .33), (9, .44), (12, .58), (14, .60), (16, .56), (18, .52), (20, .46),
                    (22, .40), (24, .36)],
    ("mix", False): [(0.5, .45), (3, .40), (7, .60), (8, .76), (10, .80), (12.5, .82), (15, .82), (15.5, .84),
                     (16, .88), (17, .96), (17.5, 1.0), (18, 1.0), (18.5, .97), (19, .92), (19.5, .86), (20, .79),
                     (22, .64), (24, .50)],
    ("mix", True): [(0.5, .46), (4, .41), (8, .56), (10, .70), (13, .72), (16, .74), (17.5, .84), (18, .85),
                    (19, .80), (20, .72), (22, .60), (24, .50)],
}


def profile(kind, weekend):
    """Shape of a day's demand by local half-hour (index 0 = the half-hour ending 00:30), weekday peak 1.0."""
    pts = ANCHORS[(kind, weekend)]
    x = np.array([p[0] for p in pts])
    y = np.array([p[1] for p in pts])
    h = (np.arange(48) + 1) * 0.5
    return np.interp(h, x, y)


def daily_temperatures(rng):
    """Daily mean temperature (the mean of the 24 GMT-day hourly readings) for each winter, AR(1) about a
    seasonal mean; each winter carries a cold spell reaching below the design condition."""
    out = {}
    for w, d0, d1 in WINTERS:
        days = [d0 + dt.timedelta(days=i) for i in range((d1 - d0).days + 1)]
        n = len(days)
        doy = np.array([(d - dt.date(d.year if d.month >= 7 else d.year - 1, 7, 1)).days for d in days])
        seas = 7.4 - 3.9 * np.cos(2 * np.pi * (doy - 205) / 365.0)   # ~8.8 C on 1 October, ~3.5 C in late January
        a = np.zeros(n)
        e = rng.normal(0, 1.85, n)
        for i in range(1, n):
            a[i] = 0.80 * a[i - 1] + e[i]
        t = seas + a
        # one or two cold spells per winter, as the record's coldest weeks
        k = {"2023/24": [(105, 7, -4.6)], "2024/25": [(98, 6, -6.2), (128, 4, -1.5)], "2025/26": [(96, 8, -5.3)]}[w]
        for start, length, low in k:
            for j in range(length):
                i = start + j
                if 0 <= i < n:
                    floor = low + 5.5 * (1 - math.sin(math.pi * (j + 0.5) / length)) + rng.normal(0, 0.4)
                    t[i] = min(t[i], floor)
        out[w] = (days, t)
    return out


def hourly_from_daily(rng, days, tday):
    """Hourly readings for each GMT day whose 24-reading mean is exactly the day's mean."""
    hrs = []
    for d, tm in zip(days, tday):
        prof = -2.2 * np.cos(2 * np.pi * (np.arange(24) - 14.5) / 24.0) + rng.normal(0, 0.35, 24)
        prof = prof - prof.mean()
        hrs.append(np.round(tm + prof, 1))
    return hrs


def build():
    rng = np.random.default_rng(SEED)
    temps = daily_temperatures(rng)
    hourly = {w: hourly_from_daily(rng, *temps[w]) for w, _, _ in WINTERS}
    # the daily mean the guideline uses is the mean of the shipped hourly readings (one decimal each)
    tday = {w: np.array([np.mean(h) for h in hourly[w]]) for w, _, _ in WINTERS}

    # half-hour grid in UTC
    stamps = {}
    for w, d0, d1 in WINTERS:
        t0 = dt.datetime.combine(d0, dt.time(0, 30), UTC)
        n = ((d1 - d0).days + 1) * 48
        stamps[w] = [t0 + dt.timedelta(minutes=30 * i) for i in range(n)]

    widx = {w: i for i, (w, _, _) in enumerate(WINTERS)}
    grid = {}
    for w, d0, d1 in WINTERS:
        hh = np.empty(len(stamps[w]), int)
        di = np.empty(len(stamps[w]), int)
        wk = np.empty(len(stamps[w]), bool)
        xm = np.empty(len(stamps[w]), bool)
        for i, t in enumerate(stamps[w]):
            tl = t + dt.timedelta(hours=uk_offset_hours(t)) - dt.timedelta(minutes=30)
            dloc = tl.date()
            di[i] = min(max((dloc - d0).days, 0), (d1 - d0).days)
            wk[i] = dloc.weekday() >= 5 or dloc in BANK_HOLIDAYS
            xm[i] = (dloc.month == 12 and dloc.day >= 24) or (dloc.month == 1 and dloc.day <= 2)
            hh[i] = tl.hour * 2 + tl.minute // 30
        grid[w] = (hh, di, wk, xm)
    own = {}
    for p in PRIMARIES:
        prng = np.random.default_rng(SEED + hash_key(p["key"]))
        a26 = p["d26"] - p["b"] * (TB - T_DESIGN)
        for w, d0, d1 in WINTERS:
            hh, di, wk, xm = grid[w]
            lev = a26 - p["yoy"] * (2 - widx[w])
            days, _ = temps[w]
            td = tday[w]
            day_eff = prng.normal(0, 0.006, len(days))
            lvl = (lev + p["b"] * np.maximum(0.0, TB - td[di])) * (1 + day_eff[di])
            lvl = np.where(xm & ~wk, lvl * 0.96, lvl)
            shape = np.where(wk | xm, PROF[(p["kind"], True)][hh], PROF[(p["kind"], False)][hh])
            vals = lvl * shape + prng.normal(0, 0.07 if p["firm"] > 20 else 0.05, len(hh))
            own[(p["key"], w)] = vals

    # flexibility events: scheduled day-ahead from the DNO's forecast, weekdays November to March, from 2024/25
    events = []
    erng = np.random.default_rng(SEED + 77)
    for w, d0, d1 in WINTERS[1:]:
        days, _ = temps[w]
        for di, d in enumerate(days):
            xmas = (d.month == 12 and d.day >= 24) or (d.month == 1 and d.day <= 2)
            if d.month in (10,) or d.weekday() >= 5 or d in BANK_HOLIDAYS or xmas:
                continue
            fc_err = erng.normal(0, 0.85)
            for z in ZONES:
                p = BY[z["key"]]
                a26 = p["d26"] - p["b"] * (TB - T_DESIGN)
                lev = a26 - p["yoy"] * (2 - widx[w])
                fc = lev + p["b"] * max(0.0, TB - (tday[w][di] + fc_err))
                if fc > 0.95 * p["firm"]:
                    events.append(dict(winter=w, day=d, di=di, zone=z["key"], provider=z["provider"],
                                       mw=z["mw"][w], T=float(tday[w][di])))
    # some scheduled events are cancelled on the morning (no reduction, no transfer); some re-issued at a reduced MW
    for k, ev in enumerate(events):
        u = erng.random()
        ev["status"] = "Cancelled" if u < 0.045 else "Completed"
        ev["revised_mw"] = None
        if ev["status"] == "Completed" and erng.random() < 0.07:
            ev["revised_mw"] = round(ev["mw"] * float(erng.choice([0.75, 0.8, 0.85])) * 2) / 2
        ev["eps"] = float(erng.normal(0, 0.045))

    # each zone's service ran from its contract start (Ashcombe Road's first on 28 November 2024, Hartwell Common's
    # 2025/26 contract on 10 November 2025) to the Friday before British Summer Time began; filtered after the draws,
    # so every other event keeps its own
    events = [e for e in events if e["day"] >= SERVICE_START.get((e["zone"], e["winter"]), e["day"])
              and not (e["day"].month == 3 and e["day"] >= last_sunday(e["day"].year, 3))]

    metered = {k: v.copy() for k, v in own.items()}
    relief = {}
    transfer = {}
    for ev in events:
        if ev["status"] != "Completed":
            continue
        w, d = ev["winter"], ev["day"]
        z = ZBY[ev["zone"]]
        prov = PROVIDERS[z["provider"]]
        sched = ev["revised_mw"] or ev["mw"]
        delta = prov["at0"] + prov["slope"] * ev["T"]
        idx = window_indices(stamps[w], d)
        r = delta * sched * RAMP * (1 + ev["eps"])
        metered[(z["key"], w)][idx] -= r
        relief[(ev["zone"], w, d)] = (idx, r, delta, sched)
        if z["sigma"] > 0:
            sec = z["sigma"] * own[(z["key"], w)][idx]
            metered[(z["key"], w)][idx] -= sec
            metered[(z["partner"], w)][idx] += sec
            transfer[(ev["zone"], w, d)] = (idx, sec)
    return dict(temps=temps, hourly=hourly, tday=tday, stamps=stamps, own=own, metered=metered,
                events=events, relief=relief, transfer=transfer)


def window_indices(stamps_w, day):
    """Indices of the half-hours ending 16:30 ... 19:30 local on day."""
    t_end0 = dt.datetime.combine(day, dt.time(16, 30))
    out = []
    for k in range(7):
        tl = t_end0 + dt.timedelta(minutes=30 * k)
        # local to UTC
        guess = tl.replace(tzinfo=UTC)
        off = uk_offset_hours(guess - dt.timedelta(hours=1))
        tu = guess - dt.timedelta(hours=off)
        out.append(int((tu - stamps_w[0]).total_seconds() // 1800))
    return np.array(out)


def hash_key(k):
    return {"A": 101, "B": 211, "C": 307, "D": 401, "E": 503, "F": 601, "G": 701, "H": 809, "I": 907}[k]


PROF = {(k, wk): profile(k, wk) for k in ("res", "com", "mix") for wk in (False, True)}


def design_truth():
    """The quantities the guideline's literal execution files, from the truth's own parameters."""
    out = {}
    for z in ZONES:
        p = BY[z["key"]]
        prov = PROVIDERS[z["provider"]]
        before = p["d26"] * (1 + p["dfes"] / 100.0) ** GROWTH_YEARS
        out[z["key"]] = dict(delivery=prov["at0"] + prov["slope"] * T_DESIGN, before_ex_register=before)
    return out


def tables(T=None):
    """The clean truth as the analyst's tables: demand (code, t_utc end, mw), events, weather (hourly)."""
    import pandas as pd
    T = T or build()
    rows = []
    for p in PRIMARIES:
        for w, _, _ in WINTERS:
            rows.append(pd.DataFrame({"code": p["code"], "t_utc": pd.to_datetime(T["stamps"][w], utc=True),
                                      "mw": T["metered"][(p["key"], w)]}))
    demand = pd.concat(rows, ignore_index=True)
    ev = pd.DataFrame([dict(zone=BY[e["zone"]]["code"], provider=e["provider"], date=e["day"],
                            scheduled_mw=(e["revised_mw"] or e["mw"]), status=e["status"]) for e in T["events"]])
    wrows = []
    for w, d0, d1 in WINTERS:
        days, _ = T["temps"][w]
        for d, hv in zip(days, T["hourly"][w]):
            for hr in range(24):
                wrows.append((dt.datetime.combine(d, dt.time(hr, 0), UTC), float(hv[hr])))
    weather = pd.DataFrame(wrows, columns=["t_utc", "temp_c"])
    weather["t_utc"] = pd.to_datetime(weather["t_utc"], utc=True)
    return dict(demand=demand, events=ev, weather=weather)
