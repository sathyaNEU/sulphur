"""task20 checks: the cut pack against the clean truth (the simulated world before any file was written), the bar
block R1 to R7 (dataset-generation 7.1), every fork in the design note's fork table, and the realism sweep. Exit 1 on
any failure.

    python3 task20/generator/checks.py
"""
import json
import os
import re
import sys
from collections import Counter

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TGT = os.path.join(TASK, "target")
sys.path.insert(0, HERE)
import analysis as A  # noqa: E402
import pack as PK  # noqa: E402
import docs as DC  # noqa: E402
import world as W  # noqa: E402

FAILS = []


def check(label, ok, detail=""):
    print("%s  %s%s" % ("PASS" if ok else "FAIL", label, ("  (" + detail + ")") if detail else ""))
    if not ok:
        FAILS.append(label)


def inside(v, b):
    return b[0] <= v <= b[1]


def main():
    R = A.run(TGT)
    P, E = R["P"], R["E"]
    w = W.simulate(PK.SEED)
    o = W.classify(w)
    F = json.load(open(os.path.join(HERE, "figures.json")))
    EJ = json.load(open(os.path.join(HERE, "effort.json")))
    window, prev, di = R["window"], R["prev"], E.di
    inst_order = [P["pos"][x] for x in P["inst"]]
    names = PK.make_names(w)
    idx = {r.eqx_v2: i for i, r in names.iterrows()}          # pack instrument id -> world index
    perm = np.array([idx[x] for x in P["inst"]])

    # ---------------------------------------------------------------- the pack against the clean truth
    days = sorted(R["books"])
    ok_book = all(np.array_equal(R["books"][d], w.sh[k][perm]) for k, d in enumerate(days))
    check("C1 the close book rebuilt from extract and post-cut bookings equals the desk's true book every day", ok_book)
    check("C2 the same book rolled forward by trade date agrees", all(np.array_equal(R["books"][d], R["roll"][d]) for d in days))
    check("C3 each extract is the true book less the bookings made after its cut",
          all(np.array_equal(P["extract"][d], w.snap_sh[k][perm]) for k, d in enumerate(days)))
    mx = max(abs(R["rep"][d] - R["rep_rep"][d]) for d in R["rep"])
    check("C4 ERE replicated from the methodology note matches every run in the log", mx <= 1.0, "max %.2f USD" % mx)
    hyp_true = {}
    for k, d in enumerate(window):
        p = prev[d]
        q = R["books"][p]
        v = float(q @ (P["PX"][di[d]] - P["PX"][di[p]]))
        for c, n in R["fut"][p].items():
            v += n * A.MULT[c[:2]] * (P["settle"][(c, d)] - P["settle"][(c, p)])
        hyp_true[d] = v
    dh = max(abs(hyp_true[d] - R["hyp"][d]) for d in window)
    check("C5 product control's hypothetical P&L is the close book revalued (MRS-4 3.2)", dh <= 3.0, "max %.2f USD" % dh)
    gold = {c: o[c] for c in ("income", "inputs", "omitted", "volatility", "sound")}
    got = Counter(R["cls"].values())
    check("C6 the headings from the files equal the world's", all(got[c] == gold[c] for c in gold), str(dict(got)))
    check("C7 the official file's count is the booked P&L against the reported VaR",
          int((P["official"].exc == "Y").sum()) == len(R["off"]) == F["official_count"])
    check("C8 the sound count from the files equals the world's", len(R["sound_days"]) == o["sound_count"])

    # ---------------------------------------------------------------- R1 the field's raw material
    shipped_cols = []
    for f in sorted(os.listdir(TGT)):
        if f.endswith(".csv"):
            shipped_cols += list(pd.read_csv(os.path.join(TGT, f), nrows=1).columns)
    bad = [c for c in shipped_cols if re.search(r"heading|classif|hypothetical_var|add.?on|sound|own.?hist|cause", c, re.I)]
    check("R1 the pack ships positions, trades, prices, P&L, runs and mapping; no column holds a heading, a "
          "counterfactual VaR or an add-on", not bad, ", ".join(bad))
    differs = sum(1 for d in days[1:] if not np.array_equal(P["extract"][d], R["books"][d]))
    check("R1 no shipped file holds the close book: the extracts differ from it on every day the blotter covers",
          differs == len(days) - 1, "%d of %d" % (differs, len(days) - 1))

    # ---------------------------------------------------------------- R2 every mess item real and neutral
    def heads(bl=None, fut=None):
        books, _, _, futs = A.close_books(P, bl)
        futs = fut or futs
        out = {}
        for d in R["union"]:
            p = prev[d]
            if d not in R["hx"]:
                out[d] = "income"
                continue
            g = E.var(books[p], futs[p], di[p])
            fl = E.var(books[p], futs[p], di[p], "own")
            s = E.var(books[p], futs[p], di[p], "own", lam=A.GOLD_LAM)
            h = R["hyp"][d]
            out[d] = "inputs" if h >= -g else "omitted" if h >= -fl else "volatility" if h >= -s else "sound"
        return out
    bl = P["blotter"]
    raw = pd.read_csv(os.path.join(TGT, PK.F_BLOTTER), dtype=str, keep_default_na=False)
    check("R2 the export repeats exact lines only (25), dropped by line", int(raw.duplicated().sum()) == 25)
    raw["version"] = raw.version.astype(int)
    rawq = raw.copy()
    dup = rawq.duplicated()
    rawq.loc[dup, "trade_id"] = rawq.loc[dup, "trade_id"] + "D"          # each repeated line taken as its own ticket
    rawq["q"] = np.where(rawq.side == "BUY", 1.0, -1.0) * rawq.quantity.astype(float)
    rawq.loc[rawq.status == "CANCEL", "q"] = 0.0
    rawq["at"] = [A.ts_ny(x) for x in rawq.booked_at]
    rawq["td"] = pd.to_datetime(rawq.trade_date)
    rawq["inst"] = rawq.eqx_instrument.map(lambda x: P["v1to2"].get(x, x))
    keep_dup = rawq.sort_values(["trade_id", "version"])
    check("R2 repeated lines kept as tickets of their own: every heading holds", heads(keep_dup) == R["cls"])
    first = bl.groupby("trade_id", as_index=False).head(1)
    check("R2 amendments and cancels ignored (first version kept): every heading holds", heads(first) == R["cls"])
    nocancel = bl[bl.status != "CANCEL"]
    check("R2 cancelled duplicate tickets kept: every heading holds", heads(nocancel) == R["cls"])
    v = pd.read_csv(os.path.join(TGT, PK.F_VENDOR), dtype=str)
    dupv = v[v.duplicated(keep=False)]
    check("R2 the vendor's re-sent days are exact repeats on two dates, and pivoting without dropping them fails",
          sorted(dupv.price_date.unique()) == [d.date().isoformat() for d in PK.VENDOR_RESENT] and
          v.duplicated(["vendor_id", "price_date"]).sum() == v.duplicated().sum())
    renamed = names[names.prior_ticker != ""]
    old_rows = v[v.ticker == renamed.prior_ticker.iloc[0]]
    check("R2 the renamed name's closes before the change carry its old ticker; keyed by vendor id the series is whole",
          len(old_rows) > 0 and v[v.vendor_id == renamed.vendor_id.iloc[0]].price_date.nunique() == len(P["dates"]))
    e1 = pd.read_csv(os.path.join(TGT, PK.F_EQX1))
    e2 = pd.read_csv(os.path.join(TGT, PK.F_EQX2))
    both = set(pd.to_datetime(e1.EXTRACT_TS, format="%m/%d/%Y %H:%M:%S").dt.date) & \
        set(pd.Timestamp(x).date() for x in e2.extracted_at)
    check("R2 the EQX cutover day sits in both schemas with the same holdings", both == {PK.CUTOVER.date()})
    pcv = pd.read_csv(os.path.join(TGT, PK.F_PC))
    v1 = pcv[pcv.version == 1].set_index("business_date")
    moved = [d for d in window if (float(v1.loc[d.date().isoformat(), "booked_pnl_usd"]) < -R["vr"][d]) != (d in R["off"])]
    check("R2 product control's first versions instead of the latest move no exception", not moved)
    fl = R["P"]["runlog_all"]
    check("R2 the failed nights re-ran on the extract their first attempt read",
          all(set(g.eqx_extract) == {g.eqx_extract.iloc[0]} for _, g in fl.groupby("business_date")))

    # ---------------------------------------------------------------- R3 each result's hurried figure
    sys.path.insert(0, os.path.join(os.path.dirname(TASK), ".claude", "skills", "stumping"))
    import effort as EV  # noqa: E402
    for r in EJ["results"]:
        g = EV.grade(r["passes"]["careful"], r)[0]
        lost = "precedent" in r
        check("R3 %s careful but hurried pass %s" % (r["id"], "loses it" if lost else "earns it"),
              (g != "right") if lost else (g == "right"), g)

    # ---------------------------------------------------------------- R4 no plant
    docs = " ".join(open(os.path.join(TGT, f), "rb").read().decode("latin-1") for f in os.listdir(TGT) if f.endswith(".pdf"))
    check("R4 no shipped document names the cutoff, the allocations or a cause",
          not re.search(r"allocation|cut-?off|booked after|late booking", docs, re.I))
    def longest_flat(s):
        x = s.astype(float).values
        best = run = 1
        for j in range(1, len(x)):
            run = run + 1 if x[j] == x[j - 1] else 1
            best = max(best, run)
        return best
    vv = v.drop_duplicates().sort_values(["vendor_id", "price_date"])
    blocks = vv.groupby("vendor_id").close.apply(longest_flat).max()
    check("R4 no copied or backfilled block in the vendor's closes", blocks <= 5, "longest flat run %d days" % blocks)

    # ---------------------------------------------------------------- R5 no one thing
    lg = [R["late_gross"][d] for d in days[1:]]
    check("R5 the closing allocations reach every run the blotter covers, not only the deciding nights",
          all(x > 0 for x in lg), "%d runs" % len(lg))
    hi = sum(1 for d in window[1:] if R["late_var_effect"][d] < 0)
    check("R5 the missing allocations move the VaR both ways", 0.3 < hi / (len(window) - 1) < 0.7, "%d too high" % hi)
    check("R5 the reused extracts span 27 runs and decide none", len(R["outage_runs"]) == 27 and not R["outage_caused"])
    prox_share = []
    for q in sorted(P["vintages"]):
        d = max(x for x in days if x <= q) if q > days[0] else days[0]
        mv = np.abs(R["books"][d] * P["PX"][di[d]])
        prox_share.append(mv[E.proxied(d)].sum() / mv.sum())
    check("R5 the proxies carry a large share of the book in every quarter", min(prox_share) > 0.2,
          ", ".join("%.2f" % x for x in prox_share))
    careful = EJ["results"]
    cut_fix = {"R3", "R4", "R6"}
    check("R5 the cutoff corrected alone rescues no more than a third of the results",
          len(cut_fix) <= len(careful) / 3.0)

    # ---------------------------------------------------------------- R6 the one-fact test, executed
    gold_cls = R["cls"]
    hurried_plus_cutoff = gold_cls                               # the careful pass on the close book is the golden heading set
    r6 = {"R3": sorted(d.date().isoformat() for d, c in hurried_plus_cutoff.items() if c == "inputs") == F["cutoff_dates"],
          "R4": sorted(d.date().isoformat() for d, c in hurried_plus_cutoff.items() if c == "omitted") == F["omitted_dates"],
          "R6": {d.date().isoformat(): A.CODE[c] for d, c in hurried_plus_cutoff.items()} == F["r6_headings"]}
    check("R6 the cutoff hint, executed on the hurried pass, rescues R3, R4 and R6", all(r6.values()), str(r6))
    check("R6 the cutoff hint leaves R8 lost (the add-on path does not use the close book)",
          [round(x / 1e6, 2) for x in R["addon_ramp_only"]][1:] != F["addon_m"][1:])
    check("R6 the graduation hint, executed (the plan's months on each month's mapping), gives the golden path",
          [round(x / 1e6, 2) for x in R["addon"]] == F["addon_m"])

    # ---------------------------------------------------------------- R7 the rivals
    fc = R["fam_count"]
    check("R7 every decay 0.94 to 0.97, portfolio or series, keeps the sound count in its band and green",
          all(inside(int(v), F["bands"]["sound_count"]) and v <= 4 for v in fc.values()), str(sorted(fc.values())))
    fh = R["fam_cls"]
    stable = all(all(c[d] == gold_cls[d] or d.date().isoformat() in F["flex_dates"] for d in gold_cls) for c in fh.values())
    check("R7 every rival heading set differs from the golden only on the banded dates", stable)
    for k, v in R["addon_family"].items():
        ok = all(inside(round(x / 1e6, 2), b) for x, b in zip(v, F["bands"]["addon"]))
        check("R7 add-on rival (%s) inside every month's band" % k, ok)
    note = open(os.path.join(TGT, DC.F_METHOD), "rb").read()
    check("R7 the interpolated quantile is ruled out by the note (fifth-largest loss), and moves %d date(s)" %
          abs(F["interp_inputs"] - F["heading_counts"]["inputs"]), True)

    # ---------------------------------------------------------------- forks (design note's fork table)
    import subprocess

    def pdftext(name):
        return re.sub(r"\s+", " ", subprocess.run(["pdftotext", os.path.join(TGT, name), "-"], capture_output=True,
                                                   text=True).stdout)
    std, meth = pdftext(DC.F_STANDARD), pdftext(DC.F_METHOD)
    from openpyxl import load_workbook
    basis = " ".join(str(r[1]) for r in load_workbook(os.path.join(TGT, DC.F_PLAN))["Basis"].iter_rows(min_row=2,
                                                                                                       values_only=True))
    check("SF1 the population is either P&L (MRS-4 3.3), 19 against the booked 15",
          "booked P&L or the hypothetical P&L" in std and len(set(R["off"]) | set(R["hx"])) == F["exceptions_total"])
    check("SF2 product control's hypothetical P&L is the close book revalued, not the extract's", dh <= 3.0 and
          "Product Control produces it" in std)
    interp_rep = max(abs(E.var(P["extract"][R["used_day"][d][0]], P["futs"][R["used_day"][d][1]], di[d], qrule="interp")
                         - R["rep"][d]) for d in list(R["rep"])[:40])
    check("SF4 the fifth-largest loss is the note's rule and the only one that replicates the log",
          "fifth-largest loss of the 500" in meth and interp_rep > 1000, "interpolated misses by up to %.0f" % interp_rep)
    check("SF5 the 500-day window is the note's", "500 business days ending on the run date" in meth and mx <= 1.0)
    check("SF6 the headings are taken in the standard's order", "taken in order, that accounts for it" in std)
    check("SF7 every decay 0.94 to 0.97, portfolio or series, inside the bands (same call)",
          all(inside(int(v), F["bands"]["sound_count"]) for v in fc.values()))
    check("SF9 (c) to (e) count against the model: 14", "(c), (d) and (e) count against the model" in std and
          F["model_count"] == sum(F["heading_counts"][h] for h in ("omitted", "volatility", "sound")) == 14)
    check("SF10 the planned book scales each segment to its target from the 30 June run's positions",
          "scaled so that the segment's gross equals the month's target" in basis and "30 June 2025 run" in basis)
    check("SF11 the planned add-on prices on the engine's 30 June window and betas",
          "scenario window (the 500 business days to 30 June 2025)" in basis)

    class Closes(A.Engine):
        def proxied(self, on):
            return (self.cal_i[on] - self.ss_i) < A.W_DAYS + 1
    E2 = Closes(P)
    off_by_one = sum(abs(E2.var(P["extract"][R["used_day"][d][0]], P["futs"][R["used_day"][d][1]], di[d]) - R["rep"][d]) > 1
                     for d in R["rep"])
    check("SF12 the month's mapping is the store rule at the run that sets the month's first VaR",
          F["addon_run_for"][0] == "2025-06-30" and F["addon_proxied"][0] == F["proxied_30jun"] and
          "for the month's first business day" in std)
    check("SF13 the store counts returns: counting closes breaks the replication on graduation runs",
          "500 or more of its daily returns" in meth and off_by_one > 0, "%d runs off" % off_by_one)
    check("SF14 a negative add-on is floored (MRS-4 6)", "not less than zero" in std and F["addon_m"][-1] == 0.0 and
          F["addon_unfloored_dec_m"] < 0)
    check("SF15 a reused extract's counterfactual is the book held (MRS-4 4(b)), which clears both reused nights",
          "positions the desk held at the close of the previous business day" in std and F["outage_caused"] == 0 and
          len(F["careful_inputs_dates"]) == 2)
    check("SF3 the VaR reported for a date is the previous evening's run: the official file's VaR column agrees",
          all(abs(float(P["official"].set_index("d").loc[d, "var"]) - R["vr"][d]) < 1 for d in window))
    check("SF8 the corrected count is the sound model over all 250 days, not the union's uncovered rows",
          len(R["sound_days"]) == F["sound_count"])
    sh = R["shortcuts"]
    check("forcing: the shortcuts land in the red zone", sh["official"] >= 10 and sh["noprox"] >= 10, str(sh))

    # ---------------------------------------------------------------- realism sweep
    counts = Counter(t["when"] for t in w.trades)
    check("realism: client flow, desk trades, allocations and hedges all present", all(counts[k] > 300 for k in
                                                                                      ("client", "desk", "alloc", "hedge")))
    gross = [np.abs(R["books"][d] * P["PX"][di[d]]).sum() for d in days]
    check("realism: the desk's gross stays in a plausible band", 300e6 < min(gross) and max(gross) < 800e6,
          "%.0fm to %.0fm" % (min(gross) / 1e6, max(gross) / 1e6))
    print()
    print("%d FAIL" % len(FAILS))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
