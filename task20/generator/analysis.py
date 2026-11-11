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
    P = {}
    res = pd.read_csv(os.path.join(tgt, PK.F_RESULTS))
    res["period_start"] = pd.to_datetime(res.period_start)
    res["period_end"] = pd.to_datetime(res.period_end)
    P["results"] = res
    P["regions"], P["pl"] = filing_tables(os.path.join(tgt, DC.F_FILING))
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
    pl = {}
    for fy, q, v in re.findall(r"Fiscal (\d{4}) Q(\d)\s+(\d+\.\d)", txt):
        pl["FY%s Q%s" % (fy, q)] = float(v)
    return reg, pl


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


def origins_of(P, first="FY2022 Q1", last=None):
    keys = P["keys"]
    return keys[keys.index(first):(keys.index(last) + 1 if last else -1)]


def route(P, pan, how="tenure", mix="company", drift=True, reg=False, plrule="pace", origins=None, bt_plrule=None,
          wfy_lag=1, other=None, target=TQ):
    """the route's growth for the target quarter and its rolling-origin record: at each past quarter the same method
    on what was known then (the prior fiscal year's regional mix, the private-label rule on the quarters reported
    before it); with reg, reported growth regressed on the chain over the origins before it (six or more)"""
    keys = P["keys"]
    origins = origins or origins_of(P)
    bq = keys[keys.index(target) - 4]
    first_fy = int(P["regions"].fiscal_year.iloc[0][2:])
    wfy = lambda q: "FY%d" % max(int(q[2:6]) - wfy_lag, first_fy)
    xt = growth(P, pan, target, bq, how, mix, drift, fern_both(P, target, bq) or target == TQ, plrule, wfy(target), other)
    xs, ys, errs = [], [], {}
    for q in origins:
        b = keys[keys.index(q) - 4]
        fo = fern_both(P, q, b)
        x = growth(P, pan, q, b, how, mix, drift, fo, bt_plrule or plrule, wfy(q), other)
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
    return dict(growth=g, x=float(xt), rmse=rmse, errs=errs, xs=xs, ys=ys, fit=fit, origins=list(origins),
                inside=int(sum(abs(v) <= Z80 * rmse for v in e)), n=len(e))


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
    # R3 and R4: comparable growth by region and at the company's mix
    rg, pw = regional(P, pan, TQ, BQ, "tenure")
    cw = company_weights(P, "FY2024")
    tot = sum(pw.values())
    out.update(regional=rg, company_w=cw, panel_w={r: pw[r] / tot for r in REGIONS},
               g_idx=sum(rg[r] * cw[r] for r in REGIONS), g_pooled=sum(rg[r] * pw[r] / tot for r in REGIONS))
    # R5: the private-label card's fourth-quarter share and the bank-card share's change
    pl = P["pl"]
    out["pl_target"] = pl_target(pl, keys, TQ, "pace")
    out["drift"] = bank_share(pl[BQ]) / bank_share(out["pl_target"])
    # R6 and R7: the golden route, its record and range
    G = with_range(route(P, pan), base)
    out["golden"] = G
    out["growth"] = G["growth"]
    out["forecast"], out["range"] = G["forecast"], (G["low"], G["high"])
    out["call"] = call_of(G, street)
    # R1 and R2 as figures
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
    # R3 and R8: the bridge, in the order the panel is processed
    p0 = panel_entity(P, cf, complete=False, exclude=False)
    p1 = panel_entity(P, cf, complete=True, exclude=False)
    g0 = growth(P, p0, TQ, BQ, "all_issuers", "panel", False)
    g1 = growth(P, p1, TQ, BQ, "all_issuers", "panel", False)
    g2 = growth(P, pan, TQ, BQ, "all_issuers", "panel", False)
    g3, g4, g5 = out["g_pooled"], out["g_idx"], G["growth"]
    out["bridge"] = [("the delivered panel, every issuer", g0), ("the latest weeks completed", g1 - g0),
                     ("the licensed shops and cafes taken out", g2 - g1),
                     ("issuers in both years, cards of the same age", g3 - g2), ("the company's regional mix", g4 - g3),
                     ("the bank-card share of net sales", g5 - g4)]
    # the bridge's order rivals: the steps applied in the reverse order where the order can move them
    g1b = growth(P, panel_entity(P, cf, complete=False, exclude=True), TQ, BQ, "all_issuers", "panel", False)
    gd = (1 + g3) * out["drift"] - 1
    out["bridge_rivals"] = {"the licensed shops and cafes taken out": g1b - g0, "the latest weeks completed": g2 - g1b,
                            "the bank-card share of net sales": gd - g3, "the company's regional mix": g5 - gd}
    return out


def family(out):
    """the golden family: defensible rivals of the golden route, each with its range"""
    P, pan, base = out["P"], out["pan"], out["base"]
    F = {"the golden route": out["golden"]}
    for rule, name in (("yoy", "private-label share carried by the third quarter's year-on-year change"),
                       ("line", "private-label share on a straight line through fiscal 2025's three quarters"),
                       ("last", "private-label share carried at the third quarter's own change")):
        F[name] = with_range(route(P, pan, plrule=rule), base)
    F["the regional mix of fiscal 2023"] = with_range(route(P, pan, wfy_lag=2), base)
    F["fiscal 2024's regional mix rolled forward a year"] = with_range(route(P, pan, mix="rolled"), base)
    F["the chain calibrated by regression on past quarters"] = with_range(route(P, pan, reg=True), base)
    F["the record from fiscal 2023 only"] = with_range(route(P, pan, origins=origins_of(P, "FY2023 Q1")), base)
    return F


def rivals_ruled_out(out):
    """rivals the data rule out, run to show where they land"""
    P, pan, base = out["P"], out["pan"], out["base"]
    R = {}
    R["spend per card instead of cards of the same age"] = with_range(route(P, pan, how="per_card"), base)
    R["spend per card, calibrated by regression"] = with_range(route(P, pan, how="per_card", reg=True), base)
    R["private-label share held at the third quarter's level"] = with_range(route(P, pan, plrule="flat"), base)
    R["the record with each quarter's own reported private-label share"] = with_range(route(P, pan, bt_plrule="hindsight"), base)
    return R


def variants(out):
    """each supporting result's rivals, for its band: R2's completion with mean factors and with the last thirteen
    deliveries; R3's comparable step on spend per card; R4 at the fiscal 2023 mix and at fiscal 2024's mix rolled
    forward; R5 and R8 under each private-label rule and each regional mix"""
    P, cf, pan = out["P"], out["cf"], out["pan"]
    keys = P["keys"]
    V = {}
    raw_c = panel_entity(P, cf, complete=False)
    tot_raw = raw_c[raw_c.fq == TQ].spend_usd.sum()
    for name, kw in (("mean factors", dict(stat="mean")), ("the last thirteen deliveries", dict(last_n=13))):
        c2 = completion_factors(P, **kw)
        p2 = panel_entity(P, c2)
        V.setdefault("completion", {})[name] = float(p2[p2.fq == TQ].spend_usd.sum() / tot_raw - 1)
    g2 = out["bridge"][0][1] + out["bridge"][1][1] + out["bridge"][2][1]
    rgp, pw = regional(P, pan, TQ, BQ, "per_card")
    t = sum(pw.values())
    V["comparable"] = {"spend per card": sum(rgp[r] * pw[r] / t for r in REGIONS) - g2}
    rg = out["regional"]
    gi = {"fiscal 2024 mix": out["g_idx"],
          "fiscal 2023 mix": sum(rg[r] * company_weights(P, "FY2023")[r] for r in REGIONS),
          "fiscal 2024 mix rolled forward": sum(rg[r] * rolled_weights(P, "FY2024")[r] for r in REGIONS)}
    V["visible"] = gi
    pl = P["pl"]
    V["pl"] = {rule: pl_target(pl, keys, TQ, rule) for rule in ("pace", "yoy", "line", "last")}
    V["drift"] = {rule: bank_share(pl[BQ]) / bank_share(v) - 1 for rule, v in V["pl"].items()}
    V["mix_step"] = {k: v - out["g_pooled"] for k, v in gi.items()}
    V["mix_step"]["the bank-card share first"] = out["bridge_rivals"]["the company's regional mix"]
    V["tender_step"] = {}
    for k, v in gi.items():
        for rule, d in V["drift"].items():
            V["tender_step"]["%s, %s" % (k, rule)] = (1 + v) * (1 + d) - 1 - v
    V["tender_step"]["the bank-card share first"] = out["bridge_rivals"]["the bank-card share of net sales"]
    return V


def shortcuts(out):
    """the hurried routes: what each files for the quarter, with its own record and range"""
    P, pan, base, cf = out["P"], out["pan"], out["base"], out["cf"]
    inc_pan = panel_entity(P, cf, complete=True, exclude=False)
    S = {}
    S["careful"] = with_range(route(P, pan, mix="panel", drift=False, reg=True), base)
    S["mix_only"] = with_range(route(P, pan, drift=False, reg=True), base)
    S["drift_only"] = with_range(route(P, pan, mix="panel"), base)
    S["drift_regressed"] = with_range(route(P, pan, mix="panel", reg=True), base)
    S["raw_regressed"] = with_range(route(P, pan, how="const_raw", mix="panel", drift=False, reg=True), base)
    S["desk_model"] = with_range(route(P, inc_pan, how="per_card", mix="panel", drift=False, reg=True), base)
    keys = P["keys"]
    org = {q: organic_growth(P, q, keys[keys.index(q) - 4], fern_both(P, q, keys[keys.index(q) - 4]))
           for q in origins_of(P)}
    S["trend"] = dict(growth=float(np.mean([org[k] for k in keys[-4:-1]])))
    S["trend"]["forecast"] = base * (1 + S["trend"]["growth"])
    p0 = panel_entity(P, cf, complete=False, exclude=False)
    S["quick"] = dict(growth=growth(P, p0, TQ, BQ, "all_issuers", "panel", False))
    S["quick"]["forecast"] = base * (1 + S["quick"]["growth"])
    out["organic"] = org
    return S


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
        res["other tenders at %d per cent of net sales" % round(100 * o)] = with_range(route(P, pan, other=o), base)["high"]
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
