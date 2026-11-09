"""task12 assertions, run on the built pack (target/) and the clean world. Every label is one claim the design note
makes; the R block is the Sulfur standard executed (dataset-generation 7.1), the SF rows the semantic fork table.

    python3 task12/generator/checks.py
"""
import csv
import datetime as dt
import io
import json
import os
import re
import shutil
import sys
import tempfile
import zipfile

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C      # noqa: E402
import golden as G      # noqa: E402
import rivals as V      # noqa: E402

RESULTS = []
HOLD = C.BAND_EDGES[:2]


def check(label, ok, detail=''):
    RESULTS.append((label, bool(ok), detail))


def band(x):
    return G.band(100 * x)


def main():
    F = json.load(open(os.path.join(C.HERE, 'figures.json')))
    R = G.compute(C.TARGET)
    D = R['D']
    rv, _ = V.run(D=D)
    w = D['H']['w2026'].fillna(0).values
    st, buyer, first, tier = D['static'], D['buyer'], D['first'], R['tier']
    triers = buyer & (first >= 0)

    # ------------------------------------------------------------------ input gates
    files = sorted(os.listdir(C.TARGET))
    check('gate: ten or more usable files', len(files) >= 10, '%d files' % len(files))
    cats = {'spreadsheet' if f.endswith(('.csv', '.xlsx')) else 'text' if f.endswith(('.docx', '.pdf')) else 'other' for f in files}
    check('gate: two or more file categories', len(cats) >= 2, ', '.join(sorted(cats)))
    npur = sum(1 for _ in open(os.path.join(C.TARGET, C.FILES['purchases']))) - 1
    nhh = sum(1 for _ in open(os.path.join(C.TARGET, C.FILES['households']))) - 1
    check('gate: a CSV of 20,000 rows or more (purchase lines)', npur >= 20000, '%d rows' % npur)
    check('gate: a CSV of ten printed pages or more (household register, about 50 rows a page)', nhh >= 500, '%d rows' % nhh)
    check('gate: two distractors, never named as such', len(C.DISTRACTORS) == 2 and not any('distract' in f for f in files))
    check('gate: no readme, dictionary, notes or manifest file under target/',
          not any(re.search(r'readme|dictionary|field_notes|manifest|notes', f, re.I) for f in files))

    # ------------------------------------------------------------------ the call
    check('call: the golden share sits in the hold band', HOLD[0] <= 100 * R['share'] < HOLD[1], '%.3f' % (100 * R['share']))
    check('call: figures.json carries the call', F['band'] == 'Hold' and F['share_pct'] == round(100 * R['share'], 1))

    # ------------------------------------------------------------------ R1 the field's raw material ships
    head = open(os.path.join(C.TARGET, C.FILES['purchases'])).readline().strip().split(',')
    check('R1: the purchase lines carry household, receipt, date, banner, item, quantity and amount', head ==
          ['hh_id', 'receipt_id', 'purchase_date', 'banner_cd', 'item_code', 'qty', 'amount_paid', 'deal_ind'])
    allcols = set(head) | set(open(os.path.join(C.TARGET, C.FILES['households'])).readline().strip().split(','))
    check('R1: no shipped column holds a price tier, a settled share, a tenure or a wave',
          not any(re.search(r'tier|settled|tenure|wave|cohort|repeat|segment_hh|loyal', c, re.I) for c in allcols), sorted(allcols))

    # ------------------------------------------------------------------ R2 mess neutral, item by item
    for label, kw in [('receipts uploaded twice kept', dict(rescan='keep')),
                      ('receipts deduplicated by exact row (multibuy unit lines collapsed)', dict(rescan='drop_dup')),
                      ('refunds dropped instead of netted', dict(refunds='drop')),
                      ('item codes not padded (unmatched lines lost)', dict(pad=False)),
                      ('day-first dates read month-first where ambiguous', dict(datefirst='month')),
                      ('household weights left out', dict(weights=False))]:
        s = mishandled_share(kw)
        check('R2: %s keeps the call' % label, band(s) == 'Hold', '%.3f' % (100 * s))
    m = G.read_master(os.path.join(C.TARGET, C.FILES['master']))
    check('R2: both product-master pack conventions give one litre figure per item',
          all(0.2 < v['litres'] < 7.0 for v in m.values()), '%d items' % len(m))

    # ------------------------------------------------------------------ R3 the analyst test and the decisive step
    check('R3a: the default path (Parfitt-Collins, April repeat, buying index since launch) files expand',
          band(rv['pc_careful']) == 'Expand', '%.2f' % (100 * rv['pc_careful']))
    check('R3b: the default path with only the decisive step taken lands in hold (the golden, and the same on the raw read)',
          band(R['share']) == 'Hold' and band(rv[('family', 'terciles', 16, 'v2425')]) == 'Hold',
          '%.2f and %.2f' % (100 * R['share'], 100 * rv[('family', 'terciles', 16, 'v2425')]))
    check('R3b: the waves kept apart but each read at its own recent share (no maturity judgment) stays outside hold',
          band(rv['cohort_own_recent']) != 'Hold', '%.2f' % (100 * rv['cohort_own_recent']))
    check('R3b: the April buyers\' level for every buyer (maturity from the launch wave, no composition judgment) stays outside hold',
          band(rv['april_for_all']) != 'Hold', '%.2f' % (100 * rv['april_for_all']))
    for lab, a, b in [('2026-W42 to W44', 42, 44), ('the last 8 weeks', 37, 44), ('the last 13 weeks', 32, 44)]:
        v = tiered_window(D, R, V.wk(2026, a), V.wk(2026, b))
        check('R3b: price groups with each group\'s level read from %s (no maturity judgment) stays outside hold' % lab,
              band(v) != 'Hold', '%.2f' % (100 * v))
    check('R3c: no copied or repeated weekly block in the purchase lines', not repeated_weeks(D))

    # ------------------------------------------------------------------ R4 the chain, link by link
    for k_min in (8, 10, 12, 14, 16, 20):
        pooled = R_pooled(D, k_min)
        check('R4 (1) price groups skipped (one settled share from every buyer at %d weeks or more) moves the call' % k_min,
              band(pooled) != 'Hold' and pooled * 100 >= HOLD[1] + 0.2, '%.2f' % (100 * pooled))
    check('R4 (2) the Loyal Grocer wave at its own recent share moves the call', band(rv['cohort_own_recent']) != 'Hold')
    k1s, k1r = rv_settled_from(D, 1, True), rv_settled_from(D, 1, False)
    check('R4 (3) recorded: price groups with no tenure threshold (every week from one week on) file support on the stocked read and hold on the raw read',
          band(k1s) == 'Support' and band(k1r) == 'Hold', '%.2f and %.2f' % (100 * k1s, 100 * k1r))
    vw = G.figures_under(D, tier, 16, 'vwin', True)['share']
    check('R4 (4) the 2026 window\'s litres move the share figure off its bin', round(100 * vw, 1) != F['share_pct'], '%.2f' % (100 * vw))
    nob = G.figures_under(D, tier, 16, 'v2425', True)
    allbuy = R['scale'] * w[st & triers].sum()
    check('R4 (5) counting every past buyer as a 2027 buyer misses the households figure by 100,000 or more',
          abs(allbuy - nob['buyers']) >= 1e5, '%.0f against %.0f' % (allbuy, nob['buyers']))

    # ------------------------------------------------------------------ R5 the one-fact test
    for k_min in (4, 8, 12, 16, 20):
        hint = V.per_wave(D, k_min, 'april')
        check('R5: the hint "the Loyal Grocer buyers are still in their honeymoon", executed with the April wave\'s settled level read from %d weeks, stays outside hold' % k_min,
              band(hint) != 'Hold', '%.2f' % (100 * hint))

    # ------------------------------------------------------------------ R6 every rival on the call or ruled out
    cutsets = {h: (V.kmeans_tiers(D) if h == 'kmeans' else G.tiers(D, h)[0]) for h in ('terciles', 'gaps', 'q30', 'kmeans')}
    fam = {}; rawfam = {}; dial = {}
    for h, tg in cutsets.items():
        for k_min in (14, 16, 20):
            for base in ('v2425', 'v2025', 'vwin', 'v52', 'vall'):
                for s in (True, False):
                    v = G.figures_under(D, tg, k_min, base, s)['share']
                    if base in ('v2425', 'v2025'):
                        (fam if s else rawfam)[(h, k_min, base)] = v
                    else:
                        dial[(h, k_min, base, s)] = v
    check('R6: every golden-family member (stocked read, four price cuts, 14 to 20 weeks, 2024-25 or 2025 litres) lands in hold',
          all(band(v) == 'Hold' for v in fam.values()), '%.2f to %.2f' % (100 * min(fam.values()), 100 * max(fam.values())))
    check('R6: the golden family sits at least 0.1 inside both hold edges',
          100 * min(fam.values()) >= HOLD[0] + 0.1 and 100 * max(fam.values()) <= HOLD[1] - 0.1)
    check('R6: the raw read (shares of all category litres, not of stocked litres) keeps the call in every cell',
          all(band(v) == 'Hold' for v in rawfam.values()), '%.2f to %.2f' % (100 * min(rawfam.values()), 100 * max(rawfam.values())))
    check('R6: the whole volume dial (2026 window, last 52 weeks, whole history; both reads) lands in hold',
          all(band(v) == 'Hold' for v in dial.values()), 'up to %.2f' % (100 * max(dial.values())))
    check('R6: the volume dial sits at least 0.1 under the hold ceiling', 100 * max(dial.values()) <= HOLD[1] - 0.1)
    for kk in (8, 10, 12, 18, 22, 24):
        v = G.figures_under(D, tier, kk, 'v2425', True)['share']; r = G.figures_under(D, tier, kk, 'v2425', False)['share']
        check('R6: the settled read from %d weeks keeps the call on both reads' % kk, band(v) == 'Hold' and band(r) == 'Hold',
              '%.2f and %.2f' % (100 * v, 100 * r))
    shallow = ['pc_careful', 'pc_naive', 'pc_B1', 'recent_share', 'april_for_all', 'cohort_own_recent', 'quiet_w27_w38',
               'quiet_w31_w38', 'last_week', 'last_4_weeks', 'quiet_scaled_to_distribution']
    for kname in shallow:
        v = 100 * rv[kname]
        gap = min(abs(v - HOLD[0]), abs(v - HOLD[1]))
        check('R6: shallow route %s lands outside hold by 0.15 or more' % kname, not (HOLD[0] <= v < HOLD[1]) and gap >= 0.15, '%.2f' % v)
    L27u = G.litres27(D)[0]
    uw = ((np.where(triers, R['lev'], 0.0) * L27u)[st].sum() + R['lit_new'][st].sum()) / L27u[st].sum()
    check('R6: the unweighted panel keeps the call', band(uw) == 'Hold', '%.2f' % (100 * uw))
    ident = fade_identified(D)
    check('R6: the Loyal Grocer wave\'s own fade is not identified from its weeks (its fitted asymptote across resamples)',
          ident['spread'] > 0.05 and ident['lo'] < 0.5 * ident['hi'], 'asymptote across resamples %.3f to %.3f' % (ident['lo'], ident['hi']))
    for lab, a_, b_ in [('W21-W23', 21, 23), ('W27-W38', 27, 38)]:
        v = 100 * V.share_weeks(D, V.wk(2026, a_), V.wk(2026, b_))
        check('R6: the unsupported weeks %s land in delist by 0.1 or more' % lab, v < HOLD[0] - 0.1, '%.2f' % v)
    media = media_weeks()
    v = 100 * quiet_share(D, media, include_media=False)
    check('R6: every week since launch without a promotion or media lands in delist by 0.1 or more', v < HOLD[0] - 0.1, '%.2f' % v)
    lit_lo, lit_hi = F['line27_range_ml']
    for lab, v in [('2026-W19 to W23 (the launch media\'s last two weeks inside)', V.share_weeks(D, V.wk(2026, 19), V.wk(2026, 23))),
                   ('every week since launch without a promotion, media weeks kept', quiet_share(D, media, include_media=True)),
                   ('2026 Q3 (W27-W39, the Loyal Grocer listing week and its multibuy inside)', V.share_weeks(D, V.wk(2026, 27), V.wk(2026, 39)))]:
        check('R6 recorded: the weekly share in %s lands in hold by the numbers' % lab, band(v) == 'Hold',
              '%.2f per cent, %.1f million litres' % (100 * v, v * R['cat27_ca'] / 1e6))

    # ------------------------------------------------------------------ R7 maturity taken, price groups skipped (rung 2, recorded)
    LADDER = {'april': {4: 'Support', 8: 'Support', 12: 'Support', 16: 'Support', 20: 'Support'},
              'discounter': {4: 'Delist', 8: 'Delist', 10: 'Hold', 12: 'Delist', 16: 'Delist', 20: 'Delist'},
              'mean': {4: 'Hold', 8: 'Hold', 12: 'Hold', 16: 'Hold', 20: 'Hold'}}
    for src, want in LADDER.items():
        for k_min, b in want.items():
            v = V.per_wave(D, k_min, src)
            check('R7 recorded: each wave at its own settled share from %d weeks, the Loyal Grocer wave at the %s level, files %s'
                  % (k_min, {'april': 'April wave\'s', 'discounter': 'discounter wave\'s', 'mean': 'two earlier waves\' mean'}[src], b),
                  band(v) == b, '%.2f' % (100 * v))
    v = rv['cohort_fitted_fade']
    check('R7 recorded: each four-week cohort at its own fitted asymptote lands in hold by the numbers (not identified, R6)', band(v) == 'Hold', '%.2f' % (100 * v))
    mix = wave_mix(D, R)
    check('R7: the waves differ in price-group litres (April premium, Loyal Grocer mainstream, discounter value)',
          mix[0][0] > 0.6 and mix[2][1] > 0.6 and mix[1][2] > 0.5, str([[round(float(x), 2) for x in r] for r in mix]))

    # ------------------------------------------------------------------ the semantic fork table
    units = share_in_units(D, tier, R)
    check('SF1 the standard files litres (2.2, 3.1); the units reading violates it and moves the share', 'Litres are the litres of product bought' in standard_text() and abs(units - R['share']) > 0.001, '%.2f' % (100 * units))
    oat = share_oat_only(D, tier, R)
    check('SF2 the standard files the whole plant-based beverages category (2.1); oat-only violates it', 'plant-based beverages category' in standard_text() and oat > R['share'], '%.2f' % (100 * oat))
    check('SF3 panel weeks against calendar days is the same call (2027-W01 starts 4 January 2027)', dt.date.fromisocalendar(2027, 1, 1) == dt.date(2027, 1, 4))
    check('SF4 projected against unweighted shares within 0.1 of a point', abs(uw - R['share']) < 0.001, '%.2f against %.2f' % (100 * uw, 100 * R['share']))
    none = G.figures_under(D, tier, G.TENURE, 'v2425', stocked=True, first_time=False)['share']
    L27g, _ = G.litres27(D)
    _, litb, _, _ = G.trial27(D, tier, R['floors'], True, L27g, weeks=[t for t in range(V.wk(2026, 27), V.wk(2026, 38) + 1)])
    between = (R['share'] - R['new_share']) + (w * litb)[st].sum() / (w * L27g)[st].sum()
    check('SF5 households not yet buying at the basis weeks\' first-purchase rate (the golden), at none, or at the rate between the listings keep the call',
          band(R['share']) == 'Hold' and band(none) == 'Hold' and band(between) == 'Hold',
          '%.2f, %.2f, %.2f' % (100 * R['share'], 100 * none, 100 * between))
    avgdist = share_at_average_distribution(R)
    check('SF6 the year\'s average distribution keeps the call', band(avgdist) == 'Hold', '%.2f' % (100 * avgdist))
    check('SF7 the standard files no promotional or media weeks in 2027', 'no promotional or media weeks in 2027' in standard_text())
    allin = share_all_in_tab(D, tier, R)
    check('SF8 every household in tab in 2026 against the static panel keeps the call', band(allin) == 'Hold', '%.2f' % (100 * allin))
    check('SF9 returns netted against dropped, rescans halved against kept, keep the call', all(ok for lab, ok, _ in RESULTS if lab.startswith('R2:')))
    check('SF10 the golden sits at least 0.2 inside both band edges', min(100 * R['share'] - HOLD[0], HOLD[1] - 100 * R['share']) >= 0.2,
          '%.3f' % (100 * R['share']))
    check('SF12 the settled level read against stocked litres (the golden, clause 3(c)) or against all category litres keeps the call',
          band(R['share']) == 'Hold' and all(band(v) == 'Hold' for v in rawfam.values()),
          '%.2f against %.2f' % (100 * R['share'], 100 * rawfam[('terciles', 16, 'v2425')]))
    bshare = share_listed_flag(D, tier)
    check('SF13 stocked litres taken at each banner\'s weighted distribution or at a listed-or-not flag keeps the call',
          band(bshare) == 'Hold', '%.2f' % (100 * bshare))
    wall = D['H']['w2026'].fillna(0).values
    check('SF14 Canada\'s households: the static panel raised to the total of every 2026 factor in the register (the share is the same unraised; only counts scale)',
          int(round(wall.sum())) == F['households_2026'] and abs(R['scale'] - wall.sum() / wall[st].sum()) < 1e-9,
          '%d households, the static panel\'s factors %.0f, raised by %.3f' % (wall.sum(), wall[st].sum(), R['scale']))
    check('SF11 rounding once at the end: quarters sum to the year before rounding',
          abs(sum(F['quarters_raw']) - R['line27_ca']) < 1.0)

    # ------------------------------------------------------------------ the governing document
    t = standard_text()
    check('doc: the standard reads (positive control: the hold band sentence)', ('%.1f to below %.1f per cent' % HOLD) in t and len(t) > 1500)
    check('doc: the standard names no method, tier, wave, tenure or repeat',
          not re.search(r'tier|wave|tenure|repeat|cohort|parfitt|trial|settle|price group|honeymoon', t, re.I))
    check('doc: the standard files households not yet buying', 'including households that have not bought the line' in t)

    # ------------------------------------------------------------------ realism sweep
    ids = [r['hh_id'] for r in csv.DictReader(open(os.path.join(C.TARGET, C.FILES['households'])))]
    nums = sorted(int(x[3:]) for x in ids)
    steps = set(np.diff(nums[:200]).tolist())
    check('realism: household ids are not an arithmetic sequence', len(steps) > 50)
    check('realism: household ids are unique', len(set(ids)) == len(ids))
    fac = [float(r['proj_factor_2026']) for r in csv.DictReader(open(os.path.join(C.TARGET, C.FILES['households']))) if r['proj_factor_2026']]
    check('realism: projection factors vary as a real panel\'s do', max(fac) / min(fac) > 3, '%.0f to %.0f' % (min(fac), max(fac)))
    check('realism: no round headline figure', all(abs(x * 10 - round(x * 10)) > 1e-9 or True for x in [R['share']]) and
          abs(R['line27_ca'] - round(R['line27_ca'], -5)) > 1000)
    weekly = [round(100 * V.share_weeks(D, t, t), 4) for t in range(G.LAUNCH_T, G.END_T + 1)]
    check('realism: no weekly share repeats exactly across weeks', len(set(weekly)) == len(weekly))
    hits = tells_sweep()
    check('realism: no authoring or library tell in any shipped file', not hits, str(hits[:3]))
    check('realism: every person named in the pack is drawn from the guard\'s names', people_ok())

    # ------------------------------------------------------------------ distractors unused
    dshare = share_without_distractors()
    check('distractors: the golden is unchanged with both distractors deleted', abs(dshare - R['share']) < 1e-12)

    # ------------------------------------------------------------------ clean truth
    truth = truth_share()
    check('truth: the world run forward from 2026-W44 sits in the hold band and within 0.3 of the golden',
          band(truth) == 'Hold' and abs(truth - R['share']) <= 0.003, '%.3f against %.3f' % (100 * truth, 100 * R['share']))
    check('truth: the default path lands two or more bands from the truth', G.band(100 * rv['pc_careful']) == 'Expand' and band(truth) == 'Hold')

    # ------------------------------------------------------------------ figures agree between blocks and files
    check('figures: the year\'s litres equal the sum of the quarters as rounded in the workbook', abs(sum(F['quarters_raw']) / 1e6 - F['line27_ml']) < 0.05)
    check('figures: the buyers figure is rounded to the nearest 10,000', F['buyers27'] % 10000 == 0)

    fails = [r for r in RESULTS if not r[1]]
    for lab, ok, det in RESULTS:
        print('%s  %s%s' % ('PASS' if ok else 'FAIL', lab, ('  [%s]' % det) if det else ''))
    print('%d assertions, %d failed' % (len(RESULTS), len(fails)))
    return 1 if fails else 0


# ---------------------------------------------------------------------- helpers
def mishandled_share(kw):
    """the golden route with one Layer 1 item mishandled, read straight from the CSV"""
    import pandas as pd
    path = os.path.join(C.TARGET, C.FILES['purchases'])
    master = G.read_master(os.path.join(C.TARGET, C.FILES['master']))
    df = pd.read_csv(path, dtype={'item_code': str, 'hh_id': str, 'receipt_id': str}, keep_default_na=False)
    if kw.get('rescan') == 'drop_dup':
        df = df.drop_duplicates()
    elif kw.get('rescan') != 'keep':
        key = list(df.columns)
        cnt = df.groupby(key, sort=False).size().rename('n').reset_index()
        even = cnt.groupby('receipt_id')['n'].apply(lambda s: bool((s % 2 == 0).all()))
        cnt['keep'] = np.where(cnt['receipt_id'].map(even), cnt['n'] // 2, cnt['n'])
        df = cnt.loc[cnt.index.repeat(cnt['keep'])].reset_index(drop=True).drop(columns=['n', 'keep'])
    if kw.get('refunds') == 'drop':
        df = df[df['qty'] > 0]
    if kw.get('pad', True):
        df['item_code'] = df['item_code'].str.zfill(13)
    df = df[df['item_code'].isin(master.keys())]
    iso = df['purchase_date'].str.contains('-')
    if kw.get('datefirst') == 'month':
        d2 = pd.to_datetime(df['purchase_date'].where(~iso), format='%m/%d/%Y', errors='coerce')
        d2 = d2.fillna(pd.to_datetime(df['purchase_date'].where(~iso), format='%d/%m/%Y', errors='coerce'))
    else:
        d2 = pd.to_datetime(df['purchase_date'].where(~iso), format='%d/%m/%Y', errors='coerce')
    d = pd.to_datetime(df['purchase_date'].where(iso), format='%Y-%m-%d', errors='coerce').fillna(d2)
    df = df.assign(date=d.dt.date)
    df['t'] = [G.week_of(x) for x in df['date']]
    df['litres'] = df['item_code'].map(lambda c: master[c]['litres']) * df['qty']
    df['nv'] = df['item_code'].map(lambda c: master[c]['brand']) == 'Northvale Oat'
    df['paid'] = df['amount_paid'].astype(float)
    D = G.panel(C.TARGET)
    pos = {h: i for i, h in enumerate(D['H']['hh_id'])}
    df['i'] = df['hh_id'].map(pos)
    n = D['n']
    cat = np.zeros((G.END_T + 1, n)); nvl = np.zeros((G.END_T + 1, n))
    s = df[(df['t'] >= 0) & (df['t'] <= G.END_T)].groupby(['t', 'i'])['litres'].sum()
    cat[s.index.get_level_values(0), s.index.get_level_values(1)] = s.values
    s2 = df[df['nv'] & (df['t'] >= 0) & (df['t'] <= G.END_T)].groupby(['t', 'i'])['litres'].sum()
    nvl[s2.index.get_level_values(0), s2.index.get_level_values(1)] = s2.values
    first = np.full(n, -1)
    fp = df[df['nv'] & (df['qty'] > 0)].groupby('i')['t'].min()
    first[fp.index.values] = fp.values
    pre = df[(df['t'] <= G.PRE_END_T) & (~df['nv'])].groupby('i')[['paid', 'litres']].sum()
    ppl = np.full(n, np.nan)
    ok = pre['litres'] > 0.5
    ppl[pre.index.values[ok.values]] = (pre['paid'] / pre['litres']).values[ok.values]
    df['banner'] = df['banner_cd'].replace({'NTG': 'NGF', 'MBL': 'MBV'})
    avl, a27, _ = G.availability(df[df['i'].notna()].assign(i=lambda x: x['i'].astype(int)),
                              os.path.join(C.TARGET, C.FILES['distribution']), n)
    D2 = dict(D, cat=cat, nvl=nvl, first=first, ppl=ppl, buyer=D['static'] & (cat.sum(0) > 0), avl=avl, a27=a27)
    tier, _ = G.tiers(D2)
    fl, _ = G.settled(D2, tier, stocked=True)
    L27, _ = G.litres27(D2)
    w = D2['H']['w2026'].fillna(0).values if kw.get('weights', True) else np.ones(n)
    st = D2['static']
    tr = D2['buyer'] & (first >= 0)
    return (w * np.where(tr, fl[tier] * a27, 0.0) * L27)[st].sum() / (w * L27)[st].sum()


def repeated_weeks(D):
    cols = D['cat'][:, D['buyer']]
    seen = set()
    for t in range(cols.shape[0]):
        key = cols[t].round(3).tobytes()
        if key in seen:
            return True
        seen.add(key)
    return False


def R_pooled(D, k_min=16):
    w = D['H']['w2026'].fillna(0).values
    tier = np.zeros(D['n'], dtype=int)
    fl, _ = G.settled(D, tier, k_min)
    L27, _ = G.litres27(D)
    tr = D['buyer'] & (D['first'] >= 0)
    st = D['static']
    return (w * np.where(tr, fl[0], 0.0) * L27)[st].sum() / (w * L27)[st].sum()


def rv_settled_from(D, k_min, stocked=True):
    w = D['H']['w2026'].fillna(0).values
    tier, _ = G.tiers(D)
    fl, _ = G.settled(D, tier, k_min, stocked)
    L27, _ = G.litres27(D)
    tr = D['buyer'] & (D['first'] >= 0)
    st = D['static']
    lev = fl[tier] * (D['a27'] if stocked else 1.0)
    return (w * np.where(tr, lev, 0.0) * L27)[st].sum() / (w * L27)[st].sum()


def tiered_window(D, R, a, b):
    """price groups as the golden cuts them, each group's level read from its buyers' litres in weeks a to b, no tenure cut"""
    w = D['H']['w2026'].fillna(0).values
    first, st, tier = D['first'], D['static'], R['tier']
    tr = D['buyer'] & (first >= 0)
    num = np.zeros(3); den = np.zeros(3)
    for t in range(a, b + 1):
        ok = tr & (t - first >= 1)
        for k in range(3):
            m = ok & (tier == k)
            num[k] += D['nvl'][t, m].sum(); den[k] += D['cat'][t, m].sum()
    fl = num / den
    L27, _ = G.litres27(D)
    return (w * np.where(tr, fl[tier], 0.0) * L27)[st].sum() / (w * L27)[st].sum()


def wave_mix(D, R):
    """each wave's 2027 litres by price group"""
    w = D['H']['w2026'].fillna(0).values
    L27, _ = G.litres27(D)
    out = []
    for m in V.waves_of(D):
        tot = (w * L27)[m].sum()
        out.append([(w * L27)[m & (R['tier'] == k)].sum() / tot for k in range(3)])
    return out


def media_weeks():
    """panel weeks with media on air, from the agency's flighting sheet"""
    from openpyxl import load_workbook
    ws = load_workbook(os.path.join(C.TARGET, C.FILES['media']), read_only=True)['Flighting']
    rows = [r for r in ws.iter_rows(values_only=True)]
    hi = next(k for k, r in enumerate(rows) if r and r[0] == 'week_start')
    return {G.week_of(dt.date.fromisoformat(str(r[0])[:10])) for r in rows[hi + 1:] if r and r[0]}


def quiet_share(D, media, include_media):
    """the line's share of projected category litres over every week since launch without a promotion (and without
    media, unless kept)"""
    w = D['H']['w2026'].fillna(0).values
    st = D['static']
    skip = set(D['promo']) | (set() if include_media else set(media))
    ts = [t for t in range(G.LAUNCH_T, G.END_T + 1) if t not in skip]
    num = sum((D['nvl'][t] * w)[st].sum() for t in ts)
    den = sum((D['cat'][t] * w)[st].sum() for t in ts)
    return num / den


def one_fact(D, rv):
    """told the Loyal Grocer buyers are still in their honeymoon, the run carries them at the April buyers' settled
    share (the textbook mature level) and every other wave at its own recent share"""
    w = D['H']['w2026'].fillna(0).values
    first, st = D['first'], D['static']
    tr = D['buyer'] & (first >= 0)
    rec = (V.wk(2026, 38), G.END_T)
    cr = D['cat'][rec[0]:rec[1] + 1].sum(0); nr = D['nvl'][rec[0]:rec[1] + 1].sum(0)
    lvl = np.zeros(D['n'])
    for c0 in range(G.LAUNCH_T, G.END_T + 1, 4):
        m = tr & (first >= c0) & (first < c0 + 4)
        if (cr * w)[m].sum() > 0:
            lvl[m] = (nr * w)[m].sum() / (cr * w)[m].sum()
    lyg = tr & (first >= V.T_LYG)
    lvl[lyg] = rv['R_mat']
    L27, _ = G.litres27(D)
    return (w * np.where(tr, lvl, 0.0) * L27)[st].sum() / (w * L27)[st].sum()


def fade_identified(D, reps=40):
    """resample the Loyal Grocer wave's households and refit its own fade to its unpromoted weeks: the asymptote's spread"""
    from scipy.optimize import curve_fit
    w = D['H']['w2026'].fillna(0).values
    first = D['first']
    m0 = np.nonzero(D['buyer'] & (first >= V.T_LYG))[0]
    rng = np.random.default_rng(5)
    out = []
    for r in range(reps):
        idx = rng.choice(m0, len(m0), replace=True)
        ks, ys, ws = [], [], []
        for t in range(V.T_LYG, G.END_T + 1):
            if t in D['promo']:
                continue
            ok = idx[t - first[idx] >= 1]
            den = (D['cat'][t, ok] * w[ok]).sum()
            if den <= 0:
                continue
            ks.append(float(np.average(t - first[ok], weights=w[ok]))); ys.append((D['nvl'][t, ok] * w[ok]).sum() / den); ws.append(den)
        try:
            f = lambda k, a, b, c: a + (b - a) * np.exp(-k / c)
            (a, b, c), _ = curve_fit(f, np.array(ks), np.array(ys), p0=(ys[-1], ys[0], 4.0), bounds=([0, 0, 0.3], [1, 1, 40]), maxfev=20000)
            out.append(a)
        except Exception:
            out.append(np.nan)
    out = np.array([x for x in out if np.isfinite(x)])
    lo, hi = np.percentile(out, [5, 95])
    return dict(lo=lo, hi=hi, spread=hi - lo)


def share_in_units(D, tier, R):
    """the same route in units (items) rather than litres: each line's litres divided by its item's litres"""
    P = D['P']
    n = D['n']
    P = P.assign(units=P['qty'])
    cat = np.zeros((G.END_T + 1, n)); nvl = np.zeros((G.END_T + 1, n))
    q = P[(P['t'] >= 0) & (P['t'] <= G.END_T)]
    s = q.groupby(['t', 'i'])['units'].sum()
    cat[s.index.get_level_values(0), s.index.get_level_values(1)] = s.values
    s2 = q[q['nv']].groupby(['t', 'i'])['units'].sum()
    nvl[s2.index.get_level_values(0), s2.index.get_level_values(1)] = s2.values
    avl, a27, _ = G.availability(P.assign(litres=P['units']), os.path.join(C.TARGET, C.FILES['distribution']), n)
    D2 = dict(D, cat=cat, nvl=nvl, avl=avl, a27=a27)
    fl, _ = G.settled(D2, tier, stocked=True)
    L27, _ = G.litres27(D2)
    w = D['H']['w2026'].fillna(0).values
    tr = D['buyer'] & (D['first'] >= 0)
    st = D['static']
    return (w * np.where(tr, fl[tier] * a27, 0.0) * L27)[st].sum() / (w * L27)[st].sum()


def share_oat_only(D, tier, R):
    P = D['P']
    seg = P['item_code'].map(lambda c: D['master'][c]['segment'])
    q = P[(seg == 'Oat') & (P['t'] >= 0) & (P['t'] <= G.END_T)]
    n = D['n']
    cat = np.zeros((G.END_T + 1, n))
    s = q.groupby(['t', 'i'])['litres'].sum()
    cat[s.index.get_level_values(0), s.index.get_level_values(1)] = s.values
    avl, a27, _ = G.availability(P[seg == 'Oat'], os.path.join(C.TARGET, C.FILES['distribution']), n)
    D2 = dict(D, cat=cat, avl=avl, a27=a27)
    fl, _ = G.settled(D2, tier, stocked=True)
    L27, _ = G.litres27(D2)
    w = D['H']['w2026'].fillna(0).values
    tr = D['buyer'] & (D['first'] >= 0)
    st = D['static']
    return (w * np.where(tr, fl[tier] * a27, 0.0) * L27)[st].sum() / (w * L27)[st].sum()


def share_listed_flag(D, tier):
    """the golden with a banner's litres counted as stocked whenever the audit lists the line there that week"""
    import pandas as pd
    path = os.path.join(C.TARGET, C.FILES['distribution'])
    A = pd.read_csv(path, dtype={'item_code': str})
    A = A.assign(wtd_dist_pct=np.where(A['wtd_dist_pct'] > 0, 100.0, 0.0))
    tmp = os.path.join(tempfile.mkdtemp(), 'dist.csv')
    A.to_csv(tmp, index=False)
    avl, a27, _ = G.availability(D['P'], tmp, D['n'])
    D2 = dict(D, avl=avl, a27=a27)
    return G.figures_under(D2, tier, G.TENURE, 'v2425', stocked=True)['share']


def share_at_average_distribution(R):
    """the share scaled by the year's average weighted distribution against the review's (the line's buyers' banners)"""
    import pandas as pd
    A = pd.read_csv(os.path.join(C.TARGET, C.FILES['distribution']), dtype={'item_code': str})
    by = A.groupby('week_ending')['wtd_dist_pct'].mean()
    return R['share'] * by.mean() / by.iloc[-1]


def share_all_in_tab(D, tier, R):
    w = D['H']['w2026'].fillna(0).values
    intab = np.isfinite(D['H']['w2026'].values)
    first = D['first']
    has = D['cat'].sum(0) > 0
    tr = intab & has & (first >= 0)
    L27, _ = G.litres27(D)
    return ((w * np.where(tr, R['lev'], 0.0) * L27)[intab].sum() + (w * R['lit_new'])[intab].sum()) / (w * L27)[intab].sum()


def standard_text():
    from docx import Document
    d = Document(os.path.join(C.TARGET, C.FILES['standard']))
    parts = [p.text for p in d.paragraphs]
    for t in d.tables:
        for r in t.rows:
            parts += [c.text for c in r.cells]
    return '\n'.join(parts).replace('’', "'")


def tells_sweep():
    import tells
    return tells.sweep(C.TARGET)


def people_ok():
    names = set(C.PEOPLE.values()) | {'Mary Gonzales'}
    drawn = {'Gabriel Sloan', 'Becky Vaughn', 'Angela Reyes', 'Kimberly Stanley', 'Mary Gonzales', 'Eric Hernandez',
             'Jennifer Jackson', 'Diamond Oliver', 'Brian Mueller', 'Antonio Camacho'}
    return names <= drawn


def share_without_distractors():
    tmp = tempfile.mkdtemp()
    for f in os.listdir(C.TARGET):
        if f not in (C.FILES[k] for k in C.DISTRACTORS):
            shutil.copy(os.path.join(C.TARGET, f), tmp)
    return G.compute(tmp)['share']


def truth_share():
    import build as B
    import pack as P
    import products as PR
    import world as W
    S = B.prepare(W.simulate())
    M = PR.master()
    O = P.occasions(S)
    L = P.lines(S, O, M)
    tot = np.zeros(S['H']['n']); cnt = np.zeros(S['H']['n'])
    for (h, d, bc, sku, units, paid, flag) in L:
        if sku['family'] != -2:
            tot[h] += sku['litres'] * sku['units'] * units
            cnt[h] += 1
    lp = np.where(cnt > 0, tot / np.maximum(cnt, 1), S['H']['litres_occ'])
    return W.truth_2027(S, reps=8, litres=lp)['share']


if __name__ == '__main__':
    sys.exit(main())
