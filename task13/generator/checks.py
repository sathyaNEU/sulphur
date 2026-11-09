"""The build's assertions, run on the cut pack: the Layer 1 texture is what each producing system makes and every
careful run cleans it the same way; every semantic fork (SF1 to SF19) lands on the golden six or is filed; every rung
that skips a step of the golden misses most of the six; the golden recovers the world's own answer.

    python3 task13/generator/checks.py
"""
import json
import os
import re
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C      # noqa: E402
import golden as G      # noqa: E402
import rivals as V      # noqa: E402
import world as W       # noqa: E402

FAILS = []


def check(name, cond, detail=''):
    print('%-4s %-74s %s' % ('PASS' if cond else 'FAIL', name, detail))
    if not cond:
        FAILS.append(name)


def overlap(a, b):
    return len(set(a) & set(b))


def main():
    X, fam, rg = V.run()
    R, K = X.R, X.K
    six = X.six
    F = json.load(open(os.path.join(C.HERE, 'figures.json')))
    T = R['T']

    # ------------------------------------------------------------ the call
    check('the golden six', six == F['six'], ' '.join(six))
    gap = float(T['avoided'].iloc[5] / T['avoided'].iloc[6])
    check('the sixth leads the seventh by a quarter or more', gap >= 1.25, '%.3f (%s)' % (gap, T.index[6]))
    S = W.simulate()
    E = W.interruptions(S)
    truth, _ = W.truth(S, E, reps=30)
    t6 = list(truth.sort_values('avoided', ascending=False)['feeder'][:6])
    check('the golden six are the world\'s six', set(six) == set(t6), ' '.join(t6))
    grp = dict(zip(S['F']['feeder'], S['F']['group']))
    check('the six are the overdue northern coastal feeders', all(grp[f] == 'O' for f in six), ''.join(grp[f] for f in six))

    # ------------------------------------------------------------ the family (SF6 to SF16): every convention, the same six
    for sf in ('SF1', 'SF2', 'SF3', 'SF4', 'SF6', 'SF7', 'SF8', 'SF9', 'SF10', 'SF11', 'SF12', 'SF13', 'SF14', 'SF16'):
        check('%s has a construction in the family' % sf, any(k.split()[0] == sf for k in fam), '')
    for k, v in fam.items():
        sf = k.split()[0]
        check('%s same call: %s' % (sf, k[len(sf) + 1:]), v == six or set(v) == set(six), ' '.join(v))

    # ------------------------------------------------------------ the rungs: each misses most of the six
    for k, v in rg.items():
        check('rung misses: %s' % k[:62], overlap(v, six) <= 3, '%d of 6' % overlap(v, six))
    cheap = [k for k, v in rg.items() if overlap(v, six) >= 4]
    check('no cheap route reaches four of the six', not cheap, ', '.join(cheap) or 'none')
    dp = rg['R1 vegetation customer interruptions, three years to October 2026 (default path)']
    check('the default path files none of the six', overlap(dp, six) == 0, ' '.join(dp))
    check('the default path is the figures\' default six', set(dp) == set(F['default_six']), '')
    check('the default path is the plantation feeders and one southern feeder',
          sum(grp[f] == 'D' for f in dp) == 5, ''.join(grp[f] for f in dp))

    # ------------------------------------------------------------ SF1 to SF5: cleaning and the filed WHAT
    o = K['o']
    raw = pd.read_csv(G.path_of('oms', C.TARGET), dtype=str, keep_default_na=False)
    cc = (raw['source'] == 'Call centre').sum()
    check('SF3 every call centre record is an operation SCADA or the field crew logged', K['n_dup'] == cc,
          '%d of %d dropped' % (K['n_dup'], cc))
    check('SF3 call centre records carry the third spelling of vegetation', (raw.loc[raw['source'] == 'Call centre', 'cause_code'] == 'Trees').sum() > 0
          and (raw.loc[raw['source'] != 'Call centre', 'cause_code'] == 'Trees').sum() == 0, '')
    t = pd.to_datetime(raw['start_time'])
    check('SF1 vegetation is VEG to 30 September 2023 and TREE after',
          (raw.loc[t >= '2023-10-01', 'cause_code'] == 'VEG').sum() == 0 and (raw.loc[t < '2023-10-01', 'cause_code'] == 'TREE').sum() == 0, '')
    mom = (raw['duration_min'].astype(float) < 1.0).sum()
    check('SF2 momentary interruptions are in the export', mom > 500, '%d rows under 1 minute' % mom)
    check('SF2 planned interruptions are in the export', (raw['interruption_class'] == 'Planned').sum() > 300, '')
    meds = sorted(K['meds'])
    snow = {d for d in meds if ((K['u']['start'].dt.normalize() == d) & K['u']['cause_code'].isin(['WTH', 'WEATHER'])).sum() >= 10}
    check('SF4 the major event days are the snow days', len(meds) == 5 and set(meds) == snow,
          ', '.join(d.strftime('%Y-%m-%d') for d in meds))
    strong_on_med = sum(int(((g >= 60) & g.index.normalize().isin(K['meds'])).sum()) for g in X.wx.values())
    check('SF4 no major event day carried a strong-wind hour', strong_on_med == 0, '%d hours' % strong_on_med)
    top_ordinary = max(v for d, v in K['saidi'].items() if d not in K['meds'])
    check('SF4 the stormiest ordinary day sits well under the SAIDI boundary', top_ordinary < 0.8 * K['bounds']['DPP4'][0],
          '%.1f minutes' % top_ordinary)
    from docx import Document
    terms = ' '.join(p.text for p in Document(G.path_of('programme', C.TARGET)).paragraphs)
    check('SF5 the terms file the window, the comparison and no cycle trim before April 2028',
          '1 April 2027 to 31 March 2028' in terms and 'left as it stands' in terms and 'No feeder has a cycle trim' in terms, '')
    check('SF15 the terms file the SAIFI denominator', 'ICPs connected at the latest month-end' in terms, '')
    icp = K['icp']
    ry25 = icp[(icp['month_end'] >= '2025-04') & (icp['month_end'] <= '2026-03')].groupby('month_end')['icps_connected'].sum().mean()
    alt = round(F['avoided_total'] / ry25, 2)
    check('SF15 the 2025-26 average ICPs give the same SAIFI', alt == F['saifi_avoided'], '%.2f' % alt)
    check('SF14 Rangiora Street feeders carry former codes before the rebuild only',
          raw.loc[t < '2023-08-14', 'feeder'].str.startswith('RGS').sum() > 0 and raw.loc[t >= '2023-08-14', 'feeder'].str.startswith('RGS').sum() == 0, '')

    # ------------------------------------------------------------ SF8: the gust load fits the record best
    from scipy.special import gammaln

    def loglik(EX):
        Pn = G.panel(K, EX, X.station, X.trims)
        c, _ = G.fit(Pn)
        mu = np.exp(np.array([c[f] for f in Pn['feeder']]) + c['g'] * Pn['ys'].values) * Pn['ex'].values
        y = Pn['n'].values
        bad = int(((Pn['ex'] == 0) & (y > 0)).sum())
        return float(np.sum(y * np.log(np.where(mu > 0, mu, 1e-300)) - mu - gammaln(y + 1))), bad
    ll_g, bad_g = loglik(X.EX)
    others = {'hours of gusts %d km/h or more' % t: loglik(G.exposure(X.wx, t)) for t in (45, 50, 60)}
    others.update({'gust load over %d km/h' % b: loglik(G.gust_load(X.wx, b)) for b in (35, 45)})
    others.update({'straight gust excess over %d km/h' % b: loglik(G.gust_load(X.wx, b, 1.0)) for b in (40, 45)})
    check('SF8 the gust load over 40 km/h fits the record best', all(ll_g > v[0] for v in others.values()),
          'log-likelihood %.0f; next %s' % (ll_g, ', '.join('%s %.0f' % (k, v[0]) for k, v in sorted(others.items(), key=lambda kv: -kv[1][0])[:3])))
    check('SF8 no feeder-month with vegetation interruptions has no gust load', bad_g == 0, '')
    check('SF8 hour counts from 50 km/h leave interruptions with no exposure', others['hours of gusts 60 km/h or more'][1] > 0
          and others['hours of gusts 50 km/h or more'][1] > 0, '%d feeder-months at 60 km/h' % others['hours of gusts 60 km/h or more'][1])

    # ------------------------------------------------------------ SF17, SF18: the station record's own texture
    tsd = pd.read_csv(G.path_of('wx_TSD', C.TARGET))
    tt = pd.to_datetime(tsd['obs_time_utc'], format='%Y-%m-%dT%H:%MZ')
    check('SF17 Titi Saddle reports knots before July 2013 only',
          (tsd.loc[tt >= '2013-07-01', 'wind_unit'] == 'kt').sum() == 0 and (tsd.loc[tt < '2013-06-30', 'wind_unit'] == 'km/h').sum() == 0, '')
    wx_kt = {sid: g.copy() for sid, g in X.wx.items()}
    pre = wx_kt['TSD'].index < pd.Timestamp('2013-07-01')
    wx_kt['TSD'][pre] = wx_kt['TSD'][pre] / 1.852
    v = V.top6(V.golden_like(X, EX=G.gust_load(wx_kt))[0])
    check('SF17 same call: knots left unconverted', set(v) == set(six), ' '.join(v))
    wx_s = {}
    for sid in C.STATION_IDS:
        w = pd.read_csv(G.path_of('wx_' + sid, C.TARGET))
        g = w['gust_max'].where(w['qc'] != 'M')
        g = np.where(w['wind_unit'] == 'kt', g * 1.852, g)
        tl = pd.to_datetime(w['obs_time_utc'], format='%Y-%m-%dT%H:%MZ', utc=True).dt.tz_convert(C.ZONE).dt.tz_localize(None)
        wx_s[sid] = pd.Series(g, index=pd.DatetimeIndex(tl))
    v = V.top6(V.golden_like(X, EX=G.gust_load(wx_s))[0])
    check('SF18 same call: suspect hours kept', set(v) == set(six), ' '.join(v))
    gaps_in_window = sum(int(((g.index >= '2022-04-01') & g.isna()).sum()) for g in X.wx.values())
    check('SF18 no missing hour inside the outage record', gaps_in_window == 0, '')

    # ------------------------------------------------------------ SF19: the 90 per cent range
    lo, hi, wy = G.weather_range(R)
    check('SF19 the range is the spread across the station record\'s years', [int(round(lo, -3)), int(round(hi, -3))] == F['range90'],
          '%s' % F['range90'])
    nr = [float(np.percentile(wy, 5, method='nearest')), float(np.percentile(wy, 95, method='nearest'))]
    check('SF19 nearest-rank percentiles round to the same range ends or one step away',
          abs(round(nr[0], -3) - F['range90'][0]) <= 1000 and abs(round(nr[1], -3) - F['range90'][1]) <= 1000, '%.0f to %.0f' % tuple(nr))
    cov = np.asarray(R['model'].cov_params())
    rng = np.random.default_rng(5)
    sims = []
    for d in rng.multivariate_normal(R['coef'].values, cov, 400):
        cc = pd.Series(d, index=R['coef'].index)
        sims.append(float(G.project(cc, {f: R['station'][f] for f in six}, R['trims'], R['NE'], R['cpe'])['avoided'].sum()))
    flo, fhi = np.percentile(sims, [5, 95])
    w19 = [int(round(float(np.percentile(G.weather_years(R, (2006, 2024)), q)), -3)) for q in (5, 95)]
    check('SF19 the range runs over every complete regulatory year, 2006-07 to 2025-26', G.RANGE_YEARS == (2006, 2025) and len(wy) == 20,
          '20 years %s; the 19 to 2024-25 would give %s' % (F['range90'], w19))
    check('SF19 the 19-year window is recorded', F['range90_19yr'] == w19, str(w19))
    check('SF19 the record\'s spread is more than twice the fit\'s own uncertainty', (hi - lo) > 2.0 * (fhi - flo),
          'weather %.0f to %.0f; fit alone %.0f to %.0f' % (lo, hi, flo, fhi))

    # ------------------------------------------------------------ texture that must not decide
    names = sorted(os.path.relpath(os.path.join(r, f), C.TARGET) for r, ds, fs in os.walk(C.TARGET) for f in fs)
    check('H9 no readme, dictionary, notes or manifest in the pack', not any(re.search(r'readme|dictionar|manifest|notes', n, re.I) for n in names), '')
    check('the pack has fourteen files', len(names) == 14, str(len(names)))
    check('the OMS export is a long messy file', len(raw) > 10000, '%d rows' % len(raw))
    check('the station files are large', all(len(g) > 180000 for g in X.wx.values()), '')
    for fn in names:
        if fn.endswith('.docx'):
            txt = ' '.join(p.text for p in Document(os.path.join(C.TARGET, fn)).paragraphs)
            check('no em dash in %s' % fn, '\u2014' not in txt and '\u2013' not in txt, '')
    for k in C.DISTRACTORS:
        check('the distractor %s is read by no golden step' % C.FILES[k], C.FILES[k] not in open(os.path.join(C.HERE, 'golden.py')).read(), '')
    for word in ('weather', 'wind', 'gust', 'growth', 'regrow', 'station', 'exposure', 'storm'):
        check('the programme terms never say "%s"' % word, not re.search(r'\b%s' % word, terms.lower()), '')
    std = ' '.join(p.text for p in Document(G.path_of('standard', C.TARGET)).paragraphs).lower()
    for word in ('gust', 'growth', 'regrow', 'station', 'exposure', 'years since'):
        check('the reliability standard never says "%s"' % word, not re.search(r'\b%s' % word, std), '')

    # ------------------------------------------------------------ the figures and the golden files agree
    g = pd.read_csv(os.path.join(C.GOLDEN, C.DELIVERABLES[0]))
    check('golden table: 48 rows ranked', list(g['feeder']) == list(T.index) and list(g['rank']) == list(range(1, 49)), '')
    check('golden table: the six marked', set(g.loc[g['in_catchup'] == 'Y', 'feeder']) == set(six), '')
    check('golden table: the six\'s avoided add to the total',
          int(g.loc[g['in_catchup'] == 'Y', 'customer_interruptions_avoided'].sum()) in (F['avoided_total'] - 2, F['avoided_total'] - 1, F['avoided_total'], F['avoided_total'] + 1, F['avoided_total'] + 2), '')
    check('the quarters add to the year', sum(F['quarters']) == F['avoided_total'], str(F['quarters']))
    print('CHECKS', 'PASS' if not FAILS else 'FAIL (%d)' % len(FAILS))
    return 0 if not FAILS else 1


if __name__ == '__main__':
    sys.exit(main())
