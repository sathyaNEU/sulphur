"""task22 architecture 2: the billing system's meter reads, taken by the AMR drive-by routes on twenty business-day
cycles, with what that system does to them: estimates when a module goes quiet (trued up by the next actual read),
final and initial reads at a meter exchange, special reads when an account opens or closes, four-dial rollovers,
commercial multipliers, and the June 2025 extract re-run that repeats a month of rows.
"""
import datetime as dt

import numpy as np
import pandas as pd

import params as P

HOLIDAYS = set()
for _y in (2023, 2024, 2025, 2026):
    HOLIDAYS |= {dt.date(_y, 1, 1), dt.date(_y, 7, 4), dt.date(_y, 12, 25)}
    _d = dt.date(_y, 5, 31)
    while _d.weekday() != 0:
        _d -= dt.timedelta(days=1)
    HOLIDAYS.add(_d)
    _d = dt.date(_y, 9, 1)
    while _d.weekday() != 0:
        _d += dt.timedelta(days=1)
    HOLIDAYS.add(_d)
    _d = dt.date(_y, 11, 1)
    _n = 0
    while True:
        if _d.weekday() == 3:
            _n += 1
            if _n == 4:
                break
        _d += dt.timedelta(days=1)
    HOLIDAYS.add(_d)


def business_days(year, month):
    d = dt.date(year, month, 1)
    out = []
    while d.month == month:
        if d.weekday() < 5 and d not in HOLIDAYS:
            out.append(d)
        d += dt.timedelta(days=1)
    return out


def cycle_dates(c):
    """The c-th business day of each month from August 2023, up to the last simulated day."""
    out = []
    y, m = 2023, 8
    while True:
        bd = business_days(y, m)
        d = bd[min(c, len(bd)) - 1]
        if d > P.SIM1:
            break
        out.append(d)
        m += 1
        if m == 13:
            y, m = y + 1, 1
    return out


def hdd65(w, a, b):
    i0, i1 = (a - P.SIM0).days, (b - P.SIM0).days
    return float(np.clip(65.0 - w.air[i0:i1], 0, None).sum())


def reads(w):
    rng = np.random.default_rng([P.SEED, 20])
    pr = w.pr
    cum = np.concatenate([np.zeros((len(pr), 1), np.float64), np.cumsum(w.R.astype(np.float64), axis=1)], axis=1)
    acc_by = {}
    for r in w.accounts.itertuples():
        acc_by.setdefault(r.PremiseID, []).append(r)
    for k in acc_by:
        acc_by[k].sort(key=lambda a: a.StartDate if isinstance(a.StartDate, dt.date) else dt.date(1900, 1, 1))
    cyc_cache = {c: cycle_dates(c) for c in range(1, 21)}
    out = []
    fails = set(rng.choice(len(pr), int(0.05 * len(pr)), replace=False))
    for i, p in pr.iterrows():
        prem = int(p["premise"])
        mult = int(p["multiplier"])
        accs = acc_by.get(prem, [])
        exch = p["exch_date"] if isinstance(p["exch_date"], dt.date) else None
        meters = []
        if exch:
            meters.append(dict(meter=p["old_meter"], until=exch, init=float(rng.integers(0, 9999)) * mult))
            meters.append(dict(meter=p["meter"], until=dt.date(2100, 1, 1), init=float(rng.integers(0, 4)) * mult))
        else:
            meters.append(dict(meter=p["meter"], until=dt.date(2100, 1, 1), init=float(rng.integers(0, 9999)) * mult))
        ex_day = (exch - P.SIM0).days if exch else None

        def index(day):
            m = meters[0] if (exch is None or day <= ex_day) else meters[1]
            reg = cum[i, day] - (cum[i, ex_day] if (exch and day > ex_day) else 0.0)
            return m, (m["init"] + reg)

        def account_on(d):
            cur = None
            for a in accs:
                if a.StartDate is not None and a.StartDate <= d and (a.EndDate is None or d < a.EndDate):
                    cur = a.AccountID
            return cur

        events = []
        for d in cyc_cache[int(p["cycle"])]:
            events.append((d, "A"))
        for a in accs:
            if a.StartDate is not None and P.SIM0 < a.StartDate <= P.SIM1:
                events.append((a.StartDate, "S"))
            if a.EndDate is not None and P.SIM0 < a.EndDate <= P.SIM1:
                events.append((a.EndDate, "S"))
        if exch:
            events = [e for e in events if e[0] != exch]
            events.append((exch, "F"))
            events.append((exch, "I"))
        events = sorted(set(events), key=lambda e: (e[0], "FIAS".index(e[1]) if e[1] in "FIAS" else 9))
        # module failures: a run of one to three cycle reads estimated
        failing = set()
        if i in fails:
            cyc = [e[0] for e in events if e[1] == "A"]
            k0 = int(rng.integers(2, len(cyc) - 4))
            for k in range(k0, k0 + int(rng.integers(1, 4))):
                failing.add(cyc[k])
        last_idx = None
        last_meter = None
        hist = []           # (date, consumption) of actual-to-actual periods for the estimator
        est_carry = None
        last_actual_date = None
        last_actual_idx = None
        for d, typ in events:
            day = (d - P.SIM0).days
            if day >= len(cum[i]):
                continue
            m, raw = index(day)
            if typ == "I":
                m = meters[1]
                raw = m["init"]
            dials = raw / mult
            shown = int(np.floor(dials)) % 10000
            acct = account_on(d) if typ != "S" else (account_on(d) or account_on(d - dt.timedelta(days=1)))
            if typ == "A" and d in failing and last_actual_date is not None:
                days_ = (d - last_actual_date).days
                same = [c for (dd, c, n) in hist if abs((dd - (d - dt.timedelta(days=365))).days) < 20]
                if same:
                    lastyr = d - dt.timedelta(days=365)
                    est = same[0] * hdd65(w, last_actual_date, d) / max(1.0, hdd65(w, lastyr - dt.timedelta(days=days_), lastyr))
                else:
                    per_day = hist[-1][1] / max(1, hist[-1][2]) if hist else 2.0
                    est = per_day * days_
                est_d = int(max(0.0, round(est / mult)))
                base_idx = est_carry if est_carry is not None else last_actual_idx
                eidx = (base_idx + est_d) % 10000
                out.append(dict(PremiseID=prem, MeterID=m["meter"], AccountID=acct, Cycle=int(p["cycle"]),
                                ReadDate=d, ReadType="E", MeterIndex=int(eidx), Multiplier=mult,
                                ConsumptionCcf=int(est_d * mult)))
                est_carry = eidx
                continue
            prev = est_carry if est_carry is not None else last_idx
            if typ == "I" or prev is None:
                cons = 0
            else:
                diff = shown - prev
                if est_carry is not None:
                    if diff < -5000:
                        diff += 10000
                elif diff < 0:
                    diff += 10000
                cons = int(diff * mult)
            out.append(dict(PremiseID=prem, MeterID=m["meter"], AccountID=acct, Cycle=int(p["cycle"]),
                            ReadDate=d, ReadType=typ, MeterIndex=shown, Multiplier=mult, ConsumptionCcf=cons))
            if typ in ("A", "S", "F") and last_actual_date is not None and m is last_meter and est_carry is None:
                hist.append((d, ((shown - last_actual_idx) % 10000) * mult, max(1, (d - last_actual_date).days)))
            last_idx = shown
            last_meter = m
            est_carry = None
            if typ != "F":
                last_actual_date, last_actual_idx = d, shown
            else:
                last_actual_date, last_actual_idx = d, None
            if typ == "I":
                last_actual_date, last_actual_idx = d, shown
    df = pd.DataFrame(out)
    df["AccountID"] = df["AccountID"].astype("Int64")
    return df
