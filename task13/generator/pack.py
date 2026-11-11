"""The pack's text exports, each in the form its system writes it: the lightning data provider's stroke extract (UTC),
the SCADA historian's event history (Philippine time, millisecond stamps from each device), the compiled event
downloads from the reclosers with no radio link (each controller's own clock and format, re-read memories repeating
across downloads), the outage management system's export, the line routes and a substation rain gauge.

Every irregularity is one the producing system makes on its own: a lightning network's cloud pulses and weak positive
discharges among its ground strokes, a fault logged as a trip and its recloses, a breaker tripping with a downstream
recloser, controllers that keep their own time between site visits and only their last events, outage times taken
from the first consumer call where the device has no radio link, dispatchers' cause codes."""
import json

import numpy as np
import pandas as pd

import common as C
import geo as GEO

SC_EVENT = {'TRIP': 'TRIP', 'RECLOSE': 'RECLOSE', 'LOCKOUT': 'LOCKOUT', 'CLOSE': 'CLOSE', 'MANUAL OPEN': 'OPEN',
            'MANUAL CLOSE': 'CLOSE', 'HOT LINE TAG ON': 'HLT ON', 'HOT LINE TAG OFF': 'HLT OFF'}
DL_EVENT = {'TRIP': 'Trip', 'RECLOSE': 'Reclose', 'LOCKOUT': 'Lockout', 'CLOSE': 'Close', 'MANUAL OPEN': 'Open',
            'MANUAL CLOSE': 'Close', 'HOT LINE TAG ON': 'HLT On', 'HOT LINE TAG OFF': 'HLT Off',
            'AC SUPPLY OFF': 'AC Supply Off', 'AC SUPPLY ON': 'AC Supply On', 'BATTERY TEST': 'Battery Test',
            'DOOR OPEN': 'Door Open', 'EVENT LOG READ': 'Event Log Read', 'CLOCK SET': 'Clock Set'}


def write_strokes(w, path, rmax=0.4):
    """the provider's extract: every ground stroke and cloud pulse it located within 400 m of a line, in UTC"""
    R = w['R']
    R = R[R.rt >= pd.Timestamp('2016-11-01')]
    idx = GEO.SegIndex(w['S'], 1.0)
    p, s, d = idx.near(R.rx.values, R.ry.values, rmax)
    keep = np.unique(p)
    R = R.iloc[keep].sort_values('rt').reset_index(drop=True)
    lat, lon = C.to_latlon(R.rx.values, R.ry.values)
    utc = R.rt - pd.Timedelta(hours=8)
    rng = np.random.default_rng(C.SEED + 401)
    out = pd.DataFrame({
        'datetime_utc': utc.dt.strftime('%Y-%m-%dT%H:%M:%S.%f') + 'Z',
        'latitude': np.round(lat, 5), 'longitude': np.round(lon, 5),
        'peak_current_ka': R.rI.values, 'type': R.type.values, 'sensors': R.sensors.values,
        'semi_major_km': R.major.values, 'semi_minor_km': R.minor.values, 'azimuth_deg': R.azim.values.astype(int),
        'chi_sq': np.round(rng.gamma(2.2, 0.55, len(R)), 1)})
    out.to_csv(path, index=False, lineterminator='\r\n')
    return len(out)


def _ms(t):
    return t.dt.strftime('%Y-%m-%d %H:%M:%S.%f').str[:-3]


def write_scada(w, path):
    """the historian's event history for the breakers and the radio-linked reclosers, each stamped by its device"""
    Z = w['Z'].set_index('zone_ix')
    Ev = w['Ev']
    E = Ev[Ev.zone_ix.map(Z.telemetry).eq('SCADA') & Ev.event.isin(list(SC_EVENT))].copy()
    E = E[(E.ts >= pd.Timestamp('2016-12-01')) & (E.ts < pd.Timestamp('2026-11-01'))]
    rng = np.random.default_rng(C.SEED + 402)
    # radio links drop now and then: the historian logs the alarm and the return
    al = []
    for z in Z.index[(Z.telemetry == 'SCADA') & (Z.controller != 'relay')]:
        n = rng.poisson(18)
        for t in pd.Timestamp('2016-12-01') + pd.to_timedelta(rng.uniform(0, 3622, n), unit='D'):
            al.append((z, t, 'COMMS FAIL'))
            al.append((z, t + pd.Timedelta(minutes=float(rng.lognormal(np.log(40), 0.9))), 'COMMS RESTORED'))
    A = pd.DataFrame(al, columns=['zone_ix', 'ts', 'event'])
    E = pd.concat([E[['zone_ix', 'ts', 'event', 'phase', 'amps']], A], ignore_index=True)
    E = E.sort_values(['ts', 'zone_ix']).reset_index(drop=True)
    kind = Z.controller
    pt = [Z.zone[z] + (' CB' if kind[z] == 'relay' else ' ACR') for z in E.zone_ix]
    out = pd.DataFrame({'timestamp': _ms(E.ts), 'point': pt, 'event': [SC_EVENT.get(e, e) for e in E.event],
                        'phase': E.phase.fillna(''), 'fault_current_a': E.amps.fillna(0).astype(int).replace(0, '')})
    out['fault_current_a'] = [('' if (e not in ('TRIP',)) else str(int(a))) for e, a in zip(out.event, E.amps.fillna(0))]
    out.to_csv(path, index=False, lineterminator='\r\n')
    return len(out)


def write_downloads(w, path):
    """every read of a radio-less recloser's event memory, in the order the technicians filed them: the controller's
    own clock and date format, each memory read whole, so events read twice appear twice"""
    Z = w['Z'].set_index('zone_ix')
    D = w['D'].copy()
    D = D[D.event.isin(list(DL_EVENT))]
    vt = D.visit_t
    dl_ids = {}
    for k, (z, v) in enumerate(D[['zone_ix', 'visit_t']].drop_duplicates().sort_values('visit_t').itertuples(index=False)):
        dl_ids[(z, v)] = 'DL%02d-%04d' % (v.year % 100, k + 101)
    out = pd.DataFrame({
        'download': [dl_ids[(z, v)] for z, v in zip(D.zone_ix, vt)],
        'recloser': D.zone_ix.map(Z.zone).values,
        'read_at': vt.dt.strftime('%Y-%m-%d %H:%M').values,
        'event_no': D.seq.values,
        'controller_time': D.ts.dt.strftime('%d/%m/%Y %H:%M:%S.%f').str[:-4].values,
        'event': D.event.map(DL_EVENT).values,
        'phase': D.phase.fillna('').values,
        'current_a': [('' if e != 'TRIP' else str(int(a))) for e, a in zip(D.event, D.amps.fillna(0))]})
    out = out.sort_values(['read_at', 'recloser', 'event_no']).reset_index(drop=True)
    out.to_csv(path, index=False, lineterminator='\r\n')
    return len(out)


def write_oms(w, path):
    Z = w['Z'].set_index('zone_ix')
    O = w['O'].copy()
    rng = np.random.default_rng(C.SEED + 403)
    crews = ['Line Crew %s' % c for c in 'ABCDEFG']
    tx_no = []
    for k in O.kind:
        tx_no.append('DT-%05d' % rng.integers(10000, 99999) if k == 'transformer' else '')
    out = pd.DataFrame({
        'outage_no': ['%d-%05d' % (s.year, i + 1) for i, s in enumerate(O.start)],
        'feeder': O.zone_ix.map(Z.feeder).values,
        'equipment': [Z.zone[z] if k == 'device' else t for z, k, t in zip(O.zone_ix, O.kind, tx_no)],
        'equipment_type': np.where(O.kind == 'device', np.where(O.zone_ix.map(Z.controller).eq('relay'), 'Feeder breaker',
                                'Line recloser'), 'Distribution transformer'),
        'time_out': O.start.dt.strftime('%m/%d/%Y %H:%M').values,
        'time_restored': O.restored.dt.strftime('%m/%d/%Y %H:%M').values,
        'consumers_affected': O.consumers.values,
        'cause_code': O.code.values, 'weather': O.weather.values, 'remarks': O.remarks.values,
        'crew': rng.choice(crews, len(O))})
    # outage numbers run per year
    yr = O.start.dt.year
    out['outage_no'] = ['%d-%05d' % (y, k) for y, k in zip(yr, O.groupby(yr).cumcount() + 1)]
    out.to_csv(path, index=False, lineterminator='\r\n')
    return len(out)


def write_routes(w, path):
    """each zone's overhead line as line strings, one per run of one construction through one kind of area"""
    S = w['S']
    Z = w['Z'].set_index('zone_ix')
    feats = []
    area = {'open': 'open field', 'treed': 'tree-lined', 'town': 'town', 'hill': 'hill'}
    cons = {'wood_xarm': 'wood crossarm', 'steel_xarm': 'steel crossarm', 'bracket': 'pole-top bracket',
            'concrete_bracket': 'bracket on concrete pole'}
    S = S.copy()
    S['run'] = ((S.zone_ix != S.zone_ix.shift()) | (S.setting != S.setting.shift()) | (S.construction != S.construction.shift())
                | (np.hypot(S.x0 - S.x1.shift(), S.y0 - S.y1.shift()) > 1e-6)).cumsum()
    for r, g in S.groupby('run'):
        xs = list(g.x0) + [g.x1.iat[-1]]
        ys = list(g.y0) + [g.y1.iat[-1]]
        lat, lon = C.to_latlon(np.array(xs), np.array(ys))
        z = g.zone_ix.iat[0]
        feats.append({'type': 'Feature',
                      'properties': {'zone': Z.zone[z], 'feeder': Z.feeder[z], 'phases': int(g.phases.iat[0]),
                                     'construction': cons[g.construction.iat[0]], 'area': area[g.setting.iat[0]],
                                     'length_km': round(float(g.km.sum()), 3)},
                      'geometry': {'type': 'LineString', 'coordinates': [[round(a, 6), round(b, 6)] for a, b in zip(lon, lat)]}})
    gj = {'type': 'FeatureCollection', 'name': 'overhead_line_routes',
          'crs': {'type': 'name', 'properties': {'name': 'urn:ogc:def:crs:OGC:1.3:CRS84'}}, 'features': feats}
    with open(path, 'w') as f:
        json.dump(gj, f, separators=(',', ':'))
    return len(feats)


def write_raingauge(w, path):
    r = w['rain']
    names = [C.SUBSTATIONS[i][1] + ' S/S' for i in (0, 4, 9)]
    out = pd.DataFrame({'date': r.day.dt.strftime('%Y-%m-%d'), 'station': [names[g] for g in r.gauge],
                        'rain_mm': r.mm.values})
    out = out.sort_values(['station', 'date'])
    out.to_csv(path, index=False, lineterminator='\r\n')
    return len(out)
