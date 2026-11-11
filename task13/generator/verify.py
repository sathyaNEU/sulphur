"""The independent verifier: reads only the shipped bundle (target/ and golden/), never the generator's world or its
analysis module, and recomputes every graded figure on its own code path (equirectangular distances from degrees,
its own trip grouping, a per-device drift found by voting over lag bins, a Poisson GLM by iteratively reweighted least
squares, the zones' own levels and the season scatter by marginal likelihood on its own Simpson grid, and each
record's chance under sound protection by exact convolution of its seasons rather than a moment-matched sum).
Exit 0 when every figure agrees.

    python3 task13/generator/verify.py [task folder]"""
import json
import math
import os
import sys

import numpy as np
import pandas as pd
from scipy import special

HERE = os.path.dirname(os.path.abspath(__file__))
SEASONS = [2022, 2023, 2024, 2025, 2026]
ALLS = list(range(2017, 2027))
REP = [ALLS.index(x) for x in SEASONS]


def files(folder):
    out = {}
    for n in os.listdir(folder):
        out[n.split('_')[0] + ('_' + n.split('_')[1] if n.startswith(('line_', 'oms_', 'scada_', 'protection_', 'cyclic_',
                                                                      'overhead_', 'recloser_', 'kidlat_', 'distribution_')) else '')] = os.path.join(folder, n)
    return out


def find(folder, prefix):
    hit = [n for n in os.listdir(folder) if n.startswith(prefix)]
    assert len(hit) == 1, (prefix, hit)
    return os.path.join(folder, hit[0])


def season(ts):
    m = ts.dt.month
    return np.where((m >= 4) & (m <= 10), ts.dt.year, -1)


def seg_dist(px, py, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    L2 = np.maximum(dx * dx + dy * dy, 1e-12)
    t = np.clip(((px - ax) * dx + (py - ay) * dy) / L2, 0, 1)
    return np.hypot(px - (ax + t * dx), py - (ay + t * dy))


def nb_logpmf(y, mu, k):
    return (special.gammaln(y + k) - special.gammaln(k) - special.gammaln(y + 1) + k * np.log(k / (k + mu))
            + y * np.log(mu / (k + mu)))


def nb_sf(x, mu, k):
    """P(X >= x) by summing the pmf below x"""
    if x <= 0:
        return 1.0
    ys = np.arange(0, x)
    if k > 1e8:
        lp = -mu + ys * math.log(mu) - special.gammaln(ys + 1)
    else:
        lp = nb_logpmf(ys, mu, k)
    return float(max(0.0, 1.0 - np.exp(lp).sum()))


def main(task):
    T = os.path.join(task, 'target')
    Gd = os.path.join(task, 'golden')
    zr = pd.read_excel(find(T, 'protection_zones'), sheet_name='Zones', header=3)
    zones = list(zr['Zone (protective device)'])
    zi = {z: i for i, z in enumerate(zones)}
    lat0 = 15.5
    kx = 111.32 * math.cos(math.radians(lat0))
    ky = 110.57
    gj = json.load(open(find(T, 'overhead_line_routes')))
    segs = []
    for f in gj['features']:
        c = np.array(f['geometry']['coordinates'])
        x = c[:, 0] * kx
        y = c[:, 1] * ky
        for i in range(len(c) - 1):
            segs.append((zi[f['properties']['zone']], x[i], y[i], x[i + 1], y[i + 1]))
    S = np.array(segs)
    st = pd.read_csv(find(T, 'kidlat_strokes'))
    st = st[st['type'] == 'G'].reset_index(drop=True)
    st['t'] = pd.to_datetime(st.datetime_utc.str[:-1]).astype('datetime64[ns]') + pd.Timedelta(hours=8)
    st['x'] = st.longitude * kx
    st['y'] = st.latitude * ky
    # strokes within 400 m of each zone: a coarse grid of segments by 2 km cells
    cell = 2.0
    from collections import defaultdict
    grid = defaultdict(list)
    for j, (z, ax, ay, bx, by) in enumerate(S):
        for gx in range(int(min(ax, bx) // cell) - 1, int(max(ax, bx) // cell) + 2):
            for gy in range(int(min(ay, by) // cell) - 1, int(max(ay, by) // cell) + 2):
                grid[(gx, gy)].append(j)
    near = []
    gxs = (st.x // cell).astype(int).values
    gys = (st.y // cell).astype(int).values
    keys = pd.Series(list(zip(gxs, gys)))
    for k, idx in keys.groupby(keys).groups.items():
        js = np.array(grid.get(k, []), dtype=int)
        if len(js) == 0:
            continue
        idx = np.asarray(list(idx))
        d = seg_dist(st.x.values[idx][:, None], st.y.values[idx][:, None], S[js, 1][None], S[js, 2][None], S[js, 3][None], S[js, 4][None])
        ii, jj = np.where(d <= 0.4)
        for a, b in zip(idx[ii], js[jj]):
            near.append((a, int(S[b, 0])))
    NS = pd.DataFrame(near, columns=['r', 'zone']).drop_duplicates()
    NS['t'] = st.t.values[NS.r.values]
    sc = pd.read_csv(find(T, 'scada_event'), dtype=str, keep_default_na=False)
    sc['zone'] = sc.point.str.rsplit(' ', n=1).str[0].map(zi)
    sc['ts'] = pd.to_datetime(sc.timestamp).astype('datetime64[ns]')
    dl = pd.read_csv(find(T, 'recloser_event'), dtype=str, keep_default_na=False)
    dl['zone'] = dl.recloser.map(zi)
    dl['ts'] = pd.to_datetime(dl.controller_time, format='%d/%m/%Y %H:%M:%S.%f').astype('datetime64[ns]')
    dl['read_at'] = pd.to_datetime(dl.read_at).astype('datetime64[ns]')
    dl['n'] = dl.event_no.astype(int)
    ev = pd.concat([sc[['zone', 'ts', 'event']].assign(event=sc.event.str.upper()),
                    dl.drop_duplicates(['recloser', 'n'])[['zone', 'ts', 'event']].assign(
                        event=lambda d: d.event.str.upper().replace({'TRIP': 'TRIP', 'RECLOSE': 'RECLOSE', 'LOCKOUT': 'LOCKOUT'}))])
    ev = ev[ev.event.isin(['TRIP', 'RECLOSE', 'LOCKOUT'])].sort_values(['zone', 'ts'])
    gap = ev.groupby('zone').ts.diff().dt.total_seconds()
    starts = ev[(ev.event == 'TRIP') & (gap.isna() | (gap > 40))][['zone', 'ts']].reset_index(drop=True)
    up = {zi[z]: zi.get(p, -1) for z, p in zip(zones, zr['Upstream device'].fillna(''))}
    starts = starts.sort_values('ts').reset_index(drop=True)
    keep = np.ones(len(starts), bool)
    tv = starts.ts.values
    zv = starts.zone.values
    for i in range(len(starts)):
        j = i + 1
        while j < len(starts) and tv[j] - tv[i] <= np.timedelta64(250, 'ms'):
            if up.get(zv[i]) == zv[j]:
                keep[j] = False
            if up.get(zv[j]) == zv[i]:
                keep[i] = False
            j += 1
    starts = starts[keep].reset_index(drop=True)
    radioless = {zi[z] for z, t in zip(zones, zr.Telemetry) if str(t).startswith('None')}
    reads = {zi[z]: np.sort(g.read_at.unique()) for z, g in dl.groupby('recloser')}
    # drift per radio-less controller: vote over rates for lags within 3 s of zero after each read, then refine
    off = np.zeros(len(starts))
    for z in radioless:
        sel = np.where(starts.zone.values == z)[0]
        if len(sel) == 0 or z not in reads:
            continue
        rs = reads[z]
        ns = np.sort(NS[NS.zone == z].t.values)
        tt = starts.ts.values[sel]
        k = np.searchsorted(rs, tt, side='right') - 1
        lags, taus, ks = [], [], []
        for t, kk in zip(tt, k):
            if kk < 0:
                continue
            lo, hi = np.searchsorted(ns, [t - np.timedelta64(900, 's'), t + np.timedelta64(900, 's')])
            d = (t - ns[lo:hi]) / np.timedelta64(1, 's')
            lags += list(d)
            taus += [(t - rs[kk]) / np.timedelta64(1, 'D')] * len(d)
            ks += [kk] * len(d)
        lags, taus, ks = np.array(lags), np.array(taus), np.array(ks)
        if len(lags) == 0:
            continue
        rates = np.arange(-5, 5.0001, 0.005)
        votes = [(np.abs(lags - r * taus) <= 3).sum() for r in rates]
        b = rates[int(np.argmax(votes))]
        a = {}
        for tol in (3.0, 1.0, 0.6):
            res = lags - b * taus - np.array([a.get(x, 0.0) for x in ks])
            m = np.abs(res) <= tol
            if m.sum() < 3:
                break
            u = np.unique(ks[m])
            X = np.column_stack([(ks[m] == x).astype(float) for x in u] + [taus[m]])
            coef = np.linalg.lstsq(X, lags[m], rcond=None)[0]
            a = {x: coef[i] for i, x in enumerate(u)}
            b = coef[-1]
        for i, t, kk in zip(sel, tt, k):
            off[i] = np.nan if kk < 0 else a.get(kk, 0.0) + b * (t - rs[kk]) / np.timedelta64(1, 'D')
    starts['corr'] = starts.ts - pd.to_timedelta(np.nan_to_num(off, nan=1e7), unit='s')
    starts['light'] = False
    nsz = {z: np.sort(g.t.values) for z, g in NS.groupby('zone')}
    for i, (z, c) in enumerate(zip(starts.zone.values, starts['corr'].values)):
        a = nsz.get(z)
        if a is None:
            continue
        j = np.searchsorted(a, c)
        best = None
        for q in (j - 1, j):
            if 0 <= q < len(a):
                d = (c - a[q]) / np.timedelta64(1, 's')
                if best is None or abs(d) < abs(best):
                    best = d
        starts.loc[i, 'light'] = best is not None and -0.6 <= best <= 0.7
    starts['season'] = season(starts.ts)
    # observed windows of the radio-less controllers
    cover = {}
    for rz, g in dl.groupby('recloser'):
        wins, pmax, pread = [], None, None
        for ra, gg in g.groupby('read_at'):
            mn = gg.n.min()
            st0 = gg.ts[gg.n.idxmin()] if (pmax is None or mn > pmax + 1) else pread
            wins.append((st0, ra))
            pmax = max(pmax or 0, gg.n.max())
            pread = ra
        cover[zi[rz]] = wins

    def observed(z, t, pad=0):
        if z not in cover:
            return np.ones(len(t), bool)
        ok = np.zeros(len(t), bool)
        for a0, a1 in cover[z]:
            ok |= (t >= np.datetime64(a0) - np.timedelta64(pad, 's')) & (t <= np.datetime64(a1) + np.timedelta64(pad, 's'))
        return ok
    NS['season'] = season(NS.t)
    NS['obs'] = True
    for z in cover:
        m = NS.zone.values == z
        NS.loc[m, 'obs'] = observed(z, NS.t.values[m])
    starts['obs'] = True
    for z in cover:
        m = starts.zone.values == z
        starts.loc[m, 'obs'] = observed(z, starts.ts.values[m], 400)
    nz = len(zones)
    ns = len(ALLS)
    Y = np.zeros((nz, ns))
    X = np.zeros((nz, ns))
    Xo = np.zeros((nz, ns))
    for i, s in enumerate(ALLS):
        a = starts[starts.light & starts.obs & (starts.season == s)].groupby('zone').size()
        Y[a.index.values.astype(int), i] = a.values
        b = NS[NS.season == s].groupby('zone').size()
        X[b.index.values.astype(int), i] = b.values
        c = NS[(NS.season == s) & NS.obs].groupby('zone').size()
        Xo[c.index.values.astype(int), i] = c.values
    km = zr['Overhead line km, three-phase'] + zr['Overhead line km, single-phase']
    cov = np.column_stack([np.ones(nz)] + [zr[c] / km for c in ['km tree-lined', 'km town', 'km hill', 'km steel crossarm',
                                                                 'km pole-top bracket', 'km bracket on concrete pole',
                                                                 'km fitted with line arresters (2015-16 programme)',
                                                                 'Distribution transformers']])
    ins = pd.read_excel(find(T, 'cyclic_line'), header=3)
    ins['zone'] = ins.Zone.map(zi)
    ins['start'] = pd.to_datetime(ins['Inspection start'])
    ins['done'] = pd.to_datetime(ins['Repairs completed'])
    ins['failed'] = ins[['Ground leads missing or cut', 'Arresters failed', 'Pin insulators cracked']].sum(axis=1) > 0
    ver = np.zeros((nz, ns), bool)
    for z, g in ins.sort_values('start').groupby('zone'):
        g = g.reset_index(drop=True)
        for i in range(len(g)):
            prev = g.done[i - 1] if i else pd.Timestamp('2016-01-01')
            if g.failed[i]:
                continue
            for j, s in enumerate(ALLS):
                if pd.Timestamp('%d-10-31' % s) < g.start[i] and pd.Timestamp('%d-04-01' % s) > prev:
                    ver[int(z), j] = True
    # Poisson GLM by IRLS on the verified zone-seasons
    rows = [(z, j) for z in range(nz) for j in range(ns) if ver[z, j] and Xo[z, j] > 0]
    A_ = np.array([cov[z] for z, j in rows])
    yv = np.array([Y[z, j] for z, j in rows])
    ofs = np.log(np.array([Xo[z, j] for z, j in rows]))
    beta = np.zeros(A_.shape[1])
    beta[0] = math.log(yv.sum() / np.exp(ofs).sum())
    for _ in range(100):
        eta = A_ @ beta + ofs
        mu = np.exp(eta)
        zt = eta - ofs + (yv - mu) / mu
        nb = np.linalg.solve(A_.T @ (A_ * mu[:, None]), A_.T @ (mu * zt))
        if np.max(np.abs(nb - beta)) < 1e-10:
            beta = nb
            break
        beta = nb
    rate = np.exp(cov @ beta)
    E = rate[:, None] * Xo
    Ef = rate[:, None] * X
    # the zones' own levels: gamma(a, a), season scatter NB(k), by marginal likelihood on a log grid (Simpson)
    ug = np.exp(np.linspace(math.log(0.01), math.log(15.0), 2001))
    h = (math.log(15.0) - math.log(0.01)) / 2000
    simp = np.ones(2001)
    simp[1:-1:2] = 4
    simp[2:-1:2] = 2
    lsw = np.log(simp * h / 3 * ug)          # Simpson weights in log u, times the Jacobian du = u dlog u
    grp = [(Y[z, ver[z] & (Xo[z] > 0)], E[z, ver[z] & (Xo[z] > 0)]) for z in range(nz) if (ver[z] & (Xo[z] > 0)).any()]

    def glog(a):
        return a * math.log(a) - special.gammaln(a) + (a - 1) * np.log(ug) - a * ug

    def mll(th):
        a, kk = math.exp(th[0]), math.exp(th[1])
        lp0 = glog(a) + lsw
        tot = 0.0
        for y, e in grp:
            lp = nb_logpmf(y[:, None], e[:, None] * ug[None, :], kk).sum(0) + lp0
            m = lp.max()
            tot += m + math.log(np.exp(lp - m).sum())
        return -tot
    from scipy import optimize
    r = optimize.minimize(mll, [math.log(5.0), math.log(30.0)], method='L-BFGS-B',
                          bounds=[(math.log(0.2), math.log(500.0)), (math.log(0.5), math.log(8000.0))])
    a_lv, k_lv = math.exp(r.x[0]), math.exp(r.x[1])
    alpha = 1.0 / (nz * 5)
    done = {z: np.sort(g.done.values) for z, g in ins.groupby('zone')}

    def window(z, s):
        d = done.get(z, np.array([], dtype='datetime64[ns]'))
        d = d[d < np.datetime64('%d-04-01' % s)]
        last = d.max() if len(d) else np.datetime64('2016-01-01')
        return [j for j, x in enumerate(ALLS) if x <= s and np.datetime64('%d-04-01' % x) > last]

    def post(z, W):
        js = [j for j in range(ns) if ver[z, j] and Xo[z, j] > 0 and j not in W]
        lp = glog(a_lv) + lsw
        if js:
            lp = lp + nb_logpmf(Y[z, js][:, None], E[z, js][:, None] * ug[None, :], k_lv).sum(0)
        w = np.exp(lp - lp.max())
        return w / w.sum()

    def sum_pmf(es, u, ymax):
        """the exact pmf of a sum of independent season NBs given the level u, by convolution"""
        pm = np.zeros(ymax + 1)
        pm[0] = 1.0
        ys = np.arange(ymax + 1)
        for e in es:
            q = np.exp(nb_logpmf(ys, max(e * u, 1e-12), k_lv))
            pm = np.convolve(pm, q)[:ymax + 1]
        return pm

    ucoarse = np.exp(np.linspace(math.log(0.01), math.log(15.0), 241))

    def pred_pmf(z, W, ymax):
        w = post(z, W)
        # the posterior on the coarse grid (mass gathered to the nearest coarse node)
        idx = np.clip(np.searchsorted(ucoarse, ug), 0, len(ucoarse) - 1)
        wc = np.bincount(idx, weights=w, minlength=len(ucoarse))
        es = [E[z, j] for j in W]
        out = np.zeros(ymax + 1)
        keep = wc > 1e-10
        for uu, ww in zip(ucoarse[keep], wc[keep] / wc[keep].sum()):
            out += ww * sum_pmf(es, uu, ymax)
        return out

    hist = {}
    tails = {}
    for s in SEASONS:
        ref = []
        for z in range(nz):
            W = window(z, s)
            e = E[z, W].sum()
            if not W or e <= 0:
                continue
            yobs = int(Y[z, W].sum())
            ymax = int(min(max(yobs + 25, 8 * e + 60), 3000))
            pm = pred_pmf(z, W, ymax)
            sf = 1 - np.concatenate([[0.0], np.cumsum(pm)[:-1]])
            tails[(s, z)] = sf
            if sf[yobs] < alpha:
                ref.append(z)
        hist[s] = ref
    out = {'referred_zones': sorted(zones[z] for z in hist[2026]), 'alerts': {str(s): len(hist[s]) for s in SEASONS}}
    out['hist'] = {str(s): sorted(zones[z] for z in hist[s]) for s in SEASONS}
    out['hist_p'] = {str(s): {zones[z]: float(tails[(s, z)][int(Y[z, window(z, s)].sum())]) for (ss, z) in tails if ss == s}
                     for s in SEASONS}
    Yf = np.where(E > 0, Y * Ef / np.where(E > 0, E, 1), Y)
    out['season_totals'] = {str(s): int(round(Yf[:, ALLS.index(s)].sum())) for s in SEASONS}
    j26 = ALLS.index(2026)
    out['radioless_2026'] = int(round(sum(Yf[z, j26] for z in radioless)))
    out['faults_2026'] = int(round(Yf[:, j26].sum()))
    eu = np.array([float((post(z, []) * ug).sum()) for z in range(nz)])
    out['sound_2026'] = int(round((eu * Ef[:, j26]).sum()))
    out['excess_2026'] = int(round(Yf[:, j26].sum() - (eu * Ef[:, j26]).sum()))
    av = 0.0
    for z in hist[2026]:
        xb = X[z, REP].mean()
        av += (Yf[z, j26] - eu[z] * Ef[z, j26]) * (xb / X[z, j26] if X[z, j26] > 0 else 0.0)
    out['avoided_average_season'] = int(round(av))
    vr = vc = vf = 0
    for r in ins[(ins.start >= '2022-11-01') & (ins.start < '2026-06-01')].itertuples():
        s = r.start.year if r.start.month >= 11 else r.start.year - 1
        refd = int(r.zone) in hist.get(s, [])
        vr += refd
        vc += refd and r.failed
        vf += r.failed
    out['validation_core'] = {'referred_inspected': int(vr), 'confirmed': int(vc), 'missed': int(vf - vc)}
    # the sound zones the rule refers in a season: each zone's tail at the smallest count it is referred at
    fp = []
    for s in SEASONS:
        tot = 0.0
        for (ss, z), sf in tails.items():
            if ss != s:
                continue
            ok = np.nonzero(sf < alpha)[0]
            tot += float(sf[ok[0]]) if len(ok) else 0.0
        fp.append(tot)
    out['false_per_season'] = float(np.mean(fp))
    # the golden CSV agrees with the recomputation
    g = pd.read_csv(os.path.join(Gd, 'lightning_referrals_2027.csv'))
    out['csv_referred'] = sorted(g[g.referred == 'yes'].zone)
    out['csv_season_totals'] = {str(s): int(round(g['lightning_faults_%d' % s].sum())) for s in SEASONS}
    return out


if __name__ == '__main__':
    task = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(HERE)
    got = main(task)
    F = json.load(open(os.path.join(HERE, 'figures.json')))
    bad = []
    for key in ('referred_zones', 'alerts', 'validation_core', 'radioless_2026', 'faults_2026', 'sound_2026',
                'excess_2026', 'avoided_average_season', 'false_per_season'):
        a, b = got[key], F[key]
        bd = F.get('bands', {}).get(key)
        if key == 'false_per_season':
            ok = abs(a - b) <= 0.01
        elif isinstance(bd, dict) and isinstance(a, dict):
            ok = all(bd[x][0] <= a[x] <= bd[x][1] for x in bd)
        elif key == 'alerts':
            ok = all(abs(a[x] - b[x]) <= 1 for x in b)
        elif isinstance(a, (int, float)):
            ok = abs(a - b) <= max(2, 0.01 * abs(b))
        elif isinstance(a, dict):
            ok = all(abs(a[x] - b[x]) <= 1 for x in b) if all(isinstance(v, (int, float)) for v in b.values()) else a == b
        else:
            ok = a == b
        print('%-24s %s  verifier %s  figures %s' % (key, 'OK  ' if ok else 'FAIL', a, b))
        bad += [] if ok else [key]
    for key in ('season_totals',):
        ok = all(abs(got[key][s] - F[key][s]) <= max(2, 0.01 * F[key][s]) for s in F[key])
        print('%-24s %s  verifier %s  figures %s' % (key, 'OK  ' if ok else 'FAIL', got[key], F[key]))
        bad += [] if ok else [key]
    ok = got['csv_referred'] == F['referred_zones']
    print('%-24s %s' % ('csv referred', 'OK' if ok else 'FAIL'))
    bad += [] if ok else ['csv_referred']
    print('verify:', 'PASS' if not bad else 'FAIL ' + ', '.join(bad))
    sys.exit(1 if bad else 0)
