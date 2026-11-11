"""task10 architecture 7: the governing documents and the charging statement, written as Wealdmoor issues them
(a Word document exported to PDF by LibreOffice, dated to its issue)."""
import datetime as dt
import os

from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import KeepTogether, Paragraph, Spacer, Table

import officepdf
import pack as PK
import world as W

SS = getSampleStyleSheet()
BODY = ParagraphStyle("body", parent=SS["BodyText"], fontName="Helvetica", fontSize=9.4, spaceAfter=4, leading=12.4)
SMALL = ParagraphStyle("small", parent=BODY, fontSize=8, spaceAfter=2)
CELL = ParagraphStyle("cell", parent=BODY, fontSize=8.2, spaceAfter=0, leading=10)
H1 = SS["Heading1"]
H2 = ParagraphStyle("h2", parent=SS["Heading2"], fontSize=11, spaceBefore=8, spaceAfter=4)
TITLE = ParagraphStyle("title", parent=H1, fontSize=15, spaceAfter=4)
LH = ParagraphStyle("lh", parent=BODY, fontSize=8, leading=10, textColor="#444444")
ORG = PK.ORG


def P(t, st=BODY):
    return Paragraph(t, st)


def T(rows, widths_mm):
    return Table([[P(c, CELL) if isinstance(c, str) else c for c in r] for r in rows],
                 colWidths=[w * 72 / 25.4 for w in widths_mm])


def aware(s):
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))


def letterhead(unit):
    return [P("<b>WEALDMOOR POWER NETWORKS PLC</b>  |  %s" % unit, LH),
            P("Kestrel House, Cardinal Way, Halverton HV2 7RQ  |  Registered in England No. 02618441", LH),
            Spacer(1, 8)]


def zone_primaries():
    return [W.BY[z["key"]] for z in W.ZONES]


def write_guideline(target):
    firm_rows = [["Primary substation", "Asset code", "Transformers (ONAF, MVA)", "Firm capacity (MW)"]]
    for p in sorted(W.PRIMARIES, key=lambda q: q["name"]):
        onaf = [u[1] for u in PK.NAMEPLATE[p["key"]]]
        firm_rows.append([p["name"], p["code"], "%d + %d" % tuple(onaf), "%.1f" % p["firm"]])
    story = letterhead("Network Planning") + [
        P("Primary Substation Capacity Assessment: Winter Planning Guideline", TITLE),
        P("Document WPN-NP-G-014, issue 5. Applies to the 33/11 kV primary substations of the Halverton grid supply point "
          "group from the assessment made in autumn 2026 for winter 2027/28.", BODY),
        P("1. Purpose", H2),
        P("Each autumn Network Planning assesses whether every primary substation in a constraint managed zone will hold its "
          "firm capacity on the design day of the winter after next, and recommends to the December capital expenditure "
          "review the primaries whose reinforcement must be committed then. A reinforcement committed at the December review "
          "is energised by the end of the following October, so a primary committed in December 2026 is reinforced for "
          "winter 2027/28. Where more flexibility could hold a primary within its firm capacity instead, the review "
          "weighs that against the reinforcement before committing it.",
          BODY),
        P("2. Design condition", H2),
        P("The design day is a working weekday on which the daily mean air temperature at Halverton weather station is "
          "minus 3.0 degrees Celsius. The daily mean is the mean of the station's hourly readings for the GMT day. A working "
          "weekday is a Monday to Friday that is not a bank holiday and does not fall in the Christmas and New Year period "
          "(24 December to 2 January). The assessment concerns every such day, whether or not a flexibility service would "
          "be instructed on it. A winter's design day is assessed as at 15 January of that winter, the assessment date.",
          BODY),
        P("3. Design-day demand", H2),
        P("A primary's design-day demand is its half-hourly demand (MW, the SCADA total of its transformer secondaries) on "
          "the design day with no flexibility service delivered and with the network in its normal running arrangement, "
          "no load transferred to or from the primary across a normally open point. Half-hours are named by the UK local "
          "time at which they end, and the day's peak is its highest half-hour. Design-day demand is established for the "
          "latest complete winter, 2025/26 for this assessment, from the primary's metered record.", BODY),
        P("4. Demand in the winter assessed", H2),
        P("Demand before flexibility in the winter assessed is the latest winter's design-day demand, increased at the "
          "primary's underlying peak growth rates in the Distribution Future Energy Scenarios best view for each year "
          "between the two winters, compounded, plus the demand that the customers on the load growth register will have "
          "added to the primary's demand between the two assessment dates. The register as saved for the assessment is "
          "taken as it stands: an offer counts once it is accepted, a customer not yet energised is taken to be energised "
          "on the date the register holds for it, and offers withdrawn, superseded or only quoted are not counted. Every "
          "customer on the register is half-hourly metered from the day it is energised, and the settlement team's monthly "
          "summary gives each half-hourly metered customer's mean demand between 17:00 and 18:00 on working days. Every "
          "half-hour of the design day is taken to grow in the proportion its highest half-hour grows.", BODY),
        P("5. Firm capacity", H2),
        P("Firm capacity is the capacity the primary keeps with its larger transformer out of service: the winter cyclic "
          "rating of the remaining transformer, expressed in MW at a power factor of 0.95. Appendix A lists it for each "
          "primary.", BODY),
        P("6. Contracted flexibility", H2),
        P("Where a flexibility contract is in place for the winter assessed, demand with flexibility is the design day's "
          "demand with the contracted service instructed in full: the megawatts contracted for that winter in the contract "
          "award notice, scheduled for the whole of the service window. The contract is credited with what the provider's "
          "sites in service on the assessment date can be expected to deliver when so instructed. The flexibility asset "
          "register records every site a provider has signed, the date it passed its commissioning test and its status; a "
          "site is in service from the day it passes that test until it is withdrawn or leaves the service. A contract's "
          "megawatts delivered are quoted as its mean delivery in the half-hours ending 17:30 and 18:00. What a service "
          "delivered is taken only from days on which the primary was in its normal running arrangement. The primary's peak "
          "with flexibility is its highest half-hourly demand on the design day with the service delivered through its "
          "window, whichever half-hour that falls in. No flexibility other than the contracted service is credited.", BODY),
        P("7. Recommendation", H2),
        P("Design days are not alike. From one day to the next a primary's demand runs above or below its usual level for "
          "the temperature, by the same proportion in every half-hour of the day; from one evening to the next a provider "
          "has more or less of its sites' megawatts available, whatever the day's demand; and the load that comes back "
          "after a window varies from one evening to the next. Network Planning recommends that reinforcement be committed "
          "for each primary whose peak with flexibility would exceed its firm capacity on more than one design day in ten, "
          "and reports for each primary the share of design days on which it would. The one day in ten and the share are "
          "taken over those three variations together, as the primary's working weekdays and the provider's completed "
          "events of the three winters on record show them, by drawing not fewer than 100,000 design days; the "
          "assessment's own estimates (design-day demand, what the customers add, the megawatts in service and the share "
          "of them available) are held at their central values. The recommendation is reviewed by the Head of DSO before "
          "the capital expenditure review.", BODY),
        P("Appendix A. Firm capacity", H2),
        T(firm_rows, [46, 24, 42, 34]),
        P("Transformer ratings from the primary substation register; winter cyclic ratings from the 2025 thermal "
          "assessment.", SMALL),
        KeepTogether([P("Document control", H2),
                      T([["Issue", "Date", "Change", "Approved"],
                         ["3", "04/09/2023", "Design condition restated for the Halverton station", "C. Evans"],
                         ["4", "15/09/2025", "Contracted flexibility and the recommendation restated", "C. Evans"],
                         ["5", "22/09/2026", "Assessment date, connections and sites in service restated; Appendix A refreshed",
                          "C. Evans"]], [14, 24, 92, 28]),
                      Spacer(1, 6),
                      P("Owner: Clifford Evans, Head of Network Planning. Reviewer: Marion Todd, Head of DSO.", SMALL)])]
    officepdf.build(os.path.join(target, PK.F_GUIDE), story, "Primary Substation Capacity Assessment: Winter Planning Guideline",
                    "Network Planning", "WPN-NP-G-014 issue 5", "WPN-NP-G-014 issue 5  |  Wealdmoor Power Networks plc",
                    aware("2026-09-22T13:02:41Z"), aware("2026-09-22T13:19:05Z"), producer="LibreOffice 7.6",
                    font="Liberation Sans", page_of=True)


PRICES = {"A": (6.40, 312), "C": (5.85, 296), "D": (6.10, 305), "F": (5.70, 289), "H": (6.65, 318)}


def write_awards(target):
    award = [["Constraint managed zone", "Primary", "Provider", "Contracted MW", "Availability (GBP per MW per hour)",
              "Utilisation (GBP per MWh)"]]
    for z in W.ZONES:
        p = W.BY[z["key"]]
        award.append([PK.ZONE_NAME[z["key"]], p["name"], W.PROVIDERS[z["provider"]]["legal"], "%.1f" % z["mw"]["2027/28"],
                      "%.2f" % PRICES[z["key"]][0], "%d" % PRICES[z["key"]][1]])
    past = [w for w in W.CONTRACT_WINTERS if w != "2027/28"]
    prev = [["Constraint managed zone", "Provider"] + ["%s contracted MW" % w for w in past]]
    for z in W.ZONES:
        prev.append([PK.ZONE_NAME[z["key"]], W.PROVIDERS[z["provider"]]["legal"]] + ["%.1f" % z["mw"][w] for w in past])
    story = letterhead("DSO, Flexibility Services") + [
        P("Flexibility Services: Contract Award Notice, Halverton Constraint Managed Zones, Winter 2027/28", TITLE),
        P("Reference WPN-DSO-FLX-2026-07. Tender issued 14 July 2026, closed 18 September 2026. Contracts run from 1 November "
          "2027 to 31 March 2028.", BODY),
        P("1. Service", H2),
        P("Scheduled peak reduction. Utilisation is instructed by the DSO day-ahead, by 15:30 UK local time, for any working "
          "weekday from 1 November to 31 March, other than bank holidays and the period 24 December to 2 January, on which "
          "the DSO's forecast shows the primary's demand approaching its firm capacity, for the megawatts the forecast shows "
          "are needed, in steps of 0.5 MW from 1.0 MW up to the megawatts contracted. The service window is 16:00 to 19:30 "
          "UK local time. An instruction may be revised or cancelled until 11:00 on the service day. Contracted megawatts "
          "are the capacity the provider has undertaken to make available for instruction in the zone for the winter. The "
          "provider delivers them from sites entered on the flexibility asset register, and a site counts toward delivery "
          "once it has passed its commissioning test.", BODY),
        P("2. Awards", H2),
        T(award, [36, 26, 36, 18, 22, 20]),
        P("Each provider's schedule of sites for these awards was fixed at award. No site may be added to a 2027/28 schedule "
          "after 16 October 2026, and a site the provider withdraws from its schedule is not replaced.", BODY),
        P("3. Payment", H2),
        P("Availability is paid for every working weekday in the contract period on the contracted megawatts for the 3.5 "
          "hours of the service window. Utilisation is paid on the energy the provider delivers in a scheduled window, "
          "measured on the provider's metered assets against the baseline methodology in the service terms, version 3.1.",
          BODY),
        P("4. Previous winters", H2),
        T(prev, [38, 40, 23, 23, 23, 23]),
        P("The service has run at these zones since winter 2023/24 on the same terms. Winter 2026/27 begins on 1 November 2026.", SMALL),
        Spacer(1, 10),
        P("Irene Carpenter, Flexibility Services Manager, 21 October 2026.", BODY)]
    officepdf.build(os.path.join(target, PK.F_AWARD), story,
                    "Flexibility Services: Contract Award Notice, Halverton CMZs, Winter 2027/28", "DSO Flexibility Services",
                    "WPN-DSO-FLX-2026-07", "WPN-DSO-FLX-2026-07  |  Wealdmoor Power Networks plc",
                    aware("2026-10-21T10:44:13Z"), aware("2026-10-21T11:02:56Z"), producer="LibreOffice 7.6",
                    font="Liberation Sans", page_of=True)


def write_duos(target):
    rows = [["Tariff", "Unit rate red (p/kWh)", "Unit rate amber (p/kWh)", "Unit rate green (p/kWh)",
             "Fixed charge (p/day)", "Capacity charge (p/kVA/day)"],
            ["Domestic aggregated", "8.412", "1.106", "0.203", "11.84", ""],
            ["Domestic aggregated with residual", "8.412", "1.106", "0.203", "38.72", ""],
            ["Non-domestic aggregated", "7.958", "1.044", "0.196", "24.61", ""],
            ["LV site specific", "6.217", "0.894", "0.171", "512.30", "4.92"],
            ["LV sub site specific", "4.880", "0.733", "0.142", "498.15", "5.41"],
            ["HV site specific", "3.065", "0.512", "0.104", "6,214.40", "6.87"]]
    bands = [["Time band", "Weekdays (UK local time)", "Weekends"],
             ["Red", "16:00 to 19:00", "None"], ["Amber", "07:30 to 16:00, 19:00 to 21:00", "None"],
             ["Green", "00:00 to 07:30, 21:00 to 24:00", "All day"]]
    story = letterhead("Charging") + [
        P("Statement of Charges for Use of the Distribution System, effective 1 April 2027", TITLE),
        P("Published 31 August 2026 under the conditions of the electricity distribution licence. Charges exclude VAT.", BODY),
        P("1. Time bands", H2),
        T(bands, [30, 70, 40]),
        P("2. Demand tariffs", H2),
        T(rows, [44, 22, 22, 22, 22, 26]),
        P("3. Notes", H2),
        P("Residual charges are allocated by charging band under the targeted charging review. Site-specific capacity "
          "charges apply to the agreed import capacity; excess capacity is charged at the same rate on the excess. Generation "
          "credits and the reactive power charge are set out in the full statement, available on request.", BODY),
        Spacer(1, 6),
        P("Charging and Tariffs, Wealdmoor Power Networks plc.", SMALL)]
    officepdf.build(os.path.join(target, PK.F_DUOS), story, "Statement of Charges for Use of the Distribution System 2027/28",
                    "Charging and Tariffs", "Use of system charges from 1 April 2027",
                    "Use of System Charging Statement 2027/28  |  Wealdmoor Power Networks plc",
                    aware("2026-08-31T08:55:20Z"), aware("2026-08-31T09:07:42Z"), producer="LibreOffice 7.6",
                    font="Liberation Sans", page_of=True)


def write_docs(target):
    write_guideline(target)
    write_awards(target)
    write_duos(target)
