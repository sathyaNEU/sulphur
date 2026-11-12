"""task20 architecture 2 analysis (second hardening): Brindle & Moss's fourth-quarter fiscal 2025 net sales nowcast, computed from the
shipped files in target/ alone, with the rivals that set each band and the hurried routes effort.json prices.

One route function carries every method: the panel's normalisation (spend per open card, per issuer, cards of the same
age, or raw spend), the issuers compared (every issuer, those in every week of both quarters, and those less any issuer
whose cards took a re-issued book between the two quarters), the regional weights (the company's prior-year brand net
sales by region, or the panel's own spend), the step from customer payments to net sales (revenue on delivery through
the customer deposits at the quarter's end, or none), and contract sales (at the run rate of the quarters before, or
inside one growth rate for all of net sales). The golden is spend per open card on the issuers in every week of both
quarters less KS-01 (whose cards took KS-06's re-issued book in October 2025), at the company's fiscal 2024 regional
mix, with the quarter-end deposits scaled from last year's by the last eight weeks' payments and custom-order share,
and contract at the median of the eight quarters before."""
import os
import re
import subprocess

import numpy as np
import pandas as pd

import docs as DC
import pack as PK

REGIONS = ["Northeast", "Southeast", "Midwest", "West"]
Z80 = 1.2816                  # the two-sided 80 per cent normal quantile
ACQUIRED = pd.Timestamp("2024-06-02")
TQ, BQ = "FY2025 Q4", "FY2024 Q4"
JUMP = 0.05                   # a four-week rise in an issuer's cards in a region larger than this is a re-issued book
NUM = {"thirteen": 13, "fourteen": 14}
ORDN = {"first": 1, "second": 2, "third": 3, "fourth": 4}


def norm_region(x):
    k = re.sub(r"[^A-Z]", "", str(x).upper())
    return {"NE": "Northeast", "NORTHEAST": "Northeast", "SE": "Southeast", "SOUTHEAST": "Southeast",
            "MW": "Midwest", "MIDWEST": "Midwest", "W": "West", "WEST": "West"}[k]


# ---------------------------------------------------------------------------------------------------------- the files
def _nums(s):
    out = []
    for tok in re.findall(r"\(?[\d,]+\)?|--", s):
        if tok == "--":
            out.append(0.0)
            continue
        neg = tok.startswith("(")
        v = float(tok.strip("()").replace(",", ""))
        out.append(-v if neg else v)
    return out


def _row(block, label):
    for ln in block.splitlines():
        if ln[:52].strip() == label:
            return _nums(ln[52:])
    return None


def read_release(path):
    txt = open(path).read()
    m = re.search(r"results for the (\w+) quarter of fiscal (\d{4}), the (\w+) weeks ended (\w+ \d+, \d{4})", txt)
    fq, fy, weeks, end = ORDN[m.group(1)], int(m.group(2)), NUM[m.group(3)], pd.Timestamp(m.group(4))
    inc = txt.split("STATEMENTS OF INCOME")[1].split("NET SALES BY BRAND")[0]
    brand = txt.split("NET SALES BY BRAND")[1].split("BALANCE SHEETS")[0]
    bs = txt.split("BALANCE SHEETS")[1]
    ns = _row(inc, "Net sales")
    ct = _row(brand, "Contract") or _row(brand, "B&M Contract")
    fern = _row(brand, "Fernhollow") or [0.0] * len(ct)
    dep = _row(bs, "Customer deposits")
    return dict(key="FY%d Q%d" % (fy, fq), fy=fy, fq=fq, weeks=weeks, end=end, ns=ns, ct=ct, fern=fern, dep=dep)


def read_releases(tgt):
    rel = {}
    for f in sorted(os.listdir(tgt)):
        if f.startswith("bmh_8k_ex99-1_"):
            r = read_release(os.path.join(tgt, f))
            r["file"] = f
            rel[r["key"]] = r
    rows, dep = [], {}
    for k, r in rel.items():
        q_ns = r["ns"][0] / 1000.0
        if r["fq"] < 4:
            ct, fern = r["ct"][0] / 1000.0, r["fern"][0] / 1000.0
        else:
            q3 = rel["FY%d Q3" % r["fy"]]
            ct = (r["ct"][0] - q3["ct"][2]) / 1000.0
            fern = (r["fern"][0] - q3["fern"][2]) / 1000.0
        rows.append(dict(fiscal_quarter=k, period_end=r["end"], weeks=r["weeks"],
                         period_start=r["end"] - pd.Timedelta(days=7 * r["weeks"] - 1), net_sales=q_ns,
                         contract=round(ct, 3), fern=round(fern, 3), release=r["file"]))
        dep[k] = r["dep"][0] / 1000.0
        if k == "FY2021 Q1":
            dep["FY2020 Q4"] = r["dep"][1] / 1000.0
    res = pd.DataFrame(rows).sort_values("period_end").reset_index(drop=True)
    last = res.iloc[-1]
    res.loc[len(res)] = dict(fiscal_quarter=TQ, period_end=last.period_end + pd.Timedelta(days=91), weeks=13,
                             period_start=last.period_end + pd.Timedelta(days=1), net_sales=np.nan, contract=np.nan,
                             fern=np.nan, release="")
    return res, dep, rel


def read_regions(path):
    txt = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True).stdout
    block = txt.split("Net sales by brand and region")[1].split("Acquisition")[0]
    years = [int(y) for y in re.findall(r"Fiscal (\d{4})", block)]
    reg = pd.DataFrame({"fiscal_year": ["FY%d" % y for y in years]})
    for r in REGIONS:
        m = re.search(r"^\s*%s\s+([\d,\.\s]+)$" % r, block, re.M)
        reg[r] = [float(x.replace(",", "")) for x in m.group(1).split()][:len(years)]
    return reg


def load(tgt):
    _CACHE.clear()
    P = {}
    P["results"], P["deposits"], P["releases"] = read_releases(tgt)
    P["regions"] = read_regions(os.path.join(tgt, DC.F_FILING))
    pan = pd.read_csv(os.path.join(tgt, PK.F_PANEL), dtype={"card_open_year": str})
    pan["week_start"] = pd.to_datetime(pan.week_start)
    codes = {c: norm_region(c) for c in pan.billing_region.unique()}
    pan["billing_region"] = pan.billing_region.map(codes)
    P["panel"] = pan
    hist = pd.read_csv(os.path.join(tgt, PK.F_HIST))
    hist["delivery_date"] = pd.to_datetime(hist.delivery_date)
    hist["week_start"] = pd.to_datetime(hist.week_start)
    P["hist"] = hist
    P["desc"] = pd.read_csv(os.path.join(tgt, PK.F_DESC))
    P["street"] = pd.read_csv(os.path.join(tgt, PK.F_STREET))
    res = P["results"]
    P["keys"] = list(res.fiscal_quarter)
    P["qyear"] = {r.fiscal_quarter: r.period_start.year for r in res.itertuples()}
    P["start"] = dict(zip(res.fiscal_quarter, res.period_start))
    P["end"] = dict(zip(res.fiscal_quarter, res.period_end))
    return P


_CACHE = {}


def res_of(P, k, col):
    return float(P["results"].set_index("fiscal_quarter")[col][k])


def prev_q(P, k):
    keys = P["keys"]
    i = keys.index(k)
    return keys[i - 1] if i > 0 else "FY2020 Q4"


def weeks_of(P, k):
    return res_of(P, k, "weeks")


# ------------------------------------------------------------------------------------------- the immature weeks
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


# ------------------------------------------------------------------------------------- the reporting entity
LICENSED = "HOLLISTERS|CAFE"
CUSTOM = "DESIGN STUDIO|CUSTOM"


def excluded_share(P):
    """the licensed shop-in-shops' and cafes' share of the brand merchant id's spend, by month"""
    b = P["desc"][P["desc"].merchant_id == "M0412"].copy()
    b["out"] = b.descriptor.str.contains(LICENSED, regex=True)
    tot = b.groupby("month").spend_usd.sum()
    return b[b.out].groupby("month").spend_usd.sum().reindex(tot.index).fillna(0) / tot


def quarter_of(P, weeks):
    out = pd.Series(index=weeks.index, dtype=object)
    for r in P["results"].itertuples():
        out[(weeks >= r.period_start) & (weeks <= r.period_end)] = r.fiscal_quarter
    return out


def panel_entity(P, cf, complete=True, exclude=True, share_scale=1.0):
    """the reporting entity's panel spend: the brand id less the licensed shops and cafes, the site, and Fernhollow
    from its acquisition; the latest weeks completed by each issuer's completion factors"""
    key = ("entity", id(cf) if cf else None, tuple(sorted(cf.items())) if cf else None, complete, exclude, share_scale)
    if key in _CACHE:
        return _CACHE[key]
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
    pan.attrs["tok"] = len(_CACHE) + 1
    _CACHE[key] = pan
    return pan


# ------------------------------------------------------------------------------- the panel's issuers and their books
def card_series(P):
    """each issuer's panel cards by billing region and week (cards are repeated on each merchant row)"""
    if "cards" not in _CACHE:
        pan = P["panel"]
        c = pan.drop_duplicates(["week_start", "issuer_code", "billing_region", "card_open_year"])
        _CACHE["cards"] = c.groupby(["issuer_code", "billing_region", "week_start"]).panel_cards.sum()
    return _CACHE["cards"]


def reissues(P, jump=JUMP):
    """weeks in which an issuer's cards in a region rose by more than `jump` over four weeks, outside the issuer's first
    eight weeks: a book of accounts re-issued under the issuer's codes"""
    return reissue_flags(P, jump)[0]


def reissue_flags(P, jump=JUMP):
    """the re-issued books' weeks by issuer, and by issuer and region"""
    key = ("reissues", jump)
    if key not in _CACHE:
        cs = card_series(P)
        out, by_reg = {}, {}
        for (iss, reg), s in cs.groupby(level=[0, 1]):
            s = s.droplevel([0, 1]).sort_index()
            r4 = s / s.shift(4) - 1
            hit = r4[(r4 > jump) & (np.arange(len(r4)) >= 8)]
            for wk in hit.index:
                out.setdefault(iss, set()).add(pd.Timestamp(wk))
                by_reg.setdefault((iss, reg), set()).add(pd.Timestamp(wk))
        _CACHE[key] = ({k: sorted(v) for k, v in out.items()}, {k: sorted(v) for k, v in by_reg.items()})
    return _CACHE[key]


def issuers_for(P, sub, q, b, how, conv=True, jump=JUMP, book="issuer"):
    """the issuers compared: every issuer (all), those reporting in every week of both quarters, less (conv) any issuer
    whose cards took a re-issued book between the base quarter's start and the target quarter's end (book "issuer"),
    or that ever took one (book "always"); books "region" and "newest" keep the issuer and set aside part of it later"""
    if how == "all":
        return sorted(sub.issuer_code.unique())
    weeks = sub.groupby("fq").week_start.nunique()
    cov = sub.groupby(["issuer_code", "fq"]).week_start.nunique().unstack()
    keep = [i for i in cov.index if cov.loc[i].get(q, 0) == weeks.get(q, 0) and cov.loc[i].get(b, 0) == weeks.get(b, 0)]
    if conv and book in ("issuer", "always"):
        lo, hi = P["start"][b], P["end"][q]
        rs = reissues(P, jump)
        keep = [i for i in keep if not any((book == "always") or (lo <= wk <= hi) for wk in rs.get(i, []))]
    return keep


def set_aside(P, sc, q, b, jump=JUMP, book="region"):
    """part of an issuer set aside for a re-issued book between the two quarters: the region whose cards jumped
    (region), or the open years from the book's own year on in the target quarter and from the year before in the base
    (newest)"""
    lo, hi = P["start"][b], P["end"][q]
    out = sc
    if book == "region":
        for (iss, reg), wks in reissue_flags(P, jump)[1].items():
            if any(lo <= wk <= hi for wk in wks):
                out = out[~((out.issuer_code == iss) & (out.billing_region == reg))]
    elif book == "newest":
        for iss, wks in reissue_flags(P, jump)[0].items():
            w = [wk for wk in wks if lo <= wk <= hi]
            if not w:
                continue
            y = min(wk.year for wk in w)
            yr = pd.to_numeric(out.card_open_year.str.replace("<=", "", regex=False), errors="coerce")
            drop = (out.issuer_code == iss) & (((out.fq == q) & (yr >= y)) | ((out.fq == b) & (yr >= y - 1)))
            out = out[~drop]
    return out


# ------------------------------------------------------------------------------------------------ growth on the panel
def regional(P, pan, q, b, how="per_card", issuers="const", conv=True, fern_ok=True, jump=JUMP, book="issuer"):
    """year-on-year growth of quarter q over quarter b (weekly averages) by billing region, and the base quarter's
    panel spend by region. how: per_card (spend per open card, pooled over the issuers), lfl (spend per open card issuer
    by issuer, weighted by the base quarter's spend), same_age (each open year against the open year one later, on the
    base quarter's cards), total (spend)"""
    key = ("regional", pan.attrs.get("tok"), q, b, how, issuers, conv, fern_ok, jump, book)
    if key in _CACHE:
        return _CACHE[key]
    sub = pan[pan.fq.isin([q, b])]
    if not fern_ok:
        sub = sub[sub.merchant_id != "M2290"]
    n = {k: sub[sub.fq == k].week_start.nunique() for k in (q, b)}
    keep = issuers_for(P, sub, q, b, issuers, conv, jump, book)
    sc = sub[sub.issuer_code.isin(keep)]
    if conv and book in ("region", "newest"):
        sc = set_aside(P, sc, q, b, jump, book)
    s = sc.groupby(["fq", "billing_region"]).spend_usd.sum()
    pw = {r: float(s[b][r]) for r in REGIONS}
    out = {}
    if how == "total":
        out = {r: (s[q][r] / n[q]) / (s[b][r] / n[b]) - 1 for r in REGIONS}
    else:
        cards = sc.drop_duplicates(["week_start", "issuer_code", "billing_region", "card_open_year"])
        if how == "per_card":
            c = cards.groupby(["fq", "billing_region"]).panel_cards.sum()
            out = {r: (s[q][r] / c[q][r]) / (s[b][r] / c[b][r]) - 1 for r in REGIONS}
        elif how == "lfl":
            si = sc.groupby(["fq", "billing_region", "issuer_code"]).spend_usd.sum()
            ci = cards.groupby(["fq", "billing_region", "issuer_code"]).panel_cards.sum()
            for r in REGIONS:
                num = den = 0.0
                for i in keep:
                    if (r, i) not in si[b].index or (r, i) not in si[q].index:
                        continue
                    num += si[b][(r, i)] * (si[q][(r, i)] / ci[q][(r, i)]) / (si[b][(r, i)] / ci[b][(r, i)])
                    den += si[b][(r, i)]
                out[r] = num / den - 1
        elif how == "same_age":
            A = cards.groupby(["fq", "billing_region", "card_open_year"]).panel_cards.sum()
            S = sc.groupby(["fq", "billing_region", "card_open_year"]).spend_usd.sum()
            dy = P["qyear"][q] - P["qyear"][b]

            def older(y, d):
                if y.startswith("<="):
                    return y
                v = int(y) + d
                return "<=%d" % PK.OLDEST if v <= PK.OLDEST else str(v)
            for r in REGIONS:
                num = den = 0.0
                for (rr, y), ab in A[b].items():
                    y2 = older(y, dy) if not y.startswith("<=") else y
                    if rr != r or ab <= 0 or (r, y2) not in A[q].index:
                        continue
                    num += ab * S[q][(r, y2)] / A[q][(r, y2)]
                    den += S[b][(r, y)]
                out[r] = num / den - 1
    _CACHE[key] = (out, pw)
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


def growth(P, pan, q, b, how="per_card", mix="company", fern_ok=True, wfy=None, issuers="const", conv=True, jump=JUMP,
           book="issuer"):
    """card-visible growth of q over b: regional growth at the company's prior-year mix (or the panel's own)"""
    rg, pw = regional(P, pan, q, b, how, issuers, conv, fern_ok, jump, book)
    if mix == "company":
        w = company_weights(P, wfy or "FY%d" % (int(q[2:6]) - 1))
    elif mix == "rolled":
        w = rolled_weights(P, wfy or "FY%d" % (int(q[2:6]) - 1))
    else:
        t = sum(pw.values())
        w = {r: pw[r] / t for r in REGIONS}
    return sum(rg[r] * w[r] for r in REGIONS)


# ------------------------------------------------------------------------------ the company's quarters
def fern_both(P, q, b):
    return P["start"][q] >= ACQUIRED and P["start"][b] >= ACQUIRED


def net_sales(P, k, fern_ok=True):
    v = res_of(P, k, "net_sales")
    return v - (0.0 if fern_ok else res_of(P, k, "fern"))


def contract(P, k):
    return res_of(P, k, "contract")


def retail(P, k, fern_ok=True):
    return net_sales(P, k, fern_ok) - contract(P, k)


def payments(P, k, fern_ok=True):
    """what retail customers paid in the quarter: retail net sales plus the change in customer deposits"""
    return retail(P, k, fern_ok) + P["deposits"][k] - P["deposits"][prev_q(P, k)]


def organic_growth(P, q, b, fern_in_both):
    """reported net sales growth of q over b, weekly averages, Fernhollow taken out unless consolidated in both"""
    return (net_sales(P, q, fern_in_both) / weeks_of(P, q)) / (net_sales(P, b, fern_in_both) / weeks_of(P, b)) - 1


def ct_hat(P, q, rule="median8"):
    """contract sales for quarter q from the quarters reported before it"""
    keys = P["keys"]
    i = keys.index(q)
    hist = [contract(P, k) for k in keys[max(0, i - 8):i]]
    if rule == "median8":
        return float(np.median(hist))
    if rule == "median4":
        return float(np.median(hist[-4:]))
    if rule == "mean4":
        return float(np.mean(hist[-4:]))
    if rule == "mean8":
        return float(np.mean(hist))
    if rule == "last_year":
        return contract(P, keys[i - 4])
    raise ValueError(rule)


# ----------------------------------------------------------------------------------- revenue on delivery
def banner_profile(P, pan, q):
    """the panel's weekly spend at the brand's ids (stores and site, not Fernhollow) over quarter q's weeks, on the
    issuers present in every week of it, as shares of the quarter"""
    key = ("profile", pan.attrs.get("tok"), q)
    if key not in _CACHE:
        sub = pan[(pan.fq == q) & (pan.merchant_id != "M2290")]
        nw = sub.week_start.nunique()
        cov = sub.groupby("issuer_code").week_start.nunique()
        wk = sub[sub.issuer_code.isin(cov[cov == nw].index)].groupby("week_start").spend_usd.sum().sort_index()
        _CACHE[key] = (wk / wk.sum()).values
    return _CACHE[key]


def trailing(profile, L):
    """the share of a quarter's payments made in its last L weeks (L fractional)"""
    v = profile[::-1]
    n = int(np.floor(L))
    fr = L - n
    return float(v[:n].sum() + (fr * v[n] if n < len(v) else 0.0))


def custom_share(P, q, days=56):
    """the custom-order share of the brand's panel spend over the last `days` of quarter q, from the monthly descriptor
    detail (months weighted by their days in the window): the design studios and the site's custom orders against the
    brand ids less the licensed shops and cafes"""
    key = ("custom", q, days)
    if key not in _CACHE:
        d = P["desc"]
        end = P["end"][q]
        win = pd.date_range(end - pd.Timedelta(days=days - 1), end, freq="D")
        wts = pd.Series(1.0, index=win).groupby(win.strftime("%Y-%m")).sum()
        b = d[d.merchant_id.isin(["M0412", "M0413"]) & ~d.descriptor.str.contains(LICENSED, regex=True)]
        b = b[b.month.isin(wts.index)]
        mt = b[b.descriptor.str.contains(CUSTOM, regex=True)].groupby("month").spend_usd.sum()
        al = b.groupby("month").spend_usd.sum()
        w_ = pd.Series({m: wts[m] / pd.Period(m).days_in_month for m in wts.index})
        _CACHE[key] = float((mt.reindex(w_.index).fillna(0) * w_).sum() / (al.reindex(w_.index).fillna(0) * w_).sum())
    return _CACHE[key]


def deposit_weeks(P, k):
    """customer deposits at the quarter's end in weeks of the brand's payments that quarter"""
    return P["deposits"][k] / (payments(P, k, False) / weeks_of(P, k))


DEP_DAYS = {"mto": 56, "mto_7w": 49, "mto_9w": 63, "mto_q": 91}


def convert(P, q, b, x, fern_ok, rule="mto", pan=None):
    """net sales growth of q over b (retail, contract aside) from payments growth x: payments rebuilt from b's, the
    deposits at q's end estimated, net sales the payments less the change in deposits. Rules: mto (last year's deposits
    scaled by the brand's payments, the share of them in the last eight weeks and the custom-order share of those
    weeks; mto_7w, mto_9w and mto_q the same over seven weeks, nine weeks and the whole quarter), ratio (last year's
    deposits scaled by the payments), flat (the deposits' change a year earlier scaled by the payments, which is what
    growing last year's net sales at the payments' rate assumes), none (net sales grow with the payments)"""
    wq, wb = weeks_of(P, q), weeks_of(P, b)
    if rule == "none":
        rq = retail(P, b, fern_ok) / wb * (1 + x) * wq
        return (rq / wq) / (retail(P, b, fern_ok) / wb) - 1, dict(rev_q=rq, dep_change=None, pay_q=None, dep_q=None)
    pay_b = payments(P, b, fern_ok)
    pay_q = pay_b / wb * (1 + x) * wq
    bshare = payments(P, b, False) / pay_b
    bp_q, bp_b = pay_q * bshare, payments(P, b, False)
    q1 = prev_q(P, q)
    dep_b = P["deposits"][b]
    if rule in DEP_DAYS:
        L = DEP_DAYS[rule] / 7.0
        tq = trailing(banner_profile(P, pan, q), L)
        tb = trailing(banner_profile(P, pan, b), L)
        dep_q = dep_b * (bp_q * tq * custom_share(P, q, DEP_DAYS[rule])) / (bp_b * tb * custom_share(P, b, DEP_DAYS[rule]))
    elif rule == "ratio":
        dep_q = dep_b * bp_q / bp_b
    elif rule == "flat":
        dep_q = P["deposits"][q1] + (dep_b - P["deposits"][prev_q(P, b)]) * bp_q / bp_b
    else:
        raise ValueError(rule)
    chg = dep_q - P["deposits"][q1]
    rev_q = pay_q - chg
    return (rev_q / wq) / (retail(P, b, fern_ok) / wb) - 1, dict(pay_q=pay_q, dep_change=chg, rev_q=rev_q, dep_q=dep_q)


def to_total(P, q, b, g_ret, fern_ok, ct):
    """net sales growth of q over b: retail from its growth, contract from its run rate (ct), or the retail growth
    applied to all of net sales (ct None)"""
    if not ct:
        return g_ret
    wq, wb = weeks_of(P, q), weeks_of(P, b)
    tot_q = retail(P, b, fern_ok) / wb * (1 + g_ret) * wq + ct_hat(P, q, ct)
    return (tot_q / wq) / (net_sales(P, b, fern_ok) / wb) - 1


def origins_of(P, first="FY2022 Q1", last=None):
    keys = P["keys"]
    return keys[keys.index(first):(keys.index(last) + 1 if last else -1)]


def route(P, pan, how="per_card", mix="company", issuers="const", conv=True, dep="mto", ct="median8", reg=False,
          origins=None, wfy_lag=1, target=TQ, jump=JUMP, record_dep=None, book="issuer"):
    """the route's growth for the target quarter and its rolling-origin record: at each past quarter the same method on
    what was known then (the issuers and re-issued books seen by that quarter's end, the prior fiscal year's regional
    mix, the deposits estimated, contract from the quarters before); with reg, reported growth regressed on the route
    over the origins before it (six or more). record_dep: the deposits as later reported in the record (a look-ahead)"""
    keys = P["keys"]
    origins = origins or origins_of(P)
    bq = keys[keys.index(target) - 4]
    first_fy = int(P["regions"].fiscal_year.iloc[0][2:])
    wfy = lambda q: "FY%d" % max(int(q[2:6]) - wfy_lag, first_fy)

    def one(q, b, fo, dep_rule):
        x = growth(P, pan, q, b, how, mix, fo, wfy(q), issuers, conv, jump, book)
        g = x
        if dep_rule:
            g, _ = convert(P, q, b, x, fo, dep_rule, pan)
        return x, to_total(P, q, b, g, fo, ct), g
    fo_t = True
    pay_t, xt, gt = one(target, bq, fo_t, dep)
    if reg == "retail":
        # reported retail growth (net sales less contract) regressed on the route's retail growth over the origins
        # before the target; contract added at its run rate
        rx, ry = [], []
        errs = {}
        for q in origins:
            b = keys[keys.index(q) - 4]
            fo = fern_both(P, q, b)
            _, xq, gq = one(q, b, fo, dep)
            yr = (retail(P, q, fo) / weeks_of(P, q)) / (retail(P, b, fo) / weeks_of(P, b)) - 1
            if len(rx) >= 6:
                c = np.linalg.lstsq(np.column_stack([np.ones(len(rx)), rx]), ry, rcond=None)[0]
                errs[q] = float(to_total(P, q, b, c[0] + c[1] * gq, fo, ct) - organic_growth(P, q, b, fo))
            rx.append(float(gq))
            ry.append(float(yr))
        fit = np.linalg.lstsq(np.column_stack([np.ones(len(rx)), rx]), ry, rcond=None)[0]
        g = float(to_total(P, target, bq, fit[0] + fit[1] * gt, fo_t, ct))
        e = np.array(list(errs.values()))
        rmse = float(np.sqrt(np.mean(e ** 2)))
        asof = [abs(e[i]) <= Z80 * float(np.sqrt(np.mean(e[:i] ** 2))) for i in range(4, len(e))]
        asof6 = [abs(e[i]) <= Z80 * float(np.sqrt(np.mean(e[:i] ** 2))) for i in range(6, len(e))]
        return dict(growth=g, x=float(xt), pay_growth=float(pay_t), rmse=rmse, errs=errs, xs=rx, ys=ry, fit=fit,
                    origins=list(origins), inside=int(sum(abs(v) <= Z80 * rmse for v in e)), n=len(e),
                    inside_asof=int(sum(asof)), n_asof=len(asof), inside_asof6=int(sum(asof6)), n_asof6=len(asof6))
    xs, ys, errs = [], [], {}
    for q in origins:
        b = keys[keys.index(q) - 4]
        fo = fern_both(P, q, b)
        if record_dep == "actual":
            x = growth(P, pan, q, b, how, mix, fo, wfy(q), issuers, conv, jump, book)
            rev = payments(P, b, fo) / weeks_of(P, b) * (1 + x) * weeks_of(P, q) - (
                P["deposits"][q] - P["deposits"][prev_q(P, q)])
            g = (rev / weeks_of(P, q)) / (retail(P, b, fo) / weeks_of(P, b)) - 1
            x = to_total(P, q, b, g, fo, ct)
        else:
            _, x, _ = one(q, b, fo, dep)
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
    # the range as it could have been built at each quarter: the errors of the quarters before it (four or more)
    asof = [abs(e[i]) <= Z80 * float(np.sqrt(np.mean(e[:i] ** 2))) for i in range(4, len(e))]
    asof6 = [abs(e[i]) <= Z80 * float(np.sqrt(np.mean(e[:i] ** 2))) for i in range(6, len(e))]
    return dict(growth=g, x=float(xt), pay_growth=float(pay_t), rmse=rmse, errs=errs, xs=xs, ys=ys, fit=fit,
                origins=list(origins), inside=int(sum(abs(v) <= Z80 * rmse for v in e)), n=len(e),
                inside_asof=int(sum(asof)), n_asof=len(asof), inside_asof6=int(sum(asof6)), n_asof6=len(asof6))


def with_range(R, base):
    g, b = R["growth"], Z80 * R["rmse"]
    R.update(forecast=base * (1 + g), low=base * (1 + g - b), high=base * (1 + g + b), band=b)
    return R


def call_of(R, street):
    return "short" if R["high"] < street else ("long" if R["low"] > street else "no position")


# -------------------------------------------------------------------------------------------------------- the run
def run(tgt):
    P = load(tgt)
    keys = P["keys"]
    base = net_sales(P, BQ)
    est = P["street"].q4_fy2025_net_sales_usd_m
    street = float(np.mean(est))
    cf = completion_factors(P)
    pan = panel_entity(P, cf)
    out = dict(P=P, cf=cf, pan=pan, base=base, street=street, street_median=float(np.median(est)),
               street_n=int(len(est)))
    # the base quarter rebuilt from the releases: contract and Fernhollow by subtraction, the deposits
    q3fy24 = P["releases"]["FY2024 Q3"]
    q4fy24 = P["releases"][BQ]
    out.update(ct_fy2024=q4fy24["ct"][0] / 1000.0, ct_9m_fy2024=q3fy24["ct"][2] / 1000.0, ct_base=contract(P, BQ),
               fern_base=res_of(P, BQ, "fern"), retail_base=retail(P, BQ), dep_base=P["deposits"][BQ],
               dep_q3fy24=P["deposits"]["FY2024 Q3"], dep_q3=P["deposits"]["FY2025 Q3"],
               pay_base=payments(P, BQ, True))
    # the issuers: who reports in both quarters, and whose cards took a re-issued book
    out["reissues"] = reissues(P)
    sub = pan[pan.fq.isin([TQ, BQ])]
    out["issuers_both"] = issuers_for(P, sub, TQ, BQ, "const", conv=False)
    out["issuers_used"] = issuers_for(P, sub, TQ, BQ, "const", conv=True)
    cs = card_series(P)
    out["ks01_mw_cards"] = {str(k.date()): float(v) for k, v in cs[("KS-01", "Midwest")].items()
                            if pd.Timestamp("2025-09-21") <= k <= pd.Timestamp("2025-11-16")}
    # comparable growth by region, with and without KS-01's book, at the panel's mix and at the company's
    rg, pw = regional(P, pan, TQ, BQ)
    rg_in, _ = regional(P, pan, TQ, BQ, conv=False)
    cw = company_weights(P, "FY2024")
    tot = sum(pw.values())
    out.update(regional=rg, regional_with_ks01=rg_in, company_w=cw, panel_w={r: pw[r] / tot for r in REGIONS},
               g_idx=sum(rg[r] * cw[r] for r in REGIONS), g_pooled=sum(rg[r] * pw[r] / tot for r in REGIONS),
               g_idx_with_ks01=sum(rg_in[r] * cw[r] for r in REGIONS))
    # payments to net sales: the deposits at the quarter's end
    g_ret, cv = convert(P, TQ, BQ, out["g_idx"], True, "mto", pan)
    out.update(retail_growth=g_ret, retail_q4=cv["rev_q"], pay_q4=cv["pay_q"], dep_q4_est=cv["dep_q"],
               dep_change=cv["dep_change"], dep_change_base=P["deposits"][BQ] - P["deposits"]["FY2024 Q3"],
               custom_q=custom_share(P, TQ), custom_b=custom_share(P, BQ),
               trail_q=trailing(banner_profile(P, pan, TQ), 8.0), trail_b=trailing(banner_profile(P, pan, BQ), 8.0),
               dep_weeks={k: deposit_weeks(P, k) for k in keys[:-1]})
    # contract at its run rate
    out["ct_hat"] = ct_hat(P, TQ, "median8")
    out["ct_hist"] = {k: contract(P, k) for k in keys[:-1]}
    # the golden route, its record and range
    G = with_range(route(P, pan), base)
    out["golden"] = G
    out["growth"] = G["growth"]
    out["forecast"], out["range"] = G["forecast"], (G["low"], G["high"])
    out["call"] = call_of(G, street)
    # the entity and the immature weeks as figures
    d = P["desc"]
    days = pd.date_range(P["start"][TQ], P["end"][TQ], freq="D")
    qm = sorted(set(days.strftime("%Y-%m")))
    b = d[(d.merchant_id == "M0412") & d.month.isin(qm)]
    out["excluded_months"] = qm
    out["excluded_share"] = float(b[b.descriptor.str.contains(LICENSED, regex=True)].spend_usd.sum() / b.spend_usd.sum())
    raw_c = panel_entity(P, cf, complete=False)
    out["completion_uplift"] = float(pan[pan.fq == TQ].spend_usd.sum() / raw_c[raw_c.fq == TQ].spend_usd.sum() - 1)
    out["cf_last_week"] = {k[0]: v for k, v in cf.items() if k[1] == 0}
    out["bridge"], out["bridge_orders"] = bridge(out)
    return out


PANEL_STEPS = ("the latest weeks completed", "the licensed shops and cafes taken out",
               "issuers in every week of both quarters, spend per open card")
COMPANY_STEPS = ("the company's regional mix", "KS-01's re-issued book taken out", "revenue on delivery",
                 "contract at its run rate")


def bridge(out):
    """growth after each step from the delivered panel (every issuer, every merchant id, raw spend, the panel's own
    regional mix) to net sales: the panel's three steps (KS-01 kept, the panel's own mix) and the company's four, in the
    golden's order, and each step's worth under every order of its group"""
    import itertools
    P, cf = out["P"], out["cf"]

    def panel_state(S):
        pan = panel_entity(P, cf, complete="the latest weeks completed" in S,
                           exclude="the licensed shops and cafes taken out" in S)
        lfl = "issuers in every week of both quarters, spend per open card" in S
        rg, pw = regional(P, pan, TQ, BQ, "per_card" if lfl else "total", "const" if lfl else "all", False)
        t = sum(pw.values())
        return sum(rg[r] * pw[r] / t for r in REGIONS)

    _, pw_in = regional(P, out["pan"], TQ, BQ, conv=False)
    _, pw_ex = regional(P, out["pan"], TQ, BQ, conv=True)

    def company_state(S):
        conv = "KS-01's re-issued book taken out" in S
        rg, pw = (out["regional"], pw_ex) if conv else (out["regional_with_ks01"], pw_in)
        if "the company's regional mix" in S:
            w = out["company_w"]
        else:
            t = sum(pw.values())
            w = {r: pw[r] / t for r in REGIONS}
        x = sum(rg[r] * w[r] for r in REGIONS)
        if "revenue on delivery" in S:
            x, _ = convert(P, TQ, BQ, x, True, "mto", out["pan"])
        if "contract at its run rate" in S:
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
    out["g_pooled_with_ks01"] = cache[("company_state",)]
    return vals, orders


def family(out):
    """the golden family: defensible rivals of the golden route, each with its range"""
    P, pan, base = out["P"], out["pan"], out["base"]
    F = {"the golden route": out["golden"]}
    F["spend per open card issuer by issuer"] = with_range(route(P, pan, how="lfl"), base)
    F["cards of the same age"] = with_range(route(P, pan, how="same_age"), base)
    F["the regional mix of fiscal 2023"] = with_range(route(P, pan, wfy_lag=2), base)
    F["fiscal 2024's regional mix rolled forward a year"] = with_range(route(P, pan, mix="rolled"), base)
    F["the deposit window at seven weeks"] = with_range(route(P, pan, dep="mto_7w"), base)
    F["the deposit window at nine weeks"] = with_range(route(P, pan, dep="mto_9w"), base)
    F["contract at the median of the last four quarters"] = with_range(route(P, pan, ct="median4"), base)
    F["a re-issued book read at a three per cent rise"] = with_range(route(P, pan, jump=0.03), base)
    F["a re-issued book read at a ten per cent rise"] = with_range(route(P, pan, jump=0.10), base)
    F["the record from fiscal 2023 only"] = with_range(route(P, pan, origins=origins_of(P, "FY2023 Q1")), base)
    # other ways to set a re-issued book aside, the same way at every origin of the record (KS-02 in fiscal 2023 to
    # 2024, KS-01 at the end): the region whose cards jumped, the newest open years, or the issuer in every quarter
    F["the re-issued book's region set aside"] = with_range(route(P, pan, book="region"), base)
    F["the re-issued book's newest open years set aside"] = with_range(route(P, pan, book="newest"), base)
    F["an issuer with a re-issued book left out of every quarter"] = with_range(route(P, pan, book="always"), base)
    F["retail growth calibrated by regression on past quarters, contract at its run rate"] = with_range(
        route(P, pan, reg="retail"), base)
    return F


def rivals_ruled_out(out):
    """rivals the data rule out, run to show where they land"""
    P, pan, base = out["P"], out["pan"], out["base"]
    R = {}
    R["raw spend on the issuers in both quarters"] = with_range(route(P, pan, how="total"), base)
    R["deposits at last year's ratio to payments"] = with_range(route(P, pan, dep="ratio"), base)
    R["the deposits' change moved as a year earlier"] = with_range(route(P, pan, dep="flat"), base)
    R["the custom-order share over the whole quarter"] = with_range(route(P, pan, dep="mto_q"), base)
    R["contract at the mean of the last four quarters, last year's contract included"] = with_range(
        route(P, pan, ct="mean4"), base)
    R["contract at last year's fourth quarter"] = with_range(route(P, pan, ct="last_year"), base)
    R["KS-01 kept"] = with_range(route(P, pan, conv=False), base)
    R["the chain calibrated by regression on past quarters"] = with_range(route(P, pan, reg=True), base)
    return R


def shortcuts(out):
    """the hurried routes: what each files for the quarter, with its own record and range"""
    P, pan, base, cf = out["P"], out["pan"], out["base"], out["cf"]
    S = {}
    # the careful but hurried pass: the textbook panel work and the company's mix, then net sales grown with it
    S["careful"] = with_range(route(P, pan, conv=False, dep=None, ct=None), base)
    S["careful_regressed"] = with_range(route(P, pan, conv=False, dep=None, ct=None, reg=True), base)
    # one deep step at a time on top of the careful pass, and every pair
    S["only_reissue"] = with_range(route(P, pan, conv=True, dep=None, ct=None), base)
    S["only_deposits"] = with_range(route(P, pan, conv=False, dep="mto", ct=None), base)
    S["only_contract"] = with_range(route(P, pan, conv=False, dep=None, ct="median8"), base)
    S["no_reissue"] = with_range(route(P, pan, conv=False), base)
    S["no_deposits"] = with_range(route(P, pan, dep=None), base)
    S["no_contract"] = with_range(route(P, pan, ct=None), base)
    S["deposit_ratio"] = with_range(route(P, pan, dep="ratio"), base)
    S["deposit_flat"] = with_range(route(P, pan, dep="flat"), base)
    S["contract_last_year"] = with_range(route(P, pan, ct="last_year"), base)
    S["panel_mix"] = with_range(route(P, pan, mix="panel"), base)
    inc_pan = panel_entity(P, cf, complete=True, exclude=False)
    S["desk_model"] = with_range(route(P, inc_pan, mix="panel", conv=False, dep=None, ct=None, reg=True), base)
    keys = P["keys"]
    S["trend"] = with_range(trend_route(P), base)
    p0 = panel_entity(P, cf, complete=False, exclude=False)
    S["quick"] = dict(growth=growth(P, p0, TQ, BQ, "total", "panel", True, None, "const", False))
    S["quick"]["forecast"] = base * (1 + S["quick"]["growth"])
    S["delivered"] = dict(growth=growth(P, p0, TQ, BQ, "total", "panel", True, None, "all", False))
    S["delivered"]["forecast"] = base * (1 + S["delivered"]["growth"])
    out["organic"] = {q: organic_growth(P, q, keys[keys.index(q) - 4], fern_both(P, q, keys[keys.index(q) - 4]))
                      for q in origins_of(P)}
    return S


def trend_route(P):
    """reported growth carried: the mean of the last three quarters' year-on-year growth, with the same rule's record"""
    keys = P["keys"]

    def yoy(k):
        b = keys[keys.index(k) - 4]
        return organic_growth(P, k, b, fern_both(P, k, b))

    def forecast(q):
        prev = keys[keys.index(q) - 3:keys.index(q)]
        return float(np.mean([yoy(k) for k in prev]))
    errs = {q: forecast(q) - yoy(q) for q in origins_of(P, "FY2022 Q4")}
    e = np.array(list(errs.values()))
    return dict(growth=forecast(TQ), rmse=float(np.sqrt(np.mean(e ** 2))), errs=errs, n=len(e),
                inside=int(sum(abs(v) <= Z80 * np.sqrt(np.mean(e ** 2)) for v in e)))


def variants(out):
    """each supporting result's rivals, for its band"""
    P, cf, pan = out["P"], out["cf"], out["pan"]
    V = {}
    raw_c = panel_entity(P, cf, complete=False)
    tot_raw = raw_c[raw_c.fq == TQ].spend_usd.sum()
    for name, kw in (("mean factors", dict(stat="mean")), ("the last thirteen deliveries", dict(last_n=13))):
        c2 = completion_factors(P, **kw)
        p2 = panel_entity(P, c2)
        V.setdefault("completion", {})[name] = float(p2[p2.fq == TQ].spend_usd.sum() / tot_raw - 1)
    V["regional"] = {}
    for how in ("lfl", "same_age"):
        rg, _ = regional(P, pan, TQ, BQ, how)
        V["regional"][how] = rg
    rg = out["regional"]
    V["visible"] = {"fiscal 2024 mix": out["g_idx"],
                    "fiscal 2023 mix": sum(rg[r] * company_weights(P, "FY2023")[r] for r in REGIONS),
                    "fiscal 2024 mix rolled forward": sum(rg[r] * rolled_weights(P, "FY2024")[r] for r in REGIONS)}
    for how in ("lfl", "same_age"):
        V["visible"]["%s at fiscal 2024 mix" % how] = sum(V["regional"][how][r] * out["company_w"][r] for r in REGIONS)
    V["dep_q4"], V["dep_points"] = {}, {}
    for rule in ("mto", "mto_7w", "mto_9w"):
        for vk, vg in V["visible"].items():
            g, cv = convert(P, TQ, BQ, vg, True, rule, pan)
            V["dep_q4"]["%s, %s" % (rule, vk)] = cv["dep_q"]
            V["dep_points"]["%s, %s" % (rule, vk)] = g - vg
    V["ct_hat"] = {r: ct_hat(P, TQ, r) for r in ("median8", "median4", "mean8", "mean4", "last_year")}
    V["reissue_jump"] = {j: issuers_for(P, pan[pan.fq.isin([TQ, BQ])], TQ, BQ, "const", True, j)
                         for j in (0.02, 0.03, 0.05, 0.08, 0.10, 0.12)}
    return V


def incumbent(out):
    """the desk's third-quarter model as its workbook states it: spend per open card on the issuers in both quarters,
    the brand ids as delivered, reported growth regressed on it over the quarters to the second quarter of fiscal 2025"""
    P, cf = out["P"], out["cf"]
    inc_pan = panel_entity(P, cf, complete=True, exclude=False)
    org = origins_of(P, "FY2022 Q1", "FY2025 Q2")
    R = route(P, inc_pan, mix="panel", conv=False, dep=None, ct=None, reg=True, target="FY2025 Q3", origins=org)
    q3_base = net_sales(P, "FY2024 Q3")
    return dict(rows=list(zip(org, R["xs"], R["ys"])), fit=R["fit"], rmse=R["rmse"], errs=R["errs"], x_q3=R["x"],
                g_q3=R["growth"], q3_base=q3_base, q3_forecast=q3_base * (1 + R["growth"]),
                q3_actual=net_sales(P, "FY2025 Q3"))


def perturbations(out):
    """each fitted or stated input moved by its defensible spread; the value is the top of the golden's 80 per cent range"""
    P, pan, base = out["P"], out["pan"], out["base"]
    res = {}
    for f in (0.97, 1.03):
        cf = {k: min(1.0, v * f) if k[1] == 0 else v for k, v in out["cf"].items()}
        res["the last week's completeness %+d per cent" % round(100 * (f - 1))] = with_range(
            route(P, panel_entity(P, cf)), base)["high"]
    for f in (0.8, 1.2):
        res["the licensed shops' and cafes' share %+d per cent" % round(100 * (f - 1))] = with_range(
            route(P, panel_entity(P, out["cf"], share_scale=f)), base)["high"]
    G = out["golden"]
    e = np.array(list(G["errs"].values()))
    res["the range from the record's 10th and 90th percentile errors"] = base * (1 + G["growth"] - float(np.quantile(e, 0.1)))
    res["the record's mean error added back, the range from its standard deviation"] = base * (
        1 + G["growth"] - float(e.mean()) + Z80 * float(e.std()))
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
