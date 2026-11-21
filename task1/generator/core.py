#!/usr/bin/env python3
"""task1, the core: Zancada's paid channels for 2027, proved on arrays before any pack exists.

The world's observation process, the truth, the golden estimator, every shortcut route, the variant battery, the
referee slices and the graded figures, ending on corelib.run(spec). Standard library and numpy only; nothing here
reads a prompt or solves a task. The generator imports the process from this file, so the pack carries what the core
proved.

    python3 task1/generator/core.py            # the core table and CORE PASS / CORE FAIL
    python3 task1/generator/core.py --explore  # the dials' diagnostics, while designing
"""
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", ".claude", "skills", "stumping"))

SEED = 71126                     # the people
BUDGET_SEED = 71116              # the team's weekly budgets and the weeks' auctions
WEEKS = 104                      # installs 4 November 2024 to 1 November 2026
MATURE = 52                      # install weeks with twelve months on file
END_DAY = WEEKS * 7 + 6          # the pull, 8 November 2026
MONTH_DAYS = 30.4375
K = 26                           # monthly charges a subscription can take inside the record
COUNTRY_SHARE = (0.60, 0.25, 0.15)          # ES, IT, PT
VAT = (0.21, 0.22, 0.23)
COMMISSION = 0.15                # the stores'
WEB_FEE = 0.03                   # the card processor's, on the web checkout
PRICE_M, PRICE_A = 9.99, 59.99
LINES = (0.90, 1.20)             # the growth policy: cut under 0.90, hold from 0.90, scale from 1.20
WEB_SHARE = 0.15                 # subscribers who pay on the web checkout (the backend takes every charge itself)
EXP_DROP = 0.75                  # wider inventory's users are this much less engaged
lg = lambda x: 1.0 / (1.0 + np.exp(-x))

# the people: e is how much a person uses the app in the first days; u is how reachable they let an app be
# (notifications on, tracking allowed), mildly related to e; f is how readily they stop opening an app they still pay
# for, which differs by where the ad found them
RHO = 0.30
CONSENT = dict(ios=-1.02, android=0.15, u=0.30, e=0.10)        # the tracking prompt's answer
CONV = dict(a=-1.15, e=1.00, u=0.55)                           # trial to paid at day 7
DORMANT0 = dict(a=-3.00, e=0.45, u=0.60)                       # the chance of never opening again after the trial week
DORMANT = dict(a=-2.10, e=0.45, u=0.60, f=1.00)                # the monthly chance of never opening again, later
CHURN = dict(a=-2.00, e=0.45, u=0.60)                          # the monthly chance of cancelling while still opening
CHURN_SILENT = dict(a=-3.45, e=-0.10)                          # and once the app is no longer opened: a store
#                                                                subscription nobody looks at is rarely cancelled
CHURN_SILENT_WEB = dict(a=-1.80, e=-0.10)                      # the web checkout emails a receipt for every charge
# an ad network finds its buyers with the signal it gets back from the people it reached. A person who declines the
# tracking prompt sends none, so a network's installs that declined are the ones it bought blind: the same first two
# days, and a weaker subscriber after them. How much weaker depends on how far the network's delivery leans on that
# signal (a search or intent network hardly at all, a feed network a great deal); organic installs were bought by
# nobody. The figure is the shift, on the logit scale, in converting at the trial's end and in cancelling each month.
GAP = {"Meta iOS": 1.05, "TikTok iOS": 0.80, "Snapchat iOS": 0.52, "Google iOS": 0.03, "Pinterest iOS": 0.28,
       "Apple Search Ads": 0.0, "Google Android": 0.18, "AppLovin Android": 0.50}
MARKETS = ("ES", "IT", "PT")
# the ad platforms' delivery: a campaign spends its weekly budget only as far as the week's auction lets it
KAPPA, LAMBDA, SIG_M, RHO_M, DBAR = 0.55, 1.00, 0.26, 0.25, 0.86

# channel: platform; complete (the channel is on file for every account, whatever the tracking answer); the people
# it brings (mean engagement, reachability, readiness to go quiet); installs a week at the reference weekly budget b0;
# the budget elasticity of installs; how fast a larger budget reaches into wider inventory; the 2027 plan's weekly
# spend over the norm; the team's budget moves (first week, weeks, factor)
SCALE = 2.0
CH = {
    "Meta iOS":         dict(ios=1, complete=0, mu=0.05,  nu=0.10, phi=-0.47, n=330, b0=2080, el=0.78, xs=0.35, plan=1.20, stretch=1.30),
    "TikTok iOS":       dict(ios=1, complete=0, mu=-0.30, nu=0.05, phi=0.60,  n=300, b0=2970, el=0.80, xs=0.35, plan=1.30, stretch=1.15),
    "Snapchat iOS":     dict(ios=1, complete=0, mu=-0.15, nu=0.08, phi=0.40,  n=250, b0=2780, el=0.76, xs=0.35, plan=1.30, stretch=1.15),
    "Google iOS":       dict(ios=1, complete=0, mu=0.10,  nu=0.10, phi=-1.30, n=260, b0=1900, el=0.70, xs=0.30, plan=1.25, stretch=1.35),
    "Pinterest iOS":    dict(ios=1, complete=0, mu=0.15,  nu=0.12, phi=-1.20, n=200, b0=1650, el=0.74, xs=0.30, plan=0.75, stretch=1.75),
    "Apple Search Ads": dict(ios=1, complete=1, mu=0.60,  nu=0.15, phi=-0.80, n=140, b0=1390, el=0.62, xs=0.30, plan=1.40, stretch=1.00),
    "Google Android":   dict(ios=0, complete=1, mu=0.00,  nu=0.10, phi=0.30,  n=420, b0=5390, el=0.66, xs=0.30, plan=0.60, stretch=1.25),
    "AppLovin Android": dict(ios=0, complete=1, mu=-0.55, nu=0.05, phi=1.10,  n=500, b0=3180, el=0.82, xs=0.30, plan=0.88, stretch=1.45),
}
ORGANIC = {"organic iOS": dict(ios=1, mu=0.25, nu=0.12, phi=-0.20, n=380),
           "organic Android": dict(ios=0, mu=0.10, nu=0.12, phi=-0.80, n=700)}
ORDER = list(CH)


def budget_moves(i):
    """the growth team's budget moves on one channel: (first week, weeks, factor on the norm)"""
    r = np.random.default_rng(9000 + i)
    out, w = [], 3 + int(r.integers(0, 5))
    while w < WEEKS - 5:
        k = int(r.integers(3, 6))
        out.append((w, k, float(r.choice([0.6, 0.65, 0.7, 0.75, 1.35, 1.4, 1.5, 1.6]))))
        w += k + int(r.integers(5, 10))
    return out


ALWAYS_ON = ("Meta iOS", "Google iOS", "Google Android", "AppLovin Android")
CAL_SEED = 7360


def market_calendar(i):
    """the weeks a paid channel's campaigns were live in each market (ES, IT, PT). The team runs each network market
    by market in flights: the four large accounts stay on in Spain for ten weeks or so between pauses of about four,
    the three small ones run shorter bursts there, and Italy and Portugal are bought in flights on every network.
    Apple Search Ads runs in every market every week. The channel's weekly budget is one line; it goes where
    campaigns are live."""
    on = np.ones((3, WEEKS), bool)
    if ORDER[i] == "Apple Search Ads":
        return on
    r = np.random.default_rng(CAL_SEED + i)
    spells = ((10, 4) if ORDER[i] in ALWAYS_ON else (7, 5), (8, 7), (6, 8))      # mean weeks live, weeks dark
    for m, (a, b) in enumerate(spells):
        w = 0
        live = bool(r.random() < a / (a + b))
        while w < WEEKS:
            mu = a if live else b
            k = int(r.integers(max(2, int(mu * 0.6)), int(mu * 1.4) + 1))
            on[m, w:w + k] = live
            w += k
            live = not live
    dark = ~on.any(0)
    on[0, dark] = True                                           # never every market dark at once
    return on


for _i, _c in enumerate(ORDER):
    CH[_c]["pushes"] = budget_moves(_i)
    CH[_c]["live"] = market_calendar(_i)
    CH[_c]["tilt"] = np.array(COUNTRY_SHARE) * np.exp(np.random.default_rng(7400 + _i).normal(0, 0.12, 3))
SOURCES = ORDER + list(ORGANIC)
# Apple Search Ads runs on a fixed brand budget outside the growth plan: it is in every record and not in the decision
MEMBERS = [c for c in ORDER if c != "Apple Search Ads"]
GATED = [c for c in ORDER if not CH[c]["complete"]]
SEASON_MU = {1: -0.12, 2: -0.05, 3: 0.0, 4: 0.02, 5: 0.03, 6: 0.0, 7: -0.04, 8: -0.06, 9: 0.05, 10: 0.04, 11: 0.02,
             12: -0.02}
SEASON_N = {1: 1.25, 2: 1.10, 3: 1.02, 4: 1.0, 5: 0.98, 6: 0.92, 7: 0.85, 8: 0.80, 9: 1.08, 10: 1.05, 11: 1.0, 12: 0.92}
SEASON_SPEND = {1: 1.18, 2: 1.05, 3: 1.0, 4: 1.0, 5: 0.98, 6: 0.92, 7: 0.86, 8: 0.82, 9: 1.06, 10: 1.04, 11: 1.0,
                12: 0.95}


def month_of_day(d):
    """calendar month (1 to 12) of day d counted from Monday 4 November 2024"""
    doy = (np.asarray(d) + 307) % 365
    edges = np.array([31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334])
    return np.digitize(doy, edges) + 1


def week_month(w):
    return int(month_of_day(int(w) * 7 + 3))


WMONTH = np.array([week_month(w) for w in range(WEEKS)])
PLAN_MONTH = np.array([int(month_of_day(791 + 7 * t + 3)) for t in range(52)])     # 4 January 2027 is day 791


def plan_spend(c):
    """the 2027 media plan: the channel's planned weekly spend, 52 weeks from Monday 4 January 2027"""
    p = CH[c]
    return np.array([round(p["plan"] * p["b0"] * SCALE * DBAR * SEASON_SPEND[m], -1) for m in PLAN_MONTH])


# --------------------------------------------------------------------------------------------------------------
# the world's process
# --------------------------------------------------------------------------------------------------------------

def market(rng, n):
    m = np.zeros(n)
    s = SIG_M * np.sqrt(1 - RHO_M ** 2)
    x = rng.normal(0, SIG_M)
    for t in range(n):
        x = RHO_M * x + rng.normal(0, s)
        m[t] = x
    return m


def delivery(m):
    return np.clip(DBAR * np.exp(KAPPA * m - 0.5 * (KAPPA * SIG_M) ** 2), 0.45, 1.10)


def budgets(seed=BUDGET_SEED):
    """each channel's weekly budget (the team's), the week's auction, and what the platform went on to spend"""
    out = {}
    for ci, (c, p) in enumerate(CH.items()):
        rng = np.random.default_rng([seed, 1, ci])
        xb = 0.94 + 0.12 * rng.random(WEEKS)
        for w0, k, f in p["pushes"]:
            xb[w0:w0 + k] *= f
        norm = np.array([p["b0"] * SCALE * SEASON_SPEND[m] for m in WMONTH])
        budget = np.round(xb * norm, -1)
        m = market(rng, WEEKS)
        d = delivery(m)
        # the installs follow the budget the team set; the file holds it rounded to ten euros
        out[c] = dict(xb=xb, m=m, d=d, budget=budget, spend=np.round(budget * d, 2))
    return out


def draw_week(rng, p, month, xb=None, m=0.0):
    """the installs of one week: each person's engagement, reachability and readiness to go quiet"""
    if xb is None:
        n = rng.poisson(p["n"] * SCALE * SEASON_N[month])
        wide = np.zeros(n, bool)
    else:
        n = rng.poisson(p["n"] * SCALE * SEASON_N[month] * xb ** p["el"] * np.exp(LAMBDA * m))
        wide = rng.random(n) < np.clip(0.25 + p["xs"] * np.log(xb), 0.02, 0.90)
    z = rng.normal(0, 1, n)
    e = p["mu"] + SEASON_MU[month] + z - EXP_DROP * wide
    u = p["nu"] + RHO * z + np.sqrt(1 - RHO ** 2) * rng.normal(0, 1, n)
    f = p["phi"] + rng.normal(0, 1, n)
    return e, u, f, wide


def life(rng, e, u, f, day, end_day, pen=0.0):
    """each install's first two days, trial, plan, billing route, charges and the app's last open; pen is how much
    weaker a subscriber the install is after its first two days (an install its network bought blind)"""
    n = e.size
    sess = np.clip(np.round(np.exp(0.9 + 0.55 * e + rng.normal(0, 0.35, n))), 0, 40).astype(int)
    trial = rng.random(n) < lg(-0.35 + 1.05 * e + rng.normal(0, 0.4, n))
    paid48 = (~trial) & (rng.random(n) < lg(-3.4 + 1.0 * e))
    conv = np.where(trial, rng.random(n) < lg(CONV["a"] + CONV["e"] * e + CONV["u"] * u - pen), paid48)
    choice = rng.random(n) < lg(-1.1 + 0.5 * e)
    annual = conv & choice
    web = conv & (rng.random(n) < WEB_SHARE)
    bucket = np.digitize(sess, [1, 2, 3, 5, 8, 12, 18])
    cv = bucket + 8 * trial + 16 * paid48                       # the first-48-hour value the app computes (0 to 31)
    conv_day = np.where(trial, day + 7, day + rng.integers(0, 2, n))
    first = rng.random(n) < lg(DORMANT0["a"] - DORMANT0["e"] * e - DORMANT0["u"] * u)
    pd_ = np.clip(lg(DORMANT["a"] - DORMANT["e"] * e - DORMANT["u"] * u + DORMANT["f"] * f), 0.01, 0.99)
    dorm = np.where(first, 0, rng.geometric(pd_))               # months awake after the first charge
    rdays = conv_day[:, None] + np.round(MONTH_DAYS * np.arange(K))[None, :].astype(int)
    charge = np.zeros((n, K), bool)
    active = conv & ~annual
    cancelled_awake = np.zeros(n, bool)
    last_paid = np.full(n, -1)
    for k in range(K):
        charge[:, k] = active & (rdays[:, k] <= end_day)
        last_paid = np.where(charge[:, k], k, last_paid)
        awake = k < dorm
        h = np.where(awake, lg(CHURN["a"] - CHURN["e"] * e - CHURN["u"] * u + pen),
                     np.where(web, lg(CHURN_SILENT_WEB["a"] - CHURN_SILENT_WEB["e"] * e),
                              lg(CHURN_SILENT["a"] - CHURN_SILENT["e"] * e)))
        stop = active & (rng.random(n) < h)
        cancelled_awake |= stop & awake
        active = active & ~stop
    a0 = annual & (conv_day <= end_day)
    lo = day + np.minimum(rng.geometric(0.16, n) - 1, 60)
    sub = conv & ~annual & (last_paid >= 0)
    ar = np.arange(n)
    lp = np.maximum(last_paid, 0)
    still = sub & charge[ar, lp] & (rdays[ar, lp] + 30 > end_day)
    kd = np.minimum(dorm, lp + 1)
    base = np.where(kd >= 1, rdays[ar, np.maximum(kd - 1, 0)], day)
    lo_sub = base + rng.integers(0, 29, n)
    lo_sub = np.where(kd == 0, day + rng.integers(0, 7, n), lo_sub)
    awake_end = sub & (dorm > last_paid) & still
    lo_sub = np.where(awake_end, end_day - rng.integers(0, 7, n), lo_sub)
    ca_lo = rdays[ar, lp] + rng.integers(0, 29, n)
    lo_sub = np.where(sub & cancelled_awake & (dorm > last_paid), ca_lo, lo_sub)
    lo = np.where(sub, lo_sub, lo)
    lo_a = conv_day + np.minimum(dorm, 24) * 30 + rng.integers(0, 29, n)
    lo_a = np.where(dorm == 0, day + rng.integers(0, 7, n), lo_a)
    lo = np.where(annual, lo_a, lo)
    lo = np.minimum(np.maximum(lo, day), end_day)
    auto_on = np.where(sub, ~cancelled_awake, annual & ~(dorm >= 12))
    in_trial = trial & ~conv & (lo < day + 7)
    auto_on = np.where(in_trial, rng.random(n) < 0.55, auto_on)
    plan_seen = np.where(annual, 2, np.where(conv, 1, 0))
    plan_seen = np.where(in_trial, np.where(choice, 2, 1), plan_seen)       # 0 none, 1 monthly, 2 annual
    return dict(e=e, u=u, f=f, day=day, cv=cv, trial=trial, conv=conv, annual=annual, web=web, conv_day=conv_day,
                dorm=dorm, rdays=rdays, charge=charge, a0=a0, last_open=lo, auto_on=auto_on.astype(bool),
                plan_seen=plan_seen)


def consent_of(rng, e, u, ios):
    a = np.where(ios, CONSENT["ios"], CONSENT["android"])
    return rng.random(e.size) < lg(a + CONSENT["u"] * u + CONSENT["e"] * e)


def simulate(seed=SEED, bseed=BUDGET_SEED):
    """every account of the 104 install weeks, flattened; src indexes SOURCES"""
    B = budgets(bseed)
    parts = []
    for si, c in enumerate(SOURCES):
        rng = np.random.default_rng([seed, 2, si])
        p = CH.get(c) or ORGANIC[c]
        es, us, fs, ds, ws, wd = [], [], [], [], [], []
        cs = []
        for w in range(WEEKS):
            if c in CH:
                e, u, f, wide = draw_week(rng, p, WMONTH[w], B[c]["xb"][w], B[c]["m"][w])
                pm = p["tilt"] * p["live"][:, w]
            else:
                e, u, f, wide = draw_week(rng, p, WMONTH[w])
                pm = np.array(COUNTRY_SHARE)
            es.append(e); us.append(u); fs.append(f); wd.append(wide)
            ds.append(w * 7 + rng.integers(0, 7, e.size)); ws.append(np.full(e.size, w))
            cs.append(rng.choice(3, e.size, p=pm / pm.sum()))
        e = np.concatenate(es); u = np.concatenate(us); f = np.concatenate(fs); d = np.concatenate(ds)
        ios = np.full(e.size, bool(p["ios"]))
        consent = consent_of(rng, e, u, ios)
        L = life(rng, e, u, f, d, END_DAY, pen=GAP.get(c, 0.0) * ~consent)
        L["week"] = np.concatenate(ws); L["wide"] = np.concatenate(wd)
        L["src"] = np.full(e.size, si)
        L["country"] = np.concatenate(cs)
        L["ios"] = ios
        L["consent"] = consent
        L["pb_lag"] = rng.integers(3, 5, e.size)                 # days from install to the network's postback
        parts.append(L)
    W = {k: np.concatenate([q[k] for q in parts]) for k in parts[0]}
    W["B"] = B
    return W


def net_m(country, web):
    return PRICE_M / (1 + np.asarray(VAT)[country]) * np.where(web, 1 - WEB_FEE, 1 - COMMISSION)


def net_a(country, web):
    return PRICE_A / (1 + np.asarray(VAT)[country]) * np.where(web, 1 - WEB_FEE, 1 - COMMISSION)


def value12(L, recorded=False):
    """each install's net revenue in its first 365 days: as charged, or as the app's records hold it (a store charge
    reaches the records only at the account's next open; the web checkout's charges all do)"""
    win = L["rdays"] < (L["day"] + 365)[:, None]
    ch = L["charge"] & win
    a0 = L["a0"] & (L["conv_day"] < L["day"] + 365)
    if recorded:
        ch = ch & ((L["rdays"] <= L["last_open"][:, None]) | L["web"][:, None])
        a0 = a0 & ((L["conv_day"] <= L["last_open"]) | L["web"])
    return ch.sum(1) * net_m(L["country"], L["web"]) + a0 * net_a(L["country"], L["web"])


def truth_at_plan(seed=SEED + 777, reps=30):
    """the world's own 2027: each channel's installs bought week by week under the budgets that deliver the plan's
    spend, and their twelve months as charged: the return per euro, installs a week, value per install, and what the
    next euro returns (the return times the sum of the two elasticities, the value's read off the two inventories)"""
    out = {}
    for ci, c in enumerate(ORDER):
        p = CH[c]
        rng = np.random.default_rng(seed + 31 * ci)
        sp = plan_spend(c)
        tv = ts = ni = 0.0
        vs = np.zeros(2); ns = np.zeros(2)
        for _ in range(reps):
            m = market(rng, 52)
            es, us, fs, ds, wd = [], [], [], [], []
            for t in range(52):
                xb = sp[t] / (p["b0"] * SCALE * DBAR * SEASON_SPEND[PLAN_MONTH[t]])
                e, u, f, w = draw_week(rng, p, PLAN_MONTH[t], xb, m[t])
                es.append(e); us.append(u); fs.append(f); wd.append(w)
                ds.append(t * 7 + rng.integers(0, 7, e.size))
                ts += sp[t] * delivery(m[t]) / DBAR
            e = np.concatenate(es); wide = np.concatenate(wd); u = np.concatenate(us)
            consent = consent_of(rng, e, u, np.full(e.size, bool(p["ios"])))
            L = life(rng, e, u, np.concatenate(fs), np.concatenate(ds), 10 ** 6, pen=GAP.get(c, 0.0) * ~consent)
            L["country"] = rng.choice(3, e.size, p=COUNTRY_SHARE)
            v = value12(L)
            tv += v.sum(); ni += e.size
            vs += [v[~wide].sum(), v[wide].sum()]; ns += [(~wide).sum(), wide.sum()]
        vpi = tv / ni
        qs = p["xs"] * (vs[1] / ns[1] - vs[0] / ns[0]) / vpi
        out[c] = dict(roas=tv / ts, installs_week=ni / reps / 52.0, vpi=vpi, revenue=tv / ts * sp.sum(),
                      marginal=tv / ts * (p["el"] + qs), el=p["el"], qs=qs)
    return out


# --------------------------------------------------------------------------------------------------------------
# what the files hold
# --------------------------------------------------------------------------------------------------------------

PB_ALIGN = "split"               # how a postback's arrival day is carried back to its install week


class Obs:
    """the pack's content as arrays: nothing below reads a person's traits, the wide flag, the auction's state or an
    unlabelled account's source"""

    def __init__(self, W, align=None):
        align = align or PB_ALIGN
        n = W["e"].size
        self.n = n
        self.week, self.day, self.country, self.ios, self.cv = W["week"], W["day"], W["country"], W["ios"], W["cv"]
        self.market = W["country"]                               # the account's storefront: ES, IT or PT
        self.consent = W["consent"]                              # the prompt's answer is on every account
        complete = np.array([(CH[c]["complete"] if c in CH else 0) for c in SOURCES], bool)[W["src"]]
        organic = W["src"] >= len(ORDER)
        # the channel on file: on iOS the attribution export holds it only for accounts that allowed tracking, and
        # Apple's own attribution gives Apple Search Ads whatever the answer; on Android the Play install referrer
        # gives it for every install. An iOS account with no channel is organic or a network's non-consenting install.
        self.label = np.where(complete | (self.consent & ~organic) | (organic & (self.consent | ~self.ios)), W["src"], -1)
        self.pool = self.label < 0
        self.web = W["web"]
        self.rdays, self.conv_day, self.last_open = W["rdays"], W["conv_day"], W["last_open"]
        seen = (W["rdays"] <= W["last_open"][:, None]) | W["web"][:, None]
        self.true_charge = W["charge"]                           # read only on the web checkout's accounts
        self.rec = W["charge"] & seen                            # monthly charges on file
        self.rec_a0 = W["a0"] & ((W["conv_day"] <= W["last_open"]) | W["web"])
        self.n_rec = self.rec.sum(1)
        self.auto_on, self.plan_seen = W["auto_on"], W["plan_seen"]
        in_trial = W["trial"] & ~W["conv"] & (W["last_open"] < W["day"] + 7)
        silent_first = W["conv"] & W["trial"] & ~W["web"] & (W["last_open"] < W["conv_day"])
        self.trial_seen = in_trial | silent_first                # last seen inside the free trial
        self.netm = net_m(W["country"], W["web"]); self.neta = net_a(W["country"], W["web"])
        self.mature = self.week < MATURE
        self.B = W["B"]
        self.mon = (W["rdays"] // MONTH_DAYS).astype(int)
        self.NM = int(END_DAY // MONTH_DAYS) + 1
        # the stores' reports: units by store, kind and month (store charges only)
        store_ch = W["charge"] & ~W["web"][:, None]
        self.store = {}
        for pl in (0, 1):
            mk = self.ios == bool(pl)
            first = np.bincount(self.mon[mk, 0][store_ch[mk, 0]], minlength=self.NM)[:self.NM]
            ren = np.zeros(self.NM)
            for k in range(1, K):
                ren += np.bincount(self.mon[mk, k][store_ch[mk, k]], minlength=self.NM)[:self.NM]
            a = W["a0"] & ~W["web"] & mk
            ann = np.bincount((W["conv_day"][a] // MONTH_DAYS).astype(int), minlength=self.NM)[:self.NM]
            self.store[pl] = dict(first=first.astype(float), ren=ren, ann=ann.astype(float))
        # the records with no account identities: an iOS network's postbacks, one per install with its
        # first-48-hour value and its campaign (a campaign runs in one market), dated three or four days after the
        # install
        self.agg, self.agg_cv, self.agg_cvm = {}, {}, {}
        for ci, c in enumerate(ORDER):
            mk = W["src"] == ci
            if not CH[c]["complete"]:
                pb = W["day"][mk] + W["pb_lag"][mk]                 # the day the postback arrived
                t = np.zeros((WEEKS, 3, 32))
                if align == "true":
                    np.add.at(t, (self.week[mk], W["country"][mk], self.cv[mk]), 1)
                else:                                              # dated back three days, four, or half and half
                    for back, wt in {"three": ((3, 1.0),), "four": ((4, 1.0),), "split": ((3, 0.5), (4, 0.5))}[align]:
                        np.add.at(t, (np.clip((pb - back) // 7, 0, WEEKS - 1), W["country"][mk], self.cv[mk]), wt)
                self.agg_cvm[c] = t
                self.agg_cv[c] = t.sum(1)
                self.agg[c] = t.sum((1, 2))
            else:
                self.agg[c] = np.bincount(self.week[mk], minlength=WEEKS).astype(float)


# --------------------------------------------------------------------------------------------------------------
# S1: the charges the app's records never took in
# --------------------------------------------------------------------------------------------------------------

def s1_candidates(O):
    """subscriptions last seen still set to renew whose next charge fell after the account's last open"""
    ar = np.arange(O.n)
    nxt = O.rdays[ar, np.minimum(O.n_rec, K - 1)]
    ren = (~O.web) & (O.plan_seen == 1) & (O.n_rec >= 1) & O.auto_on & (O.last_open < nxt) & (nxt <= END_DAY) & (O.n_rec < K)
    fst = (~O.web) & O.trial_seen & O.auto_on & (O.n_rec == 0) & ~O.rec_a0 & (O.plan_seen > 0) & (O.day + 7 <= END_DAY)
    return ren, fst


def _monthly_counts(O, mask, which):
    out = np.zeros(O.NM)
    for k in (range(1, K) if which == "ren" else (0,)):
        out += np.bincount(O.mon[mask, k][O.rec[mask, k]], minlength=O.NM)[:O.NM]
    return out


def refine(err, q, step):
    """a least-squares fit in one unknown finished on the real line: a golden-section search one grid step either
    side of the grid's best point"""
    lo, hi = q - step, min(q + step, 0.999)
    g = (5.0 ** 0.5 - 1.0) / 2.0
    a, b = hi - g * (hi - lo), lo + g * (hi - lo)
    fa, fb = err(a), err(b)
    for _ in range(60):
        if fa <= fb:
            hi, b, fb = b, a, fa
            a = hi - g * (hi - lo)
            fa = err(a)
        else:
            lo, a, fa = a, b, fb
            b = lo + g * (hi - lo)
            fb = err(b)
    return 0.5 * (lo + hi)


def s1_fit(O, split="store", trim=0, form="geo", cadence=MONTH_DAYS):
    """the share of trial-end candidates charged and the monthly continuation of a silent subscription, fitted to the
    stores' excess over the records, month by month"""
    ren, fst = s1_candidates(O)
    fits = {}
    for g in (((0,), (1,)) if split == "store" else ((0, 1),)):
        mk = np.isin(O.ios.astype(int), g) & ~O.web
        F = sum(O.store[pl]["first"] for pl in g) - _monthly_counts(O, mk, "first")
        R = sum(O.store[pl]["ren"] for pl in g) - _monthly_counts(O, mk, "ren")
        ra = np.bincount((O.conv_day[mk & O.rec_a0] // MONTH_DAYS).astype(int), minlength=O.NM)[:O.NM]
        A = sum(O.store[pl]["ann"] for pl in g) - ra
        fm = fst & mk & (O.plan_seen == 1)
        fa = fst & mk & (O.plan_seen == 2)
        c_m = F.sum() / max(1, fm.sum())
        c_a = A.sum() / max(1, fa.sum())
        idx = np.where(ren & mk)[0]
        last = O.rdays[idx, O.n_rec[idx] - 1]
        te = O.day[fm] + 7
        Mr = np.zeros((K, O.NM)); Mf = np.zeros((K, O.NM))
        for j in range(1, K):
            d = last + np.round(cadence * j).astype(int)
            d = d[d <= END_DAY]
            Mr[j - 1] = np.bincount((d // MONTH_DAYS).astype(int), minlength=O.NM)[:O.NM]
            d2 = te + np.round(cadence * j).astype(int)
            d2 = d2[d2 <= END_DAY]
            Mf[j - 1] = np.bincount((d2 // MONTH_DAYS).astype(int), minlength=O.NM)[:O.NM]
        use = np.arange(O.NM) < O.NM - 1 - trim
        best = None
        q1s = np.linspace(0.50, 0.99, 50) if form == "two" else (None,)
        for q in np.linspace(0.60, 0.99, 196):
            for q1 in q1s:
                w = q ** np.arange(1, K + 1) if q1 is None else q1 * q ** np.arange(0, K)
                err = (((w @ Mr + c_m * (w @ Mf)) - R)[use] ** 2).sum()
                if best is None or err < best[0]:
                    best = (err, q, q if q1 is None else q1)
        if form != "two":                                          # the one-rate fit, finished on the real line
            pw = np.arange(1, K + 1)
            q = refine(lambda x: float((((x ** pw) @ Mr + c_m * ((x ** pw) @ Mf) - R)[use] ** 2).sum()), best[1], 0.002)
            best = (None, q, q)
        for pl in g:
            fits[pl] = dict(c_m=c_m, c_a=c_a, q=best[1], q1=best[2])
    return fits


def _web_silent(O, mask=None):
    """the web checkout's monthly subscribers as if their charges after the last open were unseen: for each, the
    charges recorded up to the last open, and the charges that followed it (which the backend holds)"""
    w = O.web & (O.plan_seen == 1) & O.true_charge[:, 0] & O.auto_on
    if mask is not None:
        w = w & mask
    idx = np.where(w)[0]
    seen = O.rdays[idx] <= O.last_open[idx][:, None]
    n_open = (O.true_charge[idx] & seen).sum(1)
    return idx, n_open


def s1_web_fit(O):
    """the monthly continuation of a subscription after its last open, read where every charge is on file"""
    idx, n_open = _web_silent(O)
    num = den = 0.0
    for j in range(1, 13):
        k = n_open - 1 + j
        ok = (n_open >= 1) & (k < K)
        kk = np.minimum(k, K - 1)
        due = ok & (O.rdays[idx, kk] <= END_DAY) & (O.rdays[idx, kk] > O.last_open[idx])
        prev = O.true_charge[idx, np.maximum(kk - 1, 0)]
        at = due & prev
        num += (O.true_charge[idx, kk] & at).sum(); den += at.sum()
    return num / max(1.0, den)


def s1_seen_rate(O, pl):
    """one store's monthly continuation as the records show it: one less the subscriptions last seen cancelled per
    monthly charge on file"""
    mk = (O.ios == bool(pl)) & ~O.web & (O.plan_seen == 1) & (O.n_rec >= 1)
    return float(1.0 - (mk & ~O.auto_on).sum() / max(1.0, O.rec[mk].sum()))


def s1_trial_rel(O, pl):
    """among one store's trial starters whose outcome the records hold (a first charge on file, or seen after the
    trial's end or cancelled with none), the share that bought, by four levels of first-48-hour use, over the share
    across them"""
    lvl = np.minimum((O.cv & 7) // 2, 3)
    mk = (O.ios == bool(pl)) & ~O.web & (((O.cv >> 3) & 1) == 1)
    bought = mk & (O.rec[:, 0] | O.rec_a0)
    known = bought | (mk & ~bought & ((O.last_open >= O.day + 7) | ~O.auto_on))
    rate = np.array([bought[known & (lvl == k)].sum() / max(1, (known & (lvl == k)).sum()) for k in range(4)])
    return rate / max(1e-9, bought[known].sum() / max(1, known.sum()))


def s1_values(O, how="golden", split="store", trim=0, form="geo", cadence=MONTH_DAYS, fits=None, cshare="level"):
    """(each account's twelve-month net revenue, its chance of having bought) as recorded, trued up to the stores in
    proportion, or with the silent charges put on the subscriptions that were set to take them"""
    win = O.rdays < (O.day + 365)[:, None]
    rec_m = (O.rec & win).sum(1) * O.netm
    rec_a = (O.rec_a0 & (O.conv_day < O.day + 365)) * O.neta
    rec = rec_m + rec_a
    bought = (O.rec[:, 0] | O.rec_a0).astype(float)
    if how == "raw":
        return rec, bought
    if how in ("prop", "prop_month"):
        out = rec.copy(); b = bought.copy()
        for pl in (0, 1):
            mk = (O.ios == bool(pl)) & ~O.web
            if how == "prop":
                f = (O.store[pl]["first"].sum() + O.store[pl]["ren"].sum()) / O.rec[mk].sum()
                fa = O.store[pl]["ann"].sum() / max(1, O.rec_a0[mk].sum())
                out[mk] = rec_m[mk] * f + rec_a[mk] * fa
            else:
                st = O.store[pl]["first"] + O.store[pl]["ren"]
                rc = _monthly_counts(O, mk, "first") + _monthly_counts(O, mk, "ren")
                f = np.where(rc > 0, st / np.maximum(rc, 1), 1.0)
                fm = f[np.minimum(O.mon[mk], O.NM - 1)]
                out[mk] = ((O.rec[mk] & win[mk]) * fm).sum(1) * O.netm[mk]
                ra = np.bincount((O.conv_day[mk & O.rec_a0] // MONTH_DAYS).astype(int), minlength=O.NM)[:O.NM]
                fa = np.where(ra > 0, O.store[pl]["ann"] / np.maximum(ra, 1), 1.0)
                out[mk] += rec_a[mk] * fa[np.minimum((O.conv_day[mk] // MONTH_DAYS).astype(int), O.NM - 1)]
            fb = (O.store[pl]["first"].sum() + O.store[pl]["ann"].sum()) / max(1.0, bought[mk].sum())
            b[mk] = bought[mk] * fb
        return out, b
    fits = fits or s1_fit(O, split=split, trim=trim, form=form, cadence=cadence)
    if how == "awake":                                             # the cancellations the app saw, per charge on file
        fits = {pl: dict(f, q=s1_seen_rate(O, pl), q1=s1_seen_rate(O, pl)) for pl, f in fits.items()}
    ren, fst = s1_candidates(O)
    add = np.zeros(O.n)
    wend = O.day + 365
    for pl in (0, 1):
        f = fits[pl]
        wt = (lambda j, f=f: f["q"] ** j) if form == "geo" else (lambda j, f=f: f["q1"] * f["q"] ** (j - 1))
        idx = np.where(ren & (O.ios == bool(pl)))[0]
        last = O.rdays[idx, O.n_rec[idx] - 1]
        for j in range(1, K):
            d = last + np.round(cadence * j).astype(int)
            add[idx] += wt(j) * O.netm[idx] * ((d < wend[idx]) & (d <= END_DAY))
        fi = np.where(fst & (O.ios == bool(pl)))[0]
        te = O.day[fi] + 7
        mon = O.plan_seen[fi] == 1
        # the share charged at the trial's end: the store's excess of first charges spread over the candidates, evenly
        # or in proportion to how trial starters of the same first two days went on to buy
        rel = np.ones(fi.size)
        if cshare == "level":
            rel = s1_trial_rel(O, pl)[np.minimum((O.cv[fi] & 7) // 2, 3)]
            for sel in (mon, ~mon):
                if sel.any():
                    rel[sel] = rel[sel] / rel[sel].mean()
        cm, ca = f["c_m"] * rel, f["c_a"] * rel
        add[fi] += np.where(mon, cm * O.netm[fi], ca * O.neta[fi])
        bought[fi] += np.where(mon, cm, ca)
        for j in range(1, K):
            d = te + np.round(cadence * j).astype(int)
            add[fi] += mon * cm * wt(j) * O.netm[fi] * ((d < wend[fi]) & (d <= END_DAY))
    return rec + add, bought


# --------------------------------------------------------------------------------------------------------------
# S2: the installs the attribution export does not name
# --------------------------------------------------------------------------------------------------------------

LEVELS = {"one": 1, "tier2": 2, "tier4": 4, "tier8": 8}
CELL_ROWS = {"market-week-pair": 2, "market-week-bucket": 1}     # sessions values to a row of the fit
FITKEYS = ("rows", "weight", "markets", "org_pin", "span", "minpool", "group", "shrink", "r_nudge")
GROUPS = {"kind": (("Meta iOS", "TikTok iOS", "Snapchat iOS", "Pinterest iOS"),),      # the social networks as one
          "social": (("Meta iOS", "TikTok iOS", "Snapchat iOS"),),
          # the groupings a five per cent test of equal ratios lets through under one reading of the fit's spread or
          # the other (s2_equal_test with the row-by-row spread, and with one variance for every row)
          "pair": (("Meta iOS", "TikTok iOS"),),
          "pair2": (("TikTok iOS", "Snapchat iOS"),),
          "gp": (("Google iOS", "Pinterest iOS"),),
          "gpo": (("Google iOS", "Pinterest iOS", "organic iOS"),),
          "po": (("Pinterest iOS", "organic iOS"),),
          "go": (("Google iOS", "organic iOS"),)}


def groups_of(group):
    """the sets of sources that share one ratio under a grouping; two groupings taken at once are joined by a plus"""
    return tuple(g for key in group.split("+") for g in GROUPS[key])


def tier(cv, levels=4):
    cv = np.asarray(cv)
    trial, paid, bucket = (cv >> 3) & 1, (cv >> 4) & 1, cv & 7
    if levels == 1:
        return np.zeros(cv.shape, int)
    if levels == 2:
        return ((trial == 1) | (paid == 1)).astype(int)
    if levels == 4:
        return np.where(paid == 1, 3, np.where(trial == 1, np.where(bucket >= 4, 3, 2), np.where(bucket >= 3, 1, 0)))
    return np.minimum(bucket // 2, 3) + 4 * ((trial == 1) | (paid == 1))


# groupings that keep one part of the first-48-hour value and drop the rest: the sessions bits alone (their eight
# values or four pairs), the trial and purchase bits alone, and those two bits with the sessions split in two
ALONE = {"sess8": lambda cv: cv & 7, "sess4": lambda cv: (cv & 7) // 2, "tp4": lambda cv: (cv >> 3) & 3,
         "tp8": lambda cv: 2 * ((cv >> 3) & 3) + ((cv & 7) >= 4)}


def _cells(cv, cells):
    if cells in ALONE:
        return ALONE[cells](np.asarray(cv))
    return np.asarray(cv) if cells == "fine" else tier(cv, LEVELS[cells])


_S2 = {}


def platform_sources(ios):
    """(a platform's paid channels, its organic source), as indices into SOURCES"""
    return [i for i, c in enumerate(ORDER) if bool(CH[c]["ios"]) == bool(ios)], len(ORDER) + (0 if ios else 1)


def s2_cells(O, v, cells="fine", minn=20, tilt="cell", ios=True):
    """one platform's installs of the mature weeks that allowed tracking, by first-48-hour cell: how many each source
    had and what they were worth (a thin cell takes the platform's value for the cell at the source's own level)"""
    k = (id(O), id(v), cells, minn, tilt, ios, "cells")
    if k in _S2:
        return _S2[k][0]
    key = _cells(O.cv, cells)
    key32 = _cells(np.arange(32), cells)
    nk = int(key32.max()) + 1
    paid, org = platform_sources(ios)
    mat = O.mature & (O.ios == bool(ios)) & O.consent
    cons = mat & np.isin(O.label, [i for i in paid if ORDER[i] != "Apple Search Ads"] + [org])
    ref_n = np.bincount(key[cons], minlength=nk)
    ref_v = np.bincount(key[cons], weights=v[cons], minlength=nk)
    ref = np.where(ref_n >= minn, ref_v / np.maximum(ref_n, 1), v[cons].mean())
    T = dict(key=key, key32=key32, nk=nk, n={}, vc={})
    for si in paid + [org]:
        lab = mat & (O.label == si)
        n = np.bincount(key[lab], minlength=nk).astype(float)
        tot = np.bincount(key[lab], weights=v[lab], minlength=nk)
        tl = tot.sum() / max((n * ref).sum(), 1e-9)              # the source's level over the platform's
        own = (n >= minn) if tilt == "cell" else np.zeros(nk, bool)
        T["n"][si], T["vc"][si] = n, np.where(own, tot / np.maximum(n, 1), ref * tl)
    _S2[k] = (T, v)
    return T


def s2_strata(O, v, cells="fine", minn=20, tilt="cell", ios=True):
    """market by market and week by week over the mature weeks, by first-48-hour cell: the accounts that declined the
    prompt (on iOS they carry no channel; on Android every account carries one, and it is set aside here), what they
    paid, and each source's declined installs among them (an iOS network's postbacks less its installs that allowed
    tracking; the organic ones are the accounts left over)"""
    k = (id(O), id(v), cells, minn, tilt, ios, "strata")
    if k in _S2:
        return _S2[k][0]
    T = s2_cells(O, v, cells, minn, tilt, ios)
    paid, org = platform_sources(ios)
    key, nk, key32 = T["key"], T["nk"], T["key32"]
    mat = O.mature & (O.ios == bool(ios))
    pool = mat & (O.pool if ios else ~O.consent)
    hidden = [i for i in paid if not (ios and CH[ORDER[i]]["complete"])]
    shape = (3, MATURE, nk)
    pn = np.zeros(shape); pv = np.zeros(shape)
    np.add.at(pn, (O.market[pool], O.week[pool], key[pool]), 1)
    np.add.at(pv, (O.market[pool], O.week[pool], key[pool]), v[pool])
    nc = {}
    rest = pn.copy()
    for i in hidden:
        x = np.zeros(shape)
        if ios:
            A = O.agg_cvm[ORDER[i]][:MATURE]                      # week, market, first-48-hour value
            for cvv in range(32):
                x[:, :, key32[cvv]] += A[:, :, cvv].T
            lab = mat & (O.label == i)
            np.subtract.at(x, (O.market[lab], O.week[lab], key[lab]), 1)
        else:
            lab = mat & (O.label == i) & ~O.consent
            np.add.at(x, (O.market[lab], O.week[lab], key[lab]), 1)
        nc[i] = x
        rest -= x
    nc[org] = rest
    S = dict(T=T, pn=pn, pv=pv, nc=nc, hidden=hidden, org=org, pool=pool)
    _S2[k] = (S, v)
    return S


def s2_fit(O, v, cells="fine", minn=20, tilt="cell", ios=True, rows="market-week", weight="n", markets=(0, 1, 2),
           org_pin=None, span=1, minpool=0, common=False, group=None, shrink=False, cov=False, r_nudge=None):
    """what a declined install is worth over an install of the same source and the same first-48-hour value that
    allowed tracking, source by source: the declined installs of every source priced at their source's named value,
    and one ratio per source fitted so that, market by market and week by week, they add up to what the accounts
    that declined paid. rows="market-week-tier" fits the ratios separately for the trial starters of lighter and of
    heavier first-48-hour use and returns, for each source, a ratio per pricing cell."""
    k = (id(O), id(v), cells, minn, tilt, ios, rows, weight, tuple(markets), org_pin, span, minpool, common, group,
         shrink, cov, r_nudge)
    if k in _S2:
        return _S2[k][0]
    S = s2_strata(O, v, cells, minn, tilt, ios)
    T = S["T"]
    srcs = S["hidden"] + [S["org"]]
    gid = list(range(len(srcs)))                                   # sources that share one ratio share a column
    if group:
        names = [SOURCES[i] for i in srcs]
        for g in groups_of(group):
            idx = [names.index(nm) for nm in g if nm in names]
            for j in idx[1:]:
                gid[j] = gid[idx[0]]
    ucols = sorted(set(gid))
    nk = T["nk"]
    wg = np.arange(MATURE) // span
    nw = int(wg.max()) + 1
    Xc = [S["nc"][i] * T["vc"][i][None, None, :] for i in srcs]
    # a finer grain for the fit's rows: each market-week split by the first-48-hour sessions the accounts carry (the
    # eight sessions values, or their four pairs), every install still priced on the pricing cells
    per = CELL_ROWS.get(rows)
    if per:
        F = s2_strata(O, v, "fine", minn, tilt, ios)
        sg = (np.arange(32) & 7) // per
        ng = int(sg.max()) + 1
        Xf = [F["nc"][i] * T["vc"][i][T["key32"]][None, None, :] for i in srcs]

    def rows_of(out):
        return (out.sum(0) if markets == "pooled" else out[list(markets)]).reshape(-1)

    def fold(a, sel):
        out = np.zeros((3, nw))
        for kk in np.where(sel)[0]:
            np.add.at(out, (slice(None), wg), a[:, :, kk])
        return rows_of(out)

    def fold_cells(a):
        out = np.zeros((3, nw, ng))
        for cvv in range(32):
            np.add.at(out, (slice(None), wg, sg[cvv]), a[:, :, cvv])
        return rows_of(out)

    def fit(sel):
        if per:                                                    # a row is a market-week's accounts of one sessions cell
            y, n = fold_cells(F["pv"]), fold_cells(F["pn"])
            X = np.stack([fold_cells(x) for x in Xf], axis=1)
            whole = np.repeat(fold(S["pn"], np.ones(nk, bool)), ng)    # the market-week's accounts, for minpool
            keep = (n > 0) & (whole > minpool)
        else:
            y, n = fold(S["pv"], sel), fold(S["pn"], sel)
            X = np.stack([fold(x, sel) for x in Xc], axis=1)
            keep = n > minpool
        w = 1.0 / np.maximum(n, 1.0) if weight in ("n", "fitted") else np.ones(n.size)
        y, X, w = y[keep], X[keep], w[keep]
        if common == "paid":                                       # organic at the pinned ratio, one for the networks
            r = float((y - org_pin * X[:, -1]).sum() / X[:, :-1].sum())
            return [r] * (len(srcs) - 1) + [float(org_pin)]
        if common:                                                 # one ratio for every source
            return [float(y.sum() / X.sum())] * len(srcs)
        Xg = np.stack([X[:, [j for j in range(len(srcs)) if gid[j] == u]].sum(1) for u in ucols], axis=1)
        cols = list(range(len(ucols)))
        yy = y.copy()
        if org_pin is not None:
            yy = yy - org_pin * Xg[:, -1]
            cols = cols[:-1]
        sw = np.sqrt(w)
        beta = np.linalg.lstsq(Xg[:, cols] * sw[:, None], yy * sw, rcond=None)[0]
        if weight == "fitted":                                     # once more, weighted by the revenue the fit expects
            w2 = 1.0 / np.maximum(Xg[:, cols] @ beta, np.percentile(np.abs(yy), 10) + 1.0)
            sw = np.sqrt(w2)
            beta = np.linalg.lstsq(Xg[:, cols] * sw[:, None], yy * sw, rcond=None)[0]
        Xw = Xg[:, cols] * sw[:, None]
        res = yy * sw - Xw @ beta
        bread = np.linalg.inv(Xw.T @ Xw)
        V = bread @ ((Xw * res[:, None]).T @ (Xw * res[:, None])) @ bread     # the fit's own spread, row by row
        if cov == "classical":                                     # or with one variance for every row
            V = bread * float(res @ res) / (len(res) - len(cols))
        if shrink:                                                 # the networks' ratios drawn toward their pooled one
            nn = len(cols) - (0 if org_pin is not None else 1)
            b, se2 = beta[:nn], np.diag(V)[:nn]
            m = float((b / se2).sum() / (1.0 / se2).sum())
            tau2 = max(0.0, float(((b - m) ** 2).sum() / (nn - 1) - se2.mean()))
            beta = beta.copy()
            beta[:nn] = m + tau2 / (tau2 + se2) * (b - m)
        bg = [float(x) for x in beta] + ([float(org_pin)] if org_pin is not None else [])
        if cov:
            return bg, V
        return [bg[ucols.index(gid[j])] for j in range(len(srcs))]

    if cov:                                                        # the plain fit's ratios with their covariance
        out = (srcs,) + tuple(fit(np.ones(nk, bool)))
    elif rows == "market-week" or per:
        r = fit(np.ones(nk, bool))
        out = {i: r[j] for j, i in enumerate(srcs)}
    else:
        key32 = T["key32"]
        c32 = np.arange(32)
        heavy32 = (((c32 >> 4) & 1) == 1) | ((((c32 >> 3) & 1) == 1) & ((c32 & 7) >= 4))
        pays32 = (((c32 >> 4) & 1) == 1) | (((c32 >> 3) & 1) == 1)
        heavy = np.array([heavy32[key32 == kk].mean() >= 0.5 if (key32 == kk).any() else False for kk in range(nk)])
        pays = np.array([pays32[key32 == kk].any() if (key32 == kk).any() else False for kk in range(nk)])
        r_hi, r_lo = fit(pays & heavy), fit(pays & ~heavy)
        out = {i: np.where(heavy, r_hi[j], r_lo[j]) for j, i in enumerate(srcs)}
    if r_nudge and not cov:                                        # (a source, a factor): its fitted ratio moved
        out = dict(out)
        out[SOURCES.index(r_nudge[0])] = out[SOURCES.index(r_nudge[0])] * r_nudge[1]
    _S2[k] = (out, v)
    return out


def s2_equal_test(O, v, names, cov=True):
    """whether the named sources could share one ratio: the fitted ratios' differences against the fit's own spread
    (a Wald statistic on len(names) - 1 degrees of freedom) and each ratio with its standard error; cov="classical"
    takes the spread with one variance for every row in place of the row-by-row one"""
    srcs, b, V = s2_fit(O, v, cov=cov)
    b = np.array(b)
    idx = [srcs.index(SOURCES.index(nm)) for nm in names]
    R = np.zeros((len(idx) - 1, len(b)))
    for r, j in enumerate(idx[1:]):
        R[r, idx[0]], R[r, j] = 1.0, -1.0
    d = R @ b
    stat = float(d @ np.linalg.solve(R @ V @ R.T, d))
    return stat, {nm: (float(b[j]), float(np.sqrt(V[j, j]))) for nm, j in zip(names, idx)}


def asa_ratio(O, v, cells="fine", rcells="tier2"):
    """on Apple Search Ads, whose every account carries its channel: the declined installs' value over the others',
    by coarse cell, laid on the pricing cells"""
    lab = (O.label == ORDER.index("Apple Search Ads")) & O.mature
    key = _cells(O.cv, rcells)
    k32, rk = _cells(np.arange(32), cells), _cells(np.arange(32), rcells)
    out = np.full(int(rk.max()) + 1, v[lab & ~O.consent].mean() / v[lab & O.consent].mean())
    for k in range(out.size):
        a, b = lab & (key == k) & ~O.consent, lab & (key == k) & O.consent
        if a.sum() >= 200 and b.sum() >= 200 and v[b].mean() > 0:
            out[k] = v[a].mean() / v[b].mean()
    return np.array([out[int(np.bincount(rk[k32 == k]).argmax())] for k in range(int(k32.max()) + 1)])


def asa_one(O, v):
    """Apple Search Ads' declined installs over its others at the same first-48-hour value, as one number"""
    T = s2_cells(O, v)
    i = ORDER.index("Apple Search Ads")
    lab = (O.label == i) & O.mature & ~O.consent
    cnt = np.bincount(O.cv[lab], minlength=32)
    return float(v[lab].sum() / max((cnt * T["vc"][i]).sum(), 1e-9))


ANALOGUE = {"Meta iOS": "AppLovin Android", "TikTok iOS": "AppLovin Android", "Snapchat iOS": "AppLovin Android",
            "Pinterest iOS": "AppLovin Android", "Google iOS": "Google Android"}


def labelled_one(O, v, c):
    """a channel whose every account carries it (Apple Search Ads, the Android networks): its declined installs'
    value over its others' at the same first-48-hour value, as one number"""
    i = ORDER.index(c)
    T = s2_cells(O, v, ios=bool(CH[c]["ios"]))
    lab = (O.label == i) & O.mature & ~O.consent
    cnt = np.bincount(O.cv[lab], minlength=32)
    return float(v[lab].sum() / max((cnt * T["vc"][i]).sum(), 1e-9))


def _pin(O, v, org_pin):
    return asa_one(O, v) if org_pin == "asa" else org_pin


def ios_price(O, v, c, how="golden", cells="fine", minn=20, tilt="cell", rcells="tier2", **fit):
    """the value of one install of an iOS network by its first-48-hour cell: the installs that allowed tracking at
    their own value, the rest at the value the route gives them; returns (each of the 32 values' cell, the price per
    cell, the installs per cell over the mature weeks)"""
    T = s2_cells(O, v, cells, minn, tilt)
    S = s2_strata(O, v, cells, minn, tilt)
    ci = ORDER.index(c)
    vc, n = T["vc"][ci], T["n"][ci]
    nc = np.maximum(S["nc"][ci].sum((0, 1)), 0)
    if how == "bridge":                                            # every postback at the named installs' value
        vn = vc
    elif how == "flat":                                            # at the unattributed accounts' value, any source
        pn, pv = S["pn"].sum((0, 1)), S["pv"].sum((0, 1))
        vn = np.where(pn >= minn, pv / np.maximum(pn, 1), pv.sum() / pn.sum())
    elif how == "ratio":                                           # at Apple Search Ads' ratio
        vn = vc * asa_ratio(O, v, cells, rcells)
    elif how == "analogue":                                        # at the ratio its kind of network shows on Android
        vn = vc * labelled_one(O, v, ANALOGUE[c])
    elif how == "common":                                          # at the one ratio the unattributed accounts add up to
        vn = vc * s2_fit(O, v, cells, minn, tilt, common=True)[ci]
    elif how == "paid":                                            # organic at Apple Search Ads' ratio, one for the networks
        vn = vc * s2_fit(O, v, cells, minn, tilt, common="paid", org_pin=asa_one(O, v))[ci]
    else:                                                          # at the network's own fitted ratio
        fit = dict(fit)
        if "org_pin" in fit:
            fit["org_pin"] = _pin(O, v, fit["org_pin"])
        vn = vc * s2_fit(O, v, cells, minn, tilt, **fit)[ci]
    tot = n + nc
    return T["key32"], np.where(tot > 0, (n * vc + nc * vn) / np.maximum(tot, 1e-9), vc), tot


def channel_values(O, v, how="golden", cells="fine", minn=20, tilt="cell", rcells="tier2", **fit):
    """each channel's twelve-month net revenue per install over every install it bought in the 52 mature weeks"""
    out = {}
    for ci, c in enumerate(ORDER):
        lab = (O.label == ci) & O.mature
        if CH[c]["complete"] or how == "consenters":
            out[c] = float(v[lab].mean())
        elif how == "direct":
            out[c] = float(v[lab].sum() / O.agg[c][:MATURE].sum())
        else:
            _k, price, tot = ios_price(O, v, c, how, cells, minn, tilt, rcells, **fit)
            out[c] = float((tot * price).sum() / tot.sum())
    return out


def adding_up(O, v, how="golden", cells="fine", rcells="tier2"):
    """the unattributed iOS accounts' twelve-month revenue as a route prices it (the networks' declined installs and
    the organic ones) over what those accounts paid"""
    S = s2_strata(O, v, cells)
    T = S["T"]
    srcs = S["hidden"] + [S["org"]]
    r = s2_fit(O, v, cells) if how == "golden" else None
    tot = 0.0
    for i in srcs:
        f = {"bridge": 1.0, "ratio": asa_ratio(O, v, cells, rcells)}.get(how, r[i] if r else 1.0)
        tot += float((S["nc"][i].sum((0, 1)) * T["vc"][i] * f).sum())
    return tot / float(S["pv"].sum())


def true_ratios(O, v, W, ios=True):
    """the world's own figure for each source: what its declined installs paid over what they would have paid at the
    value of its installs that allowed tracking (read with every account's source, which the files do not hold)"""
    T = s2_cells(O, v, ios=ios)
    paid, org = platform_sources(ios)
    out = {}
    for i in paid + [org]:
        lab = O.mature & (W["src"] == i) & ~W["consent"]
        cnt = np.bincount(O.cv[lab], minlength=32)
        out[i] = float(v[lab].sum() / max((cnt * T["vc"][i]).sum(), 1e-9))
    return out


# --------------------------------------------------------------------------------------------------------------
# S3: what the plan's weekly spend buys
# --------------------------------------------------------------------------------------------------------------

def weekly_quality(O, v, c, how="golden", s2="golden", cells="fine", minn=20, tilt="cell", fit=None):
    """the channel's value per install by install week, on a record that sees the whole week's installs: each week's
    installs priced by first-48-hour value at what that value was worth over the mature weeks (every week), or, for a
    channel whose every account carries it, the mature weeks' own twelve-month values"""
    ci = ORDER.index(c)
    lab = O.label == ci
    if not CH[c]["complete"]:
        how2 = {"consenters": "bridge", "direct": "golden"}.get(s2, s2)
        k32, price, _A = ios_price(O, v, c, how2, cells, minn, tilt, **(fit or {}))
        A = O.agg_cv[c]
        return (A @ price[k32]) / np.maximum(A.sum(1), 1)
    m = lab & O.mature
    if how == "value":
        out = np.full(WEEKS, np.nan)
        out[:MATURE] = (np.bincount(O.week[m], weights=v[m], minlength=WEEKS)
                        / np.maximum(np.bincount(O.week[m], minlength=WEEKS), 1))[:MATURE]
        return out
    tot = np.bincount(O.cv[m], weights=v[m], minlength=32); cnt = np.bincount(O.cv[m], minlength=32)
    price = np.where(cnt >= minn, tot / np.maximum(cnt, 1), v[m].mean())
    return (np.bincount(O.week[lab], weights=price[O.cv[lab]], minlength=WEEKS)
            / np.maximum(np.bincount(O.week[lab], minlength=WEEKS), 1))


def response(O, v, how="golden", months="pooled", quality="golden", weeks_i=(0, WEEKS), s2="golden", cells="fine",
             minn=20, qpool=False, leave=(), tilt="cell", fit=None, weeks_v=(0, WEEKS)):
    """installs and value per install against the week's budget (with the platform's delivery beside it), or against
    the week's spend; each channel's own slopes, the month pattern pooled across channels (or each channel's own)"""
    C = len(ORDER)
    fits = {}
    nx = {"golden": 2, "budget": 1, "spend": 1, "iv": 1}[how]
    leave = set(leave)
    for nm in ("i", "v"):
        rows = []
        for ci, c in enumerate(ORDER):
            Bc = O.B[c]
            lb, ls = np.log(Bc["budget"]), np.log(Bc["spend"])
            ld = ls - lb
            y = O.agg[c] if nm == "i" else weekly_quality(O, v, c, quality, s2, cells, minn, tilt, fit)
            lo, hi = weeks_i if nm == "i" else weeks_v
            for w in range(lo, hi):
                if (c, w) in leave:
                    continue
                if not np.isnan(y[w]) and y[w] > 0:
                    rows.append((ci, w, lb[w] - lb.mean(), ld[w] - ld.mean(), ls[w] - ls.mean(), np.log(y[w])))
        nmon = 11 * C if months == "own" else 11
        X = np.zeros((len(rows), C + nx * C + nmon)); y = np.zeros(len(rows))
        Z = np.zeros_like(X)
        pooled_q = qpool and nm == "v"
        for i, (ci, w, lb, ld, ls, ly) in enumerate(rows):
            X[i, ci] = Z[i, ci] = 1
            sc = C if pooled_q else C + ci                         # one value slope for every channel, or its own
            if how == "golden":
                X[i, sc], X[i, 2 * C + ci] = lb, ld
            elif how == "budget":
                X[i, sc] = lb
            elif how == "spend":
                X[i, sc] = ls
            else:
                X[i, sc], Z[i, sc] = ls, lb
            mo = WMONTH[w]
            if mo > 1:
                j = C + nx * C + (11 * ci if months == "own" else 0) + mo - 2
                X[i, j] = Z[i, j] = 1
            y[i] = ly
        keep = np.abs(X).sum(0) > 0
        beta = np.zeros(X.shape[1])
        if how == "iv":
            beta[keep] = np.linalg.lstsq(Z[:, keep].T @ X[:, keep], Z[:, keep].T @ y, rcond=None)[0]
        else:
            beta[keep] = np.linalg.lstsq(X[:, keep], y, rcond=None)[0]
        mon = beta[C + nx * C:]
        mon = np.concatenate([np.zeros((C, 1)), mon.reshape(C, 11) if months == "own" else np.tile(mon, (C, 1))], axis=1)
        slope = np.full(C, beta[C]) if pooled_q else beta[C:2 * C]
        fits[nm] = dict(a=beta[:C], s=slope, d=beta[2 * C:3 * C] if how == "golden" else np.zeros(C), mon=mon)
    fits["how"] = how
    return fits


def at_plan(O, coef, c, v12, dbar_weeks=WEEKS, dbar_scale=1.0, dbar_from=0, carry="rescaled"):
    """installs a week and value per install at the plan's 2027 weekly spend and at the stretch column's, the return
    per euro at each, and what the next euro returns on top of each (a constant-elasticity response: the return at
    that spend times the two budget slopes). carry: the fitted installs at the budget that delivers the plan's spend,
    rescaled so that the fit adds up to the installs on record ("rescaled"), or the fit's own prediction as it stands
    with the share of the budget spent put at its ratio of totals ("plain"), its geometric mean ("plain-geo") or its
    median week ("plain-median"), or with each week's own share put through the delivery term and averaged
    ("plain-dist"). The share is taken over the weeks dbar_from to dbar_weeks."""
    ci = ORDER.index(c)
    Bc = O.B[c]
    sp = plan_spend(c)
    plain = carry != "rescaled"
    dterm = 0.0
    if coef["how"] in ("spend", "iv"):
        x_hist = np.log(Bc["spend"]) - np.log(Bc["spend"]).mean()
        x_plan = np.log(sp) - np.log(Bc["spend"]).mean()
    else:                                                          # the budget that delivers the plan's spend
        sl = slice(dbar_from, dbar_weeks)
        share = Bc["spend"][sl] / Bc["budget"][sl]
        dbar = Bc["spend"][sl].sum() / Bc["budget"][sl].sum()
        if carry == "plain-geo":
            dbar = float(np.exp(np.log(share).mean()))
        elif carry == "plain-median":
            dbar = float(np.median(share))
        dbar *= dbar_scale
        x_hist = np.log(Bc["budget"]) - np.log(Bc["budget"]).mean()
        x_plan = np.log(sp / dbar) - np.log(Bc["budget"]).mean()
        if plain:                                                  # the delivery term at the share the plan is put at
            ld = np.log(Bc["spend"]) - np.log(Bc["budget"])
            dterm = float(coef["i"]["d"][ci] * (np.log(dbar) - ld.mean()))
            if carry == "plain-dist":                              # or at each week's own share, averaged
                dterm = float(np.log(np.exp(coef["i"]["d"][ci] * (np.log(share * dbar_scale) - ld.mean())).mean()))
    si, sv = coef["i"]["s"][ci], coef["v"]["s"][ci]
    mi, mv = coef["i"]["mon"][ci], coef["v"]["mon"][ci]
    back = 1.0 if plain else O.agg[c].sum() / np.exp(coef["i"]["a"][ci] + si * x_hist + mi[WMONTH - 1]).sum()
    fm = np.exp(sv * x_hist[:MATURE] + mv[WMONTH[:MATURE] - 1])
    wt = O.agg[c][:MATURE]
    level = v12 / ((fm * wt).sum() / wt.sum())                    # the fitted value over the mature weeks is v12
    out = {}
    for tag, lift in (("", 0.0), ("_s", float(np.log(CH[c]["stretch"])))):
        n = back * np.exp(coef["i"]["a"][ci] + si * (x_plan + lift) + dterm + mi[PLAN_MONTH - 1])
        vp = level * np.exp(sv * (x_plan + lift) + mv[PLAN_MONTH - 1])
        out["roas" + tag] = (n * vp).sum() / (sp.sum() * np.exp(lift))
        out["revenue" + tag] = (n * vp).sum()
        if not tag:
            out.update(installs_week=n.mean(), vpi=(n * vp).sum() / n.sum())
    out.update(marginal=out["roas"] * (si + sv), marginal_s=out["roas_s"] * (si + sv), el=si, qs=sv)
    return out


# --------------------------------------------------------------------------------------------------------------
# a route: every channel's figures under one set of choices
# --------------------------------------------------------------------------------------------------------------

_CACHE = {}


def values(O, s1="golden", **kw):
    k1 = (id(O), "v", s1) + tuple(kw.get(k) for k in ("split", "trim", "form", "cadence", "webq", "cshare", "s1_nudge"))
    if k1 not in _CACHE:
        fits = None
        if kw.get("webq") and s1 == "golden":
            fits = s1_fit(O)
            q = s1_web_fit(O)
            for f in fits.values():
                f["q"] = f["q1"] = q
        if kw.get("s1_nudge") and s1 == "golden":                  # ("share" or "lapse", a factor): a fitted rate moved
            what, fac = kw["s1_nudge"]
            fits = {pl: dict(f) for pl, f in s1_fit(O).items()}
            for f in fits.values():
                if what == "share":
                    f["c_m"], f["c_a"] = f["c_m"] * fac, f["c_a"] * fac
                else:
                    f["q"] = f["q1"] = 1.0 - (1.0 - f["q"]) * fac
        _CACHE[k1] = s1_values(O, s1, split=kw.get("split", "store"), trim=kw.get("trim", 0),
                               form=kw.get("form", "geo"), cadence=kw.get("cadence", MONTH_DAYS), fits=fits,
                               cshare=kw.get("cshare", "level"))[0]
    return _CACHE[k1]


def route(O, s1="golden", s2="golden", s3="golden", **kw):
    """every channel's figures under one route: s1 in raw, prop, prop_month, golden; s2 in direct, consenters,
    bridge, ratio, golden; s3 in average, spend, budget, iv, golden; kw carries a variant's conventions"""
    key = (id(O), s1, s2, s3, tuple(sorted(kw.items())))
    if key in _CACHE:
        return _CACHE[key]
    v = values(O, s1, **kw)
    cells, minn, tilt = kw.get("cells", "fine"), kw.get("minn", 20), kw.get("tilt", "cell")
    fit = {k: kw[k] for k in FITKEYS if k in kw}
    v12 = channel_values(O, v, s2, cells, minn, tilt, **fit)
    r12 = channel_values(O, values(O, "raw"), s2, cells, minn, tilt, **fit)
    N12 = {c: float(O.agg[c][:MATURE].sum()) for c in ORDER}
    res = {}
    if s3 == "average":                                            # the mature year's return per euro carried over
        for c in ORDER:
            n = O.agg[c][:MATURE].sum()
            r = v12[c] * n / O.B[c]["spend"][:MATURE].sum()
            res[c] = dict(v12=v12[c], rec12=r12[c] * N12[c], rev12=v12[c] * N12[c], unrec=1 - r12[c] / v12[c], roas=r,
                          vpi=v12[c], installs_week=n / 52.0,
                          marginal=r, marginal_s=r, revenue=r * plan_spend(c).sum(), roas_s=r,
                          revenue_s=r * plan_spend(c).sum() * CH[c]["stretch"], el=1.0, qs=0.0)
        _CACHE[key] = res
        return res
    coef = response(O, v, how=s3, months=kw.get("months", "pooled"), quality=kw.get("quality", "golden"),
                    weeks_i=kw.get("weeks_i", (0, WEEKS)), s2=s2, cells=cells, minn=minn, qpool=kw.get("qpool", False),
                    tilt=tilt, fit=fit, weeks_v=kw.get("weeks_v", (0, WEEKS)))
    nud = kw.get("s3_nudge")                                       # ("el" or "qs" or "dbar", a factor): a fitted input moved
    if nud and nud[0] in ("el", "qs"):
        eq = "i" if nud[0] == "el" else "v"
        coef = dict(coef)
        coef[eq] = dict(coef[eq], s=coef[eq]["s"] * nud[1])
    for c in ORDER:
        res[c] = dict(v12=v12[c], rec12=r12[c] * N12[c], rev12=v12[c] * N12[c], unrec=1 - r12[c] / v12[c],
                      **at_plan(O, coef, c, v12[c], kw.get("dbar_weeks", WEEKS),
                                nud[1] if nud and nud[0] == "dbar" else 1.0, kw.get("dbar_from", 0),
                                kw.get("carry", "rescaled")))
    _CACHE[key] = res
    return res


VARIANTS = [
    ("one fit across both stores", dict(split="pooled")),
    ("two-rate continuation", dict(form="two")),
    ("fit without the last two months", dict(trim=2)),
    ("thirty-day cadence", dict(cadence=30.0)),
    ("one share charged for every trial-end candidate", dict(cshare="flat")),
    ("first-48-hour cells in eight groups", dict(cells="tier8")),
    ("first-48-hour cells in four groups", dict(cells="tier4")),
    ("cells of fifty or more", dict(minn=50)),
    ("each source's named installs through one tilt", dict(tilt="one")),
    ("the ratios fitted separately for lighter and heavier first-48-hour use", dict(rows="market-week-tier")),
    ("the ratios fitted unweighted", dict(weight="none")),
    ("the ratios fitted by fortnight", dict(span=2)),
    ("the ratios fitted by four-week period", dict(span=4)),
    ("the ratios fitted with weights from the fitted revenue", dict(weight="fitted")),
    ("organic installs' ratio taken from Apple Search Ads", dict(org_pin="asa")),
    ("market-weeks of fewer than a hundred unattributed accounts left out", dict(minpool=100)),
    ("the networks' ratios drawn toward their pooled ratio by the fit's own spread", dict(shrink=True)),
    ("Google iOS and Pinterest iOS sharing one ratio", dict(group="gp")),
    ("Google iOS, Pinterest iOS and the organic installs sharing one ratio", dict(group="gpo")),
    ("Pinterest iOS and the organic installs sharing one ratio", dict(group="po")),
    ("Google iOS and the organic installs sharing one ratio", dict(group="go")),
    ("Meta iOS and TikTok iOS sharing one ratio", dict(group="pair")),
    ("TikTok iOS and Snapchat iOS sharing one ratio", dict(group="pair2")),
    ("every postback dated back three days", dict(align="three")),
    ("every postback dated back four days", dict(align="four")),
    ("each channel's own month pattern", dict(months="own")),
    ("installs response without the launch quarter", dict(weeks_i=(13, WEEKS))),
    ("value response on the mature weeks' own values", dict(quality="value")),
    ("one value slope across channels", dict(qpool=True)),
    ("delivery share from the mature weeks", dict(dbar_weeks=MATURE)),
    ("delivery share from the last 52 weeks", dict(dbar_from=MATURE)),
    ("installs response on the last 78 weeks", dict(weeks_i=(26, WEEKS))),
    ("spend instrumented by the budget", dict(s3="iv")),
    ("the budget alone, the delivery left out", dict(s3="budget")),
]
# ways that stand beside the battery: each is run as it is and the ranges take in the edges it leaves, but it is not
# crossed with the battery's ways. Four families. The second step's fit on a finer grain of rows (each market-week's
# accounts split by the first-48-hour sessions they carry, in the eight values or their four pairs), under each of
# the three weightings. The installs equation's own prediction at the plan, not rescaled to the installs on record,
# with the share of the budget spent taken over the 104 weeks, the mature weeks or the last 52, and put at its ratio
# of totals or put week by week through the delivery term and averaged (the geometric mean of the weekly shares and
# the median week's share are not held: over the weeks the share is taken from they leave out 4 per cent or more of
# some channel's installs, RS.carry_block). The first-48-hour value grouped on one part of it alone (the sessions
# bits in their eight values or four pairs, the trial and purchase bits, those two bits with the sessions split in
# two). The value equation fitted on the mature weeks alone
SHARE_WEEKS = (("the 104 weeks'", {}), ("the mature weeks'", dict(dbar_weeks=MATURE)),
               ("the last 52 weeks'", dict(dbar_from=MATURE)))
BESIDE = [("the ratios fitted on each market-week's accounts split by %s%s" % (g, w), dict(rows=r, **kw))
          for r, g in (("market-week-pair", "pairs of first-48-hour sessions values"),
                       ("market-week-bucket", "first-48-hour sessions value"))
          for w, kw in (("", {}), (", unweighted", dict(weight="none")),
                        (", with weights from the fitted revenue", dict(weight="fitted")))]
BESIDE += [("the installs equation's own prediction, not rescaled, at %s %s" % (wn, nm), dict(carry=k, **wkw))
           for wn, wkw in SHARE_WEEKS
           for k, nm in (("plain", "share of the budgets spent"),
                         ("plain-dist", "weekly shares, each put through the delivery term and averaged"))]
BESIDE += [("the first-48-hour values grouped by %s" % nm, dict(cells=k))
           for k, nm in (("sess8", "their sessions bits alone, in eight values"),
                         ("sess4", "their sessions bits alone, in four pairs"),
                         ("tp4", "their trial and purchase bits alone"),
                         ("tp8", "their trial and purchase bits with the sessions split in two"))]
BESIDE += [("the value equation fitted on the mature weeks alone", dict(weeks_v=(0, MATURE)))]
HURRIED = {"S1": dict(s1="prop_month"), "S2": dict(s2="bridge"), "S3": dict(s3="spend")}
# the most rigorous standard design the pack affords: the stores' true-up month by month, every postback priced by
# first-48-hour value and corrected with the one labelled check iOS offers (Apple Search Ads' declined installs), the
# response fitted on spend with its hold-out
RIGOROUS = dict(s1="prop_month", s2="ratio", s3="spend")


def lattice_route(O, lost):
    kw = {}
    for s in lost:
        kw.update(HURRIED[s])
    return route(O, **kw)


def band(x):
    return "cut" if x < LINES[0] else ("hold" if x < LINES[1] else "scale")


def quarter_departure(O):
    """the widest departure of any channel's quarter from its 104-week delivery share (spend over budget)"""
    worst = 0.0
    for c in MEMBERS:
        Bc = O.B[c]
        d = Bc["spend"].sum() / Bc["budget"].sum()
        for q in range(WEEKS // 13):
            sl = slice(13 * q, 13 * q + 13)
            worst = max(worst, abs(Bc["spend"][sl].sum() / Bc["budget"][sl].sum() / d - 1.0))
    return worst


def forcing(O):
    """the audit's perturbation: each fitted input moved a fifth either way (the delivery share by its widest
    quarter), every other input as fitted; (the input, the factor, each member's return, whether the call holds)"""
    g = route(O)
    dq = quarter_departure(O)
    moves = [("the share of trial-end candidates charged", dict(s1_nudge=("share", f))) for f in (0.8, 1.2)]
    moves += [("the monthly lapse of a subscription nobody opens", dict(s1_nudge=("lapse", f))) for f in (0.8, 1.2)]
    moves += [("%s's fitted ratio" % c, dict(r_nudge=(c, f))) for c in GATED for f in (0.8, 1.2)]
    moves += [("the organic installs' fitted ratio", dict(r_nudge=("organic iOS", f))) for f in (0.8, 1.2)]
    moves += [("every channel's budget elasticity of installs", dict(s3_nudge=("el", f))) for f in (0.8, 1.2)]
    moves += [("every channel's value slope", dict(s3_nudge=("qs", f))) for f in (0.8, 1.2)]
    moves += [("the delivery share that turns the plan's spend into a budget", dict(s3_nudge=("dbar", f)))
              for f in (1.0 - dq, 1.0 + dq)]
    moves += [("the delivery share of the last 26 weeks", dict(dbar_from=78)),
              ("the delivery share of the last 13 weeks", dict(dbar_from=91))]
    out = []
    for nm, kw in moves:
        r = route(O, **kw)
        fac = list(kw.values())[0]
        fac = fac[1] if isinstance(fac, tuple) else 1.0
        out.append((nm, fac, {c: float(r[c]["roas"]) for c in MEMBERS},
                    all(band(r[c]["roas"]) == band(g[c]["roas"]) for c in MEMBERS)))
    return out


# --------------------------------------------------------------------------------------------------------------
# the referee slices: where the hidden quantity is on file, which the target does not reach
# --------------------------------------------------------------------------------------------------------------

def s1_web_method(O):
    """the first step's own fit, run where the answer is on file: the web checkout's monthly subscribers, their
    charges after the last open set aside, and the monthly continuation of a subscription nobody opens fitted to the
    months those charges fell in"""
    idx, n_open = _web_silent(O)
    idx, n_open = idx[n_open >= 1], n_open[n_open >= 1]
    after = O.true_charge[idx] & (O.rdays[idx] > O.last_open[idx][:, None])
    R = np.bincount(O.mon[idx][after], minlength=O.NM)[:O.NM].astype(float)
    last = O.rdays[idx, n_open - 1]
    Mr = np.zeros((K, O.NM))
    for j in range(1, K):
        d = last + np.round(MONTH_DAYS * j).astype(int)
        d = d[d <= END_DAY]
        Mr[j - 1] = np.bincount((d // MONTH_DAYS).astype(int), minlength=O.NM)[:O.NM]
    best = None
    miss = lambda q: float(((((q ** np.arange(1, K + 1)) @ Mr) - R)[:O.NM - 1] ** 2).sum())
    for q in np.linspace(0.40, 0.99, 296):
        err = miss(q)
        if best is None or err < best[0]:
            best = (err, q)
    return float(refine(miss, best[1], 0.002))


def referee_s1(O, c="AppLovin Android"):
    """the web checkout's subscribers of one channel, whose every charge the backend holds: the net revenue charged
    after each one's last open, inside the first twelve months, per subscriber; what the first step's fit puts there
    from the months alone; and what the stores' true-up would have put there"""
    ci = ORDER.index(c)
    idx, n_open = _web_silent(O, (O.label == ci) & O.mature)
    idx, n_open = idx[n_open >= 1], n_open[n_open >= 1]
    wend = O.day[idx] + 365
    after = O.true_charge[idx] & (O.rdays[idx] > O.last_open[idx][:, None]) & (O.rdays[idx] < wend[:, None])
    truth = (after.sum(1) * O.netm[idx]).sum() / idx.size
    last = O.rdays[idx, n_open - 1]

    def put(q):
        g = np.zeros(idx.size)
        for j in range(1, K):
            d = last + np.round(MONTH_DAYS * j).astype(int)
            g += q ** j * O.netm[idx] * ((d < wend) & (d <= END_DAY) & (d > O.last_open[idx]))
        return float(g.sum() / idx.size)

    qw = s1_web_method(O)
    qs = s1_fit(O)[0 if not CH[c]["ios"] else 1]["q"]
    # the proportional true-up: each recorded charge scaled by its store-month's ratio of charged to recorded
    pl = int(CH[c]["ios"])
    mk = (O.ios == bool(pl)) & ~O.web
    st = O.store[pl]["first"] + O.store[pl]["ren"]
    rc = _monthly_counts(O, mk, "first") + _monthly_counts(O, mk, "ren")
    fac = np.where(rc > 0, st / np.maximum(rc, 1), 1.0)
    seen = O.true_charge[idx] & (O.rdays[idx] <= O.last_open[idx][:, None]) & (O.rdays[idx] < wend[:, None])
    prop = ((seen * (fac[np.minimum(O.mon[idx], O.NM - 1)] - 1)).sum(1) * O.netm[idx]).sum() / idx.size
    return dict(slice="the web checkout's %s subscribers: net revenue charged after the last open, per subscriber" % c,
                n=int(idx.size), truth=float(truth), golden=put(qw), rivals={"proportional true-up": float(prop)},
                other={"the stores' fitted continuation carried over": put(qs), "continuation fitted on the web": qw,
                       "continuation fitted on the store": float(qs)})


def referee_s2(O, v, c="AppLovin Android"):
    """Android, where every account carries its channel: one network's declined installs' twelve-month value, and
    what the second step's fit gives them with their channel set aside (the declined accounts pooled, each source's
    count in each market-week kept)"""
    i = ORDER.index(c)
    S = s2_strata(O, v, ios=False)
    T = S["T"]
    lab = O.mature & (O.label == i) & ~O.consent
    cnt = S["nc"][i].sum((0, 1))
    base = float((cnt * T["vc"][i]).sum() / cnt.sum())
    r = s2_fit(O, v, ios=False)[i]
    rc = s2_fit(O, v, ios=False, common=True)[i]
    asa = float((cnt * T["vc"][i] * asa_ratio(O, v)).sum() / cnt.sum())
    return dict(slice="%s's installs that declined the prompt, their channel set aside: twelve-month net revenue per "
                      "install" % c, n=int(lab.sum()), truth=float(v[lab].mean()), golden=float(r * base),
                rivals={"priced at its installs that allowed tracking, by first-48-hour value": base,
                        "at Apple Search Ads' ratio": asa, "at one ratio for every source": float(rc * base)})


def referee_s3(O, v, c="Google Android"):
    """the weeks the team moved one channel's budget, each move left out of the fit in turn: installs bought in the
    raised weeks over installs bought in the lowered weeks"""
    up = dn = 0.0
    pred = {"golden": [0.0, 0.0], "spend": [0.0, 0.0], "iv": [0.0, 0.0], "budget": [0.0, 0.0]}
    ci = ORDER.index(c)
    Bc = O.B[c]
    lb, ls = np.log(Bc["budget"]), np.log(Bc["spend"])
    ld = ls - lb
    for w0, k, f in CH[c]["pushes"]:
        wk = [w for w in range(w0, w0 + k)]
        act = O.agg[c][wk].sum()
        if f > 1:
            up += act
        else:
            dn += act
        for how in pred:
            coef = response(O, v, how=how, leave=[(c, w) for w in wk])
            a, s_, d_, mon = coef["i"]["a"][ci], coef["i"]["s"][ci], coef["i"]["d"][ci], coef["i"]["mon"][ci]
            x = (lb[wk] - lb.mean()) if how in ("golden", "budget") else (ls[wk] - ls.mean())
            p = np.exp(a + s_ * x + d_ * (ld[wk] - ld.mean()) + mon[WMONTH[wk] - 1]).sum()
            pred[how][0 if f > 1 else 1] += p
    return dict(slice="%s's budget moves, each left out of the fit in turn: installs in the raised weeks over installs "
                      "in the lowered weeks" % c, truth=float(up / dn), golden=float(pred["golden"][0] / pred["golden"][1]),
                rivals={"response fitted on spend": float(pred["spend"][0] / pred["spend"][1])},
                other={"spend instrumented by the budget": float(pred["iv"][0] / pred["iv"][1]),
                       "the budget alone": float(pred["budget"][0] / pred["budget"][1])})


# --------------------------------------------------------------------------------------------------------------
# the spec corelib checks
# --------------------------------------------------------------------------------------------------------------

OWN = {"S1": "AppLovin Android", "S2": "Meta iOS", "S3": "Google Android"}
# every figure the answer blocks state, channel by channel: the return per euro at the plan's weekly spend (the
# member's own figure) and at its stretch spend, the installs a week the plan's spend buys and their value, what the
# next euro returns on top of the plan's spend and on top of the stretch spend, and what the installs of the mature
# year went on to pay
FAMILIES = [("return ", "roas"), ("stretch return ", "roas_s"), ("installs a week ", "installs_week"),
            ("value at plan ", "vpi"), ("next euro ", "marginal"), ("stretch next euro ", "marginal_s"),
            ("paid per install ", "v12")]
# each stump's own figure, one decisive step's answer: it falls with that stump alone
COMPONENTS = {"S1": "paid per install AppLovin Android", "S2": "paid per install Meta iOS",
              "S3": "installs a week Google Android"}


# the blocks answer each of the prompt's four asks with one line per channel, and the generated rubric makes one
# criterion of a line, all or nothing (supplemental-stumping Part 1 rule 7): the return at the plan's and the stretch
# spend, the installs a week and what each will have paid, the next euro at the plan's and the stretch spend, and
# what the mature year's installs paid
ASK_OF = {"return ": "returns", "stretch return ": "returns", "installs a week ": "installs and their revenue",
          "value at plan ": "installs and their revenue", "next euro ": "one more euro",
          "stretch next euro ": "one more euro", "paid per install ": "the year to November 2025"}
ON_LINE = "on its line: "         # a component's figure as its ask line states it


def stated_id(fid):
    """the figure a listed criterion figure is"""
    return fid[len(ON_LINE):] if fid.startswith(ON_LINE) else fid


def sentence_of(fid):
    """the line of the answer blocks a figure is stated on"""
    kind = max((k for k in ASK_OF if fid.startswith(k)), key=len)
    return "%s, %s" % (ASK_OF[kind], fid[len(kind):])


def as_stated(figures):
    """the graded figures as the answer blocks state them: every figure carries the line it sits on, and a
    component's figure is stated on its ask line as well as in the Critical Components"""
    out = []
    for f in figures:
        if f["block"] == "component":
            out.append(dict(f))
            out.append(dict(f, id=ON_LINE + f["id"], block="ask", sentence=sentence_of(f["id"])))
        else:
            out.append(dict(f, sentence=sentence_of(f["id"])))
    return out


def figure_values(res):
    """every graded figure a route files"""
    return {nm + c: float(res[c][k]) for c in MEMBERS for nm, k in FAMILIES}


BAND_PAD = 0.005                 # either side of the battery's span: what two careful rebuilds of one way differ by
BESIDE_PAD = 0.01                # beyond a way that stands beside the battery


def unit(fid):
    """the decimals a figure is stated at: a return per euro to the thousandth, euros per install to the cent, installs
    a week to the unit"""
    if fid.startswith("installs a week "):
        return 0
    if fid.startswith(("value at plan ", "paid per install ")):
        return 2
    return 3


def band_of(fid, g, fam, beside=()):
    """the range the answer blocks state for a figure: the battery's span with half a per cent of the figure each side
    (what two careful rebuilds of one variant differ by), reaching one per cent of the figure beyond every way that
    stands beside the battery and moves the figure (two rebuilds of a fit on finer rows differ by more), stated
    outward at the figure's precision"""
    nd = unit(fid)
    lo, hi = min(min(fam), g), max(max(fam), g)
    w = BAND_PAD * abs(g)
    lo, hi = lo - w, hi + w
    moved = [x for x in beside if abs(x - g) > 1e-6 * abs(g)]      # a way that leaves the figure where it is adds nothing
    if moved:
        w2 = BESIDE_PAD * abs(g)
        lo, hi = min(lo, min(moved) - w2), max(hi, max(moved) + w2)
    f = 10.0 ** nd
    a, b = math.floor(lo * f + 1e-9) / f, math.ceil(hi * f - 1e-9) / f
    return [int(round(a)), int(round(b))] if nd == 0 else [round(a, nd), round(b, nd)]


def build_spec(W=None, verbose=False):
    W = W or simulate()
    O = Obs(W)
    T = truth_at_plan()
    g = route(O)
    aligned = {}

    def variant(kw):
        kw = dict(kw)
        al = kw.pop("align", None)
        if al is None:
            return route(O, **kw)
        if al not in aligned:
            aligned[al] = Obs(W, align=al)
        return route(aligned[al], **kw)
    fam = [variant(kw) for _nm, kw in VARIANTS + BESIDE]
    nbat = len(VARIANTS)                                           # the battery's ways first, then the ways beside it
    keys = [["S1"], ["S2"], ["S3"], ["S1", "S2"], ["S1", "S3"], ["S2", "S3"], ["S1", "S2", "S3"]]
    lat_res = {"+".join(k): lattice_route(O, k) for k in keys}
    direct = route(O, "raw", "direct", "average")
    rigorous = route(O, **RIGOROUS)
    members = {}
    for c in MEMBERS:
        members[c] = dict(lines=list(LINES), truth=float(T[c]["roas"]), golden=float(g[c]["roas"]),
                          family=[float(r[c]["roas"]) for r in fam],
                          routes=dict(direct=float(direct[c]["roas"]), rigorous=float(rigorous[c]["roas"])))
    stumps = {
        "S1": dict(axis="what", opens=OWN["S1"], steps_left=4, precedents=["N21", "L44"],
                   said_out_loud="A store charge reaches the app's billing records only when the subscriber next opens "
                                 "the app, so the stores' excess over the records belongs to subscriptions last seen "
                                 "still set to renew, not to every account in proportion."),
        "S2": dict(axis="who", opens=OWN["S2"], steps_left=5, precedents=["L53", "N27", "L58"],
                   said_out_loud="On iOS the attribution export names an install's channel only where the user allowed "
                                 "tracking; each network's other installs sit unnamed among the accounts with no "
                                 "channel, and how much less they are worth than its named ones differs from network "
                                 "to network."),
        "S3": dict(axis="against", opens=OWN["S3"], steps_left=3, precedents=["L51", "L37", "L28"],
                   said_out_loud="A week's spend is what the platform chose to deliver of the week's budget given that "
                                 "week's auction, so weeks of high and low spend are not weeks of high and low "
                                 "budgets; what a budget buys shows in the weeks the team moved it."),
    }
    lattice = {k: {c: float(r[c]["roas"]) for c in MEMBERS} for k, r in lat_res.items()}
    gf, rf = figure_values(g), figure_values(rigorous)
    ff = [figure_values(r) for r in fam]
    lf = {k: figure_values(r) for k, r in lat_res.items()}
    # each figure priced on the range the blocks will state for it (band_of), as the build prices it on the cut pack
    rng = lambda fid: band_of(fid, gf[fid], [x[fid] for x in ff[:nbat]], [x[fid] for x in ff[nbat:]])
    figures = []
    for c in MEMBERS:
        figures.append(dict(id="return " + c, block="ask", weight=1.0, member=c, band=rng("return " + c)))
    own = set(COMPONENTS.values())
    for kind, _k in FAMILIES[1:]:
        for c in MEMBERS:
            fid = kind + c
            figures.append(dict(id=fid, block="component" if fid in own else "ask", weight=1.0, golden=gf[fid],
                                band=rng(fid), family=[x[fid] for x in ff], lattice={k: x[fid] for k, x in lf.items()},
                                routes=dict(rigorous=rf[fid])))
    v = values(O)
    refs = [referee_s1(O), referee_s2(O, v), referee_s3(O, v)]

    def sep(r):
        ge = abs(r["golden"] - r["truth"])
        return min(abs(x - r["truth"]) for x in r["rivals"].values()) / max(ge, 1e-12)
    weakest = min(refs, key=sep)
    spec = dict(call="lines", members=members, stumps=stumps, lattice=lattice,
                referee=dict(slice=weakest["slice"], covers_target=False, truth=weakest["truth"],
                             golden=weakest["golden"], rivals=weakest["rivals"]), figures=as_stated(figures))
    if verbose:
        return spec, dict(O=O, W=W, T=T, g=g, fam=fam, lat=lat_res, direct=direct, rigorous=rigorous, refs=refs,
                          sep=[sep(r) for r in refs])
    return spec


def explore():
    spec, X = build_spec(verbose=True)
    O, W, T, g = X["O"], X["W"], X["T"], X["g"]
    tv = value12(W)
    rec = values(O, "raw")
    v = values(O)
    short = lambda c: c.replace(" Android", " A").replace("Apple Search Ads", "ASA").replace("Snapchat", "Snap")[:9]
    print("accounts %d" % O.n)
    tr = dict(true_ratios(O, v, W, True)); tr.update(true_ratios(O, v, W, False))
    fi = dict(s2_fit(O, v)); fa = s2_fit(O, v, ios=False)
    for ci, c in enumerate(SOURCES):
        mk = (W["src"] == ci) & O.mature
        est = fi.get(ci, fa.get(ci, float("nan")))
        print("  %-18s n %6d consent %.2f value %6.2f unrecorded %.2f  buyers %.3f  declined/named at the same first "
              "two days: true %.3f fitted %.3f" % (
                  c, mk.sum(), W["consent"][mk].mean(), tv[mk].mean(), 1 - rec[mk].sum() / tv[mk].sum(),
                  (W["charge"][mk, 0] | W["a0"][mk]).mean(), tr[ci], est))
    print("  Apple Search Ads' labelled ratio %.3f; one ratio for every iOS source %.3f; Android %.3f" % (
        asa_one(O, v), s2_fit(O, v, common=True)[0], s2_fit(O, v, ios=False, common=True)[ORDER.index("Google Android")]))
    for pl in (1, 0):
        mk = (O.ios == bool(pl)) & O.mature
        print("  platform ios=%d unrecorded %.3f" % (pl, 1 - rec[mk].sum() / tv[mk].sum()))
    print("fits", {k: {a: round(float(x), 3) for a, x in f.items()} for k, f in s1_fit(O).items()},
          "web continuation read %.3f, fitted from the months %.3f" % (s1_web_fit(O), s1_web_method(O)))
    routes = [(("golden", "golden", "golden"), {}), (("prop_month", "golden", "golden"), {}),
              (("prop", "golden", "golden"), {}), (("raw", "golden", "golden"), {}),
              (("golden", "golden", "golden"), dict(webq=True)), (("awake", "golden", "golden"), {}),
              (("golden", "bridge", "golden"), {}), (("golden", "consenters", "golden"), {}),
              (("golden", "ratio", "golden"), {}), (("golden", "analogue", "golden"), {}),
              (("golden", "common", "golden"), {}),
              (("golden", "paid", "golden"), {}), (("golden", "golden", "golden"), dict(markets=(1, 2))),
              (("golden", "golden", "golden"), dict(markets=(0,))),
              (("golden", "flat", "golden"), {}), (("golden", "golden", "spend"), {}),
              (("golden", "golden", "budget"), {}), (("golden", "golden", "iv"), {}),
              (("golden", "golden", "average"), {}), (("prop_month", "bridge", "spend"), {}),
              (("prop_month", "ratio", "spend"), {}), (("raw", "direct", "average"), {})]
    print("%-46s" % "route" + "".join("%10s" % short(c) for c in ORDER))
    print("%-46s" % "truth at plan" + "".join("%10.3f" % T[c]["roas"] for c in ORDER))
    for r, kw in routes:
        res = route(O, *r, **kw)
        nm = "/".join(r) + ((" web-read" if kw.get("webq") else " " + str(kw)) if kw else "")
        print("%-46s" % nm + "".join("%10.3f" % res[c]["roas"] for c in ORDER))
        if (r, kw) != routes[0]:
            print("%-46s" % "   over golden" + "".join("%+10.3f" % (res[c]["roas"] / g[c]["roas"] - 1) for c in ORDER))
            print("%-46s" % "   paid per install over golden" + "".join("%+10.3f" % (res[c]["v12"] / g[c]["v12"] - 1) for c in ORDER))
    print("variants, return per euro over golden")
    spread = {c: 0.0 for c in ORDER}; spm = {c: 0.0 for c in ORDER}; spv = {c: 0.0 for c in ORDER}
    for (nm, kw), res in zip(VARIANTS, X["fam"]):
        print("%-46s" % ("  " + nm)[:46] + "".join("%+10.3f" % (res[c]["roas"] / g[c]["roas"] - 1) for c in ORDER))
        for c in ORDER:
            spread[c] = max(spread[c], abs(res[c]["roas"] / g[c]["roas"] - 1))
            spm[c] = max(spm[c], abs(res[c]["marginal"] / g[c]["marginal"] - 1))
            spv[c] = max(spv[c], abs(res[c]["v12"] / g[c]["v12"] - 1))
    print("%-46s" % "family spread, return" + "".join("%10.3f" % spread[c] for c in ORDER))
    print("%-46s" % "family spread, paid per install" + "".join("%10.3f" % spv[c] for c in ORDER))
    print("%-46s" % "family spread, next euro" + "".join("%10.3f" % spm[c] for c in ORDER))
    for nm, f in (("v12", lambda c, ci: tv[(W["src"] == ci) & O.mature].mean()),
                  ("unrec", lambda c, ci: 1 - rec[(W["src"] == ci) & O.mature].sum() / tv[(W["src"] == ci) & O.mature].sum()),
                  ("installs_week", lambda c, ci: T[c]["installs_week"]), ("vpi", lambda c, ci: T[c]["vpi"]),
                  ("marginal", lambda c, ci: T[c]["marginal"]), ("el", lambda c, ci: T[c]["el"]),
                  ("qs", lambda c, ci: T[c]["qs"])):
        print("%-46s" % ("truth " + nm) + "".join("%10.3f" % f(c, ci) for ci, c in enumerate(ORDER)))
        print("%-46s" % ("golden " + nm) + "".join("%10.3f" % g[c][nm] for c in ORDER))
    print("adding up (the unattributed accounts' revenue as priced over as paid): bridge %.3f, Apple Search Ads' "
          "ratio %.3f, fitted %.3f" % (adding_up(O, v, "bridge"), adding_up(O, v, "ratio"), adding_up(O, v)))
    for r, s_ in zip(X["refs"], X["sep"]):
        print("referee: %s%s\n    truth %.4g golden %.4g rivals %s  (weakest rival's error over golden's: %.1f)" % (
            r["slice"], (" (n %d)" % r["n"]) if "n" in r else "", r["truth"], r["golden"],
            {k: round(x, 4) for k, x in r["rivals"].items()}, s_))
        if r.get("other"):
            print("    also:", {k: round(x, 4) for k, x in r["other"].items()})
    import corelib
    lat = {corelib._key(k.split("+")): x for k, x in spec["lattice"].items()}
    figs, _p = corelib._figures(spec, lat)
    gcall = corelib._calls(spec, {m: spec["members"][m]["golden"] for m in spec["members"]})
    names = sorted(spec["members"])
    print("every shortcut on the rubric, the other two steps golden (the checker prices the first of each step):")
    for step, alts in (("S1", [("the stores' true-up month by month", ("prop_month", "golden", "golden"), {}),
                               ("one true-up factor per store", ("prop", "golden", "golden"), {}),
                               ("the records as they stand", ("raw", "golden", "golden"), {}),
                               ("candidates carried at the cancellations the app saw", ("awake", "golden", "golden"), {}),
                               ("candidates carried at the web checkout's continuation", ("golden", "golden", "golden"), dict(webq=True))]),
                       ("S2", [("every postback at the named installs' value", ("golden", "bridge", "golden"), {}),
                               ("the named installs alone", ("golden", "consenters", "golden"), {}),
                               ("Apple Search Ads' ratio", ("golden", "ratio", "golden"), {}),
                               ("the ratio its kind of network shows on Android", ("golden", "analogue", "golden"), {}),
                               ("one ratio for every source", ("golden", "common", "golden"), {}),
                               ("organic at Apple Search Ads' ratio, one for the networks", ("golden", "paid", "golden"), {}),
                               ("the unattributed accounts' own value", ("golden", "flat", "golden"), {}),
                               ("fitted, the four social networks sharing one ratio", ("golden", "golden", "golden"), dict(group="kind")),
                               ("fitted, Meta, TikTok and Snapchat sharing one ratio", ("golden", "golden", "golden"), dict(group="social")),
                               ("fitted, Meta and TikTok sharing one ratio", ("golden", "golden", "golden"), dict(group="pair")),
                               ("fitted, TikTok and Snapchat sharing one ratio", ("golden", "golden", "golden"), dict(group="pair2"))]),
                       ("S3", [("the response fitted on spend", ("golden", "golden", "spend"), {}),
                               ("the two years' average return", ("golden", "golden", "average"), {})])):
        for nm, r, kw in alts:
            res = route(O, *r, **kw)
            vals = figure_values(res)
            call = corelib._calls(spec, {m: res[m]["roas"] for m in names})
            wrong = [short(m) for m, a, b in zip(names, call, gcall) if a != b]
            comp = {k: corelib._earned([f for f in figs if f["id"] == fid][0], vals[fid]) for k, fid in COMPONENTS.items()}
            print("    %s %-58s earns %4.1f  wrong on %-22s components kept %s" % (
                step, nm, corelib._score(figs, call == gcall, lambda f: vals[stated_id(f["id"])]), ", ".join(wrong) or "none",
                " ".join(k for k, ok in comp.items() if ok)))
    print("could networks share a ratio (the fitted ratios' differences against the fit's own spread; the 5 per cent"
          " points are 3.84, 5.99, 7.81 and 9.49 on one to four degrees of freedom):")
    for nms in (("Meta iOS", "TikTok iOS"), ("TikTok iOS", "Snapchat iOS"), ("Meta iOS", "TikTok iOS", "Snapchat iOS"),
                ("Meta iOS", "TikTok iOS", "Snapchat iOS", "Pinterest iOS"),
                ("Meta iOS", "TikTok iOS", "Snapchat iOS", "Google iOS", "Pinterest iOS"),
                ("Google iOS", "Pinterest iOS"), ("Google iOS", "Pinterest iOS", "organic iOS"),
                ("Pinterest iOS", "organic iOS"), ("Google iOS", "organic iOS"), ("Snapchat iOS", "Pinterest iOS")):
        st, d = s2_equal_test(O, v, nms)
        print("    %-58s %6.1f on %d   %s" % (", ".join(short(x) for x in nms), st, len(nms) - 1,
                                             "  ".join("%s %.3f (%.3f)" % (short(k), a, b) for k, (a, b) in d.items())))
    print("each call with its own fitted ratio moved a fifth either way (the return at the plan's spend):")
    for c in GATED:
        ci = ORDER.index(c)
        S, T2 = s2_strata(O, v), s2_cells(O, v)
        r0 = s2_fit(O, v)[ci]
        n, nc, vc = T2["n"][ci], np.maximum(S["nc"][ci].sum((0, 1)), 0), T2["vc"][ci]
        base = float((n * vc + nc * vc * r0).sum())
        lo, hi = [float((n * vc + nc * vc * r0 * f).sum()) / base * g[c]["roas"] for f in (0.8, 1.2)]
        print("    %-18s fitted %.3f   %.3f  %.3f  %.3f" % (c, r0, lo, g[c]["roas"], hi))
    print("forcing: each fitted input moved a fifth either way (the delivery share by its widest quarter, %.3f); the "
          "return at the plan's spend:" % quarter_departure(O))
    print("%-62s" % "" + "".join("%9s" % short(c) for c in MEMBERS))
    for nm, fac, vals, ok in forcing(O):
        print("    %-52s x%.3f" % (nm[:52], fac) + "".join("%9.3f" % vals[c] for c in MEMBERS) + ("  holds" if ok else "  MOVES"))
    print("two stumps lost, the call and what is left:")
    for k in ("S1+S2", "S1+S3", "S2+S3"):
        print("   ", k, " ".join("%s %.3f" % (short(c), X["lat"][k][c]["roas"]) for c in ORDER))
    live = np.array([[CH[c]["live"][m].mean() for m in range(3)] for c in ORDER])
    print("share of weeks live by market (ES, IT, PT):", " | ".join("%s %s" % (short(c), " ".join("%.2f" % x for x in live[i]))
                                                                  for i, c in enumerate(ORDER)))


def seeds(n=4):
    """the fitted ratios on other draws of the same world: how far the second step's fit moves by chance"""
    for k in range(n):
        W = simulate(SEED + 1000 * (k + 1))
        O = Obs(W)
        v = values(O)
        tr = true_ratios(O, v, W, True); fi = s2_fit(O, v)
        ta = true_ratios(O, v, W, False); fa = s2_fit(O, v, ios=False)
        print("seed %d iOS " % k + " ".join("%s %.2f/%.2f" % (SOURCES[i][:6], fi[i], tr[i]) for i in sorted(fi)) +
              " | Android " + " ".join("%s %.2f/%.2f" % (SOURCES[i][:8], fa[i], ta[i]) for i in sorted(fa)))
        _CACHE.clear(); _S2.clear()


if __name__ == "__main__":
    if "--explore" in sys.argv:
        explore()
        sys.exit(0)
    if "--seeds" in sys.argv:
        seeds()
        sys.exit(0)
    import corelib
    sys.exit(corelib.run(build_spec()))
