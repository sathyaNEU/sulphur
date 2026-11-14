"""submission.md, the four answer blocks, drafted from generator/figures.json so every figure is emitted, never typed."""
import json
import os

import common as C

CAUSE_NAME = {'lightning': 'lightning', 'bird': 'bird or other animal', 'fog': 'salt contamination',
              'insulator': 'insulator failure', 'growin': 'vegetation grown into the line',
              'fallin': 'vegetation from outside the right of way', 'vehicle': 'vehicle or other third party',
              'hardware': 'equipment or hardware other than insulators', 'unknown': 'other or unknown'}


def n(x):
    return f'{x:,}'


def places(items, prefix):
    return [x.replace(prefix, '') for x in items if x.startswith(prefix)]


def wash_text(items):
    by = {}
    for x in items:
        ln, sec = x.replace('wash: ', '').split(', Section ')
        by.setdefault(ln, []).append(int(sec))
    out = []
    for ln, v in by.items():
        v = sorted(v)
        runs, cur = [], [v[0]]
        for a in v[1:]:
            if a == cur[-1] + 1:
                cur.append(a)
            else:
                runs.append(cur)
                cur = [a]
        runs.append(cur)
        toks = []
        for r in runs:
            toks += (['%d to %d' % (r[0], r[-1])] if len(r) >= 3 else [str(a) for a in r])
        out.append('%s %s %s' % (ln, 'sections' if len(v) > 1 else 'section', toks[0] if len(toks) == 1 else ', '.join(toks[:-1]) + ' and ' + toks[-1]))
    return '; '.join(out)


def day(iso):
    import datetime as dt_
    d = dt_.date.fromisoformat(iso[:10])
    return '%d %s %d' % (d.day, d.strftime('%B'), d.year)


def day_short(iso):
    import datetime as dt_
    d = dt_.date.fromisoformat(iso[:10])
    return '%d %s' % (d.day, d.strftime('%B'))


def write(path):
    f = json.load(open(os.path.join(C.HERE, 'figures.json')))
    wl = f['work_list']
    guards = places(wl, 'perch guards: ')
    strings = places(wl, 'replace the string: ')
    spans = places(wl, 'clear the span: ')
    stands = places(wl, 'remove the hazard trees: ')
    clear = places(wl, 'restore the clearance: ')
    yr = f['faults_by_year']
    c6 = f['faults_2026_by_cause']
    mi = f['member_impact_2026']
    byl = f['member_impact_2026_by_line']
    care = f['careful']
    gs, cc, rs = f['gulf_string'], f['clearance_contact'], f['resalted']
    fixed = [r for r in f['repeat_locations'] if r['fixed']]
    tap = [x for x in strings if x.startswith('Line 9,')][0]
    sust_lines = [(k, v) for k, v in byl.items() if v['sustained']]
    lines_txt = '; '.join('%s %s and %s' % (k, n(v['sustained']), n(v['member_minutes'])) for k, v in sust_lines)
    lv, band = f['flashover_level'], f['flashover_level_band']
    w1, w6 = rs['Line 2, Section 1'], rs['Line 2, Section 6']
    cw1, cw6 = care['resalted_ratio']
    db = f['wash_deposit_bands']
    due_txt = '; '.join('%s %.3f (%.3f to %.3f)' % (k, v['deposit'], db[k][0], db[k][1]) for k, v in f['wash_sections'].items() if v['due'])
    clean = [k for k, v in f['wash_sections'].items() if not v['due']]
    clean_max = max(f['wash_sections'][k]['ratio'] for k in clean)
    vs = cc['vegetation_slopes']
    out = []
    out.append('## Tags\n')
    out.append('**Domain:** Engineering and Physical Sciences, Energy Systems & Utilities, grid reliability and outage analysis '
               '(the 69 kV fault record).')
    out.append('**Analytical objective:** Data Extraction & Conformation (ETL / Pipeline Build).\n')
    out.append('## Final Recommendation\n')
    out.append('**This winter, fit perch guards at %d roost structures, replace %d cracked strings (%s on the Gulf among them), wash %d '
               'coastal sections before 1 December (Line 2 sections 1 and 6, washed in October, among them) and remove the hazard '
               'trees at %d dead pine stands; before next summer, clear %d grow-in spans and restore the clearance at %s, where the '
               'conductor reaches the 12.47 kV circuit built under it.** Not the list the fog nights, the patrols and the test '
               'insulators\' average rate give, which leaves %s to the washing crews, clears a span whose oak was cut back in %s, and '
               'takes Line 2 sections 1 and 6 as clean at %.1f times the level where the late October wind left them at %.1f and %.1f.\n'
               % (len(guards), len(strings), strings[[i for i, x in enumerate(strings) if x.startswith(gs['line'] + ',')][0]],
                  len(f['wash_due']), len(stands), len(spans), clear[0], '%s structure %d' % (gs['line'], gs['structure']),
                  cc['trim'][:4], max(cw1, cw6), w1['ratio'], w6['ratio']))
    out.append('## Supplementary Questions\n')
    out.append('### %s\n' % C.DELIVERABLES[0])
    out.append('1. One row per 69 kV fault since 1 January 2022, %d rows, in time order: date and time (Central), line and its '
               'terminals, distance from terminal A, the structure (and the span for a contact or a tree), fault type, cause in the '
               'procedure\'s categories, whether it cleared on reclose, members interrupted, member-minutes, momentary members, and '
               'the repeat location it belongs to. Faults by year: 2022 %d, 2023 %d, 2024 %d, 2025 %d, 2026 (January to October) %d, '
               'each within 1.\n' % (f['faults_total'], yr['2022'], yr['2023'], yr['2024'], yr['2025'], yr['2026']))
    out.append('### %s\n' % C.DELIVERABLES[1])
    out.append('2. Faults by line and cause for each year. The 2026 faults by cause: %s, each within 2%s.' %
               (', '.join('%s %d' % (CAUSE_NAME[k], c6[k]) for k in ['lightning', 'bird', 'fog', 'insulator', 'growin', 'fallin',
                                                                     'vehicle', 'hardware', 'unknown']),
               ' (equipment or hardware and other or unknown each within 3, the Line 6 contacts read as either)'))
    out.append('3. The 2026 member interruptions and member-minutes by line: %s member interruptions and %s member-minutes in all, '
               'each within 2 per cent; by line (interruptions and member-minutes) %s; no other line had a member out for more '
               'than five minutes.' % (n(mi['sustained']), n(mi['member_minutes']), lines_txt))
    out.append('4. Every repeat location with its cause, a structure within 2 of the one given (a span within 1): perch guards at '
               '%s (bird or other animal); replace the string at %s (insulator failure); clear the span at %s (vegetation grown into '
               'the line); remove the hazard trees at %s (vegetation from outside the right of way); restore the clearance at %s '
               '(equipment or hardware other than insulators: the conductor reaching the 12.47 kV circuit under it). Fixed after '
               'their last fault: %s.' % ('; '.join(guards), '; '.join(strings), '; '.join(spans), '; '.join(stands), clear[0],
                                          '; '.join('%s structure %d (%s)' % (r['line'], r['structure'], CAUSE_NAME[r['cause']]) for r in fixed)))
    out.append('5. Each washing section\'s salt deposit on 31 October 2026 in mg/cm2, with the range across reasonable fits, against '
               'the flashover level of %.3f mg/cm2 (%.3f to %.3f): due, %s; the other %d sections (%s), washed after the 27 October '
               'front, hold %.1f times the level or less.\n'
               % (lv, band[0], band[1], due_txt, len(clean), ', '.join(clean), clean_max))
    out.append('### %s\n' % C.DELIVERABLES[2])
    out.append('6. One page to the reliability review (the manager of engineering with the line superintendent and the '
               'vegetation management coordinator): this winter the perch guards, the four strings, the washing before 1 '
               'December (%s) and the hazard trees; before next summer the four spans and the clearance at %s; each with why the '
               'crew goes there.\n' % (wash_text(f['wash_due']), clear[0]))
    out.append('## Critical Components\n')
    out.append('1. **%s structure %d** is a cracked string, not salt: its **%d** flashovers since %s came on fog nights on %s, which '
               'the crews washed five times from November to March, and **%d** of them fell below **%.2f** of the median deposit at the '
               'Gulf\'s fog flashovers (the lowest at **%.3f** mg/cm2, %.1f times the level) while the rest of the section stayed '
               'quiet; replace it.' % (gs['line'], gs['structure'], gs['flashovers'], day(gs['first']), gs['section'], gs['below_cut'],
                                      0.6, gs['lowest_deposit'], gs['lowest_deposit'] / lv))
    out.append('2. **%s structures %s** are not a grow-in: since the oak there was cut back (%s) the conductor has reached something '
               'at **%.0f to %.0f C** every summer (a change of **%+.1f C a year**), where every grow-in\'s contact temperature falls '
               '**%.1f to %.1f C a year**; the span carries the 12.47 kV underbuild, so the clearance is restored and the span is not '
               'cleared.' % (cc['line'], cc['structures'], day(cc['trim']), cc['contact_temperature'][0], cc['contact_temperature'][1],
                            cc['slope_c_per_year'], -vs[1], -vs[0]))
    out.append('3. **Line 2 sections 1 and 6**, washed on %s and %s, are due again: **%.3f** and **%.3f** mg/cm2 on 31 October, '
               '**%.1f** and **%.1f** times the level, the onshore wind of 23 to 26 October carried through from the test insulators\' '
               'gains; read at their average rate they hold %.1f and %.1f times it.\n'
               % (day_short(w1['last_wash']), day_short(w6['last_wash']), w1['deposit'], w6['deposit'], w1['ratio'], w6['ratio'], cw1, cw6))
    out.append('## Step-by-Step\n')
    steps = [
        'Built one fault per two-ended trip sequence in `%s`, matched every relay record in `%s` and `%s` on its own clock set '
        'against SCADA, located each fault from both ends against the protection study in force on its date (`%s`, `%s`) and took '
        'the solar farm\'s ground infeed (`%s`) out of Shell Ridge\'s distance on Line 9: %d faults, %d of them in 2026, the tap '
        'line\'s string at %s.' % (C.FILES['soe'], C.FILES['er'], C.FILES['gv'], C.FILES['study22'], C.FILES['study25'],
                                    C.FILES['ipp'], f['faults_total'], yr['2026'], tap),
        'Caused each fault from what was there at the time: strokes on the true time (`%s`), storms and fronts for trees from '
        'outside the right of way, the roost survey (`%s`) for pre-dawn faults in roost season, fog at the cooperative\'s own '
        'stations (`%s`) for the Gulf porcelain, light rain for the inland strings, and the conductor\'s heat (`%s`) for summer '
        'contacts.' % (C.FILES['strokes'], C.FILES['avian'], C.FILES['stations'], C.FILES['loading']),
        'Carried each washing section\'s deposit day by day: the never-washed test insulators\' gains (`%s`) between readings with '
        'no wetting rain follow each interval\'s onshore wind at the stations (a constant rate leaves %d per cent more unexplained), '
        'so the rate is set by distance from the Gulf and each day\'s onshore wind, carried from each wash in `%s` with the rain\'s '
        'cleaning. Line 2 sections 1 and 6, washed on %s and %s, took the four days of southerly wind before the 27 October front, '
        'after every October reading: %.1f and %.1f times the level on 31 October. At the test insulators\' average rate, or read off '
        'the latest test reading, they stay below it.' % (C.FILES['esdd'], f['deposit_fit']['constant_worse_pct'], C.FILES['washing'],
                                                          day_short(w1['last_wash']), day_short(w6['last_wash']), w1['ratio'], w6['ratio']),
        'Read the deposit at every fog-night flashover on the Gulf porcelain: the median is %.3f mg/cm2, and %s structure %d '
        'flashed over %d times below %.2f of it, after each of the five washes of %s, in fog and in light rain, while no other '
        'structure there flashed. Salt flashes over only above its level; a cracked string flashes whenever it is wet. Booking '
        'every fog-night flashover as salt leaves it off the list and drags the level down with it.' % (gs['median_fog_deposit'], gs['line'],
                                                                                              gs['structure'], gs['below_cut'], 0.6, gs['section']),
        'Took the level as the tenth percentile of the deposits at the remaining salt flashovers: %.3f mg/cm2 (%.3f to %.3f across '
        'the lowest, the 5th and the 20th percentiles and the other fits). %d sections are at or above it.' % (lv, band[0], band[1],
                                                                                                     len(f['wash_due'])),
        'Read each summer contact place on its own contact temperatures since its last trim (`%s`): every grow-in reaches its tree '
        '%.1f to %.1f C cooler each summer as it grows; %s structures %s have touched at %.0f to %.0f C every summer since the oak '
        'there was cut back on %s, as the patrol asked. A tree does not stand still for four summers; the span carries the 12.47 kV '
        'underbuild (`%s`). Copying the patrol and the confirmed grow-ins\' signature (hot, still, no stroke) clears the span instead.'
        % (C.FILES['veg'], -vs[1], -vs[0], cc['line'], cc['structures'], cc['contact_temperature'][0], cc['contact_temperature'][1],
           day(cc['trim']), C.FILES['structures']),
        'Grouped faults of one cause within 400 m (procedure RP-04) and took off what was fixed after the last fault (`%s`, `%s`): '
        '%d perch guards, %d strings, %d spans, %d stands and the clearance at %s.' % (C.FILES['maint'], C.FILES['veg'], len(guards),
                                                                                       len(strings), len(spans), len(stands), clear[0]),
        'Rebuilt the 2026 member impact from the SCADA trips, transfers and recloses and `%s`: %s member interruptions and %s '
        'member-minutes.' % (C.FILES['members'], n(mi['sustained']), n(mi['member_minutes'])),
    ]
    for i, st in enumerate(steps):
        out.append('%d. %s' % (i + 1, st))
    out.append('')
    out.append('No other list survives the files. Salt cannot flash over on porcelain washed four days earlier, so the flashovers '
               'that kept coming at %s structure %d after every wash are the string\'s; a tree grows, so a conductor that has touched at '
               'the same temperature for four summers and through a trim is touching something fixed; and the test insulators\' gains '
               'follow the onshore wind, so sections washed before the late October blow did not stay clean because the last reading '
               'came before it. The three are independent: each shortcut alone leaves a different item wrong, and every reasonable '
               'variant of each fit (%d of them) files the same list.' % (gs['line'], gs['structure'], f['family_size']))
    open(path, 'w').write('\n'.join(out) + '\n')


if __name__ == '__main__':
    write(os.path.join(C.TASK, 'submission.md'))
