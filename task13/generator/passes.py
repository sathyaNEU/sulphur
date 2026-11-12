"""The effort test's three passes, each run end to end on the cut pack by the generator's own code (never a solver:
nothing here reads the prompt), with the golden family's rivals and the fitted inputs' perturbations for the
forcing block; writes generator/effort.json for stumping/effort.py.

quick     the dashboard: its "CI saved" each year as the restorations, 2026's as the net, the batteries past the
          four-year cycle, no receiving-feeder interruptions, 2025's figure carried to 2027
careful   calibrated to the run on architecture 3 (task13/runs/run1.md): every file read and cleaned, the archive
          deduplicated and timed in UTC, the five-minute rule applied, the outage record reconciled and the lockouts
          the archive does not hold filled at the archive's own success rate (N10, N14), the restored loop priced
          alone (L16), the batteries judged by the maintenance book's failures, alarms and four-year cycle (N11, N13),
          the receiving feeders' interruptions taken as the 2025-26 summers' average with the plan's dates as given
          (N02, N03), and the 2027 forecast built on the archive's success rate with the plan's dates
thorough  the golden
"""
import datetime as dt
import json
import math
import os
import warnings

import numpy as np
import pandas as pd

import analysis as A
import golden as G

warnings.filterwarnings('ignore')


def archive_sequences(P):
    """the archive's own sequences: start, completion count and completion time"""
    a = P.adms
    rows = []
    for lid, g in a.groupby('loop'):
        g = g.sort_values('t')
        cur = None
        for _, r in g.iterrows():
            if r['kind'] in ('START', 'NOT STARTED'):
                if cur:
                    rows.append(cur)
                cur = {'loop': lid, 't0': r['t'], 'tag': r['tag'], 'n': 0, 't_done': None, 'kind0': r['kind']}
            elif cur is not None and r['kind'] == 'COMPLETE' and (r['t'] - cur['t0']) < pd.Timedelta(minutes=30):
                cur['n'] = int(r['n'])
                cur['t_done'] = r['t']
        if cur:
            rows.append(cur)
    return pd.DataFrame(rows)


def careful_r1(P, ops):
    """the archive's completions within five minutes of the lockout, the lockouts it does not hold filled at its own
    success rate and average count"""
    s = archive_sequences(P)
    s['year'] = s['t0'].dt.tz_convert(A.CENTRAL).dt.year
    # the five minutes from the first loss of supply: the outage record's start for the lockout
    oms = P.oms
    starts = oms.drop_duplicates('Outage ID')
    def first_loss(r):
        dev = P.tag2asset.get(r['tag'])
        m = starts[(starts['Interrupting Device'] == dev) & ((starts['start'] - r['t0']).abs() < pd.Timedelta(minutes=20))]
        return m['start'].min() if len(m) else r['t0'] - pd.Timedelta(seconds=45)
    s['t_first'] = s.apply(first_loss, axis=1)
    s['ok5'] = s['t_done'].notna() & ((s['t_done'] - s['t_first']).dt.total_seconds() < G.FIVE_MIN + 30)
    elig = s[s['kind0'] == 'START']
    rate = float((elig['n'] > 0).mean())
    avg = float(elig.loc[elig['n'] > 0, 'n'].mean())
    o = ops.copy()
    o['year'] = o['t_lo'].dt.tz_convert(A.CENTRAL).dt.year
    # the archive's own rate among the lockouts that had something to transfer
    s_el = elig[elig['tag'].map(lambda x: isinstance(x, str) and ('CB' in x or x.endswith('R1') or x.endswith('RCL1')))]
    rate = float((s_el['n'] > 0).mean())
    avg = float(s_el.loc[s_el['n'] > 0, 'n'].mean())
    out = {}
    for y in range(2022, 2027):
        base = int(elig.loc[(elig['year'] == y) & elig['ok5'], 'n'].sum())
        missing = int(((o['year'] == y) & ~o['in_archive'] & o['kind'].isin(['CB', 'R1'])).sum())
        out[y] = int(round(base + missing * rate * avg))
    return out, rate, avg


def quick_r1(P):
    d = G.dashboard(P)
    return {int(y): int(d.loc[d['year'] == y, 'CI saved'].sum()) for y in range(2022, 2027)}


def careful_r3(P):
    """each battery judged at its coldest load test of last winter: the volts the 30 A operation would leave at that
    test's temperature, the battery as it was then (not carried to -27 C, not aged to February)"""
    bt, reg_batt = G.battery_tests(P)
    w = bt[(bt['t'] >= pd.Timestamp('2025-12-01', tz='UTC')) & (bt['t'] < pd.Timestamp('2026-03-01', tz='UTC'))]
    w = w[w.apply(lambda r: pd.notna(r['batt']) and r['batt'] == reg_batt.get(r['Device']), axis=1)]
    named = []
    for a, g in w.groupby('Device'):
        r = g.loc[g['T'].idxmin()]
        v_op = r['v_rest'] - G.OP_A * r['R']
        if v_op < G.V_MIN:
            named.append(a)
    return sorted(named)


def careful_r3_book(P):
    """the controls the maintenance book shows failing or alarming, and the batteries past their four-year cycle,
    as the record stands; a battery that passed its functional test is taken as sound"""
    br = pd.read_excel(P.p('maint'), sheet_name='Battery replacements', header=None)
    hdr = br.index[br[0] == 'Date'][0]
    br.columns = list(br.iloc[hdr])
    br = br.iloc[hdr + 1:].dropna(subset=['Date'])
    flagged = set(br.loc[br['Reason'].str.contains('Failed|alarm', case=False), 'Asset No'])
    old = set()
    for a, r in P.dev.items():
        if pd.notna(r['Battery installed']) and (pd.Timestamp('2027-02-28') - pd.Timestamp(r['Battery installed'])).days > 4 * 365.25:
            old.add(a)
    # those already re-batteried after the failure are fine by the book's own date; the rest are named
    named = sorted(old | {a for a in flagged if pd.notna(P.dev[a]['Battery installed']) and
                          pd.Timestamp(P.dev[a]['Battery installed']) < pd.Timestamp('2025-01-01')})
    return named


def quick_r3(P):
    return sorted(a for a, r in P.dev.items() if pd.notna(r['Battery installed']) and
                  (pd.Timestamp('2026-11-04') - pd.Timestamp(r['Battery installed'])).days > 4 * 365.25)


def careful_r4(P, ops, net_only=False, keep_reinforced=False):
    """the 2025 and 2026 summers' receiving-feeder interruptions after transfers, averaged, the plan's dates as
    given (a reinforced feeder's share dropped)"""
    rt = G.receiving_trips(P, ops)
    if not len(rt):
        return 0.0
    rt['m'] = rt['t'].dt.tz_convert(A.CENTRAL).dt.month
    s = rt[rt['year'].isin([2025, 2026]) & rt['m'].isin(G.SUMMER)]
    sl, plan = G.slip_months(P)
    reinf = set(plan['Feeder'])
    if not keep_reinforced:
        s = s[~s['to'].isin(reinf)]
    return float(s['own'].sum() / 2.0)


def write(target, path):
    P = A.Pack(target)
    ops = G.operations(P)
    rt = G.receiving_trips(P, ops)
    cf = G.closes_onto_fault(P, ops)
    gold = {'R1': G.r1_by_year(ops), 'R2': G.bridge_2026(P, ops, rt, cf)}
    br, k, vrd = G.battery_risk(P)
    gold['R3'] = sorted(br.loc[br['fails'], 'asset'])
    fw = G.forward(P, ops)
    gold['R4'] = float(fw['harm'].sum())
    fc = G.forecast(P, ops)
    gold['R5'] = fc['mean']
    # -------------------------------------------------------------------- the careful but hurried pass
    c_r1, c_rate, c_avg = careful_r1(P, ops)
    s = archive_sequences(P)
    s['year'] = s['t0'].dt.tz_convert(A.CENTRAL).dt.year
    filled_r1 = c_r1
    c_r1 = dict(gold['R1'])          # a careful run rebuilds the restorations from the device record: a reflex
    c_r2 = c_r1[2026] - int(cf.loc[cf['year'] == 2026, 'own'].sum() if len(cf) else 0)
    c_r3 = careful_r3(P)
    c_r4 = careful_r4(P, ops)
    c_r5 = G.forecast(P, ops, net=False, plan_trusted=True, battery=False, supervised=False, sims=400)['mean']
    # ---------------------------------------------------------------------------------- the quick pass
    q_r1 = quick_r1(P)
    q_r3 = quick_r3(P)
    d = G.dashboard(P)
    d['mon'] = pd.to_datetime(d['Month'])
    q_r5 = float(d.loc[d['mon'] >= pd.Timestamp('2025-11-01'), 'CI saved'].sum())
    # ------------------------------------------------------------------ the golden family and the bands
    fam_r3 = {
        'per-battery cold coefficient': G.battery_risk(P, pooled_k=False)[0],
        'end of January': G.battery_risk(P, at=pd.Timestamp('2027-01-31', tz='UTC'))[0],
        'design minimum -26 C': G.battery_risk(P, design=-26.0)[0],
        'design minimum -28 C': G.battery_risk(P, design=-28.0)[0],
    }
    fam_r3 = {k_: sorted(v.loc[v['fails'], 'asset']) for k_, v in fam_r3.items()}
    FJ = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'figures.json')))
    rr = FJ['r3_ruling']
    fam_r3['a mixed model, each control drawn around the fleet'] = rr['named']['a mixed model, each control drawn around the fleet']
    golden_r3 = "each battery's own ageing (the golden)"
    ruled_out = {'R3': {name: {'count': n, 'oos_rmse_v': rr['oos_rmse_v'][name],
                               'ruled_out_by': 'control intercepts F %s and ageing F %s; last winter\'s cold tests missed '
                                               'by %.2f V at 30 A against %.2f V' % (
                                                   rr['f_tests']['control_intercepts']['F'],
                                                   rr['f_tests']['control_age_slopes']['F'], rr['oos_rmse_v'][name],
                                                   rr['oos_rmse_v'][golden_r3])}
                        for name, n in rr['counts'].items() if not name.startswith(('each battery', 'a mixed'))}}
    G.CB_TYPING['repair'] = False
    r4_loc = float(G.forward(P, ops)['harm'].sum())
    r5_loc = G.forecast(P, ops, sims=300)['mean']
    G.CB_TYPING['repair'] = True
    fam_r4 = {
        'pickup at 1.05 of the hourly average': float(G.forward(P, ops, pk=1.05)['harm'].sum()),
        'every summer hour alike': float(G.forward(P, ops, weighting='hours')['harm'].sum()),
        'slip from reconductoring alone': float(G.forward(P, ops, reinf_cats=('Reconductor',))['harm'].sum()),
        'unlocated breaker lockouts as section 1 faults': r4_loc,
    }
    fam_r5 = {
        'pickup at 1.05 of the hourly average': None,
    }
    res = []
    r1_band = {str(y): [round(v * 0.98), round(v * 1.02)] for y, v in gold['R1'].items()}
    res.append({'id': 'R1', 'name': 'customers restored within five minutes, each year 2022 to 2026', 'graded_as': 'Ask 1',
                'figure': 'r1_by_year', 'depends': [], 'independent': 'the device event record and the outage record',
                'golden': {str(y): v for y, v in gold['R1'].items()}, 'bands': r1_band, 'partly_share': 0.6,
                'passes': {'quick': {str(y): v for y, v in q_r1.items()},
                           'careful': {'value': {str(y): v for y, v in c_r1.items()},
                                       'why': 'every log reconciled by reflex (R01, R29): the device record\'s closes '
                                              'timed from the first trip; the gap-filled archive route is a shortcut '
                                              'in routes'},
                           'thorough': {str(y): v for y, v in gold['R1'].items()}},
                'precedent': []})
    net = gold['R2']['net']
    res.append({'id': 'R2', 'name': "2026's customer interruptions avoided on the order's definition", 'graded_as': 'Component 1',
                'figure': 'net_2026', 'depends': [], 'independent': 'the dashboard and the 2026 records',
                'golden': net, 'band': [round(net * 0.975), round(net * 1.025)], 'partly': [round(net * 0.94), round(net * 1.06)],
                'passes': {'quick': gold['R2']['dashboard'],
                           'careful': {'value': c_r2, 'why': 'the restored loop priced alone: no receiving recloser\'s '
                                                             'trip netted (L16), only the visible closes onto a fault '
                                                             'taken off (L06)'},
                           'thorough': net},
                'precedent': ['L16', 'L06']})
    res.append({'id': 'R3', 'name': 'the controls to re-battery before the winter', 'graded_as': 'Recommendation',
                'figure': 'rebattery_set', 'depends': [], 'independent': 'the weekly load tests and the airport temperatures',
                'golden': gold['R3'],
                'passes': {'quick': q_r3,
                           'careful': {'value': c_r3, 'why': 'each battery judged at its coldest test of last winter, '
                                                             'the condition it was tested in carried as the condition it '
                                                             'will meet (N12) and the battery as it stood as its state at '
                                                             'the winter\'s end (N13)'},
                           'thorough': gold['R3']},
                'precedent': ['N12', 'N13']})
    r4 = gold['R4']
    lo4 = math.floor(min(round(r4), *[round(v) for v in fam_r4.values()]) * 0.97)
    hi4 = math.ceil(max(round(r4), *[round(v) for v in fam_r4.values()]) * 1.03)
    ruled_out['R5'] = {'without the breaker\'s own section': {
        'value': round(G.forecast(P, ops, sims=300, upstream=False)['mean']),
        'ruled_out_by': 'the record\'s breaker lockouts for a section 2 fault, re-closed onto section 1 within five '
                        'minutes in %d of %d' % (FJ['breaker_section']['reclosed'], FJ['breaker_section']['lockouts'])}}
    ruled_out['R4'] = {name: {'value': v, 'inside_band': bool(lo4 <= v <= hi4),
                              'ruled_out_by': 'the design basis files summer as 1 June to 30 September'}
                       for name, v in FJ['summer_windows'].items()}
    res.append({'id': 'R4', 'name': "the receiving feeders' customers June to September 2027 transfers would interrupt", 'graded_as': 'Ask 3',
                'figure': 'summer_2027_receiving', 'depends': [], 'independent': 'the hourly amps, the register and the capital works',
                'golden': round(r4), 'band': [math.floor(lo4), math.ceil(hi4)], 'partly': [math.floor(lo4 * 0.85), math.ceil(hi4 * 1.15)],
                'passes': {'quick': 0,
                           'careful': {'value': round(c_r4), 'why': 'the 2025-26 summers\' trips averaged as the coming '
                                                                    'summer (N02), the reinforcements in service on the '
                                                                    'plan\'s dates (N03)'},
                           'thorough': round(r4)},
                'precedent': ['N02', 'N03']})
    r5 = gold['R5']
    fam5 = {'pickup at 1.05 of the hourly average': G.forecast(P, ops, pk=1.05, sims=300)['mean'],
            'every hour alike': G.forecast(P, ops, weighting='hours', sims=300)['mean'],
            'slip from reconductoring alone': G.forecast(P, ops, reinf_cats=('Reconductor',), sims=300)['mean'],
            'the radio outage kept in the success rate': G.forecast(P, ops, skyline_fixed=False, sims=300)['mean'],
            'unlocated breaker lockouts as section 1 faults': r5_loc}
    lo5 = math.floor(min(r5, *fam5.values()) * 0.98)
    hi5 = math.ceil(max(r5, *fam5.values()) * 1.02)
    res.append({'id': 'R5', 'name': '2027 customer interruptions avoided as the schemes stand', 'graded_as': 'Component 2',
                'figure': 'forecast_2027', 'depends': ['R4'], 'independent': '',
                'golden': round(r5), 'band': [lo5, hi5], 'partly': [math.floor(lo5 * 0.95), math.ceil(hi5 * 1.05)],
                'passes': {'quick': round(q_r5),
                           'careful': {'value': round(c_r5), 'why': 'the restored loop priced alone (L16), the plan\'s '
                                                                    'dates as given (N03), the archive\'s success rate (N10)'},
                           'thorough': round(r5)},
                'precedent': ['L16', 'N03']})
    # each hint executed on the careful pass end to end; a result is rescued when its value enters the band
    def inband(rid, v):
        r = {x['id']: x for x in res}[rid]
        if isinstance(r['golden'], list):
            return set(v) == set(r['golden'])
        return r['band'][0] <= v <= r['band'][1]
    h_net = {'R2': gold['R2']['net'],
             'R5': G.forecast(P, ops, net=True, plan_trusted=True, battery=False, supervised=False, sims=300)['mean'],
             'R4': careful_r4(P, ops, net_only=True)}
    h_bat = {'R3': gold['R3'],
             'R5': G.forecast(P, ops, net=False, plan_trusted=True, battery=True, supervised=False, sims=300)['mean']}
    h_slip = {'R4': careful_r4(P, ops, keep_reinforced=True),
              'R5': G.forecast(P, ops, net=False, plan_trusted=False, battery=False, supervised=False, sims=300)['mean']}
    h_arch = {'R1': gold['R1'], 'R2': c_r2}
    hints = [{'sentence': 'a transfer onto a receiving feeder whose reclosers the ADMS does not switch can trip them '
                          'later, with no fault found', 'rescues': sorted(k for k, v in h_net.items() if inband(k, v)),
              'values': {k: (v if not isinstance(v, float) else round(v)) for k, v in h_net.items()}},
             {'sentence': 'the dashboard counts every completed sequence whatever its duration, and the archive misses '
                          'the storm overflows', 'rescues': [], 'values': {'R2': c_r2}},
             {'sentence': 'a battery that passes in mild weather can fail to crank at the design minimum',
              'rescues': sorted(k for k, v in h_bat.items() if inband(k, v)),
              'values': {'R5': round(h_bat['R5'])}},
             {'sentence': 'comparable projects finish months after their planned dates',
              'rescues': sorted(k for k, v in h_slip.items() if inband(k, v)),
              'values': {k: round(v) for k, v in h_slip.items()}}]
    routes = [
        {'name': 'the golden', 'answer': ['2026 net %d' % net, 're-battery %d controls' % len(gold['R3']),
                                         'receiving 2027 %d' % round(r4), '2027 %d' % round(r5)], 'golden': True},
        {'name': 'the dashboard', 'answer': ['2026 net %d' % gold['R2']['dashboard'], 're-battery %d controls' % len(q_r3),
                                            'receiving 2027 0', '2027 %d' % round(q_r5)]},
        {'name': 'the archive with its storm gaps filled at its own rate', 'answer': [
            '2026 net %d' % filled_r1[2026], 're-battery %d controls' % len(c_r3), 'receiving 2027 %d' % round(c_r4),
            '2027 %d' % round(c_r5)]},
        {'name': 'the careful but hurried pass', 'answer': ['2026 net %d' % c_r2, 're-battery %d controls' % len(c_r3),
                                                           'receiving 2027 %d' % round(c_r4), '2027 %d' % round(c_r5)]},
        {'name': 'the receiving trips netted, the plan trusted', 'answer': [
            '2026 net %d' % net, 're-battery %d controls' % len(c_r3),
            'receiving 2027 %d' % round(G.forward(P, ops, plan_trusted=True)['harm'].sum()),
            '2027 %d' % round(G.forecast(P, ops, plan_trusted=True, sims=300)['mean'])]},
    ]
    forcing = {'kind': 'numeric', 'line': gold['R2']['dashboard'], 'golden_side': 'below',
               'golden_family': [{'name': 'lost sequences counted from the configuration\'s customers', 'value': net},
                                 {'name': 'lost sequences counted from the outage record\'s steps', 'value': net},
                                 {'name': 'receiving trips read from the outage record alone', 'value': net}],
               'shortcuts': [{'name': 'the dashboard', 'value': gold['R2']['dashboard'] + 1}],
               'perturbations': [{'input': 'section customers +10%', 'value': round(net * 1.1)},
                                 {'input': 'section customers -10%', 'value': round(net * 0.9)}]}
    out = {'results': res, 'hints': hints, 'routes': routes, 'forcing': forcing,
           'weights': {'recommendation': 14, 'components': 24, 'asks': 55, 'instruction': 7},
           'rivals': {'R3': fam_r3, 'R4': fam_r4, 'R5': {k: round(v) for k, v in fam5.items()}},
           'ruled_out': ruled_out}
    json.dump(out, open(path, 'w'), indent=1, default=str)
    return out, gold


if __name__ == '__main__':
    import os
    import sys
    t = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..', 'target')
    out, gold = write(t, os.path.join(os.path.dirname(__file__), 'effort.json'))
    for r in out['results']:
        c = r['passes']['careful']
        print(r['id'], 'golden', r['golden'] if not isinstance(r['golden'], list) else len(r['golden']),
              '| careful', c['value'] if not isinstance(c['value'], list) else len(c['value']),
              '| quick', r['passes']['quick'] if not isinstance(r['passes']['quick'], list) else len(r['passes']['quick']))
    print('R3 golden', gold['R3'])
    for k_, v in out['rivals']['R3'].items():
        print('  rival', k_, len(v), sorted(set(v) ^ set(gold['R3'])))
    print('R4 rivals', out['rivals']['R4'])
    print('careful R3', sorted(set(out['results'][2]['passes']['careful']['value'])))
