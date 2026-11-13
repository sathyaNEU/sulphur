"""What the pack shows about the world, as arrays the estimators read (the pack writer prints these; the verifier reads
them back from the files and must reproduce the same figures)."""
import numpy as np

import params as P


class Obs:
    pass


def observe(w, seed=P.SEED + 1):
    rng = np.random.default_rng(seed)
    O = Obs()
    O.T = w.T
    O.trial = list(w.trial)
    O.trial_days = w.trial_days
    O.sub = [f["sub"] for f in w.F]
    O.r = [f["r"] for f in w.F]
    O.L = [f["L"] for f in w.F]
    O.cust = [f["customers"] for f in w.F]
    O.cost = [float(round(f["cost"], -2)) for f in w.F]
    O.kind = [f["kind"] for f in w.F]
    O.midreg = [f["midreg"] for f in w.F]
    # customer meters: each feeder's sum of interval kWh, a little meter error
    O.ami = [w.S[i] * 0.25 * (1 + rng.normal(0, 0.002, P.NQ)) for i in range(P.NF)]
    # substation-end revenue meters on the feeders whose breakers were replaced since 2019
    O.headmetered = sorted(int(x) for x in rng.choice(P.NF, size=11, replace=False))
    O.head = {f: (w.S[f] + w.loss[f]) * 0.25 * (1 + rng.normal(0, 0.001, P.NQ)) for f in O.headmetered}
    # bus SCADA, 15-minute mean volts on the 120 V base; trial feeders read after their pilot regulator
    O.vmin_h_head = [w.Vhead[i] for i in range(P.NF)]
    O.vbus = {s: np.round(v, 2) for s, v in w.vbus.items()}
    # far-end meters: the lowest of each feeder's bellwether meters, hourly minimum
    O.vmin_h = []
    import world as W
    for i, f in enumerate(w.F):
        veol = w.Vhead[i] - W.drop_end(f, w.S[i])
        O.vmin_h.append(np.round(veol.reshape(-1, 4).min(axis=1) + rng.normal(0, 0.15, P.ND * 24), 1))
    # the LTC tap log, at the quarter it happened in
    O.tap_q = {s: [] for s in P.SUBSTATIONS}
    for (s, minute, step, tap) in w.taplog:
        O.tap_q[s].append((minute // 15, step))
    # the trial: assignment and the regulator log's achieved reduction
    O.assign = {f: w.assign[f] for f in w.trial}
    O.dose_q = {f: w.dose[f] for f in w.trial}
    O.dose_daily = {f: w.dose[f].reshape(P.ND, P.Q).mean(axis=1) for f in w.trial}
    # the appliance survey: sampled households per feeder (share holding each appliance)
    O.survey = {}
    for i, f in enumerate(w.F):
        n = int(rng.integers(55, 130))
        O.survey[i] = dict(n=n, **{k: float(rng.binomial(n, f[k])) / n for k in ("sat_res_heat", "sat_hp", "sat_ewh", "sat_ac")})
    return O
