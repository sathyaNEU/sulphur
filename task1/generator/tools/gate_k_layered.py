import os  # noqa: E402
# numpy runs on Apple's Accelerate here, whose threads do not survive a fork: one thread, set before numpy loads
for _v in ("VECLIB_MAXIMUM_THREADS", "OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
"""gate (k) re-read on the cut's measured ranges (the family, its crossings and the layered family): every lattice
route and run route priced on core's stated ranges and on the cut's, four ways (base / band by band / by figure /
both), with the truth anchor and the call on every way"""
import copy
import json
import sys
_GEN = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, _GEN)
import core as C  # noqa: E402
fig = json.load(open(sys.argv[1]))
spec = C.build_spec()
cut = copy.deepcopy(spec)
for f in cut["figures"]:
    f["band"] = list(fig["figure_band"][C.stated_id(f["id"])])
R = spec["rungs"]
named = {"lost " + k: fv for k, fv in R["lattice"].items()}
named.update({"run " + k: fv for k, fv in R["runs"].items()})
a, b = C.price_routes(spec, named), C.price_routes(cut, named)
fmt = lambda r: " / ".join("%.1f" % x for x in r)
print("every route, core's figures on the simulation, on core's stated ranges, then on the cut's measured ranges "
      "(base / band by band / by figure / both):")
for nm in named:
    print("  %-40s %-28s %s" % (nm, fmt(a[nm]), fmt(b[nm])))
print("the cut's own rubric (corelib on the cut pack, base):", json.dumps(fig["rubric"]))
if os.path.exists(sys.argv[1] + ".spec.json"):
    cs = json.load(open(sys.argv[1] + ".spec.json"))
    keys = list(cs["lattice"])
    cn = {}
    for k in keys:
        fv = {}
        for f in cs["figures"]:
            sid = C.stated_id(f["id"])
            if sid.startswith("return "):
                fv[sid] = cs["lattice"][k][sid[len("return "):]]
            elif "lattice" in f:
                fv[sid] = f["lattice"][k]
        cn["lost " + k] = fv
    pc = C.price_routes(cs, cn)
    print("every lattice route, the cut's own figures on the cut's measured ranges (base / band by band / by figure / both):")
    for nm in cn:
        print("  %-40s %s" % (nm, fmt(pc[nm])))
print("calls moved: crossed %s, layered %s; ways %d crossed family, %d layered" % (
    fig["crossed"]["moved"], fig["layered"]["moved"], fig["crossed"]["ways"], fig["layered"]["ways"]))
print("Meta iOS return range on the cut:", fig["figure_band"]["return Meta iOS"])
print("anchor:")
for fid, x in spec["anchor"].items():
    print("  %-40s %12.3f %12.3f %+.3f %.3f %s" % (fid, x["golden"], x["world"], x["gap"], x["tolerance"],
                                                   "inside" if abs(x["gap"]) <= x["tolerance"] else "OUTSIDE"))
