"""task9: the generator's assertions on the installed build (target/, generator/figures.json, effort.json, submission.md).

    python3 generator/checks.py        # exit 1 on any failed assertion

The input gates, the house rule on factors (each one's footprint outside the units it decides), each result's hurried
figure against its band, the rivals inside, the one-fact test, and every row of the design note's fork table.
"""
import csv
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

import analysis as AN  # noqa: E402
import pack as PK  # noqa: E402
import params as P  # noqa: E402
from record import Record  # noqa: E402

TGT = os.path.join(TASK, "target")
FAILS = []


def check(name, ok, detail=""):
    print("%s  %-62s %s" % ("PASS" if ok else "FAIL", name, detail))
    if not ok:
        FAILS.append(name)


def inside(v, b):
    return v is not None and b[0] <= v <= b[1]


def main():
    F = json.load(open(os.path.join(HERE, "figures.json")))
    E = json.load(open(os.path.join(HERE, "effort.json")))
    g, B, R = F["gold"], F["bands"], F["routes"]
    files = sorted(os.listdir(TGT))
    # ---- the input gates
    check("ten or more usable files", len(files) >= 10, "%d files" % len(files))
    cats = {"csv": "spreadsheet", "xlsx": "spreadsheet", "pdf": "text", "md": "text", "yaml": "code", "png": "image"}
    check("two or more file categories", len({cats[f.rsplit(".", 1)[1]] for f in files}) >= 2,
          ", ".join(sorted({cats[f.rsplit(".", 1)[1]] for f in files})))
    rows = {f: sum(1 for _ in open(os.path.join(TGT, f))) - 1 for f in files if f.endswith(".csv")}
    check("a CSV of 20,000 rows or more", max(rows.values()) >= 20000, "%s %d rows" % (max(rows, key=rows.get), max(rows.values())))
    check("a second CSV of 10 printed pages or more (500 lines)", sorted(rows.values())[-2] >= 500,
          ", ".join("%s %d" % (k, v) for k, v in sorted(rows.items(), key=lambda x: -x[1])[:3]))
    src = "".join(open(os.path.join(HERE, m)).read() for m in ("record.py", "analysis.py", "figures.py"))
    for f in PK.DISTRACTORS:
        check("distractor %s on file and never read by the golden" % f, f in files and f not in src and
              not any(k in src for k, v in PK.F.items() if v == f and ('F["%s"]' % k) in src))
    bad = [f for f in files if re.search(r"read_?me|dictionar|codebook|field_?notes|manifest|schema|glossary", f, re.I)]
    check("no file named as a description of the data", not bad, ", ".join(bad) or "none")
    # ---- the record, read from the pack alone
    rec = Record(TGT)
    d = rec.d
    hot = rec.hot_flags(P.END)
    w = rec.hot_scan["window"]
    check("the bad-build window is found from the record", w is not None and str(w[0].date()) == F["record"]["hot_scan"]["window"][0],
          "%s to %s, likelihood ratio %.0f" % (w[0].date(), w[1].date(), rec.hot_scan["llr"]))
    rec.hot_flags(P.BACKTEST_CUT)
    check("the batch is not yet visible at the back-test cut", rec.hot_scan["window"] is None, "likelihood ratio %.1f" % rec.hot_scan["llr"])
    hot = rec.hot_flags(P.END)
    hx = d[hot]
    other = hx[hx.dc != "DC-2"]
    check("bad-build drives also sit outside the five DC-2 vaults (spares)", len(other) > 0, "%d drives in %s" % (
        len(other), ", ".join(sorted(other.vault_id.unique()))))
    fw = d[(d.family == "HX-8") & (d.firmware == "HX8.2.0") & ~hot & d.build.notna()]
    check("HX8.2.0 builds outside the window (the firmware story's misreading)", len(fw) >= 500,
          "%d drives, weeks %s" % (len(fw), ", ".join(sorted({"%d" % x.isocalendar()[1] for x in fw.build}))[:60]))
    ev = rec.events
    for dc in ("DC-1", "DC-2", "DC-3"):
        n = int(((ev.dc == dc) & ev.event_type.isin(["CHASSIS_POWER_EVENT", "COOLING_EXCURSION"])).sum())
        check("shared incidents logged in %s" % dc, n >= 5, "%d" % n)
    dec = ev[ev.event_type == "DECOM_START"]
    fams = {v: d[d.vault_id == v].family.iloc[0] for v in dec.vault_id}
    check("selective retirement outside the OM-6 vaults too (KS-10 in DC-3)", any(f == "KS-10" for f in fams.values()),
          ", ".join("%s %s" % (v, f) for v, f in fams.items()))
    mig = (d.dc == "DC-3") & (d.install_date == pd.Timestamp(P.MIGRATION))
    check("every DC-3 drive's inventory install date is the migration day", int(mig.sum()) == int((d.dc == "DC-3").sum() - (
        (d.dc == "DC-3") & (d.install_date > pd.Timestamp(P.MIGRATION))).sum()), "%d drives" % int(mig.sum()))
    # ---- each result: the golden inside its band, the hurried routes outside where the design says
    S = F
    check("R1 DC-3 inside its band", inside(S["dc3"], B["dc3"]), "%s in %s" % (S["dc3"], B["dc3"]))
    check("R1 the close-out's DC-3 rate carried outside", not inside(F["quick"]["dc3"], B["dc3"]), "%.0f" % F["quick"]["dc3"])
    hb = S["hot_batch"]
    fwr = R["the firmware release as the batch"]["hot_batch"]
    check("R2 the firmware story's drives outside the band", not inside(fwr["drives"], B["hot_batch"]["drives"]),
          "%d against %s" % (fwr["drives"], [round(x) for x in B["hot_batch"]["drives"]]))
    check("R2 the firmware story's rate outside the band", not inside(fwr["rate"], B["hot_batch"]["rate"]),
          "%.4f against %s" % (fwr["rate"], [round(x, 4) for x in B["hot_batch"]["rate"]]))
    check("R3 the batch inside its family outside", not inside(R["the hot batch inside its family"]["hot_count"], B["hot_count"]),
          "%.0f" % R["the hot batch inside its family"]["hot_count"])
    check("R4 one curve over every vault outside", not inside(R["one curve per family over every vault"]["om6"], B["om6"]),
          "%.0f against %s" % (R["one curve per family over every vault"]["om6"], [round(x) for x in B["om6"]]))
    check("R5 Poisson width outside", not inside(R["Poisson counts at the fitted values"]["total_width"], B["total_width"]),
          "%.0f" % R["Poisson counts at the fitted values"]["total_width"])
    check("R6 Poisson coverage outside", not inside(R["Poisson counts at the fitted values"]["coverage"], B["coverage"]),
          "%.3f against %s" % (R["Poisson counts at the fitted values"]["coverage"], [round(x, 3) for x in B["coverage"]]))
    check("R8 the firmware story's flip point outside", not inside(R["the firmware release as the batch"]["rec"]["flip"], B["rec_flip"]),
          "%.1f against %s" % (R["the firmware release as the batch"]["rec"]["flip"], [round(x, 1) for x in B["rec_flip"]]))
    gm = sorted(S["rec"]["migrate"])
    for name in ("the firmware release as the batch", "every batch vault on the batch's share", "careful but hurried",
                 "the hot batch inside its family"):
        check("R8 %s migrates other vaults" % name, sorted(R[name]["rec"]["migrate"]) != gm,
              "%s against %s" % (sorted(R[name]["rec"]["migrate"]), gm))
    line = P.COSTS["migrate_vault"] / P.COSTS["failure_handling"]
    for v, s in sorted(S["vaults"].items()):
        lo = min(x["vaults"][v]["mean"] for x in list(F["rivals"].values()) + [F["gold"]] if v in x["vaults"])
        hi = max(x["vaults"][v]["mean"] for x in list(F["rivals"].values()) + [F["gold"]] if v in x["vaults"])
        far = lo > 1.1 * line if v in gm else hi < 0.9 * line
        check("R8 vault %s clear of the break-even under every rival" % v, far, "%d to %d against %d" % (lo, hi, line))
    # ---- rivals inside every band they set
    for name, v in F["rivals"].items():
        ok = inside(v["dc3"], B["dc3"]) and inside(v["om6"], B["om6"]) and inside(v["hot_count"], B["hot_count"]) and \
            inside(v["total_width"], B["total_width"]) and inside(v["coverage"], B["coverage"]) and \
            inside(v["rec"]["flip"], B["rec_flip"]) and sorted(v["rec"]["migrate"]) == sorted(S["rec"]["migrate"])
        check("rival inside every band: %s" % name, ok)
    # ---- the call's forcing (both sides)
    fc = E["forcing"]
    check("every golden-family variant migrates the same vaults", all(x["answer"] == fc["golden_answer"] for x in fc["golden_family"]),
          "%d variants" % len(fc["golden_family"]))
    check("every listed shortcut migrates other vaults", all(x["answer"] != fc["golden_answer"] for x in fc["shortcuts"]),
          "; ".join("%s %s" % (x["name"][:24], x["answer"]) for x in fc["shortcuts"]))
    check("every perturbation keeps the call", all(x["answer"] == fc["golden_answer"] for x in fc["perturbations"]),
          ", ".join(str(x["answer"]) for x in fc["perturbations"]))
    # ---- the one-fact test
    k = max(len(h["rescues"]) for h in E["hints"])
    check("the largest single hint rescues a third or fewer", k <= len(E["results"]) / 3.0, "%d of %d" % (k, len(E["results"])))
    # ---- the fork table (DESIGN_NOTE.md, Semantic fork table)
    # SF1 a reseat (the serial back within 30 days) is not a replacement: with it counted, the history moves by its count
    n_rma = int(d.rma.sum())
    check("SF1 reseats merged", n_rma > 0, "%d reseats merged into their drive's service life" % n_rma)
    # SF2 health pulls of healthy drives under P2 count as replacements (the wiki's PULL): the golden carries their rate
    check("SF2 healthy-drive pulls carried as replacements", g["spur_rate"] > 0, "%.4f per drive-year" % g["spur_rate"])
    # SF3 the current rate is July to September 2026's replacements per drive-year of the batch
    a_, b_ = AN.qbounds("2026Q3")
    h = d[hot]
    lo = np.maximum(h.entry.values.astype("datetime64[D]"), np.datetime64(a_.date()))
    hi = np.minimum(h.exit.values.astype("datetime64[D]"), np.datetime64((b_ - pd.Timedelta(days=1)).date()))
    ex = np.clip((hi - lo).astype(float), 0, None).sum() / 365.25
    evn = int((h.event & (h.removal_date >= a_) & (h.removal_date < b_)).sum())
    check("SF3 the batch's July to September rate", abs(evn / ex - S["hot_batch"]["rate"]) < 5e-4, "%d over %.1f drive-years" % (evn, ex))
    # SF4 the population: drives in service on 30 September 2026 plus the capacity plan's installs, no further retirement
    later = ev[(ev.date > pd.Timestamp(P.END)) & ev.event_type.str.startswith("DECOM")]
    check("SF4 no retirement scheduled after the record", len(later) == 0)
    # SF5 the break-even share: migration cost over 1,200 drives at the handling cost
    be = P.COSTS["migrate_vault"] / (P.VAULT_DRIVES * P.COSTS["failure_handling"])
    check("SF5 break-even from the procurement file", abs(be * P.VAULT_DRIVES - fc["line"]) < 1e-6, "%.3f of 1,200 drives" % be)
    # SF6 the spare order is the 90th percentile less stock on hand, never below zero
    ok = all(S["spares"][f] == max(int(np.ceil(g["spares_p90"][f])) - P.SPARES_ON_HAND.get(f, 0), 0) for f in S["spares"])
    check("SF6 spare order arithmetic", ok)
    # SF7 coverage counts an actual on either limit as inside, over family-quarter cells of the stayed vaults
    cells = g["backtest_detail"]
    edge = sum(1 for c in cells if c["actual"] in (round(c["lo"]), round(c["hi"])))
    check("SF7 back-test cells", len(cells) == g["backtest_cells"] and len(cells) >= 24, "%d cells, %d on a limit" % (len(cells), edge))
    # SF8 the 80 per cent interval is the 10th to 90th percentile of the predictive draws
    check("SF8 interval is P10 to P90", P.BAND == (10, 90))
    # SF9 the flip doubling holds the July to September rate as the start and doubles it every D months over 24 months
    h0 = S["hot_batch"]["rate"] / 12.0
    D = S["rec"]["flip"]
    H = h0 * D / np.log(2) * (2 ** (24.0 / D) - 1)
    check("SF9 the flip point reproduces the break-even", abs((1 - np.exp(-H)) - be) < 0.005, "share %.4f at %.1f months" % (1 - np.exp(-H), D))
    # ---- the answer blocks state the golden
    sub = open(os.path.join(TASK, "submission.md")).read()
    for key in ("total", "dc3", "om6", "hot_count"):
        check("submission states %s" % key, "{:,}".format(S[key]) in sub, "{:,}".format(S[key]))
    print("%d failed" % len(FAILS))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
