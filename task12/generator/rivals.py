"""Every route a competent analyst could take, run on the shipped files through golden.panel(): the default path
(Parfitt-Collins with its textbook caveats), each rung of the ladder, the routes that read the settled level off the
weekly series, and every member of the golden family. checks.py asserts where each lands."""
import numpy as np
from scipy.optimize import curve_fit

import golden as G

T_LYG = 139       # 2026-W36


def wk(y, w):
    import datetime as dt
    return G.week_of(dt.date.fromisocalendar(y, w, 1))


def share_weeks(D, a, b, mask=None):
    m = D['buyer'] if mask is None else mask
    w = D['H']['w2026'].fillna(0).values
    num = (D['nvl'][a:b + 1, :][:, m].sum(0) * w[m]).sum()
    den = (D['cat'][a:b + 1, :][:, m].sum(0) * w[m]).sum()
    return num / den


def run(target=None, D=None):
    D = D or G.panel(target)
    w = D['H']['w2026'].fillna(0).values
    st, buyer, first = D['static'], D['buyer'], D['first']
    triers = buyer & (first >= 0)
    out = {}
    L27, g = G.litres27(D, 'v2425')
    Lwin, _ = G.litres27(D, 'vwin')
    recent = (wk(2026, 38), G.END_T)
    cr = D['cat'][recent[0]:recent[1] + 1].sum(0)
    nr = D['nvl'][recent[0]:recent[1] + 1].sum(0)
    mature = triers & (first <= G.LAUNCH_T + 3)
    R_mat = (nr * w)[mature].sum() / (cr * w)[mature].sum()
    R_cur = (nr * w)[triers].sum() / (cr * w)[triers].sum()
    P = (w * triers)[buyer].sum() / w[buyer].sum()
    cwin = D['cat'][G.LAUNCH_T:G.END_T + 1].sum(0)
    B_win = (w * cwin)[triers].sum() / w[triers].sum() / ((w * cwin)[buyer].sum() / w[buyer].sum())
    out.update(P=P, R_mat=R_mat, R_cur=R_cur, B_win=B_win)
    out['pc_careful'] = P * R_mat * B_win                 # the default path
    out['pc_naive'] = P * R_cur * B_win
    out['pc_B1'] = P * R_mat
    out['recent_share'] = share_weeks(D, *recent)

    def carry(level, vol):
        return (w * np.where(triers, level, 0.0) * vol)[st].sum() / (w * vol)[st].sum()
    out['april_for_all'] = carry(R_mat, L27)
    # each four-week first-purchase cohort at its own recent share
    rc = np.zeros(D['n'])
    for c0 in range(G.LAUNCH_T, G.END_T + 1, 4):
        m = triers & (first >= c0) & (first < c0 + 4)
        if (cr * w)[m].sum() > 0:
            rc[m] = (nr * w)[m].sum() / (cr * w)[m].sum()
    out['cohort_own_recent'] = carry(rc, L27)
    out['cohort_own_recent_win'] = carry(rc, Lwin)
    # each cohort's own fitted fade, its asymptote
    fl_c = np.zeros(D['n'])
    for c0 in range(G.LAUNCH_T, G.END_T + 1, 4):
        m = triers & (first >= c0) & (first < c0 + 4)
        if m.sum() < 15:
            continue
        ks, ys, ws = [], [], []
        for t in range(c0, G.END_T + 1):
            if t in D['promo']:
                continue
            mm = m & (t - first >= 1)
            den = (D['cat'][t] * w)[mm].sum()
            if den <= 0:
                continue
            ks.append(float(np.average(t - first[mm], weights=w[mm]))); ys.append((D['nvl'][t] * w)[mm].sum() / den); ws.append(den)
        ks, ys, ws = np.array(ks), np.array(ys), np.array(ws)
        try:
            f = lambda k, a, b, c: a + (b - a) * np.exp(-k / c)
            (a, b, c), _ = curve_fit(f, ks, ys, p0=(ys[-1], ys[0], 4.0), sigma=1 / np.sqrt(ws),
                                     bounds=([0, 0, 0.3], [1, 1, 40]), maxfev=20000)
        except Exception:
            a = ys[-2:].mean()
        fl_c[m] = a
    out['cohort_fitted_fade'] = carry(fl_c, L27)
    # the settled level read off the weekly series
    out['quiet_w19_w23'] = share_weeks(D, wk(2026, 19), wk(2026, 23))
    out['quiet_w27_w38'] = share_weeks(D, wk(2026, 27), wk(2026, 38))
    out['quiet_w31_w38'] = share_weeks(D, wk(2026, 31), wk(2026, 38))
    out['last_week'] = share_weeks(D, G.END_T, G.END_T)
    out['last_4_weeks'] = share_weeks(D, G.END_T - 3, G.END_T)
    # unsupported-week share raised to the review's distribution (stocking share of the buyers' banners)
    out['quiet_scaled_to_distribution'] = out['quiet_w19_w23'] * dist_ratio(D)
    # the golden family and the volume dial
    for how in ('terciles', 'gaps', 'q30'):
        tier, _ = G.tiers(D, how)
        for k_min in (14, 16, 20):
            fl, _ = G.settled(D, tier, k_min)
            for base in ('v2425', 'v2025', 'vall', 'v52', 'vwin'):
                vol, _ = G.litres27(D, base)
                out[('family', how, k_min, base)] = carry(fl[tier], vol)
    # k-means on log price per litre
    tier_k = kmeans_tiers(D)
    for k_min in (14, 16, 20):
        fl, _ = G.settled(D, tier_k, k_min)
        out[('family', 'kmeans', k_min, 'v2425')] = carry(fl[tier_k], L27)
        out[('family', 'kmeans', k_min, 'vwin')] = carry(fl[tier_k], Lwin)
    # unweighted (the projection factors left out)
    tier, _ = G.tiers(D, 'terciles')
    fl, _ = G.settled(D, tier)
    out['unweighted'] = (np.where(triers, fl[tier], 0.0) * L27)[st].sum() / L27[st].sum()
    return out, D


def kmeans_tiers(D):
    ppl, buyer = D['ppl'], D['buyer']
    ok = buyer & np.isfinite(ppl)
    x = np.log(ppl[ok])
    c = np.quantile(x, [0.17, 0.5, 0.83])
    for _ in range(60):
        lab = np.argmin(np.abs(x[:, None] - c[None, :]), 1)
        c = np.array([x[lab == j].mean() for j in range(3)])
    order = np.argsort(-c)
    allx = np.log(np.where(np.isfinite(ppl), ppl, np.exp(c[order[1]])))
    lab = np.argmin(np.abs(allx[:, None] - c[None, :]), 1)
    rank = {int(o): r for r, o in enumerate(order)}
    return np.array([rank[int(l)] for l in lab])


def dist_ratio(D):
    """the buyers' share of category litres bought where the line was stocked at the review, over the same share in
    2026-W19 to W23, from the purchase lines and the retail audit's weighted distribution"""
    import os
    import pandas as pd
    import common as C
    A = pd.read_csv(os.path.join(C.TARGET, C.FILES['distribution']), dtype={'item_code': str})
    A['t'] = [G.week_of(__import__('datetime').date.fromisoformat(x)) - 0 for x in A['week_ending']]
    wd = A.groupby(['t', 'banner_cd'])['wtd_dist_pct'].mean() / 100.0
    P = D['P']
    base = P[(P['t'] <= G.PRE_END_T) & D['buyer'][P['i'].values]].groupby('banner')['litres'].sum()
    mix = base / base.sum()

    def stock(t):
        return sum(mix.get(b, 0) * wd.get((t, b), 0.0) for b in mix.index)
    review = stock(G.END_T + 0)
    quiet = np.mean([stock(t) for t in range(wk(2026, 19), wk(2026, 23) + 1)])
    return review / quiet if quiet > 0 else np.nan


def waves_of(D):
    first = D['first']
    tr = D['buyer'] & (first >= 0)
    return [tr & (first <= wk(2026, 23)), tr & (first >= wk(2026, 24)) & (first < T_LYG), tr & (first >= T_LYG)]


def per_wave(D, k_min, src):
    """each wave at its own share of its litres in unpromoted weeks from k_min weeks after first purchase; the Loyal
    Grocer wave, too young for that, at the April wave's level, the discounter wave's, or their mean"""
    w = D['H']['w2026'].fillna(0).values
    first, st = D['first'], D['static']
    wv = waves_of(D)
    lev = []
    for m in wv[:2]:
        num = den = 0.0
        for t in range(G.LAUNCH_T, G.END_T + 1):
            if t in D['promo']:
                continue
            mm = m & (t - first >= k_min)
            num += D['nvl'][t, mm].sum(); den += D['cat'][t, mm].sum()
        lev.append(num / den)
    lyg = {'april': lev[0], 'discounter': lev[1], 'mean': (lev[0] + lev[1]) / 2}[src]
    level = np.where(wv[0], lev[0], 0.0) + np.where(wv[1], lev[1], 0.0) + np.where(wv[2], lyg, 0.0)
    L27, _ = G.litres27(D)
    return (w * level * L27)[st].sum() / (w * L27)[st].sum()


def unsupported_trial(D, tier, floors):
    """2027 first purchases at the everyday rate of the latest unsupported weeks, carried at each group's settled share"""
    w = D['H']['w2026'].fillna(0).values
    first, buyer, st = D['first'], D['buyer'], D['static']
    weeks = [wk(2026, 43), wk(2026, 44)]
    add = 0.0
    L27, _ = G.litres27(D)
    for k in range(3):
        at = buyer & (tier == k)
        risk = sum((w * (at & ((first < 0) | (first >= t)))).sum() for t in weeks)
        hit = sum((w * (at & (first == t))).sum() for t in weeks)
        h = hit / risk if risk else 0.0
        untried = at & (first < 0)
        add += floors[k] * (w * L27)[untried].sum() * (1 - (1 - h) ** 60) * 0.5
    return add / (w * L27)[st].sum()


if __name__ == '__main__':
    import common as C
    out, D = run(C.TARGET)
    for k, v in out.items():
        if not isinstance(k, tuple):
            print('%-28s %.3f%s' % (k, 100 * v if k not in ('B_win',) else v, '' if k in ('B_win',) else '%'))
    fam = {k: v for k, v in out.items() if isinstance(k, tuple)}
    for how in ('terciles', 'gaps', 'q30', 'kmeans'):
        print(how, ' '.join('k%d/%s=%.2f' % (k[2], k[3], 100 * v) for k, v in fam.items() if k[1] == how))
