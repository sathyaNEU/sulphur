"""task5 architecture 3: the pair ceiling, measured on the cut pack.

Two rows on the rubric's split (call and critical components 38, the asks 55, instruction-following 7): the landed
run takes the deep step (missing reports read by their transmissions, outcomes from the closed quarters) and cleans
every mess item, but carries a seasonal resort at its cell's change; the shallow run is the default path (the field's
imputation, two-quarter delinquents ceased). Each graded figure is kept when it matches the golden at its graded
rounding."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import golden as GD    # noqa: E402
import methods as M    # noqa: E402
import world as W      # noqa: E402

LANDED = dict(seasonal=False)
SHALLOW = dict(classify="none", two_q="zero", seasonal=False, new="zero")


def score(r, g, pk):
    """the rubric as it is generated: the call and the critical components (38), then one criterion per numbered
    supplementary answer (55 shared equally), a list answer kept only when every figure in it matches"""
    des_ok = M.designated(r["change"]) == M.designated(g["change"])
    ch = lambda x, c: round(x["change"][c] + 1e-9, 1)
    h = lambda x: int(round(x / 100.0))
    kr, kg = r["kind"], g["kind"]
    cnt = lambda k, kind: sum(1 for v in k.values() if v == kind)
    main = 8.0 * des_ok
    main += 10.0 * all(cnt(kr, k) == cnt(kg, k) for k in ("batch", "alone"))                 # CC1 the classification
    main += 10.0 * (r.get("kept_alone") is not None and round(r["kept_alone"], 2) == round(g["kept_alone"], 2))  # CC2
    main += 10.0 * all(ch(r, c) == ch(g, c) for c in G_COUNTIES)                               # CC3 the two counties
    items = [
        des_ok,                                                                                  # 1 the sheet names them
        all(h(r["total"][c]) == h(g["total"][c]) for c in W.CODES),                              # 2 December 2026 jobs
        all(h(r["imputed"][c]) == h(g["imputed"][c]) for c in W.CODES),                          # 3 estimated part
        all(ch(r, c) == ch(g, c) for c in W.CODES),                                              # 4 changes
        des_ok,                                                                                  # 5 the chart
        all(cnt(kr, k) == cnt(kg, k) for k in ("batch", "habitual", "alone", "two_q", "new")),   # 6 the employer list
    ]
    ask = 55.0 / len(items) * sum(items)
    return main, ask, main + ask + 7.0


G_COUNTIES = ("009", "019")


def main(task=os.path.dirname(HERE)):
    pk = GD.load_pack(os.path.join(task, "target"))
    g = M.county_change(pk, {})
    g["kept_alone"] = pk.route_ratios(dict(M.GOLDEN))[("alone", "all")]
    rows = {}
    for name, rt in (("landed", LANDED), ("shallow", SHALLOW)):
        r = M.county_change(pk, rt)
        r["kept_alone"] = pk.route_ratios(dict(M.GOLDEN, **rt))[("alone", "all")] if rt.get("classify", "golden") == "golden" else None
        rows[name] = score(r, g, pk)
    pair = (rows["landed"][2] + rows["shallow"][2]) / 2
    keep = rows["shallow"][1] / 55.0 * 100
    out = dict(landed=rows["landed"], shallow=rows["shallow"], pair=round(pair, 1), shallow_keep=round(keep, 1),
               landed_keep=round(rows["landed"][1] / 55.0 * 100, 1))
    print(json.dumps(out))
    return out


if __name__ == "__main__":
    main()
