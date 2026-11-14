"""The shipped records, written from the simulated world: the app's accounts and billing events, the attribution
partner's install export, the ad networks' install postbacks, both stores' daily subscription reports, the daily
ad spend, and two files the analysis does not use (creative tests, store ratings)."""
import collections
import csv
import datetime as dt
import os

import numpy as np

import params as P

FILES = {
    "acc": "accounts_2026-11-09.csv",
    "bill": "billing_events_2024-11-04_2026-11-08.csv",
    "attr": "attribution_installs_2024-11-04_2026-11-08.csv",
    "skan": "skan_postbacks_2024-11-04_2026-11-08.csv",
    "apple": "appstore_subscription_events_daily_2024-11_2026-11.csv",
    "google": "googleplay_subscription_transactions_daily_2024-11_2026-11.csv",
    "spend": "ad_spend_daily_2024-11-04_2026-11-08.csv",
    "creat": "creative_tests_2025-2026.csv",
    "rate": "store_ratings_daily_2024-11_2026-10.csv",
}
SOURCE = {"Meta iOS": "Meta Ads", "TikTok iOS": "TikTok For Business", "Apple Search Ads": "Apple Search Ads",
          "Meta Android": "Meta Ads", "Google Android": "Google Ads", "TikTok Android": "TikTok For Business",
          "AppLovin Android": "AppLovin"}
SKAN_NET = {"Meta iOS": "meta", "TikTok iOS": "tiktok"}
REPORTED = {"Meta iOS": 1.18, "TikTok iOS": 1.22, "Apple Search Ads": 1.0, "Meta Android": 1.06, "Google Android": 1.08,
            "TikTok Android": 1.10, "AppLovin Android": 1.01}
UTC = dt.timezone.utc


def _w(path, header, rows):
    with open(path, "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)
    return len(rows)


def ts(day, sec):
    t = dt.datetime.combine(P.day_date(day), dt.time(0, 0), tzinfo=UTC) + dt.timedelta(seconds=int(sec))
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


def ids(rng, n, prefix, width):
    raw = rng.choice(16 ** width, size=n * 2, replace=False)[:n]
    return np.array(["%s%0*x" % (prefix, width, r) for r in raw])


def campaigns(rng, c, p):
    base = {"Meta iOS": 2300, "TikTok iOS": 4100, "Apple Search Ads": 7700, "Meta Android": 3300,
            "Google Android": 5500, "TikTok Android": 6100, "AppLovin Android": 8800}[c]
    camp = [str(base + 11 * i + int(rng.integers(0, 9))) for i in range(p["camps"])]
    share = rng.dirichlet(np.ones(p["camps"]) * (1.4 if p["camps"] > 8 else 3.0))
    return camp, share


def write(W, target, rng):
    """returns the per-account frame the analysis-side checks use (never shipped as such)"""
    acc_rows, bill_rows, attr_rows, skan_rows = [], [], [], []
    store = collections.Counter()           # (store, local date, product, country, event) -> units
    spend_rows = []
    frame = {}
    NT = {k: {pl: P.net_of(P.PRICE[pl], k) for pl in P.PRICE} for k in P.COUNTRIES}
    seq = 0
    for c in list(P.CHANNELS) + list(P.ORGANIC):
        L = W["acc"][c]
        p = P.CHANNELS.get(c) or P.ORGANIC[c]
        n = L["e"].size
        aid = ids(rng, n, "za_", 10)
        iid = ids(rng, n, "", 12)
        sec = rng.integers(0, 86400, n)
        plat = "ios" if p["ios"] else "android"
        camp, share = campaigns(rng, c, p) if c in P.CHANNELS else ([""], np.array([1.0]))
        ci = rng.choice(len(camp), n, p=share)
        cc = np.array(P.COUNTRIES)[L["country"]]
        att = np.where(L["consent"], "authorized", "denied") if p["ios"] else np.full(n, "")
        if p["ios"]:
            nd = rng.random(n) < 0.03
            att = np.where(nd & ~L["consent"], "not_determined", att)
        frame[c] = dict(aid=aid, camp=np.array(camp)[ci])
        for i in range(n):
            d = int(L["day"][i]); s = int(sec[i])
            plan = "annual" if L["annual"][i] else ("monthly" if L["conv"][i] else "")
            seen = str(L["plan_seen"][i])
            lo_day = int(L["last_open"][i])
            lo_sec = (s + 3600 * int(rng.integers(1, 14))) % 86400
            auto = ("yes" if L["auto_on"][i] else "no") if seen else ""
            acc_rows.append([aid[i], ts(d, s), plat, cc[i], "consumer", att[i], int(L["cv"][i]), ts(lo_day, lo_sec),
                             seen, auto])
            # attribution partner: paid iOS ad installs only with consent
            src = SOURCE.get(c, "organic")
            cid = camp[ci[i]] if c in P.CHANNELS else ""
            if c in SKAN_NET and not L["consent"][i]:
                src, cid = "organic", ""
            attr_rows.append([iid[i], aid[i], plat, ts(d, s + 40 + int(rng.integers(0, 600))), src, cid,
                              att[i] if p["ios"] else "", "false"])
            if c in SKAN_NET:
                skan_rows.append([SKAN_NET[c], camp[ci[i]], d, int(L["cv"][i])])
            # charges
            if not L["conv"][i]:
                continue
            prod = P.PRODUCT[plan]
            st = "app_store" if p["ios"] else "google_play"
            if L["annual"][i]:
                evs = []
                if L["a0"][i]:
                    evs.append((int(L["conv_day"][i]), "first_charge", 0))
                if L["aren"][i]:
                    evs.append((int(L["conv_day"][i]) + 365, "renewal", 1))
                kinds = [("Paid Subscription from Free Trial" if L["trial"][i] else "Subscribe") if e[1] == "first_charge"
                         else "Renew" for e in evs]
            else:
                ks = np.nonzero(L["charge"][i])[0]
                evs = [(int(L["rdays"][i, k]), "first_charge" if k == 0 else "renewal", int(k)) for k in ks]
                kinds = [("Paid Subscription from Free Trial" if L["trial"][i] else "Subscribe") if k == 0 else "Renew"
                         for _, _, k in evs]
            csec = (s + 7 * 86400) % 86400 if L["trial"][i] else (s + 1800) % 86400
            for (cd, et, k), kind in zip(evs, kinds):
                tstamp = dt.datetime.combine(P.day_date(cd), dt.time(0), tzinfo=UTC) + dt.timedelta(seconds=csec)
                store[(st, _local(tstamp, st), prod, cc[i], kind)] += 1
                if cd <= lo_day:
                    rec_day = min(cd + int(rng.integers(0, 4)), lo_day)
                    seq += 1
                    bill_rows.append(["be%08d" % seq, aid[i], st, "production", prod, et,
                                      tstamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
                                      ts(rec_day, max(csec, lo_sec) if rec_day == lo_day else (csec + 2000) % 86400),
                                      "%.2f" % P.PRICE[plan], cc[i]])
                if not L["annual"][i] and L["refund"][i, k]:
                    rd = cd + int(rng.integers(1, 12))
                    rt = dt.datetime.combine(P.day_date(rd), dt.time(0), tzinfo=UTC) + dt.timedelta(seconds=int(rng.integers(0, 86400)))
                    store[(st, _local(rt, st), prod, cc[i], "Refund")] += 1
                    if rd <= lo_day:
                        seq += 1
                        bill_rows.append(["be%08d" % seq, aid[i], st, "production", prod, "refund",
                                          rt.strftime("%Y-%m-%dT%H:%M:%SZ"), ts(min(rd + 1, lo_day), 43000),
                                          "-%.2f" % P.PRICE[plan], cc[i]])
    return acc_rows, bill_rows, attr_rows, skan_rows, store, frame


def _local(t, st):
    """Apple reports in Pacific time, Google in UTC"""
    if st == "app_store":
        off = -7 if 3 <= t.month <= 10 else -8
        t = t + dt.timedelta(hours=off)
    return t.date()


def coarse_of(cv):
    trial, paid, bucket = (cv >> 3) & 1, (cv >> 4) & 1, cv & 7
    return "high" if (paid or (trial and bucket >= 4)) else ("medium" if trial else "low")


def skan_out(skan_rows, rng):
    """one postback per ad install: the fine value only where the campaign's installs over the past week reach Apple's
    crowd-anonymity tier, the coarse value at the tier below, neither below that"""
    wk = collections.Counter()
    for net, cid, d, cv in skan_rows:
        wk[(net, cid, d // 7)] += 1
    out = []
    for j, (net, cid, d, cv) in enumerate(skan_rows):
        n7 = wk[(net, cid, d // 7)]
        pdays = d + 3 + int(rng.integers(0, 2))
        if pdays > P.END_DAY:
            continue                                   # not yet arrived at the pull
        fine = str(cv) if n7 >= 35 else ""
        coarse = coarse_of(cv) if n7 >= 12 else ""
        sid = cid[-4:] if n7 >= 35 else cid[-2:]
        out.append([net, sid, P.day_date(pdays).isoformat(), "%02d:%02d" % (rng.integers(0, 24), rng.integers(0, 60)),
                    fine, coarse, "1", "false"])
    order = sorted(range(len(out)), key=lambda k: (out[k][2], out[k][3], out[k][0], out[k][1]))
    return [["pb%07d" % (k + 1)] + out[i] for k, i in enumerate(order)]


def store_rows(store):
    apple, google = [], []
    vat = P.VAT
    for (st, day, prod, cc, kind), u in sorted(store.items(), key=lambda kv: (kv[0][1], kv[0][0], kv[0][2], kv[0][3], kv[0][4])):
        if day < P.LAUNCH or day > P.DATA_END:
            continue
        price = P.PRICE["monthly" if prod.endswith("monthly") else "annual"]
        sign = -1 if kind == "Refund" else 1
        cust = sign * u * price
        proc = sign * u * price / (1 + vat[cc]) * (1 - P.COMMISSION)
        if st == "app_store":
            apple.append([day.isoformat(), prod, cc, kind, u, "%.2f" % cust, "%.2f" % proc])
        else:
            tt = {"Paid Subscription from Free Trial": "charge_new", "Subscribe": "charge_new", "Renew": "charge_renewal",
                  "Refund": "refund"}[kind]
            google.append([day.isoformat(), prod, cc, tt, u, "%.2f" % cust, "%.2f" % proc])
    # Google reports a new charge once per day and type: merge the two starting kinds
    g = collections.OrderedDict()
    for r in google:
        k = tuple(r[:4])
        if k in g:
            g[k][4] += r[4]; g[k][5] = "%.2f" % (float(g[k][5]) + float(r[5])); g[k][6] = "%.2f" % (float(g[k][6]) + float(r[6]))
        else:
            g[k] = list(r)
    return apple, list(g.values())


def spend_rows(W, frame, rng):
    rows = []
    for c, p in P.CHANNELS.items():
        L = W["acc"][c]
        camps = sorted(set(frame[c]["camp"]))
        inst = collections.Counter(zip(L["day"].tolist(), frame[c]["camp"].tolist()))
        share = {k: sum(1 for x in frame[c]["camp"] if x == k) / len(frame[c]["camp"]) for k in camps}
        for w in range(len(W["budgets"][c])):
            b = W["budgets"][c][w]
            dayw = 1 + 0.08 * rng.normal(size=7)
            dayw = dayw / dayw.sum()
            for k in range(7):
                d = w * 7 + k
                if d > P.END_DAY:
                    break
                for cid in camps:
                    sp = b * dayw[k] * share[cid] * (1 + 0.05 * rng.normal())
                    ni = inst.get((d, cid), 0)
                    rep = int(round(ni * REPORTED[c] * (1 + 0.06 * rng.normal()))) if ni else int(rng.random() < 0.2)
                    imp = int(sp / (4.2 + 2.0 * rng.random()) * 1000)
                    clk = int(imp * (0.006 + 0.01 * rng.random()))
                    rows.append([P.day_date(d).isoformat(), c, cid, "%.2f" % max(sp, 0.0), imp, clk, rep])
    return rows


def staff_accounts(rng, n=137):
    rows, bills = [], []
    for j in range(n):
        aid = "za_%010x" % int(rng.integers(16 ** 9, 16 ** 10))
        d = int(rng.integers(0, P.END_DAY - 30)); ios = rng.random() < 0.6
        kind = "staff" if j % 3 else "test"
        rows.append([aid, ts(d, int(rng.integers(0, 86400))), "ios" if ios else "android", "ES", kind,
                     "authorized" if ios else "", int(rng.integers(0, 32)), ts(min(d + int(rng.integers(5, 200)), P.END_DAY), 50000),
                     "monthly", "yes"])
        for k in range(int(rng.integers(1, 6))):
            cd = d + 7 + 30 * k
            if cd > P.END_DAY:
                break
            bills.append([None, aid, "app_store" if ios else "google_play", "sandbox", P.PRODUCT["monthly"],
                          "first_charge" if k == 0 else "renewal", ts(cd, 36000), ts(cd, 36100), "9.99", "ES"])
    return rows, bills


def build(W, target, rng):
    os.makedirs(target, exist_ok=True)
    acc, bill, attr, skan, store, frame = write(W, target, rng)
    sa, sb = staff_accounts(rng)
    acc += sa
    seq = len(bill)
    for b in sb:
        seq += 1; b[0] = "be%08d" % seq
    bill += sb
    # the attribution partner re-sends some rows after an SDK retry; second devices show as reinstalls
    extra = []
    for r in attr:
        u = rng.random()
        if u < 0.008:
            extra.append(list(r[:3]) + [r[3][:-3] + "%02dZ" % int(rng.integers(0, 60))] + list(r[4:]))
        elif u < 0.038:
            d0 = dt.datetime.strptime(r[3], "%Y-%m-%dT%H:%M:%SZ") + dt.timedelta(days=int(rng.integers(3, 300)))
            if d0.date() <= P.DATA_END:
                extra.append(["%012x" % int(rng.integers(16 ** 11, 16 ** 12)), r[1], r[2], d0.strftime("%Y-%m-%dT%H:%M:%SZ"),
                              "organic", "", r[6], "true"])
    attr = sorted(attr + extra, key=lambda r: (r[3], r[0]))
    acc.sort(key=lambda r: (r[1], r[0]))
    bill.sort(key=lambda r: (r[6], r[0]))
    n = {}
    n["acc"] = _w(os.path.join(target, FILES["acc"]), ["account_id", "created_at", "platform", "country", "account_type",
              "att_status", "first_48h_value", "last_open_at", "plan_at_last_open", "auto_renew_at_last_open"], acc)
    n["bill"] = _w(os.path.join(target, FILES["bill"]), ["event_id", "account_id", "store", "environment", "product_id",
               "event_type", "transaction_at", "recorded_at", "price_eur", "storefront"], bill)
    n["attr"] = _w(os.path.join(target, FILES["attr"]), ["install_id", "account_id", "platform", "install_time",
               "media_source", "campaign_id", "att_status", "is_reinstall"], attr)
    n["skan"] = _w(os.path.join(target, FILES["skan"]), ["postback_id", "ad_network", "source_identifier",
               "postback_date", "postback_time_utc", "conversion_value", "coarse_conversion_value", "fidelity_type",
               "redownload"], skan_out(skan, rng))
    apple, google = store_rows(store)
    n["apple"] = _w(os.path.join(target, FILES["apple"]), ["date_pacific", "product_id", "country", "event", "units",
                "customer_price_eur", "developer_proceeds_eur"], apple)
    n["google"] = _w(os.path.join(target, FILES["google"]), ["date_utc", "product_id", "country", "transaction_type",
                 "transactions", "amount_eur", "net_eur"], google)
    n["spend"] = _w(os.path.join(target, FILES["spend"]), ["date", "channel", "campaign_id", "spend_eur", "impressions",
                "clicks", "installs_reported_by_network"], spend_rows(W, frame, rng))
    n["creat"], n["rate"] = distractors(target, rng)
    return n, frame


def distractors(target, rng):
    rows = []
    for j in range(260):
        c = P.ORDER[int(rng.integers(0, len(P.ORDER)))]
        start = P.day_date(int(rng.integers(150, 700)))
        imp = int(rng.integers(20000, 600000)); ctr = 0.004 + 0.012 * rng.random()
        rows.append(["ct%04d" % (j + 1), c, "cr_%05d" % int(rng.integers(1, 99999)), ["A", "B"][j % 2], start.isoformat(),
                     (start + dt.timedelta(days=14)).isoformat(), imp, int(imp * ctr), "%.4f" % ctr,
                     int(imp * ctr * (0.05 + 0.1 * rng.random()))])
    a = _w(os.path.join(target, FILES["creat"]), ["test_id", "channel", "creative_id", "arm", "start_date", "end_date",
           "impressions", "clicks", "ctr", "installs_reported_by_network"], rows)
    rr = []
    for d in range((dt.date(2026, 10, 31) - P.LAUNCH).days + 1):
        for st in ("app_store", "google_play"):
            for cc in P.COUNTRIES:
                k = int(rng.poisson({"ES": 9, "IT": 4, "PT": 2.5}[cc] * (1.3 if st == "google_play" else 1.0)))
                if k:
                    rr.append([P.day_date(d).isoformat(), st, cc, k, "%.2f" % min(5.0, max(1.0, 4.45 + 0.35 * rng.normal()))])
    b = _w(os.path.join(target, FILES["rate"]), ["date", "store", "country", "ratings", "average_rating"], rr)
    return a, b
