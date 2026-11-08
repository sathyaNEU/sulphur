"""task3's assertions on the cut pack and the seeded world: the input gates, the call and its ladder with margins,
the record's hidden trend, the deep-step family and the stationary rungs on either side of Alternative A's capacity,
every semantic fork row (SF1 to SF12), the asks across the family, the analyst test on the clean truth, the
distractors and the realism sweeps.

    python3 checks.py [target_dir]            (run by build.py)"""
import csv
import os
import shutil
import sys
import tempfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as AN   # noqa: E402
import common as K      # noqa: E402
import freq as FQ       # noqa: E402
import world as W       # noqa: E402

FAILS = []
A_CAP, B_CAP, C_CAP = (c[2] for c in K.CULVERTS)
MARGIN = 1.15


def check(name, ok, detail=""):
    print("%s  %s%s" % ("PASS" if ok else "FAIL", name, (": " + detail) if detail else ""))
    if not ok:
        FAILS.append(name)


def pick(q):
    return next(a[0] for a in K.CULVERTS if a[2] >= q)


def main(target):
    files = sorted(os.listdir(target))
    check("ten or more files", len(files) >= 10, "%d" % len(files))
    check("two or more file categories", len({os.path.splitext(f)[1] for f in files}) >= 3,
          ", ".join(sorted({os.path.splitext(f)[1] for f in files})))
    nrain = sum(1 for _ in open(os.path.join(target, K.FILES["rain"]))) - 1
    npot = sum(1 for _ in open(os.path.join(target, K.FILES["pot"]))) - 1
    check("a CSV of 20,000 rows or more, used", nrain >= 20000, "rain gauge %d rows" % nrain)
    check("a CSV of 10 printed pages or more, used", npot >= 450, "peaks above base %d rows" % npot)
    check("two or more distractors", True, "daily discharge, inspection, cross sections, grab samples")
    names = [f.lower() for f in files]
    check("no readme, dictionary, notes or manifest under target/",
          not any(w in n for n in names for w in ("readme", "dictionary", "notes", "manifest", "codebook")))

    g = AN.Golden(target)
    R = g.run()
    rungs, fam = g.rivals()
    q_fam = {k: v[0] for k, v in fam.items()}
    print("      golden c %.3f on %d pairs; 1 per cent flow %.0f cfs (Alternative %s); recorded peaks %.0f cfs"
          % (R["c"], R["n_pairs"], R["q1"], R["pick"][0], R["raw_q1"]))
    check("the call: Alternative B", R["pick"][0] == "B")
    check("the record reads stationary: Kendall p over 0.3", R["mk_p"] > 0.3, "tau %.3f p %.3f" % (R["mk_tau"], R["mk_p"]))
    lo, hi = min(q_fam.values()), max(q_fam.values())
    rmax = max(list(rungs.values()) + [max(R["ann"])])
    check("every stationary rung and the record's largest flood clear Alternative A by 1.15", A_CAP / rmax >= MARGIN,
          "highest %.0f, ratio %.3f" % (rmax, A_CAP / rmax))
    check("every rung picks Alternative A", all(pick(v) == "A" for v in rungs.values()),
          ", ".join("%s %.0f" % (k, v) for k, v in rungs.items()))
    check("the deep-step family clears Alternative A by 1.15", lo / A_CAP >= MARGIN, "lowest %.0f, ratio %.3f" % (lo, lo / A_CAP))
    check("the deep-step family stays under Alternative B by 1.15", B_CAP / hi >= MARGIN, "highest %.0f, ratio %.3f" % (hi, B_CAP / hi))
    check("every member of the family picks Alternative B", all(pick(v) == "B" for v in q_fam.values()))

    # semantic forks: each alternative reading of a convention lands on the same call
    def call_with(**kw):
        return pick(variant(target, **kw))
    for sf, label, kw in (("SF1", "the new gauge's overlap readings used instead of the old gauge's", dict(new_overlap=True)),
                          ("SF2", "Monday accumulations left on Monday", dict(spread=False)),
                          ("SF3", "the duplicate 2009 and 2010 peaks counted twice", dict(dedupe_pot=False)),
                          ("SF4", "split parcels counted under both numbers", dict(dedupe_parcels=False)),
                          ("SF9", "the paved fraction carried to 2036 on its 2015 to 2025 trend", dict(to_2036=True)),
                          ("SF11", "each parcel's impervious area counted from the year after it was built", dict(lag_year=True))):
        q = variant(target, **kw)
        check("%s %s: same call" % (sf, label), pick(q) == "B", "%.0f cfs" % q)
    std = _docx_text(os.path.join(target, K.FILES["standard"]))
    for y0 in (1981, 1991, 2001):
        m = g.years >= y0
        q = FQ.lp3_quantile(R["adj"][m], K.DESIGN_AEP)
        check("SF13 only the storms since %d on today's watershed (%s): ruled out by 4.3's full length of the record"
              % (y0, pick(q)), "full length of the gauge's record" in std, "%.0f cfs" % q)
    windows = {k: v for k, v in q_fam.items() if k.startswith("G pairs")}
    check("SF5 a pairing window of two to four days: same call", all(pick(v) == "B" for v in windows.values()))
    check("SF6 storms of half an inch to three inches: same call", all(pick(v) == "B" for v in windows.values()))
    check("SF7 log-Pearson III or the generalized extreme value: same call",
          all(pick(v) == "B" for k, v in q_fam.items() if k.endswith("gev")))
    check("SF8 the annual peaks against their own storms, or decade effects: same call",
          all(pick(v) == "B" for k, v in q_fam.items() if "annual" in k or "decade" in k))
    check("SF10 the record's water years read as the standard's years: the peak file is by water year", True)
    check("SF12 the design flow rounded to the nearest hundred: same call", pick(round(R["q1"], -2)) == "B")

    # the asks across the family
    tops, largest = set(), set()
    for before in (1, 2, 3):
        for tmin in (0.5, 1.0, 1.5, 2.0, 3.0):
            c, _ = g.response(before, tmin)
            adj = g.adjusted(c)
            o = np.argsort(-adj)
            tops.add(tuple(int(g.years[i]) for i in o[:4]))
            largest.add(int(g.years[o[0]]))
    check("ask: the largest flood's water year is the same across the family", largest == {R["top5"][0]},
          str(sorted(largest)))
    check("ask: the four largest in order are the same across the family", tops == {tuple(R["top5"][:4])}, str(tops))
    check("ask: the recorded peaks name another largest year and another four",
          R["raw_top5"][0] != R["top5"][0] and R["raw_top5"][:4] != R["top5"][:4],
          "recorded %s against %s" % (R["raw_top5"][:4], R["top5"][:4]))
    adj_sorted = np.sort(R["adj"])[::-1]
    check("ask: the fourth and fifth largest on today's watershed sit 2 per cent or more apart",
          adj_sorted[3] / adj_sorted[4] >= 1.02, "%.3f" % (adj_sorted[3] / adj_sorted[4]))

    # the clean truth: the world's own storms through the 2025 watershed, and the analyst test
    w = W.World(K.SEED)
    ys = np.arange(K.YEAR0, K.YEAR1 + 1)
    ann = np.array([w.annual[y]["peak"] for y in ys])
    imp = W.imp_frac(ys)
    true_adj = ann * (W.time_to_peak_h(imp) / W.time_to_peak_h(imp[-1])) * \
        ((1 + K.VOL_RISE * (imp[-1] - K.IMP0)) / (1 + K.VOL_RISE * (imp - K.IMP0)))
    tq = FQ.lp3_quantile(true_adj, K.DESIGN_AEP)
    check("the world's own storms on the 2025 watershed pick Alternative B", pick(tq) == "B", "%.0f cfs" % tq)
    sq = FQ.lp3_quantile(ann, K.DESIGN_AEP)
    check("analyst test on the clean truth: the true peaks fitted as they stand pick Alternative A", pick(sq) == "A",
          "%.0f cfs" % sq)

    # distractors: delete each, the call and the asks unchanged
    for k in ("flow", "inspection", "survey", "quality"):
        tmp = tempfile.mkdtemp()
        try:
            for f in files:
                if f != K.FILES[k]:
                    shutil.copy(os.path.join(target, f), tmp)
            r2 = AN.Golden(tmp).run()
            check("distractor %s deleted: call and asks unchanged" % K.FILES[k],
                  r2["pick"][0] == R["pick"][0] and r2["top5"] == R["top5"] and abs(r2["q1"] - R["q1"]) < 1e-6)
        finally:
            shutil.rmtree(tmp)

    # realism
    dashes = [f for f in files if f.endswith((".csv", ".md")) and "—" in open(os.path.join(target, f), encoding="utf-8").read()]
    check("no em dash in a shipped text", not dashes, ", ".join(dashes))
    print()
    print("%s  %d failures" % ("PASS" if not FAILS else "FAIL", len(FAILS)))
    return 1 if FAILS else 0


def _docx_text(path):
    from docx import Document
    return " ".join(p.text for p in Document(path).paragraphs)


def variant(target, new_overlap=False, spread=True, dedupe_pot=True, dedupe_parcels=True, to_2036=False, lag_year=False):
    """The golden re-run under one alternative reading."""
    import datetime as dt
    g = AN.Golden(target)
    if new_overlap or not spread:
        rows = list(csv.DictReader(open(os.path.join(target, K.FILES["rain"]))))
        by = {}
        for r in rows:
            d = dt.date.fromisoformat(r["date"])
            pref = "TAM-RG-02" if (new_overlap and d >= dt.date(1987, 4, 15)) or d >= dt.date(1987, 6, 14) else "TAM-RG-01"
            if r["station_id"] == pref or d not in by:
                by[d] = r
        val = {}
        days = sorted(by)
        for i, d in enumerate(days):
            r = by[d]
            f = r["mflag"]
            if f.startswith("A") and len(f) > 1 and spread:
                k = int(f[1:])
                for j in range(k):
                    val[days[i - j]] = float(r["precip_in"]) / k
            elif f in ("A", "M"):
                val.setdefault(d, 0.0)
            else:
                val[d] = float(r["precip_in"]) if r["precip_in"] else 0.0
        g.rain = val
    if not dedupe_pot:
        g.pot = [(int(r["water_year"]), dt.date.fromisoformat(r["peak_date"]), float(r["peak_cfs"]))
                 for r in csv.DictReader(open(os.path.join(target, K.FILES["pot"])))]
    if not dedupe_parcels:
        g.frac = AN.paved_fraction(target, dedupe=False)
    if lag_year:
        g.frac = {y: g.frac.get(y - 1, 0.0) for y in g.frac}
    g.imp = np.array([g.frac[y] for y in g.years])
    c, _ = g.response()
    if to_2036:
        slope = (g.frac[2025] - g.frac[2015]) / 10
        adj = g.ann * np.exp(c * (g.frac[2025] + 11 * slope - g.imp))
    else:
        adj = g.adjusted(c)
    return FQ.lp3_quantile(adj, K.DESIGN_AEP)


if __name__ == "__main__":
    tgt = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "target")
    sys.exit(main(tgt))
