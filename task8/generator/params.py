"""task8 architecture 19: Hollinbrook Academies Trust, Year 7 entry reading on one Lexis basis.

Every constant of the simulated world. Reading is on the Lexis 2019 standardisation's z basis at the start of Year 7
(Lexis standardised score = 100 + 15 z); every other measure is generated from it by its own process."""
import datetime as dt

SEED = 8342

TRUST = "Hollinbrook Academies Trust"
# academy, local authority, entry test, cohort, school mean reading (z on the Lexis basis), test timing
ACADEMIES = [
    # Lexis academies testing in September
    ("Ashdene Academy", "Sheffield", "LEXIS", 238, 0.12, "SEPT"),
    ("Carrbrook School", "Rotherham", "LEXIS", 196, 0.02, "SEPT"),
    ("Hollinbrook Park Academy", "Sheffield", "LEXIS", 262, 0.27, "SEPT"),
    ("Kelham Bridge Academy", "Sheffield", "LEXIS", 214, 0.06, "SEPT"),
    ("Mortlake Lane School", "Derbyshire", "LEXIS", 181, 0.18, "JULY"),
    ("Thurnscoe Vale Academy", "Barnsley", "LEXIS", 169, -0.05, "SEPT"),
    # Lexis academies testing at the July transition day
    ("Crookes Academy", "Sheffield", "LEXIS", 227, 0.15, "JULY"),
    ("Dore Moor School", "Sheffield", "LEXIS", 201, 0.22, "JULY"),
    ("Wingerworth Academy", "Derbyshire", "LEXIS", 188, 0.04, "JULY"),
    # Quill academies
    ("Eastwood Hall Academy", "Nottinghamshire", "QUILL", 243, 0.02, "SEPT"),
    ("Bestwood Academy", "Nottingham", "QUILL", 219, -0.10, "SEPT"),
    ("Clifton Grange School", "Nottingham", "QUILL", 176, 0.14, "SEPT"),
    ("Kirkby Fields Academy", "Nottinghamshire", "QUILL", 205, -0.04, "SEPT"),
    ("Long Eaton Academy", "Derbyshire", "QUILL", 231, 0.19, "SEPT"),
    ("Mansfield Woodhouse Academy", "Nottinghamshire", "QUILL", 194, -0.14, "SEPT"),
    ("Ruddington Academy", "Nottinghamshire", "QUILL", 172, 0.24, "SEPT"),
    # Brightway academies (the Lexis trial this autumn)
    ("Goldthorpe Academy", "Barnsley", "BRIGHTWAY", 214, -0.55, "SEPT"),
    ("Maltby Academy", "Rotherham", "BRIGHTWAY", 228, -0.44, "SEPT"),
    ("Parkgate Academy", "Rotherham", "BRIGHTWAY", 187, -0.62, "SEPT"),
    ("Swinton Moor Academy", "Rotherham", "BRIGHTWAY", 203, -0.38, "SEPT"),
    ("Wombwell Academy", "Barnsley", "BRIGHTWAY", 196, -0.50, "SEPT"),
]
SWITCH_ACADEMIES = ("Maltby Academy", "Swinton Moor Academy", "Wombwell Academy")   # booklets late: half their tutor groups sat Lexis first
TUTOR_GROUPS = 8

WITHIN_SD = 0.92            # within-academy spread of reading
TEST_SD = {"LEXIS": 0.28, "QUILL": 0.31, "BRIGHTWAY": 0.37}   # measurement error, z units (reliabilities .92 .91 .87)

# each test's standardisation sample, against the Lexis 2019 sample (mean and spread of reading in z units)
NORM = {"LEXIS": (0.0, 1.0), "QUILL": (-0.22, 1.04), "BRIGHTWAY": (0.05, 0.90)}
SAS_RANGE = {"LEXIS": (69, 141), "QUILL": (69, 141), "BRIGHTWAY": (70, 130)}
BRIGHTWAY_KNEE = 116.0      # the paper test's top end tops out (an easier paper)

SECOND_SITTING_GAIN = 0.24  # z units: a second sitting of a reading test within three weeks (familiarity, teaching)
GAIN_SD = 0.10
JULY_LEVEL = 0.26           # z units: reading at the July transition day stands above the start of Year 7
JULY_SD = 0.12

# KS2 reading (May 2026)
KS2_MEAN, KS2_SD = 105.0, 7.3
KS2_CHANGE_SD = 0.30        # individual change between May and the start of Year 7, z units
KS2_ERR_SD = 0.43           # the KS2 paper's own error and its different reading demands
KS2_AGE = 0.75              # KS2 is not age-standardised: points by which the oldest outscore the average
KS2_ABSENT = 0.014
KS2_MISSING_ARRIVED = 0.032 # no KS2: arrived from abroad, an independent or a Welsh school
KS2_TOP = 120
KS2_B_CUT = 79              # working below the test

# sittings
LEXIS_SEPT = (dt.date(2026, 9, 7), dt.date(2026, 9, 25))
LEXIS_JULY = (dt.date(2026, 7, 1), dt.date(2026, 7, 3))
QUILL_SEPT = (dt.date(2026, 9, 14), dt.date(2026, 9, 25))
BRIGHTWAY_FIRST = (dt.date(2026, 9, 3), dt.date(2026, 9, 9))
TRIAL_GAP = (9, 16)         # days from the Brightway sitting to the Lexis trial sitting
JULY_ABSENT = 0.11          # at the July academies: absent at transition day or placed over the summer, sat in September
MISS_TRIAL = 0.045
MISS_BRIGHTWAY = 0.03
MISS_FIRST = 0.018          # no entry sitting at all by the census
ARRIVE_LATE = 0.015         # joined after the academy's sitting
LEFT_BEFORE_CENSUS = 0.012  # tested, then left before the census
MOVED_WITHIN = 0.006        # moved between trust academies after their first sitting
FAILED_ONLINE = 0.02        # an online session that failed and was re-sat
QUILL_SHORT = 0.035         # adaptive sessions ended under 24 questions
QUILL_MIN_ITEMS = 24
QUILL_UNMAPPED = 0.06       # Quill rostering sync gaps

CENSUS = dt.date(2026, 10, 1)
EXPORTED = dt.date(2026, 10, 6)

# the trust's programme
THRESHOLD = 85.0
HOURS_PER_STUDENT = 0.4     # tutor hours a week per programme student
WEEKS = 36
RATE = 27.80                # pounds an hour, 2026-27 with on-costs

BOOT_REPS = 200
PROVISIONAL_BUDGET = 339500.0   # approved in July on last October's 848 students
LAST_OCTOBER = 848
