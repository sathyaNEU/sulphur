"""task10 architecture 5: the ceiling, run as code on the cut pack (supplemental-stumping Part 5): two rows scored on
every ask figure.

Shallow run: the default path (every mess item cleaned, every filed rule read): each zone's event-window fall at its
primary against a weather-adjusted baseline, carried to the 2027/28 contracts at its average delivery per MW scheduled.
Landed run (cracker): the call taken (each zone's fall netted of its linked primary's rise), but the provider's delivery
averaged over the event days rather than read at the design condition, so every delivery and credit sits high.
Each ask figure is a keep when it equals the golden at the prompt's rounding.

    python3 ceiling.py [target]     prints the sheet, the shallow keep, the pair ceiling and the pack digest
"""
import copy
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import estim as E   # noqa: E402
import parse as PA  # noqa: E402


def credit(G, delivery):
    G = copy.deepcopy(G)
    for z in G["zones"]:
        z["delivery"] = delivery(z)
        z["credited"] = z["delivery"] * z["mw28"]
        z["after"] = z["before"] - z["credited"]
        z["over"] = z["after"] > z["firm"]
    G["commit"] = [z["primary"] for z in G["zones"] if z["over"]]
    return G


def cells(G):
    out = {"the primaries to reinforce": "+".join(G["commit"]) or "none"}
    for z in G["zones"]:
        p = z["primary"]
        out["%s delivery per MW" % p] = "%.1f" % z["delivery"]
        out["%s credited MW" % p] = "%d" % round(z["credited"])
        out["%s after flexibility MW" % p] = "%d" % round(z["after"])
        out["%s over firm" % p] = "Yes" if z["over"] else "No"
    return out


def main(target):
    X = PA.load(target)
    G = E.golden_from(X)
    prep, tm, ev = X["_prep"], E.daily_mean(X["weather"]), X["events"]
    base = {z["code"]: E.delivery_records(prep, tm, ev, z["code"]) for z in G["zones"]}
    net = {z["code"]: (E.delivery_records(prep, tm, ev, z["code"], partner=z["linked_code"]) if z["linked_code"]
                       else base[z["code"]]) for z in G["zones"]}
    rows = {"golden": cells(G),
            "shallow": cells(credit(G, lambda z: E.delivery_at(base[z["code"]], net=False, temperature=False))),
            "landed": cells(credit(G, lambda z: E.delivery_at(net[z["code"]], temperature=False)))}
    keep = {"shallow": 0, "landed": 0}
    print("%-42s %-28s %-24s %-24s" % ("ask figure", "golden", "shallow", "landed (cracker)"))
    for k, v in rows["golden"].items():
        out = []
        for r in ("shallow", "landed"):
            hit = rows[r][k] == v
            keep[r] += hit
            out.append("%s %s" % (rows[r][k][:14], "keep" if hit else "miss"))
        print("%-42s %-28s %-24s %-24s" % (k, v[:28], out[0], out[1]))
    n = len(rows["golden"])
    sk, lk = keep["shallow"] / n, keep["landed"] / n
    C = 38 + 7 + 55 * lk
    S = 5 + 7 + 55 * sk
    h = hashlib.sha256()
    for f in sorted(os.listdir(target)):
        h.update(open(os.path.join(target, f), "rb").read())
    print("shallow keep %.1f per cent; landed keep %.1f per cent; C %.1f, S %.1f, pair ceiling %.1f; pack %s"
          % (100 * sk, 100 * lk, C, S, (C + S) / 2, h.hexdigest()[:16]))
    return dict(shallow_keep=100 * sk, landed_keep=100 * lk, C=C, S=S, pair=(C + S) / 2, pack=h.hexdigest()[:16])


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target"))
