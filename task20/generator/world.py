"""task20 architecture 2 world (second hardening): Brindle & Moss, a listed home-furnishings retailer, and the Kestrel Spend Panel, a
card-transaction panel a long-short fund buys. Simulated here: the company's weekly orders by region and channel, the
made-to-order business (paid at order, recognised on delivery eight weeks later) with its holiday design event, the
design studios opening over the years, the acquired Fernhollow banner, the licensed shop-in-shops and cafes, the
contract division's invoiced sales, and the panel: six issuers whose cardholders differ in how much they spend at the
retailer, issuers joining and leaving, card accounts opened every four weeks and closing at a steady rate, spend that
settles with tenure, two card-portfolio conversions (an outside bank's book re-issued by KS-02 in May 2023, and KS-06's
premium book re-issued by KS-01 in October 2025 before KS-06's feed ends), and posting lags that leave the latest weeks
short in each weekly delivery. Nothing here writes a file; pack.py turns a World into the shipped records."""
import numpy as np
import pandas as pd

REGIONS = ["Northeast", "Southeast", "Midwest", "West"]
MERCHANTS = ["stores", "outlet", "web", "fernhollow", "licensed", "cafe"]
FY_START = pd.Timestamp("2021-01-31")
FY_ENDS = [pd.Timestamp(x) for x in ("2022-01-29", "2023-01-28", "2024-02-03", "2025-02-01", "2026-01-31")]
FY_NAMES = ["FY2021", "FY2022", "FY2023", "FY2024", "FY2025"]
ACQUIRED = pd.Timestamp("2024-06-02")
STEP = 4                            # card accounts are opened in four-week batches


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
FYI = np.array([FY_NAMES.index(f) for f in CAL.fy])


def week_of(d):
    return int(np.searchsorted(CAL.week_start.values, pd.Timestamp(d).to_datetime64(), side="right")) - 1


def holidays(y):
    def nth(m, wd, k):
        d = pd.Timestamp(y, m, 1)
        return d + pd.Timedelta(days=(wd - d.weekday()) % 7 + 7 * (k - 1))
    may_end = pd.Timestamp(y, 5, 31)
    memorial = may_end - pd.Timedelta(days=(may_end.weekday() - 0) % 7)
    tg = nth(11, 3, 4)
    return [(nth(2, 0, 3), 1.20), (memorial, 1.26), (pd.Timestamp(y, 7, 4), 1.08), (nth(9, 0, 1), 1.22),
            (tg + pd.Timedelta(days=1), 1.80), (tg + pd.Timedelta(days=4), 1.30), (pd.Timestamp(y, 12, 26), 1.16)]


MONTH = {1: 0.84, 2: 0.94, 3: 1.0, 4: 0.98, 5: 1.02, 6: 0.95, 7: 0.96, 8: 1.0, 9: 1.0, 10: 1.02, 11: 1.07, 12: 1.13}


def season_of(d):
    f = MONTH[d.month]
    e = d + pd.Timedelta(days=6)
    for day, m in holidays(d.year) + holidays(d.year - 1):
        if d <= day <= e:
            f *= m
    return f


def season_index():
    return np.array([season_of(d) for d in CAL.week_start])


def event_weeks(dates):
    """the design event runs from the Friday after Thanksgiving to the end of January"""
    out = np.zeros(len(dates), dtype=bool)
    for n, d in enumerate(dates):
        tg = holidays(d.year)[4][0]
        out[n] = d.month == 1 or d.month == 12 or (d.month == 11 and d + pd.Timedelta(days=6) >= tg)
    return out


def default_params():
    return dict(
        base={"Northeast": 23.0, "Southeast": 13.0, "Midwest": 20.0, "West": 15.0},     # USD m a week, FY2021
        growth={"Northeast": -0.04, "Southeast": 0.13, "Midwest": -0.02, "West": 0.07},
        year_growth=[0.06, 0.02, 0.0, 0.025, 0.03],                                   # the category's trend by fiscal year
        turn_week=248, turn=-0.055, turn_weeks=4,                                      # the holiday quarter's softer demand
        mto0=0.255, mto_studio=0.006,              # made-to-order share of store and site orders: a base and each studio's part
        lead=8.0,                                  # weeks from a made-to-order order to its delivery
        mto_event=[0.10, 0.20, 0.30, 0.40, 0.55],  # the design event's lift on made-to-order orders, by fiscal year
        studios=["2019-03-04", "2019-09-09", "2020-04-06", "2020-10-05", "2021-09-13", "2022-08-29", "2023-09-11",
                 "2024-03-04", "2025-08-25", "2025-09-22", "2025-10-13"],               # design studio openings
        ct_base=13.0, ct_trend=0.25, ct_noise=1.6,  # contract division sales, USD m a quarter (invoiced to businesses)
        ct_lumps={"FY2022Q2": 8.0, "FY2023Q3": 10.0, "FY2024Q4": 38.0},
        web0=0.17, web1=0.27, fern=0.085, lic0=0.055, lic_growth=0.16, cafe=0.006,
        bank=0.67,                                 # bank-card share of the banner's customer payments
        issuers={"A": dict(join=0, leave=None, size=1.00, mix=[0.20, 0.27, 0.25, 0.28], prop=1.00, acq=0.03),
                 "B": dict(join=0, leave=None, size=0.60, mix=[0.04, 0.82, 0.04, 0.10], prop=0.85, acq=0.00),
                 "C": dict(join=0, leave=None, size=0.55, mix=[0.06, 0.08, 0.04, 0.82], prop=1.10, acq=-0.04),
                 "D": dict(join=70, leave=None, size=0.50, mix=[0.03, 0.55, 0.04, 0.38], prop=0.80, acq=0.06),
                 "E": dict(join=150, leave=None, size=0.70, mix=[0.25, 0.26, 0.22, 0.27], prop=1.05, acq=0.10),
                 "F": dict(join=0, leave=248, size=1.30, mix=[0.06, 0.02, 0.88, 0.04], prop=1.15, acq=0.00,
                           premium=dict(share=0.04, prop=2.40))},
        conversions=[dict(to="B", src=None, waves=[117, 118, 119, 120], size=0.24, mix=[0.04, 0.70, 0.06, 0.20],
                          prop=1.25),
                     dict(to="A", src="F", book="premium", waves=[244, 245, 246, 247], frac=1.0)],
        cohort=4000.0, back_years=12, attrition=0.004, tau=40.0, floor=0.80,
        lag0=(0.74, 0.90), lag1=(0.94, 0.985), lag2=(0.992, 0.999), noise=0.06, feed_noise=0.02, rev_noise=0.003)


class World:
    pass


def simulate(seed, **kw):
    P = default_params()
    P.update(kw)
    r = np.random.default_rng(seed)
    w = World()
    w.P, w.seed = P, seed
    t = np.arange(W) / 52.0
    # the category: a weekly log-level that grows at each fiscal year's rate, a slow AR wobble, the season
    weekly = np.array([np.log1p(P["year_growth"][k]) / 52.0 for k in FYI])
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
    # the design event lifts made-to-order orders from the Friday after Thanksgiving to the end of January
    ev_on = event_weeks(list(CAL.week_start))
    ev = np.where(ev_on, 1.0 + np.array(P["mto_event"])[FYI], 1.0)
    w.event = ev
    studios = [pd.Timestamp(x) for x in P["studios"]]
    n_st = np.array([sum(1 for x in studios if x <= d) for d in CAL.week_start])
    w.n_studios = n_st
    mto = P["mto0"] + P["mto_studio"] * n_st
    w.mto_base = mto
    lift = (1 - mto) + mto * ev                           # store and site orders with the event's made-to-order lift
    w.mto_share = mto * ev / lift                         # made-to-order share of store and site orders, by week
    msales = np.zeros((W, 4, len(MERCHANTS)))             # what each merchant id sells to everyone, USD m a week
    msales[:, :, 0] = reg_sales * (1 - web[:, None]) * (1 - outlet) * lift[:, None]
    msales[:, :, 1] = reg_sales * (1 - web[:, None]) * outlet
    msales[:, :, 2] = reg_sales * web[:, None] * lift[:, None]
    msales[:, :, 3] = fern[:, None] * share_r
    msales[:, :, 4] = lic[:, None] * share_r
    msales[:, :, 5] = cafe[:, None] * share_r
    w.reg_sales, w.msales, w.web, w.fern, w.lic, w.consolidated = reg_sales, msales, web, fern, lic, consolidated
    # revenue is recognised on delivery: in-stock and outlet orders the week they are placed, made-to-order orders the
    # lead time later; customers pay in full at order, so undelivered orders are customer deposits
    pre = 60
    pre_dates = [FY_START - pd.Timedelta(days=7 * k) for k in range(pre, 0, -1)]
    pre_level = level[0] * np.exp(-np.log1p(P["year_growth"][0]) / 52.0 * np.arange(pre, 0, -1))
    pre_season = np.array([season_of(d) for d in pre_dates])
    pre_ev = np.where(event_weeks(pre_dates), 1.0 + 0.06, 1.0)
    pre_mto = P["mto0"] + P["mto_studio"] * np.array([sum(1 for x in studios if x <= d) for d in pre_dates])
    mto_r = np.zeros((pre + W, 4))
    for j, reg in enumerate(REGIONS):
        pre_reg = P["base"][reg] * np.exp(P["growth"][reg] * (np.arange(-pre, 0) / 52.0)) * pre_level * pre_season
        mto_r[:pre, j] = pre_mto * pre_ev * pre_reg * ((1 - web[0]) * (1 - outlet) + web[0])
    mto_r[pre:] = w.mto_share[:, None] * (msales[:, :, 0] + msales[:, :, 2])
    dlv = np.zeros((pre + W + 40, 4))
    L = P["lead"]
    for n in range(pre + W):
        d = n + L
        lo = int(np.floor(d))
        fr = d - lo
        dlv[lo] += mto_r[n] * (1 - fr)
        dlv[lo + 1] += mto_r[n] * fr
    instock = (1 - w.mto_share[:, None]) * (msales[:, :, 0] + msales[:, :, 2]) + msales[:, :, 1]
    banner = instock + dlv[pre:pre + W]
    dep_all = np.cumsum(mto_r.sum(1)) - np.cumsum(dlv.sum(1))[:pre + W]
    dep = dep_all[pre:]
    w.dep_pre = dep_all[:pre]                             # deposits at the end of each of the 60 weeks before FY2021
    w.mto_orders = mto_r[pre:]
    w.orders_w = msales[:, :, :3].sum((1, 2)) + np.where(consolidated, fern, 0.0)
    w.deposits_w = dep
    rev_w = banner.sum(1) + np.where(consolidated, fern, 0.0)
    w.rev_w = rev_w
    nq = len(QKEYS)
    rev_q = np.array([rev_w[QIDX == q].sum() for q in range(nq)]) * np.exp(r.normal(0, P["rev_noise"], nq))
    rc = np.random.default_rng(seed + 991)
    ct = np.array([P["ct_base"] + P["ct_trend"] * q + rc.normal(0, P["ct_noise"]) + P["ct_lumps"].get(k, 0.0)
                   for q, k in enumerate(QKEYS)])
    w.contract_q = ct
    w.retail_q = rev_q
    w.rev_q = rev_q + ct
    w.fern_q = np.array([fern[(QIDX == q) & consolidated].sum() for q in range(nq)])
    w.rev_q_region = np.array([banner[QIDX == q].sum(0) for q in range(nq)])
    w.dep_q = np.array([dep[np.where(QIDX == q)[0][-1]] for q in range(nq)])
    w.dep_open = float(np.cumsum(mto_r.sum(1))[pre - 1] - np.cumsum(dlv.sum(1))[pre - 1])
    w.bank = np.full(W, P["bank"])
    # the panel's card accounts: four-week batches by issuer and region, with each issuer's back book
    iss = list(P["issuers"])
    w.issuers = iss
    co = []                         # (issuer, region, open week, opened, propensity, mature, transfer id)
    for i, name in enumerate(iss):
        d = P["issuers"][name]
        first = d["join"]
        start = first - 52 * P["back_years"]
        for ow in range(start - start % STEP, (W if d["leave"] is None else d["leave"]), STEP):
            yrs = (ow - first) / 52.0
            for j in range(4):
                n = P["cohort"] * d["size"] * d["mix"][j] * np.exp(d["acq"] * yrs) * np.exp(r.normal(0, 0.06))
                pm = d.get("premium")
                if pm:
                    co.append((i, j, ow, n * pm["share"], pm["prop"], False, "premium"))
                    n = n * (1 - pm["share"])
                co.append((i, j, ow, n, d["prop"], False, None))
    # conversions: an outside book re-issued in waves, or part of another issuer's book moved across in waves
    w.conversions = []
    for k, cv in enumerate(P["conversions"]):
        to = iss.index(cv["to"])
        K = len(cv["waves"])
        if cv["src"] is None:
            for wk in cv["waves"]:
                for j in range(4):
                    n = P["cohort"] * 63.0 * cv["size"] * cv["mix"][j] / K
                    co.append((to, j, wk, n, cv["prop"], True, k))
        w.conversions.append(dict(k=k, to=cv["to"], src=cv["src"], waves=list(cv["waves"])))
    w.co_base = len(co)
    n_co = len(co)
    active = np.zeros((W, n_co))
    settle = np.zeros((W, n_co))
    for c, (i, j, ow, n0, prop, mature, tid) in enumerate(co):
        d = P["issuers"][iss[i]]
        lo, hi = max(d["join"], ow, 0), (W if d["leave"] is None else d["leave"])
        if lo >= hi:
            continue
        wk = np.arange(lo, hi)
        ten = wk - ow
        active[lo:hi, c] = n0 * np.exp(-P["attrition"] * ten)
        settle[lo:hi, c] = P["floor"] if mature else P["floor"] + (1 - P["floor"]) * np.exp(-ten / P["tau"])
    # a book moved between issuers: each wave takes an equal part of the source's accounts by region; the moved
    # accounts keep their spending (the source's propensity, settled) and are re-issued under the new issuer's codes
    extra = []
    for k, cv in enumerate(P["conversions"]):
        if cv["src"] is None:
            continue
        src, to = iss.index(cv["src"]), iss.index(cv["to"])
        K = len(cv["waves"])
        cols = [c for c, x in enumerate(co) if x[0] == src and (cv.get("book") is None or x[6] == cv["book"])]
        for m, wk in enumerate(cv["waves"]):
            keep_prev = 1 - cv["frac"] * m / K
            keep_now = 1 - cv["frac"] * (m + 1) / K
            for j in range(4):
                cj = [c for c in cols if co[c][1] == j]
                moved = active[wk, cj].sum() * (1 - keep_now / keep_prev)
                prop = P["issuers"][cv["src"]][cv["book"]]["prop"] if cv.get("book") else P["issuers"][cv["src"]]["prop"]
                extra.append((to, j, wk, moved, prop, True, k))
            active[wk:, cols] *= keep_now / keep_prev
    if extra:
        a2 = np.zeros((W, len(extra)))
        s2 = np.zeros((W, len(extra)))
        for c, (i, j, ow, n0, prop, mature, tid) in enumerate(extra):
            d = P["issuers"][iss[i]]
            hi = W if d["leave"] is None else d["leave"]
            wk = np.arange(ow, hi)
            a2[ow:hi, c] = n0 * np.exp(-P["attrition"] * (wk - ow))
            s2[ow:hi, c] = P["floor"]
        co = co + extra
        active = np.hstack([active, a2])
        settle = np.hstack([settle, s2])
        n_co = len(co)
    w.co = co
    w.active, w.settle = active, settle
    w.prop = np.array([x[4] for x in co])
    # spend per card per week at each merchant: the region's bank-card spend there, per reference card, by propensity
    ref_cards = 4.0e6
    pi = msales * w.bank[:, None, None] / ref_cards * 1e6            # USD per reference card per week
    w.pi = pi
    reg_of = np.array([x[1] for x in co])
    iss_of = np.array([x[0] for x in co])
    feed = np.exp(r.normal(0, P["feed_noise"], (W, len(iss))))      # each issuer's weekly feed wobble
    noise = np.exp(r.normal(0, P["noise"], (W, n_co, len(MERCHANTS))))
    spend = (active * settle * w.prop[None, :] * feed[:, iss_of])[:, :, None] * pi[:, reg_of, :] * noise   # USD
    w.spend = spend
    txn_size = np.array([310.0, 140.0, 260.0, 120.0, 95.0, 14.0])
    w.txns = spend / txn_size[None, None, :] * np.exp(r.normal(0, 0.05, spend.shape))      # expected counts
    # posting completeness by issuer in the latest deliveries (lag 0 is the week just ended)
    w.lag0 = r.uniform(*P["lag0"], len(iss))
    w.lag1 = r.uniform(*P["lag1"], len(iss))
    w.lag2 = r.uniform(*P["lag2"], len(iss))
    deliveries = [CAL.week_start.iloc[-1] + pd.Timedelta(days=8) - pd.Timedelta(days=7 * k) for k in range(26, -1, -1)]
    w.deliveries = deliveries
    comp = {}
    for d in deliveries:
        last = week_of(d - pd.Timedelta(days=8))
        for i in range(len(iss)):
            for lag, rng_ in ((0, w.lag0), (1, w.lag1), (2, w.lag2)):
                comp[(d, i, last - lag)] = float(np.clip(rng_[i] + r.normal(0, 0.012 if lag == 0 else 0.004), 0.5, 1.0))
    w.comp = comp
    w.last_week = W - 1
    w.studios = [pd.Timestamp(s) for s in P["studios"]]
    return w
