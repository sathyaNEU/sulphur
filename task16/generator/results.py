"""task16 results: the golden reading of the pack, the careful but hurried and quick passes, each shortcut route and
its call, the one-sentence hints, the forcing block, and figures.json and effort.json."""
import json
import os

import numpy as np
import pandas as pd

import analysis as A

RESULTS = [
    ("R1", "the converted index: distinct patients and patients held by both legacy indexes", "Ask 3", "R1_index",
     [], "the two indexes and Calder Bay's merge history", []),
    ("R2", "rule A's false merges (two different patients agreeing on name, birth date and sex)", "Component 1",
     "R2_rule_a_false", [], "the two indexes", ["L22", "L35"]),
    ("R3", "rule C's false merges (twins with near-identical first names in one household)", "Component 2",
     "R3_rule_c_false", [], "the indexes, the delivery log, the blood bank results", ["L28"]),
    ("R4", "rule D's false merges (one SSN and birth date on two people's records)", "Ask 1", "R4_rule_d_false",
     [], "the indexes and the delivery log", []),
    ("R5", "Calder Bay records holding two or more patients", "Ask 2", "R5_overlays", [],
     "Calder Bay's merge history, the delivery log and the blood bank results", ["L03"]),
    ("R6", "the rule the conversion runs", "Recommendation", "R6_rule", ["R2", "R3", "R4"], "", ["L28"]),
    ("R7", "patients left under more than one record once the chosen rule's links are made", "Ask 4",
     "R7_left_after_rule", ["R1", "R6"], "", ["L28"]),
]
BANDS = {"R2_rule_a_false": (65, 170), "R3_rule_c_false": (70, 220), "R4_rule_d_false": (140, 250),
         "R5_overlays": (480, 660)}
RULE_B_BAND = (0, 15)                      # rule B's false merges, every rival under its cap
CELL_TOL = {"distinct patients": 0.015, "patients in both indexes": 0.025}
LEFT_TOL = 0.03


def setup(F):
    R = F["R"]
    eq = A.equivalents(F["names"])
    voc = A.Vocab(R["first"].tolist())
    links = A.rule_links(R, eq, voc)
    return R, eq, voc, links


def per2000(f, n):
    return 2000.0 * f / max(n, 1)


def golden(F, S=None):
    R, eq, voc, links = S or setup(F)
    n_ov, hit, per = A.overlays(F, eq, "golden")
    Rx, must, cannot = A.with_retired(F, R, per)
    voc2 = A.Vocab(Rx["first"].tolist())
    root, info = A.link_index(Rx, F, eq, voc2, must=must, cannot_extra=cannot)
    fig = A.index_figures(Rx, root, links["B"])
    rootA = root[:len(R)]
    f = {}
    f["A"] = A.chance_rule_a(R)
    ia, ib = links["C"]
    f["C"] = float(A.false_links(rootA, info["apart"], ia, ib).sum())
    ia, ib = links["B"]
    evb = A.two_people(R, F, ia, ib)
    f["B"] = float((evb["same_visit"] | evb["delivery"]).sum())
    ia, ib = links["D"]
    forms = A.NameForms(eq)
    fn, ln = R["first"].to_numpy(), R["last"].to_numpy()
    incompat = np.array([not forms.compatible(fn[x], ln[x], fn[y], ln[y]) for x, y in zip(ia, ib)], bool)
    ev = A.two_people(R, F, ia, ib)
    f["D"] = float((incompat | ev["same_visit"] | ev["delivery"]).sum())
    n_links = {k: int(len(links[k][0])) for k in A.RULES}
    rate = {k: per2000(f[k], n_links[k]) for k in A.RULES}
    rule = choose(n_links, rate)
    noise = A.marker_noise(F, hit)
    marker = {k: A.marker(R, F, links[k], hit, noise) for k in A.RULES}
    left = A.index_figures(Rx, root, links[rule])["left"] if rule in links else fig["left"]
    return dict(links=n_links, false=f, rate=rate, rule=rule, overlays=n_ov, overlay_mrns=sorted(hit),
                persons=fig["persons"], both=fig["both"], left=left, marker=marker, noise=noise,
                incumbent=incumbent(R, n_links),
                indep_local=A.chance_independent(R),
                indep_vendor=A.chance_independent(R, u=VENDOR_U),
                _root=root, _Rx=Rx, _links=links)


VENDOR_U = dict(first=0.005, last=0.0011, dob=0.000037, sex=0.5)


def incumbent(R, n_links):
    """What the engine's documentation and the pilot give each rule: chance agreement at the engine's national
    rates (rule A's fields; rule B adds the address's; rule D the SSN's and the birth date's), and for rule C the
    pilot's reviewed pairs, none of which rule C joins."""
    import records as RC
    n = len(R)
    pairs = n * (n - 1) / 2.0
    a = A.chance_independent(R, u=VENDOR_U)
    f = {"A": a, "B": a * RC.VENDOR["addr"]["same"][1], "C": 0.0,
         "D": pairs * RC.VENDOR["ssn"]["same"][1] * RC.VENDOR["dob"]["exact"][1]}
    return {k: dict(false=v, rate=per2000(v, n_links[k])) for k, v in f.items()}


def choose(n_links, rate):
    ok = [k for k in A.RULES if rate[k] <= 1.0]
    return max(ok, key=lambda k: n_links[k]) if ok else "none"


def careful(F, S=None):
    """The careful but hurried pass: every file conformed, a probabilistic linkage of the active records, the rules
    priced on the engine's checks (chance agreement from each field's own rate, the pilot's reviewed pairs), the SSN
    rule dropped on sight of a family's shared SSN, Calder Bay's index taken as it stands."""
    R, eq, voc, links = S or setup(F)
    root, info = A.link_index(R, F, eq, voc)
    fig = A.index_figures(R.assign(active=True), root, links["B"])
    n_links = {k: int(len(links[k][0])) for k in A.RULES}
    f = {"A": A.chance_independent(R)}
    f["B"] = f["A"] * 0.0
    f["C"] = 0.0                                   # the pilot never reviewed a pair rule C joins
    ia, ib = links["D"]
    forms = A.NameForms(eq)
    fn, ln = R["first"].to_numpy(), R["last"].to_numpy()
    f["D"] = float(sum(not forms.compatible(fn[x], ln[x], fn[y], ln[y]) for x, y in zip(ia, ib)))  # two names, one SSN
    rate = {k: per2000(f[k], n_links[k]) for k in A.RULES}
    rule = choose(n_links, rate)
    left = A.index_figures(R.assign(active=True), root, links[rule])["left"] if rule in links else fig["left"]
    return dict(links=n_links, false=f, rate=rate, rule=rule, overlays=0,
                persons=fig["persons"], both=fig["both"], left=left, left_B=fig["left"])


def quick(F, S=None):
    """The ten-minute pass: the indexes as they stand, one patient per exact name, birth date and sex, every rule's
    links taken as true."""
    R, eq, voc, links = S or setup(F)
    key = R["first"] + "|" + R["last"] + "|" + R["dob"].dt.strftime("%Y%m%d") + "|" + R["sex"]
    persons = int(key.nunique())
    both = int((R.assign(k=key).groupby("k")["sys"].nunique() == 2).sum())
    n_links = {k: int(len(links[k][0])) for k in A.RULES}
    rate = {k: 0.0 for k in A.RULES}
    rule = choose(n_links, rate)
    uf = A.UF(len(R))
    for x, y in zip(*links[rule]):
        uf.union(x, y)
    rb = pd.Series([uf.find(i) for i in range(len(R))])
    left = int((pd.DataFrame({"k": key.to_numpy(), "rb": rb}).groupby("k")["rb"].nunique() >= 2).sum())
    return dict(links=n_links, false={k: 0.0 for k in A.RULES}, rate=rate, rule=rule, overlays=0,
                persons=persons, both=both, left=left)


def tables(G):
    return {
        "R1_index": {"distinct patients": int(G["persons"]), "patients in both indexes": int(G["both"])},
        "R2_rule_a_false": round(G["false"]["A"], 1),
        "R3_rule_c_false": int(round(G["false"]["C"])),
        "R4_rule_d_false": int(round(G["false"]["D"])),
        "R5_overlays": int(G["overlays"]),
        "R7_left_after_rule": int(G["left"]),
        "R6_rule": G["rule"],
    }


def bands(TG):
    b = {"R1_index": {k: [int(v * (1 - CELL_TOL[k])), int(v * (1 + CELL_TOL[k]) + 0.5)] for k, v in TG["R1_index"].items()}}
    for k, (lo, hi) in BANDS.items():
        b[k] = [lo, hi]
    v = TG["R7_left_after_rule"]
    b["R7_left_after_rule"] = [int(v * (1 - LEFT_TOL)), int(v * (1 + LEFT_TOL) + 0.5)]
    return b


def write(F, gen_dir, G, C, Q, extra):
    TG, TC, TQ = tables(G), tables(C), tables(Q)
    B = bands(TG)
    figs = dict(TG)
    figs.update({
        "rule_links": G["links"], "rule_false": {k: round(v, 1) for k, v in G["false"].items()},
        "rule_rate_per_2000": {k: round(v, 2) for k, v in G["rate"].items()},
        "careful_rule_false": {k: round(v, 1) for k, v in C["false"].items()},
        "careful_rate_per_2000": {k: round(v, 2) for k, v in C["rate"].items()},
        "careful_rule": C["rule"], "quick_rule": Q["rule"],
        "indep_local": round(G["indep_local"], 1), "indep_vendor": round(G["indep_vendor"], 1),
        "marker": {k: {a: (round(b, 1) if isinstance(b, float) else b) for a, b in v.items()} for k, v in G["marker"].items()},
        "marker_noise": {a: (round(b, 6) if isinstance(b, float) else b) for a, b in G["noise"].items()},
        "incumbent_false": {k: round(v["false"], 2) for k, v in G["incumbent"].items()},
        "incumbent_rate_per_2000": {k: round(v["rate"], 2) for k, v in G["incumbent"].items()},
        "cap_per": 2000,
        "careful_index": {"distinct patients": C["persons"], "patients in both indexes": C["both"]},
        "careful_left": C["left"], "careful_left_after_B": C["left_B"], "careful_overlays": C["overlays"],
    })
    figs.update(extra.get("figures", {}))
    figs["bands"] = B
    figs["rule_b_band"] = list(RULE_B_BAND)
    res = []
    for rid, name, graded, key, dep, indep, prec in RESULTS:
        e = dict(id=rid, name=name, graded_as=graded, figure=key, depends=dep, independent=indep, golden=TG[key])
        if isinstance(TG[key], dict):
            e["bands"] = B[key]
        elif isinstance(TG[key], (int, float)):
            lo, hi = B[key]
            e["band"] = [lo, hi]
            e["partly"] = [round(0.7 * lo, 1), round(1.3 * hi, 1)]
        e["passes"] = {"quick": TQ[key], "careful": TC[key], "thorough": TG[key]}
        if prec:
            e["precedent"] = prec
        res.append(e)
    E = dict(results=res, weights={"recommendation": 14, "components": 24, "asks": 55, "instruction": 7})
    E.update({k: v for k, v in extra.items() if k != "figures"})
    os.makedirs(gen_dir, exist_ok=True)
    json.dump(figs, open(os.path.join(gen_dir, "figures.json"), "w"), indent=1, sort_keys=True, default=_plain)
    json.dump(E, open(os.path.join(gen_dir, "effort.json"), "w"), indent=1, default=_plain)
    return figs, E


def _plain(o):
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    raise TypeError(type(o))
