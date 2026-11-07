"""The golden answer for task601, computed from the shipped files under target/ only.

    python3 task601/generator/golden.py          # writes generator/figures.json and the golden deliverables

Reads nothing the generator knows: every figure is computed from the pack the way a careful analyst would, and the
same functions price every rival route for checks.py.
"""
import csv
import datetime as dt
import json
import os
import sys
from collections import defaultdict

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *          # noqa: E402,F401,F403

CUT_M = month_index(2026, 10)          # 57, October 2026
LAST_M = month_index(2027, 9)          # 68, September 2027
BAR_EUR = 800.0                        # the growth lead's re-run bar (stated in the prompt)
FILES = json.load(open(os.path.join(HERE, 'files.json'))) if os.path.exists(os.path.join(HERE, 'files.json')) else None


def mi(d):
    return month_index(d.year, d.month)


# ------------------------------------------------------------------------------------------------ loading
def load(target=TARGET):
    f = {k: os.path.join(target, v) for k, v in FILE_NAMES.items()}
    bill = pd.read_csv(f['billing'], dtype=str, keep_default_na=False)
    mem = pd.read_csv(f['members'], dtype=str, keep_default_na=False)
    les = pd.read_csv(f['lessons'], dtype=str, keep_default_na=False)
    tut = pd.read_csv(f['tutors'], dtype=str, keep_default_na=False)
    att = pd.read_csv(f['attribution'], dtype=str, keep_default_na=False)
    ecb = pd.read_csv(f['ecb'], dtype=str, keep_default_na=False)
    plans = json.load(open(f['plans']))
    from openpyxl import load_workbook
    wb = load_workbook(f['agency'], data_only=True)
    return dict(bill=bill, mem=mem, les=les, tut=tut, att=att, ecb=ecb, plans=plans, wb=wb)


FILE_NAMES = dict(
    members='members_export_2026-11-03.csv',
    billing='billing_events_2022-01_2026-10.csv',
    lessons='lesson_activity_monthly_2022-01_2026-10.csv',
    tutors='tutor_directory_2026-11-03.csv',
    attribution='signup_attribution_2022-01_2026-10.csv',
    agency='fenwright_aut26_closeout_and_invoices.xlsx',
    plans='plans_and_promotions.json',
    standard='growth_review_standard.pdf',
    ecb='ecb_euro_reference_rates_2022-01_2026-11.csv',
    eurostat='eurostat_edat_aes_l21_foreign_languages_known.csv',
    nps='nps_in_app_responses_2026-01_2026-10.csv',
)


def ecb_rates(ecb):
    r = {}
    for _, row in ecb.iterrows():
        g, c = row['GBP'], row['CHF']
        if g not in ('', 'N/A') and c not in ('', 'N/A'):
            r[row['Date']] = (float(g), float(c))
    return r


# ------------------------------------------------------------------------------------------------ cleaning
def collected_charges(bill):
    """One row per collected membership charge not refunded in full: member, k, period month, amount, currency."""
    b = bill.drop_duplicates()                                  # webhook replays repeat a whole row
    b = b.drop_duplicates(subset=['event_id'])
    amt = np.where(b['amount'] != '', pd.to_numeric(b['amount'].replace('', np.nan), errors='coerce'),
                   pd.to_numeric(b['amount_minor'].replace('', np.nan), errors='coerce') / 100.0)
    b = b.assign(amt=amt)
    ch = b[(b.event_type == 'charge') & (b.status == 'succeeded')].copy()
    rf = b[b.event_type == 'refund'].groupby('refund_of')['amt'].sum()
    ch['refunded'] = ch['event_id'].map(rf).fillna(0.0)
    ch = ch[~(ch['refunded'] >= ch['amt'] - 0.005)]              # a charge refunded in full does not count
    ch['created'] = pd.to_datetime(ch['created_at'], utc=True)
    ch['period'] = pd.to_datetime(ch['billing_period_start']).dt.date
    ch = ch.sort_values(['member_id', 'created'])
    ch['k'] = ch.groupby('member_id').cumcount() + 1
    ch['t'] = [mi(d) for d in ch['period']]
    return ch


def campaign_members(ch, att, code=CAMPAIGN, first=CAMP_FIRST, last=CAMP_LAST, berlin=True):
    tag = att[att.utm_campaign.str.lower().str.contains(code.lower())]
    tagged = set(tag['account_id'])
    fc = ch[ch.k == 1].set_index('member_id')
    if berlin:
        d = fc['created'].dt.tz_convert('Europe/Berlin').dt.date
    else:
        d = fc['created'].dt.date
    ok = (d >= first) & (d <= last)
    return sorted(m for m in fc.index[ok] if m in tagged)


def campaign_cost(ch, wb, rates, members, plans):
    """Media net of VAT and credit notes (GBP at the ECB rate of the issue date) plus first-month discounts."""
    ws = wb['Invoices']
    rows = list(ws.iter_rows(values_only=True))
    hi = [i for i, r in enumerate(rows) if r and r[0] == 'document'][0]
    head = rows[hi]
    media = 0.0; media_gbp = 0.0; media_eur_lines = 0.0; credit = 0.0
    for r in rows[hi + 1:]:
        if not r or r[0] is None:
            continue
        rec = dict(zip(head, r))
        d = dt.date.fromisoformat(str(rec['issued_on']))
        net = float(rec['net'])
        eur = net if rec['currency'] == 'EUR' else net / rate_on(rates, d, rec['currency'])
        media += eur
        if rec['type'] == 'credit note':
            credit += eur
        elif rec['currency'] == 'GBP':
            media_gbp += net
        else:
            media_eur_lines += net
    # first-month discounts against the list price of the plan charged
    price = {}
    for p in plans['plans']:
        price[p['code']] = p['price']
    fc = ch[(ch.k == 1) & (ch.member_id.isin(set(members)))]
    disc = 0.0
    for _, r in fc.iterrows():
        lp = price[r['plan_code']][r['currency']]
        d_cur = lp - r['amt']
        if d_cur == d_cur and d_cur > 0:
            disc += d_cur if r['currency'] == 'EUR' else d_cur / rate_on(rates, r['period'], r['currency'])
    return dict(media_eur=round(media, 2), credit_eur=round(credit, 2), media_gbp_net=round(media_gbp, 2),
                media_eur_lines=round(media_eur_lines, 2), discounts_eur=round(disc, 2),
                total_eur=round(media + disc, 2))


# ------------------------------------------------------------------------------------------------ panels
def tutor_table(les, tut):
    l = les.copy()
    l['tid'] = l['tutor_id'].str.replace('T-', '', regex=False).astype(int)
    l['t'] = [month_index(int(s[:4]), int(s[5:7])) for s in l['month']]
    g = l.groupby('tid')['t'].agg(['min', 'max'])
    st = tut.assign(tid=tut.tutor_id.str.replace('T-', '', regex=False).astype(int)).set_index('tid')['profile_status']
    g['status'] = st.reindex(g.index).fillna('')
    g['stopped'] = (g['max'] < CUT_M) & g['status'].isin(['inactive', 'offboarded'])
    return l, g


def member_panel(ch, mem, l, ttab):
    """Member x paid month with the tutor state: A active tutor, S1 tutor stopped (first month), S2 the month after
    (new tutor), P the three months after that, N no lessons for another reason."""
    tut_of = l.groupby(['member_id', 't'])['tid'].first()
    tut_of = tut_of.to_dict()
    tmax = ttab['max'].to_dict(); stopped = ttab['stopped'].to_dict()
    last_k = ch.groupby('member_id')['k'].max().to_dict()
    status = mem.set_index('member_id')['status'].to_dict()
    rows = []
    for m, grp in ch.groupby('member_id', sort=False):
        ks = grp['k'].tolist(); ts = grp['t'].tolist()
        lk = last_k[m]; alive = status.get(m) == 'active'
        state_prev = None; post = 0
        for k, t in zip(ks, ts):
            tu = tut_of.get((m, t))
            prev_tu = tut_of.get((m, t - 1))
            if tu is None and prev_tu is not None and stopped.get(prev_tu, False) and tmax.get(prev_tu) == t - 1:
                state = 'S1'
            elif state_prev == 'S1':
                state = 'S2'
            elif post > 0 and tu is not None:
                state = 'P'
            elif tu is not None:
                state = 'A'
            else:
                state = 'N'
            if state == 'S2':
                post = 3
            elif state == 'P':
                post -= 1
            c = int(k == lk and not alive)
            rows.append((m, k, t, tu if tu is not None else -1, state, c))
            state_prev = state
    p = pd.DataFrame(rows, columns=['member_id', 'k', 't', 'tid', 'state', 'c'])
    tmin = ttab['min'].to_dict()
    p['tj'] = [(t - tmin[tu]) if tu >= 0 else -1 for t, tu in zip(p['t'], p['tid'])]
    return p


# ------------------------------------------------------------------------------------------------ estimation
KMAX = 24


def kcurve(df):
    g = df.groupby('k')['c'].agg(['sum', 'count'])
    h = (g['sum'] / g['count'])
    out = {}
    for k in range(1, KMAX + 1):
        out[k] = float(h.get(k, np.nan))
    # pool the sparse tail: months 7 to 12 and 13 to 24 each share one rate
    for lo, hi in ((7, 12), (13, 24)):
        s = df[(df.k >= lo) & (df.k <= hi)]
        r = s['c'].sum() / max(len(s), 1)
        for k in range(lo, hi + 1):
            out[k] = float(r)
    return out


def season(df, h):
    exp = df['k'].clip(upper=KMAX).map(h)
    cm = (df['t'] % 12) + 1
    r = df['c'].groupby(cm).sum() / exp.groupby(cm).sum()
    return {int(i): float(v) for i, v in r.items()}


def tutor_stops(ttab, cut=CUT_M):
    """Monthly stopping by teaching month j (the tutor's first lesson month is j = 0)."""
    risk = defaultdict(int); stop = defaultdict(int)
    for tid, r in ttab.iterrows():
        s, L = int(r['min']), int(r['max'])
        end = (L + 1 - s) if r['stopped'] else (cut - s)
        for j in range(1, end + 1):
            if s + j > cut:
                break
            risk[j] += 1
            if r['stopped'] and j == L + 1 - s:
                stop[j] += 1
    q = {}
    for j in range(1, 13):
        q[j] = stop[j] / risk[j] if risk[j] else 0.0
    late = [j for j in risk if j > 12]
    q['late'] = sum(stop[j] for j in late) / max(sum(risk[j] for j in late), 1)
    q['pooled_tutor_months'] = sum(stop.values()) / max(sum(risk.values()), 1)
    q['risk'] = dict(risk); q['stop'] = dict(stop)
    return q


def estimate(panel, ttab, seasonal=False):
    A = panel[panel.state == 'A']
    h = kcurve(A)
    se = season(A, h) if seasonal else {m: 1.0 for m in range(1, 13)}
    base = A['c'].mean()
    s1 = panel[panel.state == 'S1']; s2 = panel[panel.state == 'S2']; pp = panel[panel.state == 'P']
    d1, d2 = s1['c'].mean(), s2['c'].mean()
    exp_p = pp['k'].clip(upper=KMAX).map(h).sum()
    post = pp['c'].sum() / exp_p if exp_p else 1.0
    q = tutor_stops(ttab)
    # member-side stopping: share of active-tutor member months whose tutor stops the next month
    nxt = panel.sort_values(['member_id', 'k'])
    mw = ((nxt['state'] == 'S1').sum()) / max(((nxt['state'] == 'A') | (nxt['state'] == 'P') | (nxt['state'] == 'S1')).sum(), 1)
    return dict(h=h, season=se, base=float(base), d1=float(d1), d2=float(d2), post=float(post), q=q,
                n_s1=int(len(s1)), n_s2=int(len(s2)), member_weighted_stop=float(mw))


# ------------------------------------------------------------------------------------------------ projection
def shock(h, d, base):
    """A month's cancellation when a shock that raised the average month to d applies to a member whose own
    month would be h: survival scales by (1 - d) / (1 - base)."""
    return 1 - (1 - h) * (1 - d) / (1 - base)


def project_member(k0, t0, tj0, state0, par, qfun, seasonal=False, two=True, post=False, horizon=LAST_M):
    """Exact month-by-month projection for one member alive after the decision of paid month k0 (calendar t0).
    Returns {calendar month: probability the member pays that month} for t0+1..horizon, and P(pays charge 12)."""
    h, se, base, d1, d2, pm = par['h'], par['season'], par['base'], par['d1'], par['d2'], par['post']
    q_late = par['q']['late']
    # state distribution: ('A', j) tutor active at teaching month j; ('S1',) ; ('S2',) ; ('P', r) ; ('E',)
    dist = {}
    if state0 == 'S1':
        dist[('S2',)] = 1.0
    elif state0 == 'S2':
        dist[('P', 3)] = 1.0
    elif state0 == 'P':
        dist[('E',)] = 1.0
    elif tj0 is None or tj0 < 0:
        dist[('E',)] = 1.0
    else:
        dist[('A', tj0)] = 1.0
    pay = {}; p12 = 1.0 if k0 >= 12 else None
    for step, t in enumerate(range(t0 + 1, horizon + 1), start=1):
        k = k0 + step
        # tutor stops at the start of the month
        nd = defaultdict(float)
        for s, p in dist.items():
            if s[0] == 'A':
                j = s[1] + 1
                qs = qfun(j)
                nd[('S1',)] += p * qs
                nd[('A', j)] += p * (1 - qs)
            elif s[0] in ('E', 'P'):
                nd[('S1',)] += p * q_late
                nd[s] += p * (1 - q_late)
            else:
                nd[s] += p
        dist = nd
        alive = sum(dist.values())
        pay[t] = alive
        if k == 12:
            p12 = alive
        cm = (t % 12) + 1
        hk = h[min(k, KMAX)] * (se.get(cm, 1.0) if seasonal else 1.0)
        nd = defaultdict(float)
        for s, p in dist.items():
            if s[0] == 'S1':
                c = shock(hk, d1, base)
                nd[('S2',) if two else ('P', 3)] += p * (1 - c)
            elif s[0] == 'S2':
                c = shock(hk, d2, base)
                nd[('P', 3)] += p * (1 - c)
            elif s[0] == 'P':
                c = min(.95, hk * (pm if post else 1.0))
                nd[('P', s[1] - 1) if s[1] > 1 else ('E',)] += p * (1 - c)
            else:
                c = hk
                nd[s] += p * (1 - c)
        dist = nd
    return pay, p12


def state_at_cut(panel, members):
    last = panel[panel.member_id.isin(set(members))].sort_values('k').groupby('member_id').last()
    return last


def project_group(panel, mem, members, par, qfun, **kw):
    status = mem.set_index('member_id')['status'].to_dict()
    last = state_at_cut(panel, members)
    exp12 = 0.0; monthly = defaultdict(float); by = {}
    for m in members:
        r = last.loc[m]
        if status.get(m) != 'active' or r['t'] != CUT_M:
            exp12 += 1.0 if r['k'] >= 12 else 0.0
            by[m] = (1.0 if r['k'] >= 12 else 0.0, {})
            continue
        pay, p12 = project_member(int(r['k']), int(r['t']), int(r['tj']) if r['tid'] >= 0 else None,
                                  r['state'], par, qfun, **kw)
        exp12 += p12
        for t, p in pay.items():
            monthly[t] += p
        by[m] = (p12, pay)
    return exp12, dict(monthly), by


# ------------------------------------------------------------------------------------------------ the golden
def run(target=TARGET):
    P = load(target)
    rates = ecb_rates(P['ecb'])
    ch = collected_charges(P['bill'])
    members = campaign_members(ch, P['att'])
    cost = campaign_cost(ch, P['wb'], rates, members, P['plans'])
    l, ttab = tutor_table(P['les'], P['tut'])
    panel = member_panel(ch, P['mem'], l, ttab)
    par = estimate(panel, ttab)
    qf = lambda j: par['q'][j] if j <= 12 else par['q']['late']
    exp12, monthly, by = project_group(panel, P['mem'], members, par, qf)
    return dict(P=P, rates=rates, ch=ch, members=members, cost=cost, l=l, ttab=ttab, panel=panel, par=par,
                exp12=exp12, monthly=monthly, by=by, qf=qf)



# ------------------------------------------------------------------------------------------------ uncertainty
N_REP = 4000   # draws behind every range the deliverables state


def predictive_range(R, n_rep=400, seed=601, clustered=True, monthly=False, inputs_fixed=False):
    """80 per cent range of the twelfth-month members: parameters redrawn (tutors resampled for the stopping curve,
    stop-month and baseline rates redrawn), then each campaign tutor's stop drawn once and shared by its members.
    With monthly=True also returns each month's 10th and 90th percentile of the members paying."""
    rng = np.random.default_rng(seed)
    par = R['par']; ttab = R['ttab']; panel = R['panel']
    mem = R['P']['mem'].set_index('member_id')['status'].to_dict()
    last = state_at_cut(panel, R['members'])
    live = [m for m in R['members'] if mem.get(m) == 'active' and last.loc[m, 't'] == CUT_M]
    lset = set(live)
    done = sum(1 for m in R['members'] if m not in lset and last.loc[m, 'k'] >= 12)
    rows = [(int(last.loc[m, 'k']), int(last.loc[m, 'tid']), int(last.loc[m, 'tj']) if last.loc[m, 'tid'] >= 0 else -1,
             last.loc[m, 'state']) for m in live]
    tids = sorted({r[1] for r in rows if r[1] >= 0})
    A = panel[panel.state == 'A']
    nA = A.groupby(A.k.clip(upper=KMAX)).size().to_dict()
    tt = ttab.reset_index()
    H = LAST_M - CUT_M
    out = []; mon = []
    for rep in range(n_rep):
        if inputs_fixed:
            q, d1, d2, h = par['q'], par['d1'], par['d2'], par['h']
        else:
            boot = tt.iloc[rng.integers(0, len(tt), len(tt))].set_index('tid')
            q = tutor_stops(boot)
            d1 = rng.binomial(par['n_s1'], par['d1']) / par['n_s1']
            d2 = rng.binomial(par['n_s2'], par['d2']) / par['n_s2']
            h = {k: rng.binomial(nA.get(min(k, KMAX), 1000), par['h'][k]) / nA.get(min(k, KMAX), 1000) for k in par['h']}
        qf = lambda j: q[j] if j <= 12 else q['late']

        def draw_stop(tj0):
            for step in range(1, H + 1):
                if rng.random() < qf(tj0 + step):
                    return step
            return None
        stop_at = {tid: draw_stop(int(CUT_M - ttab.loc[tid, 'min'])) for tid in tids}
        kept = done
        paying = np.zeros(H + 1)
        for (k0, tid, tj0, st0) in rows:
            if clustered:
                sm = stop_at.get(tid) if tid >= 0 else None
            else:
                sm = draw_stop(tj0) if tid >= 0 else None
            alive = True; state = 'S2' if st0 == 'S1' else 'A'; vet = tid < 0
            for step in range(1, H + 1):
                k = k0 + step
                if state == 'A' and not vet and sm == step:
                    state = 'S1'
                elif state == 'A' and vet and rng.random() < q['late']:
                    state = 'S1'
                paying[step] += 1
                if k == 12:
                    kept += 1
                hk = h[min(k, KMAX)]
                if state == 'S1':
                    c = shock(hk, d1, par['base']); nxt = 'S2'
                elif state == 'S2':
                    c = shock(hk, d2, par['base']); nxt = 'A'; vet = True
                else:
                    c = hk; nxt = 'A'
                if rng.random() < c:
                    break
                state = nxt
        out.append(kept); mon.append(paying)
    lo, hi = float(np.percentile(out, 10)), float(np.percentile(out, 90))
    if monthly:
        mon = np.array(mon)
        bands = {CUT_M + s: (float(np.percentile(mon[:, s], 10)), float(np.percentile(mon[:, s], 90))) for s in range(1, H + 1)}
        return lo, hi, out, bands
    return lo, hi, out


def joining_split(R):
    ch = R['ch']; fc = ch[ch.k == 1].set_index('member_id')
    mon = {m: fc.loc[m, 't'] for m in R['members']}
    res = {}
    for t, lab in ((month_index(2026, 9), 'September'), (month_index(2026, 10), 'October')):
        ms = [m for m in R['members'] if mon[m] == t]
        e = sum(R['by'][m][0] for m in ms)
        monthly = defaultdict(float)
        for m in ms:
            for tt_, p in R['by'][m][1].items():
                monthly[tt_] += p
        res[lab] = dict(members=len(ms), exp12=e, share=e / len(ms), monthly=dict(monthly))
    return res


def main():
    R = run()
    n = len(R['members'])
    print('campaign members', n, 'cost', R['cost'])
    print('expected twelfth-month members %.1f, share %.4f' % (R['exp12'], R['exp12'] / n))
    print('cost per twelfth-month member %.2f; per paid member %.2f' % (R['cost']['total_eur'] / R['exp12'], R['cost']['total_eur'] / n))
    par = R['par']
    print('d1 %.3f d2 %.3f base %.4f post %.2f n_s1 %d' % (par['d1'], par['d2'], par['base'], par['post'], par['n_s1']))
    print('q', {j: round(par['q'][j], 3) for j in range(1, 13)}, 'late', round(par['q']['late'], 4), 'pooled', round(par['q']['pooled_tutor_months'], 4), 'mw', round(par['member_weighted_stop'], 4))
    js = joining_split(R)
    for lab, v in js.items():
        print(lab, v['members'], round(v['exp12'], 1), round(v['share'], 4), {month_str(t): round(p, 1) for t, p in sorted(v['monthly'].items())})
    lo, hi, _ = predictive_range(R, n_rep=200)
    lo2, hi2, _ = predictive_range(R, n_rep=200, clustered=False, seed=7)
    print('80%% range clustered %.0f to %.0f; independent tutors %.0f to %.0f' % (lo, hi, lo2, hi2))
    # tutor teaching month at the cut of the live campaign members
    last = state_at_cut(R['panel'], R['members'])
    live = last[(last.t == CUT_M)]
    print('live campaign members', len(live), 'tutor teaching month at cut', live.tj.value_counts().sort_index().head(14).to_dict())


if __name__ == '__main__':
    main()
