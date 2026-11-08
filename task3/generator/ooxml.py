"""task3: OOXML packages (xlsx, docx) rewritten at one fixed time, members and core properties alike, so that two
builds are byte-identical."""
import io
import re
import zipfile


def _app_xml(names, kind, company):
    if kind == "xlsx":
        sheets = names
        n = len(sheets)
        parts = "".join("<vt:lpstr>%s</vt:lpstr>" % x for x in sheets)
        return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n<Properties xmlns="http://schemas.openxmlformats.org/'
                'officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/'
                'docPropsVTypes"><Application>Microsoft Excel</Application><DocSecurity>0</DocSecurity><ScaleCrop>false'
                '</ScaleCrop><HeadingPairs><vt:vector size="2" baseType="variant"><vt:variant><vt:lpstr>Worksheets</vt:lpstr>'
                '</vt:variant><vt:variant><vt:i4>%d</vt:i4></vt:variant></vt:vector></HeadingPairs><TitlesOfParts>'
                '<vt:vector size="%d" baseType="lpstr">%s</vt:vector></TitlesOfParts><Company>%s</Company><LinksUpToDate>'
                'false</LinksUpToDate><SharedDoc>false</SharedDoc><HyperlinksChanged>false</HyperlinksChanged><AppVersion>'
                '16.0300</AppVersion></Properties>' % (n, n, parts, company)).encode()
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n<Properties xmlns="http://schemas.openxmlformats.org/'
            'officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/'
            'docPropsVTypes"><Template>Normal.dotm</Template><TotalTime>94</TotalTime><Pages>2</Pages><Application>'
            'Microsoft Office Word</Application><DocSecurity>0</DocSecurity><Lines>96</Lines><Paragraphs>27</Paragraphs>'
            '<ScaleCrop>false</ScaleCrop><Company>%s</Company><LinksUpToDate>false</LinksUpToDate><SharedDoc>false'
            '</SharedDoc><HyperlinksChanged>false</HyperlinksChanged><AppVersion>16.0000</AppVersion></Properties>'
            % company).encode()


def normalize(path, created, modified, creator=None, company=None):
    """created, modified: naive datetimes written as UTC in docProps/core.xml; every member stamped at modified."""
    src = zipfile.ZipFile(io.BytesIO(open(path, "rb").read()))
    items = [(i.filename, src.read(i.filename)) for i in src.infolist()]
    src.close()
    names = dict(items)
    kind = "xlsx" if "xl/workbook.xml" in names else "docx"
    if company is not None:
        sheets = [m.decode() for m in re.findall(rb'<sheet [^>]*name="([^"]+)"', names.get("xl/workbook.xml", b""))]
        app = _app_xml(sheets, kind, company)
        if "docProps/app.xml" in names:
            items = [(n, app if n == "docProps/app.xml" else d) for n, d in items]
    out = io.BytesIO()
    stamp = (modified.year, modified.month, modified.day, modified.hour, modified.minute, modified.second)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for n, d in items:
            if n == "docProps/core.xml":
                d = re.sub(rb"(<dcterms:created[^>]*>)[^<]*(</dcterms:created>)",
                           lambda m: m.group(1) + created.strftime("%Y-%m-%dT%H:%M:%SZ").encode() + m.group(2), d)
                d = re.sub(rb"(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)",
                           lambda m: m.group(1) + modified.strftime("%Y-%m-%dT%H:%M:%SZ").encode() + m.group(2), d)
                d = re.sub(rb"(<dc:description>)[^<]*(</dc:description>)", lambda m: m.group(1) + m.group(2), d)
                d = re.sub(rb"(<cp:keywords>)[^<]*(</cp:keywords>)", lambda m: m.group(1) + m.group(2), d)
                if creator is not None:
                    d = re.sub(rb"(<dc:creator[^>]*>)[^<]*(</dc:creator>)", lambda m: m.group(1) + creator.encode() + m.group(2), d)
                    d = re.sub(rb"(<cp:lastModifiedBy[^>]*>)[^<]*(</cp:lastModifiedBy>)",
                               lambda m: m.group(1) + creator.encode() + m.group(2), d)
            zi = zipfile.ZipInfo(n, date_time=stamp)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o600 << 16
            z.writestr(zi, d)
    open(path, "wb").write(out.getvalue())
