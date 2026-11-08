"""The pair ceiling, measured on the cut pack (supplemental-stumping Part 0). No model runs here: each route is a
construction the generator executes. The cracker lands the call, runs the hygiene battery (each hour once with the
later delivery kept, UTC to Norwegian time, the meters joined by unit ID, Snoholt's old municipality number, the
changed meters added) and rolls the population register back to 1 November by undoing every later event as the
register writes it, the November renumberings read as moves. The mirror stops on the best-scoring wrong rung of the
ladder and takes the golden's own register rollback, the most generous route it could take through the asks.

Weights 38 / 7 / 55: the main block's 38 as the call 8, each municipality's vacant dwellings and share 1.35 each and
the intervals lying wholly above the line 3; the 55 over the 50 register-quality figures (overcoverage and its rate,
undercoverage and its rate, the net bias, for each of the ten).

    python3 task5/generator/ceiling.py [target]
"""
import hashlib
import os
import sys
import warnings

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
warnings.filterwarnings("ignore")

import golden as G      # noqa: E402
import methods as M     # noqa: E402
import world as W       # noqa: E402

TASK = os.path.dirname(HERE)
ALL = [m[0] for m in W.MUNICIPALITIES]
CELLS = ("over", "over_rate", "under", "under_rate", "net_bias")


def main(target):
    d = M.load(target)
    gres, _ = M.call(d)
    gold = M.designated(gres)

    def quality(handling="golden", rule="golden", floor=None):
        pp = M.persons_nov1(d, handling).groupby("dw").size()
        res, c = M.call(d, rule, floor)
        q = M.coverage(c.assign(persons=c["bruksenhet_id"].map(pp).fillna(0).astype(int)))
        return res, {nr: {k: (v if isinstance(v, int) else "%.1f" % v) for k, v in q[nr].items()} for nr in ALL}

    _, gq = quality()

    def above(res):
        return sorted(nr for nr in ALL if G.clears(res[nr]["vacant"], res[nr]["counted"]))

    def main_score(res):
        call = M.designated(res) == gold
        hits = sum((res[nr]["vacant"] == gres[nr]["vacant"]) + (res[nr]["share"] == gres[nr]["share"]) for nr in ALL)
        return 8 * call + 1.35 * hits + 3 * (above(res) == above(gres)), call, hits

    def ask_score(q):
        h = sum(q[nr][k] == gq[nr][k] for nr in ALL for k in CELLS)
        return 55.0 * h / 50.0, h

    cres, cq = quality("book")
    c_main, _, _ = main_score(cres)
    c_ask, ch = ask_score(cq)
    C = c_main + 7 + c_ask
    print("cracker: call landed, main %.1f + instructions 7 + register table %.1f (%d of 50) = %.1f" % (
        c_main, c_ask, ch, C))
    rungs = {"the register's empty dwellings": ("register", None),
             "the register's empty dwellings with no household rise": ("reg_and_shape", None)}
    for c in (0.3, 0.5, 0.8, 1.0):
        rungs["the household rise at %.1f kWh" % c] = ("rise", c)
    for f in (1, 3, 5, 10, 10.5, 11, 12, 15):
        rungs["a consumption floor of %s kWh a day" % f] = ("level", float(f))
    best = None
    for k, (rule, fl) in rungs.items():
        res, q = quality(rule=rule, floor=fl)
        m, call, hits = main_score(res)
        a, h = ask_score(q)
        S = m + 7 + a
        print("mirror on %-55s main %.1f (call %s, %2d of 20 figures) + 7 + register table %.1f (%d of 50) = %.1f" % (
            k, m, call, hits, a, h, S))
        if best is None or S > best[0]:
            best = (S, k, h)
    pair = (C + best[0]) / 2
    zp = os.path.join(TASK, "target.zip")
    dig = hashlib.sha256(open(zp, "rb").read()).hexdigest()[:16] if os.path.exists(zp) else "no zip"
    print("Pair ceiling: %.1f (cracker %.1f, best mirror %.1f on %s), pack %s" % (pair, C, best[0], best[1], dig))
    print("Mirror leakage: %.1f per cent of ask weight (%d of 50 figures)" % (100.0 * best[2] / 50, best[2]))
    for k, h in (("the register as it stands on 5 January", "snapshot"),
                 ("the dead and emigrated not added back", "no_deaths"),
                 ("every device handled (the golden)", "golden")):
        print("register table on %-45s %2d of 50" % (k, ask_score(quality(h)[1])[1]))
    return pair


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target"))
