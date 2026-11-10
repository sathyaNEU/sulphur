"""task9 documents: the foundation's policy schedule, the master confirmation, the collateral summary, the dealers'
indicative terms, the audited net assets and the three month-end statements. Each is a Word document exported by
LibreOffice Writer through the house writer, with the issuing team as its author and its own issue time."""
import datetime as dt

from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

import officepdf as O
import params as P
import swaps as SW

CDT = dt.timezone(dt.timedelta(hours=-5))
CST = dt.timezone(dt.timedelta(hours=-6))
EDT = dt.timezone(dt.timedelta(hours=-4))
EST = dt.timezone(dt.timedelta(hours=-5))

# ---- the sentences the analysis leans on, kept here once so the checks and the verifier read the same text
D2A = ("A ladder is one swap of a given maturity sold on every monthly sale date at a fixed size. The size of a ladder is "
       "the vega notional of each monthly sale, in U.S. dollars per volatility point, and is set in multiples of USD 100 "
       "a point; a sale may be split between panel dealers.")
D2B = "The monthly sale date is the first exchange business day after the third Friday of the month."
D2C = ("A swap expires on the third Friday of the month that falls its maturity, in months, after the month of its sale, "
       "or on the preceding exchange business day if the exchange is closed that Friday.")
D2D = "Eligible maturities are three, six and twelve months. Swaps are held to expiry."
D3 = ("Swaps are executed under the master confirmation in force with each panel dealer. The volatility strike of a swap "
      "is the closing level, on its sale date, of the Cboe volatility index for its maturity: the Cboe S&amp;P 500 3-Month "
      "Volatility Index, the Cboe S&amp;P 500 6-Month Volatility Index or the Cboe S&amp;P 500 1-Year Volatility Index. Realized "
      "volatility is capped at %.1f times the strike." % SW.CAP)
D4A = ("Settlement. The net amount the Sleeve pays in settlements in any calendar year shall not exceed %.1f percent of "
       "Reference Assets." % P.LIM_SETTLE_PCT)
D4B = ("Collateral. The collateral the Sleeve has posted on any day shall not exceed %.1f percent of Reference Assets."
       % P.LIM_COLL_PCT)
D4C = "Reference Assets are the Foundation's audited net assets at the most recent fiscal year end."
D5A = ("The limits are measured on the record: the published daily closing levels of the S&amp;P 500 Index and of the Cboe "
       "volatility indices from January 2007 through the review date.")
D5B = ("A program is inside the limits if neither would have been exceeded in any calendar year or on any day of the "
       "record had every ladder of the Sleeve been sold at its size on every monthly sale date of the record. A monthly "
       "sale date of the record counts for a ladder whether or not the volatility index for that ladder's maturity was "
       "yet being published on that date.")
D5C = "A swap's settlement amount falls in the calendar year of its expiry."
D5D = ("Collateral on a day is the amount, if any, by which the Sleeve's open swaps taken together are valued against the "
       "Sleeve at that day's close, on the basis the dealers use for their daily valuations.")
D5E = "No discounting is applied."
D7A = ("swaps open at the review date, at the settlement amounts they are expected to pay, as estimated at the review "
       "date;")
D7B = ("swaps not yet sold, at the average settlement amount per sale their ladder shows on the record, taken over the "
       "swaps that would have expired by the review date.")
D7C = ("Where an estimate under this Schedule draws on experience, the experience is that of the whole record and not of "
       "the Sleeve's own years alone.")
D7LEAD = ("The annual cash plan carries, for every ladder of the Sleeve, the settlement amounts of the swaps that expire in "
          "the plan year:")
D7D = ("An average taken from the record is reported with its 80 percent range, being the range within which the average "
       "itself, as distinct from a single settlement, would be expected to lie four times in five.")
D7E = ("The plan for a year is reported with its 80 percent range, being the range within which the year's settlements, "
       "receipts net of payments, would be expected to fall four times in five.")
D8 = ("Each November the investment office and treasury review the program for the coming calendar year on closing "
      "levels through the review date, the second Monday of November. Changes within the eligible maturities and inside "
      "the limits are made jointly by the Chief Investment Officer and the Director of Treasury and reported to the "
      "Investment Committee at its next meeting.")
MC_RV = ("Realized Volatility means 100 multiplied by the square root of (252 divided by N) multiplied by the sum, over "
         "the N Observation Days, of the square of the natural logarithm of (P(i) divided by P(i-1)), where P(i) is the "
         "closing level of the Index on the i-th Observation Day and P(0) is the closing level of the Index on the Trade "
         "Date.")
MC_OBS = ("Observation Day means each day after the Trade Date to and including the Expiration Date on which the Index "
          "Sponsor publishes an official closing level of the Index. N is the number of Observation Days.")
MC_CAP = ("Volatility Cap means %.1f multiplied by the Volatility Strike. Final Realized Volatility is the lesser of "
          "Realized Volatility and the Volatility Cap." % SW.CAP)
MC_UNITS = "Variance Units means the Vega Notional Amount divided by (2 multiplied by the Volatility Strike)."
MC_SETTLE = ("Settlement Amount means Variance Units multiplied by (the square of the Volatility Strike minus the square of "
             "Final Realized Volatility). If positive, the Variance Buyer pays it to the Variance Seller; if negative, the "
             "Variance Seller pays its absolute value to the Variance Buyer.")
CSA_CAP = ("The Exposure of a Transaction against the Foundation shall not exceed the amount the Foundation would pay "
           "were Final Realized Volatility equal to the Volatility Cap.")


def _styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=9.6, leading=13.2, spaceAfter=5)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=13.5, leading=17, spaceAfter=4)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10.4, leading=14, spaceBefore=7,
                        spaceAfter=3, keepWithNext=1)
    small = ParagraphStyle("small", parent=body, fontSize=8.2, leading=10.8, textColor=colors.HexColor("#444444"))
    cell = ParagraphStyle("cell", fontName="Helvetica", fontSize=8.0, leading=9.8)
    return body, h1, h2, small, cell


def _grid(rows, widths, cell):
    t = Table([[Paragraph(str(c), cell) for c in r] for r in rows], colWidths=widths)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA0AB")), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


def usd(v, dp=0):
    return ("{:,.%df}" % dp).format(v)


def policy(path):
    body, h1, h2, small, cell = _styles()
    s = [Paragraph(P.FOUNDATION, small),
         Paragraph("Investment Policy Statement, Schedule D: Volatility Premium Sleeve", h1),
         Paragraph("Adopted by the Board of Directors on May 19, 2021. Amended May 21, 2025 (eligible maturities, D.2; "
                   "cash plan, D.7). This Schedule is part of the Investment Policy Statement and is read with it.", small),
         Spacer(1, 5),
         Paragraph("D.1 Purpose and scope", h2),
         Paragraph("The Sleeve sells variance swaps on the S&amp;P 500 Index to earn the difference between the variance the "
                   "market pays for and the variance the index goes on to realize. It holds no other position. The "
                   "investment office runs the Sleeve; treasury holds its collateral and carries its receipts in the "
                   "Foundation's cash plan.", body),
         Paragraph("D.2 Program", h2),
         Paragraph("(a) " + D2A, body), Paragraph("(b) " + D2B, body), Paragraph("(c) " + D2C, body),
         Paragraph("(d) " + D2D, body),
         Paragraph("D.3 Terms", h2), Paragraph(D3, body),
         Paragraph("D.4 Limits", h2),
         Paragraph("(a) " + D4A, body), Paragraph("(b) " + D4B, body), Paragraph("(c) " + D4C, body),
         Paragraph("D.5 Measuring the limits", h2),
         Paragraph("(a) " + D5A, body), Paragraph("(b) " + D5B, body), Paragraph("(c) " + D5C, body),
         Paragraph("(d) " + D5D, body), Paragraph("(e) " + D5E, body),
         Paragraph("D.6 Collateral arrangements", h2),
         Paragraph("The panel dealers value open swaps daily under the credit support annexes, and treasury posts and "
                   "receives collateral through the custodian accordingly. Interest on cash collateral is not a receipt "
                   "of the Sleeve.", body),
         Paragraph("D.7 Cash plan", h2),
         Paragraph(D7LEAD, body),
         Paragraph("(a) " + D7A, body), Paragraph("(b) " + D7B, body), Paragraph("(c) " + D7C, body),
         Paragraph("(d) " + D7D, body), Paragraph("(e) " + D7E, body),
         Paragraph("D.8 Annual review", h2), Paragraph(D8, body),
         Spacer(1, 8),
         _grid([["Schedule", "D, Volatility Premium Sleeve"], ["Owner", "Investment Committee of the Board of Directors"],
                ["Maintained by", "Investment Office and Treasury"], ["Last amended", "May 21, 2025"],
                ["Next review of this Schedule", "May 2027"]], [130, 330], cell)]
    O.build(path, s, "IPS Schedule D Volatility Premium Sleeve", "Investment Office", "Investment Policy Statement",
            "%s | Investment Policy Statement | Schedule D | amended May 21, 2025" % P.FOUNDATION,
            dt.datetime(2025, 5, 27, 10, 14, tzinfo=CDT), dt.datetime(2025, 5, 27, 10, 31, tzinfo=CDT))


def confirmation(path):
    body, h1, h2, small, cell = _styles()
    rows = [["Term", "Provision"],
            ["Variance Seller", P.FOUNDATION],
            ["Variance Buyer", "The panel dealer named in the Transaction Supplement"],
            ["Index", "S&amp;P 500 Index (SPX); Index Sponsor: S&amp;P Dow Jones Indices LLC"],
            ["Trade Date", "The date of the Transaction Supplement"],
            ["Expiration Date", "As stated in the Transaction Supplement"],
            ["Vega Notional Amount", "As stated in the Transaction Supplement, in USD per volatility point"],
            ["Volatility Strike", "As stated in the Transaction Supplement, being the closing level on the Trade Date of the "
                                  "Cboe volatility index named there"],
            ["Settlement Date", "Two Exchange Business Days after the Expiration Date"],
            ["Calculation Agent", "The Variance Buyer"]]
    s = [Paragraph("Amended and Restated Master Confirmation", h1),
         Paragraph("S&amp;P 500 Index Variance Swap Transactions between %s and each panel dealer. Dated as of March 14, "
                   "2024. Each Transaction is evidenced by a Transaction Supplement and is subject to the ISDA Master "
                   "Agreement between the parties." % P.FOUNDATION, small),
         Spacer(1, 5),
         Paragraph("1. General terms", h2), _grid(rows, [130, 330], cell), Spacer(1, 3), Paragraph(MC_UNITS, body),
         Paragraph("2. Observation", h2), Paragraph(MC_OBS, body),
         Paragraph("A scheduled day on which the Index Sponsor publishes no closing level is not an Observation Day and "
                   "does not postpone the Expiration Date.", body),
         Paragraph("3. Realized volatility", h2), Paragraph(MC_RV, body),
         Paragraph("4. Cap and settlement", h2), Paragraph(MC_CAP, body), Paragraph(MC_SETTLE, body),
         Paragraph("5. Transaction Supplement", h2),
         Paragraph("A Transaction Supplement states the Trade Date, the Expiration Date, the Vega Notional Amount, the "
                   "Volatility Strike and the index it was read from. A dealer may state the Variance Units and the square "
                   "of the Volatility Strike in place of the Vega Notional Amount and the Volatility Strike.", body),
         Paragraph("6. Transfer", h2),
         Paragraph("A Transaction may be transferred by novation to another panel dealer with the consent of the parties; "
                   "its terms are unchanged.", body),
         Spacer(1, 6),
         Paragraph("Executed by the Foundation and by each of Brecon Sound Securities LLC, Altamere Capital Markets and "
                   "Wexcombe Bank, N.A.", small)]
    O.build(path, s, "Amended and Restated Master Confirmation SPX Variance Swaps", "Office of the General Counsel",
            "Variance swap documentation", "%s | Master Confirmation | S&P 500 Variance Swaps | March 14, 2024" % P.FOUNDATION,
            dt.datetime(2024, 3, 14, 15, 22, tzinfo=CDT), dt.datetime(2024, 3, 14, 15, 40, tzinfo=CDT))


def csa(path):
    body, h1, h2, small, cell = _styles()
    rows = [["", "Brecon Sound Securities LLC", "Altamere Capital Markets", "Wexcombe Bank, N.A."],
            ["Annex dated", "June 24, 2021", "June 28, 2021", "July 2, 2021; amended February 9, 2024"],
            ["Valuation Agent", "Dealer", "Dealer", "Dealer"],
            ["Valuation time", "Close of business, New York", "Close of business, New York", "Close of business, New York"],
            ["Threshold", "Zero, both parties", "Zero, both parties", "Zero, both parties"],
            ["Rounding of transfers", "Up to the next USD %s" % usd(P.COLL_ROUND), "Up to the next USD %s" % usd(P.COLL_ROUND),
             "Up to the next USD %s" % usd(P.COLL_ROUND)],
            ["Eligible collateral", "USD cash", "USD cash; U.S. Treasury bills at 99 percent", "USD cash"],
            ["Transfer timing", "Next business day", "Next business day", "Next business day"],
            ["Statement basis", "Vega notional, volatility", "Variance units, variance", "Vega notional, volatility"]]
    s = [Paragraph(P.FOUNDATION + " | Treasury", small),
         Paragraph("Credit support annexes for the Volatility Premium Sleeve: summary of terms", h1),
         Paragraph("Prepared by treasury for the custodian's collateral desk. March 20, 2024. The annexes govern; this "
                   "summary is for operations.", small),
         Spacer(1, 5), _grid(rows, [100, 120, 120, 120], cell), Spacer(1, 6),
         Paragraph("Exposure", h2),
         Paragraph("Under each annex the dealer, as Valuation Agent, determines at each valuation time the amount that "
                   "would be payable to replace each open Transaction at mid-market, and the Exposure is the net of those "
                   "amounts across the dealer's Transactions with the Foundation. " + CSA_CAP, body),
         Paragraph("Transfers", h2),
         Paragraph("When a dealer's Exposure is against the Foundation, the Foundation posts collateral equal to it, "
                   "rounded as in the table; when it is in the Foundation's favor, the dealer posts to the Foundation's "
                   "account at %s. The custodian's ledger records the Foundation's postings dealer by dealer." % P.CUSTODIAN,
                   body),
         Paragraph("Interest", h2),
         Paragraph("Cash collateral earns the effective federal funds rate, settled monthly.", body)]
    O.build(path, s, "Credit support annexes summary Volatility Premium Sleeve", "Treasury", "Collateral operations",
            "%s | Treasury | CSA summary | March 20, 2024" % P.FOUNDATION,
            dt.datetime(2024, 3, 20, 9, 48, tzinfo=CDT), dt.datetime(2024, 3, 20, 10, 6, tzinfo=CDT))


def term_sheet(path, first_sale, first_exp3, first_exp6):
    body, h1, h2, small, cell = _styles()
    rows = [["Term", "3-month ladder", "6-month ladder"],
            ["Product", "S&amp;P 500 Index variance swap, Foundation sells variance", "S&amp;P 500 Index variance swap, Foundation "
                                                                             "sells variance"],
            ["Volatility Strike", "Closing level of the Cboe S&amp;P 500 3-Month Volatility Index on the Trade Date",
             "Closing level of the Cboe S&amp;P 500 6-Month Volatility Index on the Trade Date"],
            ["Volatility Cap", "%.1f times the Volatility Strike" % SW.CAP, "%.1f times the Volatility Strike" % SW.CAP],
            ["Trade Dates", "Each monthly sale date of the Foundation's program", "Each monthly sale date of the Foundation's "
                                                                                   "program"],
            ["First Trade Date", first_sale.strftime("%B %-d, %Y"), first_sale.strftime("%B %-d, %Y")],
            ["First Expiration Date", first_exp3.strftime("%B %-d, %Y"), first_exp6.strftime("%B %-d, %Y")],
            ["Vega Notional Amount", "Quoted for up to USD %s per monthly sale, split across the panel" % usd(P.PROPOSED),
             "Quoted for up to USD %s per monthly sale, split across the panel" % usd(P.PROPOSED)],
            ["Documentation", "Supplement to the Amended and Restated Master Confirmation of March 14, 2024",
             "Supplement to the Amended and Restated Master Confirmation of March 14, 2024"]]
    s = [Paragraph("Brecon Sound Securities LLC | Equity Derivatives", small),
         Paragraph("Indicative terms: 3-month and 6-month S&amp;P 500 variance swap ladders", h1),
         Paragraph("For %s, at the request of its investment office of November 2, 2026, on behalf of the dealer panel "
                   "(Brecon Sound Securities LLC, Altamere Capital Markets, Wexcombe Bank, N.A.). November 4, 2026."
                   % P.FOUNDATION, small),
         Spacer(1, 6), _grid(rows, [100, 180, 180], cell), Spacer(1, 6),
         Paragraph("The panel will paper one ladder. The Foundation is to confirm the maturity and the Vega Notional Amount "
                   "per monthly sale by December 11, 2026, so that the supplement can be signed before the first Trade "
                   "Date. The Foundation's 12-month ladder continues on its present terms.", body),
         Paragraph("Indicative only and subject to documentation and credit approval. Not an offer.", small)]
    O.build(path, s, "Indicative terms 3-month and 6-month SPX variance swap ladders", "Equity Derivatives Sales",
            "Indicative terms", "Brecon Sound Securities | Indicative terms | November 4, 2026 | Confidential",
            dt.datetime(2026, 11, 4, 16, 5, tzinfo=EST), dt.datetime(2026, 11, 4, 16, 19, tzinfo=EST))


def net_assets(path):
    body, h1, h2, small, cell = _styles()
    total = P.REF_ASSETS / 1e6
    # the classes as the audited statements show them, this year and last (authored; only the total is used)
    parts = [("Public equity", 0.412, 571.3), ("Private equity and venture capital", 0.213, 288.9), ("Fixed income and cash", 0.148, 214.6),
             ("Real assets", 0.117, 160.2), ("Absolute return", 0.094, 131.8)]
    rows = [["", "June 30, 2026", "June 30, 2025"]]
    left, prior = total, 0.0
    for name, share, last in parts:
        v = round(total * share, 1)
        left -= v
        prior += last
        rows.append([name, usd(v, 1), usd(last, 1)])
    rows.append(["Other assets, net of liabilities", usd(left, 1), usd(21.7, 1)])
    rows.append(["Net assets", usd(total, 1), usd(prior + 21.7, 1)])
    s = [Paragraph(P.FOUNDATION, small),
         Paragraph("Statement of net assets (audited), fiscal year ended June 30, 2026", h1),
         Paragraph("Extract from the audited financial statements approved by the Board of Directors on September 24, "
                   "2026. Amounts in millions of U.S. dollars.", small),
         Spacer(1, 6), _grid(rows, [200, 120, 120], cell), Spacer(1, 6),
         Paragraph("Derivative positions of the Volatility Premium Sleeve are carried at the dealers' valuations within "
                   "Other assets, net of liabilities. Collateral posted or received is shown gross in the notes.", body),
         Paragraph("The accompanying notes are an integral part of the financial statements.", small)]
    O.build(path, s, "Statement of net assets FY2026", "Finance", "Audited financial statements, extract",
            "%s | Statement of net assets | June 30, 2026" % P.FOUNDATION,
            dt.datetime(2026, 9, 24, 14, 12, tzinfo=CDT), dt.datetime(2026, 9, 24, 14, 27, tzinfo=CDT))


STATEMENT_TIME = {"BSS": dt.datetime(2026, 11, 2, 6, 31, tzinfo=EST), "ACM": dt.datetime(2026, 11, 2, 7, 2, tzinfo=CST),
                  "WXB": dt.datetime(2026, 11, 3, 8, 15, tzinfo=EST)}


def statement(path, dealer, lines, posted):
    """A dealer's month-end statement of open transactions. `lines` is the dealer's valuation rows at the statement date."""
    body, h1, h2, small, cell = _styles()
    info = P.DEALERS[dealer]
    fmt = info["datefmt"]
    variance = info["basis"] == "VARIANCE"
    if variance:
        head = ["Reference", "Trade date", "Expiration", "Variance units", "Variance strike", "Days elapsed / total",
                "Realized variance to date", "Implied variance to expiration", "Value (USD)"]
    else:
        head = ["Reference", "Trade date", "Expiration", "Vega notional (USD)", "Volatility strike", "Days elapsed / total",
                "Realized volatility to date", "Implied volatility to expiration", "Value (USD)"]
    rows = [head]
    total = 0.0
    for r in lines.itertuples():
        total += r.mtm
        if variance:
            rows.append([r.dealer_ref, r.sale.strftime(fmt), r.expiry.strftime(fmt), usd(r.vega / (2 * r.k), 2), "%.4f" % (r.k * r.k),
                         "%d / %d" % (r.n_e, r.n_e + r.n_r), "%.2f" % r.realized, "%.2f" % r.implied, usd(r.mtm)])
        else:
            rows.append([r.dealer_ref, r.sale.strftime(fmt), r.expiry.strftime(fmt), usd(r.vega), "%.2f" % r.k,
                         "%d / %d" % (r.n_e, r.n_e + r.n_r), "%.4f" % r.realized, "%.2f" % r.implied, usd(r.mtm)])
    rows.append(["Total", "", "", "", "", "", "", "", usd(total)])
    w = [84, 50, 50, 50, 46, 56, 50, 52, 50]
    s = [Paragraph(info["name"], h2), Paragraph("Equity derivatives client valuations, %s" % info["city"], small),
         Spacer(1, 4),
         Paragraph("Statement of open transactions as of %s" % P.STATEMENT.strftime("%B %-d, %Y"), h1),
         Paragraph("Counterparty: %s. Product: S&amp;P 500 Index variance swaps, counterparty sells variance. Values are "
                   "mid-market at the close of business in New York; a positive value is in the counterparty's favor."
                   % P.FOUNDATION, small),
         Spacer(1, 5), _grid(rows, w, cell), Spacer(1, 5),
         Paragraph("Collateral posted by the counterparty at the statement date: USD %s." % usd(posted), body),
         Paragraph("This statement is provided for information and does not replace the Transaction Supplements. "
                   "Please report any difference within ten business days.", small)]
    when = STATEMENT_TIME[dealer]
    O.build(path, s, "Statement of open transactions %s" % P.STATEMENT.strftime("%Y-%m-%d"), "Client Valuations",
            "Month-end valuation statement", "%s | Statement as of %s | %s" % (info["short"], P.STATEMENT.strftime("%B %-d, %Y"), P.FOUNDATION),
            when, when + dt.timedelta(minutes=3), margin_mm=12)
