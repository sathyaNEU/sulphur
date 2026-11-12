"""task20 architecture 2 pack (second hardening): the records a long-short fund's research desk holds on Brindle & Moss three weeks before
its fourth-quarter fiscal 2025 release: the Kestrel Spend Panel's weekly delivery (the issuers' feeds as the vendor
concatenates them) and its delivery history, the panel's monthly spend by raw descriptor, the company's earnings
releases (releases.py), the street's estimates, and two alternative-data feeds the desk also buys. analysis.py reads
only what this module, releases.py and docs.py write."""
import csv
import os

import numpy as np
import pandas as pd

import releases as RL
import world as W

SEED = 17
STREET_GROWTH = 0.05             # the street's retail growth for the quarter
ISSUER_CODES = {"A": "KS-01", "B": "KS-02", "C": "KS-03", "D": "KS-04", "E": "KS-05", "F": "KS-06"}
FEED_ORDER = ["C", "A", "E", "B", "F", "D"]
REGION_CODE = {"KS-01": dict(zip(W.REGIONS, W.REGIONS)),
               "KS-02": dict(zip(W.REGIONS, [r.upper() for r in W.REGIONS])),
               "KS-03": dict(zip(W.REGIONS, W.REGIONS)),
               "KS-04": dict(zip(W.REGIONS, ["NE", "SE", "MW", "W"])),
               "KS-05": dict(zip(W.REGIONS, ["North East", "South East", "Mid-West", "West"])),
               "KS-06": dict(zip(W.REGIONS, W.REGIONS))}
MERCH = {"M0412": "BRINDLE & MOSS", "M0413": "BRINDLEMOSS.COM", "M2290": "FERNHOLLOW OUTFITTERS"}
MERCH_FEED = {"KS-02": {"M0412": "BRINDLE AND MOSS", "M0413": "BRINDLEMOSS COM", "M2290": "FERNHOLLOW OUTFITTERS"},
              "KS-05": {"M0412": "Brindle & Moss", "M0413": "brindlemoss.com", "M2290": "Fernhollow Outfitters"}}
OLDEST = 2014                    # the vendor reports accounts opened in 2014 or earlier as one bucket
F_PANEL = "kestrel_bmh_panel_weekly_delivery_2026-02-02.csv"
F_HIST = "kestrel_bmh_delivery_history_2025-08-04_2026-02-02.csv"
F_DESC = "kestrel_bmh_descriptor_detail_monthly.csv"
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
    """the calendar year the card account was opened at the issuer (a re-issued account carries its re-issue date)"""
    return (W.FY_START + pd.Timedelta(days=7 * int(ow))).year


def year_label(y):
    return "<=%d" % OLDEST if y <= OLDEST else str(y)


def panel_arrays(w):
    """spend and cards by week x issuer x region x open-year bucket x vendor merchant id, complete (before posting lags)"""
    years = sorted({max(open_year(c[2]), OLDEST) for c in w.co})
    yi = {y: n for n, y in enumerate(years)}
    I, R, Y = len(w.issuers), 4, len(years)
    sp = np.zeros((W.W, I, R, Y, 3))
    cards = np.zeros((W.W, I, R, Y))
    tx = np.zeros((W.W, I, R, Y, 3))
    mcol = {0: 0, 1: 0, 4: 0, 5: 0, 2: 1, 3: 2}             # stores, outlet, licensed, cafe -> M0412; web; fernhollow
    for c, x in enumerate(w.co):
        i, j, ow = x[0], x[1], x[2]
        y = yi[max(open_year(ow), OLDEST)]
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
    for name in FEED_ORDER:
        i = w.issuers.index(name)
        code = ISSUER_CODES[name]
        rc = REGION_CODE[code]
        mn = MERCH_FEED.get(code, MERCH)
        for t in range(W.W):
            ws = W.CAL.week_start.iloc[t].date().isoformat()
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
                        rows.append([ws, code, rc[reg], year_label(yr), mid, mn[mid], "%d" % round(n),
                                     "%d" % round(tx[t, i, j, y, col] * f), "%.2f" % s])
    return write_csv(path, ["week_start", "issuer_code", "billing_region", "card_open_year", "merchant_id", "merchant_name",
                            "panel_cards", "txn_count", "spend_usd"], rows)


def write_history(path, w, sp):
    rows = []
    tot = sp.sum(axis=(2, 3, 4))                              # week x issuer
    for d in w.deliveries:
        last = W.week_of(d - pd.Timedelta(days=8))
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
STUDIO_CITIES = ["BOSTON MA", "ATLANTA GA", "CHICAGO IL", "DENVER CO", "PHILADELPHIA PA", "CHARLOTTE NC",
                 "MINNEAPOLIS MN", "SEATTLE WA", "TAMPA FL", "PHOENIX AZ", "COLUMBUS OH"]
POS_CHANGE = pd.Period("2024-08", "M")          # the stores' terminals re-keyed: new descriptor format
TICKET = dict(store=290.0, studio=2650.0, outlet=140.0, web=240.0, paypal=230.0, custom=2240.0, lic=95.0, cafe=14.0,
              fern=180.0, fernweb=165.0)


def write_descriptors(path, w):
    """panel-wide monthly spend and transactions by raw descriptor: the vendor's name match puts the licensed
    shop-in-shops and the cafes under the brand's merchant id; custom orders are rung at the design studios' terminals
    and under the site's custom-order descriptor"""
    rd = np.random.default_rng(4412)
    months = pd.period_range("2021-02", "2026-01", freq="M")
    wk_month = W.CAL.week_start.dt.to_period("M")
    rows = []
    tot = w.spend.sum(1)                                       # week x merchant (panel-wide, complete)
    mto = w.spend.sum(1)[:, [0, 2]] * w.mto_share[:, None]          # week x (stores, site): made-to-order spend
    stores = [(k, c) for k, c in enumerate([c for reg in W.REGIONS for c in STORE_CITIES[reg]])]
    split_store = rd.dirichlet(np.ones(len(stores)) * 6)
    studio_w = rd.uniform(0.7, 1.3, len(STUDIO_CITIES))
    outlet_names = ["BRINDLE MOSS OUTLET #%02d %s" % (k + 1, c) for k, c in enumerate(["PRIMM NV", "LEESBURG VA",
                                                                                         "WRENTHAM MA", "AURORA IL"])]
    lic_names = ["B&M AT HOLLISTERS #%03d %s" % (k + 11, c) for k, c in
                 enumerate(["KING OF PRUSSIA PA", "SCHAUMBURG IL", "SCOTTSDALE AZ", "BELLEVUE WA", "PARAMUS NJ", "TROY MI",
                            "FRISCO TX", "BUCKHEAD GA"])]
    cafe_names = ["BRINDLE CAFE BOSTON MA", "BRINDLE CAFE CHICAGO IL", "SQ *BRINDLE CAFE DENVER"]
    split_out, split_lic, split_cafe = rd.dirichlet(np.ones(4) * 5), rd.dirichlet(np.ones(8) * 4), rd.dirichlet(np.ones(3) * 5)
    for m in months:
        sel = (wk_month == m).values
        if not sel.any():
            continue
        s = tot[sel].sum(0)
        m_ = mto[sel].sum(0)
        new = m >= POS_CHANGE
        jitter = lambda n: np.exp(rd.normal(0, 0.03, n))
        mstart = m.to_timestamp()
        # the studios open at their dates; a new studio ramps over its first months
        ages = [(mstart - s_).days / 30.4 for s_ in w.studios]
        wts = np.array([studio_w[k] * min(1.0, 0.35 + 0.65 * a / 4.0) if a >= 0 else 0.0 for k, a in enumerate(ages)])
        st_names = [("BRINDLE&MOSS DESIGN STUDIO %s" % c[:-3]) if new else ("BRINDLE & MOSS DESIGN STUDIO %s" % c)
                    for c in STUDIO_CITIES]
        sto_names = [("BRINDLE&MOSS %04d %s" % (100 + 7 * k, c)) if new else ("BRINDLE & MOSS #%04d %s" % (100 + 7 * k, c))
                     for k, c in stores]
        groups = [(sto_names, s[0] - m_[0], split_store, "store"), (st_names, m_[0], wts / wts.sum(), "studio"),
                  (outlet_names, s[1], split_out, "outlet"), (lic_names, s[4], split_lic, "lic"),
                  (cafe_names, s[5], split_cafe, "cafe")]
        for names, base, split, kind in groups:
            v = base * split * jitter(len(names))
            v = v * base / v.sum()
            for nm, x in zip(names, v):
                if x <= 0:
                    continue
                rows.append([str(m), "M0412", nm, "%.2f" % x, "%d" % round(x / TICKET[kind] * np.exp(rd.normal(0, 0.04)))])
        custom_name = "BRINDLEMOSS.COM CUSTOM" if m < pd.Period("2023-01", "M") else "BRINDLEMOSS CUSTOM ORDER"
        for nm, x, kind in zip(["BRINDLEMOSS.COM", "PAYPAL *BRINDLEMOSS", custom_name],
                               np.r_[(s[2] - m_[1]) * np.array([0.86, 0.14]), m_[1]], ["web", "paypal", "custom"]):
            rows.append([str(m), "M0413", nm, "%.2f" % x, "%d" % round(x / TICKET[kind] * np.exp(rd.normal(0, 0.04)))])
        for nm, x, kind in zip(["FERNHOLLOW OUTFITTERS #%02d" % (k + 1) for k in range(5)] + ["FERNHOLLOW.COM"],
                               s[3] * np.r_[rd.dirichlet(np.ones(5) * 5) * 0.8, 0.2], ["fern"] * 5 + ["fernweb"]):
            rows.append([str(m), "M2290", nm, "%.2f" % x, "%d" % round(x / TICKET[kind] * np.exp(rd.normal(0, 0.04)))])
    return write_csv(path, ["month", "merchant_id", "descriptor", "spend_usd", "txn_count"], rows)


def write_street(path, street_mid):
    """the sell-side's current estimates of the quarter's net sales, each broker's estimate before the third-quarter
    results and its rating"""
    rs = np.random.default_rng(9031)
    brokers = ["Abernathy Rowe", "Calloway Securities", "Dunmore & Pike", "Eastlake Capital Markets", "Granger Whitfield",
               "Halsey Brothers", "Ironbridge Research", "Kinsale Partners", "Marlow Street", "Northgate Equity", "Pell & Sutter"]
    est = street_mid * (1 + rs.normal(0, 0.006, len(brokers)))
    est = est - est.mean() + street_mid
    dates = sorted(pd.Timestamp("2025-12-11") + pd.Timedelta(days=int(x)) for x in rs.integers(0, 55, len(brokers)))
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
                     "%d" % round(3000 * np.exp(ra.normal(0, 0.3)) * (1.6 if d.month in (11, 12)else 1.0))])
    return write_csv(path, ["date", "country", "category", "app", "category_rank", "est_downloads"], rows)


def regions_by_year(w):
    """the 10-K's net sales of the Brindle & Moss brand by region: each quarter's brand net sales (net sales less
    Fernhollow and Contract) split by the regions' recognised sales, summed over the fiscal year (USD million)"""
    out = {}
    for fy in W.FY_NAMES[:-1]:
        tot = np.zeros(4)
        for q in [n for n, k in enumerate(W.QKEYS) if k.startswith(fy)]:
            brand = w.rev_q[q] - w.fern_q[q] - w.contract_q[q]
            tot += w.rev_q_region[q] * brand / w.rev_q_region[q].sum()
        out[fy] = [round(float(x), 1) for x in tot]
    return out


def by_year(w, arr):
    return {fy: round(float(sum(arr[n] for n, k in enumerate(W.QKEYS) if k.startswith(fy))), 1) for fy in W.FY_NAMES[:-1]}


def street_mid(w):
    """the sell-side's figure: retail net sales grown at fiscal 2025's pace, contract at its run rate"""
    n = len(W.QKEYS) - 1
    return round(float(w.retail_q[n - 4]) * (1 + STREET_GROWTH) + float(np.median(w.contract_q[n - 8:n])))


def write_all(tgt, w, street):
    years, sp, cards, tx = panel_arrays(w)
    rows = {}
    rows[F_PANEL] = write_panel(os.path.join(tgt, F_PANEL), w, years, sp, cards, tx)
    rows[F_HIST] = write_history(os.path.join(tgt, F_HIST), w, sp)
    rows[F_DESC] = write_descriptors(os.path.join(tgt, F_DESC), w)
    rows[F_STREET] = write_street(os.path.join(tgt, F_STREET), street)
    rows[F_WEB] = write_web(os.path.join(tgt, F_WEB), w)
    rows[F_APP] = write_app(os.path.join(tgt, F_APP), w)
    rel, F, pre = RL.write_all(tgt, w)
    for f in rel:
        rows[f] = sum(1 for _ in open(os.path.join(tgt, f)))
    return dict(rows=rows, years=years, releases=rel, reported=F, fy2020=pre)
