"""task22 world constants: Delmont Power and Light, a city-owned electric utility in north-east Oklahoma, its four
69/12.47 kV substations and fourteen feeders, the customers and loads on them, and the systems that record them.
Every number the simulation draws from is here; world.py turns them into the clean truth."""
import datetime as dt
from zoneinfo import ZoneInfo

SEED = 22061
TZ = ZoneInfo("America/Chicago")
UTC = dt.timezone.utc
START_LOCAL = dt.datetime(2023, 9, 1, 0, 0, tzinfo=TZ)      # first hour simulated (local midnight)
END_LOCAL = dt.datetime(2026, 11, 1, 0, 0, tzinfo=TZ)        # exclusive
EXTRACT_DATE = dt.date(2026, 11, 2)                           # the day the extracts are pulled
WIN26 = (dt.date(2025, 10, 1), dt.date(2026, 10, 1))          # the twelve months to September 2026
WIN24 = (dt.date(2023, 10, 1), dt.date(2024, 10, 1))          # the twelve months to September 2024
LAT, LON = 36.66, -95.14                                      # Delmont's municipal airport (fictional)
V_KV = 12.47
SINGLE_PHASE_FACTOR = 6.0     # loss on a single-phase tap = 6 x R x (S/V)^2: phase and neutral each carry I = S/7.2 kV
SECONDARY_SHARE = 0.007       # secondary and service losses, share of energy delivered to services (the 2019 study)
OMS_CUTOVER = dt.datetime(2024, 7, 15, 6, 0, tzinfo=TZ)       # OMS upgrade: device names move to the GIS switch ids
GIS_MIGRATION = dt.date(2024, 2, 5)

# conductor code -> ohms per mile at 50 C (and 25 C), reactance; the engineering tables ship both temperatures
CONDUCTORS = {
    "336.4 ACSR": (0.306, 0.278, 0.53),
    "4/0 ACSR": (0.592, 0.543, 0.62),
    "2/0 ACSR": (0.895, 0.822, 0.64),
    "1/0 ACSR": (1.120, 1.031, 0.65),
    "#2 ACSR": (1.690, 1.553, 0.67),
    "#4 ACSR": (2.550, 2.341, 0.69),
    "1/0 AL URD": (1.010, 0.928, 0.24),
}
# distribution transformer losses by kVA: (no-load W, load loss W at rated) for units made 2010 on; older units x1.35
# no-load and x1.12 load loss (the engineering tables carry both vintages)
XFMR_LOSS = {
    10: (38, 150), 15: (50, 190), 25: (75, 290), 37.5: (100, 410), 50: (120, 520), 75: (180, 800),
    100: (220, 1000), 167: (320, 1500), 300: (500, 2600), 500: (750, 4000), 750: (1000, 5600), 1000: (1250, 7200),
    1500: (1700, 10200), 2500: (2500, 15800),
}
OLD_NL, OLD_LL = 1.35, 1.12

# substation transformers 69/12.47 kV: rating MVA, no-load kW, load loss kW at rating
SUBSTATIONS = {
    "NTH": {"name": "North", "dp": "DLM-NTH69", "mva": 25.0, "nl_kw": 19.0, "ll_kw": 118.0, "ss_kw": 9.5},
    "IND": {"name": "Industrial Park", "dp": "DLM-IND69", "mva": 25.0, "nl_kw": 19.5, "ll_kw": 121.0, "ss_kw": 11.0},
    "APT": {"name": "Airport Road", "dp": "DLM-APT69", "mva": 30.0, "nl_kw": 22.0, "ll_kw": 139.0, "ss_kw": 10.5},
    "CHL": {"name": "Cherry Hill", "dp": "DLM-CHL69", "mva": 20.0, "nl_kw": 16.5, "ll_kw": 102.0, "ss_kw": 8.0},
}

# feeders: substation, kind, trunk miles, trunk conductor, residential and small commercial counts, electric-heat
# share, PV share, illegal grow sites (count, mean kW), AMI conversion (year, month) or None (still AMR at extract)
FEEDERS = {
    "NTH-1": dict(sub="NTH", kind="town", trunk_mi=4.6, trunk="336.4 ACSR", res=930, sc=140, eheat=0.30, pv=0.075,
                  theft=(1, 4.0), ami=(2024, 11)),
    "NTH-2": dict(sub="NTH", kind="town", trunk_mi=5.1, trunk="336.4 ACSR", res=880, sc=120, eheat=0.28, pv=0.07,
                  theft=(2, 4.5), ami=(2024, 11)),
    "NTH-3": dict(sub="NTH", kind="rural", trunk_mi=12.8, trunk="4/0 ACSR", res=390, sc=30, eheat=0.45, pv=0.045,
                  theft=(6, 8.5), ami=(2025, 10)),
    "NTH-4": dict(sub="NTH", kind="rural", trunk_mi=15.6, trunk="4/0 ACSR", res=350, sc=25, eheat=0.48, pv=0.04,
                  theft=(9, 9.0), ami=(2026, 5)),
    "IND-1": dict(sub="IND", kind="industrial", trunk_mi=3.6, trunk="336.4 ACSR", res=410, sc=165, eheat=0.25,
                  pv=0.05, theft=(1, 5.0), ami=(2024, 5)),
    "IND-2": dict(sub="IND", kind="town", trunk_mi=4.2, trunk="336.4 ACSR", res=770, sc=110, eheat=0.27, pv=0.065,
                  theft=(2, 4.0), ami=(2024, 5)),
    "IND-3": dict(sub="IND", kind="rural", trunk_mi=11.9, trunk="4/0 ACSR", res=300, sc=25, eheat=0.46, pv=0.04,
                  theft=(5, 8.0), ami=None),
    "APT-1": dict(sub="APT", kind="town", trunk_mi=4.1, trunk="336.4 ACSR", res=890, sc=125, eheat=0.29, pv=0.08,
                  theft=(1, 4.0), ami=(2025, 5)),
    "APT-2": dict(sub="APT", kind="town", trunk_mi=5.6, trunk="336.4 ACSR", res=820, sc=100, eheat=0.30, pv=0.075,
                  theft=(2, 4.5), ami=(2025, 5)),
    "APT-3": dict(sub="APT", kind="rural", trunk_mi=13.6, trunk="4/0 ACSR", res=310, sc=20, eheat=0.47, pv=0.035,
                  theft=(4, 8.0), ami=(2026, 5)),
    "APT-4": dict(sub="APT", kind="rural", trunk_mi=17.8, trunk="4/0 ACSR", res=330, sc=22, eheat=0.50, pv=0.03,
                  theft=(13, 9.0), ami=None),
    "CHL-1": dict(sub="CHL", kind="town", trunk_mi=4.3, trunk="336.4 ACSR", res=860, sc=130, eheat=0.31, pv=0.07,
                  theft=(2, 4.0), ami=(2025, 5)),
    "CHL-2": dict(sub="CHL", kind="rural", trunk_mi=16.9, trunk="4/0 ACSR", res=360, sc=26, eheat=0.49, pv=0.03,
                  theft=(16, 9.0), ami=None),
    "CHL-3": dict(sub="CHL", kind="rural", trunk_mi=14.9, trunk="4/0 ACSR", res=335, sc=24, eheat=0.48, pv=0.035,
                  theft=(11, 9.0), ami=(2026, 5)),
}
FEEDER_ORDER = list(FEEDERS)
SUB_FEEDERS = {s: [f for f in FEEDER_ORDER if FEEDERS[f]["sub"] == s] for s in SUBSTATIONS}

# large power customers: (key, feeder, name, class, average kW, position as share of trunk length or "near",
# energized (y, m) or None for before the data, connected kW applied, transformer kVA)
LARGE_POWER = [
    ("LP01", "IND-1", "Ozark Valley Poultry, processing plant", "POULTRY", 1850, 0.55, None, 3400, 2500),
    ("LP02", "IND-1", "Dawes Hardwood Sawmill", "SAWMILL", 520, 0.80, None, 1100, 1000),
    ("LP03", "IND-2", "Delmont Regional Medical Center", "HOSPITAL", 880, 0.35, None, 1600, 1500),
    ("LP04", "IND-2", "Delmont High School", "SCHOOL", 330, 0.50, None, 900, 750),
    ("LP05", "NTH-1", "City of Delmont Water Treatment Plant", "WATER", 410, 0.40, None, 800, 750),
    ("LP06", "NTH-1", "Delmont Supercenter", "RETAIL", 470, 0.30, None, 950, 750),
    ("LP07", "NTH-2", "Washington Middle School", "SCHOOL", 170, 0.45, None, 450, 300),
    ("LP08", "APT-1", "City of Delmont Wastewater Plant", "WATER", 300, 0.70, None, 700, 500),
    ("LP09", "APT-1", "Delmont Municipal Airport and hangars", "RETAIL", 160, 0.85, None, 400, 300),
    ("LP10", "APT-2", "Route 60 Inn and Conference Center", "HOSPITAL", 210, 0.40, None, 500, 300),
    ("LP11", "CHL-1", "Cherry Hill Shopping Center", "RETAIL", 380, 0.35, None, 900, 750),
    ("LP12", "CHL-1", "Lincoln Elementary", "SCHOOL", 120, 0.55, None, 300, 300),
    ("LP13", "IND-3", "Spavinaw Feed and Grain", "SAWMILL", 260, 0.45, None, 600, 500),
    ("LP14", "CHL-3", "Big Cabin Aggregates, crusher", "SAWMILL", 310, 0.25, None, 1000, 750),
    ("LP15", "APT-3", "Prairie Fresh Cold Storage", "COLDSTORE", 620, 0.94, (2025, 3), 1350, 1000),
    ("LP16", "APT-3", "Green Acres Cultivation LLC", "GROW", 300, 0.62, None, 735, 500),
    ("LP17", "APT-3", "Red Dirt Botanicals", "GROW", 240, 0.95, (2023, 6), 560, 500),
    ("LP18", "APT-4", "Bluestem Craft Cannabis", "GROW", 340, 0.76, None, 845, 500),
    ("LP19", "APT-4", "Osage Hills Farms", "GROW", 290, 0.92, (2024, 4), 680, 500),
    ("LP20", "NTH-4", "Northline Growers Co-op", "GROW", 340, 0.60, None, 790, 500),
    ("LP21", "IND-3", "Six Mile Cultivation", "GROW", 290, 0.88, None, 715, 500),
    ("LP22", "CHL-2", "Hominy Creek Gardens", "GROW", 330, 0.58, None, 805, 500),
    ("LP23", "CHL-2", "Tallgrass Indoor Farms", "GROW", 310, 0.74, (2023, 9), 735, 500),
    ("LP24", "CHL-3", "Cherokee Strip Harvest", "GROW", 280, 0.30, None, 690, 500),
    ("LP25", "NTH-3", "Pensacola Road Storage Units", "RETAIL", 90, 0.50, None, 200, 167),
]
LP_BEFORE_2019 = {"LP01", "LP02", "LP03", "LP04", "LP05", "LP06", "LP07", "LP08", "LP09", "LP10", "LP11", "LP12",
                  "LP13", "LP14", "LP25"}
LP_2019_TO_2023 = {"LP16": 2020, "LP18": 2021, "LP20": 2022, "LP21": 2021, "LP22": 2020, "LP24": 2021}

# 2027 approved connections (applications file): key, feeder, name, class, applied kW, position, energize (y, m, d),
# transformer kVA; the subdivision is residential lots ramping from its first month
NEW_2027 = [
    ("AP27-01", "APT-4", "Flint Ridge Cultivation LLC", "GROW", 1250, 0.90, (2027, 5, 1), 1500),
    ("AP27-02", "APT-3", "Prairie Fresh Cold Storage, freezer expansion", "COLDSTORE", 820, 0.94, (2027, 4, 1), 1000),
    ("AP27-03", "CHL-3", "Wildhorse Greenhouse", "GROW", 700, 0.55, (2027, 8, 1), 750),
]
SUBDIVISION = dict(feeder="NTH-1", name="Prairie Rose Estates", lots=140, start=(2027, 3), per_month=12, pos=0.25)
RECONDUCTOR = dict(feeder="APT-3", in_service=dt.date(2027, 3, 15), new="336.4 ACSR", miles=9.8)
# illegal grows: each feeder's stolen energy in the twelve months to September 2026 (MWh), the sites' kW scaled to it
THEFT_TARGET = {"NTH-1": 67, "NTH-2": 103, "NTH-3": 480, "NTH-4": 643, "IND-1": 64, "IND-2": 84, "IND-3": 321,
                "APT-1": 44, "APT-2": 102, "APT-3": 480, "APT-4": 1036, "CHL-1": 86, "CHL-2": 1200, "CHL-3": 610}

# switching: permanent transfers and temporary ties (feeder from, feeder to, customers moved, local datetime start,
# end or None for permanent); planned maintenance pairs are drawn in world.py
TRANSFERS = [
    dict(key="T24", frm="NTH-2", to="NTH-1", cust=95, start=dt.datetime(2024, 3, 18, 10, 20), end=None,
         reason="Reconfiguration"),
    dict(key="T25", frm="IND-1", to="IND-2", cust=210, start=dt.datetime(2025, 6, 2, 8, 40),
         end=dt.datetime(2025, 7, 14, 15, 10), reason="Construction"),
    dict(key="T24b", frm="APT-1", to="APT-2", cust=120, start=dt.datetime(2024, 12, 3, 7, 50),
         end=dt.datetime(2024, 12, 10, 16, 30), reason="Construction"),
    dict(key="T26", frm="NTH-3", to="NTH-4", cust=64, start=dt.datetime(2026, 4, 21, 9, 15), end=None,
         reason="Reconfiguration"),
]
# the January 2026 ice storm at Cherry Hill
STORM = dict(fault=dt.datetime(2026, 1, 24, 5, 40), tie_close=dt.datetime(2026, 1, 24, 14, 20),
             repair=dt.datetime(2026, 2, 2, 11, 5), first_section_customers=28,
             gap_start=dt.datetime(2026, 1, 23, 22, 0), gap_end=dt.datetime(2026, 2, 3, 7, 0))

# lighting: street lights (the city's account) and area lights rented to customers
DEEMED_KWH = {"HPS100": 40, "HPS150": 60, "HPS250": 100, "MV175": 70, "LED40": 15, "LED70": 26, "LED110": 40}
INPUT_W = {"HPS100": 128, "HPS150": 188, "HPS250": 295, "MV175": 205, "LED40": 40, "LED70": 70, "LED110": 110}
LED_FOR = {"HPS100": "LED40", "HPS150": "LED70", "HPS250": "LED110", "MV175": "LED40"}

# business-day holidays the city's billing calendar skips (read routes run on business days)
HOLIDAYS = {dt.date(2023, 11, 10), dt.date(2023, 11, 23), dt.date(2023, 11, 24), dt.date(2023, 12, 25),
            dt.date(2024, 1, 1), dt.date(2024, 1, 15), dt.date(2024, 2, 19), dt.date(2024, 5, 27), dt.date(2024, 6, 19),
            dt.date(2024, 7, 4), dt.date(2024, 9, 2), dt.date(2024, 11, 11), dt.date(2024, 11, 28), dt.date(2024, 11, 29),
            dt.date(2024, 12, 25), dt.date(2025, 1, 1), dt.date(2025, 1, 20), dt.date(2025, 2, 17), dt.date(2025, 5, 26),
            dt.date(2025, 6, 19), dt.date(2025, 7, 4), dt.date(2025, 9, 1), dt.date(2025, 11, 11), dt.date(2025, 11, 27),
            dt.date(2025, 11, 28), dt.date(2025, 12, 25), dt.date(2026, 1, 1), dt.date(2026, 1, 19), dt.date(2026, 2, 16),
            dt.date(2026, 5, 25), dt.date(2026, 6, 19), dt.date(2026, 7, 3), dt.date(2026, 9, 7), dt.date(2026, 11, 11),
            dt.date(2026, 11, 26), dt.date(2026, 11, 27), dt.date(2023, 10, 9), dt.date(2023, 9, 4)}
