"""An independent rebuild of the golden from the bundle alone, written a second way: it shares no code with
analysis.py, reads only target/ and the regulation's constants, and works tip by tip in continuous time where the
golden works on a minute line (the loss on the rate between tips, every 60-minute window anchored on a tip, each
detector block given to the storm whose tips lie nearest). It must file the same seven classes and land every stated
figure inside the band the answer blocks give.

    python3 task3/generator/verify.py [target]
"""
import datetime as dt
import json
import math
import os
import sqlite3
import sys
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd
from openpyxl import load_workbook

HERE = os.path.dirname(os.path.abspath(__file__))
T0 = np.datetime64("2009-01-01T00:00:00")
HOUR = 3600
GAP_H, WINDOW_S, LINES, TIMES = 6, 3600, (1.0, 3.0), 5          # regulation 2.2, 2.3, 4.1, 3.2
ROME = ZoneInfo("Europe/Rome")


def sheet(path, name):
    rows = list(load_workbook(path, read_only=True, data_only=True)[name].iter_rows(values_only=True))
    return [dict(zip(rows[0], r)) for r in rows[1:] if r[0] is not None]


def logger_seconds(stamps):
    """ISO stamps on the loggers' clock (+01:00) as seconds since 2009 on that clock"""
    return (np.array([s[:19] for s in stamps], dtype="datetime64[s]") - T0).astype(np.int64)


def utc_seconds(stamps):
    return (np.array([s.replace(" ", "T") + ":00" for s in stamps], dtype="datetime64[s]") - T0).astype(np.int64) + HOUR


def visit_seconds(date, hhmm):
    d = dt.datetime.strptime(date + " " + hhmm, "%Y-%m-%d %H:%M").replace(tzinfo=ROME).astimezone(dt.timezone.utc)
    return int((d.replace(tzinfo=None) + dt.timedelta(hours=1) - dt.datetime(2009, 1, 1)).total_seconds())


class Gauge:
    def __init__(self, target, row, book, blocks):
        self.code, self.name, self.bucket, self.model = row["station"], row["name"], float(row["bucket_mm"]), row["rain_gauge"]
        self.xy = (float(row["x_etrs89_utm33n_m"]), float(row["y_etrs89_utm33n_m"]))
        tips = pd.read_csv(os.path.join(target, "tips_%s_2009-2026.csv" % self.code), dtype=str)
        t = np.unique(logger_seconds(tips["tip_time"].tolist()))
        v = book[book["station"] == self.code].copy()
        v["t"] = [visit_seconds(a, b) for a, b in zip(v["visit_date"], v["visit_time_local"])]
        v = v.sort_values("t", kind="stable")
        for tv in v.loc[v["tip_test_tips"] != "", "t"]:
            t = t[(t < tv) | (t >= tv + HOUR)]
        self.t = t
        gap = np.diff(t)
        start = np.r_[True, gap >= GAP_H * HOUR]
        self.storm = np.cumsum(start) - 1
        self.n = int(self.storm[-1]) + 1
        self.first, self.last = t[start], t[np.r_[start[1:], True]]
        # the rate each tip stands for: its bucket over the time since the tip before (a storm's first tip: a minute)
        self.dt = np.where(start, 60.0, np.r_[60.0, gap])
        self.rate = self.bucket * HOUR / self.dt
        # the storage gauge: each read holds the water since the last emptying
        reads = v[v["storage_gauge_mm"] != ""]
        self.read_t = reads["t"].to_numpy()
        self.read_mm = reads["storage_gauge_mm"].astype(float).to_numpy()
        self.interval = np.searchsorted(self.read_t, t)
        assert self.interval.max() < len(self.read_t)
        # regulation 2.1: a storm belongs to the day in which its largest 60-minute rain depth falls
        d0 = pd.DatetimeIndex(T0 + self.window_end(np.full(len(t), self.bucket)).astype("timedelta64[s]"))
        self.year = d0.year.to_numpy()
        self.warm = (d0.month.to_numpy() >= 5) & (d0.month.to_numpy() <= 10)
        self.seasons = len(set(self.year))
        # the detector's ten-minute blocks, each given to the storm whose tips lie nearest in time
        b = blocks[blocks["station"] == self.code]
        bt = logger_seconds(b["block_start"].tolist())
        edge = (self.last[:-1] + self.first[1:]) / 2.0
        self.b_storm = np.searchsorted(edge, bt)
        self.b_t, self.b_mm = bt, b["intensity_mm_h"].to_numpy(dtype=float) / 6.0
        ice = np.array([("GS" in c) or ("GR" in c) for c in b["wx"]])
        self.hail = np.zeros(self.n, bool)
        self.hail[self.b_storm[ice]] = True

    def water(self, k, one_factor=None):
        """each tip's water with the loss put back: a recorded rate r stands for r / (1 - k r)"""
        if one_factor is not None:
            return np.full(len(self.t), self.bucket * one_factor)
        return self.bucket / np.maximum(1.0 - k * self.rate, 0.02)

    def account(self, w):
        return np.bincount(self.interval, w, len(self.read_t))

    def window_max(self, w):
        """the largest depth in any 60 consecutive minutes of each storm, the water of a tip laid evenly over the time
        since the tip before; the largest window has an edge on a tip, so every tip is tried as a start and as an end"""
        cum = np.cumsum(w)
        x = np.empty(2 * len(self.t))
        y = np.empty(2 * len(self.t))
        x[0::2], x[1::2] = self.t - self.dt, self.t
        y[0::2], y[1::2] = cum - w, cum
        keep = np.r_[True, np.diff(x) > 0]
        x, y = x[keep], y[keep]
        f = lambda q: np.interp(q, x, y)
        best = np.maximum(f(self.t + WINDOW_S) - f(self.t), f(self.t) - f(self.t - WINDOW_S))
        best = np.maximum(best, f(self.t - self.dt + WINDOW_S) - f(self.t - self.dt))
        out = np.zeros(self.n)
        np.maximum.at(out, self.storm, best)
        return out

    def window_end(self, w):
        """the last second of each storm's largest 60 consecutive minutes, on the same windows as window_max"""
        cum = np.cumsum(w)
        x = np.empty(2 * len(self.t))
        y = np.empty(2 * len(self.t))
        x[0::2], x[1::2] = self.t - self.dt, self.t
        y[0::2], y[1::2] = cum - w, cum
        keep = np.r_[True, np.diff(x) > 0]
        x, y = x[keep], y[keep]
        f = lambda q: np.interp(q, x, y)
        opens = f(self.t + WINDOW_S) - f(self.t)
        closes = f(self.t) - f(self.t - WINDOW_S)
        before = f(self.t - self.dt + WINDOW_S) - f(self.t - self.dt)
        best = np.maximum(np.maximum(opens, closes), before)
        end = np.where(closes >= np.maximum(opens, before), self.t,
                       np.where(opens >= before, self.t + WINDOW_S, self.t - self.dt + WINDOW_S)) - 1
        o = np.lexsort((-best, self.storm))
        head = np.r_[True, self.storm[o][1:] != self.storm[o][:-1]]
        return end[o][head].astype(np.int64)

    def placed_max(self, w):
        """a storm's water laid on the blocks in which the detector saw precipitation, by its intensity; the largest
        total over six consecutive blocks"""
        total = np.bincount(self.storm, w, self.n)
        seen = np.bincount(self.b_storm, self.b_mm, self.n)
        slot = (self.b_t // 600).astype(np.int64)
        share = total[self.b_storm] * self.b_mm / np.maximum(seen[self.b_storm], 1e-12)
        frame = pd.DataFrame({"storm": self.b_storm, "slot": slot, "mm": share})
        out = np.zeros(self.n)
        for s, g in frame.groupby("storm"):
            line = np.zeros(int(g["slot"].max() - g["slot"].min()) + 6)
            np.add.at(line, (g["slot"] - g["slot"].min()).to_numpy(), g["mm"].to_numpy())
            c = np.cumsum(np.r_[np.zeros(6), line])
            out[s] = (c[6:] - c[:-6]).max()
        return out


def fit_loss(gauges):
    """one k for the gauges of a bucket model: the value at which their tips close the storage gauge, read by read"""
    def sse(k):
        return sum(float(((g.read_mm - g.account(g.water(k))) ** 2).sum()) for g in gauges)
    lo, hi = 0.0, 0.0075
    for _ in range(60):
        a, b = lo + (hi - lo) / 3.0, hi - (hi - lo) / 3.0
        lo, hi = (lo, b) if sse(a) < sse(b) else (a, hi)
    return 0.5 * (lo + hi)


def run(target):
    stations = sheet(os.path.join(target, "road_stations_register.xlsx"), "Stations")
    crossings = sheet(os.path.join(target, "gully_crossings_register.xlsx"), "Crossings")
    areas = {a["source_area"]: a for a in sheet(os.path.join(target, "gully_crossings_register.xlsx"), "Source areas")}
    book = pd.read_csv(os.path.join(target, "station_visit_book_2009-2026.csv"), dtype=str, keep_default_na=False)
    con = sqlite3.connect(os.path.join(target, "present_weather_blocks.sqlite"))
    blocks = pd.read_sql_query("SELECT station, block_start, wx, intensity_mm_h FROM pw_block ORDER BY station, block_start", con)
    con.close()
    G = {r["station"]: Gauge(target, r, book, blocks) for r in stations}
    k = {}
    for model in sorted({g.model for g in G.values()}):
        grp = [g for g in G.values() if g.model == model]
        kk = fit_loss(grp)
        k.update({g.code: kk for g in grp})
    # the storm maxima at each station: rain storms from the tips, hail and graupel storms from the placed water
    mx, tip_mx = {}, {}
    for c, g in G.items():
        w = g.water(k[c])
        tip_mx[c] = g.window_max(w)
        mx[c] = np.where(g.hail, g.placed_max(w), tip_mx[c])
    # the radar's cells: each source area's pixel against its governing station's
    px = pd.read_csv(os.path.join(target, "radar_pixels.csv"))
    where = {}
    for a, b, x, y in px.itertuples(index=False):
        where[int(a)] = where[int(b)] = (int(x), int(y))
    cells = pd.read_csv(os.path.join(target, "radar_cells_p60max_2013-2026.csv"))
    cells["at"] = [where[int(p)] for p in cells["pixel"]]
    pixel_of = lambda xy: (int(xy[0] // 1000) * 1000 + 500, int(xy[1] // 1000) * 1000 + 500)
    by_pixel = {p: d.drop_duplicates("cell_id").set_index("cell_id")["p60_max_mm"] for p, d in cells.groupby("at")}
    out = {"storms": {}, "depth": {}, "class": {}, "factor": {}}
    for cr in crossings:
        a = areas[cr["source_area"]]
        g = G[cr["governing_station"]]
        src = by_pixel[pixel_of((float(a["x_etrs89_utm33n_m"]), float(a["y_etrs89_utm33n_m"])))]
        own = by_pixel[pixel_of(g.xy)]
        pair = pd.concat([src, own], axis=1, join="inner").to_numpy()
        pair = pair[(pair[:, 0] >= 1.0) & (pair[:, 1] >= 1.0)]
        factor = float(np.exp(np.log(pair[:, 0] / pair[:, 1]).mean()))
        est = np.sort(factor * mx[g.code][g.warm])[::-1]
        name = cr["gully"]
        out["factor"][name] = factor
        out["storms"][name] = float((est >= float(a["triggering_depth_point_mm_60min"])).sum()) / g.seasons
        out["depth"][name] = float(est[TIMES * g.seasons - 1])
        out["class"][name] = 1 + int(out["storms"][name] >= LINES[0]) + int(out["storms"][name] >= LINES[1])
    code = {g.name: c for c, g in G.items()}
    out["under_read_valfosca_pct"] = 100.0 * (1.0 - 1.0 / (1.0 + 100.0 * k[code["Valfosca"]]))
    g = G[code["Costarossa"]]
    m = g.hail & g.warm
    out["hail_gap_costarossa_pct"] = 100.0 * (1.0 - float(tip_mx[g.code][m].sum()) / float(mx[g.code][m].sum()))
    out["burst_factor_marden"] = out["factor"]["Rio Marden"]
    out["loss"] = {G[c].name: k[c] for c in G}
    out["account_factor"] = {g.name: float(g.read_mm.sum() / g.account(g.water(0.0)).sum()) for g in G.values()}
    return out


def compare(v, f):
    """every stated figure of the answer blocks against the second implementation: (label, golden, verifier, band, ok)"""
    rows = []
    for s in sorted(f["storms"]):
        rows.append(("class " + s, f["classes"][s], v["class"][s], None, f["classes"][s] == v["class"][s]))
    for key, band in (("storms", "storms_band"), ("depth", "depth_band")):
        for s in sorted(f[key]):
            lo, hi = f[band][s]
            rows.append(("%s %s" % (key, s), f[key][s], v[key][s], (lo, hi), lo - 1e-9 <= v[key][s] <= hi + 1e-9))
    for key in ("under_read_valfosca_pct", "burst_factor_marden", "hail_gap_costarossa_pct"):
        lo, hi = f[key.replace("_pct", "") + "_band"]
        rows.append((key, f[key], v[key], (lo, hi), lo - 1e-9 <= v[key] <= hi + 1e-9))
    for s in sorted(v["account_factor"]):
        rows.append(("account factor " + s, f["account_factor"][s], v["account_factor"][s], None,
                     abs(f["account_factor"][s] - v["account_factor"][s]) < 0.0015))
    return rows


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
    v = run(target)
    f = json.load(open(os.path.join(HERE, "figures.json")))
    rows = compare(v, f)
    for label, g, x, band, ok in rows:
        print("%-4s %-34s golden %-8s verifier %-10s %s" % ("ok" if ok else "FAIL", label, g, round(x, 3) if isinstance(x, float) else x,
                                                         "" if band is None else "band %s to %s" % band))
    bad = [r for r in rows if not r[4]]
    print("VERIFY %s: %d of %d figures reproduced by the second implementation" % ("PASS" if not bad else "FAIL", len(rows) - len(bad), len(rows)))
    sys.exit(1 if bad else 0)
