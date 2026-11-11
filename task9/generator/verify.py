"""task9: the independent verifier. Recomputes every graded result from the shipped files by other code paths than
analysis.py and record.py (its own parsing of the sort record, the polish record, the MES, the maintenance log, the
stores receipts and the final-test summary, its own counter and lot rebuild, a continuous hinge fit, the fallout read
on young disks, a final-test likelihood maximised by a general optimiser instead of a profiled grid, and a numeric cost
minimisation with the pad's sawtooth) and checks each against the band the answer blocks state.

    python3 verify.py            # exit 1 when a result lands outside its band
"""
import csv
import json
import os
import re
import sys

import numpy as np
import openpyxl
import yaml
from scipy.optimize import minimize, minimize_scalar

HERE = os.path.dirname(os.path.abspath(__file__))
TGT = os.path.join(os.path.dirname(HERE), "target")


def product_of(name):
    n = name.strip().upper()
    for key, prod in (("32", "P-A"), ("64", "P-B"), ("16", "P-C")):
        if key in n:
            return prod
    return {"P-A": "P-A", "P-B": "P-B", "P-C": "P-C"}[n]


def load():
    sort = {}
    with open(os.path.join(TGT, "wafer_sort_zones.csv")) as fh:
        for r in csv.DictReader(fh):
            prev = sort.get(r["wafer_id"])
            if prev is None or r["sort_end_ts"] > prev["sort_end_ts"]:
                sort[r["wafer_id"]] = r
    fdc = {}
    with open(os.path.join(TGT, "cmp_wafer_fdc.csv")) as fh:
        for r in csv.DictReader(fh):
            fdc[r["wafer_id"]] = r
    lot_of_wafer = {}
    with open(os.path.join(TGT, "process_history.csv")) as fh:
        for r in csv.DictReader(fh):
            if r["wafer_id"]:
                lot_of_wafer[r["wafer_id"]] = r["lot_id"]
    wb = openpyxl.load_workbook(os.path.join(TGT, "cmp_unit_pm_log.xlsx"), read_only=True)
    log = [r for r in wb.active.iter_rows(min_row=2, values_only=True)]
    ranges = []
    with open(os.path.join(TGT, "stores_receipts_cmp.csv")) as fh:
        for r in csv.DictReader(fh):
            if r["part_no"] == "CMP-CD-A165":
                ranges.append((int(r["serial_first"]), int(r["serial_last"]), r["supplier_lot"]))
    ft = {}
    with open(os.path.join(TGT, "pen2_backend_lot_summary.csv")) as fh:
        for r in csv.DictReader(fh):
            e = ft.setdefault(r["lot_id"], {"units": 0, "bi": 0, "date": ""})
            e["units"] += int(r["units_in"])
            e["bi"] += int(r["burnin_fail"])
            e["date"] = max(e["date"], r["ft_end_date"])
    return sort, fdc, lot_of_wafer, log, ranges, ft


def resets(log, fdc):
    """Per unit and part, the platen counts at which the part was replaced, read from each entry's parts text, and the
    serial of each disk fitted."""
    by_unit = {}
    for w in fdc.values():
        by_unit.setdefault(w["unit_id"], []).append((w["polish_start_ts"], int(w["platen_wafer_count"])))
    for u in by_unit:
        by_unit[u].sort()
    out, serial = {}, {}
    for unit, ts, cls, text, counter, _, _, note in log:
        if cls not in ("FULL_PM", "PAD_CHANGE", "UNSCHED"):
            continue
        t = (text or "").lower()
        parts = set()
        if "pad" in t:
            parts.add("pad")
        if re.search(r"ring|rr-?300", t):
            parts.add("ring")
        if re.search(r"disk|\bcd\b", t) and not re.search(r"retained|kept", t):
            parts.add("disk")
        if counter in (None, ""):
            stamp = str(ts)[:16]
            nxt = [c for tt, c in by_unit[unit] if tt[:16] >= stamp]
            counter = nxt[0] if nxt else None
        if counter is None:
            continue
        for p in parts:
            out.setdefault((unit, p), []).append(int(counter))
        if "disk" in parts:
            m = re.search(r"s/n\s*(\d+)", t)
            serial[(unit, int(counter))] = int(m.group(1)) if m else None
    return {k: sorted(v) for k, v in out.items()}, serial


def table():
    sort, fdc, lot_of_wafer, log, ranges, ft = load()
    marks, serial = resets(log, fdc)

    def lot_of(s):
        return next((L for a, b, L in ranges if s is not None and a <= s <= b), None)
    rows = []
    for wid, s in sort.items():
        f = fdc.get(wid)
        if f is None:
            continue
        fz = [float(s["fail_z%d" % k]) for k in range(1, 9)]
        tz = [float(s["tested_z%d" % k]) for k in range(1, 9)]
        u, plat = f["unit_id"], int(f["platen_wafer_count"])
        use = {}
        for part in ("disk", "pad", "ring"):
            mk = marks[(u, part)]
            k = np.searchsorted(mk, plat, side="right") - 1
            use[part] = plat - mk[k] if k >= 0 else np.nan
            if part == "disk":
                fitted = mk[k] if k >= 0 else None
        rows.append(dict(wafer=wid, lot=lot_of_wafer.get(wid), product=product_of(s["product"]), sort=s["sort_end_ts"],
                         polish=f["polish_start_ts"], unit=u, f_in=sum(fz[:7]) / sum(tz[:7]), f_band=fz[7] / tz[7], n_band=tz[7],
                         gross=sum(tz), platen=plat, disk=use["disk"], pad=use["pad"], ring=use["ring"],
                         disk_lot=lot_of(serial.get((u, fitted))), down=float(f["downforce_psi"]) if f["downforce_psi"] else np.nan))
    return rows, marks, log, fdc, ft


def hinge(x, pad, y, w, lo=300, hi=1900):
    """The onset that minimises the weighted squared error, found by a bounded scalar search, slope and pad term by
    least squares at each trial onset."""
    def sse(w0):
        h = np.maximum(0.0, x - w0)
        X = np.column_stack([np.ones_like(x), h, h * pad / 600.0])
        b, *_ = np.linalg.lstsq(X * np.sqrt(w)[:, None], y * np.sqrt(w), rcond=None)
        return float(np.sum(w * (y - X @ b) ** 2)), b
    coarse = min(range(lo, hi + 1, 25), key=lambda v: sse(v)[0])
    w0 = minimize_scalar(lambda v: sse(v)[0], bounds=(coarse - 25, coarse + 25), method="bounded", options={"xatol": 1.0}).x
    b = sse(w0)[1]
    return dict(w0=float(w0), r0=float(b[0]), beta=float(b[1]), gamma=float(b[2] / b[1]))


def main():
    F = json.load(open(os.path.join(HERE, "figures.json")))
    B = F["bands"]
    rows, marks, log, fdc, ft = table()
    units = sorted({r["unit"] for r in rows})
    med = {u: np.nanmedian([r["down"] for r in rows if r["unit"] == u]) for u in units}
    cut = np.median(list(med.values()))
    pair = {u: ("high" if med[u] > cut else "low") for u in units}
    arr = {k: np.array([r[k] for r in rows]) for k in ("f_in", "f_band", "n_band", "gross", "disk", "pad", "ring")}
    arr["pair"] = np.array([pair[r["unit"]] for r in rows])
    arr["lotd"] = np.array([r["disk_lot"] or "" for r in rows])
    arr["y"] = arr["f_band"] - arr["f_in"]
    srt = np.array([r["sort"] for r in rows])
    win = (srt >= "2026-04-01") & (srt < "2026-09-01")
    prod = np.array([r["product"] for r in rows])
    unit = np.array([r["unit"] for r in rows])
    plat = np.array([r["platen"] for r in rows])
    pol = np.array([r["polish"] for r in rows])
    out = []

    def judge(name, v, band):
        ok = band[0] <= v <= band[1]
        out.append(ok)
        print("%s  %-44s %s against %s" % ("PASS" if ok else "FAIL", name, ("%.4g" % v) if isinstance(v, float) else v, band))
    # the lot every unit runs now
    last = {u: arr["lotd"][unit == u][np.argmax(pol[unit == u])] for u in units}
    cur = sorted(set(last.values()))
    judge("every unit's current disk from one lot", float(len(cur)), [1, 1])
    fwd = cur[0]
    lots = sorted(set(arr["lotd"]) - {""})
    fits = {}
    for p in ("low", "high"):
        for L in lots:
            m = (arr["pair"] == p) & (arr["lotd"] == L)
            fits[(p, L)] = hinge(arr["disk"][m], arr["pad"][m], arr["y"][m], arr["n_band"][m])
    # the fallout on disks short of their onset: the band's excess on wafers at under half their group's onset
    r0 = {}
    for k, f in fits.items():
        m = (arr["pair"] == k[0]) & (arr["lotd"] == k[1]) & (arr["disk"] < f["w0"] / 2)
        r0[k] = float(np.average(arr["y"][m], weights=arr["n_band"][m]))
    keys = list(zip(arr["pair"], arr["lotd"]))
    r0w = np.array([r0[k] for k in keys])
    die = arr["n_band"] * (arr["y"] - r0w)
    judge("R1 the loss at sort, points", float(np.mean(die[win] / arr["gross"][win]) * 100), B["R1_loss"]["points"])
    for pr in ("P-A", "P-B", "P-C"):
        judge("R1 good die, %s" % pr, float(die[win & (prod == pr)].sum()), B["R1_loss"]["%s die" % pr])
    # R2: the pad's and the disk's shares, the retaining ring's step at its swaps
    exd, exp = np.zeros(len(rows)), np.zeros(len(rows))
    for i in np.where(win)[0]:
        f = fits[keys[i]]
        h = max(0.0, arr["disk"][i] - f["w0"])
        exd[i] = f["beta"] * h * arr["n_band"][i] / arr["gross"][i]
        exp[i] = f["beta"] * f["gamma"] * h * arr["pad"][i] / 600.0 * arr["n_band"][i] / arr["gross"][i]
    pad_share = float(exp.sum() / (exd.sum() + exp.sum()))
    judge("R2 the pad's share", pad_share, B["R2_shares"]["pad"])
    judge("R2 the disk's share", 1 - pad_share, B["R2_shares"]["disk"])
    resid = arr["y"] - r0w - np.array([fits[k]["beta"] * max(0.0, d - fits[k]["w0"]) * (1 + fits[k]["gamma"] * pd_ / 600.0)
                                       for k, d, pd_ in zip(keys, arr["disk"], arr["pad"])])
    steps = []
    for unit_id, ts, cls, text, counter, _, _, note in log:
        t = (text or "").lower()
        if cls == "UNSCHED" and re.search(r"ring|rr-?300", t) and not re.search(r"disk|\bcd\b", t) and counter not in (None, ""):
            c = int(counter)
            mb = (unit == unit_id) & (plat >= c - 300) & (plat < c)
            ma = (unit == unit_id) & (plat >= c) & (plat < c + 300)
            if mb.sum() > 150 and ma.sum() > 150:
                steps.append(float(np.average(resid[ma], weights=arr["n_band"][ma]) - np.average(resid[mb], weights=arr["n_band"][mb])))
    print("      ring-only swap steps: %s" % ", ".join("%+.4f" % s for s in steps))
    judge("R2 the retaining ring's step at its swaps", abs(float(np.mean(steps))), [0.0, 0.006])
    # R3: final test's burn-in failures, lot by lot, by maximum likelihood
    wear = np.array([d / fits[k]["w0"] for d, k in zip(arr["disk"], keys)])
    gb = arr["n_band"] * (1 - arr["f_band"])
    lot_ids = sorted(ft)
    li = {l: i for i, l in enumerate(lot_ids)}
    wl = np.array([li.get(r["lot"], -1) for r in rows])
    keep = wl >= 0
    U = np.array([ft[l]["units"] for l in lot_ids], float)
    Y = np.array([ft[l]["bi"] for l in lot_ids], float)

    def mu(th):
        b, L, u0, us = th
        lam = L * np.clip((wear[keep] - u0) / max(us, 1e-3), 0, 1)
        return b * U + np.bincount(wl[keep], weights=gb[keep] * lam, minlength=len(lot_ids))

    def nll(th):
        if th[0] <= 0 or th[1] < 0 or th[3] <= 0.01:
            return 1e18
        m = np.maximum(mu(th), 1e-9)
        return float(np.sum(m - Y * np.log(m)))
    best = None
    for start in ([0.002, 0.05, 0.4, 0.3], [0.002, 0.08, 0.6, 0.2], [0.003, 0.04, 0.3, 0.5]):
        r = minimize(nll, start, method="Nelder-Mead", options=dict(maxiter=6000, xatol=1e-7, fatol=1e-4))
        if best is None or r.fun < best.fun:
            best = r
    th = best.x
    lam = th[1] * np.clip((wear[keep] - th[2]) / th[3], 0, 1)
    lat = np.bincount(wl[keep], weights=gb[keep] * lam, minlength=len(lot_ids))
    lot_prod = {}
    for r in rows:
        lot_prod.setdefault(r["lot"], r["product"])
    for pr in ("P-A", "P-B", "P-C"):
        v = sum(lat[i] for l, i in li.items() if lot_prod.get(l) == pr and "2026-04-01" <= ft[l]["date"] < "2026-09-01")
        judge("R3 units lost at final test, %s" % pr, float(v), B["R3_ft_units"][pr])
    # R4: the current lot's curve, each pair
    for u in units:
        f = fits[(pair[u], fwd)]
        judge("R4 %s onset" % u, f["w0"], B["R4_dose"]["%s onset" % u])
        judge("R4 %s climb" % u, f["beta"] * 1000 * 100, B["R4_dose"]["%s climb" % u])
    # REC, R5: the cost per wafer minimised numerically, the pad's sawtooth over its 600-wafer cycle
    costs = yaml.safe_load(open(os.path.join(TGT, "cost_inputs.yaml")))
    value = {p: float(v["value_per_good_die"]) for p, v in costs["die"].items()}
    assy = {p: float(v["assembly_and_test_per_unit"]) for p, v in costs["die"].items()}
    mix = {p: float(v) for p, v in costs["volume"]["product_mix"].items()}
    vol = {u: float(v) for u, v in costs["volume"]["wafers_per_year_by_unit"].items()}
    nb = {pr: float(np.median(arr["n_band"][prod == pr])) for pr in value}
    fin = float(np.average(arr["f_in"], weights=arr["n_band"]))
    c_disk, full = float(costs["all_in"]["disk_change"]), float(costs["all_in"]["full_pm"])
    part = float(costs["parts"]["conditioner_disk"])

    def loss(f, T):
        x = np.arange(0.0, T, 1.0)
        ex = f["beta"] * np.maximum(0.0, x - f["w0"]) * (1 + f["gamma"] * (x % 600) / 600.0)
        lam_x = th[1] * np.clip((x / f["w0"] - th[2]) / th[3], 0, 1)
        good = np.clip(1 - fin - f["r0"] - ex, 0, None)
        return float(sum(mix[pr] * nb[pr] * np.sum(value[pr] * ex + good * lam_x * (value[pr] + assy[pr])) for pr in mix))
    T = {}
    for p in ("low", "high"):
        f = fits[(p, fwd)]
        coarse = min(range(300, 3001, 20), key=lambda t: (c_disk + loss(f, t)) / t)
        T[p] = minimize_scalar(lambda t: (c_disk + loss(f, t)) / t, bounds=(coarse - 20, coarse + 20), method="bounded",
                               options={"xatol": 1.0}).x
    for u in units:
        judge("REC %s count" % u, float(T[pair[u]]), B["REC_counts"][u])
    saving = 0.0
    for u in units:
        f = fits[(pair[u], fwd)]
        rev_f = (full + loss(f, 2800)) / 2800
        rev_g = (full - part) / 2800 + (c_disk + loss(f, T[pair[u]])) / T[pair[u]]
        saving += (rev_f - rev_g) * vol[u]
    judge("R5 the yearly saving, USD", saving, B["R5_saving"])
    print("%d of %d inside their bands" % (sum(out), len(out)))
    return 0 if all(out) else 1


if __name__ == "__main__":
    sys.exit(main())
