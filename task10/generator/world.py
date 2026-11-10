"""task10 architecture 7: the clean truth of Wealdmoor Power Networks' Halverton zone, simulated as its process.

Nine 33/11 kV primaries, three winters (October to March, 2023/24 to 2025/26) of half-hourly demand. A primary's load
is its base load on its own daily shape plus its heating load on the heating shape; heating rises with every degree
below the balance temperature and faster once the day is cold enough for direct electric heating to come on, by an
amount that depends on how the primary's customers heat. Each day runs a little above or below that, in a way that
carries over from the day before and is partly shared across the zone. Customers connected since 2021 draw a share
of their agreed capacity that depends on what they are and build up to it over two to three years.

The DSO schedules flexibility day-ahead at five constraint managed zones from its forecast, which knows how the
primary ran the day before. A provider delivers what is scheduled while its commissioned assets can: what they have
available that evening is a share of their commissioned capacity that falls as the day gets colder and varies from
day to day. Providers sign sites for each winter's contract, plan a commissioning date, and commission later than
planned (how much later depends on the kind of asset) or, now and then, lose the site. The DSO keeps one register of
those sites for every constraint managed zone in its licence area, Halverton's five among them. After the service
window the curtailed load comes back. The control room's ordinary 11 kV switching moves feeder sections between
primaries and is logged. Nothing here is written to the pack; pack.py writes what the systems record."""
import datetime as dt
import math

import numpy as np

SEED = 20261110
UTC = dt.timezone.utc

WINTERS = [("2023/24", dt.date(2023, 10, 1), dt.date(2024, 3, 31)),
           ("2024/25", dt.date(2024, 10, 1), dt.date(2025, 3, 31)),
           ("2025/26", dt.date(2025, 10, 1), dt.date(2026, 3, 31))]
BANK_HOLIDAYS = {dt.date(2023, 12, 25), dt.date(2023, 12, 26), dt.date(2024, 1, 1), dt.date(2024, 3, 29),
                 dt.date(2024, 12, 25), dt.date(2024, 12, 26), dt.date(2025, 1, 1),
                 dt.date(2025, 12, 25), dt.date(2025, 12, 26), dt.date(2026, 1, 1)}
TB = 15.5            # balance temperature of the zone's load (the truth; never filed)
T_DESIGN = -3.0      # the guideline's design condition, daily mean at Halverton weather station
TK, TS = 0.6, 0.9    # where direct electric heating comes on, and how gradually (the truth; never filed)
RHO = 0.62           # how much of a day's running above or below carries to the next day
SD_COMMON, SD_OWN = 0.0145, 0.0125
WINDOW_LOCAL = (16, 0, 19, 30)
CREDIT_HH = ("17:30", "18:00")   # half-hours ending, local, in which the guideline quotes a contract's delivery
ASSESS = dt.date(2028, 1, 15)    # the guideline's assessment date for winter 2027/28
BASIS = dt.date(2026, 1, 15)     # the same date in the latest winter on record
LEAD_DAYS = 12                          # a site's commissioning work starts about this long before its planned date
REGISTER_DATE = dt.date(2026, 11, 4)    # the flexibility asset register's extract
GROWTH_SAVED = dt.date(2026, 10, 30)    # the load growth register's last save
MONITOR_TO = (2026, 10)                 # last month in the large-customer summary

# code, name, legacy SCADA point, profile kind, firm MW, base load at the base shape's peak in mid-winter 2025/26
# before connections made since 2021 (MW), heating MW per degree below TB at the evening peak (b1), the extra per
# degree once direct electric heating is on (b2), year-on-year growth of the base (MW), DFES %/yr
PRIMARIES = [
    dict(key="A", code="PS40617", name="Ashcombe Road", legacy="HALV.ASHCOMBE_RD.33-11.MW", kind="res",
         firm=27.5, base=15.20, b1=0.600, b2=0.250, yoy=0.42, dfes=2.2),
    dict(key="B", code="PS40233", name="Tollbrook Lane", legacy="HALV.TOLLBROOK_LN.33-11.MW", kind="com",
         firm=26.0, base=15.30, b1=0.340, b2=0.075, yoy=0.30, dfes=1.1),
    dict(key="C", code="PS41108", name="Charlecote Way", legacy="HALV.CHARLECOTE_WY.33-11.MW", kind="res",
         firm=25.6, base=14.70, b1=0.435, b2=0.070, yoy=0.36, dfes=1.5),
    dict(key="D", code="PS40852", name="Dunmore Street", legacy="HALV.DUNMORE_ST.33-11.MW", kind="res",
         firm=20.0, base=11.45, b1=0.380, b2=0.600, yoy=0.26, dfes=1.3),
    dict(key="E", code="PS40391", name="Ravenhurst Park", legacy="HALV.RAVENHURST_PK.33-11.MW", kind="mix",
         firm=17.5, base=9.20, b1=0.290, b2=0.230, yoy=0.18, dfes=1.6),
    dict(key="F", code="PS41474", name="Fenwick Street", legacy="HALV.FENWICK_ST.33-11.MW", kind="mix",
         firm=35.0, base=22.60, b1=0.620, b2=0.060, yoy=0.55, dfes=1.8),
    dict(key="G", code="PS40975", name="Wexley Hill", legacy="HALV.WEXLEY_HL.33-11.MW", kind="com",
         firm=27.0, base=15.10, b1=0.370, b2=0.095, yoy=0.28, dfes=1.2),
    dict(key="H", code="PS41236", name="Hartwell Common", legacy="HALV.HARTWELL_CMN.33-11.MW", kind="res",
         firm=24.4, base=9.75, b1=0.590, b2=0.110, yoy=0.30, dfes=2.0),
    dict(key="I", code="PS40508", name="Kestwick Fields", legacy="HALV.KESTWICK_FLDS.33-11.MW", kind="mix",
         firm=19.5, base=9.35, b1=0.310, b2=0.150, yoy=0.20, dfes=1.4),
]
BY = {p["key"]: p for p in PRIMARIES}

# What a provider's commissioned assets have available in the evening peak, as a share of their commissioned
# capacity, by the event day's daily mean temperature. cv is the day-to-day spread of that availability; reb the
# share of the megawatts delivered that comes back in each of the four half-hours after the window. pace scales how
# late the provider's sites commission against the usual for their kind.
PROVIDERS = {
    "Corvane": dict(legal="Corvane Flex Ltd", a_hi=0.741, a_lo=0.146, t_mid=-2.2, w=4.2, cv=0.112,
                    reb=(0.335, 0.205, 0.115, 0.045), pace=1.00,    # domestic heat pumps, batteries, EV charging
                    ramp=(0.63, 0.91, 1.0, 1.0, 1.0, 1.0, 0.94)),   # aggregated assets answer an instruction quickly
    "Quillon": dict(legal="Quillon Energy Services Ltd", a_hi=0.804, a_lo=0.262, t_mid=-3.0, w=4.6, cv=0.150,
                    reb=(0.150, 0.085, 0.040, 0.015), pace=1.00,    # commercial refrigeration, HVAC and process load
                    ramp=(0.47, 0.81, 1.0, 1.0, 1.0, 1.0, 0.89)),   # plant is run down and brought back in stages
    # providers with contracts elsewhere in the licence area only
    "Tessaly": dict(legal="Tessaly Grid Services Ltd", pace=0.96),
    "Ormerod": dict(legal="Ormerod Flex Ltd", pace=1.05),
    "Brackwell": dict(legal="Brackwell Demand Response Ltd", pace=1.00),
}
# asset classes: typical site kW (low, high), median days late on the planned commissioning date, the spread of that
# (log scale), the share of sites lost before commissioning
CLASSES = {
    "Domestic heat pump aggregation": dict(kw=(45, 140), late=52, sig=0.80, lost=0.05),
    "Battery storage": dict(kw=(150, 600), late=140, sig=0.80, lost=0.06),
    "EV charging aggregation": dict(kw=(40, 160), late=34, sig=0.75, lost=0.04),
    "Commercial refrigeration": dict(kw=(60, 220), late=26, sig=0.75, lost=0.03),
    "HVAC": dict(kw=(60, 200), late=40, sig=0.80, lost=0.04),
    "Process load": dict(kw=(140, 460), late=270, sig=0.80, lost=0.07),
}
CLASS_LIST = list(CLASSES)
PCLASSES = {"Corvane": ("Domestic heat pump aggregation", "Battery storage", "EV charging aggregation"),
            "Quillon": ("Commercial refrigeration", "HVAC", "Process load")}
CONTRACT_WINTERS = ["2023/24", "2024/25", "2025/26", "2026/27", "2027/28"]
WINTER_START = {"2023/24": dt.date(2023, 11, 1), "2024/25": dt.date(2024, 11, 1), "2025/26": dt.date(2025, 11, 1),
                "2026/27": dt.date(2026, 11, 1), "2027/28": dt.date(2027, 11, 1)}
# zone primary, provider, MW contracted by winter (2026/27 is the winter beginning as the assessment is made;
# 2027/28 the winter assessed), and the mix of asset classes (by number of sites) the provider signed for each
# winter's step
ZONES = [
    dict(key="A", provider="Corvane", partner="B", nop="NOP-1172",
         mw={"2023/24": 5.5, "2024/25": 6.5, "2025/26": 7.5, "2026/27": 9.0, "2027/28": 21.0},
         mix={"early": (0.58, 0.20, 0.22), "2027/28": (0.22, 0.63, 0.15)}),
    dict(key="C", provider="Quillon", partner="D", nop="NOP-0948",
         mw={"2023/24": 2.5, "2024/25": 3.0, "2025/26": 4.0, "2026/27": 6.0, "2027/28": 8.5},
         mix={"early": (0.50, 0.42, 0.08), "2027/28": (0.50, 0.40, 0.10)}),
    dict(key="D", provider="Corvane", partner="E", nop="NOP-0877",
         mw={"2023/24": 3.0, "2024/25": 4.0, "2025/26": 5.0, "2026/27": 5.5, "2027/28": 6.0},
         mix={"early": (0.64, 0.10, 0.26), "2027/28": (0.64, 0.10, 0.26)}),
    dict(key="F", provider="Quillon", partner="G", nop="NOP-1305",
         mw={"2023/24": 2.5, "2024/25": 3.0, "2025/26": 3.5, "2026/27": 4.0, "2027/28": 13.0},
         mix={"early": (0.52, 0.41, 0.07), "2027/28": (0.06, 0.06, 0.88)}),
    dict(key="H", provider="Corvane", partner="I", nop="NOP-0761",
         mw={"2023/24": 2.0, "2024/25": 2.5, "2025/26": 3.0, "2026/27": 3.5, "2027/28": 4.0},
         mix={"early": (0.62, 0.14, 0.24), "2027/28": (0.62, 0.14, 0.24)}),
]
ZBY = {z["key"]: z for z in ZONES}
SERVICE_START = {("A", "2023/24"): dt.date(2023, 11, 27), ("C", "2023/24"): dt.date(2023, 11, 13),
                 ("H", "2023/24"): dt.date(2023, 11, 20), ("D", "2023/24"): dt.date(2023, 12, 4)}
# the other constraint managed zones in the licence area (the asset register covers them; nothing else in the pack does)
OTHER_PRIMARIES = [("PS31127", "Abbotsley"), ("PS31406", "Birchanger Lane"), ("PS32219", "Coldharbour Road"),
                   ("PS32570", "Eastfield"), ("PS33012", "Greywell"), ("PS33388", "Holmbury Green"),
                   ("PS34105", "Larkfield"), ("PS34661", "Marsh Lane"), ("PS35024", "Northgate"),
                   ("PS35793", "Oakhanger"), ("PS36240", "Pennywell Road"), ("PS36918", "Stanmore Hill"),
                   ("PS37355", "Thornbury Cross"), ("PS37802", "Upper Wickham"), ("PS38116", "Valley Road"),
                   ("PS38474", "Whitmore Park"), ("PS38930", "Yarnfield"), ("PS39208", "Ashby Fields"),
                   ("PS39561", "Bramhall Lane"), ("PS42037", "Cranleigh Road"), ("PS42395", "Dovecote"),
                   ("PS42768", "Elmstead Lane"), ("PS43120", "Foxhollow"), ("PS43586", "Grange Hill")]

# customers connected since 2021: what each kind draws in the evening peak once established, as a share of its
# agreed capacity, and how many months it takes to build up (the scale and shape of the build-up)
CONN_TYPES = {
    "Industrial unit": dict(u=0.43, tau=15.0, k=1.35),
    "Commercial unit": dict(u=0.37, tau=12.0, k=1.25),
    "EV charging hub": dict(u=0.31, tau=17.0, k=1.45),
    "Supermarket": dict(u=0.56, tau=8.0, k=1.30),
    "Data hall": dict(u=0.64, tau=19.0, k=1.50),
    "Cold store": dict(u=0.58, tau=10.0, k=1.30),
    "Bus depot charging": dict(u=0.24, tau=18.0, k=1.40),
    "School or college": dict(u=0.22, tau=9.0, k=1.20),
    "Care home": dict(u=0.47, tau=9.0, k=1.25),
    "Leisure centre": dict(u=0.41, tau=11.0, k=1.25),
}
# the connections that carry each zone primary's growth: (type, agreed kVA, energised or planned date). The rest of
# each primary's register is drawn in connections().
KEY_CONNECTIONS = {
    "C": [("Commercial unit", 5000, dt.date(2025, 11, 3)), ("Industrial unit", 3800, dt.date(2025, 12, 1)),
          ("Cold store", 3100, dt.date(2025, 12, 15))],
    "H": [("Commercial unit", 4000, dt.date(2027, 9, 13)), ("Industrial unit", 2000, dt.date(2027, 10, 11)),
          ("EV charging hub", 1150, dt.date(2027, 8, 9)), ("Care home", 260, dt.date(2025, 2, 10))],
    "A": [("Supermarket", 620, dt.date(2025, 11, 17)), ("EV charging hub", 800, dt.date(2027, 3, 22)),
          ("Commercial unit", 540, dt.date(2026, 9, 14))],
    "F": [("Industrial unit", 520, dt.date(2026, 6, 15)), ("Leisure centre", 560, dt.date(2025, 5, 19)),
          ("Commercial unit", 380, dt.date(2027, 4, 26))],
    "D": [("School or college", 350, dt.date(2025, 8, 25)), ("Commercial unit", 300, dt.date(2026, 5, 11)),
          ("Care home", 240, dt.date(2027, 5, 17))],
    # the same kinds of customer at primaries with no flexibility zone
    "G": [("Industrial unit", 2200, dt.date(2025, 11, 17)), ("Commercial unit", 900, dt.date(2027, 6, 14))],
    "I": [("Cold store", 1500, dt.date(2025, 10, 20)), ("EV charging hub", 1800, dt.date(2027, 9, 6))],
}
PF_CONN = 0.96       # kVA to kW for a connection's agreed capacity
# a provider's delivery through the window (half-hours ending 16:30 ... 19:30 local), as a share of what it delivers at
# 17:00 to 18:00, is PROVIDERS[...]["ramp"]; the first, second and last half-hours vary from evening to evening
THRESHOLD = 0.92     # the DSO schedules when its forecast of the primary's peak exceeds this share of firm capacity
STEP_MW = 0.5        # schedules are issued in half megawatts
MIN_MW = 1.0         # the smallest schedule the service terms allow
NOPS = [("NOP-1172", "A", "B"), ("NOP-1088", "A", "D"), ("NOP-0948", "C", "D"), ("NOP-0815", "C", "E"),
        ("NOP-1305", "F", "G"), ("NOP-0761", "H", "I"), ("NOP-0693", "H", "E"),
        ("NOP-1260", "B", "G"), ("NOP-0877", "D", "E"), ("NOP-1351", "G", "I"), ("NOP-0722", "E", "I"),
        ("NOP-1214", "D", "F")]


def softplus(x):
    return np.log1p(np.exp(-np.abs(x))) + np.maximum(x, 0.0)


def heating(p, T):
    """Heating MW at the evening peak half-hour at daily mean T."""
    T = np.asarray(T, float)
    return p["b1"] * np.maximum(0.0, TB - T) + p["b2"] * TS * softplus((TK - T) / TS)


def availability(provider, T):
    """Share of its commissioned capacity a provider's assets have available in the evening peak at daily mean T."""
    p = PROVIDERS[provider]
    return p["a_hi"] - (p["a_hi"] - p["a_lo"]) / (1.0 + math.exp((T - p["t_mid"]) / p["w"]))


def last_sunday(year, month):
    d = dt.date(year, month + 1, 1) - dt.timedelta(days=1) if month < 12 else dt.date(year, 12, 31)
    while d.weekday() != 6:
        d -= dt.timedelta(days=1)
    return d


def uk_offset_hours(t_utc):
    """BST from 01:00 UTC on the last Sunday of March to 01:00 UTC on the last Sunday of October."""
    y = t_utc.year
    start = dt.datetime.combine(last_sunday(y, 3), dt.time(1, 0), UTC)
    end = dt.datetime.combine(last_sunday(y, 10), dt.time(1, 0), UTC)
    return 1 if start <= t_utc < end else 0


ANCHORS = {
    ("res", False): [(0.5, .50), (3, .44), (5.5, .46), (7, .64), (8, .72), (9.5, .66), (12.5, .64), (14.5, .66),
                     (15.5, .73), (16, .79), (16.5, .885), (17, .95), (17.5, .99), (18, 1.0), (18.5, .97), (19, .92),
                     (19.5, .85), (20, .77), (21, .69), (22, .61), (23, .55), (24, .51)],
    ("res", True): [(0.5, .52), (3, .45), (6, .45), (8, .57), (10, .70), (12.5, .68), (15, .69), (16, .77),
                    (17, .87), (17.5, .92), (18, .94), (18.5, .92), (19, .87), (20, .75), (22, .61), (24, .53)],
    ("com", False): [(0.5, .36), (5, .34), (7, .50), (8, .72), (9, .88), (10, .96), (11, .99), (12, 1.0), (13, .99),
                     (14, .97), (15, .93), (16, .86), (17, .78), (17.5, .74), (18, .69), (19, .60), (20, .52),
                     (22, .42), (24, .37)],
    ("com", True): [(0.5, .35), (6, .33), (9, .44), (12, .58), (14, .60), (16, .56), (18, .52), (20, .46),
                    (22, .40), (24, .36)],
    ("mix", False): [(0.5, .45), (3, .40), (7, .60), (8, .73), (10, .77), (12.5, .78), (15, .77), (15.5, .78),
                     (16, .80), (16.5, .885), (17, .96), (17.5, 1.0), (18, 1.0), (18.5, .96), (19, .90), (19.5, .82),
                     (20, .73), (22, .60), (24, .49)],
    ("mix", True): [(0.5, .46), (4, .41), (8, .56), (10, .70), (13, .72), (16, .74), (17.5, .84), (18, .85),
                    (19, .80), (20, .72), (22, .60), (24, .50)],
}
# the heating load's own day, the same at every primary: a morning warm-up, a lower afternoon, the evening
HEAT_ANCHORS = [(0.5, .58), (3, .55), (5, .60), (6.5, .86), (7.5, .96), (9, .88), (11, .72), (14, .68), (15.5, .76),
                (16.5, .89), (17.5, .975), (18, 1.0), (18.5, .985), (19, .955), (19.5, .92), (20, .87), (21, .80),
                (22.5, .68), (24, .60)]


def _interp(pts):
    x = np.array([p[0] for p in pts])
    y = np.array([p[1] for p in pts])
    return np.interp((np.arange(48) + 1) * 0.5, x, y)


def profile(kind, weekend):
    """Shape of a day's base load by local half-hour (index 0 = the half-hour ending 00:30), weekday peak 1.0."""
    return _interp(ANCHORS[(kind, weekend)])


PROF = {(k, wk): profile(k, wk) for k in ("res", "com", "mix") for wk in (False, True)}
HEAT = _interp(HEAT_ANCHORS)


def daily_temperatures(rng):
    """Daily mean temperature (the mean of the 24 GMT-day hourly readings) for each winter, AR(1) about a
    seasonal mean; each winter carries cold spells, some reaching below the design condition."""
    out = {}
    for w, d0, d1 in WINTERS:
        days = [d0 + dt.timedelta(days=i) for i in range((d1 - d0).days + 1)]
        n = len(days)
        doy = np.array([(d - dt.date(d.year if d.month >= 7 else d.year - 1, 7, 1)).days for d in days])
        seas = 7.4 - 3.9 * np.cos(2 * np.pi * (doy - 205) / 365.0)   # ~8.8 C on 1 October, ~3.5 C in late January
        a = np.zeros(n)
        e = rng.normal(0, 1.85, n)
        for i in range(1, n):
            a[i] = 0.80 * a[i - 1] + e[i]
        t = seas + a
        k = {"2023/24": [(105, 7, -4.6), (72, 5, -2.9), (131, 4, -0.8)],
             "2024/25": [(98, 6, -6.2), (128, 4, -1.5), (59, 6, -3.6), (141, 4, -2.4)],
             "2025/26": [(96, 8, -5.3), (64, 6, -4.1), (123, 5, -2.8)]}[w]
        for start, length, low in k:
            for j in range(length):
                i = start + j
                if 0 <= i < n:
                    floor = low + 5.5 * (1 - math.sin(math.pi * (j + 0.5) / length)) + rng.normal(0, 0.4)
                    t[i] = min(t[i], floor)
        out[w] = (days, t)
    return out


def hourly_from_daily(rng, days, tday):
    """Hourly readings for each GMT day whose 24-reading mean is exactly the day's mean."""
    hrs = []
    for d, tm in zip(days, tday):
        prof = -2.2 * np.cos(2 * np.pi * (np.arange(24) - 14.5) / 24.0) + rng.normal(0, 0.35, 24)
        prof = prof - prof.mean()
        hrs.append(np.round(tm + prof, 1))
    return hrs


def months_between(d0, d1):
    return (d1 - d0).days / 30.4375


def build_up(ctype, age_months, tau_scale=1.0):
    """Share of its established evening draw a connection has reached at an age in months."""
    c = CONN_TYPES[ctype]
    a = np.maximum(np.asarray(age_months, float), 0.0)
    return 1.0 - np.exp(-(a / (c["tau"] * tau_scale)) ** c["k"])


def connections():
    """Every customer connected (or accepted to connect) since 2021 across the nine primaries: type, agreed kVA,
    dates and the customer's own established draw and pace, which the register never states."""
    types = list(CONN_TYPES)
    out = []
    rng = None

    def add(key, ctype, kva, when, planned_only=False, lead=None):
        c = CONN_TYPES[ctype]
        u = c["u"] * float(np.exp(rng.normal(0, 0.10) - 0.005))
        ts = float(np.exp(rng.normal(0, 0.12)))
        accepted = when - dt.timedelta(days=int(lead or rng.integers(170, 420)))
        out.append(dict(key=key, type=ctype, kva=int(kva), energised=None if planned_only else when, planned=when,
                        accepted=accepted, u=u, ts=ts))

    for p in PRIMARIES:
        k = p["key"]
        rng = np.random.default_rng([SEED, 311, hash_key(k)])
        for ctype, kva, when in KEY_CONNECTIONS.get(k, []):
            add(k, ctype, kva, when, planned_only=when > GROWTH_SAVED)
        # the rest: established customers connected from 2021, recent ones, and accepted offers still to energise
        n_old = int(rng.integers(6, 11))
        for _ in range(n_old):
            when = dt.date(2021, 2, 1) + dt.timedelta(days=int(rng.integers(0, 1150)))     # to spring 2024
            add(k, types[int(rng.integers(0, len(types)))], int(rng.choice([180, 250, 320, 400, 500, 650, 800, 1000, 1250])), when)
        n_new = int(rng.integers(1, 4)) if k not in KEY_CONNECTIONS else int(rng.integers(0, 2))
        for _ in range(n_new):
            when = dt.date(2024, 5, 1) + dt.timedelta(days=int(rng.integers(0, 880)))      # to autumn 2026
            add(k, types[int(rng.integers(0, len(types)))], int(rng.choice([150, 200, 260, 320, 400, 500])), when,
                planned_only=False)
        n_due = int(rng.integers(0, 3)) if k not in KEY_CONNECTIONS else 0
        for _ in range(n_due):
            when = dt.date(2026, 12, 1) + dt.timedelta(days=int(rng.integers(0, 320)))     # to October 2027
            add(k, types[int(rng.integers(0, len(types)))], int(rng.choice([150, 200, 260, 320, 400])), when,
                planned_only=True)
    for c in out:
        if c["energised"] and c["energised"] > GROWTH_SAVED:
            c["energised"] = None
    out.sort(key=lambda c: (c["accepted"], c["key"], c["kva"]))
    for i, c in enumerate(out):
        c["id"] = i
    return out


def conn_mw(c, day):
    """A connection's draw in the evening peak on a day (MW), zero before it is energised."""
    start = c["energised"] or c["planned"]
    if day <= start:
        return 0.0
    return c["kva"] * PF_CONN / 1000.0 * c["u"] * float(build_up(c["type"], months_between(start, day), c["ts"]))


def conn_expected_mw(c, day):
    """The same draw for a customer of this type with the type's own established share and pace (what a forecast
    can know of a customer not yet connected)."""
    start = c["energised"] or c["planned"]
    if day <= start:
        return 0.0
    return c["kva"] * PF_CONN / 1000.0 * CONN_TYPES[c["type"]]["u"] * float(build_up(c["type"], months_between(start, day)))


def other_zones():
    """The licence area's other constraint managed zones: provider, the winter the service began, megawatts
    contracted by winter and the mix of asset classes (by number of sites) over all six kinds."""
    rng = np.random.default_rng([SEED, 431])
    prov = ["Tessaly", "Quillon", "Ormerod", "Corvane", "Brackwell", "Tessaly", "Ormerod", "Quillon", "Brackwell",
            "Corvane", "Ormerod", "Tessaly", "Quillon", "Brackwell", "Ormerod", "Quillon", "Tessaly", "Corvane",
            "Ormerod", "Quillon", "Brackwell", "Tessaly", "Ormerod", "Quillon"]
    house = {"Corvane": (0.50, 0.26, 0.24, 0, 0, 0), "Quillon": (0, 0, 0, 0.42, 0.33, 0.25),
             "Tessaly": (0.08, 0.32, 0.08, 0.17, 0.15, 0.20), "Ormerod": (0, 0.10, 0, 0.34, 0.29, 0.27),
             "Brackwell": (0.34, 0.22, 0.28, 0.06, 0.10, 0)}
    out = []
    for i, (code, name) in enumerate(OTHER_PRIMARIES):
        p = prov[i]
        first = int(rng.choice([0, 0, 0, 1, 1, 2]))
        mw, level = {}, 0.0
        for wi, w in enumerate(CONTRACT_WINTERS):
            if wi < first:
                mw[w] = 0.0
                continue
            if wi == first:
                level = float(rng.choice([2.0, 2.5, 3.0, 3.5, 4.0, 5.0, 6.0]))
            elif w == "2027/28":
                level += float(rng.choice([0.0, 0.0, 0.5, 1.0, 1.5, 2.5, 3.5]))
            else:
                level += float(rng.choice([0.0, 0.5, 0.5, 1.0, 1.0, 1.5, 2.0]))
            mw[w] = level
        base = np.array(house[p], float)
        jit = base * np.exp(rng.normal(0, 0.25, 6))
        out.append(dict(key="X%02d" % i, code=code, name=name, provider=p, mw=mw, mix6=tuple(jit / jit.sum())))
    return out


def _mix6(z, w):
    if "mix6" in z:
        return np.array(z["mix6"], float)
    m3 = z["mix"]["2027/28" if w == "2027/28" else "early"]
    v = np.zeros(6)
    for cname, share in zip(PCLASSES[z["provider"]], m3):
        v[CLASS_LIST.index(cname)] = share
    return v


def assets():
    """Every site a provider has signed for a constraint managed zone in the licence area: class, kW, the date it
    signed, the commissioning date it planned then, and what happened (commissioned on a date, lost on a date, or
    still to come at the register's extract; a few older sites have since left the service)."""
    out = []
    zones = [dict(z, code=BY[z["key"]]["code"], name=BY[z["key"]]["name"], halverton=True) for z in ZONES] + \
            [dict(z, halverton=False) for z in other_zones()]
    for zi, z in enumerate(zones):
        prev = 0.0
        pace = PROVIDERS[z["provider"]]["pace"]
        for wi_, w in enumerate(CONTRACT_WINTERS):
            rng = np.random.default_rng([SEED, 419, hash_key(z["key"]) if z["halverton"] else 2000 + zi, wi_])
            step = z["mw"][w] - prev
            prev = z["mw"][w]
            if step <= 0:
                continue
            mix = _mix6(z, w)
            # a provider signs a little more than the step it has to fill
            target_kw = step * 1000.0 * float(rng.uniform(1.07, 1.13))
            got = 0.0
            ws = WINTER_START[w]
            while got < target_kw:
                cname = CLASS_LIST[int(rng.choice(6, p=mix / mix.sum()))]
                c = CLASSES[cname]
                kw = int(round(float(rng.uniform(*c["kw"])) / 5.0) * 5)
                kw = int(min(kw, max(40, target_kw - got + 30)))
                if w == "2027/28":
                    signed = dt.date(2026, 4, 1) + dt.timedelta(days=int(rng.integers(0, 195)))
                    planned = dt.date(2027, 4, 5) + dt.timedelta(days=int(rng.beta(2.6, 1.5) * 205))
                else:
                    signed = ws - dt.timedelta(days=int(rng.integers(150, 330)))
                    planned = min(signed + dt.timedelta(days=int(rng.integers(60, 190))), ws - dt.timedelta(days=int(rng.integers(3, 40))))
                # days from the planned date to the commissioning test: a site's work starts about a fortnight before
                # its planned date, so a few of the quick classes pass their test on or before it
                late = int(round(float(np.exp(rng.normal(math.log(c["late"] * pace + LEAD_DAYS), c["sig"]))) - LEAD_DAYS))
                lost = rng.random() < c["lost"]
                leaves = rng.random() < 0.05
                rec = dict(zone=z["key"], code=z["code"], zone_name=z["name"], provider=z["provider"], cls=cname, kw=kw,
                           signed=signed, planned=planned, winter=w, late=late, lost=bool(lost), left=None,
                           halverton=z["halverton"])
                if lost:
                    rec["lost_on"] = planned + dt.timedelta(days=int(rng.integers(20, 260)))
                    rec["commissioned"] = None
                else:
                    rec["commissioned"] = planned + dt.timedelta(days=late)
                    rec["lost_on"] = None
                    if leaves:        # a few older sites have left the service since (all before the extract)
                        left = rec["commissioned"] + dt.timedelta(days=int(rng.integers(380, 900)))
                        rec["left"] = left if left <= REGISTER_DATE - dt.timedelta(days=30) else None
                out.append(rec)
                got += kw
    out.sort(key=lambda a: (a["signed"], a["code"], a["kw"]))
    for i, a in enumerate(out):
        a["id"] = i
    return out


def commissioned_mw(A, zone, day):
    """Megawatts a zone's provider has commissioned and in service on a day."""
    return sum(a["kw"] for a in A if a["zone"] == zone and a["commissioned"] and a["commissioned"] <= day
               and not (a["left"] and a["left"] <= day)) / 1000.0


def chance_by(a, as_at, by):
    """For a site still to come at as_at: the chance it is commissioned by a later day, from the truth's own rates."""
    c = CLASSES[a["cls"]]
    med = c["late"] * PROVIDERS[a["provider"]]["pace"]
    from scipy.stats import norm

    def F(days):
        return float(norm.cdf((math.log(days + LEAD_DAYS) - math.log(med + LEAD_DAYS)) / c["sig"])) if days > -LEAD_DAYS else 0.0
    elapsed = (as_at - a["planned"]).days
    horizon = (by - a["planned"]).days
    # still to come at as_at: not commissioned yet and not lost yet (a loss falls 20 to 260 days after the plan)
    surv_c = 1.0 - F(elapsed)
    lost_by = lambda d: min(max((d - 20) / 240.0, 0.0), 1.0)
    p_alive = (1 - c["lost"]) * surv_c + c["lost"] * (1 - lost_by(elapsed))
    if p_alive <= 0:
        return 0.0
    return (1 - c["lost"]) * max(F(horizon) - F(elapsed), 0.0) / p_alive


def build():
    rng = np.random.default_rng(SEED)
    temps = daily_temperatures(rng)
    hourly = {w: hourly_from_daily(rng, *temps[w]) for w, _, _ in WINTERS}
    # the daily mean the guideline uses is the mean of the shipped hourly readings (one decimal each)
    tday = {w: np.array([np.mean(h) for h in hourly[w]]) for w, _, _ in WINTERS}
    C = connections()
    A = assets()

    stamps = {}
    for w, d0, d1 in WINTERS:
        t0 = dt.datetime.combine(d0, dt.time(0, 30), UTC)
        n = ((d1 - d0).days + 1) * 48
        stamps[w] = [t0 + dt.timedelta(minutes=30 * i) for i in range(n)]

    widx = {w: i for i, (w, _, _) in enumerate(WINTERS)}
    grid = {}
    for w, d0, d1 in WINTERS:
        hh = np.empty(len(stamps[w]), int)
        di = np.empty(len(stamps[w]), int)
        wk = np.empty(len(stamps[w]), bool)
        xm = np.empty(len(stamps[w]), bool)
        for i, t in enumerate(stamps[w]):
            tl = t + dt.timedelta(hours=uk_offset_hours(t)) - dt.timedelta(minutes=30)
            dloc = tl.date()
            di[i] = min(max((dloc - d0).days, 0), (d1 - d0).days)
            wk[i] = dloc.weekday() >= 5 or dloc in BANK_HOLIDAYS
            xm[i] = (dloc.month == 12 and dloc.day >= 24) or (dloc.month == 1 and dloc.day <= 2)
            hh[i] = tl.hour * 2 + tl.minute // 30
        grid[w] = (hh, di, wk, xm)

    # the day's running above or below: a part shared across the zone, a part of the primary's own, both carried over
    crng = np.random.default_rng([SEED, 53])
    common, resid, level = {}, {}, {}
    for w, d0, d1 in WINTERS:
        n = (d1 - d0).days + 1
        c = np.zeros(n)
        e = crng.normal(0, SD_COMMON * math.sqrt(1 - RHO ** 2), n)
        c[0] = crng.normal(0, SD_COMMON)
        for i in range(1, n):
            c[i] = RHO * c[i - 1] + e[i]
        common[w] = c
    own = {}
    for p in PRIMARIES:
        prng = np.random.default_rng([SEED, hash_key(p["key"])])
        mine = [c for c in C if c["key"] == p["key"]]
        for w, d0, d1 in WINTERS:
            hh, di, wk, xm = grid[w]
            days, _ = temps[w]
            n = len(days)
            o = np.zeros(n)
            e = prng.normal(0, SD_OWN * math.sqrt(1 - RHO ** 2), n)
            o[0] = prng.normal(0, SD_OWN)
            for i in range(1, n):
                o[i] = RHO * o[i - 1] + e[i]
            r = common[w] + o
            resid[(p["key"], w)] = r
            base = p["base"] - p["yoy"] * (2 - widx[w]) + np.array([sum(conn_mw(c, d) for c in mine) for d in days])
            level[(p["key"], w)] = base
            heat = heating(p, tday[w])
            shape = np.where(wk | xm, PROF[(p["kind"], True)][hh], PROF[(p["kind"], False)][hh])
            b = np.where(xm & ~wk, base[di] * 0.96, base[di])
            vals = (b * shape + heat[di] * HEAT[hh]) * (1 + r[di]) + prng.normal(0, 0.07 if p["firm"] > 20 else 0.05, len(hh))
            own[(p["key"], w)] = vals

    # flexibility events: scheduled day-ahead from the DSO's forecast, working weekdays November to March: the megawatts
    # the forecast shows are needed to hold the primary at 92 per cent of firm capacity, in half megawatts, at least
    # the service minimum and never more than the megawatts contracted. The forecast is the control room's: its
    # temperature forecast, and how the primary ran against it the day before.
    events = []
    erng = np.random.default_rng([SEED, 77])
    for w, d0, d1 in WINTERS:
        days, _ = temps[w]
        for di_, d in enumerate(days):
            xmas = (d.month == 12 and d.day >= 24) or (d.month == 1 and d.day <= 2)
            if d.month in (10,) or d.weekday() >= 5 or d in BANK_HOLIDAYS or xmas:
                continue
            fc_err = erng.normal(0, 0.85)
            for z in ZONES:
                p = BY[z["key"]]
                yest = resid[(p["key"], w)][di_ - 1] if di_ > 0 else 0.0
                fc = (level[(p["key"], w)][di_] + float(heating(p, tday[w][di_] + fc_err))) * (1 + RHO * yest)
                need = fc - THRESHOLD * p["firm"]
                if need > 0:
                    mw = min(z["mw"][w], max(MIN_MW, math.ceil(need / STEP_MW) * STEP_MW))
                    events.append(dict(winter=w, day=d, di=di_, zone=z["key"], provider=z["provider"], need=need,
                                       mw=mw, contract=z["mw"][w], T=float(tday[w][di_])))
    # the control room stands an instruction down on the morning when its updated forecast no longer shows the need
    # (a day that was only just over the line and is running low), and now and then for reasons of its own
    for k, ev in enumerate(events):
        u = erng.random()
        low = resid[(ev["zone"], ev["winter"])][ev["di"]] < 0.0
        ev["status"] = "Cancelled" if (ev["need"] < 0.6 and low and u < 0.55) or u < 0.006 else "Completed"
        ev["revised_mw"] = None
        if ev["status"] == "Completed" and erng.random() < 0.07 and ev["mw"] >= 2.0:
            ev["revised_mw"] = max(MIN_MW, round(ev["mw"] * float(erng.choice([0.75, 0.8, 0.85])) * 2) / 2)
        ev["eps"] = float(erng.normal(0, 0.03))        # how closely the provider's dispatch tracks a schedule it can meet
        ev["nu"] = float(erng.normal(0, 1.0))          # that evening's availability, in its own spread
        ev["rb"] = [float(x) for x in erng.normal(0, 0.18, 4)]   # the evening's come-back, half-hour by half-hour
        ev["rj"] = [float(x) for x in erng.normal(0, 1.0, 3)]    # how sharply the assets came in and went out
    events = [e for e in events if e["day"] >= SERVICE_START.get((e["zone"], e["winter"]), e["day"])
              and not (e["day"].month == 3 and e["day"] >= last_sunday(e["day"].year, 3))]

    metered = {k: v.copy() for k, v in own.items()}
    relief = {}
    for ev in events:
        ev["commissioned"] = commissioned_mw(A, ev["zone"], ev["day"])
        if ev["status"] != "Completed":
            continue
        w, d = ev["winter"], ev["day"]
        z = ZBY[ev["zone"]]
        prov = PROVIDERS[z["provider"]]
        sched = ev["revised_mw"] or ev["mw"]
        avail = availability(z["provider"], ev["T"]) * ev["commissioned"] * math.exp(prov["cv"] * ev["nu"] - 0.5 * prov["cv"] ** 2)
        delivered = min(sched * (1 + ev["eps"]), avail)
        ev["available"], ev["delivered"], ev["capped"] = avail, delivered, bool(avail < sched * (1 + ev["eps"]))
        idx = window_indices(stamps[w], d)
        shape = np.array(prov["ramp"], float)
        shape[0] = min(max(shape[0] * (1 + 0.10 * ev["rj"][0]), 0.2), 1.0)
        shape[1] = min(max(shape[1] * (1 + 0.05 * ev["rj"][1]), shape[0]), 1.0)
        shape[6] = min(max(shape[6] * (1 + 0.04 * ev["rj"][2]), 0.6), 1.0)
        r = delivered * shape
        metered[(z["key"], w)][idx] -= r
        post = idx[-1] + 1 + np.arange(4)
        back = delivered * np.array(prov["reb"]) * (1 + np.array(ev["rb"]))
        metered[(z["key"], w)][post] += back
        relief[(ev["zone"], w, d)] = (idx, r, delivered, sched, post, back)

    # the control room's 11 kV switching: a feeder section moved across a normally-open point for planned work or
    # fault restoration, from a quarter of a day to three days, logged at both operations
    srng = np.random.default_rng([SEED, 191])
    switching = []
    for w, d0, d1 in WINTERS:
        n = int(srng.integers(9, 13))
        for _ in range(n):
            nop, a, b = NOPS[int(srng.integers(0, len(NOPS)))]
            frm, to = (a, b) if srng.random() < 0.5 else (b, a)
            day = d0 + dt.timedelta(days=int(srng.integers(34, (d1 - d0).days - 3)))
            start = dt.datetime.combine(day, dt.time(int(srng.integers(7, 10)), int(srng.choice([0, 15, 30, 45]))), UTC)
            hours = float(srng.choice([4, 5, 6, 6.5, 7.5, 28, 33, 52], p=[.2, .2, .18, .15, .12, .07, .05, .03]))
            share = float(srng.uniform(0.035, 0.075))
            reason = str(srng.choice(["Planned: cable jointing", "Planned: switchgear maintenance", "Planned: RMU replacement",
                                      "Fault restoration", "Planned: tree cutting outage", "Fault restoration"]))
            switching.append(dict(winter=w, nop=nop, frm=frm, to=to, start=start, end=start + dt.timedelta(hours=hours),
                                  share=share, reason=reason))
    switching.sort(key=lambda s: s["start"])
    moved = {}
    for s in switching:
        w = s["winter"]
        st = stamps[w]
        i0 = int(math.ceil((s["start"] - st[0]).total_seconds() / 1800.0)) + 1
        i1 = int(math.floor((s["end"] - st[0]).total_seconds() / 1800.0)) + 1
        i0, i1 = max(i0, 0), min(i1, len(st))
        if i1 <= i0:
            s["mw_at_start"] = 0.0
            continue
        sec = s["share"] * own[(s["frm"], w)][i0:i1]
        metered[(s["frm"], w)][i0:i1] -= sec
        metered[(s["to"], w)][i0:i1] += sec
        s["mw_at_start"] = float(sec[0])
        moved[(s["nop"], s["start"])] = (i0, i1, sec)
    return dict(temps=temps, hourly=hourly, tday=tday, stamps=stamps, own=own, metered=metered, events=events,
                relief=relief, switching=switching, moved=moved, connections=C, assets=A, resid=resid, level=level,
                grid=grid)


def window_indices(stamps_w, day):
    """Indices of the half-hours ending 16:30 ... 19:30 local on day."""
    t_end0 = dt.datetime.combine(day, dt.time(16, 30))
    out = []
    for k in range(7):
        tl = t_end0 + dt.timedelta(minutes=30 * k)
        guess = tl.replace(tzinfo=UTC)
        off = uk_offset_hours(guess - dt.timedelta(hours=1))
        tu = guess - dt.timedelta(hours=off)
        out.append(int((tu - stamps_w[0]).total_seconds() // 1800))
    return np.array(out)


def hash_key(k):
    return {"A": 101, "B": 211, "C": 307, "D": 401, "E": 503, "F": 601, "G": 701, "H": 809, "I": 907}[k]


def design_truth(T=None):
    """The quantities the guideline's literal execution files, from the truth's own parameters: each zone primary's
    design-day profile in winter 2025/26 (15 January, an ordinary working weekday at the design temperature), what its
    connections add by the assessment date, what its provider will have commissioned then (the expectation over the
    sites still to come at the register's extract), and the share of it available on the design day."""
    T = T or build()
    C, A = T["connections"], T["assets"]
    out = {}
    for z in ZONES:
        p = BY[z["key"]]
        mine = [c for c in C if c["key"] == p["key"]]
        conn26 = sum(conn_mw(c, BASIS) for c in mine)
        base26 = p["base"] + conn26
        heat = float(heating(p, T_DESIGN))
        prof26 = base26 * PROF[(p["kind"], False)] + heat * HEAT
        # what the connections add: each energised customer on its own course, each customer still to connect on its
        # type's
        add = 0.0
        for c in mine:
            if c["energised"]:
                add += conn_mw(c, ASSESS) - conn_mw(c, BASIS)
            elif c["planned"] <= dt.date(2027, 10, 31):
                add += conn_expected_mw(c, ASSESS)
        g = (1 + p["dfes"] / 100.0) ** 2
        before26 = float(prof26.max())
        before28 = before26 * g + add
        # the commissioned megawatts expected at the assessment date
        comm_now = commissioned_mw(A, z["key"], REGISTER_DATE)
        exp_more = sum(a["kw"] * chance_by(a, REGISTER_DATE, ASSESS) for a in A
                       if a["zone"] == z["key"] and not (a["commissioned"] and a["commissioned"] <= REGISTER_DATE)
                       and not (a["lost_on"] and a["lost_on"] <= REGISTER_DATE)) / 1000.0
        leaving = sum(a["kw"] for a in A if a["zone"] == z["key"] and a["left"] and REGISTER_DATE < a["left"] <= ASSESS
                      and a["commissioned"] and a["commissioned"] <= REGISTER_DATE) / 1000.0
        av = availability(z["provider"], T_DESIGN)
        out[z["key"]] = dict(profile26=prof26, before26=before26, conn_add=add, growth=g, before28=before28,
                             commissioned_now=comm_now, commissioned=comm_now + exp_more, leaving=leaving, share=av,
                             delivered=av * (comm_now + exp_more), cv=PROVIDERS[z["provider"]]["cv"],
                             reb=PROVIDERS[z["provider"]]["reb"], contracted=z["mw"]["2027/28"])
    return out


def tables(T=None):
    """The clean truth as the analyst's tables: demand (code, t_utc end, mw), events, weather (hourly), switching,
    the asset register and the connections with their monthly evening draw."""
    import pandas as pd
    T = T or build()
    rows = []
    for p in PRIMARIES:
        for w, _, _ in WINTERS:
            rows.append(pd.DataFrame({"code": p["code"], "t_utc": pd.to_datetime(T["stamps"][w], utc=True),
                                      "mw": T["metered"][(p["key"], w)]}))
    demand = pd.concat(rows, ignore_index=True)
    ev = pd.DataFrame([dict(zone=BY[e["zone"]]["code"], provider=e["provider"], date=e["day"],
                            scheduled_mw=(e["revised_mw"] or e["mw"]), status=e["status"]) for e in T["events"]])
    sw = pd.DataFrame([dict(nop=s["nop"], frm=BY[s["frm"]]["code"], to=BY[s["to"]]["code"], start=s["start"], end=s["end"],
                            mw=s["mw_at_start"]) for s in T["switching"]])
    wrows = []
    for w, d0, d1 in WINTERS:
        days, _ = T["temps"][w]
        for d, hv in zip(days, T["hourly"][w]):
            for hr in range(24):
                wrows.append((dt.datetime.combine(d, dt.time(hr, 0), UTC), float(hv[hr])))
    weather = pd.DataFrame(wrows, columns=["t_utc", "temp_c"])
    weather["t_utc"] = pd.to_datetime(weather["t_utc"], utc=True)
    seen = lambda d: d if d and d <= REGISTER_DATE else None
    assets_t = pd.DataFrame([dict(site=a["id"], zone=a["code"], provider=a["provider"], cls=a["cls"], kw=a["kw"],
                                  winter=a["winter"], signed=a["signed"], planned=a["planned"],
                                  commissioned=seen(a["commissioned"]), lost=seen(a["lost_on"]),
                                  left=seen(a["left"]) if seen(a["commissioned"]) else None)
                             for a in T["assets"] if a["signed"] <= REGISTER_DATE])
    conns = pd.DataFrame([dict(conn=c["id"], code=BY[c["key"]]["code"], type=c["type"], kva=c["kva"],
                               accepted=c["accepted"], planned=c["planned"], energised=c["energised"])
                          for c in T["connections"]])
    return dict(demand=demand, events=ev, weather=weather, switching=sw, assets=assets_t, connections=conns,
                monitor=monitor_table(T))


def monitor_table(T):
    """Each energised customer's monthly mean draw between 16:00 and 20:00 on working days (kW), from the month after
    it was energised to the summary's last month."""
    import pandas as pd
    rng = np.random.default_rng([SEED, 523])
    rows = []
    for c in T["connections"]:
        if not c["energised"]:
            continue
        y, m = c["energised"].year, c["energised"].month
        while True:
            m += 1
            if m > 12:
                y, m = y + 1, 1
            if (y, m) > MONITOR_TO:
                break
            mid = dt.date(y, m, 15)
            kw = conn_mw(c, mid) * 1000.0 * float(np.exp(rng.normal(0, 0.055)))
            rows.append(dict(conn=c["id"], month=dt.date(y, m, 1), evening_kw=kw))
    return pd.DataFrame(rows)
