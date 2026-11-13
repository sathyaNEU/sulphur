"""task9: the golden deliverables the prompt asks for, a spreadsheet and a short note for the ramp review, written from
figures.json so every number agrees with the answer blocks."""
import os

import openpyxl
from docx import Document
from docx.shared import Pt
from openpyxl.styles import Alignment, Font, PatternFill

import postprocess as PP

BOOK = "vr90_ramp_yield_review.xlsx"
NOTE = "vr90_ramp_yield_note.docx"
FILES = [BOOK, NOTE]
AUTHOR = "Gitte Ullrich"
FIRM = "Varnholt Halbleiter GmbH"
STAMPS = {BOOK: ("2026-11-09T07:52:00Z", "2026-11-12T16:27:41Z"), NOTE: ("2026-11-11T08:10:00Z", "2026-11-12T11:43:00Z")}
BOLD = Font(bold=True)
HEAD = PatternFill("solid", fgColor="DCE3EC")
ONE, TWO, WHOLE, COUNT = "0.0", "0.00", "0", "#,##0"
# the routes as the review names them (effort.json keeps the generator's own labels)
ROUTE_NAME = {
    "the golden": "this review (the four changes)",
    "the careful but hurried pass": "first reading: the far polishers' consumables, the summer's loading, CM3's recipe alone, "
                                    "a cluster factor of 2 and cleans on RF time, together",
}
CHANGE_NAME = {"loop": "P-02A to 51.5 Hz", "bath": "T3 to the spring life", "edge": "SH-300-B on DP2B with CM3 to R7",
               "etch": "ET1B and ET3A cleans", "CM1 and CM3 filters and pads": "CM1 and CM3 filters and pads",
               "CM3 harmonised alone": "CM3 to R7 alone", "etch on RF hours": "cleans on RF hours"}
CAUSE_NAME = {"R4": "DP2B showerhead with CM3's zone 5 tune", "R2": "oxide slurry loop SDS-OX1",
              "R3": "pre-gate bench T3, chemical life", "R5": "CT-DEEP-07 polymer on ET1B and ET3A"}


def f1(x):
    return "%.1f" % x


def _sheet(wb, title, header, rows, widths, formats=None, first=False):
    """formats: one number format per column (None leaves it); a row may end in a dict {column: format} overriding it"""
    ws = wb.active if first else wb.create_sheet(title)
    ws.title = title
    ws.append(header)
    for c in ws[1]:
        c.font, c.fill = BOLD, HEAD
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for r in rows:
        over = r[-1] if r and isinstance(r[-1], dict) else {}
        vals = r[:-1] if over else r
        ws.append(vals)
        for j, cell in enumerate(ws[ws.max_row]):
            fmt = over.get(j, (formats or [None] * len(header))[j] if j < len(header) else None)
            if fmt and isinstance(cell.value, (int, float)):
                cell.number_format = fmt
            if isinstance(cell.value, str) and len(cell.value) > 40:
                cell.alignment = Alignment(wrap_text=True, vertical="top")
    for i, w in enumerate(widths):
        ws.column_dimensions[openpyxl.utils.get_column_letter(i + 1)].width = w
    ws.freeze_panes = "A2"
    return ws


def write_book(path, fg):
    wb = openpyxl.Workbook()
    s = fg["R1_shortfall"]
    _sheet(wb, "Shortfall", ["product", "good die per wafer, sorted 1 Jan to 31 Mar 2026",
                             "good die per wafer, sorted 1 Jun to 30 Sep 2026", "shortfall, good die per wafer"],
           [["VX40", fg["vx40_base_good"], fg["vx40_win_good"], s["VX40"]],
            ["VP12", fg["vp12_base_good"], fg["vp12_win_good"], s["VP12"]]], [10, 26, 26, 18],
           [None, ONE, ONE, ONE], first=True)
    causes = sorted([("R4", fg["R4_edge"]), ("R2", fg["R2_loop"]), ("R3", fg["R3_bath"]), ("R5", fg["R5_etch"])],
                    key=lambda x: -x[1]["VX40"])
    what = {"R2": "the oxide slurry loop SDS-OX1 since its pump went to 38 Hz on 2 June: scratching grows with each "
                  "polisher's distance along the loop (CM2 at 64 m, CM4 148 m, CM1 231 m, CM3 318 m) and fell away on "
                  "the standby pump, 10 to 24 August",
            "R3": "the pre-gate bench tank T3 on the chemical life of ECN-2026-0417 from 1 July: metals build with every lot "
                  "between spikes and drain-and-fills (rebuilt from the bench log and the lab's samples)",
            "R4": "DP2B's SH-300-C showerhead (thick edge from 6 April) and CM3's R8 zone 5 tune (thin edge from 11 May), "
                  "which cancel on DP2B wafers polished on CM3",
            "R5": "polymer from CT-DEEP-07 on ET1B and ET3A, which builds %s times faster per RF second than the "
                  "standard recipes and flakes on the wafers after it" % ("%.2f" % fg["polymer_factor"])}
    fix = {"R2": "P-02A back to its spring setpoint (51.5 Hz); filters and pads on CM1 and CM3 change nothing",
           "R3": "tank T3 back to the spring life: a spike every 6 lots, drain and fill every 12 hours",
           "R4": "SH-300-B on DP2B on 23 November, the day the plan takes CM3 back to R7; CM3 to R7 alone recovers %s good "
                 "die per VX40 wafer, not the %s its thin-edge fails suggest" % (f1(fg["harmonise_alone_vx40"]), f1(fg["harmonise_claimed_vx40"])),
           "R5": "wet-clean ET1B and ET3A every %s wafers at the Q1 mix (before the polymer flakes), not every 2,400"
                 % "{:,}".format(fg["R5_etch"]["interval"])}
    rows = []
    for k, (rid, c) in enumerate(causes):
        rows.append([k + 1, CAUSE_NAME[rid], what[rid], c["VX40"], fix[rid], c["VR90"],
                     {5: TWO if rid == "R4" else ONE}])
    rows.append(["", "not explained by the four (the line's own variation)", "", fg["residual_vx40"], "", ""])
    _sheet(wb, "Causes", ["rank", "cause", "evidence", "good die per VX40 wafer, Jun to Sep 2026", "fix",
                          "VR90 Q1 2027 points added by this fix alone under the ramp plan"], rows, [6, 30, 70, 16, 60, 18],
           [WHOLE, None, None, ONE, None, ONE])
    _sheet(wb, "VR90 Q1 2027", ["VR90, Q1 2027 wafers", "value"], [
        ["sort yield under the ramp plan as filed (per cent)", fg["R7_plan"]["plan"], {1: ONE}],
        ["sort yield with every cause fixed (per cent)", fg["R6_fixed"], {1: ONE}],
        ["points added by restoring the slurry loop alone", fg["R2_loop"]["VR90"], {1: ONE}],
        ["points added by cleaning ET1B and ET3A every %s wafers alone" % "{:,}".format(fg["R5_etch"]["interval"]),
         fg["R5_etch"]["VR90"], {1: ONE}],
        ["points added by the spring chemical life alone", fg["R3_bath"]["VR90"], {1: ONE}],
        ["points added by SH-300-B on DP2B alone (CM3 already on R7 under the plan)", fg["R4_edge"]["VR90"], {1: TWO}],
        ["random-defect yield at VR90's 320.32 mm² die, read in blocks of die (per cent)", fg["vr90_random_yield_pct"], {1: ONE}],
        ["gross die per wafer", fg["vr90_gross"], {1: WHOLE}],
        ["wafer starts for 412,000 units with every cause fixed", fg["R7_plan"]["starts"], {1: COUNT}],
        ["wafer starts for 412,000 units under the ramp plan as filed", fg["vr90_starts_plan"], {1: COUNT}],
    ], [70, 12])
    _sheet(wb, "Loop by polisher", ["polisher", "distance along SDS-OX1 (m)",
                                    "bin 5 die per VX40 wafer polished at 51.5 Hz (before 2 June)",
                                    "polished at 38 Hz (from 2 June, standby fortnight aside)",
                                    "polished on the standby pump (10 to 24 August)",
                                    "polished at 38 Hz, counted on die not already failed at bins 3 and 4"],
           [[t, fg["taps_m"][t], fg["bin5_by_polisher"][t]["spring"], fg["bin5_by_polisher"][t]["slow"],
             fg["bin5_by_polisher"][t]["standby"], fg["bin5_at_risk"][t]["slow"]] for t in ("CM2", "CM4", "CM1", "CM3")],
           [10, 16, 18, 14, 14, 24], [None, WHOLE, ONE, ONE, ONE, ONE])
    _sheet(wb, "Routes", ["reading", "VR90 under the plan (per cent)", "VR90 with every cause fixed (per cent)",
                          "changes it calls for"],
           [[ROUTE_NAME.get(r["name"], r["name"]), r["answer"][0], r["answer"][1],
             ", ".join(CHANGE_NAME.get(x, x) for x in r["answer"][2]) if r["answer"][2] else "none"]
            for r in fg["routes"]], [62, 14, 14, 60], [None, ONE, ONE, None])
    ws = _sheet(wb, "Notes", ["note"], [
        ["Records as pulled on 6 November 2026: the Fab 2 yield database, the MES lot history, the tool, bench and "
         "facility exports and the lab's results."],
        ["A wafer counts once, at its final sort insertion; the two windows are by the sort's end time."],
        ["Good die per wafer are means over the wafers sorted in each window; VR90 yields are per cent of its %s gross "
         "die, and points are percentage points of that yield." % fg["vr90_gross"]],
        ["Wafer starts carry the back-end yields the ramp plan takes from the OSAT agreement."],
        ["Yields, points and die per wafer to one decimal, the DP2B showerhead's VR90 points to two because they are "
         "under one point; wafer starts whole."],
    ], [110])
    for row in ws.iter_rows(min_row=2):
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")
    wb.save(path)
    PP.normalize_ooxml(path, AUTHOR, AUTHOR, STAMPS[BOOK][0], STAMPS[BOOK][1], excel=True, company=FIRM)


def write_note(path, fg):
    d = Document()
    st = d.styles["Normal"]
    st.font.name, st.font.size = "Calibri", Pt(10.5)
    d.add_heading("VR90 Q1 2027: four changes take sort yield from %s to %s per cent"
                  % (fg["R7_plan"]["plan"], fg["R6_fixed"]), level=1)
    p = d.add_paragraph()
    p.add_run("For the VR90 ramp readiness review, 24 November 2026. Gitte Ullrich, yield engineering. Records as pulled "
              "on 6 November 2026.").italic = True
    d.add_paragraph(
        "Under the ramp plan as filed, VR90 would sort at %s per cent in Q1 2027. With four changes before the first "
        "lots reach the affected steps it sorts at %s per cent, and the 412,000-unit commitment needs %s wafer starts "
        "instead of %s." % (fg["R7_plan"]["plan"], fg["R6_fixed"], "{:,}".format(fg["R7_plan"]["starts"]),
                            "{:,}".format(fg["vr90_starts_plan"])))
    d.add_heading("What drove June to September", level=2)
    d.add_paragraph(
        "VX40 lost %s good die a wafer against January to March and VP12 %s. On VX40 the loss splits into the "
        "DP2B and CM3 edge pair (%s), the oxide slurry loop (%s), the pre-gate bench's chemical life (%s) and the contact "
        "etch's polymer on ET1B and ET3A (%s), with %s left to the line's own variation."
        % (fg["R1_shortfall"]["VX40"], fg["R1_shortfall"]["VP12"], fg["R4_edge"]["VX40"], fg["R2_loop"]["VX40"],
           fg["R3_bath"]["VX40"], fg["R5_etch"]["VX40"], fg["residual_vx40"]))
    for t in (
        "The scratch loss is the loop's, not the polishers': it rises with each tap's distance along SDS-OX1 (between "
        "wafers polished before 2 June and at 38 Hz after it, CM3 at 318 m went from %s to %s bin 5 die a wafer, CM2 at "
        "64 m from %s to %s) and fell back on the standby pump in August." % (fg["bin5_by_polisher"]["CM3"]["spring"], fg["bin5_by_polisher"]["CM3"]["slow"],
                                            fg["bin5_by_polisher"]["CM2"]["spring"], fg["bin5_by_polisher"]["CM2"]["slow"]),
        "DP2B's new showerhead leaves the edge thick and CM3's May tune polishes it thin, so the two cancel on the "
        "DP2B wafers CM3 polishes and fail the rest. Taking CM3 back to R7 alone, as "
        "ECN-2026-0466 plans, recovers %s good die a VX40 wafer, not the %s its thin-edge fails suggest, because those "
        "DP2B wafers then run thick." % (fg["harmonise_alone_vx40"], fg["harmonise_claimed_vx40"]),
        "The bench's metals, rebuilt lot by lot from the controller log and checked on the lab's August and September "
        "samples, run well above the spring level between the 24-hour drain-and-fills, and the plan's 31 lots a day "
        "push them higher still.",
        "Polymer on the two deep-etch chambers builds %s times faster per RF second on CT-DEEP-07, so the 2,400-wafer "
        "counter lets them flake long before the clean." % fg["polymer_factor"]):
        d.add_paragraph(t)
    d.add_heading("VR90 in Q1 2027", level=2)
    d.add_paragraph(
        "VR90's 320 mm² die yields more than a die-area formula says because the line's defects cluster: read in blocks "
        "of VX40 and VP12 die from January to March, its random-defect yield is %s per cent. Fixing each cause alone "
        "under the plan adds: the loop %s points (VR90 polishes on CM1 and CM3, the far taps), the etch cleans %s, the "
        "chemical life %s, the DP2B showerhead %s." % (fg["vr90_random_yield_pct"], fg["R2_loop"]["VR90"],
                                                       fg["R5_etch"]["VR90"], fg["R3_bath"]["VR90"], fg["R4_edge"]["VR90"]))
    d.add_heading("Changes before the ramp", level=2)
    for k, t in enumerate(("Return SDS-OX1's P-02A to 51.5 Hz.",
              "Put tank T3 on WB-1 and WB-2 back to a spike every 6 lots and a drain and fill every 12 hours.",
              "Fit SH-300-B to DP2B on 23 November, the day ECN-2026-0466 takes CM3 back to R7; do not run that ECN on its own.",
              "Wet-clean ET1B and ET3A every %s wafers while VR90 runs on them." % "{:,}".format(fg["R5_etch"]["interval"]))):
        d.add_paragraph("%d. %s" % (k + 1, t))
    d.add_paragraph(
        "Read the first way (the scratches as CM1's and CM3's own filters and pads, the edge as CM3's tune, the etch on "
        "its wafer counter), the same records put VR90 at %s per cent under the plan, and the quarter's starts would be "
        "set too low." % fg["shortcut"]["careful_plan"])
    q = d.add_paragraph()
    r = q.add_run("Good die per wafer are means over each wafer's final sort insertion; VR90 points are percentage points of "
                  "sort yield on its %s gross die." % fg["vr90_gross"])
    r.font.size = Pt(8.5)
    foot = d.sections[0].footer.paragraphs[0]
    foot.text = "Varnholt Halbleiter GmbH, Fab 2 yield engineering | internal"
    for run in foot.runs:
        run.font.size = Pt(8)
    d.save(path)
    PP.normalize_docx(path, AUTHOR, AUTHOR, STAMPS[NOTE][0], STAMPS[NOTE][1], revision=6, total_time=74, seed=9,
                      title="VR90 ramp yield note", company=FIRM)


def write_all(fg, gold):
    write_book(os.path.join(gold, BOOK), fg)
    write_note(os.path.join(gold, NOTE), fg)
