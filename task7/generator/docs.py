"""task7 architecture 11: the pack's documents. Each PDF is a Word document exported by LibreOffice Writer (officepdf.py).
They file the WHAT (what the board chooses the default on, what a summer like the last one is, which chargers and which
transformers count, the limit and the replacement costs, how the pilot's managed quarter was drawn and how its results are
reported, the rate's hours) and say nothing of how a transformer's summer peak is estimated under an option."""
import datetime as dt
import os

from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Table

import officepdf
import world as W

MT = dt.timezone(dt.timedelta(hours=-6))
MST = dt.timezone(dt.timedelta(hours=-7))
H1 = ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=14, spaceAfter=6, textColor="#2F4B2F")
H2 = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=10.5, spaceBefore=8, spaceAfter=3, textColor="#2F4B2F")
BODY = ParagraphStyle("b", fontName="Helvetica", fontSize=9.2, spaceAfter=4)
SMALL = ParagraphStyle("s", fontName="Helvetica", fontSize=8, spaceAfter=2, textColor="#444444")
ORG = "Hollins Creek Electric Association"


def P(t, st=BODY):
    return Paragraph(t, st)


def T(rows, widths):
    return Table(rows, colWidths=widths)


def policy(target):
    s = [P(ORG, SMALL), P("Board Policy EV-4: The EV Overnight rate's charging default", H1),
         P("Adopted by the board of directors on 20 February 2025; section 4 revised 17 September 2026.", SMALL),
         P("1 Purpose", H2),
         P("Members on the EV Overnight rate charge their cars at home on networked chargers enrolled with the association's "
           "charging platform. The charging default is how those chargers charge unless the member is told otherwise. This "
           "policy sets how the board chooses it."),
         P("2 The options", H2),
         P("The default is one of three options: the members' own schedules, under which each charger charges as its owner "
           "has set it; or one of the two products the platform offers, as its current proposal describes them."),
         P("3 Choosing the default", H2),
         P("Each November the board sets the default for the following calendar year. It chooses the option with the lowest "
           "cost to the association for that year. An option's cost is the platform's quoted fee for the chargers the quote "
           "covers, plus the replacement cost, under Distribution Planning Standard DPS-7, of each distribution transformer "
           "serving one of those chargers that the option would leave over its limit in a summer like the last one."),
         P("4 A summer like the last one", H2),
         P("4.1 A summer like the last one is July and August of the last summer as metered at the homes each transformer "
           "serves, with every charger the quote covers charging its sessions of that July and August (plugged in, energy "
           "drawn, unplugged) as the option would charge them, each session finishing by the time it was unplugged."),
         P("4.2 Under the members' own schedules a charger charges as its owner set it. A charger that has left the rate is "
           "taken as it was metered."),
         P("4.3 An option's cost is its expected cost."),
         P("5 The work plan", H2),
         P("The transformers the chosen default would leave over their limit are replaced before the next summer and are "
           "carried in that year's construction work plan.")]
    officepdf.build(os.path.join(target, "board_policy_EV-4_charging_default.pdf"), s,
                    "Board Policy EV-4: The EV Overnight rate's charging default", "Board of Directors", "Board Policy EV-4",
                    ORG + " | Board Policy EV-4",
                    dt.datetime(2026, 9, 17, 9, 40, tzinfo=MT), dt.datetime(2026, 9, 18, 8, 55, tzinfo=MT),
                    producer="LibreOffice 25.2", font="Liberation Sans", body_pt=9.2, margin_mm=22, top_mm=20, bottom_mm=18)


def standard(target):
    rows = [["Unit in service", "Replaced by", "Installed cost"]]
    for kva in (25.0, 37.5, 50.0, 75.0, 100.0):
        mount = "pole-mount" if kva <= 37.5 else "pad-mount"
        rows.append(["%g kVA %s" % (kva, mount), "%g kVA %s" % (W.NEXT[kva], "pole-mount" if W.NEXT[kva] <= 50 and kva <= 37.5 else "pad-mount"),
                     "$%s" % format(W.COST[kva], ",")])
    s = [P(ORG + ", Engineering", SMALL), P("Distribution Planning Standard DPS-7: Distribution transformer loading", H1),
         P("Revision 4, 3 November 2025. Owner: Sandra Bernard, engineering supervisor.", SMALL),
         P("1 Scope", H2),
         P("This standard sets when a single-phase distribution transformer serving residential load is over its limit and "
           "what replacing it costs, for the construction work plan and for any board policy that relies on it."),
         P("2 The limit", H2),
         P("2.1 A transformer is over its limit in a summer when its highest 15-minute load in July and August exceeds 120 "
           "per cent of its nameplate kVA."),
         P("2.2 A transformer's load in a 15-minute interval is the demand of the homes it serves in that interval. For "
           "planning, load in kVA is that demand in kW divided by 0.95, whether or not the transformer is monitored."),
         P("2.3 The nameplate is that of the unit in service at the date of the study."),
         P("3 Replacement", H2),
         P("A transformer over its limit is replaced by the next standard size before the following summer, at the installed "
           "cost below (crew, unit, connections and disposal)."),
         T(rows, [140, 140, 90]),
         P("4 Records", H2),
         P("Connectivity is taken from the GIS as corrected by completed work orders; a unit's nameplate from the transformer "
           "register as corrected by completed change-outs.")]
    officepdf.build(os.path.join(target, "dps-7_distribution_transformer_loading.pdf"), s,
                    "DPS-7 Distribution transformer loading", "Sandra Bernard", "Distribution Planning Standard DPS-7",
                    ORG + " | Engineering",
                    dt.datetime(2025, 11, 3, 14, 5, tzinfo=MST), dt.datetime(2025, 11, 4, 10, 18, tzinfo=MST),
                    producer="LibreOffice 24.8", font="Carlito", body_pt=9.5, margin_mm=20, top_mm=18, bottom_mm=18)


def pilot_plan(target):
    s = [P(ORG + ", Member Programs", SMALL), P("EV Overnight managed charging pilot, 2025 and 2026", H1),
         P("Issued 28 April 2025 by Chad Wyatt, pilot manager.", SMALL),
         P("1 Design", H2),
         P("On 12 May 2025 the platform draws one in four of the chargers then enrolled on the EV Overnight rate, at random, "
           "for its Stagger product. A charger enrolled after that day is drawn the same way when it enrols. The other three "
           "in four keep charging on their owners' own schedules. A member in the managed quarter sets a ready-by time in "
           "the app and cannot pause a managed session."),
         P("2 Data", H2),
         P("The platform reads every enrolled charger, managed or not, and keeps each session's plug-in, start, end and "
           "unplug times and its energy. The meter data system keeps every member's hourly reads. In 2024 the association "
           "fitted 15-minute load monitors to 48 distribution transformers chosen at random within each size class."),
         P("3 Results", H2),
         P("The pilot's results are reported per enrolled charger, averaged over every night of July and August whether the "
           "car was plugged in or not, the managed quarter against the chargers on their owners' own schedules."),
         P("4 Enrolment", H2),
         P("Enrolment on the EV Overnight rate pauses on 1 June 2026 and reopens once the board has set the default for "
           "2027 under Board Policy EV-4.")]
    officepdf.build(os.path.join(target, "ev_overnight_pilot_plan_2025.pdf"), s,
                    "EV Overnight managed charging pilot", "Chad Wyatt", "Pilot plan", ORG + " | Member Programs",
                    dt.datetime(2025, 4, 28, 11, 20, tzinfo=MT), dt.datetime(2025, 4, 28, 15, 2, tzinfo=MT),
                    producer="LibreOffice 24.8", font="DejaVu Sans", body_pt=9.0, margin_mm=24, top_mm=20, bottom_mm=20)


def rate_schedule(target):
    rows = [["Period", "Hours", "Energy charge"],
            ["Off-peak", "23:00 to 07:00, every day", "$0.068 per kWh"],
            ["On-peak", "15:00 to 19:00, weekdays June to September", "$0.284 per kWh"],
            ["Standard", "all other hours", "$0.121 per kWh"],
            ["Monthly service charge", "", "$19.50"]]
    s = [P(ORG, SMALL), P("Rate Schedule EV-1: EV Overnight", H1), P("Effective 1 January 2026", SMALL),
         P("Availability", H2),
         P("To residential members who charge an electric vehicle at home on a networked Level 2 charger enrolled with the "
           "association's charging platform. At enrolment the member says how the car usually charges."),
         T(rows, [110, 200, 90]),
         P("Charges are billed on the member's hourly meter reads. The charging default under Board Policy EV-4 applies to "
           "every enrolled charger.", SMALL),
         P("Prepared by Rebekah Fleming, rates analyst.", SMALL)]
    officepdf.build(os.path.join(target, "rate_schedule_EV-1_2026.pdf"), s, "Rate Schedule EV-1: EV Overnight",
                    "Rebekah Fleming", "Rate Schedule EV-1", ORG + " | Rates",
                    dt.datetime(2025, 12, 4, 16, 30, tzinfo=MST), dt.datetime(2025, 12, 9, 9, 12, tzinfo=MST),
                    producer="LibreOffice 24.8", font="Liberation Sans", body_pt=9.4, margin_mm=20, top_mm=18, bottom_mm=18)


def write_all(target, w):
    policy(target)
    standard(target)
    pilot_plan(target)
    rate_schedule(target)
