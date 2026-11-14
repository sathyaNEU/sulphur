"""The effort test computed on the cut pack (stumping Part 3): the quick pass (the control room log's own counts and
cause codes, the outage system's own durations), the careful but hurried pass (the reflex route: every move a run
makes unprompted set right, every stump hurried), the thorough pass (the golden), the stump factorial (each stump
dropped alone from the golden and fixed alone on the reflex route), and the forcing block (the golden family's
rivals, the shortcuts, the perturbed inputs). Writes generator/effort.json. Nothing here reads the prompt."""
import collections
import datetime as dt
import json
import os

import numpy as np
import pandas as pd

import common as C
import golden as G

# the reflex route: every move a run makes unprompted set right (the arch 5 runs' moves, R81 to R83), every stump hurried
HURRY = dict(gulf_string='signature', contacts='signature', deposit='const')
STUMPS = [
    ('J1', 'the failing string on the Gulf line told from the salt by its flashovers at deposits the salt has never flashed at',
     ('gulf_string',), ['L48', 'L26']),
    ('J2', "a summer contact place read on its own contact temperatures against its trims: the conductor reaching the "
           "circuit built under it, not a tree", ('contacts',), ['L47', 'L26']),
    ('J3', "each section's deposit carried to 31 October on the onshore wind the test insulators' gains follow, through the "
           "southerly blow after the last readings", ('deposit',), ['L15', 'N13']),
]
REFLEXES = [
    ('X1', 'one fault per two-ended trip sequence, relay clocks set on SCADA', ['R01', 'R28', 'R29', 'R46']),
    ('X2', 'lightning faults matched to strokes on the true time along the line', ['R32']),
    ('X3', 'member impact from the sequence of events and the members by feeder', ['R46']),
    ('X4', 'the work already done applied (guards, replaced strings, trims)', ['R02']),
    ('X5', 'each fault located from both ends against the date\'s network, the solar farm\'s infeed taken out', ['R81']),
    ('X6', 'a deposit build-up with rain cleaning carried from each section\'s last wash', ['R82']),
    ('X7', "each cause's signature read off the confirmed cases (strokes, roosts, the stations' fog, light rain, peak load)",
     ['R83']),
]
VARIANTS = {
    'fog: dew point within 0.3 C': dict(fog_dep=0.3), 'fog: dew point within 0.8 C': dict(fog_dep=0.8),
    'storm: 2 strokes within 8 km': dict(storm_n=2), 'storm: 5 strokes within 8 km': dict(storm_n=5),
    'storm: 3 strokes within 6 km': dict(storm_km=6.0), 'storm: 3 strokes within 10 km': dict(storm_km=10.0),
    'conductor at 36 C or more': dict(tc_min=36.0), 'conductor at 44 C or more': dict(tc_min=44.0),
    'front gusts 8.5 m/s': dict(gust_min=8.5), 'front gusts 11 m/s': dict(gust_min=11.0),
    'repeat window 350 m': dict(win_km=0.35), 'repeat window 450 m': dict(win_km=0.45),
    'flashover level: lowest': dict(level='min'), 'flashover level: 5th percentile': dict(level_q=5),
    'flashover level: 20th percentile': dict(level_q=20),
    'deposit rate: nearest test site': dict(rate='nearest'), 'deposit rate: log-linear, all sites': dict(rate='loglin'),
    'deposit rate: log-linear, coastal sites': dict(rate='loglin_coast'),
    'soaking rain leaves 35 per cent': dict(keep=0.35), 'soaking rain leaves 60 per cent': dict(keep=0.6),
    'onshore wind, first power': dict(wind_k=1.0), 'onshore wind, power 1.5': dict(wind_k=1.5),
    'onshore wind, cubed': dict(wind_k=3.0), 'onshore from 125 degrees': dict(gulf_from=125.0),
    'onshore from 155 degrees': dict(gulf_from=155.0), 'onshore wind at the airport only': dict(wind_src='airport'),
    'salt with no wind share': dict(salt_bg=0.0), 'half the salt whatever the wind': dict(salt_bg=0.5),
    'low flashovers: below half the median': dict(low_cut=0.5), 'low flashovers: below 0.7 of the median': dict(low_cut=0.7),
    'low flashovers: four or more': dict(low_n=4),
    'contact temperature falling 0.6 C a year': dict(traj_slope=-0.6),
    'contact temperature falling 1.0 C a year': dict(traj_slope=-1.0), 'five contacts since the trim': dict(traj_n=5),
}
PERTURB = {
    'deposit rate -20%': dict(rate_scale=0.8), 'deposit rate +20%': dict(rate_scale=1.2),
    'flashover level -20%': dict(level_scale=0.8), 'flashover level +20%': dict(level_scale=1.2),
    'conductor threshold -4 C': dict(tc_min=36.0), 'conductor threshold +4 C': dict(tc_min=44.0),
}
SHORTCUTS = {
    'the deposit as the latest test reading at the nearest site': dict(deposit='latest'),
    'every section that has flashed over washed': dict(deposit='history'),
    'the lowest deposit at a flashover with a constant rate': dict(deposit='const', level='min'),
}


def lname(lid):
    return 'Line %d' % int(lid[1:])


def worklist(r):
    wl = dict(guards=[], strings=[], spans=[], stands=[], clearance=[])
    for rl in r['repeat']:
        if rl['fixed']:
            continue
        key = {'bird': 'guards', 'insulator': 'strings', 'growin': 'spans', 'fallin': 'stands', 'hardware': 'clearance'}[rl['cause']]
        if key in ('spans', 'clearance') and rl['span']:
            wl[key].append((rl['line'], rl['span'][0], rl['span'][1]))
        elif key == 'stands':
            wl[key].append((rl['line'], rl['s_min'], rl['s_max']))
        else:
            wl[key].append((rl['line'], rl['structure'], rl['structure']))
    wl['wash'] = sorted(k for k, v in r['deposits']['sections'].items() if v['due'])
    return wl


def snap(wl, gold, tol=2):
    """a place within two structures of the golden's place on the same line reads as the golden's"""
    out = {}
    for k in ('guards', 'strings', 'spans', 'stands', 'clearance'):
        labs = []
        for (lid, a, b) in wl.get(k, []):
            lab = None
            for (gl, ga, gb) in gold.get(k, []):
                if gl == lid and a <= gb + tol and b >= ga - tol:
                    lab = label(k, gl, ga, gb)
                    break
            labs.append(lab or label(k, lid, a, b))
        out[k] = sorted(set(labs))
    out['wash'] = [wash_label(x) for x in wl['wash']]
    return out


def label(k, lid, a, b):
    if k == 'clearance':
        return 'restore the clearance: %s, structures %d-%d' % (lname(lid), a, b)
    if k == 'spans':
        return 'clear the span: %s, structures %d-%d' % (lname(lid), a, b)
    if k == 'stands':
        return 'remove the hazard trees: %s, structures %d-%d' % (lname(lid), a, b)
    if k == 'guards':
        return 'perch guards: %s, structure %d' % (lname(lid), a)
    return 'replace the string: %s, structure %d' % (lname(lid), a)


def wash_label(sid):
    lid, sec = sid.split('-W')
    return 'wash: %s, Section %s' % (lname(lid), sec)


def flat(wl):
    out = []
    for k in ('guards', 'strings', 'spans', 'stands', 'clearance', 'wash'):
        out += list(wl.get(k, []))
    return sorted(out)


def by_year(faults):
    return {str(y): n for y, n in sorted(collections.Counter(C.to_local(f['t']).year for f in faults).items())}


def by_cause_2026(faults):
    c = collections.Counter(f['cause'] for f in faults if C.to_local(f['t']).year == 2026)
    return {k: int(c.get(k, 0)) for k in G_CAUSES}


G_CAUSES = ['lightning', 'bird', 'fog', 'insulator', 'growin', 'fallin', 'vehicle', 'hardware', 'unknown']


def impact_table(imp):
    tot = dict(sustained=0, minutes=0.0, momentary=0)
    for v in imp.values():
        for k in tot:
            tot[k] += v[k]
    return {'sustained': int(tot['sustained']), 'member_minutes': int(round(tot['minutes'])), 'momentary': int(tot['momentary'])}


GULF = ('L01', 'L02', 'L03', 'L04')


def results_of(r, gold_wl):
    raw = worklist(r)
    wl = snap(raw, gold_wl)
    gulf_strings = snap(dict(guards=[], strings=[x for x in raw['strings'] if x[0] in GULF], spans=[], stands=[], clearance=[],
                             wash=[]), gold_wl)['strings']
    dep = r['deposits']
    # the sections the October round reached before the blow of 24 to 26 October, and whether each is due again
    early = sorted(k for k, v in dep['sections'].items() if v['last_wash'] is not None
                   and dt.date(2026, 10, 1) <= v['last_wash'] < dt.date(2026, 10, 23))
    return dict(R1=by_year(r['faults']), R2=by_cause_2026(r['faults']), R3=impact_table(r['impact']),
                R4=gulf_strings, R5=sorted(wl['clearance']),
                R6=[wash_label(k) for k in early if dep['sections'][k]['due']], wash=wl['wash'],
                R7={wash_label(k).replace('wash: ', ''): round(v['deposit'], 4) for k, v in sorted(dep['sections'].items())},
                R8=sorted(wl['guards'] + wl['strings'] + wl['spans'] + wl['stands'] + wl['clearance']), wl=wl,
                level=dep['level'])


def quick(target, gold_res):
    """the control room log's counts and cause codes, the outage system's durations"""
    log = G._wb(os.path.join(target, C.FILES['crlog']), '69 kV log')
    trips = log[log['Event'].isin(['Line trip, reclosed', 'Line lockout'])]
    yrs = pd.to_datetime(trips['Date']).dt.year
    r1 = {str(y): int(n) for y, n in sorted(collections.Counter(yrs).items())}
    code = {'LTG': 'lightning', 'CONTAM': 'fog', 'TREE': 'growin', 'WIND': 'fallin', 'VEH': 'vehicle', 'EQUIP': 'hardware',
            'BIRD': 'bird', 'UNK': 'unknown'}
    t26 = trips[yrs == 2026]
    c = collections.Counter(code.get(x, 'unknown') for x in t26['Cause'])
    r6 = {k: int(c.get(k, 0)) for k in G_CAUSES}
    import sqlite3
    con = sqlite3.connect(os.path.join(target, C.FILES['oms']))
    los = pd.read_sql("select * from outage where cause_code='LOS'", con)
    con.close()
    los = los[pd.to_datetime(los['start_time']).dt.year == 2026]
    mins = (pd.to_datetime(los['restore_time']) - pd.to_datetime(los['start_time'])).dt.total_seconds() / 60
    r5 = {'sustained': int(los['members_out'].sum()), 'member_minutes': int(round((los['members_out'] * mins).sum())), 'momentary': 0}
    return dict(R1=r1, R5=r5, R6=r6)


def _run(target, opts, d):
    return G.run(target, opts, d=d)


def build(target, out_path):
    d = G.load(target)
    gold_r = _run(target, G.GOLD, d)
    gold_wl_raw = worklist(gold_r)
    gold = results_of(gold_r, gold_wl_raw)
    care_r = _run(target, dict(G.GOLD, **HURRY), d)
    care = results_of(care_r, gold_wl_raw)
    q = quick(target, gold)
    keys = ('R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8')
    routes = {}
    fact = []
    for sid, name, ks, prec in STUMPS:
        drop = results_of(_run(target, dict(G.GOLD, **{k: HURRY[k] for k in ks}), d), gold_wl_raw)
        alone = results_of(_run(target, dict(G.GOLD, **dict(HURRY, **{k: G.GOLD[k] for k in ks})), d), gold_wl_raw)
        moved = [k for k in keys if drop[k] != gold[k]]
        rescued = [k for k in keys if alone[k] == gold[k] and care[k] != gold[k]]
        fact.append(dict(id=sid, name=name, kind='stump', precedent=prec,
                         dropped=dict(answer=flat(drop['wl']), results_moved=moved),
                         alone=dict(answer=flat(alone['wl']), results_rescued=rescued)))
        routes[sid] = (drop, alone)
    for xid, name, prec in REFLEXES:
        fact.append(dict(id=xid, name=name, kind='reflex', precedent=prec))
    fam, fam_r7 = [], []
    for name, v in VARIANTS.items():
        run_v = _run(target, dict(G.GOLD, **v), d)
        rr = results_of(run_v, gold_wl_raw)
        fam.append(dict(name=name, answer=flat(rr['wl']), r2=rr['R2'], level=round(run_v['deposits']['level'], 4),
                        ratio_W1=round(run_v['deposits']['sections']['L02-W1']['deposit'] / run_v['deposits']['level'], 2),
                        ratio_W6=round(run_v['deposits']['sections']['L02-W6']['deposit'] / run_v['deposits']['level'], 2)))
        fam_r7.append(rr['R7'])
    pert = []
    for name, v in PERTURB.items():
        rr = results_of(_run(target, dict(G.GOLD, **v), d), gold_wl_raw)
        pert.append(dict(input=name, answer=flat(rr['wl'])))
    shortcuts = [dict(name='the reflex route (every stump hurried)', answer=flat(care['wl']))]
    for sid, (drop, alone) in routes.items():
        shortcuts.append(dict(name='the golden with %s hurried' % sid, answer=flat(drop['wl'])))
    direct = results_of(_run(target, dict(G.GOLD, **dict(HURRY, deposit='latest')), d), gold_wl_raw)
    shortcuts.append(dict(name='the direct route (the patrols, the confirmed cases and the latest test readings read raw)',
                          answer=flat(direct['wl'])))
    for name, v in SHORTCUTS.items():
        rr = results_of(_run(target, dict(G.GOLD, **v), d), gold_wl_raw)
        shortcuts.append(dict(name=name, answer=flat(rr['wl'])))
    # bands: the yearly counts within one, the cause counts within two, member impact within 2 per cent, each section's
    # deposit across the golden family
    r1b = {k: [v - 1, v + 1] for k, v in gold['R1'].items()}
    # the conductor reaching the circuit below reads as equipment or hardware or as other: those two cells within 3
    r2b = {k: [max(0, v - (3 if k in ('hardware', 'unknown') else 2)), v + (3 if k in ('hardware', 'unknown') else 2)]
           for k, v in gold['R2'].items()}
    r3b = {k: [int(v * 0.98), int(v * 1.02) + 1] for k, v in gold['R3'].items()}
    r7b = {k: [round(min([gold['R7'][k]] + [x[k] for x in fam_r7]), 4), round(max([gold['R7'][k]] + [x[k] for x in fam_r7]), 4)]
           for k in gold['R7']}
    hints = []
    for sid, name, ks, prec in STUMPS:
        alone = routes[sid][1]
        hints.append(dict(sentence=name, rescues=[k for k in keys if alone[k] == gold[k] and care[k] != gold[k]]))

    def grade_tab(val, gold_v, bands):
        ok = sum(1 for k in gold_v if bands[k][0] <= val.get(k, -999) <= bands[k][1])
        return 'right' if ok == len(gold_v) else ('partly' if ok >= len(gold_v) / 2 else 'missed')

    res = [
        dict(id='R1', name='the 69 kV faults by year, January 2022 to October 2026', graded_as='Ask 1', figure='faults_by_year',
             depends=[], independent='', golden=gold['R1'], bands=r1b, partly_share=0.6,
             passes=dict(quick=q['R1'], careful=care['R1'], thorough=gold['R1'])),
        dict(id='R2', name='the 2026 faults by cause', graded_as='Ask 2', figure='faults_2026_by_cause', depends=['R1'],
             independent='', golden=gold['R2'], bands=r2b, partly_share=0.75,
             passes=dict(quick=q['R6'], careful=dict(value=care['R2'], grade=grade_tab(care['R2'], gold['R2'], r2b),
                                                      why="the Gulf string's fog flashovers booked as salt and the Line 6 "
                                                          "contacts as grow-ins"),
                         thorough=gold['R2']), precedent=['L48', 'L47']),
        dict(id='R3', name='the 2026 member interruptions, member-minutes and momentary member events from 69 kV faults',
             graded_as='Ask 3', figure='member_impact_2026', depends=['R1'], independent='', golden=gold['R3'], bands=r3b,
             passes=dict(quick=q['R5'], careful=care['R3'], thorough=gold['R3'])),
        dict(id='R4', name="the failing string on the Gulf lines: Line 2 structure 63", graded_as='Component 1',
             figure='gulf_strings', depends=['R1'], independent='', golden=gold['R4'],
             passes=dict(quick=[], careful=care['R4'], thorough=gold['R4']), precedent=['L48', 'L26']),
        dict(id='R5', name='the summer contact place that is not a tree: the clearance to restore at Line 6 structures 57-58',
             graded_as='Component 2', figure='clearance_items', depends=['R1'],
             independent='', golden=gold['R5'], passes=dict(quick=[], careful=care['R5'], thorough=gold['R5']),
             precedent=['L47', 'L26']),
        dict(id='R6', name='the sections washed in October before the blow that are due again: Line 2 sections 1 and 6',
             graded_as='Component 3', figure='resalted_due',
             depends=[], independent='the test insulators, the station winds, the washing log and rain', golden=gold['R6'],
             passes=dict(quick=[], careful=care['R6'], thorough=gold['R6']), precedent=['L15', 'N13']),
        dict(id='R7', name="each washing section's salt deposit on 31 October 2026", graded_as='Ask 5', figure='wash_deposits',
             depends=[], independent='the test insulators, the station winds, the washing log and rain', golden=gold['R7'],
             bands=r7b, partly_share=0.5,
             passes=dict(quick={}, careful=dict(value=care['R7'], grade=grade_tab(care['R7'], gold['R7'], r7b),
                                                 why='the deposit at the test insulators\' average rate'),
                         thorough=gold['R7']), precedent=['L15', 'N13']),
        dict(id='R8', name='every open repeat location with its cause and fix', graded_as='Ask 4', figure='repeat_locations_open',
             depends=['R4', 'R5'], independent='', golden=gold['R8'],
             passes=dict(quick=[], careful=care['R8'], thorough=gold['R8']), precedent=['L48', 'L47']),
        dict(id='R9', name="the memo's work list", graded_as='Ask 6', figure='work_list', depends=['R4', 'R5', 'R6'],
             independent='', golden=flat(gold['wl']), passes=dict(quick=[], careful=flat(care['wl']), thorough=flat(gold['wl'])),
             precedent=['L48', 'L47', 'L15']),
        dict(id='R10', name='the work list', graded_as='Recommendation', figure='work_list', depends=['R4', 'R5', 'R6'],
             independent='', golden=flat(gold['wl']), passes=dict(quick=[], careful=flat(care['wl']), thorough=flat(gold['wl'])),
             precedent=['L48', 'L47', 'L15']),
    ]
    out = dict(results=res, hints=hints,
               routes=[dict(name='the golden', answer=flat(gold['wl']), golden=True)] + shortcuts,
               weights=dict(recommendation=14, components=27, asks=52, instruction=7),
               forcing=dict(kind='set', golden_family=fam, shortcuts=shortcuts, perturbations=pert),
               factorial=dict(golden_answer=flat(gold['wl']), reflex_route=dict(answer=flat(care['wl'])), judgments=fact),
               direct_route=dict(answer=flat(direct['wl'])))
    json.dump(out, open(out_path, 'w'), indent=1, default=str)
    write_figures(gold_r, gold, care, q, fam, r7b, direct)
    return gold_r, gold, care, q


def write_figures(gold_r, gold, care, q, fam=(), r7b=None, direct=None):
    """every figure the answer blocks state, from the golden route run on the cut pack"""
    dep = gold_r['deposits']
    imp = gold_r['impact']
    fs = gold_r['faults']
    lines26 = {lname(k): dict(sustained=int(v['sustained']), member_minutes=int(round(v['minutes'])), momentary=int(v['momentary']))
               for k, v in sorted(imp.items(), key=lambda kv: int(kv[0][1:]))}
    by_line_year = collections.defaultdict(dict)
    for (lid, yr), n in sorted(collections.Counter((f['line'], C.to_local(f['t']).year) for f in fs).items()):
        by_line_year[lname(lid)][str(yr)] = n
    rl_detail = []
    for rl in sorted(gold_r['repeat'], key=lambda x: (x['cause'], int(x['line'][1:]), x['structure'])):
        rl_detail.append(dict(line=lname(rl['line']), cause=rl['cause'], structure=rl['structure'], s_min=rl['s_min'], s_max=rl['s_max'],
                              span=list(rl['span']) if rl['span'] else None, faults=rl['n'],
                              first=C.to_local(rl['first']).date().isoformat(), last=C.to_local(rl['last']).date().isoformat(),
                              fixed=bool(rl['fixed'])))
    lv = dep['level']
    secs = {wash_label(k).replace('wash: ', ''): dict(deposit=round(v['deposit'], 4), ratio=round(v['deposit'] / lv, 2),
                                                     gulf_km=round(v['dist'], 2), due=bool(v['due']),
                                                     last_wash=v['last_wash'].isoformat() if v['last_wash'] else None)
            for k, v in sorted(dep['sections'].items())}
    # the Gulf string: its flashovers, the deposits it flashed at, the median at the Gulf's salt flashovers
    st = gold_r['strings'][0] if gold_r['strings'] else None
    gs = {}
    if st:
        ser = dep['series']
        own = sorted([f for f in fs if f.get('gulf_string')], key=lambda f: f['t'])
        vals = []
        for f in own:
            sid = G.section_of({'sections': ser}, f)
            vals.append(round(ser[sid]['series'][C.to_local(f['t']).date()], 4) if sid else None)
        sid0 = G.section_of({'sections': ser}, own[0])
        gs = dict(line=lname(st['line']), structure=st['structure'], flashovers=len(own),
                  first=C.to_local(own[0]['t']).date().isoformat(), last=C.to_local(own[-1]['t']).date().isoformat(),
                  below_level=sum(1 for v in vals if v is not None and v < lv),
                  below_cut=sum(1 for v in vals if v is not None and v < G.GOLD['low_cut'] * st['median']),
                  lowest_deposit=min(v for v in vals if v is not None), median_fog_deposit=round(st['median'], 4),
                  section=wash_label(sid0).replace('wash: ', ''),
                  section_washes_2025_26=[w.isoformat() for w in ser[sid0]['washes'] if dt.date(2025, 7, 1) <= w <= dt.date(2026, 6, 30)])
    # the summer contact place that is not vegetation, and the grow-ins' own falls
    sc = {}
    for c in gold_r['contacts']:
        sc = dict(line=lname(c['line']), structures='%d-%d' % (c['s_min'], c['s_max']), contacts_since_trim=c['n'],
                  trim=c['trim'].isoformat() if c['trim'] else None, slope_c_per_year=round(c['slope'], 1),
                  contact_temperature=[round(min(c['tc']), 1), round(max(c['tc']), 1)])
    # each grow-in's own fall, read the way the clearance contact was: on its contacts since its last trim, where four or more
    # fall in three or more summers
    veg_slopes = []
    vv = gold_r['d']['veg']
    for rl in gold_r['repeat']:
        if rl['cause'] != 'growin':
            continue
        ln = lname(rl['line'])
        last_c = max(C.to_local(f['t']).date() for f in rl['faults'])
        tr = [pd.Timestamp(x.completed).date() for x in vv[(vv['line'] == ln) & vv['work_type'].isin(['HOT SPOT', 'CYCLE TRIM'])].itertuples()
              if int(x.from_structure) <= rl['s_max'] + 1 and rl['s_min'] - 1 <= int(x.to_structure) and pd.Timestamp(x.completed).date() <= last_c]
        t_trim = max(tr) if tr else None
        after = [f for f in rl['faults'] if f['sig'].get('tc') and (t_trim is None or C.to_local(f['t']).date() > t_trim)]
        xs = [C.to_local(f['t']).year + C.to_local(f['t']).timetuple().tm_yday / 365.25 for f in after]
        ys = [f['sig']['tc'] for f in after]
        if len(xs) >= 4 and len(set(int(x) for x in xs)) >= 3:
            veg_slopes.append(round(float(np.polyfit(xs, ys, 1)[0]), 1))
    sc['vegetation_slopes'] = [min(veg_slopes), max(veg_slopes)] if veg_slopes else None
    fam_ratios = [min(min(x['ratio_W1'], x['ratio_W6']) for x in fam)] if fam else []
    fig = dict(
        faults_by_year=gold['R1'], faults_total=sum(gold['R1'].values()), faults_2026=gold['R1'].get('2026'),
        faults_by_line_year=dict(by_line_year),
        faults_2026_by_cause=gold['R2'],
        member_impact_2026=gold['R3'], member_impact_2026_by_line=lines26,
        gulf_string=gs, gulf_strings=gold['R4'], clearance_items=gold['R5'], clearance_contact=sc,
        spans_to_clear=gold['wl']['spans'], resalted_due=gold['R6'],
        repeat_locations_open=gold['R8'],
        wash_due=gold['wash'], wash_due_count=len(gold['wash']), work_list=flat(gold['wl']),
        work_list_counts={k: len(v) for k, v in gold['wl'].items()},
        repeat_locations=rl_detail,
        flashover_level=round(lv, 4), soaking_rain_keep=round(dep['keep'], 2), salt_background=round(dep['bg'], 2),
        wash_sections=secs, wash_deposits=gold['R7'], wash_deposit_bands=r7b,
        resalted={k: secs[k] for k in ('Line 2, Section 1', 'Line 2, Section 6')},
        resalted_lowest_family_ratio=fam_ratios[0] if fam_ratios else None,
        careful=dict(work_list=flat(care['wl']), R2=care['R2'], R4=care['R4'], R5=care['R5'], R6=care['R6'], wash=care['wash'],
                     R7={k: care['R7'][k] for k in ('Line 2, Section 1', 'Line 2, Section 6')},
                     resalted_ratio=[round(care['R7'][k] / care['level'], 2) for k in ('Line 2, Section 1', 'Line 2, Section 6')]),
        direct=dict(work_list=flat(direct['wl'])) if direct else None,
        quick=dict(R1=q['R1'], R5=q['R5'], R6=q['R6']),
    )
    tap = [rl for rl in gold_r['repeat'] if rl['line'] == 'L09' and rl['cause'] == 'insulator']
    if tap:
        fig['tap_string_beyond_tap_km'] = round(tap[0]['km'] - gold_r['d']['tap_km'], 1)
        fig['tap_km'] = gold_r['d']['tap_km']
    fig['filed'] = dict(system_kv=69, repeat_location_m=int(round(G.GOLD['win_km'] * 1000)),
                        underbuild_kv=float(str(gold_r['d']['structures']['underbuild'].dropna().iloc[0]).split()[0]))
    d_ = gold_r['d']
    e_w = G.deposit_series(d_, G.GOLD)['fit_err']
    e_c = G.deposit_series(d_, dict(G.GOLD, deposit='const'))['fit_err']
    fig['deposit_fit'] = dict(wind_error=round(e_w, 2), constant_error=round(e_c, 2), constant_worse_pct=int(round(100 * (e_c / e_w - 1))))
    fig['family_size'] = len(fam)
    levels = [lv] + [v['level'] for v in fam]
    fig['flashover_level_band'] = [round(min(levels), 3), round(max(levels), 3)]
    json.dump(fig, open(os.path.join(C.HERE, 'figures.json'), 'w'), indent=1, default=str)
    return fig


if __name__ == '__main__':
    gold_r, gold, care, q = build(C.TARGET, os.path.join(C.HERE, 'effort.json'))
    print(json.dumps({k: gold[k] for k in gold if k != 'wl'}, indent=1, default=str))
