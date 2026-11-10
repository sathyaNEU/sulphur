"""World parameters for Tekenbord B.V. (task1 architecture 2). Every constant the generator, the documents and the
write-up use is read from here."""

SEED = 1107

# calendar: month index 0 = January 2022; the cut is the end of October 2026; the forecast runs to December 2027
M0_YEAR, M0_MONTH = 2022, 1
CUT = 57            # October 2026
HORIZON = 71        # December 2027
PRICE_RISE = 50     # March 2026: the Business list price rises at each contract's next renewal from 1 March 2026
TEAM_MIN = 51       # April 2026: the Team plan bills at least three seats from the first invoice dated in April

# prices (per seat per month)
BUS_LIST_OLD = {"EUR": 15.00, "GBP": 13.00}
BUS_LIST_NEW = {"EUR": 19.00, "GBP": 16.50}
TEAM_PRICE = {"EUR": 12.00, "GBP": 10.40}
TEAM_MIN_SEATS = 3
PLAN_RATE_GBP = 1.16           # EUR per GBP, the 2026 plan rate, used for every 2026 and 2027 ARR figure
ONBOARDING_FEE = {"EUR": 1500.0, "GBP": 1300.0}

# Business book
BUS_INITIAL = 230
SEAT_MEDIAN, SEAT_SIGMA = 34.0, 0.85
UTIL_MEAN, UTIL_SD = 0.84, 0.13
NEED_GROWTH_MEAN, NEED_GROWTH_SD = 0.01, 0.08    # yearly drift in the users an account needs
RAMP_DEPTH, RAMP_TAU = 0.42, 2.6                 # a new account starts about 58 per cent rolled out
CHURN_BASE = 0.045
CHURN_FIRST = 0.075            # added at a contract's first renewal
CHURN_UTIL = 0.55              # added per point of utilisation below 0.70
RIGHTSIZE_BELOW = 0.88
RIGHTSIZE_P_FIRST, RIGHTSIZE_P_LATER = 0.78, 0.40
RIGHTSIZE_HEADROOM = 0.93
CONSOLIDATION_HAZARD = 0.0065  # a month, per parent group holding two or more Business accounts
CONSOLIDATION_CHURN = 0.82     # a consolidating group's account leaves at its next renewal

# realised uplift at the first renewal on or after 1 March 2026, by seats (log-linear, capped at the list rise)
UPLIFT_FULL = 0.2667
UPLIFT_SLOPE = 0.055           # per unit of log(seats / 20)
UPLIFT_SD = 0.022
UPLIFT_FLOOR = 0.08

# Team book
TEAM_INITIAL = 1450
TEAM_SIGNUPS = (88, 142)       # a month, January 2022 and October 2026 trend ends
TEAM_HAZARD = 0.021
TEAM_HAZARD_1, TEAM_HAZARD_2 = 0.019, 0.009    # added for one- and two-member teams
TEAM_YOUNG_MULT = 1.45         # first three months
PAD_SHOCK, PAD_DECAY, PAD_PERSIST = 0.14, 1.5, 0.021   # extra monthly hazard on accounts padded in April 2026
SMALL_SIGNUP_DROP = 0.38       # fewer one- and two-member sign-ups once the minimum applies
UPGRADE_AT, UPGRADE_P = 9, 0.048

# pipeline
OPP_RATE = (24.0, 37.0, 27.0)  # created a month: January 2022, February 2026 (trend), from March 2026
STAGES = ["Discovery", "Evaluation", "Proposal", "Negotiation"]
CRM_PROB = [20, 40, 60, 80]
ADV = [0.34, 0.31, 0.30, 0.37]
LOST = [0.10, 0.075, 0.07, 0.075]
TYPICAL = [2, 2, 2, 1]
STALE_DECAY = 2.3
STALE_LOSS = 0.022
CLEANUP_AGE, CLEANUP_P = 10, 0.06
SUBSIDIARY_SHARE = 0.36        # a won prospect that joins an existing parent group

REPS = 120                     # forward replications for the clean truth
