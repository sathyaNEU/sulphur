"""the world's own 2027-28 under the policy's stress: the calls of the commitments made by the end of 2026 per quarter,
split between the funds that have held a first close and those yet to, the refinancing calls, and each 2027 re-up's own
calls (not graded; anchors the golden's estimates: the facility balances, the refinancing calls, the re-ups). The world
runs as its managers would (first closes slipping, proceeds reinvested); the policy's test fixes those on set bases, so
the totals are not compared, only what the golden estimates. policy=True holds the deal market at its normal pace."""
import numpy as np, world as Wd, pack as PK
from world import H_END, W


def truth(policy=True):
    old = Wd.P.get("policy_pace"); Wd.P["policy_pace"] = policy
    Wo = PK.build_world(); E, S, R = Wd.stressed(Wo["E"], Wo["S"], Wo["R"])
    p = Wd.propensity(E)
    out = {k: np.zeros(Wd.NQ) for k in ("call_inv", "call_pend", "dist", "line", "refi")}
    plan = {}; due = []
    for f in Wo["funds"]:
        if f["C"] <= 0:
            continue
        fc = f["fc"] if (f["fc"] <= H_END and f["vint"] <= 2026) else f["exp_fc"] + Wd.slip_of(f, E)
        log = []
        o = Wd.run_fund(dict(f), E, S, R, p, fc, succ_fc=PK.succ_fc(f, E), refi_log=log)
        calls = o["call_inv"] + o["call_fee"] + o["call_exp"]
        calls[fc + Wd.ST[f["gp"]["st"]]["life"] + 1:] = 0.0        # the commitment not called at the term's end is released
        if f["vint"] == 2027:
            plan[f["name"]] = float(calls[W].sum())
            continue
        key = "call_pend" if f["fc"] > H_END else "call_inv"
        out[key] += calls; out["dist"] += o["dist"]; out["refi"] += o["refi"]
        if f["fc"] <= H_END:
            out["line"][H_END] += o["line"][H_END]
            due += [(f["id"], x) for x in log if x[0] in W]
    if old is None: Wd.P.pop("policy_pace", None)
    else: Wd.P["policy_pace"] = old
    out["due"] = due
    return out, plan


if __name__ == "__main__":
    for pol in (True, False):
        o, plan = truth(pol)
        hv = lambda v: [round(float(v[W[i:i + 2]].sum()), 1) for i in (0, 2, 4, 6)]
        print("policy" if pol else "world", "closed", hv(o["call_inv"]), "pending", hv(o["call_pend"]), "refi", hv(o["refi"]), "line stock %.1f" % o["line"][H_END])
        print("re-ups", {k: round(v, 1) for k, v in plan.items()})
