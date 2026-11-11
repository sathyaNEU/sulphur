"""What the co-op's systems recorded: each protective device's operations through every fault, on its own clock;
the SCADA historian's event export for the breakers and the radio-linked reclosers; the event memories of the
reclosers with no radio link, read at each site visit; the outage management system's sustained outages; the
transformer replacement register."""
import numpy as np
import pandas as pd

PERM = {'lightning': 0.06, 'storm_wind': 0.22, 'typhoon': 0.55, 'animal': 0.33, 'vegetation': 0.45,
        'equipment': 0.85, 'third_party': 0.80, 'unknown': 0.12, 'arrester': 1.0}
SECOND_SHOT = {'lightning': 0.05, 'storm_wind': 0.40, 'typhoon': 0.35, 'animal': 0.25, 'vegetation': 0.35,
               'equipment': 0.0, 'third_party': 0.0, 'unknown': 0.2, 'arrester': 0.0}


def sequences(Z, faults, rng, t_end):
    """device operations (true time) for every fault, tracking lockouts so a dead zone does not fault again;
    returns operations, lockouts (with restoration) and the faults that actually happened"""
    zz = Z.set_index('zone_ix')
    parent = zz.parent_ix.to_dict()
    kind = zz.kind.to_dict()
    children = {}
    for z, p in parent.items():
        if p >= 0:
            children.setdefault(p, []).append(z)

    def downstream(z):
        out, stack = [], [z]
        while stack:
            x = stack.pop()
            out.append(x)
            stack += children.get(x, [])
        return out
    down = {z: downstream(z) for z in zz.index}
    open_until = {z: pd.Timestamp('1900-01-01') for z in zz.index}
    ops, locks, kept = [], [], []
    faults = faults.sort_values('t').reset_index(drop=True)
    for f in faults.itertuples():
        z = f.zone_ix
        t = pd.Timestamp(f.t)
        # dead if this zone or any upstream device is open
        x, dead = z, False
        while x >= 0:
            if open_until[x] > t:
                dead = True
                break
            x = parent[x]
        if dead:
            continue
        perm = rng.random() < (0.30 if (f.cause == 'lightning' and getattr(f, 'on_cracked', False)) else PERM[f.cause])
        brk = kind[z] == 'breaker'
        op = rng.uniform(0.045, 0.075) if brk else rng.uniform(0.035, 0.095)
        dead_t = [0.5, 15.0] if brk else [0.6, 2.0, 10.0]
        shots = len(dead_t) + 1 if perm else (2 if rng.random() < SECOND_SHOT[f.cause] else 1)
        ia = float(np.clip(rng.lognormal(np.log(2400 if brk else 1300), 0.45), 220, 9000))
        ph = rng.choice(['A', 'B', 'C', 'AB', 'BC', 'CA', 'ABC'], p=[0.28, 0.28, 0.28, 0.05, 0.04, 0.04, 0.03])
        tt = t + pd.Timedelta(seconds=op)
        for k in range(shots):
            ops.append((z, tt, 'TRIP', ph, round(ia * rng.uniform(0.93, 1.07))))
            if k < shots - 1 or not perm:
                if k < len(dead_t):
                    tt = tt + pd.Timedelta(seconds=dead_t[k] + rng.uniform(-0.02, 0.02))
                    ops.append((z, tt, 'RECLOSE', '', 0))
                    tt = tt + pd.Timedelta(seconds=rng.uniform(0.04, 0.25))
            if not perm and k == shots - 1:
                break
        if perm:
            ops.append((z, tt + pd.Timedelta(seconds=0.01), 'LOCKOUT', ph, 0))
            hours = rng.lognormal(np.log(9.0 if f.cause == 'typhoon' else 1.2), 0.6)
            tr = tt + pd.Timedelta(hours=float(hours))
            open_until[z] = tr
            locks.append((z, tt, tr, f.cause, f.Index))
            ops.append((z, tr, 'CLOSE', '', 0))
        # a downstream fault sometimes trips the upstream device too (miscoordination on a fast curve)
        if not brk and rng.random() < 0.04:
            p = parent[z]
            tp = t + pd.Timedelta(seconds=op + rng.uniform(0.005, 0.03))
            ops.append((p, tp, 'TRIP', ph, round(ia * rng.uniform(0.97, 1.03))))
            ops.append((p, tp + pd.Timedelta(seconds=(0.5 if kind[p] == 'breaker' else 0.6)), 'RECLOSE', '', 0))
        kept.append(f.Index)
    O = pd.DataFrame(ops, columns=['zone_ix', 't', 'event', 'phase', 'amps'])
    L = pd.DataFrame(locks, columns=['zone_ix', 't_lock', 't_restore', 'cause', 'fault_ix'])
    K = faults.loc[kept].copy()
    return O.sort_values('t').reset_index(drop=True), L, K, down


def routine_events(Z, t0, t1, rng):
    """switching, live-line tags, comms alarms: operations that are not faults"""
    rows = []
    days = (t1 - t0).days
    for z in Z.itertuples():
        for ev, rate in (('MANUAL OPEN', 3.0), ('HOT LINE TAG ON', 4.0)):
            n = rng.poisson(rate * days / 365.25)
            ts = t0 + pd.to_timedelta(np.sort(rng.uniform(0, days, n)), unit='D')
            ts = ts.normalize() + pd.to_timedelta(rng.uniform(8, 16, n), unit='h')
            for t in ts:
                rows.append((z.zone_ix, t, ev, '', 0))
                dur = pd.Timedelta(minutes=float(rng.uniform(25, 240)))
                rows.append((z.zone_ix, t + dur, 'MANUAL CLOSE' if ev == 'MANUAL OPEN' else 'HOT LINE TAG OFF', '', 0))
    return pd.DataFrame(rows, columns=['zone_ix', 't', 'event', 'phase', 'amps'])


def visits(Z, rng):
    """site visits to the reclosers with no radio link: the technician reads the event memory and sets the clock"""
    rows = []
    for z in Z[Z.telemetry == 'none'].itertuples():
        t = pd.Timestamp('2016-10-15') + pd.Timedelta(days=float(rng.uniform(0, 70)))
        while t < pd.Timestamp('2026-10-29'):
            hr = rng.uniform(8.5, 15.5)
            rows.append((z.zone_ix, t.normalize() + pd.Timedelta(hours=hr)))
            gap = float(np.clip(rng.lognormal(np.log(118), 0.33), 55, 240))
            # crews visit more in the dry season
            t = t + pd.Timedelta(days=gap)
    return pd.DataFrame(rows, columns=['zone_ix', 't'])


def device_events(Z, ops, routine, locks, down, V, rng, t0, t1):
    """every event each controller records, in true time, with its sequence number"""
    zz = Z.set_index('zone_ix')
    tele = zz.telemetry.to_dict()
    rows = [ops, routine]
    ac = []
    for l in locks.itertuples():
        for d in down[l.zone_ix][1:]:
            if tele[d] == 'none':
                ac.append((d, l.t_lock + pd.Timedelta(seconds=0.12), 'AC SUPPLY OFF', '', 0))
                ac.append((d, l.t_restore + pd.Timedelta(seconds=0.3), 'AC SUPPLY ON', '', 0))
    rows.append(pd.DataFrame(ac, columns=ops.columns))
    bt = []
    sundays = pd.date_range(t0 - pd.Timedelta(days=200), t1, freq='W-SUN') + pd.Timedelta(hours=3)
    for z in zz.index[zz.telemetry == 'none']:
        for s in sundays:
            bt.append((z, s + pd.Timedelta(seconds=float(rng.uniform(0, 2))), 'BATTERY TEST', '', 0))
    rows.append(pd.DataFrame(bt, columns=ops.columns))
    vv = []
    for v in V.itertuples():
        # the cabinet door switch, and the clock set once the memory has been read (this controller logs no read)
        vv.append((v.zone_ix, v.t - pd.Timedelta(minutes=float(rng.uniform(1.5, 4))), 'DOOR OPEN', '', 0))
        vv.append((v.zone_ix, v.t + pd.Timedelta(seconds=float(rng.uniform(40, 90))), 'CLOCK SET', '', 0))
    rows.append(pd.DataFrame(vv, columns=ops.columns))
    E = pd.concat(rows, ignore_index=True).sort_values(['zone_ix', 't']).reset_index(drop=True)
    E['seq'] = E.groupby('zone_ix').cumcount() + zz.reindex(E.zone_ix).index.map(
        lambda z: 0).values
    base = {z: int(rng.integers(1200, 48000)) for z in zz.index}
    E['seq'] = E.seq + E.zone_ix.map(base)
    return E


def stamp(Z, E, V, rng):
    """each event's time on its own device's clock"""
    zz = Z.set_index('zone_ix')
    out = np.empty(len(E), dtype='datetime64[ns]')
    tvals = E.t.values
    newt = tvals.copy()
    for z, idx in E.groupby('zone_ix').groups.items():
        idx = np.asarray(list(idx))
        tt = tvals[idx]
        if zz.telemetry[z] == 'SCADA':
            if zz.controller[z] == 'relay':
                off = rng.normal(0, 0.0012, len(idx))
            else:
                day = (tt.astype('datetime64[D]').astype(np.int64))
                ud = np.unique(day)
                od = dict(zip(ud, rng.normal(0, 0.11, len(ud))))
                off = np.array([od[d] for d in day]) + rng.normal(0, 0.004, len(idx))
        else:
            vs = V[V.zone_ix == z].t.sort_values().values
            sets = np.concatenate([[vs[0] - np.timedelta64(120, 'D')], vs + np.timedelta64(60, 's')])
            c = rng.normal(0, 0.6, len(sets))
            k = np.searchsorted(sets, tt, side='right') - 1
            k = np.clip(k, 0, None)
            days = (tt - sets[k]).astype('timedelta64[ns]').astype(np.int64) / 86400e9
            off = c[k] + zz.drift[z] * days + rng.normal(0, 0.004, len(idx))
        out[idx] = tt + (off * 1e9).astype('timedelta64[ns]')
        if zz.telemetry[z] != 'SCADA':
            # the weekly battery test runs at 03:00 on the controller's own clock: its stamp is the schedule, and it
            # happened that much earlier or later in true time
            bt = (E.event.values[idx] == 'BATTERY TEST')
            if bt.any():
                sched = tt[bt]
                newt[idx[bt]] = sched - (off[bt] * 1e9).astype('timedelta64[ns]')
                out[idx[bt]] = sched
    E = E.copy()
    E['t'] = pd.to_datetime(newt)
    E['ts'] = pd.to_datetime(out)
    # the controller numbers its events in the order it logs them
    E = E.sort_values(['zone_ix', 't'], kind='mergesort').reset_index(drop=True)
    E['seq'] = E.groupby('zone_ix').seq.transform('min').values + E.groupby('zone_ix').cumcount().values
    E['clock_offset'] = (E.ts - E.t).dt.total_seconds()
    return E


def downloads(Z, E, V):
    """each site visit reads the controller's memory: the last <memory> events before the read"""
    zz = Z.set_index('zone_ix')
    rows = []
    for k, v in enumerate(V.sort_values(['t', 'zone_ix']).itertuples()):
        cap = int(zz.memory[v.zone_ix])
        ez = E[(E.zone_ix == v.zone_ix) & (E.t <= v.t)]
        mem = ez.tail(cap)
        for r in mem.itertuples():
            rows.append((k, v.zone_ix, v.t, r.seq, r.ts, r.event, r.phase, r.amps))
    return pd.DataFrame(rows, columns=['download', 'zone_ix', 'visit_t', 'seq', 'ts', 'event', 'phase', 'amps'])
