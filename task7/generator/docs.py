"""task7: the pack's documents, each a Word document exported to PDF by LibreOffice Writer (officepdf.py). They
define fields and file the WHAT; none of them describes how a figure is to be computed beyond the bank's own formula."""
import datetime as dt
import os
from collections import defaultdict

from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import PageBreak, Paragraph, Spacer, Table

import golden as GD
import officepdf
import world as W

IE_WINTER = dt.timezone(dt.timedelta(hours=0))
IE_SUMMER = dt.timezone(dt.timedelta(hours=1))
H1 = ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=14, spaceAfter=6, textColor="#14425E")
H2 = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=10.5, spaceBefore=8, spaceAfter=3, textColor="#14425E")
BODY = ParagraphStyle("b", fontName="Helvetica", fontSize=9.2, spaceAfter=4)
SMALL = ParagraphStyle("s", fontName="Helvetica", fontSize=8, spaceAfter=2, textColor="#444444")


def P(t, st=BODY):
    return Paragraph(t, st)


def T(rows, widths):
    return Table(rows, colWidths=widths)


def pct(x, nd=2):
    return ("%." + str(nd) + "f%%") % (100 * x)


def eur(x):
    return "€" + format(int(round(x)), ",")


def policy(target):
    s = [P("Ardcarn Bank plc", SMALL), P("Credit Risk Policy: Part 4, Measurement", H1),
         P("Version 7.2, approved by the Board Risk Committee on 26 November 2025. Owner: Chief Risk Officer, "
           "Geraldine Harkins.", SMALL),
         P("4.1 Internal grades and the master scale", H2),
         P("Every business facility carries an internal grade from 1 (strongest) to 8 (weakest), set at "
           "origination and reviewed at least once a year and whenever the credit committee asks. A facility in "
           "default carries grade D. Each grade maps to a twelve-month probability of default on the master scale "
           "below, recalibrated in 2025."),
         T([["Grade", "Twelve-month probability of default"]] +
           [[str(g), pct(W.PUBLISHED_PD[g])] for g in range(1, 9)], [60, 200]),
         P("4.2 Default", H2),
         P("A facility is in default when any amount is more than 90 days past due, when the bank judges the "
           "borrower unlikely to pay in full without recourse to its security, or when a receiver is appointed. "
           "A default of one facility is a default of every facility of the same customer. The default date is the "
           "date the first of these events occurs."),
         P("4.3 Stages", H2),
         P("Stage 1 holds performing facilities graded 1 to 5 and less than 30 days past due; stage 2 holds "
           "performing facilities graded 6 to 8 or 30 or more days past due; stage 3 holds facilities in default."),
         P("4.4 Expected credit loss", H2),
         P("The twelve-month expected credit loss of a facility is its probability of default times its loss given "
           "default times its exposure at default. The loss given default of a facility secured on commercial "
           "property is set by the bank's commercial property LGD model (CRE-LGD-3). A property that secures more "
           "than one facility is shared between them in proportion to their exposures at the reporting date."),
         P("4.5 Security values", H2),
         P("The property register records two kinds of valuation for each property. An inspection is a valuation by "
           "an approved valuer who has inspected the property; the bank commissions one before it lends, whenever "
           "the credit committee asks, and when a facility the property secures defaults. An index roll-forward is "
           "the latest inspection carried forward to a quarter end by the Brackley Rowe commercial property index "
           "series for the property's sector and region, using that quarter's first release; the register writes "
           "one at each quarter's release. Each register row carries the date it took effect, the valuation basis "
           "and the date its value refers to."),
         P("4.6 Records", H2),
         P("The data warehouse keeps every version of a property's valuation as its own row, effective from the "
           "date it was loaded until the next version took effect. Facility numbers were re-issued at the core "
           "banking conversion of 5 June 2021; the facility register keeps the earlier number beside the current "
           "one. Rows loaded before the conversion carry the old system's basis codes, FULL for an inspection and "
           "IDX for an index roll-forward.")]
    path = os.path.join(target, "ardcarn_credit_risk_policy_part4_2025.pdf")
    officepdf.build(path, s, "Credit Risk Policy: Part 4, Measurement", "Geraldine Harkins", "Credit risk policy",
                    "Ardcarn Bank plc | Credit Risk Policy Part 4 | v7.2",
                    dt.datetime(2025, 11, 26, 10, 14, tzinfo=IE_WINTER), dt.datetime(2025, 11, 27, 16, 2, tzinfo=IE_WINTER))


def lgd_doc(target, T_):
    """the model's own documentation: its formula, its haircut and its back-test at the inspection at default"""
    rec = GD.record(T_)
    sales = defaultdict(float)
    by_year = defaultdict(lambda: [0.0, 0.0, 0.0, 0])
    for x in rec:
        pass
    # back-test on closed workouts: predicted LGD from the inspection at default against the realised LGD
    import csv
    post = defaultdict(float)
    with open(os.path.join(target, "recovery_postings_2012_2027.csv"), newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            post[r["facility_no"]] += float(r["amount_eur"])
    closed = {}
    with open(os.path.join(target, "default_register_2012_2026.csv"), newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["workout_status"] == "Closed - sold" and r["facility_no"] not in closed:
                closed[r["facility_no"]] = (GD.D(r["default_date"]), float(r["balance_at_default_eur"]))
    insp_at = {}
    for f, (d, ead) in closed.items():
        props = [p for (a, b, p) in T_.props_of_fac_at.get(f, []) if a <= d <= b]
        v = 0.0
        ok = True
        for p in props:
            h = T_.val.get(p, [])
            at = [x for x in h if x["basis"] == "INSPECTION" and d <= x["vdate"] <= d + dt.timedelta(days=92)]
            if not at:
                ok = False
                break
            v += at[0]["value"]
        if ok and props:
            insp_at[f] = v
    # a borrower's facilities share the inspection in proportion to their balances at default
    cust_fac = defaultdict(list)
    for f in insp_at:
        cust_fac[(T_.cust_of.get(T_.legacy_to_new.get(f, f), f), closed[f][0])].append(f)
    for key_, fs in cust_fac.items():
        tot = sum(closed[f][1] for f in fs)
        shared = max(insp_at[f] for f in fs)
        for f in fs:
            d, ead = closed[f]
            v = shared * ead / tot
            pred = max(0.0, ead - (1 - GD.H) * v)
            real = max(0.0, ead - post.get(f, 0.0))
            yr = by_year[d.year]
            yr[0] += pred
            yr[1] += real
            yr[2] += ead
            yr[3] += 1
    rows = [["Default year", "Facilities", "Predicted LGD", "Realised LGD", "Difference"]]
    for y in sorted(by_year):
        if y > 2024:
            continue
        a, b, e, n = by_year[y]
        rows.append([str(y), str(n), pct(a / e, 1), pct(b / e, 1), "%+.1f" % (100 * (b - a) / e)])
    s = [P("Ardcarn Bank plc", SMALL), P("CRE-LGD-3: commercial property loss given default", H1),
         P("Model documentation, version 3.1. Model owner: Head of Credit Risk Modelling. Independent validation: "
           "Model Risk, 14 October 2025.", SMALL),
         P("1. Scope", H2),
         P("The model sets the loss given default of business facilities secured on commercial property in the "
           "Republic of Ireland, for the expected credit loss under the Credit Risk Policy, Part 4."),
         P("2. Specification", H2),
         P("The loss given default of a facility is max(0, EAD - (1 - h) x V) / EAD, where EAD is the facility's "
           "exposure at default, V is the value of the security at the date of default as established by the "
           "inspection the bank commissions when the facility defaults, and h is the realisation haircut. Where a "
           "property secures more than one facility, V is the facility's share of it under Policy 4.4."),
         P("3. The haircut", H2),
         P("h = 22 per cent. It is the shortfall of a receiver's sale proceeds, net of selling costs, against the "
           "inspection at default, over the closed workouts of 2012 to 2024 (mean net proceeds 78 per cent of the "
           "inspection), and it absorbs the time from default to sale at the facilities' effective rates."),
         P("4. Back-test", H2),
         P("Predicted loss given default against realised loss given default for the closed workouts in each "
           "default year, exposure-weighted. The model passes when the difference lies within 3 points in every "
           "year."),
         T(rows, [70, 60, 80, 80, 70]),
         P("5. Validation conclusion", H2),
         P("Model Risk confirmed the specification and the haircut and rated the model green. Next review: "
           "October 2027.")]
    path = os.path.join(target, "cre_lgd_model_documentation_2025.pdf")
    officepdf.build(path, s, "CRE-LGD-3 model documentation", "Credit Risk Modelling", "LGD model",
                    "Ardcarn Bank plc | CRE-LGD-3 v3.1", dt.datetime(2025, 10, 20, 11, 30, tzinfo=IE_SUMMER),
                    dt.datetime(2025, 10, 21, 9, 5, tzinfo=IE_SUMMER))
    return rows


def plan_instruction(target):
    s = [P("Ardcarn Bank plc: internal memorandum", SMALL),
         P("2027 plan: credit loss on commercial property lending", H1),
         P("From: Colm Hourican, Chief Financial Officer. To: Geraldine Harkins, Chief Risk Officer. "
           "Date: 12 January 2027.", SMALL),
         P("The executive committee settles the 2027 plan on 3 February. The plan carries one line for credit loss "
           "on commercial property lending, and I need your figure for it."),
         P("The line is the expected credit loss on the commercial property facilities that are performing at "
           "31 December 2026 and default during 2027. Each facility's chance of defaulting in 2027 is the "
           "twelve-month probability of default on the master scale for its grade at 31 December 2026, and its "
           "exposure is its balance at that date. Its loss given default is CRE-LGD-3 applied to the value we would "
           "expect our inspection to put on the security if the facility defaulted, taking each default as if it fell "
           "on 1 January 2027 and property prices held at their latest published level through 2027."),
         P("Facilities already in default at 31 December 2026 are provided for separately and are not in this "
           "line, and lending we write in 2027 sits in the new-business line."),
         P("For the committee I would like the figure split between our investment lending and our owner-occupied "
           "lending, and the facilities expected to cost us most, together with the facility-level list the planning "
           "system loads.")]
    path = os.path.join(target, "plan_2027_credit_loss_request.pdf")
    officepdf.build(path, s, "2027 plan: credit loss on commercial property lending", "Colm Hourican",
                    "2027 plan", "Ardcarn Bank plc | Finance", dt.datetime(2027, 1, 12, 17, 41, tzinfo=IE_WINTER),
                    dt.datetime(2027, 1, 12, 17, 58, tzinfo=IE_WINTER))


def outlook(target):
    rows = [["Sector", "Prime yield, end 2026", "Rental growth 2027", "Capital value growth 2027"],
            ["Offices (Dublin)", "5.40%", "+1.0%", "-2.5%"], ["Offices (regions)", "6.75%", "0.0%", "-3.5%"],
            ["Retail", "6.25%", "+1.5%", "+1.0%"], ["Industrial and logistics", "5.10%", "+4.0%", "+3.5%"],
            ["Hotels", "6.90%", "+2.5%", "+2.0%"], ["Healthcare", "5.75%", "+2.0%", "+1.5%"]]
    s = [P("Corrigan Hale Research", SMALL), P("Irish commercial property: outlook for 2027", H1),
         P("Published 2 December 2026. For clients and their advisers.", SMALL),
         P("Investment volumes recovered through 2026 as financing costs eased, with logistics and healthcare "
           "drawing the most capital and secondary offices outside Dublin still finding few buyers."),
         T(rows, [130, 100, 95, 115]),
         P("We expect capital values to stabilise in 2027 in every sector except offices, where vacancy in older "
           "stock continues to weigh on regional pricing. Forecasts are for prime assets; secondary assets have "
           "historically moved further in either direction."),
         P("This note is research, not advice. Corrigan Hale Research is not regulated to give investment advice.",
           SMALL)]
    path = os.path.join(target, "irish_cre_outlook_2027.pdf")
    officepdf.build(path, s, "Irish commercial property: outlook for 2027", "Corrigan Hale Research", "Outlook",
                    "Corrigan Hale Research | December 2026", dt.datetime(2026, 12, 2, 8, 0, tzinfo=IE_WINTER),
                    dt.datetime(2026, 12, 2, 8, 20, tzinfo=IE_WINTER))


def concentration(target, P_):
    w = P_.w
    i_q3 = W.MI[(2026, 9)]
    by_s, by_r = defaultdict(float), defaultdict(float)
    for fi in P_.facs:
        f = w.facs[fi]
        if W.MI[f["orig"]] > i_q3 or (f["end"] is not None and f["end"] <= i_q3):
            continue
        b = W.balance(f, i_q3) or 0
        by_s[w.props[f["props"][0]]["sector"]] += b
        by_r[w.props[f["props"][0]]["region"]] += b
    tot = sum(by_s.values())
    limits = {"Retail": 0.30, "Office": 0.30, "Industrial": 0.30, "Hospitality": 0.25, "Healthcare": 0.20}
    rows = [["Sector", "Exposure", "Share", "Limit"]] + [[s, eur(by_s[s]), pct(by_s[s] / tot, 1), pct(limits[s], 0)]
                                                         for s in W.SECTORS]
    rows2 = [["Region", "Exposure", "Share"]] + [[r, eur(by_r[r]), pct(by_r[r] / tot, 1)] for r in W.REGIONS]
    s = [P("Ardcarn Bank plc", SMALL), P("Commercial property concentration report, 30 September 2026", H1),
         P("For the Board Risk Committee, 18 November 2026. Prepared by Credit Portfolio Management.", SMALL),
         P("All sector exposures sit inside their Board limits. The share of owner-occupied hospitality rose for "
           "the third quarter running."),
         T(rows, [110, 110, 60, 60]), Spacer(1, 8), T(rows2, [110, 110, 60])]
    path = os.path.join(target, "cre_concentration_report_2026Q3.pdf")
    officepdf.build(path, s, "Commercial property concentration report, Q3 2026", "Credit Portfolio Management",
                    "Concentration", "Ardcarn Bank plc | Credit Portfolio Management",
                    dt.datetime(2026, 11, 12, 15, 2, tzinfo=IE_WINTER), dt.datetime(2026, 11, 18, 9, 47, tzinfo=IE_WINTER))


def write_all(target, P_):
    policy(target)
    rows = lgd_doc(target, GD.load(target))
    plan_instruction(target)
    outlook(target)
    concentration(target, P_)
    return rows
