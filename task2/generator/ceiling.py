"""task2 ceiling: each route to the 2027 ceiling scored on the rubric model (supplemental-stumping Part 0) on the cut
pack, and the pair the platform's two runs would average.

The model: the recommendation 20 (the ceiling), four critical components at 4.5 (the steady share is releases
cancelling a drift; the compulsory starters' level; the 2027 mix; why 10 and 12 fail), instruction-following 7, and
the asks 55 over four supplementary answers, each kept in proportion to its gradable figures the route gets right:
  1 the memo's opening (the ceiling, the first quarter past 10, the first past 12);
  2 the chart (each quarter's band against the ceilings: four);
  3 each quarter's lowest ceiling (four);
  4 the fourth quarter's 90th-percentile word error rate (one, whole per cent).
The landed run takes the compulsory starters, starts each go-live at full volume and reads the percentile off
clinicians' average rates; the shallow run carries the 2026 share forward."""
import math
import os
import sys
from collections import defaultdict

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import checks as CK  # noqa: E402
import golden as GD  # noqa: E402

W_REC, W_COMP, W_IF, W_ASKS = 20.0, 4.5, 7.0, 55.0


def figs_of(G):
    q = [G["q"][k] for k in GD.Q27]
    return dict(ceiling=G["ceiling"], fp=G["first_past"], bands=G["bands"],
                vol=[int(math.floor(f["vol"] / 1e4 + 0.5)) for f in q], p90=[CK.pc(q[3]["p90"])])


def p90_of_levels(P, G):
    """the percentile a run reads off each clinician's average rate under 6.0 instead of off dictations"""
    acc = defaultdict(list)
    for a in P.audits:
        if a["person"] in G["typ"]:
            acc[a["person"]].append(a["wer"] * math.exp(-G["steps"][a["release"]]))
    lv = {"V": [], "M": []}
    for p, v in acc.items():
        lv[G["typ"][p]].append(float(np.mean(v)))
    rates = {k: np.array(v) for k, v in lv.items()}
    w = G["q"][(2027, 4)]["wV"]
    return [CK.pc(GD.mix_quantile(rates, {"V": w, "M": 1 - w}, 0.9))]


def score(g, r, comps):
    sq1 = ((r["ceiling"] == g["ceiling"]) + (r["fp"].get(10) == g["fp"].get(10)) + (r["fp"].get(12) == g["fp"].get(12))) / 3.0
    sq2 = sum(a == b for a, b in zip(r["bands"], g["bands"])) / 4.0
    sq3 = sq2
    sq4 = float(r["p90"] == g["p90"])
    asks = W_ASKS * (sq1 + sq2 + sq3 + sq4) / 4.0
    return W_REC * (r["ceiling"] == g["ceiling"]) + W_COMP * comps + W_IF + asks, asks / W_ASKS


def main(target=None):
    target = target or os.path.join(os.path.dirname(HERE), "target")
    CK.RESULTS.clear()
    C = CK.run(target, HERE)
    P, G = C["P"], C["G"]
    g = figs_of(G)
    landed = figs_of(C["no_ramp"])
    landed["p90"] = p90_of_levels(P, C["no_ramp"])
    flat = CK.route_flat(P, G)
    shallow = dict(ceiling=CK.ceiling_of(flat), fp={c: next((i + 1 for i, x in enumerate(flat) if 100 * x > c), None)
                                                     for c in (10, 12) if any(100 * x > c for x in flat)},
                   bands=[GD.band(x) for x in flat], vol=[int(math.floor(C["record_vol_q4_2026"] / 1e4 + 0.5))] * 4,
                   p90=[CK.pc(GD.mix_quantile(G["rates"], {"V": C["record_wV_2026"], "M": 1 - C["record_wV_2026"]}, 0.9))])
    rows = [("golden", g, 4), ("landed: full volume at go-live, percentile of clinicians' rates", landed, 4),
            ("shallow: the 2026 share carried forward", shallow, 0)]
    res = {}
    for name, r, comps in rows:
        s, keep = score(g, r, comps)
        res[name] = (s, keep)
        print("%-66s ceiling %s fp %s bands %s vol %s p90 %s  score %.1f  asks kept %.1f%%"
              % (name, r["ceiling"], r["fp"], r["bands"], r["vol"], r["p90"], s, 100 * keep))
    la = res["landed: full volume at go-live, percentile of clinicians' rates"][0]
    sh = res["shallow: the 2026 share carried forward"]
    print("pair (landed + shallow) / 2 = %.1f; shallow keep %.1f per cent of the ask weight" % ((la + sh[0]) / 2, 100 * sh[1]))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
