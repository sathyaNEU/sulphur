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
COLD1 = 0.0110     # per degree C below 16 (cab heating, rolling resistance, air density)
COLD2 = 0.0120     # a further rate per degree C below 0 (battery conditioning)
LOAD = 0.0215      # per tonne of payload per loaded km
EPS = 0.030        # trip-to-trip noise (driver, traffic, wind), multiplicative
ROUTE_SD = 0.012   # each duty's own route effect beyond its climb, multiplicative

DESIGN_T = -5.0    # FES-2 4.1, the January design day
USABLE_2027 = 540.0  # the dealer's quotation, usable battery of the 2027 tractor
SHARE = 0.85       # FES-2 4.3
LIMIT = SHARE * USABLE_2027

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
STD_LOAD = {"BMJ": 13500, "RPA": 9000}   # the standard full-load weight each std shipper writes on every note
EST_SD = 0.17     # the estimating clerks' relative error (mean zero)

# the Jonkoping pilot duties: code, shipper, (empty out, loaded, empty back) km, climb m per 100 km, delivery town
PILOT = {
    "J01": ("TEN", (14, 162, 150), 46, "Norrköping"),
    "J02": ("TEN", (14, 141, 128), 38, "Linköping"),
    "J03": ("HWP", (9, 155, 146), 30, "Borås"),
    "J04": ("HWP", (9, 128, 133), 52, "Växjö"),
    "J05": ("BMJ", (16, 150, 136), 34, "Hultsfred"),
    "J06": ("TTV", (12, 146, 140), 42, "Kalmar"),
    "J07": ("GDR", (38, 118, 82), 28, "Motala"),
    "J08": ("GDR", (38, 134, 128), 44, "Västervik"),
    "J09": ("LBY", (21, 160, 158), 36, "Halmstad"),
}
PILOT_START = dt.date(2025, 3, 3)
PILOT_END = dt.date(2026, 10, 30)
PILOT_TRACTORS = ["BEV-01", "BEV-02", "BEV-03", "BEV-04", "BEV-05", "BEV-06"]
PILOT_USABLE = 468.0

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
# target margin of the truth design-day energy against the limit (kWh): hi heavy duties just above, lo light duties
# just below, ok comfortably below, no comfortably above
TARGET = {"V03": 13.0, "V07": 12.7, "V11": 11.5, "V14": -6.9, "V18": -14.8, "V02": -26.4, "V05": -14.7, "V09": -38.7, "V16": -25.7, "V21": 31.8, "V24": 24.7, "V27": 33.4, "V30": 24.5, "V33": 34.5}

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
