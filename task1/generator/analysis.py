"""The golden analysis, run on the shipped files alone. PackObs reads target/ back into the arrays core.py's
estimators take (nothing here reads the simulation), and every route below is core's own. The pack adds what only
files carry: the App Store's report is on Pacific days, so the App Store accounts' charges are put on Pacific days
before they are set against it, and the conventions the files leave to the analyst (the period the stores and the
records are compared on, where a refunded purchase is netted, the clock an install runs from, the month a week
belongs to) are properties of a view of the observations, each run as a variant."""
import datetime as dt
import itertools
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
K, END_DAY, MD = C.K, C.END_DAY, C.MONTH_DAYS
NM = int(END_DAY // MD) + 1
OFF = 5                                    # day tables start five days before day 0
_j = np.arange(1700) - OFF
BIN = {"period": np.maximum(np.floor(_j / MD), 0).astype(int),
       "calendar": np.maximum(np.array([(d.year - 2024) * 12 + d.month - 11 for d in
                                        (dt.date(2024, 11, 4) + dt.timedelta(days=int(x)) for x in _j)]), 0)}
CHANNEL = {v: k for k, v in P.SOURCE.items()}                      # (network, os) to the plan's channel name
SKAN = {v: k for k, v in P.SKAN_NET.items()}
MKT = {"ES": 0, "IT": 1, "PT": 2}
CONV = dict(align="split", bins="period", pt=True, refunds="charge", clock="created")
ALIGN = {"three": ((3, 1.0),), "four": ((4, 1.0),), "split": ((3, 0.5), (4, 0.5))}
_KEEP = []                                  # every view stays alive: core caches by id()


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

    def __init__(self, target, slip=None):
        """slip names one piece of the files' mess left unhandled (checks.py runs each to show it moves nothing):
        staff, web_dup, refund, resent, reinstall, redownload, dup_postback"""
        self.target, self.slip = target, slip
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
        self.created_day = cr // 86400
        self.sec = cr % 86400
        self.ios = (a.platform == "ios").to_numpy()
        self.country = a.storefront.map(MKT).to_numpy()
        self.market = self.country
        self.cv = a.conversion_value_48h.astype(int).to_numpy()
        self.consent = (a.tracking_status == "authorized").to_numpy()
        self.last_open = secs(a.last_open_at) // 86400
        self.auto_on = (a.auto_renew_at_last_open == "yes").to_numpy()
        self.plan_seen = a.sub_plan_at_last_open.map({"": 0, "monthly": 1, "annual": 2}).to_numpy()
        self.trial_seen = (a.sub_state_at_last_open == "trial").to_numpy()
        self.web = (a.sub_store_at_last_open == "web").to_numpy()
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
        if slip is None:
            assert ((b.store == "web").to_numpy() == self.web[bi]).all()     # a subscription bills by one route
        trial = (self.cv & 8) > 0
        conv = np.where(trial, self.created_day + 7, self.created_day)
        conv[bi[first]] = bd[first]
        self.conv_day = conv
        self.csec = self.sec.copy()                                      # the time of day a subscription is charged
        self.csec[bi[first]] = bt[first] % 86400
        self.rdays = conv[:, None] + np.round(MD * np.arange(K))[None, :].astype(np.int64)
        self.rec = np.zeros((n, K), bool)
        m = monthly
        k = np.rint((bd[m] - conv[bi[m]]) / MD).astype(int)
        assert (k >= 0).all() and (k < K).all() and (self.rdays[bi[m], k] == bd[m]).all()
        self.rec[bi[m], k] = True
        if slip is None:
            assert (self.rec[:, 1:] <= self.rec[:, :-1]).all()           # a subscription's charges run without a gap
        self.rec_a0 = np.zeros(n, bool)
        self.rec_a0[bi[~monthly & first]] = True
        self.true_charge = self.rec                                      # read only where every charge is on file
        self.n_rec = self.rec.sum(1)
        self.netm, self.neta = C.net_m(self.country, self.web), C.net_a(self.country, self.web)
        self.rows["annual_renewals"] = int((~monthly & ~first).sum())
        self.extra = None
        if slip == "web_dup":                                            # each re-sent checkout row summed again
            di = ix.get_indexer(twice.account_id)
            ok = (di >= 0) & (twice.event_type != "refund").to_numpy()
            dd = secs(twice.transaction_at)[ok] // 86400
            di = di[ok]
            inside = dd < self.created_day[di] + 365
            price = np.where(twice.product_id[ok].str.endswith("monthly").to_numpy(), self.netm[di], self.neta[di])
            self.extra = np.bincount(di[inside], weights=price[inside], minlength=n)
        # the refunded purchases, by store and plan, at the time each was charged (they are in the stores' reports too)
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
        if slip not in ("reinstall", "resent", "staff"):
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
        self.inst_day = self.created_day.copy()
        self.inst_day[ti[::-1]] = (secs(t.install_time) // 86400)[::-1]
        self._rows = None
        if slip in ("reinstall", "resent"):                              # every export row counted as an install
            self._rows = (lab, np.clip(secs(t.install_time) // 86400 // 7, 0, C.WEEKS - 1))
        self.pool = self.label < 0
        if slip != "staff":
            assert self.ios[self.pool].all()                             # only an iOS account can be without a channel

        # ---- the ad platforms' daily spend: a campaign's market, each channel's week ------------------------------
        sp = pd.read_csv(f("spend"), dtype=str, keep_default_na=False)
        self.rows["spend"] = len(sp)
        cm = sp.drop_duplicates("campaign_id")
        assert sp.groupby("campaign_id").country.nunique().max() == 1    # a campaign runs in one market
        self.camp_market = dict(zip(cm.campaign_id, cm.country.map(MKT)))
        self.rows["campaigns"] = len(cm)
        wk = days(sp.date) // 7
        cents = np.rint(sp.spend_eur.astype(float).to_numpy() * 100).astype(np.int64)
        ch = np.array([C.ORDER.index(CHANNEL[(a_, b_)]) for a_, b_ in zip(sp.network, sp.os)])
        tot = np.zeros((len(C.ORDER), C.WEEKS), np.int64)
        np.add.at(tot, (ch, wk), cents)
        self.spend_mw = np.zeros((len(C.ORDER), 3, C.WEEKS))             # each channel's spend by market and week
        np.add.at(self.spend_mw, (ch, sp.country.map(MKT).to_numpy(), wk), cents / 100.0)

        # ---- the networks' install postbacks: one per install, a re-delivered one once, redownloads out ---------
        s = pd.read_csv(f("skan"), dtype=str, keep_default_na=False)
        self.rows["postbacks"] = len(s)
        if slip != "redownload":
            s = s[s.redownload == "false"]
        if slip != "dup_postback":
            s = s.drop_duplicates("postback_id", keep="first")
        self._pb = dict(c=s.ad_network.map(SKAN).to_numpy(), day=secs(s.received_at) // 86400,
                        cv=s.conversion_value.astype(int).to_numpy(), market=s.campaign_id.map(self.camp_market).to_numpy())
        assert not pd.isna(self._pb["market"]).any()
        self._pb["market"] = self._pb["market"].astype(int)
        self.rows["postbacks_used"] = len(s)

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

        # ---- budgets and the plan ------------------------------------------------------------------------------
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
        self.plan_weeks = [r[0].date() if hasattr(r[0], "date") else r[0] for r in g[4:56]]
        br = list(wp["Brand"].iter_rows(values_only=True))
        self.brand = {br[3][2]: np.array([float(r[2]) for r in br[4:56]])}
        self.NM = NM
        self.conv = dict(CONV)
        self._apply()

    # ------------------------------------------------------------------------------------------------------------
    def view(self, **conv):
        """the same files under another reading of what they leave open"""
        new = dict(self.conv, **conv)
        for O2 in _KEEP:
            if O2.target == self.target and O2.slip == self.slip and O2.conv == new and O2.account_id is self.account_id:
                return O2
        O2 = PackObs.__new__(PackObs)
        O2.__dict__.update(self.__dict__)
        O2.conv = new
        O2._apply()
        _KEEP.append(O2)
        return O2

    def _apply(self):
        cv = self.conv
        # the clock an install runs from: the account's creation, or the export's install time
        self.day = self.created_day if cv["clock"] == "created" else np.maximum(self.inst_day, 0)
        self.week = np.minimum(self.day // 7, C.WEEKS - 1)
        self.mature = self.week < C.MATURE
        # the installs each channel bought, week by week (and by market and first-48-hour value from the postbacks)
        self.agg, self.agg_cv, self.agg_cvm = {}, {}, {}
        early = {}
        for ci, c in enumerate(C.ORDER):
            if c in C.GATED:
                m = self._pb["c"] == c
                t = np.zeros((C.WEEKS, 3, 32))
                for back, wt in ALIGN[cv["align"]]:
                    np.add.at(t, (np.clip((self._pb["day"][m] - back) // 7, 0, C.WEEKS - 1), self._pb["market"][m],
                                  self._pb["cv"][m]), wt)
                    if cv == CONV:                                 # a half dated before the first week is counted in it
                        early[c] = early.get(c, 0.0) + wt * float((self._pb["day"][m] - back < 0).sum())
                self.agg_cvm[c], self.agg_cv[c], self.agg[c] = t, t.sum(1), t.sum((1, 2))
            elif self._rows is not None:
                self.agg[c] = np.bincount(self._rows[1][self._rows[0] == ci], minlength=C.WEEKS).astype(float)
            else:
                self.agg[c] = np.bincount(self.week[self.label == ci], minlength=C.WEEKS).astype(float)
        if early:
            self.rows["early_halves"] = round(sum(early.values()), 1)
        # the stores' charges by comparison period, and each account's charges on the same periods
        self.store = self.store_bins()
        self.mon = BIN[cv["bins"]][np.clip(self.rdays + OFF, 0, 1699)].astype(np.int16)
        if cv["pt"]:
            sh = np.where(self.ios & ~self.web)[0]
            self.mon[sh] = BIN[cv["bins"]][np.clip(pacific_day(self.rdays[sh] * 86400 + self.csec[sh][:, None]) + OFF, 0,
                                                   1699)]

    def bin(self, d, idx):
        """the comparison period of a charge made on UTC day d on account idx (an App Store account's on its
        Pacific day, the day the App Store's report puts it on)"""
        d = np.asarray(d, np.int64)
        if self.conv["pt"]:
            d = np.where(self.ios[idx] & ~self.web[idx], pacific_day(d * 86400 + self.csec[idx]), d)
        return BIN[self.conv["bins"]][np.clip(d + OFF, 0, 1699)]

    def store_bins(self):
        """each store's charges by period: first charges, renewals and annual first charges, with the refunded
        purchases taken out where the convention takes them out"""
        bins, refunds, pt = self.conv["bins"], self.conv["refunds"], self.conv["pt"]
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


def s1_fit(O, split="store", trim=0, form="geo", cadence=MD):
    """core.s1_fit on the pack: the share of trial-end candidates charged and the monthly continuation of a
    subscription nobody opens, fitted to the stores' excess over the records period by period, with every charge on
    its store's own day"""
    if not isinstance(O, PackObs):
        return _core_fit(O, split=split, trim=trim, form=form, cadence=cadence)
    ren, fst = C.s1_candidates(O)
    S = O.store
    cnt = lambda b: np.bincount(b, minlength=NM)[:NM].astype(float)
    fits = {}
    for g in (((0,), (1,)) if split == "store" else ((0, 1),)):
        mk = np.isin(O.ios.astype(int), g) & ~O.web
        ii, kk = np.nonzero(O.rec & mk[:, None])
        b = O.mon[ii, kk]
        F = sum(S[pl]["first"] for pl in g) - cnt(b[kk == 0])
        R = sum(S[pl]["ren"] for pl in g) - cnt(b[kk > 0])
        ia = np.where(mk & O.rec_a0)[0]
        A = sum(S[pl]["ann"] for pl in g) - cnt(O.bin(O.conv_day[ia], ia))
        fm = fst & mk & (O.plan_seen == 1)
        fa = fst & mk & (O.plan_seen == 2)
        c_m = F.sum() / max(1, fm.sum())
        c_a = A.sum() / max(1, fa.sum())
        idx = np.where(ren & mk)[0]
        last = O.rdays[idx, O.n_rec[idx] - 1]
        fi = np.where(fm)[0]
        te = O.day[fi] + 7
        Mr = np.zeros((K, NM)); Mf = np.zeros((K, NM))
        for j in range(1, K):
            d = last + np.round(cadence * j).astype(int)
            ok = d <= END_DAY
            Mr[j - 1] = cnt(O.bin(d[ok], idx[ok]))
            d2 = te + np.round(cadence * j).astype(int)
            ok = d2 <= END_DAY
            Mf[j - 1] = cnt(O.bin(d2[ok], fi[ok]))
        use = np.arange(NM) < NM - 1 - trim
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
            q = C.refine(lambda x: float((((x ** pw) @ Mr + c_m * ((x ** pw) @ Mf) - R)[use] ** 2).sum()), best[1], 0.002)
            best = (None, q, q)
        wq = best[1] ** np.arange(1, K + 1) if form != "two" else best[2] * best[1] ** np.arange(0, K)
        for pl in g:
            fits[pl] = dict(c_m=float(c_m), c_a=float(c_a), q=float(best[1]), q1=float(best[2]), F=F, R=R, A=A,
                            first_candidates=int(fm.sum()), annual_candidates=int(fa.sum()),
                            renew_candidates=int(idx.size), fitted=wq @ Mr + c_m * (wq @ Mf), use=use,
                            Mr=Mr, Mf=Mf)
    return fits


def values(O, s1="golden", **kw):
    """core.values on the pack (a mess item left unhandled may add its double count)"""
    v = _core_values(O, s1, **kw)
    if isinstance(O, PackObs) and O.extra is not None:
        k = ("extra", id(v))
        if k not in C._CACHE:
            C._CACHE[k] = v + O.extra
        return C._CACHE[k]
    return v


C.s1_fit = s1_fit
C.values = values

# the conventions only the files carry (the design note's SF27 to SF31)
PACK_VARIANTS = [
    ("the stores and the records compared by calendar month", dict(bins="calendar")),
    ("the App Store's report days taken as UTC days", dict(pt=False)),
    ("the stores' refunds netted on the day of the refund", dict(refunds="refund_day")),
    ("the stores' refunds netted from their renewals", dict(refunds="renewals")),
    ("the install week and the 365 days counted from the attribution export's install time", dict(clock="install")),
    ("a week's month taken from its Monday", dict(month="mon")),
]
VIEW_KEYS = ("align", "bins", "pt", "refunds", "clock")
THU = (C.WMONTH.copy(), np.array(C.PLAN_MONTH).copy())             # a week's month by its Thursday
MON = (np.array([int(C.month_of_day(7 * w)) for w in range(C.WEEKS)]),
       np.array([int(C.month_of_day(791 + 7 * t)) for t in range(52)]))


def use_plan(O):
    """core's estimators read the plan through core.plan_spend: hand them the media plan workbook's own columns"""
    C.plan_spend = lambda c: O.plan[c] if c in O.plan else O.brand[c]


def route(O, s1="golden", s2="golden", s3="golden", **kw):
    """core.route under a variant's conventions: the ones that are readings of the files go to a view of the
    observations, the month a week belongs to is swapped in core for the length of the call, the rest are core's"""
    kw = dict(kw)
    conv = {k: kw.pop(k) for k in VIEW_KEYS if k in kw}
    V = O.view(**conv) if conv else O
    if kw.get("month") == "mon":
        keep = C.WMONTH, C.PLAN_MONTH
        C.WMONTH, C.PLAN_MONTH = MON
        try:
            return C.route(V, s1, s2, s3, **kw)
        finally:
            C.WMONTH, C.PLAN_MONTH = keep
    return C.route(V, s1, s2, s3, **kw)


def lattice_route(O, lost, **kw):
    k = dict(kw)
    for s in lost:
        k.update(C.HURRIED[s])
    return route(O, **k)


def plan_checks(O):
    """the plan, the stretch column and the budget moves the analysis reads are the workbooks' own"""
    out = []
    for c in C.MEMBERS:
        out.append(("plan " + c, bool(np.array_equal(O.plan[c], _PLAN0(c)))))
        out.append(("stretch " + c, bool(np.allclose(O.stretch[c] / O.plan[c], C.CH[c]["stretch"], rtol=0, atol=1e-9))))
    out.append(("brand", bool(np.array_equal(O.brand["Apple Search Ads"], _PLAN0("Apple Search Ads")))))
    for c in C.ORDER:
        out.append(("moves " + c, [(a, b, round(f, 2)) for a, b, f in O.pushes[c]] ==
                    [(a, b, round(f, 2)) for a, b, f in C.CH[c]["pushes"]]))
    return out


_PLAN0 = C.plan_spend


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


THING = {"dbar_weeks": "delivery share weeks", "dbar_from": "delivery share weeks"}
ORGANIC_SHARED = ("gpo", "po", "go")


def _grouped(kw):
    """the sources a convention puts on a shared ratio"""
    return {nm for g in C.groups_of(kw["group"]) for nm in g} if kw.get("group") else set()


def merged(ka, kb):
    """two conventions taken together; two groupings of different sources are both made"""
    both = dict(ka, **kb)
    if ka.get("group") and kb.get("group"):
        both["group"] = ka["group"] + "+" + kb["group"]
    return both


NO_LIGHTER_CELL = ("tier8", "sess8", "sess4", "tp4")     # groupings on which the lighter half of a split fit is empty


def together(ka, kb):
    """whether two conventions can be taken together. They cannot when they are two ways of one thing: the same
    setting (two groupings of sources that share a source among them, where two that share none are both made); the
    weeks the delivery share is taken over; the organic installs' ratio taken from Apple Search Ads and shared with
    a network; the ratios fitted apart for lighter and heavier use on a grouping of the first-48-hour values that
    leaves the lighter fit no cell (the eight cells, which put every trial starter in the heavier half; the sessions
    bucket alone and the flags alone, where every group that holds a trial or a purchase counts as heavier)"""
    same = {THING.get(k, k) for k in ka} & {THING.get(k, k) for k in kb}
    if same == {"group"} and not (_grouped(ka) & _grouped(kb)):
        same = set()
    if same:
        return False
    both = merged(ka, kb)
    if "org_pin" in both and set(both.get("group", "").split("+")) & set(ORGANIC_SHARED):
        return False
    if both.get("rows") == "market-week-tier" and both.get("cells") in NO_LIGHTER_CELL:
        return False
    return True


def battery(O, cross=True, verbose=False):
    """every defensible way of taking a step: core's variants and the conventions only the files carry, each
    alone; then every two of them that can be taken together; then one way of each of the three steps together.
    Returns [(name, route)] and how many of each."""
    singles = [(nm, dict(kw)) for nm, kw in C.VARIANTS + PACK_VARIANTS]
    fam = [(nm, route(O, **kw)) for nm, kw in singles]
    counts = dict(singles=len(fam), pairs=0, triples=0, apart=0)
    step = {}
    for nm, kw in singles:
        step.setdefault(step_of(kw), []).append((nm, kw))
    counts["by_step"] = {k: len(step[k]) for k in ("S1", "S2", "S3")}
    beside = [(nm, route(O, **kw)) for nm, kw in C.BESIDE]
    counts["beside"] = len(beside)
    if not cross:
        return fam + beside, counts
    for (na, ka), (nb, kb) in itertools.combinations(singles, 2):
        if together(ka, kb):
            fam.append((na + "; " + nb, route(O, **merged(ka, kb))))
        else:
            counts["apart"] += 1
    counts["pairs"] = len(fam) - counts["singles"]
    for (na, ka), (nb, kb), (nc, kc) in itertools.product(step["S1"], step["S2"], step["S3"]):
        fam.append(("; ".join((na, nb, nc)), route(O, **dict(ka, **kb, **kc))))
    counts["triples"] = len(fam) - counts["singles"] - counts["pairs"]
    return fam + beside, counts


def crossings(O):
    """every way that stands beside the battery, crossed with it: with each single way of the battery it can be taken
    with, and with one way of each of the other two steps at once. Returns [(name, route)]."""
    singles = [(nm, dict(kw)) for nm, kw in C.VARIANTS + PACK_VARIANTS]
    step = {}
    for nm, kw in singles:
        step.setdefault(step_of(kw), []).append((nm, kw))
    out = []
    for bn, bk in C.BESIDE:
        for nm, kw in singles:
            if together(bk, kw):
                out.append((bn + "; " + nm, route(O, **merged(bk, kw))))
        a, b = [s for s in ("S1", "S2", "S3") if s != step_of(bk)]
        for (na, ka), (nb, kb) in itertools.product(step[a], step[b]):
            if together(bk, ka) and together(bk, kb):
                out.append(("; ".join((bn, na, nb)), route(O, **dict(bk, **ka, **kb))))
    return out


S1_KEYS = {"split", "trim", "form", "cadence", "cshare", "bins", "pt", "refunds", "clock"}
S3_KEYS = {"months", "weeks_i", "weeks_v", "quality", "qpool", "dbar_weeks", "dbar_from", "s3", "month", "carry"}


def step_of(kw):
    """the step a variant's convention belongs to"""
    ks = set(kw)
    if ks <= S1_KEYS:
        return "S1"
    if ks <= S3_KEYS:
        return "S3"
    return "S2"


def run(target, cross=True, verbose=False):
    """every route the build needs, computed on the shipped files"""
    O = PackObs(target)
    use_plan(O)
    g = route(O)
    fam, counts = battery(O, cross)
    keys = [["S1"], ["S2"], ["S3"], ["S1", "S2"], ["S1", "S3"], ["S2", "S3"], ["S1", "S2", "S3"]]
    lat = {"+".join(k): lattice_route(O, k) for k in keys}
    direct = route(O, "raw", "direct", "average")
    rigorous = route(O, **C.RIGOROUS)
    v = C.values(O)
    refs = dict(S1=C.referee_s1(O), S2=C.referee_s2(O, v), S3=C.referee_s3(O, v))
    return dict(O=O, golden=g, family=fam, counts=counts, lattice=lat, direct=direct, rigorous=rigorous, v=v,
                refs=refs, fits=s1_fit(O), crossed=crossings(O) if cross else [])


if __name__ == "__main__":
    import time
    t0 = time.time()
    X = run(sys.argv[1], cross="--cross" in sys.argv)
    print("%.0fs" % (time.time() - t0))
    for c in C.ORDER:
        print("%-18s" % c, " ".join("%s %.4f" % (k, X["golden"][c][k]) for k in
                                    ("roas", "roas_s", "installs_week", "vpi", "marginal", "v12", "unrec")))
