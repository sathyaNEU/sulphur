"""World parameters for task14: Penmarra's rental market, the Tenancy Bond Board's register and the Penmarra Statistics
Office's rent panel. Every number the simulation uses is set here, so a sweep or a repair moves one file."""
import datetime as dt

SEED = 1407
D = dt.date

SIM_START = D(2008, 1, 1)
SIM_END = D(2026, 12, 31)          # the truth runs to the end of the December 2026 quarter
MIGRATION = D(2023, 3, 6)          # the online system replaced the legacy register on this day
LEGACY_SCOPE = D(2019, 1, 1)       # the legacy extract holds every bond held on or after this day, with its history
EXTRACT_END = D(2026, 11, 27)      # the online system's extract was cut at the close of this day
REGIONS_FROM = D(2024, 7, 1)       # the 2024 regions replaced the rental areas on the register from this day
PANEL_FRAME = D(2017, 12, 31)      # the rent panel was drawn from the dwellings let on this day
PANEL_FIRST_Q = (2018, 1)
PANEL_LAST_Q = (2026, 3)           # the September 2026 quarter, reference day 15 August 2026
PUB_FIRST_Q = (2019, 1)

# --------------------------------------------------------------------------------------------- geography
# 2024 regions: code, name, share of the 2008 small-landlord stock, house / townhouse / apartment mix,
# growth multiplier on the market path, monthly tenancy-ending multiplier
REGIONS = [
    ("HC", "Hallam Central", 0.150, (0.18, 0.22, 0.60), 1.18, 1.10),
    ("HN", "Hallam North", 0.130, (0.34, 0.28, 0.38), 1.10, 1.22),
    ("HE", "Hallam East", 0.150, (0.42, 0.28, 0.30), 1.06, 1.00),
    ("HS", "Hallam South", 0.140, (0.62, 0.24, 0.14), 0.97, 0.92),
    ("KC", "Kerrow Coast", 0.140, (0.58, 0.27, 0.15), 0.92, 1.05),
    ("MV", "Midvale", 0.150, (0.66, 0.24, 0.10), 0.86, 0.90),
    ("WS", "Westerly", 0.140, (0.72, 0.20, 0.08), 0.80, 0.85),
]
REGION_CODES = [r[0] for r in REGIONS]

# median weekly rent at the start of 2021 by region for a two-bedroom townhouse; type and bedroom factors below
BASE_RENT_2021 = {"HC": 560, "HN": 520, "HE": 505, "HS": 470, "KC": 445, "MV": 395, "WS": 360}
TYPE_FACTOR = {"H": 1.10, "T": 1.00, "A": 0.96, "R": 0.48}
BED_FACTOR = {0: 0.70, 1: 0.80, 2: 1.00, 3: 1.18, 4: 1.34, 5: 1.47}

# --------------------------------------------------------------------------------------------- market
# annual growth of new-letting rents (all regions before the multiplier), by calendar year
MARKET_GROWTH = {2000: 0.035, 2001: 0.035, 2002: 0.036, 2003: 0.038, 2004: 0.040, 2005: 0.040, 2006: 0.042,
                 2007: 0.040, 2008: 0.036, 2009: 0.030, 2010: 0.032, 2011: 0.034, 2012: 0.036, 2013: 0.038,
                 2014: 0.040, 2015: 0.043, 2016: 0.046, 2017: 0.046, 2018: 0.045, 2019: 0.043, 2020: 0.006,
                 2021: 0.055, 2022: 0.095, 2023: 0.088, 2024: 0.063, 2025: 0.036, 2026: -0.004}
# months whose growth departs from their year's even spread (year, month): annual rate in that month
MARKET_MONTH = {(2025, 10): 0.022, (2025, 11): 0.018, (2025, 12): 0.016, (2026, 1): 0.022, (2026, 2): 0.020,
                (2026, 3): 0.016, (2026, 4): 0.010, (2026, 5): 0.004, (2026, 6): -0.004, (2026, 7): -0.012,
                (2026, 8): -0.020, (2026, 9): -0.026, (2026, 10): -0.030, (2026, 11): -0.032, (2026, 12): -0.034}
SEASON = [0.013, 0.012, 0.004, -0.002, -0.006, -0.010, -0.009, -0.005, 0.000, 0.002, 0.000, 0.002]

# all-groups CPI, annual change by quarter (year, quarter): published in the CPI release
CPI_YOY = {
    (2018, 1): 1.8, (2018, 2): 1.9, (2018, 3): 2.0, (2018, 4): 2.1,
    (2019, 1): 2.0, (2019, 2): 1.9, (2019, 3): 1.8, (2019, 4): 1.9,
    (2020, 1): 2.1, (2020, 2): 1.2, (2020, 3): 1.0, (2020, 4): 1.3,
    (2021, 1): 2.0, (2021, 2): 3.1, (2021, 3): 4.0, (2021, 4): 5.2,
    (2022, 1): 6.4, (2022, 2): 7.0, (2022, 3): 7.4, (2022, 4): 7.0,
    (2023, 1): 6.5, (2023, 2): 5.8, (2023, 3): 5.2, (2023, 4): 4.6,
    (2024, 1): 4.1, (2024, 2): 3.6, (2024, 3): 3.4, (2024, 4): 3.2,
    (2025, 1): 3.3, (2025, 2): 3.9, (2025, 3): 5.1, (2025, 4): 4.6,
    (2026, 1): 3.4, (2026, 2): 2.8, (2026, 3): 2.2,
}
CPI_RELEASED = {(2026, 3): D(2026, 10, 21)}   # the September 2026 quarter's CPI came out before the extract

# --------------------------------------------------------------------------------------------- landlords and reviews
# small and medium landlords: chance of a rise at each anniversary, by the anniversary's calendar year
P_RISE = {y: 0.66 for y in range(2000, 2020)}
P_RISE.update({2020: 0.46, 2021: 0.62, 2022: 0.72, 2023: 0.74, 2024: 0.70, 2025: 0.65, 2026: 0.57})
RISE_SLOPE = 0.55        # a rise's median tracks the region's trailing twelve-month new-letting growth at this slope
RISE_FLOOR = 0.012       # ... over this floor
RISE_SIGMA = 0.42        # log-normal spread of a rise around its median
RISE_CAP = 0.16
RELET_LAGGARD = 0.14     # share of small-landlord re-lettings priced off the old rent rather than the market

# top-ups (additional bond) lodged by small and medium landlords: logit by rise size and agent management
TOPUP_LOGIT = (-2.70, 18.0, 0.95)      # intercept, per unit rise, agent-managed
TOPUP_DELAY = (3, 85)                  # days after the rise
EFFECTIVE_FIELD_SHARE = 0.48           # share of small-landlord top-ups whose form carried the date the rise took effect

# operators: build-to-rent and student accommodation
OPERATORS = {
    "A": {"name": "Harbourline Living", "kind": "btr", "review": "december_cpi_plus", "margin": 1.0},
    "B": {"name": "Quayside Residential", "kind": "btr", "review": "november_cpi_plus", "margin": 0.5},
    "C": {"name": "Penmarra Student Halls", "kind": "student", "review": "annual_relet", "margin": 0.0},
}
# blocks: operator, region, opening date, units, street name, number, bedroom mix (0..3)
BLOCKS = [
    ("A", "HC", D(2021, 6, 14), 380, "Wharf", 12, (0.18, 0.46, 0.30, 0.06)),
    ("A", "HC", D(2022, 3, 7), 520, "Customs", 40, (0.15, 0.45, 0.32, 0.08)),
    ("A", "HE", D(2022, 11, 21), 610, "Larch", 3, (0.10, 0.40, 0.38, 0.12)),
    ("A", "HC", D(2023, 9, 4), 700, "Gasworks", 88, (0.16, 0.44, 0.32, 0.08)),
    ("A", "HE", D(2024, 5, 13), 650, "Kowhai", 210, (0.10, 0.40, 0.38, 0.12)),
    ("A", "HC", D(2025, 2, 17), 540, "Ropewalk", 7, (0.18, 0.46, 0.30, 0.06)),
    ("A", "HE", D(2025, 10, 6), 480, "Totara", 155, (0.10, 0.40, 0.38, 0.12)),
    ("B", "HC", D(2022, 8, 8), 640, "Quay", 1, (0.12, 0.48, 0.32, 0.08)),
    ("B", "HN", D(2023, 4, 17), 590, "Observatory", 25, (0.20, 0.50, 0.26, 0.04)),
    ("B", "HE", D(2024, 2, 12), 710, "Brickworks", 60, (0.10, 0.42, 0.38, 0.10)),
    ("B", "HC", D(2024, 10, 14), 760, "Dock", 33, (0.14, 0.48, 0.30, 0.08)),
    ("B", "HN", D(2025, 6, 2), 520, "Kingsland", 141, (0.18, 0.50, 0.28, 0.04)),
    ("A", "HS", D(2019, 10, 14), 560, "Esplanade", 20, (0.14, 0.44, 0.34, 0.08)),
    ("B", "HS", D(2020, 2, 17), 520, "Foundry", 9, (0.12, 0.46, 0.34, 0.08)),
    ("A", "KC", D(2023, 3, 20), 620, "Breakwater", 4, (0.12, 0.42, 0.36, 0.10)),
    ("B", "WS", D(2023, 8, 14), 600, "Harrier", 52, (0.14, 0.46, 0.32, 0.08)),
    ("B", "KC", D(2024, 4, 22), 580, "Lighthouse", 18, (0.12, 0.46, 0.34, 0.08)),
    ("A", "HN", D(2024, 8, 19), 540, "Millrace", 77, (0.16, 0.46, 0.30, 0.08)),
    ("C", "HN", D(2019, 2, 11), 820, "University", 30, (1.0, 0.0, 0.0, 0.0)),
    ("C", "HN", D(2022, 2, 14), 610, "Library", 2, (1.0, 0.0, 0.0, 0.0)),
    ("C", "HN", D(2024, 2, 12), 520, "College", 118, (1.0, 0.0, 0.0, 0.0)),
]
OP_TOPUP_LAG = {"A": (2, 26), "B": (6, 48)}   # days from a portfolio review to its additional bond
OPERATOR_QUALITY = {"A": 1.12, "B": 1.10, "C": 1.00}
STUDENT_RATE_STEP = {2019: 0.0, 2020: 0.03, 2021: 0.035, 2022: 0.045, 2023: 0.06, 2024: 0.055,
                     2025: 0.045, 2026: 0.040}

# --------------------------------------------------------------------------------------------- tenancies
# monthly chance a tenancy ends: months 1 to 11, month 12 (the fixed term's end), months 13 to 24, after
HAZARD_SMALL = (0.0085, 0.175, 0.021, 0.0165)
HAZARD_BTR = (0.012, 0.24, 0.024, 0.021)
P_EXIT_SMALL = 0.034      # chance a small landlord's dwelling leaves the rental market when a tenancy ends
VACANCY_WEEKS = (2.0, 1.6)  # gamma shape, scale for weeks between tenancies (small landlords)
P_TRANSFER_YR = 0.026     # yearly chance a small-landlord dwelling is sold with the tenant in place
P_PARTIES_YR = 0.045      # yearly chance the tenant parties change during a tenancy
LODGE_DELAY = (1, 30)     # calendar days from tenancy start to lodgement (23 working days allowed)
REFUND_DELAY = (2, 34)    # calendar days from the tenancy's end to the refund
P_RESENT = 0.004          # legacy lodgements re-sent in a batch (an exact duplicate row)
P_TENFOLD = 0.0012        # rents keyed with an extra zero
P_NO_BOND = 0.075         # tenancies let without a bond lodged (never on the register)

STOCK_2008 = 47500        # small and medium landlords' rental dwellings at the start of 2008
ENTRY_RATE = 0.022        # new small-landlord rental dwellings a year, as a share of the stock
MEDIUM_SHARE = 0.035      # dwellings owned by a company with 10 to 60 dwellings
AGENT_SHARE = 0.46        # small-landlord dwellings managed by a letting agent

# --------------------------------------------------------------------------------------------- panel
PANEL_SIZE = 3300
PANEL_MIN_STRATUM = 60
PANEL_RESPONSE = 0.93
