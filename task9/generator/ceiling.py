"""task9 ceiling (architecture 7): the pair a shallow run and a landed run would score, on Mark's measured split (call
and critical components 38, instruction-following 7, asks 55), computed from figures.json at the prompt's rounding
(chances and expected losses to one decimal, subordination in whole per cent rounded up): each note's five-year chance,
its portfolio's expected loss, the subordination for 1 and 0.5 per cent and the five year-end chances, eighteen figures.

The shallow run is the arch 6 route the platform's runs took: the house-year dependence, every file conformed, every
rule read, one average loss for every default (it buys Kestrel Lane). The deeper run finds that clustered defaults
recover less and carries the record's co-default table to the notes by counting co-defaults among each note's own loans
(it buys Ostvale). The default path (the industry copula) is scored
beside it. The landed run is the cracker: the house-linked recovery taken and the call landed, its second judgment
read another sound way (each house-year's shock inferred against the year's rates rather than the sector-year's).

    python3 ceiling.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def score(run, F, call_right, comps_right):
    G = F["golden"]
    items = []
    for k in ("KL", "OS"):
        items.append(run[k]["p5_pct"] == G[k]["p5_pct"])
        items += [a == g for a, g in zip(run[k]["need_pct"], G[k]["need_pct"])]
        items += [a == g for a, g in zip(run[k]["by_year_pct"], G[k]["by_year_pct"])]
        items.append(run[k]["el_pct"] == G[k]["el_pct"])
    ask_keep = sum(items) / len(items)
    return 14.0 * call_right + 24.0 * comps_right + 7.0 + 55.0 * ask_keep, ask_keep, len(items)


def main():
    F = json.load(open(os.path.join(HERE, "figures.json")))
    R = F["rungs"]
    # critical components: the house clustering, the recovery gap, the link, the counts and chances
    shallow, s_keep, n = score(R["house_pooled_lgd"], F, call_right=0, comps_right=1 / 4)
    default, d_keep, _ = score(F["default_path"], F, call_right=0, comps_right=0.0)
    landed, l_keep, _ = score(R["house_link_given_year"], F, call_right=1, comps_right=2 / 4)
    deeper, x_keep, _ = score(R["count_in_portfolio"], F, call_right=0, comps_right=2 / 4)
    print("ask figures scored: %d" % n)
    print("shallow run (arch 6 route, one average loss): %.1f (keeps %.1f per cent of ask weight)" % (shallow, 100 * s_keep))
    print("deeper run (the co-defaults counted among each note's own loans, buys Ostvale): %.1f (keeps %.1f per cent)"
          % (deeper, 100 * x_keep))
    print("default path (industry copula): %.1f (keeps %.1f per cent)" % (default, 100 * d_keep))
    print("landed run (cracker, house shocks against the year's rates): %.1f (keeps %.1f per cent)" % (landed, 100 * l_keep))
    print("pair ceiling, landed and shallow: %.1f; landed and deeper: %.1f" % ((landed + shallow) / 2, (landed + deeper) / 2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
