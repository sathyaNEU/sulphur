"""The cracker sheet: score every graded ask for the landed run and the shallow run on the cut pack.

    python3 task1/generator/ceiling.py

Landed run: the deep step taken (members carried through their tutors' stopping by teaching month, the two shocked
charges, the members' own curve on active-tutor months), every mess item cleaned and every filed rule read, but the
asks' own second judgment not taken: its ranges come from members drawn independently, not from tutors whose stop
every one of their members shares. Shallow run: the default path (the membership-month curve), the same cleaning.
Weights 38 (call and critical components), 7 (instruction-following), 55 (asks), as `supplemental-stumping` Part 0.
"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import golden as G            # noqa: E402
import rivals as V            # noqa: E402
from common import *          # noqa: E402,F401,F403


def r50(x):
    return int(round(x / 50.0)) * 50


def r25(x):
    return int(round(x / 25.0)) * 25


def binom_range(e, n_live, done):
    """A member-independent 80 per cent range around an expectation (the shallow run's own uncertainty)."""
    p = (e - done) / max(n_live, 1)
    sd = np.sqrt(n_live * p * (1 - p))
    return e - 1.2816 * sd, e + 1.2816 * sd


def main():
    F = json.load(open(os.path.join(HERE, 'figures.json')))
    R = G.run()
    n = len(R['members']); cost = R['cost']['total_eur']
    lo_i, hi_i, d_i = G.predictive_range(R, n_rep=G.N_REP, seed=611, clustered=False)
    p5i, p95i = np.percentile(d_i, 5), np.percentile(d_i, 95)
    gold = dict(
        exp12=F['exp12'], cost=F['cost_per_12m_eur'], flip=F['flip_cost_per_paid_eur'],
        r_c=F['range80_cost_eur'], r_c90=F['range90_cost_eur'], monthly=F['monthly']['All'],
        chart_end=(F['shares']['September'][max(F['shares']['September'])], F['shares']['October'][max(F['shares']['October'])]))
    landed = dict(
        exp12=r50(R['exp12']), cost=r25(cost / R['exp12']), flip=r25(G.BAR_EUR * R['exp12'] / n),
        r_c=[r25(cost / hi_i), r25(cost / lo_i)], r_c90=[r25(cost / p95i), r25(cost / p5i)],
        monthly=F['monthly']['All'],
        chart_end=gold['chart_end'])
    # shallow: the membership-month curve, month by month
    e0 = V.r0_curve(R)
    mem = R['P']['mem'].set_index('member_id')['status'].to_dict()
    last = G.state_at_cut(R['panel'], R['members'])
    h0 = G.kcurve(R['panel'])
    live = [m for m in R['members'] if mem.get(m) == 'active' and last.loc[m, 't'] == G.CUT_M]
    done = sum(1 for m in R['members'] if m not in set(live) and last.loc[m, 'k'] >= 12)
    acc = {t: 0.0 for t in range(G.CUT_M + 1, G.LAST_M + 1)}
    for m in live:
        s = 1.0; k0 = int(last.loc[m, 'k'])
        for step, t in enumerate(sorted(acc), start=1):
            if step > 1:
                s *= 1 - h0[min(k0 + step - 1, G.KMAX)]
            acc[t] += s
    lo0, hi0 = binom_range(e0, len(live), done)
    sd0 = (hi0 - lo0) / (2 * 1.2816)
    shallow = dict(
        exp12=r50(e0), cost=r25(cost / e0), flip=r25(G.BAR_EUR * e0 / n),
        r_c=[r25(cost / hi0), r25(cost / lo0)], r_c90=[r25(cost / (e0 + 1.645 * sd0)), r25(cost / (e0 - 1.645 * sd0))],
        monthly={month_str(t): r50(v) for t, v in acc.items()},
        chart_end=(F['curve_share'][max(F['curve_share'])],) * 2)
    # the ask sheet: (label, weight, scorer)
    def same(a, b):
        return a == b
    months = sorted(gold['monthly'])
    asks = [('A1 expected twelfth-month members (nearest 50)', 7, lambda r: same(r['exp12'], gold['exp12'])),
            ('A2 cost per twelfth-month member (nearest 25)', 7, lambda r: same(r['cost'], gold['cost'])),
            ('A2r 80% range, cost per twelfth-month member, low', 3, lambda r: same(r['r_c'][0], gold['r_c'][0])),
            ('A2r 80% range, cost per twelfth-month member, high', 3, lambda r: same(r['r_c'][1], gold['r_c'][1])),
            ('A2r 90% range, cost per twelfth-month member, low', 3, lambda r: same(r['r_c90'][0], gold['r_c90'][0])),
            ('A2r 90% range, cost per twelfth-month member, high', 3, lambda r: same(r['r_c90'][1], gold['r_c90'][1])),
            ('A3 cost per paid member that meets the bar exactly (nearest 25)', 5, lambda r: same(r['flip'], gold['flip'])),
            ('A4 chart: September and October joiners end near 26 to 27 per cent paying',
             3, lambda r: abs(r['chart_end'][0] - gold['chart_end'][0]) < 2 and abs(r['chart_end'][1] - gold['chart_end'][1]) < 2)]
    per = 8.0 / len(months)
    for t in months:
        asks.append(('A5 workbook, all AUT26 members paying in %s' % t, per, lambda r, t=t: abs(r['monthly'][t] - gold['monthly'][t]) <= 50))
    W = sum(a[1] for a in asks)
    Lc = sum(a[1] for a in asks if a[2](landed)) / W
    Ls = sum(a[1] for a in asks if a[2](shallow)) / W
    # every critical component (the stop shock, the stopping by teaching month, the AUT26 exposure, the expected
    # twelfth-month members, the cost per twelfth-month member) is a deep-step figure the shallow run never computes,
    # so its partial credit r on the 38 is the campaign-member count and cost build-up it shares: about 3
    C = 38 + 7 + 55 * Lc
    S = 3 + 7 + 55 * Ls
    print('| Ask | Weight | Shallow run | Cracker (landed run) |')
    print('|---|---|---|---|')
    for lab, w, f in asks:
        print('| %s | %.2f | %s | %s |' % (lab, w, 'keep' if f(shallow) else 'miss', 'keep' if f(landed) else 'miss'))
    print()
    print('Landed keep %.3f, shallow keep %.3f; landed run %.1f, shallow run %.1f; pair ceiling %.1f' % (Lc, Ls, C, S, (C + S) / 2))
    json.dump(dict(Lc=Lc, Ls=Ls, C=C, S=S, pair=(C + S) / 2, shallow=dict(exp12=shallow['exp12'], cost=shallow['cost'])),
              open(os.path.join(HERE, 'ceiling.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
