"""Generator assertions for task1. Exit 1 on any failure.

    python3 task1/generator/checks.py

Reads the cut pack (target/), the clean truth (truth.json), figures.json and the golden run. Every SF row of the
design note's fork table is asserted here by its id; the Sulfur block's labels start R1 to R6.
"""
import csv
import datetime as dt
import glob
import hashlib
import json
import os
import re
import sys
import zipfile

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import golden as G            # noqa: E402
import rivals as V            # noqa: E402
from common import *          # noqa: E402,F401,F403

RESULTS = []


def ok(cond, label, detail=''):
    RESULTS.append((bool(cond), label, detail))
    print('%s  %s%s' % ('PASS' if cond else 'FAIL', label, ('  [' + str(detail) + ']') if detail else ''))


def call_of(exp12, cost):
    return 'hold' if cost / exp12 > G.BAR_EUR else 're-run'


def main():
    F = json.load(open(os.path.join(HERE, 'figures.json')))
    T = json.load(open(os.path.join(HERE, 'truth.json')))
    meta = json.load(open(os.path.join(TASK, 'metadata.json')))
    R = G.run()
    n = len(R['members']); cost = R['cost']['total_eur']; e = R['exp12']
    files = sorted(os.listdir(TARGET))

    # ---------------------------------------------------------------- input gates
    ok(len(files) >= 10, 'input gate: ten or more usable files', len(files))
    cats = {'spreadsheet' if f.endswith(('.csv', '.xlsx')) else 'text' if f.endswith(('.pdf', '.json', '.txt', '.md')) else 'other' for f in files}
    ok(len(cats - {'other'}) >= 2, 'input gate: two or more file categories', sorted(cats))
    rows = {f: sum(1 for _ in open(os.path.join(TARGET, f), encoding='utf-8')) - 1 for f in files if f.endswith('.csv')}
    ok(max(rows.values()) >= 20000, 'input gate: a CSV of 20,000 rows or more', max(rows, key=rows.get))
    tut = os.path.join(TARGET, 'tutor_directory_2026-11-03.csv')
    lines = rows['tutor_directory_2026-11-03.csv']
    ok(lines >= 550, 'input gate: a CSV of 10 to 20 printed pages or more (55 lines a page)', '%d rows, about %d pages' % (lines, lines // 55))
    ok(not any(re.search(r'readme|dictionary|codebook|field.?notes|manifest|notes', f, re.I) for f in files),
       'no file describes the pack')
    ok(not any(re.search(r'distract|trap|decoy|answer|key', f, re.I) for f in files), 'no file name names its role')
    dis = [p.split('/', 1)[1] for p in meta['distractor_files']]
    ok(len(dis) >= 2 and all(d in files for d in dis), 'two distractors declared in metadata.json only', dis)
    ok(all('license' in x and 'source' in x and 'pulled_on' in x for x in meta['files']) and len(meta['files']) == len(files),
       'metadata.json records source, licence and pull date for every file')
    # distractors unused: the golden reads neither
    import inspect
    src = inspect.getsource(G)
    ok(all(re.sub(r'_.*', '', d)[:7] not in ('eurosta', 'nps_in_') or True for d in dis) and
       'eurostat' not in src.split('FILE_NAMES')[0] and "P['nps']" not in src and "P['eurostat']" not in src,
       'the golden reads neither distractor')

    # ---------------------------------------------------------------- R1 the field's raw material
    les_cols = list(pd.read_csv(os.path.join(TARGET, 'lesson_activity_monthly_2022-01_2026-10.csv'), nrows=1).columns)
    tut_cols = list(pd.read_csv(tut, nrows=1).columns)
    mem_cols = list(pd.read_csv(os.path.join(TARGET, 'members_export_2026-11-03.csv'), nrows=1).columns)
    bad = [c for c in les_cols + tut_cols + mem_cols if re.search(r'tenure|start|joined|onboard|hired|left|stop|depart|since|first_|last_|tutor_id', c, re.I)]
    ok(bad == ['tutor_id', 'tutor_id'] or set(bad) == {'tutor_id'}, 'R1 no shipped column holds a tutor\'s teaching months or stop date', bad)
    ok('tutor_id' not in mem_cols, 'R1 the member export carries no tutor; the link is in the lesson log only')
    ok(R['par']['n_s1'] > 3000 and len(R['ttab']) > 700, 'R1 the decisive step reads member months and tutor histories at their own grain',
       '%d member months with a tutor stop, %d tutors' % (R['par']['n_s1'], len(R['ttab'])))

    # ---------------------------------------------------------------- the ladder on the pack
    routes = V.all_routes(R)
    get = lambda key: [v for k, (v, s) in routes.items() if k.startswith(key)][0]
    shallow = {k: v for k, (v, s) in routes.items() if k.split()[0] in ('R0', 'R0r', 'R1s', 'R1e', 'R0f', 'R0b', 'R2', 'R2b')}
    deep = {k: v for k, (v, s) in routes.items() if (k.startswith('R3 ') and 'twice' not in k and 'one shocked' not in k)
            or (k.startswith('R3w') and 'tutors and months from 2023' not in k and 'tutors from 2023' not in k)}
    launch_dropped = {k: v for k, (v, s) in routes.items() if k.startswith('R3w') and ('tutors from 2023' in k or 'tutors and months from 2023' in k)}
    for k, v in shallow.items():
        c = cost / v
        ok(c < G.BAR_EUR * 0.92, 'R3a/R6 shallow route files the re-run at least 8 per cent inside the bar: ' + k, round(c, 1))
    for k, v in deep.items():
        c = cost / v
        ok(c > G.BAR_EUR * 1.10, 'R6 standing route files the hold at least 10 per cent outside the bar: ' + k, round(c, 1))
    ok(call_of(get('R0 '), cost) == 're-run', 'R3a the analyst test: the membership-month curve books the re-run', round(cost / get('R0 '), 1))
    ok(abs(get('R3 tutor-linked') - e) < 1e-6 and call_of(e, cost) == 'hold', 'R3b the easy route with only the decisive step changed files the golden')
    spread = max(deep.values()) - min(deep.values())
    ok(spread < 0.025 * e, 'standing family spread under 2.5 per cent of the golden', round(spread, 1))
    ok((get('R0 ') - e) > 4 * spread, 'dominance: the decisive move is worth over four times the standing spread', '%.1f against %.1f' % (get('R0 ') - e, spread))
    # R4 every chain link
    ok(call_of(get('R0 '), cost) == 're-run', 'R4 link 1-2 skipped (no tutor link, no stop shock): the re-run')
    ok(call_of(get('R2b'), cost) == 're-run', 'R4 link 3 skipped with the member-weighted stop rate: the re-run', round(cost / get('R2b'), 1))
    c2c = get('R2c'); ok(abs(c2c - e) / e > 0.10, 'R4 link 3 skipped with the tutor-month stop rate: twelfth-month members off by over 10 per cent', round(c2c, 1))
    dbl = get('R3 stops counted twice'); ok(abs(dbl - e) / e > 0.2, 'R4 link 5 skipped (stops counted twice): twelfth-month members off by over 20 per cent', round(dbl, 1))
    one = get('R3 one shocked'); ok(abs(one - e) / e > 0.08, 'R4 the second shocked charge skipped: twelfth-month members off by over 8 per cent', round(one, 1))
    ok(call_of(get('R2 curve'), cost) == 're-run', 'R4 only the members whose tutor already stopped: the re-run')
    # R5 one fact
    ok(call_of(get('R2b'), cost) == 're-run', 'R5 the one-fact hint executed literally (members leave when the tutor stops, one member-weighted rate) still books the re-run')
    # snapshot reduced forms land on the hold and are ordered by fit
    for k, v in routes.items():
        if k.startswith('R3r') or k.startswith('R2s'):
            ok(call_of(v[0], cost) == 'hold', 'R6 reduced-form route files the hold: ' + k, round(cost / v[0], 1))
    lin = [k for k in routes if 'linear' in k][0]; ban = [k for k in routes if 'banded' in k][0]
    ll = lambda k: float(re.search(r'loglik (-?[0-9.]+)', k).group(1))
    ok(2 * (ll(ban) - ll(lin)) > 100, 'R6 the linear teaching-month form is ruled out by fit against the banded form', round(2 * (ll(ban) - ll(lin)), 1))

    # ---------------------------------------------------------------- the deciding facts the data must show
    q = R['par']['q']
    ok(max(q[j] for j in (4, 5, 6)) > 5 * q['late'] and q[1] < 0.06, 'the stopping hump: teaching months 4 to 6 above five times the late rate', {j: round(q[j], 3) for j in (1, 4, 5, 6)})
    ok(R['par']['d1'] > 8 * R['par']['base'] and R['par']['d2'] > 3 * R['par']['base'], 'the stop shock: the stop month over eight times and the next over three times an ordinary month')
    ok(F['live_with_new_tutor_pct'] > 75, 'the AUT26 exposure: over three in four live AUT26 members with tutors in teaching months 0 to 1', F['live_with_new_tutor_pct'])
    cal = F['calibration']
    ok(cal['1-3']['ratio'] > 1.12 and cal['4-9']['ratio'] > 1.12 and cal['13+']['ratio'] < 0.95, 'the member-level validation: the curve misses young-tutor members by over 12 per cent', cal)
    bs, bo = F['backtest_spr25'], F['backtest_sepoct25']
    ok(bs['curve_pct'] <= bs['actual_pct'] + 2 and bo['curve_pct'] <= bo['actual_pct'] + 2, 'Back-test: the curve is not optimistic on SPR25 or last autumn\'s joiners', (bs, bo))

    # ---------------------------------------------------------------- semantic forks
    # SF1 the campaign window in Berlin days against UTC days
    mu = G.campaign_members(R['ch'], R['P']['att'], berlin=False)
    late = set(T['aut26_late_berlin'])
    ok(late <= set(mu) and not (late & set(R['members'])), 'SF1 the six sign-ups after midnight Berlin on 31 October are outside the Berlin window only')
    eu = G.project_group(R['panel'], R['P']['mem'], mu, R['par'], R['qf'])[0]
    ok(call_of(eu, cost) == 'hold' and abs(eu - e) < 15, 'SF1 a UTC window files the same call and the same twelfth-month members at the rounding', round(eu, 1))
    # SF2 refunded first charges are not paid members
    b = R['P']['bill'].drop_duplicates(subset=['event_id'])
    refunded = set(b[(b.event_type == 'refund')]['refund_of'])
    ch_all = b[(b.event_type == 'charge') & (b.status == 'succeeded')]
    first_ref = ch_all[ch_all.event_id.isin(refunded)]
    tagged = set(R['P']['att'][R['P']['att'].utm_campaign.str.lower().str.contains('aut26')]['account_id'])
    n_ref = len(set(first_ref.member_id) & tagged)
    ok(n_ref > 50 and call_of(e, cost) == 'hold', 'SF2 counting cooling-off refunds as paid members moves only the cost per paid member, not the call', n_ref)
    # SF3 retries count once; partial refunds still count
    ok(R['ch'].groupby(['member_id', 't']).size().max() == 1, 'SF3 one collected charge per member and month after retries')
    # SF4 cost net of VAT, credit note deducted, GBP at the ECB rate of the issue date
    c_agency = cost - R['cost']['media_eur'] + (R['cost']['media_eur_lines'] + R['cost']['credit_eur'] + R['cost']['media_gbp_net'] * 1.17)
    ok(call_of(e, c_agency) == 'hold', 'SF4 GBP at the agency\'s 1.17 planning rate files the same call', round(c_agency / e, 1))
    ok(call_of(e, cost * 1.19) == 'hold' and call_of(e, cost - R['cost']['credit_eur']) == 'hold', 'SF4 gross of VAT or without the credit note files the same call')
    # SF5 discounts against the list price of the plan charged
    ok(call_of(e, cost - R['cost']['discounts_eur']) == 'hold' and (cost - R['cost']['discounts_eur']) / e > G.BAR_EUR * 1.05, 'SF5 leaving the discounts out files the same call, at least 5 per cent outside the bar', round((cost - R['cost']['discounts_eur']) / e, 1))
    # SF6 expected number is the mean of the predictive distribution
    lo, hi, draws = G.predictive_range(R, n_rep=300, seed=5)
    ok(call_of(float(np.median(draws)), cost) == 'hold', 'SF6 the median twelfth-month members files the same call', np.median(draws))
    # SF7 members paying in a month: a collected charge in that calendar month (one per member per month, SF3)
    ok(all(v >= 0 for v in F['monthly']['All'].values()) and F['monthly']['All']['2026-11'] <= F['live_at_cut'] + 25, 'SF7 November 2026 paying members cannot exceed the members live at the cut')
    # SF8 the 80 per cent range is the central 80 per cent; SF10 cost per twelfth-month member is cost over the expected count
    ok(F['range80_cost_eur'][0] <= F['cost_per_12m_eur'] <= F['range80_cost_eur'][1], 'SF8 the cost range brackets the point figure')
    ratio_of_exp = float(np.mean([cost / d for d in draws]))
    ok(call_of(cost / ratio_of_exp, cost) == 'hold' and abs(ratio_of_exp - cost / e) < 15, 'SF10 the expected ratio and the ratio of expectations file the same call', round(ratio_of_exp, 1))
    # SF9 joining month is the month of the first collected charge
    ok(F['by_joining']['September']['members'] + F['by_joining']['October']['members'] == n, 'SF9 the joining months partition the campaign members')
    # SF11 the bar: at or below EUR 800 against below
    ok(abs(cost / e - G.BAR_EUR) > 50, 'SF11 the cost is far from the bar, so at-or-below against below cannot matter', round(cost / e, 1))
    # SF12 rounding once to the nearest 50: graded figures mid-bin for every standing route
    for key, val in (('exp12', [v for v in deep.values()]),):
        bins = {int(round(v / 50.0)) * 50 for v in val}
        ok(len(bins) == 1, 'SF12 every standing route rounds the twelfth-month members to one figure', sorted(bins))
    cbins = {int(round(cost / v / 25.0)) * 25 for v in deep.values()}
    ok(len(cbins) == 1, 'SF12 every standing route rounds the cost per twelfth-month member to one figure', sorted(cbins))
    fbins = {int(round(G.BAR_EUR * v / n / 25.0)) * 25 for v in deep.values()}
    ok(len(fbins) == 1, 'SF12 every standing route rounds the cost per paid member that meets the bar exactly to one figure', sorted(fbins))
    # SF12 the two estimation windows that drop the 2022 launch tutors: the launch tutors stop like later ones
    from scipy.stats import chi2
    tt = R['ttab']; qa = G.tutor_stops(tt[tt['min'] < 12]); qb = G.tutor_stops(tt[tt['min'] >= 12]); lr = 0.0
    for lo_, hi_ in ((1, 3), (4, 6), (7, 9), (10, 12), (13, 99)):
        rs = [sum(q_['risk'].get(j, 0) for j in range(lo_, hi_ + 1)) for q_ in (qa, qb)]
        ss = [sum(q_['stop'].get(j, 0) for j in range(lo_, hi_ + 1)) for q_ in (qa, qb)]
        p0 = sum(ss) / sum(rs)
        lr += sum(s_ * np.log(s_ / r_ / p0) + (r_ - s_) * np.log((1 - s_ / r_) / (1 - p0)) for r_, s_ in zip(rs, ss) if 0 < s_ < r_)
    ok(chi2.sf(2 * lr, 5) > 0.2 and all(call_of(v, cost) == 'hold' for v in launch_dropped.values()),
       'SF12 dropping the 2022 launch tutors discards tutors who stop like later ones (and files the same call)',
       'LR %.2f on 5 df, p %.3f; %s' % (2 * lr, chi2.sf(2 * lr, 5), {k[-28:]: round(cost / v, 1) for k, v in launch_dropped.items()}))
    # the clean truth: the generator's own world run forward from the cut, ten draws of the months still to come
    import world as Wd
    W0 = Wd.build_world(SEED)
    inv = {v: int(k) for k, v in T['member_ids'].items()}
    idx = [inv[m] for m in R['members']]
    fw = []
    for sd in range(10):
        V_ = Wd.continue_world(W0, 9000 + sd)
        fw.append(sum(1 for x in idx if V_.M['paid'][x] >= 12))
    fwm = float(np.mean(fw))
    ok(F['range80_cost_raw'][0] <= cost / fwm <= F['range80_cost_raw'][1] and call_of(fwm, cost) == 'hold'
       and not (F['range80_cost_raw'][0] <= cost / get('R0 ') <= F['range80_cost_raw'][1]),
       'truth: the world run forward lands inside the golden\'s 80 per cent range and files the hold; the default path lands outside it',
       'mean %.1f twelfth-month members (sd %.1f), EUR %.1f; default path EUR %.1f' % (fwm, float(np.std(fw, ddof=1)), cost / fwm, cost / get('R0 ')))
    # SF14 one continuous membership: no account has a billing period with no collected attempt and a later collected one
    bc = R['P']['bill'].drop_duplicates(subset=['event_id'])
    bc = bc[bc.event_type == 'charge']
    paid_p = bc.groupby(['member_id', 'billing_period_start']).status.apply(lambda x: (x == 'succeeded').any())
    dead_p = paid_p[~paid_p].reset_index()
    last_p = bc[bc.status == 'succeeded'].groupby('member_id')['billing_period_start'].max()
    restarts = sum(1 for mm, pp in zip(dead_p.member_id, dead_p.billing_period_start) if mm in last_p.index and pp < last_p[mm])
    ok(len(dead_p) > 1000 and restarts == 0,
       'SF14 every billing period with no collected attempt ends its account\'s charges, so standard 3.3\'s restart clause moves nothing',
       '%d dead periods, %d followed by a later collected one' % (len(dead_p), restarts))
    # SF8 the ranges with the inputs held fixed: the 80 per cent range is the same, the 90 per cent upper end moves a bin
    _, _, dfx = G.predictive_range(R, n_rep=G.N_REP, seed=601, inputs_fixed=True)
    q25 = lambda x: int(round(x / 25.0)) * 25
    fx80 = [q25(cost / np.percentile(dfx, 90)), q25(cost / np.percentile(dfx, 10))]
    fx90 = [q25(cost / np.percentile(dfx, 95)), q25(cost / np.percentile(dfx, 5))]
    ok(fx80 == F['range80_cost_eur'] and fx90[0] == F['range90_cost_eur'][0] and fx90[1] < F['range90_cost_eur'][1],
       'SF8 inputs held fixed give the same 80 per cent range and a 90 per cent range one bin short at the top (ruled out: '
       'a forecast\'s range carries its inputs\' estimation error)', (fx80, fx90))
    # SF13 the cost per paid member that meets EUR 800 exactly: a level at the nearest 25; the bound reading floors it
    lvl = G.BAR_EUR * e / n
    ok(F['flip_cost_per_paid_eur'] == int(round(lvl / 25.0)) * 25 and 'met EUR 800 exactly' in open(os.path.join(TASK, 'prompt.txt')).read()
       and call_of(e, cost) == 'hold',
       'SF13 the cost per paid member that meets the bar exactly is a level at the nearest 25 (a floored bound files the same call)',
       (round(lvl, 2), F['flip_cost_per_paid_eur'], int(lvl // 25) * 25))
    # R7 the 80 and 90 per cent ranges: tutor by tutor, at the draws the deliverables use, inside their rounding with margin
    for lev in ('80', '90'):
        rr = F['range%s_cost_raw' % lev]
        ok(min(abs(x - (round(x / 25.0) * 25 + 12.5)) for x in rr) > 4 and min(abs(x - (round(x / 25.0) * 25 - 12.5)) for x in rr) > 4,
           'R7 both ends of the %s per cent range sit over EUR 4 inside their rounding' % lev, rr)
        ok(F['range%s_cost_eur' % lev][0] != F['range%s_cost_independent' % lev][0] and
           F['range%s_cost_eur' % lev][1] != F['range%s_cost_independent' % lev][1],
           'R7 members drawn one at a time give a different figure at both ends of the %s per cent range' % lev,
           (F['range%s_cost_eur' % lev], F['range%s_cost_independent' % lev]))
    # the reduced forms: a classifier of the twelfth charge sees only members who joined by November 2025
    ok(F['rematch_young_2022_pct'] > 40 and F['rematch_young_since_2023_pct'] < 2,
       'the 2022 launch months moved members to tutors in their first nine months; since 2023 almost never',
       (F['rematch_young_2022_pct'], F['rematch_young_since_2023_pct']))

    # ---------------------------------------------------------------- R2 mess neutrality, one item at a time
    def rerun(bill=None, att=None, les=None):
        P = dict(R['P'])
        if bill is not None: P['bill'] = bill
        if att is not None: P['att'] = att
        if les is not None: P['les'] = les
        ch = G.collected_charges(P['bill']) if bill is not None else R['ch']
        mem = G.campaign_members(ch, P['att'])
        l, tt = G.tutor_table(P['les'], P['tut']) if les is not None else (R['l'], R['ttab'])
        pn = G.member_panel(ch, P['mem'], l, tt) if (bill is not None or les is not None) else R['panel']
        par = G.estimate(pn, tt)
        qf = lambda j: par['q'][j] if j <= 12 else par['q']['late']
        ex = G.project_group(pn, P['mem'], mem, par, qf)[0]
        cst = G.campaign_cost(ch, P['wb'], R['rates'], mem, P['plans'])['total_eur']
        return ex, cst, len(mem)
    bill = R['P']['bill']
    # R2a webhook replays left in: the replays repeat whole rows, so a row-level drop handles them; left in they double a charge
    ex, cst, nm = rerun(bill=bill.drop_duplicates())
    ok(call_of(ex, cst) == 'hold', 'R2 replays dropped by whole row only: same call', (round(ex, 1), nm))
    # R2b refunds ignored
    ex, cst, nm = rerun(bill=bill[bill.event_type != 'refund'])
    ok(call_of(ex, cst) == 'hold' and abs(ex - e) < 25, 'R2 refunds ignored: same call, twelfth-month members within the rounding', (round(ex, 1), nm))
    # R2c tutor ids: one format in the lesson log and the directory (the 2025 migration kept the ids)
    ok(R['P']['les'].tutor_id.str.match(r'^T-[0-9]{6}$').all(), 'R2 tutor ids carry one format, so no cleaning step can split a tutor')
    # R2d campaign codes matched exactly in upper case only
    att2 = R['P']['att'].copy()
    att2['utm_campaign'] = att2.utm_campaign.where(att2.utm_campaign.str.contains('AUT26'), att2.utm_campaign.str.replace('aut26', 'xxxx', case=True))
    ex, cst, nm = rerun(att=att2)
    ok(call_of(ex, cst) == 'hold', 'R2 campaign codes matched case-sensitively: same call (the count moves with the population)', (round(ex, 1), nm))
    # R2e amounts read from the old column only
    bill3 = bill.copy(); bill3['amount_minor'] = ''
    ex, cst, nm = rerun(bill=bill3)
    ok(call_of(ex, cst) == 'hold', 'R2 amount_minor ignored: same call', round(cst, 1))
    # R3c no plant
    ok(not any(re.search(r'decoy|staff draft|briefing', open(os.path.join(TARGET, f), errors='ignore').read()[:20000], re.I)
               for f in files if f.endswith(('.csv', '.json'))), 'R3c no decoy, draft or briefing ships')

    # ---------------------------------------------------------------- realism sweep
    mem = pd.read_csv(os.path.join(TARGET, 'members_export_2026-11-03.csv'), dtype=str)
    ids = mem.member_id.str[2:].astype(int).sort_values().diff().dropna()
    ok(ids.nunique() > 10, 'realism: member ids are not an arithmetic sequence', ids.nunique())
    tids = pd.read_csv(tut, dtype=str).tutor_id.str[2:].astype(int).sort_values().diff().dropna()
    ok(tids.nunique() > 3, 'realism: tutor ids are not an arithmetic sequence', tids.nunique())
    names = pd.read_csv(tut, dtype=str).display_name
    ok(names.nunique() > 0.9 * len(names), 'realism: tutor display names are not recycled', names.nunique())
    sig = pd.to_datetime(mem.created_at).dt.to_period('M').value_counts()
    ok(sig.nunique() > 0.8 * len(sig), 'realism: monthly sign-ups are not uniform')
    ok(round(cost) % 1000 != 0 and n % 100 != 0, 'realism: no round headline totals', (round(cost, 2), n))
    last_ts = pd.to_datetime(R['P']['bill'].created_at, utc=True).max()
    ok(last_ts.date() <= PULL_DATE, 'realism: no billing event after the pull date', last_ts)
    from pypdf import PdfReader
    for f in files:
        if f.endswith('.pdf'):
            m = PdfReader(os.path.join(TARGET, f)).metadata
            ok(m.get('/Subject') not in (None, '', '(unspecified)'), 'PDF %s carries a real Subject' % f)
            ok((m.get('/Creator') or '') == 'Writer' and (m.get('/Producer') or '').startswith('LibreOffice')
               and b'ReportLab' not in open(os.path.join(TARGET, f), 'rb').read(),
               "PDF %s is the office's LibreOffice Writer export, no library named" % f)
            ok((m.get('/Author') or '') == 'Corvane Sprachen GmbH', 'PDF %s names its issuer in Author only' % f)
            ok(str(m.get('/CreationDate', '')).startswith('D:2025'), 'PDF %s is dated in the fiction' % f, m.get('/CreationDate'))
            # H13: no text past the margin; H25: a strict reader and two independent extractors read the same words
            import fitz, pdfplumber, subprocess
            pdoc = fitz.open(os.path.join(TARGET, f))
            edge = [(i + 1, round(b[2])) for i, pg in enumerate(pdoc) for b in pg.get_text('blocks') if b[2] > pg.rect.width - 30]
            ok(not edge, 'PDF %s keeps every line inside the page margin' % f, edge)
            words = lambda t: set(re.findall(r'[a-z]{4,}', t.lower()))
            w_strict = words(' '.join(p.extract_text() for p in PdfReader(os.path.join(TARGET, f), strict=True).pages))
            with pdfplumber.open(os.path.join(TARGET, f)) as pl:
                w_plumb = words(' '.join((p.extract_text() or '') for p in pl.pages))
            w_pop = words(subprocess.run(['pdftotext', '-layout', os.path.join(TARGET, f), '-'], capture_output=True, text=True).stdout)
            ok(w_strict == w_plumb and len(w_strict ^ w_pop) <= 2 and {'twelfth', 'berlin', 'credit', 'expected'} <= w_pop,
               'PDF %s reads the same in a strict reader and two independent extractors' % f, (len(w_strict), len(w_strict ^ w_pop)))
    for f in files:
        if f.endswith(('.xlsx', '.docx')):
            z = zipfile.ZipFile(os.path.join(TARGET, f))
            app = z.read('docProps/app.xml').decode() if 'docProps/app.xml' in z.namelist() else ''
            core = z.read('docProps/core.xml').decode() if 'docProps/core.xml' in z.namelist() else ''
            ok(not re.search(r'openpyxl|python-docx|generated by', app + core, re.I), 'OOXML %s carries no writing library' % f)
            ok(re.search(r'<AppVersion>16\.', app) is not None, 'OOXML %s carries an application version that matches its application' % f)
            ok(re.search(r'2026-11-0[1-3]T', core) is not None, 'OOXML %s is dated at the pull, not the build clock' % f)
    ok(all(not re.search('—', open(os.path.join(TARGET, f), encoding='utf-8', errors='ignore').read()) for f in files if f.endswith(('.csv', '.json'))),
       'no em dash in any text file')
    # persona names drawn by the guard
    card = json.load(open(os.path.join(os.path.dirname(TASK), '.claude', 'skills', 'fingerprint', 'cards', 'task1.json')))
    ok(set(card['world']['people']) == {'Caroline Ritter', 'Marit Klemt', 'Veit Stadelmann'}, 'personas are the ones drawn with guard.py names')

    # ---------------------------------------------------------------- figures agree everywhere
    ok(F['exp12'] == int(round(e / 50.0)) * 50 and F['cost_per_12m_eur'] == int(round(cost / e / 50.0)) * 50, 'figures.json carries the golden at the asked rounding')
    ok(F['cost_per_12m_eur'] > G.BAR_EUR and F['default_cost_per_12m_eur'] < G.BAR_EUR, 'the call and the default path sit on opposite sides of the bar')
    nfail = sum(1 for r in RESULTS if not r[0])
    print('\n%d assertions, %d failed' % (len(RESULTS), nfail))
    return 1 if nfail else 0


if __name__ == '__main__':
    sys.exit(main())
