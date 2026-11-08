"""task4 architecture 4: the world's constants. Brackloon Direct Ltd delivers heavy online orders (feed, bedding,
fencing, garden goods) from its depot at Castlebar, Co. Mayo, with its own vans; each run sweeps a territory of
delivery districts in road order. Owenduff Couriers offers to take named outlying districts from January 2027."""
import datetime as dt

SEED = 4404
ORG = "Brackloon Direct Ltd"
PARTNER = "Owenduff Couriers"
DOMAIN = "brackloondirect.ie"
PARTNER_DOMAIN = "owenduffcouriers.ie"

HIST_START = dt.date(2025, 1, 2)
HIST_END = dt.date(2026, 10, 30)
AS_OF = dt.date(2026, 11, 6)

PRICE_2027 = 12.60          # Owenduff, EUR per parcel, 2027
RATE_2027 = 58.00           # Brackloon all-in van-hour rate, 2027
RATE_PARTS = (("Driver, with employer's PRSI and pension", 31.20), ("Van lease and insurance", 9.80),
              ("Fuel, tyres and servicing at the fleet's average running", 17.00))

DEPOT = ("Castlebar depot", 53.8548, -9.2988)

# code: name, lat, lon, parent (None = depot), road factor, speed km/h, run, mu (stops per delivery day, 2026),
#       parcels per stop, growth 2025 to 2026, growth 2026 to 2027 (plan), access h, local drive per stop h, offered
D = {
    "NEW": ("Newport", 53.8840, -9.5460, None, 1.22, 63, "R04", 15.0, 1.35, 1.05, 1.035, 0.06, 0.095, False),
    "MUL": ("Mulranny", 53.9060, -9.7820, "NEW", 1.25, 47, "R04", 1.8, 1.35, 1.10, 1.09, 0.07, 0.080, True),
    "ACH": ("Achill", 53.9650, -10.0400, "MUL", 1.35, 45.5, "R04", 2.9, 1.35, 1.05, 1.04, 0.10, 0.085, True),
    "CRO": ("Crossmolina", 54.1000, -9.3150, None, 1.22, 62, "R07", 14.0, 1.35, 1.06, 1.083, 0.06, 0.095, False),
    "BAN": ("Bangor Erris", 54.1430, -9.7420, "CRO", 1.24, 66, "R07", 1.4, 1.35, 1.12, 1.12, 0.07, 0.080, True),
    "BLM": ("Belmullet", 54.2250, -9.9900, "BAN", 1.25, 61, "R07", 2.5, 1.35, 1.07, 1.08, 0.10, 0.085, True),
    "WES": ("Westport rural", 53.8000, -9.5200, None, 1.20, 64, "R03", 18.0, 1.35, 1.05, 1.06, 0.05, 0.085, False),
    "LOU": ("Louisburgh", 53.7630, -9.8080, "WES", 1.30, 52, "R03", 2.1, 1.35, 1.05, 1.05, 0.10, 0.085, True),
    "AGH": ("Aghagower", 53.7400, -9.4800, None, 1.25, 60, "R05", 12.0, 1.35, 1.06, 1.093, 0.05, 0.095, False),
    "LEE": ("Leenane", 53.5960, -9.6980, "AGH", 1.30, 56, "R05", 1.3, 1.35, 1.04, 1.03, 0.07, 0.080, True),
    "LET": ("Letterfrack", 53.5520, -9.9460, "LEE", 1.30, 54, "R05", 1.7, 1.35, 1.06, 1.06, 0.07, 0.080, True),
    "CLI": ("Clifden", 53.4890, -10.0200, "LET", 1.30, 54, "R05", 4.6, 3.70, 1.05, 1.05, 0.10, 0.060, True),
    "BAL": ("Ballina rural", 54.1150, -9.1550, None, 1.20, 66, "R08", 17.0, 1.35, 1.05, 1.04, 0.05, 0.085, False),
    "KIL": ("Killala", 54.2130, -9.2200, "BAL", 1.25, 58, "R08", 4.0, 1.35, 1.05, 1.05, 0.06, 0.09, False),
    "BCA": ("Ballycastle", 54.2800, -9.3730, "KIL", 1.30, 46, "R08", 1.5, 1.35, 1.03, 1.02, 0.10, 0.085, True),
    "BRO": ("Ballinrobe", 53.6330, -9.2300, None, 1.20, 64, "R06", 15.0, 1.35, 1.05, 1.093, 0.05, 0.09, False),
    "CON": ("Cong", 53.5400, -9.2850, "BRO", 1.30, 50, "R06", 1.9, 3.00, 1.06, 1.07, 0.08, 0.075, True),
    "KTM": ("Kiltimagh", 53.8500, -9.0000, None, 1.20, 64, "R09", 13.0, 1.35, 1.05, 1.06, 0.05, 0.09, False),
    "SWI": ("Swinford", 53.9450, -8.9500, "KTM", 1.20, 64, "R09", 11.0, 1.35, 1.05, 1.06, 0.05, 0.09, False),
    "CHA": ("Charlestown", 53.9600, -8.7950, "SWI", 1.25, 60, "R09", 2.6, 2.60, 1.08, 1.10, 0.08, 0.075, True),
    "CBR": ("Castlebar town", 53.8548, -9.2988, None, 1.10, 35, "R01", 44.0, 1.20, 1.05, 1.05, 0.03, 0.05, False),
    "CLM": ("Claremorris", 53.7230, -9.0010, None, 1.18, 64, "R02", 38.0, 1.25, 1.05, 1.05, 0.04, 0.055, False),
}
# the Castlebar town district split in two in the register from 1 April 2026
SPLIT_DATE = dt.date(2026, 4, 1)
SPLIT = {"CBR": ("CBN", "Castlebar north", "CBS", "Castlebar south")}

RUNS = {
    "R01": "Castlebar town", "R02": "Claremorris", "R03": "Westport and Louisburgh", "R04": "Newport and Achill",
    "R05": "Connemara", "R06": "Ballinrobe and Cong", "R07": "Crossmolina and Erris", "R08": "Ballina and the north coast",
    "R09": "East Mayo",
}
OFFER = [k for k, v in D.items() if v[13]]

# farm and garden seasonality (lambing and spring planting, the Christmas pet trade), mean 1
SEASON = {1: 0.92, 2: 1.04, 3: 1.22, 4: 1.24, 5: 1.10, 6: 0.96, 7: 0.86, 8: 0.86, 9: 0.94, 10: 0.98, 11: 0.92, 12: 0.96}

DWELL_BASE = 2.5 / 60       # h at the door
DWELL_PARCEL = 1.0 / 60     # h per parcel handed over
DWELL_FAILED = 3.0 / 60     # h for an attempt nobody answered
FAIL_RATE = 0.035           # stops where nobody took the parcels
COLLECT_RATE = 0.03         # stops that are only a collection (a return or an empty gas bottle)
LEG_SD = 0.07               # log sd of a drive
DWELL_SD = 0.25
BREAK_AFTER = 4.5           # h out before the driver's 30-minute break
BREAK_H = 0.5
DUP_RATE = 0.015            # stop rows a handheld sent again when it re-synced
MISSING_DEP = 0.004         # stops with no departure scan


def holidays(year):
    h = {2025: ["01-01", "02-03", "03-17", "04-21", "05-05", "06-02", "08-04", "10-27", "12-25", "12-26"],
         2026: ["01-01", "02-02", "03-17", "04-06", "05-04", "06-01", "08-03", "10-26", "12-25", "12-28"],
         2027: ["01-01", "02-01", "03-17", "03-29", "05-03", "06-07", "08-02", "10-25", "12-27", "12-28"]}[year]
    return {dt.date(year, int(x[:2]), int(x[3:])) for x in h}


def delivery_days(start, end):
    out, d = [], start
    hol = holidays(start.year) | holidays(end.year)
    while d <= end:
        if d.weekday() < 5 and d not in hol:
            out.append(d)
        d += dt.timedelta(days=1)
    return out
