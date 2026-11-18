"""The world behind the pack. core.py holds the eight states' yearly moves, each host's Orlavan citizens and what every
register caught of them. This module lays the rest of the same system around those arrays without changing one of
them: the citizens of every state living in every other state (the same process as the hosts' Orlavan citizens), the
departures and returns their registers catch, their births and deaths, the census tables, the moves to and from the
rest of the world, and every yearly count split by sex and age group the way a statistical office tables it."""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import core as C  # noqa: E402

ORG = "Statistics Orlava"
HUB = "Common Movement Area Statistical Office"
MINISTRY = "Ministry of Foreign Affairs of the Republic of Orlava"
PEOPLE = dict(head="Neja Bezjak", analyst="Jani Debeljak", secretary="Emil Bajc", register="Kaja Kalan",
              liaison="Silvo Zver", census="Klemen Kokalj")
HOME, HOSTS, STATES = C.HOME, C.HOSTS, C.STATES
ROW = "Other"                                  # every state outside the area, taken together
PARTNERS = STATES + (ROW,)
CODE3 = dict(Orlava="ORL", Skarholm="SKH", Brennia="BRN", Marovia="MRV", Tesmar="TSM", Kestria="KST", Fenmark="FNM",
             Almera="ALM", Other="ZZZ")
CODE2 = dict(Orlava="OR", Skarholm="SH", Brennia="BN", Marovia="MV", Tesmar="TS", Kestria="KS", Fenmark="FM",
             Almera="AM", Other="ZZ")
CODEN = dict(Orlava="110", Skarholm="120", Brennia="130", Marovia="140", Tesmar="150", Kestria="160", Fenmark="170",
             Almera="180", Other="990")
LONG = dict(Orlava="Republic of Orlava", Skarholm="Kingdom of Skarholm", Brennia="Republic of Brennia",
            Marovia="Federal Republic of Marovia", Tesmar="Republic of Tesmar", Kestria="Principality of Kestria",
            Fenmark="Kingdom of Fenmark", Almera="Republic of Almera", Other="Other states (outside the Area)")
SEAT = dict(Skarholm="Halvik", Brennia="Dorne", Marovia="Lautern", Tesmar="Castro Tesa", Kestria="Kestria Town",
            Fenmark="Vennby", Almera="Almera City")
POP = dict(Orlava=3.91e6, Skarholm=5.62e6, Brennia=9.84e6, Marovia=17.2e6, Tesmar=8.13e6, Kestria=0.41e6,
           Fenmark=5.08e6, Almera=38.6e6)
AGES = ("0-14", "15-24", "25-34", "35-44", "45-64", "65+")
AGE_LO = (0, 15, 25, 35, 45, 65)
AGE_HI = (14, 24, 34, 44, 64, 88)
SEXES = ("F", "M")
NY, LAST, Y0 = C.NY, C.LAST, C.Y0
TABLES = ("A", "B", "C", "D")
D_HOME = 0.35                                  # foreign citizens leaving Orlava who deregister
AGE_MOVE = np.array([0.10, 0.23, 0.33, 0.18, 0.13, 0.03])     # people who move
AGE_BACK = np.array([0.08, 0.14, 0.30, 0.24, 0.19, 0.05])     # people who go back
MUNICIPALITIES = [
    "Vrhova", "Stara Loka", "Novi Dol", "Zelena Gora", "Bela Voda", "Kamna Vas", "Dolnji Breg", "Gornji Breg",
    "Crni Potok", "Rdeci Kal", "Sveti Lenart", "Mala Reka", "Velika Reka", "Podgora", "Zagorica", "Lipnik",
    "Hrastovec", "Jelsane", "Brezovo", "Smrecje", "Topolnica", "Vinski Vrh", "Suha Krajina", "Mokro Polje",
    "Ravne Njive", "Kozji Hrib", "Medvedje", "Orlov Kamen", "Sokolnik", "Javorje", "Borovnica Polje", "Trnovec",
    "Dobrava", "Zalog ob Reki", "Stari Grad", "Novo Sredisce", "Pristan", "Soline", "Otok", "Mejni Dol",
    "Planina pri Jezeru", "Jezerce", "Slapnik", "Mlinsko", "Kovaska Vas", "Rudnik", "Steklarna", "Tkalsko",
]


def _split(count, p_age, rng, tilt=0.0):
    """One yearly count as twelve cells: sex by age group."""
    p_f = min(0.62, max(0.38, 0.47 + tilt))
    p = np.concatenate([p_f * p_age, (1.0 - p_f) * p_age])
    return rng.multinomial(int(count), p / p.sum()).reshape(2, len(AGES))


def build():
    world = C.simulate()
    R = C.records(world)
    S = len(STATES)
    idx = {s: k for k, s in enumerate(PARTNERS)}
    # --- every other pair: the citizens of i living in j, the same account as the hosts' Orlavan citizens
    d_of = {h: C.W[h]["d"] for h in HOSTS}
    d_of[HOME] = D_HOME
    rg = np.random.default_rng([C.SEED, 390])
    g_of = {h: float(rg.uniform(0.30, 0.55)) for h in HOSTS}        # a state's leavers abroad who come home and re-register
    stock, exits, births, deaths = {}, {}, {}, {}
    dep, back = {}, {}                                              # Table C and Table D cells
    for x, i in enumerate(STATES):
        for y, j in enumerate(STATES):
            if i == j:
                continue
            if i == HOME:
                q = world["host"][j]
                k = HOSTS.index(j)
                b, dth = q["b"], q["dth"]                           # the core's own births and deaths
                assert np.array_equal(b - dth, q["nat"]), j
                stock[i, j], exits[i, j], births[i, j], deaths[i, j] = q["n"], q["ex"], b, dth
                dep[i, j], back[i, j] = R["host"][j]["dep"], R["host"][j]["ret"]
                continue
            rng = np.random.default_rng([C.SEED, 400, x, y])
            arr = world["T"][i, j]
            n = np.zeros(NY + 1)
            ex, b, dth = np.zeros(NY), np.zeros(NY), np.zeros(NY)
            n[0] = np.round(rng.uniform(6.0, 13.0) * arr.mean())
            rate = rng.uniform(0.05, 0.085)
            for t in range(NY):
                path = 1.0 + (0.04 * (t - 12) if t > 12 else 0.0)
                ex[t] = rng.binomial(int(n[t]), min(0.9, rate * path * rng.lognormal(0.0, 0.05)))
                b[t] = rng.poisson(n[t] * C.BIRTH * rng.uniform(0.9, 1.1))
                dth[t] = rng.poisson(n[t] * C.DEATH)
                n[t + 1] = n[t] + arr[t] - ex[t] + b[t] - dth[t]
            stock[i, j], exits[i, j], births[i, j], deaths[i, j] = n, ex, b, dth
            dep[i, j] = rng.binomial(ex.astype(int), min(0.999, d_of[j] * (1.0 + rng.uniform(-C.WIG, C.WIG)))).astype(float)
            back[i, j] = rng.binomial(ex.astype(int), g_of[i] * (1.0 + rng.uniform(-C.WIG, C.WIG))).astype(float)
    # --- the rest of the world, per state: steady Poisson streams
    rw = np.random.default_rng([C.SEED, 410])
    row = {}
    for s in STATES:
        scale = (POP[s] / POP[HOME]) ** 0.7
        lv = dict(A=3000 * scale, B=1500 * scale, C=1400 * scale, D=900 * scale)
        row[s] = {t: rw.poisson(lv[t] * np.exp(rw.normal(0, 0.06, NY))).astype(float) for t in TABLES}
    # --- the tables: cell[table][reporter][partner] is the yearly series; partner tables end with 2023
    cell = {t: {s: {} for s in STATES} for t in TABLES}
    for i in STATES:
        for j in STATES:
            if i == j:
                continue
            cell["A"][j][i] = R["recA"][i, j]                       # arrivals in j of i's citizens
            cell["B"][i][j] = R["recD"][i, j]                       # i's own citizens leaving for j
            cell["C"][j][i] = dep[i, j]                             # i's citizens leaving j
            cell["D"][i][j] = back[i, j]                            # i's own citizens arriving from j
    for s in STATES:
        for t in TABLES:
            cell[t][s][ROW] = row[s][t]
    # --- sex and age: every (table, reporter, partner, year) count split once
    split = {}
    for a, t in enumerate(TABLES):
        for x, s in enumerate(STATES):
            for p in PARTNERS:
                if p == s:
                    continue
                rs = np.random.default_rng([C.SEED, 500, a, x, idx[p]])
                tilt = float(rs.uniform(-0.05, 0.05))
                p_age = AGE_BACK if t in ("C", "D") else AGE_MOVE
                p_age = p_age * np.exp(rs.normal(0, 0.08, len(AGES)))
                p_age = p_age / p_age.sum()
                split[t, s, p] = np.array([_split(cell[t][s][p][y], p_age, rs, tilt) for y in range(NY)])
    # --- the censuses: usual residents by citizenship and by country of birth, 2011 and 2021, and Fenmark's 2016 count
    rc = np.random.default_rng([C.SEED, 420])
    rt = np.random.default_rng([C.SEED, 425])
    census, birthplace, own, other = {}, {}, {}, {}
    for j in STATES:
        # a state's whole population: its own level and its own growth, on a stream of its own
        level, growth = POP[j] * rt.uniform(0.985, 1.015), rt.uniform(0.0012, 0.0055)
        whole = {t: level * (1.0 + growth) ** t * (1.0 + rt.normal(0, 0.0008)) for t in (0, 5, 10)}
        other[j] = {t: float(np.round(POP[j] * rc.uniform(0.02, 0.05) * (1.0 + 0.012 * t))) for t in (0, 5, 10)}
        for i in STATES:
            if i != j:
                for t in (0, 5, 10):
                    census[i, j, t] = float(stock[i, j][t])
                    birthplace[i, j, t] = float(np.round(stock[i, j][t] * rc.uniform(1.15, 1.6)))
        for t in (0, 5, 10):
            foreign = sum(census[i, j, t] for i in STATES if i != j) + other[j][t]
            own[j, t] = float(np.round(whole[t] - foreign))
    pop_total = {}
    rp = np.random.default_rng([C.SEED, 430])
    for j in STATES:
        t0 = own[j, 0] + sum(census[i, j, 0] for i in STATES if i != j) + other[j][0]
        t10 = own[j, 10] + sum(census[i, j, 10] for i in STATES if i != j) + other[j][10]
        path = np.linspace(t0, t10, 11)
        step = (t10 - t0) / 10.0
        tail = t10 + step * np.arange(1, 6) * rp.uniform(0.7, 1.2)
        wig = np.concatenate([[0.0], rp.normal(0, abs(step) * 0.08, 9), [0.0], rp.normal(0, abs(step) * 0.08, 5)])
        pop_total[j] = np.round(np.concatenate([path, tail]) + wig)
    # --- Orlava's census table: foreign citizens by where they lived a year before
    c14 = {}
    for i in HOSTS:
        tot = census[i, HOME, 10]
        abroad = float(R["census_in"][i])
        moved = float(np.round((tot - abroad) * rc.uniform(0.07, 0.11)))
        c14[i] = dict(total=tot, abroad=abroad, elsewhere=moved, same=tot - abroad - moved)
    tot = other[HOME][10]
    abroad = float(np.round(row[HOME]["A"][9] / (C.A_HOME * np.random.default_rng([C.SEED, 440]).uniform(0.97, 1.03))))
    moved = float(np.round((tot - abroad) * 0.09))
    c14[ROW] = dict(total=tot, abroad=abroad, elsewhere=moved, same=tot - abroad - moved)
    return dict(world=world, R=R, cell=cell, split=split, stock=stock, exits=exits, births=births, deaths=deaths,
                census=census, birthplace=birthplace, own=own, other=other, pop_total=pop_total, c14=c14, g_of=g_of,
                d_of=d_of)


if __name__ == "__main__":
    WD = build()
    n = sum(WD["cell"][t][HOME][p].sum() for t in TABLES for p in PARTNERS if p != HOME)
    print("register events before repeats: %d" % n)
    for t in TABLES:
        print(t, {p: int(WD["cell"][t][HOME][p].sum()) for p in PARTNERS if p != HOME})
    print("stocks of other pairs at 2011, 2021:", {(i[:3], j[:3]): (int(WD["stock"][i, j][0]), int(WD["stock"][i, j][10]))
                                                   for (i, j) in list(WD["stock"])[7:14]})
    print("min stock", min(float(v.min()) for v in WD["stock"].values()))
