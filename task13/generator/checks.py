"""task13 architecture 6, the generator's checks: the golden (run on target/ alone) against the simulated world's truth,
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
        by[(f['line'], WORLD_CAUSE.get(f['cause'], f['cause']))].append(f)
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


WORLD_CAUSE = {'clearance': 'hardware'}     # the conductor reaching the circuit under it is RP-04's equipment or hardware


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
    eff_fam = {v['name']: v['answer'] for v in eff['forcing']['golden_family']}

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
    tc = collections.Counter(WORLD_CAUSE.get(f['cause'], f['cause']) for f in truth if C.to_local(f['t']).year == 2026)
    gc = collections.Counter(f['cause'] for f in gf if C.to_local(f['t']).year == 2026)
    worst = max(abs(tc.get(k, 0) - gc.get(k, 0)) for k in PS.G_CAUSES)
    ok('SF4 the golden\'s 2026 causes within 2 of the world\'s on every cause', worst <= 2, (dict(tc), dict(gc)))
    for yr in (2022, 2023, 2024, 2025):
        tcy = collections.Counter(WORLD_CAUSE.get(f['cause'], f['cause']) for f in truth if C.to_local(f['t']).year == yr)
        gcy = collections.Counter(f['cause'] for f in gf if C.to_local(f['t']).year == yr)
        wy = max(abs(tcy.get(k, 0) - gcy.get(k, 0)) for k in PS.G_CAUSES)
        # only 2026's causes are graded; before the stations (March 2023) the airport misses the line's fog, so earlier
        # years carry more unknowns
        ok('SF4 the golden\'s %d causes within 10 of the world\'s (ungraded)' % yr, wy <= 10, (dict(tcy), dict(gcy)))

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
    ok('X5 the tap line\'s string within a structure of the world\'s cracked string',
       len(tap) == 1 and abs(tap[0]['km'] - F.TAP_STRING_KM) <= 0.3, [(x['structure'], round(x['km'], 2)) for x in tap])

    # J1 the Gulf string: the golden flags the world's cracked string on the Gulf porcelain and no other place, and books
    # its flashovers as the world does
    gulf_cr = [(lid, no) for lid, no, onset, *_ in F.CRACKED if lid in F.GULF_LINES and no is not None
               and not any(k == (lid, no) for k in w['replaced'])]
    ok('J1 the golden flags the Gulf string and nothing else', [(s_['line'], s_['structure']) for s_ in g['strings']] == gulf_cr,
       (g['strings'], gulf_cr))
    t_ins = sorted(f['t'] for f in truth if f['cause'] == 'insulator' and (f['line'], f.get('string')) in [(a, b) for a, b in gulf_cr])
    g_ins = sorted(f['t'] for f in gf if f.get('gulf_string'))
    lost = [t for t in t_ins if not any(abs((t - u).total_seconds()) < 5 for u in g_ins)]
    extra_g = [u for u in g_ins if not any(abs((t - u).total_seconds()) < 5 for t in t_ins)]
    ok('J1 the string\'s flashovers booked as the world\'s, at most two left as salt (its first, before the evidence, and one '
       'placed by one end only)', len(lost) <= 2 and not extra_g,
       (len(lost), len(extra_g), len(t_ins)))
    ok('SF16 a place flagged as a cracked string under every low-deposit cut from 0.5 to 0.7 and with four required',
       all(fam_name in eff_fam and eff_fam[fam_name] == fig['work_list'] for fam_name in
           ('low flashovers: below half the median', 'low flashovers: below 0.7 of the median', 'low flashovers: four or more')))
    ok('J1 no salt flashover in the world below the porcelain\'s level (only the string flashes there)',
       all(f.get('deposit', 1) >= sim.CRIT for f in truth if f['cause'] == 'fog'))
    ok('J1 the reflex route books the string\'s flashovers as salt and files no Gulf string',
       not fig['careful']['R4'] and fig['gulf_string']['below_cut'] >= G.GOLD['low_n'] + 1, (fig['careful']['R4'], fig['gulf_string']))

    # J2 the conductor reaching the circuit under it: the golden flags exactly the world's underbuild span
    ub = [(lid, no) for lid, no, *_ in F.UNDERBUILD]
    ok('J2 the golden flags the world\'s underbuild span and nothing else',
       [(c['line'], c['s_min']) for c in g['contacts']] == ub, (g['contacts'], ub))
    gl_ub = [rl for rl in gr if rl['cause'] == 'hardware' and not rl['fixed']]
    ok('J2 its repeat location is equipment or hardware, not fixed (the trim does not touch it)',
       len(gl_ub) == 1 and gl_ub[0]['line'] == ub[0][0] and abs(gl_ub[0]['s_min'] - ub[0][1]) <= 1, [(x['line'], x['s_min']) for x in gl_ub])
    cc = fig['clearance_contact']
    ok('J2 the contact temperature since the trim flat, the grow-ins falling at least twice the cut',
       cc['slope_c_per_year'] >= G.GOLD['traj_slope'] / 2 and max(cc['vegetation_slopes']) <= 2 * G.GOLD['traj_slope'], cc)
    ok('J2 the reflex route clears the span instead', 'clear the span: Line 6, structures 57-58' in fig['careful']['work_list'])
    r2_alt = dict(fig['faults_2026_by_cause'])
    moved = r2_alt.get('hardware', 0) - sum(1 for f in gf if f['cause'] == 'hardware' and f.get('fixed_contact') and C.to_local(f['t']).year == 2026)
    ok('SF15 booking the clearance contacts as other or unknown keeps both cells inside their band of 3',
       abs(moved - r2_alt.get('hardware', 0)) <= 3, (moved, r2_alt.get('hardware')))

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
    ok('SF11 every section clear of the level by a fifth either way in truth',
       all(m >= 1.2 or m <= 0.8 for m in margins), sorted(round(m, 2) for m in margins if 0.8 < m < 1.2))
    # J3 the two sections washed before the blow: due in truth, due in every golden-family variant by 12 per cent, and
    # under the test insulators' average rate below the level
    res = fig['resalted']
    tr_m = {}
    for s_ in w['sections']:
        line = w['net']['lines'][s_['line']]
        sts = [x for x in line['structures'] if x['insulator'] == 'porcelain' and x['shore_km'] <= 6.0]
        cols = [k for k, x in enumerate(sts) if s_['s0'] <= x['no'] <= s_['s1']]
        tr_m['%s, Section %s' % (lname(s_['line']), s_['id'].split('-W')[1])] = float(w['deposits'][s_['line']][1][-1, cols].mean()) / sim.CRIT
    ok('J3 Line 2 sections 1 and 6 due in truth by a fifth', all(tr_m[k] >= 1.2 for k in res), {k: round(tr_m[k], 2) for k in res})
    fam_min = min(min(v['ratio_W1'], v['ratio_W6']) for v in eff['forcing']['golden_family'])
    ok('J3 every golden-family variant puts both at 1.12 times the level or more', fam_min >= 1.12, fam_min)
    ok('J3 the test insulators\' average rate leaves both below 0.88 of the level', max(fig['careful']['resalted_ratio']) <= 0.88,
       fig['careful']['resalted_ratio'])
    tests = [r_ for r_ in w['tests'] if r_['date'].year == 2026 and r_['date'].month == 10]
    ok('J3 every October test reading before the 23 October southerly', max(r_['date'] for r_ in tests) < dt.date(2026, 10, 23),
       max(r_['date'] for r_ in tests))
    ok('J3 the sections washed before the blow are the ones washed 1 to 22 October',
       sorted(res) == sorted(k for k, v in fig['wash_sections'].items() if v['last_wash'] and '2026-10-01' <= v['last_wash'] < '2026-10-23'))
    bands = fig['wash_deposit_bands']
    tr_d = {k: v * sim.CRIT for k, v in tr_m.items()}
    off = [k for k in bands if not (bands[k][0] * 0.9 <= tr_d[k] <= bands[k][1] * 1.1)]
    ok('J3 each section\'s true deposit inside its stated band (with a tenth either side)', not off,
       {k: (round(tr_d[k], 3), bands[k]) for k in off})
    ok('SF12 the golden\'s flashover level within a fifth of the porcelain\'s true level',
       abs(fig['flashover_level'] / sim.CRIT - 1) <= 0.2, fig['flashover_level'])
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
    for name in ('flashover level: lowest', 'flashover level: 5th percentile', 'flashover level: 20th percentile'):
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
    ok('the careful pass misses R4, R5 and R6 outright and the work list',
       care['R4'] != fig['gulf_strings'] and care['R5'] != fig['clearance_items'] and care['R6'] != fig['resalted_due']
       and care['work_list'] != fig['work_list'])
    om = eff.get('direct_route', {}).get('answer', [])
    ok('the direct route files all three open members wrong',
       'replace the string: Line 2, structure 63' not in om and 'restore the clearance: Line 6, structures 57-58' not in om
       and 'wash: Line 2, Section 6' not in om, om)

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
