"""Independent verifier for task1: reads only the shipped bundle (target/, the golden files) and figures.json, on its
own code path (csv module and a member-level simulation, not golden.py's pandas panel and exact chain).

    python3 task1/generator/verify.py      # exit 1 on any mismatch
"""
import csv
import datetime as dt
import json
import os
import random
import re
import sys
import zipfile
from collections import defaultdict
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, 'target')
GD = os.path.join(TASK, 'golden')
F = json.load(open(os.path.join(HERE, 'figures.json')))
BER = ZoneInfo('Europe/Berlin')
fails = []


def check(cond, label, detail=''):
    print('%s  %s%s' % ('ok  ' if cond else 'FAIL', label, ('  [%s]' % (detail,)) if detail != '' else ''))
    if not cond:
        fails.append(label)


def mon(y, m):
    return (y - 2022) * 12 + m - 1


def r(x, u):
    return int(round(x / float(u))) * u


# ------------------------------------------------------------------ charges
seen = set(); charges = defaultdict(list); refunds = defaultdict(float); first_promo = {}
with open(os.path.join(T, 'billing_events_2022-01_2026-10.csv'), newline='', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        if row['event_id'] in seen:
            continue
        seen.add(row['event_id'])
        amt = float(row['amount']) if row['amount'] else (int(row['amount_minor']) / 100.0 if row['amount_minor'] else None)
        if row['event_type'] == 'refund':
            refunds[row['refund_of']] += amt or 0.0
        elif row['status'] == 'succeeded':
            charges[row['member_id']].append((row['created_at'], row['event_id'], amt, row['currency'], row['plan_code'],
                                              row['billing_period_start'], row['promo_code']))
paid = {}
for m, lst in charges.items():
    lst = sorted(lst)
    keep = [c for c in lst if not (c[2] is not None and refunds.get(c[1], 0.0) >= c[2] - 0.005)]
    if keep:
        paid[m] = keep
check(len(paid) > 20000, 'paid members rebuilt from the payments export', len(paid))

# ------------------------------------------------------------------ campaign members
tag = set()
with open(os.path.join(T, 'signup_attribution_2022-01_2026-10.csv'), newline='', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        if 'aut26' in row['utm_campaign'].lower():
            tag.add(row['account_id'])
camp = []
for m, lst in paid.items():
    if m not in tag:
        continue
    ts = dt.datetime.strptime(lst[0][0], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=dt.timezone.utc).astimezone(BER).date()
    if dt.date(2026, 9, 1) <= ts <= dt.date(2026, 10, 31):
        camp.append(m)
check(len(camp) == F['campaign_members'], 'campaign members', len(camp))

# ------------------------------------------------------------------ cost
rates = {}
with open(os.path.join(T, 'ecb_euro_reference_rates_2022-01_2026-11.csv'), newline='', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        try:
            rates[row['Date']] = (float(row['GBP']), float(row['CHF']))
        except ValueError:
            pass


def rate(d, cur):
    if cur == 'EUR':
        return 1.0
    for back in range(10):
        k = (d - dt.timedelta(days=back)).isoformat()
        if k in rates:
            return rates[k][0 if cur == 'GBP' else 1]
    raise KeyError(d)


from openpyxl import load_workbook
wb = load_workbook(os.path.join(T, 'fenwright_aut26_closeout_and_invoices.xlsx'), data_only=True)
media = 0.0
rows = list(wb['Invoices'].iter_rows(values_only=True))
head = [i for i, x in enumerate(rows) if x and x[0] == 'document'][0]
for x in rows[head + 1:]:
    if x and x[0]:
        d = dt.date.fromisoformat(str(x[2]))
        media += float(x[8]) / rate(d, x[4])
plans = json.load(open(os.path.join(T, 'plans_and_promotions.json')))
lp = {p['code']: p['price'] for p in plans['plans']}
disc = 0.0
cs = set(camp)
for m in camp:
    c = paid[m][0]
    gap = lp[c[4]][c[3]] - c[2]
    if gap > 0:
        disc += gap / rate(dt.date.fromisoformat(c[5]), c[3])
cost = media + disc
check(abs(cost - F['cost_total_exact_eur']) < 0.05, 'campaign cost recomputes to the cent', round(cost, 2))
check(r(cost / len(camp), 25) == F['cost_per_paid_eur'], 'cost per paid member', round(cost / len(camp), 2))

# ------------------------------------------------------------------ lessons: tutors and member months
first_t, last_t, tut_of = {}, {}, {}
with open(os.path.join(T, 'lesson_activity_monthly_2022-01_2026-10.csv'), newline='', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        y, mm = int(row['month'][:4]), int(row['month'][5:7])
        t = mon(y, mm); tid = row['tutor_id']
        first_t[tid] = min(first_t.get(tid, t), t); last_t[tid] = max(last_t.get(tid, t), t)
        tut_of[(row['member_id'], t)] = tid
status = {}
with open(os.path.join(T, 'tutor_directory_2026-11-03.csv'), newline='', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        status[row['tutor_id']] = row['profile_status']
CUT = mon(2026, 10)
stopped = {t: (last_t[t] < CUT and status.get(t) in ('inactive', 'offboarded')) for t in first_t}
risk = defaultdict(int); stop = defaultdict(int)
for t in first_t:
    s, L = first_t[t], last_t[t]
    end = (L + 1 - s) if stopped[t] else (CUT - s)
    for j in range(1, end + 1):
        if s + j > CUT:
            break
        risk[j] += 1
        if stopped[t] and j == L + 1 - s:
            stop[j] += 1
q = {j: stop[j] / risk[j] for j in range(1, 13)}
late_r = sum(risk[j] for j in risk if j > 12); late_s = sum(stop[j] for j in stop if j > 12)
q_late = late_s / late_r
for j in range(1, 13):
    check(abs(100 * q[j] - F['tutor_stop_pct'][str(j)]) < 0.06, 'tutor stopping, teaching month %d' % j, round(100 * q[j], 2))

mstatus = {}
with open(os.path.join(T, 'members_export_2026-11-03.csv'), newline='', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        mstatus[row['member_id']] = row['status']
# member months with states
A_n = defaultdict(int); A_c = defaultdict(int); s1 = [0, 0]; s2 = [0, 0]
state_cut = {}
for m, lst in paid.items():
    ks = [(i + 1, mon(int(c[5][:4]), int(c[5][5:7]))) for i, c in enumerate(lst)]
    alive = mstatus.get(m) == 'active'
    prev = None
    for idx, (k, t) in enumerate(ks):
        tu = tut_of.get((m, t)); ptu = tut_of.get((m, t - 1))
        if tu is None and ptu is not None and stopped.get(ptu) and last_t[ptu] == t - 1:
            st = 'S1'
        elif prev == 'S1':
            st = 'S2'
        elif tu is not None:
            st = 'A'
        else:
            st = 'N'
        c = int(idx == len(ks) - 1 and not alive)
        if st == 'A':
            A_n[min(k, 24)] += 1; A_c[min(k, 24)] += c
        elif st == 'S1':
            s1[0] += 1; s1[1] += c
        elif st == 'S2':
            s2[0] += 1; s2[1] += c
        prev = st
        if idx == len(ks) - 1:
            state_cut[m] = (k, t, st, tu)
d1 = s1[1] / s1[0]; d2 = s2[1] / s2[0]
base = sum(A_c.values()) / sum(A_n.values())
check(abs(100 * d1 - F['stop_month_cancel_pct']) < 0.06, 'cancellation in the month the tutor stops', round(100 * d1, 2))
check(abs(100 * d2 - F['next_month_cancel_pct']) < 0.06, 'cancellation the month after', round(100 * d2, 2))
h = {}
for k in range(1, 25):
    h[k] = A_c[k] / A_n[k] if A_n[k] else 0
for lo, hi in ((7, 12), (13, 24)):
    v = sum(A_c[k] for k in range(lo, hi + 1)) / sum(A_n[k] for k in range(lo, hi + 1))
    for k in range(lo, hi + 1):
        h[k] = v

# ------------------------------------------------------------------ simulation: expected twelfth-month members
random.seed(20261107)
N = 400
kept = 0.0; pay = defaultdict(float)
live = [m for m in camp if mstatus.get(m) == 'active' and state_cut[m][1] == CUT]
done = sum(1 for m in camp if m not in set(live) and state_cut[m][0] >= 12)
for m in live:
    k0, t0, st0, tu = state_cut[m]
    tj = (t0 - first_t[tu]) if tu else None
    for _ in range(N):
        state = 'S2' if st0 == 'S1' else ('E' if tu is None else 'A'); j = tj; k = k0
        for step in range(1, 12):
            t = t0 + step; k += 1
            if state == 'A':
                j += 1
                if random.random() < (q[j] if j <= 12 else q_late):
                    state = 'S1'
            elif state == 'E' and random.random() < q_late:
                state = 'S1'
            pay[t] += 1.0 / N
            if k == 12:
                kept += 1.0 / N
            hk = h[min(k, 24)]
            if state == 'S1':
                c = 1 - (1 - hk) * (1 - d1) / (1 - base); nxt = 'S2'
            elif state == 'S2':
                c = 1 - (1 - hk) * (1 - d2) / (1 - base); nxt = 'E'
            else:
                c = hk; nxt = state
            if random.random() < c:
                break
            state = nxt
e12 = done + kept
check(abs(e12 - F['exp12_raw']) / F['exp12_raw'] < 0.012, 'expected twelfth-month members, simulated (within 1.2 per cent)', round(e12, 1))
check(r(e12, 50) == F['exp12'], 'expected twelfth-month members at the asked rounding', r(e12, 50))
check(r(cost / e12, 25) == F['cost_per_12m_eur'], 'cost per twelfth-month member at the asked rounding', round(cost / e12, 1))
check(r(800.0 * e12 / len(camp), 25) == F['flip_cost_per_paid_eur'], 'highest clearing cost per paid member', round(800.0 * e12 / len(camp), 2))
for t in sorted(pay):
    lab = '%04d-%02d' % (2022 + t // 12, t % 12 + 1)
    if lab in F['monthly_raw']:
        check(abs(pay[t] - F['monthly_raw'][lab]) / F['monthly_raw'][lab] < 0.015, 'members paying in %s (within 1.5 per cent)' % lab, round(pay[t], 1))
check(cost / e12 > 800, 'the call: the cost per twelfth-month member is above the EUR 800 bar')

# ------------------------------------------------------------------ the membership-month curve (the default path)
allh = defaultdict(lambda: [0, 0])
for m, lst in paid.items():
    alive = mstatus.get(m) == 'active'
    for i in range(len(lst)):
        allh[min(i + 1, 24)][0] += 1
        allh[min(i + 1, 24)][1] += int(i == len(lst) - 1 and not alive)
hc = {k: allh[k][1] / allh[k][0] for k in range(1, 25)}
for lo, hi in ((7, 12), (13, 24)):
    v = sum(allh[k][1] for k in range(lo, hi + 1)) / sum(allh[k][0] for k in range(lo, hi + 1))
    for k in range(lo, hi + 1):
        hc[k] = v
e0 = done
for m in live:
    s = 1.0
    for k in range(state_cut[m][0] + 1, 12):
        s *= 1 - hc[min(k, 24)]
    e0 += s
check(r(e0, 50) == F['default_exp12'] and r(cost / e0, 25) == F['default_cost_per_12m_eur'], 'the default path: the curve books the re-run', (round(e0, 1), round(cost / e0, 1)))

# ------------------------------------------------------------------ every format read back
from pypdf import PdfReader
txt = ' '.join(p.extract_text() for p in PdfReader(os.path.join(T, 'growth_review_standard.pdf')).pages)
txt = re.sub(r'\s+', ' ', txt)
check('pays a twelfth monthly membership charge' in txt and 'calendar days in Berlin' in txt and 'first-month discounts' in txt,
      'the standard\'s definitions read back from the PDF')
check('twelfth' in txt and 'tutor' not in txt.lower(), 'the standard names no tutor, matching or stopping')
from docx import Document
memo = ' '.join(p.text for p in Document(os.path.join(GD, 'aut26_rerun_memo.docx')).paragraphs)
check('Do not book' in memo and ('EUR %d per member still paying' % F['cost_per_12m_eur']) in memo, 'the memo states the call and the cost per twelfth-month member')
check(('80%% range EUR %d to %d' % tuple(F['range80_cost_eur'])) in memo.replace(',', ''), 'the memo states the 80 per cent range')
check(('90%% range EUR %d to %d' % tuple(F['range90_cost_eur'])) in memo.replace(',', ''), 'the memo states the 90 per cent range')
gw = load_workbook(os.path.join(GD, 'aut26_member_forecast.xlsx'), data_only=True)
ws = gw['Monthly']
vals = [row for row in ws.iter_rows(min_row=4, values_only=True) if row and row[0] and re.match(r'[A-Z][a-z]{2} \d{4}', str(row[0]))]
check(len(vals) == 11 and all(v[3] == F['monthly']['All'][dt.datetime.strptime(v[0], '%b %Y').strftime('%Y-%m')] for v in vals),
      'the workbook\'s monthly totals agree with figures.json', len(vals))
check(all(z.read('docProps/core.xml').find(b'python-docx') < 0 for z in [zipfile.ZipFile(os.path.join(GD, 'aut26_rerun_memo.docx'))]),
      'the memo carries no writing library')
print('\n%d failed' % len(fails))
sys.exit(1 if fails else 0)
