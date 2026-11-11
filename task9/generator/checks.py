"""task9: the generator's assertions on the built pack (task9/target) and its figures. Run after build.py:

    python3 checks.py            # every assertion; exit 1 on any failure

The bar block (dataset-generation 7.1) carries labels R1 to R7; the semantic fork table's rows are asserted as SF1 to
SF15; the input gates and the results' margins follow.
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


def variant(patch):
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


def r1_of(A):
    out = {"points": round(A.R1, 2)}
    out.update({"%s die" % p: round(v, -3) for p, v in A.R1_die.items()})
    return out


def r4_of(fits, A):
    out = {}
    for u in AN.UNITS:
        f = fits[A.pair_of[u]] if A.pair_of[u] in fits else fits[u]
        out["%s onset" % u] = int(round(f["w0"], -1))
        out["%s climb" % u] = round(f["beta"] * 1e5, 1)
    return out


def main():
    F = json.load(open(os.path.join(HERE, "figures.json")))
    E = json.load(open(os.path.join(HERE, "effort.json")))
    B, R, riv = F["bands"], F["routes"], F["rivals"]
    A = AN.Analysis(TGT)

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
    check("gate: the distractors are never read by the golden", not any(('F["%s"]' % k) in src for k in ("sc4", "slurry", "particles")))
    check("gate: no file describes the data (readme, dictionary, manifest, notes)",
          not any(w in n.lower() for n in names for w in ("readme", "dictionary", "manifest", "notes", "codebook", "schema")))
    check("gate: no file name carries the trap or the word distractor",
          not any(w in n.lower() for n in names for w in ("distractor", "decoy", "trap", "answer", "ring_loss", "latent", "lot_wear")))

    # ------------------------------------------------------------------ the semantic forks
    d = A.d
    check("SF1 the ring was already costing yield before April", A.R1_q1 > 0.15, "January to March %.3f points" % A.R1_q1)
    young = d[d.wear < 0.5]
    check("SF1 the fallout on disks short of their onset is the fits' no-ring level",
          abs(np.average(young.y, weights=young.tested_band) - np.average(d.r0, weights=d.tested_band)) < 0.004)
    raw = pd.read_csv(os.path.join(TGT, PK.F["sort"]), usecols=["wafer_id", "retest"])
    check("SF2 retests supersede the first pass", (raw.retest == "Y").sum() > 300 and raw.wafer_id.duplicated().sum() == (raw.retest == "Y").sum())
    pol = d[(d.polish_ts >= "2026-04-01") & (d.polish_ts < "2026-09-01")]
    check("SF3 the window is by sort date, and polish dates would select other wafers", abs(len(pol) - A.n_win) > 500,
          "%d sorted against %d polished" % (A.n_win, len(pol)))
    ft_raw = pd.read_csv(os.path.join(TGT, PK.F["ft"]), dtype={"sub_lot": str}, keep_default_na=False)
    sorted_lots = set(d[d.win].lot_id)
    tested = set(A.R.ft[(A.R.ft.ft_date >= AN.WIN[0]) & (A.R.ft.ft_date < AN.WIN[1])].lot_id)
    check("SF4 final test's window is by its own date, sub-lots added back", (ft_raw.sub_lot != "").sum() > 40 and
          len(sorted_lots - set(A.R.ft.lot_id)) > 20 and len(tested - sorted_lots) > 20,
          "%d split rows, %d window lots not yet tested, %d tested lots sorted before April" % (
              (ft_raw.sub_lot != "").sum(), len(sorted_lots - set(A.R.ft.lot_id)), len(tested - sorted_lots)))
    diff = (d.disk != d.full).mean()
    check("SF5 the disk's own usage and wafers since the full PM part on a share of wafers", diff > 0.05, "%.1f per cent" % (100 * diff))
    past = d[d.disk > 650]
    check("SF5 the polish record's pad counter is not the disk's usage", (past.pad_life_ctr != past.disk).mean() > 0.99)
    check("SF6 every unit's current disk is from one lot, the only lot with stock left", bool(A.fwd_lot) and
          all(v <= 0 for k, v in A.stock_left.items() if k != A.fwd_lot) and A.stock_left[A.fwd_lot] > 10, str(A.stock_left))
    check("SF7 each disk lot ran on both pairs", all(d[d.disk_lot == L].pair.nunique() == 2 for L in A.lot_names))
    spec = open(os.path.join(TGT, PK.F["spec"])).read()
    check("SF8 the spec's Rev G draft takes the part out of the full PM", "comes out of the full PM scope" in spec)
    costs = open(os.path.join(TGT, PK.F["costs"])).read()
    check("SF9 the cost inputs file the costing of a part moved out of the full PM, and the plan's volume and mix",
          "Rev G review" in costs and "less that part's price" in costs and "wafers_per_year_by_unit" in costs and "product_mix" in costs)
    check("SF10 the cost inputs file what a unit scrapped at final test costs", "assembly_and_test_per_unit" in costs and
          "scrapped at final test" in costs)
    check("SF11 the summer's own rate as Rev F's lands outside the saving's band", not inside(R["R5_summer_rate"], B["R5_saving"]))
    check("SF12 the summer's unit shares keep the saving inside its band", inside(riv["R5"]["each unit's share of the summer's wafers"], B["R5_saving"]))
    uf = R["R4_unit_fwd"]
    short = [u for u in AN.UNITS if d[(d.unit == u) & d.fwd].disk.max() < 1500]
    check("SF13 each unit's own fit on the current lot is inside R4's bands where the unit ran a long disk of it",
          all(inside(int(round(uf[u][0], -1)), B["R4_dose"]["%s onset" % u]) and inside(round(uf[u][1] * 100, 1), B["R4_dose"]["%s climb" % u])
              for u in AN.UNITS if u not in short) and len(short) == 2, "short: %s" % ", ".join(short))
    check("SF13 every unit's own count on the current lot is inside the count's band",
          all(inside(R["REC_unit_fwd"][u], B["REC_counts"][u]) for u in AN.UNITS))
    check("SF14 one joint fit over every lot gives the retaining ring a share below zero (read as none)", R["R2_joint"]["ring"] < 0)
    check("SF15 every final-test lot is one product at sort", d.groupby("lot_id")["product"].nunique().max() == 1)

    # ------------------------------------------------------------------ the bar block
    sort_cols = pd.read_csv(os.path.join(TGT, PK.F["sort"]), nrows=2).columns
    check("R1 the sort record ships zone fail and tested counts on every wafer",
          all("fail_z%d" % k in sort_cols and "tested_z%d" % k in sort_cols for k in range(1, 9)))
    shipped = " ".join(pd.read_csv(os.path.join(TGT, n), nrows=1).columns.str.lower().str.cat(sep=" ") for n in names if n.endswith(".csv"))
    check("R1 no shipped column holds a result", not any(w in shipped for w in ("ring_loss", "excess", "disk_life", "disk_usage", "share",
                                                                                  "latent", "disk_lot", "wear")))
    check("R1 each part's usage exists only as the log's free-text entries", "disk" not in " ".join(pd.read_csv(os.path.join(TGT, PK.F["fdc"]), nrows=1).columns))
    check("R1 a disk's lot exists only as its fitted serial and the receipts' serial ranges",
          "lot" not in " ".join(pd.read_csv(os.path.join(TGT, PK.F["fdc"]), nrows=1).columns) and
          "supplier_lot" in pd.read_csv(os.path.join(TGT, PK.F["stores"]), nrows=1).columns)
    check("R1 final test ships lot totals only", "wafer_id" not in ft_raw.columns)

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

    def dropped(self):
        RC.Record._pm_rows(self, drop_blank=True)

    def by_time(self):
        RC.Record._pm_rows(self, back_by_time=True)
    # each mess item mishandled moves at most the assembly result that grades it (R4: each disk's life and lot are
    # assembled from the log's entries and the receipts) and leaves every other result inside its band
    for label, patch, grades in (("R2 retests mishandled (the first pass kept)", {"_sort": first_record}, None),
                                 ("R2 aliases left unmapped (their wafers dropped)", {"_sort": unmapped}, None),
                                 ("R2 blank maintenance counters dropped", {"_pm": dropped}, "R4"),
                                 ("R2 back-entered rows placed by their entry time", {"_pm": by_time}, "R4")):
        V = variant(patch)
        vals = {"R1": cells_inside(r1_of(V), B["R1_loss"])[0] == len(B["R1_loss"]),
                "R3": all(inside(round(V.R3.get(p, 0), -2), B["R3_ft_units"][p]) for p in B["R3_ft_units"]),
                "R4": cells_inside(r4_of(V.fwd_fit, V), B["R4_dose"])[0] == len(B["R4_dose"]),
                "REC": all(inside(V.REC[u], B["REC_counts"][u]) for u in AN.UNITS),
                "R5": inside(V.R5, B["R5_saving"])}
        moved = [k for k, v in vals.items() if not v]
        check(label + " leaves every result %sinside its band" % ("but the assembly result it grades (%s) " % grades if grades else ""),
              all(k == grades for k in moved), ", ".join(moved) or "none moved out")

    for r in E["results"]:
        g = r["passes"]["careful"]
        ok_in = inside(g, r["band"]) if "band" in r else cells_inside(g, r["bands"])[0] == len(r["bands"])
        if r["id"] in ("R1", "R2"):
            check("R3 the careful pass lands inside %s's band (earned)" % r["id"], ok_in)
        else:
            check("R3 the careful pass lands outside %s's band (%s)" % (r["id"], ",".join(r.get("precedent", []))), not ok_in)
    blobs = {}
    for f in files:
        h = hash(open(os.path.join(TGT, f), "rb").read())
        blobs.setdefault(h, []).append(f)
    check("R4 no file is a copy of another", all(len(v) == 1 for v in blobs.values()))
    tick = open(os.path.join(TGT, PK.F["ticket"])).read()
    check("R4 the ticket states no loss figure and names no suspect", not any(w in tick for w in ("points", "disk", "PU-3", "DEP-3", "SC-4", "Rev F",
                                                                                                "burn-in", "final test", "lot A165")))
    docs = spec + tick + costs
    check("R4 no document ranks a cause, proposes a count, names a lot's wear or ties burn-in to the ring",
          not any(w in docs for w in ("1,0", "L2603", "L2511", "L2509", "burn-in", "latent", "faster")) and "count" not in tick)
    slopes = {u: A.unit_fit[u]["beta"] for u in AN.UNITS}
    check("R5 the disk's effect shows on every unit", all(v > 0 for v in slopes.values()), ", ".join("%s %.2e" % kv for kv in slopes.items()))
    dep3 = d[d.dep == "DEP-3"].unit.value_counts(normalize=True)
    check("R5 DEP-3's wafers reach every unit, not only the high pair", all(dep3.get(u, 0) > 0.05 for u in AN.UNITS))
    sc4 = d[d.sc4 == 1].unit.value_counts(normalize=True)
    check("R5 SC-4's lots reach every unit", all(sc4.get(u, 0) > 0.1 for u in AN.UNITS))
    check("R5 every disk lot ran on at least three units, the current lot on all four",
          all(d[d.disk_lot == L].unit.nunique() >= 3 for L in A.lot_names) and d[d.fwd].unit.nunique() == 4)
    ratio = {p: A.old_fit[p]["w0"] / A.fwd_fit[p]["w0"] for p in A.pairs}
    check("R5 the current lot's earlier onset shows on both pairs", all(v > 1.25 for v in ratio.values()),
          ", ".join("%s %.2f" % kv for kv in ratio.items()))
    check("R5 the lots' split decides nothing at the loss: one fit over every lot keeps it inside its band",
          cells_inside({"points": round(R["R1_pooled"], 2), **{"%s die" % p: round(v, -3) for p, v in R["R1_die_pooled"].items()}},
                       B["R1_loss"])[0] == len(B["R1_loss"]))
    ftm = F["ft_monthly"]
    check("R5 final test's losses show in every month and every product, the first quarter included",
          all(v["ring_pct"] > 0.05 for m, v in ftm.items() if m >= "2026-02") and all(v > 1000 for v in A.R3.values()),
          ", ".join("%s %.2f" % (m, v["ring_pct"]) for m, v in sorted(ftm.items())))
    q1 = d[d.q1]
    q1p = {p: float(np.mean(g.ring_die / g.gross) * 100) for p, g in q1.groupby("pair")}
    check("R5 the ring before April shows on both pairs", all(v > 0.05 for v in q1p.values()), ", ".join("%s %.3f" % kv for kv in q1p.items()))
    rescue = max(len(h["rescues"]) for h in E["hints"])
    check("R6 no single hint rescues more than a third of the results", rescue <= len(E["results"]) / 3.0, "%d of %d" % (rescue, len(E["results"])))
    gold = {r["id"]: r for r in E["results"]}
    check("R6 each hint's rescued results land inside their bands at the golden", all(
        (inside(gold[x]["golden"], gold[x]["band"]) if "band" in gold[x] else cells_inside(gold[x]["golden"], gold[x]["bands"])[0] == len(gold[x]["bands"]))
        for h in E["hints"] for x in h["rescues"]))
    r1v = [v[0] for v in riv["R1"].values()]
    check("R7 every fallout rival lands inside R1's band", all(
        cells_inside({"points": round(v[0], 2), **{"%s die" % p: round(x, -3) for p, x in v[1].items()}}, B["R1_loss"])[0] == len(B["R1_loss"])
        for v in riv["R1"].values()), ", ".join("%.3f" % v for v in r1v))
    check("R7 every share rival lands inside R2's bands", all(cells_inside({k: round(x, 3) for k, x in v.items()}, B["R2_shares"])[0] == 6
                                                            for v in riv["R2"].values()))
    check("R7 every final-test rival lands inside R3's bands", all(all(inside(round(v[p], -2), B["R3_ft_units"][p]) for p in B["R3_ft_units"])
                                                                for v in riv["R3"].values()))
    check("R7 every dose rival lands inside R4's bands", all(
        all(inside(int(round(v[u][0], -1)), B["R4_dose"]["%s onset" % u]) and inside(round(v[u][1] * 100, 1), B["R4_dose"]["%s climb" % u])
            for u in AN.UNITS) for v in riv["R4"].values()))
    check("R7 every count rival lands inside the count's bands", all(inside(v[u], B["REC_counts"][u]) for v in riv["REC"].values() for u in AN.UNITS))
    check("R7 every saving rival lands inside R5's band", all(inside(v, B["R5_saving"]) for v in riv["R5"].values()),
          ", ".join("%.0f" % v for v in riv["R5"].values()))

    # ------------------------------------------------------------------ the results' own margins
    check("result: the shortcuts on the loss all land outside its band", not any(inside(round(R[k], 2), B["R1_loss"]["points"]) for k in (
        "R1_q1_baseline", "R1_labels", "R1_no_rolloff", "R1_diemap_sample", "R1_before_after")))
    check("result: the shortcuts on final test all land outside its bands", all(
        not all(inside(round(R[k][p], -2), B["R3_ft_units"][p]) for p in B["R3_ft_units"]) for k in ("R3_proportional", "R3_clean_lot_base", "R3_q1_base")))
    for k in ("R4_pooled", "R4_old_lots", "R4_unit", "R4_fleet", "R4_linear"):
        cells = r4_of({u: dict(w0=v[0], beta=v[1] / 1000) for u, v in R[k].items()}, A)
        check("result: %s puts every unit's onset outside its band" % k, not any(inside(cells["%s onset" % u], B["R4_dose"]["%s onset" % u])
                                                                                 for u in AN.UNITS), str(cells))
    for k in ("REC_pooled", "REC_sort_only", "REC_proportional", "REC_pooled_proportional", "REC_pooled_sort_only", "REC_old_lots",
              "REC_fleet_sort_only", "REC_linear"):
        check("result: %s lands outside both pairs' count bands" % k, not any(inside(R[k][u], B["REC_counts"][u]) for u in AN.UNITS),
              ", ".join("%s %d" % (u, R[k][u]) for u in AN.UNITS))
    for k in ("R5_pooled", "R5_sort_only", "R5_pooled_proportional", "R5_pooled_sort_only", "R5_summer_rate"):
        check("result: %s lands outside the saving's band" % k, not inside(R[k], B["R5_saving"]), "%.0f" % R[k])
    t = R["R2_joint_ring_t"]
    check("result: the retaining ring's t is large on the wafers and small on the disk lives",
          all(abs(v[0]) > 5 and abs(v[1]) < 2 for v in t.values()), str(t))
    steps = [s[2] for s in A.ring_swaps]
    check("result: the ring-only swaps show no step", len(steps) == 6 and abs(np.mean(steps)) < 0.005 and max(abs(x) for x in steps) < 0.012,
          ", ".join("%+.4f" % x for x in steps))
    check("result: the two pairs' onsets differ by more than a fifth", A.onset["PU-1"] / A.onset["PU-3"] > 1.2)
    check("result: final test's loss starts before the ring at sort on both pairs", A.ft["u0"] < 0.8 and A.ft["u0"] + A.ft["us"] < 1.0)
    check("result: final test's model reads the observed burn-in to within 3 per cent", all(
        abs(A.R3_observed[p] - A.R3[p]) / A.R3[p] < 0.03 for p in A.R3))
    check("result: Rev G beats Rev F on both pairs and the counts beat counts set on every lot's curve",
          all(F["cost_per_wafer"][p]["Rev F as it stands"] > F["cost_per_wafer"][p]["Rev G at the pair's count"] for p in A.pairs)
          and F["pooled_vs_g"] > 0)
    check("result: every perturbation keeps each count inside its band", all(inside(v[u], B["REC_counts"][u]) for v in F["perturbations"].values()
                                                                           for u in AN.UNITS))
    check("result: the counters rebuild every reset the log records", (A.R.fdc.disk.isna().sum() == 0) and (A.R.fdc.pad.isna().sum() == 0))
    check("result: every wafer's disk maps to a received lot", d.disk_lot.notna().all())
    print("%d passed, %d failed" % (len(PASSES), len(FAILS)))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
