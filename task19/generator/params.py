"""task19 parameters: the island state of Kilvarra, its twelve districts and the processes that make its records.

Every number the simulation uses is here, so a rebuild is a function of this file and the seed alone."""
import datetime as _dt

SEED = 19_2026
SAMPLE_SEED = SEED + 1000 + int(__import__('os').environ.get('T19_SAMPLE', '40'))   # the coverage survey's draw of blocks and its fieldwork

EPOCH = _dt.date(1970, 1, 1)


def day(y, m, d):
    return (_dt.date(y, m, d) - EPOCH).days


def date_of(n):
    return EPOCH + _dt.timedelta(days=int(n))


CENSUS = day(2021, 3, 21)          # census day
T0 = day(2021, 6, 30)              # the base the official estimates roll forward from
REF = day(2026, 6, 30)             # the estimates' reference date
CLEAN = day(2024, 3, 31)           # the 2024 list validation ran to this date
SURVEY_START, SURVEY_END = day(2026, 6, 1), day(2026, 7, 17)
FOLLOW_START, FOLLOW_END = day(2026, 7, 27), day(2026, 9, 18)
EXTRACT = day(2026, 7, 3)          # the register extract was pulled for 30 June 2026 on this day
YEARS = [2022, 2023, 2024, 2025, 2026]   # each runs 1 July of the year before to 30 June

# The twelve districts: code, name, postcode area, type, mid-2021 population (persons), non-national share,
# age tilt (young adults, older people), pull for internal movers, share of dwellings that are shared or let rooms
DISTRICTS = [
    ("D01", "Port Ardain", "PA", "city", 57550, 0.19, 1.25, 0.85, 1.35, 0.17),
    ("D02", "Ballinrea", "BR", "city", 41120, 0.14, 1.15, 0.90, 1.10, 0.13),
    ("D03", "Drumcastle", "DC", "university", 30330, 0.11, 1.30, 0.85, 1.00, 0.16),
    ("D04", "Fort Larrick", "FL", "garrison", 22520, 0.06, 1.10, 0.90, 0.80, 0.08),
    ("D05", "Tullaghvane", "TV", "university", 23690, 0.09, 1.20, 0.95, 0.95, 0.14),
    ("D06", "Carnmoyle", "CM", "other", 24350, 0.13, 0.95, 1.10, 0.80, 0.09),
    ("D07", "Newbrook", "NB", "other", 21330, 0.11, 1.10, 0.85, 1.70, 0.08),
    ("D08", "Rossmullan", "RM", "other", 19130, 0.06, 0.80, 1.40, 0.75, 0.05),
    ("D09", "Glenarra", "GA", "other", 16640, 0.04, 0.80, 1.35, 0.65, 0.04),
    ("D10", "Loughmeen", "LM", "other", 21500, 0.07, 0.90, 1.20, 0.85, 0.06),
    ("D11", "Ardvale", "AV", "other", 14190, 0.05, 0.85, 1.30, 0.70, 0.04),
    ("D12", "Fennabeg", "FB", "other", 19920, 0.08, 0.95, 1.10, 0.90, 0.06),
]
UNIVERSITY = ("D03", "D05")
GARRISON = "D04"
LINE = 25000

# Non-national origin groups: label, share of the non-national population, transliterated names
ORIGINS = [("EE", 0.34, False), ("SA", 0.22, True), ("ME", 0.16, True), ("LA", 0.12, False), ("WE", 0.16, False)]

# Visibility: how readily a person shows up in any administrative or survey contact
VIS_SD = 0.55
VIS_YOUNG_MALE = (-0.30, 0.85)      # males 18 to 35: mean shift and spread
VIS_NONNAT = -0.45
OFFGRID = {"national": 0.23, "nonnational": 0.26}   # of males aged 18 to 44
OFFGRID_MULT = {"city": 1.15, "university": 1.15, "garrison": 1.0, "other": 0.90}
OFFGRID_SHIFT = -2.8

# Register coverage of residents: probit(a + b * visibility)
REG_A, REG_B = 2.15, 0.60
ARRIVAL_REG_A = 0.75                # newly arrived: probit(a + b * visibility) in the first year
LATE_REG = 0.35                     # of the unregistered arrivals, the share registering in each later year
# Survey response: probit(a + b * visibility)
SURV_A, SURV_B = 1.30, 0.55
# Census 2021 enumeration (for the census estimate and the 2021 link)
CENS_A, CENS_B = 1.95, 0.50

# Annual processes
FERTILITY = 0.0112                  # births per head per year
BIRTH_REG_2026 = 0.55               # of the year to June 2026's births, the share on the register by 30 June
EMIG_NN, EMIG_NN_RECENT = 0.045, 0.07
EMIG_NAT = {(0, 18): 0.003, (18, 25): 0.007, (25, 35): 0.009, (35, 50): 0.005, (50, 120): 0.002}
DEREG = {"national": 0.30, "nonnational": 0.20}
BORDER_DEPART_CAPTURE = 0.70        # non-national departures on the border system
OFFICIAL_EMIG_RECORDED = {"national": 0.35, "nonnational": 0.70}
OFFICIAL_IMM_RECORDED = 0.97
IMMIGRATION = {2022: 0.010, 2023: 0.022, 2024: 0.020, 2025: 0.012, 2026: 0.010}
RETURNING_NATIONALS = 0.12
MOVE_RATE = {(0, 18): 0.022, (18, 25): 0.075, (25, 35): 0.058, (35, 50): 0.028, (50, 120): 0.014}
LATE_REREG = 0.40                   # of movers still registered in their old district, the share re-registering each later year
REREG = {(0, 18): 0.85, (18, 25): 0.62, (25, 35): 0.74, (35, 50): 0.82, (50, 120): 0.86}
DUP_ON_REREG = 0.08
STUDENT_GO = 0.36                   # of 18-year-olds, the share leaving home for the two university districts
STUDENT_REREG = 0.45
STUDY_YEARS = (3, 4)
CLEAN_SHARE = 0.60                  # of records with five years or more since last contact, the share removed in 2024
FORCES_SHARE = 0.22                 # of Fort Larrick's residents aged 18 to 44, serving personnel
FORCES_CIVIL_RECORD = 0.12          # of serving personnel, a civilian register record kept at a former address
FORCES_TURNOVER = 0.11              # of serving personnel, the share leaving the service each year (and the recruits replacing them)
LEGACY_GHOSTS = 0.072               # of 2021 records, people who had already left
DUP_2021 = 0.025
STALE_2021 = 0.05                   # of 18 to 44s in 2021, a register address in an earlier district
DEATH_NOTIFY = 0.995

# Coverage survey and follow-up
CLUSTER_PERSONS = 40
SAMPLE_FRACTION = 0.07
FOLLOW_RESOLVE_BASE = 2.0           # probit intercept of resolving a listed record at an address
FOLLOW_NOT_KNOWN = 0.33             # of listed people no longer at the address, the share the household cannot place
GOLD = {"national": 600, "nonnational": 300}

# Data-entry differences between the systems
DOB_SWAP, DOB_TYPO = 0.012, 0.030
DOB_JAN1_NN = 0.20                  # non-nationals whose date of birth one system holds as 1 January
SURNAME_CHANGE_W = 0.04            # women 22 to 45 whose surname changed after their register record was made
MARRIED_MOVED = 0.55                # of them, the share whose register address is the one they left on marrying
SURVEY_DOB_TYPO = {"national": 0.050, "nonnational": 0.070}   # dates of birth given by another household member
NAME_ORDER_SWAP = 0.10              # survey records of residents from abroad with given and family names swapped
NICKNAME = 0.10
SURVEY_INITIAL = {"shared": 0.12, "other": 0.045}   # adults the household listed by initial and surname only
IRISH_FORM = 0.10                   # nationals whose survey record holds the other language's form of their forename
GAELIC_FORM = 0.10                  # nationals whose survey record holds the Irish form of their surname
PREFIX_DROP = 0.20                  # nationals whose survey record drops the O' or Mac of their surname
USED_NAME = 0.25                    # residents from abroad recorded in the survey under the name they go by
TRANSLIT = 0.55                     # of transliterated-origin people, the share whose two records romanise differently
TYPO = 0.03
