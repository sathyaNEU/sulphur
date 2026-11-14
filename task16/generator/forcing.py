"""task16 forcing: the stump factorial on the generator's own switches (rule A's chance agreement read from the joint
distribution, rule C's twins the delivery log and the visits do not show, rule B's blood mismatches explained by the
records that hold two patients), each member's direct route (the confirming files read as they stand), the golden
family's rival methods, each fitted input moved by its spread, what each one-sentence hint rescues, the bands, and the
open members the design note reads."""
import numpy as np

import analysis as A
import params as P
import results as RS

STUMPS = [("S_A", "A", "rule A's false merges from the joint distribution of first names, surnames, sex and birth "
                       "years, each pair's chance of one birth date read from its surname community's document dates",
           ["L22", "L35", "L28"]),
          ("S_C", "C", "rule C's false merges from the twins the probabilistic linkage keeps apart, the delivery log's "
                       "and the visits' twins and the ones neither shows", ["L28", "L03"]),
          ("S_B", "B", "rule B's blood mismatches explained: the records that hold two patients and the specimens a "
                       "record's own typings contradict, the rest left as false merges", ["L49"])]


def rates(n, f):
    return {k: RS.per2000(f[k], n[k]) for k in A.RULES}


def route_tables(G, f, call):
    """The graded results a route files: its rule false merges, its call and what follows from the call."""
    ov = G["overlay_links_all"].get(call, dict(links=0, records=0))
    return {"R2_rule_a_false": round(f["A"], 1), "R3_rule_c_false": int(round(f["C"])), "R4_rule_d_false": int(round(f["D"])),
            "R8_rule_b_false": int(round(f["B"])), "R6_rule": call, "R7_left_after_rule": int(G["left_by_rule"].get(call, G["left_by_rule"]["none"])),
            "R9_overlay_links": {"links": int(ov["links"]), "records split": int(ov["records"])}}


def inside(b, v):
    if isinstance(b, dict):
        return all(b[k][0] <= v[k] <= b[k][1] for k in b)
    return b[0] <= v <= b[1]


def moved(G, B, t):
    out = []
    for key, rid in (("R2_rule_a_false", "R2"), ("R3_rule_c_false", "R3"), ("R4_rule_d_false", "R4"), ("R8_rule_b_false", "R8"),
                     ("R7_left_after_rule", "R7"), ("R9_overlay_links", "R9")):
        if key in B and not inside(B[key], t[key]):
            out.append(rid)
    if t["R6_rule"] != G["rule"]:
        out.append("R6")
    return sorted(out)


def run(F, G, C, S):
    R, eq, voc, links = S
    n = G["links"]
    fg, fc = dict(G["false"]), dict(C["false"])
    allow = {k: n[k] / P.CAP_PER for k in A.RULES}
    call = lambda f: RS.choose(n, rates(n, f))
    # ------------------------------------------------------------------ the golden family (rival methods)
    fam = []
    for nm, kw in (("rule A's document dates read by birth decade alone, no surname communities", dict(heap_by=("decade",))),
                   ("rule A with each community's 1 January share lightly shrunk toward its decade", dict(shrink=5.0)),
                   ("rule A with each community's 1 January share heavily shrunk toward its decade", dict(shrink=60.0))):
        f = dict(fg); f["A"] = A.chance_rule_a(R, **kw)
        fam.append(dict(name=nm, member="A", value=round(f["A"], 1), answer=call(f)))
    for nm, thr in (("rule C on the linkage at a match probability of 0.3", 0.3), ("rule C on the linkage at a match probability of 0.7", 0.7)):
        f = dict(fg); f["C"] = G["c_at"][thr]
        fam.append(dict(name=nm, member="C", value=round(f["C"], 1), answer=call(f)))
    mk = G["marker"]
    rb = G["resolve_b"]
    f = dict(fg); f["B"] = fg["B"] + rb["mislabel"]
    fam.append(dict(name="rule B with the mismatches a record's own disagreeing typings explain counted as false merges too",
                    member="B", value=round(f["B"], 1), answer=call(f)))
    f = dict(fg); f["B"] = float((evb_any := A.two_people(R, F, *links["B"])["any"]).sum())
    fam.append(dict(name="rule B with every link a visit, a delivery or differing blood groups shows counted, the "
                         "overlaid records' mismatches left out", member="B", value=round(f["B"] - rb["overlay"], 1),
                    answer=call(dict(f, B=f["B"] - rb["overlay"]))))
    ia, ib = links["D"]
    forms = A.NameForms(eq)
    fn, ln = R["first"].to_numpy(), R["last"].to_numpy()
    inc = np.array([not forms.compatible(fn[x], ln[x], fn[y], ln[y]) for x, y in zip(ia, ib)], bool)
    evd = A.two_people(R, F, ia, ib)
    eqg = A.equivalents(F["names"])

    def plain(x, y):
        if x == y or A.jw_py(x, y) >= 0.85 or (eqg.get(x, set()) & eqg.get(y, set())):
            return True
        tx, ty = x.split(" ")[0], y.split(" ")[0]
        return tx == ty or A.jw_py(tx, ty) >= 0.85 or bool(eqg.get(tx, set()) & eqg.get(ty, set()))
    crude = np.array([not (plain(fn[x], fn[y]) or (plain(fn[x], ln[y]) and plain(ln[x], fn[y]))) for x, y in zip(ia, ib)], bool)
    for nm, est in (("rule D from incompatible first names alone", inc), ("rule D with blood groups added", inc | evd["any"]),
                    ("rule D on a name rule without typing slips, with the delivery log and one visit",
                     crude | evd["same_visit"] | evd["delivery"])):
        f = dict(fg); f["D"] = float(est.sum())
        fam.append(dict(name=nm, member="D", value=f["D"], answer=call(f)))
    # ------------------------------------------------------------------ the bands, from the family
    by = {m: [fg[m]] + [x["value"] for x in fam if x["member"] == m] for m in A.RULES}
    RS.BANDS.clear()
    lo_a = max(allow["A"] + 1.0, 0.85 * min(by["A"])); RS.BANDS["R2_rule_a_false"] = (round(lo_a, 1), round(1.15 * max(by["A"]), 1))
    lo_c = max(allow["C"] + 1.0, 0.85 * min(by["C"])); RS.BANDS["R3_rule_c_false"] = (int(np.floor(lo_c)), int(np.ceil(1.15 * max(by["C"]))))
    RS.BANDS["R4_rule_d_false"] = (int(np.floor(0.85 * min(by["D"]))), int(np.ceil(1.15 * max(by["D"]))))
    ov = [G["overlays"], G["overlays_forms"]]
    RS.BANDS["R5_overlays"] = (int(0.92 * min(ov)), int(np.ceil(1.08 * max(ov))))
    B = RS.bands(RS.tables(G))
    # ------------------------------------------------------------------ the factorial
    routes = [dict(name="the golden: every stump right", answer=G["rule"], golden=True, false={k: round(v, 1) for k, v in fg.items()})]
    routes.append(dict(name="the reflex route (the careful but hurried pass): the documented failures counted, rule B's mismatches held",
                       answer=C["rule"], golden=False, false={k: round(v, 1) for k, v in fc.items()}))
    judg = []
    for sid, m, nm, prec in STUMPS:
        f = dict(fg); f[m] = fc[m]; cd = call(f); td = route_tables(G, f, cd)
        f2 = dict(fc); f2[m] = fg[m]; ca = call(f2); ta = route_tables(G, f2, ca)
        tc = route_tables(G, fc, C["rule"])
        resc = [r for r in moved(G, B, tc) if r not in moved(G, B, ta)]
        judg.append(dict(id=sid, name=nm, kind="stump", precedent=prec, member=m,
                         dropped=dict(answer=cd, results_moved=moved(G, B, td)), alone=dict(answer=ca, results_rescued=resc)))
        routes.append(dict(name="the golden with %s dropped (%s)" % (sid, nm[:60]), answer=cd, golden=False))
        routes.append(dict(name="the reflex route with %s fixed alone" % sid, answer=ca, golden=False))
    judg += [dict(id="J1", name="each rule's links reproduced by the engine's standardization", kind="reflex", precedent=["R80"]),
             dict(id="J2", name="the confirming files' documented failures counted against each rule's allowance", kind="reflex", precedent=["R79"]),
             dict(id="J3", name="rule D's links whose first names are not one person's, the subscriber's SSN on a dependent", kind="reflex", precedent=["R79", "R14"]),
             dict(id="J4", name="both indexes conformed and a probabilistic linkage of the active records", kind="reflex", precedent=["R01", "R20"])]
    # ------------------------------------------------------------------ the direct routes and other shortcuts
    for nm, key in (("every rule from the blood bank's results as they read", "as_read"),
                    ("every rule from the blood bank's results net of wrong blood in tube", "net_of_wbit")):
        f = {k: mk[k][key] for k in A.RULES}
        routes.append(dict(name=nm, answer=call(f), golden=False, false={k: round(v, 1) for k, v in f.items()}))
    f = dict(fg); f["B"] = mk["B"]["net"]
    routes.append(dict(name="rule B's blood mismatches net of wrong blood in tube and of the records holding two patients, "
                            "scaled from its typed links to all of them as if they were a sample", answer=call(f), golden=False))
    inc_f = {k: v["false"] for k, v in G["incumbent"].items()}
    routes.append(dict(name="the engine's national chance rates and the pilot's reviewed pairs", answer=call(inc_f), golden=False))
    doc = G["documented"]
    f = dict(fg); f["C"] = float(doc["C"]["documented_twins"])
    routes.append(dict(name="rule C at the twins the delivery log and one visit document, the rest golden", answer=call(f), golden=False))
    # ------------------------------------------------------------------ perturbations (each fitted input by 20 per cent)
    pert = []
    for nm, m, s in (("rule A's estimate 20 per cent lower", "A", 0.8), ("rule C's estimate 20 per cent lower", "C", 0.8),
                     ("rule D's estimate 20 per cent lower", "D", 0.8), ("rule B's estimate three times higher", "B", 3.0)):
        f = dict(fg); f[m] = f[m] * s
        pert.append(dict(input=nm, answer=call(f)))
    # ------------------------------------------------------------------ hints: each stump's sentence on the reflex route
    sent = {"S_A": "Two different patients here often share a first name, last name, birth date and sex: names cluster "
                   "by community and birth year, and many men who came to work the boats carry 1 January birth dates.",
            "S_C": "Many twins in the indexes were never registered together and were born outside the two hospitals, "
                   "so neither the delivery log nor the visits show them.",
            "S_B": "Rule B's blood mismatches sit on Calder Bay records that already hold two patients, or on a record "
                   "whose own typings disagree."}
    hints = [dict(sentence=sent[j["id"]], rescues=j["alone"]["results_rescued"]) for j in judg if j["kind"] == "stump"]
    # ------------------------------------------------------------------ open members, for the note
    nz = G["noise"]
    dA = doc["A"]
    direct = {"A": dA["discordant_other_ssn"] / nz["p_diff"] * dA["links_read"] / max(dA["typed"], 1) + G["incumbent"]["A"]["false"],
              "B": mk["B"]["as_read"], "C": float(doc["C"]["documented_twins"]),
              "D": float((inc | evd["same_visit"] | evd["delivery"]).sum())}
    fam_spread = {m: round(max(abs(v - fg[m]) for v in by[m]), 1) for m in A.RULES}
    members = []
    for m in A.RULES:
        g_pass, c_pass, d_pass = fg[m] <= allow[m], fc[m] <= allow[m], direct[m] <= allow[m]
        opener = next((sid for sid, mm, _, _ in STUMPS if mm == m), None)
        members.append(dict(member=m, golden=round(fg[m], 1), allowance=round(allow[m], 1), margin=round(fg[m] - allow[m], 1),
                            family_spread=fam_spread[m], reflex=round(fc[m], 1), reflex_right=(c_pass == g_pass),
                            direct=round(direct[m], 1), direct_right=(d_pass == g_pass),
                            opened_by=(opener if (c_pass != g_pass or d_pass != g_pass) and opener else "forced")))
    factorial = dict(golden_answer=G["rule"], reflex_route=dict(answer=C["rule"]), judgments=judg)
    forcing = dict(kind="set", golden_answer=G["rule"],
                   golden_family=[dict(name="the golden", answer=G["rule"])] + [dict(name=x["name"], answer=x["answer"]) for x in fam],
                   shortcuts=[dict(name=r["name"], answer=r["answer"]) for r in routes if not r["golden"]],
                   perturbations=pert)
    return dict(routes=routes, hints=hints, forcing=forcing, factorial=factorial, members=members, family=fam,
                bands=B, allow={k: round(v, 1) for k, v in allow.items()})
