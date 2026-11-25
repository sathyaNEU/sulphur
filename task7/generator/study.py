"""The 380 load-research study homes: their roster, the contractor's randomisation log (each home shed or held out on
each event day) and their hourly interval kWh, 13:00 to 21:00 local on the 88 summer weekdays. The contractor's head
end sheds a home's switch at 15:45 and restores it at 18:45. The meters are written so that a home's response on a
day it was shed, read against its own 13:00 to 15:00 use scaled by the held-out homes' same-day ratio of 16:00 to
18:00 use to 13:00 to 15:00 use, and put at index 1 by the day's cooling index, is core's study response for that home
and day exactly; core.study() then reads the same figures off the meters as off core's arrays."""
import datetime as dt

import numpy as np

import common as CM
import params as P

HOURS = list(range(13, 21))      # hour beginning, local
PRE = (13, 14)
SHED = (16, 17)


def place(W, r):
    """Each study home's grid position (1 to 8 km from the carrier's Larkin site, core's distances) and its feeder: the
    nearest Larkin feeder."""
    st = W["study"]
    site = W["ct"][0]
    ang = r.uniform(0, 2 * np.pi, len(st["d"]))
    x = site[0] + st["d"] * np.cos(ang)
    y = site[1] + st["d"] * np.sin(ang)
    town = np.flatnonzero(W["dist"] == 0)
    cen = W["cent"][town]
    near = town[np.argmin((x[:, None] - cen[None, :, 0]) ** 2 + (y[:, None] - cen[None, :, 1]) ** 2, axis=1)]
    return x, y, near


def meters(W, idx, r):
    """kWh for every home, weekday and hour. Returns {(home, day): array over HOURS}."""
    st = W["study"]
    n = len(st["d"])
    ev_of = {d: i for i, d in enumerate(P.EVENT_DAYS)}
    prof = np.array([0.78, 0.86, 0.94, 1.0, 1.0, 0.97, 0.88, 0.76])          # 13:00 .. 20:00
    base = np.exp(r.normal(np.log(3.4), 0.28, n))
    # a home's own taste for cooling, and day to day variation in it
    out = {}
    # the hours the golden reads must be large enough to carry the largest responses (a home that took off a lot on a
    # day had that much load to take off): raise a home's level until every shed day is positive with room
    need = np.zeros(n)
    for e, d in enumerate(P.EVENT_DAYS):
        w = W["w"][e]
        F = 0.45 + 0.55 * w
        resp = st["resp"][e]
        tr = st["tr"][e]
        # shed-hour use = pre * ratio - 2 * w * resp; pre * ratio is about 2 * base * F (the two shed hours)
        need = np.maximum(need, np.where(tr, (2 * w * resp + 1.6) / (2 * F * 1.0), 0.0))
    base = np.maximum(base, need * 1.08)
    for di, d in enumerate(P.WEEKDAYS):
        F = 0.45 + 0.55 * idx[d]
        e = ev_of.get(d)
        u = base[:, None] * F * prof[None, :] * np.exp(r.normal(0, 0.09, (n, len(HOURS))))
        if e is None:
            for h in range(n):
                out[(h, d)] = u[h]
            continue
        tr = st["tr"][e]
        w = W["w"][e]
        pre = u[:, 0] + u[:, 1]
        sh = u[:, 3] + u[:, 4]
        ratio = sh[~tr].sum() / pre[~tr].sum()
        resp = st["resp"][e]
        for h in range(n):
            v = u[h].copy()
            if tr[h]:
                target = pre[h] * ratio - 2 * w * resp[h]
                assert target > 0.3, "a study home's shed hours would go negative"
                v[3], v[4] = target * u[h, 3] / sh[h], target * u[h, 4] / sh[h]
                # the quarter hour before 16:00 and the three quarters after 18:00 are shed too, then the snap-back
                take = max(float(st["kap"][h] * st["hw"][h] * st["rc"][e, h]) * w, 0.0)
                v[2] = max(v[2] - 0.25 * take, 0.05)
                v[5] = max(v[5] - 0.75 * take + 0.10 * take, 0.05)
                v[6] = v[6] + 0.22 * take
                v[7] = v[7] + 0.06 * take
            out[(h, d)] = v
    return out


def home_ids(n, r):
    nums = sorted(int(v) for v in r.choice(np.arange(1000, 9000), n, replace=False))
    return ["LR19-%04d" % v for v in nums]


def write(target, W, idx, premises, r):
    st = W["study"]
    n = len(st["d"])
    ids = home_ids(n, r)
    x, y, feeder = place(W, r)
    W["study_feeder"] = feeder
    codes, _ = CM.feeder_codes(W["dist"])
    roster = []
    for h in range(n):
        yr = 2026 - int(st["age"][h])                     # 6 or 7 years old: installed 2020 or 2019
        inst = dt.date(yr, 1, 1) + dt.timedelta(int(r.integers(100, 300)))
        reb = inst - dt.timedelta(int(r.integers(9, 60)))
        pno, addr = premises[h]
        roster.append((ids[h], pno, addr[0], addr[1], codes[int(feeder[h])], "%.3f" % x[h], "%.3f" % y[h],
                       "FX%02d-%06d" % (yr % 100, int(r.integers(100000, 999999))), CM.fmt_date(inst),
                       "Central air conditioner", CM.fmt_date(reb), "MTR-%07d" % int(r.integers(2000000, 2999999))))
    CM.write_csv("%s/%s" % (target, CM.FILES["study_homes"]),
                 ["home_id", "premise_no", "service_address", "city", "feeder", "grid_x_km", "grid_y_km", "switch_serial",
                  "switch_installed", "rebated_equipment", "equipment_installed", "interval_meter"], roster)
    rows = []
    for e, d in enumerate(P.EVENT_DAYS):
        for h in range(n):
            rows.append((ids[h], CM.fmt_date(d), "shed" if st["tr"][e, h] else "held out"))
    CM.write_csv("%s/%s" % (target, CM.FILES["study_assign"]), ["home_id", "event_date", "arm"], rows)
    kwh = meters(W, idx, r)
    mrows = []
    for h in range(n):
        for d in P.WEEKDAYS:
            v = kwh[(h, d)]
            for j, hr in enumerate(HOURS):
                mrows.append((roster[h][11], "%s %02d:00" % (CM.fmt_date(d), hr), "%.3f" % v[j]))
    CM.write_csv("%s/%s" % (target, CM.FILES["study_meters"]), ["interval_meter", "hour_beginning_local", "kwh"], mrows)
    return dict(ids=ids, x=x, y=y, feeder=feeder, rows=len(mrows))
