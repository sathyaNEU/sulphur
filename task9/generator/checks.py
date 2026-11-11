"""task9: the generator's assertions on the built pack (task9/target) and its figures. Run after build.py:

    python3 checks.py            # every assertion; exit 1 on any failure

The bar block (dataset-generation 7.1) carries labels R1 to R7; the semantic fork table's rows are asserted as SF1 to
SF13; the input gates and the results' margins follow.
"""
import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import analysis as AN  # noqa: E402
import pack as PK  # noqa: E402
import record as RC  # noqa: E402

TGT = os.path.join(TASK, "target")
FAILS, PASSES = [], []


def check(label, ok, detail=""):
    (PASSES if ok else FAILS).append(label)
    print("%s  %s%s" % ("PASS" if ok else "FAIL", label, ("  (%s)" % detail) if detail else ""))


def inside(v, b):
    return v is not None and v == v and b[0] <= v <= b[1]


def cells_inside(vals, bands):
    return sum(1 for k, b in bands.items() if inside(vals.get(k), b)), len(bands)


def variant(name, patch):
    """The golden method run with one mess item mishandled: the record class patched, the analysis rerun."""
    orig = {k: getattr(RC.Record, k) for k in patch}
    for k, f in patch.items():
        setattr(RC.Record, k, f)
    try:
        A = AN.Analysis(TGT)
    finally:
        for k, f in orig.items():
            setattr(RC.Record, k, f)
    return A


def main():
    F = json.load(open(os.path.join(HERE, "figures.json")))
    E = json.load(open(os.path.join(HERE, "effort.json")))
    B, R = F["bands"], F["routes"]
    A = AN.Analysis(TGT)
    S = {k: F[k] for k in ("R1_points", "R2_die", "R3_shares", "R4_dose", "R5_bridge", "R6_counts", "R7_saving")}

    # ------------------------------------------------------------------ input gates
    names = sorted(os.listdir(TGT))
    files = [n for n in names if os.path.isfile(os.path.join(TGT, n))] + \
        [os.path.join(n, x) for n in names if os.path.isdir(os.path.join(TGT, n)) for x in os.listdir(os.path.join(TGT, n))]
    check("gate: ten or more usable files", len(files) >= 10, "%d files" % len(files))
    cats = {("spreadsheet" if f.endswith((".csv", ".xlsx")) else "database" if f.endswith(".sqlite") else "code" if
             f.endswith((".py", ".yaml")) else "image" if f.endswith(".png") else "text") for f in files}
    check("gate: two or more file categories", len(cats) >= 2, ", ".join(sorted(cats)))
    rows = {n: sum(1 for _ in open(os.path.join(TGT, n))) - 1 for n in names if n.endswith(".csv")}
    big = sorted(rows.items(), key=lambda kv: -kv[1])
    check("gate: a CSV of 20,000 rows or more", big[0][1] >= 20000, "%s %d" % big[0])
    check("gate: a second large CSV (10 to 20 printed pages or more)", big[1][1] >= 1000, "%s %d" % big[1])
    check("gate: two or more distractors shipped", all(d in names for d in PK.DISTRACTORS) and len(PK.DISTRACTORS) >= 2,
          ", ".join(PK.DISTRACTORS))
    src = open(os.path.join(HERE, "analysis.py")).read() + open(os.path.join(HERE, "record.py")).read()
    check("gate: the distractors are never read by the golden", not any(('F["%s"]' % k) in src for k in ("sc4", "slurry")))
    check("gate: no file describes the data (readme, dictionary, manifest, notes)",
          not any(w in n.lower() for n in names for w in ("readme", "dictionary", "manifest", "notes", "codebook", "schema")))
    check("gate: no file name carries the trap or the word distractor",
          not any(w in n.lower() for n in names for w in ("distractor", "decoy", "trap", "answer", "ring_loss")))

    # ------------------------------------------------------------------ the semantic forks
    d = A.d
    check("SF1 the ring was already costing yield before April", A.R1_q1 > 0.15, "January to March %.3f points" % A.R1_q1)
    check("SF1 the fallout at a fresh disk is the band's no-ring level", abs(np.average(d[d.disk < 400].y, weights=d[d.disk < 400].tested_band)
                                                                     - np.mean(list(A.r0.values()))) < 0.006)
    raw = pd.read_csv(os.path.join(TGT, PK.F["sort"]), usecols=["wafer_id", "retest"])
    check("SF2 retests supersede the first pass", (raw.retest == "Y").sum() > 300 and raw.wafer_id.duplicated().sum() == (raw.retest == "Y").sum())
    pol = d[(d.polish_ts >= "2026-04-01") & (d.polish_ts < "2026-09-01")]
    check("SF3 the window is by sort date, and polish dates would select other wafers", abs(len(pol) - A.n_win) > 500,
          "%d sorted against %d polished" % (A.n_win, len(pol)))
    ok4 = all(inside(F["rivals"]["R4"]["each unit's own fit"][u]["onset"], B["R4_dose"]["%s onset" % u]) and
              inside(round(F["rivals"]["R4"]["each unit's own fit"][u]["slope"] * 100, 1), B["R4_dose"]["%s slope" % u]) for u in AN.UNITS)
    check("SF4 each unit's own fit lands inside every dose band", ok4)
    diff = (d.disk != d.full).mean()
    check("SF5 the disk's own usage and wafers since the full PM part on a share of wafers", diff > 0.10, "%.1f per cent" % (100 * diff))
    past = d[d.disk > 650]
    check("SF5 the polish record's pad counter is not the disk's usage", (past.pad_life_ctr != past.disk).mean() > 0.99,
          "past the first pad change on a disk, %.1f per cent differ" % (100 * (past.pad_life_ctr != past.disk).mean()))
    check("SF6 the bridge's shares add to the loss", abs(sum(A.R5.values()) - 1) < 1e-9)
    sl_in, sl_n = cells_inside(R["R5_slice"], B["R5_bridge"])
    check("SF7 the sliced bridge misses two or more of the three shares", sl_n - sl_in >= 2, "%d of %d inside" % (sl_in, sl_n))
    spec = open(os.path.join(TGT, PK.F["spec"])).read()
    check("SF8 the spec's Rev G draft takes the part out of the full PM", "comes out of the full PM scope" in spec)
    costs = open(os.path.join(TGT, PK.F["costs"])).read()
    check("SF9 the cost inputs file the costing of a part moved out of the full PM", "spec_changes" in costs and "less that part's price" in costs)
    check("SF10 the window's mix keeps every count inside its band", all(inside(F["rivals"]["R6"]["the April to August mix"][u], B["R6_counts"][u])
                                                                       for u in AN.UNITS))
    check("SF11 the summer's own rate as Rev F's lands outside the saving's band", not inside(R["R7_summer_rate"], B["R7_saving"]),
          "%.0f against %s" % (R["R7_summer_rate"], B["R7_saving"]))
    check("SF12 the window's unit shares keep the saving inside its band", inside(F["rivals"]["R7"]["each unit's share of April to August"], B["R7_saving"]))
    check("SF13 the pad's share under Shapley stays inside its band", inside(S["R3_shares"]["pad"] / 2, B["R3_shares"]["pad"]))

    # ------------------------------------------------------------------ the bar block
    sort_cols = pd.read_csv(os.path.join(TGT, PK.F["sort"]), nrows=2).columns
    check("R1 the sort record ships zone fail and tested counts on every wafer",
          all("fail_z%d" % k in sort_cols and "tested_z%d" % k in sort_cols for k in range(1, 9)))
    shipped = " ".join(pd.read_csv(os.path.join(TGT, n), nrows=1).columns.str.lower().str.cat(sep=" ") for n in names if n.endswith(".csv"))
    check("R1 no shipped column holds a result", not any(w in shipped for w in ("ring_loss", "excess", "disk_life", "disk_usage", "share")))
    check("R1 each part's usage exists only as the log's free-text entries", "disk" not in " ".join(pd.read_csv(os.path.join(TGT, PK.F["fdc"]), nrows=1).columns))

    def first_record(self):
        s = pd.read_csv(os.path.join(self.tgt, PK.F["sort"]))
        s["sort_ts"] = pd.to_datetime(s.sort_end_ts)
        s = s.sort_values(["wafer_id", "sort_ts"]).groupby("wafer_id", as_index=False).first()
        s["product"] = s["product"].str.strip().map(RC.CANON)
        self._finish_sort(s)
    def unmapped(self):
        s = pd.read_csv(os.path.join(self.tgt, PK.F["sort"]))
        s["sort_ts"] = pd.to_datetime(s.sort_end_ts)
        s = s.sort_values(["wafer_id", "sort_ts"]).groupby("wafer_id", as_index=False).last()
        s = s[s["product"].isin(["P-A", "P-B", "P-C"])].copy()
        self._finish_sort(s)
    import openpyxl
    def dropped(self):
        RC.Record._pm_rows(self, drop_blank=True)
    def by_time(self):
        RC.Record._pm_rows(self, back_by_time=True)
    for label, patch, keep in (("R2 retests mishandled (the first pass kept)", {"_sort": first_record}, "all"),
                               ("R2 aliases left unmapped (their wafers dropped)", {"_sort": unmapped}, "all"),
                               ("R2 blank maintenance counters dropped", {"_pm": dropped}, "all"),
                               ("R2 back-entered rows placed by their entry time", {"_pm": by_time}, "all")):
        V = variant(label, patch)
        vals = {"R1": inside(round(V.R1, 2), B["R1_points"]),
                "R2": all(inside(round(V.R2[p], -3), B["R2_die"][p]) for p in B["R2_die"]),
                "R4": all(inside(int(round(V.onset[u], -1)), B["R4_dose"]["%s onset" % u]) for u in AN.UNITS),
                "R5": all(inside(V.R5[k], B["R5_bridge"][k]) for k in B["R5_bridge"]),
                "R6": all(inside(V.R6[u], B["R6_counts"][u]) for u in AN.UNITS),
                "R7": inside(V.R7, B["R7_saving"])}
        check(label + " leaves every result inside its band", all(vals.values()), ", ".join(k for k, v in vals.items() if not v) or "none moved out")

    for r in E["results"]:
        g = r["passes"]["careful"]
        if r["id"] in ("R4", "R6"):
            ok = inside(g, r["band"]) if "band" in r else cells_inside(g, r["bands"])[0] == len(r["bands"])
            check("R3 the careful pass lands inside %s's band (earned)" % r["id"], ok)
        else:
            ok = (not inside(g, r["band"])) if "band" in r else cells_inside(g, r["bands"])[0] < len(r["bands"])
            check("R3 the careful pass lands outside %s's band (%s)" % (r["id"], ",".join(r.get("precedent", []))), ok)
    blobs = {}
    for f in files:
        h = hash(open(os.path.join(TGT, f), "rb").read())
        blobs.setdefault(h, []).append(f)
    check("R4 no file is a copy of another", all(len(v) == 1 for v in blobs.values()))
    tick = open(os.path.join(TGT, PK.F["ticket"])).read()
    check("R4 the ticket states no loss figure and names no suspect", not any(w in tick for w in ("points", "disk", "PU-3", "DEP-3", "SC-4", "Rev F")))
    check("R4 no document ranks a cause or proposes a count", not any(w in spec for w in ("1,5", "1,2")) and "count" not in tick)
    slopes = {u: A.unit_fit[u]["beta"] for u in AN.UNITS}
    check("R5 the disk's effect shows on every unit", all(v > 0 for v in slopes.values()), ", ".join("%s %.2e" % kv for kv in slopes.items()))
    dep3 = d[d.dep == "DEP-3"].unit.value_counts(normalize=True)
    check("R5 DEP-3's wafers reach every unit, not only the high pair", all(dep3.get(u, 0) > 0.05 for u in AN.UNITS))
    sc4 = d[d.sc4 == 1].unit.value_counts(normalize=True)
    check("R5 SC-4's lots reach every unit", all(sc4.get(u, 0) > 0.1 for u in AN.UNITS))
    ew = A.R.events[A.R.events.waiver.fillna("").astype(str).str.contains("EW-118")]
    check("R5 the waiver's retained disks are on every unit", sorted(ew.unit.unique()) == AN.UNITS)
    q1 = d[d.q1]
    q1p = {p: float(np.mean(g.ring_die / g.gross) * 100) for p, g in q1.groupby("pair")}
    check("R5 the ring before April shows on both pairs", all(v > 0.05 for v in q1p.values()), ", ".join("%s %.3f" % kv for kv in q1p.items()))
    spread = {p: float(np.std([v for k, v in A.life[p]["betas"].items() if v > 0]) / np.mean([v for v in A.life[p]["betas"].values() if v > 0]))
              for p in A.pairs}
    check("R5 the disk lives' own rates vary on both pairs", all(v > 0.05 for v in spread.values()), ", ".join("%s %.2f" % kv for kv in spread.items()))
    rescue = max(len(h["rescues"]) for h in E["hints"])
    check("R6 no single hint rescues more than a third of the results", rescue <= len(E["results"]) / 3.0, "%d of %d" % (rescue, len(E["results"])))
    gold = {r["id"]: r["golden"] for r in E["results"]}
    check("R6 each hint's rescued results land inside their bands at the golden", all(
        (inside(gold[x], r["band"]) if "band" in r else cells_inside(gold[x], r["bands"])[0] == len(r["bands"]))
        for h in E["hints"] for x in h["rescues"] for r in E["results"] if r["id"] == x))
    r1 = [v[0] for v in F["rivals"]["R1"].values()]
    check("R7 every fallout rival lands inside R1's band", all(inside(round(v, 2), B["R1_points"]) for v in r1), ", ".join("%.3f" % v for v in r1))
    check("R7 every bridge rival lands inside R5's bands", all(cells_inside(v, B["R5_bridge"])[0] == 3 for v in F["rivals"]["R5"].values()))
    check("R7 every count rival lands inside R6's bands", all(inside(v[u], B["R6_counts"][u]) for v in F["rivals"]["R6"].values() for u in AN.UNITS))
    check("R7 every saving rival lands inside R7's band", all(inside(v, B["R7_saving"]) for v in F["rivals"]["R7"].values()))
    check("R7 every share rival lands inside R3's bands", all(cells_inside(v, B["R3_shares"])[0] == 6 for v in F["rivals"]["R3"].values()))
    check("R7 every dose rival lands inside R4's bands", all(
        all(inside(int(round(v[u]["onset"], -1)), B["R4_dose"]["%s onset" % u]) and inside(round(v[u]["slope"] * 100, 1), B["R4_dose"]["%s slope" % u])
            for u in AN.UNITS) for v in F["rivals"]["R4"].values()))

    # ------------------------------------------------------------------ the results' own margins
    check("result: the shortcuts on the loss all land outside its band", not any(inside(round(R[k], 2), B["R1_points"]) for k in (
        "R1_q1_baseline", "R1_labels", "R1_no_rolloff", "R1_diemap_sample", "R1_before_after")))
    t = R["R3_joint_ring_t"]
    check("result: the retaining ring's t is large on the wafers and small on the disk lives",
          all(v[0] > 5 and abs(v[1]) < 2 for v in t.values()), str(t))
    steps = [s[2] for s in A.ring_swaps]
    check("result: the ring-only swaps show no step", len(steps) == 6 and abs(np.mean(steps)) < 0.005 and max(abs(x) for x in steps) < 0.012,
          ", ".join("%+.4f" % x for x in steps))
    check("result: the joint fit's ring share lands outside its band", not inside(R["R3_joint"]["ring"], B["R3_shares"]["ring"]))
    check("result: the two pairs' onsets differ by more than a fifth", A.onset["PU-1"] / A.onset["PU-3"] > 1.2)
    fl = R["R6_fleet"]["PU-1"]
    check("result: one fleet count lands outside both pairs' bands", not inside(fl, B["R6_counts"]["PU-1"]) and not inside(fl, B["R6_counts"]["PU-3"]),
          "%.0f" % fl)
    check("result: a dose from zero lands outside both pairs' bands", not any(inside(R["R6_linear"][u], B["R6_counts"][u]) for u in AN.UNITS))
    check("result: moving the full PM lands outside both pairs' bands", not any(inside(R["R6_full_pm_lever"][u], B["R6_counts"][u]) for u in AN.UNITS))
    check("result: Rev G beats a return to Rev E and one fleet count", F["rev_e_vs_g"] > 0 and F["fleet_vs_g"] > 0)
    check("result: every perturbation keeps each count inside its band", all(inside(v[u], B["R6_counts"][u]) for v in F["perturbations"].values()
                                                                           for u in AN.UNITS))
    check("result: the bridge's model total is the measured loss", abs(A.L["actual"] - A.R1) / A.R1 < 0.05, "%.3f against %.3f" % (A.L["actual"], A.R1))
    check("result: the counters rebuild every reset the log records", (A.R.fdc.disk.isna().sum() == 0) and (A.R.fdc.pad.isna().sum() == 0))
    print("%d passed, %d failed" % (len(PASSES), len(FAILS)))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
