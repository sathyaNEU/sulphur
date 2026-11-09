"""Constants for task6: Rotalinha, its internal services, the SLO standard's thresholds and budgets, the load
balancer's target groups, the tracing store's sampler, the people, the dates and the pack's file names."""
import datetime as dt
import os

SEED = 2711
ORG = "Rotalinha"
ORG_LTD = "Rotalinha Viagens, S.A."
YEAR = 2026
TZ_NOTE = "Lisbon"                  # December is WET, UTC+0; summer is WEST, UTC+1

# the review period: December 2026 in Lisbon time (UTC+0 all month)
REVIEW_START = dt.datetime(2026, 12, 1, 0, 0)
REVIEW_HOURS = 31 * 24
ASSEMBLED = dt.datetime(2027, 1, 6, 9, 30)          # the pack's file times
TARGET_PER_HOUR = 24                                # the sampler's server spans per service per hour

# service, team, tier, tracing name, LB target group (Jul-Dec), LB target group (Jan-Jun), status page component,
# cost tag (current), cost tag (before 1 April), threshold ms, budget %
SERVICES = [
    ("journey-search", "Search & Discovery", 1, "journey-search", "tg-jsearch-prd", "tg-search-prd", "Search",
     "svc-journey-search", "team-search", 1500, 1.0),
    ("fares", "Marketplace", 1, "fares-api", "tg-fares-prd", "tg-fares-prd", "Search",
     "svc-fares", "team-marketplace", 300, 1.0),
    ("places", "Search & Discovery", 2, "places", "tg-places-prd", "tg-autocomplete-prd", "Search",
     "svc-places", "team-search", 150, 1.0),
    ("seat-map", "Checkout", 1, "seat-map", "tg-seatmap-prd", "tg-seatmap-prd", "Booking and payments",
     "svc-seat-map", "team-checkout", 500, 1.0),
    ("booking", "Checkout", 1, "booking-core", "tg-booking-prd", "tg-booking-prd", "Booking and payments",
     "svc-booking", "team-checkout", 3000, 0.5),
    ("payments", "Checkout", 1, "payments", "tg-payments-prd", "tg-payments-prd", "Booking and payments",
     "svc-payments", "team-checkout", 2000, 0.5),
    ("tickets", "Customer", 2, "ticketing", "tg-tickets-prd", "tg-tickets-prd", "Tickets and boarding passes",
     "svc-tickets", "team-customer", 1500, 1.0),
    ("accounts", "Customer", 1, "accounts", "tg-accounts-prd", "tg-accounts-prd", "Sign-in and accounts",
     "svc-accounts", "team-customer", 600, 2.0),
    ("partner-gateway", "Marketplace", 2, "partner-gw", "tg-partners-prd", "tg-partners-prd", "Search",
     "svc-partner-gateway", "team-marketplace", 1000, 2.0),
    ("notifications", "Customer", 2, "notify", "tg-notify-prd", "tg-notify-prd", "Tickets and boarding passes",
     "svc-notifications", "team-customer", 600, 1.0),
]
SVC = [s[0] for s in SERVICES]
TEAM = {s[0]: s[1] for s in SERVICES}
TIER = {s[0]: s[2] for s in SERVICES}
TRACE_NAME = {s[0]: s[3] for s in SERVICES}
TG_H2 = {s[0]: s[4] for s in SERVICES}
TG_H1 = {s[0]: s[5] for s in SERVICES}
COMPONENT = {s[0]: s[6] for s in SERVICES}
COST_TAG = {s[0]: s[7] for s in SERVICES}
OLD_TAG = {s[0]: s[8] for s in SERVICES}
THRESHOLD = {s[0]: s[9] for s in SERVICES}
BUDGET = {s[0]: s[10] for s in SERVICES}
COMPONENTS = ["Search", "Booking and payments", "Tickets and boarding passes", "Sign-in and accounts"]

# The edge services take the app's and the website's requests and start every trace; the store keeps or drops a
# trace whole, at the edge service's keep rate for the hour the trace started. The internal services are called only
# from inside those traces.
EDGE = ["journey-search", "places", "seat-map", "booking", "accounts", "tickets"]
INTERNAL = ["fares", "partner-gateway", "payments", "notifications"]

# edge traffic: peak requests an hour, diurnal peaks (hour, width, height), whether the December campaigns reach it,
# and the service's own busy stretches (day index from 1 December, from hour, to hour, factor)
TRAFFIC = {
    "journey-search": (30000, [(12.5, 2, 1.0), (20.5, 2, 1.0)], 1, []),
    "places": (60000, [(9, 1.5, 0.9), (19, 2, 1.0)], 1, []),
    "seat-map": (5000, [(13, 3, 1.0)], 1, []),
    "booking": (1200, [(13, 3, 1.0), (21, 2, 0.8)], 1, []),
    "accounts": (7000, [(9, 3, 0.8), (20, 3, 1.0)], 0, []),
    "tickets": (1300, [(8, 2, 1.0), (17, 3, 0.7)], 0, [(20, 6, 11, 1.7), (21, 6, 11, 1.8), (22, 6, 11, 1.6)]),
}
# the December campaigns (day index from 1 December, from hour, to hour, factor): the Cyber Week email on 3 December,
# the ferry sale on 10 December, the Christmas getaway push on 17 December
CAMPAIGNS = [(2, 19, 23, 1.9), (9, 12, 15, 1.7), (16, 20, 23, 1.8)]
SEASON = {d: 1.35 for d in range(17, 23)}            # 18 to 23 December
SEASON.update({d: 1.25 for d in range(25, 30)})      # 26 to 30 December

# the calls an edge request makes (internal service, operation, share of requests that make it), and how the edge
# service makes them: "par" waits for all of them at once, "seq" makes them one after another
GRAPH = {
    "journey-search": ("par", [("fares", "batch", 0.97), ("partner-gateway", "availability", 0.985)]),
    "seat-map": ("seq", [("partner-gateway", "seats", 1.0), ("fares", "quote", 0.6)]),
    "booking": ("seq", [("fares", "quote", 0.995), ("partner-gateway", "reserve", 1.0),
                        ("payments", "authorise", 0.97), ("notifications", "email", 0.95)]),
    "accounts": ("seq", [("payments", "wallet", 0.25), ("notifications", "verify", 0.45)]),
    "tickets": ("seq", [("partner-gateway", "ticket", 0.8), ("notifications", "resend", 0.5)]),
}
RETRY = {"partner-gateway"}         # a 5xx from the partner gateway is retried once by its caller

# capacity an hour; latency at zero load as (log-normal median ms, load sensitivity, spread) and the target December
# slow share the median is set to (None: the operation's own work at a fixed median); 5xx rate
CAP = {"journey-search": 40000, "places": 88000, "seat-map": 9800, "booking": 6000, "accounts": 26000,
       "tickets": 7000, "fares": 90000, "partner-gateway": 70000, "payments": 5000, "notifications": 9000}
LAT = {
    ("journey-search", "own"): (110.0, 0.20, 0.45, None),
    ("places", "own"): (None, 0.24, 0.56, 1.52),
    ("seat-map", "own"): (None, 0.32, 0.44, 1.86),
    ("booking", "own"): (None, 0.10, 0.40, 0.28),
    ("accounts", "own"): (None, 0.08, 0.50, 1.30),
    ("tickets", "own"): (None, 0.04, 0.45, 0.68),
    ("fares", "batch"): (None, 0.05, 0.45, 0.85),
    ("fares", "quote"): (None, 0.05, 0.40, 0.10),
    ("partner-gateway", "availability"): (None, 0.45, 0.40, 2.05),
    ("partner-gateway", "seats"): (85.0, 0.10, 0.35, None),
    ("partner-gateway", "reserve"): (None, 0.20, 0.45, 0.60),
    ("partner-gateway", "ticket"): (None, 0.12, 0.42, 0.50),
    ("payments", "authorise"): (None, 0.06, 0.38, 0.45),
    ("payments", "wallet"): (45.0, 0.04, 0.35, None),
    ("notifications", "email"): (None, 0.02, 0.55, 0.30),
    ("notifications", "verify"): (None, 0.03, 0.45, 0.90),
    ("notifications", "resend"): (None, 0.02, 0.50, 0.50),
}
ERR = {"journey-search": 0.002, "places": 0.001, "seat-map": 0.002, "booking": 0.003, "accounts": 0.002,
       "tickets": 0.002, "fares": 0.002, "partner-gateway": 0.008, "payments": 0.004, "notifications": 0.003}
RHO_MAX = 0.93

# December's customer-facing incidents, as the world and the responders produced them. Each began in one service's
# own handling (`fault`, the operations it slowed by `mult` from `onset` to `end`); the services calling it slowed
# with it, and some callers' own handling slowed later as their workers waited for connections (`block`: service,
# factor, from, minutes to build up), in three incidents further than the fault's own slowdown. Each slowdown climbs
# in over `ramp` minutes and falls away after `end` (world._ramped). The
# responders declared on the first alert and named services as they suspected them (`named`); the status page posted
# its components from `posted` to `operational`. Times are December day, hour, minute (UTC, which is Lisbon time in
# December); `named` and `declared` carry seconds. Post-incident reviews for December were still open at the review.
DEC_INCIDENTS = [
    {"id": "I2", "fault": "seat-map", "ops": [("seat-map", "own")], "mult": 1.6, "ramp": (6, 3),
     "onset": (8, 12, 8), "end": (8, 13, 41), "block": [],
     "declared": (8, 12, 24, 5), "named": [("partner-gateway", (8, 12, 24, 5)), ("seat-map", (8, 12, 47, 31))],
     "posts": [("Booking and payments", (8, 12, 29), (8, 13, 49))], "sev": "SEV3"},
    {"id": "I6", "fault": "partner-gateway", "ops": [("partner-gateway", "seats")], "mult": 1.8, "ramp": (5, 2),
     "onset": (14, 12, 13), "end": (14, 13, 32), "block": [("seat-map", 3.9, (14, 12, 44), 7)],
     "declared": (14, 12, 31, 48), "named": [("seat-map", (14, 12, 31, 48)), ("partner-gateway", (14, 12, 58, 2))],
     "posts": [("Booking and payments", (14, 12, 35), (14, 13, 40))], "sev": "SEV3"},
    {"id": "I1", "fault": "partner-gateway", "ops": [("partner-gateway", "availability")], "mult": 3.7, "ramp": (9, 3),
     "onset": (15, 18, 56), "end": (15, 23, 53), "block": [("journey-search", 1.25, (15, 20, 7), 12)],
     "declared": (15, 19, 41, 14), "named": [("journey-search", (15, 19, 41, 14)), ("partner-gateway", (15, 20, 6, 40)),
                                            ("fares", (15, 20, 21, 9))],
     "posts": [("Search", (15, 19, 45), (16, 0, 3))], "sev": "SEV2"},
    {"id": "I3", "fault": "payments", "ops": [("payments", "authorise")], "mult": 1.8, "ramp": (7, 2),
     "onset": (17, 20, 33), "end": (17, 22, 6), "block": [("booking", 1.2, (17, 21, 13), 9)],
     "declared": (17, 20, 49, 22), "named": [("booking", (17, 20, 49, 22)), ("payments", (17, 21, 8, 9)),
                                            ("notifications", (17, 21, 20, 44))],
     "posts": [("Booking and payments", (17, 20, 53), (17, 22, 12))], "sev": "SEV2"},
    {"id": "I4", "fault": "fares", "ops": [("fares", "batch"), ("fares", "quote")], "mult": 3.3, "ramp": (8, 3),
     "onset": (21, 19, 37), "end": (21, 23, 12), "block": [("journey-search", 4.4, (21, 20, 22), 11),
                                                          ("booking", 1.15, (21, 20, 41), 8)],
     "declared": (21, 19, 46, 3), "named": [("journey-search", (21, 19, 46, 3)), ("fares", (21, 20, 4, 37)),
                                           ("booking", (21, 20, 15, 12))],
     "posts": [("Search", (21, 19, 50), (21, 23, 18))], "sev": "SEV2"},
    {"id": "I5", "fault": "notifications", "ops": [("notifications", "verify")], "mult": 3.9, "ramp": (10, 3),
     "onset": (26, 16, 53), "end": (26, 22, 28), "block": [("accounts", 5.0, (26, 18, 22), 13)],
     "declared": (26, 18, 1, 51), "named": [("accounts", (26, 18, 1, 51)), ("notifications", (26, 18, 29, 26)),
                                           ("payments", (26, 18, 42, 10))],
     "posts": [("Sign-in and accounts", (26, 18, 5), (26, 22, 39))], "sev": "SEV2"},
    {"id": "I7", "fault": "places", "ops": [("places", "own")], "mult": 1.8, "ramp": (4, 2),
     "onset": (29, 10, 4), "end": (29, 11, 21), "block": [],
     "declared": (29, 10, 12, 40), "named": [("places", (29, 10, 12, 40))],
     "posts": [("Search", (29, 10, 16), (29, 11, 27))], "sev": "SEV3"},
]
# autoscaling: (fewest pods, most pods, requests an hour one pod carries before another is added)
AUTOSCALE = {"journey-search": (4, 12, 5000), "fares": (4, 10, 7000), "places": (4, 14, 10000),
             "seat-map": (3, 8, 1500), "booking": (3, 6, 500), "payments": (3, 6, 600), "tickets": (3, 6, 800),
             "accounts": (3, 8, 1800), "partner-gateway": (4, 12, 6000), "notifications": (2, 6, 700)}

PEOPLE = {"head": "Teresa Nogueira", "finops": "Bruno Marques", "sre": "Ivo Pereira"}

FILES = {
    "spans": "trace_spans_2026-12.parquet",
    "lb_h1": "lb_target_group_requests_2026-H1.csv",
    "lb_h2": "lb_target_group_requests_2026-H2.csv",
    "slo": "PR-SLO-3_service_level_objectives_2026.docx",
    "catalogue": "service_catalogue_2026.xlsx",
    "incidents": "incidents_2026.csv",
    "status": "status_page_history_2026.json",
    "billing": "cloud_billing_2026.csv",
    "invoices": "cloud_invoices_2026.csv",
    "resources": "cloud_resources_2026.csv",
    "deploys": "production_deployments_2026.json",
    "rollouts": "cluster_rollout_history_2026.csv",
    "timeline": "incident_timeline_2026.csv",
    "capacity": "capacity_review_2026-Q4.md",
    "feedback": "app_store_reviews_2026-H2.xlsx",
}
# files the call and every ask leave unread: context, the balancer's January to June counts, and the review folder's
# change and cost records (PR-SLO-3 sections 5.1 and 5.3), which the review reports but the asks do not use
FILES_KEY_OF = {v: k for k, v in FILES.items()}
DISTRACTORS = ["capacity", "feedback", "lb_h1", "deploys", "rollouts", "billing", "invoices", "resources"]
DOCX_OUT = "reliability_review_2026.docx"
CSV_OUT = "service_sli_2026.csv"


def r1(x):
    """Round half away from zero to one decimal (SLIs in per cent)."""
    from decimal import Decimal, ROUND_HALF_UP
    return float(Decimal(repr(float(x))).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))


def r2(x):
    """Round half away from zero to two decimals (the standard's per cents)."""
    from decimal import Decimal, ROUND_HALF_UP
    return float(Decimal(repr(float(x))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def _font_dir():
    for d in ("/usr/share/fonts/truetype/liberation", os.path.expanduser("~/Library/Fonts"), "/Library/Fonts"):
        if os.path.exists(os.path.join(d, "LiberationSans-Regular.ttf")):
            return d
    raise FileNotFoundError("LiberationSans-Regular.ttf")


FONT_DIR = _font_dir()
