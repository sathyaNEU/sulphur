"""task9: the fleet simulator. Day by day per vault, every drive's hazard is its family's wear-out curve times an infant
term, its vault's and batch's frailty, the hot batch's ramp and its chassis's shocks; the failure day is where the
cumulative hazard crosses an exponential draw. A failing drive may show SMART growth first and be pulled under the
policy in force; a healthy drive may develop a non-zero 187 count, which P2 pulls. Every failed or pulled drive's
slot is refilled by a spare. Operations' reviews then retire the vault with the worst trailing twelve months in each
family under review. Nothing here knows what the analysis will ask.
"""
import datetime as dt
import math

import numpy as np

import params as P

DAY0 = P.SIM_START
N_DAYS = (P.END - P.SIM_START).days + 1


def day(d):
    return (d - DAY0).days


def to_date(i):
    return DAY0 + dt.timedelta(days=int(i))


def iso_week_start(year, week):
    return dt.date.fromisocalendar(year, week, 1)


def firmware_for(family, manuf_date):
    fw = P.FIRMWARE[family][0][1]
    for (y, w), name in P.FIRMWARE[family]:
        if manuf_date >= iso_week_start(y, w):
            fw = name
    return fw


class World:
    def __init__(self, seed=P.SEED):
        self.rng = np.random.default_rng(seed)
        self.vaults = []          # dicts: vid, family, dc, commission (day), z, decom (start, done) or None
        self.drives = []          # one dict per drive ever installed in a fleet slot
        self.shocks = []          # dicts: dc, vid, chassis, start (day), logged, kind
        self.batch_z = {}
        self._plan()
        self._shocks()
        for v in self.vaults:
            self._simulate_vault(v)
        self._reviews()

    # ---- the fleet's vaults, in commissioning order
    def _plan(self):
        rng = self.rng
        n = {"DC-1": 0, "DC-2": 0, "DC-3": 0}
        for fam, dc, first, last, count in P.VAULT_PLAN:
            span = (last - first).days
            when = sorted(first + dt.timedelta(days=int(x)) for x in np.linspace(0, span, count) + rng.integers(-6, 7, count))
            for d in when:
                d = min(max(d, first), last)
                n[dc] += 1
                prefix = {"DC-1": "A", "DC-2": "B", "DC-3": "C"}[dc]
                vid = "%s%02d" % (prefix, n[dc])
                self.vaults.append(dict(vid=vid, family=fam, dc=dc, commission=day(d),
                                        z=float(rng.gamma(*P.VAULT_FRAILTY)), decom=None))

    def _batch(self, family, manuf_day):
        md = to_date(manuf_day)
        iso = md.isocalendar()
        k = (family, iso[0], (iso[1] - 1) // P.BATCH_WEEKS)
        if k not in self.batch_z:
            self.batch_z[k] = float(self.rng.gamma(*P.BATCH_FRAILTY))
        return k

    # ---- chassis power and cooling events
    def _shocks(self):
        rng = self.rng
        years = N_DAYS / 365.25
        for dc in ("DC-1", "DC-2", "DC-3"):
            k = rng.poisson(P.SHOCKS_PER_DC_YEAR * years)
            for t in np.sort(rng.integers(0, N_DAYS, k)):
                live = [v for v in self.vaults if v["dc"] == dc and v["commission"] <= t]
                if not live:
                    continue
                v = live[rng.integers(0, len(live))]
                kind = "COOLING_EXCURSION" if rng.random() < P.COOLING_SHARE else "CHASSIS_POWER_EVENT"
                self.shocks.append(dict(dc=dc, vid=v["vid"], chassis=int(rng.integers(0, P.CHASSIS)), start=int(t),
                                        logged=bool(rng.random() < P.SHOCK_LOGGED), kind=kind))

    def _shock_grid(self, vid):
        g = np.ones((P.CHASSIS, N_DAYS))
        for s in self.shocks:
            if s["vid"] != vid:
                continue
            if s["kind"] == "COOLING_EXCURSION":
                g[:, s["start"]:s["start"] + P.COOLING_DAYS] *= P.COOLING_MULT
            else:
                g[s["chassis"], s["start"]:s["start"] + P.SHOCK_DAYS] *= P.SHOCK_MULT
        return g

    # ---- hazard per day for a set of drives on the whole grid (zero before install)
    def _cumhaz(self, fam, install, manuf, chassis, z, hot, grid):
        f = P.FAMILY[fam]
        t = np.arange(N_DAYS)[None, :]
        age_d = t - install[:, None]
        on = age_d >= 0
        age_y = np.where(on, age_d, 0) / 365.25
        beta, eta = f["beta"], f["eta"]
        h = (beta / eta) * np.power(np.maximum(age_y, 1e-6) / eta, beta - 1.0)
        h *= 1.0 + P.INFANT[0] * np.exp(-(age_y * 12.0) / P.INFANT[1])
        h *= z[:, None]
        if hot.any():
            man_m = (t - manuf[:, None]) / 30.4375
            ramp = np.where(man_m > P.HOT["onset_months"],
                            np.minimum(np.power(2.0, (man_m - P.HOT["onset_months"]) / P.HOT["doubling_months"]), P.HOT["cap"]), 1.0)
            h = np.where(hot[:, None], h * ramp, h)
        h *= grid[chassis]
        h = np.where(on, h, 0.0) / 365.25
        return np.cumsum(h, axis=1)

    def _hot(self, fam, manuf_day):
        if fam != P.HOT["family"]:
            return False
        md = to_date(manuf_day)
        return iso_week_start(*P.HOT["first"]) <= md < iso_week_start(*P.HOT["last"]) + dt.timedelta(days=7)

    # ---- one vault, every generation of drives in its slots
    def _simulate_vault(self, v):
        rng = self.rng
        fam = v["family"]
        grid = self._shock_grid(v["vid"])
        slots = np.arange(P.VAULT_DRIVES)
        install = v["commission"] + rng.integers(0, 4, slots.size)
        lag = np.exp(np.log(P.DEPLOY_LAG[0]) + P.DEPLOY_LAG[1] * rng.standard_normal(slots.size))
        manuf = install - np.round(lag).astype(int)
        spare = np.zeros(slots.size, bool)
        gen = 1
        while slots.size:
            batches = [self._batch(fam, int(m)) for m in manuf]
            z = v["z"] * np.array([self.batch_z[b] for b in batches])
            hot = np.array([self._hot(fam, int(m)) for m in manuf])
            chassis = slots // P.SLOTS_PER_CHASSIS
            H = self._cumhaz(fam, install, manuf, chassis, z, hot, grid)
            E = rng.exponential(1.0, slots.size)
            crossed = H >= E[:, None]
            any_f = crossed[:, -1]
            fail = np.where(any_f, np.argmax(crossed, axis=1), N_DAYS + 10)
            del H, crossed
            n = slots.size
            # SMART precursors and the pull policy in force
            pre = rng.random(n) < P.PRECURSOR_P
            win = rng.integers(P.PRECURSOR_DAYS[0], P.PRECURSOR_DAYS[1] + 1, n)
            u = rng.random(n)
            exit_d = fail.copy()
            kind = np.where(any_f, "FAIL", "ACTIVE").astype(object)
            p2 = day(P.P2_START)
            for i in np.where(any_f & pre)[0]:
                p1_at = fail[i] - int(round(P.P1_LEAD * win[i]))
                p2_at = fail[i] - int(round(P.P2_LEAD * win[i]))
                at = None
                if p2_at >= p2 and u[i] < P.P2_DETECT:
                    at = p2_at
                elif p1_at < p2 and u[i] < P.P1_DETECT:
                    at = p1_at
                if at is not None:
                    at = max(at, install[i] + 1)
                    exit_d[i], kind[i] = at, "PULL"
            # a healthy drive's non-zero 187, pulled under P2 (the prevalent stock over the harvest)
            s187 = install + np.round(rng.exponential(365.25 / P.SPURIOUS_187, n)).astype(int)
            sp = np.where(s187 < p2, p2 + rng.integers(0, P.HARVEST_DAYS, n), s187 + rng.integers(3, 21, n))
            take = (sp < exit_d) & (sp < N_DAYS)
            exit_d = np.where(take, sp, exit_d)
            kind = np.where(take, "SPUR", kind)
            for i in range(n):
                self.drives.append(dict(vid=v["vid"], family=fam, dc=v["dc"], slot=int(slots[i]), gen=gen,
                                        install=int(install[i]), manuf=int(manuf[i]), batch=batches[i], hot=bool(hot[i]),
                                        spare=bool(spare[i]), fail=int(fail[i]) if any_f[i] else None,
                                        precursor=int(win[i]) if (any_f[i] and pre[i]) else None,
                                        s187=int(s187[i]) if s187[i] < N_DAYS else None,
                                        exit=int(exit_d[i]) if exit_d[i] < N_DAYS else None,
                                        kind=kind[i] if exit_d[i] < N_DAYS else "ACTIVE"))
            # refill the slots that emptied before the record's end
            refill = (exit_d < N_DAYS - 1) & (kind != "ACTIVE")
            slots = slots[refill]
            install = exit_d[refill] + rng.integers(P.REPLACE_DAYS[0], P.REPLACE_DAYS[1] + 1, refill.sum())
            keep = install < N_DAYS
            slots, install = slots[keep], install[keep]
            lag = np.exp(np.log(P.SPARE_LAG[0]) + P.SPARE_LAG[1] * rng.standard_normal(slots.size))
            manuf = install - np.round(lag).astype(int)
            spare = np.ones(slots.size, bool)
            gen += 1

    # ---- operations' reviews: the worst vault of each family under review is retired
    def _reviews(self):
        rng = self.rng
        by_vault = {}
        for d in self.drives:
            by_vault.setdefault(d["vid"], []).append(d)
        for fam, dates in P.DECOM_FAMILIES.items():
            for R in dates:
                r = day(R)
                cands = [v for v in self.vaults if v["family"] == fam and v["decom"] is None and v["commission"] < r - 365]
                rates = []
                for v in cands:
                    ev, ex = 0, 0.0
                    for d in by_vault[v["vid"]]:
                        a, b = max(d["install"], r - 365), min(d["exit"] if d["exit"] is not None else N_DAYS, r)
                        if b > a:
                            ex += (b - a) / 365.25
                        if d["exit"] is not None and r - 365 <= d["exit"] < r and d["kind"] in ("FAIL", "PULL", "SPUR"):
                            ev += 1
                    rates.append(ev / max(ex, 1e-9))
                if not cands:
                    continue
                v = cands[int(np.argmax(rates))]
                start = r + int(rng.integers(10, 20))
                done = start + int(rng.integers(P.DECOM_DAYS[0], P.DECOM_DAYS[1] + 1))
                v["decom"] = (start, done)
                kept = []
                for d in by_vault[v["vid"]]:
                    if d["install"] >= start:
                        d["dropped"] = True
                        continue
                    if d["exit"] is None or d["exit"] >= start:
                        d["exit"] = int(rng.integers(start, done + 1))
                        d["kind"] = "DECOM"
                    kept.append(d)
                by_vault[v["vid"]] = kept
        self.drives = [d for d in self.drives if not d.get("dropped")]


def summary(W):
    """A quick look at the simulated truth (for calibration only)."""
    import collections
    out = collections.defaultdict(lambda: [0, 0.0])
    q_end = day(P.END)
    for d in W.drives:
        a, b = max(d["install"], q_end - 365), min(d["exit"] if d["exit"] is not None else N_DAYS, q_end + 1)
        key = (d["family"], d["hot"])
        if b > a:
            out[key][1] += (b - a) / 365.25
        if d["exit"] is not None and q_end - 365 <= d["exit"] <= q_end and d["kind"] in ("FAIL", "PULL", "SPUR"):
            out[key][0] += 1
    return {k: (v[0], round(v[1]), round(100 * v[0] / max(v[1], 1e-9), 2)) for k, v in sorted(out.items())}
