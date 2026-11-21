"""The shipped records, written from the world core.py simulates: the app backend's accounts and billing events, the
attribution partner's install export, the ad networks' install postbacks, both stores' daily subscription reports,
the card processor's settlements for the web checkout, the ad platforms' daily spend by campaign, and two files the
analysis does not use (creative tests, store ratings). Each file is written the way its system writes it. Every paid
channel buys market by market: a campaign runs in one market (ES, IT or PT), live in the weeks core's calendar says,
and an install's market is its storefront. The mess laid on top (re-sent rows, reinstalls, staff and test accounts,
sandbox charges, refunded purchases, webhook retries, Apple's Pacific days, a few euros billed after a pause) never
touches an array the core reads."""
import csv
import datetime as dt
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import core as C  # noqa: E402

DAY0 = dt.date(2024, 11, 4)
FILES = {
    "acc": "accounts_2024-11-04_2026-11-01.csv",
    "bill": "billing_events_2024-11-04_2026-11-08.csv",
    "attr": "attribution_installs_2024-11-04_2026-11-01.csv",
    "skan": "skan_postbacks_2024-11-07_2026-11-05.csv",
    "apple": "appstore_subscription_events_daily_2024-11_2026-11.csv",
    "google": "googleplay_subscription_transactions_daily_2024-11_2026-11.csv",
    "web": "web_checkout_settlements_monthly_2024-11_2026-11.csv",
    "spend": "ad_spend_daily_2024-11-04_2026-11-01.csv",
    "creat": "creative_tests_2025-2026.csv",
    "rate": "store_ratings_daily_2024-11_2026-10.csv",
}
SOURCE = {"Meta iOS": ("Meta Ads", "ios"), "TikTok iOS": ("TikTok For Business", "ios"),
          "Snapchat iOS": ("Snapchat Ads", "ios"), "Google iOS": ("Google Ads", "ios"),
          "Pinterest iOS": ("Pinterest Ads", "ios"), "Apple Search Ads": ("Apple Search Ads", "ios"),
          "Google Android": ("Google Ads", "android"), "AppLovin Android": ("AppLovin", "android")}
SKAN_NET = {"Meta iOS": "meta", "TikTok iOS": "tiktok", "Snapchat iOS": "snapchat", "Google iOS": "google",
            "Pinterest iOS": "pinterest"}
REPORTED = {"Meta iOS": 1.17, "TikTok iOS": 1.22, "Snapchat iOS": 1.19, "Google iOS": 1.09, "Pinterest iOS": 1.13,
            "Apple Search Ads": 1.0, "Google Android": 1.08, "AppLovin Android": 1.02}
CPM = {"Meta iOS": 7.9, "TikTok iOS": 5.2, "Snapchat iOS": 4.6, "Google iOS": 6.4, "Pinterest iOS": 5.9,
       "Apple Search Ads": 38.0, "Google Android": 3.7, "AppLovin Android": 9.4}
CAMP_BASE = {"Meta iOS": 23851000000, "TikTok iOS": 17640000000, "Snapchat iOS": 31200000, "Google iOS": 20510000000,
             "Pinterest iOS": 626740000000, "Apple Search Ads": 1410000000, "Google Android": 20930000000,
             "AppLovin Android": 5520000}
CAMP_NAMES = {
    "Meta iOS": ["Prospecting_Broad_18-44", "LAL_Subscribers_1pc", "LAL_Subscribers_3pc", "Interests_HomeWorkout",
                 "Advantage_AppInstalls", "Creators_Reels", "NewYear_Restart", "Interests_Yoga_Pilates",
                 "Summer_20min", "Broad_Women_25-54", "Video_Testimonials"],
    "TikTok iOS": ["Spark_Creators_A", "Broad_AppInstall", "Interest_Fitness", "Hashtag_HomeWorkout", "NewYear_Push",
                   "Spark_Creators_B", "LAL_Trial_Starters", "Broad_Summer"],
    "Snapchat iOS": ["Story_Ads_Broad", "Lifestyle_Fitness", "Spotlight_Creators", "Lookalike_Installers",
                     "Collection_Programmes", "Broad_18-34"],
    "Google iOS": ["ACi_Installs_Main", "ACi_InApp_TrialStart", "ACi_Installs_YouTube", "ACi_Search_Generic",
                   "ACi_InApp_Purchase"],
    "Pinterest iOS": ["Pins_HomeWorkout_Plans", "Shopping_Interest_Fitness", "Idea_Ads_Routines", "Keywords_Pilates",
                      "Actalike_Subscribers"],
    "Apple Search Ads": ["Brand_Exact", "Generic_Workout_Exact", "Generic_Workout_Broad", "Competitors",
                         "Discovery_SearchMatch", "Today_Tab_Test"],
    "Google Android": ["AC_Installs_Main", "AC_InApp_TrialStart", "AC_Installs_Display", "AC_InApp_Purchase",
                       "AC_Installs_YouTube", "AC_Search_Generic", "AC_PreReg_Test", "AC_Installs_Lite"],
    "AppLovin Android": ["AppDiscovery_CPI", "AppDiscovery_ROAS_D7", "Rewarded_Video_Broad", "Playables_Test",
                         "AppDiscovery_ROAS_D28", "Interstitial_Fitness"],
}
# how each ad account's naming convention carries the market
NAMING = {"Meta iOS": "%(m)s_%(n)s", "TikTok iOS": "%(n)s_%(m)s", "Snapchat iOS": "%(m)s-%(n)s",
          "Google iOS": "%(n)s_%(m)s", "Pinterest iOS": "%(m)s_%(n)s", "Apple Search Ads": "%(m)s_%(n)s",
          "Google Android": "%(n)s_%(m)s", "AppLovin Android": "%(n)s-%(m)s"}
# campaigns a market may hold on one ad account (ES, IT, PT): one that runs whenever the market is live, and others
MAX_CAMPS = {"Meta iOS": (4, 3, 2), "TikTok iOS": (3, 2, 2), "Snapchat iOS": (3, 2, 1), "Google iOS": (2, 2, 1),
             "Pinterest iOS": (2, 2, 1), "Apple Search Ads": (3, 2, 1), "Google Android": (3, 2, 2),
             "AppLovin Android": (3, 2, 1)}
MARKET_COST = (1.0, 0.94, 0.81)            # what an install costs in a market against Spain, roughly
HOURS = np.array([0.6, 0.3, 0.2, 0.2, 0.3, 0.9, 2.2, 3.4, 3.6, 3.3, 3.2, 3.4, 3.6, 3.3, 3.2, 3.6, 4.4, 5.6, 6.6, 7.2,
                  6.8, 5.0, 2.8, 1.3])
PRICE = (C.PRICE_M, C.PRICE_A)
PRODUCT = {0: ("zancada.premium.monthly", "zancada.premium.annual"), 1: ("premium_monthly", "premium_annual"),
           2: ("web_premium_monthly", "web_premium_annual")}
STORE = ("app_store", "google_play", "web")
COUNTRIES = C.MARKETS
# Pacific daylight time, in seconds from day 0 00:00 UTC (9 March 2025 10:00Z to 2 November 2025 09:00Z, and 2026's)
_s = lambda y, m, d, h: int((dt.datetime(y, m, d, h) - dt.datetime(2024, 11, 4)).total_seconds())
PDT = ((_s(2025, 3, 9, 10), _s(2025, 11, 2, 9)), (_s(2026, 3, 8, 10), _s(2026, 11, 1, 9)))


def pacific_day(ts):
    """the Pacific calendar day (counted from 4 November 2024) of a UTC time in seconds from day 0"""
    ts = np.asarray(ts, dtype=np.int64)
    off = np.full(ts.shape, 8 * 3600, dtype=np.int64)
    for a, b in PDT:
        off[(ts >= a) & (ts < b)] = 7 * 3600
    return (ts - off) // 86400


def rng_of(k):
    return np.random.default_rng([C.SEED, 7, k])


def clock(rng, n):
    return rng.choice(24, n, p=HOURS / HOURS.sum()) * 3600 + rng.integers(0, 3600, n)


def uniq(rng, n, bits):
    x = np.unique(rng.integers(0, 2 ** bits, int(n * 1.03) + 50, dtype=np.int64))
    rng.shuffle(x)
    assert x.size >= n
    return x[:n]


_D = [(DAY0 + dt.timedelta(days=i - 5)).isoformat() for i in range(800)]
_T = ["%02d:%02d:%02d" % (s // 3600, s // 60 % 60, s % 60) for s in range(86400)]


def stamp(ts):
    """ISO UTC strings for seconds from day 0"""
    ts = np.asarray(ts, dtype=np.int64)
    d = (ts // 86400 + 5).tolist()
    s = (ts % 86400).tolist()
    return ["%sT%sZ" % (_D[a], _T[b]) for a, b in zip(d, s)]


def date_of(day):
    return _D[int(day) + 5]


def _w(path, header, rows):
    k = 0
    with open(path, "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        for row in rows:
            w.writerow(row)
            k += 1
    return k


def campaigns(ci, c):
    """a channel's campaigns: id, name, market and the weeks each ran. A market's first campaign runs whenever the
    market is live (core's calendar); the others run through some of its live weeks"""
    r = np.random.default_rng([C.SEED, 11, ci])
    live = C.CH[c]["live"]
    names = [str(x) for x in r.permutation(CAMP_NAMES[c])]
    out, used = [], 0
    for m, code in enumerate(COUNTRIES):
        k = int(r.integers(1, MAX_CAMPS[c][m] + 1))
        for j in range(k):
            on = live[m].copy()
            if j:
                w0 = int(r.integers(0, 70))
                w1 = C.WEEKS if r.random() < 0.35 else min(C.WEEKS, w0 + int(r.integers(14, 60)))
                on[:w0] = False
                on[w1:] = False
                if on.sum() < 6:
                    continue
            nm = names[used % len(names)]
            used += 1
            out.append(dict(id=str(CAMP_BASE[c] + int(r.integers(1000, 899999))), market=m, on=on,
                            name=NAMING[c] % dict(m=code, n=nm), wt=float(r.gamma(2.2, 1.0)) + 0.25))
    assert len({x["id"] for x in out}) == len(out) and len({x["name"] for x in out}) == len(out)
    return out


def cents_split(total_cents, weights):
    """integer cents summing exactly to the total, in proportion to the weights"""
    w = np.asarray(weights, float).ravel()
    raw = total_cents * w / w.sum()
    out = np.floor(raw).astype(np.int64)
    short = int(total_cents - out.sum())
    if short:
        out[np.argsort(-(raw - out), kind="stable")[:short]] += 1
    return out.reshape(np.shape(weights))


def build(W, target):
    os.makedirs(target, exist_ok=True)
    n = W["e"].size
    day, lo = W["day"].astype(np.int64), W["last_open"].astype(np.int64)
    ios, web, conv, annual, trial = W["ios"], W["web"], W["conv"], W["annual"], W["trial"]
    src, week, country = W["src"], W["week"], W["country"]
    nsrc = len(C.ORDER)
    counts = {}

    # ---- identities and clocks -----------------------------------------------------------------------------
    r = rng_of(1)
    aid = uniq(r, n, 40)
    sec = clock(r, n)
    csec = np.minimum(sec + r.integers(25, 1500, n), 86399)       # the trial or purchase starts minutes after install
    los = clock(r, n)
    same = ((W["rdays"] == lo[:, None]) & W["charge"]).any(1) | (W["a0"] & (W["conv_day"] == lo))
    los = np.where(same & (los < csec), np.minimum(csec + r.integers(0, 3600, n), 86399), los)
    los = np.where((lo == day) & (los < sec), np.minimum(sec + r.integers(30, 5400, n), 86399), los)
    los = np.where(same & (los < csec), csec, los)
    created = day * 86400 + sec
    lo_ts = lo * 86400 + los

    # ---- campaigns: each paid install came through a campaign of its market that ran that week -----------------
    camps = {c: campaigns(ci, c) for ci, c in enumerate(C.ORDER)}
    camp_ix = np.full(n, -1)
    r = rng_of(2)
    for ci, c in enumerate(C.ORDER):
        cs = camps[c]
        P = np.zeros((C.WEEKS, 3, len(cs)))
        for j, x in enumerate(cs):
            P[x["on"], x["market"], j] = x["wt"]
        rows = np.where(src == ci)[0]
        cum = np.cumsum(P[week[rows], country[rows]], axis=1)
        assert (cum[:, -1] > 0).all(), c                           # an install's market was live that week
        u = r.random(rows.size) * cum[:, -1]
        camp_ix[rows] = (u[:, None] >= cum).sum(1)

    # ---- the app's view of each subscription at the last open ------------------------------------------------
    in_trial = trial & ~conv & (lo < day + 7)
    silent_first = conv & trial & (lo < W["conv_day"])
    state = np.where(in_trial | silent_first, "trial", np.where(W["plan_seen"] > 0, "active", "none"))
    plan = np.array(["", "monthly", "annual"])[W["plan_seen"]]
    auto = np.where(state == "none", "", np.where(W["auto_on"], "yes", "no"))
    route = np.where(state == "none", "", np.where(web, "web", np.where(ios, "app_store", "google_play")))
    r = rng_of(3)
    u = r.random(n)
    # the tracking answer: Apple's prompt on iOS (four statuses), the app's own consent screen on Android (two)
    trk = np.where(W["consent"], "authorized",
                   np.where(~ios, "denied", np.where(u < 0.05, "not_determined", np.where(u < 0.07, "restricted", "denied"))))

    # ---- staff and test accounts --------------------------------------------------------------------------
    r = rng_of(4)
    ns = 163
    s_aid = uniq(r, ns + 400, 40)
    s_aid = s_aid[~np.isin(s_aid, aid)][:ns]
    s_day = r.integers(0, C.WEEKS * 7, ns)
    s_sec = r.integers(8 * 3600, 18 * 3600, ns)
    s_ios = r.random(ns) < 0.62
    s_type = np.where(r.random(ns) < 0.64, "staff", "test")
    s_lo = np.minimum(s_day + r.integers(1, 420, ns), C.END_DAY)
    s_los = r.integers(8 * 3600, 19 * 3600, ns)
    s_cc = r.choice(3, ns, p=(0.9, 0.06, 0.04))
    s_cons = r.random(ns) < 0.7
    s_plan = r.choice(["", "monthly", "annual"], ns, p=(0.25, 0.5, 0.25))

    acc_ts = np.concatenate([created, s_day * 86400 + s_sec])
    order = np.argsort(acc_ts, kind="stable")
    cols = [
        np.concatenate([aid, s_aid]), acc_ts,
        np.concatenate([np.where(ios, "ios", "android"), np.where(s_ios, "ios", "android")]),
        np.concatenate([np.array(COUNTRIES)[country], np.array(COUNTRIES)[s_cc]]),
        np.concatenate([np.full(n, "consumer"), s_type]),
        np.concatenate([trk, np.where(s_cons, "authorized", "denied")]),
        np.concatenate([W["cv"], r.integers(0, 32, ns)]),
        np.concatenate([lo_ts, s_lo * 86400 + s_los]),
        np.concatenate([state, np.where(s_plan == "", "none", "active")]),
        np.concatenate([route, np.where(s_plan == "", "", np.where(s_ios, "app_store", "google_play"))]),
        np.concatenate([plan, s_plan]),
        np.concatenate([auto, np.where(s_plan == "", "", "yes")]),
    ]
    cols = [x[order] for x in cols]
    rows = zip(["za_%010x" % a for a in cols[0].tolist()], stamp(cols[1]), cols[2].tolist(), cols[3].tolist(),
               cols[4].tolist(), cols[5].tolist(), cols[6].tolist(), stamp(cols[7]), cols[8].tolist(), cols[9].tolist(),
               cols[10].tolist(), cols[11].tolist())
    counts["acc"] = _w(os.path.join(target, FILES["acc"]),
                       ["account_id", "created_at", "platform", "storefront", "account_type", "tracking_status",
                        "conversion_value_48h", "last_open_at", "sub_state_at_last_open", "sub_store_at_last_open",
                        "sub_plan_at_last_open", "auto_renew_at_last_open"], rows)

    # ---- every charge the stores and the checkout made -------------------------------------------------------
    r = rng_of(5)
    ii, kk = np.nonzero(W["charge"])
    ev = dict(acct=[ii], prod=[np.zeros(ii.size, int)], typ=[(kk > 0).astype(int)],
              t=[W["rdays"][ii, kk].astype(np.int64) * 86400 + csec[ii]],
              seen=[web[ii] | (W["rdays"][ii, kk] <= lo[ii])], pair=[np.full(ii.size, -1)])
    ia = np.where(W["a0"])[0]
    ev["acct"].append(ia); ev["prod"].append(np.ones(ia.size, int)); ev["typ"].append(np.zeros(ia.size, int))
    ev["t"].append(W["conv_day"][ia].astype(np.int64) * 86400 + csec[ia])
    ev["seen"].append(web[ia] | (W["conv_day"][ia] <= lo[ia])); ev["pair"].append(np.full(ia.size, -1))
    # an annual plan still set to renew is charged again a year on (outside every install's first 365 days)
    ir = ia[W["auto_on"][ia] & (W["conv_day"][ia] + 365 <= C.END_DAY) & (r.random(ia.size) < 0.7)]
    ev["acct"].append(ir); ev["prod"].append(np.ones(ir.size, int)); ev["typ"].append(np.ones(ir.size, int))
    ev["t"].append((W["conv_day"][ir].astype(np.int64) + 365) * 86400 + csec[ir])
    ev["seen"].append(web[ir] | (W["conv_day"][ir] + 365 <= lo[ir])); ev["pair"].append(np.full(ir.size, -1))
    # purchases withdrawn inside fourteen days: charged at the trial's end, refunded, both on the account's record
    cand = np.where(trial & ~conv & (lo >= day + 9))[0]
    ip = cand[r.random(cand.size) < 0.03]
    p_prod = (r.random(ip.size) < 0.2).astype(int)
    p_t = (day[ip] + 7) * 86400 + csec[ip]
    span = np.minimum(13, lo[ip] - day[ip] - 8)
    p_rt = (day[ip] + 7 + 1 + (r.random(ip.size) * span).astype(np.int64)) * 86400 + clock(r, ip.size)
    npair = ip.size
    ev["acct"] += [ip, ip]; ev["prod"] += [p_prod, p_prod]
    ev["typ"] += [np.zeros(npair, int), np.full(npair, 2)]
    ev["t"] += [p_t, p_rt]; ev["seen"] += [np.ones(npair, bool), np.ones(npair, bool)]
    ev["pair"] += [np.arange(npair), np.arange(npair) + npair]          # charge j, its refund j + npair
    E = {k: np.concatenate(v) for k, v in ev.items()}
    E["store"] = np.where(web[E["acct"]], 2, np.where(ios[E["acct"]], 0, 1))
    is_trial = trial[E["acct"]]

    # the stores' daily reports (store charges only, on each store's own day)
    for st, key, dcol in ((0, "apple", "date_pt"), (1, "google", "date_utc")):
        m = E["store"] == st
        d = (pacific_day(E["t"][m]) if st == 0 else E["t"][m] // 86400) + 5
        kind = np.where(E["typ"][m] == 2, 3, np.where(E["typ"][m] == 1, 2, np.where(is_trial[m], 0, 1)))
        if st == 1:
            kind = np.where(kind == 3, 2, np.where(kind == 2, 1, 0))
        cnt = np.zeros((800, 2, 3, 4), np.int64)
        np.add.at(cnt, (d, E["prod"][m], country[E["acct"][m]], kind), 1)
        names = (("Paid Subscription from Free Trial", "Subscribe", "Renew", "Refund") if st == 0 else
                 ("charge_new", "charge_renewal", "refund"))
        rows = []
        for di, pr, cc, kd in zip(*np.nonzero(cnt)):
            un = int(cnt[di, pr, cc, kd])
            sign = -1 if names[kd].lower() == "refund" else 1
            gross = sign * un * PRICE[pr]
            net = gross / (1 + C.VAT[cc]) * (1 - C.COMMISSION)
            rows.append([_D[di], PRODUCT[st][pr], COUNTRIES[cc], names[kd], un, "%.2f" % gross, "%.2f" % net])
        if st == 0:
            hdr = [dcol, "product_id", "storefront", "event", "units", "customer_price_eur", "developer_proceeds_eur"]
        else:
            hdr = [dcol, "product_id", "country", "transaction_type", "transactions", "amount_charged_eur",
                   "net_amount_eur"]
        counts[key] = _w(os.path.join(target, FILES[key]), hdr, rows)

    # the card processor's monthly settlements for the web checkout
    m = E["store"] == 2
    paid = E["t"][m] // 86400 + 2 + (E["t"][m] % 86400 >= 16 * 3600)     # paid out two banking cut-offs on
    mo = np.array([int(_D[x][:4]) * 12 + int(_D[x][5:7]) - 1 for x in range(800)])[paid + 5]
    out = paid <= C.END_DAY + 1                                          # paid out by the day the report was pulled
    cnt = {}
    for a, b, c_ in zip(mo[out].tolist(), E["prod"][m][out].tolist(), country[E["acct"][m]][out].tolist()):
        cnt[(a, b, c_)] = cnt.get((a, b, c_), 0) + 1
    rows = []
    for (a, b, c_), un in sorted(cnt.items()):
        gross = un * PRICE[b]
        vat = gross - gross / (1 + C.VAT[c_])
        fee = (gross - vat) * C.WEB_FEE
        rows.append(["%04d-%02d" % (a // 12, a % 12 + 1), PRODUCT[2][b], COUNTRIES[c_], un, "%.2f" % gross, "%.2f" % vat,
                     "%.2f" % fee, "%.2f" % (gross - vat - fee)])
    counts["web"] = _w(os.path.join(target, FILES["web"]),
                       ["settlement_month", "product_id", "billing_country", "payments", "gross_eur", "vat_eur",
                        "processing_fee_eur", "net_settled_eur"], rows)

    # the app backend's billing events: a store charge once the account next opens the app, a checkout charge at once
    keep = np.where(E["seen"])[0]
    a_i = E["acct"][keep]
    t = E["t"][keep]
    wb = E["store"][keep] == 2
    wait = (r.exponential(0.9 * 86400, keep.size)).astype(np.int64) + 3
    rec = np.where(wb, t + r.integers(1, 5, keep.size), np.minimum(t + wait, np.maximum(lo_ts[a_i], t)))
    pk = E["pair"][keep]
    first_rec = np.zeros(npair, np.int64)
    first_rec[pk[(pk >= 0) & (pk < npair)]] = rec[(pk >= 0) & (pk < npair)]
    back_ = pk >= npair                                             # a refund is on file no earlier than its charge
    rec[back_] = np.maximum(rec[back_], first_rec[pk[back_] - npair])
    b = dict(acct=aid[a_i], store=E["store"][keep], env=np.zeros(keep.size, int), prod=E["prod"][keep],
             typ=E["typ"][keep], t=t, rec=rec, cc=country[a_i], pair=E["pair"][keep])
    # the processor re-sends some checkout webhooks
    dup = np.where(wb & (r.random(keep.size) < 0.004))[0]
    # sandbox purchases on staff and test accounts
    sb_n = r.integers(0, 7, ns)
    sb_a = np.repeat(np.arange(ns), sb_n)
    sb_k = np.concatenate([np.arange(k) for k in sb_n]) if sb_n.sum() else np.zeros(0, int)
    sb_t = (s_day[sb_a] + 1 + 3 * sb_k + r.integers(0, 3, sb_a.size)) * 86400 + r.integers(9 * 3600, 18 * 3600, sb_a.size)
    ok = sb_t < (C.END_DAY + 1) * 86400
    sb_a, sb_k, sb_t = sb_a[ok], sb_k[ok], sb_t[ok]
    parts = {
        "acct": [b["acct"], b["acct"][dup], s_aid[sb_a]],
        "store": [b["store"], b["store"][dup], np.where(s_ios[sb_a], 0, 1)],
        "env": [b["env"], b["env"][dup], np.ones(sb_a.size, int)],
        "prod": [b["prod"], b["prod"][dup], (r.random(sb_a.size) < 0.3).astype(int)],
        "typ": [b["typ"], b["typ"][dup], (sb_k > 0).astype(int)],
        "t": [b["t"], b["t"][dup], sb_t],
        "rec": [b["rec"], b["rec"][dup] + r.integers(30, 900, dup.size), sb_t + r.integers(2, 40, sb_a.size)],
        "cc": [b["cc"], b["cc"][dup], s_cc[sb_a]],
        "pair": [b["pair"], np.full(dup.size, -1), np.full(sb_a.size, -1)],
    }
    Bv = {k: np.concatenate(v) for k, v in parts.items()}
    order = np.lexsort((Bv["t"], Bv["rec"]))
    Bv = {k: v[order] for k, v in Bv.items()}
    eid = 40000000 + np.cumsum(1 + r.geometric(0.55, order.size))
    pos = {int(p): int(e) for p, e in zip(Bv["pair"].tolist(), eid.tolist()) if p >= 0}
    ref = ["" if (p < npair) else "be%09d" % pos[p - npair] for p in Bv["pair"].tolist()]
    amount = np.where(Bv["typ"] == 2, -1.0, 1.0) * np.array(PRICE)[Bv["prod"]]
    rows = zip(["be%09d" % x for x in eid.tolist()], ["za_%010x" % a for a in Bv["acct"].tolist()],
               np.array(STORE)[Bv["store"]].tolist(), np.array(["production", "sandbox"])[Bv["env"]].tolist(),
               [PRODUCT[s][p] for s, p in zip(Bv["store"].tolist(), Bv["prod"].tolist())],
               np.array(["first_charge", "renewal", "refund"])[Bv["typ"]].tolist(), stamp(Bv["t"]), stamp(Bv["rec"]),
               ["%.2f" % x for x in amount.tolist()], np.array(COUNTRIES)[Bv["cc"]].tolist(), ref)
    counts["bill"] = _w(os.path.join(target, FILES["bill"]),
                        ["event_id", "account_id", "store", "environment", "product_id", "event_type", "transaction_at",
                         "recorded_at", "amount_eur", "storefront", "refund_of_event_id"], rows)
    counts["pairs"], counts["sandbox"], counts["web_resent"] = int(npair), int(sb_a.size), int(dup.size)

    # ---- the attribution partner's install export -------------------------------------------------------------
    r = rng_of(6)
    organic = src >= nsrc
    complete = np.array([(C.CH[c]["complete"] if c in C.CH else 0) for c in C.SOURCES], bool)[src]
    named = complete | (W["consent"] & ~organic) | (organic & (W["consent"] | ~ios))
    media = np.array([SOURCE[c][0] for c in C.ORDER] + ["organic", "organic"])[src]
    media = np.where(named, media, "")
    cid_tab = {c: np.array([x["id"] for x in camps[c]]) for c in C.ORDER}
    cid = np.full(n, "", dtype=object)
    for ci, c in enumerate(C.ORDER):
        m = src == ci
        cid[m] = cid_tab[c][camp_ix[m]]
    cid_named = np.where(named & ~organic, cid, "")
    u = r.random(n)
    rs = np.where(u < 0.008)[0]
    ri = np.where((u >= 0.008) & (u < 0.038))[0]
    iid_all = uniq(r, n + ns + ri.size, 48)
    iid = iid_all[:n + ns]
    rl = rng_of(81)                                                # the SDK's first open; sign-up comes a little later
    lag = np.minimum(np.rint(np.exp(rl.normal(np.log(70.0), 0.9, n))).astype(np.int64) + 6, 5 * 3600)
    it = created - np.minimum(lag, np.maximum(created - 2, 1))
    A = dict(iid=[iid[:n]], acct=[aid], plat=[np.where(ios, "ios", "android")], t=[it], media=[media],
             cid=[cid_named], re=[np.full(n, "false")])
    A["iid"].append(iid[n:]); A["acct"].append(s_aid); A["plat"].append(np.where(s_ios, "ios", "android"))
    A["t"].append(s_day * 86400 + s_sec - np.minimum(r.integers(40, 640, ns), np.maximum(s_day * 86400 + s_sec - 2, 1)))
    A["media"].append(np.where(s_ios & ~s_cons, "", "organic")); A["cid"].append(np.full(ns, "", dtype=object))
    A["re"].append(np.full(ns, "false"))
    # the SDK re-sends some rows after a retry, and a second device or a reinstall comes through as a new install
    A["iid"].append(iid[rs]); A["acct"].append(aid[rs]); A["plat"].append(np.where(ios[rs], "ios", "android"))
    A["t"].append(it[rs] + r.integers(1, 55, rs.size)); A["media"].append(media[rs]); A["cid"].append(cid_named[rs])
    A["re"].append(np.full(rs.size, "false"))
    rt = it[ri] + r.integers(3, 300, ri.size) * 86400 + r.integers(0, 86400, ri.size)
    ok = rt < (C.WEEKS * 7) * 86400
    r_iid = iid_all[n + ns:][ok]
    ri, rt = ri[ok], rt[ok]
    back = r.random(ri.size)
    r_media = np.where(ios[ri] & ~W["consent"][ri], "", np.where(back < 0.12, media[ri], "organic"))
    A["iid"].append(r_iid); A["acct"].append(aid[ri])
    A["plat"].append(np.where(ios[ri], "ios", "android")); A["t"].append(rt); A["media"].append(r_media)
    A["cid"].append(np.where((r_media != "") & (r_media != "organic"), cid_named[ri], "")); A["re"].append(np.full(ri.size, "true"))
    Av = {k: np.concatenate(v) for k, v in A.items()}
    order = np.lexsort((Av["iid"], Av["t"]))
    Av = {k: v[order] for k, v in Av.items()}
    rows = zip(["%012x" % x for x in Av["iid"].tolist()], ["za_%010x" % a for a in Av["acct"].tolist()],
               Av["plat"].tolist(), stamp(Av["t"]), Av["media"].tolist(), Av["cid"].tolist(), Av["re"].tolist())
    counts["attr"] = _w(os.path.join(target, FILES["attr"]),
                        ["install_id", "account_id", "platform", "install_time", "media_source", "campaign_id",
                         "is_reinstall"], rows)
    counts["resent"], counts["reinstalls"] = int(rs.size), int(ri.size)

    # ---- the networks' install postbacks: one per install of an iOS network, no account ----------------------
    r = rng_of(8)
    gated = np.isin(src, [C.ORDER.index(c) for c in C.GATED])
    g = np.where(gated)[0]
    net = np.array([SKAN_NET.get(c, "") for c in C.ORDER] + ["", ""])[src[g]]
    p_t = (day[g] + W["pb_lag"][g]) * 86400 + r.integers(0, 86400, g.size)
    p_cv = W["cv"][g]
    p_cid = cid[g]
    p_re = np.full(g.size, "false")
    ex = r.choice(g.size, int(0.008 * g.size), replace=False)         # redownloads the networks also report
    e_t = p_t[ex] + r.integers(5, 240, ex.size) * 86400
    ok = e_t < (C.WEEKS * 7 + 4) * 86400
    ex, e_t = ex[ok], e_t[ok]
    pid = uniq(r, g.size + ex.size, 60)
    P = dict(pid=np.concatenate([pid[:g.size], pid[g.size:]]), net=np.concatenate([net, net[ex]]),
             cid=np.concatenate([p_cid, p_cid[ex]]), t=np.concatenate([p_t, e_t]),
             cv=np.concatenate([p_cv, p_cv[r.permutation(ex.size)] if ex.size else p_cv[:0]]),
             re=np.concatenate([p_re, np.full(ex.size, "true")]))
    dd = r.choice(P["pid"].size, int(0.003 * P["pid"].size), replace=False)   # a postback delivered twice
    P = {k: np.concatenate([v, v[dd]]) for k, v in P.items()}
    P["t"][-dd.size:] += r.integers(20, 4000, dd.size)
    order = np.lexsort((P["pid"], P["t"]))
    P = {k: v[order] for k, v in P.items()}
    rows = zip(["%015x" % x for x in P["pid"].tolist()], P["net"].tolist(), P["cid"].tolist(), stamp(P["t"]),
               P["cv"].tolist(), P["re"].tolist())
    counts["skan"] = _w(os.path.join(target, FILES["skan"]),
                        ["postback_id", "ad_network", "campaign_id", "received_at", "conversion_value", "redownload"], rows)
    counts["redownloads"], counts["postbacks_twice"] = int(ex.size), int(dd.size)

    # ---- the ad platforms' daily spend, campaign by campaign ---------------------------------------------------
    r = rng_of(9)
    rows = []
    trailing = 0
    for ci, c in enumerate(C.ORDER):
        cs = camps[c]
        mk = src == ci
        inst = np.zeros((C.WEEKS * 7, len(cs)))
        np.add.at(inst, (day[mk], camp_ix[mk]), 1)
        tilt, live = C.CH[c]["tilt"], C.CH[c]["live"]
        mkt = np.array([x["market"] for x in cs])
        wts = np.array([x["wt"] for x in cs])
        on = np.array([x["on"] for x in cs])                           # campaign by week
        for w in range(C.WEEKS):
            act = on[:, w]
            share = tilt * live[:, w] * np.array(MARKET_COST) * np.exp(0.08 * r.normal(size=3))
            within = np.array([wts[j] / wts[act & (mkt == mkt[j])].sum() if act[j] else 0.0 for j in range(len(cs))])
            dayw = 1 + 0.07 * r.normal(size=7)
            grid = np.outer(dayw, share[mkt] * within) * np.exp(0.10 * r.normal(size=(7, len(cs))))
            # a campaign paused at the weekend still bills a little on the Monday, sometimes the Tuesday
            if w:
                for j in np.where(on[:, w - 1] & ~act)[0]:
                    if r.random() < 0.7:
                        k_ = 1 + int(r.random() < 0.3)
                        grid[:k_, j] = grid[:, act].mean() * r.uniform(0.002, 0.02, k_)
            cents = cents_split(int(round(W["B"][c]["spend"][w] * 100)), grid)
            season = {11: 1.18, 12: 1.25, 1: 0.92}.get(int(C.WMONTH[w]), 1.0)
            for k in range(7):
                d = w * 7 + k
                for j in np.where(cents[k] > 0)[0]:
                    sp = cents[k, j] / 100.0
                    cpm = CPM[c] * season * float(np.exp(0.16 * r.normal()))
                    imp = int(sp / cpm * 1000)
                    ctr = (0.055 if c == "Apple Search Ads" else 0.011) * float(np.exp(0.25 * r.normal()))
                    ni = inst[d, j]
                    if act[j]:
                        rep = int(round(ni * REPORTED[c] * (1 + 0.05 * r.normal()))) if ni else int(r.random() < 0.15)
                    else:
                        rep = int(r.random() < 0.2)
                        trailing += 1
                    rows.append([date_of(d), SOURCE[c][0], SOURCE[c][1], cs[j]["id"], cs[j]["name"], COUNTRIES[mkt[j]],
                                 "%.2f" % sp, imp, int(imp * ctr), rep])
    rows.sort(key=lambda x: (x[0], x[1], x[2], x[3]))
    counts["spend"] = _w(os.path.join(target, FILES["spend"]),
                         ["date", "network", "os", "campaign_id", "campaign_name", "country", "spend_eur", "impressions",
                          "clicks", "installs_reported_by_network"], rows)
    counts["trailing"] = trailing
    counts["creat"], counts["rate"] = other_files(target, camps)
    return dict(counts=counts, aid=aid, camps=camps, csec=csec, sec=sec, staff=ns, camp_ix=camp_ix)


def other_files(target, camps):
    """the creative team's test log and the stores' daily ratings: the organisation's, and no part of the analysis"""
    r = rng_of(12)
    rows = []
    tid = 3100
    for j in range(137):
        c = C.ORDER[int(r.integers(0, len(C.ORDER)))]
        cs = camps[c]
        cp = cs[int(r.integers(0, len(cs)))]
        start = DAY0 + dt.timedelta(days=int(r.integers(60, 700)))
        length = int(r.choice([7, 10, 14, 14, 21]))
        arms = int(r.choice([2, 2, 2, 3]))
        tid += int(r.integers(1, 6))
        base_ctr = 0.006 + 0.012 * r.random()
        for a in range(arms):
            imp = int(r.integers(18000, 520000))
            ctr = base_ctr * float(np.exp(0.22 * r.normal()))
            clicks = int(imp * ctr)
            rows.append(["ct%04d" % tid, SOURCE[c][0], SOURCE[c][1], cp["id"], "cr_%06d" % int(r.integers(1, 999999)),
                         "ABCD"[a], start.isoformat(), (start + dt.timedelta(days=length)).isoformat(), imp, clicks,
                         int(clicks * (0.04 + 0.11 * r.random()))])
    a = _w(os.path.join(target, FILES["creat"]),
           ["test_id", "network", "os", "campaign_id", "creative_id", "arm", "start_date", "end_date", "impressions",
            "clicks", "installs_reported_by_network"], rows)
    rr = []
    level = {"app_store": 4.52, "google_play": 4.31}
    for d in range((dt.date(2026, 10, 31) - DAY0).days + 1):
        for st in ("app_store", "google_play"):
            for cc, lam in (("ES", 8.6), ("IT", 3.9), ("PT", 2.3)):
                k = int(r.poisson(lam * (1.35 if st == "google_play" else 1.0)))
                if k:
                    stars = r.choice(5, k, p=_stars(level[st])) + 1
                    rr.append([(DAY0 + dt.timedelta(days=d)).isoformat(), st, cc, k, "%.2f" % stars.mean()])
    b = _w(os.path.join(target, FILES["rate"]), ["date", "store", "country", "ratings", "average_rating"], rr)
    return a, b


def _stars(mean):
    p = np.array([0.05, 0.03, 0.06, 0.2, 0.66])
    p[4] += (mean - 4.39) * 0.25
    p[0] -= (mean - 4.39) * 0.25
    return p / p.sum()


if __name__ == "__main__":
    import time
    t0 = time.time()
    W = C.simulate()
    out = build(W, sys.argv[1])
    print(out["counts"], "%.0fs" % (time.time() - t0))
