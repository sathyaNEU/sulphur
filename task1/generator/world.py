"""Zancada's world, simulated: installs bought by weekly budgets on seven channels (and organic), each install's
engagement, its first two days, iOS tracking consent, trials and plans, monthly renewals, when each subscriber stops
opening the app and how long they keep paying after it, and what the stores charged. The app's own records, the
attribution partner's export and the ad networks' postbacks are written from these in records.py."""
import numpy as np

import params as P

lg = lambda x: 1 / (1 + np.exp(-x))
SEASON_MU = {1: -0.12, 2: -0.05, 3: 0.0, 4: 0.02, 5: 0.03, 6: 0.0, 7: -0.04, 8: -0.06, 9: 0.05, 10: 0.04, 11: 0.02,
             12: -0.02}
SEASON_N = {1: 1.25, 2: 1.10, 3: 1.02, 4: 1.0, 5: 0.98, 6: 0.92, 7: 0.85, 8: 0.80, 9: 1.08, 10: 1.05, 11: 1.0, 12: 0.92}
SEASON_SPEND = P.SEASON_SPEND


def week_month(w):
    return P.day_date(w * 7 + 3).month


def budgets(rng):
    """each week's spend relative to the channel's seasonal norm (what the auction answers), and the euros billed"""
    ratio, euros = {}, {}
    for c, p in P.CHANNELS.items():
        x = 0.88 + 0.24 * rng.random(P.WEEKS)
        for w0, k, f in p["pushes"]:
            x[w0:w0 + k] *= f
        ratio[c] = x
        euros[c] = np.round(x * np.array([p["s0"] * SEASON_SPEND[week_month(w)] for w in range(P.WEEKS)]), -1)
    return ratio, euros


def draw_week(rng, c, p, w, x):
    """installs bought in week w at weekly spend x times the channel's seasonal norm: engagement and install days"""
    m = week_month(w)
    if x is None:
        n = rng.poisson(p["n"] * SEASON_N[m])
        e = rng.normal(p["mu"] + SEASON_MU[m], 1.0, n)
        wide = np.zeros(n, bool)
    else:
        n = rng.poisson(p["n"] * SEASON_N[m] * x ** p["el"])
        wide = rng.random(n) < np.clip(0.10 + p["xs"] * max(0.0, np.log(x)), 0, 0.85)
        e = rng.normal(p["mu"] + SEASON_MU[m], 1.0, n) - P.EXP_DROP * wide
    day = w * 7 + rng.integers(0, 7, n)
    return e, day, wide


def life(rng, e, day, ios, end_day):
    """each install's first two days, trial, plan, charges (store side) and the app's last open"""
    n = e.size
    sess = np.clip(np.round(np.exp(0.9 + 0.55 * e + rng.normal(0, 0.35, n))), 0, 40).astype(int)
    trial = rng.random(n) < lg(-0.35 + 1.05 * e + rng.normal(0, 0.4, n))
    paid48 = (~trial) & (rng.random(n) < lg(-3.4 + 1.0 * e))
    conv = np.where(trial, rng.random(n) < lg(-1.15 + 1.15 * e), paid48)
    choice = rng.random(n) < lg(-1.1 + 0.5 * e)          # the plan picked at the trial or purchase
    annual = conv & choice
    bucket = np.digitize(sess, [1, 2, 3, 5, 8, 12, 18])
    cv = bucket + 8 * trial + 16 * paid48
    conv_day = np.where(trial, day + 7, day + rng.integers(0, 2, n))
    # months awake after the first charge (the user opens the app in those months, then stops)
    dorm = rng.geometric(np.clip(lg(-1.7 - 1.0 * e), 0.01, 0.99)) - 1
    K = 26
    rdays = conv_day[:, None] + np.round(P.MONTH_DAYS * np.arange(K))[None, :].astype(int)
    charge = np.zeros((n, K), bool)
    active = conv & ~annual
    cancelled_awake = np.zeros(n, bool)
    last_paid = np.full(n, -1)
    for k in range(K):
        inwin = rdays[:, k] <= end_day
        charge[:, k] = active & inwin
        last_paid = np.where(charge[:, k], k, last_paid)
        awake = k < dorm
        h = np.where(awake, lg(-2.4 - 0.45 * e), lg(-2.15 + 0.10 * e))
        stop = active & (rng.random(n) < h)
        cancelled_awake |= stop & awake
        active = active & ~stop
    # annual: one charge, a renewal a year on
    a_charge0 = annual & (conv_day <= end_day)
    a_ren = annual & (conv_day + 365 <= end_day) & (rng.random(n) < np.where(dorm >= 12, 0.45, 0.72))
    # the app's last open
    lo = day + np.minimum(rng.geometric(0.16, n) - 1, 60)
    sub = conv & ~annual & (last_paid >= 0)
    still = sub & (charge[np.arange(n), np.maximum(last_paid, 0)]) & (rdays[np.arange(n), np.maximum(last_paid, 0)] + 30 > end_day)
    # dormant subscribers: last open inside the last awake month, before the next charge
    kd = np.minimum(dorm, np.maximum(last_paid, 0) + 1)          # the first month index not awake (or the end)
    base = np.where(kd >= 1, rdays[np.arange(n), np.maximum(kd - 1, 0)], day)
    lo_sub = base + rng.integers(0, 29, n)
    lo_sub = np.where(kd == 0, day + rng.integers(0, 7, n), lo_sub)          # never opened after the trial
    awake_end = sub & (dorm > last_paid) & still
    lo_sub = np.where(awake_end, end_day - rng.integers(0, 7, n), lo_sub)
    # subscribers who cancelled while awake open until their last paid month ends
    ca_lo = rdays[np.arange(n), np.maximum(last_paid, 0)] + rng.integers(0, 29, n)
    lo_sub = np.where(sub & cancelled_awake & (dorm > last_paid), ca_lo, lo_sub)
    lo = np.where(sub, lo_sub, lo)
    # annual subscribers: awake for dorm months after the charge
    lo_a = conv_day + np.minimum(dorm, 24) * 30 + rng.integers(0, 29, n)
    lo_a = np.where(dorm == 0, day + rng.integers(0, 7, n), lo_a)
    lo = np.where(annual, lo_a, lo)
    lo = np.minimum(np.maximum(lo, day), end_day)
    auto_on = np.where(sub, ~(cancelled_awake & (rng.random(n) < 0.8)), annual & ~(dorm >= 12))
    # a trial that did not convert: if the last open fell inside the trial, the app saw the plan and whether it was
    # still set to renew (cancelled after the last open, or not yet)
    in_trial = trial & ~conv & (lo < day + 7)
    auto_on = np.where(in_trial, rng.random(n) < 0.55, auto_on)
    plan_seen = np.where(annual, "annual", np.where(conv, "monthly", ""))
    plan_seen = np.where(in_trial, np.where(choice, "annual", "monthly"), plan_seen)
    # refunds: awake subscribers only, a few per cent of charges, recorded when the app next opens
    refund = charge & (rng.random(charge.shape) < 0.012) & (np.arange(K)[None, :] < dorm[:, None])
    return dict(e=e, day=day, sess=sess, trial=trial, paid48=paid48, conv=conv, annual=annual, cv=cv,
                conv_day=conv_day, dorm=dorm, rdays=rdays, charge=charge, refund=refund, a0=a_charge0, aren=a_ren,
                last_open=lo, auto_on=auto_on, sub=sub, plan_seen=plan_seen)


def value12(L, country_net, recorded=False):
    """each install's net revenue in its first 365 days (store side, or what the app recorded)"""
    n = L["e"].size
    win = L["rdays"] < (L["day"] + 365)[:, None]
    ch = L["charge"] & win
    rf = L["refund"] & win
    if recorded:
        seen = L["rdays"] <= L["last_open"][:, None]
        ch = ch & seen
        rf = rf & seen
    m = (ch.sum(1) - rf.sum(1)) * country_net["monthly"]
    a0 = L["a0"] & (L["conv_day"] < L["day"] + 365)
    if recorded:
        a0 = a0 & (L["conv_day"] <= L["last_open"])
    return m + a0 * country_net["annual"]


def simulate(seed=P.SEED):
    rng = np.random.default_rng(seed)
    X, B = budgets(rng)
    W = {"budgets": B, "ratio": X, "acc": {}}
    for c in list(P.CHANNELS) + list(P.ORGANIC):
        p = P.CHANNELS.get(c) or P.ORGANIC[c]
        es, ds, wides = [], [], []
        for w in range(P.WEEKS):
            e, d, wide = draw_week(rng, c, p, w, X[c][w] if c in P.CHANNELS else None)
            es.append(e); ds.append(d); wides.append(wide)
        e = np.concatenate(es); d = np.concatenate(ds); wide = np.concatenate(wides)
        order = np.argsort(d, kind="stable"); e, d, wide = e[order], d[order], wide[order]
        L = life(rng, e, d, p["ios"], P.END_DAY)
        L["wide"] = wide
        L["country"] = rng.choice(len(P.COUNTRIES), e.size, p=P.COUNTRY_SHARE)
        ca = p.get("ca")
        if p["ios"]:
            L["consent"] = rng.random(e.size) < lg((ca if ca is not None else P.CONSENT_OTHER) + P.CONSENT_SLOPE * e)
        else:
            L["consent"] = np.ones(e.size, bool)
        W["acc"][c] = L
    # the week of the pull (2 to 8 November 2026): installs keep coming, on a stream of their own
    r2 = np.random.default_rng(seed + 104)
    for c in list(P.CHANNELS) + list(P.ORGANIC):
        p = P.CHANNELS.get(c) or P.ORGANIC[c]
        x = None
        if c in P.CHANNELS:
            x = 0.88 + 0.24 * r2.random()
            X[c] = np.append(X[c], x)
            B[c] = np.append(B[c], round(x * p["s0"] * SEASON_SPEND[week_month(P.WEEKS)], -1))
        e, d, wide = draw_week(r2, c, p, P.WEEKS, x)
        L2 = life(r2, e, d, p["ios"], P.END_DAY)
        L2["week"] = np.full(e.size, P.WEEKS)
        L2["wide"] = wide
        L2["country"] = r2.choice(len(P.COUNTRIES), e.size, p=P.COUNTRY_SHARE)
        ca = p.get("ca")
        L2["consent"] = (r2.random(e.size) < lg((ca if ca is not None else P.CONSENT_OTHER) + P.CONSENT_SLOPE * e)) \
            if p["ios"] else np.ones(e.size, bool)
        L = W["acc"][c]
        W["acc"][c] = {k: (np.concatenate([L[k], L2[k]]) if k in L2 else L[k]) for k in L}
    return W


def net_table():
    return {k: {pl: P.net_of(P.PRICE[pl], k) for pl in P.PRICE} for k in P.COUNTRIES}


def truth_at_plan(seed=P.SEED + 777, reps=20):
    """the world's own 2027: each channel's installs bought week by week at the media plan's weekly spend, their
    twelve months as the stores charge them; net revenue per euro, installs per week and value per install"""
    rng = np.random.default_rng(seed)
    NT = net_table()
    weeks = P.plan_weeks()
    out = {}
    for c, p in P.CHANNELS.items():
        tv = ts = ni = 0.0
        for r in range(reps):
            for w, (mon, m, sp) in enumerate(weeks):
                x = sp[c] / (p["s0"] * SEASON_SPEND[m])
                n = rng.poisson(p["n"] * SEASON_N[m] * x ** p["el"])
                wide = rng.random(n) < np.clip(0.10 + p["xs"] * max(0.0, np.log(x)), 0, 0.85)
                e = rng.normal(p["mu"] + SEASON_MU[m], 1.0, n) - P.EXP_DROP * wide
                d = rng.integers(0, 7, n)
                L = life(rng, e, d, p["ios"], 10 ** 6)
                cn = rng.choice(len(P.COUNTRIES), n, p=P.COUNTRY_SHARE)
                for i, k in enumerate(P.COUNTRIES):
                    mk = cn == i
                    if mk.any():
                        sub = {kk: (vv[mk] if hasattr(vv, "__len__") and len(vv) == n else vv) for kk, vv in L.items()}
                        tv += value12(sub, NT[k]).sum()
                ts += sp[c]; ni += n
        out[c] = dict(roas=tv / ts, installs_week=ni / (52 * reps), vpi=tv / ni)
    return out
