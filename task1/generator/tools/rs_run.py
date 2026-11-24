import os as _os
_GEN = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), ".."))
_TGT = _os.path.normpath(_os.path.join(_GEN, "..", "target"))
import sys, json, time, pickle
sys.path.insert(0, _GEN)
import results as RS
t=time.time()
X, fig, E, spec = RS.run(_TGT)
print("secs", round(time.time()-t))
json.dump(fig, open(sys.argv[1], "w"), indent=1, default=float)
r=fig["rubric"]; print({k: r[k] for k in ("level","fails","one_lost","fixed_alone","two_lost","reflex","rigorous","runs_max")})
print(json.dumps(fig["crossed"])[:1500]); print(json.dumps(fig["pack_widened"])[:3000]); print(json.dumps(fig["pack_shifts"])[:3000])
for fid in fig["figure"]: print("%-44s %10s  %s" % (fid, fig["figure"][fid], fig["figure_band"][fid]))
