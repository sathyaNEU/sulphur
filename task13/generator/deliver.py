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
              'hardware': 'equipment or hardware', 'unknown': 'other or unknown'}
FIX = {'bird': 'perch guards and streamer shields', 'insulator': 'replace the string', 'growin': 'clear the span',
       'fallin': 'remove the hazard trees'}
BY_WHEN = {'bird': '15 December 2026', 'insulator': '31 December 2026', 'fallin': '31 March 2027', 'growin': '1 May 2027',
           'wash': '1 December 2026'}


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
            span = '%d-%d' % f['span'] if (f['cause'] in ('growin', 'fallin') and f.get('span')) else ''
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
         ['Washing', 'a section is due when its deposit on 31 October is at or above the lowest deposit at a past fog flashover; the fog '
                     'season runs from 1 December to 31 March (RP-04)'],
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
        place = ('%d-%d' % rl['span']) if rl['cause'] == 'growin' and rl['span'] else (
            '%d-%d' % (rl['s_min'], rl['s_max']) if rl['cause'] == 'fallin' else str(rl['structure']))
        status = 'fixed after its last fault' if rl['fixed'] else 'on the work list'
        s4.append([rl['rid'], PS.lname(rl['line']), place, CAUSE_NAME[rl['cause']], rl['n'], C.to_local(rl['first']).date(),
                   C.to_local(rl['last']).date(), FIX[rl['cause']], status])
    s5 = [['Section', 'Structures', 'Distance from the Gulf (km)', 'Deposit 31 Oct 2026 (mg/cm2)', 'Due before the fog season']]
    for _, row in d['wash_sections'].iterrows():
        lid = 'L%02d' % int(str(row['Line']).split()[1])
        sid = '%s-W%s' % (lid, str(row['Section']).split()[-1])
        v = r['deposits']['sections'][sid]
        s5.append(['%s, %s' % (row['Line'], row['Section']), '%d-%d' % (int(row['From structure']), int(row['To structure'])),
                   round(v['dist'], 2), round(v['deposit'], 3), 'yes' if v['due'] else 'no'])
    s5.append(['Flashover level (lowest deposit at a fog flashover)', '', '', round(r['deposits']['level'], 3), ''])
    s6 = [['No.', 'Work', 'Line', 'Structures', 'Cause', 'By']]
    k = 0
    for cause in ('bird', 'insulator', 'fallin', 'growin'):
        for rl in [x for x in reps if x['cause'] == cause and not x['fixed']]:
            k += 1
            place = ('%d-%d' % rl['span']) if cause == 'growin' and rl['span'] else (
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
    s7 = [['Shortcut', 'What it sends the crews to'],
          ["The relays' own distances (both ends averaged) on the 2025 study, every summer afternoon fault with no stroke taken as a tree",
           '; '.join(x.replace('clear the span: ', '').replace('remove the hazard trees: ', 'hazard trees ') for x in care['R2']) or 'none'],
          ["The airport's visibility as the fog and the roost survey left out, faults placed by the relays' distances",
           'no perch guards; string replacement at ' + '; '.join(x.replace('replace the string: ', '') for x in care['R3'])],
          ["Shell Ridge's distance on the solar tap line as recorded, the solar farm's export left out", '; '.join(x.replace('replace the string: ', '') for x in care['R4'])],
          ['Every section with a past fog flashover washed, the fog read off the airport', '; '.join(x.replace('wash: ', '') for x in care['R7'])]]
    O.xlsx(path, [('Faults by line and year', ['69 kV faults by line and year', 'One fault per protection operation sequence on one line (RP-04)'],
                   s1, [9, 34, 8, 8, 8, 8, 14, 8], {}),
                  ('2026 by cause', ['2026 faults (January to October) by cause and line'], s2, [36] + [5] * 16 + [9], {}),
                  ('2026 member impact', ['Member interruptions, member-minutes and momentary member events from 69 kV faults, January to October 2026'],
                   s3, [12, 18, 16, 18], {1: '#,##0', 2: '#,##0', 3: '#,##0'}),
                  ('Repeat locations', ['Three or more faults of one cause within 400 m on one line since 1 January 2022'],
                   s4, [7, 9, 12, 36, 7, 11, 11, 30, 24], {5: 'yyyy-mm-dd', 6: 'yyyy-mm-dd'}),
                  ('Washing sections', ['Salt deposit on each section\'s porcelain on 31 October 2026'], s5, [44, 11, 14, 16, 16], {}),
                  ('Work list', ['69 kV work list, winter 2026-27 and before summer 2027'], s6, [5, 30, 9, 22, 36, 17], {}),
                  ('Shortcuts', ['What the quicker readings of the same records would have sent the crews to'], s7, [60, 110], {}),
                  ('Notes', ['Definitions and conventions'], NOTES, [20, 120], {})],
           'xlsx', '69 kV fault review 2026', C.PEOPLE['reliability'], table=C.GOLD_STAMP)


def write_memo(r, fig, path):
    reps = [x for x in r['repeat'] if not x['fixed']]
    lst = lambda cause: ', '.join('%s str %s' % (PS.lname(x['line']), (('%d-%d' % x['span']) if cause == 'growin' and x['span'] else
                                                                       ('%d-%d' % (x['s_min'], x['s_max']) if cause == 'fallin' else x['structure'])))
                                  for x in sorted(reps, key=lambda x: (int(x['line'][1:]), x['s_min'])) if x['cause'] == cause)
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
        for r in runs:
            parts += ['%d to %d' % (r[0], r[-1])] if len(r) > 2 else [str(x) for x in r]
        return parts[0] if len(parts) == 1 else ', '.join(parts[:-1]) + ' and ' + parts[-1]
    wash = '; '.join('%s sections %s' % (ln, secs(v)) for ln, v in by_line.items())
    t = fig['member_impact_2026']
    n26 = fig['faults_2026']
    blocks = [
        ('title', 'Memo'),
        ('p', 'To: Thomas Evans, Manager of Engineering\nFrom: Brittany Melton, Reliability Engineer\nDate: 12 November 2026\nRe: 69 kV work list, winter 2026-27 and before summer 2027'),
        ('p', 'The 69 kV system had %d faults from January to October this year. They caused %s member interruptions and %s '
              'member-minutes. The fault table and the review workbook attached have every fault since January 2022, located and with '
              'its cause.' % (n26, f'{t["sustained"]:,}', f'{t["member_minutes"]:,}')),
        ('h', 'This winter'),
        ('p', 'Perch guards and streamer shields by 15 December, at %s. These are the structures the environmental team\'s survey '
              'has birds roosting on. Their faults come before dawn between November and March whatever the fog is doing, so washing '
              'would not touch them.' % lst('bird')),
        ('p', 'Replace the strings by 31 December at %s. Each keeps flashing over in light rain at any hour. The one on Line 9 is '
              '%.1f km past the solar farm tap: Shell Ridge\'s relay reads it nearer Ponder Creek because the farm\'s step-up feeds '
              'ground current into the fault, at night as well as by day.' % (lst('insulator'), fig['tap_string_beyond_tap_km'])),
        ('p', 'Wash before 1 December: %s. The insulators there carry more salt than the porcelain has flashed over at. Nothing has '
              'soaked them since early June, and the August washes near the shore have built back up. The sections washed in '
              'late October were still below it on 31 October.' % wash),
        ('p', 'Remove the hazard trees by the end of March at %s. Their faults come with fronts and summer storms, from dead '
              'pines outside the right of way, so trimming the span will not stop them.' % lst('fallin')),
        ('h', 'Before next summer'),
        ('p', 'Clear the spans by 1 May at %s. These are the trees the conductor reaches when it sags hot on still afternoons. '
              'They are located by how each fault\'s ground current split between the two ends of the line; the relays\' own '
              'distances put them %.1f to %.1f km away. The Line 10 span counts its 2022 and 2023 contacts as well, read against '
              'the 2022 protection study (before the new Inland transformer).' % (lst('growin'), fig['growin_relay_offset_km'][0],
                                                                                  fig['growin_relay_offset_km'][1])),
        ('small', 'Repeat locations, the work list and the washing rule are as RP-04 Rev 4 defines them. Structure numbers are as on '
                  'today\'s inventory; Lines 8 and 13 were renumbered after their 2023 rebuilds.'),
    ]
    O.docx(path, blocks, 'memo', '69 kV work list', C.PEOPLE['reliability'], revision=4, total_time=96, seed='memo13',
           table=C.GOLD_STAMP)
