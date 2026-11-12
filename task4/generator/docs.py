"""The documents: Havørn Regional's reliability programme and spares standard, the October 2026 reliability report and
a pool provider's 2027 offer, each a Word document exported to PDF by LibreOffice Writer through the house writer. The
report's figures are read off the shipped records by the same cleaning the analysis uses, so it reproduces from the
pack by its own stated method."""
import datetime as dt
import os
import sys

import numpy as np
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

HERE = os.path.dirname(os.path.abspath(__file__))
WRITERS = os.path.join(os.path.dirname(os.path.dirname(HERE)), ".claude", "skills", "reduce-house-fixes", "scripts", "writers")
sys.path.insert(0, WRITERS)
import officepdf as O  # noqa: E402
import params as P  # noqa: E402

CET = dt.timezone(dt.timedelta(hours=1))
MM = 2.835


def _styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=9.4, leading=13.0, spaceAfter=5)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=13.5, leading=17, spaceAfter=4)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10.2, leading=13.6,
                        spaceBefore=7, spaceAfter=3, keepWithNext=1)
    small = ParagraphStyle("small", parent=body, fontSize=8.0, leading=10.4, textColor=colors.HexColor("#444444"))
    cell = ParagraphStyle("cell", fontName="Helvetica", fontSize=7.8, leading=9.4)
    return body, h1, h2, small, cell


def _grid(rows, widths, cell):
    t = Table([[Paragraph(str(c), cell) for c in r] for r in rows], colWidths=[w * MM for w in widths], repeatRows=1)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA0AB")), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


STANDARD = [
    ("1. Scope", [
        "This standard sets how Havørn Regional's continuing airworthiness organisation reports the reliability of the "
        "repairable components it pools (rotables) and how the rotable pool is planned. It applies to every pooled "
        "part number on the DHC-8-315 fleet."]),
    ("2. Terms", [
        "2.1 An unscheduled removal is a removal of a unit for a suspected or confirmed defect, recorded in the "
        "maintenance system with reason UNSCH (U before 6 May 2024), whatever the shop or repairer later finds. A "
        "removal for scheduled maintenance or a modification (SCHED, formerly S) and a removal for fitment to another "
        "aircraft (CONV, formerly C) are not unscheduled removals.",
        "2.2 A unit found serviceable by the shop or the repairer is recorded as no fault found.",
        "2.3 A part number's pool is its units beyond those installed on the fleet: serviceable units in Bodø main "
        "stores or a station kit, unserviceable units at the Bodø component shop or a repairer, and new units on "
        "order. The pool's size is its spares.",
        "2.4 A unit's turnaround runs from its removal to its return to serviceable stock."]),
    ("3. Reliability reporting", [
        "3.1 The reliability report is issued monthly for the twelve months to the end of the report month.",
        "3.2 A part number's mean time between unscheduled removals is the flight hours its installed positions flew "
        "in the twelve months divided by its unscheduled removals in the same twelve months.",
        "3.3 The watch list holds every serial with three or more unscheduled removals in the twelve months to the "
        "end of the report month."]),
    ("4. Spares planning", [
        "4.1 Each part number's spares for the coming calendar year are set in the December plan, for the units in "
        "service at the plan date under the flying programme issued for that year.",
        "4.2 A part number's fill rate over a year is the share of its unscheduled removals in that year for which a "
        "serviceable unit was held in the pool, in Bodø main stores or a station kit, when the unit was removed.",
        "4.3 A part number holds the fewest spares that give an expected fill rate over the year of at least 95 per "
        "cent, with the year's unscheduled removals at their expected rate.",
        "4.4 The plan states each part number's expected unscheduled removals in the year with an 80 per cent range: "
        "the 10th to the 90th percentile of the year's removals, carrying both the year's chance variation and the "
        "uncertainty in the expected rate itself."]),
    ("5. Withdrawal of serials", [
        "5.1 A serial is withdrawn and replaced by a new unit when its position would see at least 1.5 more "
        "unscheduled removals over a year with the serial kept in service than with a new unit fitted in its place.",
        "5.2 The removals a withdrawal saves are counted for the position over the year: while a serial is away for "
        "repair its position carries another unit."]),
    ("6. Responsibilities", [
        "6.1 The reliability engineer issues the monthly report and the watch list. The rotables and stores "
        "controller keeps the pool records. The technical director approves the December plan and every withdrawal."]),
]


def standard(path):
    body, h1, h2, small, cell = _styles()
    s = [Paragraph("%s, continuing airworthiness" % P.ORG, small),
         Paragraph("Reliability programme and rotable spares standard", h1),
         Paragraph("CAME part 1.10, issue 6, approved by the technical director 2 September 2026. Replaces issue 5 "
                   "(March 2024). Owner: the reliability engineer.", small), Spacer(1, 4)]
    for head, paras in STANDARD:
        s.append(Paragraph(head, h2))
        for t in paras:
            s.append(Paragraph(t, body))
    s.append(Paragraph("Revisions", h2))
    s.append(_grid([["Issue", "Date", "Change"],
                    ["4", "January 2023", "monthly reporting; the watch list at three removals in twelve months"],
                    ["5", "March 2024", "2.1 reason codes after the maintenance system upgrade; 2.3 station kits"],
                    ["6", "September 2026", "4.2 to 4.4 restated for the December plan; 5.1 and 5.2 added"]],
                   [16, 30, 126], cell))
    O.build(path, s, "Reliability programme and rotable spares standard, issue 6", P.PEOPLE["reliability"],
            "%s continuing airworthiness" % P.ORG, "%s. Reliability programme and rotable spares standard, issue 6." % P.ORG,
            dt.datetime(2026, 9, 2, 10, 14, tzinfo=dt.timezone(dt.timedelta(hours=2))),
            dt.datetime(2026, 9, 2, 10, 41, tzinfo=dt.timezone(dt.timedelta(hours=2))), producer="LibreOffice 7.6")


def report_figures(F):
    """The October report's figures, read off the shipped records: each part number's twelve months of unscheduled
    removals, its installed positions' flight hours, the mean time between them, the share found serviceable, the 2027
    outlook at that rate on the programme's planned flight hours, and the watch list."""
    import analysis as A
    R = F["removals"]
    U = R[(R["reason"] == "UNSCH") & (R["date"] >= A.Y26[0]) & (R["date"] <= A.Y26[1])]
    D = F["day"]
    fh12 = float(D[(D["date"] >= A.Y26[0]) & (D["date"] <= A.Y26[1])]["fh"].sum())
    cyc12 = int(D[(D["date"] >= A.Y26[0]) & (D["date"] <= A.Y26[1])]["cyc"].sum())
    X = A.expo_2027(F)
    fh27 = float(X["fh"].sum())
    rows = []
    for p in P.PARTS:
        k = p["k"]
        u = U[U["k"] == k]
        n = len(u)
        pos_fh = fh12 * p["pos"]
        found = u[u["finding"] != ""]
        nff = float((found["finding"] == "NFF").mean() * 100) if len(found) else 0.0
        rows.append({"k": k, "pn": p["pn"], "name": p["name"], "qpa": p["pos"], "pool": P.POOL[k], "n12": n,
                     "mtbur": pos_fh / n if n else float("nan"), "nff": nff,
                     "proj": n * fh27 / fh12 if fh12 else 0.0})
    L = A.listed(F)
    wl = []
    for sn, r in L.iterrows():
        u = U[U["serial_off"] == sn]
        wl.append({"serial": sn, "k": r["k"], "pn": P.PART[r["k"]]["pn"], "name": P.PART[r["k"]]["name"],
                   "n12": int(r["n"]), "last": u["date"].max().date(), "aircraft": ", ".join(sorted(u["aircraft"].unique()))})
    months = []
    for m in pd.period_range("2025-11", "2026-10", freq="M"):
        g = D[D["date"].dt.to_period("M") == m]
        months.append((m.strftime("%b %Y"), float(g["fh"].sum()), int(g["cyc"].sum())))
    return {"rows": rows, "watch": wl, "fh12": fh12, "cyc12": cyc12, "fh27": fh27, "months": months}


def report(path, F):
    body, h1, h2, small, cell = _styles()
    R = report_figures(F)
    s = [Paragraph("%s, continuing airworthiness" % P.ORG, small),
         Paragraph("Reliability report, October 2026", h1),
         Paragraph("Rotables on the DHC-8-315 fleet, twelve months to 31 October 2026. Issued 9 November 2026 by the "
                   "reliability engineer.", small), Spacer(1, 4),
         Paragraph("1. Fleet utilisation", h2),
         Paragraph("The fleet flew %s flight hours and %s cycles in the twelve months." %
                   ("{:,.0f}".format(R["fh12"]), "{:,}".format(R["cyc12"])), body)]
    s.append(_grid([["Month", "Flight hours", "Cycles"]] +
                   [[m, "{:,.0f}".format(fh), "{:,}".format(c)] for m, fh, c in R["months"]], [30, 30, 30], cell))
    s.append(Paragraph("2. Rotable reliability", h2))
    s.append(Paragraph("Mean time between unscheduled removals is the installed positions' flight hours over the "
                       "unscheduled removals (standard 3.2). No fault found is the share of the removals the shop or "
                       "repairer has reported on.", body))
    rows = [["Part number", "Description", "QPA", "Pool", "Unscheduled removals", "MTBUR (FH)", "No fault found"]]
    for r in R["rows"]:
        rows.append([r["pn"], r["name"], r["qpa"], r["pool"], r["n12"], "{:,.0f}".format(r["mtbur"]), "%.0f%%" % r["nff"]])
    s.append(_grid(rows, [22, 50, 10, 11, 24, 20, 20], cell))
    s.append(Paragraph("3. Watch list", h2))
    s.append(Paragraph("Serials with three or more unscheduled removals in the twelve months (standard 3.3). "
                       "Engineering has entered the replacement of the listed serials in the 2027 budget.", body))
    rows = [["Serial", "Part number", "Description", "Removals", "Last removal", "Aircraft"]]
    for w in R["watch"]:
        rows.append([w["serial"], w["pn"], w["name"], w["n12"], w["last"].isoformat(), w["aircraft"]])
    s.append(_grid(rows, [17, 20, 44, 16, 20, 40], cell))
    O.build(path, s, "Reliability report, October 2026", P.PEOPLE["reliability"], "%s continuing airworthiness" % P.ORG,
            "%s. Reliability report, October 2026." % P.ORG,
            dt.datetime(2026, 11, 9, 8, 52, tzinfo=CET), dt.datetime(2026, 11, 9, 9, 37, tzinfo=CET), producer="LibreOffice 7.6")
    return R


def offer(path):
    """A pool provider's 2027 proposal: exchange access per part number at a monthly fee, sent to the technical
    director in October. The spares plan does not read it."""
    body, h1, h2, small, cell = _styles()
    prov = "Nordkapp Component Pool AS"
    s = [Paragraph(prov, small), Paragraph("Pool access proposal for %s, 2027" % P.ORG, h1),
         Paragraph("Reference NCP-2027-114, 21 October 2026. Valid until 31 January 2027.", small), Spacer(1, 4),
         Paragraph("1. Service", h2),
         Paragraph("Access to %s's DHC-8 rotable pool at Bodø and Tromsø: an exchange unit dispatched within 24 hours "
                   "of an unscheduled removal for AOG requests and 72 hours otherwise, the removed unit returned to us "
                   "within 10 days. Units are supplied with an EASA Form 1." % prov, body),
         Paragraph("2. Monthly access fees", h2)]
    rows = [["Part number", "Description", "Monthly fee per aircraft (NOK)", "Exchange fee per unit (NOK)"]]
    rng = np.random.default_rng(P.SEED + 31)
    for p in P.PARTS:
        if p["k"] in ("NWS", "FLA", "HYP"):
            continue
        rows.append([p["pn"], p["name"], "{:,.0f}".format(p["price"] * float(rng.uniform(0.0011, 0.0019))),
                     "{:,.0f}".format(p["price"] * float(rng.uniform(0.09, 0.16)))])
    s.append(_grid(rows, [24, 60, 40, 40], cell))
    s.append(Paragraph("3. Terms", h2))
    s.append(Paragraph("Fees are fixed for 2027 and invoiced monthly in arrears. The agreement runs for three years "
                       "with a twelve-month notice. Units lost or beyond economic repair through misuse are charged at "
                       "list price.", body))
    O.build(path, s, "Pool access proposal 2027", "Jorunn Christensen", prov, "%s, proposal NCP-2027-114." % prov,
            dt.datetime(2026, 10, 21, 14, 3, tzinfo=dt.timezone(dt.timedelta(hours=2))),
            dt.datetime(2026, 10, 21, 14, 25, tzinfo=dt.timezone(dt.timedelta(hours=2))), producer="LibreOffice 7.5")
