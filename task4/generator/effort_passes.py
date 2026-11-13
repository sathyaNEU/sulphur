"""effort.json from the generator's own passes on the cut pack: the golden, the careful but hurried route (the gate
counters' loss, the register as the fleet, the Maplestead pubs and the 2027 Foundry range at the fleet's own turns and
days of cover) and the quick pass, result by result, with each careful-column loss's precedent, the hints, the routes
and the forcing on both sides. Arithmetic on the generator's implementations, never a solver."""
import json

from writeup import r10

SIZES = (50, 30, 20)
K = [str(s) for s in SIZES]


def _cells(d, sizes=SIZES):
    return {str(s): r10(d[s]) for s in sizes}


def composite(f):
    """the per-size tables figures.json carries for effort.json's figures"""
    out = {}
    for key in ("loss", "fleet", "deliv", "need", "buy"):
        out[key] = {str(s): f["%s_%d" % (key, s)] for s in SIZES}
    out["estate"] = {str(s): f["estate_%d" % s] for s in (50, 30)}
    out["store_t"] = {"20": f["store"]}
    return out


def build(G, f):
    g, car, h = G["golden"], G["careful"], G["hurried"]
    c = composite(f)
    bands = lambda key, sizes=SIZES: {str(s): [f["%s_lo_%d" % (key, s)], f["%s_hi_%d" % (key, s)]] for s in sizes}
    res = []
    res.append({"id": "R1", "name": "own kegs lost in the trade in the year to November 2026", "graded_as": "Ask 2",
                "figure": "loss", "golden": c["loss"], "bands": bands("loss"), "depends": [], "independent": "",
                "passes": {"quick": _cells(G["gate_loss"]),
                           "careful": {"value": _cells(car["loss"]), "grade": "missed",
                                       "why": "the depot gate counters' fulls out less empties in, which closes "
                                              "because other brewers' kegs fill the empties and own kegs come back "
                                              "through the exchange and the recovery agent unseen by the gates"},
                           "thorough": c["loss"]},
                "precedent": ["L28", "L26"], "partly_share": 0.67})
    res.append({"id": "R2", "name": "usable kegs owned at 30 November 2026", "graded_as": "Component 1",
                "figure": "fleet", "golden": c["fleet"], "bands": bands("fleet"), "depends": [], "independent": "",
                "passes": {"quick": _cells(G["register"]),
                           "careful": {"value": _cells(car["fleet"]), "grade": "missed",
                                       "why": "the keg register's active kegs, which still carry every keg lost since "
                                              "the November 2023 reconciliation"},
                           "thorough": c["fleet"]},
                "precedent": ["L04", "N13"], "partly_share": 0.67})
    dband = {str(s): [f["deliv_band_lo_%d" % s], f["deliv_band_hi_%d" % s]] for s in SIZES}
    res.append({"id": "R3", "name": "the busiest week's deliveries at normal weather with the 80 per cent range",
                "graded_as": "Ask 4", "figure": "deliv", "golden": c["deliv"], "bands": dband, "depends": [],
                "independent": "",
                "passes": {"quick": {str(s): r10(G["quick_deliv"][s]) for s in SIZES},
                           "careful": {"value": c["deliv"], "grade": "right",
                                       "why": "a weather and calendar regression on the weekly deliveries is the "
                                              "field's textbook move and frontier runs make it unprompted"},
                           "thorough": c["deliv"]}})
    res.append({"id": "R4", "name": "the kegs the Maplestead pubs hold in the busiest week", "graded_as": "Component 3",
                "figure": "estate", "golden": c["estate"], "bands": bands("estate", (50, 30)), "depends": [],
                "independent": "",
                "passes": {"quick": {str(s): r10(G["turns_estate"][s]) for s in (50, 30)},
                           "careful": {"value": {str(s): r10(G["turns_estate"][s]) for s in (50, 30)},
                                       "grade": "partly",
                                       "why": "the estate's volume at the fleet's average days out per trip: the 50 "
                                              "litre line sells near the fleet's pace and lands close, the slow 30 "
                                              "litre lines hold far more than their volume at the fleet's turns"},
                           "thorough": c["estate"]},
                "precedent": ["N01", "L15"], "partly_share": 0.5})
    res.append({"id": "R5", "name": "full Foundry kegs in the cold store in the 20 litre busiest week",
                "graded_as": "Component 4", "figure": "store_t", "golden": c["store_t"],
                "bands": {"20": [f["store_lo"], f["store_hi"]]}, "depends": [], "independent": "",
                "passes": {"quick": {"20": r10(h["store_cover"]["store"])},
                           "careful": {"value": {"20": r10(h["store_cover"]["store"])}, "grade": "missed",
                                       "why": "the November stocktake's days of cover carried to the busiest week's "
                                              "deliveries, which misses the 200-keg lots across up to 18 beers"},
                           "thorough": c["store_t"]},
                "precedent": ["N12", "L17"]})
    res.append({"id": "R6", "name": "kegs needed in circulation in each size's busiest week", "graded_as": "Ask 7",
                "figure": "need", "golden": c["need"], "bands": bands("need"), "depends": ["R4", "R5"],
                "independent": "the 2026 circulation rebuilt from the stocktake, the washer and the fills",
                "passes": {"quick": {str(s): r10(G["quick_need"][s]) for s in SIZES},
                           "careful": {"value": _cells(car["need"]), "grade": "partly",
                                       "why": "the careful route's need carries the estate and the Foundry range at "
                                              "the fleet's turns: 50 litre lands near, 30 and 20 litre short"},
                           "thorough": c["need"]},
                "precedent": ["N01", "N12"], "partly_share": 0.34})
    res.append({"id": "R7", "name": "kegs to buy by size", "graded_as": "Recommendation", "figure": "buy",
                "golden": c["buy"], "bands": bands("buy"), "depends": ["R2", "R4", "R5", "R6"],
                "independent": "",
                "passes": {"quick": _cells(G["quick"]),
                           "careful": {"value": _cells(car["buy"]), "grade": "missed",
                                       "why": "the register's fleet and the turns leave 50 litre unordered and order "
                                              "a tenth of the 30 and 20 litre need"},
                           "thorough": c["buy"]},
                "precedent": ["L04", "N01"]})
    hints = [
        {"sentence": "the keg register still lists every keg lost since its last reconciliation", "rescues": ["R2"]},
        {"sentence": "a pub line holds a keg on tap and its delivery cover whatever it sells", "rescues": ["R4"]},
        {"sentence": "the 2027 Foundry beers are brewed in 200-keg lots", "rescues": ["R5"]},
        {"sentence": "the depots' empties include other brewers' kegs", "rescues": ["R1"]},
    ]
    def tok(x):
        return sorted("%d:%s" % (s, "in" if f["buy_lo_%d" % s] <= x[s] <= f["buy_hi_%d" % s] else
                                 ("over" if x[s] > f["buy_hi_%d" % s] else "under")) for s in SIZES)
    routes = [{"name": "golden", "label": "This order", "answer": tok(g["buy"]), "golden": True,
               "buy": _cells(g["buy"])},
              {"name": "careful but hurried: gate loss, the register, the fleet's turns", "label": "Register and turns",
               "answer": tok(car["buy"]), "buy": _cells(car["buy"])},
              {"name": "quick: last summer's busiest week at the fleet's turns against the register",
               "label": "Last summer at turns", "answer": tok(G["quick"]), "buy": _cells(G["quick"])}]
    for k, v in h.items():
        routes.append({"name": "shortcut: " + k, "label": k, "answer": tok(v["buy"]), "buy": _cells(v["buy"])})
    forcing = {"kind": "set", "golden_answer": tok(g["buy"]),
               "golden_family": [{"name": k, "answer": tok(v["buy"])} for k, v in G["family"].items()],
               "shortcuts": [{"name": "careful but hurried", "answer": tok(car["buy"])},
                             {"name": "quick", "answer": tok(G["quick"])}] +
                            [{"name": k, "answer": tok(v["buy"])} for k, v in h.items() if k != "gate"],
               "perturbations": [{"input": k, "answer": tok(v["buy"])} for k, v in G["perturbed"].items()]}
    return {"results": res, "weights": {"recommendation": 14, "components": 24, "asks": 55, "instruction": 7},
            "hints": hints, "routes": routes, "forcing": forcing}


def write(path, E):
    json.dump(E, open(path, "w"), indent=1)
