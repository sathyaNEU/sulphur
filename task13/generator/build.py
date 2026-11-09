"""Build task13's pack (target/) from the clean world, then the golden deliverables (golden/), then both zips.

    python3 task13/generator/build.py            # target/, golden/, target.zip, golden.zip
    python3 task13/generator/build.py --out DIR  # the same into DIR (the byte-identical rebuild check)
"""
import argparse
import hashlib
import json
import os
import shutil
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C      # noqa: E402
import docs as D        # noqa: E402
import pack as P        # noqa: E402
import postprocess as PP  # noqa: E402
import world as W       # noqa: E402


def build_target(target, quiet=False):
    t0 = time.time()
    if os.path.exists(target):
        shutil.rmtree(target)
    os.makedirs(target)
    os.makedirs(os.path.join(target, 'pou_aws_hourly'))
    S = W.simulate()
    E = W.interruptions(S)
    f = lambda k: os.path.join(target, C.FILES[k])
    n = {}
    n['oms'] = P.write_oms(S, E, f('oms'))
    for sid in C.STATION_IDS:
        n['wx_' + sid] = P.write_weather(S, sid, f('wx_' + sid))
    n['stations'] = P.write_stations(f('stations'))
    n['devices'] = P.write_devices(S, f('devices'))
    n['icps'], icps_oct = P.write_icps(S, f('icps'))
    n['feeders'] = D.write_feeders(S, f('feeders'), icps_oct)
    n['vegcycle'] = D.write_vegcycle(S, f('vegcycle'))
    n['notices'] = D.write_notices(S, f('notices'))
    B = D.boundary_table(S, E)
    D.write_standard(f('standard'), B)
    D.write_programme(f('programme'))
    D.write_rates(f('rates'))
    PP.own_mtimes(target, {C.FILES[k]: C.local(C.STAMP[k][1]) for k in C.FILES
                           if not C.FILES[k].endswith(('.xlsx', '.docx', '.pptx', '.pdf'))})
    if not quiet:
        print('target built in %.0fs: %s' % (time.time() - t0, ', '.join('%s %d' % kv for kv in n.items())))
    return S, E, n, B


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
    a = ap.parse_args()
    root = a.out or C.TASK
    build_target(os.path.join(root, 'target'))
    print('target digest', digest(os.path.join(root, 'target'))[:16])
    if a.target_only:
        return
    import golden as G
    G.build(os.path.join(root, 'target'), os.path.join(root, 'golden'), figures=(None if a.out else os.path.join(C.HERE, 'figures.json')))
    print('golden digest', digest(os.path.join(root, 'golden'))[:16])
    if not a.out:
        PP.zip_folder(os.path.join(root, 'target'), os.path.join(root, 'target.zip'), zone=C.ZONE)
        PP.zip_folder(os.path.join(root, 'golden'), os.path.join(root, 'golden.zip'), zone=C.ZONE)
        for z in ('target.zip', 'golden.zip'):
            print(z, hashlib.sha256(open(os.path.join(root, z), 'rb').read()).hexdigest()[:16])


if __name__ == '__main__':
    main()
