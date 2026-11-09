"""task7 architecture 7: the golden deliverables (the note for the committee's paper and the round's appraisal
workbook), figures.json and effort.json, every figure computed from the cut pack by golden.py and checks.py."""
import json
import math
import os

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


def mil(v):
    return "€%.1f million" % v


def head_row(ws, widths):
    for c in ws[1]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="1F4E46")
        c.alignment = Alignment(wrap_text=True, vertical="center")
    for k, wd in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(k)].width = wd
    ws.freeze_panes = "A2"


def write_xlsx(path, C, F):
    P, A = C["P"], C["A"]
    wb = Workbook()
    ws = wb.active
    ws.title = "measures"
    ws.append(["measure", "saving over its life, pilot buildings (%)", "saving rate on the applications received (%)",
               "applications received", "grant received (EUR)", "lifetime tonnes CO2", "grant per tonne (EUR)",
               "90% range, low (EUR)", "90% range, high (EUR)", "saving rate at which the call flips (%)", "fund"])
    for m in MEAS:
        ws.append([LABEL[m], F["R2_life_saving_pct"][m], F["R4_rate_on_applications_pct"][m], A[m]["n"],
                   F["grant_received_eur"][m], F["lifetime_tonnes_received"][m], F["R5_eur_per_tonne"][m],
                   F["R6_range_eur"][m][0], F["R6_range_eur"][m][1], F["R6_break_even_pct"][m],
                   "yes" if m in C["funded"] else "no"])
    head_row(ws, [22, 16, 18, 13, 14, 13, 13, 12, 12, 16, 7])
    for r in ws.iter_rows(min_row=2, min_col=5, max_col=6):
        for cell in r:
            cell.number_format = "#,##0"
    ws2 = wb.create_sheet("savings by season")
    ws2.append(["measure"] + F["season_labels"])
    for m in MEAS:
        ws2.append([LABEL[m]] + F["R1_saving_by_season_pct"][m])
    ws2.append([])
    ws2.append(["Saving against the owners the 2019 draw passed over, % of the gas the works buildings would have used, "
                "normal weather"])
    head_row(ws2, [22] + [10] * 7)
    ws3 = wb.create_sheet("savings by use")
    ws3.append(["measure", "use", "works buildings", "passed over", "saving, seven seasons (%)"])
    for m in MEAS:
        for t in GD.TYPES:
            if t in F["R3_by_type_pct"][m]:
                g, c = C["R3_n"][m][t]
                ws3.append([LABEL[m], USE[t], g, c, F["R3_by_type_pct"][m][t]])
    head_row(ws3, [22, 14, 14, 12, 16])
    ws4 = wb.create_sheet("funded applications")
    ws4.append(["application_no", "building_id", "received", "use", "measure", "grant_eur", "reference_consumption_kwh",
                "saving rate over its life (%)", "lifetime_tonnes"])
    for a in C["apps"]:
        if a["funded"]:
            ws4.append([a["no"], a["bid"], a["date"].strftime("%Y-%m-%d"), USE[a["use"]].lower(), a["measure"],
                        int(round(a["grant"])), int(round(a["ref_kwh"])), round(100 * a["rate"], 1),
                        int(rnd(a["life_t"], 10))])
    head_row(ws4, [15, 12, 11, 12, 20, 11, 16, 14, 13])
    for r in ws4.iter_rows(min_row=2, min_col=6, max_col=7):
        for cell in r:
            cell.number_format = "#,##0"
    ws5 = wb.create_sheet("round at close")
    ws5.append(["measure", "applications received by 12 June", "2019 answers in by the same day (%)",
                "applications at close", "late against early grant, 2019", "grant asked at close (EUR)",
                "withdrawn 2019, early (%)", "withdrawn 2019, late (%)", "paid once the works are done (EUR)", "funded"])
    for m in MEAS:
        r = C["R7"][m]
        ws5.append([LABEL[m], r["n"], F["R7_share_by_day_pct"][m], F["R7_applications_at_close"][m],
                    F["R7_late_size_ratio"][m], F["R7_grant_at_close_eur"][m], F["R7_withdrawn_pct"][m][0],
                    F["R7_withdrawn_pct"][m][1], F["R7_grant_paid_eur"][m], "yes" if m in C["funded"] else "no"])
    ws5.append([])
    ws5.append(["funded round", None, None, None, None, F["R7_funded_close_million"] * 1000000, None, None,
                F["R7_funded_paid_million"] * 1000000, None])
    ws5.cell(row=ws5.max_row, column=1).font = Font(bold=True)
    head_row(ws5, [22, 14, 14, 13, 13, 14, 12, 12, 14, 8])
    for r in ws5.iter_rows(min_row=2, min_col=6, max_col=9):
        for cell in r:
            if cell.column in (6, 9):
                cell.number_format = "#,##0"
    ws6 = wb.create_sheet("2025-26 saving")
    ws6.append(["measure", "works buildings", "saving 2025/26 (%)", "tonnes CO2"])
    for m in MEAS:
        ws6.append([LABEL[m], F["works_buildings"][m], F["R1_saving_by_season_pct"][m][-1],
                    int(rnd(C["R8_by_measure"][m], 10))])
    ws6.append(["all three", int(P.works.sum()), None, F["R8_tonnes"]])
    ws6.cell(row=ws6.max_row, column=1).font = Font(bold=True)
    head_row(ws6, [22, 14, 16, 12])
    ws7 = wb.create_sheet("routes")
    ws7.append(["route", "insulation (EUR/t)", "heating optimisation (EUR/t)", "heating controls (EUR/t)", "funds"])
    ws7.append(["this appraisal", F["R5_eur_per_tonne"]["insulation"], F["R5_eur_per_tonne"]["heating optimisation"],
                F["R5_eur_per_tonne"]["heating controls"], ", ".join(C["funded"])])
    for k in ROUTE_ORDER:
        v = F["hurried_eur_per_tonne"][k]
        ws7.append([k, v["insulation"], v["heating optimisation"], v["heating controls"], ", ".join(F["routes"][k])])
    head_row(ws7, [46, 14, 18, 16, 46])
    ws8 = wb.create_sheet("notes")
    for line in [
            ("As of", "applications received by 12 June 2026; the 2019 pilot's seasons 2019/20 to 2025/26"),
            ("Saving", "the gas a measure's works save as a share of the gas the buildings that had them would have "
                       "used, normal weather (climate action plan 4.2 and 4.3), against the owners the 2019 draw passed "
                       "over, each building against its own 2018/19 season"),
            ("Over the life", "each measure's seasons carried to its service life (30, 15 and 10 years) at the level "
                              "its saving settles at"),
            ("By use", "the use on each building's 2019 notice; an application is priced at its own use's saving"),
            ("Lifetime tonnes", "saving rate times reference consumption times 0.201 t per MWh, over the life (4.4)"),
            ("Range", "90%, the pilot's buildings drawn again within use and arm, every step repeated"),
            ("Round at close", "the 2019 answers in by the same day after the notice, their late and early grants and "
                               "withdrawals, measure by measure"),
            ("Rounding", "savings and rates to one decimal, grant per tonne to the euro, counts to 10, a measure's "
                         "grants to EUR 10,000, round totals to EUR 0.1 million, tonnes to 10, the 2025/26 saving to 100")]:
        ws8.append(list(line))
    ws8.column_dimensions["A"].width = 16
    ws8.column_dimensions["B"].width = 110
    for c in ws8["A"]:
        c.font = Font(bold=True)
    wb.save(path)
    postprocess.normalize_ooxml(path, "Torben Römer", "Torben Römer", "2026-06-19T08:02:00Z", "2026-06-24T16:47:00Z",
                                "The 2026 efficiency grant round", excel=True, company="Stadtwerke Haldenau")


ROUTE_ORDER = ["the pilot's seven-season average", "the pilot's own mix, faded", "each type's seven-season average",
               "the works buildings' own before and after"]
ROUTE_TEXT = {"the pilot's seven-season average": "The pilot's seven-season saving, carried flat",
              "the pilot's own mix, faded": "The pilot's saving over each life, at the pilot's own mix",
              "each type's seven-season average": "Each use's seven-season saving, carried flat",
              "the works buildings' own before and after": "The works buildings' before and after, no comparison"}


def chart(C, F, scratch):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "svg.hashsalt": "task7", "path.simplify": False})
    fig, axes = plt.subplots(1, 2, figsize=(9.4, 3.7), dpi=150, gridspec_kw={"width_ratios": [1.05, 1]})
    ax = axes[0]
    xs = list(range(len(MEAS)))
    for x, m in zip(xs, MEAS):
        col = GREEN if m in C["funded"] else RED
        v = C["A"][m]["eur_t"]
        lo, hi = C["R6"][m]["lo"], C["R6"][m]["hi"]
        ax.plot([x, x], [lo, hi], color=col, lw=6, alpha=0.35, solid_capstyle="butt")
        ax.plot([x], [v], "o", color=col, ms=8)
        ax.text(x + 0.12, v, "€%d" % F["R5_eur_per_tonne"][m], va="center", fontsize=10, color=INK)
    ax.axhline(GD.LIMIT, color=INK, lw=1.1, ls="--")
    ax.text(2.45, GD.LIMIT + 5, "limit €120", ha="right", fontsize=9, color=INK)
    ax.set_xticks(xs)
    ax.set_xticklabels([LABEL[m].replace(" ", "\n") for m in MEAS])
    ax.set_xlim(-0.5, 2.6)
    ax.set_ylabel("Grant per lifetime tonne of CO2, euro")
    ax.set_ylim(0, max(C["R6"][m]["hi"] for m in MEAS) * 1.08)
    ax.set_title("Insulation and controls clear the €120 limit", fontsize=10, loc="left")
    ax2 = axes[1]
    seasons = F["season_labels"]
    for m, col in zip(MEAS, ("#3B6EA5", RED, GREEN)):
        ax2.plot(range(7), F["R1_saving_by_season_pct"][m], marker="o", color=col, lw=1.8, label=LABEL[m])
    ax2.set_xticks(range(7))
    ax2.set_xticklabels([s[2:] for s in seasons], fontsize=8)
    ax2.set_ylabel("Saving, % of the gas without the works")
    ax2.set_ylim(0, max(max(v) for v in F["R1_saving_by_season_pct"].values()) * 1.15)
    ax2.legend(frameon=False, fontsize=8, loc="center right")
    ax2.set_title("Heating optimisation's saving falls back", fontsize=10, loc="left")
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
    para(doc, "Fund insulation and heating controls in the 2026 round; do not fund heating optimisation. On the "
              "applications received by 12 June, insulation comes to €%d and heating controls to €%d of grant per "
              "lifetime tonne of CO2, under the €%d limit, and heating optimisation to €%d."
         % (F["R5_eur_per_tonne"][ins], F["R5_eur_per_tonne"][ct], F["limit_eur"], F["R5_eur_per_tonne"][ho]),
         bold=True, size=10.5, after=6)
    para(doc, "Heating optimisation saved %.1f%% of the gas its buildings would have used in its first winter, but by "
              "the fourth it was saving %.1f%% and it has stayed near there since: carried over its fifteen-year life it "
              "saves %.1f%%. Heating controls save about %.0f%% in offices and around nothing in hotels and care homes "
              "heated round the clock; %d%% of the pilot's controls buildings were hotels or care homes against %d%% "
              "of this year's controls applicants, so on this year's applications controls save %.1f%% over their life, "
              "not the pilot's %.1f%%."
         % (F["R1_saving_by_season_pct"][ho][0], F["R1_saving_by_season_pct"][ho][3], F["R2_life_saving_pct"][ho],
            F["R3_by_type_pct"][ct]["office"], F["controls_round_clock_share_pct"]["2019"],
            F["controls_round_clock_share_pct"]["2026"], F["R4_rate_on_applications_pct"][ct],
            F["R4_pooled_life_pct"][ct]), after=6)
    rows = [["Measure", "Saving over its life, pilot", "Saving rate on this year's applications", "Grant per tonne",
             "90% range", "Flips at a saving of", "Fund"]]
    for m in MEAS:
        rows.append([LABEL[m], "%.1f%%" % F["R2_life_saving_pct"][m], "%.1f%%" % F["R4_rate_on_applications_pct"][m],
                     "€%d" % F["R5_eur_per_tonne"][m], "€%d to €%d" % tuple(F["R6_range_eur"][m]),
                     "%.1f%%" % F["R6_break_even_pct"][m], "yes" if m in C["funded"] else "no"])
    table(doc, rows, [34, 25, 30, 20, 26, 22, 12], left=(0, 6))
    para(doc, "Applications received by 12 June 2026, a revised application in place of the one it replaces. Reference "
              "consumption is the notice's normalised use per square metre times the register's heated floor area "
              "(plan 4.5); lifetime tonnes at 0.201 t of CO2 per MWh over 30, 15 and 10 years (plan 4.4).", size=7.5,
         italic=True, after=4)
    doc.add_picture(png, width=Mm(168))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    para(doc, "Savings are against the owners the 2019 draw passed over, measure by measure, each building against its "
              "own 2018/19 season, in normal weather. Each application is priced at the saving its own use showed in "
              "the pilot, faded as its measure's saving fades.", size=8.5, italic=True, after=8)
    para(doc, "What the round will pay", bold=True, size=11, after=3)
    para(doc, "%d insulation and %d heating controls applications were in by 12 June. In 2019 only %d%% of the "
              "insulation answers and %d%% of the controls answers had come in by the same day after the notice, the "
              "late insulation answers ran %d%% larger, and %.1f%% of the late insulation places were withdrawn against "
              "%.1f%% of the early ones. On that record the funded round will grant about %s once the offer closes and "
              "pay about %s once the works are done; heating optimisation's applications would ask for and be paid the "
              "amounts below only if it were funded."
         % (A[ins]["n"], A[ct]["n"], F["R7_share_by_day_pct"][ins], F["R7_share_by_day_pct"][ct],
            int(round(100 * (F["R7_late_size_ratio"][ins] - 1))), F["R7_withdrawn_pct"][ins][1],
            F["R7_withdrawn_pct"][ins][0], mil(F["R7_funded_close_million"]), mil(F["R7_funded_paid_million"])), after=4)
    rows = [["Measure", "Applications at close", "Grant asked", "Paid once the works are done"]]
    for m in MEAS:
        rows.append([LABEL[m] + ("" if m in C["funded"] else " (not funded)"), "about %d" % F["R7_applications_at_close"][m],
                     eur(F["R7_grant_at_close_eur"][m]), eur(F["R7_grant_paid_eur"][m])])
    table(doc, rows, [52, 36, 38, 40])
    para(doc, "The 2019 answers' dates, quotes and withdrawals from the pilot's response file; works to be done by 30 "
              "September 2026 and paid on completion (terms of the 2026 offer, 4).", size=7.5, italic=True, after=6)
    para(doc, "For the annual report", bold=True, size=11, after=3)
    para(doc, "The pilot's works saved about %s tonnes of CO2 in the season to April 2026: the gas the works buildings "
              "would have used that season without the works, less what they used, in normal weather."
         % format(F["R8_tonnes"], ","), after=8)
    para(doc, "How the quicker readings land", bold=True, size=11, after=3)
    rows = [["Reading of the pilot", "Insulation", "Heating optimisation", "Heating controls", "Funds"]]
    rows.append(["This appraisal", "€%d" % F["R5_eur_per_tonne"][ins], "€%d" % F["R5_eur_per_tonne"][ho],
                 "€%d" % F["R5_eur_per_tonne"][ct], ", ".join(LABEL[m].lower() for m in C["funded"])])
    for k in ROUTE_ORDER:
        v = F["hurried_eur_per_tonne"][k]
        rows.append([ROUTE_TEXT[k], "€%d" % v[ins], "€%d" % v[ho], "€%d" % v[ct],
                     ", ".join(LABEL[m].lower() for m in F["routes"][k]) or "none"])
    table(doc, rows, [62, 22, 30, 26, 48], left=(0, 4))
    para(doc, "Each reading run on the same applications and the same pilot record; only the way the pilot is read "
              "changes.", size=7.5, italic=True, after=6)
    para(doc, "Torben Römer, head of Energy Services", size=9, after=0)
    cp = doc.core_properties
    cp.title, cp.author, cp.last_modified_by = "The 2026 efficiency grant round", "Torben Römer", "Torben Römer"
    doc.save(path)
    postprocess.normalize_docx(path, "Torben Römer", "Torben Römer", "2026-06-22T07:31:00Z", "2026-06-24T15:58:00Z", 9,
                               212, "task7-grant-note", "The 2026 efficiency grant round", "Stadtwerke Haldenau")


def write_all(C, golden_dir, gen_dir, scratch):
    C["R8_by_measure"] = {}
    P = C["P"]
    for m in MEAS:
        rates = {mm: (C["R1"][mm][-1] if mm == m else 0.0) for mm in MEAS}
        C["R8_by_measure"][m] = GD.season_saving_2026(P, "given rates", rates)
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
