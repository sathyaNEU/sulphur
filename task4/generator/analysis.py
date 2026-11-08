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
    "routes": "route_register_2026.xlsx",
    "plan": "fleet_plan_2027.xlsx",
    "temps": "daily_mean_temperature_2016-2026.csv",
}
LAST12 = (dt.date(2025, 11, 1), dt.date(2026, 10, 31))
USABLE = 540.0   # the quotation's usable battery, read into the checks from the PDF text (checks.py)


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
    # route register
    wb = load_workbook(F["routes"], read_only=True)
    pk.routes = {}
    for r in list(wb["Duties"].iter_rows(values_only=True))[1:]:
        pk.routes[r[0]] = {"old": r[1], "depot": r[2], "shipper": r[3], "delivery": r[5], "legs": (r[6], r[7], r[8]),
                          "climb": r[10]}
    wb = load_workbook(F["plan"], read_only=True)
    pk.short = [r[0] for r in list(wb["Shortlist 2027"].iter_rows(values_only=True))[1:]]
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
                      "declared": kg(r["declared_kg"]), "net": (float(r["gross_kg"]) - float(r["tare_kg"]))})
    pk.wb_raw_rows = sum(1 for _ in open(F["weighbridge"], encoding="utf-8")) - 1
    # station temperatures
    pk.station = {}
    for r in rd(F["temps"]):
        pk.station[(r["date"], r["station"])] = float(r["temperature (C)"])
    # TMS consignments keyed by vehicle and day
    tms = {}
    for r in rd(F["tms"]):
        tms[(r["vehicle_reg"], r["collection_date"])] = r
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
        days.append({"date": dt.date.fromisoformat(r["operating_date"]), "reg": r["registration"],
                     "duty": c["duty"], "shipper": c["shipper"], "declared": kg(c["declared_weight"]),
                     "km": float(r["distance_km"]), "kwh": float(r["energy_used_kwh"]),
                     "t": float(t) if t else None, "station_t": pk.station[(r["operating_date"], "Jönköping")]})
    # an ambient sensor dropout takes the station's day, moved by the mean truck-against-station offset
    off = np.mean([d["t"] - d["station_t"] for d in days if d["t"] is not None])
    for d in days:
        d["t_filled"] = d["t"] if d["t"] is not None else d["station_t"] + off
    pk.days = days
    pk.offset = float(off)
    return pk


# ---------------------------------------------------------------- the payload each pilot day carried

def calibration(pk, mode="shipper", window=None):
    """E[weighed net payload | declared, shipper] from the Varnamo weighbridge.
    mode shipper: a line per shipper (a constant declaration takes the shipper's mean weighed load);
    mode pooled: one line over every departure; mode mean: every load at its shipper's mean weighed load."""
    rows = [r for r in pk.wb if r["declared"] is not None and (window is None or window[0] <= r["date"] <= window[1])]
    by = defaultdict(list)
    for r in rows:
        by[r["shipper"]].append((r["declared"], r["net"]))
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


def payloads(pk, how):
    """the payload (t) each pilot day carried, by the rung's basis"""
    if how == "declared":
        return np.array([d["declared"] / 1000 for d in pk.days])
    cal = calibration(pk, how)
    return np.array([(cal[d["shipper"]][0] + cal[d["shipper"]][1] * d["declared"]) / 1000 for d in pk.days])


# ---------------------------------------------------------------- the energy model

def design(pk, pay, form=("hinge2", 16, 0), temp="truck"):
    tot = np.array([d["km"] for d in pk.days])
    lk = np.array([pk.routes[d["duty"]]["legs"][1] for d in pk.days], float)
    cl = np.array([pk.routes[d["duty"]]["climb"] for d in pk.days], float)
    T = np.array([d["t_filled"] if temp == "truck" else d["station_t"] for d in pk.days])
    cols = [tot, tot * cl] + [tot * c for c in cold_terms(T, form)] + [pay * lk]
    return np.column_stack(cols)


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


def fit(pk, pay, form=("hinge2", 16, 0), mask=None, temp="truck"):
    X = design(pk, pay, form, temp)
    y = np.array([d["kwh"] for d in pk.days])
    m = np.ones(len(y), bool) if mask is None else mask
    c, *_ = np.linalg.lstsq(X[m], y[m], rcond=None)
    resid = y[m] - X[m] @ c
    return {"coef": c, "form": form, "rmse_pct": float(np.sqrt(np.mean((resid / y[m]) ** 2)) * 100)}


def predict(model, legs, climb, load_t, t=DESIGN_T):
    c, form = model["coef"], model["form"]
    a, b, cc = legs
    tot = a + b + cc
    terms = [tot, tot * climb] + [tot * float(np.ravel(x)[0]) for x in cold_terms([t], form)] + [load_t * b]
    return float(np.dot(c, terms))


def planning_load(pk, duty, basis="net"):
    v = [r[basis] for r in pk.wb if r["duty"] == duty and LAST12[0] <= r["date"] <= LAST12[1] and r[basis] is not None]
    return float(np.mean(v)) / 1000


def assess(pk, model, basis="net", t=DESIGN_T):
    out = {}
    for c in pk.short:
        r = pk.routes[c]
        e = predict(model, r["legs"], r["climb"], planning_load(pk, c, basis), t)
        out[c] = {"kwh": e, "go": e <= SHARE * USABLE}
    return out


def chosen(a):
    return sorted(c for c, v in a.items() if v["go"])


def rung0(pk):
    """the pilot's average consumption on January-like days (ambient -8 to -2 C), times each duty's route km"""
    v = [d["kwh"] / d["km"] for d in pk.days if -8 <= d["t_filled"] <= -2]
    rate = float(np.mean(v))
    out = {}
    for c in pk.short:
        e = rate * sum(pk.routes[c]["legs"])
        out[c] = {"kwh": e, "go": e <= SHARE * USABLE}
    return out, rate


def pilot_pooled(pk):
    """one weighed-on-declared line over the weighbridge departures of the pilot's own shippers"""
    ps = {d["shipper"] for d in pk.days}
    rows = [r for r in pk.wb if r["declared"] is not None and r["shipper"] in ps]
    D = np.array([r["declared"] for r in rows])
    W = np.array([r["net"] for r in rows])
    lam = np.cov(D, W)[0, 1] / np.var(D, ddof=1)
    return np.array([(W.mean() + lam * (d["declared"] - D.mean())) / 1000 for d in pk.days])


def models(pk):
    """the golden model and every rung's"""
    return {
        "naive": fit(pk, payloads(pk, "declared")),
        "pooled": fit(pk, payloads(pk, "pooled")),
        "pilot_pooled": fit(pk, pilot_pooled(pk)),
        "golden": fit(pk, payloads(pk, "shipper")),
        "golden_1h": fit(pk, payloads(pk, "shipper"), ("hinge1", 16)),
        "naive_1h": fit(pk, payloads(pk, "declared"), ("hinge1", 16)),
    }


def golden(pk):
    M = models(pk)
    a = assess(pk, M["golden"])
    return {"model": M["golden"], "assess": a, "set": chosen(a), "count": len(chosen(a)), "models": M}


def slope_per_100(model):
    return float(model["coef"][-1] * 100)


def fit_fe(pk, pay, form=("hinge2", 16, 0)):
    """within-duty fit (a level per duty for each km), the duty levels then explained by climb"""
    duties = sorted({d["duty"] for d in pk.days})
    tot = np.array([d["km"] for d in pk.days])
    lk = np.array([pk.routes[d["duty"]]["legs"][1] for d in pk.days], float)
    T = np.array([d["t_filled"] for d in pk.days])
    du = np.array([d["duty"] for d in pk.days])
    X = np.column_stack([tot * (du == k) for k in duties] + [tot * c for c in cold_terms(T, form)] + [pay * lk])
    y = np.array([d["kwh"] for d in pk.days])
    c, *_ = np.linalg.lstsq(X, y, rcond=None)
    lev = c[:len(duties)]
    cl = np.array([pk.routes[k]["climb"] for k in duties], float)
    a, b = np.polyfit(cl, lev, 1)[::-1]
    return {"coef": np.concatenate([[a, b], c[len(duties):]]), "form": form, "rmse_pct": None}


def fit_exact_slope(pk, form=("hinge2", 16, 0)):
    """the payload slope from the one pilot shipper whose declarations the weighbridge shows exact, the rest of the
    model refitted with that slope held"""
    cal = calibration(pk)
    exact = {s for s, v in cal.items() if abs(v[1] - 1) < 0.02 and abs(v[0]) < 100}
    dec = np.array([d["declared"] / 1000 for d in pk.days])
    m = np.array([d["shipper"] in exact for d in pk.days])
    tot = np.array([d["km"] for d in pk.days])
    lk = np.array([pk.routes[d["duty"]]["legs"][1] for d in pk.days], float)
    T = np.array([d["t_filled"] for d in pk.days])
    y = np.array([d["kwh"] for d in pk.days])
    Xe = np.column_stack([tot, *[tot * c for c in cold_terms(T, form)], dec * lk])[m]
    b = np.linalg.lstsq(Xe, y[m], rcond=None)[0][-1]
    pay = payloads(pk, "shipper")
    X = design(pk, pay, form)[:, :-1]
    c = np.linalg.lstsq(X, y - b * pay * lk, rcond=None)[0]
    return {"coef": np.concatenate([c, [b]]), "form": form, "rmse_pct": None}


def rivals(pk):
    """every route that takes the deep step, each a model; the golden's call must hold under all of them"""
    gp = payloads(pk, "shipper")
    y25 = np.array([d["date"].year == 2025 for d in pk.days])
    R = {
        "golden": fit(pk, gp),
        "station temperature": fit(pk, gp, temp="station"),
        "2025 only": fit(pk, gp, mask=y25),
        "2026 only": fit(pk, gp, mask=~y25),
        "hinges 14 and 0": fit(pk, gp, ("hinge2", 14, 0)),
        "hinges 18 and 0": fit(pk, gp, ("hinge2", 18, 0)),
        "hinges 16 and -2": fit(pk, gp, ("hinge2", 16, -2)),
        "hinges 16 and 2": fit(pk, gp, ("hinge2", 16, 2)),
        "quadratic below 16": fit(pk, gp, ("quad", 16)),
        "bins at 16, 8, 0, -8": fit(pk, gp, ("bins", [16, 8, 0, -8])),
        "calibrated on the last 12 months": fit(pk, np.array([(c[0] + c[1] * d["declared"]) / 1000 for d in pk.days
                                                               for c in [calibration(pk, "shipper", LAST12)[d["shipper"]]]])),
        "each load at its shipper's mean": fit(pk, payloads(pk, "mean")),
        "within-duty fit": fit_fe(pk, gp),
        "slope from the exact shipper": fit_exact_slope(pk),
    }
    return R
