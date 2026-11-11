"""Network geometry: substations, feeders, protection zones, line segments with setting and construction."""
import numpy as np
import pandas as pd

LAT0, LON0 = 15.25, 120.60
KX, KY = 107.25, 110.6          # km per degree of longitude (at 15.5 N) and latitude
W, H = 64.0, 60.0                # region in km

SETTINGS = ['open', 'treed', 'town', 'hill']
SHIELD = {'open': 0.12, 'treed': 0.55, 'town': 0.68, 'hill': 0.50}


def smooth_field(rng, n=6, scale=1.0):
    """a smooth random field on the region from a few cosine waves"""
    ks = rng.uniform(0.04, 0.16, size=(n, 2)) * rng.choice([-1, 1], size=(n, 2))
    ph = rng.uniform(0, 2 * np.pi, size=n)
    amp = rng.normal(0, 1, size=n) / np.sqrt(n)

    def f(x, y):
        x = np.asarray(x, float)
        y = np.asarray(y, float)
        out = np.zeros(np.broadcast(x, y).shape)
        for (kx, ky), p, a in zip(ks, ph, amp):
            out = out + a * np.cos(kx * x + ky * y + p)
        return out * scale
    return f


def build(seed):
    rng = np.random.default_rng(seed)
    # towns: substations sit in or near ten towns; three more market towns without a substation
    towns = []
    while len(towns) < 15:
        p = rng.uniform([5, 5], [W - 5, H - 5])
        if all(np.hypot(*(p - q)) > 10 for q in towns):
            towns.append(p)
    towns = np.array(towns)
    subs = towns[:12] + rng.normal(0, 0.8, size=(12, 2))
    town_r = rng.uniform(1.5, 3.0, size=15)
    hill = lambda x, y: np.clip(1.25 - (np.asarray(x) / 30.0) - (H - np.asarray(y)) / 80.0, 0, 1)   # west and north
    tree_f = smooth_field(rng, 7, 1.0)
    steel_f = smooth_field(rng, 5, 1.0)

    def setting_at(x, y):
        d = np.hypot(x - towns[:, 0], y - towns[:, 1])
        if (d < town_r).any():
            return 'town'
        if hill(x, y) > 0.35 + 0.15 * tree_f(x, y):
            return 'hill'
        return 'treed' if tree_f(x, y) > -0.05 else 'open'

    segs = []      # one row per 0.4 km segment
    zones = []
    feeders = []
    zid = 0
    for si, (sx, sy) in enumerate(subs):
        nf = int(rng.integers(3, 6))
        base = rng.uniform(0, 2 * np.pi)
        for fi in range(nf):
            theta = base + fi * 2 * np.pi / nf + rng.normal(0, 0.25)
            L = rng.uniform(13, 30)
            # trunk points every 0.4 km with a wandering heading, kept in the region
            pts = [(sx, sy)]
            hdg = theta
            for k in range(int(L / 0.4)):
                hdg += rng.normal(0, 0.10)
                x, y = pts[-1]
                nx, ny = x + 0.4 * np.cos(hdg), y + 0.4 * np.sin(hdg)
                if not (1 < nx < W - 1 and 1 < ny < H - 1):
                    hdg += np.pi / 2 * rng.choice([-1, 1])
                    nx, ny = x + 0.4 * np.cos(hdg), y + 0.4 * np.sin(hdg)
                    if not (1 < nx < W - 1 and 1 < ny < H - 1):
                        break
                pts.append((nx, ny))
            pts = np.array(pts)
            n = len(pts) - 1
            # recloser positions along the trunk (segment index where a new zone starts)
            cuts = [0]
            pos = rng.uniform(9, 17)
            while pos < n - 8:
                cuts.append(int(pos))
                pos += rng.uniform(11, 20)
            fid = len(feeders)
            feeders.append({'feeder_ix': fid, 'sub': si, 'n_zones': len(cuts)})
            zone_of_seg = np.searchsorted(cuts, np.arange(n), side='right') - 1
            zids = [zid + k for k in range(len(cuts))]
            for k in range(len(cuts)):
                zones.append({'zone_ix': zid + k, 'feeder_ix': fid, 'sub': si, 'order': k,
                              'kind': 'breaker' if k == 0 else 'recloser',
                              'parent_ix': (zid + k - 1) if k > 0 else -1})
            for j in range(n):
                segs.append((zids[zone_of_seg[j]], pts[j, 0], pts[j, 1], pts[j + 1, 0], pts[j + 1, 1], 3))
            # laterals off the trunk, every ~1.2 km on average
            j = 1
            while j < n - 1:
                if rng.random() < 0.38:
                    lz = zids[zone_of_seg[j]]
                    lat_len = min(7.0, rng.exponential(1.9) + 0.4)
                    side = rng.choice([-1, 1])
                    h2 = np.arctan2(pts[j + 1, 1] - pts[j, 1], pts[j + 1, 0] - pts[j, 0]) + side * rng.uniform(0.9, 1.9)
                    p = pts[j].copy()
                    for k in range(max(1, int(lat_len / 0.4))):
                        h2 += rng.normal(0, 0.15)
                        q = p + 0.4 * np.array([np.cos(h2), np.sin(h2)])
                        if not (0.5 < q[0] < W - 0.5 and 0.5 < q[1] < H - 0.5):
                            break
                        segs.append((lz, p[0], p[1], q[0], q[1], 1))
                        p = q
                j += 1
            zid += len(cuts)
    S = pd.DataFrame(segs, columns=['zone_ix', 'x0', 'y0', 'x1', 'y1', 'phases'])
    S['xm'] = (S.x0 + S.x1) / 2
    S['ym'] = (S.y0 + S.y1) / 2
    S['km'] = np.hypot(S.x1 - S.x0, S.y1 - S.y0)
    S['setting'] = [setting_at(x, y) for x, y in zip(S.xm, S.ym)]
    # construction: three-phase trunk either wood or steel crossarm (steel where rebuilt after typhoons),
    # single-phase laterals on a pole-top bracket; concrete poles in towns
    stl = steel_f(S.xm.values, S.ym.values)
    cons = np.where(S.phases == 3, np.where(stl > -0.25, 'steel_xarm', 'wood_xarm'), 'bracket')
    cons = np.where((S.setting == 'town') & (S.phases == 1), 'concrete_bracket', cons)
    S['construction'] = cons
    S['cfo'] = S.construction.map({'wood_xarm': 290.0, 'steel_xarm': 140.0, 'bracket': 135.0,
                                   'concrete_bracket': 115.0})
    S['height'] = np.where(S.phases == 3, 11.0, 9.6)
    S['tx_per_km'] = S.setting.map({'town': 3.2, 'treed': 1.3, 'open': 0.7, 'hill': 0.45})
    Z = pd.DataFrame(zones)
    F = pd.DataFrame(feeders)
    return dict(S=S, Z=Z, F=F, towns=towns, town_r=town_r, subs=subs, hill=hill)


if __name__ == '__main__':
    N = build(1302)
    S, Z = N['S'], N['Z']
    print(len(Z), 'zones', len(N['F']), 'feeders', len(S), 'segments', round(S.km.sum()), 'km')
    km = S.groupby('zone_ix').km.sum()
    print(km.describe().round(1))
    print(S.groupby('setting').km.sum().round(0))
    print(S.groupby('construction').km.sum().round(0))
