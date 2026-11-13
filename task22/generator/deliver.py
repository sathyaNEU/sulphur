"""task22 architecture 2, the golden deliverables: the engineering manager's workbook (each district's monthly gas
balance, the twelve months to September 2026, the accounts that took gas without authorization, the gas temperature
the meters saw, the 2027 changeouts' pace) and the short deck for the Utilities Commission, both from the results
that write figures.json."""
import datetime as dt
import os

import numpy as np
import openpyxl
from openpyxl.styles import Alignment, Font
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE
from pptx.util import Emu, Pt

import analysis as A
import params as P
import postprocess

WORKBOOK = "bpu_district_gas_balance_2023-10_2026-09.xlsx"
DECK = "lauf_program_2027_commission.pptx"
INK, MUTED, BLUE, GRAY = "1F1F1F", "6B6B6B", "2A78D6", "B5B4AE"
MCF = "#,##0"
PCT = "0.00"


def _hdr(ws, row, cols, widths=None):
    for j, h in enumerate(cols, 1):
        c = ws.cell(row=row, column=j, value=h)
        c.font = Font(bold=True)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for j, wd in enumerate(widths or [], 1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(j)].width = wd


def workbook(path, R, figs, F):
    mon = R["monthly"]
    agg = R["agg"]
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Monthly balance"
    ws["A1"] = "District gas balance by month, Mcf at 14.73 psia and 60 F (October 2023 to September 2026)"
    ws["A1"].font = Font(bold=True, size=12)
    cols = ["Month", "District", "Gas in at regulator stations", "Billed volume, cycle-read meters",
            "Under-registration, meters without temperature compensation", "Corrector customers", "Own use",
            "Third-party damage", "Taken without authorization", "Leak loss"]
    _hdr(ws, 3, cols, [9, 15, 13, 14, 18, 12, 9, 10, 13, 10])
    r = 4
    order = sorted(mon.itertuples(), key=lambda x: (x.month, P.DCODES.index(x.district)))
    for m in order:
        ws.append([m.month, P.DNAME[m.district], round(m.inflow, 1), round(m.billed, 1), round(m.under, 1),
                   round(m.evc, 1), round(m.own, 1), round(m.dmg, 1), round(m.div, 1), round(m.leak, 1)])
        r += 1
    for col in "CDEFGHIJ":
        for k in range(4, r):
            ws["%s%d" % (col, k)].number_format = "#,##0.0"
    ws.freeze_panes = "C4"
    ws = wb.create_sheet("Twelve months to Sep 2026")
    ws["A1"] = "Twelve months ending September 30, 2026, Mcf"
    ws["A1"].font = Font(bold=True, size=12)
    cols = ["District", "Gas in", "Billed volume", "Under-registration", "Corrector customers", "Own use", "Damage",
            "Taken without authorization", "Leak loss", "Leak loss, % of gas in", "Meters without compensation",
            "Under-registration, % of their billed volume", "Main replacement 2027-2029", "2027 changeout"]
    _hdr(ws, 3, cols, [15, 11, 12, 14, 12, 9, 9, 13, 10, 11, 12, 15, 13, 11])
    k = 4
    for c in P.DCODES:
        a = agg.loc[c]
        ur = float(a["ur_pct"]) if np.isfinite(a["ur_pct"]) else None
        elig = int(a["ntc_meters"]) >= P.CHANGEOUT_MIN_METERS
        ws.append([P.DNAME[c], round(a["inflow"], 0), round(a["billed"], 0), round(a["under"], 0),
                   round(a["evc"], 0), round(a["own"], 0), round(a["dmg"], 0), round(a["div"], 0),
                   round(a["leak"], 0), round(float(a["leak_pct"]), 2), int(a["ntc_meters"]),
                   round(ur, 2) if ur is not None else None,
                   "Yes" if c in R["designated"] else "No",
                   "Yes" if c in R["changeout"] else ("No" if elig else "No (fewer than 100 meters)")])
        k += 1
    ws.append(["All districts", round(agg["inflow"].sum(), 0), round(agg["billed"].sum(), 0),
               round(agg["under"].sum(), 0), round(agg["evc"].sum(), 0), round(agg["own"].sum(), 0),
               round(agg["dmg"].sum(), 0), round(agg["div"].sum(), 0), round(agg["leak"].sum(), 0),
               round(100 * agg["leak"].sum() / agg["inflow"].sum(), 2)])
    for col in "BCDEFGHI":
        for j in range(4, k + 1):
            ws["%s%d" % (col, j)].number_format = MCF
    for col in "JL":
        for j in range(4, k + 1):
            ws["%s%d" % (col, j)].number_format = PCT
    ws.cell(row=k + 2, column=1, value="Main replacement: leak loss over 1.0% of gas in (Rule 1). Changeout: "
            "under-registration over 3.5% of the billed volume, at least 100 meters (Rule 2).").font = Font(italic=True,
                                                                                                         size=8)
    ws = wb.create_sheet("Without authorization")
    ws["A1"] = "Accounts that took gas without authorization, October 2025 to September 2026"
    ws["A1"].font = Font(bold=True, size=12)
    _hdr(ws, 3, ["Premise", "District", "Finding", "Use first fell", "Gas not registered, Mcf"], [11, 15, 14, 13, 14])
    dv = R["diversion"].sort_values(["district", "PremiseID"]) if len(R["diversion"]) else []
    for d in (dv.itertuples() if len(dv) else []):
        ws.append([int(d.PremiseID), P.DNAME[d.district], d.kind, d.first_month, round(d.mcf_window, 0)])
    ws = wb.create_sheet("Gas temperature")
    ws["A1"] = "Gas temperature at meters without compensation, monthly mean, F"
    ws["A1"].font = Font(bold=True, size=12)
    tp = R["tpar"]
    ws["A2"] = ("Outdoor sets: soil at 20 in + %.3f x (air - soil) + %.2f F when the air is below 45 F + %.2f F, "
                "fitted on the 2024-25 loggers. Indoor: from the indoor loggers on the soil at 40 in."
                % (tp.get("k", 0), tp.get("wall", 0), tp.get("c0", 0)))
    _hdr(ws, 4, ["Month", "Airport air", "Outdoor meters", "Indoor meters"], [10, 11, 13, 13])
    Wx = A.weather(F)
    T_out, T_in, _ = A.gas_temp(F, Wx, "soil")
    for m in A.MONTHS:
        msk = (A.DAYS.year == m.year) & (A.DAYS.month == m.month)
        ws.append([str(m), round(float(Wx["air"][msk].mean()), 1), round(float(T_out[msk].mean()), 1),
                   round(float(T_in[msk].mean()), 1)])
    ws = wb.create_sheet("2027 changeouts")
    ws["A1"] = "Changeouts the 2027 plan schedules, done before November 1, 2027 at the 2024-25 pace"
    ws["A1"].font = Font(bold=True, size=12)
    pl = R["plan"]
    _hdr(ws, 3, ["Meter location", "Meters scheduled", "Expected done before the season"], [15, 15, 18])
    plan = F["plan2027"]
    for loc in ("Outside", "Inside"):
        ws.append([loc, int((plan["MeterLocation"] == loc).sum()), round(pl["by_loc"].get(loc, 0.0), 0)])
    ws.append(["All", pl["n"], round(pl["done"], 0)])
    wb.save(path)


def deck(path, R, figs):
    prs = Presentation()
    prs.slide_width, prs.slide_height = Emu(12192000), Emu(6858000)
    blank = prs.slide_layouts[6]

    def text(slide, x, y, w, h, lines, size=16):
        tf = slide.shapes.add_textbox(Emu(x), Emu(y), Emu(w), Emu(h)).text_frame
        tf.word_wrap = True
        for k, line in enumerate(lines):
            p = tf.paragraphs[0] if k == 0 else tf.add_paragraph()
            p.text = line
            p.runs[0].font.size = Pt(size)
            p.runs[0].font.color.rgb = RGBColor.from_string(INK)
            p.space_after = Pt(9)
        return tf

    def title(slide, t, sub=None):
        tf = text(slide, 457200, 300000, 11277600, 700000, [t], 24)
        tf.paragraphs[0].runs[0].font.bold = True
        if sub:
            q = tf.add_paragraph()
            q.text = sub
            q.runs[0].font.size = Pt(13)
            q.runs[0].font.color.rgb = RGBColor.from_string(MUTED)
        q = slide.shapes.add_textbox(Emu(457200), Emu(6400000), Emu(10800000), Emu(300000)).text_frame.paragraphs[0]
        q.text = "Regulator station correctors, AMR reads and accounts to October 2026; Resolution 2026-11"
        q.runs[0].font.size = Pt(9)
        q.runs[0].font.color.rgb = RGBColor.from_string(MUTED)

    agg = R["agg"]
    des = [P.DNAME[c] for c in R["designated"]]
    cho = [P.DNAME[c] for c in R["changeout"]]
    s = prs.slides.add_slide(blank)
    title(s, "2027 LAUF program: mains in %s; meters in %d districts" % (", ".join(des), len(cho)),
          "Utilities Commission, December 2026")
    text(s, 457200, 1500000, 11277600, 4600000, [
        "Main replacement 2027-2029 (Rule 1): %s. Each lost more than 1.0%% of its gas to leaks in the twelve months "
        "to September 2026." % ", ".join(des),
        "Meter changeout 2027 (Rule 2): %s." % ", ".join(cho),
        "Of the %d changeouts already scheduled in Old Town and Downtown, about %d will be done before the 2027-28 "
        "heating season; meters inside take an appointment." % (R["plan"]["n"], int(round(R["plan"]["done"])))], 17)
    s = prs.slides.add_slide(blank)
    title(s, "Leak loss by district, twelve months to September 2026",
          "Per cent of gas in at the regulator stations; the program line is 1.0%")
    cd = CategoryChartData()
    order = sorted(P.DCODES, key=lambda c: -float(agg.loc[c, "leak_pct"]))
    cd.categories = [P.DNAME[c] for c in order]
    cd.add_series("Leak loss %", [round(float(agg.loc[c, "leak_pct"]), 2) for c in order])
    ch = s.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, Emu(457200), Emu(1300000), Emu(11277600), Emu(4900000),
                            cd).chart
    ch.has_legend = False
    ch.font.size = Pt(11)
    pl = ch.plots[0]
    pl.has_data_labels = True
    pl.data_labels.number_format = "0.00"
    pl.data_labels.number_format_is_linked = False
    ch.category_axis.reverse_order = True
    for i, c in enumerate(order):
        pt = pl.series[0].points[i]
        pt.format.fill.solid()
        pt.format.fill.fore_color.rgb = RGBColor.from_string(BLUE if c in R["designated"] else GRAY)
    s = prs.slides.add_slide(blank)
    title(s, "Most of the reported LAUF is gas the meters did not register",
          "Twelve months to September 2026, Mcf")
    tot = agg.sum()
    text(s, 457200, 1450000, 11277600, 4700000, [
        "Gas in at the regulator stations: {:,.0f} Mcf; leak loss {:,.0f} Mcf ({:.2f}%).".format(
            tot["inflow"], tot["leak"], 100 * tot["leak"] / tot["inflow"]),
        "Meters without temperature compensation registered the gas at the temperature it reached them, near the "
        "soil's under the 2025-26 snow, not the airport's air: {:,.0f} Mcf more than they billed.".format(tot["under"]),
        "Gas taken without authorization: {:,.0f} Mcf at {} accounts (bypasses and furnace taps).".format(
            tot["div"], figs["R4_diversion"]["accounts"]),
        "Own use {:,.0f} Mcf; third-party damage {:,.0f} Mcf as reported.".format(tot["own"], tot["dmg"])], 16)
    s = prs.slides.add_slide(blank)
    title(s, "Where the meters under-register", "Under-registration, per cent of the volume billed for meters "
                                                "without compensation; Rule 2's line is 3.5%")
    cd = CategoryChartData()
    elig = [c for c in P.DCODES if int(agg.loc[c, "ntc_meters"]) >= P.CHANGEOUT_MIN_METERS]
    order = sorted(elig, key=lambda c: -float(agg.loc[c, "ur_pct"]))
    cd.categories = [P.DNAME[c] for c in order]
    cd.add_series("Under-registration %", [round(float(agg.loc[c, "ur_pct"]), 2) for c in order])
    ch = s.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, Emu(457200), Emu(1300000), Emu(11277600), Emu(4900000),
                            cd).chart
    ch.has_legend = False
    ch.font.size = Pt(11)
    pl = ch.plots[0]
    pl.has_data_labels = True
    pl.data_labels.number_format = "0.00"
    pl.data_labels.number_format_is_linked = False
    ch.category_axis.reverse_order = True
    for i, c in enumerate(order):
        pt = pl.series[0].points[i]
        pt.format.fill.solid()
        pt.format.fill.fore_color.rgb = RGBColor.from_string(BLUE if c in R["changeout"] else GRAY)
    prs.save(path)


def write(F, R, figs, gold_dir):
    os.makedirs(gold_dir, exist_ok=True)
    wbp = os.path.join(gold_dir, WORKBOOK)
    dkp = os.path.join(gold_dir, DECK)
    workbook(wbp, R, figs, F)
    deck(dkp, R, figs)
    postprocess.normalize_ooxml(wbp, P.ENGINEER, P.ENGINEER, "2026-11-09T14:12:00Z", "2026-11-12T21:47:33Z",
                                excel=True, company=P.ORG)
    postprocess.normalize_pptx(dkp, P.ENGINEER, P.ENGINEER, "2026-11-11T15:30:00Z", "2026-11-12T22:05:41Z",
                               title="2027 LAUF program", company=P.ORG)
    postprocess.own_mtimes(gold_dir, {})
