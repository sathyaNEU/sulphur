#!/usr/bin/env python3
"""task9 architecture 4, the core: what each feature group's degraded service cost a ranking model's conversion.

Tessel Market's search ranking model reads seven feature groups, each built by its own job or service. Through the
third quarter of 2026 none of them went down outright; several ran degraded for weeks (feeds with gaps, batches that
failed on some days, a scoring job that failed a quarter of its runs). Search conversion drifted down and no
incident shows in it. The reliability charter puts a feature group on the 2027 tier one list where its degraded
service cost 0.05 points of search conversion or more over the quarter. No record holds what a group's degraded
service cost: conversion is attributed nightly and kept by day, and its daily swings are several times any one
group's cost. What the marketplace holds is its interpretability evidence, the online ablation tests (a group
withheld from the ranking model for a random slice of users), the incidence telemetry of each job, the logs of the
jobs and stores, the edge cache's record and the records of the other services that read the same groups.

The three stumps (each opens a different group, each leaves several dependent steps once said):
  S1 (what)  an ablation test withholds a group at the ranking model, and result pages come from a cache shared by
             every user. A held user handed a cached page gets the ranking built with the group. The measured effect
             is the full one scaled by the share of the held slice's page views built fresh, which the test record
             does not hold and the edge cache record does, by market, device and day (and it fell in June).
  S2 (when)  a value goes on being served for its validity period after its source fails and comes back only at the
             entity's next refresh. How often sources failed is not how much default was served: that turns on
             whether the same entities fail again and again, and is rebuilt entity by entity from the gap, batch,
             lag and scoring records, weighted by the traffic each entity carries, net of what normal service
             leaves at the default anyway.
  S3 (who)   the tests reach one reader of a group. Three groups are also read by a service that shows the shopper
             something (a promise badge, a price label, a buy-again strip), which loses the value in the same
             sessions. Its loss is in no ablation of the ranking model. It is in the reader's own render log and
             its own test.

The referee: in April the price batch failed to reach one of the two serving regions on seven nights. Users are
split between the regions by hash and each region has its own page cache, so a random half of the users lost the
price group outright, on every page and on every reader, for the hours the values had expired. The daily conversion
record by region measures what that cost; each route calls it from its own effect and its own hours. April is not
the third quarter and price is over the line on every route, so the slice rules between estimators and settles no
open group.

Run:  python3 task9/generator/core.py            the corelib verdict
      python3 task9/generator/core.py --detail   the world, every route, the rivals and the fitted inputs
      python3 task9/generator/core.py --forcing  the call under each fitted input moved by its measured spread
"""
import itertools
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", ".claude", "skills", "stumping"))
import corelib  # noqa: E402

SEED = int(os.environ.get("CORE_SEED", 9104))
DAYS = 273                            # 1 January to 30 September 2026
H = DAYS * 24
MONTH_START = (0, 31, 59, 90, 120, 151, 181, 212, 243, 273)
Q2 = (90, 181)
Q3 = (181, 273)
Q3_MONTHS = (("July", 181, 212), ("August", 212, 243), ("September", 243, 273))
LINE = 0.05                           # points of search conversion over the quarter: the charter's tier one line
MARKETS = ("DE", "NL", "SE", "BE", "AT", "DK")
MK_W = (0.36, 0.22, 0.12, 0.11, 0.10, 0.09)
APP = (0.58, 0.66, 0.71, 0.60, 0.55, 0.69)
DEVICES = ("app", "web")
CELLS = [(m, d) for m in range(6) for d in range(2)]
DAY_SESS = 1_200_000
GROUPS = ("stock", "promise", "price", "history", "trend", "seller", "match")
# v: points of conversion a session loses when the group reaches the ranking model as its default; pre: the group is
# built into the result page before the shared cache; e2, elig: the second reader's loss per eligible session and
# the share of sessions eligible; ttl: hours a value is served after its last refresh.
G = {
    "stock": dict(v=2.40, pre=False, e2=None, ttl=2.0),
    "promise": dict(v=0.55, pre=False, e2=1.10, elig=(0.60, 0.47), ttl=0.0),
    "price": dict(v=1.10, pre=True, e2=1.00, elig=(0.48, 0.40), ttl=36.0),
    "history": dict(v=1.30, pre=False, e2=0.90, elig=(0.55, 0.42), ttl=0.0),
    "trend": dict(v=0.90, pre=True, e2=None, ttl=6.0),
    "seller": dict(v=1.70, pre=True, e2=None, ttl=120.0),
    "match": dict(v=2.20, pre=True, e2=None, ttl=0.0),
}
READERS = ("promise", "price", "history")
HELD = 0.04                           # share of sessions in an ablation's held slice, and in its control slice
TEST_DAYS = 14
READER_TEST = {"promise": (12, 54), "price": (47, 89), "history": (124, 166)}
READER_HELD = 0.10
SUPP_BASE = 0.02                      # share of eligible sessions a reader fails to render for its own reasons
SPLIT = dict(group="price", days=(97, 99, 102, 104, 107, 110, 112))   # April: one serving region missed these batches
N_SELLERS = 8000
SELLER_WINDOW = (194, 267)
SELLER_FAIL = 0.27
CACHE_CHANGE = 159                    # 9 June: the page cache's lifetime raised
FRESH_GROUP, STATE_GROUP, READER_GROUP = "trend", "seller", "promise"


def cover(intervals, n=H):
    """Hour by hour, the fraction of the hour the intervals (in hours from the start) cover."""
    out = np.zeros(n)
    for s, e in intervals:
        s, e = max(s, 0.0), min(e, float(n))
        if e <= s:
            continue
        for h in range(int(np.floor(s)), int(np.ceil(e))):
            out[h] += min(e, h + 1.0) - max(s, float(h))
    return np.minimum(out, 1.0)


def merge(iv):
    out = []
    for s, e in sorted(iv):
        if out and s <= out[-1][1]:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return [(s, e) for s, e in out]


def ar1(rng, n, rho, sd):
    x = np.zeros(n)
    e = rng.normal(0, sd * np.sqrt(1 - rho ** 2), n)
    x[0] = rng.normal(0, sd)
    for i in range(1, n):
        x[i] = rho * x[i - 1] + e[i]
    return x


def make_world(seed=SEED):
    rng = np.random.default_rng(seed)
    hod, day = np.arange(H) % 24, np.arange(H) // 24
    dow = (day + 3) % 7               # 1 January 2026 is a Thursday
    W = dict(hod=hod, day=day, dow=dow)

    # ---- sessions
    diur = np.array([0.25, 0.16, 0.11, 0.09, 0.10, 0.18, 0.40, 0.75, 1.05, 1.20, 1.28, 1.38, 1.50, 1.42, 1.30, 1.25,
                     1.32, 1.50, 1.72, 1.95, 2.02, 1.70, 1.10, 0.57])
    diur = diur / diur.mean()
    wk = np.array([1.00, 0.97, 0.98, 1.01, 1.06, 1.07, 0.91])
    promo = np.zeros((6, DAYS), bool)
    for m in range(6):
        promo[m, rng.choice(DAYS, 13, replace=False)] = True
    sess = np.zeros((12, H))
    for c, (m, d) in enumerate(CELLS):
        share = APP[m] if d == 0 else 1 - APP[m]
        lam = (DAY_SESS * MK_W[m] * share / 24.0 * diur[hod] * wk[dow] * (1 + 0.0004 * day)
               * np.where(promo[m, day], 1.30, 1.0) * np.exp(rng.normal(0, 0.05, H)))
        sess[c] = rng.poisson(lam)
    W.update(sess=sess, promo=promo, diur=diur)

    # ---- healthy conversion, in points
    bump = np.clip((np.arange(DAYS) - 171) / 20.0, 0, 1) * np.clip((258 - np.arange(DAYS)) / 20.0, 0, 1)
    common = ar1(rng, DAYS, 0.5, 0.25)
    hourly = ar1(rng, H, 0.8, 0.15)
    base_m = (12.3, 12.6, 11.9, 12.1, 12.4, 12.0)
    p0 = np.zeros((12, H))
    for m in range(6):
        mk = ar1(rng, DAYS, 0.4, 0.30)
        for d in range(2):
            c = m * 2 + d
            p0[c] = (base_m[m] + (0.5 if d == 0 else -0.8) + 0.45 * np.sin((hod - 14) / 24.0 * 2 * np.pi)
                     + np.array([0.0, 0.05, 0.05, 0.1, 0.2, -0.15, -0.25])[dow] - 0.30 * bump[day]
                     + np.where(promo[m, day], 0.8, 0.0) + common[day] + mk[day] + hourly)
    W["p0"] = p0

    # ---- what each group is worth, cell by cell
    v, e2, elig = {}, {}, {}
    for j in GROUPS:
        mm = 1 + rng.uniform(-0.08, 0.08, 6)
        dm = (1.07 + rng.uniform(-0.02, 0.02), 0.90 + rng.uniform(-0.02, 0.02))
        v[j] = np.array([G[j]["v"] * mm[m] * dm[d] for m, d in CELLS])
        if G[j]["e2"]:
            e2[j] = np.array([G[j]["e2"] * (1 + rng.uniform(-0.05, 0.05)) for _ in CELLS])
            elig[j] = np.array([G[j]["elig"][d] + rng.uniform(-0.03, 0.03) for m, d in CELLS])
    W.update(v=v, e2=e2, elig=elig)

    # ---- the share of result pages built fresh (not handed from the shared cache), cell by day
    u = np.zeros((12, DAYS))
    purge = rng.choice(DAYS, 9, replace=False)
    for c, (m, d) in enumerate(CELLS):
        off = rng.uniform(-0.04, 0.04)
        lvl = np.where(np.arange(DAYS) < CACHE_CHANGE, (0.60, 0.44)[d], (0.44, 0.30)[d])
        u[c] = np.clip(lvl + off + rng.normal(0, 0.015, DAYS), 0.05, 0.97)
        u[c, purge] = np.clip(u[c, purge] + 0.22, 0, 0.97)
    W["u"] = u

    E, S, logs = {}, {}, {}

    # ---- stock: fourteen chain feeds with gaps; a store's snapshot is served two hours after its last sync
    K = 14
    Wc = np.zeros((6, K))
    homes = {0: (0, 1, 2, 12), 1: (3, 4, 5), 2: (6, 7, 13), 3: (3, 8, 9), 4: (0, 10, 11), 5: (6, 12, 13)}
    big = {0: (0, 0.46), 1: (3, 0.44), 2: (6, 0.40), 3: (9, 0.35), 4: (11, 0.36), 5: (6, 0.30)}
    for m, ks in homes.items():
        w = rng.dirichlet(np.full(len(ks), 3.0)) * (1 - big[m][1])
        for k, x in zip(ks, w):
            Wc[m, k] += x
        Wc[m, big[m][0]] += big[m][1]
    migrating = (0, 3, 6, 9, 11)
    unavail, default_c, default_true, gaps = np.zeros((K, H)), np.zeros((K, H)), np.zeros((K, H)), []
    gateway = []                      # the new feed gateway the five migrating chains share: its stalls hit all five
    for dd in range(186, 263):
        for _ in range(rng.poisson(2.1)):
            s = dd * 24 + rng.uniform(0, 24)
            gateway.append((s, s + min(rng.lognormal(np.log(1.15), 0.9), 30.0)))
    for k in range(K):
        iv = [(s + rng.uniform(0, 0.2), e + rng.uniform(0, 0.3)) for s, e in gateway] if k in migrating else []
        for dd in range(DAYS):
            mig = k in migrating and 186 <= dd < 263
            for _ in range(rng.poisson(0.7 if mig else 0.22)):
                s = dd * 24 + rng.uniform(0, 24)
                iv.append((s, s + min(rng.lognormal(np.log(1.0 if mig else 0.8), 0.9 if mig else 1.0), 30.0)))
        iv = merge(iv)
        gaps += [(k, s, e) for s, e in iv]
        unavail[k] = cover(iv)
        default_c[k] = cover([(s + 2.0 - 0.125, e + 0.125) for s, e in iv if e - s > 2.0 - 0.125])
        tr = []
        for s, e in iv:
            a, r = rng.uniform(0, 0.25), rng.uniform(0, 0.25)
            if e - s > 2.0 - a:
                tr.append((s + 2.0 - a, e + r))
        default_true[k] = cover(tr)
    E["stock"] = np.array([Wc[m] @ default_true for m, d in CELLS])
    S["stock"] = np.array([Wc[m] @ unavail for m, d in CELLS])
    logs["stock"] = dict(Wc=Wc, gaps=gaps, unavail=unavail, default_c=default_c)

    # ---- promise: one service for every market, a share of its calls failing
    lvl = np.full(DAYS, 0.003)
    lvl[200:] = np.clip(0.055 + ar1(rng, DAYS - 200, 0.85, 0.008), 0.02, 0.11)
    err = np.clip(lvl[day] * np.sqrt(diur[hod]) / np.sqrt(diur).mean(), 0, 0.5)
    E["promise"] = S["promise"] = np.tile(err, (12, 1))

    # ---- price: five sources, one batch a day at 04:00, a price served 36 hours after its batch
    NS = 5
    Ws = np.zeros((6, NS))
    for m in range(6):
        Ws[m] = rng.dirichlet(np.array([6.0, 4.8, 3.6, 3.0, 2.6]))
    ok = rng.random((NS, DAYS)) > 0.03
    prev = False
    for dd in range(188, 228):
        prev = rng.random() < (0.75 if prev else 0.35)
        ok[0, dd] = not prev
    ok[1, 181:273] = rng.random(92) > 0.12
    ok[:, SPLIT["days"][0] - 3:SPLIT["days"][-1] + 4] = True
    ok[:, 0] = True
    st_src, df_src = np.zeros((NS, H)), np.zeros((NS, H))
    for s in range(NS):
        last = 4.0
        for h in range(H):
            dd, hh = divmod(h, 24)
            bd = dd if hh >= 4 else dd - 1          # the batch day this hour belongs to
            if bd >= 0 and ok[s, bd]:
                last = bd * 24 + 4.0
            st_src[s, h] = 0.0 if (bd < 0 or ok[s, bd]) else 1.0
            df_src[s, h] = 1.0 if h + 0.5 - last > 36.0 else 0.0
    E["price"] = np.array([Ws[m] @ df_src for m, d in CELLS])
    S["price"] = np.array([Ws[m] @ st_src for m, d in CELLS])
    logs["price"] = dict(Ws=Ws, ok=ok, df_src=df_src, st_src=st_src)

    # ---- history: the profile store, a share of its reads failing
    lh = np.full(DAYS, 0.002)
    lh[222:246] = np.clip(0.050 + ar1(rng, 24, 0.7, 0.012), 0.015, 0.10)       # the store's re-shard, 11 August on
    eh = np.clip(lh[day] * (0.8 + 0.2 * diur[hod]), 0, 0.5)
    E["history"] = S["history"] = np.tile(eh, (12, 1))

    # ---- trend: 24 partitions of the click stream; a counter is served six hours after its last update
    NP_ = 24
    wp = rng.dirichlet(np.full(NP_, 2.0))
    lag_s, lag_d, lag_t, eps = np.zeros((NP_, H)), np.zeros((NP_, H)), np.zeros((NP_, H)), []
    for p in range(NP_):
        iv = []
        for dd in range(DAYS):
            for _ in range(rng.poisson(0.050 if 193 <= dd < 270 else 0.006)):
                s = dd * 24 + rng.uniform(0, 24)
                iv.append((s, s + min(rng.lognormal(np.log(36.0), 0.8), 240.0)))
        iv = merge(iv)
        eps += [(p, s, e) for s, e in iv]
        lag_s[p] = cover(iv)
        lag_d[p] = cover([(s + 6.0, e + 1.0) for s, e in iv if e - s > 6.0])
        lag_t[p] = cover([(s + 6.0 - rng.uniform(0, 1), e + rng.uniform(0.3, 1.5)) for s, e in iv if e - s > 6.0])
    E["trend"] = np.tile(wp @ lag_t, (12, 1))
    S["trend"] = np.tile(wp @ lag_s, (12, 1))
    logs["trend"] = dict(wp=wp, eps=eps, lag_d=lag_d, lag_s=lag_s)

    # ---- seller: scored each night when it has new settled orders; a score is served five days
    rank = np.arange(1, N_SELLERS + 1)
    ws = rank ** -1.15
    ws = ws / ws.sum()
    act = np.clip(0.10 + 0.90 * (1 - np.exp(-ws * N_SELLERS * 2.5)), 0, 0.995)
    legacy = rng.random(N_SELLERS) < np.where(rank > 0.12 * N_SELLERS, 0.045, 0.005)
    dirty = rng.random((N_SELLERS, DAYS)) < act[:, None]
    fail = rng.random((N_SELLERS, DAYS)) < 0.004
    a, b = SELLER_WINDOW
    fail[:, a:b] = rng.random((N_SELLERS, b - a)) < SELLER_FAIL
    fail[legacy, a:b] = True

    def served_default(scored):
        idx = np.where(scored, np.arange(DAYS)[None, :], -10 ** 6)
        last = np.maximum.accumulate(idx, axis=1)
        return (np.arange(DAYS)[None, :] - last) > 4          # no score in the last five nights

    d_act = served_default(dirty & ~fail)
    d_cf = served_default(dirty)
    mw = np.array([ws * np.exp(rng.normal(0, 0.15, N_SELLERS)) for _ in range(9)])
    mw = mw / mw.sum(axis=1, keepdims=True)                    # the month's traffic share as the file holds it
    exc = ws @ (d_act.astype(float) - d_cf.astype(float))
    E["seller"] = np.tile(np.repeat(exc, 24), (12, 1))
    due = dirty.sum(axis=0)
    failed = (dirty & fail).sum(axis=0)
    S["seller"] = np.tile(np.repeat(failed / np.maximum(due, 1), 24), (12, 1))
    logs["seller"] = dict(ws=ws, mw=mw, dirty=dirty, fail=fail, d_act=d_act, d_cf=d_cf, base_true=np.repeat(ws @ d_cf, 24),
                          tot_true=np.repeat(ws @ d_act, 24),
                          legacy=legacy, due=due, failed=failed)

    # ---- match: one index replica a market, failing by the hour
    em = np.zeros((6, H))
    for m in range(6):
        iv = []
        for dd in range(DAYS):
            rate = 0.55 if (m == 2 and 181 <= dd < 273) else 0.02
            for _ in range(rng.poisson(rate)):
                s = dd * 24 + rng.uniform(0, 24)
                iv.append((s, s + rng.uniform(1.0, 4.0)))
        em[m] = cover(merge(iv))
    E["match"] = S["match"] = np.array([em[m] for m, d in CELLS])
    W.update(E=E, S=S, logs=logs)

    # ---- April: the price batch missed one of the two serving regions (half the users, by hash) on four
    # alternate days. Each region has its own page cache, so every page of the region was built without the prices.
    sp_def, sp_win, sp_stat = np.zeros(H), np.zeros(H, bool), np.zeros(H)
    for dd in SPLIT["days"]:
        sp_def[dd * 24 + 16:(dd + 1) * 24 + 4] = 1.0              # the hours the region served no competitor price
        sp_stat[dd * 24 + 4:(dd + 1) * 24 + 4] = 1.0             # the hours its latest batch stood failed
        sp_win[dd * 24:(dd + 2) * 24] = True                      # the calendar days either touches
    per_price = v["price"] + e2["price"] * elig["price"]

    # ---- the conversion the sessions had
    loss = np.zeros((12, H))
    for j in GROUPS:
        per = v[j][:, None] + (e2[j] * elig[j])[:, None] if j in e2 else v[j][:, None]
        loss += per * E[j]
    p = p0 - loss
    W["p"] = p
    nb_ = rng.binomial(sess.astype(int), 0.5)
    na_ = sess.astype(int) - nb_
    ob_ = rng.binomial(nb_, np.clip(p - per_price[:, None] * sp_def[None, :], 0, 100) / 100.0)
    oa_ = rng.binomial(na_, np.clip(p, 0, 100) / 100.0)
    W["orders"] = oa_ + ob_
    W["split"] = dict(window=sp_win, default=sp_def, status=sp_stat, nb=nb_, ob=ob_, na=na_, oa=oa_)

    # ---- the ablation tests of the ranking model: nine a group, ten days each
    tests = []
    for gi, j in enumerate(GROUPS):
        base_def = E[j] + (logs["seller"]["base_true"][None, :] if j == "seller" else 0.0)
        for k in range(9):
            d0 = MONTH_START[k] + 1 + 2 * gi
            d1 = min(d0 + TEST_DAYS, DAYS)
            hs = slice(d0 * 24, d1 * 24)
            wgt = np.repeat(u[:, d0:d1], 24, axis=1) if G[j]["pre"] else 1.0
            ph = p[:, hs] - wgt * v[j][:, None] * (1 - base_def[:, hs])
            nh = rng.binomial(sess[:, hs].astype(int), HELD)
            nc = rng.binomial(sess[:, hs].astype(int), HELD)
            oh = rng.binomial(nh, np.clip(ph, 0, 100) / 100.0)
            oc = rng.binomial(nc, np.clip(p[:, hs], 0, 100) / 100.0)
            f = lambda x: x.reshape(12, d1 - d0, 24).sum(axis=2)   # noqa: E731
            tests.append(dict(group=j, k=k, d0=d0, d1=d1, nh=f(nh), oh=f(oh), nc=f(nc), oc=f(oc)))
    W["tests"] = tests

    # ---- each second reader: its render log, hour by hour, and its own test
    render, rtest = {}, {}
    for j in READERS:
        el = rng.binomial(sess.astype(int), elig[j][:, None])
        sup = rng.binomial(el, np.clip(E[j] + SUPP_BASE, 0, 1))
        render[j] = dict(eligible=el, suppressed=sup)
        d0, d1 = READER_TEST[j]
        hs = slice(d0 * 24, d1 * 24)
        ph = p[:, hs] - (e2[j] * elig[j])[:, None] * (1 - E[j][:, hs])
        nh = rng.binomial(sess[:, hs].astype(int), READER_HELD)
        nc = rng.binomial(sess[:, hs].astype(int), READER_HELD)
        f = lambda x: x.sum(axis=1)   # noqa: E731
        rtest[j] = dict(nh=f(nh), oh=f(rng.binomial(nh, np.clip(ph, 0, 100) / 100.0)), nc=f(nc),
                        oc=f(rng.binomial(nc, np.clip(p[:, hs], 0, 100) / 100.0)),
                        elig_c=f(rng.binomial(nc, elig[j][:, None])))
    W.update(render=render, rtest=rtest)

    return W


# ---------------------------------------------------------------- what the world lost (the truth)
def q3w(W, lo=Q3[0], hi=Q3[1]):
    s = W["sess"][:, lo * 24:hi * 24]
    return s / s.sum()


def truth(W):
    out = {}
    for j in GROUPS:
        per = W["v"][j] + (W["e2"][j] * W["elig"][j] if j in W["e2"] else 0.0)
        out[j] = float(np.sum(q3w(W) * per[:, None] * W["E"][j][:, Q3[0] * 24:Q3[1] * 24]))
    return out


# ---------------------------------------------------------------- the estimators
def exposure(W, o):
    """The share of sessions served the default, cell by hour: the part over the group's usual level ("exc") and
    all of it ("tot"). S2 lost: the incidence telemetry (the share of chains, sources, partitions or sellers failing
    in the hour). Kept: each value's own state, rebuilt from the gap, batch, lag and scoring records with its
    validity period, and weighted by the traffic the entity carries."""
    L = W["logs"]
    out = {}
    for j in GROUPS:
        tot = None
        if o.get("s2") or G[j]["ttl"] == 0.0:
            x = W["S"][j]
        elif j == "stock":
            edge = o.get("stock_edge", 0.125)
            dc = L["stock"]["default_c"] if edge == 0.125 else np.array(
                [cover([(s + 2.0 - edge, e + edge) for kk, s, e in L["stock"]["gaps"] if kk == k and e - s > 2.0 - edge])
                 for k in range(L["stock"]["Wc"].shape[1])])
            x = np.array([L["stock"]["Wc"][m] @ dc for m, d in CELLS])
        elif j == "price":
            x = np.array([L["price"]["Ws"][m] @ L["price"]["df_src"] for m, d in CELLS])
        elif j == "trend":
            ref = o.get("trend_refill", 1.0)
            ld = L["trend"]["lag_d"] if ref == 1.0 else np.array(
                [cover([(s + 6.0, e + ref) for pp, s, e in L["trend"]["eps"] if pp == p and e - s > 6.0])
                 for p in range(len(L["trend"]["wp"]))])
            x = np.tile(L["trend"]["wp"] @ ld, (12, 1))
        else:
            sl = L["seller"]
            if o.get("seller_w") == "quarter":
                wd = np.tile(sl["mw"][6:9].mean(axis=0), (DAYS, 1)).T
            else:
                mon = np.searchsorted(MONTH_START, np.arange(DAYS), side="right") - 1
                wd = sl["mw"][mon].T
            share = (wd * sl["d_act"]).sum(axis=0)
            if o.get("seller_indep"):                              # a rival: failures independent night to night
                rate = np.repeat(sl["failed"] / np.maximum(sl["due"], 1), 1)
                p5 = np.array([np.prod(rate[max(0, d - 4):d + 1]) if d >= 4 else 0.0 for d in range(DAYS)])
                exc = p5
            elif o.get("seller_base", "replay") == "none":       # a rival: every stale score charged to the job
                exc = share
            elif o.get("seller_base", "replay") == "replay":    # the same nights with every failed run taken as scored
                exc = share - (wd * sl["d_cf"]).sum(axis=0)
            else:
                lo, hi = {"q2": Q2, "june": (151, 181), "h1": (10, 181)}[o["seller_base"]]
                exc = np.clip(share - share[lo:hi].mean(), 0, None)
            x = np.tile(np.repeat(exc, 24), (12, 1))
            tot = np.tile(np.repeat(share, 24), (12, 1))
        x = x * o.get("exp_scale", {}).get(j, 1.0)
        out[j] = dict(exc=x, tot=x if tot is None else tot)
    return out


def effects(W, o, exp):
    """What a session loses when the group reaches the ranking model as its default, cell by cell, from the
    ablation tests. S1 lost: the measured effect as it stands. Kept: the measured effect over the share of the held
    slice's pages built fresh. Either way net of the default the group was already serving on the test's days."""
    pool = o.get("eff_pool", "device")
    out = {}
    for j in GROUPS:
        num, den = [], []
        for t in W["tests"]:
            if t["group"] != j:
                continue
            if o.get("eff_period") == "h1" and t["d0"] >= Q3[0]:
                continue
            if o.get("eff_period") == "recent" and t["d0"] < Q2[0]:
                continue
            itt = 100.0 * (t["oc"] / np.maximum(t["nc"], 1) - t["oh"] / np.maximum(t["nh"], 1))
            n = t["nh"].astype(float)
            if o.get("eff_weight") == "var":
                n = 1.0 / (1.0 / np.maximum(t["nh"], 1) + 1.0 / np.maximum(t["nc"], 1))
            fresh = W["u"][:, t["d0"]:t["d1"]] if (G[j]["pre"] and not o.get("s1")) else np.ones_like(itt)
            if o.get("u_grain") == "test":
                fresh = np.repeat(fresh.mean(axis=1, keepdims=True), fresh.shape[1], axis=1)
            if not o.get("eff_raw"):
                hs = slice(t["d0"] * 24, t["d1"] * 24)
                sw = W["sess"][:, hs].reshape(12, -1, 24)
                dflt = (exp[j]["tot"][:, hs].reshape(12, -1, 24) * sw).sum(axis=2) / np.maximum(sw.sum(axis=2), 1)
                fresh = fresh * (1 - np.clip(dflt, 0, 0.9))
            num.append(itt * n)
            den.append(fresh * n)
        num, den = np.sum(num, axis=0).sum(axis=1), np.sum(den, axis=0).sum(axis=1)
        if pool == "cell":
            eff = num / den
        elif pool == "all":
            eff = np.full(12, num.sum() / den.sum())
        else:
            eff = np.array([num[d::2].sum() / den[d::2].sum() for m, d in CELLS])
        out[j] = eff * o.get("eff_scale", {}).get(j, 1.0)
    return out


def readers(W, o):
    """Each second reader: its loss per eligible session from its own test, and the share of sessions it failed to
    render over its own usual rate, cell by hour. S3 lost: nothing."""
    out = {}
    for j in READERS:
        if o.get("s3"):
            continue
        t, r = W["rtest"][j], W["render"][j]
        d = 100.0 * (t["oc"] / t["nc"] - t["oh"] / t["nh"])
        es = t["elig_c"] / t["nc"]
        if o.get("rd_pool") == "all":
            per = np.full(12, np.sum(d * t["nh"]) / np.sum(es * t["nh"]))
        else:
            per = np.array([np.sum((d * t["nh"])[dd::2]) / np.sum((es * t["nh"])[dd::2]) for m, dd in CELLS])
        sh = r["suppressed"] / np.maximum(W["sess"], 1)
        lo, hi = {"q2": Q2, "h1": (10, 181), "june": (151, 181)}[o.get("rd_base", "q2")]
        w = W["sess"][:, lo * 24:hi * 24]
        base = (r["suppressed"][:, lo * 24:hi * 24].sum(axis=1) / w.sum(axis=1))[:, None]
        out[j] = dict(per=per * o.get("rd_scale", {}).get(j, 1.0), share=np.clip(sh - base, -1, None), elig=es)
    return out


def view(W, o=None):
    """Every graded figure on one route."""
    o = o or {}
    exp = exposure(W, o)
    eff, rd = effects(W, o, exp), readers(W, o)
    w = q3w(W)
    hq = slice(Q3[0] * 24, Q3[1] * 24)
    loss, by_month, hourly, parts = {}, {}, np.zeros((12, H)), {}
    for j in GROUPS:
        x = eff[j][:, None] * exp[j]["exc"]
        r2 = rd[j]["per"][:, None] * rd[j]["share"] if j in rd else np.zeros((12, H))
        tot = x + r2
        hourly += tot
        loss[j] = float(np.sum(w * tot[:, hq]))
        parts[j] = dict(rank=float(np.sum(w * x[:, hq])), reader=float(np.sum(w * r2[:, hq])),
                        exposed=100.0 * float(np.sum(w * exp[j]["exc"][:, hq])),
                        eff=float(np.sum(w.sum(axis=1) * eff[j])))
    for n, lo, hi in Q3_MONTHS:
        by_month[n] = float(np.sum(q3w(W, lo, hi) * hourly[:, lo * 24:hi * 24]))
    total = float(sum(loss.values()))
    tier = float(sum(x for x in loss.values() if x >= LINE))
    # April's missed batches, as this route would have called them: the affected region's conversion against the
    # other region's over the calendar days the misses touch (the conversion record is daily)
    sp = W["split"]
    n = W["sess"][:, sp["window"]]
    dflt = (sp["status"] if o.get("s2") else sp["default"])[sp["window"]]
    per = eff["price"] + (rd["price"]["per"] * rd["price"]["elig"] if "price" in rd else 0.0)
    split = float(np.sum(n * per[:, None] * dflt[None, :]) / n.sum())
    return dict(loss=loss, month=by_month, total=total, tier=tier, parts=parts, split=split,
                c1=parts[FRESH_GROUP]["eff"], c2=parts[STATE_GROUP]["exposed"], c3=parts[READER_GROUP]["reader"])


def split_measured(W):
    """What the daily record shows: the other region's conversion less the affected region's, over the days touched."""
    sp = W["split"]
    w = sp["window"]
    return 100.0 * float(sp["oa"][:, w].sum() / sp["na"][:, w].sum() - sp["ob"][:, w].sum() / sp["nb"][:, w].sum())


def direct(W):
    """The pack's most direct evidence read raw: each job's own incidence figure over the quarter (not weighted by
    the traffic a chain, source or partition carries) times the group's latest test as its record reports it."""
    out = {}
    L = W["logs"]
    raw = {"stock": L["stock"]["unavail"].mean(axis=0), "price": L["price"]["st_src"].mean(axis=0),
           "trend": L["trend"]["lag_s"].mean(axis=0)}
    w = q3w(W)
    for j in GROUPS:
        t = [t for t in W["tests"] if t["group"] == j][-1]
        itt = 100.0 * (t["oc"].sum() / t["nc"].sum() - t["oh"].sum() / t["nh"].sum())
        s = np.tile(raw[j], (12, 1)) if j in raw else W["S"][j]
        out[j] = float(itt * np.sum(w * s[:, Q3[0] * 24:Q3[1] * 24]))
    return out


RIGOROUS = {"s1": True, "s2": True, "s3": True, "eff_pool": "cell", "eff_weight": "var"}


def panel(W):
    """The observational rival: daily conversion by cell on the incidence telemetry, with cell, weekday, month and
    promotion effects, weighted by sessions. Returns each group's implied loss over the quarter and its standard
    error."""
    sd = W["sess"].reshape(12, DAYS, 24).sum(axis=2)
    od = W["orders"].reshape(12, DAYS, 24).sum(axis=2)
    y = 100.0 * od / sd
    cols, names = [], []
    for c in range(12):
        z = np.zeros((12, DAYS))
        z[c] = 1
        cols.append(z)
    for k in range(1, 7):
        cols.append(np.tile((((np.arange(DAYS) + 3) % 7) == k).astype(float), (12, 1)))
    for k in range(1, 9):
        cols.append(np.tile(((np.arange(DAYS) >= MONTH_START[k]) & (np.arange(DAYS) < MONTH_START[k + 1])).astype(float), (12, 1)))
    cols.append(np.array([W["promo"][m].astype(float) for m, d in CELLS]))
    nb = len(cols)
    for j in GROUPS:
        cols.append((W["S"][j] * W["sess"]).reshape(12, DAYS, 24).sum(axis=2) / sd)
        names.append(j)
    X = np.array([c.ravel() for c in cols]).T
    wv = sd.ravel()
    Xw, yw = X * np.sqrt(wv)[:, None], y.ravel() * np.sqrt(wv)
    beta, *_ = np.linalg.lstsq(Xw, yw, rcond=None)
    res = yw - Xw @ beta
    cov = np.linalg.pinv(Xw.T @ Xw) * (res @ res) / (len(yw) - X.shape[1])
    w = q3w(W)
    out = {}
    for i, j in enumerate(names):
        mean_s = float(np.sum(w * W["S"][j][:, Q3[0] * 24:Q3[1] * 24]))
        out[j] = (-beta[nb + i] * mean_s, np.sqrt(cov[nb + i, nb + i]) * mean_s)
    return out


def panel_did(W, exps, lo=120, hi=DAYS):
    """The second observational rival: the same daily record with a market and device effect and an effect for each
    day, so only what differs between markets on a day is left to explain. Returns loss and standard error."""
    sd = W["sess"].reshape(12, DAYS, 24).sum(axis=2)[:, lo:hi]
    od = W["orders"].reshape(12, DAYS, 24).sum(axis=2)[:, lo:hi]
    y = 100.0 * od / sd

    def within(a):
        r = a.copy()
        for _ in range(40):
            r = r - (r * sd).sum(axis=1, keepdims=True) / sd.sum(axis=1, keepdims=True)
            r = r - (r * sd).sum(axis=0, keepdims=True) / sd.sum(axis=0, keepdims=True)
        return r
    xs = {j: (exps[j] * W["sess"]).reshape(12, DAYS, 24).sum(axis=2)[:, lo:hi] / sd for j in GROUPS}
    keep = [j for j in GROUPS if np.abs(within(xs[j])).max() > 1e-6]
    X = np.array([within(xs[j]).ravel() for j in keep]).T
    wv = sd.ravel()
    Xw, yw = X * np.sqrt(wv)[:, None], within(y).ravel() * np.sqrt(wv)
    beta, *_ = np.linalg.lstsq(Xw, yw, rcond=None)
    res = yw - Xw @ beta
    cov = np.linalg.pinv(Xw.T @ Xw) * (res @ res) / (len(yw) - 12 - (hi - lo) - len(keep))
    w = q3w(W)
    out = {}
    for i, j in enumerate(keep):
        mean_x = float(np.sum(w * exps[j][:, Q3[0] * 24:Q3[1] * 24]))
        out[j] = (-beta[i] * mean_x, np.sqrt(cov[i, i]) * mean_x)
    return out


# ---------------------------------------------------------------- the honest family and the lattice of shortcuts
DIMS = {
    "effect": [("effects pooled over every market and device", {"eff_pool": "all"}),
               ("effects cell by cell", {"eff_pool": "cell"}),
               ("effects weighted by the precision of each day's difference", {"eff_weight": "var"}),
               ("effects on the tests run before July", {"eff_period": "h1"}),
               ("effects on the tests run from April", {"eff_period": "recent"}),
               ("effects not netted for the default served on the tests' own days", {"eff_raw": True})],
    "fresh": [("the fresh share averaged over each test", {"u_grain": "test"})],
    "state": [("a snapshot fresh the minute its feed stops and back the minute it returns", {"stock_edge": 0.0}),
              ("a snapshot a quarter of an hour old when its feed stops, and as long again to return", {"stock_edge": 0.25}),
              ("counters back the hour their partition catches up", {"trend_refill": 0.0}),
              ("counters back two hours after their partition catches up", {"trend_refill": 2.0}),
              ("sellers weighted by the quarter's traffic", {"seller_w": "quarter"}),
              ("the sellers' usual default share from the second quarter", {"seller_base": "q2"}),
              ("the sellers' usual default share from June", {"seller_base": "june"}),
              ("the sellers' usual default share from the first half", {"seller_base": "h1"})],
    "reader": [("the readers' loss pooled over markets and devices", {"rd_pool": "all"}),
               ("the readers' usual failed renders from the first half", {"rd_base": "h1"}),
               ("the readers' usual failed renders from June", {"rd_base": "june"})],
}


def family():
    out = [(n, dict(o)) for dim in DIMS.values() for n, o in dim]
    for da, db in itertools.combinations(DIMS, 2):
        for (na, oa), (nb, ob) in itertools.product(DIMS[da], DIMS[db]):
            out.append((na + "; " + nb, {**oa, **ob}))
    return out


VARIANTS = family()
SIDS = ("S1", "S2", "S3")
LOST = {"S1": {"s1": True}, "S2": {"s2": True}, "S3": {"s3": True}}


def lat_keys():
    return ["+".join(ks) for r in (1, 2, 3) for ks in itertools.combinations(SIDS, r)]


def lat_opts(keys):
    o = {}
    for k in keys:
        o.update(LOST[k])
    return o


def calls(fig):
    return tuple(int(fig[j] >= LINE) for j in GROUPS)


def build(W):
    g = view(W)
    fam = [view(W, o) for _, o in VARIANTS]
    lat = {k: view(W, lat_opts(k.split("+"))) for k in lat_keys()}
    rg = view(W, RIGOROUS)
    dr = direct(W)
    tr = truth(W)
    members = {j: dict(lines=[LINE], truth=tr[j], golden=g["loss"][j], family=[f["loss"][j] for f in fam],
                       routes={"direct": dr[j], "rigorous": rg["loss"][j]}) for j in GROUPS}
    lattice = {k: dict(v["loss"]) for k, v in lat.items()}

    def fig(fid, block, get):
        return dict(id=fid, block=block, golden=get(g), family=[get(f) for f in fam],
                    lattice={k: get(v) for k, v in lat.items()}, routes={"rigorous": get(rg)})
    figs = [fig("C1 full effect, %s" % FRESH_GROUP, "component", lambda x: x["c1"]),
            fig("C2 sessions served the default, %s" % STATE_GROUP, "component", lambda x: x["c2"]),
            fig("C3 the reader's loss, %s" % READER_GROUP, "component", lambda x: x["c3"]),
            fig("C4 April's missed batches as called", "component", lambda x: x["split"])]
    for j in GROUPS:
        figs.append(dict(id="A1 %s" % j, block="ask", member=j))
    for n, _, _ in Q3_MONTHS:
        figs.append(fig("A2 %s" % n, "ask", lambda x, n=n: x["month"][n]))
    figs.append(fig("A3 all seven", "ask", lambda x: x["total"]))
    figs.append(fig("A4 the tier one list", "ask", lambda x: x["tier"]))
    stumps = {
        "S1": dict(axis="what", opens=FRESH_GROUP, steps_left=4, precedents=["L18", "L28"],
                   said_out_loud="A user held out of a feature group still gets result pages from the cache every "
                                 "user shares, so an ablation test measures only part of what the group is worth."),
        "S2": dict(axis="when", opens=STATE_GROUP, steps_left=5, precedents=["N21", "L26"],
                   said_out_loud="A value is served for its validity period after its source fails and returns only "
                                 "at its entity's next refresh, so the share of sources failing is not the share of "
                                 "sessions served the default."),
        "S3": dict(axis="who", opens=READER_GROUP, steps_left=4, precedents=["L16", "N27"],
                   said_out_loud="The ablation tests withhold a group from the ranking model only, and some groups "
                                 "are also read by a service that shows the user something and loses it in the same "
                                 "hours."),
    }
    meas = split_measured(W)
    ref = dict(slice="April's missed price batches: one of the two serving regions (half the users, by hash, with "
                     "its own page cache) went without four batches on alternate days, read against the other region",
               covers_target=False, truth=meas, golden=g["split"],
               rivals=dict([("%s lost" % k, lat[k]["split"]) for k in SIDS] +
                           [("every stump lost", lat["+".join(SIDS)]["split"]), ("rigorous", rg["split"])]))
    spec = dict(task="task9 architecture 4", call="lines", members=members, lattice=lattice, referee=ref,
                stumps=stumps, figures=figs)
    return spec, dict(g=g, fam=fam, lat=lat, rg=rg, dr=dr, tr=tr, meas=meas)


def spreads(x):
    g, fam = x["g"]["parts"], [f["parts"] for f in x["fam"]]
    return {j: dict(eff=max(abs(f[j]["eff"] / g[j]["eff"] - 1) for f in fam),
                    exp=max(abs(f[j]["exposed"] / g[j]["exposed"] - 1) for f in fam),
                    rd=max(abs(f[j]["reader"] / g[j]["reader"] - 1) for f in fam) if g[j]["reader"] else 0.0)
            for j in GROUPS}


def forcing_rows(W, x):
    sp = spreads(x)
    gc = calls(x["g"]["loss"])
    rows = []
    for nm, key in (("the full effects", "eff"), ("the default served", "exp"), ("the readers' losses", "rd")):
        for sgn, word in ((1, "up"), (-1, "down")):
            o = {"eff_scale": {}, "exp_scale": {}, "rd_scale": {}}
            o[{"eff": "eff_scale", "exp": "exp_scale", "rd": "rd_scale"}[key]] = {j: 1 + sgn * sp[j][key] for j in GROUPS}
            rows.append(("%s one spread %s" % (nm, word), o))
    for sa, sb, sc in itertools.product((1, -1), repeat=3):
        rows.append(("all three one spread (%+d, %+d, %+d)" % (sa, sb, sc),
                     {"eff_scale": {j: 1 + sa * sp[j]["eff"] for j in GROUPS},
                      "exp_scale": {j: 1 + sb * sp[j]["exp"] for j in GROUPS},
                      "rd_scale": {j: 1 + sc * sp[j]["rd"] for j in GROUPS}}))
    out = []
    for nm, o in rows:
        v = view(W, o)["loss"]
        near = min((abs(v[j] - LINE), j) for j in GROUPS)
        out.append((nm, calls(v) == gc, near[0], near[1], v))
    return out, sp


def forcing(W, x):
    rows, sp = forcing_rows(W, x)
    print("measured spreads, per cent of itself (full effect, default served, reader's loss):")
    for j in GROUPS:
        print("  %-8s %5.1f%%  %5.1f%%  %5.1f%%" % (j, 100 * sp[j]["eff"], 100 * sp[j]["exp"], 100 * sp[j]["rd"]))
    ok = True
    for nm, same, d, j, v in rows:
        ok = ok and same
        print("%-44s call %s  nearest the line %.4f (%s)" % (nm, "holds" if same else "MOVES", d, j))
    fam_near = min((abs(f["loss"][j] - LINE), j) for f in x["fam"] for j in GROUPS)
    print("the family's nearest approach to the line: %.4f (%s)" % fam_near)
    return ok


def detail(W, x):
    g, lat, tr = x["g"], x["lat"], x["tr"]
    print("%-8s %7s %7s | %7s %7s %7s | %7s %7s %7s | exposed%% true/gold/telemetry" % (
        "group", "truth", "golden", "S1", "S2", "S3", "reflex", "direct", "rigor"))
    w = q3w(W)
    hq = slice(Q3[0] * 24, Q3[1] * 24)
    for j in GROUPS:
        print("%-8s %7.4f %7.4f | %7.4f %7.4f %7.4f | %7.4f %7.4f %7.4f | %5.2f %5.2f %5.2f" % (
            j, tr[j], g["loss"][j], lat["S1"]["loss"][j], lat["S2"]["loss"][j], lat["S3"]["loss"][j],
            lat["S1+S2+S3"]["loss"][j], x["dr"][j], x["rg"]["loss"][j],
            100 * np.sum(w * W["E"][j][:, hq]), g["parts"][j]["exposed"], 100 * np.sum(w * W["S"][j][:, hq])))
    print("total: truth %.4f golden %.4f reflex %.4f" % (sum(tr.values()), g["total"], lat["S1+S2+S3"]["total"]))
    for k in ["S1", "S2", "S3", "S1+S2", "S1+S3", "S2+S3", "S1+S2+S3"]:
        print("  %-9s total %.4f tier %.4f months %s   (golden %.4f, %.4f, %s)" % (
            k, lat[k]["total"], lat[k]["tier"], " ".join("%.3f" % lat[k]["month"][n] for n, _, _ in Q3_MONTHS),
            g["total"], g["tier"], " ".join("%.3f" % g["month"][n] for n, _, _ in Q3_MONTHS)))
    for j in GROUPS:
        fam = [f["loss"][j] for f in x["fam"]]
        print("  family %-8s %.4f to %.4f (golden %.4f, %d variants)" % (j, min(fam), max(fam), g["loss"][j], len(fam)))
    print("full effects (golden, session weighted): " + ", ".join("%s %.3f" % (j, g["parts"][j]["eff"]) for j in GROUPS))
    print("true full effects:                       " + ", ".join(
        "%s %.3f" % (j, float(np.sum(w.sum(axis=1) * W["v"][j]))) for j in GROUPS))
    print("April's missed batches: measured %.3f, golden %.3f, S1 lost %.3f, S2 lost %.3f, S3 lost %.3f, rigorous %.3f" % (
        x["meas"], g["split"], lat["S1"]["split"], lat["S2"]["split"], lat["S3"]["split"], x["rg"]["split"]))
    un = view(W, {"seller_base": "none"})
    print("seller replayed by entity but not netted of what normal service leaves at the default: %.4f (%.2f per cent "
          "of sessions against %.2f)" % (un["loss"]["seller"], un["parts"]["seller"]["exposed"], g["parts"]["seller"]["exposed"]))
    ind = view(W, {"seller_indep": True})
    print("seller with each night's failures taken as independent of the last: %.4f" % ind["loss"]["seller"])
    sd = W["sess"].reshape(12, DAYS, 24).sum(axis=2)
    od = W["orders"].reshape(12, DAYS, 24).sum(axis=2)
    q = lambda lo, hi: 100.0 * od[:, lo:hi].sum() / sd[:, lo:hi].sum()   # noqa: E731
    print("search conversion: second quarter %.3f, third quarter %.3f, fall %.3f" % (q(*Q2), q(*Q3), q(*Q2) - q(*Q3)))
    pn = panel(W)
    print("the observational rival (daily conversion on the incidence telemetry): implied loss and its standard error")
    for j in GROUPS:
        print("  %-8s %7.4f +/- %.4f   (truth %.4f)" % (j, pn[j][0], pn[j][1], tr[j]))
    for label, exps in (("the rebuilt default served", {j: exposure(W, {})[j]["exc"] for j in GROUPS}),
                        ("the incidence telemetry", W["S"])):
        pd_ = panel_did(W, exps)
        print("the second observational rival (a day effect and a market and device effect), on %s:" % label)
        for j in GROUPS:
            print("  %-8s %s   (truth %.4f)" % (j, ("%7.4f +/- %.4f" % pd_[j]) if j in pd_ else
                                                 "the same in every market on a day: nothing left to fit", tr[j]))


def main():
    W = make_world()
    spec, x = build(W)
    if "--detail" in sys.argv:
        detail(W, x)
        return 0
    if "--forcing" in sys.argv:
        return 0 if forcing(W, x) else 1
    return corelib.run(spec)


if __name__ == "__main__":
    sys.exit(main())
