"""The cracker sheet: score every graded ask for the landed run and the shallow run on the cut pack.

    python3 task12/generator/ceiling.py

Landed run: the deep step taken (every buyer at its own price group's settled share, the Loyal Grocer wave borrowed
from long-tenure same-group buyers), every mess item cleaned and every filed rule read, but neither of the asks' own
second judgments: it weights 2027 by the litres households bought since launch (the window in which buyers were caught
buying high) and counts every household that has bought the line as a 2027 buyer. Shallow run: the default path
(Parfitt-Collins with the April buyers' repeat and the buying index since launch), the same cleaning, its litres from
its share and its buyers from its penetration. Weights 38 (call and critical components), 7 (instruction-following),
55 (asks), as supplemental-stumping Part 0. An ask is kept when the run's figure, at the prompt's rounding, sits inside
the range the golden states for it. Three rung-2 runs are scored beside them: the honeymoon taken and the price groups
skipped, one settled share pooled from every buyer at 16 weeks (Support) and at 12 weeks (Hold by the numbers), and
each wave at its own settled share with the Loyal Grocer wave at the earlier waves' mean (Hold by the numbers). A run
that lands the call without the price groups gets the call (18 of the 38) and the components it can match.
"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C      # noqa: E402
import golden as G      # noqa: E402
import rivals as V      # noqa: E402
import checks as CK     # noqa: E402

ASKS = [('A2 litres 2027 Q1', 2.75), ('A2 litres 2027 Q2', 2.75), ('A2 litres 2027 Q3', 2.75), ('A2 litres 2027 Q4', 2.75),
        ('A2 litres 2027, the year', 5.50), ('A3 households buying in 2027', 11.00), ('A4 purchases per buying household', 8.25),
        ('A5 chart, litres by quarter', 5.50), ('A6 workbook: settled share by price group', 8.25),
        ('A7 workbook: buyers by first purchase', 5.50)]


def inside(x, lo, hi, unit):
    xr = round(x / unit) * unit
    return lo - 1e-9 <= xr <= hi + 1e-9


def main():
    F = json.load(open(os.path.join(C.HERE, 'figures.json')))
    R = G.compute(C.TARGET)
    D = R['D']
    rv, _ = V.run(D=D)
    w = D['H']['w2026'].fillna(0).values
    st, buyer, first, tier = D['static'], D['buyer'], D['first'], R['tier']
    triers = buyer & (first >= 0)
    scale = R['scale']
    qs = np.array(F['quarters_raw']) / sum(F['quarters_raw'])
    lo_l, hi_l = F['line27_range_ml']
    pack = np.nanmedian(D['nvpack'])
    every_buyer = scale * w[st & triers].sum()
    # landed run: the golden's settled shares, window litres, every past buyer counted
    Lw, _ = G.litres27(D, 'vwin')
    share_l = (w * np.where(triers, R['lev'], 0.0) * Lw)[st].sum() / (w * Lw)[st].sum()
    lit_l = share_l * scale * (w * Lw)[st].sum() / 1e6
    packs = np.where(np.isfinite(D['nvpack']), D['nvpack'], pack)
    per_l = (w * np.where(triers, R['lev'] * Lw / packs, 0.0))[st].sum() / w[st & triers].sum()
    runs = {'landed': dict(share=share_l, lit=lit_l, buyers=every_buyer, per=per_l, groups=True, waves=True)}
    # the shallow run (the default path) and the two rung-2 runs, maturity taken and price groups skipped
    for name, share, waves in [('shallow', rv['pc_careful'], True), ('pooled16', CK.R_pooled(D, 16), True),
                               ('pooled12', CK.R_pooled(D, 12), True), ('wavemean16', V.per_wave(D, 16, 'mean'), True)]:
        lit = share * R['cat27_ca'] / 1e6
        runs[name] = dict(share=share, lit=lit, buyers=every_buyer, per=lit * 1e6 / every_buyer / pack, groups=False, waves=waves)
    total = sum(wt for _, wt in ASKS)
    score = {}
    table = []
    for name, r in runs.items():
        keep = [inside(r['lit'] * qs[k], lo_l * qs[k], hi_l * qs[k], 0.1) for k in range(4)]
        keep += [inside(r['lit'], lo_l, hi_l, 0.1), inside(r['buyers'], *F['buyers27_range'], 1e4),
                 inside(r['per'], *F['per_buyer_range'], 0.1), inside(r['lit'], lo_l, hi_l, 0.1), r['groups'], r['waves']]
        kept = sum(wt for (_, wt), k in zip(ASKS, keep) if k)
        on = G.band(100 * r['share']) == 'Hold'
        if name == 'landed':
            head = 38
        elif on:
            # the call (18) and the critical components it can match: the Loyal Grocer wave's households (2.5) and the
            # share inside the golden's stated range (5)
            head = 18 + 2.5 + (5 if F['share_range'][0] - 1e-9 <= round(100 * r['share'], 1) <= F['share_range'][1] + 1e-9 else 0)
        else:
            head = 5
        score[name] = head + 7 + 55 * kept / total
        table.append((name, keep, kept, on))
    print('| Ask | Weight | ' + ' | '.join(n for n, _, _, _ in table) + ' |')
    print('|---|---|' + '---|' * len(table))
    for i, (lab, wt) in enumerate(ASKS):
        print('| %s | %.2f | ' % (lab, wt) + ' | '.join('keep' if k[i] else 'miss' for _, k, _, _ in table) + ' |')
    print()
    for name, r in runs.items():
        print('%s: share %.2f (%s), litres %.2f M, buyers %.0f, per buyer %.2f, score %.1f' % (
            name, 100 * r['share'], G.band(100 * r['share']), r['lit'], r['buyers'], r['per'], score[name]))
    keep_s = 100 * dict((n, kept) for n, _, kept, _ in table)['shallow'] / total
    print('Shallow keep: %.1f' % keep_s)
    print('Pair ceiling: %.1f (landed run %.1f, shallow run %.1f)' % ((score['landed'] + score['shallow']) / 2, score['landed'], score['shallow']))
    for other in ('pooled16', 'pooled12', 'wavemean16'):
        print('Pair, landed with %s: %.1f; shallow with %s: %.1f' % (other, (score['landed'] + score[other]) / 2, other,
                                                                   (score['shallow'] + score[other]) / 2))


if __name__ == '__main__':
    main()
