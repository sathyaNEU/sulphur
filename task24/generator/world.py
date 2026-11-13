"""task24 world: Penvale Electronics' 2026 support-reply labelling and Draftline's reward-model runs, simulated item by
item from the processes that write each record (the Tallyfield crowd platform, the Ardentdesk support desk, the
senior technicians' panel, the reward model's learning, Penvale's evaluation pipeline). Nothing here is written to
carry an answer: every graded quantity is computed later from the records this module returns."""
import datetime as dt
import hashlib

import numpy as np
import pandas as pd
from scipy.stats import norm

SEED = 608
PULL = dt.date(2026, 11, 13)

TYPES = ["order_delivery", "returns_refunds", "account_billing", "product_howto", "device_troubleshooting"]
ND = len(TYPES)
# reply length by type (median words, log spread) and the spread of the log length ratio between the two drafts
WORDS = dict(order_delivery=(82, 0.28), returns_refunds=(96, 0.30), account_billing=(88, 0.27),
             product_howto=(124, 0.30), device_troubleshooting=(152, 0.31))
CONTRAST_SD = np.array([0.31, 0.36, 0.27, 0.32, 0.33])
# share of pairs the replies are as good as each other (any judge is a coin toss there)
AMB = np.array([0.09, 0.15, 0.08, 0.10, 0.12])
QLB = 0.48                        # on a pair with a better reply, the chance the longer one is it
EPS_A = np.array([0.12, 0.20, 0.24, 0.14, 0.44])     # a crowd judgment's error on a pair with a better reply
EPS_A25 = EPS_A + np.array([0.04, 0.05, 0.03, 0.04, 0.03])   # under guideline v2 (2025), before the v3 rewrite
EPS_B = np.array([0.06, 0.08, 0.07, 0.06, 0.10])     # a desk agent's
TECH = np.array([0.03, 0.03, 0.03, 0.025, 0.015])    # a senior technician's
BETA = np.array([0.30, 0.30, 0.30, 0.30, 0.30])      # the crowd's pull to the longer reply at a full contrast
TILT_C = 0.25                     # the contrast (log length ratio) over which the pull builds up
TIE_A = np.array([0.050, 0.058, 0.049, 0.052, 0.081])  # crowd "no preference" rate
# the reward model's learning: clear-pair accuracy 1 - 0.5 (1 + n_eff / K)^-ALPHA, n_eff in label information
K = np.array([1500.0, 2000.0, 2500.0, 1500.0, 15000.0])
ALPHA = 0.80
KAPPA = 0.50                      # how much of its labels' length pull the model takes on
RHO = 0.50                        # how strongly the models' errors share each pair's difficulty
SEED_SD = 0.020                   # run-to-run variation in probit units

MIX25 = np.array([0.32, 0.22, 0.15, 0.19, 0.12])
MONTH_MIX26 = {  # the share of each month's tickets by type (returns after the holidays, the smart-home beta from August)
    1: [0.26, 0.29, 0.16, 0.18, 0.11], 2: [0.28, 0.25, 0.16, 0.19, 0.12], 3: [0.30, 0.21, 0.16, 0.20, 0.13],
    4: [0.31, 0.19, 0.16, 0.21, 0.13], 5: [0.31, 0.18, 0.16, 0.21, 0.14], 6: [0.31, 0.18, 0.16, 0.21, 0.14],
    7: [0.31, 0.18, 0.16, 0.21, 0.14], 8: [0.30, 0.17, 0.16, 0.21, 0.16], 9: [0.29, 0.17, 0.16, 0.20, 0.18],
    10: [0.30, 0.17, 0.16, 0.19, 0.18], 11: [0.33, 0.17, 0.15, 0.18, 0.17], 12: [0.31, 0.22, 0.15, 0.18, 0.14]}
TICKETS26 = {1: 41200, 2: 36100, 3: 37400, 4: 36800, 5: 37900, 6: 38500, 7: 39800, 8: 42600, 9: 44100, 10: 45900,
             11: 55300, 12: 51200}
PLAN27_MONTHS = {  # the 2027 plan by month, the smart-home range shipping nationally from February
    1: [0.22, 0.18, 0.12, 0.17, 0.31], 2: [0.15, 0.11, 0.10, 0.16, 0.48], 3: [0.15, 0.11, 0.10, 0.15, 0.49],
    4: [0.15, 0.11, 0.10, 0.15, 0.49], 5: [0.15, 0.11, 0.10, 0.15, 0.49], 6: [0.15, 0.11, 0.10, 0.16, 0.48],
    7: [0.15, 0.11, 0.10, 0.16, 0.48], 8: [0.15, 0.11, 0.10, 0.16, 0.48], 9: [0.15, 0.11, 0.10, 0.16, 0.48],
    10: [0.15, 0.11, 0.10, 0.16, 0.48], 11: [0.18, 0.11, 0.10, 0.15, 0.46], 12: [0.16, 0.15, 0.10, 0.15, 0.44]}
TICKETS27 = {1: 52800, 2: 58400, 3: 61900, 4: 60300, 5: 61200, 6: 62800, 7: 64100, 8: 65900, 9: 66800, 10: 68400,
             11: 79600, 12: 74200}

ORDER_TF = 300000                  # the signed Tallyfield order for Q1 2027, comparisons invoiced
OPTION_TF = 300000                 # the order's option: up to this many more, in steps of 10,000
PRICE_TF = 0.42
PRICE_AD = 3.60
CAP_AD = 120000
BAR = 0.810

# the 2026 runs: id, trained, crowd spec, desk spec, review round, status, note
RUNS = [
    ("RM-01", dt.date(2026, 2, 2), ("all", dt.date(2026, 1, 30)), None, None, "retired", ""),
    ("RM-02", dt.date(2026, 2, 13), ("all", dt.date(2026, 2, 12)), None, 1, "retired", ""),
    ("RM-03", dt.date(2026, 2, 27), ("all", dt.date(2026, 2, 26)), None, None, "retired", ""),
    ("RM-04", dt.date(2026, 3, 13), ("all", dt.date(2026, 3, 12)), None, 2, "retired", ""),
    ("RM-05", dt.date(2026, 3, 27), ("all", dt.date(2026, 3, 26)), None, None, "retired", ""),
    ("RM-06", dt.date(2026, 4, 10), ("sample", 2000, dt.date(2026, 4, 9)), ("all", dt.date(2026, 4, 9)), None,
     "ablation", "Ardentdesk pilot, first half"),
    ("RM-07", dt.date(2026, 4, 17), ("sample", 4000, dt.date(2026, 4, 16)), ("all", dt.date(2026, 4, 16)), 3,
     "ablation", "Ardentdesk pilot"),
    ("RM-08", dt.date(2026, 4, 24), ("all", dt.date(2026, 4, 23)), None, None, "retired", ""),
    ("RM-09", dt.date(2026, 5, 8), ("all", dt.date(2026, 5, 7)), ("all", dt.date(2026, 5, 7)), None, "retired", ""),
    ("RM-10", dt.date(2026, 5, 22), ("all", dt.date(2026, 5, 21)), ("all", dt.date(2026, 5, 21)), 4, "retired", ""),
    ("RM-11", dt.date(2026, 6, 26), None, ("all", dt.date(2026, 6, 25)), None, "ablation", "Ardentdesk only"),
    ("RM-12", dt.date(2026, 6, 19), ("all", dt.date(2026, 6, 18)), ("all", dt.date(2026, 6, 18)), None, "retired", ""),
    ("RM-13", dt.date(2026, 7, 3), ("all", dt.date(2026, 7, 2)), ("all", dt.date(2026, 7, 2)), 5, "retired", ""),
    ("RM-14", dt.date(2026, 7, 6), ("all", dt.date(2026, 7, 2)), ("all", dt.date(2026, 7, 2)), None, "ablation",
     "RM-13 data, second seed"),
    ("RM-15", dt.date(2026, 7, 31), ("all", dt.date(2026, 7, 30)), ("all", dt.date(2026, 7, 30)), None, "retired", ""),
    ("RM-16", dt.date(2026, 8, 14), ("all", dt.date(2026, 8, 13)), ("all", dt.date(2026, 8, 13)), 6, "retired", ""),
    ("RM-17", dt.date(2026, 8, 28), ("sample", 30000, dt.date(2026, 8, 27)), ("all", dt.date(2026, 8, 27)), None,
     "ablation", "Tallyfield cut to 30k"),
    ("RM-18", dt.date(2026, 9, 11), ("all", dt.date(2026, 9, 10)), ("all", dt.date(2026, 9, 10)), None, "retired", ""),
    ("RM-19", dt.date(2026, 9, 18), ("all", dt.date(2026, 9, 17)), None, None, "ablation", "Tallyfield only"),
    ("RM-20", dt.date(2026, 9, 25), ("all", dt.date(2026, 9, 24)), ("all", dt.date(2026, 9, 24)), None, "retired", ""),
    ("RM-21", dt.date(2026, 10, 2), ("all", dt.date(2026, 10, 1)), ("all", dt.date(2026, 10, 1)), None, "retired", ""),
    ("RM-22", dt.date(2026, 10, 9), ("all", dt.date(2026, 10, 8)), ("all", dt.date(2026, 10, 8)), None, "production",
     ""),
]
REVIEW_ROUNDS = {1: (dt.date(2026, 2, 16), "RM-02"), 2: (dt.date(2026, 3, 16), "RM-04"), 3: (dt.date(2026, 4, 20), "RM-07"),
                 4: (dt.date(2026, 5, 25), "RM-10"), 5: (dt.date(2026, 7, 6), "RM-13"), 6: (dt.date(2026, 8, 3), "RM-15"),
                 7: (dt.date(2026, 8, 17), "RM-16")}
REVIEW_PER_TYPE = 250
STUDY_PER_TYPE = 400
INTERNAL_N = 8000


def rng_for(name):
    h = int(hashlib.sha256(("%d:%s" % (SEED, name)).encode()).hexdigest()[:16], 16)
    return np.random.default_rng(h)


def tilt_h(c):
    """the share of the crowd's full pull to the longer reply at log length ratio c"""
    return 1.0 - np.exp(-(np.abs(c) / TILT_C) ** 2)


# ------------------------------------------------------------------ pairs and judges
def draw_pairs(rng, types):
    """types: int array of ticket-type indices. Returns a frame of pairs with their latent truth."""
    n = len(types)
    med = np.array([WORDS[TYPES[d]][0] for d in types], float)
    sd = np.array([WORDS[TYPES[d]][1] for d in types])
    wa = np.maximum(14, np.round(med * np.exp(rng.normal(0, sd)))).astype(int)
    lr = rng.normal(0, CONTRAST_SD[types])
    wb = np.maximum(12, np.round(wa * np.exp(lr))).astype(int)
    amb = rng.random(n) < AMB[types]
    longer_is_b = wb > wa
    tie_len = wb == wa
    better_longer = rng.random(n) < QLB
    better_b = np.where(tie_len, rng.random(n) < 0.5, np.where(better_longer, longer_is_b, ~longer_is_b))
    c = np.log(wb / wa)
    z = rng.normal(0, 1, n)
    return pd.DataFrame(dict(type=types, words_a=wa, words_b=wb, amb=amb, better_b=better_b, contrast=c, z=z))


def _longer_b(P):
    return (P.words_b.values > P.words_a.values)


def crowd_judge(rng, P, ties=True, eps=None):
    """a Tallyfield judgment: 'A', 'B' or 'none'"""
    n = len(P); t = P.type.values
    eps = EPS_A if eps is None else eps
    pull = BETA[t] * tilt_h(P.contrast.values)
    lb = _longer_b(P)
    tilted = (rng.random(n) < pull) & (P.words_a.values != P.words_b.values)
    right = rng.random(n) >= eps[t]
    pick_b = np.where(P.amb.values, rng.random(n) < 0.5, np.where(right, P.better_b.values, ~P.better_b.values))
    pick_b = np.where(tilted, lb, pick_b)
    out = np.where(pick_b, "B", "A").astype(object)
    if ties:
        out[rng.random(n) < TIE_A[t]] = "none"
    return out


def desk_judge(rng, P):
    n = len(P); t = P.type.values
    right = rng.random(n) >= EPS_B[t]
    pick_b = np.where(P.amb.values, rng.random(n) < 0.5, np.where(right, P.better_b.values, ~P.better_b.values))
    return np.where(pick_b, "B", "A").astype(object)


def tech_judge(rng, P):
    n = len(P); t = P.type.values
    right = rng.random(n) >= TECH[t]
    pick_b = np.where(P.amb.values, rng.random(n) < 0.5, np.where(right, P.better_b.values, ~P.better_b.values))
    return np.where(pick_b, "B", "A").astype(object)


# ------------------------------------------------------------------ the learner
_INFO = None


def label_info():
    """information per usable label by source and type, the square of its signal averaged over each type's pairs (0
    where the replies are as good as each other): the quantity the reward model learns from"""
    global _INFO
    if _INFO is None:
        rng = rng_for("info-reference")
        out = {"A": np.zeros(ND), "B": np.zeros(ND)}
        for d in range(ND):
            P = draw_pairs(rng, np.full(200000, d))
            clear = ~P.amb.values
            pull = BETA[d] * tilt_h(P.contrast.values) * (P.words_a.values != P.words_b.values)
            # a judgment's signal about which reply is better: the gap between its chance of naming a reply when
            # that reply is the better one and when it is not; a judgment pulled to the longer reply carries none
            sig_a = (1 - pull) * (1 - 2 * EPS_A[d])
            out["A"][d] = np.mean(np.where(clear, sig_a ** 2, 0.0))
            out["B"][d] = np.mean(np.where(clear, (1 - 2 * EPS_B[d]) ** 2, 0.0))
        _INFO = out
    return _INFO


def learner(nA, nB):
    """clear-pair accuracy by type and the share of the crowd's pull the model takes on, for usable label counts by
    type (arrays)"""
    I = label_info()
    neff = nA * I["A"] + nB * I["B"]
    p = 1 - 0.5 * (1 + neff / K) ** (-ALPHA)
    s = np.where(nA + nB > 0, nA / np.maximum(nA + nB, 1), 0.0)
    return p, KAPPA * s, neff


def model_picks(rng, P, p, tilt_share, shift=0.0):
    """the run's pick on each pair ('A' or 'B'): its own pull to the longer reply, else its judgment on the pair,
    harder pairs harder for every run (RHO)"""
    n = len(P); t = P.type.values
    lb = _longer_b(P)
    pull = tilt_share[t] * BETA[t] * tilt_h(P.contrast.values) * (P.words_a.values != P.words_b.values)
    tilted = rng.random(n) < pull
    thr = norm.ppf(p[t]) + shift
    right = (RHO * P.z.values + np.sqrt(1 - RHO ** 2) * rng.normal(0, 1, n)) < thr
    pick_b = np.where(P.amb.values, rng.random(n) < 0.5, np.where(right, P.better_b.values, ~P.better_b.values))
    pick_b = np.where(tilted, lb, pick_b)
    return np.where(pick_b, "B", "A").astype(object)


# ------------------------------------------------------------------ expected accuracy (the truth, for checks only)
def maj_err(t):
    return 3 * t ** 2 * (1 - t) + t ** 3


def expected_accuracy(nA, nB):
    """accuracy against the majority of three senior technicians by type, in expectation over each type's pairs"""
    p, ts, _ = learner(nA, nB)
    rng = rng_for("acc-reference")
    out = np.zeros(ND)
    for d in range(ND):
        P = draw_pairs(rng, np.full(100000, d))
        clear = ~P.amb.values
        pull = ts[d] * BETA[d] * tilt_h(P.contrast.values) * (P.words_a.values != P.words_b.values)
        lb = _longer_b(P)
        longer_right = lb == P.better_b.values
        r = pull * longer_right + (1 - pull) * p[d]
        m = maj_err(TECH[d])
        out[d] = np.mean(np.where(clear, r * (1 - m) + (1 - r) * m, 0.5))
    return out


# ------------------------------------------------------------------ the 2026 delivery streams
def tallyfield_stream():
    """weekly Tallyfield batches from 12 January to 25 September 2026: each comparison's pair, worker, judgment and
    times. Usable judgments total 210,000 across the year."""
    rng = rng_for("tallyfield")
    weeks = [dt.date(2026, 1, 12) + dt.timedelta(weeks=i) for i in range(38)]
    ramp = np.array([min(1.0, 0.30 + 0.07 * i) for i in range(38)])
    size = ramp * (1 + rng.normal(0, 0.06, 38))
    usable_target = 210000
    tot = np.round(size / size.sum() * usable_target / (1 - 0.056)).astype(int)
    workers = ["TF-%05d" % (10000 + i) for i in rng.choice(89999, 460, replace=False)]
    w_rate = rng.gamma(1.6, 1.0, len(workers)); w_rate /= w_rate.sum()
    w_speed = rng.lognormal(0, 0.25, len(workers))
    w_start = rng.integers(0, 30, len(workers))     # the week a worker joined the project
    rows = []
    cid = 1
    for i, wk in enumerate(weeks):
        mix = np.array(MONTH_MIX26[wk.month]); mix = mix / mix.sum()
        n = tot[i]
        types = rng.choice(ND, n, p=mix)
        P = draw_pairs(rng, types)
        ch = crowd_judge(rng, P)
        active = np.where(w_start <= i)[0]
        pw = w_rate[active] / w_rate[active].sum()
        wid = rng.choice(active, n, p=pw)
        exp_wk = i - w_start[wid]
        base = (34 + 0.11 * (P.words_a.values + P.words_b.values)) * w_speed[wid]
        secs = np.round(base * (1 + 0.55 * np.exp(-exp_wk / 3.0)) * rng.lognormal(0, 0.35, n)).astype(int) + 6
        day = rng.integers(0, 5, n)
        tod = rng.normal(13.5, 3.2, n).clip(6, 23.5)
        sub = [dt.datetime.combine(wk + dt.timedelta(days=int(dd)), dt.time(0)) + dt.timedelta(hours=float(h))
               for dd, h in zip(day, tod)]
        batch = "TF26-%03d" % (i + 1)
        dlv = dt.datetime.combine(wk + dt.timedelta(days=4), dt.time(17, 30))
        df = P.copy()
        df["comparison_id"] = ["TFC-26-%06d" % (cid + k) for k in range(n)]
        cid += n
        df["batch_id"] = batch
        df["worker_idx"] = wid
        df["worker_id"] = [workers[k] for k in wid]
        df["choice"] = ch
        df["seconds"] = secs
        df["submitted_local"] = sub
        df["delivered_local"] = dlv
        df["week"] = i
        rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    return D


DESK_PARTS = [  # start, end, comparisons, ticket types (None: the month's ticket mix), batch prefix
    (dt.date(2026, 3, 30), dt.date(2026, 4, 16), 12000, None, "PILOT"),
    (dt.date(2026, 6, 1), dt.date(2026, 7, 17), 8000, None, "C26"),
    (dt.date(2026, 7, 6), dt.date(2026, 8, 12), 15000, [4], "SHB"),
    (dt.date(2026, 8, 17), dt.date(2026, 9, 18), 6000, None, "C26"),
]


def ardentdesk_stream():
    """the Ardentdesk pilot (12,000 comparisons, 30 March to 16 April), the contract (8,000 from 1 June, 6,000 from
    17 August) and the smart-home beta batch of device troubleshooting pairs (15,000, 6 July to 12 August)"""
    rng = rng_for("ardentdesk")
    agents = ["AD-%03d" % k for k in (rng.choice(400, 26, replace=False) + 100)]
    rows = []
    rid = 1
    for k, (d0, d1, n, only, prefix) in enumerate(DESK_PARTS):
        days = [d0 + dt.timedelta(days=i) for i in range((d1 - d0).days + 1)]
        days = [d for d in days if d.weekday() < 5]
        per = np.full(len(days), n // len(days)); per[: n - per.sum()] += 1
        for day, m in zip(days, per):
            mix = np.array(MONTH_MIX26[day.month], float)
            if only is not None:
                mix = np.zeros(ND); mix[only] = 1.0
            mix = mix / mix.sum()
            types = rng.choice(ND, m, p=mix)
            P = draw_pairs(rng, types)
            ch = desk_judge(rng, P)
            ag = rng.choice(len(agents), m)
            swapped = rng.random(m) < 0.5
            left_chosen = np.where(swapped, ch == "B", ch == "A")
            tod = rng.normal(13.0, 2.2, m).clip(8.5, 18.5)
            df = P.copy()
            df["record_id"] = ["ADR-%06d" % (rid + j) for j in range(m)]
            rid += m
            df["batch"] = ("PILOT-01" if prefix == "PILOT" else "%s-%02d" % (prefix, ((day - d0).days // 14) + 1 + (4 if k == 3 else 0)))
            df["agent_id"] = [agents[j] for j in ag]
            df["swapped"] = swapped
            df["chose"] = np.where(left_chosen, "left", "right")
            df["choice"] = ch
            df["handled_local"] = [dt.datetime.combine(day, dt.time(0)) + dt.timedelta(hours=float(h)) for h in tod]
            df["seconds"] = np.round((40 + 0.16 * (P.words_a.values + P.words_b.values)) * rng.lognormal(0, 0.28, m)).astype(int)
            rows.append(df)
    return pd.concat(rows, ignore_index=True)


# ------------------------------------------------------------------ the runs
def run_counts(TF, AD):
    """usable comparisons by type in each run's training set, from the delivery streams"""
    rng = rng_for("run-samples")
    tf_use = TF[TF.choice != "none"]
    tf_date = tf_use.delivered_local.dt.date.values
    ad_date = AD.handled_local.dt.date.values
    out = {}
    for rid, trained, cs, ds, rnd, status, note in RUNS:
        nA = np.zeros(ND); nB = np.zeros(ND)
        if cs is not None:
            if cs[0] == "all":
                sel = tf_use[tf_date <= cs[1]]
            else:
                pool = tf_use[tf_date <= cs[2]]
                sel = pool.iloc[np.sort(rng.choice(len(pool), cs[1], replace=False))]
            nA = np.bincount(sel.type.values, minlength=ND).astype(float)
        if ds is not None:
            sel = AD[ad_date <= ds[1]]
            nB = np.bincount(sel.type.values, minlength=ND).astype(float)
        out[rid] = (nA, nB)
    return out


def build():
    TF = tallyfield_stream()
    AD = ardentdesk_stream()
    counts = run_counts(TF, AD)
    shift = {r[0]: rng_for("seed-" + r[0]).normal(0, SEED_SD) for r in RUNS}
    state = {rid: learner(*counts[rid]) for rid in counts}
    # the internal set, built in 2025 and judged once each by Tallyfield
    rng = rng_for("internal")
    types = rng.choice(ND, INTERNAL_N, p=MIX25 / MIX25.sum())
    IS = draw_pairs(rng, types)
    lab = crowd_judge(rng, IS, ties=False, eps=EPS_A25)
    IS["label"] = lab
    IS["pair_id"] = ["IS25-%05d" % (i + 1) for i in range(INTERNAL_N)]
    picks = {}
    for rid, *_ in RUNS:
        p, ts, _ = state[rid]
        picks[rid] = model_picks(rng_for("is-" + rid), IS, p, ts, shift[rid])
    # the senior technicians' shadow reviews of six runs on live drafts
    REV = []
    for rnd, (d0, rid) in REVIEW_ROUNDS.items():
        rr = rng_for("review-%d" % rnd)
        types = np.repeat(np.arange(ND), REVIEW_PER_TYPE)
        rr.shuffle(types)
        P = draw_pairs(rr, types)
        p, ts, _ = state[rid]
        P["pick"] = model_picks(rr, P, p, ts, shift[rid])
        for k in range(3):
            P["vote%d" % (k + 1)] = tech_judge(rr, P)
        P["round"] = rnd
        P["run_id"] = rid
        REV.append(P)
    REV = pd.concat(REV, ignore_index=True)
    # the label audit (July and August): 1,200 delivered pairs, three fresh judgments from each source
    rs = rng_for("study")
    types = np.repeat(np.arange(ND), STUDY_PER_TYPE)
    rs.shuffle(types)
    ST = draw_pairs(rs, types)
    for k in range(3):
        ST["crowd%d" % (k + 1)] = crowd_judge(rs, ST)
        ST["desk%d" % (k + 1)] = desk_judge(rs, ST)
        ST["tech%d" % (k + 1)] = tech_judge(rs, ST)
    return dict(TF=TF, AD=AD, counts=counts, shift=shift, state=state, IS=IS, picks=picks, REV=REV, ST=ST)


# ------------------------------------------------------------------ the 2027 decision, in truth (checks only)
def mix27():
    tot = np.zeros(ND)
    for m, mix in PLAN27_MONTHS.items():
        tot += TICKETS27[m] * np.array(mix) / np.sum(mix)
    return tot / tot.sum()


def order_by_type():
    """the signed order's comparisons by ticket type: the 2027 plan's shares, to the nearest 100"""
    m = mix27()
    n = (np.round(ORDER_TF * m / 100.0) * 100).astype(int)
    n[np.argmax(m)] += ORDER_TF - n.sum()
    return n


def order_rows():
    return [(TYPES[d], int(n)) for d, n in enumerate(order_by_type())]


DESK_MIX = np.array([0.0, 0.0, 0.0, 0.0, 1.0])   # the quote is for the device-support team's troubleshooting pairs


def truth_forecast(counts, desk, option=0):
    nA0, nB0 = counts["RM-22"]
    usable = (order_by_type() + option * mix27()) * (1 - TIE_A)
    acc = expected_accuracy(nA0 + usable, nB0 + desk * DESK_MIX)
    return acc, float((acc * mix27()).sum())
