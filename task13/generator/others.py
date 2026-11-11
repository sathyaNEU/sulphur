"""Faults that are not lightning: storm winds through trees (on the same storms as the lightning), typhoons,
animals, vegetation, equipment, vehicles and kites, and the line arresters of lot B failing short; and the
transformers that burn out when a strike lands near an unprotected one."""
import numpy as np
import pandas as pd

import faults as FA
import geo as G
import net as NET

CAUSES_BG = [('animal', 0.30), ('vegetation', 0.22), ('equipment', 0.20), ('third_party', 0.10), ('unknown', 0.18)]


def storm_wind(N, Z, Fl, rng):
    """a gust front puts branches and bamboo on the line while the cell passes: a fault at a time near some
    flash of that cell, on zones the cell passes close to, more where the line runs through trees"""
    S = N['S']
    idx = G.SegIndex(S, 2.0)
    first = Fl
    p, s, d = idx.near(first.x.values, first.y.values, 1.5)
    P = pd.DataFrame({'fl': p, 'zone_ix': S.zone_ix.values[s], 'd': d}).sort_values('d').drop_duplicates(['fl', 'zone_ix'])
    veg = Z.set_index('zone_ix').veg.reindex(P.zone_ix).values
    pw = 0.0045 * veg
    hit = rng.random(len(P)) < pw
    P = P[hit]
    t = first.t.values[P.fl.values] + pd.to_timedelta(rng.normal(0, 240, len(P)), unit='s')
    out = pd.DataFrame({'zone_ix': P.zone_ix.values, 't': t, 'cause': 'storm_wind'})
    return out


def typhoon(Z, rng):
    rows = []
    for name, t0, hrs, inten in FA.TYPHOONS:
        t0 = pd.Timestamp(t0)
        for z in Z.itertuples():
            lam = inten * z.km / 10.0 * (0.5 + z.veg) * 0.22
            n = rng.poisson(lam)
            for k in range(n):
                rows.append((z.zone_ix, t0 + pd.Timedelta(hours=float(rng.uniform(-0.4, 1.0) * hrs)), 'typhoon', name))
    return pd.DataFrame(rows, columns=['zone_ix', 't', 'cause', 'event'])


def background(Z, t0, t1, rng):
    rows = []
    days = (t1 - t0).days
    for z in Z.itertuples():
        lam = 0.16 * z.km * (0.6 + 0.5 * z.veg) * days / 365.25
        n = rng.poisson(lam)
        ts = t0 + pd.to_timedelta(rng.uniform(0, days, n), unit='D')
        # daytime heavier (animals, vehicles, kites), a little seasonality
        hrs = np.where(rng.random(n) < 0.65, rng.normal(13, 3.5, n), rng.uniform(0, 24, n)) % 24
        ts = ts.normalize() + pd.to_timedelta(hrs, unit='h')
        cs = rng.choice([c for c, _ in CAUSES_BG], n, p=[w for _, w in CAUSES_BG])
        for t, c in zip(ts, cs):
            rows.append((z.zone_ix, t, c))
    return pd.DataFrame(rows, columns=['zone_ix', 't', 'cause'])


def arrester_faults(E, rng):
    """a lot B arrester that fails short faults its zone: mostly in wet weather, any hour"""
    f = E[E.kind == 'la_fault']
    t = f.t.values
    return pd.DataFrame({'zone_ix': f.zone_ix.values, 't': t, 'cause': 'arrester'})
