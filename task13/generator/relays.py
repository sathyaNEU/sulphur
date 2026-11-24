"""What each relay recorded (architecture 7, Level 5). Every fault is solved on its sequence networks node by node:
- On normal lines: two-terminal line-out sources on the fault date.
- On Line 9 (Coyote Draw Solar) and Line 8 (Brushy Creek BESS): exact 3-terminal nodal solution with the YNd1 step-up
  zero-sequence tap source (day and night) and limited inverter positive-sequence source while generating/discharging;
  each IPP's own 69 kV protection relay records its currents on CST all year.
- On double-circuit Lines 10 and 11 (shared 14.5 km steel-pole corridor out of Inland): exact coupled 2-line
  zero-sequence matrix [[Z0_10, Z0m], [Z0m, Z0_11]] solution, recording exact induced I0 on the healthy parallel line's
  relays as non-tripping pickup records."""
import cmath
import datetime as dt
import math

import numpy as np

import common as C
import network as N

V_PH = 69.0e3 / math.sqrt(3.0)
A = cmath.exp(2j * math.pi / 3)
CLOCK_FAULTS = {
    ('MSQ', None): (dt.datetime(2024, 6, 3, tzinfo=C.UTC), dt.datetime(2024, 9, 18, tzinfo=C.UTC), 0.92),
    ('CAN', None): (dt.datetime(2025, 1, 8, tzinfo=C.UTC), dt.datetime(2025, 4, 21, tzinfo=C.UTC), -1.45),
}


def _solve(nodes, branches, sources, inj, coupled=()):
    """nodal solution with optional coupled 2x2 branch pairs: coupled holds ((a1, b1, a2, b2), Z_2x2)."""
    idx = {n: i for i, n in enumerate(nodes)}
    Y = np.zeros((len(nodes), len(nodes)), complex)
    I = np.zeros(len(nodes), complex)
    for n1, n2, z in branches:
        y = 1.0 / z
        i = idx[n1]
        Y[i, i] += y
        if n2 is not None:
            j = idx[n2]
            Y[j, j] += y
            Y[i, j] -= y
            Y[j, i] -= y
    for (a1, b1, a2, b2), Zmat in coupled:
        Ym = np.linalg.inv(Zmat)
        pairs = [(a1, b1), (a2, b2)]
        for r in range(2):
            for c in range(2):
                y = Ym[r, c]
                for nr, sr in ((pairs[r][0], 1), (pairs[r][1], -1)):
                    for nc, sc in ((pairs[c][0], 1), (pairs[c][1], -1)):
                        Y[idx[nr], idx[nc]] += sr * sc * y
    for n, zs, e in sources:
        i = idx[n]
        Y[i, i] += 1.0 / zs
        I[i] += e / zs
    for n, cur in inj.items():
        I[idx[n]] += cur
    return dict(zip(nodes, np.linalg.solve(Y, I)))


def _solve_dc_zero(net, lid, d, t, i0_inj):
    """Exact coupled 2-line zero-sequence network for double-circuit Lines 10 and 11 leaving Inland (0..DC_KM)."""
    l10, l11 = net['lines']['L10'], net['lines']['L11']
    z0_10, z0_11, z0m = l10['z0'], l11['z0'], N.DC_Z0M
    L10, L11, Lm = l10['length'], l11['length'], N.DC_KM
    z0_inl = N.inl_bus_z0(t)
    _, z0_msq = N.source('L10', 'MSQ', t)
    _, z0_grg = N.source('L11', 'GRG', t)
    d = min(max(d, 0.02), (L10 if lid == 'L10' else L11) - 0.02)

    if d < Lm - 0.01:
        nodes = ['INL', 'F', 'P_d', 'M10', 'M11', 'MSQ', 'GRG']
        coupled = []
        if lid == 'L11':
            coupled.append((('INL', 'P_d', 'INL', 'F'), np.array([[z0_10, z0m], [z0m, z0_11]], complex) * d))
            coupled.append((('P_d', 'M10', 'F', 'M11'), np.array([[z0_10, z0m], [z0m, z0_11]], complex) * (Lm - d)))
        else:
            coupled.append((('INL', 'F', 'INL', 'P_d'), np.array([[z0_10, z0m], [z0m, z0_11]], complex) * d))
            coupled.append((('F', 'M10', 'P_d', 'M11'), np.array([[z0_10, z0m], [z0m, z0_11]], complex) * (Lm - d)))
        branches = [('M10', 'MSQ', z0_10 * (L10 - Lm)), ('M11', 'GRG', z0_11 * (L11 - Lm)),
                    ('INL', None, z0_inl), ('MSQ', None, z0_msq), ('GRG', None, z0_grg)]
    else:
        nodes = ['INL', 'M10', 'M11', 'F', 'MSQ', 'GRG']
        coupled = [(('INL', 'M10', 'INL', 'M11'), np.array([[z0_10, z0m], [z0m, z0_11]], complex) * Lm)]
        if lid == 'L11':
            branches = [('M10', 'MSQ', z0_10 * (L10 - Lm)), ('M11', 'F', z0_11 * (d - Lm)),
                        ('F', 'GRG', z0_11 * (L11 - d)), ('INL', None, z0_inl), ('MSQ', None, z0_msq), ('GRG', None, z0_grg)]
        else:
            branches = [('M11', 'GRG', z0_11 * (L11 - Lm)), ('M10', 'F', z0_10 * (d - Lm)),
                        ('F', 'MSQ', z0_10 * (L10 - d)), ('INL', None, z0_inl), ('MSQ', None, z0_msq), ('GRG', None, z0_grg)]

    v = _solve(nodes, branches, [], {'F': i0_inj}, coupled=coupled)
    # Branch currents leaving terminals toward the lines
    if d < Lm - 0.01:
        Z1 = np.array([[z0_10, z0m], [z0m, z0_11]], complex) * d
        dv = np.array([v['INL'] - v['P_d'], v['INL'] - v['F']]) if lid == 'L11' else np.array([v['INL'] - v['F'], v['INL'] - v['P_d']])
        i10_inl, i11_inl = np.linalg.solve(Z1, dv)
        i10_msq = (v['MSQ'] - v['M10']) / (z0_10 * (L10 - Lm))
        i11_grg = (v['GRG'] - v['M11']) / (z0_11 * (L11 - Lm))
    else:
        Z1 = np.array([[z0_10, z0m], [z0m, z0_11]], complex) * Lm
        i10_inl, i11_inl = np.linalg.solve(Z1, np.array([v['INL'] - v['M10'], v['INL'] - v['M11']]))
        if lid == 'L11':
            i10_msq = (v['MSQ'] - v['M10']) / (z0_10 * (L10 - Lm))
            i11_grg = (v['GRG'] - v['F']) / (z0_11 * (L11 - d))
        else:
            i10_msq = (v['MSQ'] - v['F']) / (z0_10 * (L10 - d))
            i11_grg = (v['GRG'] - v['M11']) / (z0_11 * (L11 - Lm))

    if lid == 'L11':
        return dict(vf=v['F'], vA=v['INL'], vB=v['GRG'], iA=i11_inl, iB=i11_grg,
                    par_line='L10', par_iA=i10_inl, par_iB=i10_msq)
    return dict(vf=v['F'], vA=v['INL'], vB=v['MSQ'], iA=i10_inl, iB=i10_msq,
                par_line='L11', par_iA=i11_inl, par_iB=i11_grg)


def fault_currents(net, f, ld, delta_deg=None):
    """complex sequence and phase quantities at each terminal (plus any IPP tap or coupled parallel line)"""
    lid = f['line']
    line = net['lines'][lid]
    t = f['t']
    L = line['length']
    d = min(max(f['km'], 0.02), L - 0.02)
    z1, z0 = line['z1'], line['z0']
    z1a, z0a = N.source(lid, line['a'], t, net=net)
    z1b, z0b = N.source(lid, line['b'], t, net=net)
    if delta_deg is None:
        delta_deg = float(ld['delta'][lid][min(f['h'], C.NH - 1)])
    ea = V_PH * cmath.exp(1j * math.radians(delta_deg / 2))
    eb = V_PH * cmath.exp(-1j * math.radians(delta_deg / 2))

    ipp_info = N.IPP_TAPS.get(lid)
    tap_on = (ipp_info is not None) and (t >= ipp_info['energized'])
    if tap_on:
        gen_mw = abs(float(ld['solar' if ipp_info['kind'] == 'solar' else 'bess'][min(f['h'], C.NH - 1)]))
        zg = N.gsu_z(0, line=lid) + z0 * ipp_info['tap_len']
        z1t = (V_PH / (ipp_info['inv_i_pu'] * max(gen_mw, 0.5) * 1e6 / (math.sqrt(3) * 69e3))) * cmath.exp(1j * math.radians(30)) if gen_mw > 1.0 else None
        km_t = ipp_info['tap_km']
    else:
        zg, z1t, km_t = None, None, None

    is_dc = lid in N.DC_LINES

    def network(seq, with_sources):
        zs_a, zs_b = (z1a, z1b) if seq != 0 else (z0a, z0b)
        zl = z1 if seq != 0 else z0
        nodes = ['A', 'F', 'B']
        branches = []
        if tap_on:
            nodes = ['A', 'T', 'F', 'B'] if d > km_t else ['A', 'F', 'T', 'B']
            if d > km_t:
                branches += [('A', 'T', zl * km_t), ('T', 'F', zl * (d - km_t)), ('F', 'B', zl * (L - d))]
            else:
                branches += [('A', 'F', zl * d), ('F', 'T', zl * (km_t - d)), ('T', 'B', zl * (L - km_t))]
        else:
            branches += [('A', 'F', zl * d), ('F', 'B', zl * (L - d))]
        sources = []
        if seq == 0:
            branches += [('A', None, zs_a), ('B', None, zs_b)]
            if tap_on:
                branches.append(('T', None, zg))
        else:
            if with_sources and seq == 1:
                sources += [('A', zs_a, ea), ('B', zs_b, eb)]
                if tap_on and z1t is not None:
                    sources.append(('T', z1t, V_PH))
            else:
                branches += [('A', None, zs_a), ('B', None, zs_b)]
                if tap_on and z1t is not None:
                    branches.append(('T', None, z1t))
        return nodes, branches, sources

    nodes, br, src = network(1, True)
    v_pre = _solve(nodes, br, src, {})
    zth = {}
    for seq in (1, 2):
        nodes_s, br_s, _ = network(seq, False)
        zth[seq] = _solve(nodes_s, br_s, [], {'F': 1.0})['F']
    if is_dc:
        zth[0] = _solve_dc_zero(net, lid, d, t, 1.0)['vf']
    else:
        nodes_s, br_s, _ = network(0, False)
        zth[0] = _solve(nodes_s, br_s, [], {'F': 1.0})['F']

    vf = v_pre['F']
    rf = f['rf']
    nph = len(f['phases'])
    if nph == 1:
        i0 = vf / (zth[1] + zth[2] + zth[0] + 3 * rf)
        i_seq = {1: i0, 2: i0, 0: i0}
        ref = f['phases'][0]
    elif nph == 2:
        i1 = vf / (zth[1] + zth[2] + rf)
        i_seq = {1: i1, 2: -i1, 0: 0.0}
        ref = [p for p in 'ABC' if p not in f['phases']][0]
    else:
        i1 = vf / (zth[1] + rf)
        i_seq = {1: i1, 2: 0.0, 0: 0.0}
        ref = 'A'

    v_seq = {}
    for seq in (1, 2):
        nodes_s, br_s, _ = network(seq, False)
        v_seq[seq] = _solve(nodes_s, br_s, [], {'F': -i_seq[seq]})
    dc0 = None
    if is_dc:
        dc0 = _solve_dc_zero(net, lid, d, t, -i_seq[0])
        v_seq[0] = {'A': dc0['vA'], 'B': dc0['vB']}
    else:
        nodes_s, br_s, _ = network(0, False)
        v_seq[0] = _solve(nodes_s, br_s, [], {'F': -i_seq[0]})

    def branch_toward_line(node, seq):
        if seq == 0 and is_dc:
            return dc0['iA'] if node == 'A' else dc0['iB']
        nodes_s, br_s, _ = network(seq, False)
        for n1, n2, z in br_s:
            if n1 == node and n2 is None:
                return -v_seq[seq][node] / z
        return 0.0

    out = {}
    term_nodes = ['A', 'B'] + (['T'] if tap_on else [])
    for tn in term_nodes:
        i_f = {seq: branch_toward_line(tn, seq) for seq in (1, 2, 0)}
        if tn == 'A':
            i_load = (ea - v_pre['A']) / z1a
        elif tn == 'B':
            i_load = (eb - v_pre['B']) / z1b
        else:
            i_load = (V_PH - v_pre['T']) / z1t if z1t is not None else 0.0
        i1, i2, i0_ = i_load + i_f[1], i_f[2], i_f[0]
        v1, v2, v0_ = v_pre[tn] + v_seq[1][tn], v_seq[2][tn], v_seq[0][tn]
        ia, ib, ic = i0_ + i1 + i2, i0_ + A ** 2 * i1 + A * i2, i0_ + A * i1 + A ** 2 * i2
        va, vb, vc = v0_ + v1 + v2, v0_ + A ** 2 * v1 + A * v2, v0_ + A * v1 + A ** 2 * v2
        ph_i = {'A': ia, 'B': ib, 'C': ic}
        ph_v = {'A': va, 'B': vb, 'C': vc}
        if nph in (1, 2):
            lab = {'A': ref, 'B': {'A': 'B', 'B': 'C', 'C': 'A'}[ref], 'C': {'A': 'C', 'B': 'A', 'C': 'B'}[ref]}
        else:
            lab = {'A': 'A', 'B': 'B', 'C': 'C'}
        out[tn] = dict(I={lab[k]: v for k, v in ph_i.items()}, V={lab[k]: v for k, v in ph_v.items()}, i0=i0_, i1=i1, i2=i2)

    if dc0 is not None and abs(i_seq[0]) > 1e-6:
        out['PAR'] = dict(line=dc0['par_line'], i0A=dc0['par_iA'], i0B=dc0['par_iB'])
    return out


def apparent_distance(meas, f, line, end):
    z1, z0 = line['z1'], line['z0']
    k0 = (z0 - z1) / (3 * z1)
    nph = len(f['phases'])
    if nph == 1:
        p = f['phases'][0]
        i_comp = meas['I'][p] + k0 * 3 * meas['i0']
        z_app = meas['V'][p] / i_comp
    elif nph == 2:
        p, q = f['phases']
        z_app = (meas['V'][p] - meas['V'][q]) / (meas['I'][p] - meas['I'][q])
    else:
        z_app = meas['V']['A'] / meas['I']['A']
    return z_app.imag / z1.imag


def record(w):
    net, ld = w['net'], w['ld']
    rng = np.random.default_rng(C.EV_SEED + 404)
    busy = {}
    for f in w['faults']:
        if f['cause'] == 'lightning':
            busy[f['t'].date()] = busy.get(f['t'].date(), 0) + 1
    seq_no = {}
    for f in w['faults']:
        line = net['lines'][f['line']]
        meas = fault_currents(net, f, ld)
        f['meas'] = {k: dict(I={p: abs(v) for p, v in m['I'].items()}, IG=abs(3 * m['i0']))
                     for k, m in meas.items() if k in ('A', 'B', 'T')}
        f['records'] = {}
        for end, node in (('a', 'A'), ('b', 'B')):
            st = line[end]
            fam = N.ST[st]['relay']
            m = meas[node]
            if fam == 'EM':
                f['records'][end] = dict(family='EM')
                continue
            dist = apparent_distance(m, f, line, end)
            dist_true_from_end = f['km'] if end == 'a' else line['length'] - f['km']
            dist = dist * (1.0 + rng.normal(0, 0.006)) + rng.normal(0, 0.03)
            lost = (busy.get(f['t'].date(), 0) >= 3 and rng.random() < 0.20) or rng.random() < 0.025
            off = 0.0
            for (sc, sl), (t0, t1, rate) in CLOCK_FAULTS.items():
                if sc == st and t0 <= f['t'] <= t1:
                    off = rate * (f['t'] - t0).total_seconds() / 86400.0
            op = 0.018 + 0.012 * rng.random()
            t_rel = f['t'] + dt.timedelta(seconds=op + off)
            seq_no[st] = seq_no.get(st, 1000 + int(rng.integers(0, 900))) + 1
            rec = dict(family=fam, station=st, line=f['line'], t=t_rel, offset=off, dist_km=dist,
                       dist_true=dist_true_from_end, I={p: abs(v) * (1 + rng.normal(0, 0.004)) for p, v in m['I'].items()},
                       IG=abs(3 * m['i0']) * (1 + rng.normal(0, 0.004)), lost=lost, event_no=seq_no[st])
            f['records'][end] = rec
        if 'T' in meas:
            m = meas['T']
            key = N.IPP_TAPS[f['line']]['key']
            f['records'][key] = dict(I={p: abs(v) * (1 + rng.normal(0, 0.004)) for p, v in m['I'].items()},
                                     IG=abs(3 * m['i0']) * (1 + rng.normal(0, 0.004)),
                                     t=f['t'] + dt.timedelta(seconds=0.021 + 0.01 * rng.random()))
        if 'PAR' in meas:
            pm = meas['PAR']
            f['records']['par'] = dict(line=pm['line'], IG_a=abs(3 * pm['i0A']) * (1 + rng.normal(0, 0.005)),
                                       IG_b=abs(3 * pm['i0B']) * (1 + rng.normal(0, 0.005)))
    return w
