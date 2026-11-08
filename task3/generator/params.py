"""task3 architecture 4: the world's constants. Corlinden Water Utility's Sallow Road well field on Ravell County's
central sand plain (Wisconsin, fictional), the county's groundwater network, the wellhead protection model's parcels,
and the decision: the 2027 or the 2031 cycle of the state loan program for the nitrate removal plant."""

SEED = 4733
ASOF = (2026, 11, 6)
YEARS = list(range(1986, 2027))          # the land-cover panel
FC_YEARS = list(range(2027, 2041))       # the forecast
LIMIT = 10.0                             # mg/L nitrate as N
CYCLES = {2027: 2030, 2031: 2034}        # loan cycle -> first calendar year in service (from 1 January)
NO3_PER_N = 4.427                        # mg/L as nitrate per mg/L as nitrogen

# land-cover classes (the county's working classes; the panel carries local codes before 2008 and cropland-layer
# codes after)
CLASSES = ["FOR", "GRS", "DRY", "IRC", "IRV", "RES", "WAT"]
IRRIGATED = ("IRC", "IRV")

# recharge by class, inches a year (the wellhead model's water balance)
RECHARGE = {"FOR": 9.0, "GRS": 10.0, "DRY": 10.5, "IRC": 14.0, "IRV": 14.0, "RES": 11.0, "WAT": 0.0}


def ramp(y, a, b):
    return min(max((float(y) - a) / (b - a), 0.0), 1.0)


def leach(c, s):
    """Nitrate-N leaving the root zone under class c in land-surface year s (mg/L), before parcel and weather
    variation. Irrigation and its fertiliser intensified from 1962 to 1985; the county's nutrient management cost-share
    took irrigated acres down from 1997 to 2004."""
    irr = ramp(s, 1962, 1985)
    bmp = ramp(s, 1997, 2004)
    if c == "FOR":
        return 0.55
    if c == "GRS":
        return 1.1
    if c == "DRY":
        return 1.4 + 2.6 * ramp(s, 1958, 1980)
    if c == "IRC":
        return 2.0 + 19.5 * irr - 8.0 * bmp
    if c == "IRV":
        return 2.0 + 29.0 * irr - 11.0 * bmp
    if c == "RES":
        return 5.2
    return 0.0


# the unsaturated sand: field-capacity water content (volumetric) and the dispersion of a front's arrival
THETA = 0.155
THETA_SD = 0.007
VADOSE_SPREAD = 0.07        # sd of a leachate front's arrival, as a fraction of its travel time
SAT_SPREAD = 0.18           # sd of the aquifer travel time to a well, as a fraction of it


def vadose_years(dtw_ft, c, theta=THETA):
    q = RECHARGE[c] / 12.0
    return theta * dtw_ft / q if q > 0 else 0.0


WELLS = ["W3", "W5", "W6", "W7"]
WELL_NAMES = {"W3": "Well 3", "W5": "Well 5", "W6": "Well 6", "W7": "Well 7"}
WELL_DRILLED = {"W3": 1971, "W5": 1979, "W6": 1984, "W7": 1996}
# the 2025 water supply plan's share of the well field's pumping from 2027
PLAN_SHARE = {"W3": 0.08, "W5": 0.30, "W6": 0.32, "W7": 0.30}
# pumping history: each well's typical share 2009 to 2026 (the SCADA record varies about these)
HIST_SHARE = {"W3": 0.20, "W5": 0.27, "W6": 0.28, "W7": 0.25}
FIELD_MGD = 1.62            # 2025 average day

# the matured cohort and the ridge
RIDGE_CLEAR = [2017, 2018, 2018, 2019, 2019, 2019, 2020, 2020, 2021, 2021]
