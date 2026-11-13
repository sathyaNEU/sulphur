"""submission.md, the four answer blocks, drafted from generator/figures.json so every figure is emitted, never typed."""
import json
import os

import common as C

CAUSE_NAME = {'lightning': 'lightning', 'bird': 'bird or other animal', 'fog': 'salt contamination',
              'insulator': 'insulator failure', 'growin': 'vegetation grown into the line',
              'fallin': 'vegetation from outside the right of way', 'vehicle': 'vehicle or other third party',
              'hardware': 'equipment or hardware', 'unknown': 'other or unknown'}


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
        out.append('%s sections %s' % (ln, toks[0] if len(toks) == 1 else ', '.join(toks[:-1]) + ' and ' + toks[-1]))
    return '; '.join(out)


def write(path):
    f = json.load(open(os.path.join(C.HERE, 'figures.json')))
    wl = f['work_list']
    guards = places(wl, 'perch guards: ')
    strings = places(wl, 'replace the string: ')
    spans = places(wl, 'clear the span: ')
    stands = places(wl, 'remove the hazard trees: ')
    yr = f['faults_by_year']
    c6 = f['faults_2026_by_cause']
    mi = f['member_impact_2026']
    byl = f['member_impact_2026_by_line']
    care = f['careful']
    fixed = [r for r in f['repeat_locations'] if r['fixed']]
    tap = f['tap_repeat_location'][0].replace('replace the string: ', '')
    care_tap = care['R4'][0].replace('replace the string: ', '') if care['R4'] else 'none'
    lo, hi = f['growin_relay_offset_km']
    sust_lines = [(k, v) for k, v in byl.items() if v['sustained']]
    lines_txt = '; '.join('%s %s and %s' % (k, n(v['sustained']), n(v['member_minutes'])) for k, v in sust_lines)
    care_strings = places(care['R3'], 'replace the string: ')
    care_spans = care['R2']
    out = []
    out.append('## Tags\n')
    out.append('**Domain:** Engineering and Physical Sciences, Energy Systems & Utilities, grid reliability and outage analysis '
               '(the 69 kV fault record).')
    out.append('**Analytical objective:** Data Extraction & Conformation (ETL / Pipeline Build).\n')
    out.append('## Final Recommendation\n')
    out.append('**This winter, fit perch guards at %d roost structures, replace %d cracked strings (%s among them, %.1f km past '
               'the solar tap), wash %d coastal sections before 1 December and remove the hazard trees at %d dead pine stands; '
               'before next summer, clear %d grow-in spans.** Not the list the relays\' own distances, the airport\'s fog and the '
               'past flashovers give, which replaces strings at the roost structures, clears spans where the relays put the tree '
               'contacts (%.1f to %.1f km from the trees) and washes sections already cleaned in October.\n' % (len(guards), len(strings), tap, f['tap_string_beyond_tap_km'],
                                                            len(f['wash_due']), len(stands), len(spans), lo, hi))
    out.append('## Supplementary Questions\n')
    out.append('### %s\n' % C.DELIVERABLES[0])
    out.append('1. One row per 69 kV fault since 1 January 2022, %d rows, in time order: date and time (Central), line and its '
               'terminals, distance from terminal A, the structure (and the span for a tree), fault type, cause in the procedure\'s '
               'categories, whether it cleared on reclose, members interrupted, member-minutes, momentary members, and the repeat '
               'location it belongs to. Faults by year: 2022 %d, 2023 %d, 2024 %d, 2025 %d, 2026 (January to October) %d, each '
               'within 1.\n' % (f['faults_total'], yr['2022'], yr['2023'], yr['2024'], yr['2025'], yr['2026']))
    out.append('### %s\n' % C.DELIVERABLES[1])
    out.append('2. Faults by line and cause for each year. The 2026 faults by cause: %s, each within 2.' %
               ', '.join('%s %d' % (CAUSE_NAME[k], c6[k]) for k in ['lightning', 'bird', 'fog', 'insulator', 'growin', 'fallin',
                                                                     'vehicle', 'hardware', 'unknown']))
    out.append('3. The 2026 member interruptions and member-minutes by line: %s member interruptions and %s member-minutes in all, '
               'each within 2 per cent; by line (interruptions and member-minutes) %s; no other line had a member out for more '
               'than five minutes.' % (n(mi['sustained']), n(mi['member_minutes']), lines_txt))
    out.append('4. Every repeat location with its cause, a structure within 2 of the one given (a span within 1): perch guards at '
               '%s (bird or other animal); replace the string at %s (insulator failure); clear the span at %s (vegetation grown into '
               'the line); remove the hazard trees at %s (vegetation from outside the right of way). Fixed after their last fault: '
               '%s.\n' % ('; '.join(guards), '; '.join(strings), '; '.join(spans), '; '.join(stands),
                          '; '.join('%s structure %d (%s)' % (r['line'], r['structure'], CAUSE_NAME[r['cause']]) for r in fixed)))
    out.append('### %s\n' % C.DELIVERABLES[2])
    out.append('5. One page to the manager of engineering: this winter the perch guards, the four strings, the washing before 1 '
               'December (%s) and the hazard trees; before next summer the four spans; each with why the crew goes there.\n'
               % wash_text(f['wash_due']))
    out.append('## Critical Components\n')
    out.append('1. The trees: grow-in spans to clear at **%s** and the hazard-tree stands at **%s**, located by how each fault\'s '
               'residual current split between the two ends of its line, Line 10\'s 2022 and 2023 contacts read against the 2022 '
               'protection study; the relays\' own distances put them **%.1f to %.1f km** away.' % ('; '.join(spans), '; '.join(stands), lo, hi))
    out.append('2. The night faults at **%d** roost structures are bird streamers (perch guards), not salt, and the **%d** strings that '
               'flash over in light rain at any hour are failing porcelain.' % (len(guards), len(strings)))
    out.append('3. The string on the solar tap line is at **%s**, %.1f km past the tap, not where Shell Ridge\'s relay reads it (%s).' %
               (tap, f['tap_string_beyond_tap_km'], care_tap))
    out.append('4. **%d** washing sections are due before the fog season (%s): their deposit on 31 October is at or above the '
               '**%.3f mg/cm2** at which the porcelain has flashed over in fog (%.3f to %.3f under the other defensible fits, every one '
               'of which files the same %d sections).\n' % (len(f['wash_due']), wash_text(f['wash_due']), f['flashover_level'],
                                                         f['flashover_level_band'][0], f['flashover_level_band'][1], len(f['wash_due'])))
    out.append('## Step-by-Step\n')
    steps = [
        'Built one fault per two-ended trip sequence in `%s` (both terminals\' breakers out within a second; single-ended protection '
        'trips with no fault record are relay tests) and matched every relay record in `%s` (UTC, miles) and `%s` (local time, km, kA) '
        'on its own clock, set against SCADA: %d faults, %d of them in 2026.' % (C.FILES['soe'], C.FILES['er'], C.FILES['gv'],
                                                                                  f['faults_total'], yr['2026']),
        'Located each fault by how its residual current split between the two terminals, solved against the line-out zero-sequence '
        'sources in `%s` for faults before Inland\'s new autotransformer (14 March 2024, `%s`) and `%s` after. The relays\' own '
        'distances assume no fault resistance and no infeed, and put the tree contacts %.1f to %.1f km from their spans; the 2025 study '
        'for every fault moves Line 10\'s 2022 and 2023 contacts off the span at structures 47-48, which then drops off the list.' % (C.FILES['study22'], C.FILES['subs'],
                                                                                                    C.FILES['study25'], lo, hi),
        'On Line 9, past the tap, Ponder Creek keeps no record, so Shell Ridge\'s distance was corrected for the solar farm\'s ground '
        'current from its own export (`%s`, Central Standard Time): its grounded-wye step-up feeds every fault beyond the tap, by night '
        'as well. The string is at %s; the uncorrected distance reads %s.' % (C.FILES['ipp'], tap, care_tap),
        'Caused each fault from what was there at the time: a stroke within a second along the line (`%s`), thunderstorms and fronts '
        'for trees from outside the right of way, the roost survey\'s structures (`%s`) for pre-dawn faults in roost season, fog at '
        'the cooperative\'s own stations (`%s`) for salt on the Gulf lines\' porcelain, and the conductor\'s heat from `%s` for grow-ins. '
        'The airport\'s visibility misses the fog at the line and the survey left out leaves the roosts reading as failing strings: '
        'that route replaces strings at %d places and fits no guards.' % (C.FILES['strokes'], C.FILES['avian'], C.FILES['stations'],
                                                                         C.FILES['loading'], len(care_strings)),
        'Grouped faults of one cause within 400 m (procedure RP-04) and took off what was fixed after the last fault (`%s`, `%s`, '
        'the numbers Lines 8 and 13 carried before their 2023 rebuilds mapped through `%s`): %d perch guards, %d strings, %d spans, %d stands. Counting '
        'every summer afternoon fault as a tree also lists the Line 13 pine stand as a span to clear.' % (C.FILES['maint'], C.FILES['veg'],
                                                                                                       C.FILES['structures'], len(guards),
                                                                                                       len(strings), len(spans), len(stands)),
        'Rebuilt the 2026 member impact from the SCADA trips, transfers and recloses and `%s`: %s member interruptions and %s '
        'member-minutes; the outage system\'s dispatcher-closed times overstate the minutes.' % (C.FILES['members'], n(mi['sustained']),
                                                                                                n(mi['member_minutes'])),
        'Carried each washing section\'s deposit from its last wash (`%s`) or soaking rain at its own rate, the rate fitted on the never-'
        'washed test insulators in `%s` against distance from the Gulf; the level is the lowest deposit carried to the day of a '
        'salt-contamination flashover in the fault table, %.3f mg/cm2: %d sections are at or above it. Washing every section that '
        'ever flashed over would wash %d, sections cleaned in October among them.'
        % (C.FILES['washing'], C.FILES['esdd'], f['flashover_level'], len(f['wash_due']), len(care['R7'])),
    ]
    for i, s in enumerate(steps):
        out.append('%d. %s' % (i + 1, s))
    out.append('')
    out.append('No other list survives the files. A relay\'s distance is a calculation that assumes a fault with no resistance and '
               'nothing feeding it from the side; the two ends\' residual currents are not, and the patrols sent to the relays\' '
               'distances after the tree contacts found nothing. The airport reports one point by the Gulf shore, and its codes miss fog '
               'that the cooperative\'s own stations record along the lines and report fog the lines did not have; the survey and the '
               'stations see what was at the structure. A section\'s past flashovers are not its salt today: nothing has '
               'soaked the coast since June and the October washes are clean.')
    open(path, 'w').write('\n'.join(out) + '\n')


if __name__ == '__main__':
    write(os.path.join(C.TASK, 'submission.md'))
