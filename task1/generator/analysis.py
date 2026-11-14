"""Every graded figure, computed only from the shipped files in target/: the golden, its family of defensible
variants and the shortcut routes. Nothing here reads the simulator."""
import datetime as dt
import os

import numpy as np
import pandas as pd
from openpyxl import load_workbook

import docs
import pack
import params as P

CHAN = {("Meta Ads", "ios"): "Meta iOS", ("TikTok For Business", "ios"): "TikTok iOS",
        ("Apple Search Ads", "ios"): "Apple Search Ads", ("Meta Ads", "android"): "Meta Android",
        ("Google Ads", "android"): "Google Android", ("TikTok For Business", "android"): "TikTok Android",
        ("AppLovin", "android"): "AppLovin Android"}
NETS = {"meta": "Meta iOS", "tiktok": "TikTok iOS"}
L0 = pd.Timestamp(P.LAUNCH)
MD = P.MONTH_DAYS
OVERRIDE = {}
CENTRE = {}


def coarse_of(cv):
    cv = np.asarray(cv)
    trial, paid, bucket = (cv >> 3) & 1, (cv >> 4) & 1, cv & 7
    return np.where((paid == 1) | ((trial == 1) & (bucket >= 4)), "high", np.where(trial == 1, "medium", "low"))


class Pack:
    def __init__(self, target):
        f = lambda k: os.path.join(target, pack.FILES[k])
        acc = pd.read_csv(f("acc"), dtype=str, keep_default_na=False)
        acc = acc[acc.account_type == "consumer"].copy()
        acc["created"] = pd.to_datetime(acc.created_at).dt.tz_localize(None)
        acc["lo"] = pd.to_datetime(acc.last_open_at).dt.tz_localize(None)
        acc["day"] = (acc.created.dt.normalize() - L0).dt.days
        acc["cv"] = acc.first_48h_value.astype(int)
        acc["vat"] = acc.country.map(P.VAT)
        attr = pd.read_csv(f("attr"), dtype=str, keep_default_na=False).drop_duplicates("install_id")
        first = attr[attr.is_reinstall == "false"].sort_values("install_time").drop_duplicates("account_id")
        ch = first.set_index("account_id")[["media_source", "platform", "campaign_id"]]
        acc = acc.join(ch, on="account_id", rsuffix="_a")
        acc["channel"] = [CHAN.get((m, p), "organic") for m, p in zip(acc.media_source, acc.platform)]
        self.acc = acc.set_index("account_id")
        bill = pd.read_csv(f("bill"), dtype=str, keep_default_na=False)
        bill = bill[(bill.environment == "production") & bill.account_id.isin(self.acc.index)].copy()
        bill["t"] = pd.to_datetime(bill.transaction_at).dt.tz_localize(None)
        bill["price"] = bill.price_eur.astype(float)
        bill["net"] = bill.price / (1 + bill.storefront.map(P.VAT)) * (1 - P.COMMISSION)
        self.bill = bill
        self.skan = pd.read_csv(f("skan"), dtype=str, keep_default_na=False)
        self.apple = pd.read_csv(f("apple"), dtype=str, keep_default_na=False)
        self.google = pd.read_csv(f("google"), dtype=str, keep_default_na=False)
        sp = pd.read_csv(f("spend"), dtype=str, keep_default_na=False)
        sp["spend"] = sp.spend_eur.astype(float)
        sp["d"] = (pd.to_datetime(sp.date) - L0).dt.days
        self.spend = sp
        wb = load_workbook(os.path.join(target, docs.FILES["plan"]), data_only=True)
        ws = wb["Weekly spend 2027"]
        hdr = [c.value for c in ws[1]]
        rows = [r for r in ws.iter_rows(min_row=2, values_only=True) if isinstance(r[1], int)]
        self.plan = pd.DataFrame(rows, columns=hdr)
        self._prep()

    def _prep(self):
        a, b = self.acc, self.bill
        win_end = a.created + pd.Timedelta(days=365)
        bj = b.join(win_end.rename("wend"), on="account_id").join(a.created.rename("cr"), on="account_id")
        inwin = (bj.t >= bj.cr.dt.normalize()) & (bj.t < bj.wend.dt.normalize())
        self.rec12 = bj[inwin].groupby("account_id").net.sum().reindex(a.index, fill_value=0.0)
        m = b[b.product_id == P.PRODUCT["monthly"]]
        ch = m[m.event_type != "refund"].sort_values("t")
        g = ch.groupby("account_id")
        self.first_t = g.t.first()
        self.n_rec = g.t.count()
        self.last_t = g.t.last()
        self.any_charge = b[b.event_type != "refund"].account_id.unique()


def store_gap(pk):
    """the stores' units against the app's synced events, by store, product, kind and month (UTC month)"""
    ap = pk.apple.copy()
    ap["units"] = ap.units.astype(int)
    ap["m"] = pd.to_datetime(ap.date_pacific).dt.to_period("M")
    ap["kind"] = ap.event.map({"Paid Subscription from Free Trial": "first", "Subscribe": "first", "Renew": "renewal",
                               "Refund": "refund"})
    go = pk.google.copy()
    go["units"] = go.transactions.astype(int)
    go["m"] = pd.to_datetime(go.date_utc).dt.to_period("M")
    go["kind"] = go.transaction_type.map({"charge_new": "first", "charge_renewal": "renewal", "refund": "refund"})
    st = pd.concat([ap.assign(store="app_store"), go.assign(store="google_play")])
    st = st.groupby(["store", "product_id", "kind", "m"]).units.sum()
    b = pk.bill.copy()
    b["kind"] = b.event_type.map({"first_charge": "first", "renewal": "renewal", "refund": "refund"})
    # the app's UTC times against Apple's Pacific days
    off = np.where(b.t.dt.month.between(3, 10), 7, 8)
    tl = np.where(b.store == "app_store", b.t - pd.to_timedelta(off, unit="h"), b.t)
    b["m"] = pd.DatetimeIndex(tl).to_period("M")
    rc = b.groupby(["store", "product_id", "kind", "m"]).size()
    return st, rc


def cadence(start, k):
    """the k-th monthly charge after `start`: thirty-and-a-bit days, or the same day of each calendar month"""
    if OVERRIDE.get("calendar"):
        return pd.DatetimeIndex(start) + pd.DateOffset(months=int(k)) if np.ndim(k) == 0 else \
            pd.DatetimeIndex([t + pd.DateOffset(months=int(kk)) for t, kk in zip(start, k)])
    return pd.DatetimeIndex(start) + pd.to_timedelta(np.round(MD * np.asarray(k)), unit="D")


def candidates(pk):
    """accounts whose last open came before a charge their subscription was still set to take"""
    a = pk.acc
    yes = a.auto_renew_at_last_open == "yes"
    mon = a.plan_at_last_open == "monthly"
    has = a.index.isin(pk.first_t.index)
    # renewal candidates: a recorded monthly charge, still set to renew at the last open, no open after the next charge
    idx = a.index[yes & mon & has]
    ft = pk.first_t.reindex(idx); nrec = pk.n_rec.reindex(idx)
    nxt = pd.Series(cadence(ft, nrec.values), index=idx)
    ren = idx[(a.lo.reindex(idx) < nxt).values]
    # first-charge candidates: still in the free trial at the last open, set to renew, nothing charged on file
    nochg = ~a.index.isin(pk.any_charge)
    fst = a.index[yes & nochg & (a.lo < a.created + pd.Timedelta(days=7)) & a.plan_at_last_open.isin(["monthly", "annual"])]
    return ren, fst


def gap_fit(pk, by_store=False, form="geometric"):
    """the share of trial-end candidates charged and the monthly continuation of a silent subscription, fitted to the
    stores' excess over the app's records"""
    st, rc = store_gap(pk)
    ren, fst = candidates(pk)
    a = pk.acc
    months = pd.period_range("2024-11", "2026-11", freq="M")
    mi = {m: i for i, m in enumerate(months)}
    plat = a.platform
    out = {}
    stores = (("app_store", "ios"), ("google_play", "android")) if by_store else ((None, None),)
    for stn, pl in stores:
        def sel(ix):
            return ix if pl is None else ix[(plat.reindex(ix) == pl).values]
        r_ix, f_ix = sel(ren), sel(fst)
        def series(kind, prod):
            keys = ("app_store", "google_play") if stn is None else (stn,)
            g = np.zeros(len(months))
            for s in keys:
                for m, v in st.get((s, prod, kind), pd.Series(dtype=int)).items():
                    if m in mi: g[mi[m]] += v
                for m, v in rc.get((s, prod, kind), pd.Series(dtype=int)).items():
                    if m in mi: g[mi[m]] -= v
            return g
        F_m = series("first", P.PRODUCT["monthly"]); F_a = series("first", P.PRODUCT["annual"])
        R_m = series("renewal", P.PRODUCT["monthly"])
        fm = f_ix[(a.plan_at_last_open.reindex(f_ix) == "monthly").values]
        fa = f_ix[(a.plan_at_last_open.reindex(f_ix) == "annual").values]
        trial_end = lambda ix: a.created.reindex(ix).dt.normalize() + pd.Timedelta(days=7)
        cnt = lambda dates: np.bincount([mi[p] for p in pd.DatetimeIndex(dates).to_period("M") if p in mi], minlength=len(months))
        c_m = F_m.sum() / max(1, len(fm)); c_a = F_a.sum() / max(1, len(fa))
        K = 24
        # renewal dates after each candidate's last recorded charge, and after a silent first charge
        ft = pk.first_t.reindex(r_ix); nrec = pk.n_rec.reindex(r_ix).values
        Mr = np.zeros((K, len(months))); Mf = np.zeros((K, len(months)))
        for k in range(1, K + 1):
            Mr[k - 1] = cnt(cadence(ft, nrec - 1 + k))
            Mf[k - 1] = cnt(cadence(trial_end(fm), np.full(len(fm), k)))
        last = mi[pd.Period(P.DATA_END, "M")]
        use = np.arange(len(months)) < last - (2 if OVERRIDE.get("trim") else 0)          # whole months only
        best = None
        q1s = np.linspace(0.40, 0.99, 60) if form == "two" else [None]
        for q in np.linspace(0.50, 0.99, 491):
            for q1 in q1s:
                w = (q ** np.arange(1, K + 1)) if q1 is None else (q1 * q ** np.arange(0, K))
                pred = w @ Mr + c_m * (w @ Mf)
                err = ((pred - R_m)[use] ** 2).sum()
                if best is None or err < best[0]:
                    best = (err, q, q1 if q1 is not None else q)
        q, q1 = best[1], best[2]
        if "q_shift" in OVERRIDE:
            q, q1 = q + OVERRIDE["q_shift"], q1 + OVERRIDE["q_shift"]
        c_m *= OVERRIDE.get("c_scale", 1.0); c_a *= OVERRIDE.get("c_scale", 1.0)
        out[pl or "all"] = dict(c_m=c_m, c_a=c_a, q=q, q1=q1, n_ren=len(r_ix), n_fst=len(f_ix))
    return out


def a_values(pk, how="golden"):
    """each account's 12-month net revenue: as recorded, scaled in proportion, or with the silent charges added"""
    a = pk.acc
    rec = pk.rec12
    if how == "recorded":
        return rec
    if how == "prop":
        out = rec.copy()
        st, rc = store_gap(pk)
        for s, pl in (("app_store", "ios"), ("google_play", "android")):
            src = pk.apple if s == "app_store" else pk.google
            col = "developer_proceeds_eur" if s == "app_store" else "net_eur"
            store_net = src[col].astype(float).sum()
            app_net = pk.bill[pk.bill.store == s].net.sum()
            mk = (a.platform == pl).values
            out[mk] = rec[mk] * store_net / app_net
        return out
    fits = gap_fit(pk, by_store=(how == "by_store"), form=("two" if how == "two" else "geometric"))
    ren, fst = candidates(pk)
    add = pd.Series(0.0, index=a.index)
    net_m = P.PRICE["monthly"] / (1 + a.vat) * (1 - P.COMMISSION)
    net_a = P.PRICE["annual"] / (1 + a.vat) * (1 - P.COMMISSION)
    wend = a.created.dt.normalize() + pd.Timedelta(days=365)
    K = 24
    for ix, kind in ((ren, "ren"), (fst, "fst")):
        for pl in ("ios", "android"):
            f = fits.get(pl) or fits["all"]
            sub = ix[(a.platform.reindex(ix) == pl).values]
            if kind == "ren":
                ft = pk.first_t.reindex(sub); nrec = pk.n_rec.reindex(sub).values
                base = lambda k: cadence(ft, nrec - 1 + k)
                p0 = np.ones(len(sub))
            else:
                mon = (a.plan_at_last_open.reindex(sub) == "monthly").values
                te = a.created.reindex(sub).dt.normalize() + pd.Timedelta(days=7)
                inw = (te < wend.reindex(sub)).values
                add.loc[sub[~mon & inw]] += f["c_a"] * net_a.reindex(sub[~mon & inw]).values
                add.loc[sub[mon & inw]] += f["c_m"] * net_m.reindex(sub[mon & inw]).values
                sub = sub[mon]
                te = te[mon]
                base = lambda k: cadence(te, np.full(len(te), k))
                p0 = np.full(len(sub), f["c_m"])
            we = wend.reindex(sub).values
            nm = net_m.reindex(sub).values
            for k in range(1, K + 1):
                dk = np.asarray(base(k))
                w = (f["q1"] * f["q"] ** (k - 1)) if how == "two" else f["q"] ** k
                add.loc[sub] += p0 * w * nm * (dk < we)
    return rec + add


def skan_mature(pk):
    s = pk.skan
    pdte = pd.to_datetime(s.postback_date)
    inst = (pdte - pd.Timedelta(days=3) - L0).dt.days            # the install a postback answers, about three days earlier
    return s[(inst >= 0) & (inst < 7 * P.MATURE_WEEKS)].assign(inst=inst)


def ios_value(pk, v, net, how="golden"):
    """a network's 12-month net revenue per install over all its installs"""
    a = pk.acc
    ios = a[(a.platform == "ios") & (a.channel != "Apple Search Ads") & (a.day >= 0) & (a.day < 7 * P.MATURE_WEEKS)]
    vv = v.reindex(ios.index)
    auth = (ios.att_status == "authorized").values
    mine = (ios.channel == NETS[net]).values
    if how == "consenters":
        return vv[mine].mean()
    s = skan_mature(pk)
    s = s[s.ad_network == net]
    fine = s.conversion_value[s.conversion_value != ""].astype(int).values
    coarse = s.coarse_conversion_value[(s.conversion_value == "") & (s.coarse_conversion_value != "")].values
    nnull = int(((s.conversion_value == "") & (s.coarse_conversion_value == "")).sum())
    cvs = ios.cv.values
    co = coarse_of(cvs)
    def cell(keymask, keymine):
        """value of the network's installs in one cell: its consenting users, and every non-consenting iOS user"""
        n_cons = (keymine & auth).sum()
        allc = keymask & auth
        vc = vv[keymine & auth].mean() if n_cons >= 20 else (vv[allc].mean() if allc.sum() else vv[keymask].mean())
        if how == "netpool" and allc.sum():
            vc = vv[allc].mean()
        den = keymask & ~auth
        vn = (vv[den].mean() if den.sum() >= 20 else vv[keymask].mean()) * OVERRIDE.get("vn_scale", 1.0)
        if how == "ratio" and allc.sum() >= 20 and den.sum() >= 20 and vv[allc].mean() > 0:
            vn = vc * vv[den].mean() / vv[allc].mean()
        return n_cons, vc, vn, vv[keymask].mean() if keymask.sum() else 0.0
    tot = 0.0; n = 0
    uc, cc = np.unique(fine, return_counts=True)
    for k, cnt in zip(uc, cc):
        if how == "coarse":
            continue
        m = cvs == k
        n_cons, vc, vn, vall = cell(m, m & mine)
        if how == "pooled":
            tot += cnt * vall; n += cnt; continue
        pi = min(1.0, n_cons / cnt)
        tot += cnt * (pi * vc + (1 - pi) * vn); n += cnt
    groups = list(zip(*np.unique(coarse, return_counts=True))) if how != "coarse" else \
        list(zip(*np.unique(np.concatenate([coarse_of(fine), coarse]), return_counts=True)))
    for g, cnt in groups:
        m = co == g
        n_cons, vc, vn, vall = cell(m, m & mine)
        if how == "pooled":
            tot += cnt * vall; n += cnt; continue
        # consenting users of the network in this coarse group are spread over fine and coarse postbacks alike
        share = cnt / ((coarse_of(fine) == g).sum() + cnt) if how != "coarse" else 1.0
        pi = min(1.0, n_cons * share / cnt) if cnt else 0.0
        tot += cnt * (pi * vc + (1 - pi) * vn); n += cnt
    per = tot / n
    return per


def weekly(pk, v):
    """each channel's weekly spend, installs and (for the twelve-month weeks) value per install"""
    a = pk.acc
    sp = pk.spend.groupby(["channel", pk.spend.d // 7]).spend.sum()
    s = pk.skan
    inst_ios = (pd.to_datetime(s.postback_date) - pd.Timedelta(days=3) - L0).dt.days // 7
    out = {}
    for c in P.ORDER:
        w = np.arange(P.WEEKS)
        spend = np.array([sp.get((c, k), np.nan) for k in w])
        NW = P.WEEKS + (1 if OVERRIDE.get("lastweek") else 0)
        w = np.arange(NW)
        spend = np.array([sp.get((c, k), np.nan) for k in w])
        if c in NETS.values():
            net = [k for k, x in NETS.items() if x == c][0]
            wi = inst_ios[s.ad_network == net]
            inst = np.bincount(wi[(wi >= 0) & (wi < P.WEEKS)], minlength=P.WEEKS)[:P.WEEKS].astype(float)
            if NW > P.WEEKS:
                inst = np.append(inst, np.nan)         # the pull week's postbacks have not all arrived
            sub = a[a.channel == c]
        else:
            sub = a[a.channel == c]
            wk_ = sub.day // 7
            inst = np.bincount(wk_[(wk_ >= 0) & (wk_ < NW)], minlength=NW)[:NW].astype(float)
        vw = sub.groupby(sub.day // 7).apply(lambda g: v.reindex(g.index).mean()).reindex(w).values
        out[c] = dict(spend=spend, inst=inst, vpi=vw)
    return out


def month_of_week(k):
    return (P.LAUNCH + dt.timedelta(days=7 * int(k) + 3)).month


def response(pk, wk, how="pooled"):
    """installs and value per install against weekly spend: each channel's own slope, the month pattern pooled across
    channels (or each channel's own, or none)"""
    rows_i, rows_v = [], []
    for ci, c in enumerate(P.ORDER):
        d = wk[c]
        mu = CENTRE[c] = np.nanmean(np.log(d["spend"][:P.WEEKS][d["spend"][:P.WEEKS] > 0]))
        for k in range(len(d["inst"])):
            if d["inst"][k] > 0 and d["spend"][k] > 0 and (how != "mature" or k < P.MATURE_WEEKS):
                rows_i.append((ci, k, np.log(d["spend"][k]) - mu, np.log(d["inst"][k])))
            if k < P.MATURE_WEEKS and d["vpi"][k] > 0 and d["spend"][k] > 0:
                rows_v.append((ci, k, np.log(d["spend"][k]) - mu, np.log(d["vpi"][k])))
    def fit(rows):
        C = len(P.ORDER)
        X, y = [], []
        for ci, k, ls, ly in rows:
            x = np.zeros(3 * C + 11)
            x[ci] = 1; x[C + ci] = ls
            if how == "quad":
                x[2 * C + 11 + ci] = ls * ls
            mo = month_of_week(k)
            if how != "none" and mo > 1:
                x[2 * C + mo - 2] = 1
            X.append(x); y.append(ly)
        X = np.array(X); y = np.array(y)
        if how == "none":
            X = X[:, :2 * C]
        if how != "quad":
            X = X[:, :2 * C + 11] if how != "none" else X
        b = np.linalg.lstsq(X, y, rcond=None)[0]
        if how != "quad" and how != "none":
            b = np.concatenate([b, np.zeros(C)])
        return b
    if how == "own":
        out = {}
        for ci, c in enumerate(P.ORDER):
            for nm, rows in (("i", rows_i), ("v", rows_v)):
                rr = [r for r in rows if r[0] == ci]
                X = np.array([[1, r[2]] + [1.0 if month_of_week(r[1]) == mo else 0.0 for mo in range(2, 13)] for r in rr])
                y = np.array([r[3] for r in rr])
                keep = X.any(0); keep[0] = keep[1] = True
                b = np.linalg.lstsq(X[:, keep], y, rcond=None)[0]
                full = np.zeros(13); full[keep] = b
                full[1] *= OVERRIDE.get("v_slope" if nm == "v" else "i_slope", 1.0)
                out[(c, nm)] = full
        return out
    bi, bv = fit(rows_i), fit(rows_v)
    C = len(P.ORDER)
    bv[C:2 * C] = bv[C:2 * C] * OVERRIDE.get("v_slope", 1.0)
    bi[C:2 * C] = bi[C:2 * C] * OVERRIDE.get("i_slope", 1.0)
    return {"i": bi, "v": bv}


def at_plan(pk, wk, coef, c, vpi_level=None, how="pooled"):
    """installs a week and value per install at the plan's 2027 weekly spend, and the return per euro"""
    C = len(P.ORDER); ci = P.ORDER.index(c)
    plan = pk.plan
    ni = vi = tot_v = tot_s = 0.0
    mature = [k for k in range(P.MATURE_WEEKS) if wk[c]["spend"][k] > 0]
    def pred(b, ls, mo, own=False):
        if own:
            return b[0] + b[1] * ls + (b[mo] if mo > 1 else 0.0)
        g = (b[2 * C + mo - 2] if (mo > 1 and len(b) > 2 * C) else 0.0)
        qd = b[2 * C + 11 + ci] * ls * ls if len(b) > 2 * C + 11 else 0.0
        return b[ci] + b[C + ci] * ls + g + qd
    own = how == "own"
    bi = coef[(c, "i")] if own else coef["i"]
    bv = coef[(c, "v")] if own else coef["v"]
    # the value level: the channel's own twelve-month weeks, or a level from elsewhere (the iOS networks)
    mu = CENTRE[c]
    fitted_mature = np.array([np.exp(pred(bv, np.log(wk[c]["spend"][k]) - mu, month_of_week(k), own)) for k in mature])
    inst_m = np.array([wk[c]["inst"][k] for k in mature])
    scale = 1.0
    if vpi_level is not None:
        scale = vpi_level / ((fitted_mature * inst_m).sum() / inst_m.sum())
    n_tot = 0.0
    for _, r in plan.iterrows():
        mon = r["Week starting"]
        mo = (mon + dt.timedelta(days=3)).month
        s = float(r[c])
        n = np.exp(pred(bi, np.log(s) - mu, mo, own))
        vp = np.exp(pred(bv, np.log(s) - mu, mo, own)) * scale
        tot_v += n * vp; tot_s += s; n_tot += n
    return dict(installs_week=n_tot / len(plan), vpi=tot_v / n_tot, roas=tot_v / tot_s)


def mature_installs(pk):
    a = pk.acc
    s = skan_mature(pk)
    out = {}
    for c in P.ORDER:
        if c in NETS.values():
            net = [k for k, x in NETS.items() if x == c][0]
            out[c] = int((s.ad_network == net).sum())
        else:
            out[c] = int(((a.channel == c) & (a.day >= 0) & (a.day < 7 * P.MATURE_WEEKS)).sum())
    return out


def route(pk, A="golden", C="golden", B="pooled", cache=None):
    """every channel's figures under one route"""
    cache = cache if cache is not None else {}
    if ("A", A) not in cache:
        cache[("A", A)] = a_values(pk, A)
    v = cache[("A", A)]
    a = pk.acc
    mat = (a.day >= 0) & (a.day < 7 * P.MATURE_WEEKS)
    v12 = {}
    for c in P.ORDER:
        if c in NETS.values():
            net = [k for k, x in NETS.items() if x == c][0]
            v12[c] = ios_value(pk, v, net, C)
        else:
            v12[c] = v.reindex(a.index[mat & (a.channel == c)]).mean()
    key = ("W", A)
    if key not in cache:
        cache[key] = weekly(pk, v)
    wk = cache[key]
    sp_mature = {c: np.nansum(wk[c]["spend"][:P.MATURE_WEEKS]) for c in P.ORDER}
    inst = mature_installs(pk)
    res = {}
    if B == "average":
        for c in P.ORDER:
            res[c] = dict(v12=v12[c], installs=inst[c], roas=v12[c] * inst[c] / sp_mature[c],
                          installs_week=None, vpi=v12[c])
        return res
    ck = ("R", A, B)
    if ck not in cache:
        cache[ck] = response(pk, wk, B)
    coef = cache[ck]
    for c in P.ORDER:
        r = at_plan(pk, wk, coef, c, vpi_level=v12[c], how=B)
        res[c] = dict(v12=v12[c], installs=inst[c], **r)
    return res


A_FAMILY = ("golden", "by_store", "two")
C_FAMILY = ("golden", "pooled", "ratio", "coarse", "netpool")
B_FAMILY = ("pooled", "own", "none", "mature", "quad")
A_SWITCHES = (("A=calendar", {"calendar": True}), ("A=trim", {"trim": True}), ("B=lastweek", {"lastweek": True}))


def family(pk, cache):
    """every defensible variant of each stump's correction, the others held at the golden"""
    out = {c: [] for c in P.ORDER}
    for A in A_FAMILY:
        r = route(pk, A, "golden", "pooled", cache)
        for c in P.ORDER: out[c].append(("A=" + A, r[c]))
    for C in C_FAMILY[1:]:
        r = route(pk, "golden", C, "pooled", cache)
        for c in P.ORDER: out[c].append(("C=" + C, r[c]))
    for B in B_FAMILY[1:]:
        r = route(pk, "golden", "golden", B, cache)
        for c in P.ORDER: out[c].append(("B=" + B, r[c]))
    for nm, ov in A_SWITCHES:
        OVERRIDE.clear(); OVERRIDE.update(ov)
        r = route(pk, cache={})
        OVERRIDE.clear()
        for c in P.ORDER: out[c].append((nm, r[c]))
    return out
