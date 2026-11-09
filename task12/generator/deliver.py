"""The two golden deliverables, built from figures.json and the golden route's own tables: the treatment paper
(northvale_oat_2027_treatment.docx, two pages, one chart) and the forecast workbook (northvale_oat_2027_forecast.xlsx).
Both pass through the house container writer."""
import io
import os

import common as C
import postprocess as PP

BLUE = '#2a78d6'
INK, INK2, GRID = '#0b0b0b', '#52514e', '#e3e2de'


def chart_png(F, path):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    q = F['quarters_ml']
    fig, ax = plt.subplots(figsize=(6.2, 2.9), dpi=200)
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    xs = range(4)
    bars = ax.bar(xs, q, width=0.42, color=BLUE, zorder=3)
    for x, v in zip(xs, q):
        ax.text(x, v + 0.06, '%.1f' % v, ha='center', va='bottom', fontsize=9, color=INK)
    ax.set_xticks(list(xs))
    ax.set_xticklabels(['Q1 2027', 'Q2 2027', 'Q3 2027', 'Q4 2027'], fontsize=9, color=INK2)
    ax.set_ylabel('Million litres', fontsize=9, color=INK2)
    ax.set_ylim(0, max(q) * 1.25)
    ax.yaxis.grid(True, color=GRID, linewidth=0.8, zorder=0)
    ax.tick_params(axis='y', labelsize=8.5, colors=INK2, length=0)
    ax.tick_params(axis='x', length=0)
    for s in ('top', 'right', 'left'):
        ax.spines[s].set_visible(False)
    ax.spines['bottom'].set_color('#b9b8b2')
    ax.set_title('Northvale Oat at hold: %.1f million litres in 2027, %.1f to %.1f million a quarter' % (F['line27_ml'], min(F['quarters_ml']), max(F['quarters_ml'])),
                 fontsize=10, color=INK, loc='left', pad=8)
    fig.tight_layout()
    fig.savefig(path, format='png', metadata={'Software': None})
    plt.close(fig)


def _cell_text(cell, text, bold=False, size=9, align=None):
    from docx.shared import Pt
    cell.text = ''
    p = cell.paragraphs[0]
    r = p.add_run(text)
    r.bold = bold
    r.font.size = Pt(size)
    if align:
        p.alignment = align


def write_paper(F, T, path, png):
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Mm, Pt, RGBColor
    import officepdf as OP
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Mm(215.9), Mm(279.4)
    sec.left_margin = sec.right_margin = Mm(22)
    sec.top_margin, sec.bottom_margin = Mm(18), Mm(16)
    st = doc.styles['Normal']
    st.font.name = 'Calibri'
    st.font.size = Pt(10)

    def para(text, bold=False, size=10, after=5, italic=False, color=None):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(after)
        r = p.add_run(text)
        r.bold, r.italic = bold, italic
        r.font.size = Pt(size)
        if color:
            r.font.color.rgb = RGBColor.from_string(color)
        return p
    for k, v in [('To', '%s, Brand Director' % C.PEOPLE['brand_director']), ('From', 'Consumer Insights'),
                 ('Date', '12 November 2026'), ('Subject', 'Northvale Oat: 2027 treatment under the Portfolio Review Standard (v3.1)')]:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(0)
        r1 = p.add_run('%s:\t' % k)
        r1.bold = True
        r1.font.size = Pt(9.5)
        r2 = p.add_run(v)
        r2.font.size = Pt(9.5)
    para('', after=2)
    para('Hold: Northvale Oat will take about %.1f per cent of plant-based beverage litres in 2027' % F['share_pct'],
         bold=True, size=13.5, after=6)
    para('On the standard’s basis (distribution and everyday price at the review, no promotional or media weeks in 2027), '
         'the line holds about %.1f per cent of the category’s 2027 litres, %.1f million litres, bought by about %s '
         'households who buy it %.1f times each on average. That is inside the hold band (%.1f to below %.1f per cent): '
         'the line stays listed and receives no 2027 media or sampling, and it keeps its current co-packer slots. Cutting '
         'the price groups another way, reading the settled level from 14 to 20 weeks, growing 2025 litres instead of '
         '2024-25, or reading the levels against all category litres gives %.1f to %.1f per cent, all inside hold.'
         % (F['share_pct'], F['line27_ml'], '{:,}'.format(F['buyers27']), F['per_buyer'], F['bands_pct'][0],
            F['bands_pct'][1], F['share_range'][0], F['share_range'][1]))
    para('Why the line’s current numbers overstate 2027', bold=True, size=10.5, after=3)
    wv, mx = F['waves'], F['wave_mix_pct']
    para('The line has been bought by three groups of households that are not alike. The April buyers, about %s '
         'households, are mostly shoppers who pay premium prices for the category (%d per cent of their category '
         'litres); at their price groups’ settled levels they give the line %.1f per cent of their own plant-based '
         'beverage litres. The buyers who came with the discounter listing from June, about %s households, are mostly '
         'value shoppers (%d per cent of their litres) and settle at %.1f per cent. The Loyal Grocer buyers of late '
         'September, about %s households, are mostly mainstream shoppers (%d per cent of their litres) still in their '
         'first weeks with the line: they are buying it at %.1f per cent of their litres now and settle at %.1f.'
         % ('{:,}'.format(wv[0]['households']), mx[0][0], wv[0]['settled_pct'], '{:,}'.format(wv[1]['households']),
            mx[1][2], wv[1]['settled_pct'], '{:,}'.format(wv[2]['households']), mx[2][1], wv[2]['recent_pct'],
            wv[2]['settled_pct']), after=4)
    para('Their settled level cannot be read from their own five weeks, so each of them is carried at the level of the '
         'households in its own price group that have bought the line for sixteen weeks or more, the price group set '
         'by what each household paid per litre for the category before launch. That level is read as the share of the '
         'litres a household buys in stores carrying the line, because the Loyal Grocer listing put the line on more of '
         'its buyers’ shelves in September: premium %.1f, mainstream %.1f and value %.1f per cent. Every household that '
         'has bought the line is carried into 2027 at its group’s level times the share of its own category buying done '
         'in stores that carry the line at the review (%d, %d and %d per cent on average), weighted by its 2024-25 '
         'category litres grown to 2027 (%.1f per cent a year). Households that have not bought the line by the review '
         'come in at the rate they first bought it in %s and %s, the weeks that match the standard’s basis (every '
         'banner listing it, no promotion or media): about %s first-time buyers in 2027, adding %.2f of a point.'
         % (F['floors_pct'][0], F['floors_pct'][1], F['floors_pct'][2], F['availability_pct'][0], F['availability_pct'][1],
            F['availability_pct'][2], F['growth_pct'], F['new_trial']['weeks'][0], F['new_trial']['weeks'][1],
            '{:,}'.format(F['new_trial']['buyers']), F['new_trial']['points']), after=4)
    para('What this rejects', bold=True, size=10.5, after=3)
    rj = F['rejected']
    para('The usual penetration times repeat times buying-level reading gives %.1f per cent, and carrying the launch '
         'buyers’ current share of their litres to every buyer gives %.1f, both because the later buyers are not '
         'launch buyers. Taking each group at its recent share gives %.1f, because the Loyal Grocer group has not '
         'settled. Reading one settled level from every long-standing buyer, whatever they pay, gives %.1f (support), '
         'because the long-standing buyers are mostly the April group’s premium shoppers. Reading the line’s share in '
         'the weeks without support between the two listings gives %.1f, because it leaves out the Loyal Grocer buyers '
         'altogether. Reading the settled levels against all category litres instead of stocked litres gives %.1f, the '
         'same treatment.' % (rj['pc_careful'], rj['april_for_all'], rj['cohort_recent'], F['rung2']['pooled_pct'],
                              rj['unsupported_weeks'], F['raw']['share_pct']), after=6)
    # the quarterly table
    tbl = doc.add_table(rows=1, cols=4)
    tbl.style = 'Table Grid'
    hdr = ['2027', 'Category litres (millions)', 'Northvale Oat litres (millions)', 'Share of litres (%)']
    for j, h in enumerate(hdr):
        _cell_text(tbl.rows[0].cells[j], h, bold=True, size=8.5)
    for k, nm in enumerate(['Q1', 'Q2', 'Q3', 'Q4']):
        r = tbl.add_row().cells
        vals = [nm, '%.1f' % F['category_quarters_ml'][k], '%.1f' % F['quarters_ml'][k], '%.1f' % F['quarter_share_pct'][k]]
        for j, v in enumerate(vals):
            _cell_text(r[j], v, size=8.5, align=None if j == 0 else WD_ALIGN_PARAGRAPH.RIGHT)
    r = tbl.add_row().cells
    for j, v in enumerate(['Year', '%.1f' % F['category27_ml'], '%.1f' % F['line27_ml'], '%.1f' % F['share_pct']]):
        _cell_text(r[j], v, bold=True, size=8.5, align=None if j == 0 else WD_ALIGN_PARAGRAPH.RIGHT)
    para('Source: Lakeshore Consumer Panel purchase lines to 2026-W44 projected to Canadian households; Meridian Retail '
         'Audit weighted distribution, 2026-W44. Quarters are panel quarters (13 weeks).', size=8, after=6, color='52514E')
    doc.add_picture(png, width=Mm(160))
    para('The year’s figure is the sum of the quarters before rounding.¹', size=8, after=8, color='52514E')
    para('¹ Households counted once however many times they buy. A household that buys the line only on promotion is '
         'counted in 2027 only if it buys at everyday price.', size=7.5, after=0, color='52514E')
    fp = sec.footer.paragraphs[0]
    rr = fp.add_run('Northvale Oat Co. Consumer Insights. Internal.   Page ')
    rr.font.size = Pt(7.5)
    OP._page_field(fp)
    doc.save(path)
    created, modified = C.GOLD_STAMP['paper']
    PP.normalize_docx(path, 'Mary Gonzales', 'Mary Gonzales', C.utc_z(created), C.utc_z(modified), 6, 214, 7731,
                      title='Northvale Oat: 2027 treatment', company=C.ORG)


def write_book(F, T, path):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
    wb = Workbook()
    ws = wb.active
    ws.title = '2027 forecast'
    head = Font(bold=True)
    fill = PatternFill('solid', fgColor='DDE4EE')
    ws['A1'] = 'Northvale Oat, 2027 forecast on the Portfolio Review Standard basis'
    ws['A1'].font = Font(bold=True, size=12)
    ws['A2'] = 'Distribution and everyday price at 2026-W44; no promotional or media weeks in 2027. Canada, projected.'
    rows = [['Panel quarter', 'Category litres (millions)', 'Northvale Oat litres (millions)', 'Share of litres']]
    for k, nm in enumerate(['2027 Q1', '2027 Q2', '2027 Q3', '2027 Q4']):
        rows.append([nm, F['category_quarters_raw'][k] / 1e6, F['quarters_raw'][k] / 1e6, F['quarter_share_raw'][k]])
    for j, h in enumerate(rows[0]):
        c = ws.cell(row=4, column=j + 1, value=h)
        c.font, c.fill = head, fill
        c.alignment = Alignment(wrap_text=True, vertical='top')
    for i, r in enumerate(rows[1:]):
        for j, v in enumerate(r):
            c = ws.cell(row=5 + i, column=j + 1, value=v)
            if j in (1, 2):
                c.number_format = '#,##0.0'
            if j == 3:
                c.number_format = '0.0%'
    ws.cell(row=9, column=1, value='2027').font = head
    ws.cell(row=9, column=2, value='=SUM(B5:B8)').number_format = '#,##0.0'
    ws.cell(row=9, column=3, value='=SUM(C5:C8)').number_format = '#,##0.0'
    ws.cell(row=9, column=4, value='=C9/B9').number_format = '0.0%'
    for j in range(1, 5):
        ws.cell(row=9, column=j).font = head
        ws.cell(row=9, column=j).border = Border(top=Side(style='thin'))
    ws['A11'] = 'Households buying Northvale Oat at least once in 2027'
    ws['C11'] = F['buyers27']
    ws['C11'].number_format = '#,##0'
    ws['A12'] = 'Purchases of Northvale Oat per buying household, 2027'
    ws['C12'] = F['per_buyer_raw']
    ws['C12'].number_format = '0.0'
    ws['A13'] = 'Treatment under the standard'
    ws['C13'] = F['band']
    ws['A14'] = 'Share with other price-group cuts, settled levels from 14 to 20 weeks, 2025 litres or all category litres'
    ws['C14'] = '%.1f%% to %.1f%%' % tuple(F['share_range'])
    for col, wdt in zip('ABCD', (52, 24, 28, 15)):
        ws.column_dimensions[col].width = wdt
    ws.freeze_panes = 'A5'
    # settled share by price group
    w2 = wb.create_sheet('Settled share by price group')
    hd = ['Price group (price paid per litre, 2024-W01 to 2026-W14)', 'Households that have bought the line (Canada)',
          'Settled share of litres bought where the line is stocked', 'Share of own 2024-25 category litres bought at banners carrying the line at 2026-W44',
          'Settled share of own category litres, 2027', 'Panel litres behind the reading', 'Northvale Oat litres 2027 (millions)']
    for j, h in enumerate(hd):
        c = w2.cell(row=1, column=j + 1, value=h)
        c.font, c.fill = head, fill
        c.alignment = Alignment(wrap_text=True, vertical='top')
    for i, t in enumerate(T['tiers']):
        vals = [t['label'], t['households'], t['settled'], t['availability'], t['carried'], t['litres_behind'], t['litres27'] / 1e6]
        fmts = [None, '#,##0', '0.0%', '0%', '0.0%', '#,##0', '#,##0.0']
        for j, (v, f) in enumerate(zip(vals, fmts)):
            c = w2.cell(row=2 + i, column=j + 1, value=v)
            if f:
                c.number_format = f
    for col, wdt in zip('ABCDEFG', (44, 22, 20, 20, 18, 16, 20)):
        w2.column_dimensions[col].width = wdt
    w2.freeze_panes = 'A2'
    # buyers by first purchase
    w3 = wb.create_sheet('Buyers by first purchase')
    hd = ['First purchase', 'Households (Canada)', 'Share of own litres, 2026-W38 to W44',
          'Settled share carried into 2027', 'Northvale Oat litres 2027 (millions)']
    for j, h in enumerate(hd):
        c = w3.cell(row=1, column=j + 1, value=h)
        c.font, c.fill = head, fill
        c.alignment = Alignment(wrap_text=True, vertical='top')
    for i, t in enumerate(T['waves']):
        vals = [t['label'], t['households'], t['recent'], t['settled'], t['litres27'] / 1e6]
        fmts = [None, '#,##0', '0.0%', '0.0%', '#,##0.0']
        for j, (v, f) in enumerate(zip(vals, fmts)):
            c = w3.cell(row=2 + i, column=j + 1, value=v)
            if f:
                c.number_format = f
    for col, wdt in zip('ABCDE', (34, 18, 22, 22, 20)):
        w3.column_dimensions[col].width = wdt
    w3.freeze_panes = 'A2'
    w4 = wb.create_sheet('Notes')
    notes = ['As of the panel delivery to 2026-W44 (week ending 1 November 2026) and the retail audit for the same week.',
             'Households reporting from 2024-W01 to 2026-W44; returns netted, receipts uploaded twice counted once.',
             'Price group: terciles of price paid per litre for the category, 2024-W01 to 2026-W14, among category buyers.',
             'Settled share: litres of Northvale Oat over the plant-based beverage litres bought in stores carrying the '
             'line (each banner at its weighted distribution that week), weeks without a Northvale promotion, households '
             'at 16 weeks or more since their own first purchase.',
             '2027 share of own litres: the settled share times the share of the household\'s 2024-25 category litres '
             'bought at banners carrying the line at 2026-W44.',
             '2027 litres: each household\'s 2024-25 weekly category litres grown at the panel\'s 2024 to 2025 rate.',
             'Households buying in 2027: each buyer\'s chance of at least one purchase given its expected 2027 purchases.',
             'Households that have not bought the line by 2026-W44: first purchases in 2027 at each price group\'s rate in '
             '2026-W43 and W44 (every banner listing the line, no promotion or media), then the group\'s level for the rest '
             'of the year.',
             'Prepared by Consumer Insights for the 2026 portfolio review (23 November 2026).']
    for i, n in enumerate(notes):
        w4.cell(row=1 + i, column=1, value=n)
    w4.column_dimensions['A'].width = 120
    wb.save(path)
    created, modified = C.GOLD_STAMP['book']
    PP.normalize_ooxml(path, 'Mary Gonzales', 'Mary Gonzales', C.utc_z(created), C.utc_z(modified),
                       title='Northvale Oat 2027 forecast', excel=True, company=C.ORG)


def build(F, T, golden_dir):
    os.makedirs(golden_dir, exist_ok=True)
    import tempfile
    tmp = tempfile.mkdtemp()
    png = os.path.join(tmp, 'q.png')
    chart_png(F, png)
    write_paper(F, T, os.path.join(golden_dir, C.DELIVERABLES['paper']), png)
    write_book(F, T, os.path.join(golden_dir, C.DELIVERABLES['book']))
    PP.own_mtimes(golden_dir, {})
