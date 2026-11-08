"""task7 architecture 5: Ardcarn Bank's commercial property book, 2004 to 2026, simulated month by month.

Every record in the pack comes from this simulation. A property's true value moves with its sector and region's
commercial property index and with a drift of its own; the bank sees the true value only when a valuer inspects the
property (at origination, in the credit committee's three-yearly cycle from 2012 to 2019, at a top-up, and when a
facility defaults) and carries it between inspections as the last inspection rolled forward by the index. A
borrower's monthly chance of default rises when its property has fallen behind the market since the last inspection;
the tilt is mean-one at every distance from the inspection, so a grade's default rate does not depend on how long
ago the property was inspected, while the properties of the borrowers who do default have fallen behind by more the
longer since the inspection."""
import datetime as dt
import math

import numpy as np

SEED = 141
AS_OF = dt.date(2027, 1, 15)
START, END = (2004, 1), (2026, 12)

SECTORS = ["Retail", "Office", "Industrial", "Hospitality", "Healthcare"]
REGIONS = ["Dublin", "Regional cities", "Rest of State"]
# a property's own drift behind or ahead of its index (log, per year), and the extra discount an inspection at
# default finds on a property whose value rests on the failed business (the going concern lost)
SIGMA = {"Retail": 0.056, "Office": 0.054, "Industrial": 0.051, "Hospitality": 0.060, "Healthcare": 0.058}
KAPPA = 0.025            # a building ages against the index that rolls its value forward (log per year)
DELTA = {"Retail": 0.040, "Office": 0.040, "Industrial": 0.035, "Hospitality": 0.085, "Healthcare": 0.075}
GAMMA = 3.0             # default hazard per unit of log drift behind the market since the last inspection
VALUER_SD = 0.03         # an inspection's own error, log
SALE_FACTOR = 0.815      # sale price against the inspection at default, before costs
SALE_SD = 0.055
COST_RATE, COST_FIXED = 0.025, 6500.0
H_MODEL = 0.22           # the LGD model's haircut: net sale proceeds against the inspection at default
MASTER_PD = [None, 0.0025, 0.0050, 0.0090, 0.0150, 0.0260, 0.0450, 0.0800, 0.1600]
# the master scale the credit policy publishes (recalibrated by the bank in 2025); the plan takes each grade's
# twelve-month chance from it
PUBLISHED_PD = {1: 0.0021, 2: 0.0042, 3: 0.0075, 4: 0.0125, 5: 0.0216, 6: 0.0374, 7: 0.0664, 8: 0.1328}
CYCLE = {2004: 0.55, 2005: 0.55, 2006: 0.6, 2007: 0.7, 2008: 1.3, 2009: 2.0, 2010: 2.2, 2011: 2.0, 2012: 1.9,
         2013: 1.55, 2014: 1.2, 2015: 0.85, 2016: 0.8, 2017: 0.75, 2018: 0.75, 2019: 0.8, 2020: 1.25, 2021: 1.05,
         2022: 0.8, 2023: 0.95, 2024: 1.05, 2025: 0.95, 2026: 0.9}
CYCLE_START, CYCLE_END = (2012, 1), (2019, 12)
RECORD_START = (2012, 1)     # the warehouse went live in January 2012; the default record starts there
REFERRAL_FROM = (2022, 1)    # from 2022 the workout unit has the security re-inspected when a facility of 500,000 or
REFERRAL_MIN = 1000e3        # more is referred to it, two to six months before the default

ORIG_COUNTS = {2004: 168, 2005: 272, 2006: 356, 2007: 376, 2008: 220, 2009: 72, 2010: 64, 2011: 72, 2012: 96, 2013: 132, 2014: 188, 2015: 240, 2016: 272, 2017: 296, 2018: 308, 2019: 296, 2020: 168, 2021: 240, 2022: 296, 2023: 260, 2024: 280, 2025: 300, 2026: 260}
SECTOR_MIX = {"Retail": 0.24, "Office": 0.21, "Industrial": 0.20, "Hospitality": 0.20, "Healthcare": 0.15}
REGION_MIX = {"Dublin": 0.38, "Regional cities": 0.33, "Rest of State": 0.29}


def _months():
    out, (y, m) = [], START
    while (y, m) <= END:
        out.append((y, m))
        y, m = (y, m + 1) if m < 12 else (y + 1, 1)
    return out


MONTHS = _months()
NM = len(MONTHS)
MI = {ym: i for i, ym in enumerate(MONTHS)}


def month_end(i):
    y, m = MONTHS[i]
    return dt.date(y + (m == 12), m % 12 + 1, 1) - dt.timedelta(days=1)


def quarter_of(i):
    y, m = MONTHS[i]
    return y, (m - 1) // 3 + 1


QUARTERS = sorted({quarter_of(i) for i in range(NM)})
QI = {q: k for k, q in enumerate(QUARTERS)}
NQ = len(QUARTERS)


def quarter_end(k):
    y, q = QUARTERS[k]
    return dt.date(y + (q == 4), (q * 3) % 12 + 1, 1) - dt.timedelta(days=1)


# ------------------------------------------------------------------ the index

WAY = {
    "Retail":      [(2004, 1, 100), (2007, 2, 141), (2009, 4, 82), (2012, 4, 55), (2015, 4, 66), (2019, 4, 80),
                    (2020, 3, 71), (2022, 2, 79), (2024, 2, 74), (2026, 3, 77), (2026, 4, 77)],
    "Office":      [(2004, 1, 100), (2007, 2, 152), (2009, 4, 85), (2013, 1, 50), (2016, 4, 92), (2019, 4, 116),
                    (2020, 3, 110), (2022, 2, 119), (2024, 4, 89), (2026, 3, 91), (2026, 4, 91)],
    "Industrial":  [(2004, 1, 100), (2007, 2, 131), (2009, 4, 86), (2012, 4, 60), (2016, 4, 84), (2019, 4, 110),
                    (2020, 3, 112), (2022, 2, 137), (2024, 2, 125), (2026, 3, 131), (2026, 4, 131)],
    "Hospitality": [(2004, 1, 100), (2007, 2, 137), (2009, 4, 78), (2012, 4, 52), (2016, 4, 79), (2019, 4, 96),
                    (2020, 4, 74), (2021, 4, 86), (2022, 4, 101), (2024, 4, 97), (2026, 3, 99), (2026, 4, 99)],
    "Healthcare":  [(2004, 1, 100), (2007, 2, 125), (2009, 4, 92), (2013, 1, 70), (2016, 4, 89), (2019, 4, 105),
                    (2020, 3, 103), (2022, 2, 112), (2024, 4, 106), (2026, 3, 109), (2026, 4, 109)],
}
REGION_AMP = {"Dublin": 1.18, "Regional cities": 1.0, "Rest of State": 0.82}
RECOVERY_DAMP = 0.5      # the moves after the 2012 trough, scaled from the waypoints


def index_true(rng):
    out = {}
    for s in SECTORS:
        xs = [QI[(y, q)] for y, q, _ in WAY[s]]
        ys = [math.log(v / 100.0) for _, _, v in WAY[s]]
        base = np.interp(np.arange(NQ), xs, ys)
        k0 = QI[(2012, 4)]
        base[k0 + 1:] = base[k0] + RECOVERY_DAMP * (base[k0 + 1:] - base[k0])
        for r in REGIONS:
            noise = np.cumsum(rng.normal(0, 0.0045, NQ))
            noise -= np.linspace(0, 1, NQ) * noise[-1]
            out[(s, r)] = 100.0 * np.exp(base * REGION_AMP[r] + noise)
    return out


def index_releases(true, rng):
    """the publisher's vintages: a first release some six weeks after the quarter, revised a quarter and two
    quarters later; only releases out by the as-of date exist"""
    rel = {}
    for key in sorted(true):
        rows = []
        for k in range(NQ):
            v = true[key][k]
            first = quarter_end(k) + dt.timedelta(days=int(rng.integers(38, 47)))
            vals = (v * (1 + rng.normal(0, 0.006)), v * (1 + rng.normal(0, 0.0025)), v)
            for n, d in enumerate((first, first + dt.timedelta(days=91), first + dt.timedelta(days=182))):
                if d <= AS_OF:
                    rows.append((k, n, d, round(float(vals[n]), 2)))
        rel[key] = rows
    return rel


def published(rel_rows, upto):
    """quarter -> index value as published on date `upto` (the latest release out by then)"""
    best = {}
    for k, n, d, x in rel_rows:
        if d <= upto and (k not in best or n > best[k][0]):
            best[k] = (n, x)
    return {k: x for k, (n, x) in best.items()}


# ------------------------------------------------------------------ the simulation


class World:
    pass


def build(seed=SEED):
    rng = np.random.default_rng(seed)
    w = World()
    w.true = index_true(rng)
    w.rel = index_releases(w.true, rng)
    w.props, w.facs = [], []
    plan = []
    for y in sorted(ORIG_COUNTS):
        for _ in range(ORIG_COUNTS[y]):
            plan.append((y, int(rng.integers(1, 13))))
    plan.sort()
    for (y, m) in plan:
        s = str(rng.choice(SECTORS, p=[SECTOR_MIX[k] for k in SECTORS]))
        r = str(rng.choice(REGIONS, p=[REGION_MIX[k] for k in REGIONS]))
        boom = y <= 2008
        ltv0 = float(np.clip(rng.normal(0.80 if boom else 0.67, 0.065), 0.50, 0.88))
        amount = float(min(max(np.exp(rng.normal(math.log(780e3), 0.72)), 90e3), 9.5e6))
        amount = round(amount, -3)
        props = [new_property(w, s, r, (y, m), amount / ltv0)]
        if rng.random() < 0.045:
            props.append(new_property(w, s, r, (y, m), amount * 0.30 / ltv0))
        bullet = (not boom) and rng.random() < 0.62
        if bullet:
            term = int(rng.choice([60, 84], p=[0.6, 0.4]))
            io = term
        else:
            term = int(rng.choice([180, 240]) if boom else rng.choice([144, 180, 240], p=[0.3, 0.4, 0.3]))
            io = int(rng.choice([0, 36, 60], p=[0.45, 0.30, 0.25]) if boom else rng.choice([0, 24, 36], p=[0.5, 0.3, 0.2]))
        rate = float(np.round(rng.normal(5.4 if boom else 4.6, 0.5), 2))
        new_facility(w, (y, m), amount, term, io, rate, len(w.facs), props, None)
    simulate(w, rng)
    return w


def new_property(w, s, r, ym, v0):
    w.props.append(dict(sector=s, region=r, first=ym, v0=v0, insp=[]))
    return len(w.props) - 1


def new_facility(w, ym, amount, term, io, rate, borrower, props, topup_of):
    w.facs.append(dict(orig=ym, amount=amount, term=term, io=io, rate=rate, borrower=borrower, props=props,
                       topup_of=topup_of, end=None, end_kind=None, grades={}, extensions=[],
                       bullet=(io == term)))
    return len(w.facs) - 1


def balance(f, i):
    """scheduled balance at month index i (interest-only, then an annuity to term; a bullet facility holds its
    balance to maturity, extensions included); None outside the term"""
    k = i - MI[f["orig"]]
    if k < 0 or k >= f["term"]:
        return None
    if f.get("bullet"):
        return f["amount"]
    r = f["rate"] / 1200.0
    b = f["amount"]
    if k <= f["io"]:
        return b
    n = f["term"] - f["io"]
    j = k - f["io"]
    return b * ((1 + r) ** n - (1 + r) ** j) / ((1 + r) ** n - 1)


def simulate(w, rng):
    props, facs = w.props, w.facs
    cap = len(props) + 1500
    logdev = np.zeros(cap)       # log(true value / last inspection rolled forward by the true index)
    svar = np.zeros(cap)         # variance of logdev since the last inspection
    anchor_i = np.full(cap, -1)
    anchor_v = np.zeros(cap)
    sig_m = np.zeros(cap)
    w.defaults = []
    w.state = {}
    w.at_risk, w.hits = {}, {}
    starts = {}
    for fi, f in enumerate(facs):
        starts.setdefault(MI[f["orig"]], []).append(fi)
    alive, grade = set(), {}

    def inspect(p, i, reason, extra=0.0):
        s = props[p]["sector"]
        if anchor_i[p] < 0:
            tv = props[p]["v0"] * math.exp(rng.normal(0, 0.02))
        else:
            k0, k1 = QI[quarter_of(anchor_i[p])], QI[quarter_of(i)]
            tv = (anchor_v[p] * w.true[(s, props[p]["region"])][k1] / w.true[(s, props[p]["region"])][k0]
                  * math.exp(logdev[p] - KAPPA * (i - anchor_i[p]) / 12.0))
        val = round(tv * math.exp(extra + rng.normal(0, VALUER_SD)), -3)
        props[p]["insp"].append((i, val, reason))
        logdev[p] = math.log(tv / val)
        svar[p] = VALUER_SD ** 2
        anchor_i[p], anchor_v[p] = i, val
        return val, tv

    for i in range(NM):
        y, m = MONTHS[i]
        for fi in starts.get(i, []):
            f = facs[fi]
            alive.add(fi)
            grade[fi] = int(rng.choice([3, 4, 5, 6, 7], p=[0.15, 0.30, 0.30, 0.18, 0.07]))
            for p in f["props"]:
                sig_m[p] = SIGMA[props[p]["sector"]] / math.sqrt(12)
                if anchor_i[p] < 0 or f["topup_of"] is not None:
                    inspect(p, i, "origination" if anchor_i[p] < 0 else "top-up")
        logdev += rng.normal(0, 1, cap) * sig_m
        svar += sig_m ** 2
        if i >= MI[(2021, 1)]:
            w.state[i] = (logdev.copy(), anchor_i.copy(), anchor_v.copy())
        order = sorted(alive)
        # the 2010 to 2011 revaluation of the book after the crash, then the committee's three-yearly cycle
        # from 2012 to 2019, both for facilities of 500,000 or more
        if (2010, 6) <= (y, m) <= (2011, 9):
            for fi in order:
                f = facs[fi]
                if f["amount"] < 500e3:
                    continue
                for p in f["props"]:
                    if anchor_i[p] < MI[(2010, 6)] and rng.random() < 0.09:
                        inspect(p, i, "revaluation")
        if CYCLE_START <= (y, m) <= CYCLE_END:
            for fi in order:
                f = facs[fi]
                if f["amount"] < 500e3:
                    continue
                for p in f["props"]:
                    if i - anchor_i[p] >= 33 + (p % 7) and rng.random() < 0.5:
                        old = logdev[p]
                        inspect(p, i, "cycle")
                        if old < -0.12 and grade[fi] < 8:
                            grade[fi] += 1
                        elif old > 0.12 and grade[fi] > 1:
                            grade[fi] -= 1
        # annual review on the anniversary month
        for fi in order:
            f = facs[fi]
            if f["orig"][1] == m and MI[f["orig"]] < i:
                c = CYCLE[y]
                u = rng.random()
                if u < 0.095 * c and grade[fi] < 8:
                    grade[fi] += 2 if (rng.random() < 0.18 * c and grade[fi] < 7) else 1
                elif u > 1 - 0.105 / c and grade[fi] > 1:
                    grade[fi] -= 1
        # top-ups from 2014: a second facility to the same borrower on the same property, inspected afresh
        if (y, m) >= (2014, 1):
            for fi in order:
                f = facs[fi]
                if f["topup_of"] is None and grade[fi] <= 5 and rng.random() < 0.0011:
                    amt = round(f["amount"] * float(rng.uniform(0.25, 0.55)), -3)
                    nf = new_facility(w, (y, m), amt, int(rng.choice([84, 120])), 0,
                                      float(np.round(rng.normal(4.9, 0.4), 2)), f["borrower"], list(f["props"]), fi)
                    alive.add(nf)
                    grade[nf] = grade[fi]
                    for p in f["props"]:
                        inspect(p, i, "top-up")
        # defaults: the grade's chance in the year's conditions, tilted by the drift since the last inspection;
        # a default takes every live facility of the borrower
        order = sorted(alive)
        hit = {}
        for fi in order:
            f = facs[fi]
            ps = f["props"]
            if (y, m) >= RECORD_START:
                band = min(int((i - min(anchor_i[q] for q in ps)) / 12), 12)
                w.at_risk[band] = w.at_risk.get(band, 0.0) + (1 - (1 - MASTER_PD[grade[fi]]) ** (1 / 12)) * CYCLE[y]
            d = float(np.mean(logdev[ps]))
            pd_m = 1 - (1 - MASTER_PD[grade[fi]]) ** (1 / 12)
            if rng.random() < pd_m * CYCLE[y] * max(0.05, 1.0 - GAMMA * d):
                hit[f["borrower"]] = fi
        for fi in order:
            f = facs[fi]
            if f["borrower"] in hit:
                alive.discard(fi)
                f["end"], f["end_kind"] = i, "default"
                f["grades"][i] = "D"
        for b, fi in sorted(hit.items()):
            if (y, m) >= RECORD_START:
                ps = facs[fi]["props"]
                band = min(int((i - min(anchor_i[q] for q in ps)) / 12), 12)
                w.hits[band] = w.hits.get(band, 0) + 1
            group = sorted(g for g in range(len(facs)) if facs[g]["borrower"] == b and facs[g]["end"] == i
                           and facs[g]["end_kind"] == "default")
            w.defaults.append(dict(borrower=b, month=i, facs=group,
                                   drift={p: float(logdev[p]) for g in group for p in facs[g]["props"]}))
        # closures: maturity, prepayment, refinancing away
        for fi in sorted(alive):
            f = facs[fi]
            if f["bullet"] and MI[f["orig"]] + f["term"] == i + 1 and rng.random() < 0.75:
                ext = int(rng.choice([36, 48, 60]))
                f["term"] += ext
                f["extensions"].append((i, ext))
            bal = balance(f, i + 1)
            if bal is None or bal < 1.0 or rng.random() < 0.0034:
                alive.discard(fi)
                f["end"], f["end_kind"] = i, ("maturity" if bal is None or bal < 1.0 else "repaid")
        if (y, m) >= (2018, 12):
            for fi in alive:
                facs[fi]["grades"][i] = grade[fi]
    w.alive_end = sorted(alive)
    w.grade_end = {fi: grade[fi] for fi in alive}
    w.logdev_end = logdev[: len(props)].copy()
    w.svar_end = svar[: len(props)].copy()
    workouts(w, rng)


def workouts(w, rng):
    """for each default: the inspection the bank orders (one to two months on), the receiver's sale six to twenty
    months after the default, selling costs, and the proceeds shared across the borrower's facilities"""
    props = w.props
    w.sales = []
    for ev in w.defaults:
        i = ev["month"]
        # from 2022 a facility of 500,000 or more is referred to the workout unit some months before it defaults,
        # and the unit has the security inspected at referral
        referral = None
        if any(w.facs[g]["amount"] >= REFERRAL_MIN for g in ev["facs"]):
            m0 = i - int(rng.integers(2, 7))
            if m0 >= MI[REFERRAL_FROM]:
                referral = m0
        for p in sorted(ev["drift"]):
            s, r = props[p]["sector"], props[p]["region"]
            j = min(i + int(rng.integers(1, 3)), NM - 1)
            li, lv, _ = [x for x in props[p]["insp"] if x[0] <= i][-1]
            k0, k1 = QI[quarter_of(li)], QI[quarter_of(j)]
            dev = ev["drift"][p] + rng.normal(0, SIGMA[s] * math.sqrt((j - i) / 12))
            tv = lv * w.true[(s, r)][k1] / w.true[(s, r)][k0] * math.exp(dev - KAPPA * (j - li) / 12.0)
            val = round(tv * (1 - DELTA[s]) * math.exp(rng.normal(0, VALUER_SD)), -3)
            props[p]["insp"].append((j, val, "default"))
            if referral is not None and li < referral:
                ld, ai, av = w.state[referral]
                a_i, a_v = int(ai[p]), float(av[p])
                r0, r1 = QI[quarter_of(a_i)], QI[quarter_of(referral)]
                tv0 = a_v * w.true[(s, r)][r1] / w.true[(s, r)][r0] * math.exp(ld[p] - KAPPA * (referral - a_i) / 12.0)
                props[p]["insp"].append((referral, round(tv0 * math.exp(rng.normal(0, VALUER_SD)), -3), "referral"))
                props[p]["insp"].sort(key=lambda x: x[0])
            sale_m = i + int(rng.integers(6, 21))
            price = round(val * SALE_FACTOR * math.exp(rng.normal(0, SALE_SD)), -3)
            costs = round(COST_RATE * price + COST_FIXED, 0)
            w.sales.append(dict(prop=p, default_month=i, insp_month=j, insp_value=val, sale_month=sale_m,
                                price=price, costs=costs, borrower=ev["borrower"], facs=ev["facs"]))
        ev["ead"] = {g: round(balance(w.facs[g], i) or w.facs[g]["amount"], 2) for g in ev["facs"]}
