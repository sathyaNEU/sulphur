"""The ceiling, run as code on the cut pack (supplemental-stumping Part 5): two rows scored on every ask figure.

Shallow run: the default path (every mess item cleaned, every filed rule read): each district priced at the van time
its stops take over the last twelve months, carried to 2027 by plan parcels; each run's hours as the last twelve
months' run-log hours carried by the run's parcels.
Landed run: the call taken (every combination priced on the fitted run model, so the golden list), but the 2027 year
carried from the last twelve months in proportion to parcels rather than forecast from the plan's stops.
Each ask figure is a keep when it equals the golden at the prompt's rounding.

    python3 ceiling.py [target]     prints the sheet, the shallow keep, the pair ceiling and the pack digest
"""
import hashlib
import math
import os
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as A
import golden as GD


def last12(pk):
    keep = A.base_year(pk)
    hrs = defaultdict(float)
    par = defaultdict(int)
    dpar = defaultdict(int)
    for (d, r), lst in pk.rundays.items():
        if keep(d):
            t0, t1 = pk.runlog[(d, r)]
            hrs[r] += t1 - t0
            for x in lst:
                par[r] += int(x["parcels_delivered"])
                dpar[x["district_code"]] += int(x["parcels_delivered"])
    return hrs, par, dpar


def main(target):
    pk, res, fig = GD.compute(target)
    offer = A.offered(pk)
    hrs, par, dpar = last12(pk)
    plan_run = defaultdict(int)
    for c in pk.plan:
        r = pk.reg.get(c, {}).get("run") or [x for x, ch in pk.chain.items() if c in ch][0]
        plan_run[r] += sum(pk.plan[c])
    runs = list(fig["runs"])
    gold = {"list": sorted(fig["set"]), "net": fig["net_saving_rounded"]}
    for r in runs:
        gold["saved_" + r] = fig["runs"][r]["saved_h_rounded"]
        gold["before_" + r] = fig["runs"][r]["before_rounded"]
        gold["after_" + r] = fig["runs"][r]["after_rounded"]
    # shallow
    tid = A.time_in_district(pk)
    d_set = sorted(c for c in offer if tid[c][1] > tid[c][2])
    sh = {"list": d_set, "net": GD.r5000(sum(tid[c][1] - tid[c][2] for c in d_set))}
    for r in runs:
        b = hrs[r] * plan_run[r] / par[r]
        s = sum(tid[c][0] for c in d_set if c in pk.chain[r])
        sh["saved_" + r], sh["before_" + r], sh["after_" + r] = GD.r50(s), GD.r50(b), GD.r50(b - s)
    # landed, proportional carry
    model, per = res["model"], res["per"]
    keep = A.base_year(pk)
    cnt = defaultdict(lambda: [0] * 12)
    days = [0] * 12
    seen = set()
    for (d, r), lst in pk.rundays.items():
        if keep(d):
            if d not in seen:
                seen.add(d)
                days[int(d[5:7]) - 1] += 1
            for x in lst:
                if x["stop_type"] != "BREAK":
                    cnt[x["district_code"]][int(d[5:7]) - 1] += 1
    mus = {c: [cnt[c][k] / days[k] for k in range(12)] for c in cnt}
    mus["__days__"] = days
    la = {"list": sorted(fig["set"]), "net": GD.r5000(A.proportional_carry(pk, res))}
    for r in runs:
        S = fig["runs"][r]["districts"]
        b = hrs[r] * plan_run[r] / par[r]
        s = 0.0
        if S:
            s = (A.run_hours(model, per, r, mus) - A.run_hours(model, per, r, mus, S)) * \
                sum(sum(pk.plan[c]) for c in S) / sum(dpar[c] for c in S)
        la["saved_" + r], la["before_" + r], la["after_" + r] = GD.r50(s), GD.r50(b), GD.r50(b - s)
    asks = [k for k in gold]
    sk = sum(1 for k in asks if sh[k] == gold[k]) / len(asks)
    lk = sum(1 for k in asks if la[k] == gold[k]) / len(asks)
    C = 38 + 7 + 55 * lk
    S = 5 + 7 + 55 * sk
    print("%-14s %-34s %-34s %-34s" % ("ask figure", "golden", "shallow", "landed (cracker)"))
    for k in asks:
        print("%-14s %-34s %-34s %-34s" % (k, gold[k], "%s %s" % (sh[k], "keep" if sh[k] == gold[k] else "miss"),
                                           "%s %s" % (la[k], "keep" if la[k] == gold[k] else "miss")))
    h = hashlib.sha256()
    for f in sorted(os.listdir(target)):
        h.update(open(os.path.join(target, f), "rb").read())
    print("shallow keep %.1f per cent; landed keep %.1f per cent; C %.1f, S %.1f, pair ceiling %.1f; pack %s"
          % (100 * sk, 100 * lk, C, S, (C + S) / 2, h.hexdigest()[:16]))
    return gold, sh, la, sk, lk


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target"))
