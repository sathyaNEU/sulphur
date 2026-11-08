"""task7 architecture 6: Stadtwerke Haldenau's commercial gas customers, the council's 2019 retrofit pilot and the
2026 round, season by season from 2013/14 to 2025/26.

A season runs from 1 May to 30 April and is named by the year it ends (season 2019 is May 2018 to April 2019). Each
building's gas use in a season of long-term average weather is its type's level times its floor area times its own
level, a slow part that drifts and fades by a tenth a season (a tenant's hours, a plant room run hard) and a fast part
that comes and goes within the season. The actual use spreads the weather-dependent share over the season's degree
days. Every May the utility's benchmarking notice goes to the buildings whose normalised use per square metre is in
the top fifth of their type. The May 2019 notice carried the council's pilot offer; the owners who answered it were
drawn by lot for the pilot's places, and the drawn buildings had their works that summer. An answer or an application came with a contractor's quote, and a quote for insulation needs a survey of the roof or walls, so those answers came later in the offer's six weeks. The pandemic winters and the
2022 gas price shock moved every building's use. From August 2019 the utility's service team tuned the burners of
its commercial customers district by district, free of charge, passing over the buildings that had pilot works; most
owners accepted, and a tuned burner burns less gas for the same heat from the visit on. The May 2026 notice carries the
offer of the 2026 round, open to 30 June; the applications received by 12 June are what the utility holds when the climate committee decides the round."""
import datetime as dt
import math

import numpy as np

SEED = 60607
SEASONS = list(range(2014, 2027))          # season Y: 1 May Y-1 to 30 April Y
K = len(SEASONS)
SI = {s: i for i, s in enumerate(SEASONS)}
PILOT = 2019                               # the pilot: offers in the May 2019 notices, places drawn on 8 July 2019
ROUNDS = [PILOT]
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
PHI_SLOW, SD_SLOW = 0.90, 0.025
SD_FAST = 0.020
INTEREST_P = 0.60                          # an offered owner answers the pilot's offer
PLACES = 0.45                              # share of the answers the draw funded
APPLY_2026 = 0.40                          # an offered owner applies in the 2026 round
NOTICE_MD = (5, 20)                        # the benchmarking notices go out on 20 May
CLOSE_MD = (6, 30)                         # an offer in a notice stands to 30 June
DRAW_DATE = dt.date(2019, 7, 8)            # the pilot's places drawn by lot
RECEIVED_TO = dt.date(2026, 6, 12)         # the 2026 applications passed to the utility
# the day an answer or application comes in: it carries a contractor's quote, so most come in the fortnight after the
# notice or in the last ten days before the offer closes, few in between; a quote for insulation needs a survey of the
# roof or walls and most insulation answers come at the end, a quote for controls needs neither and most come early
# (shares of the early fortnight, the weeks between and the last ten days)
ANSWER_SEED_OFFSET = 21
DRAW_SEED_OFFSET = 1996                       # the public draw of 8 July 2019
ANSWER_WAVES = {"insulation": (0.30, 0.10, 0.60), "heating optimisation": (0.50, 0.10, 0.40),
                "heating controls": (0.75, 0.10, 0.15)}
MEASURES = ["insulation", "heating optimisation", "heating controls"]
EFFECT = {"insulation": 0.160, "heating optimisation": 0.060, "heating controls": 0.020}
MEASURE_P = {"office": [0.26, 0.30, 0.44], "retail": [0.28, 0.30, 0.42], "hotel": [0.30, 0.34, 0.36],
             "workshop": [0.36, 0.30, 0.34], "care home": [0.30, 0.36, 0.34], "restaurant": [0.24, 0.32, 0.44]}
WITHDRAW_P = 0.03                          # a drawn owner withdraws before the works
# the service team's burner tuning: districts in a fixed order from September 2019 to March 2026, most of them in
# the first two winters, every commercial gas customer without pilot works offered a visit; a tuned burner cuts the
# building's use for good
N_DISTRICTS = 42
DISTRICTS_PER_SEASON = {2020: 16, 2021: 10, 2022: 6, 2023: 4, 2024: 3, 2025: 2, 2026: 1}
TUNE_START = 2020                          # first visits in season 2020 (from September 2019)
TUNE_ACCEPT = 0.70
TUNE_EFFECT = 0.070
# the pandemic winters and the gas price shock: every building's cut by type in those seasons
COVID = {2020: {"office": 0.02, "retail": 0.03, "hotel": 0.06, "workshop": 0.01, "care home": 0.0, "restaurant": 0.07},
         2021: {"office": 0.08, "retail": 0.07, "hotel": 0.22, "workshop": 0.03, "care home": 0.0, "restaurant": 0.25},
         2022: {"office": 0.05, "retail": 0.03, "hotel": 0.08, "workshop": 0.01, "care home": 0.0, "restaurant": 0.08}}
CRISIS = {2022: 0.020, 2023: 0.140, 2024: 0.110, 2025: 0.090, 2026: 0.080}
# quoted cost per square metre of heated floor area (median, euro) and the grant terms
COST_M2 = {"insulation": 54.5, "heating optimisation": 10.4, "heating controls": 5.4}
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
    w.area = np.round(np.exp(rng.normal(math.log(880.0), 0.62, N)) / 5.0) * 5.0
    w.area = np.clip(w.area, 120.0, 14000.0)
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
    w.district = rng.integers(0, N_DISTRICTS, N)
    order = list(rng.permutation(N_DISTRICTS))
    w.district_season = {}
    for s_, n_ in DISTRICTS_PER_SEASON.items():
        for _ in range(n_):
            w.district_season[int(order.pop(0))] = s_
    w.accept = rng.random(N) < TUNE_ACCEPT
    w.tune_day = rng.random(N)
    w.tune_date = [None] * N
    lvl = np.array([TYPE_LEVEL[TYPES[t]] for t in w.typ])
    w.base = lvl * w.area * np.exp(w.level)
    h_type = np.array([HW_SHARE[TYPES[t]] for t in w.typ])
    tname = np.array([TYPES[t] for t in w.typ])
    mi = np.array([rng.choice(3, p=MEASURE_P[TYPES[t]]) for t in w.typ])
    w.normal = np.zeros((N, K))                # the building's own normal-weather use (kWh)
    w.untuned = np.zeros((N, K))               # normal-weather use before any works or visit (kWh)
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
    eff = np.zeros(N)                          # the measure's cut, a share of use, once the works are done
    tuned = np.zeros(N, bool)
    rng2 = np.random.default_rng(seed + 1)
    for k, s in enumerate(SEASONS):
        live = (w.first <= s) & (w.last >= s)
        ds = w.days[s]
        heat = np.where(w.temp[s] < 15.0, 20.0 - w.temp[s], 0.0)
        nd = float(len(ds))
        f_hw = np.ones(N)
        f_heat = np.ones(N)

        def step(i, j, e):
            """a cut of e from day j of the season on, on the days (hot water) and the degree days (heating)"""
            f_hw[i] *= 1.0 - e * (nd - j) / nd
            f_heat[i] *= 1.0 - e * heat[j:].sum() / heat.sum()
        if s >= TUNE_START:
            months = (8, 9, 10, 11) if s == TUNE_START else (9, 10, 11, 12, 1, 2, 3)
            window = [i for i, d in enumerate(ds) if d.month in months]
            for i in np.where(live & ~tuned & w.accept & ~w.works)[0]:
                if w.district_season[int(w.district[i])] != s:
                    continue
                j = window[min(len(window) - 1, int(w.tune_day[i] * len(window)))]
                w.tune_date[i] = ds[j]
                step(i, j, TUNE_EFFECT)
                tuned[i] = True
        for i in np.where(tuned)[0]:
            if w.tune_date[i] is not None and season_of(w.tune_date[i]) < s:
                f_hw[i] *= 1.0 - TUNE_EFFECT
                f_heat[i] *= 1.0 - TUNE_EFFECT
        for i in np.where(w.works)[0]:
            if s == PILOT + 1:
                step(i, ds.index(w.done_date[i]), eff[i])
            elif s > PILOT + 1:
                f_hw[i] *= 1.0 - eff[i]
                f_heat[i] *= 1.0 - eff[i]
        shock = np.array([COVID.get(s, {}).get(t, 0.0) for t in tname]) + CRISIS.get(s, 0.0)
        ratio = w.G[s] / w.G_LT
        w.untuned[:, k] = np.where(live, w.base * np.exp(slow[:, k] + fast[:, k]) * (1 - shock), 0.0)
        w.actual[:, k] = w.untuned[:, k] * (w.hw * f_hw + (1 - w.hw) * ratio * f_heat)
        w.normal[:, k] = w.actual[:, k] / (w.hw + (1 - w.hw) * ratio)
        if s >= PILOT:
            nrm = w.actual[:, k] * (h_type + (1 - h_type) / ratio) / w.area
            nrm = np.where(live, nrm, np.nan)
            w.norm_intensity[:, k] = nrm
            for t in range(len(TYPES)):
                m = (w.typ == t) & live & (w.first <= s - 1)
                cut = np.quantile(nrm[m], 0.80)
                w.flag[m, k] = nrm[m] > cut
            if s == PILOT:
                w.offer[:, k] = w.flag[:, k]
                ans = w.offer[:, k] & (rng.random(N) < INTEREST_P)
                w.applied[:, k] = ans
                idx = np.where(ans)[0]
                draw = np.random.default_rng(seed + DRAW_SEED_OFFSET).permutation(len(idx))[:int(round(PLACES * len(idx)))]
                w.drawn[idx[draw]] = True
                w.withdrawn = w.drawn & (rng.random(N) < WITHDRAW_P)
                w.works = w.drawn & ~w.withdrawn
                for i in idx:
                    w.measure[i] = MEASURES[mi[i]]
                eff = np.where(w.works, np.array([EFFECT.get(m, 0.0) for m in w.measure]), 0.0)
                summer = [d for d in season_days(PILOT + 1) if dt.date(2019, 7, 15) <= d <= dt.date(2019, 9, 30)]
                for i in np.where(w.works)[0]:
                    w.done_date[i] = summer[int(rng2.integers(0, len(summer)))]
            elif s == PIPELINE:
                w.offer[:, k] = w.flag[:, k] & ~w.works
                take = w.offer[:, k] & (rng.random(N) < APPLY_2026)
                w.applied[:, k] = take
                mi2 = np.array([rng.choice(3, p=MEASURE_P[TYPES[t]]) for t in w.typ])
                for i in np.where(take)[0]:
                    w.measure26[i] = MEASURES[mi2[i]]
    w.grant_round = np.where(w.works, PILOT, -1)
    w.cost = {PILOT: np.zeros(N), PIPELINE: np.zeros(N)}
    w.grant = {PILOT: np.zeros(N), PIPELINE: np.zeros(N)}
    for s, meas in ((PILOT, w.measure), (PIPELINE, w.measure26)):
        k = SI[s]
        for i in np.where(w.applied[:, k])[0]:
            m = meas[i]
            c = COST_M2[m] * w.area[i] * math.exp(rng.normal(0, COST_SD))
            c = round(c / 10.0) * 10.0
            w.cost[s][i] = c
            w.grant[s][i] = min(GRANT_CAP, round(GRANT_SHARE * c / 10.0) * 10.0)
    answer_dates(w, seed + ANSWER_SEED_OFFSET)
    return w


def answer_dates(w, seed):
    """the day each pilot answer and 2026 application came in, and the 2026 applications received by 12 June"""
    rng3 = np.random.default_rng(seed)
    w.answer_date = {PILOT: [None] * w.N, PIPELINE: [None] * w.N}
    for s, meas in ((PILOT, w.measure), (PIPELINE, w.measure26)):
        k = SI[s]
        notice = dt.date(s, *NOTICE_MD)
        span = (dt.date(s, *CLOSE_MD) - notice).days
        for i in np.where(w.applied[:, k])[0]:
            u = rng3.random()
            e, mid, _ = ANSWER_WAVES[meas[i]]
            if u < e:
                day = 1 + int(14 * rng3.beta(1.2, 2.2))
            elif u < e + mid:
                day = 1 + int(span * rng3.random())
            else:
                day = span - int(10 * rng3.beta(1.0, 2.0))
            w.answer_date[s][i] = notice + dt.timedelta(days=min(span, max(1, day)))
    kp = SI[PIPELINE]
    w.received26 = np.array([bool(w.applied[i, kp]) and w.answer_date[PIPELINE][i] <= RECEIVED_TO for i in range(w.N)])


if __name__ == "__main__":
    w = build()
    print("G_LT", w.G_LT, {s: round(w.G[s]) for s in SEASONS})
    k = SI[PILOT]
    print("pilot: offered", int(w.offer[:, k].sum()), "answered", int(w.applied[:, k].sum()), "drawn",
          int(w.drawn.sum()), "works", int(w.works.sum()))
    k = SI[PIPELINE]
    print("2026: offered", int(w.offer[:, k].sum()), "applied", int(w.applied[:, k].sum()), "received by 12 June",
          int(w.received26.sum()))
    tuned = np.array([d is not None for d in w.tune_date])
    print("tuned", int(tuned.sum()), "of", w.N, "; losers tuned", int((tuned & w.applied[:, SI[PILOT]] & ~w.drawn).sum()),
          "of", int((w.applied[:, SI[PILOT]] & ~w.drawn).sum()))
    for m in MEASURES:
        print(m, "works", int((w.works & (w.measure == m)).sum()))


def daily_kwh(w, i, s):
    """building i's metered gas use, day by day, in season s (kWh): its normal-weather use spread over the days (hot
    water) and the season's degree days (heating), with the works' cut from the day they were done and the burner
    tuning's cut from the day of the visit"""
    k = SI[s]
    ds = w.days[s]
    heat = np.where(w.temp[s] < 15.0, 20.0 - w.temp[s], 0.0)
    nd = float(len(ds))
    shape = w.hw[i] / nd + (1 - w.hw[i]) * heat / w.G_LT
    stepv = np.ones(len(ds))
    if w.works[i]:
        if s == PILOT + 1:
            stepv[ds.index(w.done_date[i]):] *= 1 - EFFECT[w.measure[i]]
        elif s > PILOT + 1:
            stepv *= 1 - EFFECT[w.measure[i]]
    td = w.tune_date[i]
    if td is not None:
        st = season_of(td)
        if st == s:
            stepv[ds.index(td):] *= 1 - TUNE_EFFECT
        elif st < s:
            stepv *= 1 - TUNE_EFFECT
    return w.untuned[i, k] * shape * stepv
