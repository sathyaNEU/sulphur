"""task22 architecture 2: the simulated gas system of Brandvold Public Utilities, from the weather and the soil to what
each meter registers, each regulator station's corrector records and each read the billing system takes.

Units: true use is Mcf at base conditions (14.73 psia, 60 F); a meter registers actual volume at its own pressure
and gas temperature, in ccf; a temperature-compensating meter registers volume referred to 60 F. The billing
system multiplies registered ccf by the pressure factor PF and, for every meter, by nothing else.
"""
import datetime as dt

import numpy as np
import pandas as pd

import params as P


def _rng(k):
    return np.random.default_rng([P.SEED, k])


class World:
    pass


# ----------------------------------------------------------------------------------------------- calendar, weather
def calendar(w):
    w.days = pd.date_range(P.SIM0, P.SIM1, freq="D")
    w.D = len(w.days)
    w.dates = np.array([d.date() for d in w.days])


def _win(w, a, b):
    return (w.days >= pd.Timestamp(a)) & (w.days <= pd.Timestamp(b))


def weather(w):
    rng = _rng(1)
    doy = w.days.dayofyear.values
    norm = 43.0 - 31.0 * np.cos(2 * np.pi * (doy - 22) / 365.25)
    e = np.zeros(w.D)
    for i in range(1, w.D):
        e[i] = 0.72 * e[i - 1] + rng.normal(0, 6.0)
    damp = np.ones(w.D)
    for y in (2023, 2024, 2025, 2026):
        damp[_win(w, "%d-09-12" % y, "%d-10-25" % y)] = 0.35
    air = norm + e * damp
    for a, b, d in [("2023-12-01", "2024-02-29", 8.0), ("2024-12-20", "2025-02-20", -4.0),
                    ("2025-12-01", "2026-02-28", -3.0), ("2025-10-01", "2025-10-11", -6.5),
                    ("2026-09-22", "2026-10-03", 2.5)]:
        air[_win(w, a, b)] += d
    w.air = air
    w.tmax = air + 9.5 + rng.normal(0, 2.2, w.D)
    w.tmin = air - 9.5 + rng.normal(0, 2.2, w.D)
    # snow on the ground: the snowless El Nino winter of 2023-24, a late thin cover in 2024-25, deep snow from the
    # second week of November 2025 to the end of March 2026
    snow = np.zeros(w.D)

    def seg(a, b, depth, ramp):
        idx = np.where(_win(w, a, b))[0]
        for j, i in enumerate(idx):
            snow[i] = max(snow[i], depth * min(1.0, (j + 1) / ramp) * min(1.0, (len(idx) - j) / ramp))
    seg("2023-12-28", "2024-01-25", 3.0, 8)
    seg("2024-12-28", "2025-03-05", 6.0, 10)
    seg("2025-11-10", "2026-03-28", 11.0, 6)
    seg("2026-11-01", "2026-11-04", 1.0, 2)
    w.snow_depth = np.round(snow * (1 + rng.normal(0, 0.08, w.D)).clip(0.7, 1.3), 0).clip(0)
    w.precip = np.where(rng.random(w.D) < 0.28, rng.gamma(0.8, 0.22, w.D), 0.0)
    w.snowfall = np.where((w.air < 33) & (w.precip > 0), w.precip * 11, 0.0)
    ws = 1 - np.exp(-snow / 4.0)
    surf = ws * 31.0 + (1 - ws) * air
    s20 = np.zeros(w.D)
    s40 = np.zeros(w.D)
    s2 = np.zeros(w.D)
    s4 = np.zeros(w.D)
    s8 = np.zeros(w.D)
    s20[0], s40[0], s2[0], s4[0], s8[0] = 66.0, 63.0, 70.0, 69.0, 68.0
    for i in range(1, w.D):
        s2[i] = s2[i - 1] + 0.42 * (surf[i] - s2[i - 1])
        s4[i] = s4[i - 1] + 0.30 * (s2[i] - s4[i - 1])
        s8[i] = s8[i - 1] + 0.20 * (s4[i] - s8[i - 1])
        s20[i] = s20[i - 1] + 0.075 * (surf[i] - s20[i - 1]) + 0.006 * (46 - s20[i - 1])
        s40[i] = s40[i - 1] + 0.035 * (s20[i] - s40[i - 1]) + 0.004 * (46 - s40[i - 1])
    w.s2, w.s4, w.s8, w.s20, w.s40 = s2, s4, s8, s20, s40
    w.hdd60 = np.clip(60.0 - air, 0, None)
    w.hdd_eff = 0.7 * w.hdd60 + 0.3 * np.concatenate([[w.hdd60[0]], w.hdd60[:-1]])


# ------------------------------------------------------------------------------------------------------- premises
MODELS_NTC = ["S175", "D250", "D275"]
MODELS_TC = ["D250TC", "D275TC"]
COM_NTC = ["D425", "D630"]
COM_TC = ["D425TC", "D630TC"]


def premises(w):
    rng = _rng(2)
    rows = []
    for d in P.DISTRICTS:
        for cls, n in (("RES", d["res"]), ("COM", d["com"])):
            for _ in range(n):
                rows.append(dict(premise=0, district=d["code"], cls=cls))
    pr = pd.DataFrame(rows)
    pr["key"] = rng.permutation(len(pr)) * 3 + rng.integers(0, 3, len(pr))
    pr = pr.sort_values("key").reset_index(drop=True)
    # premise numbers as the city assigned them over the decades: unique, irregular gaps
    pr["premise"] = np.sort(_rng(102).choice(np.arange(3100000, 3299999), len(pr), replace=False))
    pr = pr.drop(columns="key")
    n = len(pr)
    dd = {d["code"]: d for d in P.DISTRICTS}
    ntc = pr["district"].map(lambda c: dd[c]["ntc"]).values
    out = pr["district"].map(lambda c: dd[c]["out"]).values
    pr["tc"] = rng.random(n) > ntc
    pr["outdoor"] = np.where(pr["tc"], rng.random(n) < 0.92, rng.random(n) < out)
    pr["cycle"] = [int(rng.choice(dd[c]["cycles"])) for c in pr["district"]]
    res = (pr["cls"] == "RES").values
    pr["base"] = np.where(res, rng.normal(0.056, 0.012, n).clip(0.02), rng.lognormal(np.log(0.45), 0.55, n))
    pr["slope"] = np.where(res, rng.normal(0.0105, 0.0025, n).clip(0.003), rng.lognormal(np.log(0.035), 0.5, n))
    kind = np.array(["occ"] * n, dtype=object)
    r = rng.random(n)
    stu = pr["district"].map(lambda c: dd[c]["stu"]).values
    sbo = pr["district"].map(lambda c: dd[c]["sbo"]).values
    sbn = pr["district"].map(lambda c: dd[c]["sbn"]).values
    kind[res & (r < stu)] = "student"
    kind[res & (r >= stu) & (r < stu + sbo)] = "snowbird"
    kind[res & (r >= stu + sbo) & (r < stu + sbo + sbn)] = "snowbird_new"
    pr["kind"] = kind
    pr.loc[pr["kind"] == "student", "slope"] *= 1.12
    # gas temperature characteristics of each meter set
    pr["k_air"] = rng.normal(0.18, 0.035, n).clip(0.08, 0.30)
    pr["wall"] = rng.normal(2.0, 0.8, n).clip(0.0, 4.0)
    pr["basement"] = rng.normal(57.5, 1.8, n)
    # meter models, install years
    pr["model"] = [rng.choice(MODELS_TC if tc else MODELS_NTC) if c == "RES" else rng.choice(COM_TC if tc else COM_NTC)
                   for tc, c in zip(pr["tc"], pr["cls"])]
    pr["installed"] = [dt.date(int(rng.integers(2009, 2024)), int(rng.integers(1, 13)), int(rng.integers(1, 28)))
                       if tc else dt.date(int(rng.integers(1984, 2009)), int(rng.integers(1, 13)), int(rng.integers(1, 28)))
                       for tc in pr["tc"]]
    _ = [int(rng.integers(0, 9)) for _ in range(n)]          # the draws the old numbering took, kept in order
    serials = _rng(103).choice(np.arange(100000, 899999), n, replace=False)
    pr["meter"] = ["%s%06d" % ("R" if c == "RES" else "C", s_) for s_, c in zip(serials, pr["cls"])]
    pr["multiplier"] = np.where(res, 1, np.where(rng.random(n) < 0.35, 10, 1))
    w.pr = pr


def programs(w):
    """The 2024 and 2025 changeouts: non-compensating meters swapped for compensating ones, at the pace access
    allowed. The premises they reached were non-compensating when the year began; the current register shows the
    new meter."""
    rng = _rng(3)
    pr = w.pr
    pr["exch_date"] = None
    pr["old_model"] = None
    pr["old_meter"] = None
    pr["old_installed"] = None
    rows = []
    wo = 70412

    def lag(outdoor):
        if outdoor:
            if rng.random() < 0.03:
                return None
            return int(max(0, round(rng.normal(4, 6))))
        if rng.random() < 0.22:
            return None
        return int(round(rng.exponential(38)))

    new_serials = _rng(105).choice(np.arange(900000, 999999), 4000, replace=False)
    progs = [dict(district="WG", start=P.PROGRAM_2024["start"], end=P.PROGRAM_2024["end"], n=None, year=2024)]
    for p in P.PROGRAM_2025:
        progs.append(dict(p, year=2025))
    for p in progs:
        # the program's meters: in Westgate every non-compensating meter then present; elsewhere a block of routes
        dmask = (pr["district"] == p["district"]) & (pr["cls"] == "RES")
        if p["n"] is None:
            cand = pr.index[dmask & pr["tc"]].tolist()   # those the program made compensating (now TC)
            take = rng.choice(cand, int(len(cand) * 0.86), replace=False)
            done_tc = True
        else:
            cand = pr.index[dmask & ~pr["tc"]].tolist()
            take = rng.choice(cand, p["n"], replace=False)
            done_tc = False
        take = sorted(take, key=lambda i: (pr.at[i, "cycle"], pr.at[i, "premise"]))
        span = (p["end"] - p["start"]).days
        for j, i in enumerate(take):
            planned = p["start"] + dt.timedelta(days=int(span * j / max(1, len(take) - 1)))
            while planned.weekday() >= 5:
                planned += dt.timedelta(days=1)
            outdoor = bool(pr.at[i, "outdoor"])
            lg = lag(outdoor)
            done = None if lg is None else planned + dt.timedelta(days=lg)
            if done is not None:
                while done.weekday() >= 5:
                    done += dt.timedelta(days=1)
            status = "Completed" if done is not None else ("No access - card left" if not outdoor else "Customer refused")
            if done is not None and done > dt.date(p["year"], 12, 18):
                done, status = None, "Carried to next program"
            old_model = rng.choice(MODELS_NTC)
            if done is not None:
                pr.at[i, "exch_date"] = done
                pr.at[i, "old_model"] = old_model
                pr.at[i, "old_meter"] = pr.at[i, "meter"]
                pr.at[i, "old_installed"] = dt.date(int(rng.integers(1984, 2008)), int(rng.integers(1, 13)), 1)
                _ = int(rng.integers(0, 3))
                pr.at[i, "meter"] = "R%06d" % int(new_serials[len(rows)])
                pr.at[i, "model"] = rng.choice(MODELS_TC)
                pr.at[i, "installed"] = done
                pr.at[i, "tc"] = True
                pr.at[i, "outdoor"] = outdoor
            elif done_tc:
                # in Westgate the meters the program never reached stayed non-compensating
                pr.at[i, "tc"] = False
                pr.at[i, "model"] = old_model
            rows.append(dict(WorkOrder="WO-%d-%05d" % (p["year"], wo), Program="%d %s meter changeout" % (
                p["year"], P.DNAME[p["district"]]), PremiseID=int(pr.at[i, "premise"]),
                District=P.DNAME[p["district"]], MeterLocation="Outside" if outdoor else "Inside",
                PlannedDate=planned, CompletedDate=done, Status=status,
                OldMeter=pr.at[i, "old_meter"] if done is not None else pr.at[i, "meter"],
                NewMeter=pr.at[i, "meter"] if done is not None else None))
            wo += 1
    w.workorders = pd.DataFrame(rows)


def plan_2027(w):
    rng = _rng(4)
    pr = w.pr
    rows = []
    cand = pr.index[pr["district"].isin(P.PLAN_2027["districts"]) & ~pr["tc"]].tolist()
    cand = sorted(cand, key=lambda i: (P.PLAN_2027["districts"].index(pr.at[i, "district"]), pr.at[i, "cycle"],
                                       pr.at[i, "premise"]))
    span = (P.PLAN_2027["end"] - P.PLAN_2027["start"]).days
    for j, i in enumerate(cand):
        planned = P.PLAN_2027["start"] + dt.timedelta(days=int(span * j / max(1, len(cand) - 1)))
        while planned.weekday() >= 5:
            planned += dt.timedelta(days=1)
        rows.append(dict(Route="%s-%02d" % (pr.at[i, "district"], pr.at[i, "cycle"]), PremiseID=int(pr.at[i, "premise"]),
                         District=P.DNAME[pr.at[i, "district"]], MeterID=pr.at[i, "meter"], Model=pr.at[i, "model"],
                         MeterLocation="Outside" if pr.at[i, "outdoor"] else "Inside", PlannedDate=planned))
    w.plan2027 = pd.DataFrame(rows)


# ------------------------------------------------------------------------------------------------- occupancy, use
def accounts(w):
    """Occupancy spells: the account that held each premise when the extract window opened, moves at each class's
    turnover (students in August), and the vacant days between accounts."""
    rng = _rng(5)
    pr = w.pr
    acc = []
    aid = 5520000
    vacant = np.zeros((len(pr), w.D), dtype=bool)
    for i, p in pr.iterrows():
        t = pd.Timestamp(P.SIM0) - pd.Timedelta(days=int(rng.integers(30, 2400)))
        cur_start = t.date()
        day = 0
        rate = {"RES": 0.09, "COM": 0.05}[p["cls"]]
        if p["district"] in ("DT", "CH"):
            rate *= 1.8
        events = []
        if p["kind"] == "student":
            for y in (2024, 2025, 2026):
                if rng.random() < 0.7:
                    d0 = dt.date(y, 7, 31) + dt.timedelta(days=int(rng.integers(0, 12)))
                    events.append(d0)
        else:
            dd = P.SIM0
            while True:
                gap = int(rng.exponential(365 / rate))
                dd = dd + dt.timedelta(days=gap)
                if dd > P.SIM1:
                    break
                events.append(dd)
        for ev in sorted(events):
            if ev <= P.SIM0 or ev >= P.SIM1:
                continue
            vac = int(rng.integers(0, 6)) if p["kind"] == "student" else int(min(90, rng.exponential(18)))
            acc.append(dict(AccountID=aid, PremiseID=int(p["premise"]), StartDate=cur_start, EndDate=ev, cls=p["cls"]))
            aid += 1
            start = ev + dt.timedelta(days=vac)
            if start > P.SIM1:
                start = None
            i0 = (ev - P.SIM0).days
            i1 = (start - P.SIM0).days if start else w.D
            vacant[i, i0:i1] = True
            if start is None:
                cur_start = None
                break
            cur_start = start
        if cur_start is not None:
            acc.append(dict(AccountID=aid, PremiseID=int(p["premise"]), StartDate=cur_start, EndDate=None, cls=p["cls"]))
            aid += 1
    acc = pd.DataFrame(acc)
    order = acc.assign(s=acc["StartDate"].map(lambda v: v if isinstance(v, dt.date) else dt.date(2100, 1, 1))) \
        .sort_values(["s", "PremiseID"], kind="mergesort").index
    gaps = 1 + (_rng(106).random(len(acc)) < 0.04).astype(int) * _rng(107).integers(1, 30, len(acc))
    ids = 5100000 + np.cumsum(gaps)
    acc.loc[order, "AccountID"] = ids
    acc["AccountID"] = acc["AccountID"].astype(int)
    w.accounts = acc
    w.vacant = vacant


def use(w):
    """True daily use at base conditions (Mcf) for every premise."""
    rng = _rng(6)
    pr = w.pr
    n = len(pr)
    hdd = w.hdd_eff.astype(np.float32)
    base = pr["base"].values.astype(np.float32)
    slope = pr["slope"].values.astype(np.float32)
    U = base[:, None] + slope[:, None] * hdd[None, :]
    U *= (1 + rng.normal(0, 0.05, (n, w.D))).astype(np.float32)
    com = (pr["cls"] == "COM").values
    wk = (w.days.dayofweek.values >= 5)
    hol = np.zeros(w.D, bool)
    for y in (2023, 2024, 2025, 2026):
        hol |= _win(w, "%d-12-23" % y, "%d-01-01" % (y + 1))
        hol |= _win(w, "%d-07-03" % y, "%d-07-05" % y)
    fac = np.where(hol, 0.55, np.where(wk, 0.75, 1.0)).astype(np.float32)
    U[com] *= fac[None, :]
    # students: the winter break and the summer away
    brk = np.zeros(w.D, bool)
    summer = np.zeros(w.D, bool)
    for y in (2023, 2024, 2025):
        brk |= _win(w, "%d-12-17" % y, "%d-01-11" % (y + 1))
    for y in (2024, 2025, 2026):
        summer |= _win(w, "%d-05-12" % y, "%d-08-20" % y)
    sb_all = np.zeros(w.D, bool)
    for y in (2023, 2024, 2025):
        sb_all |= _win(w, "%d-11-12" % y, "%d-04-14" % (y + 1))
    sb_new = _win(w, "2025-11-12", "2026-04-14")
    for i in np.where(pr["kind"] == "student")[0]:
        U[i, brk] = 0.010 + 0.35 * slope[i] * hdd[brk]
        U[i, summer] = 0.008
    for mask_kind, days_mask in (("snowbird", sb_all), ("snowbird_new", sb_new)):
        for i in np.where(pr["kind"] == mask_kind)[0]:
            jitter = int(rng.integers(-6, 7))
            dm = np.roll(days_mask, jitter)
            U[i, dm] = 0.005 + 0.40 * slope[i] * hdd[dm]
    # vacant between accounts: heat held low, nothing else
    V = w.vacant
    U = np.where(V, (0.005 + 0.55 * slope[:, None] * hdd[None, :]).astype(np.float32), U)
    # furnace replacements that earned a rebate: the heating slope drops (a distractor's footprint, not a collapse)
    w.rebates = []
    reb = rng.choice(np.where(~com)[0], 260, replace=False)
    for i in reb:
        d0 = int(rng.integers(30, w.D - 30))
        f = float(rng.uniform(0.82, 0.92))
        U[i, d0:] = base[i] + (U[i, d0:] - base[i]) * f
        w.rebates.append((i, w.dates[d0], f))
    w.U = np.clip(U, 0.0, None)
    w.brk, w.summer = brk, summer


def bypasses(w):
    """Meters bypassed in the window: a full bypass (a pipe round the meter) leaves the meter a trickle; a furnace
    tap leaves the water heater and range on the meter and takes the furnace off it."""
    rng = _rng(7)
    pr = w.pr
    cases = []
    for d in P.DISTRICTS:
        full, part = d["byp"]
        cand = pr.index[(pr["district"] == d["code"]) & (pr["cls"] == "RES") & ~pr["tc"] & (pr["kind"] == "occ")]
        pick = rng.choice(cand, full + part, replace=False) if full + part else []
        for j, i in enumerate(pick):
            start = dt.date(2025, 9, 1) + dt.timedelta(days=int(rng.integers(0, 140)))
            cases.append(dict(i=int(i), kind="full" if j < full else "tap", start=start))
        if d["cbyp"]:
            cc = pr.index[(pr["district"] == d["code"]) & (pr["cls"] == "COM") & ~pr["tc"]]
            big = pr.loc[cc].sort_values("slope", ascending=False).index[:d["cbyp"] + 2]
            for i in rng.choice(big, d["cbyp"], replace=False):
                start = dt.date(2025, 8, 15) + dt.timedelta(days=int(rng.integers(0, 120)))
                cases.append(dict(i=int(i), kind="full", start=start))
    w.bypass = cases
    # cases found and fixed before the window, for the revenue protection file
    hist = []
    cand = pr.index[(pr["cls"] == "RES") & (pr["kind"] == "occ")]
    for i in rng.choice(cand, 11, replace=False):
        found = dt.date(2021, 3, 1) + dt.timedelta(days=int(rng.integers(0, 1550)))
        months = int(rng.integers(5, 26))
        kind = "full" if rng.random() < 0.55 else "tap"
        hist.append(dict(i=int(i), kind=kind, found=found, months=months))
    w.bypass_hist = hist


def gas_temperature(w):
    """Gas temperature at each meter, day by day (F): outdoors the gas arrives at the temperature of the soil
    around the service, warmed a little by the house wall and pulled toward the air in the riser; indoors it sits
    near the basement's temperature."""
    pr = w.pr
    k = pr["k_air"].values[:, None]
    wall = pr["wall"].values[:, None]
    bas = pr["basement"].values[:, None]
    air = w.air[None, :]
    s20 = w.s20[None, :]
    cold = (w.air < 45)[None, :]
    out = s20 + k * (air - s20) + wall * cold
    ins = bas + 0.12 * (w.s40[None, :] - 46.0)
    w.Tgas = np.where(pr["outdoor"].values[:, None], out, ins).astype(np.float32)


def registration(w):
    """Registered ccf per premise per day, and the billed base ccf the billing system makes of it (registered x
    PF): a non-compensating meter registers gas at its temperature, a compensating one at 60 F."""
    pr = w.pr
    pmeter = P.P_ATM + P.DELIVERY_PSIG
    act = w.U * 10.0 * (P.P_BASE / pmeter)            # ccf at meter pressure, if the gas were at 60 F
    T_R = w.Tgas + 459.67
    exch = np.zeros(len(pr), dtype=int)
    for i, d in enumerate(pr["exch_date"].values):
        if d is not None and isinstance(d, dt.date):
            exch[i] = (d - P.SIM0).days
    day = np.arange(w.D)[None, :]
    noncomp = (~pr["tc"].values[:, None]) | (day < exch[:, None])
    R = np.where(noncomp, act * T_R / P.R_BASE, act).astype(np.float32)
    for c in w.bypass:
        i = c["i"]
        d0 = (c["start"] - P.SIM0).days
        if c["kind"] == "full":
            R[i, d0:] *= 0.03
        else:
            b = pr.at[i, "base"]
            R[i, d0:] *= (b / np.maximum(w.U[i, d0:], 1e-6)).clip(0, 1)
    for c in w.bypass_hist:
        i = c["i"]
        d1 = (c["found"] - P.SIM0).days
        d0 = d1 - c["months"] * 30
        if d1 <= 0:
            continue
        d0 = max(0, d0)
        R[i, d0:d1] *= 0.03 if c["kind"] == "full" else 0.35
    w.R = R
    w.noncomp = noncomp


# --------------------------------------------------------------------------------------- large customers (correctors)
EVC_IDS = sorted(int(x) for x in np.random.default_rng([22062, 104]).choice(np.arange(10000, 99999), 80, replace=False))


def evc_customers(w):
    rng = _rng(8)
    rows = []
    k = 0
    for d in P.DISTRICTS:
        for j in range(P.EVC[d["code"]]):
            big = d["code"] == "CH" and j == 0
            base = 380.0 if big else float(rng.lognormal(np.log(9.0), 0.8))
            slope = 3.1 if big else float(rng.lognormal(np.log(0.35), 0.6))
            outdoor = bool(rng.random() < 0.70) if not big else True
            press = float(rng.choice([2.0, 5.0, 10.0, 25.0], p=[0.45, 0.30, 0.15, 0.10]))
            rows.append(dict(account="E%05d" % EVC_IDS[k], district=d["code"], base=base, slope=slope,
                             outdoor=outdoor, press=press,
                             name="Brandvold State University central plant" if big else None))
            k += 1
    ev = pd.DataFrame(rows)
    n = len(ev)
    wk = (w.days.dayofweek.values >= 5)
    U = ev["base"].values[:, None] * np.where(wk, 0.8, 1.0)[None, :] + ev["slope"].values[:, None] * w.hdd_eff[None, :]
    U *= 1 + rng.normal(0, 0.04, (n, w.D))
    T = np.where(ev["outdoor"].values[:, None], w.s20[None, :] + 0.10 * (w.air[None, :] - w.s20[None, :]) + 1.0,
                 64.0 + 0.0 * w.air[None, :])
    T = T + rng.normal(0, 0.9, (n, w.D))
    w.evc = ev
    w.evcU = np.clip(U, 0.0, None)
    w.evcT = T


# --------------------------------------------------------------------------------- leaks, damage, own use, stations
def network(w):
    rng = _rng(9)
    pr = w.pr
    dist = pr["district"].values
    frost = np.isin(w.days.month, [12, 1, 2, 3]).astype(float)
    W = (w.days >= pd.Timestamp(P.W0)) & (w.days <= pd.Timestamp(P.W1))
    w.dist_use = {}
    w.leak = {}
    w.damage = []
    w.own = {}
    w.inflow = {}
    w.evc_dist = {}
    # damage events
    for d in P.DISTRICTS:
        rate = 3.0 * (2.0 if d["code"] in ("PR", "HP", "AP") else 1.0)
        nev = rng.poisson(rate * w.D / 365.25)
        for _ in range(nev):
            i = int(rng.integers(0, w.D))
            true = float(rng.lognormal(np.log(22), 0.8))
            w.damage.append(dict(district=d["code"], day=i, true=true, reported=round(true * rng.uniform(0.85, 1.15), 0)))
    stations = []
    for d in P.DISTRICTS:
        m = dist == d["code"]
        cust = w.U[m].sum(0).astype(float)
        ev = w.evcU[(w.evc["district"] == d["code"]).values].sum(0)
        heater = np.where(np.isin(w.days.month, [10, 11, 12, 1, 2, 3, 4]), 0.15 + 0.012 * w.hdd60, 0.0)
        heater = heater * len(d["drs"])
        dmg = np.zeros(w.D)
        for e in w.damage:
            if e["district"] == d["code"]:
                dmg[e["day"]] += e["true"]
        other = cust + ev + dmg + heater
        shape = 1 + 0.25 * frost * d["ci"]
        # the target is FY2026's share of gas in; earlier years a little lower as the mains age
        growth = (1.06 ** (-((pd.Timestamp(P.W1) - w.days).days.values / 365.25))).clip(0.8, 1.0)
        L = shape * growth
        scale = d["leak"] / 100.0 * other[W].sum() / (1 - d["leak"] / 100.0) / L[W].sum()
        L = L * scale * (1 + rng.normal(0, 0.03, w.D))
        w.leak[d["code"]] = L
        w.own[d["code"]] = heater
        w.evc_dist[d["code"]] = ev
        w.dist_use[d["code"]] = cust
        w.inflow[d["code"]] = other + L
        for s in d["drs"]:
            stations.append(s)
    w.stations = stations


def regulator_stations(w):
    """Each regulator station's corrector: corrected Mcf for the gas day, with the faults the field crews logged."""
    rng = _rng(10)
    rows = []
    split = {"OT": [0.56, 0.44], "DT": [0.61, 0.39]}
    true_station = {}
    for d in P.DISTRICTS:
        sh = split.get(d["code"], [1.0])
        for s, f in zip(d["drs"], sh):
            if len(sh) == 1:
                share = np.ones(w.D)
            elif s.endswith("-1"):
                share = f * (1 + rng.normal(0, 0.012, w.D))
            else:
                share = 1 - (true_station[d["drs"][0]] / w.inflow[d["code"]])
            true_station[s] = w.inflow[d["code"]] * share
    w.true_station = true_station
    press_nom = {s: (35.0 if s[:2] in ("OT", "DT", "RS", "NE", "EG", "SQ", "HV", "LV") else 25.0) for s in w.stations}
    for s in w.stations:
        v = true_station[s].copy()
        pr_ = press_nom[s] + rng.normal(0, 0.6, w.D)
        T = w.s40 * 0.6 + w.s20 * 0.4 + rng.normal(0, 0.4, w.D)
        unc = v * (P.P_BASE / (pr_ + P.P_ATM)) * ((T + 459.67) / P.R_BASE)
        rec = v.copy()
        alarm = np.array([""] * w.D, dtype=object)
        miss = rng.random(w.D) < 0.004
        if s == "RS-1":
            miss |= _win(w, "2026-01-12", "2026-01-25")
        if s == "LV-1":
            m = _win(w, "2025-12-04", "2025-12-21")
            rec[m] = unc[m] * ((25.0 + P.P_ATM) / P.P_BASE) * (P.R_BASE / (T[m] + 459.67))
            alarm[m] = "PXDCR FAIL FIXED P"
            pr_ = np.where(m, 25.0, pr_)
        if s == "WG-1":
            m = _win(w, "2026-02-03", "2026-02-11")
            rec[m] = unc[m] * ((pr_[m] + P.P_ATM) / P.P_BASE) * (P.R_BASE / (55.0 + 459.67))
            alarm[m] = "TXMTR STUCK"
            T = np.where(m, 55.0, T)
        if s == "CH-1":
            m = _win(w, "2024-07-08", "2024-07-10")
            alarm[m] = "BATT LOW"
        for i in range(w.D):
            if w.dates[i] < dt.date(2023, 9, 1):
                continue
            if miss[i]:
                rows.append(dict(GasDay=w.dates[i], Station=s, CorrectedMcf=None, UncorrectedMcf=None,
                                 AvgPressurePsig=None, AvgTempF=None, Alarm="COMM FAIL"))
                continue
            rows.append(dict(GasDay=w.dates[i], Station=s, CorrectedMcf=round(float(rec[i]), 1),
                             UncorrectedMcf=round(float(unc[i]), 1), AvgPressurePsig=round(float(pr_[i]), 1),
                             AvgTempF=round(float(T[i]), 1), Alarm=alarm[i]))
    w.drs = pd.DataFrame(rows)
    # the city gate: every station's gas, the high-pressure system's own losses and the gate's line heater
    tot = sum(true_station.values())
    hp = tot * 0.0006 * (1 + rng.normal(0, 0.15, w.D))
    heater = 0.0011 * tot * np.where(w.air < 50, 1.0, 0.2)
    gate = tot + hp + heater
    btu = 1038 + rng.normal(0, 4, w.D)
    g = pd.DataFrame(dict(GasDay=w.dates, CorrectedMcf=np.round(gate, 1), HeatingValueBtuScf=np.round(btu, 1),
                          Dth=np.round(gate * btu / 1000.0, 1),
                          AvgPressurePsig=np.round(612 + rng.normal(0, 9, w.D), 0),
                          AvgTempF=np.round(w.s40 * 0.7 + 14 + rng.normal(0, 0.5, w.D), 1)))
    w.gate = g[g["GasDay"] >= dt.date(2023, 9, 1)].reset_index(drop=True)
    w.hp_loss = hp
    w.gate_heater = heater


def evc_records(w):
    rng = _rng(11)
    rows = []
    ev = w.evc
    for j, e in ev.iterrows():
        pmeter = e["press"] + P.P_ATM
        T = w.evcT[j]
        U = w.evcU[j]
        unc = U * (P.P_BASE / pmeter) * ((T + 459.67) / P.R_BASE)
        fixed = np.zeros(w.D, bool)
        if rng.random() < 0.12:
            a = int(rng.integers(100, w.D - 30))
            fixed[a:a + int(rng.integers(3, 15))] = True
        for i in range(w.D):
            if w.dates[i] < dt.date(2023, 9, 1):
                continue
            if fixed[i]:
                corr = unc[i] * (pmeter / P.P_BASE) * (P.R_BASE / (60.0 + 459.67))
                rows.append(dict(GasDay=w.dates[i], Account=e["account"], CorrectedMcf=round(float(corr), 2),
                                 UncorrectedMcf=round(float(unc[i]), 2), AvgPressurePsig=round(e["press"], 1),
                                 AvgGasTempF=60.0, Status="FIXED FACTOR"))
            else:
                rows.append(dict(GasDay=w.dates[i], Account=e["account"], CorrectedMcf=round(float(U[i]), 2),
                                 UncorrectedMcf=round(float(unc[i]), 2),
                                 AvgPressurePsig=round(e["press"] + float(rng.normal(0, 0.05)), 2),
                                 AvgGasTempF=round(float(T[i]), 1), Status="OK"))
    w.evc_rec = pd.DataFrame(rows)


# --------------------------------------------------------------------------------------------- the logger study
def loggers(w):
    rng = _rng(12)
    pr = w.pr
    rows = []
    m = (w.days >= pd.Timestamp(P.STUDY0)) & (w.days <= pd.Timestamp(P.STUDY1))
    lid = 1
    picked = []
    for code, n in list(P.STUDY_OUT.items()) + list(P.STUDY_IN.items()):
        indoor = code in P.STUDY_IN
        cand = pr.index[(pr["district"] == code) & (pr["cls"] == "RES") & ~pr["tc"] & (pr["kind"] == "occ")
                        & (pr["outdoor"] == (not indoor))]
        cand = [i for i in cand if all(c["i"] != i for c in w.bypass)]
        for i in rng.choice(cand, n, replace=False):
            picked.append((lid, int(i)))
            lid += 1
    for lid, i in picked:
        for t in np.where(m)[0]:
            if rng.random() < 0.02:
                continue
            flow_h = float(np.clip(4 + 0.42 * w.hdd60[t] + rng.normal(0, 1.5), 0.5, 24))
            rows.append(dict(LoggerID="TL-%03d" % lid, PremiseID=int(pr.at[i, "premise"]), Date=w.dates[t],
                             GasTempF=round(float(w.Tgas[i, t] + rng.normal(0, 0.6)), 1),
                             FlowHours=round(flow_h, 1), RegisteredCcf=round(float(w.R[i, t]), 2)))
    w.loggers = pd.DataFrame(rows)
    w.logger_premises = [i for _, i in picked]


def build():
    w = World()
    calendar(w)
    weather(w)
    premises(w)
    programs(w)
    plan_2027(w)
    accounts(w)
    use(w)
    bypasses(w)
    gas_temperature(w)
    registration(w)
    evc_customers(w)
    network(w)
    regulator_stations(w)
    evc_records(w)
    loggers(w)
    return w


if __name__ == "__main__":
    import time
    t0 = time.time()
    w = build()
    print("built in %.1fs: %d premises, %d accounts, %d drs rows, %d evc rows, %d logger rows, %d work orders"
          % (time.time() - t0, len(w.pr), len(w.accounts), len(w.drs), len(w.evc_rec), len(w.loggers),
             len(w.workorders)))
