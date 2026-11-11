"""task20 documents: Market Risk Control's backtesting standard (MRS-4) and the risk engine's methodology note (Word
documents exported to PDF by LibreOffice Writer), the quarter's official backtest and the weekly stress report (Excel
exports), and the desk's second-half 2025 plan (an Excel workbook)."""
import datetime as dt

import numpy as np
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

import officepdf as O
import world as W

NYT = {"EDT": dt.timezone(dt.timedelta(hours=-4)), "EST": dt.timezone(dt.timedelta(hours=-5))}

F_STANDARD = "MRS-4_VaR_backtesting_and_exception_classification.pdf"
F_METHOD = "ERE_equity_VaR_methodology_note.pdf"
F_PLAN = "SMCF_H2_2025_business_plan.xlsx"
F_BACKTEST = "SMCF_VaR_backtest_2025Q2.xlsx"
F_STRESS = "SMCF_weekly_stress_results_2024-07_2025-06.xlsx"

PLAN_MID = [315, 310, 305, 300, 300, 300]      # USD million gross, July to December 2025
PLAN_SMALL = [190, 220, 250, 280, 300, 300]
PLAN_MONTHS = ["2025-07", "2025-08", "2025-09", "2025-10", "2025-11", "2025-12"]
PLAN_FLOW = [6.1, 5.4, 6.6, 7.0, 6.8, 5.9]     # client flow, USD billion
PLAN_REV = [3.9, 3.5, 4.3, 4.6, 4.5, 3.8]      # revenue, USD million


def _styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=9.4, leading=13.0, spaceAfter=5)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=13.0, leading=16.5, spaceAfter=4)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10.2, leading=13.6,
                        spaceBefore=7, spaceAfter=3, keepWithNext=1)
    small = ParagraphStyle("small", parent=body, fontSize=8.0, leading=10.6, textColor=colors.HexColor("#444444"))
    cell = ParagraphStyle("cell", fontName="Helvetica", fontSize=8.4, leading=10.4)
    return body, h1, h2, small, cell


def _grid(rows, widths, cell):
    t = Table([[Paragraph(str(c), cell) for c in r] for r in rows], colWidths=widths)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA0AB")), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


def standard(path):
    body, h1, h2, small, cell = _styles()
    hist = [["Version", "Effective", "Change"],
            ["3.0", "1 July 2021", "Hypothetical P&L added beside booked P&L; exception headings introduced"],
            ["3.1", "1 January 2023", "Headings taken in order; corrected count reported each quarter"],
            ["3.2", "1 April 2024", "Volatility heading's decay range widened to 0.94 to 0.97; add-on set monthly"]]
    s = [Paragraph("Tarrant Hale Securities LLC, Market Risk Control", small),
         Paragraph("Market Risk Standard MRS-4: VaR backtesting and exception classification", h1),
         Paragraph("Version 3.2, effective 1 April 2024. Owner: Head of Market Risk Control. Approved by the Risk "
                   "Methodology Committee on 21 March 2024.", small),
         Spacer(1, 4),
         Paragraph("1. Purpose and scope", h2),
         Paragraph("This standard sets how Market Risk Control backtests each trading desk's one-day 99 per cent value at "
                   "risk (VaR) against the desk's daily P&L, how each exception is classified in the desk's quarterly "
                   "backtesting report, and when a desk holds a capital add-on for risks its VaR does not capture. It "
                   "applies to every desk whose VaR the firm's equity risk engine (ERE) computes.", body),
         Paragraph("2. Backtesting period", h2),
         Paragraph("The backtesting period is the 250 business days ending on the last business day of the quarter.", body),
         Paragraph("3. Definitions", h2),
         Paragraph("<b>3.1 Booked P&L.</b> The desk's P&L for the business day as recorded in the general ledger for that "
                   "value date, including the day's trades, commissions, fees, valuation reserves and funding, and any "
                   "later posting made for that value date.", body),
         Paragraph("<b>3.2 Hypothetical P&L.</b> The change in value over the business day of the positions the desk held "
                   "at the close of the previous business day, revalued at the day's closing prices and futures settlement "
                   "prices, with no trades of the day and no commissions, fees, reserves or funding. Product Control "
                   "produces it for each desk each business day.", body),
         Paragraph("<b>3.3 Exception.</b> A business day on which the booked P&L or the hypothetical P&L shows a loss "
                   "larger than the VaR reported for that day. A day on which both show one is one exception.", body),
         Paragraph("<b>3.4 VaR reported for a day.</b> The one-day 99 per cent VaR that ERE produced for the desk in its "
                   "run on the evening of the previous business day, as recorded in the ERE run log.", body),
         Paragraph("4. Classification of exceptions", h2),
         Paragraph("Each exception is classified under the first of the following headings, taken in order, that accounts "
                   "for it.", body),
         Paragraph("<b>(a) Other income.</b> The hypothetical P&L shows no exception on the day.", body),
         Paragraph("<b>(b) Inputs.</b> ERE, with its own scenario window, mapping and settings, would have produced a VaR "
                   "covering the hypothetical loss had it been run on the positions the desk held at the close of the "
                   "previous business day.", body),
         Paragraph("<b>(c) Risks not in the model.</b> A VaR computed as ERE computes it on those positions, but with every "
                   "instrument's scenarios taken from its own price history over the scenario window, would have covered "
                   "the hypothetical loss.", body),
         Paragraph("<b>(d) Volatility.</b> The VaR in (c), with its scenarios rescaled by the ratio of the current to the "
                   "then-current exponentially weighted volatility (decay factor between 0.94 and 0.97), would have "
                   "covered the hypothetical loss.", body),
         Paragraph("<b>(e) Model accuracy.</b> None of the above.", body),
         Paragraph("Exceptions under (c), (d) and (e) count against the model.", body),
         Paragraph("5. Corrected count and zone", h2),
         Paragraph("The corrected count is the number of business days in the backtesting period on which the hypothetical "
                   "P&L shows a loss larger than the VaR of a sound model: the VaR in 4(d), on the positions the desk held "
                   "at the close of the previous business day. The desk's zone follows from the count:", body),
         _grid([["Zone", "Count over 250 business days"], ["Green", "0 to 4"], ["Yellow", "5 to 9"],
                ["Red", "10 or more"]], [70, 170], cell),
         Spacer(1, 3),
         Paragraph("6. Add-on for risks not in VaR", h2),
         Paragraph("While ERE maps any of a desk's positions to a proxy, the desk holds a capital add-on. Before each "
                   "calendar month Market Risk Control sets the month's add-on as the VaR in 4(c) on the positions the "
                   "desk plans to hold that month, less ERE's VaR on the same positions and scenario window as ERE will "
                   "report it for the month's first business day (3.4), and not less than zero. The desk's plan sets out "
                   "the positions it plans to hold and the basis on which they are valued.", body),
         Paragraph("7. Quarterly report", h2),
         Paragraph("For each quarter Market Risk Control reports to the desk's supervisor every exception in the "
                   "backtesting period, dated and classified under one heading, with the count under each heading; what "
                   "the review found in ERE's inputs; the corrected count and zone; and the add-on for each of the next "
                   "six months.", body),
         Paragraph("8. Roles", h2),
         Paragraph("Product Control publishes each desk's booked and hypothetical P&L each business day and restates a "
                   "day when a later posting changes it. Market Risk Control runs the quarterly backtest within five "
                   "business days of the quarter end and classifies the exceptions. Risk Methodology owns ERE, its "
                   "mapping and this standard's counterfactual models. The desk head attests to the quarterly report.", body),
         Paragraph("9. Escalation", h2),
         Paragraph("A desk in the yellow zone on the corrected count is reviewed with Risk Methodology within 20 business "
                   "days. A desk in the red zone on either count is reported to the Chief Risk Officer and the supervisor, "
                   "with a remediation plan and the add-on schedule, within 30 business days of the quarter end.", body),
         Paragraph("10. Records", h2),
         Paragraph("Market Risk Control keeps the run log, the position extracts and snapshots ERE read, the mapping "
                   "vintages, the P&L series and each quarter's classification for seven years.", body),
         Paragraph("11. Document history", h2),
         _grid(hist, [44, 70, 330], cell),
         Spacer(1, 6),
         Paragraph("Market Risk Control, 7 Hanover Square, New York. Internal.", small)]
    O.build(path, s, "MRS-4 VaR backtesting and exception classification", "Market Risk Control",
            "Market Risk Standard MRS-4 v3.2", "Tarrant Hale Securities LLC  |  MRS-4 v3.2  |  Internal",
            dt.datetime(2024, 3, 21, 16, 42, 10, tzinfo=NYT["EDT"]), dt.datetime(2024, 3, 22, 9, 5, 33, tzinfo=NYT["EDT"]),
            producer="LibreOffice 7.6")


def method_note(path):
    body, h1, h2, small, cell = _styles()
    s = [Paragraph("Tarrant Hale Securities LLC, Risk Methodology", small),
         Paragraph("ERE equity VaR: methodology note", h1),
         Paragraph("Version 2.4, March 2024. Owner: Risk Methodology. Applies to the cash equity and equity index futures "
                   "desks.", small),
         Spacer(1, 4),
         Paragraph("1. What ERE produces", h2),
         Paragraph("ERE produces each desk's one-day 99 per cent value at risk each business day by historical simulation. "
                   "The figure is the desk's VaR of record for limits, capital and backtesting.", body),
         Paragraph("2. The nightly run", h2),
         Paragraph("ERE runs for each desk after the US close, scheduled for 18:30 New York time. It reads the desk's "
                   "cash equity positions from the EQX position extract and its futures from the FUTS position snapshot, "
                   "the vendor's closing prices for the day, the CME settlement prices and the proxy mapping. If an extract "
                   "has not arrived by 18:45, the run uses the last one it received and records a warning. Each run is "
                   "recorded in the ERE run log with the extracts it read, the positions and gross exposure it valued and "
                   "the VaR it produced.", body),
         Paragraph("3. Scenarios", h2),
         Paragraph("The scenario window is the 500 business days ending on the run date. Each scenario applies one day's "
                   "returns to the desk's positions. An equity's scenario P&L is its market value at the run date's vendor "
                   "close times its return on that day. A future's scenario P&L is its notional (contracts times "
                   "multiplier times the run date's settlement price; 50 for E-mini S&P 500, 20 for E-mini Nasdaq-100) "
                   "times the return of its index on that day: the S&P 500 for E-mini S&P 500 and the Nasdaq-100 for "
                   "E-mini Nasdaq-100. Scenarios are equally weighted. The VaR is the fifth-largest loss of the 500 "
                   "scenario P&Ls.", body),
         Paragraph("4. The risk store and proxies", h2),
         Paragraph("ERE takes an equity's returns from its series in the risk store, which holds the vendor's closes for "
                   "every instrument from its store start date, the date the desk began trading it (shown in the "
                   "mapping). An equity is scenarioed on its own returns in any run for which the store holds 500 or more of its "
                   "daily returns (its returns from the day after its store start date to the run date). Until then ERE "
                   "maps it to a proxy: its return in each scenario is its beta times the return of its proxy index, the "
                   "Nasdaq-100 for Technology and Communication Services names and the S&P 500 for all others. The "
                   "mapping's series column shows each name's state on the vintage date.", body),
         Paragraph("5. Betas", h2),
         Paragraph("Betas are re-estimated on the first business day of each quarter for every instrument, by ordinary "
                   "least squares of its daily returns on its proxy index's daily returns over the 250 business days "
                   "before the quarter starts, from the vendor's closes, and rounded to three decimals. They apply to every "
                   "run from that day until the next quarter's estimate and are published as the quarter's mapping "
                   "vintage. The desks' futures hedges use the same betas.", body),
         Paragraph("6. Data controls", h2),
         Paragraph("The run checks that the vendor's close file holds every instrument the desk holds; if it does not, the "
                   "run aborts and is re-run once the file is complete, on the extracts the first attempt read. Mapping "
                   "vintages are published within two business days of the quarter start. Changes to an instrument's "
                   "identifiers in EQX are carried through the EQX crosswalk.", body),
         Paragraph("7. Known limitations", h2),
         Paragraph("Scenarios are equally weighted over two years and do not respond to the current level of volatility. "
                   "A proxied equity carries only its index's risk in the scenarios. Both are monitored through "
                   "backtesting (MRS-4).", body),
         Paragraph("8. Change log", h2),
         _grid([["Version", "Date", "Change"],
                ["2.2", "September 2022", "Proxy mapping for instruments with a short store history"],
                ["2.3", "June 2023", "Nasdaq-100 proxy for Technology and Communication Services names"],
                ["2.4", "March 2024", "Futures valued at the run date's settlement price; betas published as vintages"]],
               [44, 80, 320], cell),
         Spacer(1, 6),
         Paragraph("Risk Methodology, Tarrant Hale Securities LLC. Internal.", small)]
    O.build(path, s, "ERE equity VaR methodology note", "Risk Methodology", "ERE methodology note v2.4",
            "Tarrant Hale Securities LLC  |  ERE methodology v2.4  |  Internal",
            dt.datetime(2024, 3, 12, 14, 20, 0, tzinfo=NYT["EDT"]), dt.datetime(2024, 3, 14, 10, 48, 21, tzinfo=NYT["EDT"]),
            producer="LibreOffice 7.6")


def _style_sheet(ws, widths=None):
    for c in ws[1]:
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="D9E1F2")
        c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.freeze_panes = "A2"
    for col in ws.columns:
        w = max(len(str(c.value)) if c.value is not None else 0 for c in col)
        ws.column_dimensions[col[0].column_letter].width = (widths or {}).get(col[0].column_letter, min(max(10, w * 1.05), 60))


def plan(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Plan"
    ws.append(["Month", "Mid cap gross (USD m)", "Small cap gross (USD m)", "Total gross (USD m)",
               "Client flow (USD bn)", "Revenue (USD m)"])
    for j, m in enumerate(PLAN_MONTHS):
        ws.append([m, PLAN_MID[j], PLAN_SMALL[j], PLAN_MID[j] + PLAN_SMALL[j], PLAN_FLOW[j], PLAN_REV[j]])
    ws.append(["H2 2025", None, None, None, round(sum(PLAN_FLOW), 1), round(sum(PLAN_REV), 1)])
    _style_sheet(ws)
    b = wb.create_sheet("Basis")
    b.append(["Item", "Basis"])
    rows = [
        ("Desk", "Small and Mid Cap Facilitation (SMCF), cash equities and E-mini index futures"),
        ("Prepared", "24 June 2025, desk head; approved by the Equities Management Committee on 27 June 2025"),
        ("Positions", "Engine book at 30 Jun 2025 (the risk engine's 30 June 2025 run), names held in the same proportions "
                      "within each segment, scaled so that the segment's gross equals the month's target. Segments per the "
                      "instrument master."),
        ("Gross", "Sum of absolute market values at the 30 Jun 2025 vendor close."),
        ("Hedge", "Per desk mandate: ES and NQ (Sep-25) at 86 per cent of beta-weighted net exposure to each index, using "
                  "the engine's betas and index mapping; whole contracts at 30 Jun settles."),
        ("Market data", "Engine's 30 Jun 2025 run: scenario window (the 500 business days to 30 June 2025) and betas "
                        "(Apr-25 vintage)."),
        ("Growth", "Small cap growth comes from the names onboarded since 2023 as their client franchises build; mid cap "
                   "inventory is run down slightly to fund it."),
        ("Limits", "Desk VaR limit USD 3.0 million; gross limit USD 650 million."),
    ]
    for r in rows:
        b.append(list(r))
    _style_sheet(b, {"A": 16, "B": 110})
    for row in b.iter_rows(min_row=2):
        row[1].alignment = Alignment(wrap_text=True, vertical="top")
    c = wb.create_sheet("Calendar")
    c.append(["Business date", "Month"])
    for d in W.FUTURE_DAYS:
        c.append([d.date().isoformat(), d.strftime("%Y-%m")])
    _style_sheet(c)
    wb.save(path)


def backtest(path, w, P):
    wb = Workbook()
    ws = wb.active
    ws.title = "Daily"
    ws.append(["Business date", "Booked P&L (USD)", "VaR reported (USD)", "VaR run date", "Exception", "Exceptions to date"])
    n = 0
    for k in range(w.T):
        d = W.DATES[w.s + k]
        exc = P.booked[k] < -P.rep[k]
        n += int(exc)
        ws.append([d.date().isoformat(), float(P.booked[k]), float(P.rep[k]), W.DATES[w.s - 1 + k].date().isoformat(),
                   "Y" if exc else "", n])
    _style_sheet(ws)
    s = wb.create_sheet("Summary")
    s.append(["Item", "Value"])
    for r in (("Desk", "Small and Mid Cap Facilitation (SMCF)"),
              ("Backtesting period", "250 business days, 1 July 2024 to 30 June 2025"),
              ("P&L backtested", "Booked P&L (general ledger)"),
              ("VaR", "ERE one-day 99%, run of the previous business day"),
              ("Exceptions", n),
              ("Zone", "Red" if n >= 10 else ("Yellow" if n >= 5 else "Green")),
              ("Prepared", "Market Risk Control, 3 July 2025")):
        s.append(list(r))
    _style_sheet(s, {"A": 22, "B": 56})
    wb.save(path)
    return n


def stress(path, w, names, tm):
    """the desk's weekly stress report: Friday's engine book under the desk's standing scenarios"""
    scen = [("Equity crash", -0.12, -0.15, -0.07, -0.05), ("Small cap squeeze", 0.03, 0.03, 0.15, 0.05),
            ("2022 rates shock", -0.043, -0.052, -0.02, -0.01), ("Liquidity drain", -0.02, -0.02, -0.09, -0.04),
            ("Tech rotation", -0.02, -0.06, -0.01, 0.0), ("Relief rally", 0.05, 0.06, 0.08, 0.04)]
    wb = Workbook()
    ws = wb.active
    ws.title = "Weekly"
    ws.append(["Week ending", "Engine run date", "Scenario", "S&P 500 shock", "Nasdaq-100 shock", "Small cap shock",
               "Mid cap shock", "Stress P&L (USD)"])
    small = (w.seg == "SMALL")
    last_of_week = {}
    for k in range(w.T + 1):
        d = tm.run_day[k]
        last_of_week[tuple(d.isocalendar()[:2])] = k
    for k in sorted(last_of_week.values()):
        d = tm.run_day[k]
        friday = d + pd.Timedelta(days=4 - d.weekday())
        if friday > W.WIN_END:
            continue                                            # the week of 30 June is reported on 4 July
        t = w.s - 1 + k
        mv = w.eng_sh[k] * w.PX[t]
        _, b = w.betas_at(t)
        fut_s = sum(n * W.MULT[r] * w.stl[(r, c)][t] for (r, c), n in w.eng_fut[k].items() if r == "ES")
        fut_n = sum(n * W.MULT[r] * w.stl[(r, c)][t] for (r, c), n in w.eng_fut[k].items() if r == "NQ")
        for nm, sx, nx, sm, md in scen:
            idx = np.where(w.tech, nx, sx)
            pnl = float((mv * (b * idx + np.where(small, sm, md))).sum() + fut_s * sx + fut_n * nx)
            ws.append([friday.date().isoformat(), d.date().isoformat(), nm, sx, nx, sm, md, round(pnl)])
    _style_sheet(ws)
    s = wb.create_sheet("Scenarios")
    s.append(["Scenario", "Definition"])
    for r in (("Equity crash", "Broad equity sell-off: indices down, small and mid caps down beyond their betas"),
              ("Small cap squeeze", "Short squeeze in small caps"),
              ("2022 rates shock", "Index moves of 13 September 2022 (CPI release)"),
              ("Liquidity drain", "Small cap liquidity withdrawal, indices little changed"),
              ("Tech rotation", "Rotation out of large cap technology"),
              ("Relief rally", "Broad rebound led by small caps")):
        s.append(list(r))
    _style_sheet(s, {"A": 20, "B": 80})
    wb.save(path)
