"""gate (k): the five pack conventions re-measured on the new cut put in place of core's PACK_SHIFTS (in this
process only, core.py untouched), pack_table re-run, and the truth anchor"""
import os as _os
_GEN = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), ".."))
_TGT = _os.path.normpath(_os.path.join(_GEN, "..", "target"))
import sys, json
sys.path.insert(0, _GEN)
import core as C
fig = json.load(open(sys.argv[1]))
new = fig["pack_shifts"]
names = [n for n in C.PACK_SHIFTS]
assert set(new) == set(names), (sorted(new), names)
print("PACK_SHIFTS, core (last cut) against this cut:")
for n in names:
    keys = sorted(set(C.PACK_SHIFTS[n]) | set(new[n]))
    print(" ", n)
    for k in keys:
        print("     %-40s core %+.4f  cut %+.4f" % (k, C.PACK_SHIFTS[n].get(k, 0.0), new[n].get(k, 0.0)))
for n in names:
    C.PACK_SHIFTS[n] = dict(new[n])
spec, Xs = C.build_spec(verbose=True)
C.pack_table(spec)
print("anchor:")
for fid, a in spec["anchor"].items():
    print("  %-40s %12.3f %12.3f %+.3f %.3f %s" % (fid, a["golden"], a["world"], a["gap"], a["tolerance"],
                                                   "inside" if abs(a["gap"]) <= a["tolerance"] else "OUTSIDE"))
mi = [f for f in spec["figures"] if f["id"] == "return Meta iOS"][0]
print("Meta iOS return range", mi["band"], "with the pack in", spec["pack"]["bands"]["return Meta iOS"])
