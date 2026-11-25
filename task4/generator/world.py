"""The simulated brewery behind the pack: Wrenfold's accounts and their dispense lines, each line drawing steadily
by the season and the week's temperature, what each cellar holds and is delivered, the drivers' visits (the empties
wait in the cellar for the dray's next call), the containers the trade loses, the cold store racked a run at a time,
the depots, the wash line, the fleet by purchase lot since 2011 and a register that strikes off only what the wash
line condemns, the one count of every site on 30 November 2026, and the reps' cellar counts of the full containers
of a line on the account's order day. The dials are the core's (`core.W`); this module lays the process out line by
line and day by day, and carries the same process through the 2027 season at expected sales, which is the truth the
checks hold the golden to.

Nothing here is read by the analysis: `analysis.py` reads the shipped files only."""
import datetime as dt
import math
from collections import deque

import numpy as np

import core as C

SEED = 72417
ORG = "Wrenfold Brewery Ltd"
ESTATE = "Maplestead Inns"
MAKER = "Lindqvist Fass GmbH"
HIRER = "Pennine Container Pool Ltd"
OLD_MAKER = "Calder Coopers Ltd"
PEOPLE = {"head": "Kim Taylor", "analyst": "Justin Francis", "fleet": "Edward Moss", "sales": "Louise White",
          "brewer": "Amelia Hodgson", "depot": "Toby Morley"}
POOLS = C.POOLS
WH, WF = C.WH, C.WF
D0 = C.D0
ASOF = D0 + dt.timedelta(days=7 * WH)                 # Monday 30 November 2026, the count of every site
WX0 = -361                                            # the weather record starts on Monday 2 January 2017
N_ACCOUNTS = 2300
COUNT_FROM = 60                                       # the reps' cellar counts start in late January 2025
DRAW_SD = 0.12                                        # a line's week-to-week wobble about its steady draw
CALL_DAYS = {1.0: ([3, 4, 5, 6], [0.15, 0.27, 0.33, 0.25]), 0.5: ([2, 3], [0.40, 0.60])}   # dray to the order day
RUN_SHORT = 0.008                                     # containers a racking fails to fill, as a share of the run
SPLIT = dict(depot_full=0.45, depot_empty=0.15, awaiting=0.22, wash=0.05, repair=0.13)   # of depots, wash and repair
DEPOTS = {"LDS": ("Leeds", 0.40), "YRK": ("York", 0.28), "SHF": ("Sheffield", 0.32)}
CHANNELS = ("FREE", "GROUP", "CLUB", "REST")
CH_SHARE = (0.50, 0.24, 0.14, 0.12)
AFFINITY = {"K50": (1.0, 1.25, 1.2, 0.5), "K30": (1.0, 1.1, 0.7, 1.1), "K20": (1.0, 0.8, 0.6, 1.3),
            "FIR": (1.5, 0.8, 0.9, 0.12), "KIL": (1.0, 0.3, 1.5, 0.02)}
FIXED = {"K50": {2: 0.80, 3: 0.20}, "K30": {2: 0.90, 3: 0.10}, "K20": {1: 0.10, 2: 0.80, 3: 0.10},
         "FIR": {2: 0.15, 3: 0.70, 4: 0.15}, "KIL": {2: 0.15, 3: 0.70, 4: 0.15}}
BEER_NAMES = {
    "PIL": "Wrenfold Pils", "GLD": "Wrenfold Gold", "PAL": "Calder Pale", "IPA": "Wrenfold IPA", "HER": "Heron Lager",
    "BLK": "Wrenfold Black", "BIT": "Wrenfold Best Bitter", "MLD": "Dark Mild", "SEA": "Shepley Amber",
    "SUM": "Summer Lightning Gold", "HAR": "Harvest Ale", "BIK": "Wrenfold Best Bitter",
    "F01": "Foundry Saison", "F02": "Foundry Hazy", "F03": "Foundry Red Rye", "F04": "Foundry West Coast",
    "F05": "Foundry Session Sour", "F06": "Foundry Oat Pale", "F07": "Foundry Porter", "F08": "Foundry Kolsch",
    "F09": "Foundry DDH Pale", "F10": "Foundry Gose", "F11": "Foundry Pilsner", "F12": "Foundry Brown",
    "F13": "Foundry Amber", "F14": "Foundry Hefe", "F15": "Foundry Grisette", "F16": "Foundry Citra Single Hop",
    "F17": "Foundry Lime Lager", "F18": "Foundry Harvest Pale"}
LOT_CODE = {"K50": "50", "K30": "30", "K20": "20", "FIR": "F9", "KIL": "K18"}
MAKER_FROM = 2014                                     # Lindqvist has made every lot since 2014
RINGS = ["red", "yellow", "green", "blue", "white", "orange", "black", "grey", "brown", "purple"]
HOLIDAYS = set(dt.date(*d) for d in [
    (2023, 12, 25), (2023, 12, 26), (2024, 1, 1), (2024, 3, 29), (2024, 4, 1), (2024, 5, 6), (2024, 5, 27),
    (2024, 8, 26), (2024, 12, 25), (2024, 12, 26), (2025, 1, 1), (2025, 4, 18), (2025, 4, 21), (2025, 5, 5),
    (2025, 5, 26), (2025, 8, 25), (2025, 12, 25), (2025, 12, 26), (2026, 1, 1), (2026, 4, 3), (2026, 4, 6),
    (2026, 5, 4), (2026, 5, 25), (2026, 8, 31)])


def week_start(i):
    return D0 + dt.timedelta(days=7 * i)


def workday(i, day, back=False):
    """the calendar date of a weekday of week i, moved off a bank holiday (deliveries later, rackings earlier)"""
    d = week_start(i) + dt.timedelta(days=int(day))
    while d in HOLIDAYS or (back and d.weekday() > 4):
        d += dt.timedelta(days=-1 if back else 1)
    return d


def normal(i):
    """the station's normal for the week, as the weather record files it"""
    return round(C.normal_temp(i), 1)


def first_monday_of_may(year):
    d = dt.date(year, 5, 1)
    return d + dt.timedelta(days=(7 - d.weekday()) % 7)


def fwd_factor(p, i, temp):
    w = C.W[p]
    return (1 + w["g"]) ** (i / 52.0) * C.seas(i, w["amp"]) * C.warm(temp, w["k"])


def year_shape(p):
    """the pool's season at normal weather over the 2027 contract year, mean one"""
    w = C.W[p]
    return float(np.mean([C.seas(i, w["amp"]) * C.warm(normal(i), w["k"]) for i in range(WH + 5, WH + 57)]))


def mean_run(run):
    return run * (1.0 - RUN_SHORT)


class Pool(object):
    pass


def weather(rng):
    n = WH - WX0
    a = np.zeros(n)
    for k in range(1, n):
        a[k] = 0.5 * a[k - 1] + rng.normal(0, 2.2)
    return {WX0 + k: round(normal(WX0 + k) + a[k], 1) for k in range(n)}


def accounts(rng):
    towns = ["Brighouse", "Halifax", "Huddersfield", "Leeds", "Bradford", "Wakefield", "York", "Harrogate", "Selby",
             "Sheffield", "Rotherham", "Barnsley", "Doncaster", "Skipton", "Otley", "Ilkley", "Pudsey", "Morley",
             "Dewsbury", "Batley", "Pontefract", "Castleford", "Wetherby", "Tadcaster", "Malton", "Ripon", "Thirsk",
             "Chesterfield", "Hebden Bridge", "Todmorden", "Elland", "Holmfirth", "Penistone", "Knaresborough"]
    first = ["Red", "White", "Black", "Golden", "Old", "Royal", "Three", "Crown and", "Rose and", "Fox and", "Bay",
             "Station", "Railway", "Kings", "Queens", "Cross", "Woolpack", "Shepherds", "Miners", "Weavers", "Navigation",
             "Travellers", "Masons", "Cricketers", "Spotted", "Blue", "Green", "New", "Junction", "Commercial"]
    second = ["Lion", "Hart", "Horse", "Bull", "Fleece", "Swan", "Oak", "Arms", "Anchor", "Crown", "Hounds", "Tuns",
              "Bell", "Plough", "Feathers", "Rest", "Inn", "Tavern", "Vaults", "Tap", "Hotel", "Cock", "Dragon", "Lamb",
              "Greyhound", "Star", "Sun", "Wheatsheaf", "George", "Volunteer"]
    clubs = ["Cricket Club", "Working Men's Club", "Golf Club", "Rugby Club", "Bowling Club", "Social Club",
             "Conservative Club", "Liberal Club", "Football Club"]
    part = ["", "", "", "East ", "West ", "North ", "South ", "Old ", "St John's ", "Victoria "]
    rests = ["Kitchen", "Bistro", "Grill", "Brasserie", "Bar and Kitchen", "Canteen", "Cafe Bar", "Taproom"]
    pick = lambda xs: xs[int(rng.integers(0, len(xs)))]
    out = []
    z = np.exp(rng.normal(0, 0.5, N_ACCOUNTS))
    ch = rng.choice(len(CHANNELS), N_ACCOUNTS, p=CH_SHARE)
    dkeys = ["BRG"] + list(DEPOTS)
    dp = rng.choice(len(dkeys), N_ACCOUNTS, p=[0.28, 0.29, 0.20, 0.23])
    seen = set()
    for k in range(N_ACCOUNTS):
        c = CHANNELS[ch[k]]
        while True:
            town = pick(towns)
            if c == "CLUB":
                name = "%s%s %s" % (pick(part), town, pick(clubs))
            elif c == "REST":
                name = "%s %s, %s" % (pick(first).replace(" and", ""), pick(rests), town)
            else:
                name = "The %s %s, %s" % (pick(first), pick(second), town)
            if name not in seen:
                seen.add(name)
                break
        out.append(dict(k=k, id="W%05d" % (10031 + k * 13), name=name, town=town, channel=c, depot=dkeys[dp[k]],
                        z=float(z[k]), former=None, swap_week=None,
                        opened=dt.date(int(rng.integers(1996, 2023)), int(rng.integers(1, 13)), int(rng.integers(1, 28)))))
    for k in rng.choice(N_ACCOUNTS, int(N_ACCOUNTS * 0.11), replace=False):   # a new owner, a new account number
        a = out[int(k)]
        a["former"] = "W%05d" % (60017 + int(k) * 7)
        a["swap_week"] = int(rng.integers(8, WH - 6))
    return out


def build(seed=SEED, light=False):
    """the whole world; light=True stops after the weekly arrays and the 2027 truth"""
    rs = lambda k: np.random.default_rng([seed, k])
    rng = rs(0)
    WD = type("World", (), {})()
    WD.T = weather(rs(1))
    WD.temp = np.array([WD.T[i] for i in range(WH)])
    WD.normal = {i: normal(i) for i in range(WX0, WH + WF + 2)}
    WD.years = list(range(2017, 2027))
    WD.hot = {}
    for y in WD.years:                                   # the 2027 season on the recorded weather of summer y
        i0 = (first_monday_of_may(y) - D0).days // 7
        WD.hot[y] = {i: WD.T[i0 + k] for k, i in enumerate(C.SEASON)}
    acc = accounts(rs(2))
    WD.accounts = acc
    z = np.array([a["z"] for a in acc])
    chn = np.array([CHANNELS.index(a["channel"]) for a in acc])
    vol = np.zeros(N_ACCOUNTS)
    pools = {}
    for p in POOLS:
        w = C.W[p]
        P = Pool()
        aff = z * np.array([AFFINITY[p][c] for c in chn])
        acct, prod = [], []
        if p == "K20":
            acct, prod = list(rng.choice(N_ACCOUNTS, w["L"], replace=False, p=aff / aff.sum())), ["GST"] * w["L"]
        else:
            left = w["L"]
            beers = [(c, sh) for c, sh, q26, q27 in w["beers"]]
            for bi, (code, sh) in enumerate(beers):
                n = left if bi == len(beers) - 1 else int(round(w["L"] * sh))
                left -= n
                acct += list(rng.choice(N_ACCOUNTS, n, replace=False, p=aff / aff.sum()))
                prod += [code] * n
        P.acct = np.array(acct)
        P.prod = np.array(prod)
        r = np.exp(rng.normal(0.0, 0.6, len(acct))) * z[P.acct] ** 0.5
        P.r = r * w["S0"] / r.sum()
        ks = sorted(FIXED[p])
        P.A = rng.choice(ks, len(acct), p=[FIXED[p][k] for k in ks]).astype(float)
        P.u = rng.random(len(acct))
        np.add.at(vol, P.acct, P.r)
        pools[p] = P
    twice = vol > np.quantile(vol[vol > 0], 0.86)        # the busiest cellars are delivered twice a week
    WD.twice = twice
    WD.day1 = np.where(twice, rng.integers(0, 2, N_ACCOUNTS), rng.integers(0, 5, N_ACCOUNTS))
    WD.pools = pools
    for k, p in enumerate(POOLS):
        simulate_pool(WD, p, rs(10 + k))
    if light:
        return WD
    visits(WD, rs(30))
    for k, p in enumerate(POOLS):
        racking_days(WD, p, rs(40 + k))
    for k, p in enumerate(POOLS):
        lots(WD, p, rs(70 + k))
    cellar_counts(WD, rs(60))
    return WD


def holding(P, w, mu):
    """what each line holds after a delivery when its week's trade is mu: its own fixed stock and its cover"""
    return P.A[:, None] + np.floor(w["b"] * (P.iv[:, None] + 1.0) * mu + P.u[:, None])


def split(total, shares):
    """whole numbers in the given shares that add to the total (largest remainders)"""
    x = np.asarray(shares, dtype=float) * total / float(np.sum(shares))
    f = np.floor(x).astype(int)
    for k in np.argsort(-(x - f), kind="stable")[:int(round(total - f.sum()))]:
        f[k] += 1
    return f


def simulate_pool(WD, p, rng):
    w, P = C.W[p], WD.pools[p]
    L = len(P.r)
    P.iv = np.where(WD.twice[P.acct], 0.5, 1.0)
    G = np.array([fwd_factor(p, i, WD.temp[i]) for i in range(WH)])
    mu = P.r[:, None] * G[None, :]
    # a line draws steadily: the beer it pours in a week is its expected trade with the week's common shock and its
    # own wobble, and the containers it empties are the whole containers that beer runs through
    inc = mu * np.exp(rng.normal(0, 0.03, WH))[None, :] * np.exp(rng.normal(0, DRAW_SD, (L, WH)))
    cum = rng.random(L)[:, None] + np.cumsum(np.column_stack([np.zeros(L), inc]), axis=1)   # by the start of week i
    s = np.diff(np.floor(cum), axis=1).astype(int)
    P.cum, P.inc = cum, inc
    H = holding(P, w, mu)
    Hprev = np.column_stack([H[:, 0], H[:, :-1]])
    lost = rng.binomial(s, w["loss"])
    dlv = np.maximum(0, s + H - Hprev).astype(int)       # the driver restores the cellar's stock
    col = (Hprev - lost + dlv - H).astype(int)           # and takes the empties that are there
    assert (col >= 0).all()
    P.G, P.mu, P.s, P.H, P.lost, P.dlv, P.col = G, mu, s, H.astype(int), lost, dlv, col
    D = dlv.sum(axis=0).astype(float)
    P.D = D
    P.trade = np.concatenate([[H[:, 0].sum()], H.sum(axis=0)])    # at each Monday 0..WH
    beers26 = [(c, sh, q26) for c, sh, q26, q27 in w["beers"]]
    P.beers26 = beers26
    codes = [c for c, sh, q in beers26]
    pbs = np.array([sh for c, sh, q in beers26])
    if p == "K20":                                       # a guest line takes the small-batch beer on rotation
        P.guest = rng.choice(len(codes), (L, WH), p=pbs / pbs.sum())
        dem = np.array([(dlv * (P.guest == b)).sum(axis=0) for b in range(len(codes))], dtype=float)
    else:
        P.guest = None
        dem = np.array([dlv[P.prod == c].sum(axis=0) for c in codes], dtype=float)
    P.dem = dem
    c2 = w["c2"]
    jit = lambda: np.exp(rng.normal(0, 0.04, WH + 1))
    Dx = np.concatenate([[D[0]], D])
    P.depot_full = np.rint(SPLIT["depot_full"] * c2 * Dx * jit())
    P.parts = {k: np.rint(SPLIT[k] * c2 * Dx * jit()) for k in ("depot_empty", "awaiting", "wash", "repair")}
    P.ret = sum(P.parts.values())
    P.other = P.depot_full + P.ret
    depot_b = np.array([split(int(P.depot_full[i]), pbs) for i in range(WH + 1)]).T     # by beer
    # the cold store: each beer racked a whole run at a time when its stock falls to its cover
    stock = np.zeros((len(codes), WH + 1))
    events = []
    for bi, (code, sh, run) in enumerate(beers26):
        sb = math.floor(w["cover"] * dem[bi, 0] + run * rng.random())
        stock[bi, 0] = sb
        for i in range(WH):
            sb = sb - dem[bi, i] - (depot_b[bi, i + 1] - depot_b[bi, i])
            while sb < w["cover"] * dem[bi, i]:
                filled = int(run - rng.binomial(run, RUN_SHORT))
                sb += filled
                events.append([i, bi, filled])
            stock[bi, i + 1] = sb
    P.stock_b, P.depot_b, P.rack = stock, depot_b, events
    P.store = stock.sum(axis=0)
    washed = P.ret[:-1] + col.sum(axis=0) - P.ret[1:]
    assert (washed >= 0).all()
    P.washed = washed.astype(int)
    P.scrap = rng.binomial(P.washed, C.SCRAP)
    P.lost_w = lost.sum(axis=0)
    bought = np.zeros(WH + WF)
    for wk, n in w["lots"]:
        bought[wk] += n
    P.bought = bought
    forward(WD, p, rng)


def path(WD, p, temps=None):
    """the pool's 2027 weeks at expected sales: the trade's cellars, the store, the depots and wash, the float"""
    w, P = C.W[p], WD.pools[p]
    ne, re_ = w["estate"]
    ys = year_shape(p)
    out = []
    cprev = float(P.trade[WH])
    for i in range(WH, WH + WF):
        t = WD.normal[i] if temps is None or i not in temps else temps[i]
        mu = P.r * fwd_factor(p, i, t)
        live = 0.0 if i < C.ESTATE_WEEK else min(1.0, (i - C.ESTATE_WEEK + 1) / 3.0)
        n_live = int(round(ne * live))
        es_rate = re_ * C.seas(i, w["amp"]) * C.warm(t, w["k"]) / ys
        est = float((P.eA[:n_live] + np.floor(w["b"] * 2.0 * es_rate + P.eu[:n_live])).sum()) if n_live else 0.0
        cellar = float((P.A + np.floor(w["b"] * (P.iv + 1.0) * mu + P.u)).sum()) + est
        S = float(mu.sum()) + n_live * es_rate
        D = max(S + cellar - cprev, 0.0)
        cprev = cellar
        beers = C.beers_at(p, i)
        store = w["cover"] * D + sum(mean_run(run) / 2.0 for c, sh, run in beers)
        out.append(dict(i=i, S=S, D=D, cellar=cellar, est=est, store=store, other=w["c2"] * D, fl=C.FLOAT * D,
                        lost=w["loss"] * S, scrap=C.SCRAP * S, n_beers=len(beers)))
    return out


def forward(WD, p, rng):
    w, P = C.W[p], WD.pools[p]
    ne = max(w["estate"][0], 1)
    ks = sorted(FIXED[p])
    P.eA = rng.choice(ks, ne, p=[FIXED[p][k] for k in ks]).astype(float)
    P.eu = rng.random(ne)
    fut = path(WD, p)
    need = np.array([f["cellar"] + f["store"] + f["other"] + f["fl"] for f in fut])
    drain = np.cumsum([f["lost"] + f["scrap"] for f in fut])
    sidx = [f["i"] - WH for f in fut if f["i"] in C.SEASON]
    pk = max(sidx, key=lambda j: need[j] + drain[j])
    hist = float(P.lost_w.sum() + P.scrap.sum())
    alive0 = round((need[pk] - w["place"] + drain[pk] + hist - P.bought[:WH].sum()) / 10.0) * 10.0
    alive = np.zeros(WH + 1)
    alive[0] = alive0
    for i in range(WH):
        alive[i + 1] = alive[i] - P.lost_w[i] - P.scrap[i] + P.bought[i]
    P.alive, P.alive0 = alive, int(alive0)
    P.onsite = alive - P.trade
    P.idle = P.onsite - P.store - P.other
    assert P.idle.min() >= 0, (p, P.idle.min())
    P.fut = fut
    pre = [alive[WH] - drain[j] - need[j] for j in range(len(fut)) if fut[j]["i"] < C.ESTATE_WEEK]
    assert min(pre) >= 0, (p, min(pre))


def truth(WD, p, temps=None):
    """the world's own largest weekly shortfall in the 2027 season and the week it falls in"""
    P = WD.pools[p]
    fut = path(WD, p, temps)
    alive = float(P.alive[WH])
    best = None
    for f in fut:
        alive -= f["lost"] + f["scrap"]
        f["short"], f["alive"] = f["cellar"] + f["store"] + f["other"] + f["fl"] - alive, alive
        if f["i"] in C.SEASON and (best is None or f["short"] > best["short"]):
            best = f
    return best, fut


def truth_hot(WD, p):
    v = sorted(truth(WD, p, WD.hot[y])[0]["short"] for y in WD.years)
    return v[C.HOT_RANK], v


# ------------------------------------------------------------------------------------------- the drivers' visits
def visits(WD, rng):
    """each line's weekly delivery laid on its account's delivery day or days: on a twice-weekly round the second
    call of the week brings at least one of the line's containers whenever it has any"""
    for p in POOLS:
        P = WD.pools[p]
        tw = WD.twice[P.acct][:, None]
        first = np.where(P.dlv > 0, rng.binomial(np.maximum(P.dlv - 1, 0), 0.5), 0)
        P.d1 = np.where(tw, first, P.dlv)
        P.d2 = P.dlv - P.d1


def racking_days(WD, p, rng):
    """the day of each racking: early enough in its week that the beer never runs out on a loading morning"""
    P = WD.pools[p]
    nb = len(P.beers26)
    day_of = WD.day1[P.acct]
    dem = np.zeros((nb, WH, 5))
    for v, d in ((0, P.d1), (1, P.d2)):
        day = day_of + 3 * v
        for b in range(nb):
            x = d * ((P.guest == b) if P.guest is not None else (P.prod == P.beers26[b][0])[:, None])
            for dd in range(5):
                dem[b, :, dd] += x[day == dd].sum(axis=0)
    by = {}
    for i, bi, n in P.rack:
        by.setdefault((i, bi), []).append(n)
    out = []
    for (i, bi), runs in sorted(by.items()):
        have = P.stock_b[bi, i] + P.depot_b[bi, i]
        pend = sorted((int(rng.integers(0, 5)), n) for n in runs)
        for dd in range(5):
            while pend and (pend[0][0] <= dd or have < dem[bi, i, dd]):   # pulled forward when the beer runs short
                have += pend[0][1]
                out.append((i, dd, bi, pend.pop(0)[1]))
            have -= dem[bi, i, dd]
        assert not pend
    P.rackings = sorted(out)


# ------------------------------------------------------------------------------------------- the fleet by lot
def lots(WD, p, rng):
    """the fleet by purchase lot: a lot a year from 2011 to 2023 and the lots bought inside the docket record. Every
    lot loses the same share of what is alive each year (a lost container is any container; the share is the last
    year's loss over the fleet with a year-to-year spread), the wash line's condemnations alone are struck off the
    register, the losses and condemnations inside the record are drawn container by container, and the count of
    30 November 2026 finds on site a random draw of what is alive"""
    w, P = C.W[p], WD.pools[p]
    fleet = float(P.alive[WH - 52:WH + 1].mean())
    rl = float(P.lost_w[WH - 52:].sum()) / fleet
    rs = float(P.scrap[WH - 52:].sum()) / fleet
    years = list(C.LOT_YEARS)
    rho = {y: rl * math.exp(rng.normal(0, 0.05)) for y in years}
    size = rng.uniform(0.6, 1.4, len(years)) * np.linspace(1.25, 0.85, len(years))
    late = int(rng.integers(1, 9))                                # this lot's last part came in the January after
    info, surv0, cshare = [], [], []
    for k, y in enumerate(years):
        d = dt.date(y, int(rng.integers(2, 11)), int(rng.integers(1, 28)))
        parts = [d + dt.timedelta(days=int(x)) for x in sorted(rng.choice(np.arange(0, 70, 7), int(rng.integers(1, 4)),
                                                                          replace=False))]
        if k == late:
            parts[-1] = dt.date(y + 1, 1, int(rng.integers(8, 27)))
        s, c = 1.0, 0.0
        for z in range(y, 2024):                                   # from the first part to the record's opening
            lo, hi = max(parts[0], dt.date(z, 1, 1)), min(D0, dt.date(z + 1, 1, 1))
            f = (hi - lo).days / 365.25
            if f > 0:
                c += s * rs * f
                s *= (1.0 - rho[z] - rs) ** f
        surv0.append(s)
        cshare.append(c)
        info.append(dict(year=y, parts=parts, maker=OLD_MAKER if y < MAKER_FROM else MAKER))
    alive0 = split(P.alive0, size * np.array(surv0))
    serial_lot, serial_date, cond, lost = [], [], {}, set()
    for k, x in enumerate(info):
        n_alive = int(alive0[k])
        n = int(round(n_alive / surv0[k]))
        n_cond = int(round(n * cshare[k]))
        first = len(serial_lot)
        per = split(n, np.ones(len(x["parts"])))
        for d, m in zip(x["parts"], per):
            serial_lot += [k] * int(m)
            serial_date += [d] * int(m)
        ids = rng.permutation(np.arange(first, first + n))
        for j in ids[:n_cond]:                                    # condemned at the wash before the record opens
            d0 = serial_date[j] + dt.timedelta(days=120)
            span = max((D0 - d0).days, 1)
            cond[int(j)] = d0 + dt.timedelta(days=int(rng.integers(0, span)))
        lost |= set(int(j) for j in ids[n_cond:n - n_alive])       # lost in the trade before the record opens
        x["bought"], x["alive0"] = n, n_alive
    for wk, n in w["lots"]:                                        # the lots bought inside the record
        d = week_start(wk) + dt.timedelta(days=2)
        info.append(dict(year=d.year, parts=[d], maker=MAKER, bought=int(n), alive0=0, week=wk))
        serial_lot += [len(info) - 1] * int(n)
        serial_date += [d] * int(n)
    serial_lot = np.array(serial_lot)
    alive = np.ones(len(serial_lot), dtype=bool)
    for j in list(cond) + list(lost):
        alive[j] = False
    for k, x in enumerate(info):
        if "week" in x:
            alive[serial_lot == k] = False                         # not yet bought at the record's opening
    assert int(alive.sum()) == P.alive0, (p, int(alive.sum()), P.alive0)
    for i in range(WH):                                            # the record, week by week
        live = np.nonzero(alive)[0]
        pick = rng.choice(len(live), int(P.lost_w[i] + P.scrap[i]), replace=False)
        gone = live[pick]
        for j in gone[:int(P.lost_w[i])]:
            lost.add(int(j))
        worked = [week_start(i) + dt.timedelta(days=d) for d in range(5)]
        worked = [d for d in worked if d not in HOLIDAYS]
        for j in gone[int(P.lost_w[i]):]:
            cond[int(j)] = worked[int(rng.integers(0, len(worked)))]
        alive[gone] = False
        for k, x in enumerate(info):
            if x.get("week") == i:
                alive[serial_lot == k] = True
    assert int(alive.sum()) == int(P.alive[WH]), (p, int(alive.sum()), P.alive[WH])
    live = np.nonzero(alive)[0]
    onsite = np.zeros(len(serial_lot), dtype=bool)
    onsite[live[rng.choice(len(live), int(P.onsite[WH]), replace=False)]] = True
    P.lots = info
    P.reg = dict(lot=serial_lot, bought=serial_date, condemned=cond, lost=lost, alive=alive, onsite=onsite,
                 total=len(serial_lot), rho=rl, rs=rs)
    before = lambda d: sum(1 for x in serial_date if x < d) - sum(1 for x in cond.values() if x < d)
    P.register_at_count = before(ASOF)
    P.lot_tally = np.bincount(serial_lot[onsite], minlength=len(info))


# ------------------------------------------------------------------------------------------- the reps' counts
def cellar_counts(WD, rng):
    """trade quality reps call on an account on its order day, a few days after the dray, and count the full
    containers of each line they check and the one on dispense; the containers the line has emptied since the dray
    called wait in the cellar for its next delivery and are not on the form"""
    lines_of = {}
    for p in POOLS:
        for l, a in enumerate(WD.pools[p].acct.tolist()):
            lines_of.setdefault(a, []).append((p, l))
    accts = sorted(lines_of)
    visited = np.zeros((N_ACCOUNTS, WH), dtype=bool)
    for p in POOLS:
        P = WD.pools[p]
        np.logical_or.at(visited, (np.repeat(P.acct, WH), np.tile(np.arange(WH), len(P.acct))), (P.dlv > 0).ravel())
    off = {}
    for a in accts:                                               # the account's order day, so many days after the dray
        days, wts = CALL_DAYS[0.5 if WD.twice[a] else 1.0]
        off[a] = int(rng.choice(days, p=wts))
    has = lambda a, q: any(p == q for p, l in lines_of[a])
    wgt = np.array([1.0 + 9.0 * has(a, "KIL") + 0.6 * has(a, "FIR") + 0.4 * has(a, "K20") for a in accts])
    near_holiday = lambda i: any((week_start(i) + dt.timedelta(days=d)) in HOLIDAYS for d in range(-3, 8))
    weeks = [i for i in range(COUNT_FROM, WH - 1) if not near_holiday(i) and not (
        week_start(i).month == 12 and week_start(i).day >= 15)]
    quota = {p: C.W[p]["counts"] for p in POOLS}
    done = {p: 0 for p in POOLS}
    rep_of = {dk: k for k, dk in enumerate(["BRG", "LDS", "YRK", "SHF"])}
    rows, n = [], 0
    while any(done[p] < quota[p] for p in POOLS):
        a = accts[int(rng.choice(len(accts), p=wgt / wgt.sum()))]
        i = weeks[int(rng.integers(0, len(weeks)))]
        todo = [(p, l) for p, l in lines_of[a] if done[p] < quota[p]]
        if not visited[a, i] or not todo:
            continue
        dray = workday(i, int(WD.day1[a]) + (3 if WD.twice[a] else 0))
        day = dray + dt.timedelta(days=off[a])
        if day >= ASOF:
            continue
        rep = (rep_of[WD.accounts[a]["depot"]] + (2 if rng.random() < 0.15 else 0)) % 6
        keyed = int(rng.integers(0, 4)) if rng.random() > 0.12 else int(rng.integers(9, 45))
        for p, l in todo:
            P = WD.pools[p]
            tot = int(P.H[l, i])
            c0 = P.cum[l, i + 1]
            emp = int(min(max(tot - 1, 0), math.floor(c0 + off[a] / 7.0 * P.inc[l, i + 1]) - math.floor(c0)))
            full = tot - emp
            if rng.random() < 0.02:
                full = max(1, full + (1 if rng.random() < 0.5 else -1))
            rows.append(dict(visit=n, week=i, date=day, dray=dray, acct=a, pool=p, line=l, held=tot, empties=emp,
                             full=full - 1, on=1, rep=rep, keyed=keyed, temp=round(float(rng.normal(11.8, 0.9)), 1)))
            done[p] += 1
        n += 1
    for r in [r for r in rows if rng.random() < 0.004]:            # a line counted twice on one call
        rows.append(dict(r, full=max(0, r["full"] + int(rng.choice([-1, 0, 0, 1])))))
    WD.counts = rows


if __name__ == "__main__":
    import sys
    WD = build(light="--light" in sys.argv)
    for p in POOLS:
        P = WD.pools[p]
        b, fut = truth(WD, p)
        print("%s lines %5d  D mean %6.0f  trade %6.0f..%6.0f  store mean %5.0f  other %5.0f  alive0 %6.0f now %6.0f "
              "idle min %5.0f  truth %6.0f wk %s  hot %6.0f  lost/yr %5.0f  twice %.2f" % (
                  p, len(P.r), P.D.mean(), P.trade.min(), P.trade.max(), P.store.mean(), P.other.mean(), P.alive0,
                  P.alive[WH], P.idle.min(), b["short"], week_start(b["i"]), truth_hot(WD, p)[0],
                  P.lost_w[104:].sum(), (P.iv == 0.5).mean()))
        if "--light" not in sys.argv:
            print("     register at the count %6d, serials %6d, on site %6d, lots %d, rate of leaving %.3f, condemned %.4f, "
                  "counts %d" % (P.register_at_count, P.reg["total"], int(P.reg["onsite"].sum()), len(P.lots),
                                 P.reg["rho"], P.reg["rs"], sum(1 for r in WD.counts if r["pool"] == p)))
