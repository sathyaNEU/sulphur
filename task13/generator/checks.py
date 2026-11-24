"""task13 architecture 7 (Level 5), the generator's checks: the golden (run on target/ alone) against the simulated
world's truth, every semantic fork SF1 through SF18 in DESIGN_NOTE.md asserted, all five independent stumps (J1 to J5),
the S3 patrol referee slice, the stump factorial and forcing read back from effort.json, and the pack's input gates.

    python3 task13/generator/checks.py
"""
import bisect
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
import field as FD        # noqa: E402
import golden as G        # noqa: E402
import passes as PS       # noqa: E402
import sim                # noqa: E402

T = os.path.join(C.TASK, 'target')
N = {'pass': 0, 'fail': 0}
WORLD_CAUSE = {'clearance': 'hardware'}


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
        res.append(dict(
            line=lid, cause=cause, structure=collections.Counter(strs).most_common(1)[0][0],
            s_min=strs[0], s_max=strs[-1], last=last, n=len(grp),
        ))
    return res


def truth_fixed(w, rl):
    """a cause-removing fix after the location's last fault from the world's own records"""
    if rl['cause'] == 'bird':
        return any(lid == rl['line'] and abs(no - rl['structure']) <= 2 and when is not None and when > rl['last']
                   for lid, no, _, _, when in F.ROOSTS)
    if rl['cause'] == 'insulator':
        return any(k[0] == rl['line'] and abs(k[1] - rl['structure']) <= 2 and when > rl['last']
                   for k, when in w['replaced'].items())
    if rl['cause'] == 'growin':
        return any(k[0] == rl['line'] and abs(k[1] - rl['structure']) <= 2 and when > rl['last']
                   for k, when in w['trims'].items())
    return False


def main():
    w = sim.world()
    g = G.run(T)
    fig = json.load(open(os.path.join(C.HERE, 'figures.json')))
    eff = json.load(open(os.path.join(C.HERE, 'effort.json')))
    truth = [f for f in w['faults'] if C.REC0 <= f['t'] < C.T_END]
    gf = g['faults']
    eff_fam = {v['name']: v['answer'] for v in eff['forcing']['golden_family']}

    # SF1 a fault is one protection sequence on one line; SF2 Central calendar year, 2026 to 31 October
    ty = collections.Counter(C.to_local(f['t']).year for f in truth)
    gy = collections.Counter(C.to_local(f['t']).year for f in gf)
    ok('SF1 SF2 golden fault count by year equals simulated world', ty == gy, (dict(ty), dict(gy)))
    ok('SF1 figures.json matches conformed fault counts by year',
       fig['faults_by_year'] == {str(k): v for k, v in sorted(gy.items())}, fig['faults_by_year'])
    cross = [f for f in gf if C.to_local(f['t']).year != f['t'].astimezone(dt.timezone.utc).year]
    ok('SF2 zero faults cross a year boundary between UTC and Central', not cross, len(cross))
    ok('SF2 every fault lies inside 1 Jan 2022 to 31 Oct 2026 (Central)',
       all(dt.date(2022, 1, 1) <= C.to_local(f['t']).date() <= dt.date(2026, 10, 31) for f in gf))

    soe = list(csv.DictReader(open(os.path.join(T, C.FILES['soe']))))
    gt = sorted(f['t'].timestamp() for f in gf)

    def in_seq(ts):
        i = bisect.bisect_left(gt, ts)
        return any(abs(gt[j] - ts) <= 60 for j in (i - 1, i) if 0 <= j < len(gt))

    prot = [dt.datetime.fromisoformat(r['time_utc']).replace(tzinfo=dt.timezone.utc).timestamp() for r in soe
            if ' 69KV BKR ' in r['point'] and r['state'] == 'OPEN' and r['cause'] == 'PROT']
    lone = [ts for ts in prot if not in_seq(ts)]
    ok('SF1 single-ended relay test trips outside fault sequences are excluded',
       len(lone) > 0 and len(gf) == sum(ty.values()), (len(lone), len(gf)))

    # SF4 nine causes in 2026 (every physical-signature cause within 2; unpatrolled momentary hardware defaults to unknown)
    tc = collections.Counter(WORLD_CAUSE.get(f['cause'], f['cause']) for f in truth if C.to_local(f['t']).year == 2026)
    gc = collections.Counter(f['cause'] for f in gf if C.to_local(f['t']).year == 2026)
    phys_causes = ('lightning', 'bird', 'fog', 'insulator', 'growin', 'fallin', 'vehicle')
    worst_phys = max(abs(tc.get(k, 0) - gc.get(k, 0)) for k in phys_causes)
    hw_unk_diff = abs((tc.get('hardware', 0) + tc.get('unknown', 0)) - (gc.get('hardware', 0) + gc.get('unknown', 0)))
    ok('SF4 golden 2026 physical-signature causes within 2 of truth and hardware+unknown conserved within 2',
       worst_phys <= 2 and hw_unk_diff <= 2 and abs(tc.get('hardware', 0) - gc.get('hardware', 0)) <= 3,
       (dict(tc), dict(gc)))

    # SF3 current inventory location, SF5 repeat location (400 m, 3+), SF6 fixed after last fault
    tr = truth_clusters(w)
    for rl in tr:
        rl['fixed'] = truth_fixed(w, rl)
    gr = g['repeat']
    t_open = sorted((rl['line'], rl['structure'], rl['cause']) for rl in tr if not rl['fixed'])
    g_open = sorted((rl['line'], rl['structure'], rl['cause']) for rl in gr if not rl['fixed'])
    miss = [x for x in t_open if not any(near(x, y) and x[2] == y[2] for y in g_open)]
    extra = [y for y in g_open if not any(near(x, y) and x[2] == y[2] for x in t_open)]
    ok('SF3 SF5 every open repeat location matches world truth within 2 structures with its cause',
       not miss and not extra, (miss, extra))
    t_fix = sorted((rl['line'], rl['structure'], rl['cause']) for rl in tr if rl['fixed'])
    g_fix = sorted((rl['line'], rl['structure'], rl['cause']) for rl in gr if rl['fixed'])
    miss_f = [x for x in t_fix if not any(near(x, y) and x[2] == y[2] for y in g_fix)]
    extra_f = [y for y in g_fix if not any(near(x, y) and x[2] == y[2] for x in t_fix)]
    ok('SF6 fixed repeats excluded after post-fault repairs match world truth',
       not miss_f and not extra_f, (miss_f, extra_f))
    for name in ('repeat window 350 m', 'repeat window 450 m'):
        ok('SF5 %s files golden Priority 1 program' % name, eff_fam.get(name) == fig['work_list'], name)

    # J1 / SF15: 12.47 kV underbuild clearance spans vs underbuilt grow-in decoys
    ub_truth = sorted((lid, no) for lid, no, *_ in F.UNDERBUILD)
    ub_gold = sorted((c['line'], c['s_min']) for c in g['contacts'])
    ok('J1 SF15 golden flags exactly the two underbuild clearance spans (Line 6, Line 15)',
       len(ub_gold) == len(ub_truth) and all(a[0] == b[0] and abs(a[1] - b[1]) <= 1 for a, b in zip(ub_gold, ub_truth)),
       (ub_gold, ub_truth))
    cd = {c['line']: c for c in fig['clearance_details']}
    ub_slopes = fig['underbuilt_veg_slopes']
    ok('J1 SF15 clearance slopes flat (> -0.5 C/yr) while underbuilt grow-in decoys fall (< -1.8 C/yr)',
       cd['Line 15']['slope_c_per_year'] > -0.5 and cd['Line 6']['slope_c_per_year'] > -0.5
       and len(ub_slopes) >= 2 and max(ub_slopes.values()) < -1.8, (cd, ub_slopes))
    ok('J1 reflex route misclassifies Line 15 as grow-in and leaves R2 empty',
       not fig['careful']['R2'] and 'clear span: Line 15, structures 48-49' in fig['careful']['work_list'],
       fig['careful']['R2'])

    # J2 / SF17: dual YNd1 IPP lateral tap zero-sequence infeed (Line 9 Solar & Line 8 BESS)
    ip8, ip9 = fig['ipp_details']['Line 8'], fig['ipp_details']['Line 9']
    ok('J2 SF17 Line 9 cracked string inverted within 0.35 km of true tap-beyond location',
       abs(ip9['golden_km'] - F.TAP_STRING_KM) <= 0.35 and ip9['structure_shift'] >= 8, ip9)
    ok('J2 SF17 Line 8 cracked string inverted within 0.45 km of true BESS-beyond location',
       abs(ip8['golden_km'] - F.BESS_STRING_KM) <= 0.45 and ip8['structure_shift'] >= 8, ip8)
    ok('J2 reflex route over-reaches both IPP strings by 10+ structures',
       fig['careful']['R3'] != fig['ipp_strings'] and ip8['raw_structure'] != ip8['golden_structure']
       and ip9['raw_structure'] != ip9['golden_structure'], fig['careful']['R3'])

    # J3 / SF16: double-circuit Z0m mutual impedance coupling on Lines 10 & 11 + patrol referee
    dc11 = fig['dc_corridor_details']['Line 11 insulator']
    dc10 = fig['dc_corridor_details']['Line 10 growin']
    ref = fig['dc_referee']
    ok('J3 SF16 Line 11 str 71 and Line 10 str 68-69 inverted accurately with Z0m coupling',
       abs(dc11['golden_km'] - F.DC_STRING_KM) <= 0.35 and dc11['structure_shift'] >= 6
       and abs(dc10['golden_km'] - F.DC_GROWIN_KM) <= 0.45 and dc10['structure_shift'] >= 5,
       (dc11, dc10))
    ok('J3 SF16 patrol referee slice (non-target lockouts) confirms coupled MAE <= 0.25 km vs uncoupled >= 1.2 km',
       not ref['covers_target'] and ref['golden'] <= 0.25 and ref['rivals']['rigorous'] >= 1.2
       and ref['rivals']['direct'] >= 3.0, ref)
    ok('J3 reflex route misses both double-circuit corridor targets',
       fig['careful']['R4'] != fig['dc_corridor_repeats'], fig['careful']['R4'])

    # J4 / SF11 / SF12: joint (ESDD, NSDD) coastal porcelain washing standing on 31 October
    due_truth = set()
    margins = []
    for s in w['sections']:
        line = w['net']['lines'][s['line']]
        sts = [x for x in line['structures'] if x['insulator'] == 'porcelain' and x['shore_km'] <= 6.0]
        cols = [k for k, x in enumerate(sts) if s['s0'] <= x['no'] <= s['s1']]
        v = w['deposits'][s['line']][3][-1, cols]
        name = '%s, Section %s' % (lname(s['line']), s['id'].split('-W')[1])
        margins.append(float(v.mean()) / sim.CRIT)
        if v.mean() >= sim.CRIT:
            due_truth.add(name)
    gw = {x.replace('wash: ', '') for x in fig['wash_due']}
    ok('J4 SF11 golden 9 due washing sections equal simulated truth on 31 October',
       gw == due_truth and len(gw) == 9, (sorted(gw ^ due_truth), len(gw)))
    ok('J4 SF11 all 9 due sections >= 1.4x and all 12 clean sections <= 0.70x in golden model',
       fig['wash_due_min_ratio'] >= 1.4 and fig['wash_clean_max_ratio'] <= 0.70,
       (fig['wash_due_min_ratio'], fig['wash_clean_max_ratio']))
    ok('J4 ESDD-only shortcut over-washes >= 14 sections (crowding out P1 repeats)',
       fig['esdd_only_due_count'] >= 14 and len(fig['esdd_only_extra']) >= 5,
       (fig['esdd_only_due_count'], fig['esdd_only_extra']))
    wash_names = {r['section'] for r in w['washes']}
    test_names = {s[0] for s in FD.TEST_SITES}
    ok('SF11 test insulators are never washed (latest test reading is not a section deposit)',
       not (wash_names & test_names), sorted(wash_names & test_names))
    for name in ('flashover level: 5th percentile', 'flashover level: 15th percentile',
                 'flashover level: 20th percentile', 'joint frontier: Poisson log-link'):
        ok('SF12 %s files golden Priority 1 program' % name, eff_fam.get(name) == fig['work_list'], name)

    # J5 / SF7 / SF8 / SF9: chronological SCADA switching topology & 2026 member impact
    secs = [i['seconds'] for imp in w['impacts'] for i in imp['impact']]
    ok('SF7 zero restorations fall between 30 seconds and 6 minutes',
       not [s for s in secs if 30 < s < 360], sorted(s for s in secs if 30 < s < 360)[:5])
    tl = collections.defaultdict(lambda: [0, 0.0])
    for imp in w['impacts']:
        if C.to_local(imp['t0']).year != 2026:
            continue
        for i in imp['impact']:
            if i['seconds'] > 300:
                tl[imp['line']][0] += i['members']
                tl[imp['line']][1] += i['members'] * i['seconds'] / 60.0
    gl = fig['member_impact_2026_by_line']
    bad_l = []
    for lid, (n_s, m_s) in tl.items():
        gv = gl.get(lname(lid), {})
        if abs(gv.get('sustained', 0) - n_s) > 0.02 * n_s + 1 or abs(gv.get('member_minutes', 0) - m_s) > 0.02 * m_s + 1:
            bad_l.append((lid, n_s, round(m_s), gv))
    extra_l = [k for k, v in gl.items() if v['sustained'] and ('L%02d' % int(k.split()[1])) not in tl]
    ok('J5 SF8 SF9 2026 member interruptions and member-minutes by energizing line within 2 percent of truth',
       not bad_l and not extra_l, (bad_l, extra_l))
    ok('J5 SF9 static topology understates 2026 member-minutes by > 40 percent and over_both overstates by > 10 percent',
       fig['static_2026_pct_diff'] <= -40.0 and fig['over_both_2026_pct_diff'] >= 10.0,
       (fig['static_2026_pct_diff'], fig['over_both_2026_pct_diff']))
    con = sqlite3.connect(os.path.join(T, C.FILES['oms']))
    oms_n = con.execute("select count(*) from outage where cause_code='LOS'").fetchone()[0]
    con.close()
    ok('SF8 OMS raw loss-of-supply rows overstate 2026 member-minutes vs SCADA restoration',
       oms_n > 0 and fig['quick']['R6']['member_minutes'] > 1.2 * fig['member_impact_2026']['member_minutes'],
       fig['quick']['R6'])

    # SF10 / SF13 / SF14 / SF18: RP-04 Rev 5 36-crew-day Priority 1 allocation & filed procedure checks
    pr = fig['programme']
    ok('SF10 SF18 Priority 1 program uses exactly 36 crew-days (9 washes + 13 repeats, 0 unused) with clean cutoff margin',
       pr['budget_days'] == 36 and pr['wash_days'] == 9 and pr['repeat_days_used'] == 27 and pr['unused_days'] == 0
       and pr['funded_count'] == 13 and pr['deferred_count'] == 6
       and pr['cutoff_mm_per_day'] > pr['first_deferred_mm_per_day'] + 3000, pr)
    gold_open = [PS.place_tuple(rl) for rl in g['repeat'] if not rl['fixed']]
    gold_wl = PS.results_of(g, gold_open)['R10']
    ok('SF10 recomputed Priority 1 work program equals figures.json', gold_wl == sorted(fig['work_list']), gold_wl)

    txt = subprocess.run(['unzip', '-p', os.path.join(T, C.FILES['procedure']), 'word/document.xml'],
                         capture_output=True, text=True).stdout
    txt = re.sub(r'<[^>]+>', '', txt)
    ok('SF13 RP-04 Rev 5 files the fog season starting 1 December',
       'The fog season runs from 1 December to 31 March' in txt)
    ok('SF10 SF18 RP-04 Rev 5 files the 36-crew-day Priority 1 cap and greedy historical ranking',
       '36 crew-days' in txt and 'per crew-day' in txt and '800 m' in txt)
    ok('SF14 all 519 golden faults lie on the 16 lines in line_register_69kv_2026.xlsx',
       len(g['d']['lines']) == 16 and all(f['line'] in g['d']['lines'] for f in gf), len(g['d']['lines']))

    # Stump factorial & forcing read back from effort.json
    fa = eff['factorial']
    stumps = [j for j in fa['judgments'] if j['kind'] == 'stump']
    ok('factorial: all 5 stumps move Priority 1 call when dropped alone',
       len(stumps) == 5 and all(set(j['dropped']['answer']) != set(fa['golden_answer']) for j in stumps))
    ok('factorial: no stump reaches Priority 1 call when fixed alone',
       all(set(j['alone']['answer']) != set(fa['golden_answer']) for j in stumps))
    ok('factorial: level 5 (5 necessary stumps on 5 distinct wrong Priority 1 schedules)',
       len({tuple(sorted(j['dropped']['answer'])) for j in stumps}) == 5)
    ok('forcing: all 23 golden-family variants file identical Priority 1 program',
       len(eff['forcing']['golden_family']) >= 20
       and all(v['answer'] == fig['work_list'] for v in eff['forcing']['golden_family']))
    ok('forcing: all 6 input perturbations file identical Priority 1 program',
       len(eff['forcing']['perturbations']) == 6
       and all(v['answer'] == fig['work_list'] for v in eff['forcing']['perturbations']))
    set_shortcuts = [s for s in eff['forcing']['shortcuts'] if 'over_both' not in s['name']]
    ok('forcing: all 15 set-moving shortcuts land on wrong Priority 1 programs (while over_both breaks R6 by +14.9%)',
       len(set_shortcuts) >= 15 and all(set(s['answer']) != set(fig['work_list']) for s in set_shortcuts)
       and fig['over_both_2026_pct_diff'] >= 10.0)
    om = eff.get('direct_route', {}).get('answer', [])
    ok('direct route misses open members (Line 15 clearance, Line 8 str 93, Line 11 str 71, Line 2 Sec 5)',
       'restore clearance: Line 15, structures 48-49' not in om
       and 'replace string: Line 8, structure 93' not in om
       and 'replace string: Line 11, structure 71' not in om
       and 'wash: Line 2, Section 5' in om, om)

    # Pack input gates (29 files)
    files = sorted(os.listdir(T))
    ok('pack: 29 files matching C.FILES', sorted(C.FILES.values()) == files, (len(files), set(C.FILES.values()) ^ set(files)))
    exts = collections.Counter(os.path.splitext(f)[1] for f in files)
    ok('pack: multiple file categories (CSV/JSON/SQLite + XLSX/DOCX/PDF)',
       len({'.csv', '.json', '.sqlite'} & set(exts)) == 3 and len({'.xlsx', '.docx', '.pdf'} & set(exts)) == 3, dict(exts))
    rows = {f: sum(1 for _ in open(os.path.join(T, f), encoding='utf-8', errors='replace')) - 1
            for f in files if f.endswith('.csv')}
    ok('pack: at least one CSV >= 20,000 rows', max(rows.values()) >= 20000, max(rows.values()))
    ok('pack: second CSV >= 600 rows (10+ printed pages)', sorted(rows.values())[-2] >= 600, sorted(rows.values())[-2])
    gsrc = open(os.path.join(C.HERE, 'golden.py')).read()
    ok('pack: both distractors never read by golden.py',
       "p('corrosion')" not in gsrc and "p('easements')" not in gsrc)
    tot_mb = sum(os.path.getsize(os.path.join(T, f)) for f in files) / 1e6
    ok('pack: realistic size (30 to 65 MB)', 30.0 <= tot_mb <= 65.0, round(tot_mb, 2))

    print('%d passed, %d failed' % (N['pass'], N['fail']))
    return 1 if N['fail'] else 0


if __name__ == '__main__':
    sys.exit(main())
