"""task22 clean truth: Delmont Power and Light's distribution system from September 2023 to October 2026, hour by
hour. The process simulated: weather drives every customer class's load; customers, licensed grows, a cold store and
illegal grows sit at nodes of fourteen radial feeders whose switching changes who each feeder serves; current through
every segment loses its square times the conductor's resistance, transformers lose their core losses all year and
their copper losses with the square of their load; the feeder breakers' telemetry, the wholesale delivery point
meters, the AMR and AMI meters, the lights' deemed billing and the 2019 loss study each see part of it."""
import datetime as dt
import math
import zlib
from collections import defaultdict, deque

import numpy as np

import params as P

UTC = dt.timezone.utc


class W:
    pass


# ---------------------------------------------------------------------------------------------------------------
# time and weather
# ---------------------------------------------------------------------------------------------------------------

def time_grid(start_local, end_local):
    s, e = start_local.astimezone(UTC), end_local.astimezone(UTC)
    H = int((e - s).total_seconds() // 3600)
    utc = [s + dt.timedelta(hours=k) for k in range(H)]
    loc = [u.astimezone(P.TZ) for u in utc]
    d0 = start_local.date()
    g = W()
    g.H, g.utc, g.loc = H, utc, loc
    g.hod = np.array([x.hour for x in loc], dtype=np.int16)
    g.dow = np.array([x.weekday() for x in loc], dtype=np.int16)
    g.day = np.array([(x.date() - d0).days for x in loc], dtype=np.int32)
    g.month = np.array([x.month for x in loc], dtype=np.int16)
    g.doy = np.array([x.timetuple().tm_yday for x in loc], dtype=np.int16)
    g.D = int(g.day.max()) + 1
    g.dord = np.array([x.date().toordinal() for x in loc], dtype=np.int32)
    g.dates = [d0 + dt.timedelta(days=k) for k in range(g.D)]
    g.d0 = d0
    return g


def solar_elevation(utc_list, lat, lon):
    out = np.zeros(len(utc_list))
    for k, u in enumerate(utc_list):
        # the hour's midpoint
        t = u + dt.timedelta(minutes=30)
        n = t.timetuple().tm_yday
        frac = 2 * math.pi / 365.0 * (n - 1 + (t.hour - 12) / 24.0)
        decl = (0.006918 - 0.399912 * math.cos(frac) + 0.070257 * math.sin(frac) - 0.006758 * math.cos(2 * frac)
                + 0.000907 * math.sin(2 * frac) - 0.002697 * math.cos(3 * frac) + 0.00148 * math.sin(3 * frac))
        eqt = 229.18 * (0.000075 + 0.001868 * math.cos(frac) - 0.032077 * math.sin(frac) - 0.014615 * math.cos(2 * frac)
                        - 0.040849 * math.sin(2 * frac))
        tst = t.hour * 60 + t.minute + eqt + 4 * lon
        ha = math.radians(tst / 4.0 - 180.0)
        la = math.radians(lat)
        cz = math.sin(la) * math.sin(decl) + math.cos(la) * math.cos(decl) * math.cos(ha)
        out[k] = math.degrees(math.asin(max(-1.0, min(1.0, cz))))
    return out


def weather(g, rng, events):
    D = g.D
    base = np.array([15.6 - 12.6 * math.cos(2 * math.pi * (d.timetuple().tm_yday - 21) / 365.25) for d in g.dates])
    an = np.zeros(D)
    z = rng.normal(0, 1, D)
    for k in range(1, D):
        an[k] = 0.74 * an[k - 1] + 3.0 * z[k]
    for (a, b, delta) in events:
        for k, d in enumerate(g.dates):
            if a <= d <= b:
                an[k] += delta
    tday = base + an
    amp = 4.6 + 1.8 * np.array([math.sin(math.pi * (d.timetuple().tm_yday - 80) / 365.25) ** 2 for d in g.dates])
    tday_h = tday[g.day]
    amp_h = amp[g.day]
    diurnal = np.cos(2 * math.pi * (g.hod - 15) / 24.0)
    T = tday_h + amp_h * diurnal + rng.normal(0, 0.6, g.H)
    clear = np.clip(rng.beta(3.2, 1.5, D), 0.08, 1.0)
    for (a, b, delta) in events:
        if delta < -6:
            for k, d in enumerate(g.dates):
                if a <= d <= b:
                    clear[k] = min(clear[k], 0.2)
    return T, tday, clear


EVENTS = [
    (dt.date(2024, 1, 13), dt.date(2024, 1, 17), -13.0),
    (dt.date(2024, 8, 14), dt.date(2024, 8, 24), 4.6),
    (dt.date(2025, 2, 17), dt.date(2025, 2, 21), -9.0),
    (dt.date(2025, 7, 19), dt.date(2025, 7, 31), 4.8),
    (dt.date(2026, 1, 22), dt.date(2026, 2, 2), -8.5),
    (dt.date(2026, 8, 4), dt.date(2026, 8, 14), 4.4),
]
EVENTS_2019 = [(dt.date(2019, 1, 29), dt.date(2019, 2, 2), -9.0), (dt.date(2019, 7, 17), dt.date(2019, 7, 26), 4.5)]


# ---------------------------------------------------------------------------------------------------------------
# hourly load shapes per unit (mean 1 over the reference year)
# ---------------------------------------------------------------------------------------------------------------

CLASSES = ["RES", "RESE", "SC", "POULTRY", "SAWMILL", "HOSPITAL", "SCHOOL", "WATER", "RETAIL", "COLDSTORE", "GROW",
           "THEFT"]
PF = {"RES": 0.96, "RESE": 0.95, "SC": 0.92, "POULTRY": 0.88, "SAWMILL": 0.85, "HOSPITAL": 0.92, "SCHOOL": 0.93,
      "WATER": 0.87, "RETAIL": 0.93, "COLDSTORE": 0.87, "GROW": 0.94, "THEFT": 0.93, "LIGHT_HPS": 0.92,
      "LIGHT_LED": 0.98}


def shapes(g, T, ref_mask):
    h, dw, m = g.hod.astype(float), g.dow, g.month
    wk = dw < 5
    cool = np.clip(T - 21.0, 0, None)
    heat = np.clip(14.0 - T, 0, None)
    out = {}
    diur = (0.62 + 0.18 * np.exp(-((h - 7.5) ** 2) / 3.0) + 0.42 * np.exp(-((h - 19.5) ** 2) / 6.0)
            - 0.20 * np.exp(-((h - 3.5) ** 2) / 4.0))
    out["RES"] = diur + 0.060 * cool ** 1.15 * (0.6 + 0.4 * np.exp(-((h - 17) ** 2) / 18.0)) + 0.010 * heat
    out["RESE"] = diur + 0.055 * cool ** 1.15 * (0.6 + 0.4 * np.exp(-((h - 17) ** 2) / 18.0)) + 0.062 * heat * (
        0.8 + 0.2 * np.exp(-((h - 7) ** 2) / 8.0))
    bus = ((h >= 8) & (h < 18) & wk).astype(float)
    out["SC"] = 0.48 + 0.95 * bus + 0.25 * ((h >= 7) & (h < 20)).astype(float) + 0.045 * cool + 0.012 * heat
    shift = (((h >= 5) & (h < 22)) & (dw < 6)).astype(float)
    out["POULTRY"] = 0.55 + 0.62 * shift + 0.012 * cool
    out["SAWMILL"] = 0.22 + 1.35 * (((h >= 6) & (h < 17)) & wk).astype(float) + 0.25 * ((dw == 5) & (h >= 6) & (h < 12))
    out["HOSPITAL"] = 0.84 + 0.18 * ((h >= 7) & (h < 19)).astype(float) + 0.020 * cool + 0.006 * heat
    summer = ((m >= 6) & (m <= 7)).astype(float)
    out["SCHOOL"] = (0.30 + 1.25 * (((h >= 7) & (h < 16)) & wk).astype(float) * (1 - 0.75 * summer)
                     + 0.020 * cool * (1 - 0.5 * summer))
    out["WATER"] = 0.88 + 0.22 * np.exp(-((h - 6.5) ** 2) / 4.0) + 0.25 * np.exp(-((h - 19) ** 2) / 6.0) + 0.006 * cool
    out["RETAIL"] = 0.45 + 0.85 * ((h >= 7) & (h < 22)).astype(float) + 0.030 * cool + 0.006 * heat
    out["COLDSTORE"] = 0.93 + 0.012 * np.clip(T - 10.0, 0, None) + 0.05 * ((h >= 6) & (h < 18) & wk).astype(float)
    # licensed grows: flower rooms on 12/12 from 07:00, veg rooms on 18/6 from 05:00, cooling all day
    lights = 0.50 * ((h >= 7) & (h < 19)).astype(float) + 0.30 * ((h >= 5) | (h < 23)).astype(float) * (
        (h >= 5) & (h < 23)).astype(float)
    out["GROW"] = 0.42 + lights + 0.010 * np.clip(T - 16.0, 0, None)
    tl = 0.70 * (((h >= 20) | (h < 8))).astype(float)   # illegal grows light at night, when no one looks
    out["THEFT"] = 0.40 + tl + 0.008 * np.clip(T - 16.0, 0, None)
    for c in out:
        out[c] = out[c] / out[c][ref_mask].mean()
    return out


# ---------------------------------------------------------------------------------------------------------------
# the network
# ---------------------------------------------------------------------------------------------------------------

class Net:
    def __init__(self):
        self.nodes = []            # node ids
        self.node_feeder = {}      # home feeder (as built)
        self.node_pos = {}         # miles from the home breaker along the home path
        self.seg = []              # dicts: id, a, b, mi, cond, phasing, feeder, year
        self.sw = []               # dicts: id, a, b, kind, normal, feeder, pole_tag, legacy
        self.adj = defaultdict(list)
        self.breaker = {}          # feeder -> breaker node
        self.trunk = {}            # feeder -> list of trunk nodes in order from the breaker
        self.laterals = defaultdict(list)


def _node_id(rng, used):
    while True:
        x = "N%06d" % rng.integers(100000, 999999)
        if x not in used:
            used.add(x)
            return x


def build_network(rng):
    net = Net()
    used = set()
    seg_used = set()

    def seg_id(kind):
        while True:
            x = "%s-%06d" % (kind, rng.integers(100000, 999999))
            if x not in seg_used:
                seg_used.add(x)
                return x

    for f in P.FEEDER_ORDER:
        spec = P.FEEDERS[f]
        bkr = "BKR-" + f
        net.breaker[f] = bkr
        net.nodes.append(bkr)
        net.node_feeder[bkr] = f
        net.node_pos[bkr] = 0.0
        n_t = max(6, int(round(spec["trunk_mi"] / 0.55)))
        L = rng.uniform(0.6, 1.4, n_t)
        L = L / L.sum() * spec["trunk_mi"]
        prev, pos = bkr, 0.0
        trunk = []
        for k in range(n_t):
            nd = _node_id(rng, used)
            pos += L[k]
            cond = spec["trunk"]
            if f == "APT-4" and pos > 16.0:
                cond = "2/0 ACSR"
            if f in ("NTH-3", "IND-3") and pos > 10.5:
                cond = "1/0 ACSR"
            if f == "CHL-2" and pos > 14.0:
                cond = "2/0 ACSR"
            yr = int(rng.choice([1971, 1978, 1984, 1991, 1998, 2006, 2013]))
            s = dict(id=seg_id("OH"), a=prev, b=nd, mi=float(L[k]), cond=cond, phasing="ABC", feeder=f, year=yr)
            net.seg.append(s)
            net.adj[prev].append(("seg", len(net.seg) - 1))
            net.adj[nd].append(("seg", len(net.seg) - 1))
            net.nodes.append(nd)
            net.node_feeder[nd] = f
            net.node_pos[nd] = pos
            trunk.append(nd)
            prev = nd
        net.trunk[f] = trunk
        # laterals
        town = spec["kind"] != "rural"
        p_lat = 0.85 if town else 0.62
        for k, tn in enumerate(trunk):
            if rng.random() > p_lat:
                continue
            nlat = int(rng.integers(1, 3)) if town else 1
            for _ in range(nlat):
                n_l = int(rng.integers(3, 8)) if town else int(rng.integers(2, 7))
                three = rng.random() < (0.28 if town else 0.18)
                urd = town and rng.random() < 0.30
                if three:
                    cond = "1/0 ACSR"
                    ph = "ABC"
                elif urd:
                    cond = "1/0 AL URD"
                    ph = str(rng.choice(["A", "B", "C"]))
                else:
                    cond = str(rng.choice(["#2 ACSR", "#4 ACSR"], p=[0.6, 0.4]))
                    ph = str(rng.choice(["A", "B", "C"]))
                par, ppos = tn, net.node_pos[tn]
                lat_nodes = []
                for j in range(n_l):
                    nd = _node_id(rng, used)
                    mi = float(rng.uniform(0.05, 0.16) if town else rng.uniform(0.15, 0.55))
                    ppos += mi
                    s = dict(id=seg_id("UG" if urd else "OH"), a=par, b=nd, mi=mi, cond=cond, phasing=ph, feeder=f,
                             year=int(rng.choice([1975, 1983, 1990, 1997, 2004, 2011, 2018])))
                    net.seg.append(s)
                    net.adj[par].append(("seg", len(net.seg) - 1))
                    net.adj[nd].append(("seg", len(net.seg) - 1))
                    net.nodes.append(nd)
                    net.node_feeder[nd] = f
                    net.node_pos[nd] = ppos
                    lat_nodes.append(nd)
                    par = nd
                net.laterals[f].append(dict(tap=tn, nodes=lat_nodes, cond=cond, ph=ph, three=three))
    return net


def add_switch(net, rng, a, b, kind, normal, feeder, used_poles, year=2009):
    while True:
        tag = "%s%d-%d" % (feeder[0], int(feeder[-1]), int(rng.integers(100, 999)))
        if tag not in used_poles:
            used_poles.add(tag)
            break
    sid = "SW-%05d" % int(rng.integers(10000, 99999))
    while any(s["id"] == sid for s in net.sw):
        sid = "SW-%05d" % int(rng.integers(10000, 99999))
    net.sw.append(dict(id=sid, a=a, b=b, kind=kind, normal=normal, feeder=feeder, pole_tag=tag, year=year))
    k = len(net.sw) - 1
    net.adj[a].append(("sw", k))
    net.adj[b].append(("sw", k))
    return k


def insert_tap_switch(net, lateral):
    """A normally closed cutout or sectionalizer at a lateral's tap: the first lateral segment is re-pointed to a new
    node, and the switch joins the trunk node to it."""
    first = lateral["nodes"][0]
    tap = lateral["tap"]
    # find the segment tap -> first
    for k, s in enumerate(net.seg):
        if (s["a"] == tap and s["b"] == first) or (s["b"] == tap and s["a"] == first):
            return k, tap, first
    raise RuntimeError("no tap segment")


def split_segment_with_switch(net, rng, seg_index, used_poles, kind, normal, feeder):
    """Put a switch on a segment: the segment's upstream end moves to a new pole node joined to the old end by the
    switch."""
    s = net.seg[seg_index]
    a, b = s["a"], s["b"]
    nd = "S" + s["id"][-6:]
    net.nodes.append(nd)
    net.node_feeder[nd] = net.node_feeder[a]
    net.node_pos[nd] = net.node_pos[a]
    # rewire: a -[switch]- nd -[segment]- b
    net.adj[a] = [x for x in net.adj[a] if x != ("seg", seg_index)]
    s["a"] = nd
    net.adj[nd].append(("seg", seg_index))
    return add_switch(net, rng, a, nd, kind, normal, feeder, used_poles)


# ---------------------------------------------------------------------------------------------------------------
# the world
# ---------------------------------------------------------------------------------------------------------------

def build(seed=P.SEED):
    rng = np.random.default_rng(seed)
    w = W()
    w.g = g = time_grid(P.START_LOCAL, P.END_LOCAL)
    ref = np.array([(dt.date(2024, 10, 1) <= x.date() < dt.date(2025, 10, 1)) for x in g.loc])
    w.T, w.Tday, w.clear = weather(g, np.random.default_rng(seed + 10), EVENTS)
    w.elev = solar_elevation(g.utc, P.LAT, P.LON)
    w.u = shapes(g, w.T, ref)
    w.dayU = {c: np.bincount(g.day, weights=w.u[c], minlength=g.D) for c in w.u}

    net = w.net = build_network(rng)
    used_poles = set()
    # sectionalizing reclosers on each trunk
    for f in P.FEEDER_ORDER:
        tr = net.trunk[f]
        for frac in (0.35, 0.7):
            k = int(len(tr) * frac)
            idx = next(i for i, s in enumerate(net.seg) if s["b"] == tr[k] and s["feeder"] == f)
            split_segment_with_switch(net, rng, idx, used_poles, "Recloser", "Closed", f)

    customers, xfmrs = place_customers(w, rng, used_poles)
    w.cust, w.xfmrs = customers, xfmrs
    # each component draws from its own stream, so a change in one never reshuffles another
    w.lp = place_large_power(w, np.random.default_rng(seed + 11))
    place_transfers(w, np.random.default_rng(seed + 12), used_poles)
    w.lights = place_lights(w, np.random.default_rng(seed + 13))
    w.theft = place_theft(w, np.random.default_rng(seed + 14))
    w.ops = switching_operations(w, np.random.default_rng(seed + 15))
    w.outages = outage_events(w, np.random.default_rng(seed + 16))
    customer_daily(w, np.random.default_rng(seed + 17))
    hourly_flows(w)
    return w


def _pick(rng, seq):
    return seq[int(rng.integers(0, len(seq)))]


def place_customers(w, rng, used_poles):
    """Residential and small commercial customers on transformers at lateral and trunk nodes; their average load,
    electric heat, PV, meter and account history."""
    net = w.net
    cust, xf = [], []
    used = set()

    def new_xfmr(node, kva, kind, f, install, mfg):
        while True:
            x = "T-%05d" % int(rng.integers(10000, 99999))
            if x not in used:
                used.add(x)
                break
        xf.append(dict(id=x, node=node, kva=kva, kind=kind, feeder=f, install=install, removed=None, mfg=mfg))
        return len(xf) - 1

    sp_used = set()

    def sp_id():
        while True:
            x = "%07d" % int(rng.integers(1000000, 9999999))
            if x not in sp_used:
                sp_used.add(x)
                return x

    for f in P.FEEDER_ORDER:
        spec = P.FEEDERS[f]
        town = spec["kind"] != "rural"
        lat_nodes = [n for L in net.laterals[f] for n in L["nodes"]]
        trunk = net.trunk[f]
        # residential on laterals, a few on the trunk
        per_x = (4, 9) if town else (1, 3)
        n_res = spec["res"]
        k = 0
        nodes_cycle = list(lat_nodes) + list(trunk[1:])
        rng.shuffle(nodes_cycle)
        ni = 0
        while k < n_res:
            node = nodes_cycle[ni % len(nodes_cycle)]
            ni += 1
            m = int(rng.integers(per_x[0], per_x[1] + 1))
            m = min(m, n_res - k)
            kva = float(rng.choice([25, 37.5, 50] if town else [10, 15, 25], p=[0.45, 0.35, 0.2]))
            mfg = int(rng.choice([1988, 1994, 1999, 2004, 2008, 2012, 2016, 2019, 2022],
                                 p=[0.08, 0.1, 0.12, 0.14, 0.14, 0.14, 0.12, 0.1, 0.06]))
            xi = new_xfmr(node, kva, "Pole", f, dt.date(max(mfg, 1990), 1, 1), mfg)
            for _ in range(m):
                eh = rng.random() < spec["eheat"]
                cls = "RESE" if eh else "RES"
                mean = (1.55 if eh else 1.22) * (1.10 if not town else 1.0)
                a = float(rng.lognormal(math.log(mean) - 0.09, 0.42))
                cust.append(dict(sp=sp_id(), feeder=f, node=node, xf=xi, cls=cls, a=a, rate="RS" if not eh else "RS-E"))
                k += 1
        # small commercial on the trunk and laterals, on pad-mounts or pole banks
        for j in range(spec["sc"]):
            node = _pick(rng, trunk[1:] if rng.random() < 0.65 else lat_nodes)
            a = float(rng.lognormal(math.log(4.6), 0.75))
            kva = 75.0 if a < 8 else (100.0 if a < 14 else 167.0)
            mfg = int(rng.choice([1996, 2003, 2009, 2014, 2018, 2021]))
            xi = new_xfmr(node, kva, "Pad" if town else "Pole", f, dt.date(max(mfg, 1996), 3, 1), mfg)
            cust.append(dict(sp=sp_id(), feeder=f, node=node, xf=xi, cls="SC", a=a, rate="GS"))
    # history: connection dates (new service points), PV, meter exchange, accounts
    # the AMI rollout dates draw from their own stream, so the schedule never reshuffles the customers
    ami_rng = np.random.default_rng(P.SEED + 19)
    for c in cust:
        f = c["feeder"]
        spec = P.FEEDERS[f]
        town = spec["kind"] != "rural"
        r = rng.random()
        if r < (0.035 if town else 0.025):
            c["start"] = dt.date(2023, 10, 1) + dt.timedelta(days=int(rng.integers(30, 1080)))
        else:
            c["start"] = None
        c["pv_kw"], c["pv_date"] = 0.0, None
        if c["cls"] != "SC" and rng.random() < spec["pv"]:
            c["pv_kw"] = float(np.round(rng.uniform(4.8, 11.5), 2))
            yr = int(rng.choice([2018, 2020, 2021, 2022, 2023, 2024, 2025, 2026], p=[0.05, 0.07, 0.09, 0.13, 0.16,
                                                                                        0.2, 0.2, 0.1]))
            mo = int(rng.integers(1, 13)) if yr < 2026 else int(rng.integers(1, 10))
            c["pv_date"] = dt.date(yr, mo, int(rng.integers(1, 28)))
        ami = spec["ami"]
        off = int(ami_rng.integers(-20, 40))
        c["ami_date"] = None if ami is None else dt.date(ami[0], ami[1], 1) + dt.timedelta(days=off)
        c["slow"] = float(np.clip(rng.normal(0.986, 0.008), 0.95, 1.004))
        if rng.random() < 0.018:
            c["slow"] = float(rng.uniform(0.80, 0.93))
        c["cycle"] = int(rng.integers(1, 21))
        c["tamper"] = None
        if c["cls"] == "SC" and rng.random() < 0.035:
            s0 = dt.date(2023, 12, 1) + dt.timedelta(days=int(rng.integers(0, 900)))
            c["tamper"] = (s0, s0 + dt.timedelta(days=int(rng.integers(120, 400))), float(rng.uniform(0.55, 0.8)))
        # occupants: account numbers and vacancies
        accts = []
        t0 = c["start"] or dt.date(2023, 8, 1)
        n_moves = rng.poisson(0.35 * 3)
        cuts = sorted(dt.date(2023, 9, 1) + dt.timedelta(days=int(x)) for x in rng.integers(30, 1150, n_moves))
        prev = t0
        for cdate in cuts:
            if cdate <= prev:
                continue
            accts.append((prev, cdate))
            vac = int(rng.integers(5, 70))
            prev = cdate + dt.timedelta(days=vac)
        accts.append((prev, None))
        c["accounts"] = [(a, b, "%08d" % int(rng.integers(10000000, 99999999))) for a, b in accts]
    return cust, xf


def place_large_power(w, rng):
    net = w.net
    lps = []
    for key, f, name, cls, avg, pos, en, conn, kva in P.LARGE_POWER:
        tr = net.trunk[f]
        node = tr[min(len(tr) - 1, int(round(pos * (len(tr) - 1))))]
        en_date = dt.date(en[0], en[1], int(rng.integers(3, 25))) if en else None
        if key in P.LP_2019_TO_2023:
            hist = dt.date(P.LP_2019_TO_2023[key], int(rng.integers(2, 11)), int(rng.integers(1, 27)))
        elif key in P.LP_BEFORE_2019:
            hist = dt.date(int(rng.integers(1995, 2016)), int(rng.integers(1, 12)), 1)
        else:
            hist = en_date
        mfg = max(2005, hist.year)
        xi = len(w.xfmrs)
        w.xfmrs.append(dict(id="T-%05d" % int(rng.integers(10000, 99999)), node=node, kva=float(kva), kind="Pad",
                            feeder=f, install=hist, removed=None, mfg=mfg))
        lps.append(dict(key=key, feeder=f, name=name, cls=cls, a=float(avg), node=node, start=en_date, energized=hist,
                        conn_kw=float(conn), xf=xi, sp="%07d" % int(rng.integers(1000000, 9999999)),
                        meter="LP%06d" % int(rng.integers(100000, 999999))))
    # a grow's transformer changed out for a larger one when it expanded (the register keeps both)
    for lp in lps:
        if lp["key"] in ("LP18", "LP22"):
            x = w.xfmrs[lp["xf"]]
            old = dict(x)
            old["id"] = "T-%05d" % int(rng.integers(10000, 99999))
            old["kva"] = 300.0
            old["removed"] = dt.date(2024, 9, 12) if lp["key"] == "LP18" else dt.date(2025, 4, 3)
            x["install"] = old["removed"]
            x["mfg"] = old["removed"].year
            w.xfmrs.append(old)
    return lps


def place_transfers(w, rng, used_poles):
    """The laterals and sections the switching log moves: each permanent or temporary transfer gets a lateral (or a
    trunk section) of the stated size on its home feeder, a normally closed switch at its tap and a tie to the
    receiving feeder; the GIS (today's view) shows permanent transfers on the receiving feeder."""
    net = w.net
    w.transfer_sw = {}
    for T in P.TRANSFERS:
        f, g2 = T["frm"], T["to"]
        target = T["cust"]
        # choose the lateral whose customer count is nearest the target
        counts = []
        for i, L in enumerate(net.laterals[f]):
            n = sum(1 for c in w.cust if c["node"] in set(L["nodes"]))
            counts.append((abs(n - target), i, n))
        counts.sort()
        _, li, n = counts[0]
        L = net.laterals[f][li]
        # move customers in or out so the lateral carries exactly the target
        lat_set = set(L["nodes"])
        on = [c for c in w.cust if c["node"] in lat_set and c["cls"] != "SC"]
        off = [c for c in w.cust if c["feeder"] == f and c["node"] not in lat_set and c["cls"] != "SC"]
        while len(on) + sum(1 for c in w.cust if c["node"] in lat_set and c["cls"] == "SC") > target and on:
            c = on.pop()
            c["node"] = _pick(rng, net.trunk[f][1:])
        while sum(1 for c in w.cust if c["node"] in lat_set) < target and off:
            c = off.pop()
            c["node"] = _pick(rng, L["nodes"])
            w.xfmrs[c["xf"]]["node"] = c["node"]
        k_tap, tap, first = insert_tap_switch(net, L)
        sw_tap = split_segment_with_switch(net, rng, k_tap, used_poles, "Sectionalizer", "Closed", f)
        # tie from the lateral's last node to the nearest trunk node of the receiving feeder
        tgt = _pick(rng, net.trunk[g2][2:6])
        sw_tie = add_switch(net, rng, L["nodes"][-1], tgt, "Tie", "Open", f, used_poles)
        # the tie's span (a short segment on the receiving side)
        L["transfer"] = T["key"]
        w.transfer_sw[T["key"]] = dict(tap=sw_tap, tie=sw_tie, lateral=li, feeder=f, to=g2)
        if T["end"] is None:
            # the GIS holds today's normal state: a permanent transfer's tap open and its tie closed
            net.sw[sw_tap]["normal"] = "Open"
            net.sw[sw_tie]["normal"] = "Closed"
    # the ice storm: a sectionalizer about 1.2 miles out on CHL-2's trunk and a tie from CHL-2's far end to CHL-3
    tr = net.trunk["CHL-2"]
    k = next(i for i, nd in enumerate(tr) if net.node_pos[nd] > 1.1)
    idx = next(i for i, s in enumerate(net.seg) if s["b"] == tr[k] and s["feeder"] == "CHL-2")
    sw_sec = split_segment_with_switch(net, rng, idx, used_poles, "Sectionalizer", "Closed", "CHL-2")
    tgt = net.trunk["CHL-3"][int(len(net.trunk["CHL-3"]) * 0.55)]
    sw_tie = add_switch(net, rng, tr[-1], tgt, "Tie", "Open", "CHL-2", used_poles)
    w.storm_sw = dict(sec=sw_sec, tie=sw_tie, first_nodes=set(tr[:k]))
    # first section's customers are exactly the stated count
    first_nodes = set(tr[:k])
    near = [c for c in w.cust if c["feeder"] == "CHL-2" and c["node"] in first_nodes]
    far = [c for c in w.cust if c["feeder"] == "CHL-2" and c["node"] not in first_nodes and c["cls"] != "SC"]
    while len(near) < P.STORM["first_section_customers"] and far:
        c = far.pop()
        c["node"] = _pick(rng, tr[:k])
        w.xfmrs[c["xf"]]["node"] = c["node"]
        near.append(c)
    # a few more ties with no transfer (texture in the GIS)
    for f in P.FEEDER_ORDER:
        sub = P.FEEDERS[f]["sub"]
        others = [x for x in P.SUB_FEEDERS[sub] if x != f]
        if others and rng.random() < 0.7:
            add_switch(net, rng, net.trunk[f][-1], _pick(rng, net.trunk[_pick(rng, others)][3:]), "Tie", "Open", f,
                       used_poles)


def place_lights(w, rng):
    net = w.net
    lights = []
    for f in P.FEEDER_ORDER:
        town = P.FEEDERS[f]["kind"] != "rural"
        nodes = [n for L in net.laterals[f] for n in L["nodes"]] + net.trunk[f]
        n_street = int(sum(1 for c in w.cust if c["feeder"] == f) * (0.26 if town else 0.03))
        n_area = int(sum(1 for c in w.cust if c["feeder"] == f) * (0.03 if town else 0.17))
        for j in range(n_street):
            lamp = str(rng.choice(["HPS100", "HPS150", "HPS250"], p=[0.58, 0.27, 0.15]))
            lights.append(dict(kind="Street", feeder=f, node=_pick(rng, nodes), lamp=lamp,
                               install=dt.date(int(rng.integers(1992, 2019)), int(rng.integers(1, 13)), 1)))
        for j in range(n_area):
            lamp = str(rng.choice(["MV175", "HPS100"], p=[0.38, 0.62]))
            lights.append(dict(kind="Area", feeder=f, node=_pick(rng, nodes), lamp=lamp,
                               install=dt.date(int(rng.integers(1985, 2020)), int(rng.integers(1, 13)), 1)))
    # the LED programme: street lights district by district, area lights on failure; billing updated or not
    order = ["IND-2", "NTH-1", "APT-1", "CHL-1", "NTH-2", "APT-2", "IND-1", "NTH-3", "IND-3", "CHL-3", "NTH-4",
             "APT-3", "CHL-2", "APT-4"]
    start = dt.date(2024, 3, 1)
    for L in lights:
        L["led"], L["billed_led"] = None, None
        if L["kind"] == "Street":
            k = order.index(L["feeder"])
            d = start + dt.timedelta(days=int(k * 68 + rng.integers(0, 60)))
            if d < dt.date(2026, 9, 1) and rng.random() < 0.92:
                L["led"] = d
                # the lighting bill followed the programme's first districts; after the summer of 2024 the
                # conversions mostly stayed on the old lamp codes
                if d < dt.date(2024, 8, 1):
                    L["billed_led"] = d + dt.timedelta(days=int(rng.integers(20, 110)))
                elif rng.random() < 0.28:
                    L["billed_led"] = d + dt.timedelta(days=int(rng.integers(25, 140)))
        else:
            if rng.random() < 0.30:
                d = dt.date(2023, 10, 1) + dt.timedelta(days=int(rng.integers(0, 1080)))
                L["led"] = d
                if rng.random() < 0.82:
                    L["billed_led"] = d + dt.timedelta(days=int(rng.integers(5, 45)))
        if L["billed_led"] and L["billed_led"] >= dt.date(2026, 11, 1):
            L["billed_led"] = None
        L["id"] = "L%05d" % int(rng.integers(10000, 99999))
    return lights


def place_theft(w, rng):
    net = w.net
    th = []
    for f in P.FEEDER_ORDER:
        n, kw = P.FEEDERS[f]["theft"]
        res = [c for c in w.cust if c["feeder"] == f and c["cls"] in ("RES", "RESE")]
        # rural grows sit further out
        res.sort(key=lambda c: -net.node_pos[c["node"]])
        pool = res[: max(n * 3, int(len(res) * 0.6))]
        for j in range(n):
            c = pool[int(rng.integers(0, len(pool)))]
            s = dt.date(2023, 5, 1) + dt.timedelta(days=int(rng.integers(0, 1030)))
            e = None
            if rng.random() < 0.22:
                e = s + dt.timedelta(days=int(rng.integers(120, 500)))
            th.append(dict(feeder=f, node=c["node"], sp=c["sp"], kw=float(rng.lognormal(math.log(kw) - 0.05, 0.32)),
                           start=s, end=e))
    # scale each feeder's sites to its stolen energy in the twelve months to September 2026
    g = w.g
    m26 = (g.dord >= P.WIN26[0].toordinal()) & (g.dord < P.WIN26[1].toordinal())
    for f in P.FEEDER_ORDER:
        sites = [t for t in th if t["feeder"] == f]
        e = sum(t["kw"] * (w.u["THEFT"] * ((g.dord >= t["start"].toordinal()) & (
            (g.dord < t["end"].toordinal()) if t["end"] else True)))[m26].sum() for t in sites) / 1000.0
        if e > 0:
            k = P.THEFT_TARGET[f] / e
            for t in sites:
                t["kw"] *= k
    return th


def switching_operations(w, rng):
    """Every switch operation (local time): the transfers, the storm and planned maintenance on cutouts and
    sectionalizers; each one with the device, OPEN or CLOSE and the reason."""
    ops = []
    for T in P.TRANSFERS:
        s = w.transfer_sw[T["key"]]
        t = T["start"].replace(tzinfo=P.TZ)
        ops.append(dict(t=t, sw=s["tie"], op="CLOSE", reason=T["reason"]))
        ops.append(dict(t=t + dt.timedelta(minutes=4), sw=s["tap"], op="OPEN", reason=T["reason"]))
        if T["end"]:
            e = T["end"].replace(tzinfo=P.TZ)
            ops.append(dict(t=e, sw=s["tap"], op="CLOSE", reason=T["reason"]))
            ops.append(dict(t=e + dt.timedelta(minutes=3), sw=s["tie"], op="OPEN", reason=T["reason"]))
    S = P.STORM
    ops.append(dict(t=S["tie_close"].replace(tzinfo=P.TZ) - dt.timedelta(minutes=12), sw=w.storm_sw["sec"], op="OPEN",
                    reason="Storm restoration"))
    ops.append(dict(t=S["tie_close"].replace(tzinfo=P.TZ), sw=w.storm_sw["tie"], op="CLOSE", reason="Storm restoration"))
    ops.append(dict(t=S["repair"].replace(tzinfo=P.TZ), sw=w.storm_sw["tie"], op="OPEN", reason="Storm restoration"))
    ops.append(dict(t=S["repair"].replace(tzinfo=P.TZ) + dt.timedelta(minutes=6), sw=w.storm_sw["sec"], op="CLOSE",
                    reason="Storm restoration"))
    # planned maintenance: open a recloser or sectionalizer for a few hours and close it again (customers out)
    special = {v for T in w.transfer_sw.values() for v in (T["tap"], T["tie"])} | {w.storm_sw["sec"], w.storm_sw["tie"]}
    cand = [k for k, s in enumerate(w.net.sw) if s["normal"] == "Closed" and k not in special]
    t = P.START_LOCAL + dt.timedelta(days=9)
    while t < P.END_LOCAL - dt.timedelta(days=5):
        t = t + dt.timedelta(days=int(rng.integers(6, 22)))
        if t.weekday() >= 5:
            continue
        k = cand[int(rng.integers(0, len(cand)))]
        t0 = t.replace(hour=int(rng.integers(8, 13)), minute=int(rng.integers(0, 60)))
        dur = dt.timedelta(minutes=int(rng.integers(70, 300)))
        if t0 + dur >= P.END_LOCAL - dt.timedelta(days=1):
            break
        ops.append(dict(t=t0, sw=k, op="OPEN", reason="Planned maintenance"))
        ops.append(dict(t=t0 + dur, sw=k, op="CLOSE", reason="Planned maintenance"))
    ops.sort(key=lambda o: (o["t"], o["sw"]))
    return ops


def outage_events(w, rng):
    """Unplanned outages on taps and transformers (the OMS outage record, a file no balance needs): customers out
    for an hour or a day; and the storm's."""
    out = []
    nodes = [n for n in w.net.nodes if not n.startswith("BKR")]
    t = P.START_LOCAL
    while t < P.END_LOCAL - dt.timedelta(days=2):
        t = t + dt.timedelta(hours=float(rng.exponential(31)))
        n = nodes[int(rng.integers(0, len(nodes)))]
        dur = float(rng.lognormal(math.log(1.6), 0.8))
        cause = str(rng.choice(["Vegetation", "Animal", "Equipment failure", "Lightning", "Vehicle", "Unknown"],
                               p=[0.27, 0.18, 0.22, 0.14, 0.05, 0.14]))
        out.append(dict(start=t, end=t + dt.timedelta(hours=dur), node=n, cause=cause, storm=False))
    return out


# ---------------------------------------------------------------------------------------------------------------
# customer energies, day by day
# ---------------------------------------------------------------------------------------------------------------

def customer_daily(w, rng):
    g = w.g
    D = g.D
    n = len(w.cust)
    sig = np.array([0.13 if c["cls"] != "SC" else 0.09 for c in w.cust])
    z = rng.normal(0, 1, (n, D))
    e = np.zeros((n, D))
    for k in range(1, D):
        e[:, k] = 0.72 * e[:, k - 1] + sig * z[:, k]
    fac = np.exp(e - 0.5 * (sig ** 2 / (1 - 0.72 ** 2))[:, None])
    E = np.zeros((n, D), dtype=np.float64)
    for i, c in enumerate(w.cust):
        active = np.ones(D)
        if c["start"]:
            active[: (c["start"] - g.d0).days] = 0.0
        # vacancies between accounts draw a fifth of the load
        for (a, b, _), (a2, _, _) in zip(c["accounts"][:-1], c["accounts"][1:]):
            i0, i1 = max(0, (b - g.d0).days), max(0, (a2 - g.d0).days)
            active[i0:i1] *= 0.2
        E[i] = c["a"] * fac[i] * active * w.dayU[c["cls"]]
    w.E = E   # kWh per customer per day consumed (before outages)


def lp_hourly(w, lp):
    g = w.g
    x = lp["a"] * w.u[lp["cls"]].copy()
    if lp["start"]:
        x[g.dord < lp["start"].toordinal()] = 0.0
    # each plant has its own small hour-to-hour noise
    r = np.random.default_rng(zlib.crc32(lp["key"].encode()))
    x = x * np.exp(r.normal(0, 0.05, g.H))
    return x


def theft_hourly(w, t):
    g = w.g
    on = (g.dord >= t["start"].toordinal()) & ((g.dord < t["end"].toordinal()) if t["end"] else True)
    return t["kw"] * w.u["THEFT"] * on


def pv_hourly(w, kw, date0):
    g = w.g
    el = np.clip(np.sin(np.radians(w.elev)), 0, None)
    gen = kw * 0.78 * el ** 1.15 * (0.25 + 0.75 * w.clear[g.day])
    if date0:
        gen[g.dord < date0.toordinal()] = 0.0
    return gen


def light_hourly_watts(w, L):
    g = w.g
    dark = (w.elev < -0.8).astype(float)
    led = L["led"]
    w_old = P.INPUT_W[L["lamp"]]
    w_new = P.INPUT_W[P.LED_FOR[L["lamp"]]]
    if led is None:
        return dark * w_old
    after = g.dord >= led.toordinal()
    return dark * np.where(after, w_new, w_old)


# ---------------------------------------------------------------------------------------------------------------
# hourly flows and losses
# ---------------------------------------------------------------------------------------------------------------

def hour_index(w, t_local):
    u = t_local.astimezone(UTC)
    return int((u - w.g.utc[0]).total_seconds() // 3600)


def switch_states(w):
    """Epochs of constant switch state: (h0, h1, state list)."""
    base = [s["normal"] == "Closed" for s in w.net.sw]
    # the GIS shows today's view: permanent transfers already applied; the history starts before them
    state = list(base)
    for T in P.TRANSFERS:
        if T["end"] is None:
            s = w.transfer_sw[T["key"]]
            state[s["tap"]] = True     # before the transfer the tap was closed
            state[s["tie"]] = False
    events = defaultdict(list)
    for o in w.ops:
        events[max(0, hour_index(w, o["t"]))].append(o)
    epochs = []
    h0 = 0
    cur = list(state)
    for h in sorted(events):
        if h > h0:
            epochs.append((h0, h, list(cur)))
        for o in events[h]:
            cur[o["sw"]] = o["op"] == "CLOSE"
        h0 = h
    epochs.append((h0, w.g.H, list(cur)))
    return epochs, state


def trees(w, closed):
    """Each feeder's radial tree under a switch state: BFS from the breaker through segments and closed switches.
    Returns {feeder: (order, parent_seg, parent_node)}; the storm's open breaker is handled by the caller."""
    net = w.net
    seen = {}
    out = {}
    for f in P.FEEDER_ORDER:
        root = net.breaker[f]
        q = deque([root])
        seen[root] = f
        order, pseg, pnode = [root], {root: None}, {root: None}
        while q:
            u = q.popleft()
            for kind, k in net.adj[u]:
                if kind == "sw" and not closed[k]:
                    continue
                if kind == "seg":
                    s = net.seg[k]
                    v = s["b"] if s["a"] == u else s["a"]
                else:
                    s = net.sw[k]
                    v = s["b"] if s["a"] == u else s["a"]
                if v in seen or v.startswith("BKR"):
                    continue
                seen[v] = f
                pseg[v] = (kind, k)
                pnode[v] = u
                order.append(v)
                q.append(v)
        out[f] = (order, pseg, pnode)
    return out


def hourly_flows(w):
    """Node loads, flows and losses substation by substation (every tie and transfer is inside one substation)."""
    g = w.g
    net = w.net
    H = g.H
    dord = g.dord
    out_mask = defaultdict(list)
    for o in w.outages:
        h0, h1 = hour_index(w, o["start"]), hour_index(w, o["end"]) + 1
        out_mask[o["node"]].append((max(0, h0), min(H, h1)))
    epochs, w.state_before = switch_states(w)
    w.epochs = epochs
    w.ep_trees = [trees(w, closed) for (_, _, closed) in epochs]
    # a node no breaker reaches (a recloser opened for maintenance) is out for those hours
    all_nodes = set(net.nodes)
    w.deen = defaultdict(list)
    for ei, (h0, h1, _) in enumerate(epochs):
        inside = set(n for f, (order, _, _) in w.ep_trees[ei].items() for n in order)
        for n in sorted(all_nodes - inside):
            w.deen[n].append((h0, h1))
            out_mask[n].append((h0, h1))
    fault_h = hour_index(w, P.STORM["fault"].replace(tzinfo=P.TZ))
    tie_h = hour_index(w, P.STORM["tie_close"].replace(tzinfo=P.TZ))
    rep_h = hour_index(w, P.STORM["repair"].replace(tzinfo=P.TZ))
    storm_out = set(w.storm_sw["first_nodes"])
    w.storm_hours = dict(fault=fault_h, tie=tie_h, repair=rep_h)
    # the storm: CHL-2's first section out from the fault to the repair, its downstream until the tie closed
    for n in net.nodes:
        if net.node_feeder[n] == "CHL-2" and not n.startswith("BKR"):
            out_mask[n].append((fault_h, (rep_h + 1) if n in storm_out else (tie_h + 1)))
    w.out_mask = out_mask
    head_P = {f: np.zeros(H) for f in P.FEEDER_ORDER}
    head_Q = {f: np.zeros(H) for f in P.FEEDER_ORDER}
    prim = {f: np.zeros(H) for f in P.FEEDER_ORDER}
    tech = {f: np.zeros(H) for f in P.FEEDER_ORDER}
    w.xfmr_nl = {f: np.zeros(H) for f in P.FEEDER_ORDER}
    w.xfmr_ll = {f: np.zeros(H) for f in P.FEEDER_ORDER}
    w.secl = {f: np.zeros(H) for f in P.FEEDER_ORDER}
    w.pv = {}
    for i, c in enumerate(w.cust):
        if c["pv_kw"] > 0:
            w.pv[i] = pv_hourly(w, c["pv_kw"], c["pv_date"]).astype(np.float32)
    w.lp_load = {lp["key"]: lp_hourly(w, lp).astype(np.float32) for lp in w.lp}
    w.theft_load = [theft_hourly(w, t).astype(np.float32) for t in w.theft]
    for t, x in zip(w.theft, w.theft_load):
        for h0, h1 in out_mask.get(t["node"], []):
            x[h0:h1] = 0
    dark = (w.elev < -0.8)
    w.light_daily = np.zeros((len(w.lights), g.D))
    for j, L in enumerate(w.lights):
        x = light_hourly_watts(w, L) / 1000.0
        for h0, h1 in out_mask.get(L["node"], []):
            x[h0:h1] = 0
        w.light_daily[j] = np.bincount(g.day, weights=x, minlength=g.D)
    cls_list = sorted(set(c["cls"] for c in w.cust))
    share = {c: (w.u[c] / np.maximum(w.dayU[c][g.day], 1e-9)).astype(np.float32) for c in cls_list}
    for sub in P.SUBSTATIONS:
        feeders = P.SUB_FEEDERS[sub]
        nodes = [n for n in net.nodes if net.node_feeder[n] in feeders]
        nidx = {n: i for i, n in enumerate(nodes)}
        N = len(nodes)
        Pc = np.zeros((N, H), dtype=np.float32)      # metered and unmetered customer load at the node
        Qn = np.zeros((N, H), dtype=np.float32)
        for c_cls in cls_list:
            tanp = math.tan(math.acos(PF[c_cls]))
            agg = defaultdict(lambda: np.zeros(g.D))
            for i, c in enumerate(w.cust):
                if c["cls"] == c_cls and c["node"] in nidx:
                    agg[c["node"]] += w.E[i]
            for nd, e in agg.items():
                x = e[g.day].astype(np.float32) * share[c_cls]
                Pc[nidx[nd]] += x
                Qn[nidx[nd]] += x * tanp
        for i, c in enumerate(w.cust):
            if i in w.pv and c["node"] in nidx:
                Pc[nidx[c["node"]]] -= w.pv[i]
        for lp in w.lp:
            if lp["node"] in nidx:
                x = w.lp_load[lp["key"]]
                Pc[nidx[lp["node"]]] += x
                Qn[nidx[lp["node"]]] += x * math.tan(math.acos(PF[lp["cls"]]))
        for t, x in zip(w.theft, w.theft_load):
            if t["node"] in nidx:
                Pc[nidx[t["node"]]] += x
                Qn[nidx[t["node"]]] += x * math.tan(math.acos(PF["THEFT"]))
        for L in w.lights:
            if L["node"] in nidx:
                x = (light_hourly_watts(w, L) / 1000.0).astype(np.float32)
                Pc[nidx[L["node"]]] += x
                Qn[nidx[L["node"]]] += x * 0.35
        for nd, spans in out_mask.items():
            if nd in nidx:
                i = nidx[nd]
                for h0, h1 in spans:
                    Pc[i, h0:h1] = 0
                    Qn[i, h0:h1] = 0
        # transformers: core all year while in service, copper with the square of the node's load
        nl = np.zeros((N, H), dtype=np.float32)
        kva_node = defaultdict(float)
        ll_node = defaultdict(float)
        for x in w.xfmrs:
            if x["node"] not in nidx:
                continue
            a, b = P.XFMR_LOSS[x["kva"]]
            old = x["mfg"] < 2010
            a *= P.OLD_NL if old else 1.0
            b *= P.OLD_LL if old else 1.0
            on = (dord >= x["install"].toordinal())
            if x["removed"]:
                on &= dord < x["removed"].toordinal()
            nl[nidx[x["node"]]] += on.astype(np.float32) * (a / 1000.0)
            if x["removed"] is None:
                kva_node[x["node"]] += x["kva"]
                ll_node[x["node"]] += b / 1000.0
        for nd in nodes:
            i = nidx[nd]
            if nd.startswith("BKR"):
                nl[i] = 0
            for h0, h1 in out_mask.get(nd, []):
                nl[i, h0:h1] = 0
        # a node with load is out of service in an outage: no core loss either
        xl = np.zeros((N, H), dtype=np.float32)
        for nd, kva in kva_node.items():
            i = nidx[nd]
            sva = np.sqrt(np.maximum(Pc[i], 0) ** 2 + Qn[i] ** 2)
            xl[i] = ll_node[nd] * (sva / max(kva, 1.0)) ** 2
        sec = np.maximum(Pc, 0) * P.SECONDARY_SHARE
        Pn = Pc + nl + xl + sec
        for ei, (h0, h1, _) in enumerate(epochs):
            tr = w.ep_trees[ei]
            for f in feeders:
                order, pseg, pnode = tr[f]
                idx = [nidx[n] for n in order]
                Pf = Pn[idx, h0:h1].astype(np.float64)
                Qf = Qn[idx, h0:h1].astype(np.float64)
                if f == "CHL-2":
                    a, b = max(h0, fault_h), min(h1, rep_h + 1)
                    if a < b:
                        Pf[:, a - h0:b - h0] = 0
                        Qf[:, a - h0:b - h0] = 0
                pos = {n: j for j, n in enumerate(order)}
                FP, FQ = Pf.copy(), Qf.copy()
                loss_tot = np.zeros(h1 - h0)
                for j in range(len(order) - 1, 0, -1):
                    n = order[j]
                    kind, k = pseg[n]
                    lossP = 0.0
                    if kind == "seg":
                        s = net.seg[k]
                        R = s["mi"] * P.CONDUCTORS[s["cond"]][0]
                        fac = 1.0 if s["phasing"] == "ABC" else P.SINGLE_PHASE_FACTOR
                        lossP = fac * R * (FP[j] ** 2 + FQ[j] ** 2) / (P.V_KV ** 2) / 1000.0
                        loss_tot += lossP
                    pj = pos[pnode[n]]
                    FP[pj] += FP[j] + lossP
                    FQ[pj] += FQ[j]
                head_P[f][h0:h1] = FP[0]
                head_Q[f][h0:h1] = FQ[0]
                prim[f][h0:h1] = loss_tot
                w.xfmr_nl[f][h0:h1] = Pf[:, :][[pos[n] for n in order]].sum(axis=0) * 0 + nl[idx, h0:h1].sum(axis=0)
                if f == "CHL-2":
                    a, b = max(h0, fault_h), min(h1, rep_h + 1)
                    if a < b:
                        w.xfmr_nl[f][a:b] = 0
                w.xfmr_ll[f][h0:h1] = xl[idx, h0:h1].sum(axis=0)
                w.secl[f][h0:h1] = sec[idx, h0:h1].sum(axis=0)
                if f == "CHL-2":
                    a, b = max(h0, fault_h), min(h1, rep_h + 1)
                    if a < b:
                        w.xfmr_ll[f][a:b] = 0
                        w.secl[f][a:b] = 0
        del Pc, Qn, nl, xl, sec, Pn
    for f in P.FEEDER_ORDER:
        tech[f] = prim[f] + w.xfmr_nl[f] + w.xfmr_ll[f] + w.secl[f]
    w.head_P, w.head_Q, w.prim, w.tech = head_P, head_Q, prim, tech
    w.dp = {}
    w.sub_loss = {}
    for s, spec in P.SUBSTATIONS.items():
        Ps = sum(head_P[f] for f in P.SUB_FEEDERS[s])
        Qs = sum(head_Q[f] for f in P.SUB_FEEDERS[s])
        S = np.sqrt(Ps ** 2 + Qs ** 2)
        loss = spec["nl_kw"] + spec["ll_kw"] * (S / (spec["mva"] * 1000.0)) ** 2
        ss = spec["ss_kw"] * (1 + 0.25 * np.clip(14.0 - w.T, 0, None) / 14.0)
        w.sub_loss[s] = loss
        w.dp[s] = Ps + loss + ss
        w.dp[s + "_ss"] = ss


# ---------------------------------------------------------------------------------------------------------------
# the 2019 loss evaluation study: the network and loads as they stood in 2019, and the consultant's method
# ---------------------------------------------------------------------------------------------------------------

def tree_static(w, closed, feeders):
    tr = trees(w, closed)
    return {f: tr[f] for f in feeders}


def study_2019(w, seed=P.SEED + 19):
    """The consultant's 2019 study: hourly 2019 loads on the 2019 network (no licensed grows energized after 2019, no
    cold store, few illegal grows, no LED lights, the 2024 and 2026 transfers not yet made), then the study's own
    method: a peak-hour load flow with loads allocated to transformers by connected kVA, annual losses from the peak
    through the Buller-Woodrow loss factor, transformer losses from the test data, secondary at 0.7 per cent."""
    rng = np.random.default_rng(seed)
    g = time_grid(dt.datetime(2019, 1, 1, tzinfo=P.TZ), dt.datetime(2020, 1, 1, tzinfo=P.TZ))
    T, _, clear = weather(g, rng, EVENTS_2019)
    ref = np.ones(g.H, dtype=bool)
    u = shapes(g, T, ref)
    # keep the 2023-26 reference scale: rescale 2019 shapes to the 2024-25 means
    for c in u:
        u[c] = u[c] * (w.u[c].mean() / u[c].mean())
    dayU = {c: np.bincount(g.day, weights=u[c], minlength=g.D) for c in u}
    elev = solar_elevation(g.utc, P.LAT, P.LON)
    net = w.net
    # customers in 2019: the new connections since October 2023 absent, and three per cent more since 2019
    keep = []
    for i, c in enumerate(w.cust):
        if c["start"] is not None:
            continue
        if rng.random() < 0.035:
            continue
        keep.append(i)
    # 2019 topology: the 2024 and 2026 permanent transfers not yet made, every temporary tie open
    closed = list(w.state_before)
    lp19 = [lp for lp in w.lp if lp["key"] in P.LP_BEFORE_2019]
    out = {}
    nidx_all = {}
    for sub in P.SUBSTATIONS:
        feeders = P.SUB_FEEDERS[sub]
        nodes = [n for n in net.nodes if net.node_feeder[n] in feeders]
        nidx = {n: i for i, n in enumerate(nodes)}
        N, H = len(nodes), g.H
        Pc = np.zeros((N, H))
        Qn = np.zeros((N, H))
        metered = defaultdict(float)
        for i in keep:
            c = w.cust[i]
            if c["node"] not in nidx:
                continue
            fac = np.exp(rng.normal(0, 0.12, g.D))
            e = 0.985 * c["a"] * fac * dayU[c["cls"]]
            x = e[g.day] * u[c["cls"]] / np.maximum(dayU[c["cls"]][g.day], 1e-9)
            Pc[nidx[c["node"]]] += x
            Qn[nidx[c["node"]]] += x * math.tan(math.acos(PF[c["cls"]]))
            if c["pv_kw"] > 0 and c["pv_date"] and c["pv_date"] < dt.date(2019, 7, 1):
                gen = c["pv_kw"] * 0.78 * np.clip(np.sin(np.radians(elev)), 0, None) ** 1.15 * (0.25 + 0.75 * clear[g.day])
                Pc[nidx[c["node"]]] -= gen
            metered[c["feeder"]] += float(x.sum())
        for lp in lp19:
            if lp["node"] in nidx:
                x = 0.97 * lp["a"] * u[lp["cls"]]
                Pc[nidx[lp["node"]]] += x
                Qn[nidx[lp["node"]]] += x * math.tan(math.acos(PF[lp["cls"]]))
                metered[lp["feeder"]] += float(x.sum())
        for t in w.theft:
            if t["node"] in nidx and rng.random() < 0.25:
                x = 0.6 * t["kw"] * u["THEFT"]
                Pc[nidx[t["node"]]] += x
                Qn[nidx[t["node"]]] += x * 0.4
        dark = (elev < -0.8).astype(float)
        for L in w.lights:
            if L["node"] in nidx and L["install"] < dt.date(2019, 1, 1):
                Pc[nidx[L["node"]]] += dark * P.INPUT_W[L["lamp"]] / 1000.0
        # transformers in service in 2019
        kva_node = defaultdict(float)
        nl_f = defaultdict(float)
        ll_f = defaultdict(float)
        kva_f = defaultdict(float)
        xl = np.zeros((N, H))
        llnode = defaultdict(float)
        nl_node = np.zeros(N)
        for x in w.xfmrs:
            if x["node"] not in nidx or x["install"] >= dt.date(2019, 1, 1):
                continue
            if x["removed"] and x["removed"] < dt.date(2019, 1, 1):
                continue
            a, b = P.XFMR_LOSS[x["kva"]]
            old = x["mfg"] < 2010
            a *= P.OLD_NL if old else 1.0
            b *= P.OLD_LL if old else 1.0
            kva_node[x["node"]] += x["kva"]
            llnode[x["node"]] += b / 1000.0
            nl_node[nidx[x["node"]]] += a / 1000.0
        for nd, kva in kva_node.items():
            i = nidx[nd]
            sva = np.sqrt(np.maximum(Pc[i], 0) ** 2 + Qn[i] ** 2)
            xl[i] = llnode[nd] * (sva / kva) ** 2
        sec = np.maximum(Pc, 0) * P.SECONDARY_SHARE
        Pn = Pc + nl_node[:, None] + xl + sec
        tr = tree_static(w, closed, feeders)
        for f in feeders:
            order, pseg, pnode = tr[f]
            idx = [nidx[n] for n in order]
            FP, FQ = Pn[idx].copy(), Qn[idx].copy()
            pos = {n: j for j, n in enumerate(order)}
            loss = np.zeros(H)
            for j in range(len(order) - 1, 0, -1):
                n = order[j]
                kind, k = pseg[n]
                lp_ = 0.0
                if kind == "seg":
                    s = net.seg[k]
                    R = s["mi"] * P.CONDUCTORS[s["cond"]][0]
                    fac = 1.0 if s["phasing"] == "ABC" else P.SINGLE_PHASE_FACTOR
                    lp_ = fac * R * (FP[j] ** 2 + FQ[j] ** 2) / (P.V_KV ** 2) / 1000.0
                    loss += lp_
                pj = pos[pnode[n]]
                FP[pj] += FP[j] + lp_
                FQ[pj] += FQ[j]
            head, headQ = FP[0], FQ[0]
            kpk = int(np.argmax(head))
            S_pk = math.hypot(head[kpk], headQ[kpk])
            E = head.sum()
            LF = E / (head[kpk] * H)
            LsF = 0.15 * LF + 0.85 * LF ** 2
            # the study's peak load flow: loads allocated to the feeder's transformers by connected kVA
            kva = {n: kva_node.get(n, 0.0) for n in order}
            tot = sum(kva.values())
            down = {n: kva[n] for n in order}
            for j in range(len(order) - 1, 0, -1):
                n = order[j]
                down[pnode[n]] += down[n]
            Req = 0.0
            for j in range(1, len(order)):
                n = order[j]
                kind, k = pseg[n]
                if kind == "seg":
                    s = net.seg[k]
                    R = s["mi"] * P.CONDUCTORS[s["cond"]][0]
                    fac = 1.0 if s["phasing"] == "ABC" else P.SINGLE_PHASE_FACTOR
                    Req += fac * R * (down[n] / tot) ** 2
            peak_loss_kw = Req * (S_pk / P.V_KV) ** 2 / 1000.0
            prim_mwh = peak_loss_kw * H * LsF / 1000.0
            nl_mwh = nl_node[idx].sum() * H / 1000.0
            ll_rated = sum(llnode.get(n, 0.0) for n in order)
            ll_mwh = ll_rated * (S_pk / tot) ** 2 * H * LsF / 1000.0
            sec_mwh = P.SECONDARY_SHARE * metered[f] / 1000.0
            tech = prim_mwh + nl_mwh + ll_mwh + sec_mwh
            true_tech = (loss.sum() + nl_node[idx].sum() * H + xl[idx].sum() + sec[idx].sum()) / 1000.0
            out[f] = dict(peak_mw=head[kpk] / 1000.0, energy_mwh=E / 1000.0, lf=LF, lsf=LsF, req=Req,
                          peak_loss_kw=peak_loss_kw, prim_mwh=prim_mwh, nl_mwh=nl_mwh, ll_mwh=ll_mwh, sec_mwh=sec_mwh,
                          tech_mwh=tech, tech_pct=100.0 * tech / (E / 1000.0), kva=tot, true_tech_mwh=true_tech,
                          true_prim_mwh=loss.sum() / 1000.0, peak_time=g.loc[kpk], sales_mwh=metered[f] / 1000.0)
    return out
