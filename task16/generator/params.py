"""The Quellstein world's constants: the calendar, the depots, the reason families and the process rates.

Every rate here is a property of the simulated process (how parcels run late, how often a recipient asks, where an
unhelped customer goes next, when the telephone line stops asking for the tracking number, how long a written case
stays open). Nothing is set per result.
"""
import datetime as dt

SEED = 16020
START = dt.date(2026, 8, 3)            # Monday, ISO week 32
DAYS = 98                              # to Sunday 8 November (ISO week 45)
V3_DAY = 56                            # Monday 28 September: version 3 live
ALERT_DAY = 70                         # Monday 12 October: delay alerts at the pilot depots
EXTRACT = dt.datetime(2026, 11, 9)     # Monday 00:00 local: every export is cut here
ACHIEVED_END = 91                      # conversations that ended before Monday 2 November are seven days old
ZONE = "Europe/Vienna"
DST_END = dt.datetime(2026, 10, 25, 3)  # local clocks go back: UTC+2 before, UTC+1 after
LINE = 75.0

DEPOTS = [("WIN", "Wien Nord", 62), ("WIS", "Wien Süd", 55), ("STP", "St. Pölten", 22), ("LNZ", "Linz", 38),
          ("WEL", "Wels", 20), ("SZG", "Salzburg", 30), ("GRZ", "Graz", 40), ("KLU", "Klagenfurt", 20),
          ("IBK", "Innsbruck", 28), ("BRE", "Bregenz", 15)]          # code, name, thousand parcels a week
PILOT = ("LNZ", "GRZ", "IBK")          # delay alerts from ALERT_DAY (the roll-out followed the depots' scanner upgrade)
HUB = ("WIN", "WIS", "STP", "WEL")     # depots moved onto Hub Traunfeld on Monday 5 October
STORM = ("SZG", "KLU", "IBK", "GRZ", "LNZ")   # storms and flooding, 17 to 24 August
DOW = [1.05, 1.15, 1.10, 1.05, 1.10, 0.55, 0.0]   # parcels due by weekday (Sunday none)

CLASSES = ["ON", "L1", "L2", "EX"]
CLASS_NAME = {"ON": "ON_TIME", "L1": "LATE_1", "L2": "LATE_2PLUS", "EX": "EXCEPTION"}
BASE_SHARE = {"L1": 0.040, "L2": 0.011, "EX": 0.010}
EX_TILT = {"WIN": 1.5, "WIS": 1.3, "BRE": 1.6}     # customs traffic
CONTACT = {"ON": 0.0225, "L1": 0.092, "L2": 0.300, "EX": 0.420}   # a recipient asks at all
ALERT_CUT = 0.42                        # a delay alert stops this share of late recipients from asking

FAMILIES = [("TRK", "Track and trace"), ("DLV", "Delivery day and time"), ("RDR", "Redirect and address"),
            ("RDL", "Missed delivery and redelivery"), ("PUP", "Pickup point and collection"),
            ("CUS", "Customs and import charges"), ("DMG", "Damaged parcel"), ("LST", "Missing parcel"),
            ("RET", "Returns and labels"), ("PAY", "Charges and refunds")]
FAM = [f for f, _ in FAMILIES]
FAM_GIVEN = {   # the reason a recipient first asks about, by how the parcel ran
    "ON": [.28, .20, .13, .06, .13, .01, .03, .00, .11, .05],
    "L1": [.40, .22, .10, .09, .08, .01, .01, .03, .01, .05],
    "L2": [.36, .14, .08, .09, .05, .02, .01, .17, .01, .07],
    "EX": [.10, .03, .10, .20, .04, .25, .18, .06, .01, .03]}
FIRST_CH = {"*": [.52, .28, .10, .10], "RDR": [.44, .38, .10, .08], "RDL": [.42, .40, .10, .08],
            "DMG": [.46, .18, .08, .28], "LST": [.48, .22, .08, .22], "CUS": [.48, .20, .08, .24],
            "PAY": [.48, .20, .08, .24]}        # assistant, phone, chat, written
CH = ["A", "P", "C", "W"]

# the assistant's chance of ending the matter (logit), version 3, parcel on time; class and version shifts
A_ON = {"TRK": 1.85, "DLV": 2.17, "RDR": 2.20, "RDL": 1.70, "PUP": 2.40, "CUS": 1.36, "DMG": 1.53, "LST": 1.00,
        "RET": 2.65, "PAY": 2.20}
CLASS_SHIFT = {"L1": {"*": -0.75, "TRK": -1.05, "DLV": -1.10, "RET": -0.40},
               "L2": {"*": -1.45, "TRK": -1.95, "DLV": -2.30, "LST": -0.85, "RET": -0.80},
               "EX": {"*": -0.80, "CUS": -0.45, "RDL": -0.95}}
V2_SHIFT = {"TRK": -0.30, "DLV": -0.30, "RDR": -0.20, "RDL": -0.35, "PUP": -0.15, "CUS": -0.25, "DMG": -0.10,
            "LST": -0.15, "RET": -0.10, "PAY": -0.20}
DAY_SD, FAMDAY_SD = 0.21, 0.10
HUMAN_MORE = {"P": 0.10, "C": 0.12, "W": 0.16}  # a further contact after an adviser handled it
NEXT_AFTER_A = {"*": [.20, .44, .20, .16], "TRK": [.26, .42, .22, .10], "DLV": [.26, .42, .22, .10],
                "RDR": [.14, .58, .18, .10], "RDL": [.13, .60, .17, .10], "PUP": [.20, .46, .22, .12],
                "CUS": [.12, .26, .12, .50], "DMG": [.10, .24, .12, .54], "LST": [.12, .28, .12, .48],
                "PAY": [.12, .26, .12, .50], "RET": [.24, .34, .22, .20]}
NEXT_AFTER_H = {"P": [.10, .40, .14, .36], "C": [.12, .40, .28, .20], "W": [.08, .50, .12, .30]}
HANDOVER = 0.55                         # of chats that follow the assistant, handed over inside the session

QUEUES = ["TRACKING", "CLAIMS", "CUSTOMS", "GENERAL"]            # the IVR's menu
QUEUE_OF = {"TRK": "TRACKING", "DLV": "TRACKING", "RDR": "TRACKING", "RDL": "TRACKING", "PUP": "TRACKING",
            "DMG": "CLAIMS", "LST": "CLAIMS", "CUS": "CUSTOMS", "PAY": "CUSTOMS", "RET": "GENERAL"}
KEY_RATE = 0.80                         # callers who key a valid tracking number when the IVR asks
BYPASS_TAKE = 0.62                      # callers who take the offered bypass
BYPASS_AT = 1.00                        # offered when the queue's load passes about this multiple of its staffing
TAG_HIT, TAG_FALSE = 0.58, 0.012        # advisers' previous-contact tick

CASE_QUEUES = {"ADDRESS": ("RDR", "RDL", "PUP"), "TRACE": ("TRK", "DLV", "LST"), "CLAIMS": ("DMG",),
               "CUSTOMS": ("CUS",), "BILLING": ("PAY", "RET")}
CASE_QUEUE_OF = {f: q for q, fs in CASE_QUEUES.items() for f in fs}
CASE_LAG = {"ADDRESS": 0.7, "TRACE": 3.2, "CLAIMS": 11.0, "CUSTOMS": 4.2, "BILLING": 6.0}   # median days to close
CASE_SIGMA = 0.85
AGE_BANDS = [(0, 6), (7, 13), (14, 20), (21, 27), (28, 9999)]

PEAK_WEEKS = [dt.date(2026, 11, 16) + dt.timedelta(days=7 * i) for i in range(7)]
PEAK_PARCELS = [410, 470, 560, 540, 560, 520, 330]               # thousand a week, all depots
PEAK_SERVICE = [(86.0, 8.5, 3.5, 2.0), (84.0, 9.5, 4.5, 2.0), (80.0, 11.5, 6.5, 2.0), (82.0, 10.5, 5.5, 2.0),
                (81.0, 11.0, 6.0, 2.0), (79.0, 12.0, 7.0, 2.0), (88.0, 7.5, 2.8, 1.7)]   # ON, +1, +2 or more, exception
