#!/usr/bin/env python3
"""task5 architecture 5, the core: Orlavan citizens living in seven partner states on 1 January 2027.

Orlava's statistics office has to say how many Orlavan citizens are usually resident in each of seven partner states
of the free-movement area on 1 January 2027, because the foreign ministry staffs each consular district at one
officer for every 5,000 citizens or part of 5,000. No record holds the number. Each host counted its Orlavan
residents at its censuses of 1 January 2011 and 1 January 2021; between and after them there are only flows, and
every flow is reported twice and incompletely: by the state the person arrives in (which catches its own share of
arrivals) and by the state the person leaves (which catches its own share of departures). The partners' tables end
with 2023; only Orlava's own register runs to the end of 2026.

The three stumps (each opens a different member, each needs several dependent steps):
  S1 (against)  a host's arrivals table is not the arrivals. Every state's recording share is latent; the matrix
                of twice-reported flows fixes the shares only up to one common factor, and the level comes from
                Orlava's own census, which counted the foreign citizens who had lived abroad a year before.
  S2 (what)     a host's departures table is a fraction of the exits. The exits of the decade are the residual of
                the account between the two censuses, on corrected arrivals, and the host's recorded share follows.
  S3 (when)     2024 to 2026 are in no partner's table. Orlava's own deregistrations and re-registrations see those
                years at a fraction of the moves, measured host by host on the years both sides report.

Run:  python3 task5/generator/core.py            the corelib verdict
      python3 task5/generator/core.py --detail   the world, every route and the fitted shares
      python3 task5/generator/core.py --forcing  the call under each fitted input moved by its measured spread
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".claude", "skills", "stumping"))
import corelib  # noqa: E402

SEED = int(os.environ.get("CORE_SEED", 5127))
Y0, NY = 2011, 16                    # flow years 2011 to 2026; stocks on 1 January 2011 to 2027
CENSUS_A, CENSUS_B = 0, 10           # the hosts' censuses: 1 January 2011 and 1 January 2021
LAST = 13                            # the partners' tables end with 2023; Orlava's own run to 2026
REF = 5                              # Fenmark's intercensal count: 1 January 2016
STD = 5000.0                         # citizens per consular officer
HOME = "Orlava"
HOSTS = ("Skarholm", "Brennia", "Marovia", "Tesmar", "Kestria", "Fenmark", "Almera")
STATES = (HOME,) + HOSTS
REFHOST = "Fenmark"

# Each host: citizens at the 2011 census; yearly arrivals from Orlava before and after 2021; the yearly share who
# leave and its path from 2021; the share of arrivals its register records (a) and of departures (d); `early` tilts
# the exits of the first half of the decade against the second.
W = {
    "Skarholm": dict(n0=25750, inp=2600, inf=1700, e=0.050, epath=[1.0, 1.0, 1.15, 1.3, 1.35, 1.4], a=1.00, d=0.48, early=1.0),
    "Brennia": dict(n0=25500, inp=1800, inf=5600, e=0.060, epath=[1.0, 1.0, 1.1, 1.2, 1.25, 1.3], a=0.55, d=0.40, early=1.0),
    "Marovia": dict(n0=28500, inp=3900, inf=3000, e=0.085, epath=[1.0, 1.05, 1.1, 1.15, 1.2, 1.2], a=0.84, d=0.24, early=1.0),
    "Tesmar": dict(n0=16750, inp=3300, inf=2900, e=0.060, epath=[1.0, 1.1, 1.5, 1.9, 2.1, 2.2], a=0.70, d=0.45, early=1.0),
    "Kestria": dict(n0=3750, inp=900, inf=1000, e=0.055, epath=[1.0, 1.0, 1.05, 1.1, 1.1, 1.1], a=1.20, d=0.92, early=1.0),
    "Fenmark": dict(n0=12000, inp=2100, inf=1500, e=0.070, epath=[1.0, 1.05, 1.2, 1.3, 1.4, 1.4], a=0.66, d=0.30, early=1.6),
    "Almera": dict(n0=42250, inp=4200, inf=3200, e=0.045, epath=[1.0, 1.0, 1.2, 1.35, 1.45, 1.5], a=0.88, d=0.55, early=1.0),
}
for _k, _v in (("CORE_N0_" + h.upper(), h) for h in HOSTS):
    if os.environ.get(_k):
        W[_v]["n0"] = int(os.environ[_k])
A_HOME, B_HOME = 0.72, 0.36          # Orlava records 72 per cent of foreign arrivals, 36 per cent of its own emigrants
B_HOST = {"Skarholm": 0.80, "Brennia": 0.52, "Marovia": 0.45, "Tesmar": 0.60, "Kestria": 0.50, "Fenmark": 0.38,
          "Almera": 0.70}            # each host's own emigrants who deregister
RET, AO = 0.82, 0.50                 # exits that are returns home; returns the Orlavan register records
WIG = 0.02                           # pair to pair wobble of a recording share
BIRTH, DEATH = 0.0085, 0.0025        # births to and deaths of citizens abroad, per citizen per year


def simulate():
    """The world: each host's citizens year by year, and everybody's moves between the eight states."""
    w = {}
    for k, h in enumerate(HOSTS):
        p = W[h]
        r_in, r_ex, r_nat = (np.random.default_rng([SEED, k, j]) for j in (1, 2, 3))
        n = np.zeros(NY + 1)
        inn, ex, nat = np.zeros(NY), np.zeros(NY), np.zeros(NY)
        n[0] = p["n0"]
        for t in range(NY):
            if t < 10:
                lvl = p["inp"] * (1.0 + 0.02 * (t - 5))
                rate = p["e"] * (p["early"] if t < 5 else (2.0 - p["early"]) if p["early"] != 1.0 else 1.0)
            else:
                lvl = p["inf"] * (1.0 + 0.03 * (t - 12.5))
                rate = p["e"] * p["epath"][t - 10]
            inn[t] = r_in.poisson(lvl * r_in.lognormal(0.0, 0.06))
            ex[t] = r_ex.binomial(int(n[t]), min(0.9, rate * r_ex.lognormal(0.0, 0.05)))
            nat[t] = r_nat.poisson(n[t] * BIRTH * (1.0 + 0.1 * (k % 3 - 1))) - r_nat.poisson(n[t] * DEATH)
            n[t + 1] = n[t] + inn[t] - ex[t] + nat[t]
        w[h] = dict(n=n, inn=inn, ex=ex, nat=nat)
    rng = np.random.default_rng([SEED, 100])
    T = {}
    for i in STATES:
        for j in STATES:
            if i == j:
                continue
            if i == HOME:
                T[i, j] = w[j]["inn"].copy()
            else:
                lvl = rng.uniform(300, 3500)
                T[i, j] = rng.poisson(lvl * np.exp(rng.normal(0, 0.08, NY)) * (1.0 + 0.02 * (np.arange(NY) - 8)))
    return dict(host=w, T=T)


def records(world):
    """What is on file: both reports of every flow, the census counts, the vital events, the home census table."""
    a = {HOME: A_HOME}
    b = {HOME: B_HOME}
    for h in HOSTS:
        a[h] = W[h]["a"]
        b[h] = B_HOST[h]
    recA, recD = {}, {}
    for x, i in enumerate(STATES):
        for y, j in enumerate(STATES):
            if i == j:
                continue
            rng = np.random.default_rng([SEED, 200, x, y])
            t = world["T"][i, j]
            ra = a[j] * (1.0 + rng.uniform(-WIG, WIG))
            rb = b[i] * (1.0 + rng.uniform(-WIG, WIG))
            recA[i, j] = (rng.binomial(t.astype(int), ra) if ra < 1 else t + rng.poisson(t * (ra - 1.0))).astype(float)
            recD[i, j] = rng.binomial(t.astype(int), min(0.999, rb)).astype(float)
    R = dict(recA=recA, recD=recD, census_in={i: float(world["T"][i, HOME][9]) for i in HOSTS}, host={})
    for k, h in enumerate(HOSTS):
        rng = np.random.default_rng([SEED, 300, k])
        q = world["host"][h]
        dep = rng.binomial(q["ex"].astype(int), W[h]["d"]).astype(float)        # the host's departures of citizens
        ret = rng.binomial(rng.binomial(q["ex"].astype(int), RET), AO).astype(float)   # re-registrations at home
        R["host"][h] = dict(n11=float(q["n"][CENSUS_A]), n21=float(q["n"][CENSUS_B]), dep=dep, ret=ret,
                            nat=q["nat"].copy(), n16=float(q["n"][REF]) if h == REFHOST else None)
    return R


_FC = {}


def factors(R, o):
    """Every state's recording shares. Orlava's arrival share from its census (the foreign citizens who lived abroad
    a year before, against its register's arrivals of that year); each partner's share of its own emigrants from
    its flow to Orlava; each host's arrival share from the other partners' citizens moving to it."""
    key = (o.get("anchor", "sum"), o.get("win", (0, LAST)), o.get("drop_small", False), o.get("ah", "sums"),
           o.get("a_mode"))
    if key in _FC:
        return _FC[key]
    sl = slice(*o.get("win", (0, LAST)))
    ratios = [R["recA"][i, HOME][9] / R["census_in"][i] for i in HOSTS]
    if o.get("anchor", "sum") in ("sum", "referee"):
        a_home = sum(R["recA"][i, HOME][9] for i in HOSTS) / sum(R["census_in"].values())
    elif o["anchor"] == "mean":
        a_home = float(np.mean(ratios))
    else:
        a_home = float(np.median(ratios))
    b = {i: a_home * R["recD"][i, HOME][sl].sum() / R["recA"][i, HOME][sl].sum() for i in HOSTS}
    a = {}
    for h in HOSTS:
        send = [i for i in HOSTS if i != h]
        if o.get("drop_small"):
            send = sorted(send, key=lambda i: -R["recA"][i, h][sl].sum())[:-1]
        each = [R["recA"][i, h][sl].sum() * b[i] / R["recD"][i, h][sl].sum() for i in send]
        if o.get("ah", "sums") == "sums":
            a[h] = sum(R["recA"][i, h][sl].sum() for i in send) / sum(R["recD"][i, h][sl].sum() / b[i] for i in send)
        else:
            a[h] = float(np.mean(each)) if o["ah"] == "mean" else float(np.median(each))
    if o.get("anchor") == "referee":             # the level from Fenmark's two half-decade accounts instead
        q = R["host"][REFHOST]
        i1, i2 = R["recA"][HOME, REFHOST][:REF].sum(), R["recA"][HOME, REFHOST][REF:10].sum()
        d1, d2 = q["dep"][:REF].sum(), q["dep"][REF:10].sum()
        g1 = q["n16"] - q["n11"] - q["nat"][:REF].sum()
        g2 = q["n21"] - q["n16"] - q["nat"][REF:10].sum()
        u = (d1 * g2 - d2 * g1) / (d1 * i2 - d2 * i1)
        s = (1.0 / u) / a[REFHOST]
        a = {h: a[h] * s for h in HOSTS}
    if o.get("a_mode") == "raw":                 # the host's arrivals table taken as the arrivals
        a = {h: 1.0 for h in HOSTS}
    elif o.get("a_mode") == "best":              # the shares scaled so the fullest recorder is complete
        top = max(a.values())
        a = {h: a[h] / top for h in HOSTS}
    elif o.get("a_mode") == "mean":              # the shares scaled about their own average
        gm = float(np.exp(np.mean([np.log(v) for v in a.values()])))
        a = {h: a[h] / gm for h in HOSTS}
    _FC[key] = dict(a_home=a_home, b=b, a=a)
    return _FC[key]


def chain(R, h, o=None, upto=NY):
    """Citizens in host h on 1 January of year index `upto` (16 is 2027), with the pieces of the account."""
    o = o or {}
    f = factors(R, o)
    q = R["host"][h]
    ov = slice(*o.get("ov", (0, LAST)))
    a_h = f["a"][h] * o.get("x_a", 1.0)
    inn = R["recA"][HOME, h][:LAST] / a_h                        # arrivals to 2023
    nat = q["nat"]
    rec = q["ret"][:LAST] if o.get("timing") == "home" else q["dep"][:LAST]
    ex_p = inn[:10].sum() + nat[:10].sum() - (q["n21"] - q["n11"])   # who left between the two censuses
    d = 1.0 if o.get("ex_level") == "recorded" else rec[:10].sum() / ex_p * o.get("x_d", 1.0)
    out = dict(d=d, ex_p=float(ex_p), a=a_h)
    if upto <= 10:
        out["n"] = float(q["n11"] + inn[:upto].sum() + nat[:upto].sum() - rec[:upto].sum() / d)
        return out
    ex = rec / d
    b_h = R["recD"][HOME, h][ov].sum() / inn[ov].sum() * o.get("x_b", 1.0)     # the home register's share of moves to h
    r_h = q["ret"][ov].sum() / ex[ov].sum() * o.get("x_r", 1.0)                # and of the exits from h
    n = q["n21"]
    py = 0.0
    for t in range(10, LAST):
        py += n
        n = n + inn[t] + nat[t] - ex[t]
    n24 = n
    nat_rate = nat[10:LAST].sum() / py
    if o.get("fwd") == "carry":                                  # 2021 to 2023 carried through 2024 to 2026
        arr2 = np.full(NY - LAST, inn[10:LAST].mean())
        eps, ex2 = ex[10:LAST].sum() / py, []
        for t in range(NY - LAST):
            ex2.append(n * eps)
            n = n + arr2[t] - ex2[-1] + n * nat_rate
        ex2 = np.array(ex2)
    else:
        arr2 = R["recD"][HOME, h][LAST:] / b_h
        ex2 = q["ret"][LAST:] / r_h
        for t in range(NY - LAST):
            n = n + arr2[t] - ex2[t] + (nat[10:LAST].mean() if o.get("nat") == "count" else n * nat_rate)
    out.update(n=float(n), b_h=float(b_h), r_h=float(r_h), left=float(ex[10:LAST].sum() + ex2.sum()),
               late=float(ex2.sum() / ex[10:LAST].sum()), arr=float(inn[10:LAST].sum() + arr2.sum()), n24=float(n24))
    return out


def b_home(R, o=None):
    """Of the citizens who moved to the seven hosts in 2011 to 2023, the share who deregistered in Orlava."""
    f = factors(R, o or {})
    return sum(R["recD"][HOME, h][:LAST].sum() for h in HOSTS) / sum(
        R["recA"][HOME, h][:LAST].sum() / f["a"][h] for h in HOSTS)


def direct(R, h, upto=NY):
    """The host's own records at face value: its census count rolled on by its tables to where they end."""
    q = R["host"][h]
    if upto <= 10:
        return float(q["n11"] + R["recA"][HOME, h][:upto].sum() + q["nat"][:upto].sum() - q["dep"][:upto].sum())
    return float(q["n21"] + R["recA"][HOME, h][10:LAST].sum() + q["nat"][10:LAST].sum() - q["dep"][10:LAST].sum())


def mirror(R, h, upto=NY):
    """The larger of the two reports of every flow, and the last three years repeated to 2027."""
    q = R["host"][h]
    arr = np.maximum(R["recA"][HOME, h][:LAST], R["recD"][HOME, h][:LAST])
    ex = np.maximum(q["dep"][:LAST], q["ret"][:LAST])
    if upto <= 10:
        return float(q["n11"] + arr[:upto].sum() + q["nat"][:upto].sum() - ex[:upto].sum())
    return float(q["n21"] + 2.0 * (arr[10:LAST].sum() + q["nat"][10:LAST].sum() - ex[10:LAST].sum()))


HURRIED = {"S1": {"a_mode": "raw"}, "S2": {"ex_level": "recorded"}, "S3": {"fwd": "carry"}}
RIGOROUS = {"a_mode": "best"}
FAMILY = [
    ("the golden", {}),
    ("home share as the mean of the seven partners' ratios", {"anchor": "mean"}),
    ("home share as their median", {"anchor": "median"}),
    ("host share as the mean of the senders' ratios", {"ah": "mean"}),
    ("host share as their median", {"ah": "median"}),
    ("the smallest sender to each host dropped", {"drop_small": True}),
    ("shares fitted on 2014 to 2023", {"win": (3, LAST)}),
    ("shares fitted on 2011 to 2020", {"win": (0, 10)}),
    ("shares fitted on 2016 to 2023", {"win": (5, LAST)}),
    ("home register's shares on 2016 to 2023", {"ov": (5, LAST)}),
    ("home register's shares on 2019 to 2023", {"ov": (8, LAST)}),
    ("home register's shares on 2021 to 2023", {"ov": (10, LAST)}),
    ("home register's shares on 2011 to 2020", {"ov": (0, 10)}),
    ("shares on 2014 to 2023 by mean, home shares on 2016 to 2023", {"win": (3, LAST), "ah": "mean", "ov": (5, LAST)}),
    ("smallest sender dropped, home share by mean, home shares on 2019 to 2023",
     {"drop_small": True, "anchor": "mean", "ov": (8, LAST)}),
    ("exits timed by the home's re-registrations throughout", {"timing": "home"}),
    ("births less deaths carried as a count", {"nat": "count"}),
    ("the level taken from Fenmark's two half-decade accounts", {"anchor": "referee"}),
]


def lattice_opts():
    keys, ids = {}, sorted(HURRIED)
    for mask in range(1, 2 ** len(ids)):
        o = {}
        for k, s in enumerate(ids):
            if mask >> k & 1:
                o.update(HURRIED[s])
        keys["+".join(s for k, s in enumerate(ids) if mask >> k & 1)] = o
    return keys


def band(x):
    return int(x // STD)


def lines_for(x):
    k = band(x)
    return [STD * j for j in range(max(1, k - 4), k + 6)]


def host_view(world, R, h):
    lat_o = lattice_opts()
    return dict(truth=float(world["host"][h]["n"][NY]), golden=chain(R, h)["n"],
                fam=[chain(R, h, o)["n"] for _, o in FAMILY],
                lat={k: chain(R, h, o)["n"] for k, o in lat_o.items()},
                routes={"direct": direct(R, h), "rigorous": chain(R, h, RIGOROUS)["n"], "mirror": mirror(R, h)},
                mean=chain(R, h, {"a_mode": "mean"})["n"])


def spreads(R, h):
    """Each fitted input's largest relative move across the family."""
    g = chain(R, h)
    out = {}
    for k, f in (("x_a", "a"), ("x_d", "d"), ("x_b", "b_h"), ("x_r", "r_h")):
        out[k] = max(abs(chain(R, h, o)[f] / g[f] - 1.0) for _, o in FAMILY if o.get("timing") != "home")
    return out


def main():
    world = simulate()
    R = records(world)
    lat_o = lattice_opts()
    reflex = "+".join(sorted(HURRIED))
    V = {h: host_view(world, R, h) for h in HOSTS}
    if "--forcing" in sys.argv:
        gold = {h: band(V[h]["golden"]) for h in HOSTS}
        sp = {h: spreads(R, h) for h in HOSTS}
        bad = 0
        print("%-58s %s" % ("fitted input moved", "  ".join("%8s" % h[:8] for h in HOSTS)))
        rows = []
        for k, label in (("x_a", "the host's arrival share"), ("x_d", "the host's departure share"),
                         ("x_b", "the home register's share of moves"), ("x_r", "the home register's share of exits")):
            for sign in (-1.0, 1.0):
                rows.append(("%s, one spread %s" % (label, "down" if sign < 0 else "up"),
                             {h: {k: 1.0 + sign * sp[h][k]} for h in HOSTS}))
        for sign in (-1.0, 1.0):                 # the four are not independent (the last three are fitted on the
            rows.append(("all four %s together, one spread each" % ("down" if sign < 0 else "up"),   # first), so this overstates
                         {h: {k: 1.0 + sign * sp[h][k] for k in sp[h]} for h in HOSTS}))
        for name, o in rows:
            v = {h: chain(R, h, o[h])["n"] for h in HOSTS}
            same = all(band(v[h]) == gold[h] for h in HOSTS)
            bad += 0 if same else 1
            print("%-58s %s  %s" % (name, "  ".join("%8.0f" % v[h] for h in HOSTS), "same call" if same else "CALL MOVES"))
        for k in ("x_a", "x_d", "x_b", "x_r"):
            print("%-58s %s" % ("measured spread of %s, per cent" % k, "  ".join("%8.2f" % (100 * sp[h][k]) for h in HOSTS)))
        return 1 if bad else 0
    G = {h: chain(R, h) for h in HOSTS}
    truth = {h: V[h]["truth"] for h in HOSTS}
    members = {h: dict(lines=lines_for(truth[h]), truth=truth[h], golden=V[h]["golden"], family=V[h]["fam"],
                       routes=V[h]["routes"]) for h in HOSTS}
    lat = {k: {h: V[h]["lat"][k] for h in HOSTS} for k in lat_o}

    def c1(o=None):                      # S1's own: the home register's share of the citizens who emigrated
        return 100.0 * b_home(R, o)

    def c2(o=None):                      # S2's own: the share of exits from Skarholm that its register recorded
        o = o or {}
        if o.get("ex_level") == "recorded":
            return 100.0
        return 100.0 * R["host"]["Skarholm"]["dep"][:10].sum() / chain(R, "Skarholm", o)["ex_p"]

    def c3(o=None):                      # S3's own: exits from Tesmar in 2024 to 2026 against 2021 to 2023
        return chain(R, "Tesmar", o)["late"]
    figures = []
    for cid, fn in (("C1", c1), ("C2", c2), ("C3", c3)):
        figures.append(dict(id=cid, block="component", golden=fn(), family=[fn(o) for _, o in FAMILY],
                            lattice={k: fn(o) for k, o in lat_o.items()}, routes={"rigorous": fn(RIGOROUS)}))
    for h in HOSTS:
        figures.append(dict(id="N-%s" % h, block="ask", member=h))
    for h in HOSTS:
        figures.append(dict(id="L-%s" % h, block="ask", golden=G[h]["left"],
                            family=[chain(R, h, o)["left"] for _, o in FAMILY],
                            lattice={k: chain(R, h, o)["left"] for k, o in lat_o.items()},
                            routes={"rigorous": chain(R, h, RIGOROUS)["left"]}))
    rq = R["host"][REFHOST]
    referee = dict(slice="Fenmark's own count of its Orlavan citizens on 1 January 2016, half way between its two "
                         "censuses, which no method here is fitted to and which no other host or later year shares",
                   covers_target=False, truth=rq["n16"], golden=chain(R, REFHOST, None, REF)["n"],
                   rivals={"the host's tables at face value": direct(R, REFHOST, REF),
                           "the larger report of each flow": mirror(R, REFHOST, REF),
                           "shares scaled to the fullest recorder": chain(R, REFHOST, RIGOROUS, REF)["n"],
                           "arrivals as recorded, the account closed on departures":
                               chain(R, REFHOST, {"a_mode": "raw"}, REF)["n"]})
    spec = dict(task="task5 architecture 5", call="lines", members=members, lattice=lat, referee=referee,
                figures=figures, stumps={
                    "S1": dict(axis="against", opens="Brennia",
                               said_out_loud="Each state records only a share of the people who move in and a share "
                                             "of its own people who move out, a different share in each state, so "
                                             "no host's arrivals table is the number who arrived.",
                               steps_left=4, precedents=["L22", "L51", "N27"]),
                    "S2": dict(axis="what", opens="Marovia",
                               said_out_loud="People who leave a host mostly leave no record there, so its "
                                             "departures table is a fraction of the exits, a different fraction in "
                                             "each host.",
                               steps_left=4, precedents=["L48", "L32", "N10"]),
                    "S3": dict(axis="when", opens="Tesmar",
                               said_out_loud="The partners' tables stop at 2023, and 2024 to 2026 are seen only by "
                                             "Orlava's own register, which catches a fraction of the moves.",
                               steps_left=3, precedents=["N13", "N28", "L03"]),
                })
    if "--detail" in sys.argv:
        f = factors(R, {})
        print("Orlava's arrival share %.3f (world %.2f); its emigrants who deregistered %.3f (world %.2f)" % (
            f["a_home"], A_HOME, b_home(R), B_HOME))
        print("%-9s %14s %14s %14s %8s %8s" % ("host", "arrival share", "departure sh.", "own emigrants", "b_h", "r_h"))
        for h in HOSTS:
            print("%-9s  %.3f (%.2f)   %.3f (%.2f)   %.3f (%.2f)  %.3f  %.3f" % (
                h, f["a"][h], W[h]["a"], G[h]["d"], W[h]["d"], f["b"][h], B_HOST[h], G[h]["b_h"], G[h]["r_h"]))
        print("citizens on 1 January 2027")
        print("%-9s %6s %6s %5s %5s | %6s %6s %6s | %6s %6s %6s | %6s | %6s %6s %6s %6s | officers: golden (truth) S1 S2 S3 "
              "reflex direct rigorous mirror mean" % ("host", "truth", "golden", "famlo", "famhi", "S1", "S2", "S3", "S1+S2",
                                                      "S1+S3", "S2+S3", "reflex", "direct", "rigor", "mirror", "meanrp"))
        for h in HOSTS:
            v = V[h]
            print("%-9s %6.0f %6.0f %5.0f %5.0f | %6.0f %6.0f %6.0f | %6.0f %6.0f %6.0f | %6.0f | %6.0f %6.0f %6.0f %6.0f | "
                  "%d (%d): %d %d %d %d %d %d %d %d" % (
                      h, v["truth"], v["golden"], min(v["fam"]) - v["golden"], max(v["fam"]) - v["golden"],
                      v["lat"]["S1"], v["lat"]["S2"], v["lat"]["S3"], v["lat"]["S1+S2"], v["lat"]["S1+S3"],
                      v["lat"]["S2+S3"], v["lat"][reflex], v["routes"]["direct"], v["routes"]["rigorous"],
                      v["routes"]["mirror"], v["mean"], band(v["golden"]) + 1, band(v["truth"]) + 1,
                      band(v["lat"]["S1"]) + 1, band(v["lat"]["S2"]) + 1, band(v["lat"]["S3"]) + 1,
                      band(v["lat"][reflex]) + 1, band(v["routes"]["direct"]) + 1, band(v["routes"]["rigorous"]) + 1,
                      band(v["routes"]["mirror"]) + 1, band(v["mean"]) + 1))
        print("variant deviations from the golden")
        for name, o in FAMILY[1:]:
            print("  %-78s" % name[:78], " ".join("%6.0f" % (chain(R, h, o)["n"] - V[h]["golden"]) for h in HOSTS))
        print("the account: census 2011, census 2021, golden 1 January 2024, arrivals and exits 2021 to 2026, the world's")
        for h in HOSTS:
            q, g, w = R["host"][h], G[h], world["host"][h]
            print("  %-9s %6.0f %6.0f %6.0f | arrivals %6.0f (%6.0f) exits %6.0f (%6.0f) | 2024 to 2026 over 2021 to 2023 "
                  "exits %.2f (%.2f)" % (h, q["n11"], q["n21"], g["n24"], g["arr"], w["inn"][10:].sum(), g["left"],
                                         w["ex"][10:].sum(), g["late"], w["ex"][LAST:].sum() / w["ex"][10:LAST].sum()))
        print("referee: Fenmark on 1 January 2016, its count %.0f, the golden %.0f; %s" % (
            referee["truth"], referee["golden"], "; ".join("%s %.0f" % kv for kv in referee["rivals"].items())))
        # the second referee: 2021 to 2023 held out, the home register scaled on 2011 to 2020 against the carry
        hold = []
        for h in HOSTS:
            g = G[h]
            inn = R["recA"][HOME, h][:LAST] / g["a"]
            br = R["recD"][HOME, h][:10].sum() / inn[:10].sum()
            hold.append((h, inn[10:LAST].sum(), R["recD"][HOME, h][10:LAST].sum() / br, 3.0 * inn[7:10].mean()))
        print("held out, arrivals 2021 to 2023: " + "; ".join("%s %.0f, home register scaled %.0f, 2018 to 2020 carried "
                                                               "%.0f" % x for x in hold))
        for fg in figures[:3]:
            print(fg["id"], "%.3f" % fg["golden"], "family %.3f to %.3f" % (min(fg["family"]), max(fg["family"])),
                  {k: round(float(x), 3) for k, x in fg["lattice"].items()}, "rigorous %.3f" % fg["routes"]["rigorous"])
        print()
    return corelib.run(spec)


if __name__ == "__main__":
    sys.exit(main())
