"""Build the pack and the goldens, write metadata.json and figures.json, run every check and the independent
verifier, build a second time into a scratch folder and require byte-identical output, then cut target.zip.

    python3 task7/generator/make.py [--once] [--target DIR]
"""
import filecmp
import json
import math
import os
import random
import shutil
import subprocess
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import docs
import golden as GD
import postprocess
import pack as PK
import records as RC
import world as W

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")
DISTRACTORS = ["sector_risk_appetite_2027.pdf", "regional_economic_indicators_2019-2026.csv",
               "security_register_2026-12.xlsx", "title_instruments_2026-12.csv",
               "commercial_property_index_2015-2026.csv", "companies_register_extract_2026-12.csv"]


def rnd(x, u):
    return int(math.floor(x / u + 0.5)) * u


def grade_rows(w):
    bands = [(0, 0.01, "1-2", "under 1.0%"), (0.01, 0.02, "3", "1.0% to 2.0%"), (0.02, 0.035, "4", "2.0% to 3.5%"),
             (0.035, 0.06, "5", "3.5% to 6.0%"), (0.06, 0.10, "6", "6.0% to 10.0%"), (0.10, 1.0, "7", "10.0% and over")]
    rows = []
    for lo, hi, g, label in bands:
        n = k = 0
        s = 0.0
        for c in w.customers.values():
            if not c["facilities"] or c["since"] > W.D(2023, 12, 31):
                continue
            if c["exit"] and c["exit"] <= W.D(2023, 12, 31):
                continue
            if PK.in_default(w, c["cid"], W.D(2023, 12, 31)):
                continue
            pd = c["pd"] if c["role"] != "watch" else c["pd"] * 0.25
            if not (lo <= pd < hi):
                continue
            n += 1
            s += pd
            k += any(df["cid"] == c["cid"] and W.D(2024, 1, 1) <= df["first"] <= W.D(2024, 12, 31) for df in w.defaults)
        if n:
            mp = s / n
            tail = sum(math.comb(n, x) * mp ** x * (1 - mp) ** (n - x) for x in range(k, n + 1))
            light = "Green" if tail > 0.05 else ("Amber" if tail > 0.0001 else "Red")
            rows.append([g, label, str(n), "%.1f%%" % (100 * mp), "%.1f%%" % (100 * k / n), light])
    return rows


def build_target(target):
    if os.path.isdir(target):
        shutil.rmtree(target)
    os.makedirs(target)
    w = W.build()
    rows = RC.build(w)
    counts = {"ledger": PK.write_ledger(rows, target), "customers": PK.write_customers(w, target),
              "crosswalk": PK.write_crosswalk(w, target), "defaults": PK.write_defaults(w, target),
              "runs": PK.write_runs(w, target), "security": PK.write_security(w, target),
              "titles": PK.write_titles(w, target), "index": PK.write_index(target)[0],
              "companies": PK.write_companies(w, target), "regional": PK.write_regional(target)}
    docs.terms(target)
    docs.watch_list(w, target)
    docs.validation(w, target, grade_rows(w))
    docs.appetite(target)
    stamp = 1800560400   # 22 January 2027, 09:40 NZDT
    for f in os.listdir(target):
        os.utime(os.path.join(target, f), (stamp, stamp))
    return w, counts


def short(name):
    return name.replace(" Limited", "")


ENVELOPES = [4_500_000, 5_000_000, 5_500_000, 6_000_000, 6_500_000]


def listing(ns):
    ns = sorted(ns)
    return ns[0] if len(ns) == 1 else ", ".join(ns[:-1]) + " and " + ns[-1]


def compute(target, w):
    lines = {c["cid"]: c["line"] for c in w.watch.values()}
    names = {c["cid"]: c["name"] for c in w.watch.values()}
    P = GD.Pack(target, lines)
    p1, k1, n1, _ = P.p1(0.30)
    p0, k0, n0 = P.p0(0.30)
    up = p1 - p0
    own = {c: P.own(c) for c in lines}
    val = P.values(up)
    best, tot, runner, rtot = P.best_set(val)
    tb, ttot, _, _ = P.best_set(own)
    order = sorted(lines, key=lambda c: -val[c])
    nm = lambda s: listing([short(names[c]) for c in s])
    fallback = {}
    for c in sorted(best, key=lambda c: names[c]):
        s, t, used, lead = P.best_at(val, W.ENVELOPE, without=(c,))
        fallback[short(names[c])] = {"intake": nm(s), "lines": used, "kept_off": rnd(t, 50_000),
                                     "unrounded": round(t, 2), "lead": round(lead, 2)}
    curve = []
    for e in ENVELOPES:
        s, t, used, lead = P.best_at(val, e)
        curve.append({"envelope": e, "intake": nm(s), "lines": used, "kept_off": rnd(t, 50_000),
                      "unrounded": round(t, 2), "lead": round(lead, 2)})

    F = {
        "call": " and ".join(short(names[c]) for c in sorted(best, key=lambda c: names[c])),
        "call_ids": sorted(best),
        "total_kept_off": rnd(tot, 50_000),
        "total_unrounded": round(tot, 2),
        "lines_chosen": sum(lines[c] for c in best),
        "envelope": W.ENVELOPE,
        "default_path_call": " and ".join(short(names[c]) for c in sorted(tb, key=lambda c: names[c])),
        "default_path_total": rnd(ttot, 50_000),
        "runner_up": " and ".join(short(names[c]) for c in sorted(runner, key=lambda c: names[c])),
        "runner_up_total": rnd(rtot, 50_000),
        "p1_k": k1, "p1_n": n1, "p0_k": k0, "p0_n": n0,
        "p1": round(p1, 4), "p0": round(p0, 4), "uplift": round(up, 4),
        "kept_off": {short(names[c]): rnd(val[c], 50_000) for c in order},
        "kept_off_unrounded": {short(names[c]): round(val[c], 2) for c in order},
        "own": {short(names[c]): round(own[c], 2) for c in order},
        "own_k": {short(names[c]): rnd(own[c], 1_000) for c in order},
        "dependants": {short(names[c]): len(P.dependents(c)) for c in order},
        "dependant_divisions": {short(names[c]): len({P.cust[d]["sector"] for d in P.dependents(c)}) for c in order},
        "dependants_lgd_ead": {short(names[c]): round(sum(P.lgd_ead(d) for d in P.dependents(c)), 2) for c in order},
        "order": [short(names[c]) for c in order],
        "lines": {short(names[c]): lines[c] for c in order},
        "fallback": fallback,
        "envelopes": ENVELOPES,
        "envelope_curve": curve,
        "write_off_rounding": 50_000,
        "migration_date": W.MIGRATION.strftime("%d/%m/%Y"),
        "dependence_threshold_pct": 30,
        "threshold_corridor_pct": [10, 45],
        "follow_up_corridor_months": [9, 18],
    }
    return F, P


# ---- goldens ---------------------------------------------------------------------------------------------
def write_golden_xlsx(F, path):
    import openpyxl
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    wb = openpyxl.Workbook()
    wb.properties.creator = wb.properties.lastModifiedBy = "Lance Middlemiss"
    ws = wb.active
    ws.title = "Intake 2027"
    navy = "1F3A5F"
    thin = Side(style="thin", color="999999")

    def header(sheet, row, labels, left):
        for j, lab in enumerate(labels, 1):
            c = sheet.cell(row, j, lab)
            c.font = Font(bold=True, color="FFFFFF")
            c.fill = PatternFill("solid", fgColor=navy)
            c.alignment = Alignment(wrap_text=True, vertical="top", horizontal="left" if j in left else "right")
        sheet.row_dimensions[row].height = 46

    def money(sheet, row, cols):
        for j in cols:
            sheet.cell(row, j).number_format = "#,##0"

    def ruled(sheet, row, ncol):
        for j in range(1, ncol + 1):
            sheet.cell(row, j).border = Border(bottom=thin)

    ws["A1"] = "2027 intake: take on %s" % F["call"]
    ws["A1"].font = Font(bold=True, size=13, color=navy)
    ws["A2"] = "For the Credit Committee, February 2027 meeting. Values at the 31 December 2026 IFRS 9 run, in NZ$."
    ws["A2"].font = Font(italic=True, size=9, color="555555")
    ws["A4"], ws["C4"] = "Take on", F["call"]
    ws["A5"], ws["C5"] = "Working-capital lines", F["lines_chosen"]
    ws["D5"] = "of the %s envelope" % format(F["envelope"], ",")
    ws["A6"], ws["C6"] = "Write-off kept off, 2027 (nearest 50,000)", F["total_kept_off"]
    for r in (4, 5, 6):
        ws.cell(r, 1).font = Font(bold=True)
    ws["C5"].number_format = ws["C6"].number_format = "#,##0"
    ws["C5"].alignment = ws["C6"].alignment = Alignment(horizontal="right")

    hr = 8
    header(ws, hr, ["Rank", "Borrower", "Proposed line", "Own expected write-off (nearest 1,000)",
                    "Write-off kept off the book (nearest 50,000)", "Taken on"], left=(2, 6))
    taken = set(F["call"].split(" and "))
    for i, b in enumerate(F["order"], 1):
        r = hr + i
        for j, v in enumerate([i, b, F["lines"][b], F["own_k"][b], F["kept_off"][b], "Yes" if b in taken else ""], 1):
            ws.cell(r, j, v)
        money(ws, r, (3, 4, 5))
        ruled(ws, r, 6)
        if b in taken:
            for j in range(1, 7):
                ws.cell(r, j).fill = PatternFill("solid", fgColor="E8EEF5")
    fb = hr + len(F["order"]) + 2
    ws.cell(fb, 1, "If a borrower taken on turns its package down").font = Font(bold=True, color=navy)
    header(ws, fb + 1, ["", "Turns its package down", "Fall-back intake", "", "Working-capital lines",
                        "Write-off kept off (nearest 50,000)"], left=(2, 3))
    ws.merge_cells(start_row=fb + 1, start_column=3, end_row=fb + 1, end_column=4)
    r = fb + 1
    for b, x in F["fallback"].items():
        r += 1
        ws.cell(r, 2, b)
        ws.cell(r, 3, x["intake"])
        ws.merge_cells(start_row=r, start_column=3, end_row=r, end_column=4)
        ws.cell(r, 5, x["lines"])
        ws.cell(r, 6, x["kept_off"])
        money(ws, r, (5, 6))
        ruled(ws, r, 6)
    notes = [
        "Write-off kept off the book is the borrower's own expected write-off plus the defaults its package prevents "
        "among Ruahine borrowers that take most of their receipts from it, at the rise in default the bank's own 2022 "
        "to 2025 record shows: %d of %d such borrowers defaulted within a year of their main payer's default, against "
        "%d in %d borrower-years where the main payer kept trading. Each default is valued at the borrower's facility "
        "LGD times EAD in the 31 December 2026 run (terms of reference, section 3.5)."
        % (F["p1_k"], F["p1_n"], F["p0_k"], F["p0_n"]),
        "A fall-back intake is the best whole-package choice inside the envelope from the other watch-list borrowers. "
        "The intake at other envelope sizes is on the next sheet.",
    ]
    r0 = r + 2
    for i, txt in enumerate(notes):
        rr = r0 + i
        ws.cell(rr, 1, txt).font = Font(size=9, color="444444")
        ws.cell(rr, 1).alignment = Alignment(wrap_text=True, vertical="top")
        ws.merge_cells(start_row=rr, start_column=1, end_row=rr, end_column=6)
        ws.row_dimensions[rr].height = 52 if i == 0 else 26
    for col, wd in zip("ABCDEF", [7, 30, 16, 17, 19, 19]):
        ws.column_dimensions[col].width = wd
    ws.freeze_panes = "A%d" % (hr + 1)
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.print_area = "A1:F%d" % (r0 + len(notes) - 1)

    ws2 = wb.create_sheet("Envelope")
    ws2["A1"] = "Intake by envelope: Matai Valley Foods in every one"
    ws2["A1"].font = Font(bold=True, size=12, color=navy)
    ws2["A2"] = "The whole-package intake that keeps the most 2027 write-off off the book at each envelope, in NZ$."
    ws2["A2"].font = Font(italic=True, size=9, color="555555")
    header(ws2, 4, ["Envelope", "Intake", "Working-capital lines", "Write-off kept off (nearest 50,000)"], left=(2,))
    for i, x in enumerate(F["envelope_curve"]):
        r = 5 + i
        for j, v in enumerate([x["envelope"], x["intake"], x["lines"], x["kept_off"]], 1):
            ws2.cell(r, j, v)
        money(ws2, r, (1, 3, 4))
        ruled(ws2, r, 4)
        if x["envelope"] == F["envelope"]:
            for j in range(1, 5):
                ws2.cell(r, j).fill = PatternFill("solid", fgColor="E8EEF5")
    rr = 5 + len(F["envelope_curve"]) + 1
    ws2.cell(rr, 1, "Each intake is valued as on the first sheet; the 2027 envelope approved by the Board is "
                    "NZ$%s (terms of reference, section 3.1)." % format(F["envelope"], ",")).font = Font(size=9, color="444444")
    ws2.cell(rr, 1).alignment = Alignment(wrap_text=True, vertical="top")
    ws2.merge_cells(start_row=rr, start_column=1, end_row=rr, end_column=4)
    ws2.row_dimensions[rr].height = 30
    for col, wd in zip("ABCD", [14, 52, 16, 19]):
        ws2.column_dimensions[col].width = wd
    ws2.freeze_panes = "A5"
    ws2.page_setup.orientation = "landscape"
    ws2.print_area = "A1:D%d" % rr
    wb.save(path)
    postprocess.scrub(path, "Lance Middlemiss", "2027-01-22")
    postprocess.finish_office(path, "2027-01-22T01:14:00Z", "2027-01-22T03:36:00Z", "Ruahine Bank")


WORDS = {1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven", 8: "Eight", 9: "Nine",
         10: "Ten", 11: "Eleven", 12: "Twelve"}


def write_golden_docx(F, path):
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Cm, Pt, RGBColor
    k = F["kept_off"]
    c = lambda x: format(x, ",")
    doc = Document()
    sec = doc.sections[0]
    sec.left_margin = sec.right_margin = Cm(2.2)
    sec.top_margin = sec.bottom_margin = Cm(1.8)
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    st.paragraph_format.space_after = Pt(6)
    h = doc.add_heading("2027 intake: take on %s" % F["call"], level=1)
    for r in h.runs:
        r.font.size = Pt(15)
    meta = doc.add_table(rows=4, cols=2)
    for i, (a_, b_) in enumerate([("To", "Credit Committee, February 2027 meeting"),
                                  ("From", "Stella Perano, Head of Business Support"),
                                  ("Prepared by", "Lance Middlemiss, Credit Risk"),
                                  ("Date", "22 January 2027")]):
        meta.cell(i, 0).text, meta.cell(i, 1).text = a_, b_
        meta.cell(i, 0).paragraphs[0].runs[0].bold = True
        for cc in (meta.cell(i, 0), meta.cell(i, 1)):
            cc.paragraphs[0].paragraph_format.space_after = Pt(0)
    meta.columns[0].width = Cm(3.0)
    for cell in meta.columns[0].cells:
        cell.width = Cm(3.0)
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.add_run("Recommendation. ").bold = True
    p.add_run("Take on %s. Their working-capital lines use NZ$%s of the NZ$%s envelope, and the two packages keep "
              "NZ$%s of 2027 write-off off Ruahine's book." % (F["call"], c(F["lines_chosen"]), c(F["envelope"]),
                                                                c(F["total_kept_off"])))
    p = doc.add_paragraph()
    p.add_run("Why Matai rather than Ridgeway. ").bold = True
    p.add_run("Ranked on each borrower's own expected write-off, the envelope would go to Kinloch Engineering and "
              "Ridgeway Precast: Matai's own figure is NZ$%s against Ridgeway's NZ$%s. That ranking leaves out what a "
              "package does for the borrowers that depend on the one we support. %s of our borrowers, in packaging, "
              "labels, pallets, haulage, cold storage, cleaning, labour hire and engineering, take most of their "
              "receipts from Matai Valley Foods. In our own record, %d of the %d borrowers whose main payer defaulted "
              "between 2022 and 2025 defaulted within a year, against %d in %d borrower-years where a borrower just as "
              "dependent had a main payer that kept trading. Borrowers that took a smaller share from a failing payer are "
              "no comparison, as the same default reached them. A package that keeps Matai trading keeps its "
              "dependants at the lower rate, so it is worth NZ$%s against NZ$%s at Ridgeway, whose %s dependant adds "
              "little to its own figure."
              % (c(F["own_k"]["Matai Valley Foods"]), c(F["own_k"]["Ridgeway Precast"]),
                 WORDS[F["dependants"]["Matai Valley Foods"]], F["p1_k"], F["p1_n"], F["p0_k"], F["p0_n"],
                 c(k["Matai Valley Foods"]), c(k["Ridgeway Precast"]),
                 WORDS[F["dependants"]["Ridgeway Precast"]].lower()))
    t = doc.add_table(rows=1, cols=4)
    t.style = "Light Grid Accent 1"
    for j, hd in enumerate(["Borrower", "Write-off kept off (NZ$)", "Proposed line (NZ$)", "Taken on"]):
        t.rows[0].cells[j].text = hd
    taken = set(F["call"].split(" and "))
    for b in F["order"]:
        row = t.add_row().cells
        row[0].text, row[1].text, row[2].text, row[3].text = b, c(k[b]), c(F["lines"][b]), "Yes" if b in taken else ""
        for j in (1, 2):
            row[j].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    for j in (1, 2):
        t.rows[0].cells[j].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    t.autofit = False
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    lay = OxmlElement("w:tblLayout")
    lay.set(qn("w:type"), "fixed")
    t._tbl.tblPr.append(lay)
    widths = [Cm(6.4), Cm(4.0), Cm(3.6), Cm(2.4)]
    for gc, wd in zip(t._tbl.tblGrid.findall(qn("w:gridCol")), widths):
        gc.set(qn("w:w"), str(int(wd.twips)))
    for j, wd in enumerate(widths):
        for cell in t.columns[j].cells:
            cell.width = wd
    src = doc.add_paragraph("Write-off to the nearest NZ$50,000, each default valued at the borrower's facility LGD times "
                            "EAD in the 31 December 2026 IFRS 9 run (terms of reference, section 3.5).")
    src.paragraph_format.space_before = Pt(3)
    for r in src.runs:
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
    fbk, fbm = F["fallback"]["Kinloch Engineering"], F["fallback"]["Matai Valley Foods"]
    p = doc.add_paragraph()
    p.add_run("If a package is turned down. ").bold = True
    p.add_run("Should Kinloch Engineering turn its package down, the unit falls back on %s (NZ$%s kept off); should "
              "Matai Valley Foods, on %s (NZ$%s, Ridgeway's own dependant included). Matai is in the best intake at "
              "every envelope from NZ$%s to NZ$%s, set out on the workbook's second sheet, where a ranking on own "
              "figures never takes it."
              % (fbk["intake"], c(fbk["kept_off"]), fbm["intake"], c(fbm["kept_off"]),
                 c(F["envelopes"][0]), c(F["envelopes"][-1])))
    fp = sec.footer.paragraphs[0]
    fp.text = "Ruahine Bank  |  Credit Committee  |  Restricted"
    for r in fp.runs:
        r.font.size = Pt(8)
        r.font.color.rgb = RGBColor(0x66, 0x66, 0x66)
    cp = doc.core_properties
    cp.author = cp.last_modified_by = "Lance Middlemiss"
    cp.title = "Business Support Unit intake 2027"
    import datetime as dt
    cp.created = cp.modified = dt.datetime(2027, 1, 22, 2, 5, 0)
    cp.revision = 3
    doc.save(path)
    postprocess.scrub(path, "Lance Middlemiss", "2027-01-22")
    postprocess.finish_office(path, "2027-01-22T02:05:00Z", "2027-01-22T03:58:00Z", "Ruahine Bank")


def write_submission(F, path):
    k = F["kept_off"]
    c = lambda x: format(x, ",")
    fbk, fbm = F["fallback"]["Kinloch Engineering"], F["fallback"]["Matai Valley Foods"]
    L = []
    L.append("## Tags\n")
    L.append("**Domain:** Banking, Credit & Financial Risk (expected credit loss provisioning).  ")
    L.append("**Analytical objective:** Opportunity Sizing & Decision Support.\n")
    L.append("## Final Recommendation\n")
    L.append("**The business support unit should take on %s, keeping NZ$%s of 2027 write-off off Ruahine's book "
             "with NZ$%s of the NZ$%s envelope.** A package at Matai also keeps out of default the Ruahine borrowers "
             "that take most of their receipts from it. Not %s, which lead on the two borrowers' own expected "
             "write-off but leave Matai's dependants exposed. Not %s, the next-best pair inside the envelope, "
             "which gives up Kinloch's NZ$%s for Ridgeway's NZ$%s.\n"
             % (F["call"], c(F["total_kept_off"]), c(F["lines_chosen"]), c(F["envelope"]), F["default_path_call"],
                F["runner_up"], c(k["Kinloch Engineering"]), c(k["Ridgeway Precast"])))
    L.append("## Supplementary Questions\n")
    L.append("### bsu_intake_2027.xlsx\n")
    L.append("1. The first sheet opens with the choice and its total: take on %s; 2027 write-off kept off the book "
             "NZ$%s. The eight watch-list packages it was chosen from sit below, largest first."
             % (F["call"], c(F["total_kept_off"])))
    L.append("2. For each borrower taken on, the intake to fall back on were it to turn its package down, and the "
             "2027 write-off that intake keeps off, New Zealand dollars to the nearest %s:" % c(F["write_off_rounding"]))
    L.append("   - Kinloch Engineering turns its package down: %s, NZ$%s" % (fbk["intake"], c(fbk["kept_off"])))
    L.append("   - Matai Valley Foods turns its package down: %s, NZ$%s" % (fbm["intake"], c(fbm["kept_off"])))
    L.append("3. A second sheet with one row per envelope, giving the intake and the 2027 write-off it keeps off:")
    for x in F["envelope_curve"]:
        L.append("   - NZ$%s: %s, NZ$%s" % (c(x["envelope"]), x["intake"], c(x["kept_off"])))
    L.append("\n### bsu_intake_2027.docx\n")
    L.append("4. A note to the credit committee giving the recommendation and its reasoning: Matai Valley Foods' own "
             "expected write-off of NZ$%s against NZ$%s once its dependants are counted, the record's comparison "
             "behind that figure, and the fall-back intakes." % (c(F["own_k"]["Matai Valley Foods"]),
                                                                 c(k["Matai Valley Foods"])))
    L.append("")
    L.append("## Critical Components\n")
    L.append("1. A package at Matai Valley Foods also keeps out of default the **%d** Ruahine borrowers taking most of "
             "their 2026 receipts from it, and one at Ridgeway Precast the **%d** taking most of its receipts from "
             "Ridgeway; no other watch-list borrower has such a borrower"
             % (F["dependants"]["Matai Valley Foods"], F["dependants"]["Ridgeway Precast"]))
    L.append("2. That protection is measured against borrowers just as dependent on a payer that kept trading: "
             "borrowers taking 30 per cent or more of their receipts from a payer that defaulted in 2022 to 2025 "
             "defaulted within twelve months **%d** times in **%d**, against **%d** times in **%d** borrower-years "
             "whose such payer was neither in default nor defaulting" % (F["p1_k"], F["p1_n"], F["p0_k"], F["p0_n"]))
    L.append("3. Priced that way, Matai Valley Foods' package keeps **NZ$%s** off the book, more than twice its own "
             "expected write-off of **NZ$%s**\n" % (c(k["Matai Valley Foods"]), c(F["own_k"]["Matai Valley Foods"])))
    L.append("## Step-by-Step\n")
    L.append("1. Summed twelve-month PD times LGD times EAD over each watch-list borrower's facilities in "
             "ifrs9_facility_run_2026-12-31.csv, borrowers and proposed lines from watch_list_2027-01.pdf: Kinloch "
             "Engineering NZ$%s, Ridgeway Precast NZ$%s and Matai Valley Foods NZ$%s of their own. Filling the "
             "envelope on these figures alone takes %s for NZ$%s, the reasonable analysis this answer rejects."
             % (c(F["own_k"]["Kinloch Engineering"]), c(F["own_k"]["Ridgeway Precast"]),
                c(F["own_k"]["Matai Valley Foods"]), F["default_path_call"], c(F["default_path_total"])))
    L.append("2. Built each customer's 2026 receipts in business_account_transactions_2021-2026.csv, own-account "
             "transfers and Ruahine lending left out and on-us counterparties resolved through "
             "customer_master_2026-12.xlsx and account_number_crosswalk_2023.csv: %d borrowers take most of their "
             "receipts from Matai Valley Foods and %d from Ridgeway Precast."
             % (F["dependants"]["Matai Valley Foods"], F["dependants"]["Ridgeway Precast"]))
    L.append("3. Dated each default by its first trigger in default_register_2021-2026.csv, with cures from "
             "default_cures_2021-2026.csv, per the definition in ifrs9_pd_model_validation_2025.pdf: %d of %d "
             "borrowers that had taken 30 per cent or more of their receipts in the previous twelve months from a "
             "payer that defaulted in 2022 to 2025, and were performing at its first trigger, defaulted within twelve "
             "months of it." % (F["p1_k"], F["p1_n"]))
    L.append("4. Measured that against borrowers just as dependent on a payer that kept trading: %d of %d "
             "borrower-years from 2022 to 2025 in which a performing borrower took 30 per cent or more of the previous "
             "year's receipts from a Ruahine borrower neither in default at the start of the year nor defaulting during "
             "it (any share from %d to %d per cent selects the same borrowers). Borrowers that took a smaller share "
             "from a failing payer are no control, because that default reached them too."
             % (F["p0_k"], F["p0_n"], F["threshold_corridor_pct"][0], F["threshold_corridor_pct"][1]))
    L.append("5. Added to each watch-list borrower its PD times %s (%d of %d less %d of %d) times each dependant's LGD "
             "times EAD and ranked the eight: Matai Valley Foods NZ$%s, Kinloch Engineering NZ$%s, Ridgeway Precast "
             "NZ$%s with its one dependant, the rest their own figures."
             % (F["uplift"], F["p1_k"], F["p1_n"], F["p0_k"], F["p0_n"], c(k["Matai Valley Foods"]),
                c(k["Kinloch Engineering"]), c(k["Ridgeway Precast"])))
    L.append("6. Chose, under section 3 of bsu_terms_of_reference_2027.pdf (a NZ$%s envelope, whole packages), the "
             "proposed lines with the largest total: %s, NZ$%s, ahead of %s at NZ$%s."
             % (c(F["envelope"]), F["call"], c(F["total_kept_off"]), F["runner_up"], c(F["runner_up_total"])))
    L.append("7. Solved the same choice without each borrower taken on (Kinloch Engineering out: %s, NZ$%s; Matai "
             "Valley Foods out: %s, NZ$%s) and at each envelope from NZ$%s to NZ$%s (%s), Matai in every intake."
             % (fbk["intake"], c(fbk["kept_off"]), fbm["intake"], c(fbm["kept_off"]), c(F["envelopes"][0]),
                c(F["envelopes"][-1]), "; ".join("NZ$%s" % c(x["kept_off"]) for x in F["envelope_curve"])))
    L.append("")
    L.append("No other conclusion survives. Ranking on the borrowers' own expected write-off, twelve-month or "
             "lifetime, or adding the dependants' own IFRS 9 expected loss, keeps Ridgeway, because the IFRS 9 model "
             "scores each borrower on its own accounts and the trade dependence sits only in the payments ledger; an "
             "assumed rise, or one pooled over every payee of a failing payer whatever its share, keeps Ridgeway too. "
             "Measuring the rise against the less dependent payees of the same failing payers, or against the book's "
             "default rate, keeps the choice but understates the rise, Matai's figure and every intake that holds "
             "Matai, since the payer's default reached those borrowers too. Any receipts threshold from %d to %d per "
             "cent, a %d- to %d-month follow-up, and a baseline from payers that never defaulted or from the "
             "dependants' own PDs file the same figures."
             % (F["threshold_corridor_pct"][0], F["threshold_corridor_pct"][1], F["follow_up_corridor_months"][0],
                F["follow_up_corridor_months"][1]))
    open(path, "w").write("\n".join(L) + "\n")


def write_metadata(counts, target, path):
    files = []
    desc = {
        "business_account_transactions_2021-2026.csv": "core banking extract of business transaction accounts, one row per posted transaction",
        "customer_master_2026-12.xlsx": "business customer register and their accounts at December 2026",
        "account_number_crosswalk_2023.csv": "legacy to new account numbers at the June 2023 core banking conversion",
        "default_register_2021-2026.csv": "default triggers raised by the credit and collections teams",
        "default_cures_2021-2026.csv": "cures recorded by the credit team",
        "ifrs9_facility_run_2026-12-31.csv": "IFRS 9 facility run as at 31 December 2026",
        "ifrs9_facility_run_2024-12-31.csv": "IFRS 9 facility run as at 31 December 2024",
        "security_register_2026-12.xlsx": "property securities, guarantees and the deed log held by Lending Services",
        "title_instruments_2026-12.csv": "mortgage instruments registered against the secured titles",
        "commercial_property_index_2015-2026.csv": "regional commercial property index by quarter and release",
        "companies_register_extract_2026-12.csv": "companies register extract for the bank's business customers",
        "regional_economic_indicators_2019-2026.csv": "regional economic series by quarter",
        "bsu_terms_of_reference_2027.pdf": "Business Support Unit terms of reference for 2027",
        "watch_list_2027-01.pdf": "Credit Committee watch list, January 2027",
        "ifrs9_pd_model_validation_2025.pdf": "annual validation of the business PD model, 2025",
        "sector_risk_appetite_2027.pdf": "sector risk appetite for business lending, 2027",
    }
    for f in sorted(os.listdir(target)):
        files.append({"path": f, "format": f.rsplit(".", 1)[-1], "bytes": os.path.getsize(os.path.join(target, f)),
                      "covers": desc[f], "made": "constructed by task7/generator/make.py (seeded, deterministic)"})
    meta = {
        "task": "task7",
        "title": "Business Support Unit intake, 2027",
        "domain": "Banking, Credit & Financial Risk",
        "task_type": "expected credit loss provisioning",
        "objective": "Opportunity Sizing & Decision Support",
        "as_of": "2027-01-22",
        "deliverables": ["bsu_intake_2027.xlsx", "bsu_intake_2027.docx"],
        "distractor_files": DISTRACTORS,
        "input_gates": {"files": len(files), "formats": sorted(set(x["format"] for x in files)),
                        "largest_file": "business_account_transactions_2021-2026.csv",
                        "largest_file_rows": counts["ledger"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task around a fictional New Zealand member-owned bank, its "
                               "business customers and people; every record and figure is invented.",
                     "date": "2027-01-22", "license": "CC BY 4.0 (original work)"}],
        "files": files,
    }
    json.dump(meta, open(path, "w"), indent=1)


def zip_target(target, path, names=None):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(names or os.listdir(target)):
            zi = zipfile.ZipInfo(f, date_time=(2027, 1, 22, 9, 40, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(target, f), "rb").read())


def same_tree(a, b):
    fa, fb = sorted(os.listdir(a)), sorted(os.listdir(b))
    if fa != fb:
        return False
    return all(filecmp.cmp(os.path.join(a, f), os.path.join(b, f), shallow=False) for f in fa)


def main():
    once = "--once" in sys.argv
    tgt = sys.argv[sys.argv.index("--target") + 1] if "--target" in sys.argv else TARGET
    w, counts = build_target(tgt)
    F, P = compute(tgt, w)
    json.dump(F, open(os.path.join(HERE, "figures.json"), "w"), indent=1, ensure_ascii=False)
    if tgt != TARGET:
        print(json.dumps({k: F[k] for k in ("call", "total_kept_off", "kept_off")}, ensure_ascii=False))
        return
    os.makedirs(GOLDEN, exist_ok=True)
    write_golden_xlsx(F, os.path.join(GOLDEN, "bsu_intake_2027.xlsx"))
    write_golden_docx(F, os.path.join(GOLDEN, "bsu_intake_2027.docx"))
    zip_target(GOLDEN, os.path.join(TASK, "golden.zip"), ["bsu_intake_2027.xlsx", "bsu_intake_2027.docx"])
    write_submission(F, os.path.join(TASK, "submission.md"))
    write_metadata(counts, tgt, os.path.join(TASK, "metadata.json"))
    for script in ("checks.py", "verify.py"):
        if os.path.exists(os.path.join(HERE, script)):
            r = subprocess.run([sys.executable, os.path.join(HERE, script)], capture_output=True, text=True)
            print(r.stdout[-3000:])
            if r.returncode != 0:
                print(r.stderr[-3000:])
                sys.exit("%s failed" % script)
    if not once:
        tmp = tempfile.mkdtemp(prefix="t127b-")
        build_target(os.path.join(tmp, "target"))
        ok = same_tree(tgt, os.path.join(tmp, "target"))
        shutil.rmtree(tmp, ignore_errors=True)
        print("byte-identical second build:", ok)
        if not ok:
            sys.exit("rebuild differs")
        zip_target(tgt, os.path.join(TASK, "target.zip"))
    print(json.dumps({k: F[k] for k in ("call", "total_kept_off")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
