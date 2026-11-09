"""The independent verifier: reads only target.zip and golden.zip (no generator state, no pandas, no openpyxl; the
workbooks are read from their XML), recomputes the call and every figure the answer blocks owe, and reads both golden
files back.

    python3 task12/generator/verify.py
"""
import csv
import datetime as dt
import io
import json
import math
import os
import re
import sys
import zipfile
from collections import defaultdict

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
FIRST = dt.date(2024, 1, 1)
RESULTS = []


def ok(label, cond, detail=''):
    RESULTS.append((label, bool(cond), detail))


def xlsx_rows(data, sheet_name):
    """rows of one sheet from the workbook's XML: shared strings resolved, numbers as floats"""
    z = zipfile.ZipFile(io.BytesIO(data))
    ss = []
    if 'xl/sharedStrings.xml' in z.namelist():
        x = z.read('xl/sharedStrings.xml').decode('utf-8')
        for si in re.findall(r'<si>(.*?)</si>', x, re.S):
            ss.append(''.join(re.findall(r'<t[^>]*>(.*?)</t>', si, re.S)).replace('&amp;', '&'))
    wb = z.read('xl/workbook.xml').decode('utf-8')
    rels = z.read('xl/_rels/workbook.xml.rels').decode('utf-8')
    sheets = re.findall(r'<sheet [^>]*name="([^"]+)"[^>]*r:id="([^"]+)"', wb)
    rid = dict(sheets)[sheet_name]
    target = re.search(r'<Relationship [^>]*Id="%s"[^>]*Target="([^"]+)"' % rid, rels) or \
        re.search(r'<Relationship [^>]*Target="([^"]+)"[^>]*Id="%s"' % rid, rels)
    path = 'xl/' + target.group(1).lstrip('/').replace('xl/', '')
    x = z.read(path).decode('utf-8')
    out = []
    for row in re.findall(r'<row [^>]*>(.*?)</row>', x, re.S):
        cells = {}
        for ref, attrs, body in re.findall(r'<c r="([A-Z]+)\d+"([^>]*)>(.*?)</c>', row, re.S):
            v = re.search(r'<v>(.*?)</v>', body)
            if v is None:
                continue
            if 't="s"' in attrs:
                cells[ref] = ss[int(v.group(1))]
            else:
                try:
                    cells[ref] = float(v.group(1))
                except ValueError:
                    cells[ref] = v.group(1)
        if cells:
            width = max(col_index(k) for k in cells) + 1
            out.append([cells.get(col_name(i)) for i in range(width)])
    return out


def col_index(s):
    n = 0
    for ch in s:
        n = n * 26 + ord(ch) - 64
    return n - 1


def col_name(i):
    s = ''
    i += 1
    while i:
        i, r = divmod(i - 1, 26)
        s = chr(65 + r) + s
    return s


def week(d):
    return (d - FIRST).days // 7


def parse_date(s):
    if '-' in s:
        return dt.date(int(s[:4]), int(s[5:7]), int(s[8:10]))
    d, m, y = s.split('/')
    return dt.date(int(y), int(m), int(d))


def main():
    F = json.load(open(os.path.join(HERE, 'figures.json')))
    tz = zipfile.ZipFile(os.path.join(TASK, 'target.zip'))
    names = {os.path.basename(n): n for n in tz.namelist() if not n.endswith('/')}
    get = lambda part: tz.read(names[next(k for k in names if part in k)])
    # product master
    rows = xlsx_rows(get('product_master'), 'Items')
    head = rows[0]
    litres = {}
    brand = {}
    for r in rows[1:]:
        d = dict(zip(head, r))
        code = str(d['item_code']).split('.')[0].zfill(13)
        size = float(d['pack_size'])
        litres[code] = (size / 1000.0 if d['pack_uom'] == 'mL' else size) * float(d['units_per_pack'])
        brand[code] = d['brand']
    ok('master: 39 items read from the workbook XML', len(litres) == 39, str(len(litres)))
    # households
    H = list(csv.DictReader(io.StringIO(get('household_register').decode('utf-8'))))
    idx = {h['hh_id']: i for i, h in enumerate(H)}
    n = len(H)
    static = np.array([int(h['joined_week'][:4]) <= 2023 and h['left_week'] == '' for h in H])
    wt = np.array([float(h['proj_factor_2026']) if h['proj_factor_2026'] else 0.0 for h in H])
    # trade calendar weeks (run events)
    tr = xlsx_rows(get('trade_calendar'), '2026 events')
    hi = next(i for i, r in enumerate(tr) if r and r[0] == 'event_id')
    th = tr[hi]
    promo = set()
    for r in tr[hi + 1:]:
        d = dict(zip(th, r))
        if d.get('status') != 'Run':
            continue
        a = parse_date(str(d['start_date'])[:10]) if '-' in str(d['start_date']) else excel_date(d['start_date'])
        b = parse_date(str(d['end_date'])[:10]) if '-' in str(d['end_date']) else excel_date(d['end_date'])
        promo.update(range(week(a), week(b) + 1))
    # the retail audit: the line's weighted distribution in each banner and week (the highest of its items)
    dist = defaultdict(float)
    for d in csv.DictReader(io.StringIO(get('mra_weighted_distribution').decode('utf-8'))):
        key = (week(parse_date(d['week_ending'])), d['banner_cd'])
        dist[key] = max(dist[key], float(d['wtd_dist_pct']) / 100.0)
    recode = {'NTG': 'NGF', 'MBL': 'MBV'}
    # purchase lines: receipts uploaded twice halved
    text = get('lcp_purchases').decode('utf-8')
    rec = defaultdict(list)
    for r in csv.reader(io.StringIO(text)):
        if r[0] == 'hh_id':
            continue
        rec[r[1]].append(tuple(r))
    END, LAUNCH, PRE_END = 147, 118, 117
    cat = np.zeros((END + 1, n)); nvl = np.zeros((END + 1, n)); avl = np.zeros((END + 1, n))
    pre_all = np.zeros(n); pre_stk = np.zeros(n)
    first = np.full(n, 10 ** 6)
    paid = np.zeros(n); lit_pre = np.zeros(n)
    nvlit = np.zeros(n); nvrec = np.zeros(n)
    for rid, lines in rec.items():
        cnt = defaultdict(int)
        for ln in lines:
            cnt[ln] += 1
        halve = all(c % 2 == 0 for c in cnt.values())
        seen_nv = False
        for ln, c in cnt.items():
            k = c // 2 if halve else c
            hh, _, ds, bc, code, q, amt, deal = ln
            i = idx[hh]
            code = code.zfill(13)
            d = parse_date(ds)
            t = week(d)
            L = litres[code] * int(q) * k
            isnv = brand[code] == 'Northvale Oat'
            bn = recode.get(bc, bc)
            if LAUNCH <= t <= END:
                avl[t, i] += L * dist[(t, bn)]
            if 0 <= t < 104:
                pre_all[i] += L
                pre_stk[i] += L * dist[(END, bn)]
            if 0 <= t <= END:
                cat[t, i] += L
                if isnv:
                    nvl[t, i] += L
                    if int(q) > 0:
                        first[i] = min(first[i], t)
                        nvlit[i] += L
                        if not seen_nv:
                            nvrec[i] += 1
                            seen_nv = True
            if t <= PRE_END and not isnv:
                paid[i] += float(amt) * k
                lit_pre[i] += L
    first = np.where(first == 10 ** 6, -1, first)
    buyer = static & (cat.sum(0) > 0)
    triers = buyer & (first >= 0)
    ok('panel: static households, category buyers and buyers of the line', (static.sum(), buyer.sum(), triers.sum()) ==
       (F['static_panel'], F['buyers_panel'], F['triers_panel']), '%d %d %d' % (static.sum(), buyer.sum(), triers.sum()))
    ppl = np.where(lit_pre > 0.5, paid / np.maximum(lit_pre, 1e-9), np.nan)
    okp = buyer & np.isfinite(ppl)
    q1, q2 = np.nanquantile(ppl[okp], [1 / 3, 2 / 3])
    tier = np.where(np.isfinite(ppl), np.where(ppl >= q2, 0, np.where(ppl >= q1, 1, 2)), 1)
    ok('tiers: tercile cuts of price paid per litre', abs(q1 - F['cuts_ppl'][0]) < 0.006 and abs(q2 - F['cuts_ppl'][1]) < 0.006,
       '%.3f %.3f' % (q1, q2))
    num = np.zeros(3); den = np.zeros(3)
    for t in range(LAUNCH, END + 1):
        if t in promo:
            continue
        m0 = buyer & (first >= 0) & (t - first >= 16)
        for k in range(3):
            m = m0 & (tier == k)
            num[k] += nvl[t, m].sum(); den[k] += avl[t, m].sum()
    fl = num / den
    ok('settled shares of stocked litres by price group', all(abs(100 * fl[k] - F['floors_pct'][k]) < 0.051 for k in range(3)), str(np.round(100 * fl, 2)))
    a27 = np.where(pre_all > 0, pre_stk / np.maximum(pre_all, 1e-9), 0.0)
    lev = fl[tier] * a27
    a = (cat[0:52, static].sum(0) * wt[static]).sum()
    b = (cat[52:104, static].sum(0) * wt[static]).sum()
    g = b / a
    L27 = cat[0:104].sum(0) / 104.0 * g ** ((182.5 - 51.5) / 52.0) * 52.0
    # households not yet buying: each price group's weekly first-purchase rate in the weeks matching the basis (every
    # banner carrying the line at the review already carrying it, no promotion, no media), carried into 2027
    mrows = xlsx_rows(get('media_plan'), 'Flighting')
    mh = next(i for i, r in enumerate(mrows) if r and r[0] == 'week_start')
    media = set()
    for r in mrows[mh + 1:]:
        if r and r[0] not in (None, ''):
            d0 = parse_date(str(r[0])[:10]) if '-' in str(r[0]) else excel_date(r[0])
            media.add(week(d0))
    listed = [b for (t, b), x in dist.items() if t == END and x > 0]
    full_t = max(min(t for (t, b), x in dist.items() if b == bb and x > 0) for bb in listed)
    tweeks = [t for t in range(full_t, END + 1) if t not in promo and t not in media]
    raw_pack = np.where(nvrec > 0, nvlit / np.maximum(nvrec, 1), np.nan)
    pmed = float(np.nanmedian(raw_pack))
    p27 = np.zeros(n)
    for k in range(3):
        at = buyer & (tier == k)
        risk = sum((wt * (at & ((first < 0) | (first >= t)))).sum() for t in tweeks)
        hit = sum((wt * (at & (first == t))).sum() for t in tweeks)
        h = hit / risk if risk > 0 else 0.0
        p27[at & (first < 0)] = (1 - h) ** (157 - END - 1) * (1 - (1 - h) ** 52)
    lit_new = p27 * (pmed + lev * L27 * 0.5)
    pur_new = p27 * (1 + lev * L27 * 0.5 / pmed)
    share = ((wt * np.where(triers, lev, 0.0) * L27)[static].sum() + (wt * lit_new)[static].sum()) / (wt * L27)[static].sum()
    ok('the 2027 share to one decimal', round(100 * share, 1) == F['share_pct'], '%.3f' % (100 * share))
    e0, e1, e2 = F['bands_pct']
    bandname = 'Delist' if 100 * share < e0 else 'Hold' if 100 * share < e1 else 'Support' if 100 * share < e2 else 'Expand'
    ok('the treatment', bandname == F['band'] == 'Hold', bandname)
    scale = wt.sum() / wt[static].sum()     # the static panel raised to the 2026 factors' total
    cat27 = scale * (wt * L27)[static].sum()
    ok('2027 litres in millions', abs(share * cat27 / 1e6 - F['line27_ml']) < 0.051, '%.3f' % (share * cat27 / 1e6))
    pack = np.where(nvrec > 0, nvlit / np.maximum(nvrec, 1), np.nan)
    pack = np.where(np.isfinite(pack), pack, np.nanmedian(pack))
    npur = np.where(triers, lev * L27 / pack, 0.0)
    pb = 1 - np.exp(-npur)
    buyers27 = scale * ((wt * pb)[static].sum() + (wt * p27)[static].sum())
    ok('households buying in 2027 to the nearest 10,000', int(round(buyers27 / 1e4) * 1e4) == F['buyers27'], '%.0f' % buyers27)
    per = ((wt * npur)[static].sum() + (wt * pur_new)[static].sum()) / ((wt * pb)[static].sum() + (wt * p27)[static].sum())
    ok('purchases per buying household', abs(per - F['per_buyer']) < 0.051, '%.3f' % per)
    # the default path: Parfitt-Collins with the April buyers' repeat and the buying index since launch
    r0, r1 = 141, END
    cr = cat[r0:r1 + 1].sum(0); nr = nvl[r0:r1 + 1].sum(0)
    mature = triers & (first <= LAUNCH + 3)
    R_mat = (nr * wt)[mature].sum() / (cr * wt)[mature].sum()
    P = (wt * triers)[buyer].sum() / wt[buyer].sum()
    cw = cat[LAUNCH:END + 1].sum(0)
    B = ((wt * cw)[triers].sum() / wt[triers].sum()) / ((wt * cw)[buyer].sum() / wt[buyer].sum())
    pc = P * R_mat * B
    ok('the default path files expand at the stated figure', round(100 * pc, 1) == F['rejected']['pc_careful'] and 100 * pc >= e2,
       '%.3f' % (100 * pc))
    # golden files read back
    gz = zipfile.ZipFile(os.path.join(TASK, 'golden.zip'))
    gn = sorted(os.path.basename(x) for x in gz.namelist() if not x.endswith('/'))
    ok('golden zip holds exactly the two requested files', gn == ['northvale_oat_2027_forecast.xlsx', 'northvale_oat_2027_treatment.docx'], str(gn))
    doc = gz.read(next(x for x in gz.namelist() if x.endswith('.docx')))
    body = zipfile.ZipFile(io.BytesIO(doc)).read('word/document.xml').decode('utf-8')
    txt = re.sub(r'<[^>]+>', '', body)
    ok('paper: opens with the treatment and the share (positive control)', 'Hold: Northvale Oat will take about %.1f per cent' % F['share_pct'] in txt)
    ok('paper: carries one chart', zipfile.ZipFile(io.BytesIO(doc)).namelist().count('word/media/image1.png') == 1)
    book = gz.read(next(x for x in gz.namelist() if x.endswith('.xlsx')))
    fr = xlsx_rows(book, '2027 forecast')
    qv = [r[2] for r in fr if r and isinstance(r[0], str) and r[0].startswith('2027 Q')]
    ok('workbook: four quarters whose litres round to the paper\'s', [round(x, 1) for x in qv] == F['quarters_ml'], str(qv))
    fails = [r for r in RESULTS if not r[1]]
    for lab, good, det in RESULTS:
        print('%s  %s%s' % ('PASS' if good else 'FAIL', lab, ('  [%s]' % det) if det else ''))
    print('verify: %d checks, %d failed' % (len(RESULTS), len(fails)))
    return 1 if fails else 0


def excel_date(v):
    return dt.date(1899, 12, 30) + dt.timedelta(days=int(float(v)))


if __name__ == '__main__':
    sys.exit(main())
