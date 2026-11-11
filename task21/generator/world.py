"""The simulated process behind Halvergate Mutual's comparison-site motor book, 2024 to October 2026.

Month by month and segment by segment, drivers ask four comparison sites for a price. Each quote carries the
driver's rating factors and a true expected claims cost; Halvergate's rating model estimates that cost with an error
(v6 before 1 February 2026, v7 after); Halvergate's price is the estimate times its segment loading; each rival on the
panel prices the same risk with its own error, part of which every insurer shares. The driver buys mostly from the
cheapest. Sold quotes become policies that cancel, claim through the calendar's seasons, report late and settle
over months; nothing is placed where it decides an answer, every pattern runs through the whole book.

world.build() returns plain numpy/pandas tables; pack.py writes them as the organisation's exports.
"""
import datetime as dt
import hashlib

import numpy as np
import pandas as pd

import params as P

D0 = dt.date(2025, 1, 1)
IPT = 0.12                      # insurance premium tax, on the gross price shown on the sites
REGIONS = ["AB", "B", "BS", "CF", "EH", "G", "L", "LS", "M", "NE", "NG", "S", "SO", "TN", "LE", "CV", "PL", "EX"]
REGION_REL = np.array([0.82, 1.38, 1.02, 0.96, 0.88, 1.20, 1.42, 1.08, 1.33, 0.97, 1.05, 1.01, 0.93, 0.90, 1.07,
                       1.12, 0.86, 0.84])
REGION_W = np.array([3, 9, 5, 4, 5, 7, 6, 7, 8, 5, 5, 5, 5, 4, 5, 5, 3, 4], float)
REGION_W /= REGION_W.sum()


# ---- calendar helpers ------------------------------------------------------------------------------------------
def months(a, b):
    out, y, m = [], a.year, a.month
    while (y, m) <= (b.year, b.month):
        out.append(dt.date(y, m, 1))
        m += 1
        if m == 13:
            y, m = y + 1, 1
    return out


def days_in_month(d):
    nxt = dt.date(d.year + (d.month == 12), d.month % 12 + 1, 1)
    return (nxt - d).days


def sev_index(d):
    """Claim cost level at date d, 1.0 on 1 January 2025."""
    idx, y = 1.0, 2025
    t = d.year + (d.timetuple().tm_yday - 1) / 365.25
    if t >= 2025:
        for yy in range(2025, 2027):
            frac = min(max(t - yy, 0.0), 1.0)
            idx *= (1 + P.SEV_INFLATION[yy]) ** frac
    else:
        for yy in range(2024, 2020, -1):
            frac = min(max((yy + 1) - t, 0.0), 1.0)
            idx /= (1 + P.SEV_INFLATION[yy]) ** frac
    return idx


def load(seg, d):
    """Halvergate's loading over predicted cost on date d: the 2026 level less every change dated after d."""
    f = P.LOAD_2026[seg]
    for (dd, s, c) in P.RATE_CHANGES:
        if s == seg and dd > d:
            f /= 1 + c
    return f


def rival_level(d):
    return P.RIVAL_LEVEL.get(d.year, 1.0)


def version(d):
    return "v6" if d < P.REFIT else "v7"


def stable_u(*parts):
    """A deterministic uniform in [0, 1) from text parts (sampling decisions that must not move between builds)."""
    h = hashlib.sha256("|".join(map(str, parts)).encode()).digest()
    return int.from_bytes(h[:8], "big") / 2 ** 64


# ---- the drivers and their risk ----------------------------------------------------------------------------------
AGE_BANDS = {"u25": (np.arange(17, 25), np.array([4, 9, 12, 13, 14, 15, 16, 17], float)),
             "mid": (np.arange(25, 65), None), "o65": (np.arange(65, 90), None)}


def draw_drivers(rng, seg, n):
    ages, w = AGE_BANDS[seg]
    if w is None:
        if seg == "mid":
            w = np.exp(-((ages - 42) / 13.0) ** 2)
        else:
            w = np.exp(-(ages - 65) / 8.0)
    age = rng.choice(ages, n, p=w / w.sum())
    lic = np.clip(age - 17 - rng.integers(0, 4, n) - (rng.random(n) < 0.25) * rng.integers(0, 12, n), 0, None)
    ncd = np.minimum(lic, rng.integers(0, 10, n)) if seg != "u25" else np.minimum(lic, rng.integers(0, 4, n))
    vg = np.clip(np.round(rng.lognormal(np.log({"u25": 14, "mid": 22, "o65": 19}[seg]), 0.38, n)), 1, 50).astype(int)
    reg = rng.choice(len(REGIONS), n, p=REGION_W)
    mil = rng.choice([5000, 7000, 9000, 12000, 15000, 20000], n,
                     p={"u25": [.08, .17, .27, .25, .15, .08], "mid": [.07, .14, .22, .27, .19, .11],
                        "o65": [.22, .29, .25, .14, .07, .03]}[seg])
    cover = np.where(rng.random(n) < {"u25": 0.84, "mid": 0.93, "o65": 0.95}[seg], "COMP", "TPFT")
    # relative risk carried by the rating factors (mean about 1 within a segment)
    a = age.astype(float)
    age_rel = {"u25": np.exp(-0.085 * (a - 17)), "mid": np.exp(0.006 * (a - 42) ** 2 / 10 - 0.03),
               "o65": np.exp(0.035 * np.maximum(a - 74, 0))}[seg]
    rel = (age_rel * np.exp(-0.06 * np.minimum(ncd, 9)) * (vg / 20.0) ** 0.35 * REGION_REL[reg]
           * (mil / 9000.0) ** 0.42 * np.where(cover == "COMP", 1.0, 0.82))
    rel = rel / rel.mean()
    return dict(age=age, licence_years=lic, ncd=ncd, vehicle_group=vg, region=reg, mileage=mil, cover=cover,
                rel=rel)


def segment_cost(seg, d):
    """Expected claims cost of an average driver in the segment at date d (claims capped per the plan)."""
    return sum(P.FREQ[seg][t] * (1 - NIL_SHARE[t]) * P.SEV_MEAN[t] * capped_mean_factor(t)
               for t in P.CLAIM_TYPES) * sev_index(d)


def capped_mean_factor(t):
    mu, sd = np.log(P.SEV_MEAN[t]) - P.SEV_SD[t] ** 2 / 2, P.SEV_SD[t]
    # E[min(X, cap)] / E[X] for a lognormal
    from math import erf, exp, log, sqrt
    c = P.CLAIM_CAP
    phi = lambda x: 0.5 * (1 + erf(x / sqrt(2)))
    m = exp(mu + sd * sd / 2)
    above = c * (1 - phi((log(c) - mu) / sd))
    below = m * phi((log(c) - mu - sd * sd) / sd)
    return (below + above) / m


# ---- comparison-site quotes ---------------------------------------------------------------------------------------
PR = np.array([P.P_RANK.get(r, P.P_RANK_OTHER) for r in range(1, 40)])


def quote_month(seg, d, seed):
    rng = np.random.default_rng(seed)
    n = int(P.QUOTES_PER_MONTH[seg] * P.QUOTE_SEASON[d.month - 1] * rng.uniform(0.97, 1.03))
    drv = draw_drivers(rng, seg, n)
    u_sd = np.sqrt(max(P.RISK_SD[seg] ** 2 - np.var(np.log(drv["rel"])), 0.01))
    u = rng.normal(-u_sd ** 2 / 2, u_sd, n)
    relrisk = drv["rel"] * np.exp(u)                     # the driver's true risk relative to the segment
    day = rng.integers(0, days_in_month(d), n)
    hour = rng.choice(np.arange(24), n, p=_HOURS)
    minute = rng.integers(0, 60, n)
    second = rng.integers(0, 60, n)
    dates = np.array([d + dt.timedelta(days=int(x)) for x in day])
    mu = relrisk * segment_cost(seg, d)                  # true expected annual claims cost (capped)
    v = version(d)
    sdm = P.MODEL_SD[(seg, v)]
    z = rng.normal(0, 1, n)
    eps = sdm * (np.sqrt(P.COMMON_SHARE) * z + np.sqrt(1 - P.COMMON_SHARE) * rng.normal(0, 1, n))
    pred = mu * np.exp(eps)                              # Halvergate's predicted cost (its risk premium)
    pfreq = relrisk * sum(P.FREQ[seg].values()) * np.exp(eps)   # the model's predicted annual claim frequency
    net = pred * load(seg, d)
    gross = net * (1 + IPT)
    K = P.RIVALS[seg]
    eta = P.RIVAL_SD[seg] * (np.sqrt(P.COMMON_SHARE) * z[:, None]
                             + np.sqrt(1 - P.COMMON_SHARE) * rng.normal(0, 1, (n, K)))
    rl = np.exp(rng.normal(np.log(P.RIVAL_LOAD[seg]), P.RIVAL_LOAD_SD[seg], (n, K))) * rival_level(d)
    comp = mu[:, None] * np.exp(eta) * rl * (1 + IPT)
    comp.sort(axis=1)
    rank = 1 + (comp < gross[:, None]).sum(1)
    w = P.P_SHOP * PR[rank - 1]
    sold = rng.random(n) < w
    site = rng.choice(P.SITES, n, p=[P.SITE_SHARE[s] for s in P.SITES])
    monthly = rng.random(n) < P.MONTHLY_PAY_SHARE[seg]
    member = rng.random(n) < {"u25": 0.03, "mid": 0.07, "o65": 0.12}[seg]
    return dict(seg=np.full(n, seg), date=dates, hour=hour, minute=minute, second=second, site=site,
                age=drv["age"], licence_years=drv["licence_years"], ncd=drv["ncd"],
                vehicle_group=drv["vehicle_group"], region=drv["region"], mileage=drv["mileage"],
                cover=drv["cover"], relrisk=relrisk, mu=mu, pred=pred, pfreq=pfreq, net=net, gross=gross,
                comp1=comp[:, 0], comp2=comp[:, 1], comp3=comp[:, 2], comp_all=comp, rank=rank, w=w, sold=sold,
                monthly=monthly, member=member, version=np.full(n, v), n=n)


_h = np.array([0.4, 0.2, 0.1, 0.1, 0.1, 0.2, 0.6, 1.3, 2.2, 3.0, 3.2, 3.3, 3.6, 3.4, 3.2, 3.3, 3.6, 4.1, 5.0,
               5.6, 5.9, 5.3, 3.4, 1.4])
_HOURS = _h / _h.sum()


# ---- claims ---------------------------------------------------------------------------------------------------------
REPORT = {"AD": (6.0, 0.06), "TPPD": (9.0, 0.08), "TPBI": (70.0, 0.20), "THEFT": (2.5, 0.02), "WS": (4.0, 0.03)}
SETTLE = {"AD": (38, 0.6), "TPPD": (75, 0.7), "TPBI": (330, 0.8), "THEFT": (60, 0.5), "WS": (12, 0.4)}
NIL_SHARE = {"AD": 0.07, "TPPD": 0.09, "TPBI": 0.12, "THEFT": 0.05, "WS": 0.02}


def simulate_claims(rng, pol, seg_of, horizon):
    """Claims on each policy from inception to its end, month by month with the seasons (exposure days per calendar
    month as one matrix, Poisson by claim type); the future ones are the truth no as-at view can see."""
    s_ord = np.array([x.toordinal() for x in pol["inception"]])
    e_ord = np.array([x.toordinal() for x in pol["end"]])
    first = dt.date(min(pol["inception"]).year, 1, 1)
    last = max(pol["end"])
    ms = months(first, last)
    B = np.array([m.toordinal() for m in ms] + [(ms[-1] + dt.timedelta(days=days_in_month(ms[-1]))).toordinal()])
    mon = np.array([m.month for m in ms])
    rr = pol["relrisk"]
    out = []
    chunk = 40000
    for c0 in range(0, len(s_ord), chunk):
        sl = slice(c0, c0 + chunk)
        lo = np.maximum(s_ord[sl, None], B[None, :-1])
        hi = np.minimum(e_ord[sl, None], B[None, 1:])
        days = np.clip(hi - lo, 0, None)
        segs = seg_of[sl]
        for t in P.CLAIM_TYPES:
            f = np.array([P.FREQ[g][t] for g in segs])
            lam = f[:, None] * rr[sl, None] * np.array(P.CLAIM_SEASON[t])[mon - 1][None, :] * days / 365.0
            k = rng.poisson(lam)
            ii, mm = np.nonzero(k)
            for a, b in zip(ii, mm):
                for _ in range(k[a, b]):
                    acc = lo[a, b] + int(rng.integers(0, max(days[a, b], 1)))
                    out.append((c0 + a, t, dt.date.fromordinal(int(acc))))
    out.sort(key=lambda r: (r[2], r[0], r[1]))
    return out


def claim_details(rng, rows):
    out = []
    for (i, t, acc) in rows:
        mean_rep, late = REPORT[t]
        rep = rng.exponential(mean_rep) if rng.random() > late else rng.lognormal(np.log(mean_rep * 6), 0.9)
        if t == "TPBI":
            rep = rng.lognormal(np.log(28), 0.9)
        rep_date = acc + dt.timedelta(days=int(rep))
        nil = rng.random() < NIL_SHARE[t]
        sev = 0.0 if nil else min(rng.lognormal(np.log(P.SEV_MEAN[t]) - P.SEV_SD[t] ** 2 / 2, P.SEV_SD[t])
                                  * sev_index(acc), 4.0e6)
        med, sd = SETTLE[t]
        settle = rep_date + dt.timedelta(days=int(rng.lognormal(np.log(med), sd)))
        out.append((i, t, acc, rep_date, settle, sev, nil))
    return out


def as_at_view(rng, det, as_at):
    """Paid and incurred on each reported claim as at a date: payments run from report to settlement, and the case
    estimate on the open part carries a handler's error that is corrected as the claim matures."""
    recs = []
    for (i, t, acc, rep, settle, sev, nil) in det:
        if rep > as_at:
            continue
        if settle <= as_at:
            paid, case, status = sev, 0.0, "Closed"
        else:
            span = max((settle - rep).days, 1)
            frac = min(max((as_at - rep).days / span, 0.0), 1.0)
            paid = sev * frac ** 1.4 if t != "WS" else 0.0
            noise = np.exp(rng.normal(-0.02, 0.28 * (1 - frac) + 0.05))
            case = max(sev - paid, 0.0) * noise if not nil else sev * 0 + rng.uniform(150, 900) * (1 - frac)
            status = "Open"
        recs.append((i, t, acc, rep, settle if settle <= as_at else None, paid, case, status, nil))
    return recs


# ---- the whole book -------------------------------------------------------------------------------------------------
def build(seed=P.SEED, quote_from=dt.date(2024, 1, 1)):
    rng_master = np.random.default_rng(seed)
    q_parts, sample_parts = [], []
    for d in months(quote_from, P.AS_AT):
        for k, seg in enumerate(P.SEGMENTS):
            qm = quote_month(seg, d, seed + d.year * 100 + d.month * 7 + k * 1009)
            idx_sold = np.where(qm["sold"])[0]
            keep = {"sold": idx_sold}
            if d >= P.QUOTE_EXPORT_FROM:
                rng_s = np.random.default_rng(seed + 31 * d.month + 7 * k + d.year)
                unsold = np.where(~qm["sold"])[0]
                keep["sample"] = unsold[rng_s.random(len(unsold)) < 1 / 50.0]
            for kind, ix in keep.items():
                part = {c: (qm[c][ix] if isinstance(qm[c], np.ndarray) and qm[c].ndim == 1 else None)
                        for c in qm if c not in ("comp_all", "n")}
                part = {c: v for c, v in part.items() if v is not None}
                part["comp_all"] = qm["comp_all"][ix]
                part["kind"] = np.full(len(ix), kind)
                q_parts.append(part)
            sample_parts.append((seg, d, qm["n"]))
    Q = {c: np.concatenate([p[c] for p in q_parts]) for c in q_parts[0] if c != "comp_all"}
    comp_all = [p["comp_all"] for p in q_parts]
    maxk = max(c.shape[1] for c in comp_all)
    Q["comp_all"] = np.vstack([np.pad(c, ((0, 0), (0, maxk - c.shape[1])), constant_values=np.inf) for c in comp_all])
    n = len(Q["seg"])
    rng = np.random.default_rng(seed + 5)
    # quote references: one scheme per site (Pricelark changes its scheme on 1 July 2025)
    order = np.lexsort((Q["second"], Q["minute"], Q["hour"], np.array([x.toordinal() for x in Q["date"]])))
    for c in list(Q):
        Q[c] = Q[c][order]
    # each site numbers its own quote sessions, most of them other insurers' quotes, so Halvergate's references on a
    # site advance in that site's own irregular steps
    ref_rng = np.random.default_rng(seed + 61)
    seqno = np.zeros(n, dtype=np.int64)
    for s, (base, lo, hi) in {"Kitecompare": (4310000, 3, 40), "Covertide": (120000, 2, 25),
                              "Brightquote": (51200, 4, 70), "Pricelark": (610000, 2, 30)}.items():
        idx = np.where(Q["site"] == s)[0]
        seqno[idx] = base + np.cumsum(ref_rng.integers(lo, hi, len(idx)))
    Q["quote_ref"] = np.array([_ref(Q["site"][i], Q["date"][i], int(seqno[i])) for i in range(n)])
    # sold quotes become policies
    sold = Q["kind"] == "sold"
    pol_idx = np.where(sold)[0]
    inc = np.array([Q["date"][i] + dt.timedelta(days=int(rng.choice([0, 0, 1, 1, 2, 3, 5, 7, 10, 14, 21])))
                    for i in pol_idx])
    expiry = np.array([dt.date(x.year + 1, x.month, min(x.day, 28)) if not (x.month == 2 and x.day == 29)
                       else dt.date(x.year + 1, 2, 28) for x in inc])
    # cancellations: cooling-off, then mid-term (non-payment, vehicle sold) at the segment's rate
    segs = Q["seg"][pol_idx]
    cool = rng.random(len(pol_idx)) < P.COOLING_OFF
    lapse_rate = np.array([P.LAPSE_MIDTERM[s] for s in segs]) * np.where(Q["monthly"][pol_idx], 1.35, 0.6)
    t_lapse = rng.exponential(1 / lapse_rate) * 365.0
    end = []
    cancel_date, cancel_reason = [], []
    for j, i in enumerate(pol_idx):
        if cool[j]:
            cd = inc[j] + dt.timedelta(days=int(rng.integers(1, 14)))
            end.append(cd), cancel_date.append(cd), cancel_reason.append("Cooling-off")
        elif t_lapse[j] < (expiry[j] - inc[j]).days:
            cd = inc[j] + dt.timedelta(days=int(t_lapse[j]))
            reason = "Non-payment" if Q["monthly"][i] and rng.random() < 0.62 else "Vehicle sold"
            end.append(cd), cancel_date.append(cd), cancel_reason.append(reason)
        else:
            end.append(expiry[j]), cancel_date.append(None), cancel_reason.append("")
    pol = dict(q=pol_idx, inception=inc, expiry=expiry, end=np.array(end), cancel_date=np.array(cancel_date, object),
               cancel_reason=np.array(cancel_reason), relrisk=Q["relrisk"][pol_idx], seg=segs)
    # claims over each policy's whole term (the future ones are the truth the as-at view cannot see)
    rows = simulate_claims(np.random.default_rng(seed + 11), pol, segs, None)
    det = claim_details(np.random.default_rng(seed + 13), rows)
    view = as_at_view(np.random.default_rng(seed + 17), det, P.AS_AT)
    R = renewal_book(np.random.default_rng(seed + 23))
    RH = renewal_history(np.random.default_rng(seed + 29))
    return dict(Q=Q, pol=pol, claims_full=det, claims_view=view, quote_counts=sample_parts, R=R, RH=RH)


def _ref(site, d, i):
    if site == "Kitecompare":
        return "KC%s%07d" % (d.strftime("%y%m"), i % 10000000)
    if site == "Covertide":
        return "CT-%s-%06d" % (d.strftime("%Y%m%d"), i % 1000000)
    if site == "Brightquote":
        return "BQ%09d" % (300000000 + i)
    if d < dt.date(2025, 7, 1):
        return "PL/%s/%06d" % (d.strftime("%Y%m"), i % 1000000)
    return "PLK%s%07d" % (d.strftime("%y%j"), i % 10000000)


# ---- the over-65 renewal book ------------------------------------------------------------------------------------
def retention(dp):
    """Probability a renewing over-65 customer renews at a price change dp (offered over last year's premium, less 1)."""
    x = np.log(P.RETENTION_BASE / (1 - P.RETENTION_BASE)) - P.RETENTION_SLOPE * dp
    return 1 / (1 + np.exp(-x))


def renewal_book(rng):
    """The over-65 comparison-site customers due to renew in 2027: last year's premium, the renewal price Halvergate
    intends, and the equivalent new-business price that caps it (at 2026 new-business rates, 2027 cost index)."""
    n = P.O65_RENEWALS_2027
    drv = draw_drivers(rng, "o65", n)
    u_sd = np.sqrt(max(P.RISK_SD["o65"] ** 2 - np.var(np.log(drv["rel"])), 0.01))
    rel = drv["rel"] * np.exp(rng.normal(-u_sd ** 2 / 2, u_sd, n))
    d27 = np.array([dt.date(2027, int(m), 1) for m in rng.choice(np.arange(1, 13), n, p=np.array(P.QUOTE_SEASON) / sum(P.QUOTE_SEASON))])
    cost27 = rel * segment_cost("o65", dt.date(2027, 1, 1)) * (1 + P.CLAIMS_INFLATION_2027) / sev_index(dt.date(2027, 1, 1)) * sev_index(dt.date(2026, 7, 1))
    # the renewal model knows each customer's own claims history, so its estimate is closer than new business
    pred_ren = cost27 * np.exp(rng.normal(0, 0.06, n))
    pred_nb = cost27 * np.exp(P.MODEL_SD[("o65", "v7")] * rng.normal(0, 1, n))
    enbp = pred_nb * P.LOAD_2026["o65"]                  # net equivalent new-business price at unchanged rates
    intended = pred_ren * P.LOAD_2026["o65"] * np.exp(rng.normal(np.log(P.RENEWAL_INTENT_LOAD), 0.07, n))
    last = np.minimum(intended, enbp) / np.exp(rng.normal(0.045, 0.06, n))
    site = rng.choice(P.SITES, n, p=[P.SITE_SHARE[s] for s in P.SITES])
    return dict(age=drv["age"], ncd=drv["ncd"], vehicle_group=drv["vehicle_group"], region=drv["region"],
                mileage=drv["mileage"], renewal_month=np.array([x.month for x in d27]), site=site,
                last_premium=last, intended=intended, enbp=enbp, cost27=cost27, pred_ren=pred_ren)


def renewal_history(rng):
    """Over-65 renewal invitations January 2025 to October 2026, as the retention MI holds them: month, price-change
    band, invitations and renewals."""
    rows = []
    bands = np.arange(-0.14, 0.32, 0.02)
    for d in months(dt.date(2025, 1, 1), P.AS_AT):
        n = int(P.O65_RENEWALS_2027 / 12 * P.QUOTE_SEASON[d.month - 1] * rng.uniform(0.95, 1.05))
        dp = np.clip(rng.normal(0.055 if d.year == 2025 else 0.04, 0.075, n), -0.149, 0.319)
        ren = rng.random(n) < retention(dp)
        b = np.digitize(dp, bands) - 1
        for k in range(len(bands)):
            m = b == k
            if m.sum():
                rows.append((d, round(bands[k], 2), int(m.sum()), int(ren[m].sum())))
    return rows


# ---- the claims history before 2024 (aggregate cohorts for the reserving triangles) ------------------------------
BOOK_VEHICLE_YEARS = {2021: 158000, 2022: 171000, 2023: 183000}   # comparison-site private car exposure by year


def history_claims(rng):
    """Claims with accidents in 2021 to 2023 on the book as it was (the triangles' early rows): counts by month and
    type at the book's frequency and the seasons, each claim taken through the same report and settlement process."""
    mix = {"u25": 0.17, "mid": 0.67, "o65": 0.16}
    rows = []
    for y, vy in BOOK_VEHICLE_YEARS.items():
        for m in range(1, 13):
            d = dt.date(y, m, 1)
            for t in P.CLAIM_TYPES:
                f = sum(mix[g] * P.FREQ[g][t] for g in P.SEGMENTS)
                k = rng.poisson(f * vy / 12.0 * P.CLAIM_SEASON[t][m - 1])
                days = rng.integers(0, days_in_month(d), k)
                for x in days:
                    rows.append((-1, t, d + dt.timedelta(days=int(x))))
    return claim_details(rng, rows)


class ClaimBook:
    """Every claim as arrays, with each claim's handler error drawn once, so any as-at date values the whole book
    consistently (the claims extract at 31 October 2026 and each quarter-end of the triangles come from one record)."""

    def __init__(self, det, seed):
        rng = np.random.default_rng(seed)
        n = len(det)
        self.pol = np.array([d[0] for d in det])
        self.type = np.array([d[1] for d in det])
        self.acc = np.array([d[2].toordinal() for d in det])
        self.rep = np.array([d[3].toordinal() for d in det])
        self.settle = np.array([d[4].toordinal() for d in det])
        self.sev = np.array([d[5] for d in det])
        self.nil = np.array([d[6] for d in det])
        self.bias = rng.normal(0.0, 0.24, n)
        self.jit = rng.normal(0, 0.05, n)
        self.unil = rng.uniform(150, 900, n)
        # a closed claim reopens now and then and settles again a few months later for a little more
        self.reopen = rng.random(n) < 0.012
        self.reopen_at = self.settle + rng.integers(40, 200, n)
        self.reopen_add = np.where(self.reopen, self.sev * rng.uniform(0.04, 0.25, n) + 180.0, 0.0)
        self.reopen_close = self.reopen_at + rng.integers(30, 150, n)

    def value(self, as_at):
        a = as_at.toordinal() if hasattr(as_at, "toordinal") else int(as_at)
        reported = self.rep <= a
        closed = self.settle <= a
        span = np.maximum(self.settle - self.rep, 1)
        frac = np.clip((a - self.rep) / span, 0.0, 1.0)
        paid = np.where(closed, self.sev, np.where(self.type == "WS", 0.0, self.sev * frac ** 1.4))
        case = np.where(closed, 0.0, np.where(self.nil, self.unil * (1 - frac),
                                             np.maximum(self.sev - paid, 0.0) * np.exp(self.bias * (1 - frac) + self.jit)))
        reop = self.reopen & (self.reopen_at <= a)
        reop_open = reop & (self.reopen_close > a)
        paid = paid + np.where(reop & ~reop_open, self.reopen_add, 0.0)
        case = case + np.where(reop_open, self.reopen_add * 1.1, 0.0)
        status = np.where(~closed, "Open", np.where(reop_open, "Reopened", "Closed"))
        return reported, paid, case, status
