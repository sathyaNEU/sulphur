"""The golden deliverables for task13 (architecture 7, Level 5), from target/ alone through the golden route:
  1. lpec_69kv_faults_2022-2026.csv (conformed fault table, one row per 69 kV fault since January 2022)
  2. lpec_69kv_fault_review_2026.xlsx (annual faults, 2026 causes, 2026 as-operated member impact, repeat locations,
     joint ESDD/NSDD coastal washing sections, Priority 1 36-crew-day program & Priority 2 backlog, diagnostics, shortcuts)
  3. 69kv_work_list_winter_2026-27.docx (one-page memo to Charles Ortiz, Manager of Engineering)"""
import collections
import csv
import datetime as dt
import json
import os
import shutil

import common as C
import golden as G
import office as O
import passes as PS

CAUSE_NAME = {
    'lightning': 'lightning', 'bird': 'bird or other animal', 'fog': 'salt contamination',
    'insulator': 'insulator failure', 'growin': 'vegetation grown into the line',
    'fallin': 'vegetation from outside the right of way', 'vehicle': 'vehicle or other third party',
    'hardware': 'equipment or hardware other than insulators', 'unknown': 'other or unknown',
}
FIX = {
    'bird': 'perch guards and streamer shields',
    'insulator': 'replace the string',
    'growin': 'clear the span',
    'fallin': 'remove the hazard trees',
    'hardware': 'restore clearance to 12.47 kV underbuild (re-sag span)',
}
BY_WHEN = {
    'bird': '15 December 2026', 'insulator': '31 December 2026', 'fallin': '31 March 2027',
    'growin': '1 May 2027', 'hardware': '1 May 2027', 'wash': '1 December 2026',
}


def build_golden(target, golden, w=None):
    if os.path.exists(golden):
        shutil.rmtree(golden)
    os.makedirs(golden)
    r = G.run(target, G.GOLD)
    d = r['d']
    fig = json.load(open(os.path.join(C.HERE, 'figures.json')))
    rep_id = {}
    reps = sorted(r['repeat'], key=lambda x: (x['fixed'], -round(x.get('mm_per_day', 0.0), 2), int(x['line'][1:]), x['s_min']))
    for i, rl in enumerate(reps):
        rl['rid'] = 'RL-%02d' % (i + 1)
        for f in rl['faults']:
            rep_id[id(f)] = rl['rid']
    write_csv(r, d, rep_id, os.path.join(golden, C.DELIVERABLES[0]))
    write_xlsx(r, d, reps, fig, os.path.join(golden, C.DELIVERABLES[1]))
    write_memo(r, fig, os.path.join(golden, C.DELIVERABLES[2]))
    import postprocess as PP
    PP.own_mtimes(golden, {C.DELIVERABLES[0]: C.local(C.GOLD_STAMP['csv'][1])})
    return r


def _locked(f):
    return bool(f.get('locked')) or any(x.get('state') == 'LOCKOUT' for x in f.get('soe', []))


def write_csv(r, d, rep_id, path):
    with open(path, 'w', newline='') as fh:
        wr = csv.writer(fh)
        wr.writerow(['fault_id', 'date', 'time', 'line', 'terminal_a', 'terminal_b', 'km_from_terminal_a', 'structure',
                     'span', 'fault_type', 'cause', 'cleared_on_reclose', 'members_interrupted', 'member_minutes',
                     'members_momentary', 'repeat_location'])
        for i, f in enumerate(sorted(r['faults'], key=lambda f: f['t'])):
            L = d['lines'][f['line']]
            lt = C.to_local(f['t'])
            imp = f.get('impact') or dict(sustained=0, minutes=0.0, momentary=0)
            span = '%d-%d' % f['span'] if (f['cause'] in ('growin', 'fallin', 'hardware') and f.get('span')) else ''
            wr.writerow([
                'F%04d' % (i + 1), lt.strftime('%Y-%m-%d'), lt.strftime('%H:%M:%S'), PS.lname(f['line']),
                d['stations'][L['a']]['name'], d['stations'][L['b']]['name'],
                '' if f['km'] is None else '%.2f' % f['km'], '' if f['structure'] is None else f['structure'], span,
                f.get('type') or '', CAUSE_NAME[f['cause']], 'no' if _locked(f) else 'yes',
                int(imp['sustained']), int(round(imp['minutes'])), int(imp['momentary']), rep_id.get(id(f), ''),
            ])


def _place_str(rl):
    if rl['cause'] in ('growin', 'hardware') and rl.get('span'):
        return '%d-%d' % tuple(rl['span'])
    if rl['cause'] == 'fallin':
        return '%d-%d' % (rl['s_min'], rl['s_max'])
    return str(rl['structure'])


NOTES = [
    ['Item', 'Note'],
    ['As of', '31 October 2026; in this November report the year 2026 runs from 1 January to 31 October (RP-04 Rev 5).'],
    ['Fault', 'One protection operation sequence on one 69 kV line within 60 s; switching, testing, maintenance, and non-tripping mutual pickups are not faults (RP-04 Rev 5).'],
    ['Location', 'Current structure inventory numbering (Lines 8 and 13 renumbered after 2023 rebuilds). Two-ended ground faults use zero-sequence current split with protection study sources in force on the fault date; Lines 10 and 11 invert the coupled 2-line mutual impedance Z0m along the 14.5 km Inland double-circuit corridor; Lines 8 and 9 invert YNd1 IPP ground infeed from Brushy Creek BESS and Coyote Draw Solar exports.'],
    ['Member impact', 'Members out >5 minutes from fault initiation to substation restoration, attributed to the 69 kV line energizing that substation at the time of the fault by replaying chronological SCADA ALT SRC / NORM SW switching windows (RP-04 Rev 5).'],
    ['Repeat location', 'Three or more faults of one cause on one line within 400 m since 1 January 2022; salt contamination is section-managed through washing (RP-04 Rev 5).'],
    ['Coastal washing', 'Daily two-state model carrying soluble sea salt (ESDD, onshore wind, fast rain washout) and non-soluble dust (NSDD, dry inland wind, slow rain washout) from each wash; 2D fog-flashover frontier C_eff = ESDD * (NSDD/0.20)^beta fitted empirically over coastal fog nights against the 10th-percentile flashover level.'],
    ['Priority 1 program', 'Fixed 36-crew-day winter/spring allowance: all due coastal washing sections scheduled first (1 crew-day each), remaining crew-days allocated greedily to open repeats by historical 2022-2026 conformed member-minutes per crew-day; remaining open items defer to Priority 2 (RP-04 Rev 5).'],
    ['Times', 'Central prevailing time throughout; relay clocks aligned to SCADA UTC, both IPP exports read on Central Standard Time all year.'],
]


def write_xlsx(r, d, reps, fig, path):
    years = ['2022', '2023', '2024', '2025', '2026']
    lids = sorted(d['lines'], key=lambda x: int(x[1:]))

    # Sheet 1: Faults by line and year
    s1 = [['Line', 'Name'] + [y if y != '2026' else '2026 (Jan-Oct)' for y in years] + ['Total']]
    tot = collections.Counter()
    for lid in lids:
        row = fig['faults_by_line_year'].get(PS.lname(lid), {})
        vals = [int(row.get(y, 0)) for y in years]
        for y, v in zip(years, vals):
            tot[y] += v
        s1.append([PS.lname(lid), '%s-%s' % (d['lines'][lid]['a_name'], d['lines'][lid]['b_name'])] + vals + [sum(vals)])
    s1.append(['All lines', ''] + [tot[y] for y in years] + [sum(tot.values())])

    # Sheet 2: 2026 by cause
    c26 = collections.Counter((f['cause'], f['line']) for f in r['faults'] if C.to_local(f['t']).year == 2026)
    s2 = [['Cause'] + ['L%d' % int(l[1:]) for l in lids] + ['All lines']]
    for c in PS.G_CAUSES:
        vals = [c26.get((c, l), 0) for l in lids]
        s2.append([CAUSE_NAME[c]] + vals + [sum(vals)])
    s2.append(['All causes'] + [sum(c26.get((c, l), 0) for c in PS.G_CAUSES) for l in lids] + [sum(c26.values())])

    # Sheet 3: 2026 member impact (as-operated SCADA topology)
    s3 = [['Line', 'Member interruptions (>5 min)', 'Member-minutes', 'Momentary member events']]
    for lid in lids:
        v = fig['member_impact_2026_by_line'].get(PS.lname(lid), dict(sustained=0, member_minutes=0, momentary=0))
        s3.append([PS.lname(lid), v['sustained'], v['member_minutes'], v['momentary']])
    t = fig['member_impact_2026']
    s3.append(['All lines', t['sustained'], t['member_minutes'], t['momentary']])

    # Sheet 4: Repeat locations (all 27 open + fixed, ranked)
    s4 = [['Ref', 'Line', 'Structures', 'Cause', 'Faults', 'First', 'Last', 'Crew-days',
           '2022-26 Member-minutes', 'MM / crew-day', 'Fix', 'Status']]
    for rl in reps:
        status = 'Fixed after last fault' if rl['fixed'] else ('Priority 1 (funded)' if rl.get('priority') == 'P1' else 'Priority 2 (deferred)')
        cd = int(rl.get('crew_days', C.CREW_DAYS.get(rl['cause'], 0)))
        hmm = int(round(rl.get('hist_mm', 0.0)))
        mmd = int(round(rl.get('mm_per_day', 0.0)))
        s4.append([
            rl['rid'], PS.lname(rl['line']), _place_str(rl), CAUSE_NAME[rl['cause']], rl['n'],
            C.to_local(rl['first']).date(), C.to_local(rl['last']).date(),
            0 if rl['fixed'] else cd, hmm, 0 if rl['fixed'] else mmd, FIX[rl['cause']], status,
        ])

    # Sheet 5: Coastal washing sections (joint ESDD, NSDD)
    s5 = [['Section', 'Structures', 'Corridor surface', 'Gulf shore (km)', 'Last washed',
           '31 Oct ESDD (mg/cm2)', '31 Oct NSDD (mg/cm2)', 'Effective C_eff (mg/cm2)',
           'Times flashover level', 'Due before 1 Dec']]
    lv = r['deposits']['level']
    for _, row in d['wash_sections'].iterrows():
        lid = 'L%02d' % int(str(row['Line']).split()[1])
        sid = '%s-W%s' % (lid, str(row['Section']).split()[-1])
        v = r['deposits']['sections'][sid]
        s5.append([
            '%s, %s' % (row['Line'], row['Section']), '%d-%d' % (int(row['From structure']), int(row['To structure'])),
            v['surface'], round(v['dist'], 2), v['last_wash'],
            round(v['esdd'], 4), round(v['nsdd'], 4), round(v['ceff'], 4), round(v['ratio'], 2),
            'yes' if v['due'] else 'no',
        ])
    s5.append(['Flashover level (10th pct of fog flashovers, fitted beta=%.3f)' % fig['beta_nsdd'],
               '', '', '', '', '', '', round(lv, 4), 1.0, ''])

    # Sheet 6: Priority 1 (36 crew-days) & Priority 2 backlog
    s6 = [['Priority', 'Order', 'Work', 'Line', 'Structures / Section', 'Cause', 'Crew-days', 'MM / crew-day', 'Target date']]
    k = 0
    for _, row in d['wash_sections'].iterrows():
        lid = 'L%02d' % int(str(row['Line']).split()[1])
        sid = '%s-W%s' % (lid, str(row['Section']).split()[-1])
        if r['deposits']['sections'][sid]['due']:
            k += 1
            s6.append([
                'Priority 1', k, 'wash porcelain insulators', str(row['Line']),
                '%d-%d (%s)' % (int(row['From structure']), int(row['To structure']), row['Section']),
                CAUSE_NAME['fog'], C.CREW_DAYS['wash'], '', BY_WHEN['wash'],
            ])
    prog = r['programme']
    for rl in prog['funded']:
        k += 1
        s6.append([
            'Priority 1', k, FIX[rl['cause']], PS.lname(rl['line']), _place_str(rl),
            CAUSE_NAME[rl['cause']], int(rl['crew_days']), int(round(rl['mm_per_day'])), BY_WHEN[rl['cause']],
        ])
    s6.append(['Priority 1 total', '', '%d washes + %d repeats' % (len(prog['due_washes']), len(prog['funded'])),
               '', '', '', int(prog['wash_days'] + prog['repeat_days_used']), int(round(prog['cutoff_mm_per_day'])), ''])
    for j, rl in enumerate(prog['deferred'], 1):
        s6.append([
            'Priority 2 (deferred)', j, FIX[rl['cause']], PS.lname(rl['line']), _place_str(rl),
            CAUSE_NAME[rl['cause']], int(rl['crew_days']), int(round(rl['mm_per_day'])), 'Post-spring backlog',
        ])

    # Sheet 7: Summer contacts (S1 thermal sag trajectories)
    s7 = [['Line', 'Span', 'Underbuild', 'Date', 'Time', 'Line current (A)', 'Air (C)', 'Wind (m/s)',
           'Conductor (C)', 'Last trim before', 'Booked as']]
    vv = d['veg']
    for f in sorted([f for f in r['faults'] if f['cause'] in ('growin', 'hardware') and f.get('span') and
                     isinstance(f.get('sig'), dict) and f['sig'].get('tc')],
                    key=lambda f: (int(f['line'][1:]), f['structure'], f['t'])):
        ln = PS.lname(f['line'])
        day = C.to_local(f['t']).date()
        tr = [x for x in vv[(vv['line'] == ln) & vv['work_type'].isin(['HOT SPOT', 'CYCLE TRIM'])].itertuples()
              if int(x.from_structure) <= f['span'][1] and f['span'][0] <= int(x.to_structure)
              and dt.date.fromisoformat(str(x.completed)[:10]) <= day]
        last = max((dt.date.fromisoformat(str(x.completed)[:10]) for x in tr), default=None)
        sg = f['sig']
        s7.append([ln, '%d-%d' % f['span'], 'yes' if sg.get('underbuild') else 'no', day,
                   C.to_local(f['t']).strftime('%H:%M'), sg.get('amps'), sg.get('tair'), sg.get('wind'),
                   round(sg['tc'], 1), last, CAUSE_NAME[f['cause']]])

    # Sheet 8: Network location diagnostics (S2 IPP taps & S3 double-circuit Z0m + referee)
    s8 = [['Mechanism', 'Line & Repeat', 'Golden km', 'Golden structure', 'Naive/uncoupled km',
           'Naive/uncoupled structure', 'Shift (structures)', 'Notes']]
    for ln, info in sorted(fig['ipp_details'].items()):
        s8.append([
            'S2 YNd1 IPP infeed', '%s cracked string (%s)' % (ln, info['facility']),
            info['golden_km'], info['golden_structure'], info['raw_km'], info['raw_structure'],
            info['structure_shift'], 'Tap at %.1f km; %.2f km past tap' % (info['tap_km'], info['beyond_tap_km']),
        ])
    for key, info in sorted(fig['dc_details'].items()):
        s8.append([
            'S3 Double-circuit Z0m', key, info['golden_km'], info['golden_structure'],
            info['uncoupled_km'], info['uncoupled_structure'], info['structure_shift'],
            '14.5 km shared steel-pole corridor out of Inland',
        ])
    ref = fig['dc_referee']
    s8.append(['S3 Patrol referee', ref['slice'], ref['golden'], '', ref['rivals']['rigorous'], '',
               '', 'MAE km: coupled %.3f vs uncoupled %.2f vs direct %.2f' % (ref['golden'], ref['rivals']['rigorous'], ref['rivals']['direct'])])

    # Sheet 9: Shortcuts comparison
    care = fig['careful']
    s9 = [
        ['Shortcut', 'What it changes relative to the RP-04 Rev 5 golden program'],
        ['S1: Book all summer afternoon contacts as grow-ins (ignore post-trim IEEE 738 trajectory)',
         'Misclassifies Line 15 structures 48-49 (and Line 6 57-58) as 2-day grow-ins instead of 3-day underbuild clearance restorations, pulling Line 12 structure 104 into the freed crew-day.'],
        ['S2: Ignore YNd1 ground-fault infeed on Line 8 (BESS) and Line 9 (Solar)',
         'Sends string-replacement crews 11 to 13 structures past the true faults (Line 8 str %d instead of %d; Line 9 str %d instead of %d).'
         % (fig['ipp_details']['Line 8']['raw_structure'], fig['ipp_details']['Line 8']['golden_structure'],
            fig['ipp_details']['Line 9']['raw_structure'], fig['ipp_details']['Line 9']['golden_structure'])],
        ['S3: Locate Lines 10 and 11 with uncoupled two-ended residual ratio (ignore Z0m)',
         'Shifts all five active repeats on Lines 10 and 11 toward Inland by 6 to 9 structures (Line 11 str 71 to 62; Line 10 str 68 to 61); referee MAE rises from %.3f km to %.2f km.'
         % (ref['golden'], ref['rivals']['rigorous'])],
        ['S4: Wash coastal sections on 1D ESDD alone (ignore slow-washing NSDD dust)',
         'Schedules %d washes instead of %d (adding %d marsh/pasture sections), eating 6 extra crew-days and crowding out 3 Priority 1 repeats.'
         % (fig['esdd_only_due_count'], fig['wash_due_count'], len(fig['esdd_only_extra']))],
        ['S5: Attribute member-minutes using static Taps sheet (ignore SCADA ALT SRC/NORM SW windows)',
         'Understates 2026 member-minutes by %.1f percent (%s vs %s) and drops Line 16 structure 23 (from #1 Priority 1 to 0 mm/day) and Line 9 structure 137 out of Priority 1.'
         % (abs(fig['static_2026_pct_diff']), f"{fig['member_impact_2026_static']['member_minutes']:,}", f"{t['member_minutes']:,}")],
        ['All five hurried (reflex route)',
         'Schedules %d washes and misses all five critical components; Priority 1 slate drops %d golden items.'
         % (care['wash_due_count'], len(set(fig['work_list']) - set(care['work_list'])))],
    ]

    O.xlsx(path, [
        ('Faults by line and year', ['69 kV faults by line and year', 'One fault per protection operation sequence on one line (RP-04 Rev 5)'],
         s1, [9, 34, 8, 8, 8, 8, 14, 8], {}),
        ('2026 by cause', ['2026 faults (January to October) by cause and line'], s2, [38] + [5] * 16 + [9], {}),
        ('2026 member impact', ['2026 member interruptions, member-minutes and momentary events under chronological as-operated SCADA topology'],
         s3, [12, 22, 18, 22], {1: '#,##0', 2: '#,##0', 3: '#,##0'}),
        ('Repeat locations', ['All open and fixed repeat locations (3+ same-cause faults within 400 m since 1 January 2022)'],
         s4, [7, 9, 12, 34, 7, 11, 11, 10, 18, 14, 34, 22], {5: 'yyyy-mm-dd', 6: 'yyyy-mm-dd', 8: '#,##0', 9: '#,##0'}),
        ('Washing sections', ['31 October 2026 joint ESDD/NSDD contamination standing across all 21 coastal porcelain sections'],
         s5, [22, 11, 18, 13, 12, 16, 16, 18, 15, 14], {4: 'yyyy-mm-dd', 5: '0.0000', 6: '0.0000', 7: '0.0000', 8: '0.00'}),
        ('Work program', ['RP-04 Rev 5 36-crew-day Priority 1 winter/spring work program and Priority 2 deferred backlog'],
         s6, [20, 6, 36, 9, 20, 34, 10, 14, 18], {7: '#,##0'}),
        ('Summer contacts', ['Summer afternoon contacts: post-trim IEEE 738 conductor temperatures separating underbuild clearance from grow-ins'],
         s7, [8, 9, 10, 11, 6, 13, 8, 9, 12, 13, 38], {3: 'yyyy-mm-dd', 9: 'yyyy-mm-dd'}),
        ('Network locations', ['Dual YNd1 IPP infeed (S2) and coupled double-circuit Z0m (S3) fault location diagnostics'],
         s8, [22, 34, 10, 14, 15, 18, 14, 46], {2: '0.00', 4: '0.00'}),
        ('Shortcuts', ['What quicker readings of the same records would have sent line crews to'], s9, [58, 110], {}),
        ('Notes', ['Definitions and conventions (RP-04 Rev 5)'], NOTES, [20, 120], {}),
    ], 'xlsx', '69 kV fault review 2026', C.PEOPLE['reliability'], table=C.GOLD_STAMP)


def write_memo(r, fig, path):
    prog = r['programme']
    funded = prog['funded']
    deferred = prog['deferred']

    def group_txt(items, cause):
        pts = ['%s str %s' % (PS.lname(x['line']), _place_str(x))
               for x in sorted(items, key=lambda x: (int(x['line'][1:]), x['s_min'])) if x['cause'] == cause]
        return ', '.join(pts)

    by_line = collections.OrderedDict()
    for x in fig['wash_due']:
        ln, sec = x.replace('wash: ', '').split(', Section ')
        by_line.setdefault(ln, []).append(int(sec))

    def secs_txt(v):
        v = sorted(v)
        return ', '.join(str(a) for a in v[:-1]) + ' and ' + str(v[-1]) if len(v) > 1 else str(v[0])

    wash = '; '.join('%s %s %s' % (ln, 'sections' if len(v) > 1 else 'section', secs_txt(v)) for ln, v in by_line.items())
    t = fig['member_impact_2026']
    pr = fig['programme']
    ip8, ip9 = fig['ipp_details']['Line 8'], fig['ipp_details']['Line 9']
    dc11 = fig['dc_corridor_details']['Line 11 insulator']
    c_l15 = next(x for x in fig['clearance_details'] if x['line'] == 'Line 15')
    c_l6 = next(x for x in fig['clearance_details'] if x['line'] == 'Line 6')
    ub_rng = fig['underbuilt_veg_slope_range']
    l12_slp = next(v for k, v in fig['underbuilt_veg_slopes'].items() if k.startswith('Line 12'))
    def_txt = '; '.join('%s str %s (%s, %dd)' % (PS.lname(x['line']), _place_str(x), x['cause'], x['crew_days']) for x in deferred)

    blocks = [
        ('title', 'Memorandum'),
        ('p', 'To: Reliability Review (C. Ortiz, Manager of Engineering; Julie Peterson; Allison Ward)\n'
              'From: Brittany Melton, Reliability Engineer\n'
              'Date: 12 November 2026\n'
              'Subject: Priority 1 69 kV winter and spring work program and Priority 2 backlog (RP-04 Rev 5)'),
        ('p', 'From January through October 2026 the 69 kV system recorded %d faults (%d lockouts), producing %s sustained '
              'member interruptions and %s member-minutes under chronological as-operated SCADA switching topology (versus %s '
              'member-minutes on static feeder assignments). Full 2022-2026 fault conformation (%d faults) and rankings sit in '
              'the accompanying CSV and review workbook.'
              % (fig['faults_2026'], fig['faults_lockouts_2026'], f"{t['sustained']:,}", f"{t['member_minutes']:,}",
                 f"{fig['member_impact_2026_static']['member_minutes']:,}", fig['faults_total'])),
        ('h', 'Priority 1 work program (%d of %d crew-days allocated; cutoff %s member-minutes/crew-day)'
              % (pr['wash_days'] + pr['repeat_days_used'], pr['budget_days'], f"{pr['cutoff_mm_per_day']:,}")),
        ('p', 'Coastal washing before 1 December (%d crew-days): %s. Joint ESDD/NSDD state tracking (empirical beta %.3f, '
              'flashover level %.4f mg/cm2 effective) separates these %d due sections from %d clean coastal-marsh and '
              'October-washed pasture sections; washing on ESDD alone would spend %d crew-days and displace 3 Priority 1 repairs.'
              % (pr['wash_days'], wash, fig['beta_nsdd'], fig['flashover_level'],
                 fig['wash_due_count'], fig['wash_not_due_count'], fig['esdd_only_due_count'])),
        ('p', 'Winter avian guards by 15 December (%d crew-days): %s. Line 16 str 23 ranks #1 overall because Heron Bend '
              'was energized from Line 16 during planned 2024 supervisory switching when the roost locked out.'
              % (pr['crew_day_mix'].get('bird', 0), group_txt(funded, 'bird'))),
        ('p', 'Winter insulator replacements by 31 December (%d crew-days): %s. Correcting YNd1 ground infeed from Brushy Creek '
              'BESS and Coyote Draw Solar shifts Line 8 back %d structures (to %.2f km) and Line 9 back %d structures (to %.2f km); '
              'inverting coupled double-circuit Z0m shifts Line 11 str %d forward %d structures from its uncoupled estimate.'
              % (pr['crew_day_mix'].get('insulator', 0), group_txt(funded, 'insulator'),
                 ip8['structure_shift'], ip8['golden_km'], ip9['structure_shift'], ip9['golden_km'],
                 dc11['golden_structure'], dc11['structure_shift'])),
        ('p', 'Outside-ROW hazard trees by 31 March (%d crew-days): %s. Pre-summer vegetation clearing by 1 May (%d crew-days): %s '
              '(including Line 10 str 68-69 and 102-103 and Line 11 str 112-113 located with coupled Z0m, and underbuilt grow-in '
              'Line 12 str 44-45 whose contact temperature falls %.2f C/yr).'
              % (pr['crew_day_mix'].get('fallin', 0), group_txt(funded, 'fallin'),
                 pr['crew_day_mix'].get('growin', 0), group_txt(funded, 'growin'), abs(l12_slp))),
        ('p', 'Underbuild clearance restoration by 1 May (%d crew-days): %s. Post-trim IEEE 738 contact temperatures remained '
              'flat (%+.2f C/yr vs %.2f to %.2f C/yr on underbuilt grow-ins), confirming fixed contact with the 12.47 kV circuit below.'
              % (pr['crew_day_mix'].get('hardware', 0), group_txt(funded, 'hardware'),
                 c_l15['slope_c_per_year'], ub_rng[1], ub_rng[0])),
        ('h', 'Priority 2 deferred backlog (%d open locations, next highest %s member-minutes/crew-day)'
              % (pr['deferred_count'], f"{pr['first_deferred_mm_per_day']:,}")),
        ('p', 'Defer past the %d-crew-day cap: %s. Line 6 str 57-58 is also a confirmed 12.47 kV underbuild clearance span '
              '(flat %+.2f C/yr post-trim), not a tree, and moves to Priority 2 hardware restoration rather than vegetation clearing. '
              '%d additional historical repeats were fixed after their last fault and excluded.'
              % (pr['budget_days'], def_txt, c_l6['slope_c_per_year'], fig['fixed_repeats_count'])),
        ('small', 'Prepared under RP-04 Rev 5. All structure numbers follow the current 2026 inventory (post-2023 rebuild numbering on Lines 8 and 13).'),
    ]
    O.docx(path, blocks, 'memo', '69 kV work list', C.PEOPLE['reliability'], revision=5, total_time=112, seed='memo13v7',
           table=C.GOLD_STAMP)
