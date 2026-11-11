"""Build task13's pack (target/) from the clean world, then the golden deliverables (golden/), then both zips.

    python3 task13/generator/build.py            # target/, golden/, target.zip, golden.zip
    python3 task13/generator/build.py --out DIR  # the same into DIR (the byte-identical rebuild check)
    python3 task13/generator/build.py --target-only
"""
import argparse
import hashlib
import os
import pickle
import shutil
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C      # noqa: E402
import docs as D        # noqa: E402
import pack as P        # noqa: E402
import postprocess as PP  # noqa: E402
import sim              # noqa: E402

import tempfile  # noqa: E402
CACHE = os.path.join(tempfile.gettempdir(), 'task13_world_cache')


def world(refresh=False):
    """the simulated world, cached under task13/.cache (never committed)"""
    os.makedirs(CACHE, exist_ok=True)
    p = os.path.join(CACHE, 'world.pkl')
    sim_files = ('common', 'net', 'geo', 'storms', 'phys', 'world', 'faults', 'others', 'logs', 'sim')
    src = max(os.path.getmtime(os.path.join(C.HERE, f + '.py')) for f in sim_files)
    if not refresh and os.path.exists(p) and os.path.getmtime(p) > src:
        return pickle.load(open(p, 'rb'))
    w = sim.simulate()
    w.pop('N', None)
    pickle.dump(w, open(p, 'wb'))
    return w


def build_target(target, w, quiet=False):
    t0 = time.time()
    if os.path.exists(target):
        shutil.rmtree(target)
    os.makedirs(target)
    f = lambda k: os.path.join(target, C.FILES[k])
    n = {}
    n['strokes'] = P.write_strokes(w, f('strokes'))
    n['scada'] = P.write_scada(w, f('scada'))
    n['downloads'] = P.write_downloads(w, f('downloads'))
    n['oms'] = P.write_oms(w, f('oms'))
    n['routes'] = P.write_routes(w, f('routes'))
    n['raingauge'] = P.write_raingauge(w, f('raingauge'))
    n['zones'] = D.write_zones(w, f('zones'))
    n['inspections'] = D.write_inspections(w, f('inspections'))
    n['transformers'] = D.write_transformers(w, f('transformers'))
    D.write_terms(f('terms'))
    D.write_procedure(f('procedure'))
    D.write_quotation(f('quotation'))
    PP.own_mtimes(target, {C.FILES[k]: C.local(C.STAMP[k][1]) for k in C.FILES
                           if not C.FILES[k].endswith(('.xlsx', '.docx', '.pptx', '.pdf'))})
    if not quiet:
        print('target built in %.0fs: %s' % (time.time() - t0, ', '.join('%s %d' % kv for kv in n.items())))
    return n


def digest(folder):
    h = hashlib.sha256()
    names = sorted(os.path.relpath(os.path.join(r, f), folder) for r, ds, fs in os.walk(folder) for f in fs)
    for fn in names:
        h.update(fn.encode())
        h.update(open(os.path.join(folder, fn), 'rb').read())
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out')
    ap.add_argument('--target-only', action='store_true')
    ap.add_argument('--refresh', action='store_true')
    a = ap.parse_args()
    root = a.out or C.TASK
    w = world(refresh=a.refresh or bool(a.out))
    build_target(os.path.join(root, 'target'), w)
    print('target digest', digest(os.path.join(root, 'target'))[:16])
    if a.target_only:
        return
    import golden as G
    R, T, F = G.build(os.path.join(root, 'target'), os.path.join(root, 'golden'),
                      figures=(None if a.out else os.path.join(C.HERE, 'figures.json')))
    print('golden digest', digest(os.path.join(root, 'golden'))[:16])
    if not a.out:
        import effort_passes as EP
        EP.write(os.path.join(root, 'target'), os.path.join(C.HERE, 'effort.json'), F, R=R)
        print('effort.json written')
        PP.zip_folder(os.path.join(root, 'target'), os.path.join(root, 'target.zip'), zone=C.ZONE)
        PP.zip_folder(os.path.join(root, 'golden'), os.path.join(root, 'golden.zip'), zone=C.ZONE)
        for z in ('target.zip', 'golden.zip'):
            print(z, hashlib.sha256(open(os.path.join(root, z), 'rb').read()).hexdigest()[:16])


if __name__ == '__main__':
    main()
