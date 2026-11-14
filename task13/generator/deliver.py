"""The golden deliverables, from target/ alone through the golden route: the fault table (CSV, one row per fault since
January 2022), the review workbook (faults by line and year, 2026 by cause, the 2026 member impact, the repeat
locations, the washing sections, the work list and what the shortcuts would have sent the crews to), and the one-page
work list memo (Word)."""
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

CAUSE_NAME = {'lightning': 'lightning', 'bird': 'bird or other animal', 'fog': 'salt contamination',
              'insulator': 'insulator failure', 'growin': 'vegetation grown into the line',
              'fallin': 'vegetation from outside the right of way', 'vehicle': 'vehicle or other third party',
              'hardware': 'equipment or hardware other than insulators', 'unknown': 'other or unknown'}
FIX = {'bird': 'perch guards and streamer shields', 'insulator': 'replace the string', 'growin': 'clear the span',
       'fallin': 'remove the hazard trees', 'hardware': 'restore the clearance to the 12.47 kV circuit below (re-sag the span)'}
BY_WHEN = {'bird': '15 December 2026', 'insulator': '31 December 2026', 'fallin': '31 March 2027', 'growin': '1 May 2027',
           'hardware': '1 May 2027', 'wash': '1 December 2026'}


def build_golden(target, golden, w=None):
    if os.path.exists(golden):
        shutil.rmtree(golden)
    os.makedirs(golden)
    r = G.run(target, G.GOLD)
    d = r['d']
    G.member_impact(d, r['faults'], year=None)
    fig = json.load(open(os.path.join(C.HERE, 'figures.json')))
    rep_id = {}
    reps = sorted(r['repeat'], key=lambda x: (int(x['line'][1:]), x['s_min']))
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


def write_csv(r, d, rep_id, path):
    with open(path, 'w', newline='') as fh:
        wr = csv.writer(fh)
        wr.writerow(['fault_id', 'date', 'time', 'line', 'terminal_a', 'terminal_b', 'km_from_terminal_a', 'structure', 'span',
                     'fault_type', 'cause', 'cleared_on_reclose', 'members_interrupted', 'member_minutes', 'members_momentary',
                     'repeat_location'])
        for i, f in enumerate(sorted(r['faults'], key=lambda f: f['t'])):
            L = d['lines'][f['line']]
            lt = C.to_local(f['t'])
            imp = f.get('impact') or dict(sustained=0, minutes=0.0, momentary=0)
            span = '%d-%d' % f['span'] if (f['cause'] in ('growin', 'fallin', 'hardware') and f.get('span')) else ''
            wr.writerow(['F%04d' % (i + 1), lt.strftime('%Y-%m-%d'), lt.strftime('%H:%M:%S'), PS.lname(f['line']),
                         d['stations'][L['a']]['name'], d['stations'][L['b']]['name'],
                         '' if f['km'] is None else '%.2f' % f['km'], '' if f['structure'] is None else f['structure'], span,
                         f.get('type') or '', CAUSE_NAME[f['cause']], 'no' if imp['sustained'] or _locked(f) else 'yes',
                         imp['sustained'], int(round(imp['minutes'])), imp['momentary'], rep_id.get(id(f), '')])


def _locked(f):
    return any(x.get('state') == 'LOCKOUT' for x in f.get('soe', []))


NOTES = [['Item', 'Note'],
         ['As of', '31 October 2026; in this November report the year 2026 runs from January to October (RP-04)'],
         ['Fault', 'one protection operation sequence on one 69 kV line; switching, testing and maintenance operations are not faults (RP-04)'],
         ['Location', "the structure nearest the fault, numbered as on today's structure inventory; Lines 8 and 13 were renumbered after "
                      "their 2023 rebuilds, and their older records are read through the inventory's former numbers"],
         ['Member interruption', "a member out for more than five minutes, to the restoration of supply to the member's substation, from "
                                 "the SCADA sequence of events and the monthly members by feeder (RP-04)"],
         ['Repeat location', 'three or more faults of one cause on one line within 400 m since 1 January 2022; salt contamination is left '
                             'to the washing programme (RP-04)'],
         ['Washing', 'a section is due when its deposit on 31 October is at or above the deposit at which the porcelain has flashed '
                     'over in fog, read as the tenth percentile of the deposits at the salt flashovers since 2022; the fog season '
                     'runs from 1 December to 31 March (RP-04)'],
         ['Deposit', "each section carried day by day from its washes: the test insulators' gains between readings with no "
                     "wetting rain follow the onshore wind at the substation stations (the Port Alcorn airport before them), so "
                     "the rate is set by each section's distance from the Gulf and each day's onshore wind, and a soaking rain "
                     "leaves about half"],
         ['Times', "Central time throughout; each relay's clock set against SCADA, the solar farm's export read on standard time"]]


def write_xlsx(r, d, reps, fig, path):
    years = ['2022', '2023', '2024', '2025', '2026']
    s1 = [['Line', 'Name'] + [y if y != '2026' else '2026 (Jan-Oct)' for y in years] + ['Total']]
    tot = collections.Counter()
    for lid in sorted(d['lines'], key=lambda x: int(x[1:])):
        row = fig['faults_by_line_year'].get(PS.lname(lid), {})
        vals = [int(row.get(y, 0)) for y in years]
        for y, v in zip(years, vals):
            tot[y] += v
        s1.append([PS.lname(lid), '%s-%s' % (d['lines'][lid]['a_name'], d['lines'][lid]['b_name'])] + vals + [sum(vals)])
    s1.append(['All lines', ''] + [tot[y] for y in years] + [sum(tot.values())])
    causes = ['lightning', 'bird', 'fog', 'insulator', 'growin', 'fallin', 'vehicle', 'hardware', 'unknown']
    c26 = collections.Counter((f['cause'], f['line']) for f in r['faults'] if C.to_local(f['t']).year == 2026)
    lids = sorted(d['lines'], key=lambda x: int(x[1:]))
    s2 = [['Cause'] + ['L%d' % int(l[1:]) for l in lids] + ['All lines']]
    for c in causes:
        vals = [c26.get((c, l), 0) for l in lids]
        s2.append([CAUSE_NAME[c]] + vals + [sum(vals)])
    s2.append(['All causes'] + [sum(c26.get((c, l), 0) for c in causes) for l in lids] + [sum(c26.values())])
    s3 = [['Line', 'Member interruptions (over 5 min)', 'Member-minutes', 'Momentary member events']]
    for lid in lids:
        v = fig['member_impact_2026_by_line'].get(PS.lname(lid), dict(sustained=0, member_minutes=0, momentary=0))
        s3.append([PS.lname(lid), v['sustained'], v['member_minutes'], v['momentary']])
    t = fig['member_impact_2026']
    s3.append(['All lines', t['sustained'], t['member_minutes'], t['momentary']])
    s4 = [['Ref', 'Line', 'Structures', 'Cause', 'Faults', 'First', 'Last', 'Fix', 'Status']]
    for rl in reps:
        place = ('%d-%d' % rl['span']) if rl['cause'] in ('growin', 'hardware') and rl['span'] else (
            '%d-%d' % (rl['s_min'], rl['s_max']) if rl['cause'] == 'fallin' else str(rl['structure']))
        status = 'fixed after its last fault' if rl['fixed'] else 'on the work list'
        s4.append([rl['rid'], PS.lname(rl['line']), place, CAUSE_NAME[rl['cause']], rl['n'], C.to_local(rl['first']).date(),
                   C.to_local(rl['last']).date(), FIX[rl['cause']], status])
    s5 = [['Section', 'Structures', 'Distance from the Gulf (km)', 'Last washed', 'Deposit 31 Oct 2026 (mg/cm2)',
           'Times the flashover level', 'Due before the fog season']]
    lv = r['deposits']['level']
    for _, row in d['wash_sections'].iterrows():
        lid = 'L%02d' % int(str(row['Line']).split()[1])
        sid = '%s-W%s' % (lid, str(row['Section']).split()[-1])
        v = r['deposits']['sections'][sid]
        s5.append(['%s, %s' % (row['Line'], row['Section']), '%d-%d' % (int(row['From structure']), int(row['To structure'])),
                   round(v['dist'], 2), v['last_wash'], round(v['deposit'], 3), round(v['deposit'] / lv, 1), 'yes' if v['due'] else 'no'])
    s5.append(['Flashover level (tenth percentile of the deposits at the salt flashovers)', '', '', '', round(lv, 3), 1.0, ''])
    s6 = [['No.', 'Work', 'Line', 'Structures', 'Cause', 'By']]
    k = 0
    for cause in ('bird', 'insulator', 'fallin', 'growin', 'hardware'):
        for rl in [x for x in reps if x['cause'] == cause and not x['fixed']]:
            k += 1
            place = ('%d-%d' % rl['span']) if cause in ('growin', 'hardware') and rl['span'] else (
                '%d-%d' % (rl['s_min'], rl['s_max']) if cause == 'fallin' else str(rl['structure']))
            s6.append([k, FIX[cause], PS.lname(rl['line']), place, CAUSE_NAME[cause], BY_WHEN[cause]])
    for _, row in d['wash_sections'].iterrows():
        lid = 'L%02d' % int(str(row['Line']).split()[1])
        sid = '%s-W%s' % (lid, str(row['Section']).split()[-1])
        if r['deposits']['sections'][sid]['due']:
            k += 1
            s6.append([k, 'wash the insulators', str(row['Line']), '%d-%d (%s)' % (int(row['From structure']), int(row['To structure']), row['Section']),
                       CAUSE_NAME['fog'], BY_WHEN['wash']])
    care = fig['careful']
    gs, cc = fig['gulf_string'], fig['clearance_contact']
    s7 = [['Shortcut', 'What it sends the crews to'],
          ["Every fog-night flashover on the Gulf porcelain booked as salt, the inland strings' light-rain flashovers as the "
           "insulator signature", 'no string on the Gulf lines; %s structure %d left for the washing crews' % (gs['line'], gs['structure'])],
          ["Every summer afternoon contact with no stroke at a span with trees booked as a grow-in, as the patrol's live oak "
           "suggested", 'clear the span: %s, structures %s, though the oak was cut back in %s' % (cc['line'], cc['structures'],
                                                                                              cc['trim'][:7])],
          ["Each section's deposit at the test insulators' average daily rate, or the latest test reading at the nearest site",
           'Line 2 sections 1 and 6 left as washed in October (%s and %s times the level on that reading of the record)'
           % tuple('%.1f' % x for x in care['resalted_ratio'])],
          ['All three together (the reflex route)', '; '.join(x for x in care['work_list'] if x not in fig['work_list'])
           + ' on the list; missing ' + '; '.join(x for x in fig['work_list'] if x not in care['work_list'])]]
    # the evidence behind the three judgments, fault by fault
    ser = r['deposits']['series']
    s8 = [['Date', 'Time', 'Line', 'Structure', 'Weather at the line', 'Section', 'Last washed before',
           'Section deposit that day (mg/cm2)', 'Times the flashover level', 'Booked as']]
    for f in sorted([f for f in r['faults'] if f['line'] == 'L%02d' % int(gs['line'].split()[1]) and f['structure'] is not None
                     and abs(f['structure'] - gs['structure']) <= 1 and f['cause'] in ('insulator', 'fog')], key=lambda f: f['t']):
        sid = G.section_of({'sections': ser}, f)
        if sid is None:
            continue
        day = C.to_local(f['t']).date()
        last = max([w for w in ser[sid]['washes'] if w <= day], default=None)
        dep = ser[sid]['series'][day]
        s8.append([day, C.to_local(f['t']).strftime('%H:%M'), PS.lname(f['line']), f['structure'],
                   'light rain' if (f.get('sig') or {}).get('rain') else 'fog or dew', PS.wash_label(sid).replace('wash: ', ''),
                   last, round(dep, 3), round(dep / lv, 1), CAUSE_NAME[f['cause']]])
    s9 = [['Line', 'Span', 'Date', 'Time', 'Line current (A)', 'Air (C)', 'Wind (m/s)', 'Conductor (C)', 'Last trim before',
           'Booked as']]
    vv = d['veg']
    for f in sorted([f for f in r['faults'] if f['cause'] in ('growin', 'hardware') and f.get('span') and
                     isinstance(f.get('sig'), dict) and f['sig'].get('tc')], key=lambda f: (int(f['line'][1:]), f['structure'], f['t'])):
        lname = PS.lname(f['line'])
        day = C.to_local(f['t']).date()
        tr = [x for x in vv[(vv['line'] == lname) & vv['work_type'].isin(['HOT SPOT', 'CYCLE TRIM'])].itertuples()
              if int(x.from_structure) <= f['span'][1] and f['span'][0] <= int(x.to_structure)
              and dt.date.fromisoformat(str(x.completed)[:10]) <= day]
        last = max((dt.date.fromisoformat(str(x.completed)[:10]) for x in tr), default=None)
        sg = f['sig']
        s9.append([lname, '%d-%d' % f['span'], day, C.to_local(f['t']).strftime('%H:%M'), sg.get('amps'), sg.get('tair'),
                   sg.get('wind'), round(sg['tc'], 1), last, CAUSE_NAME[f['cause']]])
    O.xlsx(path, [('Faults by line and year', ['69 kV faults by line and year', 'One fault per protection operation sequence on one line (RP-04)'],
                   s1, [9, 34, 8, 8, 8, 8, 14, 8], {}),
                  ('2026 by cause', ['2026 faults (January to October) by cause and line'], s2, [36] + [5] * 16 + [9], {}),
                  ('2026 member impact', ['Member interruptions, member-minutes and momentary member events from 69 kV faults, January to October 2026'],
                   s3, [12, 18, 16, 18], {1: '#,##0', 2: '#,##0', 3: '#,##0'}),
                  ('Repeat locations', ['Three or more faults of one cause within 400 m on one line since 1 January 2022'],
                   s4, [7, 9, 12, 36, 7, 11, 11, 30, 24], {5: 'yyyy-mm-dd', 6: 'yyyy-mm-dd'}),
                  ('Washing sections', ['Salt deposit on each section\'s porcelain on 31 October 2026'], s5, [44, 11, 14, 12, 16, 14, 16],
                   {3: 'yyyy-mm-dd', 4: '0.000', 5: '0.0'}),
                  ('Work list', ['69 kV work list, winter 2026-27 and before summer 2027'], s6, [5, 44, 9, 22, 40, 17], {}),
                  ('Line 2 str 63', ['Flashovers at %s structure %d and its neighbours, against the section deposit' % (gs['line'], gs['structure'])],
                   s8, [11, 6, 8, 9, 14, 18, 13, 16, 12, 30], {0: 'yyyy-mm-dd', 6: 'yyyy-mm-dd'}),
                  ('Summer contacts', ['Summer afternoon contacts with no stroke: conductor temperature at each, against the trims'],
                   s9, [8, 8, 11, 6, 12, 8, 9, 12, 14, 40], {2: 'yyyy-mm-dd', 8: 'yyyy-mm-dd'}),
                  ('Shortcuts', ['What the quicker readings of the same records would have sent the crews to'], s7, [60, 110], {}),
                  ('Notes', ['Definitions and conventions'], NOTES, [20, 120], {})],
           'xlsx', '69 kV fault review 2026', C.PEOPLE['reliability'], table=C.GOLD_STAMP)


def write_memo(r, fig, path):
    reps = [x for x in r['repeat'] if not x['fixed']]
    lst = lambda cause, skip=(): ', '.join(
        '%s str %s' % (PS.lname(x['line']), (('%d-%d' % x['span']) if cause in ('growin', 'hardware') and x['span'] else
                                            ('%d-%d' % (x['s_min'], x['s_max']) if cause == 'fallin' else x['structure'])))
        for x in sorted(reps, key=lambda x: (int(x['line'][1:]), x['s_min'])) if x['cause'] == cause and (x['line'], x['structure']) not in skip)
    by_line = collections.OrderedDict()
    for x in fig['wash_due']:
        ln, sec = x.replace('wash: ', '').split(', Section ')
        by_line.setdefault(ln, []).append(int(sec))

    def secs(v):
        v = sorted(v)
        runs, cur = [], [v[0]]
        for a in v[1:]:
            if a == cur[-1] + 1:
                cur.append(a)
            else:
                runs.append(cur)
                cur = [a]
        runs.append(cur)
        parts = []
        for rr in runs:
            parts += ['%d to %d' % (rr[0], rr[-1])] if len(rr) > 2 else [str(x) for x in rr]
        return parts[0] if len(parts) == 1 else ', '.join(parts[:-1]) + ' and ' + parts[-1]
    wash = '; '.join('%s %s %s' % (ln, 'sections' if len(v) > 1 else 'section', secs(v)) for ln, v in by_line.items())
    t = fig['member_impact_2026']
    n26 = fig['faults_2026']
    gs, cc, rs = fig['gulf_string'], fig['clearance_contact'], fig['resalted']
    gulf = [x for x in reps if x['cause'] == 'insulator' and x['line'] in ('L01', 'L02', 'L03', 'L04')]
    blocks = [
        ('title', 'Memo'),
        ('p', 'To: Reliability review (Thomas Evans, chair; Julie Peterson; Allison Ward)\nFrom: Brittany Melton, Reliability Engineer\nDate: 12 November 2026\nRe: 69 kV work list, winter 2026-27 and before summer 2027'),
        ('p', 'The 69 kV system had %d faults from January to October, with %s member interruptions and %s member-minutes. The '
              'fault table and the review workbook have every fault since January 2022, located and caused.'
              % (n26, f'{t["sustained"]:,}', f'{t["member_minutes"]:,}')),
        ('h', 'This winter'),
        ('p', 'Perch guards and streamer shields by 15 December at %s, the roost structures in the environmental survey.' % lst('bird')),
        ('p', 'Replace the strings by 31 December at %s. The Line 9 one is %.1f km past the solar tap; Shell Ridge reads it '
              'short because the farm feeds ground current into the fault. %s structure %d looked like salt, but it kept '
              'flashing over after each of the five washes of %s, %d times below any deposit the salt has flashed at, while '
              'the rest of the section stayed quiet. The string is cracked.'
              % (lst('insulator'), fig['tap_string_beyond_tap_km'], gs['line'], gs['structure'], gs['section'], gs['below_level'])),
        ('p', 'Wash before 1 December: %s. Their deposit on 31 October is at or above the %.3f mg/cm2 the porcelain has flashed '
              'over at; nothing has soaked the coast since June. Line 2 sections 1 and 6, washed on %s and %s, took the four days '
              'of southerly wind before the 27 October front and held %.1f and %.1f times the level again by 31 October.'
              % (wash, fig['flashover_level'], dt.date.fromisoformat(rs['Line 2, Section 1']['last_wash']).strftime('%d %B').lstrip('0'),
                 dt.date.fromisoformat(rs['Line 2, Section 6']['last_wash']).strftime('%d %B').lstrip('0'),
                 rs['Line 2, Section 1']['ratio'], rs['Line 2, Section 6']['ratio'])),
        ('p', 'Remove the hazard trees by the end of March at %s: dead pines outside the right of way, down with fronts and storms.'
              % lst('fallin')),
        ('h', 'Before next summer'),
        ('p', 'Clear the spans by 1 May at %s, where the conductor reaches a tree that comes closer every summer.' % lst('growin')),
        ('p', 'Restore the clearance at %s structures %s by 1 May. It is not a tree: the oak there was cut back in %s, yet the '
              'conductor has gone on touching at the same %.0f to %.0f C every summer, where every grow-in touches about 2 C cooler '
              'each year. It is reaching the 12.47 kV circuit built under it; re-sag the span.'
              % (cc['line'], cc['structures'], dt.date.fromisoformat(cc['trim']).strftime('%B %Y'), cc['contact_temperature'][0],
                 cc['contact_temperature'][1])),
        ('small', 'Repeat locations, the work list and the washing rule are as RP-04 Rev 4 defines them. Structure numbers are as on '
                  'today\'s inventory; Lines 8 and 13 were renumbered after their 2023 rebuilds.'),
    ]
    O.docx(path, blocks, 'memo', '69 kV work list', C.PEOPLE['reliability'], revision=4, total_time=96, seed='memo13',
           table=C.GOLD_STAMP)
