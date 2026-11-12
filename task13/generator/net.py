"""The network: nine substations, 74 feeders, 22 of them paired into automated loops (44 loop feeders), each loop
feeder cut into three main-line sections by two midline reclosers and closed to its partner through one normally
open tie switch; customers, main-line length, customer mix and growth per section; the reclosers' controls, their
radio sites and link quality, their batteries; the loops' commissioning and the March 2025 ADMS upgrade's tags."""
import datetime as dt

import numpy as np

import common as C


def _feeder_ids(rng):
    ids = []
    for code, _ in C.SUBSTATIONS:
        n = rng.integers(7, 10)
        nums = sorted(rng.choice(np.arange(201, 299), size=n, replace=False))
        prefix = {'RPD': 4, 'EGL': 2, 'KST': 2, 'MNP': 3, 'LMV': 5, 'SKY': 6, 'MDL': 3, 'JUD': 7, 'GTH': 5}[code]
        for k in nums:
            ids.append((code, '%s%d%02d' % (code, prefix, k % 100)))
    return ids


def build():
    rng = np.random.default_rng(C.SEED)
    all_ids = _feeder_ids(rng)
    rng.shuffle(all_ids)
    feeders = {}
    for sub, fid in all_ids[:74]:
        feeders[fid] = {'id': fid, 'sub': sub}
    fids = sorted(feeders)
    # 22 loops: 14 tie two substations, 8 tie two feeders of one substation
    by_sub = {}
    for f in fids:
        by_sub.setdefault(feeders[f]['sub'], []).append(f)
    subs = [s for s, _ in C.SUBSTATIONS]
    adj = {'RPD': ['EGL', 'JUD', 'GTH'], 'EGL': ['RPD', 'KST', 'MDL'], 'KST': ['EGL', 'MNP', 'LMV'],
           'MNP': ['KST', 'SKY', 'JUD'], 'LMV': ['KST', 'SKY', 'MDL'], 'SKY': ['MNP', 'LMV', 'GTH'],
           'MDL': ['EGL', 'LMV'], 'JUD': ['RPD', 'MNP', 'GTH'], 'GTH': ['RPD', 'SKY', 'JUD']}
    pool = {s: list(by_sub[s]) for s in subs}
    for s in subs:
        rng.shuffle(pool[s])
    loops = []
    tries = 0
    while len(loops) < 22 and tries < 5000:
        tries += 1
        a_sub = subs[rng.integers(len(subs))]
        same = rng.random() < 0.36
        b_sub = a_sub if same else adj[a_sub][rng.integers(len(adj[a_sub]))]
        if not pool[a_sub] or not pool[b_sub] or (same and len(pool[a_sub]) < 2):
            continue
        fa = pool[a_sub].pop()
        fb = pool[b_sub].pop()
        loops.append((fa, fb))
    assert len(loops) == 22
    loops.sort()
    # commissioning: 18 before the record, 4 during 2022
    comm = []
    base = [dt.date(2019, 4, 15) + dt.timedelta(days=int(d)) for d in sorted(rng.integers(0, 960, size=18))]
    late = [dt.date(2022, 3, 21), dt.date(2022, 5, 9), dt.date(2022, 7, 26), dt.date(2022, 10, 18)]
    order = rng.permutation(22)
    dates = base + late
    for k, i in enumerate(order):
        comm.append((i, dates[k]))
    comm = dict(comm)
    LOOPS = []
    for i, (fa, fb) in enumerate(loops):
        LOOPS.append({'loop': 'L%02d' % (i + 1), 'a': fa, 'b': fb, 'commissioned': comm[i],
                      'scheme': 'FLISR_%s_%s' % (fa, fb)})
    loop_feeders = set()
    for L in LOOPS:
        for f in (L['a'], L['b']):
            loop_feeders.add(f)
            feeders[f]['loop'] = L['loop']
            feeders[f]['partner'] = L['b'] if f == L['a'] else L['a']
    # sections, customers, lengths, mix, growth
    for f in fids:
        F = feeders[f]
        cust = int(rng.integers(900, 2750))
        res = float(rng.uniform(0.78, 0.95))
        F['customers0'] = cust
        F['res_share'] = res
        if f in loop_feeders:
            s1 = rng.uniform(0.28, 0.42)
            s2 = rng.uniform(0.25, 0.38)
            s3 = 1.0 - s1 - s2
            if s3 < 0.2:
                s2 -= 0.2 - s3
                s3 = 0.2
            shares = [s1, s2, s3]
            km = [rng.uniform(2.2, 6.0), rng.uniform(3.0, 8.0), rng.uniform(3.0, 9.0)]
        else:
            shares = [1.0]
            km = [rng.uniform(8, 24)]
        n = [int(round(cust * s)) for s in shares]
        n[-1] = cust - sum(n[:-1])
        F['sections'] = []
        for k, (c, L_) in enumerate(zip(n, km)):
            grow = 0.006 + rng.normal(0, 0.003)
            sub_start = None
            if f in loop_feeders and k == 2 and rng.random() < 0.3:
                grow += rng.uniform(0.025, 0.05)
                sub_start = 2023
            F['sections'].append({'s': k + 1, 'cust0': int(c), 'km': round(float(L_), 2), 'grow': float(grow),
                                  'boom_from': sub_start, 'pv': float(rng.uniform(0.01, 0.09)),
                                  'lat_rate': float(rng.uniform(0.7, 1.4))})
        F['ml_km'] = round(sum(s['km'] for s in F['sections']), 2)
        F['exposure'] = float(rng.lognormal(0, 0.18))      # trees, terrain, construction: a feeder's own fault level
        F['emerg_amps'] = int(rng.choice([360, 390, 420, 450, 480, 500, 520, 540]))
        F['cb_pickup'] = int(rng.choice([600, 640, 680, 720]))
    # the 2024 reconfiguration: three loop feeders' R2 moved, customers moved between S2 and S3
    recon = []
    cand = [f for f in sorted(loop_feeders)]
    for f in rng.choice(cand, size=3, replace=False):
        F = feeders[str(f)]
        moved = int(round(F['sections'][2]['cust0'] * rng.uniform(0.18, 0.3)))
        recon.append({'feeder': str(f), 'date': dt.date(2024, 10, 15), 'moved': moved,
                      'km_moved': round(F['sections'][2]['km'] * 0.25, 2)})
    # devices: CB per feeder; R1, R2 per loop feeder; one tie per loop
    devices = {}
    asset_no = 20100
    ctl_old_loops = set()
    for L in LOOPS:
        if L['commissioned'] < dt.date(2020, 9, 1) and rng.random() < 0.62:
            ctl_old_loops.add(L['loop'])
    sites_by_sub = {'RPD': 'Judson Elevator', 'EGL': 'Eagle Lake Water Tower', 'KST': 'Kasota Bluff',
                    'MNP': 'Skyline Tower', 'LMV': 'Kasota Bluff', 'SKY': 'Skyline Tower', 'MDL': 'Madison Lake',
                    'JUD': 'Judson Elevator', 'GTH': 'Skyline Tower'}
    for L in LOOPS:
        for f in (L['a'], L['b']):
            F = feeders[f]
            for k in (1, 2):
                asset_no += int(rng.integers(3, 29))
                old = L['loop'] in ctl_old_loops and (rng.random() < 0.85)
                d = {'asset': 'RCL-%d' % asset_no, 'feeder': f, 'loop': L['loop'], 'kind': 'R%d' % k,
                     'ctl': 'CTL-4C' if old else 'CTL-6', 'site': sites_by_sub[F['sub']],
                     'tag_old': '%s_R%d' % (f, k), 'tag_new': '%s-RCL%d' % (f, k),
                     'q': float(min(0.6, rng.lognormal(np.log(0.012), 0.55))),
                     'installed': L['commissioned'] - dt.timedelta(days=int(rng.integers(20, 120)))}
                devices[d['asset']] = d
        asset_no += int(rng.integers(3, 29))
        t = {'asset': 'TSW-%d' % asset_no, 'feeder': L['a'] + '/' + L['b'], 'loop': L['loop'], 'kind': 'TS',
             'ctl': 'CTL-6', 'site': sites_by_sub[feeders[L['a']]['sub']],
             'tag_old': '%s_%s_TIE' % (L['a'], L['b']), 'tag_new': '%s-TIE-%s' % (L['a'], L['b'][-3:]),
             'q': float(min(0.6, rng.lognormal(np.log(0.010), 0.5))),
             'installed': L['commissioned'] - dt.timedelta(days=int(rng.integers(10, 60)))}
        devices[t['asset']] = t
    # chronic poor radio paths at five devices
    rcl = sorted(a for a in devices if a.startswith('RCL'))
    for a in rng.choice(rcl, size=5, replace=False):
        devices[str(a)]['q'] = float(rng.uniform(0.16, 0.3))
    # batteries: the battery in each recloser control at the start, its make-up and how fast it ages
    for a in rcl:
        D = devices[a]
        age0 = float(rng.uniform(0.2, 4.6))
        D['batt0'] = (C.T0 - dt.timedelta(days=int(age0 * 365.25))).date()
        if D['batt0'] < D['installed']:
            D['batt0'] = D['installed']
    return {'feeders': feeders, 'fids': fids, 'loops': LOOPS, 'loop_feeders': sorted(loop_feeders),
            'devices': devices, 'recon': recon, 'ctl_old_loops': sorted(ctl_old_loops), 'rng_state': None}


def section_customers(F, k, year_frac, recon_by_feeder):
    """customers on section k (1..3) at a decimal year, with growth and the 2024 move of R2"""
    S = F['sections'][k - 1]
    g = S['grow']
    t = year_frac - 2022.0
    c = S['cust0'] * (1 + g) ** max(0.0, t) if S['boom_from'] is None else \
        S['cust0'] * (1 + 0.006) ** max(0.0, t) * (1 + g) ** max(0.0, year_frac - S['boom_from'])
    r = recon_by_feeder.get(F['id'])
    if r is not None:
        frac = (r['date'].year + (r['date'].timetuple().tm_yday - 1) / 365.25)
        if year_frac >= frac:
            if k == 2:
                c += r['moved']
            elif k == 3:
                c -= r['moved']
    return c
