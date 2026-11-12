"""Build task13's pack (target/) from the simulated world, then the golden deliverables (golden/), then both zips.

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
import tempfile
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C      # noqa: E402
import docs as D        # noqa: E402
import pack as P        # noqa: E402
import postprocess as PP  # noqa: E402
import sim              # noqa: E402

CACHE = os.path.join(tempfile.gettempdir(), 'task13_v4_world_cache')
SIM_FILES = ('common', 'net', 'weather', 'load', 'sim')


def world(refresh=False):
    os.makedirs(CACHE, exist_ok=True)
    p = os.path.join(CACHE, 'world.pkl')
    src = max(os.path.getmtime(os.path.join(C.HERE, f + '.py')) for f in SIM_FILES)
    if not refresh and os.path.exists(p) and os.path.getmtime(p) > src:
        return pickle.load(open(p, 'rb'))
    w = sim.simulate()
    pickle.dump(w, open(p, 'wb'))
    return w


def build_target(target, w, quiet=False):
    t0 = time.time()
    if os.path.exists(target):
        shutil.rmtree(target)
    os.makedirs(target)
    f = lambda k: os.path.join(target, C.FILES[k])
    n = {}
    n['adms'] = P.write_adms(w, f('adms'))
    n['oms'] = P.write_oms(w, f('oms'))
    n['scada'] = P.write_scada(w, f('scada'))
    n['devents'] = P.write_devents(w, f('devents'))
    P.write_weather(w, f('weather'))
    P.write_ami(w, f('ami'))
    D.write_register(w, f('register'))
    D.write_loops(w, f('loops'))
    D.write_maint(w, f('maint'))
    # the planners' 2027 reinforcements go to the end sections the transfers load hardest; the large load is
    # where its customer asked for it. Both are chosen on a provisional cut, then the workbooks are written.
    plan = D.choose_plan(w, target, f)
    D.write_capital(w, f('capital'), plan)
    D.write_loads(w, f('loads'), plan)
    D.write_incidents(w, f('incidents'))
    D.write_dashboard(w, f('dashboard'), f('adms'))
    D.write_veg(w, f('veg'))
    D.write_order(f('order'))
    D.write_design(f('design'))
    PP.own_mtimes(target, {C.FILES[k]: C.local(C.STAMP[k][1]) for k in C.FILES
                           if not C.FILES[k].endswith(('.xlsx', '.docx', '.pptx', '.pdf'))})
    if not quiet:
        print('target built in %.0fs: %s' % (time.time() - t0, ', '.join('%s %s' % kv for kv in n.items())))
    return n, plan


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
    G.build(os.path.join(root, 'target'), os.path.join(root, 'golden'),
            figures=(None if a.out else os.path.join(C.HERE, 'figures.json')))
    print('golden digest', digest(os.path.join(root, 'golden'))[:16])
    if not a.out:
        import passes as EP
        EP.write(os.path.join(root, 'target'), os.path.join(C.HERE, 'effort.json'))
        PP.zip_folder(os.path.join(root, 'target'), os.path.join(root, 'target.zip'), zone=C.ZONE)
        PP.zip_folder(os.path.join(root, 'golden'), os.path.join(root, 'golden.zip'), zone=C.ZONE)
        for z in ('target.zip', 'golden.zip'):
            print(z, hashlib.sha256(open(os.path.join(root, z), 'rb').read()).hexdigest()[:16])


if __name__ == '__main__':
    main()
