"""The effort test computed on the cut pack (stumping Part 3, architecture 7, Level 5):
the quick pass (control room log counts/causes, OMS durations), the careful but hurried pass
(the reflex route: every standard ETL/clock/two-ended/1D-ESDD move set right, all five Level-5
stumps hurried), the thorough pass (the golden), the 5-stump factorial (each stump dropped alone
from the golden and fixed alone on the reflex route), and the forcing block (18 honest golden-family
variants, 6 perturbations, and shortcuts). Writes generator/effort.json and generator/figures.json."""
import collections
import datetime as dt
import json
import os

import numpy as np
import pandas as pd

import common as C
import golden as G

# Reflex route: every standard utility ETL/hygiene/2-ended/1D-ESDD move set right, all 5 Level-5 stumps hurried
HURRY = dict(
    contacts='signature',
    tap_infeed='none',
    dc_mutual='uncoupled',
    deposit='esdd_wind',
    topology='static',
)
STUMPS = [
    ('J1', 'separating fixed 12.47 kV underbuild clearance spans from underbuilt grow-ins by post-trim IEEE 738 conductor temperature trajectories',
     ('contacts',), ['L47', 'L26']),
    ('J2', 'inverting ground-fault zero-sequence infeed from both YNd1 independent power producer lateral taps (Line 9 solar and Line 8 BESS)',
     ('tap_infeed',), ['L63', 'N21']),
    ('J3', 'solving the coupled 2-line zero-sequence network with mutual impedance Z0m on the 14.5 km double-circuit corridor shared by Lines 10 and 11',
     ('dc_mutual',), ['L58', 'L48']),
    ('J4', 'modeling joint two-state coastal contamination (soluble ESDD + slow-washing non-soluble NSDD) and fitting the 2D fog-flashover frontier',
     ('deposit',), ['L38', 'L42', 'L15']),
    ('J5', 'replaying chronological SCADA supervisory switching windows (ALT SRC / NORM SW) for as-operated member-minutes and Priority 1 allocation',
     ('topology',), ['N09', 'L55']),
]
REFLEXES = [
    ('X1', 'one fault per two-ended trip sequence, relay clocks set on SCADA', ['R01', 'R28', 'R29', 'R46']),
    ('X2', 'lightning faults matched to CG strokes on true time along the line', ['R32']),
    ('X3', 'restoration durations read from SCADA breaker/transfer events rather than OMS close times', ['R46']),
    ('X4', 'completed fixes after last fault removed (avian guards, replaced strings, vegetation trims)', ['R02']),
    ('X5', 'two-ended uncoupled residual-current split with Inland March 2024 autotransformer source change', ['R81']),
    ('X6', '1D wind-driven ESDD accumulation with rain washout carried from each section\'s last wash', ['R82']),
    ('X7', 'cause signatures read off confirmed cases (roost survey, substation bay fog, peak thermal load)', ['R83']),
]
VARIANTS = {
    'fog: dew point within 0.3 C': dict(fog_dep=0.3),
    'fog: dew point within 0.8 C': dict(fog_dep=0.8),
    'storm: 2 strokes within 8 km': dict(storm_n=2),
    'storm: 5 strokes within 8 km': dict(storm_n=5),
    'storm: 3 strokes within 6 km': dict(storm_km=6.0),
    'storm: 3 strokes within 10 km': dict(storm_km=10.0),
    'conductor threshold 36 C': dict(tc_min=36.0),
    'conductor threshold 44 C': dict(tc_min=44.0),
    'front gusts 8.5 m/s': dict(gust_min=8.5),
    'front gusts 11.0 m/s': dict(gust_min=11.0),
    'repeat window 350 m': dict(win_km=0.35),
    'repeat window 450 m': dict(win_km=0.45),
    'thermal slope cut -0.6 C/yr': dict(traj_slope=-0.6),
    'thermal slope cut -1.0 C/yr': dict(traj_slope=-1.0),
    'flashover level: 5th percentile': dict(level_q=5),
    'flashover level: 15th percentile': dict(level_q=15),
    'flashover level: 20th percentile': dict(level_q=20),
    'joint frontier: Poisson log-link': dict(beta_model='poisson'),
    'wind exponent 1.5': dict(wind_k=1.5),
    'wind exponent 2.5': dict(wind_k=2.5),
    'onshore bearing 125 deg': dict(gulf_from=125.0),
    'onshore bearing 155 deg': dict(gulf_from=155.0),
    'coastal log-linear ESDD rate': dict(rate='loglin_coast'),
}
PERTURB = {
    'deposit rate -20%': dict(rate_scale=0.8),
    'deposit rate +20%': dict(rate_scale=1.2),
    'flashover level -20%': dict(level_scale=0.8),
    'flashover level +20%': dict(level_scale=1.2),
    'conductor threshold -4 C': dict(tc_min=36.0),
    'conductor threshold +4 C': dict(tc_min=44.0),
}
SHORTCUTS = {
    'underbuilt filter for S1 (all underbuilt spans as clearance)': dict(contacts='underbuild_all'),
    'solar-only infeed for S2 (Coyote Draw only, Brushy Creek BESS unadjusted)': dict(tap_infeed='solar_only'),
    'constant +0.65 km shift for S3 (uncoupled L10/L11 plus empirical offset)': dict(dc_mutual='one_fact'),
    'nearest test-site NSDD shortcut for S4': dict(deposit='one_fact'),
    '2026-only SCADA switching replay for S5': dict(topology='one_fact_2026'),
    'over-weighted NSDD exponent (beta=1.50)': dict(deposit='over_nsdd'),
    'double-counted switched taps (over_both)': dict(topology='over_both'),
    'latest test reading at nearest site': dict(deposit='latest'),
    'every section that ever flashed over washed': dict(deposit='history'),
}

G_CAUSES = ['lightning', 'bird', 'fog', 'insulator', 'growin', 'fallin', 'vehicle', 'hardware', 'unknown']


def lname(lid):
    return 'Line %d' % int(lid[1:])


def wash_label(sid):
    lid, sec = sid.split('-W')
    return 'wash: %s, Section %s' % (lname(lid), sec)


def place_tuple(rl):
    cause = rl['cause']
    if cause in ('growin', 'hardware') and rl.get('span'):
        return (rl['line'], rl['span'][0], rl['span'][1], cause)
    if cause == 'fallin':
        return (rl['line'], rl['s_min'], rl['s_max'], cause)
    return (rl['line'], rl['structure'], rl['structure'], cause)


def rep_label(lid, a, b, cause):
    if cause == 'hardware':
        return 'restore clearance: %s, structures %d-%d' % (lname(lid), a, b)
    if cause == 'growin':
        return 'clear span: %s, structures %d-%d' % (lname(lid), a, b)
    if cause == 'fallin':
        return 'remove hazard trees: %s, structures %d-%d' % (lname(lid), a, b)
    if cause == 'bird':
        return 'perch guards: %s, structure %d' % (lname(lid), a)
    return 'replace string: %s, structure %d' % (lname(lid), a)


def snap_rep(rl, gold_open, tol=2):
    lid, a, b, cause = place_tuple(rl)
    for gl, ga, gb, gc in gold_open:
        if gl == lid and gc == cause and a <= gb + tol and b >= ga - tol:
            return rep_label(gl, ga, gb, gc)
    return rep_label(lid, a, b, cause)


def by_year(faults):
    return {str(y): n for y, n in sorted(collections.Counter(C.to_local(f['t']).year for f in faults).items())}


def by_cause_2026(faults):
    c = collections.Counter(f['cause'] for f in faults if C.to_local(f['t']).year == 2026)
    return {k: int(c.get(k, 0)) for k in G_CAUSES}


def impact_table(imp):
    tot = dict(sustained=0, minutes=0.0, momentary=0)
    for v in imp.values():
        for k in tot:
            tot[k] += v[k]
    return {'sustained': int(tot['sustained']), 'member_minutes': int(round(tot['minutes'])), 'momentary': int(tot['momentary'])}


def results_of(r, gold_open):
    prog = r['programme']
    open_rls = [rl for rl in r['repeat'] if not rl['fixed']]
    snapped_open = [(snap_rep(rl, gold_open), rl) for rl in open_rls]
    snapped_p1 = sorted(snap_rep(rl, gold_open) for rl in prog['funded'])
    snapped_p2 = sorted(snap_rep(rl, gold_open) for rl in prog['deferred'])
    snapped_ranked = sorted('%s [%s]' % (snap_rep(rl, gold_open), rl['priority']) for rl in prog['ranked'])
    washes = sorted(wash_label(sid) for sid in prog['due_washes'])

    # Critical Components (5 independent decisive steps)
    cc1 = sorted(lbl for lbl, rl in snapped_open if rl['cause'] == 'hardware')
    cc2 = sorted(lbl for lbl, rl in snapped_open if rl['line'] in ('L08', 'L09') and rl['cause'] == 'insulator')
    cc3 = sorted(lbl for lbl, rl in snapped_open
                 if (rl['line'] == 'L11' and rl['cause'] == 'insulator')
                 or (rl['line'] == 'L10' and rl['cause'] == 'growin' and rl['structure'] < 85))
    cc4 = list(washes)
    cc5 = impact_table(r['impact'])

    # Coupled Asks & Recommendation
    p1_program = sorted(washes + snapped_p1)
    mix = collections.Counter()
    for rl in prog['funded']:
        mix[rl['cause']] += rl['crew_days']
    mix['wash'] = prog['wash_days']
    corridor_p1 = sorted(snap_rep(rl, gold_open) for rl in prog['funded'] if rl['line'] in ('L08', 'L09', 'L10', 'L11', 'L15', 'L16'))
    mix_summary = sorted(['%s=%dd' % (k, v) for k, v in mix.items()] + corridor_p1)

    r1_combo = {}
    for k, v in by_year(r['faults']).items():
        r1_combo['year_' + k] = v
    for k, v in by_cause_2026(r['faults']).items():
        r1_combo['2026_' + k] = v

    dep = r['deposits']
    ceff_map = {wash_label(k).replace('wash: ', ''): round(v['ceff'], 4) for k, v in sorted(dep['sections'].items())}

    return dict(
        R1=r1_combo,
        R2=cc1,
        R3=cc2,
        R4=cc3,
        R5=cc4,
        R6=cc5,
        R7=mix_summary,
        R8=snapped_ranked,
        R9=snapped_p1,
        R10=p1_program,
        p2=snapped_p2,
        by_year=by_year(r['faults']),
        by_cause_2026=by_cause_2026(r['faults']),
        ceff=ceff_map,
        level=dep['level'],
    )


def quick(target):
    """The 10-minute pass: raw control room log counts & causes, raw OMS LOS durations."""
    log = G._wb(os.path.join(target, C.FILES['crlog']), '69 kV log')
    trips = log[log['Event'].isin(['Line trip, reclosed', 'Line lockout'])]
    yrs = pd.to_datetime(trips['Date']).dt.year
    r1 = {}
    for y, n in sorted(collections.Counter(yrs).items()):
        r1['year_' + str(y)] = int(n)
    code = {'LTG': 'lightning', 'CONTAM': 'fog', 'TREE': 'growin', 'WIND': 'fallin', 'VEH': 'vehicle',
            'EQUIP': 'hardware', 'BIRD': 'bird', 'UNK': 'unknown'}
    t26 = trips[yrs == 2026]
    c = collections.Counter(code.get(x, 'unknown') for x in t26['Cause'])
    for k in G_CAUSES:
        r1['2026_' + k] = int(c.get(k, 0))
    import sqlite3
    con = sqlite3.connect(os.path.join(target, C.FILES['oms']))
    los = pd.read_sql("select * from outage where cause_code='LOS'", con)
    con.close()
    los = los[pd.to_datetime(los['start_time']).dt.year == 2026]
    mins = (pd.to_datetime(los['restore_time']) - pd.to_datetime(los['start_time'])).dt.total_seconds() / 60.0
    r6 = {'sustained': int(los['members_out'].sum()), 'member_minutes': int(round((los['members_out'] * mins).sum())), 'momentary': 0}
    return dict(R1=r1, R6=r6)


def _run(target, opts, d):
    return G.run(target, opts, d=d)


def build(target, out_path):
    d = G.load(target)
    gold_r = _run(target, G.GOLD, d)
    gold_open = [place_tuple(rl) for rl in gold_r['repeat'] if not rl['fixed']]
    gold = results_of(gold_r, gold_open)
    care_r = _run(target, dict(G.GOLD, **HURRY), d)
    care = results_of(care_r, gold_open)
    q = quick(target)

    keys = ('R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'R9', 'R10')
    routes = {}
    fact = []
    r1b = {}
    for k, v in gold['R1'].items():
        if k.startswith('year_'):
            r1b[k] = [v - 1, v + 1]
        else:
            r1b[k] = [max(0, v - 2), v + 2]
    r6b = {k: [int(v * 0.98), int(v * 1.02) + 1] for k, v in gold['R6'].items()}

    def matches(k, val):
        if k == 'R1':
            return all(r1b[c][0] <= val.get(c, -999) <= r1b[c][1] for c in gold['R1'])
        if k == 'R6':
            return all(r6b[c][0] <= val.get(c, -999) <= r6b[c][1] for c in gold['R6'])
        return val == gold[k]

    for sid, name, ks, prec in STUMPS:
        drop = results_of(_run(target, dict(G.GOLD, **{k: HURRY[k] for k in ks}), d), gold_open)
        alone = results_of(_run(target, dict(G.GOLD, **dict(HURRY, **{k: G.GOLD[k] for k in ks})), d), gold_open)
        moved = [k for k in keys if not matches(k, drop[k])]
        rescued = [k for k in keys if matches(k, alone[k]) and not matches(k, care[k])]
        fact.append(dict(id=sid, name=name, kind='stump', precedent=prec,
                         dropped=dict(answer=drop['R10'], results_moved=moved),
                         alone=dict(answer=alone['R10'], results_rescued=rescued)))
        routes[sid] = (drop, alone)
    for xid, name, prec in REFLEXES:
        fact.append(dict(id=xid, name=name, kind='reflex', precedent=prec))

    fam, fam_ceff = [], []
    for name, v in VARIANTS.items():
        run_v = _run(target, dict(G.GOLD, **v), d)
        rr = results_of(run_v, gold_open)
        fam.append(dict(name=name, answer=rr['R10'], level=round(run_v['deposits']['level'], 4),
                        beta=round(run_v['deposits']['beta'], 3),
                        ratio_W5=round(run_v['deposits']['sections']['L02-W5']['ratio'], 3),
                        ratio_W1=round(run_v['deposits']['sections']['L02-W1']['ratio'], 3)))
        fam_ceff.append(rr['ceff'])

    pert = []
    for name, v in PERTURB.items():
        rr = results_of(_run(target, dict(G.GOLD, **v), d), gold_open)
        pert.append(dict(input=name, answer=rr['R10']))

    shortcuts = [dict(name='the reflex route (every stump hurried)', answer=care['R10'])]
    for sid, (drop, _) in routes.items():
        shortcuts.append(dict(name='the golden with %s hurried' % sid, answer=drop['R10']))
    direct_r = _run(target, dict(G.GOLD, loc='dist', contacts='signature', tap_infeed='none',
                                 dc_mutual='uncoupled', deposit='latest', topology='oms_direct'), d)
    direct = results_of(direct_r, gold_open)
    shortcuts.append(dict(name='the direct route (raw relay distances, raw OMS, latest test readings)', answer=direct['R10']))
    for name, v in SHORTCUTS.items():
        rr = results_of(_run(target, dict(G.GOLD, **v), d), gold_open)
        shortcuts.append(dict(name=name, answer=rr['R10']))

    ceff_bands = {
        k: [round(min([gold['ceff'][k]] + [x[k] for x in fam_ceff]), 4),
            round(max([gold['ceff'][k]] + [x[k] for x in fam_ceff]), 4)]
        for k in gold['ceff']
    }

    hints = []
    for sid, name, ks, prec in STUMPS:
        alone = routes[sid][1]
        hints.append(dict(sentence=name, rescues=[k for k in keys if matches(k, alone[k]) and not matches(k, care[k])]))

    def grade_tab(val, gold_v, bands, pshare=0.5):
        ok = sum(1 for k in gold_v if bands[k][0] <= val.get(k, -999) <= bands[k][1])
        return 'right' if ok == len(gold_v) else ('partly' if ok / max(1, len(gold_v)) >= pshare else 'missed')

    res = [
        dict(id='R1', name='conformed 2022-2026 faults by year and 2026 faults by cause', graded_as='Ask 1',
             figure='faults_summary_conformed', depends=[], independent='', golden=gold['R1'], bands=r1b,
             partly_share=0.55,
             passes=dict(
                 quick=q['R1'],
                 careful=care['R1'],
                 thorough=gold['R1'],
             ),
             precedent=['L47', 'L26']),
        dict(id='R2', name='active 12.47 kV underbuild clearance spans (Line 6 str 57-58 and Line 15 str 48-49)',
             graded_as='Component 1', figure='clearance_items', depends=['R1'],
             independent='IEEE 738 conductor temperature trajectory on summer contacts against vegetation trims',
             golden=gold['R2'], passes=dict(quick=[], careful=care['R2'], thorough=gold['R2']),
             precedent=['L47', 'L26']),
        dict(id='R3', name='active cracked insulator strings downstream of YNd1 IPP taps (Line 8 str 93 and Line 9 str 137)',
             graded_as='Component 2', figure='ipp_strings', depends=['R1'],
             independent='single-ended relay distances and both IPP protection exports',
             golden=gold['R3'], passes=dict(quick=[], careful=care['R3'], thorough=gold['R3']),
             precedent=['L63', 'N21']),
        dict(id='R4', name='active double-circuit corridor repeats on Lines 10 and 11 (Line 10 str 68-69 and Line 11 str 71)',
             graded_as='Component 3', figure='dc_corridor_repeats', depends=['R1'],
             independent='two-ended zero-sequence currents and protection study mutual impedance Z0m',
             golden=gold['R4'], passes=dict(quick=[], careful=care['R4'], thorough=gold['R4']),
             precedent=['L58', 'L48']),
        dict(id='R5', name='nine coastal washing sections due before 1 December 2026 under joint (ESDD, NSDD)',
             graded_as='Component 4', figure='wash_due', depends=[],
             independent='test insulator ESDD/NSDD monitoring, directional winds, rain and washing log',
             golden=gold['R5'], passes=dict(quick=[], careful=care['R5'], thorough=gold['R5']),
             precedent=['L38', 'L42', 'L15']),
        dict(id='R6', name='2026 conformed member interruptions and member-minutes under as-operated SCADA topology',
             graded_as='Component 5', figure='member_impact_2026', depends=['R1'],
             independent='SCADA SOE supervisory switching windows, breaker operations and monthly members',
             golden=gold['R6'], bands=r6b,
             passes=dict(quick=q['R6'], careful=care['R6'], thorough=gold['R6']),
             precedent=['N09', 'L55']),
        dict(id='R7', name='Priority 1 work-type crew-day mix and network-corridor repeat structures',
             graded_as='Ask 2', figure='p1_mix_and_corridor', depends=['R2', 'R3', 'R4', 'R5', 'R6'],
             independent='', golden=gold['R7'],
             passes=dict(quick=[], careful=care['R7'], thorough=gold['R7']),
             precedent=['L47', 'L63', 'L58', 'L38', 'N09']),
        dict(id='R8', name='ranked open repeat register (19 open repeats with current structure, cause, fix, priority)',
             graded_as='Ask 3', figure='ranked_open_register', depends=['R2', 'R3', 'R4', 'R5', 'R6'],
             independent='', golden=gold['R8'],
             passes=dict(quick=[], careful=care['R8'], thorough=gold['R8']),
             precedent=['L47', 'L63', 'L58', 'L38', 'N09']),
        dict(id='R9', name='Priority 1 funded repeat slate (13 repeats, 27 crew-days)',
             graded_as='Ask 4', figure='p1_repeat_slate', depends=['R2', 'R3', 'R4', 'R5', 'R6'],
             independent='', golden=gold['R9'],
             passes=dict(quick=[], careful=care['R9'], thorough=gold['R9']),
             precedent=['L47', 'L63', 'L58', 'L38', 'N09']),
        dict(id='R10', name='RP-04 Rev 5 36-crew-day Priority 1 winter and spring work program (9 washes + 13 repeats)',
             graded_as='Recommendation', figure='work_list', depends=['R2', 'R3', 'R4', 'R5', 'R6'],
             independent='', golden=gold['R10'],
             passes=dict(quick=[], careful=care['R10'], thorough=gold['R10']),
             precedent=['L47', 'L63', 'L58', 'L38', 'N09']),
    ]

    out = dict(
        results=res, hints=hints,
        routes=[dict(name='the golden', answer=gold['R10'], golden=True)] + shortcuts,
        weights=dict(recommendation=14, components=34, asks=45, instruction=7),
        forcing=dict(kind='set', golden_family=fam, shortcuts=shortcuts, perturbations=pert),
        factorial=dict(golden_answer=gold['R10'], reflex_route=dict(answer=care['R10']), judgments=fact),
        direct_route=dict(answer=direct['R10']),
    )
    json.dump(out, open(out_path, 'w'), indent=1, default=str)
    write_figures(target, d, gold_r, gold, care_r, care, direct_r, direct, q, fam, ceff_bands, gold_open)
    return gold_r, gold, care, q


def write_figures(target, d, gold_r, gold, care_r, care, direct_r, direct, q, fam, ceff_bands, gold_open):
    """Emit every figure stated in submission.md and the golden deliverables into generator/figures.json."""
    dep = gold_r['deposits']
    imp = gold_r['impact']
    fs = gold_r['faults']
    prog = gold_r['programme']

    lines26 = {
        lname(k): dict(sustained=int(v['sustained']), member_minutes=int(round(v['minutes'])), momentary=int(v['momentary']))
        for k, v in sorted(imp.items(), key=lambda kv: int(kv[0][1:]))
    }
    by_line_year = collections.defaultdict(dict)
    for (lid, yr), n in sorted(collections.Counter((f['line'], C.to_local(f['t']).year) for f in fs).items()):
        by_line_year[lname(lid)][str(yr)] = n

    # Repeat location detail table (open + fixed)
    rl_detail = []
    for rl in sorted(gold_r['repeat'], key=lambda x: (x['fixed'], -round(x.get('mm_per_day', 0.0), 2), int(x['line'][1:]), x['structure'])):
        rl_detail.append(dict(
            line=lname(rl['line']), line_id=rl['line'], cause=rl['cause'],
            structure=int(rl['structure']), s_min=int(rl['s_min']), s_max=int(rl['s_max']),
            span=list(rl['span']) if rl.get('span') else None,
            km=round(float(rl['km']), 2),
            faults=int(rl['n']),
            first=C.to_local(rl['first']).date().isoformat(),
            last=C.to_local(rl['last']).date().isoformat(),
            fixed=bool(rl['fixed']),
            crew_days=int(rl.get('crew_days', C.CREW_DAYS.get(rl['cause'], 0))),
            hist_mm=int(round(rl.get('hist_mm', 0.0))),
            mm_per_day=int(round(rl.get('mm_per_day', 0.0))),
            priority=rl.get('priority', 'Fixed' if rl['fixed'] else 'P2'),
            label=snap_rep(rl, gold_open),
        ))

    # S1: clearance contact details + grow-in slopes (including underbuilt decoys)
    clearance_details = []
    for c in sorted(gold_r['contacts'], key=lambda x: int(x['line'][1:])):
        clearance_details.append(dict(
            line=lname(c['line']), structures='%d-%d' % (c['s_min'], c['s_max']),
            contacts_since_trim=int(c['n']), trim=c['trim'].isoformat() if c['trim'] else None,
            slope_c_per_year=round(float(c['slope']), 2),
            contact_temperature=[round(min(c['tc']), 1), round(max(c['tc']), 1)],
        ))
    veg_slopes = {}
    ub_veg_slopes = {}
    vv = d['veg']
    st_df = d['structures']
    ub_mask = st_df['underbuild'].fillna('').astype(str).str.strip().str.len() > 0
    st_ub = set(zip(st_df.loc[ub_mask, 'line'], st_df.loc[ub_mask, 'structure_no'].astype(int)))
    for rl in gold_r['repeat']:
        if rl['cause'] != 'growin' or rl['fixed']:
            continue
        ln = lname(rl['line'])
        last_c = max(C.to_local(f['t']).date() for f in rl['faults'])
        tr = [pd.Timestamp(x.completed).date() for x in vv[(vv['line'] == ln) & vv['work_type'].isin(['HOT SPOT', 'CYCLE TRIM'])].itertuples()
              if int(x.from_structure) <= rl['s_max'] + 1 and rl['s_min'] - 1 <= int(x.to_structure) and pd.Timestamp(x.completed).date() <= last_c]
        t_trim = max(tr) if tr else None
        after = [f for f in rl['faults'] if isinstance(f.get('sig'), dict) and f['sig'].get('tc') and (t_trim is None or C.to_local(f['t']).date() > t_trim)]
        xs = [C.to_local(f['t']).year + C.to_local(f['t']).timetuple().tm_yday / 365.25 for f in after]
        ys = [f['sig']['tc'] for f in after]
        if len(xs) >= 3 and len(set(int(x) for x in xs)) >= 2:
            slp = round(float(np.polyfit(xs, ys, 1)[0]), 2)
            key_s = '%s str %d-%d' % (ln, rl['s_min'], rl['s_max'])
            veg_slopes[key_s] = slp
            if any((ln, s) in st_ub for s in range(rl['s_min'], rl['s_max'] + 1)):
                ub_veg_slopes[key_s] = slp

    # S2: dual YNd1 IPP tap location comparison (golden vs raw no-infeed vs over)
    no_inf = _run(target, dict(G.GOLD, tap_infeed='none'), d)
    ipp_details = {}
    for lid in ('L08', 'L09'):
        gr = next((r for r in gold_r['repeat'] if not r['fixed'] and r['line'] == lid and r['cause'] == 'insulator'), None)
        nr = next((r for r in no_inf['repeat'] if not r['fixed'] and r['line'] == lid and r['cause'] == 'insulator'), None)
        if gr and nr:
            tk = d['ipp_taps'][lid]['tap_km']
            ipp_details[lname(lid)] = dict(
                facility=d['ipp_taps'][lid]['facility'],
                tap_km=round(tk, 2),
                golden_km=round(float(gr['km']), 2), golden_structure=int(gr['structure']),
                beyond_tap_km=round(float(gr['km']) - tk, 2),
                raw_km=round(float(nr['km']), 2), raw_structure=int(nr['structure']),
                structure_shift=int(nr['structure']) - int(gr['structure']),
            )

    # S3: double-circuit Z0m coupled vs uncoupled location comparison & referee metrics
    unc_r = _run(target, dict(G.GOLD, dc_mutual='uncoupled'), d)
    dc_details = {}
    for gr in sorted([r for r in gold_r['repeat'] if not r['fixed'] and r['line'] in ('L10', 'L11')],
                     key=lambda x: (int(x['line'][1:]), x['structure'])):
        ur = min([r for r in unc_r['repeat'] if not r['fixed'] and r['line'] == gr['line'] and r['cause'] == gr['cause']],
                 key=lambda x: abs(x['km'] - gr['km']), default=None)
        if ur:
            row_dc = dict(
                line=lname(gr['line']), cause=gr['cause'],
                golden_km=round(float(gr['km']), 2), golden_structure=int(gr['structure']),
                golden_span=list(gr['span']) if gr.get('span') else None,
                uncoupled_km=round(float(ur['km']), 2), uncoupled_structure=int(ur['structure']),
                uncoupled_span=list(ur['span']) if ur.get('span') else None,
                structure_shift=int(gr['structure']) - int(ur['structure']),
            )
            dc_details['%s str %d %s' % (lname(gr['line']), gr['structure'], gr['cause'])] = row_dc
    dc_corridor_details = {
        'Line 11 insulator': next(v for v in dc_details.values() if v['line'] == 'Line 11' and v['cause'] == 'insulator'),
        'Line 10 growin': next(v for v in dc_details.values() if v['line'] == 'Line 10' and v['cause'] == 'growin' and v['golden_structure'] < 85),
    }
    import core as CORE
    import sim
    dc_ref = CORE.referee_metrics(d, sim.world(), gold_r, unc_r, direct_r)

    # S4: joint (ESDD, NSDD) section details vs ESDD-only shortcut
    lv = dep['level']
    esdd_only_r = _run(target, dict(G.GOLD, deposit='esdd_wind'), d)
    esdd_only_due = sorted(wash_label(k).replace('wash: ', '') for k in esdd_only_r['programme']['due_washes'])
    secs = {
        wash_label(k).replace('wash: ', ''): dict(
            esdd=round(v['esdd'], 4), nsdd=round(v['nsdd'], 4), ceff=round(v['ceff'], 4),
            ratio=round(v['ratio'], 2), surface=v['surface'], gulf_km=round(v['dist'], 2),
            due=bool(v['due']), last_wash=v['last_wash'].isoformat() if v['last_wash'] else None,
            esdd_only_due=bool(esdd_only_r['deposits']['sections'][k]['due']),
        )
        for k, v in sorted(dep['sections'].items())
    }
    levels = [lv] + [v['level'] for v in fam]
    betas = [dep['beta']] + [v['beta'] for v in fam]

    # S5: chronological SCADA switching topology vs static / over_both / oms_direct
    st_r = _run(target, dict(G.GOLD, topology='static'), d)
    ob_r = _run(target, dict(G.GOLD, topology='over_both'), d)
    oms_r = _run(target, dict(G.GOLD, topology='oms_direct'), d)
    wins = G.parse_switching_windows(d)
    st_26 = impact_table(st_r['impact'])
    ob_26 = impact_table(ob_r['impact'])
    oms_26 = impact_table(oms_r['impact'])
    live_26 = gold['R6']

    mix_dict = collections.Counter()
    for rl in prog['funded']:
        mix_dict[rl['cause']] += rl['crew_days']
    mix_dict['wash'] = prog['wash_days']

    fig = dict(
        faults_summary_conformed=gold['R1'],
        faults_by_year=gold['by_year'],
        faults_total=sum(gold['by_year'].values()),
        faults_2026=gold['by_year'].get('2026'),
        faults_lockouts_total=sum(1 for f in fs if f['locked']),
        faults_lockouts_2026=sum(1 for f in fs if f['locked'] and C.to_local(f['t']).year == 2026),
        faults_by_line_year=dict(by_line_year),
        faults_2026_by_cause=gold['by_cause_2026'],
        # CC1 - S1
        clearance_items=gold['R2'],
        clearance_details=clearance_details,
        vegetation_slopes=veg_slopes,
        vegetation_slope_range=[min(veg_slopes.values()), max(veg_slopes.values())] if veg_slopes else None,
        underbuilt_veg_slopes=ub_veg_slopes,
        underbuilt_veg_slope_range=[min(ub_veg_slopes.values()), max(ub_veg_slopes.values())] if ub_veg_slopes else None,
        underbuilt_veg_slope_abs=[round(abs(v), 2) for v in sorted(ub_veg_slopes.values(), reverse=True)] if ub_veg_slopes else None,
        # CC2 - S2
        ipp_strings=gold['R3'],
        ipp_details=ipp_details,
        # CC3 - S3
        dc_corridor_repeats=gold['R4'],
        dc_corridor_details=dc_corridor_details,
        dc_details=dc_details,
        dc_referee=dc_ref,
        dc_referee_ratio=round(dc_ref['rivals']['rigorous'] / max(1e-6, dc_ref['golden']), 1),
        # CC4 - S4
        wash_due=gold['R5'],
        wash_due_count=len(gold['R5']),
        wash_not_due_count=len(secs) - len(gold['R5']),
        wash_due_min_ratio=min(v['ratio'] for v in secs.values() if v['due']),
        wash_clean_max_ratio=max(v['ratio'] for v in secs.values() if not v['due']),
        wash_sections=secs,
        wash_ceff=gold['ceff'],
        wash_ceff_bands=ceff_bands,
        flashover_level=round(lv, 4),
        flashover_level_band=[round(min(levels), 4), round(max(levels), 4)],
        beta_nsdd=round(dep['beta'], 3),
        beta_nsdd_band=[round(min(betas), 3), round(max(betas), 3)],
        k_esdd=round(dep['k_esdd'], 4),
        k_nsdd=round(dep['k_nsdd'], 4),
        esdd_only_due_count=len(esdd_only_due),
        esdd_only_extra=sorted(set(esdd_only_due) - {x.replace('wash: ', '') for x in gold['R5']}),
        # CC5 - S5
        member_impact_2026=live_26,
        member_impact_2026_band={k: [int(v * 0.98), int(v * 1.02) + 1] for k, v in live_26.items()},
        member_impact_2026_by_line=lines26,
        member_impact_2026_static=st_26,
        member_impact_2026_over_both=ob_26,
        member_impact_2026_oms=oms_26,
        static_2026_pct_diff=round(100.0 * (st_26['member_minutes'] / max(1, live_26['member_minutes']) - 1.0), 1),
        static_2026_pct_diff_abs=round(abs(100.0 * (st_26['member_minutes'] / max(1, live_26['member_minutes']) - 1.0)), 1),
        over_both_2026_pct_diff=round(100.0 * (ob_26['member_minutes'] / max(1, live_26['member_minutes']) - 1.0), 1),
        switching_windows_count=len(wins),
        switching_windows_2026_count=sum(1 for w_ in wins if w_['end'].year >= 2026),
        # Repeat register & RP-04 Rev 5 Priority 1 / Priority 2 Programme
        repeat_locations=rl_detail,
        open_repeats_count=len(prog['ranked']),
        fixed_repeats_count=sum(1 for r in gold_r['repeat'] if r['fixed']),
        p1_mix_and_corridor=gold['R7'],
        ranked_open_register=gold['R8'],
        p1_repeat_slate=gold['R9'],
        p2_deferred_backlog=gold['p2'],
        work_list=gold['R10'],
        programme=dict(
            budget_days=int(prog['budget']),
            wash_days=int(prog['wash_days']),
            repeat_budget=int(prog['repeat_budget']),
            repeat_days_used=int(prog['repeat_days_used']),
            unused_days=int(prog['unused_days']),
            funded_count=len(prog['funded']),
            deferred_count=len(prog['deferred']),
            cutoff_mm_per_day=int(round(prog['cutoff_mm_per_day'])),
            first_deferred_mm_per_day=int(round(prog['first_deferred_mm_per_day'])),
            crew_day_mix=dict(sorted(mix_dict.items())),
        ),
        # Rival / shortcut comparison
        careful=dict(
            work_list=care['R10'], R2=care['R2'], R3=care['R3'], R4=care['R4'], R5=care['R5'], R6=care['R6'],
            p1_repeat_slate=care['R9'], wash_due_count=len(care['R5']),
        ),
        direct=dict(work_list=direct['R10'], R6=direct['R6']),
        quick=q,
        family_size=len(fam),
        filed=dict(
            system_kv=69, repeat_location_m=400, underbuild_kv=12.47,
            crew_budget_days=int(prog['budget']), dc_corridor_km=14.5,
            sequence_window_s=60, ieee_standard=738,
            z0m_ohm_per_km=round(abs(d['studies'][2025]['DC_Z0M']), 3),
            z0m_r_ohm_per_km=round(float(d['studies'][2025]['DC_Z0M'].real), 4),
            z0m_x_ohm_per_km=round(float(d['studies'][2025]['DC_Z0M'].imag), 4),
        ),
    )
    json.dump(fig, open(os.path.join(C.HERE, 'figures.json'), 'w'), indent=1, default=str)
    return fig


if __name__ == '__main__':
    gold_r, gold, care, q = build(C.TARGET, os.path.join(C.HERE, 'effort.json'))
    print('effort.json + figures.json written; P1 items:', len(gold['R10']), 'careful items:', len(care['R10']))
