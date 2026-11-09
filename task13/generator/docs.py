"""The pack's office files in their issuers' genres: the network's feeder register, the vegetation cycle log, the
reliability reporting standard, the 2027 catch-up's programme terms, the tree notices register and the vegetation
contractor's 2027 schedule of rates. Workbooks are written and then saved in Excel's own form
(postprocess.normalize_ooxml); documents are laid out by the house writer's Word stage (officepdf) and saved in
Word's own form (postprocess.normalize_docx)."""
import hashlib

import numpy as np
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

import common as C
import pack as P
import postprocess as PP
import world as W

BODY = ParagraphStyle('body', fontName='Helvetica', fontSize=10, leading=13.2, spaceAfter=6)
SMALL = ParagraphStyle('small', parent=BODY, fontSize=8.6, leading=11, spaceAfter=3)
HEAD = ParagraphStyle('head', parent=BODY, fontName='Helvetica-Bold', fontSize=11, spaceBefore=7, spaceAfter=4)
TITLE = ParagraphStyle('title', parent=BODY, fontName='Helvetica-Bold', fontSize=15, leading=18, spaceAfter=3)
CELL = ParagraphStyle('cell', fontName='Helvetica', fontSize=8.8, leading=10.8)
CELLB = ParagraphStyle('cellb', parent=CELL, fontName='Helvetica-Bold')

DISTRICT = {'PBY': 'Paua Bay', 'WTK': 'Waitaki Road', 'HRK': 'Harakeke', 'MTR': 'Mataroa', 'RNG': 'Mataroa',
            'OKR': 'Okere', 'KWH': 'Kowhai', 'TOT': 'Totara Gully', 'TIT': 'Titi', 'MKR': 'Makora'}


def _stamps(key):
    a, b = C.STAMP[key]
    return C.utc_z(a), C.utc_z(b)


def _xlsx(path, sheets, key, title, author, company):
    """sheets: list of (name, header lines, rows, column widths, number formats by column letter)."""
    wb = Workbook()
    wb.remove(wb.active)
    for name, heads, rows, widths, fmts in sheets:
        ws = wb.create_sheet(name)
        r = 1
        for h in heads:
            ws.cell(row=r, column=1, value=h).font = Font(bold=(r == 1), size=11 if r == 1 else 9)
            r += 1
        if heads:
            r += 1
        top = r
        for k, row in enumerate(rows):
            for j, v in enumerate(row):
                c = ws.cell(row=r, column=j + 1, value=v)
                if k == 0:
                    c.font = Font(bold=True)
                    c.fill = PatternFill('solid', fgColor='DCE6F0')
                    c.alignment = Alignment(wrap_text=True, vertical='top')
                else:
                    f = fmts.get(chr(65 + j))
                    if f:
                        c.number_format = f
            r += 1
        for j, wdt in enumerate(widths):
            ws.column_dimensions[chr(65 + j)].width = wdt
        ws.freeze_panes = ws.cell(row=top + 1, column=1)
    wb.save(path)
    cr, md = _stamps(key)
    PP.normalize_ooxml(path, author, author, cr, md, title=title, excel=True, company=company)


def _docx(path, story, key, title, author, company, footer):
    """the issuer's document as its word processor saves it (the house writer's Word stage, then Word's own form)"""
    from docx import Document
    from docx.enum.text import WD_BREAK
    from docx.shared import Mm, Pt, RGBColor
    from reportlab.platypus import KeepTogether, PageBreak
    import officepdf as OP
    OP.FONT = 'Calibri'
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Mm(210), Mm(297)
    sec.left_margin = sec.right_margin = Mm(22)
    sec.top_margin, sec.bottom_margin = Mm(20), Mm(20)
    normal = doc.styles['Normal']
    normal.font.name = OP.FONT
    normal.font.size = Pt(10)
    for fl in story:
        if isinstance(fl, Paragraph):
            OP._paragraph(doc, fl)
        elif isinstance(fl, Table):
            OP._table(doc, fl)
        elif isinstance(fl, KeepTogether):
            OP._keep(doc, fl._content)
        elif isinstance(fl, Spacer):
            sp = doc.add_paragraph()
            sp.paragraph_format.space_after = Pt(0)
            sp.paragraph_format.line_spacing = Pt(max(1, fl.height))
        elif isinstance(fl, PageBreak):
            doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
    fp = sec.footer.paragraphs[0]
    r = fp.add_run(footer)
    r.font.name = OP.FONT
    r.font.size = Pt(8)
    r.font.color.rgb = RGBColor.from_string('555555')
    OP._page_field(fp)
    cp = doc.core_properties
    cp.title, cp.author, cp.last_modified_by = title, author, author
    cp.revision = 1
    doc.save(path)
    seed = int(hashlib.blake2b(title.encode(), digest_size=4).hexdigest(), 16)
    cr, md = _stamps(key)
    PP.normalize_docx(path, author, author, cr, md, 3 + seed % 5, 31 + seed % 60, seed, title=title, company=company)


def _tbl(rows, widths):
    data = [[Paragraph(str(x), CELLB if k == 0 else CELL) for x in r] for k, r in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LINEBELOW', (0, 0), (-1, 0), 0.7, colors.black),
                           ('TOPPADDING', (0, 0), (-1, -1), 2), ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
                           ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0.86, 0.9, 0.94))]))
    return t


# ------------------------------------------------------------------ the feeder register
def write_feeders(S, path, icps):
    """icps: each feeder's ICPs at 31 October 2026 as the registry counts them"""
    F = S['F'].sort_values('feeder')
    rng = np.random.default_rng(W.SEED + 720)
    cust = icps
    rows = [['Feeder', 'Former code', 'Zone substation', 'District', 'Voltage (kV)', 'Overhead (km)', 'Underground (km)',
             'ICPs (31 Oct 2026)', 'Commissioned', 'Vegetation cycle (years)', 'Notes']]
    for _, r in F.iterrows():
        fc = P.old_feeder_code(r['feeder'])
        note = ''
        if r['feeder'].startswith('RNG-'):
            note = 'Renamed at the Rangiora Street rebuild, August 2023'
        rows.append([r['feeder'], fc if fc != r['feeder'] else '', r['zone'], DISTRICT[r['zone']], 11, float(r['km']),
                     float(r['ug_km']), int(cust[r['feeder']]), int(r['age']), int(r['cycle']), note])
    zrows = [['Code', 'Zone substation', 'Latitude', 'Longitude', 'Commissioned', 'Transformers (MVA)']]
    for z in W.ZONES:
        zrows.append([z[0], z[1], z[2], z[3], int(rng.integers(1958, 1990)) if z[0] != 'RNG' else 2023,
                      ['2 x 5', '2 x 7.5', '1 x 10', '2 x 10'][int(rng.integers(0, 4))]])
    heads = ['Kotuku Networks: 11 kV feeder register', 'Network Planning. Kept current to 28 July 2026; ICPs from the '
             'registry at 31 October 2026. Coordinates WGS84.']
    _xlsx(path, [('Feeders', heads, rows, [10, 12, 15, 15, 11, 12, 14, 15, 13, 14, 44],
                  {'F': '0.0', 'G': '0.0', 'H': '#,##0'}),
                 ('Zone substations', ['Zone substations'], zrows, [8, 18, 11, 11, 13, 17], {'C': '0.000', 'D': '0.000'})],
          'feeders', '11 kV feeder register', 'Network Planning', C.ORG)
    return len(rows) - 1


# ------------------------------------------------------------------ the vegetation cycle log
def cycle_jobs(S):
    rng = np.random.default_rng(W.SEED + 730)
    jobs = []
    for f in sorted(S['F']['feeder']):
        for d in S['trims'][f]:
            d = pd.Timestamp(d)
            if d < pd.Timestamp('2014-01-01'):
                continue
            jobs.append((d, f))
    jobs.sort()
    km = dict(zip(S['F']['feeder'], S['F']['km']))
    tau = dict(zip(S['F']['feeder'], S['F']['tau']))
    out = []
    count = {}
    for d, f in jobs:
        y = d.year
        count[y] = count.get(y, 0) + 1
        start = d - pd.Timedelta(days=int(rng.integers(18, 60)))
        closed = d + pd.Timedelta(days=int(rng.integers(12, 75)))
        if closed > pd.Timestamp('2026-10-30'):
            closed = None
        spans = int(round(km[f] * rng.uniform(11.5, 13.5)))
        cut = int(round(spans * min(0.95, 0.18 + 0.12 * tau[f] * rng.uniform(0.85, 1.15))))
        contractor = 'Ridgeline Arborists' if d >= pd.Timestamp('2018-07-01') else 'Totara Tree Services'
        out.append(dict(job='VM-%d-%03d' % (y, count[y]), feeder=f, start=start, finish=d, closed=closed, spans=spans,
                        cut=cut, km=round(km[f] * rng.uniform(0.92, 1.0), 1), contractor=contractor))
    return out


def write_vegcycle(S, path):
    rows = [['Job', 'Feeder', 'Crew started', 'Crew finished', 'Job closed', 'Spans inspected', 'Spans cut',
             'Corridor km', 'Contractor', 'Comments']]
    rng = np.random.default_rng(W.SEED + 731)
    comments = ['', '', '', 'Access by landowner arrangement', 'Traffic management on state highway spans',
                'Hazard trees outside corridor referred for notice', 'Two spans deferred to landowner works',
                'Wet weather delays', '']
    for j in cycle_jobs(S):
        rows.append([j['job'], j['feeder'], j['start'].to_pydatetime(), j['finish'].to_pydatetime(),
                     j['closed'].to_pydatetime() if j['closed'] is not None else None, j['spans'], j['cut'], j['km'],
                     j['contractor'], comments[int(rng.integers(0, len(comments)))]])
    heads = ['Vegetation management: cycle trim jobs', 'Kept by %s, Vegetation Manager. A job is closed once the '
             'audit of the finished spans is signed off.' % C.PEOPLE['veg_manager']]
    _xlsx(path, [('Cycle jobs', heads, rows, [13, 9, 13, 13, 13, 9, 9, 10, 20, 44],
                  {'C': 'dd/mm/yyyy', 'D': 'dd/mm/yyyy', 'E': 'dd/mm/yyyy', 'H': '0.0'})],
          'vegcycle', 'Vegetation cycle log', C.PEOPLE['veg_manager'], C.ORG)
    return len(rows) - 1


# ------------------------------------------------------------------ the tree notices register
def write_notices(S, path):
    rng = np.random.default_rng(W.SEED + 740)
    F = S['F']
    weight = (F['km'] * np.sqrt(F['tau'])).values
    weight = weight / weight.sum()
    types = ['Hazard warning notice', 'Cut or trim notice', 'Cut or trim notice', 'No-interest notice']
    resp = ['Owner to trim', 'Owner declared no interest', 'Network to trim at owner cost', 'Disputed', 'Owner to trim']
    rows = [['Notice', 'Feeder', 'Pole or span', 'Notice type', 'Issued', 'Owner response', 'Works due', 'Status', 'Closed']]
    n = 0
    for d in pd.date_range('2024-01-08', '2026-10-16', freq='D'):
        if d.dayofweek >= 5:
            continue
        for _ in range(int(rng.poisson(0.42))):
            n += 1
            f = F['feeder'].iloc[int(rng.choice(len(F), p=weight))]
            due = d + pd.Timedelta(days=int(rng.choice([20, 40, 60])))
            closed = due + pd.Timedelta(days=int(rng.integers(-15, 90)))
            open_ = closed > pd.Timestamp('2026-10-21') or rng.random() < 0.06
            rows.append(['THN-%05d' % (4100 + n), f, 'P%04d' % int(rng.integers(1, 3800)), types[int(rng.integers(0, 4))],
                         d.to_pydatetime(), resp[int(rng.integers(0, len(resp)))], due.to_pydatetime(),
                         'Open' if open_ else 'Closed', None if open_ else closed.to_pydatetime()])
    heads = ['Electricity (Hazards from Trees) Regulations 2003: notices issued', 'Vegetation team register, '
             'January 2024 to October 2026']
    _xlsx(path, [('Notices', heads, rows, [12, 9, 11, 22, 12, 28, 12, 9, 12],
                  {'E': 'dd/mm/yyyy', 'G': 'dd/mm/yyyy', 'I': 'dd/mm/yyyy'})],
          'notices', 'Tree notices register', C.PEOPLE['veg_manager'], C.ORG)
    return len(rows) - 1


# ------------------------------------------------------------------ the reliability reporting standard
def boundary_table(S, E):
    bounds, _ = W.boundary_values(E, S['F'])
    return {k: (round(v[0], 2), round(v[1], 4)) for k, v in bounds.items()}


def write_standard(path, B):
    st = [Paragraph('Reliability Reporting Standard', TITLE),
          Paragraph('Kotuku Networks Limited  |  Regulatory  |  Version 4, approved 8 April 2026', SMALL),
          Paragraph('Owner: %s, Regulatory Manager' % C.PEOPLE['regulatory_mgr'], SMALL), Spacer(1, 6)]
    sections = [
        ('1. Purpose and scope', [
            'This standard sets how Kotuku Networks records, counts and reports interruptions to supply on its '
            'distribution network, for its information disclosures, its reporting against the default price-quality '
            'path, and its internal reporting by feeder. It applies to every interruption recorded in the outage '
            'management system (OMS).']),
        ('2. Definitions', [
            '(a) An interruption is a loss of supply to one or more ICPs caused by the operation of a protective device '
            'or by switching on the network.',
            '(b) A sustained interruption lasts 1 minute or longer. A shorter interruption is momentary and is not '
            'counted in SAIDI or SAIFI.',
            '(c) A planned interruption is one notified to the affected customers at least four working days ahead. '
            'Every other interruption is unplanned.',
            '(d) The customers interrupted by an interruption are the ICPs downstream of the device that operated, as '
            'the OMS records them. Customer interruptions are the sum of customers interrupted; customer minutes are '
            'customers interrupted times the duration of the interruption.',
            '(e) The regulatory year runs from 1 April to 31 March. Days are New Zealand calendar days in local time, '
            'and the OMS records times in local time.',
            '(f) SAIDI and SAIFI for a period are the customer minutes and the customer interruptions of the period '
            'divided by the average number of ICPs connected over the regulatory year, taken as the mean of the '
            'month-end ICP counts. For a regulatory year not yet complete, the latest month-end count is used.']),
        ('3. Counting', [
            '(a) An interruption is counted once for each operation of a protective device.',
            '(b) The OMS takes records from SCADA, from the field crew and from the call centre. Where one operation has '
            'been recorded from more than one source, it is one interruption, and the SCADA or field crew record gives '
            'its times and its customers interrupted.']),
        ('4. Causes', [
            'Each unplanned interruption carries one cause. The OMS cause codes changed on 1 October 2023; both sets '
            'are shown.']),
        ('5. Major event days', [
            '(a) A major event day is a day on which the unplanned SAIDI for the day, or the unplanned SAIFI for the '
            'day, exceeds the boundary value of the price-quality path in force on that day. Daily SAIDI and SAIFI '
            'count sustained unplanned interruptions starting on the day.',
            '(b) The boundary values are those set for Kotuku Networks by the Commerce Commission:']),
        ('6. Reporting by feeder', [
            'Reliability is reported for each feeder, and for each cause, with the interruptions starting on major '
            'event days excluded. Feeder figures use the same counting and the same customers interrupted as the '
            'network figures.']),
    ]
    for head, paras in sections:
        st.append(Paragraph(head, HEAD))
        for p in paras:
            st.append(Paragraph(p, BODY))
        if head.startswith('4.'):
            st.append(_tbl([['Cause', 'Code to 30 September 2023', 'Code from 1 October 2023', 'Covers'],
                            ['Vegetation', 'VEG', 'TREE', 'Trees and other vegetation contacting or falling onto lines'],
                            ['Defective equipment', 'EQP', 'EQUIP', 'Failure of network equipment'],
                            ['Wildlife', 'ANI', 'ANIMAL', 'Birds, possums and other animals'],
                            ['Third party', 'VEH', 'THIRD-PARTY', 'Vehicles, excavation and other third-party damage'],
                            ['Adverse weather', 'WTH', 'WEATHER', 'Wind, snow and debris other than vegetation'],
                            ['Lightning', 'LGT', 'LIGHTNING', 'Lightning strikes'],
                            ['Unknown', 'UNK', 'UNKNOWN', 'No cause found after patrol'],
                            ['Planned', 'PLN', 'PLANNED', 'Planned interruptions']], [90, 85, 85, 200]))
            st.append(Spacer(1, 4))
        if head.startswith('5.'):
            st.append(_tbl([['Path', 'In force', 'SAIDI boundary value (minutes)', 'SAIFI boundary value (interruptions)'],
                            ['DPP3', '1 April 2020 to 31 March 2025', '%.2f' % B['DPP3'][0], '%.4f' % B['DPP3'][1]],
                            ['DPP4', 'From 1 April 2025', '%.2f' % B['DPP4'][0], '%.4f' % B['DPP4'][1]]],
                           [45, 140, 130, 145]))
            st.append(Spacer(1, 4))
    st.append(Spacer(1, 6))
    st.append(Paragraph('Version history: version 1 issued March 2023; version 2 August 2023, the October 2023 cause '
                        'codes; version 3 May 2025, DPP4 boundary values; version 4 April 2026, the counting rules '
                        'for call centre records.', SMALL))
    _docx(path, st, 'standard', 'Reliability Reporting Standard', C.PEOPLE['regulatory_mgr'], C.ORG,
          'Kotuku Networks Reliability Reporting Standard v4. Internal.   Page ')


# ------------------------------------------------------------------ the 2027 catch-up's programme terms
PROGRAMME = [
    ('1. Purpose', [
        'The 2027 vegetation catch-up is one season of corridor work on six 11 kV feeders, on top of the cycle '
        'programme. It is carried in the asset management plan Kotuku Networks discloses before 1 April 2027, and the '
        'board approves the six feeders at its November 2026 meeting.']),
    ('2. The work', [
        '(a) On each of the six feeders, Ridgeline Arborists’ crews trim the corridor of every overhead span back to '
        'the clearance a cycle trim leaves, to the cycle programme’s specification.',
        '(b) Every span on the six feeders is finished by 31 March 2027.',
        '(c) A feeder’s next cycle trim falls due from the date the catch-up finished on it.',
        '(d) Ridgeline’s crews carry the catch-up from November 2026, and the cycle programme resumes on 1 April 2028. '
        'No feeder has a cycle trim between the end of October 2026 and 31 March 2028 other than the catch-up.']),
    ('3. What the catch-up is judged on', [
        '(a) The catch-up is judged on the sustained customer interruptions caused by vegetation that it avoids in the '
        '2027-28 regulatory year, 1 April 2027 to 31 March 2028.',
        '(b) Interruptions are counted as the Reliability Reporting Standard counts them: sustained, unplanned and '
        'caused by vegetation, with the customers interrupted that the OMS records at the device that operated, on days '
        'that are not major event days.',
        '(c) The interruptions the catch-up avoids on a feeder are the difference between the vegetation customer '
        'interruptions the feeder can be expected to have in 2027-28 with its corridor left as it stands, and those it '
        'can be expected to have with its corridor as the catch-up leaves it.',
        '(d) The six feeders are the six on which the catch-up avoids the most.']),
    ('4. Eligibility', [
        'Every 11 kV feeder Kotuku Networks operates is eligible. A feeder is in the catch-up or out of it as a whole.']),
    ('5. Reporting', [
        'The asset management plan names the six feeders and states the customer interruptions the catch-up is expected '
        'to avoid on each, in total, and as network SAIFI on the ICPs connected at the latest month-end.']),
]


def write_programme(path):
    st = [Paragraph('2027 Vegetation Catch-up: Programme Terms', TITLE),
          Paragraph('Kotuku Networks Limited  |  Network Operations  |  14 October 2026', SMALL),
          Paragraph('Approved by %s, General Manager Network. Prepared with %s, Vegetation Manager.'
                    % (C.PEOPLE['network_gm'], C.PEOPLE['veg_manager']), SMALL), Spacer(1, 6)]
    for head, paras in PROGRAMME:
        st.append(Paragraph(head, HEAD))
        for p in paras:
            st.append(Paragraph(p, BODY))
    _docx(path, st, 'programme', '2027 Vegetation Catch-up: Programme Terms', C.PEOPLE['network_gm'], C.ORG,
          'Kotuku Networks. 2027 vegetation catch-up programme terms. Board in confidence.   Page ')
    return [p for _, ps in PROGRAMME for p in ps]


# ------------------------------------------------------------------ the contractor's 2027 schedule of rates
def write_rates(path):
    st = [Paragraph('Schedule of Rates 2027: Vegetation Management', TITLE),
          Paragraph('%s for Kotuku Networks Limited  |  Rates valid 1 January to 31 December 2027' % C.CONTRACTOR, SMALL),
          Paragraph('Prepared by %s, Contracts Supervisor, 30 September 2026' % C.PEOPLE['contractor'], SMALL),
          Spacer(1, 6),
          Paragraph('1. Corridor trimming', HEAD),
          Paragraph('Rates are per overhead span inspected and trimmed to the cycle specification, including cut and '
                    'chip, and are set by the terrain class of the span.', BODY),
          _tbl([['Terrain class', 'Rate per span (NZD, excl. GST)', 'Typical spans per crew day'],
                ['Urban and township', '182.00', '14'], ['Rural flat', '96.50', '26'],
                ['Rural hill', '148.00', '17'], ['Plantation edge', '211.00', '11'],
                ['Bush and scrub', '173.50', '13']], [150, 160, 150]),
          Spacer(1, 4),
          Paragraph('2. Hazard trees and extras', HEAD),
          _tbl([['Item', 'Unit', 'Rate (NZD, excl. GST)'],
                ['Hazard tree felling, trees outside the corridor (by notice)', 'per tree', '640.00'],
                ['Elevated work platform', 'per hour', '165.00'],
                ['Traffic management, level 1 road', 'per day', '890.00'],
                ['Traffic management, state highway', 'per day', '1,940.00'],
                ['Emergency call-out (storm response), crew of three', 'per hour', '412.00'],
                ['Chipping and removal of cut material', 'per load', '95.00']], [260, 80, 120]),
          Spacer(1, 4),
          Paragraph('3. Terms', HEAD),
          Paragraph('Rates are fixed for work ordered and completed in 2027. Work carried into 2028 is charged at the '
                    '2028 schedule. Storm response is charged at the call-out rate from the time the crew is mobilised. '
                    'Spans the crew cannot reach because of landowner access are recorded and charged at the inspection '
                    'rate of 38.00 per span.', BODY)]
    _docx(path, st, 'rates', 'Schedule of Rates 2027: Vegetation Management', C.PEOPLE['contractor'], C.CONTRACTOR,
          'Ridgeline Arborists Limited. Schedule of rates 2027. Commercial in confidence.   Page ')
