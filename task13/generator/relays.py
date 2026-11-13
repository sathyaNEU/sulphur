"""What each relay recorded. Every fault is solved on its line's sequence networks node by node: the two terminals'
line-out sources on the fault's date, the line split at the fault, and on Shell Ridge-Ponder Creek the solar farm's
tap (its grounded-wye step-up a zero-sequence source day and night, its inverters a limited positive-sequence source
while they generate). Each terminal's relay then measures its own phase and residual currents and computes its
distance by the reactance method from its own voltage and its zero-sequence-compensated current, as if nothing fed
the fault from anywhere else; EventRecall relays report miles in UTC, GridVue relays kilometres and kA on the station's
local clock, Ponder Creek's electromechanical relays only drop targets. Relays also record the faults on neighbouring
lines their backup zones see, lose events from memory in busy storms, and two of them lost their time source for a
spell. The solar farm's own protection relay at its 69 kV breaker records the ground current it feeds."""
import cmath
import datetime as dt
import math

import numpy as np

import common as C
import network as N

V_PH = 69.0e3 / math.sqrt(3.0)
A = cmath.exp(2j * math.pi / 3)
# relays whose time source failed: (station, line or None for all) -> (start UTC, end UTC, drift seconds per day)
CLOCK_FAULTS = {
    ('MSQ', None): (dt.datetime(2024, 6, 3, tzinfo=C.UTC), dt.datetime(2024, 9, 18, tzinfo=C.UTC), 0.92),
    ('CAN', None): (dt.datetime(2025, 1, 8, tzinfo=C.UTC), dt.datetime(2025, 4, 21, tzinfo=C.UTC), -1.45),
}


def _solve(nodes, branches, sources, inj):
    """nodal solution: branches (n1, n2, Z) with n2 None for ground; sources (node, Zs, E) Norton-converted;
    inj {node: current into node}. Returns node voltages."""
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
    for n, zs, e in sources:
        i = idx[n]
        Y[i, i] += 1.0 / zs
        I[i] += e / zs
    for n, cur in inj.items():
        I[idx[n]] += cur
    return dict(zip(nodes, np.linalg.solve(Y, I)))


def fault_currents(net, f, ld, delta_deg=None):
    """complex sequence and phase quantities at each terminal (and the solar tap) for a fault"""
    lid = f['line']
    line = net['lines'][lid]
    t = f['t']
    L = line['length']
    d = min(max(f['km'], 0.02), L - 0.02)
    z1, z0 = line['z1'], line['z0']
    z1a, z0a = N.source(lid, line['a'], t)
    z1b, z0b = N.source(lid, line['b'], t)
    if delta_deg is None:
        delta_deg = float(ld['delta'][lid][min(f['h'], C.NH - 1)])
    ea = V_PH * cmath.exp(1j * math.radians(delta_deg / 2))
    eb = V_PH * cmath.exp(-1j * math.radians(delta_deg / 2))
    tap = (lid == N.TAP_LINE)
    solar_on = tap and t >= C.SOLAR_ENERGIZED
    gen_mw = float(ld['solar'][min(f['h'], C.NH - 1)]) if solar_on else 0.0
    zg = N.gsu_z() + z0 * N.TAP_LEN if solar_on else None
    # positive-sequence model of the inverters: a limited source while generating
    z1t = (V_PH / (N.INV_I_PU * max(gen_mw, 0.5) * 1e6 / (math.sqrt(3) * 69e3))) * cmath.exp(1j * math.radians(30)) if gen_mw > 1.0 else None

    def network(seq, with_sources):
        zs_a, zs_b = (z1a, z1b) if seq != 0 else (z0a, z0b)
        zl = z1 if seq != 0 else z0
        nodes = ['A', 'F', 'B']
        branches = []
        if tap and solar_on:
            km_t = N.TAP_KM
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
            if tap and solar_on:
                branches.append(('T', None, zg))
        else:
            if with_sources and seq == 1:
                sources += [('A', zs_a, ea), ('B', zs_b, eb)]
                if tap and solar_on and z1t is not None:
                    sources.append(('T', z1t, V_PH))
            else:
                branches += [('A', None, zs_a), ('B', None, zs_b)]
                if tap and solar_on and z1t is not None:
                    branches.append(('T', None, z1t))
        return nodes, branches, sources

    # prefault (positive sequence with sources)
    nodes, br, src = network(1, True)
    v_pre = _solve(nodes, br, src, {})
    # Thevenin impedance at F for each sequence: inject 1 A
    zth = {}
    for seq in (1, 2, 0):
        nodes_s, br_s, _ = network(seq, False)
        v = _solve(nodes_s, br_s, [], {'F': 1.0})
        zth[seq] = v['F']
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
    rot = {'A': 1.0, 'B': A ** 2, 'C': A}[ref] if nph == 1 else {'A': 1.0, 'B': A ** 2, 'C': A}[ref]
    # node voltages and branch currents from each sequence's fault injection (current drawn out of F)
    out = {}
    term_nodes = ['A', 'B'] + (['T'] if (tap and solar_on) else [])
    v_seq = {}
    for seq in (1, 2, 0):
        nodes_s, br_s, _ = network(seq, False)
        v_seq[seq] = _solve(nodes_s, br_s, [], {'F': -i_seq[seq]})
    zl_map = {1: z1, 2: z1, 0: z0}

    def branch_toward_line(node, seq):
        """current from the terminal's source into the line, fault component"""
        nodes_s, br_s, _ = network(seq, False)
        zs = {('A', None): None}
        for n1, n2, z in br_s:
            if n1 == node and n2 is None:
                return -v_seq[seq][node] / z
        return 0.0

    for tn in term_nodes:
        i_f = {seq: branch_toward_line(tn, seq) for seq in (1, 2, 0)}
        # prefault load current out of the terminal into the line
        if tn == 'A':
            i_load = (ea - v_pre['A']) / z1a
        elif tn == 'B':
            i_load = (eb - v_pre['B']) / z1b
        else:
            i_load = (V_PH - v_pre['T']) / z1t if z1t is not None else 0.0
        i1 = i_load + i_f[1]
        i2 = i_f[2]
        i0 = i_f[0]
        v1 = v_pre[tn] + v_seq[1][tn]
        v2 = v_seq[2][tn]
        v0 = v_seq[0][tn]
        # phase quantities (rotate so the faulted phase is the reference)
        ia = i0 + i1 + i2
        ib = i0 + A ** 2 * i1 + A * i2
        ic = i0 + A * i1 + A ** 2 * i2
        va = v0 + v1 + v2
        vb = v0 + A ** 2 * v1 + A * v2
        vc = v0 + A * v1 + A ** 2 * v2
        ph_i = {'A': ia, 'B': ib, 'C': ic}
        ph_v = {'A': va, 'B': vb, 'C': vc}
        # the sequence solution put the fault on phase A; relabel to the fault's own phase(s)
        if nph == 1:
            lab = {'A': ref, 'B': {'A': 'B', 'B': 'C', 'C': 'A'}[ref], 'C': {'A': 'C', 'B': 'A', 'C': 'B'}[ref]}
        elif nph == 2:
            lab = {'A': ref, 'B': {'A': 'B', 'B': 'C', 'C': 'A'}[ref], 'C': {'A': 'C', 'B': 'A', 'C': 'B'}[ref]}
        else:
            lab = {'A': 'A', 'B': 'B', 'C': 'C'}
        I_ph = {lab[k]: v for k, v in ph_i.items()}
        V_ph = {lab[k]: v for k, v in ph_v.items()}
        out[tn] = dict(I=I_ph, V=V_ph, i0=i0, i1=i1, i2=i2)
    return out


def apparent_distance(meas, f, line, end):
    """the relay's own distance (km from its terminal) by the reactance method"""
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
    """attach to each fault what every relay recorded; build the relay event lists"""
    net, ld = w['net'], w['ld']
    rng = np.random.default_rng(C.EV_SEED + 404)
    er_rows, gv_rows, em_rows, ipp_rows = [], [], [], []
    storm_days = {}
    for f in w['faults']:
        storm_days[(f['t'].date(), f['line'])] = storm_days.get((f['t'].date(), f['line']), 0) + 1
    busy = {}
    for f in w['faults']:
        if f['cause'] == 'lightning':
            busy[f['t'].date()] = busy.get(f['t'].date(), 0) + 1
    seq_no = {}
    for f in w['faults']:
        line = net['lines'][f['line']]
        meas = fault_currents(net, f, ld)
        f['meas'] = {k: dict(I={p: abs(v) for p, v in m['I'].items()}, IG=abs(3 * m['i0'])) for k, m in meas.items()}
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
            # relay clock
            off = 0.0
            for (sc, sl), (t0, t1, rate) in CLOCK_FAULTS.items():
                if sc == st and t0 <= f['t'] <= t1:
                    off = rate * (f['t'] - t0).total_seconds() / 86400.0
            op = 0.018 + 0.012 * rng.random()   # relay operating time to the trip output (s)
            t_rel = f['t'] + dt.timedelta(seconds=op + off)
            seq_no[st] = seq_no.get(st, 1000 + int(rng.integers(0, 900))) + 1
            rec = dict(family=fam, station=st, line=f['line'], t=t_rel, offset=off, dist_km=dist,
                       dist_true=dist_true_from_end, I={p: abs(v) * (1 + rng.normal(0, 0.004)) for p, v in m['I'].items()},
                       IG=abs(3 * m['i0']) * (1 + rng.normal(0, 0.004)), lost=lost, event_no=seq_no[st])
            f['records'][end] = rec
        if 'T' in meas:
            m = meas['T']
            f['records']['ipp'] = dict(I={p: abs(v) for p, v in m['I'].items()}, IG=abs(3 * m['i0']),
                                       t=f['t'] + dt.timedelta(seconds=0.021 + 0.01 * rng.random()))
    return w
