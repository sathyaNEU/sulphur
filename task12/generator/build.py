"""Build task12's pack (target/) from the clean world, then the golden deliverables (golden/), then both zips.

    python3 task12/generator/build.py            # target/, golden/, target.zip, golden.zip
    python3 task12/generator/build.py --out DIR  # the same into DIR (the byte-identical rebuild check)
"""
import argparse
import hashlib
import os
import shutil
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C      # noqa: E402
import docs as D        # noqa: E402
import pack as P        # noqa: E402
import postprocess as PP  # noqa: E402
import products as PR   # noqa: E402
import world as W       # noqa: E402


def prepare(S):
    import numpy as np
    rng = np.random.default_rng(W.SEED + 110)
    S['hh_id'] = P.household_ids(S['H']['n'])
    prov = []
    for r in S['H']['region']:
        opts, p = P.PROV[W.REGIONS[r]]
        prov.append(opts[int(rng.choice(len(opts), p=p))])
    S['province'] = np.array(prov)
    S['weights'] = P.weights(S)
    return S


def build_target(target, quiet=False):
    t0 = time.time()
    if os.path.exists(target):
        shutil.rmtree(target)
    os.makedirs(target)
    S = prepare(W.simulate())
    M = PR.master()
    O = P.occasions(S)
    L = P.lines(S, O, M)
    import numpy as np
    tot = np.zeros(S['H']['n']); cnt = np.zeros(S['H']['n'])
    for (h, d, bc, sku, units, paid, flag) in L:
        if sku['family'] != -2:
            tot[h] += sku['litres'] * sku['units'] * units; cnt[h] += 1
    S['litres_pack'] = np.where(cnt > 0, tot / np.maximum(cnt, 1), S['H']['litres_occ'])
    f = lambda k: os.path.join(target, C.FILES[k])
    n = {}
    n['purchases'], n['rescans'] = P.write_purchases(S, L, f('purchases'))
    n['households'] = P.write_households(S, f('households'))
    n['weeks'] = P.write_weeks(f('weeks'))
    n['banners'] = P.write_banners(f('banners'))
    n['distribution'] = P.write_distribution(f('distribution'), M)
    n['master'] = D.write_master(f('master'), M)
    n['trade'] = D.write_trade(f('trade'), M)
    n['media'] = D.write_media(f('media'))
    n['tracker'] = D.write_tracker(f('tracker'))
    D.write_standard(f('standard'))
    D.write_proposal(f('proposal'))
    PP.own_mtimes(target, {C.FILES[k]: C.local(C.STAMP[k]) for k in C.FILES
                           if not C.FILES[k].endswith(('.xlsx', '.docx', '.pptx', '.pdf'))})
    if not quiet:
        print('target built in %.0fs: %s' % (time.time() - t0, ', '.join('%s %d' % kv for kv in n.items())))
    return S, M, O, L, n


def digest(folder):
    h = hashlib.sha256()
    for fn in sorted(os.listdir(folder)):
        h.update(fn.encode())
        h.update(open(os.path.join(folder, fn), 'rb').read())
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out')
    ap.add_argument('--target-only', action='store_true')
    a = ap.parse_args()
    root = a.out or C.TASK
    build_target(os.path.join(root, 'target'))
    print('target digest', digest(os.path.join(root, 'target'))[:16])
    if a.target_only:
        return
    import golden as G
    G.build(os.path.join(root, 'target'), os.path.join(root, 'golden'))
    print('golden digest', digest(os.path.join(root, 'golden'))[:16])
    if not a.out:
        PP.zip_folder(os.path.join(root, 'target'), os.path.join(root, 'target.zip'), zone=C.ZONE)
        PP.zip_folder(os.path.join(root, 'golden'), os.path.join(root, 'golden.zip'), zone=C.ZONE)
        for z in ('target.zip', 'golden.zip'):
            print(z, hashlib.sha256(open(os.path.join(root, z), 'rb').read()).hexdigest()[:16])


if __name__ == '__main__':
    main()
