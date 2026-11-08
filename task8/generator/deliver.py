"""task8 architecture 18: the golden deliverables, written from core.compute on the shipped seed.

    pass_mark_2027.docx    the assessment manager's recommendation to the Awards Committee
    l1_2027_items.xlsx     one row per 2027 item, the regional figures and the working
"""
import os

import numpy as np
import openpyxl
from docx import Document
from docx.shared import Cm, Pt
from openpyxl.styles import Alignment, Font

import golden as G
import params as P
import postprocess as PP
import world as W

REG = {r[0]: r for r in P.REGIONS}


def _par(doc, text, bold=False, size=10, after=6, italic=False):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.bold, r.italic = bold, italic
    r.font.size = Pt(size)
    p.paragraph_format.space_after = Pt(after)
    return p


def _tab(doc, rows, widths_cm, size=8.5):
    t = doc.add_table(rows=len(rows), cols=len(rows[0]))
    t.style = "Table Grid"
    for i, row in enumerate(rows):
        for j, v in enumerate(row):
            c = t.cell(i, j)
            c.width = Cm(widths_cm[j])
            c.text = ""
            run = c.paragraphs[0].add_run(str(v))
            run.font.size = Pt(size)
            run.bold = i == 0
    doc.add_paragraph().paragraph_format.space_after = Pt(2)


def memo(w, r, f, path):
    g, d = r["gold"], r["default"]
    items = G.item_rows(w, r)
    below = [x for x in items if x["chance"] < P.BAND[0]]
    above = [x for x in items if x["chance"] > P.BAND[1]]
    doc = Document()
    sec = doc.sections[0]
    sec.left_margin = sec.right_margin = Cm(2.3)
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10)
    _par(doc, "Prairie Adult Credentials Board", bold=True, size=9, after=0)
    _par(doc, "To: Awards Committee    From: Yvette Clark, Assessment Manager    For: meeting of 3 December 2026",
         size=9, after=10)
    _par(doc, "2027 Level 1 Numeracy pass mark", bold=True, size=13, after=8)
    _par(doc, "Recommendation", bold=True, size=11, after=3)
    _par(doc, "Set the 2027 Level 1 Numeracy pass mark at %d of 40. A candidate who just meets the Level 1 standard "
              "(26 of 40 on the 2022 paper) can be expected to score %.2f on the 2027 paper. Read straight off the "
              "bank, the paper would give %.2f and a pass mark of %d, %s above what a candidate at the "
              "standard is likely to score." % (g["pass_mark"], g["expected"], d["expected"], d["pass_mark"],
                                                {1: "one mark", 2: "two marks", 3: "three marks", 4: "four marks"}[
                                                    d["pass_mark"] - g["pass_mark"]]))
    _par(doc, "Why the bank's values do not hold for this paper", bold=True, size=11, after=3)
    _par(doc, "Twenty-eight of the 2027 items are Level 1 items whose bank values come from Level 1 sittings. The "
              "twelve patterns and relationships items come from the Level 2 pool, and their bank values come from "
              "Level 2 candidates. Level 1 candidates do not find a Level 2 item as hard as Level 2 candidates do in "
              "every case: across the %d Level 2 items set on the 2023 to 2026 Level 1 papers, Level 1 candidates "
              "found the items in everyday contexts easier by about %.1f logits and lost about %.1f logits for every "
              "100 words of stem. On the long everyday items the two cancel, which is why those items looked "
              "unchanged when we checked them each year; the short everyday items showed the advantage on its own "
              "and the short mathematical items showed neither." % (f["n_bridging"], f["everyday_advantage"],
                                                                 f["reading_cost_per_100_words"]))
    prw = w["it"]["words"][w["it"]["sets"]["pr"]]
    _par(doc, "The 2027 patterns items are long and mathematical (%d to %d words), so they carry the reading cost "
              "with no everyday advantage to offset it. At the standard the twelve are worth %.2f marks together, "
              "against %.2f on the bank's values." % (int(prw.min()), int(prw.max()), f["pr_expected_golden"],
                                                     f["pr_expected_bank"]))
    _par(doc, "Items and the targeting band", bold=True, size=11, after=3)
    txt = ("%d of the 40 items fall below the band in section 5.1 of the specification for a candidate at the "
           "standard, all of them patterns and relationships items (%s)." % (len(below), ", ".join(x["pos"] for x in below)))
    if above:
        txt += (" %d sit above it (%s)." % (len(above), ", ".join(x["pos"] for x in above)))
    txt += " They stay on the 2027 paper; I will report them to the Item Review Group. The full table is in the workbook."
    _par(doc, txt)
    _par(doc, "Regions", bold=True, size=11, after=3)
    _par(doc, "The learners who sat the 2026 Level 1 paper at each region's centres would be expected to score, on "
              "average, the following marks on the 2027 paper. The figures allow for each region's own pattern on "
              "everyday items in the 2026 sittings, which the 2027 paper, with fewer everyday items, rewards less.")
    rows = [["Region", "2026 Level 1 candidates", "Mean expected mark on the 2027 paper"]]
    for rc, (m, n) in r["reg_golden"].items():
        rows.append([REG[rc][1], n, "%d" % int(round(m))])
    _tab(doc, rows, [6.0, 4.0, 5.5])
    _par(doc, "Notes", bold=True, size=11, after=3)
    _par(doc, "The Level 1 figures come from the Level 1 sittings 2022 to 2026 and the Level 2 figures from the "
              "Level 2 sittings 2022 to 2026, each calibrated on its own and linked through the Level 2 items both "
              "sets of candidates sat. Andrew Adams has checked the working. The workbook carries the item table, "
              "the regional figures and the comparison of the two levels on the shared items.", size=9.5)
    doc.core_properties.author = "Yvette Clark"
    doc.save(path)
    PP.normalize_ooxml(path, "Yvette Clark", "Yvette Clark", "2026-11-24T15:10:00Z", "2026-11-27T21:42:00Z",
                       title="2027 Level 1 Numeracy pass mark")


def workbook(w, r, f, path):
    g, d = r["gold"], r["default"]
    it = w["it"]
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "2027 items"
    hdr = ["Position", "Item", "Pool", "Strand", "Context", "Stem words", "Difficulty for a Level 1 candidate (logits)",
           "Chance at the standard", "Inside the band (0.20 to 0.90)"]
    ws.append(hdr)
    for x in G.item_rows(w, r):
        ws.append([x["pos"], x["item"], x["pool"], x["strand"], x["context"], x["words"], round(x["b"], 3),
                   round(x["chance"], 2), "yes" if x["inside"] else "no"])
    for c, wd in zip("ABCDEFGHI", (9, 10, 9, 26, 13, 11, 22, 14, 16)):
        ws.column_dimensions[c].width = wd
    for cell in ws[1]:
        cell.font = Font(bold=True)
        cell.alignment = Alignment(wrap_text=True, vertical="top")
    ws2 = wb.create_sheet("Regions")
    ws2.append(["Region", "Province", "2026 Level 1 candidates", "Mean expected mark on the 2027 paper"])
    for rc, (m, n) in r["reg_golden"].items():
        ws2.append([REG[rc][1], REG[rc][2], n, int(round(m))])
    for c, wd in zip("ABCD", (24, 9, 20, 22)):
        ws2.column_dimensions[c].width = wd
    for cell in ws2[1]:
        cell.font = Font(bold=True)
        cell.alignment = Alignment(wrap_text=True, vertical="top")
    ws3 = wb.create_sheet("Pass mark")
    ws3.append(["Figure", "Value"])
    for k, v in [("Standard: mark on the 2022 Level 1 paper", P.STANDARD_RAW),
                 ("Ability at the standard (logits, Level 1 scale)", round(g["theta"], 3)),
                 ("Expected mark on the 2027 paper at the standard", round(g["expected"], 2)),
                 ("Recommended pass mark", g["pass_mark"]),
                 ("For comparison: expected mark on the bank's final 2026 values", round(d["expected"], 2)),
                 ("Patterns items at the standard (12 items)", f["pr_expected_golden"]),
                 ("Patterns items at the standard on the bank's values", f["pr_expected_bank"])]:
        ws3.append([k, v])
    ws3.column_dimensions["A"].width = 58
    ws3.column_dimensions["B"].width = 12
    ws3["A1"].font = ws3["B1"].font = Font(bold=True)
    ws4 = wb.create_sheet("Shared items")
    ws4.append(["Item", "Context", "Stem words", "Level 1 sittings (logits)", "Level 2 sittings (logits)",
                "Level 1 less Level 2"])
    tab = g["tab"]
    for k, i in enumerate(tab["items"]):
        ws4.append([str(it["code"][i]), "everyday" if it["everyday"][i] else "mathematical", int(it["words"][i]),
                    round(float(r["lv"]["l1"]["b"][i]), 3), round(float(r["lv"]["l2"]["b"][i]), 3),
                    round(float(tab["d"][k]), 3)])
    ws4.append([])
    m = g["model"]["coef"]
    ws4.append(["Fitted on the shared items (weighted by precision)"])
    ws4.append(["Link between the two calibrations (logits)", None, None, None, None, round(float(m[0]), 3)])
    ws4.append(["Reading cost per 100 words of stem (logits)", None, None, None, None, round(float(m[1]), 3)])
    ws4.append(["Everyday-context advantage (logits)", None, None, None, None, round(float(m[2]), 3)])
    for c, wd in zip("ABCDEF", (12, 13, 11, 22, 22, 18)):
        ws4.column_dimensions[c].width = wd
    for cell in ws4[1]:
        cell.font = Font(bold=True)
        cell.alignment = Alignment(wrap_text=True, vertical="top")
    wb.save(path)
    PP.normalize_ooxml(path, "Yvette Clark", "Andrew Adams", "2026-11-18T16:05:00Z", "2026-11-27T20:58:00Z",
                       excel=True)


def write_all(w, r, f, golden_dir):
    os.makedirs(golden_dir, exist_ok=True)
    for x in os.listdir(golden_dir):
        os.remove(os.path.join(golden_dir, x))
    memo(w, r, f, os.path.join(golden_dir, "pass_mark_2027.docx"))
    workbook(w, r, f, os.path.join(golden_dir, "l1_2027_items.xlsx"))
