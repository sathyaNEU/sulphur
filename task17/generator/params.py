"""The world's constants: the Landesrechenzentrum Ravensfeld's gpu partition, its scheduler, its projects and its
operators. Every number here is a parameter of the process the generator simulates; none is a result."""
import datetime as dt
from zoneinfo import ZoneInfo

SEED = 1610
ORG = "Landesrechenzentrum Ravensfeld"
ORG_SHORT = "LRZ Ravensfeld"
CLUSTER = "sturmvogel"
PARTITION = "gpu"
TZ = ZoneInfo("Europe/Berlin")
UTC = dt.timezone.utc

# the clock: hours since T0 (UTC)
T0 = dt.datetime(2023, 9, 1, 0, 0, tzinfo=UTC)
LOG_FROM = dt.datetime(2024, 1, 1, 0, 0, tzinfo=TZ)          # the accounting export's window opens
CUT = dt.datetime(2026, 11, 16, 6, 10, 0, tzinfo=TZ)           # the exports were run on this morning
CUT_DATE = dt.date(2026, 11, 15)                                # the records are complete to this day
SIM_END = dt.datetime(2026, 11, 17, 0, 0, tzinfo=UTC)

# the partition
N_NODES = 64
RACKS = 8
NODES_PER_RACK = 8
RACK_IN_SERVICE = {1: T0, 2: T0, 3: T0, 4: T0, 5: T0, 6: T0,
                   7: dt.datetime(2025, 3, 17, 9, 40, tzinfo=TZ), 8: dt.datetime(2025, 4, 7, 11, 15, tzinfo=TZ)}

# quality of service limits (hours) and the dates they changed
QOS_NORMAL_24_UNTIL = dt.datetime(2026, 5, 3, 9, 0, tzinfo=TZ)
QOS_NORMAL_LIMITS = [(T0, 24.0), (QOS_NORMAL_24_UNTIL, 48.0)]
QOS_NORMAL_2027 = (dt.datetime(2027, 4, 1, 0, 0, tzinfo=TZ), 96.0)
QOS_SHORT = 4.0

# scheduler
BF_MODE = 1            # conservative backfill (every queued job tested gets a reservation)
BF_MAX = 100
REQUEUE_HOLD = 0.05    # hours a killed job is held before it is back in the queue
FIRST_JOB_ID = 100000
MAX_JOB_ID = 259999

# projects: categories, their realised use of a grant (mean of the project's target ratio) by funding year
CATEGORIES = ["FOR", "NWG", "LEH", "KOP"]
CAT_SHARE = {"FOR": 0.52, "NWG": 0.21, "LEH": 0.16, "KOP": 0.11}
USE_TARGET = {"FOR": (0.585, 0.81), "NWG": (0.535, 0.75), "LEH": (0.38, 0.527), "KOP": (0.635, 0.85)}  # first year, later
USE_SD = 0.11
CONTINUE_P = {"FOR": 0.76, "NWG": 0.70, "LEH": 0.80, "KOP": 0.65}
NEW_PROJECTS = {2023: 140, 2024: 72, 2025: 84, 2026: 90, 2027: 98}
GRANT_MEDIAN = {"FOR": 1750.0, "NWG": 1300.0, "LEH": 850.0, "KOP": 2400.0}
GRANT_SIGMA = 0.70
GRANT_GROWTH = {2023: 0.78, 2024: 0.92, 2025: 0.96, 2026: 0.82, 2027: 1.15}   # the rounds' growth in grant size
REQUEST_SCALE_2027 = 0.76        # the 2027 requests against the 2026 grants, before the per-project spread
CKPT_SHARE = {"FOR": (0.54, 0.27, 0.19), "NWG": (0.56, 0.27, 0.17), "LEH": (0.74, 0.19, 0.07), "KOP": (0.44, 0.35, 0.21)}
CKPT_HOURS = (0.0, 1.0, 6.0)

# outages
SW_H0 = 1.0 / 620.0             # software failure hazard at zero uptime, per node-hour
SW_U0 = 300.0                    # uptime scale of the rising hazard (hours)
SW_K = 1.6
HW_RATE = 1.0 / 15500.0          # hardware failure rate per node-hour
RACK_SWITCH_RATE = 1.3 / 8760.0 # per rack-hour
RACK_PDU_RATE = 1.0 / 8760.0
RESTARTS_ADHOC = 9
MAINT_LONG_MONTHS = {2024: 6, 2025: 9, 2026: 3, 2027: 6}

# the 2027 round
BOARD_DATE = dt.date(2026, 12, 14)
REQUEST_DEADLINE = dt.date(2026, 10, 31)
