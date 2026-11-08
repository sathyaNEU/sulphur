"""The clean truth: every delivery day of 2025 and 2026 to 30 October, every run, every stop, drawn from the
territory geometry in params.py. Each run sweeps its districts outward in road order and drives back to the depot
from the farthest district it served that day; a district with no stops that day is driven through, not entered."""
import datetime as dt
import hashlib
import math

import numpy as np

import params as P


def hav(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 6371.0 * 2 * math.asin(math.sqrt(h))


def coord(code):
    return (P.DEPOT[1], P.DEPOT[2]) if code is None else (P.D[code][1], P.D[code][2])


def edge_h(code):
    """the drive from the district before it on the road (or the depot) to this district, hours"""
    v = P.D[code]
    km = max(hav(coord(v[3]), coord(code)), 0.8)
    return km * v[4] / v[5]


def edge_km(code):
    v = P.D[code]
    return max(hav(coord(v[3]), coord(code)), 0.8) * v[4]


def chain(run):
    """the run's districts from the depot outward"""
    first = [c for c, v in P.D.items() if v[6] == run and v[3] is None]
    out = [first[0]]
    while True:
        nxt = [c for c, v in P.D.items() if v[3] == out[-1]]
        if not nxt:
            return out
        out.append(nxt[0])


RUN_CHAIN = {r: chain(r) for r in P.RUNS}
RUN_OF = {c: v[6] for c, v in P.D.items()}


def season(d):
    return P.SEASON[d.month]


def mu(code, d):
    """expected stops on a delivery day d"""
    v = P.D[code]
    base = v[7] / v[9] if d.year == 2025 else v[7]
    return base * season(d)


def stop_ref(code, i):
    return "A" + hashlib.sha1(("%s-%d" % (code, i)).encode()).hexdigest()[:7].upper()


def world():
    rng = np.random.default_rng(P.SEED)
    days = P.delivery_days(P.HIST_START, P.HIST_END)
    pools = {c: max(40, int(v[7] * 140)) for c, v in P.D.items()}
    vans = {r: "%s-D-%05d" % ("191" if i % 2 else "192", 10411 + 37 * i) for i, r in enumerate(P.RUNS)}
    drivers = {r: "DRV%03d" % (101 + 7 * i) for i, r in enumerate(P.RUNS)}
    rundays = []
    for d in days:
        for r, ch in RUN_CHAIN.items():
            stops = {}
            for c in ch:
                n = rng.poisson(mu(c, d))
                lst = []
                for _ in range(n):
                    kind = "DEL"
                    u = rng.random()
                    if u < P.COLLECT_RATE:
                        kind = "COL"
                    elif u < P.COLLECT_RATE + P.FAIL_RATE:
                        kind = "FAIL"
                    pps = P.D[c][8]
                    parcels = 0 if kind == "COL" else 1 + rng.poisson(pps - 1)
                    lst.append({"kind": kind, "parcels": parcels, "ref": stop_ref(c, int(rng.integers(pools[c]))),
                                "collect": int(1 + rng.poisson(0.3)) if kind == "COL" else 0})
                stops[c] = lst
            vis = [c for c in ch if stops[c]]
            out_t = 7.45 + rng.normal(0, 0.12)          # leaves the depot about a quarter to eight, hours
            t = out_t
            seq, prev = [], None                        # prev: the district of the stop before (None: depot)
            broke = False
            for c in vis:
                # drive from prev (or the depot) to this district's first stop
                k = ch.index(c)
                j = ch.index(prev) + 1 if prev is not None else 0
                drive = sum(edge_h(x) for x in ch[j:k + 1]) + P.D[c][11] / 2 + (P.D[prev][11] / 2 if prev else 0)
                first = True
                for s in stops[c]:
                    leg = drive if first else P.D[c][12]
                    leg *= float(np.exp(rng.normal(0, P.LEG_SD)))
                    t += leg
                    arr = t
                    if s["kind"] == "FAIL":
                        dw = P.DWELL_FAILED
                    elif s["kind"] == "COL":
                        dw = P.DWELL_BASE + 0.4 / 60 * s["collect"]
                    else:
                        dw = P.DWELL_BASE + P.DWELL_PARCEL * s["parcels"]
                    dw *= float(np.exp(rng.normal(0, P.DWELL_SD)))
                    t += dw
                    seq.append({"district": c, "arr": arr, "dep": t, "leg": leg, **s})
                    first = False
                    if not broke and t - out_t >= 3.0:
                        seq.append({"district": None, "kind": "BREAK", "arr": t, "dep": t + P.BREAK_H, "leg": 0.0,
                                    "parcels": 0, "ref": "", "collect": 0})
                        t += P.BREAK_H
                        broke = True
                prev = c
            if not broke:
                seq.append({"district": None, "kind": "BREAK", "arr": t, "dep": t + P.BREAK_H, "leg": 0.0,
                            "parcels": 0, "ref": "", "collect": 0})
                t += P.BREAK_H
            back = (sum(edge_h(x) for x in ch[:ch.index(prev) + 1]) + P.D[prev][11] / 2) if prev else 0.0
            back *= float(np.exp(rng.normal(0, P.LEG_SD)))
            t += back
            km = 2 * sum(edge_km(x) for x in ch[:ch.index(prev) + 1]) if prev else 0.0
            km += sum(len(stops[c]) * P.D[c][12] * 45 for c in vis)
            rundays.append({"date": d, "run": r, "van": vans[r], "driver": drivers[r], "out": out_t, "in": t,
                            "stops": seq, "km": km * float(np.exp(rng.normal(0, 0.03))), "counts": {c: len(stops[c]) for c in ch}})
    return {"days": days, "rundays": rundays}


if __name__ == "__main__":
    w = world()
    import collections
    hrs = collections.defaultdict(list)
    for rd in w["rundays"]:
        hrs[rd["run"]].append(rd["in"] - rd["out"])
    for r in sorted(hrs):
        print(r, P.RUNS[r], "mean hours %.2f min %.2f max %.2f" % (np.mean(hrs[r]), min(hrs[r]), max(hrs[r])))
    print(len(w["rundays"]), "run-days", sum(len(x["stops"]) for x in w["rundays"]), "stop rows")
