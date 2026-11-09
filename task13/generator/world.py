"""The clean world behind task13: Kotuku Networks' 48 11 kV feeders, four weather stations, the corridors'
growth since each cycle trim, and every sustained and momentary interruption from 2016 to October 2026.

Tree contacts happen hour by hour at a rate set by the gust at the feeder's station, the corridor's density and
length, and the growth since the corridor's last cycle trim. Other causes run at their own rates. Storm days push
the system's daily SAIDI over the regulator's boundary value and are major event days. The truth for the decision
is each feeder's expected 2027-28 tree-caused customer interruptions outside major event days, with and without a
catch-up trim completed on 31 March 2027, over many synthetic weather years.
"""
import datetime as dt

import numpy as np
import pandas as pd

SEED = 1312
START = dt.datetime(2006, 1, 1)      # the weather stations' hourly record
REC_START = dt.datetime(2016, 1, 1)  # interruptions are simulated from here (boundary values need the history)
END = dt.datetime(2026, 10, 31, 23)
OMS_START = dt.datetime(2022, 4, 1)
RY27 = (dt.datetime(2027, 4, 1), dt.datetime(2028, 3, 31, 23))
CATCHUP_DONE = dt.datetime(2027, 3, 31)
LAST12 = (dt.datetime(2025, 11, 1), dt.datetime(2026, 10, 31, 23))
# the stretch of weather that ran against the long-run normal, calm in the north and windy in the south
ANOM = (dt.datetime(2023, 11, 1), dt.datetime(2026, 10, 31, 23))
# an earlier swing the other way, which ran its course
EARLY = (dt.datetime(2009, 11, 1), dt.datetime(2011, 10, 31, 23))

# ------------------------------------------------------------------ stations and their climate
STATIONS = [
    # id, name, lat, lon, elevation m, anemometer m, area, wind level (km/h), spread
    ('PBA', 'Paua Bay', -39.718, 176.958, 18, 10, 'north', 27.0, 0.13),
    ('MTF', 'Mataroa Flats', -40.071, 176.512, 64, 10, 'central', 26.0, 0.13),
    ('KWR', 'Kowhai Ridge', -40.402, 176.235, 412, 10, 'south', 29.0, 0.13),
    ('TSD', 'Titi Saddle', -40.611, 176.588, 538, 10, 'south', 29.5, 0.13),
]
NS = len(STATIONS)
# the two years to October 2026: calm on the northern coast and plains, the windiest in the record in the south


def tree_intensity(w):
    """tree contacts per hour per unit corridor at an hourly gust of w km/h (the weakest limbs are down by the
    strongest gusts, so the rate stops climbing)"""
    return np.clip(np.clip((w - 40.0) / 30.0, 0.0, None) ** 2, 0.0, 3.0)


GAMMA = 0.15      # corridor growth per year since a cycle trim
Y0 = 0.0
KAPPA = 2.5e-3    # tree contacts per km per unit density per unit intensity per hour


def growth(ys):
    return np.exp(GAMMA * np.clip(ys - Y0, 0.0, None))


# ------------------------------------------------------------------ zone substations and feeders
ZONES = [
    # code, name, lat, lon, station
    ('PBY', 'Paua Bay', -39.731, 176.941, 0),
    ('WTK', 'Waitaki Road', -39.805, 176.872, 0),
    ('HRK', 'Harakeke', -39.872, 176.990, 0),
    ('MTR', 'Mataroa', -40.064, 176.540, 1),
    ('RNG', 'Rangiora Street', -40.112, 176.455, 1),
    ('OKR', 'Okere', -40.185, 176.602, 1),
    ('KWH', 'Kowhai', -40.388, 176.262, 2),
    ('TOT', 'Totara Gully', -40.452, 176.155, 2),
    ('TIT', 'Titi', -40.598, 176.571, 3),
    ('MKR', 'Makora', -40.664, 176.452, 3),
]

SOUTH = ['KWH', 'TOT', 'TIT', 'MKR']
GROUPS = {
    # overdue northern coastal feeders: a moderate corridor left longest since its cycle trim
    'O': dict(n=6, zones=['PBY', 'WTK', 'HRK'], tau=(2.05, 2.25), km=(35, 38), cust=(1000, 1100), p_bb=(0.05, 0.08),
              rc=(4, 4), fu=(10, 14), fu_share=0.45, win=('2019-10-01', '2020-06-30'), cycle=4),
    # plantation feeders in the southern hills: a dense corridor on a three-year cycle, trimmed in the second half of 2025
    'D': dict(n=5, zones=SOUTH, tau=(2.5, 2.8), km=(25, 30), cust=(750, 950), p_bb=(0.05, 0.08),
              rc=(1, 1), fu=(4, 6), fu_share=0.55, win=('2025-06-01', '2025-10-31'), cycle=3),
    # southern feeders late in their cycle
    'W': dict(n=8, zones=SOUTH, tau=(1.10, 1.30), km=(30, 35), cust=(800, 950), p_bb=(0.05, 0.08),
              rc=(4, 4), fu=(10, 14), fu_share=0.45, win=('2021-04-01', '2021-12-31'), cycle=4),
    # small overdue feeders with few trees
    'P': dict(n=4, zones=['PBY', 'WTK', 'HRK', 'MTR', 'OKR'], tau=(0.6, 0.9), km=(16, 24), cust=(330, 520),
              p_bb=(0.05, 0.10), rc=(2, 3), fu=(6, 10), fu_share=0.50, win=('2019-06-01', '2020-03-31'), cycle=4),
    # open plains feeders on an eight-year cycle
    'L': dict(n=5, zones=['PBY', 'RNG', 'MTR'], tau=(0.10, 0.16), km=(18, 28), cust=(1100, 1500), p_bb=(0.05, 0.10),
              rc=(3, 4), fu=(8, 12), fu_share=0.50, win=('2017-02-01', '2017-09-30'), cycle=8),
    # the rest of the network
    'B': dict(n=20, zones=None, tau=(0.4, 1.0), km=(16, 40), cust=(400, 1150), p_bb=(0.05, 0.12),
              rc=(2, 4), fu=(6, 12), fu_share=0.50, win=None, cycle=4),
}
B_LAST = ('2021-06-01', '2026-06-30')


def build_network(rng):
    rows = []
    order = []
    for g, spec in GROUPS.items():
        order += [g] * spec['n']
    rng.shuffle(order)
    for g in order:
        spec = GROUPS[g]
        zc = rng.choice(spec['zones']) if spec['zones'] else ZONES[int(rng.integers(0, len(ZONES)))][0]
        rows.append(dict(group=g, zone=zc, tau=rng.uniform(*spec['tau']), km=rng.uniform(*spec['km']),
                         cust0=int(rng.uniform(*spec['cust'])), p_bb=rng.uniform(*spec['p_bb']),
                         nrc=int(rng.integers(spec['rc'][0], spec['rc'][1] + 1)), nfu=int(rng.integers(spec['fu'][0], spec['fu'][1] + 1)),
                         fu_share=spec['fu_share'], cycle=spec['cycle'], win=spec['win']))
    F = pd.DataFrame(rows)
    zidx = {z[0]: i for i, z in enumerate(ZONES)}
    F['station'] = [ZONES[zidx[z]][4] for z in F['zone']]
    # feeder codes: zone code and a number, in zone order
    F['n_in_zone'] = F.groupby('zone').cumcount() + 1
    F['feeder'] = [('%s-%02d' % (z, k)) for z, k in zip(F['zone'], F['n_in_zone'])]
    F['ug_km'] = np.round(rng.uniform(0.5, 6.0, len(F)) + np.where(F['group'] == 'L', 8.0, 0.0), 1)
    F['km'] = np.round(F['km'], 1)
    F['age'] = rng.integers(1962, 1998, len(F))
    return F


def trim_history(F, rng):
    """cycle trim completion dates for each feeder from 2009 to October 2026"""
    hist = {}
    for i, r in F.iterrows():
        if r['win'] is not None:
            a, b = pd.Timestamp(r['win'][0]), pd.Timestamp(r['win'][1])
            last = a + (b - a) * rng.random()
        else:
            # background feeders: on a four-year cycle, last completion between late 2020 and mid 2026
            last = pd.Timestamp(B_LAST[0]) + (pd.Timestamp(B_LAST[1]) - pd.Timestamp(B_LAST[0])) * rng.random()
        dates = [last]
        step = r['cycle']
        while dates[-1] > pd.Timestamp('2005-06-01'):
            dates.append(dates[-1] - pd.Timedelta(days=float(step * 365.25 + rng.normal(0, 60))))
        hist[r['feeder']] = sorted(d.floor('D').to_pydatetime() for d in dates)
    return hist


def years_since(dates, t):
    """years since the latest completion at or before each time in t (array of datetime64)"""
    d = np.array(dates, dtype='datetime64[s]')
    idx = np.searchsorted(d, t, side='right') - 1
    last = d[np.clip(idx, 0, None)]
    ys = (t - last).astype('timedelta64[s]').astype(float) / (365.25 * 86400)
    ys[idx < 0] = 8.0
    return ys


# ------------------------------------------------------------------ the gust process
REGION = np.array([0, 0, 1, 1])        # stations on the northern coast and plains (0), in the southern hills (1)
P_SYSTEM = 0.25                        # a frontal system or low reaches the district on this share of days
REACH = np.array([0.50, 0.46])         # the share of systems that bring strong winds to each region
ANOM_REACH = np.array([0.35, 2.00])    # the three years to October 2026: the storm track sat south
EARLY_REACH = np.array([1.60, 0.55])   # November 2009 to October 2011: it sat north
STRONG = np.exp(0.83)                  # systems this strong lengthen restoration and bring lightning


def seasonal(doy):
    return 1.0 + 0.10 * np.cos(2 * np.pi * (doy - 230) / 365.25)


def gusts(rng, hours, reach_mult=None):
    """hourly maximum gusts (km/h) for every station over the given hourly index; reach_mult (days x regions)
    scales the share of passing systems that bring strong winds to each region"""
    days = hours.normalize().unique()
    nd = len(days)
    # a regional synoptic index shared by every station, with its own day-to-day persistence (ordinary days)
    z = np.zeros(nd)
    e = rng.normal(0, 1, nd)
    for k in range(1, nd):
        z[k] = 0.55 * z[k - 1] + np.sqrt(1 - 0.55 ** 2) * e[k]
    doy = np.array([d.dayofyear for d in days])
    # strong-wind days: a passing system, which reaches each region with its own probability
    system = rng.random(nd) < P_SYSTEM * seasonal(doy)
    rm = np.ones((nd, 2)) if reach_mult is None else reach_mult
    hit = np.zeros((nd, 2), bool)
    u = rng.random((nd, 2))
    for r in range(2):
        hit[:, r] = system & (u[:, r] < np.clip(REACH[r] * rm[:, r], 0, 1))
    strength = np.exp(rng.normal(0.75, 0.06, nd))          # the system's peak gust over the day's ordinary level
    centre = rng.uniform(0, 24, nd)
    out = np.zeros((len(hours), NS))
    day_of_hour = np.searchsorted(days.values, hours.normalize().values)
    hod = hours.hour.values
    diurnal = 1.0 + 0.12 * np.sin(2 * np.pi * (hod - 9) / 24)
    for s, st in enumerate(STATIONS):
        level, spread = st[7], st[8]
        own = rng.normal(0, 1, nd)
        lvl = level * seasonal(doy) * np.exp(spread * (0.75 * z + 0.66 * own) - spread ** 2 / 2)
        local = strength * np.exp(rng.normal(0, 0.06, nd))
        bump = np.exp(-0.5 * ((hod - centre[day_of_hour]) / 4.0) ** 2)
        storm = np.where(hit[day_of_hour, REGION[s]], 1.0 + (local[day_of_hour] - 1.0) * bump, 1.0)
        noise = np.exp(rng.normal(0, 0.10, len(hours)))
        out[:, s] = lvl[day_of_hour] * diurnal * storm * noise
    return out, days, (hit, strength)


def reach_by_day(days):
    """the reach multipliers for each day: two stretches ran against the long-run normal"""
    rm = np.ones((len(days), 2))
    for (a, b), m in ((ANOM, ANOM_REACH), (EARLY, EARLY_REACH)):
        sel = (days >= pd.Timestamp(a)) & (days <= pd.Timestamp(b))
        rm[sel] = m
    return rm


# ------------------------------------------------------------------ devices and customers per interruption
def build_devices(F, rng):
    """a breaker at the zone substation, reclosers sectionalising the backbone, fuses on the spurs"""
    dev = []
    for i, r in F.iterrows():
        f = r['feeder']
        dev.append(dict(feeder=f, device_id='%s-CB' % f, device_type='Circuit breaker', share=1.0, lateral_km=0.0))
        cuts = np.array([0.45, 0.30, 0.18, 0.08])[:int(r['nrc'])] * rng.uniform(0.9, 1.1, int(r['nrc']))
        for k, c in enumerate(cuts):
            dev.append(dict(feeder=f, device_id='%s-R%d' % (f, k + 1), device_type='Recloser', share=float(c), lateral_km=0.0))
        nfu = int(r['nfu'])
        w = rng.gamma(3.0, 1.0, nfu)
        shf = r['fu_share'] * w / w.sum()
        lk = r['km'] * (1 - 0.35) * w / w.sum()
        for k in range(nfu):
            dev.append(dict(feeder=f, device_id='%s-F%02d' % (f, k + 1), device_type='Fuse', share=float(shf[k]), lateral_km=float(lk[k])))
    return pd.DataFrame(dev)


P_CB = 0.05     # the share of sustained backbone faults the zone substation breaker clears


def cust_per_tree(F, D):
    """expected customers per tree interruption at each feeder (2026 customers)"""
    out = {}
    for i, r in F.iterrows():
        d = D[D['feeder'] == r['feeder']]
        rc = d[d['device_type'] == 'Recloser']['share'].values
        fu = d[d['device_type'] == 'Fuse']
        bb = P_CB * 1.0 + (1 - P_CB) * rc.mean()
        lat = (fu['share'] * fu['lateral_km']).sum() / fu['lateral_km'].sum()
        out[r['feeder']] = r['cust0'] * (r['p_bb'] * bb + (1 - r['p_bb']) * lat)
    return out


# ------------------------------------------------------------------ simulation of the record
OTHER = {
    # cause: daily rate per overhead km (or per 1,000 customers for vehicles), seasonal amplitude
    'equipment': (0.00060, 0.0),
    'animal': (0.00045, 0.35),
    'vehicle': (0.00140, 0.0),
    'unknown': (0.00028, 0.0),
}
PLANNED_PER_DAY = 0.0105
MOMENTARY_PER_TREE = 1.6


def simulate(seed=SEED):
    rng = np.random.default_rng(seed)
    F = build_network(rng)
    trims = trim_history(F, rng)
    D = build_devices(F, rng)
    hours_w = pd.date_range(START, END, freq='h')
    days_w = hours_w.normalize().unique()
    W_all, _, (hit, strength) = gusts(rng, hours_w, reach_mult=reach_by_day(days_w))
    keep_h = hours_w >= pd.Timestamp(REC_START)
    keep_d = days_w >= pd.Timestamp(REC_START)
    hours, days, W = hours_w[keep_h], days_w[keep_d], W_all[keep_h]
    G = tree_intensity(W)
    return dict(F=F, trims=trims, D=D, hours=hours, days=days, W=W, G=G, z=(hit[keep_d], strength[keep_d]),
                hours_w=hours_w, W_all=W_all, rng=rng)


def tree_rates(S):
    """expected tree contacts for each feeder and hour (array hours x feeders)"""
    F, hours = S['F'], S['hours']
    t = hours.values.astype('datetime64[s]')
    lam = np.zeros((len(hours), len(F)))
    for j, r in F.iterrows():
        ys = years_since(S['trims'][r['feeder']], t)
        lam[:, j] = KAPPA * r['km'] * r['tau'] * growth(ys) * S['G'][:, r['station']]
    return lam


# ------------------------------------------------------------------ interruptions
P_SUSTAINED_TREE = 0.62


def customers_at(F, year):
    return np.round(F['cust0'].values * (1 - 0.011 * (2026 - year))).astype(int)


def pick_device(rng, devs, backbone):
    """a device for one interruption: a breaker or a recloser on the backbone, else a fuse by lateral km"""
    if backbone:
        cb = devs[devs['device_type'] == 'Circuit breaker']
        rc = devs[devs['device_type'] == 'Recloser']
        return cb.iloc[0] if rng.random() < P_CB else rc.iloc[int(rng.integers(0, len(rc)))]
    fu = devs[devs['device_type'] == 'Fuse']
    p = fu['lateral_km'].values / fu['lateral_km'].values.sum()
    return fu.iloc[int(rng.choice(len(fu), p=p))]


def interruptions(S):
    rng = np.random.default_rng(SEED + 11)
    F, D, hours = S['F'], S['D'], S['hours']
    lam = tree_rates(S)
    S['lam'] = lam
    n_tree = rng.poisson(lam)
    devs = {f: D[D['feeder'] == f].reset_index(drop=True) for f in F['feeder']}
    days = S['days']
    dayG = pd.DataFrame(S['G'], index=hours).resample('D').sum().values      # days x stations
    rows = []
    hr_index = hours

    def add(j, t, cause, backbone, sustained, storm=False):
        r = F.iloc[j]
        d = pick_device(rng, devs[r['feeder']], backbone)
        cust = int(round(customers_at(F, t.year)[j] * d['share']))
        if sustained:
            mean = 75.0 if backbone else 118.0
            dur = float(np.exp(rng.normal(np.log(mean), 0.55))) * (1.4 if storm else 1.0)
        else:
            dur = float(rng.uniform(0.05, 0.9))
        rows.append(dict(feeder=r['feeder'], device_id=d['device_id'], device_type=d['device_type'], start=t,
                         minutes=dur, customers=cust, cause=cause, sustained=sustained))

    hit, strength = S['z']
    storm_day = set(days[np.where(hit.any(1) & (strength > STRONG))[0]])
    # tree contacts, hour by hour
    hh, jj = np.nonzero(n_tree)
    for h, j in zip(hh, jj):
        for _ in range(n_tree[h, j]):
            t = hr_index[h] + pd.Timedelta(minutes=int(rng.integers(0, 60)))
            bb = rng.random() < F.iloc[j]['p_bb']
            add(j, t, 'tree', bb, rng.random() < P_SUSTAINED_TREE, storm=t.normalize() in storm_day)
    # other causes, day by day
    doy = np.array([d.dayofyear for d in days])
    season = 1.0 + 0.35 * np.cos(2 * np.pi * (doy - 330) / 365.25)
    for j, r in F.iterrows():
        cust_k = r['cust0'] / 1000.0
        age_f = 1.0 + (1990 - r['age']) / 40.0
        st = r['station']
        rates = {
            'equipment': np.full(len(days), OTHER['equipment'][0] * r['km'] * age_f),
            'animal': OTHER['animal'][0] * r['km'] * season,
            'vehicle': np.full(len(days), OTHER['vehicle'][0] * cust_k),
            'unknown': np.full(len(days), OTHER['unknown'][0] * r['km']),
            'wind': 2.0e-6 * r['km'] * dayG[:, st],
            'lightning': np.where(np.isin(days, list(storm_day)), 0.02 * r['km'] / 30.0, 0.0001 * r['km'] / 30.0),
        }
        for cause, lam_d in rates.items():
            n = rng.poisson(lam_d)
            for k in np.nonzero(n)[0]:
                for _ in range(n[k]):
                    t = days[k] + pd.Timedelta(minutes=int(rng.integers(0, 1440)))
                    bb = rng.random() < (0.25 if cause in ('equipment', 'wind', 'lightning') else 0.12)
                    add(j, t, cause, bb, rng.random() < 0.80, storm=days[k] in storm_day)
        # planned work, mostly on laterals and on weekdays
        n = rng.poisson(np.full(len(days), PLANNED_PER_DAY))
        for k in np.nonzero(n)[0]:
            if days[k].dayofweek >= 5:
                continue
            t = days[k] + pd.Timedelta(hours=int(rng.integers(8, 14)), minutes=int(rng.choice([0, 15, 30, 45])))
            d = pick_device(rng, devs[r['feeder']], rng.random() < 0.1)
            cust = int(round(customers_at(F, t.year)[j] * d['share']))
            rows.append(dict(feeder=r['feeder'], device_id=d['device_id'], device_type=d['device_type'], start=t,
                             minutes=float(rng.uniform(150, 420)), customers=cust, cause='planned', sustained=True))
    # snow on the southern hills: a winter day or two most years, when snow-loaded conductors and trees bring down
    # backbone sections across the southern feeders for hours
    srng = np.random.default_rng(SEED + 13)
    south = [j for j, r in F.iterrows() if r['zone'] in SOUTH]
    central = [j for j, r in F.iterrows() if r['zone'] in ('MTR', 'OKR', 'RNG')]
    for y in range(REC_START.year, END.year + 1):
        for _ in range(int(srng.poisson(1.3))):
            day = pd.Timestamp(y, 6, 1) + pd.Timedelta(days=int(srng.integers(0, 92)))
            for j in south + [c for c in central if srng.random() < 0.3]:
                r = F.iloc[j]
                for _ in range(int(srng.poisson(2.0))):
                    t = day + pd.Timedelta(minutes=int(srng.integers(0, 1440)))
                    d = pick_device(srng, devs[r['feeder']], srng.random() < 0.6)
                    rows.append(dict(feeder=r['feeder'], device_id=d['device_id'], device_type=d['device_type'], start=t,
                                     minutes=float(np.exp(srng.normal(np.log(420.0), 0.5))),
                                     customers=int(round(customers_at(F, t.year)[j] * d['share'])), cause='wind',
                                     sustained=True))
    E = pd.DataFrame(rows).sort_values('start').reset_index(drop=True)
    return E


# ------------------------------------------------------------------ major event days
def regulatory_year(t):
    return t.year if t.month >= 4 else t.year - 1


# the price-quality paths: each sets its boundary values from the regulatory years before it starts
PERIODS = {'DPP3': (2020, 2024, (2016, 2019)), 'DPP4': (2025, 2029, (2016, 2023))}


def daily_indices(E, F):
    """daily unplanned SAIDI and SAIFI (sustained interruptions), over the year's customers"""
    u = E[(E['cause'] != 'planned') & E['sustained']].copy()
    u['day'] = u['start'].dt.normalize()
    u['ry'] = [regulatory_year(t) for t in u['start']]
    base = {ry: float(customers_at(F, ry).sum()) for ry in range(2014, 2031)}
    den = u['ry'].map(base)
    saidi = (u['customers'] * u['minutes'] / den).groupby(u['day']).sum()
    saifi = (u['customers'] / den).groupby(u['day']).sum()
    return saidi, saifi


# the boundary values the Commerce Commission set for the network on each path, from its own reference years
BOUNDARY = {'DPP3': (31.40, 0.2050), 'DPP4': (29.85, 0.1985)}


def boundary_values(E, F):
    """each path's SAIDI and SAIFI boundary values, and the record's daily unplanned SAIDI and SAIFI"""
    return dict(BOUNDARY), daily_indices(E, F)


def path_of(ry):
    for name, (y0, y1, _) in PERIODS.items():
        if y0 <= ry <= y1:
            return name
    return None


def med_days(daily, bounds):
    saidi, saifi = daily
    out = set()
    for x, k in ((saidi, 0), (saifi, 1)):
        for d, v in x.items():
            p = path_of(regulatory_year(d))
            if p and v > bounds[p][k]:
                out.add(d)
    return out


# ------------------------------------------------------------------ the truth for 2027-28
def truth(S, E, reps=60, seed=SEED + 77):
    """each feeder's expected 2027-28 sustained tree-caused customer interruptions on days that are not major
    event days, left as it is and with a catch-up trim completed on 31 March 2027, over synthetic weather years.
    Major event days are the stormiest days; each station's share of tree exposure on them is taken from the
    record and held for 2027-28."""
    F, D = S['F'], S['D']
    bounds, daily = boundary_values(E, F)
    meds = med_days(daily, bounds)
    ism = pd.Index(S['hours'].normalize()).isin(meds)
    med_share = S['G'][ism].sum(0) / S['G'].sum(0)
    cpe = np.array([cust_per_tree(F, D)[f] for f in F['feeder']])
    hours = pd.date_range(RY27[0], RY27[1], freq='h')
    tt = hours.values.astype('datetime64[s]')
    gr_keep = np.zeros((len(hours), len(F)))
    for j, r in F.iterrows():
        gr_keep[:, j] = growth(years_since(S['trims'][r['feeder']], tt))
    ys_cu = (tt - np.datetime64(CATCHUP_DONE)).astype('timedelta64[s]').astype(float) / (365.25 * 86400)
    gr_cu = growth(ys_cu)
    base = KAPPA * F['km'].values * F['tau'].values
    st = F['station'].values
    rng = np.random.default_rng(seed)
    keep = np.zeros(len(F)); cu = np.zeros(len(F))
    for k in range(reps):
        Wk, _, _ = gusts(rng, hours)
        Gk = tree_intensity(Wk)[:, st] * (1 - med_share[st])[None, :]
        keep += (base[None, :] * gr_keep * Gk).sum(0)
        cu += (base[None, :] * gr_cu[:, None] * Gk).sum(0)
    keep = keep / reps * P_SUSTAINED_TREE * cpe
    cu = cu / reps * P_SUSTAINED_TREE * cpe
    n_med = len([d for d in meds if regulatory_year(d) in (2022, 2023, 2024, 2025)]) / 4.0
    return pd.DataFrame(dict(feeder=F['feeder'], group=F['group'], keep=keep, catchup=cu, avoided=keep - cu,
                             cpe=cpe)), n_med / reps
