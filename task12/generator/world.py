"""The clean truth for task12: a Canadian household purchase panel's plant-based beverage category, 2024-W01 to
2026-W44, with Northvale Oat launched in 2026-W15, and the expected 2027 share of category litres.

Everything here is the world before any export, any mess or any document: households, their latent price tier,
their long-run category rate and transient buying phases, the banners each one shops, the distribution of the new
line by banner and week, each household's trial and repeat of it, and every purchase occasion's banner, brand,
pack and price. `simulate()` returns the clean panel; `truth_2027()` returns the exact expectation of the 2027
share given the state the panel ends in (no future draws, so it is deterministic)."""
import datetime as dt
import math

import numpy as np

SEED = 1208

# ---------------------------------------------------------------- calendar (ISO panel weeks, Monday start)
FIRST = dt.date.fromisocalendar(2024, 1, 1)
LAUNCH = dt.date.fromisocalendar(2026, 15, 1)       # Northvale on shelf in the launch banners
DISC_LIST = dt.date.fromisocalendar(2026, 24, 1)    # the two discount banners list the line
LYG_LIST = dt.date.fromisocalendar(2026, 39, 1)     # Loyal Grocer lists the line nationally
LAST = dt.date.fromisocalendar(2026, 44, 1)         # last panel week delivered
Y27_FIRST = dt.date.fromisocalendar(2027, 1, 1)
Y27_LAST = dt.date.fromisocalendar(2027, 52, 1)


def widx(d):
    return (d - FIRST).days // 7


T_LAUNCH, T_DISC, T_END = widx(LAUNCH), widx(DISC_LIST), widx(LAST)
T_LYG = widx(LYG_LIST)
T27_0, T27_1 = widx(Y27_FIRST), widx(Y27_LAST)
NW = T_END + 1                                       # observed weeks
NW_ALL = T27_1 + 1


def week_start(t):
    return FIRST + dt.timedelta(days=7 * t)


def iso_label(t):
    y, w, _ = week_start(t).isocalendar()
    return '%04d-W%02d' % (y, w)


# ---------------------------------------------------------------- the market
REGIONS = ['ATL', 'QC', 'ON', 'PR', 'BC']
REGION_P = [0.066, 0.226, 0.386, 0.181, 0.141]
TIERS = ['P', 'M', 'V']
TIER_P = np.array([0.300, 0.330, 0.370])
RATE_TIER = np.array([0.276, 0.333, 0.435])     # category occasions a week, by tier
LITRES_TIER = np.array([1.22, 1.88, 2.79])   # litres an occasion: barista cartons, 1.75 L, 1.89 L and twin packs

# banners: code, name, channel, regions served (empty = national)
BANNERS = [
    ('FMF', 'Foxmere Fresh', 'premium', ['ON', 'BC', 'PR']),
    ('GLM', 'Greenleaf Market', 'natural', ['ON', 'BC', 'QC']),
    ('LYG', 'Loyal Grocer', 'mainstream', []),
    ('NGF', 'Northglen Foods', 'mainstream', ['PR', 'BC', 'ON']),
    ('MBV', 'Marche Belvoir', 'mainstream', ['QC', 'ATL']),
    ('VLW', 'ValuWay', 'discount', []),
    ('TBK', 'Trade Basket', 'discount', ['ATL', 'ON', 'QC']),
    ('CWC', 'Costwell Club', 'club', []),
]
NB = len(BANNERS)
B_CODE = [b[0] for b in BANNERS]
B_CHAN = [b[2] for b in BANNERS]
DISCOUNT = np.array([c == 'discount' for c in B_CHAN])
LAUNCH_BANNERS = np.array([c in ('premium', 'natural', 'mainstream') and code != 'LYG' for code, c in zip(B_CODE, B_CHAN)])
LYG = np.array([code == 'LYG' for code in B_CODE])

# brand families (non-Northvale): name, tier group, base price per litre (CAD, everyday), litres per pack options
BRANDS = [
    ('Prairie Grove', 'main', 2.62), ('Silverbrook', 'main', 2.48), ('Coastline', 'main', 2.95),
    ('Wildflax', 'prem', 3.55), ('Haven & Hollow', 'prem', 3.78), ('Little Ferns', 'prem', 3.30),
    ('PL', 'pl', 1.78),
]
NBR = len(BRANDS)
NV_PRICE_L = {'1750': 5.79 / 1.75, '946': 4.49 / 0.946}

# ---------------------------------------------------------------- Northvale behaviour by tier (P, M, V)
P_TRY = np.array([1.0586, 0.0160, 0.0039])     # first-purchase chance per stocking occasion at everyday price
S0 = np.array([0.6649, 0.2860, 0.1608])             # share of occasions to the line just after trial
FLOOR = np.array([0.2565, 0.0624, 0.0118])      # long-run share once the novelty is gone
TAU = np.array([3.00, 6.50, 1.40])               # weeks for the novelty to fade by a factor e
# trial and repeat lifts by promotion kind: 1 launch price (launch banners), 2 discounters' listing price,
# 3 the mainstream multibuy
TRY_BOOST = {1: np.array([0.30, 1.20, 0.00]), 2: np.array([0.20, 2.00, 6.00]), 3: np.array([0.18, 120.00, 7.79])}
REP_LIFT = {1: np.array([1.05, 1.40, 2.00]), 2: np.array([1.05, 1.60, 3.00]), 3: np.array([1.05, 1.40, 2.00])}
MEDIA_TRY = 2.57                                # trial lift on a media week

# transient buying phases: log-AR(1), weekly persistence and innovation
RHO, SIG = 0.95, 0.161
PHASE_TRY = 1.91                                # trial propensity rises with the phase (u ** PHASE_TRY)
PROP_SHAPE = 1.20
WILLING = np.array([0.625, 0.660, 0.485])
EVERYDAY_TRY = 0.0010                            # trial once the line is no longer new, as a share of the novelty rate
TAU_NOV = 4.0                                  # weeks for the line's newness on a banner's shelf to fade by e


def seasonal(t):
    """Category seasonality by week of year: higher in January, lower in high summer."""
    w = week_start(t).isocalendar()[1]
    return 1.0 + 0.075 * math.cos(2 * math.pi * (w - 2) / 52.0)


def growth(t):
    return 1.048 ** (t / 52.18)


def media_week(t):
    """Northvale's 2026 TV and online video bursts (from the media plan)."""
    return (T_LAUNCH <= t <= T_LAUNCH + 5) or (widx(dt.date.fromisocalendar(2026, 39, 1)) <= t <=
                                                widx(dt.date.fromisocalendar(2026, 42, 1)))


def promo(t, b):
    """The kind of Northvale price promotion in banner b in week t (from the trade calendar), 0 for none."""
    if LAUNCH_BANNERS[b] and T_LAUNCH <= t <= T_LAUNCH + 3:
        return 1                                          # launch price, four weeks
    if DISCOUNT[b] and T_DISC <= t <= T_DISC + 2:
        return 2                                          # discounters' listing price, three weeks
    if B_CHAN[b] == 'mainstream' and widx(dt.date.fromisocalendar(2026, 39, 1)) <= t <= \
            widx(dt.date.fromisocalendar(2026, 41, 1)):
        return 3                                          # a three-week multibuy in the mainstream banners
    return 0


def distribution(t, b):
    """Weighted distribution of the line (share of the banner's category sales in stores stocking it)."""
    if B_CHAN[b] == 'club':
        return 0.0
    if LYG[b]:
        if t < T_LYG:
            return 0.0
        ramp = [0.71, 0.92, 0.96]
        k = t - T_LYG
        return ramp[k] if k < len(ramp) else 0.97
    if LAUNCH_BANNERS[b]:
        if t < T_LAUNCH:
            return 0.0
        ramp = [0.58, 0.79, 0.90, 0.95]
        k = t - T_LAUNCH
        return ramp[k] if k < len(ramp) else 0.96
    if t < T_DISC:
        return 0.0
    ramp = [0.62, 0.86, 0.93]
    k = t - T_DISC
    return ramp[k] if k < len(ramp) else 0.94


DIST = np.array([[distribution(t, b) for b in range(NB)] for t in range(NW_ALL)])
LIST_WEEK = np.array([T_LAUNCH if LAUNCH_BANNERS[b] else (T_DISC if DISCOUNT[b] else (T_LYG if LYG[b] else 10 ** 6)) for b in range(NB)])


def novelty(t):
    return np.where(t >= LIST_WEEK, np.exp(-np.clip(t - LIST_WEEK, 0, 10 ** 4) / TAU_NOV), 0.0)
PROMO_KIND = np.array([[promo(t, b) if t <= T_END else 0 for b in range(NB)] for t in range(NW_ALL)])
PROMO = PROMO_KIND > 0
MEDIA = np.array([media_week(t) if t <= T_END else False for t in range(NW_ALL)])
SEAS = np.array([seasonal(t) for t in range(NW_ALL)])
GROW = np.array([growth(t) for t in range(NW_ALL)])


# each household does most of its mainstream shopping at one chain: the chain's weight is kept and every other
# mainstream chain serving its region is cut to PRIMARY_KEEP of its draw (the mainstream total is held)
PRIMARY_KEEP = 0.04
LYG_PRIMARY_P = np.array([0.05, 0.70, 0.60])     # Loyal Grocer is the main chain mostly of mainstream and value shoppers


# ---------------------------------------------------------------- households
def households(rng, n=18000):
    region = rng.choice(len(REGIONS), n, p=REGION_P)
    tier = rng.choice(3, n, p=TIER_P)
    size = np.clip(rng.poisson(np.array([1.3, 1.6, 1.9])[tier]) + 1, 1, 7)
    buyer = rng.random(n) < np.array([0.56, 0.47, 0.42])[tier]
    mean_rate = RATE_TIER[tier] * (0.85 + 0.08 * size)
    k = 0.85
    lam = np.where(buyer, rng.gamma(k, mean_rate / k), 0.0)
    # banner mix: weights by channel for the tier, restricted to banners serving the region
    chan_w = {
        0: {'premium': 3.2, 'natural': 2.0, 'mainstream': 3.0, 'discount': 0.55, 'club': 0.6},
        1: {'premium': 0.8, 'natural': 0.5, 'mainstream': 5.0, 'discount': 1.5, 'club': 0.9},
        2: {'premium': 0.15, 'natural': 0.1, 'mainstream': 2.3, 'discount': 5.2, 'club': 1.1},
    }
    mix = np.zeros((n, NB))
    rng_p = np.random.default_rng(SEED + 919)     # its own stream, so the other draws are unchanged
    for i in range(n):
        reg = REGIONS[region[i]]
        w = np.array([chan_w[tier[i]][B_CHAN[b]] if (not BANNERS[b][3] or reg in BANNERS[b][3]) else 0.0
                      for b in range(NB)])
        w = w * rng.gamma(1.2, 1.0, NB)
        if PRIMARY_KEEP < 1.0:
            main = [b for b in range(NB) if B_CHAN[b] == 'mainstream' and w[b] > 0]
            if len(main) > 1:
                p_lyg = LYG_PRIMARY_P[tier[i]] if np.ndim(LYG_PRIMARY_P) else LYG_PRIMARY_P
                lyg_first = rng_p.random() < p_lyg
                prim = B_CODE.index('LYG') if lyg_first else next(b for b in main if B_CODE[b] != 'LYG')
                tot = w[main].sum()
                for b in main:
                    if b != prim:
                        w[b] *= PRIMARY_KEEP
                w[main] *= tot / w[main].sum()
        mix[i] = w / w.sum()
    # brand preference over the seven brand families
    base = {0: [0.07, 0.05, 0.06, 0.30, 0.24, 0.20, 0.08], 1: [0.30, 0.26, 0.12, 0.04, 0.03, 0.03, 0.22],
            2: [0.10, 0.08, 0.03, 0.01, 0.005, 0.005, 0.77]}
    pref = np.vstack([rng.dirichlet(np.array(base[tier[i]]) * 24.0) for i in range(n)])
    willing = rng.random(n) < WILLING[tier]                 # households that would ever buy the line
    propensity = np.where(willing, rng.gamma(PROP_SHAPE, 1 / PROP_SHAPE, n), 0.0)
    floor_mult = rng.gamma(5.0, 1 / 5.0, n)                  # within-tier spread of the long-run share
    club = mix[:, B_CODE.index('CWC')] > 0.25
    litres_occ = np.where(club, 5.68, LITRES_TIER[tier] * rng.uniform(0.85, 1.18, n))
    barista = rng.random(n) < np.array([0.55, 0.20, 0.06])[tier]          # the household's Northvale SKU
    nv_units = np.maximum(1, np.round(litres_occ / np.where(barista, 0.946, 1.75) * 0.8)).clip(1, 3)
    nv_litres = np.where(barista, 0.946, 1.75) * nv_units
    # panel membership: join and leave weeks (attrition about 9 per cent a year, replaced by recruits)
    join = np.where(rng.random(n) < 0.83, 0, rng.integers(1, NW, n))
    leave = np.where(rng.random(n) < 0.20, rng.integers(20, NW + 60, n), NW_ALL + 10)
    leave = np.maximum(leave, join + 12)
    return dict(n=n, region=region, tier=tier, size=size, buyer=buyer, lam=lam, mix=mix, pref=pref,
                propensity=propensity, floor_mult=floor_mult, litres_occ=litres_occ, join=join, leave=leave,
                barista=barista, nv_units=nv_units, nv_litres=nv_litres)


def phases(rng, n, nw):
    """Transient buying phases u (mean one), weekly log-AR(1)."""
    x = rng.normal(0, SIG / math.sqrt(1 - RHO ** 2), n)
    out = np.empty((nw, n))
    c = 0.5 * SIG ** 2 / (1 - RHO ** 2)
    for t in range(nw):
        x = RHO * x + rng.normal(0, SIG, n)
        out[t] = np.exp(x - c)
    return out, x


def simulate(seed=SEED, n=18000):
    """The clean panel, household-week aggregates plus each Northvale purchase's banner. Returns a dict."""
    rng = np.random.default_rng(seed)
    H = households(rng, n)
    u, x_end = phases(np.random.default_rng(seed + 1), n, NW)
    occ = np.zeros((NW, n), dtype=np.int32)
    nv = np.zeros((NW, n), dtype=np.int32)                   # Northvale occasions
    nv_promo = np.zeros((NW, n), dtype=np.int32)
    tried = np.full(n, -1)
    trial_banner = np.full(n, -1)
    r_occ = np.random.default_rng(seed + 2)
    r_nv = np.random.default_rng(seed + 3)
    tier = H['tier']
    inpanel = lambda t: (H['join'] <= t) & (t < H['leave'])
    for t in range(NW):
        rate = H['lam'] * u[t] * SEAS[t] * GROW[t]
        o = r_occ.poisson(rate) * inpanel(t)
        occ[t] = o
        if t < T_LAUNCH:
            continue
        # stocking occasions split into promoted and everyday banners for this household
        stock_w = H['mix'] * DIST[t][None, :]
        promo_w = stock_w * PROMO[t][None, :]
        p_stock = stock_w.sum(1)
        p_promo_in_stock = np.divide(promo_w.sum(1), p_stock, out=np.zeros(n), where=p_stock > 0)
        o_stock = r_nv.binomial(o, np.clip(p_stock, 0, 1))
        o_pr = r_nv.binomial(o_stock, p_promo_in_stock)
        o_ev = o_stock - o_pr
        kinds = set(PROMO_KIND[t][PROMO_KIND[t] > 0].tolist())
        kind = kinds.pop() if kinds else 0
        has = tried >= 0
        # repeat
        ten = np.where(has, t - tried, 0)
        f = FLOOR[tier] * H['floor_mult']
        s = np.clip(f + (S0[tier] - f) * np.exp(-ten / TAU[tier]), 0, 0.95)
        rep_ev = r_nv.binomial(o_ev, np.where(has, s, 0.0))
        rl = REP_LIFT[kind][tier] if kind else 1.0
        rep_pr = r_nv.binomial(o_pr, np.where(has, np.clip(s * rl, 0, 0.95), 0.0))
        # trial: the chance any stocking occasion this week is a first purchase. While the line is new on the
        # household's shelves it is tried by households exploring the category (high phases); a promotion adds its
        # own pull; otherwise it is tried only now and then.
        nov_h = (stock_w * novelty(t)[None, :]).sum(1) / np.maximum(p_stock, 1e-12)
        pull = P_TRY[tier] * H['propensity'] * u[t] ** PHASE_TRY * (MEDIA_TRY if MEDIA[t] else 1.0)
        q_ev = 1 - (1 - np.clip(pull * (EVERYDAY_TRY + nov_h), 0, 0.9)) ** o_ev
        boost = TRY_BOOST[kind][tier] if kind else 0.0
        q_pr = 1 - (1 - np.clip(pull * (EVERYDAY_TRY + nov_h + boost), 0, 0.9)) ** o_pr
        try_pr = (~has) & (r_nv.random(n) < q_pr)
        try_ev = (~has) & ~try_pr & (r_nv.random(n) < q_ev)
        new = try_pr | try_ev
        # the banner of the first purchase: drawn from the stocking banners, promoted ones if a promoted trial
        if new.any():
            idx = np.nonzero(new)[0]
            w_tr = np.where(try_pr[idx, None], promo_w[idx], stock_w[idx] * (1 - PROMO[t][None, :]))
            bad = w_tr.sum(1) <= 0
            w_tr[bad] = stock_w[idx][bad]
            cum = np.cumsum(w_tr / w_tr.sum(1, keepdims=True), axis=1)
            trial_banner[idx] = (r_nv.random(len(idx))[:, None] > cum).sum(1)
            tried[idx] = t
        nv[t] = rep_ev + rep_pr + new
        nv_promo[t] = rep_pr + try_pr
    return dict(H=H, u=u, x_end=x_end, occ=occ, nv=nv, nv_promo=nv_promo, tried=tried, trial_banner=trial_banner)


def truth_2027(S, reps=8, seed=SEED + 50, litres=None):
    """The expected 2027 share of category litres (panel weeks 2027-W01 to 2027-W52) given the state the panel
    ends in at 2026-W44, at everyday price, the distribution held at the review, no promotions and no media: the
    average over `reps` seeded futures of the same households (each future draws its own phases, occasions,
    trials and repeats). Deterministic for a given seed."""
    H = S['H']
    n = H['n']
    tier = H['tier']
    lit = H['litres_occ'] if litres is None else litres
    inp = (H['join'] <= T_END) & (T_END < H['leave'])
    stock = (H['mix'] * DIST[T_END][None, :]).sum(1)
    c = 0.5 * SIG ** 2 / (1 - RHO ** 2)
    f = FLOOR[tier] * H['floor_mult']
    shares, cat_l, line_l, ex_l, new_l, ntry = [], [], [], [], [], []
    for r in range(reps):
        rng = np.random.default_rng(seed + r)
        x = S['x_end'].copy()
        tried = S['tried'].copy()
        ex = tried >= 0
        cat = line_ex = line_new = 0.0
        for t in range(T_END + 1, T27_1 + 1):
            x = RHO * x + rng.normal(0, SIG, n)
            u = np.exp(x - c)
            o = rng.poisson(H['lam'] * u * SEAS[t] * GROW[t]) * inp
            o_s = rng.binomial(o, np.clip(stock, 0, 1))
            has = tried >= 0
            ten = np.where(has, t - tried, 0)
            s = np.clip(f + (S0[tier] - f) * np.exp(-ten / TAU[tier]), 0, 0.95)
            rep = rng.binomial(o_s, np.where(has, s, 0.0))
            nov_h = (H['mix'] * DIST[T_END][None, :] * novelty(t)[None, :]).sum(1) / np.maximum(stock, 1e-12)
            base = P_TRY[tier] * H['propensity'] * u ** PHASE_TRY * (EVERYDAY_TRY + nov_h)
            q = 1 - (1 - np.clip(base, 0, 0.9)) ** o_s
            new = (~has) & (rng.random(n) < q)
            tried[new] = t
            if t >= T27_0:
                cat += (o * lit).sum()
                line_ex += (np.where(ex, rep, 0) * H['nv_litres']).sum()
                line_new += (np.where(~ex, rep + new, 0) * H['nv_litres']).sum()
        cat_l.append(cat); ex_l.append(line_ex); new_l.append(line_new)
        shares.append((line_ex + line_new) / cat)
        ntry.append(((tried >= 0) & ~ex).sum())
    return dict(share=float(np.mean(shares)), share_sd=float(np.std(shares)), cat_litres=float(np.mean(cat_l)),
                existing_litres=float(np.mean(ex_l)), new_litres=float(np.mean(new_l)), new_triers=float(np.mean(ntry)))


if __name__ == '__main__':
    import time
    t0 = time.time()
    S = simulate()
    T = truth_2027(S)
    print('simulated in %.1fs; truth share 2027 %.3f%%' % (time.time() - t0, 100 * T['share']))
