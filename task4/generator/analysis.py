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
IN_SERVICE = dt.date(2025, 2, 17)   # the pilot tractors' in-service date (fleet register)


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
                          "climb": r[10], "plan_h": float(r[12])}
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
    pk.days = days
    pk.offset = float(off)
    return pk


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


def payloads(pk, how, split=True, window=None):
    """the payload (t) each pilot day carried, by the route's basis"""
    if how == "declared":
        return np.array([d["declared"] / 1000 for d in pk.days])
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


def speed_term(v, speed):
    """the energy model's speed column per km: air drag rising with the square of speed (sq), a straight line (lin),
    or none"""
    v = np.asarray(v, float)
    if speed == "sq":
        return [(v * v - V_REF ** 2) / 1000.0]
    if speed == "lin":
        return [v - V_REF]
    return []


def design(pk, pay, form=("hinge2", 16, 0), temp="truck", speed="sq"):
    tot = np.array([d["km"] for d in pk.days])
    lk = np.array([pk.routes[d["duty"]]["legs"][1] for d in pk.days], float)
    cl = np.array([pk.routes[d["duty"]]["climb"] for d in pk.days], float)
    T = np.array([d["t_filled"] if temp == "truck" else d["station_t"] for d in pk.days])
    v = np.array([d["v"] for d in pk.days])
    cols = ([tot, tot * cl] + [tot * c for c in cold_terms(T, form)] + [tot * c for c in speed_term(v, speed)]
            + [pay * lk])
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


def fit(pk, pay, form=("hinge2", 16, 0), mask=None, temp="truck", speed="sq", vmode="hinge10"):
    """vmode: how each shortlisted duty's speed on the design day is set (speed_ratio's how)"""
    X = design(pk, pay, form, temp, speed)
    y = np.array([d["kwh"] for d in pk.days])
    m = np.ones(len(y), bool) if mask is None else mask
    c, *_ = np.linalg.lstsq(X[m], y[m], rcond=None)
    resid = y[m] - X[m] @ c
    return {"coef": c, "form": form, "speed": speed, "vmode": vmode,
            "rmse_pct": float(np.sqrt(np.mean((resid / y[m]) ** 2)) * 100)}


def predict(model, legs, climb, load_t, t=DESIGN_T, v=V_REF):
    c, form = model["coef"], model["form"]
    a, b, cc = legs
    tot = a + b + cc
    terms = ([tot, tot * climb] + [tot * float(np.ravel(x)[0]) for x in cold_terms([t], form)]
             + [tot * float(np.ravel(x)[0]) for x in speed_term([v], model.get("speed"))] + [load_t * b])
    return float(np.dot(c, terms))


# ---------------------------------------------------------------- the battery a 2027 tractor has after a year

def fade(pk, how="cold"):
    """the share of its capacity a pilot battery permanently loses in a year in service, from each day's energy per
    full charge (energy used over the state of charge it took): a level per tractor, a slope on age, and the day's
    cold, which takes capacity for the day and gives it back.
    how cold: degrees below 20 C on the day; linear: the day's temperature; age: age alone; yoy: the same months a year
    apart; quad: temperature and its square"""
    cap = np.array([d["cap"] for d in pk.days])
    age = np.array([d["age"] for d in pk.days])
    T = np.array([d["t_filled"] for d in pk.days])
    regs = sorted({d["reg"] for d in pk.days})
    R = np.column_stack([[1.0 if d["reg"] == g else 0.0 for d in pk.days] for g in regs])
    if how == "yoy":
        mo = np.array([d["date"].month for d in pk.days])
        yr = np.array([d["date"].year for d in pk.days])
        r = [cap[(yr == 2026) & (mo == m)].mean() / cap[(yr == 2025) & (mo == m)].mean() for m in range(3, 11)]
        return float(1 - np.mean(r))
    extra = {"cold": [np.maximum(0, 20 - T)], "cold15": [np.maximum(0, 15 - T)], "linear": [T], "quad": [T, T * T],
             "age": []}[how]
    X = np.column_stack([R, age] + extra)
    c = np.linalg.lstsq(X, cap, rcond=None)[0]
    lev = c[:len(regs)]
    if how in ("linear", "quad"):   # the level at 20 C
        lev = lev + c[len(regs) + 1] * 20 + (c[len(regs) + 2] * 400 if how == "quad" else 0)
    return float(-c[len(regs)] / lev.mean())


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
    out = {}
    for c in pk.short:
        r = pk.routes[c]
        v = plan_speed(pk, c) * rr
        e = predict(model, r["legs"], r["climb"], planning_load(pk, c, basis), t, v)
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
    X = design(pk, pay, form)
    y = np.array([d["kwh"] for d in pk.days])
    e = (X @ m["coef"] - y) / y
    return float(100 * e[ho & sub].mean()), float(100 * e[ho].mean())


def routes(pk):
    """each shortcut's committed answer: (model, limit) for the golden and every hurried route effort.json records"""
    gp, dp = payloads(pk, "shipper"), payloads(pk, "declared")
    f, fa = fade(pk), fade(pk, "age")
    L = limit(pk, f)
    return {
        "golden": (fit(pk, gp, H2), L),
        "no speed term": (fit(pk, gp, H2, speed=None), L),
        "the routing tool's speed": (fit(pk, gp, H2, vmode="plan"), L),
        "the year's mean speed ratio": (fit(pk, gp, H2, vmode="mean"), L),
        "declared weights": (fit(pk, dp, H2), L),
        "one pooled correction": (fit(pk, payloads(pk, "pooled"), H2), L),
        "one line over the pilot shippers": (fit(pk, pilot_pooled(pk), H2), L),
        "one cold rate": (fit(pk, gp, H1), L),
        "no first-year loss": (fit(pk, gp, H2), SHARE * USABLE),
        "careful but hurried": (fit(pk, gp, H2, speed=None), L),
        "the arch 6 golden": (fit(pk, gp, H2, speed=None), L),
    }


def models(pk):
    gp, dp = payloads(pk, "shipper"), payloads(pk, "declared")
    return {
        "naive": fit(pk, dp, H2),
        "pooled": fit(pk, payloads(pk, "pooled"), H2),
        "pilot_pooled": fit(pk, pilot_pooled(pk), H2),
        "golden": fit(pk, gp, H2),
        "golden_1h": fit(pk, gp, H1),
        "naive_1h": fit(pk, dp, H1),
        "no_speed": fit(pk, gp, H2, speed=None),
    }


def golden(pk):
    M = models(pk)
    f = fade(pk)
    lim = limit(pk, f)
    a = assess(pk, M["golden"], lim=lim)
    return {"model": M["golden"], "assess": a, "set": chosen(a), "count": len(chosen(a)), "models": M,
            "fade": f, "limit": lim, "usable_y1": USABLE * (1 - f)}


def slope_per_100(model):
    return float(model["coef"][-1] * 100)


def fit_fe(pk, pay, form=("hinge2", 16, 0)):
    """within-duty fit (a level per duty for each km), the duty levels then explained by climb"""
    duties = sorted({d["duty"] for d in pk.days})
    tot = np.array([d["km"] for d in pk.days])
    lk = np.array([pk.routes[d["duty"]]["legs"][1] for d in pk.days], float)
    T = np.array([d["t_filled"] for d in pk.days])
    v = np.array([d["v"] for d in pk.days])
    du = np.array([d["duty"] for d in pk.days])
    X = np.column_stack([tot * (du == k) for k in duties] + [tot * c for c in cold_terms(T, form)]
                        + [tot * c for c in speed_term(v, "sq")] + [pay * lk])
    y = np.array([d["kwh"] for d in pk.days])
    c, *_ = np.linalg.lstsq(X, y, rcond=None)
    lev = c[:len(duties)]
    cl = np.array([pk.routes[k]["climb"] for k in duties], float)
    a, b = np.polyfit(cl, lev, 1)[::-1]
    return {"coef": np.concatenate([[a, b], c[len(duties):]]), "form": form, "speed": "sq", "vmode": "hinge10",
            "rmse_pct": None}


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
    """every route that takes all three steps, each (model, limit); the golden's call must hold under all of them"""
    gp = payloads(pk, "shipper")
    lim = limit(pk)
    y25 = np.array([d["date"].year == 2025 for d in pk.days])
    return {
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
        "calibrated on the last 12 months": (fit(pk, payloads(pk, "shipper", window=LAST12), H2), lim),
        "each load at its shipper's mean": (fit(pk, payloads(pk, "mean"), H2), lim),
        "one shipper line over both note periods": (fit(pk, payloads(pk, "shipper", split=False), H2), lim),
        "within-duty fit": (fit_fe(pk, gp), lim),
        "loss: the day's temperature": (fit(pk, gp, H2), limit(pk, fade(pk, "linear"))),
        "loss: temperature and its square": (fit(pk, gp, H2), limit(pk, fade(pk, "quad"))),
        "loss: degrees below 15 C": (fit(pk, gp, H2), limit(pk, fade(pk, "cold15"))),
        "loss: the same months a year apart": (fit(pk, gp, H2), limit(pk, fade(pk, "yoy"))),
        "speed: a straight line": (fit(pk, gp, H2, speed="lin"), lim),
        "speed ratio: slope below 8 C": (fit(pk, gp, H2, vmode="hinge8"), lim),
        "speed ratio: slope below 12 C": (fit(pk, gp, H2, vmode="hinge12"), lim),
        "speed ratio: on the temperature": (fit(pk, gp, H2, vmode="linear"), lim),
        "speed ratio: days within 2.5 C": (fit(pk, gp, H2, vmode="bins"), lim),
    }
