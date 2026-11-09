"""The pack's office files in their issuers' genres: the panel's product master, Northvale's trade calendar and
media plan, the brand-health tracker wave, the portfolio review standard, and the agency's 2027 support proposal.
Workbooks are written and then saved in Excel's own form (postprocess.normalize_ooxml); documents are laid out by
the house writer's Word stage (officepdf) and saved in Word's own form (postprocess.normalize_docx)."""
import datetime as dt

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

import common as C
import postprocess as PP
import world as W

BODY = ParagraphStyle('body', fontName='Helvetica', fontSize=10, leading=13.2, spaceAfter=6)
SMALL = ParagraphStyle('small', parent=BODY, fontSize=8.6, leading=11, spaceAfter=3)
HEAD = ParagraphStyle('head', parent=BODY, fontName='Helvetica-Bold', fontSize=11, spaceBefore=7, spaceAfter=4)
TITLE = ParagraphStyle('title', parent=BODY, fontName='Helvetica-Bold', fontSize=15, leading=18, spaceAfter=3)
CELL = ParagraphStyle('cell', fontName='Helvetica', fontSize=8.8, leading=10.8)
CELLB = ParagraphStyle('cellb', parent=CELL, fontName='Helvetica-Bold')


def _xlsx(path, sheets, key, title, author, company):
    """sheets: list of (name, header rows, rows, column widths). Header rows bold, the table header shaded."""
    wb = Workbook()
    wb.remove(wb.active)
    for name, heads, rows, widths in sheets:
        ws = wb.create_sheet(name)
        r = 1
        for h in heads:
            ws.cell(row=r, column=1, value=h).font = Font(bold=(r == 1), size=11 if r == 1 else 10)
            r += 1
        if heads:
            r += 1
        top = r
        for k, row in enumerate(rows):
            for j, v in enumerate(row):
                c = ws.cell(row=r, column=j + 1, value=v)
                if k == 0:
                    c.font = Font(bold=True)
                    c.fill = PatternFill('solid', fgColor='DDE4EE')
                    c.alignment = Alignment(wrap_text=True, vertical='top')
            r += 1
        for j, wdt in enumerate(widths):
            ws.column_dimensions[chr(65 + j)].width = wdt
        ws.freeze_panes = ws.cell(row=top + 1, column=1)
    wb.save(path)
    PP.normalize_ooxml(path, author, author, C.utc_z(C.CREATED[key]), C.utc_z(C.STAMP[key]), title=title, excel=True,
                       company=company)


def write_master(path, M):
    """The panel's plant-based beverage product master, October 2026 refresh. Rows carried from the 2024 and 2025
    masters keep that master's pack convention (millilitres); rows added from 2026 are in litres."""
    rows = [['item_code', 'brand', 'item_description', 'manufacturer', 'own_label_banner_cd', 'panel_category',
             'segment', 'pack_size', 'pack_uom', 'units_per_pack', 'organic', 'first_seen']]
    for s in sorted(M, key=lambda s: (s['brand'] != 'Northvale Oat', s['brand'], s['description'])):
        if s['first_year'] <= 2025:
            size, uom = int(round(s['litres'] * 1000)), 'mL'
        else:
            size, uom = s['litres'], 'L'
        rows.append([s['ean'], s['brand'], s['description'], s['manufacturer'], s['own_label_banner'],
                     'PLANT BASED BEVERAGES', s['segment'], size, uom, s['units'], s['organic'],
                     '%d-W%02d' % (s['first_year'], 15 if s['first_year'] == 2026 else 3 + s['first_year'] % 40)])
    _xlsx(path, [('Items', [], rows, [16, 18, 30, 26, 10, 22, 10, 10, 9, 9, 8, 11])], 'master',
          'Plant based beverages item master', C.PEOPLE['panel_lead'], C.PANEL_ORG)
    return len(rows) - 1


def write_trade(path, M):
    nv = {s['description']: s['ean'] for s in M if s['family'] == -2}
    big = '%s, %s' % (nv['Oat Original'], nv['Oat Unsweetened'])
    allv = '%s, %s, %s' % (nv['Oat Original'], nv['Oat Unsweetened'], nv['Barista Oat'])

    def d(y, w, k=1):
        return dt.date.fromisocalendar(y, w, k).isoformat()
    rows = [['event_id', 'banner', 'items', 'mechanic', 'start_date', 'end_date', 'shelf_price_1.75L', 'shelf_price_946mL', 'status'],
            ['NV26-001', 'Foxmere Fresh', allv, 'Launch price', d(2026, 15), d(2026, 18, 7), 4.79, 3.79, 'Run'],
            ['NV26-002', 'Greenleaf Market', allv, 'Launch price', d(2026, 15), d(2026, 18, 7), 4.79, 3.79, 'Run'],
            ['NV26-003', 'Northglen Foods', allv, 'Launch price', d(2026, 15), d(2026, 18, 7), 4.79, 3.79, 'Run'],
            ['NV26-004', 'Marche Belvoir', allv, 'Launch price', d(2026, 15), d(2026, 18, 7), 4.79, 3.79, 'Run'],
            ['NV26-005', 'ValuWay', allv, 'Listing price', d(2026, 24), d(2026, 26, 7), 3.99, 3.29, 'Run'],
            ['NV26-006', 'Trade Basket', allv, 'Listing price', d(2026, 24), d(2026, 26, 7), 3.99, 3.29, 'Run'],
            ['NV26-007', 'Loyal Grocer', big, 'Listing, multibuy 2 for $10.00', d(2026, 39), d(2026, 41, 7), 5.00, '', 'Run'],
            ['NV26-008', 'Loyal Grocer', nv['Barista Oat'], 'Listing, multibuy 2 for $8.00', d(2026, 39), d(2026, 41, 7), '', 4.00, 'Run'],
            ['NV26-009', 'Northglen Foods', allv, 'Multibuy 2 for $10.00 / 2 for $8.00', d(2026, 39), d(2026, 41, 7), 5.00, 4.00, 'Run'],
            ['NV26-010', 'Marche Belvoir', allv, 'Multibuy 2 for $10.00 / 2 for $8.00', d(2026, 39), d(2026, 41, 7), 5.00, 4.00, 'Run'],
            ['NV26-011', 'Foxmere Fresh', allv, 'TPR $4.99 / $3.99', d(2026, 48), d(2026, 49, 7), 4.99, 3.99, 'Cancelled'],
            ['NV26-012', 'Loyal Grocer', allv, 'Holiday end cap', d(2026, 50), d(2026, 51, 7), '', '', 'Cancelled']]
    heads = ['Northvale Oat 2026 trade calendar', 'Owner: %s, trade marketing. Funded events only.' % C.PEOPLE['trade_manager']]
    _xlsx(path, [('2026 events', heads, rows, [10, 18, 48, 34, 12, 12, 15, 15, 10])], 'trade',
          'Northvale Oat 2026 trade calendar', C.PEOPLE['trade_manager'], C.ORG)
    return len(rows) - 1


def write_media(path):
    rows = [['week_start', 'channel', 'buy', 'target_grps', 'impressions_000', 'net_spend_cad']]
    import numpy as np
    rng = np.random.default_rng(W.SEED + 107)
    for t in range(W.T_LAUNCH, W.T_END + 1):
        if not W.MEDIA[t]:
            continue
        ws = W.week_start(t).isoformat()
        tv = int(round(rng.uniform(150, 210) if t < W.T_LAUNCH + 6 else rng.uniform(190, 260)))
        rows.append([ws, 'National TV', 'A25-54', tv, '', int(round(tv * rng.uniform(1820, 1960), -2))])
        ov = int(round(rng.uniform(2600, 4100), -1))
        rows.append([ws, 'Online video', 'A25-54', '', ov, int(round(ov * rng.uniform(17.5, 19.8), -1))])
        if t >= W.T_LYG:
            so = int(round(rng.uniform(3100, 3900), -1))
            rows.append([ws, 'Social', 'A25-44', '', so, int(round(so * rng.uniform(8.1, 9.4), -1))])
    heads = ['Northvale Oat 2026 media flighting (as bought)', 'Prepared by %s for %s.' % (C.AGENCY, C.ORG)]
    _xlsx(path, [('Flighting', heads, rows, [12, 14, 9, 12, 15, 14])], 'media', 'Northvale Oat 2026 media flighting',
          C.PEOPLE['agency_lead'], C.AGENCY)
    return len(rows) - 1


def write_tracker(path):
    rows = [['brand', 'aided_awareness_pct', 'consideration_pct', 'ever_tried_claimed_pct', 'bought_past_3_months_claimed_pct', 'base_n'],
            ['Prairie Grove', 71, 44, 52, 31, 1204], ['Silverbrook', 78, 41, 61, 29, 1204],
            ['Coastline', 46, 19, 24, 9, 1204], ['Wildflax', 33, 17, 15, 7, 1204],
            ['Haven & Hollow', 29, 15, 13, 6, 1204], ['Little Ferns', 18, 9, 6, 3, 1204],
            ['Northvale Oat', 41, 23, 19, 11, 1204], ['Store own label (any)', 88, 47, 74, 46, 1204]]
    heads = ['Plant-based beverage brand health tracker, wave 9', 'Fieldwork 8 to 21 September 2026. Online, '
             'Canadian adults 18 to 69 who bought plant-based beverages in the past three months.']
    _xlsx(path, [('Wave 9', heads, rows, [22, 18, 16, 20, 30, 8])], 'tracker', 'Brand health tracker wave 9',
          'Insights team', C.ORG)
    return len(rows) - 1


def _docx(path, story, key, title, author, company, footer):
    """the issuer's document as its word processor saves it (the house writer's Word stage, then Word's own form)"""
    import hashlib
    from docx import Document
    from docx.enum.text import WD_BREAK
    from docx.shared import Mm, Pt, RGBColor
    from reportlab.platypus import KeepTogether, PageBreak
    import officepdf as OP
    OP.FONT = 'Calibri'
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Mm(215.9), Mm(279.4)
    sec.left_margin = sec.right_margin = Mm(23)
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
    PP.normalize_docx(path, author, author, C.utc_z(C.CREATED[key]), C.utc_z(C.STAMP[key]), 3 + seed % 5,
                      31 + seed % 60, seed, title=title, company=company)


def _tbl(rows, widths):
    data = [[Paragraph(str(x), CELLB if k == 0 else CELL) for x in r] for k, r in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LINEBELOW', (0, 0), (-1, 0), 0.7, colors.black),
                           ('TOPPADDING', (0, 0), (-1, -1), 2), ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
                           ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0.9, 0.92, 0.95))]))
    return t


STANDARD = [
    ('1. Purpose and scope', [
        'This standard sets how Northvale Oat Co. decides, once a year, what each product line launched in the previous '
        'twelve months receives in the following calendar year: whether it is delisted, held, supported or expanded. It '
        'applies to every line first shipped to retail in the twelve months before the review date. The 2026 review is '
        'held on 23 November 2026 and covers lines first shipped from 24 November 2025.']),
    ('2. Definitions', [
        '(a) The category is the Lakeshore Consumer Panel’s plant-based beverages category: every item the panel’s '
        'product master places in it, whatever the brand, own label included.',
        '(b) Litres are the litres of product bought: units bought times the litres in each unit.',
        '(c) Projected purchases are the panel households’ purchases raised to all Canadian households by each '
        'household’s projection factor for the year.',
        '(d) Distribution is the retail audit’s weighted distribution of the line in each banner.']),
    ('3. The forecast', [
        '(a) The review rests on one number for each line: its forecast share of the category’s litres in calendar 2027, '
        'meaning panel weeks 2027-W01 to 2027-W52, for Canada, as the panel’s projected purchases will measure it.',
        '(b) The forecast covers every Canadian household, including households that have not bought the line by the '
        'review.',
        '(c) The forecast is made with the line at the distribution and the everyday shelf price it holds at the review, '
        'and with no promotional or media weeks in 2027. Any support the line receives in 2027 is decided by this '
        'review and is not part of the forecast it rests on.',
        '(d) The forecast is prepared by the consumer insights team from the panel and audit data delivered before the '
        'review, and states the line’s litres and households buying for the year beside the share.']),
    ('4. Treatments', [
        'The forecast share sets the treatment. The share is compared with the bands before it is rounded for '
        'reporting.']),
    ('5. Approval and timing', [
        '(a) The brand director approves a delist or hold treatment. A support or expand treatment goes to the commercial '
        'leadership team with the forecast.',
        '(b) The treatment is set before the co-packer confirms the coming year’s production slots (for the 2026 review, '
        'on 1 December 2026). A line that is held keeps its current slots; a line that is expanded moves to a dedicated '
        'line from the second quarter.']),
]


def write_standard(path):
    st = [Paragraph('Portfolio Review Standard: Treatment of New Lines', TITLE),
          Paragraph('Northvale Oat Co.  |  Finance and Commercial  |  Version 3.1, approved 17 February 2026', SMALL),
          Paragraph('Owner: %s, Vice-President, Finance' % C.PEOPLE['vp_finance'], SMALL), Spacer(1, 6)]
    for head, paras in STANDARD:
        st.append(Paragraph(head, HEAD))
        for p in paras:
            st.append(Paragraph(p, BODY))
        if head.startswith('4.'):
            st.append(_tbl([['Forecast 2027 share of category litres', 'Treatment', 'What it means'],
                            ['Below %.1f per cent' % C.BAND_EDGES[0], 'Delist', 'Leave the range when current retailer commitments end'],
                            ['%.1f to below %.1f per cent' % C.BAND_EDGES[:2], 'Hold', 'Stay listed at everyday price; no 2027 media or sampling'],
                            ['%.1f to below %.1f per cent' % C.BAND_EDGES[1:], 'Support', 'Fund the 2027 media and sampling plan'],
                            ['%.1f per cent or more' % C.BAND_EDGES[2], 'Expand', 'Move to a dedicated co-packer line and widen distribution']],
                           [150, 70, 230]))
            st.append(Spacer(1, 4))
    st.append(Spacer(1, 6))
    st.append(Paragraph('Version history: first issued March 2023; February 2025, litres replaced value as the measure; '
                        'February 2026, bands reset for the 2026 review.', SMALL))
    _docx(path, st, 'standard', 'Portfolio Review Standard: Treatment of New Lines', C.PEOPLE['vp_finance'], C.ORG,
          'Northvale Oat Co. Portfolio Review Standard v3.1. Internal.   Page ')
    return [p for _, ps in STANDARD for p in ps]


def write_proposal(path):
    st = [Paragraph('Northvale Oat: 2027 Support Plan', TITLE),
          Paragraph('Prepared for %s by %s, 2 November 2026' % (C.PEOPLE['brand_director'], C.AGENCY), SMALL),
          Spacer(1, 6),
          Paragraph('What we propose', HEAD),
          Paragraph('Three national TV bursts (February, May, September) with online video in each, a summer sampling '
                    'tour in eight cities, and in-store demonstrations in Loyal Grocer and Northglen Foods in the weeks '
                    'around each burst. The plan keeps the barista carton in coffee-shop partnerships in Toronto, Montreal '
                    'and Vancouver.', BODY),
          Paragraph('Budget', HEAD),
          _tbl([['Item', 'Weeks', 'Net cost CAD'], ['National TV, three bursts', '12', '1,140,000'],
                ['Online video and social', '18', '410,000'], ['Sampling tour', '6', '265,000'],
                ['In-store demonstrations', '9', '188,000'], ['Agency fees', '', '96,000'],
                ['Total', '', '2,099,000']], [230, 60, 110]),
          Spacer(1, 6),
          Paragraph('Why now', HEAD),
          Paragraph('Awareness reached 41 per cent of category buyers in the September tracker wave, five months after '
                    'launch, and consideration 23 per cent. The September burst lifted weekly sales in the mainstream '
                    'banners.', BODY),
          Paragraph('Measurement', HEAD),
          Paragraph('Each burst will be read from the panel against the weeks before it, and the tracker will be '
                    'fielded after each burst.', BODY)]
    _docx(path, st, 'proposal', 'Northvale Oat 2027 Support Plan', C.PEOPLE['agency_lead'], C.AGENCY,
          'Halyard & Finch. Confidential proposal.   Page ')
