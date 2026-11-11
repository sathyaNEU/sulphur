"""Fjordkob's fresh trade, simulated as the process that makes the files.

Customers arrive through each store's trading day and buy what is on the shelf; a store's stock each morning is what
last night's order brought plus what is still sellable; the order is the order-up-to rule of the ERP (the next day's
forecast plus a safety stock set from the forecast's own recent misses against sales, less the sellable stock,
rounded up to the case pack); what reaches its last sellable day unsold is written off at close. Two forecasts feed
the rule: AutoOrdre's, which smooths each store and item's own sales on that store's own weekday pattern with the
planners' promotion uplifts, and Kornblomst's, a chain-wide model that knows the weather, local events and each
format's promotion response and that learned one weekly and seasonal pattern for the whole chain. When the shelf
empties, the customers still to come either take the other item of the pair, if it is there, or leave without it.

Three runs share every random draw: the trade as it happened (Kornblomst's forecast in the pilot stores from
2 March 2026), every store on AutoOrdre throughout, and every store on Kornblomst from 2 March 2026. The first makes
the files; the other two are the clean truth the checks measure the golden against."""
import datetime as dt
import math

import numpy as np
from scipy.special import betaincinv

SEED = 4419

# ---------------------------------------------------------------- calendar
D_SIM0 = dt.date(2025, 1, 6)        # Monday, ISO 2025-W02: eight weeks of trade before the records begin
D0 = dt.date(2025, 3, 3)            # Monday, ISO 2025-W10, the first day the files hold
D_END = dt.date(2026, 8, 30)        # Sunday, ISO 2026-W35
PILOT0 = dt.date(2026, 3, 2)        # Monday, ISO 2026-W10, the first delivery planned on Kornblomst's forecast
DAYS = [D_SIM0 + dt.timedelta(d) for d in range((D_END - D_SIM0).days + 1)]
ND = len(DAYS)
DOW = np.array([d.weekday() for d in DAYS])
ISO = [d.isocalendar() for d in DAYS]
YEAR = np.array([i[0] for i in ISO])
WEEK = np.array([i[1] for i in ISO])
PILOT = np.array([d >= PILOT0 for d in DAYS])
BASE25 = np.array([(i[0] == 2025 and 10 <= i[1] <= 35) for i in ISO])   # the same weeks of 2025
EXPORT = np.array([d >= D0 for d in DAYS])
WEEK_OFFSET = (D0 - D_SIM0).days // 7      # weeks of burn-in before the first exported week
PRE = np.array([EXPORT[k] and (not PILOT[k]) and (not BASE25[k]) for k in range(ND)])  # 2025-W36 to 2026-W09
T_YEARS = np.array([(d - D0).days / 365.0 for d in DAYS])

HOLIDAY = {
    dt.date(2025, 4, 17): ("hol", 1.10), dt.date(2025, 4, 18): ("hol", 0.85), dt.date(2025, 4, 19): ("eve", 1.25),
    dt.date(2025, 4, 20): ("hol", 0.70), dt.date(2025, 4, 21): ("hol", 0.80), dt.date(2025, 5, 29): ("hol", 0.85),
    dt.date(2025, 6, 5): ("hol", 0.90), dt.date(2025, 6, 7): ("eve", 1.10), dt.date(2025, 6, 9): ("hol", 0.85),
    dt.date(2025, 6, 23): ("eve", 1.15), dt.date(2025, 12, 22): ("eve", 1.15), dt.date(2025, 12, 23): ("eve", 1.35),
    dt.date(2025, 12, 24): ("eve", 1.30), dt.date(2025, 12, 25): ("hol", 0.25), dt.date(2025, 12, 26): ("hol", 0.55),
    dt.date(2025, 12, 31): ("eve", 1.30), dt.date(2026, 1, 1): ("hol", 0.40), dt.date(2026, 2, 15): ("eve", 1.10),
    dt.date(2026, 4, 2): ("hol", 1.10), dt.date(2026, 4, 3): ("hol", 0.85), dt.date(2026, 4, 4): ("eve", 1.25),
    dt.date(2026, 4, 5): ("hol", 0.70), dt.date(2026, 4, 6): ("hol", 0.80), dt.date(2026, 5, 14): ("hol", 0.85),
    dt.date(2026, 5, 23): ("eve", 1.10), dt.date(2026, 5, 25): ("hol", 0.85), dt.date(2026, 6, 5): ("hol", 0.90),
    dt.date(2026, 6, 23): ("eve", 1.15),
}
CATS = ["Bageri", "Frugt og grønt", "Mejeri", "Kød", "Færdigretter"]
NC = len(CATS)

# ---------------------------------------------------------------- items: 16 pairs, two of each subcategory
# name, category, shelf life (days), case pack, price DKK, gross margin rate, base units a day in a neighbourhood
# store, promotion response in the larger formats
ITEMS = [
    ("Rugbrød, fuldkorn 1000 g", 0, "Rugbrød", 4, 6, 28.0, 0.38, 13.0),
    ("Rugbrød, solsikke 750 g", 0, "Rugbrød", 4, 6, 32.0, 0.41, 8.5),
    ("Franskbrød, groft", 0, "Franskbrød", 2, 6, 22.0, 0.44, 17.0),
    ("Franskbrød, surdej", 0, "Franskbrød", 2, 6, 26.0, 0.47, 9.5),
    ("Rundstykker, 6 stk", 0, "Rundstykker", 1, 8, 30.0, 0.46, 15.0),
    ("Grovboller, 4 stk", 0, "Rundstykker", 1, 8, 34.0, 0.48, 8.0),
    ("Wienerbrød, tebirkes", 0, "Wienerbrød", 1, 10, 14.0, 0.55, 19.0),
    ("Wienerbrød, spandauer", 0, "Wienerbrød", 1, 10, 16.0, 0.56, 11.5),
    ("Salat, babyleaf 100 g", 1, "Salat", 4, 8, 20.0, 0.36, 9.5),
    ("Salat, romaine hjerter", 1, "Salat", 4, 8, 24.0, 0.35, 6.0),
    ("Jordbær 400 g", 1, "Bær", 3, 10, 30.0, 0.33, 11.0),
    ("Blåbær 225 g", 1, "Bær", 3, 10, 35.0, 0.34, 7.0),
    ("Bananer, 5 stk", 1, "Bananer", 5, 12, 15.0, 0.30, 24.0),
    ("Bananer, økologiske 5 stk", 1, "Bananer", 5, 12, 18.0, 0.31, 14.0),
    ("Skyr, naturel 1 kg", 2, "Skyr", 14, 8, 18.0, 0.31, 21.0),
    ("Skyr, vanilje 450 g", 2, "Skyr", 14, 8, 22.0, 0.33, 12.0),
    ("Letmælk 1 l", 2, "Mælk", 8, 10, 12.0, 0.22, 29.0),
    ("Letmælk, økologisk 1 l", 2, "Mælk", 8, 10, 16.0, 0.24, 17.0),
    ("Hytteost 250 g", 2, "Hytteost", 10, 6, 22.0, 0.32, 7.5),
    ("Hytteost, mager 250 g", 2, "Hytteost", 10, 6, 25.0, 0.33, 4.5),
    ("Piskefløde 38% 250 ml", 2, "Fløde", 12, 10, 16.0, 0.30, 9.5),
    ("Madlavningsfløde 9% 250 ml", 2, "Fløde", 12, 10, 19.0, 0.31, 5.5),
    ("Hakket oksekød 8-12% 500 g", 3, "Hakket kød", 4, 6, 45.0, 0.29, 11.5),
    ("Hakket grise- og kalvekød 500 g", 3, "Hakket kød", 4, 6, 39.0, 0.30, 7.5),
    ("Kyllingebryst 600 g", 3, "Kylling", 5, 6, 62.0, 0.27, 9.5),
    ("Kyllingeinderfilet 400 g", 3, "Kylling", 5, 6, 68.0, 0.28, 5.5),
    ("Sandwich, kylling og bacon", 4, "Sandwich", 2, 6, 42.0, 0.52, 11.5),
    ("Sandwich, æg og rejer", 4, "Sandwich", 2, 6, 48.0, 0.53, 7.0),
    ("Salatbowl, kylling", 4, "Salatbowl", 2, 6, 52.0, 0.50, 6.0),
    ("Salatbowl, falafel", 4, "Salatbowl", 2, 6, 55.0, 0.51, 4.0),
    ("Pasta, lasagne 400 g", 4, "Varm ret", 3, 6, 48.0, 0.45, 6.5),
    ("Pasta, kylling penne 400 g", 4, "Varm ret", 3, 6, 52.0, 0.46, 4.5),
]
NI = len(ITEMS)
ICAT = np.array([it[1] for it in ITEMS])
SUBCAT = [it[2] for it in ITEMS]
LIFE = np.array([it[3] for it in ITEMS])
PACK = np.array([it[4] for it in ITEMS])
PRICE = np.array([it[5] for it in ITEMS])
MRATE = np.array([it[6] for it in ITEMS])
COST = np.round(PRICE * (1 - MRATE), 2)
BASE = np.array([it[7] for it in ITEMS])
PAIR = np.array([i + 1 if i % 2 == 0 else i - 1 for i in range(NI)])
MAXLIFE = int(LIFE.max())
CAT_IDX = [np.where(ICAT == c)[0] for c in range(5)]

# weekly patterns, Monday first, each normalised to a mean of one
WK_WEEKEND = np.array([
    [0.85, 0.82, 0.84, 0.88, 1.05, 1.45, 1.11],
    [0.92, 0.90, 0.93, 0.97, 1.12, 1.25, 0.91],
    [0.98, 0.94, 0.95, 0.98, 1.08, 1.17, 0.90],
    [0.86, 0.85, 0.90, 0.98, 1.22, 1.30, 0.89],
    [1.05, 1.03, 1.04, 1.05, 1.10, 0.90, 0.83]])
WK_COMMUTE = np.array([
    [1.27, 1.30, 1.31, 1.29, 1.20, 0.36, 0.24],
    [1.24, 1.26, 1.28, 1.27, 1.22, 0.42, 0.29],
    [1.25, 1.27, 1.28, 1.26, 1.20, 0.40, 0.30],
    [1.21, 1.23, 1.25, 1.26, 1.28, 0.44, 0.31],
    [1.32, 1.34, 1.35, 1.33, 1.17, 0.28, 0.21]])
WK_WEEKEND = WK_WEEKEND / WK_WEEKEND.mean(axis=1, keepdims=True)
WK_COMMUTE = WK_COMMUTE / WK_COMMUTE.mean(axis=1, keepdims=True)
SEASON_AMP = np.array([0.03, 0.15, 0.02, 0.09, -0.07])   # annual swing, peak in July
TREND = {"Super": 0.005, "Kvarter": 0.02, "To Go": 0.07}
KNB = np.array([9.0, 7.5, 10.0, 7.0, 6.0])               # negative binomial size by category

# ---------------------------------------------------------------- stores
# number, name, format, town, setting, size, commuter share of the week, opening hour, closing hour
STORES = [
    (2104, "Fjordkob Super Viby", "Super", "Aarhus", "retail park", 2.95, 0.05, 7, 22),
    (2117, "Fjordkob Super Randers Syd", "Super", "Randers", "retail park", 2.55, 0.04, 7, 22),
    (2131, "Fjordkob Super Horsens", "Super", "Horsens", "town centre", 2.75, 0.09, 7, 22),
    (2146, "Fjordkob Super Silkeborg", "Super", "Silkeborg", "retail park", 2.30, 0.06, 7, 22),
    (2158, "Fjordkob Super Vejle Nord", "Super", "Vejle", "retail park", 2.40, 0.07, 7, 22),
    (2163, "Fjordkob Super Skanderborg", "Super", "Skanderborg", "town centre", 2.15, 0.08, 7, 22),
    (2179, "Fjordkob Super Risskov", "Super", "Aarhus", "suburb", 2.20, 0.05, 7, 22),
    (2185, "Fjordkob Super Grenaa", "Super", "Grenaa", "town centre", 1.95, 0.04, 7, 21),
    (3012, "Fjordkob Trøjborg", "Kvarter", "Aarhus", "neighbourhood", 1.25, 0.14, 7, 21),
    (3027, "Fjordkob Frederiksbjerg", "Kvarter", "Aarhus", "neighbourhood", 1.30, 0.18, 7, 21),
    (3031, "Fjordkob Aarhus N", "Kvarter", "Aarhus", "neighbourhood", 1.20, 0.12, 7, 21),
    (3048, "Fjordkob Højbjerg", "Kvarter", "Aarhus", "neighbourhood", 1.10, 0.08, 7, 21),
    (3055, "Fjordkob Brabrand", "Kvarter", "Aarhus", "neighbourhood", 0.95, 0.10, 7, 21),
    (3069, "Fjordkob Hasle", "Kvarter", "Aarhus", "neighbourhood", 0.90, 0.07, 7, 21),
    (3072, "Fjordkob Odder", "Kvarter", "Odder", "town", 1.05, 0.06, 7, 21),
    (3086, "Fjordkob Hinnerup", "Kvarter", "Hinnerup", "town", 0.85, 0.05, 7, 21),
    (3093, "Fjordkob Hadsten", "Kvarter", "Hadsten", "town", 0.88, 0.06, 7, 21),
    (3101, "Fjordkob Ry", "Kvarter", "Ry", "town", 0.80, 0.07, 7, 21),
    (3114, "Fjordkob Galten", "Kvarter", "Galten", "town", 0.92, 0.05, 7, 21),
    (3128, "Fjordkob Randers C", "Kvarter", "Randers", "neighbourhood", 1.00, 0.16, 7, 21),
    (3136, "Fjordkob Vejle Midtby", "Kvarter", "Vejle", "neighbourhood", 1.05, 0.21, 7, 21),
    (3142, "Fjordkob Horsens Nord", "Kvarter", "Horsens", "neighbourhood", 0.97, 0.11, 7, 21),
    (3157, "Fjordkob Aarhus Banegårdsplads", "Kvarter", "Aarhus", "by the station", 1.15, 0.71, 7, 21),
    (3165, "Fjordkob Skejby", "Kvarter", "Aarhus", "office district", 1.08, 0.58, 7, 21),
    (3170, "Fjordkob Silkeborg Banegård", "Kvarter", "Silkeborg", "by the station", 0.98, 0.52, 7, 21),
    (3189, "Fjordkob Katrinebjerg", "Kvarter", "Aarhus", "office district", 0.95, 0.66, 7, 21),
    (4203, "Fjordkob To Go Aarhus H", "To Go", "Aarhus", "station", 0.48, 0.86, 6, 21),
    (4218, "Fjordkob To Go Skanderborg St.", "To Go", "Skanderborg", "station", 0.30, 0.91, 6, 21),
    (4224, "Fjordkob To Go Horsens St.", "To Go", "Horsens", "station", 0.33, 0.88, 6, 21),
    (4237, "Fjordkob To Go Vejle St.", "To Go", "Vejle", "station", 0.36, 0.84, 6, 21),
    (4241, "Fjordkob To Go Randers St.", "To Go", "Randers", "station", 0.31, 0.87, 6, 21),
    (4256, "Fjordkob To Go Silkeborg St.", "To Go", "Silkeborg", "station", 0.27, 0.90, 6, 21),
    (4262, "Fjordkob To Go Universitetet", "To Go", "Aarhus", "campus", 0.34, 0.81, 7, 20),
    (4279, "Fjordkob To Go Navitas", "To Go", "Aarhus", "campus", 0.29, 0.78, 7, 20),
    (4285, "Fjordkob To Go Aarhus Ø", "To Go", "Aarhus", "office district", 0.32, 0.83, 7, 20),
    (4290, "Fjordkob To Go Skejby Sygehus", "To Go", "Aarhus", "hospital", 0.37, 0.68, 6, 21),
    (4307, "Fjordkob To Go Vejle Havn", "To Go", "Vejle", "office district", 0.26, 0.85, 7, 20),
    (4313, "Fjordkob To Go Katrinebjerg", "To Go", "Aarhus", "office district", 0.28, 0.89, 7, 20),
    (4326, "Fjordkob To Go Strøget", "To Go", "Aarhus", "pedestrian street", 0.72, 0.17, 8, 21),
    (4331, "Fjordkob To Go Vejle Gågade", "To Go", "Vejle", "pedestrian street", 0.63, 0.20, 8, 21),
    (4345, "Fjordkob To Go Horsens Søndergade", "To Go", "Horsens", "pedestrian street", 0.58, 0.22, 8, 21),
    (4352, "Fjordkob To Go Randers Brødregade", "To Go", "Randers", "pedestrian street", 0.49, 0.24, 8, 21),
]
NS = len(STORES)
SNO = np.array([s[0] for s in STORES])
SNAME = [s[1] for s in STORES]
FMT = np.array([s[2] for s in STORES])
TOWN = [s[3] for s in STORES]
SETTING = [s[4] for s in STORES]
SIZE = np.array([s[5] for s in STORES])
OMEGA = np.array([s[6] for s in STORES])
OPEN_H = np.array([s[7] for s in STORES])
CLOSE_H = np.array([s[8] for s in STORES])
FORMATS = ["Super", "Kvarter", "To Go"]
# the regional managers' picks: their four biggest Super stores, nine busy neighbourhood stores (three of them at a
# station or in an office district) and the three busiest To Go stores, all on pedestrian streets
PILOT_STORES = {2104, 2131, 2158, 2117, 3012, 3027, 3031, 3048, 3128, 3136, 3157, 3165, 3189, 4326, 4331, 4345}
ISPILOT = np.array([s in PILOT_STORES for s in SNO])

# competitor openings: (date, store number the discounter opened near, distance km)
OPENINGS = [
    (dt.date(2025, 5, 12), 3114, 0.8), (dt.date(2025, 5, 12), 2146, 2.6),
    (dt.date(2026, 4, 13), 3031, 0.9), (dt.date(2026, 4, 13), 3012, 1.7),
    (dt.date(2026, 6, 8), 2131, 0.7), (dt.date(2026, 6, 8), 4224, 1.3),
]

# substitution: the share of the customers who still wanted an item after its shelf emptied who take the other item
# of the pair when it is there; a store's shelf choice decides it
RECAPTURE = {"Super": 0.0, "Kvarter": 0.0, "To Go": 0.0}
# Kornblomst's 2027 licence per store a year by store format (its price list), DKK
LICENCE = {"Super": 34000, "Kvarter": 20000, "To Go": 12000}
# the ERP's service factor on the safety stock; the pilot stores ran Kornblomst's recommended setting
Z_L, Z_N = 1.05, 0.75
# the range each store carries: the To Go stores do not sell raw meat
RANGED = np.ones((NS, NI), bool)
RANGED[np.ix_(FMT == "To Go", ICAT == 3)] = False
# the To Go stores' shelf prices carry the convenience premium over the chain's price list
PREMIUM = np.where(FMT == "To Go", 1.12, 1.0)
# the warehouse breaks cases for the To Go stores
PACK_S = np.where((FMT == "To Go")[:, None], np.maximum(1, PACK[None, :] // 3), PACK[None, :]).astype(float)


def mu_unranged(w, lam_full):
    """The expected demand of the items a store does not carry, had it carried them: used only so that the random
    draws for the rest of the trade are the same whichever items each format carries."""
    return (lam_full[None, :, :] * w.wshape[:, DOW, :].transpose(1, 0, 2) * w.season[:, ICAT][:, None, :]
            * w.summer[:, :, None] * w.hol[:, :, ICAT] * np.where(w.promo[:, None, :], w.uplift[None, :, :], 1.0)
            * w.trend[:, :, None] * w.comp[:, :, None] * w.eta[:, :, ICAT])


def _hours(open_h, close_h):
    return np.arange(open_h, close_h)


def intraday_weights(cat, dow, omega, open_h, close_h):
    """Share of a day's demand in each opening hour: a weekend-trading store's shape and a commuter store's shape
    mixed by the store's commuter share of the week."""
    h = _hours(open_h, close_h) + 0.5
    def bump(c, w, a):
        return a * np.exp(-0.5 * ((h - c) / w) ** 2)
    if cat == 0:
        we = bump(9.5, 1.8, 1.0) + bump(15.5, 2.0, 0.45) + 0.08
        cm = bump(7.6, 1.0, 1.0) + bump(12.0, 1.2, 0.35) + bump(16.8, 1.2, 0.45) + 0.04
    elif cat == 1:
        we = bump(11.0, 2.5, 0.6) + bump(16.5, 1.8, 1.0) + 0.10
        cm = bump(12.0, 1.2, 0.55) + bump(16.6, 1.3, 1.0) + 0.05
    elif cat == 2:
        we = bump(10.0, 2.5, 0.75) + bump(16.5, 2.2, 1.0) + 0.12
        cm = bump(7.8, 1.1, 0.8) + bump(12.0, 1.4, 0.5) + bump(16.7, 1.3, 1.0) + 0.06
    elif cat == 3:
        we = bump(11.5, 2.0, 0.5) + bump(16.8, 1.6, 1.0) + 0.08
        cm = bump(12.0, 1.2, 0.4) + bump(16.9, 1.2, 1.0) + 0.05
    else:
        we = bump(12.0, 1.3, 1.0) + bump(17.3, 1.5, 0.8) + 0.08
        cm = bump(8.0, 1.0, 0.45) + bump(11.9, 0.9, 1.0) + bump(16.9, 1.1, 0.75) + 0.04
    if dow >= 5:
        cm = 0.6 * cm + 0.4 * (we / we.sum() * cm.sum())
        we = bump(11.0, 2.8, 1.0) + (0.25 if cat in (1, 3) else 0.1) * bump(16.0, 2.0, 1.0) + 0.06
    we, cm = we / we.sum(), cm / cm.sum()
    w = (1 - omega) * we + omega * cm
    return w / w.sum()


class World:
    """Everything the generator knows: the stores, items, calendar, demand and the three runs."""

    def __init__(self, seed=SEED):
        self.seed = seed
        rng = np.random.default_rng(seed)
        self.rng_seed = seed
        tilt = np.array([1.25, 0.45, 0.85, 0.22, 2.1])
        aff = np.exp(rng.normal(0.0, 0.33, (NS, NI)))
        skyr = np.array([1.35 if SUBCAT[i] == "Skyr" else (0.6 if SUBCAT[i] == "Mælk" else 1.0) for i in range(NI)])
        togo = (FMT == "To Go")[:, None]
        aff = np.where(togo, aff * tilt[ICAT][None, :] * skyr[None, :], aff)
        lam_full = SIZE[:, None] * BASE[None, :] * aff
        self.lam0 = lam_full * RANGED                                          # base units a day, store x item
        # weekly shape, store x dow x item
        self.wshape = np.empty((NS, 7, NI))
        for s in range(NS):
            ws = (1 - OMEGA[s]) * WK_WEEKEND + OMEGA[s] * WK_COMMUTE          # cat x 7
            ws = ws / ws.mean(axis=1, keepdims=True)
            self.wshape[s] = ws[ICAT].T
        # promotions: the weekly leaflet, chain-wide, two to four items a week
        nweeks = (ND + 6) // 7
        self.promo_week = np.zeros((nweeks, NI), bool)
        for w in range(nweeks):
            k = rng.integers(2, 5)
            self.promo_week[w, rng.choice(NI, k, replace=False)] = True
        self.promo = self.promo_week[np.arange(ND) // 7]                     # day x item
        self.uplift_big = rng.uniform(1.55, 2.35, NI)
        self.uplift_togo = 1.0 + (self.uplift_big - 1.0) * rng.uniform(0.18, 0.32, NI)
        self.promo_disc = np.round(rng.uniform(0.18, 0.30, NI), 2)
        up = np.where((FMT == "To Go")[:, None], self.uplift_togo[None, :], self.uplift_big[None, :])
        self.uplift = up                                                      # store x item
        # season by category and day; a commuter store's trade falls away in the industrial holiday weeks
        doy = np.array([d.timetuple().tm_yday for d in DAYS])
        self.season = 1.0 + SEASON_AMP[None, :] * np.cos(2 * np.pi * (doy[:, None] - 196) / 365.25)   # day x cat
        summer = np.array([1.0 if (28 <= WEEK[k] <= 31) else (0.5 if WEEK[k] in (27, 32) else 0.0) for k in range(ND)])
        street = np.array([1.0 if SETTING[s] == "pedestrian street" else 0.0 for s in range(NS)])
        self.summer = 1.0 - summer[:, None] * (0.66 * OMEGA[None, :]) + summer[:, None] * 0.08 * street[None, :]
        hol = np.ones((ND, NS, NC))
        for k, d in enumerate(DAYS):
            if d in HOLIDAY:
                kind, f = HOLIDAY[d]
                for c in range(NC):
                    fc = f
                    if c == 4 and kind == "eve":
                        fc = 1.0 + (f - 1.0) * 0.3
                    if c == 4 and kind == "hol":
                        fc = f * 0.85
                    hol[k, :, c] = fc
                hol[k, :, :] = hol[k, :, :] ** (1.0 + 2.2 * OMEGA[:, None]) if kind == "hol" else hol[k, :, :]
        self.hol = hol
        tr = np.array([TREND[f] for f in FMT])
        self.trend = np.exp(np.outer(T_YEARS, tr))                            # day x store
        comp = np.ones((ND, NS))
        idx = {s: k for k, s in enumerate(SNO)}
        for d0, sno, km in OPENINGS:
            s = idx[sno]
            depth = 0.115 * math.exp(-km / 1.25)
            start = (d0 - D_SIM0).days
            ramp = np.clip((np.arange(ND) - start + 3) / (22.0 + 6.0 * km), 0.0, 1.0)
            comp[:, s] *= 1.0 - depth * ramp
        self.comp = comp
        # weather and local events: a regional spell common to the towns, plus each store's own
        towns = sorted(set(TOWN))
        ti = np.array([towns.index(t) for t in TOWN])
        reg = np.zeros((ND, len(towns), NC))
        e = rng.normal(0, 1, (ND, len(towns), NC))
        for k in range(ND):
            reg[k] = (0.30 * reg[k - 1] if k else 0) + e[k] * 0.12
        own = rng.normal(0, 0.06, (ND, NS, NC))
        self.eta = np.exp(reg[:, ti, :] + own)                                # day x store x cat
        # expected demand, day x store x item
        mu = (self.lam0[None, :, :] * self.wshape[:, DOW, :].transpose(1, 0, 2)
              * self.season[:, ICAT][:, None, :] * self.summer[:, :, None] * self.hol[:, :, ICAT]
              * np.where(self.promo[:, None, :], self.uplift[None, :, :], 1.0)
              * self.trend[:, :, None] * self.comp[:, :, None] * self.eta[:, :, ICAT])
        self.mu = mu
        k = KNB[ICAT][None, None, :]
        mu_draw = np.where(RANGED[None, :, :], mu, mu_unranged(self, lam_full))
        self.demand = (rng.negative_binomial(np.broadcast_to(k, mu.shape), k / (k + mu_draw)) * RANGED[None, :, :]).astype(np.int64)
        # draws shared by the three runs
        self.u_time = rng.random((ND, NS, NI))
        self.u_sub = rng.random((ND, NS, NI))
        self.u_late = rng.random((ND, NS))
        self.u_short = rng.random((ND, NS, NI))
        self.eps_n = rng.normal(0, 0.06, (ND, NS, NI))
        self.n_level_err = np.exp(rng.normal(0, 0.05, (NS, NI)))
        self.plan_noise = np.exp(rng.normal(0, 0.20, NI))
        self.theta = np.array([RECAPTURE[f] for f in FMT]) + 0.0 * rng.normal(0, 0.03, NS)
        self.wl_err = np.exp(rng.normal(0, 0.035, (NS, 7, NI)))
        # intraday cumulative shares, store x cat x dow x hour
        self.cdf = {}
        for s in range(NS):
            for c in range(NC):
                for dw in range(7):
                    w = intraday_weights(c, dw, OMEGA[s], OPEN_H[s], CLOSE_H[s])
                    self.cdf[(s, c, dw)] = np.concatenate([[0.0], np.cumsum(w)])
        # the chain-wide model's weekly and seasonal pattern: every store's, weighted by its fresh volume
        vol = self.lam0.sum(axis=1)
        self.pool_wshape = (self.wshape * vol[:, None, None]).sum(axis=0) / vol.sum()      # 7 x item
        self.pool_summer = (self.summer * vol[None, :]).sum(axis=1) / vol.sum()           # day
        self.pool_hol = (self.hol * vol[None, :, None]).sum(axis=1) / vol.sum()           # day x cat
        # ambient (non-fresh) trade by week: the same stores, seasons, trends and competitors, untouched by ordering
        amb_ratio = np.array([{"Super": 2.9, "Kvarter": 2.2, "To Go": 0.8}[f] for f in FMT])
        nwk = ND // 7
        wk_day0 = np.arange(nwk) * 7
        xmas = np.array([1.28 if (DAYS[d].month == 12 and DAYS[d].day >= 15) else (1.06 if DAYS[d].month == 12 else 1.0)
                         for d in wk_day0])
        summer_w = self.summer[wk_day0 + 3]
        amb = (amb_ratio[None, :] * lam_full.sum(axis=1)[None, :] * 7 * 24.0 * xmas[:, None] * summer_w
               * self.trend[wk_day0 + 3] * self.comp[wk_day0 + 3] * np.exp(rng.normal(0, 0.025, (nwk, NS))))
        self.ambient_week = amb
        self.runs = {}

    def profile_table(self, rng_seed=5):
        """The hourly sales profile by format, category and weekday that business intelligence measured on days the
        shelf did not run empty (September 2024 to August 2025), as the store app's empty-shelf alert uses it."""
        rng = np.random.default_rng(self.seed + rng_seed)
        rows = []
        vol = self.lam0
        for f in FORMATS:
            ss = np.where(FMT == f)[0]
            oh, ch = int(OPEN_H[ss].min()), int(CLOSE_H[ss].max())
            for c in range(NC):
                for dw in range(7):
                    acc = np.zeros(ch - oh)
                    wsum = 0.0
                    for s in ss:
                        w = intraday_weights(c, dw, OMEGA[s], OPEN_H[s], CLOSE_H[s])
                        v = vol[s, CAT_IDX[c]].sum() * self.wshape[s, dw, CAT_IDX[c]].mean()
                        acc[OPEN_H[s] - oh:CLOSE_H[s] - oh] += w * v
                        wsum += v
                    noise = np.exp(rng.normal(0, 0.03, acc.shape))
                    if wsum <= 0:
                        continue                      # a category the format does not carry has no profile
                    acc = acc / wsum * noise
                    acc = acc / acc.sum()
                    for h in range(ch - oh):
                        rows.append((f, CATS[c], dw, oh + h, acc[h]))
        return rows

    # ------------------------------------------------------------ forecasts
    def forecast_n(self, k, n_level):
        """Kornblomst for day k: its own level for each store and item, the chain's weekly, seasonal and holiday
        pattern, each format's promotion response, and most of the weather and event signal."""
        f = (n_level * self.pool_wshape[DOW[k]][None, :] * self.season[k, ICAT][None, :] * self.pool_summer[k]
             * self.pool_hol[k, ICAT][None, :] * np.where(self.promo[k][None, :], self.uplift, 1.0)
             * self.eta[k][:, ICAT] ** 0.85 * np.exp(self.eps_n[k]))
        return f

    def run(self, n_stores, tag):
        """One run of the trade: n_stores is a store mask on Kornblomst's forecast from 2 March 2026."""
        inv = np.zeros((NS, NI, MAXLIFE + 1))              # units by days of shelf life left
        wl = self.wshape * self.wl_err                                         # L's learned weekly pattern
        lvl = self.lam0.copy()
        plan_up = self.uplift_big * self.plan_noise          # the planners' promotion uplift, chain-wide
        n_level = self.lam0 * self.n_level_err
        sig2 = (self.lam0 * 0.45) ** 2
        out = {key: np.zeros((ND, NS, NI)) for key in ["sold", "own_sold", "waste", "lost", "sub_in", "deliv", "order",
                                                       "fc", "ss", "open_stock", "close_stock"]}
        out["t_last"] = np.full((ND, NS, NI), np.nan)
        out["t_out"] = np.full((ND, NS, NI), np.nan)
        out["system"] = np.zeros((ND, NS), bool)
        out["fc_l"] = np.zeros((ND, NS, NI))
        out["fc_n"] = np.full((ND, NS, NI), np.nan)
        for j in range(NI):
            inv[:, j, LIFE[j]] = np.ceil(self.lam0[:, j] * 1.4)
        late_carry = np.zeros((NS, NI))
        for k in range(ND):
            stock = inv.sum(axis=2)
            out["open_stock"][k] = stock
            dem = self.demand[k].astype(float)
            own = np.minimum(dem, stock)
            unmet = dem - own
            left = stock - own
            # the pair's leftover takes part of what the empty shelf turned away
            want = np.floor(unmet[:, PAIR] * self.theta[:, None] + self.u_sub[k])
            want = np.where(unmet[:, PAIR] > 0, want, 0.0)
            take = np.minimum(want, left)
            sold = own + take
            out["sold"][k] = sold
            out["own_sold"][k] = own
            out["lost"][k] = unmet
            out["sub_in"][k] = take
            # times: on a day the shelf emptied before the day's customers were done, the last sale is the arrival
            # that took the last unit (the S-th of the day's D arrivals in the store's own trading clock); on any
            # other day it is the last of the day's arrivals
            out_mask_all = (unmet > 0) & (own > 0)
            for s in range(NS):
                for c in range(NC):
                    cdf = self.cdf[(s, c, DOW[k])]
                    ii = CAT_IDX[c]
                    d_ = dem[s, ii]
                    o_ = own[s, ii]
                    u = self.u_time[k, s, ii]
                    om = out_mask_all[s, ii]
                    q_last = u ** (1.0 / np.maximum(o_, 1.0))
                    q_out = betaincinv(np.maximum(o_, 1.0), np.maximum(d_ - o_ + 1.0, 1.0), np.clip(u, 1e-9, 1 - 1e-9))
                    q = np.where(om, q_out, q_last)
                    hrs = np.interp(q, cdf, np.arange(len(cdf))) + OPEN_H[s]
                    out["t_out"][k, s, ii] = np.where(om, hrs, np.nan)
                    out["t_last"][k, s, ii] = np.where(o_ > 0, hrs, np.nan)
            # a substitute's sales come after the other item's shelf emptied
            tk = take > 0
            if tk.any():
                ts = out["t_out"][k][:, PAIR]
                close = CLOSE_H[:, None] + 0.0 * ts
                late = ts + (close - ts) * self.u_sub[k] ** 0.5
                cur = out["t_last"][k]
                out["t_last"][k] = np.where(tk, np.fmax(cur, late), cur)
            # FIFO depletion
            rem = sold.copy()
            for r in range(1, MAXLIFE + 1):
                tk = np.minimum(inv[:, :, r], rem)
                inv[:, :, r] -= tk
                rem -= tk
            waste = inv[:, :, 1].copy()
            inv[:, :, 1] = 0.0
            out["waste"][k] = waste
            inv = np.concatenate([np.zeros((NS, NI, 1)), inv[:, :, 2:], np.zeros((NS, NI, 1))], axis=2)
            # inv index r now holds units with r days left for tomorrow; shift so index = days left at tomorrow's open
            out["close_stock"][k] = inv.sum(axis=2)
            if k == ND - 1:
                break
            kn = k + 1
            on_n = n_stores & PILOT[kn]
            out["system"][kn] = on_n
            # AutoOrdre learns from today's sales on its own weekly pattern
            pf_now = np.where(self.promo[k][None, :], plan_up[None, :], 1.0)
            hol_now = self.pool_hol[k, ICAT][None, :]
            base_now = sold / np.maximum(wl[:, DOW[k], :] * pf_now * hol_now, 0.05)
            lvl = 0.88 * lvl + 0.12 * base_now
            f_l = (lvl * wl[:, DOW[kn], :] * np.where(self.promo[kn][None, :], plan_up[None, :], 1.0)
                   * self.pool_hol[kn, ICAT][None, :])
            n_level = 0.9 * n_level + 0.1 * (self.lam0 * self.n_level_err * self.trend[k][:, None] * self.comp[k][:, None])
            f_n = self.forecast_n(kn, n_level)
            f = np.where(on_n[:, None], f_n, f_l)
            # the forecast's own recent misses against sales set the safety stock (the ERP's rule)
            err = (sold - out["fc"][k]) if k > 0 else np.zeros((NS, NI))
            sig2 = 0.96 * sig2 + 0.04 * err ** 2
            sig = np.sqrt(sig2)
            sig = np.maximum(sig, 0.5 * np.sqrt(np.maximum(f, 0.1)))
            ss = np.where(on_n[:, None], Z_N, Z_L) * sig
            usable = inv[:, :, 1:].sum(axis=2)
            # tomorrow's sellable stock excludes what expires at tomorrow's close only after it has been on sale
            need = np.maximum(0.0, f + ss - usable)
            q = np.ceil(need / PACK_S - 1e-9) * PACK_S * RANGED
            short = self.u_short[kn] < 0.005
            deliv = np.where(short, np.floor(q * 0.5 / PACK_S) * PACK_S, q)
            out["fc"][kn] = f
            out["fc_l"][kn] = f_l
            if PILOT[kn]:
                out["fc_n"][kn] = f_n
            out["ss"][kn] = ss
            out["order"][kn] = q
            out["deliv"][kn] = deliv
            for j in range(NI):
                inv[:, j, LIFE[j]] += deliv[:, j]
        self.runs[tag] = out
        return out
