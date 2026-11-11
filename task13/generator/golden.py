"""The golden deliverables, built from the shipped pack by analysis.run: the zone table every referral reads from
(lightning_referrals_2027.csv) and the reliability engineer's note to the management committee with its chart
(lightning_refit_2027_note.docx). Every figure is written to generator/figures.json, which the answer blocks quote."""
import io
import json
import os
import shutil

import numpy as np
import pandas as pd

import analysis as A
import common as C
import postprocess as PP

WORDS = {2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six', 7: 'seven', 8: 'eight', 9: 'nine', 10: 'ten'}


def r1(x):
    return float(np.round(x + 1e-12, 1))


def table(R):
    L = R['L']
    zr = L['zr']
    DF = R['DF']
    T26 = R['hist'][2026].set_index('zone_ix')
    ins = L['ins']
    last = ins.groupby('zone_ix').done.max()
    rows = []
    for z, zone in enumerate(R['zones']):
        W = R['window'](z, 2026)
        yv = sum(DF.loc[(z, s), 'yf'] for s in W)
        lv = R['Eu'][z]
        ev = lv * sum(DF.loc[(z, s), 'Ef'] for s in W)
        refd = z in R['ref']
        nconf = int(sum(1 for s in A.ALL if DF.loc[(z, s), 'ver']))
        rows.append({
            'zone': zone, 'feeder': zr.Feeder[z], 'substation': zr.Substation[z],
            'radio_link': 'no' if str(zr.Telemetry[z]).startswith('None') else 'yes',
            'last_cyclic_inspection': pd.Timestamp(last[z]).strftime('%Y-%m-%d'),
            **{'lightning_faults_%d' % s: r1(DF.loc[(z, s), 'yf']) for s in A.SEASONS},
            'confirmed_sound_seasons': nconf, 'own_sound_level': float(np.round(lv, 2)),
            'sound_expected_2026': r1(lv * DF.loc[(z, 2026), 'Ef']),
            'seasons_since_inspection': len(W),
            'faults_since_inspection': r1(yv), 'sound_expected_since_inspection': r1(ev),
            'ratio': float(np.round(yv / ev, 2)) if ev > 0 else '',
            'chance_if_sound': ('%.1e' % T26.p[z]) if z in T26.index else '',
            'referred': 'yes' if refd else 'no'})
    return pd.DataFrame(rows)


def make_figures(R, T):
    zones = R['zones']
    ref = R['ref']
    F = {
        'referred_zones': sorted(R['ref_names']),
        'n_referred': len(ref),
        'alpha': R['alpha'], 'nb_size': round(R['k'], 1), 'budget_seasons': R['opt']['budget_seasons'],
        'alerts': {str(s): R['alerts'][s] for s in A.SEASONS},
        'false_per_season': round(R['false_per'], 2),
        'alert_load': dict({str(x): R['alerts'][x] for x in A.SEASONS}, sound_per_season=round(R['false_per'], 2)),
        'validation': {'referred_inspected': R['v_ref'], 'confirmed': R['v_conf'], 'missed': R['v_miss'],
                       'failed_found': R['v_fail']},
        'season_totals': {str(s): int(round(R['season_tot'][s])) for s in A.SEASONS},
        'radioless_2026': int(round(R['radioless26'])),
        'faults_2026': int(round(R['obs26'])), 'sound_2026': int(round(R['sound26'])),
        'excess_2026': int(round(R['excess26'])),
        'avoided_average_season': int(round(R['avoided_total'])),
        'validation_core': {'referred_inspected': R['v_ref'], 'confirmed': R['v_conf'], 'missed': R['v_miss']},
        'referred_zones_sorted': sorted(R['ref_names']),
        'rows': {r.zone: {'lightning_faults_2026': r.lightning_faults_2026, 'faults_since_inspection': r.faults_since_inspection,
                          'sound_expected_since_inspection': r.sound_expected_since_inspection, 'ratio': r.ratio,
                          'sound_expected_2026': r.sound_expected_2026, 'referred': r.referred}
                 for r in T.itertuples() if r.referred == 'yes'},
    }
    F.update(evidence(R))
    F['n_unreferred'] = R['N'] - len(ref)
    F['season_totals_with_radioless'] = dict(F['season_totals'], radioless_2026=F['radioless_2026'])
    F['expected_since_inspection'] = {z: v['sound_expected_since_inspection'] for z, v in F['rows'].items()}

    def pct(v, p):
        return [int(round(v * (1 - p))), int(round(v * (1 + p)))]
    # the bands the answer blocks state, where reasonable methods differ (the rivals in checks.py land inside each)
    F['bands'] = {'season_totals': {k: pct(v, 0.04) for k, v in F['season_totals'].items()},
                  'radioless_2026': [int(round(F['radioless_2026'] * 0.925)), int(round(F['radioless_2026'] * 1.06))],
                  # the counterfactual's rivals (the stroke-level sound model, the matching radius, the covariate sets,
                  # the restoration rate) span 178 to 186: the band is that span with a margin each way
                  'excess_2026': [int(round(F['excess_2026'] * 0.915)), int(round(F['excess_2026'] * 1.075))],
                  'false_per_season': [round(F['false_per_season'] - 0.02, 2), round(F['false_per_season'] + 0.02, 2)],
                  'avoided_average_season': pct(F['avoided_average_season'], 0.10),
                  # the replay's counts under the rival family (the stroke-level sound model refers one or two more
                  # after 2024 and 2025)
                  'alerts': {str(x): [max(0, R['alerts'][x] - 1), R['alerts'][x] + (2 if x == 2025 else 1)]
                             for x in A.SEASONS},
                  'expected_since_inspection': {z: [r1(v['sound_expected_since_inspection'] * 0.8),
                                                    r1(v['sound_expected_since_inspection'] * 1.2)]
                                                for z, v in F['rows'].items()},
                  # the replay's borderline zones (two sit within ten per cent of the threshold after 2022 and 2025) move
                  # the check by up to two under the rival family, downward
                  'validation_core': {'referred_inspected': [F['validation_core']['referred_inspected'] - 2,
                                                             F['validation_core']['referred_inspected'] + 1],
                                      'confirmed': [F['validation_core']['confirmed'] - 2, F['validation_core']['confirmed'] + 1],
                                      'missed': [F['validation_core']['missed'] - 1, F['validation_core']['missed'] + 2]}}
    F['routes'] = routes(R)
    return F


ROUTES = {
    # the shortcuts the note's last table sets beside the rule, each with what it would refer and report
    'logs_as_recorded': ('The controllers\' logs as recorded (a ten-minute window, only the events kept)',
                         dict(clock='wide', fill=False)),
    'unverified_baseline': ('Sound rate from every season no inspection has found failed', dict(null='not_failed')),
    'independent_seasons': ('Each season\'s scatter taken on its own (quasi-Poisson)', dict(disp='quasi')),
    'no_own_level': ('Every zone at the network rate, with no level of its own', dict(own='none')),
    'known_level': ('Each zone\'s own level taken as known', dict(level='plugin')),
    'window_average': ('Avoided faults averaged over the record since inspection', dict(avoided='average')),
    'careful': ('Seasons on their own and the record averaged', dict(disp='quasi', avoided='average')),
    'poisson': ('Chance taken as Poisson', dict(disp='poisson')),
    'whole_record': ('Faults over the whole record, not since the last inspection', dict(window='whole')),
    'fixed_offset': ('One fixed offset per radio-less controller', dict(clock='constant', fill=False)),
    'logged_only': ('Drift fitted, only the events kept', dict(fill=False)),
}


def summary(r):
    return {'n_referred': len(r['ref']), 'referred_zones': sorted(r['ref_names']),
            'season_totals': {str(s): int(round(r['season_tot'][s])) for s in A.SEASONS},
            'faults_2026': int(round(r['obs26'])), 'radioless_2026': int(round(r['radioless26'])),
            'excess_2026': int(round(r['excess26'])), 'alerts': {str(s): r['alerts'][s] for s in A.SEASONS},
            'validation': {'referred_inspected': r['v_ref'], 'confirmed': r['v_conf'], 'missed': r['v_miss']},
            'avoided_average_season': int(round(r['avoided_total'])), 'false_per_season': round(r['false_per'], 2),
            'false_per_season_true': round(r['false_true'], 2), 'nb_size': round(r['k'], 1)}


def routes(R):
    L = R['L']
    gold = set(R['ref_names'])
    out = {}
    for k, (lab, o) in ROUTES.items():
        v = summary(A.run(None, o, L=L))
        v['differs_from_rule'] = len(set(v['referred_zones']) ^ gold)
        out[k] = dict(v, label=lab)
    return out


def evidence(R):
    """the figures the answer blocks cite on the way: the record's losses, the confirmed seasons, the test of the
    spread, the threshold's margins and the readings the terms rule out"""
    from scipy import stats
    L = R['L']
    DF = R['DF']
    ins = L['ins'].sort_values('start')
    clean_then_failed = 0
    for z, g in ins.groupby('Zone'):
        f = list(g.failed)
        clean_then_failed += sum(1 for a, b in zip(f, f[1:]) if not a and b)
    fs = DF[DF.ver & (DF.E > 0)]
    lr = 2 * (stats.nbinom.logpmf(fs.y, R['k'], R['k'] / (R['k'] + fs.E)).sum() - stats.poisson.logpmf(fs.y, fs.E).sum())
    ll_pooled = stats.nbinom.logpmf(fs.y, R['k'], R['k'] / (R['k'] + fs.E)).sum()
    lr_zone = 2 * (R['ll_lv'] - ll_pooled) if R.get('zone_model') else 0.0
    cov = R['cov']
    lost = [(z, n) for z, w in cov.items() for a0, a1, n in w if n > 0]
    T26 = R['hist'][2026]
    d26 = DF.xs(2026, level='season')
    rl = set(R['radioless'])
    av26 = 0.0
    for z in R['ref']:
        W = R['window'](z, 2026)
        ratio = sum(DF.loc[(z, x), 'y'] for x in W) / sum(DF.loc[(z, x), 'E'] for x in W)
        av26 += (ratio - 1) * DF.loc[(z, 2026), 'Ef']
    return {
        'n_zones': R['N'], 'n_radioless': len(rl), 'n_synchronised': R['N'] - len(rl), 'match_radius_m': 400,
        'referred_radioless': len(rl & set(R['ref'])),
        'alpha_one_in': int(round(1 / R['alpha'])), 'budget_per_season': 0.2,
        'confirmed_sound_zone_seasons': int(DF.ver.sum()), 'clean_then_failed_zones': clean_then_failed,
        'lr_nb_poisson': round(float(lr), 2),
        'lr_zone_vs_pooled': round(float(lr_zone), 1), 'level_shape': round(float(R['a_lv'] or 0), 2),
        'level_cv': round(float(1 / np.sqrt(R['a_lv'])) if R.get('a_lv') else 0.0, 2),
        'reads': sum(len(w) for w in cov.values()), 'reads_with_loss': len(lost),
        'events_lost': int(sum(n for z, n in lost)), 'zones_with_loss': len({z for z, n in lost}),
        'radioless_2026_logged': int(round(d26.loc[sorted(rl), 'y'].sum())),
        'weakest_referred_chance': float('%.1e' % T26[T26.referred].p.max()),
        'strongest_unreferred_chance': float('%.1e' % T26[~T26.referred].p.min()),
        'excess_referred_only': int(round(sum(d26.loc[z, 'yf'] - d26.loc[z, 'Ef'] for z in R['ref']))),
        'excess_positive_parts': int(round(float(np.clip(d26.yf - d26.Ef, 0, None).sum()))),
        'avoided_2026_lightning': int(round(av26)),
        'restored_test_flip': restored_flip(R),
        **onsets(R),
        **known_level(R),
    }


def onsets(R):
    """each referred zone's record since its inspection season by season against its own sound level: how many ran at
    that level in their first season and above twice it in the last, and the refit valued on the seasons since each
    failure began instead of the last season"""
    DF, Eu = R['DF'], R['Eu']
    first_low, last_high = 0, 0
    for z in R['ref']:
        W = R['window'](z, 2026)
        rr = [DF.loc[(z, x), 'yf'] / max(Eu[z] * DF.loc[(z, x), 'Ef'], 1e-9) for x in W]
        first_low += int(len(W) > 1 and rr[0] < 0.5 * rr[-1])
        last_high += int(rr[-1] > 2.0)
    po = A.run(None, {'avoided': 'post_onset'}, L=R['L'])
    return {'referred_first_season_low': first_low, 'referred_last_season_high': last_high,
            'avoided_post_onset': int(round(po['avoided_total']))}


def known_level(R):
    """the rule with each zone's level taken as known: what it refers and how often it would refer a sound zone"""
    kl = A.run(None, {'level': 'plugin'}, L=R['L'])
    return {'known_level_referred': len(kl['ref']), 'known_level_false_claimed': round(kl['false_per'], 2),
            'known_level_false_true': round(kl['false_true'], 2),
            'known_level_adds': sorted(set(kl['ref_names']) - set(R['ref_names']))}


def restored_flip(R):
    """the zones a chance judged on restored counts, as if counted, would add or drop"""
    Rr = A.run(None, {'test': 'restored'}, L=R['L'])
    T26 = R['hist'][2026].set_index('zone_ix')
    return [{'zone': R['zones'][z], 'recorded': int(T26.y[z]), 'expected_recorded': round(float(T26.E[z]), 1),
             'chance_recorded': float('%.1e' % T26.p[z])} for z in sorted(set(Rr['ref']) ^ set(R['ref']))]


def chart(R, T, F, path):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    surface, ink, ink2, muted, accent = '#fcfcfb', '#0b0b0b', '#52514e', '#a3a19b', '#2a78d6'
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'svg.hashsalt': 'task13'})
    fig, ax = plt.subplots(figsize=(6.6, 4.6), dpi=200)
    fig.patch.set_facecolor(surface)
    ax.set_facecolor(surface)
    t = T[T.sound_expected_since_inspection > 0]
    ref = t.referred == 'yes'
    ax.scatter(t.sound_expected_since_inspection[~ref], t.faults_since_inspection[~ref], s=14, c=muted, alpha=0.85,
               label='Not referred', edgecolors='none', zorder=2)
    ax.scatter(t.sound_expected_since_inspection[ref], t.faults_since_inspection[ref], s=30, c=accent,
               label='Referred for the 2027 refit', edgecolors=surface, linewidths=0.8, zorder=3)
    xm = t.sound_expected_since_inspection.max() * 1.08
    ym = t.faults_since_inspection.max() * 1.1
    ax.plot([0, xm], [0, xm], color=ink2, lw=1.0, ls=(0, (4, 3)), zorder=1)
    lx = min(xm, ym) * 0.93
    ax.text(lx, lx + ym * 0.015, 'faults = sound expectation', fontsize=6.5, color=ink2, ha='right', va='bottom')
    ax.set_xlim(0, xm)
    ax.set_ylim(0, ym)
    lo, hi = min(F['rows'][z]['ratio'] for z in F['rows']), max(F['rows'][z]['ratio'] for z in F['rows'])
    ax.set_title('The %d referred zones run %.2f to %.2f times the faults sound protection would give them'
                 % (len(F['rows']), lo, hi), fontsize=8.6, color=ink, loc='left', pad=8)
    ax.set_xlabel('Lightning faults sound protection would have given since the last cyclic inspection', fontsize=7.6,
                  color=ink2)
    ax.set_ylabel('Lightning faults since the last cyclic inspection', fontsize=7.6, color=ink2)
    leg = ax.legend(frameon=False, fontsize=7, loc='lower right')
    for tx in leg.get_texts():
        tx.set_color(ink)
    for sp in ('top', 'right'):
        ax.spines[sp].set_visible(False)
    for sp in ('left', 'bottom'):
        ax.spines[sp].set_color(ink2)
        ax.spines[sp].set_linewidth(0.7)
    ax.tick_params(labelsize=7, colors=ink2, width=0.7)
    fig.tight_layout()
    # direct labels, each placed at the first offset that clears the labels already placed and the plot's edges
    fig.canvas.draw()
    rnd = fig.canvas.get_renderer()
    axbox = ax.get_window_extent(rnd)
    from matplotlib.transforms import Bbox
    rr = t[ref].sort_values('faults_since_inspection', ascending=False)
    pts = ax.transData.transform(np.c_[rr.sound_expected_since_inspection.values, rr.faults_since_inspection.values])
    placed = [Bbox.from_extents(x - 6, y - 6, x + 6, y + 6) for x, y in pts]
    cands = [(6, 0), (-6, 0)]
    for rad in (12, 20, 28, 36, 46):
        for ux, uy in ((1, 0), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1), (0.4, 1), (-0.4, 1), (0.4, -1), (-0.4, -1)):
            cands.append((ux * rad, uy * rad * 0.8))
    from matplotlib.transforms import offset_copy
    for i, r in enumerate(rr.itertuples()):
        xy = (r.sound_expected_since_inspection, r.faults_since_inspection)
        others = placed[:i] + placed[i + 1:]
        for dx, dy in cands:
            ha = 'left' if dx >= 0 else 'right'
            probe = ax.text(xy[0], xy[1], r.zone, fontsize=6.3, ha=ha, va='center',
                            transform=offset_copy(ax.transData, fig=fig, x=dx, y=dy, units='points'))
            bb = probe.get_window_extent(rnd).expanded(1.06, 1.25)
            probe.remove()
            inside = bb.x0 >= axbox.x0 and bb.x1 <= axbox.x1 and bb.y0 >= axbox.y0 and bb.y1 <= axbox.y1
            if inside and not any(bb.overlaps(o) for o in others):
                near = abs(dy) < 1 and abs(dx) <= 6
                ax.annotate(r.zone, xy, fontsize=6.3, color=ink, xytext=(dx, dy), textcoords='offset points', ha=ha,
                            va='center', arrowprops=None if near else dict(arrowstyle='-', color=ink2, lw=0.5,
                                                                           shrinkA=1, shrinkB=3))
                placed.append(bb)
                break
    fig.savefig(path, metadata={'Software': None}, facecolor=surface)
    plt.close(fig)


def last_reads(R):
    """the earliest and latest of the radio-less reclosers' last reads, as the note states them"""
    rd = A.reads(R['L'])
    last = [pd.Timestamp(rd[z].max()) for z in R['radioless'] if z in rd and len(rd[z])]
    return min(last).strftime('%B %Y'), max(last).strftime('%B %Y')


def _small(p, size=8.5, italic=False):
    from docx.shared import Pt
    for r in p.runs:
        r.font.size = Pt(size)
        r.italic = italic
    return p


def note(R, T, F, path, png):
    from docx import Document
    from docx.shared import Mm, Pt, RGBColor
    import officepdf as OP
    zones = R['zones']
    zr = R['L']['zr']
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Mm(210), Mm(297)
    sec.left_margin = sec.right_margin = Mm(20)
    sec.top_margin, sec.bottom_margin = Mm(18), Mm(18)
    st = doc.styles['Normal']
    st.font.name = 'Calibri'
    st.font.size = Pt(10)
    refs = R['ref']
    names = [zones[z] for z in refs]
    h = doc.add_paragraph()
    r = h.add_run('Fifteen zones for the 2027 lightning protection refit' if len(refs) == 15 else
                  '%d zones for the 2027 lightning protection refit' % len(refs))
    r.bold = True
    r.font.size = Pt(13)
    for line in ('To: %s, Technical Services Department Manager' % C.PEOPLE['tsd_manager'],
                 'From: %s, Reliability and Protection' % C.PEOPLE['reliability'],
                 'Date: 10 November 2026',
                 'Subject: 2027 Lightning Protection Refit, the zones the referral rule names and the rule itself'):
        _small(doc.add_paragraph(line), 9)
    by_sub = {}
    for z in refs:
        by_sub.setdefault(zr.Substation[z], []).append(zones[z])
    parts = ['%s %s' % (sub, ' and '.join(zs) if len(zs) < 3 else ', '.join(zs[:-1]) + ' and ' + zs[-1])
             for sub, zs in by_sub.items()]
    doc.add_paragraph('Refit these %d zones before the 2027 lightning season. By substation: %s.' % (
        len(refs), '; '.join(parts)))
    a = R['alerts']
    st_ = F['season_totals']
    doc.add_paragraph(
        'How the rule works. A lightning fault is a fault whose first trip lines up with a ground stroke the Kidlat '
        'service located within %d m of the zone\'s lines, counted once against the zone it was on (terms 2(c)). The '
        'breakers and the radio reclosers report in SCADA time. The %d reclosers read on site keep their own clocks, '
        'which drift between visits and are reset at each read, so each one\'s clock is fitted read by read from its own '
        'trips against the strokes. What a zone\'s lines would have with sound protection has two parts: the lightning '
        'near them times a rate for their construction, area, arrester cover and transformers, and the zone\'s own level, '
        'which stays with it whatever the state of its protection (the soil its grounds are driven into, its hardware and '
        'its route). Both are learned only from the %d zone-seasons a later cyclic inspection found sound, each zone\'s '
        'level from its own such seasons and never from the seasons being judged. The levels spread with a coefficient '
        'of variation of %.2f across zones, far more than a zone moves from season to season, so a zone that runs high '
        'when sound runs high every season and is not a failure. After each season the rule refers a zone when its faults '
        'since its last cyclic inspection are more than that expectation by more than chance explains, with its level as '
        'uncertain as its confirmed seasons leave it, at a chance below 1 in %d a zone a season: across %d zones, one '
        'sound zone referred in five seasons, the limit in terms 3(b). For the reclosers read on site the comparison runs '
        'over the months each memory holds.' % (F['match_radius_m'], F['n_radioless'], F['confirmed_sound_zone_seasons'],
                                                 F['level_cv'], F['alpha_one_in'], F['n_zones']))
    doc.add_paragraph(
        'Alert load. Run as it stands after each season, the rule would have referred %d zones after 2022, %d after '
        '2023, %d after 2024, %d after 2025 and %d after 2026. Summing each zone\'s chance at the count it would first be '
        'referred at, about %.2f of a season\'s referrals should be zones with sound protection, one in about %s '
        'seasons. Taking each zone\'s level as if it were known would refer %d zones after 2026, and would refer a sound '
        'zone about %.1f times a season, against the once in five seasons terms 3(b) allows.' % (
            a[2022], a[2023], a[2024], a[2025], a[2026], F['false_per_season'], WORDS[int(round(1 / F['false_per_season']))],
            F['known_level_referred'], F['known_level_false_true']))
    doc.add_paragraph(
        'Against the inspections. The cyclic rounds of 2022-23 to 2025-26 inspected %d zones the rule had referred after '
        'the season before, and confirmed %d of those referrals. They found failed protection on %d zones the rule had '
        'not referred, mostly failures too recent to have run up enough faults since the zone\'s last inspection.' % (
            F['validation']['referred_inspected'], F['validation']['confirmed'], F['validation']['missed']))
    doc.add_paragraph(
        'Lightning faults by season. The network had {:,} lightning faults in 2022, {:,} in 2023, {:,} in 2024, {:,} in '
        '2025 and {:,} in 2026. Of 2026\'s, {:,} were on the zones whose reclosers are read on site; their memories held '
        '{:,}, and the rest are the months they overwrote or nobody has read since the last visit, taken at each zone\'s '
        'own rate. With every zone\'s protection sound the 2026 season would have had {:,}, so failed protection caused '
        '{:,}.'.format(st_['2022'], st_['2023'], st_['2024'], st_['2025'], st_['2026'], F['radioless_2026'],
                       F['radioless_2026_logged'], F['sound_2026'], F['excess_2026']))
    doc.add_paragraph('The refit. Restoring the %d zones avoids about %d lightning faults in a season with the average '
                      'lightning of 2022 to 2026, with their protection as it stood at the end of the 2026 season (terms '
                      '4(c)). Most of them failed partway through their record since inspection: %d of them ran, in '
                      'their first season after it, at less than half the multiple of their own sound level they '
                      'reached in 2026, and %s ran above twice that level in 2026. So the '
                      'refit is valued on each zone\'s 2026 season above its own sound level, taken at that lightning; '
                      'the seasons since each failure began give %d. The record since each inspection, averaged, would '
                      'put it at %d, because it mixes in the seasons before the failure.' % (
                          len(refs), F['avoided_average_season'], F['referred_first_season_low'],
                          ('all %d' % len(refs)) if F['referred_last_season_high'] == len(refs) else
                          '%d' % F['referred_last_season_high'], F['avoided_post_onset'],
                          F['routes']['window_average']['avoided_average_season']))
    doc.add_picture(png, width=Mm(160))
    _small(doc.add_paragraph('Figure 1. Each of the %d zones\' lightning faults since its last cyclic inspection against '
                             'what sound protection would have given it.' % F['n_zones']), 8.5)
    doc.add_paragraph('')
    _small(doc.add_paragraph('Table 1. The referred zones'), 9).runs[0].bold = True
    tb = doc.add_table(rows=1, cols=4)
    tb.style = 'Table Grid'
    for i, hd in enumerate(['Zone', 'Faults since inspection', 'Sound expectation', 'Ratio']):
        tb.rows[0].cells[i].text = hd
    Tr = T.set_index('zone')
    for zn in names:
        c = tb.add_row().cells
        c[0].text = zn
        c[1].text = '%.1f' % Tr.faults_since_inspection[zn]
        c[2].text = '%.1f' % Tr.sound_expected_since_inspection[zn]
        c[3].text = '%.2f' % Tr.ratio[zn]
    _small(doc.add_paragraph('Source: SCADA event history and recloser memory downloads to October 2026, Kidlat stroke '
                             'extract November 2016 to October 2026, cyclic inspection log through the 2025-26 round.'),
           8, italic=True)
    doc.add_paragraph('')
    _small(doc.add_paragraph('Table 2. What simpler versions of the rule would have given, on the same files'), 9).runs[0].bold = True
    tr = doc.add_table(rows=1, cols=6)
    tr.style = 'Table Grid'
    for i, hd in enumerate(['Version', 'Zones referred after 2026', 'Referrals the next inspection found sound',
                            '2026 lightning faults', 'Caused by failed protection', 'Avoided, average season']):
        tr.rows[0].cells[i].text = hd
    vg = F['validation']
    rows = [('This rule', F['n_referred'], vg['referred_inspected'] - vg['confirmed'], F['faults_2026'], F['excess_2026'],
             F['avoided_average_season'])]
    for k in ('independent_seasons', 'known_level', 'no_own_level', 'window_average', 'logs_as_recorded',
              'unverified_baseline', 'poisson', 'whole_record'):
        v = F['routes'][k]
        rows.append((v['label'], v['n_referred'], v['validation']['referred_inspected'] - v['validation']['confirmed'],
                     v['faults_2026'], v['excess_2026'], v['avoided_average_season']))
    for r in rows:
        c = tr.add_row().cells
        c[0].text = r[0]
        for i in range(1, 6):
            c[i].text = '{:,}'.format(r[i])
    for t in (tb, tr):
        for row in t.rows:
            for c in row.cells:
                for p in c.paragraphs:
                    for rr in p.runs:
                        rr.font.size = Pt(8.5)
    doc.add_paragraph('')
    _small(doc.add_paragraph(
        'Notes. Seasons run 1 April to 31 October (terms 2(b)). A zone\'s record since its last inspection starts the day '
        'after that inspection\'s repairs were completed (terms 2(e)). Reclosers with no radio link were last read between '
        '%s and %s, so their unread months differ zone by zone.' % last_reads(R)), 8.5)
    fp = sec.footer.paragraphs[0]
    fr = fp.add_run('KALVECO Technical Services, Reliability and Protection. 2027 Lightning Protection Refit.   Page ')
    fr.font.size = Pt(8)
    fr.font.color.rgb = RGBColor.from_string('555555')
    OP._page_field(fp)
    cp = doc.core_properties
    cp.title = '2027 Lightning Protection Refit: zones and rule'
    cp.author = C.PEOPLE['reliability']
    cp.last_modified_by = C.PEOPLE['reliability']
    doc.save(path)
    a, b = C.GOLD_STAMP['note']
    PP.normalize_docx(path, C.PEOPLE['reliability'], C.PEOPLE['reliability'], C.utc_z(a), C.utc_z(b), 4, 96, 1313,
                      title='2027 Lightning Protection Refit: zones and rule', company=C.ORG)


def build(target, out, figures=None, R=None):
    R = R or A.run(target)
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    T = table(R)
    csv = os.path.join(out, C.DELIVERABLES[0])
    T.to_csv(csv, index=False, lineterminator='\r\n')
    F = make_figures(R, T)
    import tempfile
    png = os.path.join(tempfile.mkdtemp(), 'chart.png')
    chart(R, T, F, png)
    note(R, T, F, os.path.join(out, C.DELIVERABLES[1]), png)
    PP.own_mtimes(out, {C.DELIVERABLES[0]: C.local(C.GOLD_STAMP['csv'][1])})
    if figures:
        json.dump(F, open(figures, 'w'), indent=1, sort_keys=True)
    return R, T, F
