"""task13 architecture 5, the generator's checks: the golden (run on target/ alone) against the simulated world's truth,
every semantic fork in the design note asserted, the stump factorial and the forcing read back from effort.json, and the
pack's input gates.

    python3 task13/generator/checks.py
"""
import collections
import csv
import datetime as dt
import json
import os
import re
import sqlite3
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C        # noqa: E402
import faults as F        # noqa: E402
import golden as G        # noqa: E402
import passes as PS       # noqa: E402
import sim                # noqa: E402

T = os.path.join(C.TASK, 'target')
N = {'pass': 0, 'fail': 0}


def ok(label, cond, detail=''):
    N['pass' if cond else 'fail'] += 1
    print(('PASS  ' if cond else 'FAIL  ') + label + ('' if cond else '  %s' % (detail,)))


def lname(lid):
    return 'Line %d' % int(lid[1:])


def near(a, b, tol=2):
    """two places on one line within tol structures of each other"""
    return a[0] == b[0] and abs(a[1] - b[1]) <= tol


def truth_clusters(w):
    """the world's repeat locations: three or more true faults of one cause on one line within 400 m since 2022"""
    net = w['net']
    by = collections.defaultdict(list)
    for f in w['faults']:
        if f['t'] < C.REC0 or f['t'] >= C.T_END or f['cause'] in ('fog', 'lightning', 'vehicle', 'hardware', 'unknown'):
            continue
        by[(f['line'], f['cause'])].append(f)
    out = []
    for (lid, cause), fs in by.items():
        fs = sorted(fs, key=lambda f: f['km'])
        grp = [fs[0]]
        for f in fs[1:]:
            if f['km'] - grp[0]['km'] <= 0.4:
                grp.append(f)
            else:
                out.append((lid, cause, grp))
                grp = [f]
        out.append((lid, cause, grp))
    res = []
    for lid, cause, grp in out:
        if len(grp) < 3:
            continue
        strs = sorted(f['structure'] for f in grp)
        last = max(f['t'] for f in grp)
        res.append(dict(line=lid, cause=cause, structure=collections.Counter(strs).most_common(1)[0][0], s_min=strs[0],
                        s_max=strs[-1], last=last, n=len(grp)))
    return res


def truth_fixed(w, rl):
    """a fix of the location's cause after its last fault, from the world's own records"""
    if rl['cause'] == 'bird':
        return any(lid == rl['line'] and abs(no - rl['structure']) <= 2 and when is not None and when > rl['last']
                   for lid, no, _, _, when in F.ROOSTS)
    if rl['cause'] == 'insulator':
        return any(k[0] == rl['line'] and abs(k[1] - rl['structure']) <= 2 and when > rl['last'] for k, when in w['replaced'].items())
    if rl['cause'] == 'growin':
        return any(k[0] == rl['line'] and abs(k[1] - rl['structure']) <= 2 and when > rl['last'] for k, when in w['trims'].items())
    return False


def main():
    w = sim.world()
    g = G.run(T)
    fig = json.load(open(os.path.join(C.HERE, 'figures.json')))
    eff = json.load(open(os.path.join(C.HERE, 'effort.json')))
    truth = [f for f in w['faults'] if C.REC0 <= f['t'] < C.T_END]
    gf = g['faults']

    # SF1 a fault is one protection sequence on one line; SF2 the year is the Central calendar year, 2026 to 31 October
    ty = collections.Counter(C.to_local(f['t']).year for f in truth)
    gy = collections.Counter(C.to_local(f['t']).year for f in gf)
    ok('SF1 SF2 the golden fault count by year equals the world\'s', ty == gy, (dict(ty), dict(gy)))
    ok('SF1 figures.json carries the same count', fig['faults_by_year'] == {str(k): v for k, v in sorted(gy.items())},
       fig['faults_by_year'])
    cross = [f for f in gf if C.to_local(f['t']).year != f['t'].astimezone(dt.timezone.utc).year]
    ok('SF2 no fault crosses a year boundary between UTC and Central', not cross, len(cross))
    ok('SF2 every fault inside 1 January 2022 to 31 October 2026 (Central)',
       all(dt.date(2022, 1, 1) <= C.to_local(f['t']).date() <= dt.date(2026, 10, 31) for f in gf))
    import bisect
    soe = list(csv.DictReader(open(os.path.join(T, C.FILES['soe']))))
    gt = sorted(f['t'].timestamp() for f in gf)

    def in_sequence(ts):
        i = bisect.bisect_left(gt, ts)
        return any(abs(gt[j] - ts) <= 60 for j in (i - 1, i) if 0 <= j < len(gt))
    prot = [dt.datetime.fromisoformat(r['time_utc']).replace(tzinfo=dt.timezone.utc).timestamp() for r in soe
            if ' 69KV BKR ' in r['point'] and r['state'] == 'OPEN' and r['cause'] == 'PROT']
    lone = [ts for ts in prot if not in_sequence(ts)]
    ok('SF1 single-ended protection trips outside every fault sequence (relay tests) are not counted',
       len(lone) > 0 and len(gf) == sum(ty.values()), (len(lone), len(gf)))

    # SF4 the nine causes, 2026
    tc = collections.Counter(f['cause'] for f in truth if C.to_local(f['t']).year == 2026)
    gc = collections.Counter(f['cause'] for f in gf if C.to_local(f['t']).year == 2026)
    worst = max(abs(tc.get(k, 0) - gc.get(k, 0)) for k in PS.G_CAUSES)
    ok('SF4 the golden\'s 2026 causes within 2 of the world\'s on every cause', worst <= 2, (dict(tc), dict(gc)))
    ok('SF4 the 2026 causes exact against the world', worst == 0, (dict(tc), dict(gc)))

    # SF3 the location, SF5 the repeat location, SF6 fixed after the last fault
    tr = truth_clusters(w)
    for rl in tr:
        rl['fixed'] = truth_fixed(w, rl)
    gr = g['repeat']
    t_open = sorted((rl['line'], rl['structure'], rl['cause']) for rl in tr if not rl['fixed'])
    g_open = sorted((rl['line'], rl['structure'], rl['cause']) for rl in gr if not rl['fixed'])
    miss = [x for x in t_open if not any(near(x, y) and x[2] == y[2] for y in g_open)]
    extra = [y for y in g_open if not any(near(x, y) and x[2] == y[2] for x in t_open)]
    ok('SF3 SF5 every open repeat location of the world found by the golden within 2 structures, with its cause',
       not miss and not extra, (miss, extra))
    t_fix = sorted((rl['line'], rl['structure'], rl['cause']) for rl in tr if rl['fixed'])
    g_fix = sorted((rl['line'], rl['structure'], rl['cause']) for rl in gr if rl['fixed'])
    miss = [x for x in t_fix if not any(near(x, y) and x[2] == y[2] for y in g_fix)]
    extra = [y for y in g_fix if not any(near(x, y) and x[2] == y[2] for x in t_fix)]
    ok('SF6 the locations fixed after their last fault match the world\'s', not miss and not extra, (miss, extra))
    tap = [rl for rl in gr if rl['line'] == 'L09' and rl['cause'] == 'insulator']
    ok('R4 the tap line\'s string within a structure of the world\'s cracked string',
       len(tap) == 1 and abs(tap[0]['km'] - F.TAP_STRING_KM) <= 0.3, [(x['structure'], round(x['km'], 2)) for x in tap])

    # SF7 the five-minute line: no restoration between 20 seconds and 6 minutes; SF8 SF9 member-minutes by faulted line
    secs = [i['seconds'] for imp in w['impacts'] for i in imp['impact']]
    ok('SF7 no member restoration between 30 seconds and 6 minutes (transfers at 21 s at most)', not [s for s in secs if 30 < s < 360],
       sorted(s for s in secs if 30 < s < 360)[:5])
    tl = collections.defaultdict(lambda: [0, 0.0])
    for imp in w['impacts']:
        if C.to_local(imp['t0']).year != 2026:
            continue
        for i in imp['impact']:
            if i['seconds'] > 300:
                tl[imp['line']][0] += i['members']
                tl[imp['line']][1] += i['members'] * i['seconds'] / 60.0
    gl = fig['member_impact_2026_by_line']
    bad = []
    for lid, (n, m) in tl.items():
        gv = gl.get(lname(lid), {})
        if abs(gv.get('sustained', 0) - n) > 0.02 * n + 1 or abs(gv.get('member_minutes', 0) - m) > 0.02 * m + 1:
            bad.append((lid, n, round(m), gv))
    extra = [k for k, v in gl.items() if v['sustained'] and ('L%02d' % int(k.split()[1])) not in tl]
    ok('SF8 SF9 the 2026 member interruptions and member-minutes by faulted line within 2 per cent of the world\'s',
       not bad and not extra, (bad, extra))
    con = sqlite3.connect(os.path.join(T, C.FILES['oms']))
    late = con.execute("select count(*) from outage where cause_code='LOS'").fetchone()[0]
    con.close()
    ok('SF8 the outage system\'s loss-of-supply rows overstate the minutes (the quick route is ruled out by data)',
       late > 0 and fig['quick']['R5']['member_minutes'] > 1.5 * fig['member_impact_2026']['member_minutes'],
       fig['quick']['R5'])

    # SF10 the work list; SF11 due for washing on the 31 October deposit; SF12 the flashover level's readings
    due = set()
    margins = []
    for s in w['sections']:
        line = w['net']['lines'][s['line']]
        sts = [x for x in line['structures'] if x['insulator'] == 'porcelain' and x['shore_km'] <= 6.0]
        cols = [k for k, x in enumerate(sts) if s['s0'] <= x['no'] <= s['s1']]
        v = w['deposits'][s['line']][1][-1, cols]
        name = '%s, Section %s' % (lname(s['line']), s['id'].split('-W')[1])
        margins.append(float(v.mean()) / sim.CRIT)
        if v.mean() >= sim.CRIT:
            due.add(name)
    gw = {x.replace('wash: ', '') for x in fig['wash_due']}
    ok('SF10 SF11 the golden\'s washing list equals the sections whose true deposit on 31 October is past the flashover level',
       gw == due, sorted(gw ^ due))
    ok('SF11 every section clear of the level by a third either way in truth',
       all(m >= 1.33 or m <= 0.75 for m in margins), sorted(round(m, 2) for m in margins if 0.75 < m < 1.33))
    wash_names = {r['section'] for r in w['washes']}
    test_names = {s[0] for s in __import__('field').TEST_SITES}
    ok('SF11 the test insulators are never washed (the latest test reading is not a section\'s deposit)',
       not (wash_names & test_names), sorted(wash_names & test_names))
    latest = G.run(T, dict(G.GOLD, deposit='latest'))
    lw = sorted(k for k, v in latest['deposits']['sections'].items() if v['due'])
    gk = sorted(k for k, v in g['deposits']['sections'].items() if v['due'])
    ok('SF11 the latest-test-reading route files another list, ruled out by the washing log', lw != gk, lw)
    gold_wl = PS.flat(PS.results_of(g, PS.worklist(g))['wl'])
    fam = {v['name']: v['answer'] for v in eff['forcing']['golden_family']}
    for name in ('flashover level: 5th percentile', 'flashover level: 10th percentile'):
        ok('SF12 %s files the golden work list' % name, fam.get(name) == fig['work_list'], name)
    for name in ('repeat window 350 m', 'repeat window 450 m'):
        ok('SF5 %s files the golden work list' % name, fam.get(name) == fig['work_list'], name)
    ok('SF10 the work list recomputed equals figures.json', gold_wl == sorted(fig['work_list']), gold_wl)

    # SF13 the fog season files the washing date; SF14 the 69 kV system is the line register's sixteen lines
    txt = subprocess.run(['unzip', '-p', os.path.join(T, C.FILES['procedure']), 'word/document.xml'], capture_output=True,
                         text=True).stdout
    txt = re.sub(r'<[^>]+>', '', txt)
    ok('SF13 RP-04 files the fog season from 1 December', 'The fog season runs from 1 December to 31 March' in txt)
    ok('SF14 every golden fault on one of the line register\'s sixteen lines',
       len(g['d']['lines']) == 16 and all(f['line'] in g['d']['lines'] for f in gf), len(g['d']['lines']))

    # the stump factorial and the forcing, read back
    fa = eff['factorial']
    stumps = [j for j in fa['judgments'] if j['kind'] == 'stump']
    ok('factorial: every stump moves the call when dropped', all(set(j['dropped']['answer']) != set(fa['golden_answer']) for j in stumps))
    ok('factorial: no stump reaches the call alone', all(set(j['alone']['answer']) != set(fa['golden_answer']) for j in stumps))
    ok('factorial: level 5 (three or more necessary stumps on distinct wrong lists)',
       len(stumps) >= 3 and len({tuple(sorted(j['dropped']['answer'])) for j in stumps}) == len(stumps))
    ok('forcing: every golden-family rival files the golden list', all(v['answer'] == fig['work_list'] for v in eff['forcing']['golden_family']))
    ok('forcing: every perturbation files the golden list', all(v['answer'] == fig['work_list'] for v in eff['forcing']['perturbations']))
    ok('forcing: every shortcut files another list', all(set(s['answer']) != set(fig['work_list']) for s in eff['forcing']['shortcuts']))
    care = fig['careful']
    ok('the careful pass misses R2, R3, R4, R7 and R8 outright',
       care['R2'] != fig['vegetation_repeat_locations'] and care['R3'] != fig['night_repeat_locations'] and
       care['R4'] != fig['tap_repeat_location'] and care['R7'] != fig['wash_due'] and care['R8'] != fig['repeat_locations_open'])

    # the pack's input gates
    files = sorted(os.listdir(T))
    ok('pack: 28 files, every name the generator writes', sorted(C.FILES.values()) == files, len(files))
    exts = collections.Counter(os.path.splitext(f)[1] for f in files)
    ok('pack: two or more file categories', len({'.csv', '.json', '.sqlite'} & set(exts)) and len({'.xlsx', '.docx', '.pdf'} & set(exts)))
    rows = {f: sum(1 for _ in open(os.path.join(T, f), encoding='utf-8', errors='replace')) - 1 for f in files if f.endswith('.csv')}
    ok('pack: a CSV of 20,000 rows or more', max(rows.values()) >= 20000, rows)
    ok('pack: a second CSV of ten printed pages or more (600 lines)', sorted(rows.values())[-2] >= 600, rows)
    src = open(os.path.join(C.HERE, 'golden.py')).read()
    ok('pack: the two distractors are never read by the golden', "p('corrosion')" not in src and "p('easements')" not in src)
    ok('pack: 40 MB or so of data', 30e6 <= sum(os.path.getsize(os.path.join(T, f)) for f in files) <= 60e6)

    print('%d passed, %d failed' % (N['pass'], N['fail']))
    return 1 if N['fail'] else 0


if __name__ == '__main__':
    sys.exit(main())
