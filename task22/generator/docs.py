"""task22 architecture 2: the documents in the pack, each a Word document its issuing office exported to PDF
(officepdf): the Utilities Commission's program rules, the 2019 consultant's lost and unaccounted-for gas study, the
Measurement and Regulation section's 2025 gas temperature study memo, and the data field notes."""
import datetime as dt

import numpy as np
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
CST = dt.timezone(dt.timedelta(hours=-6))
CDT = dt.timezone(dt.timedelta(hours=-5))

# filed sentences the checks and the verifier read back
RULE_DEF = ("Leak loss in a pressure district is the gas delivered into the district at its regulator stations, less "
            "the gas the district's customers took through their meters, the Utility's own use in the district, gas "
            "lost to third-party damage in the district and gas taken in the district without authorization. Every "
            "quantity is measured at base conditions, 14.73 psia and 60 degrees Fahrenheit.")
RULE_MAINS = ("A pressure district enters the 2027-2029 main replacement program if its leak loss in the twelve months "
              "ending September 30, 2026 exceeded 1.0 per cent of the gas delivered into it in the same twelve months.")
RULE_METERS = ("The 2027 meter changeout replaces the meters that do not compensate for gas temperature in each "
               "pressure district where, in the twelve months ending September 30, 2026, the gas those meters "
               "delivered at base conditions exceeded the volume billed for them by more than 3.5 per cent of that "
               "billed volume, and where at least 100 such meters remain in service.")
RULE_PLAN = ("The changeouts the 2027 plan already schedules in Old Town and Downtown proceed as planned and are not "
             "re-decided under Rule 2.")


def P_(t, st=BODY):
    return Paragraph(t, st)


def T(rows, widths_mm):
    return Table([[P_(str(c), CELL) for c in r] for r in rows], colWidths=[w * 72 / 25.4 for w in widths_mm])


def rules(path):
    story = [
        P_("<b>BRANDVOLD UTILITIES COMMISSION</b>  |  City of Brandvold, Minnesota", LH),
        P_("Resolution 2026-11", LH),
        Spacer(1, 8),
        P_("Lost and Unaccounted-For Gas Reduction Program: Program Rules", TITLE),
        P_("Adopted by the Commission at its regular meeting of June 16, 2026.", BODY),
        P_("1. Purpose", H2),
        P_("The Commission reviewed the gas utility's lost and unaccounted-for gas at its meetings of February and April "
           "2026. Each pressure district has had its own regulator station metering since 2021. These rules set how the "
           "2027 capital budget decides which districts' mains are replaced in 2027 to 2029 and where the 2027 meter "
           "changeout goes."),
        P_("2. Definitions", H2),
        P_(RULE_DEF),
        P_("Gas the district's customers took includes every premise served from the district's mains, the large "
           "customers on electronic volume correctors among them. The Utility's own use is the gas burned in the "
           "regulator station heaters. Gas taken without authorization is gas taken through any bypass of, or "
           "interference with, a meter."),
        P_("A meter's under-registration is the gas it delivered at base conditions less the volume billed for it "
           "(the billing system bills each meter's registered volume times the pressure factor)."),
        P_("3. Rules", H2),
        P_("<b>Rule 1, main replacement.</b> " + RULE_MAINS),
        P_("<b>Rule 2, meter changeout.</b> " + RULE_METERS),
        P_("<b>Rule 3, changeouts already planned.</b> " + RULE_PLAN),
        P_("4. Filing", H2),
        P_("The Engineering Manager files the districts that enter the main replacement program and the districts where "
           "the 2027 changeout goes with the Commission by December 1, 2026, for the 2027 capital budget. The "
           "Commission adopts the 2027 capital budget at its December 15, 2026 meeting."),
        Spacer(1, 10),
        P_("Attest: Secretary to the Commission", LH),
    ]
    officepdf.build(path, story, "LAUF Reduction Program Rules", P.COMMISSION, "Resolution 2026-11",
                    "Brandvold Utilities Commission  |  Resolution 2026-11",
                    dt.datetime(2026, 6, 16, 19, 40, tzinfo=CDT), dt.datetime(2026, 6, 18, 10, 2, tzinfo=CDT),
                    letter=True, producer="LibreOffice 7.6")


def lauf_study(path, s):
    t1 = [["Month", "Airport mean, F", "Volume billed through meters without compensation, Mcf",
           "Temperature effect, Mcf"]]
    for r in s["months"]:
        t1.append(r)
    t2 = [["Component", "Mcf", "Per cent of receipts"]]
    for r in s["components"]:
        t2.append(r)
    story = [
        P_("<b>J. MURRAY &amp; ASSOCIATES</b>  |  Gas measurement consulting, Fargo, North Dakota", LH),
        Spacer(1, 8),
        P_("Brandvold Public Utilities: Lost and Unaccounted-For Gas Study, Fiscal Year 2019", TITLE),
        P_("Prepared for the Brandvold Utilities Commission. Final report, December 9, 2019.", BODY),
        P_("1. Scope", H2),
        P_("The Commission asked for the gas utility's lost and unaccounted-for gas in the fiscal year ended September 30, "
           "2019 and its parts. Receipts are the city gate station's corrected volume; sales are the volume billed on "
           "bills issued in the fiscal year; company use is the Utility's regulator heaters and the gate line heater."),
        P_("2. Results", H2),
        P_("Lost and unaccounted-for gas was %s Mcf, %s per cent of receipts. Its parts as we estimate them:" % (
            "{:,.0f}".format(s["lauf"]), "%.2f" % s["lauf_pct"])),
        T(t2, [80, 30, 40]),
        P_("3. The temperature effect", H2),
        P_("About seventy per cent of the Utility's residential meters do not compensate for gas temperature, and the "
           "billing system bills their registered volume at the pressure factor alone. We took the temperature of the "
           "gas at those meters to be each month's mean temperature at Brandvold Regional Airport and applied the "
           "ratio of 519.67 to that temperature in degrees Rankine to the month's volume billed through those meters."),
        T(t1, [24, 30, 70, 34]),
        P_("4. Recommendations", H2),
        P_("Install corrected flow metering at every district regulator station so lost gas can be followed district by "
           "district. Continue replacing non-compensating meters as they reach the end of their test period."),
    ]
    officepdf.build(path, story, "Lost and Unaccounted-For Gas Study, FY2019", "J. Murray & Associates",
                    "Brandvold Public Utilities LAUF, FY2019", "J. Murray & Associates  |  Brandvold Public Utilities",
                    dt.datetime(2019, 12, 9, 10, 15, tzinfo=CST), dt.datetime(2019, 12, 9, 15, 52, tzinfo=CST),
                    letter=True, page_of=True, producer="LibreOffice 6.3")


def study_memo(path, m):
    t1 = [["Month", "Airport mean air, F", "Outdoor meters, mean gas temperature, F",
           "Indoor meters, mean gas temperature, F", "Logger-days"]]
    for r in m["months"]:
        t1.append(r)
    story = [
        P_("<b>BRANDVOLD PUBLIC UTILITIES</b>  |  Gas Division, Measurement and Regulation", LH),
        Spacer(1, 8),
        P_("Memo: Gas Temperature at Residential Meters, Winter 2024-25", TITLE),
        P_("To: Engineering Manager. Date: June 12, 2025.", BODY),
        P_("1. What we measured", H2),
        P_("From November 1, 2024 to April 30, 2025 we fitted temperature loggers at the inlets of %d residential "
           "meters that do not compensate for temperature: %d outdoor meter sets in North End, Riverside, Elm Grove, "
           "Halvorsen, Sundquist and Lakeview, and %d meters inside basements in Old Town and Downtown. Each logger "
           "recorded the gas temperature every 15 minutes and counted the meter's index pulses; the file "
           "gas_temperature_study_loggers_2024-11_2025-04.csv holds each logger's daily summary (the flow-weighted "
           "mean gas temperature, the hours with flow and the registered ccf)." % (m["n"], m["n_out"], m["n_in"])),
        P_("2. Results", H2),
        T(t1, [22, 28, 42, 42, 22]),
        P_("Gas at the outdoor meter sets ran well above the air through the winter, and the indoor meters sat close to "
           "basement temperature all winter. A straight-line fit of the outdoor loggers' daily mean gas temperature on "
           "the airport's daily mean air temperature gives gas temperature = %.1f + %.3f x air temperature (F), with "
           "R-squared %.2f over %d logger-days." % (m["a"], m["b"], m["r2"], m["n_days"])),
        P_("3. Note", H2),
        P_("The loggers were removed in May 2025. Logger TL-%s lost its pulse input for nine days in February; its "
           "temperatures for those days are kept." % m["dropout"]),
    ]
    officepdf.build(path, story, "Gas Temperature at Residential Meters, Winter 2024-25", P.ORG,
                    "Measurement and Regulation memo", "Brandvold Public Utilities  |  Measurement and Regulation",
                    dt.datetime(2025, 6, 12, 8, 50, tzinfo=CDT), dt.datetime(2025, 6, 12, 14, 7, tzinfo=CDT),
                    letter=True, producer="LibreOffice 7.6")


def rate_schedules(path):
    rows = [["Schedule", "Service", "Customer charge", "Distribution charge"],
            ["G-1", "Residential firm", "USD 14.50 a month", "USD 0.2875 per ccf"],
            ["G-2", "Small commercial firm", "USD 32.00 a month", "USD 0.2410 per ccf"],
            ["G-3", "Large commercial and industrial, corrector metered", "USD 185.00 a month",
             "USD 1.912 per Mcf"]]
    story = [
        P_("<b>BRANDVOLD PUBLIC UTILITIES</b>  |  Gas Division", LH),
        Spacer(1, 6),
        P_("Gas Rate Schedules and General Terms (excerpt)", TITLE),
        P_("Effective January 1, 2026, as adopted by the Brandvold Utilities Commission.", BODY),
        P_("1. Rate schedules", H2),
        T(rows, [18, 70, 36, 44]),
        P_("The purchased gas adjustment is added to every schedule each month as the Commission sets it."),
        P_("2. Billing volume", H2),
        P_("Meters on Schedules G-1 and G-2 are read monthly on the Utility's reading cycles. The billing volume is the "
           "volume the meter registered since the previous reading, in ccf, multiplied by the pressure factor %.4f "
           "for the standard delivery pressure of 7 inches water column at Brandvold's elevation. Meters on Schedule "
           "G-3 are billed on the corrected volume their electronic volume corrector records, in Mcf at 14.73 psia "
           "and 60 degrees Fahrenheit." % P.PF),
        P_("3. Estimated bills", H2),
        P_("When no reading is obtained the Utility bills an estimated volume. The next actual reading corrects the "
           "estimate, and the difference is billed or credited on that bill."),
        P_("4. Gas day", H2),
        P_("The gas day is the 24 hours beginning at 9:00 a.m. Central Clock Time, named by the date on which it begins."),
    ]
    officepdf.build(path, story, "Gas Rate Schedules and General Terms", P.ORG, "Gas rate schedules, 2026",
                    "Brandvold Public Utilities  |  Gas rate schedules",
                    dt.datetime(2025, 12, 9, 15, 20, tzinfo=CST), dt.datetime(2025, 12, 16, 10, 4, tzinfo=CST),
                    letter=True, producer="LibreOffice 25.8")
