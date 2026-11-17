"""The Servizio Strade Alta Ardesa's records on the calendar. `core.build(SEED)` is the world; this file gives every
storm, every hour of long rain and every station visit a date and a clock time, turns the recorded minutes into tips
by letting the bucket fill and tip, and lays out what each instrument wrote. Nothing here draws from core's streams
or changes one of its arrays."""
import datetime as dt
import math
import os
import sys
from zoneinfo import ZoneInfo

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import core as C  # noqa: E402

EPOCH = dt.datetime(2009, 1, 1)            # the station loggers' clock: UTC+1 all year
ROME = ZoneInfo("Europe/Rome")
UTC = dt.timezone.utc
YEARS = [2009 + s for s in range(C.G_SEASONS)]
BUCKET = {"A": 0.2, "B": 0.1}
MINGAP = 8 * 3600                          # no two rain events at a station closer than this
STORM_LEN = C.M * 60
MONTHS = 6

# name: code, road km, easting, northing (ETRS89 / UTM 33N), elevation, mean annual precipitation 1991-2020 (mm)
STATIONS = {
    "Valfosca":   ("VFO", 6.4, 333420, 5145180, 642, 1512),
    "Pradalt":    ("PRD", 14.9, 339730, 5149260, 978, 1236),
    "Rio Scuro":  ("RSC", 18.2, 341850, 5151420, 1118, 1148),
    "Malga Sora": ("MSO", 21.3, 343650, 5153410, 1306, 1204),
    "Forcella":   ("FRC", 27.8, 347240, 5157620, 1561, 1318),
    "Costarossa": ("CSR", 33.6, 350180, 5161830, 1887, 1442),
}
ORDER = ["Valfosca", "Pradalt", "Rio Scuro", "Malga Sora", "Forcella", "Costarossa"]   # the round, up the valley
# source area: offset from its governing station (m east, m north), elevation
SOURCES = {
    "Rio Gelt":   (-1270, 1275, 1480), "Rio Sass":   (1120, -1657, 1690), "Rio Marden": (-2300, 2504, 2060),
    "Rio Ciadin": (-2200, 1890, 2180), "Rio Larin":  (3800, -2592, 2010), "Rio Toval":  (-3050, 2740, 2290),
    "Rio Bianc":  (1650, -1455, 2410),
    "Scuro 1": (400, 0, 1340), "Scuro 2": (-300, 742, 1560), "Scuro 3": (-1190, 160, 1720), "Scuro 4": (-1260, 1140, 1930),
}
CROSSING_KM = {"Rio Gelt": 7.9, "Rio Sass": 13.2, "Rio Marden": 16.2, "Rio Ciadin": 22.4, "Rio Larin": 24.2,
               "Rio Toval": 29.9, "Rio Bianc": 32.1}
GRID_E, GRID_N = (326, 357), (5140, 5167)  # radar pixels, km lines


def rng(k):
    return np.random.default_rng([C.SEED, 9000 + k])


def sec(d):
    """a naive datetime on the loggers' clock, in seconds from the epoch"""
    return int((d - EPOCH).total_seconds())


def civil_to_logger(d):
    """a civil (Europe/Rome) wall-clock datetime on the loggers' clock"""
    return d.replace(tzinfo=ROME).astimezone(UTC).replace(tzinfo=None) + dt.timedelta(hours=1)


def easter_monday(y):
    a, b, c = y % 19, y // 100, y % 100
    d, e = b // 4, b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    m_ = (32 + 2 * e + 2 * i - h - k) % 7
    n = (a + 11 * h + 22 * m_) // 451
    month, day = (h + m_ - 7 * n + 114) // 31, (h + m_ - 7 * n + 114) % 31 + 1
    return dt.date(y, month, day) + dt.timedelta(days=1)


HOLIDAYS = {(4, 25), (5, 1), (6, 2), (8, 15), (11, 1)}


def working(d):
    return d.weekday() < 5 and (d.month, d.day) not in HOLIDAYS and d != easter_monday(d.year)


def next_working(d, step=1):
    while not working(d):
        d += dt.timedelta(days=step)
    return d


def point(name):
    """easting, northing of a station or a source area"""
    if name in STATIONS:
        return STATIONS[name][2], STATIONS[name][3]
    dep = C.ALL[name]["depot"]
    return STATIONS[dep][2] + SOURCES[name][0], STATIONS[dep][3] + SOURCES[name][1]


def pixel(name):
    e, n = point(name)
    return e // 1000, n // 1000


# ------------------------------------------------------------------------------------------------- the visits
def visits():
    """Every station's visits: the opening in late April, a read near the first of each month, the closing in early
    November. Returns {(station, season): [logger seconds x 7]}, the civil datetimes and who went."""
    r = rng(1)
    base = {"Valfosca": (8, 35), "Pradalt": (9, 40), "Rio Scuro": (10, 35), "Malga Sora": (11, 25), "Forcella": (13, 10),
            "Costarossa": (14, 20)}
    out, civil, who = {}, {}, {}
    for s, y in enumerate(YEARS):
        for b in range(MONTHS + 1):
            if b == 0:
                day = next_working(dt.date(y, 4, 22) + dt.timedelta(days=int(r.integers(0, 6))))
            elif b == MONTHS:
                day = next_working(dt.date(y, 11, 3) + dt.timedelta(days=int(r.integers(0, 4))))
            else:
                slip = int(r.choice([-2, -1, 0, 0, 0, 1, 1, 2, 3]))
                day = dt.date(y, 5 + b, 1) + dt.timedelta(days=slip)
                day = next_working(day, 1 if slip >= 0 else -1)
            split = int(r.integers(2, 5)) if r.random() < 0.24 else None
            u = r.random()
            tech = "L. Comboni" if u < 0.05 else "B. Panatta" if (y >= 2019 and u < 0.37) else "A. Cundari"
            late = float(r.normal(0, 14))
            for i, st in enumerate(ORDER):
                d, (hh, mm) = day, base[st]
                if split is not None and i >= split:
                    d = next_working(day + dt.timedelta(days=1))
                    hh, mm = base[ORDER[i - split]]
                if r.random() < 0.04:
                    d = next_working(d + dt.timedelta(days=1))
                mins = hh * 60 + mm + late + float(r.normal(0, 11))
                mins = int(round(mins / 5.0)) * 5
                cv = dt.datetime(d.year, d.month, d.day) + dt.timedelta(minutes=mins)
                civil[(st, s, b)] = cv
                who[(st, s, b)] = tech
                out.setdefault((st, s), []).append(sec(civil_to_logger(cv)))
    return out, civil, who


# ------------------------------------------------------------------------------------------- the calendar of rain
def spell_parts(r, k, total, low):
    parts = np.full(k, low) + r.multinomial(total - low * k, np.full(k, 1.0 / k))
    return [int(x) for x in parts]


def tent(v, r):
    """a spell's hours: light at both ends, heaviest somewhere in the middle"""
    v = sorted(v)
    left, right = [], []
    for i, x in enumerate(v):
        (left if (i + int(r.integers(0, 2))) % 2 == 0 else right).append(x)
    return np.array(left + right[::-1])


def place(r, n, w0, w1, busy):
    """n storm onsets in [w0, w1 - STORM_LEN], each at least MINGAP clear of the busy windows and of one another"""
    segs, a = [], w0
    for b0, b1 in sorted(busy):
        e = b0 - MINGAP - STORM_LEN
        if e > a:
            segs.append((a, e))
        a = max(a, b1 + MINGAP)
    if w1 - STORM_LEN > a:
        segs.append((a, w1 - STORM_LEN))
    step = STORM_LEN + MINGAP
    cap = np.array([int((e - a) // step) + 1 for a, e in segs])
    assert cap.sum() >= n, "an interval cannot hold its storms"
    lens = np.array([e - a for a, e in segs], float)
    alloc = np.zeros(len(segs), int)
    for _ in range(n):
        p = lens * (cap > alloc)
        alloc[r.choice(len(segs), p=p / p.sum())] += 1
    starts, bounds = [], []
    for (a, e), m in zip(segs, alloc):
        if m == 0:
            continue
        slack = (e - a) - (m - 1) * step
        cuts = np.sort(r.uniform(0, slack, m))
        for i in range(m):
            starts.append(a + cuts[i] + i * step)
            bounds.append((a, e))
    starts = np.array(starts)
    # storms of this valley build in the afternoon: move each towards one where its neighbours leave room
    for _ in range(3):
        for i in range(len(starts)):
            lo = max(bounds[i][0], starts[i - 1] + step) if i > 0 and bounds[i - 1] == bounds[i] else bounds[i][0]
            hi = min(bounds[i][1], starts[i + 1] - step) if i + 1 < len(starts) and bounds[i + 1] == bounds[i] else bounds[i][1]
            if r.random() > 0.86 or hi <= lo:
                continue
            hour = float(np.clip(r.normal(15.6, 2.4), 9.5, 22.5))
            d0, d1 = int(lo // 86400), int(hi // 86400)
            cand = [d * 86400 + hour * 3600 for d in range(d0, d1 + 1)]
            cand = [t for t in cand if lo <= t <= hi]
            if cand:
                starts[i] = min(cand, key=lambda t: abs(t - starts[i]))
    return np.floor(starts).astype(np.int64)


def calendar(W, V):
    """Every storm's onset and every spell of long rain, station by station. The long rain is the valley's: its
    spells come to every station within an hour or two of each other; the storms are each station's own."""
    r = rng(2)
    onset = {d: np.zeros(W[d]["N"], np.int64) for d in W}
    spells = {d: [] for d in W}                # (season, interval, start, hourly recorded depths)
    for s in range(C.G_SEASONS):
        y = YEARS[s]
        for m in range(MONTHS):
            v0 = max(V[(d, s)][m] for d in W) + 10 * 3600
            v1 = min(V[(d, s)][m + 1] for d in W) - 10 * 3600
            k = int(r.integers(4, 7))
            base, wide = spell_parts(r, k, 40, 5), None
            wide = [int(round(1.5 * x)) for x in base]
            wide[int(np.argmax(wide))] += 60 - sum(wide)
            longest = max(wide) * 3600
            for _ in range(5000):
                t = np.sort(r.uniform(v0 + 6 * 3600, v1 - 6 * 3600 - longest - 2 * 3600, k))
                if k == 1 or np.all(np.diff(t) >= longest + 30 * 3600):
                    break
            else:
                raise AssertionError("no room for the spells of %d month %d" % (y, m))
            for d in W:
                w = W[d]
                parts = wide if C.DEPOTS[d].get("wet", 40) == 60 else base
                hours = w["front_rec"][s * MONTHS + m]
                assert len(hours) == sum(parts)
                busy, at = [], 0
                for j in range(k):
                    st = int(t[j] + r.uniform(-5400, 5400))
                    spells[d].append((s, s * MONTHS + m, st, tent(hours[at:at + parts[j]], r)))
                    busy.append((st, st + parts[j] * 3600))
                    at += parts[j]
                idx = np.nonzero(w["ivl"] == s * MONTHS + m)[0]
                w0 = max(v0, sec(dt.datetime(y, 5, 2))) if m == 0 else v0
                w1 = min(v1, sec(dt.datetime(y, 10, 30, 23, 30))) if m == MONTHS - 1 else v1
                st = place(r, len(idx), w0, w1, busy)
                onset[d][r.permutation(idx)] = st
    return onset, spells


# ---------------------------------------------------------------------------------------------------- the tips
def tips(W, onset, spells):
    """Tip times by station: the bucket fills with what the gauge recorded and tips each time it holds a bucketful.
    A storm's recorded minutes fall evenly inside the minute, the long rain's hours evenly inside the hour, and what
    is left in the bucket waits for the next rain."""
    r = rng(3)
    out = {}
    for d, w in W.items():
        b = BUCKET[w["model"]]
        alls = []
        for s in range(C.G_SEASONS):
            t0, du, de = [], [], []
            for n in np.nonzero(w["season"] == s)[0]:
                t0.append(onset[d][n] + 60.0 * np.arange(C.M))
                du.append(np.full(C.M, 60.0))
                de.append(w["rec"][n])
            for (ss, _, st, hours) in spells[d]:
                if ss == s:
                    t0.append(st + 3600.0 * np.arange(len(hours)))
                    du.append(np.full(len(hours), 3600.0))
                    de.append(hours)
            t0, du, de = np.concatenate(t0), np.concatenate(du), np.concatenate(de)
            o = np.argsort(t0, kind="stable")
            t0, du, de = t0[o], du[o], np.maximum(de[o], 0.0)
            u0 = float(r.random()) * b * 0.6
            cum = np.cumsum(de) + u0
            lev = b * np.arange(1, int(math.floor(cum[-1] / b)) + 1)
            i = np.searchsorted(cum, lev, side="left")
            prev = np.where(i > 0, cum[np.maximum(i - 1, 0)], u0)
            tt = np.floor(t0[i] + du[i] * (lev - prev) / de[i]).astype(np.int64)
            assert np.all(np.diff(tt) >= 1), "two tips in one second at %s" % d
            alls.append(tt)
        out[d] = np.concatenate(alls)
    return out


# ----------------------------------------------------------------------------------------- the weather detector
def detector(W, onset, spells):
    """The present-weather detector's rows: one for each ten-minute block with precipitation, the blocks counted from
    the moment it first saw precipitation in the episode. Returns per station (block start, code, intensity mm/h)."""
    r = rng(4)
    out = {}
    for d, w in W.items():
        kap = C.KAPPA[w["model"]]
        N = w["N"]
        k = np.arange(C.M // 10)[None, :]
        inten = np.round(w["opt"] * 6.0, 2)
        show = w["wet"] & (inten >= 0.01)
        mix = r.random(w["opt"].shape)
        code = np.where(w["hail10"],
                        np.where(w["opt"] >= 1.5, np.where(mix < 0.45, "+RAGR", "GR"), np.where(mix < 0.35, "RAGS", "GS")),
                        np.where(inten >= 7.6, "+RA", np.where(inten >= 2.5, "RA", np.where(inten >= 0.3, "-RA", "DZ"))))
        t = (onset[d][:, None] + 600 * k)[show]
        ts, cs, vs = [t], [code[show]], [inten[show]]
        for (_, _, st, hours) in spells[d]:
            true = hours / (1.0 - kap * hours)
            v = np.repeat(true, 6) * math.exp(0.30 * r.standard_normal()) * np.exp(0.12 * r.standard_normal(6 * len(hours)))
            v = np.round(v, 2)
            ok = v >= 0.1
            ts.append((st + 600 * np.arange(len(v)))[ok])
            vs.append(v[ok])
            cs.append(np.where(v[ok] >= 7.6, "+RA", np.where(v[ok] >= 2.5, "RA", np.where(v[ok] >= 0.3, "-RA", "DZ"))))
        t, c, v = np.concatenate(ts), np.concatenate(cs), np.concatenate(vs)
        o = np.argsort(t, kind="stable")
        out[d] = (t[o], c[o], v[o])
    return out


def last_wet(w):
    """minutes from a storm's onset to the end of its last block with precipitation"""
    idx = np.where(w["wet"].any(axis=1), w["wet"].shape[1] - np.argmax(w["wet"][:, ::-1], axis=1), 1)
    return idx * 600


# --------------------------------------------------------------------------------------------------- the radar
def neighbours():
    """the pixels a cell passing over a station's ground also covers: a fixed ring around the station and its sources"""
    r = rng(5)
    out = {}
    taken = {pixel(n) for n in list(STATIONS) + list(SOURCES)}
    for d in STATIONS:
        own = [pixel(d)] + [pixel(s) for s in C.ALL if C.ALL[s]["depot"] == d]
        ring = set()
        for (pe, pn) in own:
            for de in (-1, 0, 1):
                for dn in (-1, 0, 1):
                    q = (pe + de, pn + dn)
                    if q not in taken and GRID_E[0] <= q[0] < GRID_E[1] and GRID_N[0] <= q[1] < GRID_N[1]:
                        ring.add(q)
        ring = sorted(ring)
        pick = [ring[i] for i in sorted(r.choice(len(ring), min(11, len(ring)), replace=False))]
        out[d] = [(q, float(r.uniform(0.84, 1.22)), float(r.uniform(0.3, 0.8))) for q in pick]
        taken |= set(pick)
    return out


def radar_rows(W, onset):
    """The agency's convective-cell extract, 2013 to 2026: for each cell that crossed a station's ground, the
    60-minute maximum on every pixel of its footprint. Returns the events in time order."""
    r = rng(6)
    nb = neighbours()
    ev = []
    for d, w in W.items():
        era = np.nonzero(w["season"] >= C.G_SEASONS - C.R_SEASONS)[0]
        vals = [C.radar(w, j) for j in range(1 + len(w["pts"]))]
        end = last_wet(w)
        zn = r.standard_normal((w["N"], len(nb[d])))
        nu = C.SIG_NU * r.standard_normal((w["N"], len(nb[d])))
        seen = r.random((w["N"], len(nb[d])))
        for n in era:
            t0 = onset[d][n] - 3600 - int(r.integers(240, 900))
            t1 = onset[d][n] - 3600 + int(end[n]) + int(r.integers(300, 1500))
            rows = [(pixel(d), float(vals[0][n]))] + [(pixel(s), float(vals[1 + j][n])) for j, s in enumerate(w["pts"])]
            for q, ((pix, f, rho), z) in enumerate(zip(nb[d], zn[n])):
                if seen[n, q] < 0.78:
                    e = rho * w["e"][n, 0] + math.sqrt(1.0 - rho * rho) * C.SIG_E * z
                    rows.append((pix, float(f * w["rb"][n] * w["base"][n] * math.exp(C.GAMMA * e + nu[n, q]))))
            ev.append((t0 // 300 * 300, -(-t1 // 300) * 300, d, int(n), rows))
    ev.sort(key=lambda x: (x[0], x[2]))
    return ev, nb


def pixel_ids():
    """the product's pixel numbers: the raster used to 2018, and the one in use since the 2019 season"""
    new, old = {}, {}
    for pn in range(GRID_N[0], GRID_N[1]):
        for pe in range(GRID_E[0], GRID_E[1]):
            new[(pe, pn)] = 40000 + (pn - GRID_N[0]) * (GRID_E[1] - GRID_E[0]) + (pe - GRID_E[0])
            old[(pe, pn)] = (5200 - pn) * 212 + (pe - 250)
    return new, old


# ------------------------------------------------------------------------------------- the research valley
def research_rows(W, onset):
    """The university's event table for the Rio Scuro valley: each weighing gauge's largest 60-minute depth in each
    convective event it recorded, 2013 to 2026."""
    r = rng(7)
    w = W["Rio Scuro"]
    era = np.nonzero(w["season"] >= C.G_SEASONS - C.C_SEASONS)[0]
    end = last_wet(w)
    rows = []
    for j, s in enumerate(C.RESEARCH):
        x = C.source_max(w, s)
        for n in era:
            v = round(float(x[n]), 2)
            if v < 0.1:
                continue
            t0 = onset["Rio Scuro"][n] - 3600 + int(r.integers(-240, 120))
            t1 = onset["Rio Scuro"][n] - 3600 + int(end[n]) + int(r.integers(60, 900))
            rows.append((t0 // 60 * 60, t1 // 60 * 60, s, int(n), v))
    rows.sort(key=lambda x: (x[0], x[2]))
    return rows


# ------------------------------------------------------------------------------------- the rainfall normal
def normal_grid():
    """Mean annual precipitation 1991 to 2020 on 500 m cells: a smooth field that takes the stations' and the source
    areas' values at their cells."""
    e0, n0 = GRID_E[0] * 1000, GRID_N[0] * 1000
    ne, nn = (GRID_E[1] - GRID_E[0]) * 2, (GRID_N[1] - GRID_N[0]) * 2
    cx = e0 + 250.0 + 500.0 * np.arange(ne)
    cy = n0 + 250.0 + 500.0 * np.arange(nn)
    X, Y = np.meshgrid(cx, cy)
    along = ((X - 333000) * 0.62 + (Y - 5145000) * 0.78) / 1000.0
    across = (-(X - 333000) * 0.78 + (Y - 5145000) * 0.62) / 1000.0
    field = 1290 + 4.0 * along + 21.0 * np.abs(across) + 46 * np.sin(X / 2900.0) * np.cos(Y / 3700.0) + 31 * np.sin((X + Y) / 5200.0)
    target = {}
    for name, v in STATIONS.items():
        target[name] = float(v[5])
    for s, c in C.ALL.items():
        target[s] = float(round(STATIONS[c["depot"]][5] * c["map"]))
    cells = {}
    for name in target:
        e, n = point(name)
        cells[name] = (int((e - e0) // 500), int((n - n0) // 500))
    assert len(set(cells.values())) == len(cells), "two points share a cell of the rainfall normal"
    P = np.array([(cx[i], cy[j]) for i, j in cells.values()])
    dv = np.array([target[k] - field[cells[k][1], cells[k][0]] for k in cells])
    sg = 620.0
    G = np.exp(-((P[:, None, 0] - P[None, :, 0]) ** 2 + (P[:, None, 1] - P[None, :, 1]) ** 2) / (2 * sg * sg))
    amp = np.linalg.solve(G, dv)
    for (px, py), a in zip(P, amp):
        field += a * np.exp(-((X - px) ** 2 + (Y - py) ** 2) / (2 * sg * sg))
    field = np.round(field).astype(int)
    for k, (i, j) in cells.items():
        assert field[j, i] == int(target[k]), (k, field[j, i], target[k])
    return cx, cy, field, cells


# ---------------------------------------------------------------------------------------------- the whole world
def build():
    W = C.build(C.SEED)
    for d, w in W.items():                 # the pixel pairs and the weighing gauges as the instruments wrote them
        assert float((w["rec"] * 60.0).max()) < 3600.0 * BUCKET[w["model"]], "a bucket would tip twice a second"
    V, civil, who = visits()
    onset, spells = calendar(W, V)
    T = tips(W, onset, spells)
    D = detector(W, onset, spells)
    R, nb = radar_rows(W, onset)
    return dict(W=W, V=V, civil=civil, who=who, onset=onset, spells=spells, tips=T, detector=D, radar=R, neigh=nb,
                research=research_rows(W, onset), normal=normal_grid())


if __name__ == "__main__":
    import time
    t = time.time()
    wd = build()
    print("built in %.0f s" % (time.time() - t))
    for d in ORDER:
        print(d, "tips", len(wd["tips"][d]), "detector rows", len(wd["detector"][d][0]), "spells", len(wd["spells"][d]))
    print("radar events", len(wd["radar"]), "rows", sum(len(e[4]) for e in wd["radar"]), "research rows", len(wd["research"]))
    px = {n: pixel(n) for n in list(STATIONS) + list(SOURCES)}
    assert len(set(px.values())) == len(px)
    for n in px:
        e, nn = point(n)
        assert min(e % 1000, 1000 - e % 1000, nn % 1000, 1000 - nn % 1000) >= 120, (n, e % 1000, nn % 1000)
        if n in SOURCES:
            de, dn = SOURCES[n][0], SOURCES[n][1]
            assert abs(math.hypot(de, dn) / 1000.0 - C.ALL[n]["km"]) < 0.01, n
    on = wd["onset"]
    for d in ORDER:
        hrs = (on[d] % 86400) / 3600.0
        print(d, "onset hour quartiles", np.round(np.quantile(hrs, [0.1, 0.25, 0.5, 0.75, 0.9]), 1))
