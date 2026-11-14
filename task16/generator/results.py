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
     "R2_rule_a_false", [], "the two indexes", ["L22", "L35", "L28"]),
    ("R3", "rule C's false merges (twins with near-identical first names in one household)", "Component 2",
     "R3_rule_c_false", [], "the indexes, the delivery log, the registrations' times", ["L28", "L03"]),
    ("R4", "rule D's false merges (one SSN and birth date on two people's records)", "Ask 1", "R4_rule_d_false",
     [], "the indexes and the delivery log", []),
    ("R5", "Calder Bay records holding two or more patients", "Ask 2", "R5_overlays", [],
     "Calder Bay's merge history, the delivery log and the blood bank results", ["L03", "L49"]),
    ("R6", "the rule the conversion runs", "Recommendation", "R6_rule", ["R2", "R3", "R8"], "", ["L22", "L28", "L49"]),
    ("R7", "patients left under more than one record once the chosen rule's links are made", "Ask 4",
     "R7_left_after_rule", ["R1", "R6"], "", ["L28", "L49"]),
    ("R8", "rule B's false merges once its blood mismatches are explained", "Component 3", "R8_rule_b_false",
     [], "the blood bank results, Calder Bay's merge history", ["L49"]),
    ("R9", "the recommended rule's links that touch a record holding two or more patients, and the records split",
     "Ask 5", "R9_overlay_links", ["R5", "R6"], "", ["L49", "L03"]),
]
BANDS = {}                                 # set from each result's golden family on the cut pack (forcing.py)
RULE_B_BAND = (0, 8)                       # rule B's false merges, every rival under its cap
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
    res_b0 = A.resolve_discordant(R, F, links["B"], hit)
    left_b = set(res_b0["left_pairs"])
    unexplained = np.array([(int(x), int(y)) in left_b for x, y in zip(ia, ib)], bool)
    # rule B's false merges: the twins one visit or one delivery shows, and every blood mismatch that neither a record
    # holding two patients nor a record's own disagreeing typings explains (counted as found, not scaled from the typed)
    f["B"] = float((evb["same_visit"] | evb["delivery"] | unexplained).sum())
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
    doc = A.documented_failures(R, F, links)
    ovl = {k: A.overlay_links(R, links[k], hit) for k in A.RULES}
    res_b = A.resolve_discordant(R, F, links["B"], hit)
    left_by = {k: A.index_figures(Rx, root, links[k])["left"] for k in A.RULES}
    left_by["none"] = A.index_figures(Rx, root, (np.array([], int), np.array([], int)))["left"]
    c_at = {}
    for thr in (0.3, 0.7):
        rt, inf = A.link_index(Rx, F, eq, voc2, threshold=thr, must=must, cannot_extra=cannot)
        ia, ib = links["C"]
        c_at[thr] = float(A.false_links(rt[:len(R)], inf["apart"], ia, ib).sum())
    return dict(links=n_links, false=f, rate=rate, rule=rule, overlays=n_ov, overlay_mrns=sorted(hit),
                documented=doc, overlay_links=ovl.get(rule, dict(links=0, records=0)), overlay_links_all=ovl,
                resolve_b=res_b, left_by_rule=left_by, c_at=c_at,
                overlays_forms=int(A.overlays(F, eq, "golden", namecheck="forms")[0]),
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
    """The careful but hurried pass, the stump factorial's reflex route: every file conformed, a probabilistic linkage of
    the active records, each rule's links reproduced (R80), and each rule read off the confirming files' direct counts of
    documented failures against its allowance with no model of the error rate (R79): rule A at the chance agreement each
    field's own rate gives, raised only as far as its blood-discordant links with different SSNs scale to; rules C and D
    at the twins the delivery log and one registration visit document (rule D also every link whose first names are not
    one person's); rule B's blood mismatches held as false merges until explained; Calder Bay's index as it stands."""
    R, eq, voc, links = S or setup(F)
    root, info = A.link_index(R, F, eq, voc)
    fig = A.index_figures(R.assign(active=True), root, links["B"])
    n_links = {k: int(len(links[k][0])) for k in A.RULES}
    doc = A.documented_failures(R, F, links)
    nz = A.marker_noise(F)
    f = {}
    d = doc["A"]
    scaled = d["discordant_other_ssn"] / nz["p_diff"] * d["links_read"] / max(d["typed"], 1)
    f["A"] = max(A.chance_independent(R), scaled)
    f["B"] = A.marker(R, F, links["B"], (), nz)["as_read"]
    f["C"] = float(doc["C"]["documented_twins"])
    ia, ib = links["D"]
    forms = A.NameForms(eq)
    fn, ln = R["first"].to_numpy(), R["last"].to_numpy()
    inc = np.array([not forms.compatible(fn[x], ln[x], fn[y], ln[y]) for x, y in zip(ia, ib)], bool)
    evd = A.two_people(R, F, ia, ib)
    f["D"] = float((inc | evd["same_visit"] | evd["delivery"]).sum())
    rate = {k: per2000(f[k], n_links[k]) for k in A.RULES}
    rule = choose(n_links, rate)
    left = A.index_figures(R.assign(active=True), root, links[rule])["left"] if rule in links else fig["left"]
    ov = A.overlay_links(R, links[rule], []) if rule in links else dict(links=0, records=0)
    return dict(links=n_links, false=f, rate=rate, rule=rule, overlays=0, documented=doc,
                persons=fig["persons"], both=fig["both"], left=left, left_B=fig["left"], overlay_links=ov)


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
                persons=persons, both=both, left=left, overlay_links=dict(links=0, records=0))


def tables(G):
    return {
        "R1_index": {"distinct patients": int(G["persons"]), "patients in both indexes": int(G["both"])},
        "R2_rule_a_false": round(G["false"]["A"], 1),
        "R3_rule_c_false": int(round(G["false"]["C"])),
        "R4_rule_d_false": int(round(G["false"]["D"])),
        "R5_overlays": int(G["overlays"]),
        "R7_left_after_rule": int(G["left"]),
        "R6_rule": G["rule"],
        "R8_rule_b_false": int(round(G["false"]["B"])),
        "R9_overlay_links": {"links": int(G["overlay_links"]["links"]), "records split": int(G["overlay_links"]["records"])},
    }


def bands(TG):
    b = {"R1_index": {k: [int(v * (1 - CELL_TOL[k])), int(v * (1 + CELL_TOL[k]) + 0.5)] for k, v in TG["R1_index"].items()}}
    for k, (lo, hi) in BANDS.items():
        b[k] = [lo, hi]
    v = TG["R7_left_after_rule"]
    b["R7_left_after_rule"] = [int(v * (1 - LEFT_TOL)), int(v * (1 + LEFT_TOL) + 0.5)]
    b["R8_rule_b_false"] = list(RULE_B_BAND)
    v = TG["R9_overlay_links"]
    b["R9_overlay_links"] = {k: [int(x * 0.85), int(x * 1.15 + 0.5) + 1] for k, x in v.items()}
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
