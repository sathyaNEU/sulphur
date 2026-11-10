"""task7 architecture 8: the golden deliverables (the note for the committee's paper and the round's appraisal
workbook), figures.json and effort.json, every figure computed from the cut pack by golden.py and checks.py."""
import json
import math
import os

import numpy as np

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Mm, Pt, RGBColor
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

import checks as CK
import golden as GD
import postprocess

MEAS = GD.MEASURES
LABEL = {"insulation": "Insulation", "heating optimisation": "Heating optimisation", "heating controls": "Heating controls"}
USE = {"office": "Offices", "retail": "Shops", "hotel": "Hotels", "workshop": "Workshops", "care home": "Care homes",
       "restaurant": "Restaurants"}
GREEN, RED, INK = "#2E7D6B", "#B5543C", "#333333"


def rnd(v, u):
    return math.floor(v / u + 0.5) * u


def eur(v):
    return "€" + format(int(rnd(v, 1)), ",")


def head_row(ws, widths):
    for c in ws[1]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="1F4E46")
        c.alignment = Alignment(wrap_text=True, vertical="center")
    for k, wd in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(k)].width = wd
    ws.freeze_panes = "A2"


def pct_fmt(ws, cols, fmt="0.00", start=2):
    for r in ws.iter_rows(min_row=start):
        for cell in r:
            if cell.column in cols and isinstance(cell.value, (int, float)):
                cell.number_format = fmt


def write_xlsx(path, C, F):
    P, A = C["P"], C["A"]
    wb = Workbook()
    ws = wb.active
    ws.title = "measures"
    ws.append(["measure", "saving over its life, pilot buildings (%)", "saving rate on the applications received (%)",
               "applications received", "grant received (EUR)", "lifetime tonnes CO2", "grant per tonne (EUR)",
               "90% range, low (EUR)", "90% range, high (EUR)", "saving rate at which the call flips (%)", "fund"])
    for m in MEAS:
        ws.append([LABEL[m], F["R2_life_saving_pct"][m], F["R5_rate_on_applications_pct"][m], A[m]["n"],
                   F["grant_received_eur"][m], F["lifetime_tonnes_received"][m], F["R6_eur_per_tonne"][m],
                   F["R7_range_eur"][m][0], F["R7_range_eur"][m][1], F["R7_break_even_pct"][m],
                   "yes" if m in C["funded"] else "no"])
    head_row(ws, [22, 16, 18, 13, 14, 13, 13, 12, 12, 16, 7])
    pct_fmt(ws, (2, 3, 7, 8, 9, 10))
    pct_fmt(ws, (4, 5, 6), "#,##0")
    ws2 = wb.create_sheet("savings by season")
    ws2.append(["measure"] + F["season_labels"])
    for m in MEAS:
        ws2.append([LABEL[m]] + F["R1_saving_by_season_pct"][m])
    ws2.append([])
    ws2.append(["Saving against the owners the 2019 draw passed over, % of the gas the works buildings would have used, "
                "normal weather"])
    head_row(ws2, [22] + [10] * 7)
    pct_fmt(ws2, range(2, 9))
    ws3 = wb.create_sheet("controls by empty week")
    ws3.append(["band of the pilot's controls answers", "share of the week empty, gas-weighted (%)", "works buildings",
                "passed over", "saving, seven seasons (%)", "fitted (%)"])
    for (x, v, _), (g, c) in zip(C["R3_pts"], C["R3_n"]):
        lab = "lived in round the clock" if x <= 0 else "closes"
        ws3.append([lab, round(100 * x, 2), g, c, round(100 * v, 2), round(100 * float(GD.dose_at(C["R3_fit"], x)[0]), 2)])
    ws3.append([])
    ws3.append(["controls save nothing until %.1f%% of the week is empty, then %.2f points for each further tenth"
                % (F["R3_threshold_empty_pct"], F["R3_slope_points_per_tenth"])])
    ws3.append(["share of the week empty, pilot's controls works buildings, by 2018/19 gas (%)",
                F["R3_empty_week_pct"]["pilot"]])
    ws3.append(["share of the week empty, this year's controls applications, by reference consumption (%)",
                F["R3_empty_week_pct"]["2026"]])
    head_row(ws3, [34, 18, 14, 12, 16, 12])
    ws4 = wb.create_sheet("insulation by roof")
    ws4.append(["band of the pilot's insulation answers", "roof per square metre of floor, gas-weighted", "works buildings",
                "passed over", "saving of the heating, seven seasons (%)", "fitted (%)"])
    for k, ((x, v, _), (g, c)) in enumerate(zip(C["R4_pts"], C["R4_n"]), 1):
        ws4.append(["band %d" % k, round(math.exp(x), 2), g, c, round(100 * v, 2),
                    round(100 * float(GD.dose_at(C["R4_fit"], x)[0]), 2)])
    ws4.append([])
    ws4.append(["the heating saving is %.4f + %.4f times the natural log of the roof per floor; an application saves it "
                "on its building's heating, the use's hot-water share untouched" % tuple(F["R4_line"])])
    ws4.append(["roof per floor, pilot's insulation works buildings, by 2018/19 gas", F["R4_roof_per_floor"]["pilot"]])
    ws4.append(["roof per floor, this year's insulation applications, by reference consumption",
                F["R4_roof_per_floor"]["2026"]])
    head_row(ws4, [34, 18, 14, 12, 18, 12])
    ws5 = wb.create_sheet("applications")
    ws5.append(["application_no", "building_id", "received", "use", "measure", "share_of_week_empty_pct",
                "roof_per_floor", "grant_eur", "reference_consumption_kwh", "saving rate over its life (%)",
                "lifetime_tonnes", "funded"])
    for a in C["apps"]:
        ws5.append([a["no"], a["bid"], a["date"].strftime("%Y-%m-%d"), USE[a["use"]].lower(), a["measure"],
                    round(100 * a["empty"], 1) if a["measure"] == "heating controls" else None,
                    round(a["roof"], 2) if a["measure"] == "insulation" else None,
                    int(round(a["grant"])), int(round(a["ref_kwh"])), round(100 * a["rate"], 2),
                    round(a["life_t"], 1), "yes" if a["funded"] else "no"])
    n = ws5.max_row
    ws5.append([])
    ws5.append(["all applications", None, None, None, None, None, None, F["R9_grant_eur"], None, None, F["R9_tonnes"], None])
    ws5.cell(row=ws5.max_row, column=1).font = Font(bold=True)
    head_row(ws5, [15, 12, 11, 12, 20, 12, 10, 11, 16, 14, 13, 8])
    pct_fmt(ws5, (6,), "0.0")
    pct_fmt(ws5, (7, 10))
    pct_fmt(ws5, (8, 9), "#,##0")
    pct_fmt(ws5, (11,), "#,##0.0")
    ws5.auto_filter.ref = "A1:L%d" % n
    ws6 = wb.create_sheet("round at close")
    ws6.append(["measure", "applications received by 12 June", "2019 answers in by the same day (%)",
                "applications at close", "late against early grant, 2019", "grant asked at close (EUR)",
                "withdrawn 2019, early (%)", "withdrawn 2019, late (%)", "paid once the works are done (EUR)", "funded"])
    for m in MEAS:
        r = C["R8"][m]
        ws6.append([LABEL[m], r["n"], F["R8_share_by_day_pct"][m], F["R8_applications_at_close"][m],
                    round(r["size"], 3), F["R8_grant_at_close_eur"][m], F["R8_withdrawn_pct"][m][0],
                    F["R8_withdrawn_pct"][m][1], F["R8_grant_paid_eur"][m], "yes" if m in C["funded"] else "no"])
    ws6.append([])
    ws6.append(["funded round", None, None, None, None, F["R8_funded_close_eur"], None, None, F["R8_funded_paid_eur"], None])
    ws6.cell(row=ws6.max_row, column=1).font = Font(bold=True)
    head_row(ws6, [22, 14, 14, 13, 13, 14, 12, 12, 14, 8])
    pct_fmt(ws6, (6, 9), "#,##0")
    pct_fmt(ws6, (3, 7, 8))
    ws7 = wb.create_sheet("2025-26 saving")
    ws7.append(["measure", "works buildings", "saving 2025/26 (%)", "tonnes CO2"])
    for m in MEAS:
        ws7.append([LABEL[m], F["works_buildings"][m], F["R1_saving_by_season_pct"][m][-1],
                    int(round(C["R10_by_measure"][m]))])
    ws7.append(["all three", int(P.works.sum()), None, F["R10_tonnes"]])
    ws7.cell(row=ws7.max_row, column=1).font = Font(bold=True)
    head_row(ws7, [22, 14, 16, 12])
    ws8 = wb.create_sheet("routes")
    ws8.append(["route", "insulation (EUR/t)", "heating optimisation (EUR/t)", "heating controls (EUR/t)", "funds"])
    ws8.append(["this appraisal", F["R6_eur_per_tonne"]["insulation"], F["R6_eur_per_tonne"]["heating optimisation"],
                F["R6_eur_per_tonne"]["heating controls"], ", ".join(C["funded"])])
    for k in ROUTE_ORDER:
        v = F["hurried_eur_per_tonne"][k]
        ws8.append([ROUTE_TEXT[k], v["insulation"], v["heating optimisation"], v["heating controls"],
                    ", ".join(F["routes"][k]) or "none"])
    head_row(ws8, [58, 14, 18, 16, 46])
    pct_fmt(ws8, (2, 3, 4))
    ws9 = wb.create_sheet("notes")
    for line in [
            ("As of", "applications received by 12 June 2026; the 2019 pilot's seasons 2019/20 to 2025/26"),
            ("Saving", "the gas a measure's works save as a share of the gas the buildings that had them would have "
                       "used, normal weather (climate action plan 4.2 and 4.3), against the owners the 2019 draw passed "
                       "over, each building against its own 2018/19 season"),
            ("Over the life", "each measure's seasons carried to its service life (30, 15 and 10 years) at the level "
                              "its saving settles at"),
            ("Empty week", "the hours of each building's 2025 typical week (its market locations summed) whose load is "
                           "under half-way from its lowest hour to its highest, none where the load never falls below "
                           "three quarters of its highest hour; every hotel and care home is lived in round the clock, "
                           "its guests or residents there at night whatever its load does"),
            ("Roof per floor", "the roof faces at the building's address in the state solar cadastre (2023 flight) over "
                               "the heated floor area in the register"),
            ("Pricing", "controls at the saving the pilot's buildings showed at the application's own empty week, "
                        "insulation at its own roof per floor (on the heating, the use's hot-water share untouched), "
                        "heating optimisation at its own use's saving; each faded as its measure's saving fades"),
            ("Lifetime tonnes", "saving rate times reference consumption times 0.201 t per MWh, over the life (4.4)"),
            ("Range", "90%, the pilot's buildings drawn again within use and arm, every step repeated"),
            ("Round at close", "the 2019 answers in by the same day after the notice, their late and early grants and "
                               "withdrawals, measure by measure"),
            ("Precision", "savings and rates to two decimals, grant per tonne to the cent, money to the euro, counts and "
                          "totals whole, an application's lifetime tonnes to a tenth")]:
        ws9.append(list(line))
    ws9.column_dimensions["A"].width = 16
    ws9.column_dimensions["B"].width = 110
    for c in ws9["A"]:
        c.font = Font(bold=True)
    wb.save(path)
    postprocess.normalize_ooxml(path, "Torben Römer", "Torben Römer", "2026-06-19T08:02:00Z", "2026-06-24T16:47:00Z",
                                "The 2026 efficiency grant round", excel=True, company="Stadtwerke Haldenau")


ROUTE_ORDER = ["each use's saving, faded", "the pilot's own mix, faded", "the pilot's seven-season average",
               "controls on its empty week, insulation by use", "insulation on its roof, controls by use",
               "the works buildings' own before and after"]
ROUTE_TEXT = {"each use's saving, faded": "Each application at its own use's saving, faded",
              "the pilot's own mix, faded": "The pilot's saving over each life, at the pilot's own mix",
              "the pilot's seven-season average": "The pilot's seven-season saving, carried flat",
              "controls on its empty week, insulation by use": "Controls on the empty week, insulation by use",
              "insulation on its roof, controls by use": "Insulation on the roof, controls by use",
              "the works buildings' own before and after": "The works buildings' before and after, no comparison"}


def chart(C, F, scratch):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "svg.hashsalt": "task7", "path.simplify": False})
    fig, axes = plt.subplots(1, 3, figsize=(10.2, 3.5), dpi=150, gridspec_kw={"width_ratios": [1.0, 1.0, 1.0]})
    ax = axes[0]
    xs = list(range(len(MEAS)))
    for x, m in zip(xs, MEAS):
        col = GREEN if m in C["funded"] else RED
        v = C["A"][m]["eur_t"]
        lo, hi = C["R7"][m]["lo"], C["R7"][m]["hi"]
        ax.plot([x, x], [lo, hi], color=col, lw=6, alpha=0.35, solid_capstyle="butt")
        ax.plot([x], [v], "o", color=col, ms=7)
        ax.text(x + 0.14, v, "€%.2f" % F["R6_eur_per_tonne"][m], va="center", fontsize=8.5, color=INK)
    ax.axhline(GD.LIMIT, color=INK, lw=1.0, ls="--")
    ax.text(2.55, GD.LIMIT + 6, "limit €120", ha="right", fontsize=8, color=INK)
    ax.set_xticks(xs)
    ax.set_xticklabels([LABEL[m].replace(" ", "\n") for m in MEAS], fontsize=8)
    ax.set_xlim(-0.5, 2.7)
    ax.set_ylabel("Grant per lifetime tonne of CO2, euro")
    ax.set_ylim(0, max(C["R7"][m]["hi"] for m in MEAS) * 1.08)
    ax.set_title("Insulation and controls clear €120", fontsize=9.5, loc="left")
    ax2 = axes[1]
    pts = [p for p in C["R3_pts"] if p[0] > 0]
    ax2.plot([100 * p[0] for p in pts], [100 * p[1] for p in pts], "o", color=GREEN, ms=5, label="pilot bands")
    ex = np.linspace(0.35, 0.80, 50)
    ax2.plot(100 * ex, 100 * GD.dose_at(C["R3_fit"], ex), color=GREEN, lw=1.6, label="fitted")
    for key, ls, lab in (("pilot", ":", "pilot works"), ("2026", "--", "2026 applications")):
        ax2.axvline(F["R3_empty_week_pct"][key], color=INK, lw=0.9, ls=ls)
        ax2.text(F["R3_empty_week_pct"][key] - 0.6, 12.9, lab, fontsize=7, color=INK, ha="right", va="top")
    ax2.set_xlabel("Share of the week the building stands empty, %")
    ax2.set_ylabel("Controls' saving, % of the gas")
    ax2.set_xlim(35, 80)
    ax2.set_ylim(0, 13)
    ax2.set_title("Controls save with the empty week", fontsize=9.5, loc="left")
    ax3 = axes[2]
    xs3 = [math.exp(p[0]) for p in C["R4_pts"]]
    ax3.plot(xs3, [100 * p[1] for p in C["R4_pts"]], "o", color="#3B6EA5", ms=5)
    rx = np.linspace(0.2, 1.4, 60)
    ax3.plot(rx, 100 * GD.dose_at(C["R4_fit"], np.log(rx)), color="#3B6EA5", lw=1.6)
    for key, ls, lab in (("pilot", ":", "pilot works"), ("2026", "--", "2026 applications")):
        ax3.axvline(F["R4_roof_per_floor"][key], color=INK, lw=0.9, ls=ls)
        ax3.text(F["R4_roof_per_floor"][key] - 0.015, 34.6 if key == "2026" else 32.4, lab, fontsize=7, color=INK,
                 ha="right", va="top")
    ax3.set_xlabel("Roof per square metre of floor, m²")
    ax3.set_ylabel("Insulation's saving, % of the heating")
    ax3.set_xlim(0.15, 1.45)
    ax3.set_ylim(0, 35)
    ax3.set_title("Insulation saves with the roof", fontsize=9.5, loc="left")
    for a_ in axes:
        for s in ("top", "right"):
            a_.spines[s].set_visible(False)
        a_.grid(axis="y", color="#E5E5E5", lw=0.6)
    fig.tight_layout()
    out = os.path.join(scratch, "grant_round_2026.png")
    fig.savefig(out, format="png", metadata={"Software": None})
    plt.close(fig)
    return out


def _cell(cell, text, bold=False, size=9, align=None, shade=None):
    cell.text = ""
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    if align:
        p.alignment = align
    r = p.add_run(text)
    r.bold = bold
    r.font.size = Pt(size)
    if shade:
        tcPr = cell._tc.get_or_add_tcPr()
        sh = OxmlElement("w:shd")
        sh.set(qn("w:val"), "clear")
        sh.set(qn("w:color"), "auto")
        sh.set(qn("w:fill"), shade)
        tcPr.append(sh)


def table(doc, rows, widths, header=True, left=(0,)):
    t = doc.add_table(rows=len(rows), cols=len(rows[0]))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, row in enumerate(rows):
        for j, v in enumerate(row):
            _cell(t.cell(i, j), str(v), bold=(header and i == 0), size=8.5,
                  align=WD_ALIGN_PARAGRAPH.LEFT if j in left else WD_ALIGN_PARAGRAPH.RIGHT,
                  shade="E8EFEC" if (header and i == 0) else None)
    for j, wd in enumerate(widths):
        for i in range(len(rows)):
            t.cell(i, j).width = Mm(wd)
    return t


def para(doc, text, bold=False, size=10, after=5, italic=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(after)
    r = p.add_run(text)
    r.bold = bold
    r.italic = italic
    r.font.size = Pt(size)
    return p


def write_note(path, C, F, png):
    A = C["A"]
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Mm(210), Mm(297)
    sec.left_margin = sec.right_margin = Mm(20)
    sec.top_margin, sec.bottom_margin = Mm(16), Mm(16)
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10)
    para(doc, "Stadtwerke Haldenau, Energy Services", size=8.5, after=2)
    para(doc, "Fund insulation and heating controls in 2026, not heating optimisation", bold=True, size=14, after=3)
    para(doc, "To the Committee for Climate and Environment, for its meeting of 9 July 2026. From Torben Römer, head of "
              "Energy Services. 24 June 2026. Subject: the 2026 efficiency grant round (climate action plan, section 4).",
         size=8.5, after=8)
    footer = doc.sections[0].footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    fr = footer.add_run("Stadtwerke Haldenau | Energy Services | Grant round 2026 | page ")
    fr.font.size = Pt(7.5)
    for kind, txt in (("begin", None), (None, "PAGE"), ("end", None)):
        run = footer.add_run()
        run.font.size = Pt(7.5)
        if kind:
            el = OxmlElement("w:fldChar")
            el.set(qn("w:fldCharType"), kind)
            run._r.append(el)
        else:
            el = OxmlElement("w:instrText")
            el.set(qn("xml:space"), "preserve")
            el.text = txt
            run._r.append(el)
    ins, ho, ct = "insulation", "heating optimisation", "heating controls"
    eu, byuse = F["R6_eur_per_tonne"], F["R6_by_use_eur_per_tonne"]
    para(doc, "Fund insulation and heating controls in the 2026 round; do not fund heating optimisation. On the "
              "applications received by 12 June, insulation comes to €%.2f and heating controls to €%.2f of grant per "
              "lifetime tonne of CO2, under the €%d limit, and heating optimisation to €%.2f."
         % (eu[ins], eu[ct], F["limit_eur"], eu[ho]), bold=True, size=10.5, after=6)
    para(doc, "This year's owners chose their measures knowing their buildings, and the pilot shows each measure saving "
              "with what suits it. Heating controls save nothing until about %.0f%% of the week is empty and %.2f "
              "points more for each further tenth (%.2f%% of the gas at seven tenths); this year's controls applications "
              "stand empty %.2f%% of the week, the pilot's controls buildings %.2f%%. Roof insulation saves %.2f%% of "
              "the heating where the roof is as large as the floor and %.2f%% at a quarter; this year's insulation "
              "applications have %.2f square metres of roof per square metre of floor, the pilot's %.2f (applications "
              "weighted by reference consumption, the pilot's buildings by their 2018/19 gas). Priced at its "
              "own use's saving instead, insulation would come to €%.2f and controls to €%.2f, and the round would fund "
              "nothing."
         % (F["R3_threshold_empty_pct"], F["R3_slope_points_per_tenth"], F["R3_controls_at_empty_pct"]["70"],
            F["R3_empty_week_pct"]["2026"], F["R3_empty_week_pct"]["pilot"], F["R4_heating_at_roof_pct"]["1"],
            F["R4_heating_at_roof_pct"]["0.25"], F["R4_roof_per_floor"]["2026"], F["R4_roof_per_floor"]["pilot"],
            byuse[ins], byuse[ct]), after=6)
    para(doc, "Heating optimisation saved %.2f%% of the gas its buildings would have used in its first winter, %.2f%% by "
              "the fourth and %.2f%% in 2025/26, settling towards about %.2f%%: carried over its fifteen-year life it "
              "saves %.2f%%, and it fails the limit by a wide margin."
         % (F["R2_ho_first_pct"], F["R2_ho_fourth_pct"], F["R1_saving_by_season_pct"][ho][-1], F["R2_ho_floor_pct"],
            F["R2_life_saving_pct"][ho]), after=6)
    rows = [["Measure", "Saving over its life, pilot", "Saving rate on this year's applications", "Grant per tonne",
             "90% range", "Flips at a saving of", "Fund"]]
    for m in MEAS:
        rows.append([LABEL[m], "%.2f%%" % F["R2_life_saving_pct"][m], "%.2f%%" % F["R5_rate_on_applications_pct"][m],
                     "€%.2f" % eu[m], "€%.2f to €%.2f" % tuple(F["R7_range_eur"][m]),
                     "%.2f%%" % F["R7_break_even_pct"][m], "yes" if m in C["funded"] else "no"])
    table(doc, rows, [34, 25, 30, 20, 26, 22, 12], left=(0, 6))
    para(doc, "Applications received by 12 June 2026, a revised application in place of the one it replaces. Reference "
              "consumption is the notice's normalised use per square metre times the register's heated floor area "
              "(plan 4.5); lifetime tonnes at 0.201 t of CO2 per MWh over 30, 15 and 10 years (plan 4.4).", size=7.5,
         italic=True, after=4)
    doc.add_picture(png, width=Mm(170))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    para(doc, "Savings are against the owners the 2019 draw passed over, measure by measure, each building against its "
              "own 2018/19 season, in normal weather. A building's empty week is read off the meter operator's 2025 "
              "typical week of its electricity (the hours under half-way from its lowest to its highest), every hotel "
              "and care home taken as lived in round the clock; its roof is the solar cadastre's roof faces at its "
              "address over the register's floor area.",
         size=8.5, italic=True, after=8)
    para(doc, "What the round will pay", bold=True, size=11, after=3)
    para(doc, "%d insulation and %d heating controls applications were in by 12 June. In 2019 only %.2f%% of the "
              "insulation answers and %.2f%% of the controls answers had come in by the same day after the notice, the "
              "late insulation answers ran %.2f%% larger, and %.2f%% of the late insulation places were withdrawn "
              "against %.2f%% of the early ones. On that record the funded round's applications will ask for %s once "
              "the offer closes and it will pay %s once the works are done; heating optimisation's applications would "
              "ask for and be paid the amounts below only if it were funded."
         % (A[ins]["n"], A[ct]["n"], F["R8_share_by_day_pct"][ins], F["R8_share_by_day_pct"][ct],
            F["R8_late_size_premium_pct"][ins], F["R8_withdrawn_pct"][ins][1],
            F["R8_withdrawn_pct"][ins][0], eur(F["R8_funded_close_eur"]), eur(F["R8_funded_paid_eur"])), after=4)
    rows = [["Measure", "Applications at close", "Grant asked", "Paid once the works are done"]]
    for m in MEAS:
        rows.append([LABEL[m] + ("" if m in C["funded"] else " (not funded)"), "about %d" % F["R8_applications_at_close"][m],
                     eur(F["R8_grant_at_close_eur"][m]), eur(F["R8_grant_paid_eur"][m])])
    table(doc, rows, [52, 36, 38, 40])
    para(doc, "The 2019 answers' dates, quotes and withdrawals from the pilot's response file; works to be done by 30 "
              "September 2026 and paid on completion (terms of the 2026 offer, 4).", size=7.5, italic=True, after=6)
    para(doc, "For the annual report", bold=True, size=11, after=3)
    para(doc, "The pilot's works saved %s tonnes of CO2 in the season to April 2026: the gas the works buildings "
              "would have used that season without the works, less what they used, in normal weather."
         % format(F["R10_tonnes"], ","), after=8)
    para(doc, "How the quicker readings land", bold=True, size=11, after=3)
    rows = [["Reading of the pilot", "Insulation", "Heating optimisation", "Heating controls", "Funds"]]
    rows.append(["This appraisal", "€%.2f" % eu[ins], "€%.2f" % eu[ho], "€%.2f" % eu[ct],
                 ", ".join(LABEL[m].lower() for m in C["funded"])])
    for k in ROUTE_ORDER:
        v = F["hurried_eur_per_tonne"][k]
        rows.append([ROUTE_TEXT[k], "€%.2f" % v[ins], "€%.2f" % v[ho], "€%.2f" % v[ct],
                     ", ".join(LABEL[m].lower() for m in F["routes"][k]) or "none"])
    table(doc, rows, [62, 22, 30, 26, 48], left=(0, 4))
    para(doc, "Each reading run on the same applications and the same pilot record; only the way the pilot is read "
              "changes.", size=7.5, italic=True, after=6)
    para(doc, "Torben Römer, head of Energy Services", size=9, after=0)
    cp = doc.core_properties
    cp.title, cp.author, cp.last_modified_by = "The 2026 efficiency grant round", "Torben Römer", "Torben Römer"
    doc.save(path)
    postprocess.normalize_docx(path, "Torben Römer", "Torben Römer", "2026-06-22T07:31:00Z", "2026-06-24T15:58:00Z", 9,
                               236, "task7-grant-note", "The 2026 efficiency grant round", "Stadtwerke Haldenau")


def write_all(C, golden_dir, gen_dir, scratch):
    C["R10_by_measure"] = {}
    P = C["P"]
    for m in MEAS:
        rates = {mm: (C["R1"][mm][-1] if mm == m else 0.0) for mm in MEAS}
        C["R10_by_measure"][m] = GD.season_saving_2026(P, "given rates", rates)
    F = CK.figures(C)
    E = CK.effort(C, F)
    F = CK.tables_for_figures(F, E)
    os.makedirs(golden_dir, exist_ok=True)
    write_xlsx(os.path.join(golden_dir, "grant_round_2026_appraisal.xlsx"), C, F)
    png = chart(C, F, scratch)
    write_note(os.path.join(golden_dir, "grant_round_2026_note.docx"), C, F, png)
    with open(os.path.join(gen_dir, "figures.json"), "w", encoding="utf-8") as fh:
        json.dump(F, fh, indent=1, ensure_ascii=False)
    with open(os.path.join(gen_dir, "effort.json"), "w", encoding="utf-8") as fh:
        json.dump(E, fh, indent=1, ensure_ascii=False)
    return F
