"""The clean truth: Vehkasalon Liikenne's Niittylä depot simulated day by day from January 2024 to October 2026.

Blocks (a bus's day of trips on one or two lines) with their kilometres, hours, climb and a difficulty the
timetable does not record (stops, dwell with the doors open, passenger load, the drivers who take them); a fleet
of diesel buses rotating over the blocks under the dispatcher's hand, each burning fuel by the block's physics and
the day's cold, filled at the depot pump when low; six battery-electric buses from March and June 2025 on the nine
blocks the planner picked from the 2024 fuel figures, with electric heating up to their small heat pump's capacity
and a fuel-fired cabin heater below that; the depot chargers each night; the batteries fading fastest in their
first months. Nothing here is placed for a result: every figure the task needs falls out of this process."""
import datetime as dt
import math

import numpy as np

import params as P

FI_HOLIDAYS = {dt.date(2024, 1, 1), dt.date(2024, 1, 6), dt.date(2024, 3, 29), dt.date(2024, 4, 1), dt.date(2024, 5, 1),
               dt.date(2024, 5, 9), dt.date(2024, 6, 21), dt.date(2024, 6, 22), dt.date(2024, 11, 2), dt.date(2024, 12, 6),
               dt.date(2024, 12, 24), dt.date(2024, 12, 25), dt.date(2024, 12, 26),
               dt.date(2025, 1, 1), dt.date(2025, 1, 6), dt.date(2025, 4, 18), dt.date(2025, 4, 21), dt.date(2025, 5, 1),
               dt.date(2025, 5, 29), dt.date(2025, 6, 20), dt.date(2025, 6, 21), dt.date(2025, 11, 1), dt.date(2025, 12, 6),
               dt.date(2025, 12, 24), dt.date(2025, 12, 25), dt.date(2025, 12, 26),
               dt.date(2026, 1, 1), dt.date(2026, 1, 6), dt.date(2026, 4, 3), dt.date(2026, 4, 6), dt.date(2026, 5, 1),
               dt.date(2026, 5, 14), dt.date(2026, 6, 19), dt.date(2026, 6, 20)}


def daytype(d):
    if d in FI_HOLIDAYS or d.weekday() == 6:
        return "S"
    return "L" if d.weekday() == 5 else "M"


def daterange(a, b):
    d = a
    while d <= b:
        yield d
        d += dt.timedelta(days=1)


# ----------------------------------------------------------------------------------------------- weather
def temperatures(rng):
    """Daily mean temperature at two stations in the town, 2016 to October 2026: a lake-district climate with
    persistence, the airport station with a three-week outage in April 2023."""
    days = list(daterange(P.TEMP_START, P.END))
    n = len(days)
    doy = np.array([d.timetuple().tm_yday for d in days])
    clim = 4.2 - 13.0 * np.cos(2 * math.pi * (doy - 20) / 365.25)
    anom = np.zeros(n)
    e = rng.normal(0, 2.4, n)
    for i in range(1, n):
        anom[i] = 0.80 * anom[i - 1] + e[i]
    winter = np.where(np.cos(2 * math.pi * (doy - 20) / 365.25) > 0.3, 1.6, 1.0)
    t_air = clim + anom * winter + rng.normal(0, 0.5, n)
    t_city = t_air + 0.9 + rng.normal(0, 0.45, n)
    out = {}
    gap = (dt.date(2023, 4, 2), dt.date(2023, 4, 19))
    for i, d in enumerate(days):
        ta = None if gap[0] <= d <= gap[1] else round(float(t_air[i]), 1)
        out[d] = {"airport": ta, "city": round(float(t_city[i]), 1), "truth": float(t_air[i])}
    return out


# ----------------------------------------------------------------------------------------------- blocks
LINES_URBAN = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
LINES_SUBURB = [14, 15, 16, 17, 18, 19, 21, 22]
LINES_REGION = [31, 32, 33, 34, 35, 36, 37, 38]
ZONE = {"urban": 1, "suburban": 2, "regional": 3}


def make_blocks(rng):
    """48 weekday blocks, 28 Saturday blocks, 20 Sunday blocks, each with the timetable's attributes and the
    difficulty the timetable does not carry."""
    blocks = []

    def one(code, old, dtype, kind, i):
        if kind == "urban":
            km = rng.uniform(112, 172)
            span = rng.uniform(9.6, 14.2)
            d = rng.uniform(0.45, 1.0)
            climb = rng.uniform(2.5, 7.0)
            lines = sorted(rng.choice(LINES_URBAN, size=rng.choice([1, 2]), replace=False).tolist())
        elif kind == "suburban":
            km = rng.uniform(165, 235)
            span = rng.uniform(9.0, 13.8)
            d = rng.uniform(0.28, 0.66)
            climb = rng.uniform(3.0, 9.0)
            lines = sorted(rng.choice(LINES_SUBURB, size=rng.choice([1, 2]), replace=False).tolist())
        else:
            km = rng.uniform(205, 312)
            span = rng.uniform(8.6, 14.0)
            d = rng.uniform(0.04, 0.34)
            climb = rng.uniform(4.0, 12.0)
            lines = sorted(rng.choice(LINES_REGION, size=rng.choice([1, 2]), replace=False).tolist())
        if dtype != "M":
            d = max(0.02, d - rng.uniform(0.08, 0.22))
            km *= rng.uniform(0.85, 1.0)
        # the span sets the speed; the difficulty slows the block a little on top (stops and dwell)
        span = span * (1 + 0.04 * (d - 0.4))
        dep = int(rng.uniform(4 * 60 + 40, 7 * 60 + 35))
        if rng.uniform() < 0.18 and span < 11:
            dep = int(rng.uniform(11 * 60, 14 * 60 + 30))          # an afternoon-and-evening block
        ret = dep + int(span * 60)
        if ret > 23 * 60 + 45:
            ret = 23 * 60 + 45
            span = (ret - dep) / 60.0
        km2 = km * rng.uniform(0.975, 1.035)   # the autumn 2025 timetable moved a few kilometres on most blocks
        blocks.append({"code": code, "old_code": old, "daytype": dtype, "kind": kind, "zone": ZONE[kind],
                       "lines": lines, "km_old": round(km, 1), "km": round(km2, 1), "hours": round(span, 2),
                       "dep": dep, "ret": ret, "climb": round(climb, 1), "d": round(d, 3),
                       "trips": int(round(km2 / rng.uniform(9, 16)))})

    kinds_m = ["urban"] * 18 + ["suburban"] * 16 + ["regional"] * 14
    rng.shuffle(kinds_m)
    for i, k in enumerate(kinds_m):
        one("M%03d" % (101 + i), "%d" % (101 + i), "M", k, i)
    kinds_l = ["urban"] * 11 + ["suburban"] * 10 + ["regional"] * 7
    rng.shuffle(kinds_l)
    for i, k in enumerate(kinds_l):
        one("L%03d" % (201 + i), "%d" % (201 + i), "L", k, i)
    kinds_s = ["urban"] * 8 + ["suburban"] * 7 + ["regional"] * 5
    rng.shuffle(kinds_s)
    for i, k in enumerate(kinds_s):
        one("S%03d" % (301 + i), "%d" % (301 + i), "S", k, i)
    # the timetable's own kilometres are drawn; a weekday block whose design-day energy would sit within 9 kWh of the
    # standard's limit is redrawn a few kilometres away from it (the world is drawn, never trimmed to a result: this
    # keeps every verdict clear of the limit by more than the honest family's spread, which the checks assert)
    lim = P.SHARE * P.E_USABLE_2027 * (1 - fade(365))
    for b in blocks:
        if b["daytype"] != "M":
            continue
        for _ in range(12):
            e = design_energy(b)
            if abs(e - lim) >= 26.0:
                break
            f = 1.035 if e >= lim else 0.965
            b["km"] = round(b["km"] * f, 1)
            b["km_old"] = round(b["km_old"] * f, 1)
            b["trips"] = max(6, int(round(b["trips"] * f)))
    # the city's electrification priority over the weekday blocks: centre lines first, then suburban, then regional,
    # with the planner's own ordering inside each group (not by any energy figure)
    weekday = [b for b in blocks if b["daytype"] == "M"]
    prng = np.random.default_rng(P.PRIORITY_SEED)
    order = sorted(weekday, key=lambda b: (b["zone"], prng.uniform()))
    for p, b in enumerate(order, 1):
        b["priority"] = p
    return blocks


# ----------------------------------------------------------------------------------------------- physics
def cop(t):
    """the pilot buses' heat pump: 2.4 at +10 and above, falling to 1.0 at -10 and below"""
    return float(np.clip(1.0 + 1.4 * (t - P.HP_FLOOR_T) / 20.0, 1.0, 2.4))


def heat_demand(t):
    return max(0.0, P.UA * (P.T_IN - t))


def pilot_heating(t):
    """(electric kW drawn from the battery, thermal kW supplied by the fuel heater) on a pilot bus at ambient t"""
    d = heat_demand(t)
    el_th = min(d, P.P_CAP_PILOT)
    fuel_th = max(0.0, d - P.P_CAP_PILOT) if t < P.FUEL_HEATER_ON else 0.0
    if t >= P.FUEL_HEATER_ON:
        el_th = d        # above the heater's enable point the electric system carries the whole (small) demand
    return el_th / cop(t), fuel_th


def new_bus_heating(t):
    """the 2027 model: all-electric heating, the heat pump to -10 C and resistive boosters below it"""
    return heat_demand(t) / cop(t)


def diesel_heating_l_per_h(t):
    """the diesel buses' fuel-fired cabin heater runs when the engine's waste heat does not cover the demand"""
    d = max(0.0, P.UA_DIESEL * (P.T_IN - t))
    return max(0.0, d - P.ENGINE_HEAT) / (P.FUEL_KWH_PER_L * P.BURNER_EFF)


def traction_kwh_per_km(b):
    return P.E0 + P.E_CLIMB * b["climb"] + P.E_DIFF * b["d"]


def diesel_l_per_100km(b):
    return P.R0 + P.R_CLIMB * b["climb"] + P.R_DIFF * b["d"]


def fade(age_days):
    """share of usable capacity permanently lost by an age in service: fast in the first months, then steady"""
    m = age_days / 30.4375
    return 0.030 * (1 - math.exp(-m / 4.0)) + 0.0012 * m


def cold_capacity(t):
    """reversible: the usable capacity the battery system shows on a cold day (small: the thermal management keeps the
    pack near its working temperature)"""
    return 1.0 - 0.0004 * max(0.0, 10.0 - t)


def conditioning_kw(t_night):
    """what a plugged-in bus takes through its charger beside the recharge, while the charger is released: the 24 V
    system, the BMS and the outlet's standby, and the traction battery held at its charging temperature on a cold night"""
    return P.COND_BASE + P.COND_SLOPE * max(0.0, P.COND_T0 - t_night)


def night_temp(temps, d):
    """the night after day d: between the evening's daily mean and the next morning's"""
    nxt = temps.get(d + dt.timedelta(days=1), temps[d])
    return 0.5 * (temps[d]["truth"] + nxt["truth"])


def released(a, b):
    """minutes of [a, b] (minutes from the evening's midnight) inside the night period, when the relay releases the chargers"""
    return max(0, min(b, P.NIGHT_TO + 1440) - max(a, P.NIGHT_FROM))


# ----------------------------------------------------------------------------------------------- fleet
MODELS = ["Volvo 8900LE", "Scania Citywide LE", "VDL Citea LLE"]


def make_fleet(rng):
    buses = []
    letters = "ABCDEFGHJKLMNPRSTUVXYZ"
    used = set()

    def reg():
        while True:
            r = "%s%s%s-%03d" % (rng.choice(list(letters)), rng.choice(list(letters)), rng.choice(list(letters)),
                                 rng.integers(100, 999))
            if r not in used:
                used.add(r)
                return r

    for i in range(54):
        fn = 1101 + i
        model = MODELS[0] if i < 24 else (MODELS[1] if i < 44 else MODELS[2])
        year = int(rng.choice([2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021], p=[.06, .1, .14, .16, .16, .14, .14, .10]))
        buses.append({"fleet_no": fn, "reg": reg(), "make_model": model, "drive": "diesel", "year": year,
                      "length_m": 12.0 if model != "VDL Citea LLE" else 12.9, "seats": int(rng.integers(37, 46)),
                      "tank_l": P.TANK_L[model], "heater": "Webasto Thermo 300 (fuel-fired, 30 kW)",
                      "eff": float(rng.normal(1.0, 0.010)), "in_service_from": dt.date(year, int(rng.integers(3, 11)), 1),
                      "retired": None, "battery_kwh": None})
    # six retired in the summer after the second electric batch (the oldest)
    oldest = sorted([b for b in buses], key=lambda b: (b["year"], b["fleet_no"]))[:6]
    for b in oldest:
        b["retired"] = dt.date(2025, 6, 30)
    for fn, since in P.EBUS_BATCH.items():
        buses.append({"fleet_no": fn, "reg": reg(), "make_model": "%s %s" % (P.EMAKE, P.EMODEL), "drive": "electric",
                      "year": 2025, "length_m": 12.2, "seats": 39, "tank_l": None,
                      "heater": "Eberspächer Hydronic L-II 35 kW fuel-fired (HVO, 3.9 l/h at full output, 30 l tank); heat pump 8 kW thermal",
                      "eff": float(rng.normal(1.0, 0.015)), "in_service_from": since, "retired": None,
                      "battery_kwh": P.E_USABLE_PILOT})
    return buses


def make_cards(rng, buses):
    """one fuel card per vehicle, eight reissued during the period, three spare cards held by the night staff"""
    cards = []
    n = 0

    def no():
        nonlocal n
        n += 1
        return "7054 %04d %04d" % (int(rng.integers(1000, 9999)), 2100 + n * 7 + int(rng.integers(0, 6)))

    reissue = set(rng.choice([b["fleet_no"] for b in buses if b["drive"] == "diesel"], 8, replace=False).tolist())
    for b in buses:
        start = max(P.START - dt.timedelta(days=400), b["in_service_from"] - dt.timedelta(days=3))
        if b["fleet_no"] in reissue:
            cut = P.START + dt.timedelta(days=int(rng.integers(120, 900)))
            cards.append({"card": no(), "fleet_no": b["fleet_no"], "valid_from": start, "valid_to": cut, "kind": "vehicle"})
            cards.append({"card": no(), "fleet_no": b["fleet_no"], "valid_from": cut + dt.timedelta(days=1), "valid_to": None,
                          "kind": "vehicle"})
        else:
            cards.append({"card": no(), "fleet_no": b["fleet_no"], "valid_from": start, "valid_to": None, "kind": "vehicle"})
    for k in range(3):
        cards.append({"card": no(), "fleet_no": None, "valid_from": dt.date(2022, 5, 2), "valid_to": None, "kind": "spare %d" % (k + 1)})
    return cards


def card_for(cards, fleet_no, d):
    for c in cards:
        if c["fleet_no"] == fleet_no and c["valid_from"] <= d and (c["valid_to"] is None or d <= c["valid_to"]):
            return c["card"]
    return None


# ----------------------------------------------------------------------------------------------- the days
def world(seed=P.SEED):
    rng = np.random.default_rng(seed)
    crng = np.random.default_rng(seed + 9)     # the conditioning's own variation, apart from the day's stream
    temps = temperatures(np.random.default_rng(seed + 1))
    blocks = make_blocks(np.random.default_rng(seed + 2))
    buses = make_fleet(np.random.default_rng(seed + 3))
    cards = make_cards(np.random.default_rng(seed + 4), buses)
    by_code = {b["code"]: b for b in blocks}
    bus_by = {b["fleet_no"]: b for b in buses}
    dates = list(daterange(P.START, P.END))

    # the pilot blocks: the planner's nine, the lowest 2024 fuel figures among weekday blocks of 225 km or less,
    # read from the 2024 fuel accounting (the simulated truth plus the accounting's own noise)
    def fits_pilot(b):
        # the planner's own range check for the pilot buses: the block's kilometres at its rate, the auxiliaries and
        # the electric heating at its capacity over the hours out, inside 88 per cent of the usable battery
        return b["km_old"] * traction_kwh_per_km(b) * 1.04 + b["hours"] * (P.P_AUX + P.P_CAP_PILOT + 0.4) <= 0.80 * P.E_USABLE_PILOT

    cand = [b for b in blocks if b["daytype"] == "M" and b["km_old"] <= 225 and fits_pilot(b)]
    days24 = [d for d in dates if d.year == 2024 and daytype(d) == "M"]

    def rate24(b):
        lit = 0.0
        for d in days24:
            t = temps[d]["truth"]
            lit += b["km_old"] * diesel_l_per_100km(b) / 100.0 * (1 + 0.0025 * max(0.0, 5.0 - t)) \
                + b["hours"] * (P.H_IDLE + diesel_heating_l_per_h(t))
        return lit / (b["km_old"] * len(days24)) * 100.0
    r24 = {b["code"]: rate24(b) * (1 + rng.normal(0, 0.006)) for b in cand}
    pilot = sorted(cand, key=lambda b: r24[b["code"]])[:9]
    pilot_codes = [b["code"] for b in pilot]
    for b in blocks:
        b["pilot"] = b["code"] in pilot_codes
    # the three weekday blocks the planner approved as stand-ins for an electric bus when the dispatcher is short of
    # a diesel one: the next three on the planner's own list after the nine
    fallback = [b["code"] for b in sorted(cand, key=lambda b: r24[b["code"]])[9:12]]

    # workshop days (a bus out of service for a day or several)
    out = {}       # fleet_no -> set of dates
    workshop = []
    wo = 24100
    for b in buses:
        out[b["fleet_no"]] = set()
    for b in buses:
        life = [d for d in dates if d >= b["in_service_from"] and (b["retired"] is None or d <= b["retired"])]
        k = int(rng.poisson(len(life) / 365.0 * (5.5 if b["drive"] == "diesel" else 4.0)))
        for _ in range(k):
            d0 = life[int(rng.integers(0, len(life)))]
            n = int(rng.choice([1, 1, 1, 2, 2, 3, 4, 6]))
            cat = str(rng.choice(["brakes", "tyres", "doors", "electrical", "body", "engine", "exhaust", "hvac", "service"]
                                 if b["drive"] == "diesel" else
                                 ["brakes", "tyres", "doors", "electrical", "body", "hv-battery check", "hvac", "service"]))
            wo += int(rng.integers(1, 9))
            for j in range(n):
                out[b["fleet_no"]].add(d0 + dt.timedelta(days=j))
            workshop.append({"wo": "WO-%d" % wo, "fleet_no": b["fleet_no"], "opened": d0, "closed": d0 + dt.timedelta(days=n - 1),
                             "category": cat, "hours": round(float(rng.uniform(1.5, 14)), 1), "note": ""})
    # the fuel heater faults on two electric buses in the winter of 2025/26 (the parts took weeks)
    heater_out = {1202: (dt.date(2026, 1, 12), dt.date(2026, 2, 8)), 1205: (dt.date(2026, 2, 2), dt.date(2026, 2, 24))}
    # two mechanics, two ways of writing the same fault up
    notes = {1202: ("Fuel heater does not start, fault F12 (no flame). Glow pin and metering pump on order.",
                    "Fuel heater repaired (glow pin, metering pump), test run OK."),
             1205: ("Heater fails to start after two restarts, code F12 no flame. Glow pin + dosing pump ordered from Eberspacher.",
                    "Heater repaired: new glow pin and dosing pump fitted, 30 min test run OK.")}
    for fn, (a, b_) in heater_out.items():
        wo += int(rng.integers(1, 9))
        workshop.append({"wo": "WO-%d" % wo, "fleet_no": fn, "opened": a, "closed": a, "category": "hvac",
                         "hours": 2.5, "note": notes[fn][0]})
        wo += int(rng.integers(1, 9))
        workshop.append({"wo": "WO-%d" % wo, "fleet_no": fn, "opened": b_, "closed": b_, "category": "hvac",
                         "hours": 3.0, "note": notes[fn][1]})

    # the depot pump out of service for a week (every fill at the street station)
    pump_out = (dt.date(2025, 8, 18), dt.date(2025, 8, 24))

    # ---- day by day: assignments
    roster = []       # one row per bus-day in service
    prev = {}         # block code -> bus yesterday (persistence)
    e_rot = 0
    diesel_days = []  # (date, fleet_no, block, litres, km, hours)
    ebus_days = []
    level = {b["fleet_no"]: rng.uniform(0.45, 0.95) * b["tank_l"] for b in buses if b["drive"] == "diesel"}
    htank = {fn: rng.uniform(8, 28) for fn in P.EBUS_BATCH}     # the electric buses' heater fuel tanks (30 l)
    fills = []
    sessions = []
    soc_end_prev = {fn: 100 for fn in P.EBUS_BATCH}
    sid = 0
    last_fill_day = {b["fleet_no"]: P.START - dt.timedelta(days=2) for b in buses}
    for d in dates:
        t_true = temps[d]["truth"]
        dtp = daytype(d)
        todays = [b for b in blocks if b["daytype"] == dtp]
        avail_d = [b["fleet_no"] for b in buses if b["drive"] == "diesel" and b["in_service_from"] <= d and
                   (b["retired"] is None or d <= b["retired"]) and d not in out[b["fleet_no"]]]
        avail_e = [fn for fn, since in P.EBUS_BATCH.items() if since <= d and d not in out[fn]]
        rng.shuffle(avail_d)
        assign = {}
        # electric buses first: the pilot blocks on weekdays (rotating), weekend blocks of 220 km or less, and on
        # some weekdays one bus stands in on another block the dispatcher is short on
        if avail_e:
            if dtp == "M":
                pool = [b["code"] for b in pilot]
                k = len(avail_e)
                chosen = [pool[(e_rot + i) % len(pool)] for i in range(k)]
                e_rot += 1 + (e_rot % 2)
                if rng.uniform() < 0.085 and k >= 3:
                    chosen[-1] = str(rng.choice(fallback))
            else:
                pool = [b["code"] for b in todays if b["km"] <= 220 and fits_pilot(b)]
                chosen = rng.choice(pool, size=min(len(avail_e), len(pool)), replace=False).tolist()
            for fn, code in zip(avail_e, chosen):
                assign[code] = fn
        for b in todays:
            if b["code"] in assign:
                continue
            pb = prev.get(b["code"])
            if pb in avail_d and rng.uniform() < 0.55:
                assign[b["code"]] = pb
                avail_d.remove(pb)
            else:
                if not avail_d:
                    break
                assign[b["code"]] = avail_d.pop()
        prev = dict(assign)
        for code, fn in assign.items():
            b = by_code[code]
            bus = bus_by[fn]
            km = b["km_old"] if d < P.NEW_CODES_FROM else b["km"]
            hours = b["hours"]
            roster.append({"date": d, "code": code, "fleet_no": fn, "km": km, "hours": hours})
            if bus["drive"] == "diesel":
                cold_eng = 1 + 0.0025 * max(0.0, 5.0 - t_true)
                litres = (km * diesel_l_per_100km(b) / 100.0 * cold_eng + hours * (P.H_IDLE + diesel_heating_l_per_h(t_true))) \
                    * bus["eff"] * (1 + rng.normal(0, 0.045))
                diesel_days.append({"date": d, "fleet_no": fn, "code": code, "litres": litres, "km": km, "hours": hours})
                level[fn] -= litres
                # the depot pump at the end of the day: fill when under 45 per cent, or after three days
                tank = bus["tank_l"]
                if level[fn] < 0.50 * tank or (d - last_fill_day[fn]).days >= 3 or level[fn] < 60:
                    need = tank - level[fn]
                    if pump_out[0] <= d <= pump_out[1] or rng.uniform() < 0.03:
                        # a street station, often not to full, during the day or in the evening
                        lit = min(need, rng.uniform(100, 230)) if rng.uniform() < 0.6 else need
                        fills.append({"date": d, "fleet_no": fn, "litres": lit, "where": "street", "product": "DIESEL",
                                      "minute": int(rng.uniform(9 * 60, 21 * 60))})
                        level[fn] += lit
                    else:
                        # the night staff fuel between the returns and midnight; a bus back after midnight is fuelled
                        # within the hour of its return
                        minute = int(rng.uniform(max(20 * 60 + 40, b["ret"] + 8), min(23 * 60 + 58, max(23 * 60 + 40, b["ret"] + 40))))
                        first = min(need, 250.0)
                        fills.append({"date": d, "fleet_no": fn, "litres": first, "where": "depot", "product": "DIESEL", "minute": minute})
                        rest = need - first
                        if rest > 8 and rng.uniform() < 0.72:
                            fills.append({"date": d, "fleet_no": fn, "litres": rest, "where": "depot", "product": "DIESEL",
                                          "minute": minute + int(rng.integers(2, 6))})
                            first += rest
                        level[fn] += first
                    last_fill_day[fn] = d
                # AdBlue now and then
                if rng.uniform() < 0.045:
                    fills.append({"date": d, "fleet_no": fn, "litres": float(rng.uniform(18, 42)), "where": "depot",
                                  "product": "ADBLUE", "minute": int(rng.uniform(21 * 60, 25 * 60))})
            else:
                age = (d - bus["in_service_from"]).days
                el_kw, fuel_th = pilot_heating(t_true)
                heater_dead = fn in heater_out and heater_out[fn][0] <= d < heater_out[fn][1]
                if heater_dead:
                    # with the fuel heater out the controller lets the boosters carry the demand up to their 12 kW
                    el_kw, fuel_th = min(heat_demand(t_true), 12.0) / cop(t_true), 0.0
                trac = km * traction_kwh_per_km(b) * bus["eff"] * (1 + rng.normal(0, 0.035))
                hvac = hours * el_kw * (1 + rng.normal(0, 0.05)) + hours * 0.35 * (1 if t_true > 22 else 0.3)
                aux = hours * P.P_AUX * (1 + rng.normal(0, 0.03))
                energy = trac + hvac + aux
                cap = P.E_USABLE_PILOT * (1 - fade(age)) * cold_capacity(t_true)
                soc0 = int(round(min(100, soc_end_prev[fn])))
                soc1 = soc0 - energy / cap * 100.0
                hf_l = hours * fuel_th / (P.FUEL_KWH_PER_L * P.BURNER_EFF) * (1 + rng.normal(0, 0.08))
                htank[fn] -= hf_l
                ebus_days.append({"date": d, "fleet_no": fn, "code": code, "km": km, "hours": hours, "energy": energy,
                                  "hvac": hvac, "trac": trac, "aux": aux, "soc0": soc0, "soc1": soc1, "t": t_true,
                                  "cap": cap, "heater_l": hf_l, "age": age})
                if hf_l > 0 and htank[fn] < 8:
                    lit = 30.0 - htank[fn]
                    fills.append({"date": d, "fleet_no": fn, "litres": lit, "where": "depot", "product": "HVO",
                                  "minute": int(rng.uniform(21 * 60 + 10, 25 * 60))})
                    htank[fn] += lit
                # the night's charge: plugged in after the return, unplugged before the next departure; the charger
                # meters the recharge over its efficiency and, while the relay releases it, what the bus takes beside it
                sid += 1
                target = 100 if rng.uniform() < 0.9 else int(rng.integers(90, 100))
                gain = max(0.0, target - soc1) / 100.0 * cap
                meter_noise = rng.normal(0, 0.012)
                plug_in = b["ret"] + int(rng.integers(4, 28))
                plug_out = 24 * 60 + b["dep"] - int(rng.integers(8, 45))
                start = max(plug_in, P.NIGHT_FROM) + int(rng.integers(0, 4))
                cond = conditioning_kw(night_temp(temps, d)) * released(plug_in, plug_out) / 60.0 * (1 + crng.normal(0, 0.07))
                delivered = gain / P.ETA_CHARGE * (1 + meter_noise) + cond
                sessions.append({"sid": sid, "date": d, "fleet_no": fn, "plug_in": plug_in, "plug_out": plug_out, "start": start,
                                 "kwh": delivered, "recharge_kwh": delivered - cond, "cond_kwh": cond, "soc_in": soc1, "soc_out": target,
                                 "outlet": "C%d-%s" % ((fn - 1201) // 2 + 1, "AB"[(fn - 1201) % 2])})
                soc_end_prev[fn] = target
    return {"temps": temps, "blocks": blocks, "buses": buses, "cards": cards, "roster": roster, "diesel_days": diesel_days,
            "ebus_days": ebus_days, "fills": fills, "sessions": sessions, "workshop": workshop, "pilot": pilot_codes,
            "heater_out": heater_out, "pump_out": pump_out, "dates": dates, "fallback": fallback}


def design_energy(b, t=P.DESIGN_T):
    """the truth: a 2027 bus's battery energy on block b on a day of mean temperature t"""
    return b["km"] * traction_kwh_per_km(b) + b["hours"] * (P.P_AUX + new_bus_heating(t))


def design_window(b):
    """the block's charging window on the design night: its return to its next departure, inside the night period"""
    return max(b["ret"], P.NIGHT_FROM), min(b["dep"] + 1440, P.NIGHT_TO + 1440)


def design_night_draw(b, t=P.DESIGN_T):
    """the truth: what the installation takes at the connection point for block b's bus on the design night"""
    a, z = design_window(b)
    return design_energy(b, t) / P.ETA_CHARGE + conditioning_kw(t) * max(0, z - a) / 60.0


if __name__ == "__main__":
    w = world()
    print(len(w["roster"]), "bus-days;", len(w["fills"]), "fills;", len(w["ebus_days"]), "electric bus-days;",
          len(w["sessions"]), "sessions;", len(w["workshop"]), "work orders")
    print("pilot:", w["pilot"])
    lim = P.SHARE * P.E_USABLE_2027 * (1 - fade(365))
    es = sorted((design_energy(b), b["code"], b["kind"], b["pilot"]) for b in w["blocks"] if b["daytype"] == "M")
    print("limit %.1f" % lim)
    for e, c, k, p in es:
        print("%s %-9s %6.1f %s" % (c, k, e, "pilot" if p else ""))
    print("qualify:", sum(1 for e, *_ in es if e <= lim))
    print("lowest soc end: %.1f" % min(r["soc1"] for r in w["ebus_days"]))
