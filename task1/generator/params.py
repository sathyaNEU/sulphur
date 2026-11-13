"""The world's constants: Kraanvogel Luisterboeken B.V., Utrecht, an audiobook and e-book subscription app in the
Netherlands and Flanders. Month index 0 is January 2023; the records ship from January 2024 (month 12) to October
2026 (month 45); the world runs on to December 2027 (month 59) for the clean truth of the 2027 remuneration."""
import datetime as dt

SEED = 20261112
M0_YEAR = 2023
REC0, CUT, END = 12, 45, 59          # Jan 2024, Oct 2026, Dec 2027
R2_MONTHS = list(range(CUT - 11, CUT + 1))   # Nov 2025 to Oct 2026
SPRING24 = (12, 13, 14)              # trial starts January to March 2024
HORIZON = 24
Y2027 = list(range(48, 60))

PLANS = ["FLEX", "STD", "ONB", "GEZ"]
PLAN_NAME = {"FLEX": "Kraanvogel Flex", "STD": "Kraanvogel Standaard", "ONB": "Kraanvogel Onbeperkt",
             "GEZ": "Kraanvogel Gezin"}
PRICE = {"FLEX": 9.99, "STD": 14.99, "ONB": 18.99, "GEZ": 22.99}          # by 2026, VAT included
PRICE0 = {"FLEX": 9.49, "STD": 13.99, "ONB": 17.99, "GEZ": 21.99}         # 2023 and 2024
RISES = {(2025, "BE"): ("STD", "ONB"), (2025, "NL"): ("FLEX", "GEZ"), (2026, "NL"): ("STD", "ONB"),
         (2026, "BE"): ("FLEX", "GEZ")}
RIVAL = {"NL": {"FLEX": 9.79, "STD": 15.49, "ONB": 19.49, "GEZ": 23.49},   # the rival's comparable plans
         "BE": {"FLEX": 9.39, "STD": 14.49, "ONB": 18.49, "GEZ": 22.49}}
RIVAL_NAME = {"FLEX": "Luistr Basis 10 uur", "STD": "Luistr Plus 30 uur", "ONB": "Luistr Onbeperkt",
              "GEZ": "Luistr Familie"}
RISE27 = ("FLEX", "STD", "ONB", "GEZ")    # the rises the price list announces for January 2027
PRICE27 = {"FLEX": 10.99, "STD": 15.99, "ONB": 19.99, "GEZ": 24.99}       # from 1 January 2027
CAP = {"FLEX": 10.0, "STD": 30.0, "ONB": None, "GEZ": None}               # hours of listening a month
MAX_PROFILES = {"FLEX": 1, "STD": 1, "ONB": 2, "GEZ": 4}
VAT = {"NL": 0.09, "BE": 0.06}
STORE_FEE = {"apple": (0.30, 0.15), "google": (0.15, 0.15), "web": (0.0, 0.0)}
SHARE26 = 0.52                       # 2026 agreement: 52 per cent of net subscription revenue
RATE27 = 0.40                        # 2027 to 2029 agreement: EUR per counted hour
FEE27 = {"FLEX": 13.90, "STD": 44.20, "ONB": 14.20, "GEZ": 54.80}         # agency fee per trial start, spring 2027

# behaviour
CAMPAIGN = {2023: 1250, 2024: 1480, 2025: 1620, 2026: 1700}               # spring trial starts, January to March
CAMPAIGN_MIX = {"FLEX": 0.22, "STD": 0.30, "ONB": 0.28, "GEZ": 0.20}
ORGANIC = 150                        # organic trial starts a month (14-day trial)
ORGANIC_MIX = {"FLEX": 0.30, "STD": 0.36, "ONB": 0.22, "GEZ": 0.12}
BASE0 = 3300                         # paying accounts in January 2023
HOURS = {"FLEX": 6.4, "STD": 12.6, "ONB": 27.5, "GEZ": 10.0}              # adult content hours a settled month
CHILD_HOURS = 7.5
COMMUTER = {"FLEX": 0.12, "STD": 0.18, "ONB": 0.80, "GEZ": 0.10}
CONVERT = {"FLEX": 0.56, "STD": 0.63, "ONB": 0.58, "GEZ": 0.55}
CHURN = {"FLEX": 0.088, "STD": 0.052, "ONB": 0.039, "GEZ": 0.036}
SEASON = [1.03, 0.96, 0.97, 0.98, 0.99, 1.02, 1.21, 1.17, 0.94, 0.95, 0.97, 1.10]
ROUTE = {"web": 0.68, "apple": 0.21, "google": 0.11}
COUNTRY = {"NL": 0.71, "BE": 0.29}
N_PUBLISHERS = 40


def ym(m):
    return M0_YEAR + m // 12, m % 12 + 1


def month_label(m):
    y, mo = ym(m)
    return "%04d-%02d" % (y, mo)


def month_start(m):
    y, mo = ym(m)
    return dt.date(y, mo, 1)


def days_in(m):
    y, mo = ym(m)
    nxt = dt.date(y + (mo == 12), mo % 12 + 1, 1)
    return (nxt - dt.date(y, mo, 1)).days


def price_of(plan, country, m, rise27=RISE27):
    y = M0_YEAR + m // 12
    if y >= 2027:
        return PRICE27[plan] if plan in rise27 else PRICE[plan]
    p = PRICE0[plan]
    for yy in (2025, 2026):
        if y >= yy and plan in RISES.get((yy, country), ()):
            p = PRICE[plan]
    return p
