"""the world's own 2027-28 under the policy's stress: calls by group per quarter (not graded; checks the golden)."""
import numpy as np, world as Wd, pack as PK
from world import H_END, W
def truth(budget=500.0):
    Wo = PK.build_world(); E, S, R = Wd.stressed(Wo["E"], Wo["S"], Wo["R"])
    p = Wd.propensity(E)
    out = {k: np.zeros(Wd.NQ) for k in ("call_inv", "call_pend", "call_plan", "support", "dist")}
    plan_tot = sum(f["C"] for f in Wo["funds"] if f["vint"] == 2027)
    for f in Wo["funds"]:
        g = dict(f)
        if f["vint"] == 2027:
            g["C"] = f["C"] * budget / plan_tot; g["size"] = f["size"]
            key = "call_plan"
        elif f["fc"] > H_END:
            key = "call_pend"
        else:
            key = "call_inv"
        fc = f["fc"] if (f["fc"] <= H_END and f["vint"] <= 2026) else f["exp_fc"] + Wd.slip_of(f, E)
        if g["C"] <= 0: continue
        log = []
        o = Wd.run_fund(g, E, S, R, p, fc, deal_log=log)
        for q in W:
            out[key][q] += o["call_inv"][q] + o["call_fee"][q] + o["call_exp"][q]; out["dist"][q] += o["dist"][q]
    return out
if __name__ == "__main__":
    import sys
    for b in (0.0, 500.0):
        o = truth(b)
        print("budget %4.0f  existing %.1f  pending %.1f  plan %.1f  dist(world) %.1f" % (b, o["call_inv"][W].sum(), o["call_pend"][W].sum(), o["call_plan"][W].sum(), o["dist"][W].sum()))
        print("   by half: existing", [round(o["call_inv"][W[i:i+2]].sum(), 1) for i in (0, 2, 4, 6)], "pending", [round(o["call_pend"][W[i:i+2]].sum(), 1) for i in (0, 2, 4, 6)])
