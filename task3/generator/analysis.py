"""Every figure of the answer, computed from the shipped files alone. Nothing here imports the world: the tips, the
visit book, the detector's database, the radar extract, the rainfall normal, the registers and the research valley's
tables are read the way an analyst reads them, and the regulation's constants are the ones its text states
(checks.py reads the PDF and asserts each).

The golden route: each station's tips cleaned (re-sent rows once, the technicians' tip tests out), storms cut at six
dry hours, each tip's water spread over the time since the tip before and counted by the clock minute; one loss by
rate per bucket model fitted through the storage gauge account and put back minute by minute; on storms with a hail
or graupel block the storm's water placed on the detector's ten-minute intensities; each source area carried from
its governing station by the mean log ratio of the radar's pixel pairs; counted against the triggering depth over
the eighteen seasons. Around it: the battery of defensible rebuilds, the shortcut routes, the cruder rivals and the
research valley's check."""
import datetime as dt
import math
import os
import sqlite3
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd
from openpyxl import load_workbook

# the regulation (rev. 4): 2.1 the warm season, 2.2 six dry hours, 2.3 sixty consecutive minutes, 4.1 the lines
SEASON = ((5, 1), (10, 31))
GAP = 6 * 3600
LINES = (1.0, 3.0)
EVEN = 5.0                                  # 3.2: the depth reached five times a season
EPOCH = np.datetime64("2009-01-01T00:00:00")
ROME = ZoneInfo("Europe/Rome")

LOSS_WAYS = ("recip", "scaled")             # the tipping-time form, alone or with a static factor fitted beside it
POOL_WAYS = ("model", "gauge")
READ_WAYS = ("spread", "lump", "tip")       # a tip's water over the time since the tip before, or in its own minute,
STEP_WAYS = (1, 2, 3, 5)                    # the rate read on one-, two-, three- or five-minute totals; or tip by tip
READS = tuple((rd, st) for rd in ("spread", "lump") for st in STEP_WAYS) + (("tip", 1),)
# the battery's ways of the loss: the tipping-time form on every reading of the rate, and tip by tip its first-order form too
LOSS_READS = tuple((fo, rd, st) for fo in LOSS_WAYS for rd, st in READS) + (("lin", "tip", 1),)
# ways outside the battery, each set against the tipping-time form on the same reading of the rate through the storage
# gauge account: the first-order form on minute totals is not refused by it and is carried in every stated band
# (CARRIED); a power law and totals of ten and fifteen minutes are refused by it
CARRIED = "first-order form"
REFUSED = {"first-order form": tuple(("lin", rd, st) for rd, st in READS if rd != "tip"),
           "power law": tuple(("power", rd, st) for rd, st in READS),
           "10-minute totals": (("recip", "spread", 10), ("recip", "lump", 10)),
           "15-minute totals": (("recip", "spread", 15), ("recip", "lump", 15))}
SITE_WAYS = ("geo", "median", "sums", "trim", "geo3", "gauge3", "pairs", "upper")
HAIL_WAYS = ("profile", "weighted", "onset", "carried")
CRUDE_SITE = ("slope", "top", "q90", "qq")
CRUDE_HAIL = ("dry", "even", "optical", "hailonly")
# ways the files do not refuse and the battery does not hold: inside every band, crossed with every way of the battery
MORE_SITE, MORE_HAIL = ("qq",), ("hailonly",)
CRUDE_STEP = (10, 15)
COUNT_FLOOR, DEPTH_FLOOR, OWN_FLOOR = 0.04, 0.015, 0.03
# room above the widest way: a second implementation's windows (slid by the second, or a hail storm's blocks laid on clock
# minutes) move a count by a storm or two and a depth by a tenth of a millimetre
TOP_STORMS, TOP_SHARE, TOP_MM = 1.0, 0.01, 0.1
K_LIMIT = 0.0075                            # the fit's upper limit on the time lost at a tip, hours per mm

FILES = dict(tips="tips_%s_2009-2026.csv", visits="station_visit_book_2009-2026.csv", pw="present_weather_blocks.sqlite",
             radar="radar_cells_p60max_2013-2026.csv", pixels="radar_pixels.csv",
             normal="precipitation_normal_1991-2020_500m.csv", rs_events="rio_scuro_weighing_gauges_events_2013-2026.csv",
             rs_gauges="rio_scuro_weighing_gauges.csv", stations="road_stations_register.xlsx",
             crossings="gully_crossings_register.xlsx")


class Rates(dict):
    """Triggering storms a season by member, with .even (the depth reached five times a season) and .upper."""


def secs(strings):
    return (np.array([s[:19] for s in strings], dtype="datetime64[s]") - EPOCH).astype(np.int64)


def civil(date, hhmm):
    """a visit's local date and time on the loggers' clock (UTC+1), in seconds"""
    d = dt.datetime.strptime(date + " " + hhmm, "%Y-%m-%d %H:%M").replace(tzinfo=ROME)
    u = d.astimezone(dt.timezone.utc).replace(tzinfo=None) + dt.timedelta(hours=1)
    return int((u - dt.datetime(2009, 1, 1)).total_seconds())


def put_back(r, k, form, per_hour=60.0):
    if form == "lin":
        return r * (1.0 + k * per_hour * r)
    if form == "scaled":
        return k[0] * r / np.maximum(1.0 - k[1] * per_hour * r, 0.02)
    if form == "power":                      # the calibration curve as a power of the recorded rate
        return k[0] * r * np.maximum(per_hour * r, 1e-9) ** (k[1] - 1.0)
    return r / np.maximum(1.0 - k * per_hour * r, 0.02)


def under_read(k, form="recip", true_rate=100.0):
    """what the bucket fails to record at a true rate, in per cent, under a fitted loss"""
    lo, hi = 0.0, true_rate
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if float(put_back(mid, k, form, 1.0)) < true_rate else (lo, mid)
    return 100.0 * (1.0 - lo / true_rate)


def six(b):
    """the largest total over six consecutive ten-minute blocks"""
    cs = np.concatenate([np.zeros((b.shape[0], 6)), np.cumsum(b, axis=1)], axis=1)
    return (cs[:, 6:] - cs[:, :-6]).max(axis=1)


def band(golden, family, floor):
    lo, hi = min(family + [golden]), max(family + [golden])
    return [min(lo, golden * (1.0 - floor)), max(hi, golden * (1.0 + floor))]


def rank_carry(x, a, b):
    """the two pixels' depths matched rank for rank, unpaired: each station depth is carried by the ratio of the
    pixels' depths at its own rank among the storms"""
    a, b = np.sort(a), np.sort(b)
    pr = (np.argsort(np.argsort(x)) + 0.5) / len(x)
    q = (np.arange(len(a)) + 0.5) / len(a)
    return x * np.interp(pr, q, a) / np.maximum(np.interp(pr, q, b), 1e-9)


def at_line(x, seasons):
    return float(np.sort(x)[::-1][int(round(EVEN * seasons)) - 1])


def upper_mean(x, seasons, per=5):
    return float(np.sort(x)[::-1][:per * seasons].mean())


class Station:
    """One road station's records, cleaned and laid on a compact minute line: each storm's minutes, then 59 empty ones."""

    def __init__(self, code, name, bucket, model, xy, tip_times, visits, det, dedupe=True, drop_tests=True, strict=True,
                 season_by="max", stamp="end"):
        self.code, self.name, self.bucket, self.model, self.xy = code, name, bucket, model, xy
        raw = np.sort(tip_times)
        t = np.unique(raw) if dedupe else raw
        self.resent = int(len(raw) - len(np.unique(raw)))
        tests = 0
        for tv, n in visits["tests"]:
            m = (t >= tv) & (t < tv + 3600)
            tests += int(m.sum())
            if drop_tests:
                t = t[~m]
        self.tests, self.t = tests, t
        brk = np.nonzero(np.diff(t) >= GAP)[0] + 1
        first, last = np.r_[0, brk], np.r_[brk, len(t)] - 1
        self.E = E = len(first)
        self.t0, self.t1 = t[first], t[last]
        # a tip's time stamp is the second in which the bucket tipped: its water has fallen by the end of that second
        # ("end", the golden's reading); checks.py runs the stamp read as the second's start beside it
        e1 = 1 if stamp == "end" else 0
        a, b = (t[first] + e1 - 1) // 60, (t[last] + e1) // 60
        L = b - a + 1 + 59
        self.off = off = np.r_[0, np.cumsum(L)[:-1]]
        self.n = n = int(L.sum())
        ev = np.repeat(np.arange(E), L)
        self.ev = ev
        self.absm = np.arange(n) - off[ev] + a[ev]
        tip_ev = np.repeat(np.arange(E), last - first + 1)
        lump = np.bincount(off[tip_ev] + t // 60 - a[tip_ev], minlength=n) * bucket
        xs = np.concatenate([t[first] + e1 - 1.0, t + float(e1)])
        ys = np.concatenate([first * bucket, (np.arange(len(t)) + 1.0) * bucket])
        o = np.argsort(xs, kind="stable")
        xs, ys = xs[o], ys[o]
        if not dedupe:                       # two rows at one second: the later knot carries both
            last_of = np.r_[xs[1:] != xs[:-1], True]
            xs, ys = xs[last_of], ys[last_of]
        self.kx, self.ky, self.e1 = xs, ys, e1
        F = np.interp(np.r_[60.0 * self.absm, 60.0 * (self.absm[-1] + 1)], xs, ys)
        spread = np.diff(F)
        spread[off[1:] - 1] = 0.0            # the last empty minute of a storm never holds the next storm's first tip
        self.r = {"spread": spread, "lump": lump.astype(float), "tip": lump.astype(float)}
        # tip by tip: the rate a tip stands for is its bucket over the time since the tip before (a storm's first: a minute)
        gap = np.r_[60.0, np.maximum(np.diff(t), 0.5)].astype(float)
        gap[first] = 60.0
        self.tip_rate = bucket * 3600.0 / gap
        self.tip_ix = off[tip_ev] + t // 60 - a[tip_ev]
        self._blk = {}
        # the storage gauge account: a read holds the water since the gauge was last emptied
        reads = visits["reads"]
        self.read_t = np.array([x[0] for x in reads])
        self.check = np.array([x[1] for x in reads])
        self.nint = len(reads)
        self.iv = np.clip(np.searchsorted(self.read_t, self.t0), 0, self.nint - 1)
        if strict:                           # every storm lies inside one emptying-to-read interval
            assert np.all(self.t1 < self.read_t[self.iv])
            emp = np.array(visits["emptied"])
            assert np.all(emp[np.searchsorted(emp, self.t0) - 1] == emp[np.searchsorted(emp, self.read_t[self.iv]) - 1])
        d0 = pd.DatetimeIndex(EPOCH + self.t0.astype("timedelta64[s]"))
        self.day = d0.strftime("%Y-%m-%d").to_numpy()
        # 2.1: a storm belongs to the day, and so to the season, in which its largest 60-minute rain depth falls: the
        # day that holds the last second of the largest 60 consecutive minutes of its tips ("max"); checks.py runs the
        # day those minutes open ("open") and the day of the storm's first tip ("first") beside it
        cs = np.concatenate([np.zeros(60), np.cumsum(spread)])
        w60 = cs[60:] - cs[:-60]
        at = np.array([o + int(np.argmax(w60[o:o + l])) for o, l in zip(off, L)])
        ends = 60 * (self.absm[at] + 1) - 1
        when = {"max": ends, "open": ends - 3599, "first": self.t0, "civil": ends + 3600, "utc": ends - 3600}[season_by]
        dm = pd.DatetimeIndex(EPOCH + np.asarray(when).astype("timedelta64[s]"))
        self.year = dm.year.to_numpy()
        md = dm.month.to_numpy() * 100 + dm.day.to_numpy()
        self.inseason = (md >= SEASON[0][0] * 100 + SEASON[0][1]) & (md <= SEASON[1][0] * 100 + SEASON[1][1])
        self.seasons = int(len(np.unique(self.year)))
        # the detector's blocks, storm by storm, on the grid of the storm's own first block
        td, code, inten = det
        j = np.clip(np.searchsorted(self.t0, td) - 1, 0, E - 1)
        j2 = np.clip(j + 1, 0, E - 1)
        dist = lambda e: np.maximum(np.maximum(self.t0[e] - td, td - self.t1[e]), 0)
        e = np.where(dist(j2) < dist(j), j2, j)
        ok = dist(e) < GAP
        self.det_unmatched = int((~ok).sum())
        td, code, inten, e = td[ok], code[ok], inten[ok], e[ok]
        self.det0 = np.array(self.t0, dtype=np.int64)
        has = np.zeros(E, bool)
        first_row = np.full(E, np.iinfo(np.int64).max)
        np.minimum.at(first_row, e, td)
        has[e] = True
        self.det0[has] = first_row[has]
        k = (td - self.det0[e]) // 600
        assert np.all((td - self.det0[e]) % 600 == 0), "a detector block off its storm's ten-minute grid at %s" % code
        kp = np.clip((60 * self.absm - self.det0[ev]) // 600, 0, None)
        self.K = K = int(max(k.max(), kp.max())) + 1
        self.kp = ev * K + kp
        self.opt = np.zeros((E, K))
        self.opt[e, k] = inten / 6.0
        self.wet = np.zeros((E, K), bool)
        self.wet[e, k] = True
        self.hail10 = np.zeros((E, K), bool)
        ish = np.array([("GS" in c) or ("GR" in c) for c in code])
        self.hail10[e[ish], k[ish]] = True
        self.hail = self.hail10.any(axis=1)
        self.haildays = set(self.day[self.hail])
        self.cells = {}

    def blk(self, step):
        if step not in self._blk:
            key = self.ev.astype(np.int64) * 10 ** 9 + self.absm // step
            self._blk[step] = np.unique(key, return_inverse=True)[1]
        return self._blk[step]

    def minutes(self, k, form="recip", rd="spread", step=1):
        if rd == "tip":
            w = self.bucket * put_back(self.tip_rate, k, form, 1.0) / self.tip_rate
            return np.bincount(self.tip_ix, w, minlength=self.n)
        r = self.r[rd]
        if step == 1:
            return put_back(r, k, form)
        ix = self.blk(step)
        b = np.bincount(ix, r)
        cb = put_back(b, k, form, 60.0 / step)
        return r * np.where(b > 0, cb / np.maximum(b, 1e-12), 1.0)[ix]

    def total(self, c):
        return np.add.reduceat(c, self.off)

    def slide(self, c):
        cs = np.concatenate([np.zeros(60), np.cumsum(c)])
        return np.maximum.reduceat(cs[60:] - cs[:-60], self.off)

    def slide_sec(self, c):
        """each storm's largest depth in any 3,600 consecutive seconds, for checks.py: a minute's water (c) lies inside
        the minute as its tips' spread water does, so the running total is piecewise linear in time and its largest
        hour starts or ends on one of its knots (a tip's stamp or a minute's first second)"""
        r = self.r["spread"]
        phi = np.where(r > 0, c / np.maximum(r, 1e-300), 1.0)
        m0 = 60.0 * self.absm
        F0 = np.interp(m0, self.kx, self.ky)
        C0 = np.concatenate([[0.0], np.cumsum(c)[:-1]])
        L = np.diff(np.r_[self.off, self.n])
        a = self.absm[self.off]
        ek = np.clip(np.searchsorted(self.t0 + self.e1 - 1, self.kx, side="right") - 1, 0, self.E - 1)
        ik = self.off[ek] + np.clip(self.kx.astype(np.int64) // 60 - a[ek], 0, L[ek] - 1)
        VK = C0[ik] + phi[ik] * (self.ky - F0[ik])
        K, V, ev = np.r_[self.kx, m0], np.r_[VK, C0], np.r_[ek, self.ev]
        o = np.argsort(K, kind="stable")
        K, V, ev = K[o], V[o], ev[o]
        keep = np.r_[K[1:] != K[:-1], True]
        Ku, Vu = K[keep], V[keep]
        out = np.zeros(self.E)
        for tau in (K, K - 3600.0):
            np.maximum.at(out, ev, np.interp(tau + 3600.0, Ku, Vu) - np.interp(tau, Ku, Vu))
        return out

    def account(self, c):
        return np.bincount(self.iv, self.total(c), self.nint)

    def blocks(self, c):
        return np.bincount(self.kp, c, self.E * self.K).reshape(self.E, self.K)

    def nearest(self, times):
        """the storm a dated record of another instrument belongs to (-1: none within six hours)"""
        j = np.clip(np.searchsorted(self.t0, times) - 1, 0, self.E - 1)
        j2 = np.clip(j + 1, 0, self.E - 1)
        dist = lambda e: np.maximum(np.maximum(self.t0[e] - times, times - self.t1[e]), 0)
        e = np.where(dist(j2) < dist(j), j2, j)
        return np.where(dist(e) < GAP, e, -1)


class Pack:
    def __init__(self, target, dedupe=True, drop_tests=True, visit_clock="civil", radar_ids="both", radar_clock="utc",
                 hail_by="storm", season_by="max", stamp="end", slide_by="minute"):
        """the keyword switches are the natural mishandlings of the files' texture, for checks.py; the defaults are
        the golden's reading"""
        self.target, self.slide_by = target, slide_by
        strict = dedupe and drop_tests and visit_clock == "civil"
        naive = lambda a, b: int((dt.datetime.strptime(a + " " + b, "%Y-%m-%d %H:%M") - dt.datetime(2009, 1, 1)).total_seconds())
        clock = civil if visit_clock == "civil" else naive
        rshift = 3600 if radar_clock == "utc" else 0
        wb = load_workbook(os.path.join(target, FILES["stations"]), read_only=True, data_only=True)
        rows = list(wb["Stations"].iter_rows(values_only=True))
        hd = rows[0]
        reg = [dict(zip(hd, r)) for r in rows[1:] if r[0]]
        wb = load_workbook(os.path.join(target, FILES["crossings"]), read_only=True, data_only=True)
        rows = list(wb["Crossings"].iter_rows(values_only=True))
        cr = [dict(zip(rows[0], r)) for r in rows[1:] if r[0]]
        rows = list(wb["Source areas"].iter_rows(values_only=True))
        sa = {r[0]: dict(zip(rows[0], r)) for r in rows[1:] if r[0]}
        vb = pd.read_csv(os.path.join(target, FILES["visits"]), dtype=str, keep_default_na=False)
        con = sqlite3.connect(os.path.join(target, FILES["pw"]))
        pw = pd.read_sql_query("SELECT station, block_start, wx, intensity_mm_h FROM pw_block", con)
        con.close()
        self.S, self.by_name = {}, {}
        for g in reg:
            code = g["station"]
            tips = pd.read_csv(os.path.join(target, FILES["tips"] % code), dtype=str)
            assert tips["tip_time"].str.endswith("+01:00").all() and (tips["tip_mm"].astype(float) == float(g["bucket_mm"])).all()
            v = vb[vb["station"] == code]
            vt = np.array([clock(a, b) for a, b in zip(v["visit_date"], v["visit_time_local"])])
            o = np.argsort(vt, kind="stable")
            v, vt = v.iloc[o], vt[o]
            visits = dict(reads=[(int(t), float(x)) for t, x in zip(vt, v["storage_gauge_mm"]) if x != ""],
                          emptied=[int(t) for t, x in zip(vt, v["storage_emptied"]) if x in ("yes", "set empty")],
                          tests=[(int(t), int(x)) for t, x in zip(vt, v["tip_test_tips"]) if x != ""])
            d = pw[pw["station"] == code]
            det = (secs(d["block_start"].tolist()), d["wx"].to_numpy(), d["intensity_mm_h"].to_numpy(dtype=float))
            o = np.argsort(det[0], kind="stable")
            st = Station(code, g["name"], float(g["bucket_mm"]), g["rain_gauge"], (g["x_etrs89_utm33n_m"], g["y_etrs89_utm33n_m"]),
                         secs(tips["tip_time"].tolist()), visits, tuple(x[o] for x in det), dedupe, drop_tests, strict,
                         season_by, stamp)
            st.rows = len(tips)
            if hail_by == "day":             # every storm of a day on which the detector coded hail or graupel
                st.hail = np.array([d in st.haildays for d in st.day]) & (st.opt.sum(axis=1) > 0)
            self.S[code] = st
        self.codes = list(self.S)
        # the members: the register's crossings, and the research valley's gauges on the station they stand above
        self.M, self.crossings, self.research = {}, [], []
        for c in cr:
            a = sa[c["source_area"]]
            self.M[c["gully"]] = dict(station=c["governing_station"], xy=(a["x_etrs89_utm33n_m"], a["y_etrs89_utm33n_m"]),
                                      T=float(a["triggering_depth_point_mm_60min"]), id=c["crossing"], km=c["road_km"])
            self.crossings.append(c["gully"])
        gz = pd.read_csv(os.path.join(target, FILES["rs_gauges"]))
        for _, g in gz.iterrows():
            xy = (float(g["x_etrs89_utm33n_m"]), float(g["y_etrs89_utm33n_m"]))
            near = min(self.codes, key=lambda c: math.hypot(self.S[c].xy[0] - xy[0], self.S[c].xy[1] - xy[1]))
            self.M[g["gauge"]] = dict(station=near, xy=xy, T=float(g["triggering_depth_point_mm_60min"]))
            self.research.append(g["gauge"])
        self.valley = self.M[self.research[0]]["station"]
        assert all(self.M[g]["station"] == self.valley for g in self.research)
        # the rainfall normal: each point's cell against its station's
        nm = pd.read_csv(os.path.join(target, FILES["normal"]))
        cell = {(int(x), int(y)): float(v) for x, y, v in nm.itertuples(index=False)}
        at = lambda xy: cell[(int(xy[0] // 500) * 500 + 250, int(xy[1] // 500) * 500 + 250)]
        self.normal = {c: at(s.xy) for c, s in self.S.items()}
        for m in self.M.values():
            m["normal"] = at(m["xy"])
            m["map"] = m["normal"] / self.normal[m["station"]]
        # the radar: every cell's 60-minute maximum on the station's pixel and on each member's pixel
        px = pd.read_csv(os.path.join(target, FILES["pixels"]))
        cx, cy = px.iloc[:, 2].to_numpy(), px.iloc[:, 3].to_numpy()
        ident = {}
        for a, b, x, y in px.itertuples(index=False):
            ident[int(a)] = (int(x), int(y))
            if radar_ids == "both":
                ident[int(b)] = (int(x), int(y))
        near = lambda xy: (int(xy[0] // 1000) * 1000 + 500, int(xy[1] // 1000) * 1000 + 500)
        assert all(near(s.xy) in set(zip(cx, cy)) for s in self.S.values())
        rd = pd.read_csv(os.path.join(target, FILES["radar"]))
        rd = rd[[int(p) in ident for p in rd["pixel"]]].copy()
        rd["xy"] = [ident[int(p)] for p in rd["pixel"]]
        self.radar_rows = len(rd)
        for c, s in self.S.items():
            own = rd[rd["xy"] == near(s.xy)].drop_duplicates("cell_id").set_index("cell_id")
            s.cell_t0 = secs([x.replace(" ", "T") + ":00" for x in own["first_scan_utc"]]) + rshift
            s.cell0 = own["p60_max_mm"].to_numpy(dtype=float)
            s.cell_year = np.array([int(x[:4]) for x in own["first_scan_utc"]])
            s.cell_ev = s.nearest(s.cell_t0)
            for name, m in self.M.items():
                if m["station"] != c:
                    continue
                pt = rd[rd["xy"] == near(m["xy"])].drop_duplicates("cell_id").set_index("cell_id")["p60_max_mm"]
                s.cells[name] = pt.reindex(own.index).to_numpy(dtype=float)
                assert np.isfinite(s.cells[name]).all()
        # the research valley's weighing gauges, event by event, on the valley station's storms
        ev = pd.read_csv(os.path.join(target, FILES["rs_events"]))
        s = self.S[self.valley]
        self.weigh, self.weigh_ev = {}, {}
        for g in self.research:
            e = ev[ev["gauge"] == g]
            self.weigh[g] = e["p60_max_mm"].to_numpy(dtype=float)
            self.weigh_ev[g] = s.nearest(secs([x.replace(" ", "T") + ":00" for x in e["event_start_utc"]]) + 3600)
        self.weigh_years = sorted({int(x[:4]) for x in ev["event_start_utc"]})
        self.radar_years = sorted({int(x[:4]) for x in rd["first_scan_utc"]})
        self._kap, self._xs = {}, {}

    # ------------------------------------------------------------------------------------------ the bucket's loss
    def fit(self, group, form, rd, step):
        ws = [self.S[c] for c in group]
        acc = lambda k: [w.account(w.minutes(k, form, rd, step)) for w in ws]
        if form in ("scaled", "power"):
            def scale(k):
                a = acc((1.0, k))
                return sum(float((w.check * x).sum()) for w, x in zip(ws, a)) / sum(float((x * x).sum()) for x in a)
            sse = lambda k: sum(float(((w.check - x) ** 2).sum()) for w, x in zip(ws, acc((scale(k), k))))
        else:
            sse = lambda k: sum(float(((w.check - x) ** 2).sum()) for w, x in zip(ws, acc(k)))
        lo, hi = (1.0, 1.4) if form == "power" else (0.0, K_LIMIT)
        g = (math.sqrt(5.0) - 1.0) / 2.0
        a, b = hi - g * (hi - lo), lo + g * (hi - lo)
        fa, fb = sse(a), sse(b)
        for _ in range(44):
            if fa < fb:
                hi, b, fb = b, a, fa
                a = hi - g * (hi - lo)
                fa = sse(a)
            else:
                lo, a, fa = a, b, fb
                b = lo + g * (hi - lo)
                fb = sse(b)
        k = 0.5 * (lo + hi)
        return (scale(k), k) if form in ("scaled", "power") else k

    def kappas(self, form="recip", pool="model", rd="spread", step=1):
        key = (form, pool, rd, step)
        if key not in self._kap:
            out = {}
            for mdl in sorted({s.model for s in self.S.values()}):
                grp = [c for c in self.codes if self.S[c].model == mdl]
                if pool == "gauge":
                    out.update({c: self.fit([c], form, rd, step) for c in grp})
                else:
                    k = self.fit(grp, form, rd, step)
                    out.update({c: k for c in grp})
            self._kap[key] = out
        return self._kap[key]

    def factor(self, c, rd="spread"):
        s = self.S[c]
        return float(s.check.sum() / s.account(s.r[rd]).sum())

    def base(self, c, s1, k=0.0, form="recip", rd="spread", step=1):
        s = self.S[c]
        if s1 == "rate":
            return s.minutes(k, form, rd, step)
        if s1 == "factor":
            return s.r[rd] * self.factor(c, rd)
        return s.r[rd]

    # --------------------------------------------------------------------------------------------- the hail storms
    def storm_max(self, c, mins, s3, carried=None):
        s = self.S[c]
        x = s.slide(mins) if self.slide_by == "minute" else s.slide_sec(mins)
        if s3 == "tips":
            return x
        h = s.hail
        if s3 == "carried":
            return np.where(h, x * carried, x)
        tot = s.total(mins)
        opt = s.opt
        if s3 in ("optical", "weighted"):
            cr = float(tot[~h].sum() / opt[~h].sum())
        if s3 == "optical":
            return np.where(h, six(cr * opt), x)
        if s3 == "weighted":
            wh = float((tot[h].sum() - cr * (opt[h] * ~s.hail10[h]).sum()) / (cr * (opt[h] * s.hail10[h]).sum()))
            opt = opt * np.where(s.hail10, wh, 1.0)
        if s3 in ("profile", "weighted"):
            b = tot[:, None] * opt / np.maximum(opt.sum(axis=1, keepdims=True), 1e-12)
        elif s3 == "onset":
            c10 = s.blocks(mins)
            first = np.where(h, s.hail10.argmax(axis=1), 0)
            pre = np.arange(s.K)[None, :] < first[:, None]
            rest = opt * ~pre
            b = c10 * pre + (tot - (c10 * pre).sum(axis=1))[:, None] * rest / np.maximum(rest.sum(axis=1, keepdims=True), 1e-12)
        elif s3 == "even":
            b = tot[:, None] * s.wet / np.maximum(s.wet.sum(axis=1, keepdims=True), 1)
        elif s3 == "hailonly":               # every drop of a hail storm laid on its hail-coded blocks, by their intensity
            key = opt * s.hail10
            b = tot[:, None] * key / np.maximum(key.sum(axis=1, keepdims=True), 1e-12)
        else:
            c10 = s.blocks(mins)
            dry = ~s.wet
            key = opt * s.hail10
            b = c10 * ~dry + (c10 * dry).sum(axis=1, keepdims=True) * key / np.maximum(key.sum(axis=1, keepdims=True), 1e-12)
        return np.where(h, six(b), x)

    def research_reads(self, k, rd="spread"):
        """the valley's weighing gauges read as a calibration of the bucket: one ratio of source to bucket over every
        storm they recorded, and one multiplier for the storms with hail"""
        s = self.S[self.valley]
        src, n = np.zeros(s.E), np.zeros(s.E)
        for g in self.research:
            ok = self.weigh_ev[g] >= 0
            np.add.at(src, self.weigh_ev[g][ok], self.weigh[g][ok])
            np.add.at(n, self.weigh_ev[g][ok], 1.0)
        m = n > 0
        src = src / len(self.research)
        raw, cor = s.slide(s.r[rd]), s.slide(s.minutes(k, "recip", rd, 1))
        h, r = m & s.hail, m & ~s.hail
        return float(src[m].sum() / raw[m].sum()), float((src[h].sum() / cor[h].sum()) / (src[r].sum() / cor[r].sum()))

    def station_maxima(self, s1="rate", s3="profile", form="recip", pool="model", rd="spread", step=1):
        key = (s1, s3, form, pool, rd, step)
        if key not in self._xs:
            kap = self.kappas(form, pool, rd, step) if s1 == "rate" else {c: 0.0 for c in self.codes}
            carried = self.research_reads(self.kappas()[self.valley])[1] if s3 == "carried" else None
            self._xs[key] = ({c: self.storm_max(c, self.base(c, s1, kap[c], form, rd, step), s3, carried) for c in self.codes}, kap)
        return self._xs[key]

    # ------------------------------------------------------------------------------------------- the source areas
    def site_factor(self, name, how="geo"):
        s = self.S[self.M[name]["station"]]
        a, b = s.cells[name], s.cell0
        if how == "q90":
            return float(np.quantile(a, 0.9) / np.quantile(b, 0.9))
        if how == "slope":
            return float((a * b).sum() / (b * b).sum())
        if how == "top":
            m = b >= np.quantile(b, 0.75)
            return float(a[m].sum() / b[m].sum())
        if how == "upper":
            g = np.sqrt(a * b)
            m = (g >= np.quantile(g, 0.75)) & (a > 0) & (b > 0)
            return float(np.exp(np.log(a[m] / b[m]).mean()))
        ok = (b >= 3.0) if how == "gauge3" else ((a >= 3.0) & (b >= 3.0)) if how == "geo3" else (a >= 1.0) & (b >= 1.0)
        a, b = a[ok & (a > 0)], b[ok & (a > 0)]
        lr = np.log(a / b)
        if how in ("geo", "geo3", "gauge3", "pairs"):
            return float(np.exp(lr.mean()))
        if how == "median":
            return float(np.exp(np.median(lr)))
        if how == "sums":
            return float(a.sum() / b.sum())
        q = np.sort(lr)
        k = int(0.1 * len(q))
        return float(np.exp(q[k:len(q) - k].mean()))

    def transfer(self, name, x, s2, power=1.0):
        m = self.M[name]
        if s2 == "map":
            return m["map"] * x
        if s2 == "one":
            return x
        if s2 == "qq":
            s = self.S[m["station"]]
            return rank_carry(x, s.cells[name], s.cell0)
        f = self.site_factor(name, s2) ** power
        if s2 != "pairs":
            return f * x
        s = self.S[m["station"]]
        a, b = np.zeros(s.E), np.zeros(s.E)
        ok = s.cell_ev >= 0
        a[s.cell_ev[ok]], b[s.cell_ev[ok]] = s.cells[name][ok], s.cell0[ok]
        use = (a >= 1.0) & (b >= 1.0)
        return np.where(use, x * a / np.maximum(b, 1e-9), x * f)

    def keep(self, name, recent=None):
        s = self.S[self.M[name]["station"]]
        return s.inseason & ((s.year >= recent) if recent else True)

    def estimate(self, s1="rate", s2="geo", s3="profile", form="recip", pool="model", rd="spread", step=1,
                 members=None, recent=None, xs=None, power=1.0):
        if xs is None:
            xs, kap = self.station_maxima(s1, s3, form, pool, rd, step)
        out, even, upper = Rates(), {}, {}
        for name in (members or self.crossings):
            m = self.M[name]
            s = self.S[m["station"]]
            est = self.transfer(name, xs[m["station"]], s2, power)[self.keep(name, recent)]
            n = (max(s.year) - recent + 1) if recent else s.seasons
            out[name] = float((est >= m["T"]).sum()) / n
            even[name], upper[name] = at_line(est, n), upper_mean(est, n)
        out.even, out.upper = even, upper
        return out

    def at_stations(self, fn, at=12.0):
        """a radar-depth route set on each station's own pixel: the storms of `at` mm it files there beside those the
        station's own depths hold in the same cells, and the radar's scatter about the station's depth on logs"""
        xs = self.station_maxima()[0]
        out = {}
        for c, s in self.S.items():
            ok = s.cell_ev >= 0
            x, r = xs[c][s.cell_ev[ok]], s.cell0[ok]
            big = (x >= 3.0) & (r > 0)
            out[s.name] = dict(route=int((fn(r) >= at).sum()), station=int((x >= at).sum()),
                               scatter=float(np.std(np.log(r[big] / x[big]))))
        return out

    def radar_route(self, members=None, recent=None):
        """the standard radar product: one field bias against the gauges' account-closed storm maxima, then the
        source pixel counted against the triggering depth"""
        num = den = 0.0
        for c, s in self.S.items():
            x = s.slide(self.base(c, "factor"))
            ok = s.cell_ev >= 0
            num += float(x[s.cell_ev[ok]].sum())
            den += float(s.cell0[ok].sum())
        bias = num / den
        n = len(self.radar_years)
        out, even, upper = Rates(), {}, {}
        for name in (members or self.crossings):
            v = bias * self.S[self.M[name]["station"]].cells[name]
            out[name] = float((v >= self.M[name]["T"]).sum()) / n
            even[name], upper[name] = at_line(v, n), upper_mean(v, n)
        out.even, out.upper, out.bias = even, upper, bias
        out.station = self.at_stations(lambda r: bias * r)
        return out

    def mapped_route(self, members=None):
        """the radar's own depths as a route: the cells' depths on the weighing gauges' pixels matched rank for rank,
        largest first, with what the gauges recorded in the same seasons; the map applied to the cells' depths on each
        member's pixel and counted against its triggering depth over the radar's seasons. `.station` sets the same map
        on each station's own pixel against the station's depths in the same cells."""
        v = self.S[self.valley]
        r = np.sort(np.concatenate([v.cells[g] for g in self.research]))[::-1]
        g = np.sort(np.concatenate([self.weigh[g] for g in self.research]))[::-1]
        k = min(len(r), len(g))
        r, g = r[:k][::-1], g[:k][::-1]
        fmap = lambda x: np.where(x > r[-1], x * g[-1] / r[-1], np.where(x < r[0], x * g[0] / r[0], np.interp(x, r, g)))
        n = len(self.radar_years)
        out, even, upper = Rates(), {}, {}
        for name in (members or self.crossings):
            y = fmap(self.S[self.M[name]["station"]].cells[name])
            out[name] = float((y >= self.M[name]["T"]).sum()) / n
            even[name], upper[name] = at_line(y, n), upper_mean(y, n)
        out.even, out.upper, out.station = even, upper, self.at_stations(fmap)
        return out

    def carried_route(self):
        c = self.research_reads(0.0)[0]
        out = Rates()
        for name in self.crossings:
            m = self.M[name]
            s = self.S[m["station"]]
            out[name] = float((c * s.slide(s.r["spread"])[self.keep(name)] >= m["T"]).sum()) / s.seasons
        return out

    def seen(self, g):
        n = len(self.weigh_years)
        v = self.weigh[g]
        return float((v >= self.M[g]["T"]).sum()), at_line(v, n), upper_mean(v, n)


def classes(v, names):
    return {s: 1 + int(v[s] >= LINES[0]) + int(v[s] >= LINES[1]) for s in names}


def run(target, quiet=True):
    P = Pack(target)
    names = sorted(P.crossings)
    gold = P.estimate()
    kap = P.kappas()
    ways = [(fo, po, rd, st, a, b) for fo, rd, st in LOSS_READS for po in POOL_WAYS for a in SITE_WAYS for b in HAIL_WAYS]
    fam = [P.estimate("rate", a, b, fo, po, rd, st) for fo, po, rd, st, a, b in ways]

    def route(lost):
        return P.estimate("factor" if "S1" in lost else "rate", "map" if "S2" in lost else "geo",
                          "tips" if "S3" in lost else "profile")
    keys = [("S1",), ("S2",), ("S3",), ("S1", "S2"), ("S1", "S3"), ("S2", "S3"), ("S1", "S2", "S3")]
    lat = {"+".join(k): route(k) for k in keys}
    direct = P.estimate("raw", "one", "tips")
    rad = P.radar_route()
    mapped = P.mapped_route()
    car = P.carried_route()
    crude = {"hail " + b: P.estimate(s3=b) for b in CRUDE_HAIL}
    crude.update({"site " + a: P.estimate(s2=a) for a in CRUDE_SITE})
    crude.update({"loss on %d-minute totals" % st: P.estimate(step=st) for st in (10, 15)})
    crude["loss first-order"] = P.estimate(form="lin")
    crude["loss as a power law"] = P.estimate(form="power")
    # every refused way of the loss, crossed with every other way of the battery
    crude_all = {label: [P.estimate("rate", a, b, fo, po, rd, st) for fo, rd, st in sel for po in POOL_WAYS
                         for a in SITE_WAYS for b in HAIL_WAYS] for label, sel in REFUSED.items()}

    code = {s.name: c for c, s in P.S.items()}
    vfo, csr, prd = code["Valfosca"], code["Costarossa"], code["Pradalt"]
    loss_ways = [(fo, po, rd, st) for fo, rd, st in LOSS_READS for po in POOL_WAYS]
    more = {"site": [P.estimate("rate", a, b, fo, po, rd, st) for fo, po, rd, st in loss_ways for a in MORE_SITE
                     for b in HAIL_WAYS + MORE_HAIL],
            # crossed with the battery and with the other carried way, the first-order form of the loss
            "hail": [P.estimate("rate", a, b, fo, po, rd, st)
                     for fo, po, rd, st in loss_ways + [(fo, po, rd, st) for fo, rd, st in REFUSED[CARRIED] for po in POOL_WAYS]
                     for a in SITE_WAYS for b in MORE_HAIL]}
    c1 = {"g": under_read(kap[vfo]), "lost": 100.0 * (1.0 - 1.0 / P.factor(vfo)),
          "fam": [under_read(P.kappas(fo, po, rd, st)[vfo], fo) for fo, po, rd, st in loss_ways],
          "wide": [under_read(P.kappas(fo, po, rd, st)[vfo], fo) for fo, rd, st in REFUSED["first-order form"] for po in POOL_WAYS]}
    c2 = {"g": P.site_factor("Rio Marden"), "lost": P.M["Rio Marden"]["map"],
          "fam": [P.site_factor("Rio Marden", a) for a in SITE_WAYS]}

    def hail_gap(c, s3="profile", form="recip", pool="model", rd="spread", step=1):
        s = P.S[c]
        a = P.station_maxima("rate", "tips", form, pool, rd, step)[0][c][s.hail & s.inseason]
        b = P.station_maxima("rate", s3, form, pool, rd, step)[0][c][s.hail & s.inseason]
        return 100.0 * (1.0 - float(a.sum()) / float(b.sum()))
    for c in P.codes:
        P.S[c].gap = hail_gap(c)
    c3 = {"g": hail_gap(csr), "lost": 0.0,
          "fam": [hail_gap(csr, b, fo, po, rd, st) for fo, po, rd, st in loss_ways for b in HAIL_WAYS],
          "wide": [hail_gap(csr, b, fo, po, rd, st) for fo, rd, st in REFUSED["first-order form"] for po in POOL_WAYS for b in HAIL_WAYS],
          "more": [hail_gap(csr, b, fo, po, rd, st)
                   for fo, po, rd, st in loss_ways + [(fo, po, rd, st) for fo, rd, st in REFUSED[CARRIED] for po in POOL_WAYS]
                   for b in MORE_HAIL]}

    # the referee: the research valley's weighing gauges
    y0 = P.weigh_years[0]
    R = P.research
    rv = lambda **kw: P.estimate(members=R, recent=y0, **kw)
    ns = len(P.weigh_years)
    rtop = lambda v: float(np.mean([v.upper[g] for g in R]))
    rdepth = lambda v: float(np.mean([v.even[g] for g in R]))
    rcount = lambda v: float(sum(v[g] for g in R)) * ns
    rivals = {"bucket put back by one factor": rv(s1="factor"), "source scaled by the rainfall normal": rv(s2="map"),
              "tips taken as rain on hail days": rv(s3="tips"), "the gauge read raw": rv(s1="raw", s2="one", s3="tips")}
    others = {"hail water moved only from the dry intervals": rv(s3="dry"), "hail water spread evenly": rv(s3="even"),
              "the detector's own amounts on hail storms": rv(s3="optical"), "each storm by its own pixel pair": rv(s2="pairs"),
              "one hail-day multiplier from the valley": rv(s3="carried"), "the rate read on five-minute totals": rv(step=5),
              "tips counted in their own minute": rv(rd="lump"), "the rate read tip by tip": rv(rd="tip"),
              "the rate read on three-minute totals": rv(step=3),
              "the pixels' upper deciles": rv(s2="q90"), "the source pixel regressed on the gauge's": rv(s2="slope"),
              "hail water laid on the hail-coded blocks alone": rv(s3="hailonly"),
              "the two pixels matched rank for rank": rv(s2="qq"), "the radar product": P.radar_route(members=R),
              "the radar mapped on these same gauges": P.mapped_route(members=R)}
    rgold = rv()
    sn = [P.seen(g) for g in R]
    referee = dict(seen_count=sum(x[0] for x in sn), seen_depth=float(np.mean([x[1] for x in sn])),
                   seen_top=float(np.mean([x[2] for x in sn])),
                   golden=(rtop(rgold), rdepth(rgold), rcount(rgold)),
                   rivals={k: (rtop(v), rdepth(v), rcount(v)) for k, v in rivals.items()},
                   others={k: (rtop(v), rdepth(v), rcount(v)) for k, v in others.items()}, seasons=ns)

    # what the files say against each shortcut
    st = {}
    for c, s in P.S.items():
        raw = s.r["spread"]
        acc0, fac = s.account(raw), P.factor(c)
        x = np.bincount(s.iv, np.add.reduceat(60.0 * raw ** 2, s.off), s.nint)
        rf, rg = s.check - fac * acc0, s.check - s.account(s.minutes(kap[c]))
        r = float(np.corrcoef(x, rf)[0, 1])
        mins = s.minutes(kap[c])
        c10 = s.blocks(mins)
        late = lambda m: 100.0 * float((c10[m] * ~s.wet[m]).sum() / c10[m].sum())
        storm = s.inseason & (s.slide(mins) >= 0.0)
        rain = ~s.hail & (s.opt.sum(axis=1) > 0)
        lsd = float(np.log(s.opt.sum(axis=1)[rain] / s.total(raw)[rain]).std())
        st[c] = dict(name=s.name, rows=s.rows, resent=s.resent, tests=s.tests, tips=int(len(s.t)), events=int(s.E),
                     hail=int((s.hail & s.inseason).sum()), factor=fac, resid_factor=float(np.sqrt((rf ** 2).mean())),
                     resid_rate=float(np.sqrt((rg ** 2).mean())), resid_r=r, late_hail=late(s.hail), late_rain=late(~s.hail),
                     optical_log_sd=lsd, intervals=int(s.nint), seasons=s.seasons, det_unmatched=s.det_unmatched,
                     storage=float(s.check.sum()), tipped=float(acc0.sum()), in_season=int(storm.sum()),
                     hail_gap=s.gap, kappa=kap[c], gaps_3_to_6h=int(((np.diff(s.t) >= 3 * 3600) & (np.diff(s.t) < GAP)).sum()),
                     gaps_6_to_8h=int(((np.diff(s.t) >= GAP) & (np.diff(s.t) < 8 * 3600)).sum()))
    # the account's residual under every way of the loss, by bucket size (mm rms over the visit intervals)
    def left(fo, po, rd, sp):
        k = P.kappas(fo, po, rd, sp)
        res = {}
        for c in P.codes:
            res.setdefault(P.S[c].bucket, []).append(P.S[c].check - P.S[c].account(P.S[c].minutes(k[c], fo, rd, sp)))
        return {b: float(np.sqrt(np.mean(np.concatenate(r) ** 2))) for b, r in res.items()}
    acct = {("kept", fo, po, rd, sp): left(fo, po, rd, sp) for fo, po, rd, sp in loss_ways}
    for label, sel in REFUSED.items():
        for fo, rd, sp in sel:
            for po in POOL_WAYS:
                acct[(label, fo, po, rd, sp)] = left(fo, po, rd, sp)
    small = min(P.S[c].bucket for c in P.codes)
    span = lambda label: {b: [min(v[b] for k, v in acct.items() if k[0] == label), max(v[b] for k, v in acct.items() if k[0] == label)]
                          for b in sorted({P.S[c].bucket for c in P.codes})}
    same = lambda label, fo, po, rd, sp: acct[(label, fo, po, rd, sp)][small] / acct[("kept", "recip", po, rd, sp)][small]
    pair = {"first-order form": [same("first-order form", "lin", po, rd, sp) for _, rd, sp in REFUSED["first-order form"] for po in POOL_WAYS],
            "power law": [same("power law", "power", po, rd, sp) for _, rd, sp in REFUSED["power law"] for po in POOL_WAYS]}
    one = acct[("kept", "recip", "model", "spread", 1)]
    for label in ("10-minute totals", "15-minute totals"):
        pair[label] = [v[small] / one[small] for k, v in acct.items() if k[0] == label]
    steps = dict(kept=span("kept"), refused={label: span(label) for label in REFUSED}, small=small, golden=one,
                 ratio={label: [min(v), max(v)] for label, v in pair.items()},
                 # the cut on the account: what every way used or held in the bands leaves, and every way refused
                 held_max=max(v[small] for k, v in acct.items() if k[0] in ("kept", CARRIED)),
                 refused_min=min(v[small] for k, v in acct.items() if k[0] not in ("kept", CARRIED)),
                 power=[P.kappas("power", po, rd, sp)[c][1] for _, rd, sp in REFUSED["power law"] for po in POOL_WAYS
                        for c in P.codes])
    site = {}
    for name in names + R:
        s = P.S[P.M[name]["station"]]
        a, b = s.cells[name], s.cell0
        yr = np.array([int(str(EPOCH + np.timedelta64(int(t), "s"))[:4]) for t in s.cell_t0])
        odd, evn = yr % 2 == 1, yr % 2 == 0
        q = lambda m: float(np.quantile(a[m], 0.9) / np.quantile(b[m], 0.9))
        ok = (a >= 1.0) & (b >= 1.0)
        g = lambda m: float(np.exp(np.log(a[m & ok] / b[m & ok]).mean()))
        tb, ta = b >= np.quantile(b, 0.75), a >= np.quantile(a, 0.75)
        halves = {}
        if name in names:                    # each relation made on the odd and on the even seasons of the radar alone
            x = P.station_maxima()[0][P.M[name]["station"]]
            for how in ("qq", "pairs"):
                got = []
                for m in (odd, evn):
                    est = (rank_carry(x, a[m], b[m]) if how == "qq" else x * g(m))[P.keep(name)]
                    got.append((float((est >= P.M[name]["T"]).sum()) / s.seasons, at_line(est, s.seasons)))
                halves[how] = (abs(got[0][0] - got[1][0]), abs(got[0][1] - got[1][1]))
        site[name] = dict(factor=P.site_factor(name), map=P.M[name]["map"], pairs=int(ok.sum()), cells=int(len(a)),
                          q90_halves=100.0 * abs(q(odd) / q(evn) - 1.0), geo_halves=100.0 * abs(g(odd) / g(evn) - 1.0),
                          slope=float((a * b).sum() / (b * b).sum()), slope_rev=float((a * a).sum() / (a * b).sum()),
                          top=float(a[tb].sum() / b[tb].sum()), top_rev=float(a[ta].sum() / b[ta].sum()),
                          halves=halves, ways={w: P.site_factor(name, w) for w in SITE_WAYS + CRUDE_SITE if w != "qq"})
    sv = P.S[P.valley]
    gx = P.station_maxima()[0][P.valley]
    for g in R:
        ok = P.weigh_ev[g] >= 0
        site[g]["weighed_over_station"] = float(P.weigh[g][ok].sum() / gx[P.weigh_ev[g][ok]].sum())
    # forcing: each fitted input moved by a fifth
    moved = {}
    for fk in (0.8, 1.2):
        xs = {c: P.storm_max(c, P.S[c].minutes(fk * kap[c]), "profile") for c in P.codes}
        moved["the fitted loss times %.1f" % fk] = P.estimate(xs=xs)
    for pw in (0.8, 1.2):
        moved["each burst factor's distance from one times %.1f" % pw] = P.estimate(power=pw)
    for lam in (0.8, 1.2):
        xa, xb = P.station_maxima("rate", "tips")[0], P.station_maxima()[0]
        moved["the hail storms' put-back times %.1f" % lam] = P.estimate(xs={c: xa[c] + lam * (xb[c] - xa[c]) for c in P.codes})
    # a second implementation's readings of a tip's stamp and of the sliding hour, on the golden's own route
    conv = {label: Pack(target, **kw) for label, kw in (
        ("a tip's stamp read as the start of its second", dict(stamp="start")),
        ("the 60 minutes slid by the second", dict(slide_by="second")),
        ("both", dict(stamp="start", slide_by="second")))}
    out = dict(P=P, names=names, gold=gold, kap=kap, ways=ways, fam=fam, lat=lat, direct=direct, radar=rad, mapped=mapped, more=more, carried=car,
               conv=conv,
               crude=crude, crude_all=crude_all, acct=acct, c1=c1, c2=c2, c3=c3, referee=referee, rgold=rgold, stations=st, steps=steps, site=site,
               moved=moved, classes=classes(gold, names), reads=P.research_reads(kap[P.valley]),
               reads_raw=P.research_reads(0.0), code=code, loss_ways=loss_ways)
    if not quiet:
        report(out)
    return out


def report(A):
    P, names = A["P"], A["names"]
    p = lambda label, v: print("%-34s" % label + ", ".join("%s %.2f" % (s.replace("Rio ", ""), v[s]) for s in names))
    pe = lambda label, v: print("%-34s" % label + ", ".join("%s %.1f" % (s.replace("Rio ", ""), v.even[s]) for s in names))
    print("loss per unit of rate: " + ", ".join("%s %.5f" % (c, k) for c, k in A["kap"].items()))
    for c, s in A["stations"].items():
        print("  %s rows %d re-sent %d tests %d events %d hail %d factor %.3f resid factor %.2f (r %.2f) rate %.2f late hail %.1f rain %.2f optical sd %.2f unmatched det %d" % (
            c, s["rows"], s["resent"], s["tests"], s["events"], s["hail"], s["factor"], s["resid_factor"], s["resid_r"],
            s["resid_rate"], s["late_hail"], s["late_rain"], s["optical_log_sd"], s["det_unmatched"]))
    print("account, kept ways:", A["steps"]["kept"], "ratios", A["steps"]["ratio"])
    for k, v in A["steps"]["refused"].items():
        print("account, refused %-18s" % k, v, "classes hold", all(classes(x, names) == A["classes"] for x in A["crude_all"][k]))
    p("golden", A["gold"])
    fam = A["fam"]
    print("%-34s" % "family" + ", ".join("%s %.2f-%.2f" % (s.replace("Rio ", ""), min(v[s] for v in fam), max(v[s] for v in fam)) for s in names))
    for k, v in A["lat"].items():
        p(k + " lost", v)
    p("direct", A["direct"])
    p("radar", A["radar"])
    p("carried", A["carried"])
    for k, v in A["crude"].items():
        p(k, v)
    pe("depth golden", A["gold"])
    print("%-34s" % "depth family" + ", ".join("%s %.1f-%.1f" % (s.replace("Rio ", ""), min(v.even[s] for v in fam), max(v.even[s] for v in fam)) for s in names))
    for k in ("S1", "S2", "S3"):
        pe("depth %s lost" % k, A["lat"][k])
    for nm in ("c1", "c2", "c3"):
        c = A[nm]
        print("%s golden %.3f lost %.3f family %.3f to %.3f" % (nm, c["g"], c["lost"], min(c["fam"]), max(c["fam"])))
    print("site:", {k: (round(v["factor"], 3), round(v["map"], 3), v["pairs"]) for k, v in A["site"].items()})
    r = A["referee"]
    print("referee: seen %.2f, %.2f, %.0f; golden %.2f, %.2f, %.0f" % ((r["seen_top"], r["seen_depth"], r["seen_count"]) + r["golden"]))
    for k, v in {**r["rivals"], **r["others"]}.items():
        print("   %-46s %.2f, %.2f and %.0f" % ((k,) + v))
    print("research reads: source over bucket %.3f (raw), hail-day multiplier %.3f" % (A["reads_raw"][0], A["reads"][1]))
    cl = A["classes"]
    for k, v in A["moved"].items():
        print("forcing, %-48s %s; %s" % (k, ", ".join("%s %.2f" % (s.replace("Rio ", ""), v[s]) for s in names),
                                         "unchanged" if classes(v, names) == cl else "MOVED"))
    bad = [w for w, v in zip(A["ways"], fam) if classes(v, names) != cl]
    print("battery: %d variants, %d off the golden classing" % (len(fam), len(bad)), bad[:5])
    print("classes:", cl)


if __name__ == "__main__":
    import sys
    import time
    t = time.time()
    run(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "target"), quiet=False)
    print("%.0f s" % (time.time() - t))
