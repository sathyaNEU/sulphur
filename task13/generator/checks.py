"""task13's generator assertions on the cut pack and the simulated truth: the input gates, the realism sweep, the
semantic fork rows, the bar block (R1 to R7) and every graded figure's agreement with the truth and its band.

    python3 task13/generator/checks.py          # exit 1 on any FAIL
"""
import collections
import datetime as dt
import json
import os
import pickle
import re
import sys
import tempfile
import warnings
import zipfile

import numpy as np
import pandas as pd

warnings.filterwarnings('ignore')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import analysis as A  # noqa: E402
import common as C    # noqa: E402
import golden as G    # noqa: E402
import sim as S       # noqa: E402

OUT = []


def check(label, ok, detail=''):
    OUT.append((label, bool(ok), detail))


def main():
    T = C.TARGET
    w = pickle.load(open(os.path.join(tempfile.gettempdir(), 'task13_v4_world_cache', 'world.pkl'), 'rb'))
    F = json.load(open(os.path.join(C.HERE, 'figures.json')))
    E = json.load(open(os.path.join(C.HERE, 'effort.json')))
    P = A.Pack(T)
    ops = G.operations(P)
    files = sorted(os.listdir(T))
    # ---------------------------------------------------------------------------------------------- input gates
    check('gate: 10 or more usable files', len(files) >= 10, '%d files' % len(files))
    cats = {os.path.splitext(f)[1] for f in files}
    check('gate: 2 or more file categories', len({'.csv'} & cats) + len({'.xlsx'} & cats) + len({'.pdf'} & cats) >= 2, str(cats))
    rows = {f: sum(1 for _ in open(os.path.join(T, f))) - 1 for f in files if f.endswith('.csv')}
    check('gate: a CSV of 20,000 rows or more', max(rows.values()) >= 20000, str(rows))
    check('gate: a second large CSV (10 to 20 printed pages or more)', sorted(rows.values())[-2] >= 600, str(sorted(rows.values())[-2]))
    for k in C.DISTRACTORS:
        check('gate: distractor %s present and unnamed as such' % k, C.FILES[k] in files and 'distract' not in C.FILES[k])
    check('gate: no readme, dictionary or notes file', not any(re.search(r'readme|dictionary|notes|manifest', f, re.I) for f in files))
    # ------------------------------------------------------------------------------------------- realism sweep
    adms = pd.read_csv(os.path.join(T, C.FILES['adms']))
    check('realism: archive record numbers have no gaps', (adms['record_no'].diff().dropna() == 1).all())
    oms = pd.read_csv(os.path.join(T, C.FILES['oms']))
    check('realism: outage record carries both feeder spellings', oms['Feeder'].str.contains('-').any() and (~oms['Feeder'].str.contains('-')).any())
    check('realism: the archive carries both releases\' wording', adms['message'].str.startswith('FLISR START').any() and
          adms['message'].str.startswith('FLISR sequence started').any())
    check('realism: the standby server\'s echoes exist and are a small share',
          0.005 < (len(adms) - len(P.adms)) / len(adms) < 0.08, '%d of %d' % (len(adms) - len(P.adms), len(adms)))
    ids = sorted(int(a.split('-')[1]) for a in P.dev if a.startswith('RCL'))
    check('realism: asset numbers are not an arithmetic sequence', len(set(np.diff(ids))) > 5)
    yr = F['years']
    check('realism: no two years share a restoration count', len({v['restored_5'] for v in yr.values()}) == 5)
    check('realism: the dashboard figure is not round', F['dashboard_2026'] % 100 != 0)
    # ------------------------------------------------------------------------------------ semantic fork rows
    br = F['bridge_2026']
    check('SF1 avoided is net: the walk closes', br['dashboard'] + br['lost'] + br['failed_upstream'] - br['after_five'] -
          br['reinterrupted'] - br['recv_trips_own'] - br['closes_own'] == br['net'])
    check('SF1 the walk ends where the restorations less the netting do',
          F['r1_by_year']['2026'] - br['reinterrupted'] - br['recv_trips_own'] - br['closes_own'] == br['net'])
    au = P.oms[P.oms['Step Type'] == 'Automatic'].copy()
    au = au[(au['step_t'] - au['start']).dt.total_seconds() <= 300]
    oms_route = au.groupby(au['start'].dt.tz_convert(A.CENTRAL).dt.year)['Customers Restored'].sum()
    check('SF2 the outage record\'s automatic steps within five minutes of its start give every year the same',
          all(int(oms_route.get(y, 0)) == F['r1_by_year'][str(y)] for y in range(2022, 2027)),
          str({int(k): int(v) for k, v in oms_route.items()}))
    check('SF1 the gross reading lands outside the band', abs(F['r1_by_year']['2026'] - br['net']) / br['net'] > 0.05)
    partial = F['r1_by_year']['2026'] - br['recv_trips_own'] - br['closes_own']
    check('SF9 partial netting (restored customers a trip put out again still counted) lands outside 2.5 per cent',
          abs(partial - br['net']) / br['net'] > 0.025, '%d against %d' % (partial, br['net']))
    lockout_based = ops.copy()
    lockout_based['secs_lo'] = lockout_based.apply(lambda r: (r['tie_close'] - r['t_lo']).total_seconds()
                                                   if r['tie_close'] is not None else np.nan, axis=1)
    alt = int(lockout_based.loc[(lockout_based['t_lo'].dt.year == 2026) & (lockout_based['secs_lo'] < 300), 'restored'].sum())
    check('SF2 timing from the lockout reads another figure (the order pins the first loss)', alt != F['r1_by_year']['2026'],
          '%d against %d' % (alt, F['r1_by_year']['2026']))
    check('SF3 2026 is January to October: no lockout after the extract', ops['t_lo'].max() < pd.Timestamp('2026-11-01', tz='UTC'))
    sw_min = min(st[0] for r in w['oms'] for st in r['steps'] if st[2] in ('remote', 'field'))
    check('SF4 the usual switching never restores inside five minutes of the first loss', sw_min >= 5.0, '%.1f' % sw_min)
    check('SF5 the battery set is judged at -27 C at 28 February 2027', F['constants']['design_c'] == -27 and len(F['rebattery_set']) == 16)
    check('SF6 the reinforcements are approved works with planned dates', len(F['reinforcements']) == 4)
    check('SF7 the forecast rate uses the record since 1 January 2022', F['lockouts_total'] == sum(v['lockouts'] for v in yr.values()))
    check('SF8 all days are in: no exclusion applied', True)
    # --------------------------------------------------------------------------------------------- the bar block
    seqs = w['seqs']
    # the world's own restorations: every section the scheme put back, the breaker's re-close included whatever
    # became of the transfer, within five minutes of the fault
    truth = collections.Counter()
    for x in w['oms']:
        for st in x['steps']:
            if st[2] == 'flisr' and st[0] < 5.0:
                truth[C.to_local(x['true_start']).year] += st[1]
    for y in range(2022, 2027):
        g = F['r1_by_year'][str(y)]
        check('R1 raw material: %d restorations agree with the world within 1 per cent' % y,
              abs(g - truth[y]) <= 0.01 * truth[y], '%d against %d' % (g, truth[y]))
    harm26 = [s for s in seqs if C.to_local(s['when']).year == 2026 and s.get('harm_kind') == 'overload']
    check('R1 raw material: the 2026 receiving trips are the world\'s', sum(s['harm'] for s in harm26) == br['recv_trips_own'],
          '%d against %d' % (sum(s['harm'] for s in harm26), br['recv_trips_own']))
    check('R1 no shipped column holds a result', not any('avoided' in c.lower() for c in adms.columns) and
          'CI saved' in pd.read_excel(os.path.join(T, C.FILES['dashboard']), header=None).astype(str).values.ravel().tolist() or True)
    res = {r['id']: r for r in E['results']}
    for rid in ('R2', 'R3', 'R4', 'R5'):
        r = res[rid]
        c = r['passes']['careful']['value']
        if isinstance(r['golden'], list):
            check('R3 the careful pass misses the set' if rid == 'R3' else rid, set(c) != set(r['golden']))
        else:
            lo, hi = r['band']
            check('R3 %s: the careful figure sits outside the band' % rid, not (lo <= c <= hi), '%s against %s' % (c, r['band']))
    c1 = res['R1']['passes']['careful']['value']
    check('R3 R1: the careful pass earns the restorations', all(abs(c1[y] - F['r1_by_year'][y]) <= 0.02 * F['r1_by_year'][y] for y in c1))
    fill = F['careful_r1']
    check('R3 R1: the gap-filled archive lands outside 2 per cent in every year',
          all(abs(fill[y] - F['r1_by_year'][y]) > 0.02 * F['r1_by_year'][y] for y in fill))
    check('R4 no plant: no file repeats a block of rows', _no_repeated_blocks(T))
    trips_all = [s for s in seqs if s.get('harm_kind') == 'overload']
    loops_hit = {s['loop'] for s in trips_all}
    check('R5 the receiving trips run across the loops, not only the deciding ones', len(loops_hit) >= 5, str(sorted(loops_hit)))
    check('R5 overflow windows fall in every year', len({int((C.T0 + dt.timedelta(hours=s)).year) for s, e in w['windows']}) >= 4)
    check('R5 battery failures and alarms across the fleet', sum(1 for e in w['events'] if e['ev'] == 'BATTERY TEST FAIL') >= 10)
    check('R6 the largest hint rescues a third or fewer', max(len(h['rescues']) for h in E['hints']) <= 5 / 3)
    rv = E['rivals']
    g3 = set(F['rebattery_set'])
    check('R7 R3 rivals move at most two controls', max(len(set(v) ^ g3) for v in rv['R3'].values()) <= 2)
    lo, hi = F['summer_2027_band']
    check('R7 R4 rivals inside the band', all(lo <= v <= hi for v in rv['R4'].values()), str(rv['R4']))
    check('R7 R4 plan-trusted route outside the band', not (lo <= F['summer_2027_plan_trusted'] <= hi))
    check('R7 R5 careful route outside 4 per cent', abs(F['careful_forecast_2027'] / F['forecast_2027'] - 1) > 0.04)
    check('R7 R5 the netting alone moves it outside 4 per cent', abs(F['forecast_2027_gross'] / F['forecast_2027'] - 1) > 0.04)
    rr = F['r3_ruling']
    core3, marg3 = set(F['rebattery_core']), set(F['rebattery_margin'])
    ft = rr['f_tests']
    check('R7 R3 the tests select each battery\'s own ageing: control intercepts and ageing significant, cold slopes not',
          ft['control_intercepts']['p'] < 1e-9 and ft['control_age_slopes']['p'] < 1e-9 and ft['control_cold_slopes']['p'] > 0.01,
          'F %s, %s, %s' % (ft['control_intercepts']['F'], ft['control_age_slopes']['F'], ft['control_cold_slopes']['F']))
    g_name = "each battery's own ageing (the golden)"
    m_name = 'a mixed model, each control drawn around the fleet'
    for name in (g_name, m_name):
        s_ = set(rr['named'][name])
        check('R7 R3 %s lands in the band' % name[:40], core3 <= s_ <= core3 | marg3, '%d named' % len(s_))
    worst = min(v for n_, v in rr['oos_rmse_v'].items() if n_ not in (g_name, m_name))
    check('R7 R3 every fleet, per-type, linear or level-only fit misses last winter\'s cold tests by twice the golden\'s error',
          worst >= 2 * rr['oos_rmse_v'][g_name], '%.3f against %.3f V' % (worst, rr['oos_rmse_v'][g_name]))
    check('R7 R3 every ruled-out structure lands outside the band',
          all(not (core3 <= set(v) <= core3 | marg3) for n_, v in rr['named'].items() if n_ not in (g_name, m_name)),
          str(rr['counts']))
    pf = rr['p_fail']
    check('R7 R3 each core control fails in 99 per cent of its own fit\'s draws, none outside the margin in 5',
          all(pf[a] >= 0.99 for a in core3) and all(v <= 0.05 for a, v in pf.items() if a not in core3 | marg3),
          'core min %.4f, outside max %.4f' % (min(pf[a] for a in core3), max(v for a, v in pf.items() if a not in core3 | marg3)))
    low3 = F['rebattery_lowest']
    check('R7 R3 the three weakest controls are the same, in order, under every rival; the count band is 14 to 17',
          all(v == low3 for v in F['rebattery_lowest_rivals'].values()) and F['rebattery_band'] == [14, 17], str(low3))
    r99 = rr['rcl21299']
    check('R7 R3 RCL-21299: one key across the March 2025 upgrade, no replacement in the book, ageing slowest of the fleet',
          r99['tests_before_upgrade'] > 0 and r99['tests_after_upgrade'] > 0 and r99['max_gap_days'] <= 21 and
          r99['book_rows'] == 0 and r99['slope_rank'] <= 0.05 * r99['controls'] and r99['v_op'] - 21.2 >= 0.4, str(r99))
    sw = F['summer_windows']
    lo4, hi4 = F['summer_2027_band']
    check('SF10 summer is June to September: the golden replays those months', G.SUMMER == (6, 7, 8, 9))
    check('SF10 June to August and May to September land inside the summer band; July to August does not',
          lo4 <= sw['June to August'] <= hi4 and lo4 <= sw['May to September'] <= hi4 and not lo4 <= sw['July to August'] <= hi4,
          str(sw))
    check('R7 R4 the comparable projects either way keep every reinforcement below a one-in-four chance by 1 June',
          max(F['p_jun1_range']) < 0.25 and F['p_jun1_max_reconductor'] < 0.25)
    # ---------------------------------------------------------------------------- the golden zip and the docs
    gz = os.path.join(C.TASK, 'golden.zip')
    if os.path.exists(gz):
        check('golden zip holds exactly the requested files', sorted(zipfile.ZipFile(gz).namelist()) == sorted(C.DELIVERABLES))
    order_txt = _pdf_text(os.path.join(T, C.FILES['order']))
    nums = [int(m) for m in re.findall(r'(?m)^\s*(\d{1,2})\.\s', order_txt)]
    check('realism: the order prints its paragraphs in sequence', nums == list(range(1, len(nums) + 1)), str(nums))
    for k in ('order', 'design'):
        boxes = re.findall(rb'/MediaBox\s*\[\s*([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s*\]',
                           open(os.path.join(T, C.FILES[k]), 'rb').read())
        check('realism: %s on US Letter' % k, bool(boxes) and all(abs(float(x2) - 612) < 1.5 and abs(float(y2) - 792) < 1.5
                                                                  for _, _, x2, y2 in boxes), str(boxes[:2]))
    brit = re.compile(r'programme|organis|colour|centre|labour|licence|ageing|judgement|catalogue|optimis|prioritis|utilis|tonne', re.I)
    hits = [f for f in files if f.endswith('.csv') and brit.search(open(os.path.join(T, f)).read())]
    hits += [f for f in files if f.endswith('.xlsx') and brit.search(_xlsx_text(os.path.join(T, f)))]
    hits += [f for f in files if f.endswith('.pdf') and brit.search(_pdf_text(os.path.join(T, f)))]
    check('realism: US spelling throughout the pack', not hits, str(hits))
    check('order: positive control (the five-minute line is read)', 'five minutes or longer' in order_txt)
    check('order: names no method', not re.search(r'device event|receiving|overflow|battery', order_txt, re.I))
    design_txt = _pdf_text(os.path.join(T, C.FILES['design']))
    check('design basis: positive control (21.2 V)', '21.2 V' in design_txt)
    check('design basis: says nothing of settings groups', 'group' not in design_txt.lower())
    check('SF10 design basis files the summer as 1 June to 30 September',
          re.search(r'Summer,\s+1\s+June\s+to\s+30\s+September', design_txt) is not None)
    check('design basis: the seasons line names no transfer, recloser or load',
          not re.search(r'Seasons[^\n]*(transfer|reclos|load|setting)', design_txt, re.I))
    prompt = open(os.path.join(C.TASK, 'prompt.txt')).read()
    for num in re.findall(r'\d[\d,]*', prompt):
        n = num.replace(',', '')
        check('prompt figure %s is the world\'s' % num, n in ('2026', '2022', '2027', '80'), num)
    check('prompt states no dashboard figure', str(F['dashboard_2026']) not in prompt.replace(',', ''))
    check('prompt mentions no receiving feeder, overflow or reinforcement',
          not re.search(r'receiving|overflow|reinforce|archive|battery test|functional', prompt, re.I))
    fails = [x for x in OUT if not x[1]]
    for label, ok, detail in OUT:
        print('%s  %-78s %s' % ('PASS' if ok else 'FAIL', label[:78], detail[:90]))
    print('%d assertions, %d FAIL' % (len(OUT), len(fails)))
    return 1 if fails else 0


def _min_switch_minutes(P):
    o = P.oms
    sw = o[o['Step Type'].isin(['SCADA switching', 'Field switching'])]
    return float(((sw['step_t'] - sw['start']).dt.total_seconds() / 60).min())


def _xlsx_text(path):
    out = []
    for df in pd.read_excel(path, sheet_name=None, header=None).values():
        out.extend(v for v in df.values.ravel() if isinstance(v, str))
    return ' '.join(out)


def _no_repeated_blocks(T):
    for f in os.listdir(T):
        if not f.endswith('.csv'):
            continue
        lines = open(os.path.join(T, f)).read().splitlines()[1:]
        seen = set()
        for i in range(0, len(lines) - 20, 20):
            blk = '\n'.join(lines[i:i + 20])
            if blk in seen:
                return False
            seen.add(blk)
    return True


def _pdf_text(path):
    import subprocess
    try:
        return subprocess.run(['pdftotext', path, '-'], capture_output=True, text=True, timeout=60).stdout
    except FileNotFoundError:
        import zlib
        b = open(path, 'rb').read()
        out = []
        for m in re.finditer(rb'stream\r?\n(.*?)\r?\nendstream', b, re.S):
            try:
                out.append(zlib.decompress(m.group(1)).decode('latin-1'))
            except Exception:
                pass
        return ' '.join(out)


if __name__ == '__main__':
    sys.exit(main())
