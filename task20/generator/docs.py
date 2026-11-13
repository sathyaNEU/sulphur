"""The documents and workbooks of target/ written by hand for the world: the endowment's liquidity policy, its
investment policy statement and the university's capital plan (PDFs through the house office writer), the liquid
holdings report, the spending history, Corrigan Hart's draft pacing plan and a peer survey. Documents describe the
rules the trustees set and the positions held; none describes how the managers behave."""
import csv
import datetime as dt
import os
from zoneinfo import ZoneInfo

from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Spacer, Table

import officepdf as O
import world as Wd

NY = ZoneInfo("America/New_York")
F_POLICY = "wexmoor_endowment_liquidity_policy_2025.pdf"
F_IPS = "wexmoor_investment_policy_statement_2024.pdf"
F_CAPPLAN = "wexmoor_university_capital_plan_FY2027_FY2031.pdf"
F_LIQ = "liquid_holdings_2026-12-31.xlsx"
F_SPEND = "spending_distributions_FY2014_FY2027.csv"
F_PLAN = "corrigan_hart_pacing_plan_2027.xlsx"
F_PEER = "peer_endowment_survey_2025.xlsx"

CUSHION = 1150.0          # the minimum reserve the Investment Committee set for the 2027 budget (USD m)
# Corrigan Hart's alternatives for 2027: the full program and three with re-ups deferred to 2028
PROGRAMS = [
    ("A", "The full 2027 program", ("BO", "GE", "VC", "RE", "PC")),
    ("B", "The credit re-up deferred to 2028", ("BO", "GE", "VC", "RE")),
    ("C", "The growth and credit re-ups deferred to 2028", ("BO", "VC", "RE")),
    ("D", "The venture re-up only", ("VC",)),
]

# the holdings at 31 December 2026 (USD m) and the class the Office of Investments assigns each
HOLDINGS = [
    ("Operating cash and money market funds", "Northern Ohio Trust (custody)", "Cash, money market funds and US Treasuries", 186.4, "Daily"),
    ("US Treasury bills, 3 to 12 months", "Northern Ohio Trust (custody)", "Cash, money market funds and US Treasuries", 142.0, "Daily"),
    ("US Treasury notes, 2 to 5 years", "Northern Ohio Trust (custody)", "Cash, money market funds and US Treasuries", 171.3, "Daily"),
    ("Core fixed income account", "Harrowden Asset Management", "Investment-grade bonds", 228.6, "Daily"),
    ("Intermediate credit account", "Lowfield Bond Partners", "Investment-grade bonds", 154.9, "Daily"),
    ("US large cap index fund", "Brayfield Index Trust", "Public equities", 603.3, "Daily"),
    ("US small and mid cap account", "Pembury Capital", "Public equities", 174.2, "Daily"),
    ("International developed equity", "Strand Hill Global", "Public equities", 390.5, "Monthly"),
    ("Emerging markets equity fund", "Kesgrave Partners", "Public equities", 212.7, "Monthly"),
    ("Hollins Bay Multi-Strategy Fund", "Hollins Bay Capital", "Hedge funds: redeemable within 24 months", 96.4, "Quarterly, 65 days' notice"),
    ("Carrow Point Credit Opportunities", "Carrow Point", "Hedge funds: redeemable within 24 months", 118.2, "Quarterly, 90 days' notice"),
    ("Westerby Global Macro", "Westerby Partners", "Hedge funds: redeemable within 24 months", 84.7, "Monthly, 30 days' notice"),
    ("Aldwick Equity Long/Short", "Aldwick Asset Management", "Hedge funds: redeemable within 24 months", 63.0, "Quarterly, 45 days' notice"),
    ("Fenmore Event Driven Fund", "Fenmore Capital", "Hedge funds: not redeemable within 24 months", 141.5, "Locked to 30 June 2029"),
    ("Saltire Structured Credit", "Saltire Investors", "Hedge funds: not redeemable within 24 months", 176.0, "Annual, 25% investor gate, side pocket"),
    ("Corringham Activist Partners", "Corringham", "Hedge funds: not redeemable within 24 months", 95.3, "Three-year rolling lock to 2029"),
    ("Timberland separate account", "Allerton Forest Resources", "Other holdings", 118.0, "None"),
    ("University housing note (program-related)", "Wexmoor University", "Other holdings", 34.0, "None"),
]
FACTORS = {"Cash, money market funds and US Treasuries": 1.00, "Investment-grade bonds": 0.90, "Public equities": 0.70,
           "Hedge funds: redeemable within 24 months": 0.90, "Hedge funds: not redeemable within 24 months": 0.0,
           "Other holdings": 0.0}


def _st():
    body = ParagraphStyle("body", fontName="Helvetica", fontSize=9.4, leading=13.2, spaceAfter=5)
    h1 = ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=13, leading=17, spaceAfter=6)
    h2 = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=10.2, leading=14, spaceBefore=6, spaceAfter=3)
    small = ParagraphStyle("small", fontName="Helvetica", fontSize=8.0, leading=10.5)
    cell = ParagraphStyle("cell", fontName="Helvetica", fontSize=8.6, leading=11)
    return body, h1, h2, small, cell


def policy(path):
    body, h1, h2, small, cell = _st()
    s = [Paragraph("Wexmoor University Endowment  |  Office of Investments", small),
         Paragraph("Liquidity policy for private-fund commitments", h1),
         Paragraph("Adopted by the Investment Committee of the Board of Trustees on 14 March 2024 and amended on 11 "
                   "September 2025. Owner: Chief Investment Officer.", body),
         Paragraph("1. Purpose", h2),
         Paragraph("The endowment commits to private funds years before the money is called, and the funds return it years "
                   "later. This policy makes sure that a year's new commitments leave the endowment able to pay the "
                   "university's spending distribution and every capital call through a severe market without selling "
                   "fund interests or cutting the distribution.", body),
         Paragraph("2. When the test is run", h2),
         Paragraph("Before the Investment Committee approves a year's private-fund commitment budget, the Office of "
                   "Investments tests the budget on the endowment's position at the preceding 31 December. The test covers "
                   "the eight quarters from 1 January of the budget year.", body),
         Paragraph("3. Net cash needs", h2),
         Paragraph("Net cash needs over the eight quarters are the spending distribution, plus the capital calls on every "
                   "private commitment (those made by 31 December and the budget's new commitments), less the distributions "
                   "from the private funds. The spending distribution of each quarter is one quarter of the distribution "
                   "the trustees approved for the fiscal year in which the test is run. Commitments to funds that have not "
                   "held a first close count in full. A commitment's part not called when its fund's term ends is released "
                   "and does not count.", body),
         Paragraph("4. Liquid reserve", h2),
         Paragraph("The liquid reserve is the endowment's holdings at 31 December, each counted at the share of its value its "
                   "liquidity class allows: cash, money market funds and US Treasuries 100 percent; investment-grade bonds "
                   "90 percent; public equities 70 percent; hedge funds the endowment can redeem with the proceeds received "
                   "within the eight quarters 90 percent; all other holdings nothing. The factors stand for the stress in section "
                   "6, so the holdings are counted at their 31 December values and not revalued along its path. The Office of "
                   "Investments assigns each holding its class in the year-end holdings report.", body),
         Paragraph("5. The test", h2),
         Paragraph("A budget passes when the liquid reserve less the net cash needs of the eight quarters is at least the "
                   "minimum reserve the Investment Committee sets each year. For the 2027 budget the minimum reserve is "
                   "USD %s million." % format(int(CUSHION), ","), body),
         Paragraph("6. The stress", h2),
         Paragraph("Net cash needs are measured in a stress this policy sets. The exit market, read on the exit activity "
                   "index, follows its path from the third quarter of 2008 to the second quarter of 2010 relative to its "
                   "level in the second quarter of 2008, starting from its level in the last quarter before the test. "
                   "Public equities stand at 85 percent of their 31 December level in the first quarter and 70 percent "
                   "in the second, then recover five points a quarter to 100 percent. Short-term interest rates stand 2.5 "
                   "percentage points above their 31 December level throughout.", body),
         Paragraph("7. Distributions in the stress", h2),
         Paragraph("In each quarter of the stress, each fund distributes its value at 31 December times the distribution "
                   "rate of its strategy in the matching quarter from the third quarter of 2008 in the industry cash-flow "
                   "benchmark: the benchmark funds' distributions in that quarter over their value at the end of the "
                   "previous quarter, each summed over the strategy's funds. A fund's value at 31 December is its capital "
                   "account value at that date; where the manager's statement for the fourth quarter has not arrived, it is "
                   "the value at 30 September plus the fourth quarter's capital calls less its distributions as the "
                   "custodian recorded them.", body),
         Paragraph("8. Capital calls in the stress", h2),
         Paragraph("Capital calls are those the endowment's managers can be expected to make in the stress, judged on the "
                   "evidence the Office of Investments holds.", body),
         Paragraph("9. The year's new commitments", h2),
         Paragraph("The pacing plan's commitments are tested each at its proposed size. Where the plan sets out alternative "
                   "programs, the Investment Committee adopts the program with the largest total of new commitments that "
                   "passes; where none passes, the endowment makes no new commitments in the year.", body),
         Paragraph("10. Reporting", h2),
         Paragraph("The Office of Investments reports the result to the Investment Committee with the budget, and the "
                   "Committee may approve any budget up to the largest that passes.", body),
         Spacer(1, 8),
         Paragraph("Wexmoor University Endowment. Office of Investments. Internal.", small)]
    O.build(path, s, "Liquidity policy for private-fund commitments", "Daniel Marshall", "Liquidity policy",
            "Wexmoor University Endowment  |  Office of Investments  |  Internal",
            dt.datetime(2025, 9, 11, 16, 2, 31, tzinfo=NY), dt.datetime(2025, 9, 11, 16, 20, 4, tzinfo=NY), producer="LibreOffice 25.8")


def ips(path):
    body, h1, h2, small, cell = _st()
    rows = [["Asset class", "Target", "Range"], ["Public equities", "23%", "15% to 30%"], ["Hedge funds", "13%", "8% to 18%"],
            ["Private equity and venture capital", "32%", "25% to 40%"], ["Real assets (real estate, infrastructure, timber)", "14%", "8% to 18%"],
            ["Private credit", "6%", "2% to 10%"], ["Fixed income and cash", "12%", "8% to 20%"]]
    t = Table([[Paragraph(c, cell) for c in r] for r in rows], colWidths=[260, 70, 90])
    s = [Paragraph("Wexmoor University Endowment", small),
         Paragraph("Investment policy statement", h1),
         Paragraph("Approved by the Board of Trustees on 6 June 2024 on the recommendation of the Investment Committee.", body),
         Paragraph("1. The endowment's purpose", h2),
         Paragraph("The endowment supports the university's teaching, research and financial aid in perpetuity. Its "
                   "investment objective is a real total return of at least the spending rate plus the growth of the "
                   "university's costs, measured over rolling ten-year periods.", body),
         Paragraph("2. Spending", h2),
         Paragraph("The distribution for each fiscal year (1 July to 30 June) is approved by the trustees in June. It is "
                   "70 percent of the previous year's distribution raised by the Higher Education Price Index, plus 30 "
                   "percent of 4.5 percent of the endowment's value at the preceding 31 December. The trustees may "
                   "depart from the rule in an extraordinary year.", body),
         Paragraph("3. Asset allocation", h2), t, Spacer(1, 6),
         Paragraph("4. Rebalancing", h2),
         Paragraph("The Chief Investment Officer rebalances the liquid portfolio when an asset class leaves its range. "
                   "Private allocations move with commitments and are not rebalanced by sale.", body),
         Paragraph("5. Delegation", h2),
         Paragraph("The Investment Committee approves the annual private-fund commitment budget and the liquidity policy. "
                   "The Chief Investment Officer selects managers within the budget, with the advice of the endowment's "
                   "consultant.", body),
         Spacer(1, 8),
         Paragraph("Wexmoor University. Board of Trustees.", small)]
    O.build(path, s, "Investment policy statement", "Jonathan Potter", "Investment policy statement",
            "Wexmoor University Endowment  |  Investment policy statement",
            dt.datetime(2024, 6, 6, 10, 44, 12, tzinfo=NY), dt.datetime(2024, 6, 6, 11, 5, 48, tzinfo=NY), producer="LibreOffice 24.2")


def capplan(path):
    body, h1, h2, small, cell = _st()
    rows = [["Project", "Cost (USD m)", "Funding", "Years"],
            ["Hartley Science Building renewal", "182", "Bonds 120, gifts 62", "FY2027 to FY2030"],
            ["North Campus residence halls", "146", "Bonds 146 (housing revenue)", "FY2027 to FY2029"],
            ["Library and learning commons", "64", "Gifts 40, operating 24", "FY2028 to FY2030"],
            ["Central plant and steam line replacement", "58", "Operating 30, bonds 28", "FY2027 to FY2031"],
            ["Athletics fields and track", "21", "Gifts 21", "FY2029 to FY2030"]]
    t = Table([[Paragraph(c, cell) for c in r] for r in rows], colWidths=[180, 60, 130, 90])
    s = [Paragraph("Wexmoor University  |  Finance and Administration", small),
         Paragraph("Capital plan FY2027 to FY2031", h1),
         Paragraph("Presented to the Finance Committee of the Board of Trustees on 18 September 2026.", body),
         Paragraph("Summary", h2),
         Paragraph("The plan carries USD 471 million of projects over five years. USD 294 million is to be borrowed in two "
                   "tax-exempt series in fiscal 2027 and fiscal 2029, USD 123 million is to come from gifts already "
                   "pledged or in solicitation, and USD 54 million from operating budgets. No project draws on the "
                   "endowment beyond the annual distribution the trustees approve.", body),
         Paragraph("Projects", h2), t, Spacer(1, 6),
         Paragraph("Debt", h2),
         Paragraph("After the two series the university's debt rises from USD 612 million to USD 871 million. Debt service "
                   "stays below 5.5 percent of operating expenses in every year of the plan, inside the 7 percent limit "
                   "of the debt policy. The university keeps USD 150 million of operating liquidity, separate from the "
                   "endowment, against its bonds' covenants.", body),
         Paragraph("Gifts", h2),
         Paragraph("Of the USD 123 million of gifts, USD 71 million is pledged and USD 52 million is in solicitation. If "
                   "solicitation falls short the library is deferred.", body),
         Spacer(1, 8),
         Paragraph("Wexmoor University. Office of the Vice President for Finance.", small)]
    O.build(path, s, "Capital plan FY2027 to FY2031", "Wexmoor University Finance", "Capital plan",
            "Wexmoor University  |  Capital plan FY2027 to FY2031",
            dt.datetime(2026, 9, 18, 9, 12, 5, tzinfo=NY), dt.datetime(2026, 9, 18, 9, 40, 31, tzinfo=NY), producer="LibreOffice 26.2")


def holdings(path):
    wb = Workbook(); ws = wb.active; ws.title = "Holdings 31 Dec 2026"
    ws.append(["Holding", "Manager or custodian", "Policy liquidity class", "Market value 31 Dec 2026 (USD m)", "Liquidity terms"])
    for c in ws[1]: c.font = Font(bold=True)
    for h in HOLDINGS:
        ws.append(list(h[:3]) + [h[3], h[4]])
    ws.append([])
    ws.append(["Private funds at capital account value are reported separately (capital account statements)."])
    for col, w in zip("ABCDE", (44, 30, 44, 16, 34)):
        ws.column_dimensions[col].width = w
    wb.save(path)


def spending_series():
    """the trustees' distributions by fiscal year under the spending rule, from the endowment's value at each preceding
    31 December (USD m)."""
    vals = {2012: 3050.0}
    ret = {2013: 0.112, 2014: 0.071, 2015: 0.018, 2016: 0.064, 2017: 0.121, 2018: 0.026, 2019: 0.118, 2020: 0.094,
           2021: 0.236, 2022: -0.071, 2023: 0.083, 2024: 0.097, 2025: 0.088}
    inflow = {y: 0.030 for y in ret}
    for y in sorted(ret):
        vals[y] = round(vals[y - 1] * (1 + ret[y] + inflow[y]) - 0.045 * vals[y - 1], 1)
    out = []
    dist = round(0.045 * vals[2012], 1)
    hepi = 0.031
    for fy in range(2014, 2028):
        v = vals[fy - 2]
        dist = dist if fy == 2014 else round(0.7 * dist * (1 + hepi) + 0.3 * 0.045 * v, 1)
        out.append((fy, v, dist))
    return out


def spending(path):
    rows = spending_series()
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["fiscal_year", "endowment_value_prior_dec31_usd_m", "approved_distribution_usd_m", "paid_q1_usd_m",
                    "paid_q2_usd_m", "paid_q3_usd_m", "paid_q4_usd_m"])
        for fy, v, dist in rows:
            q = "%.2f" % (dist / 4.0)
            w.writerow([fy, "%.1f" % v, "%.1f" % dist] + ([q] * 4 if fy < 2027 else [q, q, "", ""]))
    return len(rows)


def pacing_plan(path, plan_funds, names):
    wb = Workbook(); ws = wb.active; ws.title = "2027 proposed commitments"
    ws.append(["Fund", "Manager", "Strategy", "Proposed commitment (USD m)", "Commitment expected", "First close expected", "Relationship"])
    for c in ws[1]: c.font = Font(bold=True)
    for f in plan_funds:
        ws.append([f["name"], names[f["gp"]["id"]], {"BO": "Buyout", "GE": "Growth equity", "VC": "Venture capital", "RE": "Real estate",
                   "IN": "Infrastructure", "PC": "Private credit"}[f["gp"]["st"]], f["C"], "Q%d 2027" % Wd.qq(f["commit_q"]),
                   "Q%d %d" % (Wd.qq(f["exp_fc"]), Wd.qy(f["exp_fc"])), "Re-up"])
    ws.append(["Total", "", "", sum(f["C"] for f in plan_funds), "", "", ""])
    wp = wb.create_sheet("Programs")
    wp.append(["Program", "Description", "Funds committed in 2027", "Total (USD m)"])
    for c in wp[1]: c.font = Font(bold=True)
    by = {f["gp"]["st"]: f for f in plan_funds}
    for code, desc, sts in PROGRAMS:
        fs = [by[s] for s in sts if s in by]
        wp.append([code, desc, "; ".join(f["name"] for f in fs), sum(f["C"] for f in fs)])
    ws2 = wb.create_sheet("Long-range pacing")
    ws2.append(["Year", "Buyout", "Growth equity", "Venture capital", "Real estate", "Infrastructure", "Private credit", "Total (USD m)"])
    for c in ws2[1]: c.font = Font(bold=True)
    order = ["BO", "GE", "VC", "RE", "IN", "PC"]
    first = [sum(f["C"] for f in plan_funds if f["gp"]["st"] == s) for s in order]     # 2027 is the year's proposed funds
    ws2.append([2027] + first + [sum(first)])
    base = [175, 95, 50, 65, 50, 65]
    for k, y in enumerate(range(2028, 2032), start=1):
        g = 1.0 + 0.04 * k
        v = [round(b * g / 5.0) * 5 for b in base]
        ws2.append([y] + v + [sum(v)])
    ws3 = wb.create_sheet("Notes")
    for line in ["Draft for discussion with the Office of Investments, 7 December 2026, for the Investment Committee's March 2027 meeting.",
                 "The 2027 program continues existing relationships; no new managers are proposed for 2027, and infrastructure resumes in 2028.",
                 "Commitments are sized to keep the private allocation near its 52 percent policy target by 2031.",
                 "Corrigan Hart LLC, Private Markets Advisory."]:
        ws3.append([line])
    wb.save(path)


def peers(path, rng):
    wb = Workbook(); ws = wb.active; ws.title = "Survey 2025"
    ws.append(["Endowment", "Value 30 Jun 2025 (USD bn)", "Private allocation", "Unfunded commitments / value", "Liquid within 1 year",
               "Payout rate FY2025", "10-year return"])
    for c in ws[1]: c.font = Font(bold=True)
    for i in range(24):
        v = round(float(rng.uniform(2.5, 14.0)), 1)
        pa = float(rng.uniform(0.30, 0.62)); unf = pa * float(rng.uniform(0.28, 0.55)); liq = max(0.08, 1 - pa - float(rng.uniform(0.10, 0.25)))
        ws.append(["Peer %02d" % (i + 1), v, "%.0f%%" % (100 * pa), "%.0f%%" % (100 * unf), "%.0f%%" % (100 * liq),
                   "%.1f%%" % float(rng.uniform(4.0, 5.4)), "%.1f%%" % float(rng.uniform(6.2, 10.8))])
    ws2 = wb.create_sheet("About")
    ws2.append(["Survey of private university endowments of USD 2.5 billion to USD 14 billion, fiscal year 2025, anonymised."])
    ws2.append(["Compiled by Corrigan Hart LLC from responses received by 30 September 2025."])
    wb.save(path)
