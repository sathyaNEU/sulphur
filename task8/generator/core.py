"""task8 architecture 18: the main call's computations on the clean truth. The Board's bank runs, the default
path, the golden (each Level 2 item's shift for Level 1 candidates split between stem length and context on the
items earlier Level 1 papers borrowed, the link fixed by the model's intercept), every rival route, the truth, and
the two asks."""
import numpy as np

import params as P
import rasch as RA
import world as W

BANK_ORIGIN = -0.96     # the bank scale: the 2022 Level 1 paper's items average -0.96 logits (fixed in 2022)
L2_ORIGIN = 0.50        # the Level 2 calibration's own origin, the 2022 Level 2 paper's items


def rows_of(sittings, level=None, upto=None, year=None):
    out = []
    for j, s in enumerate(sittings):
        if level and s["level"] != level:
            continue
        if year and s["year"] != year:
            continue
        if upto and s["date"] > upto:
            continue
        out.append(j)
    return np.array(out, dtype=int)


def bank_runs(w):
    """The Board's concurrent calibration of every sitting, preliminary (to 30 June 2026) and final."""
    X, papers = w["X"], w["papers"]
    final = RA.jml(X, papers["L1-2022"], BANK_ORIGIN)
    keep = rows_of(w["sittings"], upto=P.PRELIM_CUTOFF)
    prelim = RA.jml(X[keep], papers["L1-2022"], BANK_ORIGIN, b0=final["b"])
    infit, outfit = RA.fit(X, final["theta"], final["b"])
    return dict(final=final, prelim=prelim, infit=infit, outfit=outfit, prelim_rows=keep)


def standard_theta(b, papers):
    return RA.solve_tcc(b[papers["L1-2022"]], P.STANDARD_RAW)


def expected(b, idx, theta):
    return RA.tcc(b[idx], theta)


def default_path(w, bank):
    b = bank["final"]["b"]
    th = standard_theta(b, w["papers"])
    e = expected(b, w["papers"]["L1-2027"], th)
    return dict(theta=th, expected=e, pass_mark=int(round(e)), b=b)


def level_runs(w):
    """Each level calibrated on its own sittings: Level 1 on the bank's origin, Level 2 on its own."""
    X, papers, s = w["X"], w["papers"], w["sittings"]
    r1, r2 = rows_of(s, "L1"), rows_of(s, "L2")
    c1 = RA.jml(X[r1], papers["L1-2022"], BANK_ORIGIN)
    c2 = RA.jml(X[r2], papers["L2-2022"], L2_ORIGIN)
    return dict(l1=c1, l2=c2, r1=r1, r2=r2)


def bridging(w):
    s = w["it"]["sets"]
    return np.concatenate([s["sp"], s["sa"], s["lp"]])


def shift_table(w, lv):
    """Each bridging item's Level 1 difficulty less its Level 2 difficulty, with its stem length and context."""
    br = bridging(w)
    it = w["it"]
    d = lv["l1"]["b"][br] - lv["l2"]["b"][br]
    se = np.sqrt(lv["l1"]["se"][br] ** 2 + lv["l2"]["se"][br] ** 2)
    return dict(items=br, d=d, se=se, words=it["words"][br].astype(float), everyday=it["everyday"][br].astype(float))


def fit_shift(tab, form="linear", weighted=True, terms=("words", "everyday")):
    """Least squares of the shift on an intercept (the link between the two calibrations) and the named causes."""
    cols = [np.ones_like(tab["d"])]
    for t in terms:
        if t == "words":
            x = tab["words"] / 100.0
            if form == "log":
                x = np.log(tab["words"])
            elif form == "step":
                x = (tab["words"] >= 80).astype(float)
            cols.append(x)
        else:
            cols.append(-tab["everyday"])
    A = np.column_stack(cols)
    wt = 1.0 / tab["se"] ** 2 if weighted else np.ones_like(tab["d"])
    sw = np.sqrt(wt)
    coef = np.linalg.lstsq(A * sw[:, None], tab["d"] * sw, rcond=None)[0]
    resid = tab["d"] - A @ coef
    return dict(coef=coef, form=form, terms=terms, resid=resid)


def predict_shift(m, words, everyday):
    out = np.full(len(words), m["coef"][0], dtype=float)
    k = 1
    for t in m["terms"]:
        if t == "words":
            x = np.asarray(words, dtype=float) / 100.0
            if m["form"] == "log":
                x = np.log(np.asarray(words, dtype=float))
            elif m["form"] == "step":
                x = (np.asarray(words) >= 80).astype(float)
            out = out + m["coef"][k] * x
        else:
            out = out - m["coef"][k] * np.asarray(everyday, dtype=float)
        k += 1
    return out


def l1_difficulties(w, lv, m):
    """Difficulty for a Level 1 candidate of every item the 2027 paper carries: Level 1 items from the Level 1
    calibration, borrowed items from the Level 2 calibration plus the modelled shift."""
    it = w["it"]
    b = lv["l1"]["b"].copy()
    pr = it["sets"]["pr"]
    b[pr] = lv["l2"]["b"][pr] + predict_shift(m, it["words"][pr], it["everyday"][pr])
    return b


def golden(w, lv=None, form="linear", weighted=True):
    lv = lv or level_runs(w)
    tab = shift_table(w, lv)
    m = fit_shift(tab, form=form, weighted=weighted)
    b = l1_difficulties(w, lv, m)
    th = standard_theta(b, w["papers"])
    e = expected(b, w["papers"]["L1-2027"], th)
    return dict(theta=th, expected=e, pass_mark=int(round(e)), b=b, model=m, tab=tab, lv=lv)


def rival_terms(w, lv, terms):
    tab = shift_table(w, lv)
    m = fit_shift(tab, terms=terms)
    b = l1_difficulties(w, lv, m)
    th = standard_theta(b, w["papers"])
    e = expected(b, w["papers"]["L1-2027"], th)
    return dict(expected=e, pass_mark=int(round(e)), model=m)


def rival_screen(w, lv, z_cut=2.0):
    """The displacement screen: link the Level 2 calibration on the bridging items, flag those whose shift sits
    more than z_cut robust deviations from the median, re-link on the rest and carry the borrowed items over."""
    tab = shift_table(w, lv)
    d = tab["d"]
    med = np.median(d)
    mad = 1.4826 * np.median(np.abs(d - med))
    keep = np.abs(d - med) <= z_cut * mad
    link = float(np.average(d[keep], weights=1 / tab["se"][keep] ** 2))
    it = w["it"]
    b = lv["l1"]["b"].copy()
    pr = it["sets"]["pr"]
    b[pr] = lv["l2"]["b"][pr] + link
    th = standard_theta(b, w["papers"])
    e = expected(b, w["papers"]["L1-2027"], th)
    return dict(expected=e, pass_mark=int(round(e)), flagged=tab["items"][~keep], link=link)


def truth(w):
    """A candidate who just meets the standard, over the Level 1 population's regions: expected marks under the
    generating model on the 2022 and 2027 papers."""
    it, papers = w["it"], w["papers"]
    shares = np.array([r[3] for r in P.REGIONS])
    shares = shares / shares.sum()

    def mix_tcc(idx, th):
        tot = 0.0
        for (rc, _, _, _, _, dr), sh in zip(P.REGIONS, shares):
            d = it["b"][idx] + W.l1_shift(it, idx, dr)
            tot += sh * W.sig(th - d).sum()
        return float(tot)
    lo, hi = -8.0, 8.0
    for _ in range(80):
        m = 0.5 * (lo + hi)
        if mix_tcc(papers["L1-2022"], m) < P.STANDARD_RAW:
            lo = m
        else:
            hi = m
    th = 0.5 * (lo + hi)
    e = mix_tcc(papers["L1-2027"], th)
    per_item = {}
    for i in papers["L1-2027"]:
        per_item[int(i)] = mix_tcc(np.array([i]), th)
    return dict(theta=th, expected=e, pass_mark=int(round(e)), per_item=per_item)


# ---- ask B: each region's 2026 Level 1 candidates on the 2027 paper -------------------------------------------

def region_index(w, rows):
    regs = [r[0] for r in P.REGIONS]
    return np.array([regs.index(w["sittings"][j]["region"]) for j in rows])


def regional_model(w, lv, outer=12):
    """Level 1 calibration with each region's everyday-context deviation (centred on the Level 1 sittings' regional
    shares): difficulty of everyday item i for a candidate in region r is b_i - delta_r."""
    X, papers, s = w["X"], w["papers"], w["sittings"]
    r1 = lv["r1"]
    Xr = X[r1]
    reg = region_index(w, r1)
    ev = w["it"]["everyday"].astype(float)
    nreg = len(P.REGIONS)
    share = np.bincount(reg, minlength=nreg) / len(reg)
    delta = np.zeros(nreg)
    b0 = lv["l1"]["b"]
    for _ in range(outer):
        off = -delta[reg][:, None] * ev[None, :]
        c = RA.jml(Xr, papers["L1-2022"], BANK_ORIGIN, offset=off, b0=b0, iters=200)
        b0 = c["b"]
        th = c["theta"]
        ok = ~np.isnan(th)
        Xz = np.where(np.isnan(Xr), 0.0, Xr)
        M = (~np.isnan(Xr)).astype(float) * (~np.isnan(b0))[None, :]
        p = W.sig(th[:, None] - np.nan_to_num(b0)[None, :] - off)
        g = ((Xz - p) * M * ev[None, :])
        h = (p * (1 - p) * M * ev[None, :])
        for r in range(nreg):
            sel = ok & (reg == r)
            delta[r] += g[sel].sum() / max(h[sel].sum(), 1e-9)
        delta -= (share * delta).sum()
    return dict(b=b0, delta=delta, share=share)


def region_means(w, b_l1, b_pr, delta=None, est="wle", k=1.0):
    """Mean expected mark on the 2027 paper of each region's 2026 Level 1 sitters (region of the centre sat at).
    b_l1: Level 1 difficulties (Level 1 items and the 2026 paper's borrowed items); b_pr: the borrowed 2027 items'
    Level 1 difficulties; delta: regional everyday deviations or None (pooled)."""
    X, papers = w["X"], w["papers"]
    rows = rows_of(w["sittings"], "L1", year=2026)
    reg = region_index(w, rows)
    ev = w["it"]["everyday"].astype(float)
    p26 = papers["L1-2026"]
    p27 = papers["L1-2027"]
    pr = w["it"]["sets"]["pr"]
    b = b_l1.copy()
    b[pr] = b_pr
    sub = np.full((len(rows), X.shape[1]), np.nan)
    sub[:, p26] = X[np.ix_(rows, p26)]
    if k != 1.0:   # a scale contracted about the 2026 paper's centre (the joint-likelihood stretch undone)
        cen = np.nanmean(b[p26])
        b = cen + k * (b - cen)
    dl = np.zeros(len(P.REGIONS)) if delta is None else delta
    off = -dl[reg][:, None] * ev[None, :]
    if est == "wle":
        th = RA.wle(sub, b, offset=off)
    else:          # maximum likelihood, every 2026 sitter scored between 0 and 40 exclusive
        th = np.zeros(len(rows))
        for _ in range(60):
            p = W.sig(th[:, None] - b[None, p26] - off[:, p26])
            th = np.clip(th + (sub[:, p26] - p).sum(1) / (p * (1 - p)).sum(1), -6, 6)
    e = np.array([W.sig(th[k] - b[p27] - off[k, p27]).sum() for k in range(len(rows))])
    out = {}
    for r, reg_row in enumerate(P.REGIONS):
        sel = reg == r
        out[reg_row[0]] = (float(e[sel].mean()), int(sel.sum()))
    return out


def region_truth(w):
    it, papers = w["it"], w["papers"]
    rows = rows_of(w["sittings"], "L1", year=2026)
    p27 = papers["L1-2027"]
    dl = {r[0]: r[5] for r in P.REGIONS}
    out = {}
    for rc in dl:
        vals = []
        for j in rows:
            s = w["sittings"][j]
            if s["region"] != rc:
                continue
            d = it["b"][p27] + W.l1_shift(it, p27, dl[rc])
            vals.append(W.sig(s["theta"] - d).sum())
        out[rc] = float(np.mean(vals))
    return out


def compute(w, with_mml=True):
    bank = bank_runs(w)
    dp = default_path(w, bank)
    lv = level_runs(w)
    g = golden(w, lv)
    t = truth(w)
    r_screen = rival_screen(w, lv)
    r_ctx = rival_terms(w, lv, ("everyday",))
    r_read = rival_terms(w, lv, ("words",))
    variants = {"log": golden(w, lv, form="log")["expected"], "step": golden(w, lv, form="step")["expected"],
                "unweighted": golden(w, lv, weighted=False)["expected"]}
    # ask A: each 2027 item's chance at the standard under the golden
    p27 = w["papers"]["L1-2027"]
    chances = {int(i): float(W.sig(g["theta"] - g["b"][i])) for i in p27}
    # ask B: regions
    regm = regional_model(w, lv)
    tab = shift_table(w, dict(l1=dict(b=regm["b"], se=lv["l1"]["se"]), l2=lv["l2"]))
    mreg = fit_shift(tab)
    b_pr_reg = lv["l2"]["b"][w["it"]["sets"]["pr"]] + predict_shift(mreg, w["it"]["words"][w["it"]["sets"]["pr"]],
                                                                     w["it"]["everyday"][w["it"]["sets"]["pr"]])
    reg_golden = region_means(w, regm["b"], b_pr_reg, regm["delta"])
    reg_family = {"mle": region_means(w, regm["b"], b_pr_reg, regm["delta"], est="mle"),
                  "stretch_39_40": region_means(w, regm["b"], b_pr_reg, regm["delta"], k=39 / 40),
                  "stretch_0.93": region_means(w, regm["b"], b_pr_reg, regm["delta"], k=0.93)}
    reg_pooled = region_means(w, g["b"], g["b"][w["it"]["sets"]["pr"]], None)
    reg_bank = region_means(w, dp["b"], dp["b"][w["it"]["sets"]["pr"]], None)
    reg_true = region_truth(w)
    out = dict(bank=bank, default=dp, lv=lv, gold=g, truth=t, screen=r_screen, ctx=r_ctx, read=r_read,
               variants=variants, chances=chances, regm=regm, reg_golden=reg_golden, reg_pooled=reg_pooled,
               reg_bank=reg_bank, reg_true=reg_true, reg_family=reg_family)
    if with_mml:
        X = w["X"]
        m1 = RA.mml(X[lv["r1"]], w["papers"]["L1-2022"], BANK_ORIGIN)
        m2 = RA.mml(X[lv["r2"]], w["papers"]["L2-2022"], L2_ORIGIN)
        lvm = dict(l1=dict(b=m1, se=lv["l1"]["se"]), l2=dict(b=m2, se=lv["l2"]["se"]), r1=lv["r1"], r2=lv["r2"])
        out["mml"] = golden(w, lvm)["expected"]
    return out
