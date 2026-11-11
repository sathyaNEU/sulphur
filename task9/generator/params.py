"""task9: the world's paperwork. The platform, its pods, its rules and its people are authored here; no market value
is. Every market return the pods ride on is computed by market.py from the public series under raw/."""
import datetime as dt

import pandas as pd

PLATFORM = "Harbourne Capital"
PLATFORM_LEGAL = "Harbourne Capital Management LP"
CITY = "New York, New York"
ADMIN = "Kestrel Fund Services"            # the fund administrator
ZONE = "America/New_York"
ET = dt.timezone(dt.timedelta(hours=-5))   # Eastern Standard Time in November
EDT = dt.timezone(dt.timedelta(hours=-4))

# people (drawn with guard.py names --geo US --seed 909)
CIO = "Christine Owen"                     # chief investment officer, chairs the allocation committee
CRO = "Nicholas Riddle"                    # chief risk officer
CFO = "Kathryn Roberts"                    # chief financial officer

LAUNCH = pd.Timestamp("2017-01-03")        # the platform's first trading day
LAST_DAY = pd.Timestamp("2026-11-06")      # the last day in the risk system's export (a Friday)
REVIEW = pd.Timestamp("2026-11-09")        # the review's as-of date
PLAN_YEAR = 2027
BUDGET_PLAN = 21.50e9     # the capital the draft 2027 plan runs (targets)
LEAD = 37                 # trading days from the review's as-of date to the plan year's first trading day (4 January 2027)
PLAN_YEARS = list(range(2018, 2027))     # the plans on file, each made at the January review

# the platform's rules (filed in the capital review policy and the PM agreements)
PAYOUT = 0.18          # share of a pod's positive calendar-year P&L paid to its PM team
HALVE_DD = 0.05        # a pod's capital is halved when its year-to-date P&L falls this far below its year-to-date peak
STOP_DD = 0.075        # a pod is closed at this drawdown, measured the same way
HURDLE = 0.015         # an increase must add this much net P&L a year on the capital it adds, after payout and funding
PLATFORM_COST_2027 = 218_400_000   # the platform's own costs in the 2027 budget (technology, data, operations, people)
# the 2027 budget's lines, USD
COST_LINES_2027 = [("Technology and infrastructure", 61_200_000), ("Market data and research", 38_500_000), ("Operations and finance", 44_900_000),
                   ("Risk, legal and compliance", 27_600_000), ("Central staff and premises", 46_200_000)]
# each past plan's platform costs, USD (the budget the plan carried)
PLATFORM_COST = {2017: 124_900_000, 2018: 131_600_000, 2019: 140_200_000, 2020: 148_000_000, 2021: 158_300_000, 2022: 168_900_000,
                 2023: 177_100_000, 2024: 185_600_000, 2025: 195_800_000, 2026: 206_300_000}
FIN_SPREAD = 0.0035    # each pod is charged the 3-month bill rate plus this on 20 per cent of its capital (funding)
FIN_SHARE = 0.20

# capacity and the allocation process (the world's truth; never filed)
C0 = 150e6             # the capital at which a pod's base edge is stated
THETA = 0.40           # alpha per dollar scales with capital to the power -THETA
KAPPA = 0.25           # the annual review moves capital by exp(KAPPA x the pod's Sharpe ratio over its last three years) before the budget is applied
HIRE_SKILL = 0.45      # a new pod's starting capital rises with the record the PM brings (its base edge), log scale
GROUP_TILT = 0.08       # and with the group's own Sharpe ratio over the year just ended (the committee's view of the strategy)
DISCRETION = 0.08       # the committee's own judgment on top of the record (log scale)
CYCLE = 0.0           # each group's common edge shock carries this much of itself into the next year
# the capital the platform runs at each January review (the budget the reviews are scaled to), USD
# the pods the platform keeps running each year (hiring at the start of each quarter), and the capital it runs
PODS = {2017: 60, 2018: 64, 2019: 68, 2020: 72, 2021: 77, 2022: 82, 2023: 86, 2024: 90, 2025: 95, 2026: 100}
BUDGET = {y: round(n * 0.2035e9, -7) for y, n in PODS.items()}
K_MIN, K_MAX = 40e6, 1_400e6
BAND = 0.10           # a review leaves a pod's capital alone when its record moves it by less than this
# a new pod starts at 25 per cent of its target capital, half after six months and its full target after twelve
RAMP = [(0, 0.25), (126, 0.50), (252, 1.00)]
LEAVE_RATE = 0.12      # a year: PM teams that leave the platform for reasons of their own

# strategy groups: launch count, factor loadings (mean, sd), idiosyncratic volatility a year, base edge (mean, sd),
# and the hiring weight (gy, a common edge shock for the group each year, is kept at zero)
GROUPS = {
    "EQLS":   dict(name="Equity long/short", n0=12, load={"MKT": (0.10, 0.05), "TECH": (0.0, 0.12)}, iv=0.050, a0=(0.105, 0.030), hire=0.20, gy=0.0),
    "QEQ":    dict(name="Quantitative equity", n0=5, load={"MKT": (0.0, 0.03)}, iv=0.045, a0=(0.100, 0.025), hire=0.09, gy=0.0),
    "RATES":  dict(name="Rates", n0=5, load={"RATES": (0.0, 0.22), "CURVE": (0.0, 0.15)}, iv=0.045, a0=(0.090, 0.025), hire=0.10, gy=0.0),
    "FX":     dict(name="Currencies", n0=6, load={"FXCARRY": (0.75, 0.12), "USD": (0.0, 0.18)}, iv=0.045, a0=(0.050, 0.020), hire=0.12, gy=0.0),
    "CREDIT": dict(name="Credit", n0=20, load={"CREDIT": (1.45, 0.20), "MKT": (0.03, 0.02)}, iv=0.030, a0=(0.040, 0.015), hire=0.34, gy=0.0),
    "COMDTY": dict(name="Commodities", n0=6, load={"OIL": (0.0, 0.035)}, iv=0.055, a0=(0.100, 0.030), hire=0.07, gy=0.0),
    "VOLARB": dict(name="Volatility", n0=6, load={"VOL": (0.05, 0.02), "MKT": (0.02, 0.02)}, iv=0.050, a0=(0.095, 0.025), hire=0.08, gy=0.0),
}
GROUP_ORDER = ["EQLS", "QEQ", "RATES", "FX", "CREDIT", "COMDTY", "VOLARB"]
SEED = 403

# the 2023 risk system migration: the new export reports P&L in USD thousands and capital in USD millions
MIGRATION = pd.Timestamp("2023-07-03")
REORG = pd.Timestamp("2022-04-01")         # pod codes re-issued when the platform reorganised its books
RESENT = pd.Timestamp("2021-03-12")        # a day the old system delivered twice
