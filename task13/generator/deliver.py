"""The golden deliverables, written from the golden's own tables: the review workbook the distribution automation
engineer keeps (the 2026 working, the years, the operations, the batteries, the summer transfers, the 2027 forecast) and the
two-page memo for the commission filing, exported from Word by the house writer."""
import datetime as dt
import math

import pandas as pd
from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference
from openpyxl.styles import Alignment, Font, PatternFill
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Spacer, Table

import common as C
import postprocess as PP

BODY = ParagraphStyle('body', fontName='Helvetica', fontSize=9.6, leading=12.6, spaceAfter=5)
HEAD = ParagraphStyle('head', parent=BODY, fontName='Helvetica-Bold', fontSize=10.2, spaceBefore=7, spaceAfter=3)
TITLE = ParagraphStyle('title', parent=BODY, fontName='Helvetica-Bold', fontSize=12.5, leading=15, spaceAfter=2)
CELL = ParagraphStyle('cell', fontName='Helvetica', fontSize=8.6, leading=10.4)


def fmt(n):
    return '{:,}'.format(int(round(n)))


def _ws(wb, name, head, rows, widths, fmts=None, note=None):
    ws = wb.create_sheet(name)
    r = 1
    if note:
        ws.cell(row=1, column=1, value=note).font = Font(italic=True, size=9)
        r = 3
    for j, h in enumerate(head):
        c = ws.cell(row=r, column=j + 1, value=h)
        c.font = Font(bold=True)
        c.fill = PatternFill('solid', fgColor='E3E9F0')
        c.alignment = Alignment(wrap_text=True, vertical='top')
    for i, row in enumerate(rows):
        for j, v in enumerate(row):
            c = ws.cell(row=r + 1 + i, column=j + 1, value=v)
            if fmts and j in fmts:
                c.number_format = fmts[j]
    for j, w in enumerate(widths):
        ws.column_dimensions[chr(65 + j) if j < 26 else 'A' + chr(65 + j - 26)].width = w
    ws.freeze_panes = ws.cell(row=r + 1, column=1)
    return ws


def workbook(path, G):
    """G: the golden's results and tables (golden.results_for_deliverables)"""
    wb = Workbook()
    wb.remove(wb.active)
    br = G['bridge']
    restored5 = G['years'][2026]['restored_5']
    rows = [['Customers restored within five minutes of the first loss of supply', restored5],
            ['less: restored customers a receiving recloser\'s trip put out again', -br['reinterrupted']],
            ['less: receiving feeders\' own customers those trips put out', -br['recv_trips_own']],
            ['less: receiving feeders\' customers put out by closes onto the fault', -br['closes_own']],
            ['Customer interruptions avoided, Jan to Oct 2026 (order para. 2)', br['net']]]
    ws = _ws(wb, '2026 avoided', ['Item', 'Customer interruptions'], rows, [70, 20], {1: '#,##0;-#,##0'},
             note='Jan to Oct 2026. Sources: SCADA device events, OMS, ADMS FLISR archive. Prepared by N. Reeves.')
    ch = BarChart()
    ch.type = 'bar'
    ch.title = '2026: restored within five minutes to avoided'
    ch.add_data(Reference(ws, min_col=2, min_row=4, max_row=8), titles_from_data=False)
    ch.set_categories(Reference(ws, min_col=1, min_row=4, max_row=8))
    ch.legend = None
    ch.height, ch.width = 7.5, 17
    ws.add_chart(ch, 'D3')
    yrs = []
    for y in range(2022, 2027):
        d = G['years'][y]
        yrs.append([y if y < 2026 else '2026 (Jan-Oct)', d['lockouts'], d['restored_5'], d['restored_after'],
                    d['not_in_archive'], d['dashboard']])
    _ws(wb, 'Restorations by year', ['Year', 'Loop lockouts (loops in service)', 'Customers restored within 5 min',
                                     'Customers restored after 5 min', 'Lockouts not in the event archive',
                                     'Dashboard CI saved'], yrs, [16, 18, 18, 18, 18, 16],
        {1: '#,##0', 2: '#,##0', 3: '#,##0', 4: '#,##0', 5: '#,##0'})
    ops = G['ops2026']
    _ws(wb, 'Operations 2026', list(ops.columns), ops.values.tolist(), [18, 6, 9, 11, 10, 9, 12, 12, 11, 12, 12])
    bt = G['batteries']
    _ws(wb, 'Batteries', list(bt.columns), bt.values.tolist(), [11, 12, 9, 10, 12, 14, 10],
        note='Each control\'s battery fitted on its own weekly load tests (resistance against the hour\'s airport '
             'temperature and the battery\'s age), carried to -27 C at 28 Feb 2027. Operation needs 21.2 V at 30 A.')
    sm = G['summer']
    _ws(wb, 'Summer 2027 transfers', list(sm.columns), sm.values.tolist(), [6, 9, 9, 13, 13, 13, 16, 14])
    fc = G['forecast_rows']
    _ws(wb, '2027 forecast', list(fc.columns), fc.values.tolist(), [6, 9, 12, 12, 12, 12, 14])
    notes = [['As of', 'Extracts of 1 to 3 November 2026; 2026 is January to October.'],
             ['Avoided', 'MPUC order E-999/CI-23-412 para. 2: sustained interruptions customers would have had without '
                         'automatic restoration, less those they had; all days.'],
             ['Sustained', 'Five minutes or longer from the first loss of supply (para. 3): the lockout device\'s first '
                           'trip in the device events.'],
             ['Customers', 'From the outage record\'s automatic steps; the loop configuration\'s sections where the '
                           'outage record has no step (Oct 2024 relocations applied by date).'],
             ['Forecast', 'Lockouts at the average annual rate since 1 Jan 2022 (para. 5); 4,000 simulated years for '
                          'the 80 per cent range.']]
    _ws(wb, 'Notes', ['Item', 'Basis'], notes, [14, 110])
    wb.save(path)
    a, b = C.GOLD_STAMP['xlsx']
    PP.normalize_ooxml(path, C.PEOPLE['da_engineer'], C.PEOPLE['da_engineer'], C.utc_z(a), C.utc_z(b),
                       title='FLISR review 2026', excel=True, company=C.ORG)


def memo(path, G):
    import officepdf as OP
    br = G['bridge']
    P = lambda t, st=BODY: Paragraph(t, st)
    bat = G['rebattery']
    sets = G['summer_set']
    fc = G['forecast']
    restored5 = G['years'][2026]['restored_5']
    work = [[Paragraph(x, CELL) for x in r] for r in [
        ['2026 (Jan to Oct)', 'Customer interruptions'],
        ['Restored within five minutes of the first loss of supply', fmt(restored5)],
        ['Restorations undone by a receiving recloser trip', '-' + fmt(br['reinterrupted'])],
        ['Receiving feeders\' own customers interrupted', '-' + fmt(br['recv_trips_own'] + br['closes_own'])],
        ['Avoided, order para. 2', fmt(br['net'])]]]
    story = [
        P('%s, Grid Modernization' % C.ORG_SHORT, TITLE),
        P('Re-battery %d controls before December and reset the receiving reclosers before June' % len(bat), HEAD),
        P('To: %s, %s. From: %s. %s' % (C.PEOPLE['gm_perf'], C.PEOPLE['regulatory'], C.PEOPLE['da_engineer'],
                                        dt.date(2026, 11, 11).strftime('%d %B %Y').lstrip('0'))),
        P('<b>Bottom line.</b> Replace the batteries in %d recloser controls before December. Before June, move the '
          'receiving reclosers on the transfer directions the ADMS does not switch to settings that carry a transfer, '
          'rather than waiting for the four reinforcements. Run as they stand, the loops should avoid about %s '
          'sustained customer interruptions in 2027 (80 per cent range %s to %s); from January to October 2026 they '
          'avoided %s on the order\'s definition.' % (len(bat), fmt(fc['mean']), fmt(fc['p10']), fmt(fc['p90']),
                                                       fmt(br['net']))),
        P('1. Before this winter: batteries', HEAD),
        P('A control on a dead line trips and closes on its battery, drawing 30 A, and stops below 21.2 V. The '
          'weekly load tests run at 5 A, and the annual functional tests run on line power, so neither shows how a '
          'weak battery behaves at -27 C. Fitting each battery\'s resistance to the temperature of its test hour and '
          'its age, and carrying it to -27 C at the end of February, the following would not operate: %s.' %
          ', '.join(bat)),
        P('2. Before next summer: transfer settings', HEAD),
        P('On the directions whose receiving controls the ADMS does not move to group 2 (CTL-4C controls), the '
          'combined load can trip the receiving recloser after a transfer, with no fault found; operators switching '
          'the same transfers set group 2 first. Replaying the 2025 and 2026 summer loads at the hours the loops\' '
          'lockouts strike, transfers in June to September 2027 would interrupt about %s of the receiving feeders\' '
          'own customers if the settings stand. The four reconductoring projects would remove part of that, but the '
          'capital works record puts comparable projects a median %.1f months late. Directions to change: %s.' %
          (fmt(G['summer_total']), G['slip_median'], sets)),
        P('3. 2026 on the commission\'s definition', HEAD),
        Table(work, colWidths=[300, 120]),
        P('Sources: SCADA device events, OMS, ADMS FLISR archive; customers from the outage record\'s steps.',
          ParagraphStyle('src', parent=BODY, fontSize=8, leading=10)),
        P('The event archive drops events when its queue overflows in storms, and the front end ran so slowly then '
          'that none of those restorations came inside five minutes; the device record shows what the scheme did. '
          'The vendor dashboard counts completed sequences in the archive whatever their duration.'),
        P('4. 2027 as the loops stand', HEAD),
        P('At the record\'s average rate of lockouts since January 2022, with the scheme\'s own success rate, the '
          'batteries and the transfer trips as they stand and the reinforcements at their likely dates: about %s '
          'customer interruptions avoided, 80 per cent range %s to %s. The workbook carries every figure and its '
          'working.' % (fmt(fc['mean']), fmt(fc['p10']), fmt(fc['p90']))),
    ]
    a, b = C.GOLD_STAMP['memo']
    OP.build(path, story, title='FLISR performance 2026 and 2027 outlook', author=C.PEOPLE['da_engineer'],
             subject='Grid modernization filing', footer=C.ORG_SHORT + ' Grid Modernization, internal',
             created=C.local(a), modified=C.local(b), font='Liberation Sans', body_pt=9.6, page_mm=C.LETTER_MM)
