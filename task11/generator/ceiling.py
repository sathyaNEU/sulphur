"""The pair estimate on the cut pack, for the re-sited asks (supplemental-stumping Part 0 and 5).

The ask figures are the deep step's own output across the answer's shape: every sub-watershed's days above the
trigger by month of the season (5 rows of 7 months) and the carbon fed in each month from May to August that the
plant would not have fed without each sub-watershed's atrazine (5 rows of 4 months). A row is kept only when every
cell in it is exact, which is how the generated rubric grades a row. The chart carries no ask figure: the platform's
round-1 rubric graded it in one-point rows beside the file checks, so it sits in the 7 for instruction-following.

Routes, each with every mess item cleaned and every filed rule read:
  landed      the deep step taken on all 47 days and the SOP replayed on the results without each sub-watershed
  tagged      landed, but each day's carbon booked to the sub-watershed behind that day (the run-on left out)
  pulse       landed on 45 days, 29 and 30 May left unattributed (platform run 1's route)
  shallow     the default path: the 30-day load share with the lake treated as one mixed volume
  withheld    no count filed for any sub-watershed (platform run 2's route)

Recommendation side: 38 for the call and the critical components when all 47 days land (25.3 for the pulse route,
which loses the 47, on the round-1 rubric's 18, 12 and 6; 5 off the call); 7 for instruction-following; 55 for the
asks, weighted by figures. The cracker is the pulse route, the landed route the platform measured (run 1); the full
landing is printed beside it as the layer's exposure.

    python3 ceiling.py [target]"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import asks as A            # noqa: E402
import golden as G          # noqa: E402

CHART = 0


def rows_kept(cells, gold):
    kept, total = 0, 0
    for kind, months in (("days", A.SEASON_MONTHS), ("lb", A.PAC_MONTHS)):
        for k in G.SUBS:
            w = len(months)
            total += w
            if cells is not None and all(cells.get((kind, k, m)) == gold[(kind, k, m)] for m in months):
                kept += w
    return kept, total


def main(target):
    R = G.compute(target)
    gold = A.ask_cells(R)
    routes = {"landed": dict(gold)}
    tag = A.day_tagged_carbon(target, R)
    routes["tagged"] = {**gold, **{("lb", "FEN", m): int(round(tag[m])) for m in A.PAC_MONTHS}}
    pulse = A.unresolved_pulse(target, R)
    pc = dict(gold)
    for n, m in enumerate(A.SEASON_MONTHS):
        pc[("days", "FEN", m)] = list(pulse["days"].values())[n]
    for m in A.PAC_MONTHS:
        pc[("lb", "FEN", m)] = int(round(pulse["carbon"][m]))
    routes["pulse"] = pc
    routes["shallow"] = A.shallow_routes(target, R)["load share, 30 days"]
    routes["withheld"] = None
    rec = dict(landed=38.0, tagged=38.0, pulse=38.0 * 24 / 36, shallow=5.0, withheld=5.0)
    score = {}
    for name, cells in routes.items():
        kept, total = rows_kept(cells, gold)
        L = (kept + CHART) / (total + CHART)
        score[name] = rec[name] + 7 + 55 * L
        print("%-8s keeps %2d of %d ask figures in whole rows (+%d chart): ask share %.1f per cent, score %.1f"
              % (name, kept, total, CHART, 100 * L, score[name]))
    print("Pair, landed with shallow: %.1f" % ((score["landed"] + score["shallow"]) / 2))
    print("Pair, landed with withheld (the platform's round-1 shape at its best for the landed run): %.1f"
          % ((score["landed"] + score["withheld"]) / 2))
    print("Pair, pulse with withheld (the platform's round-1 runs on the new asks): %.1f"
          % ((score["pulse"] + score["withheld"]) / 2))
    print("Pair, tagged with shallow: %.1f" % ((score["tagged"] + score["shallow"]) / 2))
    print("Pair ceiling: %.1f (cracker, the pulse route, with the shallow route)" % ((score["pulse"] + score["shallow"]) / 2))
    print("Pair, both landed: %.1f (the ladder's exposure; no ask layer reaches it)" % score["landed"])
    print("Shallow keep: %.1f per cent of ask weight"
          % (100 * (rows_kept(routes["shallow"], gold)[0] + CHART) / (rows_kept(None, gold)[1] + CHART)))
    return 0


if __name__ == "__main__":
    tgt = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
    sys.exit(main(tgt))
