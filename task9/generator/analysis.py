"""task9 (architecture 3): the golden analysis, run on the cut pack only. It reads the files the way a careful analyst
would (lot IDs normalised across the MES upgrade, CM1's clock and CM3's German export, WB-2's UTC log, final sort
insertions, the trend's units and outages) and computes every graded figure. effort_passes.py runs the hurried routes
on the same loaded data."""
import csv
import datetime as dt
import io
import json
import math
import os
import re
import sqlite3
from functools import lru_cache
from zoneinfo import ZoneInfo

import numpy as np
import openpyxl

BERLIN = ZoneInfo("Europe/Berlin")
BASE = (dt.datetime(2026, 1, 1), dt.datetime(2026, 3, 31, 23, 59, 59))
WIN = (dt.datetime(2026, 6, 1), dt.datetime(2026, 9, 30, 23, 59, 59))
T_VFD = dt.datetime(2026, 6, 2, 9, 40)


def norm(lot):
    return lot.replace(".", "").strip()


def pt(s, fmt="%Y-%m-%d %H:%M:%S"):
    return dt.datetime.strptime(s, fmt)


def rows(path, delimiter=","):
    with open(path, newline="", encoding="utf-8") as fh:
        r = csv.reader(fh, delimiter=delimiter)
        h = next(r)
        return h, [x for x in r]


def xlsx(path):
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb.worksheets[0]
    it = ws.iter_rows(values_only=True)
    h = list(next(it))
    return h, [list(r) for r in it if r and any(v is not None for v in r)]


class Pack:
    """the loaded pack"""

    def __init__(self, tgt):
        self.tgt = tgt
        p = lambda n: os.path.join(tgt, n)
        # --- sort: the final insertion of every wafer
        con = sqlite3.connect(p("fab2_yield.sqlite"))
        self.products = {r[0]: dict(w=r[1], h=r[2], cols=r[3], rows=r[4], x0=r[5], y0=r[6], gross=r[7])
                         for r in con.execute("SELECT product, die_w_mm, die_h_mm, map_cols, map_rows, col0_x_mm, row0_y_mm, gross_die FROM product")}
        last = {}
        for key, ins, lot, wno, prod, end, tested, good in con.execute(
                "SELECT wafer_key, insertion, lot_id, wafer_no, product, end_time, tested, good FROM sort_wafer"):
            if key not in last or ins > last[key]["ins"]:
                last[key] = dict(key=key, ins=ins, lot=norm(lot), slot=int(wno), product=prod, t=pt(end), tested=tested,
                                 good=good, bins={})
        for key, ins, b, n in con.execute("SELECT wafer_key, insertion, bin, die FROM sort_bin_count"):
            if last[key]["ins"] == ins:
                last[key]["bins"][int(b)] = int(n)
        self.wafers = last
        self._con = con
        # --- MES: each lot's tool and track-in at each step
        h, rs = rows(p("mes_lot_history.csv"))
        ix = {k: i for i, k in enumerate(h)}
        self.mes = {}
        for r in rs:
            if r[ix["HOLD_CODE"]] == "TRACKIN-REVERSED":
                continue
            lot = norm(r[ix["LOT_ID"]])
            self.mes.setdefault(lot, {})[r[ix["STEP"]]] = (r[ix["EQP_ID"]], pt(r[ix["TRACK_IN"]]), r[ix["PRODUCT"]])
        # --- ILD0 deposition chamber per wafer
        h, rs = rows(p("ild0_dep_wafer_log.csv"))
        self.dep = {(norm(r[2]), int(r[3])): (r[0] + r[1], pt(r[5])) for r in rs}
        # --- ILD0 CMP per wafer, from each polisher's own export
        self.cmp = {}
        h, rs = rows(p("CM1_ild0_polish.csv"))
        for r in rs:
            self.cmp[(norm(r[0]), int(r[1]))] = ("CM1", pt(r[3]) - dt.timedelta(minutes=4), float(r[5]))
        for tool in ("CM2", "CM4"):
            h, rs = rows(p("%s_ild0_polish.csv" % tool))
            for r in rs:
                self.cmp[(norm(r[0]), int(r[1].rsplit("-", 1)[1]))] = (tool, pt(r[3]), float(r[5]))
        h, rs = rows(p("CM3_ild0_polish.csv"), delimiter=";")
        for r in rs:
            self.cmp[(norm(r[0]), int(r[1]))] = ("CM3", pt(r[4], "%d.%m.%Y %H:%M:%S"), float(r[6].replace(",", ".")))
        # --- contact etch per wafer
        h, rs = rows(p("ct_etch_fdc_summary.csv"))
        self.etch = {}
        for r in rs:
            self.etch[(norm(r[2]), int(r[3]))] = dict(ch=r[0] + r[1], rec=r[4], t=pt(r[5]), rf=float(r[6]), n=int(r[10]),
                                                      rfh=float(r[11]))
        h, rs = rows(p("etch_chamber_monitors.csv"))
        self.mon = [dict(ch=r[0] + r[1], t=pt(r[2]), adders=int(r[4]), n=int(r[6])) for r in rs]
        # --- the slurry loop's trend: flow in L/min (gpm after the firmware update), the tank's particle count
        h, rs = rows(p("sds_ox1_trend_export.csv"))
        flow, lpc = [], []
        for r in rs:
            t = pt(r[0])
            if r[2] == "FT-101":
                v = float(r[3]) * (3.785411784 if r[4] == "gpm" else 1.0)
                flow.append((t, v))
            elif r[2] == "AT-104":
                lpc.append((t, float(r[3])))
        self.flow = (np.array([x[0].timestamp() for x in flow]), np.array([x[1] for x in flow]))
        self.lpc = (np.array([x[0].timestamp() for x in lpc]), np.array([x[1] for x in lpc]))
        h, rs = xlsx(p("facility_line_list.xlsx"))
        self.taps = {r[4]: float(r[5]) for r in rs if r[0] == "SDS-OX1" and r[4] and r[4] != "-"}
        self.pipe_id_mm = [float(r[7]) for r in rs if r[0] == "SDS-OX1"][0]
        # --- maintenance
        h, rs = xlsx(p("equipment_pm_log.xlsx"))
        self.pou = {}
        self.wet_cleans = {}
        for r in rs:
            t = pt(r[2], "%Y-%m-%d %H:%M")
            if r[3] == "POU_FILTER":
                self.pou.setdefault(r[1], []).append(t)
            elif r[3] == "WET_CLEAN":
                ch = r[1] + r[4].split()[1]
                self.wet_cleans.setdefault(ch, []).append(t)
        for k in self.pou:
            self.pou[k].sort()
        for k in self.wet_cleans:
            self.wet_cleans[k].sort()
        # --- the bench controller log (WB-2 writes UTC)
        self.bench = {}
        seen = set()
        with open(p("pgc_bench_controller.jsonl"), encoding="utf-8") as fh:
            for line in fh:
                e = json.loads(line)
                k = (e["tool"], e["seq"])
                if k in seen:
                    continue
                seen.add(k)
                s = e["ts"]
                if s.endswith("Z"):
                    t = dt.datetime.strptime(s[:19], "%Y-%m-%dT%H:%M:%S").replace(tzinfo=dt.timezone.utc).astimezone(BERLIN).replace(tzinfo=None)
                else:
                    t = dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%S")
                e["t"] = t
                self.bench.setdefault(e["tool"], []).append(e)
        for b in self.bench:
            self.bench[b].sort(key=lambda e: (e["t"], e["seq"]))
        # --- the lab
        h, rs = xlsx(p("lab_bath_metals_2026.xlsx"))
        def val(x):
            if isinstance(x, str) and x.startswith("<"):
                return 0.025
            return float(x)
        self.lab = [dict(bench=r[1], t=pt(r[3], "%Y-%m-%d %H:%M"), total=val(r[6]) + val(r[7]) + val(r[8]), req=r[5]) for r in rs]
        # --- product data
        h, rs = xlsx(p("product_data_sheet.xlsx"))
        ix = {k: i for i, k in enumerate(h)}
        self.sheet = {r[0]: {k: r[i] for k, i in ix.items()} for r in rs if r[0] in ("VX40", "VP12", "VR90")}

    # ---------------------------------------------------------------- helpers
    def maps(self, keys):
        """per-die bins of the final insertion for the wafers asked for"""
        out = {}
        want = {k: self.wafers[k]["ins"] for k in keys}
        q = "SELECT wafer_key, insertion, map_text FROM sort_map WHERE wafer_key IN (%s)"
        keys = list(keys)
        for i in range(0, len(keys), 500):
            chunk = keys[i:i + 500]
            for key, ins, text in self._con.execute(q % ",".join("?" * len(chunk)), chunk):
                if want[key] == ins:
                    out[key] = text
        return out

    def die_geometry(self, product):
        """centres, outer corner radius and (col,row) of every probed die, from the map grid and the die size"""
        pr = self.products[product]
        return grid_geometry(pr["w"], pr["h"], pr["cols"], pr["rows"], pr["x0"], pr["y0"])

    def in_window(self, w, win):
        return win[0] <= w["t"] <= win[1]


def grid_geometry(w, h, cols, rows, x0, y0):
    c, r = np.meshgrid(np.arange(cols), np.arange(rows), indexing="xy")
    xl, yl = x0 + c * w, y0 + r * h
    rmax = np.zeros_like(xl, dtype=float)
    for dx, dy in ((0, 0), (w, 0), (0, h), (w, h)):
        rmax = np.maximum(rmax, np.hypot(xl + dx, yl + dy))
    return dict(col=c, row=r, xc=xl + w / 2, yc=yl + h / 2, rmax=rmax)


def decode(text):
    """map text (top row first) -> 2-D array of bins indexed [row from bottom, col]; 0 where no die"""
    lines = text.split("\n")[::-1]
    code = {".": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "8": 8, "9": 9, "B": 11}
    return np.array([[code[ch] for ch in ln] for ln in lines], dtype=np.int8)


# ======================================================================== R1: the shortfall
def shortfall_first_insertion(pk):
    first = {}
    for key, ins, prod, end, good in pk._con.execute("SELECT wafer_key, insertion, product, end_time, good FROM sort_wafer"):
        if key not in first or ins < first[key][0]:
            first[key] = (ins, prod, pt(end), good)
    out = {}
    for prod in ("VX40", "VP12"):
        b = [g for i, p_, t, g in first.values() if p_ == prod and BASE[0] <= t <= BASE[1]]
        n = [g for i, p_, t, g in first.values() if p_ == prod and WIN[0] <= t <= WIN[1]]
        out[prod] = float(np.mean(b) - np.mean(n))
    return out


def shortfall(pk):
    out = {}
    for prod in ("VX40", "VP12"):
        b = [w["good"] for w in pk.wafers.values() if w["product"] == prod and pk.in_window(w, BASE)]
        n = [w["good"] for w in pk.wafers.values() if w["product"] == prod and pk.in_window(w, WIN)]
        out[prod] = dict(base=float(np.mean(b)), win=float(np.mean(n)), n_base=len(b), n_win=len(n),
                         shortfall=float(np.mean(b) - np.mean(n)), gross=pk.products[prod]["gross"])
    return out


# ======================================================================== R2: the scratch cause and the loop
def step_hold(series, t):
    ts_, vs = series
    i = np.searchsorted(ts_, t, side="right") - 1
    return vs[np.clip(i, 0, len(vs) - 1)]


def loop_frame(pk, products=("VX40", "VP12")):
    """one row per sorted wafer: its polisher, polish time, loop velocity and tank count at polish, filter age, bin 5"""
    area = math.pi * (pk.pipe_id_mm / 2000.0) ** 2
    out = []
    for key, w in pk.wafers.items():
        if w["product"] not in products:
            continue
        c = pk.cmp.get((w["lot"], w["slot"]))
        if not c:
            continue
        tool, t, p1 = c
        ts_ = t.timestamp()
        flow = float(step_hold(pk.flow, ts_))          # L/min
        v = flow / 60000.0 / area
        lpc = float(step_hold(pk.lpc, ts_))
        ch = pk.pou.get(tool, [])
        i = int(np.searchsorted(np.array([x.timestamp() for x in ch]), ts_, side="right")) - 1
        age = (t - ch[i]).total_seconds() / 86400.0 if i >= 0 else np.nan
        early = w["bins"].get(3, 0) + w["bins"].get(4, 0)       # die failed on a test run before the shorts test
        out.append(dict(key=key, product=w["product"], tool=tool, t=t, p1=p1, v=v, lpc=lpc, age=age, tap=pk.taps[tool],
                        b5=w["bins"].get(5, 0), b5r=w["bins"].get(5, 0) * w["tested"] / max(1, w["tested"] - early),
                        good=w["good"], tested=w["tested"], sort_t=w["t"]))
    return out


def regime(r):
    """the loop's state at polish, read off its own velocity: spring (about 1.6 m/s), slow (about 1.0), standby (faster)"""
    if r["v"] > 1.75:
        return "standby"
    return "spring" if r["v"] > 1.3 else "slow"


def scratch_cause(pk, F=None):
    fr = loop_frame(pk)
    vx = [r for r in fr if r["product"] == "VX40"]
    # spring-regime level per polisher (the loop as it ran before June), VX40
    spring = {}
    for tool in ("CM1", "CM2", "CM3", "CM4"):
        x = [r["b5"] for r in vx if r["tool"] == tool and regime(r) == "spring"]
        spring[tool] = float(np.mean(x))
    by, raw_by = {}, {}
    for tool in spring:
        by[tool] = {g: float(np.mean([r["b5r"] for r in vx if r["tool"] == tool and regime(r) == g] or [np.nan]))
                    for g in ("spring", "slow", "standby")}
        raw_by[tool] = {g: float(np.mean([r["b5"] for r in vx if r["tool"] == tool and regime(r) == g] or [np.nan]))
                        for g in ("spring", "slow", "standby")}
    win = [r for r in vx if WIN[0] <= r["sort_t"] <= WIN[1]]
    excess = np.array([r["b5"] - spring[r["tool"]] for r in win])
    surv = np.array([r["good"] / max(1, r["tested"] - r["b5"]) for r in win])
    cost_vx = float(np.mean(excess * surv))
    raw_vx = float(np.mean(excess))
    # bin 5's non-scratch part from the inline scans (bin 5 against the scratch count on the scanned wafers)
    return dict(spring=spring, by_regime=by, raw_by_regime=raw_by, cost_vx40=cost_vx, excess_vx40=raw_vx, n_win=len(win),
                tap=dict(pk.taps))


# ======================================================================== R3: the bath's metals, rebuilt from its flows
def bath_basis(pk):
    """replay each bench's tank from its own log with unit drag (b) and unit fresh level (a): the state is
    a * c_fresh + b * drag_per_wafer at every event, so the lab's samples fit both by least squares"""
    out = {}
    for bench, evs in pk.bench.items():
        a = b = 0.0
        vol = 52.0
        recs, lots = [], {}
        for e in evs:
            if e["event"] == "DRAIN_FILL":
                vol = float(e.get("fill_l", vol))
                a, b = 1.0, 0.0
            elif e["event"] == "CHEM_SPIKE":
                f = float(e["added_l"]) / vol
                a, b = a * (1 - f) + f, b * (1 - f)
            elif e["event"] == "BATCH_START":
                n = int(e["wafers"])
                lots[norm(e["lot"])] = (a, b + 0.5 * n, e["t"])
                b += n
            else:
                continue
            recs.append((e["t"].timestamp(), a, b))
        out[bench] = dict(t=np.array([r[0] for r in recs]), a=np.array([r[1] for r in recs]),
                          b=np.array([r[2] for r in recs]), lots=lots, vol=vol)
    return out


def fit_bath(pk, basis):
    X, y = [], []
    for s in pk.lab:
        bb = basis[s["bench"]]
        i = int(np.searchsorted(bb["t"], s["t"].timestamp(), side="right")) - 1
        X.append([bb["a"][i], bb["b"][i]])
        y.append(s["total"])
    X, y = np.array(X), np.array(y)
    coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    return dict(c_fresh=float(coef[0]), drag=float(coef[1]), n=len(y), rmse=float(np.sqrt(np.mean((X @ coef - y) ** 2))))


def lot_bath(pk, basis, fit):
    out = {}
    for bench, bb in basis.items():
        for lot, (a, b, t) in bb["lots"].items():
            out[lot] = (fit["c_fresh"] * a + fit["drag"] * b, bench, t)
    return out


def replay(arrivals_days, wafers, sched, c_fresh, drag, vol=52.0, spike_l=6.0, start_day=0.0):
    """a bench run on a stream of batches under a chemical life schedule ('spring': drain and fill at 06:00 and 18:00,
    spike every 6 lots; 'summer': drain and fill at 06:00, spike every 10 lots); returns what each batch saw"""
    hours, every = ((6, 18), 6) if sched == "spring" else ((6,), 10)
    c, since, seen = c_fresh, 0, []
    nxt = math.floor(start_day) + min(h for h in hours) / 24.0
    while nxt <= start_day:
        nxt = _next_change(nxt, hours)
    for d, n in zip(arrivals_days, wafers):
        while nxt <= d:
            c, since = c_fresh, 0
            nxt = _next_change(nxt, hours)
        seen.append(c + 0.5 * drag * n)
        c += drag * n
        since += 1
        if since >= every:
            f = spike_l / vol
            c = c * (1 - f) + c_fresh * f
            since = 0
    return np.array(seen)


def _next_change(t, hours):
    day = math.floor(t + 1e-9)
    for k in range(3):
        for h in hours:
            c = day + k + h / 24.0
            if c > t + 1e-9:
                return c
    return day + 1.25


GATE = {"VX40": 31.4, "VP12": 15.1, "VR90": 53.4}


def goi_fit(pk, lb):
    """bin 6 per die against the metal the wafer saw, scaled by gate oxide area per die"""
    xs, ys, gs, ps = [], [], [], []
    for w in pk.wafers.values():
        if w["lot"] not in lb:
            continue
        xs.append(lb[w["lot"]][0])
        risk = w["tested"] - sum(w["bins"].get(b, 0) for b in (3, 4, 5))
        ys.append(w["bins"].get(6, 0) / max(1, risk))
        gs.append(float(pk.sheet[w["product"]]["gate_oxide_area_mm2"]))
        ps.append(w["product"])
    xs, ys, gs = np.array(xs), np.array(ys), np.array(gs)
    best = None
    for cth in np.arange(0.70, 2.01, 0.01):
        for gam in np.arange(0.8, 1.81, 0.05):
            z = gs * np.maximum(0.0, xs - cth) ** gam
            A = np.column_stack([gs, z])
            coef, *_ = np.linalg.lstsq(A, ys, rcond=None)
            r = float(np.sum((A @ coef - ys) ** 2))
            if best is None or r < best[0]:
                best = (r, float(cth), float(gam), float(coef[0]), float(coef[1]))
    _, cth, gam, base, k = best
    return dict(c_th=cth, gamma=gam, base_per_mm2=base, k_per_mm2=k)


def goi_p(gf, c, gate):
    return gf["base_per_mm2"] * gate + gf["k_per_mm2"] * gate * np.maximum(0.0, np.asarray(c) - gf["c_th"]) ** gf["gamma"]


def bath_cause(pk):
    basis = bath_basis(pk)
    fit = fit_bath(pk, basis)
    lb = lot_bath(pk, basis, fit)
    gf = goi_fit(pk, lb)
    # the counterfactual: the same batches under the spring life
    spring_seen = {}
    for bench, evs in pk.bench.items():
        bat = [e for e in evs if e["event"] == "BATCH_START"]
        t0 = bat[0]["t"]
        days = np.array([(e["t"] - t0).total_seconds() / 86400.0 + (t0.hour + t0.minute / 60.0) / 24.0 for e in bat])
        seen = replay(days, [int(e["wafers"]) for e in bat], "spring", fit["c_fresh"], fit["drag"], start_day=days[0] - 0.01)
        for e, s in zip(bat, seen):
            spring_seen[norm(e["lot"])] = s
    win = [w for w in pk.wafers.values() if w["product"] == "VX40" and WIN[0] <= w["t"] <= WIN[1] and w["lot"] in lb]
    cost = []
    for w in win:
        g = GATE["VX40"]
        dp = goi_p(gf, lb[w["lot"]][0], g) - goi_p(gf, spring_seen[w["lot"]], g)
        surv = w["good"] / max(1, w["tested"] - w["bins"].get(6, 0))
        cost.append(float(dp) * w["tested"] * surv)
    raw = float(np.mean([float(goi_p(gf, lb[w["lot"]][0], GATE["VX40"]) - goi_p(gf, spring_seen[w["lot"]], GATE["VX40"])) * w["tested"]
                         for w in win]))
    return dict(fit=fit, goi=gf, cost_vx40=float(np.mean(cost)), raw_vx40=raw, lot_bath=lb, spring_seen=spring_seen)


def bench_q1(fit, sched, lots_per_day=31.0, days=400, seed=7):
    """a bench at the plan's loading under a chemical life, as the golden replays it (Poisson arrivals of 25-wafer lots)"""
    rng = np.random.default_rng(seed)
    arr = np.cumsum(rng.exponential(1.0 / lots_per_day, int(lots_per_day * days)))
    seen = replay(arr, [25] * len(arr), sched, fit["c_fresh"], fit["drag"], start_day=0.0)
    return seen[int(len(seen) * 0.05):]


# ======================================================================== R4: the edge pair
def change_dates(pk):
    h, rs = xlsx(os.path.join(pk.tgt, "equipment_pm_log.xlsx"))
    sh = [pt(r[2], "%Y-%m-%d %H:%M") for r in rs if r[3] == "PART_REPLACE" and "showerhead" in str(r[4]) and r[1] == "DP2"]
    h, rr = rows(os.path.join(pk.tgt, "recipe_change_log.csv"))
    r8 = [pt(r[0], "%Y-%m-%d %H:%M") for r in rr if r[1] == "CM3" and r[4] == "R8"]
    return dict(showerhead=min(sh), cm3_r8=min(r8))


def edge_frame(pk, cd):
    out = []
    for key, w in pk.wafers.items():
        k = (w["lot"], w["slot"])
        if k not in pk.dep or k not in pk.cmp:
            continue
        ch, tdep = pk.dep[k]
        tool, tcmp, _ = pk.cmp[k]
        thick = ch == "DP2B" and tdep >= cd["showerhead"]
        thin = tool == "CM3" and tcmp >= cd["cm3_r8"]
        out.append(dict(key=key, product=w["product"], t=w["t"], dp2b=thick, cm3=thin, b3=w["bins"].get(3, 0),
                        b4=w["bins"].get(4, 0), good=w["good"], tested=w["tested"], cls=("pair" if thick and thin else
                        "thick" if thick else "thin" if thin else "nominal")))
    return out


def edge_cause(pk):
    cd = change_dates(pk)
    fr = edge_frame(pk, cd)
    out = dict(dates=cd, cls={})
    for prod in ("VX40", "VP12"):
        x = [r for r in fr if r["product"] == prod]
        base3 = float(np.mean([r["b3"] for r in x if r["cls"] == "nominal"]))
        base4 = float(np.mean([r["b4"] for r in x if r["cls"] == "nominal"]))
        cls = {}
        for c in ("nominal", "pair", "thick", "thin"):
            y = [r for r in x if r["cls"] == c]
            cls[c] = dict(n=len(y), b3=float(np.mean([r["b3"] for r in y])) - base3 if y else 0.0,
                          b4=float(np.mean([r["b4"] for r in y])) - base4 if y else 0.0)
        out["cls"][prod] = dict(base3=base3, base4=base4, **cls)
    vx = [r for r in fr if r["product"] == "VX40" and WIN[0] <= r["t"] <= WIN[1]]
    b3, b4 = out["cls"]["VX40"]["base3"], out["cls"]["VX40"]["base4"]
    cost = [((r["b3"] - b3) + (r["b4"] - b4)) * r["good"] / max(1, r["tested"] - r["b3"] - r["b4"]) for r in vx]
    out["cost_vx40"] = float(np.mean(cost))
    out["raw_vx40"] = float(np.mean([(r["b3"] - b3) + (r["b4"] - b4) for r in vx]))
    share = {c: sum(1 for r in vx if r["cls"] == c) / len(vx) for c in ("nominal", "pair", "thick", "thin")}
    thick_ex = out["cls"]["VX40"]["thick"]["b3"]
    thin_ex = out["cls"]["VX40"]["thin"]["b4"]
    surv = float(np.mean([r["good"] / max(1, r["tested"] - r["b3"] - r["b4"]) for r in vx]))
    out["share"] = share
    out["harmonise_alone_vx40"] = float((share["thin"] * thin_ex - share["pair"] * thick_ex) * surv)   # die gained per wafer
    out["harmonise_claimed_vx40"] = float(share["thin"] * thin_ex * surv)
    out["frame"] = fr
    return out


def vr90_grid(sheet):
    w, h = float(sheet["VR90"]["die_w_mm"]), float(sheet["VR90"]["die_h_mm"])
    r = 147.0
    best = None
    for ox in np.arange(0, 1.0, 0.1):
        for oy in np.arange(0, 1.0, 0.1):
            cols = np.arange(-20, 21)
            X, Y = np.meshgrid((cols + ox) * w, (cols + oy) * h)
            ok = np.ones_like(X, dtype=bool)
            rmax = np.zeros_like(X)
            for cx, cy in ((X, Y), (X + w, Y), (X, Y + h), (X + w, Y + h)):
                rr = np.hypot(cx, cy)
                ok &= rr <= r
                rmax = np.maximum(rmax, rr)
            n = int(ok.sum())
            if best is None or n > best[0]:
                best = (n, rmax[ok])
    return dict(n=best[0], rmax=best[1], w=w, h=h)


def edge_profile_by_r(pk, frame, cls, product_bins=(3,)):
    """per-die excess fail rate by outer-corner radius on the wafers of a route class, against nominal wafers"""
    edges = np.array([0, 118, 124, 128, 132, 136, 139, 142, 145, 147.01])
    acc = {}
    for prod in ("VX40", "VP12"):
        geo = pk.die_geometry(prod)
        rmax = geo["rmax"]
        band = np.digitize(rmax, edges) - 1
        for c in (cls, "nominal"):
            keys = [r["key"] for r in frame if r["product"] == prod and r["cls"] == c]
            if c == "nominal":
                keys = keys[::4]
            mp = pk.maps(keys)
            fails = np.zeros(len(edges) - 1)
            dies = np.zeros(len(edges) - 1)
            for key, text in mp.items():
                m = decode(text)
                present = m > 0
                f = np.isin(m, product_bins)
                for b in range(len(edges) - 1):
                    sel = present & (band == b)
                    dies[b] += sel.sum()
                    fails[b] += (f & sel).sum()
            acc[(prod, c)] = fails / np.maximum(dies, 1)
    rate = np.zeros(len(edges) - 1)
    for b in range(len(edges) - 1):
        vals = [acc[(p, cls)][b] - acc[(p, "nominal")][b] for p in ("VX40", "VP12")]
        rate[b] = max(0.0, float(np.mean(vals)))
    return edges, rate


# ======================================================================== R5: the etch chambers' polymer
def etch_frame(pk):
    by = {}
    for (lot, slot), r in pk.etch.items():
        by.setdefault(r["ch"], []).append(dict(r, lot=lot, slot=slot))
    for ch in by:
        by[ch].sort(key=lambda r: r["t"])
        deep = 0.0
        last_n = 10 ** 9
        for r in by[ch]:
            if r["n"] < last_n:          # the counter reset: a wet clean since the last wafer we saw
                deep = 0.0
            if r["rec"] == "CT-DEEP-07":
                deep += r["rf"]
            r["deep_s"] = deep
            r["total_s"] = r["rfh"] * 3600.0
            last_n = r["n"]
    return by


def polymer_fit(pk, by, kappa_fixed=None):
    """monitor adders against the chamber's load since its wet clean, with the deep recipe's polymer per RF second a
    free factor; the onset load and the factor come out of the cycles that carried different deep shares"""
    std_per_wafer = []
    for ch, rs in by.items():
        for r in rs:
            if r["deep_s"] == 0 and r["n"] > 50:
                std_per_wafer.append(r["total_s"] / r["n"])
    s_std = float(np.median(std_per_wafer))
    pts = []
    for m in pk.mon:
        rs = by.get(m["ch"])
        if not rs:
            continue
        ts_ = np.array([r["t"].timestamp() for r in rs])
        i = int(np.searchsorted(ts_, m["t"].timestamp(), side="right")) - 1
        if i < 0:
            continue
        r = rs[i]
        extra = m["n"] - r["n"]
        if extra < 0 or extra > 400:
            continue
        pts.append((r["total_s"] - r["deep_s"] + extra * s_std, r["deep_s"], m["adders"]))
    S = np.array([p[0] for p in pts])
    Dp = np.array([p[1] for p in pts])
    y = np.array([p[2] for p in pts], dtype=float)
    best = None
    for kap in ([kappa_fixed] if kappa_fixed else np.arange(1.0, 2.61, 0.02)):
        Lk = S + kap * Dp
        for lth in np.arange(150000, 260001, 1000):
            E = (np.maximum(0.0, Lk - lth) / 1e4) ** 1.5
            A = np.column_stack([np.ones_like(E), E])
            coef, *_ = np.linalg.lstsq(A, y, rcond=None)
            r = float(np.sum((A @ coef - y) ** 2))
            if best is None or r < best[0]:
                best = (r, float(kap), float(lth), float(coef[0]), float(coef[1]))
    _, kap, lth, a, b = best
    return dict(kappa=kap, l_th=lth, mon_a=a, mon_b=b, std_rf_s=s_std, n=len(pts))


def etch_cause(pk, kappa_fixed=None):
    by = etch_frame(pk)
    pf = polymer_fit(pk, by, kappa_fixed)
    E = {}
    for ch, rs in by.items():
        for r in rs:
            L = r["total_s"] - r["deep_s"] + pf["kappa"] * r["deep_s"]
            E[(r["lot"], r["slot"])] = (max(0.0, L - pf["l_th"]) / 1e4) ** 1.5
    kill = {}
    for prod in ("VX40", "VP12"):
        xs, ys = [], []
        for w in pk.wafers.values():
            k = (w["lot"], w["slot"])
            if w["product"] != prod or k not in E:
                continue
            risk = w["tested"] - sum(w["bins"].get(b, 0) for b in (3, 4, 5, 6))
            f8 = w["bins"].get(8, 0) / max(1, risk)
            xs.append(E[k])
            ys.append(-math.log(max(1e-6, 1 - f8)))
        A = np.column_stack([np.ones(len(xs)), xs])
        coef, *_ = np.linalg.lstsq(A, np.array(ys, float), rcond=None)
        kill[prod] = dict(intercept=float(coef[0]), per_E=float(coef[1]))   # per die, in log-survival
    win = [w for w in pk.wafers.values() if w["product"] == "VX40" and WIN[0] <= w["t"] <= WIN[1] and (w["lot"], w["slot"]) in E]
    k = kill["VX40"]
    cost = float(np.mean([(1 - math.exp(-k["per_E"] * E[(w["lot"], w["slot"])])) * math.exp(-k["intercept"])
                          * (w["tested"] - sum(w["bins"].get(b, 0) for b in (3, 4, 5, 6))) for w in win]))
    raw = float(np.mean([w["bins"].get(8, 0) for w in win])) - float(np.mean(
        [w["bins"].get(8, 0) for w in pk.wafers.values() if w["product"] == "VX40" and BASE[0] <= w["t"] <= BASE[1]]))
    raw = max(raw, float(np.mean([(1 - math.exp(-k["per_E"] * E[(w["lot"], w["slot"])])) * w["tested"] for w in win])))
    return dict(fit=pf, kill=kill, cost_vx40=cost, raw_vx40=raw, E=E)


def vr90_etch(pk, ec, clean, share=0.21, rf_vr=186.0, n_path=None):
    """VR90's particle kill per die on a chamber running it at the share given, cleaned every `clean` wafers, along the
    expected load path; the per-mm2 kill intensity from VX40's bin 8 per unit of flaking"""
    pf = ec["fit"]
    per_w = share * rf_vr * pf["kappa"] + (1 - share) * pf["std_rf_s"]
    ks = np.arange(int(clean))
    L = (ks + 0.5) * per_w
    Ek = (np.maximum(0.0, L - pf["l_th"]) / 1e4) ** 1.5
    gV = pk.products["VX40"]
    mu = ec["kill"]["VX40"]["per_E"] / (gV["w"] * gV["h"])     # log-survival per mm2 of die per unit E
    area = float(pk.sheet["VR90"]["die_area_mm2"])
    p = 1 - np.exp(-mu * Ek * area)
    return dict(p=float(np.mean(p)), no_flake=int(pf["l_th"] // per_w), per_wafer_load=per_w)


# ======================================================================== R6: VR90's yield read at its own die area
def block_yields(pk, products=("VX40", "VP12"), window=BASE, rmax_cut=144.0):
    shapes = {"VX40": [(1, 1), (2, 1), (1, 2), (2, 2), (3, 2), (2, 3)],
              "VP12": [(1, 1), (2, 1), (1, 2), (2, 2), (3, 2), (2, 3), (3, 3), (4, 2), (2, 4)]}
    out = []
    for prod in products:
        geo = pk.die_geometry(prod)
        inner = geo["rmax"] <= rmax_cut
        keys = [k for k, w in pk.wafers.items() if w["product"] == prod and window[0] <= w["t"] <= window[1]]
        mp = pk.maps(keys)
        pr = pk.products[prod]
        acc = {s: [0, 0] for s in shapes[prod]}
        for key, text in mp.items():
            m = decode(text)
            valid = (m > 0) & inner
            fail = (m == 8) & valid
            V = np.pad(valid.astype(int), ((1, 0), (1, 0))).cumsum(0).cumsum(1)
            Fc = np.pad(fail.astype(int), ((1, 0), (1, 0))).cumsum(0).cumsum(1)
            for (bw, bh) in shapes[prod]:
                def box(C):
                    return C[bh:, bw:] - C[:-bh, bw:] - C[bh:, :-bw] + C[:-bh, :-bw]
                v, f = box(V), box(Fc)
                full = v == bw * bh
                acc[(bw, bh)][0] += int(full.sum())
                acc[(bw, bh)][1] += int((full & (f == 0)).sum())
        for (bw, bh), (n, g) in acc.items():
            out.append(dict(product=prod, shape=(bw, bh), area=bw * bh * pr["w"] * pr["h"], n=n, y=g / n))
    return out


def tile_route(pk, window=None):
    """VR90 read as four VX40 die: January to March's VX40 maps on CM1 and CM3 tiled in 2 by 2 blocks, a block good when
    no die fails a defect bin (2 to 6 and 8), carried to VR90's area and the design-limited yield; it keeps VX40's own
    polish time, gate oxide, bench loading, polisher mix and edge die"""
    window = window or BASE
    keys = [k for k, w in pk.wafers.items() if w["product"] == "VX40" and window[0] <= w["t"] <= window[1]
            and pk.cmp.get((w["lot"], w["slot"]), (None,))[0] in ("CM1", "CM3")]
    n = g = 0
    for key, text in pk.maps(keys).items():
        m = decode(text)
        valid = m > 0
        bad = valid & (m > 1) & (m != 9) & (m != 11)
        V = np.pad(valid.astype(int), ((1, 0), (1, 0))).cumsum(0).cumsum(1)
        B = np.pad(bad.astype(int), ((1, 0), (1, 0))).cumsum(0).cumsum(1)
        box = lambda C: C[2:, 2:] - C[:-2, 2:] - C[2:, :-2] + C[:-2, :-2]
        full = box(V) == 4
        n += int(full.sum())
        g += int((full & (box(B) == 0)).sum())
    pr = pk.products["VX40"]
    k = float(pk.sheet["VR90"]["die_area_mm2"]) / (4 * pr["w"] * pr["h"])
    return (g / n) ** k * float(pk.sheet["VR90"]["design_limited_yield"])


def nb_fit(blocks):
    A = np.array([b["area"] for b in blocks])
    Y = np.array([b["y"] for b in blocks])
    W = np.sqrt(np.array([b["n"] for b in blocks], float))
    best = None
    for alpha in np.exp(np.linspace(np.log(0.2), np.log(20), 300)):
        # for each alpha, D from a 1-D search
        for D in np.linspace(0.0002, 0.0030, 281):
            r = float(np.sum((W * ((1 + A * D / alpha) ** (-alpha) - Y)) ** 2))
            if best is None or r < best[0]:
                best = (r, float(alpha), float(D))
    _, alpha, D = best
    return dict(alpha=alpha, D_per_mm2=D)


def nb_yield(fit, area):
    return float((1 + area * fit["D_per_mm2"] / fit["alpha"]) ** (-fit["alpha"]))


# ======================================================================== R7: VR90's Q1 2027 yield, built up
PLAN = dict(commitment=412000, assembly=0.992, final_test=0.981, gross=184, lots_per_day=31.0, share=0.21, clean=2400)


GOLDEN_OPT = dict(mix="vr90t", scr_form="exp", nb="fit", goi="fit", q1_bath="replay", kappa="fit", etch_kill="VX40",
                  edge_plan="thick", uniform_loop=False, share=0.21)


def pooled_scratch(pk, sc):
    """the rival reading of each polisher's scratch level: bin 5 per mm2 of die per polish second pooled over VX40 and
    VP12 wafers (the loop's damage does not depend on the product), put back in VX40-wafer units"""
    fr = loop_frame(pk, products=("VX40", "VP12"))
    unit = lambda p: pk.products[p]["gross"] * pk.products[p]["w"] * pk.products[p]["h"] * float(pk.sheet[p]["ild0_p1_time_s"])
    uV = unit("VX40")
    by = {}
    for tool in ("CM1", "CM2", "CM3", "CM4"):
        by[tool] = {}
        for reg in ("spring", "slow", "standby"):
            xs = [r["b5r"] / unit(r["product"]) for r in fr if r["tool"] == tool and regime(r) == reg]
            by[tool][reg] = float(np.mean(xs)) * uV if xs else float("nan")
    return dict(sc, by_regime=by)


def scratch_intensity(sc, gV, pol_vx, tool, reg, uniform=False):
    """bin 5 per VX40 wafer as a kill intensity per mm2 of die per polish second; 'uniform' is the hurried reading
    that books each polisher's own level to its consumables and spreads the summer's excess evenly over all four"""
    br = sc["by_regime"]
    if uniform and reg != "spring":
        b5 = br[tool]["spring"] + float(np.mean([br[t][reg] - br[t]["spring"] for t in br]))
    else:
        b5 = br[tool][reg]
    return b5 / (gV["gross"] * gV["w"] * gV["h"] * pol_vx)


def vr90_build(pk, sc, bc, ec, eg, opt=None, blocks=None):
    o = dict(GOLDEN_OPT, **(opt or {}))
    sheet = pk.sheet
    area = float(sheet["VR90"]["die_area_mm2"])
    pol_vr = float(sheet["VR90"]["ild0_p1_time_s"])
    pol_vx = float(sheet["VX40"]["ild0_p1_time_s"])
    gV = pk.products["VX40"]
    grid = vr90_grid(sheet)
    # random-defect yield at VR90's area (January to March, read in blocks of die)
    blocks = blocks if blocks is not None else block_yields(pk)
    if o["nb"] == "fit":
        nbf = nb_fit(blocks)
        y_rand = nb_yield(nbf, area)
    elif o["nb"] in ("vx40", "vp12"):
        nbf = nb_fit([b for b in blocks if b["product"] == o["nb"].upper()])
        y_rand = nb_yield(nbf, area)
    elif o["nb"] == "interp":
        nbf = None
        pts = sorted((b["area"], b["y"]) for b in blocks)
        xs, ys = np.array([p[0] for p in pts]), np.array([p[1] for p in pts])
        y_rand = float(np.exp(np.interp(area, xs, np.log(ys))))
    else:   # the die-area formula from the die's own yield: Poisson, or a negative binomial at a stated cluster factor
        y1 = [b for b in blocks if b["product"] == "VX40" and b["shape"] == (1, 1)][0]["y"]
        a1 = gV["w"] * gV["h"]
        if o["nb"] == "poisson":
            y_rand = y1 ** (area / a1)
        else:
            al = float(o["nb"].split("=")[1])
            D = al * (y1 ** (-1 / al) - 1) / a1
            y_rand = (1 + area * D / al) ** (-al)
        nbf = None
    # scratches on the polishers VR90 runs on
    if o["mix"] == "vr90t":
        tv = [tool for (lot, slot), (tool, t, p1) in pk.cmp.items() if lot.startswith("VRT") and t >= T_VFD]
        mix = {tool: sum(1 for x in tv if x == tool) / len(tv) for tool in ("CM1", "CM2", "CM3", "CM4")}
    elif o["mix"] == "even13":
        mix = {"CM1": 0.5, "CM2": 0.0, "CM3": 0.5, "CM4": 0.0}
    else:
        fr = loop_frame(pk, products=("VX40",))
        rr = [r for r in fr if regime(r) == "slow"]
        mix = {tool: sum(1 for r in rr if r["tool"] == tool) / len(rr) for tool in ("CM1", "CM2", "CM3", "CM4")}
    def s_scr(reg):
        s = 0.0
        for tool, share in mix.items():
            if share == 0:
                continue
            x = scratch_intensity(sc, gV, pol_vx, tool, reg, o["uniform_loop"]) * area * pol_vr
            s += share * (float(np.exp(-x)) if o["scr_form"] == "exp" else max(0.0, 1 - x))
        return s
    S_scr = {"plan": s_scr("slow"), "fixed": s_scr("spring")}
    # gate oxide integrity under the plan's loading
    S_goi = {}
    gf = bc["goi"] if o["goi"] == "fit" else o["goi"]
    for state, sched in (("plan", "summer"), ("fixed", "spring")):
        if o["q1_bath"] == "replay":
            seen = bench_q1(bc["fit"], sched, PLAN["lots_per_day"])
        else:   # the summer's own lots, as they ran (and their spring replay)
            lots = [l for l, (c, b, t) in bc["lot_bath"].items() if t >= dt.datetime(2026, 7, 1) and l in bc["spring_seen"]]
            seen = np.array([bc["lot_bath"][l][0] if state == "plan" else bc["spring_seen"][l] for l in lots])
        S_goi[state] = float(np.mean(1 - goi_p(gf, seen, GATE["VR90"])))
    # the edge under the plan: CM3 harmonised, DP2B on SH-300-C, so every DP2B wafer runs thick
    edges, rate = eg["thick_rate"]
    band = np.clip(np.digitize(grid["rmax"], edges) - 1, 0, len(rate) - 1)
    p_thick = rate[band]
    sh = eg["dp2b_share"]
    S_edge = {"plan": float((1 - sh) + sh * np.mean(1 - p_thick)) if o["edge_plan"] == "thick" else 1.0, "fixed": 1.0}
    # contact-etch particles above the line's own level
    ec2 = ec
    if o["kappa"] != "fit" or o["etch_kill"] != "VX40":
        ec2 = dict(ec, fit=dict(ec["fit"]))
        if o["kappa"] != "fit":
            ec2["fit"]["kappa"] = float(o["kappa"])
        if o["etch_kill"] != "VX40":
            kv = ec["kill"]["VP12"]["per_E"] / (pk.products["VP12"]["w"] * pk.products["VP12"]["h"]) * (gV["w"] * gV["h"])
            ec2["kill"] = dict(ec["kill"], VX40=dict(ec["kill"]["VX40"], per_E=kv))
    et = vr90_etch(pk, ec2, PLAN["clean"], o["share"])
    S_prt = {"plan": 1 - et["p"], "fixed": 1.0}
    S_fall = float(np.mean(1 - np.where(grid["rmax"] > 145.0, eg["fallout_145"], 0.0)))
    design = float(sheet["VR90"]["design_limited_yield"])
    parts = dict(rand=y_rand, scr=S_scr, goi=S_goi, edge=S_edge, prt=S_prt, fall=S_fall, design=design)
    def y(st):
        return y_rand * S_scr[st["scr"]] * S_goi[st["goi"]] * S_edge[st["edge"]] * S_prt[st["prt"]] * S_fall * design
    plan = dict(scr="plan", goi="plan", edge="plan", prt="plan")
    fixed = dict(scr="fixed", goi="fixed", edge="fixed", prt="fixed")
    y_plan, y_fixed = y(plan), y(fixed)
    add = {}
    for c, k in (("loop", "scr"), ("bath", "goi"), ("edge", "edge"), ("etch", "prt")):
        add[c] = 100 * (y(dict(plan, **{k: "fixed"})) - y_plan)
    starts = lambda yy: PLAN["commitment"] / (PLAN["gross"] * yy * PLAN["assembly"] * PLAN["final_test"])
    return dict(y_plan=y_plan, y_fixed=y_fixed, cost=add, parts=parts, nb=nbf, blocks=blocks, grid_n=grid["n"],
                starts_fixed=starts(y_fixed), starts_plan=starts(y_plan), no_flake=et["no_flake"], mix=mix)


def edge_inputs(pk, ed):
    edges, rate = edge_profile_by_r(pk, ed["frame"], "thick", (3,))
    fr = ed["frame"]
    dp = [r for r in fr if r["product"] == "VX40" and WIN[0] <= r["t"] <= WIN[1]]
    share = sum(1 for r in dp if r["dp2b"]) / len(dp)
    # normal edge fallout per outermost die (bins 3, 4 and 8 there, less bin 8's interior rate), nominal wafers
    vals = []
    for prod in ("VX40", "VP12"):
        geo = pk.die_geometry(prod)
        out_ = geo["rmax"] > 145.0
        inner = geo["rmax"] <= 144.0
        keys = [r["key"] for r in fr if r["product"] == prod and r["cls"] == "nominal"][::5]
        f_out = n_out = f8_in = n_in = 0
        for key, text in pk.maps(keys).items():
            m = decode(text)
            pres = m > 0
            f_out += int((np.isin(m, (3, 4, 8)) & pres & out_).sum())
            n_out += int((pres & out_).sum())
            f8_in += int(((m == 8) & pres & inner).sum())
            n_in += int((pres & inner).sum())
        vals.append(f_out / n_out - f8_in / n_in)
    return dict(thick_rate=(edges, rate), dp2b_share=share, fallout_145=float(np.mean(vals)))


def run_all(tgt):
    pk = Pack(tgt)
    F = {}
    F["R1"] = shortfall(pk)
    F["R1_first"] = shortfall_first_insertion(pk)
    sc = scratch_cause(pk)
    bc = bath_cause(pk)
    ed = edge_cause(pk)
    ec = etch_cause(pk)
    eg = edge_inputs(pk, ed)
    vr = vr90_build(pk, sc, bc, ec, eg)
    F["R2"] = dict(cost_vx40=sc["cost_vx40"], excess_vx40=sc["excess_vx40"], by_regime=sc["by_regime"],
                   raw_by_regime=sc["raw_by_regime"], tap=sc["tap"],
                   vr90_cost=vr["cost"]["loop"])
    F["R3"] = dict(cost_vx40=bc["cost_vx40"], raw_vx40=bc["raw_vx40"], fit=bc["fit"], goi=bc["goi"], vr90_cost=vr["cost"]["bath"])
    F["R4"] = dict(cost_vx40=ed["cost_vx40"], raw_vx40=ed["raw_vx40"], harmonise_alone=ed["harmonise_alone_vx40"],
                   harmonise_claimed=ed["harmonise_claimed_vx40"], share=ed["share"], cls=ed["cls"],
                   vr90_cost=vr["cost"]["edge"], dates={k: str(v) for k, v in ed["dates"].items()})
    F["R5"] = dict(cost_vx40=ec["cost_vx40"], raw_vx40=ec["raw_vx40"], fit=ec["fit"], kill=ec["kill"], vr90_cost=vr["cost"]["etch"],
                   no_flake=vr["no_flake"])
    F["R6"] = dict(y_fixed=vr["y_fixed"], nb=vr["nb"], parts=vr["parts"], grid_n=vr["grid_n"])
    F["R7"] = dict(y_plan=vr["y_plan"], starts_fixed=vr["starts_fixed"], starts_plan=vr["starts_plan"], mix=vr["mix"])
    return F, dict(pk=pk, sc=sc, bc=bc, ed=ed, ec=ec, eg=eg, vr=vr)
