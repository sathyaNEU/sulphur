"""task7 architecture 11: Hollins Creek Electric Association's EV Overnight rate and the 2025-26 managed-charging pilot.

The world is simulated as the association's systems would see it: homes on distribution transformers, each home's load at the
quarter-hour (a baseline that follows the household, central air that follows the heat with the house's lag, dryers, cooking,
hot tubs, rooftop solar), EVs that drive, come home, plug in and leave in the morning, and the chargers enrolled on the rate
charging either on their owners' own timers or, for the pilot's managed half, at a random start that still finishes by the
member's departure. Nothing is placed where it decides: every mechanism runs across every transformer."""
import datetime as dt

import numpy as np
from scipy.signal import lfilter

SEED = 110711
AS_OF = dt.date(2026, 11, 6)
RAND_DAY = dt.date(2025, 5, 12)            # the pilot's split of the chargers enrolled by then
PAUSE_DAY = dt.date(2026, 6, 1)            # enrolment paused until the board sets the 2027 default
JUL1 = dt.date(2026, 7, 1)
NDAY = 62                                  # July and August 2026
Q = 96
OFF = 23 * 4                               # the off-peak window opens at 23:00
WEND = 7 * 4                               # and closes at 07:00 next morning
PF = 0.95
LIMIT = 1.20                               # DPS-7: 120 per cent of nameplate kVA on the highest 15-minute load
FEE = {"stagger": 18.0, "sequence": 40.0}  # Quillpoint's 2027 fee per enrolled charger per year (USD)
COST = {25.0: 10800, 37.5: 11400, 50.0: 18200, 75.0: 21500, 100.0: 26900}   # replacement by the next size, installed
NEXT = {25.0: 50.0, 37.5: 50.0, 50.0: 75.0, 75.0: 100.0, 100.0: 167.0}
COST_POLE50 = 13900                        # DPS-7 Table 1: a 50 kVA pole-mount unit by a 75 kVA pole-mount, installed
# DPS-7 Table 2 (revision 5): the 15-minute peaking factor by nameplate, set by engineering from the 48 monitored
# transformers' July and August 2026 loads (a day's highest 15-minute load over its clock hour's load, averaged over
# the days and the monitored units of each size, to two places); checks.py asserts the monitors file reproduces it
PEAK = {25.0: 1.15, 37.5: 1.15, 50.0: 1.13, 75.0: 1.11, 100.0: 1.10}
AREAS = {
    # name: transformers, kVA choices with weights, homes per transformer, mount, EV-rate adoption, AC share, home size
    "Prairie Hollow": dict(n=160, kva=([25.0, 37.5], [0.62, 0.38]), homes={25.0: (3, 5), 37.5: (4, 7)}, mount="pole", adopt=0.31, ac=0.78, size=0.85,
                           prefix="PH", year=(1987, 2002)),
    "Larkin Ridge": dict(n=145, kva=([50.0], [1.0]), homes={50.0: (7, 11)}, mount="pad", adopt=0.30, ac=0.88, size=1.0,
                         prefix="LR", year=(2003, 2012)),
    "Stonebrook": dict(n=125, kva=([75.0, 100.0], [0.6, 0.4]), homes={75.0: (9, 13), 100.0: (12, 16)}, mount="pad", adopt=0.33, ac=0.95, size=1.22,
                       prefix="SB", year=(2015, 2024)),
}
POWER = np.array([7.2, 9.6, 11.5])
OWN = ["t2300", "t2330", "t0000", "ready", "now"]
OWN_P = [0.74, 0.07, 0.05, 0.09, 0.05]


def summer_days(year):
    d0 = dt.date(year, 6, 1)
    return [d0 + dt.timedelta(days=k) for k in range(122)]


def weather(rng):
    """hourly dry-bulb temperature (F), June to September 2024 to 2026, at the association's station (local standard time)"""
    out = {}
    for year in (2024, 2025, 2026):
        days = summer_days(year)
        n = len(days)
        doy = np.arange(n)
        tmax = 84.5 + 6.5 * np.sin((doy - 5) / 122 * np.pi) + rng.normal(0, 4.0, n)
        tmax = np.convolve(tmax, [0.25, 0.5, 0.25], mode="same")
        tmax[0] = 82.0
        for s in rng.choice(np.arange(20, n - 8), 3 if year != 2026 else 4, replace=False):
            ln = int(rng.integers(3, 6))
            tmax[s:s + ln] += rng.uniform(6, 10) * np.sin(np.linspace(0.6, 2.5, ln))
        storms = rng.random(n) < 0.22
        tmax[storms] -= rng.uniform(3, 9, storms.sum())
        tmin = 0.55 * tmax + 10.5 + rng.normal(0, 2.2, n)
        hrs = []
        for k in range(n):
            nxt = tmin[min(k + 1, n - 1)]
            for h in range(24):
                if h <= 5:
                    v = tmin[k] + 1.8 * (5 - h) / 5
                elif h <= 15:
                    v = tmin[k] + (tmax[k] - tmin[k]) * (1 - np.cos((h - 5) / 10 * np.pi)) / 2
                else:
                    v = tmax[k] - (tmax[k] - nxt) * (1 - np.exp(-(h - 15) / 4.2)) / (1 - np.exp(-9 / 4.2))
                hrs.append(v + rng.normal(0, 0.8))
        out[year] = dict(days=days, tmax=tmax, tmin=tmin, hourly=np.array(hrs))
    return out


class World:
    pass


def build():
    rng = np.random.default_rng(SEED)
    w = World()
    w.wx = weather(rng)
    # transformers and homes
    tx, homes = [], []
    for area, a in AREAS.items():
        kvas, kp = a["kva"]
        for i in range(a["n"]):
            kv = float(rng.choice(kvas, p=kp))
            t = dict(area=area, kva=kv, mount=a["mount"],
                     year=int(rng.integers(a["year"][0], a["year"][1] + 1)), nh=int(rng.integers(a["homes"][kv][0], a["homes"][kv][1] + 1)),
                     lean=float(rng.lognormal(0, 0.55)))
            t["idx"] = len(tx)
            tx.append(t)
            for h in range(t["nh"]):
                homes.append(dict(tx=t["idx"], area=area, size=a["size"] * float(rng.lognormal(0, 0.22)),
                                  ac=bool(rng.random() < a["ac"]), accap=float(rng.uniform(2.8, 4.6)),
                                  setp=float(rng.normal(75.5, 1.8)), lag=float(rng.uniform(3.0, 6.0)),
                                  tub=bool(rng.random() < 0.035), pv=float(rng.choice([5.5, 7.6, 9.2]) if rng.random() < 0.12 else 0),
                                  dryer=float(rng.uniform(0.10, 0.40)), cook=float(rng.uniform(0.3, 0.8)),
                                  wkoff=float(rng.normal(0, 0.6))))
    w.tx, w.homes = tx, homes
    H = len(homes)
    # EVs: enrolled chargers and unenrolled EVs, adoption clustered by transformer
    chargers, unev = [], []
    for hi, h in enumerate(homes):
        t = tx[h["tx"]]
        a = AREAS[h["area"]]
        p = min(0.75, a["adopt"] * t["lean"])
        if rng.random() < p:
            n = 2 if rng.random() < 0.14 else 1
            for k in range(n):
                chargers.append(dict(home=hi, power=float(rng.choice(POWER, p=[0.30, 0.35, 0.35] if h["area"] == "Prairie Hollow" else ([0.50, 0.30, 0.20] if h["area"] == "Larkin Ridge" else [0.35, 0.35, 0.30]))),
                                     own=str(rng.choice(OWN, p=OWN_P)), plug=float(rng.choice([0.96, 0.82, 0.60], p=[0.50, 0.35, 0.15])),
                                     km=float(rng.lognormal(np.log(62), 0.45)), arr=float(rng.normal(18.6, 1.1)),
                                     dep=float(np.clip(rng.normal(7.35, 0.55), 5.0, 9.0)), batt=float(rng.choice([60, 75, 82, 100]))))
        elif rng.random() < min(0.30, 0.45 * a["adopt"] * t["lean"]):
            unev.append(dict(home=hi, power=float(rng.choice([7.2, 9.6, 1.4], p=[0.7, 0.2, 0.1])),
                             mode=str(rng.choice(["now", "t1900", "t2300"], p=[0.55, 0.30, 0.15])),
                             plug=float(rng.choice([0.9, 0.6, 0.4])), km=float(rng.lognormal(np.log(48), 0.45)),
                             arr=float(rng.normal(17.8, 1.1)), dep=float(np.clip(rng.normal(7.3, 0.8), 5.0, 9.5))))
    # enrolment dates, the pilot's split, swaps and departures
    rate0 = dt.date(2024, 3, 4)
    for c in chargers:
        u = rng.random()
        if u < 0.42:
            c["enrol"] = rate0 + dt.timedelta(days=int(rng.integers(0, 150)))
        elif u < 0.72:
            c["enrol"] = dt.date(2024, 8, 1) + dt.timedelta(days=int(rng.integers(0, 284)))
        else:
            c["enrol"] = RAND_DAY + dt.timedelta(days=int(rng.integers(1, (PAUSE_DAY - RAND_DAY).days)))
        c["arm"] = "managed" if rng.random() < 0.25 else "own"
        c["swap"] = None
        if rng.random() < 0.035:
            c["swap"] = dt.date(2025, 9, 1) + dt.timedelta(days=int(rng.integers(0, 400)))
        c["left"] = None
        if rng.random() < 0.035:
            c["left"] = dt.date(2026, 9, 3) + dt.timedelta(days=int(rng.integers(0, 55)))
        c["change"] = None
        if c["enrol"] < RAND_DAY and rng.random() < 0.06:
            c["change"] = str(rng.choice(OWN, p=OWN_P))     # an own setting changed after summer 2024
        # what the member told the enrolment form about how they charge (most say what they do)
        c["declared"] = c["own"] if rng.random() < 0.90 else str(rng.choice(OWN, p=OWN_P))
    w.chargers, w.unev = chargers, unev
    w.rng = rng
    sessions(w, rng)
    records(w, rng)
    base(w, rng)
    actual(w, rng)
    return w


def _nights(year):
    return summer_days(year)


def sessions(w, rng):
    """each EV's plug-ins, energy and unplug, night by night, June to September of 2024 to 2026"""
    w.sess = {}
    for ci, c in enumerate(w.chargers):
        w.sess[ci] = _ev_nights(c, rng, enrolled=True)
    w.usess = {}
    for ui, u in enumerate(w.unev):
        w.usess[ui] = _ev_nights(u, rng, enrolled=False)


def _ev_nights(c, rng, enrolled):
    out = []
    deficit = float(rng.uniform(5, 25))
    for year in (2024, 2025, 2026):
        for d in summer_days(year):
            wd = d.weekday()
            drive = c["km"] * 0.18 * float(rng.lognormal(0, 0.45)) * (0.75 if wd >= 5 else 1.0)
            if wd >= 5 and rng.random() < 0.07:
                drive += float(rng.uniform(25, 55))        # a weekend trip
            deficit = min(deficit + drive, c.get("batt", 75) * 0.9)
            p = c["plug"] * (0.85 if wd in (4, 5) else 1.0)
            if deficit < 6 and rng.random() < 0.6:
                continue
            if rng.random() > p:
                continue
            arr = c["arr"] + (float(rng.normal(1.3, 1.6)) if wd >= 5 else float(rng.normal(0, 0.9)))
            arr = float(np.clip(arr, 14.0, 23.6))
            dep = c["dep"] + (float(rng.normal(1.8, 1.0)) if wd in (4, 5) else float(rng.normal(0, 0.35)))
            dep = float(np.clip(dep, 4.75, 11.5))
            e = deficit * float(rng.uniform(0.92, 1.0))
            pq, dq = int(round(arr * 4)), int(round(dep * 4)) + Q
            out.append((d, pq, dq, round(e, 2), pq * 15 + int(rng.integers(0, 15)), dq * 15 + int(rng.integers(0, 15))))
            deficit -= e
    return out


def own_start(setting, plug, dep, q):
    """the quarter an own-schedule charger starts: its owner's timer, a ready-by time, or at once"""
    if setting == "t2300":
        return max(plug, OFF)
    if setting == "t2330":
        return max(plug, OFF + 2)
    if setting == "t0000":
        return max(plug, Q)
    if setting == "ready":
        return max(plug, dep - q - 2)
    return plug


def setting_on(c, d):
    if c["change"] is not None and d >= dt.date(2025, 1, 1):
        return c["change"]
    return c["own"]


def charge_profile(start, e, p, horizon=2 * Q + 16):
    """kW by quarter from the evening's quarter 0: a block at the charger's power from `start` (in quarters, possibly
    part-way into one) for e/p hours"""
    L = np.zeros(horizon)
    a = float(start)
    b = a + e / p * 4.0
    for k in range(int(np.floor(a)), min(horizon, int(np.ceil(b)))):
        ov = min(b, k + 1) - max(a, k)
        if ov > 0:
            L[k] += p * ov
    return L


def base(w, rng):
    """each home's own load (no enrolled charger) at the quarter-hour, July and August 2026, plus the unenrolled EVs"""
    wx = w.wx[2026]
    days = wx["days"]
    i0 = days.index(JUL1)
    # local daylight time = standard time + 1 hour: the station's hour h (LST) is local hour h+1
    temp = wx["hourly"].reshape(-1, 24)
    H = len(w.homes)
    nq = (NDAY + 1) * Q
    tq = np.repeat(np.concatenate([temp[i0 - 1:i0 + NDAY + 1].ravel()]), 4)[4 * 23:]     # shift one hour to daylight time
    tq = tq[:nq]
    hq = np.tile(np.arange(Q) / 4.0, NDAY + 1)
    dows = np.repeat([(JUL1 + dt.timedelta(days=k)).weekday() for k in range(NDAY + 1)], Q)
    wkend = (dows >= 5).astype(float)
    B = np.zeros((H, nq), dtype=np.float32)
    sun = np.clip(np.sin((hq - 5.8) / 14.6 * np.pi), 0, None)
    for hi, h in enumerate(w.homes):
        s = h["size"]
        hh = (hq - h["wkoff"]) % 24
        prof = (0.30 + 0.16 * np.exp(-((hh - 7.0) / 1.3) ** 2) * (1 - 0.6 * wkend) + 0.22 * np.exp(-((hh - 12.5) / 3.5) ** 2) * wkend
                + 0.42 * np.exp(-((hh - 19.6) / 2.4) ** 2) - 0.10 * np.exp(-((hh - 3.5) / 2.2) ** 2))
        load = s * prof * (1 + rng.normal(0, 0.10, nq))
        if h["ac"]:
            alpha = 1 / (4 * h["lag"])
            ind, _ = lfilter([alpha], [1, -(1 - alpha)], tq, zi=[tq[0] * (1 - alpha)])
            drive = ind + 6.0 * sun - h["setp"] - 0.5 * ((hh > 23) | (hh < 6))
            duty = np.clip(drive / 21.0, 0, 1)
            cyc = np.clip(duty + rng.normal(0, 0.16, nq) * np.sqrt(np.clip(duty * (1 - duty), 0, None)) * 1.4, 0, 1)
            load = load + h["accap"] * cyc * s ** 0.5
        # dryers and cooking
        for day in range(NDAY + 1):
            o = day * Q
            if rng.random() < h["dryer"]:
                st = int(np.clip(rng.normal(19.0 if dows[o] < 5 else 13.0, 2.6), 7, 22.5) * 4)
                load[o + st:o + st + int(rng.integers(3, 5))] += 3.8
            if rng.random() < h["cook"]:
                st = int(np.clip(rng.normal(17.6, 0.8), 15.5, 20) * 4)
                load[o + st:o + st + int(rng.integers(2, 4))] += float(rng.uniform(1.5, 2.6))
            if h["tub"] and rng.random() < 0.8:
                st = int(rng.uniform(21.5, 27.5) * 4)
                ln = int(rng.integers(2, 6))
                a0, a1 = o + st, min(o + st + ln, nq)
                load[a0:a1] += 5.5
        if h["pv"]:
            cloud = np.repeat(rng.uniform(0.35, 1.0, NDAY + 1), Q)
            load = load - h["pv"] * 0.78 * sun ** 1.3 * cloud
        B[hi] = load
    w.B = B                    # kW by home and quarter, from 00:00 on 1 July 2026 (and one extra day of night)
    # unenrolled EVs add their charging to their homes
    U = np.zeros_like(B)
    for ui, u in enumerate(w.unev):
        for (d, plug, dep, e, pm, dm) in w.usess[ui]:
            if not (JUL1 <= d < JUL1 + dt.timedelta(days=NDAY)):
                continue
            o = (d - JUL1).days * Q
            if u["mode"] == "t1900" and d.weekday() < 5:
                st = max(plug, 19 * 4)
            elif u["mode"] == "t2300":
                st = max(plug, OFF)
            else:
                st = pm / 15.0
            L = charge_profile(st, e, u["power"])
            lo = o
            hi = min(o + len(L), nq)
            U[u["home"], lo:hi] += L[:hi - lo]
    w.U = U


def actual(w, rng):
    """what each enrolled charger actually did, session by session: its owner's setting before the split and in the own half,
    Quillpoint Stagger's random start in the managed half (finishing by the member's ready-by time)"""
    w.act = {}
    for ci, c in enumerate(w.chargers):
        out = []
        for (d, plug, dep, e, pm, dm) in w.sess[ci]:
            if d < c["enrol"] or (c["left"] is not None and d >= c["left"]):
                out.append(None)
                continue
            q = int(np.ceil(e / c["power"] * 4))
            plug = int(np.ceil(pm / 15.0))                     # no charger starts before it is plugged in
            managed = c["arm"] == "managed" and d >= max(RAND_DAY, c["enrol"])
            if managed:
                ready = dep - int(rng.integers(0, 3))
                lo = max(plug, OFF)
                hi = max(lo, ready - q)
                st = int(rng.integers(lo, hi + 1))
                out.append(dict(start=st, ready=ready, mode="managed"))
            else:
                s = setting_on(c, d)
                st = own_start(s, plug, dep, q)
                out.append(dict(start=(pm / 15.0 if s == "now" else st), ready=None, mode=s))
        w.act[ci] = out
    # the enrolled chargers' actual charging in July and August 2026, by home and quarter
    H = len(w.homes)
    nq = (NDAY + 1) * Q
    A = np.zeros((H, nq), dtype=np.float32)
    for ci, c in enumerate(w.chargers):
        for (d, plug, dep, e, pm, dm), a in zip(w.sess[ci], w.act[ci]):
            if a is None or not (JUL1 <= d < JUL1 + dt.timedelta(days=NDAY)):
                continue
            o = (d - JUL1).days * Q
            L = charge_profile(a["start"], e, c["power"])
            hi = min(o + len(L), nq)
            A[c["home"], o:hi] += L[:hi - o]
    w.A = A


def records(w, rng):
    """what the association's systems hold about the network: monitors, transformer work in 2025-26, meter exchanges"""
    T = len(w.tx)
    by_area = {}
    for t in w.tx:
        by_area.setdefault((t["area"], t["kva"]), []).append(t["idx"])
    mon = []
    for key in sorted(by_area):
        ids = by_area[key]
        k = max(4, int(round(48 * len(ids) / T)))
        mon += list(rng.choice(ids, size=min(k, len(ids)), replace=False))
    w.monitored = sorted(int(m) for m in mon)[:48] if len(mon) > 48 else sorted(int(m) for m in mon)
    # units replaced in spring 2026 (sized up after 2025), and a few where a second transformer took some homes
    small = [t["idx"] for t in w.tx if t["kva"] <= 37.5]
    w.replaced = sorted(int(x) for x in rng.choice(small, size=9, replace=False))
    for x in w.replaced:
        t = w.tx[x]
        t["old_kva"] = t["kva"]
        t["kva"] = NEXT[t["kva"]]
        t["replaced_on"] = dt.date(2026, 3, 9) + dt.timedelta(days=int(rng.integers(0, 70)))
    multi = [t["idx"] for t in w.tx if t["nh"] >= 5 and t["idx"] not in w.replaced]
    w.splits = []
    for x in rng.choice(multi, size=4, replace=False):
        hs = [hi for hi, h in enumerate(w.homes) if h["tx"] == int(x)]
        moved = sorted(int(m) for m in rng.choice(hs, size=2, replace=False))
        w.splits.append(dict(parent=int(x), moved=moved, on=dt.date(2026, 4, 6) + dt.timedelta(days=int(rng.integers(0, 50)))))
    for sp in w.splits:
        new = dict(area=w.tx[sp["parent"]]["area"], kva=w.tx[sp["parent"]]["kva"], mount=w.tx[sp["parent"]]["mount"], year=2026,
                   nh=len(sp["moved"]), lean=1.0, idx=len(w.tx), new_on=sp["on"])
        w.tx.append(new)
        for hi in sp["moved"]:
            w.homes[hi]["tx"] = new["idx"]
        w.tx[sp["parent"]]["nh"] -= len(sp["moved"])
        sp["child"] = new["idx"]
    # meters exchanged during July and August 2026
    w.exchanged = {}
    for hi in rng.choice(len(w.homes), size=int(0.018 * len(w.homes)), replace=False):
        w.exchanged[int(hi)] = JUL1 + dt.timedelta(days=int(rng.integers(3, NDAY - 3)))
