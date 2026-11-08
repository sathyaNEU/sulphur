"""The pack's documents: the agency workbook, the plan catalogue, the growth review standard, metadata.json."""
import datetime as dt
import json
import os

from common import *          # noqa: F401,F403

MARKETS = ['DE', 'AT', 'NL', 'FR', 'IT', 'ES', 'UK']
CHANNELS = ['Meta', 'Google Search', 'TikTok', 'YouTube', 'Affiliate']
SHARE_M = {'DE': .37, 'AT': .06, 'NL': .09, 'FR': .15, 'IT': .12, 'ES': .11, 'UK': .10}
SHARE_C = {'Meta': .44, 'Google Search': .26, 'TikTok': .15, 'YouTube': .10, 'Affiliate': .05}
AGENCY_GBP_RATE = 1.17          # the agency's own planning conversion, EUR per GBP


def agency_workbook(path, rng, rates, n_paid):
    """Fenwright Media's AUT26 close-out and invoices. Returns the media figures for truth.json."""
    from openpyxl import Workbook
    from openpyxl.styles import Font, Alignment
    media_total_eur = 221.4 * n_paid                  # about EUR 221 of media per paid member
    wb = Workbook()
    ws = wb.active
    ws.title = 'Invoices'
    ws.append(['Fenwright Media GmbH / Fenwright Media Ltd: invoices and credit notes for campaign AUT26 (Corvane)'])
    ws['A1'].font = Font(bold=True)
    ws.append([])
    head = ['document', 'type', 'issued_on', 'issuer', 'currency', 'month', 'market', 'channel', 'net', 'vat_rate',
            'vat', 'gross']
    ws.append(head)
    for c in ws[3]:
        c.font = Font(bold=True)
    lines = []
    month_split = {'2026-09': .47, '2026-10': .53}
    for mon, ms in month_split.items():
        issued = dt.date(2026, 9, 30) if mon == '2026-09' else dt.date(2026, 10, 31)
        for mk in MARKETS:
            for ch in CHANNELS:
                base = media_total_eur * ms * SHARE_M[mk] * SHARE_C[ch] * float(rng.uniform(.88, 1.12))
                if mk == 'UK':
                    gbp = round(base * rate_on(rates, issued, 'GBP') / 10) * 10 + float(rng.choice([0, 0, 5]))
                    lines.append(('FM-UK-2026-%s' % ('0931' if mon == '2026-09' else '1031'), 'invoice', issued,
                                  'Fenwright Media Ltd', 'GBP', mon, mk, ch, round(gbp, 2), 0.0))
                else:
                    eur = round(base / 10) * 10 + float(rng.choice([0, 0, 5]))
                    lines.append(('FM-DE-2026-%s' % ('0930' if mon == '2026-09' else '1030'), 'invoice', issued,
                                  'Fenwright Media GmbH', 'EUR', mon, mk, ch, round(eur, 2), 0.19))
    # credit note: September YouTube under-delivery, DE and FR
    for mk, amt in (('DE', -9180.00), ('FR', -5070.00)):
        lines.append(('FM-DE-2026-CN07', 'credit note', dt.date(2026, 10, 15), 'Fenwright Media GmbH', 'EUR',
                      '2026-09', mk, 'YouTube', amt, 0.19))
    lines.sort(key=lambda l: (l[2], l[0], MARKETS.index(l[6]), CHANNELS.index(l[7])))
    net_eur = 0.0
    for l in lines:
        vat = round(l[8] * l[9], 2)
        ws.append([l[0], l[1], l[2].isoformat(), l[3], l[4], l[5], l[6], l[7], l[8],
                   ('%d%%' % round(l[9] * 100)) if l[9] else 'reverse charge', vat, round(l[8] + vat, 2)])
        net_eur += l[8] if l[4] == 'EUR' else l[8] / rate_on(rates, l[2], 'GBP')
    for col, w in zip('ABCDEFGHIJKL', [20, 12, 12, 22, 9, 9, 8, 15, 12, 15, 11, 12]):
        ws.column_dimensions[col].width = w
    # close-out, on the agency's own tracking and its planning conversion
    co = wb.create_sheet('Close-out')
    co.append(['AUT26 close-out, 1 September to 31 October 2026. Prepared by Veit Stadelmann, account director, '
               '2 November 2026. Tracked conversions are Fenwright pixel conversions (7-day click, 1-day view); '
               'GBP media shown in EUR at the plan rate of 1.17.'])
    co['A1'].alignment = Alignment(wrap_text=False)
    co.append([])
    co.append(['market', 'channel', 'impressions', 'clicks', 'tracked_signups', 'tracked_paid_conversions',
               'media_net_eur', 'cost_per_tracked_paid_eur'])
    for c in co[3]:
        c.font = Font(bold=True)
    for mk in MARKETS:
        for ch in CHANNELS:
            net = sum(l[8] for l in lines if l[6] == mk and l[7] == ch)
            net_e = net * AGENCY_GBP_RATE if mk == 'UK' else net
            cpm = {'Meta': 6.1, 'Google Search': 31.0, 'TikTok': 4.4, 'YouTube': 9.8, 'Affiliate': 12.0}[ch]
            imp = int(net_e / cpm * 1000 * float(rng.uniform(.9, 1.1)))
            ctr = {'Meta': .011, 'Google Search': .062, 'TikTok': .008, 'YouTube': .004, 'Affiliate': .021}[ch]
            clicks = int(imp * ctr * float(rng.uniform(.85, 1.15)))
            paid = int(round(n_paid * SHARE_M[mk] * SHARE_C[ch] * float(rng.uniform(1.0, 1.16))))
            sign = int(paid * float(rng.uniform(2.2, 2.9)))
            co.append([mk, ch, imp, clicks, sign, paid, round(net_e, 2), round(net_e / max(paid, 1), 2)])
    for col, w in zip('ABCDEFGH', [8, 15, 13, 10, 15, 24, 14, 24]):
        co.column_dimensions[col].width = w
    wb.properties.creator = 'Fenwright Media'
    wb.properties.lastModifiedBy = 'Veit Stadelmann'
    wb.properties.created = dt.datetime(2026, 11, 2, 16, 12, 0)
    wb.properties.modified = dt.datetime(2026, 11, 2, 16, 40, 0)
    wb.save(path)
    import postprocess as PP
    PP.normalize_ooxml(path, 'Veit Stadelmann', 'Veit Stadelmann', '2026-11-02T16:12:00Z', '2026-11-02T16:40:00Z',
                       excel=True, company='Fenwright Media GmbH')
    return dict(media_net_eur_ecb=round(net_eur, 2), lines=len(lines))


APP_XLSX = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
            'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes"><Application>Microsoft Excel'
            '</Application><DocSecurity>0</DocSecurity><ScaleCrop>false</ScaleCrop><Company>{company}</Company>'
            '<LinksUpToDate>false</LinksUpToDate><SharedDoc>false</SharedDoc><HyperlinksChanged>false</HyperlinksChanged>'
            '<AppVersion>16.0300</AppVersion></Properties>')
APP_DOCX = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
            'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes"><Template>Normal.dotm</Template>'
            '<TotalTime>{minutes}</TotalTime><Pages>{pages}</Pages><Words>{words}</Words><Characters>{chars}</Characters>'
            '<Application>Microsoft Office Word</Application><DocSecurity>0</DocSecurity><Lines>{lines}</Lines>'
            '<Paragraphs>{paras}</Paragraphs><ScaleCrop>false</ScaleCrop><Company>{company}</Company>'
            '<LinksUpToDate>false</LinksUpToDate><CharactersWithSpaces>{chars_sp}</CharactersWithSpaces>'
            '<SharedDoc>false</SharedDoc><HyperlinksChanged>false</HyperlinksChanged><AppVersion>16.0000</AppVersion></Properties>')
CORE = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
        'xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
        '{title}<dc:creator>{creator}</dc:creator><cp:lastModifiedBy>{last}</cp:lastModifiedBy>{rev}'
        '<dcterms:created xsi:type="dcterms:W3CDTF">{created}</dcterms:created>'
        '<dcterms:modified xsi:type="dcterms:W3CDTF">{modified}</dcterms:modified></cp:coreProperties>')


def ooxml_props(path, creator, last, created, modified, company, title=None, docx_stats=None, revision=None):
    """Rewrite docProps/app.xml and docProps/core.xml with the fiction's own values (the writing library's name,
    version and the build clock removed), every other entry byte for byte, fixed entry times."""
    import zipfile
    ext = os.path.splitext(path)[1].lower()
    if ext == '.xlsx':
        app = APP_XLSX.format(company=company)
    else:
        s = docx_stats
        app = APP_DOCX.format(company=company, **s)
    core = CORE.format(title=('<dc:title>%s</dc:title>' % title) if title else '', creator=creator, last=last,
                       rev=('<cp:revision>%d</cp:revision>' % revision) if revision else '',
                       created=created.strftime('%Y-%m-%dT%H:%M:%SZ'), modified=modified.strftime('%Y-%m-%dT%H:%M:%SZ'))
    tmp = path + '.tmp'
    with zipfile.ZipFile(path) as zin, zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zout:
        for item in sorted(zin.infolist(), key=lambda i: i.filename):
            data = zin.read(item.filename)
            if item.filename == 'docProps/app.xml':
                data = app.encode('utf-8')
            elif item.filename == 'docProps/core.xml':
                data = core.encode('utf-8')
            zi = zipfile.ZipInfo(item.filename, date_time=modified.timetuple()[:6])
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o600 << 16
            zout.writestr(zi, data)
    os.replace(tmp, path)


def _fix_zip_times(path):
    """Rewrite an OOXML zip with fixed entry times so rebuilds are byte-identical."""
    import zipfile
    tmp = path + '.tmp'
    with zipfile.ZipFile(path) as zin, zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zout:
        for item in sorted(zin.infolist(), key=lambda i: i.filename):
            data = zin.read(item.filename)
            zi = zipfile.ZipInfo(item.filename, date_time=(2026, 11, 2, 16, 40, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o600 << 16
            zout.writestr(zi, data)
    os.replace(tmp, path)


def plans_json(path):
    cat = {
        'catalogue': 'Corvane membership plans and promotions',
        'exported_at': '2026-11-03T06:55:00Z',
        'plans': [],
        'promotions': [
            {'code': 'FRIEND15', 'discount_percent': 15, 'applies_to': 'first membership charge',
             'valid_from': '2022-03-01', 'valid_to': None, 'channel': 'referral programme'},
            {'code': 'SPR25-WELCOME10', 'discount_percent': 10, 'applies_to': 'first membership charge',
             'valid_from': '2025-03-01', 'valid_to': '2025-04-30', 'campaign': 'SPR25'},
            {'code': 'AUT26-WELCOME10', 'discount_percent': 10, 'applies_to': 'first membership charge',
             'valid_from': '2026-09-01', 'valid_to': '2026-10-31', 'campaign': 'AUT26'},
        ],
    }
    for p in (0, 1):
        pl = PLANS[p]
        cat['plans'].append({'code': pl['old'], 'name': pl['name'], 'lessons_per_month': pl['lessons'],
                             'lesson_minutes': 50, 'billing': 'monthly',
                             'price': {c: v[0] for c, v in pl['price'].items()},
                             'valid_from': '2022-01-01', 'valid_to': '2025-03-31', 'replaced_by': pl['new']})
        cat['plans'].append({'code': pl['new'], 'name': pl['name'], 'lessons_per_month': pl['lessons'],
                             'lesson_minutes': 50, 'billing': 'monthly',
                             'price': {c: v[1] for c, v in pl['price'].items()},
                             'valid_from': '2025-04-01', 'valid_to': None,
                             'note': 'existing members move to this code and price at their first renewal on or after 1 April 2025'})
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(cat, f, indent=2, ensure_ascii=False)
        f.write('\n')


STANDARD = [
    ('h', 'Corvane growth review standard: paid acquisition campaigns'),
    ('m', 'Version 3, effective 1 July 2025. Owner: Caroline Ritter, Head of Growth. Applies to every paid '
          'acquisition campaign booked through an agency under a campaign code.'),
    ('s', '1. Purpose'),
    ('p', 'Before a campaign is re-run, the growth team reviews what each member it brought in has cost against the '
          'members it keeps. This standard fixes the terms of that review so that every campaign is judged on the '
          'same basis. It does not set how a campaign is planned, bought or creatively tested.'),
    ('s', '2. When a review is due'),
    ('p', 'A review is due before a campaign is booked again with the same agency and offer, and in any case within '
          'six weeks of the campaign\'s last day. The growth lead sets the re-run bar for each campaign before the '
          'review starts and records it in the booking request.'),
    ('s', '3. Definitions'),
    ('p', '3.1 A paid member is an account with at least one membership charge collected and not refunded in full.'),
    ('p', '3.2 A campaign member is a paid member whose sign-up carries the campaign\'s code in its utm_campaign tag '
          'and whose first membership charge was collected on or between the campaign\'s first and last day. Days '
          'are calendar days in Berlin.'),
    ('p', '3.3 A twelfth-month member is a campaign member who pays a twelfth monthly membership charge. A charge '
          'counts once, when it is collected (a charge collected on a retry counts as that month\'s charge), and only '
          'if it is not refunded in full. Charges count from the member\'s first collected charge within one '
          'continuous membership; an account that cancels and later starts paying again begins a new membership, '
          'and its later charges do not count towards the first.'),
    ('p', '3.4 Campaign cost is the media the agency invoiced for the campaign, net of VAT and of credit notes, plus '
          'the first-month discounts given to campaign members under the campaign\'s promotion code, measured '
          'against the list price of the plan charged. Amounts in GBP or CHF are converted to EUR at the ECB euro '
          'reference rate for the invoice or charge date, or the last rate published before it.'),
    ('p', '3.5 Cost per paid member is campaign cost divided by the number of campaign members. Cost per twelfth-month '
          'member is campaign cost divided by the number of twelfth-month members.'),
    ('p', '3.6 While some campaign members have not yet reached a twelfth monthly charge, the review uses the '
          'expected number of twelfth-month members: members who have already paid a twelfth charge, plus the '
          'expected number of the others who will.'),
    ('s', '4. The re-run decision'),
    ('p', 'A campaign is re-run at the same cost per paid member only when its cost per twelfth-month member is at or '
          'below the bar the growth lead set. A campaign that misses the bar may be re-planned and brought back as a '
          'new booking; it is not re-run on the same terms.'),
    ('s', '5. Records used'),
    ('p', 'Charges, retries and refunds are read from the payments export, sign-up tags from the attribution export, '
          'and media from the agency\'s invoices and credit notes. Agency-reported conversions are not used to count '
          'campaign members.'),
    ('s', 'Revision history'),
    ('t', [['Version', 'Effective', 'Change'],
           ['1', '1 February 2024', 'First issue: campaigns judged on cost per paid member.'],
           ['2', '1 January 2025', 'Cost per six-month member added beside cost per paid member.'],
           ['3', '1 July 2025', 'Cost per twelfth-month member replaces the six-month basis; the cost definition '
                                'adds first-month discounts.']]),
]


def standard_pdf(path):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib import colors
    ss = getSampleStyleSheet()
    body = ParagraphStyle('b', parent=ss['BodyText'], fontName='Helvetica', fontSize=9.5, leading=13.2,
                          spaceAfter=5)
    head = ParagraphStyle('h', parent=ss['Heading1'], fontName='Helvetica-Bold', fontSize=14, spaceAfter=6)
    sub = ParagraphStyle('s', parent=ss['Heading3'], fontName='Helvetica-Bold', fontSize=10.5, spaceBefore=8,
                         spaceAfter=3)
    meta = ParagraphStyle('m', parent=body, fontSize=8.5, textColor=colors.HexColor('#444444'))
    story = []
    for kind, txt in STANDARD:
        if kind == 'h':
            story.append(Paragraph(txt, head))
        elif kind == 'm':
            story.append(Paragraph(txt, meta)); story.append(Spacer(1, 4))
        elif kind == 's':
            story.append(Paragraph(txt, sub))
        elif kind == 'p':
            story.append(Paragraph(txt.replace("\\'", "'"), body))
        elif kind == 't':
            cell = ParagraphStyle('c', parent=body, fontSize=8.5, leading=10.5, spaceAfter=0)
            cellb = ParagraphStyle('cb', parent=cell, fontName='Helvetica-Bold')
            rows = [[Paragraph(c, cellb if i == 0 else cell) for c in row] for i, row in enumerate(txt)]
            tb = Table(rows, colWidths=[18 * mm, 32 * mm, 115 * mm])
            tb.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'),
                                    ('LINEBELOW', (0, 0), (-1, 0), .5, colors.black)]))
            story.append(tb)

    # the office's own PDF: the story as a Word document exported by LibreOffice Writer (reduce-house-fixes H1),
    # issued 19 June 2025 with the version 3 revision
    import officepdf
    when = dt.datetime(2025, 6, 19, 10, 15, 0, tzinfo=dt.timezone.utc)
    officepdf.build(path, story, title='Growth review standard v3', author='Corvane Sprachen GmbH',
                    subject='Growth review standard v3: definitions for paid acquisition campaign reviews',
                    footer='Corvane Sprachen GmbH, Growth. Internal. Growth review standard v3.',
                    created=when, modified=when, margin_mm=20, top_mm=20, bottom_mm=20, body_pt=9.5)


def metadata(path, files, distractors):
    prov = {
        'members': ('Corvane member export (constructed operating layer)', 'one row per paid account since launch'),
        'billing': ('Corvane payments export (constructed operating layer)', 'charge attempts and refunds, January 2022 to October 2026'),
        'lessons': ('Corvane lesson platform export (constructed operating layer)', 'booked and completed lessons by member, tutor and month'),
        'tutors': ('Corvane tutor directory export (constructed operating layer)', 'every tutor profile ever created'),
        'attribution': ('Corvane sign-up attribution export (constructed operating layer)', 'one row per sign-up with its UTM tags'),
        'agency': ('Fenwright Media invoices and close-out for AUT26 (constructed operating layer)', 'media invoiced and delivered for the campaign'),
        'plans': ('Corvane plan catalogue (constructed operating layer)', 'plans, prices and promotion codes'),
        'standard': ('Corvane growth review standard v3 (constructed governing document)', 'definitions for campaign reviews'),
        'ecb': ('European Central Bank, euro foreign exchange reference rates (real)', 'daily reference rates, January 2022 to 3 November 2026, as published'),
        'eurostat': ('Eurostat, Adult Education Survey, edat_aes_l21, number of foreign languages known (real)', 'as published, last update 27 October 2026'),
        'nps': ('Corvane in-app NPS responses (constructed operating layer)', 'monthly in-app survey scores, 2026'),
    }
    lic = {
        'ecb': 'ECB statistics: reuse permitted with the source acknowledged (European Central Bank)',
        'eurostat': 'Eurostat: CC BY 4.0 (reuse permitted with acknowledgement)',
    }
    src = {
        'ecb': 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.zip',
        'eurostat': 'https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/edat_aes_l21/',
    }
    out = {
        'task': 'task1',
        'decision': 'whether Corvane books the January and February 2027 re-run of its AUT26 acquisition campaign at the same cost per paid member',
        'deliverables': ['aut26_rerun_memo.docx', 'aut26_member_forecast.xlsx'],
        'pull_date': PULL_DATE.isoformat(),
        'files': [],
        'distractor_files': ['target/' + files[k] for k in distractors],
    }
    for k, name in files.items():
        what, covers = prov[k]
        out['files'].append({
            'path': 'target/' + name, 'source': what, 'covers': covers,
            'origin': src.get(k, 'generated by task1/generator from a monthly process; no LLM-written data'),
            'pulled_on': '2026-11-07' if k in src else PULL_DATE.isoformat(),
            'license': lic.get(k, 'constructed for this task; no third-party content'),
        })
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
        f.write('\n')
