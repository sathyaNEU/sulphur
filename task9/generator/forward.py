"""task9: the truth for VR90's Q1 2027 quarter. The same physics world.py runs on the record, run forward on the ramp
plan's operating conditions (and on each condition changed). Each VR90 wafer's conditions are drawn once with common
random numbers (the same polisher, chamber, hour, tote, filter, bath and etch quantile and wafer draw in every scenario),
and each die's survival is the expectation over the mechanisms' own randomness, so a scenario's difference is the
condition's effect and nothing else. Nothing here is written to the pack, and the golden never reads it."""
import numpy as np

import params as P

COND_PLAN = dict(loop="slow", chem="summer", edge="plan", etch_clean=P.CLEAN_WAFERS)
COND_FIXED = dict(loop="spring", chem="spring", edge="none", etch_clean="no-flake")
CAUSES = (("loop", dict(loop="spring")), ("bath", dict(chem="spring")), ("edge", dict(edge="none")),
          ("etch", dict(etch_clean="no-flake")))


def bench_states(chem, lots_per_day, days=120, seed=0):
    """the tank's metal content at each batch, for a bench run at the loading and chemical life given"""
    rng = np.random.default_rng(P.SEED + 900 + seed)
    sched = P.SUMMER if chem == "summer" else P.SPRING
    d, c, since, next_change, out = 0.0, P.C_FRESH, 0, sched["change_h"] / 24.0, []
    while d < days:
        d += float(rng.exponential(1.0 / lots_per_day))
        while next_change <= d:
            c = P.C_FRESH * rng.lognormal(0, 0.15)
            since = 0
            next_change += sched["change_h"] / 24.0
        drag = P.DRAG_PPB * 25 * rng.lognormal(0, 0.18)
        out.append(c + 0.5 * drag)
        c += drag
        since += 1
        if since >= sched["spike_lots"]:
            f = P.SPIKE_L / P.BATH_L
            c = c * (1 - f) + P.C_FRESH * f
            since = 0
    return np.sort(np.array(out[200:]))


def no_flake_clean(share):
    load_vr = P.PRODUCTS["VR90"]["rf_s"] * P.CHEM["CT-DEEP-07"]
    return int(P.L_TH / (share * load_vr + (1 - share) * 89.5))


def etch_lams(clean, share, n_cycles=60, seed=0):
    """particle adder rate seen by each VR90 wafer on a chamber running VR90 at the share given, cleaned at the count
    given ('no-flake' cleans it before the polymer reaches the flaking load)"""
    rng = np.random.default_rng(P.SEED + 950 + seed)
    load_vr = P.PRODUCTS["VR90"]["rf_s"] * P.CHEM["CT-DEEP-07"]
    load_std = 89.5
    if clean == "no-flake":
        clean = no_flake_clean(share)
    out = []
    for _ in range(n_cycles):
        load = 0.0
        for k in range(int(clean)):
            vr = rng.random() < share
            if vr:
                excess = max(0.0, load - P.L_TH) / 1e4
                out.append(P.PRT_BASE + P.FLAKE_A * excess ** P.FLAKE_POW)
            load += (load_vr if vr else load_std) * rng.normal(1, 0.012)
    return np.sort(np.array(out)), int(clean)


_TOUCH = {}
_REG = {}


def region_areas(fab, name, k=6):
    """each die's area in each 40 mm clustering region (a large die spans several, as a block of small die does)"""
    if name in _REG:
        return _REG[name]
    g = fab.grids[name]
    u = (np.arange(k) + 0.5) / k
    xs = g.x0[:, None, None] + u[None, :, None] * g.w
    ys = g.y0[:, None, None] + u[None, None, :] * g.h
    xs, ys = np.broadcast_arrays(xs, ys)
    reg = (np.floor((xs + 160) / P.REGION_MM)).astype(int) * 16 + (np.floor((ys + 160) / P.REGION_MM)).astype(int)
    reg = reg.reshape(g.n, -1)
    out = []
    for d in range(g.n):
        vals, cnt = np.unique(reg[d], return_counts=True)
        out.append(cnt / cnt.sum() * g.area_cm2)
    _REG[name] = out
    return out


def touch_rate(fab, name, n=120000):
    """each die's chance of being touched by one micro-scratch (the record's own scratch geometry, simulated once)"""
    if name in _TOUCH:
        return _TOUCH[name]
    g = fab.grids[name]
    rng = np.random.default_rng(P.SEED + 990)
    hits = np.zeros(g.n)
    for dd in fab.scratch_dies(g, n, rng):
        hits[dd] += 1
    _TOUCH[name] = hits / n
    return _TOUCH[name]


def conditions(n, seed=0, fab=None):
    """one draw of every VR90 wafer's conditions, shared by every scenario; the deposition chamber and polisher pairs
    are drawn from the line's own dispatch of VX40 since the loop slowed (bay rules, downtime and all)"""
    rng = np.random.default_rng(P.SEED + 1000 + seed)
    pairs = [(e["ch"], e["cmp"]) for (lid, slot), e in sorted(fab.edge_of.items())
             if lid.startswith("VXA") and fab_lot_time(fab, lid) >= tday_vfd()]
    pick = rng.integers(0, len(pairs), n)
    ch = np.array([P.DEP_CHAMBERS.index(pairs[i][0]) for i in pick])
    # VR90 polishes ILD0 on CM1 and CM3 only, as VR90-T has (the shares VR90-T ran on since the loop slowed)
    tv = [L.tools["ILD0-CMP"] for L in fab.lots if L.tv and L.times.get("ILD0-CMP", -1) >= tday_vfd()]
    p_cm3 = sum(1 for t in tv if t == "CM3") / len(tv)
    u_cmp = np.where(rng.random(n) < p_cm3, P.CMP_TOOLS.index("CM3"), P.CMP_TOOLS.index("CM1"))
    return dict(ch=ch, u_cmp=u_cmp, hour=rng.uniform(0, 24, n), v_noise=rng.normal(0, 0.011, n), u_time=rng.random(n),
                tote=rng.uniform(0, 2.55, n), lpc_noise=rng.lognormal(0, 0.08, n), pou=rng.uniform(0, P.POU_DAYS + 1.5, n),
                edge_noise=rng.normal(0, P.EDGE_NOISE, n), u_bath=rng.random(n), u_etch=rng.random(n),
                gw=rng.gamma(P.ALPHA_WAFER, 1.0 / P.ALPHA_WAFER, n) * np.exp(rng.normal(0, P.DRIFT_WEEKS, n)))


def expected_yield(fab, cond, X, seed=0):
    g = fab.grids["VR90"]
    prod = P.PRODUCTS["VR90"]
    n = len(X["ch"])
    states = bench_states(cond["chem"], P.Q1_LOTS_PER_DAY, seed=seed)
    lams, clean = etch_lams(cond["etch_clean"], P.Q1_TV_SHARE, seed=seed)
    tr = touch_rate(fab, "VR90")
    ra = region_areas(fab, "VR90")
    prof = fab.edge_profile(g.rmax)
    area_mm2 = g.w * g.h
    t = fab.loop["t"]
    slow_t = t[(t >= tday_vfd()) & ((t < _td(P.T_STANDBY_ON)) | (t >= _td(P.T_STANDBY_OFF))) & (t < _td(P.SORT_TO))]
    spring_t = t[(t >= _td(P.SORT_FROM)) & (t < tday_vfd())]
    ys = np.zeros(n)
    loss = {m: np.zeros(n) for m in ("rand", "prt", "scr", "goi", "thick", "thin", "edgefall", "design")}
    for i in range(n):
        ch = P.DEP_CHAMBERS[int(X["ch"][i])]
        cmp_tool = P.CMP_TOOLS[int(X["u_cmp"][i])]
        # the loop as it ran: a moment of the record's slow period (from 2 June, standby fortnight excluded) or of its
        # spring (January to May), the same quantile in every scenario
        grid = slow_t if cond["loop"] == "slow" else spring_t
        tt = float(grid[min(int(X["u_time"][i] * len(grid)), len(grid) - 1)])
        lpc = float(fab.tap_lpc(cmp_tool, tt))
        pas = min(0.95, P.POU_PASS0 + P.POU_PASS_DAY * float(fab.pou_age(cmp_tool, tt)))
        lam_s = P.SCR_BASE * (lpc / P.SCR_REF) ** P.SCR_POW * pas * prod["polish_s"] / 60.0
        dep = P.CHAMBER_STATIC[ch] + (P.DP2B_EDGE if (ch == "DP2B" and cond["edge"] in ("plan", "today")) else 0.0)
        rem = P.CMP_STATIC[cmp_tool] + (P.CM3_EDGE if (cmp_tool == "CM3" and cond["edge"] == "today") else 0.0)
        net = (dep - rem + X["edge_noise"][i]) * prof
        c = float(states[min(int(X["u_bath"][i] * len(states)), len(states) - 1)])
        lam_p = float(lams[min(int(X["u_etch"][i] * len(lams)), len(lams) - 1)])
        p = {}
        p["rand"] = np.array([1 - np.prod((1 + P.D0 * a * X["gw"][i] / P.ALPHA_REGION) ** (-P.ALPHA_REGION)) for a in ra])
        p["prt"] = np.full(g.n, 1 - np.exp(-lam_p * area_mm2 / (np.pi * 150.0 ** 2) * P.PRT_KILL))
        p["scr"] = 1 - np.exp(-lam_s * tr * P.SCR_KILL)
        p["goi"] = np.full(g.n, P.GOI_K * prod["gate"] * max(0.0, c - P.C_TH) ** P.GOI_EXP + 0.0006 * prod["gate"])
        p["thick"] = P.KILL_THICK * (1 - np.exp(-np.maximum(0.0, net - P.TOL_THICK) / P.EDGE_SCALE))
        p["thin"] = P.KILL_THIN * (1 - np.exp(-np.maximum(0.0, -net - P.TOL_THIN) / P.EDGE_SCALE))
        p["edgefall"] = np.where(g.rmax > 145.0, 0.06, 0.0)
        p["design"] = np.full(g.n, 1 - prod["design"])
        surv = np.ones(g.n)
        for m, pm in p.items():
            pm = np.broadcast_to(pm, (g.n,))
            surv = surv * (1 - pm)
            loss[m][i] = float(np.mean(pm))
        ys[i] = float(surv.mean())
    return dict(yield_=float(ys.mean()), loss={m: float(v.mean()) for m, v in loss.items()}, clean=clean)


def fab_lot_time(fab, lid):
    if not hasattr(fab, "_lot_cmp_t"):
        fab._lot_cmp_t = {L.lid: L.times.get("ILD0-CMP", -1) for L in fab.lots}
    return fab._lot_cmp_t.get(lid, -1)


def _td(x):
    return (x - P.EPOCH).total_seconds() / 86400.0


def tday_vfd():
    return (P.T_VFD_DOWN - P.EPOCH).total_seconds() / 86400.0


def scenario_table(fab, n=4000, seed=0):
    """the plan, every cause removed, and each cause removed alone from the plan (marginal costs in yield points)"""
    X = conditions(n, seed, fab)
    out = {"plan": expected_yield(fab, COND_PLAN, X, seed), "fixed": expected_yield(fab, COND_FIXED, X, seed)}
    for name, change in CAUSES:
        out["minus_" + name] = expected_yield(fab, dict(COND_PLAN, **change), X, seed)
    out["cost"] = {name: 100 * (out["minus_" + name]["yield_"] - out["plan"]["yield_"]) for name, _ in CAUSES}
    return out
