"""The analyst's routes on the clean panel (before any export mess), used to price the ladder and the rivals.

Every route reads only what the shipped pack will carry: household-week category litres and Northvale litres,
each household's purchases by brand family before launch (its price paid per litre), the banner of its first
Northvale purchase, the trade calendar's promoted weeks, the media plan's weeks, and the panel's membership.
Nothing here reads the latent tier, the phases or the floors."""
import numpy as np

import world as W

RECENT = (W.widx(W.dt.date.fromisocalendar(2026, 38, 1)), W.T_END)        # the last seven delivered weeks
PRE = (W.widx(W.dt.date.fromisocalendar(2025, 1, 1)), W.T_LAUNCH - 1)      # 2025-W01 to 2026-W14
PRE_LONG = (0, W.T_LAUNCH - 1)


def brand_counts(S, seed=W.SEED + 9):
    """Pre-launch occasions split across brand families by each household's preference; PL is the banner's own
    label, so its availability follows the banner mix (every banner but the natural grocer carries one)."""
    H = S['H']
    rng = np.random.default_rng(seed)
    n = H['n']
    occ_pre = S['occ'][PRE_LONG[0]:PRE_LONG[1] + 1].sum(0)
    p = H['pref'].copy()
    natural = H['mix'][:, W.B_CODE.index('GLM')]
    p[:, -1] *= (1 - natural)
    p = p / p.sum(1, keepdims=True)
    counts = np.vstack([rng.multinomial(occ_pre[i], p[i]) if occ_pre[i] > 0 else np.zeros(W.NBR, int)
                        for i in range(n)])
    price = np.array([b[2] for b in W.BRANDS])
    ppl = np.divide((counts * price).sum(1), counts.sum(1), out=np.full(n, np.nan), where=counts.sum(1) > 0)
    pl_share = np.divide(counts[:, -1], counts.sum(1), out=np.full(n, np.nan), where=counts.sum(1) > 0)
    return counts, ppl, pl_share


def base(S):
    H = S['H']
    lit = H['litres_occ']
    cat = S['occ'] * lit[None, :]
    nvl = S['nv'] * H['nv_litres'][None, :]
    static = (H['join'] <= PRE_LONG[0]) & (H['leave'] > W.T_END)
    buyer = static & (S['occ'][:W.T_END + 1].sum(0) > 0)
    return lit, cat, nvl, static, buyer


def share(nvl, cat, a, b, mask):
    return nvl[a:b + 1, mask].sum() / cat[a:b + 1, mask].sum()


def fit_trial(S, mask):
    """Cumulative trial among category buyers by week since launch, a modified exponential fitted to it."""
    from scipy.optimize import curve_fit
    tr = S['tried']
    weeks = np.arange(W.T_LAUNCH, W.T_END + 1)
    cum = np.array([((tr >= 0) & (tr <= t) & mask).sum() / mask.sum() for t in weeks])
    f = lambda k, a, b: a * (1 - np.exp(-b * (k + 1)))
    (a, b), _ = curve_fit(f, weeks - W.T_LAUNCH, cum, p0=(0.3, 0.05), maxfev=20000)
    k27 = np.arange(W.T27_0, W.T27_1 + 1) - W.T_LAUNCH
    return cum[-1], a, f(k27, a, b).mean()


def tenure_curves(S, tier_hat, buyer, max_k=29, exclude_promo=True):
    """Each rebuilt tier's share of its triers' category litres by weeks since their own first purchase (the
    first purchase itself excluded, promoted weeks excluded), pooled over every trier cohort."""
    H = S['H']
    lit = H['litres_occ']
    tr = S['tried']
    num = np.zeros((3, max_k + 1)); den = np.zeros((3, max_k + 1))
    promo_any = W.PROMO[:W.T_END + 1].any(1)
    for t in range(W.T_LAUNCH, W.T_END + 1):
        if exclude_promo and promo_any[t]:
            continue
        ten = t - tr
        ok = buyer & (tr >= 0) & (ten >= 1) & (ten <= max_k)
        for k in range(3):
            m = ok & (tier_hat == k)
            np.add.at(num[k], ten[m], (S['nv'][t, m]) * lit[m])
            np.add.at(den[k], ten[m], S['occ'][t, m] * lit[m])
    return num, den


def fit_curve(num, den, k_min=1):
    """s(k) = f + (s0 - f) exp(-k / tau), weighted least squares on the pooled tenure curve."""
    from scipy.optimize import curve_fit
    k = np.arange(len(num))
    ok = (den > 0) & (k >= k_min)
    y = num[ok] / den[ok]
    w = np.sqrt(den[ok])
    g = lambda kk, f, s0, tau: f + (s0 - f) * np.exp(-kk / tau)
    (f, s0, tau), _ = curve_fit(g, k[ok], y, p0=(y[-5:].mean(), y[:3].mean(), 6.0), sigma=1 / w,
                                bounds=([0, 0, 0.5], [1, 1, 60]), maxfev=20000)
    return f, s0, tau


def golden_curve(S, tier_hat, buyer, vol_week, curves=None):
    """The 2027 share with each trier carried on its tier's fitted curve at its own 2027 tenure, the households
    still to try entering at their tier's everyday hazard, and every household's weekly litres from vol_week."""
    tr = S['tried']
    if curves is None:
        num, den = tenure_curves(S, tier_hat, buyer)
        curves = [fit_curve(num[k], den[k]) for k in range(3)]
    ev_weeks = [t for t in range(W.T_LAUNCH + 6, W.T_END + 1) if not W.MEDIA[t] and not W.PROMO[t].any()]
    haz = []
    for k in range(3):
        at_risk = sum((((tr < 0) | (tr >= t)) & buyer & (tier_hat == k)).sum() for t in ev_weeks)
        hits = sum(((tr == t) & buyer & (tier_hat == k)).sum() for t in ev_weeks)
        haz.append(hits / at_risk)
    num = 0.0
    den = 0.0
    seas = W.SEAS; grow = W.GROW
    p_un = np.where(tr >= 0, 0.0, 1.0)
    entries = []
    for t in range(W.T_END + 1, W.T27_1 + 1):
        h = np.array(haz)[tier_hat]
        new = p_un * h * buyer
        p_un = p_un - new
        entries.append((t, new))
        if t < W.T27_0:
            continue
        v = vol_week * seas[t] * grow[t] / grow[W.T_END]
        den += v[buyer].sum()
        f = np.array([c[0] for c in curves])[tier_hat]; s0 = np.array([c[1] for c in curves])[tier_hat]
        tau = np.array([c[2] for c in curves])[tier_hat]
        ten = t - tr
        s = np.where((tr >= 0) & buyer, f + (s0 - f) * np.exp(-ten / tau), 0.0)
        num += (s * v).sum()
        for (t0, mass) in entries:
            if t0 == t:
                num += (mass * v).sum() * 0.0
            else:
                num += (mass * (f + (s0 - f) * np.exp(-(t - t0) / tau)) * v).sum()
    return num / den, curves, haz


def tier_cut(ppl, buyer, how):
    """Rebuilt price tier from the price paid per litre before launch: 0 premium, 1 mainstream, 2 value."""
    ok = buyer & np.isfinite(ppl)
    if how == 'terciles':
        q1, q2 = np.nanquantile(ppl[ok], [1 / 3, 2 / 3])
    elif how == 'q30':                # 30/40/30 cut
        q1, q2 = np.nanquantile(ppl[ok], [0.30, 0.70])
    elif how == 'gaps':               # the two widest gaps in the price-per-litre distribution
        q1, q2 = 2.20, 2.95
    else:
        raise ValueError(how)
    return np.where(ppl >= q2, 0, np.where(ppl >= q1, 1, 2))


def settled_floors(S, tier_hat, buyer, k_min, weeks=None):
    """Each rebuilt tier's share of its triers' category litres over everyday weeks at tenure k_min or more."""
    lit = S['H']['litres_occ']
    tr = S['tried']
    promo_any = W.PROMO[:W.T_END + 1].any(1)
    weeks = weeks or [t for t in range(W.T_LAUNCH, W.T_END + 1) if not promo_any[t]]
    num = np.zeros(3); den = np.zeros(3)
    for t in weeks:
        ok = buyer & (tr >= 0) & (t - tr >= k_min)
        for k in range(3):
            m = ok & (tier_hat == k)
            num[k] += (S['nv'][t, m] * S['H']['nv_litres'][m]).sum()
            den[k] += (S['occ'][t, m] * lit[m]).sum()
    return np.divide(num, den, out=np.zeros(3), where=den > 0), den


def replay(S, tier_hat, buyer, floors, vol):
    """2027 share with every household that has bought the line carried at its tier's settled share, the
    households still to try left out (no support in 2027), each household weighted by vol."""
    tr = S['tried']
    fl = np.asarray(floors)[tier_hat]
    return (np.where((tr >= 0) & buyer, fl, 0.0) * vol)[buyer].sum() / vol[buyer].sum()


def family(S):
    """The golden family (advisor point 5): tier cut x floor tenure x volume base, and the shallow routes."""
    H = S['H']
    lit, cat, nvl, static, buyer = base(S)
    _, ppl, _ = brand_counts(S)
    out = {}
    vols = {'v2425': cat[0:104].sum(0) / 104.0, 'v2025': cat[52:104].sum(0) / 52.0,
            'vall': cat[0:W.T_END + 1].sum(0) / (W.T_END + 1),
            'v52': cat[W.T_END - 51:W.T_END + 1].sum(0) / 52.0,
            'vwin': cat[W.T_LAUNCH:W.T_END + 1].sum(0) / (W.T_END - W.T_LAUNCH + 1)}
    for how in ('terciles', 'q30', 'gaps'):
        th = tier_cut(ppl, buyer, how)
        for k_min in (14, 16, 20):
            fl, den = settled_floors(S, th, buyer, k_min)
            for vn, v in vols.items():
                out[(how, k_min, vn)] = replay(S, th, buyer, fl, v)
            out[('floors', how, k_min)] = fl
            out[('floor_den', how, k_min)] = den
    tr = S['tried']
    a, b = RECENT
    cw = cat[a:b + 1].sum(0); nw = nvl[a:b + 1].sum(0)
    triers = buyer & (tr >= 0)
    mature = triers & (tr <= W.T_LAUNCH + 3)
    R_mat = nw[mature].sum() / cw[mature].sum()
    R_cur = nw[triers].sum() / cw[triers].sum()
    for vn in ('v2425', 'vwin'):
        v = vols[vn]
        out[('mature_all', vn)] = (np.where(triers, R_mat, 0.0) * v)[buyer].sum() / v[buyer].sum()
        # per-cohort: each four-week trial cohort at its own recent share
        rc = np.zeros(H['n'])
        for c0 in range(W.T_LAUNCH, W.T_END + 1, 4):
            m = triers & (tr >= c0) & (tr < c0 + 4)
            if cw[m].sum() > 0:
                rc[m] = nw[m].sum() / cw[m].sum()
        out[('cohort', vn)] = (rc * v)[buyer].sum() / v[buyer].sum()
    P_now = triers.sum() / buyer.sum()
    B_win = vols['vwin'][triers].mean() / vols['vwin'][buyer].mean()
    B_pre = vols['v2425'][triers].mean() / vols['v2425'][buyer].mean()
    out['pc_naive'] = P_now * R_cur * B_win
    out['pc_careful'] = P_now * R_mat * B_win
    out['pc_B1'] = P_now * R_mat * 1.0
    out['recent'] = nw[buyer].sum() / cw[buyer].sum()
    out['B_win'], out['B_pre'], out['R_mat'], out['R_cur'], out['P_now'] = B_win, B_pre, R_mat, R_cur, P_now
    return out


def routes(S, verbose=True):
    H = S['H']
    lit, cat, nvl, static, buyer = base(S)
    tr = S['tried']
    a, b = RECENT
    out = {}
    weekly = [share(nvl, cat, t, t, buyer) for t in range(W.T_LAUNCH, W.T_END + 1)]
    out['weekly'] = weekly
    out['R0_recent'] = share(nvl, cat, a, b, buyer)
    P_now, P_inf, P27 = fit_trial(S, buyer)
    out['P_now'], out['P_inf'], out['P27'] = P_now, P_inf, P27
    triers = buyer & (tr >= 0)
    cw = cat[a:b + 1].sum(0)
    nw = nvl[a:b + 1].sum(0)
    R_cur = nw[triers].sum() / cw[triers].sum()
    win = (W.T_LAUNCH, W.T_END)
    cwin = cat[win[0]:win[1] + 1].sum(0)
    B_win = cwin[triers].mean() / cwin[buyer].mean()
    mature = triers & (tr <= W.T_LAUNCH + 3)
    R_mat = nw[mature].sum() / cw[mature].sum()
    out.update(R_cur=R_cur, R_mat=R_mat, B_win=B_win)
    out['R1_pc_naive'] = P_inf * R_cur * B_win
    out['R1b_pc_naive27'] = P27 * R_cur * B_win
    out['R2_pc_careful'] = P27 * R_mat * B_win
    cpre = cat[PRE[0]:PRE[1] + 1].sum(0)
    B_pre = cpre[triers].mean() / cpre[buyer].mean()
    out['B_pre'] = B_pre
    out['R2_B1'] = P27 * R_mat * 1.0
    # tiers rebuilt from the price paid per litre before launch (terciles among category buyers)
    counts, ppl, pl_share = brand_counts(S)
    ok = buyer & np.isfinite(ppl)
    q1, q2 = np.nanquantile(ppl[ok], [1 / 3, 2 / 3])
    tier_hat = np.where(ppl >= q2, 0, np.where(ppl >= q1, 1, 2))
    out['tier_agree'] = (tier_hat[ok] == H['tier'][ok]).mean()
    ten_end = np.where(tr >= 0, b - tr, -1)
    # floor by rebuilt tier: triers with at least 16 weeks since their own first purchase, their recent share
    floors = []
    for k in range(3):
        m = triers & (tier_hat == k) & (ten_end >= 16)
        floors.append(nw[m].sum() / cw[m].sum() if cw[m].sum() > 0 else 0.0)
    out['floors_hat'] = floors
    # organic trial hazard by tier: everyday weeks with no media, households still untried
    ev_weeks = [t for t in range(W.T_LAUNCH + 6, W.T_END + 1) if not W.MEDIA[t] and not W.PROMO[t].any()]
    haz = []
    for k in range(3):
        at_risk = sum((((tr < 0) | (tr >= t)) & buyer & (tier_hat == k)).sum() for t in ev_weeks)
        hits = sum(((tr == t) & buyer & (tier_hat == k)).sum() for t in ev_weeks)
        haz.append(hits / at_risk)
    out['haz'] = haz
    weeks_to_mid27 = (W.T27_0 + W.T27_1) / 2 - W.T_END

    def project(floor_by, vol, use_tier):
        num, den = 0.0, vol[buyer].sum()
        for k in range(3):
            m_t = triers & (tier_hat == k) if use_tier else triers & (tier_hat == k)
            fl = floor_by[k]
            num += fl * vol[m_t].sum()
            m_n = buyer & (tr < 0) & (tier_hat == k)
            gain = 1 - (1 - haz[k]) ** weeks_to_mid27
            num += fl * vol[m_n].sum() * gain
        return num / den
    g = W.GROW[(W.T27_0 + W.T27_1) // 2]
    vol_win = cwin / (win[1] - win[0] + 1)
    vol_pre = cpre / (PRE[1] - PRE[0] + 1)
    out['RS1_only'] = project(floors, vol_win, True)
    out['RS2_only'] = project([R_mat] * 3, vol_pre, True)
    out['golden'] = project(floors, vol_pre, True)
    # trier volume against its own pre-launch rate, beside non-triers
    nontr = buyer & (tr < 0)
    out['trier_ratio'] = (cwin[triers].sum() / (win[1] - win[0] + 1)) / (cpre[triers].sum() / (PRE[1] - PRE[0] + 1))
    out['nontr_ratio'] = (cwin[nontr].sum() / (win[1] - win[0] + 1)) / (cpre[nontr].sum() / (PRE[1] - PRE[0] + 1))
    # tier mix by litres: the mature cohort against every trier
    out['mix_mature'] = [cw[mature & (H['tier'] == k)].sum() / cw[mature].sum() for k in range(3)]
    out['mix_triers'] = [cw[triers & (H['tier'] == k)].sum() / cw[triers].sum() for k in range(3)]
    # rival volume bases for the buying index: last 52 weeks, the whole history, calendar 2025
    def vol_over(a0, a1):
        return cat[a0:a1 + 1].sum(0) / (a1 - a0 + 1)
    v52 = vol_over(W.T_END - 51, W.T_END)
    vall = vol_over(0, W.T_END)
    v25 = vol_over(52, 103)
    out['RS1_vol52'] = project(floors, v52, True)
    out['RS1_volall'] = project(floors, vall, True)
    out['golden_v25'] = project(floors, v25, True)
    # the golden route: fitted tenure curves per rebuilt tier, 2024-25 litres grown to 2027
    v_pre_wk = cat[0:104].sum(0) / 104.0 * (W.GROW[W.T_END] / W.GROW[52])
    out['golden_curve'], out['curves'], out['haz_c'] = golden_curve(S, tier_hat, buyer, v_pre_wk)
    v_win_wk = cwin / (win[1] - win[0] + 1) * (1.0 / W.SEAS[W.T_LAUNCH:W.T_END + 1].mean())
    out['curve_winvol'], _, _ = golden_curve(S, tier_hat, buyer, v_win_wk, out['curves'])
    v52_wk = cat[W.T_END - 51:W.T_END + 1].sum(0) / 52.0
    out['curve_vol52'], _, _ = golden_curve(S, tier_hat, buyer, v52_wk, out['curves'])
    vall_wk = cat[0:W.T_END + 1].sum(0) / (W.T_END + 1) * (W.GROW[W.T_END] / W.GROW[W.T_END // 2])
    out['curve_volall'], _, _ = golden_curve(S, tier_hat, buyer, vall_wk, out['curves'])
    # per-cohort route: each four-week trial cohort carried at its own recent share, window volumes and pre volumes
    num_w = num_p = 0.0
    for c0 in range(W.T_LAUNCH, W.T_END + 1, 4):
        m = triers & (tr >= c0) & (tr < c0 + 4)
        if cw[m].sum() == 0:
            continue
        rc = nw[m].sum() / cw[m].sum()
        num_w += rc * vol_win[m].sum()
        num_p += rc * vol_pre[m].sum()
    # new triers at the latest cohort's share
    out['cohort_win'] = num_w / vol_win[buyer].sum()
    out['cohort_pre'] = num_p / vol_pre[buyer].sum()
    # trial banner route: floors by the channel of the first purchase (discount or not)
    disc_tr = triers & np.isin(S['trial_banner'], np.nonzero(W.DISCOUNT)[0])
    out['disc_trier_share'] = disc_tr.sum() / triers.sum()
    if verbose:
        T = W.truth_2027(S)
        out['truth'] = T['share']
        print('truth 2027: %.2f%%' % (100 * T['share']))
        print('weekly share W15-W44:', ' '.join('%.1f' % (100 * x) for x in weekly))
        for k in ['R0_recent', 'R1_pc_naive', 'R1b_pc_naive27', 'R2_pc_careful', 'R2_B1', 'RS1_only', 'RS1_vol52',
                  'RS1_volall', 'RS2_only', 'cohort_win', 'cohort_pre', 'golden', 'golden_v25']:
            print('  %-15s %.2f%%' % (k, 100 * out[k]))
        print('  P now %.3f inf %.3f 2027 %.3f | R_cur %.3f R_mat %.3f | B_win %.2f B_pre %.2f' % (
            P_now, P_inf, P27, R_cur, R_mat, B_win, B_pre))
        print('  floors_hat', np.round(floors, 4), 'haz', np.round(haz, 4), 'tier agreement %.2f' % out['tier_agree'])
        print('  trier litres vs own pre-launch %.3f, non-triers %.3f' % (out['trier_ratio'], out['nontr_ratio']))
        print('  tier mix by litres: mature', np.round(out['mix_mature'], 2), 'all triers', np.round(out['mix_triers'], 2))
        print('  triers %d of %d buyers (%.1f%%), discount-banner first purchase %.2f' % (
            triers.sum(), buyer.sum(), 100 * triers.sum() / buyer.sum(), out['disc_trier_share']))
    return out


if __name__ == '__main__':
    import sys
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else W.SEED
    routes(W.simulate(seed))
