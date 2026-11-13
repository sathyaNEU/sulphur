"""The world behind task20 architecture 4: Wexmoor University's endowment, its private-fund managers, the funds'
portfolio companies, an industry cash-flow benchmark, the market (exit activity, equities, short rate) and the
stress the liquidity policy defines for 2027-28. Everything here is the world's truth; the golden (analysis.py) reads
only the files pack.py writes from it."""
import math
import numpy as np

Q0 = 2000
def qi(y, q): return (y - Q0) * 4 + (q - 1)
def qy(i): return Q0 + i // 4
def qq(i): return i % 4 + 1
def qlab(i): return "%dQ%d" % (qy(i), qq(i))
NQ = qi(2028, 4) + 1
H_END = qi(2026, 4)
W = list(range(H_END + 1, H_END + 9))          # the policy's 24 months, 2027Q1 to 2028Q4

P = dict(
    exit_lag=2, a_dn=0.85, a_up=0.20, gamma=1.3, gamma2=0.0, e_ref=100.0,
    deal_gamma=0.20, line_margin=1.75, support=0.070, support_e=1.00, support_cap=0.30, rescue=0.30, rescue_th=0.45,
    slip_k=6.0, slip_ref=100.0, slip_base=0.08,
    ext_on=True, ext_e=95.0, ext_share=0.92, ext_win=2, ext_q=8,
    stress_rate_up=2.5, stress_eq=[0.85, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1.00],
    plan_total=500.0,
)

def _interp(knots, n=NQ):
    xs = [qi(*k[0]) for k in knots]
    return np.interp(np.arange(n), xs, [k[1] for k in knots])

def market(seed=11):
    rng = np.random.default_rng(seed)
    E = _interp([((2000,1),95),((2000,3),105),((2001,2),60),((2002,3),42),((2003,4),60),((2005,2),85),((2007,2),112),((2008,2),105),
                 ((2008,3),90),((2008,4),55),((2009,1),35),((2009,2),30),((2009,3),38),((2009,4),50),((2010,1),60),((2010,2),68),
                 ((2011,2),80),((2011,4),74),((2013,2),92),((2014,4),105),((2016,1),100),((2018,4),128),((2019,4),130),((2020,1),118),
                 ((2020,2),62),((2020,3),84),((2020,4),102),((2021,2),150),((2021,4),165),((2022,1),150),((2022,2),122),((2022,4),84),
                 ((2023,2),64),((2023,4),60),((2024,2),66),((2024,4),78),((2025,2),94),((2025,4),106),((2026,2),112),((2026,4),116)])
    E = E * np.exp(rng.normal(0, 0.03, NQ))
    E = E * 100.0 / E[qi(2015, 1):qi(2015, 4) + 1].mean()          # the index is published with 2015 = 100
    S = _interp([((2000,1),100),((2000,3),104),((2002,3),58),((2003,4),78),((2007,3),118),((2008,4),75),((2009,1),60),((2010,4),95),
                 ((2013,4),128),((2015,4),140),((2018,3),196),((2018,4),172),((2019,4),210),((2020,1),164),((2020,4),218),((2021,4),268),
                 ((2022,3),210),((2023,4),256),((2024,4),288),((2025,4),298),((2026,4),308)])
    S = S * np.exp(rng.normal(0, 0.015, NQ))
    R = _interp([((2000,1),5.6),((2000,4),6.4),((2001,4),1.8),((2003,2),1.0),((2004,2),1.0),((2006,2),5.0),((2007,3),5.1),((2008,2),2.0),
                 ((2008,4),0.2),((2015,4),0.2),((2016,4),0.6),((2018,4),2.4),((2019,3),2.2),((2020,1),1.2),((2020,2),0.05),((2021,4),0.05),
                 ((2022,2),1.0),((2022,4),4.2),((2023,3),5.3),((2024,3),5.3),((2024,4),4.6),((2025,2),4.1),((2025,4),3.4),((2026,2),3.0),((2026,4),2.75)])
    return E, S, R

def stressed(E, S, R):
    E, S, R = E.copy(), S.copy(), R.copy()
    base = E[qi(2008, 2)]
    for k in range(8):
        E[H_END + 1 + k] = E[H_END] * E[qi(2008, 3) + k] / base
        S[H_END + 1 + k] = S[H_END] * P["stress_eq"][k]
        R[H_END + 1 + k] = R[H_END] + P["stress_rate_up"]
    return E, S, R

# ------------------------------------------------------------------------------------------------ strategies
ST = {  # ip/life in quarters; n deals; hazard start/plateau; income per quarter
    "BO": dict(ip=20, life=44, fee=0.020, mult=1.85, sd=0.45, n=(9, 14), h0=8, h1=18, hmax=0.085, inc=0.0, fo=0.12, pace=(0.060, 0.068), deploy=0.82),
    "GE": dict(ip=20, life=44, fee=0.020, mult=1.95, sd=0.55, n=(11, 16), h0=8, h1=18, hmax=0.080, inc=0.0, fo=0.15, pace=(0.058, 0.066), deploy=0.82),
    "VC": dict(ip=20, life=48, fee=0.025, mult=2.10, sd=0.95, n=(20, 30), h0=12, h1=24, hmax=0.060, inc=0.0, fo=0.30, pace=(0.055, 0.065), deploy=0.80),
    "RE": dict(ip=16, life=32, fee=0.0125, mult=1.35, sd=0.25, n=(7, 11), h0=6, h1=14, hmax=0.070, inc=0.0105, fo=0.05, pace=(0.080, 0.092), deploy=0.90),
    "IN": dict(ip=20, life=48, fee=0.015, mult=1.55, sd=0.25, n=(6, 9), h0=16, h1=28, hmax=0.035, inc=0.0135, fo=0.08, pace=(0.056, 0.064), deploy=0.90),
    "PC": dict(ip=12, life=28, fee=0.010, mult=1.05, sd=0.08, n=(30, 45), h0=5, h1=6, hmax=0.075, inc=None, fo=0.0, pace=(0.13, 0.15), deploy=0.92),
}
EXIT_DRIVEN = ("BO", "GE", "VC", "RE", "IN")

def hazard_age(st, age_q):
    s = ST[st]
    if age_q < s["h0"]: return 0.0
    if age_q >= s["h1"]: return s["hmax"]
    return s["hmax"] * (age_q - s["h0"] + 1) / (s["h1"] - s["h0"] + 1)

def exit_target(e):
    lx = math.log(max(e, 1.0) / P["e_ref"])
    return min(max(math.exp(P["gamma"] * lx - P["gamma2"] * lx * lx), 0.06), 1.7)

def propensity(E, a_dn=None, a_up=None, lag=None):
    """the managers' exit propensity: follows the exit market `lag` quarters late, falls fast and recovers slowly."""
    a_dn = P["a_dn"] if a_dn is None else a_dn; a_up = P["a_up"] if a_up is None else a_up
    lag = P["exit_lag"] if lag is None else lag
    p = np.ones(len(E)); cur = 1.0
    for t in range(len(E)):
        tau = exit_target(E[max(t - lag, 0)])
        cur = cur + (a_dn if tau < cur else a_up) * (tau - cur)
        p[t] = cur
    return p

def line_quarters(gp, r):
    """how long a manager leaves an investment on the fund's subscription line before calling it, given the short
    rate: its own habit at near-zero rates, shortened as the line's cost rises, and nothing once the all-in cost
    passes the manager's own tolerance (the clean-down)."""
    if gp["cd_base"] == 0: return 0
    cost = r + P["line_margin"]
    if cost >= gp["tol"]: return 0
    if r < 1.0: return gp["cd_base"]
    if r < 3.0: return max(gp["cd_base"] - 1, 0)
    return max(gp["cd_base"] - 2, 0)

# ------------------------------------------------------------------------------------------------ managers
GP_PLAN = {"BO": 8, "GE": 3, "VC": 4, "RE": 3, "IN": 3, "PC": 4}

def managers(seed=23):
    rng = np.random.default_rng(seed)
    out = []
    for st, n in GP_PLAN.items():
        for j in range(n):
            cdp = {"VC": [0.55, 0.30, 0.15, 0.0, 0.0], "PC": [0.05, 0.15, 0.30, 0.30, 0.20]}.get(st, [0.10, 0.15, 0.25, 0.30, 0.20])
            out.append(dict(id="%s%d" % (st, j + 1), st=st, cd_base=int(rng.choice([0, 1, 2, 3, 4], p=cdp)),
                            tol=float(rng.uniform(4.6, 5.6)), recyc=float(rng.choice([0.15, 0.3, 0.45], p=[0.35, 0.35, 0.30])),
                            pace=float(rng.uniform(*ST[st]["pace"])), slip_k=float(rng.uniform(1.6, 3.4)),
                            first=int(rng.integers(2013, 2019)), gap=int(rng.integers(3, 5)), fy_june=False))
    out[3]["fy_june"] = True; out[17]["fy_june"] = True
    return out

def slip_quarters(E, exp_q, rng):
    """how many quarters a fund's first close comes after the date its manager gave at commitment: fundraising stalls
    when the exit market (and with it the distributions investors live on) sat below normal in the quarter before the
    close; a few funds slip a quarter whatever the market."""
    e = E[max(exp_q - 1, 0)]
    weak = max(0.0, 1.0 - e / P["slip_ref"])
    return int(math.floor(P["slip_k"] * weak + rng.random())) + (1 if rng.random() < P["slip_base"] else 0)

def commitments(gps, E, seed=37):
    rng = np.random.default_rng(seed)
    base = {"BO": 75, "GE": 50, "VC": 26, "RE": 50, "IN": 72, "PC": 72}
    out = []
    for gp in gps:
        y = gp["first"]; k = 0
        while y <= 2027:
            C = round(base[gp["st"]] * 1.07 ** (y - 2013) * float(rng.uniform(0.8, 1.25)))
            share = float(rng.uniform(0.025, 0.06))
            commit_q = qi(y, int(rng.integers(1, 5)))
            exp_fc = commit_q + int(rng.integers(1, 4))
            if y == 2026:
                if rng.random() < 0.5:
                    commit_q = qi(2026, int(rng.integers(1, 3))); exp_fc = commit_q + 1
                else:
                    commit_q = qi(2026, int(rng.integers(3, 5))); exp_fc = qi(2027, 3) + int(rng.integers(0, 2))
            if y == 2027:
                commit_q = qi(2027, int(rng.integers(1, 3))); exp_fc = commit_q + int(rng.integers(0, 2))
            out.append(dict(gp=gp, vint=y, k=k, C=float(C), share=share, size=round(C / share), commit_q=commit_q, exp_fc=exp_fc,
                            seed=int(rng.integers(1, 2**31))))
            y += gp["gap"]; k += 1
    srng = np.random.default_rng(seed + 1)
    for f in out:
        f["slip_u"] = (float(srng.random()), float(srng.random()))
        f["fc"] = f["exp_fc"] + slip_of(f, E)
    return out

def slip_of(f, E):
    class _R:
        def __init__(s, u): s.u = list(u)
        def random(s): return s.u.pop(0)
    return slip_quarters(E, f["exp_fc"], _R(f["slip_u"]))

# ------------------------------------------------------------------------------------------------ one fund
def run_fund(f, E, S, R, p, fc, upto=NQ - 1, scale=None, rec=None, cd_override=None, deal_log=None):
    """simulates a fund at fund level from its first close `fc`; returns quarterly arrays at the endowment's share
    (or per unit of commitment when scale is given). rec: dict to receive fund-level series for the audited accounts."""
    gp = f["gp"]; st = gp["st"]; s = ST[st]
    rng = np.random.default_rng(f["seed"])
    size = float(f["size"]); share = f["C"] / size if scale is None else scale
    n_deals = int(rng.integers(s["n"][0], s["n"][1] + 1))
    target = s["deploy"] * size
    deal_size = target / (n_deals * (1 + s["fo"] * 0.6))
    o = {k: np.zeros(NQ) for k in ("call_inv", "call_fee", "call_exp", "dist", "proc", "inc", "inv", "nav", "line", "recyc", "cost")}
    called_cum = 0.0               # fund-level contributions to date (calls never exceed the commitments)
    deals = []                     # [cost, inv_q, mult, alive, fo_done, id]
    queue = []                     # line draws: [q, amount]
    inv_cum = 0.0; recyc_cum = 0.0; dealno = 0
    ip = s["ip"]; o["ip_end"] = fc + ip
    for q in range(fc, min(upto, fc + s["life"]) + 1):
        age = q - fc
        if age == ip and ip == s["ip"] and P["ext_on"]:
            weak = float(np.mean([E[max(q - k, 0)] for k in range(1, P["ext_win"] + 1)])) < P["ext_e"]
            behind = inv_cum < P["ext_share"] * target
            if weak and behind:
                ip = s["ip"] + P["ext_q"]; o["ip_end"] = fc + ip      # the advisory committee extends the period
        # exits and income on the deals held at the start of the quarter
        proc = 0.0; inc = 0.0
        for d in deals:
            if not d[3]: continue
            a = q - d[1]
            if st == "PC":
                inc += (R[q] + 6.0) / 400.0 * d[0]
                h = hazard_age(st, a)
            else:
                if s["inc"]: inc += s["inc"] * d[0] * (1 + (d[2] - 1) * min(a / 16.0, 1.0)) * 0.9
                h = hazard_age(st, a) * p[q]
            if age >= s["life"] - 1: h = 1.0
            if rng.random() < h:
                m = d[2] * ((S[q] / S[d[1]]) ** 0.30 if st != "PC" else 1.0)
                proc += d[0] * m; d[3] = False
                if deal_log is not None: deal_log.append(("exit", f["id"], d[5], q, d[0], d[0] * m))
        # deployment: new deals and follow-ons
        inv = 0.0
        if age < ip:
            room = max(target - inv_cum + recyc_cum, 0.0)
            # the deal market: the managers find fewer deals when exits are weak (credit funds lend on regardless)
            md = min(max((E[q] / P["e_ref"]) ** P["deal_gamma"], 0.4), 1.4) if st != "PC" else 1.0
            budget = gp["pace"] * room * md
            while budget > 0.35 * deal_size and dealno < n_deals * 1.5:
                c = deal_size * math.exp(rng.normal(0, 0.35))
                c = min(c, budget * 1.6)
                mult = s["mult"] * math.exp(rng.normal(0, s["sd"]) - s["sd"] ** 2 / 2)
                deals.append([c, q, mult, True, False, dealno]); inv += c; budget -= c
                if deal_log is not None: deal_log.append(("new", f["id"], dealno, q, c, mult))
                dealno += 1
        for d in deals:
            if d[3] and not d[4] and q - d[1] >= 5 and s["fo"] > 0 and age < ip + 8:
                fo = s["fo"] * d[0] / (1 + s["fo"]) ; d[0] += fo; d[4] = True; inv += fo
                if deal_log is not None: deal_log.append(("follow_on", f["id"], d[5], q, fo, 0.0))
        sf = max(0.0, P["support_e"] - E[max(q - 2, 0)] / P["e_ref"]) / P["support_e"]
        # two channels: the managers' follow-on reserves (capped once a fund's reserve plan is spent) and, past a
        # shortfall where lenders call covenants, rescue financings that keep rising with the shortfall
        dep_e = min(sf, P["support_cap"]) + P["rescue"] / P["support"] * max(0.0, sf - P["rescue_th"])
        if st in ("BO", "GE", "VC") and dep_e > 0:
            headroom = max(size - called_cum - sum(a for _, a in queue), 0.0)
            for d in deals:
                if d[3] and q - d[1] >= 8 and headroom > 0 and rng.random() < 0.6:
                    sup = min(P["support"] / 0.6 * dep_e * d[0] * math.exp(rng.normal(0, 0.25) - 0.03125), headroom)
                    if sup > 0.0002 * size:
                        d[0] += sup; inv += sup; headroom -= sup
                        if deal_log is not None: deal_log.append(("follow_on", f["id"], d[5], q, sup, 0.0))
        rc = 0.0
        if age < ip and gp["recyc"] > 0 and proc > 0:
            rc = min(gp["recyc"] * proc, max(0.15 * size - recyc_cum, 0.0), inv)
        recyc_cum += rc; inv_cum += inv
        need = inv - rc
        fee = s["fee"] / 4.0 * (size if age < ip else sum(d[0] for d in deals if d[3]))
        cd = (cd_override if cd_override is not None else line_quarters(gp, R[q])) if f["vint"] >= 2012 else 0
        queue.append([q, need]); called = 0.0; keep = []
        for (q0, a) in queue:
            if q - q0 >= cd: called += a
            else: keep.append([q0, a])
        queue = keep
        line = sum(a for _, a in queue)
        fv = sum(d[0] * (1 + (d[2] - 1) * min((q - d[1]) / 16.0, 1.0)) * ((S[max(q - 1, 0)] / S[d[1]]) ** 0.40 if st != "PC" else 1.0)
                 for d in deals if d[3])
        cost = sum(d[0] for d in deals if d[3])
        if deal_log is not None and q <= H_END:
            for d in deals:
                if d[3]:
                    v = d[0] * (1 + (d[2] - 1) * min((q - d[1]) / 16.0, 1.0)) * ((S[max(q - 1, 0)] / S[d[1]]) ** 0.40 if st != "PC" else 1.0)
                    deal_log.append(("val", f["id"], d[5], q, d[0], v))
        exp = 0.0005 * size if age > 0 else 0.0
        avail = max(size - called_cum, 0.0)
        fee_c = min(fee, avail); avail -= fee_c
        exp_c = min(exp, avail); avail -= exp_c
        inv_c = min(called, avail)
        short = (fee - fee_c) + (exp - exp_c) + (called - inv_c)      # paid out of proceeds once the commitment is used
        called_cum += fee_c + exp_c + inv_c
        D = max(proc - rc + inc - short, 0.0)
        for k, v in (("call_inv", inv_c), ("call_fee", fee_c), ("call_exp", exp_c), ("dist", D), ("proc", proc), ("inc", inc), ("inv", inv),
                     ("nav", fv - line), ("line", line), ("recyc", rc), ("cost", cost)):
            o[k][q] = v * share
        if rec is not None:
            rec.setdefault("fv", {})[q] = fv; rec.setdefault("line", {})[q] = line; rec.setdefault("cost", {})[q] = cost
    return o

def benchmark_funds(gps, n=2200, seed=71):
    rng = np.random.default_rng(seed)
    out = []
    strat = list(GP_PLAN.keys()); wts = np.array([0.36, 0.12, 0.20, 0.12, 0.08, 0.12])
    for i in range(n):
        st = str(rng.choice(strat, p=wts))
        vv = np.arange(2000, 2025); pv = 4.0 + np.maximum(vv - 2004, 0) * 0.6; pv = pv / pv.sum()
        vint = int(rng.choice(vv, p=pv))
        cdp = {"VC": [0.55, 0.30, 0.15, 0.0, 0.0], "PC": [0.05, 0.15, 0.30, 0.30, 0.20]}.get(st, [0.10, 0.15, 0.25, 0.30, 0.20])
        gp = dict(id="B%04d" % i, st=st, cd_base=int(rng.choice([0, 1, 2, 3, 4], p=cdp)), tol=float(rng.uniform(4.6, 5.6)),
                  recyc=float(rng.choice([0.15, 0.3, 0.45], p=[0.35, 0.35, 0.30])), pace=float(rng.uniform(*ST[st]["pace"])),
                  slip_k=2.5, fy_june=False)
        fc = qi(vint, int(rng.integers(1, 5)))
        out.append(dict(id=gp["id"], gp=gp, vint=vint, C=100.0, share=1.0, size=100.0, fc=fc, exp_fc=fc, seed=int(rng.integers(1, 2**31))))
    return out
