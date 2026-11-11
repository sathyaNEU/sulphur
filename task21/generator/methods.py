"""The analysis, read only from target/: each step a function the golden, the hurried passes and the checks share.

Every function takes the loaded pack (load()) and returns plain numbers or frames; nothing here reads the
generator's world. The constants are the planning paper's (PLN-2027-03) and the commission schedule's.
"""
import datetime as dt
import json
import os
import re
import subprocess
import zoneinfo

import numpy as np
import pandas as pd

LONDON = zoneinfo.ZoneInfo("Europe/London")
AS_AT = dt.date(2026, 10, 31)
TRI_AT = dt.date(2026, 9, 30)
CURRENT_FROM = dt.date(2026, 2, 1)          # PLN-2027-03 4.1: the 2027 quotes are those since 1 February 2026
SCALE = 12 / 9.0                            # ... scaled to twelve months
TARGET = 0.75                               # 5.1
INFL = 0.055                                # 2.2
MARKET = 0.02                               # 4.2
CAP = 100000.0                              # 2.1
SERVICING = 34.0                            # 6.1
SEGS = ("u25", "mid", "o65")
TYPES = {"Accidental damage": "AD", "Third party property": "TPPD", "Third party injury": "TPBI", "Theft": "THEFT",
         "Windscreen": "WS"}


def seg_of(age):
    a = np.asarray(age)
    return np.where(a < 25, "u25", np.where(a < 65, "mid", "o65"))


# ---- loading and conforming ---------------------------------------------------------------------------------------
def _find(target, prefix):
    for f in sorted(os.listdir(target)):
        if f.startswith(prefix):
            return os.path.join(target, f)
    raise FileNotFoundError(prefix)


def load_feeds(target, drop_tests=True):
    kc = pd.read_csv(_find(target, "kitecompare"))
    kc = pd.DataFrame({"site": "Kitecompare", "ref": kc.quote_ref, "local": pd.to_datetime(kc.quote_time_local),
                       "age": kc.main_driver_age, "district": kc.postcode_district, "gross": kc.halvergate_premium_gbp,
                       "pos": kc.halvergate_position, "panel": kc.panel_size, "r1": kc.rival_1_gbp,
                       "r2": kc.rival_2_gbp, "r3": kc.rival_3_gbp, "w": kc.extract_weight})
    rows = [json.loads(l) for l in open(_find(target, "covertide"))]
    ct = pd.DataFrame({"site": "Covertide", "ref": [r["ref"] for r in rows],
                       "local": pd.to_datetime([r["ts"] for r in rows], unit="ms", utc=True).tz_convert(LONDON)
                       .tz_localize(None), "age": [r["risk"]["age"] for r in rows],
                       "district": [r["risk"]["postcode"] for r in rows], "gross": [r["quotedPremium"] for r in rows],
                       "pos": [r["rank"] for r in rows], "panel": [r["panel"] for r in rows],
                       "r1": [r["top3"][0] for r in rows], "r2": [r["top3"][1] for r in rows],
                       "r3": [r["top3"][2] for r in rows], "w": [r["weight"] for r in rows]})
    ct = ct.drop_duplicates("ref", keep="first")
    bq = pd.read_csv(_find(target, "brightquote"), sep=";")
    bq = pd.DataFrame({"site": "Brightquote", "ref": bq.QuoteID,
                       "local": pd.to_datetime(bq.QuoteDate, format="%d/%m/%Y %H:%M"), "age": bq.DriverAge,
                       "district": bq.PostcodeDistrict, "gross": bq.PremiumPence / 100.0, "pos": bq.Rank,
                       "panel": bq.PanelSize, "r1": bq.Comp1Pence / 100.0, "r2": bq.Comp2Pence / 100.0,
                       "r3": bq.Comp3Pence / 100.0, "w": bq.Weight})
    pl = pd.read_csv(_find(target, "pricelark"))
    pl = pd.DataFrame({"site": "Pricelark", "ref": pl.reference,
                       "local": pd.to_datetime(pl.created_utc, utc=True).dt.tz_convert(LONDON).dt.tz_localize(None),
                       "age": pl.age, "district": pl.district, "gross": pl.price, "pos": pl.position,
                       "panel": pl.brands_quoting, "r1": pl.cheapest_other, "r2": pl.second_other,
                       "r3": pl.third_other, "w": pl.sampling_weight})
    f = pd.concat([kc, ct, bq, pl], ignore_index=True)
    if drop_tests:
        f = f[f.district != "ZZ99"]                         # the sites' monitoring quotes
    f = f.copy()
    f["date"] = f.local.dt.date
    f["seg"] = seg_of(f.age.values)
    f["gap"] = np.log(f.gross / f.r1)
    return f.reset_index(drop=True)


def load_policies(target):
    p = pd.read_csv(_find(target, "pcw_nb_policies"), keep_default_na=False, na_values=[""])
    for c in ("inception_date", "expiry_date", "cancelled_on"):
        p[c] = pd.to_datetime(p[c]).dt.date
    p["seg"] = seg_of(p.main_driver_age.values)
    p["cancelled_on"] = [c if pd.notna(c) else None for c in p.cancelled_on]
    p["end"] = [min(c, e) if c is not None else e for c, e in zip(p.cancelled_on, p.expiry_date)]
    return p


def load_claims(target):
    c = pd.read_csv(_find(target, "motor_claims_extract"), keep_default_na=False, na_values=[""])
    c["accident_date"] = pd.to_datetime(c.accident_date).dt.date
    c["notified_date"] = pd.to_datetime(c.notified_date).dt.date
    c["type"] = c.claim_type.map(TYPES)
    c["capped"] = np.minimum(c.incurred_gbp, CAP)
    return c


def load_triangles(target):
    path = _find(target, "reserving_triangles")
    out = {}
    for t in TYPES.values():
        for kind in ("notified", "incurred"):
            df = pd.read_excel(path, sheet_name="%s %s" % (t, kind))
            out[(t, kind)] = df.set_index("Accident quarter")
    return out


def load_renewals(target):
    return pd.read_csv(_find(target, "renewal_schedule"))


def load_retention(target):
    r = pd.read_excel(_find(target, "renewal_retention_mi"), sheet_name="Renewal invitations")
    lo = r["Price change on last year"].str.extract(r"([+-]?\d+)%")[0].astype(float) / 100.0
    r["mid"] = lo + 0.01
    return r


def load_rates(target):
    r = pd.read_excel(_find(target, "pcw_rate_change_log"))
    r["Effective"] = pd.to_datetime(r["Effective"]).dt.date
    r["seg"] = r["Main driver age"].map({"under 25": "u25", "25 to 64": "mid", "65 and over": "o65"})
    return r


def load_commissions(target):
    txt = subprocess.run(["pdftotext", "-layout", _find(target, "PCW-COM-2026"), "-"], capture_output=True,
                         text=True).stdout
    out = {}
    for site in ("Kitecompare", "Covertide", "Brightquote", "Pricelark"):
        m = re.search(site + r"\s+£([0-9.]+)", txt)
        out[site] = float(m.group(1))
    return out


def load(target):
    return dict(feeds=load_feeds(target), pol=load_policies(target), clm=load_claims(target),
                tri=load_triangles(target), ren=load_renewals(target), ret=load_retention(target),
                rates=load_rates(target), comm=load_commissions(target))


# ---- development ---------------------------------------------------------------------------------------------------
def quarter_label(d):
    return "%dQ%d" % (d.year, (d.month - 1) // 3 + 1)


def cdfs(tri, kind="incurred", exclude_last=0):
    """Volume-weighted chain-ladder factors by claim type: CDF to ultimate at each development quarter."""
    out = {}
    for t in TYPES.values():
        m = tri[(t, kind)].astype(float).values
        n = m.shape[1]
        f = np.ones(n)
        for j in range(n - 1):
            col, nxt = m[:, j], m[:, j + 1]
            ok = ~np.isnan(col) & ~np.isnan(nxt)
            if exclude_last and ok.sum() > exclude_last:
                ok[np.where(ok)[0][-exclude_last:]] = False
            f[j] = nxt[ok].sum() / max(col[ok].sum(), 1e-9) if ok.sum() else 1.0
        cdf = np.cumprod(f[::-1])[::-1]
        out[t] = cdf
    return out


def dev_age(acc_date):
    """Development quarter (1 = the accident quarter) of an accident date at the triangles' 30 September 2026."""
    q_acc = acc_date.year * 4 + (acc_date.month - 1) // 3
    q_tri = TRI_AT.year * 4 + (TRI_AT.month - 1) // 3
    return q_tri - q_acc + 1


def report_pattern(clm, mature_to=dt.date(2025, 10, 31)):
    """Each claim type's share of claims notified within each lag (days), read on accidents old enough that every
    lag up to a year has been seen."""
    out = {}
    for t in TYPES.values():
        c = clm[(clm.type == t) & (clm.accident_date <= mature_to)]
        lag = np.array([(n - a).days for a, n in zip(c.accident_date, c.notified_date)])
        lag = np.sort(lag[lag <= 365])
        out[t] = lag
    return out


def reported_share(pattern, t, days):
    lag = pattern[t]
    return np.searchsorted(lag, np.asarray(days), side="right") / len(lag)


def mature_severity(clm, mature_to=dt.date(2025, 10, 31)):
    """Each claim type's mean capped incurred per reported claim, read on accidents a full year old."""
    m = clm[clm.accident_date <= mature_to]
    return m.groupby("type").capped.mean().to_dict()


def developed(clm, pattern, as_at=AS_AT):
    """Claims to ultimate: each reported claim at its capped incurred (case estimates at face), and the claims of its
    type not yet notified at its age (one over the share notified by then, less the claim itself) at the type's
    mean cost, so a young large claim is counted once and not multiplied."""
    age = np.array([(as_at - a).days for a in clm.accident_date])
    share = np.array([max(reported_share(pattern, t, a), 0.05) for t, a in zip(clm.type, age)])
    sev = mature_severity(clm)
    out = clm.copy()
    out["dev_cost"] = out.capped + (1.0 / share - 1.0) * clm.type.map(sev).values
    out["dev_count"] = 1.0 / share
    return out


def cdf_at(cdf, x):
    """A chain-ladder CDF read at a fractional development age in quarters (1 = the end of the accident quarter),
    log-linear between quarter ends and along the first step below the first."""
    n = len(cdf)
    lc = np.log(np.maximum(cdf, 1.0))
    x = np.clip(x, 0.0, n)
    j = np.clip(np.floor(x).astype(int), 1, n - 1)
    lo, hi = lc[j - 1], lc[np.minimum(j, n - 1)]
    return np.exp(lo + (hi - lo) * (x - j))


def developed_cl(clm, cdf_inc, cdf_cnt, as_at=AS_AT):
    """The rival: the triangles' chain-ladder factors, each claim's accident quarter read at its own age on the as-at
    date: the notified-count factor for the claims still to come (at the type's mean cost), and the incurred factor
    over the count factor for the movement on the claims already notified."""
    qs = [dt.date(d.year, 3 * ((d.month - 1) // 3) + 1, 1) for d in clm.accident_date]
    x = np.array([((as_at + dt.timedelta(days=1)) - q).days / 91.3125 for q in qs])
    f_inc, f_cnt = np.ones(len(clm)), np.ones(len(clm))
    for t in set(clm.type):
        m = (clm.type == t).values
        f_inc[m] = cdf_at(cdf_inc[t], x[m])
        f_cnt[m] = cdf_at(cdf_cnt[t], x[m])
    sev = mature_severity(clm)
    out = clm.copy()
    out["dev_cost"] = out.capped * f_inc / f_cnt + (f_cnt - 1.0) * clm.type.map(sev).values
    out["dev_count"] = f_cnt
    return out


# ---- earned exposure by calendar month ------------------------------------------------------------------------------
MONTHS = [dt.date(y, m, 1) for y in (2025, 2026) for m in range(1, 13) if dt.date(y, m, 1) <= AS_AT]


def month_exposure(pol, upto=AS_AT):
    """Vehicle-years each policy earns in each calendar month to the as-at date (policies x months)."""
    s = np.array([d.toordinal() for d in pol.inception_date])
    e = np.array([min(d, upto + dt.timedelta(days=1)).toordinal() for d in pol.end])
    b = [m.toordinal() for m in MONTHS] + [dt.date(2026, 11, 1).toordinal()]
    lo = np.maximum(s[:, None], np.array(b[:-1])[None, :])
    hi = np.minimum(e[:, None], np.array(b[1:])[None, :])
    return np.clip(hi - lo, 0, None) / 365.0


def seasonal_factors(pol, clm_dev, expo, weight="cost", last=dt.date(2026, 9, 1)):
    """Each calendar month's claims per vehicle-year against the year's average (2025 and 2026 months pooled, the
    as-at month left out as too young)."""
    cm = np.array([(d.year, d.month) for d in clm_dev.accident_date])
    val = clm_dev.dev_cost.values if weight == "cost" else clm_dev.dev_count.values
    pidx = {p: k for k, p in enumerate(pol.policy_number)}
    rate = np.zeros(12)
    ex = np.zeros(12)
    num = np.zeros(12)
    for k, m in enumerate(MONTHS):
        if m > last:
            continue
        sel = (cm[:, 0] == m.year) & (cm[:, 1] == m.month)
        num[m.month - 1] += val[sel].sum()
        ex[m.month - 1] += expo[:, k].sum() if weight == "count" else (expo[:, k] * pol.written_premium_gbp.values).sum()
    rate = num / ex
    return rate / (rate * ex).sum() * ex.sum()       # exposure-weighted mean of 1


# ---- the base: the current book over a full year ----------------------------------------------------------------------
def claims_by_policy(pol, clm_dev):
    g = clm_dev.groupby("policy_number")
    cost = g.dev_cost.sum()
    cnt = g.dev_count.sum()
    return (pol.policy_number.map(cost).fillna(0.0).values, pol.policy_number.map(cnt).fillna(0.0).values)


def base_lr(pol, clm_dev, expo, s_cost, mask, seasonal=True):
    cost, _ = claims_by_policy(pol, clm_dev)
    ep = expo * pol.written_premium_gbp.values[:, None]
    w = np.array([s_cost[m.month - 1] for m in MONTHS]) if seasonal else np.ones(len(MONTHS))
    return cost[mask].sum() / (ep[mask] * w[None, :]).sum()


# ---- the won book's selection ---------------------------------------------------------------------------------------
def sales_frame(feeds, pol):
    sold = feeds[feeds.w == 1][["ref", "site", "date", "seg", "gross", "pos", "r1", "r2", "r3", "gap"]]
    m = pol.merge(sold, left_on="quote_reference", right_on="ref", how="inner", suffixes=("", "_q"))
    return m


def ae_frame(pol, clm_dev, expo, s_cnt, sales, upto=dt.date(2026, 9, 30)):
    """Each sale's claims against its predicted claims, to 30 September 2026 (the as-at month too young to count)."""
    _, cnt = claims_by_policy(pol, clm_dev[[a <= upto for a in clm_dev.accident_date]])
    w = np.array([s_cnt[m.month - 1] if m <= upto else 0.0 for m in MONTHS])
    exp_cnt = pol.predicted_claim_frequency.values * (expo * w[None, :]).sum(1)
    pidx = pd.Series(np.arange(len(pol)), index=pol.policy_number)
    j = pidx.loc[sales.policy_number].values
    out = sales.copy()
    out["cnt"] = cnt[j]
    out["exp_cnt"] = exp_cnt[j]
    return out


def gap_curve(af, form="loglinear", bins=10, clip=True):
    """Claims per predicted claim against the price gap to the cheapest rival."""
    a = af[af.exp_cnt > 0]
    q = np.quantile(a.gap, np.linspace(0, 1, bins + 1))
    b = np.clip(np.digitize(a.gap, q[1:-1]), 0, bins - 1)
    x = np.array([a.gap.values[b == k].mean() for k in range(bins)])
    y = np.array([a.cnt.values[b == k].sum() / a.exp_cnt.values[b == k].sum() for k in range(bins)])
    wts = np.array([a.exp_cnt.values[b == k].sum() for k in range(bins)])
    if form == "loglinear":
        A = np.polyfit(x, np.log(y), 1, w=np.sqrt(wts))
        return (lambda g: np.exp(np.polyval(A, np.clip(g, x.min(), x.max())))), dict(slope=A[0], x=x, y=y)
    if form == "poisson":
        gx, c, e = a.gap.values, a.cnt.values, a.exp_cnt.values
        p = np.array([np.log(c.sum() / e.sum()), 0.0])
        for _ in range(50):
            mu = e * np.exp(p[0] + p[1] * gx)
            grad = np.array([(c - mu).sum(), ((c - mu) * gx).sum()])
            H = np.array([[mu.sum(), (mu * gx).sum()], [(mu * gx).sum(), (mu * gx * gx).sum()]])
            step = np.linalg.solve(H, grad)
            p = p + step
            if np.abs(step).max() < 1e-10:
                break
        lo, hi = (np.quantile(gx, 0.005), np.quantile(gx, 0.995)) if clip else (-np.inf, np.inf)
        return (lambda g: np.exp(p[0] + p[1] * np.clip(g, lo, hi))), dict(slope=p[1], x=x, y=y)
    edges = q

    def step(g):
        k = np.clip(np.digitize(g, edges[1:-1]), 0, bins - 1)
        return y[k]
    return step, dict(x=x, y=y)


def conversion_by_rank(feeds, seg, start=CURRENT_FROM, end=AS_AT):
    f = feeds[(feeds.seg == seg) & (feeds.date >= start) & (feeds.date <= end)]
    r = np.minimum(f.pos.values, 4)
    out = {}
    for k in (1, 2, 3, 4):
        m = r == k
        out[k] = (f.w.values[m] == 1).sum() / f.w.values[m].sum()
    return out


def new_rank(gross, r1, r2, r3, L, move=MARKET):
    p = gross * (1 + L)
    return np.where(p < r1 * (1 + move), 1, np.where(p < r2 * (1 + move), 2, np.where(p < r3 * (1 + move), 3, 4)))


def lr_2027(base, cur, curve, conv, L, move=MARKET):
    """The 2027 loss ratio of the business a change L would win: the current sold book reweighted by each quote's
    conversion at its new rank, its claims per predicted claim read off the gap curve at the quote's own gap."""
    r0 = np.minimum(cur.pos.values, 4)
    r1_ = new_rank(cur.gross.values, cur.r1.values, cur.r2.values, cur.r3.values, L, move)
    v = np.array([conv[k] for k in r1_]) / np.array([conv[k] for k in r0])
    ae = curve(cur.gap.values)
    pred = cur.risk_premium_gbp.values
    net = cur.written_premium_gbp.values
    rel = ((v * pred * ae).sum() / (v * net).sum()) / ((pred * ae).sum() / net.sum())
    return base * rel * (1 + INFL) / (1 + L)


def smallest_change(fn, lo=0, hi=60):
    for k in range(lo, hi + 1):
        if fn(k / 100.0) <= TARGET + 1e-12:
            return k
    return None


def volumes(feeds, seg, conv, L, move=MARKET):
    f = feeds[(feeds.seg == seg) & (feeds.date >= CURRENT_FROM)]
    rk = new_rank(f.gross.values, f.r1.values, f.r2.values, f.r3.values, L, move)
    pr = np.array([conv[k] for k in rk])
    sales = (f.w.values * pr).sum() * SCALE
    prem = (f.w.values * pr * f.gross.values / 1.12 * (1 + L)).sum() * SCALE
    return sales, prem
