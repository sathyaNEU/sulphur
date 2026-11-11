"""World parameters for Medienhaus Brückenhafen (task1 architecture 3). Every constant the simulator, the documents and
the write-up use is read from here.

Calendar: month index 0 is January 2023; the subscription system's export starts there (subscriptions running in
January 2023 come with their original start dates and nothing before); the reading log starts in January 2024; the
cut is the end of October 2026. The April 2025 and April 2027 list-price rises take effect at each subscription's first
billing on or after the 1st of April."""

SEED = 3107

M0_YEAR, M0_MONTH = 2023, 1
CUT = 45                 # October 2026
READ_FROM = 12           # January 2024
RISE_2025 = 27           # April 2025
NOTICE_2025 = 25         # February 2025: the notice letters
RISE_2027 = 51           # April 2027
PLAN0, PLAN1 = 48, 59    # the 2027 plan's starts, January to December 2027
HORIZON = 36             # months of a start's value
BASE_END = 59            # December 2027
VAT = 0.07               # reduced rate on newspapers and e-papers, prices quoted gross

TITLES = ["BHR", "GAZ", "KBO", "ELN"]
TITLE_NAME = {"BHR": "Brückenhafener Rundschau", "GAZ": "Grevenauer Anzeiger", "KBO": "Kreisblatt Ostheide",
              "ELN": "Elmsbacher Nachrichten"}
# full monthly price, gross: before April 2025, from April 2025, from April 2027
PRICE = {"BHR": (15.99, 17.99, 19.99), "GAZ": (13.99, 15.99, 17.99), "KBO": (13.99, 15.99, 17.99),
         "ELN": (11.99, 13.99, 15.99)}
TITLE_H = {"BHR": 0.10, "GAZ": 0.0, "KBO": -0.05, "ELN": 0.05}

CHANNELS = ["SOC", "SEA", "PART", "TEL", "APP", "DIR"]
PAID = ["SOC", "SEA", "PART", "TEL", "APP"]
CH_NAME = {"SOC": "paid social", "SEA": "paid search", "PART": "cashback partners", "TEL": "telemarketing",
           "APP": "app-store campaigns", "DIR": "direct (paywall)"}
OLD_CODE = {"SOC": "FB", "SEA": "SEM", "PART": "AFF", "TEL": "TM", "APP": "ASA", "DIR": "ORG"}
CODE_SWITCH = 26         # March 2025: the marketing system renamed its channel codes

# offers: intro months, intro price as a share of the full price or a fixed gross price
OFFERS = {
    "PM1": {"name": "Probemonat 0,99 €", "months": 1, "fixed": 0.99},
    "M3E1": {"name": "3 Monate für je 1 €", "months": 3, "fixed": 1.00},
    "H6": {"name": "6 Monate zum halben Preis", "months": 6, "share": 0.50},
    "G3": {"name": "3 Monate gratis", "months": 3, "fixed": 0.00},
    "J12": {"name": "12 Monate 40 % günstiger", "months": 12, "share": 0.60},
}

# the paid lines: (channel, title) -> history of offers [(from month, offer)], 2027 offer, starts a month (2026 level)
LINES = {
    ("SOC", "BHR"): ([(0, "PM1"), (20, "M3E1")], "M3E1", 23),
    ("SOC", "GAZ"): ([(0, "PM1"), (20, "M3E1")], "H6", 15),
    ("SOC", "KBO"): ([(0, "PM1")], "M3E1", 13),
    ("SOC", "ELN"): ([(0, "PM1"), (26, "H6")], "H6", 9),
    ("SEA", "BHR"): ([(0, "M3E1"), (17, "H6")], "H6", 21),
    ("SEA", "GAZ"): ([(0, "M3E1")], "M3E1", 14),
    ("SEA", "KBO"): ([(0, "PM1"), (24, "M3E1")], "H6", 12),
    ("SEA", "ELN"): ([(0, "M3E1")], "M3E1", 8),
    ("PART", "BHR"): ([(0, "H6")], "H6", 17),
    ("PART", "GAZ"): ([(0, "PM1"), (12, "J12"), (21, "H6")], "J12", 11),
    ("PART", "KBO"): ([(0, "H6")], "H6", 10),
    ("TEL", "BHR"): ([(0, "M3E1"), (10, "G3"), (16, "J12"), (26, "G3")], "J12", 19),
    ("TEL", "GAZ"): ([(0, "G3")], "G3", 15),
    ("TEL", "KBO"): ([(0, "M3E1"), (14, "G3")], "J12", 13),
    ("TEL", "ELN"): ([(0, "G3")], "G3", 9),
    ("APP", "BHR"): ([(0, "J12"), (24, "PM1")], "J12", 15),
    ("APP", "GAZ"): ([(0, "PM1")], "PM1", 9),
    ("APP", "KBO"): ([(0, "PM1"), (29, "M3E1")], "M3E1", 8),
}
DIR_STARTS = {"BHR": 66, "GAZ": 40, "KBO": 36, "ELN": 21}
# the paywall's offer by calendar month (Black Friday and the summer run half price)
DIR_OFFER = {1: "PM1", 2: "PM1", 3: "M3E1", 4: "PM1", 5: "PM1", 6: "H6", 7: "H6", 8: "PM1", 9: "M3E1",
             10: "PM1", 11: "H6", 12: "PM1"}
DIR_BF_ANNUAL = (10, 22)   # November 2023 and November 2024: the Black Friday offer was the annual one
LINE_GROWTH = 0.10        # starts grew about this much from 2023 to 2026
START_SEASON = {1: 1.30, 2: 1.08, 3: 1.12, 4: 1.0, 5: 0.95, 6: 0.85, 7: 0.72, 8: 0.78, 9: 1.05, 10: 1.08,
                11: 1.22, 12: 0.85}
NEWS = {13: 0.25, 17: 0.20, 18: 0.18, 24: 0.30, 25: 0.42, 26: 0.12, 44: 0.10}   # starts and reading lift

# the 2027 plan's planned cost per net start by line (euros); 2026's realised cost per start ran about CPA_2027 below
PLAN_CPA = {("SOC", "BHR"): 38.0, ("SOC", "GAZ"): 66.0, ("SOC", "KBO"): 31.5, ("SOC", "ELN"): 57.5,
            ("SEA", "BHR"): 60.0, ("SEA", "GAZ"): 44.5, ("SEA", "KBO"): 49.0, ("SEA", "ELN"): 41.5,
            ("PART", "BHR"): 67.5, ("PART", "GAZ"): 52.0, ("PART", "KBO"): 63.5, ("TEL", "BHR"): 71.0,
            ("TEL", "GAZ"): 63.0, ("TEL", "KBO"): 63.0, ("TEL", "ELN"): 69.5, ("APP", "BHR"): 58.5,
            ("APP", "GAZ"): 53.0, ("APP", "KBO"): 39.0}
HURDLE = 3.5               # a line is funded when its expected 36-month net revenue per start is at least this
                           # many times its planned cost per start
# cost per start (2026 level, euros) by line, from which the marketing spend history is drawn
CPA_OLD = {("SOC", "BHR"): 53, ("SOC", "GAZ"): 47, ("SOC", "KBO"): 44, ("SOC", "ELN"): 40,
       ("SEA", "BHR"): 58, ("SEA", "GAZ"): 50, ("SEA", "KBO"): 47, ("SEA", "ELN"): 41,
       ("PART", "BHR"): 46, ("PART", "GAZ"): 42, ("PART", "KBO"): 41,
       ("TEL", "BHR"): 76, ("TEL", "GAZ"): 66, ("TEL", "KBO"): 65, ("TEL", "ELN"): 58,
       ("APP", "BHR"): 63, ("APP", "GAZ"): 52, ("APP", "KBO"): 50}

# households: reading habit h and price sensitivity p, both standard normal around a channel mean
H_MEAN = {"SOC": -0.15, "SEA": 0.20, "PART": -0.30, "TEL": -0.10, "APP": 0.00, "DIR": 0.50}
P_MEAN = {"SOC": 0.30, "SEA": -0.10, "PART": 0.50, "TEL": 0.20, "APP": 0.00, "DIR": -0.30}
HP_CORR = -0.30
# drifts in the reading habit of new starts: channel -> (ramp start month, ramp end month, shift)
DRIFT = {"SOC": (32, 35, -0.90), "PART": (28, 30, -0.70), "SEA": (24, 26, +0.45)}
COHORT_SD = 0.20          # a line-month's shared habit shift
COHORT_SU_SD = 0.15       # a line-month's shared shift on the end-of-intro exit (logit)

# end of the introductory price: logit of leaving
SU_A0 = -2.02
SU_CH = {"SOC": 0.30, "SEA": 0.05, "PART": 0.30, "TEL": 0.55, "APP": 0.20, "DIR": -0.10}
SU_TITLE = {"BHR": 0.05, "GAZ": 0.0, "KBO": -0.05, "ELN": 0.0}
SU_DEPTH = 2.40           # per unit of discount depth (1 - intro / full)
SU_LEN = -0.38            # per log intro month
SU_PRICE = 3.00           # per log of the full price against the title's pre-2025 full price
SU_P = 0.50               # per unit of price sensitivity
SU_H = 0.0               # the decision rides on price, not on reading habit
INTRO_HAZ = 0.004         # a month during the introductory price

# after the end of the intro: monthly hazard of cancelling
POST_BASE = 0.050
POST_FLOOR = 0.36
POST_TAU = 8.0
POST_CH = {"SOC": 1.12, "SEA": 0.95, "PART": 1.18, "TEL": 1.22, "APP": 1.08, "DIR": 0.86}
POST_H = 0.44             # hazard falls by this per unit of reading habit (log scale)
POST_P = 0.10
COHORT_POST_SD = 0.10
SUMMER = {7: 1.12, 8: 1.10}

# payment failures a month, by payment route; a failed debit is collected the next month in RECOVER of cases
INVOL = {"SEPA": 0.0035, "PAYPAL": 0.0025, "CARD": 0.0055, "APPLE": 0.0030, "GOOGLE": 0.0040}
RECOVER = 0.55
ROUTE_MIX_WEB = {"SEPA": 0.58, "PAYPAL": 0.29, "CARD": 0.13}
ROUTE_MIX_APP = {"APPLE": 0.68, "GOOGLE": 0.32}
DIR_APP_SHARE = 0.14
STORE_FEE = {"APPLE": (0.30, 0.15), "GOOGLE": (0.15, 0.15)}   # first 12 paid months, after

# withdrawal within 14 days (refunded, not a start)
WITHDRAW = {"SOC": 0.012, "SEA": 0.010, "PART": 0.015, "TEL": 0.070, "APP": 0.008, "DIR": 0.008}

# a list-price rise: extra one-off leaving among subscribers on the full price, logit
RISE_X0 = -3.05
RISE_YOUNG = 0.95         # paid tenure under 12 months
RISE_MID = 0.42           # 12 to 35 months
RISE_P = 0.45
RISE_H = -0.20
RISE_TIMING = (0.45, 0.40, 0.15)   # before the new price, after its first month, after its second

# returns after leaving: monthly hazard r0 * exp(b * h) * exp(-s / tau), through the paywall
RET_R0 = 0.0200
RET_H = 0.60
RET_TAU = 14.0
RET_NEW_ACCOUNT = 0.55
RET_SAME_PAYMENT = 0.88
RET_SAME_ADDRESS = 0.95

# the subscriptions running in January 2023
BASE = {"BHR": 3500, "GAZ": 2250, "KBO": 1950, "ELN": 1100}
BASE_H, BASE_P = 0.65, -0.35

# reading: days a month ~ Binomial(days, p), logit p = R0 + R_H * h + novelty + season + news + noise
R0, R_H = -1.25, 1.00
R_NOVELTY = (0.30, 0.15)
R_SEASON = {7: -0.20, 8: -0.18, 12: -0.10}
R_NOISE = 0.35
SECOND_LOGIN = 0.12        # customers whose reading is split over a second login
ARTICLES_PER_DAY = 3.4

# texture
STAFF, TESTS, GROUPS = 160, 24, 38
GIFTS_A_MONTH = 21
DUP_SHARE = 0.014

# the 2027 plan
PLAN_GROWTH = {("SEA", "BHR"): 1.10, ("SOC", "BHR"): 1.05, ("PART", "GAZ"): 1.10, ("TEL", "KBO"): 1.05}
CPA_2027 = 1.04
CPA = {k: round(v / CPA_2027, 1) for k, v in PLAN_CPA.items()}

REPS = 60
BOOT_REPS = 40           # the start-month resamples behind the forcing check
