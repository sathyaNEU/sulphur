import os  # noqa: E402
# numpy runs on Apple's Accelerate here, whose threads do not survive a fork: one thread, set before numpy loads
for _v in ("VECLIB_MAXIMUM_THREADS", "OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
"""gate (k)'s difference: the figures the S2-lost route earns on core's bound ranges (pack_band with the shifts
re-measured on this cut) and not on the cut's exact crossed ranges, with the reach of every way on the cut"""
import json
import sys
_GEN = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, _GEN)
import core as C  # noqa: E402
import corelib as L  # noqa: E402,F401
fig = json.load(open(sys.argv[1]))
for n in C.PACK_SHIFTS:
    C.PACK_SHIFTS[n] = dict(fig["pack_shifts"][n])
spec = C.build_spec()
import copy
fv = spec["rungs"]["lattice"]["S2"]
def earned(sp):
    figs, _p = L._figures(sp, {})
    return {f["id"]: f for f in figs if L._earned(f, fv[C.stated_id(f["id"])])}
sb, se = copy.deepcopy(spec), copy.deepcopy(spec)
for f in sb["figures"]:
    f["band"] = list(spec["pack"]["bands"][C.stated_id(f["id"])])
for f in se["figures"]:
    f["band"] = list(fig["figure_band"][C.stated_id(f["id"])])
a, b, e = earned(spec), earned(sb), earned(se)
print("S2 lost on base: core's stated %s, core's bound %s, the cut's exact %s" % tuple(
    "%.1f" % C.price_routes(x, {"S2": fv})["S2"][0] for x in (spec, sb, se)))
for fid in sorted(set(b) - set(e)):
    sid = C.stated_id(fid)
    print("earned on the bound, not on the cut: %-48s value %.4f  bound %s  exact %s  widened by the cut: %s" % (
        fid, fv[sid], spec["pack"]["bands"][sid], fig["figure_band"][sid], sid in fig["pack_widened"]))
best = max(fig["rubric"]["runs"].items(), key=lambda kv: kv[1] or -1)
print("runs_max on the cut:", best)
