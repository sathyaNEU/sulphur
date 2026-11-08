"""The ask layer's ceiling, measured on the cut pack. Every ask reads the SLI's own numerator (each service's
over-threshold December requests) or the services the call names, so each is scored on two rows: the landed run (the
golden's estimator, every hygiene item cleaned, every filed sentence read) and the shallow run (the default path: each
service's own kept spans reweighted hour by hour on its own balancer count, every hygiene item cleaned, every filed
sentence read, so it reads the incident clock right for the services it names). The landed run is scored twice for
the incident ask: on the export's final service lists read from the declaration (the incident tool's column) and on
the timeline's naming times (PR-SLO-3 5.2 read in full). The lower rungs (an hour-of-day pooling, a day weighting, the
kept share) are printed beside them. Figures are scored at the asks' own rounding: the start order position by
position, shares to the whole per cent, the requests beyond budget to the nearest ten thousand, minutes to the minute.

    python3 ceiling.py [pack_dir]
"""
import os
import sys

import common as K
import analysis as AN
import deliver as D

HERE = os.path.dirname(os.path.abspath(__file__))


def ask_figures(prog, minutes):
    """The fourteen ask figures as the deliverables state them: the start order (five positions), each named
    service's share (five), the share they served together, the requests beyond their budgets, the incident minutes
    in which an incident named one of them (two halves)."""
    order = list(prog["order"]) + [None] * (5 - len(prog["order"]))
    shares = {s: D.whole(prog["share"][s]) for s in prog["order"]}
    return {"order": order[:5], "shares": shares, "over_share": D.whole(prog["over_share"]),
            "beyond": D.nearest(prog["beyond"], 10000), "minutes": [D.whole(v) for v in minutes]}


def score(got, gold):
    """Ask figures kept, out of 14, and per ask."""
    k = {"order": sum(a == b for a, b in zip(got["order"], gold["order"])),
         "shares": sum(got["shares"].get(s) == v for s, v in gold["shares"].items()),
         "over_share": int(got["over_share"] == gold["over_share"]),
         "beyond": int(got["beyond"] == gold["beyond"]),
         "minutes": sum(a == b for a, b in zip(got["minutes"], gold["minutes"]))}
    return sum(k.values()), k


def measure(t):
    g = AN.Golden(t)
    m = g.main()
    N = {s: m[s]["requests"] for s in K.SVC}
    gold_p = AN.programme({s: m[s]["sli"] for s in K.SVC}, N, g.bud)
    gold = ask_figures(gold_p, g.incidents(gold_p["over"]))
    rows = []
    landed_final = ask_figures(gold_p, g.incidents(gold_p["over"], backdate=True))
    rows.append(("Landed run (cracker): the incident tool's final service lists from the declaration", "landed_final",
                 score(landed_final, gold)))
    rows.append(("Landed run: PR-SLO-3 5.2 read in full, each service from its naming time", "landed_full",
                 score(gold, gold)))
    for key, label in (("by_service_hour", "Shallow run (default path): each service's own spans by its own hour"),
                       ("by_hour_of_day", "Rung 2: an hour-of-day pooling"), ("by_day", "Rung 1: a day weighting"),
                       ("unweighted", "Rung 0: the kept spans' own share")):
        p = AN.programme({s: m[s][key] for s in K.SVC}, N, g.bud)
        rows.append((label, key, score(ask_figures(p, g.incidents(p["over"])), gold)))
    return rows


def pair(lc, ls, r=5.0):
    """Sulfur's paper arithmetic (supplemental-stumping Part 0): the call and critical components 38, instruction 7,
    the asks 55; the landed run keeps the call, the shallow run about r of it."""
    on, off = 38 + 7 + 55 * lc, r + 7 + 55 * ls
    return on, off, (on + off) / 2


def main(argv):
    t = argv[1] if len(argv) > 1 else os.path.join(HERE, "..", "target")
    rows = measure(t)
    print("| Path (cracker = lands the call, runs the battery, executes filed documents) | Kept of 14 | Order | Shares |"
          " Together | Beyond | Minutes | Verdict |")
    print("|---|---|---|---|---|---|---|---|")
    for label, key, (k, per) in rows:
        print("| %s | %d of 14 | %d of 5 | %d of 5 | %d | %d | %d of 2 | %s |" % (
            label, k, per["order"], per["shares"], per["over_share"], per["beyond"], per["minutes"],
            "miss" if k < 14 else "keeps"))
    sc = {key: k / 14.0 for _, key, (k, _) in rows}
    ls = sc["by_service_hour"]
    print()
    print("Shallow keep: %.1f per cent of ask weight (the default path's figures at the asks' rounding)." % (100 * ls))
    for key, label in (("landed_final", "landed run on the final service lists"),
                       ("landed_full", "landed run reading 5.2 in full")):
        on, off, pr = pair(sc[key], ls)
        print("Pair ceiling (%s): %.1f (landed %.1f, shallow %.1f)." % (label, pr, on, off))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
