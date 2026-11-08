"""task5 architecture 3: the State of Franklin's employers and their unemployment insurance filings, 2023 to 2026.

The clean truth: every employer's monthly jobs (pay period including the 12th), its filing channel (a payroll agent's
transmission, the web portal, paper), when each quarterly report reached the Division, what happened to employers in
trouble (closed without a word, or shrank and filed late), and the Division's account maintenance (new liabilities,
inactivations after two quarters without a report, closures on notice, transfers to a successor). One random stream
per component, so tuning one leaves the others' draws unchanged."""
import datetime as dt
import math

import numpy as np

import world as W

STREAMS = {"pop": 1, "industry": 2, "channel": 3, "paths": 4, "distress": 5, "births": 6, "timing": 7,
           "amend": 8, "maint": 9, "worksites": 10, "names": 11, "shock": 12, "season": 13, "switch": 14}

MONTH0 = dt.date(2023, 1, 1)


def rng(key, seed=W.SEED):
    return np.random.default_rng([seed, STREAMS[key]])


def month_date(m):
    """first day of month index m (0 = January 2023)"""
    return dt.date(2023 + m // 12, m % 12 + 1, 1)


class World:
    pass


# ----------------------------------------------------------------------------------------------------------- people
def _size(r, n, cls=None):
    bounds = [0] + [b for b, _ in W.SIZE_CLASSES]
    p = np.array([s for _, s in W.SIZE_CLASSES])
    p = p / p.sum()
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
    for code, _, ss, wt, _ in W.NAICS:
        t = wt
        if county_code == "019" and code in W.SHOCK_NAICS["ostrom"]:
            t *= 9.0
        if county_code == "009" and code in W.SHOCK_NAICS["garrow"]:
            t *= 3.0
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


def _build(seed=W.SEED, offsets=None):
    w = World()
    w.offsets = offsets or {}
    w.seed = seed
    rp, ri, rc = rng("pop", seed), rng("industry", seed), rng("channel", seed)
    rows = []                                    # one per account
    cinfo = {c[0]: c for c in W.COUNTIES}

    def new_account(county, start_m, cls=None, emp=None, gov=False, birth=False):
        if cls is None:
            cl, e = _size(rp, 1)
            cls, emp = int(cl[0]), float(e[0])
        naics, ss = _industry(ri, county, cls, gov)
        a = dict(county=county, cls=int(cls), emp0=float(emp), naics=naics, ss=ss, gov=gov, start_m=start_m,
                 birth=birth, end_m=None)
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

    # births, quarter by quarter (the first report of a new employer covers its liability quarter)
    rb = rng("births", seed)
    for q in range(1, W.NQ):
        for code, name, n0, trend, *_ in W.COUNTIES:
            lam = n0 * 0.0215
            nb = rb.poisson(lam)
            cls, emp = _size(rb, nb, rb.choice(4, nb, p=[0.62, 0.24, 0.10, 0.04]))
            for k in range(nb):
                m = 3 * q + int(rb.integers(0, 3))
                i = new_account(code, m, int(cls[k]), float(emp[k]), birth=True)
                rows[i]["liab_day"] = int(rb.integers(1, 28))

    # transfers of business: a successor account takes over from the first day of a quarter
    rx = rng("maint", seed + 7)
    n_before = len(rows)
    for i in range(n_before):
        r0 = rows[i]
        if r0["gov"] or r0["cls"] < 1:
            continue
        for q in range(2, W.NQ - 1):
            if 3 * q <= r0["start_m"]:
                continue
            if rx.random() < 0.0022:
                r0["xfer_q"] = q
                j = new_account(r0["county"], 3 * q, r0["cls"], r0["emp0"])
                rows[j]["naics"], rows[j]["ss"] = r0["naics"], r0["ss"]
                rows[j]["pred"] = i
                rows[j]["liab_day"] = 1
                rows[j]["birth"] = False
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
    w.liab_day = np.array([r.get("liab_day") or 1 for r in rows])
    w.xfer_q = np.array([r.get("xfer_q", -1) for r in rows])
    w.pred = np.array([r.get("pred", -1) for r in rows])

    # ------------------------------------------------------------------------------------------- shock exposure
    rs = rng("shock", seed)
    w.exposed = np.zeros(n, bool)
    for cc, key in W.SHOCK.items():
        idx = np.where((w.county == cc) & np.isin(w.naics, list(W.SHOCK_NAICS[key])) & (w.cls <= 3) & ~w.gov
                       & (w.start_m <= 42))[0]
        share = 0.70 if key == "garrow" else 0.88
        w.exposed[idx[rs.random(len(idx)) < share]] = True

    # ------------------------------------------------------------------------------------- seasonal lake resorts
    rse = rng("season", seed)
    w.seasonal = np.zeros(n, bool)
    lake = np.isin(w.county, ["013", "023"]) & np.isin(w.naics, list(W.LAKE_SEASONAL)) & ~w.gov & (w.cls <= 3)
    w.seasonal[lake & (rse.random(n) < 0.55)] = True

    # --------------------------------------------------------------------------------------------- channels
    # agents: twelve statewide payroll bureaus; local accountants in every county
    bureaus = 12
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
        if w.gov[i]:
            continue
        c = cinfo[w.county[i]]
        pa = p_agent_by_cls[w.cls[i]] * c[4] / 0.60
        pb = c[5]
        if w.exposed[i]:
            pa, pb = (0.88, 0.04) if W.SHOCK[w.county[i]] == "garrow" else (0.14, 0.10)
        if w.seasonal[i]:
            pa, pb = 0.80, 0.85
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
        w.agent[j], w.paper[j], w.habitual[j], w.exposed[j], w.seasonal[j] = w.agent[i], w.paper[i], False, False, w.seasonal[i]
    # clients whose payroll data reach their agent late go in the agent's follow-up file
    w.followup_client = (w.agent >= 0) & (rc.random(n) < 0.07)
    w.followup_draw = rc.random(na) < 0.30
    w.agent_has_followup = w.followup_draw & (np.arange(na) < bureaus)    # only the statewide bureaus send one
    w.agent_q = _agent_by_quarter(w, rng("switch", seed), bureaus)

    _paths(w, rng("paths", seed))
    _distress(w, rng("distress", seed))
    _maintenance(w, rng("maint", seed))
    _filing(w, rng("timing", seed), bureaus)
    _registration(w)
    _amendments(w, rng("amend", seed))
    _worksites(w, rng("worksites", seed))
    return w


def _agent_by_quarter(w, r, bureaus):
    """an employer's agent each quarter: a few change agents (or start filing themselves) during the period"""
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


# ------------------------------------------------------------------------------------------------- jobs by month
def _paths(w, r):
    n = w.n
    trend = {c[0]: c[3] for c in W.COUNTIES}
    t = np.array([trend[c] + 0.006 for c in w.county])
    off = np.array([w.offsets.get(c, 0.0) for c in w.county])
    lvl = np.zeros((n, W.NM))
    x = w.emp0.copy()
    sf = np.array([W.SUPERSECTORS[s][1] for s in w.ss])                 # n x 12
    summer = np.array([0.14, 0.14, 0.16, 0.22, 0.62, 0.95, 1.00, 1.00, 0.86, 0.38, 0.16, 0.13])
    for m in range(W.NM):
        drift = (t + (off if m >= 36 else 0.0)) / 12 + r.normal(0, 0.012, n)
        if m >= 36:                                                       # 2026: Merritt's plants cut back
            drift = drift + np.where((w.county == "017") & (w.ss == "1013") & (w.cls >= 4), -0.0045, 0.0)
        x = x * np.exp(drift - 0.012 ** 2 / 2)
        s = sf[:, m % 12]
        s = np.where(w.seasonal, summer[m % 12] / 0.62, s)
        lvl[:, m] = x * s
    noise = r.normal(0, 1, (n, W.NM)) * np.sqrt(np.maximum(lvl, 1)) * 0.10
    jobs = np.maximum(0, np.round(lvl + noise))
    jobs = np.where(w.seasonal[:, None], np.maximum(0, np.round(lvl)), jobs)
    for j in np.where(w.pred >= 0)[0]:
        i = w.pred[j]
        m0 = w.start_m[j]
        jobs[j, m0:] = jobs[i, m0:]
        jobs[i, m0:] = 0
    alive = np.arange(W.NM)[None, :] >= w.start_m[:, None]
    jobs = np.where(alive, jobs, 0)
    # every non-seasonal employer has at least one worker in its first month
    first = np.zeros(n, int)
    for i in range(n):
        m0 = w.start_m[i]
        if jobs[i, m0] == 0 and not w.seasonal[i]:
            jobs[i, m0] = 1
    w.jobs_healthy = jobs.astype(float)


def _distress(w, r):
    """employers in trouble: some close without a word (and stop filing), the rest shrink and file late"""
    n = w.n
    w.distress_q = np.full(n, -1)
    w.distress_m = np.full(n, -1)
    w.ceased = np.zeros(n, bool)
    w.final_report = np.zeros(n, bool)         # closed on notice with a final report on time
    w.shrink = np.ones(n)
    w.orderly_q = np.full(n, -1)               # closed in the ordinary way: a final report and a notice
    base_h = np.array([0.022, 0.014, 0.008, 0.0045, 0.0016, 0.0005, 0.0, 0.0])
    p_cease = np.array([0.64, 0.64, 0.64, 0.64, 0.64, 0.64, 0.0, 0.0])
    jobs = w.jobs_healthy.copy()
    for q in range(1, W.NQ):
        m0 = 3 * q
        live = (w.start_m <= m0) & (w.distress_q < 0) & (w.orderly_q < 0) & ((w.xfer_q < 0) | (q < w.xfer_q)) & ~w.gov
        h = base_h[w.cls]
        if q >= 14:
            h = np.where(w.cls >= 5, 0.0, h)
        if q == W.FLASH_Q:
            add = np.where(w.county == "009", 0.40, np.where(w.county == "019", 0.32, 0.0))
            h = h + np.where(w.exposed, add, 0.0)
        # every employer's draws for the quarter, so a hazard tuned for one county moves no other employer's outcome
        u_hit, u_month, u_cease, u_final = r.random(n), r.integers(0, 3, n), r.random(n), r.random(n)
        u_shrink, u_floor = r.uniform(0.50, 0.85, n), r.random(n)
        u_close, u_cmonth = r.random(n), r.integers(0, 3, n)
        hit = live & (u_hit < h)
        for i in np.where(hit)[0]:
            w.distress_q[i] = q
            mm = m0 + int(u_month[i])
            w.distress_m[i] = mm
            if u_cease[i] < p_cease[w.cls[i]]:
                w.ceased[i] = True
                jobs[i, mm:] = 0
                w.final_report[i] = u_final[i] < 0.12
            else:
                f = u_shrink[i]
                w.shrink[i] = f
                jobs[i, mm:] = np.floor(jobs[i, mm:] * f + u_floor[i])
        # ordinary closures
        live = live & ~hit
        oc = live & (u_close < 0.0035) & (w.start_m < m0)
        for i in np.where(oc)[0]:
            w.orderly_q[i] = q
            mm = m0 + int(u_cmonth[i])
            jobs[i, mm:] = 0
    w.jobs = jobs


def _maintenance(w, r):
    """the Division's account maintenance, with the date each change was processed (each employer's lags drawn up
    front, so a change to one employer's history moves no other employer's dates)"""
    n = w.n
    lag_liab, lag_close, lag_inact = r.integers(6, 40, n), r.integers(5, 60, n), r.integers(120, 330, n)
    lag_xfer, lag_orderly = r.integers(10, 55, n), r.integers(3, 50, n)
    ev = []                                     # (employer index, kind, effective date, processed date, reason, other)
    w.inact_processed = {}
    # an employer's own notice of closing names the day after its last payroll: any day between the pay period that
    # includes the 12th of its last month with workers and the next one (the draws on their own stream)
    uday = np.random.default_rng([w.seed, 43]).random(n)
    def closing_day(i, z):
        a = month_date(z - 1) + dt.timedelta(days=12) if z >= 1 else month_date(0)
        b = month_date(z) + dt.timedelta(days=11)
        d = a + dt.timedelta(days=int(uday[i] * ((b - a).days + 1)))
        sm_ = month_date(w.start_m[i])
        own = dt.date(sm_.year, sm_.month, int(w.liab_day[i])) if w.birth[i] else sm_      # its own liability date
        return max(d, own + dt.timedelta(days=1))
    for i in range(n):
        sm = w.start_m[i]
        if w.birth[i]:
            eff = dt.date(month_date(sm).year, month_date(sm).month, int(w.liab_day[i]))
            proc = eff + dt.timedelta(days=int(lag_liab[i]))
            ev.append((i, "LIABLE", eff, proc, "NEW EMPLOYER", None))
        if w.ceased[i]:
            q = w.distress_q[i]
            eff = month_date(w.distress_m[i])
            if w.final_report[i]:
                proc = W.due_date(q) + dt.timedelta(days=int(lag_close[i]))
                ev.append((i, "CLOSED", closing_day(i, w.distress_m[i]), proc, "EMPLOYER NOTICE - BUSINESS CLOSED", None))
            else:
                second = W.due_date(q + 1) if q + 1 < W.NQ else W.due_date(q) + dt.timedelta(days=92)
                proc = second + dt.timedelta(days=int(lag_inact[i]))
                sm_ = month_date(w.start_m[i])
                own = dt.date(sm_.year, sm_.month, int(w.liab_day[i])) if w.birth[i] else sm_
                eff = max(eff, own + dt.timedelta(days=1))                  # never on or before its own liability
                ev.append((i, "INACTIVATED", eff, proc, "NO WAGE REPORTS 2 QTRS", None))
                w.inact_processed[i] = proc
        if w.pred[i] >= 0:
            p = w.pred[i]
            eff = month_date(sm)
            proc = eff + dt.timedelta(days=int(lag_xfer[i]))
            ev.append((p, "TRANSFERRED", eff, proc, "SUCCESSOR", i))
            ev.append((i, "LIABLE", eff, proc, "SUCCESSOR TO", p))
        if w.orderly_q[i] >= 0:
            q = w.orderly_q[i]
            last = max([m for m in range(W.NM) if w.jobs[i, m] > 0] or [3 * q])
            proc = W.due_date(q) + dt.timedelta(days=int(lag_orderly[i]))
            ev.append((i, "CLOSED", closing_day(i, min(last + 1, W.NM - 1)), proc, "EMPLOYER NOTICE - BUSINESS CLOSED", None))
    w.events = ev


# ------------------------------------------------------------------------------------------------- the filings
def _stamp(day_offset, due, sec):
    """a received stamp: the due date plus an offset in days, at a business-hours second"""
    d = due + dt.timedelta(days=int(math.floor(day_offset)))
    return dt.datetime(d.year, d.month, d.day) + dt.timedelta(seconds=int(sec))


def _filing(w, r, bureaus):
    """each liable employer-quarter's original report: whether it reached the Division and when; every employer-
    quarter's draws are taken up front, so one employer's circumstances move no other employer's stamp"""
    n = w.n
    na = w.n_agents
    recv = {}                                   # (i, q) -> datetime (paper at 00:00:00)
    # every agent's transmissions, quarter by quarter
    main_t, follow_t = {}, {}
    for q in range(W.NQ):
        due = W.due_date(q)
        for a in range(na):
            bureau = a < bureaus
            off = r.uniform(-12, -1) if bureau else r.uniform(-26, -2)
            late_p = (0.50 if bureau else 0.05) if q % 4 == 3 else 0.02
            if r.random() < late_p:
                off = r.uniform(W.CUTOFF_DAY + 1, W.CUTOFF_DAY + 36)
            main_t[a, q] = _stamp(off, due, r.integers(7 * 3600 + 1800, 19 * 3600))
            if w.followup_draw[a]:
                ft = main_t[a, q] + dt.timedelta(days=int(r.integers(1, 6)), seconds=int(r.integers(600, 30000)))
                if w.agent_has_followup[a]:
                    follow_t[a, q] = ft
    w.main_t, w.follow_t = main_t, follow_t
    U = r.random((n, W.NQ, 4))                  # branch draws
    V = r.random((n, W.NQ, 2))                  # offset draws
    SEC = r.integers(7 * 3600 + 1800, 19 * 3600, (n, W.NQ))
    MAIL = r.integers(1, 5, (n, W.NQ))
    lerp = lambda u, a, b: a + (b - a) * u
    # a healthy employer's report misses the cutoff on its own about as often, size for size, as trouble strikes,
    # whoever files it
    late_agent = late_direct = 0.0136 * np.array([0.022, 0.014, 0.008, 0.0045, 0.0016, 0.0005, 0.0, 0.0])
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
            if dq >= 0 and q >= dq and w.ceased[i]:
                if q == dq and w.final_report[i]:
                    recv[i, q] = _stamp(lerp(v[0], -20, 0), due, sec) if w.agent_q[i, q] < 0 else main_t[w.agent_q[i, q], q]
                continue                        # closed without a word: nothing more arrives
            if dq == q and not w.ceased[i]:
                recv[i, q] = _stamp(lerp(v[0], 30, 140), due, sec)   # shrank: the report comes late, on its own
                continue
            a = w.agent_q[i, q]
            first = w.birth[i] and w.start_m[i] >= 3 * q
            if a >= 0:
                if first and u[0] < 0.004:
                    recv[i, q] = _stamp(lerp(v[0], W.CUTOFF_DAY + 1, W.CUTOFF_DAY + 40), due, sec)
                elif u[1] < late_agent[w.cls[i]]:          # its data reached the agent too late for any file
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
                elif first and u[0] < 0.004:
                    off = lerp(v[0], W.CUTOFF_DAY + 1, W.CUTOFF_DAY + 40)
                elif u[1] < late_direct[w.cls[i]]:
                    off = lerp(v[0], W.CUTOFF_DAY + 1, W.CUTOFF_DAY + 55)
                else:
                    off = lerp(v[0], -6, 0) if u[2] < 0.55 else (lerp(v[0], -28, -6) if u[2] < 0.86 else lerp(v[0], 0, 11))
                t = _stamp(off, due, sec)
                if w.paper[i]:
                    t = dt.datetime(t.year, t.month, t.day) + dt.timedelta(days=int(MAIL[i, q]))
                recv[i, q] = t
    w.recv = recv


def _registration(w):
    """a new employer's liability is established from its first report, on the day that report arrives; one whose
    first report has not arrived is not yet on the register"""
    first = {}
    for (i, q), t in w.recv.items():
        if w.birth[i] and (i not in first or t < first[i]):
            first[i] = t
    w.registered = np.array([(not w.birth[i]) or (i in first and first[i] <= W.EXTRACT) for i in range(w.n)])
    lag = np.random.default_rng([w.seed, 41]).integers(0, 4, w.n)      # the overnight runs that post a new account
    ev = []
    for (i, kind, eff, proc, reason, other) in w.events:
        if w.birth[i] and kind == "LIABLE":
            proc = min(first[i].date() + dt.timedelta(days=int(lag[i])), W.EXTRACT.date()) if i in first else dt.date(2099, 12, 31)
        ev.append((i, kind, eff, proc, reason, other))
    # a notice of closing is entered with the employer's final report, so a closure whose final report is still out
    # is not yet on the history
    post = np.random.default_rng([w.seed, 44]).integers(1, 6, w.n)
    ev = []
    for (i, kind, eff, proc, reason, other) in w.events:
        if kind == "CLOSED":
            qc = w.distress_q[i] if (w.ceased[i] and w.final_report[i]) else w.orderly_q[i]
            t = w.recv.get((i, qc))
            if t is not None:
                proc = max(proc, t.date() + dt.timedelta(days=int(post[i])))
        ev.append((i, kind, eff, proc, reason, other))
    w.events = ev


def _amendments(w, r):
    """some reports are amended later (a corrected month), and a few are sent twice within seconds; the draws are
    taken for every employer-quarter up front"""
    n = w.n
    U = r.random((n, W.NQ))
    DAYS, SECS = r.integers(2, 75, (n, W.NQ)), r.integers(100, 40000, (n, W.NQ))
    K, DEL = r.integers(0, 3, (n, W.NQ)), r.choice([-2, -1, 1, 1, 2], (n, W.NQ))
    DUPS = r.integers(2, 95, (n, W.NQ))
    amend, dup = {}, {}
    for (i, q), t in w.recv.items():
        u = U[i, q]
        if u < 0.028:
            amend[i, q] = (t + dt.timedelta(days=int(DAYS[i, q]), seconds=int(SECS[i, q])), int(K[i, q]), int(DEL[i, q]))
        elif u < 0.034 and t.hour + t.minute + t.second > 0:
            dup[i, q] = t + dt.timedelta(seconds=int(DUPS[i, q]))
    w.amend, w.dup = amend, dup


def _worksites(w, r):
    """employers with worksites in several counties report each worksite's jobs on the multiple worksite report"""
    n = w.n
    w.sites = {}
    for i in range(n):
        if w.state[i]:
            k = len(W.CODES)
            shares = r.dirichlet(np.ones(k) * 3.0)
            w.sites[i] = list(zip(W.CODES, shares))
        elif (not w.gov[i]) and w.cls[i] >= 4 and r.random() < 0.24:
            k = int(r.integers(2, 5))
            others = [c for c in W.CODES if c != w.county[i]]
            extra = list(r.choice(others, k - 1, replace=False))
            shares = r.dirichlet(np.ones(k) * 2.5)
            shares = np.sort(shares)[::-1]
            w.sites[i] = list(zip([w.county[i]] + extra, shares))


def healthy_change(w, c):
    """a county's December 2025 to December 2026 change with the fourth-quarter shock's employers left out"""
    m = (w.county == c) & ~((w.distress_q == W.FLASH_Q) & w.exposed)
    return w.jobs[m, 47].sum() / w.jobs[m, 35].sum() - 1


def build(seed=W.SEED):
    """two passes: the first measures each county's change under the trend alone, the second offsets each
    county's drift so the change (the shock's employers apart) lands on the county's trend"""
    w0 = _build(seed, {})
    target = {c[0]: c[3] for c in W.COUNTIES}
    off = {c: math.log((1 + target[c]) / (1 + healthy_change(w0, c))) + W.NUDGE[c] for c in W.CODES}
    w = _build(seed, off)
    w.calibration = off
    return w
