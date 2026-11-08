"""task3 architecture 3: the pair ceiling and the shallow keep, from generator/rungs.json (the rungs run on the cut
pack). Scoring on supplemental-stumping Part 0: the call and its components 38, the instructions 7, the asks 55
shared equally over the graded ask figures (A1's four peaks, A2's Mill Street drawdown, A3's domestic well).

    cracker   lands the call by the deep step but takes the shallow form of each ask's second judgment: the walls
              left out (the record fits without them), the far wells anchored to 2005 to 2008 for MS-MW
    mirror    the default path (the leaky aquifer calibrated against CV-07)
    full      the golden route with every second judgment

    python3 ceiling.py [rungs.json]"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
W_CALL, W_IF, W_ASK, R_OFF = 38.0, 7.0, 55.0, 5.0


def ft(x):
    return int(math.floor(x + 0.5))


def cells(r, msmw=None, dw=None):
    return [ft(r["peaks"][k]) for k in ("450", "700", "1000", "1250")] + [ft(msmw if msmw is not None else r["msmw_2025"]),
                                                                          ft(dw if dw is not None else (r["dw"] or 0))]


def score(path_cells, gold_cells, on_call):
    keep = sum(a == b for a, b in zip(path_cells, gold_cells)) / len(gold_cells)
    return (W_CALL if on_call else R_OFF) + W_IF + W_ASK * keep, keep


def main(rp):
    R = json.load(open(rp))
    g = R["golden"]
    gold = cells(g)
    crack = cells(R["walls_none"], msmw=R["msmw_anchor_slip"])
    mirror = cells(R["rung1_cv07"])
    full_s, _ = score(gold, gold, True)
    c_s, c_keep = score(crack, gold, R["walls_none"]["call"] == g["call"])
    m_s, m_keep = score(mirror, gold, R["rung1_cv07"]["call"] == g["call"])
    print("gold cells    %s" % gold)
    print("cracker cells %s  score %.1f (keep %.2f)" % (crack, c_s, c_keep))
    print("mirror cells  %s  score %.1f (keep %.2f)" % (mirror, m_s, m_keep))
    print("pair ceiling (cracker with mirror) %.1f; full includer with mirror %.1f" % ((c_s + m_s) / 2, (full_s + m_s) / 2))
    print("shallow keep %.1f per cent of ask weight" % (100 * m_keep))
    json.dump({"pair_ceiling": round((c_s + m_s) / 2, 1), "full_with_mirror": round((full_s + m_s) / 2, 1),
               "shallow_keep": round(100 * m_keep, 1)}, open(os.path.join(HERE, "ceiling.json"), "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "rungs.json"))
