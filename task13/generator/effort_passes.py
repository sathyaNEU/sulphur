"""The effort test computed on the cut pack: the three passes run end to end by the generator's own implementations of
named methods (never a solver; nothing here reads the prompt), each result graded against the golden by effort.py.

  quick      ten minutes: the outage system's LIGHTNING cause code as the lightning record, per km
  careful    an afternoon, calibrated to the stage 4 judges' own first passes (architecture 2 landed the repairs, the
             baseline and the window; architecture 3 read the budget as the rule's own false referrals and executed
             every filed definition) and graded up where either went further: every export cleaned and the re-read events
             dropped, the radio-less clocks aligned and the lost and unread months restored, the sound rate fitted on the
             seasons a later inspection confirmed sound with every register feature, the window and the budget read
             right, the rule's own false referrals computed; the scatter taken season by season (quasi-Poisson) and the
             refit valued on each zone's record since its inspection, averaged
  thorough   the golden

Also the routes (each shortcut's committed referral set) and the hints (each single sentence, executed literally on
the careful pass alone, and the results it rescues)."""
import json
import os

import analysis as A
import common as C

CAREFUL = dict(disp='quasi', avoided='average')
PRECEDENTS = {'R2': ['L09'], 'R3': ['L35', 'L09', 'L33'], 'R4': ['L09', 'L33'], 'R5': ['L35', 'L28'], 'R6': ['L28', 'L29'], 'R7': ['L12', 'N02']}
ROUTES = {
    'one clock for every device (no offset, the tight window)': dict(clock='naive'),
    'a ten-minute window around the radio-less controllers\' own stamps': dict(clock='wide'),
    'the logged events taken as every fault': dict(fill=False),
    'the sound rate fitted on every zone-season': dict(null='all'),
    'the sound rate fitted on every season no inspection has found failed': dict(null='not_failed'),
    'a quasi-Poisson scatter, season by season': dict(disp='quasi'),
    'a negative binomial each season, the record\'s seasons independent': dict(disp='nb_seasons'),
    'each zone\'s own level taken as known': dict(level='plugin'),
    'a Poisson spread': dict(disp='poisson'),
    'every zone at the network rate, with no level of its own': dict(own='none'),
    'the whole record, not since the last inspection': dict(window='whole'),
    'the careful but hurried pass': CAREFUL,
}
# each sentence executed the way a run would act on it, and no further: told that a zone keeps its own level, a run
# estimates that level from the zone's confirmed seasons and judges the zone against it
HINTS = [
    ('a zone that runs high when its protection is sound runs high every season: judge each zone against its own '
     'confirmed-sound seasons', dict(disp='nb', level='plugin')),
    ('a zone\'s own sound level is only as certain as its few confirmed seasons make it', dict()),
    ('most referred zones failed partway through their record since inspection: value the refit on the state each had '
     'reached by the end of 2026', dict(avoided='last_season')),
    ('the reclosers with no radio link keep their own drifting clocks and only their last events between site visits',
     dict(clock='aligned', fill=True)),
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


def expected_since(Rx, zones):
    """a run's sound expectation since each zone's last inspection, at the level it gives the zone"""
    DF = Rx['DF']
    out = {}
    for z in zones:
        W = Rx['window'](z, 2026)
        out[Rx['zones'][z]] = float(round(Rx['Eu'][z] * sum(DF.loc[(z, s), 'Ef'] for s in W) + 1e-12, 1))
    return out


def pass_values(Rx, gold_ref):
    """what a pass files for each result, from its run"""
    tot = {str(s): int(round(Rx['season_tot'][s])) for s in A.SEASONS}
    tot['radioless_2026'] = int(round(Rx['radioless26']))
    return {'R1': tot,
            'R2': int(round(Rx['excess26'])),
            'R3': sorted(Rx['ref_names']),
            'R4': expected_since(Rx, gold_ref),
            'R5': dict({str(s): Rx['alerts'][s] for s in A.SEASONS}, sound_per_season=round(Rx['false_per'], 2)),
            'R6': {'referred_inspected': Rx['v_ref'], 'confirmed': Rx['v_conf'], 'missed': Rx['v_miss']},
            'R7': int(round(Rx['avoided_total']))}


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
    g, c = pass_values(R, R['ref']), pass_values(Rc, R['ref'])
    tot_q = {str(s): Q['season_tot'][s] for s in A.SEASONS}
    tot_q['radioless_2026'] = Q['radioless26']

    def pct(v, p):
        return [round(v * (1 - p)), round(v * (1 + p))]
    b1 = dict(F['bands']['season_totals'], radioless_2026=F['bands']['radioless_2026'])
    out = [
        {'id': 'R1', 'name': 'lightning faults per season, the radio-less zones\' 2026', 'graded_as': 'Component 1',
         'figure': 'season_totals_with_radioless', 'depends': [], 'golden': g['R1'], 'bands': b1,
         'passes': {'quick': tot_q, 'careful': c['R1'], 'thorough': g['R1']}},
        {'id': 'R2', 'name': '2026 faults failed protection caused', 'graded_as': 'Component 3', 'figure': 'excess_2026',
         'depends': ['R1'], 'golden': F['excess_2026'], 'band': F['bands']['excess_2026'],
         'partly': pct(F['excess_2026'], 0.2),
         'passes': {'quick': None, 'careful': c['R2'], 'thorough': F['excess_2026']}},
        {'id': 'R3', 'name': 'zones referred for the 2027 refit', 'graded_as': 'Recommendation', 'figure': 'referred_zones',
         'depends': ['R1'], 'golden': g['R3'],
         'passes': {'quick': Q['ref'], 'careful': c['R3'], 'thorough': g['R3']}},
        {'id': 'R4', 'name': 'the referred zones against sound protection', 'graded_as': 'Ask (record since inspection)',
         'figure': 'expected_since_inspection', 'depends': ['R1'], 'golden': g['R4'],
         'bands': F['bands']['expected_since_inspection'],
         'passes': {'quick': None, 'careful': c['R4'], 'thorough': g['R4']}},
        {'id': 'R5', 'name': 'the alert load: referrals each season, sound ones', 'graded_as': 'Ask (alert load)',
         'figure': 'alert_load', 'depends': ['R3'], 'golden': g['R5'],
         'bands': dict(F['bands']['alerts'], sound_per_season=F['bands']['false_per_season']),
         'partly_share': 0.6, 'passes': {'quick': None, 'careful': c['R5'], 'thorough': g['R5']}},
        {'id': 'R6', 'name': 'referrals against the following inspections', 'graded_as': 'Ask (inspection check)',
         'figure': 'validation_core', 'depends': ['R3', 'R5'], 'golden': g['R6'], 'bands': F['bands']['validation_core'],
         'passes': {'quick': None, 'careful': c['R6'], 'thorough': g['R6']}},
        {'id': 'R7', 'name': 'faults the refit avoids, average season', 'graded_as': 'Component 2',
         'figure': 'avoided_average_season', 'depends': ['R1', 'R3'], 'golden': F['avoided_average_season'],
         'band': F['bands']['avoided_average_season'], 'partly': pct(F['avoided_average_season'], 0.2),
         'passes': {'quick': None, 'careful': c['R7'], 'thorough': F['avoided_average_season']}},
    ]
    # where frontier runs have lost the same kind of move (references/precedents.json): a zone's seasons taken as
    # independent though they share its level (L35), the pooled figure decided on after the split was seen (L09), units
    # never checked for varying beyond sampling error (L33), a rule certified by checks that cannot see the problem (L28,
    # L29), cohorts pooled though their rates drift and history taken as informative of the forward window (L12, N02)
    for r in out:
        if r['id'] in PRECEDENTS:
            r['precedent'] = PRECEDENTS[r['id']]
    return out


def forcing(target, R, L):
    """the call's two sides: the golden family's sets, the fitted inputs moved by their defensible spread, the
    shortcuts' sets"""
    lo, hi = A.level_ci(R['lv_groups'], R['a_lv'], R['k_lv'], R['ll_lv'])
    fam = {'match window -0.4 to 0.5 s': {'win': (-0.4, 0.5)}, 'match window -1.0 to 1.2 s': {'win': (-1.0, 1.2)},
           'no transformer density term': {'spec': 'notx'}, 'faults matched within 300 m': {'rmax': 0.3, 'rexp': 0.4},
           'faults matched within 500 m': {'rmax': 0.5, 'rexp': 0.4}, 'weak positive discharges left out': {'excl_ic': True},
           'each level from every confirmed season': {'own': 'all'},
           'a stroke-level sound model (current and distance)': {'expo': 'stroke'},
           'the replay with only the inspections completed by then': {'asof': True},
           'unread months restored at the zone\'s rate since inspection': {'fill_rate': 'window'}}
    pert = {'the sound rate 10 per cent lower (about five standard errors)': {'rate_scale': 0.9},
            'the sound rate 10 per cent higher': {'rate_scale': 1.1},
            'the level shape at its 95 per cent interval\'s low end (%.2f)' % lo: {'a_fix': lo},
            'the level shape at its 95 per cent interval\'s high end (%.2f)' % hi: {'a_fix': hi},
            'the seasons\' scatter size 20 per cent smaller': {'klv_scale': 0.8},
            'the seasons\' scatter size 20 per cent larger': {'klv_scale': 1.2}}
    gold = sorted(R['ref_names'])
    return {'kind': 'set', 'golden_answer': gold,
            'golden_family': [{'name': n, 'answer': sorted(A.run(target, o, L=L)['ref_names'])} for n, o in fam.items()],
            'perturbations': [{'input': n, 'answer': sorted(A.run(target, o, L=L)['ref_names'])} for n, o in pert.items()]}


def _grader():
    import importlib.util
    p = os.path.join(C.TASK, '..', '.claude', 'skills', 'stumping', 'effort.py')
    spec = importlib.util.spec_from_file_location('effort_skill', os.path.abspath(p))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def grade_hints(res, hints, gold_ref):
    """each hint executed literally on the careful pass: the results it moves from short of Right to Right"""
    G = _grader()
    out = []
    for sentence, Rh in hints:
        pv = pass_values(Rh, gold_ref)
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
    H = grade_hints(res, hints, R['ref'])
    E = {'results': res, 'hints': H, 'routes': routes, 'forcing': forcing(target, R, L),
         'weights': {'recommendation': 14, 'components': 24, 'asks': 55, 'instruction': 7}}
    json.dump(E, open(path, 'w'), indent=1, sort_keys=False)
    return E, R, Rc
