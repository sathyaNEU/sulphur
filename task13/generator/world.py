"""The clean world: the co-op's zones and their equipment, the defects that develop on them (ground leads stolen,
a batch of line arresters failing, a batch of porcelain pin insulators cracking), the cyclic line inspections that
find and repair them, every fault on every zone (lightning flashovers, storm winds, typhoons, animals, vegetation,
equipment, arrester failures), each fault's protection sequence, transformer burnouts and restorations."""
import numpy as np
import pandas as pd

import common as C
import net as NET
import phys as PH
import storms as ST

SEED = 1302
T0 = pd.Timestamp('2016-12-01')
T1 = pd.Timestamp('2026-11-01')
DAY = pd.Timedelta(days=1)

# cyclic line inspection rounds: each dry season (December to March) one fifth of the substations' zones
ROUND_START = {2016: '2016-12-01', 2017: '2017-12-01', 2018: '2018-12-01', 2019: '2019-12-01', 2020: '2020-12-01',
               2021: '2021-12-01', 2022: '2022-12-01', 2023: '2023-12-01', 2024: '2024-12-01', 2025: '2025-12-01'}


def yfrac(t):
    t = pd.Timestamp(t)
    return t.year + (t.dayofyear - 0.5) / 365.25


def zones(N, rng):
    """zone attributes: equipment, members, the line arrester programme, hidden pressures"""
    S, Z = N['S'], N['Z']
    g = S.groupby('zone_ix')
    Z = Z.copy()
    Z['km'] = g.km.sum().reindex(Z.zone_ix).values
    Z['km3'] = S[S.phases == 3].groupby('zone_ix').km.sum().reindex(Z.zone_ix).fillna(0).values
    Z['km1'] = Z.km - Z.km3
    for st in NET.SETTINGS:
        Z['km_' + st] = S[S.setting == st].groupby('zone_ix').km.sum().reindex(Z.zone_ix).fillna(0).values
    for c in ('wood_xarm', 'steel_xarm', 'bracket', 'concrete_bracket'):
        Z['km_' + c] = S[S.construction == c].groupby('zone_ix').km.sum().reindex(Z.zone_ix).fillna(0).values
    tx = g.apply(lambda d: (d.km * d.tx_per_km).sum()).reindex(Z.zone_ix).values
    Z['n_tx'] = rng.poisson(tx)
    Z['members'] = (Z.n_tx * rng.lognormal(np.log(27), 0.25, len(Z))).round().astype(int)
    # the 2015-2016 line arrester programme on the exposed zones: arresters about every 300 m on open and hill line
    exposed = (Z.km_open + Z.km_hill + 0.5 * Z.km_treed) / Z.km
    Z['la_prog'] = rng.random(len(Z)) < np.clip(0.15 + 0.9 * exposed, 0, 0.92)
    prog_km = (Z.km_open + Z.km_hill + Z.km_treed) * Z.la_prog
    Z['n_la'] = np.where(Z.la_prog, rng.poisson(prog_km * 3.2), 0)
    Z['km_prot'] = np.where(Z.la_prog, Z.km_open + Z.km_hill + Z.km_treed, 0.0)
    # one of the programme's two contract lots used a polymer arrester that ages badly
    lot = rng.random(len(Z)) < 0.10
    Z['la_lot_b'] = Z.la_prog & lot
    # hidden: vegetation density along the zone (storm-wind faults), theft pressure (scrap buyers, road access)
    Z['veg'] = rng.lognormal(0, 0.55, len(Z)) * (0.6 + Z.km_treed / Z.km)
    dtown = np.array([np.min(np.hypot(N['towns'][:, 0] - xm, N['towns'][:, 1] - ym))
                      for xm, ym in zip(g.xm.mean().reindex(Z.zone_ix), g.ym.mean().reindex(Z.zone_ix))])
    Z['dtown'] = dtown
    Z['theft_rate'] = np.clip((0.003 + 0.075 * np.exp(-dtown / 5.0) * rng.lognormal(0, 0.6, len(Z))) * np.where(Z.la_prog, 1.0, 0.15), 0, 0.3)
    # a batch of porcelain pin insulators on the 2019 post-typhoon rebuilds
    Z['pin_batch'] = (Z.km_steel_xarm > 2) & (rng.random(len(Z)) < 0.08)
    # what no register holds: each zone's own susceptibility to a flashover, and its season-to-season swing
    # (the soil each zone's arrester grounds are driven into and the hardware and route the register does not
    # describe: a level that stays with the zone whatever its protection's state, and a season-to-season swing)
    Z['susc'] = rng.lognormal(-0.5 * 0.45 ** 2, 0.45, len(Z))
    Z['susc_season'] = [list(rng.lognormal(-0.5 * 0.10 ** 2, 0.10, 11)) for _ in range(len(Z))]
    # protection device and controller
    kind = Z.kind.values
    model = np.where(kind == 'breaker', 'relay', np.where(rng.random(len(Z)) < 0.46, 'old', 'new'))
    Z['controller'] = model
    Z['telemetry'] = np.where(model == 'relay', 'SCADA', np.where(model == 'new', np.where(rng.random(len(Z)) < 0.9,
                              'SCADA', 'none'), np.where(rng.random(len(Z)) < 0.12, 'SCADA', 'none')))
    Z['memory'] = np.where(model == 'old', rng.choice([64, 100], len(Z), p=[0.55, 0.45]), 1024)
    Z['drift'] = np.where(Z.telemetry == 'none', rng.normal(0, 1.35, len(Z)), 0.0)
    Z.loc[(Z.telemetry == 'none') & (Z.drift.abs() < 0.25), 'drift'] *= 4
    # names: the substation's code, its feeders numbered F1 up, the breaker zone named for the feeder and each
    # recloser zone downstream of it R1, R2 in order
    Z['sub_code'] = [C.SUBSTATIONS[s][0] for s in Z['sub']]
    fno = {}
    for s_, g_ in Z.groupby('sub'):
        for k, f in enumerate(sorted(g_.feeder_ix.unique())):
            fno[f] = k + 1
    Z['feeder'] = [sc + '-F%d' % fno[f] for sc, f in zip(Z.sub_code, Z.feeder_ix)]
    Z['zone'] = [fd if o == 0 else '%s-R%d' % (fd, o) for fd, o in zip(Z.feeder, Z.order)]
    zname = dict(zip(Z.zone_ix, Z.zone))
    Z['parent'] = [zname.get(p, '') for p in Z.parent_ix]
    yrs = np.where(Z.controller == 'old', rng.integers(2003, 2010, len(Z)), np.where(Z.controller == 'new',
                   rng.integers(2013, 2017, len(Z)), rng.integers(2008, 2016, len(Z))))
    Z['commissioned'] = yrs
    return Z


def inspection_plan(N, Z, rng):
    """each substation's zones go in one round of five; inside the round, feeder by feeder"""
    subs = np.arange(len(N['subs']))
    rng.shuffle(subs)
    groups = np.array_split(subs, 5)
    grp_of = {s: gi for gi, gr in enumerate(groups) for s in gr}
    rows = []
    for gi in range(5):
        for year in (2016 + gi, 2021 + gi):
            zs = Z[Z['sub'].isin(groups[gi])].sort_values(['sub', 'feeder_ix', 'order'])
            t = pd.Timestamp(ROUND_START[year]) + pd.Timedelta(days=float(rng.uniform(0, 8)))
            span = (pd.Timestamp(year + 1, 3, 25) - t).days
            step = span / max(1, len(zs))
            for k, z in enumerate(zs.itertuples()):
                st = t + pd.Timedelta(days=k * step + rng.uniform(0, step * 0.4))
                dur = int(np.clip(rng.lognormal(np.log(z.km / 7.0), 0.3), 1, 6))
                rows.append(dict(zone_ix=z.zone_ix, round=year, start=st.normalize(), end=(st + pd.Timedelta(days=dur - 1)).normalize()))
    I = pd.DataFrame(rows).sort_values(['zone_ix', 'start']).reset_index(drop=True)
    Z['round_group'] = Z['sub'].map(grp_of)
    return I


def defects(Z, I, rng):
    """event timelines per zone from 2016 to the end of the record: thefts of ground leads, line arrester
    failures (lot B), pin insulator cracks (the 2019 batch); repairs at each cyclic inspection
    (each item found with probability 0.9) and when a crew replaces a failed arrester after it faulted"""
    ev = []          # (zone_ix, time, kind, value)
    t_start = pd.Timestamp('2016-01-01')
    for z in Z.itertuples():
        insp = I[I.zone_ix == z.zone_ix].sort_values('start')
        ng = z.n_tx + z.n_la
        # ground lead theft: a Poisson process of night-time strippings, each taking a share of what is left
        t = t_start
        while True:
            t = t + pd.Timedelta(days=float(min(rng.exponential(365.25 / max(z.theft_rate, 1e-3)), 7300.0)))
            if t >= T1:
                break
            ev.append((z.zone_ix, t.normalize() + pd.Timedelta(hours=float(rng.uniform(0, 5))), 'theft',
                       float(rng.beta(14.0, 1.2))))
        # lot B line arresters: Weibull ageing from installation in 2015-2016
        if z.la_lot_b and z.n_la > 0:
            inst = pd.Timestamp('2015-06-01 12:00') + pd.Timedelta(days=float(rng.uniform(0, 420)))
            life = (rng.uniform(8.2, 11.5) + rng.normal(0, 0.35, z.n_la))
            for L in life:
                tf = inst + pd.Timedelta(days=float(L * 365.25))
                if tf < T1:
                    # a failure that faults the line is found and replaced by the crew; one whose disconnector
                    # drops it out leaves the line unprotected there until the next inspection
                    ev.append((z.zone_ix, tf, 'la_fault' if rng.random() < 0.35 else 'la_fail', 1.0))
        # the 2019 pin insulator batch: spans crack with a hazard from 2020
        if z.pin_batch:
            nsp = max(1, int((z.km_steel_xarm + z.km_bracket) * 2.5))
            tc = pd.Timestamp('2020-03-01') + pd.Timedelta(days=float(rng.uniform(500, 1900))) + pd.to_timedelta(rng.gamma(2.0, 70.0, nsp), unit='D')
            for x in tc[tc < T1]:
                ev.append((z.zone_ix, x, 'crack', 1.0 / nsp))
    E = pd.DataFrame(ev, columns=['zone_ix', 't', 'kind', 'v']).sort_values(['zone_ix', 't']).reset_index(drop=True)
    return E


def state_timeline(Z, I, E, rng):
    """walk each zone's events and inspections in time order: g = share of arrester ground leads intact,
    a = share of line arresters working, c = share of steel-crossarm spans with a cracked pin insulator.
    Returns the piecewise-constant states and the inspection findings."""
    states = []
    finds = []
    for z in Z.itertuples():
        g, a_fail, c, nfail_open = 1.0, 0, 0.0, 0
        n_la = max(z.n_la, 1)
        stolen = 0.0
        evs = E[E.zone_ix == z.zone_ix]
        insp = I[I.zone_ix == z.zone_ix]
        items = [(r.t, 0, r.kind, r.v) for r in evs.itertuples()] + \
                [(r.end + pd.Timedelta(hours=17), 1, 'inspect', r.round) for r in insp.itertuples()]
        items.sort(key=lambda x: (x[0], x[1]))
        states.append((z.zone_ix, pd.Timestamp('2016-01-01'), 1.0, 1.0, 0.0))
        for t, _, kind, v in items:
            if kind == 'theft':
                stolen = stolen + (1 - stolen) * v
                g = 1 - stolen
            elif kind == 'la_fail':
                a_fail += 1
            elif kind == 'crack':
                c = min(1.0, c + v)
            elif kind == 'inspect':
                ngr = z.n_tx + z.n_la
                missing = int(round(stolen * ngr))
                found_g = rng.binomial(missing, 0.9) if missing else 0
                found_a = rng.binomial(a_fail, 0.9) if a_fail else 0
                ncr = int(round(c * max(1, int((z.km_steel_xarm + z.km_bracket) * 2.5))))
                found_c = rng.binomial(ncr, 0.9) if ncr else 0
                finds.append(dict(zone_ix=z.zone_ix, round=v, t=t, grounds_missing=found_g, arresters_failed=found_a,
                                  insulators_cracked=found_c, grounds_total=ngr))
                stolen = stolen * (1 - (found_g / missing if missing else 1.0))
                g = 1 - stolen
                a_fail -= found_a
                c = c * (1 - (found_c / ncr if ncr else 1.0))
            a = 1 - a_fail / n_la if z.n_la > 0 else 1.0
            states.append((z.zone_ix, t, g, max(a, 0.0), c))
    St = pd.DataFrame(states, columns=['zone_ix', 't', 'g', 'a', 'c'])
    Fi = pd.DataFrame(finds)
    return St, Fi
