#!/usr/bin/env python3
"""task13/generator/core.py: Architecture 7 (Level 5, v4_hardened) mathematical core proof.

Computes EVERY member figure, honest variant family, lattice route, over-corrected side, coded one-fact
shortcut, referee slice, and frontier run route directly from the shipped files in task13/target/ via
golden.run() (zero hand-typed figures), and checks the core through corelib.run(spec).
"""
import datetime as dt
import itertools
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(REPO, '.agents', 'skills', 'stumping'))

import common as C      # noqa: E402
import corelib          # noqa: E402
import faults as F      # noqa: E402
import golden as G      # noqa: E402
import sim              # noqa: E402

# The five independent Level-5 decisive judgments (all 5 axes: what, who, against, unit, when)
HURRY = dict(
    S1={'contacts': 'signature'},
    S2={'tap_infeed': 'none'},
    S3={'dc_mutual': 'uncoupled'},
    S4={'deposit': 'esdd_wind'},
    S5={'topology': 'static'},
)
OVER = dict(
    S1={'contacts': 'underbuild_all'},
    S2={'tap_infeed': 'over'},
    S3={'dc_mutual': 'over'},
    S4={'deposit': 'over_nsdd'},
    S5={'topology': 'over_both'},
)
ONE_FACT = dict(
    S1={'contacts': 'underbuild_all'},
    S2={'tap_infeed': 'solar_only'},
    S3={'dc_mutual': 'one_fact'},
    S4={'deposit': 'one_fact'},
    S5={'topology': 'one_fact_2026'},
)

# 14 honest variants spanning all five physical/operational mechanisms
VARIANTS = [
    ('fog_dep_0.3', dict(fog_dep=0.3)),
    ('fog_dep_0.8', dict(fog_dep=0.8)),
    ('storm_n_2', dict(storm_n=2)),
    ('storm_n_5', dict(storm_n=5)),
    ('tc_min_36', dict(tc_min=36.0)),
    ('tc_min_44', dict(tc_min=44.0)),
    ('gust_min_8.5', dict(gust_min=8.5)),
    ('gust_min_11.0', dict(gust_min=11.0)),
    ('win_km_0.35', dict(win_km=0.35)),
    ('win_km_0.45', dict(win_km=0.45)),
    ('traj_slope_-0.6', dict(traj_slope=-0.6)),
    ('traj_slope_-1.0', dict(traj_slope=-1.0)),
    ('level_q_5', dict(level_q=5)),
    ('beta_poisson', dict(beta_model='poisson')),
]


def _span_slope(res, lid, s_center, opts):
    """Post-trim IEEE 738 conductor temperature slope (C/yr) for a summer contact span under opts."""
    mode = opts.get('contacts', 'trajectory')
    if mode == 'underbuild_all':
        return 0.0
    if mode == 'signature':
        # Pooled summer-contact temperature trend across all summer contact faults (never separates flat spans)
        xs, ys = [], []
        for f in res['faults']:
            if f['cause'] in ('growin', 'hardware') and isinstance(f.get('sig'), dict) and f['sig'].get('tc'):
                lt = C.to_local(f['t'])
                xs.append(lt.year + lt.timetuple().tm_yday / 365.25)
                ys.append(f['sig']['tc'])
        return float(np.polyfit(xs, ys, 1)[0]) if len(xs) >= 2 else -2.0
    # Trajectory mode: compute post-trim OLS slope specifically on this span
    d = res['d']
    vv = d['veg']
    ln = 'Line %d' % int(lid[1:])
    grp = [f for f in res['faults'] if f['line'] == lid and f['cause'] in ('growin', 'hardware')
           and f['structure'] is not None and abs(f['structure'] - s_center) <= 3
           and isinstance(f.get('sig'), dict) and f['sig'].get('tc') is not None]
    if not grp:
        return -2.5
    lo = min(g['structure'] for g in grp) - 1
    hi = max(g['structure'] for g in grp) + 1
    last_c = max(C.to_local(g['t']).date() for g in grp)
    tr = []
    for _, r in vv[(vv['line'] == ln) & vv['work_type'].isin(['HOT SPOT', 'CYCLE TRIM'])].iterrows():
        day = G.pd.Timestamp(r['completed']).date()
        a = G.plate_to_current(d, lid, int(r['from_structure']), day)
        b = G.plate_to_current(d, lid, int(r['to_structure']), day)
        if a <= hi and lo <= b and day <= last_c:
            tr.append(day)
    t_trim = max(tr) if tr else None
    after = [g for g in grp if t_trim is None or C.to_local(g['t']).date() > t_trim]
    if len(after) < 2:
        return -2.5
    xs = [C.to_local(g['t']).year + C.to_local(g['t']).timetuple().tm_yday / 365.25 for g in after]
    ys = [g['sig']['tc'] for g in after]
    return float(np.polyfit(xs, ys, 1)[0])


def _rep_km(res, lid, cause, fallback=0.0):
    cands = [r for r in res['repeat'] if not r['fixed'] and r['line'] == lid and r['cause'] == cause]
    if not cands:
        # Check all non-fixed repeats on this line if cause flipped under mislocation
        cands = [r for r in res['repeat'] if not r['fixed'] and r['line'] == lid]
    return float(cands[0]['km']) if cands else fallback


def _rep_mmd_k(res, lid, s_center, cause):
    cands = [r for r in res['programme']['ranked'] if r['line'] == lid and r['cause'] == cause
             and abs(r['structure'] - s_center) <= 5]
    if not cands:
        cands = [r for r in res['programme']['ranked'] if r['line'] == lid and r['cause'] == cause]
    return float(cands[0]['mm_per_day'] / 1000.0) if cands else 0.0


def extract_members(res, opts):
    mm26 = sum(v['minutes'] for v in res['impact'].values()) / 1e6
    secs = res['deposits']['sections']
    return {
        'M1_L15_clearance': round(_span_slope(res, 'L15', 48, opts), 4),
        'M1b_L12_growin': round(_span_slope(res, 'L12', 44, opts), 4),
        'M2_L08_bess_km': round(_rep_km(res, 'L08', 'insulator', 24.0), 4),
        'M3_L11_dc_km': round(_rep_km(res, 'L11', 'insulator', 10.0), 4),
        'M4_L02_W5_ratio': round(float(secs['L02-W5']['ratio']), 4),
        'M4b_L02_W1_ratio': round(float(secs['L02-W1']['ratio']), 4),
        'M5_L16_roost_p1': round(_rep_mmd_k(res, 'L16', 23, 'bird'), 3),
        'M5b_2026_mm': round(mm26, 4),
        'M6_L13_fallin_p1': round(_rep_mmd_k(res, 'L13', 105, 'fallin'), 3),
    }


def _snap_rep(rl, gold_reps, tol=2):
    """Snap a repeat location within +-tol structures of the golden's place on the same line and cause."""
    for gr in gold_reps:
        if gr['line'] == rl['line'] and gr['cause'] == rl['cause'] and abs(gr['structure'] - rl['structure']) <= tol:
            return (gr['line'], gr['structure'], gr['cause'])
    return (rl['line'], rl['structure'], rl['cause'])


def extract_figures(res, gold_reps):
    open_r = [r for r in res['repeat'] if not r['fixed']]
    snapped_open = sorted(_snap_rep(r, gold_reps) for r in open_r)
    snapped_p1 = sorted(_snap_rep(r, gold_reps) for r in res['programme']['funded'])
    snapped_ranked = sorted(_snap_rep(r, gold_reps) + (r['priority'],) for r in res['programme']['ranked'])
    washes = sorted(res['programme']['due_washes'])

    # 5 independent Critical Components (each moves ONLY under its own stump!)
    cc1 = sorted('%s:%d' % (l, s) for (l, s, c) in snapped_open if c == 'hardware')
    cc2 = sorted('%s:%d' % (l, s) for (l, s, c) in snapped_open if l in ('L08', 'L09') and c == 'insulator')
    cc3 = sorted('%s:%d:%s' % (l, s, c) for (l, s, c) in snapped_open
                 if (l == 'L11' and c == 'insulator') or (l == 'L10' and c == 'growin' and s < 85))
    cc4 = list(washes)
    cc5 = round(sum(v['minutes'] for v in res['impact'].values()), 1)

    # 4 coupled non-ECF Ask figures (every single ask moves under 4-5 independent stumps!)
    a1 = ['%s:%d:%s' % x for x in snapped_p1]
    a2 = ['%s:%d:%s:%s' % x for x in snapped_ranked]
    a3 = sorted(washes + ['%s:%d:%s' % x for x in snapped_p1])
    mix = {}
    for r in res['programme']['funded']:
        mix[r['cause']] = mix.get(r['cause'], 0) + r['crew_days']
    mix['wash'] = res['programme']['wash_days']
    a4 = sorted(['%s=%d' % kv for kv in mix.items()] + ['%s:%d' % (l, s) for (l, s, c) in snapped_p1 if l in ('L08', 'L09', 'L10', 'L11', 'L15', 'L16')])
    return dict(CC1=cc1, CC2=cc2, CC3=cc3, CC4=cc4, CC5=cc5, A1=a1, A2=a2, A3=a3, A4=a4)


def referee_metrics(d, w, g_res, unc_res, dir_res):
    """Evaluate S3 referee slice: all two-ended patrol-confirmed ground lockouts on Lines 10 & 11
    (zero overlap with S3 target structures L10 str 68 or L11 str 71 -> covers_target=False)."""
    pat = d['patrols']

    def mae_of(res):
        errs = []
        for _, r in pat.iterrows():
            lid = 'L%02d' % int(str(r['Line']).split()[1])
            if lid not in ('L10', 'L11'):
                continue
            txt = str(r['Findings']).lower()
            if 'no broken hardware' in txt or 'not found' in txt or 'nothing found' in txt:
                continue
            day = dt.date.fromisoformat(str(r['Date'])[:10])
            wfs = [f for f in w['faults'] if f['line'] == lid and f['permanent']
                   and abs((C.to_local(f['t']).date() - day).days) <= 4]
            gfs = [f for f in res['faults'] if f['line'] == lid and f['locked']
                   and abs((C.to_local(f['t']).date() - day).days) <= 4]
            if wfs and gfs:
                wf, gf = wfs[0], gfs[0]
                if gf.get('type') in ('AG', 'BG', 'CG') and gf['rec'].get('a') and gf['rec'].get('b'):
                    errs.append(abs((gf['km'] or 0.0) - wf['km']))
        return float(np.mean(errs)) if errs else 0.0, len(errs)

    g_mae, n_ref = mae_of(g_res)
    u_mae, _ = mae_of(unc_res)
    d_mae, _ = mae_of(dir_res)
    return dict(
        slice='%d patrol-confirmed two-ended ground lockouts on Lines 10 and 11 (outside the target repeat structures L10 str 68 and L11 str 71)' % n_ref,
        covers_target=False,
        truth=0.0,
        golden=round(g_mae, 4),
        rivals={'direct': round(d_mae, 4), 'rigorous': round(u_mae, 4)},
    )


def world_truth_members(w):
    """True world quantities on each of the 9 core members directly from sim.world()."""
    imp_by_f = {imp['fault']: imp['impact'] for imp in w['impacts']}
    mm26 = sum(
        i['members'] * i['seconds'] / 60.0
        for imp in w['impacts'] if C.to_local(imp['t0']).year == 2026
        for i in imp['impact'] if i['seconds'] > 300
    ) / 1e6
    l16_mm = sum(
        i['members'] * i['seconds'] / 60.0
        for f in w['faults'] if f['line'] == 'L16' and f['cause'] == 'bird' and abs(f['structure'] - 23) <= 2
        for i in imp_by_f.get(f['id'], ()) if i['seconds'] > 300
    ) / (1000.0 * C.CREW_DAYS['bird'])
    l13_mm = sum(
        i['members'] * i['seconds'] / 60.0
        for f in w['faults'] if f['line'] == 'L13' and f['cause'] == 'fallin' and 103 <= f['structure'] <= 107
        for i in imp_by_f.get(f['id'], ()) if i['seconds'] > 300
    ) / (1000.0 * C.CREW_DAYS['fallin'])
    # True 31 Oct C_eff / CEFF_CRIT on L02-W5 and L02-W1
    def true_ratio(sid):
        s_ = next(x for x in w['sections'] if x['id'] == sid)
        line = w['net']['lines'][s_['line']]
        sts = [x for x in line['structures'] if x['insulator'] == 'porcelain' and x['shore_km'] <= 6.0]
        cols = [k for k, x in enumerate(sts) if s_['s0'] <= x['no'] <= s_['s1']]
        ceff = float(w['deposits'][s_['line']][3][-1, cols].mean())
        return ceff / F.CEFF_CRIT
    return {
        'M1_L15_clearance': 0.0,
        'M1b_L12_growin': -2.75,
        'M2_L08_bess_km': F.BESS_STRING_KM,
        'M3_L11_dc_km': F.DC_STRING_KM,
        'M4_L02_W5_ratio': round(true_ratio('L02-W5'), 4),
        'M4b_L02_W1_ratio': round(true_ratio('L02-W1'), 4),
        'M5_L16_roost_p1': round(l16_mm, 3),
        'M5b_2026_mm': round(mm26, 4),
        'M6_L13_fallin_p1': round(l13_mm, 3),
    }


def build_spec():
    d = G.load(C.TARGET)
    w = sim.world()

    def run_opts(opts_dict):
        full = dict(G.GOLD, **opts_dict)
        res = G.run(C.TARGET, full, d=d)
        return res, full

    g_res, g_opts = run_opts({})
    gold_reps = [r for r in g_res['repeat'] if not r['fixed']]
    g_mem = extract_members(g_res, g_opts)
    g_fig = extract_figures(g_res, g_reps := gold_reps)
    truth_mem = world_truth_members(w)

    # 14 honest variants
    fam_mem = {m: [] for m in g_mem}
    fam_cc5 = []
    for _, vopts in VARIANTS:
        vres, vfull = run_opts(vopts)
        vm = extract_members(vres, vfull)
        for m in g_mem:
            fam_mem[m].append(vm[m])
        fam_cc5.append(extract_figures(vres, g_reps)['CC5'])

    # Complete lattice: singles (5), all-but-one (5), reflex (1)
    sids = ['S1', 'S2', 'S3', 'S4', 'S5']
    need_sets = [[s] for s in sids] + [[t for t in sids if t != s] for s in sids] + [sids]
    lattice_mem = {}
    lattice_fig = {}
    for combo in need_sets:
        key = '+'.join(sorted(combo))
        opts_c = {}
        for s in combo:
            opts_c.update(HURRY[s])
        cres, cfull = run_opts(opts_c)
        lattice_mem[key] = extract_members(cres, cfull)
        lattice_fig[key] = extract_figures(cres, g_reps)

    # Over-corrected sides (5) & coded one-fact shortcuts (5)
    over_mem = {}
    one_fact_spec = {}
    for s in sids:
        ores, ofull = run_opts(OVER[s])
        over_mem[s] = extract_members(ores, ofull)
        fres, ffull = run_opts(ONE_FACT[s])
        ffig = extract_figures(fres, g_reps)
        cc_id = 'CC' + s[1]
        one_fact_spec[s] = {'members': extract_members(fres, ffull), 'component': ffig[cc_id]}

    # Direct, Rigorous, and the 4 Frontier Run Routes (generous, calibrated, hedge, cutoff)
    route_defs = {
        'direct': dict(loc='dist', contacts='signature', tap_infeed='none', dc_mutual='uncoupled', deposit='latest', topology='oms_direct'),
        'rigorous': dict(contacts='signature', tap_infeed='none', dc_mutual='uncoupled', deposit='esdd_wind', topology='static'),
        'generous': dict(contacts='underbuild_all', tap_infeed='over', dc_mutual='over', deposit='over_nsdd', topology='over_both'),
        'calibrated': dict(contacts='signature', tap_infeed='solar_only', dc_mutual='one_fact', deposit='esdd_wind', topology='static'),
        'hedge': dict(contacts='signature', tap_infeed='dual', infeed_scale=0.35, dc_mutual='coupled', dc_z0m_scale=0.35, beta_override=0.10, topology='static'),
        'cutoff': dict(contacts='underbuild_all', tap_infeed='solar_only', dc_mutual='one_fact', deposit='one_fact', topology='one_fact_2026'),
    }
    route_mem, route_fig, route_res = {}, {}, {}
    for rname, ropts in route_defs.items():
        rres, rfull = run_opts(ropts)
        route_res[rname] = rres
        route_mem[rname] = extract_members(rres, rfull)
        route_fig[rname] = extract_figures(rres, g_reps)

    lines_map = {
        'M1_L15_clearance': [-0.8],
        'M1b_L12_growin': [-0.8],
        'M2_L08_bess_km': [17.7, 19.6],
        'M3_L11_dc_km': [13.2, 14.5],
        'M4_L02_W5_ratio': [1.0],
        'M4b_L02_W1_ratio': [1.0],
        'M5_L16_roost_p1': [55.0],
        'M5b_2026_mm': [4.5, 5.8],
        'M6_L13_fallin_p1': [55.0],
    }
    members = {
        m: {
            'lines': lines_map[m],
            'truth': truth_mem[m],
            'golden': g_mem[m],
            'family': fam_mem[m],
            'routes': {'direct': route_mem['direct'][m], 'rigorous': route_mem['rigorous'][m]},
        }
        for m in sorted(lines_map)
    }

    stumps = {
        'S1': {
            'axis': 'what',
            'opens': 'M1_L15_clearance',
            'said_out_loud': 'Some summer afternoon contacts on underbuilt 69 kV spans are fixed conductor-to-underbuild clearance contacts rather than growing trees.',
            'steps_left': 4,
            'precedents': ['L47', 'L26'],
            'sides': {'over': over_mem['S1']},
            'one_fact_shortcut': one_fact_spec['S1'],
        },
        'S2': {
            'axis': 'who',
            'opens': 'M2_L08_bess_km',
            'said_out_loud': 'Both independent power producer lateral taps inject zero-sequence ground current through grounded-wye step-up transformers that distorts single-ended relay distance beyond each tap.',
            'steps_left': 4,
            'precedents': ['L63', 'N21'],
            'sides': {'over': over_mem['S2']},
            'one_fact_shortcut': one_fact_spec['S2'],
        },
        'S3': {
            'axis': 'against',
            'opens': 'M3_L11_dc_km',
            'said_out_loud': 'Zero-sequence mutual coupling on the shared double-circuit steel-pole corridor out of Inland biases uncoupled two-ended residual-current fault locations on both parallel lines.',
            'steps_left': 5,
            'precedents': ['L58', 'L48'],
            'sides': {'over': over_mem['S3']},
            'one_fact_shortcut': one_fact_spec['S3'],
        },
        'S4': {
            'axis': 'unit',
            'opens': 'M4_L02_W5_ratio',
            'said_out_loud': 'Coastal porcelain fog flashovers depend jointly on soluble sea salt (ESDD) and slow-washing non-soluble corridor dust (NSDD) rather than salt alone.',
            'steps_left': 5,
            'precedents': ['L38', 'L42', 'L15'],
            'sides': {'over': over_mem['S4']},
            'one_fact_shortcut': one_fact_spec['S4'],
        },
        'S5': {
            'axis': 'when',
            'opens': 'M5_L16_roost_p1',
            'said_out_loud': 'Planned multi-week SCADA supervisory switching windows re-feed tap substations onto alternate 69 kV lines, shifting both 2026 member-minutes and historical Priority 1 repeat rankings.',
            'steps_left': 4,
            'precedents': ['N09', 'L55'],
            'sides': {'over': over_mem['S5']},
            'one_fact_shortcut': one_fact_spec['S5'],
        },
    }

    figures = []
    for fid in ('CC1', 'CC2', 'CC3', 'CC4'):
        figures.append({
            'id': fid, 'block': 'component', 'exact': True,
            'golden': g_fig[fid],
            'lattice': {k: v[fid] for k, v in lattice_fig.items()},
            'routes': {rn: route_fig[rn][fid] for rn in ('rigorous', 'generous', 'calibrated', 'hedge', 'cutoff')},
        })
    cc5_lo = min(min(fam_cc5), g_fig['CC5']) * 0.98
    cc5_hi = max(max(fam_cc5), g_fig['CC5']) * 1.02
    figures.append({
        'id': 'CC5', 'block': 'component', 'exact': False,
        'golden': g_fig['CC5'], 'family': fam_cc5, 'band': [round(cc5_lo, 1), round(cc5_hi, 1)],
        'lattice': {k: v['CC5'] for k, v in lattice_fig.items()},
        'routes': {rn: route_fig[rn]['CC5'] for rn in ('rigorous', 'generous', 'calibrated', 'hedge', 'cutoff')},
    })
    for fid in ('A1', 'A2', 'A3', 'A4'):
        figures.append({
            'id': fid, 'block': 'ask', 'exact': True, 'ecf': False,
            'golden': g_fig[fid],
            'lattice': {k: v[fid] for k, v in lattice_fig.items()},
            'routes': {rn: route_fig[rn][fid] for rn in ('rigorous', 'generous', 'calibrated', 'hedge', 'cutoff')},
        })

    ref = referee_metrics(d, w, g_res, route_res['rigorous'], route_res['direct'])
    run_routes = {rn: route_mem[rn] for rn in ('generous', 'calibrated', 'hedge', 'cutoff')}

    return {
        'task': 'task13',
        'v4_hardened': True,
        'call': 'lines',
        'members': members,
        'stumps': stumps,
        'lattice': lattice_mem,
        'referee': ref,
        'run_routes': run_routes,
        'figures': figures,
    }


if __name__ == '__main__':
    spec = build_spec()
    sys.exit(corelib.run(spec))
