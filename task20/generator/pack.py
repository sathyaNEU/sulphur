"""task20 architecture 2 pack: the records a long-short fund's research desk holds on Brindle & Moss three weeks before
its fourth-quarter fiscal 2025 release: the Kestrel Spend Panel's weekly delivery and its delivery history, the
panel's monthly descriptor detail, the company's quarterly results, the street's estimates, and two
alternative-data feeds the desk also buys. analysis.py reads only what this module writes."""
import csv
import datetime as dt
import os
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

import world as W

NY = ZoneInfo("America/New_York")
SEED = 17
STREET_GROWTH = 0.0396           # the street consensus over the fourth quarter of fiscal 2024
ISSUER_CODES = {"A": "KS-01", "B": "KS-02", "C": "KS-03", "D": "KS-04", "E": "KS-05", "F": "KS-06"}
MERCH = {"M0412": "BRINDLE & MOSS", "M0413": "BRINDLEMOSS.COM", "M2290": "FERNHOLLOW OUTFITTERS"}
F_PANEL = "kestrel_bmh_panel_weekly_delivery_2026-02-02.csv"
F_HIST = "kestrel_bmh_delivery_history_2025-08-04_2026-02-02.csv"
F_DESC = "kestrel_bmh_descriptor_detail_monthly.csv"
F_NOTES = "kestrel_spend_panel_release_notes.txt"
F_RESULTS = "bmh_quarterly_results_fy2021q1_fy2025q3.csv"
F_STREET = "bmh_q4fy25_street_estimates.csv"
F_WEB = "kestrel_web_visits_bmh_weekly.csv"
F_APP = "appmetric_bmh_app_daily.csv"


def write_csv(path, header, rows):
    with open(path, "w", newline="") as f:
        wr = csv.writer(f, lineterminator="\n")
        wr.writerow(header)
        wr.writerows(rows)
    return len(rows)


def open_year(ow):
    """the calendar year the card account was opened (the issuer's own open date)"""
    return (W.FY_START + pd.Timedelta(days=7 * int(ow))).year


def panel_arrays(w):
    """spend and cards by week x issuer x region x open year x vendor merchant id, complete (before posting lags)"""
    years = sorted({open_year(c[2]) for c in w.co})
    yi = {y: n for n, y in enumerate(years)}
    I, R, Y = len(w.issuers), 4, len(years)
    sp = np.zeros((W.W, I, R, Y, 3))
    cards = np.zeros((W.W, I, R, Y))
    tx = np.zeros((W.W, I, R, Y, 3))
    mcol = {0: 0, 1: 0, 4: 0, 5: 0, 2: 1, 3: 2}             # stores, outlet, licensed, cafe -> M0412; web; fernhollow
    for c, (i, j, ow, _) in enumerate(w.co):
        y = yi[open_year(ow)]
        cards[:, i, j, y] += w.active[:, c]
        for m, col in mcol.items():
            sp[:, i, j, y, col] += w.spend[:, c, m]
            tx[:, i, j, y, col] += w.txns[:, c, m]
    return years, sp, cards, tx


def completeness(w, delivery, i, wk):
    return w.comp.get((delivery, i, wk), 1.0)


def write_panel(path, w, years, sp, cards, tx):
    d = w.deliveries[-1]
    rows = []
    for t in range(W.W):
        ws = W.CAL.week_start.iloc[t].date().isoformat()
        for i, iss in enumerate(w.issuers):
            f = completeness(w, d, i, t)
            for j, reg in enumerate(W.REGIONS):
                for y, yr in enumerate(years):
                    n = cards[t, i, j, y]
                    if n < 0.5:
                        continue
                    for col, mid in enumerate(MERCH):
                        s = sp[t, i, j, y, col] * f
                        if s <= 0:
                            continue
                        rows.append([ws, ISSUER_CODES[iss], reg, yr, mid, MERCH[mid], "%d" % round(n),
                                     "%d" % round(tx[t, i, j, y, col] * f), "%.2f" % s])
    return write_csv(path, ["week_start", "issuer_code", "billing_region", "card_open_year", "merchant_id", "merchant_name",
                            "panel_cards", "txn_count", "spend_usd"], rows)


def write_history(path, w, sp):
    rows = []
    tot = sp.sum(axis=(2, 3, 4))                              # week x issuer
    for d in w.deliveries:
        last = int(np.searchsorted(W.CAL.week_start.values, (d - pd.Timedelta(days=8)).to_datetime64(), side="right")) - 1
        for i, iss in enumerate(w.issuers):
            for t in range(last - 5, last + 1):
                if tot[t, i] <= 0:
                    continue
                rows.append([d.date().isoformat(), ISSUER_CODES[iss], W.CAL.week_start.iloc[t].date().isoformat(),
                             "%.2f" % (tot[t, i] * completeness(w, d, i, t))])
    return write_csv(path, ["delivery_date", "issuer_code", "week_start", "spend_usd"], rows)


STORE_CITIES = {"Northeast": ["BOSTON MA", "HARTFORD CT", "PROVIDENCE RI", "ALBANY NY", "PHILADELPHIA PA", "NEWARK NJ"],
                "Southeast": ["ATLANTA GA", "CHARLOTTE NC", "RALEIGH NC", "TAMPA FL", "ORLANDO FL", "NASHVILLE TN"],
                "Midwest": ["CHICAGO IL", "COLUMBUS OH", "INDIANAPOLIS IN", "MINNEAPOLIS MN", "DETROIT MI", "ST LOUIS MO"],
                "West": ["DENVER CO", "PHOENIX AZ", "PORTLAND OR", "SEATTLE WA", "SACRAMENTO CA", "SALT LAKE CTY UT"]}


def write_descriptors(path, w):
    """panel-wide monthly spend by raw descriptor: the vendor's name match puts the licensed shop-in-shops and the cafes
    under the brand's merchant id"""
    rd = np.random.default_rng(4412)
    months = pd.period_range("2021-02", "2026-01", freq="M")
    wk_month = W.CAL.week_start.dt.to_period("M")
    rows = []
    tot = w.spend.sum(1)                                       # week x merchant (panel-wide, complete)
    split_store = rd.dirichlet(np.ones(24) * 6)
    store_names = ["BRINDLE & MOSS #%04d %s" % (100 + 7 * k, c) for k, c in
                   enumerate([c for reg in W.REGIONS for c in STORE_CITIES[reg]])]
    outlet_names = ["BRINDLE MOSS OUTLET #%02d %s" % (k + 1, c) for k, c in enumerate(["PRIMM NV", "LEESBURG VA", "WRENTHAM MA", "AURORA IL"])]
    lic_names = ["B&M AT HOLLISTERS #%03d %s" % (k + 11, c) for k, c in
                 enumerate(["KING OF PRUSSIA PA", "SCHAUMBURG IL", "SCOTTSDALE AZ", "BELLEVUE WA", "PARAMUS NJ", "TROY MI",
                            "FRISCO TX", "BUCKHEAD GA"])]
    cafe_names = ["BRINDLE CAFE %s" % c for c in ("BOSTON MA", "CHICAGO IL", "DENVER CO")]
    split_out, split_lic, split_cafe = rd.dirichlet(np.ones(4) * 5), rd.dirichlet(np.ones(8) * 4), rd.dirichlet(np.ones(3) * 5)
    for m in months:
        sel = (wk_month == m).values
        if not sel.any():
            continue
        s = tot[sel].sum(0)
        jitter = lambda n: np.exp(rd.normal(0, 0.03, n))
        for names, base, split in ((store_names, s[0], split_store), (outlet_names, s[1], split_out),
                                   (lic_names, s[4], split_lic), (cafe_names, s[5], split_cafe)):
            v = base * split * jitter(len(names))
            v = v * base / v.sum()
            for nm, x in zip(names, v):
                rows.append([str(m), "M0412", nm, "%.2f" % x])
        for nm, x in zip(["BRINDLEMOSS.COM", "PAYPAL *BRINDLEMOSS"], s[2] * np.array([0.86, 0.14])):
            rows.append([str(m), "M0413", nm, "%.2f" % x])
        for nm, x in zip(["FERNHOLLOW OUTFITTERS #%02d" % (k + 1) for k in range(5)] + ["FERNHOLLOW.COM"],
                         s[3] * np.r_[rd.dirichlet(np.ones(5) * 5) * 0.8, 0.2]):
            rows.append([str(m), "M2290", nm, "%.2f" % x])
    return write_csv(path, ["month", "merchant_id", "descriptor", "spend_usd"], rows)


def write_results(path, w):
    rows = []
    for q, qk in enumerate(W.QKEYS[:-1]):
        sel = W.QIDX == q
        st = W.CAL.week_start[sel].iloc[0].date()
        en = W.CAL.week_end[sel].iloc[-1].date()
        fern = w.fern[sel & w.consolidated].sum() if (sel & w.consolidated).any() else 0.0
        rows.append([qk.replace("Q", " Q"), st.isoformat(), en.isoformat(), int(sel.sum()), "%.1f" % w.rev_q[q],
                     ("%.1f" % fern) if fern else ""])
    sel = W.QIDX == len(W.QKEYS) - 1
    rows.append(["FY2025 Q4", W.CAL.week_start[sel].iloc[0].date().isoformat(), W.CAL.week_end[sel].iloc[-1].date().isoformat(),
                 int(sel.sum()), "", ""])
    return write_csv(path, ["fiscal_quarter", "period_start", "period_end", "weeks", "net_sales_usd_m",
                            "fernhollow_net_sales_usd_m"], rows)


def write_street(path, street_mid):
    """the sell-side's current estimates of the quarter's net sales, each broker's estimate before the third-quarter
    results and its rating"""
    rs = np.random.default_rng(9031)
    brokers = ["Abernathy Rowe", "Calloway Securities", "Dunmore & Pike", "Eastlake Capital Markets", "Granger Whitfield",
               "Halsey Brothers", "Ironbridge Research", "Kinsale Partners", "Marlow Street", "Northgate Equity", "Pell & Sutter"]
    est = street_mid * (1 + rs.normal(0, 0.006, len(brokers)))
    est = est - est.mean() + street_mid
    dates = sorted(pd.Timestamp("2025-12-04") + pd.Timedelta(days=int(x)) for x in rs.integers(0, 60, len(brokers)))
    prior = est * (1 + rs.normal(0.004, 0.003, len(brokers)))
    ratings = ["Buy", "Hold", "Buy", "Hold", "Buy", "Sell", "Hold", "Hold", "Buy", "Hold", "Sell"]
    rows = [[b, d.date().isoformat(), "%.1f" % e, "%.1f" % p_, r] for b, d, e, p_, r in zip(brokers, dates, est, prior, ratings)]
    return write_csv(path, ["broker", "estimate_date", "q4_fy2025_net_sales_usd_m", "prior_q4_fy2025_net_sales_usd_m",
                            "rating"], rows)


def write_web(path, w):
    rw = np.random.default_rng(5150)
    rows = []
    season = W.season_index()
    for t in range(W.W):
        visits = 2.3e6 * w.traffic[t] * season[t] * w.web[t] / 0.17 * np.exp(rw.normal(0, 0.06)) * (1 + 0.15 * t / W.W)
        rows.append([W.CAL.week_start.iloc[t].date().isoformat(), "brindlemoss.com", "%d" % round(visits),
                     "%.2f" % (0.62 + 0.0004 * t + rw.normal(0, 0.01)), "%.1f" % (4.1 + rw.normal(0, 0.3))])
    return write_csv(path, ["week_start", "domain", "est_visits", "mobile_share", "avg_pages_per_visit"], rows)


def write_app(path, w):
    ra = np.random.default_rng(7777)
    days = pd.date_range("2023-03-01", "2026-01-31", freq="D")
    rows = []
    rank = 140.0
    for d in days:
        rank = max(20.0, min(400.0, rank * np.exp(ra.normal(0, 0.05)) + (-(d.month in (11, 12)) * 0.6)))
        rows.append([d.date().isoformat(), "US", "Shopping", "Brindle & Moss", "%d" % round(rank),
                     "%d" % round(3000 * np.exp(ra.normal(0, 0.3)) * (1.6 if d.month in (11, 12) else 1.0))])
    return write_csv(path, ["date", "country", "category", "app", "category_rank", "est_downloads"], rows)


def pl_by_quarter(w):
    """the private-label card's share of net sales by fiscal quarter, as the filings report it (one decimal)"""
    out = {}
    for q, qk in enumerate(W.QKEYS):
        sel = W.QIDX == q
        out[qk] = round(100 * (w.own[sel] * w.rev_w[sel]).sum() / w.rev_w[sel].sum(), 1)
    return out


def regions_by_year(w):
    """the 10-K's net sales of the Brindle & Moss banner by region: each quarter's reported banner net sales (net sales
    less Fernhollow) split by the regions' sales, summed over the fiscal year"""
    out = {}
    for fy in W.FY_NAMES[:-1]:
        tot = np.zeros(4)
        for q in [n for n, k in enumerate(W.QKEYS) if k.startswith(fy)]:
            sel = W.QIDX == q
            banner = w.rev_q[q] - w.fern[sel & w.consolidated].sum()
            tot += w.rev_q_region[q] * banner / w.rev_q_region[q].sum()
        out[fy] = [round(float(x), 1) for x in tot]
    return out


def street_mid(w):
    return round(float(w.rev_q[-5]) * (1 + STREET_GROWTH))


def write_all(tgt, w, street_mid):
    years, sp, cards, tx = panel_arrays(w)
    rows = {}
    rows[F_PANEL] = write_panel(os.path.join(tgt, F_PANEL), w, years, sp, cards, tx)
    rows[F_HIST] = write_history(os.path.join(tgt, F_HIST), w, sp)
    rows[F_DESC] = write_descriptors(os.path.join(tgt, F_DESC), w)
    rows[F_RESULTS] = write_results(os.path.join(tgt, F_RESULTS), w)
    rows[F_STREET] = write_street(os.path.join(tgt, F_STREET), street_mid)
    rows[F_WEB] = write_web(os.path.join(tgt, F_WEB), w)
    rows[F_APP] = write_app(os.path.join(tgt, F_APP), w)
    return dict(rows=rows, years=years)
