"""The registers, settings, studies, procedure and the field workbooks: the 69 kV line register, the structure
inventory, the substation register, the relay settings, the 2022 and 2025 protection studies (PDFs the planning
engineer exported from Word), the reliability reporting procedure (Word), the test insulator, washing, patrol, roost,
control room and Ponder Creek workbooks, and two files the cooperative keeps that the question does not need."""
import cmath
import csv
import datetime as dt
import math

import numpy as np
from reportlab.platypus import Paragraph, Spacer, Table

import common as C
import faults as F
import network as N
import office as O
import pack_env as E
import pack_ops as PO

MI = 1.609344
REBUILT = N.REBUILT


def line_no(lid):
    return 'Line %d' % int(lid[1:])


def write_lines(w, path):
    net = w['net']
    rows = [['Line', 'Name', 'Terminal A', 'Terminal B', 'Length (km)', 'Conductor', 'Built', 'Rebuilt, structures renumbered',
             'Insulators', 'R1 (ohm/km)', 'X1 (ohm/km)', 'R0 (ohm/km)', 'X0 (ohm/km)']]
    for lid in sorted(net['lines']):
        L = net['lines'][lid]
        ins = sorted(set(s['insulator'] for s in L['structures']))
        insd = ' / '.join({'porcelain': '69 kV porcelain line post, 1,320 mm leakage', 'polymer': '69 kV silicone polymer post'}[i] for i in ins)
        rows.append([line_no(lid), L['name'], N.ST[L['a']]['name'], N.ST[L['b']]['name'], round(L['length'], 2), L['conductor'],
                     L['year'], (N.REBUILT[lid][0] if lid in N.REBUILT else None), insd, round(L['z1'].real, 4), round(L['z1'].imag, 4),
                     round(L['z0'].real, 4), round(L['z0'].imag, 4)])
    taps = [['Tap substation', 'Line', 'Distance from terminal A (km)', 'Members (Oct 2026)', 'Feeders',
             'Second 69 kV source', 'Transfer to second source', 'Line switches']]
    for tp in sorted(net['taps'], key=lambda t: (t['line'], t['km'])):
        taps.append([tp['name'], line_no(tp['line']), tp['km'], tp['members'], tp['feeders'],
                     line_no(tp['alt']) if tp['alt'] else '', {'auto': 'automatic throw-over', 'manual': 'by control room (SCADA)',
                                                              'none': ''}[tp['backup']],
                     'motor-operated, SCADA' if tp['moab'] else 'manual'])
    tapl = [['Item', 'Value'], ['Line', line_no(N.TAP_LINE)], ['Tap point, distance from Shell Ridge (km)', N.TAP_KM],
            ['Tap line to the solar farm substation (km)', N.TAP_LEN], ['Tap line conductor', '477 ACSR Hawk'],
            ['Interconnection', 'Coyote Draw Solar LLC, 60 MW AC, in service 20 Feb 2023']]
    O.xlsx(path, [('Lines', [C.ORG + ' 69 kV line register', 'Sequence impedances per km at 50 C, from the conductor tables'],
                   rows, [8, 34, 16, 16, 10, 16, 7, 14, 46, 10, 10, 10, 10], {7: 'yyyy-mm-dd'}),
                  ('Taps', [], taps, [20, 8, 14, 12, 8, 12, 24, 20], {}),
                  ('Solar tap', [], tapl, [40, 40], {})],
           'lines', '69 kV line register', C.PEOPLE['planning'])


def write_structures(w, path):
    net = w['net']
    with open(path, 'w', newline='') as fh:
        wr = csv.writer(fh)
        wr.writerow(['structure_id', 'line', 'structure_no', 'former_no', 'km_from_terminal_a', 'structure_type', 'insulator',
                     'insulator_installed', 'underbuild', 'latitude', 'longitude', 'gulf_shore_km'])
        for lid in sorted(net['lines']):
            for s in net['lines'][lid]['structures']:
                la, lo = E.latlon(s['x'], s['y'])
                former = ''
                if lid in REBUILT:
                    former = s['no'] + REBUILT[lid][1] if s['no'] + REBUILT[lid][1] > 0 else ''
                wr.writerow(['%s-%03d' % (lid, s['no']), line_no(lid), s['no'], former, '%.2f' % s['km'], s['kind'],
                             s['insulator'], s['ins_year'], s['underbuild'], '%.5f' % la, '%.5f' % lo, '%.2f' % s['shore_km']])
    return len(net['structures'])


def write_subs(w, path):
    net = w['net']
    st = [['Code', 'Station', 'Type', 'Relays on the 69 kV line terminals']]
    for code in sorted(N.ST):
        s = N.ST[code]
        st.append([code, s['name'], s['kind'], {'ER': 'EventRecall R-421 series', 'GV': 'GridVue D60',
                                                'EM': 'electromechanical (distance and ground overcurrent, no event recording)'}[s['relay']]])
    xf = [['Location', 'Unit', 'Rating (MVA)', 'Impedance (%)', 'Connection', 'Neutral', 'In service', 'Retired']]
    xf += [['Bayside', 'T1 138/69 kV autotransformer', 150, 8.1, 'YNa0 with delta tertiary', 'solid', '2009-05-12', ''],
           ['Bayside', 'T2 138/69 kV autotransformer', 150, 8.3, 'YNa0 with delta tertiary', 'solid', '2014-10-02', ''],
           ['Inland', 'T1 138/69 kV autotransformer', 75, 7.6, 'YNa0', 'solid', '1994-06-20', '2024-03-14'],
           ['Inland', 'T2 138/69 kV autotransformer', 150, 8.0, 'YNa0 with delta tertiary', 'solid', '2024-03-14', ''],
           ['Coyote Draw Solar', 'GSU 69/34.5 kV', N.GSU['mva'], N.GSU['z_pct'], 'YNd1 (69 kV side grounded wye)',
            'reactor, %.0f ohm' % N.GSU['ngr_ohm'], '2023-02-20', '']]
    for tp in sorted(net['taps'], key=lambda t: t['name']):
        mva = 12.5 if tp['members'] < 2500 else (20.0 if tp['members'] < 4000 else 28.0)
        xf.append([tp['name'], 'T1 69/12.47 kV', mva, 7.2 + (mva > 15) * 0.8, 'Dyn1 (69 kV side delta)', 'solid (12.47 kV)',
                   '%d-%02d-%02d' % (1985 + (sum(map(ord, tp['name'])) % 30), 1 + sum(map(ord, tp['name'])) % 12, 10), ''])
    tr = [['Tap substation', 'Second source', 'Transfer']]
    for tp in sorted(net['taps'], key=lambda t: t['name']):
        tr.append([tp['name'], line_no(tp['alt']) if tp['alt'] else 'none',
                   {'auto': 'automatic throw-over on loss of voltage (20 s)', 'manual': 'closed by the control room (SCADA)',
                    'none': '-'}[tp['backup']]])
    O.xlsx(path, [('Stations', [C.ORG + ' substation register'], st, [7, 20, 12, 60], {}),
                  ('Transformers', [], xf, [20, 30, 10, 11, 30, 18, 11, 11], {}),
                  ('Transfer schemes', [], tr, [20, 14, 44], {})],
           'subs', 'Substation register', C.PEOPLE['planning'])


def write_settings(w, path):
    net = w['net']
    rows = [['Station', 'Relay', 'Line', 'Family', 'CT ratio', 'Line length setting', 'Units', 'Z1 primary (ohm)', 'Z1 angle',
             'Z0 primary (ohm)', 'Z0 angle', 'k0 magnitude', 'k0 angle', 'Zone 1 reach (%)', 'Zone 2 reach (%)',
             'Reclose', 'Time source', 'Settings issued']]
    for lid in sorted(net['lines']):
        L = net['lines'][lid]
        z1, z0 = L['z1'] * L['length'], L['z0'] * L['length']
        k0 = (z0 - z1) / (3 * z1)
        for end in ('a', 'b'):
            stc = L[end]
            fam = N.ST[stc]['relay']
            if fam == 'EM':
                rows.append([N.ST[stc]['name'], 'PND-L%d' % int(lid[1:]), line_no(lid), 'electromechanical', '600:5', '', '', '', '', '',
                             '', '', '', 85, '', '2 shots (1 s, 15 s)', '-', '1998-04-07'])
                continue
            units = 'mi' if fam == 'ER' else 'km'
            length = L['length'] / MI if fam == 'ER' else L['length']
            issued = '2024-03-12' if stc == 'INL' else ('2023-02-14' if lid == 'L09' else
                                                        '%d-%02d-%02d' % (2016 + int(lid[1:]) % 7, 1 + int(lid[1:]) % 12, 9))
            rows.append([N.ST[stc]['name'], '%s-L%d' % (stc, int(lid[1:])), line_no(lid), 'EventRecall R-421' if fam == 'ER' else 'GridVue D60',
                         '1200:5' if L['conductor'] == '795 ACSR Drake' else '800:5', round(length, 2), units,
                         round(abs(z1), 2), round(math.degrees(cmath.phase(z1)), 1), round(abs(z0), 2), round(math.degrees(cmath.phase(z0)), 1),
                         round(abs(k0), 3), round(math.degrees(cmath.phase(k0)), 1), 85, 125, '2 shots (1 s, 15 s)',
                         'IRIG-B (GPS clock)' if fam == 'ER' else 'SNTP (station clock)', issued])
    O.xlsx(path, [('Line relays', [C.ORG + ' 69 kV line relay settings summary', 'Primary ohms; distances in the relay\'s own units'],
                   rows, [16, 11, 8, 18, 9, 10, 6, 10, 8, 10, 8, 9, 8, 9, 9, 18, 18, 12], {})],
           'settings', '69 kV line relay settings', 'System Protection')


def _study(w, path, key, year, when, note):
    net = w['net']
    P = lambda t, s=O.BODY: Paragraph(t, s)
    rows = [[Paragraph(x, O.CELL) for x in ['Line', 'Terminal', 'Z1 source (ohm)', 'Angle', 'Z0 source (ohm)', 'Angle']]]
    for lid in sorted(net['lines']):
        L = net['lines'][lid]
        for end in ('a', 'b'):
            z1, z0 = N.source(lid, L[end], when)
            rows.append([Paragraph(x, O.CELL) for x in [line_no(lid), N.ST[L[end]]['name'], '%.2f' % abs(z1),
                                                        '%.1f' % math.degrees(cmath.phase(z1)), '%.2f' % abs(z0),
                                                        '%.1f' % math.degrees(cmath.phase(z0))]])
    t = Table(rows, colWidths=[52, 92, 74, 46, 74, 46])
    extra = []
    if year == 2025:
        zg = N.gsu_z(0)
        extra = [P('Coyote Draw Solar (tap on Line 9 at %.1f km from Shell Ridge): step-up transformer %.0f MVA, %.1f per cent, '
                   'YNd1 with a %.0f ohm neutral reactor; zero-sequence impedance seen from the 69 kV tap point %.2f ohm at %.1f '
                   'degrees including the %.1f km tap line. Inverter fault current limited to %.1f per unit of rated current.'
                   % (N.TAP_KM, N.GSU['mva'], N.GSU['z_pct'], N.GSU['ngr_ohm'], abs(zg + net['lines']['L09']['z0'] * N.TAP_LEN),
                      math.degrees(cmath.phase(zg + net['lines']['L09']['z0'] * N.TAP_LEN)), N.TAP_LEN, N.INV_I_PU))]
    story = [P(C.ORG + '<br/>Engineering, Transmission Planning', O.TITLE),
             P('69 kV System Protection Study, %d' % year, O.HEAD),
             P(note),
             P('1. Scope', O.HEAD),
             P('Short-circuit levels and source impedances for setting and checking the distance and ground relays on the '
               'cooperative\'s sixteen 69 kV lines. Positive and zero sequence values are given behind each line terminal '
               'with the line itself out of service, for the normal configuration, at 69 kV, in primary ohms.'),
             P('2. Source impedances behind each line terminal', O.HEAD), t]
    story += extra
    story += [P('3. Basis', O.HEAD),
              P('Transmission equivalents at the 138 kV buses as provided by the generation and transmission cooperative. '
                'Line constants from the conductor tables at 50 C. Loads and shunt capacitance neglected.'),
              Spacer(1, 6), P('Prepared by A. Russell, PE', O.SMALL)]
    O.pdf(path, story, key, '69 kV System Protection Study %d' % year, 'A. Russell', 'Protection study',
          '69 kV protection study %d' % year, producer={2022: 'LibreOffice 7.2', 2025: 'LibreOffice 7.6'}[year])


def write_studies(w, p22, p25):
    _study(w, p22, 'study22', 2022, C.REC0, 'March 2022. System model as of January 2022.')
    _study(w, p25, 'study25', 2025, C.T_END, 'February 2025. System model as of December 2024; supersedes the 2022 study.')


def write_procedure(path):
    blocks = [
        ('title', C.ORG),
        ('h', 'Reliability Reporting Procedure RP-04, Revision 4'),
        ('p', 'Engineering. Issued February 2024. Supersedes Revision 3 (January 2023).'),
        ('h', '1. Purpose'),
        ('p', 'How the cooperative keeps its record of faults on the 69 kV system and of the member interruptions they cause, '
              'and how the yearly 69 kV work list is drawn from it.'),
        ('h', '2. Definitions'),
        ('p', 'Fault. One protection operation sequence on one 69 kV line: the trips, the reclosing and any lockout that follow '
              'one initiation within 60 seconds count as one fault. Breaker operations for switching, testing or maintenance '
              'are not faults. A fault on another line that a relay sees without tripping is not a fault on the relay\'s line.'),
        ('p', 'Fault location. The structure nearest the point of the fault, numbered as on the structure inventory in force '
              'today; for a fault between two structures, the span, given by both structure numbers.'),
        ('p', 'Cause. One of: lightning; bird or other animal; salt contamination; insulator failure; vegetation grown into the '
              'line; vegetation from outside the right of way; vehicle or other third party; equipment or hardware other than '
              'insulators; other or unknown.'),
        ('p', 'Member interruption. A member account without power for more than five minutes because of a fault. Five minutes '
              'or less is a momentary event. Member-minutes are the sum, over the members interrupted, of the minutes each '
              'was without power, from the fault to the restoration of supply to the member\'s substation.'),
        ('p', 'Year. The calendar year. In a report made in November, the current year runs from 1 January to 31 October.'),
        ('p', 'Repeat location. A structure or span, or a run of adjacent structures no more than 400 m long, at which three '
              'or more faults of one cause have occurred on one line since 1 January 2022. Salt contamination is dealt with by '
              'the washing programme section by section and is not entered as a repeat location.'),
        ('p', 'Work list. Each repeat location whose cause has not been fixed since its last fault, with the fix for its '
              'cause: perch guards and streamer shields for birds; replacement for an insulator failure; clearing the span '
              'for vegetation grown into the line; removal of the hazard trees for vegetation from outside the right of way; '
              'for any other cause, the repair that removes it. And each washing section due for washing before the fog season.'),
        ('p', 'Due for washing before the fog season. A washing section is due when the salt deposit on its porcelain '
              'insulators on 31 October is at or above the deposit at which the cooperative\'s 69 kV porcelain line posts '
              'have flashed over in fog. The fog season runs from 1 December to 31 March.'),
        ('h', '3. Records'),
        ('p', 'Relay event records are retrieved from the line relays by System Protection each month. The SCADA master keeps '
              'the sequence of events. The system operators keep the control room 69 kV log on each shift. The outage '
              'management system keeps member outages by feeder. The line superintendent books line patrols, insulator '
              'washing and maintenance; the vegetation management coordinator books vegetation work. The line crews sample '
              'the test insulators each month.'),
        ('h', '4. Revision history'),
        ('p', 'Revision 3 (January 2023): repeat locations added. Revision 4 (February 2024): the work list and the washing '
              'definition added.'),
        ('small', 'Approved: T. Evans, Manager of Engineering'),
    ]
    O.docx(path, blocks, 'procedure', 'Reliability Reporting Procedure RP-04 Rev 4', C.PEOPLE['reliability'], seed='rp04')


def write_esdd(w, path):
    rows = [['Site', 'Date sampled', 'ESDD (mg/cm2)', 'NSDD (mg/cm2)', 'Sampled by', 'Remarks']]
    rng = np.random.default_rng(C.EV_SEED + 1212)
    for r in sorted(w['tests'], key=lambda r: (r['date'], r['site'])):
        rows.append([r['site'], r['date'], round(r['esdd'], 4), round(r['esdd'] * rng.uniform(4, 9), 3),
                     str(rng.choice(['Crew 2', 'Crew 4', 'Crew 5'])), ''])
    sites = [['Site', 'Location', 'Latitude', 'Longitude', 'Gulf shore (km)', 'Test string', 'Installed']]
    import field as FD
    for code, desc, (x, y) in FD.TEST_SITES:
        la, lo = E.latlon(x, y)
        sites.append([code, desc, round(la, 5), round(lo, 5), round(N._shore_dist(x, y), 2),
                      'same porcelain line post as the 69 kV lines, not energized, never washed', '2019-11-04'])
    O.xlsx(path, [('Readings', [C.ORG + ' test insulator deposits', 'Equivalent salt deposit density; each string sampled in place without cleaning'],
                   rows, [6, 12, 12, 12, 10, 20], {1: 'yyyy-mm-dd'}),
                  ('Sites', [], sites, [6, 26, 10, 11, 10, 60, 11], {})],
           'esdd', 'Test insulator deposits', C.PEOPLE['lines'])


def write_washing(w, path):
    rng = np.random.default_rng(C.EV_SEED + 1313)
    rows = [['Date', 'Line', 'Section', 'From structure', 'To structure', 'Crew', 'Water resistivity (ohm-cm)', 'Remarks']]
    for wsh in w['washes']:
        if wsh['date'] < dt.date(2022, 1, 1):
            continue
        rows.append([wsh['date'], line_no(wsh['line']), wsh['section'].split('-')[1].replace('W', 'Section '), wsh['s0'], wsh['s1'],
                     str(rng.choice(['Crew 5', 'Crew 7'])), int(rng.integers(2600, 4200)), ''])
    secs = [['Line', 'Section', 'From structure', 'To structure']]
    for s in w['sections']:
        secs.append([line_no(s['line']), s['id'].split('-')[1].replace('W', 'Section '), s['s0'], s['s1']])
    O.xlsx(path, [('Log', [C.ORG + ' 69 kV insulator washing log', 'Live-line high-pressure water'], rows,
                   [11, 8, 10, 10, 10, 8, 14, 20], {0: 'yyyy-mm-dd'}),
                  ('Sections', [], secs, [8, 10, 12, 12], {})],
           'washing', 'Insulator washing log', C.PEOPLE['lines'])


def write_patrols(rows, path):
    out = [['Patrol', 'Date', 'Line', 'From structure', 'To structure', 'Crew', 'Findings']]
    for i, r in enumerate(rows):
        out.append([8001 + i, r['date'], r['line'], r['frm'], r['to'], r['crew'], r['find']])
    O.xlsx(path, [('Patrols', [C.ORG + ' 69 kV line patrols'], out, [8, 11, 8, 10, 10, 8, 80], {1: 'yyyy-mm-dd'})],
           'patrols', 'Line patrol reports', C.PEOPLE['lines'])


def write_crlog(rows, path):
    out = [['Date', 'Time', 'Line', 'Event', 'Cause', 'Remarks', 'Members (est.)', 'Operator']]
    for r in rows:
        out.append([r['date'], r['time'], r['line'], r['event'], r['cause'], r['remarks'], r['members'], r['operator']])
    O.xlsx(path, [('69 kV log', [C.ORG + ' control room 69 kV log', 'Times are local (Central)'], out,
                   [11, 6, 8, 46, 7, 34, 12, 12], {0: 'yyyy-mm-dd'})],
           'crlog', 'Control room 69 kV log', C.PEOPLE['operations'])


def write_legacy(rows, path):
    out = [['Date', 'Time', 'Breaker', 'Line', 'Targets', 'Operations counter', 'Technician', 'Remarks']]
    for r in rows:
        out.append([r['date'], r['time'], r['breaker'], line_no(r['line']), r['targets'], r['counter'], r['tech'], r['remark']])
    O.xlsx(path, [('Targets', ['Ponder Creek substation, 69 kV relay targets', 'Electromechanical relays: targets found and reset on each visit'],
                   out, [11, 6, 12, 8, 14, 10, 8, 26], {0: 'yyyy-mm-dd'})],
           'legacy', 'Ponder Creek relay targets', C.PEOPLE['lines'])


def write_avian(rows, path):
    out = [['Site', 'Site name', 'Latitude', 'Longitude', 'Habitat', 'Species', 'Survey date', 'Count', 'Observer', 'Notes']]
    out += rows
    O.xlsx(path, [('Counts', [C.ORG + ' waterbird and raptor roost survey', 'Winter roost counts for the avian protection plan'],
                   out, [7, 26, 10, 11, 28, 34, 11, 7, 18, 40], {6: 'yyyy-mm-dd'})],
           'avian', 'Waterbird and raptor roost survey', C.PEOPLE['environment'])


def write_distractors(w, p_corr, p_ease):
    net = w['net']
    rng = np.random.default_rng(C.EV_SEED + 1414)
    rows = [['Structure', 'Line', 'Overall rating (1 best to 5)', 'Ground-line decay (%)', 'Woodpecker holes', 'Crossarm', 'Insulators', 'Notes']]
    for lid in sorted(net['lines']):
        for s in net['lines'][lid]['structures']:
            if rng.random() < 0.55:
                continue
            rows.append(['%s-%03d' % (lid, s['no']), line_no(lid), int(rng.choice([1, 2, 2, 3, 3, 4, 5], p=[0.2, 0.25, 0.2, 0.15, 0.1, 0.07, 0.03])),
                         int(max(0, rng.normal(6, 5))), int(rng.poisson(0.4)), str(rng.choice(['good', 'good', 'fair', 'checked', 'split'])),
                         str(rng.choice(['good', 'good', 'good', 'dirty', 'chipped skirt'])), ''])
    O.xlsx(p_corr, [('Survey', [C.ORG + ' tower and pole condition survey 2025', 'Ground-line and visual inspection, about half the structures'],
                     rows, [11, 8, 12, 12, 10, 10, 14, 20], {})],
           'corrosion', 'Tower and pole condition survey 2025', 'Osmose-style inspection contractor')
    with open(p_ease, 'w', newline='') as fh:
        wr = csv.writer(fh)
        wr.writerow(['easement_id', 'line', 'from_structure', 'to_structure', 'width_ft', 'recorded', 'grantor', 'restrictions'])
        k = 1
        for lid in sorted(net['lines']):
            n = len(net['lines'][lid]['structures'])
            a = 1
            while a < n:
                b = min(n, a + int(rng.integers(6, 30)))
                wr.writerow(['E-%05d' % (10000 + k), line_no(lid), a, b, int(rng.choice([60, 75, 100])),
                             '%d-%02d-%02d' % (int(rng.integers(1958, 2004)), int(rng.integers(1, 13)), int(rng.integers(1, 28))),
                             'Tract %d' % int(rng.integers(100, 999)), str(rng.choice(['', '', 'no herbicide', 'notify owner before trimming', 'gate key at ranch office']))])
                a = b
                k += 1
