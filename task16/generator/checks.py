"""task16 checks: the golden against the simulated truth, the call and its two sides, every result's rival methods
against its band, the forks, the input gates and the realism sweep, asserted on the built task folder (target/,
generator/figures.json and effort.json) and on the clean truth.

    python3 task16/generator/checks.py            every check
    python3 task16/generator/checks.py --fast     without the two rival linkages (about four minutes less)
"""
import datetime as dt
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import warnings  # noqa: E402

warnings.filterwarnings("ignore")
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

import analysis as A  # noqa: E402
import deliver as DL  # noqa: E402
import docs as DC  # noqa: E402
import golden as GD  # noqa: E402
import pack as PK  # noqa: E402
import params as P  # noqa: E402
import results as RS  # noqa: E402
import world as WD  # noqa: E402

N = [0, 0]


def ok(label, cond, detail=""):
    N[0] += 1
    if not cond:
        N[1] += 1
    print("%s  %-84s %s" % ("PASS" if cond else "FAIL", label[:84], str(detail)[:150]))


def inside(v, band):
    return band[0] <= v <= band[1]


def pdftext(path):
    return re.sub(r"\s+", " ", subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True,
                                              text=True).stdout)


def main(fast=False):
    target = os.path.join(TASK, "target")
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    E = json.load(open(os.path.join(HERE, "effort.json")))
    BAND = figs["bands"]
    F = GD.load(target)
    S = RS.setup(F)
    R, eq, voc, links = S
    W = WD.build()

    # ---------------------------------------------------------------- the golden against the truth
    pid = {r["mrn"]: r["pid"] for r in W.recs}
    Pr = np.array([pid[m] for m in R["mrn"]])
    truth = {}
    for k in A.RULES:
        ia, ib = links[k]
        truth[k] = int((Pr[ia] != Pr[ib]).sum())
        ok("truth: rule %s's links counted from the pack equal the world's" % k,
           figs["rule_links"][k] == len(ia), (figs["rule_links"][k], len(ia)))
    ok("truth: rule A's false merges inside R2's band", inside(truth["A"], BAND["R2_rule_a_false"]), truth["A"])
    ok("truth: rule C's false merges inside R3's band", inside(truth["C"], BAND["R3_rule_c_false"]), truth["C"])
    ok("truth: rule D's false merges inside R4's band", inside(truth["D"], BAND["R4_rule_d_false"]), truth["D"])
    ok("truth: rule B under its cap, rules A, C and D over theirs",
       truth["B"] <= figs["rule_links"]["B"] / 2000 and all(truth[k] > figs["rule_links"][k] / 2000 for k in "ACD"),
       truth)
    for k in A.RULES:
        g = figs["rule_false"][k]
        tol = 0.30 if k == "A" else 0.15        # rule A's false merges come in lumpy pairs of people; HIM-14 caps the expected count
        ok("truth: the golden's rule %s estimate within %d per cent or 5 of the world's realized count" % (k, int(100 * tol)),
           abs(g - truth[k]) <= max(5, tol * truth[k]), (g, truth[k]))
    holds = {}
    for r in W.recs:
        holds.setdefault(r["final"], set()).add(r["pid"])
    active_a = set(F["index_a"]["MRN"])
    ov_truth = {m for m, v in holds.items() if m in active_a and len(v) >= 2}
    ok("truth: Calder Bay records holding two or more patients inside R5's band", inside(len(ov_truth),
                                                                                       BAND["R5_overlays"]), len(ov_truth))
    persons_t = len({r["pid"] for r in W.recs})
    sys_of = {}
    for r in W.recs:
        sys_of.setdefault(r["pid"], set()).add(r["sys"])
    both_t = sum(1 for v in sys_of.values() if len(v) == 2)
    b1 = BAND["R1_index"]
    ok("truth: distinct patients inside R1's band", inside(persons_t, b1["distinct patients"]), persons_t)
    ok("truth: patients both indexes hold inside R1's band", inside(both_t, b1["patients in both indexes"]), both_t)
    uf = A.UF(len(R))
    for x, y in zip(*links["B"]):
        uf.union(x, y)
    grp = pd.DataFrame({"pid": Pr, "g": [uf.find(i) for i in range(len(R))]})
    left_t = int((grp.groupby("pid")["g"].nunique() >= 2).sum())
    ok("truth: patients left under two or more records after rule B inside R6's band",
       inside(left_t, BAND["R7_left_after_rule"]), left_t)
    print("      truth: false merges %s, overlays %d, patients %d, both %d, left after B %d"
          % (truth, len(ov_truth), persons_t, both_t, left_t))

    # ---------------------------------------------------------------- the call and its two sides
    rt = figs["rule_rate_per_2000"]
    ok("call: rule B, the only rule inside the cap", figs["R6_rule"] == "B" and rt["B"] <= 1.0 and
       all(rt[k] > 1.0 for k in "ACD"), rt)
    ok("margin: rule B at half its line or less, rules A and C at 1.3 times theirs or more, rule D at twice", rt["B"] <= 0.5 and
       rt["A"] >= 1.3 and rt["C"] >= 1.3 and rt["D"] >= 2.0, rt)
    ok("call: the careful but hurried pass (the reflex route) files rule A", figs["careful_rule"] == "A", figs["careful_rule"])
    ok("call: the quick pass files rule A", figs["quick_rule"] == "A", figs["quick_rule"])
    fo = E["forcing"]
    wrong = {s["answer"] for s in fo["shortcuts"]}
    ok("forcing: the shortcuts file four distinct wrong answers (A, C, D, none)", wrong == {"A", "C", "D", "none"},
       sorted(wrong))
    ok("forcing: every golden-family variant files rule B", all(x["answer"] == "B" for x in fo["golden_family"]),
       [x["answer"] for x in fo["golden_family"]])
    ok("forcing: every perturbation leaves rule B", all(x["answer"] == "B" for x in fo["perturbations"]),
       [x["answer"] for x in fo["perturbations"]])
    fac = {j["id"]: j for j in E["factorial"]["judgments"] if j["kind"] == "stump"}
    ok("factorial: each stump dropped alone moves the call to its own wrong answer (A, C, no rule)",
       (fac["S_A"]["dropped"]["answer"], fac["S_C"]["dropped"]["answer"], fac["S_B"]["dropped"]["answer"]) == ("A", "C", "none"),
       {k: v["dropped"]["answer"] for k, v in fac.items()})
    ok("factorial: no stump fixed alone on the reflex route reaches rule B",
       all(v["alone"]["answer"] != "B" for v in fac.values()), {k: v["alone"]["answer"] for k, v in fac.items()})
    mem = {m["member"]: m for m in figs["open_members"]}
    ok("open members: rules A, B and C open, each by its own stump, rule D forced",
       [mem[k]["opened_by"] for k in "ABCD"] == ["S_A", "S_B", "S_C", "forced"], [mem[k]["opened_by"] for k in "ABCD"])
    for k in "ABC":
        mm = mem[k]
        worth = abs(mm["golden"] - mm["reflex"])
        ok("open member %s: the family's spread under its margin, the margin under its stump's worth" % k,
           mm["family_spread"] < abs(mm["margin"]) < worth, (mm["family_spread"], mm["margin"], round(worth, 1)))
        ok("open member %s: the direct route files it wrong" % k, not mm["direct_right"], (mm["direct"], mm["allowance"]))
    doc = figs["documented"]
    ok("direct route: rule A's blood-discordant links with different SSNs (the links rule B does not make) one or none",
       doc["A"]["discordant_other_ssn"] <= 1, doc["A"])
    ok("direct route: rule C's documented twins under its line", doc["C"]["documented_twins"] < figs["rule_links"]["C"] / 2000,
       doc["C"])
    ok("direct route: rule D's documented twins already over its line (a forced member)",
       doc["D"]["documented_twins"] > figs["rule_links"]["D"] / 2000, doc["D"])
    rb_ = figs["resolve_b"]
    ok("R8: rule B's blood mismatches add up (overlay, mislabel, left)", rb_["overlay"] + rb_["mislabel"] + rb_["left"] ==
       rb_["discordant"] and rb_["overlay"] >= 2, rb_)
    ok("R8: rule B's blood mismatches read as they stand put it over its line", figs["marker"]["B"]["as_read"] >
       figs["rule_links"]["B"] / 2000, figs["marker"]["B"]["as_read"])
    ok("R9: rule B's links touching an overlaid record, the records among R5's", 0 < figs["R9_overlay_links"]["records split"]
       <= figs["R5_overlays"] and figs["R9_overlay_links"]["links"] >= figs["R9_overlay_links"]["records split"],
       figs["R9_overlay_links"])

    # ---------------------------------------------------------------- rivals, result by result
    for x in figs["family"]:
        key = {"A": "R2_rule_a_false", "C": "R3_rule_c_false", "D": "R4_rule_d_false", "B": "R8_rule_b_false"}[x["member"]]
        ok("%s rival inside the band: %s" % (key[:2], x["name"]), inside(x["value"], BAND[key]), x["value"])
    # the rivals outside a band, each with the data that rules it out
    e = A.person_entries(R).assign(decade=lambda d: (d["y"] // 10) * 10, j1=lambda d: (d["d"] == "0101"))
    by = e.groupby(["last", "decade"]).agg(n=("j1", "size"), j1=("j1", "mean")).reset_index()
    dec = e.groupby("decade")["j1"].mean()
    big = by[by["n"] >= 200].copy()
    big["ratio"] = big["j1"] / big["decade"].map(dec)
    top = big.sort_values("ratio", ascending=False).head(3)
    ok("R2 named data: large surname communities' 1 January shares run several times their decade's",
       (top["ratio"] >= 3).all(), top[["last", "decade", "n", "j1", "ratio"]].round(3).values.tolist())
    ok("R2 ruled out: the blood groups net of their errors, from typed patients older than rule A's links",
       not inside(figs["marker"]["A"]["net"], BAND["R2_rule_a_false"]), figs["marker"]["A"]["net"])
    ia, ib = links["D"]
    forms = A.NameForms(eq)
    fn, ln = R["first"].to_numpy(), R["last"].to_numpy()
    comp = np.array([forms.compatible(fn[x], ln[x], fn[y], ln[y]) for x, y in zip(ia, ib)], bool)
    ev = A.two_people(R, F, ia, ib)
    inc = ~comp
    for lab, extra in (("names and the delivery log only", ev["delivery"]), ("names and one visit only", ev["same_visit"])):
        v = int((inc | extra).sum())
        ok("R4 rival inside the band: %s" % lab, inside(v, BAND["R4_rule_d_false"]), v)
    ok("R4 the shortcut outside the band: every link whose names are unalike as typed",
       not inside(figs["rule_d_names_unalike"], BAND["R4_rule_d_false"]), figs["rule_d_names_unalike"])
    mk = figs["marker"]
    ok("R2 ruled out: the blood groups as they read (overlaid records and mislabelled specimens in)",
       not inside(mk["A"]["as_read"], BAND["R2_rule_a_false"]), mk["A"]["as_read"])
    ok("R2 ruled out: the blood groups net of mislabelled specimens, overlaid records left in",
       not inside(mk["A"]["net_of_wbit"], BAND["R2_rule_a_false"]), mk["A"]["net_of_wbit"])
    ok("R2 named data: the overlaid records carry most of rule A's one-patient disagreements",
       mk["A"]["discordant"] - mk["A"]["discordant_clear"] > mk["A"]["expected_one_patient"], mk["A"])
    nz = figs["marker_noise"]
    ok("R2 named data: records typed twice or more disagree with themselves (mislabelled specimens)",
       nz["disagreeing"] >= 5, nz)
    ok("R3 the blood groups see only the twins whose groups differ (rule C net of their errors under half the golden)",
       mk["C"]["net"] < 0.5 * figs["rule_false"]["C"], (mk["C"]["net"], figs["rule_false"]["C"]))
    by = figs["marker_a_birth_year"]
    ok("R2 named data: the typed links behind the blood groups' check are older than rule A's links (a selected sample)",
       by["typed"] <= by["all"] - 15, by)
    import writeup as WU
    lo_, hi_ = WU.poisson_net(mk["A"], figs["marker_noise"]["p_diff"])
    ok("R2 the blood groups' interval holds the golden's rule A estimate", lo_ <= figs["R2_rule_a_false"] <= hi_,
       (round(lo_), round(hi_)))
    ok("R2 ruled out: the engine's chance rates and the records' per-field rates",
       not inside(figs["indep_vendor"], BAND["R2_rule_a_false"]) and not inside(figs["indep_local"],
                                                                                BAND["R2_rule_a_false"]),
       (figs["indep_vendor"], figs["indep_local"]))
    ok("R4 the careful pass's names-only count inside the band (a result careful runs land)",
       inside(figs["careful_rule_false"]["D"], BAND["R4_rule_d_false"]), figs["careful_rule_false"]["D"])
    ok("rule B's band holds the golden and the truth, all under its line; the mismatches scaled as a sample outside it",
       figs["rule_b_band"][0] <= min(figs["rule_false"]["B"], truth["B"]) and
       max(figs["rule_false"]["B"], truth["B"]) <= figs["rule_b_band"][1] < figs["rule_links"]["B"] / 2000 and
       not inside(mk["B"]["net"], figs["rule_b_band"]), (figs["rule_false"]["B"], mk["B"]["net"], truth["B"], figs["rule_b_band"]))
    for nc, ev, label in (("forms", True, "the looser name forms (Jaro-Winkler 0.85, a typed slip, swapped order)"),
                          ("equiv", False, "the names alone, no clinical evidence")):
        n_ov = A.overlays(F, eq, "golden", namecheck=nc, evidence=ev)[0]
        ok("R5 rival inside the band: %s" % label, inside(n_ov, BAND["R5_overlays"]), n_ov)
    ok("R5 ruled out: every automatic merge whose names differ as typed", not inside(figs["overlays_as_typed"],
                                                                                    BAND["R5_overlays"]),
       figs["overlays_as_typed"])
    ok("SF12: the patients an overlay hides are fewer than R1's band half-width",
       figs["R5_overlays"] < 0.015 * figs["R1_index"]["distinct patients"], figs["R5_overlays"])
    if not fast:
        n_ov, hit, per = A.overlays(F, eq, "golden")
        Rx, must, cannot = A.with_retired(F, R, per)
        voc2 = A.Vocab(Rx["first"].tolist())
        for th in (0.3, 0.7):
            root, info = A.link_index(Rx, F, eq, voc2, threshold=th, must=must, cannot_extra=cannot)
            fg = A.index_figures(Rx, root, links["B"])
            ok("R1 rival inside the band: the linkage at a match probability of %.1f" % th,
               inside(fg["persons"], b1["distinct patients"]) and inside(fg["both"], b1["patients in both indexes"]),
               (fg["persons"], fg["both"]))
            ok("R6 rival inside the band: the linkage at a match probability of %.1f" % th,
               inside(fg["left"], BAND["R7_left_after_rule"]), fg["left"])
            fc = float(A.false_links(root[:len(R)], info["apart"], *links["C"]).sum())
            ok("R3 rival inside the band: the linkage at a match probability of %.1f" % th,
               inside(fc, BAND["R3_rule_c_false"]), fc)
        for fw, lab in ((31.0, "automatic"), (19.0, "review")):
            root, info = A.link_index(Rx, F, eq, voc2, must=must, cannot_extra=cannot, fixed_weight=fw)
            fg = A.index_figures(Rx, root, links["B"])
            ok("R1 rival inside the band: the specification's fixed weights at its %s cut-off" % lab,
               inside(fg["persons"], b1["distinct patients"]) and inside(fg["both"], b1["patients in both indexes"]),
               (fg["persons"], fg["both"]))
            ok("R7 rival inside the band: the specification's fixed weights at its %s cut-off" % lab,
               inside(fg["left"], BAND["R7_left_after_rule"]), fg["left"])

    # ---------------------------------------------------------------- the forks, as filed
    pol = pdftext(os.path.join(target, PK.FILES["policy"]))
    plan = pdftext(os.path.join(target, PK.FILES["plan"]))
    spec = pdftext(os.path.join(target, PK.FILES["spec"]))
    norm = lambda t: re.sub(r"\s+", " ", t)
    for sent in re.split(r"(?<=\.) ", DC.POLICY_DEFS):
        ok("SF1 to SF3, SF14, SF15: the policy files \"%s\"" % sent[:48], norm(sent) in pol)
    ok("SF2, SF8, SF10: the policy files the cap and its choice", norm(DC.POLICY_LINK) in pol)
    for k, v in DC.RULES.items():
        ok("SF7: the plan files rule %s as written" % k, norm(v) in plan)
    ok("SF4, SF5: the plan files the pairs and the baseline", norm(DC.PLAN_SCOPE) in plan)
    ok("SF6: the specification files the standardization", "unit" in spec.lower() and "hyphen" in spec.lower())
    ok("the specification's chance rate is the engine's own (about one in 10 billion)", "10 billion" in spec)
    for w in ("twin", "1 January", "subscriber", "dependent", "overlay"):
        ok("nothing filed names a trap: no document says '%s'" % w,
           w.lower() not in (spec + " " + plan).lower() or w == "overlay", w)
    ok("the policy defines an overlay but never says where one comes from", "2019" not in pol and "automatic merge"
       not in pol.lower())

    allv = []
    for x in figs["family"]:
        f_ = dict(figs["rule_false"])
        f_[x["member"]] = x["value"]
        allv.append({k: 2000.0 * f_[k] / figs["rule_links"][k] for k in A.RULES})
    ok("SF9 expected false merges: no rival puts rule B over 0.5 per 2,000 or rule A, C or D under 1.3",
       all(v["B"] <= 0.5 and min(v["A"], v["C"], v["D"]) >= 1.3 for v in allv),
       [{k: round(x, 2) for k, x in v.items()} for v in allv][:3])
    ok("SF11 twins are two patients: the policy's false merge is a link between two different patients' records",
       "two different patients" in pol)
    ok("SF13 patients both indexes hold: the golden's figure counts patients with records in both systems, within the "
       "band of the truth", inside(both_t, b1["patients in both indexes"]) and figs["R1_index"]["patients in both indexes"]
       < figs["R1_index"]["distinct patients"], (figs["R1_index"]["patients in both indexes"], both_t))
    ok("SF16 per 2,000 links: each rate is 2,000 times the false merges over the rule's automatic links",
       all(abs(figs["rule_rate_per_2000"][k] - round(2000.0 * figs["rule_false"][k] / figs["rule_links"][k], 2)) < 0.011
           for k in A.RULES))

    ok("SF17 a link touching an overlay is judged on the patient the record was registered for, the overlay split first",
       "registered for that patient" in pol and "split before the conversion" in norm(pol) and
       figs["R8_rule_b_false"] <= figs["resolve_b"]["left"] + doc["B"]["documented_twins"] + 1, figs["resolve_b"])
    bb = F["blood"]
    fin = A.survivors(F)
    typed_mrn = {fin(x) if x.startswith("CB") else x for x in bb["MRN"]}
    age = (pd.Timestamp("2026-11-02") - R["dob"]).dt.days / 365.25
    over55 = float((age[R["mrn"].isin(typed_mrn)] > 55).mean())
    ok("SF18 rule B's mismatches counted as found: the typed records are a selected sample (most over 55), and the "
       "mismatches scaled as a sample fall outside R8's band", over55 > 0.6 and not inside(mk["B"]["net"], BAND["R8_rule_b_false"]),
       (round(over55, 3), mk["B"]["net"]))
    ovl = A.overlay_links(R, links["B"], set(figs["R9_overlay_links"] and A.overlays(F, eq, "golden")[1]))
    ok("SF19 the recommended rule's links touching an overlay, each pair once, and the distinct records they touch",
       ovl == {"links": figs["R9_overlay_links"]["links"], "records": figs["R9_overlay_links"]["records split"]}, ovl)
    first_birth = pd.to_datetime(F["deliveries"]["DELIVERY_DTTM"]).min()
    ok("SF20 the confirming files test what they cover: the delivery log starts in 2006, and its documented twins fall "
       "short of rule C's golden", first_birth.year >= 2006 and doc["C"]["documented_twins"] < figs["rule_false"]["C"],
       (str(first_birth.date()), doc["C"]["documented_twins"], figs["rule_false"]["C"]))

    # ---------------------------------------------------------------- the routine factors decide nothing
    ok("routine: the SSN read correctly still leaves rule D over the cap on names alone",
       figs["careful_rule_false"]["D"] > figs["rule_links"]["D"] / 2000, figs["careful_rule_false"]["D"])
    ok("routine: the golden route never reads the mislabelled-specimen rate (rule A from the joint cells)",
       abs(figs["rule_false"]["A"] - figs["R2_rule_a_false"]) < 0.05)

    # ---------------------------------------------------------------- input gates
    files = sorted(os.listdir(target))
    ok("gate: ten or more usable files", len(files) >= 10, len(files))
    cats = {os.path.splitext(f)[1] for f in files}
    ok("gate: two or more file categories", len(cats & {".csv", ".xlsx", ".pdf"}) >= 2, sorted(cats))
    big = {f: sum(1 for _ in open(os.path.join(target, f))) for f in files if f.endswith(".csv")}
    ok("gate: a CSV of 20,000 rows or more", max(big.values()) >= 20000, max(big.values()))
    ok("gate: a second large CSV (ten or more printed pages)", sorted(big.values())[-2] >= 600, sorted(big.values())[-2])
    md = json.load(open(os.path.join(TASK, "metadata.json")))
    ok("gate: two or more distractors named in metadata.json", len(md["distractor_files"]) >= 2, md["distractor_files"])
    loader = open(os.path.join(HERE, "golden.py")).read() + open(os.path.join(HERE, "analysis.py")).read()
    ok("gate: the golden never reads a distractor", all('"%s"' % k not in loader for k in PK.DISTRACTORS))
    ok("gate: no file name says distractor, answer or trap",
       not any(re.search(r"distract|answer|trap|truth", f, re.I) for f in files))
    ok("gate: no readme, dictionary or manifest ships",
       not any(re.search(r"readme|dictionary|manifest|notes", f, re.I) for f in files))
    ok("gate: metadata names the public surname source and its license",
       any("Census" in s.get("name", "") and "public domain" in s.get("license", "") for s in md.get("public_inputs", [])))
    heads = []
    for name in files:
        p = os.path.join(target, name)
        if name.endswith(".csv"):
            heads += list(pd.read_csv(p, nrows=2, dtype=str).columns)
        elif name.endswith(".xlsx"):
            for sh, df in pd.read_excel(p, sheet_name=None, nrows=4, header=None).items():
                heads += [str(c) for c in df.astype(str).values.ravel()]
    bad = [h for h in heads if re.search(r"false.?merge|twin|overlay|chance|true.?match|same.?person|pid", str(h), re.I)]
    ok("gate: no shipped column or header holds a result or the truth", not bad, bad[:5])

    # ---------------------------------------------------------------- realism sweep
    for k in ("index_a", "index_b"):
        col = "MRN" if k == "index_a" else "PATIENT_ID"
        ids = F[k][col].str.replace(r"\D", "", regex=True).astype(int).sort_values().to_numpy()
        ok("realism: %s identifiers rise with registration and skip the numbers merged or voided" % k,
           len(set(np.diff(ids))) > 3 and (ids == np.sort(ids)).all(), sorted(set(np.diff(ids)))[:6])
    ok("realism: first names take thousands of forms", R["first"].nunique() > 4000, R["first"].nunique())
    census = set()
    for fname in ("census1990_first_female.txt", "census1990_first_male.txt"):
        census |= {ln.split()[0] for ln in open(os.path.join(HERE, fname)) if ln.strip()}
    vc = R["first"].value_counts()
    rare = [n for n in vc[vc <= 2].index if n in census]
    ok("realism: a thousand or more rare first names are real names, not typing slips", len(rare) >= 1000, len(rare))
    ok("realism: surnames take thousands of forms", R["last"].nunique() > 5000, R["last"].nunique())
    jan1 = (R["dob"].dt.strftime("%m%d") == "0101").mean()
    ok("realism: 1 January birth dates between 1 and 6 per cent of records", 0.01 < jan1 < 0.06, round(jan1, 4))
    for k in ("spec", "policy", "plan"):
        meta = subprocess.run(["pdfinfo", os.path.join(target, PK.FILES[k])], capture_output=True, text=True).stdout
        ok("realism: %s PDF made by Writer, authored by its issuer" % k,
           "Writer" in meta and "LibreOffice" in meta and "Author:" in meta, re.findall(r"Author:\s*(.*)", meta)[:1])
    em = [f for f in files if f.endswith(".csv") and "\u2014" in open(os.path.join(target, f)).read()]
    ok("realism: no em dash in any shipped text", not em, em)
    asof = dt.datetime(2026, 11, 4).timestamp()
    late = [f for f in files if os.path.getmtime(os.path.join(target, f)) >= asof]
    ok("realism: every pack file saved before the as-of date", not late, late)
    gold = os.path.join(TASK, "golden")
    gfiles = sorted(os.listdir(gold))
    ok("golden: exactly the requested files (a spreadsheet and a memo)", gfiles == sorted([DL.WORKBOOK, DL.MEMO]), gfiles)

    # ---------------------------------------------------------------- prompt ties
    prompt = open(os.path.join(TASK, "prompt.txt")).read()
    ok("prompt: the conversion date is the plan's", "5 April 2027" in prompt)
    ok("prompt: the cap is the policy's (one false merge per 2,000 automatic links)",
       "one false merge per 2,000 automatic links" in prompt and "2,000 automatic links" in DC.POLICY_LINK)
    ok("prompt: names no shipped file", not any(os.path.splitext(f)[0].replace("_", " ") in prompt for f in files))
    ok("prompt: no count the data hold (no four rules)", not re.search(r"\b(four|4) (candidate )?rules\b", prompt, re.I))
    sub = open(os.path.join(TASK, "submission.md")).read()
    for key, fmt in (("R2_rule_a_false", "%.1f"), ("R3_rule_c_false", "{:,}"), ("R4_rule_d_false", "{:,}"),
                     ("R5_overlays", "{:,}"), ("R7_left_after_rule", "{:,}")):
        v = figs[key]
        s = (fmt % v) if fmt.startswith("%") else fmt.format(v)
        ok("submission states %s (%s)" % (key, s), s in sub)
    for k, v in figs["R1_index"].items():
        ok("submission states %s (%s)" % (k, "{:,}".format(v)), "{:,}".format(v) in sub)
    print("\n%d checks, %d FAIL" % (N[0], N[1]))
    return 1 if N[1] else 0


if __name__ == "__main__":
    sys.exit(main(fast="--fast" in sys.argv))
