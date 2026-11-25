"""A thin seed sweep for architecture 8's world (generator/common.py's settings): for each seed the pack is cut into a
scratch folder and the golden run on it, and one JSON line is printed with the golden list and SLIs, the list each of
the lattice's seven routes files (the three judgments made the hurried way alone, in pairs and together), the split
family's spread on every bridged SLI and whether every split, interpolation and bound keeps the golden list. A seed
takes about two minutes; the world's dials are not searched here, only its draw.

    python3 seed_sweep.py 2700 2710 > sweep.jsonl"""
import json
import os
import shutil
import sys
import tempfile
import warnings

for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import analysis as AN   # noqa: E402
import common as K      # noqa: E402
import pack as PK       # noqa: E402
import world as W       # noqa: E402

GOLD = ["fares", "places", "seat-map", "partner-gateway", "notifications"]


def one(seed):
    out = tempfile.mkdtemp(prefix="task6_seed%d_" % seed)
    try:
        PK.write_pack(out, W.World(seed=seed))
        g = AN.Golden(out)
        R = g.run()
    finally:
        shutil.rmtree(out, ignore_errors=True)
    bud = R["bud"]
    over_raw = lambda S: [s for s in K.SVC if S[s]["sli"] > bud[s]]
    fam = R["family"]
    bridged = [s for s in K.SVC if R["bucket"][s] is not None]
    return {"seed": seed,
            "golden": R["P"]["over"], "golden_is_design": R["P"]["over"] == GOLD,
            "sli": {s: round(R["S"][s]["sli"], 3) for s in K.SVC},
            "attribution": R["attribution"],
            "lattice": {k: v["P"]["over"] for k, v in R["lattice"].items()},
            "family_spread": {s: [round(min(f[s]["sli"] for f in fam.values()), 3),
                                  round(max(f[s]["sli"] for f in fam.values()), 3)] for s in bridged},
            "family_one_list": len({tuple(over_raw(f)) for f in fam.values()}) == 1,
            "naive_lists": {k: over_raw(v) for k, v in R["naive"].items()},
            "ci": {s: [round(R["ci"][s][0], 2), round(R["ci"][s][1], 2)] for s in R["P"]["over"]}}


if __name__ == "__main__":
    a, b = int(sys.argv[1]), int(sys.argv[2])
    for seed in range(a, b):
        print(json.dumps(one(seed), sort_keys=True))
        sys.stdout.flush()
