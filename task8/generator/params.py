"""task8 architecture 18: the world's constants. The Prairie Adult Credentials Board certifies adult numeracy at
Level 1 and Level 2; one Rasch bank holds both levels' items; the 2027 Level 1 paper borrows twelve long
patterns and relationships items from the Level 2 pool."""
import datetime as dt

SEED = 818025
ORG = "Prairie Adult Credentials Board"
ORG_SHORT = "PACB"

YEARS = (2022, 2023, 2024, 2025, 2026)
ITEMS_PER_PAPER = 40
STANDARD_RAW = 26                 # the 2022 panel's standard: 26 of the 40 marks on the 2022 Level 1 paper
BAND = (0.20, 0.90)               # the specification's targeting band for a candidate who just meets the standard

# Level 1 candidates (adults in community learning centres) against the Level 2 reference
LAMBDA = 0.80                     # reading cost, logits per 100 words of stem
BETA = 0.90                       # everyday-context advantage, logits (population mean over regions)
RESID_DIF = 0.07                  # item-specific residual of the Level 1 shift, logits (sd)

# regions: code, name, province, share of Level 1 sittings, ability offset, everyday-advantage deviation
REGIONS = [
    ("WPG", "Winnipeg", "MB", 0.29, -0.06, -0.36),
    ("WST", "Westman", "MB", 0.12, 0.05, 0.07),
    ("INT", "Interlake-Eastman", "MB", 0.13, 0.03, 0.29),
    ("PKN", "Parkland and North", "MB", 0.10, -0.08, 0.40),
    ("SKC", "Saskatoon and Central", "SK", 0.19, 0.04, -0.14),
    ("RGS", "Regina and South", "SK", 0.17, 0.03, 0.08),
]

L1_SITTINGS = {2022: 792, 2023: 823, 2024: 861, 2025: 897, 2026: 934}
L2_SITTINGS = {2022: 1043, 2023: 1088, 2024: 1131, 2025: 1187, 2026: 1236}
L1_MU, L1_SD = -0.62, 0.74
L2_MU, L2_SD = 0.78, 0.80

# sittings run on demand at the centres from February to October; papers close on 30 October
SITTING_START = (2, 3)
SITTING_END = (10, 30)
ASOF = dt.date(2026, 11, 9)        # the request
MEETING = dt.date(2026, 12, 3)     # the Awards Committee sets the pass mark
OPENS_2027 = dt.date(2027, 2, 1)   # the 2027 paper opens
PRELIM_CUTOFF = dt.date(2026, 6, 30)

RECONNECT_RATE = 0.012            # share of online sittings with a reconnect (re-answered items)
DUP_REGISTRATION = 0.021          # candidates registered twice (centre and regional office)
WITHDRAWN = 0.034                 # registrations withdrawn or absent (no sitting)
