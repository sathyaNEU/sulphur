"""Zancada's world: the channels, the calendar, prices, fees, the 2027 plan and the growth policy's bands.
Every constant the simulator and the documents share lives here."""
import datetime as dt

SEED = 61113
ORG = "Zancada Fitness S.L."
APP = "Zancada"

LAUNCH = dt.date(2024, 11, 4)          # first paid day, a Monday; the app opened in Spain, Portugal and Italy that week
WEEKS = 104                            # installs 4 November 2024 to 1 November 2026
DATA_END = dt.date(2026, 11, 8)        # the last day the exports cover
PULL = dt.date(2026, 11, 9)
MATURE_WEEKS = 52                      # installs 4 November 2024 to 2 November 2025, each with its twelve months on file
END_DAY = (DATA_END - LAUNCH).days

COUNTRIES = ("ES", "IT", "PT")
COUNTRY_SHARE = (0.60, 0.25, 0.15)
VAT = {"ES": 0.21, "IT": 0.22, "PT": 0.23}
COMMISSION = 0.15                      # Apple's Small Business Program and Google Play's subscription rate
PRICE = {"monthly": 9.99, "annual": 59.99}
PRODUCT = {"monthly": "zancada.premium.monthly", "annual": "zancada.premium.annual"}
MONTH_DAYS = 30.4375

# channel: platform, mean engagement, installs a week at the reference weekly spend s0 (EUR), the spend elasticity of
# installs, the share of installs from wider inventory past s0 (per unit of log spend over s0), the 2026 pushes
# (first week index, weeks, factor), campaigns, iOS consent intercept, the 2027 plan's weekly spend
CHANNELS = {
    "Meta iOS":         dict(ios=True,  mu=0.05,  n=330, s0=2860, el=0.80, xs=0.30, pushes=[(30, 3, 1.6), (82, 3, 1.5)],
                             camps=5,  ca=-1.00, plan=3020),
    "TikTok iOS":       dict(ios=True,  mu=-0.20, n=220, s0=2180, el=0.82, xs=0.30, pushes=[(45, 3, 1.5), (95, 2, 1.4)],
                             camps=9,  ca=-1.50, plan=2180),
    "Apple Search Ads": dict(ios=True,  mu=0.60,  n=110, s0=1070, el=0.60, xs=0.36, pushes=[(60, 3, 1.5)],
                             camps=4,  ca=None,  plan=1140),
    "Meta Android":     dict(ios=False, mu=0.00,  n=330, s0=2740, el=0.80, xs=0.30, pushes=[(40, 3, 1.5), (88, 3, 1.4)],
                             camps=6,  ca=None,  plan=2740),
    "Google Android":   dict(ios=False, mu=0.05,  n=420, s0=2380, el=0.65, xs=0.67,
                             pushes=[(14, 3, 2.0), (33, 3, 2.2), (66, 3, 2.1), (86, 3, 1.9)], camps=5, ca=None, plan=4000),
    "TikTok Android":   dict(ios=False, mu=-0.45, n=330, s0=2540, el=0.82, xs=0.30, pushes=[(8, 3, 1.7), (74, 2, 1.5)],
                             camps=12, ca=None,  plan=2540),
    "AppLovin Android": dict(ios=False, mu=-0.85, n=500, s0=1890, el=0.85, xs=0.22, pushes=[(27, 3, 1.6), (79, 3, 1.5)],
                             camps=8,  ca=None,  plan=1890),
}
ORGANIC = {"organic iOS": dict(ios=True, mu=0.25, n=380), "organic Android": dict(ios=False, mu=0.10, n=450)}
ORDER = list(CHANNELS)

CONSENT_SLOPE = 0.60                   # iOS tracking consent rises with engagement
CONSENT_OTHER = -1.20                  # Apple Search Ads and organic iOS users' consent intercept
EXP_DROP = 0.75                        # wider inventory's users are this much less engaged

LINES = (0.90, 1.20)                   # growth policy: cut below 0.90, hold from 0.90, scale from 1.20
BANDS = ("cut", "hold", "scale")


def band(x):
    return BANDS[0] if x < LINES[0] else (BANDS[1] if x < LINES[1] else BANDS[2])


def day_date(d):
    return LAUNCH + dt.timedelta(days=int(d))


def net_of(price, country):
    return price / (1 + VAT[country]) * (1 - COMMISSION)

PLAN_START = dt.date(2027, 1, 4)       # the media plan's first week (Monday)
SEASON_SPEND = {1: 1.18, 2: 1.05, 3: 1.0, 4: 1.0, 5: 0.98, 6: 0.92, 7: 0.86, 8: 0.82, 9: 1.06, 10: 1.04, 11: 1.0,
                12: 0.95}


def plan_weeks():
    """the 2027 media plan's 52 weeks: each week's Monday and the plan's weekly spend by channel"""
    out = []
    for w in range(52):
        mon = PLAN_START + dt.timedelta(days=7 * w)
        m = (mon + dt.timedelta(days=3)).month
        out.append((mon, m, {c: round(p["plan"] * SEASON_SPEND[m], -1) for c, p in CHANNELS.items()}))
    return out
