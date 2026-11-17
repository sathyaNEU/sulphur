"""task1 architecture 6, the independent verifier: every graded figure recomputed from target/ by code that shares
nothing with core.py or analysis.py (pandas frames keyed by account, its own Pacific-day conversion, its own
period builder, a continuous fit of the continuation where the build searches a grid, its own design matrices),
each checked against figures.json inside its stated band, with the two golden files read back against both. It
finds the files by what they are, reads every format the pack ships, and takes nothing from the generator's state.

    python3 task1/generator/verify.py
"""
import datetime as dt
import glob
import json
import os
import subprocess
import sys

import numpy as np
import pandas as pd
from scipy.optimize import minimize_scalar

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
G = os.path.join(TASK, "golden")
FIG = json.load(open(os.path.join(HERE, "figures.json")))
N = {"pass": 0, "fail": 0}

D0 = pd.Timestamp("2024-11-04", tz="UTC")
END = (pd.Timestamp("2026-11-08", tz="UTC") - D0).days           # the last day on record
MD = 365.25 / 12                                                  # the billing cadence, checked on the events below
WEEKS, MATURE, HORIZON = 104, 52, 365
NP = int(END // MD) + 1
NAMES = {("Meta Ads", "ios"): "Meta iOS", ("TikTok For Business", "ios"): "TikTok iOS", ("Snapchat Ads", "ios"): "Snapchat iOS",
         ("Google Ads", "ios"): "Google iOS", ("Pinterest Ads", "ios"): "Pinterest iOS",
         ("Apple Search Ads", "ios"): "Apple Search Ads", ("Google Ads", "android"): "Google Android",
         ("AppLovin", "android"): "AppLovin Android", ("organic", "ios"): "organic iOS", ("organic", "android"): "organic Android"}
POSTBACK = {"meta": "Meta iOS", "tiktok": "TikTok iOS", "snapchat": "Snapchat iOS", "google": "Google iOS",
            "pinterest": "Pinterest iOS"}
NETWORKS = list(POSTBACK.values())
ASA = "Apple Search Ads"


def ok(label, cond, detail=""):
    N["pass" if cond else "fail"] += 1
    print(("PASS  " if cond else "FAIL  ") + label + ("" if cond else "  %s" % (detail,)))


def one(pattern):
    hit = sorted(glob.glob(os.path.join(T, pattern)))
    assert len(hit) == 1, (pattern, hit)
    return hit[0]


def day_of(s):
    return (pd.to_datetime(s, utc=True) - D0).dt.days.astype("int64")


def tod_of(s):
    t = pd.to_datetime(s, utc=True)
    return (t.dt.hour * 3600 + t.dt.minute * 60 + t.dt.second).astype("int64")


def pacific(day, tod):
    """the Pacific calendar day (counted from 4 November 2024) of a UTC day and time of day"""
    ns = D0.value + (np.asarray(day, np.int64) * 86400 + np.asarray(tod, np.int64)) * 10 ** 9
    loc = pd.to_datetime(ns, utc=True).tz_convert("America/Los_Angeles").tz_localize(None).normalize()
    return np.asarray((loc - pd.Timestamp("2024-11-04")).days, dtype=np.int64)


def period(day):
    return np.maximum(np.floor(np.asarray(day) / MD), 0).astype(int)


def by_period(p, w=None):
    return np.bincount(np.asarray(p, int), weights=w, minlength=NP)[:NP].astype(float)


def pdf_text(path):
    try:
        return subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True, check=True).stdout
    except Exception:
        from pypdf import PdfReader
        return "\n".join(p.extract_text() for p in PdfReader(path).pages)


def main():
    # ------------------------------------------------------------------ the documents, each read back
    pol = " ".join(pdf_text(one("growth_policy*.pdf")).split())
    for phrase in ("1.20 or more", "0.90 or more and under 1.20", "under 0.90", "in the 365 days from the install",
                   "Spain 21 per cent, Italy 22 per cent, Portugal 23 per cent", "commission of 15 per cent",
                   "fee of 3 per cent", "EUR 9.99 a month and EUR 59.99 a year", "seven-day free trial",
                   "first install of a new consumer account", "every week of the period raised in the same proportion",
                   "at the time of the transaction", "channels of the media plan's growth sheet"):
        ok("policy PDF carries: " + phrase, phrase in pol)
    schema = json.load(open(one("skadnetwork_*.json")))
    ok("conversion-value JSON: a 48-hour window, the postback 24 to 48 hours after it",
       schema["postback"]["measurement_window_hours"] == 48 and schema["postback"]["sent_after_window_closes_hours"] == [24, 48])
    plan = pd.read_excel(one("media_plan*.xlsx"), sheet_name="Growth channels", header=3).iloc[:52]
    stretch = pd.read_excel(one("media_plan*.xlsx"), sheet_name="Stretch case", header=3).iloc[:52]
    members = [c for c in plan.columns if c in NAMES.values()]
    ok("plan workbook: 52 weeks from 4 January 2027 for seven growth channels",
       len(plan) == 52 and len(members) == 7 and pd.Timestamp(plan.iloc[0, 0]).date() == dt.date(2027, 1, 4), members)
    brand = pd.read_excel(one("media_plan*.xlsx"), sheet_name="Brand", header=3).iloc[:52]
    ok("plan workbook: Apple Search Ads on the brand sheet only", ASA in brand.columns and ASA not in members)
    bud = pd.read_excel(one("paid_budgets*.xlsx"), sheet_name="Weekly budgets", header=2).iloc[:WEEKS]
    chg = pd.read_excel(one("paid_budgets*.xlsx"), sheet_name="Changes")
    channels = [c for c in bud.columns if c in NAMES.values()]
    ok("budget workbook: 104 weeks from 4 November 2024 for eight channels",
       len(bud) == WEEKS and len(channels) == 8 and pd.Timestamp(bud.iloc[0, 0]).date() == dt.date(2024, 11, 4))

    # ------------------------------------------------------------------ accounts and their charges
    a = pd.read_csv(one("accounts_*.csv"), dtype=str, keep_default_na=False)
    a = a[a.account_type == "consumer"].set_index("account_id")
    a["day"], a["tod"] = day_of(a.created_at), tod_of(a.created_at)
    a["week"] = a.day // 7
    a["lo"] = day_of(a.last_open_at)
    a["ios"] = a.platform == "ios"
    a["cv"] = a.conversion_value_48h.astype(int)
    a["consent"] = a.tracking_status == "authorized"
    a["mature"] = a.week < MATURE
    vat = a.storefront.map({"ES": 0.21, "IT": 0.22, "PT": 0.23})

    b = pd.read_csv(one("billing_events_*.csv"), dtype=str, keep_default_na=False)
    b = b[(b.environment == "production") & b.account_id.isin(a.index)]
    b = b.drop_duplicates(["account_id", "product_id", "event_type", "transaction_at"])
    back = set(b.refund_of_event_id[b.event_type == "refund"])
    undone = b[b.event_id.isin(back)].copy()
    b = b[(b.event_type != "refund") & ~b.event_id.isin(back)].copy()
    for f in (b, undone):
        f["d"], f["tod"] = day_of(f.transaction_at), tod_of(f.transaction_at)
        f["monthly"] = f.product_id.str.endswith("monthly")
    ok("billing events: prices are 9.99 monthly and 59.99 annual",
       set(b.amount_eur[b.monthly]) == {"9.99"} and set(b.amount_eur[~b.monthly]) == {"59.99"})
    a["web"] = a.index.isin(set(b.account_id[b.store == "web"]))
    fee = np.where(a.web, 0.97, 0.85)
    a["netm"], a["neta"] = 9.99 / (1 + vat) * fee, 59.99 / (1 + vat) * fee
    bm = b[b.monthly].sort_values(["account_id", "d"])
    gaps = bm.groupby("account_id").d.diff().dropna()
    ok("billing events: monthly charges a twelfth of a year apart (30 or 31 days, mean %.3f)" % gaps.mean(),
       set(gaps.unique()) <= {30, 31} and abs(gaps.mean() - MD) < 0.02)
    g = bm.groupby("account_id").d.agg(["min", "max", "count"])
    a["conv"] = g["min"].reindex(a.index)
    a["last"] = g["max"].reindex(a.index)
    a["n_rec"] = g["count"].reindex(a.index).fillna(0).astype(int)
    first = b[b.event_type == "first_charge"].drop_duplicates("account_id").set_index("account_id")
    a["ctod"] = first.tod.reindex(a.index).fillna(a.tod).astype("int64")
    a["annual"] = a.index.isin(set(b.account_id[~b.monthly & (b.event_type == "first_charge")]))
    b = b.join(a[["day", "netm", "neta", "ios", "web"]], on="account_id")
    b["net"] = np.where(b.monthly, b.netm, b.neta)
    a["rec12"] = b[b.d < b.day + HORIZON].groupby("account_id").net.sum().reindex(a.index).fillna(0.0)

    # ------------------------------------------------------------------ the stores against the records, by period
    ap = pd.read_csv(one("appstore_*.csv"), dtype=str, keep_default_na=False)
    gp = pd.read_csv(one("googleplay_*.csv"), dtype=str, keep_default_na=False)
    kind_a = {"Paid Subscription from Free Trial": "first", "Subscribe": "first", "Renew": "renew", "Refund": "refund"}
    kind_g = {"charge_new": "first", "charge_renewal": "renew", "refund": "refund"}
    S = {}
    for store, df, dcol, kcol, ucol, kinds in (("app_store", ap, "date_pt", "event", "units", kind_a),
                                              ("google_play", gp, "date_utc", "transaction_type", "transactions", kind_g)):
        p = period((pd.to_datetime(df[dcol]) - pd.Timestamp("2024-11-04")).dt.days)
        k = df[kcol].map(kinds)
        mo = df.product_id.str.endswith("monthly")
        u = df[ucol].astype(float)
        S[store] = {"first": by_period(p[(k == "first") & mo], u[(k == "first") & mo]),
                    "renew": by_period(p[(k == "renew") & mo], u[(k == "renew") & mo]),
                    "annual": by_period(p[(k == "first") & ~mo], u[(k == "first") & ~mo])}
        net = df[[c for c in df.columns if c.startswith(("developer_proceeds", "net_amount"))][0]].astype(float)
        gross = df[[c for c in df.columns if c.startswith(("customer_price", "amount_charged"))][0]].astype(float)
        rate = {"ES": 0.21, "IT": 0.22, "PT": 0.23}
        v = df[[c for c in df.columns if c in ("storefront", "country")][0]].map(rate)
        ok("%s report: proceeds are the price less VAT less 15 per cent" % store,
           bool((abs(net - gross / (1 + v) * 0.85) < 0.006).all()))

    def rec_period(f):
        """a charge's period on its store's own day"""
        d = f.d.to_numpy()
        ios = (f.store == "app_store").to_numpy()
        out = d.copy()
        out[ios] = pacific(d[ios], f.tod.to_numpy()[ios])
        return period(out)
    fits, cand = {}, {}
    auto = a.auto_renew_at_last_open == "yes"
    nxt = a.conv + np.round(MD * a.n_rec)
    ren = ~a.web & (a.sub_plan_at_last_open == "monthly") & (a.n_rec >= 1) & auto & (a.lo < nxt) & (nxt <= END) & (a.n_rec < 26)
    fst = (~a.web & (a.sub_state_at_last_open == "trial") & auto & (a.n_rec == 0) & ~a.annual
           & (a.sub_plan_at_last_open != "") & (a.day + 7 <= END))
    J = np.arange(1, 26)
    step = np.round(MD * J).astype(int)
    for store, is_ios in (("google_play", False), ("app_store", True)):
        mine = b[b.store == store]
        gone = undone[undone.store == store]
        pr, pg = rec_period(mine), rec_period(gone)
        fc, mo = (mine.event_type == "first_charge").to_numpy(), mine.monthly.to_numpy()
        F = S[store]["first"] - by_period(pr[fc & mo]) - by_period(pg[gone.monthly.to_numpy()])
        R = S[store]["renew"] - by_period(pr[~fc & mo])
        A = S[store]["annual"] - by_period(pr[fc & ~mo]) - by_period(pg[~gone.monthly.to_numpy()])
        side = a.ios == is_ios
        fm, fa, rn = a[fst & side & (a.sub_plan_at_last_open == "monthly")], a[fst & side & (a.sub_plan_at_last_open == "annual")], a[ren & side]
        c_m, c_a = F.sum() / len(fm), A.sum() / len(fa)

        def projected(base, tod):
            M = np.zeros((25, NP))
            for j, s in enumerate(step):
                d = base + s
                keep = d <= END
                dd = pacific(d[keep], tod[keep]) if is_ios else d[keep]
                M[j] = by_period(period(dd))
            return M
        Mr = projected(rn["last"].to_numpy().astype(int), rn.ctod.to_numpy())
        Mf = projected(fm.day.to_numpy() + 7, fm.ctod.to_numpy())
        use = np.arange(NP) < NP - 1

        def miss(q):
            w = q ** J
            return (((w @ Mr + c_m * (w @ Mf)) - R)[use] ** 2).sum()
        q = minimize_scalar(miss, bounds=(0.6, 0.99), method="bounded", options={"xatol": 1e-6}).x
        fits[store] = dict(c_m=c_m, c_a=c_a, q=q)
        cand[store] = dict(monthly=len(fm), annual=len(fa), renew=len(rn))
    for store, name in (("google_play", "Google Play"), ("app_store", "App Store")):
        x = FIG["stores"][name]
        ok("%s: %d and %d candidates, trial-end share %.3f, continuation %.3f" % (
            name, cand[store]["monthly"], cand[store]["renew"], fits[store]["c_m"], fits[store]["q"]),
           cand[store]["monthly"] == x["trial_candidates_monthly"] and cand[store]["renew"] == x["renewal_candidates"]
           and abs(fits[store]["c_m"] - x["trial_end_share_monthly"]) < 0.0006 and abs(fits[store]["q"] - x["continuation"]) < 0.0025,
           (cand[store], fits[store], x["trial_end_share_monthly"], x["continuation"]))

    # each account's twelve-month net revenue with the charges its record never took in
    add = pd.Series(0.0, index=a.index)
    for store, is_ios in (("google_play", False), ("app_store", True)):
        f = fits[store]
        side = a.ios == is_ios
        rn = a[ren & side]
        d = rn["last"].to_numpy()[:, None] + step[None, :]
        inside = (d < (rn.day.to_numpy() + HORIZON)[:, None]) & (d <= END)
        add[rn.index] += (inside * f["q"] ** J).sum(1) * rn.netm.to_numpy()
        fr = a[fst & side]
        mon = (fr.sub_plan_at_last_open == "monthly").to_numpy()
        d = (fr.day.to_numpy() + 7)[:, None] + step[None, :]
        inside = (d < (fr.day.to_numpy() + HORIZON)[:, None]) & (d <= END)
        add[fr.index] += np.where(mon, f["c_m"] * fr.netm.to_numpy() * (1 + (inside * f["q"] ** J).sum(1)),
                                  f["c_a"] * fr.neta.to_numpy())
    a["v"] = a.rec12 + add

    # ------------------------------------------------------------------ channels: the export and the postbacks
    t = pd.read_csv(one("attribution_*.csv"), dtype=str, keep_default_na=False)
    t = t[(t.is_reinstall == "false") & t.account_id.isin(a.index)].drop_duplicates("install_id")
    ok("attribution export: one install row for every consumer account", t.account_id.is_unique and len(t) == len(a))
    lab = pd.Series([NAMES.get(k, "") for k in zip(t.media_source, t.platform)], index=t.account_id)
    a["label"] = lab.reindex(a.index)
    ok("attribution export: the organic label only on iOS accounts that allowed tracking; no Android row unnamed",
       bool(a.consent[a.label == "organic iOS"].all()) and bool(a.ios[a.label == ""].all()))
    s = pd.read_csv(one("skan_postbacks_*.csv"), dtype=str, keep_default_na=False)
    s = s[s.redownload == "false"].drop_duplicates("postback_id")
    s["c"] = s.ad_network.map(POSTBACK)
    s["week"] = np.clip((day_of(s.received_at) - 3) // 7, 0, WEEKS - 1)
    s["cv"] = s.conversion_value.astype(int)
    cube = {c: pd.crosstab(x.week, x.cv).reindex(index=range(WEEKS), columns=range(32), fill_value=0).to_numpy(float)
            for c, x in s.groupby("c")}
    installs = {c: cube[c].sum(1) if c in cube else
                np.bincount(a.week[a.label == c], minlength=WEEKS).astype(float) for c in channels}
    m = a[a.mature]
    named = m[m.consent & m.label.isin(NETWORKS + ["organic iOS"])]
    for c in NETWORKS:
        ok("%s: postbacks outnumber the installs the export names by more than three to one" % c,
           cube[c][:MATURE].sum() > 3 * (m.label == c).sum())

    def channel_values(col):
        """each channel's twelve-month net revenue per install over every install of the mature weeks, and each
        iOS network's price by first-48-hour value"""
        cells = lambda f: (np.bincount(f.cv, minlength=32).astype(float), np.bincount(f.cv, weights=f[col], minlength=32))
        rn, rv = cells(named)
        ref = np.where(rn >= 20, rv / np.maximum(rn, 1), named[col].mean())
        n, vc = {}, {}
        for c in NETWORKS + [ASA, "organic iOS"]:
            n[c], tot = cells(m[(m.label == c) & m.consent])
            vc[c] = np.where(n[c] >= 20, tot / np.maximum(n[c], 1), ref * tot.sum() / (n[c] * ref).sum())
        pn, pv = cells(m[m.label == ""])
        rest, nc = pn.copy(), {}
        for c in NETWORKS:
            nc[c] = np.maximum(cube[c][:MATURE].sum(0) - n[c], 0)
            rest -= nc[c]
        nc["organic iOS"] = np.maximum(rest, 0)
        den = sum(nc[c] * vc[c] for c in nc)
        r = np.where((den > 0) & (pn >= 20), pv / np.maximum(den, 1e-9), pv.sum() / den.sum())
        out, price = {}, {}
        for c in channels:
            if c in NETWORKS:
                tot = n[c] + nc[c]
                price[c] = np.where(tot > 0, (n[c] * vc[c] + nc[c] * vc[c] * r) / np.maximum(tot, 1e-9), vc[c])
                out[c] = (tot * price[c]).sum() / tot.sum()
            else:
                out[c] = m[col][m.label == c].mean()
        return out, price, dict(n=n, vc=vc, nc=nc, r=r, pool_n=pn, pool_v=pv)
    v12, price, X = channel_values("v")
    r12, _p, _x = channel_values("rec12")
    bridge = (X["n"]["Meta iOS"] + X["nc"]["Meta iOS"])
    bridge = (bridge * X["vc"]["Meta iOS"]).sum() / bridge.sum()
    priced_named = sum((X["nc"][c] * X["vc"][c]).sum() for c in X["nc"]) / X["pool_v"].sum()
    u = FIG["unnamed"]
    ok("accounts with no channel: %d paid EUR %.0f; valued like the named installs they come to %.2f times that" % (
        X["pool_n"].sum(), X["pool_v"].sum(), priced_named),
       int(X["pool_n"].sum()) == u["accounts"] and abs(X["pool_v"].sum() / u["paid"] - 1) < 0.005
       and abs(priced_named - u["adding_up_named_price"]) < 0.015, (X["pool_n"].sum(), X["pool_v"].sum(), priced_named))
    ok("Meta iOS, every postback valued like the named installs: EUR %.2f (the shortcut's figure)" % bridge,
       abs(bridge - FIG["channels"]["Meta iOS"]["bridge_value"]) < 0.06, bridge)
    sa = m[(m.label == ASA) & ~m.consent]
    cnt = np.bincount(sa.cv, minlength=32)
    est = (cnt * X["vc"][ASA] * X["r"]).sum() / cnt.sum()
    asn = (cnt * X["vc"][ASA]).sum() / cnt.sum()
    k = FIG["check_search_ads"]
    ok("Apple Search Ads' %d installs without tracking paid EUR %.2f each; the pricing puts %.2f, the named installs' "
       "value %.2f" % (len(sa), sa.v.mean(), est, asn),
       len(sa) == k["installs"] and abs(sa.v.mean() - k["paid"]) < 0.06 and abs(est - k["estimate"]) < 0.06
       and abs(asn - k["named_by_cell"]) < 0.08 and abs(est - sa.v.mean()) < 0.2 * abs(asn - sa.v.mean()),
       (len(sa), sa.v.mean(), est, asn))

    # the web checkout's subscribers on AppLovin Android: every charge after the last open is on file
    w = m[m.web & (m.label == "AppLovin Android") & (m.sub_plan_at_last_open == "monthly") & (m.auto_renew_at_last_open == "yes")]
    wb = b[b.account_id.isin(w.index) & b.monthly].join(w[["lo"]], on="account_id", rsuffix="_a")
    opened = wb[wb.d <= wb.lo].groupby("account_id").size()
    w = w[w.index.isin(opened.index)]
    wb = wb[wb.account_id.isin(w.index)]
    after = wb[(wb.d > wb.lo) & (wb.d < wb.day + HORIZON)]
    charged = after.net.sum() / len(w)
    k = FIG["check_web"]
    ok("AppLovin Android's %d web subscribers were charged EUR %.2f each after their last open" % (len(w), charged),
       len(w) == k["subscribers"] and abs(charged - k["charged"]) < 0.01, (len(w), charged, k))

    # ------------------------------------------------------------------ what a budget buys
    sp = pd.read_csv(one("ad_spend_daily_*.csv"), dtype=str, keep_default_na=False)
    sp["c"] = [NAMES[k] for k in zip(sp.network, sp.os)]
    sp["week"] = (pd.to_datetime(sp.date) - pd.Timestamp("2024-11-04")).dt.days // 7
    spend = sp.assign(e=sp.spend_eur.astype(float)).groupby(["c", "week"]).e.sum().round(2).unstack().reindex(columns=range(WEEKS))
    thursday = lambda start, n: np.array([(start + dt.timedelta(days=7 * i + 3)).month for i in range(n)])
    wmonth, pmonth = thursday(dt.date(2024, 11, 4), WEEKS), thursday(dt.date(2027, 1, 4), 52)

    def quality(c):
        if c in NETWORKS:
            return (cube[c] @ price[c]) / np.maximum(cube[c].sum(1), 1)
        mine = a[a.label == c]
        mm = mine[mine.mature]
        tot, cnt = np.bincount(mm.cv, weights=mm.v, minlength=32), np.bincount(mm.cv, minlength=32)
        p = np.where(cnt >= 20, tot / np.maximum(cnt, 1), mm.v.mean())
        return (np.bincount(mine.week, weights=p[mine.cv.to_numpy()], minlength=WEEKS)
                / np.maximum(np.bincount(mine.week, minlength=WEEKS), 1))

    def fit(y_of, regress="budget"):
        """log outcome on the channel, its own slope on the week's budget with the share of it spent beside it (or
        its own slope on the week's spend), and a month pattern shared by the channels"""
        rows = []
        for c in channels:
            lb, ls = np.log(bud[c].to_numpy(float)), np.log(spend.loc[c].to_numpy(float))
            ld = ls - lb
            y = y_of(c)
            for wk in range(WEEKS):
                if y[wk] > 0:
                    rows.append(dict(c=c, month=wmonth[wk], xb=lb[wk] - lb.mean(), xd=ld[wk] - ld.mean(), xsp=ls[wk] - ls.mean(),
                                     y=np.log(y[wk])))
        d = pd.DataFrame(rows)
        cols = {("a", c): (d.c == c).astype(float) for c in channels}
        if regress == "budget":
            cols.update({("s", c): (d.c == c) * d.xb for c in channels})
            cols.update({("d", c): (d.c == c) * d.xd for c in channels})
        else:
            cols.update({("s", c): (d.c == c) * d.xsp for c in channels})
        cols.update({("m", mth): (d.month == mth).astype(float) for mth in range(2, 13)})
        Xm = pd.DataFrame(cols)
        beta = pd.Series(np.linalg.lstsq(Xm.to_numpy(float), d.y.to_numpy(), rcond=None)[0], index=Xm.columns)
        mon = np.concatenate([[0.0], [beta[("m", mth)] for mth in range(2, 13)]])
        return beta, mon
    bi, mi = fit(lambda c: installs[c])
    bv, mv = fit(quality)
    bs, _ms = fit(lambda c: installs[c], regress="spend")
    out = {}
    for c in members:
        b_, s_ = bud[c].to_numpy(float), spend.loc[c].to_numpy(float)
        share = s_.sum() / b_.sum()
        xh = np.log(b_) - np.log(b_).mean()
        pl, st = plan[c].to_numpy(float), stretch[c].to_numpy(float)
        si, sv = bi[("s", c)], bv[("s", c)]
        scale = installs[c].sum() / np.exp(bi[("a", c)] + si * xh + mi[wmonth - 1]).sum()
        shape = np.exp(sv * xh[:MATURE] + mv[wmonth[:MATURE] - 1])
        level = v12[c] / ((shape * installs[c][:MATURE]).sum() / installs[c][:MATURE].sum())
        res = {}
        for tag, money in (("plan", pl), ("stretch", st)):
            xp = np.log(money / share) - np.log(b_).mean()
            n = scale * np.exp(bi[("a", c)] + si * xp + mi[pmonth - 1])
            val = level * np.exp(sv * xp + mv[pmonth - 1])
            res[tag] = dict(revenue=(n * val).sum(), ret=(n * val).sum() / money.sum(), value=(n * val).sum() / n.sum())
        out[c] = dict(ret=res["plan"]["ret"], stretch=res["stretch"]["ret"], value=res["plan"]["value"],
                      next=res["plan"]["ret"] * (si + sv), revenue=res["plan"]["revenue"], revenue_s=res["stretch"]["revenue"],
                      el=si, el_spend=bs[("s", c)])
    ga = FIG["channels"]["Google Android"]
    ok("Google Android: installs rise %.2f per cent for one per cent of budget, %.2f when fitted on spend" % (
        out["Google Android"]["el"], out["Google Android"]["el_spend"]),
       abs(out["Google Android"]["el"] - ga["budget_elasticity"]) < 0.006
       and abs(out["Google Android"]["el_spend"] - ga["spend_elasticity"]) < 0.006)
    up = dn = 0.0
    for _i, r in chg[chg.iloc[:, 1] == "Google Android"].iterrows():
        if str(r.iloc[3]).endswith("%"):
            w0 = (pd.Timestamp(r.iloc[2]).date() - dt.date(2024, 11, 4)).days // 7
            tot = installs["Google Android"][w0:w0 + int(r.iloc[4])].sum()
            up, dn = (up + tot, dn) if str(r.iloc[3]).startswith("+") else (up, dn + tot)
    ok("Google Android's moved weeks: installs in the raised weeks over the lowered weeks %.2f" % (up / dn),
       abs(up / dn - FIG["check_moves"]["Google Android"]["actual"]) < 0.006, up / dn)

    # ------------------------------------------------------------------ the graded figures
    mine = {}
    for c in members:
        mine["return " + c], mine["stretch return " + c] = out[c]["ret"], out[c]["stretch"]
        mine["value at plan " + c], mine["next euro " + c] = out[c]["value"], out[c]["next"]
    mine["unrecorded share AppLovin Android"] = 100 * (1 - r12["AppLovin Android"] / v12["AppLovin Android"])
    mine["value per install Meta iOS"] = v12["Meta iOS"]
    mine["plan revenue iOS networks"] = sum(out[c]["revenue"] for c in NETWORKS)
    mine["stretch adds"] = sum(out[c]["revenue_s"] - out[c]["revenue"] for c in members)
    same = 0
    for fid, gold in FIG["figure"].items():
        lo, hi = FIG["figure_band"][fid]
        x = mine[fid]
        nd = -3 if gold > 10000 else (1 if fid.startswith("unrecorded") else 2)
        same += round(x, nd) == gold
        ok("%s: %s recomputed %.4f, band %s to %s" % (fid, gold, x, lo, hi), lo <= x <= hi and abs(x / gold - 1) < 0.01, x)
    ok("%d of %d graded figures equal to the stated digit under the continuous fit" % (same, len(FIG["figure"])),
       same >= len(FIG["figure"]) - 6, same)
    band = lambda x: "cut" if x < 0.90 else ("hold" if x < 1.20 else "scale")
    ok("the bands: " + ", ".join("%s %s" % (c, band(out[c]["ret"])) for c in members),
       {c: band(out[c]["ret"]) for c in members} == FIG["bands"])

    # ------------------------------------------------------------------ the golden files, against both
    gc = pd.read_csv(glob.glob(os.path.join(G, "*.csv"))[0])
    ok("golden CSV: seven rows, highest return first", len(gc) == 7 and list(gc.iloc[:, 2]) == sorted(gc.iloc[:, 2], reverse=True))
    for _i, r in gc.iterrows():
        c = r.iloc[0]
        ok("golden CSV, %s: %s %.2f %.2f %.2f %.2f" % (c, r.iloc[1], r.iloc[2], r.iloc[3], r.iloc[4], r.iloc[5]),
           r.iloc[1] == FIG["bands"][c] == band(out[c]["ret"]) and r.iloc[2] == FIG["return_plan"][c]
           and r.iloc[3] == FIG["return_stretch"][c] and r.iloc[4] == FIG["value_plan"][c] and r.iloc[5] == FIG["next_euro"][c])
    gw = pd.read_excel(glob.glob(os.path.join(G, "*.xlsx"))[0], sheet_name=0, header=None)
    head = str(gw.iloc[0, 0])
    ok("golden workbook: the first sheet opens on the call", head.startswith("2027 media plan: scale ") and " cut " in head, head)
    body = gw.iloc[5:12]
    ok("golden workbook: the first sheet's rows are the CSV's",
       all(body.iloc[i, 0] == gc.iloc[i, 0] and str(body.iloc[i, 1]).lower() == gc.iloc[i, 1]
           and all(abs(float(body.iloc[i, 2 + j]) - float(gc.iloc[i, 2 + j])) < 1e-9 for j in range(4)) for i in range(7)))
    print("\n%d passed, %d failed" % (N["pass"], N["fail"]))
    return 1 if N["fail"] else 0


if __name__ == "__main__":
    sys.exit(main())
