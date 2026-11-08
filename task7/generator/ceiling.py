"""task7 ceiling: each route a solver could take, scored on the rubric model (supplemental-stumping Part 0) on the cut
pack, and the pair the platform's two runs would average.

The model: the recommendation 20 and four critical components 4.5 each (38 together), instruction-following 7 (files
present and named, sheets and columns: every route that delivers keeps it), and the asks 55, split evenly over the
seven supplementary answers the rubric is generated from, each answer's share kept in proportion to the gradable
figures in it that the route gets right at the asked rounding:

  1 the deck opens on the call and the funded round once the offer closes (the call, the round's grant, its tonnes);
  2 each measure's saving rate (three);
  3 each measure's grant per tonne charted against the limit (three values and the chart's bars and limit line);
  4 the pilot's 2025/26 saving (one);
  5 the measures sheet (per measure: rate, applications, grant, lifetime tonnes, grant per tonne, fund: eighteen, of which
    the applications and grants are read off the applications file by every route);
  6 the funded applications sheet (the row set, their grants, expected savings, lifetime tonnes and total grant: kept
    only by a route whose funded set is the golden's, the figures only on the golden's rates);
  7 the funded round once the offer closes (its grant and its tonnes).

The components: C1 the visits to the passed-over owners and C2 the narrowing against the flat gap (kept by a route that
found the visits), C3 the saving rates and C4 the grants per tonne (each kept by a route whose figures round as the
golden's)."""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import checks as CK  # noqa: E402
import golden as GD  # noqa: E402

W_REC, W_COMP, W_IF, W_ASKS = 20.0, 4.5, 7.0, 55.0
MEAS = GD.MEASURES


def rnd(v, u):
    return math.floor(v / u + 0.5) * u


def route(C, rates, found_visits, close="by measure", saving=None):
    """the figures a route files: its whole-per-cent rates, its funded set and appraisal, the round at close by its
    projection, and its 2025/26 saving"""
    P = C["P"]
    w = GD.whole(rates)
    f, A = CK.funded(P, w)
    ac = GD.at_close(P, w, f, close)
    ss = saving if saving is not None else GD.season_saving(P, w, GD.PIPELINE, "grossed up")
    return {"w": w, "f": f, "A": A, "ac": ac, "ss": ss, "found": found_visits}


def score(C, gold, r):
    same_set = r["f"] == gold["f"]
    ok_rate = {m: r["w"][m] == gold["w"][m] for m in MEAS}
    ok_eur = {m: r["A"][m]["tonnes"] > 0 and rnd(r["A"][m]["eur_t"], 10) == rnd(gold["A"][m]["eur_t"], 10) for m in MEAS}
    ok_ton = {m: rnd(r["A"][m]["tonnes"], 10) == rnd(gold["A"][m]["tonnes"], 10) for m in MEAS}
    ok_fund = {m: (m in r["f"]) == (m in gold["f"]) for m in MEAS}
    ok_g = rnd(r["ac"]["grant"], 1e6) == rnd(gold["ac"]["grant"], 1e6)
    ok_t = rnd(r["ac"]["tonnes"], 10000) == rnd(gold["ac"]["tonnes"], 10000)
    sq = []
    sq.append((same_set + ok_g + ok_t) / 3.0)
    sq.append(sum(ok_rate.values()) / 3.0)
    sq.append((sum(ok_eur.values()) + 1) / 4.0)
    sq.append(1.0 if rnd(r["ss"], 500) == rnd(gold["ss"], 500) else 0.0)
    sq.append(sum(ok_rate[m] + 1 + 1 + ok_ton[m] + ok_eur[m] + ok_fund[m] for m in MEAS) / 18.0)
    sq.append((same_set * (3 + all(ok_rate.values()) * 2)) / 5.0)
    sq.append((ok_g + ok_t) / 2.0)
    asks = W_ASKS * sum(sq) / len(sq)
    main = W_REC * same_set + W_COMP * (2 * r["found"] + all(ok_rate.values()) + all(ok_eur.values()))
    return main + W_IF + asks, asks / W_ASKS, same_set, sq


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "target")
    C = CK.run(target, HERE, quick=True)
    R = C["routes"]
    P = C["P"]
    gold = route(C, C["rates"], True)
    static = C["season_saving_rivals"]["the rate on the 2019 use, buildings still connected"]
    lot = R["R1 lottery, every passed-over building, notice season base"]
    routes = [
        ("golden", gold),
        ("landed run: the received applications summed, the rate on the 2019 use",
         route(C, C["rates"], True, "received", static)),
        ("landed run: one pooled share for the round, the rate on the 2019 use",
         route(C, C["rates"], True, "pooled over the funded measures", static)),
        ("landed run: the round right, the rate on the 2019 use", route(C, C["rates"], True, "by measure", static)),
        ("landed run: the 2025/26 saving right, the received applications summed", route(C, C["rates"], True, "received")),
        ("default path (the lottery, every passed-over owner)", route(C, lot, False)),
        ("the before and after", route(C, R["R0 before and after"], False)),
        ("decay read from the last two seasons", route(C, R["R1d lottery, every passed-over building, last two seasons"], False)),
        ("crisis seasons dropped", route(C, R["R1e lottery, every passed-over building, seasons to 2022"], False)),
        ("the first season alone", route(C, R["R1c lottery, every passed-over building, first season only"], False)),
        ("the lottery as drawn", route(C, R["R1a lottery, every passed-over building, as drawn"], False)),
    ]
    out = {}
    for label, r in routes:
        s, keep, on, sq = score(C, gold, r)
        out[label] = (s, keep, on)
        print("%-74s score %5.1f  asks kept %5.1f%%  %s  %s" % (label, s, 100 * keep, "on the call" if on else "off the call",
                                                               " ".join("%.2f" % x for x in sq)))
    landed = out["landed run: the received applications summed, the rate on the 2019 use"][0]
    shallow = out["default path (the lottery, every passed-over owner)"]
    print("Shallow keep: %.1f per cent of ask weight (default path)" % (100 * shallow[1]))
    print("Pair ceiling: %.1f (landed run %.1f, default path %.1f)" % ((landed + shallow[0]) / 2, landed, shallow[0]))
    worst = max(v[0] for k, v in out.items() if not v[2])
    print("Pair with the strongest off-call route: %.1f" % ((landed + worst) / 2))
    print("Pair if the landed run takes one of the two second judgments: %.1f" % (
        (max(out["landed run: the round right, the rate on the 2019 use"][0],
             out["landed run: the 2025/26 saving right, the received applications summed"][0]) + shallow[0]) / 2))
    print("Pair if the landed run also gets both: %.1f" % ((out["golden"][0] + shallow[0]) / 2))


if __name__ == "__main__":
    main()
