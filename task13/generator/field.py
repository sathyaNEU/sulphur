"""The line crews' insulator washing on the Gulf lines and the test insulators the cooperative samples each month.
Washing: before most fog seasons and after a run of flashovers, a section at a time, some autumns skipped; in 2026 the
crews washed some sections in late winter, some in August after the drought set in and the rest in the October round,
which reached some sections before the southerly blow of 24 to 26 October. The test
insulators hang at eight sites from the Gulf shore to the bay and inland; they are never washed, so each monthly
reading is the deposit since the last soaking rain at that site's distance from the Gulf."""
import datetime as dt
import math

import numpy as np

import common as C
import faults as F
import weather as W

TEST_SITES = [
    # code, description, (x, y)
    ('T1', 'Beachwood pole yard', (69.5, 21.0)),
    ('T2', 'Palmetto Shores', (80.0, 31.5)),
    ('T3', 'Gull Harbor', (85.5, 39.0)),
    ('T4', 'Dune Road', (93.5, 50.0)),
    ('T5', 'Redfish Pass station', (55.0, 6.0)),
    ('T6', 'Sedge Point station', (97.0, 60.0)),
    ('T7', 'Tule Marsh station', (68.0, 31.0)),
    ('T8', 'Live Oak Crossing station', (40.0, 22.0)),
]


def washing_schedule(net, wx, rng=None):
    """dated washes by section; the 2026 plan set so that no section ends October between 0.7 and 1.4 times the
    porcelain's flashover level"""
    rng = rng or np.random.default_rng(C.EV_SEED + 101)
    secs = F.wash_sections(net)
    out = []
    for s in secs:
        for yr in (2021, 2022, 2023, 2024, 2025):
            if s['shore'] > 4.5:
                p = 0.25
            else:
                p = 0.62
            if rng.random() < p:
                d = dt.date(yr, int(rng.choice([9, 10, 11])), int(rng.integers(1, 28)))
                if dt.date(2021, 9, 1) <= d <= dt.date(2026, 10, 31):
                    out.append(dict(section=s['id'], line=s['line'], s0=s['s0'], s1=s['s1'], date=d, why='pre-season'))
            if yr >= 2022 and rng.random() < 0.30:
                d = dt.date(yr, int(rng.choice([3, 4])), int(rng.integers(1, 28)))
                out.append(dict(section=s['id'], line=s['line'], s0=s['s0'], s1=s['s1'], date=d, why='after flashovers'))
    out = [x for x in out if not (x['section'] == 'L02-W4' and x['date'] >= dt.date(2024, 7, 1))]
    s4 = [x for x in secs if x['id'] == 'L02-W4'][0]
    for d, why in L02W4_WASHES:
        out.append(dict(section='L02-W4', line=s4['line'], s0=s4['s0'], s1=s4['s1'], date=dt.date.fromisoformat(d), why=why))
    return secs, out


# the 2026 washes, section by section: the crews' after-flashover washes in winter, the August hot washes once the
# drought set in, and the October pre-season round, which reached some sections before the southerly blow of 24 to 26
# October and the rest after the front; Line 3 section 5 was not reached in 2026
PLAN_2026 = {
    'L01-W1': [('2026-03-12', 'after flashovers')], 'L01-W2': [('2026-10-28', 'pre-season')],
    'L01-W3': [('2026-10-29', 'pre-season')], 'L01-W4': [('2026-10-29', 'pre-season')],
    'L01-W5': [('2026-03-13', 'after flashovers')],
    'L02-W1': [('2026-10-17', 'pre-season')], 'L02-W2': [('2026-08-11', 'hot wash')], 'L02-W3': [('2026-08-12', 'hot wash')],
    'L02-W4': [('2026-01-26', 'after flashovers'), ('2026-02-23', 'after flashovers'), ('2026-03-24', 'after flashovers')],
    'L02-W5': [('2026-08-18', 'hot wash')], 'L02-W6': [('2026-10-20', 'pre-season')], 'L02-W7': [('2026-08-04', 'hot wash')],
    'L03-W1': [('2026-10-27', 'pre-season')], 'L03-W2': [('2026-10-28', 'pre-season')], 'L03-W3': [('2026-10-30', 'pre-season')],
    'L03-W4': [('2026-03-19', 'after flashovers')], 'L03-W5': [], 'L03-W6': [('2026-10-30', 'pre-season')],
    'L03-W7': [('2026-08-20', 'hot wash')],
    'L04-W1': [('2026-03-16', 'after flashovers')], 'L04-W2': [('2026-10-27', 'pre-season')],
    'L04-W3': [('2026-10-28', 'pre-season')],
}
# Line 2 section 4's washes from the autumn of 2024, the crews answering its runs of flashovers
L02W4_WASHES = [('2024-11-12', 'pre-season'), ('2025-11-18', 'pre-season'), ('2025-12-15', 'after flashovers')]


def plan_2026(net, wx, secs, washes, crit, rng=None):
    """the 2026 washes as the crews did them"""
    by = {x['id']: x for x in secs}
    plan = []
    for sid, ws in PLAN_2026.items():
        s = by[sid]
        for d, why in ws:
            plan.append(dict(section=sid, line=s['line'], s0=s['s0'], s1=s['s1'], date=dt.date.fromisoformat(d), why=why))
    return plan


def test_readings(wx, rng=None):
    """monthly test insulator deposits, mg per cm2, on each site's sampling day"""
    rng = rng or np.random.default_rng(C.EV_SEED + 303)
    days = wx['days']
    rows = []
    near = {}
    for code, desc, (x, y) in TEST_SITES:
        sd = W.N._shore_dist(x, y)
        best = min(('APT', 'PAL', 'SHR', 'SED', 'TUL', 'LOK', 'RFP'),
                   key=lambda c: math.hypot(W.PLACES[c][0] - x, W.PLACES[c][1] - y))
        r = W.daily_rain(wx, best)
        rate = F.deposit_rate(sd)
        fac = F.salt_factor(wx, [best])
        dep = rate * 60.0
        series = {}
        for di, d in enumerate(days):
            dep += rate * fac[di]
            dep *= F.rain_keep(r[di])
            series[d] = dep
        near[code] = (sd, series)
        for yr in range(2022, 2027):
            for mo in range(1, 13):
                if yr == 2026 and mo > 10:
                    continue
                day = int(rng.integers(5, 22))
                d = dt.date(yr, mo, day)
                if d not in series:
                    continue
                if rng.random() < 0.04:
                    continue
                val = series[d] * (1.0 + rng.normal(0, 0.07))
                rows.append(dict(site=code, desc=desc, x=x, y=y, date=d, esdd=max(0.001, val)))
    return rows, near
