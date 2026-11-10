"""task5 architecture 4: the State of Franklin's employers and their unemployment insurance filings, 2023 to 2026.

The clean truth, simulated as the process that makes the Division's files: every employer's monthly jobs (pay period
including the 12th) and where its worksites are; how each files (a payroll agent's transmission, the web portal,
paper) and when each quarterly report and each worksite report reached the Division; the 2026 housing downturn, which
every county carries by its industry mix; employers in trouble (closed without a word, or cut back and filed late);
new employers and when the Division set up their accounts; and the Division's account maintenance (inactivations
after two quarters without a report, closures on notice, transfers to a successor). One random stream per component,
so tuning one leaves the others' draws unchanged."""
import datetime as dt
import math

import numpy as np

import world as W

STREAMS = {"pop": 1, "industry": 2, "channel": 3, "paths": 4, "distress": 5, "births": 6, "timing": 7,
           "amend": 8, "maint": 9, "worksites": 10, "names": 11, "bust": 12, "season": 13, "switch": 14,
           "reg": 15, "mwr": 16, "sites": 17}

REG_PROMPT, REG_REPORT, REG_FOUND = 1, 2, 3
# a new employer registers ahead of its first report, with it, or only once the Division finds it
REG_SHARES = (0.28, 0.62, 0.10)
REG_SIZE = {REG_PROMPT: [0.50, 0.28, 0.15, 0.07], REG_REPORT: [0.64, 0.24, 0.09, 0.03], REG_FOUND: [0.74, 0.20, 0.05, 0.01]}
BASE_HAZARD = np.array([0.022, 0.014, 0.008, 0.0045, 0.0016, 0.0005, 0.0, 0.0])
ORDERLY = np.array([0.036, 0.031, 0.009, 0.002, 0.0, 0.0, 0.0, 0.0])
P_CEASE = 0.64
# a lake worksite's month against its year (leisure and retail), and outdoor work in the North Woods
LEISURE_LAKE = np.array([0.45, 0.45, 0.50, 0.62, 0.92, 1.26, 1.42, 1.40, 1.10, 0.70, 0.50, 0.46])
RETAIL_LAKE = np.array([0.82, 0.80, 0.82, 0.88, 1.00, 1.15, 1.25, 1.24, 1.05, 0.92, 0.86, 0.88])
OUTDOOR_NORTH = np.array([0.72, 0.70, 0.80, 0.98, 1.10, 1.15, 1.16, 1.15, 1.10, 1.04, 0.92, 0.78])
# winter recreation in the North Woods, and the holiday trade at the metro's stores
WINTER_NORTH = np.array([1.52, 1.50, 1.28, 0.88, 0.70, 0.74, 0.84, 0.86, 0.76, 0.80, 0.98, 1.38])
HOLIDAY_METRO = np.array([0.95, 0.93, 0.94, 0.96, 0.98, 1.00, 1.00, 1.01, 0.98, 1.01, 1.13, 1.27])
METRO = ("003", "015")
PROJECT_NAICS = {"561320", "561720", "561730"}


def rng(key, seed=W.SEED):
    return np.random.default_rng([seed, STREAMS[key]])


def month_date(m):
    """first day of month index m (0 = January 2023)"""
    return dt.date(2023 + m // 12, m % 12 + 1, 1)


class World:
    pass


# ----------------------------------------------------------------------------------------------------- structure
def _size(r, n, cls=None, p=None):
    bounds = [0] + [b for b, _ in W.SIZE_CLASSES]
    if p is None:
        p = np.array([s for _, s in W.SIZE_CLASSES])
    p = np.array(p, float) / np.sum(p)
    if cls is None:
        cls = r.choice(len(p), n, p=p)
    lo = np.array([bounds[c] + 1 for c in cls], float)
    hi = np.array([bounds[c + 1] for c in cls], float)
    u = r.random(n)
    emp = np.floor(lo * (hi / lo) ** u)        # log-uniform inside the class
    return cls, np.maximum(1, emp)


def _industry(r, county_code, cls, gov):
    if gov:
        k = r.integers(0, len(W.GOV_NAICS))
        return W.GOV_NAICS[k][0], W.GOV_NAICS[k][2]
    w = []
    tilt = W.TILT.get(county_code)
    for code, _, ss, wt, _ in W.NAICS:
        t = wt
        if tilt and code in tilt[1]:
            t *= tilt[0]
        if county_code in ("013", "023") and ss == "1026":
            t *= 3.0
        if county_code == "017" and ss == "1013":
            t *= 2.0
        if county_code == "003" and ss in ("1024", "1023", "1022"):
            t *= 1.8
        if cls >= 5 and ss in ("1013", "1025", "1021"):
            t *= 2.5
        if cls >= 5 and ss in ("1027", "1012"):
            t *= 0.4
        w.append(t)
    w = np.array(w) / sum(w)
    k = r.choice(len(W.NAICS), p=w)
    return W.NAICS[k][0], W.NAICS[k][2]


def structure(seed=W.SEED):
    """who the employers are: county, size, industry, when they started, how they file, where their worksites are"""
    w = World()
    w.seed = seed
    rp, ri, rc = rng("pop", seed), rng("industry", seed), rng("channel", seed)
    rows = []
    cinfo = {c[0]: c for c in W.COUNTIES}

    def new_account(county, start_m, cls=None, emp=None, gov=False, birth=False):
        if cls is None:
            cl, e = _size(rp, 1)
            cls, emp = int(cl[0]), float(e[0])
        naics, ss = _industry(ri, county, cls, gov)
        a = dict(county=county, cls=int(cls), emp0=float(emp), naics=naics, ss=ss, gov=gov, start_m=start_m,
                 birth=birth)
        rows.append(a)
        return len(rows) - 1

    # the employers of January 2023 (government units first in each county: a county, its towns, its schools)
    for code, name, n0, *_ in W.COUNTIES:
        ngov = max(4, int(round(n0 * 0.012)))
        for g in range(ngov):
            cls = 5 if g < 2 else int(rp.choice([3, 4, 5], p=[0.5, 0.35, 0.15]))
            _, e = _size(rp, 1, [cls])
            new_account(code, 0, cls, float(e[0]), gov=True)
        cls, emp = _size(rp, n0 - ngov)
        for k in range(n0 - ngov):
            new_account(code, 0, int(cls[k]), float(emp[k]))
    # state agencies with worksites in every county
    for s in range(4):
        new_account("003", 0, 7, float(rp.integers(900, 1500)), gov=True)
        rows[-1]["state"] = True

    # new employers, quarter by quarter; in 2026 fewer start up, far fewer in the housing chain
    rb = rng("births", seed)
    for q in range(1, W.NQ):
        for code, name, n0, *_ in W.COUNTIES:
            nb = rb.poisson(n0 * W.BIRTH_RATE)
            kind = rb.choice([REG_PROMPT, REG_REPORT, REG_FOUND], nb, p=REG_SHARES)
            um, ud, uk = rb.integers(0, 3, nb), rb.integers(1, 28, nb), rb.random(nb)
            for k in range(nb):
                cl, e = _size(rb, 1, p=REG_SIZE[int(kind[k])] + [0, 0, 0, 0])
                i = new_account(code, 3 * q + int(um[k]), int(cl[0]), float(e[0]), birth=True)
                rows[i]["liab_day"] = int(ud[k])
                rows[i]["reg"] = int(kind[k])
                if q >= 12:
                    keep = (W.BUST_BIRTHS if rows[i]["naics"] in W.HOUSING_CHAIN else W.OTHER_BIRTHS)[q - 12]
                    if uk[k] >= keep:
                        rows.pop()

    # transfers of business: a successor account takes over from the first day of a quarter
    rx = rng("maint", seed + 7)
    n_before = len(rows)
    for i in range(n_before):
        r0 = rows[i]
        if r0["gov"] or r0["cls"] < 1 or r0["cls"] > 3 or r0.get("reg") == REG_FOUND:
            continue
        for q in range(2, W.NQ - 1):
            if 3 * q <= r0["start_m"] + 3:
                continue
            if rx.random() < 0.0022:
                r0["xfer_q"] = q
                j = new_account(r0["county"], 3 * q, r0["cls"], r0["emp0"])
                rows[j]["naics"], rows[j]["ss"] = r0["naics"], r0["ss"]
                rows[j]["pred"] = i
                rows[j]["liab_day"] = 1
                break
    n = len(rows)
    w.n = n
    w.county = np.array([r["county"] for r in rows])
    w.cls = np.array([r["cls"] for r in rows])
    w.emp0 = np.array([r["emp0"] * W.SCALE[r["county"]] for r in rows])
    w.naics = np.array([r["naics"] for r in rows])
    w.ss = np.array([r["ss"] for r in rows])
    w.gov = np.array([r["gov"] for r in rows])
    w.state = np.array([bool(r.get("state")) for r in rows])
    w.start_m = np.array([r["start_m"] for r in rows])
    w.birth = np.array([r["birth"] for r in rows])
    w.reg = np.array([r.get("reg", 0) for r in rows])
    w.liab_day = np.array([r.get("liab_day") or 1 for r in rows])
    w.xfer_q = np.array([r.get("xfer_q", -1) for r in rows])
    w.pred = np.array([r.get("pred", -1) for r in rows])
    w.chain = np.isin(w.naics, list(W.HOUSING_CHAIN)) & ~w.gov

    # channels: twelve statewide payroll bureaus; local accountants in every county
    bureaus = 12
    w.bureaus = bureaus
    locals_by_county = {c[0]: max(4, int(round(c[2] / 95))) for c in W.COUNTIES}
    agents = [("bureau", None)] * bureaus
    for c in W.CODES:
        agents += [("local", c)] * locals_by_county[c]
    w.agent_kind = np.array([a[0] for a in agents])
    w.agent_county = np.array([a[1] or "" for a in agents])
    na = len(agents)
    w.n_agents = na
    bw = rc.lognormal(0, 0.6, bureaus)
    lw = rc.lognormal(0, 0.9, na - bureaus)
    p_agent_by_cls = np.array([0.62, 0.60, 0.50, 0.38, 0.22, 0.08, 0.04, 0.02])
    w.agent = np.full(n, -1)
    w.paper = np.zeros(n, bool)
    w.habitual = np.zeros(n, bool)
    for i in range(n):
        if w.gov[i] or w.reg[i] == REG_FOUND:
            continue
        c = cinfo[w.county[i]]
        pa = p_agent_by_cls[w.cls[i]] * c[4] / 0.60
        pb = c[5]
        if rc.random() < pa:
            if rc.random() < pb:
                w.agent[i] = int(rc.choice(bureaus, p=bw / bw.sum()))
            else:
                loc = np.where(w.agent_county == w.county[i])[0]
                ww = lw[loc - bureaus]
                w.agent[i] = int(rc.choice(loc, p=ww / ww.sum()))
        else:
            if w.cls[i] <= 1 and rc.random() < 0.06:
                w.paper[i] = True
            ph = [0.085, 0.07, 0.04, 0.02, 0.005, 0.0, 0.0, 0.0][w.cls[i]]
            w.habitual[i] = rc.random() < ph
    w.habitual &= ~w.birth                      # a new employer files on time until it has a record to keep
    for j in np.where(w.pred >= 0)[0]:
        i = w.pred[j]
        w.agent[j], w.paper[j], w.habitual[j] = w.agent[i], w.paper[i], False
    # year end: some agents are swamped every January (wage statements, annual returns) and send late most years
    busy = np.zeros(na, bool)
    busy[rc.choice(bureaus, 5, replace=False)] = True
    busy[bureaus:] = rc.random(na - bureaus) < 0.20
    w.agent_busy = busy
    w.followup_client = (w.agent >= 0) & (rc.random(n) < 0.07)
    w.followup_draw = rc.random(na) < 0.30
    w.agent_has_followup = w.followup_draw & (np.arange(na) < bureaus)    # only the statewide bureaus send one
    w.agent_q = _agent_by_quarter(w, rng("switch", seed), bureaus)
    _sites(w, rng("sites", seed))
    return w


def _agent_by_quarter(w, r, bureaus):
    """an employer's agent each quarter: a few change agents during the period"""
    aq = np.repeat(w.agent[:, None], W.NQ, axis=1)
    for i in np.where(w.agent >= 0)[0]:
        if r.random() < 0.02:
            q0 = int(r.integers(1, W.NQ))
            if w.agent[i] < bureaus:
                new = int(r.integers(0, bureaus))
            else:
                loc = np.where(w.agent_county == w.county[i])[0]
                new = int(r.choice(loc))
            aq[i, q0:] = new
    return aq


def _sites(w, r):
    """employers with worksites in several counties: each worksite's county, its share of the employer's jobs, when
    it opened and closed, its own drift from quarter to quarter and the season it keeps"""
    w.sites = {}
    size = {c[0]: c[2] for c in W.COUNTIES}
    for i in range(w.n):
        if w.state[i]:
            shares = r.dirichlet(np.ones(len(W.CODES)) * 3.0)
            w.sites[i] = [dict(county=c, share=float(s), open=0, close=W.NQ + 9, season=None,
                               walk=np.cumsum(r.normal(0, 0.006, W.NQ))) for c, s in zip(W.CODES, shares)]
            continue
        if w.gov[i] or w.cls[i] < 4 or w.birth[i] or w.pred[i] >= 0 or w.xfer_q[i] >= 0:
            continue
        if r.random() >= 0.24:
            continue
        home, ss = w.county[i], w.ss[i]
        trade = ss in ("1026", "1021")
        project = ss == "1012" or w.naics[i] in PROJECT_NAICS
        k = int(r.integers(2, 5))
        others = [c for c in W.CODES if c != home]
        wt = np.array([(size[c] ** 0.5) * (W.LAKE_SITES.get(c, 1.0) if trade else (2.5 if (c in W.NORTH and ss == "1026") else 1.0))
                       for c in others])
        extra = list(r.choice(others, k - 1, replace=False, p=wt / wt.sum()))
        shares = np.sort(r.dirichlet(np.ones(k) * 2.5))[::-1]

        def season(c):
            if c in W.LAKES and ss == "1026":
                return "leisure"
            if c in W.LAKES and ss == "1021":
                return "retail"
            if c in W.NORTH and (ss == "1012" or w.naics[i] == "561730"):
                return "outdoor"
            if c in W.NORTH and ss == "1026":
                return "winter"
            if c in METRO and ss == "1021":
                return "holiday"
            return None
        sites = [dict(county=c, share=float(s), open=0, close=W.NQ + 9, season=season(c),
                      walk=np.cumsum(r.normal(0, 0.03, W.NQ))) for c, s in zip([home] + extra, shares)]
        p_open, p_close = (0.060, 0.050) if project else (0.012, 0.009)
        for q in range(1, W.NQ):
            u1, u2 = r.random(), r.random()
            if u1 < p_open:
                have = {s["county"] for s in sites if s["close"] > q}
                cand = [c for c in W.CODES if c not in have]
                c = str(r.choice(cand))
                sites.append(dict(county=c, share=float(r.uniform(0.05, 0.25)), open=q, close=W.NQ + 9,
                                  season=season(c), walk=np.cumsum(r.normal(0, 0.03, W.NQ))))
            if u2 < p_close:
                live = [s for s in sites[1:] if s["open"] < q and s["close"] > q]
                if len(live) >= 2:
                    live[int(r.integers(0, len(live)))]["close"] = q
        w.sites[i] = sites


SEASON = {"leisure": LEISURE_LAKE, "retail": RETAIL_LAKE, "outdoor": OUTDOOR_NORTH, "winter": WINTER_NORTH,
          "holiday": HOLIDAY_METRO}


def site_weights(w, i, m):
    """each open worksite's weight in the employer's jobs for month m: (county, weight), weights summing to one"""
    q = m // 3
    out = []
    for s in w.sites[i]:
        if s["open"] <= q < s["close"]:
            f = SEASON[s["season"]][m % 12] if s["season"] else 1.0
            out.append((s["county"], s["share"] * math.exp(s["walk"][q]) * f))
    tot = sum(v for _, v in out)
    return [(c, v / tot) for c, v in out]


# ------------------------------------------------------------------------------------------------- jobs by month
def dynamics(w, offsets):
    """monthly jobs: the healthy path, the housing chain's 2026 slide, trouble and ordinary closures"""
    _paths(w, rng("paths", w.seed), offsets)
    _distress(w, rng("distress", w.seed), rng("bust", w.seed))


def _paths(w, r, offsets):
    n = w.n
    t = np.full(n, 0.006)
    off = np.array([offsets.get(c, 0.0) for c in w.county])
    lvl = np.zeros((n, W.NM))
    x = w.emp0.copy()
    sf = np.array([W.SUPERSECTORS[s][1] for s in w.ss])                 # n x 12
    for m in range(W.NM):
        drift = (t + (off if m >= 36 else 0.0)) / 12 + r.normal(0, 0.012, n)
        if m >= 36:
            # 2026: Merritt's plants cut back; the housing chain sheds work month after month
            drift = drift + np.where((w.county == "017") & (w.ss == "1013") & (w.cls >= 4), -0.0045, 0.0)
            slide = -(0.0035 + 0.0008 * (m - 36))
            drift = drift + np.where(w.chain, slide * np.where(w.cls >= 4, 0.55, 1.0), 0.0)
        x = x * np.exp(drift - 0.012 ** 2 / 2)
        lvl[:, m] = x * sf[:, m % 12]
    noise = r.normal(0, 1, (n, W.NM)) * np.sqrt(np.maximum(lvl, 1)) * 0.10
    jobs = np.maximum(0, np.round(lvl + noise))
    for j in np.where(w.pred >= 0)[0]:
        i = w.pred[j]
        m0 = w.start_m[j]
        jobs[j, m0:] = jobs[i, m0:]
        jobs[i, m0:] = 0
    alive = np.arange(W.NM)[None, :] >= w.start_m[:, None]
    jobs = np.where(alive, jobs, 0)
    for i in range(n):                      # every employer has at least one worker in its first month
        m0 = w.start_m[i]
        if jobs[i, m0] == 0:
            jobs[i, m0] = 1
    w.jobs_healthy = jobs.astype(float)


def _distress(w, r, rb):
    """employers in trouble: some close without a word (and stop filing), the rest cut back and file late; and the
    ordinary closures, with a final report and a notice"""
    n = w.n
    w.distress_q = np.full(n, -1)
    w.distress_m = np.full(n, -1)
    w.ceased = np.zeros(n, bool)
    w.final_report = np.zeros(n, bool)         # closed on notice with a final report on time
    w.shrink = np.ones(n)
    w.orderly_q = np.full(n, -1)
    jobs = w.jobs_healthy.copy()
    cidx = {c: k for k, c in enumerate(W.CODES)}
    ck = np.array([cidx[c] for c in w.county])
    for q in range(1, W.NQ):
        m0 = 3 * q
        live = (w.start_m <= m0) & (w.distress_q < 0) & (w.orderly_q < 0) & ((w.xfer_q < 0) | (q < w.xfer_q)) & ~w.gov
        h = BASE_HAZARD[w.cls]
        local = rb.gamma(70.0, 1 / 70.0, len(W.CODES))        # the downturn bites a little differently county to county
        if q >= 12:      # the downturn adds to a housing employer's usual risk, the small and the mid-sized alike
            h = np.where(w.chain, h + W.BUST_HAZARD[q - 12] * np.array(W.BUST_SIZE)[w.cls] * local[ck], h)
        if q >= 14:
            h = np.where(w.cls >= 5, 0.0, h)
        # every employer's draws for the quarter, so a hazard tuned for one group moves no other employer's outcome
        u_hit, u_month, u_cease, u_final = r.random(n), r.integers(0, 3, n), r.random(n), r.random(n)
        u_shrink, u_floor = r.uniform(0.50, 0.85, n), r.random(n)
        u_close, u_cmonth = r.random(n), r.integers(0, 3, n)
        hit = live & (u_hit < h)
        for i in np.where(hit)[0]:
            w.distress_q[i] = q
            mm = m0 + int(u_month[i])
            w.distress_m[i] = mm
            if u_cease[i] < P_CEASE:
                w.ceased[i] = True
                jobs[i, mm:] = 0
                w.final_report[i] = u_final[i] < 0.12
            else:
                f = u_shrink[i]
                w.shrink[i] = f
                jobs[i, mm:] = np.floor(jobs[i, mm:] * f + u_floor[i])
        live = live & ~hit
        oc = live & (u_close < ORDERLY[w.cls]) & (w.start_m < m0 - 2)
        for i in np.where(oc)[0]:
            w.orderly_q[i] = q
            mm = m0 + int(u_cmonth[i])
            jobs[i, mm:] = 0
    w.jobs = jobs


def county_truth(w, m):
    """true covered jobs by worksite county for month m"""
    tot = {c: 0.0 for c in W.CODES}
    multi = np.zeros(w.n, bool)
    for i in w.sites:
        multi[i] = True
        j = w.jobs[i, m]
        if j > 0:
            for c, s in site_weights(w, i, m):
                tot[c] += j * s
    for k, c in enumerate(W.CODES):
        tot[c] += w.jobs[(w.county == c) & ~multi, m].sum()
    return tot


def true_change(w):
    a, b = county_truth(w, 35), county_truth(w, 47)
    return {c: b[c] / a[c] - 1 for c in W.CODES}


# ----------------------------------------------------------------------------------------- the Division's records
def _stamp(day_offset, due, sec):
    """a received stamp: the due date plus an offset in days, at a business-hours second"""
    d = due + dt.timedelta(days=int(math.floor(day_offset)))
    return dt.datetime(d.year, d.month, d.day) + dt.timedelta(seconds=int(sec))


def liab_date(w, i):
    md = month_date(w.start_m[i])
    return dt.date(md.year, md.month, int(w.liab_day[i]) if w.birth[i] else 1)


def _filing(w, r):
    """each liable employer-quarter's original report: whether it reached the Division and when; every employer-
    quarter's draws are taken up front, so one employer's circumstances move no other employer's stamp"""
    n, na, bureaus = w.n, w.n_agents, w.bureaus
    recv = {}                                   # (i, q) -> datetime (paper at 00:00:00)
    main_t, follow_t = {}, {}
    for q in range(W.NQ):
        due = W.due_date(q)
        for a in range(na):
            bureau = a < bureaus
            off = r.uniform(-12, -1) if bureau else r.uniform(-26, -2)
            if q % 4 == 3:
                late_p = (0.85 if w.agent_busy[a] else 0.12) if bureau else (0.70 if w.agent_busy[a] else 0.06)
            else:
                late_p = 0.02
            if r.random() < late_p:
                off = r.uniform(W.CUTOFF_DAY + 1, W.CUTOFF_DAY + 36)
            main_t[a, q] = _stamp(off, due, r.integers(7 * 3600 + 1800, 19 * 3600))
            if w.followup_draw[a]:
                ft = main_t[a, q] + dt.timedelta(days=int(r.integers(1, 6)), seconds=int(r.integers(600, 30000)))
                if w.agent_has_followup[a]:
                    follow_t[a, q] = ft
    w.main_t, w.follow_t = main_t, follow_t
    U = r.random((n, W.NQ, 4))
    V = r.random((n, W.NQ, 2))
    SEC = r.integers(7 * 3600 + 1800, 19 * 3600, (n, W.NQ))
    MAIL = r.integers(1, 5, (n, W.NQ))
    lerp = lambda u, a, b: a + (b - a) * u
    late_own = 0.0136 * BASE_HAZARD
    # an employer the Division had to find: nothing arrives until its account is set up, then every report due
    rr = rng("reg", w.seed)
    FOUND = rr.integers(120, 431, n)
    SETUP = rr.integers(10, 41, n)
    BACK = rr.integers(5, 46, n)
    w.found_setup, w.found_back = {}, {}
    for i in np.where(w.reg == REG_FOUND)[0]:
        est = liab_date(w, i) + dt.timedelta(days=int(FOUND[i]) + int(SETUP[i]))
        w.found_setup[i] = est
        w.found_back[i] = dt.datetime(est.year, est.month, est.day) + dt.timedelta(days=int(BACK[i]), seconds=int(SEC[i, 0]))
    for i in range(n):
        for q in range(W.NQ):
            if w.start_m[i] > 3 * q + 2:
                continue                        # not yet liable
            if w.xfer_q[i] >= 0 and q >= w.xfer_q[i]:
                continue                        # the successor reports from the transfer quarter
            due = W.due_date(q)
            dq = w.distress_q[i]
            u, v, sec = U[i, q], V[i, q], SEC[i, q]
            if w.orderly_q[i] >= 0 and q > w.orderly_q[i]:
                continue
            a = w.agent_q[i, q]
            if dq >= 0 and q >= dq and w.ceased[i]:
                if q == dq and w.final_report[i] and i not in w.found_back:
                    recv[i, q] = _stamp(lerp(v[0], -20, 0), due, sec) if a < 0 else main_t[a, q]
                continue                        # closed without a word: nothing more arrives
            if i in w.found_back and dt.datetime(due.year, due.month, due.day) <= w.found_back[i] + dt.timedelta(days=20):
                recv[i, q] = w.found_back[i] + dt.timedelta(seconds=140 * q + int(sec) % 97)
                continue
            if dq == q and not w.ceased[i]:
                recv[i, q] = _stamp(lerp(v[0], 30, 140), due, sec)   # cut back: the report comes late, on its own
                continue
            first = w.birth[i] and w.start_m[i] >= 3 * q
            if a >= 0:
                if first and u[0] < 0.06:
                    recv[i, q] = _stamp(lerp(v[0], W.CUTOFF_DAY + 1, W.CUTOFF_DAY + 40), due, sec)
                elif u[1] < late_own[w.cls[i]]:            # its data reached the agent too late for any file
                    recv[i, q] = _stamp(lerp(v[0], W.CUTOFF_DAY + 1, W.CUTOFF_DAY + 40), due, sec)
                elif w.followup_client[i] and w.agent_has_followup[a]:
                    recv[i, q] = follow_t[a, q]
                else:
                    recv[i, q] = main_t[a, q]
            elif w.gov[i]:
                recv[i, q] = _stamp(lerp(v[0], -15, 0), due, sec)
            else:
                if w.habitual[i]:
                    off = lerp(v[0], 20, 68)
                elif first and u[0] < 0.10:
                    off = lerp(v[0], W.CUTOFF_DAY + 1, W.CUTOFF_DAY + 40)
                elif u[1] < late_own[w.cls[i]]:
                    off = lerp(v[0], W.CUTOFF_DAY + 1, W.CUTOFF_DAY + 55)
                else:
                    off = lerp(v[0], -6, 0) if u[2] < 0.55 else (lerp(v[0], -28, -6) if u[2] < 0.86 else lerp(v[0], 0, 11))
                t = _stamp(off, due, sec)
                if w.paper[i]:
                    t = dt.datetime(t.year, t.month, t.day) + dt.timedelta(days=int(MAIL[i, q]))
                recv[i, q] = t
    w.recv = recv


def _registration(w):
    """when the Division set up each new employer's account: ahead of its first report for an employer that applied
    promptly, some weeks after its first report for one that registered with it, and on discovery for one the
    Division had to find; a successor's account is set up when the transfer is entered"""
    rr = np.random.default_rng([w.seed, 41])
    APPLY, EXAM, WITH = rr.integers(3, 36, w.n), rr.integers(4, 31, w.n), rr.integers(6, 71, w.n)
    first = {}
    for (i, q), t in w.recv.items():
        if w.birth[i] and (i not in first or t < first[i]):
            first[i] = t
    est = [None] * w.n
    for i in range(w.n):
        if not w.birth[i]:
            continue
        ld = liab_date(w, i)
        if w.reg[i] == REG_PROMPT:
            est[i] = ld + dt.timedelta(days=int(APPLY[i]) + int(EXAM[i]))
        elif w.reg[i] == REG_FOUND:
            est[i] = w.found_setup[i]
        else:
            est[i] = (first[i].date() + dt.timedelta(days=int(WITH[i]))) if i in first else dt.date(2099, 12, 31)
    w.established = est


def _maintenance(w, r):
    """the Division's account maintenance, with the date each change was entered"""
    n = w.n
    lag_close, lag_inact = r.integers(5, 60, n), r.integers(120, 330, n)
    lag_xfer, lag_orderly = r.integers(10, 55, n), r.integers(3, 50, n)
    post = np.random.default_rng([w.seed, 44]).integers(1, 6, n)
    ev = []                                     # (employer index, kind, effective date, entered date, reason, other)
    uday = np.random.default_rng([w.seed, 43]).random(n)

    def closing_day(i, z):
        a = month_date(z - 1) + dt.timedelta(days=12) if z >= 1 else month_date(0)
        b = month_date(z) + dt.timedelta(days=11)
        d = a + dt.timedelta(days=int(uday[i] * ((b - a).days + 1)))
        return max(d, liab_date(w, i) + dt.timedelta(days=1))
    for i in range(n):
        sm = w.start_m[i]
        if w.birth[i]:
            ev.append((i, "LIABLE", liab_date(w, i), w.established[i], "NEW EMPLOYER", None))
        if w.ceased[i]:
            q = w.distress_q[i]
            eff = month_date(w.distress_m[i])
            if w.final_report[i] and (i, q) in w.recv:
                proc = max(W.due_date(q) + dt.timedelta(days=int(lag_close[i])),
                           w.recv[i, q].date() + dt.timedelta(days=int(post[i])))
                ev.append((i, "CLOSED", closing_day(i, w.distress_m[i]), proc, "EMPLOYER NOTICE - BUSINESS CLOSED", None))
            else:
                second = W.due_date(q + 1) if q + 1 < W.NQ else W.due_date(q) + dt.timedelta(days=92)
                proc = second + dt.timedelta(days=int(lag_inact[i]))
                eff = max(eff, liab_date(w, i) + dt.timedelta(days=1))      # never on or before its own liability
                ev.append((i, "INACTIVATED", eff, proc, "NO WAGE REPORTS 2 QTRS", None))
        if w.pred[i] >= 0:
            p = w.pred[i]
            eff = month_date(sm)
            proc = eff + dt.timedelta(days=int(lag_xfer[i]))
            ev.append((p, "TRANSFERRED", eff, proc, "SUCCESSOR", i))
            ev.append((i, "LIABLE", eff, proc, "SUCCESSOR TO", p))
            w.established[i] = proc
        if w.orderly_q[i] >= 0:
            q = w.orderly_q[i]
            last = max([m for m in range(W.NM) if w.jobs[i, m] > 0] or [3 * q])
            proc = W.due_date(q) + dt.timedelta(days=int(lag_orderly[i]))
            t = w.recv.get((i, q))
            if t is not None:
                proc = max(proc, t.date() + dt.timedelta(days=int(post[i])))
            ev.append((i, "CLOSED", closing_day(i, min(last + 1, W.NM - 1)), proc, "EMPLOYER NOTICE - BUSINESS CLOSED", None))
    w.events = ev
    w.registered = np.array([w.established[i] is None or w.established[i] <= W.EXTRACT.date() for i in range(n)])


def _amendments(w, r):
    """some reports are amended later (a corrected month), and a few are sent twice within seconds"""
    n = w.n
    U = r.random((n, W.NQ))
    DAYS, SECS = r.integers(2, 75, (n, W.NQ)), r.integers(100, 40000, (n, W.NQ))
    K, DEL = r.integers(0, 3, (n, W.NQ)), r.choice([-2, -1, 1, 1, 2], (n, W.NQ))
    DUPS = r.integers(2, 95, (n, W.NQ))
    amend, dup = {}, {}
    for (i, q), t in w.recv.items():
        u = U[i, q]
        if u < 0.028:
            # most corrections follow within weeks; a few come out of an audit months later
            days = int(DAYS[i, q]) if u >= 0.004 else 76 + int(DAYS[i, q]) * 4 + int(SECS[i, q]) % 31
            amend[i, q] = (t + dt.timedelta(days=days, seconds=int(SECS[i, q])), int(K[i, q]), int(DEL[i, q]))
        elif u < 0.034 and t.hour + t.minute + t.second > 0:
            dup[i, q] = t + dt.timedelta(seconds=int(DUPS[i, q]))
    w.amend, w.dup = amend, dup


def _worksite_reports(w, r):
    """when each multiple worksite report reached the Division: with the contribution report, or weeks after it"""
    w.mwr_recv = {}
    for i in sorted(w.sites):
        U, A, B, C = r.random(W.NQ), r.integers(0, 10, W.NQ), r.integers(18, 61, W.NQ), r.integers(60, 151, W.NQ)
        for q in range(W.NQ):
            t = w.recv.get((i, q))
            if t is None:
                continue
            p_fast = 0.90 if w.state[i] else 0.52
            lag = A[q] if U[q] < p_fast else (B[q] if U[q] < 0.87 or w.state[i] else C[q])
            w.mwr_recv[i, q] = t.date() + dt.timedelta(days=int(lag))


def build(seed=W.SEED, passes=7, quiet=True):
    """the structure once; then the jobs with each county's 2026 drift set so its December-on-December change lands
    on the county's target; then the Division's records"""
    w = structure(seed)
    target = {c[0]: c[3] for c in W.COUNTIES}
    off = {c: 0.0 for c in W.CODES}
    for k in range(passes):
        dynamics(w, off)
        ch = true_change(w)
        if not quiet:
            print("pass", k, {W.NAMES[c]: round(100 * ch[c], 2) for c in W.CODES})
        if k < passes - 1:
            off = {c: off[c] + math.log((1 + target[c] + W.NUDGE[c]) / (1 + ch[c])) for c in W.CODES}
    w.calibration = off
    _filing(w, rng("timing", seed))
    _registration(w)
    _maintenance(w, rng("maint", seed))
    _amendments(w, rng("amend", seed))
    _worksite_reports(w, rng("mwr", seed))
    return w
