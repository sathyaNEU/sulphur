"""Halvergate Mutual's comparison-site motor book: every constant the simulated process uses, in one place.

The process (world.py): drivers shop for private car cover on four comparison sites; each site returns a panel of
insurers' prices; Halvergate's price is its rating model's estimate of the risk times its segment loading; the
driver buys mostly from the cheapest. What Halvergate's model gets wrong about a risk decides whether it is cheapest,
so the business it sells is the business it under-estimated. Sold policies run a year, claim with the seasons,
cancel and renew; a renewal price is capped at the equivalent new-business price.
"""
import datetime as dt

SEED = 210122

# ---- calendar -------------------------------------------------------------------------------------------------
NB_START = dt.date(2025, 1, 1)          # first new-business month carried at policy level
AS_AT = dt.date(2026, 10, 31)           # every extract is as at this date
QUOTE_EXPORT_FROM = dt.date(2025, 1, 1) # the comparison-site market-position extracts start here
REFIT = dt.date(2026, 2, 1)             # rating model v7 live with the 2026 rate review (v6 before)
HIST_START = dt.date(2021, 1, 1)        # claims triangles start (aggregate history)
PLAN_YEAR = 2027

# ---- segments ---------------------------------------------------------------------------------------------------
SEGMENTS = ("u25", "mid", "o65")
SEG_LABEL = {"u25": "under 25", "mid": "25 to 64", "o65": "65 and over"}
AGE_RANGE = {"u25": (17, 24), "mid": (25, 64), "o65": (65, 89)}

# comparison-site quotes Halvergate returned a price on, per month (before seasonality)
QUOTES_PER_MONTH = {"u25": 55000, "mid": 120000, "o65": 30000}
QUOTE_SEASON = [1.18, 1.05, 1.07, 0.98, 0.97, 0.94, 0.95, 0.88, 1.02, 1.00, 0.98, 0.98]   # Jan..Dec

# true expected claim frequency by type per vehicle-year (annual average), and its calendar-month pattern
CLAIM_TYPES = ("AD", "TPPD", "TPBI", "THEFT", "WS")
FREQ = {"u25": {"AD": 0.150, "TPPD": 0.085, "TPBI": 0.040, "THEFT": 0.012, "WS": 0.055},
        "mid": {"AD": 0.072, "TPPD": 0.038, "TPBI": 0.016, "THEFT": 0.007, "WS": 0.052},
        "o65": {"AD": 0.066, "TPPD": 0.036, "TPBI": 0.013, "THEFT": 0.005, "WS": 0.047}}
# winter darkness, ice and longer evenings: accidental damage, third-party damage and theft peak Nov to Feb;
# windscreens peak in late winter (frost) and summer (gravel); the month factors average 1 over the year
CLAIM_SEASON = {
    "AD":    [1.30, 1.22, 1.04, 0.92, 0.86, 0.82, 0.84, 0.85, 0.92, 1.02, 1.12, 1.25],
    "TPPD":  [1.24, 1.18, 1.03, 0.94, 0.89, 0.86, 0.87, 0.88, 0.93, 1.02, 1.11, 1.20],
    "TPBI":  [1.12, 1.08, 1.01, 0.96, 0.94, 0.93, 0.93, 0.95, 0.97, 1.01, 1.05, 1.10],
    "THEFT": [1.24, 1.10, 0.96, 0.88, 0.84, 0.82, 0.85, 0.90, 0.96, 1.08, 1.22, 1.30],
    "WS":    [1.18, 1.22, 1.06, 0.90, 0.88, 0.96, 1.04, 1.02, 0.90, 0.88, 0.92, 1.06]}
RISK_SD = {"u25": 0.40, "mid": 0.38, "o65": 0.36}          # sd of log true risk across drivers

# mean claim cost at 1 January 2025 cost levels (GBP), lognormal shape, the cap the planning basis applies
SEV_MEAN = {"AD": 2460.0, "TPPD": 2070.0, "TPBI": 7400.0, "THEFT": 5770.0, "WS": 335.0}
SEV_SD = {"AD": 0.85, "TPPD": 0.80, "TPBI": 1.25, "THEFT": 0.70, "WS": 0.35}
CLAIM_CAP = 100000.0
SEV_INFLATION = {2021: 0.034, 2022: 0.092, 2023: 0.118, 2024: 0.074, 2025: 0.061, 2026: 0.048}

# rating model error (log scale): v6 before the refit, v7 after; a share of it is the market's common misreading
MODEL_SD = {("u25", "v6"): 0.20, ("u25", "v7"): 0.20,
            ("mid", "v6"): 0.24, ("mid", "v7"): 0.10,
            ("o65", "v6"): 0.09, ("o65", "v7"): 0.09}
COMMON_SHARE = 0.30
RIVALS = {"u25": 8, "mid": 10, "o65": 6}                    # rival brands on a site's panel
RIVAL_SD = {"u25": 0.17, "mid": 0.18, "o65": 0.12}
RIVAL_LOAD = {"u25": 1.50, "mid": 1.575, "o65": 1.70}        # rivals' price over true cost, 2026 level
RIVAL_LOAD_SD = {"u25": 0.05, "mid": 0.05, "o65": 0.05}   # each rival brand's quote-to-quote spread

# conversion on a price-led panel: the driver shops with P_SHOP and picks by rank
P_SHOP = 0.56
P_RANK = {1: 0.62, 2: 0.020, 3: 0.007}
P_RANK_OTHER = 0.0016

# Halvergate's 2026 loading over its predicted cost (after the 2026 rate changes), and its dated rate changes
LOAD_2026 = {"u25": 1.55, "mid": 1.40, "o65": 1.666}
RATE_CHANGES = [  # (date, segment, change) on comparison-site new business
    (dt.date(2024, 3, 1), "u25", 0.07), (dt.date(2024, 3, 1), "mid", 0.05), (dt.date(2024, 3, 1), "o65", 0.04),
    (dt.date(2025, 3, 1), "u25", 0.06), (dt.date(2025, 3, 1), "mid", 0.04), (dt.date(2025, 3, 1), "o65", 0.03),
    (dt.date(2026, 2, 1), "u25", 0.08), (dt.date(2026, 2, 1), "mid", 0.03), (dt.date(2026, 2, 1), "o65", 0.02),
]
# the rivals' comparison-site price level relative to its 2026 level, by year (the market hardened into 2025)
RIVAL_LEVEL = {2024: 0.93, 2025: 0.975, 2026: 1.00}

# ---- the 2027 planning basis (filed in the executive pricing team's planning paper) ----------------------------
TARGET_LR = 0.75
CLAIMS_INFLATION_2027 = 0.055        # 2026 cost levels to 2027 cost levels, every capped claim
MARKET_MOVE_2027 = 0.02              # rivals' comparison-site prices on 1 January 2027
PROPOSAL_O65 = -0.03                 # the commercial proposal for over-65s

# ---- cancellations and payment ---------------------------------------------------------------------------------
MONTHLY_PAY_SHARE = {"u25": 0.78, "mid": 0.52, "o65": 0.31}
COOLING_OFF = 0.012
LAPSE_MIDTERM = {"u25": 0.14, "mid": 0.07, "o65": 0.04}      # per policy-year, non-payment and vehicle sold

# ---- the over-65 renewal book ------------------------------------------------------------------------------------
O65_RENEWALS_2027 = 165000           # over-65 comparison-site customers due to renew in 2027
RENEWAL_INTENT_LOAD = 1.11           # intended renewal price over the equivalent new-business price
RETENTION_BASE = 0.875               # retention at an unchanged price
RETENTION_SLOPE = 2.6                # logit slope per unit of renewal price change
EXPENSE_COMMISSION = {"Kitecompare": 52.0, "Covertide": 48.0, "Brightquote": 44.0, "Pricelark": 55.0}
EXPENSE_SERVICING = 34.0

SITES = ("Kitecompare", "Covertide", "Brightquote", "Pricelark")
SITE_SHARE = {"Kitecompare": 0.34, "Covertide": 0.27, "Brightquote": 0.22, "Pricelark": 0.17}
