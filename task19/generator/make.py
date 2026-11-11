"""task19 build: the simulated population, the pack under target/, the golden analysis, figures.json, effort.json,
the golden workbook and note, submission.md and metadata.json.

    python3 make.py --full     builds everything in place
    python3 make.py            builds the pack alone (target/)
    python3 make.py --twice    builds twice into scratch folders and fails unless target/ and golden/ are byte-identical
"""
import filecmp
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
os.environ.setdefault("OMP_NUM_THREADS", "1")

import pack as PK  # noqa: E402
import params as PR  # noqa: E402
import records as RC  # noqa: E402
import sample as SM  # noqa: E402
import world as WD  # noqa: E402


def world():
    W = WD.build()
    SM.build(W, seed=PR.SAMPLE_SEED)
    RC.person_open_index(W)
    RC.citizenship(W)
    RC.build(W)
    RC.build_other(W)
    return W


def build_pack(task_dir):
    target = os.path.join(task_dir, "target")
    if os.path.isdir(target):
        shutil.rmtree(target)
    W = world()
    counts = PK.write(W, target)
    return W, counts


def build(task_dir, gen_out):
    import analysis as AN
    import deliver as DV
    import metadata as MD
    import results as RS
    import writeup as WU
    W, counts = build_pack(task_dir)
    target = os.path.join(task_dir, "target")
    cache = os.environ.get("T19_ANALYSIS_CACHE")
    if cache and os.path.exists(cache) and os.environ.get("T19_REUSE_ANALYSIS"):
        import pickle
        res = pickle.load(open(cache, "rb"))
    else:
        res = AN.compute(target)
        if cache:
            import pickle
            keep = {k: v for k, v in res.items() if k not in ("prep", "golden_raw", "careful_raw")}
            pickle.dump(keep, open(cache, "wb"))
    F, E = RS.write(res, gen_out)
    gold = os.path.join(task_dir, "golden")
    if os.path.isdir(gold):
        shutil.rmtree(gold)
    DV.write(F, gold)
    WU.write(F, os.path.join(task_dir, "submission.md"), DV.WORKBOOK, DV.NOTE)
    json.dump(MD.metadata(target, counts), open(os.path.join(task_dir, "metadata.json"), "w"), indent=1)
    # the clean truth beside the build, for checks.py (never shipped)
    truth = {"national": int(W["truth"]["national"]), "district": [int(x) for x in W["truth"]["district"]],
             "official_2026": int(W["official_2026"]), "audit": audit(W)}
    json.dump(truth, open(os.path.join(gen_out, "truth.json"), "w"), indent=1)
    return W, res, F, E


def audit(W):
    """Process footprints in the clean truth, by district, for checks.py: each factor the results need shows across
    the districts the way its process puts it there."""
    import numpy as np
    P, R = W["P"], W["R"]
    res = np.where(P.view("status") == 0)[0]
    age = WD.ages_at(P.view("dob")[res], PR.REF)
    d = P.view("dist")[res].astype(int)
    og = P.view("offgrid")[res] & (age >= 18) & (age <= 44)
    o = W["rec_open"]
    cls = W["rec_class"]
    rd = R.dist[o].astype(int)
    pid = R.pid[o]
    cur_d = np.full(P.n, -1)
    cur_d[pid[cls == 0]] = rd[cls == 0]
    listed_else = np.zeros(WD.ND, int)
    on_none = np.zeros(WD.ND, int)
    anyrec = np.zeros(P.n, bool)
    anyrec[pid] = True
    for p_, dd in zip(res, d):
        if P.forces[p_]:
            continue
        if cur_d[p_] == dd:
            continue
        if anyrec[p_]:
            listed_else[dd] += 1
        else:
            on_none[dd] += 1
    return {"offgrid_men_18_44": np.bincount(d[og], minlength=WD.ND).tolist(),
            "students": np.bincount(d[P.view("student")[res]], minlength=WD.ND).tolist(),
            "records_left_or_died": np.bincount(rd[np.isin(cls, [3, 4])], minlength=WD.ND).tolist(),
            "records_duplicate": np.bincount(rd[cls == 1], minlength=WD.ND).tolist(),
            "records_elsewhere": np.bincount(rd[cls == 2], minlength=WD.ND).tolist(),
            "residents_listed_elsewhere": listed_else.tolist(), "residents_on_no_list": on_none.tolist(),
            "emigrants_unrecorded": int(((P.view("status") == 1) & ~P.view("emig_rec")).sum()),
            "emigrants": int((P.view("status") == 1).sum()),
            "forces": int((P.view("forces") & (P.view("status") == 0)).sum())}


def same_tree(a, b):
    for root, _, files in os.walk(a):
        for f in files:
            pa = os.path.join(root, f)
            pb = os.path.join(b, os.path.relpath(pa, a))
            if not os.path.exists(pb) or not filecmp.cmp(pa, pb, shallow=False):
                return False, os.path.relpath(pa, a)
    return True, ""


if __name__ == "__main__":
    if "--twice" in sys.argv:
        outs = []
        for k in range(2):
            d = tempfile.mkdtemp(prefix="task19-build%d-" % k)
            os.makedirs(os.path.join(d, "generator"))
            build(d, os.path.join(d, "generator"))
            outs.append(d)
        ok = True
        for sub in ("target", "golden"):
            same, which = same_tree(os.path.join(outs[0], sub), os.path.join(outs[1], sub))
            print("%s byte-identical: %s %s" % (sub, same, which))
            ok = ok and same
        for f in ("generator/figures.json", "generator/effort.json", "submission.md", "metadata.json"):
            same = filecmp.cmp(os.path.join(outs[0], f), os.path.join(outs[1], f), shallow=False)
            print("%s byte-identical: %s" % (f, same))
            ok = ok and same
        for d in outs:
            shutil.rmtree(d, ignore_errors=True)
        sys.exit(0 if ok else 1)
    if "--full" in sys.argv:
        build(TASK, HERE)
        print("built", TASK)
    else:
        W, counts = build_pack(TASK)
        print(json.dumps(counts, indent=1))
