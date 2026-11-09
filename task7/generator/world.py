"""task7 architecture 7: Stadtwerke Haldenau's commercial gas customers, the council's 2019 retrofit pilot and the
2026 round, season by season from 2013/14 to 2025/26.

A season runs from 1 May to 30 April and is named by the year it ends (season 2019 is May 2018 to April 2019). Each
building's gas use in a season of long-term average weather is its type's level times its floor area times its own
level, a slow part that drifts and fades by a tenth a season (a tenant's hours, a plant room run hard) and a fast part
that comes and goes within the season. The actual use spreads the building's hot-water share evenly over the days and
the rest over the season's degree days. Buildings change as buildings do: an extension or a roof storey adds heated
floor area from the season after it is finished, and a floor stands empty for a season or three before it is let again.

Every May the utility's benchmarking notice goes to the buildings whose normalised use per square metre is in the top
fifth of their type. The May 2019 notice carried the council's pilot offer; the owners who answered it, each naming one
measure, were drawn by lot for the pilot's places, and the drawn buildings had their works that summer. What a measure's
works save depends on the building: insulation cuts the heat a building loses, so it saves a share of the heating and
none of the hot water; heating optimisation balances the system and lowers its heating curve, and caretakers turn the
curve back up after complaints over the winters that follow, by building, until a part of the saving that stays is
left; heating controls save by setting the heating back when a building is empty, so they save most in offices,
workshops and shops and almost nothing in a care home or a hotel heated round the clock. Which measure an owner asks for
depends on the building's use, and the 2026 applicants are not the pilot's: the pilot's controls answers came heavily
from care homes and hotels, the 2026 ones mostly from offices, shops and workshops.

An answer or an application comes with a contractor's quote. A quote for insulation needs a survey of the roof or walls,
longer on a larger building, so insulation answers come late in the offer's six weeks and the large ones latest; a
drawn owner can still withdraw, likelier on a large job and on an answer sent close to the deadline. The pandemic
winters and the 2022 gas price shock moved every building's use. From August 2019 the utility's service team offered
its commercial customers a burner check district by district, free of charge, whatever their place in the pilot; most
owners accepted, and a checked burner burns less gas for the same heat from the visit on, by however far out of tune it
was. The May 2026 notice carries the offer of the 2026 round, open to 30 June; the applications received by 12 June are
what the utility holds when the climate committee decides the round, and an owner who revises a quote sends the
application again."""
import datetime as dt
import math

import numpy as np

SEED = 70707
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
# the cut a measure's works make in the heating part of a building's use (the hot-water part is untouched), as the type's
# mean in the first season after the works; each building's own cut spreads around it
EFFECT = {"insulation": {"office": 0.212, "retail": 0.200, "hotel": 0.188, "workshop": 0.150, "care home": 0.190,
                         "restaurant": 0.176},
          "heating optimisation": {"office": 0.158, "retail": 0.138, "hotel": 0.170, "workshop": 0.135,
                                   "care home": 0.178, "restaurant": 0.150},
          "heating controls": {"office": 0.125, "retail": 0.098, "hotel": 0.010, "workshop": 0.094,
                               "care home": 0.006, "restaurant": 0.066}}
EFFECT_SD = 0.26                           # log spread of a building's own cut around its type's
# how much of the first season's cut a building keeps once its caretakers have turned the heating curve back up
# (heating optimisation) or overridden the timers (controls), and how fast it falls there; insulation keeps it all
KEEP = {"heating optimisation": (0.05, 0.04, 1.0), "heating controls": (0.80, 0.07, 2.0)}
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
# the service team's burner checks: districts in a fixed order from August 2019 to March 2026, most of them in the
# first two winters, every commercial gas customer offered a visit; a checked burner's cut, by how far out of tune it was
N_DISTRICTS = 42
DISTRICTS_PER_SEASON = {2020: 16, 2021: 10, 2022: 6, 2023: 4, 2024: 3, 2025: 2, 2026: 1}
TUNE_START = 2020
TUNE_ACCEPT = 0.70
TUNE_MEAN, TUNE_SD, TUNE_MAX = 0.034, 0.022, 0.10
# buildings change: an extension adds heated floor area from the next season, the new space using about half the gas
# a square metre of the old does; a floor stands empty for one to three seasons and is let again
EXTEND_P, EXTEND_GAIN = 0.0055, 0.55
VACANT_P = 0.0045
# the pandemic winters and the gas price shock: every building's cut by type in those seasons
COVID = {2020: {"office": 0.02, "retail": 0.03, "hotel": 0.06, "workshop": 0.01, "care home": 0.0, "restaurant": 0.07},
         2021: {"office": 0.08, "retail": 0.07, "hotel": 0.22, "workshop": 0.03, "care home": 0.0, "restaurant": 0.25},
         2022: {"office": 0.05, "retail": 0.03, "hotel": 0.08, "workshop": 0.01, "care home": 0.0, "restaurant": 0.08}}
CRISIS = {2022: 0.020, 2023: 0.140, 2024: 0.110, 2025: 0.090, 2026: 0.072}
# quoted cost per square metre of heated floor area (median, euro) and the grant terms
COST_M2 = {"insulation": 54.5, "heating optimisation": 7.4, "heating controls": 8.2}
COST_SD = 0.22
GRANT_SHARE, GRANT_CAP = 0.30, 40000.0

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
    w.level = rng.normal(0, SD_LEVEL, N)
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
    # the service team's burner checks
    w.district = rng.integers(0, N_DISTRICTS, N)
    order = list(rng.permutation(N_DISTRICTS))
    w.district_season = {}
    for s_, n_ in DISTRICTS_PER_SEASON.items():
        for _ in range(n_):
            w.district_season[int(order.pop(0))] = s_
    w.accept = rng.random(N) < TUNE_ACCEPT
    w.tune_day = rng.random(N)
    w.tune_cut = np.clip(rng.normal(TUNE_MEAN, TUNE_SD, N), 0.0, TUNE_MAX)
    w.tune_date = [None] * N
    lvl = np.array([TYPE_LEVEL[TYPES[t]] for t in w.typ])
    w.base = lvl * area0 * np.exp(w.level)
    h_type = np.array([HW_SHARE[TYPES[t]] for t in w.typ])
    # each building's own cut for each measure (drawn once, used only if its works are done) and how much it keeps
    rng_e = np.random.default_rng(seed + 3)
    w.cut = {m: np.array([EFFECT[m][t] for t in tname]) * np.exp(rng_e.normal(-0.5 * EFFECT_SD ** 2, EFFECT_SD, N))
             for m in MEASURES}
    w.keep_f = {m: np.ones(N) for m in MEASURES}
    for m, (fm, fs, tau) in KEEP.items():
        w.keep_f[m] = np.clip(rng_e.normal(fm, fs, N), 0.0, 1.0)
    mi19 = np.array([rng.choice(3, p=MEASURE_P_2019[TYPES[t]]) for t in w.typ])
    mi26 = np.array([rng.choice(3, p=MEASURE_P_2026[TYPES[t]]) for t in w.typ])
    w.normal = np.zeros((N, K))                # the building's own normal-weather use (kWh)
    w.underlying = np.zeros((N, K))            # use before any works or visit, in the season's own state (kWh)
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
    w.heat_factor = np.ones((N, K))            # the works' factor on the heating part in each season
    tuned = np.zeros(N, bool)
    rng2 = np.random.default_rng(seed + 1)
    w.answer_date = {PILOT: [None] * N, PIPELINE: [None] * N}
    for k, s in enumerate(SEASONS):
        live = (w.first <= s) & (w.last >= s)
        ds = w.days[s]
        heat = np.where(w.temp[s] < 15.0, 20.0 - w.temp[s], 0.0)
        nd = float(len(ds))
        f_hw = np.ones(N)
        f_heat = np.ones(N)

        def step(i, j, e, hot_water):
            """a cut of e from day j of the season on, on the days (hot water) and the degree days (heating)"""
            if hot_water:
                f_hw[i] *= 1.0 - e * (nd - j) / nd
            f_heat[i] *= 1.0 - e * heat[j:].sum() / heat.sum()
        if s >= TUNE_START:
            months = (8, 9, 10, 11) if s == TUNE_START else (9, 10, 11, 12, 1, 2, 3)
            window = [i for i, d in enumerate(ds) if d.month in months]
            for i in np.where(live & ~tuned & w.accept)[0]:
                if w.district_season[int(w.district[i])] != s:
                    continue
                j = window[min(len(window) - 1, int(w.tune_day[i] * len(window)))]
                w.tune_date[i] = ds[j]
                step(i, j, w.tune_cut[i], True)
                tuned[i] = True
        for i in np.where(tuned)[0]:
            if w.tune_date[i] is not None and season_of(w.tune_date[i]) < s:
                f_hw[i] *= 1.0 - w.tune_cut[i]
                f_heat[i] *= 1.0 - w.tune_cut[i]
        for i in np.where(w.works)[0]:
            m = w.measure[i]
            age = s - PILOT
            e = w.cut[m][i] * (keep_curve(w.keep_f[m][i], KEEP[m][2], age) if m in KEEP else 1.0)
            if s == PILOT + 1:
                step(i, ds.index(w.done_date[i]), e, False)
            elif s > PILOT + 1:
                f_heat[i] *= 1.0 - e
            w.heat_factor[i, k] = 1.0 - e
        shock = np.array([COVID.get(s, {}).get(t, 0.0) for t in tname]) + CRISIS.get(s, 0.0)
        ratio = w.G[s] / w.G_LT
        w.underlying[:, k] = np.where(live, w.base * w.change[:, k] * np.exp(slow[:, k] + fast[:, k]) * (1 - shock), 0.0)
        w.actual[:, k] = w.underlying[:, k] * (w.hw * f_hw + (1 - w.hw) * ratio * f_heat)
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
                ans = w.offer[:, k] & (rng.random(N) < INTEREST_P)
                w.applied[:, k] = ans
                idx = np.where(ans)[0]
                for i in idx:
                    w.measure[i] = MEASURES[mi19[i]]
                answer_dates(w, PILOT, seed + ANSWER_SEED_OFFSET)
                # the places drawn by lot within each measure, so each measure's share of places matches its answers
                rd = np.random.default_rng(seed + DRAW_SEED_OFFSET)
                for m in MEASURES:
                    im = np.array([i for i in idx if w.measure[i] == m])
                    pick = rd.permutation(len(im))[:int(round(PLACES * len(im)))]
                    w.drawn[im[pick]] = True
                rw = np.random.default_rng(seed + 5)
                day0 = dt.date(PILOT, *NOTICE_MD)
                for i in np.where(w.drawn)[0]:
                    m = w.measure[i]
                    dday = (w.answer_date[PILOT][i] - day0).days
                    p = WITHDRAW[m] * math.exp(WITHDRAW_SIZE * w.size_z[i] + WITHDRAW_DAY * (dday - 23))
                    w.withdrawn[i] = rw.random() < min(0.6, p)
                w.works = w.drawn & ~w.withdrawn
                summer = [d for d in season_days(PILOT + 1) if dt.date(2019, 7, 15) <= d <= dt.date(2019, 9, 30)]
                for i in np.where(w.works)[0]:
                    w.done_date[i] = summer[int(rng2.integers(0, len(summer)))]
            elif s == PIPELINE:
                w.offer[:, k] = w.flag[:, k] & ~w.works
                take = w.offer[:, k] & (rng.random(N) < APPLY_2026)
                w.applied[:, k] = take
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
            c = COST_M2[m] * w.area[i, k] * math.exp(rq.normal(0, COST_SD))
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
    return w


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
        w.answer_date[s][i] = notice + dt.timedelta(days=min(span, max(1, day)))


def daily_kwh(w, i, s):
    """building i's metered gas use, day by day, in season s (kWh): its use spread over the days (hot water) and the
    season's degree days (heating), with the works' cut on the heating from the day they were done and the burner
    check's cut on both from the day of the visit"""
    k = SI[s]
    ds = w.days[s]
    heat = np.where(w.temp[s] < 15.0, 20.0 - w.temp[s], 0.0)
    nd = float(len(ds))
    hwv = np.full(len(ds), w.hw[i] / nd)
    htv = (1 - w.hw[i]) * heat / w.G_LT
    if w.works[i]:
        e = 1.0 - w.heat_factor[i, k]
        if s == PILOT + 1:
            htv[ds.index(w.done_date[i]):] *= 1 - e
        elif s > PILOT + 1:
            htv *= 1 - e
    td = w.tune_date[i]
    if td is not None:
        st = season_of(td)
        v = w.tune_cut[i]
        if st == s:
            j = ds.index(td)
            hwv[j:] *= 1 - v
            htv[j:] *= 1 - v
        elif st < s:
            hwv *= 1 - v
            htv *= 1 - v
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
