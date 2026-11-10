"""task10 architecture 6: the clean truth of Wealdmoor Power Networks' Halverton zone, simulated as its process.

Nine 33/11 kV primaries, three winters (October to March, 2023/24 to 2025/26) of half-hourly demand driven by the
reference station's daily mean temperature. From November 2024 the DSO schedules flexibility day-ahead at four
constraint managed zones, sized to what its forecast shows is needed to hold the primary at 95 per cent of firm
capacity and never more than the megawatts contracted. A provider delivers what is scheduled while its enrolled
assets can: what they have available that evening is a share of the contracted (registered) megawatts that falls as
the day gets colder and varies from day to day, so a call above it delivers the available megawatts and no more.
After the service window the curtailed load comes back for an hour or two. The control room's ordinary 11 kV
switching (planned work, fault restoration) moves feeder sections between primaries and is logged. Nothing here is
written to the pack; pack.py writes what the systems record."""
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

# What a provider's enrolled assets have available in the evening peak, as a share of the megawatts contracted
# (their registered capacity), by the event day's daily mean temperature: the weather-dependent part of the
# portfolio holds back as it gets colder. cv is the day-to-day spread of that availability; reb the share of the
# megawatts delivered that comes back in each of the four half-hours after the window.
PROVIDERS = {
    "Corvane": dict(legal="Corvane Flex Ltd", a_hi=0.741, a_lo=0.094, t_mid=-2.2, w=4.2, cv=0.112,
                    reb=(0.335, 0.205, 0.115, 0.045)),      # domestic heat pumps and batteries
    "Quillon": dict(legal="Quillon Energy Services Ltd", a_hi=0.804, a_lo=0.222, t_mid=-3.0, w=4.6, cv=0.172,
                    reb=(0.285, 0.155, 0.065, 0.02)),       # commercial refrigeration, HVAC and process load
}
MW28 = {"A": 21.0, "C": 7.5, "F": 10.0, "H": 7.5}
# zone primary, provider, MW contracted in 2024/25 and 2025/26, MW contracted for 2027/28
ZONES = [
    dict(key="A", provider="Corvane", mw={"2023/24": 5.5, "2024/25": 6.5, "2025/26": 7.5}, mw28=MW28["A"], partner="B", nop="NOP-1172"),
    dict(key="C", provider="Quillon", mw={"2023/24": 2.5, "2024/25": 3.0, "2025/26": 4.0}, mw28=MW28["C"], partner="D", nop="NOP-0948"),
    dict(key="F", provider="Quillon", mw={"2023/24": 2.5, "2024/25": 3.5, "2025/26": 4.5}, mw28=MW28["F"], partner="G", nop="NOP-1305"),
    dict(key="H", provider="Corvane", mw={"2023/24": 2.0, "2024/25": 2.5, "2025/26": 3.0}, mw28=MW28["H"], partner="I", nop="NOP-0761"),
]
ZBY = {z["key"]: z for z in ZONES}
SERVICE_START = {("A", "2023/24"): dt.date(2023, 11, 27), ("C", "2023/24"): dt.date(2023, 11, 13), ("H", "2025/26"): dt.date(2025, 11, 10)}
# accepted connections energising before 1 November 2027, MW at the design condition, by primary
REGISTER_MW = {"A": 2.30, "B": 0.62, "C": 0.71, "D": 0.34, "E": 2.88, "F": 0.93, "G": 0.79, "H": 1.19, "I": 0.41}
RAMP = np.array([0.55, 0.86, 1.0, 1.0, 1.0, 1.0, 0.92])   # half-hours ending 16:30 ... 19:30 local
THRESHOLD = 0.92     # the DSO schedules when its forecast of the primary's peak exceeds this share of firm capacity
STEP_MW = 0.5        # schedules are issued in half megawatts
MIN_MW = 1.0         # the smallest schedule the service terms allow
NOPS = [("NOP-1172", "A", "B"), ("NOP-1088", "A", "D"), ("NOP-0948", "C", "D"), ("NOP-0815", "C", "E"),
        ("NOP-1305", "F", "G"), ("NOP-0761", "H", "I"), ("NOP-0693", "H", "E"),
        ("NOP-1260", "B", "G"), ("NOP-0877", "D", "E"), ("NOP-1351", "G", "I"), ("NOP-0722", "E", "I"),
        ("NOP-1214", "D", "F")]


def availability(provider, T):
    """Share of the contracted megawatts a provider's assets have available in the evening peak at daily mean T."""
    p = PROVIDERS[provider]
    return p["a_hi"] - (p["a_hi"] - p["a_lo"]) / (1.0 + math.exp((T - p["t_mid"]) / p["w"]))


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
                     (15.5, .72), (16, .785), (16.5, .885), (17, .95), (17.5, .99), (18, 1.0), (18.5, .97), (19, .92),
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
        k = {"2023/24": [(105, 7, -4.6), (72, 5, -2.9)],
             "2024/25": [(98, 6, -6.2), (128, 4, -1.5), (59, 6, -3.6), (141, 4, -2.4)],
             "2025/26": [(96, 8, -5.3), (64, 6, -4.1), (123, 5, -2.8)]}[w]
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

    # flexibility events: scheduled day-ahead from the DSO's forecast, working weekdays November to March, from
    # 2024/25: the megawatts the forecast shows are needed to hold the primary at 95 per cent of firm capacity,
    # in half megawatts, at least the service minimum and never more than the megawatts contracted
    events = []
    erng = np.random.default_rng(SEED + 77)
    for w, d0, d1 in WINTERS:
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
                need = fc - THRESHOLD * p["firm"]
                if need > 0:
                    mw = min(z["mw"][w], max(MIN_MW, math.ceil(need / STEP_MW) * STEP_MW))
                    events.append(dict(winter=w, day=d, di=di, zone=z["key"], provider=z["provider"],
                                       mw=mw, contract=z["mw"][w], T=float(tday[w][di])))
    # some schedules are cancelled on the morning (no reduction); some re-issued at fewer megawatts
    for k, ev in enumerate(events):
        u = erng.random()
        ev["status"] = "Cancelled" if u < 0.045 else "Completed"
        ev["revised_mw"] = None
        if ev["status"] == "Completed" and erng.random() < 0.07 and ev["mw"] >= 2.0:
            ev["revised_mw"] = max(MIN_MW, round(ev["mw"] * float(erng.choice([0.75, 0.8, 0.85])) * 2) / 2)
        ev["eps"] = float(erng.normal(0, 0.03))        # how closely the provider's dispatch tracks a schedule it can meet
        ev["nu"] = float(erng.normal(0, 1.0))          # that evening's availability, in its own spread
        ev["rb"] = [float(x) for x in erng.normal(0, 0.18, 4)]   # the evening's come-back, half-hour by half-hour

    # each zone's service ran from its contract start (Ashcombe Road's first on 28 November 2024, Hartwell Common's
    # 2025/26 contract on 10 November 2025) to the Friday before British Summer Time began; filtered after the draws,
    # so every other event keeps its own
    events = [e for e in events if e["day"] >= SERVICE_START.get((e["zone"], e["winter"]), e["day"])
              and not (e["day"].month == 3 and e["day"] >= last_sunday(e["day"].year, 3))]

    metered = {k: v.copy() for k, v in own.items()}
    relief = {}
    for ev in events:
        if ev["status"] != "Completed":
            continue
        w, d = ev["winter"], ev["day"]
        z = ZBY[ev["zone"]]
        prov = PROVIDERS[z["provider"]]
        sched = ev["revised_mw"] or ev["mw"]
        avail = availability(z["provider"], ev["T"]) * ev["contract"] * math.exp(prov["cv"] * ev["nu"] - 0.5 * prov["cv"] ** 2)
        delivered = min(sched * (1 + ev["eps"]), avail)
        ev["available"], ev["delivered"], ev["capped"] = avail, delivered, bool(avail < sched * (1 + ev["eps"]))
        idx = window_indices(stamps[w], d)
        r = delivered * RAMP
        metered[(z["key"], w)][idx] -= r
        post = idx[-1] + 1 + np.arange(4)
        back = delivered * np.array(prov["reb"]) * (1 + np.array(ev["rb"]))
        metered[(z["key"], w)][post] += back
        relief[(ev["zone"], w, d)] = (idx, r, delivered, sched, post, back)

    # the control room's 11 kV switching: a feeder section moved across a normally-open point for planned work or
    # fault restoration, from a quarter of a day to three days, logged at both operations
    srng = np.random.default_rng(SEED + 191)
    switching = []
    for w, d0, d1 in WINTERS:
        n = int(srng.integers(9, 13))
        for _ in range(n):
            nop, a, b = NOPS[int(srng.integers(0, len(NOPS)))]
            frm, to = (a, b) if srng.random() < 0.5 else (b, a)
            day = d0 + dt.timedelta(days=int(srng.integers(34, (d1 - d0).days - 3)))
            start = dt.datetime.combine(day, dt.time(int(srng.integers(7, 10)), int(srng.choice([0, 15, 30, 45]))), UTC)
            hours = float(srng.choice([4, 5, 6, 6.5, 7.5, 28, 33, 52], p=[.2, .2, .18, .15, .12, .07, .05, .03]))
            share = float(srng.uniform(0.035, 0.075))
            reason = str(srng.choice(["Planned: cable jointing", "Planned: switchgear maintenance", "Planned: RMU replacement",
                                      "Fault restoration", "Planned: tree cutting outage", "Fault restoration"]))
            switching.append(dict(winter=w, nop=nop, frm=frm, to=to, start=start, end=start + dt.timedelta(hours=hours),
                                  share=share, reason=reason))
    switching.sort(key=lambda s: s["start"])
    moved = {}
    for s in switching:
        w = s["winter"]
        st = stamps[w]
        i0 = int(math.ceil((s["start"] - st[0]).total_seconds() / 1800.0)) + 1
        i1 = int(math.floor((s["end"] - st[0]).total_seconds() / 1800.0)) + 1
        i0, i1 = max(i0, 0), min(i1, len(st))
        if i1 <= i0:
            s["mw_at_start"] = 0.0
            continue
        sec = s["share"] * own[(s["frm"], w)][i0:i1]
        metered[(s["frm"], w)][i0:i1] -= sec
        metered[(s["to"], w)][i0:i1] += sec
        s["mw_at_start"] = float(sec[0])
        moved[(s["nop"], s["start"])] = (i0, i1, sec)
    return dict(temps=temps, hourly=hourly, tday=tday, stamps=stamps, own=own, metered=metered,
                events=events, relief=relief, switching=switching, moved=moved)


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
        before = p["d26"] * (1 + p["dfes"] / 100.0) ** GROWTH_YEARS
        av = availability(z["provider"], T_DESIGN)
        out[z["key"]] = dict(available_share=av, delivered=av * z["mw28"], before_ex_register=before,
                             cv=PROVIDERS[z["provider"]]["cv"], reb=PROVIDERS[z["provider"]]["reb"])
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
    sw = pd.DataFrame([dict(nop=s["nop"], frm=BY[s["frm"]]["code"], to=BY[s["to"]]["code"], start=s["start"], end=s["end"],
                            mw=s["mw_at_start"]) for s in T["switching"]])
    wrows = []
    for w, d0, d1 in WINTERS:
        days, _ = T["temps"][w]
        for d, hv in zip(days, T["hourly"][w]):
            for hr in range(24):
                wrows.append((dt.datetime.combine(d, dt.time(hr, 0), UTC), float(hv[hr])))
    weather = pd.DataFrame(wrows, columns=["t_utc", "temp_c"])
    weather["t_utc"] = pd.to_datetime(weather["t_utc"], utc=True)
    return dict(demand=demand, events=ev, weather=weather, switching=sw)
