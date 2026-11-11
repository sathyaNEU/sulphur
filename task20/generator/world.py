"""task20 architecture 2 world: Brindle & Moss, a listed home-furnishings retailer, and the Kestrel Spend Panel, a
card-transaction panel a long-short fund buys. Simulated here: the company's weekly sales by region and channel, the
acquired Fernhollow banner and the licensed shop-in-shops, the tender mix (bank cards, the B&M private-label card,
other), and the panel: issuers joining and leaving, card cohorts opened each quarter, attrition, spend that settles
with card tenure, and posting lags that leave the latest weeks short in each weekly delivery. Nothing here writes a
file; pack.py turns a World into the shipped records."""
import numpy as np
import pandas as pd

REGIONS = ["Northeast", "Southeast", "Midwest", "West"]
MERCHANTS = ["stores", "outlet", "web", "fernhollow", "licensed", "cafe"]
FY_START = pd.Timestamp("2021-01-31")
FY_ENDS = [pd.Timestamp(x) for x in ("2022-01-29", "2023-01-28", "2024-02-03", "2025-02-01", "2026-01-31")]
FY_NAMES = ["FY2021", "FY2022", "FY2023", "FY2024", "FY2025"]
ACQUIRED = pd.Timestamp("2024-06-02")
BACK_YEARS = 4                      # the panel's back book: cards opened in the four years before an issuer's first week


def calendar():
    rows = []
    start = FY_START
    for fy, end in zip(FY_NAMES, FY_ENDS):
        n = ((end - start).days + 1) // 7
        lens = [13, 13, 13, 13 + (n - 52)]
        wk = 0
        for q, L in enumerate(lens, 1):
            for _ in range(L):
                rows.append(dict(week_start=start + pd.Timedelta(days=7 * wk), fy=fy, fq=q))
                wk += 1
        start = end + pd.Timedelta(days=1)
    cal = pd.DataFrame(rows)
    cal["week_end"] = cal.week_start + pd.Timedelta(days=6)
    cal["qkey"] = cal.fy + "Q" + cal.fq.astype(str)
    return cal


CAL = calendar()
W = len(CAL)
QKEYS = list(dict.fromkeys(CAL.qkey))
QIDX = np.array([QKEYS.index(q) for q in CAL.qkey])


def holidays(y):
    def nth(m, wd, k):
        d = pd.Timestamp(y, m, 1)
        return d + pd.Timedelta(days=(wd - d.weekday()) % 7 + 7 * (k - 1))
    may_end = pd.Timestamp(y, 5, 31)
    memorial = may_end - pd.Timedelta(days=(may_end.weekday() - 0) % 7)
    tg = nth(11, 3, 4)
    return [(nth(2, 0, 3), 1.20), (memorial, 1.26), (pd.Timestamp(y, 7, 4), 1.08), (nth(9, 0, 1), 1.22),
            (tg + pd.Timedelta(days=1), 1.80), (tg + pd.Timedelta(days=4), 1.30), (pd.Timestamp(y, 12, 26), 1.16)]


def season_index():
    month = {1: 0.84, 2: 0.94, 3: 1.0, 4: 0.98, 5: 1.02, 6: 0.95, 7: 0.96, 8: 1.0, 9: 1.0, 10: 1.02, 11: 1.07, 12: 1.13}
    idx = np.array([month[d.month] for d in CAL.week_start])
    for n, d in enumerate(CAL.week_start):
        e = d + pd.Timedelta(days=6)
        for day, f in holidays(d.year) + holidays(d.year - 1):
            if d <= day <= e:
                idx[n] *= f
    return idx


def season_of(d):
    month = {1: 0.84, 2: 0.94, 3: 1.0, 4: 0.98, 5: 1.02, 6: 0.95, 7: 0.96, 8: 1.0, 9: 1.0, 10: 1.02, 11: 1.07, 12: 1.13}
    f = month[d.month]
    e = d + pd.Timedelta(days=6)
    for day, m in holidays(d.year) + holidays(d.year - 1):
        if d <= day <= e:
            f *= m
    return f


def lead_path(P, pre):
    """made-to-order weeks from order to delivery, by the week the order is placed (pre weeks before the panel's first):
    the 2021 backlog building, its unwind in fiscal 2022, normal from fiscal 2023, lengthening in fiscal 2025"""
    out = np.empty(pre + W)
    for n in range(pre + W):
        t = n - pre
        if t < 0:
            out[n] = P["lead_start"]
        elif t <= 51:
            out[n] = P["lead_start"] + (P["lead_peak"] - P["lead_start"]) * t / 51.0
        elif t <= P["unwind_end"]:
            out[n] = P["lead_peak"] + (P["lead_norm"] - P["lead_peak"]) * (t - 51) / float(P["unwind_end"] - 51)
        elif t < P["late_from"]:
            out[n] = P["lead_norm"]
        elif t < P["late_full"]:
            out[n] = P["lead_norm"] + (P["lead_late"] - P["lead_norm"]) * (t - P["late_from"]) / float(P["late_full"] - P["late_from"])
        else:
            out[n] = P["lead_late"]
    return out


def default_params():
    return dict(
        base={"Northeast": 23.0, "Southeast": 13.0, "Midwest": 20.0, "West": 15.0},     # USD m a week, FY2021
        growth={"Northeast": -0.04, "Southeast": 0.13, "Midwest": -0.02, "West": 0.07},
        year_growth=[0.06, 0.02, 0.0, 0.025, 0.03],                                   # the category's trend by fiscal year
        turn_week=248, turn=-0.07, turn_weeks=4,                                      # the holiday quarter's softer demand
        mto=0.30,                                  # made-to-order share of the banner's store and site orders
        lead_start=8.0, lead_peak=8.0, unwind_end=95, lead_norm=8.0,             # weeks from order to delivery
        late_from=900, late_full=901, lead_late=8.0,
        mto_event=[0.10, 0.14, 0.0, 0.03, 0.60],   # the December to January made-to-order event's lift, by fiscal year
        ws_base=13.0, ws_trend=0.25, ws_noise=1.6,  # wholesale contract sales, USD m a quarter (invoiced, not on cards)
        ws_lumps={"FY2022Q2": 8.0, "FY2023Q3": 10.0, "FY2024Q4": 36.0},
        web0=0.17, web1=0.27, fern=0.085, lic0=0.055, lic_growth=0.16, cafe=0.006,
        own0=0.245, own_drift=0.010, own_drift_late=0.040, late_drift_from=209, other=0.12,
        issuers={"A": dict(join=0, leave=None, size=1.00, mix=[0.15, 0.32, 0.15, 0.38]),
                 "B": dict(join=0, leave=None, size=0.60, mix=[0.04, 0.82, 0.04, 0.10]),
                 "C": dict(join=0, leave=None, size=0.55, mix=[0.06, 0.08, 0.04, 0.82]),
                 "D": dict(join=70, leave=None, size=0.50, mix=[0.03, 0.55, 0.04, 0.38]),
                 "E": dict(join=150, leave=None, size=0.70, mix=[0.25, 0.26, 0.22, 0.27]),
                 "F": dict(join=0, leave=248, size=1.30, mix=[0.06, 0.02, 0.88, 0.04])},
        cohort=52000.0, attrition=0.004, tau=60.0, floor=0.65,
        lag0=(0.74, 0.90), lag1=(0.94, 0.985), lag2=(0.992, 0.999), noise=0.015, rev_noise=0.003)


class World:
    pass


def simulate(seed, **kw):
    P = default_params()
    P.update(kw)
    r = np.random.default_rng(seed)
    w = World()
    w.P, w.seed = P, seed
    t = np.arange(W) / 52.0
    fyi = np.array([FY_NAMES.index(f) for f in CAL.fy])
    # the category: a weekly log-level that grows at each fiscal year's rate, a slow AR wobble, the season
    weekly = np.array([np.log1p(P["year_growth"][k]) / 52.0 for k in fyi])
    ar = np.zeros(W)
    for i in range(1, W):
        ar[i] = 0.95 * ar[i - 1] + r.normal(0, 0.003)
    turn = P["turn"] * np.clip((np.arange(W) - P["turn_week"] + 1) / float(P["turn_weeks"]), 0, 1)
    level = np.exp(np.cumsum(weekly) + ar + turn)
    w.traffic = np.exp(np.cumsum(weekly) + ar)       # store and site visits: the turn is fewer purchases per visit
    season = season_index()
    reg_sales = np.zeros((W, 4))
    for j, reg in enumerate(REGIONS):
        reg_sales[:, j] = P["base"][reg] * np.exp(P["growth"][reg] * t) * level * season * np.exp(r.normal(0, 0.012, W))
    web = np.clip(P["web0"] + (P["web1"] - P["web0"]) * t / t[-1] + r.normal(0, 0.004, W), 0.1, 0.4)
    outlet = 0.07
    share_r = reg_sales / reg_sales.sum(1, keepdims=True)
    total = reg_sales.sum(1)
    fern = P["fern"] * total * np.exp(r.normal(0, 0.02, W))
    lic = P["lic0"] * total * np.exp(P["lic_growth"] * t) * np.exp(r.normal(0, 0.03, W))
    cafe = P["cafe"] * total * np.exp(r.normal(0, 0.05, W))
    consolidated = (CAL.week_start >= ACQUIRED).values
    # merchant sales by region (USD m a week): what each merchant id in the panel sells to everyone
    ev = np.ones(W)
    for n, d in enumerate(CAL.week_start):
        if CAL.fq.iloc[n] == 4 and (d.month == 12 or d.month == 1 or (d.month == 11 and d.day >= 28)):
            ev[n] = 1.0 + P["mto_event"][fyi[n]]
    w.event = ev
    lift = (1 - P["mto"]) + P["mto"] * ev                 # store and site orders with the event's made-to-order lift
    w.mto_share = P["mto"] * ev / lift                    # made-to-order share of store and site orders, by week
    msales = np.zeros((W, 4, len(MERCHANTS)))
    msales[:, :, 0] = reg_sales * (1 - web[:, None]) * (1 - outlet) * lift[:, None]
    msales[:, :, 1] = reg_sales * (1 - web[:, None]) * outlet
    msales[:, :, 2] = reg_sales * web[:, None] * lift[:, None]
    msales[:, :, 3] = fern[:, None] * share_r
    msales[:, :, 4] = lic[:, None] * share_r
    msales[:, :, 5] = cafe[:, None] * share_r
    w.reg_sales, w.msales, w.web, w.fern, w.lic, w.consolidated = reg_sales, msales, web, fern, lic, consolidated
    # revenue is recognised on delivery: in-stock and outlet orders the week they are placed, made-to-order orders after
    # the lead time of the week they were placed; customers pay in full at order, so undelivered orders are deposits
    pre = 60
    pre_level = level[0] * np.exp(-np.log1p(P["year_growth"][0]) / 52.0 * np.arange(pre, 0, -1))
    pre_dates = [FY_START - pd.Timedelta(days=7 * k) for k in range(pre, 0, -1)]
    pre_season = np.array([season_of(d) for d in pre_dates])
    mto_r = np.zeros((pre + W, 4))
    for j, reg in enumerate(REGIONS):
        pre_reg = P["base"][reg] * np.exp(P["growth"][reg] * (np.arange(-pre, 0) / 52.0)) * pre_level * pre_season
        mto_r[:pre, j] = P["mto"] * pre_reg * (1 - web[0]) * (1 - outlet) + P["mto"] * pre_reg * web[0]
    mto_r[pre:] = w.mto_share[:, None] * (msales[:, :, 0] + msales[:, :, 2])
    lead = lead_path(P, pre)
    dlv = np.zeros((pre + W + 40, 4))
    for n in range(pre + W):
        d = n + lead[n]
        lo = int(np.floor(d))
        fr = d - lo
        dlv[lo] += mto_r[n] * (1 - fr)
        dlv[lo + 1] += mto_r[n] * fr
    instock = (1 - w.mto_share[:, None]) * (msales[:, :, 0] + msales[:, :, 2]) + msales[:, :, 1]
    banner = instock + dlv[pre:pre + W]
    dep = np.cumsum(mto_r.sum(1))[pre:] - np.cumsum(dlv.sum(1))[pre:pre + W]
    w.lead = lead[pre:]
    w.orders_w = msales[:, :, :3].sum((1, 2)) + np.where(consolidated, fern, 0.0)
    w.deposits_w = dep
    w.deposits_open = float(np.cumsum(mto_r.sum(1))[pre - 1] - np.cumsum(dlv.sum(1))[pre - 1])
    rev_w = banner.sum(1) + np.where(consolidated, fern, 0.0)
    w.rev_w = rev_w
    rev_q = np.array([rev_w[QIDX == q].sum() for q in range(len(QKEYS))]) * np.exp(r.normal(0, P["rev_noise"], len(QKEYS)))
    rw = np.random.default_rng(seed + 991)
    ws = np.array([P["ws_base"] + P["ws_trend"] * q + rw.normal(0, P["ws_noise"]) + P["ws_lumps"].get(k, 0.0)
                   for q, k in enumerate(QKEYS)])
    w.wholesale_q = ws
    w.retail_q = rev_q
    rev_q = rev_q + ws
    w.rev_q = rev_q
    w.rev_q_region = np.array([banner[QIDX == q].sum(0) for q in range(len(QKEYS))])
    w.dep_q = np.array([dep[np.where(QIDX == q)[0][-1]] for q in range(len(QKEYS))])
    tl = np.maximum(np.arange(W) - P["late_drift_from"], 0) / 52.0
    own = P["own0"] - P["own_drift"] * t - (P["own_drift_late"] - P["own_drift"]) * tl + r.normal(0, 0.002, W)
    bank = 1.0 - own - P["other"]
    w.own, w.bank = own, bank
    # the panel's cards: cohorts by issuer, region and the fiscal quarter they were opened
    iss = list(P["issuers"])
    qstart = [n for n in range(W) if n == 0 or QIDX[n] != QIDX[n - 1]]
    w.qstart = qstart
    co = []                                          # (issuer, region, open week, opened)
    for i, name in enumerate(iss):
        d = P["issuers"][name]
        first = d["join"]
        for j in range(4):
            for b in range(1, 4 * BACK_YEARS + 1):           # the back book at the issuer's first week
                n = P["cohort"] * d["size"] * d["mix"][j] * np.exp(r.normal(0, 0.10))
                co.append((i, j, first - 13 * b, n))
            for qs in qstart:
                if qs < first or (d["leave"] is not None and qs >= d["leave"]):
                    continue
                co.append((i, j, qs, P["cohort"] * d["size"] * d["mix"][j] * np.exp(r.normal(0, 0.08))))
    w.issuers = iss
    w.co = co
    # spend per card per week at each merchant: the region's bank-card spend there, per reference card, settling with tenure
    ref_cards = 4.0e6                                # bank cards behind each region's spend, the panel's sampling base
    pi = msales * bank[:, None, None] / ref_cards * 1e6            # USD per reference card per week
    w.pi = pi
    n_co = len(co)
    active = np.zeros((W, n_co))
    settle = np.zeros((W, n_co))
    for c, (i, j, ow, n0) in enumerate(co):
        d = P["issuers"][iss[i]]
        lo, hi = max(d["join"], ow, 0), (W if d["leave"] is None else d["leave"])
        if lo >= hi:
            continue
        wk = np.arange(lo, hi)
        ten = wk - ow
        active[lo:hi, c] = n0 * np.exp(-P["attrition"] * ten)
        settle[lo:hi, c] = P["floor"] + (1 - P["floor"]) * np.exp(-ten / P["tau"])
    w.active, w.settle = active, settle
    reg_of = np.array([j for (_, j, _, _) in co])
    noise = np.exp(r.normal(0, P["noise"], (W, n_co, len(MERCHANTS))))
    spend = active[:, :, None] * settle[:, :, None] * pi[:, reg_of, :] * noise          # USD, complete
    w.spend = spend
    txn_size = np.array([310.0, 140.0, 260.0, 120.0, 95.0, 14.0])
    w.txns = np.round(spend / txn_size[None, None, :] * np.exp(r.normal(0, 0.05, spend.shape)))
    # posting completeness by issuer in the latest deliveries (lag 0 is the week just ended)
    w.lag0 = r.uniform(*P["lag0"], len(iss))
    w.lag1 = r.uniform(*P["lag1"], len(iss))
    w.lag2 = r.uniform(*P["lag2"], len(iss))
    # the weekly deliveries of the last six months: each issuer's latest weeks as first delivered
    deliveries = [CAL.week_start.iloc[-1] + pd.Timedelta(days=8) - pd.Timedelta(days=7 * k) for k in range(26, -1, -1)]
    w.deliveries = deliveries
    comp = {}
    for d in deliveries:
        last = int(np.searchsorted(CAL.week_start.values, (d - pd.Timedelta(days=8)).to_datetime64(), side="right")) - 1
        for i in range(len(iss)):
            for lag, rng_ in ((0, w.lag0), (1, w.lag1), (2, w.lag2)):
                comp[(d, i, last - lag)] = float(np.clip(rng_[i] + r.normal(0, 0.012 if lag == 0 else 0.004), 0.5, 1.0))
    w.comp = comp
    w.last_week = W - 1
    return w
