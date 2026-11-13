"""the world's own 2027-28 under the policy's stress: the calls of the commitments made by the end of 2026 per quarter,
split between the funds that have held a first close and those yet to, and each 2027 re-up's own calls (not graded;
checks the golden)."""
import numpy as np, world as Wd, pack as PK
from world import H_END, W


def truth():
    Wo = PK.build_world(); E, S, R = Wd.stressed(Wo["E"], Wo["S"], Wo["R"])
    p = Wd.propensity(E)
    out = {k: np.zeros(Wd.NQ) for k in ("call_inv", "call_pend", "dist", "line")}
    plan = {}
    for f in Wo["funds"]:
        if f["C"] <= 0:
            continue
        fc = f["fc"] if (f["fc"] <= H_END and f["vint"] <= 2026) else f["exp_fc"] + Wd.slip_of(f, E)
        o = Wd.run_fund(dict(f), E, S, R, p, fc)
        calls = o["call_inv"] + o["call_fee"] + o["call_exp"]
        calls[fc + Wd.ST[f["gp"]["st"]]["life"] + 1:] = 0.0        # the commitment not called at the term's end is released
        if f["vint"] == 2027:
            plan[f["name"]] = float(calls[W].sum())
            continue
        key = "call_pend" if f["fc"] > H_END else "call_inv"
        out[key] += calls; out["dist"] += o["dist"]
        if f["fc"] <= H_END:
            out["line"][H_END] += o["line"][H_END]
    return out, plan


if __name__ == "__main__":
    o, plan = truth()
    hv = lambda v: [round(float(v[W[i:i + 2]].sum()), 1) for i in (0, 2, 4, 6)]
    print("closed", hv(o["call_inv"]), "pending", hv(o["call_pend"]), "line stock %.1f" % o["line"][H_END])
    print("re-ups", {k: round(v, 1) for k, v in plan.items()})
