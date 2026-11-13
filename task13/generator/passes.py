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

HURRY = dict(loc='relay', study_by_date=False, tap_infeed=False, fog='airport', survey=False, growin='season',
             deposit='history')
STUMPS = [
    ('S1', 'each fault located by the split of its residual current between the line ends', ('loc',), ['L22']),
    ('S2', 'faults before March 2024 read against the 2022 protection study', ('study_by_date',), ['N09']),
    ('S3', "the solar farm's ground infeed taken out of Shell Ridge's distance", ('tap_infeed',), ['L38', 'N27']),
    ('S4', 'night coastal faults split on the bay stations, the roost survey and light rain', ('fog', 'survey'), ['N26', 'L38', 'L26']),
    ('S5', "grow-in contacts told by the conductor's state, storms set apart", ('growin',), ['L26', 'L04']),
    ('S6', "each section's deposit carried from its last wash or soaking rain", ('deposit',), ['N02', 'N13']),
]
REFLEXES = [
    ('X1', 'one fault per two-ended trip sequence, relay clocks set on SCADA', ['R01', 'R28', 'R29', 'R46']),
    ('X2', 'lightning faults matched to strokes on the true time along the line', ['R32']),
    ('X3', 'member impact from the sequence of events and the members by feeder', ['R46']),
    ('X4', 'the work already done applied (guards, replaced strings, trims)', ['R02']),
]
VARIANTS = {
    'fog: dew point within 0.3 C': dict(fog_dep=0.3), 'fog: dew point within 0.8 C': dict(fog_dep=0.8),
    'storm: 2 strokes within 8 km': dict(storm_n=2), 'storm: 5 strokes within 8 km': dict(storm_n=5),
    'storm: 3 strokes within 6 km': dict(storm_km=6.0), 'storm: 3 strokes within 10 km': dict(storm_km=10.0),
    'conductor at 36 C or more': dict(tc_min=36.0), 'conductor at 44 C or more': dict(tc_min=44.0),
    'front gusts 8.5 m/s': dict(gust_min=8.5), 'front gusts 11 m/s': dict(gust_min=11.0),
    'flashover level: 5th percentile': dict(level='p5'), 'flashover level: 10th percentile': dict(level='p10'),
    'deposit rate: nearest test site': dict(rate='nearest'), 'deposit rate: linear in distance': dict(rate='linear'),
    'soaking rain leaves 35 per cent': dict(keep=0.35), 'soaking rain leaves 60 per cent': dict(keep=0.6),
    'repeat window 350 m': dict(win_km=0.35), 'repeat window 450 m': dict(win_km=0.45),
}
PERTURB = {
    'deposit rate -20%': dict(rate_scale=0.8), 'deposit rate +20%': dict(rate_scale=1.2),
    'flashover level -20%': dict(level_scale=0.8), 'flashover level +20%': dict(level_scale=1.2),
    'conductor threshold -4 C': dict(tc_min=36.0), 'conductor threshold +4 C': dict(tc_min=44.0),
}


def lname(lid):
    return 'Line %d' % int(lid[1:])


def worklist(r):
    wl = dict(guards=[], strings=[], spans=[], stands=[])
    for rl in r['repeat']:
        if rl['fixed']:
            continue
        key = {'bird': 'guards', 'insulator': 'strings', 'growin': 'spans', 'fallin': 'stands'}[rl['cause']]
        if key == 'spans' and rl['span']:
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
    for k in ('guards', 'strings', 'spans', 'stands'):
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
    for k in ('guards', 'strings', 'spans', 'stands', 'wash'):
        out += list(wl[k])
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


def results_of(r, gold_wl):
    wl = snap(worklist(r), gold_wl)
    tap = [x for x in wl['strings'] if 'Line 9,' in x]
    return dict(R1=by_year(r['faults']), R2=sorted(wl['spans'] + wl['stands']), R3=sorted(wl['guards'] + [x for x in wl['strings'] if 'Line 9,' not in x]),
                R4=tap, R5=impact_table(r['impact']), R6=by_cause_2026(r['faults']), R7=wl['wash'],
                R8=sorted(wl['guards'] + wl['strings'] + wl['spans'] + wl['stands']), wl=wl)


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


def build(target, out_path):
    gold_r = G.run(target, G.GOLD)
    gold_wl_raw = worklist(gold_r)
    gold = results_of(gold_r, gold_wl_raw)
    care_r = G.run(target, HURRY)
    care = results_of(care_r, gold_wl_raw)
    q = quick(target, gold)
    routes = {}
    fact = []
    for sid, name, keys, prec in STUMPS:
        drop = results_of(G.run(target, dict(G.GOLD, **{k: HURRY[k] for k in keys})), gold_wl_raw)
        alone = results_of(G.run(target, dict(HURRY, **{k: G.GOLD[k] for k in keys})), gold_wl_raw)
        moved = [k for k in ('R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8') if drop[k] != gold[k]]
        rescued = [k for k in ('R2', 'R3', 'R4', 'R6', 'R7', 'R8') if alone[k] == gold[k] and care[k] != gold[k]]
        fact.append(dict(id=sid, name=name, kind='stump', precedent=prec,
                         dropped=dict(answer=flat(drop['wl']), results_moved=moved),
                         alone=dict(answer=flat(alone['wl']), results_rescued=rescued)))
        routes[sid] = (drop, alone)
    for xid, name, prec in REFLEXES:
        fact.append(dict(id=xid, name=name, kind='reflex', precedent=prec))
    fam = []
    for name, v in VARIANTS.items():
        run_v = G.run(target, dict(G.GOLD, **v))
        rr = results_of(run_v, gold_wl_raw)
        fam.append(dict(name=name, answer=flat(rr['wl']), r6=rr['R6'], level=round(run_v['deposits']['level'], 4)))
    pert = []
    for name, v in PERTURB.items():
        rr = results_of(G.run(target, dict(G.GOLD, **v)), gold_wl_raw)
        pert.append(dict(input=name, answer=flat(rr['wl'])))
    shortcuts = [dict(name='the reflex route (every stump hurried)', answer=flat(care['wl']))]
    for sid, (drop, alone) in routes.items():
        shortcuts.append(dict(name='the golden with %s hurried' % sid, answer=flat(drop['wl'])))
    # bands
    r1b = {k: [v - 1, v + 1] for k, v in gold['R1'].items()}
    r6b = {k: [max(0, v - 2), v + 2] for k, v in gold['R6'].items()}
    r5b = {k: [int(v * 0.98), int(v * 1.02) + 1] for k, v in gold['R5'].items()}
    hints = []
    for sid, name, keys, prec in STUMPS:
        alone = routes[sid][1]
        hints.append(dict(sentence=name, rescues=[k for k in ('R2', 'R3', 'R4', 'R6', 'R7', 'R8') if alone[k] == gold[k] and care[k] != gold[k]]))

    def grade_tab(val, gold_v, bands):
        ok = sum(1 for k in gold_v if bands[k][0] <= val.get(k, -999) <= bands[k][1])
        return 'right' if ok == len(gold_v) else ('partly' if ok >= len(gold_v) / 2 else 'missed')

    res = [
        dict(id='R1', name='the 69 kV faults by year, January 2022 to October 2026', graded_as='Ask 1', figure='faults_by_year', depends=[],
             independent='', golden=gold['R1'], bands=r1b, partly_share=0.6,
             passes=dict(quick=q['R1'], careful=care['R1'], thorough=gold['R1'])),
        dict(id='R6', name='the 2026 faults by cause', graded_as='Ask 2', figure='faults_2026_by_cause', depends=['R1'], independent='',
             golden=gold['R6'], bands=r6b, partly_share=0.75,
             passes=dict(quick=q['R6'], careful=dict(value=care['R6'], grade=grade_tab(care['R6'], gold['R6'], r6b),
                                                      why='birds read as failing strings without the survey, the bay fog off the airport'),
                         thorough=gold['R6']), precedent=['N26', 'L38']),
        dict(id='R5', name='the 2026 member interruptions, member-minutes and momentary member events from 69 kV faults',
             graded_as='Ask 3', figure='member_impact_2026', depends=['R1'], independent='', golden=gold['R5'], bands=r5b,
             passes=dict(quick=q['R5'], careful=care['R5'], thorough=gold['R5'])),
        dict(id='R3', name='the night repeat locations: roost structures for perch guards and failing strings',
             graded_as='Component 2', figure='night_repeat_locations', depends=['R1'], independent='', golden=gold['R3'],
             passes=dict(quick=[], careful=care['R3'], thorough=gold['R3']), precedent=['N26', 'L38', 'L26']),
        dict(id='R4', name="the tap line's repeat location", graded_as='Component 3', figure='tap_repeat_location', depends=['R1'],
             independent='', golden=gold['R4'], passes=dict(quick=[], careful=care['R4'], thorough=gold['R4']), precedent=['L38', 'N27']),
        dict(id='R2', name='the vegetation repeat locations: grow-in spans to clear and hazard-tree stands', graded_as='Component 1',
             figure='vegetation_repeat_locations', depends=['R1'], independent='', golden=gold['R2'],
             passes=dict(quick=[], careful=care['R2'], thorough=gold['R2']), precedent=['L22', 'N09', 'L26', 'L04']),
        dict(id='R7', name='the washing sections due before the fog season', graded_as='Component 4', figure='wash_due',
             depends=[], independent='the deposit from the test insulators, the washing log and rain', golden=gold['R7'],
             passes=dict(quick=[], careful=care['R7'], thorough=gold['R7']), precedent=['N02', 'N13']),
        dict(id='R8', name='every open repeat location with its cause and fix', graded_as='Ask 4', figure='repeat_locations_open',
             depends=['R2', 'R3', 'R4'], independent='', golden=gold['R8'],
             passes=dict(quick=[], careful=care['R8'], thorough=gold['R8']), precedent=['L22', 'N09', 'N26', 'L38', 'N27', 'L26']),
        dict(id='R9', name="the memo's work list: each open repeat location's fix and the sections washed before 1 December",
             graded_as='Ask 5', figure='work_list', depends=['R2', 'R3', 'R4', 'R7'], independent='', golden=flat(gold['wl']),
             passes=dict(quick=[], careful=flat(care['wl']), thorough=flat(gold['wl'])), precedent=['L22', 'N26', 'N02']),
        dict(id='R10', name='the work list', graded_as='Recommendation', figure='work_list', depends=['R2', 'R3', 'R4', 'R7'],
             independent='', golden=flat(gold['wl']), passes=dict(quick=[], careful=flat(care['wl']), thorough=flat(gold['wl'])),
             precedent=['L22', 'N26', 'N02']),
    ]
    out = dict(results=res, hints=hints,
               routes=[dict(name='the golden', answer=flat(gold['wl']), golden=True)] + shortcuts,
               weights=dict(recommendation=14, components=24, asks=55, instruction=7),
               forcing=dict(kind='set', golden_family=fam, shortcuts=shortcuts, perturbations=pert),
               factorial=dict(golden_answer=flat(gold['wl']), reflex_route=dict(answer=flat(care['wl'])), judgments=fact))
    json.dump(out, open(out_path, 'w'), indent=1, default=str)
    write_figures(gold_r, gold, care, q, fam)
    return gold_r, gold, care, q


def write_figures(gold_r, gold, care, q, fam=()):
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
    secs = {wash_label(k).replace('wash: ', ''): dict(deposit=round(v['deposit'], 4), gulf_km=round(v['dist'], 2), due=bool(v['due']))
            for k, v in sorted(dep['sections'].items())}
    fig = dict(
        faults_by_year=gold['R1'], faults_total=sum(gold['R1'].values()), faults_2026=gold['R1'].get('2026'),
        faults_by_line_year=dict(by_line_year),
        faults_2026_by_cause=gold['R6'],
        member_impact_2026=gold['R5'], member_impact_2026_by_line=lines26,
        night_repeat_locations=gold['R3'], tap_repeat_location=gold['R4'], vegetation_repeat_locations=gold['R2'],
        repeat_locations_open=gold['R8'],
        wash_due=gold['R7'], work_list=flat(gold['wl']), work_list_counts={k: len(v) for k, v in gold['wl'].items()},
        repeat_locations=rl_detail,
        flashover_level=round(dep['level'], 4), deposit_rate_fit=[round(x, 4) for x in dep['coef']], soaking_rain_keep=round(dep['keep'], 2),
        wash_sections=secs,
        careful=dict(work_list=flat(care['wl']), R6=care['R6'], R7=care['R7'], R2=care['R2'], R3=care['R3'], R4=care['R4'], R8=care['R8']),
        quick=dict(R1=q['R1'], R5=q['R5'], R6=q['R6']),
    )
    # the relays' own distances against the golden location for the grow-in contacts at the spans on the work list
    offs = []
    for rl in gold_r['repeat']:
        if rl['cause'] != 'growin' or rl['fixed']:
            continue
        per = []
        for f in rl['faults']:
            ests = []
            ra, rb = f['rec'].get('a'), f['rec'].get('b')
            L = gold_r['d']['lines'][f['line']]
            if ra and ra['dist'] is not None:
                ests.append(ra['dist'])
            if rb and rb['dist'] is not None:
                ests.append(L['length'] - rb['dist'])
            if ests:
                per.append(abs(sum(ests) / len(ests) - f['km']))
        if per:
            offs.append(sorted(per)[len(per) // 2])
    fig['growin_relay_offset_km'] = [round(min(offs), 1), round(max(offs), 1)] if offs else None
    tap = [rl for rl in gold_r['repeat'] if rl['line'] == 'L09' and rl['cause'] == 'insulator']
    if tap:
        fig['tap_string_beyond_tap_km'] = round(tap[0]['km'] - gold_r['d']['tap_km'], 1)
        fig['tap_km'] = gold_r['d']['tap_km']
    fig['filed'] = dict(system_kv=69, repeat_location_m=int(round(G.GOLD['win_km'] * 1000)))
    levels = [dep['level']] + [v['level'] for v in fam]
    fig['flashover_level_band'] = [round(min(levels), 3), round(max(levels), 3)]
    json.dump(fig, open(os.path.join(C.HERE, 'figures.json'), 'w'), indent=1, default=str)
    return fig


if __name__ == '__main__':
    gold_r, gold, care, q = build(C.TARGET, os.path.join(C.HERE, 'effort.json'))
    print(json.dumps({k: gold[k] for k in gold if k != 'wl'}, indent=1, default=str))
