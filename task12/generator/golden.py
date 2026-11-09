"""The golden route, computed from the shipped files alone (target/), and the two golden deliverables.

Route: clean the purchase lines (rescanned receipts halved, refunds netted, item codes padded to 13 digits, both date
forms, the retailer recode); keep households reporting from 2024-W01 to 2026-W44; rebuild each household's price tier
from what it paid per litre from 2024-W01 to 2026-W14 (terciles among category buyers); read each tier's settled share
of its buyers' own category litres over the weeks without a Northvale promotion at 16 weeks or more since the buyer's
first purchase; carry every household that has bought the line into 2027 at its tier's settled share, weighted by its
own 2024-25 category litres grown to 2027; the 2027 share against the portfolio standard's bands."""
import csv
import datetime as dt
import json
import os

import numpy as np
import pandas as pd

import common as C

BANDS = [(0.0, C.BAND_EDGES[0], 'Delist'), (C.BAND_EDGES[0], C.BAND_EDGES[1], 'Hold'),
         (C.BAND_EDGES[1], C.BAND_EDGES[2], 'Support'), (C.BAND_EDGES[2], 99.0, 'Expand')]
FIRST = dt.date(2024, 1, 1)
LAUNCH_T, END_T = 118, 147                 # 2026-W15, 2026-W44 as weeks from 2024-W01
PRE_END_T = 117                            # 2026-W14
Y27 = (157, 208)                           # 2027-W01 to 2027-W52
TENURE = 16


def week_of(d):
    return (d - FIRST).days // 7


def band(share_pct):
    for lo, hi, name in BANDS:
        if lo <= share_pct < hi:
            return name


def read_master(path):
    from openpyxl import load_workbook
    ws = load_workbook(path, read_only=True)['Items']
    rows = list(ws.iter_rows(values_only=True))
    head = list(rows[0])
    out = {}
    for r in rows[1:]:
        d = dict(zip(head, r))
        size = float(d['pack_size'])
        litres = (size / 1000.0 if d['pack_uom'] == 'mL' else size) * int(d['units_per_pack'])
        out[str(d['item_code']).zfill(13)] = dict(brand=d['brand'], litres=litres, own=d['own_label_banner_cd'] or '',
                                                  segment=d['segment'], category=d['panel_category'])
    return out


def read_purchases(path, master):
    df = pd.read_csv(path, dtype={'item_code': str, 'hh_id': str, 'receipt_id': str, 'banner_cd': str, 'deal_ind': str},
                     keep_default_na=False)
    iso = df['purchase_date'].str.contains('-')
    d = pd.to_datetime(df['purchase_date'].where(iso), format='%Y-%m-%d', errors='coerce')
    d = d.fillna(pd.to_datetime(df['purchase_date'].where(~iso), format='%d/%m/%Y', errors='coerce'))
    df['date'] = d.dt.date
    df['item_code'] = df['item_code'].str.zfill(13)
    df['banner'] = df['banner_cd'].replace({'NTG': 'NGF', 'MBL': 'MBV'})
    # a receipt uploaded twice repeats every line: halve a receipt whose lines all come in identical pairs
    key = ['receipt_id', 'hh_id', 'purchase_date', 'banner_cd', 'item_code', 'qty', 'amount_paid', 'deal_ind']
    cnt = df.groupby(key, sort=False).size().rename('n').reset_index()
    even = cnt.groupby('receipt_id')['n'].apply(lambda s: bool((s % 2 == 0).all()))
    cnt['keep'] = np.where(cnt['receipt_id'].map(even), cnt['n'] // 2, cnt['n'])
    df = cnt.loc[cnt.index.repeat(cnt['keep'])].reset_index(drop=True)
    iso = df['purchase_date'].str.contains('-')
    d = pd.to_datetime(df['purchase_date'].where(iso), format='%Y-%m-%d', errors='coerce')
    d = d.fillna(pd.to_datetime(df['purchase_date'].where(~iso), format='%d/%m/%Y', errors='coerce'))
    df['date'] = d.dt.date
    df['banner'] = df['banner_cd'].replace({'NTG': 'NGF', 'MBL': 'MBV'})
    df['t'] = [week_of(x) for x in df['date']]
    df['litres'] = df['item_code'].map(lambda c: master[c]['litres']) * df['qty']
    df['brand'] = df['item_code'].map(lambda c: master[c]['brand'])
    df['nv'] = df['brand'] == 'Northvale Oat'
    df['paid'] = df['amount_paid'].astype(float)
    return df


def read_households(path):
    df = pd.read_csv(path, dtype=str, keep_default_na=False)

    def wk(s):
        if not s:
            return None
        y, w = s.split('-W')
        return week_of(dt.date.fromisocalendar(int(y), int(w), 1))
    df['join_t'] = df['joined_week'].map(wk)
    df['leave_t'] = df['left_week'].map(wk)
    for y in (2024, 2025, 2026):
        df['w%d' % y] = pd.to_numeric(df['proj_factor_%d' % y], errors='coerce')
    return df


def read_promo_weeks(path):
    from openpyxl import load_workbook
    ws = load_workbook(path, read_only=True)['2026 events']
    rows = [r for r in ws.iter_rows(values_only=True)]
    hi = next(k for k, r in enumerate(rows) if r and r[0] == 'event_id')
    head = list(rows[hi])
    weeks = set()
    for r in rows[hi + 1:]:
        d = dict(zip(head, r))
        if not d.get('event_id') or d.get('status') != 'Run':
            continue
        a = dt.date.fromisoformat(str(d['start_date'])[:10])
        b = dt.date.fromisoformat(str(d['end_date'])[:10])
        weeks.update(range(week_of(a), week_of(b) + 1))
    return weeks


def read_media_weeks(path):
    from openpyxl import load_workbook
    ws = load_workbook(path, read_only=True)['Flighting']
    rows = [r for r in ws.iter_rows(values_only=True)]
    hi = next(k for k, r in enumerate(rows) if r and r[0] == 'week_start')
    return {week_of(dt.date.fromisoformat(str(r[0])[:10])) for r in rows[hi + 1:] if r and r[0]}


def panel(target):
    f = lambda k: os.path.join(target, C.FILES[k])
    master = read_master(f('master'))
    P = read_purchases(f('purchases'), master)
    Hh = read_households(f('households'))
    promo = read_promo_weeks(f('trade'))
    ids = Hh['hh_id'].tolist()
    pos = {h: i for i, h in enumerate(ids)}
    P['i'] = P['hh_id'].map(pos)
    n = len(ids)
    nw = END_T + 1
    cat = np.zeros((nw, n)); nvl = np.zeros((nw, n)); nvq = np.zeros((nw, n))
    g = P[(P['t'] >= 0) & (P['t'] <= END_T)].groupby(['t', 'i'])
    s = g['litres'].sum()
    cat[s.index.get_level_values(0), s.index.get_level_values(1)] = s.values
    pn = P[P['nv'] & (P['t'] >= 0) & (P['t'] <= END_T)]
    s2 = pn.groupby(['t', 'i'])['litres'].sum()
    nvl[s2.index.get_level_values(0), s2.index.get_level_values(1)] = s2.values
    # purchases of the line: one per receipt carrying it
    s3 = pn[pn['qty'] > 0].groupby(['t', 'i'])['receipt_id'].nunique()
    nvq[s3.index.get_level_values(0), s3.index.get_level_values(1)] = s3.values
    first = np.full(n, -1)
    fp = pn[pn['qty'] > 0].groupby('i')['t'].min()
    first[fp.index.values] = fp.values
    pre = P[(P['t'] <= PRE_END_T) & (~P['nv'])].groupby('i')[['paid', 'litres']].sum()
    ppl = np.full(n, np.nan)
    ok = pre['litres'] > 0.5
    ppl[pre.index.values[ok.values]] = (pre['paid'] / pre['litres']).values[ok.values]
    # litres per purchase of the line, the household's own
    lp = pn[pn['qty'] > 0].groupby('i').agg(l=('litres', 'sum'), r=('receipt_id', 'nunique'))
    nvpack = np.full(n, np.nan)
    nvpack[lp.index.values] = (lp['l'] / lp['r']).values
    static = ((Hh['join_t'].isna() | (Hh['join_t'] <= 0)) & Hh['leave_t'].isna()).values
    # joined before 2024-W01 means a joined week in an earlier year
    jy = Hh['joined_week'].str[:4].astype(int).values
    static = (jy <= 2023) & Hh['leave_t'].isna().values
    buyer = static & (cat.sum(0) > 0)
    avl, a27, full_t = availability(P, f('distribution'), n)
    media = read_media_weeks(f('media'))
    return dict(P=P, H=Hh, master=master, promo=promo, media=media, cat=cat, nvl=nvl, nvq=nvq, first=first, ppl=ppl,
                nvpack=nvpack, static=static, buyer=buyer, n=n, avl=avl, a27=a27, full_t=full_t)


def availability(P, path, n):
    """category litres each household bought at banners carrying the line, week by week (each banner's litres taken
    at the line's weighted distribution there that week), and the share of its 2024-25 category litres bought at
    banners carrying the line at the review"""
    A = pd.read_csv(path, dtype={'item_code': str})
    A['t'] = [week_of(dt.date.fromisoformat(str(x)[:10])) for x in A['week_ending']]
    dist = (A.groupby(['t', 'banner_cd'])['wtd_dist_pct'].max() / 100.0).to_dict()
    cat = P[(P['t'] >= LAUNCH_T) & (P['t'] <= END_T)]
    d = np.array([dist.get((t, b), 0.0) for t, b in zip(cat['t'], cat['banner'])])
    s = (cat['litres'] * d).groupby([cat['t'], cat['i']]).sum()
    avl = np.zeros((END_T + 1, n))
    avl[s.index.get_level_values(0), s.index.get_level_values(1)] = s.values
    pre = P[(P['t'] >= 0) & (P['t'] < 104)]
    d0 = np.array([dist.get((END_T, b), 0.0) for b in pre['banner']])
    tot = pre.groupby('i')['litres'].sum()
    av = (pre['litres'] * d0).groupby(pre['i']).sum()
    a27 = np.zeros(n)
    a27[tot.index.values] = (av / tot).values
    # the first week every banner carrying the line at the review already carried it
    listed = {b for (t, b), v in dist.items() if t == END_T and v > 0}
    full_t = max(min(t for (t, b), v in dist.items() if b == bb and v > 0) for bb in listed)
    return avl, a27, full_t


def tiers(D, how='terciles'):
    ppl, buyer = D['ppl'], D['buyer']
    ok = buyer & np.isfinite(ppl)
    if how == 'terciles':
        q1, q2 = np.nanquantile(ppl[ok], [1 / 3, 2 / 3])
    elif how == 'gaps':
        q1, q2 = 2.20, 2.95
    elif how == 'q30':
        q1, q2 = np.nanquantile(ppl[ok], [0.30, 0.70])
    else:
        raise ValueError(how)
    t = np.where(ppl >= q2, 0, np.where(ppl >= q1, 1, 2))
    return np.where(np.isfinite(ppl), t, 1), (q1, q2)


def settled(D, tier, k_min=TENURE, stocked=False):
    """each price group's share of its own category litres (or, stocked, of the litres it bought where the line was
    on the shelf) over the weeks without a Northvale promotion, from buyers k_min weeks or more after first purchase"""
    first, buyer = D['first'], D['buyer']
    base = D['avl'] if stocked else D['cat']
    num = np.zeros(3); den = np.zeros(3)
    for t in range(LAUNCH_T, END_T + 1):
        if t in D['promo']:
            continue
        ok = buyer & (first >= 0) & (t - first >= k_min)
        for k in range(3):
            m = ok & (tier == k)
            num[k] += D['nvl'][t, m].sum()
            den[k] += base[t, m].sum()
    return np.divide(num, den, out=np.zeros(3), where=den > 0), den


def growth(D):
    """the category's litres per static household a week, 2025 against 2024 (projected)"""
    w = D['H']['w2026'].fillna(0).values
    st = D['static']
    a = (D['cat'][0:52, st].sum(0) * w[st]).sum()
    b = (D['cat'][52:104, st].sum(0) * w[st]).sum()
    return b / a


def litres27(D, base='v2425'):
    g = growth(D)
    if base == 'v2425':
        wk = D['cat'][0:104].sum(0) / 104.0 * g ** ((182.5 - 51.5) / 52.0)
    elif base == 'v2025':
        wk = D['cat'][52:104].sum(0) / 52.0 * g ** ((182.5 - 77.5) / 52.0)
    elif base == 'vwin':
        wk = D['cat'][LAUNCH_T:END_T + 1].sum(0) / (END_T - LAUNCH_T + 1) * g ** ((182.5 - 132.5) / 52.0)
    elif base == 'v52':
        wk = D['cat'][END_T - 51:END_T + 1].sum(0) / 52.0 * g ** ((182.5 - 121.5) / 52.0)
    elif base == 'vall':
        wk = D['cat'][0:END_T + 1].sum(0) / (END_T + 1) * g ** ((182.5 - 73.5) / 52.0)
    return wk * 52.0, g


T27_0 = 157     # panel week 2027-W01 (2026 has 53 ISO weeks)


def trial27(D, tier, fl, stocked, L27, weeks=None):
    """households not yet buying at the review: each price group's weekly first-purchase rate in the weeks that match
    the forecast's basis (every banner carrying the line, no promotion, no media), carried to the chance of a first
    purchase in 2027, with the litres and purchases that follow it (the first purchase at the usual pack, then the
    group's level for the half of the year left on average)"""
    w = D['H']['w2026'].fillna(0).values
    first, buyer = D['first'], D['buyer']
    weeks = weeks or [t for t in range(D['full_t'], END_T + 1) if t not in D['promo'] and t not in D['media']]
    pack = float(np.nanmedian(D['nvpack']))
    p27 = np.zeros(D['n'])
    for k in range(3):
        at = buyer & (tier == k)
        risk = sum((w * (at & ((first < 0) | (first >= t)))).sum() for t in weeks)
        hit = sum((w * (at & (first == t))).sum() for t in weeks)
        h = hit / risk if risk > 0 else 0.0
        m = at & (first < 0)
        p27[m] = (1 - h) ** (T27_0 - END_T - 1) * (1 - (1 - h) ** 52)
    lev = np.nan_to_num(fl[tier] * (D['a27'] if stocked else 1.0)) * np.nan_to_num(L27)
    lit = np.where(p27 > 0, p27 * (pack + lev * 0.5), 0.0)
    pur = np.where(p27 > 0, p27 * (1 + lev * 0.5 / pack), 0.0)
    return p27, lit, pur, weeks


def compute(target, how='terciles', k_min=TENURE, base='v2425', stocked=True, first_time=True):
    D = panel(target)
    tier, cuts = tiers(D, how)
    fl, den = settled(D, tier, k_min, stocked)
    L27, g = litres27(D, base)
    w = D['H']['w2026'].fillna(0).values
    st, buyer, first = D['static'], D['buyer'], D['first']
    triers = buyer & (first >= 0)
    # each buyer's 2027 share of its own litres: its group's settled share of the litres bought where the line is on
    # the shelf, times the share of its own buying done in stores carrying the line at the review
    lev = fl[tier] * (D['a27'] if stocked else 1.0)
    p27, lit_new, pur_new, tweeks = trial27(D, tier, fl, stocked, L27)
    if not first_time:
        p27, lit_new, pur_new = 0 * p27, 0 * lit_new, 0 * pur_new
    share = ((w * np.where(triers, lev, 0.0) * L27)[st].sum() + (w * lit_new)[st].sum()) / (w * L27)[st].sum()
    # Canada: the static panel raised to the 2026 universe of households
    scale = w.sum() / w[st].sum()     # the static panel raised to the 2026 factors' total
    cat27_ca = scale * (w * L27)[st].sum()
    line27_ca = share * cat27_ca
    # buyers in 2027: each household that has bought, its expected purchases of the line, the chance of at least one
    pack = np.where(np.isfinite(D['nvpack']), D['nvpack'], np.nanmedian(D['nvpack']))
    npur = np.where(triers, lev * L27 / pack, 0.0)
    pbuy = 1 - np.exp(-npur)
    buyers27 = scale * ((w * pbuy)[st].sum() + (w * p27)[st].sum())
    per_buyer = ((w * npur)[st].sum() + (w * pur_new)[st].sum()) / ((w * pbuy)[st].sum() + (w * p27)[st].sum())
    # quarters: the category's 2024-25 litres by panel quarter
    qs = []
    for a, b in ((0, 13), (13, 26), (26, 39), (39, 52)):
        qs.append(sum((D['cat'][y * 52 + a:y * 52 + b, st].sum(0) * w[st]).sum() for y in (0, 1)))
    qs = np.array(qs) / sum(qs)
    quarters = line27_ca * qs
    return dict(D=D, tier=tier, cuts=cuts, floors=fl, floor_den=den, lev=lev, stocked=stocked, share=share,
                band=band(100 * share), g=g, cat27_ca=cat27_ca, line27_ca=line27_ca, quarters=quarters,
                buyers27=buyers27, per_buyer=per_buyer, npur=npur, p27=p27, lit_new=lit_new, pur_new=pur_new,
                trial_weeks=tweeks, new_buyers=scale * (w * p27)[st].sum(),
                new_share=(w * lit_new)[st].sum() / (w * L27)[st].sum(),
                triers=int(triers.sum()), buyers=int(buyer.sum()), static=int(st.sum()), scale=scale)


def r1(x):
    return round(x + 1e-12, 1)


FAMILY = [(how, k, base) for how in ('terciles', 'gaps', 'q30', 'kmeans') for k in (14, 16, 20) for base in ('v2425', 'v2025')]


def figures_under(D, tier, k_min, base, stocked=False, first_time=True):
    fl, den = settled(D, tier, k_min, stocked)
    L27, g = litres27(D, base)
    w = D['H']['w2026'].fillna(0).values
    st, buyer, first = D['static'], D['buyer'], D['first']
    triers = buyer & (first >= 0)
    lev = fl[tier] * (D['a27'] if stocked else 1.0)
    p27, lit_new, pur_new, _ = trial27(D, tier, fl, stocked, L27)
    if not first_time:
        p27, lit_new, pur_new = 0 * p27, 0 * lit_new, 0 * pur_new
    share = ((w * np.where(triers, lev, 0.0) * L27)[st].sum() + (w * lit_new)[st].sum()) / (w * L27)[st].sum()
    scale = w.sum() / w[st].sum()     # the static panel raised to the 2026 factors' total
    cat27 = scale * (w * L27)[st].sum()
    pack = np.where(np.isfinite(D['nvpack']), D['nvpack'], np.nanmedian(D['nvpack']))
    npur = np.where(triers, lev * L27 / pack, 0.0)
    pbuy = 1 - np.exp(-npur)
    return dict(share=share, litres=share * cat27, buyers=scale * ((w * pbuy)[st].sum() + (w * p27)[st].sum()),
                per_buyer=((w * npur)[st].sum() + (w * pur_new)[st].sum()) / ((w * pbuy)[st].sum() + (w * p27)[st].sum()))


def build(target, golden_dir):
    """Write figures.json (every figure the answer blocks state) and the golden deliverables."""
    import deliver
    import rivals as V
    R = compute(target)
    D = R['D']
    fam = []
    for how, k, base in FAMILY:
        tier = V.kmeans_tiers(D) if how == 'kmeans' else tiers(D, how)[0]
        for stocked in (False, True):
            fam.append(figures_under(D, tier, k, base, stocked))
    rv, _ = V.run(D=D)
    w = D['H']['w2026'].fillna(0).values
    st, buyer, first, tier = D['static'], D['buyer'], D['first'], R['tier']
    triers = buyer & (first >= 0)
    L27, g = litres27(D, 'v2425')
    scale = R['scale']
    fl = R['floors']
    # quarters: category and line litres, share
    qs = []
    for a, b in ((0, 13), (13, 26), (26, 39), (39, 52)):
        qs.append(sum((D['cat'][y * 52 + a:y * 52 + b, st].sum(0) * w[st]).sum() for y in (0, 1)))
    qs = np.array(qs) / sum(qs)
    cat_q = R['cat27_ca'] * qs
    line_q = R['line27_ca'] * qs
    # tables
    lab = ['Premium (%.2f and above)' % R['cuts'][1], 'Mainstream (%.2f to %.2f)' % R['cuts'], 'Value (below %.2f)' % R['cuts'][0]]
    tiers_t = []
    for k in range(3):
        m = triers & (tier == k)
        tiers_t.append(dict(label=lab[k], households=int(round(scale * w[m].sum(), -4)), settled=float(fl[k]),
                            availability=float(np.average(D['a27'][m], weights=w[m])),
                            carried=float((w * R['lev'] * L27)[m].sum() / (w * L27)[m].sum()),
                            litres_behind=int(round(R['floor_den'][k])),
                            litres27=float(scale * (w * R['lev'] * L27)[m].sum())))
    rec = (G_wk(2026, 38), END_T)
    cr = D['cat'][rec[0]:rec[1] + 1].sum(0); nr = D['nvl'][rec[0]:rec[1] + 1].sum(0)
    waves = []
    for nm, a, b in (('April launch, 2026-W15 to W23', 118, G_wk(2026, 23)),
                     ('Discounter listing to September, 2026-W24 to W38', G_wk(2026, 24), G_wk(2026, 38)),
                     ('Loyal Grocer listing, 2026-W39 to W44', G_wk(2026, 39), END_T)):
        m = triers & (first >= a) & (first <= b)
        lit = (w * R['lev'] * L27)[m].sum()
        waves.append(dict(label=nm, households=int(round(scale * w[m].sum(), -4)),
                          recent=float((nr * w)[m].sum() / (cr * w)[m].sum()),
                          recent_pct=100 * float((nr * w)[m].sum() / (cr * w)[m].sum()),
                          settled=float(lit / (w * L27)[m].sum()), litres27=float(scale * lit)))
    T = dict(tiers=tiers_t, waves=waves)
    sh = [100 * f['share'] for f in fam]
    F = dict(share_pct=r1(100 * R['share']), band=R['band'], share_range=[r1(min(sh)), r1(max(sh))],
             line27_ml=r1(R['line27_ca'] / 1e6), line27_range_ml=[r1(min(f['litres'] for f in fam) / 1e6), r1(max(f['litres'] for f in fam) / 1e6)],
             category27_ml=r1(R['cat27_ca'] / 1e6), category_quarters_ml=[r1(x / 1e6) for x in cat_q],
             quarters_ml=[r1(x / 1e6) for x in line_q], quarter_share_pct=[r1(100 * R['share'])] * 4,
             buyers27=int(round(R['buyers27'] / 1e4) * 1e4),
             buyers27_range=[int(round(min(f['buyers'] for f in fam) / 1e4) * 1e4), int(round(max(f['buyers'] for f in fam) / 1e4) * 1e4)],
             per_buyer=r1(R['per_buyer']), per_buyer_range=[r1(min(f['per_buyer'] for f in fam)), r1(max(f['per_buyer'] for f in fam))],
             floors_pct=[r1(100 * f) for f in fl], cuts_ppl=[round(c, 2) for c in R['cuts']], growth=round(R['g'], 3),
             triers_panel=R['triers'], buyers_panel=R['buyers'], static_panel=R['static'],
             triers_ca=int(round(scale * w[triers].sum(), -4)),
             waves=[dict(label=x['label'], households=int(x['households']), recent_pct=r1(100 * x['recent']),
                         settled_pct=r1(100 * x['settled'])) for x in waves],
             rejected=dict(pc_careful=r1(100 * rv['pc_careful']), pc_naive=r1(100 * rv['pc_naive']),
                           april_for_all=r1(100 * rv['april_for_all']), cohort_recent=r1(100 * rv['cohort_own_recent']),
                           unsupported_weeks=r1(100 * rv['quiet_w27_w38']), last_week=r1(100 * rv['last_week']),
                           buying_index_one=r1(100 * rv['pc_B1']), recent_share=r1(100 * rv['recent_share']),
                           window_volumes=r1(100 * figures_under(D, tier, TENURE, 'vwin', True)['share'])),
             pc_terms=dict(P=r1(100 * rv['P']), R=r1(100 * rv['R_mat']), B=round(rv['B_win'], 2)),
             category_quarters_raw=[float(x) for x in cat_q], quarters_raw=[float(x) for x in line_q],
             quarter_share_raw=[float(R['share'])] * 4, buyers27_raw=float(R['buyers27']), per_buyer_raw=float(R['per_buyer']))
    F['quarters_ml'] = [r1(x / 1e6) for x in line_q]
    F['bands_pct'] = [BANDS[1][0], BANDS[2][0], BANDS[3][0]]
    F['growth_pct'] = r1(100 * (R['g'] - 1))
    F['tenure_weeks'] = TENURE
    fr, _ = settled(D, tier, TENURE, stocked=False)
    raw = figures_under(D, tier, TENURE, 'v2425', stocked=False)
    F['raw'] = dict(share_pct=r1(100 * raw['share']), floors_pct=[r1(100 * x) for x in fr])
    F['availability_pct'] = [int(round(100 * t['availability'])) for t in tiers_t]
    F['carried_pct'] = [r1(100 * t['carried']) for t in tiers_t]
    # the rung-2 routes the write-up names: the honeymoon taken, the price groups skipped
    z = np.zeros(D['n'], dtype=int)
    flp, _ = settled(D, z, TENURE)
    pooled = (w * np.where(triers, flp[0], 0.0) * L27)[st].sum() / (w * L27)[st].sum()
    F['rung2'] = dict(pooled_pct=r1(100 * pooled), pooled_level_pct=r1(100 * flp[0]),
                      april_level_route_pct=r1(100 * V.per_wave(D, TENURE, 'april')))
    mix = []
    for m in V.waves_of(D):
        tot = (w * L27)[m].sum()
        mix.append([int(round(100 * (w * L27)[m & (tier == k)].sum() / tot)) for k in range(3)])
    F['wave_mix_pct'] = mix
    R0 = figures_under(D, tier, TENURE, 'v2425', stocked=True, first_time=False)
    F['households_2026'] = int(round(w.sum()))
    F['static_scale'] = round(float(scale), 3)
    F['new_trial'] = dict(buyers=int(round(R['new_buyers'], -4)), points=round(100 * R['new_share'], 2),
                          share_without_pct=r1(100 * R0['share']),
                          weeks=['2026-W%02d' % (t - 103) for t in R['trial_weeks']])
    F['rung2']['disc_level_route_k8_pct'] = r1(100 * V.per_wave(D, 8, 'discounter'))
    F['rung2']['disc_level_route_pct'] = r1(100 * V.per_wave(D, TENURE, 'discounter'))
    F['fixed_cuts_ppl'] = [round(c, 2) for c in tiers(D, 'gaps')[1]]
    F['rung2']['no_tenure_cut_pct'] = r1(100 * figures_under(D, tier, 1, 'v2425', True)['share'])
    F['rung2']['no_tenure_cut_raw_pct'] = r1(100 * figures_under(D, tier, 1, 'v2425', False)['share'])
    for k in (8, 20):
        flk, _ = settled(D, z, k)
        F['rung2']['pooled_k%d_pct' % k] = r1(100 * (w * np.where(triers, flk[0], 0.0) * L27)[st].sum() / (w * L27)[st].sum())
    F['tiers'] = [dict(label=t['label'], households=t['households'], settled_pct=r1(100 * t['settled']),
                       litres27_ml=r1(t['litres27'] / 1e6)) for t in tiers_t]
    for x, y in zip(F['waves'], waves):
        x['litres27_ml'] = r1(y['litres27'] / 1e6)
    dial = [figures_under(D, V.kmeans_tiers(D) if how == 'kmeans' else tiers(D, how)[0], k, b, s)['share']
            for how in ('terciles', 'gaps', 'q30', 'kmeans') for k in (14, 16, 20) for b in ('vwin', 'v52', 'vall') for s in (False, True)]
    F['dial_max_pct'] = r1(100 * max(dial))
    npur = R['npur']
    F['tier_purchases'] = [r1(np.average(npur[triers & (tier == k)], weights=w[triers & (tier == k)])) for k in range(3)]
    F['tier_pbuy_pct'] = [int(round(100 * np.average(1 - np.exp(-npur[triers & (tier == k)]), weights=w[triers & (tier == k)])))
                          for k in range(3)]
    json.dump(F, open(os.path.join(C.HERE, 'figures.json'), 'w'), indent=1)
    deliver.build(F, T, golden_dir)
    return R, F, T


def G_wk(y, w):
    return week_of(dt.date.fromisocalendar(y, w, 1))


if __name__ == '__main__':
    import sys
    R = compute(C.TARGET)
    print('static %d, buyers %d, triers %d; tier cuts %.2f / %.2f $/L; growth %.3f' % (R['static'], R['buyers'], R['triers'], R['cuts'][0], R['cuts'][1], R['g']))
    print('settled shares by tier %s (litres behind them %s)' % (np.round(100 * R['floors'], 2), np.round(R['floor_den']).astype(int)))
    print('2027 share %.3f%% -> %s; line litres %.2f M of %.1f M; quarters %s M; buyers %.0f; per buyer %.2f' % (
        100 * R['share'], R['band'], R['line27_ca'] / 1e6, R['cat27_ca'] / 1e6, np.round(R['quarters'] / 1e6, 2), R['buyers27'], R['per_buyer']))
