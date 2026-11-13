"""The world's constants: Wrenfold Brewery Ltd, its beers and keg sizes, its four depots and the pubs, clubs and
restaurants it delivers to, the keg fleet and its lots, the trade's habits with kegs, the 2027 plans. Every figure
the pack or the golden states is computed from these and the seeded simulation, never typed."""
import datetime as dt

SEED = 72417
ORG = "Wrenfold Brewery Ltd"
D0 = dt.date(2023, 5, 1)              # the simulation's warm-up start
RECON = dt.date(2023, 11, 30)         # the fleet reconciliation: untraced kegs written off in the register
H0 = dt.date(2023, 12, 1)             # the exports' first day
ASOF = dt.date(2026, 11, 30)          # the stocktake and the exports' last day
EXPORT = dt.date(2026, 12, 1)         # the day the exports were pulled
RFID0 = dt.date(2025, 6, 1)           # the RFID export starts here
VISITS0 = dt.date(2025, 1, 1)         # the delivery visits export starts here
DEPOSIT_DAY = dt.date(2024, 4, 1)     # deposits charged to free-trade accounts from here
ESTATE_DAY = dt.date(2027, 4, 12)     # Maplestead's first pubs listed (phased over three weeks)
KEGS_ARRIVE = dt.date(2027, 4, 26)    # an order placed by 18 December arrives in this week (the maker's quote)
SEASON = (dt.date(2027, 5, 3), dt.date(2027, 9, 26))   # the summer the order is sized for: weeks starting Monday
Y27_END = dt.date(2027, 10, 31)

PEOPLE = {"head": "Kim Taylor", "analyst": "Justin Francis", "fleet": "Edward Moss", "sales": "Louise White",
          "brewer": "Amelia Hodgson", "depot": "Toby Morley"}
ESTATE = "Maplestead Inns"
EXCHANGE = "Northern Keg Exchange"
RECOVERY = "KegTrace Recovery Services"
MAKER = "Lindqvist Fass GmbH"

SIZES = (50, 30, 20)

# beers: code, name, keg size, style, temperature response (share per degree of daily maximum above 17 C),
# Christmas lift
SKUS = [
    ("PIL", "Wrenfold Pils", 50, "lager", 0.050, 1.10),
    ("GLD", "Wrenfold Gold", 50, "smooth bitter", 0.018, 1.22),
    ("PAL", "Calder Pale", 30, "pale ale", 0.032, 1.12),
    ("IPA", "Wrenfold IPA", 30, "IPA", 0.026, 1.12),
    ("HER", "Heron Lager", 30, "premium lager", 0.046, 1.10),
    ("BLK", "Wrenfold Black", 30, "stout", 0.004, 1.30),
]
FOUNDRY_2026 = ["F01", "F02", "F03", "F04", "F05", "F06", "F07", "F08"]
FOUNDRY_NAMES = {
    "F01": "Foundry Saison", "F02": "Foundry Hazy", "F03": "Foundry Red Rye", "F04": "Foundry West Coast",
    "F05": "Foundry Session Sour", "F06": "Foundry Oat Pale", "F07": "Foundry Porter", "F08": "Foundry Kölsch",
    "F09": "Foundry DDH Pale", "F10": "Foundry Gose", "F11": "Foundry Pilsner", "F12": "Foundry Brown",
    "F13": "Foundry Amber", "F14": "Foundry Hefe", "F15": "Foundry Grisette", "F16": "Foundry Citra Single Hop",
    "F17": "Foundry Lime Lager", "F18": "Foundry Harvest Ale"}
FOUNDRY_LOT = 120            # one 24 hl pilot-kit brew fills 120 twenty-litre kegs
FOUNDRY_LOT_2027 = 200       # the 40 hl kit from January 2027 fills 200
FOUNDRY_LEAD = 16            # days from brew to fill (fermentation and conditioning in tank)
FOUNDRY_TEMP = 0.024

DEPOTS = {"BRG": "Brighouse (brewery)", "LDS": "Leeds", "YRK": "York", "SHF": "Sheffield"}
DEPOT_SHARE = {"BRG": 0.30, "LDS": 0.30, "YRK": 0.20, "SHF": 0.20}
TRUNK_DAYS = {"BRG": 0, "LDS": 1, "YRK": 1, "SHF": 1}     # depot to brewery transit
TRUNK_WEEKDAYS = {"BRG": (0, 1, 2, 3, 4, 5), "LDS": (0, 1, 2, 3, 4), "YRK": (0, 2, 4), "SHF": (1, 3)}

# outlets: channel, share, loss per keg emptied before and after deposits, foreign empties per own empty collected,
# share of emptied kegs taken by another brewer's driver (back through the exchange)
CHANNELS = {
    "FREE": {"share": 0.52, "loss": (0.0080, 0.0042), "foreign": 0.0130, "exch": 0.0080},
    "GROUP": {"share": 0.27, "loss": (0.0070, 0.0070), "foreign": 0.0190, "exch": 0.0110},
    "CLUB": {"share": 0.13, "loss": (0.0100, 0.0060), "foreign": 0.0080, "exch": 0.0050},
    "REST": {"share": 0.08, "loss": (0.0060, 0.0040), "foreign": 0.0065, "exch": 0.0040},
}
N_OUTLETS = 1960
SEASONAL_SHARE = 0.065        # cricket and golf clubs, caravan parks, riverside gardens: closed November to March
CLOSE_RATE = 0.038            # outlets closing for good each year
OPEN_RATE = 0.034             # new accounts each year
CLOSE_FATE = (0.15, 0.25, 0.60)   # kegs at a closing outlet: collected on the last visit, recovered later, lost
RECOVER_SHARE = 0.18          # kegs lost per trip that the recovery agent later finds
EXCH_LAG = (21, 70)           # days for an exchanged keg to come back
RECOV_LAG = (45, 270)

# line rates (kegs a week at the outlet's own mean), lognormal medians and spreads, and the share of outlets with the line
LINES = {"PIL": (0.62, 1.70, 0.62), "GLD": (0.42, 1.15, 0.55), "PAL": (0.40, 1.25, 0.55), "IPA": (0.20, 0.95, 0.50),
         "HER": (0.16, 1.10, 0.55), "BLK": (0.16, 0.80, 0.50), "FND": (0.24, 1.05, 0.45)}
TWO_TAPS_ABOVE = 5.0          # a line selling more than this many kegs a week is set up on two taps
COVER_DAYS = 7                # an outlet orders up to its delivery interval plus a week's cover, at least one spare
TWICE_WEEKLY_ABOVE = 7.0      # outlets selling more kegs a week than this get two deliveries a week

GROWTH = {"FREE": -0.008, "GROUP": 0.010, "CLUB": -0.020, "REST": 0.030}   # a year, per line
DOW = (0.78, 0.80, 0.86, 0.96, 1.22, 1.40, 0.98)
BANK_HOLIDAYS = [dt.date(2023, 5, 29), dt.date(2023, 8, 28), dt.date(2023, 12, 25), dt.date(2023, 12, 26),
                 dt.date(2024, 1, 1), dt.date(2024, 3, 29), dt.date(2024, 4, 1), dt.date(2024, 5, 6),
                 dt.date(2024, 5, 27), dt.date(2024, 8, 26), dt.date(2024, 12, 25), dt.date(2024, 12, 26),
                 dt.date(2025, 1, 1), dt.date(2025, 4, 18), dt.date(2025, 4, 21), dt.date(2025, 5, 5),
                 dt.date(2025, 5, 26), dt.date(2025, 8, 25), dt.date(2025, 12, 25), dt.date(2025, 12, 26),
                 dt.date(2026, 1, 1), dt.date(2026, 4, 3), dt.date(2026, 4, 6), dt.date(2026, 5, 4),
                 dt.date(2026, 5, 25), dt.date(2026, 8, 31), dt.date(2026, 12, 25), dt.date(2026, 12, 28),
                 dt.date(2027, 1, 1), dt.date(2027, 3, 26), dt.date(2027, 3, 29), dt.date(2027, 5, 3),
                 dt.date(2027, 5, 31), dt.date(2027, 8, 30)]

# the fleet: lots bought (size, purchase date, kegs, tagged)
LOTS = [
    ("50-2009", 50, dt.date(2009, 3, 2), 11000, False), ("50-2013", 50, dt.date(2013, 4, 8), 9800, False),
    ("50-2018", 50, dt.date(2018, 3, 12), 7400, False), ("50-2024", 50, dt.date(2024, 3, 18), 3600, True),
    ("50-2025", 50, dt.date(2025, 4, 7), 2400, True),
    ("30-2011", 30, dt.date(2011, 5, 9), 6500, False), ("30-2016", 30, dt.date(2016, 4, 4), 6000, False),
    ("30-2021", 30, dt.date(2021, 3, 15), 4000, False), ("30-2024", 30, dt.date(2024, 3, 18), 1700, True),
    ("30-2025", 30, dt.date(2025, 4, 7), 1200, True),
    ("20-2022", 20, dt.date(2022, 6, 6), 2500, True), ("20-2024", 20, dt.date(2024, 3, 18), 1300, True),
    ("20-2025", 20, dt.date(2025, 4, 7), 1300, True),
]
# share of each pre-2023 lot already lost and written off at earlier reconciliations (gone before the simulation)
LOT_GONE = {"50-2009": 0.47, "50-2013": 0.36, "50-2018": 0.21, "30-2011": 0.44, "30-2016": 0.33, "30-2021": 0.15,
            "20-2022": 0.03}
DAMAGE = 0.010                # share of washes that send a keg to repair
CONDEMN = 0.09                # share of repairs condemned
REPAIR_DAYS = (10, 35)

READ = {"FILL": 0.992, "DELIVER": 0.90, "RETURN": 0.985}

# 2027: Maplestead's 240 pubs list Wrenfold Pils and three 30 litre lines, delivered once a week
ESTATE_PUBS = 300
ESTATE_LINES = {"PIL": (1.05, 0.35), "PAL": (0.46, 0.35), "IPA": (0.33, 0.35), "HER": (0.39, 0.35)}
# 2027 Foundry range: ten year-round beers and eight seasonals; the range's outlets grow by a fifth
FOUNDRY_2027_CORE = ["F01", "F02", "F03", "F04", "F05", "F06", "F07", "F08", "F09", "F10"]
FOUNDRY_2027_SEASONAL = {"F11": (dt.date(2027, 4, 5), dt.date(2027, 7, 25)),
                         "F12": (dt.date(2027, 1, 4), dt.date(2027, 4, 25)),
                         "F13": (dt.date(2027, 3, 1), dt.date(2027, 6, 27)),
                         "F14": (dt.date(2027, 5, 3), dt.date(2027, 8, 29)),
                         "F15": (dt.date(2027, 5, 31), dt.date(2027, 9, 26)),
                         "F16": (dt.date(2027, 6, 14), dt.date(2027, 10, 10)),
                         "F17": (dt.date(2027, 6, 28), dt.date(2027, 9, 19)),
                         "F18": (dt.date(2027, 8, 16), dt.date(2027, 11, 28))}
FOUNDRY_OUTLET_GROWTH = 0.20
WASH_FLOAT_DAYS = 2           # the standard's working float of clean empties at the washer, in days of fills

FOUNDRY_COVER = 3            # days of dispatch beyond the brewing lead time the brewer keeps in tank and store
FOUNDRY_LIFE = 120            # days a Foundry beer is sold for after racking
