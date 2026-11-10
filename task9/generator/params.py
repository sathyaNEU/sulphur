"""task9: the world's paperwork. Positions, sizes, limits, names and dates are authored here; no market value is.

Every market value the build uses is read from raw/ by market.py (public Cboe index histories, used as is).
"""
import datetime as dt

import pandas as pd

FOUNDATION = "Carrow Fields Foundation"
FOUNDATION_CITY = "Minneapolis, Minnesota"
CUSTODIAN = "Larkhill Trust Company"
ZONE = "America/Chicago"
CT = dt.timezone(dt.timedelta(hours=-6))          # Central Standard Time in November
CDT = dt.timezone(dt.timedelta(hours=-5))

# people (drawn with guard.py names --geo US --seed 908)
TREASURY = "Stephanie Bowman"                      # director of treasury
CIO = "Edward Stewart"                             # chief investment officer
OPS = "Gloria Wilkins"                             # investment operations, keeps the blotter

# the three dealers of the panel: code, name, how each writes its trade reference and its dates
DEALERS = {
    "BSS": dict(name="Brecon Sound Securities LLC", short="Brecon Sound", city="New York", datefmt="%Y-%m-%d", basis="VEGA"),
    "ACM": dict(name="Altamere Capital Markets", short="Altamere", city="Chicago", datefmt="%m/%d/%Y", basis="VARIANCE"),
    "WXB": dict(name="Wexcombe Bank, N.A.", short="Wexcombe", city="Charlotte", datefmt="%d-%b-%Y", basis="VEGA"),
}
PAIRS = [("BSS", "ACM"), ("ACM", "WXB"), ("WXB", "BSS")]    # the two dealers of a month's sale, in rotation

REVIEW = pd.Timestamp("2026-11-09")               # the review date: closes through this day
STATEMENT = pd.Timestamp("2026-10-30")            # the dealers' last month-end statements
SLEEVE_FIRST = (2021, 7)                          # the sleeve's first sale month
OLD_MAT = 12                                      # the ladder the sleeve runs, months
OLD_CONF_VEGA = 25_000                            # US dollars a volatility point, each of the two confirmations a month
OLD_SIZE = 2 * OLD_CONF_VEGA                      # the 12-month ladder's size: US dollars a point per monthly sale
NEW_MAT = 3                                       # the ladder the investment office wants to add
ALT_MAT = 6                                       # the alternative on the dealers' term sheet
PROPOSED = 200_000                                # the size the investment office tabled, US dollars a point
PLAN_YEAR = 2027
FIRST_NEW = (2027, 1)                             # the new ladder's first sale month
PER = 100_000                                     # the size per-ladder figures are quoted for

REF_ASSETS = 1_487_600_000                        # the endowment's audited value at 30 June 2026
FY_END = pd.Timestamp("2026-06-30")
LIM_SETTLE_PCT = 2.0
LIM_COLL_PCT = 3.0
LIM_SETTLE = REF_ASSETS * LIM_SETTLE_PCT / 100.0  # US dollars, net settlement paid in a calendar year
LIM_COLL = REF_ASSETS * LIM_COLL_PCT / 100.0      # US dollars, collateral posted on a day
SIZE_STEP = 100                                   # sizes are set to USD 100 a point
HOT = 35.0                                        # the level of the 30-day index the overlap's stressed days are read above

# paperwork events in the blotter (authored; they move no result once handled)
# both sit on swaps that have since expired, so no open position turns on how they are read
AMENDED = (2023, 8, "ACM", 250_000)               # the August 2023 Altamere confirmation first booked at ten times its size
NOVATED = (2024, 3, "WXB", "BSS", pd.Timestamp("2024-06-17"))   # the March 2024 Wexcombe confirmation novated to Brecon Sound
RESENT = ("ACM", pd.Timestamp("2024-03-15"))      # a valuation file delivered twice
MISSING = {"WXB": [pd.Timestamp("2022-11-25"), pd.Timestamp("2023-11-24"), pd.Timestamp("2025-07-03")]}   # days a dealer sent no file

# dealers' valuation differences from the published term structure, in volatility points (authored noise)
DEALER_BIAS = {"BSS": 0.04, "ACM": -0.06, "WXB": 0.09}
DEALER_DAY_SD = 0.12
DEALER_SWAP_SD = 0.05
COLL_ROUND = 10_000                               # collateral is called in multiples of USD 10,000
