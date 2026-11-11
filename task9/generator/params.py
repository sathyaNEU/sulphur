"""task9: Halden Vault's drive fleet. Every parameter the simulator, the pack writer and the analysis share.

The world is simulated day by day per vault: drives with real manufacture batches and deploy lags, bathtub hazards by
family, vault and batch frailty, one hot batch on old firmware whose hazard ramps with age, chassis power and cooling
events, SMART precursors and two health-pull policies, replacements into the same slot, operations' decommissioning
reviews, and the Brightstore centre whose drives were running for years before the 2024 migration that starts its
records. The analysis never reads this file's world parameters; it reads the pack.
"""
import datetime as dt

SEED = 9017
FIRM = "Halden Vault"
ACQUIRED = "Brightstore"
ZONE = "America/Chicago"

SIM_START = dt.date(2017, 6, 1)        # the simulator's first day (the oldest vaults are commissioned in 2018)
REC_START = dt.date(2022, 1, 1)        # DC-1 and DC-2 telemetry starts (the warehouse was back-filled to 2022)
MIGRATION = dt.date(2024, 3, 1)        # DC-3's drives enter Halden's records (and its install dates are set to this day)
P2_START = dt.date(2025, 6, 1)         # the second health-pull policy
HARVEST_END = dt.date(2025, 8, 31)     # the prevalent stock of healthy 187>0 drives is pulled by this day
END = dt.date(2026, 9, 30)             # the record's last day
FORECAST_Q = ["2026Q4", "2027Q1", "2027Q2", "2027Q3"]
BACKTEST_Q = ["2025Q4", "2026Q1", "2026Q2", "2026Q3"]
BACKTEST_CUT = dt.date(2025, 9, 30)
BAND = (10, 90)                        # the 80 per cent interval

VAULT_DRIVES, CHASSIS, SLOTS_PER_CHASSIS = 1200, 20, 60

# family: vendor, capacity TB, canonical model string, Weibull shape and scale (years) of the wear-out hazard
FAMILY = {
    "OM-6":  dict(vendor="Meridian", tb=8,  model="MERIDIAN MD8000NM", beta=2.57, eta=14.8),
    "M-14":  dict(vendor="Meridian", tb=14, model="MERIDIAN MD14TNM",  beta=1.77, eta=28.6),
    "M-16":  dict(vendor="Meridian", tb=16, model="MERIDIAN MD16TNM",  beta=1.80, eta=29.6),
    "T-20":  dict(vendor="Tamsin",   tb=20, model="TAMSIN TS20000E",   beta=1.60, eta=29.7),
    "W-22":  dict(vendor="Tamsin",   tb=22, model="TAMSIN TS22000E",   beta=1.60, eta=25.5),
    "HX-8":  dict(vendor="Kestrel",  tb=18, model="KESTREL HX18T8A",   beta=1.70, eta=20.7),
    "KS-10": dict(vendor="Kestrel",  tb=10, model="KESTREL KS10T0A",   beta=2.85, eta=14.0),
    "VB-12": dict(vendor="Borealis", tb=12, model="BOREALIS VB12000",  beta=2.41, eta=17.4),
    "X-24":  dict(vendor="Tamsin",   tb=24, model="TAMSIN TS24000E",   beta=1.60, eta=26.0),
}
INFANT = (1.5, 1.5)                    # hazard x (1 + a exp(-months since install / b)): about x2.5 at install

# vaults: family, data centre, commission window (first, last) and how many; one model per vault, one or two batches
VAULT_PLAN = [
    ("OM-6",  "DC-1", dt.date(2018, 3, 1),  dt.date(2019, 6, 30), 10),
    ("M-14",  "DC-1", dt.date(2021, 2, 1),  dt.date(2021, 11, 30), 5),
    ("M-14",  "DC-2", dt.date(2021, 6, 1),  dt.date(2022, 3, 31), 5),
    ("M-16",  "DC-2", dt.date(2022, 5, 1),  dt.date(2023, 6, 30), 9),
    ("HX-8",  "DC-1", dt.date(2023, 7, 1),  dt.date(2024, 2, 28), 2),
    ("HX-8",  "DC-2", dt.date(2024, 6, 4), dt.date(2024, 9, 16), 5),    # the 2024-W14..W30 builds on HX8.2.0
    ("HX-8",  "DC-1", dt.date(2025, 2, 1),  dt.date(2025, 3, 31), 1),
    ("T-20",  "DC-1", dt.date(2024, 4, 1),  dt.date(2024, 12, 31), 4),
    ("T-20",  "DC-2", dt.date(2025, 1, 15), dt.date(2025, 6, 30), 4),
    ("W-22",  "DC-2", dt.date(2025, 9, 1),  dt.date(2026, 6, 30), 5),
    ("KS-10", "DC-3", dt.date(2019, 3, 1),  dt.date(2020, 6, 30), 8),
    ("VB-12", "DC-3", dt.date(2020, 4, 1),  dt.date(2021, 3, 31), 5),
]
DEPLOY_LAG = (63.0, 0.35)              # manufacture to install, days: lognormal median and sdlog
SPARE_LAG = (150.0, 0.45)              # a spare's manufacture to its install as a replacement
REPLACE_DAYS = (1, 6)                  # a failed or pulled drive's slot is refilled this many days later

VAULT_FRAILTY = (6.0, 1 / 6.0)          # gamma shape and scale: mean 1, cv 0.41
BATCH_FRAILTY = (30.0, 1 / 30.0)       # gamma shape and scale: mean 1, cv 0.18
BATCH_WEEKS = 8                        # a manufacturing batch is an eight-week build window

HOT = dict(family="HX-8", first=(2024, 16), last=(2024, 30), firmware="HX8.2.0", fixed="HX8.2.3",
           onset_months=13.0, doubling_months=6.0, cap=25.0)
FIRMWARE = {"HX-8": [((2023, 1), "HX8.1.4"), ((2024, 10), "HX8.2.0"), ((2024, 31), "HX8.2.3")],
            "KS-10": [((2018, 1), "KS10.3.2")], "VB-12": [((2019, 1), "BV12.07")],
            "OM-6": [((2017, 1), "MD80.4.1")], "M-14": [((2020, 1), "MD14.2.0")], "M-16": [((2021, 1), "MD16.1.6")],
            "T-20": [((2023, 1), "TS20.0.9")], "W-22": [((2025, 1), "TS22.0.3")], "X-24": [((2026, 1), "TS24.0.1")]}

SHOCKS_PER_DC_YEAR = 8.0               # power or cooling incidents per data centre and year
SHOCK_MULT, SHOCK_DAYS = 5.0, 21       # a chassis power event: one chassis, hazard x5 for three weeks
COOLING_SHARE, COOLING_MULT, COOLING_DAYS = 0.45, 2.5, 28   # a cooling excursion: the whole vault's row, x2.5 for four weeks
SHOCK_LOGGED = 0.70

PRECURSOR_P = 0.72                     # a failing drive shows SMART 5/187/197/198 growth before it fails
PRECURSOR_DAYS = (7, 90)
P1_DETECT, P1_LEAD = 0.55, 0.35        # P1 catches this share of precursor drives, this far into the window from failure
P2_DETECT, P2_LEAD = 0.85, 0.70
SPURIOUS_187 = 0.004                   # healthy drives developing a non-zero 187 count, per drive-year (persists)
HARVEST_DAYS = 92                      # P2's prevalent 187>0 stock is pulled over June to August 2025

REVIEWS = [dt.date(2025, 1, 15), dt.date(2025, 6, 16), dt.date(2025, 11, 17), dt.date(2026, 3, 16), dt.date(2026, 6, 15)]
DECOM_FAMILIES = {"OM-6": REVIEWS, "KS-10": [dt.date(2026, 3, 16)]}   # the reviews that retired each family's vaults
DECOM_DAYS = (21, 45)                  # decommissioning a vault takes this long

RMA_SHARE = 0.03                       # FAIL removals that come back to service within 30 days (not failures)
DUP_SHARE = 0.01
OUTAGE_SHARE = 0.005

INSTALLS_PLAN = [("2026Q4", "DC-2", "X-24", 2), ("2027Q1", "DC-2", "X-24", 2), ("2027Q2", "DC-1", "X-24", 2),
                 ("2027Q3", "DC-1", "X-24", 2)]
SPARES_ON_HAND = {"OM-6": 40, "M-14": 35, "M-16": 25, "T-20": 20, "W-22": 15, "HX-8": 60, "KS-10": 55, "VB-12": 20,
                  "X-24": 10}
COSTS = dict(migrate_vault=60000, failure_handling=250, spare_unit={"OM-6": 95, "M-14": 165, "M-16": 180, "T-20": 230,
             "W-22": 255, "HX-8": 210, "KS-10": 110, "VB-12": 125, "X-24": 280}, lead_quarters=1, stockout=0.10)

PEOPLE = dict(reliability="Amanda Higgins", dc3="Sandra Collins", capacity="Emily Salas", tech="Heidi Turner")
TECHS = ["Heidi Turner", "Joseph Jones", "Connie Johnson", "Matthew Stevens"]
