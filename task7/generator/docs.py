"""task7 architecture 10: the pack's documents. Each PDF is a Word document exported by LibreOffice Writer (officepdf.py).
They file the WHAT (what the board renews on, what a reduction is, which intervals and which devices, the rate, how the
test events are drawn and what the research sample is, what an event does to a thermostat) and say nothing of how an
impact is estimated, carried to the peak days, to next summer's devices or to the fleet's homes."""
import datetime as dt
import os

from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Table

import officepdf
import world as W

CT = dt.timezone(dt.timedelta(hours=-5))
CST = dt.timezone(dt.timedelta(hours=-6))
H1 = ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=14, spaceAfter=6, textColor="#22415E")
H2 = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=10.5, spaceBefore=8, spaceAfter=3, textColor="#22415E")
BODY = ParagraphStyle("b", fontName="Helvetica", fontSize=9.2, spaceAfter=4)
SMALL = ParagraphStyle("s", fontName="Helvetica", fontSize=8, spaceAfter=2, textColor="#444444")


def P(t, st=BODY):
    return Paragraph(t, st)


def T(rows, widths):
    return Table(rows, colWidths=widths)


def hhmm(m):
    return "%d:%02d" % divmod(int(m), 60)


def policy(target):
    s = [P("Cedar Brake Electric Cooperative", SMALL), P("Board Policy 412: Demand-response providers", H1),
         P("Adopted by the board of directors on 24 October 2023; section 4 revised 17 March 2026.", SMALL),
         P("1 Purpose", H2),
         P("ERCOT allocates the transmission cost of its system to each distribution service provider on that provider's "
           "load in the four 15-minute intervals in which ERCOT's own load peaked in June, July, August and September of "
           "the year before (the 4CP intervals). The co-op pays its wholesale transmission charge on its average load in "
           "those four intervals. Peak Partners, the co-op's bring-your-own-thermostat programme, lowers that load: on "
           "the days the co-op expects a 4CP interval it asks the members' thermostats, through the providers that "
           "connect them, to run warmer for a few hours."),
         P("2 Providers", H2),
         P("A provider is a thermostat company whose platform dispatches the co-op's events to the thermostats its "
           "members enrolled. Each provider runs the event its own way, within the settings it files with the co-op each "
           "summer, and is paid a price per enrolled device for the summer, which includes the member's incentive."),
         P("3 Renewal", H2),
         P("The board renews a provider's contract for a summer when the transmission cost its devices are expected to "
           "save that summer is more than the co-op would pay the provider for them."),
         P("4 The saving", H2),
         P("4.1 The saving is the provider's reduction of the co-op's load in the 4CP intervals, averaged over the four, "
           "times the transmission rate in the co-op's current notice."),
         P("4.2 The reduction in an interval is what the co-op's load would have been in that interval without the "
           "provider's event, less what it was. It is counted per device enrolled with the provider on 1 July of the "
           "summer, whether or not the device takes part in a given event."),
         P("4.3 A summer is judged as one like the last three: over the twelve 4CP intervals of the three summers before "
           "it, with the co-op calling its 4CP alerts as it called them on those days, and each provider running its "
           "event with the settings it has quoted."),
         P("5 What the co-op pays", H2),
         P("The co-op pays the provider's quoted price per device enrolled on 1 July, for the summer."),
         P("6 Review", H2),
         P("Energy Programs brings the providers' quotes and its appraisal to the board's November meeting each year.")]
    officepdf.build(os.path.join(target, "board_policy_412_demand_response_providers.pdf"), s,
                    "Board Policy 412: Demand-response providers", "Charles Hardin", "Board Policy 412",
                    "Cedar Brake Electric Cooperative | Board Policy 412",
                    dt.datetime(2026, 3, 17, 10, 4, tzinfo=CT), dt.datetime(2026, 3, 18, 9, 12, tzinfo=CT),
                    producer="LibreOffice 25.2", font="Liberation Sans", body_pt=9.2, margin_mm=22, top_mm=20,
                    bottom_mm=18)


def rate_notice(target):
    rows = [["Charge", "Basis", "Rate from 1 January 2027"],
            ["Transmission (TCOS pass-through)", "per kW of 4CP load, a year", "$%.2f" % W.RATE],
            ["Wholesale energy", "per kWh", "per the power supply agreement"]]
    s = [P("Cedar Brake Electric Cooperative, Finance and Rates", SMALL),
         P("Wholesale transmission charge for 2027", H1),
         P("28 October 2026", SMALL),
         P("ERCOT published the 2026 4CP intervals on 15 October 2026. The co-op's 2027 transmission charge is set on its "
           "average load in those four intervals at the rate below, billed in twelve equal monthly amounts through the "
           "co-op's wholesale power supplier."),
         T(rows, [170, 150, 150]),
         P("The rate is the one the board's appraisals use for 2027."),
         P("Prepared by Matthew Santos, rates analyst.", SMALL)]
    officepdf.build(os.path.join(target, "transmission_charge_notice_2027.pdf"), s,
                    "Wholesale transmission charge for 2027", "Matthew Santos", "Transmission charge 2027",
                    "Cedar Brake Electric Cooperative | Finance and Rates",
                    dt.datetime(2026, 10, 28, 15, 40, tzinfo=CT), dt.datetime(2026, 10, 28, 16, 2, tzinfo=CT),
                    producer="LibreOffice 25.8", font="Carlito", body_pt=9.5, margin_mm=20, top_mm=18, bottom_mm=18)


def mv_plan(target):
    s = [P("Cedar Brake Electric Cooperative, Energy Programs", SMALL),
         P("Peak Partners: measurement and verification plan, 2024 to 2026", H1),
         P("Issued 14 May 2024 by Renee Henry, manager of energy programs.", SMALL),
         P("1 Test events", H2),
         P("Each summer the co-op calls eight test events on weekdays in June to September, none on a day with a 4CP "
           "alert or next to one. On each test event the co-op divides every provider's enrolled devices into two halves "
           "at random, calls one half and holds the other back; the assignment is kept in the event assignment file. "
           "Each provider runs a test event as it runs any other event."),
         P("2 4CP alerts", H2),
         P("On the weekdays the co-op's 4CP forecast flags, it calls every enrolled device. No device is held back on an "
           "alert day."),
         P("3 The research sample", H2),
         P("The co-op fitted 15-minute interval meters on the Marble Ridge North and Liberty Grove substations in 2023. "
           "The research sample is the Peak Partners homes on those meters that enrolled before 1 June 2024. The co-op "
           "exports their 15-minute reads, 13:00 to 21:00, on every event day and on eight weekdays each summer without "
           "an event. Every other member's meter records hourly and is not exported for the programme."),
         P("4 Provider reports", H2),
         P("After each event each provider sends its report: a row for each device it dispatched and what happened to "
           "it, in the provider's own layout. The roster of enrolled devices is the co-op's."),
         P("5 Results", H2),
         P("Energy Programs reports each summer's results to the board with the providers' quotes for the next summer.")]
    officepdf.build(os.path.join(target, "peak_partners_mv_plan_2024.pdf"), s,
                    "Peak Partners: measurement and verification plan", "Renee Henry", "M&V plan",
                    "Cedar Brake Electric Cooperative | Energy Programs",
                    dt.datetime(2024, 5, 14, 11, 20, tzinfo=CT), dt.datetime(2024, 5, 14, 13, 2, tzinfo=CT),
                    producer="LibreOffice 24.2", font="DejaVu Sans", body_pt=9.0, margin_mm=24, top_mm=20,
                    bottom_mm=20)


def guide(target):
    rows = [["Provider", "Event window", "Pre-cool", "Setback"]]
    for p in W.PROVIDERS:
        q = W.PROG[p]
        rows.append([p, "%s to %s" % (hhmm(q["s"]), hhmm(q["e"])), ("%d minutes" % q["pre"]) if q["pre"] else "none",
                     "%d F" % q["d"]])
    s = [P("Peak Partners", SMALL), P("How a Peak Partners event works", H1),
         P("Member and provider guide, summer 2026", SMALL),
         P("When the co-op calls an event, your thermostat company sends your thermostat the event. For the event window "
           "your thermostat runs a few degrees warmer than your own setting, and some companies cool your home a little "
           "before the window starts. When the window ends your thermostat goes back to your own setting."),
         P("You can leave an event at any time by changing the temperature on the thermostat or in the app. Your "
           "thermostat then goes back to your own setting for the rest of the window."),
         P("Your thermostat has to be connected to your home's wifi to receive an event. If it is not connected when the "
           "event is sent, it runs as normal."),
         P("Event settings for summer 2026", BODY),
         T(rows, [120, 110, 90, 70]),
         P("Your incentive is paid by your thermostat company each summer you stay enrolled.")]
    officepdf.build(os.path.join(target, "peak_partners_member_guide_2026.pdf"), s,
                    "How a Peak Partners event works", "Mary Hampton", "Member and provider guide",
                    "Peak Partners | Cedar Brake Electric Cooperative",
                    dt.datetime(2026, 4, 22, 9, 30, tzinfo=CT), dt.datetime(2026, 4, 23, 14, 11, tzinfo=CT),
                    producer="LibreOffice 25.2", font="Liberation Sans", body_pt=9.4, margin_mm=20, top_mm=18,
                    bottom_mm=18)


def study(target):
    rows = [["Programme type", "Typical reduction per device, first event hour", "Cost per kW-year"],
            ["Utility-installed thermostat", "1.0 to 1.4 kW", "$45 to $80"],
            ["Bring your own thermostat", "0.7 to 1.1 kW", "$35 to $70"],
            ["Peak-time rebate (behavioural)", "0.1 to 0.3 kW", "$60 to $140"]]
    s = [P("Gulf and Plains Energy Research", SMALL),
         P("Residential demand response in ERCOT: potential to 2030", H1),
         P("Summary report, September 2025", SMALL),
         P("This study estimates the residential summer demand response that ERCOT's distribution service providers "
           "could enrol by 2030, from a survey of 31 programmes and the housing stock of each weather zone."),
         T(rows, [170, 170, 110]),
         P("Programme results vary with the event design, the climate and the homes enrolled. The study's ranges are "
           "drawn from programme evaluations filed between 2019 and 2024 and are not adjusted to any one utility."),
         P("Potential by weather zone, 2030: Coast 410 MW, North Central 520 MW, South Central 360 MW, West 90 MW.")]
    officepdf.build(os.path.join(target, "ercot_residential_dr_potential_2025.pdf"), s,
                    "Residential demand response in ERCOT: potential to 2030", "Gulf and Plains Energy Research",
                    "Summary report", "Gulf and Plains Energy Research | Summary report",
                    dt.datetime(2025, 9, 9, 8, 15, tzinfo=CT), dt.datetime(2025, 9, 9, 8, 50, tzinfo=CT),
                    producer="LibreOffice 25.2", font="DejaVu Sans", body_pt=9.0, margin_mm=25, top_mm=22,
                    bottom_mm=22)


def write_all(target, w):
    policy(target)
    rate_notice(target)
    mv_plan(target)
    guide(target)
    study(target)
