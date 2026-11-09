"""The pack's text exports, each in the form its system writes it: the outage management system's interruption
export, the weather service's hourly records and station register, the protection device register and the
ICP registry's monthly counts. The office files (feeder register, cycle log, standard, programme terms and the
two others) are written by docs.py.

Every irregularity here is one the producing system makes on its own: the call centre and the field crew both
logging one device operation, planned work in the same register, a cause-coding change on 1 October 2023, local
times with no offset, feeders renamed at the Rangiora Street rebuild, a station reporting gusts in knots before
its anemometer was replaced, and the gaps an automatic station leaves when its logger fails."""
import csv
import datetime as dt

import numpy as np
import pandas as pd

import common as C
import world as W

OMS0 = pd.Timestamp(W.OMS_START)
OMS1 = pd.Timestamp('2026-10-31 23:59')
RECODE = pd.Timestamp('2023-10-01')          # the OMS cause scheme changed on this date
RNG_REBUILD = pd.Timestamp('2023-08-14')     # Rangiora Street zone substation recommissioned, feeders renamed
OLD_CODES = {'VEG': 'tree', 'EQP': 'equipment', 'ANI': 'animal', 'VEH': 'vehicle', 'UNK': 'unknown',
             'WTH': 'wind', 'LGT': 'lightning', 'PLN': 'planned'}
NEW_CODES = {'TREE': 'tree', 'EQUIP': 'equipment', 'ANIMAL': 'animal', 'THIRD-PARTY': 'vehicle',
             'UNKNOWN': 'unknown', 'WEATHER': 'wind', 'LIGHTNING': 'lightning', 'PLANNED': 'planned'}
CODE_OLD = {v: k for k, v in OLD_CODES.items()}
CODE_NEW = {v: k for k, v in NEW_CODES.items()}
DEVTYPE = {'Circuit breaker': 'CB', 'Recloser': 'ACR', 'Fuse': 'FUSE'}
REMARKS = {
    'tree': ['Tree contact, line patrolled', 'Branch on conductor, removed', 'Tree through line, crew cut clear',
             'Vegetation contact', 'Tree down across line', ''],
    'equipment': ['Insulator failure', 'Crossarm failure', 'Connector failure', 'Transformer fault', 'Cable joint failure', ''],
    'animal': ['Possum on transformer', 'Bird contact', 'Possum', ''],
    'vehicle': ['Vehicle versus pole', 'Digger contact', 'Truck snagged line', ''],
    'unknown': ['Patrolled, no cause found', 'Fuse replaced, nothing found', ''],
    'wind': ['Clashing conductors in wind', 'Debris on line', 'Roofing iron on line', ''],
    'lightning': ['Lightning strike', 'Surge arrester failure after lightning', ''],
    'planned': ['Planned outage: pole replacement', 'Planned outage: transformer change', 'Planned outage: line rebuild',
                'Planned outage: recloser installation', 'Planned outage: conductor replacement'],
}


def old_feeder_code(code):
    """Rangiora Street's feeders before the rebuild: RGS1, RGS2, ..."""
    if code.startswith('RNG-'):
        return 'RGS%d' % int(code.split('-')[1])
    return code


def code_at(code, t):
    return old_feeder_code(code) if (code.startswith('RNG-') and t < RNG_REBUILD) else code


def device_at(dev, feeder, t):
    return dev.replace(feeder, code_at(feeder, t), 1)


def fmt(t):
    return t.strftime('%Y-%m-%d %H:%M')


def write_oms(S, E, path):
    rng = np.random.default_rng(W.SEED + 501)
    D = S['D']
    rec = E[(E['start'] >= OMS0) & (E['start'] <= OMS1)].sort_values(['start', 'feeder', 'device_id']).reset_index(drop=True)
    reclosers = D[D['device_type'] == 'Recloser'].groupby('feeder')['device_id'].apply(list).to_dict()
    cbs = D[D['device_type'] == 'Circuit breaker'].set_index('feeder')['device_id'].to_dict()
    share = D.set_index('device_id')['share'].to_dict()
    cust_year = {y: dict(zip(S['F']['feeder'], W.customers_at(S['F'], y))) for y in range(2021, 2027)}
    rows = []
    for k, r in rec.iterrows():
        t = r['start']
        cause = r['cause']
        dev, dtype, cust, minutes = r['device_id'], r['device_type'], int(r['customers']), float(r['minutes'])
        if not r['sustained']:
            # a transient fault cleared by a reclose: the recloser (or the breaker) operated and restored supply
            opts = reclosers.get(r['feeder'], [])
            dev = opts[int(rng.integers(0, len(opts)))] if (opts and rng.random() < 0.85) else cbs[r['feeder']]
            dtype = 'Recloser' if dev in opts else 'Circuit breaker'
            cust = int(round(cust_year[t.year][r['feeder']] * share[dev]))
        source = 'Planned works' if cause == 'planned' else ('SCADA' if dtype != 'Fuse' else 'Field crew')
        code = (CODE_OLD if t < RECODE else CODE_NEW)[cause]
        rem = REMARKS[cause][int(rng.integers(0, len(REMARKS[cause])))] if rng.random() < 0.55 else ''
        restore = t + pd.Timedelta(seconds=round(minutes * 60))
        rows.append(dict(t=t, source=source, feeder=code_at(r['feeder'], t), device=device_at(dev, r['feeder'], t),
                         device_type=DEVTYPE[dtype], start=fmt(t), restore=fmt(restore),
                         minutes='%.1f' % minutes if minutes >= 1 else '%.2f' % minutes, customers=cust,
                         klass='Planned' if cause == 'planned' else 'Unplanned', cause=code, remarks=rem))
        # the call centre logs some of the same operations from customers' calls
        if r['sustained'] and cause != 'planned' and rng.random() < 0.07:
            lag = pd.Timedelta(minutes=int(rng.integers(3, 26)))
            t2 = t + lag
            m2 = max(1.0, minutes - lag.total_seconds() / 60 + float(rng.normal(0, 6)))
            cc = 'Trees' if cause == 'tree' else ('Power off' if rng.random() < 0.6 else 'Unknown')
            rows.append(dict(t=t2, source='Call centre', feeder=code_at(r['feeder'], t), device=device_at(dev, r['feeder'], t),
                             device_type=DEVTYPE[dtype], start=fmt(t2), restore=fmt(t2 + pd.Timedelta(minutes=m2)),
                             minutes='%.1f' % m2, customers=int(max(1, round(cust, -1) if cust >= 10 else cust)),
                             klass='Unplanned', cause=cc, remarks='Customer calls'))
    rows.sort(key=lambda d: (d['t'], d['feeder'], d['device'], d['source']))
    seq = {}
    with open(path, 'w', newline='') as fh:
        w = csv.writer(fh, lineterminator='\r\n')
        w.writerow(['event_no', 'source', 'feeder', 'protection_ref', 'protection_type', 'start_time', 'restored_time',
                    'duration_min', 'customers_interrupted', 'interruption_class', 'cause_code', 'remarks'])
        for d in rows:
            ym = d['t'].strftime('%y%m')
            seq[ym] = seq.get(ym, 0) + 1
            w.writerow(['K%s-%05d' % (ym, seq[ym]), d['source'], d['feeder'], d['device'], d['device_type'], d['start'],
                        d['restore'], d['minutes'], d['customers'], d['klass'], d['cause'], d['remarks']])
    return len(rows)


# ------------------------------------------------------------------ weather
GAPS = {
    # station: (local start, hours) logger failures; none inside the outage record
    'PBA': [('2008-07-11 14:00', 52), ('2013-02-02 03:00', 19), ('2019-09-24 10:00', 31)],
    'MTF': [('2010-05-30 22:00', 140), ('2017-12-08 06:00', 12)],
    'KWR': [('2009-08-14 01:00', 75), ('2015-03-19 17:00', 26), ('2020-11-02 09:00', 44)],
    'TSD': [('2007-06-21 12:00', 210), ('2012-01-30 05:00', 33), ('2018-08-07 20:00', 18)],
}
KNOTS_UNTIL = {'TSD': pd.Timestamp('2013-07-01')}     # Titi Saddle's anemometer was replaced on 1 July 2013


def utc_hours():
    a = pd.Timestamp(W.START).tz_localize(C.ZONE).tz_convert('UTC')
    b = pd.Timestamp(W.END).tz_localize(C.ZONE, ambiguous=False).tz_convert('UTC')
    return pd.date_range(a, b, freq='h')


def write_weather(S, sid, path):
    s = C.STATION_IDS.index(sid)
    rng = np.random.default_rng(W.SEED + 600 + s)
    hu = utc_hours()
    loc = hu.tz_convert(C.ZONE).tz_localize(None)
    idx = np.searchsorted(S['hours_w'].values, loc.values)
    gust = S['W_all'][idx, s]
    n = len(hu)
    factor = 1.48 + 0.22 * rng.random(n)
    mean = gust / factor * np.exp(rng.normal(0, 0.05, n))
    # wind direction: a slowly turning flow, westerly in strong winds
    dirn = (np.cumsum(rng.normal(0, 9, n)) + 250) % 360
    strong = gust >= 50
    dirn[strong] = (230 + 35 * rng.normal(0, 1, strong.sum())) % 360
    qc = np.array(['G'] * n, dtype=object)
    missing = np.zeros(n, bool)
    for a, h in GAPS[sid]:
        i0 = int(np.searchsorted(loc.values, np.datetime64(pd.Timestamp(a))))
        missing[i0:i0 + h] = True
    qc[missing] = 'M'
    # a handful of anemometer spikes the service flags as suspect
    pre = np.where((loc < OMS0) & ~missing)[0]
    spikes = rng.choice(pre, 4, replace=False)
    gust = gust.copy()
    gust[spikes] = gust[spikes] + rng.uniform(70, 110, 4)
    qc[spikes] = 'S'
    knots = loc < KNOTS_UNTIL.get(sid, pd.Timestamp('1900-01-01'))
    stamp = hu.strftime('%Y-%m-%dT%H:%MZ')
    with open(path, 'w', newline='') as fh:
        w = csv.writer(fh, lineterminator='\n')
        w.writerow(['station_id', 'obs_time_utc', 'wind_mean', 'gust_max', 'wind_dir_deg', 'wind_unit', 'qc'])
        for i in range(n):
            if missing[i]:
                w.writerow([sid, stamp[i], '', '', '', 'kt' if knots[i] else 'km/h', 'M'])
                continue
            if knots[i]:
                w.writerow([sid, stamp[i], '%d' % round(mean[i] / 1.852), '%d' % round(gust[i] / 1.852),
                            '%d' % (round(dirn[i] / 10) * 10 % 360), 'kt', qc[i]])
            else:
                w.writerow([sid, stamp[i], '%.1f' % mean[i], '%.1f' % gust[i], '%d' % (round(dirn[i]) % 360), 'km/h', qc[i]])
    return n


def write_stations(path):
    notes = {'PBA': 'Coastal site on the Paua Bay headland.',
             'MTF': 'Open farmland, Mataroa Flats aerodrome.',
             'KWR': 'Ridge-top site above the Kowhai valley.',
             'TSD': 'Saddle site on the Titi range road. Anemometer replaced 1 July 2013; gusts and mean wind were '
                    'reported in knots before then.'}
    opened = {'PBA': '1998-04-01', 'MTF': '2003-10-15', 'KWR': '2005-02-01', 'TSD': '2005-11-20'}
    with open(path, 'w', newline='') as fh:
        w = csv.writer(fh, lineterminator='\n')
        w.writerow(['station_id', 'station_name', 'latitude', 'longitude', 'elevation_m', 'anemometer_height_m',
                    'opened', 'operator', 'notes'])
        for st in W.STATIONS:
            w.writerow([st[0], st[1], '%.3f' % st[2], '%.3f' % st[3], st[4], st[5], opened[st[0]], C.WEATHER, notes[st[0]]])
    return len(W.STATIONS)


# ------------------------------------------------------------------ registers
def write_devices(S, path):
    F, D = S['F'], S['D']
    rng = np.random.default_rng(W.SEED + 700)
    cust = dict(zip(F['feeder'], W.customers_at(F, 2026)))
    year = dict(zip(F['feeder'], F['age']))
    rows = []
    for _, d in D.sort_values(['feeder', 'device_id']).iterrows():
        icp = int(round(cust[d['feeder']] * d['share']))
        inst = int(year[d['feeder']]) if d['device_type'] == 'Circuit breaker' else int(rng.integers(max(1995, year[d['feeder']]), 2025))
        rows.append([d['device_id'], d['feeder'], DEVTYPE[d['device_type']], icp, inst,
                     'Y' if d['device_type'] != 'Fuse' else 'N'])
    with open(path, 'w', newline='') as fh:
        w = csv.writer(fh, lineterminator='\r\n')
        w.writerow(['protection_ref', 'feeder', 'protection_type', 'icps_downstream', 'installed', 'scada'])
        w.writerows(rows)
    return len(rows)


def icp_months():
    return pd.period_range('2022-04', '2026-10', freq='M')


def icp_count(S, feeder, period, rng_val):
    F = S['F']
    j = int(np.where(F['feeder'] == feeder)[0][0])
    c0 = F['cust0'].iloc[j]
    yrs = (period.year + (period.month - 0.5) / 12.0) - 2026.83
    return int(round(c0 * (1 + 0.011 * yrs) * (1 + rng_val)))


def write_icps(S, path):
    rng = np.random.default_rng(W.SEED + 710)
    F = S['F']
    rows = []
    for p in icp_months():
        for f in sorted(F['feeder']):
            rows.append([p.strftime('%Y-%m'), f, icp_count(S, f, p, float(rng.normal(0, 0.002)))])
    with open(path, 'w', newline='') as fh:
        w = csv.writer(fh, lineterminator='\n')
        w.writerow(['month_end', 'feeder', 'icps_connected'])
        w.writerows(rows)
    latest = {f: n for m, f, n in rows if m == icp_months()[-1].strftime('%Y-%m')}
    return len(rows), latest
