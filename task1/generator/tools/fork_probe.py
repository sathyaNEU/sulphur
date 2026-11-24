import os as _os
_GEN = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), ".."))
_TGT = _os.path.normpath(_os.path.join(_GEN, "..", "target"))
import sys, time
sys.path.insert(0, _GEN)
import analysis as A, core as C
O = A.PackObs(_TGT); A.use_plan(O)
ways = C.crossed_ways(A.SINGLES)[:120]
t = time.time(); f = A.crossed_family(O, ways); print(len(f), round(time.time() - t, 1), "s")
