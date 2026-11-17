#!/usr/bin/env python3
"""task4 architecture 14, the core: Wrenfold Brewery's five container pools (50, 30 and 20 litre kegs, firkins and
kilderkins) against the fleet standard's lines for the 2027 summer season (no shortfall in any week of it: hold; a shortfall under the maker's minimum run: hire for the season; the minimum run or more: buy).

A weekly miniature of the world the generator simulates day by day: the trade's cellars line by line, the containers
the trade loses, the store's racking runs, the four 30 November stocktakes and a register that never loses a
container. No record holds what the trade has in its cellars in a summer week, how many containers are still alive,
or what the store will hold under next year's range. The miniature writes the records the pack will hold (weekly
deliveries, the stocktakes, the register, the reps' cellar counts, the store's stock by week, the tags of the one
tracked pool, the 2027 plan), and every estimator below reads those records only. It proves, before any pack exists,
that

  S1  a cellar holds containers by the line and its delivery interval, so the trade's stock does not move in step
      with its sales,
  S2  the store holds each beer a racking run at a time, so its stock follows the runs and the range on sale,
  S3  the containers the trade loses where nothing is tracked have to come from the stock account, not from the
      tracked pool,

each move one pool's call when made the hurried way, none reaches the call when fixed alone, and a run that loses any
one of them is priced under the bar on the rubric. Nothing here reads a prompt or solves a task.

    python3 task4/generator/core.py            the core table and CORE PASS level N
    python3 task4/generator/core.py --detail   every figure on every route
"""
import datetime as dt
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".claude", "skills", "stumping"))
import corelib  # noqa: E402

SEED = int(os.environ.get("CORE_SEED", 72417))
D0 = dt.date(2023, 12, 4)            # week 0 starts here; the reconciliation stocktake is the Thursday before
WH = 156                             # history weeks; the stocktakes sit at week boundaries 0, 52, 104 and 156
WF = 43                              # 2027 weeks carried: to the week starting 20 September 2027
SEASON = range(WH + 22, WH + WF)     # the summer the order is sized for: weeks starting 3 May to 20 September 2027
ESTATE_WEEK = WH + 19                # Maplestead's pubs are listed from 12 April 2027, a third a week
RUNS_WEEK = WH + 22                  # the summer racking plan and the summer range start on 3 May 2027
FLOAT = 2.0 / 7.0                    # the standard's float: two days of deliveries
HOT_RANK = -2                        # the upper end of the 80 per cent range: the second highest of the ten summers
POOLS = ("K50", "K30", "K20", "FIR", "KIL")
NAMES = {"K50": "50 litre keg", "K30": "30 litre keg", "K20": "20 litre keg", "FIR": "firkin", "KIL": "kilderkin"}

# per pool: weekly sales at the seasonal mean, the season's amplitude (casks sell best in the cold months), the
# response to a warm day, growth a year, lines, containers a line holds whatever it sells (a) and per container sold
# a week and week of interval and cover (b), the share of emptied containers the trade loses, the weeks of sales in
# depots, transit, wash and repair (c2), the store's cover in weeks, the beers with their share of the pool and their
# racking run before and under the summer 2027 plan, beers added to the summer range, the estate's lines and their weekly
# sales, the world's shortfall the fleet is placed at, lots bought since the reconciliation (week, containers), the
# maker's minimum run, counts the reps made, and whether the pool carries tags
W = {
    "K50": dict(S0=4300, amp=0.20, k=0.045, g=0.000, L=2700, a=2.2, b=0.50, loss=0.0066, c2=0.55, cover=0.35,
                beers=[("PIL", 0.62, 400, 1600), ("GLD", 0.38, 300, 1000)], new27=[],
                estate=(300, 0.60), place=1000, lots=[(15, 1800), (70, 1200)], moq=2000, counts=1000, tagged=False),
    "K30": dict(S0=2400, amp=0.05, k=0.012, g=0.005, L=2600, a=2.1, b=0.50, loss=0.0085, c2=0.55, cover=0.35,
                beers=[("PAL", 0.35, 250, 800), ("IPA", 0.25, 165, 550), ("HER", 0.22, 165, 500),
                       ("BLK", 0.18, 125, 400)], new27=[],
                estate=(900, 0.39), place=3300, lots=[(15, 900), (70, 600)], moq=1500, counts=1000, tagged=False),
    "K20": dict(S0=640, amp=0.14, k=0.024, g=0.030, L=1800, a=2.0, b=0.50, loss=0.0030, c2=0.60, cover=0.35,
                beers=[("F%02d" % i, 1.0 / 8, 120, 200) for i in range(1, 9)],
                new27=[("F%02d" % i, 200) for i in range(9, 19)],
                estate=(150, 0.20), place=650, lots=[(15, 650), (70, 650)], moq=1200, counts=700, tagged=True),
    "FIR": dict(S0=1500, amp=-0.04, k=0.0, g=-0.020, L=1700, a=3.0, b=0.50, loss=0.0150, c2=0.60, cover=0.35,
                beers=[("BIT", 0.60, 300, 540), ("MLD", 0.20, 150, 270), ("SEA", 0.20, 240, 480)],
                new27=[("SUM", 240), ("HAR", 240)],
                estate=(160, 0.60), place=1500, lots=[(40, 800)], moq=1200, counts=650, tagged=False),
    "KIL": dict(S0=250, amp=-0.04, k=0.0, g=-0.030, L=170, a=3.0, b=0.50, loss=0.0090, c2=0.60, cover=0.35,
                beers=[("BIK", 1.0, 80, 120)], new27=[],
                estate=(0, 0.0), place=-450, lots=[], moq=600, counts=160, tagged=False),
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
    record = np.zeros((10, WF))                                  # the ten summers on record, 2016 to 2025
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
        S = np.array([w["S0"] * (1 + w["g"]) ** (i / 52.0) * seas(i, w["amp"]) * warm(normal_temp(i) + anom[i], w["k"])
                      * math.exp(rng.normal(0, 0.03)) for i in range(WH)])
        cellar = w["a"] * w["L"] + w["b"] * m * S
        store = np.zeros(WH)
        stock = {}
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
        register = np.zeros(WH + WF + 1)
        alive[0] = register[0] = alive0
        allost = np.concatenate([lost, lost27])
        allscrap = np.concatenate([scrap, scrap27])
        for i in range(WH + WF):
            alive[i + 1] = alive[i] - allost[i] - allscrap[i] + bought[i]
            register[i + 1] = register[i] - allscrap[i] + bought[i]
        onsite = alive[1:WH + 1] - cellar                         # at each history week's close
        idle = onsite - store - other - FLOAT * S
        idle27 = alive[WH + 1:] - need27
        q.update(S=S, cellar=cellar, store=store, other=other, lost=lost, scrap=scrap, alive=alive, register=register,
                 onsite=onsite, idle=idle, idle27=idle27, fut=fut, peak=WH + pk, need27=need27, alive0=alive0)
        out["pool"][p] = q
    return out


def truth_at(p, world, anom27=None):
    """the world's own largest weekly shortfall in the 2027 season, at the given summer's weather"""
    q = world["pool"][p]
    fut = path27(p, q, anom27)
    short = [(f["cellar"] + f["store"] + f["other"] + f["fl"] - q["alive"][f["i"] + 1], f) for f in fut
             if f["i"] in SEASON]
    return max(short, key=lambda x: x[0])


# ------------------------------------------------------------------------------------------------- the records
def records(world, seed=SEED + 1):
    """what the pack will hold, per pool: weekly deliveries, the four stocktakes, the register, the store's weekly
    stock, the reps' cellar counts, each line's rate and interval, the tracked pool's weekly census, the plan"""
    rng = np.random.default_rng(seed)
    R = {"anom": world["anom"].copy(), "record": world["record"], "pool": {}}
    for p in POOLS:
        w, q = W[p], world["pool"][p]
        takes = {}
        for b in (0, 52, 104, 156):
            j = max(b - 1, 0)
            takes[b] = dict(onsite=float(q["alive"][b] - q["cellar"][j]), register=float(q["register"][b]),
                            other=float(q["other"][j]), flow=float(q["S"][j]))
        n = w["counts"]
        idx = rng.integers(0, w["L"], n)
        wk = rng.integers(60, WH, n)
        rate = q["r"][idx] * q["S"][wk] / w["S0"]
        held = np.rint(w["a"] + w["b"] * rate * (q["iv"][idx] + 1.0) + rng.normal(0, 0.7, n))
        R["pool"][p] = dict(takes=takes, flow=q["S"].copy(), store=q["store"].copy(),
                            count_rate=rate, count_iv=q["iv"][idx], count_held=held, count_week=wk,
                            line_rate=q["r"], line_iv=q["iv"], estate=w["estate"], beers26=beers_at(p, 0),
                            census=q["cellar"].copy() if w["tagged"] else None,
                            tag_loss=float(q["lost"][104:156].sum()) if w["tagged"] else None,
                            tag_trips=float(q["S"][104:156].sum()) if w["tagged"] else None)
    return R


# ------------------------------------------------------------------------------------------------- the estimators
GOLDEN = dict(swing="lines", store="runs", loss="account", loss_years=1, trade_change=True, fit="ols",
              count_months="all", harmonics=2, hinge=0.0, cover="mean", other="mean", level=4, census=False,
              x_b=1.0, x_cov=1.0, x_lam=1.0, x_del=1.0)   # the forcing battery's multipliers on the fitted inputs
HURRIED = {"S1": {"swing": "prop"}, "S2": {"store": "cover"}, "S3": {"loss": "tag"}}
RIGOROUS = {"swing": "tracked", "store": "regress", "loss": "tag"}


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
    number per container it sells a week and week between deliveries (b2); or one line per delivery interval"""
    rate, iv, held, wk = rec["count_rate"], rec["count_iv"], rec["count_held"], rec["count_week"]
    if o["count_months"] == "summer":
        keep = np.array([4 <= week_date(int(i)).month <= 9 for i in wk])
        rate, iv, held = rate[keep], iv[keep], held[keep]
    if o["fit"] == "ols":
        a, b1, b2 = np.linalg.lstsq(np.column_stack([np.ones(len(rate)), rate, rate * iv]), held, rcond=None)[0]
        return float(a), (lambda x: float(b1 + b2 * x))
    slope = {}
    icpt = {}
    for x in sorted(set(iv.tolist())):                           # one line through the counts of each interval
        k = iv == x
        slope[x], icpt[x] = np.polyfit(rate[k], held[k], 1)
    return float(icpt[1.0]), (lambda x: float(slope[x]))


def tracked_response(R):
    """the tracked pool's own response: the share by which its containers in the trade move when its deliveries
    move by one per cent, from its weekly census"""
    t = R["pool"]["K20"]
    slope, icpt = np.polyfit(t["flow"][52:], t["census"][52:], 1)
    return float(slope * t["flow"][52:].mean() / t["census"][52:].mean())


def chain(R, p, opt=None, anom27=None):
    """one pool's shortfall in its busiest week of the 2027 season from the records, with every step's option"""
    o = dict(GOLDEN)
    o.update(opt or {})
    w, rec = W[p], R["pool"][p]
    T, flow = rec["takes"], rec["flow"]
    tagged = rec["census"] is not None
    X = {b: T[b]["register"] - T[b]["onsite"] for b in T}         # outside the gates by the register, lost included
    a, slope = fit_cellar(rec, o)
    lr, li = rec["line_rate"], rec["line_iv"]                     # the trade's containers per container sold a week
    b, m = slope(1.0) / 2.0, 2.0 * sum(slope(x) * float(lr[li == x].sum()) for x in set(li.tolist())) / \
        slope(1.0) / float(lr.sum())
    b *= o["x_b"]
    predict, shape = fit_sales(flow, R["anom"], o["harmonics"], o["hinge"])
    if o["level"] == "fit":
        lev = {bk: predict(max(bk - 1, 0), normal_temp(max(bk - 1, 0)) + R["anom"][max(bk - 1, 0)]) for bk in T}
    else:
        lev = {bk: float(flow[max(bk - o["level"], 0):bk].mean()) if bk else float(flow[:o["level"]].mean())
               for bk in T}
    # the trade's loss: what the register still holds outside the gates beyond what the trade's cellars took on
    lo = 156 - 52 * o["loss_years"]
    gone = X[156] - X[lo] - (b * m * (lev[156] - lev[lo]) if o["trade_change"] else 0.0)
    lam_acc = gone / float(flow[lo:156].sum())
    tag = R["pool"]["K20"]
    lam_tag = tag["tag_loss"] / tag["tag_trips"]
    if o["loss"] == "none":
        lam = 0.0
    elif o["loss"] == "tag" or (tagged and not o.get("account_tagged")):
        lam = lam_tag
    else:
        lam = lam_acc
    lam *= o["x_lam"]
    year_loss = lam * float(flow[104:156].sum())
    alive_out = X[156] - lam * float(flow[:156].sum())           # the trade's containers at the stocktake, alive
    resp = tracked_response(R) if o["swing"] == "tracked" else 1.0
    # the store: its cover in weeks of deliveries, beside the half run each beer on sale holds on average
    half26 = sum(run for c, sh, run in rec["beers26"]) / 2.0
    reg = np.polyfit(flow[52:], rec["store"][52:], 1)
    cov = (float(rec["store"][52:].mean()) - half26) / float(flow[52:].mean()) if o["cover"] == "mean" else \
        float(np.median((rec["store"][52:] - half26) / flow[52:]))
    cov *= o["x_cov"]
    ne, re_ = rec["estate"]
    c2 = float(np.mean([T[bk]["other"] / T[bk]["flow"] for bk in T])) if o["other"] == "mean" else \
        T[156]["other"] / T[156]["flow"]
    path, cum = [], 0.0
    for i in range(WH, WH + WF):
        j = i - 52
        temp = normal_temp(i) + (0.0 if anom27 is None else anom27[i - WH])
        F = predict(i, temp) * o["x_del"]
        live = 0.0 if i < ESTATE_WEEK else min(1.0, (i - ESTATE_WEEK + 1) / 3.0)
        es = ne * re_ * live * shape(i, temp)
        est = a * ne * live + b * 2.0 * es
        D = F + es
        if o["swing"] == "lines" or (tagged and o["swing"] == "tracked"):
            if tagged and o["census"]:
                swing = rec["census"][j] - rec["census"][155] + b * m * (F - flow[j]) + est
            else:
                swing = b * m * (F - lev[156]) + est
        elif tagged:                                              # last season's census, moved with the deliveries
            swing = rec["census"][j] * D / flow[j] - rec["census"][155]
        else:                                                     # the trade's stock moved with the deliveries
            swing = alive_out * resp * (D / lev[156] - 1.0)
        if o["store"] == "runs":
            store = sum(cov * sh * D + run / 2.0 for c, sh, run in beers_at(p, i))
        elif o["store"] == "cover":
            store = float(rec["store"][j - 2:j + 3].mean() / flow[j - 2:j + 3].mean()) * D
        else:
            store = float(reg[1] + reg[0] * D)
        cum += lam * D
        need = swing + store + c2 * D + FLOAT * D                 # beside the trade's containers at the stocktake
        path.append(dict(i=i, need=need, short=need - T[156]["onsite"] + cum, swing=swing, store=store))
    season = [x for x in path if x["i"] in SEASON]
    pick = max(season, key=lambda x: x["short"])
    return dict(short=pick["short"], week=pick["i"], swing=pick["swing"], store=pick["store"], year_loss=year_loss,
                lam=lam, lam_acc=lam_acc, a=a, b=b, m=m)


def direct(R, p, anom27=None):
    """the register as the fleet and its turns: the fleet moved with the busiest week's deliveries over the year's"""
    rec = R["pool"][p]
    predict, shape = fit_sales(rec["flow"], R["anom"], 2)
    ne, re_ = rec["estate"]
    peak = max(predict(i, normal_temp(i) + (0.0 if anom27 is None else anom27[i - WH])) +
               ne * re_ * shape(i, normal_temp(i) + (0.0 if anom27 is None else anom27[i - WH])) for i in SEASON)
    return rec["takes"][156]["register"] * (peak / float(rec["flow"][104:156].mean()) - 1.0)


def hot(fn):
    """a figure at the upper end of the 80 per cent range over the ten summers on record (the second highest)"""
    return float(sorted(fn(y) for y in range(10))[HOT_RANK])


FAMILY = [
    ("the golden's conventions", {}),
    ("the loss rate over the last two years", {"loss_years": 2}),
    ("the loss rate over the three years since the reconciliation", {"loss_years": 3}),
    ("the trade's own change between the stocktakes left out of the loss", {"trade_change": False}),
    ("the cellar counts fitted one line for each delivery interval", {"fit": "byclass"}),
    ("the bend in the weather response a degree lower", {"hinge": -1.0}),
    ("the bend in the weather response a degree higher", {"hinge": 1.0}),
    ("the summer's cellar counts only", {"count_months": "summer"}),
    ("one seasonal harmonic in the deliveries fit", {"harmonics": 1}),
    ("three seasonal harmonics in the deliveries fit", {"harmonics": 3}),
    ("the store's cover as the median week's, not the mean's", {"cover": "median"}),
    ("depots, wash and repair at the last stocktake's weeks of deliveries", {"other": "last"}),
    ("the three-year loss and the fitted level together", {"loss_years": 3, "level": "fit"}),
    ("deliveries at each stocktake over eight weeks, not four", {"level": 8}),
    ("deliveries at each stocktake from the fit", {"level": "fit"}),
    ("the tracked pool's trade stock from its own census", {"census": True}),
    ("the tracked pool's loss from the stock account", {"account_tagged": True}),
    ("the two-year loss and the lines by interval together", {"loss_years": 2, "fit": "byclass"}),
    ("the summer counts and the eight-week level together", {"count_months": "summer", "level": 8}),
]


# each fitted input moved by its spread, one at a time and to the same side together: the call has to hold
FORCING = [
    ("what a line holds per container sold, 20 per cent down", {"x_b": 0.8}),
    ("what a line holds per container sold, 20 per cent up", {"x_b": 1.2}),
    ("the store's cover, 20 per cent down", {"x_cov": 0.8}),
    ("the store's cover, 20 per cent up", {"x_cov": 1.2}),
    ("the loss per container delivered, 20 per cent down", {"x_lam": 0.8}),
    ("the loss per container delivered, 20 per cent up", {"x_lam": 1.2}),
    ("the season's deliveries, 5 per cent down", {"x_del": 0.95}),
    ("the season's deliveries, 5 per cent up", {"x_del": 1.05}),
]


def spreads(R, p, reps=120, seed=11):
    """each fitted input's own measured spread for one pool, as a share of its value: what a line holds per
    container sold (the counts resampled), the store's cover (the weeks resampled in blocks of four), the loss per
    container delivered (its range over one, two and three years of the stock account) and the worst week's
    deliveries (the fit's residuals resampled)"""
    rng = np.random.default_rng(seed)
    rec = R["pool"][p]
    lr, li = rec["line_rate"], rec["line_iv"]
    n = len(rec["count_held"])
    bm = []
    for _ in range(reps):
        idx = rng.integers(0, n, n)
        r2 = dict(rec)
        for k in ("count_rate", "count_iv", "count_held", "count_week"):
            r2[k] = rec[k][idx]
        sl = fit_cellar(r2, GOLDEN)[1]
        bm.append(sum(sl(x) * float(lr[li == x].sum()) for x in set(li.tolist())) / float(lr.sum()))
    half = sum(run for c, sh, run in rec["beers26"]) / 2.0
    st, fl = rec["store"][52:], rec["flow"][52:]
    cv = []
    for _ in range(reps):
        idx = np.concatenate([np.arange(k * 4, k * 4 + 4) for k in rng.integers(0, len(st) // 4, len(st) // 4)])
        cv.append((st[idx].mean() - half) / fl[idx].mean())
    lams = [chain(R, p, {"loss_years": y, "account_tagged": True})["lam_acc"] for y in (1, 2, 3)]
    g = chain(R, p)
    predict = fit_sales(rec["flow"], R["anom"], 2)[0]
    fit = np.array([predict(i, normal_temp(i) + R["anom"][i]) for i in range(WH)])
    res = np.log(rec["flow"]) - np.log(fit)
    pk = [fit_sales(fit * np.exp(rng.choice(res, len(res))), R["anom"], 2)[0](g["week"], normal_temp(g["week"]))
          for _ in range(reps // 3)]
    return dict(x_b=float(np.std(bm) / np.mean(bm)), x_cov=float(np.std(cv) / abs(np.mean(cv))),
                x_lam=float((max(lams) - min(lams)) / lams[0]) / 2.0,
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
    members = {}
    for p in POOLS:
        members[p] = dict(lines=[0.0, float(W[p]["moq"])], truth=truth[p], golden=G[p]["short"],
                          family=[chain(R, p, o)["short"] for _, o in FAMILY],
                          routes={"direct": direct(R, p), "rigorous": chain(R, p, RIGOROUS)["short"]})
    lat = {k: {p: chain(R, p, o)["short"] for p in POOLS} for k, o in lat_o.items()}
    untagged = tuple(p for p in POOLS if not W[p]["tagged"])
    comps = [("C1", "swing", POOLS), ("C2", "store", POOLS), ("C3", "year_loss", untagged)]
    figures = []
    for cid, field, pools in comps:
        figures.append(dict(id=cid, block="component", golden=fig(field, None, pools),
                            family=[fig(field, o, pools) for _, o in FAMILY],
                            lattice={k: fig(field, o, pools) for k, o in lat_o.items()},
                            routes={"rigorous": fig(field, RIGOROUS, pools)}))
    for p in POOLS:
        figures.append(dict(id="A-%s" % p, block="ask", member=p))
    for p in POOLS:
        figures.append(dict(id="H-%s" % p, block="ask", golden=fig("short", None, (p,), True),
                            family=[fig("short", o, (p,), True) for _, o in FAMILY],
                            lattice={k: fig("short", o, (p,), True) for k, o in lat_o.items()},
                            routes={"rigorous": fig("short", RIGOROUS, (p,), True)}))
    # the referee: the tracked pool's containers in the trade, 30 November 2025 to its busiest week of summer 2026
    t = R["pool"]["K20"]
    pk = 104 + int(np.argmax(t["census"][104:156]))
    gk = G["K20"]
    lev25 = float(t["flow"][100:104].mean())
    referee = dict(slice="the tracked pool's containers in the trade, from the 30 November 2025 stocktake to its "
                         "busiest week of summer 2026, which its tags count and no 2027 week or other pool shares",
                   covers_target=False, truth=float(t["census"][pk] - t["census"][103]),
                   golden=gk["b"] * gk["m"] * (float(t["flow"][pk]) - lev25),
                   rivals={"the trade's stock moved in step with deliveries":
                           float(t["census"][103] * (t["flow"][pk] / lev25 - 1.0))})
    spec = dict(task="task4 architecture 14", call="lines", members=members, lattice=lat, referee=referee,
                figures=figures, stumps={
                    "S1": dict(axis="unit", opens="K50",
                               said_out_loud="A cellar holds a number of containers for each line whatever it sells, "
                                             "plus cover for its delivery interval, so the trade's stock does not "
                                             "move in step with its sales.",
                               steps_left=4, precedents=["N01", "L15", "L40"]),
                    "S2": dict(axis="when", opens="K20",
                               said_out_loud="The store receives each beer a whole racking run at a time, so its "
                                             "stock follows the runs and the number of beers on sale, and both "
                                             "change in 2027.",
                               steps_left=3, precedents=["N17", "N02", "L37"]),
                    "S3": dict(axis="who", opens="FIR",
                               said_out_loud="The register never loses a container, and the only pool whose losses "
                                             "are seen is the tracked one, which loses far fewer.",
                               steps_left=4, precedents=["N08", "N12", "L53"]),
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
        print("variant deviations from the golden")
        for name, o in FAMILY[1:]:
            print("  %-68s" % name[:68], " ".join("%6.0f" % (chain(R, p, o)["short"] - G[p]["short"]) for p in POOLS))
        print("hot summer: truth, golden")
        for f in figures[-5:]:
            p = f["id"][2:]
            print("  %-4s %7.0f %7.0f | %7.0f %7.0f %7.0f | %7.0f" % (
                p, truth_hot[p], f["golden"], f["lattice"]["S1"], f["lattice"]["S2"], f["lattice"]["S3"],
                f["lattice"][reflex]))
        print("the world")
        for p in POOLS:
            q = world["pool"][p]
            print("  %-4s fleet at the reconciliation %6.0f, register now %6.0f, alive now %6.0f, on site %6.0f; "
                  "idle least in history %6.0f, at the 2026 peak %6.0f, least before the estate %6.0f; a %.2f b %.2f "
                  "(%.2f, %.2f); loss rate %.4f account, %.4f world; year loss %5.0f (%5.0f)" % (
                      p, q["alive0"], q["register"][156], q["alive"][156], R["pool"][p]["takes"][156]["onsite"],
                      q["idle"].min(), q["idle"][104:156].min(), q["idle27"][:ESTATE_WEEK - WH].min(), G[p]["a"],
                      G[p]["b"], W[p]["a"], W[p]["b"], G[p]["lam_acc"], q["lost"][104:156].sum() / q["S"][104:156].sum(),
                      G[p]["lam_acc"] * q["S"][104:156].sum(), q["lost"][104:156].sum()))
        print("  the tracked pool's response %.3f; referee truth %.0f golden %.0f rival %.0f" % (
            tracked_response(R), referee["truth"], referee["golden"], list(referee["rivals"].values())[0]))
        print()
    return corelib.run(spec)


if __name__ == "__main__":
    sys.exit(main())
