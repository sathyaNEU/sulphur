"""task1 architecture 7: an independent recomputation of the golden from the shipped files.

    python3 task1/generator/verify.py

Nothing here imports the generator. The pack is read with pandas, the documents with pdftotext and openpyxl, and each
step is written again from the answer blocks' own description: the stores' excess over the billing records put on the
subscriptions that were set to take it, one ratio per source fitted across market-weeks, the response fitted on the
budget with the platform's delivery beside it and carried to the plan. The continuation is fitted by a bounded
scalar minimiser where the golden finishes a grid search, a day's half is rounded up where the golden rounds to
even, the App Store's days come from the tz database, and the least squares are solved by their normal equations.
Every graded figure is then held against figures.json, the golden CSV and the golden workbook."""
import glob
import json
import math
import os
import re
import subprocess
import sys

import numpy as np
import pandas as pd
from openpyxl import load_workbook
from scipy.optimize import minimize_scalar

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
G = os.path.join(TASK, "golden")
DAY0 = pd.Timestamp("2024-11-04", tz="UTC")
END_DAY = (pd.Timestamp("2026-11-08", tz="UTC") - DAY0).days          # the pull
PERIOD = 365.25 / 12                                                   # 30.4375 days
WEEKS, FULL = 104, 52
N = {"pass": 0, "fail": 0}
MEDIA = {("Meta Ads", "ios"): "Meta iOS", ("TikTok For Business", "ios"): "TikTok iOS", ("Snapchat Ads", "ios"): "Snapchat iOS",
         ("Google Ads", "ios"): "Google iOS", ("Pinterest Ads", "ios"): "Pinterest iOS",
         ("Apple Search Ads", "ios"): "Apple Search Ads", ("Google Ads", "android"): "Google Android",
         ("AppLovin", "android"): "AppLovin Android", ("organic", "ios"): "organic iOS", ("organic", "android"): "organic Android"}
POSTBACK = {"meta": "Meta iOS", "tiktok": "TikTok iOS", "snapchat": "Snapchat iOS", "google": "Google iOS",
            "pinterest": "Pinterest iOS"}
NETWORKS = list(POSTBACK.values())                                     # the iOS channels the export names only in part
MKT = {"ES": 0, "IT": 1, "PT": 2}


def ok(label, cond, detail=""):
    N["pass" if cond else "fail"] += 1
    print(("PASS  " if cond else "FAIL  ") + label + ("" if cond else "  %s" % (detail,)))


def one(pattern):
    hits = glob.glob(os.path.join(T, pattern))
    assert len(hits) == 1, (pattern, hits)
    return hits[0]


def read(pattern, **kw):
    return pd.read_csv(one(pattern), dtype=str, keep_default_na=False, **kw)


def stamp(s):
    return pd.to_datetime(s, utc=True)


def day_of(ts):
    return ((ts - DAY0) // pd.Timedelta(days=1)).to_numpy(np.int64)


def pacific_day(ts):
    """the day a UTC time falls on in the App Store's reporting zone"""
    local = pd.DatetimeIndex(ts).tz_convert("America/Los_Angeles").tz_localize(None).normalize()
    return ((local - pd.Timestamp("2024-11-04")) // pd.Timedelta(days=1)).to_numpy(np.int64)


def period(day):
    return np.floor(np.maximum(np.asarray(day, float), 0) / PERIOD).astype(int)


def up(x):
    """rounded to the day, a half going up"""
    return np.floor(np.asarray(x, float) + 0.5).astype(np.int64)


def month_of(date):
    return pd.DatetimeIndex(date).month.to_numpy()


def band_name(x, hold, scale):
    return "scale" if x >= scale else ("hold" if x >= hold else "cut")


def wls(X, y, w):
    """weighted least squares through the normal equations"""
    XtW = X.T * w
    return np.linalg.solve(XtW @ X, XtW @ y)


def main():
    fig = json.load(open(os.path.join(HERE, "figures.json")))

    # ------------------------------------------------------------------------------------------------------------
    # the documents
    # ------------------------------------------------------------------------------------------------------------
    pol = " ".join(subprocess.run(["pdftotext", "-layout", one("growth_policy*.pdf"), "-"], capture_output=True,
                                  text=True).stdout.split())
    m = re.search(r"scale when the return is (\d+\.\d+) or more, hold when it is (\d+\.\d+) or more and under (\d+\.\d+), "
                  r"and cut when it is under (\d+\.\d+)", pol)
    SCALE, HOLD = float(m.group(1)), float(m.group(2))
    ok("policy: the lines read 0.90 and 1.20", (HOLD, SCALE) == (0.90, 1.20) and m.group(3) == "1.20" and m.group(4) == "0.90")
    m = re.search(r"Spain (\d+) per cent, Italy (\d+) per cent, Portugal (\d+) per cent", pol)
    VAT = {"ES": int(m.group(1)) / 100.0, "IT": int(m.group(2)) / 100.0, "PT": int(m.group(3)) / 100.0}
    COMM = int(re.search(r"commission of (\d+) per cent", pol).group(1)) / 100.0
    FEE = int(re.search(r"fee of (\d+) per cent", pol).group(1)) / 100.0
    m = re.search(r"EUR ([\d.]+) a month and EUR ([\d.]+) a year, each with a (\w+)-day free trial", pol)
    P_M, P_A = float(m.group(1)), float(m.group(2))
    ok("policy: VAT 21, 22 and 23 per cent, the stores' 15, the checkout's 3, EUR 9.99 and 59.99, a seven-day trial",
       VAT == {"ES": 0.21, "IT": 0.22, "PT": 0.23} and (COMM, FEE, P_M, P_A, m.group(3)) == (0.15, 0.03, 9.99, 59.99, "seven"))
    ok("policy: the 365 days from the install, every charge the stores or the checkout made, refunds out",
       "in the 365 days from the install, each at the time of the transaction, less the net revenue of any of those charges "
       "refunded" in pol)
    schema = json.load(open(one("skadnetwork_conversion_values.json")))
    ok("schema: a 48-hour window, the postback 24 to 48 hours after it closes, sessions in bits 0 to 2, the trial in bit 3",
       schema["postback"]["measurement_window_hours"] == 48 and schema["postback"]["sent_after_window_closes_hours"] == [24, 48]
       and schema["fine_value_bits"]["0-2"]["name"] == "sessions_bucket" and schema["fine_value_bits"]["3"]["name"] == "trial_started")

    plan_wb = load_workbook(one("media_plan_2027.xlsx"), read_only=True, data_only=True)
    grow = list(plan_wb["Growth channels"].iter_rows(values_only=True))
    stre = list(plan_wb["Stretch case"].iter_rows(values_only=True))
    MEMBERS = [x for x in grow[3][2:] if x and x != "Total"]
    plan = {c: np.array([float(r[grow[3].index(c)]) for r in grow[4:56]]) for c in MEMBERS}
    stretch = {c: np.array([float(r[stre[3].index(c)]) for r in stre[4:56]]) for c in MEMBERS}
    plan_monday = pd.DatetimeIndex([r[0] for r in grow[4:56]])
    ok("plan: seven growth channels, 52 weeks from Monday 4 January 2027, a stretch column above each week's spend",
       len(MEMBERS) == 7 and len(plan_monday) == 52 and plan_monday[0] == pd.Timestamp("2027-01-04")
       and (np.diff(plan_monday.to_numpy()) == np.timedelta64(7, "D")).all()
       and all((stretch[c] > plan[c]).all() for c in MEMBERS) and [r[0] for r in stre[4:56]] == [r[0] for r in grow[4:56]])
    ok("plan: each channel's stretch is one multiple of its plan in every week",
       all(np.ptp(stretch[c] / plan[c]) < 1e-9 for c in MEMBERS))
    bud = list(load_workbook(one("paid_budgets_weekly_*.xlsx"), read_only=True, data_only=True)["Weekly budgets"]
               .iter_rows(values_only=True))
    CHANNELS = [x for x in bud[2][1:] if x and x != "Total"]
    body = [r for r in bud[3:] if r[0] is not None]
    budget = {c: np.array([float(r[bud[2].index(c)]) for r in body]) for c in CHANNELS}
    ok("budgets: eight channels, 104 weeks from Monday 4 November 2024",
       len(CHANNELS) == 8 and len(body) == WEEKS and body[0][0] == pd.Timestamp("2024-11-04").to_pydatetime()
       and set(MEMBERS) < set(CHANNELS))
    COMPLETE = [c for c in CHANNELS if c not in NETWORKS]              # every install of theirs carries its channel

    # ------------------------------------------------------------------------------------------------------------
    # accounts and charges
    # ------------------------------------------------------------------------------------------------------------
    acc = read("accounts_*.csv")
    n_all = len(acc)
    acc = acc[acc.account_type == "consumer"].reset_index(drop=True)
    n = len(acc)
    ix = pd.Index(acc.account_id)
    created = stamp(acc.created_at)
    day = day_of(created)
    tod = (created - created.dt.normalize()).dt.total_seconds().to_numpy().astype(np.int64)
    week = day // 7
    last_open = day_of(stamp(acc.last_open_at))
    ios = (acc.platform == "ios").to_numpy()
    market = acc.storefront.map(MKT).to_numpy()
    cv = acc.conversion_value_48h.astype(int).to_numpy()
    allowed = (acc.tracking_status == "authorized").to_numpy()
    state, sub_store = acc.sub_state_at_last_open.to_numpy(), acc.sub_store_at_last_open.to_numpy()
    sub_plan, auto = acc.sub_plan_at_last_open.to_numpy(), (acc.auto_renew_at_last_open == "yes").to_numpy()
    on_web = sub_store == "web"
    full = week < FULL
    ok("accounts: %d rows, %d consumer accounts, installs from 4 November 2024 to 1 November 2026" % (n_all, n),
       n == fig["steps"]["consumer_accounts"] and n_all - n == fig["steps"]["other_accounts"] and ix.is_unique
       and day.min() == 0 and week.max() == WEEKS - 1)
    vat_acc = acc.storefront.map(VAT).to_numpy()
    net_m = P_M / (1 + vat_acc) * np.where(on_web, 1 - FEE, 1 - COMM)
    net_a = P_A / (1 + vat_acc) * np.where(on_web, 1 - FEE, 1 - COMM)

    bil = read("billing_events_*.csv")
    bil = bil[(bil.environment == "production") & bil.account_id.isin(ix)]
    bil = bil.drop_duplicates(["account_id", "product_id", "event_type", "transaction_at"])
    refunded = set(bil.refund_of_event_id[bil.event_type == "refund"])
    made = bil[bil.event_type != "refund"].copy()                      # every charge made, the refunded ones among them
    made["ts"] = stamp(made.transaction_at)
    made["d"] = day_of(made.ts)
    made["i"] = ix.get_indexer(made.account_id)
    made["monthly"] = made.product_id.str.endswith("monthly")
    made["net"] = made.amount_eur.astype(float) / (1 + made.storefront.map(VAT)) * np.where(made.store == "web", 1 - FEE, 1 - COMM)
    gone = made[made.event_id.isin(refunded)]
    kept = made[~made.event_id.isin(refunded)]                         # the charges that stood
    ok("billing: %d refunded purchases, each a first charge on a store" % len(refunded),
       len(refunded) == fig["steps"]["refunded_purchases"] == len(gone) and (gone.event_type == "first_charge").all()
       and (gone.store != "web").all())
    ok("billing: a charge's storefront and route are its account's",
       (made.storefront.to_numpy() == acc.storefront.to_numpy()[made.i]).all()
       and ((made.store == "web").to_numpy() == on_web[made.i]).all())
    inside = kept.d.to_numpy() < day[kept.i.to_numpy()] + 365
    rec12 = np.bincount(kept.i.to_numpy()[inside], weights=kept.net.to_numpy()[inside], minlength=n)

    km = kept[kept.monthly]
    n_m = np.bincount(km.i, minlength=n)
    first_m = km[km.event_type == "first_charge"]
    first_day = np.full(n, -1, np.int64); first_day[first_m.i] = first_m.d
    first_tod = tod.copy()
    ft = (first_m.ts - first_m.ts.dt.normalize()).dt.total_seconds().to_numpy().astype(np.int64)
    first_tod[first_m.i.to_numpy()] = ft
    last_m = np.full(n, -1, np.int64)
    np.maximum.at(last_m, km.i.to_numpy(), km.d.to_numpy())
    ka = kept[~kept.monthly & (kept.event_type == "first_charge")]
    has_a = np.zeros(n, bool); has_a[ka.i] = True
    a_day = np.full(n, -1, np.int64); a_day[ka.i] = ka.d
    ok("billing: a monthly subscription's charges on file run from its first with no gap, %s days apart rounded to the day" % PERIOD,
       (n_m[first_m.i] >= 1).all() and (n_m[first_day < 0] == 0).all()
       and bool((np.abs(last_m[n_m > 0] - (first_day[n_m > 0] + (n_m[n_m > 0] - 1) * PERIOD)) <= 0.5).all()))

    # ------------------------------------------------------------------------------------------------------------
    # the stores against the records, by period, each charge on its store's own day
    # ------------------------------------------------------------------------------------------------------------
    NP = int(END_DAY // PERIOD) + 1
    ap, gp = read("appstore_subscription_events_*.csv"), read("googleplay_subscription_transactions_*.csv")
    rep = {}
    for name, df, dcol, ecol, ucol, kinds in (
            ("App Store", ap, "date_pt", "event", "units",
             {"Paid Subscription from Free Trial": "first", "Subscribe": "first", "Renew": "renewal", "Refund": "refund"}),
            ("Google Play", gp, "date_utc", "transaction_type", "transactions",
             {"charge_new": "first", "charge_renewal": "renewal", "refund": "refund"})):
        d = ((pd.to_datetime(df[dcol]) - pd.Timestamp("2024-11-04")) // pd.Timedelta(days=1)).to_numpy()
        kind, mon, units = df[ecol].map(kinds), df.product_id.str.endswith("monthly"), df[ucol].astype(int).to_numpy()
        assert kind.notna().all()
        rep[name] = {(k, mm): np.bincount(period(d[(kind == k) & (mon == mm)]), weights=units[(kind == k) & (mon == mm)],
                                          minlength=NP)[:NP] for k in ("first", "renewal", "refund") for mm in (True, False)}
    STORES = (("Google Play", "google_play", False), ("App Store", "app_store", True))
    excess, cand = {}, {}
    for name, code, is_ios in STORES:
        rows = made[made.store == code]
        d = pacific_day(rows.ts) if is_ios else rows.d.to_numpy()
        p = period(d)
        cnt = lambda sel: np.bincount(p[sel.to_numpy()], minlength=NP)[:NP].astype(float)
        fm_, rn_, an_ = (rows.monthly & (rows.event_type == "first_charge"), rows.monthly & (rows.event_type == "renewal"),
                         ~rows.monthly & (rows.event_type == "first_charge"))
        excess[name] = dict(first=rep[name][("first", True)] - cnt(fm_), renewal=rep[name][("renewal", True)] - cnt(rn_),
                            annual=rep[name][("first", False)] - cnt(an_))
        st = fig["stores"][name]
        stood = ~rows.event_id.isin(refunded)
        ok("%s: %d renewals reported against %d in the records, %d never taken in; %d first monthly and %d annual first charges" % (
            name, rep[name][("renewal", True)].sum(), rn_.sum(), excess[name]["renewal"].sum(), excess[name]["first"].sum(),
            excess[name]["annual"].sum()),
           (int(rep[name][("renewal", True)].sum()), int(rn_.sum()), int(excess[name]["renewal"].sum()),
            int(excess[name]["first"].sum()), int(excess[name]["annual"].sum())) ==
           (st["store_renewals"], st["recorded_renewals"], st["renewal_excess"], st["first_excess"], st["annual_excess"])
           and int((fm_ & stood).sum()) == st["recorded_first"] and int((an_ & stood).sum()) == st["recorded_annual"])
        ok("%s: the store reports no fewer charges than the records hold in any period" % name,
           all((excess[name][k] >= 0).all() for k in excess[name]))

    # the subscriptions the app last saw still set to renew
    def candidates(rnd):
        nxt = first_day + rnd(PERIOD * n_m)
        ren = ~on_web & (sub_plan == "monthly") & (n_m >= 1) & auto & (last_open < nxt) & (nxt <= END_DAY)
        tri = ~on_web & (state == "trial") & auto & (n_m == 0) & ~has_a
        return ren, tri
    ren, tri = candidates(up)
    ren_even, _ = candidates(lambda x: np.round(x).astype(np.int64))
    ok("candidates: the same subscriptions whether a half day is rounded up or to even (%d and %d)" % (ren.sum(), ren_even.sum()),
       bool((ren == ren_even).all()))
    ok("candidates: every trial last seen unconverted is seven days old by the pull, on a store, with a plan chosen",
       bool((day[tri] + 7 <= END_DAY).all()) and set(sub_plan[tri]) == {"monthly", "annual"}
       and bool((np.where(ios, "app_store", "google_play")[ren | tri] == sub_store[ren | tri]).all()))
    lvl = np.minimum((cv & 7) // 2, 3)                                # the sessions bucket in four pairs
    trial_bit = ((cv >> 3) & 1) == 1
    bought = (n_m >= 1) | has_a
    fits = {}
    for name, code, is_ios in STORES:
        mine = (ios == is_ios)
        r_i = np.where(ren & mine)[0]
        tm_i = np.where(tri & mine & (sub_plan == "monthly"))[0]
        ta_i = np.where(tri & mine & (sub_plan == "annual"))[0]
        share_m = excess[name]["first"].sum() / len(tm_i)
        share_a = excess[name]["annual"].sum() / len(ta_i)
        # how the trial starters whose outcome the records hold went on to buy, by sessions level
        starters = mine & ~on_web & trial_bit
        known = starters & (bought | (last_open >= day + 7) | ~auto)
        rate = np.array([bought[known & (lvl == k)].mean() for k in range(4)]) / bought[known].mean()
        rel_m = rate[lvl[tm_i]] / rate[lvl[tm_i]].mean()
        rel_a = rate[lvl[ta_i]] / rate[lvl[ta_i]].mean()

        def on_store_day(d, idx, sec):
            return pacific_day(DAY0 + pd.to_timedelta(d * 86400 + sec[idx], unit="s")) if is_ios else d
        Mr, Mf, Mf_own = np.zeros((25, NP)), np.zeros((25, NP)), np.zeros((25, NP))
        for j in range(1, 26):
            d = last_m[r_i] + up(PERIOD * j)
            keep = d <= END_DAY
            Mr[j - 1] = np.bincount(period(on_store_day(d[keep], r_i[keep], first_tod)), minlength=NP)[:NP]
            d = day[tm_i] + 7 + up(PERIOD * j)
            keep = d <= END_DAY
            pp = period(on_store_day(d[keep], tm_i[keep], tod))
            Mf[j - 1] = np.bincount(pp, minlength=NP)[:NP]
            Mf_own[j - 1] = np.bincount(pp, weights=rel_m[keep], minlength=NP)[:NP]
        R = excess[name]["renewal"]

        def miss(q, own=False):
            w = q ** np.arange(1, 26)
            return float((((w @ Mr + share_m * (w @ (Mf_own if own else Mf))) - R)[:NP - 1] ** 2).sum())
        q = minimize_scalar(miss, bounds=(0.60, 0.995), method="bounded", options={"xatol": 1e-7}).x
        q_own = minimize_scalar(lambda x: miss(x, True), bounds=(0.60, 0.995), method="bounded", options={"xatol": 1e-7}).x
        st = fig["stores"][name]
        ok("%s: %d renewal candidates, %d monthly and %d annual trial candidates" % (name, len(r_i), len(tm_i), len(ta_i)),
           (len(r_i), len(tm_i), len(ta_i)) == (st["renewal_candidates"], st["trial_candidates_monthly"],
                                                st["trial_candidates_annual"]))
        ok("%s: the share of trial candidates charged is %.3f monthly and %.3f annual" % (name, share_m, share_a),
           (round(share_m, 3), round(share_a, 3)) == (st["trial_end_share_monthly"], st["trial_end_share_annual"]))
        ok("%s: the continuation fitted on the real line is %.4f against the stated %.3f; with each trial at its own share "
           "in the fit %.4f" % (name, q, st["continuation"], q_own),
           abs(q - st["continuation"]) <= 0.0006 and abs(q_own - q) <= 0.001)
        w = q ** np.arange(1, 26)
        took = float(((w @ Mr + share_m * (w @ Mf))[:NP - 1]).sum())
        ok("%s: the fit takes in %d of the %d renewals beyond the records over the fitted periods" % (
            name, round(took), R[:NP - 1].sum()),
           abs(took / R[:NP - 1].sum() - 1) < 0.01 and int(R[:NP - 1].sum()) == st["renewal_excess_fitted_periods"]
           and abs(round(took) - st["rivals"]["fitted"]["takes_in"]) <= 0.001 * st["rivals"]["fitted"]["takes_in"])
        fits[name] = dict(q=q, share_m=share_m, share_a=share_a, r_i=r_i, tm_i=tm_i, ta_i=ta_i, rel_m=rel_m, rel_a=rel_a)

    # each account's 12-month net revenue with the charges the records never took in
    v = rec12.copy()
    end365 = day + 365
    for name, f in fits.items():
        q, r_i, tm_i, ta_i = f["q"], f["r_i"], f["tm_i"], f["ta_i"]
        for j in range(1, 26):
            d = last_m[r_i] + up(PERIOD * j)
            v[r_i] += q ** j * net_m[r_i] * ((d < end365[r_i]) & (d <= END_DAY))
            d = day[tm_i] + 7 + up(PERIOD * j)
            v[tm_i] += f["share_m"] * f["rel_m"] * q ** j * net_m[tm_i] * ((d < end365[tm_i]) & (d <= END_DAY))
        v[tm_i] += f["share_m"] * f["rel_m"] * net_m[tm_i]
        v[ta_i] += f["share_a"] * f["rel_a"] * net_a[ta_i]

    # ------------------------------------------------------------------------------------------------------------
    # the channels: the export's names, the postbacks, the accounts with no channel
    # ------------------------------------------------------------------------------------------------------------
    att = read("attribution_installs_*.csv")
    att = att[att.is_reinstall == "false"].drop_duplicates("install_id")
    att = att[att.account_id.isin(ix)]
    ok("attribution: one first install for every consumer account", att.account_id.is_unique and len(att) == n)
    name_of = pd.Series([MEDIA.get((a, b), "") for a, b in zip(att.media_source, att.platform)], index=att.account_id.to_numpy())
    ok("attribution: a row with no media source is an iOS account's", bool((att.platform[att.media_source == ""] == "ios").all()))
    label = name_of.reindex(ix).to_numpy()
    unnamed = label == ""
    sp = read("ad_spend_daily_*.csv")
    sp["channel"] = [MEDIA[(a, b)] for a, b in zip(sp.network, sp.os)]
    sp["w"] = ((pd.to_datetime(sp.date) - pd.Timestamp("2024-11-04")) // pd.Timedelta(days=7)).to_numpy()
    sp["cents"] = np.rint(sp.spend_eur.astype(float) * 100).astype(np.int64)
    spend = {c: np.bincount(sp.w[sp.channel == c], weights=sp.cents[sp.channel == c], minlength=WEEKS) / 100.0 for c in CHANNELS}
    camp_market = sp.drop_duplicates("campaign_id").set_index("campaign_id").country.map(MKT)
    ok("spend: every channel spends in every one of the 104 weeks, a campaign runs in one market",
       all((spend[c] > 0).all() for c in CHANNELS) and sp.groupby("campaign_id").country.nunique().max() == 1)
    pb = read("skan_postbacks_*.csv")
    n_pb = len(pb)
    pb = pb[pb.redownload == "false"].drop_duplicates("postback_id")
    ok("postbacks: %d rows, %d installs once redownloads and twice-delivered postbacks are out" % (n_pb, len(pb)),
       n_pb == fig["steps"]["postbacks"] and len(pb) == fig["steps"]["postbacks_used"])
    pb_ch = pb.ad_network.map(POSTBACK).to_numpy()
    pb_day = day_of(stamp(pb.received_at))
    pb_cv = pb.conversion_value.astype(int).to_numpy()
    pb_mkt = pb.campaign_id.map(camp_market).to_numpy()
    assert not pd.isna(pb_mkt).any()
    pb_mkt = pb_mkt.astype(int)
    # a postback's install week: three days back for half of it, four for the other half
    posted = {c: np.zeros((WEEKS, 3, 32)) for c in NETWORKS}
    for c in NETWORKS:
        sel = pb_ch == c
        for back in (3, 4):
            np.add.at(posted[c], (np.clip((pb_day[sel] - back) // 7, 0, WEEKS - 1), pb_mkt[sel], pb_cv[sel]), 0.5)
    installs = {c: (posted[c].sum((1, 2)) if c in NETWORKS else np.bincount(week[label == c], minlength=WEEKS).astype(float))
                for c in CHANNELS}

    # each source's named installs by first-48-hour value, and what they went on to pay
    SOURCES = NETWORKS + ["organic iOS"]
    refset = full & ios & allowed & np.isin(label, SOURCES)
    ref_n = np.bincount(cv[refset], minlength=32)
    ref_v = np.where(ref_n >= 20, np.bincount(cv[refset], weights=v[refset], minlength=32) / np.maximum(ref_n, 1), v[refset].mean())
    named_n, named_v = {}, {}
    for s in SOURCES:
        lab = full & ios & allowed & (label == s)
        cnt = np.bincount(cv[lab], minlength=32).astype(float)
        tot = np.bincount(cv[lab], weights=v[lab], minlength=32)
        level = tot.sum() / (cnt * ref_v).sum()
        named_n[s], named_v[s] = cnt, np.where(cnt >= 20, tot / np.maximum(cnt, 1), ref_v * level)
    pool = full & ios & unnamed
    shape = (3, FULL, 32)
    pool_n, pool_v = np.zeros(shape), np.zeros(shape)
    np.add.at(pool_n, (market[pool], week[pool], cv[pool]), 1)
    np.add.at(pool_v, (market[pool], week[pool], cv[pool]), v[pool])
    hidden, rest = {}, pool_n.copy()
    for c in NETWORKS:
        x = posted[c][:FULL].transpose(1, 0, 2).copy()                 # market, week, first-48-hour value
        lab = full & (label == c)
        np.subtract.at(x, (market[lab], week[lab], cv[lab]), 1)
        hidden[c] = x
        rest -= x
    hidden["organic iOS"] = rest
    y = pool_v.sum(2).reshape(-1)
    npool = pool_n.sum(2).reshape(-1)
    X = np.stack([(hidden[s] * named_v[s][None, None, :]).sum(2).reshape(-1) for s in SOURCES], axis=1)
    ok("unnamed installs: %d accounts with no channel over the 52 weeks paid EUR %d; %d the five networks', %d organic; %d "
       "market-weeks" % (pool.sum(), round(pool_v.sum()), round(sum(hidden[c].sum() for c in NETWORKS)), round(rest.sum()),
                         (npool > 0).sum()),
       (int(pool.sum()), int(round(sum(hidden[c].sum() for c in NETWORKS))), int(round(rest.sum())), int((npool > 0).sum())) ==
       (fig["ratios"]["pool"]["accounts"], fig["ratios"]["pool"]["network_installs"], fig["ratios"]["pool"]["organic_installs"],
        fig["ratios"]["pool"]["market_weeks"]) and abs(pool_v.sum() / fig["ratios"]["pool"]["paid"] - 1) < 0.002)
    ratio = dict(zip(SOURCES, wls(X, y, 1.0 / np.maximum(npool, 1.0))))
    ok("unnamed installs: the fitted ratios are " + ", ".join("%s %.3f" % (s.split()[0], ratio[s]) for s in SOURCES),
       all(abs(ratio[s] - fig["ratios"]["sources"][s]["ratio"]) <= 0.003 for s in SOURCES))
    paid = {}
    for c in CHANNELS:
        if c in NETWORKS:
            extra = np.maximum(hidden[c].sum((0, 1)), 0)
            tot = named_n[c] + extra
            price = np.where(tot > 0, (named_n[c] * named_v[c] + extra * named_v[c] * ratio[c]) / np.maximum(tot, 1e-9), named_v[c])
            paid[c] = dict(v=float((tot * price).sum() / tot.sum()), price=price)
        else:
            lab = full & (label == c)
            cnt = np.bincount(cv[lab], minlength=32)
            price = np.where(cnt >= 20, np.bincount(cv[lab], weights=v[lab], minlength=32) / np.maximum(cnt, 1), v[lab].mean())
            paid[c] = dict(v=float(v[lab].mean()), price=price)
    named_share = [100 * named_n[c].sum() / installs[c][:FULL].sum() for c in NETWORKS]
    ok("unnamed installs: the export names %.1f to %.1f per cent of an iOS network's installs" % (min(named_share), max(named_share)),
       round(min(named_share), 1) == min(fig["channels"][c]["named_pct"] for c in NETWORKS)
       and round(max(named_share), 1) == max(fig["channels"][c]["named_pct"] for c in NETWORKS))

    # ------------------------------------------------------------------------------------------------------------
    # the response to the budget, with the share of it the platform spent
    # ------------------------------------------------------------------------------------------------------------
    monday = pd.Timestamp("2024-11-04") + pd.to_timedelta(7 * np.arange(WEEKS), unit="D")
    wmonth = month_of(monday + pd.Timedelta(days=3))                   # a week takes the month of its Thursday
    pmonth = month_of(plan_monday + pd.Timedelta(days=3))
    value_w = {}
    for c in CHANNELS:
        if c in NETWORKS:
            A = posted[c].sum(1)                                       # week by first-48-hour value
            value_w[c] = (A @ paid[c]["price"]) / np.maximum(A.sum(1), 1)
        else:
            lab = label == c
            value_w[c] = (np.bincount(week[lab], weights=paid[c]["price"][cv[lab]], minlength=WEEKS)
                          / np.maximum(np.bincount(week[lab], minlength=WEEKS), 1))
    frames = []
    for c in CHANNELS:
        lb, ls = np.log(budget[c]), np.log(spend[c])
        frames.append(pd.DataFrame(dict(channel=c, w=np.arange(WEEKS), lb=lb - lb.mean(), ld=(ls - lb) - (ls - lb).mean(),
                                        ls=ls - ls.mean(), month=wmonth, installs=installs[c], value=value_w[c])))
    D = pd.concat(frames, ignore_index=True)

    def fit(col, on="budget"):
        d = D[D[col] > 0]
        cols = [(d.channel == c).astype(float).rename("a " + c) for c in CHANNELS]
        if on == "budget":
            cols += [((d.channel == c) * d.lb).rename("b " + c) for c in CHANNELS]
            cols += [((d.channel == c) * d.ld).rename("d " + c) for c in CHANNELS]
        else:
            cols += [((d.channel == c) * d.ls).rename("b " + c) for c in CHANNELS]
        cols += [(d.month == k).astype(float).rename("m %d" % k) for k in range(2, 13)]
        Xd = pd.concat(cols, axis=1)
        beta = pd.Series(np.linalg.solve(Xd.T.to_numpy() @ Xd.to_numpy(), Xd.T.to_numpy() @ np.log(d[col].to_numpy())), index=Xd.columns)
        mon = np.concatenate([[0.0], beta[["m %d" % k for k in range(2, 13)]].to_numpy()])
        return {c: dict(a=beta["a " + c], s=beta["b " + c], mon=mon) for c in CHANNELS}
    fi, fv = fit("installs"), fit("value")
    fi_s = fit("installs", on="spend")
    ga = fig["channels"]["Google Android"]
    ok("response: Google Android's installs rise %.3f per cent for one per cent of budget, %.3f when fitted on spend" % (
        fi["Google Android"]["s"], fi_s["Google Android"]["s"]),
       round(fi["Google Android"]["s"], 3) == ga["budget_elasticity"] and round(fi_s["Google Android"]["s"], 3) == ga["spend_elasticity"])

    out = {}
    for c in MEMBERS:
        share = spend[c].sum() / budget[c].sum()                       # the share of the budget the platform spent
        lbm = np.log(budget[c]).mean()
        xh = np.log(budget[c]) - lbm
        si, sv, mi, mv = fi[c]["s"], fv[c]["s"], fi[c]["mon"], fv[c]["mon"]
        scale_i = installs[c].sum() / np.exp(fi[c]["a"] + si * xh + mi[wmonth - 1]).sum()
        shape_v = np.exp(sv * xh[:FULL] + mv[wmonth[:FULL] - 1])
        scale_v = paid[c]["v"] / ((shape_v * installs[c][:FULL]).sum() / installs[c][:FULL].sum())
        r = {}
        for tag, weekly in (("plan", plan[c]), ("stretch", stretch[c])):
            xp = np.log(weekly / share) - lbm
            n_t = scale_i * np.exp(fi[c]["a"] + si * xp + mi[pmonth - 1])
            v_t = scale_v * np.exp(sv * xp + mv[pmonth - 1])
            r[tag] = dict(ret=(n_t * v_t).sum() / weekly.sum(), installs=n_t.mean(), value=(n_t * v_t).sum() / n_t.sum())
        out[c] = {"return ": r["plan"]["ret"], "stretch return ": r["stretch"]["ret"], "installs a week ": r["plan"]["installs"],
                  "value at plan ": r["plan"]["value"], "next euro ": r["plan"]["ret"] * (si + sv),
                  "stretch next euro ": r["stretch"]["ret"] * (si + sv), "paid per install ": paid[c]["v"]}

    # ------------------------------------------------------------------------------------------------------------
    # every graded figure against the blocks' figure and range
    # ------------------------------------------------------------------------------------------------------------
    worst = (0.0, "")
    for c in MEMBERS:
        misses = []
        for fam, x in out[c].items():
            fid = fam + c
            lo, hi = fig["figure_band"][fid]
            nd = 0 if fam == "installs a week " else (2 if fam in ("value at plan ", "paid per install ") else 3)
            mine_ = int(round(x)) if nd == 0 else round(x, nd)
            rel = abs(x / fig["figure"][fid] - 1)
            worst = max(worst, (rel, fid))
            if not (lo <= mine_ <= hi) or rel > 0.003:
                misses.append((fid, mine_, fig["figure"][fid], [lo, hi]))
        ok("%s: the seven figures recomputed here sit in their ranges and within 0.3 per cent of the stated ones (return %.3f, "
           "%s)" % (c, out[c]["return "], band_name(out[c]["return "], HOLD, SCALE)),
           not misses and band_name(out[c]["return "], HOLD, SCALE) == fig["bands"][c], misses)
    ok("the largest distance between a figure recomputed here and the stated one is %.2f per cent (%s)" % (100 * worst[0], worst[1]),
       worst[0] < 0.003)
    call = {b: [c for c in MEMBERS if band_name(out[c]["return "], HOLD, SCALE) == b] for b in ("scale", "hold", "cut")}
    ok("the call: scale %s; hold %s; cut %s" % tuple(", ".join(call[b]) for b in ("scale", "hold", "cut")),
       all(sorted(call[b]) == sorted(fig["by_band"][b]) for b in call))
    comp = fig["components"]
    ok("the three steps' own figures: EUR %.2f, EUR %.2f and %d installs a week" % (
        out["AppLovin Android"]["paid per install "], out["Meta iOS"]["paid per install "], round(out["Google Android"]["installs a week "])),
       abs(out["AppLovin Android"]["paid per install "] - comp["S1"]["value"]) <= 0.02
       and abs(out["Meta iOS"]["paid per install "] - comp["S2"]["value"]) <= 0.03
       and abs(out["Google Android"]["installs a week "] - comp["S3"]["value"]) <= 2)
    rec_al = rec12[full & (label == "AppLovin Android")].mean()
    ok("AppLovin Android's installs of the year paid EUR %.2f each in the records as they stand" % rec_al,
       round(rec_al, 2) == fig["channels"]["AppLovin Android"]["recorded_per_install"])

    # ------------------------------------------------------------------------------------------------------------
    # the golden files
    # ------------------------------------------------------------------------------------------------------------
    gcsv = pd.read_csv(os.path.join(G, "paid_channels_2027.csv"))
    ok("golden CSV: seven channels, a band and seven figures each, the three steps' figures among them",
       list(gcsv.columns[:2]) == ["channel", "band"] and gcsv.shape == (7, 9) and set(gcsv.channel) == set(MEMBERS))
    cols = dict(zip(["return ", "stretch return ", "installs a week ", "value at plan ", "next euro ", "stretch next euro ",
                     "paid per install "], gcsv.columns[2:]))
    off = [(c, fam) for c in MEMBERS for fam, col in cols.items()
           if float(gcsv.set_index("channel").loc[c, col]) != fig["figure"][fam + c]]
    ok("golden CSV: every figure is the blocks' figure, every band the call's",
       not off and all(gcsv.set_index("channel").band[c] == fig["bands"][c] for c in MEMBERS), off)
    near = max(abs(float(gcsv.set_index("channel").loc[c, col]) / out[c][fam] - 1) for c in MEMBERS for fam, col in cols.items())
    ok("golden CSV: every figure within 0.3 per cent of the one recomputed here (largest %.2f)" % (100 * near), near < 0.003)
    gwb = load_workbook(os.path.join(G, "paid_channels_2027.xlsx"), data_only=True)
    first = gwb.worksheets[0]
    head = str(first["A1"].value)
    ok("golden workbook: the first sheet opens on the call", all(c in head for c in call["scale"] + call["hold"] + call["cut"])
       and head.index("scale") < head.index("hold") < head.index("cut"))
    rows = {first.cell(row=r, column=1).value: [first.cell(row=r, column=k).value for k in range(2, 10)]
            for r in range(1, first.max_row + 1) if first.cell(row=r, column=1).value in MEMBERS}
    ok("golden workbook: the first sheet's rows are the CSV's rows",
       len(rows) == 7 and all(rows[c][0].lower() == fig["bands"][c]
                              and [float(x) for x in rows[c][1:]] == [float(gcsv.set_index("channel").loc[c, col]) for col in cols.values()]
                              for c in MEMBERS))
    print("\n%d passed, %d failed" % (N["pass"], N["fail"]))
    return 1 if N["fail"] else 0


if __name__ == "__main__":
    sys.exit(main())
