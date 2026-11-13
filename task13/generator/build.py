"""Build task13's pack (target/) from the simulated world, then the golden deliverables (golden/), then both zips.

    python3 task13/generator/build.py            # target/, golden/, target.zip, golden.zip
    python3 task13/generator/build.py --out DIR  # the same into DIR (the byte-identical rebuild check)
    python3 task13/generator/build.py --target-only
"""
import argparse
import hashlib
import json
import os
import shutil
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C            # noqa: E402
import numpy as np            # noqa: E402
import pack_docs as PD        # noqa: E402
import pack_env as E          # noqa: E402
import pack_ops as PO         # noqa: E402
import pack_relays as PR      # noqa: E402
import postprocess as PP      # noqa: E402
import sim                    # noqa: E402


def build_target(target, w, quiet=False):
    t0 = time.time()
    if os.path.exists(target):
        shutil.rmtree(target)
    os.makedirs(target)
    f = lambda k: os.path.join(target, C.FILES[k])
    rng = lambda k: np.random.default_rng(C.EV_SEED * 7 + k)
    n = {}
    # the lightning record first: the control room's cause codes read the radar
    strokes = E.stroke_rows(w, rng(1))
    n['strokes'] = E.write_strokes(strokes, f('strokes'))
    er, gv, em = PR.build_rows(w)
    n['er'] = PR.write_er(er, f('er'))
    n['gv'] = PR.write_gv(gv, f('gv'))
    PD.write_legacy(PR.legacy_rows(w, em), f('legacy'))
    fds = PO.feeders(w['net'])
    n['soe'] = PO.write_soe(PO.soe_rows(w, fds), f('soe'))
    PD.write_crlog(PO.crlog_rows(w), f('crlog'))
    n['oms'] = PO.oms_build(w, fds, f('oms'))
    mrows = PO.members_rows(w, fds)
    with open(f('members'), 'w', newline='') as fh:
        import csv
        wr = csv.writer(fh)
        wr.writerow(['month', 'feeder', 'substation', 'members'])
        for r in mrows:
            wr.writerow(r)
    n['members'] = len(mrows)
    PD.write_lines(w, f('lines'))
    n['structures'] = PD.write_structures(w, f('structures'))
    PD.write_subs(w, f('subs'))
    PD.write_studies(w, f('study22'), f('study25'))
    PD.write_settings(w, f('settings'))
    n['loading'] = E.write_rows(E.loading_rows(w, rng(2)), f('loading'))
    n['apt'] = E.write_asos(E.asos_rows(w['wx'], 'APT', rng(3)), f('apt'), 'KPAX')
    n['inl_apt'] = E.write_asos(E.asos_rows(w['wx'], 'INA', rng(4)), f('inl_apt'), 'KIRW')
    n['stations'] = E.write_stations(E.station_rows(w['wx'], rng(5)), f('stations'))
    PD.write_patrols(PO.patrol_rows(w), f('patrols'))
    PD.write_avian(E.avian_rows(w, rng(6)), f('avian'))
    PD.write_esdd(w, f('esdd'))
    PD.write_washing(w, f('washing'))
    vr = E.veg_rows(w, rng(7))
    with open(f('veg'), 'w', newline='') as fh:
        import csv
        wr = csv.writer(fh)
        wr.writerow(['work_order', 'completed', 'line', 'from_structure', 'to_structure', 'work_type', 'description', 'trees_or_acres'])
        for r in vr:
            wr.writerow(r)
    mr = E.maint_rows(w, rng(8))
    with open(f('maint'), 'w', newline='') as fh:
        import csv
        wr = csv.writer(fh)
        wr.writerow(['work_order', 'opened', 'completed', 'line', 'structure', 'work_type', 'description', 'crew'])
        for r in mr:
            wr.writerow(r)
    n['ipp'] = E.write_ipp(E.ipp_rows(w, rng(9)), f('ipp'))
    PD.write_procedure(f('procedure'))
    PD.write_distractors(w, f('corrosion'), f('easements'))
    PP.own_mtimes(target, {C.FILES[k]: C.local(C.STAMP[k][1]) for k in C.FILES
                           if not C.FILES[k].endswith(('.xlsx', '.docx', '.pptx', '.pdf'))})
    if not quiet:
        print('target built in %.0fs: %s' % (time.time() - t0, ', '.join('%s %s' % kv for kv in n.items())))
    return n


def digest(folder):
    h = hashlib.sha256()
    names = sorted(os.path.relpath(os.path.join(r, fn), folder) for r, ds, fs in os.walk(folder) for fn in fs)
    for fn in names:
        h.update(fn.encode())
        h.update(open(os.path.join(folder, fn), 'rb').read())
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=None)
    ap.add_argument('--target-only', action='store_true')
    ap.add_argument('--refresh', action='store_true')
    a = ap.parse_args()
    w = sim.world(refresh=a.refresh)
    base = a.out or C.TASK
    target = os.path.join(base, 'target')
    counts = build_target(target, w)
    if a.target_only:
        print('target digest', digest(target)[:16])
        return
    import deliver as D
    import passes as PS
    PS.build(target, os.path.join(C.HERE, 'effort.json') if base == C.TASK else os.path.join(base, 'effort.json'))
    golden = os.path.join(base, 'golden')
    D.build_golden(target, golden, w)
    if base == C.TASK:
        import metadata as MD
        import writeup
        writeup.write(os.path.join(C.TASK, 'submission.md'))
        json.dump(MD.metadata(target, counts), open(os.path.join(C.TASK, 'metadata.json'), 'w'), indent=1)
    PP.zip_folder(target, os.path.join(base, 'target.zip'), zone=C.ZONE)
    PP.zip_folder(golden, os.path.join(base, 'golden.zip'), zone=C.ZONE)
    print('target digest', digest(target)[:16], 'golden digest', digest(golden)[:16])


if __name__ == '__main__':
    main()
