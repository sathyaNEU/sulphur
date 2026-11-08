"""task3: the pair ceiling on the cut pack (supplemental-stumping Part 5).

Rows: the landed runs (the storm-by-storm snow-line carry taken, every mess item cleaned, every filed rule read, one
second judgment at its reflex: the standard atmosphere's lapse rate, the freezing level as the rain-snow line, rain
counted without its rise with elevation, all three, or the valley's daily temperatures in place of the hourly record)
and the shallow run (Bulletin 17C at the Coyner River carried by drainage area). Seven ask cells score on every row:
the 50 and 1 per cent flows in their 5,000 cfs cells, the three spans' exceedance bands, the two largest floods and the
annual-peaks file's year without a flood fed by rain. Priced on 38 (the call and critical components), 7
(instruction-following) and 55 (the asks), with 5 of partial credit for a run off the call. The cracker is the
landed run with every second judgment at its reflex (the standard atmosphere's lapse rate, the freezing level, rain
without its rise with elevation); the best landed row and the full includer are reported beside it.

    python3 task3/generator/ceiling.py [target_dir]
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as A  # noqa: E402
import docs as DC  # noqa: E402
import figures as FG  # noqa: E402
import freq as F  # noqa: E402

LANDED = ("lapse_6.5", "freezing_0C", "no_orography", "textbook", "lapse_6.5_0C", "daily_storm_mean", "daily_wettest_day")


def cells(par, series, missing_marked):
    q50, q01 = F.quantile(par, 0.5), F.quantile(par, 0.01)
    out = dict(q50=FG.k5000(q50), q01=FG.k5000(q01))
    for sp, rq in DC.SPANS:
        out["band_%d" % sp] = FG.band(F.aep_of(par, rq))
    out["top2"] = frozenset(FG.top_years(series))
    out["csv_year_marked"] = missing_marked
    out["span"] = FG.spans_of(q01)
    return out


def score(c, gold):
    keys = [k for k in gold if k != "span"]
    kept = [c[k] == gold[k] for k in keys]
    frac = sum(kept) / float(len(kept))
    return (38 if c["span"] == gold["span"] else 5) + 7 + 55 * frac, dict(zip(keys, kept))


def main(tgt):
    R = A.run(tgt)
    gold = cells(R["par"], R["series"], True)
    rows = {}
    for name in LANDED:
        v = R["variants"][name]
        missing = [y for y in range(1951, 2026) if y not in v["series"]]
        rows[name] = score(cells(v["par"], v["series"], bool(missing)), gold)
    rpar_c = dict(R["river_par"])
    rpar_c["mean"] += A.STATE_B * __import__("numpy").log10(R["area_c"] / R["area_r"])
    river = {y: R["annual"][y][1] for y in R["annual"]}
    shallow = score(cells(rpar_c, river, False), gold)
    best = max(rows, key=lambda k: rows[k][0])
    C, S = rows["textbook"][0], shallow[0]
    full = 100.0
    out = dict(cracker=round(C, 1), cracker_row="textbook", best_landed_row=best, best_landed=round(rows[best][0], 1),
               shallow=round(S, 1), pair=round((C + S) / 2, 1),
               shallow_keep_pct=round(100 * sum(shallow[1].values()) / float(len(shallow[1])), 1),
               full_includer_pair=round((full + S) / 2, 1),
               landed={k: (round(v[0], 1), [kk for kk, ok in v[1].items() if ok]) for k, v in rows.items()},
               shallow_kept=[kk for kk, ok in shallow[1].items() if ok])
    print(json.dumps(out, indent=1))
    return out


if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
    A.STATE_B = round(json.load(open(os.path.join(HERE, "figures.json")))["equations"]["100"]["b"], 3)
    main(t)
