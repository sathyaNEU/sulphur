"""task7 ceiling: each route a solver could take, scored on the rubric model (supplemental-stumping Part 0) on the cut
pack, and the pair the platform's two runs would average.

The model: the recommendation 20 and the four critical components 4.5 each (38 together), instruction-following 7
(files present, named, rows and columns: every route that delivers keeps it), the asks 55: each book's figure 11, the
facilities expected to cost most 18 (shared equally among the names), the CSV 15 (its rows and columns 5, which every
route keeps; its total and its first row 10, which only a route on the golden's construction keeps).

The components (submission.md): C1 the record's ratio by years since inspection for each lending book (a route that
fits the ratio by book keeps it), C2 the book's staleness against the record's (a route that rebuilt the years since
inspection keeps it), C3 the plan figure against the carried-value figure (a route on the call keeps it), C4 the
owner-occupied gap and the split (a route that splits the books keeps it)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import checks as CK  # noqa: E402
import golden as GD  # noqa: E402

UT, UB = 500000.0, 250000.0
W_REC, W_COMP, W_IF = 20.0, 4.5, 7.0
W_BOOK, W_NAMES, W_CSV_FIXED, W_CSV_ROUTE = 11.0, 18.0, 5.0, 10.0

# what each route computes: (fits the ratio by book, rebuilt the years since inspection)
ROUTES = [
    ("golden (split by book)", "golden", True, True),
    ("landed run, books pooled", "pooled", False, True),
    ("landed run, linear fit pooled", "pooled_lin", False, True),
    ("default path (carried values)", "carried", False, False),
    ("reflex haircut on old valuations", "reflex_10_over_3y", False, False),
    ("the record's average shortfall", "record_mean", False, False),
    ("cycle re-inspections only", "cycle_drift", False, True),
]


def rnd(v, u):
    return round(v / u) * u


def score(r, g, by_book, staleness):
    on_call = rnd(r["total"], UT) == rnd(g["total"], UT)
    main = W_REC * on_call
    main += W_COMP * (by_book and staleness)          # C1
    main += W_COMP * staleness                         # C2
    main += W_COMP * on_call                           # C3
    main += W_COMP * (by_book and on_call)             # C4
    asks = W_BOOK * (rnd(r["investment"], UB) == rnd(g["investment"], UB))
    asks += W_BOOK * (rnd(r["owner_occupied"], UB) == rnd(g["owner_occupied"], UB))
    asks += W_NAMES * len(set(r["top5"]) & set(g["top5"])) / len(g["top5"])
    asks += W_CSV_FIXED
    asks += W_CSV_ROUTE * (on_call and r["top5"][0] == g["top5"][0])
    return main + W_IF + asks, asks / 55.0, on_call


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "target")
    C = CK.run(target, HERE)
    res = C["res"]
    g = res["golden"]
    out = {}
    for label, k, by_book, stale in ROUTES:
        s, keep, on = score(res[k], g, by_book, stale)
        out[k] = (s, keep, on)
        print("%-34s score %5.1f  asks kept %5.1f%%  %s" % (label, s, 100 * keep, "on the call" if on else "off the call"))
    best_recent = max((k for k in res if k.startswith("recent ")), key=lambda k: score(res[k], g, False, False)[0])
    s, keep, on = score(res[best_recent], g, False, False)
    out["recent"] = (s, keep, on)
    print("%-34s score %5.1f  asks kept %5.1f%%  %s  (%s)" % ("recent experience, best window", s, 100 * keep,
                                                            "on the call" if on else "off the call", best_recent))
    landed = out["pooled"][0]
    shallow = out["carried"]
    print("Shallow keep: %.1f per cent of ask weight (default path)" % (100 * shallow[1]))
    print("Pair ceiling: %.1f (landed run with books pooled %.1f, default path %.1f)" % ((landed + shallow[0]) / 2, landed, shallow[0]))
    worst = max(out[k][0] for k in ("cycle_drift", "record_mean", "reflex_10_over_3y", "carried", "recent"))
    print("Pair with the strongest off-call route: %.1f" % ((landed + worst) / 2))
    print("Pair if the landed run also splits the books: %.1f" % ((out["golden"][0] + shallow[0]) / 2))


if __name__ == "__main__":
    main()
