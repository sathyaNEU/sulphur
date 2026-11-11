"""The effort test computed on the cut pack: the three passes run end to end by the generator's own implementations of
named methods (never a solver; nothing here reads the prompt), each result graded against the golden by effort.py.

  quick      ten minutes: the outage system's LIGHTNING cause code as the lightning record, per km
  careful    an afternoon, calibrated to the run record: every export cleaned and the re-read events dropped, faults
             matched to strokes on a tight window where the clocks are synchronised and on a ten-minute window around
             the radio-less controllers' own stamps, the logged events counted as the faults, the sound rate fitted on
             every zone-season no cyclic inspection has found failed (the field's regression, a negative binomial for
             the spread), the terms' window and budget read right, the rule's own false referrals computed
  thorough   the golden

Also the routes (each shortcut's committed referral set) and the hints (each single sentence, executed on the careful
pass alone, and the results it rescues)."""
import json
import os

import analysis as A
import common as C

CAREFUL = dict(clock='wide', fill=False, null='not_failed', disp='nb')
ROUTES = {
    'one clock for every device (no offset, the tight window)': dict(clock='naive'),
    'a ten-minute window around the radio-less controllers\' own stamps': dict(clock='wide'),
    'each radio-less controller at one fixed offset': dict(clock='constant'),
    'a five-minute window on every device': dict(win=(-300, 300)),
    'the logged events taken as every fault': dict(fill=False),
    'the sound rate fitted on every zone-season': dict(null='all'),
    'the sound rate fitted on every season no inspection has found failed': dict(null='not_failed'),
    'the sound rate fitted on the seasons after a clean inspection as well': dict(null='verified_post'),
    'a Poisson spread': dict(disp='poisson'),
    'the whole record, not since the last inspection': dict(window='whole'),
    'the careful but hurried pass': CAREFUL,
}
HINTS = [
    ('the reclosers with no radio link keep their own clocks, set at each site visit and drifting between',
     dict(clock='aligned')),
    ('a radio-less recloser keeps only its last events, and nobody has read some of them since their last visit',
     dict(fill=True)),
    ('the reclosers with no radio link keep their own drifting clocks and only their last events between site visits',
     dict(clock='aligned', fill=True)),
    ('a season counts as sound only when the next cyclic inspection found nothing', dict(null='verified')),
]


def quick(L, R):
    """the OMS's LIGHTNING code as the lightning record: sustained outages only, the dispatchers' word for the cause"""
    oms = L['oms']
    zix = L['zix']
    d = oms[(oms.equipment_type != 'Distribution transformer') & (oms.cause_code == 'LIGHTNING')].copy()
    d['zone_ix'] = d.equipment.map(zix)
    d['season'] = A.season_of(d.t_out.values)
    tot = {s: int((d.season == s).sum()) for s in A.SEASONS}
    rl = set(R['radioless'])
    radioless26 = int(((d.season == 2026) & d.zone_ix.isin(rl)).sum())
    zr = L['zr']
    km = zr['Overhead line km, three-phase'] + zr['Overhead line km, single-phase']
    per = d[d.season.isin([2025, 2026])].groupby('zone_ix').size().reindex(range(len(zr)), fill_value=0) / km
    top = sorted(per.sort_values(ascending=False).head(len(R['ref'])).index)
    return dict(season_tot=tot, radioless26=radioless26, ref=[L['zones'][z] for z in top])


def pass_values(Rx):
    """what a pass files for each result, from its run"""
    return {'R1': {str(s): int(round(Rx['season_tot'][s])) for s in A.SEASONS},
            'R2': int(round(Rx['radioless26'])), 'R3': int(round(Rx['excess26'])), 'R4': sorted(Rx['ref_names']),
            'R5': {str(s): Rx['alerts'][s] for s in A.SEASONS},
            'R6': round(Rx['false_per'], 2),
            'R7': {'referred_inspected': Rx['v_ref'], 'confirmed': Rx['v_conf'], 'missed': Rx['v_miss']},
            'R8': int(round(Rx['avoided_total']))}


def grade_pack(target, R=None):
    L = R['L'] if R else A.load(target)
    R = R or A.run(target, L=L)
    Rc = A.run(target, CAREFUL, L=L)
    Q = quick(L, R)
    routes = []
    for name, o in ROUTES.items():
        r = Rc if o is CAREFUL else A.run(target, o, L=L)
        routes.append({'name': name, 'answer': sorted(r['ref_names'])})
    routes.insert(0, {'name': 'the golden', 'answer': sorted(R['ref_names']), 'golden': True})
    hints = []
    for sentence, fix in HINTS:
        o = dict(CAREFUL)
        o.update(fix)
        hints.append((sentence, A.run(target, o, L=L)))
    return L, R, Rc, Q, routes, hints


def results(R, Rc, Q, F):
    """each result's golden (the figures.json key), band, partial band, and what each pass files"""
    g, c = pass_values(R), pass_values(Rc)
    tot_q = {str(s): Q['season_tot'][s] for s in A.SEASONS}

    def pct(v, p):
        return [round(v * (1 - p)), round(v * (1 + p))]
    out = [
        {'id': 'R1', 'name': 'lightning faults per season', 'graded_as': 'Component 1', 'figure': 'season_totals',
         'depends': [], 'golden': g['R1'], 'bands': F['bands']['season_totals'],
         'passes': {'quick': tot_q, 'careful': c['R1'], 'thorough': g['R1']}},
        {'id': 'R2', 'name': 'radio-less zones, 2026 faults', 'graded_as': 'Ask 1', 'figure': 'radioless_2026',
         'depends': ['R1'], 'golden': F['radioless_2026'], 'band': F['bands']['radioless_2026'],
         'partly': pct(F['radioless_2026'], 0.12),
         'passes': {'quick': Q['radioless26'], 'careful': c['R2'], 'thorough': F['radioless_2026']}},
        {'id': 'R3', 'name': '2026 faults failed protection caused', 'graded_as': 'Component 2', 'figure': 'excess_2026',
         'depends': ['R1', 'R2'], 'golden': F['excess_2026'], 'band': F['bands']['excess_2026'],
         'partly': pct(F['excess_2026'], 0.3),
         'passes': {'quick': None, 'careful': c['R3'], 'thorough': F['excess_2026']}},
        {'id': 'R4', 'name': 'zones referred for the 2027 refit', 'graded_as': 'Recommendation', 'figure': 'referred_zones',
         'depends': ['R1', 'R2', 'R3'], 'golden': g['R4'],
         'passes': {'quick': Q['ref'], 'careful': c['R4'], 'thorough': g['R4']}},
        {'id': 'R5', 'name': 'referrals after each season since 2022', 'graded_as': 'Component 3', 'figure': 'alerts',
         'depends': ['R3', 'R4'], 'golden': g['R5'], 'bands': {k: [max(0, v - 1), v + 1] for k, v in g['R5'].items()},
         'partly_share': 0.6, 'passes': {'quick': None, 'careful': c['R5'], 'thorough': g['R5']}},
        {'id': 'R6', 'name': 'sound zones referred in a season', 'graded_as': 'Ask 2', 'figure': 'false_per_season',
         'independent': 'each zone\'s own expectation and the spread, at the smallest count the rule refers it at',
         'depends': [], 'golden': F['false_per_season'], 'band': F['bands']['false_per_season'], 'partly': [0.09, 0.17],
         'passes': {'quick': None, 'careful': c['R6'], 'thorough': F['false_per_season']}},
        {'id': 'R7', 'name': 'referrals against the following inspections', 'graded_as': 'Component 4',
         'figure': 'validation_core', 'depends': ['R4', 'R5'], 'golden': g['R7'], 'bands': F['bands']['validation_core'],
         'passes': {'quick': None, 'careful': c['R7'], 'thorough': g['R7']}},
        {'id': 'R8', 'name': 'faults the refit avoids, average season', 'graded_as': 'Ask 3',
         'figure': 'avoided_average_season', 'depends': ['R3', 'R4'], 'golden': F['avoided_average_season'],
         'band': F['bands']['avoided_average_season'], 'partly': pct(F['avoided_average_season'], 0.3),
         'passes': {'quick': None, 'careful': c['R8'], 'thorough': F['avoided_average_season']}},
    ]
    return out


def _grader():
    import importlib.util
    p = os.path.join(C.TASK, '..', '.claude', 'skills', 'stumping', 'effort.py')
    spec = importlib.util.spec_from_file_location('effort_skill', os.path.abspath(p))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def grade_hints(res, hints):
    """each hint executed literally on the careful pass: the results it moves from short of Right to Right"""
    G = _grader()
    out = []
    for sentence, Rh in hints:
        pv = pass_values(Rh)
        rescued = []
        for r in res:
            before = G.grade(r['passes']['careful'], r)[0]
            after = G.grade(pv[r['id']], r)[0]
            if before != 'right' and after == 'right':
                rescued.append(r['id'])
        out.append({'sentence': sentence, 'rescues': rescued})
    return out


def write(target, path, F, R=None):
    L, R, Rc, Q, routes, hints = grade_pack(target, R)
    res = results(R, Rc, Q, F)
    H = grade_hints(res, hints)
    E = {'results': res, 'hints': H, 'routes': routes,
         'weights': {'recommendation': 14, 'components': 24, 'asks': 55, 'instruction': 7}}
    json.dump(E, open(path, 'w'), indent=1, sort_keys=False)
    return E, R, Rc
