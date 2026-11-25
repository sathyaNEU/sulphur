"""The fiction's constants: Cottonwood Draw Electric Cooperative, a fictional rural electric cooperative in south-central
Kansas, its summer air-conditioner load-management programme and the 2026 dispatch trial. The world itself (every
switch, every event, every step) is generator/core.py's; this file holds the names, the calendar and the clocks the
files are written in."""
import datetime as dt

import numpy as np

import core

SEED = core.SEED
ORG = "Cottonwood Draw Electric Cooperative, Inc."
ORG_SHORT = "Cottonwood Draw Electric Cooperative"
SUPPLIER = "Sunflower Basin Power Cooperative"
CARRIER = "TriCounty Paging LLC"
COUNTY = "Harlan Bend County"
CDT = dt.timezone(dt.timedelta(hours=-5))
CST = dt.timezone(dt.timedelta(hours=-6))
UTC = dt.timezone.utc

PEOPLE = {
    "energy": "Peter Mitchell",       # energy services manager (the golden's author)
    "ops": "Timothy Powell",          # operations superintendent: radio shop and SCADA
    "member": "Caleb Mclean",         # member services: the switch register
    "finance": "Emily Maldonado",     # finance: the work plan's appraisal constants
    "gm": "Alejandra Williams",       # general manager, signs the work plan
    "radio": "Kelsey Mercer",         # radio shop technician, keeps the outage log
    "radio2": "Jacob Johnson",        # radio shop technician
    "scada": "James Warren",          # SCADA administrator
    "billing": "Shelly Davis",        # supplier's member billing
    "eval": "Christopher Ortega",     # the load research contractor's analyst
}
TECHS = ["Luke Torres", "Brian Thompson", "Dustin Mcknight", "Bradley Mueller", "Brandon Martinez", "Gregory Preston",
         "Matthew Malone", "Stephen Ellis", "Derek Smith", "Charles Hammond", "Jason Sanchez", "Ronald Allen"]
CONTRACTORS = ["Mueller Heating & Air", "Hammond Mechanical", "Preston Comfort Systems", "Galvan HVAC Service",
               "Sparks Heating & Cooling", "Huber Plumbing & Heating", "Frey Refrigeration", "Duran Air Conditioning",
               "Mathis & Sons Mechanical", "Blair Climate Control", "Chambers Heating", "Flores Air LLC"]

DISTRICTS = ["Larkin", "Medora Flats", "Halverson", "Pruett"]
TOWNS = {0: ("Larkin", (0.4, -0.3)), 1: ("Medora Flats", (-14.6, 0.4)), 2: ("Halverson", (4.6, 20.8)), 3: ("Pruett", (24.2, -2.6))}
# substations by district, in the order core's feeders run (the West district's feeders run outward from town)
SUBSTATIONS = {0: [("LKN", "Larkin North", 5), ("LKS", "Larkin South", 4), ("CTW", "Cottonwood", 4)],
               1: [("MDF", "Medora Flats", 4), ("ANT", "Antelope", 4), ("SDH", "Sandhill", 4)],
               2: [("HAL", "Halverson", 4), ("OST", "Ostrander", 4), ("BLF", "Bluff City", 3)],
               3: [("PRU", "Pruett", 4), ("ELM", "Elm Mills", 3), ("CDR", "Cedar Draw", 3)]}
# the two Pruett feeders whose SCADA points were renamed when the Pruett substation was rebuilt
RENAMED = {"PRU-2": "PRUETT_T2.FDR22.KW", "PRU-3": "PRUETT_T2.FDR23.KW"}
RENAME_AT = dt.datetime(2026, 7, 14, 9, 40, tzinfo=CDT)

# the paging systems: the cooperative's own VHF (core's vt) and the carrier's FLEX 900 MHz (core's ct)
VHF_SITES = [("VHF-01", "Headquarters", "Larkin HQ tower"), ("VHF-02", "Medora Flats substation", "MF sub stick"),
             ("VHF-03", "Halverson substation", "Hal sub VHF")]
FLEX_SITES = [("TCP-104", "Larkin water tower", "TCP Larkin"), ("TCP-117", "Sandhill", "TCP Sandhill"),
              ("TCP-121", "Ostrander", "TCP Ostrander"), ("TCP-133", "Pruett", "TCP Pruett"),
              ("TCP-109", "Bluestem", "TCP Bluestem")]
VHF_FREQ = "VHF 153.875 MHz"
FLEX_FREQ = "FLEX 929.6125 MHz"
# the proposals (core's members), in the work plan's order
PROPOSALS = [("rep_w", "LM-27-01", "Kettle Ridge VHF repeater"), ("rep_n", "LM-27-02", "Halverson carrier fill-in site"),
             ("fix_t", "LM-27-03", "Larkin find-and-fix round"), ("fix_w", "LM-27-04", "Medora Flats find-and-fix round"),
             ("recon_in", "LM-27-05", "Reconnection round within 14 km"), ("recon_out", "LM-27-06", "Outlying reconnection round")]

# ---- the summer of 2026 -----------------------------------------------------------------------------------------
SUMMER0, SUMMER1 = dt.date(2026, 6, 1), dt.date(2026, 9, 30)
WEEKDAYS = [SUMMER0 + dt.timedelta(d) for d in range((SUMMER1 - SUMMER0).days + 1)
            if (SUMMER0 + dt.timedelta(d)).weekday() < 5]
HOLIDAYS = {dt.date(2026, 7, 3), dt.date(2026, 9, 7)}
EVENTS_PER_MONTH = {6: 15, 7: 16, 8: 15, 9: 14}
PEAK_EVENTS = (2, 19, 45, 55)       # the supplier's coincident-peak afternoons are these event days
PEAK_HOUR = {2: 17, 19: 18, 45: 17, 55: 16}   # hour beginning, local
W_DEC = 3                           # the supplier publishes its cooling index to three decimals


def calendar():
    """The 60 event days among the 88 summer weekdays, in core's event order, holidays never called. Drawn once,
    seeded; asserted against the outage, commissioning and peak-day placements in checks.py."""
    r = np.random.default_rng(SEED + 101)
    days = []
    for mo, k in EVENTS_PER_MONTH.items():
        pool = [d for d in WEEKDAYS if d.month == mo and d not in HOLIDAYS]
        pick = sorted(r.choice(len(pool), k, replace=False))
        days += [pool[i] for i in pick]
    assert len(days) == core.N_EVENTS
    return days


EVENT_DAYS = calendar()
NON_EVENT = [d for d in WEEKDAYS if d not in set(EVENT_DAYS)]
FLEET_MIN0 = 60                     # the first fleet command, minutes after 15:00 local (16:00)
STUDY_SHED = (45, 225)              # the study homes' shed and restore, minutes after 15:00 local (15:45 and 18:45)
RESTORE_MIN = 240                   # the fleet's restores begin at 19:00 local, one group a minute
WINDOW = 5                          # the golden's step: the five minutes after the transmit minute less the five before

AS_OF = dt.date(2026, 11, 23)       # the analysis is done for the December board
REGISTER_AT = dt.date(2026, 9, 30)  # the register, the transmitter list and the replaced-unit records as of this date
