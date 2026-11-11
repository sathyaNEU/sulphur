"""The pack's office files in their issuers' genres: the protection zones register, the cyclic line inspection log, the
stores' transformer replacement register, the 2027 refit's programme terms, the line inspection procedure (a PDF the
technical services department exported from Word) and a supplier's materials quotation. Workbooks are written and then
saved in Excel's own form (postprocess.normalize_ooxml); documents are laid out by the house writer's Word stage
(officepdf) and saved in Word's own form (postprocess.normalize_docx)."""
import hashlib

import numpy as np
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

import common as C
import postprocess as PP

BODY = ParagraphStyle('body', fontName='Helvetica', fontSize=10, leading=13.2, spaceAfter=6)
SMALL = ParagraphStyle('small', parent=BODY, fontSize=8.6, leading=11, spaceAfter=3)
HEAD = ParagraphStyle('head', parent=BODY, fontName='Helvetica-Bold', fontSize=11, spaceBefore=7, spaceAfter=4)
TITLE = ParagraphStyle('title', parent=BODY, fontName='Helvetica-Bold', fontSize=15, leading=18, spaceAfter=3)
CELL = ParagraphStyle('cell', fontName='Helvetica', fontSize=8.8, leading=10.8)
CELLB = ParagraphStyle('cellb', parent=CELL, fontName='Helvetica-Bold')


def _stamps(key):
    a, b = C.STAMP[key]
    return C.utc_z(a), C.utc_z(b)


def _col(j):
    s = ''
    j += 1
    while j:
        j, r = divmod(j - 1, 26)
        s = chr(65 + r) + s
    return s


def _xlsx(path, sheets, key, title, author, company):
    """sheets: list of (name, header lines, rows, column widths, number formats by column index)."""
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
                    f = fmts.get(j)
                    if f:
                        c.number_format = f
            r += 1
        for j, wdt in enumerate(widths):
            ws.column_dimensions[_col(j)].width = wdt
        ws.freeze_panes = ws.cell(row=top + 1, column=1)
    wb.save(path)
    cr, md = _stamps(key)
    PP.normalize_ooxml(path, author, author, cr, md, title=title, excel=True, company=company)


def _docx(path, story, key, title, author, company, footer):
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


# ------------------------------------------------------------------ the protection zones register
def write_zones(w, path):
    Z = w['Z'].sort_values(['sub', 'feeder_ix', 'order'])
    model = {'relay': 'Feeder protection relay', 'new': 'Recloser control NX-20', 'old': 'Recloser control NX-10'}
    rows = [['Zone (protective device)', 'Feeder', 'Substation', 'Equipment', 'Control', 'Telemetry', 'In service',
             'Upstream device', 'Overhead line km, three-phase', 'Overhead line km, single-phase',
             'km wood crossarm', 'km steel crossarm', 'km pole-top bracket', 'km bracket on concrete pole',
             'km open field', 'km tree-lined', 'km town', 'km hill',
             'km fitted with line arresters (2017-18 programme)', 'Line arresters', 'Distribution transformers',
             'Member-consumers']]
    subname = dict(C.SUBSTATIONS)
    for z in Z.itertuples():
        rows.append([z.zone, z.feeder, subname[z.sub_code], 'Feeder breaker' if z.kind == 'breaker' else 'Line recloser',
                     model[z.controller], 'SCADA (radio)' if (z.telemetry == 'SCADA' and z.controller != 'relay') else
                     ('SCADA (substation RTU)' if z.controller == 'relay' else 'None, read on site'),
                     int(z.commissioned), z.parent or '', round(z.km3, 2), round(z.km1, 2),
                     round(z.km_wood_xarm, 2), round(z.km_steel_xarm, 2), round(z.km_bracket, 2), round(z.km_concrete_bracket, 2),
                     round(z.km_open, 2), round(z.km_treed, 2), round(z.km_town, 2), round(z.km_hill, 2),
                     round(z.km_prot, 2), int(z.n_la), int(z.n_tx), int(z.members)])
    subs = [['Code', 'Substation', 'Transformer', 'Feeders']]
    mva = {0: '10 MVA', 1: '10 MVA', 2: '15 MVA', 3: '5 MVA', 4: '10 MVA', 5: '10 MVA', 6: '5 MVA', 7: '10 MVA',
           8: '15 MVA', 9: '10 MVA', 10: '5 MVA', 11: '10 MVA'}
    for i, (code, name) in enumerate(C.SUBSTATIONS):
        subs.append([code, name, '69/13.2 kV, ' + mva[i], int(w['Z'][w['Z'].sub_code == code].feeder.nunique())])
    heads = ['%s: protection zones register' % C.ORG, 'Technical Services Department. One row per breaker or line '
             'recloser: the overhead line it clears up to the next recloser downstream. Revised 17 September 2026.']
    fm = {j: '0.00' for j in range(8, 19)}
    _xlsx(path, [('Zones', heads, rows, [16, 10, 13, 15, 22, 18, 9, 14] + [11] * 11 + [12, 12, 12], fm),
                 ('Substations', [], subs, [8, 16, 18, 9], {})],
          'zones', 'Protection zones register', C.PEOPLE['tsd_manager'], C.ORG)
    return len(rows) - 1


# ------------------------------------------------------------------ the cyclic line inspection log
def write_inspections(w, path):
    I = w['I'].copy()
    Fi = w['Fi'].copy()
    Z = w['Z'].set_index('zone_ix')
    rng = np.random.default_rng(C.SEED + 501)
    F = Fi.set_index(['zone_ix', 'round'])
    rows = [['Round', 'Zone', 'Inspection start', 'Inspection end', 'Team', 'Transformer structures',
             'Line arrester structures', 'Ground leads missing or cut', 'Arresters failed', 'Pin insulators cracked',
             'Leaning poles', 'Spans with vegetation', 'Repairs completed', 'Remarks']]
    teams = ['Team %d' % k for k in range(1, 5)]
    for r in I.sort_values(['round', 'start', 'zone_ix']).itertuples():
        z = Z.loc[r.zone_ix]
        f = F.loc[(r.zone_ix, r.round)] if (r.zone_ix, r.round) in F.index else None
        gm = int(f.grounds_missing) if f is not None else 0
        af = int(f.arresters_failed) if f is not None else 0
        ic = int(f.insulators_cracked) if f is not None else 0
        lean = int(rng.poisson(0.05 * z.km))
        veg = int(rng.poisson(0.18 * z.km * (0.5 + min(z.veg, 3))))
        rem = []
        if gm:
            rem.append('ground leads replaced')
        if af:
            rem.append('arresters replaced')
        if ic:
            rem.append('pin insulators replaced')
        if lean:
            rem.append('poles straightened')
        rep = (r.end + pd.Timedelta(days=int(rng.integers(0, 3)))).strftime('%Y-%m-%d')
        rows.append(['%d-%02d' % (r.round, (r.round + 1) % 100), z.zone, r.start.strftime('%Y-%m-%d'),
                     r.end.strftime('%Y-%m-%d'), rng.choice(teams), int(z.n_tx), int(z.n_la), gm, af, ic, lean, veg, rep,
                     '; '.join(rem).capitalize() if rem else 'No defects requiring work'])
    heads = ['Cyclic line inspection log', 'Line Inspection Section, %s Kept by %s.' % (C.ORG, C.PEOPLE['inspection'])]
    _xlsx(path, [('Inspections', heads, rows, [9, 15, 12, 12, 8, 12, 12, 12, 10, 11, 9, 10, 12, 40], {})],
          'inspections', 'Cyclic line inspection log', C.PEOPLE['inspection'], C.ORG)
    return len(rows) - 1


# ------------------------------------------------------------------ the stores' transformer replacement register
def write_transformers(w, path):
    B = w['B']
    Z = w['Z'].set_index('zone_ix')
    rng = np.random.default_rng(C.SEED + 502)
    rows = [['W.O. No.', 'Date replaced', 'Feeder', 'Zone', 'DT No.', 'kVA', 'Reason recorded']]
    reason = {'lightning': ['Burnt', 'Burnt', 'Burnt (lightning)'], 'overload': ['Overloaded', 'Burnt'],
              'age': ['Old/defective', 'Burnt'], 'oil': ['Leaking']}
    for k, b in enumerate(B.sort_values('t').itertuples()):
        d = b.t + pd.Timedelta(days=float(rng.uniform(0.3, 3.5)))
        rows.append(['WO-%d-%04d' % (d.year, 1000 + k), d.strftime('%Y-%m-%d'), Z.feeder[b.zone_ix], Z.zone[b.zone_ix],
                     'DT-%05d' % rng.integers(10000, 99999), int(rng.choice([10, 15, 25, 37.5, 50], p=[0.2, 0.3, 0.3, 0.1, 0.1]) if True else 0),
                     rng.choice(reason[b.reason])])
    heads = ['Distribution transformer replacements', 'Stores and Materials. One row per transformer issued to replace one in '
             'service.']
    _xlsx(path, [('Replacements', heads, rows, [14, 12, 9, 15, 10, 6, 18], {})], 'transformers',
          'Distribution transformer replacements', C.PEOPLE['materials'], C.ORG)
    return len(rows) - 1


# ------------------------------------------------------------------ the 2027 refit's programme terms
TERMS = [
    ('1. Purpose', [
        'The 2027 Lightning Protection Refit restores the lightning protection of the overhead protection zones where '
        'it has failed, in the 2026-27 dry season, before the 2027 lightning season. The zones are those named by the '
        'referral rule in section 3, which the Technical Services Department will also run after every lightning season '
        'from 2027 on.']),
    ('2. Terms used', [
        '(a) A protection zone is the overhead line a feeder breaker or line recloser clears, up to the next line recloser '
        'downstream, as listed in the protection zones register.',
        '(b) The lightning season runs from 1 April to 31 October of each year.',
        '(c) A lightning fault is a fault started by a lightning flash on a zone\'s lines. It is counted once, against the '
        'zone whose lines it was on, however many times breakers or reclosers trip and reclose on it.',
        '(d) A zone\'s lightning protection is sound when its ground leads, its line and transformer arresters and its pin '
        'insulators are as the Cooperative\'s construction standard has them. Failed protection is any departure from that: '
        'a missing or cut ground lead, a failed arrester, a cracked or punctured pin insulator.',
        '(e) A zone\'s record since its last cyclic inspection runs from the day after the inspection\'s repairs were '
        'completed to the end of the lightning season the rule is run after.',
        '(f) The lightning faults failed protection caused in a season are the network\'s lightning faults in that season '
        'less the lightning faults its lines would have had in it with every zone\'s protection sound.',
        '(g) The lightning near a zone\'s lines is the ground strokes the lightning location service placed within 400 m '
        'of them.']),
    ('3. The referral rule', [
        '(a) After each lightning season the rule refers every zone whose lightning faults since its last cyclic '
        'inspection are more than its lines would have had with sound protection, under the lightning that fell near '
        'them, by more than chance explains.',
        '(b) Across the network, the rule may refer a zone whose protection is sound no more than once in five lightning '
        'seasons on average.']),
    ('4. The 2027 refit', [
        '(a) The refit covers every zone the rule refers after the 2026 lightning season.',
        '(b) On each zone it covers, the refit restores every ground lead, arrester and pin insulator to the construction '
        'standard.',
        '(c) The lightning faults the refit avoids are the faults its zones run above what sound protection would give '
        'them, taken in a season with the lightning of an average of the 2022 to 2026 lightning seasons.']),
    ('5. Checking the rule', [
        'Each cyclic inspection checks the rule on the zone it inspects, against the rule as run after the lightning '
        'season before the inspection. The inspection confirms a referral when the rule referred the zone and the '
        'inspection records failed protection on it. It records a miss when it finds failed protection on a zone the rule '
        'did not refer.']),
]


def write_terms(path):
    st = [Paragraph('2027 Lightning Protection Refit: Programme Terms', TITLE),
          Paragraph('%s  |  Technical Services Department  |  26 October 2026' % C.ORG, SMALL),
          Paragraph('Approved by %s, General Manager. Prepared by %s, Technical Services Department Manager.'
                    % (C.PEOPLE['gm'], C.PEOPLE['tsd_manager']), SMALL), Spacer(1, 6)]
    for head, paras in TERMS:
        st.append(Paragraph(head, HEAD))
        for p in paras:
            st.append(Paragraph(p, BODY))
    _docx(path, st, 'terms', '2027 Lightning Protection Refit: Programme Terms', C.PEOPLE['tsd_manager'], C.ORG,
          'KALVECO. 2027 Lightning Protection Refit: programme terms. For the Management Committee.   Page ')
    return [p for _, ps in TERMS for p in ps]


# ------------------------------------------------------------------ the line inspection procedure (PDF)
PROC = [
    ('1. Scope', ['This procedure covers the cyclic inspection of the Cooperative\'s 13.2 kV overhead lines. Every '
                  'protection zone is inspected once in five dry seasons. The zones of each substation are inspected in '
                  'the same dry season, feeder by feeder, between December and March.']),
    ('2. What the team checks', [
        'At every transformer structure and every line arrester structure: the ground lead from the arrester and the '
        'neutral to the ground rod is in place, unbroken and bonded; the arrester\'s disconnector has not operated and the '
        'housing is not cracked or tracked.',
        'Along every span: pin insulators for cracks, punctures and flashover marks; crossarms, braces and poles for rot, '
        'lean and damage; tie wires and connectors; vegetation within the clearance zone.']),
    ('3. Recording', [
        'The team leader records, for each zone, the number of transformer and line arrester structures inspected, the '
        'number of ground leads missing or cut, arresters failed and pin insulators cracked, the poles found leaning and '
        'the spans with vegetation, and the date the repairs were completed. The log is kept by the Line Inspection Section.']),
    ('4. Repairs', [
        'Missing or cut ground leads are replaced, failed arresters and cracked pin insulators are changed, before the zone '
        'is closed out. Work that needs an outage is scheduled with the dispatcher within the same dry season.']),
    ('5. Safety', ['Ground leads are checked and replaced with the line energized only by a crew qualified for live-line '
                   'work. Inspections stop during thunderstorms.']),
]


def write_procedure(path):
    import officepdf as OP
    st = [Paragraph('Cyclic Line Inspection Procedure', TITLE),
          Paragraph('%s  |  Technical Services Department  |  Procedure TSD-LI-04, revision 4, 11 August 2022' % C.ORG, SMALL),
          Spacer(1, 6)]
    for head, paras in PROC:
        st.append(Paragraph(head, HEAD))
        for p in paras:
            st.append(Paragraph(p, BODY))
    a, b = C.STAMP['procedure']
    OP.build(path, st, 'Cyclic Line Inspection Procedure', C.PEOPLE['inspection'], 'Procedure TSD-LI-04',
             'KALVECO TSD-LI-04 rev 4. Page ', C.local(a), C.local(b), producer='LibreOffice 7.3')
    return [p for _, ps in PROC for p in ps]


# ------------------------------------------------------------------ a supplier's materials quotation (distractor)
def write_quotation(path):
    items = [('Copper ground wire, #4 AWG soft-drawn', 'm', 5200, 186.50), ('Ground rod, 16 mm x 2.4 m, copper-bonded', 'pc', 420, 742.00),
             ('Ground rod clamp', 'pc', 460, 88.75), ('Surge arrester, 10 kV, polymer, with disconnector', 'pc', 610, 3140.00),
             ('Pin insulator, 15 kV, porcelain (ANSI 55-5)', 'pc', 900, 412.25), ('Pin insulator, 15 kV, polymer', 'pc', 650, 538.00),
             ('Steel insulator pin, 1 in thread', 'pc', 1500, 96.40), ('Parallel groove connector, Al-Cu', 'pc', 1200, 61.20),
             ('Ground wire molding, PVC, 2.4 m', 'pc', 450, 118.00), ('Anti-theft ground lead cover, galvanized', 'pc', 380, 655.00)]
    rows = [['Item', 'Description', 'Unit', 'Quantity', 'Unit price (PHP)', 'Amount (PHP)']]
    for k, (d, u, q, p) in enumerate(items):
        rows.append([k + 1, d, u, q, p, round(q * p, 2)])
    rows.append(['', 'Total, VAT exclusive', '', '', '', round(sum(q * p for _, _, q, p in items), 2)])
    heads = ['%s: quotation Q-2026-1187' % C.SUPPLIER, 'To: %s, attention %s. Prices valid 60 days, delivery 3 to 5 '
             'weeks from order.' % (C.ORG, C.PEOPLE['materials'])]
    _xlsx(path, [('Quotation', heads, rows, [6, 46, 6, 9, 15, 15], {4: '#,##0.00', 5: '#,##0.00'})], 'quotation',
          'Quotation Q-2026-1187', 'Silangan Sales', C.SUPPLIER)
    return len(rows) - 2
