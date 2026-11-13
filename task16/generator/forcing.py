"""task16 forcing: the call under every combination of the three corrections (chance agreement read from the joint
distribution, twins kept apart, the subscriber's SSN), the golden family's rival methods, each fitted input moved by
its spread, and what each one-sentence hint rescues."""
import itertools

import numpy as np

import analysis as A
import results as RS


def rates(n_links, f):
    return {k: RS.per2000(f[k], n_links[k]) for k in A.RULES}


def run(F, G, C, S):
    R, eq, voc, links = S
    n = G["links"]
    gold_f, care_f = G["false"], C["false"]
    routes = []
    names = {"chance": "rule A's false merges from the joint distribution of names, birth years and birth dates",
             "twins": "rule C's false merges from the twins the delivery log, the visits and the blood groups keep apart",
             "ssn": "rule D's false merges from the records that carry a subscriber's SSN"}
    for k in range(4):
        for combo in itertools.combinations(["chance", "twins", "ssn"], k):
            f = {"A": care_f["A"], "B": care_f["B"], "C": 0.0, "D": 0.0}
            if "chance" in combo:
                f["A"] = gold_f["A"]
                f["B"] = gold_f["B"]
            if "twins" in combo:
                f["C"] = gold_f["C"]
            if "ssn" in combo:
                f["D"] = gold_f["D"]
            call = RS.choose(n, rates(n, f))
            label = "only " + ", ".join(combo) if combo else "no correction (every rule's links taken as true)"
            if len(combo) == 3:
                label = "all three corrections (the golden)"
            routes.append(dict(name=label, corrections=list(combo), answer=call, golden=len(combo) == 3))
    routes.append(dict(name="the careful but hurried pass (the SSN rule dropped on sight, the rest on the engine's checks)",
                       corrections=["ssn (as typed)"], answer=C["rule"], golden=False))
    mk = G["marker"]
    for nm, key in (("every rule's false merges from the blood bank's results as they read", "as_read"),
                    ("every rule's false merges from the blood bank's results net of wrong blood in tube, the records "
                     "holding two patients left in", "net_of_wbit")):
        f = {k: mk[k][key] for k in A.RULES}
        routes.append(dict(name=nm, corrections=["blood groups: " + key], answer=RS.choose(n, rates(n, f)),
                           golden=False, false={k: round(v, 1) for k, v in f.items()}))
    # the golden family: rival methods, each must file the golden rule
    fam = []
    for nm, kw in (("rule A by birth decade only (no surname communities)", dict(heap_by=("decade",))),
                   ("rule A with light shrinkage of each community's 1 January share", dict(shrink=5.0)),
                   ("rule A with heavy shrinkage of each community's 1 January share", dict(shrink=60.0))):
        f = dict(gold_f)
        f["A"] = A.chance_rule_a(R, **kw)
        fam.append(dict(name=nm, answer=RS.choose(n, rates(n, f)), rule_a=round(f["A"], 1)))
    f = {k: G["marker"][k]["net"] for k in A.RULES}
    fam.append(dict(name="every rule's false merges from the blood bank's results net of wrong blood in tube and of the "
                         "records holding two patients", answer=RS.choose(n, rates(n, f)),
                    marker={k: round(v, 1) for k, v in f.items()}))
    ia, ib = links["C"]
    ev = A.two_people(R, F, ia, ib)
    f = dict(gold_f)
    f["C"] = float((ev["same_visit"] | ev["delivery"]).sum())
    fam.append(dict(name="rule C from the evidence on the linked pair alone", answer=RS.choose(n, rates(n, f)),
                    rule_c=f["C"]))
    ia, ib = links["D"]
    forms = A.NameForms(eq)
    fn, ln = R["first"].to_numpy(), R["last"].to_numpy()
    inc = np.array([not forms.compatible(fn[x], ln[x], fn[y], ln[y]) for x, y in zip(ia, ib)], bool)
    evd = A.two_people(R, F, ia, ib)
    for nm, est in (("rule D from incompatible first names alone", inc),
                    ("rule D with blood groups added", inc | evd["any"])):
        f = dict(gold_f)
        f["D"] = float(est.sum())
        fam.append(dict(name=nm, answer=RS.choose(n, rates(n, f)), rule_d=f["D"]))
    # perturbations: each fitted input moved
    pert = []
    for nm, scale in (("rule A's estimate 30 per cent lower", ("A", 0.7)), ("rule C's estimate 30 per cent lower", ("C", 0.7)),
                      ("rule D's estimate 30 per cent lower", ("D", 0.7)), ("rule B's estimate 50 per cent higher", ("B", 1.5))):
        f = dict(gold_f)
        f[scale[0]] = f[scale[0]] * scale[1]
        pert.append(dict(input=nm, answer=RS.choose(n, rates(n, f))))
    hints = [
        dict(sentence="Two different patients here often share a first name, last name, birth date and sex: names "
                      "cluster by community and birth year, and many birth dates were recorded as 1 January.",
             rescues=["R2"]),
        dict(sentence="Twins share a household, a surname and a birth date, and some have near-identical first names.",
             rescues=["R3"]),
        dict(sentence="From March 2019 Calder Bay merged a new registration into an existing record with the same "
                      "last name, birth date and sex.", rescues=["R5"]),
        dict(sentence="A patient's own records can disagree on blood group, from a mislabelled specimen or a record "
                      "that holds two patients.",
             rescues=["R6"] + (["R7"] if abs(C["left_B"] - G["left"]) <= RS.LEFT_TOL * G["left"] else [])),
    ]
    forcing = dict(kind="set", golden_answer=G["rule"], golden_family=fam,
                   shortcuts=[dict(name=r["name"], answer=r["answer"]) for r in routes if not r["golden"]],
                   perturbations=pert)
    return dict(routes=routes, hints=hints, forcing=forcing)
