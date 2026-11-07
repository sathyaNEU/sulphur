"""Every route a careful analyst could take to the expected twelfth-month members, priced on the shipped pack.

Imported by checks.py (R3a, R3b, R4, R5, R6) and ceiling.py. Each function takes the golden run R and returns the
expected number of twelfth-month members among the campaign members.
"""
import os
import sys
from collections import defaultdict

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import golden as G            # noqa: E402
from common import *          # noqa: E402,F401,F403


def _alive_last(R):
    mem = R['P']['mem'].set_index('member_id')['status'].to_dict()
    last = R['panel'][R['panel'].member_id.isin(set(R['members']))].sort_values('k').groupby('member_id').last()
    return mem, last


def curve_route(R, hfun, label=None):
    """Project each live campaign member on a membership-month curve: hfun(member, k, calendar month) -> month's cancel."""
    mem, last = _alive_last(R)
    tot = 0.0
    for m in R['members']:
        r = last.loc[m]
        if mem.get(m) != 'active' or r['t'] != G.CUT_M:
            tot += 1.0 if r['k'] >= 12 else 0.0
            continue
        s = 1.0
        for step, k in enumerate(range(int(r['k']) + 1, 12), start=1):
            t = int(r['t']) + step
            s *= 1 - hfun(m, k, (t % 12) + 1)
        tot += s
    return tot


def r0_curve(R, panel=None):
    p = R['panel'] if panel is None else panel
    h = G.kcurve(p)
    return curve_route(R, lambda m, k, cm: h[min(k, G.KMAX)])


def r0_recent(R):
    return r0_curve(R, R['panel'][R['panel'].t >= G.month_index(2026, 1)])


def r1_season(R):
    p = R['panel']; h = G.kcurve(p); se = G.season(p, h)
    return curve_route(R, lambda m, k, cm: h[min(k, G.KMAX)] * se.get(cm, 1.0))


def _engagement_band(R):
    l = R['l']
    lm = l.assign(comp=l.lessons_completed.astype(int), book=l.lessons_booked.astype(int))
    g = lm.groupby('member_id')[['comp', 'book']].sum()
    share = (g['comp'] / g['book'].clip(lower=1))
    return pd.cut(share, [-1, .7, .9, 2], labels=['low', 'mid', 'high']).astype(str).to_dict()


def r1_engagement(R):
    p = R['panel'].copy(); band = _engagement_band(R)
    p['band'] = p.member_id.map(band)
    h = G.kcurve(p)
    exp = p['k'].clip(upper=G.KMAX).map(h)
    ratio = (p['c'].groupby(p['band']).sum() / exp.groupby(p['band']).sum()).to_dict()
    return curve_route(R, lambda m, k, cm: min(.95, h[min(k, G.KMAX)] * ratio.get(band.get(m), 1.0)))


def r0_frailty(R):
    p = R['panel']; h = G.kcurve(p)
    own = p[p.member_id.isin(set(R['members']))]
    ratio = own['c'].sum() / own['k'].clip(upper=G.KMAX).map(h).sum()
    return curve_route(R, lambda m, k, cm: min(.95, h[min(k, G.KMAX)] * ratio)), float(ratio)


def r0_sbg(R):
    from scipy.optimize import minimize
    h = G.kcurve(R['panel'])
    ks = np.arange(1, 25); hk = np.array([h[k] for k in ks])
    f = lambda a, b, k: a / (a + b + k - 1)
    o = minimize(lambda q: ((np.array([f(*np.exp(q), k) for k in ks]) - hk) ** 2).sum(), [0.0, 1.0], method='Nelder-Mead')
    a, b = np.exp(o.x)
    return curve_route(R, lambda m, k, cm: f(a, b, k)), (float(a), float(b))


def r2_already_stopped(R):
    p = R['panel']; h = G.kcurve(p); par = R['par']
    mem, last = _alive_last(R)
    tot = 0.0
    for m in R['members']:
        r = last.loc[m]
        if mem.get(m) != 'active' or r['t'] != G.CUT_M:
            tot += 1.0 if r['k'] >= 12 else 0.0
            continue
        s = 1.0
        for step, k in enumerate(range(int(r['k']) + 1, 12), start=1):
            hk = h[min(k, G.KMAX)]
            if r['state'] == 'S1' and step == 1:
                hk = G.shock(hk, par['d2'], par['base'])
            s *= 1 - hk
        tot += s
    return tot


def linked(R, qfun=None, **kw):
    par = R['par']
    q = qfun or R['qf']
    e, _, _ = G.project_group(R['panel'], R['P']['mem'], R['members'], par, q, **kw)
    return e


def linked_pooled(R, rate):
    return linked(R, qfun=lambda j: rate)


def linked_smoothed(R):
    q = R['par']['q']
    sm = {}
    for j in range(1, 13):
        win = [q[i] for i in (j - 1, j, j + 1) if 1 <= i <= 12]
        sm[j] = sum(win) / len(win)
    return linked(R, qfun=lambda j: sm[j] if j <= 12 else q['late'])


def linked_double_count(R):
    """The all-cause membership-month curve with the stop shocks added on top (stops counted twice)."""
    par = dict(R['par'])
    par['h'] = G.kcurve(R['panel'])
    return linked(R) if False else G.project_group(R['panel'], R['P']['mem'], R['members'], par, R['qf'])[0]


def snapshot_logit(R, form='banded', since=None):
    """P(pays a twelfth charge | alive after paid month k0 in 1..3, the tutor's teaching month) fitted on members whose
    twelfth charge falls by the cut (joined from month `since`, if given), applied to the live campaign members."""
    import statsmodels.formula.api as smf
    p = R['panel']
    lastk = p.groupby('member_id')['k'].max()
    alive = R['P']['mem'].set_index('member_id')['status']
    snap = p[(p.k >= 1) & (p.k <= 3) & (p.c == 0)].copy()
    snap = snap[(snap.t - snap.k + 12) <= G.CUT_M]
    if since is not None:
        snap = snap[(snap.t - snap.k + 1) >= since]
    snap['y'] = (snap.member_id.map(lastk) >= 12).astype(int)
    bins = [-2, -1, 2, 8, 12, 999]; labs = ['none', '0-2', '3-8', '9-12', '13+']
    snap['band'] = pd.cut(snap.tj, bins, labels=labs).astype(str); snap['tt'] = snap.tj.clip(lower=0)
    f = {'banded': 'y ~ C(k) + C(band)', 'linear': 'y ~ C(k) + tt', 'log': 'y ~ C(k) + np.log1p(tt)'}[form]
    md = smf.logit(f, data=snap).fit(disp=0)
    mem, last = _alive_last(R)
    rows = []
    tot = 0.0
    for m in R['members']:
        r = last.loc[m]
        if mem.get(m) != 'active' or r['t'] != G.CUT_M:
            tot += 1.0 if r['k'] >= 12 else 0.0
            continue
        rows.append(dict(k=min(int(r['k']), 3), tj=int(r['tj'])))
    a = pd.DataFrame(rows)
    a['band'] = pd.cut(a.tj, bins, labels=labs).astype(str); a['tt'] = a.tj.clip(lower=0)
    tot += float(md.predict(a).sum())
    return tot, float(md.llf)


def stratified_at_match(R, since=None):
    """Twelfth-charge share of past members (joined from month `since`, if given) by whether their first tutor was in
    their first three months of teaching, mixed to the campaign members' own split."""
    p = R['panel']
    first = p[p.k == 1].set_index('member_id')
    lastk = p.groupby('member_id')['k'].max()
    done = first[(first.t + 11) <= G.CUT_M].copy()
    if since is not None:
        done = done[done.t >= since]
    done['y'] = (done.index.map(lastk) >= 12).astype(int)
    done['young'] = (done.tj >= 0) & (done.tj <= 2)
    camp = first.loc[[m for m in R['members'] if m in first.index]]
    ys = ((camp.tj >= 0) & (camp.tj <= 2)).mean()
    return len(R['members']) * (ys * done[done.young].y.mean() + (1 - ys) * done[~done.young].y.mean())


def linked_window(R, tutors_from=None, months_from=None):
    """The golden's projection with its inputs estimated on later tutors or later months only."""
    pe = R['panel'] if months_from is None else R['panel'][R['panel'].t >= months_from]
    tt = R['ttab'] if tutors_from is None else R['ttab'][R['ttab']['min'] >= tutors_from]
    par = G.estimate(pe, tt)
    qf = lambda j: par['q'][j] if j <= 12 else par['q']['late']
    return G.project_group(R['panel'], R['P']['mem'], R['members'], par, qf)[0]


def rematch_regime(R):
    """Share of members moved to a tutor in that tutor's first nine months of teaching, in the month after their own
    tutor stopped: 2022 against 2023 onward."""
    s2 = R['panel'][R['panel'].state == 'S2']
    yr = s2.t // 12 + 2022
    young = (s2.tj >= 0) & (s2.tj <= 8)
    return float(young[yr == 2022].mean()), float(young[yr >= 2023].mean()), int((yr == 2022).sum()), int((yr >= 2023).sum())


def all_routes(R):
    n = len(R['members'])
    out = {}
    out['R0 membership-month curve, every membership'] = r0_curve(R)
    out['R0r membership-month curve, 2026 months only'] = r0_recent(R)
    out['R1s curve by membership month and calendar month'] = r1_season(R)
    out['R1e curve with engagement band'] = r1_engagement(R)
    v, ratio = r0_frailty(R); out['R0f curve times the campaign members\' own observed-to-expected (%.2f)' % ratio] = v
    v, ab = r0_sbg(R); out['R0b shifted-beta-geometric fit (a %.2f, b %.2f)' % ab] = v
    out['R2 curve, members whose tutor already stopped shocked'] = r2_already_stopped(R)
    out['R2b tutor-linked, member-weighted stop rate %.3f' % R['par']['member_weighted_stop']] = linked_pooled(R, R['par']['member_weighted_stop'])
    out['R2c tutor-linked, tutor-month stop rate %.3f' % R['par']['q']['pooled_tutor_months']] = linked_pooled(R, R['par']['q']['pooled_tutor_months'])
    out['R3 tutor-linked, stopping by teaching month (golden)'] = R['exp12']
    out['R3 with calendar-month factors'] = G.project_group(R['panel'], R['P']['mem'], R['members'], G.estimate(R['panel'], R['ttab'], seasonal=True), R['qf'], seasonal=True)[0]
    out['R3 smoothed stopping curve'] = linked_smoothed(R)
    out['R3 with a post-rematch uplift (%.2f)' % R['par']['post']] = linked(R, post=True)
    out['R3 one shocked charge only'] = linked(R, two=False)
    out['R3 stops counted twice (all-cause curve plus shocks)'] = linked_double_count(R)
    for f in ('banded', 'log', 'linear'):
        v, ll = snapshot_logit(R, f); out['R3r snapshot logit, teaching month %s (loglik %.1f)' % (f, ll)] = v
    out['R2s stratified on the tutor\'s teaching month at match'] = stratified_at_match(R)
    for y in (2023, 2024):
        since = G.month_index(y, 1)
        for f in ('banded', 'log', 'linear'):
            v, ll = snapshot_logit(R, f, since=since); out['R3r snapshot logit, teaching month %s, joined from %d (loglik %.1f)' % (f, y, ll)] = v
        out['R2s stratified on the tutor\'s teaching month at match, joined from %d' % y] = stratified_at_match(R, since=since)
    for lab, a_, b_ in (('tutors from 2023', 2023, None), ('tutors from 2024', 2024, None), ('months from 2023', None, 2023),
                        ('months from 2024', None, 2024), ('months from 2025', None, 2025), ('tutors and months from 2023', 2023, 2023),
                        ('tutors and months from 2024', 2024, 2024), ('tutors and months from 2025', 2025, 2025)):
        out['R3w tutor-linked, estimated on %s' % lab] = linked_window(
            R, None if a_ is None else G.month_index(a_, 1), None if b_ is None else G.month_index(b_, 1))
    return {k: (v, v / n) for k, v in out.items()}


if __name__ == '__main__':
    R = G.run()
    cost = R['cost']['total_eur']
    for k, (v, s) in all_routes(R).items():
        print('%7.1f  %.4f  EUR %7.2f  %s' % (v, s, cost / v, k))
