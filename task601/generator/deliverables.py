"""figures.json and the two golden deliverables, written from golden.run().

    python3 task601/generator/deliverables.py
"""
import datetime as dt
import json
import os
import sys
from collections import defaultdict

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import golden as G            # noqa: E402
import rivals as V            # noqa: E402
from common import *          # noqa: E402,F401,F403

MONTHS = list(range(G.CUT_M + 1, G.LAST_M + 1))
MLABEL = {t: dt.date(*month_of(t), 1).strftime('%b %Y') for t in MONTHS}


def r10(x):
    return int(round(x / 10.0)) * 10


def r50(x):
    return int(round(x / 50.0)) * 50


def r25(x):
    return int(round(x / 25.0)) * 25


# ------------------------------------------------------------------------------------------------ validation
def backtest(R, members, BC):
    """Project a past cohort from cut BC on the membership-month curve and on the tutor-linked projection, both
    estimated on months up to BC, against what the cohort actually kept to the twelfth charge."""
    p = R['panel']
    hist = p[p.t <= BC]
    lastk = p.groupby('member_id')['k'].max(); lastt = p.groupby('member_id')['t'].max()
    actual = float(np.mean([lastk[m] >= 12 for m in members]))
    h0 = G.kcurve(hist)
    l, ttab = R['l'], R['ttab']
    tt = ttab.copy()
    tt['stopped'] = tt['stopped'] & (tt['max'] < BC)
    tt['max'] = tt['max'].clip(upper=BC)
    tt = tt[tt['min'] <= BC]
    par = G.estimate(hist, tt)
    par['q'] = G.tutor_stops(tt, cut=BC)
    qf = lambda j: par['q'][j] if j <= 12 else par['q']['late']
    at = hist.sort_values('k').groupby('member_id').last()
    c0 = c3 = 0.0
    for m in members:
        r = at.loc[m]
        if lastt[m] <= BC and not (lastt[m] == BC and lastk[m] > r['k']):
            alive = lastt[m] > BC
        alive = lastt[m] > BC
        if not alive:
            v = 1.0 if r['k'] >= 12 else 0.0
            c0 += v; c3 += v
            continue
        s = 1.0
        for k in range(int(r['k']) + 1, 12):
            s *= 1 - h0[min(k, G.KMAX)]
        c0 += s
        _, p12 = G.project_member(int(r['k']), int(r['t']), int(r['tj']) if r['tid'] >= 0 else None, r['state'],
                                  par, qf, horizon=int(r['t']) + 12)
        c3 += p12 if p12 is not None else 0.0
    n = len(members)
    return dict(n=n, actual=actual, curve=c0 / n, linked=c3 / n)


def calibration(R, first=12, last=50, step=3):
    """Six-month cancellations after a snapshot, against the membership-month curve, by the tutor's teaching month."""
    p = R['panel']; h0 = G.kcurve(p)
    lastt = p.groupby('member_id')['t'].max(); status = R['P']['mem'].set_index('member_id')['status']
    cancel_t = {m: (lastt[m] if status.get(m) != 'active' else None) for m in lastt.index}
    rows = []
    for BC in range(first, last + 1, step):
        snap = p[p.t == BC]
        for m, k, tj, tid in zip(snap.member_id, snap.k, snap.tj, snap.tid):
            if lastt[m] == BC and cancel_t[m] is not None:
                continue
            ct = cancel_t[m]
            obs = int(ct is not None and BC < ct <= BC + 6)
            s = 1.0
            for kk in range(int(k) + 1, int(k) + 7):
                s *= 1 - h0[min(kk, G.KMAX)]
            # the tutor's teaching month counted from 1 (their first lesson month is the first)
            band = 'none' if tid < 0 else ('1-3' if tj <= 2 else '4-9' if tj <= 8 else '10-12' if tj <= 11 else '13+')
            rows.append((band, obs, 1 - s))
    c = pd.DataFrame(rows, columns=['band', 'obs', 'exp'])
    g = c.groupby('band').agg(n=('obs', 'size'), obs=('obs', 'sum'), exp=('exp', 'sum'))
    g['ratio'] = g['obs'] / g['exp']
    return g


# ------------------------------------------------------------------------------------------------ figures
def figures(R):
    n = len(R['members']); cost = R['cost']; par = R['par']
    js = G.joining_split(R)
    lo, hi, draws = G.predictive_range(R, n_rep=G.N_REP, seed=601)
    lo_i, hi_i, draws_i = G.predictive_range(R, n_rep=G.N_REP, seed=611, clustered=False)
    p5, p95 = float(np.percentile(draws, 5)), float(np.percentile(draws, 95))
    p5i, p95i = float(np.percentile(draws_i, 5)), float(np.percentile(draws_i, 95))
    e12 = R['exp12']
    r0 = V.r0_curve(R)
    last = G.state_at_cut(R['panel'], R['members'])
    live = last[last.t == G.CUT_M]
    status = R['P']['mem'].set_index('member_id')['status']
    live = live[[status.get(m) == 'active' for m in live.index]]
    new_t = int(((live.tj >= 0) & (live.tj <= 1) & (live.tid >= 0)).sum())
    spr = G.campaign_members(R['ch'], R['P']['att'], code='SPR25', first=dt.date(2025, 3, 1), last=dt.date(2025, 4, 30))
    ch = R['ch']; fc = ch[ch.k == 1].set_index('member_id')
    tagged = set(R['P']['att'][R['P']['att'].utm_campaign.str.lower().str.contains('aut26|spr25')]['account_id'])
    sep_oct_25 = [m for m in fc.index if fc.loc[m, 't'] in (G.month_index(2025, 9), G.month_index(2025, 10)) and m not in tagged]
    bt_spr = backtest(R, spr, G.month_index(2025, 6))
    bt_so = backtest(R, sep_oct_25, G.month_index(2025, 12))
    cal = calibration(R)
    monthly = {}
    for lab in ('September', 'October'):
        monthly[lab] = {month_str(t): r50(js[lab]['monthly'].get(t, 0.0)) for t in MONTHS}
    monthly['All'] = {month_str(t): r50(js['September']['monthly'].get(t, 0.0) + js['October']['monthly'].get(t, 0.0))
                      for t in MONTHS}
    monthly_raw = {month_str(t): round(js['September']['monthly'].get(t, 0.0) + js['October']['monthly'].get(t, 0.0), 1)
                   for t in MONTHS}
    shares = {}
    for lab in ('September', 'October'):
        shares[lab] = {month_str(t): round(100 * js[lab]['monthly'].get(t, 0.0) / js[lab]['members'], 1) for t in MONTHS}
    curve_share = {}
    # the membership-month curve's own month-by-month projection, all AUT26 members
    h0 = G.kcurve(R['panel'])
    acc = defaultdict(float)
    for m in R['members']:
        r = last.loc[m]
        if status.get(m) != 'active' or r['t'] != G.CUT_M:
            continue
        s = 1.0
        for step, t in enumerate(MONTHS, start=1):
            if step > 1:
                s *= 1 - h0[min(int(r['k']) + step - 1, G.KMAX)]
            acc[t] += s
    curve_share = {month_str(t): round(100 * acc[t] / n, 1) for t in MONTHS}
    all_share = {month_str(t): round(100 * (js['September']['monthly'].get(t, 0) + js['October']['monthly'].get(t, 0)) / n, 1)
                 for t in MONTHS}
    F = dict(
        call='do not book the January and February 2027 re-run on the same terms',
        bar_eur=int(G.BAR_EUR),
        campaign_members=n,
        live_at_cut=int(len(live)),
        live_with_new_tutor=new_t,
        live_with_new_tutor_pct=round(100 * new_t / len(live), 1),
        new_tutors_mar_aug_2026=int(R['ttab']['min'].between(G.month_index(2026, 3), G.month_index(2026, 8)).sum()),
        new_tutors_sep_oct_2026=int(R['ttab']['min'].between(G.month_index(2026, 9), G.month_index(2026, 10)).sum()),
        media_net_eur=r25(cost['media_eur']), credit_note_eur=int(round(-cost['credit_eur'])),
        media_gbp_net=round(cost['media_gbp_net'], 2), discounts_eur=r25(cost['discounts_eur']),
        cost_total_eur=r25(cost['total_eur']), cost_total_exact_eur=round(cost['total_eur'], 2),
        cost_per_paid_eur=r25(cost['total_eur'] / n),
        exp12=r50(e12), exp12_raw=round(e12, 2), exp12_share_pct=round(100 * e12 / n, 1),
        cost_per_12m_eur=r25(cost['total_eur'] / e12), cost_per_12m_raw=round(cost['total_eur'] / e12, 2),
        range80_cost_eur=[r25(cost['total_eur'] / hi), r25(cost['total_eur'] / lo)],
        range80_cost_raw=[round(cost['total_eur'] / hi, 1), round(cost['total_eur'] / lo, 1)],
        range80_cost_independent=[r25(cost['total_eur'] / hi_i), r25(cost['total_eur'] / lo_i)],
        range80_cost_independent_raw=[round(cost['total_eur'] / hi_i, 1), round(cost['total_eur'] / lo_i, 1)],
        range90_cost_eur=[r25(cost['total_eur'] / p95), r25(cost['total_eur'] / p5)],
        range90_cost_raw=[round(cost['total_eur'] / p95, 1), round(cost['total_eur'] / p5, 1)],
        range90_cost_independent=[r25(cost['total_eur'] / p95i), r25(cost['total_eur'] / p5i)],
        range90_cost_independent_raw=[round(cost['total_eur'] / p95i, 1), round(cost['total_eur'] / p5i, 1)],
        flip_cost_per_paid_eur=r25(G.BAR_EUR * e12 / n), flip_raw=round(G.BAR_EUR * e12 / n, 2),
        by_joining={lab: dict(members=js[lab]['members'], exp12=r50(js[lab]['exp12']), exp12_raw=round(js[lab]['exp12'], 1),
                              share_pct=round(100 * js[lab]['share'], 1)) for lab in ('September', 'October')},
        monthly=monthly, monthly_raw=monthly_raw,
        shares=shares, all_share=all_share, curve_share=curve_share,
        stop_month_cancel_pct=round(100 * par['d1'], 1), next_month_cancel_pct=round(100 * par['d2'], 1),
        ordinary_month_cancel_pct=round(100 * par['base'], 1), member_stops=par['n_s1'],
        tutor_stop_pct={str(j): round(100 * par['q'][j], 1) for j in range(1, 13)},
        tutor_stop_late_pct=round(100 * par['q']['late'], 1),
        tutors_on_record=int(len(R['ttab'])),
        tutor_month_stop_pct=round(100 * par['q']['pooled_tutor_months'], 1),
        member_weighted_stop_pct=round(100 * par['member_weighted_stop'], 1),
        default_exp12=r50(r0), default_share_pct=round(100 * r0 / n, 1),
        default_cost_per_12m_eur=r25(cost['total_eur'] / r0), default_cost_raw=round(cost['total_eur'] / r0, 2),
        backtest_spr25=dict(n=bt_spr['n'], actual_pct=round(100 * bt_spr['actual'], 1),
                            curve_pct=round(100 * bt_spr['curve'], 1), linked_pct=round(100 * bt_spr['linked'], 1)),
        backtest_sepoct25=dict(n=bt_so['n'], actual_pct=round(100 * bt_so['actual'], 1),
                               curve_pct=round(100 * bt_so['curve'], 1), linked_pct=round(100 * bt_so['linked'], 1)),
        calibration={b: dict(n=int(r['n']), ratio=round(float(r['ratio']), 2)) for b, r in cal.iterrows()},
        season={str(m): round(v, 2) for m, v in par['season'].items()},
        range_levels=[80, 90],
        rounding=dict(members=50, eur=25),
    )
    routes = V.all_routes(R)
    c = cost['total_eur']
    shallow_keys = ('R0 ', 'R0r', 'R1s', 'R1e', 'R0f', 'R0b', 'R2 ', 'R2b', 'R2c')
    sh = [c / v for k, (v, s_) in routes.items() if k.startswith(shallow_keys)]
    dp = [c / v for k, (v, s_) in routes.items() if (k.startswith('R3 ') and 'twice' not in k and 'one shocked' not in k)
          or k.startswith('R3w')]
    rf = [c / v for k, (v, s_) in routes.items() if k.startswith(('R3r', 'R2s'))]
    F['rivals_shallow_cost_eur'] = [int(round(min(sh))), int(round(max(sh)))]
    F['rivals_standing_cost_eur'] = [int(round(min(dp))), int(round(max(dp)))]
    F['rivals_reduced_form_cost_eur'] = [int(round(min(rf))), int(round(max(rf)))]
    one = [c / v for k, (v, s_) in routes.items() if k.startswith('R3 one shocked')][0]
    dbl = [c / v for k, (v, s_) in routes.items() if k.startswith('R3 stops counted twice')][0]
    F['half_step_one_shock_eur'] = int(round(one)); F['double_count_eur'] = int(round(dbl))
    y22, y23, n22, n23 = V.rematch_regime(R)
    fk = R['panel'][R['panel'].k == 1].set_index('member_id')
    def young_share(ms):
        f = fk.loc[[m for m in ms if m in fk.index]]
        return round(100 * float(((f.tj >= 0) & (f.tj <= 2)).mean()), 1)
    F['first_tutor_young_pct'] = dict(SPR25=young_share(spr), SepOct25=young_share(sep_oct_25),
                                      AUT26=young_share(R['members']))
    F['rematch_young_2022_pct'] = round(100 * y22, 1); F['rematch_young_since_2023_pct'] = round(100 * y23, 1)
    return F, draws


# ------------------------------------------------------------------------------------------------ chart
def chart(F, path):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9, 'svg.hashsalt': 'task601',
                         'axes.edgecolor': '#8a8984', 'axes.labelcolor': '#52514e', 'xtick.color': '#52514e',
                         'ytick.color': '#52514e'})
    ks = list(F['shares']['September'].keys())
    x = list(range(len(ks)))
    fig, ax = plt.subplots(figsize=(6.4, 3.1), dpi=160)
    ax.plot(x, [F['curve_share'][k] for k in ks], color='#8a8984', lw=1.6, ls=(0, (4, 3)),
            label='Retention curve by membership month, all AUT26 members')
    ax.plot(x, [F['shares']['September'][k] for k in ks], color='#2a78d6', lw=2, marker='o', ms=4,
            label='Joined in September, tutor-linked projection')
    ax.plot(x, [F['shares']['October'][k] for k in ks], color='#eb6834', lw=2, marker='o', ms=4,
            label='Joined in October, tutor-linked projection')
    for series, dy in (('September', -9), ('October', -1)):
        v = F['shares'][series][ks[-1]]
        ax.annotate('%.1f%%' % v, (x[-1], v), xytext=(6, dy), textcoords='offset points',
                    fontsize=8, color='#0b0b0b', va='center')
    ax.annotate('%.1f%%' % F['curve_share'][ks[-1]], (x[-1], F['curve_share'][ks[-1]]), xytext=(6, 4),
                textcoords='offset points', fontsize=8, color='#52514e', va='center')
    ax.set_title('AUT26 members drop below the usual retention curve in spring 2027', loc='left', fontsize=9.5,
                 color='#0b0b0b', pad=8)
    ax.set_xticks(x)
    ax.set_xticklabels([dt.date(int(k[:4]), int(k[5:]), 1).strftime('%b\n%Y') if k.endswith(('-11', '-01')) else
                        dt.date(int(k[:4]), int(k[5:]), 1).strftime('%b') for k in ks], fontsize=8)
    ax.set_ylabel('Share of AUT26 members paying (%)')
    ax.set_ylim(0, 100)
    ax.grid(axis='y', color='#e6e5e0', lw=.6)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    ax.set_xlim(-.3, len(x) - .2 + 1.0)
    ax.legend(frameon=False, fontsize=7.5, loc='upper right')
    fig.tight_layout()
    fig.savefig(path, metadata={'Software': None})
    plt.close(fig)


# ------------------------------------------------------------------------------------------------ workbook
def workbook(R, F, path):
    from openpyxl import Workbook
    from openpyxl.styles import Font, Alignment, PatternFill
    wb = Workbook()
    bold = Font(bold=True)
    ws = wb.active; ws.title = 'Monthly'
    ws.append(['AUT26 members expected to pay a membership charge in each month, by the month they joined (tutor-linked projection, cut 31 October 2026)'])
    ws['A1'].font = bold
    ws.append([])
    ws.append(['Month', 'Joined September 2026', 'Joined October 2026', 'All AUT26 members'])
    for c in ws[3]:
        c.font = bold
    for k in F['monthly']['All']:
        ws.append([dt.date(int(k[:4]), int(k[5:]), 1).strftime('%b %Y'), F['monthly']['September'][k],
                   F['monthly']['October'][k], F['monthly']['All'][k]])
    ws.append([])
    ws.append(['Each count is rounded to the nearest 50 members on its own, so the two joining months need not add '
               'to the total.'])
    for col, w in zip('ABCD', [12, 24, 22, 20]):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = 'B4'
    for row in ws.iter_rows(min_row=4, max_row=3 + len(F['monthly']['All']), min_col=2, max_col=4):
        for c in row:
            c.number_format = '#,##0'
    # twelfth charge
    t2 = wb.create_sheet('Twelfth charge')
    t2.append(['', 'Joined September 2026', 'Joined October 2026', 'All AUT26 members'])
    for c in t2[1]:
        c.font = bold
    bj = F['by_joining']
    t2.append(['Campaign members', bj['September']['members'], bj['October']['members'], F['campaign_members']])
    t2.append(['Expected twelfth-month members', bj['September']['exp12'], bj['October']['exp12'], F['exp12']])
    t2.append(['Share paying a twelfth charge (%)', bj['September']['share_pct'], bj['October']['share_pct'], F['exp12_share_pct']])
    for c in t2[t2.max_row][1:]:
        c.number_format = '0.0'
    t2.append([])
    t2.append(['Retention curve by membership month alone (for comparison)', '', '', F['default_exp12']])
    for col, w in zip('ABCD', [52, 22, 22, 20]):
        t2.column_dimensions[col].width = w
    # cost
    c3 = wb.create_sheet('Cost')
    c3.append(['Item', 'EUR'])
    for c in c3[1]:
        c.font = bold
    c3.append(['Media invoiced, net of VAT (GBP at the ECB rate of each issue date)', F['media_net_eur'] + F['credit_note_eur']])
    c3.append(['Credit note FM-DE-2026-CN07', -F['credit_note_eur']])
    c3.append(['First-month discounts (AUT26-WELCOME10 against list price)', F['discounts_eur']])
    c3.append(['Campaign cost', F['cost_total_eur']])
    c3.append(['Campaign members', F['campaign_members']])
    c3.append(['Cost per paid member', F['cost_per_paid_eur']])
    c3.append(['Expected twelfth-month members', F['exp12']])
    c3.append(['Cost per twelfth-month member', F['cost_per_12m_eur']])
    c3.append(['80% range, cost per twelfth-month member', '%d to %d' % tuple(F['range80_cost_eur'])])
    c3.append(['90% range, cost per twelfth-month member', '%d to %d' % tuple(F['range90_cost_eur'])])
    c3.append(['Re-run bar', F['bar_eur']])
    c3.append(['Cost per paid member that would meet the bar exactly', F['flip_cost_per_paid_eur']])
    c3.column_dimensions['A'].width = 66; c3.column_dimensions['B'].width = 16
    for row in c3.iter_rows(min_row=2, max_row=c3.max_row, min_col=2, max_col=2):
        for c in row:
            if isinstance(c.value, (int, float)):
                c.number_format = '#,##0'
            else:
                c.alignment = Alignment(horizontal='right')
    # inputs
    i4 = wb.create_sheet('Inputs')
    i4.append(['Monthly cancellation by membership month, months with an active tutor (%)'])
    i4['A1'].font = bold
    i4.append(['Membership month', 'Cancel (%)'])
    for k in range(1, 13):
        i4.append([k, round(100 * R['par']['h'][k], 2)])
    i4.append([])
    i4.append(['First month without the member\'s tutor: cancel (%)', F['stop_month_cancel_pct']])
    i4.append(['Following month, with a new tutor: cancel (%)', F['next_month_cancel_pct']])
    i4.append(['Average month with an active tutor: cancel (%)', F['ordinary_month_cancel_pct']])
    i4.append([])
    i4.append(['Tutors who do not teach the next month, by months taught (%)'])
    i4.append(['Months taught', 'Stop (%)'])
    for j in range(1, 13):
        i4.append([j, F['tutor_stop_pct'][str(j)]])
    i4.append(['13 and later', F['tutor_stop_late_pct']])
    i4.column_dimensions['A'].width = 52; i4.column_dimensions['B'].width = 12
    # member-level projection
    m5 = wb.create_sheet('Members')
    m5.append(['member_id', 'joined', 'charges paid to 31 Oct 2026', 'tutor_id, last month paid',
               'tutor teaching month, last month paid', 'P(pays a twelfth charge)'])
    for c in m5[1]:
        c.font = bold
    last = G.state_at_cut(R['panel'], R['members'])
    fc = R['ch'][R['ch'].k == 1].set_index('member_id')
    for m in R['members']:
        r = last.loc[m]
        tid = ('T-%06d' % r['tid']) if r['tid'] >= 0 else ''
        m5.append([m, month_str(int(fc.loc[m, 't'])), int(r['k']), tid, int(r['tj']) + 1 if r['tid'] >= 0 else '',
                   round(R['by'][m][0], 4)])
    for col, w in zip('ABCDEF', [12, 9, 26, 24, 34, 22]):
        m5.column_dimensions[col].width = w
    m5.freeze_panes = 'A2'
    m5.auto_filter.ref = 'A1:F%d' % m5.max_row
    for row in m5.iter_rows(min_row=2, max_row=m5.max_row, min_col=6, max_col=6):
        for c in row:
            c.number_format = '0.0000'
    n6 = wb.create_sheet('Notes')
    for line in ('Data cut: billing events and lesson activity to 31 October 2026; members export and tutor directory '
                 'of 3 November 2026.',
                 'AUT26 members, campaign cost and the twelfth charge as defined in the growth review standard, '
                 'section 3: first charge collected 1 September to 31 October 2026 (Berlin days) with the AUT26 code on '
                 'the sign-up; cost net of VAT and credit notes, GBP at the ECB reference rate of each invoice\'s '
                 'issue date, plus first-month discounts against the list price.',
                 'Projection: each member still paying on 31 October is carried month by month through their tutor\'s '
                 'chance of stopping by months taught and their own cancellation by membership month; a member whose '
                 'tutor stops faces the stop-month and following-month cancellation on the Inputs sheet.',
                 'Rounding: member counts to the nearest 50 and euro amounts to the nearest 25, each figure on its own.'):
        n6.append([line])
        n6.cell(row=n6.max_row, column=1).alignment = Alignment(wrap_text=True, vertical='top')
    n6.column_dimensions['A'].width = 110
    wb.properties.creator = 'Marit Klemt'
    wb.properties.lastModifiedBy = 'Marit Klemt'
    wb.properties.created = dt.datetime(2026, 11, 5, 9, 14, 0)
    wb.properties.modified = dt.datetime(2026, 11, 6, 17, 2, 0)
    wb.properties.title = None
    wb.save(path)
    import docs
    docs.ooxml_props(path, 'Marit Klemt', 'Marit Klemt', dt.datetime(2026, 11, 5, 9, 14, 0),
                     dt.datetime(2026, 11, 6, 17, 2, 0), 'Corvane Sprachen GmbH')


# ------------------------------------------------------------------------------------------------ memo
def memo(R, F, path, png):
    from docx import Document
    from docx.shared import Pt, Cm, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    d = Document()
    st = d.styles['Normal']; st.font.name = 'Calibri'; st.font.size = Pt(10)
    for s in d.sections:
        s.left_margin = s.right_margin = Cm(2.2); s.top_margin = Cm(1.8); s.bottom_margin = Cm(1.8)

    def para(text, bold=False, size=None, space=4):
        p = d.add_paragraph()
        r = p.add_run(text); r.bold = bold
        if size:
            r.font.size = Pt(size)
        p.paragraph_format.space_after = Pt(space)
        return p
    para('AUT26 re-run: do not book on the same terms', bold=True, size=13, space=2)
    para('To Caroline Ritter. From Marit Klemt. 6 November 2026. Data cut 31 October 2026.', size=8.5, space=8)
    bj = F['by_joining']
    para('Decision', bold=True, size=10.5, space=2)
    para('Do not book the January and February re-run of AUT26 on the same terms. The campaign is expected to cost '
         'EUR %d per member still paying in their twelfth month (80%% range EUR %d to %s, 90%% range EUR %d to %s), '
         'above the EUR %d bar across both ranges. The retention curve we usually project with puts it at EUR %d and '
         'would clear the bar; it misses what happens to members when their tutor stops teaching.' % (
             F['cost_per_12m_eur'], F['range80_cost_eur'][0], f'{F["range80_cost_eur"][1]:,}', F['range90_cost_eur'][0],
             f'{F["range90_cost_eur"][1]:,}', F['bar_eur'], F['default_cost_per_12m_eur']))
    para('The numbers', bold=True, size=10.5, space=2)
    para('AUT26 brought in %s paid members (first charge from 1 September to 31 October, Berlin time, AUT26 code on '
         'the sign-up). It cost EUR %s: EUR %s of media net of VAT and of the EUR %s credit note, and EUR %s of '
         'first-month discounts, or EUR %d per paid member. We expect about %s of these members to pay a twelfth '
         'monthly charge (%.1f%%), about %s of the %s who joined in September and %s of the %s who joined in October. '
         'The ranges allow for the fact that every member of one tutor shares that tutor\'s chance of stopping, which '
         'widens them well beyond what members taken one at a time would give. Members like these would have met '
         'EUR %d exactly at about EUR %d per paid member.' % (
             f'{F["campaign_members"]:,}', f'{F["cost_total_eur"]:,}', f'{F["media_net_eur"]:,}',
             f'{F["credit_note_eur"]:,}', f'{F["discounts_eur"]:,}', F['cost_per_paid_eur'], f'{F["exp12"]:,}',
             F['exp12_share_pct'], f'{bj["September"]["exp12"]:,}', f'{bj["September"]["members"]:,}',
             f'{bj["October"]["exp12"]:,}', f'{bj["October"]["members"]:,}', F['bar_eur'], F['flip_cost_per_paid_eur']))
    para('Why the usual curve is too high', bold=True, size=10.5, space=2)
    para('Projected on our retention curve by membership month, %.1f%% of AUT26 members (%s) would reach the '
         'twelfth charge. The curve has not been optimistic before: it ran low on the spring 2025 campaign (%.1f%% '
         'projected from June 2025 against %.1f%% kept) and on last autumn\'s joiners (%.1f%% against %.1f%%). '
         'AUT26 is a different mix: %d tutors began teaching in September and October, against %d from March to '
         'August, and %s of the %s AUT26 members still paying on '
         '31 October (%.1f%%) are with them.' % (F['default_share_pct'], f'{F["default_exp12"]:,}', F['backtest_spr25']['curve_pct'],
                       F['backtest_spr25']['actual_pct'], F['backtest_sepoct25']['curve_pct'],
                       F['backtest_sepoct25']['actual_pct'], F['new_tutors_sep_oct_2026'], F['new_tutors_mar_aug_2026'],
                       f'{F["live_with_new_tutor"]:,}', f'{F["live_at_cut"]:,}', F['live_with_new_tutor_pct']))
    tq = F['tutor_stop_pct']
    para('That matters for two reasons the lesson log shows. A member whose tutor stops teaching cancels %.1f%% of '
         'the time in the first month without that tutor and %.1f%% the month after, against %.1f%% in an ordinary '
         'month (%s member months with a tutor stop since 2022). And tutors stop early: of tutors who have taught '
         'four, five and six months, %.1f%%, %.1f%% and %.1f%% do not teach the next month, against %.1f%% a month '
         'for tutors past their first year (%s tutors on record). Carrying each member through their own tutor\'s '
         'odds of stopping gives %s twelfth-month members. Over six-month windows the curve under-predicts the '
         'cancellations of members whose tutor is in their first three months of teaching by a factor of %.2f and '
         'in their fourth to ninth months by %.2f, and over-predicts members of tutors past their first year '
         '(%.2f); the tutor-linked projection carries that difference.' % (
             F['stop_month_cancel_pct'], F['next_month_cancel_pct'], F['ordinary_month_cancel_pct'],
             f'{F["member_stops"]:,}', tq['4'], tq['5'], tq['6'], F['tutor_stop_late_pct'],
             f'{F["tutors_on_record"]:,}', f'{F["exp12"]:,}', F['calibration']['1-3']['ratio'],
             F['calibration']['4-9']['ratio'], F['calibration']['13+']['ratio']))
    d.add_picture(png, width=Cm(16.2))
    cap = para('Expected share of AUT26 members paying each month, by joining month, against the retention curve. '
               'The AUT26 lines stay above the curve through the winter and fall below it from March (September '
               'joiners) and April (October joiners), once their tutors reach the months in which tutors most often stop.', size=8,
               space=6)
    para('Source: billing events and lesson activity to 31 October 2026; tutor directory of 3 November 2026. Campaign '
         'members, cost and twelfth charges as defined in the growth review standard, section 3.', size=7.5, space=10)
    para('The month-by-month projection, the cost build-up and each member\'s projection are in '
         'aut26_member_forecast.xlsx.', size=8.5)
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    fp = d.sections[0].footer.paragraphs[0]
    fr = fp.add_run('Corvane Sprachen GmbH, growth analytics. Internal.   Page ')
    fr.font.size = Pt(7.5)
    fld = OxmlElement('w:fldSimple'); fld.set(qn('w:instr'), 'PAGE')
    pr = OxmlElement('w:r'); rpr = OxmlElement('w:rPr'); sz = OxmlElement('w:sz'); sz.set(qn('w:val'), '15')
    rpr.append(sz); pr.append(rpr); t = OxmlElement('w:t'); t.text = '1'; pr.append(t); fld.append(pr)
    fp._p.append(fld)
    cp = d.core_properties
    cp.author = 'Marit Klemt'; cp.last_modified_by = 'Marit Klemt'; cp.title = 'AUT26 re-run decision note'
    cp.created = dt.datetime(2026, 11, 6, 8, 30, 0); cp.modified = dt.datetime(2026, 11, 6, 16, 45, 0)
    cp.revision = 3
    d.save(path)
    import docs
    text = ' '.join(p.text for p in d.paragraphs)
    words = len(text.split()); chars = len(text.replace(' ', ''))
    docs.ooxml_props(path, 'Marit Klemt', 'Marit Klemt', dt.datetime(2026, 11, 6, 8, 30, 0),
                     dt.datetime(2026, 11, 6, 16, 45, 0), 'Corvane Sprachen GmbH', title='AUT26 re-run decision note',
                     docx_stats=dict(minutes=94, pages=2, words=words, chars=chars, chars_sp=len(text),
                                     lines=max(1, chars // 70), paras=len(d.paragraphs)), revision=3)


def main():
    R = G.run()
    F, draws = figures(R)
    os.makedirs(GOLDEN, exist_ok=True)
    for f in os.listdir(GOLDEN):
        os.remove(os.path.join(GOLDEN, f))
    png = os.path.join(HERE, 'cache', 'aut26_share_chart.png')
    chart(F, png)
    workbook(R, F, os.path.join(GOLDEN, 'aut26_member_forecast.xlsx'))
    memo(R, F, os.path.join(GOLDEN, 'aut26_rerun_memo.docx'), png)
    json.dump(F, open(os.path.join(HERE, 'figures.json'), 'w'), indent=1, sort_keys=True)
    stamp = dt.datetime(2026, 11, 6, 16, 45, tzinfo=UTC).timestamp()
    for f in os.listdir(GOLDEN):
        os.utime(os.path.join(GOLDEN, f), (stamp, stamp))
    print(json.dumps({k: F[k] for k in ('campaign_members', 'cost_total_eur', 'cost_per_paid_eur', 'exp12',
                                         'exp12_share_pct', 'cost_per_12m_eur', 'range80_cost_eur', 'range90_cost_eur',
                                         'range80_cost_independent', 'flip_cost_per_paid_eur', 'default_exp12',
                                         'default_cost_per_12m_eur', 'live_with_new_tutor', 'live_at_cut',
                                         'backtest_spr25', 'backtest_sepoct25', 'calibration', 'by_joining')}, indent=1))


if __name__ == '__main__':
    main()
