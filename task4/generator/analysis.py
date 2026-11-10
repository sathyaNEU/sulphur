"""Every figure the build owes, computed from the shipped files alone (never from sim.py): the cleaning, the energy
model on the pilot's daily summaries, the payload calibration on the Varnamo weighbridge, each rung of the ladder and
each rival the design note runs.

    load(target) -> Pack      the cleaned files
    golden(pk) -> dict        the golden model and every shortlisted duty's design-day energy
"""
import csv
import datetime as dt
import os
import re
from collections import defaultdict

import numpy as np
from openpyxl import load_workbook

DESIGN_T = -5.0
SHARE = 0.85
FILES = {
    "weighbridge": "weighbridge_varnamo_2024-11_2026-10.csv",
    "bev": "bev_daily_summary_2025-03_2026-10.csv",
    "tms": "tms_consignments_jonkoping_2025-2026.csv",
    "tmsv": "tms_consignments_varnamo_2025-11_2026-10.csv",
    "fleet": "fleet_register_2026.xlsx",
    "routes": "route_register_2026.xlsx",
    "plan": "fleet_plan_2027.xlsx",
    "temps": "daily_mean_temperature_2016-2026.csv",
}
LAST12 = (dt.date(2025, 11, 1), dt.date(2026, 10, 31))
USABLE = 540.0   # the quotation's usable battery, read into the checks from the PDF text (checks.py)
IN_SERVICE = dt.date(2025, 2, 17)   # the pilot tractors' in-service date (fleet register)
TRACTOR_2027_KG = 11980.0   # the quotation's unladen weight, read into the checks from the PDF text (checks.py)
TARE_REF = 19.0             # t: the tare term is centred here so the per-km level reads at an ordinary combination


def rd(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def kg(s):
    s = (s or "").strip()
    if not s:
        return None
    if s.endswith("t"):
        return float(s[:-1].strip().replace(",", ".")) * 1000
    return float(s.replace("kg", "").replace(" ", "").replace(",", "."))


class Pack:
    pass


def load(target):
    pk = Pack()
    F = {k: os.path.join(target, v) for k, v in FILES.items()}
    # route register: the duties and the routing tool's stop list
    wb = load_workbook(F["routes"], read_only=True)
    pk.routes = {}
    for r in list(wb["Duties"].iter_rows(values_only=True))[1:]:
        pk.routes[r[0]] = {"old": r[1], "depot": r[2], "shipper": r[3], "delivery": r[5], "legs": (r[6], r[7], r[8]),
                          "climb": r[10], "plan_h": float(r[12])}
    pk.stops = defaultdict(list)
    for r in list(wb["Stops"].iter_rows(values_only=True))[1:]:
        pk.stops[r[0]].append((r[2], float(r[3])))
    wb = load_workbook(F["plan"], read_only=True)
    pk.short = [r[0] for r in list(wb["Shortlist 2027"].iter_rows(values_only=True))[1:]]
    # fleet register: tractors' and trailers' tare, the trailers' body and equipment
    wb = load_workbook(F["fleet"], read_only=True)
    pk.tractor_tare = {r[1]: float(r[7]) for r in list(wb["Tractors"].iter_rows(values_only=True))[1:] if r[7]}
    pk.trailer = {}
    for r in list(wb["Trailers"].iter_rows(values_only=True))[1:]:
        pk.trailer[r[1]] = {"body": str(r[2]), "type": r[3], "equip": r[4] or "", "tare": float(r[7])}
    # weighbridge: the last weighing of each departure (a re-weigh after a reload replaces the first)
    last = {}
    for r in rd(F["weighbridge"]):
        k = r["cmr_no"]
        if k not in last or r["weighed_at"] >= last[k]["weighed_at"]:
            last[k] = r
    pk.wb = []
    for r in last.values():
        duty = r["duty"]
        if duty.startswith("VMO-"):
            duty = "V" + duty[4:]
        pk.wb.append({"date": dt.date.fromisoformat(r["weighed_at"][:10]), "duty": duty, "shipper": r["shipper"],
                      "declared": kg(r["declared_kg"]), "net": (float(r["gross_kg"]) - float(r["tare_kg"])),
                      "trailer": r["trailer_reg"]})
    pk.wb_raw_rows = sum(1 for _ in open(F["weighbridge"], encoding="utf-8")) - 1
    # station temperatures
    pk.station = {}
    for r in rd(F["temps"]):
        pk.station[(r["date"], r["station"])] = float(r["temperature (C)"])
    # TMS consignments: one note per drop, grouped to the vehicle's day
    tms = {}
    for r in rd(F["tms"]):
        k = (r["vehicle_reg"], r["collection_date"])
        t = tms.setdefault(k, {"duty": r["duty"], "shipper": r["shipper"], "trailer": r["trailer_reg"], "drops": []})
        t["drops"].append((r["delivery_town"], kg(r["declared_weight"])))
    # the Varnamo consignments: one departure is a duty's notes on one day
    pk.vdep = defaultdict(list)
    vd = {}
    for r in rd(F["tmsv"]):
        duty = "V" + r["duty"][4:] if r["duty"].startswith("VMO-") else r["duty"]
        vd.setdefault((duty, r["collection_date"]), {"trailer": r["trailer_reg"], "drops": []})["drops"].append(
            (r["delivery_town"], kg(r["declared_weight"])))
    for (duty, day), v in sorted(vd.items()):
        pk.vdep[duty].append(v)
    # battery-electric daily summaries: a day uploaded twice is one day
    seen = {}
    for r in rd(F["bev"]):
        k = (r["registration"], r["operating_date"])
        if k not in seen or r["uploaded_utc"] < seen[k]["uploaded_utc"]:
            seen[k] = r
    days = []
    for k, r in sorted(seen.items(), key=lambda kv: (kv[0][1], kv[0][0])):
        c = tms.get(k)
        if c is None:
            continue
        t = r["ambient_mean_c"]
        t0 = dt.datetime.fromisoformat(r["first_departure_utc"].replace("Z", ""))
        t1 = dt.datetime.fromisoformat(r["last_arrival_utc"].replace("Z", ""))
        tl = pk.trailer[c["trailer"]]
        days.append({"date": dt.date.fromisoformat(r["operating_date"]), "reg": r["registration"],
                     "duty": c["duty"], "shipper": c["shipper"], "declared": sum(x[1] for x in c["drops"]),
                     "drops": c["drops"], "trailer": c["trailer"],
                     "combo": (pk.tractor_tare[r["registration"]] + tl["tare"]) / 1000.0,
                     "epto": "ePTO" in tl["equip"], "reefer": tl["body"] == "04",
                     "km": float(r["distance_km"]), "kwh": float(r["energy_used_kwh"]),
                     "drive_h": float(r["driving_time_h"]), "span_h": (t1 - t0).total_seconds() / 3600.0,
                     "v": float(r["distance_km"]) / float(r["driving_time_h"]),
                     "t": float(t) if t else None, "station_t": pk.station[(r["operating_date"], "Jönköping")],
                     "soc0": float(r["soc_start_pct"]), "soc1": float(r["soc_end_pct"])})
    # an ambient sensor dropout takes the station's day, moved by the mean truck-against-station offset
    off = np.mean([d["t"] - d["station_t"] for d in days if d["t"] is not None])
    for d in days:
        d["t_filled"] = d["t"] if d["t"] is not None else d["station_t"] + off
    for d in days:
        d["cap"] = d["kwh"] / (d["soc0"] - d["soc1"]) * 100   # the battery's energy per full charge that day
        d["age"] = (d["date"] - IN_SERVICE).days / 365.25
        d["phi"] = phi_of(pk, d["duty"], d["drops"])
        d["phi_eq"] = phi_of(pk, d["duty"], d["drops"], equal=True)
        d["n_drops"] = len(d["drops"])
    pk.days = days
    pk.offset = float(off)
    return pk


def phi_of(pk, duty, drops, equal=False):
    """the share of the loaded run's km the departing load rides: each drop's declared share taken off at its stop's
    km on the routing tool's stop list"""
    st = dict(pk.stops[duty])
    L = float(pk.routes[duty]["legs"][1])
    tot = sum(x[1] for x in drops)
    pos = sorted(((st[t], w) for t, w in drops), key=lambda z: z[0])
    rem, prev, acc = 1.0, 0.0, 0.0
    for p, w in pos:
        acc += rem * (p - prev)
        rem -= (1.0 / len(pos)) if equal else w / tot
        prev = p
    return acc / L


# ---------------------------------------------------------------- the payload each pilot day carried

def ticket_months(pk, shipper):
    """the months in which a shipper's notes carry its own scale weight: nearly every departure's declaration equals
    the weighed load to the bridge's 20 kg"""
    cache = pk.__dict__.setdefault("_tickets", {})
    if shipper in cache:
        return cache[shipper]
    m = defaultdict(list)
    for r in pk.wb:
        if r["shipper"] == shipper and r["declared"] is not None:
            m[(r["date"].year, r["date"].month)].append(abs(r["declared"] - r["net"]) <= 20)
    cache[shipper] = {k for k, v in m.items() if np.mean(v) > 0.9}
    return cache[shipper]


def regime(pk, shipper, day):
    t = ticket_months(pk, shipper)
    if not t:
        return "all"
    return "ticket" if (day.year, day.month) in t else "note"


def calibration(pk, mode="shipper", window=None, split=True):
    """E[weighed net payload | declared, shipper] from the Varnamo weighbridge.
    mode shipper: a line per shipper (a constant declaration takes the shipper's mean weighed load);
    mode pooled: one line over every departure; mode mean: every load at its shipper's mean weighed load."""
    rows = [r for r in pk.wb if r["declared"] is not None and (window is None or window[0] <= r["date"] <= window[1])]
    by = defaultdict(list)
    for r in rows:
        key = (r["shipper"], regime(pk, r["shipper"], r["date"]) if split else "all")
        by[key].append((r["declared"], r["net"]))
    out = {}
    if mode == "pooled":
        D = np.array([r["declared"] for r in rows])
        W = np.array([r["net"] for r in rows])
        lam = np.cov(D, W)[0, 1] / np.var(D, ddof=1)
        for s in by:
            out[s] = (W.mean() - lam * D.mean(), lam)
        return out
    for s, v in by.items():
        D, W = map(np.array, zip(*v))
        if mode == "mean" or np.var(D) < 1e-6:
            out[s] = (W.mean(), 0.0)
        else:
            lam = np.cov(D, W)[0, 1] / np.var(D, ddof=1)
            out[s] = (W.mean() - lam * D.mean(), lam)
    return out


def error_model(pk, window=None):
    """each shipper's declaration error at each note period, from the Varnamo weighings: the variance of declared less
    weighed (additive) and of the same as a share of the weighed load (multiplicative)"""
    by = defaultdict(list)
    for r in pk.wb:
        if r["declared"] is None or (window is not None and not window[0] <= r["date"] <= window[1]):
            continue
        by[(r["shipper"], regime(pk, r["shipper"], r["date"]))].append((r["declared"], r["net"]))
    out = {}
    for k, v in by.items():
        D, W = map(np.array, zip(*v))
        out[k] = (float(np.var(D - W)), float(np.var((D - W) / W)))
    return out


def lane_payloads(pk, err="mult", window=None):
    """the load each pilot day carried, from its own duty's declarations: the shipper's declaration error (read on the
    Varnamo bridge) removed from the spread of the duty's own declared weights at that note period, each declaration
    taken to the expected load given it on that duty (the error carries from the bridge, the loads do not)"""
    em = error_model(pk, window)
    lane = defaultdict(list)
    for i, d in enumerate(pk.days):
        lane[(d["duty"], regime(pk, d["shipper"], d["date"]))].append(i)
    out = np.zeros(len(pk.days))
    for (duty, rg), idx in lane.items():
        D = np.array([pk.days[i]["declared"] for i in idx], float)
        m, v = D.mean(), D.var()
        ea, er = em[(pk.days[idx[0]]["shipper"], rg)]
        s2 = ea if err == "add" else er * np.mean(D ** 2) / (1 + er)
        lam = max(0.0, (v - s2) / v) if v > 0 else 0.0
        out[idx] = (m + lam * (D - m)) / 1000
    return out


def payloads(pk, how, split=True, window=None):
    """the payload (t) each pilot day carried, by the route's basis: lane (the golden), lane_add, shipper (the
    terminal's weighed-on-declared line per shipper and note period), pooled, mean, declared"""
    if how == "declared":
        return np.array([d["declared"] / 1000 for d in pk.days])
    if how in ("lane", "lane_add"):
        return lane_payloads(pk, "add" if how == "lane_add" else "mult", window)
    cal = calibration(pk, how, window, split)
    out = []
    for d in pk.days:
        k = (d["shipper"], regime(pk, d["shipper"], d["date"]) if split else "all")
        if how == "pooled":
            k = next(iter(cal))
        a, b = cal[k]
        out.append((a + b * d["declared"]) / 1000)
    return np.array(out)


# ---------------------------------------------------------------- the energy model

V_REF = 65.0
GOLD = {"form": ("hinge2", 16, 0), "temp": "truck", "speed": "sq", "vmode": "hinge10", "tare": "sep",
        "drops": "yes", "tru": None, "hours": "span"}


def opts(**kw):
    o = dict(GOLD)
    o.update(kw)
    return o


def speed_term(v, speed):
    """the energy model's speed column per km: air drag rising with the square of speed (sq), a straight line (lin),
    or none"""
    v = np.asarray(v, float)
    if speed == "sq":
        return [(v * v - V_REF ** 2) / 1000.0]
    if speed == "lin":
        return [v - V_REF]
    return []


def columns(tot, cl, T, v, lk, pay, ph, combo, flag, hours, o):
    """the model's columns, the same for a pilot day and a shortlisted duty's design day; returns (columns, index of
    the payload column)"""
    cols = [tot, tot * cl] + [tot * c for c in cold_terms(T, o["form"])] + [tot * c for c in speed_term(v, o["speed"])]
    tare = tot * (combo - TARE_REF)
    if o["tare"] == "sep":
        cols.append(tare)
    load = pay * lk * ph
    cols.append(load + tare if o["tare"] == "shared" else load)
    ip = len(cols) - 1
    if o["tru"]:
        cols.append(flag * hours)
    return cols, ip


def day_arrays(pk, o, pay):
    D = pk.days
    tot = np.array([d["km"] for d in D])
    lk = np.array([pk.routes[d["duty"]]["legs"][1] for d in D], float)
    cl = np.array([pk.routes[d["duty"]]["climb"] for d in D], float)
    T = np.array([d["t_filled"] if o["temp"] == "truck" else d["station_t"] for d in D])
    v = np.array([d["v"] for d in D])
    ph = np.array([{"yes": d["phi"], "no": 1.0, "equal": d["phi_eq"]}[o["drops"]] for d in D])
    combo = np.array([d["combo"] for d in D])
    flag = np.array([float(d["epto"] if o["tru"] == "epto" else d["reefer"]) for d in D])
    hours = np.array([{"span": d["span_h"], "drive": d["drive_h"], "km": d["km"]}[o["hours"]] for d in D])
    return tot, cl, T, v, lk, pay, ph, combo, flag, hours


def design(pk, pay, o=None, **kw):
    o = opts(**kw) if o is None else o
    cols, ip = columns(*day_arrays(pk, o, pay), o)
    return np.column_stack(cols)


def plan_speed(pk, duty):
    r = pk.routes[duty]
    return sum(r["legs"]) / r["plan_h"]


def speed_ratio(pk, t=DESIGN_T, how="hinge10"):
    """actual over planned speed, fitted on the pilot days against the day's temperature, read at t.
    how hinge10: a slope below 10 C; hinge8, hinge12; linear: on the temperature; bins: the mean of days within 2.5 C
    of t; mean: the year's mean ratio, whatever the weather; plan: the routing tool's speed as it stands (1.0)"""
    if how == "plan":
        return 1.0
    r = np.array([d["v"] / plan_speed(pk, d["duty"]) for d in pk.days])
    T = np.array([d["t_filled"] for d in pk.days])
    if how == "mean":
        return float(r.mean())
    if how == "bins":
        return float(r[np.abs(T - t) <= 2.5].mean())
    if how == "linear":
        b = np.polyfit(T, r, 1)
        return float(np.polyval(b, t))
    k = float(how[5:])
    X = np.column_stack([np.ones(len(T)), np.maximum(0, k - T)])
    c = np.linalg.lstsq(X, r, rcond=None)[0]
    return float(c[0] + c[1] * max(0.0, k - t))


def cold_terms(T, form):
    T = np.asarray(T, float)
    if form[0] == "hinge1":
        return [np.maximum(0, form[1] - T)]
    if form[0] == "linear":
        return [form[1] - T]
    if form[0] == "hinge2":
        return [np.maximum(0, form[1] - T), np.maximum(0, form[2] - T)]
    if form[0] == "quad":
        u = np.maximum(0, form[1] - T)
        return [u, u * u]
    if form[0] == "bins":
        edges = form[1]
        return [np.clip(edges[i] - T, 0, edges[i] - edges[i + 1] if i + 1 < len(edges) else 99)
                for i in range(len(edges))]
    raise ValueError(form)


def dwell(pk):
    """time at the collection and the drops (first departure to last arrival less driving), on the drops beyond the
    first: (base, per extra drop)"""
    n = np.array([d["n_drops"] - 1 for d in pk.days], float)
    s = np.array([d["span_h"] - d["drive_h"] for d in pk.days])
    b = np.polyfit(n, s, 1)
    return float(b[1]), float(b[0])


def fit(pk, pay, form=("hinge2", 16, 0), mask=None, temp="truck", speed="sq", vmode="hinge10", **kw):
    """vmode: how each shortlisted duty's speed on the design day is set (speed_ratio's how); kw: tare (sep, shared or
    None), drops (yes, no, equal), tru (epto, all or None), hours (span, drive, km)"""
    o = opts(form=form, temp=temp, speed=speed, vmode=vmode, **kw)
    cols, ip = columns(*day_arrays(pk, o, pay), o)
    X = np.column_stack(cols)
    y = np.array([d["kwh"] for d in pk.days])
    m = np.ones(len(y), bool) if mask is None else mask
    c, *_ = np.linalg.lstsq(X[m], y[m], rcond=None)
    resid = y[m] - X[m] @ c
    return {"coef": c, "form": o["form"], "speed": o["speed"], "vmode": o["vmode"], "o": o, "ip": ip,
            "dwell": dwell(pk), "rmse_pct": float(np.sqrt(np.mean((resid / y[m]) ** 2)) * 100)}


def duty_inputs(pk, c):
    """what a shortlisted duty brings to the design day: its trailers' mean tare with the 2027 tractor, the share of
    the loaded run its load rides (from its Varnamo notes and the routing tool's stops), and whether its trailers' unit
    runs from the tractor (ePTO) or is a reefer at all"""
    dd = [r for r in pk.wb if r["duty"] == c and LAST12[0] <= r["date"] <= LAST12[1]]
    combo = TRACTOR_2027_KG / 1000.0 + float(np.mean([pk.trailer[r["trailer"]]["tare"] for r in dd])) / 1000.0
    deps = pk.vdep[c]
    ph = float(np.mean([phi_of(pk, c, x["drops"]) for x in deps]))
    ph_eq = float(np.mean([phi_of(pk, c, x["drops"], equal=True) for x in deps]))
    epto = float(np.mean(["ePTO" in pk.trailer[x["trailer"]]["equip"] for x in deps]))
    reef = float(np.mean([pk.trailer[x["trailer"]]["body"] == "04" for x in deps]))
    return {"combo": combo, "phi": ph, "phi_eq": ph_eq, "epto": epto, "reefer": reef, "n_drops": len(pk.stops[c])}


def predict(model, legs, climb, load_t, t=DESIGN_T, v=V_REF, inp=None):
    o = model.get("o", GOLD)
    a, b, cc = legs
    tot = float(a + b + cc)
    inp = inp or {"combo": TARE_REF, "phi": 1.0, "phi_eq": 1.0, "epto": 0.0, "reefer": 0.0, "n_drops": 1}
    ph = {"yes": inp["phi"], "no": 1.0, "equal": inp["phi_eq"]}[o["drops"]]
    flag = inp["epto"] if o["tru"] == "epto" else inp["reefer"]
    d0, d1 = model.get("dwell", (0.0, 0.0))
    hours = {"span": tot / v + d0 + d1 * (inp["n_drops"] - 1), "drive": tot / v, "km": tot}[o["hours"]]
    cols, ip = columns(np.array([tot]), np.array([float(climb)]), np.array([t]), np.array([v]), np.array([float(b)]),
                       np.array([load_t]), np.array([ph]), np.array([inp["combo"]]), np.array([flag]),
                       np.array([hours]), o)
    return float(np.dot(model["coef"], np.array([float(np.ravel(x)[0]) for x in cols])))


# ---------------------------------------------------------------- the battery a 2027 tractor has after a year

FADE_TAUS = [round(0.08 + 0.02 * k, 2) for k in range(37)]


def _age_cols(age, how):
    """the age terms of each loss form, as (columns, function of one age)"""
    if how in ("cold", "linear", "quad", "cold15", "age", "first_year"):
        return [age], lambda a: np.array([a])
    if how == "sqrt":
        return [np.sqrt(age)], lambda a: np.array([np.sqrt(a)])
    if how == "sqrtlin":
        return [np.sqrt(age), age], lambda a: np.array([np.sqrt(a), a])
    if how == "loglin":
        return [np.log1p(age / 0.1), age], lambda a: np.array([np.log1p(a / 0.1), a])
    if how == "spline":
        kn = (0.25, 0.5, 1.0)
        return [age] + [np.maximum(0, age - k) for k in kn], lambda a: np.array([a] + [max(0.0, a - k) for k in kn])
    if how.startswith("exp"):
        t = float(how[3:])
        return [1 - np.exp(-age / t), age], lambda a: np.array([1 - np.exp(-a / t), a])
    raise ValueError(how)


def fade_fit(pk, how="curve", temp="cold"):
    """energy per full charge (energy used over the state of charge it took) on a level per tractor, an age form and
    the day's cold, which takes capacity for the day and gives it back. Returns (loss over the first twelve months as
    a share of the level at entry into service, residual sum of squares, parameters)."""
    cap = np.array([d["cap"] for d in pk.days])
    age = np.array([d["age"] for d in pk.days])
    T = np.array([d["t_filled"] for d in pk.days])
    regs = sorted({d["reg"] for d in pk.days})
    R = np.column_stack([[1.0 if d["reg"] == g else 0.0 for d in pk.days] for g in regs])
    if how == "curve":   # the early-life time scale chosen by the fit itself
        best = min(((fade_fit(pk, "exp%.2f" % t, temp)[1], t) for t in FADE_TAUS))
        return fade_fit(pk, "exp%.2f" % best[1], temp)
    m = np.ones(len(cap), bool) if how != "first_year" else age <= 1.0
    cols, f = _age_cols(age, how)
    tcols = {"cold": [np.maximum(0, 20 - T)], "cold15": [np.maximum(0, 15 - T)], "linear": [T], "quad": [T, T * T],
             "none": []}[temp]
    X = np.column_stack([R] + cols + tcols)[m]
    c = np.linalg.lstsq(X, cap[m], rcond=None)[0]
    r = cap[m] - X @ c
    lev = c[:len(regs)]
    if temp in ("linear", "quad"):   # the level at 20 C
        lev = lev + c[len(regs) + len(cols)] * 20 + (c[len(regs) + len(cols) + 1] * 400 if temp == "quad" else 0)
    k = c[len(regs):len(regs) + len(cols)]
    f0, f1 = f(0.0), f(1.0)
    loss = float(-(k @ f1 - k @ f0) / (lev.mean() + k @ f0))
    return loss, float(r @ r), how


def fade(pk, how="curve", temp="cold"):
    """the share of its usable energy a pilot battery permanently loses in its first twelve months in service.
    how curve (the golden): an early-life loss that settles over a time scale the fit chooses, then a steady loss;
    cold: a straight line in age (temperature below 20 C and a level per tractor beside it, the runs' fit); age: the
    straight line with no temperature term; first_year: the straight line on the first year's days; yoy: the same
    months a year apart; sqrt, sqrtlin, loglin, spline, expT: other curved forms; temp: the cold term's form"""
    if how == "yoy":
        cap = np.array([d["cap"] for d in pk.days])
        mo = np.array([d["date"].month for d in pk.days])
        yr = np.array([d["date"].year for d in pk.days])
        r = [cap[(yr == 2026) & (mo == m)].mean() / cap[(yr == 2025) & (mo == m)].mean() for m in range(3, 11)]
        return float(1 - np.mean(r))
    if how == "age":
        return fade_fit(pk, "cold", "none")[0]
    if how in ("linear", "quad", "cold15"):   # the straight line with another temperature term
        return fade_fit(pk, "cold", how)[0]
    return fade_fit(pk, how, temp)[0]


def fade_tau(pk):
    return float(fade_fit(pk, "curve")[2][3:])


def limit(pk, f=None):
    """FES-2 2.3 and 4.3: 85 per cent of the ordered model's usable battery less its first year's loss"""
    f = fade(pk) if f is None else f
    return SHARE * USABLE * (1 - f)


def planning_load(pk, duty, basis="net"):
    v = [r[basis] for r in pk.wb if r["duty"] == duty and LAST12[0] <= r["date"] <= LAST12[1] and r[basis] is not None]
    return float(np.mean(v)) / 1000


def assess(pk, model, basis="net", t=DESIGN_T, lim=None):
    lim = limit(pk) if lim is None else lim
    rr = speed_ratio(pk, t, model.get("vmode", "hinge10")) if model.get("speed") else 1.0
    cache = pk.__dict__.setdefault("_inp", {})
    out = {}
    for c in pk.short:
        r = pk.routes[c]
        if c not in cache:
            cache[c] = duty_inputs(pk, c)
        v = plan_speed(pk, c) * rr
        e = predict(model, r["legs"], r["climb"], planning_load(pk, c, basis), t, v, cache[c])
        out[c] = {"kwh": e, "go": e <= lim}
    return out


def chosen(a):
    return sorted(c for c, v in a.items() if v["go"])


H2 = ("hinge2", 16, 0)   # the golden cold form: a rate below 16 C and a further rate below 0 C
H1 = ("hinge1", 16)      # the field's degree-day form: one rate below 16 C


def rung0(pk, lim=None):
    """the pilot's average consumption on January-like days (ambient -8 to -2 C), times each duty's route km"""
    v = [d["kwh"] / d["km"] for d in pk.days if -8 <= d["t_filled"] <= -2]
    rate = float(np.mean(v))
    lim = SHARE * USABLE if lim is None else lim
    out = {}
    for c in pk.short:
        e = rate * sum(pk.routes[c]["legs"])
        out[c] = {"kwh": e, "go": e <= lim}
    return out, rate


def pilot_pooled(pk):
    """one weighed-on-declared line over the weighbridge departures of the pilot's own shippers"""
    ps = {d["shipper"] for d in pk.days}
    rows = [r for r in pk.wb if r["declared"] is not None and r["shipper"] in ps]
    D = np.array([r["declared"] for r in rows])
    W = np.array([r["net"] for r in rows])
    lam = np.cov(D, W)[0, 1] / np.var(D, ddof=1)
    return np.array([(W.mean() + lam * (d["declared"] - D.mean())) / 1000 for d in pk.days])


def backtest(pk, pay, form, months=((2026, 1), (2026, 2))):
    """fit without the held-out months, forecast their working days: mean error in per cent on the days below 0 C"""
    ho = np.array([(d["date"].year, d["date"].month) in months for d in pk.days])
    sub = np.array([d["t_filled"] < 0 for d in pk.days])
    m = fit(pk, pay, form, mask=~ho)
    X = design(pk, pay, m["o"])
    y = np.array([d["kwh"] for d in pk.days])
    e = (X @ m["coef"] - y) / y
    return float(100 * e[ho & sub].mean()), float(100 * e[ho].mean())


def careful_payloads(pk):
    """the runs' payload: each pilot declaration taken to the weighed load it stands for on the terminal's
    weighed-on-declared line for its shipper and note period"""
    return payloads(pk, "shipper")


def careful_fade(pk):
    """the runs' loss: a straight line in age beside a level per tractor and the day's cold"""
    return fade(pk, "cold")


def routes(pk):
    """each pass's and each shortcut's committed answer, (model, limit): the golden, the careful but hurried pass (the
    union of the recorded runs' methods), that pass with each one step done right (the hints), and each shortcut with
    every other step done the golden's way"""
    gp, cp, dp = payloads(pk, "lane"), careful_payloads(pk), payloads(pk, "declared")
    L = limit(pk)
    Lc = limit(pk, careful_fade(pk))
    return {
        "golden": (fit(pk, gp, H2), L),
        "careful but hurried": (fit(pk, cp, H2, vmode="mean"), Lc),
        "careful, design-day speed": (fit(pk, cp, H2), Lc),
        "careful, own-duty loads": (fit(pk, gp, H2, vmode="mean"), Lc),
        "careful, curved loss": (fit(pk, cp, H2, vmode="mean"), L),
        "the terminal's calibration line": (fit(pk, cp, H2), L),
        "declared weights": (fit(pk, dp, H2), L),
        "one pooled correction": (fit(pk, payloads(pk, "pooled"), H2), L),
        "a straight-line loss": (fit(pk, gp, H2), Lc),
        "the same months a year apart": (fit(pk, gp, H2), limit(pk, fade(pk, "yoy"))),
        "no first-year loss": (fit(pk, gp, H2), SHARE * USABLE),
        "the year's mean speed ratio": (fit(pk, gp, H2, vmode="mean"), L),
        "the routing tool's speed": (fit(pk, gp, H2, vmode="plan"), L),
        "no speed term": (fit(pk, gp, H2, speed=None), L),
        "one cold rate": (fit(pk, gp, H1), L),
        "no trailer weight": (fit(pk, gp, H2, tare=None), L),
        "the load to the last drop": (fit(pk, gp, H2, drops="no"), L),
    }


def models(pk):
    gp = payloads(pk, "lane")
    return {
        "golden": fit(pk, gp, H2),
        "naive": fit(pk, payloads(pk, "declared"), H2),
        "careful": fit(pk, careful_payloads(pk), H2, vmode="mean"),
        "golden_1h": fit(pk, gp, H1),
        "no_speed": fit(pk, gp, H2, speed=None),
    }


def golden(pk):
    M = models(pk)
    f = fade(pk)
    lim = limit(pk, f)
    a = assess(pk, M["golden"], lim=lim)
    m = M["golden"]
    return {"model": m, "assess": a, "set": chosen(a), "count": len(chosen(a)), "models": M,
            "fade": f, "limit": lim, "usable_y1": USABLE * (1 - f), "inputs": dict(pk._inp),
            "tare_term": float(m["coef"][m["ip"] - 1] * 100), "tau": fade_tau(pk),
            "pilot_combo": float(np.mean([d["combo"] for d in pk.days]))}


def _fe_design(pk, pay, form=("hinge2", 16, 0)):
    o = opts(form=form)
    tot, cl, T, v, lk, pay_, ph, combo, flag, hours = day_arrays(pk, o, pay)
    duties = sorted({d["duty"] for d in pk.days})
    du = np.array([d["duty"] for d in pk.days])
    cm = np.array([combo[du == d].mean() for d in du])
    X = np.column_stack([tot * (du == k) for k in duties] + [tot * c for c in cold_terms(T, form)]
                        + [tot * c for c in speed_term(v, "sq")] + [tot * (combo - cm)] + [pay * lk * ph])
    return X, duties, du, combo, o


def fe_slope_se(pk, pay):
    """the within-duty fit's payload slope and its standard error (per 100 km)"""
    X, duties, du, combo, o = _fe_design(pk, pay)
    y = np.array([d["kwh"] for d in pk.days])
    c, *_ = np.linalg.lstsq(X, y, rcond=None)
    r = y - X @ c
    cov = r @ r / (len(y) - X.shape[1]) * np.linalg.inv(X.T @ X)
    k = X.shape[1] - 1
    return float(c[k] * 100), float(np.sqrt(cov[k, k]) * 100)


def golden_se(pk, pay):
    """the golden fit's payload slope standard error (per 100 km)"""
    m = fit(pk, pay, H2)
    X = design(pk, pay, m["o"])
    y = np.array([d["kwh"] for d in pk.days])
    r = y - X @ m["coef"]
    cov = r @ r / (len(y) - X.shape[1]) * np.linalg.inv(X.T @ X)
    return float(np.sqrt(cov[m["ip"], m["ip"]]) * 100)


def slope_per_100(model):
    return float(model["coef"][model.get("ip", -1)] * 100)


def fit_fe(pk, pay, form=("hinge2", 16, 0)):
    """within-duty fit (a level per duty for each km), the duty levels then explained by climb and the duty's mean
    combination tare"""
    X, duties, du, combo, o = _fe_design(pk, pay, form)
    y = np.array([d["kwh"] for d in pk.days])
    c, *_ = np.linalg.lstsq(X, y, rcond=None)
    lev = c[:len(duties)]
    cl_d = np.array([pk.routes[k]["climb"] for k in duties], float)
    cb_d = np.array([combo[du == k].mean() - TARE_REF for k in duties])
    Z = np.column_stack([np.ones(len(duties)), cl_d, cb_d])
    a = np.linalg.lstsq(Z, lev, rcond=None)[0]
    rest = c[len(duties):]
    nc = len(cold_terms([0.0], form))
    coef = np.concatenate([[a[0], a[1]], rest[:nc + 1], [a[2]], rest[nc + 2:]])
    return {"coef": coef, "form": form, "speed": "sq", "vmode": "hinge10", "o": o, "ip": 2 + nc + 1 + 1,
            "dwell": dwell(pk), "rmse_pct": None}


LOSS_RIVALS = ("sqrt", "sqrtlin", "loglin", "spline", "exp0.20", "exp0.45")


def rivals(pk):
    """every route that takes all the steps, each (model, limit); the golden's call must hold under all of them"""
    gp = payloads(pk, "lane")
    lim = limit(pk)
    y25 = np.array([d["date"].year == 2025 for d in pk.days])
    out = {
        "golden": (fit(pk, gp, H2), lim),
        "station temperature": (fit(pk, gp, H2, temp="station"), lim),
        "2025 only": (fit(pk, gp, H2, mask=y25), lim),
        "2026 only": (fit(pk, gp, H2, mask=~y25), lim),
        "hinges 14 and 0": (fit(pk, gp, ("hinge2", 14, 0)), lim),
        "hinges 18 and 0": (fit(pk, gp, ("hinge2", 18, 0)), lim),
        "hinges 16 and -2": (fit(pk, gp, ("hinge2", 16, -2)), lim),
        "hinges 16 and 2": (fit(pk, gp, ("hinge2", 16, 2)), lim),
        "quadratic below 16": (fit(pk, gp, ("quad", 16)), lim),
        "bins at 16, 8, 0, -8": (fit(pk, gp, ("bins", [16, 8, 0, -8])), lim),
        "loads: additive declaration error": (fit(pk, payloads(pk, "lane_add"), H2), lim),
        "loads: error read on the last 12 months": (fit(pk, payloads(pk, "lane", window=LAST12), H2), lim),
        "loads: each day at its duty's mean declared": (fit(pk, lane_mean(pk), H2), lim),
        "within-duty fit": (fit_fe(pk, gp), lim),
        "speed: a straight line": (fit(pk, gp, H2, speed="lin"), lim),
        "speed ratio: slope below 8 C": (fit(pk, gp, H2, vmode="hinge8"), lim),
        "speed ratio: slope below 12 C": (fit(pk, gp, H2, vmode="hinge12"), lim),
        "speed ratio: on the temperature": (fit(pk, gp, H2, vmode="linear"), lim),
        "speed ratio: days within 2.5 C": (fit(pk, gp, H2, vmode="bins"), lim),
        "tare: one coefficient with the payload": (fit(pk, gp, H2, tare="shared"), lim),
        "drops: equal shares": (fit(pk, gp, H2, drops="equal"), lim),
        "loss: the day's temperature": (fit(pk, gp, H2), limit(pk, fade(pk, "curve", "linear"))),
        "loss: degrees below 15 C": (fit(pk, gp, H2), limit(pk, fade(pk, "curve", "cold15"))),
        "loss: a straight line on the first year's days": (fit(pk, gp, H2), limit(pk, fade(pk, "first_year"))),
    }
    for h in LOSS_RIVALS:
        out["loss: %s" % h] = (fit(pk, gp, H2), limit(pk, fade(pk, h)))
    return out


def lane_mean(pk):
    """every pilot day at its duty's mean declared weight in its note period"""
    lane = defaultdict(list)
    for i, d in enumerate(pk.days):
        lane[(d["duty"], regime(pk, d["shipper"], d["date"]))].append(i)
    out = np.zeros(len(pk.days))
    for k, idx in lane.items():
        out[idx] = np.mean([pk.days[i]["declared"] for i in idx]) / 1000
    out[[i for i, d in enumerate(pk.days) if regime(pk, d["shipper"], d["date"]) == "ticket"]] = \
        [d["declared"] / 1000 for d in pk.days if regime(pk, d["shipper"], d["date"]) == "ticket"]
    return out
