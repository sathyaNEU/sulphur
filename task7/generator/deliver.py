"""The golden deliverables, exactly what the prompt asks for: a CSV with a row per proposal, a workbook showing how each
figure comes from the data (the call on its first sheet), and a few slides for the board. Every number is read from
figures.json, so the files, the answer blocks and the checks carry one set of figures."""
import csv
import datetime as dt
import os
import sys

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_LABEL_POSITION
from pptx.util import Emu, Inches, Pt

HERE = os.path.dirname(os.path.abspath(__file__))
WRITERS = os.path.join(os.path.dirname(os.path.dirname(HERE)), ".claude", "skills", "reduce-house-fixes", "scripts", "writers")
sys.path.insert(0, WRITERS)
import postprocess  # noqa: E402
import params as P  # noqa: E402

FILES = {"csv": "load_management_proposals_2027.csv", "xlsx": "load_management_trial_2026.xlsx",
         "pptx": "load_management_2027_board.pptx"}
ORDER = ["rep_w", "rep_n", "fix_t", "fix_w", "recon_in", "recon_out"]
NOS = {m: no for m, no, _ in P.PROPOSALS}
SCOPE = {"rep_w": "new VHF site at Kettle Ridge", "rep_n": "new FLEX site at the Halverson elevator",
         "fix_t": "A/C switches installed through 2015, Larkin district, not on the reconnection lists",
         "fix_w": "A/C switches installed through 2015, Medora Flats district, not on the reconnection lists",
         "recon_in": "replaced units after the switch went in, within 14 km of the nearest transmitter serving the switch",
         "recon_out": "replaced units after the switch went in, more than 14 km from the nearest transmitter serving the switch"}


PROPER = ("Kettle", "Halverson", "Larkin", "Medora")


def lname(n):
    """A proposal's name inside a sentence: proper names keep their capital, generic ones lose it."""
    return n if n.split()[0] in PROPER else n[0].lower() + n[1:]


def call_sentence(F):
    fund, rej = F["funded"], F["rejected"]
    return "Fund the %s, the %s and the %s; do not fund the %s, the %s or the %s." % tuple(
        [lname(n) for n in fund] + [lname(n) for n in rej])


def write_csv(path, F):
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\r\n")
        w.writerow(["proposal_no", "proposal", "scope", "premises_visited", "kw_added_2027", "kw_band_low", "kw_band_high",
                    "break_even_kw", "annual_cost_usd", "cost_per_kw_year_usd", "fund"])
        for m in ORDER:
            p = F["proposals"][m]
            w.writerow([NOS[m], p["name"], SCOPE[m], p["premises"] if p["premises"] is not None else "", p["kw"],
                        p["band"][0], p["band"][1], p["breakeven"], p["cost"],
                        "%.1f" % p["cost_per_kw"] if p["cost_per_kw"] else "", "yes" if p["funded"] else "no"])


def _hdr(ws, row=1):
    for c in ws[row]:
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="DDE5EE")
        c.alignment = Alignment(wrap_text=True, vertical="top")


def write_xlsx(path, F):
    wb = Workbook()
    ws = wb.active
    ws.title = "Call"
    ws["A1"] = "2027 load management proposals: what the 2026 dispatch trial says each adds at the wholesale peak"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A3"] = call_sentence(F)
    ws["A3"].font = Font(bold=True)
    ws["A4"] = ("Together the three add %s kW at the coincident peak for USD %s a year, USD %.1f a kW-year against the "
                "USD 88 a kW is worth." % (format(F["plan_kw"], ","), format(F["plan_cost"], ","), F["plan_cost_per_kw"]))
    ws.append([])
    ws.append(["Proposal", "kW added in 2027", "Band", "Break-even kW", "Annual cost (USD)", "Fund"])
    _hdr(ws, 6)
    for m in ORDER:
        p = F["proposals"][m]
        ws.append([p["name"], p["kw"], "%d to %d" % tuple(p["band"]), p["breakeven"], p["cost"], "yes" if p["funded"] else "no"])
    ws.append([])
    ws.append(["Shares the proposals rest on", "Per 100", "Band"])
    _hdr(ws, ws.max_row)
    ws.append(["Shed commands that get through at the fringe (more than 20 km), against switches within 8 km",
               F["c1_through"], "%d to %d" % tuple(F["c1_through_band"])])
    ws.append(["Switches installed through 2015 that still work (premises with no replaced unit)", F["c2_work"],
               "%d to %d" % tuple(F["c2_work_band"])])
    ws.append(["Switches still wired in where the air conditioner was replaced since", F["c3_wired"],
               "%d to %d" % tuple(F["c3_wired_band"])])
    for col, wd in zip("ABCDEF", [66, 16, 14, 14, 17, 8]):
        ws.column_dimensions[col].width = wd
    # the step record
    ws2 = wb.create_sheet("Steps")
    C = F["counts"]
    ws2.append(["Measure", "Value", "Source"])
    _hdr(ws2)
    for row in [("Event days in the 2026 trial", C["events"], "paging_encoder_log_2026.csv"),
                ("Group shed commands", C["commands"], "paging_encoder_log_2026.csv (first transmit of each group)"),
                ("Feeders", C["feeders"], "scada_point_list.csv"),
                ("Feeder steps (one per command per feeder)", C["steps"], "scada_feeder_1min_2026.csv"),
                ("Step measured as", "mean of the 5 minutes from the transmit minute less the 5 before, held readings out", ""),
                ("Active A/C switches on the register at 30 September 2026", C["switches"], "lm_switch_register.csv"),
                ("Switches installed through 2015", C["old"], "lm_switch_register.csv"),
                ("Switches with a replaced unit after install (rebate or permit)", C["flagged"],
                 "hvac_rebates_2012_2026.csv, county_mechanical_permits_2010_2026.csv"),
                ("Delivered at the coincident-peak index (kW)", F["delivered"], "the fitted model below")]:
        ws2.append(list(row))
    ws2.column_dimensions["A"].width = 58
    ws2.column_dimensions["B"].width = 26
    ws2.column_dimensions["C"].width = 62
    # the fitted model
    ws3 = wb.create_sheet("Model")
    ws3.append(["Term", "Value", "Read as"])
    _hdr(ws3)
    q = F["fit"]["q"]
    labels = ["within 8 km", "8 to 14 km", "14 to 20 km", "more than 20 km"]
    for i, lab in enumerate(labels):
        ws3.append(["Reception, %s of an on-air transmitter of the switch's own system" % lab, q[i], "against within 8 km"])
    ws3.append(["Replaced unit: share of the switch's delivery kept", F["fit"]["c_connected"], "against no replaced unit"])
    for i, a in enumerate(F["fit"]["a"]):
        ws3.append(["District term, %s" % P.DISTRICTS[i], a, "against Larkin"])
    for g, h in enumerate(F["fit"]["h"]):
        ws3.append(["Paging group AC-%02d: kW a switch delivers within 8 km at index 1" % (g + 1), h, "Larkin, no replaced unit"])
    ws3.append(["A working switch near a transmitter at index 1 (study homes that respond)", F["fit"]["working_kw"], "kW"])
    ws3.append(["Study homes: mean response per enrolled switch at index 1", F["fit"]["study_itt"], "kW"])
    ws3.append(["Study homes that respond (per 100)", F["fit"]["study_share"], "mean response over 0.25 kW"])
    ws3.column_dimensions["A"].width = 76
    ws3.column_dimensions["B"].width = 12
    ws3.column_dimensions["C"].width = 30
    # the bridge
    ws4 = wb.create_sheet("Bridge")
    ws4.append(["Line", "kW at the coincident-peak index", "Band"])
    _hdr(ws4)
    ws4.append(["What the switches could take off (each as a working switch near a transmitter)", F["could_shed"], ""])
    ws4.append(["Commands not received", -F["lost_reach"], "%d to %d" % tuple(F["lost_reach_band"])])
    ws4.append(["Received but the switch failed", -F["lost_hw"], "%d to %d" % tuple(F["lost_hw_band"])])
    ws4.append(["Working but not connected to the air conditioner", -F["lost_unwired"], "%d to %d" % tuple(F["lost_unwired_band"])])
    ws4.append(["Delivered", F["delivered"], ""])
    ws4.column_dimensions["A"].width = 72
    ws4.column_dimensions["B"].width = 30
    ws4.column_dimensions["C"].width = 14
    # the proposals in full
    ws5 = wb.create_sheet("Proposals")
    ws5.append(["No.", "Proposal", "Premises visited", "Annual cost (USD)", "Break-even kW", "kW added in 2027", "Band",
                "USD a kW-year", "Fund"])
    _hdr(ws5)
    for m in ORDER:
        p = F["proposals"][m]
        ws5.append([NOS[m], p["name"], p["premises"] if p["premises"] is not None else "", p["cost"], p["breakeven_1"], p["kw"],
                    "%d to %d" % tuple(p["band"]), p["cost_per_kw"] if p["cost_per_kw"] else "", "yes" if p["funded"] else "no"])
    ws5.append([])
    ws5.append(["", "Funded plan", "", F["plan_cost"], "", F["plan_kw"], "%d to %d" % tuple(F["plan_kw_band"]),
                F["plan_cost_per_kw"], ""])
    for col, wd in zip("ABCDEFGHI", [10, 34, 16, 17, 14, 16, 14, 14, 7]):
        ws5.column_dimensions[col].width = wd
    # the routes
    ws6 = wb.create_sheet("Routes")
    ws6.append(["Route", "Kettle Ridge", "Halverson", "Larkin round", "Medora Flats round", "Within 14 km", "Outlying",
                "Funds"])
    _hdr(ws6)
    rows = [("This analysis", {m: F["proposals"][m]["kw"] for m in ORDER}, F["funded"]),
            ("Coverage map read as it stands (every premise covered)", F["lattice"]["S1"], F["lattice"]["S1"]["funded"]),
            ("Test log read as it stands (96 in 100 pass)", F["lattice"]["S2"], F["lattice"]["S2"]["funded"]),
            ("Work orders read as they stand (9 in 100 unwired)", F["lattice"]["S3"], F["lattice"]["S3"]["funded"]),
            ("All three records as they stand", F["routes"]["reflex"], F["routes"]["reflex"]["funded"]),
            ("Study homes carried to the fleet", F["routes"]["rigorous"], F["routes"]["rigorous"]["funded"]),
            ("Reach to the nearest listed transmitter of either system", F["routes"]["generous"], F["routes"]["generous"]["funded"])]
    for lab, v, fund in rows:
        ws6.append([lab] + [v[m] for m in ORDER] + ["; ".join(fund) if fund else "none"])
    ws6.append([])
    ws6.append(["Break-even kW"] + [F["proposals"][m]["breakeven"] for m in ORDER] + [""])
    ws6.column_dimensions["A"].width = 56
    for col in "BCDEFG":
        ws6.column_dimensions[col].width = 13
    ws6.column_dimensions["H"].width = 70
    # the variants
    ws7 = wb.create_sheet("Variants")
    ws7.append(["Rebuild", "Kettle Ridge", "Halverson", "Larkin round", "Medora Flats round", "Within 14 km", "Outlying",
                "Fringe lost (per 100)", "Pre-2016 failed (per 100)", "Replaced unwired (per 100)"])
    _hdr(ws7)
    for v, f in F["family"].items():
        ws7.append([v] + [int(round(f[m])) for m in ORDER] + [int(round(100 * f["c1_fringe_loss"])),
                                                              int(round(100 * f["c2_failed_old"])),
                                                              int(round(100 * f["c3_unwired"]))])
    ws7.column_dimensions["A"].width = 50
    for col in "BCDEFGHIJ":
        ws7.column_dimensions[col].width = 13
    ws8 = wb.create_sheet("Notes")
    for line in [
        ("As of", "Switch register, paging site register and replaced-unit records at 30 September 2026; trial 1 June to "
                  "30 September 2026 (60 event afternoons)."),
        ("Footing", "kW during a shed at Sunflower Basin's cooling index of the four 2026 coincident-peak afternoons (1.15), "
                    "every listed transmitter on the air, each proposal on its own against present practice (work plan 6.4)."),
        ("Break-even", "Annual cost over USD 88 a kW-year (four summer months at the USD 22.00 demand rate)."),
        ("Steps", "Mean feeder kW over the five minutes from a group's first transmit, less the five minutes before; "
                  "held historian readings (three or more equal readings in a row) left out."),
        ("Not counted", "Water heater switches, switches removed from the register, and the load research homes' own "
                        "switches (not on the switch register)."),
        ("Rounding", "kW to the whole kW after summing; shares per 100; USD a kW-year to one decimal. Bands are the range "
                     "of the 78 rebuilds on the Variants sheet with a quarter of its width either side.")]:
        ws8.append(list(line))
    ws8.column_dimensions["A"].width = 14
    ws8.column_dimensions["B"].width = 110
    for row in ws8.iter_rows():
        row[1].alignment = Alignment(wrap_text=True, vertical="top")
        row[0].font = Font(bold=True)
    for sh, hdr_row in (("Steps", 1), ("Model", 1), ("Bridge", 1), ("Proposals", 1), ("Routes", 1), ("Variants", 1)):
        wb[sh].freeze_panes = "B%d" % (hdr_row + 1)
    for row in wb["Call"].iter_rows(min_row=7, max_row=12):
        row[1].number_format = "#,##0"
        row[3].number_format = "#,##0"
        row[4].number_format = "#,##0"
    for row in wb["Proposals"].iter_rows(min_row=2):
        row[2].number_format = "#,##0"
        row[3].number_format = "#,##0"
        row[4].number_format = "#,##0.0"
        row[5].number_format = "#,##0"
        row[7].number_format = "0.0"
    for row in wb["Bridge"].iter_rows(min_row=2):
        row[1].number_format = "#,##0"
    for row in wb["Model"].iter_rows(min_row=2):
        row[1].number_format = "0.000"
    for row in wb["Routes"].iter_rows(min_row=2):
        for c in row[1:7]:
            c.number_format = "#,##0"
    for s in wb.worksheets:
        s.sheet_view.showGridLines = s.title not in ("Call", "Notes")
    wb.save(path)


def _bar(slide, x, y, w, h, cats, series, kind=XL_CHART_TYPE.BAR_CLUSTERED, stacked=False, colours=None, labels=True):
    cd = CategoryChartData()
    cd.categories = cats
    for name, vals in series:
        cd.add_series(name, vals)
    gf = slide.shapes.add_chart(kind, x, y, w, h, cd)
    ch = gf.chart
    ch.has_legend = len(series) > 1
    if ch.has_legend:
        ch.legend.position = XL_LEGEND_POSITION.BOTTOM
        ch.legend.include_in_layout = False
        ch.legend.font.size = Pt(11)
    ch.font.size = Pt(11)
    for i, s in enumerate(ch.series):
        if colours and colours[i] is not None:
            s.format.fill.solid()
            s.format.fill.fore_color.rgb = colours[i]
        elif colours:
            s.format.fill.background()
        if labels and (not colours or colours[i] is not None):
            s.data_labels.show_value = True
            s.data_labels.font.size = Pt(10)
            s.data_labels.number_format = "#,##0"
            s.data_labels.number_format_is_linked = False
    return ch


def _title(slide, text, sub=None):
    tb = slide.shapes.add_textbox(Inches(0.55), Inches(0.35), Inches(12.2), Inches(0.9))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(24)
    p.font.bold = True
    if sub:
        p2 = tf.add_paragraph()
        p2.text = sub
        p2.font.size = Pt(14)


def write_pptx(path, F):
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
    blank = prs.slide_layouts[6]
    # 1: the call
    s = prs.slides.add_slide(blank)
    _title(s, "2027 load management: fund three of the six proposals")
    tb = s.shapes.add_textbox(Inches(0.6), Inches(1.5), Inches(12.0), Inches(5.4))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = call_sentence(F)
    p.font.size = Pt(20)
    p.font.bold = True
    lines = ["Together they add %s kW at Sunflower Basin's coincident peak for USD %s a year: USD %.1f a kW-year, against the "
             "USD 88 a kilowatt saves." % (format(F["plan_kw"], ","), format(F["plan_cost"], ","), F["plan_cost_per_kw"]),
             "Only %d in 100 shed commands get through at the edge of paging coverage, %d in 100 of the switches installed "
             "through 2015 still work, and %d in 100 are still wired in where the air conditioner has been replaced." % (
                 F["c1_through"], F["c2_work"], F["c3_wired"]),
             "Read as they stand, the coverage map, the test log and the work orders fund none of the six."]
    for t in lines:
        q = tf.add_paragraph()
        q.text = t
        q.font.size = Pt(16)
        q.space_before = Pt(14)
    # 2: the bridge
    s = prs.slides.add_slide(blank)
    _title(s, "Where the shed goes: %s kW delivered of %s kW the switches could take off" % (
        format(F["delivered"], ","), format(F["could_shed"], ",")), "kW at the coincident-peak cooling index (1.15)")
    cats = ["Could take off", "Commands not received", "Switch failed", "Not connected", "Delivered"]
    top = F["could_shed"]
    a, b, c = F["lost_reach"], F["lost_hw"], F["lost_unwired"]
    base = [0, top - a, top - a - b, top - a - b - c, 0]
    vals = [top, a, b, c, F["delivered"]]
    ch = _bar(s, Inches(0.6), Inches(1.6), Inches(12.1), Inches(5.5), cats, [("base", base), ("kW", vals)],
              kind=XL_CHART_TYPE.COLUMN_STACKED, colours=[None, RGBColor(0x25, 0x7D, 0xE0)])
    ch.has_legend = False
    ch.plots[0].gap_width = 60
    ch.value_axis.tick_labels.number_format = "#,##0"
    ch.value_axis.tick_labels.number_format_is_linked = False
    lab = ch.series[1].data_labels
    lab.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    lab.font.bold = True
    # 3: each proposal against its break-even
    s = prs.slides.add_slide(blank)
    _title(s, "Three proposals add more peak kW in 2027 than their cost buys; three do not",
           "kW at the coincident-peak cooling index (1.15), each proposal on its own; break-even is its annual cost at USD 88 a kW-year")
    cats = [F["proposals"][m]["name"] for m in ORDER]
    ch = _bar(s, Inches(0.6), Inches(1.6), Inches(12.1), Inches(5.5), cats,
              [("kW added in 2027", [F["proposals"][m]["kw"] for m in ORDER]),
               ("Break-even kW", [F["proposals"][m]["breakeven"] for m in ORDER])],
              colours=[RGBColor(0x25, 0x7D, 0xE0), RGBColor(0xF4, 0x72, 0x30)])
    ch.plots[0].gap_width = 70
    ch.category_axis.reverse_order = True
    ch.value_axis.tick_labels.number_format = "#,##0"
    ch.value_axis.tick_labels.number_format_is_linked = False
    for i, sl in enumerate(prs.slides, 1):
        tb = sl.shapes.add_textbox(Inches(0.55), Inches(7.02), Inches(12.2), Inches(0.35))
        p_ = tb.text_frame.paragraphs[0]
        p_.text = ("Source: 2026 dispatch trial (feeder SCADA, paging encoder log, switch register, load research homes); "
                   "2027 work plan, section 6.4. Energy Services, November 2026.   %d" % i)
        p_.font.size = Pt(10)
        p_.font.color.rgb = RGBColor(0x59, 0x59, 0x59)
    prs.save(path)


def build(folder, F):
    os.makedirs(folder, exist_ok=True)
    write_csv(os.path.join(folder, FILES["csv"]), F)
    write_xlsx(os.path.join(folder, FILES["xlsx"]), F)
    write_pptx(os.path.join(folder, FILES["pptx"]), F)
    postprocess.normalize_ooxml(os.path.join(folder, FILES["xlsx"]), P.PEOPLE["energy"], P.PEOPLE["energy"],
                                "2026-11-23T15:12:00Z", "2026-11-24T21:38:52Z", title="Load management trial 2026",
                                excel=True, company=P.ORG_SHORT)
    postprocess.normalize_pptx(os.path.join(folder, FILES["pptx"]), P.PEOPLE["energy"], P.PEOPLE["energy"],
                               "2026-11-24T16:05:00Z", "2026-11-25T14:47:00Z", "2027 load management", P.ORG_SHORT)
    stamps = {FILES["csv"]: dt.datetime(2026, 11, 24, 15, 31, 9, tzinfo=P.CST)}
    postprocess.own_mtimes(folder, stamps)
