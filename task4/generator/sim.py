"""The clean truth: daily temperatures, the Jonkoping pilot's duty-days and trips, the Varnamo fleet's departures with
their true and declared payloads. pack.py writes the files from it, mess and all."""
import datetime as dt
import math

import numpy as np

import params as P


def kwh_per_km(climb, t):
    return P.E0 + P.CLIMB * climb + P.COLD1 * max(0.0, 16 - t) + P.COLD2 * max(0.0, -t)


def leg_kwh(km, climb, t, payload):
    return km * kwh_per_km(climb, t) + P.LOAD * payload * km


def design_kwh(legs, climb, payload, t=None):
    t = P.DESIGN_T if t is None else t
    a, b, c = legs
    return (a + b + c) * kwh_per_km(climb, t) + P.LOAD * payload * b


def declare(rng, code, true_t):
    prac = P.SHIPPERS[code][2]
    if prac == "exact":
        return int(round(true_t * 1000 / 10)) * 10
    if prac == "std":
        return P.STD_LOAD[code]
    v = true_t * (1 + rng.normal(0, P.EST_SD))
    return int(round(v * 1000 / 50)) * 50


def temperatures(rng):
    """daily mean temperature at the two stations, 2016-01-01 to 2026-10-31"""
    d0, d1 = dt.date(2016, 1, 1), dt.date(2026, 10, 31)
    out = {}
    a_j = a_v = 0.0
    d = d0
    while d <= d1:
        doy = d.timetuple().tm_yday
        clim = 6.6 - 9.4 * math.cos(2 * math.pi * (doy - 22) / 365.25)
        sd = 3.9 - 1.4 * math.cos(2 * math.pi * (doy - 22) / 365.25 + math.pi)
        a_j = 0.78 * a_j + rng.normal(0, sd * math.sqrt(1 - 0.78 ** 2))
        a_v = 0.6 * a_v + 0.4 * a_j + rng.normal(0, 0.6)
        out[d] = (round(clim + a_j, 1), round(clim - 0.4 + a_v, 1))
        d += dt.timedelta(days=1)
    return out


def shortlist_km(code, mean_payload):
    shipper, climb, town, cat = P.SHORT[code]
    rng = np.random.default_rng(P.SEED + 7 + int(code[1:]))
    a = int(rng.integers(6, 34))
    r = 0.93 + 0.08 * rng.random()
    k = kwh_per_km(climb, P.DESIGN_T)
    target = P.LIMIT + P.TARGET[code]
    b = (target - a * k) / ((1 + r) * k + P.LOAD * mean_payload)
    best = None
    for aa in range(max(5, a - 4), a + 5):
        for bb in (int(b) - 1, int(b), int(b) + 1, int(b) + 2):
            for cc in range(int(bb * r) - 2, int(bb * r) + 3):
                err = abs(design_kwh((aa, bb, cc), climb, mean_payload) - target)
                if best is None or err < best[0] - 1e-9:
                    best = (err, (aa, bb, cc))
    return best[1]


def world():
    rng = np.random.default_rng(P.SEED)
    temps = temperatures(rng)
    # pilot duty-days: each working day six of the nine duties go to the six battery-electric tractors
    pdays = P.workdays(P.PILOT_START, P.PILOT_END)
    duties = list(P.PILOT)
    route_u = {d: rng.normal(0, P.ROUTE_SD) for d in duties}
    pilot = []
    for day in pdays:
        chosen = sorted(rng.choice(len(duties), size=6, replace=False))
        tractors = list(P.PILOT_TRACTORS)
        rng.shuffle(tractors)
        tmean = temps[day][0]
        for slot, i in enumerate(chosen):
            dcode = duties[i]
            ship, legs, climb, town = P.PILOT[dcode]
            mu, sd = P.SHIPPERS[ship][3], P.SHIPPERS[ship][4]
            pay = float(np.clip(rng.normal(mu, sd), 0.4 * mu, 1.6 * mu))
            dec = declare(rng, ship, pay)
            start = 5.0 + 0.8 * rng.random()
            trips = []
            for leg, km in enumerate(legs):
                t = tmean + (-1.2, 0.8, 1.6)[leg] + rng.normal(0, 0.9)
                p = pay if leg == 1 else 0.0
                e = leg_kwh(km, climb, t, p) * (1 + route_u[dcode]) * (1 + rng.normal(0, P.EPS))
                speed = (52, 71, 74)[leg] + rng.normal(0, 4)
                dur = km / speed
                trips.append({"leg": leg, "km": km, "t": round(t, 1), "kwh": e, "start_h": start,
                              "end_h": start + dur, "speed": speed})
                start += dur + (0.75 if leg == 0 else 0.6) + 0.2 * rng.random()
            pilot.append({"date": day, "duty": dcode, "tractor": tractors[slot], "shipper": ship, "payload": pay,
                          "declared": dec, "trips": trips, "pallets": int(round(pay / 0.52 + rng.normal(0, 1.2)))})
    # Varnamo duties: the shortlist plus the rest of the terminal's regular duties
    others = {}
    pool = ["TEN", "HWP", "BMJ", "TTV", "GDR", "LBY", "GST", "SKB", "HIL", "VIS", "BPL", "RPA", "FGU", "RTR", "ANE", "KCY", "VGL"]
    n = 0
    for k in range(1, 47):
        code = "V%02d" % k
        if code in P.SHORT:
            continue
        ship = pool[n % len(pool)] if n < 2 * len(pool) else pool[int(rng.integers(0, 6))]
        n += 1
        a = int(rng.integers(6, 40))
        b = int(rng.integers(190, 420))
        others[code] = (ship, (a, b, int(b * (0.9 + 0.12 * rng.random()))), int(rng.integers(18, 60)))
    wdays = P.workdays(P.WB_START, P.WB_END)
    depart = []
    for code in ["V%02d" % k for k in range(1, 47)]:
        ship = P.SHORT[code][0] if code in P.SHORT else others[code][0]
        mu, sd = P.SHIPPERS[ship][3], P.SHIPPERS[ship][4]
        for day in wdays:
            if code not in P.SHORT and rng.random() < 0.04:
                continue
            pay = float(np.clip(rng.normal(mu, sd), 0.4 * mu, 1.6 * mu))
            depart.append({"date": day, "duty": code, "shipper": ship, "payload": pay,
                           "declared": declare(rng, ship, pay), "hour": 5.2 + 1.6 * rng.random()})
    # shortlist km set from each duty's last-twelve-months mean weighed payload
    short = {}
    for code in P.SHORT:
        loads = [x["payload"] for x in depart if x["duty"] == code and P.LAST12[0] <= x["date"] <= P.LAST12[1]]
        m = float(np.mean([round(v * 1000 / 20) * 20 / 1000 for v in loads]))
        legs = shortlist_km(code, m)
        short[code] = (P.SHORT[code][0], legs, P.SHORT[code][1], m)
    return {"temps": temps, "pilot": pilot, "route_u": route_u, "others": others, "depart": depart, "short": short}
