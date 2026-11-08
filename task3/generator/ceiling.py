"""task3 architecture 4: the pair ceiling and the shallow keep, from generator/rungs.json (the rungs run on the cut
pack). Scoring on supplemental-stumping Part 0: the call and its components 38, the instructions 7, the asks 55
shared equally over the graded ask figures (the first year at 10, the 2034 entry point, the highest well, its 2034
mean, each to the asked rounding).

    cracker   lands the call by the deep step (each parcel's delay through its own unsaturated sand) but takes the
              shallow form of the asks' second judgment: each parcel's water mixed at the recharge that carried it
              from the root zone, the model carried to the wells' level (it reads the ridge's early dilution as bias)
    cracker2  the same with acres alone as the mixing weight (its 2034 entry point sits on the rounding edge and is
              counted kept)
    mirror    the default path: one lag fitted to the wells' record, the clearing's effect fitted to 2019-2026 (nil)
    full      the golden route with every second judgment

    python3 ceiling.py [rungs.json]"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
W_CALL, W_IF, W_ASK, R_OFF = 38.0, 7.0, 55.0, 5.0


def mg(x):
    return int(math.floor(x + 0.5))


def cells(r):
    return [r["cross"], mg(float(r["ep"]["2034"])), r["hi_well"], mg(r["hi_2034"])]


def score(path_cells, gold_cells, on_call, kept_extra=0):
    keep = (sum(a == b for a, b in zip(path_cells, gold_cells)) + kept_extra) / len(gold_cells)
    return (W_CALL if on_call else R_OFF) + W_IF + W_ASK * keep, keep


def main(rp):
    R = json.load(open(rp))
    g = R["golden"]
    gold = cells(g)
    crack = cells(R["leachtime_anchored"])
    crack2 = cells(R["area_weights"])
    edge = 1 if crack2[1] != gold[1] else 0
    mirror = cells(R["rung1_single_lag"])
    full_s, _ = score(gold, gold, True)
    c_s, c_keep = score(crack, gold, R["leachtime_anchored"]["call"] == g["call"])
    c2_s, c2_keep = score(crack2, gold, R["area_weights"]["call"] == g["call"], edge)
    m_s, m_keep = score(mirror, gold, R["rung1_single_lag"]["call"] == g["call"])
    print("gold cells     %s" % gold)
    print("cracker cells  %s  score %.1f (keep %.2f)" % (crack, c_s, c_keep))
    print("cracker2 cells %s  score %.1f (keep %.2f, the 2034 entry point counted kept)" % (crack2, c2_s, c2_keep))
    print("mirror cells   %s  score %.1f (keep %.2f)" % (mirror, m_s, m_keep))
    print("pair ceiling (cracker with mirror) %.1f; cracker2 with mirror %.1f; full includer with mirror %.1f" %
          ((c_s + m_s) / 2, (c2_s + m_s) / 2, (full_s + m_s) / 2))
    print("shallow keep %.1f per cent of ask weight" % (100 * m_keep))
    json.dump({"pair_ceiling": round((c_s + m_s) / 2, 1), "pair_ceiling_area": round((c2_s + m_s) / 2, 1),
               "full_with_mirror": round((full_s + m_s) / 2, 1), "shallow_keep": round(100 * m_keep, 1)},
              open(os.path.join(HERE, "ceiling.json"), "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "rungs.json"))
