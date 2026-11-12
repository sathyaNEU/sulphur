"""task22: the documents in the pack, each a Word document its issuing office exported to PDF (officepdf): the
consultant's 2019 loss evaluation study, the 2027-2028 construction work plan excerpt, the retail rate schedules,
the Finance Department's budget instructions, the revenue protection scope of work and the wholesale supplier's rate
schedule."""
import datetime as dt

from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer, Table

import officepdf
import params as P

SS = getSampleStyleSheet()
BODY = ParagraphStyle("body", parent=SS["BodyText"], fontName="Helvetica", fontSize=9.6, spaceAfter=5, leading=12.8)
CELL = ParagraphStyle("cell", parent=BODY, fontSize=8.0, spaceAfter=0, leading=9.8)
H2 = ParagraphStyle("h2", parent=SS["Heading2"], fontSize=11, spaceBefore=8, spaceAfter=4)
TITLE = ParagraphStyle("title", parent=SS["Heading1"], fontSize=15, spaceAfter=4)
LH = ParagraphStyle("lh", parent=BODY, fontSize=8, leading=10, textColor="#444444")
CT = dt.timezone(dt.timedelta(hours=-6))
CDT = dt.timezone(dt.timedelta(hours=-5))

# filed sentences the checks and the verifier read back
SCOPE_NTL = ("Non-technical loss on a feeder is the energy that entered the feeder, at its substation breaker and "
             "from customers' own generation, and was neither recorded by a customer's meter, used by the City's "
             "unmetered street and area lights, nor lost in the feeder's own conductors, transformers and secondary and "
             "service conductors.")
SCOPE_RULE = ("The City will name the four feeders that carried the largest non-technical loss in the twelve months "
              "ending September 30, 2026, and the contractor's 2027 inspections will cover every service on those four "
              "feeders.")
BUDGET_BASE = ("The electric utility's 2027 power cost budget uses the twelve months ending September 30, 2026 as its base "
               "year: each month of the base year stands for the same month of 2027.")
BUDGET_ADD = ("Add only new connections that hold an approved service application, from their scheduled service dates, "
              "and only works in the approved Construction Work Plan, from their in-service dates. Make no adjustment "
              "for weather.")


def P_(t, st=BODY):
    return Paragraph(t, st)


def T(rows, widths_mm):
    return Table([[P_(str(c), CELL) if not hasattr(c, "wrap") else c for c in r] for r in rows],
                 colWidths=[w * 72 / 25.4 for w in widths_mm])


def study(path, st):
    t1 = [["Feeder", "2019 peak MW", "Energy MWh", "Load factor", "Loss factor", "Equivalent R, ohm", "Peak loss kW"]]
    t2 = [["Feeder", "Primary MWh", "Transformer no-load MWh", "Transformer load MWh", "Secondary MWh",
           "Technical MWh", "Percent of energy"]]
    tot_e = tot_t = 0.0
    for f in P.FEEDER_ORDER:
        s = st[f]
        t1.append([f, "%.2f" % s["peak_mw"], "{:,.0f}".format(s["energy_mwh"]), "%.3f" % s["lf"], "%.3f" % s["lsf"],
                   "%.3f" % s["req"], "%.1f" % s["peak_loss_kw"]])
        t2.append([f, "{:,.0f}".format(s["prim_mwh"]), "{:,.0f}".format(s["nl_mwh"]), "{:,.0f}".format(s["ll_mwh"]),
                   "{:,.0f}".format(s["sec_mwh"]), "{:,.0f}".format(s["tech_mwh"]), "%.2f" % s["tech_pct"]])
        tot_e += s["energy_mwh"]
        tot_t += s["tech_mwh"]
    t2.append(["System", "", "", "", "", "{:,.0f}".format(tot_t), "%.2f" % (100 * tot_t / tot_e)])
    story = [
        P_("<b>HESTER ENGINEERING GROUP, PLLC</b>  |  Consulting Electrical Engineers", LH),
        P_("1420 S Boston Ave, Suite 600, Tulsa, Oklahoma 74119", LH),
        Spacer(1, 8),
        P_("Delmont Power and Light: Distribution System Loss Evaluation", TITLE),
        P_("Prepared for the City of Delmont Utilities Department. Final report, December 13, 2019.", BODY),
        P_("1. Purpose and scope", H2),
        P_("The City asked for an estimate of the technical losses on its fourteen 12.47 kV distribution feeders for "
           "calendar year 2019: the energy lost in primary conductors, distribution transformers and secondary and "
           "service conductors, feeder by feeder, against the energy each feeder delivered from its substation "
           "breaker. Substation transformer losses and station service are reported to the City separately in our "
           "substation study."),
        P_("2. Method", H2),
        P_("Each feeder was modeled in the City's planning model from the GIS extract of October 2019. Primary losses "
           "were computed at the August 2019 system peak hour from a load flow in which each feeder's breaker demand "
           "was allocated to its distribution transformers in proportion to connected kVA. Conductor resistances are "
           "the manufacturers' values at 50 C. On single-phase taps the current returns on the neutral, and the loss on "
           "a single-phase segment is taken as twice the phase conductor's loss at the tap's line-to-neutral current, "
           "which is six times the three-phase expression for the same kVA. Annual primary losses are the peak losses "
           "times 8,760 hours times the loss factor, from each feeder's own 2019 load factor by the Buller and "
           "Woodrow relation (loss factor = 0.15 x load factor + 0.85 x load factor squared)."),
        P_("Distribution transformer no-load losses are the manufacturers' test values by kVA and vintage, applied to "
           "every hour of the year; load losses at rated load from the same tables are scaled by the square of each "
           "transformer's peak loading and by the loss factor. Secondary and service conductor losses are taken as "
           "0.7 percent of the energy delivered to services. The tables used are those in the City's distribution "
           "engineering tables."),
        P_("3. Results", H2),
        P_("Table 1. Feeder loading at the 2019 peak and the equivalent resistance of each feeder's primary.", CELL),
        T(t1, [20, 24, 26, 22, 22, 30, 26]),
        Spacer(1, 8),
        P_("Table 2. Technical losses, calendar year 2019.", CELL),
        T(t2, [20, 24, 28, 28, 24, 26, 24]),
        Spacer(1, 6),
        P_("System technical losses for 2019 are estimated at %.2f percent of the energy delivered at the feeder "
           "breakers. The rural feeders run higher than the town feeders, as their length would lead one to expect." %
           (100 * tot_t / tot_e)),
        P_("4. Limitations", H2),
        P_("Results rest on the 2019 GIS, the 2019 peak and the City's 2019 load factors. The study should be updated "
           "with the next Construction Work Plan."),
        Spacer(1, 6),
        P_("Heidi Hester, P.E., Principal", BODY),
    ]
    officepdf.build(path, story, "Distribution System Loss Evaluation", "Hester Engineering Group, PLLC",
                    "Delmont Power and Light technical losses, 2019", "Hester Engineering Group  |  Delmont Power and Light",
                    dt.datetime(2019, 12, 13, 9, 40, tzinfo=CT), dt.datetime(2019, 12, 13, 16, 12, tzinfo=CT),
                    letter=True, page_of=True, producer="LibreOffice 6.3")


def cwp(path, segments):
    segs = ", ".join(segments)
    rows = [["Project", "Feeder", "Description", "Miles", "In service", "Estimate USD"],
            ["CWP-27-03", "APT-3", "Reconductor the three-phase main from the Airport Road substation outward, 4/0 ACSR "
             "to 336.4 ACSR, GIS segments " + segs, "%.1f" % P.RECONDUCTOR["miles"], "March 15, 2027", "2,380,000"],
            ["CWP-27-05", "NTH-4", "Replace the 1985 step-voltage regulator bank at mile 7; no conductor change", "",
             "May 2027", "214,000"],
            ["CWP-27-07", "CHL-2", "Storm hardening: replace 61 poles and crossarms on the main, same conductor", "",
             "October 2027", "1,105,000"],
            ["CWP-27-09", "APT-4, CHL-2, IND-3", "AMI meter deployment, third phase (meters only)", "",
             "June to September 2027", "1,640,000"],
            ["CWP-27-12", "IND-1", "New underground tap to the Highway 60 business park lots; no load before 2028", "0.6",
             "November 2027", "390,000"]]
    story = [
        P_("<b>CITY OF DELMONT</b>  |  Utilities Department, Electric Division", LH),
        P_("2027-2028 Construction Work Plan: approved projects (excerpt)", TITLE),
        P_("Approved by the Delmont Utilities Board on September 15, 2026 (Resolution UB-2026-31). This excerpt lists the "
           "2027 distribution projects; substation and metering-system projects appear in the full plan."),
        Spacer(1, 4),
        T(rows, [22, 17, 78, 11, 24, 20]),
        Spacer(1, 6),
        P_("In-service dates are the dates the Electric Division plans to energize the completed work. Estimates are "
           "2026 dollars."),
    ]
    officepdf.build(path, story, "2027-2028 Construction Work Plan (excerpt)", "City of Delmont Utilities Department",
                    "Approved 2027 distribution projects", "City of Delmont  |  Utilities Department",
                    dt.datetime(2026, 9, 16, 10, 5, tzinfo=CDT), dt.datetime(2026, 9, 16, 14, 31, tzinfo=CDT), letter=True)


def rates(path):
    lamp_rows = [["Lamp", "Description", "Monthly kWh charged"]]
    names = {"HPS100": "100 W high pressure sodium", "HPS150": "150 W high pressure sodium",
             "HPS250": "250 W high pressure sodium", "MV175": "175 W mercury vapor (closed to new installations)",
             "LED40": "40 W LED", "LED70": "70 W LED", "LED110": "110 W LED"}
    for k in ("HPS100", "HPS150", "HPS250", "MV175", "LED40", "LED70", "LED110"):
        lamp_rows.append([k, names[k], str(P.DEEMED_KWH[k])])
    story = [
        P_("<b>CITY OF DELMONT</b>  |  Delmont Power and Light", LH),
        P_("Electric Rate Schedules (excerpt)", TITLE),
        P_("Effective with bills rendered on and after October 1, 2025. Ordinance 2025-41."),
        P_("Schedule RS, Residential Service", H2),
        P_("Customer charge 18.50 per month. Energy charge 0.1021 per kWh. Power cost adjustment as set monthly under "
           "Schedule PCA. Schedule RS-E applies to residences heated electrically, with the energy charge reduced to "
           "0.0912 per kWh for kWh over 1,000 in the months of November through March."),
        P_("Schedule GS, General Service", H2),
        P_("For non-residential service under 300 kW. Customer charge 32.00 per month. Energy charge 0.1104 per kWh."),
        P_("Schedule LP, Large Power", H2),
        P_("For service of 300 kW and over, metered by interval meter. Customer charge 285.00 per month. Demand charge "
           "13.90 per kW of the highest 15-minute demand in the month. Energy charge 0.0618 per kWh."),
        P_("Schedules SL and AL, Street and Area Lighting", H2),
        P_("Dusk-to-dawn lighting controlled by photocell, owned and maintained by the City. Schedule SL applies to "
           "street lighting billed to the City's general fund; Schedule AL to area lights rented to customers at "
           "8.75 per lamp per month. Lighting is not metered: each lamp is charged the monthly kWh below for its lamp "
           "type, at the GS energy charge."),
        T(lamp_rows, [22, 90, 36]),
        Spacer(1, 6),
        P_("Schedule PCA, Power Cost Adjustment: the City's purchased power cost per kWh sold, set monthly from the "
           "Bluestem Municipal Power Agency invoice and the twelve-month average line loss."),
    ]
    officepdf.build(path, story, "Electric Rate Schedules (excerpt)", "City of Delmont", "Retail electric rates",
                    "Delmont Power and Light  |  Rate schedules", dt.datetime(2025, 9, 3, 9, 15, tzinfo=CDT),
                    dt.datetime(2025, 9, 24, 11, 48, tzinfo=CDT), letter=True, producer="LibreOffice 25.2")


def budget(path):
    story = [
        P_("<b>CITY OF DELMONT</b>  |  Finance Department", LH),
        P_("FY2027 Utility Budget Instructions: Electric Fund", TITLE),
        P_("To: Utility Director and division managers. From: Director of Finance. October 7, 2026."),
        P_("1. Base year", H2),
        P_(BUDGET_BASE),
        P_("2. What to add", H2),
        P_(BUDGET_ADD),
        P_("3. Purchased power", H2),
        P_("Purchased power is budgeted as forecast sales plus forecast losses, at the Bluestem Municipal Power Agency "
           "rates in effect on January 1, 2027. Show technical losses for each feeder, and substation losses and "
           "station service for each substation. Non-technical losses are carried at the base year's level unless the "
           "Revenue Protection program is funded, in which case the Utility Director may budget a recovery."),
        P_("4. Timetable", H2),
        P_("Division submissions are due to Finance by December 4, 2026, for the City Council's budget hearing on "
           "December 15, 2026."),
    ]
    officepdf.build(path, story, "FY2027 Utility Budget Instructions", "City of Delmont Finance Department",
                    "Electric Fund budget instructions", "City of Delmont  |  Finance Department",
                    dt.datetime(2026, 10, 7, 8, 55, tzinfo=CDT), dt.datetime(2026, 10, 7, 9, 40, tzinfo=CDT), letter=True)


def scope(path):
    story = [
        P_("<b>CITY OF DELMONT</b>  |  Purchasing Division", LH),
        P_("Request for Proposals 2026-14: Revenue Protection Field Services", TITLE),
        P_("Issued October 21, 2026. Proposals due November 18, 2026."),
        P_("Attachment A. Scope of work", H2),
        P_("A.1 The contractor will inspect every metered and unmetered service on the feeders the City names, verify "
           "meter seals, connections and service drops, identify diversion, bypass and tampering, and report each finding "
           "with photographs to Delmont Power and Light's Revenue Protection supervisor."),
        P_("A.2 " + SCOPE_RULE),
        P_("A.3 " + SCOPE_NTL),
        P_("A.4 Field work runs from February 1 to November 30, 2027. The contract funds inspections on four feeders."),
        P_("Attachment B. Insurance and bonding", H2),
        P_("The contractor carries general liability of not less than 1,000,000 per occurrence and holds the City "
           "harmless as set out in the City's standard terms."),
    ]
    officepdf.build(path, story, "RFP 2026-14 Revenue Protection Field Services", "City of Delmont Purchasing Division",
                    "Scope of work", "City of Delmont  |  Purchasing", dt.datetime(2026, 10, 21, 13, 10, tzinfo=CDT),
                    dt.datetime(2026, 10, 21, 15, 2, tzinfo=CDT), letter=True)


def wholesale(path):
    rows = [["Charge", "Rate", "Basis"],
            ["Production demand", "11.42 per kW", "the member's demand at the agency's monthly coincident peak"],
            ["Transmission", "3.18 per kW", "the same coincident demand"],
            ["Energy", "0.0391 per kWh", "metered at each delivery point"],
            ["Power cost adjustment", "set monthly", "the agency's fuel and purchased power cost above base"],
            ["Delivery point charge", "1,450 per month", "each delivery point"]]
    story = [
        P_("<b>BLUESTEM MUNICIPAL POWER AGENCY</b>", LH),
        P_("Wholesale Power Rate Schedule W-1, 2026", TITLE),
        P_("Applies to all-requirements members. Effective January 1, 2026; adopted by the Agency Board on November 20, "
           "2025."),
        T(rows, [40, 30, 90]),
        Spacer(1, 6),
        P_("Delivery point meters record kWh and kVArh by hour ending, Central Standard Time throughout the year. "
           "Members receive interval data with each monthly invoice."),
    ]
    officepdf.build(path, story, "Wholesale Power Rate Schedule W-1, 2026", "Bluestem Municipal Power Agency",
                    "Wholesale rates", "Bluestem Municipal Power Agency", dt.datetime(2025, 11, 21, 10, 0, tzinfo=CT),
                    dt.datetime(2025, 11, 24, 8, 30, tzinfo=CT), letter=True, producer="LibreOffice 25.8")
