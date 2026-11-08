"""task7: the golden, computed from the shipped files under target/ and nothing else, so every figure is what the
pack forces. Also the ladder's rungs and the rival family, on the same cleaned tables (checks.py asserts them)."""
import csv
import datetime as dt
import math
import os
from collections import defaultdict

import numpy as np

MASTER_PD = {1: 0.0021, 2: 0.0042, 3: 0.0075, 4: 0.0125, 5: 0.0216, 6: 0.0374, 7: 0.0664, 8: 0.1328}
H = 0.22
REPORT = dt.date(2026, 12, 31)
AS_IF = dt.date(2027, 1, 1)
TRADING = "Owner-occupied"
BOOK_CODE = {"INV": "Investment", "OWN": "Owner-occupied"}
BASIS = {"FULL": "INSPECTION", "INSPECTION": "INSPECTION", "IDX": "INDEX ROLL-FORWARD",
         "INDEX ROLL-FORWARD": "INDEX ROLL-FORWARD"}


def D(s):
    return dt.date(int(s[:4]), int(s[5:7]), int(s[8:10]))


def rows(target, name):
    with open(os.path.join(target, name), newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


class Tables:
    pass


def load(target):
    T = Tables()
    # valuation history: exact repeats dropped, zero-length corrections dropped, legacy codes mapped, the row in
    # force on a date read from the effective and expiry dates (the current flag is not trusted)
    seen, val = set(), defaultdict(list)
    for r in rows(target, "dw_dim_property_valuation_2004_2026.csv"):
        k = tuple(r.values())
        if k in seen:
            continue
        seen.add(k)
        eff, exp = D(r["row_effective_date"]), D(r["row_expiry_date"])
        if exp < eff:
            continue
        val[r["property_id"]].append(dict(eff=eff, exp=exp, basis=BASIS[r["valuation_basis"]],
                                          vdate=D(r["valuation_date"]), value=float(r["market_value_eur"]),
                                          series=r["index_series"]))
    for p in val:
        val[p].sort(key=lambda x: (x["eff"], x["vdate"]))
    T.val = val
    # facilities: the crosswalk from legacy numbers, the month-end fact at 31 December 2026 (one batch per month)
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(target, "facility_register_2026-12.xlsx"), read_only=True)
    ws = wb["Facilities"]
    hdr = None
    T.legacy_to_new, T.book_of, T.cust_of = {}, {}, {}
    for r in ws.iter_rows(values_only=True):
        if hdr is None:
            hdr = list(r)
            continue
        d = dict(zip(hdr, r))
        T.book_of[d["facility_no"]] = d["lending_book"]
        T.cust_of[d["facility_no"]] = d["customer_no"]
        if d["legacy_facility_no"]:
            T.legacy_to_new[d["legacy_facility_no"]] = d["facility_no"]
            T.book_of[d["legacy_facility_no"]] = d["lending_book"]
    snap = {}
    for r in rows(target, "dw_fact_loan_month_end_2022_2026.csv"):
        if r["month_end_key"] == "20261231":
            snap[r["facility_no"]] = r
    T.book = {f: r for f, r in snap.items() if r["default_flag"] == "N"}
    # security: the bridge rows in force at the reporting date
    T.secures = defaultdict(list)
    T.bridge = rows(target, "dw_bridge_facility_security_2026-12.csv")
    for r in T.bridge:
        if D(r["row_effective_date"]) <= REPORT <= D(r["row_expiry_date"]):
            T.secures[r["facility_no"]].append(r["property_id"])
    # the default record: one default per facility (the first trigger), facility numbers brought to the bridge's
    T.defaults = {}
    for r in rows(target, "default_register_2012_2026.csv"):
        f = r["facility_no"]
        d = D(r["default_date"])
        if f not in T.defaults or d < T.defaults[f]["date"]:
            T.defaults[f] = dict(date=d, ead=float(r["balance_at_default_eur"]))
    T.props_of_fac_at = {}
    for r in T.bridge:
        T.props_of_fac_at.setdefault(r["facility_no"], []).append((D(r["row_effective_date"]), D(r["row_expiry_date"]), r["property_id"]))
    return T


def in_force(hist, day):
    for x in reversed(hist):
        if x["eff"] <= day <= x["exp"]:
            return x
    return None


def last_inspection(hist, day):
    ins = [x for x in hist if x["basis"] == "INSPECTION" and x["vdate"] <= day]
    return max(ins, key=lambda x: (x["vdate"], x["eff"])) if ins else None


def anchor(hist, row):
    """the inspection a register row rests on: the row itself, or for a roll-forward the latest inspection dated by
    its quarter end and on file when it was written"""
    if row["basis"] == "INSPECTION":
        return row
    ins = [x for x in hist if x["basis"] == "INSPECTION" and x["vdate"] <= row["vdate"] and x["eff"] <= row["eff"]]
    return max(ins, key=lambda x: (x["vdate"], x["eff"])) if ins else None


def record(T, window=92, carried_on="default", age="anchor", side="after"):
    """each default since 2012 whose security the bank inspected at default: the inspection against the value the
    register carried on the default date, and the years from the inspection that carried value rests on to the
    default. `window`, `carried_on` and `age` exist for the fork checks (the window after default, the carried value
    read on the default date or on the day before the inspection, and the years counted from the last inspection
    dated before the default whether or not it was on file); the golden uses the defaults."""
    out = []
    seen = set()
    for f, dft in T.defaults.items():
        d = dft["date"]
        props = [p for (a, b, p) in T.props_of_fac_at.get(f, []) if a <= d <= b]
        book = T.book_of.get(f)
        for p in props:
            if p in seen:
                continue
            h = T.val.get(p, [])
            if side == "after":
                at_def = [x for x in h if x["basis"] == "INSPECTION" and d <= x["vdate"] <= d + dt.timedelta(days=window)]
            else:   # the inspection nearest the default on either side (a fork check)
                near = [x for x in h if x["basis"] == "INSPECTION" and abs((x["vdate"] - d).days) <= window]
                at_def = sorted(near, key=lambda x: (abs((x["vdate"] - d).days), x["vdate"]))[:1]
            if not at_def:
                continue
            car = in_force(h, d if carried_on == "default" else at_def[0]["vdate"] - dt.timedelta(days=1))
            if car is None:
                continue
            prev = anchor(h, car) if age == "anchor" else last_inspection(h, d - dt.timedelta(days=1))
            if prev is None or prev["vdate"] >= d:
                continue
            seen.add(p)
            tau = (d - prev["vdate"]).days / 365.25
            out.append(dict(p=p, fac=f, date=d, tau=tau, ratio=at_def[0]["value"] / car["value"], book=book,
                            ead=dft["ead"]))
    return out


def book_items(T, tau_from=AS_IF):
    """each facility performing at 31 December 2026: grade, exposure, and its share of each property's carried value
    and years since that property's last inspection (counted to 1 January 2027; `tau_from` exists for the fork
    checks)"""
    expo = defaultdict(float)
    for f, r in T.book.items():
        for p in T.secures.get(f, []):
            expo[p] += float(r["balance_eur"])
    items = []
    for f, r in sorted(T.book.items()):
        ead = float(r["balance_eur"])
        g = int(r["internal_grade"])
        parts = []
        for p in T.secures.get(f, []):
            h = T.val[p]
            car = in_force(h, REPORT)
            li = anchor(h, car)
            parts.append(dict(p=p, carried=car["value"] * ead / expo[p], tau=(tau_from - li["vdate"]).days / 365.25,
                              share=ead / expo[p], series=car["series"]))
        items.append(dict(fac=f, cust=r["customer_no"], ead=ead, grade=g, pd=MASTER_PD[g], book=BOOK_CODE[r["lending_book"]],
                          parts=parts))
    return items


def fit_log(rec, mask=None):
    rr = [x for x in rec if mask is None or mask(x)]
    t = np.array([x["tau"] for x in rr])
    y = np.log(np.array([x["ratio"] for x in rr]))
    X = np.c_[np.ones_like(t), t]
    c = np.linalg.lstsq(X, y, rcond=None)[0]
    res = y - X @ c
    return dict(a=float(c[0]), b=float(c[1]), smear=float(np.mean(np.exp(res))), var=float(res.var()), n=len(rr))


def fit_lin(rec, mask=None):
    rr = [x for x in rec if mask is None or mask(x)]
    t = np.array([x["tau"] for x in rr])
    y = np.array([x["ratio"] for x in rr])
    c = np.linalg.lstsq(np.c_[np.ones_like(t), t], y, rcond=None)[0]
    return dict(a=float(c[0]), b=float(c[1]))


EDGES = [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 99]


def fit_band(rec, mask=None):
    rr = [x for x in rec if mask is None or mask(x)]
    allm = float(np.mean([x["ratio"] for x in rr]))
    out = []
    for lo, hi in zip(EDGES[:-1], EDGES[1:]):
        v = [x["ratio"] for x in rr if lo <= x["tau"] < hi]
        out.append(float(np.mean(v)) if v else allm)
    return out


def band_of(bm, t):
    return bm[max(k for k, lo in enumerate(EDGES[:-1]) if t >= lo)]


def factor_fns(rec):
    """expected value at default as a share of the carried value, by method"""
    trade = lambda x: x["book"] == TRADING
    inv = lambda x: x["book"] != TRADING
    P = fit_log(rec)
    G = {True: fit_log(rec, trade), False: fit_log(rec, inv)}
    L = fit_lin(rec)
    GL = {True: fit_lin(rec, trade), False: fit_lin(rec, inv)}
    B = fit_band(rec)
    GB = {True: fit_band(rec, trade), False: fit_band(rec, inv)}
    mean_all = float(np.mean([x["ratio"] for x in rec]))
    return {
        "golden": lambda t, bk: math.exp(G[bk == TRADING]["a"] + G[bk == TRADING]["b"] * t) * G[bk == TRADING]["smear"],
        "split_normal": lambda t, bk: math.exp(G[bk == TRADING]["a"] + G[bk == TRADING]["b"] * t + G[bk == TRADING]["var"] / 2),
        "split_lin": lambda t, bk: GL[bk == TRADING]["a"] + GL[bk == TRADING]["b"] * t,
        "split_band": lambda t, bk: band_of(GB[bk == TRADING], t),
        "split_median": lambda t, bk: math.exp(G[bk == TRADING]["a"] + G[bk == TRADING]["b"] * t),
        "pooled": lambda t, bk: math.exp(P["a"] + P["b"] * t) * P["smear"],
        "pooled_lin": lambda t, bk: L["a"] + L["b"] * t,
        "pooled_band": lambda t, bk: band_of(B, t),
        "pooled_median": lambda t, bk: math.exp(P["a"] + P["b"] * t),
        "carried": lambda t, bk: 1.0,
        "record_mean": lambda t, bk: mean_all,
        "reflex_10_over_3y": lambda t, bk: 0.9 if t > 3 else 1.0,
    }, dict(pooled=P, split=G, mean=mean_all)


def ecl(items, fac):
    out = []
    for it in items:
        v = sum(pt["carried"] * fac(pt["tau"], it["book"]) for pt in it["parts"])
        lgd = max(0.0, it["ead"] - (1 - H) * v) / it["ead"] if it["ead"] > 0 else 0.0
        out.append(dict(fac=it["fac"], cust=it.get("cust"), book=it["book"], ead=it["ead"], pd=it["pd"], grade=it["grade"], vexp=v,
                        carried=sum(pt["carried"] for pt in it["parts"]), lgd=lgd, el=it["pd"] * lgd * it["ead"]))
    return out


def summarise(loans):
    tot = sum(x["el"] for x in loans)
    inv = sum(x["el"] for x in loans if x["book"] != TRADING)
    trd = sum(x["el"] for x in loans if x["book"] == TRADING)
    top = [x["fac"] for x in sorted(loans, key=lambda x: (-x["el"], x["fac"]))[:5]]
    return dict(total=tot, investment=inv, owner_occupied=trd, top5=top)


def compute(target):
    T = load(target)
    rec = record(T)
    items = book_items(T)
    fns, fits = factor_fns(rec)
    res = {k: summarise(ecl(items, fn)) for k, fn in fns.items()}
    return T, rec, items, fns, fits, res
