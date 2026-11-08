"""task3's paper ceiling on the cut pack. The asks: the design flow (scored inside the family's band), the largest
flood's water year and the four largest in order in the table the estimate rests on, the table's peaks (scored on
the four largest years' rows inside the family's band). The landed run takes the deep step; the shallow run fits the
recorded peaks; the rungs beside it.

    python3 ceiling.py [pack_dir]
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as AN   # noqa: E402
import common as K      # noqa: E402
import freq as FQ       # noqa: E402


def score(series, q1, gold, band, rows_band):
    years = gold["years"]
    o = [int(years[i]) for i in np.argsort(-series)]
    k = {"design flow": int(band[0] <= q1 <= band[1]),
         "largest year": int(o[0] == gold["top5"][0]),
         "four largest": int(o[:4] == gold["top5"][:4])}
    rows = 0
    for y in gold["top5"][:4]:
        i = list(years).index(y)
        rows += int(rows_band[y][0] <= series[i] <= rows_band[y][1])
    k["table rows"] = rows / 4.0
    return k


def measure(t):
    g = AN.Golden(t)
    R = g.run()
    rungs, fam = g.rivals()
    qs = [v[0] for v in fam.values()]
    band = (min(qs), max(qs))
    rows_band = {}
    for y in R["top5"][:4]:
        i = list(R["years"]).index(y)
        vals = [g.adjusted(v[1])[i] for v in fam.values() if v[1] == v[1]]
        rows_band[y] = (min(vals), max(vals))
    out = {"landed": score(R["adj"], R["q1"], R, band, rows_band),
           "shallow (recorded peaks)": score(R["ann"], R["raw_q1"], R, band, rows_band)}
    b = np.polyfit(R["imp"], np.log(R["ann"]), 1)
    s2 = R["ann"] * np.exp(b[0] * (R["imp"][-1] - R["imp"]))
    out["rung 2 (peaks regressed on paved fraction)"] = score(s2, FQ.lp3_quantile(s2, 0.01), R, band, rows_band)
    return out


def main(argv):
    t = argv[1] if len(argv) > 1 else os.path.join(HERE, "..", "target")
    out = measure(t)
    print("| Path (cracker = lands the call, runs the battery, executes filed documents) | Design flow | Largest year | Four largest | Table rows | Verdict |")
    print("|---|---|---|---|---|---|")
    keep = {}
    for k, v in out.items():
        kept = sum(v.values()) / 4.0
        keep[k] = kept
        print("| %s | %d | %d | %d | %.2f | %s |" % (k, v["design flow"], v["largest year"], v["four largest"],
                                                   v["table rows"], "keeps" if kept == 1 else "miss"))
    lc, ls = keep["landed"], keep["shallow (recorded peaks)"]
    on, off = 38 + 7 + 55 * lc, 5 + 7 + 55 * ls
    print()
    print("Shallow keep: %.1f per cent of ask weight." % (100 * ls))
    print("Pair ceiling: %.1f (landed %.1f, shallow %.1f)." % ((on + off) / 2, on, off))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
