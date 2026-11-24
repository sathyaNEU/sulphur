"""The line crews' insulator washing on the Gulf lines and the eight test insulator sites sampled each month for both
ESDD (soluble sea salt) and NSDD (non-soluble caliche/agricultural dust). Never-washed test strings span coastal
marsh, pasture and caliche/cropland corridors from the Gulf shore inland, so both state processes (salt on onshore
winds with fast rain washout; insoluble dust on dry inland winds with slow rain washout) are directly measurable."""
import datetime as dt
import math

import numpy as np

import common as C
import faults as F
import network as N
import weather as W

# Eight test sites spanning shore distance AND corridor surface (coastal marsh, pasture, caliche / cropland)
TEST_SITES = [
    # code, description, (x, y), corridor surface
    ('T1', 'Beachwood pole yard', (69.5, 21.0), 'coastal marsh'),
    ('T2', 'Palmetto Shores', (80.0, 31.5), 'pasture'),
    ('T3', 'Gull Harbor', (85.5, 39.0), 'caliche / cropland'),
    ('T4', 'Dune Road', (93.5, 50.0), 'coastal marsh'),
    ('T5', 'Redfish Pass station', (55.0, 6.0), 'coastal marsh'),
    ('T6', 'Sedge Point station', (97.0, 60.0), 'caliche / cropland'),
    ('T7', 'Tule Marsh station', (68.0, 31.0), 'pasture'),
    ('T8', 'Live Oak Crossing station', (40.0, 22.0), 'caliche / cropland'),
]


def washing_schedule(net, wx, rng=None):
    """Realistic multi-year washing log across all 22 Gulf porcelain sections (no single-section 5-wash anomaly)."""
    rng = rng or np.random.default_rng(C.EV_SEED + 101)
    secs = F.wash_sections(net)
    out = []
    for s in secs:
        for yr in (2021, 2022, 2023, 2024, 2025):
            p = 0.30 if s['shore'] > 4.5 else 0.65
            if rng.random() < p:
                d = dt.date(yr, int(rng.choice([9, 10, 11])), int(rng.integers(1, 28)))
                if dt.date(2021, 9, 1) <= d <= dt.date(2026, 10, 31):
                    out.append(dict(section=s['id'], line=s['line'], s0=s['s0'], s1=s['s1'], date=d, why='pre-season'))
            if yr >= 2022 and rng.random() < 0.32:
                d = dt.date(yr, int(rng.choice([2, 3, 4])), int(rng.integers(1, 28)))
                out.append(dict(section=s['id'], line=s['line'], s0=s['s0'], s1=s['s1'], date=d, why='after flashovers'))
    return secs, out


# Realistic 2026 washing calendar across winter, summer hot washes, and autumn pre-season washes.
# Creates a continuous spread of 31 Oct (ESDD, NSDD) states with TWO-SIDED flips against ESDD-only models:
# - High-NSDD caliche/cropland sections washed mid-summer/early-autumn (moderate ESDD, high NSDD) -> DUE under (ESDD,NSDD), MISSED by ESDD-only!
# - Low-NSDD coastal-marsh sections washed earlier (moderate ESDD, low NSDD) -> NOT DUE under (ESDD,NSDD), FALSELY WASHED by ESDD-only!
PLAN_2026 = {
    'L01-W1': [('2026-03-14', 'after flashovers')], # caliche/cropland (3.37 km): moderate ESDD, high NSDD -> DUE (ESDD-only MISS!)
    'L01-W2': [('2026-10-16', 'pre-season')],       # pasture -> recent wash -> NOT DUE
    'L01-W3': [('2026-10-19', 'pre-season')],       # pasture -> recent wash -> NOT DUE
    'L01-W4': [('2026-02-22', 'after flashovers')], # caliche/cropland (3.81 km): low-mod ESDD, high NSDD -> DUE (ESDD-only MISS!)
    'L01-W5': [('2026-04-12', 'after flashovers')], # caliche/cropland -> high NSDD + mod ESDD -> DUE (ESDD-only MISS!)
    'L02-W1': [('2026-07-15', 'hot wash')],         # pasture, near shore -> high ESDD, mod NSDD -> DUE (NSDD-heavy OVER-CORRECTION MISS!)
    'L02-W2': [('2026-10-11', 'pre-season')],       # coastal marsh (1.56 km): HIGH ESDD, tiny NSDD -> NOT DUE (ESDD-only FALSE POSITIVE!)
    'L02-W3': [('2026-10-16', 'pre-season')],       # pasture -> NOT DUE
    'L02-W4': [('2026-04-18', 'after flashovers')], # caliche/cropland -> DUE
    'L02-W5': [('2026-10-12', 'pre-season')],       # coastal marsh (1.34 km): HIGH ESDD, tiny NSDD -> NOT DUE (ESDD-only FALSE POSITIVE!)
    'L02-W6': [('2026-05-20', 'after flashovers')], # pasture -> DUE
    'L02-W7': [('2026-06-25', 'hot wash')],         # pasture/caliche -> DUE
    'L03-W1': [('2026-10-21', 'pre-season')],       # pasture -> NOT DUE
    'L03-W2': [('2026-03-08', 'after flashovers')], # caliche/cropland (3.29 km): mod ESDD, high NSDD -> DUE
    'L03-W3': [('2026-10-22', 'pre-season')],       # pasture -> NOT DUE
    'L03-W4': [('2026-04-15', 'after flashovers')], # caliche/cropland -> DUE
    'L03-W5': [('2026-10-08', 'pre-season')],       # caliche/cropland washed Oct -> NOT DUE
    'L03-W6': [('2026-10-18', 'pre-season')],       # pasture -> NOT DUE
    'L03-W7': [('2026-10-13', 'pre-season')],       # coastal marsh (2.03 km): HIGH ESDD, tiny NSDD -> NOT DUE (ESDD-only FALSE POSITIVE!)
    'L04-W1': [('2026-10-15', 'pre-season')],       # pasture -> NOT DUE
    'L04-W2': [('2026-08-01', 'hot wash')],         # coastal marsh (3.40 km): mod-high ESDD, tiny NSDD -> NOT DUE (ESDD-only FALSE POSITIVE!)
}


def plan_2026(net, wx, secs, washes, crit, rng=None):
    by = {x['id']: x for x in secs}
    plan = []
    for sid, ws in PLAN_2026.items():
        if sid not in by:
            continue
        s = by[sid]
        for d, why in ws:
            plan.append(dict(section=sid, line=s['line'], s0=s['s0'], s1=s['s1'], date=dt.date.fromisoformat(d), why=why))
    return plan


def test_readings(wx, rng=None):
    """Monthly test insulator deposits (ESDD and NSDD, mg/cm2) on each site's sampling day, driven by the exact
    same physical wind/rain/surface dynamics as the 69 kV lines."""
    rng = rng or np.random.default_rng(C.EV_SEED + 303)
    days = wx['days']
    rows = []
    near = {}
    for code, desc, (x, y), surf in TEST_SITES:
        sd = N._shore_dist(x, y)
        best = min(('APT', 'PAL', 'SHR', 'SED', 'TUL', 'LOK', 'RFP'),
                   key=lambda c: math.hypot(W.PLACES[c][0] - x, W.PLACES[c][1] - y))
        r = W.daily_rain(wx, best)
        e_rate = F.deposit_rate(sd)
        n_rate = F.nsdd_rate(surf)
        e_fac = F.salt_factor(wx, [best])
        n_fac = F.dust_factor(wx, [best])
        esdd = e_rate * 45.0
        nsdd = n_rate * 60.0
        es_ser, ns_ser = {}, {}
        for di, d in enumerate(days):
            esdd = (esdd + e_rate * e_fac[di]) * F.esdd_rain_keep(r[di])
            nsdd = (nsdd + n_rate * n_fac[di] * (1.0 if r[di] < 2.0 else 0.0)) * F.nsdd_rain_keep(r[di])
            es_ser[d] = esdd
            ns_ser[d] = nsdd
        near[code] = (sd, surf, es_ser, ns_ser)
        for yr in range(2022, 2027):
            for mo in range(1, 13):
                if yr == 2026 and mo > 10:
                    continue
                day = int(rng.integers(5, 24))
                d = dt.date(yr, mo, day)
                if d not in es_ser:
                    continue
                if rng.random() < 0.04:
                    continue
                eval_ = es_ser[d] * (1.0 + rng.normal(0, 0.075))
                nval_ = ns_ser[d] * (1.0 + rng.normal(0, 0.080))
                rows.append(dict(site=code, desc=desc, x=x, y=y, surface=surf, date=d,
                                 esdd=max(0.001, eval_), nsdd=max(0.005, nval_)))
    return rows, near
