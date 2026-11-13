"""Office files in their issuers' genres: workbooks saved in Excel's form (postprocess.normalize_ooxml), PDFs the
issuing office exported from Word (officepdf), Word documents as Word saves them (postprocess.normalize_docx)."""
import datetime as dt

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from reportlab.lib.styles import ParagraphStyle

import common as C
import postprocess as PP

BODY = ParagraphStyle('body', fontName='Helvetica', fontSize=10, leading=13.4, spaceAfter=6)
HEAD = ParagraphStyle('head', parent=BODY, fontName='Helvetica-Bold', fontSize=10.5, spaceBefore=8, spaceAfter=4)
TITLE = ParagraphStyle('title', parent=BODY, fontName='Helvetica-Bold', fontSize=13, leading=16, spaceAfter=4)
SMALL = ParagraphStyle('small', parent=BODY, fontSize=8.6, leading=11, spaceAfter=3)
CELL = ParagraphStyle('cell', fontName='Helvetica', fontSize=8.4, leading=10.2)


def _col(j):
    s = ''
    j += 1
    while j:
        j, r = divmod(j - 1, 26)
        s = chr(65 + r) + s
    return s


def stamps(key, table=None):
    a, b = (table or C.STAMP)[key]
    return C.utc_z(a), C.utc_z(b)


def xlsx(path, sheets, key, title, author, company=C.ORG, table=None):
    """sheets: list of (name, header lines, rows (first is the column header), widths, number formats by column)"""
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
                    c.fill = PatternFill('solid', fgColor='DDE5EE')
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
    cr, md = stamps(key, table)
    PP.normalize_ooxml(path, author, author, cr, md, title=title, excel=True, company=company)


def pdf(path, story, key, title, author, subject, footer, producer=None, table=None):
    import officepdf as OP
    a, b = (table or C.STAMP)[key]
    OP.build(path, story, title=title, author=author, subject=subject, footer=footer, created=C.local(a),
             modified=C.local(b), font='Liberation Sans', body_pt=9.6, producer=producer, page_mm=C.LETTER_MM)


def docx(path, blocks, key, title, author, revision=6, total_time=184, seed='t13', table=None, company=C.ORG):
    """blocks: list of ('h', text) | ('p', text) | ('table', rows) | ('small', text)"""
    from docx import Document
    from docx.shared import Pt, Mm
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Mm(C.LETTER_MM[0]), Mm(C.LETTER_MM[1])
    sec.left_margin = sec.right_margin = Mm(22)
    st = doc.styles['Normal']
    st.font.name = 'Calibri'
    st.font.size = Pt(10.5)
    for kind, val in blocks:
        if kind == 'title':
            p = doc.add_paragraph()
            r = p.add_run(val)
            r.bold = True
            r.font.size = Pt(14)
        elif kind == 'h':
            p = doc.add_paragraph()
            r = p.add_run(val)
            r.bold = True
            r.font.size = Pt(11.5)
        elif kind == 'p':
            doc.add_paragraph(val)
        elif kind == 'small':
            p = doc.add_paragraph()
            r = p.add_run(val)
            r.font.size = Pt(8.5)
        elif kind == 'bullets':
            for b in val:
                doc.add_paragraph(b, style='List Bullet')
        elif kind == 'table':
            t = doc.add_table(rows=len(val), cols=len(val[0]))
            t.style = 'Table Grid'
            for i, row in enumerate(val):
                for j, v in enumerate(row):
                    cell = t.cell(i, j)
                    cell.text = str(v)
                    for par in cell.paragraphs:
                        for run in par.runs:
                            run.font.size = Pt(9)
                            if i == 0:
                                run.bold = True
    doc.core_properties.title = title
    doc.core_properties.author = author
    doc.save(path)
    a, b = (table or C.STAMP)[key]
    PP.normalize_docx(path, author, author, C.utc_z(a)[:-4] + ':00Z' if False else C.local(a).astimezone(C.UTC).strftime('%Y-%m-%dT%H:%M:00Z'),
                      C.local(b).astimezone(C.UTC).strftime('%Y-%m-%dT%H:%M:00Z'), revision, total_time, seed, title=title,
                      company=company)
