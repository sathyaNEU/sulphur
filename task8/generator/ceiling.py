"""task8 architecture 18: the pair ceiling, measured on the cut pack. Two rows, both cleaning every mess item and
reading every filed rule: the landed run takes the deep step (the two-cause model on the shared items) but pools
the regions (no regional everyday deviation); the shallow run pre-equates from the bank's own values. Every ask
figure is scored on both rows against figures.json, on 38 (call and critical components), 7 (instructions) and 55
(asks), with the shallow run given 5 of partial credit on the call. The asks as the answer blocks grade them: the
items below the band (2), none above it (1), the twelve patterns items' chances as a group within 0.02 (1) and each
region's whole mark (1.5 each)."""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import verify as V  # noqa: E402

S = V.S


def main():
    fig = json.load(open(V.FIG))
    papers, bank, latest, meta = V.conform()
    s1 = sorted(s for s, (c, p) in meta.items() if p.startswith("LN1"))
    s2 = sorted(s for s, (c, p) in meta.items() if p.startswith("LN2"))
    i1 = sorted({c for nm, cs in papers.items() if nm.startswith("LN1") and not nm.endswith("2027") for c in cs})
    i2 = sorted({c for nm, cs in papers.items() if nm.startswith("LN2") for c in cs})
    X1, X2 = V.matrix(s1, i1, latest), V.matrix(s2, i2, latest)
    ref = [i1.index(c) for c in papers["LN1-2022"]]
    b1, se1, _ = V.jml(X1, ref, -0.96)
    b2, se2, _ = V.jml(X2, [i2.index(c) for c in papers["LN2-2022"]], 0.50)
    shared = [c for c in i1 if bank[c]["pool"] == "Level 2"]
    d = np.array([b1[i1.index(c)] - b2[i2.index(c)] for c in shared])
    se = np.array([np.hypot(se1[i1.index(c)], se2[i2.index(c)]) for c in shared])
    words = np.array([bank[c]["words"] for c in shared], float)
    ev = np.array([bank[c]["context"] == "everyday" for c in shared], float)
    A = np.column_stack([np.ones_like(d), words / 100.0, -ev])
    wgt = np.sqrt(1 / se ** 2)
    coef = np.linalg.lstsq(A * wgt[:, None], d * wgt, rcond=None)[0]
    p27 = papers["LN1-2027"]
    # the landed run: the golden difficulties, the regions pooled
    bl = np.array([b1[i1.index(c)] if c in i1 else b2[i2.index(c)] + coef[0] + coef[1] * bank[c]["words"] / 100.0
                   for c in p27])
    th = V.solve(np.array([b1[k] for k in ref]), 26)
    # the shallow run: the bank's values throughout
    bs = np.array([bank[c]["b"] for c in p27])
    ths = V.solve(np.array([bank[c]["b"] for c in papers["LN1-2022"]]), 26)
    reg_of = {r["centre"]: r["region_name"] for r in V.read_csv("pacb_learning_centres.csv")}
    sat = {}
    for r in V.read_csv("pacb_candidate_register_2022_2026.csv"):
        if r["status"] == "Sat" and r["candidate_id"]:
            lv = "LN1" if r["level"] in ("Level 1", "L1") else "LN2"
            sat[(r["candidate_id"], "%s-%s" % (lv, r["paper_year"]))] = r["sat_at"]
    s26 = [s for s in s1 if meta[s][1] == "LN1-2026"]
    p26 = papers["LN1-2026"]

    def regions(b_items, b27):
        X26 = np.full((len(s26), len(p26)), np.nan)
        for k, s in enumerate(s26):
            for j, c in enumerate(p26):
                X26[k, j] = latest[(s, c)][1]
        th26 = V.wle(X26, b_items, np.zeros(X26.shape))
        e = np.array([S(t - b27).sum() for t in th26])
        out = {}
        for nm in fig["regions"]:
            sel = np.array([reg_of[sat[meta[s]]] == nm for s in s26])
            out[nm] = int(round(float(e[sel].mean())))
        return out
    reg_land = regions(np.array([b1[i1.index(c)] for c in p26]), bl)
    reg_shal = regions(np.array([bank[c]["b"] for c in p26]), bs)
    pr_pos = ["Q%02d" % (k + 1) for k, c in enumerate(p27) if bank[c]["pool"] == "Level 2"]
    ch_l = {("Q%02d" % (k + 1)): round(float(S(th - bl[k])), 2) for k in range(len(p27))}
    ch_s = {("Q%02d" % (k + 1)): round(float(S(ths - bs[k])), 2) for k in range(len(p27))}
    units = {"patterns chances": 1.0}
    units["below band"] = 2.0
    units["above band"] = 1.0
    for nm in fig["regions"]:
        units["region " + nm] = 1.5
    tot = sum(units.values())

    def score(ch, reg):
        got = units["patterns chances"] * all(abs(ch[q] - fig["chances"][q]) <= 0.02 for q in pr_pos)
        below = [q for q, v in ch.items() if v < 0.20]
        above = [q for q, v in ch.items() if v > 0.90]
        got += units["below band"] * (below == fig["items_below_band"])
        got += units["above band"] * (above == fig["items_above_band"])
        for nm in fig["regions"]:
            got += units["region " + nm] * (reg[nm] == fig["regions"][nm])
        return got / tot
    lc = score(ch_l, reg_land)
    ls = score(ch_s, reg_shal)
    landed = 38 + 7 + 55 * lc
    shallow = 5 + 7 + 55 * ls
    pair = (landed + shallow) / 2
    print("landed run (deep step, regions pooled): asks kept %.3f, score %.1f" % (lc, landed))
    print("shallow run (the bank's values): asks kept %.3f, score %.1f" % (ls, shallow))
    print("pair, one on the call and one off: %.1f" % pair)
    print("pair, both on the call: %.1f" % landed)
    print("shallow keep (per cent of ask weight): %.1f" % (100 * ls))
    json.dump(dict(landed=round(landed, 1), shallow=round(shallow, 1), pair=round(pair, 1), lc=round(lc, 3),
                   ls=round(ls, 3)), open(os.path.join(HERE, "ceiling.json"), "w"), indent=1)
    return 0 if pair <= 50 and ls <= 0.25 else 1


if __name__ == "__main__":
    sys.exit(main())
