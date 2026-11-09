"""task10 architecture 5: the ceiling, run as code on the cut pack (supplemental-stumping Part 5), every ask scored.

Rows, each a complete route with every mess item cleaned and every filed rule read:
  shallow       the default path: each zone's event-window fall at its primary against a weather-adjusted baseline,
                carried to the 2027/28 contracts at its average delivery per MW scheduled
  zone fall     the off-call route the platform measured (run 2): the zone's fall regressed on temperature and read at
                each day assessed
  cracker       the landed run that takes the deep step and the design day (both platform runs read minus 3.0 C) but
                not the asks' own second judgment: the design day's credit carried to the colder working weekdays
  cracker (avg) the design's first landed row: the fall netted of the linked rise, averaged over the event days
  full includer every judgment taken (the golden's own route): the worst honest landed row
Each figure is a keep when it equals the golden at the prompt's rounding; each Supplementary Questions item is a keep
only when every figure it states is. Scores are on the house split (call and components 38, instruction 7, asks 55).

    python3 ceiling.py [target]     prints the sheet, the shallow keep, the pair ceilings and the pack digest
"""
import hashlib
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import estim as E   # noqa: E402
import parse as PA  # noqa: E402


def route(G, X, delivery, before=None):
    """The golden-shaped result of a route: delivery(z, T) per MW scheduled at the design day and the colder days."""
    zones = []
    for z in G["zones"]:
        r1, r2 = X["rates"][z["code"]]
        g = (1 + r1 / 100.0) * (1 + r2 / 100.0)
        reg = X["growth"].get(z["code"], 0.0)
        b_at = lambda T, z=z: (z["d26"] + z["slope"] * (max(0.0, E.BASE_T - T) - max(0.0, E.BASE_T - E.T_DESIGN))) * g + reg
        d = delivery(z, E.T_DESIGN)
        after = z["before"] - d * z["mw28"]
        sens = {T: b_at(T) - delivery(z, T) * z["mw28"] > z["firm"] for T in E.SENS_TS}
        zones.append(dict(primary=z["primary"], delivery=d, credited=d * z["mw28"], after=after, firm=z["firm"],
                          over=after > z["firm"], over_by=after - z["firm"], sens=sens))
    return dict(zones=zones, commit=[z["primary"] for z in zones if z["over"]],
                sens={T: [z["primary"] for z in zones if z["sens"][T]] for T in E.SENS_TS})


def cells(R, golden_commit):
    """Every figure the Supplementary Questions state, keyed by the item that states it."""
    out = {}
    call = "+".join(R["commit"]) or "none"
    for z in R["zones"]:
        p = z["primary"]
        out[(1, "%s delivery per MW" % p)] = "%.1f" % z["delivery"]
        out[(2, "%s credited MW" % p)] = "%d" % round(z["credited"])
        out[(3, "%s after flexibility MW" % p)] = "%d" % round(z["after"])
    out[(3, "over firm capacity")] = call
    out[(4, "chart: after above firm at")] = call
    byp = {z["primary"]: z for z in R["zones"]}
    for p in golden_commit:
        out[(5, "%s exceeds firm by" % p)] = ("%d" % round(byp[p]["over_by"])) if byp[p]["over"] else "holds"
    for T in E.SENS_TS:
        out[(6, "over firm at %.1f C" % T)] = "+".join(R["sens"][T]) or "none"
    out[(7, "slides name")] = call
    return out


def main(target):
    X = PA.load(target)
    G = E.golden_from(X)
    prep, tm, ev = X["_prep"], E.daily_mean(X["weather"]), X["events"]
    base = {z["code"]: E.delivery_records(prep, tm, ev, z["code"]) for z in G["zones"]}
    net = {z["code"]: (E.delivery_records(prep, tm, ev, z["code"], partner=z["linked_code"]) if z["linked_code"]
                       else base[z["code"]]) for z in G["zones"]}

    def fit(recs, netted):
        y = np.array([((r[3] - r[4]) if netted else r[3]) / r[2] for r in recs])
        c = np.polyfit(np.array([r[1] for r in recs]), y, 1)
        return lambda T: float(np.polyval(c, T))
    fn = {z["code"]: fit(net[z["code"]], True) for z in G["zones"]}
    fg = {z["code"]: fit(base[z["code"]], False) for z in G["zones"]}
    rows = {
        "golden": route(G, X, lambda z, T: fn[z["code"]](T)),
        "shallow": route(G, X, lambda z, T: E.delivery_at(base[z["code"]], net=False, temperature=False)),
        "zone fall": route(G, X, lambda z, T: fg[z["code"]](T)),
        "cracker": route(G, X, lambda z, T: fn[z["code"]](E.T_DESIGN)),
        "cracker (avg)": route(G, X, lambda z, T: E.delivery_at(net[z["code"]], temperature=False)),
        "full includer": route(G, X, lambda z, T: fn[z["code"]](T)),
    }
    gold = cells(rows["golden"], rows["golden"]["commit"])
    items = sorted({k[0] for k in gold})
    score = {}
    print("%-44s %-22s %-14s %-14s %-14s %-14s %-14s" % ("ask figure", "golden", "shallow", "zone fall", "cracker",
                                                           "cracker (avg)", "full includer"))
    for k, v in gold.items():
        line = "%-44s %-22s" % ("%d %s" % k, v[:22])
        for r in ("shallow", "zone fall", "cracker", "cracker (avg)", "full includer"):
            c = cells(rows[r], rows["golden"]["commit"])
            hit = c[k] == v
            line += " %-14s" % ("%s %s" % (c[k][:8], "keep" if hit else "miss"))
        print(line)
    for r in ("shallow", "zone fall", "cracker", "cracker (avg)", "full includer"):
        c = cells(rows[r], rows["golden"]["commit"])
        fig = sum(c[k] == v for k, v in gold.items()) / len(gold)
        itm = sum(all(c[k] == v for k, v in gold.items() if k[0] == i) for i in items) / len(items)
        score[r] = (fig, itm)
    landed = lambda keep: 38 + 7 + 55 * keep
    shallow = lambda keep: 5 + 7 + 55 * keep
    pair = lambda a, b, j: (landed(score[a][j]) + shallow(score[b][j])) / 2
    h = hashlib.sha256()
    for f in sorted(os.listdir(target)):
        h.update(open(os.path.join(target, f), "rb").read())
    print("\nkeeps (share of figures, share of items):",
          {r: "%.3f, %.3f" % s for r, s in score.items()})
    out = dict(shallow_keep=100 * score["shallow"][0], shallow_keep_items=100 * score["shallow"][1],
               pair=pair("cracker", "shallow", 0), pair_items=pair("cracker", "shallow", 1),
               pair_avg=pair("cracker (avg)", "shallow", 0),
               full_vs_zone=pair("full includer", "zone fall", 0), full_vs_zone_items=pair("full includer", "zone fall", 1),
               cracker_vs_zone=pair("cracker", "zone fall", 0), pack=h.hexdigest()[:16])
    print("shallow keep %.1f per cent of figures (%.1f of items); pair ceiling %.1f (cracker against the default path, by "
          "figure; %.1f by item; %.1f with the averaging cracker); the full includer against the measured off-call route "
          "%.1f by figure, %.1f by item; the cracker against it %.1f; pack %s"
          % (out["shallow_keep"], out["shallow_keep_items"], out["pair"], out["pair_items"], out["pair_avg"],
             out["full_vs_zone"], out["full_vs_zone_items"], out["cracker_vs_zone"], out["pack"]))
    return out


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target"))
