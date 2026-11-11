"""task9: the independent verifier. Recomputes every graded result from the shipped files by other code paths than
analysis.py and record.py (its own parsing of the sort record, the polish record and the maintenance log, its own
counter rebuild, a continuous hinge fit, its own run of each maintenance rule, a numeric cost minimisation instead of
the closed form) and checks each against the band the answer blocks state.

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
from scipy.optimize import minimize_scalar

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
    wb = openpyxl.load_workbook(os.path.join(TGT, "cmp_unit_pm_log.xlsx"), read_only=True)
    log = [r for r in wb.active.iter_rows(min_row=2, values_only=True)]
    return sort, fdc, log


def resets(log, fdc):
    """Per unit and part, the platen counts at which the part was replaced, read from each entry's parts text."""
    by_unit = {}
    for w in fdc.values():
        by_unit.setdefault(w["unit_id"], []).append((w["polish_start_ts"], int(w["platen_wafer_count"])))
    for u in by_unit:
        by_unit[u].sort()
    out = {}
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
        if cls == "FULL_PM":
            parts.add("full")
        if counter in (None, ""):
            stamp = str(ts)[:16]
            nxt = [c for tt, c in by_unit[unit] if tt[:16] >= stamp]
            counter = nxt[0] if nxt else None
        if counter is None:
            continue
        for p in parts:
            out.setdefault((unit, p), []).append(int(counter))
    return {k: sorted(v) for k, v in out.items()}


def usage(platen, marks):
    k = np.searchsorted(marks, platen, side="right") - 1
    return platen - marks[k] if k >= 0 else np.nan


def table():
    sort, fdc, log = load()
    marks = resets(log, fdc)
    rows = []
    for wid, s in sort.items():
        f = fdc.get(wid)
        if f is None:
            continue
        fz = [float(s["fail_z%d" % k]) for k in range(1, 9)]
        tz = [float(s["tested_z%d" % k]) for k in range(1, 9)]
        u, plat = f["unit_id"], int(f["platen_wafer_count"])
        rows.append(dict(wafer=wid, product=product_of(s["product"]), sort=s["sort_end_ts"], polish=f["polish_start_ts"], unit=u,
                         f_in=sum(fz[:7]) / sum(tz[:7]), f_band=fz[7] / tz[7], n_band=tz[7], gross=sum(tz), platen=plat,
                         disk=usage(plat, marks[(u, "disk")]), pad=usage(plat, marks[(u, "pad")]),
                         ring=usage(plat, marks[(u, "ring")]), down=float(f["downforce_psi"]) if f["downforce_psi"] else np.nan))
    return rows, marks, log, fdc


def hinge(x, pad, y, w):
    """The onset that minimises the weighted squared error, found by a bounded scalar search, slope and pad term by
    least squares at each trial onset."""
    def sse(w0):
        h = np.maximum(0.0, x - w0)
        X = np.column_stack([np.ones_like(x), h, h * pad / 600.0])
        b, *_ = np.linalg.lstsq(X * np.sqrt(w)[:, None], y * np.sqrt(w), rcond=None)
        return float(np.sum(w * (y - X @ b) ** 2)), b
    best = minimize_scalar(lambda v: sse(v)[0], bounds=(500, 1900), method="bounded", options={"xatol": 1.0})
    coarse = min(range(500, 1901, 25), key=lambda v: sse(v)[0])
    w0 = best.x if sse(best.x)[0] <= sse(coarse)[0] else minimize_scalar(lambda v: sse(v)[0], bounds=(coarse - 25, coarse + 25),
                                                                       method="bounded").x
    b = sse(w0)[1]
    return dict(w0=float(w0), r0=float(b[0]), beta=float(b[1]), gamma=float(b[2] / b[1]))


def main():
    F = json.load(open(os.path.join(HERE, "figures.json")))
    B = F["bands"]
    rows, marks, log, fdc = table()
    units = sorted({r["unit"] for r in rows})
    med = {u: np.nanmedian([r["down"] for r in rows if r["unit"] == u]) for u in units}
    cut = np.median(list(med.values()))
    pair = {u: ("high" if med[u] > cut else "low") for u in units}
    arr = {k: np.array([r[k] for r in rows]) for k in ("f_in", "f_band", "n_band", "gross", "disk", "pad", "ring")}
    arr["pair"] = np.array([pair[r["unit"]] for r in rows])
    arr["y"] = arr["f_band"] - arr["f_in"]
    srt = np.array([r["sort"] for r in rows])
    win = (srt >= "2026-04-01") & (srt < "2026-09-01")
    prod = np.array([r["product"] for r in rows])
    fits = {}
    for p in ("low", "high"):
        m = arr["pair"] == p
        fits[p] = hinge(arr["disk"][m], arr["pad"][m], arr["y"][m], arr["n_band"][m])
    # the fallout at a fresh disk: the band's excess on wafers at under half the pair's onset
    r0 = {}
    for p in fits:
        m = (arr["pair"] == p) & (arr["disk"] < fits[p]["w0"] / 2)
        r0[p] = float(np.average(arr["y"][m], weights=arr["n_band"][m]))
    die = arr["f_band"] * arr["n_band"] - arr["n_band"] * (arr["f_in"] + np.array([r0[p] for p in arr["pair"]]))
    R1 = float(np.mean(die[win] / arr["gross"][win]) * 100)
    R2 = {pr: float(die[win & (prod == pr)].sum()) for pr in ("P-A", "P-B", "P-C")}
    out = []

    def judge(name, v, band):
        ok = band[0] <= v <= band[1]
        out.append(ok)
        print("%s  %-40s %s against %s" % ("PASS" if ok else "FAIL", name, ("%.4g" % v) if isinstance(v, float) else v, band))
    judge("R1 the loss, points", R1, B["R1_points"])
    for pr in R2:
        judge("R2 good die, %s" % pr, R2[pr], B["R2_die"][pr])
    # R3: the ring's swaps as a natural experiment, the disk's and the pad's shares from the hinge
    resid = arr["y"] - np.array([r0[p] for p in arr["pair"]]) - np.array(
        [fits[p]["beta"] * max(0.0, d - fits[p]["w0"]) * (1 + fits[p]["gamma"] * pd_ / 600.0) for p, d, pd_ in zip(arr["pair"], arr["disk"], arr["pad"])])
    plat = np.array([r["platen"] for r in rows])
    unit = np.array([r["unit"] for r in rows])
    steps = []
    for unit_id, ts, cls, text, counter, _, _, note in log:
        if cls == "UNSCHED" and re.search(r"ring|rr-?300", (text or "").lower()) and not re.search(r"disk|\bcd\b", (text or "").lower()):
            c = int(counter) if counter not in (None, "") else None
            if c is None:
                continue
            mb = (unit == unit_id) & (plat >= c - 300) & (plat < c)
            ma = (unit == unit_id) & (plat >= c) & (plat < c + 300)
            if mb.sum() > 150 and ma.sum() > 150:
                steps.append(float(np.average(resid[ma], weights=arr["n_band"][ma]) - np.average(resid[mb], weights=arr["n_band"][mb])))
    mean_step = float(np.mean(steps))
    print("      ring-only swap steps: %s" % ", ".join("%+.4f" % s for s in steps))
    judge("R3 the retaining ring's step at its swaps", abs(mean_step), [0.0, 0.006])
    ex = np.zeros(len(rows))
    pad_part = np.zeros(len(rows))
    for p in fits:
        m = (arr["pair"] == p) & win
        h = np.maximum(0.0, arr["disk"][m] - fits[p]["w0"])
        ex[m] = fits[p]["beta"] * h * arr["n_band"][m] / arr["gross"][m]
        pad_part[m] = fits[p]["beta"] * h * fits[p]["gamma"] * arr["pad"][m] / 600.0 * arr["n_band"][m] / arr["gross"][m]
    pad_share = float(pad_part.sum() / (ex.sum() + pad_part.sum()))
    judge("R3 the pad's share", pad_share, B["R3_shares"]["pad"])
    judge("R3 the disk's share", 1 - pad_share, B["R3_shares"]["disk"])
    # R4
    for u in units:
        f = fits[pair[u]]
        judge("R4 %s onset" % u, f["w0"], B["R4_dose"]["%s onset" % u])
        judge("R4 %s slope" % u, f["beta"] * 1000 * 100, B["R4_dose"]["%s slope" % u])
    # R5: each rule run again on each unit's own wafers
    def run(u, rule):
        m = np.where(unit == u)[0]
        order = m[np.argsort(plat[m])]
        first = plat[order[0]]
        fulls = [c for c in marks[(u, "full")] if c < first]
        pads = [c for c in marks[(u, "pad")] if c < first]
        st = {"disk": first - max(fulls), "full": first - max(fulls), "pad": first - max(pads)}
        uns = {}
        for unit_id, ts, cls, text, counter, _, _, note in log:
            if unit_id == u and cls == "UNSCHED":
                t = (text or "").lower()
                if re.search(r"disk|\bcd\b", t):
                    uns.setdefault(int(counter) if counter not in (None, "") else -1, []).append("disk")
        res = {}
        pol = {r["platen"]: r["polish"] for r in rows if r["unit"] == u}
        allplat = sorted(int(w["platen_wafer_count"]) for w in fdc.values() if w["unit_id"] == u)
        polish_of = {int(w["platen_wafer_count"]): w["polish_start_ts"] for w in fdc.values() if w["unit_id"] == u}
        for pl in allplat:
            for part in uns.get(pl, ()):
                st[part] = 0
            res[pl] = (st["disk"], st["pad"])
            for k in st:
                st[k] += 1
            iv = 2000 if rule == "E" or polish_of[pl] < "2026-04-02" else 2800
            if st["full"] >= iv:
                st = {"disk": 0, "full": 0, "pad": 0}
            elif st["pad"] >= 600:
                st["pad"] = 0
        return res
    tot = {}
    for rule in ("E", "F", "A"):
        s = 0.0
        for u in units:
            f = fits[pair[u]]
            sched = run(u, rule) if rule != "A" else None
            m = np.where((unit == u) & win)[0]
            for i in m:
                d, pd_ = (arr["disk"][i], arr["pad"][i]) if rule == "A" else sched[plat[i]]
                s += f["beta"] * max(0.0, d - f["w0"]) * (1 + f["gamma"] * pd_ / 600.0) * arr["n_band"][i] / arr["gross"][i]
        tot[rule] = s
    br = {"old_rule": tot["E"] / tot["A"], "rev_f": (tot["F"] - tot["E"]) / tot["A"], "ew118": (tot["A"] - tot["F"]) / tot["A"]}
    for k, v in br.items():
        judge("R5 %s share" % k, v, B["R5_bridge"][k])
    # R6, R7: the cost per wafer minimised numerically, the pad's sawtooth averaged over its 600-wafer cycle
    costs = yaml.safe_load(open(os.path.join(TGT, "cost_inputs.yaml")))
    value = {p: float(v["value_per_good_die"]) for p, v in costs["die"].items()}
    nb = {pr: float(np.median(arr["n_band"][prod == pr])) for pr in value}
    summer = srt >= "2026-06-01"
    mix = {pr: float(np.mean(prod[summer] == pr)) for pr in value}
    V = sum(mix[pr] * nb[pr] * value[pr] for pr in value)
    c_disk, full = float(costs["all_in"]["disk_change"]), float(costs["all_in"]["full_pm"])
    part = float(costs["parts"]["conditioner_disk"])

    def ring_cost(f, T):
        x = np.arange(0.0, T, 1.0)
        return float(np.sum(V * f["beta"] * np.maximum(0.0, x - f["w0"]) * (1 + f["gamma"] * (x % 600) / 600.0)))
    T = {}
    for p, f in fits.items():
        T[p] = minimize_scalar(lambda t: (c_disk + ring_cost(f, t)) / t, bounds=(600, 3000), method="bounded", options={"xatol": 1.0}).x
    for u in units:
        judge("R6 %s count" % u, float(T[pair[u]]), B["R6_counts"][u])
    wpy = float(costs["volume"]["wafers_per_year_ild_cmp"])
    pol_dates = np.array([r["polish"] for r in rows])
    share = {u: float(np.mean(unit[pol_dates >= "2026-06-01"] == u)) for u in units}
    saving = 0.0
    for u in units:
        f = fits[pair[u]]
        rev_f = (full + ring_cost(f, 2800)) / 2800
        rev_g = (full - part) / 2800 + (c_disk + ring_cost(f, T[pair[u]])) / T[pair[u]]
        saving += (rev_f - rev_g) * wpy * share[u]
    judge("R7 the yearly saving, USD", saving, B["R7_saving"])
    print("%d of %d inside their bands" % (sum(out), len(out)))
    return 0 if all(out) else 1


if __name__ == "__main__":
    sys.exit(main())
