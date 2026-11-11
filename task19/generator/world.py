"""task19 world: Kilvarra's people from mid-2021 to 30 June 2026 and the health register's records of them.

The simulation runs the processes that make the files: births, deaths, emigration and immigration, moves between
districts, students leaving home for the two university districts, serving personnel at Fort Larrick, and the health
register's own behaviour (who registers and when, who deregisters on leaving, who re-registers after a move, the
duplicates a re-registration leaves, contact with a practice, the 2024 list validation). A latent visibility trait
sets how readily each person shows up in any system; it is never written to a file.

The clean truth (who usually lived where on 30 June 2026) is kept beside the records for the checks."""
import math

import numpy as np

import params as PR

SQ2 = math.sqrt(2.0)


def Phi(x):
    x = np.asarray(x, dtype=float)
    # Abramowitz and Stegun 7.1.26 on |x|, error under 1.5e-7
    z = np.abs(x) / SQ2
    t = 1.0 / (1.0 + 0.3275911 * z)
    poly = t * (0.254829592 + t * (-0.284496736 + t * (1.421413741 + t * (-1.453152027 + t * 1.061405429))))
    erf = 1.0 - poly * np.exp(-z * z)
    return 0.5 * (1.0 + np.sign(x) * erf)


ND = len(PR.DISTRICTS)
DCODE = [d[0] for d in PR.DISTRICTS]
DNAME = [d[1] for d in PR.DISTRICTS]
DTYPE = [d[3] for d in PR.DISTRICTS]
UNI_IDX = [DCODE.index(c) for c in PR.UNIVERSITY]
GAR_IDX = DCODE.index(PR.GARRISON)


def band_rate(table, age):
    out = np.zeros(len(age))
    for (lo, hi), r in table.items():
        out[(age >= lo) & (age < hi)] = r
    return out


def base_age_weights():
    """A single-year age profile for mid-2021: a mature island population with a baby boom echo in the thirties."""
    a = np.arange(100)
    w = np.where(a < 20, 1.16 - 0.004 * a, 0.0)
    w = w + np.where((a >= 20) & (a < 60), 1.10 - 0.002 * (a - 20) + 0.10 * np.exp(-((a - 36) / 7.0) ** 2), 0.0)
    w = w + np.where(a >= 60, 1.0 * np.exp(-(np.clip(a - 60, 0, None) / 17.0) ** 1.6), 0.0)
    return w / w.sum()


def mortality(age, sex):
    """Annual death probability, in the three parts of a Heligman-Pollard schedule: infant and childhood deaths falling
    away after birth, a young adults' accident hump (much larger for men), and a Gompertz curve; men higher."""
    a = np.asarray(age, dtype=float)
    men = np.asarray(sex) == 1
    q = 0.00004 * np.exp(0.092 * a) * np.where(men, 1.45, 1.0)
    q = q + np.where(a < 1, 0.003, 0.00018 * np.exp(-0.4 * a))
    q = q + np.where(men, 0.0007, 0.0001) * np.exp(-8.0 * np.log(np.maximum(a, 1.0) / 21.0) ** 2)
    return np.minimum(q, 0.6)


def _survival(sex):
    a = np.arange(101)
    q = mortality(a, np.full(101, sex))
    return np.concatenate([[1.0], np.cumprod(1 - q)[:-1]])


SURV_M, SURV_F = _survival(1), _survival(0)
SURV_RATIO = SURV_M / SURV_F


class People:
    """Columnar person table that grows as people are born and arrive."""
    FIELDS = dict(sex=np.int8, dob=np.int32, nat=np.int8, origin=np.int8, v=np.float32, offgrid=np.bool_,
                  dist=np.int8, home=np.int8, status=np.int8, arrive=np.int32, leave=np.int32, student=np.bool_,
                  study_end=np.int16, forces=np.bool_, born_here=np.bool_, prev=np.int8, emig_rec=np.bool_,
                  border_dep=np.bool_, imm_rec=np.bool_, dereg=np.bool_)
    # status: 0 resident, 1 emigrated, 2 died, 9 former resident who had left before 2021 (legacy record only)

    def __init__(self, cap):
        self.n = 0
        self.cap = cap
        for k, t in self.FIELDS.items():
            setattr(self, k, np.zeros(cap, dtype=t))

    def add(self, **cols):
        m = len(next(iter(cols.values())))
        if self.n + m > self.cap:
            raise RuntimeError("person table full")
        sl = slice(self.n, self.n + m)
        for k, v in cols.items():
            getattr(self, k)[sl] = v
        self.n += m
        return np.arange(sl.start, sl.stop)

    def view(self, k):
        return getattr(self, k)[: self.n]


class Records:
    """The health register's records: one per registration, closed when removed."""
    FIELDS = dict(pid=np.int32, dist=np.int8, reg=np.int32, last=np.int32, open=np.bool_, closed=np.int32,
                  why=np.int8, stale_within=np.bool_)
    # why: 0 open, 1 death notified, 2 emigration notified, 3 closed on re-registration, 4 removed in the 2024
    # validation, 5 birth not yet registered (never opened)

    def __init__(self, cap):
        self.n = 0
        self.cap = cap
        for k, t in self.FIELDS.items():
            setattr(self, k, np.zeros(cap, dtype=t))

    def add(self, **cols):
        m = len(next(iter(cols.values())))
        if self.n + m > self.cap:
            raise RuntimeError("record table full")
        sl = slice(self.n, self.n + m)
        for k, v in cols.items():
            getattr(self, k)[sl] = v
        self.open[sl] = True
        self.n += m
        return np.arange(sl.start, sl.stop)

    def view(self, k):
        return getattr(self, k)[: self.n]


def visibility(rng, n, sex, age, nat, dtype_idx):
    v = rng.normal(0.0, PR.VIS_SD, n)
    ym = (sex == 1) & (age >= 18) & (age < 36)
    v[ym] = rng.normal(PR.VIS_YOUNG_MALE[0], PR.VIS_YOUNG_MALE[1], ym.sum())
    v = v + np.where(nat == 1, PR.VIS_NONNAT, 0.0)
    og_rate = np.where(nat == 1, PR.OFFGRID["nonnational"], PR.OFFGRID["national"])
    og_rate = og_rate * np.array([PR.OFFGRID_MULT[DTYPE[d]] for d in dtype_idx])
    og = (sex == 1) & (age >= 18) & (age < 41) & (rng.random(n) < og_rate)
    v = v + np.where(og, PR.OFFGRID_SHIFT, 0.0)
    return v.astype(np.float32), og


def contact_prob(age, sex, v):
    """Probability of at least one contact with the practice in a year."""
    base = np.where(age < 5, 1.6, np.where(age < 18, 0.65, np.where(age < 45, 0.62, np.where(age < 70, 0.95, 1.4))))
    base = base - np.where((sex == 1) & (age >= 16) & (age < 60), 0.35, 0.0)
    return Phi(base + 0.55 * v)


def ages_at(dob, when):
    return ((when - dob) / 365.25).astype(np.int32)


def build(seed=PR.SEED):
    rng = np.random.default_rng(seed)
    P = People(700_000)
    R = Records(900_000)
    W = {"rng_seed": seed, "events": []}
    aw = base_age_weights()

    # ---------------------------------------------------------------- mid-2021 population
    for di, d in enumerate(PR.DISTRICTS):
        code, name, pc, typ, pop, nn, young, old = d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7]
        a = np.arange(100)
        tilt = np.where((a >= 18) & (a < 40), young, 1.0) * np.where(a >= 62, old, 1.0)
        if typ == "university":
            tilt = tilt * np.where((a >= 18) & (a < 23), 1.0, 1.0)
        w = aw * tilt
        w = w / w.sum()
        age = rng.choice(100, size=pop, p=w)
        nat = (rng.random(pop) < nn * np.where((age >= 20) & (age < 45), 1.7, np.where(age >= 60, 0.25, 0.6)))
        nat = nat.astype(np.int8)
        # nationals' sex follows their birth cohort's sex ratio and the two sexes' survival since birth
        srb = 1.052 + 0.008 * np.sin((PR.T0 / 365.25 - age) * 0.7) + rng.normal(0, 0.004, pop)
        surv = SURV_RATIO[np.clip(age, 0, 99)]
        r = srb * surv
        pm = np.where(nat == 0, r / (1 + r), np.where((age >= 18) & (age < 45), 0.535, 0.51))
        sex = (rng.random(pop) < pm).astype(np.int8)
        if typ == "garrison":
            forces = (age >= 18) & (age < 45) & (rng.random(pop) < PR.FORCES_SHARE) & (rng.random(pop) < np.where(sex == 1, 1.0, 0.0) + 0.17)
            sex = np.where(forces & (rng.random(pop) < 0.86), 1, sex).astype(np.int8)
        else:
            forces = np.zeros(pop, dtype=bool)
        dob = PR.T0 - (age * 365.25).astype(np.int32) - rng.integers(0, 365, pop)
        origin = np.where(nat == 1, 1 + rng.choice(len(PR.ORIGINS), size=pop, p=[o[1] for o in PR.ORIGINS]), 0)
        v, og = visibility(rng, pop, sex, age, nat, np.full(pop, di))
        arrive = np.where(nat == 1, PR.T0 - rng.integers(200, 365 * 10, pop), dob)
        arrive = np.maximum(arrive, dob)
        P.add(sex=sex, dob=dob, nat=nat, origin=origin, v=v, offgrid=og, dist=np.full(pop, di), home=np.full(pop, di),
              status=np.zeros(pop), arrive=arrive, leave=np.zeros(pop), student=np.zeros(pop, bool),
              study_end=np.zeros(pop), forces=forces, born_here=(nat == 0), prev=np.full(pop, di),
              emig_rec=np.zeros(pop, bool), border_dep=np.zeros(pop, bool), imm_rec=np.zeros(pop, bool))

    # students already at university in 2021: a share of 18 to 22-year-olds now living in the university districts
    age0 = ages_at(P.view("dob"), PR.T0)
    st = (age0 >= 18) & (age0 <= 21) & (rng.random(P.n) < PR.STUDENT_GO * 0.9) & ~P.view("forces")
    st_idx = np.where(st)[0]
    P.home[st_idx] = P.dist[st_idx]
    P.dist[st_idx] = rng.choice(UNI_IDX, size=len(st_idx), p=[0.58, 0.42])
    P.student[st_idx] = True
    P.study_end[st_idx] = 2021 + rng.integers(1, 4, len(st_idx))

    # ---------------------------------------------------------------- the register in 2021
    n = P.n
    age0 = ages_at(P.view("dob"), PR.T0)
    v = P.view("v").astype(float)
    regp = Phi(PR.REG_A + PR.REG_B * v)
    has = (rng.random(n) < regp) & ~P.view("forces")
    # serving personnel: some keep a civilian record at a former address
    has = has | (P.view("forces") & (rng.random(n) < PR.FORCES_CIVIL_RECORD))
    idx = np.where(has)[0]
    rdist = P.view("dist")[idx].copy()
    # students: registered at university only if they re-registered
    stu = P.view("student")[idx]
    keep_home = stu & (rng.random(len(idx)) >= PR.STUDENT_REREG)
    rdist[keep_home] = P.view("home")[idx][keep_home]
    forces_rec = P.view("forces")[idx]
    rdist[forces_rec] = rng.integers(0, ND, forces_rec.sum())
    rdist[forces_rec & (rdist == GAR_IDX)] = 0
    # stale addresses among young adults: registered in an earlier district
    stale = (age0[idx] >= 18) & (age0[idx] < 45) & (rng.random(len(idx)) < PR.STALE_2021) & ~stu
    rdist[stale] = rng.integers(0, ND, stale.sum())
    regd = np.maximum(P.view("dob")[idx] + rng.integers(0, 60, len(idx)),
                      PR.T0 - (rng.exponential(9 * 365, len(idx))).astype(np.int32))
    regd = np.maximum(regd, P.view("arrive")[idx] + rng.integers(10, 400, len(idx)))
    regd = np.minimum(regd, PR.T0 - 1)
    cp = contact_prob(age0[idx], P.view("sex")[idx], v[idx])
    gap = rng.geometric(np.clip(cp, 0.02, 0.999)) - 1
    last = PR.T0 - (gap * 365 + rng.integers(0, 365, len(idx))).astype(np.int32)
    last = np.maximum(last, regd)
    R.add(pid=idx.astype(np.int32), dist=rdist, reg=regd, last=last, closed=np.zeros(len(idx)), why=np.zeros(len(idx)),
          stale_within=np.zeros(len(idx), bool))
    # duplicates from earlier re-registrations
    dup_src = idx[rng.random(len(idx)) < PR.DUP_2021]
    if len(dup_src):
        ddist = np.where(rng.random(len(dup_src)) < 0.6, P.view("dist")[dup_src], rng.integers(0, ND, len(dup_src)))
        dreg = PR.T0 - (rng.exponential(6 * 365, len(dup_src))).astype(np.int32) - 200
        dlast = np.minimum(dreg + rng.integers(0, 3 * 365, len(dup_src)), PR.T0 - 400)
        dlast = np.maximum(dlast, dreg)
        R.add(pid=dup_src.astype(np.int32), dist=ddist, reg=dreg, last=dlast, closed=np.zeros(len(dup_src)),
              why=np.zeros(len(dup_src)), stale_within=np.zeros(len(dup_src), bool))
    # people who had left before 2021 and are still listed
    nleg = int(PR.LEGACY_GHOSTS * R.n)
    wdist = np.array([d[5] for d in PR.DISTRICTS]) * np.array([d[4] for d in PR.DISTRICTS])
    wdist = 0.5 * wdist / wdist.sum() + 0.5 * np.array([d[4] for d in PR.DISTRICTS]) / sum(d[4] for d in PR.DISTRICTS)
    ldist = rng.choice(ND, size=nleg, p=wdist)
    lnat = (rng.random(nleg) < 0.55).astype(np.int8)
    lage = np.clip(rng.normal(36, 13, nleg), 1, 90).astype(int)
    lsex = (rng.random(nleg) < 0.54).astype(np.int8)
    ldob = PR.T0 - (lage * 365.25).astype(np.int32) - rng.integers(0, 365, nleg)
    lleave = PR.T0 - (rng.uniform(0.05, 10.5, nleg) * 365).astype(np.int32)
    lpid = P.add(sex=lsex, dob=ldob, nat=lnat,
                 origin=np.where(lnat == 1, 1 + rng.choice(len(PR.ORIGINS), size=nleg, p=[o[1] for o in PR.ORIGINS]), 0),
                 v=rng.normal(0, PR.VIS_SD, nleg).astype(np.float32), offgrid=np.zeros(nleg, bool), dist=np.full(nleg, -1),
                 home=ldist, status=np.full(nleg, 9), arrive=ldob, leave=lleave, student=np.zeros(nleg, bool),
                 study_end=np.zeros(nleg), forces=np.zeros(nleg, bool), born_here=(lnat == 0), prev=ldist,
                 emig_rec=np.zeros(nleg, bool), border_dep=np.zeros(nleg, bool), imm_rec=np.zeros(nleg, bool))
    lreg = lleave - (rng.exponential(5 * 365, nleg)).astype(np.int32) - 30
    lreg = np.maximum(lreg, ldob)
    llast = np.maximum(lleave - rng.integers(0, 2 * 365, nleg), lreg)
    R.add(pid=lpid.astype(np.int32), dist=ldist, reg=lreg, last=llast, closed=np.zeros(nleg), why=np.zeros(nleg),
          stale_within=np.zeros(nleg, bool))

    W["census_records"] = R.n
    W["last2021"] = R.view("last").copy()
    # ---------------------------------------------------------------- census 2021 enumeration (kept for its files)
    n2021 = P.n
    res2021 = np.where(P.view("status") == 0)[0]
    cens_p = Phi(PR.CENS_A + PR.CENS_B * P.view("v")[res2021].astype(float))
    W["census_enum"] = res2021[rng.random(len(res2021)) < cens_p]
    W["res2021"] = res2021
    W["dist2021"] = P.view("dist")[res2021].copy()
    W["truth2021"] = census_table(P, res2021, rng)
    W["records2021"] = R.n

    # ---------------------------------------------------------------- the five years to 30 June 2026
    move_attr = np.array([d[8] for d in PR.DISTRICTS])
    comp = {}
    for yi, year in enumerate(PR.YEARS):
        y0, y1 = PR.T0 + 365 * yi, PR.T0 + 365 * (yi + 1)
        c = {"births": 0, "deaths": 0, "imm": 0, "imm_rec": 0, "emig": 0, "emig_rec": 0}
        res = np.where(P.view("status") == 0)[0]
        age = ages_at(P.view("dob")[res], y0)
        sex = P.view("sex")[res]
        when = y0 + rng.integers(1, 365, len(res))
        # deaths
        dies = rng.random(len(res)) < mortality(age, sex)
        di = res[dies]
        P.status[di] = 2
        P.leave[di] = when[dies]
        c["deaths"] = int(dies.sum())
        # emigration
        nat = P.view("nat")[res]
        recent = (y0 - P.view("arrive")[res]) < 730
        er = np.where(nat == 1, PR.EMIG_NN + np.where(recent, PR.EMIG_NN_RECENT, 0.0), band_rate(PR.EMIG_NAT, age))
        er = np.where(P.view("forces")[res], 0.0, er)
        em = (rng.random(len(res)) < er) & ~dies
        ei = res[em]
        P.status[ei] = 1
        P.leave[ei] = when[em]
        P.border_dep[ei] = (P.nat[ei] == 1) & (rng.random(len(ei)) < PR.BORDER_DEPART_CAPTURE)
        # register: deaths notified, a share of emigrants deregister; the accounts record an emigrant who told the
        # register, and a non-national whose departure the border system caught
        _close_for(R, P, di, when[dies], 1, rng.random(len(di)) < PR.DEATH_NOTIFY)
        dereg = rng.random(len(ei)) < np.where(P.nat[ei] == 1, PR.DEREG["nonnational"], PR.DEREG["national"])
        P.dereg[ei] = dereg
        P.emig_rec[ei] = dereg | P.border_dep[ei]
        c["emig"] = int(em.sum())
        c["emig_rec"] = int(P.emig_rec[ei].sum())
        c["emig_m"] = int((P.sex[ei] == 1).sum())
        c["deaths_by"] = np.bincount(np.clip(age[dies] // 5, 0, 18) * 2 + sex[dies], minlength=38)
        _close_for(R, P, ei, when[em], 2, dereg)
        # births
        res = np.where(P.view("status") == 0)[0]
        mothers = res[(P.view("sex")[res] == 0) & (ages_at(P.view("dob")[res], y0) >= 18) & (ages_at(P.view("dob")[res], y0) < 45)]
        nb = rng.binomial(len(res), PR.FERTILITY)
        mom = rng.choice(mothers, size=nb)
        bdob = y0 + rng.integers(1, 365, nb)
        bsex = (rng.random(nb) < 0.513).astype(np.int8)
        bdist = P.view("dist")[mom]
        bdist = np.where(P.view("student")[mom], P.view("home")[mom], bdist)
        bdist = np.where(P.view("forces")[mom], GAR_IDX, bdist)
        bnat = P.view("nat")[mom]
        bv, bog = visibility(rng, nb, bsex, np.zeros(nb, int), bnat, bdist)
        bv = (0.5 * bv + 0.5 * P.view("v")[mom]).astype(np.float32)
        bid = P.add(sex=bsex, dob=bdob, nat=bnat, origin=P.view("origin")[mom], v=bv, offgrid=np.zeros(nb, bool),
                    dist=bdist, home=bdist, status=np.zeros(nb), arrive=bdob, leave=np.zeros(nb), student=np.zeros(nb, bool),
                    study_end=np.zeros(nb), forces=np.zeros(nb, bool), born_here=np.ones(nb, bool), prev=bdist,
                    emig_rec=np.zeros(nb, bool), border_dep=np.zeros(nb, bool), imm_rec=np.zeros(nb, bool))
        c["births"] = nb
        c["births_m"] = int(bsex.sum())
        # birth registration with a practice: complete for earlier years, lagging for the latest
        if year == PR.YEARS[-1]:
            lag = rng.exponential(110, nb)
            on = bdob + lag < PR.REF
        else:
            on = rng.random(nb) < 0.995
        bi = bid[on]
        R.add(pid=bi.astype(np.int32), dist=P.view("dist")[bi], reg=(P.view("dob")[bi] + rng.integers(14, 90, len(bi))).clip(None, y1 - 1),
              last=np.minimum(P.view("dob")[bi] + rng.integers(20, 300, len(bi)), y1 - 1), closed=np.zeros(len(bi)),
              why=np.zeros(len(bi)), stale_within=np.zeros(len(bi), bool))
        # immigration
        pop_now = len(res)
        ni = rng.binomial(pop_now, PR.IMMIGRATION[year])
        iret = rng.random(ni) < PR.RETURNING_NATIONALS
        iage = np.clip(rng.gamma(5.5, 5.4, ni), 0, 80).astype(int)
        iage = np.where(rng.random(ni) < 0.12, rng.integers(0, 15, ni), iage)
        isex = (rng.random(ni) < np.where(iage >= 18, 0.53, 0.51)).astype(np.int8)
        inat = np.where(iret, 0, 1).astype(np.int8)
        wimm = np.array([d[5] for d in PR.DISTRICTS]) * np.array([d[4] for d in PR.DISTRICTS])
        idist = rng.choice(ND, size=ni, p=wimm / wimm.sum())
        iarr = y0 + rng.integers(1, 365, ni)
        idob = iarr - (iage * 365.25).astype(np.int32) - rng.integers(0, 365, ni)
        iv, iog = visibility(rng, ni, isex, iage, inat, idist)
        iid = P.add(sex=isex, dob=idob, nat=inat, origin=np.where(inat == 1, 1 + rng.choice(len(PR.ORIGINS), size=ni, p=[o[1] for o in PR.ORIGINS]), 0),
                    v=iv, offgrid=iog, dist=idist, home=idist, status=np.zeros(ni), arrive=iarr, leave=np.zeros(ni),
                    student=np.zeros(ni, bool), study_end=np.zeros(ni), forces=np.zeros(ni, bool),
                    born_here=(inat == 0) & (rng.random(ni) < 0.9), prev=idist, emig_rec=np.zeros(ni, bool),
                    border_dep=np.zeros(ni, bool), imm_rec=rng.random(ni) < PR.OFFICIAL_IMM_RECORDED)
        c["imm"] = ni
        c["imm_rec"] = int(P.imm_rec[iid].sum())
        c["imm_rec_nn"] = int((P.imm_rec[iid] & (P.nat[iid] == 1)).sum())
        c["imm_nn"] = int((P.nat[iid] == 1).sum())
        # arrivals register with a practice, some late
        regp = Phi(PR.ARRIVAL_REG_A + PR.REG_B * iv.astype(float))
        first = rng.random(ni) < regp
        fi = iid[first]
        R.add(pid=fi.astype(np.int32), dist=P.view("dist")[fi], reg=np.minimum(P.view("arrive")[fi] + rng.integers(7, 200, len(fi)), y1 - 1),
              last=np.minimum(P.view("arrive")[fi] + rng.integers(7, 330, len(fi)), y1 - 1), closed=np.zeros(len(fi)),
              why=np.zeros(len(fi)), stale_within=np.zeros(len(fi), bool))
        # late registration of earlier residents with no open record
        res = np.where(P.view("status") == 0)[0]
        opened = np.zeros(P.n, bool)
        ov = R.view("open")
        opened[R.view("pid")[ov]] = True
        unreg = res[~opened[res] & ~P.view("forces")[res]]
        late = unreg[rng.random(len(unreg)) < PR.LATE_REG * Phi(0.4 + 0.6 * P.view("v")[unreg].astype(float))]
        lw = y0 + rng.integers(1, 365, len(late))
        R.add(pid=late.astype(np.int32), dist=P.view("dist")[late], reg=lw, last=lw, closed=np.zeros(len(late)),
              why=np.zeros(len(late)), stale_within=np.zeros(len(late), bool))
        # moves between districts
        res = np.where((P.view("status") == 0) & ~P.view("forces") & ~P.view("student"))[0]
        age = ages_at(P.view("dob")[res], y0)
        mv = rng.random(len(res)) < band_rate(PR.MOVE_RATE, age)
        mi = res[mv]
        # children move with a parent: approximated by their own draw at the lower rate
        dest = rng.choice(ND, size=len(mi), p=move_attr / move_attr.sum())
        same = dest == P.view("dist")[mi]
        dest[same] = rng.choice(ND, size=same.sum(), p=move_attr / move_attr.sum())
        mi, dest = mi[dest != P.view("dist")[mi]], dest[dest != P.view("dist")[mi]]
        mwhen = y0 + rng.integers(1, 365, len(mi))
        P.prev[mi] = P.dist[mi]
        P.dist[mi] = dest
        P.home[mi] = dest
        mage = ages_at(P.view("dob")[mi], y0)
        rereg = rng.random(len(mi)) < band_rate(PR.REREG, mage) * Phi(1.0 + 0.6 * P.view("v")[mi].astype(float))
        _move_records(R, P, rng, mi[rereg], mwhen[rereg], dest[rereg])
        # movers still registered only at an earlier district register where they live now, some each year
        res = np.where((P.view("status") == 0) & ~P.view("forces"))[0]
        o = np.where(R.view("open"))[0]
        here_rec = np.zeros(P.n, bool)
        here_rec[R.view("pid")[o][P.view("dist")[R.view("pid")[o]] == R.view("dist")[o]]] = True
        any_rec = np.zeros(P.n, bool)
        any_rec[R.view("pid")[o]] = True
        away = res[any_rec[res] & ~here_rec[res] & ~P.view("student")[res]]
        lr = away[rng.random(len(away)) < PR.LATE_REREG * Phi(0.6 + 0.6 * P.view("v")[away].astype(float))]
        _move_records(R, P, rng, lr, y0 + rng.integers(1, 365, len(lr)), P.view("dist")[lr])
        # students: 18-year-olds leaving home, finishing students going home or moving on
        res = np.where((P.view("status") == 0) & ~P.view("forces"))[0]
        age = ages_at(P.view("dob")[res], y0)
        go = res[(age == 18) & ~P.view("student")[res] & (rng.random(len(res)) < PR.STUDENT_GO)]
        P.home[go] = P.dist[go]
        P.dist[go] = rng.choice(UNI_IDX, size=len(go), p=[0.58, 0.42])
        P.student[go] = True
        P.study_end[go] = year + rng.integers(PR.STUDY_YEARS[0], PR.STUDY_YEARS[1] + 1, len(go))
        rr = rng.random(len(go)) < PR.STUDENT_REREG
        _move_records(R, P, rng, go[rr], y0 + rng.integers(60, 120, rr.sum()), P.view("dist")[go[rr]])
        fin = np.where((P.view("status") == 0) & P.view("student") & (P.view("study_end") <= year))[0]
        P.student[fin] = False
        back = rng.random(len(fin)) < 0.55
        P.dist[fin[back]] = P.home[fin[back]]
        on = fin[~back]
        P.dist[on] = rng.choice(ND, size=len(on), p=move_attr / move_attr.sum())
        P.home[fin] = P.dist[fin]
        rr = rng.random(len(fin)) < 0.55
        _move_records(R, P, rng, fin[rr], y0 + rng.integers(1, 365, rr.sum()), P.view("dist")[fin[rr]])
        # the Defence Forces: a share leave the service each year, replaced by recruits aged 18 to 21
        srv = np.where((P.view("status") == 0) & P.view("forces"))[0]
        sage = ages_at(P.view("dob")[srv], y0)
        out = srv[(rng.random(len(srv)) < PR.FORCES_TURNOVER) | (sage >= 44)]
        P.forces[out] = False
        stay = rng.random(len(out)) < 0.45
        moved_out = out[~stay]
        P.prev[moved_out] = GAR_IDX
        P.dist[moved_out] = rng.choice(ND, size=len(moved_out), p=move_attr / move_attr.sum())
        P.home[out] = P.dist[out]
        lv = out[rng.random(len(out)) < 0.8]
        if len(lv):
            _move_records(R, P, rng, lv, y0 + rng.integers(1, 365, len(lv)), P.view("dist")[lv])
        pool = np.where((P.view("status") == 0) & ~P.view("forces") & ~P.view("student") & (P.view("nat") == 0))[0]
        pa = ages_at(P.view("dob")[pool], y0)
        pool = pool[(pa >= 18) & (pa <= 21)]
        rec = pool[rng.choice(len(pool), size=min(len(pool), len(out)), replace=False)]
        rec = rec[rng.random(len(rec)) < np.where(P.sex[rec] == 1, 1.0, 0.2)]
        P.forces[rec] = True
        P.prev[rec] = P.dist[rec]
        P.dist[rec] = GAR_IDX
        P.home[rec] = GAR_IDX
        # a recruit's civilian record is closed when the Defence Medical Service takes over, mostly
        sel = np.zeros(P.n, bool)
        sel[rec[rng.random(len(rec)) < 0.85]] = True
        oo = np.where(R.view("open"))[0]
        hit = oo[sel[R.view("pid")[oo]]]
        R.open[hit] = False
        R.closed[hit] = y0 + rng.integers(1, 365, len(hit))
        R.why[hit] = 3
        # contact with the practice this year
        o = np.where(R.view("open"))[0]
        pid = R.view("pid")[o]
        alive = P.view("status")[pid] == 0
        here = alive & (P.view("dist")[pid] == R.view("dist")[o])
        oa = o[alive]
        pa = pid[alive]
        cp = contact_prob(ages_at(P.view("dob")[pa], y0), P.view("sex")[pa], P.view("v")[pa].astype(float))
        # a record at a district the person no longer lives in is rarely used
        cp = np.where(here[alive], cp, cp * 0.08)
        hit = rng.random(len(oa)) < cp
        newlast = y0 + rng.integers(1, 365, hit.sum())
        R.last[oa[hit]] = np.maximum(R.last[oa[hit]], np.minimum(newlast, y1 - 1))
        # the 2024 list validation
        if year == 2024:
            o = np.where(R.view("open"))[0]
            long_gap = (PR.CLEAN - R.view("last")[o]) >= 5 * 365
            rm = o[long_gap & (rng.random(len(o)) < PR.CLEAN_SHARE)]
            R.open[rm] = False
            R.closed[rm] = PR.CLEAN - rng.integers(0, 90, len(rm))
            R.why[rm] = 4
            W["cleaned"] = len(rm)
            W["cleaned_resident"] = int((P.status[R.pid[rm]] == 0).sum())
        comp[year] = c
    W["components"] = comp

    # within-district address changes nobody told the practice about
    o = np.where(R.view("open"))[0]
    pid = R.view("pid")[o]
    ok = (P.view("status")[pid] == 0) & (P.view("dist")[pid] == R.view("dist")[o])
    a = ages_at(P.view("dob")[pid], PR.REF)
    nat_o = P.view("nat")[pid]
    sw = ok & (rng.random(len(o)) < np.where((a >= 18) & (a < 45), 0.24, 0.11) + np.where(nat_o == 1, 0.08, 0.0))
    R.stale_within[o[sw]] = True
    # women whose surname changed on marriage after their record was made; many moved house at the same time
    sexo = P.view("sex")[pid]
    mar_p = (sexo == 0) & (a >= 22) & (a <= 45) & (R.view("reg")[o] < PR.REF - 3 * 365)
    married = np.zeros(P.n, bool)
    cand = np.unique(pid[mar_p])
    married[cand[rng.random(len(cand)) < PR.SURNAME_CHANGE_W]] = True
    mo = ok & married[pid] & (rng.random(len(o)) < PR.MARRIED_MOVED)
    R.stale_within[o[mo]] = True
    W["married"] = married
    W["P"], W["R"] = P, R
    W["truth"] = truth(P)
    return W


def census_table(P, res, rng):
    """The 2021 Census usual residents by district, five-year age group and sex, as published after its coverage
    adjustment: close to the truth, with the residual shortfalls a coverage survey leaves among young men and infants."""
    import pandas as pd
    age = ages_at(P.view("dob")[res], PR.T0)
    sex = P.view("sex")[res]
    nat = P.view("nat")[res]
    dist = P.view("dist")[res]
    g = np.minimum(age // 5, 18)
    err = np.where((sex == 1) & (age >= 18) & (age < 45), np.where(nat == 1, -0.020, -0.009),
                   np.where(age < 5, -0.006, 0.0015))
    key = dist.astype(int) * 38 + g * 2 + sex
    w = 1.0 + err
    est = np.bincount(key, weights=w, minlength=ND * 38)
    est = est * (1 + rng.normal(0, 0.004, len(est)))
    rows = []
    labels = ["0-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59",
              "60-64", "65-69", "70-74", "75-79", "80-84", "85-89", "90+"]
    for di in range(ND):
        for gg in range(19):
            rows.append([DCODE[di], DNAME[di], labels[gg], int(round(est[di * 38 + gg * 2 + 1])),
                         int(round(est[di * 38 + gg * 2]))])
    tab = pd.DataFrame(rows, columns=["district_code", "district", "age_group", "males", "females"])
    return {"table": tab, "census_estimate_total": int(tab["males"].sum() + tab["females"].sum())}


def _close_for(R, P, pids, when, why, mask):
    """Close every open record of the people in pids where mask is set."""
    if len(pids) == 0:
        return
    sel = np.zeros(P.n, bool)
    sel[pids[mask]] = True
    wmap = np.zeros(P.n, np.int32)
    wmap[pids] = when
    o = np.where(R.view("open"))[0]
    hit = o[sel[R.view("pid")[o]]]
    R.open[hit] = False
    R.closed[hit] = wmap[R.pid[hit]]
    R.why[hit] = why


def _move_records(R, P, rng, pids, when, dest):
    """A re-registration at the new district: a new record opens; the old one closes, except for a share left open as a
    duplicate."""
    if len(pids) == 0:
        return
    sel = np.zeros(P.n, bool)
    sel[pids] = True
    o = np.where(R.view("open"))[0]
    old = o[sel[R.view("pid")[o]]]
    keep = rng.random(len(old)) < PR.DUP_ON_REREG
    cl = old[~keep]
    wmap = np.zeros(P.n, np.int32)
    wmap[pids] = when
    R.open[cl] = False
    R.closed[cl] = wmap[R.pid[cl]]
    R.why[cl] = 3
    R.add(pid=pids.astype(np.int32), dist=dest, reg=when, last=when, closed=np.zeros(len(pids)), why=np.zeros(len(pids)),
          stale_within=np.zeros(len(pids), bool))


def truth(P):
    res = np.where(P.view("status") == 0)[0]
    d = P.view("dist")[res]
    return {"national": len(res), "district": np.bincount(d, minlength=ND)}


if __name__ == "__main__":
    import time
    t = time.time()
    W = build()
    P, R = W["P"], W["R"]
    print("built in %.1fs; persons %d, records %d" % (time.time() - t, P.n, R.n))
    tr = W["truth"]
    print("national", tr["national"])
    reg = np.bincount(R.view("dist")[R.view("open")], minlength=ND)
    for i in range(ND):
        print("%-12s truth %6d register %6d  %+.2f%%" % (DNAME[i], tr["district"][i], reg[i], 100 * (reg[i] / tr["district"][i] - 1)))
    print("register", reg.sum(), "%+.2f%%" % (100 * (reg.sum() / tr["national"] - 1)))
    print({k: v for k, v in W["components"].items()})
    print("cleaned", W.get("cleaned"), "of them residents", W.get("cleaned_resident"))
