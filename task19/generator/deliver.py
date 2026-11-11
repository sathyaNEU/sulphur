"""task19 golden deliverables: the Statistics Office's workbook of mid-2026 district estimates and the short note that
goes with it to the Commission. Every figure comes from figures.json."""
import datetime as dt
import os

import openpyxl
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt
from openpyxl.styles import Alignment, Font, PatternFill

import postprocess

WORKBOOK = "kilvarra_district_population_mid2026.xlsx"
NOTE = "memo_district_estimates_mid2026.docx"
ORG = "Kilvarra Statistics Office"
AUTHOR = "Grainne Grennan"
SAVED_XL = ("2026-11-24T09:41:00Z", "2026-12-02T16:18:00Z")
SAVED_DOC = ("2026-12-01T10:05:00Z", "2026-12-03T11:52:00Z")
HEAD = Font(bold=True)
SHADE = PatternFill("solid", fgColor="DDE6F0")


def n0(x):
    return "{:,}".format(int(round(x)))


def write(F, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    names = F["district_names"]
    dists = list(F["district_estimates"].keys())
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Estimates"
    ws["A1"] = "Usual residents at 30 June 2026, by district: estimates for the 2027/28 grant determination"
    ws["A1"].font = Font(bold=True, size=12)
    hdr = ["District code", "District", "Estimate", "90% interval: lower", "90% interval: upper",
           "Chance of 25,000 or more", "Urban-services supplement", "Health register count"]
    for j, h in enumerate(hdr, 1):
        c = ws.cell(row=3, column=j, value=h)
        c.font = HEAD
        c.fill = SHADE
        c.alignment = Alignment(wrap_text=True, vertical="top")
    call = F["call"]
    row = 4
    for d in dists:
        lo, hi = F["district_intervals"][d]
        verdict = ("qualifies" if d in call["qualifies"] else
                   "too close to call (half rate)" if d in call["too close to call"] else "does not qualify")
        p = F["p_line"][d]
        ptxt = "over 0.99" if p > 0.99 else ("under 0.01" if p < 0.01 else p)
        vals = [d, names[d], F["district_estimates"][d], lo, hi, ptxt, verdict, F["register_counts"][d]]
        for j, v in enumerate(vals, 1):
            ws.cell(row=row, column=j, value=v)
        row += 1
    ws.cell(row=row, column=1, value="Kilvarra").font = HEAD
    lo, hi = F["national_interval"]
    for j, v in ((3, F["national_estimate"]), (4, lo), (5, hi), (8, F["register_national"])):
        ws.cell(row=row, column=j, value=v).font = HEAD
    for j, w in enumerate([10, 14, 11, 12, 12, 12, 26, 12], 1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(j)].width = w
    for r in range(4, row + 1):
        for c in (3, 4, 5, 8):
            ws.cell(row=r, column=c).number_format = "#,##0"
    ws.cell(row=row + 2, column=1, value="Estimates rounded to the nearest 10 and interval ends to the nearest 10 (nearest 100 "
                                         "for Kilvarra). Fort Larrick includes serving personnel at Larrick Barracks from the "
                                         "Defence Forces' return.").font = Font(italic=True, size=8)
    ws.freeze_panes = "C4"

    ws = wb.create_sheet("Register to estimate")
    ws["A1"] = "From each district's health register count to its estimate (persons)"
    ws["A1"].font = Font(bold=True, size=12)
    parts = ["left Kilvarra or died", "duplicate registrations", "living elsewhere in Kilvarra"]
    hdr = ["District", "Register count", "less: left Kilvarra or died", "less: duplicate registrations",
           "less: living elsewhere in Kilvarra", "plus: residents listed in another district",
           "plus: residents on no list", "plus: serving personnel", "Estimate"]
    for j, h in enumerate(hdr, 1):
        c = ws.cell(row=3, column=j, value=h)
        c.font = HEAD
        c.fill = SHADE
        c.alignment = Alignment(wrap_text=True, vertical="top")
    r = 4
    for d in dists:
        pp = F["register_not_correct_parts"][d]
        forces = F["district_estimates"][d] - (F["register_counts"][d] - F["register_not_correct"][d] +
                                               F["listed_elsewhere"][d] + F["on_no_list"][d]) if d == "D04" else 0
        vals = [names[d], F["register_counts"][d]] + [pp[p] for p in parts] + [F["listed_elsewhere"][d], F["on_no_list"][d],
                                                                                forces, F["district_estimates"][d]]
        for j, v in enumerate(vals, 1):
            ws.cell(row=r, column=j, value=v).number_format = "#,##0"
        r += 1
    ws.cell(row=r + 1, column=1, value="Parts rounded to the nearest 10; they add to the estimate within rounding. Entries the "
                                        "follow-up could not place (not known at the address, vacant, no contact) are shared "
                                        "as the district's placed outcomes are.").font = Font(italic=True, size=8)
    for j, w in enumerate([14, 11, 12, 12, 13, 13, 12, 11, 11], 1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(j)].width = w

    ws = wb.create_sheet("National bridge")
    ws["A1"] = "From the rolled-forward estimate for 30 June 2026 to this estimate (persons)"
    ws["A1"].font = Font(bold=True, size=12)
    rows = [["Rolled-forward estimate, 30 June 2026", F["official_2026"]],
            ["less: emigrants since mid-2021 the accounts did not record", -F["unrecorded_emigration"]],
            ["plus: arrivals on the border record missing from the accounts", F["immigration_not_in_accounts"]],
            ["less: remainder (the 2021 base and other components)", -F["official_remainder"]],
            ["This estimate", F["national_estimate"]]]
    for i, (a, b) in enumerate(rows, 3):
        ws.cell(row=i, column=1, value=a)
        ws.cell(row=i, column=2, value=b).number_format = "#,##0"
    ws.column_dimensions["A"].width = 58
    ws.column_dimensions["B"].width = 14

    ws = wb.create_sheet("Coverage and factors")
    ws["A1"] = "Coverage of the survey's residents by their own district's register list, and the raising factors"
    ws["A1"].font = Font(bold=True, size=12)
    rows = [["", "Kilvarran citizens", "Other citizenships"],
            ["Linked by the matcher to a record in their own district (%)", F["linked_pct"]["nationals"], F["linked_pct"]["others"]],
            ["Matcher's recall on the clerical review (%)", F["recall_pct"]["nationals"], F["recall_pct"]["others"]],
            ["On their own district's list, missed and false links counted (%)", F["coverage_pct"]["nationals"],
             F["coverage_pct"]["others"]],
            [], ["Raising factor for men", "aged 18 to 29", "aged 30 to 44"],
            ["Births and survival against the estimate's sex ratio", F["raising_factor"]["18-29"], F["raising_factor"]["30-44"]]]
    for i, rr in enumerate(rows, 3):
        for j, v in enumerate(rr, 1):
            ws.cell(row=i, column=j, value=v)
    ws.column_dimensions["A"].width = 62
    ws.column_dimensions["B"].width = 18
    ws.column_dimensions["C"].width = 18
    wpath = os.path.join(out_dir, WORKBOOK)
    wb.save(wpath)
    postprocess.normalize_ooxml(wpath, AUTHOR, AUTHOR, SAVED_XL[0], SAVED_XL[1], excel=True, company=ORG)

    # ---------------------------------------------------------------------------------------------- the note
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    p = doc.add_paragraph()
    r = p.add_run("Mid-2026 district estimates for the 2027/28 grant determination")
    r.bold = True
    r.font.size = Pt(13)
    doc.add_paragraph("To: Secretary, Local Government Grants Commission. From: Population Statistics, Kilvarra Statistics "
                      "Office. 3 December 2026.")
    q = [names[d] for d in call["qualifies"]]
    tc = [names[d] for d in call["too close to call"]]
    nq = [names[d] for d in dists if d not in call["qualifies"] and d not in call["too close to call"]]
    lo, hi = F["national_interval"]
    doc.add_paragraph(
        "Kilvarra had an estimated %s usual residents on 30 June 2026 (90 per cent interval %s to %s). %s qualify for the "
        "urban-services supplement. %s is too close to call: its interval includes 25,000, so under paragraph 3.2 of "
        "circular 2026/14 it is paid at half rate for 2027/28. %s do not qualify." % (
            n0(F["national_estimate"]), n0(lo), n0(hi), ", ".join(q), " and ".join(tc), ", ".join(nq)))
    for d in [x for x in dists if x in call["too close to call"] or x in ("D05", "D06")]:
        lo_, hi_ = F["district_intervals"][d]
        pr = F["p_line"][d]
        ptxt = "over 0.99" if pr > 0.99 else ("under 0.01" if pr < 0.01 else "%.2f" % pr)
        doc.add_paragraph("%s: %s (interval %s to %s); chance of 25,000 or more %s." % (
            names[d], n0(F["district_estimates"][d]), n0(lo_), n0(hi_), ptxt))
    doc.add_paragraph(
        "How the figures were made. Each district's estimate is the number of its health register entries that are correct "
        "for the district, measured by the field follow-up of the entries listed at the coverage survey's addresses, divided "
        "by the share of the people the survey found who are on that district's list. The survey was matched to the register "
        "on names, dates of birth and postcodes, and the clerical review shows what the matching misses: the matcher links "
        "%s per cent of Kilvarran citizens and %s per cent of others to their own district's list, against %s and %s per "
        "cent once missed and false links are counted. The register and the survey miss the same young men, so the "
        "estimate's sex ratios at 18 to 44 fall short of the ones births and survival give; men aged 18 to 29 and 30 to 44 "
        "are raised by %.3f and %.3f. Serving personnel at Larrick Barracks are taken from the Defence Forces' return." % (
            F["linked_pct"]["nationals"], F["linked_pct"]["others"], F["coverage_pct"]["nationals"],
            F["coverage_pct"]["others"], F["raising_factor"]["18-29"], F["raising_factor"]["30-44"]))
    doc.add_paragraph(
        "How sure. The intervals come from resampling the survey's blocks and repeating every step, the clerical review's "
        "measure of the matching and the raising factors included, because those errors move every district together. "
        "Resampling the survey alone gives a national interval of plus or minus %.1f per cent; the full one is plus or "
        "minus %.1f per cent." % (F["careful_halfwidth_pct"], F["national_halfwidth_pct"]))
    doc.add_paragraph(
        "Why the figures differ from the register. Every district's register count is higher than its estimate: the lists "
        "still hold people who have left Kilvarra or died, duplicate registrations and people now living in another "
        "district, partly offset by residents listed elsewhere (students registered at home, recent movers) and residents "
        "on no list. The workbook's second sheet gives each part by district.")
    doc.add_paragraph(
        "Why the figures differ from the rolled-forward estimate. The population accounts put Kilvarra at %s on 30 June "
        "2026, %s above this estimate. About %s emigrants since mid-2021 are still on the register and were never "
        "recorded in the accounts; %s arrivals on the border record are missing from them; the remaining %s sits in the "
        "2021 base and the other components. The accounts and the register share the same unrecorded emigrants, so the "
        "closeness of a register-based figure to the accounts is no check on it." % (
            n0(F["official_2026"]), n0(F["official_gap"]), n0(F["unrecorded_emigration"]),
            n0(F["immigration_not_in_accounts"]), n0(abs(F["official_remainder"]))))
    npath = os.path.join(out_dir, NOTE)
    doc.save(npath)
    postprocess.normalize_docx(npath, AUTHOR, AUTHOR, SAVED_DOC[0], SAVED_DOC[1], revision=4, total_time=96,
                               seed=19, title="Mid-2026 district estimates", company=ORG)
    postprocess.own_mtimes(out_dir, {})
    return [WORKBOOK, NOTE]
