"""task9 (architecture 10): Brindlemoor Securities' credit desk on the Tidewell request-for-quote platform.

Every constant of the simulated world. The market itself (Treasury curve, Moody's Baa and Aaa, SOFR, VIX) is read
from the public series under raw10/; nothing here is a market value.
"""
SEED = 1010

FIRM = "Brindlemoor Securities"
DESK = "Brindlemoor credit trading"
PLATFORM = "Tidewell Credit Network"
PRICER = "Ashcote Evaluations"
HEAD = "Yolanda Cobb"            # head of credit trading, owner of the quoting policy
STRAT = "James Flowers"          # the desk's strategist, keeps the auto-quoter's schedule

START = "2023-01-03"             # first day of the record
END = "2026-11-06"               # its last day (the requests export and the tape are cut here)
REVIEW = "2026-11-09"            # the committee's papers are put together on this morning's pull
BASE_FROM, BASE_TO = "2025-11-01", "2026-10-31"   # the plan's base period: the twelve months to October 2026
MIGRATION = "2025-04-07"         # Tidewell's export moved to its second generation on this day
ZONE = "America/New_York"

# ---- the bond universe -----------------------------------------------------------------------------------------
N_ISSUERS = 96
N_BONDS = 236
RATINGS = ["AA", "A", "BBB", "BB", "B", "CCC"]
RATING_SHARE = [0.08, 0.27, 0.35, 0.17, 0.10, 0.03]
IG = {"AA", "A", "BBB"}
# spread level at the start of the record, bp, as a multiple of Moody's Baa spread (IG names near Aaa or Baa,
# high yield a multiple of it)
SPREAD_MULT = {"AA": 0.42, "A": 0.62, "BBB": 0.95, "BB": 1.55, "B": 2.30, "CCC": 4.20}
CREDIT_BETA = {"AA": 0.75, "A": 0.85, "BBB": 1.00, "BB": 1.20, "B": 1.35, "CCC": 1.60}
VIX_BETA = {"AA": 0.0, "A": 0.0, "BBB": 0.15, "BB": 0.55, "B": 0.85, "CCC": 1.30}   # bp of spread per VIX point
NEWS_RATE = {"AA": 0.4, "A": 0.5, "BBB": 0.6, "BB": 0.7, "B": 0.9, "CCC": 1.2}      # larger issuer events a year
NEWS_SD = {"AA": 5.0, "A": 7.0, "BBB": 9.0, "BB": 16.0, "B": 22.0, "CCC": 34.0}    # bp of spread per event
NEWS_DAYS = (1, 6)               # an event reaches the bond's value over 1 to 6 trading days
IDIO_SD = {"AA": 0.25, "A": 0.3, "BBB": 0.4, "BB": 0.8, "B": 1.2, "CCC": 2.0}       # bp a day, the information flow

# ---- evaluated prices (Ashcote) --------------------------------------------------------------------------------
# the curve and the rating-sector spread move are taken in daily; the issuer's own move is taken in toward the
# market's level by each print the bond shows and by a slow daily review otherwise
EVAL_PRINT_PULL = 0.40
EVAL_ISSUER_DAILY = 0.04                     # the evaluator's daily review of an issuer's news, with no print
EVAL_OWN_DAILY = {"liquid": 0.12, "medium": 0.05, "thin": 0.025}   # a bond's own share, with no print of its own
EVAL_NOISE = {"IG": 0.6, "HY": 2.0}          # cents, the evaluator's own error on a day

# ---- clients ---------------------------------------------------------------------------------------------------
CLIENT_TYPES = ["AM", "INS", "HF", "RET"]
CLIENT_NAMES = {"AM": "asset manager", "INS": "insurer", "HF": "hedge fund", "RET": "wealth platform"}
N_CLIENTS = {"AM": 118, "INS": 38, "HF": 72, "RET": 54}
INFORMED_SHARE = {"AM": 0.08, "INS": 0.0, "HF": 0.38, "RET": 0.0}   # clients who see issuer news early
INFORMED_HORIZON = 5                         # an informed client sees the issuer's move this many days ahead
INFORMED_THRESHOLD = {"IG": 2.0, "HY": 4.5}  # bp: the coming move it acts on
INFORMED_DAILY = {"AM": 0.04, "HF": 0.30}    # chance a day it sends a request while the coming move is that large
DEALERS_ASKED = {"AM": (4, 7), "INS": (3, 6), "HF": (3, 5), "RET": (5, 9)}
REQ_LAM_POW = 0.95                           # how strongly requests follow a bond's trading
RIVAL_BASE = {"IG": 1.12, "HY": 1.18}         # rivals' typical half-spread, as a multiple of the desk's first schedule
SIZE = {"AM": (14.6, 0.8), "INS": (15.3, 0.7), "HF": (14.4, 0.7), "RET": (11.4, 0.9)}   # log face, mean and sd
HY_PREF = {"AM": 0.33, "INS": 0.18, "HF": 0.62, "RET": 0.40}

# requests the desk receives a day at the start of the record, and their growth a year as the platform takes share
RFQ_PER_DAY = 200.0
RFQ_GROWTH = 0.11
TYPE_SHARE = {"AM": 0.47, "INS": 0.10, "HF": 0.27, "RET": 0.16}

# ---- rival dealers -------------------------------------------------------------------------------------------
# two large dealers see enough flow to read informed requests and mark thin bonds near the market; the others
# mark on evaluated prices as the desk does
DEALERS = ["D01", "D02", "D03", "D04", "D05", "D06", "D07", "D08", "D09"]
LARGE = {"D01", "D02"}
DEALER_WEIGHT = [0.20, 0.18, 0.11, 0.10, 0.10, 0.09, 0.08, 0.07, 0.07]
DEALER_AGGR = [0.92, 0.95, 1.02, 1.05, 1.00, 1.08, 1.12, 0.98, 1.15]     # half-spread multiple
DETECT = {"large": 0.68, "regular": 0.12}    # chance a dealer reads an informed request and widens
WIDEN = 2.6                                  # half-spread multiple a dealer quotes on a request it reads as informed
AXE_P = {"liquid": 0.21, "medium": 0.12, "thin": 0.06}   # chance a given rival is axed the client's way
AXE_H = 0.12                                 # an axed rival quotes this share of its half-spread
QUOTE_SD = 0.18                              # a rival's quote noise, as a share of its half-spread
LARGE_MARK_SD = 0.25                         # large dealers' own marks: share of the issuer move they have not seen

# ---- the desk's auto-quoter ---------------------------------------------------------------------------------
BUCKETS = ["liquid", "medium", "thin"]
SEGMENTS = [(b, l, t) for b in ("IG", "HY") for l in BUCKETS for t in CLIENT_TYPES]
# the schedule: half-spread in cents per 100 face against the evaluated mid
SCHEDULE_V1 = {
    ("IG", "liquid"): {"AM": 4.0, "INS": 4.0, "HF": 6.0, "RET": 12.0},
    ("IG", "medium"): {"AM": 7.0, "INS": 6.0, "HF": 10.0, "RET": 18.0},
    ("IG", "thin"): {"AM": 12.0, "INS": 10.0, "HF": 16.0, "RET": 28.0},
    ("HY", "liquid"): {"AM": 15.0, "INS": 14.0, "HF": 20.0, "RET": 35.0},
    ("HY", "medium"): {"AM": 25.0, "INS": 22.0, "HF": 32.0, "RET": 50.0},
    ("HY", "thin"): {"AM": 40.0, "INS": 35.0, "HF": 55.0, "RET": 75.0},
}
V2_DATE, V2_CHANGES = "2024-07-01", {("IG", "liquid", "AM"): 2.5, ("IG", "medium", "INS"): 4.5}
V3_DATE, V3_CHANGES = "2025-03-03", {("HY", "thin", "HF"): 65.0}
PROPOSED = {                                 # the draft 2027 schedule's changes
    ("IG", "liquid", "AM"): 1.5,
    ("IG", "medium", "AM"): 5.5,
    ("IG", "medium", "HF"): 8.0,
    ("IG", "thin", "INS"): 8.0,
    ("HY", "liquid", "AM"): 12.5,
    ("HY", "liquid", "HF"): 16.5,
    ("HY", "medium", "AM"): 21.0,
    ("HY", "medium", "HF"): 27.0,
    ("HY", "thin", "AM"): 34.0,
    ("HY", "thin", "HF"): 57.0,
}
SIZE_MULT = [(("IG", 5_000_000), 1.30), (("HY", 1_000_000), 1.20), (("ANY", 100_000), 1.50)]
STRESS = [(20.0, 1.0), (30.0, 1.3), (999.0, 1.7)]     # VIX at the prior close below the bound: multiple
SKEW = 0.35                                 # inventory skew, share of the distance at the bond's full limit
JITTER = 0.06                               # the quoter's own noise, share of the half-spread
POS_LIMIT = {"IG": 25_000_000, "HY": 10_000_000}       # a bond's inventory limit, face
PASS_SHARE = 0.025                          # requests the quoter passes for reasons of its own

# ---- inventory, offloading and funding ------------------------------------------------------------------------
OFFLOAD = {"liquid": 0.45, "medium": 0.24, "thin": 0.10}     # chance a position is sold to dealers on a day
BUCKET_PRINTS = (150, 60)                    # prints a quarter: liquid at or over the first, thin under the second
D2D_HALF = {("IG", "liquid"): 2.0, ("IG", "medium"): 4.0, ("IG", "thin"): 8.0,
            ("HY", "liquid"): 7.0, ("HY", "medium"): 14.0, ("HY", "thin"): 26.0}   # cents, dealer-to-dealer cost
FUND_SPREAD = 0.0030                        # the desk funds inventory at SOFR plus 0.30 per cent

# ---- the tape --------------------------------------------------------------------------------------------------
CAP = {"IG": 5_000_000, "HY": 1_000_000}    # sizes over these print as 5MM+ and 1MM+
CANCEL_P, CORRECT_P, ASOF_P = 0.012, 0.018, 0.005
OTHER_PRINT_SCALE = 0.6                     # other customer trades a bond prints a day, as a share of its trading

# ---- the plan --------------------------------------------------------------------------------------------------
PLAN_DAYS = 251                             # bond-market trading days in 2027
RANGE_P = (10, 90)
SIMS = 4000
BLOCK = 21                                  # the golden's block length, trading days
LEAGUE_TABLE = True                         # the platform's monthly league table ships (unused by the golden)
