"""The golden analysis, run on the shipped files alone. PackObs reads target/ back into the arrays core.py's
estimators take (nothing here reads the simulation), and the routes below are core's own, with two things the pack
adds to them: the App Store's report is on Pacific days, so the App Store accounts' charges are put on Pacific days
before they are set against it, and the conventions the pack leaves to the analyst (the period the two are compared
on, where a refund is netted, the install week of a postback) are run as variants."""
import datetime as dt
import os
import sys

import numpy as np
import pandas as pd
from openpyxl import load_workbook

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import core as C  # noqa: E402
import pack as P  # noqa: E402
import docs as D  # noqa: E402

DAY0 = pd.Timestamp("2024-11-04")
K, NM, END_DAY, MD = C.K, int(C.END_DAY // C.MONTH_DAYS) + 1, C.END_DAY, C.MONTH_DAYS
OFF = 5                                    # day tables start five days before day 0
_j = np.arange(1700) - OFF
BIN = {"period": np.maximum(np.floor(_j / MD), 0).astype(int),
       "calendar": np.array([(d.year - 2024) * 12 + d.month - 11 for d in
                             (dt.date(2024, 11, 4) + dt.timedelta(days=int(x)) for x in _j)])}
BIN["calendar"] = np.maximum(BIN["calendar"], 0)
CHANNEL = {v: k for k, v in P.SOURCE.items()}                      # (network, os) to the plan's channel name
SKAN = {v: k for k, v in P.SKAN_NET.items()}


def secs(s):
    t = pd.to_datetime(s, format="%Y-%m-%dT%H:%M:%SZ")
    return ((t - DAY0) // pd.Timedelta(seconds=1)).to_numpy(np.int64)


def days(s):
    return ((pd.to_datetime(s, format="%Y-%m-%d") - DAY0) // pd.Timedelta(days=1)).to_numpy(np.int64)


def pacific_day(ts):
    ts = np.asarray(ts, dtype=np.int64)
    off = np.full(ts.shape, 8 * 3600, dtype=np.int64)
    for a, b in P.PDT:
        off[(ts >= a) & (ts < b)] = 7 * 3600
    return (ts - off) // 86400


class PackObs:
    """the pack's content as arrays, in the accounts file's order"""

    def __init__(self, target, pb_days=3, slip=None):
        """slip names one piece of the files' mess left unhandled (checks.py runs each to show it moves nothing):
        staff, web_dup, refund, resent, reinstall, redownload, dup_postback"""
        self.target = target
        f = lambda k: os.path.join(target, P.FILES[k])
        # ---- accounts: consumer accounts only (policy 2.2) ---------------------------------------------------
        a = pd.read_csv(f("acc"), dtype=str, keep_default_na=False)
        self.rows = dict(accounts=len(a))
        if slip != "staff":
            a = a[a.account_type == "consumer"]
        a = a.reset_index(drop=True)
        n = self.n = len(a)
        self.account_id = a.account_id.to_numpy()
        cr = secs(a.created_at)
        self.day = cr // 86400
        self.sec = cr % 86400
        self.week = self.day // 7
        self.ios = (a.platform == "ios").to_numpy()
        self.country = a.storefront.str.upper().map({"ES": 0, "IT": 1, "PT": 2}).to_numpy()
        self.cv = a.conversion_value_48h.astype(int).to_numpy()
        self.consent = (a.tracking_status == "authorized").to_numpy()
        self.last_open = secs(a.last_open_at) // 86400
        self.auto_on = (a.auto_renew_at_last_open == "yes").to_numpy()
        self.plan_seen = a.sub_plan_at_last_open.map({"": 0, "monthly": 1, "annual": 2}).to_numpy()
        state_trial = (a.sub_state_at_last_open == "trial").to_numpy()
        self.mature = self.week < C.MATURE
        ix = pd.Index(self.account_id)
        assert ix.is_unique

        # ---- billing events: production charges of consumer accounts, a re-sent row once, refunded charges out --
        b = pd.read_csv(f("bill"), dtype=str, keep_default_na=False)
        self.rows["billing"] = len(b)
        b = b[b.environment == "production"]
        b = b[ix.get_indexer(b.account_id) >= 0]
        again = b.duplicated(["account_id", "product_id", "event_type", "transaction_at"], keep="first").to_numpy()
        twice = b[again]
        b = b[~again]
        refunded = set(b.refund_of_event_id[b.event_type == "refund"]) if slip != "refund" else set()
        gone = b[b.event_id.isin(refunded)]
        self.rows.update(refunds=len(refunded), billing_used=len(b), billing_twice=len(twice))
        b = b[(b.event_type != "refund") & ~b.event_id.isin(refunded)]
        bi = ix.get_indexer(b.account_id)
        bt = secs(b.transaction_at)
        bd = bt // 86400
        monthly = b.product_id.str.endswith("monthly").to_numpy()
        first = (b.event_type == "first_charge").to_numpy()
        self.web = np.zeros(n, bool)
        self.web[bi[(b.store == "web").to_numpy()]] = True
        trial = (self.cv & 8) > 0
        conv = np.where(trial, self.day + 7, self.day)
        conv[bi[first]] = bd[first]
        self.conv_day = conv
        self.csec = self.sec.copy()
        self.csec[bi[first]] = bt[first] % 86400
        self.rdays = conv[:, None] + np.round(MD * np.arange(K))[None, :].astype(np.int64)
        self.rec = np.zeros((n, K), bool)
        m = monthly
        k = np.rint((bd[m] - conv[bi[m]]) / MD).astype(int)
        assert (k >= 0).all() and (k < K).all() and (self.rdays[bi[m], k] == bd[m]).all()
        self.rec[bi[m], k] = True
        assert (self.rec[:, 1:] <= self.rec[:, :-1]).all()               # a subscription's charges run without a gap
        self.rec_a0 = np.zeros(n, bool)
        self.rec_a0[bi[~monthly & first]] = True
        self.true_charge = self.rec                                      # read only where every charge is on file
        self.n_rec = self.rec.sum(1)
        self.trial_seen = state_trial & ~self.web
        self.netm, self.neta = C.net_m(self.country, self.web), C.net_a(self.country, self.web)
        self.NM = NM
        self.extra = None
        if slip == "web_dup":                                            # each re-sent checkout row summed again
            di = ix.get_indexer(twice.account_id)
            ok = (di >= 0) & (twice.event_type != "refund").to_numpy()
            dd = secs(twice.transaction_at)[ok] // 86400
            di = di[ok]
            inside = dd < self.day[di] + 365
            price = np.where(twice.product_id[ok].str.endswith("monthly").to_numpy(), self.netm[di], self.neta[di])
            self.extra = np.bincount(di[inside], weights=price[inside], minlength=n)
        # the refunded charges, by store and plan, on the day each was made (they are in the stores' reports too)
        gi = ix.get_indexer(gone.account_id)
        self._gone = dict(i=gi, t=secs(gone.transaction_at), monthly=gone.product_id.str.endswith("monthly").to_numpy())

        # ---- the attribution export: an account's install row, a re-sent row once ---------------------------------
        t = pd.read_csv(f("attr"), dtype=str, keep_default_na=False)
        self.rows["attribution"] = len(t)
        if slip != "reinstall":
            t = t[t.is_reinstall == "false"]
        if slip != "resent":
            t = t.drop_duplicates("install_id", keep="first")
        ti = ix.get_indexer(t.account_id)
        t = t[ti >= 0]
        ti = ti[ti >= 0]
        if slip not in ("reinstall", "resent"):
            assert np.unique(ti).size == ti.size == n                   # one install for every consumer account
        lab = np.full(len(t), -1)
        ms, pf = t.media_source.to_numpy(), t.platform.to_numpy()
        for (net, osn), c in CHANNEL.items():
            lab[(ms == net) & (pf == osn)] = C.ORDER.index(c)
        lab[(ms == "organic") & (pf == "ios")] = len(C.ORDER)
        lab[(ms == "organic") & (pf == "android")] = len(C.ORDER) + 1
        assert ((lab >= 0) | (ms == "")).all()
        self.label = np.full(n, -1)
        self.label[ti[::-1]] = lab[::-1]                                 # an account's first row in the export
        self.inst_day = self.day.copy()
        self.inst_day[ti[::-1]] = (secs(t.install_time) // 86400)[::-1]
        self._rows = None
        if slip in ("reinstall", "resent"):                              # every export row counted as an install
            self._rows = (lab, np.clip(secs(t.install_time) // 86400 // 7, 0, C.WEEKS - 1))
        self.pool = self.label < 0
        assert self.ios[self.pool].all()                                 # only an iOS account can be without a channel

        # ---- the networks' install postbacks: one per install, a re-delivered one once, redownloads out ---------
        s = pd.read_csv(f("skan"), dtype=str, keep_default_na=False)
        self.rows["postbacks"] = len(s)
        if slip != "redownload":
            s = s[s.redownload == "false"]
        if slip != "dup_postback":
            s = s.drop_duplicates("postback_id", keep="first")
        self._pb = dict(c=s.ad_network.map(SKAN).to_numpy(), day=secs(s.received_at) // 86400,
                        cv=s.conversion_value.astype(int).to_numpy())
        self.rows["postbacks_used"] = len(s)
        self.set_postback_days(pb_days)

        # ---- the stores' daily reports, on each store's own day ---------------------------------------------------
        self.daily = {}
        ap = pd.read_csv(f("apple"), dtype=str, keep_default_na=False)
        gp = pd.read_csv(f("google"), dtype=str, keep_default_na=False)
        self.rows.update(apple=len(ap), google=len(gp))
        for pl, df, dcol, ecol, ucol, kinds in (
                (1, ap, "date_pt", "event", "units",
                 {"Paid Subscription from Free Trial": "first", "Subscribe": "first", "Renew": "ren", "Refund": "refund"}),
                (0, gp, "date_utc", "transaction_type", "transactions",
                 {"charge_new": "first", "charge_renewal": "ren", "refund": "refund"})):
            d = days(df[dcol]) + OFF
            kd = df[ecol].map(kinds).to_numpy()
            mo = df.product_id.str.endswith("monthly").to_numpy()
            un = df[ucol].astype(int).to_numpy()
            assert (d >= 0).all() and pd.notna(kd).all()
            self.daily[pl] = {(kk, mm): np.bincount(d[(kd == kk) & (mo == mm)], weights=un[(kd == kk) & (mo == mm)],
                                                    minlength=1700) for kk in ("first", "ren", "refund") for mm in (True, False)}
        self.store = self.store_bins()
        self.mon = (self.rdays // MD).astype(int)
        sh = np.where(self.ios & ~self.web)[0]
        self.mon[sh] = BIN["period"][np.clip(pacific_day(self.rdays[sh] * 86400 + self.csec[sh][:, None]) + OFF, 0, 1699)]

        # ---- budgets, spend, the plan --------------------------------------------------------------------------
        sp = pd.read_csv(f("spend"), dtype=str, keep_default_na=False)
        self.rows["spend"] = len(sp)
        wk = days(sp.date) // 7
        cents = np.rint(sp.spend_eur.astype(float).to_numpy() * 100).astype(np.int64)
        ch = np.array([C.ORDER.index(CHANNEL[(a_, b_)]) for a_, b_ in zip(sp.network, sp.os)])
        tot = np.zeros((len(C.ORDER), C.WEEKS), np.int64)
        np.add.at(tot, (ch, wk), cents)
        wb = load_workbook(os.path.join(target, D.FILES["budget"]), read_only=True, data_only=True)
        rows = list(wb["Weekly budgets"].iter_rows(values_only=True))
        hdr = list(rows[2])
        body = rows[3:3 + C.WEEKS]
        assert [r[0].date() if hasattr(r[0], "date") else r[0] for r in body] == \
            [dt.date(2024, 11, 4) + dt.timedelta(days=7 * w) for w in range(C.WEEKS)]
        self.B = {c: dict(budget=np.array([float(r[hdr.index(c)]) for r in body]), spend=tot[ci] / 100.0)
                  for ci, c in enumerate(C.ORDER)}
        self.pushes = {c: [] for c in C.ORDER}
        for r in list(wb["Changes"].iter_rows(values_only=True))[1:]:
            if r[3] and r[3] != "back to base":
                eff = r[2].date() if hasattr(r[2], "date") else r[2]
                self.pushes[r[1]].append(((eff - dt.date(2024, 11, 4)).days // 7, int(r[4]), 1 + int(r[3].rstrip("%")) / 100.0))
        for c in C.ORDER:
            self.pushes[c].sort()
        wp = load_workbook(os.path.join(target, D.FILES["plan"]), read_only=True, data_only=True)
        self.plan, self.stretch = {}, {}
        g = list(wp["Growth channels"].iter_rows(values_only=True))
        st = list(wp["Stretch case"].iter_rows(values_only=True))
        hd = list(g[3])
        for c in hd[2:-1]:
            j = hd.index(c)
            self.plan[c] = np.array([float(r[j]) for r in g[4:56]])
            self.stretch[c] = np.array([float(r[list(st[3]).index(c)]) for r in st[4:56]])
        br = list(wp["Brand"].iter_rows(values_only=True))
        self.brand = {br[3][2]: np.array([float(r[2]) for r in br[4:56]])}

    # the installs each channel bought, week by week
    def set_postback_days(self, pb_days=3):
        self.agg, self.agg_cv = {}, {}
        for ci, c in enumerate(C.ORDER):
            if c in C.GATED:
                m = self._pb["c"] == c
                wk = np.clip((self._pb["day"][m] - pb_days) // 7, 0, C.WEEKS - 1)
                t = np.zeros((C.WEEKS, 32))
                np.add.at(t, (wk, self._pb["cv"][m]), 1)
                self.agg_cv[c], self.agg[c] = t, t.sum(1)
            elif self._rows is not None:
                self.agg[c] = np.bincount(self._rows[1][self._rows[0] == ci], minlength=C.WEEKS).astype(float)
            else:
                self.agg[c] = np.bincount(self.week[self.label == ci], minlength=C.WEEKS).astype(float)

    def bin(self, d, idx, bins="period", pt=True):
        """the comparison period of a charge made on UTC day d on account idx (an App Store account's on its
        Pacific day, the day the App Store's report puts it on)"""
        d = np.asarray(d, np.int64)
        if pt:
            d = np.where(self.ios[idx] & ~self.web[idx], pacific_day(d * 86400 + self.csec[idx]), d)
        return BIN[bins][np.clip(d + OFF, 0, 1699)]

    def store_bins(self, bins="period", refunds="charge", pt=True):
        """each store's charges by period: first charges, renewals and annual first charges, with the refunded
        purchases taken out where the convention takes them out"""
        out = {}
        g = self._gone
        for pl in (0, 1):
            cnt = lambda key: np.bincount(BIN[bins][:1700], weights=self.daily[pl][key], minlength=NM)[:NM]
            first, ren, ann = cnt(("first", True)), cnt(("ren", True)), cnt(("first", False))
            mine = (self.ios[g["i"]] == bool(pl)) & ~self.web[g["i"]]
            if refunds == "charge":                                  # each refunded purchase out on the day it was charged
                gd = g["t"][mine] // 86400
                if pl == 1 and pt:
                    gd = pacific_day(g["t"][mine])
                gb = BIN[bins][np.clip(gd + OFF, 0, 1699)]
                first = first - np.bincount(gb[g["monthly"][mine]], minlength=NM)[:NM]
                ann = ann - np.bincount(gb[~g["monthly"][mine]], minlength=NM)[:NM]
            elif refunds == "refund_day":                            # the stores' refunds netted on the day of the refund
                first = first - cnt(("refund", True))
                ann = ann - cnt(("refund", False))
            elif refunds == "renewals":                              # the stores' refunds netted from their renewals
                ren = ren - cnt(("refund", True))
                ann = ann - cnt(("refund", False))
            out[pl] = dict(first=first, ren=ren, ann=ann)
        return out


_core_fit, _core_values = C.s1_fit, C.values


def s1_fit(O, split="store", trim=0, form="geo", cadence=MD, bins="period", pt=True, refunds="charge", annual="own",
           joint=False):
    """core.s1_fit on the pack: the share of trial-end candidates charged and the monthly continuation of a silent
    subscription, fitted to the stores' excess over the records period by period, the App Store's on Pacific days"""
    if not isinstance(O, PackObs):
        return _core_fit(O, split=split, trim=trim, form=form, cadence=cadence)
    ren, fst = C.s1_candidates(O)
    S = O.store_bins(bins, refunds, pt)
    cnt = lambda b: np.bincount(b, minlength=NM)[:NM].astype(float)
    fits = {}
    for g in (((0,), (1,)) if split == "store" else ((0, 1),)):
        mk = np.isin(O.ios.astype(int), g) & ~O.web
        ii, kk = np.nonzero(O.rec & mk[:, None])
        b = O.bin(O.rdays[ii, kk], ii, bins, pt)
        F = sum(S[pl]["first"] for pl in g) - cnt(b[kk == 0])
        R = sum(S[pl]["ren"] for pl in g) - cnt(b[kk > 0])
        ia = np.where(mk & O.rec_a0)[0]
        A = sum(S[pl]["ann"] for pl in g) - cnt(O.bin(O.conv_day[ia], ia, bins, pt))
        fm = fst & mk & (O.plan_seen == 1)
        fa = fst & mk & (O.plan_seen == 2)
        c_m = F.sum() / max(1, fm.sum())
        own_a = A.sum() / max(1, fa.sum())
        c_a = {"own": own_a, "monthly": c_m, "none": 0.0}[annual]
        idx = np.where(ren & mk)[0]
        last = O.rdays[idx, O.n_rec[idx] - 1]
        fi = np.where(fm)[0]
        te = O.day[fi] + 7
        Mr = np.zeros((K, NM)); Mf = np.zeros((K, NM))
        for j in range(1, K):
            d = last + np.round(cadence * j).astype(int)
            ok = d <= END_DAY
            Mr[j - 1] = cnt(O.bin(d[ok], idx[ok], bins, pt))
            d2 = te + np.round(cadence * j).astype(int)
            ok = d2 <= END_DAY
            Mf[j - 1] = cnt(O.bin(d2[ok], fi[ok], bins, pt))
        use = np.arange(NM) < NM - 1 - trim
        best = None
        q1s = np.linspace(0.50, 0.99, 50) if form == "two" else (None,)
        Tf = cnt(O.bin(te[te <= END_DAY], fi[te <= END_DAY], bins, pt))  # the monthly trials' ends, period by period
        for q in np.linspace(0.60, 0.99, 196):
            for q1 in q1s:
                w = q ** np.arange(1, K + 1) if q1 is None else q1 * q ** np.arange(0, K)
                cm = c_m
                if joint:                                            # the share and the continuation fitted together
                    a_, b_ = (w @ Mf)[use], (R - w @ Mr)[use]
                    cm = float((Tf[use] @ F[use] + a_ @ b_) / max(Tf[use] @ Tf[use] + a_ @ a_, 1e-9))
                err = (((w @ Mr + cm * (w @ Mf)) - R)[use] ** 2).sum()
                if joint:
                    err += ((cm * Tf - F)[use] ** 2).sum()
                if best is None or err < best[0]:
                    best = (err, q, q if q1 is None else q1, cm)
        if joint:
            c_m = best[3]
            c_a = {"own": own_a, "monthly": c_m, "none": 0.0}[annual]
        for pl in g:
            fits[pl] = dict(c_m=float(c_m), c_a=float(c_a), q=float(best[1]), q1=float(best[2]), F=F, R=R, A=A,
                            first_candidates=int(fm.sum()), annual_candidates=int(fa.sum()), renew_candidates=int(idx.size),
                            fitted=(best[1] ** np.arange(1, K + 1)) @ Mr + c_m * ((best[1] ** np.arange(1, K + 1)) @ Mf))
    return fits


S1_KW = ("split", "trim", "form", "cadence", "bins", "pt", "refunds", "annual", "joint")
S1_DEF = dict(split="store", trim=0, form="geo", cadence=MD, bins="period", pt=True, refunds="charge", annual="own",
              joint=False)


def values(O, s1="golden", **kw):
    """core.values on the pack, with the pack's conventions carried into the fit"""
    if not isinstance(O, PackObs):
        return _core_values(O, s1, **kw)
    fk = {k: kw.get(k, S1_DEF[k]) for k in S1_KW}
    k1 = (id(O), "v", s1, bool(kw.get("webq"))) + tuple(fk[k] for k in S1_KW)
    if k1 not in C._CACHE:
        fits = None
        if s1 == "golden":
            fits = s1_fit(O, **fk)
            if kw.get("webq"):
                q = C.s1_web_fit(O)
                for f_ in fits.values():
                    f_["q"] = f_["q1"] = q
        v = C.s1_values(O, s1, split=fk["split"], trim=fk["trim"], form=fk["form"], cadence=fk["cadence"], fits=fits)[0]
        C._CACHE[k1] = v if O.extra is None else v + O.extra
    return C._CACHE[k1]


C.s1_fit = s1_fit
C.values = values

# the conventions the pack adds to core's nineteen
PACK_VARIANTS = [
    ("stores and records compared by calendar month", dict(bins="calendar")),
    ("the App Store's report days taken as UTC days", dict(pt=False)),
    ("the stores' refunds netted on the day of the refund", dict(refunds="refund_day")),
    ("the stores' refunds netted from their renewals", dict(refunds="renewals")),
    ("calendar months, one fit across both stores", dict(bins="calendar", split="pooled")),
]
OBS_VARIANTS = [("a postback's install four days before it arrived", dict(pb_days=4))]
MONTH_VARIANT = "a week's month taken from its Monday"


# --------------------------------------------------------------------------------------------------------------
# the response taken the other defensible ways: its design, its weeks, the month a week belongs to, and how the
# fitted equations are carried to the plan year (as they stand, or with their levels set to the history as the
# estimate sets them). The battery runs each, so the bands are what careful work spans.
# --------------------------------------------------------------------------------------------------------------
THU = (C.WMONTH.copy(), C.PLAN_MONTH.copy())                       # a week's month by its Thursday
MON = (np.array([int(C.month_of_day(7 * w)) for w in range(C.WEEKS)]),
       np.array([int(C.month_of_day(791 + 7 * t)) for t in range(52)]))
_core_cells = C._cells


def _cells(cv, cells):
    """core's first-48-hour cells, and two coarser readings of the same five bits"""
    if cells == "sessions":                                        # the sessions bucket alone
        return np.asarray(cv) & 7
    if cells == "bits":                                            # the trial and purchase bits alone
        return np.asarray(cv) >> 3
    return _core_cells(cv, cells)


C._cells = _cells
C.LEVELS.update(sessions=8, bits=4)
S2_KW = ("s2", "cells", "minn", "tilt")
_core_asa = C.asa_ratio
_RC = [None]                               # (grouping, smallest group) of Apple Search Ads' ratio, when not core's


def _asa(O, v, cells="fine", rcells="tier2"):
    """core's ratio of Apple Search Ads' unnamed to named value by two groups; or the ratio at which its unnamed
    installs, priced at its named installs' value by first-48-hour value, add up to what they paid: one number, or
    value by value where the value holds enough of them"""
    if _RC[0] is None:
        return _core_asa(O, v, cells, rcells)
    how, mn = _RC[0]
    ci = C.ORDER.index("Apple Search Ads")
    T = C.s2_cells(O, v, cells)
    key = _cells(O.cv, cells)
    nc = (O.label == ci) & O.mature & ~O.consent
    n = np.bincount(key[nc], minlength=T["nk"]).astype(float)
    paid = np.bincount(key[nc], weights=v[nc], minlength=T["nk"])
    priced = n * T["vc"][ci]
    one = paid.sum() / priced.sum()
    if how == "one":
        return np.full(T["nk"], one)
    return np.where((n >= mn) & (priced > 0), paid / np.maximum(priced, 1e-9), one)


C.asa_ratio = _asa


def series(O, v, quality="golden", s2kw=None):
    """each channel's weeks: log budget, log spend, installs and value per install"""
    k = dict(s2="golden", cells="fine", minn=20, tilt="cell")
    k.update(s2kw or {})
    return {c: dict(lb=np.log(O.B[c]["budget"]), ls=np.log(O.B[c]["spend"]), n=np.asarray(O.agg[c], float),
                    q=np.asarray(C.weekly_quality(O, v, c, quality, k["s2"], k["cells"], k["minn"], k["tilt"]), float))
            for c in C.ORDER}


def fit_x(S, chans, wmon, x="budget", share=True, months="pooled", weeks_i=(0, C.WEEKS), weeks_v=(0, C.WEEKS),
          extra=None, iv=False, qpool=False):
    """log installs and log value per install on the week's log budget with the log share of it spent beside it (or
    on log spend, or on log spend with log budget as its instrument): each channel its own level and slopes, the
    month pattern shared by `chans` or each channel's own; `extra` is one more column of the installs equation"""
    nC = len(chans)
    out = {}
    for nm, key, (lo, hi) in (("i", "n", weeks_i), ("v", "q", weeks_v)):
        rows = [(j, w) for j, c in enumerate(chans) for w in range(lo, hi)
                if np.isfinite(S[c][key][w]) and S[c][key][w] > 0]
        nmon = 11 * nC if months == "own" else 11
        ne = 1 if (extra is not None and nm == "i") else 0
        X = np.zeros((len(rows), 3 * nC + nmon + ne))
        Z = np.zeros_like(X)
        y = np.zeros(len(rows))
        one = qpool and nm == "v"                                    # one value slope for every channel
        for i, (j, w) in enumerate(rows):
            sc = S[chans[j]]
            X[i, j] = 1
            X[i, nC + (0 if one else j)] = sc["ls"][w] if x == "spend" else sc["lb"][w]
            if share:
                X[i, 2 * nC + j] = sc["ls"][w] - sc["lb"][w]
            if wmon[w] > 1:
                X[i, 3 * nC + (11 * j if months == "own" else 0) + wmon[w] - 2] = 1
            if ne:
                X[i, -1] = extra(w)
            Z[i] = X[i]
            Z[i, nC + (0 if one else j)] = sc["lb"][w]
            y[i] = np.log(sc[key][w])
        keep = np.abs(X).sum(0) > 0
        beta = np.zeros(X.shape[1])
        if iv:
            beta[keep] = np.linalg.lstsq(Z[:, keep].T @ X[:, keep], Z[:, keep].T @ y, rcond=None)[0]
        else:
            beta[keep] = np.linalg.lstsq(X[:, keep], y, rcond=None)[0]
        res = y - X @ beta
        who = np.array([j for j, _w in rows])
        mon = beta[3 * nC:3 * nC + nmon]
        mon = mon.reshape(nC, 11) if months == "own" else np.tile(mon, (nC, 1))
        out[nm] = dict(a={c: beta[j] for j, c in enumerate(chans)},
                       b={c: beta[nC + (0 if one else j)] for j, c in enumerate(chans)},
                       g={c: beta[2 * nC + j] for j, c in enumerate(chans)},
                       mon={c: np.concatenate([[0.0], mon[j]]) for j, c in enumerate(chans)},
                       e=float(beta[-1]) if ne else 0.0, resid={c: res[who == j] for j, c in enumerate(chans)})
    return out


def carry(O, S, F, c, v12, wmon, pmon, level="asis", share="ratio", x="budget", extra=None, extra_at=0.0, smear=False,
          dbar_weeks=(0, C.WEEKS), share_weeks=None):
    """a channel's fitted equations at the plan's weekly spend and at the stretch column's. level 'history' sets the
    installs equation to the installs counted over the 104 weeks and the value equation to the channel's twelve-month
    value over the complete weeks (the estimate's way); 'asis' reads the equations as fitted, the share spent at its
    two-year ratio, at its mean log or averaged over its weeks, with or without the smearing factor"""
    sc, sp, st = S[c], O.plan[c], O.stretch[c]
    d0, d1 = dbar_weeks
    dbar = O.B[c]["spend"][d0:d1].sum() / O.B[c]["budget"][d0:d1].sum()
    ld_all = sc["ls"] - sc["lb"]
    ld = ld_all if share_weeks is None else ld_all[share_weeks[0]:share_weeks[1]]
    sw = (0, C.WEEKS) if share_weeks is None else share_weeks
    dsh = O.B[c]["spend"][sw[0]:sw[1]].sum() / O.B[c]["budget"][sw[0]:sw[1]].sum()
    xh = sc["ls"] if x == "spend" else sc["lb"]
    xp = (lambda spend: np.log(spend)) if x == "spend" else (lambda spend: np.log(spend / dbar))
    fi, fv = F["i"], F["v"]
    line = lambda f, xv, mon, e=0.0: np.exp(f["a"][c] + f["b"][c] * xv + f["mon"][c][mon - 1] + e)

    def shr(f):
        g = f["g"][c]
        if g == 0.0:
            return 1.0
        if share == "ratio":
            return float(dsh ** g)
        return float(np.exp(g * ld.mean())) if share == "meanlog" else float(np.exp(g * ld).mean())
    if level == "history":
        eh = fi["e"] * np.array([extra(w) for w in range(C.WEEKS)]) if extra is not None else 0.0
        ki = sc["n"].sum() / line(fi, xh, wmon, eh).sum()
        wt = sc["n"][:C.MATURE]
        fm = line(fv, xh[:C.MATURE], wmon[:C.MATURE])
        kv = v12 / ((fm * wt).sum() / wt.sum())
        if share_weeks is not None:                                  # the share spent at another window's average
            ki *= np.exp(fi["g"][c] * ld).mean() / np.exp(fi["g"][c] * ld_all).mean()
            em = np.exp(fv["g"][c] * ld_all[:C.MATURE])
            kv *= np.exp(fv["g"][c] * ld).mean() / ((em * wt).sum() / wt.sum())
    else:
        ki = shr(fi) * (float(np.exp(fi["resid"][c]).mean()) if smear else 1.0)
        kv = shr(fv) * (float(np.exp(fv["resid"][c]).mean()) if smear else 1.0)
    n, vp = ki * line(fi, xp(sp), pmon, fi["e"] * extra_at), kv * line(fv, xp(sp), pmon)
    ns, vs = ki * line(fi, xp(st), pmon, fi["e"] * extra_at), kv * line(fv, xp(st), pmon)
    out = dict(roas=float((n * vp).sum() / sp.sum()), revenue=float((n * vp).sum()), installs_week=float(n.mean()),
               vpi=float((n * vp).sum() / n.sum()), roas_s=float((ns * vs).sum() / st.sum()),
               revenue_s=float((ns * vs).sum()), el=float(fi["b"][c]), qs=float(fv["b"][c]))
    out["marginal"] = out["roas"] * (out["el"] + out["qs"])
    return out


def carry_form(O, S, c, kind, wmon, pmon, weeks_v):
    """the same two equations in levels, or in levels on the logs ('semilog'), fitted channel by channel"""
    sc, sp, st = S[c], O.plan[c], O.stretch[c]
    B, sh = np.exp(sc["lb"]), np.exp(sc["ls"] - sc["lb"])
    dbar = O.B[c]["spend"].sum() / O.B[c]["budget"].sum()

    def X(b, h, mon):
        cols = [np.ones(len(b)), b if kind == "levels" else np.log(b), h if kind == "levels" else np.log(h)]
        return np.column_stack(cols + [(mon == m).astype(float) for m in range(2, 13)])

    def fit(y, lo, hi):
        w = np.array([k for k in range(lo, hi) if np.isfinite(y[k]) and y[k] > 0])
        Xm = X(B[w], sh[w], wmon[w])
        keep = np.abs(Xm).sum(0) > 0
        beta = np.zeros(Xm.shape[1])
        beta[keep] = np.linalg.lstsq(Xm[:, keep], y[w], rcond=None)[0]
        return beta
    bi, bv = fit(sc["n"], 0, C.WEEKS), fit(sc["q"], *weeks_v)
    at = lambda spend: (X(spend / dbar, np.full(len(spend), dbar), pmon) @ bi,
                        X(spend / dbar, np.full(len(spend), dbar), pmon) @ bv)
    (n, vp), (ns, vs), (n1, v1) = at(sp), at(st), at(sp * 1.01)
    rev = float((n * vp).sum())
    return dict(roas=rev / sp.sum(), revenue=rev, installs_week=float(n.mean()), vpi=rev / float(n.sum()),
                roas_s=float((ns * vs).sum() / st.sum()), revenue_s=float((ns * vs).sum()),
                marginal=float(((n1 * v1).sum() - rev) / (0.01 * sp.sum())), el=float("nan"), qs=float("nan"))


EST = dict(quality="golden", chans="all", weeks_v=(0, C.WEEKS), level="history")       # the estimate's own way
LIT = dict(quality="value", chans="plan", weeks_v=(0, C.MATURE), level="asis")          # the equations as fitted
X_DEF = dict(month="thu", months="pooled", x="budget", share_term=True, iv=False, weeks_i=(0, C.WEEKS), extra=None,
             share="ratio", smear=False, form="loglog", s1how="golden", qpool=False, dbar_weeks=(0, C.WEEKS),
             share_weeks=None)
EXTRA = {"trend": lambda w: w / 52.0, "year2": lambda w: float(w >= 52)}


def route_x(O, s1kw=None, s2kw=None, **opt):
    """every plan channel's figures with the response taken one of the other defensible ways"""
    o = dict(X_DEF)
    o.update(opt)
    s2kw = dict(s2kw or {})
    _RC[0] = s2kw.pop("rcells", None)
    try:
        return _route_x(O, o, s1kw, s2kw)
    finally:
        _RC[0] = None


def _route_x(O, o, s1kw, s2kw):
    a2 = [s2kw.get("s2", "golden"), s2kw.get("cells", "fine"), s2kw.get("minn", 20), s2kw.get("tilt", "cell")]
    v = C.values(O, o["s1how"], **(s1kw or {}))
    v12 = C.channel_values(O, v, *a2)
    r12 = C.channel_values(O, C.values(O, "raw"), *a2)
    S = series(O, v, o["quality"], s2kw)
    wmon, pmon = MON if o["month"] == "mon" else THU
    chans = list(C.ORDER) if o["chans"] == "all" else list(C.MEMBERS)
    F = None
    if o["form"] == "loglog":
        F = fit_x(S, chans, wmon, x=o["x"], share=o["share_term"], months=o["months"], weeks_i=o["weeks_i"],
                  weeks_v=o["weeks_v"], extra=EXTRA.get(o["extra"]), iv=o["iv"], qpool=o["qpool"])
    res = {}
    for c in C.MEMBERS:
        n12 = float(O.agg[c][:C.MATURE].sum())
        if F is not None:
            f = carry(O, S, F, c, v12[c], wmon, pmon, level=o["level"], share=o["share"], x=o["x"],
                      extra=EXTRA.get(o["extra"]), extra_at=1.0 if o["extra"] else 0.0, smear=o["smear"],
                      dbar_weeks=o["dbar_weeks"], share_weeks=o["share_weeks"])
        else:
            f = carry_form(O, S, c, o["form"], wmon, pmon, o["weeks_v"])
        res[c] = dict(v12=v12[c], rec12=r12[c] * n12, rev12=v12[c] * n12, unrec=1 - r12[c] / v12[c], **f)
    return res


_KEEP = []                                  # every derived set of observations stays alive: core caches by id()


def clock_obs(O):
    """the same accounts with the install week and the 365 days counted from the attribution export's install time"""
    O2 = PackObs.__new__(PackObs)
    O2.__dict__.update(O.__dict__)
    _KEEP.append(O2)
    O2.day = np.maximum(O.inst_day, 0)
    O2.week = O2.day // 7
    O2.mature = O2.week < C.MATURE
    O2.set_postback_days(3)
    return O2


S1S2_KEYS = set(S1_KW) | set(S2_KW) | {"webq"}
# the estimate's way with one more choice taken differently
EST_VARIANTS = [
    ("the annual trials at the monthly trials' share", dict(_s1=dict(annual="monthly"))),
    ("the trial-end share and the continuation fitted together", dict(_s1=dict(joint=True))),
    ("first-48-hour values by the sessions bucket alone", dict(_s2=dict(cells="sessions"))),
    ("first-48-hour values by the trial and purchase bits alone", dict(_s2=dict(cells="bits"))),
    ("the month pattern of the plan's seven channels, Apple Search Ads left out of the fit", dict(chans="plan")),
    ("installs response on the 52 complete weeks", dict(weeks_i=(0, C.MATURE))),
    ("a trend in the installs equation, held at its mid-history level", dict(extra="trend")),
    ("a second-year level in the installs equation, carried", dict(extra="year2")),
]
# the equations read as fitted, and that reading with one more choice taken differently
LIT_NAME = "the equations as fitted, value per install on the complete weeks, the share spent at its two-year ratio"
LIT_VARIANTS = [
    ("", {}),
    ("each channel's own month pattern", dict(months="own")),
    ("the smearing factor", dict(smear=True)),
    ("the share spent at its mean log", dict(share="meanlog")),
    ("the share spent averaged over its weeks", dict(share="weekly")),
    ("installs response on the 52 complete weeks", dict(weeks_i=(0, C.MATURE))),
    ("the launch quarter left out of the installs equation", dict(weeks_i=(13, C.WEEKS))),
    ("installs response on the last 78 weeks", dict(weeks_i=(26, C.WEEKS))),
    ("the budget alone, the share spent left out", dict(share_term=False)),
    ("spend instrumented by the budget", dict(x="spend", share_term=False, iv=True)),
    ("a trend in the installs equation, held at its mid-history level", dict(extra="trend")),
    ("a second-year level in the installs equation, carried", dict(extra="year2")),
    ("Apple Search Ads in the month pattern", dict(chans="all")),
    ("value per install priced by first-48-hour value over the 104 weeks", dict(quality="golden", weeks_v=(0, C.WEEKS))),
    ("the levels set to the history", dict(level="history")),
]


# every way of taking a step (the stores' excess, the unnamed installs, the record's clocks, the response), and the
# three ways of carrying the two equations as fitted; the battery crosses them
WAYS = [
    ("one fit across both stores", dict(split="pooled"), None, {}, None),
    ("two-rate continuation", dict(form="two"), None, {}, None),
    ("fit without the last two months", dict(trim=2), None, {}, None),
    ("thirty-day cadence", dict(cadence=30.0), None, {}, None),
    ("continuation read on the web subscribers", dict(webq=True), None, {}, None),
    ("stores and records compared by calendar month", dict(bins="calendar"), None, {}, None),
    ("the App Store's report days taken as UTC days", dict(pt=False), None, {}, None),
    ("the stores' refunds netted on the day of the refund", dict(refunds="refund_day"), None, {}, None),
    ("the stores' refunds netted from their renewals", dict(refunds="renewals"), None, {}, None),
    ("calendar months, one fit across both stores", dict(bins="calendar", split="pooled"), None, {}, None),
    ("the annual trials at the monthly trials' share", dict(annual="monthly"), None, {}, None),
    ("the trial-end share and the continuation fitted together", dict(joint=True), None, {}, None),
    ("first-48-hour cells in eight groups", None, dict(cells="tier8"), {}, None),
    ("first-48-hour cells in four groups", None, dict(cells="tier4"), {}, None),
    ("cells of fifty or more", None, dict(minn=50), {}, None),
    ("each source's consenting installs through one tilt", None, dict(tilt="one"), {}, None),
    ("non-consenting installs at the unattributed accounts' value, whatever the network", None, dict(s2="flat"), {}, None),
    ("non-consenting installs at Apple Search Ads' ratio", None, dict(s2="ratio"), {}, None),
    ("first-48-hour values by the sessions bucket alone", None, dict(cells="sessions"), {}, None),
    ("first-48-hour values by the trial and purchase bits alone", None, dict(cells="bits"), {}, None),
    ("every first-48-hour value on its own installs, however few", None, dict(minn=1), {}, None),
    ("non-consenting installs at Apple Search Ads' ratio, value by value", None, dict(s2="ratio", rcells=("each", 20)), {},
     None),
    ("non-consenting installs at Apple Search Ads' ratio, value by value, every value on its own installs", None,
     dict(s2="ratio", rcells=("each", 1), minn=1), {}, None),
    ("a postback's install four days before it arrived", None, None, {}, "pb4"),
    ("the 365 days and the install week counted from the attribution export's install time", None, None, {}, "clock"),
    ("each channel's own month pattern", None, None, dict(months="own"), None),
    ("installs response without the launch quarter", None, None, dict(weeks_i=(13, C.WEEKS)), None),
    ("value response on the mature weeks' own values", None, None, dict(quality="value"), None),
    ("one value slope across channels", None, None, dict(qpool=True), None),
    ("delivery share from the mature weeks", None, None, dict(dbar_weeks=(0, C.MATURE)), None),
    ("installs response on the last 78 weeks", None, None, dict(weeks_i=(26, C.WEEKS)), None),
    ("spend instrumented by the budget", None, None, dict(x="spend", share_term=False, iv=True), None),
    ("the budget alone, the delivery left out", None, None, dict(share_term=False), None),
    ("the month pattern of the plan's seven channels, Apple Search Ads left out of the fit", None, None, dict(chans="plan"),
     None),
    ("installs response on the 52 complete weeks", None, None, dict(weeks_i=(0, C.MATURE)), None),
    ("a trend in the installs equation, held at its mid-history level", None, None, dict(extra="trend"), None),
    ("a second-year level in the installs equation, carried", None, None, dict(extra="year2"), None),
    ("the delivery share of the last 52 weeks", None, None, dict(dbar_weeks=(C.MATURE, C.WEEKS),
                                                                 share_weeks=(C.MATURE, C.WEEKS)), None),
]
NEW_WAYS = ("every first-48-hour value on its own installs, however few",
            "non-consenting installs at Apple Search Ads' ratio, value by value",
            "non-consenting installs at Apple Search Ads' ratio, value by value, every value on its own installs",
            "the delivery share of the last 52 weeks")     # the ways neither core's list nor the lists below carry
AS_FITTED = [
    ("the equations carried as fitted, the share spent at its two-year ratio", dict(level="asis", share="ratio")),
    ("the equations carried as fitted, the share spent at its mean log", dict(level="asis", share="meanlog")),
    ("the equations carried as fitted, the share spent averaged over its weeks", dict(level="asis", share="weekly")),
]


def crossed(O):
    """every way under each as-fitted carry, the bare carries (with and without the smearing factor), and the new
    ways under the estimate's own carry"""
    obs = {None: O, "pb4": _pb_obs(O, 4), "clock": clock_obs(O)}
    fam = []
    for nm, s1, s2, opt, ob in WAYS:
        if nm in NEW_WAYS:
            fam.append((nm, route_x(obs[ob], s1, s2, **dict(EST, **opt))))
    for cn, ckw in AS_FITTED:
        fam.append((cn, route_x(O, **dict(EST, **ckw))))
        fam.append((cn + "; the smearing factor", route_x(O, **dict(EST, smear=True, **ckw))))
        for nm, s1, s2, opt, ob in WAYS:
            fam.append((cn + "; " + nm, route_x(obs[ob], s1, s2, **dict(EST, **dict(opt, **ckw)))))
    return fam


def more_family(O, verbose=False):
    """the battery beyond core's nineteen and the pack's conventions"""
    fam = []
    O3 = clock_obs(O)
    fam.append(("the 365 days and the install week counted from the attribution export's install time", C.route(O3)))
    for nm, kw in EST_VARIANTS:
        kw = dict(kw)
        s1, s2 = kw.pop("_s1", None), kw.pop("_s2", None)
        if not kw:                                                   # a choice core's route carries
            fam.append((nm, C.route(O, **dict(s1 or {}, **(s2 or {})))))
        else:
            fam.append((nm, route_x(O, s1, s2, **dict(EST, **kw))))
    for nm, kw in LIT_VARIANTS:
        fam.append((LIT_NAME + ("; " + nm if nm else ""), route_x(O, **dict(LIT, **kw))))
    for nm, kw in C.VARIANTS + PACK_VARIANTS + [(n, dict(k)) for n, k in EST_VARIANTS[:4]]:
        kw = dict(kw)
        kw.update(kw.pop("_s1", None) or {})
        kw.update(kw.pop("_s2", None) or {})
        if not set(kw) <= S1S2_KEYS:
            continue                                                 # a choice about the response: taken above
        s1 = {k: x for k, x in kw.items() if k in S1_KW or k == "webq"}
        s2 = {k: x for k, x in kw.items() if k in S2_KW}
        fam.append((LIT_NAME + "; " + nm, route_x(O, s1, s2, **LIT)))
    fam.append((LIT_NAME + "; a postback's install four days before it arrived",
                route_x(_pb_obs(O, 4), **LIT)))
    fam.append((LIT_NAME + "; the 365 days and the install week counted from the attribution export's install time",
                route_x(O3, **LIT)))
    return fam + crossed(O)


def _pb_obs(O, pb_days):
    O2 = PackObs.__new__(PackObs)
    O2.__dict__.update(O.__dict__)
    _KEEP.append(O2)
    O2.set_postback_days(pb_days)
    return O2


# each shortcut under the other ways of taking the response: its own member stays across the line under every one
SHORT_CONV = [("the estimate's way", dict(EST)), ("as fitted", dict(LIT)),
              ("as fitted, each channel's own month pattern", dict(LIT, months="own")),
              ("as fitted, the share at its mean log", dict(LIT, share="meanlog")),
              ("as fitted, the share averaged over its weeks", dict(LIT, share="weekly")),
              ("as fitted, the smearing factor", dict(LIT, smear=True)),
              ("each channel's own month pattern", dict(EST, months="own"))]


def shortcuts(O):
    out = {}
    for sid, member in (("S1", "AppLovin Android"), ("S2", "Meta iOS"), ("S3", "Google Android")):
        vals = []
        for nm, kw in SHORT_CONV:
            kw = dict(kw)
            if sid == "S1":
                r = route_x(O, s1how=C.HURRIED["S1"]["s1"], **kw)
            elif sid == "S2":
                r = route_x(O, s2kw=dict(s2=C.HURRIED["S2"]["s2"]), **kw)
            else:
                kw.update(x="spend", share_term=False)
                r = route_x(O, **kw)
            vals.append((nm, float(r[member]["roas"])))
        out[sid] = dict(member=member, values=vals)
    return out


# ways of taking a step that a figure from the shipped files rules out: run, reported, and kept out of the bands
def plan_blocks(O):
    """where the media plan's weekly spend changes, against the two ways of giving a week its month"""
    chg = np.zeros(52, bool)
    for c in O.plan:
        chg[1:] |= np.diff(O.plan[c]) != 0
    thu = np.zeros(52, bool); thu[1:] = np.diff(THU[1]) != 0
    mon = np.zeros(52, bool); mon[1:] = np.diff(MON[1]) != 0
    apart = thu != mon
    return dict(changes=int(chg.sum()), on_thursday_months=int((chg & thu).sum()), month_starts=int(thu.sum()),
                apart=int((thu & apart).sum()), apart_on_thursday=int((chg & thu & apart).sum()),
                apart_on_monday=int((chg & mon & apart).sum()), off=int((chg & ~thu).sum()))


def ruled_out(O, v, fits, monday):
    """each refuted way with the route it files and the figure that refutes it"""
    out = [dict(name=MONTH_VARIANT, route=monday, by="media plan", blocks=plan_blocks(O)),
           dict(name="the equations as fitted, each channel's own month pattern, a week's month taken from its Monday",
                route=route_x(O, **dict(LIT, months="own", month="mon")), by="media plan", blocks=plan_blocks(O))]
    # the two equations in levels, or in levels on the logs: each logged budget move left out and its weeks predicted
    S = series(O, v, "golden")
    wmon = THU[0]
    err = {k: {} for k in ("log", "levels", "semilog")}
    for c in C.ORDER:
        sc = S[c]
        B, sh, y = np.exp(sc["lb"]), np.exp(sc["ls"] - sc["lb"]), sc["n"]
        for kind in err:
            e = []
            for w0, k, _f in O.pushes[c]:
                te = np.arange(w0, min(w0 + k, C.WEEKS))
                tr = np.setdiff1d(np.arange(C.WEEKS), te)
                lin = kind == "levels"
                X = lambda w: np.column_stack([np.ones(len(w)), B[w] if lin else np.log(B[w]), sh[w] if lin else np.log(sh[w])]
                                              + [(wmon[w] == m).astype(float) for m in range(2, 13)])
                Xt = X(tr)
                keep = np.abs(Xt).sum(0) > 0
                beta = np.zeros(Xt.shape[1])
                beta[keep] = np.linalg.lstsq(Xt[:, keep], np.log(y[tr]) if kind == "log" else y[tr], rcond=None)[0]
                p = X(te) @ beta
                e += list(np.abs((np.exp(p) if kind == "log" else p) / y[te] - 1))
            err[kind][c] = float(np.mean(e))
    weeks = sum(min(w0 + k, C.WEEKS) - w0 for c in C.ORDER for w0, k, _f in O.pushes[c])
    mean = {k: float(sum(err[k][c] * sum(min(w0 + kk, C.WEEKS) - w0 for w0, kk, _f in O.pushes[c]) for c in C.ORDER) / weeks)
            for k in err}
    hold = dict(weeks=int(weeks), error=mean, lower_on=int(sum(err["log"][c] < min(err["levels"][c], err["semilog"][c])
                                                               for c in C.ORDER)), channels=len(C.ORDER))
    for nm, kind in (("the two equations in levels, channel by channel", "levels"),
                     ("the two equations in levels on the logs, channel by channel", "semilog")):
        out.append(dict(name=nm, route=route_x(O, **dict(EST, form=kind)), by="moved weeks", holdout=hold, kind=kind))
    # one price for a network's unnamed installs, their first-48-hour values unused: Apple Search Ads' unnamed installs
    ci = C.ORDER.index("Apple Search Ads")
    T = C.s2_cells(O, v, "one")
    nc = (O.label == ci) & O.mature & ~O.consent
    out.append(dict(name="one price for a network's unnamed installs, their first-48-hour values unused",
                    route=C.route(O, cells="one"), by="Apple Search Ads",
                    paid=float(v[nc].mean()), priced=float(T["vc"][ci][0] * T["r"][0]), installs=int(nc.sum())))
    # Apple Search Ads' ratio as one number for every first-48-hour value: its own unnamed installs that started a trial,
    # by the sessions bucket of their value, against what they paid
    cvv = np.asarray(O.cv)
    trial, bought, bucket = (cvv >> 3) & 1, (cvv >> 4) & 1, cvv & 7
    Tf = C.s2_cells(O, v)
    named = Tf["vc"][ci][cvv]
    one = float(v[nc].sum() / named[nc].sum())
    grp = {}
    for nm, m in (("lower", bucket < 4), ("upper", bucket >= 4)):
        k = nc & (trial == 1) & (bought == 0) & m
        grp[nm] = dict(installs=int(k.sum()), paid=float(v[k].mean()), priced=float(one * named[k].mean()))
    for nm, kw in (("non-consenting installs at Apple Search Ads' ratio, one number", dict(s2="ratio", rcells=("one", 1))),
                   ("non-consenting installs at Apple Search Ads' ratio, one number, every value on its own installs",
                    dict(s2="ratio", rcells=("one", 1), minn=1))):
        out.append(dict(name=nm, route=route_x(O, None, kw, **EST), by="Apple Search Ads by sessions", ratio=one, groups=grp))
    # the annual trials left out: the stores' annual first charges over the records'
    ann = {pl: float(fits[pl]["A"].sum()) for pl in (0, 1)}
    out.append(dict(name="the annual trials last seen set to renew left out", route=C.route(O, annual="none"),
                    by="annual first charges", excess=ann,
                    candidates={pl: int(fits[pl]["annual_candidates"]) for pl in (0, 1)}))
    return out


def plan_checks(O):
    """the plan, the stretch column and the budget moves the analysis reads are the workbook's own"""
    out = []
    for c in C.MEMBERS:
        out.append(("plan " + c, bool(np.array_equal(O.plan[c], C.plan_spend(c)))))
        out.append(("stretch " + c, bool(np.allclose(O.stretch[c] / O.plan[c], C.CH[c]["stretch"], rtol=0, atol=1e-9))))
    out.append(("brand", bool(np.array_equal(O.brand["Apple Search Ads"], C.plan_spend("Apple Search Ads")))))
    for c in C.ORDER:
        out.append(("moves " + c, [(a, b, round(f, 2)) for a, b, f in O.pushes[c]] ==
                    [(a, b, round(f, 2)) for a, b, f in C.CH[c]["pushes"]]))
    return out


def run(target, verbose=False):
    """every route the build needs, computed on the shipped files"""
    O = PackObs(target)
    g = C.route(O)
    fam = [(nm, C.route(O, **kw)) for nm, kw in C.VARIANTS + PACK_VARIANTS]
    for nm, kw in OBS_VARIANTS:
        fam.append((nm, C.route(_pb_obs(O, **kw))))
    # a week's month taken from its Monday (core takes it from the week's Thursday), the plan read from the workbook
    keep = C.WMONTH, C.PLAN_MONTH, C.plan_spend
    C.WMONTH = np.array([int(C.month_of_day(7 * w)) for w in range(C.WEEKS)])
    C.PLAN_MONTH = np.array([int(C.month_of_day(791 + 7 * t)) for t in range(52)])
    C.plan_spend = lambda c: O.plan[c] if c in O.plan else O.brand[c]
    try:
        monday = C.route(O, week_month="monday")
    finally:
        C.WMONTH, C.PLAN_MONTH, C.plan_spend = keep
    keys = [["S1"], ["S2"], ["S3"], ["S1", "S2"], ["S1", "S3"], ["S2", "S3"], ["S1", "S2", "S3"]]
    lat = {"+".join(k): C.lattice_route(O, k) for k in keys}
    direct = C.route(O, "raw", "direct", "average")
    v = C.values(O)
    refs = dict(S1=C.referee_s1(O), S2=C.referee_s2(O, v), S3=C.referee_s3(O, v))
    fam += more_family(O)
    fits = s1_fit(O)
    return dict(O=O, golden=g, family=fam, lattice=lat, direct=direct, v=v, refs=refs, fits=fits,
                ruled_out=ruled_out(O, v, fits, monday), shortcuts=shortcuts(O), clock=C.route(clock_obs(O)))


if __name__ == "__main__":
    import time
    t0 = time.time()
    X = run(sys.argv[1])
    print("%.0fs" % (time.time() - t0))
    for c in C.ORDER:
        print("%-18s" % c, " ".join("%s %.4f" % (k, X["golden"][c][k]) for k in ("roas", "roas_s", "vpi", "marginal", "unrec")))
