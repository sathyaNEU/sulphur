#!/usr/bin/env python3
"""task1, the core: Zancada's paid channels for 2027, proved on arrays before any pack exists.

The world's observation process, the truth, the golden estimator, every shortcut route, the variant battery, the
referee slices and the graded figures, ending on corelib.run(spec). Standard library and numpy only; nothing here
reads a prompt or solves a task. The generator imports the process from this file, so the pack carries what the core
proved.

    python3 task1/generator/core.py            # the core table and CORE PASS / CORE FAIL
    python3 task1/generator/core.py --explore  # the dials' diagnostics, while designing
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", ".claude", "skills", "stumping"))

SEED = 71116
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
CONSENT = dict(ios=-1.30, android=0.15, u=1.20, e=0.25)        # the tracking prompt's answer
CONV = dict(a=-1.15, e=1.00, u=0.55)                           # trial to paid at day 7
DORMANT0 = dict(a=-2.00, e=0.45, u=0.60)                       # the chance of never opening again after the trial week
DORMANT = dict(a=-1.75, e=0.45, u=0.60, f=1.00)                # the monthly chance of never opening again, later
CHURN = dict(a=-2.40, e=0.45, u=0.60)                          # the monthly chance of cancelling while still opening
CHURN_SILENT = dict(a=-2.15, e=-0.10)                          # and once the app is no longer opened
# the ad platforms' delivery: a campaign spends its weekly budget only as far as the week's auction lets it
KAPPA, LAMBDA, SIG_M, RHO_M, DBAR = 0.55, 1.00, 0.26, 0.25, 0.86

# channel: platform; complete (the channel is on file for every account, whatever the tracking answer); the people
# it brings (mean engagement, reachability, readiness to go quiet); installs a week at the reference weekly budget b0;
# the budget elasticity of installs; how fast a larger budget reaches into wider inventory; the 2027 plan's weekly
# spend over the norm; the team's budget moves (first week, weeks, factor)
SCALE = 2.0
CH = {
    "Meta iOS":         dict(ios=1, complete=0, mu=0.05,  nu=0.10, phi=0.35,  n=330, b0=3180, el=0.78, xs=0.35, plan=1.20, stretch=1.30),
    "TikTok iOS":       dict(ios=1, complete=0, mu=-0.30, nu=0.05, phi=0.60,  n=240, b0=2740, el=0.80, xs=0.35, plan=1.30, stretch=1.15),
    "Snapchat iOS":     dict(ios=1, complete=0, mu=-0.15, nu=0.08, phi=0.40,  n=200, b0=2720, el=0.76, xs=0.35, plan=1.30, stretch=1.15),
    "Google iOS":       dict(ios=1, complete=0, mu=0.10,  nu=0.10, phi=-1.30, n=260, b0=2030, el=0.70, xs=0.30, plan=1.25, stretch=1.35),
    "Pinterest iOS":    dict(ios=1, complete=0, mu=0.15,  nu=0.12, phi=-1.20, n=160, b0=1320, el=0.74, xs=0.30, plan=0.75, stretch=1.75),
    "Apple Search Ads": dict(ios=1, complete=1, mu=0.60,  nu=0.15, phi=-0.80, n=140, b0=1390, el=0.62, xs=0.30, plan=1.40, stretch=1.00),
    "Google Android":   dict(ios=0, complete=1, mu=0.00,  nu=0.10, phi=0.30,  n=420, b0=5690, el=0.66, xs=0.30, plan=0.60, stretch=1.25),
    "AppLovin Android": dict(ios=0, complete=1, mu=-0.55, nu=0.05, phi=1.10,  n=500, b0=3280, el=0.82, xs=0.30, plan=0.75, stretch=1.75),
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


for _i, _c in enumerate(ORDER):
    CH[_c]["pushes"] = budget_moves(_i)
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


def budgets(seed=SEED):
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
        out[c] = dict(xb=budget / norm, m=m, d=d, budget=budget, spend=np.round(budget * d, 2))
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


def life(rng, e, u, f, day, end_day):
    """each install's first two days, trial, plan, billing route, charges and the app's last open"""
    n = e.size
    sess = np.clip(np.round(np.exp(0.9 + 0.55 * e + rng.normal(0, 0.35, n))), 0, 40).astype(int)
    trial = rng.random(n) < lg(-0.35 + 1.05 * e + rng.normal(0, 0.4, n))
    paid48 = (~trial) & (rng.random(n) < lg(-3.4 + 1.0 * e))
    conv = np.where(trial, rng.random(n) < lg(CONV["a"] + CONV["e"] * e + CONV["u"] * u), paid48)
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
        h = np.where(awake, lg(CHURN["a"] - CHURN["e"] * e - CHURN["u"] * u),
                     lg(CHURN_SILENT["a"] - CHURN_SILENT["e"] * e))
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
    auto_on = np.where(sub, ~(cancelled_awake & (rng.random(n) < 0.8)), annual & ~(dorm >= 12))
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


def simulate(seed=SEED):
    """every account of the 104 install weeks, flattened; src indexes SOURCES"""
    B = budgets(seed)
    parts = []
    for si, c in enumerate(SOURCES):
        rng = np.random.default_rng([seed, 2, si])
        p = CH.get(c) or ORGANIC[c]
        es, us, fs, ds, ws, wd = [], [], [], [], [], []
        for w in range(WEEKS):
            if c in CH:
                e, u, f, wide = draw_week(rng, p, WMONTH[w], B[c]["xb"][w], B[c]["m"][w])
            else:
                e, u, f, wide = draw_week(rng, p, WMONTH[w])
            es.append(e); us.append(u); fs.append(f); wd.append(wide)
            ds.append(w * 7 + rng.integers(0, 7, e.size)); ws.append(np.full(e.size, w))
        e = np.concatenate(es); u = np.concatenate(us); f = np.concatenate(fs); d = np.concatenate(ds)
        L = life(rng, e, u, f, d, END_DAY)
        L["week"] = np.concatenate(ws); L["wide"] = np.concatenate(wd)
        L["src"] = np.full(e.size, si)
        L["country"] = rng.choice(3, e.size, p=COUNTRY_SHARE)
        L["ios"] = np.full(e.size, bool(p["ios"]))
        L["consent"] = consent_of(rng, e, u, L["ios"])
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
            e = np.concatenate(es); wide = np.concatenate(wd)
            L = life(rng, e, np.concatenate(us), np.concatenate(fs), np.concatenate(ds), 10 ** 6)
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

class Obs:
    """the pack's content as arrays: nothing below reads a person's traits, the wide flag, the auction's state or an
    unlabelled account's source"""

    def __init__(self, W):
        n = W["e"].size
        self.n = n
        self.week, self.day, self.country, self.ios, self.cv = W["week"], W["day"], W["country"], W["ios"], W["cv"]
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
        # first-48-hour value, dated three or four days after the install
        self.agg, self.agg_cv = {}, {}
        for ci, c in enumerate(ORDER):
            mk = W["src"] == ci
            if not CH[c]["complete"]:
                wk = np.clip((W["day"][mk] + W["pb_lag"][mk] - 3) // 7, 0, WEEKS - 1)
                t = np.zeros((WEEKS, 32))
                np.add.at(t, (wk, self.cv[mk]), 1)
                self.agg_cv[c] = t
                self.agg[c] = t.sum(1)
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


def s1_values(O, how="golden", split="store", trim=0, form="geo", cadence=MONTH_DAYS, fits=None):
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
        add[fi] += np.where(mon, f["c_m"] * O.netm[fi], f["c_a"] * O.neta[fi])
        bought[fi] += np.where(mon, f["c_m"], f["c_a"])
        for j in range(1, K):
            d = te + np.round(cadence * j).astype(int)
            add[fi] += mon * f["c_m"] * wt(j) * O.netm[fi] * ((d < wend[fi]) & (d <= END_DAY))
    return rec + add, bought


# --------------------------------------------------------------------------------------------------------------
# S2: the installs the attribution export does not hold
# --------------------------------------------------------------------------------------------------------------

LEVELS = {"one": 1, "tier2": 2, "tier4": 4, "tier8": 8}


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


def _cells(cv, cells):
    return np.asarray(cv) if cells == "fine" else tier(cv, LEVELS[cells])


_S2 = {}


def s2_cells(O, v, cells="fine", minn=20, tilt="cell"):
    """the iOS installs of the mature weeks by first-48-hour cell: each source's consenting installs and what they
    were worth, each network's non-consenting installs (its postbacks less its consenting installs), the organic
    non-consenting installs (the unattributed accounts less the networks'), the unattributed accounts' revenue, and
    the ratio that makes the non-consenting installs add up to it"""
    k = (id(O), id(v), cells, minn, tilt)
    if k in _S2:
        return _S2[k][0]
    key = _cells(O.cv, cells)
    key32 = _cells(np.arange(32), cells)
    nk = int(key32.max()) + 1
    mat = O.mature & O.ios
    org = len(ORDER)                                             # organic iOS in SOURCES
    cons = mat & np.isin(O.label, [ORDER.index(c) for c in GATED] + [org])
    ref_n = np.bincount(key[cons], minlength=nk)
    ref_v = np.bincount(key[cons], weights=v[cons], minlength=nk)
    ref = np.where(ref_n >= minn, ref_v / np.maximum(ref_n, 1), v[cons].mean())
    T = dict(key32=key32, nk=nk, n={}, vc={}, A={}, nc={})
    for si in [ORDER.index(c) for c in ORDER if CH[c]["ios"]] + [org]:
        lab = mat & (O.label == si) & O.consent
        n = np.bincount(key[lab], minlength=nk).astype(float)
        tot = np.bincount(key[lab], weights=v[lab], minlength=nk)
        tl = tot.sum() / max((n * ref).sum(), 1e-9)              # the source's consenting installs over the reference
        own = (n >= minn) if tilt == "cell" else np.zeros(nk, bool)
        T["n"][si], T["vc"][si] = n, np.where(own, tot / np.maximum(n, 1), ref * tl)
    pool = mat & O.pool
    T["pool_n"] = np.bincount(key[pool], minlength=nk).astype(float)
    T["pool_v"] = np.bincount(key[pool], weights=v[pool], minlength=nk)
    rest = T["pool_n"].copy()
    for c in GATED:
        ci = ORDER.index(c)
        A = np.bincount(key32, weights=O.agg_cv[c][:MATURE].sum(0), minlength=nk)
        T["A"][ci] = A
        T["nc"][ci] = np.maximum(A - T["n"][ci], 0)
        rest -= T["nc"][ci]
    T["nc"][org] = np.maximum(rest, 0)
    den = sum(T["nc"][si] * T["vc"][si] for si in T["nc"])
    T["r"] = np.where((den > 0) & (T["pool_n"] >= minn), T["pool_v"] / np.maximum(den, 1e-9),
                      T["pool_v"].sum() / den.sum())
    T["flat"] = np.where(T["pool_n"] >= minn, T["pool_v"] / np.maximum(T["pool_n"], 1),
                         T["pool_v"].sum() / T["pool_n"].sum())
    _S2[k] = (T, v)
    return T


def asa_ratio(O, v, cells="fine", rcells="tier2"):
    """on Apple Search Ads, whose every account carries its channel: the non-consenting installs' value over the
    consenting ones', by coarse cell, laid on the pricing cells"""
    lab = (O.label == ORDER.index("Apple Search Ads")) & O.mature
    key = _cells(O.cv, rcells)
    k32, rk = _cells(np.arange(32), cells), _cells(np.arange(32), rcells)
    out = np.full(int(rk.max()) + 1, v[lab & ~O.consent].mean() / v[lab & O.consent].mean())
    for k in range(out.size):
        a, b = lab & (key == k) & ~O.consent, lab & (key == k) & O.consent
        if a.sum() >= 200 and b.sum() >= 200 and v[b].mean() > 0:
            out[k] = v[a].mean() / v[b].mean()
    return np.array([out[int(np.bincount(rk[k32 == k]).argmax())] for k in range(int(k32.max()) + 1)])


def ios_price(O, v, c, how="golden", cells="fine", minn=20, tilt="cell", rcells="tier2"):
    """the value of one install of an iOS network by its first-48-hour cell: the consenting installs at their own
    value, the rest at the value the route gives them; returns (each of the 32 values' cell, the price per cell, the
    installs per cell over the mature weeks)"""
    T = s2_cells(O, v, cells, minn, tilt)
    ci = ORDER.index(c)
    vc, n, nc = T["vc"][ci], T["n"][ci], T["nc"][ci]
    if how == "bridge":                                            # every postback at the consenting installs' value
        vn = vc
    elif how == "flat":                                            # at the unattributed accounts' value, any source
        vn = T["flat"]
    elif how == "ratio":                                           # at Apple Search Ads' ratio
        vn = vc * asa_ratio(O, v, cells, rcells)
    else:                                                          # at the ratio the unattributed accounts add up to
        vn = vc * T["r"]
    tot = n + nc
    return T["key32"], np.where(tot > 0, (n * vc + nc * vn) / np.maximum(tot, 1e-9), vc), tot


def channel_values(O, v, how="golden", cells="fine", minn=20, tilt="cell", rcells="tier2"):
    """each channel's twelve-month net revenue per install over every install it bought in the 52 mature weeks"""
    out = {}
    for ci, c in enumerate(ORDER):
        lab = (O.label == ci) & O.mature
        if CH[c]["complete"] or how == "consenters":
            out[c] = float(v[lab].mean())
        elif how == "direct":
            out[c] = float(v[lab].sum() / O.agg[c][:MATURE].sum())
        else:
            _k, price, tot = ios_price(O, v, c, how, cells, minn, tilt, rcells)
            out[c] = float((tot * price).sum() / tot.sum())
    return out


def adding_up(O, v, how="golden", cells="fine", rcells="tier2"):
    """the unattributed iOS accounts' twelve-month revenue as a route prices it (the networks' non-consenting
    installs and the organic ones) over what those accounts paid"""
    T = s2_cells(O, v, cells)
    f = {"bridge": np.ones(T["nk"]), "ratio": asa_ratio(O, v, cells, rcells)}.get(how, T["r"])
    return float(sum((T["nc"][si] * T["vc"][si] * f).sum() for si in T["nc"]) / T["pool_v"].sum())


# --------------------------------------------------------------------------------------------------------------
# S3: what the plan's weekly spend buys
# --------------------------------------------------------------------------------------------------------------

def weekly_quality(O, v, c, how="golden", s2="golden", cells="fine", minn=20, tilt="cell"):
    """the channel's value per install by install week, on a record that sees the whole week's installs: each week's
    installs priced by first-48-hour value at what that value was worth over the mature weeks (every week), or, for a
    channel whose every account carries it, the mature weeks' own twelve-month values"""
    ci = ORDER.index(c)
    lab = O.label == ci
    if not CH[c]["complete"]:
        how2 = {"consenters": "bridge", "direct": "golden"}.get(s2, s2)
        k32, price, _A = ios_price(O, v, c, how2, cells, minn, tilt)
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
             minn=20, qpool=False, leave=(), tilt="cell"):
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
            y = O.agg[c] if nm == "i" else weekly_quality(O, v, c, quality, s2, cells, minn, tilt)
            lo, hi = weeks_i if nm == "i" else (0, WEEKS)
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


def at_plan(O, coef, c, v12, dbar_weeks=WEEKS):
    """installs a week and value per install at the plan's 2027 weekly spend and at the stretch column's, the return
    per euro at each, and what the next euro returns at the plan"""
    ci = ORDER.index(c)
    Bc = O.B[c]
    sp = plan_spend(c)
    if coef["how"] in ("spend", "iv"):
        x_hist = np.log(Bc["spend"]) - np.log(Bc["spend"]).mean()
        x_plan = np.log(sp) - np.log(Bc["spend"]).mean()
    else:                                                          # the budget that delivers the plan's spend
        dbar = Bc["spend"][:dbar_weeks].sum() / Bc["budget"][:dbar_weeks].sum()
        x_hist = np.log(Bc["budget"]) - np.log(Bc["budget"]).mean()
        x_plan = np.log(sp / dbar) - np.log(Bc["budget"]).mean()
    si, sv = coef["i"]["s"][ci], coef["v"]["s"][ci]
    mi, mv = coef["i"]["mon"][ci], coef["v"]["mon"][ci]
    back = O.agg[c].sum() / np.exp(coef["i"]["a"][ci] + si * x_hist + mi[WMONTH - 1]).sum()
    fm = np.exp(sv * x_hist[:MATURE] + mv[WMONTH[:MATURE] - 1])
    wt = O.agg[c][:MATURE]
    level = v12 / ((fm * wt).sum() / wt.sum())                    # the fitted value over the mature weeks is v12
    out = {}
    for tag, lift in (("", 0.0), ("_s", float(np.log(CH[c]["stretch"])))):
        n = back * np.exp(coef["i"]["a"][ci] + si * (x_plan + lift) + mi[PLAN_MONTH - 1])
        vp = level * np.exp(sv * (x_plan + lift) + mv[PLAN_MONTH - 1])
        out["roas" + tag] = (n * vp).sum() / (sp.sum() * np.exp(lift))
        out["revenue" + tag] = (n * vp).sum()
        if not tag:
            out.update(installs_week=n.mean(), vpi=(n * vp).sum() / n.sum())
    out.update(marginal=out["roas"] * (si + sv), el=si, qs=sv)
    return out


# --------------------------------------------------------------------------------------------------------------
# a route: every channel's figures under one set of choices
# --------------------------------------------------------------------------------------------------------------

_CACHE = {}


def values(O, s1="golden", **kw):
    k1 = (id(O), "v", s1) + tuple(kw.get(k) for k in ("split", "trim", "form", "cadence", "webq"))
    if k1 not in _CACHE:
        fits = None
        if kw.get("webq") and s1 == "golden":
            fits = s1_fit(O)
            q = s1_web_fit(O)
            for f in fits.values():
                f["q"] = f["q1"] = q
        _CACHE[k1] = s1_values(O, s1, split=kw.get("split", "store"), trim=kw.get("trim", 0),
                               form=kw.get("form", "geo"), cadence=kw.get("cadence", MONTH_DAYS), fits=fits)[0]
    return _CACHE[k1]


def route(O, s1="golden", s2="golden", s3="golden", **kw):
    """every channel's figures under one route: s1 in raw, prop, prop_month, golden; s2 in direct, consenters,
    bridge, ratio, golden; s3 in average, spend, budget, iv, golden; kw carries a variant's conventions"""
    key = (id(O), s1, s2, s3, tuple(sorted(kw.items())))
    if key in _CACHE:
        return _CACHE[key]
    v = values(O, s1, **kw)
    cells, minn, tilt = kw.get("cells", "fine"), kw.get("minn", 20), kw.get("tilt", "cell")
    v12 = channel_values(O, v, s2, cells, minn, tilt)
    r12 = channel_values(O, values(O, "raw"), s2, cells, minn, tilt)
    N12 = {c: float(O.agg[c][:MATURE].sum()) for c in ORDER}
    res = {}
    if s3 == "average":                                            # the mature year's return per euro carried over
        for c in ORDER:
            n = O.agg[c][:MATURE].sum()
            r = v12[c] * n / O.B[c]["spend"][:MATURE].sum()
            res[c] = dict(v12=v12[c], rec12=r12[c] * N12[c], rev12=v12[c] * N12[c], unrec=1 - r12[c] / v12[c], roas=r,
                          vpi=v12[c], installs_week=n / 52.0,
                          marginal=r, revenue=r * plan_spend(c).sum(), roas_s=r,
                          revenue_s=r * plan_spend(c).sum() * CH[c]["stretch"], el=1.0, qs=0.0)
        _CACHE[key] = res
        return res
    coef = response(O, v, how=s3, months=kw.get("months", "pooled"), quality=kw.get("quality", "golden"),
                    weeks_i=kw.get("weeks_i", (0, WEEKS)), s2=s2, cells=cells, minn=minn, qpool=kw.get("qpool", False),
                    tilt=tilt)
    for c in ORDER:
        res[c] = dict(v12=v12[c], rec12=r12[c] * N12[c], rev12=v12[c] * N12[c], unrec=1 - r12[c] / v12[c],
                      **at_plan(O, coef, c, v12[c], kw.get("dbar_weeks", WEEKS)))
    _CACHE[key] = res
    return res


VARIANTS = [
    ("one fit across both stores", dict(split="pooled")),
    ("two-rate continuation", dict(form="two")),
    ("fit without the last two months", dict(trim=2)),
    ("thirty-day cadence", dict(cadence=30.0)),
    ("continuation read on the web subscribers", dict(webq=True)),
    ("first-48-hour cells in eight groups", dict(cells="tier8")),
    ("first-48-hour cells in four groups", dict(cells="tier4")),
    ("cells of fifty or more", dict(minn=50)),
    ("each source's consenting installs through one tilt", dict(tilt="one")),
    ("non-consenting installs at the unattributed accounts' value, whatever the network", dict(s2="flat")),
    ("non-consenting installs at Apple Search Ads' ratio", dict(s2="ratio")),
    ("each channel's own month pattern", dict(months="own")),
    ("installs response without the launch quarter", dict(weeks_i=(13, WEEKS))),
    ("value response on the mature weeks' own values", dict(quality="value")),
    ("one value slope across channels", dict(qpool=True)),
    ("delivery share from the mature weeks", dict(dbar_weeks=MATURE)),
    ("installs response on the last 78 weeks", dict(weeks_i=(26, WEEKS))),
    ("spend instrumented by the budget", dict(s3="iv")),
    ("the budget alone, the delivery left out", dict(s3="budget")),
]
HURRIED = {"S1": dict(s1="prop_month"), "S2": dict(s2="bridge"), "S3": dict(s3="spend")}


def lattice_route(O, lost):
    kw = {}
    for s in lost:
        kw.update(HURRIED[s])
    return route(O, **kw)


def band(x):
    return "cut" if x < LINES[0] else ("hold" if x < LINES[1] else "scale")


# --------------------------------------------------------------------------------------------------------------
# the referee slices: where the hidden quantity is on file, which the target does not reach
# --------------------------------------------------------------------------------------------------------------

def referee_s1(O, c="AppLovin Android"):
    """the web checkout's subscribers of one channel, whose every charge the backend holds: the net revenue charged
    after each one's last open, inside the first twelve months, per subscriber; and what each route would have put
    there had those charges been unseen"""
    ci = ORDER.index(c)
    idx, n_open = _web_silent(O, (O.label == ci) & O.mature)
    idx, n_open = idx[n_open >= 1], n_open[n_open >= 1]
    wend = O.day[idx] + 365
    after = O.true_charge[idx] & (O.rdays[idx] > O.last_open[idx][:, None]) & (O.rdays[idx] < wend[:, None])
    truth = (after.sum(1) * O.netm[idx]).sum() / idx.size
    f = s1_fit(O)[0 if not CH[c]["ios"] else 1]
    gold = np.zeros(idx.size)
    has = np.ones(idx.size, bool)
    last = O.rdays[idx, n_open - 1]
    for j in range(1, K):
        d = last + np.round(MONTH_DAYS * j).astype(int)
        gold += has * f["q"] ** j * O.netm[idx] * ((d < wend) & (d <= END_DAY) & (d > O.last_open[idx]))
    # the proportional true-up: each recorded charge scaled by its store-month's ratio of charged to recorded
    pl = int(CH[c]["ios"])
    mk = (O.ios == bool(pl)) & ~O.web
    st = O.store[pl]["first"] + O.store[pl]["ren"]
    rc = _monthly_counts(O, mk, "first") + _monthly_counts(O, mk, "ren")
    fac = np.where(rc > 0, st / np.maximum(rc, 1), 1.0)
    seen = O.true_charge[idx] & (O.rdays[idx] <= O.last_open[idx][:, None]) & (O.rdays[idx] < wend[:, None])
    prop = ((seen * (fac[np.minimum(O.mon[idx], O.NM - 1)] - 1)).sum(1) * O.netm[idx]).sum() / idx.size
    return dict(slice="the web checkout's %s subscribers: net revenue charged after the last open, per subscriber" % c,
                n=int(idx.size), truth=float(truth), golden=float(gold.sum() / idx.size), rivals={"proportional true-up": float(prop)})


def referee_s2(O, v):
    """Apple Search Ads' non-consenting installs, whose channel is on file: their twelve-month value per install, and
    what each route prices them at from their first-48-hour values alone"""
    ci = ORDER.index("Apple Search Ads")
    T = s2_cells(O, v)
    lab = (O.label == ci) & O.mature
    nc = lab & ~O.consent
    cnt = np.bincount(O.cv[nc], minlength=32).astype(float)
    est = lambda p: float((cnt * p).sum() / cnt.sum())
    return dict(slice="Apple Search Ads' non-consenting installs: twelve-month net revenue per install",
                n=int(nc.sum()), truth=float(v[nc].mean()), golden=est(T["vc"][ci] * T["r"]),
                rivals={"consenting installs' value by first-48-hour value": est(T["vc"][ci]),
                        "consenting installs' value": float(v[lab & O.consent].mean())},
                other={"the unattributed accounts' value by first-48-hour value": est(T["flat"])})


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


FAMILIES = [("return ", "roas"), ("stretch return ", "roas_s"), ("value at plan ", "vpi"), ("next euro ", "marginal")]
ANDROID = [c for c in MEMBERS if not CH[c]["ios"]]


def figure_values(res):
    """every graded figure a route files"""
    out = {}
    for c in MEMBERS:
        for nm, k in FAMILIES:
            out[nm + c] = res[c][k]
        out["unrecorded share " + c] = res[c]["unrec"]
    out["unrecorded share iOS networks"] = 1 - sum(res[c]["rec12"] for c in GATED) / sum(res[c]["rev12"] for c in GATED)
    out["value per install Meta iOS"] = res["Meta iOS"]["v12"]
    out["installs a week Google Android"] = res["Google Android"]["installs_week"]
    out["plan revenue"] = sum(res[c]["revenue"] for c in MEMBERS)
    out["plan revenue iOS networks"] = sum(res[c]["revenue"] for c in GATED)
    out["plan revenue Android"] = sum(res[c]["revenue"] for c in ANDROID)
    out["stretch revenue"] = sum(res[c]["revenue_s"] for c in MEMBERS)
    out["stretch adds"] = out["stretch revenue"] - out["plan revenue"]
    return out


COMPONENTS = ["unrecorded share AppLovin Android", "value per install Meta iOS", "stretch adds",
              "plan revenue iOS networks"]
CANDIDATES = ["unrecorded share iOS networks", "unrecorded share Meta iOS", "installs a week Google Android",
              "plan revenue", "plan revenue Android", "stretch revenue"]


def build_spec(W=None, verbose=False):
    W = W or simulate()
    O = Obs(W)
    T = truth_at_plan()
    g = route(O)
    fam = [route(O, **kw) for _nm, kw in VARIANTS]
    sids = ["S1", "S2", "S3"]
    keys = [["S1"], ["S2"], ["S3"], ["S1", "S2"], ["S1", "S3"], ["S2", "S3"], ["S1", "S2", "S3"]]
    lat_res = {"+".join(k): lattice_route(O, k) for k in keys}
    direct = route(O, "raw", "direct", "average")
    rigorous = lat_res["S1+S2+S3"]
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
        "S2": dict(axis="who", opens=OWN["S2"], steps_left=4, precedents=["L53", "N27", "L13"],
                   said_out_loud="The attribution export holds an iOS network's installs only where the user allowed "
                                 "tracking, and those users are worth more than the rest even at the same first two "
                                 "days; the rest sit among the accounts with no channel."),
        "S3": dict(axis="against", opens=OWN["S3"], steps_left=3, precedents=["L51", "L37", "L28"],
                   said_out_loud="A week's spend is what the platform chose to deliver of the week's budget given that "
                                 "week's auction, so weeks of high and low spend are not weeks of high and low "
                                 "budgets; what a budget buys shows in the weeks the team moved it."),
    }
    lattice = {k: {c: float(r[c]["roas"]) for c in MEMBERS} for k, r in lat_res.items()}
    gf = figure_values(g)
    ff = [figure_values(r) for r in fam]
    lf = {k: figure_values(r) for k, r in lat_res.items()}
    figures = []
    for c in MEMBERS:
        figures.append(dict(id="return " + c, block="ask", weight=1.0, member=c))
    for kind, _k in FAMILIES[1:]:
        for c in MEMBERS:
            fid = kind + c
            figures.append(dict(id=fid, block="ask", weight=1.0, golden=float(gf[fid]),
                                family=[float(x[fid]) for x in ff], lattice={k: float(x[fid]) for k, x in lf.items()},
                                routes=dict(rigorous=float(lf["S1+S2+S3"][fid]))))
    for fid in COMPONENTS + (CANDIDATES if "--candidates" in sys.argv else []):
        figures.append(dict(id=fid, block="component", weight=1.0, golden=float(gf[fid]),
                            family=[float(x[fid]) for x in ff], lattice={k: float(x[fid]) for k, x in lf.items()},
                            routes=dict(rigorous=float(lf["S1+S2+S3"][fid]))))
    v = values(O)
    refs = [referee_s1(O), referee_s2(O, v), referee_s3(O, v)]

    def sep(r):
        ge = abs(r["golden"] - r["truth"])
        return min(abs(x - r["truth"]) for x in r["rivals"].values()) / max(ge, 1e-12)
    weakest = min(refs, key=sep)
    spec = dict(call="lines", members=members, stumps=stumps, lattice=lattice,
                referee=dict(slice=weakest["slice"], covers_target=False, truth=weakest["truth"],
                             golden=weakest["golden"], rivals=weakest["rivals"]), figures=figures)
    if verbose:
        return spec, dict(O=O, W=W, T=T, g=g, fam=fam, lat=lat_res, direct=direct, refs=refs, sep=[sep(r) for r in refs])
    return spec


def explore():
    spec, X = build_spec(verbose=True)
    O, W, T, g = X["O"], X["W"], X["T"], X["g"]
    tv = value12(W)
    rec = values(O, "raw")
    short = lambda c: c.replace(" Android", " A").replace("Apple Search Ads", "ASA").replace("Snapchat", "Snap")[:9]
    print("accounts %d" % O.n)
    for ci, c in enumerate(SOURCES):
        mk = (W["src"] == ci) & O.mature
        print("  %-18s n %6d consent %.2f value %6.2f unrecorded %.2f  consenting/not %6.2f / %6.2f  buyers %.3f" % (
            c, mk.sum(), W["consent"][mk].mean(), tv[mk].mean(), 1 - rec[mk].sum() / tv[mk].sum(),
            tv[mk & W["consent"]].mean(), tv[mk & ~W["consent"]].mean(), (W["charge"][mk, 0] | W["a0"][mk]).mean()))
    for pl in (1, 0):
        mk = (O.ios == bool(pl)) & O.mature
        print("  platform ios=%d unrecorded %.3f" % (pl, 1 - rec[mk].sum() / tv[mk].sum()))
    print("fits", {k: {a: round(float(x), 3) for a, x in f.items()} for k, f in s1_fit(O).items()},
          "web continuation %.3f" % s1_web_fit(O))
    routes = [("golden", "golden", "golden"), ("prop_month", "golden", "golden"), ("prop", "golden", "golden"),
              ("raw", "golden", "golden"), ("golden", "bridge", "golden"), ("golden", "consenters", "golden"),
              ("golden", "ratio", "golden"), ("golden", "flat", "golden"), ("golden", "golden", "spend"),
              ("golden", "golden", "budget"), ("golden", "golden", "iv"), ("golden", "golden", "average"),
              ("prop_month", "bridge", "spend"), ("raw", "direct", "average")]
    print("%-46s" % "route" + "".join("%10s" % short(c) for c in ORDER))
    print("%-46s" % "truth at plan" + "".join("%10.3f" % T[c]["roas"] for c in ORDER))
    for r in routes:
        res = route(O, *r)
        print("%-46s" % "/".join(r) + "".join("%10.3f" % res[c]["roas"] for c in ORDER))
        if r != routes[0]:
            print("%-46s" % "   over golden" + "".join("%+10.3f" % (res[c]["roas"] / g[c]["roas"] - 1) for c in ORDER))
    print("variants, return per euro over golden")
    spread = {c: 0.0 for c in ORDER}; spm = {c: 0.0 for c in ORDER}
    for (nm, kw), res in zip(VARIANTS, X["fam"]):
        print("%-46s" % ("  " + nm) + "".join("%+10.3f" % (res[c]["roas"] / g[c]["roas"] - 1) for c in ORDER))
        for c in ORDER:
            spread[c] = max(spread[c], abs(res[c]["roas"] / g[c]["roas"] - 1))
            spm[c] = max(spm[c], abs(res[c]["marginal"] / g[c]["marginal"] - 1))
    print("%-46s" % "family spread, return" + "".join("%10.3f" % spread[c] for c in ORDER))
    print("%-46s" % "family spread, next euro" + "".join("%10.3f" % spm[c] for c in ORDER))
    for nm, f in (("v12", lambda c, ci: tv[(W["src"] == ci) & O.mature].mean()),
                  ("unrec", lambda c, ci: 1 - rec[(W["src"] == ci) & O.mature].sum() / tv[(W["src"] == ci) & O.mature].sum()),
                  ("installs_week", lambda c, ci: T[c]["installs_week"]), ("vpi", lambda c, ci: T[c]["vpi"]),
                  ("marginal", lambda c, ci: T[c]["marginal"]), ("el", lambda c, ci: T[c]["el"]),
                  ("qs", lambda c, ci: T[c]["qs"])):
        print("%-46s" % ("truth " + nm) + "".join("%10.3f" % f(c, ci) for ci, c in enumerate(ORDER)))
        print("%-46s" % ("golden " + nm) + "".join("%10.3f" % g[c][nm] for c in ORDER))
    sp = route(O, s3="spend")
    print("%-46s" % "spend route el" + "".join("%10.3f" % sp[c]["el"] for c in ORDER))
    print("%-46s" % "spend route marginal over golden" + "".join("%+10.3f" % (sp[c]["marginal"] / g[c]["marginal"] - 1) for c in ORDER))
    print("%-46s" % "prop_month unrec" + "".join("%10.3f" % route(O, "prop_month")[c]["unrec"] for c in ORDER))
    print("%-46s" % "bridge unrec" + "".join("%10.3f" % route(O, s2="bridge")[c]["unrec"] for c in ORDER))
    print("mean auction state by channel:", " ".join("%+.3f" % O.B[c]["m"].mean() for c in ORDER))
    v = values(O)
    print("adding up (the unattributed accounts' revenue as priced over as paid): bridge %.3f, Apple Search Ads' ratio %.3f" % (
        adding_up(O, v, "bridge"), adding_up(O, v, "ratio")))
    for r, s_ in zip(X["refs"], X["sep"]):
        print("referee: %s\n    truth %.4g golden %.4g rivals %s  (weakest rival's error over golden's: %.1f)" % (
            r["slice"], r["truth"], r["golden"], {k: round(x, 4) for k, x in r["rivals"].items()}, s_))
        if r.get("other"):
            print("    also:", {k: round(x, 4) for k, x in r["other"].items()})
    print("two stumps lost, the call and what is left:")
    for k in ("S1+S2", "S1+S3", "S2+S3"):
        print("   ", k, " ".join("%s %.3f" % (short(c), X["lat"][k][c]["roas"]) for c in ORDER))


if __name__ == "__main__":
    if "--explore" in sys.argv:
        explore()
        sys.exit(0)
    import corelib
    sys.exit(corelib.run(build_spec()))
