"""The world's constants: Havørn Regional AS, its fleet, bases and route networks, the rotables it pools, the Bodø
component shop, the weather each base keeps, and the 2027 flying schedule. Every figure the pack or the golden
states is computed from these and from the seeded simulation, never typed."""
import datetime as dt

SEED = 41239
ORG = "Havørn Regional AS"
TYPE = "DHC-8-315"
D0 = dt.date(2023, 1, 1)
ASOF = dt.date(2026, 11, 30)          # the stores snapshot and the last day of the exports
EXPORT = dt.date(2026, 12, 1)         # the day the exports were pulled
Y27 = (dt.date(2027, 1, 1), dt.date(2027, 12, 31))
HELGELAND = dt.date(2027, 4, 1)       # the route contract's first day
SB_DATE = dt.date(2024, 10, 7)        # SB 61-0042 issued, embodied at the next shop visit
REPORT_END = dt.date(2026, 10, 31)    # the October reliability report's twelve months end here

PEOPLE = {"director": "Britt Berge", "reliability": "Sigurd Fredriksen", "stores": "Ruth Johannessen",
          "shop": "Sondre Edvardsen", "analyst": "Siri Johansen"}

# Bases: maintenance station, troubleshooting practice (share of symptoms on an intermittent aircraft fault met by
# swapping the unit; chance that troubleshooting a symptom instead finds the aircraft-side fault), the share of a unit's own
# intermittents swapped, climate (January and July mean daily minimum, cold-snap exposure)
BASES = {
    "BOO": {"name": "Bodø", "swap": 0.42, "find": 0.52, "nff_mult": 0.85, "jan": -4.6, "jul": 9.6, "snap": 1.0,
            "ship_days": 0},
    "TOS": {"name": "Tromsø", "swap": 0.81, "find": 0.30, "nff_mult": 1.32, "jan": -6.9, "jul": 8.7, "snap": 1.1,
            "ship_days": 1},
    "BGO": {"name": "Bergen", "swap": 0.74, "find": 0.32, "nff_mult": 1.22, "jan": -1.2, "jul": 11.8, "snap": 0.35,
            "ship_days": 1},
    "TRD": {"name": "Trondheim", "swap": 0.77, "find": 0.31, "nff_mult": 1.26, "jan": -5.1, "jul": 10.6, "snap": 0.6,
            "ship_days": 1},
}

# Each base's route network: (destination, scheduled block minutes, weight); rotations out and back from the base,
# sometimes through a second stop. Flight time is block less taxi (a few minutes at the small fields).
NETWORK = {
    "BOO": [("SVJ", 24, 4), ("LKN", 23, 4), ("RET", 26, 2), ("ANX", 33, 2), ("EVE", 31, 3), ("MQN", 34, 3),
            ("SSJ", 31, 2), ("BNN", 38, 1), ("TOS", 50, 1), ("TRD", 64, 1)],
    "TOS": [("ALF", 41, 4), ("HFT", 40, 4), ("SOJ", 31, 2), ("HAA", 36, 2), ("HVG", 52, 2), ("KKN", 70, 3),
            ("LKL", 47, 2), ("BDU", 29, 1), ("BOO", 56, 3), ("EVE", 45, 1)],
    "BGO": [("FRO", 44, 3), ("FDE", 43, 2), ("SOG", 49, 3), ("HOV", 54, 3), ("SDN", 50, 2), ("AES", 58, 3),
            ("KSU", 67, 2), ("TRD", 72, 2), ("SVG", 57, 3), ("KRS", 83, 1)],
    "TRD": [("OSL", 76, 5), ("BGO", 76, 3), ("BOO", 79, 3), ("TOS", 113, 2), ("KRS", 96, 2), ("AES", 67, 1),
            ("EVE", 98, 1)],
}
LEGS_PER_DAY = {"BOO": 9.0, "TOS": 7.0, "BGO": 5.8, "TRD": 4.2}
# the Helgeland package flown from Bodø from 1 April 2027: short sectors between the region's small fields
HELGELAND_NET = [("SSJ", 22, 3), ("BNN", 21, 2), ("MJF", 18, 3), ("MQN", 22, 2), ("RVK", 26, 1)]
HELGELAND_LEGS = 10.4
TAXI = {"OSL": 11, "BGO": 9, "TRD": 9, "SVG": 8, "EVE": 6, "BOO": 7, "TOS": 7, "KRS": 6, "AES": 6, "KKN": 6, "KSU": 5,
        "MOL": 5}
TAXI_SMALL = 4

FLEET_N = 30
BASE_SPLIT = {"BOO": 11, "TOS": 8, "BGO": 6, "TRD": 5}
# 2027: January to March as November 2026; from 1 April the airline leaves the Trondheim network (lost in the same
# tender round) and flies the Helgeland package from Bodø with eight aircraft: four from Trondheim and four from
# Bergen, the fifth Trondheim aircraft going to Tromsø
BASE_2027_Q1 = {"BOO": 11, "TOS": 8, "BGO": 6, "TRD": 5}
BASE_2027_AP = {"BOO": 19, "TOS": 9, "BGO": 2, "TRD": 0}
HELGELAND_N = 8

# The rotables: key, part number, nomenclature, ATA, positions per aircraft, the exposure that drives its own
# failures ("cyc" landings, "sta" engine starts, "fh" flight hours, "cal" days), confirmed failures per 1,000 units
# of that exposure per position (per position-year for cal), Weibull shape on exposure since the last shop visit,
# cold sensitivity (multiplier slope per degree of daily minimum below 0 C), rogue share, size and kind ("cf" multiplies
# the failure hazard; "nff" adds an intermittent the bench never reproduces, at that many removals an installed year),
# aircraft-side intermittent fault rate per aircraft-year, a unit's own intermittent share (no fault found without an
# aircraft fault), shop ("BOO" or a vendor), repair work hours or vendor repair days, no-fault-found hours or days,
# beyond-economic-repair share, unit price NOK
PARTS = [
    dict(k="SG", pn="23085-016", name="Starter-generator", ata="24", pos=2, drv="sta", rate=0.3, beta=1.25,
         cold=0.035, rogue=(0.02, 14.0, "cf"), fault=0.040, own_nff=0.10, shop="BOO", work=15.5, nff_work=3.2, ber=0.035,
         price=412000),
    dict(k="BRK", pn="2-1577-3", name="Main wheel brake assembly", ata="32", pos=4, drv="cyc", rate=0.185,
         beta=1.55, cold=0.006, rogue=(0.0, 1.0, "cf"), fault=0.0, own_nff=0.05, shop="BOO", work=8.6, nff_work=2.4,
         ber=0.055, price=186000),
    dict(k="BAV", pn="3214552-2", name="Bleed air shutoff valve", ata="36", pos=2, drv="cyc", rate=0.205, beta=1.1,
         cold=0.055, rogue=(0.025, 14.0, "cf"), fault=0.0, own_nff=0.14, shop="BOO", work=10.2, nff_work=2.6, ber=0.04,
         price=164000),
    dict(k="NWS", pn="4405-3", name="Nose wheel steering actuator", ata="32", pos=1, drv="cyc", rate=0.19,
         beta=1.4, cold=0.004, rogue=(0.0, 1.0, "cf"), fault=0.0, own_nff=0.07, shop="BOO", work=11.4, nff_work=2.8,
         ber=0.03, price=238000),
    dict(k="BAT", pn="4078-1", name="Main battery, nickel-cadmium", ata="24", pos=2, drv="cal", rate=1.10,
         beta=1.35, cold=0.045, rogue=(0.0, 1.0, "cf"), fault=0.0, own_nff=0.18, shop="BOO", work=5.4, nff_work=1.6,
         ber=0.09, price=61000),
    dict(k="CPC", pn="7022AJ01", name="Cabin pressure controller", ata="21", pos=1, drv="cyc", rate=0.235,
         beta=1.0, cold=0.0, rogue=(0.03, 8.0, "nff"), fault=0.030, own_nff=0.22, shop="VND", work=23, nff_work=10,
         ber=0.03, price=297000, vendor="Hamar Aero Systems AS", ccy="NOK"),
    dict(k="FLA", pn="12B9010-4", name="Flap drive actuator", ata="27", pos=2, drv="cyc", rate=0.05, beta=1.2,
         cold=0.0, rogue=(0.0, 1.0, "cf"), fault=0.0, own_nff=0.06, shop="VND", work=31, nff_work=12, ber=0.02,
         price=355000, vendor="Motala Aero Repair AB", ccy="EUR"),
    dict(k="ADC", pn="822-1123-002", name="Air data computer", ata="34", pos=2, drv="fh", rate=0.2, beta=1.0,
         cold=0.0, rogue=(0.025, 8.5, "nff"), fault=0.1, own_nff=0.33, shop="VND", work=21, nff_work=9, ber=0.02,
         price=528000, vendor="Avionics Repair Group Ltd", ccy="USD"),
    dict(k="WXR", pn="622-5132-512", name="Weather radar receiver-transmitter", ata="34", pos=1, drv="fh",
         rate=0.4, beta=1.0, cold=0.0, rogue=(0.03, 12.0, "cf"), fault=0.07, own_nff=0.28, shop="VND", work=27,
         nff_work=11, ber=0.025, price=611000, vendor="Avionics Repair Group Ltd", ccy="USD"),
    dict(k="VHF", pn="822-1081-003", name="VHF transceiver", ata="23", pos=2, drv="fh", rate=0.16, beta=1.0,
         cold=0.0, rogue=(0.03, 8.0, "nff"), fault=0.12, own_nff=0.47, shop="VND", work=14, nff_work=7, ber=0.02,
         price=142000, vendor="Avionics Repair Group Ltd", ccy="USD"),
    dict(k="PEC", pn="816534-3", name="Propeller electronic control", ata="61", pos=2, drv="fh", rate=0.60,
         beta=1.0, cold=0.0, rogue=(0.0, 1.0, "cf"), fault=0.0, own_nff=0.12, shop="VND", work=30, nff_work=12,
         ber=0.02, price=489000, vendor="Lier Propeller Services NV", ccy="EUR", sb=0.34),
    dict(k="PDT", pn="3E2210", name="Propeller de-ice timer", ata="30", pos=1, drv="fh", rate=0.235, beta=1.0,
         cold=0.035, rogue=(0.0, 1.0, "cf"), fault=0.0, own_nff=0.24, shop="VND", work=18, nff_work=8, ber=0.03,
         price=88000, vendor="Hamar Aero Systems AS", ccy="NOK"),
    dict(k="HYP", pn="66158-7", name="Engine-driven hydraulic pump", ata="29", pos=2, drv="fh", rate=0.093,
         beta=1.5, cold=0.0, rogue=(0.0, 1.0, "cf"), fault=0.0, own_nff=0.05, shop="VND", work=35, nff_work=12, ber=0.04,
         price=341000, vendor="Motala Aero Repair AB", ccy="EUR"),
    dict(k="FBP", pn="2C7-1", name="Fuel boost pump", ata="28", pos=2, drv="fh", rate=0.107, beta=1.3, cold=0.0,
         rogue=(0.0, 1.0, "cf"), fault=0.0, own_nff=0.08, shop="VND", work=26, nff_work=10, ber=0.03, price=176000,
         vendor="Motala Aero Repair AB", ccy="EUR"),
    dict(k="WHC", pn="1131-4", name="Windshield heat controller", ata="30", pos=2, drv="fh", rate=0.13,
         beta=1.0, cold=0.030, rogue=(0.025, 8.0, "nff"), fault=0.05, own_nff=0.27, shop="VND", work=15, nff_work=7,
         ber=0.03, price=94000, vendor="Hamar Aero Systems AS", ccy="NOK"),
    dict(k="FDU", pn="34-7320-2", name="Engine fire detection control unit", ata="26", pos=1, drv="fh", rate=0.19,
         beta=1.0, cold=0.0, rogue=(0.03, 8.0, "nff"), fault=0.08, own_nff=0.42, shop="VND", work=20, nff_work=8,
         ber=0.02, price=203000, vendor="Avionics Repair Group Ltd", ccy="USD"),
]
PART = {p["k"]: p for p in PARTS}
IN_HOUSE = [p["k"] for p in PARTS if p["shop"] == "BOO"]
# the pool each part number holds at the snapshot: spare units beyond the installed positions
POOL = {"SG": 5, "BRK": 5, "BAV": 4, "NWS": 2, "BAT": 3, "CPC": 4, "FLA": 3, "ADC": 8, "WXR": 7, "VHF": 8,
        "PEC": 7, "PDT": 4, "HYP": 4, "FBP": 4, "WHC": 6, "FDU": 6}

# The Bodø shop: technicians on the roster, productive hours each on a working day, the share of their hours other
# work takes (the third-party component contract, oxygen and fire bottles, emergency equipment), the July holiday
# weeks run on two
SHOP_TECHS = 3
PARTS_WAIT = 8.0                      # days a confirmed repair waits for its piece parts (median)
SHOP_HOURS = 6.9
OTHER_WORK = 0.52
OTHER_WORK_2027 = 0.48                # from April 2027 the shop's third-party contract shrinks as the Helgeland work starts
OTHER_FROM = dt.date(2027, 4, 1)

# the standard's targets
FILL = 0.95
SCRAP_EXCESS = 1.5                    # a serial is scrapped when it is expected to cost this many removals a year
                                      # over a new unit in the same position
FX = {"EUR": 11.62, "USD": 10.71}     # NOK per unit, the invoices' average; each invoice carries its own rate
