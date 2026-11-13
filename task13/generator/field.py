"""The line crews' insulator washing on the Gulf lines and the test insulators the cooperative samples each month.
Washing: before most fog seasons and after a run of flashovers, a section at a time, some autumns skipped; in 2026 the
crews washed some sections in late winter, some in August after the drought set in and some in October. The test
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
    return secs, out


def plan_2026(net, wx, secs, washes, crit, rng=None):
    """the 2026 washes: March for some, August for some near the shore, October for some, none for the rest, chosen so
    each section's deposit on 31 October sits clear of the flashover level"""
    rng = rng or np.random.default_rng(C.EV_SEED + 202)
    days = wx['days']
    rain = {c: W.daily_rain(wx, c) for c in ('APT', 'PAL', 'SHR', 'SED')}
    codes = {'L01': ('PAL', 'APT'), 'L02': ('PAL', 'SHR'), 'L03': ('SHR', 'SED'), 'L04': ('APT', 'PAL')}
    end = days.index(dt.date(2026, 10, 31))
    plan = []
    for s in secs:
        r = (rain[codes[s['line']][0]] + rain[codes[s['line']][1]]) / 2.0
        rate = F.deposit_rate(s['shore'])

        def oct31(wash_day):
            dep = rate * 60.0
            for di in range(days.index(dt.date(2026, 1, 1)), end + 1):
                d = days[di]
                dep += rate * F.onshore_factor(d.month)
                dep *= F.rain_keep(r[di])
                if wash_day is not None and d == wash_day:
                    dep = 0.003
            return dep

        choice = None
        none = oct31(None)
        aug = dt.date(2026, 8, int(rng.integers(3, 21)))
        octo = dt.date(2026, 10, int(rng.integers(19, 29)))
        mar = dt.date(2026, 3, int(rng.integers(2, 27)))
        dep_aug = oct31(aug)
        u = rng.random()
        if none <= 0.5 * crit:
            choice = mar if u < 0.5 else None                     # far from the shore: whatever was done, below
        elif dep_aug >= 1.8 * crit and u < 0.45:
            choice = aug                                          # near the shore, washed in August, back over
        elif none >= 1.8 * crit and u < 0.75:
            choice = None if u < 0.5 else mar                     # not washed since the drought began: over
        else:
            choice = octo                                         # washed in October: clean
        if choice is not None:
            plan.append(dict(section=s['id'], line=s['line'], s0=s['s0'], s1=s['s1'], date=choice,
                             why={3: 'after flashovers', 8: 'hot wash', 10: 'pre-season'}[choice.month]))
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
        dep = rate * 60.0
        series = {}
        for di, d in enumerate(days):
            dep += rate * F.onshore_factor(d.month)
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
