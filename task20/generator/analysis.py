"""task20 architecture 2 analysis: Brindle & Moss's fourth-quarter fiscal 2025 net sales nowcast, computed from the
shipped files in target/ alone, with the rivals that set each band and the hurried routes effort.json prices.

One route function carries every method: the panel's normalisation (cards of the same age, per card, raw spend), the
regional weights (the company's prior-year net sales by region, or the panel's own spend), the bank-card share's change
(carried by a rule for the private-label card's share, or left out), and the calibration (the chain as built, or a
regression of reported growth on it over past quarters). The golden is the same-age chain at the company's regional mix
with the bank-card share carried at the pace of fiscal 2025's first three quarters, as built."""
import os
import re
import subprocess

import numpy as np
import pandas as pd

import docs as DC
import pack as PK

REGIONS = ["Northeast", "Southeast", "Midwest", "West"]
OTHER_TENDER = 0.12           # the 10-K's cash, checks, financing and other tenders' share of net sales
Z80 = 1.2816                  # the two-sided 80 per cent normal quantile
ACQUIRED = pd.Timestamp("2024-06-02")
TQ, BQ = "FY2025 Q4", "FY2024 Q4"


# ---------------------------------------------------------------------------------------------------------- the files
def load(tgt):
    _TOKENS[0] = 0
    _PROFILE.clear()
    _LEAD.clear()
    _MTO.clear()
    P = {}
    res = pd.read_csv(os.path.join(tgt, PK.F_RESULTS))
    res["period_start"] = pd.to_datetime(res.period_start)
    res["period_end"] = pd.to_datetime(res.period_end)
    P["results"] = res
    P["regions"], P["pl"], P["deposits"] = filing_tables(os.path.join(tgt, DC.F_FILING))
    pan = pd.read_csv(os.path.join(tgt, PK.F_PANEL))
    pan["week_start"] = pd.to_datetime(pan.week_start)
    P["panel"] = pan
    hist = pd.read_csv(os.path.join(tgt, PK.F_HIST))
    hist["delivery_date"] = pd.to_datetime(hist.delivery_date)
    hist["week_start"] = pd.to_datetime(hist.week_start)
    P["hist"] = hist
    P["desc"] = pd.read_csv(os.path.join(tgt, PK.F_DESC))
    P["street"] = pd.read_csv(os.path.join(tgt, PK.F_STREET))
    P["keys"] = list(res.fiscal_quarter)
    P["qyear"] = {r.fiscal_quarter: r.period_start.year for r in res.itertuples()}
    return P


def filing_tables(path):
    """the regional net sales table and the private-label card's share of net sales by quarter, from the excerpts"""
    txt = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True).stdout
    num = lambda s: float(s.replace(",", ""))
    block = txt.split("Net sales by region")[1].split("Acquisition")[0]
    years = [int(y) for y in re.findall(r"Fiscal (\d{4})", block)]
    rows = {}
    for r in REGIONS:
        m = re.search(r"^\s*%s\s+([\d,\.\s]+)$" % r, block, re.M)
        rows[r] = [num(x) for x in m.group(1).split()]
    reg = pd.DataFrame({"fiscal_year": ["FY%d" % y for y in years[:len(rows[REGIONS[0]])]]})
    for r in REGIONS:
        reg[r] = rows[r][:len(reg)]
    pl, dep = {}, {}
    for fy, q, v, d in re.findall(r"Fiscal (\d{4}) Q(\d)\s+(\d+\.\d)\s+([\d,]+\.\d)", txt):
        pl["FY%s Q%s" % (fy, q)] = float(v)
        dep["FY%s Q%s" % (fy, q)] = num(d)
    m = re.search(r"Customer deposits were USD ([\d,]+\.\d) million at the end of fiscal (\d{4})", re.sub(r"\s+", " ", txt))
    dep["FY%s Q4" % m.group(2)] = num(m.group(1))
    return reg, pl, dep


def quarter_of(P, weeks):
    out = pd.Series(index=weeks.index, dtype=object)
    for r in P["results"].itertuples():
        out[(weeks >= r.period_start) & (weeks <= r.period_end)] = r.fiscal_quarter
    return out


# ------------------------------------------------------------------------------------------- R2: the immature weeks
def completion_factors(P, stat="median", last_n=None):
    """each issuer's first-delivered share of a week's final spend at lags 0, 1 and 2: the week as first delivered
    against the same week three or more weeks later, over the delivery history"""
    h = P["hist"]
    dels = sorted(h.delivery_date.unique())
    if last_n:
        dels = dels[-last_n - 3:]
    f = {}
    for d in dels:
        g0 = h[h.delivery_date == d]
        for iss, g in g0.groupby("issuer_code"):
            for wk in g.week_start:
                lag = (pd.Timestamp(d) - wk).days // 7 - 1          # lag 0: the week ended two days before delivery
                if lag not in (0, 1, 2):
                    continue
                later = h[(h.issuer_code == iss) & (h.week_start == wk) & (h.delivery_date >= d + pd.Timedelta(days=21))]
                if later.empty:
                    continue
                fin = later.sort_values("delivery_date").spend_usd.iloc[-1]
                f.setdefault((iss, lag), []).append(float(g[g.week_start == wk].spend_usd.iloc[0]) / fin)
    agg = np.median if stat == "median" else np.mean
    return {k: float(agg(v)) for k, v in f.items()}


# ------------------------------------------------------------------------------------- R1: the reporting entity
def excluded_share(P):
    """the licensed shop-in-shops' and cafes' share of the brand merchant id's spend, by month"""
    b = P["desc"][P["desc"].merchant_id == "M0412"].copy()
    b["out"] = b.descriptor.str.contains("HOLLISTERS|CAFE", regex=True)
    tot = b.groupby("month").spend_usd.sum()
    return b[b.out].groupby("month").spend_usd.sum().reindex(tot.index).fillna(0) / tot


_TOKENS = [0]


def _token(pan):
    """a stable identity for a panel frame within a run (object ids are reused once a frame is freed)"""
    if "tok" not in pan.attrs:
        _TOKENS[0] += 1
        pan.attrs["tok"] = _TOKENS[0]
    return pan.attrs["tok"]


def panel_entity(P, cf, complete=True, exclude=True, share_scale=1.0):
    """the reporting entity's panel spend: the brand id less the licensed shops and cafes, the site, and Fernhollow
    from its acquisition; the latest weeks completed by each issuer's completion factors"""
    pan = P["panel"].copy()
    if exclude:
        sh = excluded_share(P) * share_scale
        mon = pan.week_start.dt.to_period("M").astype(str)
        keep = np.where(pan.merchant_id == "M0412", 1 - mon.map(sh).fillna(0).values, 1.0)
        pan["spend_usd"] = pan.spend_usd * keep
    pan = pan[(pan.merchant_id != "M2290") | (pan.week_start >= ACQUIRED)].copy()
    if complete and cf:
        last = pan.week_start.max()
        lag = ((last - pan.week_start).dt.days // 7).clip(upper=3)
        fac = np.array([cf.get((i, l), 1.0) if l < 3 else 1.0 for i, l in zip(pan.issuer_code, lag)])
        pan["spend_usd"] = pan.spend_usd / fac
    pan["fq"] = quarter_of(P, pan.week_start).values
    pan.loc[pan.week_start > P["results"].period_end.iloc[-2], "fq"] = TQ
    return pan


# ------------------------------------------------------------------------------ R3 and R4: growth on the panel
def regional(P, pan, q, b, how, fern_ok=True):
    """year-on-year growth of quarter q over quarter b (weekly averages) by billing region, and the base quarter's
    panel spend by region. how: tenure (issuers in both quarters; each open year against the open year one later, on
    the base quarter's cards), per_card (issuers in both, spend per open card), const_raw (issuers in both, spend),
    all_issuers (every issuer, spend)"""
    sub = pan[pan.fq.isin([q, b])]
    if not fern_ok:
        sub = sub[sub.merchant_id != "M2290"]
    weeks = sub.groupby("fq").week_start.nunique()
    n = {q: weeks.get(q, 13), b: weeks.get(b, 13)}
    cov = sub.groupby(["issuer_code", "fq"]).week_start.nunique().unstack()
    const = [i for i in cov.index if cov.loc[i].get(q, 0) == n[q] and cov.loc[i].get(b, 0) == n[b]]
    sc = sub if how == "all_issuers" else sub[sub.issuer_code.isin(const)]
    s = sc.groupby(["fq", "billing_region"]).spend_usd.sum()
    pw = {r: float(s[b][r]) for r in REGIONS}
    if how in ("const_raw", "all_issuers"):
        return {r: (s[q][r] / n[q]) / (s[b][r] / n[b]) - 1 for r in REGIONS}, pw
    cards = sc.drop_duplicates(["week_start", "issuer_code", "billing_region", "card_open_year"])
    if how == "per_card":
        c = cards.groupby(["fq", "billing_region"]).panel_cards.sum()
        return {r: (s[q][r] / c[q][r]) / (s[b][r] / c[b][r]) - 1 for r in REGIONS}, pw
    A = cards.groupby(["fq", "billing_region", "card_open_year"]).panel_cards.sum()
    S = sc.groupby(["fq", "billing_region", "card_open_year"]).spend_usd.sum()
    dy = P["qyear"][q] - P["qyear"][b]
    out = {}
    for r in REGIONS:
        num = den = 0.0
        for (rr, y), ab in A[b].items():
            if rr != r or ab <= 0 or (r, y + dy) not in A[q].index or A[q][(r, y + dy)] <= 0:
                continue
            num += ab * S[q][(r, y + dy)] / A[q][(r, y + dy)]
            den += S[b][(r, y)]
        out[r] = num / den - 1
    return out, pw


def company_weights(P, fy):
    row = P["regions"][P["regions"].fiscal_year == fy].iloc[0]
    v = np.array([row[r] for r in REGIONS], dtype=float)
    return dict(zip(REGIONS, v / v.sum()))


def rolled_weights(P, fy):
    """fiscal year fy's regional mix rolled forward one year by each region's growth in fy"""
    reg = P["regions"].set_index("fiscal_year")
    prev = "FY%d" % (int(fy[2:]) - 1)
    if prev not in reg.index:
        return company_weights(P, fy)
    v = np.array([reg.loc[fy, r] ** 2 / reg.loc[prev, r] for r in REGIONS])
    return dict(zip(REGIONS, v / v.sum()))


# ------------------------------------------------------------------------------- R5: the bank-card share's change
def bank_share(pl, other=None):
    return 1 - pl / 100.0 - (OTHER_TENDER if other is None else other)


def pl_target(pl, keys, q, rule="pace"):
    """the private-label card's share of quarter q's net sales from the quarters reported before it. pace: the latest
    quarter plus a third of the change over the last three quarters; yoy: the same quarter a year earlier plus the latest
    year-on-year change; line: a straight line through the last three quarters; last: the latest quarter plus its own
    change; flat: the latest quarter held; hindsight: the quarter's own reported share"""
    i = keys.index(q)
    k1, k2, k3, k4 = keys[i - 1], keys[i - 2], keys[i - 3], keys[i - 4]
    if rule == "pace":
        return pl[k1] + (pl[k1] - pl[k4]) / 3.0
    if rule == "yoy":
        if i < 5:
            return pl_target(pl, keys, q, "pace")
        return pl[k4] + (pl[k1] - pl[keys[i - 5]])
    if rule == "line":
        return float(np.polyval(np.polyfit([1, 2, 3], [pl[k3], pl[k2], pl[k1]], 1), 4))
    if rule == "last":
        return pl[k1] + (pl[k1] - pl[k2])
    if rule == "flat":
        return pl[k1]
    if rule == "hindsight":
        return pl[q] if q in pl else pl_target(pl, keys, q, "pace")
    raise ValueError(rule)


# --------------------------------------------------------------------------------------------- the chain and routes
def growth(P, pan, q, b, how="tenure", mix="company", drift=True, fern_ok=True, plrule="pace", wfy=None, other=None):
    rg, pw = regional(P, pan, q, b, how, fern_ok)
    if mix == "company":
        w = company_weights(P, wfy or "FY%d" % (int(q[2:6]) - 1))
    elif mix == "rolled":
        w = rolled_weights(P, "FY%d" % (int(q[2:6]) - 1))
    else:
        t = sum(pw.values())
        w = {r: pw[r] / t for r in REGIONS}
    g = sum(rg[r] * w[r] for r in REGIONS)
    if drift:
        g = (1 + g) * bank_share(P["pl"][b], other) / bank_share(pl_target(P["pl"], P["keys"], q, plrule), other) - 1
    return g


def organic_growth(P, q, b, fern_in_both):
    """reported net sales growth of q over b, weekly averages, Fernhollow taken out unless consolidated in both"""
    res = P["results"].set_index("fiscal_quarter")

    def ns(k):
        v = float(res.net_sales_usd_m[k])
        f = res.fernhollow_net_sales_usd_m[k]
        if not fern_in_both and pd.notna(f):
            v -= float(f)
        return v / float(res.weeks[k])
    return ns(q) / ns(b) - 1


def fern_both(P, q, b):
    res = P["results"].set_index("fiscal_quarter")
    return res.period_start[q] >= ACQUIRED and res.period_start[b] >= ACQUIRED


def prev_q(P, k):
    keys = P["keys"]
    i = keys.index(k)
    return keys[i - 1] if i > 0 else "FY%d Q4" % (int(k[2:6]) - 1)


def weeks_of(P, k):
    return float(P["results"].set_index("fiscal_quarter").weeks[k])


def net_sales(P, k, fern_ok=True):
    res = P["results"].set_index("fiscal_quarter")
    v = float(res.net_sales_usd_m[k])
    f = res.fernhollow_net_sales_usd_m[k]
    return v - (float(f) if (not fern_ok and pd.notna(f)) else 0.0)


def wholesale(P, k):
    return float(P["results"].set_index("fiscal_quarter").wholesale_net_sales_usd_m[k])


def retail(P, k, fern_ok=True):
    return net_sales(P, k, fern_ok) - wholesale(P, k)


def payments(P, k, fern_ok=True):
    """what retail customers paid in the quarter: retail net sales plus the change in customer deposits"""
    return retail(P, k, fern_ok) + P["deposits"][k] - P["deposits"][prev_q(P, k)]


def ws_hat(P, q, rule="median8"):
    """wholesale for quarter q from the quarters reported before it"""
    keys = P["keys"]
    i = keys.index(q)
    hist = [wholesale(P, k) for k in keys[max(0, i - 8):i]]
    if rule == "median8":
        return float(np.median(hist))
    if rule == "median4":
        return float(np.median(hist[-4:]))
    if rule == "mean4":
        return float(np.mean(hist[-4:]))
    if rule == "last_year":
        return wholesale(P, keys[i - 4])
    raise ValueError(rule)


def deposit_weeks(P, k):
    """customer deposits at the quarter's end in weeks of the banner's payments that quarter"""
    return P["deposits"][k] / (payments(P, k, False) / weeks_of(P, k))


_PROFILE = {}


def banner_profile(P, pan, q):
    """the panel's weekly spend at the banner's ids (stores and site, not Fernhollow) over quarter q's weeks, on the
    issuers present in every week of it, as shares of the quarter"""
    key = (_token(pan), q)
    if key not in _PROFILE:
        sub = pan[(pan.fq == q) & (pan.merchant_id != "M2290")]
        nw = sub.week_start.nunique()
        cov = sub.groupby("issuer_code").week_start.nunique()
        wk = sub[sub.issuer_code.isin(cov[cov == nw].index)].groupby("week_start").spend_usd.sum().sort_index()
        _PROFILE[key] = (wk / wk.sum()).values
    return _PROFILE[key]


def trailing(profile, L):
    """the share of a quarter's payments made in its last L weeks (L fractional)"""
    v = profile[::-1]
    n = int(np.floor(L))
    fr = L - n
    return float(v[:n].sum() + (fr * v[n] if n < len(v) else 0.0))


def fit_lead(P, pan, quarters):
    """the made-to-order share s and the weeks from order to delivery L that best explain the deposits at these quarter
    ends as s times the banner's payments in the quarter's last L weeks (least squares over a grid of L)"""
    y = np.array([P["deposits"][k] for k in quarters])
    best = None
    for L in np.arange(2.0, 13.001, 0.05):
        x = np.array([payments(P, k, False) * trailing(banner_profile(P, pan, k), L) for k in quarters])
        sh = float(x @ y / (x @ x))
        sse = float(((y - sh * x) ** 2).sum())
        if best is None or sse < best[0]:
            best = (sse, sh, float(L))
    return best[1], best[2]


def solve_lead(P, pan, k, sh):
    """the weeks from order to delivery that give the deposits at quarter k's end with made-to-order share sh"""
    prof = banner_profile(P, pan, k)
    target = P["deposits"][k] / (sh * payments(P, k, False))
    lo, hi = 0.0, float(len(prof))
    for _ in range(60):
        mid = (lo + hi) / 2
        if trailing(prof, mid) < target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


_LEAD = {}


def lead_rolling(P, pan, q):
    """as known before quarter q: s and L fitted together on the four quarter ends before q"""
    key = (_token(pan), q, "rolling")
    if key not in _LEAD:
        ks = [prev_q(P, q)]
        for _ in range(3):
            ks.append(prev_q(P, ks[-1]))
        sh, L = fit_lead(P, pan, [k for k in ks if k in P["keys"]])
        _LEAD[key] = (sh, L, L)
    return _LEAD[key]


def lead_asof(P, pan, q, rule="persist"):
    """as known before quarter q: s fitted on the quarter ends of the complete fiscal years before q's, L solved at the
    end of the quarter before q (persist) or moved on by its latest change (trend)"""
    key = (_token(pan), q, rule)
    if key not in _LEAD:
        fy = int(q[2:6])
        fit_q = [k for k in P["keys"][:-1] if int(k[2:6]) < fy]
        sh, L0 = fit_lead(P, pan, fit_q)
        q1 = prev_q(P, q)
        L = solve_lead(P, pan, q1, sh)
        if rule == "trend":
            L = L + (L - solve_lead(P, pan, prev_q(P, q1), sh))
        _LEAD[key] = (sh, L, L0)
    return _LEAD[key]


def convert(P, q, b, x, fern_ok, rule="ratio", pan=None):
    """net sales growth of q over b from payments growth x: payments rebuilt from b's, the deposits at q's end from the
    deposits-to-payments weeks at the end of the quarter before q (ratio), that figure moved on by its latest change
    (trend), its mean over the last four quarter ends (mean4), or last year's change in the same quarter scaled to the
    payments (persist_change); net sales are the payments less the change in deposits"""
    wq, wb = weeks_of(P, q), weeks_of(P, b)
    pay_b = payments(P, b, fern_ok)
    pay_q = pay_b / wb * (1 + x) * wq
    bshare = payments(P, b, False) / pay_b
    bp_q = pay_q * bshare
    q1 = prev_q(P, q)
    if rule in ("mto", "mto_7w", "mto_9w", "mto_q"):
        dy = {"mto": 56, "mto_7w": 49, "mto_9w": 63, "mto_q": 91}[rule]
        tq = trailing(banner_profile(P, pan, q), dy / 7.0)
        tb = trailing(banner_profile(P, pan, b), dy / 7.0)
        dep_q = P["deposits"][b] * (bp_q * tq * mto_share_last(P, q, dy)) / (payments(P, b, False) * tb * mto_share_last(P, b, dy))
        chg = dep_q - P["deposits"][q1]
    elif rule in ("lead", "lead_trend", "lead4"):
        if rule == "lead4":
            sh, L, _ = lead_rolling(P, pan, q)
        else:
            sh, L, _ = lead_asof(P, pan, q, "persist" if rule == "lead" else "trend")
        dep_q = sh * bp_q * trailing(banner_profile(P, pan, q), L)
        chg = dep_q - P["deposits"][q1]
    elif rule == "persist_change":
        chg = (P["deposits"][b] - P["deposits"][prev_q(P, b)]) * bp_q / payments(P, b, False)
    else:
        if rule == "ratio":
            r = deposit_weeks(P, q1)
        elif rule == "trend":
            r = deposit_weeks(P, q1) + (deposit_weeks(P, q1) - deposit_weeks(P, prev_q(P, q1)))
        elif rule == "mean4":
            ks = [q1]
            for _ in range(3):
                ks.append(prev_q(P, ks[-1]))
            r = float(np.mean([deposit_weeks(P, k) for k in ks]))
        else:
            raise ValueError(rule)
        chg = r * bp_q / wq - P["deposits"][q1]
    rev_q = pay_q - chg
    return (rev_q / wq) / (retail(P, b, fern_ok) / wb) - 1, dict(pay_q=pay_q, dep_change=chg, rev_q=rev_q)


_MTO = {}


def mto_share_last(P, q, days=56):
    key = (q, days)
    """the made-to-order share of the banner's panel spend over the last eight weeks of quarter q, from the monthly
    descriptor detail (months weighted by their days in the window): the design studios and the site's custom orders
    against the brand ids less the licensed shops and cafes"""
    if key not in _MTO:
        d = P["desc"]
        res = P["results"].set_index("fiscal_quarter")
        end = res.period_end[q]
        start = end - pd.Timedelta(days=days - 1)
        win = pd.date_range(start, end, freq="D")
        wts = pd.Series(1.0, index=win).groupby(win.strftime("%Y-%m")).sum()
        mdays = {m: pd.Period(m).days_in_month for m in wts.index}
        b = d[d.merchant_id.isin(["M0412", "M0413"]) & ~d.descriptor.str.contains("HOLLISTERS|CAFE", regex=True)]
        b = b[b.month.isin(wts.index)]
        mt = b[b.descriptor.str.contains("DESIGN STUDIO|CUSTOM", regex=True)].groupby("month").spend_usd.sum()
        al = b.groupby("month").spend_usd.sum()
        w_ = pd.Series({m: wts[m] / mdays[m] for m in wts.index})
        _MTO[key] = float((mt.reindex(w_.index).fillna(0) * w_).sum() / (al.reindex(w_.index).fillna(0) * w_).sum())
    return _MTO[key]


def origins_of(P, first="FY2022 Q1", last=None):
    keys = P["keys"]
    return keys[keys.index(first):(keys.index(last) + 1 if last else -1)]


def to_total(P, q, b, g_ret, fern_ok, ws):
    """net sales growth of q over b: retail from its growth, wholesale from its run rate (ws), or the retail growth
    applied to all of net sales (ws None)"""
    if not ws:
        return g_ret
    wq, wb = weeks_of(P, q), weeks_of(P, b)
    tot_q = retail(P, b, fern_ok) / wb * (1 + g_ret) * wq + ws_hat(P, q, ws)
    return (tot_q / wq) / (net_sales(P, b, fern_ok) / wb) - 1


def route(P, pan, how="tenure", mix="company", drift=True, reg=False, plrule="pace", origins=None, bt_plrule=None,
          wfy_lag=1, other=None, target=TQ, dep=None, ws=None):
    """the route's growth for the target quarter and its rolling-origin record: at each past quarter the same method
    on what was known then (the prior fiscal year's regional mix, the private-label rule on the quarters reported
    before it); with reg, reported growth regressed on the chain over the origins before it (six or more)"""
    keys = P["keys"]
    origins = origins or origins_of(P)
    bq = keys[keys.index(target) - 4]
    first_fy = int(P["regions"].fiscal_year.iloc[0][2:])
    wfy = lambda q: "FY%d" % max(int(q[2:6]) - wfy_lag, first_fy)
    fo_t = fern_both(P, target, bq) or target == TQ
    xt = growth(P, pan, target, bq, how, mix, drift, fo_t, plrule, wfy(target), other)
    pay_t = xt
    if dep:
        xt, _ = convert(P, target, bq, xt, fo_t, dep, pan)
    xt = to_total(P, target, bq, xt, fo_t, ws)
    xs, ys, errs = [], [], {}
    for q in origins:
        b = keys[keys.index(q) - 4]
        fo = fern_both(P, q, b)
        x = growth(P, pan, q, b, how, mix, drift, fo, bt_plrule or plrule, wfy(q), other)
        if dep:
            x, _ = convert(P, q, b, x, fo, dep, pan)
        x = to_total(P, q, b, x, fo, ws)
        y = organic_growth(P, q, b, fo)
        if reg:
            if len(xs) >= 6:
                c = np.linalg.lstsq(np.column_stack([np.ones(len(xs)), xs]), ys, rcond=None)[0]
                errs[q] = float(c[0] + c[1] * x - y)
        else:
            errs[q] = float(x - y)
        xs.append(float(x))
        ys.append(float(y))
    fit = None
    if reg:
        fit = np.linalg.lstsq(np.column_stack([np.ones(len(xs)), xs]), ys, rcond=None)[0]
        g = float(fit[0] + fit[1] * xt)
    else:
        g = float(xt)
    e = np.array(list(errs.values()))
    rmse = float(np.sqrt(np.mean(e ** 2)))
    return dict(growth=g, x=float(xt), pay_growth=float(pay_t), rmse=rmse, errs=errs, xs=xs, ys=ys, fit=fit,
                origins=list(origins), inside=int(sum(abs(v) <= Z80 * rmse for v in e)), n=len(e))


def with_range(R, base):
    g, b = R["growth"], Z80 * R["rmse"]
    R.update(forecast=base * (1 + g), low=base * (1 + g - b), high=base * (1 + g + b), band=b)
    return R


def call_of(R, street):
    return "short" if R["high"] < street else ("long" if R["low"] > street else "no position")


# -------------------------------------------------------------------------------------------------------- the run
def run(tgt):
    P = load(tgt)
    res = P["results"]
    keys = P["keys"]
    base = float(res.set_index("fiscal_quarter").net_sales_usd_m[BQ])
    est = P["street"].q4_fy2025_net_sales_usd_m
    street = float(np.mean(est))
    cf = completion_factors(P)
    pan = panel_entity(P, cf)
    out = dict(P=P, cf=cf, pan=pan, base=base, street=street, street_median=float(np.median(est)),
               street_n=int(len(est)))
    # comparable growth by region, at the panel's mix and at the company's
    rg, pw = regional(P, pan, TQ, BQ, "tenure")
    cw = company_weights(P, "FY2024")
    tot = sum(pw.values())
    out.update(regional=rg, company_w=cw, panel_w={r: pw[r] / tot for r in REGIONS},
               g_idx=sum(rg[r] * cw[r] for r in REGIONS), g_pooled=sum(rg[r] * pw[r] / tot for r in REGIONS))
    # the private-label card's fourth-quarter share and net sales per bank-card dollar
    pl = P["pl"]
    out["pl_target"] = pl_target(pl, keys, TQ, "pace")
    out["drift"] = bank_share(pl[BQ]) / bank_share(out["pl_target"])
    out["g_pay"] = (1 + out["g_idx"]) * out["drift"] - 1
    # payments to net sales: the deposits at the quarter's end
    q3 = prev_q(P, TQ)
    _, cv = convert(P, TQ, BQ, out["g_pay"], True, "mto", pan)
    out["dep_weeks_q3"] = deposit_weeks(P, q3)
    out["lead_share"], out["lead_weeks"], out["lead_fit_weeks"] = lead_asof(P, pan, TQ, "persist")
    out["lead_by_quarter"] = {k: solve_lead(P, pan, k, out["lead_share"]) for k in keys[:-1]}
    out["dep_weeks_hist"] = {k: deposit_weeks(P, k) for k in keys[:-1]}
    out["dep_q4_est"] = P["deposits"][q3] + cv["dep_change"]
    out["dep_change"] = cv["dep_change"]
    out["dep_change_base"] = P["deposits"][BQ] - P["deposits"][prev_q(P, BQ)]
    out["pay_q4"] = cv["pay_q"]
    out["pay_base"] = payments(P, BQ, True)
    # the golden route, its record and range
    G = with_range(route(P, pan, dep="mto", ws="median8"), base)
    out["golden"] = G
    out["ws_hat"] = ws_hat(P, TQ, "median8")
    out["ws_base"] = wholesale(P, BQ)
    out["retail_base"] = retail(P, BQ, True)
    out["retail_growth"], _cv = convert(P, TQ, BQ, out["g_pay"], True, "mto", pan)
    out["retail_q4"] = _cv["rev_q"]
    out["growth"] = G["growth"]
    out["forecast"], out["range"] = G["forecast"], (G["low"], G["high"])
    out["call"] = call_of(G, street)
    # the entity and the immature weeks as figures
    d = P["desc"]
    days = pd.date_range(res.period_start.iloc[-1], res.period_end.iloc[-1], freq="D")
    qm = sorted(set(days.strftime("%Y-%m")))
    b = d[(d.merchant_id == "M0412") & d.month.isin(qm)]
    out["excluded_months"] = qm
    out["excluded_share"] = float(b[b.descriptor.str.contains("HOLLISTERS|CAFE", regex=True)].spend_usd.sum()
                                  / b.spend_usd.sum())
    raw_c = panel_entity(P, cf, complete=False)
    out["completion_uplift"] = float(pan[pan.fq == TQ].spend_usd.sum() / raw_c[raw_c.fq == TQ].spend_usd.sum() - 1)
    out["cf_last_week"] = {k[0]: v for k, v in cf.items() if k[1] == 0}
    # the bridge, in the order the panel is processed, and every order of its steps for the bands
    out["bridge"], out["bridge_orders"] = bridge(out)
    return out


PANEL_STEPS = ("the latest weeks completed", "the licensed shops and cafes taken out",
               "issuers in both years, cards of the same age")
COMPANY_STEPS = ("the company's regional mix", "the bank-card share of net sales", "revenue on delivery",
                 "wholesale at its run rate")


def bridge(out):
    """growth after each step from the delivered panel (every issuer, every merchant id) to net sales; the panel's three
    steps and the company's three in the golden's order, and each step's worth under every order of its group"""
    import itertools
    P, cf = out["P"], out["cf"]

    def panel_state(S):
        pan = panel_entity(P, cf, complete="the latest weeks completed" in S,
                           exclude="the licensed shops and cafes taken out" in S)
        if "issuers in both years, cards of the same age" in S:
            rg, pw = regional(P, pan, TQ, BQ, "tenure")
            t = sum(pw.values())
            return sum(rg[r] * pw[r] / t for r in REGIONS)
        return growth(P, pan, TQ, BQ, "all_issuers", "panel", False)

    def company_state(S):
        x = out["g_idx"] if "the company's regional mix" in S else out["g_pooled"]
        if "the bank-card share of net sales" in S:
            x = (1 + x) * out["drift"] - 1
        if "revenue on delivery" in S:
            x, _ = convert(P, TQ, BQ, x, True, "mto", out["pan"])
        if "wholesale at its run rate" in S:
            x = to_total(P, TQ, BQ, x, True, "median8")
        return x

    cache = {}
    orders = {k: [] for k in PANEL_STEPS + COMPANY_STEPS}
    for group, fn in ((PANEL_STEPS, panel_state), (COMPANY_STEPS, company_state)):
        for perm in itertools.permutations(group):
            done = []
            prev = cache.setdefault(tuple(sorted(done)) + (fn.__name__,), fn(set(done)))
            for st in perm:
                done.append(st)
                key = tuple(sorted(done)) + (fn.__name__,)
                if key not in cache:
                    cache[key] = fn(set(done))
                orders[st].append(cache[key] - prev)
                prev = cache[key]
    g0 = cache[("panel_state",)]
    vals = [("the delivered panel, every issuer", g0)]
    done, prev = [], g0
    for st in PANEL_STEPS:
        done.append(st)
        v = cache[tuple(sorted(done)) + ("panel_state",)]
        vals.append((st, v - prev))
        prev = v
    done, prev = [], cache[("company_state",)]
    for st in COMPANY_STEPS:
        done.append(st)
        v = cache[tuple(sorted(done)) + ("company_state",)]
        vals.append((st, v - prev))
        prev = v
    return vals, orders


def family(out):
    """the golden family: defensible rivals of the golden route, each with its range"""
    P, pan, base = out["P"], out["pan"], out["base"]
    F = {"the golden route": out["golden"]}
    for rule, name in (("yoy", "private-label share carried by the third quarter's year-on-year change"),
                       ("line", "private-label share on a straight line through fiscal 2025's three quarters"),
                       ("last", "private-label share carried at the third quarter's own change")):
        F[name] = with_range(route(P, pan, plrule=rule, dep="mto", ws="median8"), base)
    F["the regional mix of fiscal 2023"] = with_range(route(P, pan, wfy_lag=2, dep="mto", ws="median8"), base)
    F["fiscal 2024's regional mix rolled forward a year"] = with_range(route(P, pan, mix="rolled", dep="mto", ws="median8"), base)
    F["the deposit window at seven weeks"] = with_range(route(P, pan, dep="mto_7w", ws="median8"), base)
    F["wholesale at the median of the last four quarters"] = with_range(route(P, pan, dep="mto", ws="median4"), base)
    F["the deposit window at nine weeks"] = with_range(route(P, pan, dep="mto_9w", ws="median8"), base)
    F["the chain calibrated by regression on past quarters"] = with_range(route(P, pan, reg=True, dep="mto", ws="median8"), base)
    F["the record from fiscal 2023 only"] = with_range(route(P, pan, origins=origins_of(P, "FY2023 Q1"), dep="mto", ws="median8"), base)
    return F


def rivals_ruled_out(out):
    """rivals the data rule out, run to show where they land"""
    P, pan, base = out["P"], out["pan"], out["base"]
    R = {}
    R["spend per card instead of cards of the same age"] = with_range(route(P, pan, how="per_card", dep="mto", ws="median8"), base)
    R["private-label share held at the third quarter's level"] = with_range(route(P, pan, plrule="flat", dep="mto", ws="median8"), base)
    R["the record with each quarter's own reported private-label share"] = with_range(
        route(P, pan, bt_plrule="hindsight", dep="mto", ws="median8"), base)
    R["deposits at the third quarter's weeks of payments"] = with_range(route(P, pan, dep="ratio", ws="median8"), base)
    R["the made-to-order share over the whole quarter"] = with_range(route(P, pan, dep="mto_q", ws="median8"), base)
    R["wholesale at the mean of the last four quarters, last year's contract included"] = with_range(
        route(P, pan, dep="mto", ws="mean4"), base)
    R["deposits from a lead time carried from the third quarter"] = with_range(route(P, pan, dep="lead", ws="median8"), base)
    return R


def shortcuts(out):
    """the hurried routes: what each files for the quarter, with its own record and range"""
    P, pan, base, cf = out["P"], out["pan"], out["base"], out["cf"]
    inc_pan = panel_entity(P, cf, complete=True, exclude=False)
    S = {}
    S["careful"] = with_range(route(P, pan), base)
    S["careful_regressed"] = with_range(route(P, pan, reg=True), base)
    S["panel_regressed"] = with_range(route(P, pan, mix="panel", drift=False, reg=True), base)
    S["deposit_ratio"] = with_range(route(P, pan, dep="ratio", ws="median8"), base)
    S["last_year_deposits"] = with_range(route(P, pan, dep="persist_change", ws="median8"), base)
    S["deposits_only"] = with_range(route(P, pan, dep="mto"), base)
    S["wholesale_only"] = with_range(route(P, pan, ws="median8"), base)
    S["no_mix"] = with_range(route(P, pan, mix="panel", dep="mto", ws="median8"), base)
    S["no_tender"] = with_range(route(P, pan, drift=False, dep="mto", ws="median8"), base)
    S["desk_model"] = with_range(route(P, inc_pan, how="per_card", mix="panel", drift=False, reg=True), base)
    keys = P["keys"]
    org = {q: organic_growth(P, q, keys[keys.index(q) - 4], fern_both(P, q, keys[keys.index(q) - 4]))
           for q in origins_of(P)}
    S["trend"] = with_range(trend_route(P, False), base)
    S["trend_retail"] = with_range(trend_route(P, True), base)
    p0 = panel_entity(P, cf, complete=False, exclude=False)
    S["quick"] = dict(growth=growth(P, p0, TQ, BQ, "all_issuers", "panel", False))
    S["quick"]["forecast"] = base * (1 + S["quick"]["growth"])
    out["organic"] = org
    return S


def variants(out):
    """each supporting result's rivals, for its band"""
    P, cf, pan = out["P"], out["cf"], out["pan"]
    keys = P["keys"]
    V = {}
    raw_c = panel_entity(P, cf, complete=False)
    tot_raw = raw_c[raw_c.fq == TQ].spend_usd.sum()
    for name, kw in (("mean factors", dict(stat="mean")), ("the last thirteen deliveries", dict(last_n=13))):
        c2 = completion_factors(P, **kw)
        p2 = panel_entity(P, c2)
        V.setdefault("completion", {})[name] = float(p2[p2.fq == TQ].spend_usd.sum() / tot_raw - 1)
    rgp, pw = regional(P, pan, TQ, BQ, "per_card")
    t = sum(pw.values())
    V["comparable_per_card"] = sum(rgp[r] * pw[r] / t for r in REGIONS)
    rg = out["regional"]
    V["visible"] = {"fiscal 2024 mix": out["g_idx"],
                    "fiscal 2023 mix": sum(rg[r] * company_weights(P, "FY2023")[r] for r in REGIONS),
                    "fiscal 2024 mix rolled forward": sum(rg[r] * rolled_weights(P, "FY2024")[r] for r in REGIONS)}
    pl = P["pl"]
    V["pl"] = {rule: pl_target(pl, keys, TQ, rule) for rule in ("pace", "yoy", "line", "last")}
    V["drift"] = {rule: bank_share(pl[BQ]) / bank_share(v) - 1 for rule, v in V["pl"].items()}
    V["dep_change"] = {}
    V["dep_points"] = {}
    for rule in ("mto", "mto_7w", "mto_9w"):
        for vk, vg in V["visible"].items():
            for pk, pd_ in V["drift"].items():
                x = (1 + vg) * (1 + pd_) - 1
                g, cv = convert(P, TQ, BQ, x, True, rule, pan)
                V["dep_change"]["%s, %s, %s" % (rule, vk, pk)] = cv["dep_change"]
                V["dep_points"]["%s, %s, %s" % (rule, vk, pk)] = g - x
    return V


def trend_route(P, retail_only):
    """reported growth carried: the mean of the last three quarters' year-on-year growth (net sales, or retail with
    wholesale at its run rate), with the same rule's record from the first quarter it can be built for"""
    keys = P["keys"]

    def yoy(k, ret):
        b = keys[keys.index(k) - 4]
        fo = fern_both(P, k, b)
        if ret:
            return (retail(P, k, fo) / weeks_of(P, k)) / (retail(P, b, fo) / weeks_of(P, b)) - 1
        return organic_growth(P, k, b, fo)

    def forecast(q):
        prev = keys[keys.index(q) - 3:keys.index(q)]
        g = float(np.mean([yoy(k, retail_only) for k in prev]))
        return to_total(P, q, keys[keys.index(q) - 4], g, fern_both(P, q, keys[keys.index(q) - 4]) or q == TQ,
                        "median8" if retail_only else None)

    errs = {}
    for q in origins_of(P, "FY2022 Q4"):
        errs[q] = forecast(q) - organic_growth(P, q, keys[keys.index(q) - 4], fern_both(P, q, keys[keys.index(q) - 4]))
    e = np.array(list(errs.values()))
    rmse = float(np.sqrt(np.mean(e ** 2)))
    return dict(growth=forecast(TQ), rmse=rmse, errs=errs, n=len(e), inside=int(sum(abs(v) <= Z80 * rmse for v in e)))


def incumbent(out):
    """the desk's third-quarter model as its workbook states it: spend per open card on the issuers in both years, the
    brand ids as delivered, reported growth regressed on it over the quarters to the second quarter of fiscal 2025"""
    P, cf = out["P"], out["cf"]
    inc_pan = panel_entity(P, cf, complete=True, exclude=False)
    org = origins_of(P, "FY2022 Q1", "FY2025 Q2")
    R = route(P, inc_pan, how="per_card", mix="panel", drift=False, reg=True, target="FY2025 Q3", origins=org)
    res = P["results"].set_index("fiscal_quarter")
    q3_base = float(res.net_sales_usd_m["FY2024 Q3"])
    return dict(rows=list(zip(org, R["xs"], R["ys"])), fit=R["fit"], rmse=R["rmse"], errs=R["errs"], x_q3=R["x"],
                g_q3=R["growth"], q3_base=q3_base, q3_forecast=q3_base * (1 + R["growth"]),
                q3_actual=float(res.net_sales_usd_m["FY2025 Q3"]))


def perturbations(out):
    """each fitted or stated input moved by its defensible spread; the value is the top of the golden's 80 per cent range"""
    P, pan, base = out["P"], out["pan"], out["base"]
    res = {}
    for o in (0.10, 0.14):
        res["other tenders at %d per cent of net sales" % round(100 * o)] = with_range(
            route(P, pan, other=o, dep="mto", ws="median8"), base)["high"]
    for f in (0.97, 1.03):
        cf = {k: min(1.0, v * f) if k[1] == 0 else v for k, v in out["cf"].items()}
        res["the last week's completeness %+d per cent" % round(100 * (f - 1))] = with_range(
            route(P, panel_entity(P, cf), dep="mto", ws="median8"), base)["high"]
    for f in (0.8, 1.2):
        res["the licensed shops' and cafes' share %+d per cent" % round(100 * (f - 1))] = with_range(
            route(P, panel_entity(P, out["cf"], share_scale=f), dep="mto", ws="median8"), base)["high"]
    G = out["golden"]
    e = np.array(list(G["errs"].values()))
    res["the range from the record's 10th and 90th percentile errors"] = base * (1 + G["growth"] - float(np.quantile(e, 0.1)))
    return res


def full(tgt):
    out = run(tgt)
    out["family"] = family(out)
    out["ruled_out"] = rivals_ruled_out(out)
    out["shortcuts"] = shortcuts(out)
    out["incumbent"] = incumbent(out)
    out["perturb"] = perturbations(out)
    out["variants"] = variants(out)
    return out
