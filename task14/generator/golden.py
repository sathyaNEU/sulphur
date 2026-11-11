"""task14: the golden deliverables, written from figures.json and the results object: the prices team's workbook
and the three slides for the launch briefing. Every number shown is the figures.json value at the same rounding."""
import datetime as dt
import os

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION, XL_LEGEND_POSITION
from pptx.enum.dml import MSO_LINE_DASH_STYLE
from pptx.util import Emu, Inches, Pt

import measure as MS
import postprocess

WORKBOOK = "private_rents_measure_2026Q4.xlsx"
SLIDES = "private_rents_launch_briefing.pptx"
ORG = "Penmarra Statistics Office"
AUTHOR = "Christine Buckley"
REG = ["NAT"] + MS.REGIONS
NAMES = {"NAT": "Penmarra", "HC": "Hallam Central", "HN": "Hallam North", "HE": "Hallam East", "HS": "Hallam South",
         "KC": "Kerrow Coast", "MV": "Midvale", "WS": "Westerly"}
BLUE = "2A78D6"
ORANGE = "EB6834"
ROUTE_LABELS = {
    "the golden": "This workbook: survey rises for small landlords, operators' own bonds, December projected",
    "careful but hurried: the panel's rises carried to every landlord":
        "Survey rises given to every landlord; December read off the register as it stands",
    "careful but hurried: the latest recorded rent carried forward at the panel's rate":
        "Latest recorded rent carried forward at the survey's rate; December as it stands",
    "careful but hurried: the recorded rent where an additional bond exists, the model otherwise":
        "Recorded rent wherever an additional bond exists, survey rises otherwise; December as it stands",
    "the additional bonds read as every rise": "Additional bonds read as every rise; December on a straight trend",
    "re-lettings tied by property identifier alone": "Re-lettings tied by property identifier only; December on a trend",
    "re-lettings against the earlier tenancy's starting rent":
        "Re-lettings priced against the earlier tenancy's starting rent; December on a trend",
    "the quarterly figures carried on a straight trend": "December on a straight trend through the quarters",
    "the September figure carried into December": "September figure carried into December",
    "the register read as it stands on 31 December": "December read off the register as it stands on 31 December",
    "the register as it stands, corrected by its own back-test":
        "December as it stands, corrected by that reading's errors on earlier Decembers",
    "December projected without the review not yet on file": "December projected without the 1 December operator review",
    "new-letting rents for the measure": "Median rent of new lettings in place of the measure",
}
INK = "0B0B0B"
INK2 = "52514E"
GRID = "D9D8D3"


def _hdr(ws, row, values, widths=None):
    for j, v in enumerate(values, 1):
        c = ws.cell(row=row, column=j, value=v)
        c.font = Font(bold=True)
        c.alignment = Alignment(wrap_text=True, vertical="bottom")
        c.border = Border(bottom=Side(style="thin", color="808080"))
    for j, w in enumerate(widths or [], 1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(j)].width = w


def workbook(F, res, path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Measure"
    ws["A1"] = "Private rents measure (bond-based): annual change, per cent"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = ("Total weekly rent payable on dwellings let under a bond on the last day of the quarter and of the same "
                "quarter a year earlier (PS-2026-07, 2.4). 2026Q4 projected from the register as at 27 November 2026.")
    ws["A2"].font = Font(italic=True, size=9, color=INK2)
    _hdr(ws, 4, ["Quarter", "Penmarra"] + ["%s (September 2026)" % NAMES[g] if False else NAMES[g] for g in MS.REGIONS],
         [12, 11] + [14] * 7)
    r = 5
    for q, v in F["series"].items():
        ws.cell(row=r, column=1, value=q)
        ws.cell(row=r, column=2, value=v).number_format = "0.0"
        if q == "2026Q3":
            for j, g in enumerate(MS.REGIONS, 3):
                ws.cell(row=r, column=j, value=F["sep26"][g]).number_format = "0.0"
        r += 1
    ws.cell(row=r, column=1, value="2026Q4 (projected)").font = Font(bold=True)
    for j, g in enumerate(REG, 2):
        c = ws.cell(row=r, column=j, value=F["dec26"][g])
        c.number_format = "0.0"
        c.font = Font(bold=True)
    ws.cell(row=r + 2, column=1, value="Regions are given for the September 2026 quarter and the December 2026 projection.").font = Font(size=9, color=INK2)
    ws.freeze_panes = "B5"

    ws = wb.create_sheet("Year to Sep 2026")
    ws["A1"] = "Year to September 2026"
    ws["A1"].font = Font(bold=True, size=12)
    _hdr(ws, 3, ["Region", "Bonded tenancies held 30 Sep 2026", "Dwellings re-let in the year", "Measure, per cent"],
         [18, 18, 16, 12])
    rr = 4
    for g in REG:
        ws.cell(row=rr, column=1, value=NAMES[g]).font = Font(bold=(g == "NAT"))
        ws.cell(row=rr, column=2, value=F["held"][g]).number_format = "#,##0"
        ws.cell(row=rr, column=3, value=F["relet_n"][g]).number_format = "#,##0"
        ws.cell(row=rr, column=4, value=F["sep26"][g]).number_format = "0.0"
        rr += 1
    rr += 1
    ws.cell(row=rr, column=1, value="Penmarra, by group").font = Font(bold=True)
    rr += 1
    _hdr(ws, rr, ["Group", "Change in rent payable, per cent", "Share whose rent rose, per cent",
                  "Contribution to the measure, points"])
    rr += 1
    c26 = F["contrib26"]
    rows = [("Continuing tenancies", F["cont_change"], F["cont_share"], c26["continuing"]),
            ("Dwellings re-let", F["relet_change"], None, c26["relet"]),
            ("All dwellings compared", F["sep26"]["NAT"], None, c26["continuing"] + c26["relet"])]
    for row in rows:
        ws.cell(row=rr, column=1, value=row[0])
        for j, v in enumerate(row[1:], 2):
            if v is None:
                continue
            c = ws.cell(row=rr, column=j, value=round(v, 2) if j >= 4 else v)
            c.number_format = "0.00" if j >= 4 else "0.0"
        rr += 1
    ws.cell(row=rr + 1, column=1, value=("Continuing tenancies' rises at an anniversary measured on the Rent Survey "
                                         "(design-weighted, by year and region); the block operators' rises from "
                                         "their own additional bonds. The share for small landlords' tenancies is the "
                                         "survey's share with a rise.")).font = Font(size=9, color=INK2)

    ws = wb.create_sheet("December 2026")
    ws["A1"] = "December 2026 quarter, projected"
    ws["A1"].font = Font(bold=True, size=12)
    _hdr(ws, 3, ["Region", "Annual change, per cent"], [18, 14])
    rr = 4
    for g in REG:
        ws.cell(row=rr, column=1, value=NAMES[g]).font = Font(bold=(g == "NAT"))
        ws.cell(row=rr, column=2, value=F["dec26"][g]).number_format = "0.0"
        rr += 1
    rr += 1
    _hdr(ws, rr, ["Penmarra, 90 per cent range", "From", "To"])
    ws.column_dimensions["C"].width = 30
    rr += 1
    ws.cell(row=rr, column=1, value="Annual change, per cent")
    ws.cell(row=rr, column=2, value=F["dec26_range"][0]).number_format = "0.0"
    ws.cell(row=rr, column=3, value=F["dec26_range"][1]).number_format = "0.0"
    rr += 2
    _hdr(ws, rr, ["Penmarra, by group: contribution, points", "Year to Sep 2026", "Year to Dec 2026", "Change"])
    ws.column_dimensions["D"].width = 12
    rr += 1
    cd_, c26_, sl_ = F["contrib_dec"], F["contrib26"], F["slow"]
    for label, k in (("Continuing tenancies", "continuing"), ("Dwellings re-let", "relet")):
        ws.cell(row=rr, column=1, value=label)
        for j, v in enumerate((c26_[k], cd_[k], sl_[k]), 2):
            ws.cell(row=rr, column=j, value=v).number_format = "0.00"
        rr += 1
    ws.cell(row=rr, column=1, value="All dwellings compared")
    for j, v in enumerate((c26_["continuing"] + c26_["relet"], cd_["continuing"] + cd_["relet"], sl_["fall"]), 2):
        ws.cell(row=rr, column=j, value=round(v, 2)).number_format = "0.00"
    rr += 2
    _hdr(ws, rr, ["Operator reviews in the quarter", "Rise, per cent", "On file at 27 Nov"])
    rr += 1
    for label, rise, onfile in (
            ("Landlord %s (build-to-rent), 1 November 2026 review (lodged bonds' median)" % F["b_landlord"],
             F["b_review_2026"],
             "part; %s tenancies completed at the same rise" % "{:,}".format(F["pending_n"])),
            ("Landlord %s (build-to-rent), 1 December 2026 review (September CPI %.1f plus %.1f)"
             % (F["a_landlord"], F["cpi_sep"]["2026"], F["a_margin"]),
             F["a_review_2026"], "no; applied to %s tenancies" % "{:,}".format(F["scheduled_n"]))):
        ws.cell(row=rr, column=1, value=label)
        ws.cell(row=rr, column=2, value=rise).number_format = "0.0"
        ws.cell(row=rr, column=3, value=onfile)
        rr += 1
    rr += 1
    _hdr(ws, rr, ["Same projection on earlier Decembers", "Projected", "Measured"])
    rr += 1
    for b in F["backtest"]:
        ws.cell(row=rr, column=1, value="December %d (from 27 November %d)" % (b["year"], b["year"]))
        ws.cell(row=rr, column=2, value=b["projected"]).number_format = "0.0"
        ws.cell(row=rr, column=3, value=b["actual"]).number_format = "0.0"
        rr += 1
    ws.cell(row=rr + 1, column=1, value=("Range: the Rent Survey resampled by dwelling within its strata (%d draws) "
                                         "with the projection's own error on the three earlier Decembers."
                                         % F["boot_n"])).font = Font(size=9, color=INK2)

    ws = wb.create_sheet("Routes")
    ws["A1"] = "Other constructions tested, and what each gives"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = "Annual change, per cent, Penmarra. The first row is the construction used in this workbook."
    ws["A2"].font = Font(italic=True, size=9, color=INK2)
    _hdr(ws, 3, ["Construction", "Year to Sep 2026", "Year to Dec 2026"], [92, 14, 14])
    rr = 4
    order = [k for k in ROUTE_LABELS if k in F["routes_sep"]] + [k for k in F["routes_sep"] if k not in ROUTE_LABELS]
    for name in order:
        sep, dec = F["routes_sep"][name], F["routes_dec"][name]
        name = ROUTE_LABELS.get(name, name)
        ws.cell(row=rr, column=1, value=name)
        ws.cell(row=rr, column=2, value=sep).number_format = "0.0"
        ws.cell(row=rr, column=3, value=dec).number_format = "0.0"
        rr += 1
    ws = wb.create_sheet("Notes")
    ws["A1"] = "Notes"
    ws["A1"].font = Font(bold=True, size=12)
    notes = [
        ("Definition", "Methods paper PS-2026-07, 2.1 to 2.7: dwellings let on the last day of both quarters, each at "
                       "the weekly rent payable on its own day; the breakdowns are computed the same way."),
        ("Coverage", "Bonded private tenancies only (2.7). Regions are the seven in use from 1 July 2024, by suburb, "
                     "for every quarter (2.6)."),
        ("Sources", "Tenancy Bond Board register: legacy extract to 5 March 2023 and online events to the close of "
                    "27 November 2026. Rent Survey to the September 2026 quarter. CPI, September 2026 quarter."),
        ("Rounding", "Annual changes to one decimal from unrounded totals; contributions to two decimals, and the "
                     "change in contribution taken from the rounded contributions."),
        ("December", "Projected: the quarter closes after the register extract. The range is shown for Penmarra only."),
    ]
    _hdr(ws, 3, ["Item", "Note"], [14, 110])
    for k, (a_, b_) in enumerate(notes, 4):
        ws.cell(row=k, column=1, value=a_).font = Font(bold=True)
        c = ws.cell(row=k, column=2, value=b_)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    wb.save(path)
    postprocess.normalize_ooxml(path, AUTHOR, AUTHOR, "2026-12-01T21:12:00Z", "2026-12-03T02:47:00Z", excel=True,
                                company=ORG)


def _text(slide, x, y, w, h, text, size=14, bold=False, color=INK):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    lines = text if isinstance(text, list) else [text]
    for i, ln in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = ln
        p.font.size = Pt(size)
        p.font.bold = bold
        p.font.color.rgb = RGBColor.from_string(color)
    return tb


def _axis_style(chart):
    for ax in (chart.category_axis, chart.value_axis):
        ax.tick_labels.font.size = Pt(11)
        ax.tick_labels.font.color.rgb = RGBColor.from_string(INK2)
        ax.format.line.color.rgb = RGBColor.from_string(GRID)
    chart.value_axis.has_major_gridlines = True
    chart.value_axis.major_gridlines.format.line.color.rgb = RGBColor.from_string(GRID)
    chart.value_axis.major_gridlines.format.line.width = Pt(0.75)


def _footer(slide, n):
    _text(slide, 0.6, 7.0, 10.5, 0.35, "Source: Tenancy Bond Board register to 27 November 2026; Rent Survey; CPI. "
                                       "Penmarra Statistics Office calculations (PS-2026-07).", 9, False, INK2)
    _text(slide, 12.2, 7.0, 0.6, 0.35, str(n), 9, False, INK2)


def slides(F, res, path):
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
    blank = prs.slide_layouts[6]
    # 1: the December figures
    s = prs.slides.add_slide(blank)
    lo, hi = F["dec26_range"]
    _text(s, 0.6, 0.4, 12.2, 0.8, "Rents up %.1f per cent in the year to December 2026, down from %.1f to September"
          % (F["dec26"]["NAT"], F["sep26"]["NAT"]), 24, True)
    _text(s, 0.6, 1.55, 5.2, 1.0, "%.1f per cent" % F["dec26"]["NAT"], 44, True)
    _text(s, 0.6, 2.55, 5.2, 1.4, ["Penmarra, year to the December 2026 quarter (projected)",
                                  "90 per cent range %.1f to %.1f" % (lo, hi),
                                  "Year to September 2026: %.1f per cent" % F["sep26"]["NAT"]], 16, False)
    _footer(s, 1)
    _text(s, 0.6, 4.0, 5.2, 2.8, ["Projected from the bond register as at 27 November 2026.",
                                  "The larger build-to-rent landlord's 1 December review: %.1f per cent (September "
                                  "CPI plus %.1f), against %.1f in 2025. The other's 1 November review: %.1f, against "
                                  "%.1f. Going rents have eased since July." % (F["a_review_2026"], F["a_margin"],
                                                                               F["a_review"]["2025"],
                                                                               F["b_review_2026"],
                                                                               F["b_review"]["2025"])],
          13, False, INK2)
    cd = CategoryChartData()
    order = sorted(MS.REGIONS, key=lambda g: -F["dec26"][g])
    cd.categories = [NAMES[g] for g in order]
    cd.add_series("Year to Dec 2026", [F["dec26"][g] for g in order])
    gf = s.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, Inches(6.2), Inches(1.2), Inches(6.6), Inches(5.6), cd)
    ch = gf.chart
    ch.has_legend = False
    ch.has_title = True
    ch.chart_title.text_frame.text = "Annual change to December 2026, per cent, by region"
    ch.chart_title.text_frame.paragraphs[0].font.size = Pt(13)
    pl = ch.plots[0]
    pl.gap_width = 60
    pl.has_data_labels = True
    pl.data_labels.number_format = "0.0"
    pl.data_labels.number_format_is_linked = False
    pl.data_labels.position = XL_LABEL_POSITION.OUTSIDE_END
    pl.data_labels.font.size = Pt(11)
    pl.data_labels.font.color.rgb = RGBColor.from_string(INK2)
    ser = pl.series[0]
    ser.format.fill.solid()
    ser.format.fill.fore_color.rgb = RGBColor.from_string(BLUE)
    ch.category_axis.reverse_order = True
    _axis_style(ch)
    ch.value_axis.minimum_scale = 0
    # 2: the path since 2022
    s = prs.slides.add_slide(blank)
    _text(s, 0.6, 0.4, 12.2, 0.8, "The measure peaked at %.1f per cent in %s and is projected at %.1f for December 2026"
          % (F["peak"], F["peak_q"], F["dec26"]["NAT"]), 26, True)
    cd = CategoryChartData()
    qs = list(F["series"].keys()) + ["2026Q4"]
    cd.categories = qs
    cd.add_series("Measured", [F["series"][q] for q in F["series"]] + [None])
    cd.add_series("Projected", [None] * (len(qs) - 2) + [F["series"]["2026Q3"], F["dec26"]["NAT"]])
    gf = s.shapes.add_chart(XL_CHART_TYPE.LINE_MARKERS, Inches(0.6), Inches(1.3), Inches(12.0), Inches(5.0), cd)
    ch = gf.chart
    ch.has_legend = True
    ch.legend.position = XL_LEGEND_POSITION.TOP
    ch.legend.include_in_layout = False
    ch.legend.font.size = Pt(11)
    for i, sr in enumerate(ch.plots[0].series):
        sr.format.line.color.rgb = RGBColor.from_string(BLUE)
        sr.format.line.width = Pt(2.25)
        sr.smooth = False
        sr.marker.size = 7
        sr.marker.format.fill.solid()
        sr.marker.format.fill.fore_color.rgb = RGBColor.from_string(BLUE)
        sr.marker.format.line.color.rgb = RGBColor.from_string(BLUE)
        if i == 1:
            sr.format.line.dash_style = MSO_LINE_DASH_STYLE.DASH
    _axis_style(ch)
    ch.value_axis.minimum_scale = 0
    ch.value_axis.tick_labels.number_format = "0.0"
    ch.value_axis.tick_labels.number_format_is_linked = False
    _text(s, 0.6, 6.3, 12, 0.5, "Annual change, per cent, Penmarra. The projected December figure %.1f has a 90 per "
                                "cent range of %.1f to %.1f." % (F["dec26"]["NAT"], lo, hi), 12, False, INK2)
    _footer(s, 2)
    # 3: the year to September
    s = prs.slides.add_slide(blank)
    sp = F["slow_pts"]
    _text(s, 0.6, 0.4, 12.2, 0.8, "From September to December the measure loses %.2f points: continuing tenancies "
          "%.2f, re-lettings %.2f" % (sp["fall"], sp["continuing"], sp["relet"]), 24, True)
    _text(s, 0.6, 1.4, 5.6, 4.8, [
        "Year to September 2026: %.1f per cent." % F["sep26"]["NAT"],
        "Continuing tenancies: rent payable up %.1f per cent, %.1f per cent of them with a rise." % (
            F["cont_change"], F["cont_share"]),
        "Dwellings re-let (%s in the year): up %.1f per cent on what the earlier tenancy paid." % (
            "{:,}".format(F["relet_n"]["NAT"]), F["relet_change"]),
        "Bonded tenancies in place on 30 September 2026: %s." % "{:,}".format(F["held"]["NAT"]),
        "Year to December 2026, projected: %.1f per cent." % F["dec26"]["NAT"],
    ], 15, False)
    cd = CategoryChartData()
    cd.categories = ["Year to Sep 2026", "Year to Dec 2026 (projected)"]
    cd.add_series("Continuing tenancies", [F["contrib26"]["continuing"], F["contrib_dec"]["continuing"]])
    cd.add_series("Dwellings re-let", [F["contrib26"]["relet"], F["contrib_dec"]["relet"]])
    gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_STACKED, Inches(6.6), Inches(1.3), Inches(6.2), Inches(5.0), cd)
    ch = gf.chart
    ch.has_title = True
    ch.chart_title.text_frame.text = "Contribution to the measure, points"
    ch.chart_title.text_frame.paragraphs[0].font.size = Pt(13)
    ch.has_legend = True
    ch.legend.position = XL_LEGEND_POSITION.TOP
    ch.legend.include_in_layout = False
    ch.legend.font.size = Pt(11)
    pl = ch.plots[0]
    pl.gap_width = 70
    pl.has_data_labels = True
    pl.data_labels.number_format = "0.00"
    pl.data_labels.number_format_is_linked = False
    pl.data_labels.font.size = Pt(11)
    pl.data_labels.font.color.rgb = RGBColor.from_string("FFFFFF")
    for sr, col in zip(pl.series, (BLUE, ORANGE)):
        sr.format.fill.solid()
        sr.format.fill.fore_color.rgb = RGBColor.from_string(col)
        sr.format.line.color.rgb = RGBColor.from_string("FFFFFF")
        sr.format.line.width = Pt(1.5)
    _axis_style(ch)
    ch.value_axis.minimum_scale = 0
    ch.value_axis.tick_labels.number_format = "0.0"
    ch.value_axis.tick_labels.number_format_is_linked = False
    _footer(s, 3)
    prs.save(path)
    postprocess.normalize_pptx(path, AUTHOR, AUTHOR, "2026-12-02T03:30:00Z", "2026-12-03T03:05:00Z",
                               "Private rents measure: launch briefing", ORG)


def write(F, res, golden_dir):
    os.makedirs(golden_dir, exist_ok=True)
    workbook(F, res, os.path.join(golden_dir, WORKBOOK))
    slides(F, res, os.path.join(golden_dir, SLIDES))
