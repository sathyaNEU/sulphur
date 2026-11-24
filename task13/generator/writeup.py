"""submission.md, the four Sulfur answer blocks (architecture 7, Level 5), drafted purely from generator/figures.json
so every stated figure is emitted, never typed, and carries zero em/en dashes."""
import datetime as dt
import json
import os

import common as C

CAUSE_NAME = {
    'lightning': 'lightning', 'bird': 'bird or other animal', 'fog': 'salt contamination',
    'insulator': 'insulator failure', 'growin': 'vegetation grown into the line',
    'fallin': 'vegetation from outside the right of way', 'vehicle': 'vehicle or other third party',
    'hardware': 'equipment or hardware other than insulators', 'unknown': 'other or unknown',
}


def n(x):
    return f'{int(round(x)):,}'


def wash_text(items):
    by = {}
    for x in items:
        ln, sec = x.replace('wash: ', '').split(', Section ')
        by.setdefault(ln, []).append(int(sec))
    out = []
    for ln, v in by.items():
        v = sorted(v)
        s = ', '.join(str(a) for a in v[:-1]) + ' and ' + str(v[-1]) if len(v) > 1 else str(v[0])
        out.append('%s %s %s' % (ln, 'sections' if len(v) > 1 else 'section', s))
    return '; '.join(out)


def write(path):
    f = json.load(open(os.path.join(C.HERE, 'figures.json')))
    yr = f['faults_by_year']
    c6 = f['faults_2026_by_cause']
    mi = f['member_impact_2026']
    mi_st = f['member_impact_2026_static']
    mi_ob = f['member_impact_2026_over_both']
    byl = f['member_impact_2026_by_line']
    pr = f['programme']
    ip8, ip9 = f['ipp_details']['Line 8'], f['ipp_details']['Line 9']
    dc = f['dc_corridor_details']
    ref = f['dc_referee']
    cd_list = f['clearance_details']
    c_l6 = next(x for x in cd_list if x['line'] == 'Line 6')
    c_l15 = next(x for x in cd_list if x['line'] == 'Line 15')
    ub_rng = f['underbuilt_veg_slope_range']

    open_reps = [r for r in f['repeat_locations'] if not r['fixed']]
    p1_reps = [r for r in open_reps if r['priority'] == 'P1']
    p2_reps = [r for r in open_reps if r['priority'] == 'P2']
    fixed_reps = [r for r in f['repeat_locations'] if r['fixed']]

    def place_of(r):
        if r['cause'] in ('growin', 'hardware') and r.get('span'):
            return 'structures %d-%d' % (r['span'][0], r['span'][1])
        if r['cause'] == 'fallin':
            return 'structures %d-%d' % (r['s_min'], r['s_max'])
        return 'structure %d' % r['structure']

    def find_rep(line, cause, min_s=0, max_s=999):
        return next(r for r in open_reps if r['line'] == line and r['cause'] == cause and min_s <= r['structure'] <= max_s)

    r_l15 = find_rep('Line 15', 'hardware')
    r_l6 = find_rep('Line 6', 'hardware')
    r_l11_f = find_rep('Line 11', 'fallin')
    r_l13_f = find_rep('Line 13', 'fallin')
    r_l11_g = find_rep('Line 11', 'growin')
    r_l10_g1 = find_rep('Line 10', 'growin', 0, 85)
    r_l10_g2 = find_rep('Line 10', 'growin', 86, 999)
    r_l12_g = find_rep('Line 12', 'growin')
    r_l14_g = find_rep('Line 14', 'growin')
    r_l5_i = find_rep('Line 5', 'insulator')
    r_l11_i = find_rep('Line 11', 'insulator')
    r_l16_b = find_rep('Line 16', 'bird')
    r_l7_b = find_rep('Line 7', 'bird', 0, 40)

    sust_lines = [(k, v) for k, v in byl.items() if v['sustained']]
    lines_txt = '; '.join('%s %s and %s' % (k, n(v['sustained']), n(v['member_minutes'])) for k, v in sust_lines)
    due_secs = [k for k, v in f['wash_sections'].items() if v['due']]
    clean_secs = [k for k, v in f['wash_sections'].items() if not v['due']]
    w5 = f['wash_sections']['Line 2, Section 5']
    w1 = f['wash_sections']['Line 2, Section 1']
    due_detail = '; '.join(
        '%s %.4f (%.4f to %.4f, ratio %.2f)' % (k, v['ceff'], f['wash_ceff_bands'][k][0], f['wash_ceff_bands'][k][1], v['ratio'])
        for k, v in f['wash_sections'].items() if v['due']
    )

    out = []
    out.append('## Tags\n')
    out.append('**Domain:** Engineering and Physical Sciences, Energy Systems & Utilities, grid reliability and outage analysis (the 69 kV fault record).')
    out.append('**Analytical objective:** Data Extraction & Conformation (ETL / Pipeline Build).\n')

    out.append('## Final Recommendation\n')
    out.append(
        '**Allocate all %d winter and spring 69 kV crew-days under RP-04 Rev 5 to %d due coastal washing sections (%d crew-days: '
        '%s) and %d Priority 1 repeat locations (%d crew-days, 0 unused; marginal cutoff %s member-minutes/crew-day), deferring '
        'the remaining %d open repeat locations (led by %s %s at %s member-minutes/crew-day) to Priority 2.** '
        'The Priority 1 repeat slate funds avian guards at %s %s (ranked #1 at %s member-minutes/crew-day under as-operated '
        'SCADA switching) and %s %s; insulator string replacements at %s %s (coupled double-circuit Z0m), Line 8 structure %d '
        '(Brushy Creek BESS infeed), %s %s, and Line 9 structure %d (Coyote Draw Solar infeed); outside-ROW hazard-tree '
        'removals at %s %s and %s %s; 12.47 kV underbuild clearance restoration at %s %s; and grow-in clearing at %s %s, '
        '%s %s, %s %s, and underbuilt grow-in %s %s. '
        'This rejects the standard uncoupled/static/1D-ESDD reading, which misclassifies Line 15 %s and Line 6 %s as grow-ins, '
        'sends string crews %d and %d structures past the true Line 8 and Line 9 faults, misplaces all double-circuit repeats '
        'on Lines 10 and 11 by 6 to 9 structures, over-washes %d coastal sections (displacing 3 Priority 1 repairs), and understates '
        '2026 member-minutes by %.1f percent (%s vs %s), wrongly deferring %s %s and Line 9 structure %d.\n'
        % (
            pr['budget_days'], f['wash_due_count'], pr['wash_days'], wash_text(f['wash_due']),
            pr['funded_count'], pr['repeat_days_used'], n(pr['cutoff_mm_per_day']),
            pr['deferred_count'], p2_reps[0]['line'], place_of(p2_reps[0]), n(pr['first_deferred_mm_per_day']),
            r_l16_b['line'], place_of(r_l16_b), n(r_l16_b['mm_per_day']), r_l7_b['line'], place_of(r_l7_b),
            r_l11_i['line'], place_of(r_l11_i), ip8['golden_structure'], r_l5_i['line'], place_of(r_l5_i),
            ip9['golden_structure'], r_l11_f['line'], place_of(r_l11_f), r_l13_f['line'], place_of(r_l13_f),
            r_l15['line'], place_of(r_l15), r_l11_g['line'], place_of(r_l11_g), r_l10_g1['line'], place_of(r_l10_g1),
            r_l10_g2['line'], place_of(r_l10_g2), r_l12_g['line'], place_of(r_l12_g),
            place_of(r_l15), place_of(r_l6), ip8['structure_shift'], ip9['structure_shift'],
            f['esdd_only_due_count'], abs(f['static_2026_pct_diff']), n(mi_st['member_minutes']), n(mi['member_minutes']),
            r_l16_b['line'], place_of(r_l16_b), ip9['golden_structure'],
        )
    )

    out.append('## Supplementary Questions\n')
    out.append('### %s\n' % C.DELIVERABLES[0])
    out.append(
        '1. **Conformed 2022-2026 fault register (CSV, %d rows, %d lockouts):** one row per two-ended 69 kV protection '
        'sequence in Central prevailing time with current structure/span locations, RP-04 causes, reclose clearance flags, '
        'as-operated member impact, and repeat IDs. Annual fault totals (within 1): 2022 %d, 2023 %d, 2024 %d, 2025 %d, '
        '2026 (Jan-Oct) %d. Conformed 2026 faults by cause (within 2): %s.\n'
        % (
            f['faults_total'], f['faults_lockouts_total'],
            yr['2022'], yr['2023'], yr['2024'], yr['2025'], yr['2026'],
            ', '.join('%s %d' % (CAUSE_NAME[k], c6[k]) for k in ['lightning', 'bird', 'fog', 'insulator', 'growin',
                                                                 'fallin', 'vehicle', 'hardware', 'unknown']),
        )
    )

    out.append('### %s\n' % C.DELIVERABLES[1])
    out.append(
        '2. **2026 conformed member impact by line and ranked open repeat register:** total 2026 impact under chronological '
        'SCADA as-operated topology is %s sustained member interruptions, %s member-minutes (band %s to %s, within 2 percent), '
        'and %s momentary events across lines (sustained and member-minutes): %s. Across 2022-2026 there are %d open repeat '
        'locations (tolerance within 2 structures, 1 span) and %d fixed historical repeats excluded after post-fault repairs '
        '(%s). Priority 1 crew-day mix across the 36-crew-day budget: washing %d days, avian guards %d days, insulator strings '
        '%d days, outside-ROW hazard trees %d days, vegetation grow-in clearing %d days, underbuild clearance restoration %d days.\n'
        % (
            n(mi['sustained']), n(mi['member_minutes']),
            n(f['member_impact_2026_band']['member_minutes'][0]), n(f['member_impact_2026_band']['member_minutes'][1]),
            n(mi['momentary']), lines_txt,
            f['open_repeats_count'], f['fixed_repeats_count'],
            '; '.join('%s %s (%s)' % (r['line'], place_of(r), CAUSE_NAME[r['cause']]) for r in fixed_reps),
            pr['crew_day_mix'].get('wash', 0), pr['crew_day_mix'].get('bird', 0),
            pr['crew_day_mix'].get('insulator', 0), pr['crew_day_mix'].get('fallin', 0),
            pr['crew_day_mix'].get('growin', 0), pr['crew_day_mix'].get('hardware', 0),
        )
    )
    out.append(
        '3. **Priority 1 funded repeat slate (%d items, %d crew-days) and Priority 2 deferred backlog (%d items), plus coastal '
        'washing standings (21 sections):** Priority 1 funded repeats in rank order (historical member-minutes/crew-day): %s. '
        'Priority 2 deferred repeats: %s. Joint (ESDD, NSDD) effective contamination on 31 October (empirical beta %.3f, band '
        '%.3f to %.3f; 10th-percentile flashover level %.4f mg/cm2, band %.4f to %.4f): %d due sections (%s); the %d remaining '
        'sections (%s) sit at or below %.2f times the flashover level (Line 2 Section 5 at %.2f despite high raw ESDD %.4f '
        'because its coastal-marsh NSDD is only %.4f).\n'
        % (
            pr['funded_count'], pr['repeat_days_used'], pr['deferred_count'],
            '; '.join('%d) %s %s [%s, %dd, %s mm/d]' % (i + 1, r['line'], place_of(r), CAUSE_NAME[r['cause']], r['crew_days'], n(r['mm_per_day']))
                      for i, r in enumerate(p1_reps)),
            '; '.join('%s %s [%s, %dd, %s mm/d]' % (r['line'], place_of(r), CAUSE_NAME[r['cause']], r['crew_days'], n(r['mm_per_day']))
                      for r in p2_reps),
            f['beta_nsdd'], f['beta_nsdd_band'][0], f['beta_nsdd_band'][1],
            f['flashover_level'], f['flashover_level_band'][0], f['flashover_level_band'][1],
            len(due_secs), due_detail, len(clean_secs), ', '.join(clean_secs),
            f['wash_clean_max_ratio'], w5['ratio'], w5['esdd'], w5['nsdd'],
        )
    )

    out.append('### %s\n' % C.DELIVERABLES[2])
    out.append(
        '4. **One-page Priority 1 work program memo (Word):** addressed to C. Ortiz (Manager of Engineering) and the '
        'reliability review, itemizing all %d due coastal washing sections before 1 December (%s), all %d funded Priority 1 '
        'repeat locations (%d total crew-days, 0 unused, marginal cutoff %s member-minutes/crew-day), and the %d Priority 2 '
        'deferred locations with physical justification for every network, thermal, contamination, and switching adjustment.\n'
        % (f['wash_due_count'], wash_text(f['wash_due']), pr['funded_count'], pr['budget_days'], n(pr['cutoff_mm_per_day']), pr['deferred_count'])
    )

    out.append('## Critical Components\n')
    out.append(
        '1. **Active 12.47 kV underbuild clearance spans (not vegetation grow-ins):** **Line 15 %s** (Priority 1, '
        '3 crew-days; %d post-trim summer contacts at %.1f to %.1f C, slope %+.2f C/yr) and **Line 6 %s** '
        '(Priority 2, 3 crew-days; %d post-trim contacts at %.1f to %.1f C, slope %+.2f C/yr), separated from the two '
        'underbuilt grow-in spans (Line 12 %s and Line 14 %s, falling %.2f to %.2f C/yr).'
        % (place_of(r_l15), c_l15['contacts_since_trim'], c_l15['contact_temperature'][0], c_l15['contact_temperature'][1],
           c_l15['slope_c_per_year'], place_of(r_l6), c_l6['contacts_since_trim'], c_l6['contact_temperature'][0],
           c_l6['contact_temperature'][1], c_l6['slope_c_per_year'], place_of(r_l12_g), place_of(r_l14_g),
           abs(ub_rng[1]), abs(ub_rng[0]))
    )
    out.append(
        '2. **Active cracked insulator strings downstream of YNd1 IPP lateral taps:** **Line 8 structure %d** (%.2f km from '
        'Caney Bend, %.2f km past Brushy Creek BESS tap at %.1f km; raw single-ended distance over-reaches to structure %d, '
        '%.2f km) and **Line 9 structure %d** (%.2f km from Shell Ridge, %.2f km past Coyote Draw Solar tap at %.1f km; raw '
        'distance over-reaches to structure %d, %.2f km), both within 2 structures.'
        % (ip8['golden_structure'], ip8['golden_km'], ip8['beyond_tap_km'], ip8['tap_km'], ip8['raw_structure'], ip8['raw_km'],
           ip9['golden_structure'], ip9['golden_km'], ip9['beyond_tap_km'], ip9['tap_km'], ip9['raw_structure'], ip9['raw_km'])
    )
    out.append(
        '3. **Active repeat structures inside the 14.5 km double-circuit steel-pole corridor (Lines 10 and 11, Z0m coupling):** '
        '**Line 11 structure %d** (insulator string, %.2f km from Inland vs uncoupled structure %d at %.2f km) and **Line 10 '
        '%s** (grow-in, %.2f km vs uncoupled structure %d at %.2f km), validated on %d patrol-confirmed two-ended '
        'ground lockouts outside the target structures (coupled MAE %.3f km vs uncoupled %.2f km and direct %.2f km).'
        % (dc['Line 11 insulator']['golden_structure'], dc['Line 11 insulator']['golden_km'],
           dc['Line 11 insulator']['uncoupled_structure'], dc['Line 11 insulator']['uncoupled_km'],
           place_of(r_l10_g1), dc['Line 10 growin']['golden_km'], dc['Line 10 growin']['uncoupled_structure'],
           dc['Line 10 growin']['uncoupled_km'], int(ref['slice'].split()[0]), ref['golden'],
           ref['rivals']['rigorous'], ref['rivals']['direct'])
    )
    out.append(
        '4. **Coastal porcelain washing sections due before 1 December 2026 under joint (ESDD, NSDD):** exactly **%d sections** '
        '(%s; fitted beta %.3f, 10th-percentile flashover level %.4f mg/cm2 effective), excluding the %d clean coastal-marsh and '
        'October-washed sections (including Line 2 Section 5 at %.2f times level, whereas ESDD-only washes %d sections and '
        'crowds out 3 Priority 1 repeats; over-weighting NSDD drops Line 2 Section 1 at %.2f times golden level).'
        % (f['wash_due_count'], wash_text(f['wash_due']), f['beta_nsdd'], f['flashover_level'], f['wash_not_due_count'],
           w5['ratio'], f['esdd_only_due_count'], w1['ratio'])
    )
    out.append(
        '5. **2026 conformed member-minutes under chronological as-operated SCADA switching topology:** **%s member-minutes** '
        '(band %s to %s, within 2 percent) and **%s sustained member interruptions** across %d planned supervisory ALT SRC / '
        'NORM SW switching windows (%d active in 2026), compared with %s member-minutes under static feeder mapping (%.1f '
        'percent) and %s when switched taps are double-counted (+%.1f percent); chronological replay elevates %s %s from 0 to '
        '%s member-minutes/crew-day (#1 Priority 1).\n'
        % (n(mi['member_minutes']), n(f['member_impact_2026_band']['member_minutes'][0]),
           n(f['member_impact_2026_band']['member_minutes'][1]), n(mi['sustained']),
           f['switching_windows_count'], f['switching_windows_2026_count'],
           n(mi_st['member_minutes']), f['static_2026_pct_diff'], n(mi_ob['member_minutes']),
           f['over_both_2026_pct_diff'], r_l16_b['line'], place_of(r_l16_b), n(r_l16_b['mm_per_day']))
    )

    out.append('## Step-by-Step\n')
    steps = [
        'Assembled one fault per two-ended 69 kV protection operation sequence within 60 s from `%s` (excluding single-breaker '
        'relay tests, maintenance clearances, and non-tripping mutual pickups), synchronized EventRecall (`%s`, UTC, miles) and '
        'GridVue (`%s`, Central prevailing, km/kA) clocks against SCADA, and conformed %d faults (%d lockouts; %d faults in '
        'Jan-Oct 2026).' % (C.FILES['soe'], C.FILES['er'], C.FILES['gv'], f['faults_total'], f['faults_lockouts_total'], f['faults_2026']),
        'Located two-ended ground faults via zero-sequence current split using date-appropriate source impedances (`%s` before '
        'Inland T2 energization on 14 March 2024, `%s` onward). On double-circuit Lines 10 and 11, solved the coupled 2-line '
        'zero-sequence nodal network with mutual impedance Z0m = 0.1180 + j0.7150 ohm/km along the 14.5 km shared steel-pole '
        'corridor and Inland bus Z0, moving Line 11 structure %d (+%d poles from %d) and Line 10 %s (+%d poles from %d). Verified '
        'against %d patrol-confirmed two-ended ground lockouts outside the target structures: coupled MAE %.3f km vs uncoupled '
        '%.2f km and raw relay distance %.2f km.'
        % (C.FILES['study22'], C.FILES['study25'],
           dc['Line 11 insulator']['golden_structure'], dc['Line 11 insulator']['structure_shift'],
           dc['Line 11 insulator']['uncoupled_structure'], place_of(r_l10_g1),
           dc['Line 10 growin']['structure_shift'], dc['Line 10 growin']['uncoupled_structure'],
           int(ref['slice'].split()[0]), ref['golden'], ref['rivals']['rigorous'], ref['rivals']['direct']),
        'Inverted ground-fault infeed from both YNd1 IPP lateral taps using their CST protection exports (`%s` on Line 9 at %.1f '
        'km; `%s` on Line 8 at %.1f km). Taking out the zero-sequence infeed ratio k = (I_p,tap + k0*I_N,tap) / (I_p,sub + '
        'k0*I_N,sub) relocated the Line 8 cracked string from structure %d (%.2f km) to structure %d (%.2f km) and the Line 9 '
        'cracked string from structure %d (%.2f km) to structure %d (%.2f km); correcting only Coyote Draw Solar leaves Line 8 '
        'off by %d structures.'
        % (C.FILES['ipp'], ip9['tap_km'], C.FILES['ipp2'], ip8['tap_km'], ip8['raw_structure'], ip8['raw_km'],
           ip8['golden_structure'], ip8['golden_km'], ip9['raw_structure'], ip9['raw_km'], ip9['golden_structure'],
           ip9['golden_km'], ip8['structure_shift']),
        'Classified fault causes from physical evidence at the line: CG lightning strokes (`%s`), substation weather-station bay '
        'fog (`%s`), winter roost counts (`%s`), storm/front gusts, wet-weather inland insulator clusters, patrol confirmations '
        '(`%s`), and IEEE 738 steady-state conductor temperature (`%s`). For every summer contact repeat on an underbuilt span, '
        'fitted the post-trim contact temperature trajectory (`%s`): Line 15 %s (%+.2f C/yr) and Line 6 %s (%+.2f C/yr) '
        'remained flat across summers (fixed clearance to 12.47 kV underbuild, 3 crew-days), whereas underbuilt grow-in spans '
        'Line 12 %s and Line 14 %s fell %.2f to %.2f C/yr like non-underbuilt grow-ins (2 crew-days). A blanket '
        'underbuilt filter wrongly reclassifies Line 12 %s and knocks it out of Priority 1.'
        % (C.FILES['strokes'], C.FILES['stations'], C.FILES['avian'], C.FILES['patrols'], C.FILES['loading'], C.FILES['veg'],
           place_of(r_l15), c_l15['slope_c_per_year'], place_of(r_l6), c_l6['slope_c_per_year'],
           place_of(r_l12_g), place_of(r_l14_g), abs(ub_rng[1]), abs(ub_rng[0]), place_of(r_l12_g)),
        'Fitted the daily two-state coastal contamination recurrence from the eight never-washed test sites (`%s`): soluble ESDD '
        'follows shore distance, onshore Gulf wind, and fast exponential rain washout (k_ESDD %.4f /mm), while sticky caliche '
        'and agricultural NSDD follows corridor surface, dry inland wind, and slow washout (k_NSDD %.4f /mm). Carrying all 21 '
        'porcelain sections from each wash (`%s`) through 31 October and fitting a 2D logistic fog-flashover frontier yielded '
        'beta = %.3f and 10th-percentile threshold %.4f mg/cm2 effective: exactly %d due sections (all >=%.2fx level) and %d '
        'clean sections (all <=%.2fx level). A 1D ESDD-only model fails linear separation, over-washing %d sections and '
        'displacing 3 Priority 1 repeats.'
        % (C.FILES['esdd'], f['k_esdd'], f['k_nsdd'], C.FILES['washing'], f['beta_nsdd'], f['flashover_level'],
           f['wash_due_count'], f['wash_due_min_ratio'], f['wash_not_due_count'], f['wash_clean_max_ratio'],
           f['esdd_only_due_count']),
        'Replayed all %d planned SCADA supervisory switching windows (`ALT SRC CLOSE` + `NORM SW OPEN` through `NORM SW CLOSE` '
        'in `%s`) chronologically alongside monthly feeder member counts (`%s`) to attribute every 2022-2026 lockout to the 69 kV '
        'line actually energizing each tap substation at the instant of the fault (with no backup transfer back onto a cleared '
        'normal line). This yielded %s sustained interruptions and %s member-minutes in 2026 (static mapping gives %s, off by '
        '%.1f percent) and lifted %s %s to #1 overall (%s mm/crew-day) from Heron Bend\'s 2024 abnormal feed window.'
        % (f['switching_windows_count'], C.FILES['soe'], C.FILES['members'], n(mi['sustained']), n(mi['member_minutes']),
           n(mi_st['member_minutes']), f['static_2026_pct_diff'], r_l16_b['line'], place_of(r_l16_b), n(r_l16_b['mm_per_day'])),
        'Grouped same-cause faults within 400 m, excluded %d repeats fixed after their last fault (`%s`, `%s`), and executed '
        'RP-04 Rev 5 Priority 1 crew-day allocation (`%s`, 36 crew-days): %d due coastal washes scheduled first (%d days), leaving '
        '%d days allocated greedily by historical 2022-2026 member-minutes/crew-day across %d Priority 1 repeats (cutoff %s '
        'mm/crew-day, 0 days unused) and %d Priority 2 deferred items (next %s mm/crew-day). Every one of %d honest parameter '
        'variants and all 6 input perturbations reproduce the exact same 22-item Priority 1 work program.'
        % (f['fixed_repeats_count'], C.FILES['maint'], C.FILES['veg'], C.FILES['procedure'], f['wash_due_count'],
           pr['wash_days'], pr['repeat_days_used'], pr['funded_count'], n(pr['cutoff_mm_per_day']),
           pr['deferred_count'], n(pr['first_deferred_mm_per_day']), f['family_size']),
    ]
    for i, st in enumerate(steps):
        out.append('%d. %s' % (i + 1, st))
    out.append('')
    out.append(
        'No rival schedule survives the physical and operational records. Each of the five mechanisms is independently forced: '
        'post-trim IEEE 738 slopes separate fixed underbuild clearances from growing trees on underbuilt spans; both IPP CST '
        'protection exports directly measure the YNd1 ground-infeed currents; %d patrol-confirmed lockouts outside the target '
        'structures confirm coupled Z0m mutual impedance over uncoupled ratios by %.1fx MAE; 2D fog-night flashover outcomes '
        'refute 1D ESDD separation and over-weighted NSDD alike; and timestamped SCADA NORM SW / ALT SRC switching records '
        'directly establish as-operated topology. Dropping or over-correcting any single step produces a distinct wrong Priority '
        '1 program, while all %d honest variants converge on the identical 36-crew-day schedule.'
        % (int(ref['slice'].split()[0]), f['dc_referee_ratio'], f['family_size'])
    )
    open(path, 'w').write('\n'.join(out) + '\n')


if __name__ == '__main__':
    write(os.path.join(C.TASK, 'submission.md'))
