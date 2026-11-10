"""The clean truth: daily temperatures, the Jonkoping pilot's duty-days and trips, the Varnamo fleet's departures with
their true and declared payloads. pack.py writes the files from it, mess and all."""
import datetime as dt
import math

import numpy as np

import params as P


def cond(t):
    """battery and cab conditioning: nothing in the mild months, coming in gradually around freezing and rising about
    linearly below it (a smooth hinge, so no setting shows as a corner in the data)"""
    z = (P.COLD2_T0 - t) / P.COLD2_S
    return P.COLD2_S * (math.log1p(math.exp(-abs(z))) + max(z, 0.0))


def kwh_per_km(climb, t, v=None):
    v = P.V_REF if v is None else v
    return (P.E0 + P.CLIMB * climb + P.COLD1 * max(0.0, 16 - t) + P.COLD2 * cond(t)
            + P.AERO * (v * v - P.V_REF ** 2) / 1000.0)


def ratio(t):
    """actual over planned speed on a day at t: winter roads, darkness and slower traffic"""
    z = (P.RT - t) / P.RS
    return P.R0 - P.RC * P.RS * (math.log1p(math.exp(-abs(z))) + max(z, 0.0))


def leg_kwh(km, climb, t, payload_km, v=None, combo_t=None):
    """one leg: the per-km draw, the combination's tare on every km, the payload's tonne-km"""
    combo_t = P.TARE_REF if combo_t is None else combo_t
    return km * kwh_per_km(climb, t, v) + P.LOAD * (combo_t - P.TARE_REF) * km + P.LOAD * payload_km


def design_speed(code):
    return P.SHORT_V[code] * ratio(P.DESIGN_T)


def phi(drops, shares=None):
    """the share of the loaded run's km the departing load rides, drop by drop"""
    shares = [d[1] for d in drops] if shares is None else shares
    pos = [d[2] for d in drops]
    rem, prev, tot = 1.0, 0.0, 0.0
    for s, p in zip(shares, pos):
        tot += rem * (p - prev)
        rem -= s
        prev = p
    return tot


def dwell_mean(n_drops):
    return (P.DWELL_LOAD[0] + P.DWELL_LOAD[1] / 2 + (n_drops - 1) * (P.DWELL_DROP[0] + P.DWELL_DROP[1] / 2)
            + P.DWELL_LAST[0] + P.DWELL_LAST[1] / 2)


def design_kwh(legs, climb, payload, t=None, v=None, combo_t=None, ph=1.0, etru=False, n_drops=1):
    t = P.DESIGN_T if t is None else t
    v = P.V_REF if v is None else v
    a, b, c = legs
    tot = a + b + c
    e = leg_kwh(tot, climb, t, payload * b * ph, v, combo_t)
    if etru:
        e += P.TRU_KW * (tot / v + dwell_mean(n_drops))
    return e


def declare(rng, code, true_t, day=None):
    prac = P.SHIPPERS[code][2]
    if code in P.SCALE_FROM and day is not None and day >= P.SCALE_FROM[code]:
        prac = "exact"
    if prac == "exact":
        return int(round(true_t * 1000 / 10)) * 10
    if prac == "std":   # the load plan's pallet count at the shipper's standard pallet weight
        n = max(1, int(round(true_t * 1000 / P.STD_LOAD[code] + rng.normal(0, 1.1))))
        return n * P.STD_LOAD[code]
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


def shortlist_km(code, mean_payload, combo_t, etru):
    shipper, climb, town, cat = P.SHORT[code]
    rng = np.random.default_rng(P.SEED + 7 + int(code[1:]))
    a = int(rng.integers(6, 34))
    r = 0.93 + 0.08 * rng.random()
    vd = design_speed(code)
    drops = P.DROPS.get(code)
    ph = phi(drops) if drops else 1.0
    nd = len(drops) if drops else 1
    target = P.TARGET[code]
    f = lambda legs: design_kwh(legs, climb, mean_payload, v=vd, combo_t=combo_t, ph=ph, etru=etru, n_drops=nd)
    # energy is linear in b at fixed a and r: solve, then search the integers
    e0, e1 = f((a, 100, int(100 * r))), f((a, 200, int(200 * r)))
    b = 100 + (target - e0) * 100 / (e1 - e0)
    best = None
    for aa in range(max(5, a - 4), a + 5):
        for bb in (int(b) - 1, int(b), int(b) + 1, int(b) + 2):
            for cc in range(int(bb * r) - 2, int(bb * r) + 3):
                err = abs(f((aa, bb, cc)) - target)
                if best is None or err < best[0] - 1e-9:
                    best = (err, (aa, bb, cc))
    return best[1]


def trailers():
    """the trailer fleet: each duty's own pool (its kind, reefers with their unit kinds), registered at its depot"""
    rng = np.random.default_rng(P.SEED + 50)
    extras = ["Tail lift 2,000 kg", "Tail lift 2,500 kg", "Side doors", "Lashing kit", "Pallet box", "Load bars",
              "ADR kit", "Roof lift", "Sliding roof", "Coil well", "Stanchions 12", "Spare wheel", "Rear doors",
              "Mezzanine deck", "Toolbox", "Strap winches", "Lift axle", "Rear steer axle"]
    xkg = {"Tail lift 2,000 kg": 480, "Tail lift 2,500 kg": 560, "Coil well": 220, "Lift axle": 90,
           "Rear steer axle": 160, "Mezzanine deck": 210, "Roof lift": 140,
           "Truck-mounted forklift": 1920}
    out, pools = {}, {}
    n = 0
    duties = sorted(P.PILOT) + ["V%02d" % k for k in range(1, 47)]
    for dcode in duties:
        spec = P.DUTY_KIND.get(dcode)
        if spec is None:
            ship = OTHERS_SHIP[dcode]
            spec = P.SHIPPER_KIND[ship]
        kind, units = (spec, None) if isinstance(spec, str) else spec
        size = 6 if dcode == "J05" else len(P.POOL_KINDS[dcode]) if dcode in P.POOL_KINDS else int(rng.integers(2, 4))
        pool = []
        for k in range(size):
            n += 1
            code = "T-%03d" % (100 + n * 3 + int(rng.integers(0, 3)))
            if dcode in P.POOL_KINDS:
                kind = P.POOL_KINDS[dcode][k]
            body, text, (lo, hi) = P.KINDS[kind]
            ex = sorted(set(rng.choice(extras, size=int(rng.integers(0, 3)), replace=False)), key=extras.index)
            if kind == "FLAT" and "Coil well" not in ex and rng.random() < 0.5:
                ex = ["Coil well"] + ex
            if P.MOFFETT.get(dcode, [False] * size)[k]:
                ex = ex + ["Truck-mounted forklift"]
            unit = None
            if units:
                ks = sorted(units)
                if dcode == "J05":
                    unit = ["SR-60e ePTO", "SR-60e ePTO", "SR-60e ePTO", "SR-60 D", "SR-60 D", "AX-40 AGen"][k]
                else:
                    unit = ks[int(rng.choice(len(ks), p=[units[x] for x in ks]))]
                ex = ["TRU " + unit] + [x for x in ex if not x.startswith("Coil")]
            tare = int(round(rng.uniform(lo, hi) + sum(xkg.get(x, 0) for x in ex), -1))
            out[code] = {"kind": kind, "body": body, "text": text, "equip": ex, "tare": tare, "unit": unit,
                         "depot": "Jönköping" if dcode.startswith("J") else "Värnamo",
                         "year": int(rng.integers(2014, 2026))}
            pool.append(code)
        pools[dcode] = pool
    return out, pools


OTHERS_SHIP = {}


def drop_shares(rng, drops):
    if not drops:
        return [1.0]
    return list(rng.dirichlet([d[1] * P.DROP_CONC for d in drops]))


def world():
    rng = np.random.default_rng(P.SEED)
    xr = np.random.default_rng(P.SEED + 60)   # architecture 8's own stream: trailers in use, drops, dwell
    temps = temperatures(rng)
    # the Varnamo terminal's other regular duties first (their shippers set their trailers)
    pool = ["TEN", "HWP", "BMJ", "TTV", "GDR", "LBY", "GST", "SKB", "HIL", "VIS", "BPL", "RPA", "FGU", "RTR", "ANE",
            "KCY", "VGL", "GLF", "HFG"]
    orng = np.random.default_rng(P.SEED + 61)
    others = {}
    n = 0
    for k in range(1, 47):
        code = "V%02d" % k
        if code in P.SHORT:
            continue
        ship = pool[n % len(pool)] if n < len(pool) else pool[int(orng.integers(0, len(pool)))]
        n += 1
        a = int(orng.integers(6, 40))
        b = int(orng.integers(190, 420))
        nd = int(orng.choice([1, 1, 1, 2, 2, 3]))
        drops = None
        if nd > 1:
            sh = orng.dirichlet([3.0] * nd)
            pos = sorted(orng.uniform(0.2, 0.9, nd - 1)) + [1.0]
            drops = [("", float(sh[i]), float(pos[i])) for i in range(nd)]
        others[code] = (ship, (a, b, int(b * (0.9 + 0.12 * orng.random()))), int(orng.integers(18, 60)), drops)
        OTHERS_SHIP[code] = ship
    tr, pools = trailers()
    # pilot duty-days: each working day six of the nine duties go to the six battery-electric tractors
    pdays = P.workdays(P.PILOT_START, P.PILOT_END)
    duties = list(P.PILOT)
    route_u = {d: rng.normal(0, P.ROUTE_SD) for d in duties}
    frng = np.random.default_rng(P.SEED + 11)
    fade = {t: P.FADE_Y1 + frng.normal(0, P.FADE_TRACTOR_SD) for t in P.PILOT_TRACTORS}
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
            dec = declare(rng, ship, pay, day)
            start = 5.0 + 0.8 * rng.random()
            t0 = start
            trips = []
            vday = P.PILOT_V[dcode] * ratio(tmean) * (1 + rng.normal(0, P.R_SD))
            tl = pools[dcode][int(xr.integers(0, len(pools[dcode])))]
            trc = tractors[slot]
            combo = (P.PILOT_TRACTOR_TARE[trc] + tr[tl]["tare"]) / 1000.0
            drops = P.DROPS.get(dcode)
            shares = drop_shares(xr, drops)
            ph = phi(drops, shares) if drops else 1.0
            for leg, km in enumerate(legs):
                t = tmean + (-1.2, 0.8, 1.6)[leg] + rng.normal(0, 0.9)
                pkm = pay * km * ph if leg == 1 else 0.0
                speed = vday * (0.9, 1.02, 1.03)[leg] * (1 + rng.normal(0, 0.015))
                e = leg_kwh(km, climb, t, pkm, speed, combo) * (1 + route_u[dcode]) * (1 + rng.normal(0, P.EPS))
                dur = km / speed
                stops = 0.0
                if leg == 1 and drops:
                    stops = sum(P.DWELL_DROP[0] + P.DWELL_DROP[1] * xr.random() for _ in drops[:-1])
                trips.append({"leg": leg, "km": km, "t": round(t, 1), "kwh": e, "start_h": start,
                              "end_h": start + dur + stops, "speed": speed})
                rest = rng.random()
                start += dur + stops + ((P.DWELL_LOAD[0] + P.DWELL_LOAD[1] * rest) if leg == 0 else
                                        (P.DWELL_LAST[0] + P.DWELL_LAST[1] * rest))
            span = trips[-1]["end_h"] - t0
            unit = tr[tl]["unit"]
            etru = unit == "SR-60e ePTO"
            if etru:   # the fridge unit runs from the battery from depot out to depot in
                w = P.TRU_KW * span * (1 + rng.normal(0, 0.08))
                for x in trips:
                    x["kwh"] += w * (x["end_h"] - x["start_h"]) / span
                trips[-1]["kwh"] += w * (1 - sum((x["end_h"] - x["start_h"]) for x in trips) / span)
            age = (day - P.PILOT_IN_SERVICE).days / 365.25
            tday = float(np.mean([x["t"] for x in trips]))
            cap = P.PILOT_USABLE * (1 - fade[trc] * age) * (1 - P.CAP_COLD * max(0.0, 20 - tday)) * \
                (1 + frng.normal(0, 0.004))
            pilot.append({"date": day, "duty": dcode, "tractor": trc, "shipper": ship, "payload": pay, "cap": cap,
                          "declared": dec, "trips": trips, "pallets": int(round(pay / 0.52 + rng.normal(0, 1.2))),
                          "trailer": tl, "shares": shares, "phi": ph, "etru": etru, "combo": combo, "span": span})
    wdays = P.workdays(P.WB_START, P.WB_END)
    depart = []
    for code in ["V%02d" % k for k in range(1, 47)]:
        ship = P.SHORT[code][0] if code in P.SHORT else others[code][0]
        drops = P.DROPS.get(code) if code in P.SHORT else others[code][3]
        mu, sd = P.SHIPPERS[ship][3], P.SHIPPERS[ship][4]
        for day in wdays:
            if code not in P.SHORT and rng.random() < 0.04:
                continue
            pay = float(np.clip(rng.normal(mu, sd), 0.4 * mu, 1.6 * mu))
            depart.append({"date": day, "duty": code, "shipper": ship, "payload": pay,
                           "declared": declare(rng, ship, pay, day), "hour": 5.2 + 1.6 * rng.random(),
                           "trailer": pools[code][int(xr.integers(0, len(pools[code])))],
                           "shares": drop_shares(xr, drops)})
    # shortlist km set from each duty's last-twelve-months mean weighed payload and the trailers it pulled
    short = {}
    for code in P.SHORT:
        dd = [x for x in depart if x["duty"] == code and P.LAST12[0] <= x["date"] <= P.LAST12[1]]
        m = float(np.mean([round(x["payload"] * 1000 / 20) * 20 / 1000 for x in dd]))
        ttare = float(np.mean([tr[x["trailer"]]["tare"] for x in dd])) / 1000.0
        combo = P.TRACTOR_2027_TARE / 1000.0 + ttare
        etru = all(tr[x["trailer"]]["unit"] == "SR-60e ePTO" for x in dd)
        legs = shortlist_km(code, m, combo, etru)
        short[code] = (P.SHORT[code][0], legs, P.SHORT[code][1], m, combo, etru)
    return {"temps": temps, "pilot": pilot, "fade": fade, "route_u": route_u, "others": others, "depart": depart,
            "short": short, "trailers": tr, "pools": pools}


def truth_design(w, code):
    """the shortlisted duty's true design-day energy (what the TARGET was set to)"""
    ship, legs, climb, m, combo, etru = w["short"][code]
    drops = P.DROPS.get(code)
    return design_kwh(legs, climb, m, v=design_speed(code), combo_t=combo, ph=phi(drops) if drops else 1.0,
                      etru=etru, n_drops=len(drops) if drops else 1)
