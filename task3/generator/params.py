"""task3 architecture 3: the Corrin Valley world, every constant in one place.

The truth: a confined sand and gravel aquifer filling a buried bedrock valley (Corrin Valley, Indiana), capped by
clay-rich till. The valley walls are no-flow boundaries; the till leaks water down into the aquifer in proportion to
the drawdown. Over a three-day pumping test the walls' extra drawdown and the till's leakage nearly cancel, so the
test reads as an infinite aquifer that never leaks; over years the leakage wins and the cone stops growing.
Harlow Springs has pumped the Mill Street wells since 2009, and the record those wells left in the monitoring wells
is the only place the far field shows. The aquifer's natural level moves with the region's wet and dry years, and
the nearest network well sits inside the Mill Street cone."""
import math

SEED = 20261109
AS_OF = "2026-11-06"

# aquifer (truth)
T = 8000.0          # ft2/day
S = 1.0e-3
B = 3500.0          # leakage factor, ft
WIDTH = 5000.0      # effective valley width between the no-flow walls, ft
BE = 0.48           # barometric efficiency of the confined aquifer
GPM = 192.5         # ft3/day per gpm (1 gpm = 0.13368 ft3/min * 1440)

# valley frame: the axis runs N 18 E through ORIGIN; a = along the axis (north-north-east positive),
# c = across it (east-south-east positive); the walls sit at c = -WIDTH/2 and c = +WIDTH/2
ORIGIN = (412640.0, 1688210.0)     # Indiana East State Plane, US survey feet
AZ = math.radians(18.0)

# wells in valley coordinates (a, c), ft
WELLS = {
    # Harlow Springs, Mill Street well field (pumping since 2009, TW-2 since 2014)
    "TW-1": (0.0, -250.0), "TW-2": (40.0, 260.0), "MS-MW": (60.0, -630.0),
    # Reidel Road well field (2026 test)
    "PW-1": (9000.0, -200.0), "PW-2": (9010.0, 210.0),
    "OW-1": (9150.0, -205.0), "OW-2": (8985.0, -820.0), "OW-3": (10450.0, -190.0),
    # district network
    "OW-S": (7300.0, 700.0),
    "CV-07": (3200.0, -900.0),
    "CV-02": (-26000.0, 300.0),
    "CV-11": (30500.0, -420.0),
    "CV-04": (5200.0, 1500.0),     # shallow outwash
    "CV-09": (-12400.0, -1600.0),  # shallow outwash
    "CV-13": (-8100.0, -3900.0),   # bedrock, outside the valley fill
    "CV-05": (-18600.0, 1900.0),   # confined, west tributary reach, short record
    # registered domestic wells in the confined aquifer (no readings)
    "DW-17": (6800.0, -2300.0), "DW-22": (13800.0, 1900.0), "DW-09": (1500.0, 2100.0),
}
NETWORK = ["OW-S", "CV-02", "CV-04", "CV-05", "CV-07", "CV-09", "CV-11", "CV-13"]
CONFINED = {"DW-17", "DW-22", "DW-09", "OW-S", "CV-02", "CV-05", "CV-07", "CV-11", "MS-MW", "OW-1", "OW-2", "OW-3", "PW-1", "PW-2",
            "TW-1", "TW-2"}

# Mill Street pumping history: annual average gpm by well, the summer peak and the 2014 second well
TOWN_START = (2009, 3)
TW2_START = (2014, 6)
TOWN_BASE_GPM = 372.0
TOWN_GROWTH = 0.0185
TOWN_SEASON = 0.24
TW1_SHARE_AFTER = 0.56
# the town's own projection for 2027 to 2046 (filed in the application): growth on the 2025 average
TOWN_PROJ_GROWTH = 0.012

# the application's four rates (annual average gpm, Reidel Road field split evenly over PW-1 and PW-2)
OPTIONS = [450, 700, 1000, 1250]
NEW_SEASON = [0.78, 0.76, 0.80, 0.88, 1.02, 1.21, 1.34, 1.31, 1.17, 0.98, 0.88, 0.87]   # Jan..Dec
NEW_START = (2027, 4)
TERM_END = 2046
LIMIT = 9.0          # ft at OW-S, Rule WR-4 Table 1

# the test
TEST_START = "2026-09-14 09:00"   # EDT, pump on
TEST_HOURS = 72
TEST_RATE_GPM = (1018.0, 1003.0)  # the rate drifts down as the column warms, start to end
LOG_FROM = "2026-09-08 12:00"
LOG_TO = "2026-09-20 12:00"
RECOVERY_HOURS = 72

# the application's projection for the Mill Street wells (annual average gpm in 2026, then growth a year)
TOWN_PROJ_BASE = 548.0
TOWN_MONTH_FACTORS = [0.81, 0.80, 0.84, 0.90, 1.03, 1.17, 1.25, 1.23, 1.11, 0.98, 0.95, 0.93]

# the region's wet and dry years for the confined aquifer (ft against the long-run level); the 2005 to 2008
# baseline was a dry run, the 2010s and early 2020s wet, with the 2012 drought and the 2023 dry autumn
WET_DRY = {2005: -0.75, 2006: -0.45, 2007: -0.95, 2008: -0.55, 2009: 0.15, 2010: 0.35, 2011: 1.25, 2012: -0.55,
           2013: 0.75, 2014: 0.95, 2015: 1.05, 2016: 0.65, 2017: 1.55, 2018: 1.85, 2019: 1.75, 2020: 1.15,
           2021: 0.85, 2022: 0.45, 2023: -0.15, 2024: 0.75, 2025: 0.95, 2026: 0.55}
NAT_GAIN = {"CV-02": 0.97, "CV-11": 1.03, "CV-05": 0.92, "OW-S": 1.0, "MS-MW": 1.0, "CV-07": 1.0}
