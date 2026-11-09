"""The pack: the clean panel written out as the files the panel provider, the retail audit and Northvale hold, each in
its producing system's own form and with the mess those systems really make (the design note's Layer 1 inventory).
Nothing here narrates the files; each carries its conventions the way its system writes them."""
import csv
import datetime as dt
import os

import numpy as np

import common as C
import products as PR
import world as W

DAY_W = np.array([0.10, 0.11, 0.12, 0.13, 0.17, 0.21, 0.16])
MIGRATION = dt.date(2025, 3, 3)          # the panel platform's move to ISO dates
RECODE = dt.date(2025, 6, 30)            # the retailer coding change
OLD_CODE = {'NGF': 'NTG', 'MBV': 'MBL'}
# the universe's households by province and size (census shares), which the panel's own mix departs from
UNIV_PROV = {'ON': 0.376, 'QC': 0.234, 'BC': 0.139, 'AB': 0.111, 'MB': 0.034, 'SK': 0.030, 'NS': 0.028, 'NB': 0.022,
             'NL': 0.015, 'PE': 0.004}
UNIV_SIZE = {1: 0.293, 2: 0.340, 3: 0.150, 4: 0.136, 5: 0.081}
PROV = {'ATL': (['NS', 'NB', 'NL', 'PE'], [0.42, 0.33, 0.18, 0.07]), 'QC': (['QC'], [1.0]), 'ON': (['ON'], [1.0]),
        'PR': (['AB', 'MB', 'SK'], [0.57, 0.24, 0.19]), 'BC': (['BC'], [1.0])}


def occasions(S, seed=W.SEED + 101):
    """Every category occasion of the clean panel as parallel arrays: household, week, day, banner, Northvale flag,
    promoted flag, trial flag. Northvale occasions sit at banners stocking the line that week (promoted ones at
    promoted banners, the first purchase at the banner the world drew for it)."""
    rng = np.random.default_rng(seed)
    H = S['H']
    occ, nv, nvp, tried, tb = S['occ'], S['nv'], S['nv_promo'], S['tried'], S['trial_banner']
    hh, wk, isnv, ispr, istr, ban = [], [], [], [], [], []
    for t in range(W.NW):
        idx = np.nonzero(occ[t])[0]
        if len(idx) == 0:
            continue
        for h in idx:
            o, k, kp = int(occ[t, h]), int(nv[t, h]), int(nvp[t, h])
            mix = H['mix'][h]
            for j in range(o):
                hh.append(h); wk.append(t)
                if j < k:
                    isnv.append(True)
                    first = (tried[h] == t and j == 0)
                    istr.append(first)
                    pr = j < kp
                    ispr.append(pr)
                    if first:
                        ban.append(int(tb[h]))
                        continue
                    w = mix * W.DIST[t] * (W.PROMO[t] if pr else (1 - W.PROMO[t]))
                    if w.sum() <= 0:
                        w = mix * W.DIST[t]
                    ban.append(int(rng.choice(W.NB, p=w / w.sum())))
                else:
                    isnv.append(False); istr.append(False); ispr.append(False)
                    ban.append(int(rng.choice(W.NB, p=mix)))
    day = rng.choice(7, len(hh), p=DAY_W)
    return dict(hh=np.array(hh), wk=np.array(wk), day=day, banner=np.array(ban), nv=np.array(isnv),
                promo=np.array(ispr), trial=np.array(istr))


def iso_date(t, day):
    return W.week_start(t) + dt.timedelta(days=int(day))


def lines(S, O, M, seed=W.SEED + 102):
    """Purchase lines for every occasion: the SKU, units and amount paid, before the export's own mess."""
    rng = np.random.default_rng(seed)
    H = S['H']
    fam, own, nvs = PR.index(M)
    fav = rng.integers(0, 6, (H['n'], 6))                         # the household's usual SKU in each family
    nv_flavour = rng.random(H['n']) < 0.62                         # Original over Unsweetened
    # background deals on other brands: (banner, ean, week) on deal, about one week in nine, a quarter as multibuys
    out = []
    n = len(O['hh'])
    u = rng.random(n)
    deal_draw = rng.random(n)
    for i in range(n):
        h, t, b = int(O['hh'][i]), int(O['wk'][i]), int(O['banner'][i])
        bc = W.B_CODE[b]
        d = iso_date(t, O['day'][i])
        if O['nv'][i]:
            sku = nvs[2] if H['barista'][h] else (nvs[0] if nv_flavour[h] else nvs[1])
            units = int(H['nv_units'][h])
            kind = int(W.PROMO_KIND[t, b]) if t <= W.T_END else 0
            price = round(sku['price'] * PR.BANNER_PRICE[bc] * 20) / 20 - 0.01 if bc not in ('LYG',) else sku['price']
            if kind == 1:
                price = 4.79 if sku['litres'] > 1 else 3.79
            elif kind == 2:
                price = 3.99 if sku['litres'] > 1 else 3.29
            if kind == 3:
                units = 2
                out.append((h, d, bc, sku, units, 10.00 if sku['litres'] > 1 else 8.00, 'MB'))
            else:
                out.append((h, d, bc, sku, units, round(price * units, 2), 'Y' if kind else 'N'))
            continue
        f = int(rng.choice(W.NBR, p=H['pref'][h]))
        if bc == 'CWC':
            pool = own['CWC'] + fam[0][:1] + fam[1][:1]
            sku = pool[fav[h, 0] % len(pool)] if u[i] < 0.8 else pool[int(rng.integers(len(pool)))]
        elif f == W.NBR - 1:
            pool = own[bc]
            sku = pool[fav[h, 5] % len(pool)] if u[i] < 0.75 else pool[int(rng.integers(len(pool)))]
        else:
            pool = fam[f]
            sku = pool[fav[h, f] % len(pool)] if u[i] < 0.75 else pool[int(rng.integers(len(pool)))]
        L = sku['litres'] * sku['units']
        x = H['litres_occ'][h] / L
        units = max(1, int(np.floor(x)) + (1 if rng.random() < x - np.floor(x) else 0))
        units = min(units, 6)
        base = round(sku['price'] * PR.BANNER_PRICE[bc] * 20) / 20 - 0.01
        if deal_draw[i] < 0.085:
            paid, flag = round(base * 0.78 * units, 2), 'Y'
        elif deal_draw[i] < 0.11 and units >= 2:
            paid, flag = round((base * 2 * 0.8) * (units // 2) + base * (units % 2), 2), 'MB'
        else:
            paid, flag = round(base * units, 2), 'N'
        out.append((h, d, bc, sku, units, paid, flag))
    return out


def write_purchases(S, L, path, seed=W.SEED + 103):
    """The panel's purchase-line export. One line per item scanned from a receipt: household, receipt, date, banner,
    item code, quantity and amount paid, and whether the shopper recorded a deal. The export carries what its systems do:
    multibuys parsed with the deal total on the first unit and nothing on the rest, receipts re-uploaded after an app
    timeout, refunds scanned as negative lines, one retailer feed storing item codes as numbers, day-first dates before
    the platform migration and the retailer coding change."""
    rng = np.random.default_rng(seed)
    hid = S['hh_id']
    used = set()

    def rid():
        while True:
            r = 'R%010d' % int(rng.integers(10 ** 9, 10 ** 10 - 1))
            if r not in used:
                used.add(r)
                return r
    rows = []
    for (h, d, bc, sku, units, paid, flag) in L:
        r = rid()
        code = bc if d >= RECODE or bc not in OLD_CODE else OLD_CODE[bc]
        if flag == 'MB' and units >= 2:
            for k in range(units):
                rows.append([hid[h], r, d, code, sku['ean'], 1, paid if k == 0 else 0.0, 'Y'])
        else:
            rows.append([hid[h], r, d, code, sku['ean'], units, paid, 'Y' if flag != 'N' else 'N'])
        if rng.random() < 0.0026:                                    # a refund, scanned a few days later
            rows.append([hid[h], rid(), d + dt.timedelta(days=int(rng.integers(1, 10))), code, sku['ean'],
                         -units if flag != 'MB' else -1, -(paid if flag != 'MB' else round(paid / max(units, 1), 2)), 'N'])
    # receipts re-uploaded after a timeout: every line of the receipt again, same receipt id
    by_r = {}
    for k, row in enumerate(rows):
        by_r.setdefault(row[1], []).append(k)
    dup = [r for r in by_r if rng.random() < 0.0055]
    extra = [list(rows[k]) for r in dup for k in by_r[r]]
    rows += extra
    rows.sort(key=lambda x: (x[2], x[1]))
    blank_flag = rng.random(len(rows)) < 0.017
    with open(path, 'w', newline='') as fh:
        w = csv.writer(fh, lineterminator='\r\n')
        w.writerow(['hh_id', 'receipt_id', 'purchase_date', 'banner_cd', 'item_code', 'qty', 'amount_paid', 'deal_ind'])
        for k, (h, r, d, code, ean, q, paid, flag) in enumerate(rows):
            ds = d.strftime('%d/%m/%Y') if d < MIGRATION else d.isoformat()
            ec = ean.lstrip('0') if code == 'VLW' else ean
            w.writerow([h, r, ds, code, ec, q, '%.2f' % paid, '' if blank_flag[k] else flag])
    return len(rows), len(extra)


def household_ids(n, seed=W.SEED + 104):
    rng = np.random.default_rng(seed)
    ids = rng.choice(np.arange(1_000_000, 9_999_999), n, replace=False)
    return np.array(['LCP%07d' % i for i in ids])


def weights(S):
    """The panel's projection factor for each household and year: the province and household-size cell's universe
    over the households in tab for at least half the year in that cell."""
    H = S['H']
    prov = S['province']
    size_cell = np.clip(H['size'], 1, 5)
    out = {}
    for yr in (2024, 2025, 2026):
        a = W.widx(dt.date.fromisocalendar(yr, 1, 1))
        b = min(W.widx(dt.date.fromisocalendar(yr, 52, 1)), W.T_END)
        weeks_in = np.clip(np.minimum(H['leave'], b + 1) - np.maximum(H['join'], a), 0, None)
        intab = weeks_in >= (b - a + 1) / 2
        f = np.full(H['n'], np.nan)
        cells = {}
        for p in sorted(set(prov)):
            for s in range(1, 6):
                m = intab & (prov == p) & (size_cell == s)
                cells[(p, s)] = m.sum()
        share_p, share_s = UNIV_PROV, UNIV_SIZE
        for (p, s), c in cells.items():
            if c == 0:
                continue
            m = intab & (prov == p) & (size_cell == s)
            f[m] = C.UNIVERSE_HH[yr] * share_p[p] * share_s[s] / c
        out[yr] = f
    return out


def write_households(S, path, seed=W.SEED + 105):
    """The panel's household register: one row per household ever recruited, its province, size and the bands the
    recruitment survey asked, the weeks it joined and left, and each year's projection factor."""
    rng = np.random.default_rng(seed)
    H = S['H']
    n = H['n']
    age = rng.choice(['18-34', '35-44', '45-54', '55-64', '65+'], n, p=[0.19, 0.20, 0.19, 0.19, 0.23])
    inc = rng.choice(['<40k', '40-59k', '60-79k', '80-99k', '100-149k', '150k+', ''], n,
                     p=[0.16, 0.15, 0.15, 0.13, 0.19, 0.14, 0.08])
    old_sys = (rng.random(n) < 0.27) & (H['join'] == 0)            # recruited before the 2023 register rebuild
    first_year = rng.choice([2018, 2019, 2020, 2021, 2022, 2023], n, p=[0.12, 0.14, 0.15, 0.18, 0.2, 0.21])
    first_year = np.where(old_sys, np.minimum(first_year, 2022), first_year)
    WT = S['weights']
    rows = []
    for i in range(n):
        p = S['province'][i]
        pc = {'ON': 'Ont.', 'QC': 'Que.', 'BC': 'B.C.', 'AB': 'Alta.', 'MB': 'Man.', 'SK': 'Sask.', 'NS': 'N.S.',
              'NB': 'N.B.', 'NL': 'N.L.', 'PE': 'P.E.I.'}[p] if old_sys[i] else p
        size = int(H['size'][i])
        sz = ('5+' if size >= 5 else str(size)) if old_sys[i] else str(size)
        jw = W.iso_label(int(H['join'][i])) if H['join'][i] > 0 else '%d-W%02d' % (first_year[i], int(rng.integers(2, 52)))
        lw = W.iso_label(int(H['leave'][i])) if H['leave'][i] <= W.T_END else ''
        fs = ['' if not np.isfinite(WT[yr][i]) else '%.1f' % WT[yr][i] for yr in (2024, 2025, 2026)]
        rows.append([S['hh_id'][i], pc, sz, age[i], inc[i] if inc[i] else ('Prefer not to say' if rng.random() < 0.5 else ''),
                     jw, lw] + fs)
    with open(path, 'w', newline='') as fh:
        w = csv.writer(fh, lineterminator='\n')
        w.writerow(['hh_id', 'province', 'hh_size', 'head_age_band', 'hh_income_band', 'joined_week', 'left_week',
                    'proj_factor_2024', 'proj_factor_2025', 'proj_factor_2026'])
        w.writerows(rows)
    return n


def write_weeks(path):
    rows = []
    t0 = W.widx(dt.date.fromisocalendar(2024, 1, 1))
    for t in range(t0, W.NW_ALL):
        s = W.week_start(t)
        y, wk, _ = s.isocalendar()
        period = min(13, (wk - 1) // 4 + 1)
        q = min(4, (wk - 1) // 13 + 1)
        rows.append(['%04d-W%02d' % (y, wk), s.isoformat(), (s + dt.timedelta(days=6)).isoformat(), y,
                     'P%02d' % period, 'Q%d' % q])
    with open(path, 'w', newline='') as fh:
        w = csv.writer(fh, lineterminator='\n')
        w.writerow(['panel_week', 'week_start', 'week_end', 'panel_year', 'retail_period', 'panel_quarter'])
        w.writerows(rows)
    return len(rows)


def write_banners(path):
    rows = [
        ['FMF', 'Foxmere Fresh', 'Premium grocery', 'ON;BC;AB;MB;SK', '2019-01-01', ''],
        ['GLM', 'Greenleaf Market', 'Natural and organic', 'ON;BC;QC', '2019-01-01', ''],
        ['LYG', 'Loyal Grocer', 'Mainstream grocery', 'All', '2019-01-01', ''],
        ['NTG', 'Northglen Foods', 'Mainstream grocery', 'AB;MB;SK;BC;ON', '2019-01-01', '2025-06-29'],
        ['NGF', 'Northglen Foods', 'Mainstream grocery', 'AB;MB;SK;BC;ON', '2025-06-30', ''],
        ['MBL', 'Marche Belvoir', 'Mainstream grocery', 'QC;NB;NS;PE;NL', '2019-01-01', '2025-06-29'],
        ['MBV', 'Marche Belvoir', 'Mainstream grocery', 'QC;NB;NS;PE;NL', '2025-06-30', ''],
        ['VLW', 'ValuWay', 'Discount', 'All', '2019-01-01', ''],
        ['TBK', 'Trade Basket', 'Discount', 'NS;NB;NL;PE;ON;QC', '2019-01-01', ''],
        ['CWC', 'Costwell Club', 'Warehouse club', 'All', '2019-01-01', ''],
    ]
    with open(path, 'w', newline='') as fh:
        w = csv.writer(fh, lineterminator='\n')
        w.writerow(['banner_cd', 'banner_name', 'channel', 'provinces', 'code_valid_from', 'code_valid_to'])
        w.writerows(rows)
    return len(rows)


def write_distribution(path, M, seed=W.SEED + 106):
    """The retail audit's weekly read of the line by banner: weighted distribution and the regular and promoted shelf
    prices its store checks recorded."""
    rng = np.random.default_rng(seed)
    nv = [s for s in M if s['family'] == -2]
    rows = []
    for t in range(W.T_LAUNCH, W.T_END + 1):
        we = (W.week_start(t) + dt.timedelta(days=6)).isoformat()
        for b in range(W.NB):
            bc = W.B_CODE[b]
            if bc == 'CWC':
                continue
            for s in nv:
                d = W.DIST[t, b]
                if d <= 0:
                    continue
                adj = 0.93 if (s['litres'] < 1 and W.DISCOUNT[b]) else 1.0
                wd = min(100.0, 100 * d * adj * (1 + rng.normal(0, 0.012)))
                reg = s['price'] if bc == 'LYG' else round(s['price'] * PR.BANNER_PRICE[bc] * 20) / 20 - 0.01
                kind = int(W.PROMO_KIND[t, b])
                pp = {1: 4.79 if s['litres'] > 1 else 3.79, 2: 3.99 if s['litres'] > 1 else 3.29,
                      3: 5.00 if s['litres'] > 1 else 4.00}.get(kind)
                rows.append([we, bc, s['ean'], '%.1f' % wd, '%.2f' % reg, '' if pp is None else '%.2f' % pp])
    with open(path, 'w', newline='') as fh:
        w = csv.writer(fh, lineterminator='\r\n')
        w.writerow(['week_ending', 'banner_cd', 'item_code', 'wtd_dist_pct', 'reg_shelf_price', 'promo_shelf_price'])
        w.writerows(rows)
    return len(rows)
