"""The simulated brewery behind the pack: Wrenfold's accounts and their dispense lines, each line's sales by the
season and the week's temperature, what each cellar holds and is delivered, the drivers' visits, the containers the
trade loses, the cold store racked a run at a time, the depots, the wash line, the fleet and its register, the
stocktakes, the reps' cellar audits and the tags of the 20 litre kegs. The dials are the core's (`core.W`); this
module lays the process out line by line and day by day, and carries the same process through the 2027 season at
expected sales, which is the truth the checks hold the golden to.

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
RECOVERY = "KegTrace Recovery Services"
PEOPLE = {"head": "Kim Taylor", "analyst": "Justin Francis", "fleet": "Edward Moss", "sales": "Louise White",
          "brewer": "Amelia Hodgson", "depot": "Toby Morley"}
POOLS = C.POOLS
WH, WF = C.WH, C.WF
D0 = C.D0
ASOF = D0 + dt.timedelta(days=7 * WH)                 # Monday 30 November 2026, the stocktake
STOCKTAKES = (0, 52, 104, 156)
WX0 = -361                                            # the weather record starts on Monday 2 January 2017
N_ACCOUNTS = 2300
AUDIT_FROM = 60                                       # the reps' cellar audits start in late January 2025
N_AUDITS = 860
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
OLD_LOTS = {"K50": [("50-2009", 2009, 0.30), ("50-2013", 2013, 0.33), ("50-2018", 2018, 0.37)],
            "K30": [("30-2011", 2011, 0.34), ("30-2016", 2016, 0.36), ("30-2021", 2021, 0.30)],
            "K20": [("20-2019", 2019, 0.45), ("20-2022", 2022, 0.55)],
            "FIR": [("F9-2008", 2008, 0.38), ("F9-2014", 2014, 0.36), ("F9-2019", 2019, 0.26)],
            "KIL": [("K18-2010", 2010, 0.55), ("K18-2017", 2017, 0.45)]}
READ_MISS = {"FILL": 0.005, "DELIVER": 0.03, "WASH": 0.01}
READ_DOUBLE = 0.01
TAG_SWAP = 0.004                                      # share of washes at which a damaged tag is replaced
OVERDUE_DAYS = 182
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
    kegs(WD, rs(50))
    audits(WD, rs(60))
    register(WD, rs(70))
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
    s = rng.poisson(mu * np.exp(rng.normal(0, 0.03, WH))[None, :])
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
    reg = np.zeros(WH + 1)
    alive[0] = reg[0] = alive0
    for i in range(WH):
        alive[i + 1] = alive[i] - P.lost_w[i] - P.scrap[i] + P.bought[i]
        reg[i + 1] = reg[i] - P.scrap[i] + P.bought[i]
    P.alive, P.register, P.alive0 = alive, reg, int(alive0)
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
    """each line's weekly delivery and collection laid on its account's delivery day or days"""
    E = np.zeros((2, N_ACCOUNTS, WH), dtype=int)                 # empties collected at each visit, every type
    for p in POOLS:
        P = WD.pools[p]
        tw = WD.twice[P.acct][:, None]
        P.d1 = np.where(tw, rng.binomial(P.dlv, 0.5), P.dlv)
        P.d2 = P.dlv - P.d1
        P.c1 = np.where(tw, rng.binomial(P.col, 0.5), P.col)
        P.c2 = P.col - P.c1
        for v, c in ((0, P.c1), (1, P.c2)):
            np.add.at(E[v], P.acct, c)
    WD.empties = E


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


# ----------------------------------------------------------------------------------- the 20 litre kegs, one by one
def kegs(WD, rng):
    """every 20 litre keg through fill, delivery and wash: the reads its tag makes, the kegs the trade loses and the
    kegs the recovery agent is sent after"""
    p = "K20"
    w, P = C.W[p], WD.pools[p]
    L = len(P.r)
    n0 = P.alive0
    lots = [(wk, int(n)) for wk, n in w["lots"]]
    idle = deque(rng.permutation(n0).tolist())
    queue = [deque() for _ in range(L)]
    empt = [deque() for _ in range(L)]
    fifo = [deque() for _ in P.beers26]
    for l in range(L):
        for _ in range(int(P.H[l, 0])):
            queue[l].append((idle.popleft(), None))
    for b in range(len(fifo)):
        for _ in range(int(P.stock_b[b, 0] + P.depot_b[b, 0])):
            fifo[b].append(idle.popleft())
    trips = []                 # keg, beer, fill day, line, deliver day, wash day (day numbers from D0; None if not seen)
    open_trip = {}             # keg -> index in trips of its trip in progress
    lost_kegs = []             # keg, deliver day, week lost
    scrapped = []              # keg, day
    racks, deliv = {}, {}
    for i, dd, bi, n in P.rackings:
        racks.setdefault(i, []).append((dd, bi, n))
    acct = P.acct
    for v, d, c in ((0, P.d1, P.c1), (1, P.d2, P.c2)):
        ls, ws = np.nonzero((d > 0) | (c > 0))
        for l, i in zip(ls.tolist(), ws.tolist()):
            deliv.setdefault(i, []).append((int(WD.day1[acct[l]]) + 3 * v, l, int(d[l, i]), int(c[l, i])))
    owed = np.zeros(L, dtype=int)
    due = np.zeros(L, dtype=int)
    back = {}                  # day number -> kegs read at the wash that day
    next_lot = 0
    gone_for_good = set()
    for i in range(WH):
        while next_lot < len(lots) and lots[next_lot][0] == i:
            first = n0 + sum(n for wk, n in lots[:next_lot])
            idle.extend(range(first, first + lots[next_lot][1]))
            next_lot += 1
        wk_racks = sorted(racks.get(i, []))
        wk_del = sorted(deliv.get(i, []))
        sold = set()
        washed_now = []
        for dd in range(7):
            day = 7 * i + dd
            for k in back.pop(day, []):
                washed_now.append(k)
                idle.append(k)
            while wk_racks and wk_racks[0][0] == dd:
                _, bi, n = wk_racks.pop(0)
                for _ in range(n):
                    k = idle.popleft()
                    open_trip[k] = len(trips)
                    trips.append([k, bi, day, -1, None, None])
                    fifo[bi].append(k)
            while wk_del and wk_del[0][0] == dd:
                _, l, q, c = wk_del.pop(0)
                if l not in sold:                                # what the line sold since the last call
                    sold.add(l)
                    n_s, n_l = int(P.s[l, i]) + int(owed[l]), int(P.lost[l, i])
                    take = min(n_s, len(queue[l]))
                    owed[l] = n_s - take
                    gone = [queue[l].popleft() for _ in range(take)]
                    for k, dday in gone[:min(n_l, take)]:
                        lost_kegs.append((k, dday, i))
                        gone_for_good.add(k)
                        open_trip.pop(k, None)
                    empt[l].extend(gone[min(n_l, take):])
                want, due[l] = c + int(due[l]), 0
                for n_c in range(want):                          # the empties that are there
                    if empt[l]:
                        k, dday = empt[l].popleft()
                    elif len(queue[l]) > int(P.H[l, i]):
                        k, dday = queue[l].pop()
                    else:
                        due[l] = want - n_c
                        break
                    wd = day + (1 if WD.accounts[acct[l]]["depot"] != "BRG" else 0) + (1 if rng.random() < 0.12 else 0)
                    if k in open_trip:
                        trips[open_trip.pop(k)][5] = wd
                    else:                                        # delivered before the record opens
                        trips.append([k, -1, None, l, dday, wd])
                    back.setdefault(max(wd, day + 1), []).append(k)   # clean and ready for filling the day after
                bi = int(P.guest[l, i])
                for _ in range(q):
                    src = fifo[bi] if fifo[bi] else max(fifo, key=len)
                    k = src.popleft()
                    if k in open_trip:
                        trips[open_trip[k]][3] = l
                        trips[open_trip[k]][4] = day
                    else:                                        # filled before the record opens
                        open_trip[k] = len(trips)
                        trips.append([k, bi, None, l, day, None])
                    queue[l].append((k, day))
        for l in range(L):                                       # a line with no call this week
            if l not in sold and P.s[l, i]:
                owed[l] += int(P.s[l, i])
        for _ in range(int(P.scrap[i])):
            cand = [k for k in washed_now if k in idle]
            if cand:
                k = cand[int(rng.integers(0, len(cand)))]
                washed_now.remove(k)
                idle.remove(k)
                scrapped.append((k, 7 * i + int(rng.integers(0, 5))))
    P.keg_total = n0 + sum(n for wk, n in lots)
    P.trips, P.lost_kegs, P.scrapped = trips, lost_kegs, scrapped
    P.keg_trade = sum(len(q) for q in queue) + sum(len(e) for e in empt)
    # the kegs the recovery agent is sent after: unread 26 weeks after a delivery
    end = 7 * WH
    chase = []
    for k, dday, wk in lost_kegs:
        if dday is not None and dday + OVERDUE_DAYS < end:
            ref = dday + OVERDUE_DAYS + int(rng.integers(0, 6))
            closed = ref + int(rng.integers(12, 40))
            if ref < end:
                chase.append((k, dday, ref, closed if closed < end else None, "NOT TRACED" if closed < end else None))
    for k, bi, fday, l, dday, wday in trips:
        if dday is None or k in gone_for_good and wday is None:
            continue
        if (wday is None and dday + OVERDUE_DAYS < end) or (wday is not None and wday - dday > OVERDUE_DAYS + 5):
            ref = dday + OVERDUE_DAYS + int(rng.integers(0, 6))
            closed = ref + int(rng.integers(5, 25))
            if ref < end:
                chase.append((k, dday, ref, closed if closed < end else None, "AT ACCOUNT" if closed < end else None))
    P.chase = sorted(chase, key=lambda x: (x[2], x[0]))


# ------------------------------------------------------------------------------------------- the reps' audits
def audits(WD, rng):
    """trade quality reps count a cellar line by line on their rounds: full, on dispense and empty"""
    lines_of = {}
    for p in POOLS:
        for l, a in enumerate(WD.pools[p].acct.tolist()):
            lines_of.setdefault(a, []).append((p, l))
    accts = sorted(lines_of)
    wgt = np.array([1.0 + 1.6 * any(p == "KIL" for p, l in lines_of[a]) + 0.5 * any(p == "FIR" for p, l in lines_of[a])
                    for a in accts])
    near_holiday = lambda i: any((week_start(i) + dt.timedelta(days=d)) in HOLIDAYS for d in range(-3, 8))
    weeks = [i for i in range(AUDIT_FROM, WH) if not near_holiday(i) and not (
        week_start(i).month == 12 and week_start(i).day >= 15)]
    rows = []
    for n in range(N_AUDITS):
        a = accts[int(rng.choice(len(accts), p=wgt / wgt.sum()))]
        i = weeks[int(rng.integers(0, len(weeks)))]
        dd = int(rng.integers(0, 5))
        d1 = int(WD.day1[a])
        tw = bool(WD.twice[a])
        last = [x for x in ([d1, d1 + 3] if tw else [d1]) if x <= dd]
        i_eff = i if last else i - 1
        gap = (dd - last[-1]) if last else (dd + 7 - (d1 + 3 if tw else d1))
        frac = min(1.0, (gap + rng.random()) / (3.5 if tw else 7.0))
        rep = int(rng.integers(0, 6))
        keyed = int(rng.integers(0, 4)) if rng.random() > 0.12 else int(rng.integers(9, 45))
        for p, l in lines_of[a]:
            P = WD.pools[p]
            tot = int(P.H[l, i_eff])
            nxt = int(P.s[l, min(i_eff + 1, WH - 1)])
            emp = min(max(tot - 1, 0), int(rng.binomial(nxt, frac)) if nxt else 0)
            on = 1 if tot >= 1 else 0
            full = tot - on - emp
            if rng.random() < 0.02:
                full = max(0, full + (1 if rng.random() < 0.5 else -1))
            rows.append(dict(visit=n, week=i, day=dd, acct=a, pool=p, line=l, full=full, on=on, empty=emp,
                             foreign=int(rng.poisson(0.35)), rep=rep, keyed=keyed))
    WD.audits = rows


# ------------------------------------------------------------------------------------------- the register
def register(WD, rng):
    """every container by serial: its lot and purchase date, and the day it was condemned if it was"""
    for p in POOLS:
        w, P = C.W[p], WD.pools[p]
        n0 = P.alive0
        lot, bought = [], []
        for (name, year, sh), n in zip(OLD_LOTS[p], split(n0, [sh for _, _, sh in OLD_LOTS[p]])):
            base = dt.date(year, int(rng.integers(2, 11)), int(rng.integers(1, 28)))
            for part in range(3):
                m = int(n) // 3 + (1 if part < int(n) % 3 else 0)
                lot += [name] * m
                bought += [base + dt.timedelta(days=21 * part)] * m
        for wk, n in w["lots"]:
            d = week_start(wk) + dt.timedelta(days=2)
            lot += ["%s-%d" % (OLD_LOTS[p][0][0].rsplit("-", 1)[0], d.year)] * int(n)
            bought += [d] * int(n)
        total = len(lot)
        condemned = {}
        lost = set()
        done = np.zeros(WH, dtype=int)
        if p == "K20":
            for k, day in P.scrapped:
                condemned[int(k)] = D0 + dt.timedelta(days=int(day))
                done[min(int(day) // 7, WH - 1)] += 1
            lost = {int(k) for k, _, _ in P.lost_kegs}
        avail = n0 + np.cumsum(P.bought[:WH]) - P.bought[:WH]
        for i in range(WH):
            for _ in range(int(P.scrap[i] - done[i])):
                while True:
                    k = int(rng.integers(0, int(avail[i])))
                    if k not in condemned and k not in lost:
                        break
                condemned[k] = week_start(i) + dt.timedelta(days=int(rng.integers(0, 5)))
        P.reg = dict(lot=lot, bought=bought, condemned=condemned, total=total)
        for b in STOCKTAKES:                                     # the register holds what the fleet account says
            d = week_start(b)
            n = sum(1 for x in bought if x < d) - sum(1 for x in condemned.values() if x < d)
            assert n == int(P.register[b]), (p, b, n, P.register[b])


if __name__ == "__main__":
    import sys
    WD = build(light="--light" in sys.argv)
    for p in POOLS:
        P = WD.pools[p]
        b, fut = truth(WD, p)
        print("%s lines %5d  D mean %6.0f  trade %6.0f..%6.0f  store mean %5.0f  other %5.0f  alive0 %6.0f now %6.0f "
              "register %6.0f  idle min %5.0f  truth %6.0f wk %s  hot %6.0f  lost/yr %5.0f  twice %.2f" % (
                  p, len(P.r), P.D.mean(), P.trade.min(), P.trade.max(), P.store.mean(), P.other.mean(), P.alive0,
                  P.alive[WH], P.register[WH], P.idle.min(), b["short"], week_start(b["i"]), truth_hot(WD, p)[0],
                  P.lost_w[104:].sum(), (P.iv == 0.5).mean()))
    if "--light" not in sys.argv:
        P = WD.pools["K20"]
        seen = sum(1 for t in P.trips if t[4] is not None)
        print("K20 kegs %d trips %d delivered %d (dockets %d) lost %d (%d) scrapped %d (%d) chase %d keg-level trade %d "
              "(%d) audits %d rackings %s" % (
                  P.keg_total, len(P.trips), seen, P.dlv.sum(), len(P.lost_kegs), P.lost_w.sum(), len(P.scrapped),
                  P.scrap.sum(), len(P.chase), P.keg_trade, P.trade[WH], len(WD.audits),
                  {q: len(WD.pools[q].rackings) for q in POOLS}))
