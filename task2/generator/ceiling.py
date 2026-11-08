"""task2 architecture 4: the pair ceiling and the shallow keep, from generator/rungs.json (the rungs run on the cut
pack). Scoring on supplemental-stumping Part 0: the call and its components 38, the instructions 7, the asks 55 on
the graded ask figure (the gold above the agreement's cut-off, nearest 50,000 oz).

    cracker   lands the tier by the support correction but carries the declustered distribution to a block variance
              taken from the composites as drilled (the clustered variance), so its gold rounds elsewhere
    mirror    the default path (the declustered composites)
    full      the golden route

    python3 ceiling.py [rungs.json]"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
W_CALL, W_IF, W_ASK, R_OFF = 38.0, 7.0, 55.0, 5.0


def r50(oz):
    return int(50000 * math.floor(oz / 50000 + 0.5))


def score(r, g):
    on = r["tier"] == g["tier"]
    keep = 1.0 if r50(r["oz"]) == r50(g["oz"]) else 0.0
    return (W_CALL if on else R_OFF) + W_IF + W_ASK * keep, keep


def main(rp):
    R = json.load(open(rp))
    g = R["golden"]
    c_s, c_k = score(R["cracker_raw_variance"], g)
    m_s, m_k = score(R["rung1_declustered"], g)
    k_s, k_k = score(R["kriged"], g)
    f_s, _ = score(g, g)
    print("cracker (raw variance) %s koz tier %s: %.1f" % (round(R["cracker_raw_variance"]["oz"] / 1e3), R["cracker_raw_variance"]["tier"], c_s))
    print("mirror (declustered) %s koz tier %s: %.1f" % (round(R["rung1_declustered"]["oz"] / 1e3), R["rung1_declustered"]["tier"], m_s))
    print("kriged %s koz tier %s: %.1f" % (round(R["kriged"]["oz"] / 1e3), R["kriged"]["tier"], k_s))
    print("pair ceiling (cracker with mirror) %.1f; full includer with mirror %.1f" % ((c_s + m_s) / 2, (f_s + m_s) / 2))
    print("shallow keep %.1f per cent" % (100 * m_k))
    json.dump({"pair_ceiling": round((c_s + m_s) / 2, 1), "full_with_mirror": round((f_s + m_s) / 2, 1),
               "shallow_keep": round(100 * m_k, 1)}, open(os.path.join(HERE, "ceiling.json"), "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "rungs.json"))
