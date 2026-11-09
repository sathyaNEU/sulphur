"""An independent recomputation of the golden from the cut pack: its own readers, its own cleaning, its own major
event days, its own Poisson fit (iteratively reweighted least squares in numpy) and its own projection. It shares
no code with golden.py and checks the six, every feeder's figures and the board note's totals against figures.json.

    python3 task13/generator/verify.py
"""
import csv
import datetime as dt
import json
import math
import os
import sys
import zipfile
from zoneinfo import ZoneInfo

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, 'target')
NZ = ZoneInfo('Pacific/Auckland')


def xlsx_rows(path, sheet_name):
    """a sheet's cell values from the workbook's XML (shared strings resolved), row by row"""
    import re
    z = zipfile.ZipFile(path)
    wb = z.read('xl/workbook.xml').decode()
    rels = z.read('xl/_rels/workbook.xml.rels').decode()
    sheets = re.findall(r'<sheet [^>]*name="([^"]+)"[^>]*r:id="([^"]+)"', wb)
    rid = dict(sheets)[sheet_name]
    target = re.search(r'Id="%s"[^>]*Target="([^"]+)"' % rid, rels) or re.search(r'Target="([^"]+)"[^>]*Id="%s"' % rid, rels)
    sx = z.read('xl/' + target.group(1).lstrip('/').replace('xl/', '')).decode()
    ss = []
    if 'xl/sharedStrings.xml' in z.namelist():
        for si in re.findall(r'<si>(.*?)</si>', z.read('xl/sharedStrings.xml').decode(), re.S):
            ss.append(''.join(re.findall(r'<t[^>]*>(.*?)</t>', si, re.S)).replace('&amp;', '&'))
    out = []
    for row in re.findall(r'<row [^>]*>(.*?)</row>', sx, re.S):
        cells = {}
        for ref, attrs, body in re.findall(r'<c r="([A-Z]+)\d+"([^>]*)>(.*?)</c>', row, re.S):
            v = re.search(r'<v>(.*?)</v>', body)
            if not v:
                continue
            val = v.group(1)
            if 't="s"' in attrs:
                val = ss[int(val)]
            cells[ref] = val
        if cells:
            width = max(ord(k[-1]) - 64 + 26 * (len(k) - 1) for k in cells)
            out.append([cells.get(chr(65 + j), None) for j in range(width)])
    return out


def excel_date(v):
    return dt.datetime(1899, 12, 30) + dt.timedelta(days=float(v))


def read_all():
    files = {}
    for root, dirs, fs in os.walk(T):
        for f in fs:
            files[f] = os.path.join(root, f)
    reg = xlsx_rows([p for f, p in files.items() if f.startswith('feeder_register')][0], 'Feeders')
    hdr = [i for i, r in enumerate(reg) if r and r[0] == 'Feeder'][0]
    feeders = {}
    for r in reg[hdr + 1:]:
        feeders[r[0]] = dict(former=r[1], zone=r[2], cycle=float(r[9]))
    zs = xlsx_rows([p for f, p in files.items() if f.startswith('feeder_register')][0], 'Zone substations')
    zh = [i for i, r in enumerate(zs) if r and r[0] == 'Code'][0]
    zone = {r[0]: (float(r[2]), float(r[3])) for r in zs[zh + 1:]}
    st = list(csv.DictReader(open([p for f, p in files.items() if 'station_register' in f][0])))
    cyc = xlsx_rows([p for f, p in files.items() if f.startswith('vegetation_cycle_log')][0], 'Cycle jobs')
    ch = [i for i, r in enumerate(cyc) if r and r[0] == 'Job'][0]
    trims = {}
    for r in cyc[ch + 1:]:
        trims.setdefault(r[1], []).append(excel_date(r[3]))
    for f in trims:
        trims[f].sort()
    icp = {}
    for r in csv.DictReader(open([p for f, p in files.items() if f.startswith('icp_counts')][0])):
        icp.setdefault(r['month_end'], 0)
        icp[r['month_end']] += int(r['icps_connected'])
    return files, feeders, zone, st, trims, icp


def boundaries(files):
    import re
    from docx import Document
    doc = Document([p for f, p in files.items() if f.startswith('reliability_reporting_standard')][0])
    out = {}
    for t in doc.tables:
        rows = [[c.text.strip() for c in r.cells] for r in t.rows]
        if rows[0][0] == 'Path':
            for r in rows[1:]:
                out[r[0]] = (float(r[2]), float(r[3]))
    return out


def ry(d):
    return d.year if d.month >= 4 else d.year - 1


def main():
    files, feeders, zone, st, trims, icp = read_all()
    former = {v['former']: k for k, v in feeders.items() if v['former']}
    B = boundaries(files)
    # the interruption record, one row per device operation
    rows = list(csv.DictReader(open([p for f, p in files.items() if f.startswith('oms_')][0])))
    logged = {}
    for r in rows:
        if r['source'] != 'Call centre':
            logged.setdefault(r['protection_ref'], []).append(dt.datetime.strptime(r['start_time'], '%Y-%m-%d %H:%M'))
    recs = []
    for r in rows:
        t = dt.datetime.strptime(r['start_time'], '%Y-%m-%d %H:%M')
        if r['source'] == 'Call centre' and any(abs((t - x).total_seconds()) <= 1800 for x in logged.get(r['protection_ref'], [])):
            continue
        if r['interruption_class'] != 'Unplanned' or float(r['duration_min']) < 1.0:
            continue
        recs.append((former.get(r['feeder'], r['feeder']), t, float(r['duration_min']), int(r['customers_interrupted']),
                     r['cause_code']))
    # ICPs: the year's mean of month-ends, the latest month-end for the year in progress
    months = sorted(icp)
    latest = icp[months[-1]]
    den = {}
    for y in range(2022, 2027):
        ms = ['%d-%02d' % (y + (m < 4), m) for m in list(range(4, 13)) + [1, 2, 3]]
        den[y] = np.mean([icp[m] for m in ms]) if all(m in icp for m in ms) else latest
    day_cm, day_ci = {}, {}
    for f, t, mi, cu, cause in recs:
        d = t.date()
        day_cm[d] = day_cm.get(d, 0) + cu * mi / den[ry(t)]
        day_ci[d] = day_ci.get(d, 0) + cu / den[ry(t)]
    meds = {d for d in day_cm if day_cm[d] > B['DPP3' if ry(d) <= 2024 else 'DPP4'][0]
            or day_ci[d] > B['DPP3' if ry(d) <= 2024 else 'DPP4'][1]}
    veg = [(f, t, cu) for f, t, mi, cu, cause in recs if cause in ('VEG', 'TREE') and t.date() not in meds]
    # stations: the nearest to each zone substation
    def dist(a, b, c, d):
        r = math.pi / 180
        return 2 * 6371 * math.asin(math.sqrt(math.sin((c - a) * r / 2) ** 2 + math.cos(a * r) * math.cos(c * r) * math.sin((d - b) * r / 2) ** 2))
    stn = {}
    for f, v in feeders.items():
        la, lo = zone[v['zone']]
        stn[f] = min(st, key=lambda s: dist(la, lo, float(s['latitude']), float(s['longitude'])))['station_id']
    # the gust load: each hour's gust above 40 km/h, squared, summed by local month
    ex = {}
    for s in st:
        sid = s['station_id']
        path = [p for f, p in files.items() if f.startswith('pou_aws_%s' % sid)][0]
        c = {}
        for r in csv.DictReader(open(path)):
            if r['qc'] in ('M', 'S') or r['gust_max'] == '':
                continue
            g = float(r['gust_max']) * (1.852 if r['wind_unit'] == 'kt' else 1.0)
            loc = dt.datetime.strptime(r['obs_time_utc'], '%Y-%m-%dT%H:%MZ').replace(tzinfo=dt.timezone.utc).astimezone(NZ)
            key = (loc.year, loc.month)
            c[key] = c.get(key, 0) + max(g - 40.0, 0.0) ** 2
        ex[sid] = c
    norm = {sid: {m: np.mean([ex[sid].get((y, m), 0) for y in range(2006, 2026)]) for m in range(1, 13)} for sid in ex}
    # the panel and the fit
    fl = sorted(feeders)
    cnt = {}
    for f, t, cu in veg:
        cnt[(f, t.year, t.month)] = cnt.get((f, t.year, t.month), 0) + 1
    def ys(f, when):
        prior = [d for d in trims[f] if d <= when]
        return (when - prior[-1]).days / 365.25
    Xr, y, off = [], [], []
    ym = [(2022 + (m + 3) // 12, (m + 3) % 12 + 1) for m in range(0, 55)]
    for j, f in enumerate(fl):
        for (yy, mm) in ym:
            e = ex[stn[f]].get((yy, mm), 0)
            if e <= 0:
                continue
            when = dt.datetime(yy, mm, 1) + dt.timedelta(days=14)
            row = np.zeros(len(fl) + 1)
            row[j] = 1.0
            row[-1] = ys(f, when)
            Xr.append(row)
            y.append(cnt.get((f, yy, mm), 0))
            off.append(math.log(e))
    X, y, off = np.array(Xr), np.array(y, float), np.array(off)
    beta = np.zeros(X.shape[1])
    beta[:-1] = math.log(max(y.mean(), 1e-3)) - off.mean()
    for _ in range(60):
        eta = X @ beta + off
        mu = np.exp(eta)
        z = eta - off + (y - mu) / mu
        W = mu
        new = np.linalg.solve(X.T @ (W[:, None] * X), X.T @ (W * z))
        if np.max(np.abs(new - beta)) < 1e-10:
            beta = new
            break
        beta = new
    gamma = beta[-1]
    cpe = {}
    for f in fl:
        v = [cu for g, t, cu in veg if g == f]
        cpe[f] = sum(v) / len(v)
    done = dt.datetime(2027, 3, 31)
    ry27 = [(2027 + (m + 3) // 12, (m + 3) % 12 + 1) for m in range(0, 12)]
    out = {}
    for j, f in enumerate(fl):
        keep = cu_ = 0.0
        for (yy, mm) in ry27:
            when = dt.datetime(yy, mm, 1) + dt.timedelta(days=14)
            e = norm[stn[f]][mm]
            keep += math.exp(beta[j] + gamma * ys(f, when)) * e
            cu_ += math.exp(beta[j] + gamma * (when - done).days / 365.25) * e
        out[f] = (keep, cu_, cpe[f], (keep - cu_) * cpe[f])
    order = sorted(fl, key=lambda f: -out[f][3])
    six = order[:6]
    F = json.load(open(os.path.join(HERE, 'figures.json')))

    def avoided_six(expo):
        """the six's avoided customer interruptions month by month in 2027-28 at the given monthly exposure"""
        months = []
        for (yy, mm) in ry27:
            when = dt.datetime(yy, mm, 1) + dt.timedelta(days=14)
            tot = 0.0
            for f in six:
                j = fl.index(f)
                e = expo(stn[f], mm)
                tot += (math.exp(beta[j] + gamma * ys(f, when)) - math.exp(beta[j] + gamma * (when - done).days / 365.25)) * e * cpe[f]
            months.append(tot)
        return months
    m27 = avoided_six(lambda sid, mm: norm[sid][mm])
    quarters = [sum(m27[3 * k:3 * k + 3]) for k in range(4)]
    years = []
    for y in range(2006, 2026):
        def expo_y(sid, mm, y=y):
            return ex[sid].get((y if mm >= 4 else y + 1, mm), 0)
        years.append(sum(avoided_six(expo_y)))
    rng90 = [int(round(float(np.percentile(years, q)), -3)) for q in (5, 95)]
    ok = True

    def check(name, cond, detail=''):
        nonlocal ok
        ok = ok and cond
        print('%-4s %-52s %s' % ('PASS' if cond else 'FAIL', name, detail))
    check('the six', six == F['six'], ' '.join(six))
    check('total avoided', int(round(sum(out[f][3] for f in six))) == F['avoided_total'], '%.0f' % sum(out[f][3] for f in six))
    check('SAIFI avoided', round(sum(out[f][3] for f in six) / latest, 2) == F['saifi_avoided'], '%.2f' % (sum(out[f][3] for f in six) / latest))
    check('growth per year', round((math.exp(gamma) - 1) * 100, 1) == F['growth_per_year_pct'], '%.1f' % ((math.exp(gamma) - 1) * 100))
    check('major event days', len(meds) == F['med_days'], str(len(meds)))
    rows_ok = all(int(round(out[r['feeder']][3])) == r['avoided'] and int(round(out[r['feeder']][0] * out[r['feeder']][2])) == r['keep_ci']
                  and round(out[r['feeder']][0], 1) == r['keep_n'] and int(round(out[r['feeder']][2])) == r['cpe'] for r in F['rows'])
    check('every feeder row', rows_ok, '%d rows' % len(F['rows']))
    check('stations', stn == F['station_of'], '')
    # the golden table on disk agrees with the figures
    g = list(csv.DictReader(open(os.path.join(TASK, 'golden', 'vegetation_catchup_2027_feeders.csv'))))
    check('golden table ranks', [r['feeder'] for r in g] == [r['feeder'] for r in F['rows']], '%d rows' % len(g))
    check('golden table avoided', all(int(r['customer_interruptions_avoided']) == int(round(out[r['feeder']][3])) for r in g), '')
    check('quarters', all(abs(round(q) - g) <= 1 for q, g in zip(quarters, F['quarters'])), ' '.join('%.0f' % q for q in quarters))
    check('90 per cent range over the 20 complete regulatory years', rng90 == F['range90'], '%d to %d' % tuple(rng90))
    print('VERIFY', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
