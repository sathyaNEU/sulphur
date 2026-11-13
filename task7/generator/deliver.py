"""The golden deliverables the prompt asks for: a workbook (vo_program_2027.xlsx) and a short memo
(vo_program_2027_memo.docx), both from figures.json."""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from docx import Document  # noqa: E402
from docx.enum.text import WD_ALIGN_PARAGRAPH  # noqa: E402
from docx.shared import Mm, Pt, RGBColor  # noqa: E402
from openpyxl import Workbook  # noqa: E402
from openpyxl.styles import Alignment, Font, PatternFill  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
WRITERS = os.path.join(os.path.dirname(os.path.dirname(HERE)), ".claude", "skills", "reduce-house-fixes", "scripts", "writers")
sys.path.insert(0, WRITERS)
import postprocess  # noqa: E402

ORG = "Platte Ridge Public Power District"
INK = "1F3A5F"
FILES = {"wb": "vo_program_2027.xlsx", "memo": "vo_program_2027_memo.docx"}
CLS = {"res": "Residential", "com": "Commercial", "rural": "Rural"}


def usd(x):
    return "$" + format(int(round(x, -2)), ",")


def workbook(path, F):
    wb = Workbook()
    ws = wb.active
    ws.title = "Decision"
    hdr = ["Feeder", "Class", "Yearly saving at the customer meters (MWh)", "Rise in the feeder's own line losses (MWh a year)",
           "Yearly saving at the substation (MWh)", "Present value of the saving (USD)", "Installed cost (USD)", "Value over cost",
           "2027 program"]
    ws.append(hdr)
    for i in F["ids"]:
        pv = F["save_mwh"][i] * F["price"] * F["annuity"]
        ws.append([i, CLS[F["kind"][i]], F["cust_mwh"][i], F["loss_mwh"][i], F["save_mwh"][i], round(pv, -2), F["cost"][i],
                   F["value_ratio"][i], "VO in 2027" if i in F["funded"] else "Not in 2027"])
    ws2 = wb.create_sheet("Trial")
    ws2.append(["Trial feeder", "Change in energy per 1% of feeder-head voltage removed (%)"])
    for i in F["trial"]:
        ws2.append([i, F["trial_effect"][i]])
    ws2.append(["Average", F["trial_mean"]])
    ws3 = wb.create_sheet("Feeders")
    ws3.append(["Feeder", "2026 energy at the customer meters (MWh)", "Average reduction the equipment could hold over the year (V, 120 V base)",
                "Yearly change in customer energy per 1% of voltage removed (%)"])
    for i in F["ids"]:
        ws3.append([i, F["energy_mwh"][i], F["room_v"][i], F["cvrf"][i]])
    ws4 = wb.create_sheet("Method")
    for line in F["method"]:
        ws4.append([line])
    for s in (ws, ws2, ws3):
        for c in s[1]:
            c.font = Font(bold=True)
            c.fill = PatternFill("solid", fgColor="DCE3EE")
            c.alignment = Alignment(wrap_text=True, vertical="top")
        s.freeze_panes = "B2"
    for col, w in zip("ABCDEFGHI", (11, 13, 16, 16, 16, 16, 14, 11, 14)):
        ws.column_dimensions[col].width = w
    ws2.column_dimensions["A"].width = 13
    ws2.column_dimensions["B"].width = 34
    for col, w in zip("ABCD", (11, 20, 30, 30)):
        ws3.column_dimensions[col].width = w
    ws4.column_dimensions["A"].width = 118
    for r in ws4.iter_rows():
        r[0].alignment = Alignment(wrap_text=True, vertical="top")
    wb.save(path)
    postprocess.normalize_ooxml(path, "Mary Wilson", "Mary Wilson", "2027-01-11T15:10:00Z", "2027-01-14T21:34:16Z",
                                excel=True, company=ORG)


def chart(F, scratch):
    ids = sorted(F["ids"], key=lambda i: -F["value_ratio"][i])
    vals = [F["value_ratio"][i] for i in ids]
    cols = ["#2F5D8C" if i in F["funded"] else "#B8C2CC" for i in ids]
    fig, ax = plt.subplots(figsize=(6.4, 2.6), dpi=150)
    ax.bar(range(len(ids)), vals, color=cols, width=0.7)
    ax.axhline(1.0, color="#8C2F2F", lw=0.9)
    ax.set_xticks(range(len(ids)))
    ax.set_xticklabels(ids, rotation=90, fontsize=6.5)
    ax.set_ylabel("Present value of the saving\nover installed cost", fontsize=7.5)
    ax.tick_params(axis="y", labelsize=7)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    p = os.path.join(scratch, "vo_value.png")
    fig.savefig(p, metadata={"Software": None})
    plt.close(fig)
    return p


def memo(path, F, png):
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Mm(215.9), Mm(279.4)
    for side in ("left_margin", "right_margin"):
        setattr(sec, side, Mm(22))
    sec.top_margin, sec.bottom_margin = Mm(18), Mm(18)
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10)

    def para(text, bold=False, size=None, color=None, space=4):
        p = doc.add_paragraph()
        r = p.add_run(text)
        r.bold = bold
        if size:
            r.font.size = Pt(size)
        if color:
            r.font.color.rgb = RGBColor.from_string(color)
        p.paragraph_format.space_after = Pt(space)
        return p
    for line in F["memo_head"]:
        para(line, size=8.5, color="555555", space=1)
    para(F["memo_title"], bold=True, size=13.5, color=INK, space=6)
    para(F["memo_call"], bold=True, space=5)
    t = doc.add_table(rows=1, cols=4)
    t.style = "Table Grid"
    for c, h in zip(t.rows[0].cells, ["Feeder", "Yearly saving at the substation", "Installed cost", "Value over cost"]):
        c.text = h
        for r in c.paragraphs[0].runs:
            r.bold = True
            r.font.size = Pt(8.5)
    for i in sorted(F["funded"], key=lambda i: -F["value_ratio"][i]):
        cells = t.add_row().cells
        for c, x in zip(cells, [i, "%s MWh" % format(int(F["save_mwh"][i]), ","), usd(F["cost"][i]), "%.2f" % F["value_ratio"][i]]):
            c.text = x
            for r in c.paragraphs[0].runs:
                r.font.size = Pt(8.5)
    doc.add_picture(png, width=Mm(165))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    for head, body in F["memo_body"]:
        para(head, bold=True, color=INK, space=2)
        para(body)
    doc.save(path)
    postprocess.normalize_docx(path, "Mary Wilson", "Joseph Harmon", "2027-01-12T14:22:00Z", "2027-01-14T22:05:00Z", 9, 214,
                               "task7-vo-memo", title="Voltage optimization: the 2027 program", company=ORG)


def build(folder, F, scratch):
    os.makedirs(folder, exist_ok=True)
    workbook(os.path.join(folder, FILES["wb"]), F)
    memo(os.path.join(folder, FILES["memo"]), F, chart(F, scratch))
