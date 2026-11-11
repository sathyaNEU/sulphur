"""task7 architecture 9: Stadtwerke Haldenau's commercial customers, the council's 2019 retrofit pilot and the 2026
round, season by season from 2013/14 to 2025/26.

A season runs from 1 May to 30 April and is named by the year it ends (season 2019 is May 2018 to April 2019). Each
building's gas use in a season of long-term average weather is its type's level times its floor area times its own
level and its envelope (a single-storey hall loses more heat per square metre than a block of five floors), a slow part
that drifts and a fast part that comes and goes within the season. The actual use spreads the building's hot-water share
evenly over the days and the rest over the season's degree days. Buildings change as buildings do: an extension adds
heated floor area from the season after it is finished, and a floor stands empty for a season or three.

Every building keeps a week of its own: an office open five days from about seven, a four-day office, a shop open six
days or late every evening, a workshop on one, two or three shifts, a restaurant closed on Mondays; hotels and care homes
are lived in round the clock, apart from the conference houses and day-care centres among them. Its electricity follows
that week, a base load that never stops (servers, refrigeration, standby) and a load while it is in use. Its storeys set
how much roof it has per square metre of floor.

Every May the benchmarking notice goes to the buildings whose normalised gas use per square metre is in the top fifth of
their type. The May 2019 notice carried the council's pilot offer; the owners who answered it, each naming one measure,
were drawn by lot for the pilot's places within each measure, and the drawn buildings had their works that summer. What
the works save depends on the building: insulation of the roof or top-floor ceiling cuts the heat lost through the roof,
so it saves most where a building has much roof for its floor area and none of the hot water; heating optimisation
balances the system and lowers its heating curve, and caretakers turn the curve back up after complaints over the
winters that follow; heating controls set the heating back while a building stands empty, so they save with the length
of the empty week and nothing in a building lived in round the clock. Which measure an owner asks for depends on the
building's use and, a little in 2019 and much more in 2026 (the pilot's results by use were published in 2023 and the
utility's portal has shown each customer its load profile since 2022), on what suits the building: this year's controls
applicants stand empty for more of the week, and this year's insulation applicants have more roof per floor, than the
pilot's buildings of the same use.

An answer or an application comes with a contractor's quote, roof insulation priced on the roof's area and the other
measures on the floor's. A quote for insulation needs a survey of the roof, longer on a larger building, so insulation
answers come late in the offer's six weeks and the large ones latest; a drawn owner can still withdraw, likelier on a
large job and on an answer sent close to the deadline. The quote comes from a roofer for insulation and from a heating
firm for the others, and each firm works through its granted jobs in the order its owners answered.

Many buildings belong to owners with several of them (a chain of shops, a hotel group, a care operator, a landlord);
such an owner answers an offer for all its buildings at once, with one measure, and its facility manager runs their
heating the same way: whether the setback times a controller is given are kept or overridden, how far the heating curve
is let creep back up. The pilot's places were drawn by lot among the owners who answered, within each measure, an
owner's buildings together. A building's heating curve tends to sit higher than the building needs; heating
optimisation balances the system and sets the curve right, and a balanced system keeps part of that when the caretakers
nudge the curve back up over the winters that follow. The pandemic winters and the 2022 gas price shock moved every
building's use. From August 2019 to March 2022 the utility's service team offered every commercial customer a free
burner check district by district, and from September 2022 to March 2026, under the state's energy-saving campaign, a
heating check: the campaign's check also set the heating curve back down to what the building needs, and in a building
whose system was never balanced the curve was soon turned up again, while a balanced one held it. Since 2023 the check report recommends balancing
where it finds the system unbalanced, and owners checked in the campaign's last two winters asked for heating
optimisation in 2026 more often. The May 2026 notice carries the offer of the 2026 round, open to 30 June; the
applications received by 12 June are what the utility holds when the climate committee decides the round, and an owner
who revises a quote sends the application again."""
import datetime as dt
import math

import numpy as np

SEED = 70706
SEASONS = list(range(2014, 2027))          # season Y: 1 May Y-1 to 30 April Y
K = len(SEASONS)
SI = {s: i for i, s in enumerate(SEASONS)}
PILOT = 2019                               # the pilot: offers in the May 2019 notices, places drawn on 8 July 2019
PIPELINE = 2026                            # the 2026 round: notices of May 2026, open to 30 June 2026
N_BUILDINGS = 24000

TYPES = ["office", "retail", "hotel", "workshop", "care home", "restaurant"]
TYPE_P = [0.30, 0.24, 0.08, 0.20, 0.08, 0.10]
# normalised use per square metre of a typical building of the type (kWh), and the hot-water share the utility's
# method takes as weather-independent for the type
TYPE_LEVEL = {"office": 128.0, "retail": 112.0, "hotel": 196.0, "workshop": 146.0, "care home": 214.0,
              "restaurant": 242.0}
HW_SHARE = {"office": 0.08, "retail": 0.06, "hotel": 0.30, "workshop": 0.05, "care home": 0.25, "restaurant": 0.35}
SD_LEVEL = 0.24
PHI_SLOW, SD_SLOW = 0.90, 0.013
SD_FAST = 0.011
INTEREST_P = 0.66                          # an offered owner answers the pilot's offer
PLACES = 0.45                              # share of the answers the draw funded
APPLY_2026 = 0.40                          # an offered owner applies in the 2026 round
NOTICE_MD = (5, 20)                        # the benchmarking notices go out on 20 May
CLOSE_MD = (6, 30)                         # an offer in a notice stands to 30 June
DRAW_DATE = dt.date(2019, 7, 8)            # the pilot's places drawn by lot
RECEIVED_TO = dt.date(2026, 6, 12)         # the 2026 applications passed to the utility
ANSWER_SEED_OFFSET = 21
DRAW_SEED_OFFSET = 1996                    # the public draw of 8 July 2019
MEASURES = ["insulation", "heating optimisation", "heating controls"]
# the measure an answering owner asks for, by the building's use: the pilot's answers and the 2026 applications
MEASURE_P_2019 = {"office": [0.26, 0.40, 0.34], "retail": [0.28, 0.38, 0.34], "hotel": [0.12, 0.20, 0.68],
                  "workshop": [0.32, 0.36, 0.32], "care home": [0.10, 0.17, 0.73], "restaurant": [0.22, 0.38, 0.40]}
MEASURE_P_2026 = {"office": [0.20, 0.22, 0.58], "retail": [0.27, 0.27, 0.46], "hotel": [0.38, 0.54, 0.08],
                  "workshop": [0.34, 0.28, 0.38], "care home": [0.38, 0.57, 0.05], "restaurant": [0.27, 0.33, 0.40]}
# a building's heating curve sits above what it needs by CURVE of its heating (the type's mean; each building's own
# spreads around it); heating optimisation balances the system (a lasting cut of BALANCE of the heating) and sets the
# curve right, and a balanced building keeps a share f of the curve's cut once the caretakers have nudged it back up
# (f by the owner's facility management), creeping back with TAU_BAL seasons; a building set right by a service check
# alone, never balanced, creeps back with TAU_UNBAL seasons all the way
CURVE = {"office": 0.130, "retail": 0.120, "hotel": 0.150, "workshop": 0.120, "care home": 0.160, "restaurant": 0.130}
CURVE_SD = 0.28
BALANCE, BALANCE_SD = 0.012, 0.30
KEEP_BAL, KEEP_BAL_OWNER, KEEP_BAL_SD = 0.03, 0.02, 0.015
TAU_BAL, TAU_UNBAL = 2.2, 0.5
EFFECT_SD = 0.26                           # log spread of a building's own cut around its expected cut
# insulation of the roof or top-floor ceiling cuts INS_C of the heating where the roof is as large as the floor, less
# where there is less roof per floor; controls cut CTRL_C of the heating per unit of the week a building stands empty
# beyond CTRL_E0 (short empty spells are spent heating the building up again), and next to nothing where it is lived in
INS_C, INS_X = 0.2472, 0.75
CTRL_C, CTRL_E0, CTRL_LIVED = 0.40, 0.40, 0.004
ENV_X = 0.15                               # a building's use per square metre rises with its roof per floor
# how strongly an owner's choice follows what suits the building (the empty week for controls, the log of the roof per
# floor for insulation), in 2019 and in 2026
PICK = {2019: {"insulation": 0.0, "heating controls": 0.5}, 2026: {"insulation": 7.0, "heating controls": 18.0}}
# a building's week: the archetypes of each use (share, days open Monday to Sunday, opening hour, hours open)
SCHEDULES = {
    "office": [(0.56, "1111100", 7.3, 10.6), (0.18, "1111000", 7.4, 10.4), (0.10, "1111110", 7.2, 10.8),
               (0.12, "1111100", 6.0, 15.0), (0.04, "1111111", 0.0, 24.0)],
    "retail": [(0.53, "1111110", 8.6, 11.0), (0.25, "1111110", 7.0, 14.5), (0.13, "0111110", 9.0, 9.0),
               (0.09, "1111111", 7.0, 15.5)],
    "workshop": [(0.48, "1111100", 6.8, 9.6), (0.15, "1111110", 6.9, 9.4), (0.26, "1111100", 6.0, 16.0),
                 (0.11, "1111100", 0.0, 24.0)],
    "restaurant": [(0.55, "0111111", 10.8, 12.6), (0.25, "1111111", 10.6, 12.8), (0.15, "0011111", 11.0, 12.0),
                   (0.05, "0111111", 16.0, 8.0)],
    "hotel": [(0.95, "1111111", 0.0, 24.0), (0.05, "1111100", 7.0, 12.0)],
    "care home": [(0.88, "1111111", 0.0, 24.0), (0.12, "1111100", 7.5, 9.5)]}
LIVED_IN = ("hotel", "care home")
# storeys by use (choices and shares)
STOREYS = {"office": ([1, 2, 3, 4, 5, 6, 8], [0.08, 0.22, 0.26, 0.20, 0.12, 0.08, 0.04]),
           "retail": ([1, 2, 3], [0.55, 0.35, 0.10]), "hotel": ([2, 3, 4, 5, 6], [0.10, 0.30, 0.30, 0.20, 0.10]),
           "workshop": ([1, 2], [0.78, 0.22]), "care home": ([1, 2, 3, 4], [0.12, 0.38, 0.35, 0.15]),
           "restaurant": ([1, 2, 3], [0.50, 0.35, 0.15])}
# electricity: the base load and the load in use (W per square metre of floor), and the activity through the day of a
# building lived in round the clock (share of its load in use, hour 0 to 23)
ELEC_BASE = {"office": 3.5, "retail": 9.0, "hotel": 6.0, "workshop": 4.0, "care home": 5.0, "restaurant": 14.0}
ELEC_USE = {"office": 13.0, "retail": 20.0, "hotel": 14.0, "workshop": 22.0, "care home": 12.0, "restaurant": 38.0}
ACTIVITY = {"hotel": [0.42] * 6 + [0.60, 0.85, 0.85, 0.85] + [0.62] * 7 + [0.92] * 5 + [0.75, 0.55],
            "care home": [0.48] * 6 + [0.75] + [1.0] * 6 + [0.90] * 6 + [0.80] * 3 + [0.60, 0.60]}
# the shape of a working day's load in use, by the clock hour (lunch, the afternoon tail, a restaurant's afternoon lull,
# a workshop's break); a building's own day leans more or less on it
DAY_SHAPE = {"office": {7: 0.80, 8: 0.92, 12: 0.88, 13: 0.90, 16: 0.92, 17: 0.82, 18: 0.75, 19: 0.70},
             "retail": {7: 0.80, 8: 0.85, 9: 0.92, 16: 1.05, 17: 1.08, 18: 1.06, 19: 0.95, 20: 0.90},
             "restaurant": {10: 0.72, 11: 0.85, 12: 1.0, 13: 1.0, 14: 0.85, 15: 0.66, 16: 0.66, 17: 0.80, 18: 1.0,
                            19: 1.0, 20: 1.0, 21: 0.95, 22: 0.82, 23: 0.75},
             "workshop": {6: 0.88, 9: 0.94, 12: 0.82, 18: 0.92, 22: 0.90}}
# 2025's public holidays in Baden-Wuerttemberg by weekday (Monday first), and the weekdays' counts in 2025
HOLIDAYS_2025 = [3, 0, 1, 4, 3, 1, 0]
WEEKDAYS_2025 = [52, 52, 53, 52, 52, 52, 52]
# heating controls: how much of the first season's cut a building keeps once its staff have overridden the timers (the
# owner's facility management sets the mean), and how fast it falls there; insulation keeps it all
KEEP_CTRL, KEEP_CTRL_OWNER, KEEP_CTRL_SD, TAU_CTRL = 0.80, 0.18, 0.04, 2.0
# owners: the share of each use's buildings held in portfolios (chains, groups, operators, landlords), the portfolios'
# sizes (a discrete Pareto from PF_MIN), and the facility manager's spread on what controls save; a portfolio's
# buildings share one weekly schedule and part of their level
PORTFOLIO_SHARE = {"office": 0.40, "retail": 0.62, "hotel": 0.55, "workshop": 0.18, "care home": 0.60,
                   "restaurant": 0.45}
PF_MIN, PF_ALPHA, PF_MAX = 4, 0.95, 320
OWNER_LEVEL_SD = 0.13
OWNER_DRIFT_SD = 0.012                     # a portfolio's buildings drift together (one operator, one policy)
CTRL_OWNER_SD, CTRL_SINGLE_SD = 1.1, 0.12
CTRL_BUILDING_SD = 0.14                    # a building's own spread on what controls save, beyond its owner's
INS_OWNER_SD = 0.06
# the day an answer or application comes in: it carries a contractor's quote, so most come in the fortnight after the
# notice or in the last ten days before the offer closes, few in between; shares of the early fortnight, the weeks
# between and the last ten days, and how much a larger building pushes an answer later (per log-sd of floor area)
ANSWER_WAVES = {"insulation": (0.28, 0.10, 0.62), "heating optimisation": (0.48, 0.10, 0.42),
                "heating controls": (0.74, 0.10, 0.16)}
LATE_SIZE = {"insulation": 0.13, "heating optimisation": 0.05, "heating controls": 0.0}
# a drawn owner withdraws before the works: a base chance by measure, higher on a larger job and on an answer sent
# closer to the deadline
WITHDRAW = {"insulation": 0.052, "heating optimisation": 0.022, "heating controls": 0.011}
WITHDRAW_SIZE, WITHDRAW_DAY = 0.45, 0.028
RESUBMIT_P = 0.035                         # a 2026 applicant sends a revised quote with a second application
# the service team's free heating checks: districts in a fixed order, a first round from August 2019 to March 2022 and a
# second, under the state's energy-saving campaign, from September 2022 to March 2026; an owner takes the check for all
# its buildings or none; a check tunes the burner (a lasting cut of the whole use) and sets the curve right
N_DISTRICTS = 42
VISIT_ROUNDS = [{2020: 14, 2021: 16, 2022: 12}, {2023: 12, 2024: 12, 2025: 12, 2026: 6}]
VISIT_ACCEPT = [0.70, 0.90]
TUNE_START = 2020
BURNER_MEAN, BURNER_SD, BURNER_MAX = 0.012, 0.006, 0.03
CURVE_ROUND = 1                            # the campaign's checks (the second round) also set the heating curve right
CHECK_LEAVES = 0.25                        # the share of its crept-back excess a campaign check leaves
REPORT_FROM = 2025                         # checks from the 2024/25 winter on recommend balancing in their report
REPORT_PICK = 2.2                          # how much more often such an owner asks for heating optimisation in 2026
# buildings change: an extension adds heated floor area from the next season, the new space using about half the gas
# a square metre of the old does; a floor stands empty for one to three seasons and is let again
EXTEND_P, EXTEND_GAIN = 0.0055, 0.55
VACANT_P = 0.0045
# the pandemic winters and the gas price shock: every building's cut by type in those seasons
COVID = {2020: {"office": 0.02, "retail": 0.03, "hotel": 0.06, "workshop": 0.01, "care home": 0.0, "restaurant": 0.07},
         2021: {"office": 0.08, "retail": 0.07, "hotel": 0.22, "workshop": 0.03, "care home": 0.0, "restaurant": 0.25},
         2022: {"office": 0.05, "retail": 0.03, "hotel": 0.08, "workshop": 0.01, "care home": 0.0, "restaurant": 0.08}}
CRISIS = {2022: 0.020, 2023: 0.140, 2024: 0.110, 2025: 0.090, 2026: 0.072}
# quoted cost per square metre (median, euro): of roof for insulation, of heated floor for the others; the grant terms
COST_M2 = {"insulation": 92.0, "heating optimisation": 7.2, "heating controls": 18.0}   # insulation per m2 of roof
COST_SD = 0.22
GRANT_SHARE, GRANT_CAP = 0.30, 40000.0
# the contractors: a quote for roof insulation comes from a roofer, one for heating optimisation or controls from a
# heating firm, the larger firms quoting more often; a granted job waits its turn, each firm working through its jobs in
# the order its owners answered, a roofer at its own pace in square metres of roof a working day, a heating firm with
# its own fitters, each job to the first one free. Of the firms that quoted in 2019 under half the roofers and nine in
# ten heating firms still take council work in 2026 (surnames from guard.py names --geo Germany, seeds 53 and 59)
ROOFERS = ["Dachdeckerei Hande GmbH", "Paffrath Bedachungen", "Trupp Dach und Wand GmbH", "Holzbau und Dach Klingelhöfer",
           "Metz Dachtechnik", "Dachbau Becker GmbH & Co. KG", "Dachdeckerei Geisler", "Kaul Bedachungen GmbH",
           "Weimer Dach und Wand", "Holzbau und Dach Hein", "Etzler Dachtechnik GmbH", "Dachbau Patberg",
           "Dachdeckerei Seifert GmbH", "Speer Bedachungen", "Blümel Dach und Wand GmbH", "Holzbau und Dach Holsten",
           "Conradi Dachtechnik", "Dachbau Lehmann GmbH & Co. KG", "Dachdeckerei Mangold", "Sontag Bedachungen GmbH",
           "Förster Dach und Wand", "Holzbau und Dach Seidel", "Heidrich Dachtechnik GmbH", "Dachbau Beckmann",
           "Dachdeckerei Steinberg GmbH", "Kraus Bedachungen"]
HEATING_FIRMS = ["Siering Haustechnik GmbH", "Mies Heizung Sanitär", "SHK Barkholz GmbH", "Wärmetechnik Scholtz",
                 "Neureuther Gebäudetechnik", "Reising Heizungsbau GmbH", "Wesack Haustechnik", "Vollbrecht Heizung Sanitär GmbH",
                 "SHK Kambs", "Wärmetechnik Gierschner GmbH", "Putz Gebäudetechnik", "Drewes Heizungsbau",
                 "Köhler Haustechnik GmbH", "Benthin Heizung Sanitär", "SHK Jopich GmbH", "Wärmetechnik Gröttner",
                 "Schmidtke Gebäudetechnik GmbH", "Huhn Heizungsbau", "Stahr Haustechnik", "Weihmann Heizung Sanitär GmbH",
                 "SHK Eckbauer", "Wärmetechnik Lachmann GmbH", "Wulff Gebäudetechnik", "Mentzel Heizungsbau GmbH",
                 "Hecker Haustechnik", "Plath Heizung Sanitär", "SHK Kuhl GmbH", "Wärmetechnik Jäkel", "Stumpf Gebäudetechnik",
                 "Wilms Heizungsbau GmbH"]
STILL_TRADING = {"roofers": 24, "heating": 28}
ROOF_PACE = (380.0, 0.30)                  # square metres of roof a firm insulates a working day: median, log sd
FITTERS = ([1, 2, 3], [0.15, 0.45, 0.40])
# a roofer loses the days it rains (one working day in seven over the summer, the same days for every firm), starts its
# first granted roof a few days late if it is finishing other work, and a roof goes faster or slower than its area alone
# says (access, the old covering, the crew on the day)
RAIN_P = 0.14
START_LAG = [0, 0, 0, 1, 2, 3, 4]
ROOF_SD = 0.15
WORK_FROM = {2019: dt.date(2019, 7, 15), 2026: dt.date(2026, 7, 13)}   # the Monday after the draw, after the meeting
WORK_BY = {2019: dt.date(2019, 9, 30), 2026: dt.date(2026, 9, 30)}
FIRM_SEED_OFFSET = 53

# weather: Haldenau station, daily means; the anomaly a season's winter ran against the 1991 to 2020 normal
WINTER = {2014: 1.1, 2015: 0.2, 2016: 1.3, 2017: -0.4, 2018: -0.2, 2019: 0.6, 2020: 1.9, 2021: -0.3, 2022: 0.9,
          2023: 1.0, 2024: 2.0, 2025: 0.5, 2026: 1.2}


def season_days(s):
    d0 = dt.date(s - 1, 5, 1)
    return [d0 + dt.timedelta(days=i) for i in range((dt.date(s, 5, 1) - d0).days)]


def season_of(d):
    return d.year + 1 if d.month >= 5 else d.year


def _temps(rng, days, anomaly):
    doy = np.array([d.timetuple().tm_yday for d in days], dtype=float)
    seas = 9.8 - 9.4 * np.cos(2 * np.pi * (doy - 18.0) / 365.25)
    w = np.zeros(len(days))
    for i in range(1, len(days)):
        w[i] = 0.78 * w[i - 1] + rng.normal(0, 2.25)
    winter = np.clip(np.cos(2 * np.pi * (doy - 18.0) / 365.25), 0, None)
    return seas + w + anomaly * winter


def g2015(t):
    """VDI 3807 Gradtagzahl G20/15: the sum of 20 minus the daily mean over the days below 15 degrees"""
    t = np.asarray(t)
    return float(np.where(t < 15.0, 20.0 - t, 0.0).sum())


def keep_curve(f, tau, age):
    """the share of the first season's cut a building keeps at the works' age (1 is the first season after them)"""
    return f + (1.0 - f) * math.exp(-(age - 1.0) / tau)


class World:
    pass


def build(seed=SEED):
    rng = np.random.default_rng(seed)
    w = World()
    w.seed = seed
    # weather
    w.days, w.temp = {}, {}
    for s in SEASONS:
        ds = season_days(s)
        w.days[s] = ds
        w.temp[s] = np.round(_temps(rng, ds, WINTER[s]), 1)
    w.G = {s: g2015(w.temp[s]) for s in SEASONS}
    lt = [_temps(rng, season_days(2001), 0.0) for _ in range(30)]
    months = [5, 6, 7, 8, 9, 10, 11, 12, 1, 2, 3, 4]
    ds = season_days(2001)
    w.G_LT_MONTH = {}
    for m in months:
        idx = [i for i, d in enumerate(ds) if d.month == m]
        w.G_LT_MONTH[m] = round(float(np.mean([g2015(t[idx]) for t in lt])), 0)
    w.G_LT = float(sum(w.G_LT_MONTH.values()))
    # buildings
    N = N_BUILDINGS
    w.N = N
    w.typ = rng.choice(len(TYPES), N, p=TYPE_P)
    tname = np.array([TYPES[t] for t in w.typ])
    area0 = np.round(np.exp(rng.normal(math.log(880.0), 0.62, N)) / 5.0) * 5.0
    area0 = np.clip(area0, 120.0, 14000.0)
    w.size_z = (np.log(area0) - math.log(880.0)) / 0.62
    lev_b = rng.normal(0, SD_LEVEL, N)
    # owners: each use's portfolios (chains, groups, operators, landlords) and the buildings held alone
    rng_o = np.random.default_rng(seed + 61)
    w.owner = np.full(N, -1, int)
    w.portfolio = np.zeros(N, bool)
    n_own = 0
    for t in range(len(TYPES)):
        idx = rng_o.permutation(np.where(w.typ == t)[0])
        target = int(round(PORTFOLIO_SHARE[TYPES[t]] * len(idx)))
        pos = 0
        while pos < target:
            size = int(min(PF_MAX, math.floor(PF_MIN * (1.0 - rng_o.random()) ** (-1.0 / PF_ALPHA))))
            size = min(size, target - pos)
            w.owner[idx[pos:pos + size]] = n_own
            w.portfolio[idx[pos:pos + size]] = size > 1
            n_own += 1
            pos += size
        for i in idx[pos:]:
            w.owner[i] = n_own
            n_own += 1
    w.n_owners = n_own
    own_lvl = rng_o.normal(0, OWNER_LEVEL_SD, n_own)
    w.level = np.where(w.portfolio, own_lvl[w.owner] + lev_b * math.sqrt(1.0 - (OWNER_LEVEL_SD / SD_LEVEL) ** 2), lev_b)
    # each building's week and storeys: a portfolio's buildings keep one schedule, each with a little of its own
    rng_s = np.random.default_rng(seed + 29)
    w.days_open = np.zeros((N, 7), bool)
    w.open_h = np.zeros(N)
    w.len_h = np.zeros(N)
    w.arch = np.zeros(N, int)
    own_arch = {}
    for i in range(N):
        opts = SCHEDULES[TYPES[w.typ[i]]]
        o_ = int(w.owner[i])
        if w.portfolio[i] and o_ in own_arch:
            j, o0, l0 = own_arch[o_]
        else:
            j = int(rng_s.choice(len(opts), p=[o[0] for o in opts]))
            o0 = opts[j][2] + rng_s.normal(0, 0.45)
            l0 = opts[j][3] + rng_s.normal(0, 0.8)
            if w.portfolio[i]:
                own_arch[o_] = (j, o0, l0)
        _, days, o, ln = opts[j]
        w.arch[i] = j
        w.days_open[i] = [c == "1" for c in days]
        if ln >= 24.0:
            w.open_h[i], w.len_h[i] = 0.0, 24.0
        else:
            jit = 0.25 if w.portfolio[i] else 0.0
            w.open_h[i] = round(float(np.clip(o0 + rng_s.normal(0, jit), 4.0, 18.0)) * 2) / 2
            w.len_h[i] = round(float(np.clip(l0 + rng_s.normal(0, 2 * jit), 4.0, 19.0)) * 2) / 2
    w.lived_in = np.isin(tname, LIVED_IN) & (w.len_h >= 24.0)
    w.hours = np.where(w.lived_in, 168.0, w.days_open.sum(1) * w.len_h)
    w.empty = 1.0 - w.hours / 168.0
    w.storeys = np.zeros(N, int)
    for t in range(len(TYPES)):
        idx = np.where(w.typ == t)[0]
        ch, pr = STOREYS[TYPES[t]]
        w.storeys[idx] = rng_s.choice(ch, len(idx), p=pr)
    w.pitched = rng_s.random(N) < np.where(np.isin(tname, ["retail", "workshop"]), 0.25, 0.70)
    pitch = np.where(w.pitched, rng_s.uniform(1.10, 1.30, N), rng_s.uniform(1.00, 1.04, N))
    w.roof_ratio = np.clip(pitch / w.storeys * np.exp(rng_s.normal(0, 0.10, N)), 0.08, 1.6)
    w.level = w.level + ENV_X * np.log(w.roof_ratio / 0.5)
    w.hw = np.array([HW_SHARE[TYPES[t]] for t in w.typ]) + rng.normal(0, 0.02, N)
    w.hw = np.clip(w.hw, 0.02, 0.45)
    w.first = np.full(N, SEASONS[0])
    late = rng.random(N) < 0.045
    w.first[late] = rng.integers(2015, 2024, late.sum())
    w.last = np.full(N, SEASONS[-1])
    gone = (rng.random(N) < 0.035) & ~late
    w.last[gone] = rng.integers(2016, 2026, gone.sum())
    slow = np.zeros((N, K))
    fast = rng.normal(0, SD_FAST, (N, K))
    slow[:, 0] = rng.normal(0, SD_SLOW / math.sqrt(1 - PHI_SLOW ** 2), N)
    for k in range(1, K):
        slow[:, k] = PHI_SLOW * slow[:, k - 1] + rng.normal(0, SD_SLOW, N)
    # a portfolio's buildings share part of their slow drift (opening hours, temperatures, refits set by the operator)
    rng_d = np.random.default_rng(seed + 71)
    od = np.zeros((n_own, K))
    od[:, 0] = rng_d.normal(0, OWNER_DRIFT_SD / math.sqrt(1 - PHI_SLOW ** 2), n_own)
    for k in range(1, K):
        od[:, k] = PHI_SLOW * od[:, k - 1] + rng_d.normal(0, OWNER_DRIFT_SD, n_own)
    slow = slow + np.where(w.portfolio[:, None], od[w.owner], 0.0)
    w.slow, w.fast = slow, fast
    # extensions and empty floors, season by season: the floor area each season and the use they add or take away
    rng_c = np.random.default_rng(seed + 7)
    w.area = np.zeros((N, K))
    w.change = np.ones((N, K))
    a = area0.copy()
    ch = np.ones(N)
    vac_until = np.zeros(N, int)
    vac_cut = np.zeros(N)
    w.extended = np.zeros((N, K), bool)
    for k, s in enumerate(SEASONS):
        if k > 0:
            live = (w.first < s) & (w.last >= s)
            ext = live & (rng_c.random(N) < EXTEND_P)
            gain = rng_c.uniform(0.10, 0.35, N)
            add = np.round(a * gain / 5.0) * 5.0
            ch = np.where(ext, ch * (1.0 + EXTEND_GAIN * add / a), ch)
            a = np.where(ext, a + add, a)
            w.extended[:, k] = ext
            ends = (vac_until > 0) & (vac_until <= s)
            vac_cut = np.where(ends, 0.0, vac_cut)
            vac_until = np.where(ends, 0, vac_until)
            new = live & (vac_until == 0) & (rng_c.random(N) < VACANT_P)
            vac_cut = np.where(new, rng_c.uniform(0.10, 0.40, N), vac_cut)
            vac_until = np.where(new, s + rng_c.integers(1, 4, N), vac_until)
        w.area[:, k] = a
        w.change[:, k] = ch * (1.0 - vac_cut)
    w.area0 = area0
    # the service team's heating checks: two rounds district by district, each owner taking or declining a round's
    # check for all its buildings
    w.district = rng.integers(0, N_DISTRICTS, N)
    rv = np.random.default_rng(seed + 67)
    w.visit_plan = []
    for plan in VISIT_ROUNDS:
        order = list(rv.permutation(N_DISTRICTS))
        dsn = {}
        for s_, n_ in plan.items():
            for _ in range(n_):
                dsn[int(order.pop(0))] = s_
        w.visit_plan.append(dsn)
    w.accept = [(rv.random(n_own) < VISIT_ACCEPT[r])[w.owner] for r in range(len(VISIT_ROUNDS))]
    w.visit_day = rv.random((N, len(VISIT_ROUNDS)))
    w.visits = [[] for _ in range(N)]
    w.visit_round = [[] for _ in range(N)]
    w.burner = np.clip(rv.normal(BURNER_MEAN, BURNER_SD, N), 0.0, BURNER_MAX)
    lvl = np.array([TYPE_LEVEL[TYPES[t]] for t in w.typ])
    w.base = lvl * area0 * np.exp(w.level)
    h_type = np.array([HW_SHARE[TYPES[t]] for t in w.typ])
    # each building's heating curve and what each measure would cut in it (used only if its works are done)
    rng_e = np.random.default_rng(seed + 3)
    noise = {m: np.exp(rng_e.normal(-0.5 * EFFECT_SD ** 2, EFFECT_SD, N)) for m in MEASURES}
    noise["heating controls"] = noise["heating controls"] ** (CTRL_BUILDING_SD / EFFECT_SD)
    w.curve_c = np.array([CURVE[t] for t in tname]) * np.exp(rng_e.normal(-0.5 * CURVE_SD ** 2, CURVE_SD, N))
    w.balance = BALANCE * np.exp(rng_e.normal(-0.5 * BALANCE_SD ** 2, BALANCE_SD, N))
    kb = rng_e.normal(KEEP_BAL, KEEP_BAL_OWNER, n_own)
    w.keep_bal = np.clip(kb[w.owner] + rng_e.normal(0, KEEP_BAL_SD, N), 0.05, 0.90)
    kc = rng_e.normal(KEEP_CTRL, KEEP_CTRL_OWNER, n_own)
    w.keep_ctrl = np.clip(kc[w.owner] + rng_e.normal(0, KEEP_CTRL_SD, N), 0.30, 1.0)
    u_ctrl = rng_e.normal(-0.5 * CTRL_OWNER_SD ** 2, CTRL_OWNER_SD, n_own)
    u_single = rng_e.normal(-0.5 * CTRL_SINGLE_SD ** 2, CTRL_SINGLE_SD, N)
    u_ins = rng_e.normal(-0.5 * INS_OWNER_SD ** 2, INS_OWNER_SD, n_own)
    w.cut = {"insulation": INS_C * w.roof_ratio ** INS_X * noise["insulation"]
                           * np.exp(np.where(w.portfolio, u_ins[w.owner], 0.0)),
             "heating optimisation": w.balance,
             "heating controls": np.where(w.lived_in, CTRL_LIVED, CTRL_C * np.clip(w.empty - CTRL_E0, 0.0, None)
                                          + CTRL_LIVED) * noise["heating controls"]
                                 * np.exp(np.where(w.portfolio, u_ctrl[w.owner], u_single))}
    w.normal = np.zeros((N, K))                # the building's own normal-weather use (kWh)
    w.underlying = np.zeros((N, K))            # use before any works or check, in the season's own state (kWh)
    w.actual = np.zeros((N, K))                # metered use in the season's weather (kWh)
    w.flag = np.zeros((N, K), bool)
    w.offer = np.zeros((N, K), bool)
    w.applied = np.zeros((N, K), bool)        # answered the pilot offer (2019) or applied (2026)
    w.drawn = np.zeros(N, bool)                # given a pilot place by the draw
    w.withdrawn = np.zeros(N, bool)
    w.works = np.zeros(N, bool)                # pilot works done in summer 2019
    w.done_date = [None] * N                   # the day the works were completed (July to September 2019)
    w.measure = np.array([""] * N, dtype=object)  # the measure a pilot answer asked for
    w.measure26 = np.array([""] * N, dtype=object)  # the measure a 2026 application asks for
    w.norm_intensity = np.full((N, K), np.nan)
    w.f_hw = np.ones((N, K))
    w.f_heat = np.ones((N, K))
    w.answer_date = {PILOT: [None] * N, PIPELINE: [None] * N}
    mi19 = pick_by_owner(w, MEASURE_P_2019, PICK[2019], np.random.default_rng(seed + 37))
    for k, s in enumerate(SEASONS):
        live = (w.first <= s) & (w.last >= s)
        ds = w.days[s]
        heat = np.where(w.temp[s] < 15.0, 20.0 - w.temp[s], 0.0)
        if s >= TUNE_START:
            for r, plan in enumerate(w.visit_plan):
                first_season = min(plan.values())
                months = (8, 9, 10, 11) if s == first_season and s == TUNE_START else (9, 10, 11, 12, 1, 2, 3)
                window = [j for j, d in enumerate(ds) if d.month in months]
                for i in np.where(live & w.accept[r])[0]:
                    if plan.get(int(w.district[i])) != s:
                        continue
                    j = window[min(len(window) - 1, int(w.visit_day[i, r] * len(window)))]
                    w.visits[i].append(ds[j])
                    w.visit_round[i].append(r)
        for i in np.where(live)[0]:
            if w.visits[i] or w.works[i]:
                hw_d, ht_d = day_mults(w, int(i), s)
                w.f_hw[i, k] = float(hw_d.mean())
                w.f_heat[i, k] = float((heat * ht_d).sum() / heat.sum())
        shock = np.array([COVID.get(s, {}).get(t, 0.0) for t in tname]) + CRISIS.get(s, 0.0)
        ratio = w.G[s] / w.G_LT
        w.underlying[:, k] = np.where(live, w.base * w.change[:, k] * np.exp(slow[:, k] + fast[:, k]) * (1 - shock), 0.0)
        w.actual[:, k] = w.underlying[:, k] * (w.hw * w.f_hw[:, k] + (1 - w.hw) * ratio * w.f_heat[:, k])
        w.normal[:, k] = w.actual[:, k] / (w.hw + (1 - w.hw) * ratio)
        if s >= PILOT:
            nrm = w.actual[:, k] * (h_type + (1 - h_type) / ratio) / w.area[:, k]
            nrm = np.where(live, nrm, np.nan)
            w.norm_intensity[:, k] = nrm
            for t in range(len(TYPES)):
                m_ = (w.typ == t) & live & (w.first <= s - 1)
                cut = np.quantile(nrm[m_], 0.80)
                w.flag[m_, k] = nrm[m_] > cut
            if s == PILOT:
                w.offer[:, k] = w.flag[:, k]
                ans = w.offer[:, k] & (rng.random(n_own) < INTEREST_P)[w.owner]
                w.applied[:, k] = ans
                idx = np.where(ans)[0]
                for i in idx:
                    w.measure[i] = MEASURES[mi19[i]]
                answer_dates(w, PILOT, seed + ANSWER_SEED_OFFSET)
                # the places drawn by lot among the owners who answered, within each measure, an owner's buildings
                # together, until each measure's places (its share of the answers) are filled
                rd = np.random.default_rng(seed + DRAW_SEED_OFFSET)
                for m in MEASURES:
                    im = [int(i) for i in idx if w.measure[i] == m]
                    by_owner = {}
                    for i in im:
                        by_owner.setdefault(int(w.owner[i]), []).append(i)
                    owners_m = sorted(by_owner)
                    places = int(round(PLACES * len(im)))
                    got = 0
                    for oi in rd.permutation(len(owners_m)):
                        if got >= places:
                            break
                        b_ = by_owner[owners_m[int(oi)]]
                        w.drawn[b_] = True
                        got += len(b_)
                rw = np.random.default_rng(seed + 5)
                day0 = dt.date(PILOT, *NOTICE_MD)
                for i in np.where(w.drawn)[0]:
                    m = w.measure[i]
                    dday = (w.answer_date[PILOT][i] - day0).days
                    p = WITHDRAW[m] * math.exp(WITHDRAW_SIZE * w.size_z[i] + WITHDRAW_DAY * (dday - 23))
                    w.withdrawn[i] = rw.random() < min(0.6, p)
                w.works = w.drawn & ~w.withdrawn
                # each answer's quote names its contractor; the drawn jobs are done firm by firm in the order the
                # owners answered
                firms(w, seed)
                rf = np.random.default_rng(seed + FIRM_SEED_OFFSET + 1)
                w.firm = {PILOT: {}, PIPELINE: {}}
                for i in idx:
                    w.firm[PILOT][int(i)] = choose_firm(w, rf, w.measure[i], PILOT)
                jobs = [(int(i), w.measure[i], w.firm[PILOT][int(i)], w.answer_date[PILOT][i], job_size(w, i, w.measure[i], k))
                        for i in np.where(w.works)[0]]
                done = schedule(w, jobs, PILOT)
                for i in np.where(w.works)[0]:
                    w.done_date[i] = done[int(i)]
            elif s == PIPELINE:
                w.offer[:, k] = w.flag[:, k] & ~w.works
                take = w.offer[:, k] & (rng.random(n_own) < APPLY_2026)[w.owner]
                w.applied[:, k] = take
                mi26 = pick_by_owner(w, MEASURE_P_2026, PICK[2026], np.random.default_rng(seed + 41), report=True)
                for i in np.where(take)[0]:
                    w.measure26[i] = MEASURES[mi26[i]]
                answer_dates(w, PIPELINE, seed + ANSWER_SEED_OFFSET + 1)
    w.cost = {PILOT: np.zeros(N), PIPELINE: np.zeros(N)}
    w.grant = {PILOT: np.zeros(N), PIPELINE: np.zeros(N)}
    rq = np.random.default_rng(seed + 11)
    for s, meas in ((PILOT, w.measure), (PIPELINE, w.measure26)):
        k = SI[s]
        for i in np.where(w.applied[:, k])[0]:
            m = meas[i]
            per = w.roof_ratio[i] if m == "insulation" else 1.0       # roof insulation is quoted on the roof
            c = COST_M2[m] * per * w.area[i, k] * math.exp(rq.normal(0, COST_SD))
            c = round(c / 10.0) * 10.0
            w.cost[s][i] = c
            w.grant[s][i] = min(GRANT_CAP, round(GRANT_SHARE * c / 10.0) * 10.0)
    # a 2026 applicant who revises the quote sends a second application a few days later; the later one stands
    kp = SI[PIPELINE]
    w.resubmit = {}
    rr = np.random.default_rng(seed + 13)
    close = dt.date(PIPELINE, *CLOSE_MD)
    for i in np.where(w.applied[:, kp])[0]:
        if rr.random() < RESUBMIT_P:
            d2 = w.answer_date[PIPELINE][i] + dt.timedelta(days=int(rr.integers(3, 13)))
            if d2 <= close:
                first_cost = round(w.cost[PIPELINE][i] * math.exp(rr.normal(-0.06, 0.08)) / 10.0) * 10.0
                w.resubmit[int(i)] = (d2, first_cost, min(GRANT_CAP, round(GRANT_SHARE * first_cost / 10.0) * 10.0))
    w.received26 = np.array([bool(w.applied[i, kp]) and w.answer_date[PIPELINE][i] <= RECEIVED_TO for i in range(N)])
    # the 2026 applications that will be withdrawn after the round is set (the world's own outcome, never shipped)
    rw2 = np.random.default_rng(seed + 17)
    day0 = dt.date(PIPELINE, *NOTICE_MD)
    w.withdraw26 = np.zeros(N, bool)
    for i in np.where(w.applied[:, kp])[0]:
        m = w.measure26[i]
        dday = (w.answer_date[PIPELINE][i] - day0).days
        p = WITHDRAW[m] * math.exp(WITHDRAW_SIZE * w.size_z[i] + WITHDRAW_DAY * (dday - 23))
        w.withdraw26[i] = rw2.random() < min(0.6, p)
    # the 2026 quotes come from the firms still taking council work; the round the committee sets (insulation and
    # heating controls) is done firm by firm from 13 July, and a job not finished by 30 September is not paid (the
    # world's own outcome, never shipped)
    rf = np.random.default_rng(seed + FIRM_SEED_OFFSET + 2)
    for i in np.where(w.applied[:, kp])[0]:
        w.firm[PIPELINE][int(i)] = choose_firm(w, rf, w.measure26[i], PIPELINE)
    jobs = [(int(i), w.measure26[i], w.firm[PIPELINE][int(i)], w.answer_date[PIPELINE][i],
             job_size(w, i, w.measure26[i], kp))
            for i in np.where(w.applied[:, kp] & ~w.withdraw26)[0] if w.measure26[i] in ("insulation", "heating controls")]
    w.done26 = schedule(w, jobs, PIPELINE)
    return w


def workdays(d0, n):
    """the first n working days (Monday to Friday) from d0 on"""
    out, d = [], d0
    while len(out) < n:
        if d.weekday() < 5:
            out.append(d)
        d += dt.timedelta(days=1)
    return out


def firms(w, seed):
    """the roofers and heating firms: each roofer's pace in square metres of roof a working day, each heating firm's
    fitters, and which of them still take council work in 2026"""
    rng = np.random.default_rng(seed + FIRM_SEED_OFFSET)
    w.roofers = [{"name": n, "pace": float(ROOF_PACE[0] * math.exp(rng.normal(0, ROOF_PACE[1])))} for n in ROOFERS]
    w.heating = [{"name": n, "fitters": int(rng.choice(FITTERS[0], p=FITTERS[1]))} for n in HEATING_FIRMS]
    w.trading = {"insulation": sorted(rng.permutation(len(ROOFERS))[:STILL_TRADING["roofers"]].tolist()),
                 "heating": sorted(rng.permutation(len(HEATING_FIRMS))[:STILL_TRADING["heating"]].tolist())}


def choose_firm(w, rng, m, year):
    """the firm an owner's quote comes from: a roofer for insulation, a heating firm otherwise, the larger firms (a
    roofer's pace, a heating firm's fitters) more often"""
    if m == "insulation":
        idx = list(range(len(ROOFERS))) if year == PILOT else w.trading["insulation"]
        wts = np.array([w.roofers[j]["pace"] for j in idx])
    else:
        idx = list(range(len(HEATING_FIRMS))) if year == PILOT else w.trading["heating"]
        wts = np.array([w.heating[j]["fitters"] for j in idx], float)
    return int(idx[int(rng.choice(len(idx), p=wts / wts.sum()))])


def job_size(w, i, m, k):
    """a job's size: insulation the building's roof in square metres, heating optimisation and controls the fitter's
    days (a balancing two to five days by the floor area, controls one or two)"""
    if m == "insulation":
        return float(w.roof_ratio[i] * w.area[i, k])
    if m == "heating optimisation":
        return int(min(5, max(2, round(1.5 + w.area[i, k] / 1000.0))))
    return 1 if w.area[i, k] < 2500.0 else 2


def schedule(w, jobs, year):
    """the day each job is done: jobs are (i, measure, firm, answer date, size); each firm takes its jobs in the order
    its owners answered, a roofer insulating at its pace in square metres a working day, a heating firm giving each job
    to its first free fitter; a job is done on the working day its last square metre or day falls"""
    days = workdays(WORK_FROM[year], 400)
    done = {}
    by_firm = {}
    for j in jobs:
        by_firm.setdefault((j[1] == "insulation", j[2]), []).append(j)
    rain = np.random.default_rng(w.seed + FIRM_SEED_OFFSET + 20 + year).random(len(days)) < RAIN_P
    r_lag = np.random.default_rng(w.seed + FIRM_SEED_OFFSET + 30 + year)
    r_job = np.random.default_rng(w.seed + FIRM_SEED_OFFSET + 40 + year)
    for (roof, f), js in sorted(by_firm.items()):
        js.sort(key=lambda j: (j[3], j[0]))
        if roof:
            pace = w.roofers[f]["pace"]
            k = int(r_lag.choice(START_LAG))      # the firm's first working day on the round's roofs
            got = 0.0                             # square metres insulated so far
            need = 0.0
            for i, _m, _f, _d, size in js:
                need += size * math.exp(r_job.normal(0.0, ROOF_SD))
                while got < need - 1e-9:
                    if not rain[k]:
                        got += pace
                    k += 1
                done[i] = days[k - 1]
        else:
            free = [0] * w.heating[f]["fitters"]
            for i, _m, _f, _d, size in js:
                k = int(np.argmin(free))
                free[k] += size
                done[i] = days[free[k] - 1]
    return done


def pick_by_owner(w, shares, pick, rng, report=False):
    """the measure each owner would name if it answered, for all its buildings at once: its use's shares, leaning
    towards controls the longer its buildings stand empty and towards insulation the more roof they have per floor, by
    the strength in pick (each use's shares kept on average over its buildings); with report, an owner whose buildings
    had a check from the 2024/25 winter on leans towards heating optimisation as the check report recommends"""
    out = np.zeros(w.N, int)
    members = {}
    for i in range(w.N):
        members.setdefault(int(w.owner[i]), []).append(i)
    lr = np.log(w.roof_ratio)
    for t in range(len(TYPES)):
        idx = np.where(w.typ == t)[0]
        p = np.array(shares[TYPES[t]])
        e_mean, r_mean = w.empty[idx].mean(), lr[idx].mean()
        owners_t = sorted({int(w.owner[i]) for i in idx})
        e_o = np.array([w.empty[members[o]].mean() for o in owners_t])
        r_o = np.array([lr[members[o]].mean() for o in owners_t])
        n_o = np.array([len(members[o]) for o in owners_t], float)
        zc = np.exp(pick["heating controls"] * (e_o - e_mean))
        pc = np.clip(p[2] * zc / np.average(zc, weights=n_o), 0.0, 0.95)
        zi = np.exp(pick["insulation"] * (r_o - r_mean))
        pi = np.minimum(np.clip(p[0] * zi / np.average(zi, weights=n_o), 0.0, 0.95), 0.97 - pc)
        po = 1.0 - pc - pi
        if report:
            rec = np.array([np.mean([any(season_of(d) >= REPORT_FROM and r >= CURVE_ROUND for d, r in zip(w.visits[i], w.visit_round[i])) for i in members[o]])
                            for o in owners_t])
            po_new = np.clip(po * (1.0 + (REPORT_PICK - 1.0) * rec), 0.0, None)
            po_new = po_new * np.average(po, weights=n_o) / np.average(po_new, weights=n_o)
            po_new = np.minimum(po_new, 1.0 - 1e-6)
            rest = pc + pi
            scale = np.where(rest > 0, (1.0 - po_new) / np.where(rest > 0, rest, 1.0), 0.0)
            pc, pi, po = pc * scale, pi * scale, po_new
        pp = np.column_stack([pi, po, pc])
        u = rng.random(len(owners_t))
        pick_o = (u[:, None] > np.cumsum(pp, 1)).sum(1)
        for o, m in zip(owners_t, pick_o):
            out[members[o]] = min(int(m), 2)
    return out


def curve_state(w, i, days):
    """the share of the building's curve excess wasted on each day (1 untouched): the pilot's heating optimisation sets
    it to nothing and a campaign check to CHECK_LEAVES of what it had crept back to; from each reset it creeps back
    towards all of it in a building never balanced (TAU_UNBAL) or towards what a balanced building lets go (1 less its
    kept share, TAU_BAL)"""
    opt = bool(w.works[i] and w.measure[i] == "heating optimisation")
    ev = ([(w.done_date[i], "works")] if opt else []) + \
         [(d, "check") for d, r in zip(w.visits[i], w.visit_round[i]) if r >= CURVE_ROUND]
    s = np.ones(len(days))
    if not ev:
        return s
    ev.sort()
    dn = np.array([d.toordinal() for d in days], float)
    t0, s0, bal = None, 1.0, False
    out = np.ones(len(days))
    for d, kind in ev + [(None, None)]:
        upto = d.toordinal() if d is not None else 10 ** 9
        if t0 is not None:
            target = 1.0 - w.keep_bal[i] if bal else 1.0
            tau = TAU_BAL if bal else TAU_UNBAL
            seg = (dn >= t0) & (dn < upto)
            out[seg] = target - (target - s0) * np.exp(-(dn[seg] - t0) / 365.25 / tau)
        if d is None:
            break
        if t0 is not None:
            target = 1.0 - w.keep_bal[i] if bal else 1.0
            tau = TAU_BAL if bal else TAU_UNBAL
            before = target - (target - s0) * math.exp(-(upto - t0) / 365.25 / tau)
        else:
            before = 1.0
        if kind == "works":
            bal, s0 = True, 0.0
        else:
            s0 = CHECK_LEAVES * before
        t0 = float(upto)
    return out


def day_mults(w, i, s):
    """building i's day-by-day factors in season s on its hot water and on its heating: the burner tuned at its first
    check, the heating curve as it stands, and its pilot works' cut from the day they were done"""
    ds = w.days[s]
    nd = len(ds)
    hw = np.ones(nd)
    ht = np.ones(nd)
    if w.visits[i]:
        v0 = w.visits[i][0]
        on = np.array([d >= v0 for d in ds])
        hw = np.where(on, 1.0 - w.burner[i], 1.0)
        ht = ht * hw
    ht = ht * (1.0 - w.curve_c[i] * (1.0 - curve_state(w, i, ds)))
    if w.works[i]:
        m = w.measure[i]
        after = np.array([d >= w.done_date[i] for d in ds])
        age = s - PILOT
        if m == "heating controls":
            e = w.cut[m][i] * keep_curve(w.keep_ctrl[i], TAU_CTRL, age)
        else:
            e = w.cut[m][i]
        ht = ht * np.where(after, 1.0 - e, 1.0)
    return hw, ht


def load_week(w, i, seed):
    """building i's electricity in 2025 as Stadtwerke Haldenau Netz's meter data averages it: the mean load (kW) in
    each hour of each weekday, Monday first (7 x 24); a base load that never stops (with outdoor lighting through the
    night at some shops and workshops), a load while the building is in use shaped through the day, the hour before
    opening and the hour after closing partly lit, a few staff on some Saturdays at buildings that close for the
    weekend, and public holidays on the weekdays they fell"""
    rng = np.random.default_rng(seed + 7919 * i)
    t = TYPES[w.typ[i]]
    a = w.area[i, SI[PIPELINE]]
    base = a * ELEC_BASE[t] / 1000.0 * math.exp(rng.normal(0, 0.30))
    use = a * ELEC_USE[t] / 1000.0 * math.exp(rng.normal(0, 0.30))
    lean = float(rng.uniform(0.5, 1.0))
    shape = np.ones(24)
    for h, v in DAY_SHAPE.get(t, {}).items():
        shape[h] = 1.0 + lean * (v - 1.0)
    occ = np.zeros((7, 24))
    if w.lived_in[i]:
        act = np.array(ACTIVITY[t]) * np.exp(rng.normal(0, 0.05, 24))
        occ[:] = np.clip(act, 0.2, 1.1)[None, :]
    elif w.len_h[i] >= 24.0:
        for d in range(7):
            if w.days_open[i, d]:
                occ[d] = 0.92 * np.where(np.arange(24) < 6, 0.88, 1.0) + rng.normal(0, 0.02, 24)
    else:
        o, c = w.open_h[i], w.open_h[i] + w.len_h[i]
        after = 0.35 if t == "restaurant" else 0.22
        for d in range(7):
            if not w.days_open[i, d]:
                continue
            day = float(rng.normal(1.0, 0.03))
            for h in range(24):
                ov = max(0.0, min(h + 1.0, c) - max(float(h), o))
                if ov <= 0.0:
                    if o - 1.0 <= h < o:
                        ov = 0.30
                    elif c <= h < c + 1.0:
                        ov = after
                    occ[d, h] = ov
                else:
                    occ[d, h] = ov * shape[h] * day
        if t in ("office", "workshop") and not w.days_open[i, 5] and rng.random() < 0.20:
            for h in range(9, 13):
                occ[5, h] = float(rng.uniform(0.10, 0.22))
    for d in range(7):
        occ[d] *= 1.0 - HOLIDAYS_2025[d] / float(WEEKDAYS_2025[d]) if not w.lived_in[i] else 1.0
    night = np.zeros(24)
    if t in ("retail", "workshop") and rng.random() < 0.40:
        night[np.r_[0:6, 18:24]] = 0.06 * use
    kw = (base + night[None, :]) * (1.0 + 0.03 * rng.normal(0, 1, (7, 24))) + \
        use * occ * (1.0 + 0.03 * rng.normal(0, 1, (7, 24)))
    return np.round(np.clip(kw, 0.1, None), 1)


def answer_dates(w, s, seed):
    """the day each answer or application of round s came in"""
    rng3 = np.random.default_rng(seed)
    k = SI[s]
    meas = w.measure if s == PILOT else w.measure26
    notice = dt.date(s, *NOTICE_MD)
    span = (dt.date(s, *CLOSE_MD) - notice).days
    for i in np.where(w.applied[:, k])[0]:
        u = rng3.random()
        e, mid, lt = ANSWER_WAVES[meas[i]]
        z = w.size_z[i]
        lt_i = min(0.92, max(0.05, lt + LATE_SIZE[meas[i]] * z))
        e_i = max(0.03, 1.0 - mid - lt_i)
        if u < e_i:
            day = 1 + int(14 * rng3.beta(1.2, 2.2))
        elif u < e_i + mid:
            day = 1 + int(span * rng3.random())
        else:
            day = span - int(10 * rng3.beta(1.0, 2.0))
        d = notice + dt.timedelta(days=min(span, max(1, day)))
        if d.weekday() >= 5:
            # the 2019 responses came by post and e-mail and were logged on working days; the 2026 portal takes
            # applications every day, though most owners send theirs on a working day
            if not (s == PIPELINE and (int(i) * 2654435761) % 1000 < 350):
                d2 = d + dt.timedelta(days=7 - d.weekday())
                d = d2 if d2 <= dt.date(s, *CLOSE_MD) else d - dt.timedelta(days=d.weekday() - 4)
        w.answer_date[s][i] = d


def daily_kwh(w, i, s):
    """building i's metered gas use, day by day, in season s (kWh): its use spread over the days (hot water) and the
    season's degree days (heating), with the burner, the heating curve and the works as they stood each day"""
    k = SI[s]
    ds = w.days[s]
    heat = np.where(w.temp[s] < 15.0, 20.0 - w.temp[s], 0.0)
    nd = float(len(ds))
    hwv = np.full(len(ds), w.hw[i] / nd)
    htv = (1 - w.hw[i]) * heat / w.G_LT
    if w.visits[i] or w.works[i]:
        hw_d, ht_d = day_mults(w, i, s)
        hwv = hwv * hw_d
        htv = htv * ht_d
    return w.underlying[i, k] * (hwv + htv)


if __name__ == "__main__":
    w = build()
    print("G_LT", w.G_LT, {s: round(w.G[s]) for s in SEASONS})
    k = SI[PILOT]
    print("pilot: offered", int(w.offer[:, k].sum()), "answered", int(w.applied[:, k].sum()), "drawn",
          int(w.drawn.sum()), "withdrawn", int(w.withdrawn.sum()), "works", int(w.works.sum()))
    k = SI[PIPELINE]
    print("2026: offered", int(w.offer[:, k].sum()), "applied", int(w.applied[:, k].sum()), "received by 12 June",
          int(w.received26.sum()), "resubmitted", len(w.resubmit))
    for m in MEASURES:
        print(m, "works", int((w.works & (w.measure == m)).sum()), "applied 2026", int((w.applied[:, k] & (w.measure26 == m)).sum()))
