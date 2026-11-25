#!/usr/bin/env python3
"""task4 architecture 14, loop 1, the core: Wrenfold Brewery's five container pools (50, 30 and 20 litre kegs,
firkins and kilderkins) against the fleet standard's lines for the 2027 summer season (no shortfall in any week of
it: hold; a shortfall under the maker's minimum run: hire for the season; the minimum run or more: buy).

A weekly miniature of the world the generator simulates day by day: the trade's cellars line by line, the containers
the trade loses, the store's racking runs, one count of every site on 30 November 2026 and a register that never
loses a container. No record holds what the trade has in its cellars in a summer week, how many containers are
still alive, or what the store will hold under next year's range. The miniature writes the records the pack will
hold (weekly deliveries, the count by purchase lot, the register by purchase lot, the reps' cellar counts of full
containers with the day of each line's last delivery, the store's stock by week, the 2027 plan), and every
estimator below reads those records only. It proves, before any pack exists, that

  S1  a rep's cellar count sees the full containers of a line on its order day and never the empties waiting for
      the dray, so what a line holds has to be rebuilt from its own delivery cycle before the trade's stock can be
      carried to a summer week,
  S2  the store holds each beer a racking run at a time, so its stock follows the runs and the range on sale; the
      share of a run a beer holds beyond its cover is measured on the beers' own Monday stocks, never assumed,
  S3  the register never loses a container, so the containers the trade loses have to be estimated from how the
      share of each purchase lot still seen on site falls with the lot's age,

each move one pool's call when made the hurried way, none reaches the call when fixed alone, each files a wrong call
when pushed past its fitted value, the four routes the runs take (generous, calibrated, hedge, cut-off) each file a
wrong call, and a run that loses any one of them is priced under the bar on the rubric. Nothing here reads a prompt
or solves a task.

    python3 task4/generator/core.py            the core table and CORE PASS level N
    python3 task4/generator/core.py --detail   every figure on every route
    python3 task4/generator/core.py --forcing  each fitted input moved by its spread
"""
import datetime as dt
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".claude", "skills", "stumping"))
import corelib  # noqa: E402

SEED = int(os.environ.get("CORE_SEED", 72417))
D0 = dt.date(2023, 12, 4)            # week 0 starts here; the dockets open that Monday
WH = 156                             # history weeks; the count of every site closes week 155 (30 November 2026)
WF = 43                              # 2027 weeks carried: to the week starting 20 September 2027
SEASON = range(WH + 22, WH + WF)     # the summer the order is sized for: weeks starting 3 May to 20 September 2027
ESTATE_WEEK = WH + 19                # Maplestead's pubs are listed from 12 April 2027, a third a week
RUNS_WEEK = WH + 22                  # the summer racking plan and the summer range start on 3 May 2027
FLOAT = 2.0 / 7.0                    # the standard's float: two days of deliveries
HOT_RANK = -2                        # the upper end of the 80 per cent range: the second highest of the ten summers
POOLS = ("K50", "K30", "K20", "FIR", "KIL")
NAMES = {"K50": "50 litre keg", "K30": "30 litre keg", "K20": "20 litre keg", "FIR": "firkin", "KIL": "kilderkin"}
LOT_YEARS = tuple(range(2011, 2024))  # the purchase lots older than the docket record, one a year

# per pool: weekly sales at the seasonal mean, the season's amplitude (casks sell best in the cold months), the
# response to a warm day, growth a year, lines, containers a line holds whatever it sells (a) and per container sold
# a week and week of interval and cover (b), the share of emptied containers the trade loses, the weeks of sales in
# depots, transit, wash and repair (c2), the store's cover in weeks, the beers with their share of the pool and their
# racking run before and under the summer 2027 plan, beers added to the summer range, the estate's lines and their
# weekly sales, the world's shortfall the fleet is placed at, lots bought inside the docket record (week,
# containers), the maker's minimum run and the cellar counts the reps made
W = {
    "K50": dict(S0=4300, amp=0.20, k=0.045, g=0.000, L=2700, a=2.2, b=0.50, loss=0.0100, c2=0.55, cover=0.35,
                beers=[("PIL", 0.62, 400, 2400), ("GLD", 0.38, 300, 1400)], new27=[],
                estate=(720, 0.90), place=4800, lots=[(15, 1800), (70, 1200)], moq=3500, counts=1800),
    "K30": dict(S0=2400, amp=0.10, k=0.012, g=0.005, L=2600, a=2.1, b=0.50, loss=0.0085, c2=0.55, cover=0.35,
                beers=[("PAL", 0.35, 250, 800), ("IPA", 0.25, 165, 550), ("HER", 0.22, 165, 500),
                       ("BLK", 0.18, 125, 400)], new27=[],
                estate=(450, 1.30), place=2000, lots=[(15, 900), (70, 600)], moq=1500, counts=1800),
    "K20": dict(S0=640, amp=0.22, k=0.024, g=0.030, L=1800, a=2.0, b=0.50, loss=0.0060, c2=0.60, cover=0.35,
                beers=[("F%02d" % i, 1.0 / 8, 120, 200) for i in range(1, 9)],
                new27=[("F%02d" % i, 200) for i in range(9, 19)],
                estate=(150, 0.45), place=650, lots=[(15, 650), (70, 650)], moq=1200, counts=900),
    "FIR": dict(S0=1500, amp=-0.15, k=0.0, g=-0.020, L=1700, a=3.0, b=0.50, loss=0.0150, c2=0.60, cover=0.35,
                beers=[("BIT", 0.60, 300, 700), ("MLD", 0.20, 150, 270), ("SEA", 0.20, 240, 600)],
                new27=[("SUM", 300), ("HAR", 300)],
                estate=(160, 0.60), place=1600, lots=[(40, 800)], moq=1200, counts=900),
    "KIL": dict(S0=250, amp=-0.15, k=0.0, g=-0.030, L=170, a=3.0, b=0.50, loss=0.0200, c2=0.60, cover=0.35,
                beers=[("BIK", 1.0, 80, 360)], new27=[],
                estate=(0, 0.0), place=-450, lots=[], moq=600, counts=250),
}
SCRAP = 0.0009                        # share of returning containers condemned at the wash
NEW_SHARE = 0.03                      # a beer added to the 2027 range takes this share of its pool


def week_date(i):
    return D0 + dt.timedelta(days=7 * i + 3)


def doy(i):
    return week_date(i).timetuple().tm_yday


def normal_temp(i):
    return 13.5 + 7.5 * math.cos(2 * math.pi * (doy(i) - 205) / 365.0)


def seas(i, amp):
    return 1.0 + amp * math.cos(2 * math.pi * (doy(i) - 200) / 365.0)


def warm(t, k):
    return 1.0 + k * max(t - 17.0, 0.0) + 0.006 * min(t - 17.0, 0.0)


def beers_at(p, i):
    """the pool's beers in week i: (code, share of the pool's deliveries, racking run)"""
    w = W[p]
    if i < RUNS_WEEK:
        return [(c, sh, q26) for c, sh, q26, q27 in w["beers"]]
    left = 1.0 - NEW_SHARE * len(w["new27"])
    return [(c, sh * left, q27) for c, sh, q26, q27 in w["beers"]] + [(c, NEW_SHARE, q) for c, q in w["new27"]]


# ------------------------------------------------------------------------------------------------- the world
def lines_of(p, rng):
    """each line's weekly sales at the seasonal mean and its delivery interval in weeks (busy cellars twice a week)"""
    w = W[p]
    r = np.exp(rng.normal(0.0, 0.6, w["L"]))
    r *= w["S0"] / r.sum()
    busy = rng.random(w["L"]) < 1.0 / (1.0 + np.exp(-(r - np.quantile(r, 0.8)) / (0.25 * r.mean())))
    return r, np.where(busy, 0.5, 1.0)


def path27(p, q, anom27=None):
    """the pool's 2027 weeks at the given summer's weather: sales, the trade's stock and the stock the site needs"""
    w = W[p]
    ne, re_ = w["estate"]
    out = []
    for i in range(WH, WH + WF):
        t = normal_temp(i) + (0.0 if anom27 is None else anom27[i - WH])
        base = w["S0"] * (1 + w["g"]) ** (i / 52.0) * seas(i, w["amp"]) * warm(t, w["k"])
        live = 0.0 if i < ESTATE_WEEK else min(1.0, (i - ESTATE_WEEK + 1) / 3.0)
        es = ne * re_ * live * seas(i, w["amp"]) * warm(t, w["k"])
        est = w["a"] * ne * live + w["b"] * 2.0 * es
        cellar = w["a"] * w["L"] + w["b"] * q["m"] * base + est
        E = base + es
        store = sum(w["cover"] * sh * E + run / 2.0 for c, sh, run in beers_at(p, i))
        out.append(dict(i=i, E=E, cellar=cellar, est=est, store=store, other=w["c2"] * E, fl=FLOAT * E))
    return out


def simulate(seed=SEED):
    rng = np.random.default_rng(seed)
    anom = np.zeros(WH)
    for i in range(1, WH):
        anom[i] = 0.5 * anom[i - 1] + rng.normal(0, 2.2)
    record = np.zeros((10, WF))                                  # the ten summers on record
    for y in range(10):
        e = rng.normal(0, 2.54)
        for j in range(WF):
            e = 0.5 * e + rng.normal(0, 2.2)
            record[y, j] = e
    out = {"anom": anom, "record": record, "pool": {}}
    for p in POOLS:
        w = W[p]
        r, iv = lines_of(p, rng)
        m = float((r * (iv + 1.0)).sum() / r.sum())              # the cellars' weeks of interval and cover, by sales
        q = dict(r=r, iv=iv, m=m)
        level = np.array([w["S0"] * (1 + w["g"]) ** (i / 52.0) * seas(i, w["amp"]) *
                          warm(normal_temp(i) + anom[i], w["k"]) for i in range(WH)])
        S = level * np.exp(rng.normal(0, 0.03, WH))               # the week's deliveries, lumpy about the level
        cellar = w["a"] * w["L"] + w["b"] * m * level             # a line stocks to what it sells, not to a week's dockets
        store = np.zeros(WH)
        stock = {}
        by_beer = {code: np.zeros(WH) for code, sh, run in beers_at(p, 0)}
        for i in range(WH):
            for code, sh, run in beers_at(p, i):
                d = sh * S[i]
                s = stock.get(code)
                if s is None:
                    s = w["cover"] * d + run * rng.random()
                s -= d
                while s < w["cover"] * d:                        # racked a whole run at a time
                    s += run
                stock[code] = s
                store[i] += s
                by_beer[code][i] = s
        other = w["c2"] * S
        lost = rng.binomial(S.astype(int), w["loss"]).astype(float)
        scrap = rng.binomial((S - lost).astype(int), SCRAP).astype(float)
        fut = path27(p, q)
        lost27 = np.array([f["E"] * w["loss"] for f in fut])
        scrap27 = np.array([f["E"] * SCRAP for f in fut])
        bought = np.zeros(WH + WF)
        for wk, n in w["lots"]:
            bought[wk] += n
        # the fleet is placed so the world's own shortfall in the pool's busiest 2027 week is the pool's place
        need27 = np.array([f["cellar"] + f["store"] + f["other"] + f["fl"] for f in fut])
        drain27 = np.cumsum(lost27 + scrap27)
        sidx = [f["i"] - WH for f in fut if f["i"] in SEASON]
        pk = max(sidx, key=lambda j: need27[j] + drain27[j])
        drain = float(lost.sum() + scrap.sum() + drain27[pk])
        alive0 = round((need27[pk] - w["place"] + drain - bought.sum()) / 10.0) * 10.0
        alive = np.zeros(WH + WF + 1)
        alive[0] = alive0
        allost = np.concatenate([lost, lost27])
        allscrap = np.concatenate([scrap, scrap27])
        for i in range(WH + WF):
            alive[i + 1] = alive[i] - allost[i] - allscrap[i] + bought[i]
        onsite = alive[1:WH + 1] - cellar                         # at each history week's close
        idle = onsite - store - other - FLOAT * S
        idle27 = alive[WH + 1:] - need27
        q.update(S=S, cellar=cellar, store=store, store_beer=by_beer, other=other, lost=lost, scrap=scrap, alive=alive,
                 onsite=onsite, idle=idle, idle27=idle27, fut=fut, peak=WH + pk, need27=need27, alive0=alive0)
        q.update(lots_of(p, q, rng))
        out["pool"][p] = q
    return out


def lots_of(p, q, rng):
    """the fleet by purchase lot at the count: a lot a year from 2011 to 2023 and the lots bought inside the docket
    record. Every lot loses the same share of what is alive each year (a lost container is any container), the
    register keeps every container bought that was not condemned at the wash, and the count finds on site a random
    share of what is alive."""
    w = W[p]
    frac = q["lost"] / q["alive"][:WH]
    keep = np.ones(WH + 1)                                       # survival from the start of week i to the count
    for i in range(WH - 1, -1, -1):
        keep[i] = keep[i + 1] * (1.0 - frac[i] - q["scrap"][i] / q["alive"][i])
    fleet = float(q["alive"][WH - 52])                           # the fleet a year before the count
    rl = float(q["lost"][WH - 52:].sum()) / fleet                 # the share of the fleet the trade loses in a year
    rs = float(q["scrap"][WH - 52:].sum()) / fleet                # the share condemned at the wash and struck off
    rho_y = {y: rl * math.exp(rng.normal(0, 0.05)) for y in LOT_YEARS}
    size = rng.uniform(0.6, 1.4, len(LOT_YEARS)) * np.linspace(1.25, 0.85, len(LOT_YEARS))
    surv0 = []
    for y in LOT_YEARS:                                          # from a mid-year purchase to the start of week 0
        s = (1.0 - rho_y[y] - rs) ** 0.42
        for z in range(y + 1, 2024):
            s *= 1.0 - rho_y[z] - rs
        surv0.append(s)
    surv0 = np.array(surv0)
    bought0 = size * q["alive0"] / float((size * surv0).sum())   # each old lot as bought
    alive_old = bought0 * surv0 * keep[0]
    age = [(dt.date(2026, 11, 30) - dt.date(y, 7, 1)).days / 365.25 for y in LOT_YEARS]
    reg = [b * (1.0 - rs) ** a for b, a in zip(bought0, age)]
    alive = list(alive_old)
    for wk, n in w["lots"]:
        a = (WH - wk) / 52.18
        age.append(a)
        reg.append(n * (1.0 - rs) ** a)
        alive.append(n * keep[wk])
    alive = np.array(alive)
    alive *= q["alive"][WH] / alive.sum()                        # the lots add to the fleet alive at the count
    alive_i = np.floor(alive).astype(int)
    onsite_n = int(round(q["alive"][WH] - q["cellar"][WH - 1]))
    ons = rng.multivariate_hypergeometric(alive_i, min(onsite_n, int(alive_i.sum())))
    return dict(lot_age=np.array(age), lot_reg=np.rint(np.array(reg)), lot_alive=alive, lot_ons=ons.astype(float),
                rho=rl)


def truth_at(p, world, anom27=None):
    """the world's own largest weekly shortfall in the 2027 season, at the given summer's weather"""
    q = world["pool"][p]
    fut = path27(p, q, anom27)
    short = [(f["cellar"] + f["store"] + f["other"] + f["fl"] - q["alive"][f["i"] + 1], f) for f in fut
             if f["i"] in SEASON]
    return max(short, key=lambda x: x[0])


# ------------------------------------------------------------------------------------------------- the records
def records(world, seed=SEED + 1):
    """what the pack will hold, per pool: weekly deliveries, the count of 30 November 2026 by purchase lot, the
    register by purchase lot, the store's weekly stock, the reps' cellar counts (the full containers of a line on
    the day of the call, with the days since the line's last delivery and its weekly sales, both built from the
    dockets), each line's rate and interval, the plan"""
    rng = np.random.default_rng(seed)
    R = {"anom": world["anom"].copy(), "record": world["record"], "pool": {}}
    for p in POOLS:
        w, q = W[p], world["pool"][p]
        take = dict(onsite=float(q["lot_ons"].sum()), register=float(q["lot_reg"].sum()),
                    other=float(q["other"][WH - 1]), flow=float(q["S"][WH - 1]),
                    condemned=float(q["scrap"][WH - 52:].sum()))  # struck off the register in the year to the count
        n = w["counts"]
        idx = rng.integers(0, w["L"], n)
        wk = rng.integers(60, WH, n)
        rate = q["r"][idx] * q["S"][wk] / w["S0"]
        iv = q["iv"][idx]
        held = np.maximum(np.rint(w["a"] + w["b"] * rate * (iv + 1.0) + rng.normal(0, 0.45, n)), 1.0)
        # a rep calls on the account's order day: four to six days after the dray on a weekly round (three in a
        # week with a bank holiday), two or three days after it on a twice-weekly one
        days = np.where(iv == 1.0, rng.choice([3, 4, 5, 6], n, p=[0.15, 0.27, 0.33, 0.25]),
                        rng.choice([2, 3], n, p=[0.40, 0.60])).astype(float)
        # a line draws steadily, so the containers emptied since the dray called are its sales over those days,
        # caught at a random point of the container on dispense
        sold = np.minimum(np.floor(rate * days / 7.0 * np.exp(rng.normal(0, 0.08, n)) + rng.random(n)), held - 1.0)
        full = held - sold                                       # the count: full containers and the one on dispense
        R["pool"][p] = dict(take=take, flow=q["S"].copy(), store=q["store"].copy(),
                            store_beer={c: v.copy() for c, v in q["store_beer"].items()},   # the Monday stock by beer
                            flow_beer={c: sh * q["S"] for c, sh, run in beers_at(p, 0)},     # the dockets by beer
                            # a line's weekly sales at the call: its share of its type's deliveries over the record
                            # times the type's deliveries that week; or its own dockets over thirteen or four weeks,
                            # lumpier because a line takes whole containers
                            count_rate_share=rate * np.exp(rng.normal(0, 0.03, n)),
                            count_rate13=rate * np.exp(rng.normal(0, 0.06, n)),
                            count_rate=rate * np.exp(rng.normal(0, 0.10, n)),
                            count_iv=iv, count_full=full, count_days=days, count_week=wk,
                            line_rate=q["r"], line_iv=q["iv"], estate=w["estate"], beers26=beers_at(p, 0),
                            lot_age=q["lot_age"].copy(), lot_reg=q["lot_reg"].copy(), lot_ons=q["lot_ons"].copy())
    return R


# ------------------------------------------------------------------------------------------------- the estimators
GOLDEN = dict(swing="lines", recon="days", store="runs", loss="age", fit="ols", rate="count_rate_share",
              count_months="all", harmonics=2, hinge=0.0, share_fit="between", level="fit", age_fit="wls", age_drop=0,
              alive="lots", clock="deliveries",
              x_b=1.0, x_cov=1.0, x_lam=1.0, x_del=1.0)   # the forcing battery's multipliers on the fitted inputs
# the hurried choice at each stump, and the same stump pushed past its fitted value to the far end a run might set
HURRIED = {"S1": {"recon": "face"}, "S2": {"store": "cover"}, "S3": {"loss": "none"}}
OVER = {"S1": {"swing": "prop"}, "S2": {"store": "wholerun"}, "S3": {"loss": "writeoff"}}
RIGOROUS = {"recon": "face", "store": "regress", "loss": "none"}
# the routes the runs take, each with every stump it does not touch made the golden's way (the strongest opponent)
RUN = {
    "hedge": {"recon": "face", "store": "cover", "loss": "none"},
    "generous": {"recon": "whole", "store": "wholerun", "loss": "writeoff"},
    "calibrated": {"recon": "face", "swing": "level"},
    "cutoff": {"recon": "cut4"},
    "cutoff:three days": {"recon": "cut3"},
    "cutoff:summer counts": {"recon": "face", "count_months": "summer"},
    "cutoff:weekly rounds": {"recon": "face", "fit": "weekly"},
}


def fit_sales(flow, anom, harmonics, hinge=0.0):
    """weekly deliveries on the season, the trend and the week's temperature, with a bend at the temperature the
    record itself fits best (moved by `hinge` degrees in the battery)"""
    y = np.log(flow)

    def fit(h0):
        def row(i, temp, level=1.0):
            x = [level, level * i / 52.0]
            for h in range(1, harmonics + 1):
                x += [math.cos(2 * math.pi * h * doy(i) / 365.0), math.sin(2 * math.pi * h * doy(i) / 365.0)]
            return x + [max(temp - h0, 0.0), min(temp - h0, 0.0)]
        X = np.array([row(i, normal_temp(i) + anom[i]) for i in range(WH)])
        beta, res = np.linalg.lstsq(X, y, rcond=None)[:2]
        return float(((X @ beta - y) ** 2).sum()), beta, row
    best = min((fit(h0)[0], h0) for h0 in np.arange(12.0, 22.01, 0.5))[1]
    sse, beta, row = fit(best + hinge)
    return (lambda i, temp: float(math.exp(np.dot(beta, row(i, temp))))), \
           (lambda i, temp: float(math.exp(np.dot(beta, row(i, temp, 0.0)))))


def fit_cellar(rec, o):
    """containers a line holds: a number whatever it sells (a), a number per container it sells a week (b1) and a
    number per container it sells a week and week between deliveries (b2). The count is of full containers, so what
    the line holds is the count and the containers it has sold since the dray last called (`days`); or the count as
    it stands (`face`), with half a delivery or a whole one added (`half`, `whole`), on the calls soonest after a
    delivery (`cut3`, `cut4`), or with the days since the delivery as a term of the fit (`joint`)"""
    rate, iv, full, days, wk = rec[o["rate"]], rec["count_iv"], rec["count_full"], rec["count_days"], rec["count_week"]
    keep = np.ones(len(rate), bool)
    if o["count_months"] == "summer":
        keep &= np.array([4 <= week_date(int(i)).month <= 9 for i in wk])
    recon = o["recon"]
    if recon.startswith("cut"):
        keep &= days <= np.where(iv == 1.0, float(recon[3:]), 2.0)
    if o["fit"] == "weekly":
        keep &= iv == 1.0
    rate, iv, full, days = rate[keep], iv[keep], full[keep], days[keep]
    sold = rate * days / 7.0
    if recon == "joint":
        a, b1, b2, bd = np.linalg.lstsq(np.column_stack([np.ones(len(rate)), rate, rate * iv, sold]), full,
                                        rcond=None)[0]
        return float(a), (lambda x: float(b1 + b2 * x)), float(bd)
    held = full + {"days": sold, "half": rate * iv / 2.0, "whole": rate * iv}.get(recon, 0.0)
    if o["fit"] == "weekly":                                      # the weekly rounds only: one slope, carried to all
        b, a = np.polyfit(rate, held, 1)
        return float(a), (lambda x: float(b)), None
    if o["fit"] == "ols":
        a, b1, b2 = np.linalg.lstsq(np.column_stack([np.ones(len(rate)), rate, rate * iv]), held, rcond=None)[0]
        return float(a), (lambda x: float(b1 + b2 * x)), None
    slope = {}
    icpt = {}
    for x in sorted(set(iv.tolist())):                           # one line through the counts of each interval
        k = iv == x
        slope[x], icpt[x] = np.polyfit(rate[k], held[k], 1)
    return float(icpt[1.0]), (lambda x: float(slope[x])), None


def fit_store(R, o):
    """the cold store's stock beer by beer. A beer's Monday stock saws between its cover and its cover and a run, and
    a heavy week of deliveries is itself what draws it down, so the week-to-week movement inside a beer says nothing
    of its cover; the beers' means do. The golden fits each beer's mean Monday stock (the last 104 Mondays) on its
    mean weekly deliveries (a cover in weeks of deliveries) and on its racking run (the share of a run a beer holds
    beyond its cover), across every beer of every container type. Nothing files the share and no type's own record
    can show it, because a type's runs never changed in the record; the beers' different runs do. The battery fits
    the same on every Monday of the record, on the beer-weeks themselves with one cover, and on the beer-weeks with
    a cover for each container type. Returns the share and each type's cover"""
    kind = o["share_fit"]
    first = 0 if kind == "between_all" else 52
    by_type = kind == "panel"
    rows = []
    for k, p in enumerate(POOLS):
        rec = R["pool"][p]
        for code, sh, run in rec["beers26"]:
            st, fl = rec["store_beer"][code][first:], rec["flow_beer"][code][first:]
            if kind.startswith("between"):                        # each beer's mean stock on its mean deliveries
                st, fl = np.array([st.mean()]), np.array([fl.mean()])
            for a, b in zip(st, fl):
                x = np.zeros(len(POOLS) + 1)
                x[k if by_type else 0] = b
                x[-1] = run
                rows.append((x, a))
    X, y = np.array([r[0] for r in rows]), np.array([r[1] for r in rows])
    use = [j for j in range(X.shape[1]) if np.abs(X[:, j]).sum() > 0]
    beta = np.zeros(X.shape[1])
    beta[use] = np.linalg.lstsq(X[:, use], y, rcond=None)[0]
    return dict(theta=float(beta[-1]), cov={p: float(beta[k if by_type else 0]) for k, p in enumerate(POOLS)})


def fit_age(rec, o):
    """the share of each purchase lot the count found on site against the lot's age: its fall with age is the share
    of the fleet that leaves each year, and its level at age nought the share of the fleet that is on site. Returns
    the yearly rate of leaving (continuous) and the share on site"""
    age, reg, ons = rec["lot_age"], rec["lot_reg"], rec["lot_ons"]
    k = ons > 0
    order = np.argsort(age)
    if o["age_drop"] == "newest":
        k[order[0]] = False
    elif o["age_drop"] == "oldest":
        k[order[-1]] = False
    x, y, wt = age[k], np.log(ons[k] / reg[k]), ons[k]
    if o["loss"] == "origin":                                     # every lot's whole absence from site read as loss
        return float(-(wt * x * y).sum() / (wt * x * x).sum()), 1.0
    if o["age_fit"] == "ols":
        wt = np.ones(len(x))
    if o["age_fit"] == "ends":                                    # the oldest four lots against the newest four
        idx = np.argsort(x)
        lo, hi = idx[:4], idx[-4:]
        lam = (math.log(ons[k][lo].sum() / reg[k][lo].sum()) - math.log(ons[k][hi].sum() / reg[k][hi].sum())) / \
              (np.average(x[hi], weights=reg[k][hi]) - np.average(x[lo], weights=reg[k][lo]))
        f = ons[k][lo].sum() / reg[k][lo].sum() * math.exp(lam * np.average(x[lo], weights=reg[k][lo]))
        return float(lam), float(f)
    sw = np.sqrt(wt)
    b, a = np.linalg.lstsq(np.column_stack([x * sw, sw]), y * sw, rcond=None)[0]
    return float(-b), float(math.exp(a))


_CACHE = {}


def cached(kind, R, p, o, keys, fn):
    k = (kind, id(R), p) + tuple(o[x] for x in keys)
    if k not in _CACHE:
        _CACHE[k] = fn()
    return _CACHE[k]


def chain(R, p, opt=None, anom27=None):
    """one pool's shortfall in its busiest week of the 2027 season from the records, with every step's option"""
    o = dict(GOLDEN)
    o.update(opt or {})
    w, rec = W[p], R["pool"][p]
    T, flow = rec["take"], rec["flow"]
    a, slope, bd = cached("cellar", R, p, o, ("recon", "fit", "rate", "count_months"), lambda: fit_cellar(rec, o))
    lr, li = rec["line_rate"], rec["line_iv"]                     # the trade's containers per container sold a week
    b, m = slope(1.0) / 2.0, 2.0 * sum(slope(x) * float(lr[li == x].sum()) for x in set(li.tolist())) / \
        slope(1.0) / float(lr.sum())
    b *= o["x_b"]
    predict, shape = cached("sales", R, p, o, ("harmonics", "hinge"),
                            lambda: fit_sales(flow, R["anom"], o["harmonics"], o["hinge"]))
    if o["level"] == "fit":
        lev = predict(WH - 1, normal_temp(WH - 1) + R["anom"][WH - 1])
    else:
        lev = float(flow[WH - o["level"]:WH].mean())
    year = float(flow[WH - 52:WH].sum())
    # the fleet alive, and the containers the trade loses in a year
    if o["loss"] == "none":                                       # the register read as the fleet
        alive, year_loss = T["register"], 0.0
    elif o["loss"] == "writeoff":                                 # what the register holds beyond the site and the
        held0 = a * w["L"] + b * m * lev                          # cellars, written off over the three years on record
        alive, year_loss = T["onsite"] + held0, max(T["register"] - T["onsite"] - held0, 0.0) / 3.0
    else:
        lam_y, share = cached("age", R, p, o, ("loss", "age_fit", "age_drop"), lambda: fit_age(rec, o))
        alive = float((rec["lot_reg"] * np.exp(-lam_y * rec["lot_age"])).sum()) if o["alive"] == "lots" else \
            T["onsite"] / share
        year_loss = alive * (math.exp(lam_y) - 1.0)
    year_loss *= o["x_lam"]
    lam = year_loss / year                                        # per container delivered
    scrap = T["condemned"] / year                                 # condemned at the wash, per container delivered
    alive_out = alive - T["onsite"]                               # the trade's containers at the count, alive
    if o["loss"] == "none":                                       # no loss known: the counts as they stand, every line
        o2 = dict(o, recon="face")
        af, sf, _ = cached("cellar", R, p, o2, ("recon", "fit", "rate", "count_months"), lambda: fit_cellar(rec, o2))
        alive_out = af * w["L"] + sum(sf(x) * float(lr[li == x].sum()) for x in set(li.tolist())) * lev / w["S0"]
    if o["swing"] == "level":                                     # the counts as they stand, scaled to that level
        scale = alive_out / (a * w["L"] + b * m * lev)
        a, b = a * scale, b * scale
    # the store: its cover in weeks of deliveries, beside the share of a racking run each beer on sale holds beyond
    # it, both measured on the beers' own Monday stocks; or a whole run for each beer, the far end
    full26 = float(sum(run for c, sh, run in rec["beers26"]))
    reg = np.polyfit(flow[52:], rec["store"][52:], 1)
    if o["store"] == "wholerun":
        part = 1.0
        cov = (float(rec["store"][52:].mean()) - full26) / float(flow[52:].mean())
    else:
        fs = cached("store", R, "all", o, ("share_fit",), lambda: fit_store(R, o))
        part, cov = fs["theta"], fs["cov"][p]
    cov *= o["x_cov"]
    ne, re_ = rec["estate"]
    c2 = T["other"] / (lev if o["level"] == "fit" else float(flow[WH - o["level"]:WH].mean()))
    path, cum = [], 0.0
    for i in range(WH, WH + WF):
        j = i - 52
        temp = normal_temp(i) + (0.0 if anom27 is None else anom27[i - WH])
        F = predict(i, temp) * o["x_del"]
        live = 0.0 if i < ESTATE_WEEK else min(1.0, (i - ESTATE_WEEK + 1) / 3.0)
        es = ne * re_ * live * shape(i, temp)
        est = a * ne * live + b * 2.0 * es
        D = F + es
        if o["swing"] == "prop":                                  # the trade's stock moved with the deliveries
            swing = alive_out * (D / lev - 1.0)
        else:
            swing = b * m * (F - lev) + est
        if o["store"] in ("runs", "wholerun"):
            store = sum(cov * sh * D + part * run for c, sh, run in beers_at(p, i))
        elif o["store"] == "cover":
            store = float(rec["store"][j - 2:j + 3].mean() / flow[j - 2:j + 3].mean()) * D
        else:
            store = float(reg[1] + reg[0] * D)
        cum += (lam * D if o["clock"] == "deliveries" else year_loss / 52.18) + scrap * D
        need = swing + store + c2 * D + FLOAT * D                 # beside the trade's containers at the count
        path.append(dict(i=i, need=need, short=need - T["onsite"] + cum, swing=swing, store=store))
    season = [x for x in path if x["i"] in SEASON]
    pick = max(season, key=lambda x: x["short"])
    return dict(short=pick["short"], week=pick["i"], swing=pick["swing"], store=pick["store"], year_loss=year_loss,
                rise=max(x["swing"] for x in season), fullest=max(x["store"] for x in season), theta=part, cov=cov,
                lam=lam, a=a, b=b, m=m, alive=alive, days_coef=bd)


def direct(R, p, anom27=None):
    """the register read as the fleet: the requirement built from the records as they stand (the cellar counts
    carried to every line, the store at its weeks of cover) less every container the register holds"""
    w, rec = W[p], R["pool"][p]
    o = dict(GOLDEN, recon="face", store="cover", loss="none")
    g = chain(R, p, o, anom27)
    a, slope, _ = fit_cellar(rec, o)
    lr, li = rec["line_rate"], rec["line_iv"]
    lev = fit_sales(rec["flow"], R["anom"], 2)[0](WH - 1, normal_temp(WH - 1) + R["anom"][WH - 1])
    held = a * w["L"] + sum(slope(x) * float(lr[li == x].sum()) for x in set(li.tolist())) * lev / w["S0"]
    return g["short"] + rec["take"]["onsite"] + held - rec["take"]["register"]


def hot(fn):
    """a figure at the upper end of the 80 per cent range over the ten summers on record (the second highest)"""
    return float(sorted(fn(y) for y in range(10))[HOT_RANK])


FAMILY = [
    ("the golden's conventions", {}),
    ("the cellar counts fitted one line for each delivery interval", {"fit": "byclass"}),
    ("a line's weekly sales from thirteen weeks of its own dockets, not its share of the type's", {"rate": "count_rate13"}),
    ("the summer's cellar counts only", {"count_months": "summer"}),
    ("the bend in the weather response a degree lower", {"hinge": -1.0}),
    ("the bend in the weather response a degree higher", {"hinge": 1.0}),
    ("one seasonal harmonic in the deliveries fit", {"harmonics": 1}),
    ("three seasonal harmonics in the deliveries fit", {"harmonics": 3}),
    ("the store's stock fitted between beers on every Monday of the record, not the last 104", {"share_fit": "between_all"}),
    ("the store's stock fitted on the beer-weeks themselves, one cover", {"share_fit": "one_cover"}),
    ("the store's stock fitted on the beer-weeks with a cover for each container type", {"share_fit": "panel"}),
    ("deliveries at the count over its last two weeks, not the fit's value for its week", {"level": 2}),
    ("deliveries at the count as its own week's", {"level": 1}),
    ("the lots fitted unweighted", {"age_fit": "ols"}),
    ("the lots fitted without the newest lot", {"age_drop": "newest"}),
    ("the lots fitted without the oldest lot", {"age_drop": "oldest"}),
    ("the oldest four lots against the newest four", {"age_fit": "ends"}),
    ("the fleet alive as the count over the fitted share on site", {"alive": "share"}),
    ("the loss carried on the calendar, not on deliveries", {"clock": "calendar"}),
    ("thirteen weeks of own dockets and the lines by interval together", {"rate": "count_rate13", "fit": "byclass"}),
    ("the summer counts and the two-week level together", {"count_months": "summer", "level": 2}),
    ("the unweighted lots and the calendar loss together", {"age_fit": "ols", "clock": "calendar"}),
]


# each fitted input moved by its spread, one at a time and to the same side together: the call has to hold
FORCING = [
    ("what a line holds per container sold, 20 per cent down", {"x_b": 0.8}),
    ("what a line holds per container sold, 20 per cent up", {"x_b": 1.2}),
    ("the store's cover, 20 per cent down", {"x_cov": 0.8}),
    ("the store's cover, 20 per cent up", {"x_cov": 1.2}),
    ("the containers lost in a year, 20 per cent down", {"x_lam": 0.8}),
    ("the containers lost in a year, 20 per cent up", {"x_lam": 1.2}),
    ("the season's deliveries, 5 per cent down", {"x_del": 0.95}),
    ("the season's deliveries, 5 per cent up", {"x_del": 1.05}),
]


def spreads(R, p, reps=120, seed=11):
    """each fitted input's own measured spread for one pool, as a share of its value: what a line holds per
    container sold (the counts resampled), the store's cover (the weeks resampled in blocks of four), the containers
    lost in a year (the lots resampled) and the worst week's deliveries (the fit's residuals resampled)"""
    rng = np.random.default_rng(seed)
    rec = R["pool"][p]
    lr, li = rec["line_rate"], rec["line_iv"]
    n = len(rec["count_full"])
    bm = []
    for _ in range(reps):
        idx = rng.integers(0, n, n)
        r2 = dict(rec)
        for k in ("count_rate_share", "count_rate", "count_rate13", "count_iv", "count_full", "count_days", "count_week"):
            r2[k] = rec[k][idx]
        sl = fit_cellar(r2, GOLDEN)[1]
        bm.append(sum(sl(x) * float(lr[li == x].sum()) for x in set(li.tolist())) / float(lr.sum()))
    half = sum(run for c, sh, run in rec["beers26"]) * fit_store(R, GOLDEN)["theta"]
    st, fl = rec["store"][52:], rec["flow"][52:]
    cv = []
    for _ in range(reps):
        idx = np.concatenate([np.arange(k * 4, k * 4 + 4) for k in rng.integers(0, len(st) // 4, len(st) // 4)])
        cv.append((st[idx].mean() - half) / fl[idx].mean())
    nl = len(rec["lot_age"])
    lams = []
    for _ in range(reps):
        idx = rng.integers(0, nl, nl)
        r2 = dict(rec)
        for k in ("lot_age", "lot_reg", "lot_ons"):
            r2[k] = rec[k][idx]
        if len(set(r2["lot_age"].tolist())) < 4:
            continue
        lam_y = fit_age(r2, GOLDEN)[0]
        lams.append(math.exp(lam_y) - 1.0)
    g = chain(R, p)
    predict = fit_sales(rec["flow"], R["anom"], 2)[0]
    fit = np.array([predict(i, normal_temp(i) + R["anom"][i]) for i in range(WH)])
    res = np.log(rec["flow"]) - np.log(fit)
    pk = [fit_sales(fit * np.exp(rng.choice(res, len(res))), R["anom"], 2)[0](g["week"], normal_temp(g["week"]))
          for _ in range(reps // 3)]
    return dict(x_b=float(np.std(bm) / np.mean(bm)), x_cov=float(np.std(cv) / abs(np.mean(cv))),
                x_lam=float(np.std(lams) / np.mean(lams)),
                x_del=float(np.std(pk) / predict(g["week"], normal_temp(g["week"]))))


def band_of(x, lines):
    return sum(1 for ln in lines[1:] if x >= ln) + (1 if x > lines[0] else 0)


def lattice_opts():
    keys = {}
    ids = sorted(HURRIED)
    for mask in range(1, 2 ** len(ids)):
        o = {}
        for k, s in enumerate(ids):
            if mask >> k & 1:
                o.update(HURRIED[s])
        keys["+".join(s for k, s in enumerate(ids) if mask >> k & 1)] = o
    return keys


def days_check(R):
    """the falsification check: across every pool's cellar counts in one fit, each pool with its own relation to a
    line's sales and delivery interval, the fall in the full containers counted for each container the line has
    sold since its last delivery"""
    X, y = [], []
    for k, p in enumerate(POOLS):
        rec = R["pool"][p]
        rate, iv, full, days = rec[GOLDEN["rate"]], rec["count_iv"], rec["count_full"], rec["count_days"]
        blk = np.zeros((len(rate), 3 * len(POOLS) + 1))
        blk[:, 3 * k], blk[:, 3 * k + 1], blk[:, 3 * k + 2], blk[:, -1] = 1.0, rate, rate * iv, rate * days / 7.0
        X.append(blk)
        y.append(full)
    return float(np.linalg.lstsq(np.vstack(X), np.concatenate(y), rcond=None)[0][-1])


def main():
    detail = "--detail" in sys.argv
    world = simulate()
    R = records(world)
    if "--forcing" in sys.argv:
        gold = {p: band_of(chain(R, p)["short"], [0.0, float(W[p]["moq"])]) for p in POOLS}
        bad = 0
        print("%-58s %s" % ("fitted input moved", "  ".join("%7s" % p for p in POOLS)))
        for name, o in FORCING:
            v = {p: chain(R, p, o)["short"] for p in POOLS}
            same = all(band_of(v[p], [0.0, float(W[p]["moq"])]) == gold[p] for p in POOLS)
            bad += 0 if same else 1
            print("%-58s %s  %s" % (name, "  ".join("%7.0f" % v[p] for p in POOLS), "same call" if same else "CALL MOVES"))
        sp = {p: spreads(R, p) for p in POOLS}
        for k in ("x_b", "x_cov", "x_lam", "x_del"):
            print("%-58s %s" % ("measured spread of %s, per cent" % k, "  ".join("%7.1f" % (100 * sp[p][k]) for p in POOLS)))
        for side, sign in (("down", -1.0), ("up", 1.0)):                 # two spreads each, all to one side
            v = {p: chain(R, p, {k: 1.0 + sign * 2.0 * sp[p][k] for k in sp[p]})["short"] for p in POOLS}
            same = all(band_of(v[p], [0.0, float(W[p]["moq"])]) == gold[p] for p in POOLS)
            bad += 0 if same else 1
            print("%-58s %s  %s" % ("all four %s together, two measured spreads each" % side,
                                    "  ".join("%7.0f" % v[p] for p in POOLS), "same call" if same else "CALL MOVES"))
        return 1 if bad else 0
    slack = {p: (float(world["pool"][p]["idle"].min()), float(world["pool"][p]["idle27"][:ESTATE_WEEK - WH].min()))
             for p in POOLS}
    if min(min(v) for v in slack.values()) < 0:
        print("WORLD FAIL  a pool is short of containers in the record or before the estate arrives: %s" % ", ".join(
            "%s %.0f and %.0f" % (p, v[0], v[1]) for p, v in slack.items()))
        return 1
    rec10 = world["record"]
    lat_o = lattice_opts()
    reflex = "+".join(sorted(HURRIED))
    truth = {p: truth_at(p, world)[0] for p in POOLS}
    truth_hot = {p: hot(lambda y: truth_at(p, world, rec10[y])[0]) for p in POOLS}
    G = {p: chain(R, p) for p in POOLS}

    def fig(field, opt=None, pools=POOLS, heat=False):
        if heat:
            return float(sum(hot(lambda y: chain(R, p, opt, rec10[y])[field]) for p in pools))
        return float(sum(chain(R, p, opt)[field] for p in pools))
    base = ("hedge", "generous", "calibrated", "cutoff")
    members = {}
    for p in POOLS:
        members[p] = dict(lines=[0.0, float(W[p]["moq"])], truth=truth[p], golden=G[p]["short"],
                          family=[chain(R, p, o)["short"] for _, o in FAMILY],
                          routes={"direct": direct(R, p), "rigorous": chain(R, p, RIGOROUS)["short"]})
    lat = {k: {p: chain(R, p, o)["short"] for p in POOLS} for k, o in lat_o.items()}
    comps = [("C1", "rise"), ("C2", "fullest"), ("C3", "year_loss")]
    figures = []
    for cid, field in comps:
        routes = {"rigorous": fig(field, RIGOROUS)}
        routes.update({k: fig(field, RUN[k]) for k in base})
        figures.append(dict(id=cid, block="component", golden=fig(field), family=[fig(field, o) for _, o in FAMILY],
                            lattice={k: fig(field, o) for k, o in lat_o.items()}, routes=routes))
    # the asks: the fleet account, one row a pool and one sentence a row (the containers lost over the year to the
    # count, the trade's rise to its summer peak, the store at its fullest, the largest weekly shortfall in the
    # planning case and in the hot case), so a pool's row is one criterion and needs all five of its figures
    for p in POOLS:
        figures.append(dict(id="A-%s" % p, block="ask", member=p, sentence="row-%s" % p))
        routes = {"rigorous": fig("short", RIGOROUS, (p,), True)}
        routes.update({k: fig("short", RUN[k], (p,), True) for k in base})
        figures.append(dict(id="H-%s" % p, block="ask", sentence="row-%s" % p, golden=fig("short", None, (p,), True),
                            family=[fig("short", o, (p,), True) for _, o in FAMILY],
                            lattice={k: fig("short", o, (p,), True) for k, o in lat_o.items()}, routes=routes))
        for tag, field in (("T", "rise"), ("S", "fullest"), ("L", "year_loss")):
            routes = {"rigorous": fig(field, RIGOROUS, (p,))}
            routes.update({k: fig(field, RUN[k], (p,)) for k in base})
            figures.append(dict(id="%s-%s" % (tag, p), block="ask", sentence="row-%s" % p, golden=fig(field, None, (p,)),
                                family=[fig(field, o, (p,)) for _, o in FAMILY],
                                lattice={k: fig(field, o, (p,)) for k, o in lat_o.items()}, routes=routes))
    run_routes = {k: {p: chain(R, p, o)["short"] for p in POOLS} for k, o in RUN.items()}
    over = {s: {p: chain(R, p, o)["short"] for p in POOLS} for s, o in OVER.items()}
    # what forces the call between the ways of reading a cellar count: the counts' own fall with the containers a
    # line has sold since its last delivery, which no file states and no route but the golden's expects
    dc = days_check(R)
    falsification = dict(check="across the cellar counts, with a line's weekly sales and delivery interval held, the "
                               "full containers counted fall by one for each container the line has sold since its "
                               "last delivery (the dockets give the day); no file holds a line's empties, the "
                               "trade's stock or any pool's shortfall",
                         observes_target=False, truth=dc, golden=-1.0,
                         rivals={"the count as it stands is what the line holds": 0.0,
                                 "the count and a whole delivery is what the line holds": 0.0,
                                 "the count and half a delivery is what the line holds": 0.0})
    spec = dict(task="task4 architecture 14 loop 1", call="lines", members=members, lattice=lat,
                falsification=falsification, run_routes=run_routes, figures=figures, stumps={
                    "S1": dict(axis="what", opens="K50", sides={"over": over["S1"]},
                               said_out_loud="A rep's cellar count is of the full containers of a line on its order "
                                             "day, and the empties wait there for the dray, so what the trade holds "
                                             "is more than the counts show and does not move in step with its sales.",
                               steps_left=5, precedents=["L56", "L57", "L07"]),
                    "S2": dict(axis="when", opens="K20", sides={"over": over["S2"]},
                               said_out_loud="The store receives each beer a whole racking run at a time, so its "
                                             "stock follows the runs and the number of beers on sale, and both "
                                             "change in 2027.",
                               steps_left=4, precedents=["N17", "N02", "L37"]),
                    "S3": dict(axis="who", opens="FIR", sides={"over": over["S3"]},
                               said_out_loud="A container lost in the trade is never taken off the register, so the "
                                             "register is not the fleet and nothing records how many are lost.",
                               steps_left=4, precedents=["L53", "L43", "N13"]),
                })
    if detail:
        print("containers short in the pool's worst week of the 2027 season")
        print("%-4s %7s %7s %7s %7s | %7s %7s %7s | %7s %7s %7s | lines" % (
            "pool", "truth", "golden", "fam lo", "fam hi", "S1", "S2", "S3", "reflex", "direct", "rigor"))
        for p in POOLS:
            mm = members[p]
            print("%-4s %7.0f %7.0f %7.0f %7.0f | %7.0f %7.0f %7.0f | %7.0f %7.0f %7.0f | 0 / %d  %s (truth %s)" % (
                p, truth[p], mm["golden"], min(mm["family"]), max(mm["family"]), lat["S1"][p], lat["S2"][p],
                lat["S3"][p], lat[reflex][p], mm["routes"]["direct"], mm["routes"]["rigorous"], W[p]["moq"],
                week_date(G[p]["week"]), week_date(truth_at(p, world)[1]["i"])))
        print("each stump pushed past its fitted value, and the routes the runs take")
        for name, mp in [("S1 over: moved with deliveries", over["S1"]), ("S2 over: a whole run a beer", over["S2"]),
                         ("S3 over: every absence a loss", over["S3"])] + sorted(run_routes.items()):
            print("  %-34s %s  %s" % (name, " ".join("%7.0f" % mp[p] for p in POOLS),
                                      [band_of(mp[p], [0.0, float(W[p]["moq"])]) for p in POOLS]))
        for name, o in (("half a delivery added to every count", {"recon": "half"}),
                        ("a whole delivery added to every count", {"recon": "whole"})):
            v = {p: chain(R, p, o) for p in POOLS}
            print("  %-34s %s  %s  rise %6.0f" % (name[:34], " ".join("%7.0f" % v[p]["short"] for p in POOLS),
                                                  [band_of(v[p]["short"], [0.0, float(W[p]["moq"])]) for p in POOLS],
                                                  sum(v[p]["swing"] for p in POOLS)))
        print("variant deviations from the golden")
        for name, o in FAMILY[1:]:
            print("  %-68s" % name[:68], " ".join("%6.0f" % (chain(R, p, o)["short"] - G[p]["short"]) for p in POOLS))
        print("components: golden, family, lattice")
        for f in figures[:3]:
            print("  %s golden %7.0f family %7.0f to %7.0f | S1 %7.0f S2 %7.0f S3 %7.0f reflex %7.0f | %s" % (
                f["id"], f["golden"], min(f["family"]), max(f["family"]), f["lattice"]["S1"], f["lattice"]["S2"],
                f["lattice"]["S3"], f["lattice"][reflex], " ".join("%s %.0f" % kv for kv in sorted(f["routes"].items()))))
        print("hot summer: truth, golden")
        for f in [x for x in figures if x["id"].startswith("H-")]:
            p = f["id"][2:]
            print("  %-4s %7.0f %7.0f | %7.0f %7.0f %7.0f | %7.0f" % (
                p, truth_hot[p], f["golden"], f["lattice"]["S1"], f["lattice"]["S2"], f["lattice"]["S3"],
                f["lattice"][reflex]))
        print("the world")
        for p in POOLS:
            q = world["pool"][p]
            rec = R["pool"][p]
            lam_y, share = fit_age(rec, GOLDEN)
            af = fit_cellar(rec, dict(GOLDEN, recon="face"))
            print("  %-4s register %6.0f, alive %6.0f (fitted %6.0f), on site %6.0f, in the trade %6.0f; idle least "
                  "in history %6.0f, at the 2026 peak %6.0f; a %.2f b %.2f (%.2f, %.2f; as counted a %.2f b %.2f); "
                  "leaving a year %.3f fitted, %.3f world; on site share %.3f; year loss %5.0f (%5.0f); rise %5.0f "
                  "store %5.0f" % (
                      p, rec["take"]["register"], q["alive"][WH], G[p]["alive"], rec["take"]["onsite"],
                      q["cellar"][WH - 1], q["idle"].min(), q["idle"][104:156].min(), G[p]["a"], G[p]["b"], W[p]["a"],
                      W[p]["b"], af[0], af[1](1.0) / 2.0, 1.0 - math.exp(-lam_y), q["rho"], share, G[p]["year_loss"],
                      q["lost"][104:156].sum(), G[p]["swing"], G[p]["store"]))
        tw = {p: truth_at(p, world)[1] for p in POOLS}
        print("  the world's own rise in the trade %s, store %s, year loss %s" % (
            " ".join("%.0f" % (tw[p]["cellar"] - world["pool"][p]["cellar"][WH - 1]) for p in POOLS),
            " ".join("%.0f" % tw[p]["store"] for p in POOLS),
            " ".join("%.0f" % world["pool"][p]["lost"][WH - 52:].sum() for p in POOLS)))
        print("  the falsification check: counted fall per container sold since the delivery %.3f (the golden's "
              "model -1, every rival's 0)" % dc)
        print()
    return corelib.run(spec)


if __name__ == "__main__":
    sys.exit(main())
