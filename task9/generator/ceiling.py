"""task9 ceiling: the pair a shallow run and a landed run would score, on Mark's measured split (call and critical
components 38, instruction-following 7, asks 55), computed from figures.json.

The shallow run is the default path (the industry copula, every file conformed, every rule read). The landed run is
the cracker: the house-year dependence taken, every file conformed, every rule read, its second judgments at their
reflex (the loss given default averaged over every closed workout). A chance is kept within 0.02 points or a tenth
of the golden, a subordination within 0.2 points; the chart is kept when its ordering in the tail is the golden's.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def kept_chance(a, g):
    return abs(a - g) <= max(0.02, 0.10 * g)


def kept_sub(a, g):
    return abs(a - g) <= 0.2


def score(run, F, call_right, comps_right):
    G = F["golden"]
    items = []
    for k in ("KL", "OS"):
        items.append(kept_chance(run[k]["p5_pct"], G[k]["p5_pct"]))
        items += [kept_sub(a, g) for a, g in zip(run[k]["need_pct"], G[k]["need_pct"])]
        items += [kept_chance(a, g) for a, g in zip(run[k]["by_year_pct"], G[k]["by_year_pct"])]
    tail_order_right = (run["KL"]["p5_pct"] > run["OS"]["p5_pct"]) == (G["KL"]["p5_pct"] > G["OS"]["p5_pct"])
    items.append(tail_order_right)
    ask_keep = sum(items) / len(items)
    call_part = 14.0 * call_right + 24.0 * comps_right
    return call_part + 7.0 + 55.0 * ask_keep, ask_keep


def main():
    F = json.load(open(os.path.join(HERE, "figures.json")))
    D, Lc = F["default_path"], F["rungs"]["closed_lgd"]
    # critical components: the pair evidence, the house component, the house counts, the loss given default, the chances
    shallow, s_keep = score(D, F, call_right=0, comps_right=0.0)
    landed, l_keep = score(Lc, F, call_right=1, comps_right=3 / 5)
    full, f_keep = score(F["golden"], F, call_right=1, comps_right=1.0)
    print("shallow run: %.1f (keeps %.1f per cent of ask weight)" % (shallow, 100 * s_keep))
    print("landed run (cracker): %.1f (keeps %.1f per cent of ask weight)" % (landed, 100 * l_keep))
    print("pair ceiling, landed and shallow: %.1f" % ((landed + shallow) / 2))
    print("both shallow: %.1f; the full includer against a shallow run: %.1f" % (shallow, (full + shallow) / 2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
