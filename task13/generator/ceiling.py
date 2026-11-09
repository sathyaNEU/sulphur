"""The cracker sheet: score every graded ask for the landed run, the shallow run and two rung runs on the cut pack.

    python3 task13/generator/ceiling.py

Weights as supplemental-stumping Part 0: 38 for the call and the critical components (the six 20, the components
18), 7 for instruction-following, 55 for the asks. An ask over a column of the feeder table is kept when at least nine
rows in ten sit within 10 per cent of the golden's; a total within 10 per cent; each quarter within 10 per cent; the
range when both ends sit within 1,000 of the golden's.

Landed run (the cracker): the deep step taken (each feeder's vegetation interruptions read per hour of gusts of 60 km/h
or more at its station, split into the corridor's rate and the growth since trim, 2027-28 at the long-run exposure),
every mess item cleaned and every filed rule read, but neither ask judgment: it works at the year's grain and splits
the saving evenly across the quarters, and its range is the fit's own uncertainty (the corridors' and the growth's
standard errors), not the spread of a year's storms. Shallow run: the default path (the six with the most vegetation
customer interruptions in the three years to October 2026), each feeder's expected 2027-28 interruptions its
three-year average, half of them avoided by a catch-up. Rung runs: the wind-normalised expected interruptions taken
as all removable (R3b), and the decomposition on counts without the station record (R6).
"""
import json
import math
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C      # noqa: E402
import golden as G      # noqa: E402
import rivals as V      # noqa: E402

ASKS = [('A1a table: tree interruptions left as is, every feeder', 9), ('A1b table: customer interruptions left as is', 9),
        ('A1c table: customer interruptions after the catch-up', 9), ('A1d table: interruptions avoided and the ranking', 9),
        ('A2 note: the six\'s total and network SAIFI', 7), ('A3 note: the split across the quarters', 6),
        ('A4 note: the 90 per cent range', 6)]


def col_kept(run, gold, key):
    ok = [abs(run[f][key] - gold[f][key]) <= 0.10 * max(abs(gold[f][key]), 1.0) for f in gold]
    return np.mean(ok) >= 0.9


def score(name, run, gold, F, six_run, components):
    kept = {}
    kept[ASKS[0][0]] = col_kept(run['rows'], gold, 'keep_n')
    kept[ASKS[1][0]] = col_kept(run['rows'], gold, 'keep_ci')
    kept[ASKS[2][0]] = col_kept(run['rows'], gold, 'cu_ci')
    kept[ASKS[3][0]] = col_kept(run['rows'], gold, 'avoided') and set(six_run) == set(F['six'])
    kept[ASKS[4][0]] = abs(run['total'] - F['avoided_total']) <= 0.1 * F['avoided_total'] and abs(run['saifi'] - F['saifi_avoided']) <= 0.02
    kept[ASKS[5][0]] = all(abs(a - b) <= 0.1 * b for a, b in zip(run['quarters'], F['quarters']))
    kept[ASKS[6][0]] = abs(run['range'][0] - F['range90'][0]) <= 1000 and abs(run['range'][1] - F['range90'][1]) <= 1000
    ask = sum(w for a, w in ASKS if kept[a])
    call = 20 if set(six_run) == set(F['six']) else (5 if len(set(six_run) & set(F['six'])) >= 2 else 0)
    total = call + components + 7 + ask
    return total, kept, ask


def rows_from(T):
    return {f: dict(keep_n=float(T.loc[f, 'keep_n']), keep_ci=float(T.loc[f, 'keep_ci']), cu_ci=float(T.loc[f, 'cu_ci']),
                    avoided=float(T.loc[f, 'avoided'])) for f in T.index}


def main():
    F = json.load(open(os.path.join(C.HERE, 'figures.json')))
    X = V.Ctx()
    R = X.R
    gold = rows_from(R['T'])
    icps = F['icps_latest']
    runs = {}
    # the landed run: strong-wind hours of 60 km/h, annual grain, the fit's own uncertainty as its range
    av, T55, c55 = V.golden_like(X, EX=G.exposure(X.wx, 60.0))
    six = V.top6(av)
    tot = float(T55.loc[six, 'avoided'].sum())
    Pn = G.panel(X.K, G.exposure(X.wx, 60.0), X.station, X.trims)
    c, m = G.fit(Pn)
    cov = np.asarray(m.cov_params())
    rng = np.random.default_rng(13)
    sims = []
    NE55 = G.normal(G.exposure(X.wx, 60.0))
    for d in rng.multivariate_normal(c.values, cov, 300):
        cc = pd.Series(d, index=c.index)
        sims.append(float(G.project(cc, {f: X.station[f] for f in six}, X.trims, NE55, X.cpe)['avoided'].sum()))
    rg = [int(round(np.percentile(sims, 5), -3)), int(round(np.percentile(sims, 95), -3))]
    runs['landed'] = (dict(rows=rows_from(T55), total=tot, saifi=round(tot / icps, 2), quarters=[tot / 4] * 4, range=rg), six, 18)
    # the shallow run: the default path
    nv = X.nv
    x3 = nv[nv['ym'] >= pd.Period('2023-11', 'M')]
    n3 = x3.groupby('feeder_now').size().reindex(gold.keys()).fillna(0) / 3.0
    ci3 = x3.groupby('feeder_now')['customers'].sum().reindex(gold.keys()).fillna(0) / 3.0
    rows = {f: dict(keep_n=n3[f], keep_ci=ci3[f], cu_ci=0.5 * ci3[f], avoided=0.5 * ci3[f]) for f in gold}
    six_s = list(ci3.sort_values(ascending=False).index[:6])
    tot_s = float(sum(rows[f]['avoided'] for f in six_s))
    runs['shallow'] = (dict(rows=rows, total=tot_s, saifi=round(tot_s / icps, 2), quarters=[tot_s / 4] * 4,
                            range=[int(round(0.8 * tot_s, -3)), int(round(1.2 * tot_s, -3))]), six_s, 0)
    # R3b: the golden fit, everything left as is counted as avoided
    T = R['T']
    rows = {f: dict(keep_n=float(T.loc[f, 'keep_n']), keep_ci=float(T.loc[f, 'keep_ci']), cu_ci=0.0, avoided=float(T.loc[f, 'keep_ci'])) for f in T.index}
    six_b = list(T['keep_ci'].sort_values(ascending=False).index[:6])
    tot_b = float(T.loc[six_b, 'keep_ci'].sum())
    runs['R3b all removable'] = (dict(rows=rows, total=tot_b, saifi=round(tot_b / icps, 2), quarters=[tot_b / 4] * 4,
                                      range=[int(round(0.85 * tot_b, -3)), int(round(1.15 * tot_b, -3))]), six_b, 6)
    # R6: the decomposition on counts alone
    av6 = V.no_exposure(X)
    six6 = V.top6(av6)
    rows6 = {f: dict(keep_n=0.0, keep_ci=0.0, cu_ci=0.0, avoided=float(av6[f])) for f in gold}
    tot6 = float(av6[six6].sum())
    runs['R6 no station record'] = (dict(rows=rows6, total=tot6, saifi=round(tot6 / icps, 2), quarters=[tot6 / 4] * 4,
                                         range=[int(round(0.85 * tot6, -3)), int(round(1.15 * tot6, -3))]), six6, 6)
    out = {}
    for name, (run, six_r, comp) in runs.items():
        s, kept, ask = score(name, run, gold, F, six_r, comp)
        out[name] = (s, kept)
        print('%-22s %5.1f  (six %d of 6, asks %d of 55)' % (name, s, len(set(six_r) & set(F['six'])), ask))
    print('cracker sheet')
    for a, w in ASKS:
        print('  %-56s %5.2f  ' % (a, w) + '  '.join('%s %s' % (n[:8], 'keep' if out[n][1][a] else 'miss') for n in out))
    landed, shallow = out['landed'][0], out['shallow'][0]
    sk = sum(w for a, w in ASKS if out['shallow'][1][a]) / 55 * 100
    print('Shallow keep: %.1f' % sk)
    print('Pair ceiling: %.1f (landed %.1f with shallow %.1f)' % ((landed + shallow) / 2, landed, shallow))
    for n in ('R3b all removable', 'R6 no station record'):
        print('  pair landed with %s: %.1f; shallow with %s: %.1f' % (n, (landed + out[n][0]) / 2, n, (shallow + out[n][0]) / 2))


if __name__ == '__main__':
    main()
