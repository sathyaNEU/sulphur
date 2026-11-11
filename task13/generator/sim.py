"""The whole world in one call: network, zones and their equipment, defects and cyclic inspections, thunderstorms and
the lightning network's records, every fault and its protection sequence, the device clocks and memories, the outage
management system's records, transformer burnouts and the stores' replacements, and a substation rain gauge."""
import numpy as np
import pandas as pd

import common as C
import faults as FA
import geo as GEO
import logs as LG
import net as NET
import others as OT
import phys as PH
import storms as ST
import world as W

REMARKS = {
    'lightning': ['Patrolled, no fault found. Energized.', 'Tripped during thunderstorm, line patrolled, energized.',
                  'Flashed-over insulator cleaned.', 'Burnt jumper replaced.', 'No fault found, energized.'],
    'lightning_cracked': ['Busted pin insulator replaced.', 'Cracked pin insulator replaced at pole.',
                          'Punctured pin insulator replaced.'],
    'arrester': ['Busted LA removed, line energized.', 'Blown LA replaced.', 'LA failed, disconnected and replaced.'],
    'storm_wind': ['Bamboo on line, cleared.', 'Coconut frond on line, removed.', 'Branch on conductor, cleared.'],
    'typhoon': ['Typhoon: tree on line.', 'Typhoon: broken pole.', 'Typhoon: conductor down.', 'Typhoon: debris on line.'],
    'animal': ['Snake on cutout.', 'Bird contact at transformer.', 'Rat on bushing.', 'Bird nest on crossarm.'],
    'vegetation': ['Bamboo contact.', 'Tree branch on line.', 'Banana leaves on line.'],
    'equipment': ['Burnt connector replaced.', 'Broken crossarm replaced.', 'Defective cutout replaced.',
                  'Broken tie wire.'],
    'third_party': ['Vehicle hit pole.', 'Kite string on line.', 'Crane contact.'],
    'unknown': ['No fault found, energized.', 'Patrolled, nothing found.'],
}
CODE = {'lightning': 'LIGHTNING', 'arrester': 'EQUIPMENT', 'storm_wind': 'WEATHER', 'typhoon': 'TYPHOON',
        'animal': 'ANIMAL', 'vegetation': 'VEGETATION', 'equipment': 'EQUIPMENT', 'third_party': 'THIRD PARTY',
        'unknown': 'UNKNOWN'}


def burnouts(N, Z, Stt, St, rng):
    """distribution transformers burnt by nearby strikes: rare behind a grounded, working arrester, common behind a
    stolen ground lead or a failed arrester"""
    S = N['S']
    c = PH.contacts(St)
    idx = GEO.SegIndex(S, 1.0)
    p, s, d = idx.near(c.x.values, c.y.values, 0.12)
    P = pd.DataFrame({'ci': p, 'seg': s, 'd': d})
    P['zone_ix'] = S.zone_ix.values[s]
    P = P.sort_values('d').drop_duplicates(['ci', 'zone_ix'])
    P['t'] = c.t.values[P.ci.values]
    P['I'] = np.abs(c.I.values[P.ci.values])
    st = FA.state_at(Stt, P.zone_ix.values, P.t.values)
    g, a = st[:, 0], st[:, 1]
    txd = S.tx_per_km.values[P.seg.values]
    pr = 0.0075 * np.minimum(1.0, txd * 0.35) * (P.I.values / 30.0) ** 0.5 * (1 + 7.0 * (1 - g)) * (1 + 3.5 * (1 - a))
    hit = rng.random(len(P)) < pr
    B = P[hit][['zone_ix', 't']].copy()
    B['reason'] = 'lightning'
    # burnouts with no lightning: overload, age, oil
    rows = []
    days = (W.T1 - W.T0).days
    for z in Z.itertuples():
        n = rng.poisson(0.012 * z.n_tx * days / 365.25)
        for t in W.T0 + pd.to_timedelta(rng.uniform(0, days, n), unit='D'):
            rows.append((z.zone_ix, t, rng.choice(['overload', 'age', 'oil'], p=[0.45, 0.35, 0.2])))
    B2 = pd.DataFrame(rows, columns=['zone_ix', 't', 'reason'])
    B = pd.concat([B, B2], ignore_index=True)
    B = B[(B.t >= W.T0) & (B.t < W.T1)].sort_values('t').reset_index(drop=True)
    return B


def oms(Z, locks, kept, down, B, rng):
    """the outage management system: every lockout and every burnt transformer, with the dispatcher's cause code,
    the crew's remark and the consumers the outage reached"""
    zz = Z.set_index('zone_ix')
    members_down = {z: int(sum(zz.members[d] for d in down[z])) for z in zz.index}
    rows = []
    for l in locks.itertuples():
        f = kept.loc[l.fault_ix]
        cause = f.cause
        tele = zz.telemetry[l.zone_ix]
        start = l.t_lock if tele == 'SCADA' else l.t_lock + pd.Timedelta(minutes=float(rng.lognormal(np.log(14), 0.6)))
        start = start.floor('min')
        restored = l.t_restore.floor('min')
        if cause == 'lightning':
            rem = rng.choice(REMARKS['lightning_cracked']) if (f.on_cracked and rng.random() < 0.72) else rng.choice(REMARKS['lightning'])
            code = 'LIGHTNING' if rng.random() < 0.58 else rng.choice(['WEATHER', 'UNKNOWN'], p=[0.55, 0.45])
            if 'insulator' in rem and rng.random() < 0.5:
                code = 'EQUIPMENT'
            wx = 'Thunderstorm' if rng.random() < 0.8 else 'Rain'
        elif cause == 'arrester':
            rem = rng.choice(REMARKS['arrester']) if rng.random() < 0.78 else rng.choice(REMARKS['unknown'])
            code = 'EQUIPMENT' if 'LA' in rem else 'UNKNOWN'
            wx = rng.choice(['Fair', 'Rain', 'Cloudy'], p=[0.45, 0.35, 0.2])
        elif cause == 'typhoon':
            rem = rng.choice(REMARKS['typhoon'])
            code = 'TYPHOON'
            wx = 'Typhoon'
        else:
            rem = rng.choice(REMARKS[cause])
            code = CODE[cause] if rng.random() < 0.85 else 'UNKNOWN'
            wx = ('Thunderstorm' if rng.random() < 0.6 else 'Rain') if cause == 'storm_wind' else \
                rng.choice(['Fair', 'Cloudy', 'Rain'], p=[0.6, 0.25, 0.15])
        rows.append(dict(zone_ix=l.zone_ix, kind='device', start=start, restored=restored, consumers=members_down[l.zone_ix],
                         code=code, remarks=rem, weather=wx))
    for b in B.itertuples():
        start = (b.t + pd.Timedelta(minutes=float(rng.lognormal(np.log(25), 0.7)))).floor('min')
        hrs = rng.lognormal(np.log(30), 0.5)
        if b.reason == 'lightning':
            code = 'LIGHTNING' if rng.random() < 0.55 else 'EQUIPMENT'
            rem = rng.choice(['Burnt DT replaced.', 'DT burnt after thunderstorm, replaced.', 'Burnt transformer replaced.'])
            wx = 'Thunderstorm' if rng.random() < 0.7 else 'Rain'
        else:
            code = 'EQUIPMENT'
            rem = rng.choice(['Burnt DT replaced.', 'Overloaded DT replaced.', 'Leaking DT replaced.'])
            wx = rng.choice(['Fair', 'Cloudy', 'Rain'], p=[0.6, 0.25, 0.15])
        rows.append(dict(zone_ix=b.zone_ix, kind='transformer', start=start, restored=(start + pd.Timedelta(hours=float(hrs))).floor('min'),
                         consumers=int(rng.integers(9, 46)), code=code, remarks=rem, weather=wx))
    O = pd.DataFrame(rows).sort_values('start').reset_index(drop=True)
    return O


def raingauge(N, Fl, rng):
    """daily rain at three substations, wetter on storm days near them (a distractor: nothing reads it)"""
    days = pd.date_range('2022-01-01', '2026-10-31', freq='D')
    subs = N['subs'][[0, 4, 9]]
    out = []
    fl = Fl.copy()
    fl['day'] = fl.t.dt.normalize()
    for k, (sx, sy) in enumerate(subs):
        near = fl[np.hypot(fl.x - sx, fl.y - sy) < 12].groupby('day').size()
        for d in days:
            wet_base = 0.28 if d.month in (6, 7, 8, 9) else (0.12 if d.month in (4, 5, 10, 11) else 0.04)
            n = near.get(d, 0)
            p = min(0.95, wet_base + 0.02 * n)
            mm = rng.gamma(0.8, 9 + 0.6 * min(n, 60)) if rng.random() < p else 0.0
            out.append((d, k, round(mm, 1)))
    return pd.DataFrame(out, columns=['day', 'gauge', 'mm'])


def simulate():
    rng = np.random.default_rng(C.SEED)
    N = NET.build(C.SEED)
    S = N['S']
    Z = W.zones(N, rng)
    I = W.inspection_plan(N, Z, rng)
    E = W.defects(Z, I, rng)
    Stt, Fi = W.state_timeline(Z, I, E, rng)
    Cc, Fl, St = ST.simulate(N, C.STORM_SEED, start='2016-11-01', annual=40000)
    P = PH.pairs(N, St, 0.6)
    F, P2 = FA.lightning_faults(N, Z, P, Stt, rng)
    wind = OT.storm_wind(N, Z, Fl, rng)
    ty = OT.typhoon(Z, rng)
    bg = OT.background(Z, W.T0, W.T1, rng)
    la = OT.arrester_faults(E[(E.t >= W.T0)], rng)
    allf = pd.concat([F[['zone_ix', 't', 'cause', 'on_cracked', 'flash', 'stroke']], wind, ty[['zone_ix', 't', 'cause']],
                      bg, la], ignore_index=True)
    allf['on_cracked'] = allf.on_cracked.fillna(False).astype(bool)
    allf = allf[(allf.t >= W.T0) & (allf.t < W.T1)].reset_index(drop=True)
    ops, locks, kept, down = LG.sequences(Z, allf, rng, W.T1)
    rt = LG.routine_events(Z, W.T0, W.T1, rng)
    V = LG.visits(Z, rng)
    Ev = LG.device_events(Z, ops, rt, locks, down, V, rng, W.T0, W.T1)
    Ev = LG.stamp(Z, Ev, V, rng)
    D = LG.downloads(Z, Ev, V)
    R = ST.detect(St, Fl, C.STORM_SEED + 1)
    B = burnouts(N, Z, Stt, St, rng)
    O = oms(Z, locks, kept, down, B, rng)
    rain = raingauge(N, Fl, np.random.default_rng(C.SEED + 77))
    return dict(N=N, S=S, Z=Z, I=I, E=E, Stt=Stt, Fi=Fi, Fl=Fl, St=St, P2=P2, F=F, allf=allf, ops=ops, locks=locks,
                kept=kept, down=down, V=V, Ev=Ev, D=D, R=R, B=B, O=O, rain=rain)
