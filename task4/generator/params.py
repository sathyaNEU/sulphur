"""task4 architecture 5: the world's fixed facts. Fryele Akeri AB, a road haulier in Smaland, ran a battery-electric
pilot from its Jonkoping depot from March 2025 and orders battery-electric tractors for its Varnamo terminal's duties
from January 2027. Nothing here is shipped as written; pack.py and docs.py write the files from it."""
import datetime as dt

SEED = 5405
ORG = "Fryele Åkeri AB"
DOMAIN = "fryeleakeri.se"
AS_OF = dt.date(2026, 11, 6)

# the truth of a battery-electric 64-tonne combination's battery energy per km (kWh), never shipped
E0 = 0.86          # base, at 16 C and above, flat road, empty
CLIMB = 0.0028     # per metre of climb per 100 km of route
COLD1 = 0.0100     # per degree C below 16 (cab heating, rolling resistance, air density)
COLD2 = 0.0240     # battery and cab conditioning below about freezing, a smooth curve (sim.cond), per degree
COLD2_T0 = 1.5     # where the conditioning curve is centred (C)
COLD2_S = 2.2      # how gradually it comes in (C)
LOAD = 0.0215      # per tonne of payload per loaded km
EPS = 0.030        # trip-to-trip noise (driver, traffic, wind), multiplicative
ROUTE_SD = 0.006   # each duty's own route effect beyond its climb, multiplicative

AERO = 0.046      # air drag: kWh per km per 1000 (km/h)^2 of average speed above the reference
V_REF = 65.0       # the speed at which E0 holds
# the routing tool's planned speed is optimistic, and more so on winter roads: actual = planned x ratio(T) x noise
R0 = 0.945         # actual over planned on mild days
RC = 0.0085        # the ratio's fall per degree below about 10 C, a smooth curve (sim.ratio)
RT, RS = 10.0, 3.0
R_SD = 0.03        # day-to-day spread of the ratio (traffic, roadworks, the driver)

DESIGN_T = -5.0    # FES-2 4.1, the January design day
USABLE_2027 = 540.0  # the dealer's quotation, usable battery of the 2027 tractor
SHARE = 0.85       # FES-2 4.3
FADE_Y1 = 0.039    # share of usable capacity a pilot battery permanently loses in its first year (never shipped)
FADE_TRACTOR_SD = 0.002   # tractor-to-tractor spread of that first-year loss
CAP_COLD = 0.0030  # apparent capacity lost per degree C below 20 on the day (cold cells, voltage sag), recovers
LIMIT = SHARE * USABLE_2027 * (1 - FADE_Y1)

# shippers: code, name, town, declaration practice (never shipped), mean and sd of a full load's net payload (t)
# est: the clerk's estimate from the order (scatters around the weighed load); std: one standard load weight declared
# for every full load (the weighed load scatters around it); exact: the shipper's own weighbridge ticket
SHIPPERS = {
    "TEN": ("Tenhult Möbler AB", "Tenhult", "est", 11.4, 1.25),
    "HWP": ("Huskvarna Wellpapp AB", "Huskvarna", "est", 10.8, 1.20),
    "BMJ": ("Bankeryds Mejeri ek. för.", "Bankeryd", "std", 13.4, 1.40),
    "TTV": ("Tabergs Trävaror AB", "Taberg", "exact", 13.9, 1.50),
    "GDR": ("Gränna Dryckes AB", "Gränna", "est", 13.6, 1.30),
    "LBY": ("Lekeryds Byggvaror AB", "Lekeryd", "est", 12.4, 1.30),
    "GST": ("Gnosjö Stålcenter AB", "Gnosjö", "est", 29.0, 2.10),
    "SKB": ("Skillingaryds Ballast AB", "Skillingaryd", "exact", 32.0, 1.60),
    "HIL": ("Hillerstorps Metall AB", "Hillerstorp", "est", 26.5, 2.00),
    "VIS": ("Värnamo Isolering AB", "Värnamo", "est", 4.6, 0.70),
    "BPL": ("Bredaryds Plast AB", "Bredaryd", "est", 7.6, 1.10),
    "RPA": ("Rydaholms Pall AB", "Rydaholm", "std", 9.1, 1.20),
    "FGU": ("Forsheda Gummi AB", "Forsheda", "est", 12.6, 1.50),
    "RTR": ("Reftele Trä AB", "Reftele", "exact", 18.4, 1.90),
    "ANE": ("Anderstorps Elektronik AB", "Anderstorp", "est", 5.4, 0.80),
    "KCY": ("Kulltorps Cykel AB", "Kulltorp", "est", 3.9, 0.60),
    "VGL": ("Vaggeryds Glas AB", "Vaggeryd", "est", 21.0, 1.80),
}
STD_LOAD = {"BMJ": 540, "RPA": 360}   # the standard weight per pallet each std shipper writes, times the pallets on the note
EST_SD = 0.22     # the estimating clerks' relative error (mean zero)
# Granna Dryckes put a platform scale on its loading dock: from this date its notes carry the scale's weight
SCALE_FROM = {"GDR": dt.date(2026, 8, 17)}

# the Jonkoping pilot duties: code, shipper, (empty out, loaded, empty back) km, climb m per 100 km, delivery town
PILOT = {
    "J01": ("TEN", (14, 106, 96), 46, "Linköping"),
    "J02": ("TEN", (14, 96, 92), 38, "Tranås"),
    "J03": ("HWP", (9, 112, 104), 30, "Borås"),
    "J04": ("HWP", (9, 102, 104), 52, "Växjö"),
    "J05": ("BMJ", (16, 106, 98), 34, "Hultsfred"),
    "J06": ("VGL", (12, 98, 92), 42, "Kalmar"),
    "J07": ("GDR", (38, 104, 70), 28, "Motala"),
    "J08": ("GDR", (30, 100, 90), 44, "Vimmerby"),
    "J09": ("LBY", (21, 112, 108), 36, "Värnamo"),
}
# the routing tool's planned average speed over the round trip (km/h): the pilot's regional routes and the Varnamo
# shortlist's long runs, mostly on the E4, E6, 25 and 27
PILOT_V = {"J01": 68, "J02": 62, "J03": 66, "J04": 63, "J05": 64, "J06": 67, "J07": 61, "J08": 65, "J09": 69}
SHORT_V = {"V03": 79, "V07": 77, "V11": 80, "V14": 78, "V18": 81, "V02": 76, "V05": 82, "V09": 83, "V16": 81,
           "V21": 80, "V24": 74, "V27": 79, "V30": 81, "V33": 75}
PILOT_START = dt.date(2025, 3, 3)
PILOT_END = dt.date(2026, 10, 30)
PILOT_TRACTORS = ["BEV-01", "BEV-02", "BEV-03", "BEV-04", "BEV-05", "BEV-06"]
PILOT_USABLE = 520.0
PILOT_IN_SERVICE = dt.date(2025, 2, 17)

# the Varnamo duties on the 2027 shortlist: shipper, (empty out, loaded, empty back) km, climb, delivery town
# the km are set by sim.shortlist_km so each duty's design-day energy sits where the design puts it
SHORT = {
    "V03": ("GST", 36, "Helsingborg", "hi"),
    "V07": ("SKB", 40, "Linköping", "hi"),
    "V11": ("HIL", 32, "Kristianstad", "hi"),
    "V14": ("VIS", 30, "Karlskrona", "lo"),
    "V18": ("ANE", 40, "Alingsås", "ok"),
    "V02": ("KCY", 32, "Kalmar", "ok"),
    "V05": ("BPL", 42, "Ängelholm", "ok"),
    "V09": ("VGL", 30, "Göteborg", "ok"),
    "V16": ("RPA", 38, "Varberg", "ok"),
    "V21": ("RTR", 30, "Malmö", "no"),
    "V24": ("VGL", 44, "Oskarshamn", "no"),
    "V27": ("GDR", 34, "Trollhättan", "no"),
    "V30": ("BMJ", 40, "Uddevalla", "no"),
    "V33": ("KCY", 34, "Västervik", "no"),
}
# each duty's true design-day energy (kWh), set so the duty sits where the order's design puts it
TARGET = {"V02": 414.4, "V03": 456.2, "V05": 430.5, "V07": 464.9, "V09": 405.9, "V11": 457.5, "V14": 438.6, "V16": 415.8, "V18": 430.0, "V21": 476.4, "V24": 478.4, "V27": 476.3, "V30": 463.0, "V33": 485.0}

WB_START = dt.date(2024, 11, 1)
WB_END = dt.date(2026, 10, 30)
LAST12 = (dt.date(2025, 11, 1), dt.date(2026, 10, 31))
TMS_UPGRADE = dt.date(2026, 4, 13)   # duty codes re-keyed (VMO-07 -> V07) at the TMS upgrade

HOLIDAYS = {dt.date(*d) for d in [
    (2024, 12, 24), (2024, 12, 25), (2024, 12, 26), (2024, 12, 31), (2025, 1, 1), (2025, 1, 6), (2025, 4, 18),
    (2025, 4, 21), (2025, 5, 1), (2025, 5, 29), (2025, 6, 6), (2025, 6, 20), (2025, 12, 24), (2025, 12, 25),
    (2025, 12, 26), (2025, 12, 31), (2026, 1, 1), (2026, 1, 6), (2026, 4, 3), (2026, 4, 6), (2026, 5, 1),
    (2026, 5, 14), (2026, 6, 19)]}


def workdays(a, b):
    d = a
    out = []
    while d <= b:
        if d.weekday() < 5 and d not in HOLIDAYS and not (d.month == 7 and 7 <= d.day <= 25):
            out.append(d)
        d += dt.timedelta(days=1)
    return out
