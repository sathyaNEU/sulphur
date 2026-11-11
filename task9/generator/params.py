"""task9: Tessaline Semiconductor's Fab 2. Every parameter the simulator, the pack writer and the analysis share.

The fab is simulated wafer by wafer: lot starts with a product mix that shifts in June, a forty-step flow where one
deposition chamber's wafers are routed mostly to two of the four polish units, clustered random defects with a weekly
drift and a fab-wide particle week, the outer band's normal roll-off, and the edge ring: excess kill in the outer band
that rises with the CMP conditioner disk's wear once the disk passes its onset, faster on the higher-downforce units and
on the disks of the supplier's March lot, with a small pad term; and below that onset, thinned edge dielectric that
passes sort and fails burn-in at final test, rising over a shorter span and levelling off. The maintenance timeline
resets the pad every 600 wafers and pad, disk and retaining ring together at a full PM (2,000 wafers under Rev E, 2,800
under Rev F from 2 April), except at the July full PMs that kept the disk under waiver EW-118, and the unscheduled
disk-only and ring-only swaps; stores issue the oldest disk lot first. The analysis never reads this file's world
parameters; it reads the pack.
"""
import datetime as dt

SEED = 9021
FIRM = "Tessaline Semiconductor"
FAB = "Fab 2"
ZONE = "America/Phoenix"

START = dt.date(2026, 1, 5)            # first ILD-CMP polish in the record
LAST_POLISH = dt.date(2026, 8, 16)     # wafers polished after this day are not yet sorted at the pull
PULL = dt.date(2026, 8, 31)            # the record's last day (sort results to here)
LOSS_FROM, LOSS_TO = dt.date(2026, 4, 1), dt.date(2026, 8, 31)   # the window the loss is asked for, by sort date
REV_F = dt.date(2026, 4, 2)            # full PM interval 2,000 -> 2,800 wafers
EW118 = (dt.date(2026, 6, 1), dt.date(2026, 8, 14))   # the disk-life trial waiver's window
PARTICLE_WEEK = (dt.date(2026, 5, 18), dt.date(2026, 5, 24))
SC4_START = dt.date(2026, 4, 10)       # the new scanner joins the M1 litho step
MIX_SHIFT = dt.date(2026, 6, 1)

LOTS_PER_WEEK = 45
WAFERS_PER_LOT = 25
PRODUCTS = {
    "P-A": dict(area=0.50, die_w=7.2, die_h=6.95, value=0.80, alias=["PA-MCU32", "MCU32A"], assembly=0.31, package="MCU32A-QFN48"),
    "P-B": dict(area=1.10, die_w=10.6, die_h=10.4, value=2.10, alias=["PB-MCU64", "MCU64B"], assembly=0.58, package="MCU64B-LQFP100"),
    "P-C": dict(area=0.25, die_w=5.0, die_h=5.0, value=0.45, alias=["PC-MCU16", "MCU16C"], assembly=0.22, package="MCU16C-QFN32"),
}
MIX = {"P-A": 0.50, "P-B": 0.20, "P-C": 0.30}
MIX_LATE = {"P-A": 0.45, "P-B": 0.28, "P-C": 0.27}
WAFER_R, EDGE_EXCL = 150.0, 3.0
ZONE_EDGES = [0, 40, 62, 80, 95, 108, 120, 136, 147]    # radial zones z1..z8 (mm); z8 is the outer band
BAND_ZONE = 8

D0_MEAN, D0_SHAPE = 0.12, 2.0          # killer defects per cm2, gamma across wafers
CLUSTER_SHAPE = 1.6                    # gamma clustering of defects within a wafer, by zone
WEEK_DRIFT = 0.08
PARTICLE_MULT = 1.4
ROLL_OFF = 0.03                        # the outer band's normal extra fail probability
TOOL_OFFSET_SD = 0.04                  # small benign tool effects on D0

# the ring: excess kill probability in the outer band
RING_ONSET, RING_SPAN, RING_SCALE, RING_CAP = 1100.0, 1700.0, 0.22, 0.92
PAD_TERM = 0.08                        # x (1 + 0.08 pad_life / 600)
UNIT_WEAR = {"PU-1": 0.84, "PU-2": 0.88, "PU-3": 1.22, "PU-4": 1.27}   # disk wear per wafer, by downforce
DISK_SPREAD = 0.05                     # disk-to-disk spread of the wear rate within a lot (lognormal sd)
# the supplier's conditioner-disk lots as stores received them, with each lot's wear relative to the 2025 lots; stores
# issue the oldest lot on the shelf first
DISK_LOTS = [dict(lot="A165-L2509", received=dt.date(2025, 10, 9), first=7012, qty=14, wear=1.00),
             dict(lot="A165-L2511", received=dt.date(2025, 12, 11), first=7466, qty=7, wear=1.00),
             dict(lot="A165-L2603", received=dt.date(2026, 3, 30), first=9104, qty=30, wear=1.42)]
# latent edge damage: thinned dielectric that passes sort and fails burn-in at final test, from an earlier wear
LAT_ONSET, LAT_SPAN, LAT_SCALE = 600.0, 350.0, 0.06   # ramps over 350 wear units to 6 per cent of the band's good die
FT_LAG = (12.0, 20.0)                  # days from a lot's last sort to its final test at the assembly house
FT_BASE = dict(ft1=0.0060, burnin=0.0022, ft2=0.0035)
ASSY_LOSS = 0.0028                     # die lost in assembly (saw, attach, bond) before final test
UNIT_DOWNFORCE = {"PU-1": 3.55, "PU-2": 3.60, "PU-3": 4.20, "PU-4": 4.25}
CMP_GROUPS = {"CMP1": ["PU-1", "PU-2"], "CMP2": ["PU-3", "PU-4"]}

# maintenance
PAD_LIFE = (600, 40)
FULL_PM = {"REV_E": 2000, "REV_F": 2800}
INITIAL = {"PU-1": dict(full=1350, disk=1350, pad=180, ring=1350), "PU-2": dict(full=1240, disk=1240, pad=410, ring=1240),
           "PU-3": dict(full=1800, disk=1800, pad=320, ring=1800), "PU-4": dict(full=1720, disk=1720, pad=90, ring=1720)}
EW118_REUSES = 2
PLATEN_BASE = {"PU-1": 431200, "PU-2": 418950, "PU-3": 402310, "PU-4": 396880}   # each platen's lifetime counter on 5 January
DOWN_HOURS = dict(full=17, disk=8, ring=3, pad=2)   # a unit is down this long for each kind of part change
DISK_ONLY_SWAPS = [("PU-2", dt.date(2026, 3, 3)), ("PU-4", dt.date(2026, 5, 6)), ("PU-1", dt.date(2026, 7, 21))]
RING_ONLY_SWAPS = [("PU-1", dt.date(2026, 2, 9)), ("PU-3", dt.date(2026, 3, 24)), ("PU-2", dt.date(2026, 4, 28)),
                   ("PU-4", dt.date(2026, 6, 23)), ("PU-3", dt.date(2026, 7, 8)), ("PU-1", dt.date(2026, 8, 4))]
DEP_AFFINITY = 0.70                    # DEP-3's wafers go to PU-3 or PU-4 this often (others 0.40)

# metrology on one wafer in five: edge-to-centre removal-rate ratio
RR_ONSET, RR_SLOPE, RR_RING, RR_NOISE = 900.0, 9e-5, 2e-5, 0.010

# the fab's ring classifier
ADC = dict(severe=0.22, severe_recall=0.88, moderate=0.12, moderate_recall=0.50, mild=0.05, mild_recall=0.18, fp_base=0.012)

# the yield team's die-map pulls
DIEMAP = dict(flagged=0.45, low_yield=0.84, low_yield_share=0.35, random=0.03)

COSTS = dict(disk_part=2350, pad_part=640, ring_part=1180, tech_rate=95, requal_hours=6, downtime_rate=350,
             pad_hours=2, disk_hours=8, ring_hours=3, full_pm_hours=17, wafers_per_year=58500,
             by_unit={"PU-1": 15400, "PU-2": 15500, "PU-3": 13800, "PU-4": 13800},
             mix_plan={"P-A": 0.46, "P-B": 0.26, "P-C": 0.28})

PEOPLE = dict(yield_lead="Katelyn Bailey", cmp="Victor Kelley", maint="Leah Griffith", finance="Elizabeth Sandoval")
TECHS = ["J. Ortega", "M. Pham", "R. Castillo", "D. Whitfield", "S. Nakamura", "T. Boyd"]
