"""task20 golden deliverables: Market Risk Control's exception classification workbook and the one-page note to the
supervisor, every figure from figures.json (which analysis.py computed from the cut pack)."""
import datetime as dt

from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference
from openpyxl.styles import Alignment, Font, PatternFill
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

import officepdf as O

XLSX = "exception_classification_2025Q2.xlsx"
NOTE = "backtesting_note_2025Q2.pdf"
EDT = dt.timezone(dt.timedelta(hours=-4))
MONTH = {"2025-07": "July", "2025-08": "August", "2025-09": "September", "2025-10": "October", "2025-11": "November",
         "2025-12": "December"}
LETTER = {1: "(a)", 2: "(b)", 3: "(c)", 4: "(d)", 5: "(e)"}


def nice(iso):
    d = dt.date.fromisoformat(iso)
    return "%d %s %d" % (d.day, d.strftime("%b"), d.year)


def _head(ws, widths):
    for c in ws[1]:
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="DDE4EE")
        c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.freeze_panes = "A2"
    for col, w in widths.items():
        ws.column_dimensions[col].width = w


def workbook(F, R, path):
    wb = Workbook()
    hc = F["heading_counts"]
    s = wb.active
    s.title = "Summary"
    s.append(["%d exceptions in the 250 days to 30 June 2025, %d against the model; a sound model shows %d (%s)"
              % (F["exceptions_total"], F["model_count"], F["sound_count"], F["sound_zone"].lower()), ""])
    rows = [
        ("Exceptions on either P&L (MRS-4 3.3)", F["exceptions_total"]),
        ("  on booked P&L (the official count)", F["official_count"]),
        ("  on hypothetical P&L", F["hyp_count"]),
        ("  on hypothetical P&L only", F["hyp_only"]),
        ("  on booked P&L only", F["booked_only"]),
        ("(a) Other income", hc["income"]),
        ("(b) Inputs", hc["inputs"]),
        ("(c) Risks not in the model", hc["omitted"]),
        ("(d) Volatility", hc["volatility"]),
        ("(e) Model accuracy", hc["sound"]),
        ("Total", sum(hc.values())),
        ("Counted against the model, (c) to (e)", F["model_count"]),
        ("Runs that read an older extract", F["outage_runs"]),
        ("  exceptions they caused", F["outage_caused"]),
        ("Exceptions caused by closing allocations booked after the extract", F["cutoff_caused"]),
        ("Corrected count, sound model (decay 0.94, portfolio scaling)", F["sound_count"]),
        ("  across decay 0.94 to 0.97, portfolio or series scaling", "%d to %d" % tuple(F["sound_family_range"])),
        ("Zone, corrected", F["sound_zone"]),
        ("Zone, official", F["official_zone"]),
    ]
    for r in rows:
        s.append(list(r))
    s.append([])
    s.append(["Add-on for risks not in VaR (USD million)", ""])
    for m, v in zip(F["addon_months"], F["addon_m"]):
        s.append([MONTH[m] + " 2025", v])
    _head(s, {"A": 62, "B": 16})
    for row in s.iter_rows(min_row=len(rows) + 4, max_row=len(rows) + 3 + len(F["addon_m"])):
        row[1].number_format = "0.00"
    e = wb.create_sheet("Exceptions")
    e.append(["Date", "Booked P&L (USD m)", "Hypothetical P&L (USD m)", "VaR reported (USD m)", "ERE run", "Exception on",
              "Heading", "ERE VaR on the book held (USD m)", "Own-history VaR (USD m)", "Volatility-scaled VaR (USD m)",
              "Allocations missing from the run (USD m gross)", "Run read an older extract", "Basis"])
    for r in F["rows"]:
        e.append([r["date"], r["booked"], r["hyp"], r["var"], r["run"], r["on"], LETTER[r["code"]] + " " + r["heading"],
                  r["good"], r["full"], r["sound"], r["late_gross"], "Yes" if r["reused"] else "", basis(r)])
    _head(e, {"A": 12, "B": 11, "C": 13, "D": 11, "E": 12, "F": 12, "G": 26, "H": 14, "I": 12, "J": 13, "K": 14,
              "L": 11, "M": 70})
    for row in e.iter_rows(min_row=2):
        row[12].alignment = Alignment(wrap_text=True, vertical="top")
        for j in (0, 4):
            row[j].value = dt.date.fromisoformat(row[j].value)
            row[j].number_format = "yyyy-mm-dd"
        for j in (1, 2, 3, 7, 8, 9):
            row[j].number_format = "0.00"
        row[10].number_format = "0.0"
    e.auto_filter.ref = "A1:M%d" % (len(F["rows"]) + 1)
    i = wb.create_sheet("Engine inputs")
    i.append(["ERE run", "Extract read", "Older extract", "Allocations booked after the extract (USD m gross)",
              "VaR reported (USD m)", "ERE VaR on the book held (USD m)", "Difference (USD m)"])
    for row in R["input_rows"]:
        i.append(row)
    _head(i, {"A": 12, "B": 22, "C": 10, "D": 18, "E": 12, "F": 14, "G": 12})
    for row in i.iter_rows(min_row=2):
        row[0].value = dt.date.fromisoformat(row[0].value)
        row[0].number_format = "yyyy-mm-dd"
        row[3].number_format = "0.0"
        for j in (4, 5, 6):
            row[j].number_format = "0.00"
    i.auto_filter.ref = "A1:G%d" % (len(R["input_rows"]) + 1)
    a = wb.create_sheet("Add-on")
    a.append(["Month", "Mapping as for", "Mid cap gross (USD m)", "Small cap gross (USD m)", "E-mini S&P 500",
              "E-mini Nasdaq-100", "Names proxied", "Own-history VaR (USD m)", "ERE VaR (USD m)", "Add-on (USD m)"])
    for j, m in enumerate(F["addon_months"]):
        c = F["plan_contracts"][j]
        a.append([MONTH[m] + " 2025", F["addon_run_for"][j], F["plan_mid_m"][j], F["plan_small_m"][j], c["ESU5"], c["NQU5"],
                  F["addon_proxied"][j], F["addon_full_m"][j], F["addon_engine_m"][j], F["addon_m"][j]])
    _head(a, {"A": 15, "B": 13, "C": 11, "D": 11, "E": 10, "F": 11, "G": 9, "H": 13, "I": 11, "J": 10})
    for row in a.iter_rows(min_row=2, max_row=len(F["addon_months"]) + 1):
        row[1].value = dt.date.fromisoformat(row[1].value)
        row[1].number_format = "yyyy-mm-dd"
        for j in (7, 8, 9):
            row[j].number_format = "0.00"
    ch = BarChart()
    ch.type = "col"
    ch.title = "The add-on falls to nil by December as proxied names reach 500 returns"
    ch.y_axis.title = "USD m"
    ch.add_data(Reference(a, min_col=10, min_row=1, max_row=len(F["addon_months"]) + 1), titles_from_data=True)
    ch.set_categories(Reference(a, min_col=1, min_row=2, max_row=len(F["addon_months"]) + 1))
    ch.legend = None
    ch.height, ch.width = 7, 14
    a.add_chart(ch, "B10")
    ro = wb.create_sheet("Routes")
    sc = F["shortcut_counts"]
    ro.append(["Route", "Exceptions", "Against the model", "Inputs", "Caused by reused extracts", "Sound model count",
               "Zone", "Add-on Jul to Dec (USD m)"])
    fmt = lambda v: ", ".join("%.2f" % x for x in v)
    ro.append(["This review", F["exceptions_total"], F["model_count"], hc["inputs"], F["outage_caused"], F["sound_count"],
               F["sound_zone"], fmt(F["addon_m"])])
    ro.append(["Official file (booked P&L only)", F["official_count"], F["official_count"], 0, "", sc["official"],
               "Red", fmt([F["addon_now_m"]] * 6)])
    ro.append(["Extracts taken as the book held, reused nights re-run on that day's extract", F["exceptions_total"],
               F["careful_model_count"], len(F["careful_inputs_dates"]), len(F["careful_inputs_dates"]),
               sc["extract_book"], "Green", ""])
    ro.append(["Book held, proxies kept, volatility-scaled", F["exceptions_total"], "", "", "", sc["noprox"], "Red", ""])
    ro.append(["Book held, own history, no volatility response", F["exceptions_total"], "", "", "", sc["novol"], "Green", ""])
    ro.append(["Plan's ramp on the 30 June mapping", "", "", "", "", "", "", fmt(F["addon_ramp_only_m"])])
    ro.append(["Full plan from July with the store's graduations", "", "", "", "", "", "", fmt(F["addon_grad_only_m"])])
    ro.append(["30 June add-on scaled with the plan's gross", "", "", "", "", "", "", fmt(F["addon_prop_m"])])
    _head(ro, {"A": 62, "B": 11, "C": 11, "D": 8, "E": 12, "F": 11, "G": 8, "H": 34})
    sd = wb.create_sheet("Sound model")
    sd.append(["Date", "Hypothetical P&L (USD m)", "Sound model VaR (USD m)", "Exception"])
    for row in R["sound_rows"]:
        sd.append(row)
    _head(sd, {"A": 12, "B": 14, "C": 14, "D": 10})
    for row in sd.iter_rows(min_row=2):
        row[0].value = dt.date.fromisoformat(row[0].value)
        row[0].number_format = "yyyy-mm-dd"
        row[1].number_format = row[2].number_format = "0.00"
    n = wb.create_sheet("Notes")
    n.append(["Note", ""])
    for r in (("Standard", "MRS-4 v3.2: exceptions on booked or hypothetical P&L (3.3) against the VaR of the previous "
                           "evening's ERE run (3.4), classified under the first of 4(a) to 4(e) that accounts for each."),
              ("Book held", "Each night's EQX and FUTS extract plus the OMS bookings for that trade date or earlier made "
                            "after the extract was cut; the trades rolled forward from the 28 June 2024 extract give the "
                            "same book."),
              ("Volatility", "Sound model and heading (d) at decay 0.94, scenarios rescaled at the portfolio. 14 February and "
                             "28 March 2025 move between (d) and (e) within MRS-4's 0.94 to 0.97; the corrected count stays "
                             "0 to 2."),
              ("Add-on", "MRS-4 6 on the H2 plan's basis: the 30 June 2025 run's positions scaled by segment, the hedge "
                         "re-sized at 86 per cent, the 30 June window and betas; ERE's mapping as it stands for the run "
                         "that sets each month's first VaR; floored at zero."),
              ("Units", "P&L and VaR in USD million to two decimals; allocations in USD million gross to one decimal."),
              ("Prepared", "Market Risk Control, 18 July 2025, on data to 30 June 2025.")):
        n.append(list(r))
    _head(n, {"A": 14, "B": 110})
    for row in n.iter_rows(min_row=2):
        row[1].alignment = Alignment(wrap_text=True, vertical="top")
    wb.save(path)


def basis(r):
    if r["code"] == 1:
        return "Hypothetical P&L shows no exception; fees and same-day trading on the day carry the booked loss"
    if r["code"] == 2:
        return ("The run's extract was cut before USD %.1f m gross of closing allocations were booked; ERE on the book "
                "held gives %.2f against a loss of %.2f" % (r["late_gross"], r["good"], -r["hyp"]))
    if r["code"] == 3:
        extra = "; the run read an older extract, but the book held still exceeds ERE's VaR" if r["reused"] else ""
        return "ERE on the book held gives %.2f; with every name on its own history %.2f covers the loss%s" % (
            r["good"], r["full"], extra)
    if r["code"] == 4:
        return "Own history gives %.2f, short of the loss; volatility-scaled %.2f covers it" % (r["full"], r["sound"])
    return "No counterfactual covers the loss of %.2f (volatility-scaled %.2f)" % (-r["hyp"], r["sound"])


def note(F, path):
    ss = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=ss["Normal"], fontName="Helvetica", fontSize=8.6, leading=11.2, spaceAfter=4)
    h1 = ParagraphStyle("h", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=11.5, leading=14, spaceAfter=3)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=9.2, leading=12, spaceBefore=4,
                        spaceAfter=2)
    cell = ParagraphStyle("c", fontName="Helvetica", fontSize=7.8, leading=9.6)
    small = ParagraphStyle("s", parent=body, fontSize=7.6, leading=9.6, textColor=colors.HexColor("#444444"))
    hc = F["heading_counts"]
    hd = F["heading_dates"]
    cut = ", ".join(nice(x) for x in F["cutoff_dates"])
    tab = [["Heading (MRS-4 4)", "Exceptions", "Dates"],
           ["(a) Other income", hc["income"], ", ".join(nice(x) for x in hd["income"])],
           ["(b) Inputs", hc["inputs"], cut],
           ["(c) Risks not in the model", hc["omitted"], ", ".join(nice(x) for x in hd["omitted"])],
           ["(d) Volatility", hc["volatility"], ", ".join(nice(x) for x in hd["volatility"])],
           ["(e) Model accuracy", hc["sound"], ", ".join(nice(x) for x in hd["sound"])],
           ["Total", F["exceptions_total"], ""]]
    t = Table([[Paragraph(str(c), cell) for c in r] for r in tab], colWidths=[105, 50, 315])
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA0AB")), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    ad = [["Month"] + [MONTH[m][:3] for m in F["addon_months"]],
          ["Add-on (USD m)"] + ["%.2f" % v for v in F["addon_m"]],
          ["Names proxied"] + [str(v) for v in F["addon_proxied"]]]
    t2 = Table([[Paragraph(str(c), cell) for c in r] for r in ad], colWidths=[100] + [61] * 6)
    t2.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA0AB"))]))
    s = [Paragraph("Tarrant Hale Securities LLC, Market Risk Control", small),
         Paragraph("To: Supervisory team, SMCF desk review. From: Nancy Ayala, Head of Market Risk Control. 18 July 2025. "
                   "Subject: SMCF VaR backtesting, 250 business days to 30 June 2025 (MRS-4 section 7).", small),
         Paragraph("%d of the desk's %d exceptions count against the model, and a sound model would have been %s"
                   % (F["model_count"], F["exceptions_total"], F["sound_zone"].lower()), h1),
         Paragraph("The desk's official backtest counted %d exceptions on booked P&L, a red zone. Taking both P&Ls as MRS-4 "
                   "requires, there were %d: %d on hypothetical P&L, %d of them hidden in booked P&L by the day's fees and "
                   "trading, and %d on booked P&L only. %d of the %d count against the model; a sound model would have "
                   "shown %d exceptions over the period (%d to %d across the volatility settings MRS-4 allows), which is "
                   "the %s zone."
                   % (F["official_count"], F["exceptions_total"], F["hyp_count"], F["hyp_only"], F["booked_only"],
                      F["model_count"], F["exceptions_total"], F["sound_count"], F["sound_family_range"][0],
                      F["sound_family_range"][1], F["sound_zone"].lower()), body),
         t,
         Paragraph("Source: product control daily P&L, ERE run log, OMS blotter; ERE re-run by Market Risk Control on the "
                   "book held. 14 February and 28 March 2025 move between (d) and (e) within MRS-4's decay range of 0.94 "
                   "to 0.97; the table uses 0.94.", small),
         Paragraph("ERE's inputs", h2),
         Paragraph("ERE read an older position extract on %d runs, when the extract feed failed. Two exceptions fall on "
                   "those runs (%s), but neither was caused by the reused extract: ERE run on the book the desk held that "
                   "night still falls short of the loss. The failure that did cause exceptions runs every night: the EQX "
                   "and FUTS extracts are cut as the run starts, around 18:30, and the middle office books the day's "
                   "closing-auction allocations after that, so every run from 1 July 2024 on missed them (median USD %.1f "
                   "million gross a night). The futures hedge on those allocations is booked before the cut, so the gap "
                   "moved ERE's VaR both ways (too high on %d of %d runs) and averages out; on %s it decided the exception, "
                   "since ERE on the book actually held would have covered the loss."
                   % (F["outage_runs"], " and ".join(nice(x) for x in F["outage_exceptions"]),
                      F["late_gross_median_m"], F["late_var_high_runs"], F["late_runs_assessed"], cut), body),
         Paragraph("The model", h2),
         Paragraph("%d exceptions are risks not in the model: ERE maps names with fewer than 500 days in its risk store to "
                   "an index by beta, and on these days the proxied names' own moves made the loss. At 30 June ERE proxied "
                   "%d names, %d per cent of the small cap book. A VaR that also responds to current volatility accounts "
                   "for %d more; %d is left to model accuracy."
                   % (hc["omitted"], F["proxied_30jun"], F["proxied_small_share_pct"], hc["volatility"], hc["sound"]), body),
         Paragraph("Add-on for the second half (MRS-4 6)", h2),
         Paragraph("On the desk's H2 plan, small caps grow from USD %d million in July to %d million and mid caps ease from "
                   "%d million to %d million, on the 30 June window and betas. As names reach 500 days in the store, ERE "
                   "proxies fewer of them each month (%d in July, %d by December), and the add-on falls even as the small "
                   "cap book grows:" % (F["plan_small_m"][0], F["plan_small_m"][-1], F["plan_mid_m"][0], F["plan_mid_m"][-1],
                                         F["addon_proxied"][0], F["addon_proxied"][-1]), body),
         t2,
         Paragraph("Source: SMCF H2 2025 plan; ERE mapping vintages and store start dates; Market Risk Control. Floored at "
                   "zero (MRS-4 6).", small),
         Paragraph("Actions", h2),
         Paragraph("Move ERE's extract after the middle office's allocation batch, or add the evening's post-cut bookings to "
                   "the run, and restate the four input exceptions; fix the EQX/FUTS delivery that failed on %d runs; hold "
                   "the add-on above for the months shown and bring the proxied names onto their own vendor history rather "
                   "than waiting for the store." % F["outage_runs"], body),
         Paragraph("Nancy Ayala, Head of Market Risk Control. Workbook: %s." % XLSX, small)]
    O.build(path, s, "SMCF VaR backtesting note, Q2 2025", "Nancy Ayala", "Exception classification, Q2 2025",
            "Tarrant Hale Securities LLC  |  Market Risk Control  |  Confidential",
            dt.datetime(2025, 7, 18, 9, 41, 0, tzinfo=EDT), dt.datetime(2025, 7, 18, 11, 6, 27, tzinfo=EDT),
            margin_mm=14, top_mm=12, bottom_mm=12, body_pt=8.6)
