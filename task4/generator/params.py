"""task4 architecture 8: the world's fixed facts. Fryele Akeri AB, a road haulier in Smaland, ran a battery-electric
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

AERO = 0.054      # air drag: kWh per km per 1000 (km/h)^2 of average speed above the reference
V_REF = 65.0       # the speed at which E0 holds
# the routing tool's planned speed is optimistic, and more so on winter roads: actual = planned x ratio(T) x noise
R0 = 0.945         # actual over planned on mild days
RC = 0.0120        # the ratio's fall per degree below about 10 C, a smooth curve (sim.ratio)
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
    "GLF": ("Gislaveds Livsmedel AB", "Gislaved", "est", 15.2, 1.40),
    "HFG": ("Hestra Frukt & Grönt AB", "Hestra", "est", 12.6, 1.40),
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
    "V24": ("GLF", 44, "Oskarshamn", "no"),
    "V27": ("GDR", 34, "Trollhättan", "no"),
    "V30": ("BMJ", 40, "Uddevalla", "no"),
    "V33": ("HFG", 34, "Västervik", "ok"),
}
# each duty's true design-day energy (kWh), set so the duty sits where the order's design puts it
TARGET = {"V02": 471.9, "V03": 430.5, "V05": 425.2, "V07": 467.8, "V09": 419.7, "V11": 429.9, "V14": 467.0, "V16": 419.5, "V18": 426.7, "V21": 471.8, "V24": 470.9, "V27": 478.2, "V30": 463.9, "V33": 435.2}

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


# ---------------------------------------------------------------- architecture 8: the combination and its load
# rolling and climbing resistance act on the whole combination: every tonne of tractor and trailer tare costs on every
# leg what a tonne of payload costs on the loaded leg (LOAD), measured from the reference combination E0 holds at
TARE_REF = 19.0          # t, tractor plus trailer
PILOT_TRACTOR_TARE = {"BEV-01": 11440, "BEV-02": 11470, "BEV-03": 11420, "BEV-04": 11490, "BEV-05": 11450,
                      "BEV-06": 11460}
TRACTOR_2027_TARE = 11980   # the quotation's tractor, kg (larger pack)
# trailer kinds: body code (EU), the register's type text, tare range kg
KINDS = {
    "CUR": ("06", "Curtain-sider semi-trailer 13.6 m", (6950, 7450)),
    "MEGA": ("06", "Curtain-sider semi-trailer 13.6 m, mega 3.0 m", (7300, 7800)),
    "BOX": ("03", "Box semi-trailer 13.6 m", (7900, 8450)),
    "DD": ("03", "Box semi-trailer 13.6 m, double deck", (10350, 10950)),
    "REEF": ("04", "Reefer semi-trailer 13.6 m", (9050, 9600)),
    "FLAT": ("01", "Flatbed semi-trailer 13.6 m, stanchions", (6050, 6550)),
    "TIP": ("10", "Tipper semi-trailer 36 m3", (7650, 8200)),
    "INL": ("30", "Inloader semi-trailer (glass)", (10950, 11500)),
}
# refrigeration units on the reefers: only an ePTO unit runs from the tractor's battery; an AGen unit runs from its own
# axle generator and battery, a diesel unit from its own tank, a D+SB unit from its tank on the road and a yard plug
TRU_KINDS = ["SR-60 D", "SR-60 D+SB", "SR-60e ePTO", "AX-40 AGen"]
TRU_KW = 4.4             # mean electrical draw of an ePTO unit over a duty (cooling, heating, door openings), kW
# each duty's trailer kind; reefer duties name the unit kinds their pool carries with weights
DUTY_KIND = {
    "J01": "BOX", "J02": "BOX", "J03": "DD", "J04": "DD", "J05": ("REEF", {"SR-60e ePTO": 0.55, "SR-60 D": 0.30,
                                                                         "AX-40 AGen": 0.15}),
    "J06": "INL", "J07": "CUR", "J08": "CUR", "J09": "FLAT",
    "V02": "DD", "V03": "FLAT", "V05": "MEGA", "V07": "TIP", "V09": "INL", "V11": "FLAT", "V14": "DD", "V16": "CUR",
    "V18": "BOX", "V21": "CUR", "V24": ("REEF", {"SR-60e ePTO": 1.0}), "V27": "CUR",
    "V30": ("REEF", {"SR-60e ePTO": 1.0}), "V33": ("REEF", {"SR-60 D+SB": 0.7, "SR-60 D": 0.3}),
    "V06": ("REEF", {"SR-60e ePTO": 0.6, "AX-40 AGen": 0.4}), "V38": ("REEF", {"SR-60e ePTO": 0.5, "SR-60 D": 0.5}),
}
SHIPPER_KIND = {"TEN": "BOX", "HWP": "DD", "BMJ": ("REEF", {"SR-60 D": 0.3, "SR-60e ePTO": 0.5, "AX-40 AGen": 0.2}),
                "TTV": "FLAT", "GDR": "CUR", "LBY": "FLAT", "GST": "FLAT", "SKB": "TIP", "HIL": "FLAT", "VIS": "DD",
                "BPL": "MEGA", "RPA": "CUR", "FGU": "BOX", "RTR": "CUR", "ANE": "BOX", "KCY": "DD", "VGL": "INL",
                "GLF": ("REEF", {"SR-60 D+SB": 0.4, "SR-60e ePTO": 0.6}),
                "HFG": ("REEF", {"SR-60 D": 0.6, "AX-40 AGen": 0.4})}
# drops on the loaded run: (town, share of the load taken off there) in order, the last at the delivery; km along the
# loaded run from the collection set as fractions of it
DROPS = {
    "J05": [("Eksjö", 0.34, 0.33), ("Vetlanda", 0.27, 0.58), ("Målilla", 0.22, 0.84), ("Hultsfred", 0.17, 1.0)],
    "J07": [("Ödeshög", 0.40, 0.30), ("Vadstena", 0.33, 0.64), ("Motala", 0.27, 1.0)],
    "J08": [("Eksjö", 0.38, 0.36), ("Ingatorp", 0.30, 0.66), ("Vimmerby", 0.32, 1.0)],
    "J09": [("Skillingaryd", 0.55, 0.42), ("Värnamo", 0.45, 1.0)],
    "V03": [("Ängelholm", 0.47, 0.36), ("Höganäs", 0.33, 0.71), ("Helsingborg", 0.20, 1.0)],
    "V11": [("Ljungby", 0.30, 0.20), ("Hässleholm", 0.40, 0.55), ("Kristianstad", 0.30, 1.0)],
    "V24": [("Kalmar", 0.52, 0.62), ("Oskarshamn", 0.48, 1.0)],
    "V27": [("Borås", 0.38, 0.41), ("Vänersborg", 0.34, 0.86), ("Trollhättan", 0.28, 1.0)],
    "V30": [("Göteborg", 0.36, 0.60), ("Kungälv", 0.30, 0.78), ("Uddevalla", 0.34, 1.0)],
}
# the Jonkoping pilot duties draw from mixed pools: the kind of each trailer in the duty's pool, in order
POOL_KINDS = {"J01": ["BOX", "BOX", "MEGA", "BOX"], "J02": ["BOX", "MEGA", "BOX"], "J03": ["DD", "DD", "BOX"],
              "J04": ["DD", "BOX", "DD"], "J07": ["CUR", "MEGA", "CUR"], "J08": ["CUR", "CUR", "MEGA"],
              "J09": ["FLAT", "FLAT", "FLAT", "FLAT"]}
MOFFETT = {"J09": [True, False, True, False]}   # a truck-mounted forklift carried on the trailer's rear (about 1.9 t)
DROP_CONC = 45.0          # day-to-day spread of the shares (Dirichlet concentration)
DWELL_LOAD = (0.75, 0.20)  # loading at the collection, h (base, uniform extra)
DWELL_DROP = (0.40, 0.15)  # each drop before the last, h
DWELL_LAST = (0.60, 0.20)  # unloading at the delivery, h
