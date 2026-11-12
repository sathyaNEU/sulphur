"""task7 architecture 10: the world. Cedar Brake Electric Cooperative (Central Texas, ERCOT) runs a bring-your-own-thermostat
demand-response programme through six thermostat providers. Each summer (2024 to 2026) the co-op calls alert events on the
days its 4CP forecast flags, which come in heat waves, and a few randomised test events on single hot days for evaluation.
Members override when the house warms; a device that is offline at dispatch does nothing. Homes carry their own air-
conditioning load (size and age); a research sample of homes in the north has 15-minute meters. Everything decided later is
read off what this process wrote down."""
import datetime as dt

import numpy as np

SEED = 100710
YEARS = (2024, 2025, 2026)
RATE = 54.80                      # USD per kW of 4CP load a year, the co-op's 2026 transmission rate
STEP = 15
AMI_FROM, AMI_TO = 13 * 60, 21 * 60   # the research sample's export window, local time
PROVIDERS = ["Corvane", "Lumivale", "Ardena", "Ondera", "Kitebrook", "Pinecrest Home"]
# each provider's event as its platform runs it (minutes after midnight, local): start, end, pre-cool minutes, setback F,
# base override hazard per 15 minutes; its 2027 quote (USD per enrolled device for the summer) and planned enrolments
PROG = {
    "Corvane":        dict(s=960, e=1140, pre=60, d=3, lam=0.0060, price=29.00, south=0.45, new27={"app": 260, "retail": 80}),
    "Lumivale":       dict(s=900, e=1140, pre=0,  d=4, lam=0.0100, price=23.60, south=0.45, new27={"app": 150, "retail": 60}),
    "Ardena":         dict(s=990, e=1110, pre=30, d=3, lam=0.0060, price=41.00, south=0.45, new27={}),
    "Ondera":         dict(s=900, e=1020, pre=0,  d=3, lam=0.0070, price=26.00, south=0.50, new27={"app": 100}),
    "Kitebrook":      dict(s=960, e=1140, pre=30, d=2, lam=0.0060, price=33.00, south=0.80, new27={"app": 300}),
    "Pinecrest Home": dict(s=960, e=1140, pre=0,  d=2, lam=0.0060, price=20.80, south=0.45, new27={"retail": 1800}),
}
# enrolments by provider, year and channel (devices that joined that year), 2021 to 2026
JOINS = {
    "Corvane":        {"app": [220, 330, 360, 330, 300, 260], "mail": [180, 200, 90, 0, 0, 0], "retail": [0, 0, 0, 0, 50, 70]},
    "Lumivale":       {"app": [240, 360, 420, 400, 380, 300], "mail": [60, 80, 40, 0, 0, 0], "retail": [0, 0, 0, 0, 40, 60]},
    "Ardena":         {"app": [120, 160, 180, 170, 160, 120], "mail": [260, 300, 200, 0, 0, 0]},
    "Ondera":         {"app": [140, 170, 190, 180, 170, 160], "mail": [160, 220, 200, 0, 0, 0]},
    "Kitebrook":      {"app": [180, 240, 260, 260, 240, 220], "mail": [70, 90, 60, 0, 0, 0]},
    "Pinecrest Home": {"app": [150, 220, 240, 230, 220, 200], "retail": [0, 0, 0, 0, 60, 90]},
}
CHANNELS = {"app": dict(m=1.0, off=0.05, attr=0.08), "mail": dict(m=0.9, off=0.04, attr=0.06),
            "retail": dict(m=4.5, off=0.42, attr=0.22)}
TENURE = 0.10                     # override hazard per year enrolled
STREAK = [1.0, 1.3, 1.6, 1.9, 2.2, 2.4]   # by the event's place in a run of consecutive event days
# the 4CP intervals ERCOT will publish (start of the 15-minute interval, local), by year and month
CP_TIME = {2024: [1005, 1020, 1035, 1005], 2025: [1020, 1035, 1050, 1020], 2026: [1035, 1050, 1065, 1035]}


def ac_scale(sqft, year_built):
    """a home's air-conditioning load at full afternoon heat, kW: size and envelope (older homes leak more)"""
    age = np.clip((2005 - year_built) / 40.0, 0, 1.2)
    return 0.0014 * sqft ** 0.95 * (1 + 0.65 * age)


def duty(T):
    return np.clip((T - 75.0) / 28.0, 0, 1.25)


class World:
    pass


def weather(rng, w):
    """daily highs and lows and a 15-minute temperature for every summer day (1 June to 30 September), with a heat wave
    built each month around the day ERCOT will peak"""
    days, tmax, tmin = [], [], []
    clim = {6: 94.0, 7: 97.0, 8: 98.5, 9: 93.5}
    for y in YEARS:
        d = dt.date(y, 6, 1)
        anom = 0.0
        while d <= dt.date(y, 9, 30):
            anom = 0.75 * anom + rng.normal(0, 1.6)
            days.append(d)
            tmax.append(clim[d.month] + anom)
            tmin.append(clim[d.month] - 21 + 0.4 * anom + rng.normal(0, 1.0))
            d += dt.timedelta(days=1)
    tmax, tmin = np.array(tmax), np.array(tmin)
    w.days = days
    w.di = {d: i for i, d in enumerate(days)}
    # each month's heat wave: four to six weekdays, the hottest on its third to fifth day, which ERCOT will peak on
    w.cp_days, w.waves = [], []
    for y in YEARS:
        for k, m in enumerate((6, 7, 8, 9)):
            first = dt.date(y, m, 1)
            starts = [first + dt.timedelta(days=j) for j in range(5, 21) if (first + dt.timedelta(days=j)).weekday() == 0]
            start = starts[int(rng.integers(0, len(starts)))]
            n = int(rng.integers(4, 6))
            peak = int(rng.integers(2, n))              # the third to the fifth weekday
            wave = [start + dt.timedelta(days=j) for j in range(n)]
            base = {6: 102.5, 7: 104.0, 8: 105.0, 9: 101.5}[m]
            for j, dd in enumerate(wave):
                i = w.di[dd]
                tmax[i] = base + 1.1 * j - (0.9 * (j - peak) if j > peak else 0) + rng.normal(0, 0.5)
                tmin[i] = tmax[i] - 22 + rng.normal(0, 0.8)
            ip = w.di[wave[peak]]
            tmax[ip] = max(tmax[[w.di[x] for x in wave]]) + 0.8 + abs(rng.normal(0, 0.3))
            # the weekend either side cools off a little
            for dd in (start - dt.timedelta(days=1), start - dt.timedelta(days=2)):
                if dd in w.di:
                    tmax[w.di[dd]] = min(tmax[w.di[dd]], base - 3.5)
            w.cp_days.append(wave[peak])
            w.waves.append(wave)
    # no other day of the month beats ERCOT's peak day
    for y in YEARS:
        for k, m in enumerate((6, 7, 8, 9)):
            cp = w.cp_days[YEARS.index(y) * 4 + k]
            top = tmax[w.di[cp]]
            for i, d in enumerate(days):
                if d.year == y and d.month == m and d != cp and tmax[i] >= top - 0.4:
                    tmax[i] = top - 0.4 - abs(rng.normal(0, 0.3))
    # statewide heat (what ERCOT's load and the 4CP forecast follow): the local high plus weather of its own elsewhere,
    # the heat waves statewide
    state = tmax + np.array([rng.normal(0, 2.4) for _ in tmax])
    for wave in w.waves:
        for dd in wave:
            state[w.di[dd]] = max(state[w.di[dd]], tmax[w.di[dd]] + 0.5)
    # a few dry, locally hot days that the rest of the state does not share
    for y in YEARS:
        cand = [i for i, d in enumerate(days) if d.year == y and d.weekday() < 5 and 94 <= tmax[i] <= 101
                and not any(d in wv for wv in w.waves)]
        for i in rng.choice(cand, 5, replace=False):
            tmax[i] = 102.5 + 3.5 * rng.random()
            tmin[i] = tmax[i] - 23 + rng.normal(0, 0.8)
            state[i] = tmax[i] - 5.0 - 2.0 * rng.random()
    w.tmax, w.tmin, w.state = tmax, tmin, state
    w.cp_time = {cp: CP_TIME[cp.year][cp.month - 6] for cp in w.cp_days}


def temp_at(w, i, minute):
    """the outdoor temperature at a minute of day i: the low at 6:00, the high at 16:45, an evening fall"""
    lo, hi = w.tmin[i], w.tmax[i]
    h = minute / 60.0
    if h < 6:
        return lo + (hi - lo) * 0.25 * (6 - h) / 6
    if h <= 16.75:
        return lo + (hi - lo) * np.sin(np.pi / 2 * (h - 6) / 10.75)
    return hi - (hi - lo) * 0.75 * (h - 16.75) / 7.25


def calendar(rng, w):
    """alert events on the days the co-op's 4CP forecast flags (weekdays with a forecast high of 101F or more; the
    forecast misses by a degree or two), and eight randomised test events a summer on single hot weekdays"""
    w.events = []
    eid = 0
    for y in YEARS:
        ydays = [d for d in w.days if d.year == y]
        alerts = []
        for d in ydays:
            if d.weekday() >= 5:
                continue
            fc = w.state[w.di[d]] + rng.normal(0, 1.1)
            if fc >= 102.0:
                alerts.append(d)
        # one of ERCOT's peak days in 2025 came in under the forecast
        miss = w.cp_days[YEARS.index(2025) * 4 + 3]
        if y == 2025 and miss in alerts:
            alerts.remove(miss)
        for cp in w.cp_days:
            if cp.year == y and cp != miss and cp not in alerts:
                alerts.append(cp)
        alerts = sorted(alerts)
        aset = set(alerts)
        cand = [d for d in ydays if d.weekday() < 5 and d not in aset and (d - dt.timedelta(days=1)) not in aset
                and (d + dt.timedelta(days=1)) not in aset and 95.0 <= w.tmax[w.di[d]] <= 107.0]
        # the M&V plan spreads its test events over the summer's heat: about a third on the hottest quiet days
        hot = [d for d in cand if w.tmax[w.di[d]] >= 101.5]
        mild = [d for d in cand if w.tmax[w.di[d]] < 101.5]
        rng.shuffle(hot)
        rng.shuffle(mild)
        tests = []
        for pool, want in ((hot, 3), (mild, 8)):
            for d in pool:
                if len(tests) >= want:
                    break
                if all(abs((d - t).days) >= 5 for t in tests):
                    tests.append(d)
        for d in sorted(alerts + tests):
            eid += 1
            kind = "alert" if d in aset else "test"
            run = 0
            if kind == "alert":
                k = 1
                while (d - dt.timedelta(days=k)) in aset:
                    run += 1
                    k += 1
            w.events.append(dict(id=eid, date=d, kind=kind, run=min(run, 5), year=y))
    w.ev_by_date = {e["date"]: e for e in w.events}


def homes(rng, w):
    """the co-op's residential members and the county's residential parcels: size, year built, stories, north or south"""
    n_parcel, n_member = 52000, 44000
    south = rng.random(n_parcel) < 0.55
    yb = np.where(south, rng.normal(1979, 15, n_parcel), rng.normal(2003, 11, n_parcel))
    yb = np.clip(np.round(yb), 1948, 2025).astype(int)
    sqft = np.where(south, rng.lognormal(np.log(1750), 0.33, n_parcel), rng.lognormal(np.log(2150), 0.28, n_parcel))
    sqft = np.clip(np.round(sqft / 10) * 10, 640, 6400).astype(int)
    stories = np.where(rng.random(n_parcel) < np.where(south, 0.12, 0.45), 2, 1)
    w.parcel = dict(south=south, yb=yb, sqft=sqft, stories=stories)
    w.member = np.sort(rng.choice(n_parcel, n_member, replace=False))     # parcels the co-op serves
    w.home_c = ac_scale(sqft, yb)


def devices(rng, w):
    """every device ever enrolled, 2021 to 2026, and the homes they sit in: each provider's members by north and south,
    the channel they came through, when they joined and left, and how readily they override"""
    P = w.parcel
    members = w.member
    south_m = members[P["south"][members]]
    north_m = members[~P["south"][members]]
    # bigger, older homes in the south for Kitebrook's dealers
    big_old = south_m[np.argsort(-(w.home_c[south_m] + rng.normal(0, 0.25, len(south_m))))]
    used = set()
    rows = []
    did = 0
    for p in PROVIDERS:
        q = PROG[p]
        for ch, by_year in JOINS[p].items():
            for k, n in enumerate(by_year):
                year = 2021 + k
                for _ in range(n):
                    in_south = rng.random() < q["south"]
                    if p == "Kitebrook" and in_south:
                        pool = big_old[: len(big_old) // 5]
                    else:
                        pool = south_m if in_south else north_m
                    for _try in range(50):
                        h = int(pool[rng.integers(0, len(pool))])
                        if h not in used:
                            break
                    used.add(h)
                    day = dt.date(year, 1, 1) + dt.timedelta(days=int(rng.integers(0, 365 if year < 2026 else 140)))
                    if year >= 2024 and day.month in (6, 7, 8):
                        day = dt.date(year, 5, int(rng.integers(1, 29)))
                    did += 1
                    attr = CHANNELS[ch]["attr"]
                    life = rng.exponential(1.0 / attr) if attr > 0 else 99
                    left = day + dt.timedelta(days=int(life * 365))
                    if left > dt.date(2026, 10, 30):
                        left = None
                    eng = float(rng.lognormal(0, 0.35))
                    rows.append(dict(i=did, p=p, ch=ch, home=h, joined=day, left=left, eng=eng,
                                     off=float(np.clip(CHANNELS[ch]["off"] * rng.lognormal(0, 0.4), 0, 0.9))))
    w.dev = rows
    for r in rows:
        r["north"] = not bool(P["south"][r["home"]])


def active(w, r, d):
    return r["joined"] <= d and (r["left"] is None or r["left"] > d)


def tenure(r, d):
    return max(0.0, (d - r["joined"]).days / 365.25)


def event_outcomes(rng, w):
    """for every device on every event it was due to get: called or held out (test events), offline at dispatch, and the
    minute it was overridden, if it was"""
    w.out = {}
    for e in w.events:
        i = w.di[e["date"]]
        for r in w.dev:
            if not active(w, r, e["date"]):
                continue
            q = PROG[r["p"]]
            called = True if e["kind"] == "alert" else bool(rng.random() < 0.5)
            offline = bool(rng.random() < r["off"])
            ov = None
            if called and not offline:
                dur = q["e"] - q["s"]
                ks = np.arange(0, dur, STEP)
                T = np.array([temp_at(w, i, q["s"] + k + STEP / 2) for k in ks])
                tin = q["d"] * (1 - np.exp(-(ks + STEP) / 45.0)) + 0.12 * (T - 100)
                lam = (q["lam"] * np.exp(0.85 * (tin - 2.0)) * STREAK[e["run"]] * CHANNELS[r["ch"]]["m"]
                       * (1 + TENURE * tenure(r, e["date"])) * r["eng"])
                hit = rng.random(len(ks)) < 1 - np.exp(-lam)
                if hit.any():
                    k = int(np.argmax(hit))
                    ov = q["s"] + int(ks[k]) + int(rng.integers(0, STEP))
            w.out[(e["id"], r["i"])] = (called, offline, ov)


def change(w, r, e, minute, out):
    """the device's change to its home's load (kW) at a minute of the event day against no event: pre-cool, the coast and
    the partial shed until an override, the snapback after the window if it ran to the end"""
    called, offline, ov = out
    if not called or offline:
        return 0.0
    q = PROG[r["p"]]
    i = w.di[e["date"]]
    T = temp_at(w, i, minute)
    c = w.home_c[r["home"]]
    L = c * duty(T)
    cap = c * 1.25 * 1.08
    if minute < q["s"]:
        return 0.35 * (cap - L) if (q["pre"] and minute >= q["s"] - q["pre"]) else 0.0
    if minute < q["e"]:
        if ov is not None and minute >= ov:
            return 0.0
        m = minute - q["s"]
        return -L if m < 15 + 5 * q["d"] else -L * 0.11 * q["d"]
    if ov is not None:
        return 0.0
    tau = 15 + 6 * q["d"] * (q["e"] - q["s"]) / 60.0
    return 0.85 * (cap - L) if minute - q["e"] < tau else 0.0


def ami(rng, w):
    """the research sample: programme homes in the north with the 15-minute meters fitted in 2023, enrolled before June
    2024; their load every 15 minutes, 13:00 to 21:00, on each event day and on eight hot weekdays a summer without one"""
    fitted = rng.random(len(w.parcel["south"])) < 0.45      # the two north substations that got 15-minute meters
    sample = sorted({r["home"] for r in w.dev if r["north"] and fitted[r["home"]] and r["joined"] < dt.date(2024, 6, 1)})
    w.ami_homes = sample
    dev_of = {}
    for r in w.dev:
        if r["home"] in set(sample):
            dev_of.setdefault(r["home"], []).append(r)
    w.dev_of = dev_of
    days = []
    for y in YEARS:
        ev = [e["date"] for e in w.events if e["year"] == y]
        quiet = [d for d in w.days if d.year == y and d.weekday() < 5 and d not in w.ev_by_date
                 and w.tmax[w.di[d]] >= 96]
        rng.shuffle(quiet)
        days += ev + sorted(quiet[:8])
    w.ami_days = sorted(days)
    mins = np.arange(AMI_FROM, AMI_TO, STEP)
    w.ami_load = {}
    for h in sample:
        c = w.home_c[h]
        base_h = 0.9 + 0.35 * rng.random()
        for d in w.ami_days:
            i = w.di[d]
            T = np.array([temp_at(w, i, m + STEP / 2) for m in mins])
            load = base_h + 0.25 * np.sin((mins - 780) / 480 * np.pi) + c * duty(T) * rng.lognormal(0, 0.06)
            e = w.ev_by_date.get(d)
            if e is not None:
                for r in dev_of.get(h, []):
                    if not active(w, r, d):
                        continue
                    out = w.out.get((e["id"], r["i"]))
                    if out is None:
                        continue
                    load = load + np.array([change(w, r, e, m + STEP / 2, out) for m in mins])
            load = load + rng.normal(0, 0.15, len(mins))
            w.ami_load[(h, d)] = np.maximum(load, 0.05) * STEP / 60.0      # kWh in each 15 minutes


def build():
    rng = np.random.default_rng(SEED)
    w = World()
    weather(rng, w)
    calendar(rng, w)
    homes(rng, w)
    devices(rng, w)
    event_outcomes(rng, w)
    ami(rng, w)
    return w
