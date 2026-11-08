"""The ceiling, run as code on the cut pack (supplemental-stumping Part 5): two rows scored on every ask figure.

Shallow run: the default path (every mess item cleaned, every filed rule read): the pilot's energy fitted on the
declared payloads, with both cold rates, applied to each duty's planning load on the design day.
Landed run (cracker): the call taken (each declaration taken to its weighed load shipper by shipper), but one cold
rate below 16 C, so every design-day energy sits low.
Each ask figure is a keep when it equals the golden at the prompt's rounding.

    python3 ceiling.py [target]     prints the sheet, the shallow keep, the pair ceiling and the pack digest
"""
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as A


def r10(x):
    return int(round(x / 10.0) * 10)


def main(target):
    pk = A.load(target)
    g = A.golden(pk)
    M = g["models"]
    rows = {"golden": g["assess"], "shallow": A.assess(pk, M["naive"]), "landed": A.assess(pk, M["golden_1h"])}
    asks = ["the order (count and duties)"] + sorted(pk.short)
    keep = {"shallow": 0, "landed": 0}
    print("%-30s %-22s %-22s %-22s" % ("ask figure", "golden", "shallow", "landed (cracker)"))
    for k in asks:
        if k.startswith("the order"):
            vals = {r: "%d %s" % (len(A.chosen(a)), "+".join(A.chosen(a))) for r, a in rows.items()}
        else:
            vals = {r: "%d kWh" % r10(a[k]["kwh"]) for r, a in rows.items()}
        out = []
        for r in ("shallow", "landed"):
            hit = vals[r] == vals["golden"]
            keep[r] += hit
            out.append("%s %s" % (vals[r][:16], "keep" if hit else "miss"))
        print("%-30s %-22s %-22s %-22s" % (k, vals["golden"][:22], out[0], out[1]))
    sk, lk = keep["shallow"] / len(asks), keep["landed"] / len(asks)
    C = 38 + 7 + 55 * lk
    S = 5 + 7 + 55 * sk
    h = hashlib.sha256()
    for f in sorted(os.listdir(target)):
        h.update(open(os.path.join(target, f), "rb").read())
    print("shallow keep %.1f per cent; landed keep %.1f per cent; C %.1f, S %.1f, pair ceiling %.1f; pack %s"
          % (100 * sk, 100 * lk, C, S, (C + S) / 2, h.hexdigest()[:16]))
    return sk, lk


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target"))
