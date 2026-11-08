"""task2 architecture 4: the independent verifier. Reads only the cut pack on its own code path (pandas for the
tables, pdftotext for the term sheet and the plan summary, its own compositing by RL overlap, its own declustering,
its own variogram fit by coordinate search and a Monte Carlo block average), and recomputes the tier and the rounded
gold above the agreement's cut-off.

    python3 task2/generator/verify.py <target> [figures.json]"""
import json
import math
import os
import re
import subprocess
import sys

import numpy as np
import pandas as pd


def pdf_text(p):
    return subprocess.run(["pdftotext", "-layout", p, "-"], capture_output=True, text=True, check=True).stdout


def main(target, figs=None):
    out = {}
    terms = pdf_text(os.path.join(target, "Yarrabin_OPA_2027-2028_term_sheet.pdf"))
    cut = float(re.search(r"grade is ([\d.]+) g/t or more", terms).group(1))
    tiers = [(t, int(v.replace(",", ""))) for t, v in re.findall(r"^\s*([ABC])\s+([\d,]+)\s+\d+\s*$", terms, re.M)]
    plan = pdf_text(os.path.join(target, "MC_2027_mine_plan_summary.pdf"))
    se, sn = [float(x.replace(",", "")) for x in re.findall(r"less\s+([\d,]+\.\d) m east and ([\d,]+\.\d) m north",
                                                             re.sub(r"\s+", " ", plan))[0]]
    out.update(cut=cut, tiers=tiers, shift=[se, sn])
    col = pd.read_csv(os.path.join(target, "MC_drillhole_collars.csv"))
    mga = col["grid"] == "MGA94_51"
    col.loc[mga, "east"] -= se
    col.loc[mga, "north"] -= sn
    col = col.set_index("hole_id")
    a = pd.read_csv(os.path.join(target, "MC_drillhole_assays.csv"), dtype={"au": str})
    a["v"] = np.where(a["au"].str.startswith("<"), 0.005, pd.to_numeric(a["au"].str.lstrip("<"), errors="coerce"))
    a = a.drop_duplicates(["hole_id", "depth_from", "depth_to"], keep="first")
    w = pd.read_csv(os.path.join(target, "MC_weathering_logs.csv"))
    des = pd.read_csv(os.path.join(target, "MC_stage5_design_flitches.csv"))
    rho = pd.read_csv(os.path.join(target, "MC_bulk_density.csv")).groupby("weathering")["density_t_m3"].mean()
    rows = []
    for h, grp in a.groupby("hole_id"):
        rl0 = col.loc[h, "rl"]
        top_rl = rl0 - grp["depth_from"].values
        bot_rl = rl0 - grp["depth_to"].values
        ww = w[w["hole_id"] == h]
        for _, d in des.iterrows():
            ov = np.clip(np.minimum(top_rl, d["rl_top"]) - np.maximum(bot_rl, d["rl_bottom"]), 0, None)
            if ov.sum() < 1.25:
                continue
            e, n = col.loc[h, "east"], col.loc[h, "north"]
            if not (d["east_min"] <= e <= d["east_max"] and d["north_min"] <= n <= d["north_max"]):
                continue
            mid = rl0 - (d["rl_top"] + d["rl_bottom"]) / 2
            zn = ww[(ww["depth_from"] <= mid) & (ww["depth_to"] > mid)]["weathering"]
            rows.append((h, e, n, d["flitch"], float((ov * grp["v"].values).sum() / ov.sum()),
                         zn.iloc[0] if len(zn) else "FR"))
    c = pd.DataFrame(rows, columns=["h", "e", "n", "f", "g", "z"])
    c["cell"] = list(zip((c["e"] // 25).astype(int), (c["n"] // 25).astype(int), c["f"]))
    c["w"] = 1.0 / c.groupby("cell")["g"].transform("size")
    m = float((c["w"] * c["g"]).sum() / c["w"].sum())
    v = float((c["w"] * (c["g"] - m) ** 2).sum() / c["w"].sum())
    out.update(n=len(c), mean_decl=round(m, 3))
    # tonnage
    c["rho"] = c["z"].map(rho)
    T = 0.0
    for _, d in des.iterrows():
        sub = c[c["f"] == d["flitch"]]
        r = (sub["w"] * sub["rho"]).sum() / sub["w"].sum() if len(sub) else rho["FR"]
        T += (d["east_max"] - d["east_min"]) * (d["north_max"] - d["north_min"]) * 2.5 * r
    # variogram: downhole lags and across-hole classes, a nugget and two spherical structures by coordinate search
    piv = c.pivot_table(index="h", columns="f", values="g")
    dh = []
    for L in range(1, 11):
        dif = (piv.values[:, L:] - piv.values[:, :-L]).ravel()
        dif = dif[~np.isnan(dif)]
        dh.append((2.5 * L, 0.5 * float(np.mean(dif ** 2)), len(dif)))
    xy = c.groupby("h")[["e", "n"]].first().loc[piv.index].values
    P = piv.values
    hz_acc = {}
    for i in range(len(xy)):
        dd = np.hypot(xy[i + 1:, 0] - xy[i, 0], xy[i + 1:, 1] - xy[i, 1])
        for j in np.nonzero((dd > 0.5) & (dd < 112.5))[0]:
            dif = P[i] - P[i + 1 + j]
            dif = dif[~np.isnan(dif)]
            if len(dif):
                b = int(dd[j] // 12.5)
                s = hz_acc.setdefault(b, [0.0, 0, 0.0])
                s[0] += float((dif ** 2).sum())
                s[1] += len(dif)
                s[2] += dd[j] * len(dif)
    hz = [(s[2] / s[1], 0.5 * s[0] / s[1], s[1]) for b, s in sorted(hz_acc.items()) if s[1] > 50]
    sill = float(np.var(c["g"]))

    def sph(h, a):
        x = np.minimum(np.asarray(h) / a, 1.0)
        return 1.5 * x - 0.5 * x ** 3

    def gam(hx, hzz, p):
        c0, c1, a1, a2, r = p
        h = np.sqrt(np.asarray(hx) ** 2 + (np.asarray(hzz) / r) ** 2)
        return np.where(h > 0, c0, 0.0) + c1 * sph(h, a1) + (1 - c0 - c1) * sph(h, a2)

    def err(p):
        if p[0] < 0 or p[1] < 0 or p[0] + p[1] > 0.97 or p[2] < 3 or p[3] <= p[2] or p[4] <= 0.1:
            return 1e9
        e1 = sum(n * (gam(0, a, p) - g / sill) ** 2 for a, g, n in dh) / sum(n for *_, n in dh)
        e2 = sum(n * (gam(a, 0, p) - g / sill) ** 2 for a, g, n in hz) / sum(n for *_, n in hz)
        return e1 + e2
    p = [0.3, 0.3, 10.0, 60.0, 0.5]
    steps = [0.05, 0.05, 2.0, 10.0, 0.1]
    for _ in range(200):
        moved = False
        for i in range(5):
            for s in (steps[i], -steps[i]):
                q = list(p)
                q[i] += s
                if err(q) < err(p):
                    p, moved = q, True
        if not moved:
            steps = [s / 2 for s in steps]
            if max(steps) < 1e-3:
                break
    rng = np.random.default_rng(7)
    u1 = rng.uniform(0, 1, (4000, 3)) * [5, 5, 2.5]
    u2 = rng.uniform(0, 1, (4000, 3)) * [5, 5, 2.5]
    gb = float(gam(np.hypot(u1[:, 0] - u2[:, 0], u1[:, 1] - u2[:, 1]), np.abs(u1[:, 2] - u2[:, 2]), p).mean())
    ratio = 1 - gb
    b = math.sqrt(math.log(1 + ratio * v / m ** 2) / math.log(1 + v / m ** 2))
    gs = c["g"].values ** b
    gs *= m / ((c["w"] * gs).sum() / c["w"].sum())
    tw = c["w"].values * c["rho"].values
    above = gs >= cut
    oz = T * tw[above].sum() / tw.sum() * (tw[above] * gs[above]).sum() / tw[above].sum() / 31.1035
    ok = [t for t, val in tiers if oz >= val]
    out.update(model=[round(x, 3) for x in p], ratio=round(ratio, 3), T=round(T), oz=round(oz), tier=ok[-1] if ok else None,
               oz_50k=int(50000 * math.floor(oz / 50000 + 0.5)))
    fails = []
    if figs:
        F = json.load(open(figs))
        if out["tier"] != F["call"]:
            fails.append("tier %s against %s" % (out["tier"], F["call"]))
        if out["oz_50k"] != F["oz_50k"]:
            fails.append("gold %s against %s" % (out["oz_50k"], F["oz_50k"]))
    print(json.dumps(out, indent=1))
    print("verify: %s" % ("PASS" if not fails else "FAIL " + "; ".join(fails)))
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None))
