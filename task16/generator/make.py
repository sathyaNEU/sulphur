"""task16 build: the simulated patient population and its registrations at Calder Bay and Rosario, the pack under
target/, the golden analysis read back from the pack, figures.json and effort.json, the golden workbook and memo,
submission.md and metadata.json.

    python3 make.py            builds in place
"""
import json
import os
import shutil
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import warnings  # noqa: E402

warnings.filterwarnings("ignore")
import analysis as A  # noqa: E402
import deliver as DL  # noqa: E402
import forcing as FO  # noqa: E402
import golden as GD  # noqa: E402
import metadata as MD  # noqa: E402
import pack as PK  # noqa: E402
import records as RC  # noqa: E402
import results as RS  # noqa: E402
import world as WD  # noqa: E402
import writeup as WU  # noqa: E402


def typed_years(F, R, link):
    """The mean birth year of rule A's linked records, all of them and those whose two records both carry blood bank
    results: the blood groups' cross-check sees an older population than the rule."""
    ia, ib = link
    typ = A.typings(F)
    m, yr = R["mrn"].to_numpy(), R["dob"].dt.year.to_numpy()
    typed = np.array([bool(typ.get(m[x])) and bool(typ.get(m[y])) for x, y in zip(ia, ib)], bool)
    a, t = float(yr[ia].mean()), float(yr[ia[typed]].mean())
    return {"all": round(a, 1), "typed": round(t, 1), "years_older": int(round(a - t))}


def build(task_dir, gen_out):
    target = os.path.join(task_dir, "target")
    gold = os.path.join(task_dir, "golden")
    for d in (target, gold):
        if os.path.isdir(d):
            shutil.rmtree(d)
    W = WD.build()
    F0 = RC.frames(W)
    counts = PK.write(F0, target)
    F = GD.load(target)
    S = RS.setup(F)
    G = RS.golden(F, S)
    C = RS.careful(F, S)
    Q = RS.quick(F, S)
    fo = FO.run(F, G, C, S)
    R, eq, voc, links = S
    root = G["_root"][:len(R)]
    dup = {}
    for s_ in ("A", "B"):
        sel = (R["sys"] == s_).to_numpy()
        dup[s_] = round(100.0 * (sel.sum() - len(set(root[sel]))) / sel.sum(), 1)
    ia, ib = links["D"]
    unalike = int((voc.jw(voc.code(R["first"].iloc[ia]), voc.code(R["first"].iloc[ib])) < 0.88).sum())
    forms = A.NameForms(eq)
    fn, ln = R["first"].to_numpy(), R["last"].to_numpy()
    comp = np.array([forms.compatible(fn[x], ln[x], fn[y], ln[y]) for x, y in zip(ia, ib)], bool)
    ev = A.two_people(R, F, ia, ib)
    sim_twins = int((comp & (ev["same_visit"] | ev["delivery"])).sum())
    extra = dict(routes=[dict(name=r["name"], answer=r["answer"], **({"golden": True} if r["golden"] else {}))
                         for r in fo["routes"]],
                 hints=fo["hints"], forcing=fo["forcing"],
                 figures=dict(active_records=int(len(R)), overlays_as_typed=int(A.overlays(F, eq, "raw")[0]),
                              overlays_forms=int(A.overlays(F, eq, "golden", namecheck="forms")[0]),
                              duplicate_share=dup, rule_d_names_unalike=unalike,
                              rule_d_similar_named_twins=sim_twins,
                              rule_a_shares={k: round(v, 3) for k, v in DL.community_shares(F, R).items()},
                              marker_a_birth_year=typed_years(F, R, links["A"]),
                              cited_sections={"plan": 7.2, "policy": 3},
                              routes={r["name"]: r["answer"] for r in fo["routes"]},
                              golden_family={x["name"]: x["answer"] for x in fo["forcing"]["golden_family"]},
                              perturbations={x["input"]: x["answer"] for x in fo["forcing"]["perturbations"]}))
    figs, E = RS.write(F, gen_out, G, C, Q, extra)
    figs.update(WU.derived(figs, fo))
    json.dump(figs, open(os.path.join(gen_out, "figures.json"), "w"), indent=1, sort_keys=True, default=RS._plain)
    DL.write(F, G, figs, gold)
    WU.write(figs, G, fo, os.path.join(task_dir, "submission.md"))
    json.dump(MD.metadata(target, counts), open(os.path.join(task_dir, "metadata.json"), "w"), indent=1)
    return W, F, G, C, Q, fo, figs, E


if __name__ == "__main__":
    build(TASK, HERE)
    print("built", TASK)
