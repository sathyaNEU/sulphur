"""Thunderstorm cells, their cloud-to-ground flashes and strokes (true), and the lightning location network's
records of them (detected, with location error, current error, sensor count and cloud pulses)."""
import numpy as np
import pandas as pd

import net as NET

MONTH_W = np.array([0.020, 0.018, 0.028, 0.068, 0.128, 0.138, 0.130, 0.128, 0.132, 0.093, 0.075, 0.042])
SEASON_MULT = {2016: 1.0, 2017: 0.94, 2018: 1.07, 2019: 0.89, 2020: 1.03, 2021: 0.97, 2022: 1.00, 2023: 0.87, 2024: 1.09,
               2025: 0.93, 2026: 1.16}


def ng_rel(N):
    rng = np.random.default_rng(77)
    f = NET.smooth_field(rng, 5, 0.22)
    return lambda x, y: 1.0 + 0.55 * N['hill'](x, y) + f(x, y)


def simulate(N, seed, start='2021-12-01', end='2026-11-01', annual=21000.0):
    rng = np.random.default_rng(seed)
    ngr = ng_rel(N)
    days = pd.date_range(start, end, freq='D', inclusive='left')
    z = 0.0
    cells = []
    for d in days:
        z = 0.72 * z + rng.normal(0, 0.62)
        mult = SEASON_MULT[d.year] * MONTH_W[d.month - 1] * 12 / 1.0
        F = annual / 365.0 * mult * np.exp(z - 0.5 * 0.62 ** 2 / (1 - 0.72 ** 2))
        nc = rng.poisson(F / 70.0)
        for _ in range(nc):
            # start hour: afternoon convection, some nocturnal monsoon storms
            hr = rng.normal(15.3, 2.2) if rng.random() < 0.8 else rng.uniform(0, 24)
            hr = hr % 24
            # genesis weighted by the flash density field, over the region plus a margin
            while True:
                x, y = rng.uniform(-8, NET.W + 8), rng.uniform(-8, NET.H + 8)
                if rng.random() < ngr(x, y) / 1.9:
                    break
            if d.month in (6, 7, 8, 9):
                hdg = np.deg2rad(rng.normal(55, 25))
            else:
                hdg = np.deg2rad(rng.normal(215, 35))
            cells.append(dict(t0=d + pd.Timedelta(hours=hr), x0=x, y0=y, hdg=hdg,
                              v=rng.uniform(8, 28), dur=rng.lognormal(np.log(55), 0.45),
                              nfl=max(3, int(rng.lognormal(np.log(52), 0.75))), sig=rng.uniform(1.4, 4.0)))
    C = pd.DataFrame(cells)
    # flashes
    rows = []
    for ci, c in enumerate(cells):
        n = c['nfl']
        u = rng.beta(2.0, 2.6, size=n)
        tmin = u * c['dur']
        cx = c['x0'] + c['v'] * tmin / 60 * np.cos(c['hdg'])
        cy = c['y0'] + c['v'] * tmin / 60 * np.sin(c['hdg'])
        fx = cx + rng.normal(0, c['sig'], size=n)
        fy = cy + rng.normal(0, c['sig'], size=n)
        keep = (fx > -2) & (fx < NET.W + 2) & (fy > -2) & (fy < NET.H + 2)
        for k in np.where(keep)[0]:
            rows.append((ci, c['t0'] + pd.Timedelta(minutes=float(tmin[k])), fx[k], fy[k]))
    Fl = pd.DataFrame(rows, columns=['cell', 't', 'x', 'y']).sort_values('t').reset_index(drop=True)
    Fl['flash'] = np.arange(len(Fl))
    nF = len(Fl)
    neg = rng.random(nF) < 0.9
    I1 = np.where(neg, -rng.lognormal(np.log(31), 0.48, nF), rng.lognormal(np.log(38), 0.7, nF))
    mult = np.where(neg, 1 + rng.poisson(1.7, nF), 1 + (rng.random(nF) < 0.2))
    # strokes
    st = []
    for i in range(nF):
        t = Fl.t.iat[i]
        x, y = Fl.x.iat[i], Fl.y.iat[i]
        st.append((i, 0, t, x, y, I1[i], True))
        tt = t
        for k in range(1, mult[i]):
            tt = tt + pd.Timedelta(seconds=float(rng.lognormal(np.log(0.055), 0.65)))
            if rng.random() < 0.35:
                r = rng.exponential(1.3)
                a = rng.uniform(0, 2 * np.pi)
                xs, ys, newc = x + r * np.cos(a), y + r * np.sin(a), True
            else:
                xs, ys, newc = x, y, False
            Ik = -rng.lognormal(np.log(12), 0.53) if I1[i] < 0 else rng.lognormal(np.log(20), 0.6)
            st.append((i, k, tt, xs, ys, Ik, newc))
    St = pd.DataFrame(st, columns=['flash', 'k', 't', 'x', 'y', 'I', 'new_contact'])
    St['stroke'] = np.arange(len(St))
    return C, Fl, St


def detect(St, Fl, seed):
    """the lightning location network's records: ground strokes detected by current, with location and current
    error; cloud pulses near each flash, some classified as ground strokes"""
    rng = np.random.default_rng(seed)
    n = len(St)
    I = St.I.abs().values
    de = 1 / (1 + np.exp(-(np.log(I) - np.log(4.0)) / 0.30))
    det = rng.random(n) < de
    D = St[det].copy()
    m = len(D)
    a = rng.lognormal(np.log(0.15), 0.45, m)
    b = a * rng.uniform(0.35, 0.9, m)
    az = rng.uniform(0, np.pi, m)
    e1 = rng.normal(0, 1, m) * a / 1.1774
    e2 = rng.normal(0, 1, m) * b / 1.1774
    D['rx'] = D.x + e1 * np.cos(az) - e2 * np.sin(az)
    D['ry'] = D.y + e1 * np.sin(az) + e2 * np.cos(az)
    D['rI'] = np.round(D.I * rng.lognormal(0, 0.12, m), 1)
    D['major'] = np.round(a, 2)
    D['minor'] = np.round(np.maximum(b, 0.05), 2)
    D['azim'] = np.round(np.rad2deg(az), 0)
    D['sensors'] = 2 + rng.poisson(np.clip(3 + 0.25 * I[det], 3, 11))
    D['type'] = 'G'
    D['rt'] = D.t + pd.to_timedelta(rng.normal(0, 2e-6, m), unit='s')
    # cloud pulses: some reported as cloud, a few small positive ones reported as ground strokes
    nF = len(Fl)
    nic = rng.poisson(0.45, nF)
    idx = np.repeat(np.arange(nF), nic)
    k = len(idx)
    IC = pd.DataFrame({'flash': idx, 'k': -1, 't': Fl.t.values[idx] + pd.to_timedelta(rng.uniform(-0.6, 0.4, k), unit='s'),
                       'x': Fl.x.values[idx] + rng.normal(0, 2.0, k), 'y': Fl.y.values[idx] + rng.normal(0, 2.0, k)})
    IC['I'] = rng.choice([-1, 1], k, p=[0.4, 0.6]) * rng.lognormal(np.log(6.5), 0.45, k)
    IC['new_contact'] = False
    IC['stroke'] = -1
    a = rng.lognormal(np.log(0.45), 0.5, k)
    b = a * rng.uniform(0.3, 0.9, k)
    az = rng.uniform(0, np.pi, k)
    IC['rx'] = IC.x + rng.normal(0, 1, k) * a / 1.1774
    IC['ry'] = IC.y + rng.normal(0, 1, k) * b / 1.1774
    IC['rI'] = np.round(IC.I * rng.lognormal(0, 0.15, k), 1)
    IC['major'] = np.round(a, 2)
    IC['minor'] = np.round(np.maximum(b, 0.05), 2)
    IC['azim'] = np.round(np.rad2deg(az), 0)
    IC['sensors'] = 2 + rng.poisson(2.5, k)
    IC['type'] = np.where((IC.I > 0) & (rng.random(k) < 0.22), 'G', 'C')
    IC['rt'] = IC.t
    R = pd.concat([D, IC], ignore_index=True).sort_values('rt').reset_index(drop=True)
    return R
