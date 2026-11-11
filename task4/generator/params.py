"""task4 architecture 11: the world's constants. Telkkä Logistics Oy runs the Saarnela fulfilment centre (Uusimaa)
for Kotikaari Oy, an online home and interior retailer with showrooms, which bought the sporting goods web shop
Huippu Sport in 2025 and moves Huippu's orders from another provider's warehouse into Saarnela in March 2027."""
import datetime as dt

SEED = 110411
ORG = "Telkkä Logistics Oy"
SITE = "Saarnela"
CLIENT = "Kotikaari Oy"
BRAND_K = "Kotikaari"
BRAND_H = "Huippu Sport"
AGENCY = "Työpiste Henkilöstö Oy"
PEOPLE = {"director": "Helena Korhonen", "site": "Tapio Nieminen", "planning": "Tarja Huhtala",
          "ci": "Marko Autio", "hr": "Anja Kanerva", "agency": "Marika Sutinen", "slotting": "Juho Kivinen"}

SIM_START = dt.date(2020, 1, 1)       # the planners' first base year
DATA_START = dt.date(2022, 1, 3)      # ISO 2022-W01, the WMS labour log's first day
DATA_END = dt.date(2026, 11, 1)       # ISO 2026-W44 ends
ASOF = dt.date(2026, 11, 6)
PAYROLL_SWITCH = dt.date(2024, 1, 1)  # the new payroll system
LIMIT_FROM = dt.date(2024, 1, 8)      # the zone limits of pickers on the floor (the 2023 safety review), with the extension
PILOT = (dt.date(2026, 9, 7), dt.date(2026, 11, 1))   # ISO 2026-W37 to W44
TRUTH_END = dt.date(2027, 12, 31)

ZONES = ("P1", "P2", "B1")
SMALL = ("P1", "P2")
AISLES = {"P1": 12, "P2": 11, "B1": 6}        # since the mezzanine extension opened on 8 January 2024
AISLES_OLD = {"P1": 8, "P2": 7, "B1": 6}
EXTENSION = dt.date(2024, 1, 8)
BW_K = (1.55, 1.68, 1.85, 2.10)                 # Black Week, Monday to Thursday, Kotikaari's web orders
BF_K = (3.80, 2.40, 2.05, 2.45, 1.60, 1.30, 1.12)  # Black Friday and the six days after it
VOL_K = (4400.0, 800.0)                         # Kotikaari's web lines a day on 1 December 2020 (small parts, bulky)
VOL_H = (1540.0, 136.0)                         # Huippu Sport's on 1 December 2023
LIMIT = {"P1": 24, "P2": 22}
PEAK_WEEKS = tuple(range(46, 51))     # the planning standard 2.1: ISO weeks 46 to 50
CLASSES = ("A", "B", "C", "D", "F")

# pick physics, task minutes a line (WMS task time: travel, pick, confirm), additive
BASE = {"A": 0.60, "B": 0.77, "C": 1.04, "D": 1.52, "F": 1.23}
PER_UNIT = 0.105                      # each unit after the first
ZONE_EXTRA = {"P1": 0.035, "P2": 0.0}
BRAND_EXTRA = 0.055                   # a Huippu Sport line: size and colour label checked at the pick
BULKY_BASE = 2.35                     # B1, reach-truck picks, minutes a line
BULKY_PER_UNIT = 0.42
CONG_KNOT, CONG_POW, CONG_GAMMA = 0.60, 1.9, 0.33   # minutes a line = gamma * max(0, d - knot) ** pow, d pickers an aisle

# minutes of each paid hour a picker is logged in to the zone (starts, breaks, the unpaid lunch's stagger, wrap-up)
LS_DAY = {6: 0.84, 7: 0.97, 8: 0.90, 9: 0.96, 10: 0.80, 11: 0.72, 12: 0.82, 13: 0.92, 14: 0.44}
LS_EVE = {14: 0.44, 15: 0.95, 16: 0.92, 17: 0.94, 18: 0.74, 19: 0.80, 20: 0.93, 21: 0.95, 22: 0.70}
SHIFT_PAID = 8.0

# the client's planners: realised growth of a year's peak level over the last = SLOPE * planned growth + noise
PLAN_SLOPE = 0.42
PLAN_K = {2021: (0.11, 0.06), 2022: (0.25, 0.12), 2023: (0.04, 0.03), 2024: (0.30, 0.09), 2025: (0.10, 0.14),
          2026: (0.14, 0.06), 2027: (0.07, 0.04)}      # (small parts, bulky)
PLAN_H = {2026: (0.15, 0.10), 2027: (0.26, 0.18)}


def aisles(zone, d):
    return AISLES[zone] if d >= EXTENSION else AISLES_OLD[zone]
