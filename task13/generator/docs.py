"""The pack's office files in their issuers' genres: the distribution automation device register, the FLISR loop
configuration workbook, the field maintenance books, the capital works register and the large load requests (the
utility's own workbooks, saved in Excel's form by postprocess.normalize_ooxml); the communications and control
system incident log (a service desk export); the commission's order and the distribution automation design basis
(PDFs the issuing office exported from Word, by officepdf); the vendor's FLISR dashboard export; and the
vegetation cycle status workbook."""
import csv
import datetime as dt

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Spacer, Table

import common as C
import postprocess as PP
import sim as S

BODY = ParagraphStyle('body', fontName='Helvetica', fontSize=10, leading=13.4, spaceAfter=6)
HEAD = ParagraphStyle('head', parent=BODY, fontName='Helvetica-Bold', fontSize=10.5, spaceBefore=8, spaceAfter=4)
TITLE = ParagraphStyle('title', parent=BODY, fontName='Helvetica-Bold', fontSize=13, leading=16, spaceAfter=4)
SMALL = ParagraphStyle('small', parent=BODY, fontSize=8.6, leading=11, spaceAfter=3)
CELL = ParagraphStyle('cell', fontName='Helvetica', fontSize=8.8, leading=10.8)


def _rng(k):
    return np.random.default_rng(C.SEED * 17 + k)


def _stamps(key):
    a, b = C.STAMP[key]
    return C.utc_z(a), C.utc_z(b)


def _col(j):
    s = ''
    j += 1
    while j:
        j, r = divmod(j - 1, 26)
        s = chr(65 + r) + s
    return s


def _xlsx(path, sheets, key, title, author, company=C.ORG):
    """sheets: list of (name, header lines, rows (first is the column header), widths, number formats by column)"""
    wb = Workbook()
    wb.remove(wb.active)
    for name, heads, rows, widths, fmts in sheets:
        ws = wb.create_sheet(name)
        r = 1
        for h in heads:
            ws.cell(row=r, column=1, value=h).font = Font(bold=(r == 1), size=11 if r == 1 else 9)
            r += 1
        if heads:
            r += 1
        top = r
        for k, row in enumerate(rows):
            for j, v in enumerate(row):
                c = ws.cell(row=r, column=j + 1, value=v)
                if k == 0:
                    c.font = Font(bold=True)
                    c.fill = PatternFill('solid', fgColor='DDE5EE')
                    c.alignment = Alignment(wrap_text=True, vertical='top')
                else:
                    f = fmts.get(j)
                    if f:
                        c.number_format = f
            r += 1
        for j, wdt in enumerate(widths):
            ws.column_dimensions[_col(j)].width = wdt
        ws.freeze_panes = ws.cell(row=top + 1, column=1)
    wb.save(path)
    cr, md = _stamps(key)
    PP.normalize_ooxml(path, author, author, cr, md, title=title, excel=True, company=company)


PRODUCER = {'design': 'LibreOffice 7.4', 'order': 'LibreOffice 7.6'}    # the release each office ran at its document's date


def _pdf(path, story, key, title, author, subject, footer):
    import officepdf as OP
    a, b = C.STAMP[key]
    OP.build(path, story, title=title, author=author, subject=subject, footer=footer,
             created=C.local(a), modified=C.local(b), font='Liberation Sans', body_pt=9.6, producer=PRODUCER.get(key),
             page_mm=C.LETTER_MM)


# ------------------------------------------------------------------------------------------------ the register

def write_register(w, path):
    NET = w['NET']
    devs = NET['devices']
    BAT = w['BAT']
    asof = dt.date(2026, 10, 22)
    rows = [['Asset No', 'Device', 'Loop', 'Feeder', 'Position', 'Control', 'ADMS tag', 'ADMS tag before 18 Mar 2025',
             'Radio site', 'In service', 'Battery installed', 'Phase pickup group 1 (A)', 'Phase pickup group 2 (A)',
             'Settings applied']]
    for a in sorted(devs, key=lambda x: (devs[x]['loop'], devs[x]['feeder'], devs[x]['kind'])):
        D = devs[a]
        pos = {'R1': 'Midline recloser 1', 'R2': 'Midline recloser 2', 'TS': 'Tie switch (normally open)'}[D['kind']]
        dev = 'Recloser' if D['kind'] != 'TS' else 'Motor-operated switch'
        batt = BAT.current(a, asof)[0] if a in BAT.b else None
        rows.append([a, dev, D['loop'], D['feeder'], pos, D['ctl'], D['tag_new'], D['tag_old'], D['site'],
                     D['installed'], batt, D.get('pickup1'), D.get('pickup2'),
                     dt.date(max(2019, D.get('set_year', 2019)), 5, 1) if D['kind'] != 'TS' else None])
    cb = [['Breaker', 'Substation', 'Feeder', 'Phase pickup (A)']]
    for f in NET['loop_feeders']:
        F = NET['feeders'][f]
        sub = dict(C.SUBSTATIONS)[F['sub']]
        cb.append([f + ' CB', sub, f, F['cb_pickup']])
    models = [['Control', 'Battery', 'In use from'],
              ['CTL-4C', '24 V VRLA (2 x 12 V, 12 Ah)', 2018],
              ['CTL-6', '24 V VRLA (2 x 12 V, 17 Ah)', 2020]]
    _xlsx(path, [('Devices', [C.ORG_SHORT + ' distribution automation device register', 'Extract 22 Oct 2026'],
                  rows, [11, 20, 6, 9, 22, 8, 15, 22, 21, 11, 13, 12, 12, 12], {9: 'yyyy-mm-dd', 10: 'yyyy-mm-dd',
                                                                                  13: 'yyyy-mm-dd'}),
                 ('Breakers', [], cb, [13, 14, 9, 14], {}),
                 ('Controls', [], models, [9, 28, 11], {})],
          'register', 'Distribution automation device register', C.PEOPLE['da_engineer'])


# ---------------------------------------------------------------------------------------- the loop configuration

def write_loops(w, path):
    NET = w['NET']
    feeders = NET['feeders']
    loops = [['Loop', 'ADMS scheme', 'Feeder A', 'Feeder B', 'Tie switch', 'FLISR in service']]
    for Lp in NET['loops']:
        loops.append([Lp['loop'], Lp['scheme'], Lp['a'], Lp['b'], S.tie_of(NET, Lp['loop']), Lp['commissioned']])
    import net as N
    recon = {r['feeder']: r for r in NET['recon']}
    secs = [['Feeder', 'Section', 'From', 'To', 'Main line (km)', 'Customers (Sep 2026)']]
    for f in NET['loop_feeders']:
        F = feeders[f]
        for k in (1, 2, 3):
            frm = f + ' CB' if k == 1 else S.dev_of(NET, f, 'R%d' % (k - 1))
            to = S.dev_of(NET, f, 'R%d' % k) if k < 3 else S.tie_of(NET, F['loop'])
            km = F['sections'][k - 1]['km']
            r = recon.get(f)
            if r is not None:
                km = km + r['km_moved'] if k == 2 else (km - r['km_moved'] if k == 3 else km)
            secs.append([f, k, frm, to, round(km, 2), int(round(N.section_customers(F, k, 2026.7, recon)))])
    fd = [['Feeder', 'Substation', 'Breaker', 'Emergency limit (A)', 'Customers (Sep 2026)']]
    for f in NET['loop_feeders']:
        F = feeders[f]
        tot = sum(int(round(N.section_customers(F, k, 2026.7, recon))) for k in (1, 2, 3))
        fd.append([f, dict(C.SUBSTATIONS)[F['sub']], f + ' CB', F['emerg_amps'], tot])
    ch = [['Date', 'Loop', 'Feeder', 'Change']]
    for r in NET['recon']:
        F = feeders[r['feeder']]
        ch.append([r['date'], F['loop'], r['feeder'], 'Midline recloser 2 (%s) relocated %.2f km toward the tie; '
                   'about %d customers moved from section 3 to section 2' % (S.dev_of(NET, r['feeder'], 'R2'),
                                                                            r['km_moved'], r['moved'])])
    for Lp in NET['loops']:
        ch.append([Lp['commissioned'], Lp['loop'], Lp['a'] + ' / ' + Lp['b'], 'FLISR scheme placed in service'])
    for lid, (a0, a1) in NET.get('supervised', {}).items():
        Lp = [x for x in NET['loops'] if x['loop'] == lid][0]
        ch.append([C.to_local(a0).date(), lid, Lp['a'] + ' / ' + Lp['b'],
                   'Scheme set to supervised mode (transfers need operator confirmation) pending protection review'])
        if a1.year < 2027:
            ch.append([C.to_local(a1).date(), lid, Lp['a'] + ' / ' + Lp['b'], 'Scheme returned to automatic mode'])
    ch[1:] = sorted(ch[1:], key=lambda x: x[0])
    _xlsx(path, [('Loops', [C.ORG_SHORT + ' FLISR loop configuration', 'Revised 30 Sep 2026'], loops,
                  [6, 24, 9, 9, 11, 14], {5: 'yyyy-mm-dd'}),
                 ('Sections', [], secs, [9, 8, 13, 13, 13, 18], {4: '0.00'}),
                 ('Feeders', [], fd, [9, 14, 12, 17, 18], {}),
                 ('Changes', [], ch, [11, 6, 15, 90], {0: 'yyyy-mm-dd'})],
          'loops', 'FLISR loop configuration', C.PEOPLE['da_engineer'])


# ------------------------------------------------------------------------------------------- maintenance books

CREWS = ['Line crew 2 (Mankato)', 'Line crew 4 (St. Peter)', 'Line crew 5 (Waseca)', 'Relay tech (R. Lund)',
         'Relay tech (T. Okafor)']


def write_maint(w, path):
    rng = _rng(3)
    NET = w['NET']
    devs = NET['devices']
    BAT = w['BAT']
    W = w['W']
    ft = [['Date', 'Asset No', 'Crew', 'Open/close (local)', 'Open/close (remote)', 'Fault indicator', 'Comms',
           'Battery (V)', 'Result', 'Notes']]
    for a in sorted(devs):
        D = devs[a]
        for y in range(2019, 2027):
            if dt.date(y, 12, 31) < D['installed']:
                continue
            spring = rng.random() < 0.55
            d = dt.date(y, 4 if spring else 9, 1) + dt.timedelta(days=int(rng.integers(0, 58)))
            if d < D['installed'] or d > dt.date(2026, 10, 30):
                continue
            comms_ok = rng.random() > 2.5 * D['q']
            res = 'PASS' if comms_ok else 'PASS (comms retried)'
            note = ''
            if rng.random() < 0.012:
                res = 'FAIL'
                note = rng.choice(['Close coil slow; mechanism lubricated, retested OK',
                                   'FPI target did not reset; reset and retested OK', 'Door seal replaced'])
            bv = '' if D['kind'] == 'TS' else '%.1f' % (25.5 + rng.normal(0, 0.12))
            ft.append([d, a, CREWS[int(rng.integers(0, len(CREWS)))], 'OK', 'OK' if comms_ok else 'OK (2nd try)',
                       'OK', 'OK' if comms_ok else 'Weak signal', bv, res, note])
    ft[1:] = sorted(ft[1:], key=lambda x: (x[0], x[1]))
    br = [['Date', 'Asset No', 'Reason', 'Battery removed (installed)', 'Work order']]
    wo = 640012
    for a in sorted(BAT.b):
        recs = BAT.b[a]
        for i in range(1, len(recs)):
            d = recs[i][0]
            if d < dt.date(2019, 1, 1) or d > dt.date(2026, 10, 30):
                continue
            wo += int(rng.integers(3, 41))
            reason = {'scheduled': 'Four-year replacement', 'failed to operate': 'Failed to operate (see outage)',
                      'battery test alarm': 'Battery test alarm'}[recs[i][4]]
            br.append([d, a, reason, recs[i - 1][0], 'WO-%d' % wo])
    br[1:] = sorted(br[1:], key=lambda x: (x[0], x[1]))
    rep = [['Date', 'Asset No', 'Finding', 'Action']]
    for e in w['events']:
        if e['ev'] == 'BATTERY LOW ALARM' and C.REC0 <= e['t'] < C.T_END:
            d = (e['t'] + dt.timedelta(days=float(rng.uniform(1, 6)))).date()
            rep.append([d, e['dev'], 'Control found off line after outage; battery low',
                        'Control restarted on line power; battery replacement raised'])
    rep[1:] = sorted(rep[1:], key=lambda x: (x[0], x[1]))
    _xlsx(path, [('Functional tests', [C.ORG_SHORT + ' distribution automation maintenance', 'Field returns'], ft,
                  [11, 11, 22, 16, 18, 14, 12, 11, 20, 46], {0: 'yyyy-mm-dd'}),
                 ('Battery replacements', [], br, [11, 11, 30, 24, 12], {0: 'yyyy-mm-dd', 3: 'yyyy-mm-dd'}),
                 ('Repairs', [], rep, [11, 11, 46, 52], {0: 'yyyy-mm-dd'})],
          'maint', 'Distribution automation maintenance records', C.PEOPLE['ops'])


# ---------------------------------------------------------------------------- capital works and the 2027 plan

CATS = {'Reconductor': (4.6, 0.85, 0.16), 'Recloser control replacement': (3.4, 0.8, 0.2),
        'FLISR loop commissioning': (5.0, 0.7, 0.1), 'Substation transformer': (6.2, 0.6, 0.08),
        'Capacitor bank': (1.4, 0.7, 0.42), 'Pole replacement program': (1.8, 0.8, 0.35),
        'Underground conversion': (5.4, 0.7, 0.12), 'Voltage regulator': (2.0, 0.7, 0.3)}


def choose_plan(w, target, f):
    """the large load first (a customer's request on an end section of an unswitched receiving feeder whose
    transfers it would push over), then the four reinforcements on the receiving feeders whose summer transfers
    the replay shows doing the most harm"""
    import warnings
    warnings.filterwarnings('ignore')
    import golden as G
    import analysis as A
    NET = w['NET']
    write_capital(w, f('capital'), {'reinforce': [], 'newload': None})
    write_loads(w, f('loads'), {'reinforce': [], 'newload': None})
    P = A.Pack(target)
    ops = G.operations(P)
    base = G.forward(P, ops, newload=False)
    D = G.directions(P)
    rate, mshare, lo = G.lockout_rates(P, ops)
    l, dur = G.fault_hours(P, lo)
    best = None
    for _, d in D[~D['switched']].iterrows():
        h0 = float(base[(base['from'] == d['from']) & (base['to'] == d['to'])]['harm'].iloc[0])
        p0 = G.trip_prob(P, d, 'S2', l, dur, months=(7,))
        p1 = G.trip_prob(P, d, 'S2', l, dur, extra_amps=G.mw_to_amps(2.2), months=(7,))
        gain = p1 - p0
        if h0 < base['harm'].median() and (best is None or gain > best[0]):
            best = (gain, d['loop'], d['from'], d['to'])
    newload = (best[1], best[2], best[3])
    ranked = base.sort_values('harm', ascending=False)
    reinf = []
    for _, r in ranked.iterrows():
        if r['to'] == newload[2] or r['to'] in [x[2] for x in reinf]:
            continue
        reinf.append((r['loop'], r['from'], r['to']))
        if len(reinf) == 4:
            break
    return {'reinforce': reinf, 'newload': newload}


def capital_rows(w, P):
    rng = _rng(4)
    NET = w['NET']
    rows = []
    pid = 19021
    fids = NET['fids']
    for Lp in NET['loops']:
        # the loops' own commissioning, planned against actual
        act = Lp['commissioned']
        mu, sg, ontime = CATS['FLISR loop commissioning']
        slip = 0.0 if rng.random() < ontime else float(rng.lognormal(np.log(mu), sg))
        planned = act - dt.timedelta(days=int(slip * 30.44))
        pid += int(rng.integers(2, 9))
        rows.append(['DP-%d' % pid, 'FLISR loop %s (%s / %s)' % (Lp['loop'], Lp['a'], Lp['b']),
                     'FLISR loop commissioning', Lp['a'], planned, act, 'Complete', round(float(rng.uniform(0.38, 0.62)), 2)])
    for cat, (mu, sg, ontime) in CATS.items():
        if cat == 'FLISR loop commissioning':
            continue
        n = {'Reconductor': 26, 'Recloser control replacement': 14, 'Substation transformer': 9, 'Capacitor bank': 12,
             'Pole replacement program': 15, 'Underground conversion': 8, 'Voltage regulator': 10}[cat]
        for i in range(n):
            planned = dt.date(2019, 3, 1) + dt.timedelta(days=int(rng.integers(0, 2700)))
            slip = float(rng.uniform(-0.6, 0.5)) if rng.random() < ontime else float(rng.lognormal(np.log(mu), sg))
            actual = planned + dt.timedelta(days=int(slip * 30.44))
            f = fids[int(rng.integers(0, len(fids)))]
            title = {'Reconductor': 'Reconductor %s main line (%.1f mi) to 336 ACSR' % (f, rng.uniform(0.8, 4.5)),
                     'Recloser control replacement': 'Replace recloser controls on %s' % f,
                     'Substation transformer': 'Replace %s transformer T%d' % (dict(C.SUBSTATIONS)[f[:3]], rng.integers(1, 3)),
                     'Capacitor bank': 'Install switched capacitor bank on %s' % f,
                     'Pole replacement program': 'Pole replacements, %s (%d poles)' % (f, rng.integers(18, 140)),
                     'Underground conversion': 'Convert %s tap to underground' % f,
                     'Voltage regulator': 'Install line regulator on %s' % f}[cat]
            pid += int(rng.integers(2, 9))
            if actual > dt.date(2026, 10, 15):
                status, act = 'In construction', None
            else:
                status, act = 'Complete', actual
            rows.append(['DP-%d' % pid, title, cat, f, planned, act, status, round(float(rng.lognormal(np.log(0.6), 0.6)), 2)])
    # the 2027 plan
    plan_dates = [dt.date(2027, 5, 3), dt.date(2027, 5, 17), dt.date(2027, 6, 1), dt.date(2027, 6, 14)]
    for (lid, a, b), pd in zip(P['reinforce'], plan_dates):
        pid += int(rng.integers(2, 9))
        rows.append(['DP-%d' % pid, 'Reconductor %s sections 2 and 3, replace recloser controls (%s, %s)' %
                     (b, S.dev_of(NET, b, 'R1'), S.dev_of(NET, b, 'R2')), 'Reconductor', b, pd, None, 'Approved 2027',
                     round(float(rng.uniform(1.1, 2.4)), 2)])
    for i in range(7):
        pid += int(rng.integers(2, 9))
        f = fids[int(rng.integers(0, len(fids)))]
        cat = ['Capacitor bank', 'Pole replacement program', 'Voltage regulator', 'Underground conversion',
               'Substation transformer', 'Pole replacement program', 'Capacitor bank'][i]
        rows.append(['DP-%d' % pid, '%s, %s' % (cat, f), cat, f, dt.date(2027, 3, 1) + dt.timedelta(days=int(rng.integers(0, 240))),
                     None, 'Approved 2027', round(float(rng.lognormal(np.log(0.5), 0.5)), 2)])
    rows.sort(key=lambda r: (r[4], r[0]))
    return rows, P


def write_capital(w, path, P):
    rows, P = capital_rows(w, P)
    hdr = ['Project', 'Title', 'Category', 'Feeder', 'Planned in service', 'Actual in service', 'Status', 'Budget (USD m)']
    _xlsx(path, [('Projects', [C.ORG_SHORT + ' distribution capital works register', 'Capital Projects Office'],
                  [hdr] + rows, [10, 74, 26, 9, 16, 16, 15, 14], {4: 'yyyy-mm-dd', 5: 'yyyy-mm-dd', 7: '0.00'})],
          'capital', 'Distribution capital works register', C.PEOPLE['capital'])
    return P


def write_loads(w, path, P):
    rng = _rng(5)
    NET = w['NET']
    lid, a, b = P['newload'] if P.get('newload') else (None, None, None)
    rows = [['Request', 'Customer', 'Feeder', 'Location', 'Load (MW)', 'Requested in service', 'Status']]
    pick = []
    others = [f for f in NET['fids'] if f not in (b,)]
    names = ['Cold storage expansion', 'Grain dryer addition', 'Ethanol plant process load', 'Hospital addition',
             'School district EV bus depot', 'Data processing building', 'Feed mill', 'Apartment complex',
             'Car dealership EV chargers', 'Fire station']
    for i in range(9):
        f = others[int(rng.integers(0, len(others)))]
        pick.append(['LL-26-%03d' % (i * 3 + 11), names[(i + 3) % len(names)], f,
                     'Section %d' % int(rng.integers(1, 4)) if f in NET['loop_feeders'] else 'Main line',
                     round(float(rng.uniform(0.3, 1.6)), 2), dt.date(2026, 3, 1) + dt.timedelta(days=int(rng.integers(0, 600))),
                     rng.choice(['Approved', 'In review', 'Energized', 'Withdrawn'])])
    if b is not None:
        pick.append(['LL-26-007', 'Cold storage expansion (North Star Foods)', b, 'Section 3 (near %s)' % S.tie_of(NET, lid),
                     2.2, dt.date(2027, 4, 19), 'Approved, under construction'])
    pick.sort(key=lambda r: r[0])
    _xlsx(path, [('Requests', [C.ORG_SHORT + ' large load requests', 'Customer Engineering, as of 27 Oct 2026'],
                  rows + pick, [11, 38, 9, 22, 10, 20, 26], {4: '0.00', 5: 'yyyy-mm-dd'})],
          'loads', 'Large load requests', C.PEOPLE['capital'])


# ------------------------------------------------------------------------------------------------ incident log

def write_incidents(w, path):
    rng = _rng(6)
    rows = []
    no = 21844
    for s, e in w['windows']:
        t0 = C.T0 + dt.timedelta(hours=s)
        t1 = C.T0 + dt.timedelta(hours=e)
        if t0 < C.REC0 or t0 >= C.T_END:
            continue
        a = t0 - dt.timedelta(minutes=float(rng.uniform(1, 9)))
        b = t1 + dt.timedelta(minutes=float(rng.uniform(2, 25)))
        rows.append([a, b, 'ADMS', 'Control center',
                     rng.choice(['Event archive service: inbound queue overflow during storm activity; queued events '
                                 'discarded until the queue drained',
                                 'Event archive writer backlog, queue limit reached; events dropped',
                                 'Archive service queue full during storm; events discarded'])])
    sky0, sky1 = w['sky']
    rows.append([C.T0 + dt.timedelta(hours=sky0), C.T0 + dt.timedelta(hours=sky1), 'Radio', 'Skyline Tower',
                 'Base site damaged by lightning; temporary panel antenna installed, coverage degraded for the '
                 'site\'s remotes; permanent antenna and feed line replaced 12 Sep'])
    for _ in range(26):
        d = C.REC0 + dt.timedelta(hours=float(rng.uniform(0, 42000)))
        site = C.RADIO_SITES[int(rng.integers(0, 5))]
        dur = float(rng.lognormal(np.log(2.5), 0.9))
        rows.append([d, d + dt.timedelta(hours=dur), 'Radio', site,
                     rng.choice(['Base site on battery after utility power loss', 'Backhaul link down',
                                 'Radio base station reboot', 'Site generator test, brief loss of service'])])
    rows.append([dt.datetime(2025, 3, 18, 14, 0, tzinfo=dt.timezone.utc), dt.datetime(2025, 3, 18, 21, 30, tzinfo=dt.timezone.utc),
                 'ADMS', 'Control center', 'ADMS upgraded from 7.4 to 8.1; FLISR schemes re-armed after upgrade; device '
                 'tags renamed to the 2025 naming standard'])
    for _ in range(9):
        d = C.REC0 + dt.timedelta(hours=float(rng.uniform(0, 42000)))
        rows.append([d, d + dt.timedelta(minutes=float(rng.uniform(4, 40))), 'ADMS', 'Control center',
                     rng.choice(['Server failover ADMS-A to ADMS-B', 'Server failover ADMS-B to ADMS-A',
                                 'Planned patching, standby server active'])])
    for _ in range(7):
        d = C.REC0 + dt.timedelta(hours=float(rng.uniform(0, 42000)))
        rows.append([d, d + dt.timedelta(hours=float(rng.uniform(1, 6))), 'SCADA historian', 'Control center',
                     'Historian collector restart; hourly values interpolated'])
    other = [('OMS', 'Control center', ['OMS client slow to load outage map', 'OMS to IVR interface down; call-ins '
                                         'keyed by dispatchers', 'OMS crew assignment screen error after patch']),
             ('AMI', 'Head-end', ['AMI head-end message backlog; meter reads delayed', 'Collector offline after '
                                  'utility power loss', 'Head-end certificate renewal']),
             ('Radio', None, ['Remote not answering polls; field check found loose antenna connector',
                              'Interference reported on channel 3; frequency coordinator notified',
                              'Base site tower light alarm', 'Backhaul microwave fade during heavy rain']),
             ('ADMS', 'Control center', ['Operator console freeze; restarted', 'Display build error on one-line '
                                         'diagram after model update', 'Load flow did not converge for one feeder; '
                                         'model corrected']),
             ('Network', 'Data center', ['Firewall rule change for historian replication', 'Switch port flapping in '
                                         'control center LAN', 'Planned network maintenance window']),
             ('SCADA', None, ['RTU communication failure at substation; technician dispatched',
                              'Analog point stuck at last value; scaling corrected', 'Substation RTU firmware update'])]
    for _ in range(190):
        sysn, loc, texts = other[int(rng.integers(0, len(other)))]
        d = C.REC0 + dt.timedelta(hours=float(rng.uniform(0, 42000)))
        place = loc or (C.RADIO_SITES[int(rng.integers(0, 5))] if sysn == 'Radio' else
                        dict(C.SUBSTATIONS)[C.SUBSTATIONS[int(rng.integers(0, 9))][0]] + ' substation')
        rows.append([d, d + dt.timedelta(hours=float(rng.lognormal(np.log(3.0), 1.0))), sysn, place,
                     texts[int(rng.integers(0, len(texts)))]])
    rows.sort(key=lambda r: r[0])
    with open(path, 'w', newline='') as fh:
        wr = csv.writer(fh)
        wr.writerow(['Incident', 'Opened', 'Closed', 'System', 'Location', 'Summary'])
        for a, b, sysn, loc, summ in rows:
            no += int(rng.integers(1, 30))
            wr.writerow(['INC%07d' % no, C.to_local(a).strftime('%Y-%m-%d %H:%M'), C.to_local(b).strftime('%Y-%m-%d %H:%M'),
                         sysn, loc, summ])


# ---------------------------------------------------------------------------------------------- the dashboard

def write_dashboard(w, path, adms_path):
    """the vendor's monthly FLISR KPI report, computed from the ADMS event archive"""
    import pandas as pd
    df = pd.read_csv(adms_path)
    df['t'] = pd.to_datetime(df['event_time_utc'], utc=True).dt.tz_convert(C.ZONE)
    df = df.sort_values(['scheme', 'message', 't'])
    echo = (df['scheme'] == df['scheme'].shift()) & (df['message'] == df['message'].shift()) & \
        ((df['t'] - df['t'].shift()).dt.total_seconds() < 1.0)
    prim = df[~echo].sort_values('t').copy()
    prim['m'] = prim['t'].dt.strftime('%Y-%m')
    rows = [['Month', 'Sequences started', 'Restorations complete', 'Aborted', 'Blocked', 'Not started (disarmed)',
             'No restoration available', 'Customers restored', 'CI saved', 'CMI saved']]
    import re
    for m, g in prim.groupby('m'):
        u = g['message'].str.upper()
        started = int((u.str.startswith('FLISR START') | u.str.startswith('FLISR SEQUENCE STARTED')).sum())
        comp = g[u.str.startswith('RESTORATION COMPLETE')]
        n = 0
        for x in comp['message']:
            n += int(re.findall(r'(\d+)', x)[-1])
        ab = int((u.str.contains('ABORT')).sum())
        bl = int((u.str.startswith('RESTORATION BLOCKED')).sum())
        ns = int((u.str.startswith('FLISR NOT STARTED')).sum())
        nr = int((u.str.startswith('NO RESTORATION AVAILABLE')).sum())
        rows.append([m, started, len(comp), ab, bl, ns, nr, n, n, n * 60])
    _xlsx(path, [('Monthly KPI', ['FLISR performance dashboard: monthly KPI export (report v2.3)',
                                  'Source: ADMS FLISR event archive. CI saved = customers restored by completed '
                                  'sequences. CMI saved assumes 60 minutes per restored customer.',
                                  'Refreshed 2026-11-01 06:00 CT. Maintained by %s for %s Grid Modernization.' %
                                  (C.VENDOR, C.ORG_SHORT)],
                  rows, [9, 11, 12, 9, 9, 13, 13, 12, 10, 12], {})],
          'dashboard', 'FLISR KPI dashboard export', 'ADMS Reporting')


# -------------------------------------------------------------------------------------------- the distractor

def write_veg(w, path):
    rng = _rng(8)
    NET = w['NET']
    rows = [['Feeder', 'Substation', 'Overhead miles', 'Last trimmed', 'Cycle (years)', 'Next scheduled', 'Hazard trees removed 2025',
             'Notes']]
    for f in NET['fids']:
        F = NET['feeders'][f]
        last = int(rng.integers(2021, 2026))
        cyc = int(rng.choice([4, 4, 5]))
        rows.append([f, dict(C.SUBSTATIONS)[F['sub']], round(F['ml_km'] / 1.609 * rng.uniform(1.3, 2.1), 1), last, cyc,
                     last + cyc, int(rng.integers(0, 60)), rng.choice(['', '', 'Ash removal ongoing', 'Contractor change 2025',
                                                                      'ROW access issues'])])
    _xlsx(path, [('Cycle status', [C.ORG_SHORT + ' vegetation management, cycle status', 'Forestry, Sep 2026'], rows,
                  [9, 14, 14, 12, 12, 14, 22, 26], {})],
          'veg', 'Vegetation cycle status', 'Forestry')


# ------------------------------------------------------------------------------------------------ the documents

def write_order(path):
    P = lambda t, st=BODY: Paragraph(t, st)
    story = [
        P('STATE OF MINNESOTA<br/>PUBLIC UTILITIES COMMISSION', TITLE),
        P('In the Matter of Grid Modernization Performance Metrics for Electric Distribution Utilities', HEAD),
        P('Docket No. E-999/CI-23-412', BODY),
        P('ORDER ESTABLISHING REPORTING METRICS FOR AUTOMATIC RESTORATION (EXCERPT)', HEAD),
        P('Issue date: June 20, 2024', BODY),
        Spacer(1, 6),
        P('ORDER', HEAD),
        P('1. Utilities operating automatic fault location, isolation and service restoration (automatic '
          'restoration) on their distribution systems shall report the metrics in paragraphs 2 to 5 each year by '
          'April 1 for the preceding calendar year, beginning with calendar year 2022.'),
        P('2. Customer interruptions avoided. For a calendar year, the number of sustained customer interruptions the '
          'utility\'s customers would have had without automatic restoration, less the number of sustained customer '
          'interruptions they had. All days of the year are included, major event days among them.'),
        P('3. A sustained interruption lasts five minutes or longer, measured from the first loss of supply. An '
          'interruption shorter than five minutes is momentary and is not counted in paragraph 2.'),
        P('4. Without automatic restoration, customers are restored by the utility\'s usual switching: remote '
          'switching from the control room where the devices respond, and otherwise field switching. The faults, '
          'the repairs and every other operation on the system are as they were.'),
        P('5. Forecast. The utility shall also report the customer interruptions avoided it expects in the next '
          'calendar year if its schemes are operated as they stand, in a year whose faults occur at the average '
          'annual rate of its records since January 1, 2022, with an 80 percent range.'),
        P('6. The utility shall describe any scheme it has taken out of service or changed in the reporting year '
          'and the reason.'),
        P('7. Advanced metering. The utility shall report the share of meters read on schedule each month, the '
          'number of remote disconnections and reconnections, and the share of outage notifications received from '
          'meters within one minute of the outage.'),
        P('8. Hosting capacity. The utility shall publish feeder-level hosting capacity for distributed energy '
          'resources at least annually and report the number of interconnection applications that required a '
          'supplemental review.'),
        P('9. Volt-var optimization. For each substation with volt-var optimization in service the utility shall '
          'report the measured conservation voltage reduction factor and the energy saved, with the method used.'),
        P('10. Costs. The utility shall report capital and operating costs of each grid modernization program '
          'against the amounts approved in its most recent rate case.'),
        P('11. The utility shall file the data underlying paragraphs 2 to 5 with its report in a form that allows '
          'the Department of Commerce to reproduce each figure.'),
        P('12. This order shall become effective immediately.'),
        Spacer(1, 8),
        P('BY ORDER OF THE COMMISSION', HEAD),
        P('Executive Secretary', BODY),
        Spacer(1, 4),
        P('This document can be made available in alternative formats by calling 651-296-0406 or 1-800-657-3782.',
          SMALL),
    ]
    _pdf(path, story, 'order', 'Order Establishing Reporting Metrics for Automatic Restoration',
         'Minnesota Public Utilities Commission', 'Docket E-999/CI-23-412', 'Docket No. E-999/CI-23-412')


def write_design(path):
    P = lambda t, st=BODY: Paragraph(t, st)
    rows = [[Paragraph(x, CELL) for x in r] for r in [
        ['Item', 'Basis'],
        ['Ambient range', '-27 C (-17 F) to +40 C. -27 C is the one-in-ten-year design minimum at Mankato '
                          'Regional Airport.'],
        ['Seasons', 'Summer, 1 June to 30 September. Winter, 1 December to the end of February.'],
        ['Control power', 'Line-powered through a voltage transformer; 24 V valve-regulated lead-acid battery carries '
                          'the control, its radio and the recloser\'s trip and close operations when the line is '
                          'de-energized.'],
        ['Battery load test', 'Automatic, weekly, at 5 A. The control reports the voltage at rest and under the test '
                              'load, and alarms when the voltage under load is below 24.4 V.'],
        ['Operation on battery', 'A trip or close operation draws 30 A from the battery for up to 60 ms. The control '
                                 'does not complete an operation if the battery voltage falls below 21.2 V under '
                                 'that draw.'],
        ['Battery replacement', 'Four-year cycle, and after a load test alarm.'],
        ['Functional test', 'Annual, line energized: local and remote open and close, fault indicator response, '
                            'communications check, battery voltage.'],
        ['Communications', 'Licensed UHF data radio to the ADMS front end through five base sites; DNP3, '
                           'integrity poll every 10 minutes, event reporting by exception.'],
        ['System voltage', '13.8 kV grounded wye, 95 kV BIL; main lines 336.4 kcmil ACSR, taps 1/0 ACSR.'],
        ['Reclosers', 'Three-phase vacuum, 630 A continuous, 12.5 kA interrupting; two fast and two delayed '
                      'operations to lockout.'],
        ['Tie switches', 'Motor-operated load-break, 900 A, powered from voltage transformers on both sides.'],
        ['Fault indication', 'Built into the recloser controls; phase threshold 400 A, ground 140 A.'],
        ['Coordination', 'Midline reclosers coordinate with the substation breaker and with downstream fuses by '
                         'time-current curve margins of at least 0.3 s.'],
        ['Enclosures', 'Pole-mounted control cabinets, NEMA 4X, padlocked; door switch alarmed to SCADA.'],
        ['Grounding', 'Each automated device grounded to 25 ohms or less, tested at installation.'],
    ]]
    t = Table(rows, colWidths=[110, 360])
    story = [
        P(C.ORG + '<br/>Distribution Engineering', TITLE),
        P('Distribution Automation Design Basis, Revision 3', HEAD),
        P('March 2023. Supersedes Revision 2 (June 2020).', BODY),
        P('1. Scope', HEAD),
        P('Midline reclosers, tie switches and their controls on the automated loops, and the ADMS fault location, '
          'isolation and service restoration (FLISR) schemes that operate them.'),
        P('2. Design basis', HEAD),
        t,
        P('3. Schemes', HEAD),
        P('Each loop pairs two feeders through a normally open tie switch. Each feeder is divided into three '
          'sections by two midline reclosers. A scheme is armed while every device in its loop answers and the loop '
          'is in its normal configuration.'),
        P('4. Testing and records', HEAD),
        P('Device test results are entered in the maintenance records within five working days. Battery '
          'replacements are recorded with the battery removed. Settings changes are issued by System Protection '
          'and recorded in the device register with their date.'),
        P('5. Revision history', HEAD),
        P('Rev 1 (2019): first loops. Rev 2 (June 2020): CTL-6 controls added to the approved list. Rev 3 (March '
          '2023): radio site list, enclosure and grounding requirements updated.'),
        P('Approved: E. Stewart, System Protection; N. Reeves, Distribution Automation', SMALL),
    ]
    _pdf(path, story, 'design', 'Distribution Automation Design Basis Rev 3', 'Distribution Engineering',
         'Distribution automation design basis', C.ORG_SHORT + ' Distribution Engineering, DA design basis Rev 3')
