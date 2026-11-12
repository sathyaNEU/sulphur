"""The operations of five years on Blue Earth Valley Power's network, event by event.

Faults strike main lines, laterals and transformers at rates the weather drives (thunderstorm cells, wind, ice,
deep cold) and each feeder's own exposure. A permanent main-line fault locks out the breaker or recloser above it.
On an automated loop that is armed, the ADMS runs its sequence: it reads the fault indicators, isolates the faulted
section by opening the next recloser (a control on a dead line runs on its battery), checks the receiving feeder's
breaker loading, switches the receiving reclosers to their transfer settings where their controls take the
command, and closes the tie. Commands are lost on weak radio paths and in storms; a control whose battery cannot
carry the operation browns out and does not answer. A transfer stays in place until the faulted section is repaired;
if the receiving path's reclosers were not switched and the combined load climbs past a pickup, the receiving
recloser trips. Operators restore what the automation did not, switching from the control room where the devices
answer and sending crews where they do not. The archive's event queue overflows on the busiest storm hours and
discards what it holds then, including the restoration messages the outage system takes from it. Batteries age by
unit, and are replaced on a cycle, after a failed operation or a failed self-test."""
import bisect
import datetime as dt
import math

import numpy as np

import common as C
import load as LD
import net as N
import weather as WX

COLD_K = 0.018          # internal resistance rises by this fraction per degree below 25 C
TEST_A, OP_A, V_MIN = 5.0, 30.0, 21.2


def round10(x):
    return int(10 * round(x / 10.0))


def settings(NET, L, W, rng):
    """protection pickups set when each loop was commissioned, from that summer's peak through each recloser, and not
    revisited since; the transfer group at about twice the normal group"""
    yrs = np.array([t.year for t in W['local']])
    mon = np.array([t.month for t in W['local']])
    loops = {Lp['loop']: Lp for Lp in NET['loops']}
    for a, D in NET['devices'].items():
        if D['kind'] not in ('R1', 'R2'):
            continue
        f = D['feeder']
        F = NET['feeders'][f]
        y = max(2022, loops[D['loop']]['commissioned'].year)
        m = (yrs == y) & (mon >= 6) & (mon <= 9)
        flow = L['amps'][(f, 3)] if D['kind'] == 'R2' else L['amps'][(f, 2)] + L['amps'][(f, 3)]
        pk = float(np.percentile(flow[m], 99.5))
        # older settings were cut closer; growth since has used the margin up on some sections
        if D['ctl'] == 'CTL-4C':
            mult = rng.uniform(1.55, 2.05)
        else:
            mult = rng.uniform(1.9, 2.6)
        D['pickup1'] = max(140, round10(mult * pk))
        D['pickup2'] = round10(D['pickup1'] * rng.uniform(1.9, 2.3))
        D['set_year'] = y
    for f in NET['loop_feeders']:
        F = NET['feeders'][f]
        m24 = (yrs == 2024) & (mon >= 6) & (mon <= 9)
        F['cb_pickup'] = max(F['cb_pickup'], round10(1.6 * load_peak_cb(L, f, m24)))


def load_peak_cb(L, f, mask):
    return float(np.percentile(LD.device_flow(L, f, 'CB')[mask], 99.5))


def dev_of(NET, f, kind):
    for a, D in NET['devices'].items():
        if D['feeder'] == f and D['kind'] == kind:
            return a
    return None


def tie_of(NET, loop):
    for a, D in NET['devices'].items():
        if D['loop'] == loop and D['kind'] == 'TS':
            return a
    return None


class Batteries:
    """each recloser control's batteries over time: installed, aged at the unit's own rate, replaced on the four-year
    cycle (the programme runs late more often than early), after a failed operation or after a self-test alarm"""

    def __init__(self, NET, rng):
        self.rng = rng
        self.b = {}          # asset -> list of [install_date, R0, g, removed_date or None, reason_in]
        for a, D in NET['devices'].items():
            if D['kind'] not in ('R1', 'R2'):
                continue
            self.b[a] = [[D['batt0'], self._r0(), self._g(), None,
                          'commissioning' if D['batt0'] == D['installed'] else 'scheduled']]
            self._extend(a, dt.date(2027, 12, 31))

    def _r0(self):
        return float(np.clip(self.rng.normal(0.0240, 0.0017), 0.019, 0.03))

    def _g(self):
        return float(np.clip(self.rng.lognormal(np.log(0.25), 0.36), 0.06, 0.45))

    def _slip(self):
        # the cycle is four years; the crews run behind, sometimes by a year or more
        return float(self.rng.choice([self.rng.uniform(-0.15, 0.25), self.rng.uniform(0.3, 1.1),
                                      self.rng.uniform(1.1, 2.3)], p=[0.45, 0.38, 0.17]))

    def _extend(self, a, until):
        while True:
            last = self.b[a][-1]
            nxt = last[0] + dt.timedelta(days=int((4.0 + self._slip()) * 365.25))
            if nxt > until:
                break
            last[3] = nxt
            self.b[a].append([nxt, self._r0(), self._g(), None, 'scheduled'])

    def current(self, a, when):
        cur = self.b[a][0]
        for rec in self.b[a]:
            if rec[0] <= when:
                cur = rec
        return cur

    def r25(self, a, when):
        rec = self.current(a, when)
        age = (when - rec[0]).days / 365.25
        return rec[1] * math.exp(rec[2] * max(0.0, age))

    def replace(self, a, when, reason):
        """an unscheduled replacement: the cycle restarts from it"""
        cur = self.current(a, when)
        if cur[0] >= when:
            return False
        keep = [r for r in self.b[a] if r[0] <= when]
        keep[-1][3] = when
        keep.append([when, self._r0(), self._g(), None, reason])
        self.b[a] = keep
        self._extend(a, dt.date(2027, 12, 31))
        return True


def v_oc(T):
    return 25.6 - 0.006 * max(0.0, 5.0 - T)


def r_at(r25, T_cab):
    return r25 * math.exp(COLD_K * (25.0 - T_cab))


CAB = 2.0      # a control cabinet runs about two degrees above the air


def operates(r25, T_air):
    T_cab = T_air + CAB
    return v_oc(T_cab) - OP_A * r_at(r25, T_cab) >= V_MIN


def comms_down_intervals(NET, W, rng):
    """link-down episodes per device (hours since T0, start and end as floats)"""
    H = W['H']
    out = {}
    sky0 = C.hour_index(dt.datetime(2025, 6, 2, 19, 40, tzinfo=dt.timezone.utc))
    sky1 = C.hour_index(dt.datetime(2025, 9, 12, 16, 15, tzinfo=dt.timezone.utc))
    for a, D in NET['devices'].items():
        if D['kind'] not in ('R1', 'R2', 'TS'):
            continue
        rate = 0.028 * (D['q'] / 0.012) ** 0.85 / 24.0
        iv = []
        h = rng.exponential(1 / rate)
        while h < H:
            dur = rng.lognormal(np.log(0.9 if D['q'] < 0.1 else 2.6), 0.8)
            iv.append((h, h + dur))
            h += dur + rng.exponential(1 / rate)
        if D['site'] == 'Skyline Tower':
            h = sky0
            while h < sky1:
                up = rng.lognormal(np.log(4.0), 0.9)
                dn = rng.lognormal(np.log(3.2), 0.9)
                iv.append((h + up, min(sky1, h + up + dn)))
                h += up + dn
        iv.sort()
        out[a] = iv
    return out, (sky0, sky1)


def is_down(iv, h):
    i = bisect.bisect_right(iv, (h, float('inf'))) - 1
    return i >= 0 and iv[i][0] <= h < iv[i][1]


def draw_faults(NET, W, rng):
    """every fault: hour, offset seconds, feeder, where (section 1-3, lateral, transformer), permanent, low-current"""
    H = W['H']
    storm, gust, ice, T = W['storm'], W['gust'], W['ice'], W['temp']
    doy = W['doy']
    wind = np.clip(gust - 45, 0, None) / 30.0
    cold = np.clip(-12.0 - T, 0, None) / 10.0
    animal = 1.0 + 0.6 * (np.exp(-((doy - 110) / 25) ** 2) + np.exp(-((doy - 285) / 25) ** 2))
    mult = animal + 9.0 * storm + 4.0 * wind ** 1.3 + 12.0 * ice + 3.6 * cold ** 1.2
    faults = []
    for f in NET['fids']:
        F = NET['feeders'][f]
        ex = F['exposure']
        for S in F['sections']:
            base_perm = 0.072 / 8760.0 * S['km'] * ex
            lam = base_perm * mult
            n = rng.poisson(lam)
            for h in np.nonzero(n)[0]:
                for _ in range(int(n[h])):
                    faults.append((int(h), float(rng.uniform(0, 3600)), f, S['s'], 'main', True,
                                   bool(rng.random() < 0.11)))
            lam_t = 2.6 * base_perm * mult
            n = rng.poisson(lam_t)
            for h in np.nonzero(n)[0]:
                for _ in range(int(n[h])):
                    faults.append((int(h), float(rng.uniform(0, 3600)), f, S['s'], 'main', False, False))
            lam_l = 5.2 * S['lat_rate'] * S['cust0'] / 1000.0 / 8760.0 * ex * (0.45 + 0.55 * mult)
            n = rng.poisson(lam_l)
            for h in np.nonzero(n)[0]:
                for _ in range(int(n[h])):
                    faults.append((int(h), float(rng.uniform(0, 3600)), f, S['s'], 'lateral', True, False))
            lam_x = 12.5 * S['cust0'] / 1000.0 / 8760.0 * (0.7 + 0.3 * mult + 0.4 * np.clip(T - 28, 0, None))
            n = rng.poisson(lam_x)
            for h in np.nonzero(n)[0]:
                for _ in range(int(n[h])):
                    faults.append((int(h), float(rng.uniform(0, 3600)), f, S['s'], 'xfmr', True, False))
    faults.sort()
    return faults


def simulate():
    NET = N.build()
    W = WX.simulate()
    L = LD.simulate(NET, W)
    rng = np.random.default_rng(C.EV_SEED)
    settings(NET, L, W, rng)
    BAT = Batteries(NET, rng)
    down, sky = comms_down_intervals(NET, W, rng)
    faults = draw_faults(NET, W, rng)
    H = W['H']
    T = W['temp']
    # system-wide trips per hour (every main-line trip, transient or not) drive the ADMS alarm load
    trips_h = np.zeros(H)
    perm_h = np.zeros(H)
    for fl in faults:
        if fl[4] == 'main':
            trips_h[fl[0]] += 1 if fl[5] else 2
        if fl[5]:
            perm_h[fl[0]] += 1          # every outage the dispatchers open: main lines, laterals, transformers
    alarm = 35 + 190 * trips_h + 600 * W['storm']
    overflow_h = alarm > 640
    # overflow windows: contiguous runs of overflowing hours, trimmed to minutes
    windows = []
    h = 0
    while h < H:
        if overflow_h[h]:
            h1 = h
            while h1 + 1 < H and overflow_h[h1 + 1]:
                h1 += 1
            s = h + rng.uniform(0.05, 0.55)
            e = h1 + rng.uniform(0.45, 0.98) + rng.uniform(0.4, 2.2)     # the backlog takes a while to clear
            windows.append((s, e))
            h = h1 + 1
        else:
            h += 1

    def in_overflow(hf):
        for s, e in windows:
            if s <= hf < e:
                return True
        return False

    loops = {Lp['loop']: Lp for Lp in NET['loops']}
    devs = NET['devices']
    feeders = NET['feeders']
    lf = set(NET['loop_feeders'])
    recon = {r['feeder']: r for r in NET['recon']}
    yearfrac = L['yearfrac']
    amps = L['amps']

    def cust(f, k, h):
        return int(round(N.section_customers(feeders[f], k, yearfrac[h], recon)))

    def sec_amps(f, k, h):
        return float(amps[(f, k)][h])

    events = []        # every protective, switching and control event (SCADA sequence of events)
    adms = []          # every FLISR archive message (before the archive's losses)
    oms = []           # outage records
    seqs = []          # the FLISR sequences, with their full truth
    batt_fail = []
    abnormal_until = {}     # loop -> hour float the loop returns to normal
    rtn_events = []
    manual_transfers = []
    disarm_log = []
    mech_fail_p = 0.008
    engine_busy = [None]
    lids = [Lp['loop'] for Lp in NET['loops']]
    sup_pick = list(rng.choice(lids, size=3, replace=False))
    supervised = {sup_pick[0]: (dt.datetime(2024, 3, 11, 15, tzinfo=dt.timezone.utc), dt.datetime(2024, 9, 30, 15, tzinfo=dt.timezone.utc)),
                  sup_pick[1]: (dt.datetime(2025, 4, 22, 15, tzinfo=dt.timezone.utc), dt.datetime(2026, 2, 17, 16, tzinfo=dt.timezone.utc)),
                  sup_pick[2]: (dt.datetime(2026, 5, 6, 15, tzinfo=dt.timezone.utc), dt.datetime(2027, 1, 1, tzinfo=dt.timezone.utc))}
    NET['supervised'] = supervised

    # scheme arm state changes (disarmed while any of its devices is unreachable)
    for Lp in NET['loops']:
        lid = Lp['loop']
        members = [dev_of(NET, Lp['a'], 'R1'), dev_of(NET, Lp['a'], 'R2'), dev_of(NET, Lp['b'], 'R1'),
                   dev_of(NET, Lp['b'], 'R2'), tie_of(NET, lid)]
        start_h = C.hour_index(dt.datetime.combine(Lp['commissioned'], dt.time(12), tzinfo=dt.timezone.utc))
        ivs = sorted((s, e, a) for a in members for (s, e) in down[a] if e > max(0, start_h))
        for s, e, a in ivs:
            if s < 0:
                continue
            disarm_log.append((s, lid, a, 'disarm'))
            disarm_log.append((e, lid, a, 'arm'))
    disarm_log.sort()

    def armed(lid, hf):
        Lp = loops[lid]
        if hf < C.hour_index(dt.datetime.combine(Lp['commissioned'], dt.time(12), tzinfo=dt.timezone.utc)):
            return False, 'not commissioned'
        for a in [dev_of(NET, Lp['a'], 'R1'), dev_of(NET, Lp['a'], 'R2'), dev_of(NET, Lp['b'], 'R1'),
                  dev_of(NET, Lp['b'], 'R2'), tie_of(NET, lid)]:
            if is_down(down[a], hf):
                return False, a
        if abnormal_until.get(lid, -1) > hf:
            return False, 'abnormal'
        return True, None

    oms_no = {}

    def oms_id(when):
        y = C.to_local(when).year
        oms_no[y] = oms_no.get(y, int(rng.integers(100, 400))) + int(rng.integers(1, 4))
        return 'OMS-%d-%06d' % (y, oms_no[y])

    def crew_minutes(hf, storm_load, kind):
        lt = C.to_local(C.ts_of(0) + dt.timedelta(hours=hf))
        night = lt.hour < 6 or lt.hour >= 22
        base = {'switch': 58.0, 'repair_main': 270.0, 'repair_lat': 150.0, 'repair_xfmr': 190.0}[kind]
        m = base * (1.35 if night else 1.0) * (1 + 0.55 * min(storm_load, 4))
        return float(m * rng.lognormal(0, 0.35))

    def storm_load(h):
        lo, hi = max(0, h - 2), min(H, h + 3)
        return float(trips_h[lo:hi].sum() / 3.0)

    def workload(h):
        """main-line lockouts the control room is working at once, around this hour"""
        lo, hi = max(0, h - 1), min(H, h + 2)
        return float(perm_h[lo:hi].sum())

    def remote_minutes(h):
        return float(7.0 + 1.35 * max(0.0, workload(h) - 1) + rng.lognormal(np.log(5.0), 0.55))

    tests = []
    d = dt.datetime(2021, 12, 5, 9, 0, tzinfo=dt.timezone.utc)      # Sundays, 03:00 Central Standard Time
    while d < C.T_END:
        tests.append((C.hour_index(d), 0.0, None, None, 'test', None, None))
        d += dt.timedelta(days=7)
    timeline = sorted(faults + tests, key=lambda x: (x[0], x[1]))
    rcl = sorted(a for a in devs if devs[a]['kind'] in ('R1', 'R2'))
    selftests = []
    for fl in timeline:
        h, off, f, k, where, perm, hiz = fl
        hf = h + off / 3600.0
        when = C.ts_of(h, off)
        Tair = float(T[h])
        if where == 'test':
            for a in rcl:
                if when.date() < devs[a]['installed']:
                    continue
                t_a = when + dt.timedelta(seconds=float(rng.uniform(0, 240)))
                r25 = BAT.r25(a, t_a.date())
                T_cab = Tair + CAB
                vr = v_oc(T_cab) + float(rng.normal(0, 0.06))
                vl = vr - TEST_A * r_at(r25, T_cab) * float(np.exp(rng.normal(0, 0.03))) + float(rng.normal(0, 0.012))
                if is_down(down[a], hf + 0.05):
                    continue
                selftests.append({'t': t_a, 'dev': a, 'v_rest': vr, 'v_load': vl})
                if vl < 24.40:
                    events.append({'t': t_a + dt.timedelta(seconds=2), 'dev': a, 'feeder': devs[a]['feeder'],
                                   'ev': 'BATTERY TEST FAIL', 'amps': None, 'src': 'CTL'})
                    BAT.replace(a, (t_a + dt.timedelta(days=float(rng.uniform(6, 30)))).date(), 'battery test alarm')
            continue
        if when < C.REC0 - dt.timedelta(days=20):
            continue
        F = feeders[f]
        if where == 'xfmr':
            n = int(rng.choice([1, 2, 3, 4, 5, 6, 8, 11, 14], p=[.18, .14, .14, .13, .12, .1, .08, .06, .05]))
            dur = crew_minutes(hf, storm_load(h), 'repair_xfmr')
            call_lag = rng.lognormal(np.log(14), 0.9) * (2.6 if C.to_local(when).hour < 6 else 1.0)
            oms.append({'id': oms_id(when), 'feeder': f, 'device': 'XFMR', 'sec': k, 'start': when + dt.timedelta(minutes=call_lag),
                        'true_start': when, 'cust': n, 'steps': [(dur, n, 'repair', k)], 'cause': None, 'kind': 'xfmr',
                        'storm': storm_load(h)})
            continue
        if where == 'lateral':
            n = int(rng.integers(12, 160))
            dur = crew_minutes(hf, storm_load(h), 'repair_lat')
            call_lag = rng.lognormal(np.log(9), 0.8) * (2.2 if C.to_local(when).hour < 6 else 1.0)
            oms.append({'id': oms_id(when), 'feeder': f, 'device': 'FUSE', 'sec': k, 'start': when + dt.timedelta(minutes=call_lag),
                        'true_start': when, 'cust': n, 'steps': [(dur, n, 'repair', k)], 'cause': None, 'kind': 'lateral',
                        'storm': storm_load(h)})
            continue
        # main-line fault: which device trips (miscoordination: the breaker for a close-in section 2 fault)
        if f in lf:
            trip_dev = {1: 'CB', 2: 'R1', 3: 'R2'}[k]
            if k == 2 and perm and rng.random() < 0.13:
                trip_dev = 'CB'
        else:
            trip_dev = 'CB'
        dev_id = (f + ' CB') if trip_dev == 'CB' else dev_of(NET, f, trip_dev)
        cur = float(rng.lognormal(np.log(2400), 0.5)) if not hiz else float(rng.uniform(260, 520))
        if not perm:
            events.append({'t': when, 'dev': dev_id, 'feeder': f, 'ev': 'TRIP', 'amps': round(cur), 'src': 'PROT'})
            events.append({'t': when + dt.timedelta(seconds=float(rng.uniform(1.5, 3.0))), 'dev': dev_id, 'feeder': f,
                           'ev': 'RECLOSE SUCCESS', 'amps': None, 'src': 'PROT'})
            continue
        t_lo = when + dt.timedelta(seconds=float(rng.uniform(28, 64)))
        events.append({'t': when, 'dev': dev_id, 'feeder': f, 'ev': 'TRIP', 'amps': round(cur), 'src': 'PROT'})
        events.append({'t': t_lo, 'dev': dev_id, 'feeder': f, 'ev': 'LOCKOUT', 'amps': None, 'src': 'PROT'})
        # customers downstream of the tripping device
        secs_out = {'CB': [1, 2, 3], 'R1': [2, 3], 'R2': [3]}[trip_dev] if f in lf else [1]
        c_out = {s: cust(f, s, h) for s in secs_out}
        repair = crew_minutes(hf, storm_load(h), 'repair_main')
        rec = {'id': oms_id(when), 'feeder': f, 'device': dev_id, 'sec': k, 'start': when, 'true_start': when,
               'cust': sum(c_out.values()), 'steps': [], 'cause': None, 'kind': 'main', 'storm': storm_load(h),
               'trip_dev': trip_dev}
        oms.append(rec)
        in_service = False
        if f in lf:
            lid = F['loop']
            Lp = loops[lid]
            in_service = hf >= C.hour_index(dt.datetime.combine(Lp['commissioned'], dt.time(12), tzinfo=dt.timezone.utc))
        if not in_service:
            # no automation: crews switch what they can and repair the rest
            sw = min(crew_minutes(hf, storm_load(h), 'switch'), repair * 0.9)
            tot = sum(c_out.values())
            a1 = int(tot * rng.uniform(0.25, 0.6)) if f not in lf else sum(c_out[s] for s in c_out if s != k)
            rec['steps'] = [(sw, a1, 'field', None), (repair, tot - a1, 'repair', k)]
            continue
        other = F['partner']
        ok, why = armed(lid, hf + 0.01)
        S = {'loop': lid, 'feeder': f, 'recv': other, 'sec': k, 'trip_dev': trip_dev, 'when': when, 't_lo': t_lo,
             'hiz': hiz, 'temp': Tair, 'oms': rec['id'], 'steps': [], 'outcome': None, 'cause': None,
             'restored': 0, 't_rest': None, 'harm': 0, 'harm_kind': None, 'storm': storm_load(h), 'h': h}
        seqs.append(S)
        if k == 3 and trip_dev == 'R2':
            S['outcome'] = 'no restoration possible'
        if not ok:
            S['outcome'] = S['outcome'] or 'not armed'
            S['cause'] = 'not armed' if S['outcome'] == 'not armed' else None
            S['armed_why'] = why
        t = t_lo + dt.timedelta(seconds=float(rng.uniform(2, 8)))
        if S['outcome'] is None and engine_busy[0] is not None and engine_busy[0] > t:
            t = engine_busy[0] + dt.timedelta(seconds=float(rng.uniform(6, 25)))
        S['steps'].append((t, 'START', {'lockout': dev_id}))
        if S['outcome'] in ('not armed',):
            S['steps'][-1] = (t, 'NOT STARTED', {'lockout': dev_id, 'why': why})
        restored_secs = []
        isolated_ok = True
        congestion = min(4.0, storm_load(h))

        bad_link = {}

        def command(dev, t, op, alive):
            """a command to a device: (ok, t_done, failure kind); a path that is bad for this sequence stays bad"""
            D = devs[dev]
            if dev not in bad_link:
                bad_link[dev] = rng.random() < min(0.75, 3.6 * D['q'] * (1.0 + 0.9 * congestion))
            p_to = 0.97 if bad_link[dev] else 0.02
            if dev in down and is_down(down[dev], (t - C.T0).total_seconds() / 3600.0):
                p_to = 1.0
            rt = float(rng.lognormal(np.log(4.0 + 3.0 * congestion), 0.35))
            if in_overflow((t - C.T0).total_seconds() / 3600.0):
                # the front end is saturated: every round trip waits behind the storm's alarm traffic
                rt = float(rng.lognormal(np.log(58.0), 0.3))
            tries = 0
            while True:
                tries += 1
                if not alive and D['kind'] in ('R1', 'R2'):
                    r25 = BAT.r25(dev, t.date())
                    if not operates(r25, Tair):
                        return False, t + dt.timedelta(seconds=30), 'battery', tries
                if rng.random() >= p_to:
                    if rng.random() < mech_fail_p:
                        return False, t + dt.timedelta(seconds=rt), 'mechanism', tries
                    return True, t + dt.timedelta(seconds=rt), None, tries
                t = t + dt.timedelta(seconds=30)
                if tries >= 2:
                    return False, t, 'comms', tries

        if S['outcome'] is None:
            # fault indicators: devices upstream of the fault that carried its current indicate
            fpi = {}
            path = {'CB': ['R1', 'R2'], 'R1': ['R2'], 'R2': []}[trip_dev]
            for kind in path:
                d = dev_of(NET, f, kind)
                carried = (kind == 'R1' and k >= 2) or (kind == 'R2' and k >= 3)
                if carried:
                    miss = 0.03 + (0.5 if hiz else 0.0)
                    fpi[kind] = rng.random() >= miss
                else:
                    false_ind = 0.012 + 0.08 * F['sections'][2]['pv'] * (kind == 'R2')
                    fpi[kind] = rng.random() < false_ind
            # read the indicators (radio)
            t2 = t + dt.timedelta(seconds=float(rng.uniform(2, 5)))
            read_ok = True
            for kind in path:
                d = dev_of(NET, f, kind)
                okc, t2, fk, tries = command(d, t2, 'read', True)
                if not okc:
                    read_ok = False
                    S['steps'].append((t2, 'TIMEOUT', {'dev': d, 'op': 'read'}))
                    S['outcome'], S['cause'] = 'failed', 'communications' if fk == 'comms' else 'control'
                    break
                S['steps'].append((t2, 'FPI', {'dev': d, 'ind': fpi[kind]}))
            if read_ok:
                # locate: the section after the last indicating device
                order = ['CB'] + path
                last = 'CB'
                for kind in path:
                    if fpi[kind]:
                        last = kind
                    else:
                        break
                if trip_dev != 'CB':
                    last = trip_dev if not any(fpi.get(x) for x in path) else last
                loc_sec = {'CB': 1, 'R1': 2, 'R2': 3}[last]
                S['located'] = loc_sec
                S['steps'].append((t2 + dt.timedelta(seconds=1), 'LOCATED', {'sec': loc_sec}))
                if loc_sec == 3:
                    S['outcome'] = 'no restoration possible' if k == 3 else 'failed'
                    if k != 3:
                        # the scheme thinks the fault is beyond R2: it recloses the upstream device onto the fault
                        S['cause'] = 'fault location'
                        S['steps'].append((t2 + dt.timedelta(seconds=3), 'CLOSE ONTO FAULT', {'dev': dev_id}))
                else:
                    iso = {1: 'R1', 2: 'R2'}[loc_sec]
                    iso_dev = dev_of(NET, f, iso)
                    t3 = t2 + dt.timedelta(seconds=float(rng.uniform(1, 3)))
                    okc, t3, fk, tries = command(iso_dev, t3, 'open', False)
                    if not okc:
                        S['steps'].append((t3, 'TIMEOUT' if fk in ('comms', 'battery') else 'OP FAILED',
                                           {'dev': iso_dev, 'op': 'open'}))
                        S['outcome'] = 'failed'
                        S['cause'] = {'comms': 'communications', 'battery': 'control', 'mechanism': 'control'}[fk]
                        S['true_cause'] = fk
                        if fk == 'battery':
                            batt_fail.append((t3, iso_dev, Tair))
                            BAT.replace(iso_dev, (t3 + dt.timedelta(days=float(rng.uniform(9, 45)))).date(),
                                        'failed to operate')
                            events.append({'t': t3 + dt.timedelta(minutes=repair + float(rng.uniform(1, 40))),
                                           'dev': iso_dev, 'feeder': f, 'ev': 'CONTROL POWER UP', 'amps': None,
                                           'src': 'CTL'})
                            events.append({'t': t3 + dt.timedelta(minutes=repair + float(rng.uniform(41, 90))),
                                           'dev': iso_dev, 'feeder': f, 'ev': 'BATTERY LOW ALARM', 'amps': None,
                                           'src': 'CTL'})
                    else:
                        S['steps'].append((t3, 'OPENED', {'dev': iso_dev}))
                        events.append({'t': t3, 'dev': iso_dev, 'feeder': f, 'ev': 'OPEN', 'amps': None,
                                       'src': 'ADMS'})
                        # upstream restoration when the breaker locked out for a section 2 fault
                        if trip_dev == 'CB' and loc_sec == 2:
                            r1 = dev_of(NET, f, 'R1')
                            okc, t3b, fk, tries = command(r1, t3, 'open', False)
                            if okc:
                                events.append({'t': t3b, 'dev': r1, 'feeder': f, 'ev': 'OPEN', 'amps': None, 'src': 'ADMS'})
                                events.append({'t': t3b + dt.timedelta(seconds=4), 'dev': f + ' CB', 'feeder': f,
                                               'ev': 'CLOSE', 'amps': None, 'src': 'ADMS'})
                                S['steps'].append((t3b + dt.timedelta(seconds=4), 'UPSTREAM RESTORED', {'sec': 1}))
                                restored_secs.append((1, t3b + dt.timedelta(seconds=4)))
                        # downstream sections to transfer
                        down_secs = [s for s in (2, 3) if s > loc_sec]
                        T_amps = sum(sec_amps(f, s, h) for s in down_secs)
                        recv = other
                        cb_load = float(LD.device_flow(L, recv, 'CB')[h])
                        lim = feeders[recv]['emerg_amps']
                        S['xfer_amps'] = T_amps
                        S['steps'].append((t3 + dt.timedelta(seconds=1), 'CAPACITY',
                                           {'recv': recv, 'load': cb_load, 'xfer': T_amps, 'limit': lim}))
                        if cb_load + T_amps > lim:
                            S['outcome'], S['cause'] = 'blocked', 'capacity'
                        else:
                            r1b, r2b = dev_of(NET, recv, 'R1'), dev_of(NET, recv, 'R2')
                            configured = devs[r1b]['ctl'] == 'CTL-6' and devs[r2b]['ctl'] == 'CTL-6'
                            S['configured'] = configured
                            t4 = t3 + dt.timedelta(seconds=2)
                            grp_ok = True
                            if configured:
                                for d in (r1b, r2b):
                                    okc, t4, fk, tries = command(d, t4, 'group', True)
                                    if not okc:
                                        grp_ok = False
                                        S['steps'].append((t4, 'TIMEOUT', {'dev': d, 'op': 'group'}))
                                        S['outcome'], S['cause'] = 'failed', 'communications'
                                        break
                                    S['steps'].append((t4, 'GROUP2', {'dev': d}))
                                    events.append({'t': t4, 'dev': d, 'feeder': recv, 'ev': 'SETTINGS GROUP 2',
                                                   'amps': None, 'src': 'ADMS'})
                            if grp_ok:
                                tie = tie_of(NET, lid)
                                sv = supervised.get(lid)
                                if sv and sv[0] <= t4 < sv[1]:
                                    S['steps'].append((t4 + dt.timedelta(seconds=1), 'AWAIT CONFIRM', {}))
                                    t4 = t4 + dt.timedelta(minutes=remote_minutes(h) * float(rng.uniform(0.35, 0.9)))
                                    S['steps'].append((t4, 'CONFIRMED', {}))
                                    S['supervised'] = True
                                okc, t5, fk, tries = command(tie, t4 + dt.timedelta(seconds=1), 'close', True)
                                if not okc:
                                    S['steps'].append((t5, 'TIMEOUT' if fk == 'comms' else 'OP FAILED',
                                                       {'dev': tie, 'op': 'close'}))
                                    S['outcome'] = 'failed'
                                    S['cause'] = 'communications' if fk == 'comms' else 'control'
                                else:
                                    events.append({'t': t5, 'dev': tie, 'feeder': lid, 'ev': 'CLOSE', 'amps': None,
                                                   'src': 'ADMS'})
                                    if k in down_secs:
                                        # the fault is inside the transferred part: the receiving path trips
                                        hit = r2b
                                        events.append({'t': t5 + dt.timedelta(seconds=0.2), 'dev': hit, 'feeder': recv,
                                                       'ev': 'TRIP', 'amps': round(cur * 0.8), 'src': 'PROT'})
                                        events.append({'t': t5 + dt.timedelta(seconds=float(rng.uniform(25, 50))),
                                                       'dev': hit, 'feeder': recv, 'ev': 'LOCKOUT', 'amps': None,
                                                       'src': 'PROT'})
                                        S['steps'].append((t5 + dt.timedelta(seconds=1), 'RECV TRIPPED ON CLOSE',
                                                           {'dev': hit}))
                                        S['outcome'], S['cause'] = 'failed', 'fault location'
                                        S['harm'] = cust(recv, 3, h)
                                        S['harm_kind'] = 'close onto fault'
                                        S['harm_dev'] = hit
                                        S['harm_t'] = t5
                                    else:
                                        tr = t5
                                        n_rest = sum(cust(f, s, h) for s in down_secs)
                                        n_up = sum(cust(f, s, h) for s, _t in restored_secs if s == 1)
                                        S['restored'] = n_rest
                                        S['t_rest'] = tr
                                        S['outcome'] = 'restored'
                                        restored_secs += [(s, tr) for s in down_secs]
                                        S['steps'].append((tr + dt.timedelta(seconds=1), 'COMPLETE', {'n': n_rest + n_up}))
                                        S['restored_up'] = n_up
        if S['steps']:
            last_t = max(x[0] for x in S['steps'])
            if engine_busy[0] is None or last_t > engine_busy[0]:
                engine_busy[0] = last_t
        # the outage record's steps (minutes after the fault) and the return to normal
        t_rep = when + dt.timedelta(minutes=repair)
        steps = []
        rest_map = {}
        for s, tr in restored_secs:
            rest_map[s] = tr
        if S.get('outcome') == 'restored' or rest_map:
            for s, tr in sorted(rest_map.items(), key=lambda x: x[1]):
                steps.append(((tr - when).total_seconds() / 60.0, cust(f, s, h), 'flisr', s))
        # sections not restored by the scheme: operator remote switching, or crews
        left = [s for s in secs_out if s not in rest_map and s != k]
        if left:
            remote = all(not is_down(down[a], hf + 0.2) for a in
                         [dev_of(NET, f, 'R1'), dev_of(NET, f, 'R2'), tie_of(NET, lid)])
            remote = remote and S.get('cause') != 'control'
            base_t = remote_minutes(h) if remote else crew_minutes(hf, storm_load(h), 'switch')
            base_t = min(base_t, repair * 0.95)
            recv = other
            for s in left:
                # operators transfer only after placing the receiving reclosers in their transfer group
                steps.append((base_t + float(rng.uniform(0, 3)), cust(f, s, h), 'remote' if remote else 'field', s))
            if any(s > k for s in left):
                manual_transfers.append({'loop': lid, 'feeder': f, 'recv': recv, 'when': when + dt.timedelta(minutes=base_t)})
                for d in (dev_of(NET, recv, 'R1'), dev_of(NET, recv, 'R2')):
                    events.append({'t': when + dt.timedelta(minutes=base_t - 1.5), 'dev': d, 'feeder': recv,
                                   'ev': 'SETTINGS GROUP 2', 'amps': None, 'src': 'SCADA OPERATOR'})
                events.append({'t': when + dt.timedelta(minutes=base_t), 'dev': tie_of(NET, lid), 'feeder': lid,
                               'ev': 'CLOSE', 'amps': None, 'src': 'SCADA OPERATOR'})
        steps.append((repair, cust(f, k, h) if k in secs_out else 0, 'repair', k))
        rec['steps'] = steps
        rec['seq'] = S
        # a transfer stays until the repair; on an unswitched receiving path the combined load may trip a recloser
        if S.get('outcome') == 'restored' and S['t_rest'] is not None:
            recv = other
            t_rtn = t_rep + dt.timedelta(minutes=float(rng.uniform(6, 35)))
            abnormal_until[lid] = (t_rtn - C.T0).total_seconds() / 3600.0
            rtn_events.append((t_rtn, lid))
            S['t_rtn'] = t_rtn
            S['iso_dev'] = dev_of(NET, f, {1: 'R1', 2: 'R2'}[S['located']])
            if not S.get('configured', True):
                r1b, r2b = dev_of(NET, recv, 'R1'), dev_of(NET, recv, 'R2')
                xs = [s for s in (2, 3) if s > S['located']]
                hh0 = int((S['t_rest'] - C.T0).total_seconds() // 3600)
                hh1 = int((t_rtn - C.T0).total_seconds() // 3600)
                for hh in range(hh0, min(H, hh1 + 1)):
                    xa = sum(sec_amps(f, s, hh) for s in xs)
                    c2 = sec_amps(recv, 3, hh) + xa
                    c1 = sec_amps(recv, 2, hh) + c2
                    pk = 1.03 + 0.045 * rng.random()
                    tripped = None
                    if c2 * pk > devs[r2b]['pickup1']:
                        tripped = (r2b, c2 * pk)
                    elif c1 * pk > devs[r1b]['pickup1']:
                        tripped = (r1b, c1 * pk)
                    if tripped:
                        lo_t = max(S['t_rest'] + dt.timedelta(minutes=2), C.ts_of(hh, float(rng.uniform(0, 3600))))
                        d, ia = tripped
                        events.append({'t': lo_t, 'dev': d, 'feeder': recv, 'ev': 'TRIP', 'amps': round(ia),
                                       'src': 'PROT'})
                        events.append({'t': lo_t + dt.timedelta(seconds=float(rng.uniform(20, 45))), 'dev': d,
                                       'feeder': recv, 'ev': 'LOCKOUT', 'amps': None, 'src': 'PROT'})
                        kind = devs[d]['kind']
                        own = cust(recv, 3, hh) + (cust(recv, 2, hh) if kind == 'R1' else 0)
                        S['harm'] = own
                        S['harm_kind'] = 'overload'
                        S['harm_dev'] = d
                        S['harm_t'] = lo_t
                        S['reinterrupted'] = S['restored']
                        sw = remote_minutes(hh) + float(rng.uniform(2, 9))
                        events.append({'t': lo_t + dt.timedelta(minutes=sw - 1.2), 'dev': tie_of(NET, lid), 'feeder': lid,
                                       'ev': 'OPEN', 'amps': None, 'src': 'SCADA OPERATOR'})
                        events.append({'t': lo_t + dt.timedelta(minutes=sw), 'dev': d, 'feeder': recv,
                                       'ev': 'CLOSE', 'amps': None, 'src': 'SCADA OPERATOR'})
                        S['t_rtn_actual'] = lo_t + dt.timedelta(minutes=sw - 1.2)
                        oms.append({'id': oms_id(lo_t), 'feeder': recv, 'device': d, 'sec': 3 if kind == 'R2' else 2,
                                    'start': lo_t, 'true_start': lo_t, 'cust': own + S['restored'],
                                    'steps': [(sw, own, 'remote', None),
                                              (max(sw + 5, (t_rep - lo_t).total_seconds() / 60.0), S['restored'],
                                               'repair', None)],
                                    'cause': 'overload', 'kind': 'recv_trip', 'storm': storm_load(hh), 'seq': None,
                                    'link': rec['id']})
                        break
        if S.get('t_rtn') is not None:
            if S.get('harm_kind') != 'overload':
                events.append({'t': S['t_rtn'], 'dev': tie_of(NET, lid), 'feeder': lid, 'ev': 'OPEN', 'amps': None,
                               'src': 'SCADA OPERATOR'})
            events.append({'t': S['t_rtn'] + dt.timedelta(seconds=float(rng.uniform(20, 140))), 'dev': S['iso_dev'],
                           'feeder': f, 'ev': 'CLOSE', 'amps': None, 'src': 'SCADA OPERATOR'})
        if S.get('harm_kind') == 'close onto fault':
            sw = remote_minutes(h) + float(rng.uniform(2, 9))
            oms.append({'id': oms_id(S['harm_t']), 'feeder': other, 'device': S['harm_dev'], 'sec': 3,
                        'start': S['harm_t'], 'true_start': S['harm_t'], 'cust': S['harm'],
                        'steps': [(sw, S['harm'], 'remote', None)], 'cause': 'fault on transferred section',
                        'kind': 'recv_trip', 'storm': storm_load(h), 'seq': None, 'link': rec['id']})
    return {'perm_h': perm_h, 'selftests': selftests, 'NET': NET, 'W': W, 'L': L, 'BAT': BAT, 'down': down, 'sky': sky, 'faults': faults, 'events': events,
            'oms': oms, 'seqs': seqs, 'windows': windows, 'batt_fail': batt_fail, 'manual': manual_transfers,
            'disarm_log': disarm_log, 'trips_h': trips_h, 'rtn': rtn_events}


def directions(NET):
    """every transfer direction: the loop, the feeder whose downstream sections move, and the receiving feeder"""
    out = []
    for Lp in NET['loops']:
        for a, b in ((Lp['a'], Lp['b']), (Lp['b'], Lp['a'])):
            r1, r2 = dev_of(NET, b, 'R1'), dev_of(NET, b, 'R2')
            conf = NET['devices'][r1]['ctl'] == 'CTL-6' and NET['devices'][r2]['ctl'] == 'CTL-6'
            out.append({'loop': Lp['loop'], 'from': a, 'to': b, 'configured': conf, 'r1': r1, 'r2': r2})
    return out


def summer_trip_risk(w, extra=None, pk=1.05):
    """for each unswitched direction, the chance a summer transfer trips a receiving recloser, replayed over the
    record's summer main-line lockout times and repair durations on the 2025-26 summer loads (truth side)"""
    NET, L, W = w['NET'], w['L'], w['W']
    devs = NET['devices']
    extra = extra or {}
    loc = W['local']
    yrs = np.array([t.year for t in loc])
    mon = np.array([t.month for t in loc])
    summer = (mon >= 6) & (mon <= 9)
    fault_h = [s['h'] for s in w['seqs'] if summer[s['h']]]
    reps = [st[0] for r in w['oms'] if r['kind'] == 'main' for st in r['steps'] if st[2] == 'repair']
    rng = np.random.default_rng(5)
    reps = rng.choice(reps, size=len(fault_h))
    out = {}
    for d in directions(NET):
        if d['configured']:
            continue
        a, b = d['from'], d['to']
        res = {}
        for typ, xs in (('S1', (2, 3)), ('S2', (3,))):
            n = 0
            trips = 0
            for h_f, rep in zip(fault_h, reps):
                for yy in (2025, 2026):
                    lt = loc[h_f]
                    try:
                        tgt = lt.replace(year=yy)
                    except ValueError:
                        continue
                    hh = C.hour_index(tgt.replace(tzinfo=C.TZ).astimezone(dt.timezone.utc))
                    if hh + int(rep / 60) + 2 >= W['H']:
                        continue
                    n += 1
                    trip = False
                    for k in range(hh, hh + int(rep / 60) + 1):
                        xa = sum(L['amps'][(a, s)][k] for s in xs)
                        c2 = L['amps'][(b, 3)][k] + xa + extra.get((b, 3), 0.0)
                        c1 = L['amps'][(b, 2)][k] + c2 + extra.get((b, 2), 0.0)
                        if c2 * pk > devs[d['r2']]['pickup1'] or c1 * pk > devs[d['r1']]['pickup1']:
                            trip = True
                            break
                    trips += trip
            res[typ] = trips / max(1, n)
        out[(d['loop'], a, b)] = res
    return out
