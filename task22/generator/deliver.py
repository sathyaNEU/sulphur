"""task22 golden deliverables: the engineering division's workbook (each feeder's monthly energy balance, the twelve
months, the line loss bridge, the 2027 connections and 2027 technical losses) and its one-page memo to the utility
director, both from the same results that write figures.json."""
import datetime as dt
import io
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import openpyxl  # noqa: E402
from openpyxl.styles import Alignment, Font  # noqa: E402

import analysis as A  # noqa: E402
import postprocess  # noqa: E402

WORKBOOK = "dpl_feeder_energy_balance_2023-10_2026-09.xlsx"
MEMO = "revenue_protection_2027_memo.pdf"
ORG = "City of Delmont"
AUTHOR = "Dustin Jones"
BLUE, GRAY, INK, INK2 = "#2a78d6", "#b5b4ae", "#0b0b0b", "#52514e"


def _hdr(ws, row, cols, widths=None):
    for j, h in enumerate(cols, 1):
        c = ws.cell(row=row, column=j, value=h)
        c.font = Font(bold=True)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for j, wd in enumerate(widths or [], 1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(j)].width = wd


def r1(x):
    return round(float(x), 1)


MWH, CNT, PCT, PTS = "#,##0.0", "#,##0", "0.00", "+0.00;-0.00;0.00"


def _fmt(ws, cols, r0, r1_, fmt):
    for col in cols:
        for r in range(r0, r1_ + 1):
            ws["%s%d" % (col, r)].number_format = fmt


def write(F, G, mon, gold_dir):
    os.makedirs(gold_dir, exist_ok=True)
    b = G["_balance"]
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Monthly balance"
    ws["A1"] = "Feeder energy balance by month, MWh (October 2023 to September 2026)"
    ws["A1"].font = Font(bold=True, size=12)
    cols = ["Month", "Feeder", "Customers at month end", "Energy in at breaker", "Received from customers' generation",
            "Delivered through customers' meters", "Large power meters", "City street and area lights",
            "Technical losses", "Non-technical loss"]
    _hdr(ws, 3, cols, [9, 8, 11, 12, 14, 14, 12, 12, 11, 12])
    r = 4
    for m in mon:
        ws.append if False else None
        vals = [m["month"], m["feeder"], m["customers"], r1(m["e_in"]), r1(m["rcv"]), r1(m["dlv"]), r1(m["lp"]),
                r1(m["lights"]), r1(m["tech"]), r1(m["ntl"])]
        for j, v in enumerate(vals, 1):
            ws.cell(row=r, column=j, value=v)
        r += 1
    _fmt(ws, "C", 4, r - 1, CNT)
    _fmt(ws, "DEFGHIJ", 4, r - 1, MWH)
    ws.freeze_panes = "C4"
    ws.auto_filter.ref = "A3:J%d" % (r - 1)
    ws.print_title_rows = "3:3"
    # twelve months
    ws = wb.create_sheet("Twelve months")
    ws["A1"] = "Twelve months to September 2026, MWh"
    ws["A1"].font = Font(bold=True, size=12)
    cols = ["Feeder", "Energy in at breaker", "Received from customers' generation", "Delivered through customers' meters",
            "Large power meters", "City lights", "Primary conductors", "Transformer core", "Transformer load",
            "Secondary and service", "Technical losses", "Non-technical loss", "Rank"]
    _hdr(ws, 3, cols, [8, 12, 14, 14, 12, 10, 11, 11, 11, 11, 11, 12, 6])
    order = sorted(A.FEEDERS, key=lambda f: -b[f]["ntl"])
    rank = {f: i + 1 for i, f in enumerate(order)}
    r = 4
    for f in A.FEEDERS:
        x = b[f]
        vals = [f, r1(x["e_in"] / 1000), r1(x["rcv"] / 1000), r1(x["dlv"] / 1000), r1(x["lp"] / 1000),
                r1(x["lights"] / 1000), r1(x["prim"] / 1000), r1(x["nl"] / 1000), r1(x["cu"] / 1000),
                r1(x["sec"] / 1000), r1(x["tech"] / 1000), r1(x["ntl"] / 1000), rank[f]]
        for j, v in enumerate(vals, 1):
            ws.cell(row=r, column=j, value=v)
        r += 1
    tot = {k: sum(b[f][k] for f in A.FEEDERS) / 1000 for k in ("e_in", "rcv", "dlv", "lp", "lights", "prim", "nl",
                                                                 "cu", "sec", "tech", "ntl")}
    vals = ["Total", r1(tot["e_in"]), r1(tot["rcv"]), r1(tot["dlv"]), r1(tot["lp"]), r1(tot["lights"]),
            r1(tot["prim"]), r1(tot["nl"]), r1(tot["cu"]), r1(tot["sec"]), r1(tot["tech"]), r1(tot["ntl"]), ""]
    for j, v in enumerate(vals, 1):
        ws.cell(row=r, column=j, value=v).font = Font(bold=True)
    _fmt(ws, "BCDEFGHIJKL", 4, r, MWH)
    ws.freeze_panes = "B4"
    r += 2
    ws.cell(row=r, column=1, value="Substations: purchases at the delivery points less the feeders' energy in "
                                   "(substation transformer losses and station service), MWh").font = Font(italic=True)
    r += 1
    ws.cell(row=r, column=1, value="Purchases")
    ws.cell(row=r, column=2, value=r1(G["purchases_26"]))
    ws.cell(row=r + 1, column=1, value="Substations")
    ws.cell(row=r + 1, column=2, value=r1(G["substation_26"]))
    ws.cell(row=r + 2, column=1, value="Lights billed at deemed kWh")
    ws.cell(row=r + 2, column=2, value=r1(G["lights_deemed_26"]))
    _fmt(ws, "B", r, r + 2, MWH)
    # bridge
    ws = wb.create_sheet("Line loss bridge")
    ws["A1"] = "Line loss, purchases less billed sales over purchases, per cent"
    ws["A1"].font = Font(bold=True, size=12)
    _hdr(ws, 3, ["", "Twelve months to September 2024", "Twelve months to September 2026", "Change, points"],
         [40, 16, 16, 14])
    br = G["bridge"]
    names = [("substation", "Substation transformers and station service"), ("technical", "Technical losses"),
             ("nontechnical", "Non-technical losses"), ("lights", "Lights: real use less deemed kWh billed"),
             ("billing", "Metered use not billed in the period")]
    r = 4
    ws.cell(row=r, column=1, value="Line loss").font = Font(bold=True)
    ws.cell(row=r, column=2, value=round(G["loss_pct_24"], 2))
    ws.cell(row=r, column=3, value=round(G["loss_pct_26"], 2))
    ws.cell(row=r, column=4, value=round(G["loss_change"], 2))
    for k, lab in names:
        r += 1
        ws.cell(row=r, column=1, value=lab)
        ws.cell(row=r, column=2, value=round(br["2024"]["parts"][k], 2))
        ws.cell(row=r, column=3, value=round(br["2026"]["parts"][k], 2))
        ws.cell(row=r, column=4, value=round(br["change"][k], 2))
    r += 2
    ws.cell(row=r, column=1, value="Change from technical losses, points")
    ws.cell(row=r, column=4, value=round(G["d_technical"], 2))
    ws.cell(row=r + 1, column=1, value="Change from non-technical losses, points")
    ws.cell(row=r + 1, column=4, value=round(G["d_nontechnical"], 2))
    ws.cell(row=r + 2, column=1, value="Change from everything else, points")
    ws.cell(row=r + 2, column=4, value=round(G["d_other"], 2))
    _fmt(ws, "BC", 4, r - 2, PCT)
    _fmt(ws, "D", 4, r + 2, PTS)
    # 2027
    ws = wb.create_sheet("2027")
    ws["A1"] = "2027: approved large connections and each feeder's technical losses"
    ws["A1"].font = Font(bold=True, size=12)
    _hdr(ws, 3, ["Application", "Applicant", "Feeder", "Applied kW", "Service date", "Peak hourly demand added, kW"],
         [12, 40, 8, 10, 12, 16])
    r = 4
    for rr in F["applications"].itertuples(index=False):
        if rr.Status != "Approved":
            continue
        for j, v in enumerate([rr.AppNo, rr.Applicant, rr.Feeder, float(rr.Connected_kW), rr.ServiceDate,
                               r1(G["new_peaks"][rr.AppNo])], 1):
            ws.cell(row=r, column=j, value=v)
        r += 1
    _fmt(ws, "D", 4, r - 1, CNT)
    _fmt(ws, "F", 4, r - 1, MWH)
    r += 1
    r27 = r + 1
    _hdr(ws, r, ["Feeder", "Energy in, MWh", "Primary conductors", "Transformer core", "Transformer load",
                 "Secondary and service", "Technical losses, MWh"])
    t27 = G["_tech27"]
    for f in A.FEEDERS:
        r += 1
        x = t27[f]
        for j, v in enumerate([f, r1(x["e_in"] / 1000), r1(x["prim"] / 1000), r1(x["nl"] / 1000), r1(x["cu"] / 1000),
                               r1(x["sec"] / 1000), r1(x["tech"] / 1000)], 1):
            ws.cell(row=r, column=j, value=v)
    r += 1
    ws.cell(row=r, column=1, value="Total").font = Font(bold=True)
    ws.cell(row=r, column=7, value=r1(G["tech27_system"])).font = Font(bold=True)
    _fmt(ws, "BCDEFG", r27, r, MWH)
    # sweep
    ws = wb.create_sheet("2027 sweep")
    ws["A1"] = "Revenue protection sweep, 2027: feeders by non-technical loss, twelve months to September 2026"
    ws["A1"].font = Font(bold=True, size=12)
    _hdr(ws, 3, ["Rank", "Feeder", "Non-technical loss, MWh", "Swept in 2027"], [6, 8, 16, 12])
    for i, f in enumerate(order):
        for j, v in enumerate([i + 1, f, r1(b[f]["ntl"] / 1000), "Yes" if i < 4 else ""], 1):
            ws.cell(row=4 + i, column=j, value=v)
    _fmt(ws, "C", 4, 3 + len(order), MWH)
    notes(wb.create_sheet("Notes"))
    path = os.path.join(gold_dir, WORKBOOK)
    wb.save(path)
    postprocess.normalize_ooxml(path, AUTHOR, AUTHOR, "2026-11-09T15:12:00Z", "2026-11-10T22:41:00Z", excel=True,
                                company=ORG)
    memo(G, order, os.path.join(gold_dir, MEMO))
    return path


NOTES = [
    ("Non-technical loss", "As RFP 2026-14 scope A.3 defines it: energy that entered the feeder at its substation "
                           "breaker and from customers' own generation, less what customers' meters recorded, the "
                           "City's unmetered street and area lights, and the feeder's own technical losses."),
    ("Energy in at breaker", "The feeder breakers' hourly metering from the substation historian. Hours the "
                             "telemetry missed, and APT-2's stuck readings of August 18 to 20, 2025, are rebuilt "
                             "from the substation's delivery point purchases less its transformer losses, station "
                             "service and the other feeders' breaker energy."),
    ("Customers at month end", "Service points connected on the last day of the month on nodes the feeder served at "
                               "midnight, with every OMS switching order replayed on the GIS network."),
    ("Customers' meters", "Each read's kWh spread over the days it covers by the substation's daily energy; an "
                          "estimated read is carried into the actual read that trues it up."),
    ("City lights", "Lamps in the lighting inventory at their input watts (engineering tables) and each month's "
                    "burning hours, by conversion date."),
    ("Technical losses", "Primary conductors at 50 C, single-phase taps at six times the three-phase expression, as "
                         "in the 2019 loss evaluation, with each month's metered load at the nodes of the network "
                         "that served it; transformer core and load losses from the asset register by kVA and "
                         "vintage; secondary and service conductors at 0.7 per cent of energy delivered to services."),
    ("Line loss", "Purchases at the delivery points less sales on bills issued in the period (customer bills net of "
                  "energy received from customers, large power bills and the lights' deemed kWh), over purchases; "
                  "the basis of the annual line loss report."),
    ("2027", "The twelve months to September 2026 stand for 2027's months on today's network, with the approved "
             "connections from their service dates at the peak share of applied load that comparable connected "
             "customers draw, and the APT-3 reconductor from March 15, 2027 (FY2027 budget instructions 1 and 2)."),
    ("Sources", "Delivery point interval data and feeder historian to October 31, 2026; CIS meter reads pulled "
                "November 5, 2026; GIS, transformer register and lighting inventory exported October 27, 2026."),
    ("Rounding", "MWh to one decimal and line loss to two; totals and changes from unrounded values."),
]


def notes(ws):
    ws["A1"] = "Notes"
    ws["A1"].font = Font(bold=True, size=12)
    ws.column_dimensions["A"].width = 22
    ws.column_dimensions["B"].width = 100
    for i, (k, v) in enumerate(NOTES):
        ws.cell(row=3 + i, column=1, value=k).font = Font(bold=True)
        c = ws.cell(row=3 + i, column=2, value=v)
        c.alignment = Alignment(wrap_text=True, vertical="top")
        ws.cell(row=3 + i, column=1).alignment = Alignment(vertical="top")


def chart(G, order):
    b = G["_balance"]
    vals = [b[f]["ntl"] / 1000 for f in order][::-1]
    labs = order[::-1]
    fig, ax = plt.subplots(figsize=(6.2, 3.6), dpi=200)
    colors = [BLUE if f in G["sweep"] else GRAY for f in labs]
    ax.barh(labs, vals, color=colors, height=0.62, edgecolor="white", linewidth=1.5)
    for y, v in enumerate(vals):
        ax.text(v + 12, y, "{:,.0f}".format(v), va="center", fontsize=7.5, color=INK2)
    ax.set_xlabel("Non-technical loss, MWh, twelve months to September 2026", fontsize=8, color=INK2)
    ax.tick_params(axis="both", labelsize=7.5, colors=INK2)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.spines["left"].set_color("#d6d5d0")
    ax.spines["bottom"].set_color("#d6d5d0")
    ax.xaxis.grid(True, color="#ecebe7", linewidth=0.6)
    ax.set_axisbelow(True)
    ax.set_xlim(0, max(vals) * 1.15)
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fig)
    buf.seek(0)
    return buf


def memo(G, order, path):
    """The one-page memo to the utility director, written in Word and exported to PDF (officepdf)."""
    import datetime as dt
    import tempfile

    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.platypus import Image, Paragraph, Spacer

    import officepdf
    SS = getSampleStyleSheet()
    BODY = ParagraphStyle("b", parent=SS["BodyText"], fontName="Helvetica", fontSize=10, leading=13, spaceAfter=6)
    HEAD = ParagraphStyle("h", parent=BODY, spaceAfter=0)
    b = G["_balance"]
    s = G["sweep"]
    ntl = {f: b[f]["ntl"] / 1000 for f in A.FEEDERS}
    story = [
        Paragraph("<b>Delmont Power and Light, Engineering</b>", HEAD),
        Paragraph("To: Utility Director", HEAD),
        Paragraph("From: Dustin Jones, Engineering Manager", HEAD),
        Paragraph("Date: November 10, 2026", HEAD),
        Paragraph("<b>Subject: 2027 revenue protection sweep and 2027 technical losses</b>", BODY),
        Paragraph("Sweep %s, %s, %s and %s in 2027. They carried %s, %s, %s and %s MWh of non-technical loss in the "
                  "twelve months to September 2026; the next feeder, %s, carried %s." % (
                      s[0], s[1], s[2], s[3], "{:,.0f}".format(ntl[s[0]]), "{:,.0f}".format(ntl[s[1]]),
                      "{:,.0f}".format(ntl[s[2]]), "{:,.0f}".format(ntl[s[3]]), order[4],
                      "{:,.0f}".format(ntl[order[4]])), BODY),
        Paragraph("APT-3 and NTH-3 look like candidates on a raw residual and are not. APT-3's excess is its own "
                  "network losses: with the cold store and the grow at the end of the feeder its lines and "
                  "transformers lost %s MWh, where the 2019 study's %.2f per cent of its energy gives %s. NTH-3 looks "
                  "high only if every customer is kept on today's feeder; the switching log moved one of its laterals "
                  "to NTH-4 on April 21." % ("{:,.0f}".format(G["tech_apt3_26"]), G["study_apt3_pct"],
                                             "{:,.0f}".format(G["careful_tech_apt3_26"])), BODY),
        Paragraph("CHL-3 belongs on the list even though its breaker metering was down through the January ice "
                  "storm, when it was also carrying CHL-2's customers. Its energy in for the year is %s MWh, rebuilt "
                  "for those hours from the Cherry Hill delivery point." % "{:,.0f}".format(G["e_in_chl3_26"]), BODY),
        Paragraph("Line loss rose from %.2f to %.2f per cent between the twelve months to September 2024 and to "
                  "September 2026. Technical losses account for %.2f points of the rise and non-technical losses for "
                  "%.2f; the lights, billing timing and the substations take %.2f points off." % (
                      G["loss_pct_24"], G["loss_pct_26"], G["d_technical"], G["d_nontechnical"], -G["d_other"]), BODY),
        Paragraph("For the 2027 budget, technical losses come to %s MWh on the fourteen feeders, including %s MWh on "
                  "APT-4 once the Flint Ridge grow connects in May. The three approved connections will add %s, %s "
                  "and %s kW at their peaks, well under what they applied for." % (
                      "{:,.0f}".format(G["tech27_system"]), "{:,.0f}".format(G["tech27_apt4"]),
                      *["{:,.0f}".format(G["new_peaks"][k]) for k in sorted(G["new_peaks"])]), BODY),
    ]
    tmp = tempfile.mkdtemp(prefix="t22memo-")
    png = os.path.join(tmp, "ntl_by_feeder.png")
    open(png, "wb").write(chart(G, order).read())
    story.append(Image(png, width=150 * 72 / 25.4, height=150 * 72 / 25.4 * 3.6 / 6.2))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Non-technical loss by feeder as RFP 2026-14 scope A.3 defines it, the four to sweep in "
                           "blue. Monthly detail in the feeder energy balance workbook.", BODY))
    CST = dt.timezone(dt.timedelta(hours=-6))
    officepdf.build(path, story, "2027 revenue protection sweep", "Delmont Power and Light",
                    "Revenue protection sweep and technical losses, 2027", "Delmont Power and Light  |  Engineering",
                    dt.datetime(2026, 11, 10, 8, 5, tzinfo=CST), dt.datetime(2026, 11, 10, 16, 58, tzinfo=CST),
                    letter=True)
    import shutil
    shutil.rmtree(tmp, ignore_errors=True)
