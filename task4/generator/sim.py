"""The simulated brewery, day by day: the weather, each outlet line's sales, the outlets' cellars and their orders,
the drivers' visits (fulls delivered, empties collected, other brewers' kegs picked up with them), kegs lost in the
trade, taken by other brewers' drivers and handed back through the exchange, found by the recovery agent, the depots'
gates and trunks, the washer, repairs and condemnations, the brew-house's fills (mainstream to a stock target, the
Foundry beers in whole 120-keg lots), the register and its 2023 reconciliation, and every RFID read of a tagged keg.

The history runs to 30 November 2026. The same engine then carries the 30 November state through the 2027 summer at
normal weather with the plans (Maplestead's pubs, the 18-beer Foundry range), with new kegs drawn whenever the
washer runs out, which is the truth the checks hold the golden to: the kegs in use in the busiest week and the
original fleet still usable then."""
import datetime as dt
import math
from collections import defaultdict, deque

import numpy as np

import params as P

ONE = dt.timedelta(days=1)


def daterange(a, b):
    d = a
    while d <= b:
        yield d
        d += ONE


class Weather:
    """Daily maximum temperature at Leeds (and two stations near the other depots), 2016 to November 2026."""

    def __init__(self, rng):
        self.days = list(daterange(dt.date(2016, 1, 1), P.ASOF))
        n = len(self.days)
        doy = np.array([d.timetuple().tm_yday for d in self.days])
        base = 13.6 + 7.4 * np.cos(2 * np.pi * (doy - 204) / 365.25)
        shift = {2016: 0.1, 2017: 0.2, 2018: 1.1, 2019: 0.3, 2020: 0.4, 2021: 0.0, 2022: 1.0, 2023: 0.5, 2024: -0.6,
                 2025: 1.2, 2026: 0.3}
        summer = np.array([shift[d.year] if 5 <= d.month <= 9 else 0.3 * shift[d.year] for d in self.days])
        a = np.zeros(n)
        e = rng.normal(0, 1.0, n)
        for i in range(1, n):
            a[i] = 0.72 * a[i - 1] + 2.4 * e[i]
        self.leeds = np.round(base + summer + a, 1)
        self.idx = {d: i for i, d in enumerate(self.days)}
        offs = {"LDS": 0.0, "YRK": -0.4, "SHF": 0.3}
        self.station = {k: np.round(self.leeds + v + rng.normal(0, 0.6, n), 1) for k, v in offs.items()}
        self._normal = {}
        self.like = None          # replay a past year's weather (the range)

    def normal(self, d):
        """the 2016 to 2025 average for the same calendar day (the standard's normal weather)"""
        key = (d.month, d.day)
        if key not in self._normal:
            vals = []
            for y in range(2016, 2026):
                day = min(d.day, 28) if d.month == 2 else d.day
                vals.append(self.leeds[self.idx[dt.date(y, d.month, day)]])
            self._normal[key] = float(np.mean(vals))
        return self._normal[key]

    def temp(self, d):
        if d in self.idx:
            return float(self.leeds[self.idx[d]])
        if self.like is not None:
            day = min(d.day, 28) if d.month == 2 else d.day
            return float(self.leeds[self.idx[dt.date(self.like, d.month, day)]])
        return self.normal(d)


def season(d):
    """the trade's calendar beside the weather: a summer lift, a quiet January, the Christmas weeks"""
    doy = d.timetuple().tm_yday
    s = 1.0 + 0.10 * math.cos(2 * math.pi * (doy - 200) / 365.25)
    if d.month == 1:
        s *= 0.84
    if d.month == 12 and d.day >= 10:
        s *= 1.0 + 0.18 * min(1.0, (d.day - 9) / 10)
    return s


def bank(d):
    if d in P.BANK_HOLIDAYS:
        return 1.35
    if d + ONE in P.BANK_HOLIDAYS:
        return 1.15
    return 1.0


class Keg:
    __slots__ = ("id", "size", "lot", "tag", "status", "sku", "where", "status_date", "out_at")

    def __init__(self, kid, size, lot, tag):
        self.id = kid
        self.size = size
        self.lot = lot
        self.tag = tag
        self.status = "ACTIVE"
        self.sku = None
        self.where = None
        self.status_date = None
        self.out_at = None


class Line:
    __slots__ = ("outlet", "sku", "size", "rate", "taps", "temp_k", "xmas", "ontap", "fulls", "empties", "foundry",
                 "since")

    def __init__(self, outlet, sku, size, rate, temp_k, xmas, foundry=False, since=None):
        self.outlet = outlet
        self.sku = sku
        self.size = size
        self.rate = rate
        self.taps = 2 if rate > P.TWO_TAPS_ABOVE else 1
        self.temp_k = temp_k
        self.xmas = xmas
        self.ontap = []
        self.fulls = deque()
        self.empties = []
        self.foundry = foundry
        self.since = since


class Outlet:
    __slots__ = ("id", "channel", "depot", "seasonal", "opened", "closed", "lines", "interval", "days", "group",
                 "estate", "renumbered")

    def __init__(self, oid, channel, depot, seasonal, opened, closed):
        self.id = oid
        self.channel = channel
        self.depot = depot
        self.seasonal = seasonal
        self.opened = opened
        self.closed = closed
        self.lines = []
        self.interval = 7
        self.days = ()
        self.group = None
        self.estate = False
        self.renumbered = None


def seasonal_open(d):
    return 4 <= d.month <= 10


def set_route(o, rng):
    tot = sum(ln.rate for ln in o.lines)
    o.interval = 3 if tot > P.TWICE_WEEKLY_ABOVE else 7
    first = int(rng.integers(0, 5 if o.interval == 7 else 2))
    o.days = (first,) if o.interval == 7 else (first, first + 3)


def build_world(rng):
    w = type("World", (), {})()
    w.rng = rng
    w.weather = Weather(rng)
    w.sku_info = {s[0]: s for s in P.SKUS}
    chans = list(P.CHANNELS)
    cp = np.array([P.CHANNELS[c]["share"] for c in chans])
    cp = cp / cp.sum()
    depots = list(P.DEPOT_SHARE)
    dprob = np.array([P.DEPOT_SHARE[k] for k in depots])
    horizon = (P.Y27_END - P.D0).days / 365.25
    n_new = int(round(P.N_OUTLETS * P.OPEN_RATE * horizon))
    outlets = []
    groups = ["Pennine Taverns", "Ridings Pub Co", "Aire Valley Inns", "Moorside Leisure"]
    for i in range(P.N_OUTLETS + n_new):
        ch = chans[rng.choice(len(chans), p=cp)]
        dep = depots[rng.choice(len(depots), p=dprob)]
        seasonal = (ch == "CLUB" and rng.random() < 0.38) or (ch in ("FREE", "REST") and rng.random() < 0.025)
        if i < P.N_OUTLETS:
            opened = P.D0 - dt.timedelta(days=int(rng.integers(200, 8000)))
        else:
            opened = P.D0 + dt.timedelta(days=int(rng.integers(30, (P.Y27_END - P.D0).days)))
        t = rng.exponential(1.0 / P.CLOSE_RATE) * 365.25
        cd = max(opened, P.D0) + dt.timedelta(days=int(t))
        o = Outlet("W%05d" % (10031 + i * 13), ch, dep, seasonal, opened, cd if cd <= P.Y27_END else None)
        if ch == "GROUP":
            o.group = groups[int(rng.integers(0, 4))]
        for code, (share, med, sd) in P.LINES.items():
            boost = 1.25 if ch == "GROUP" and code in ("PIL", "HER") else 1.0
            if rng.random() < share * boost:
                r = float(med * math.exp(rng.normal(0, sd))) * (1.3 if seasonal else 1.0)
                if code == "FND":
                    o.lines.append(Line(o, "FND", 20, r, P.FOUNDRY_TEMP, 1.10, foundry=True))
                else:
                    s = w.sku_info[code]
                    o.lines.append(Line(o, code, s[2], r, s[4], s[5]))
        if not o.lines:
            s = w.sku_info["PIL"]
            o.lines.append(Line(o, "PIL", 50, float(P.LINES["PIL"][1] * math.exp(rng.normal(0, 0.5))), s[4], s[5]))
        set_route(o, rng)
        if rng.random() < 0.05 and o.closed is None:
            o.renumbered = o.opened + dt.timedelta(days=int(rng.integers(400, 4000)))
        outlets.append(o)
    w.outlets = outlets
    kegs = []
    w.lots = {}
    for lot, size, bought, n, tagged in P.LOTS:
        gone = P.LOT_GONE.get(lot, 0.0)
        w.lots[lot] = {"size": size, "bought": bought, "n": n, "tagged": tagged, "gone": gone}
        for _ in range(n):
            k = Keg(len(kegs), size, lot, tagged)
            if bought < P.D0 and rng.random() < gone:
                k.status = "WRITTEN_OFF"
                k.status_date = dt.date(2019 if bought.year < 2019 else 2022, 11, 30)
            kegs.append(k)
    w.kegs = kegs
    return w


class Engine:
    """the brewery and its trade, stepped one day at a time; the state lives here between the history and 2027"""

    def __init__(self, w):
        self.w = w
        self.rng = w.rng
        self.ev = defaultdict(list)
        self.clean = {s: deque() for s in P.SIZES}
        self.unbought = []
        for k in w.kegs:
            if k.status != "ACTIVE":
                continue
            if w.lots[k.lot]["bought"] > P.D0:
                self.unbought.append(k)
            else:
                k.where = "BREWERY"
                self.clean[k.size].append(k)
        self.unbought.sort(key=lambda k: (w.lots[k.lot]["bought"], k.id))
        self.depot_full = {dp: defaultdict(deque) for dp in P.DEPOTS}
        self.depot_empty = {dp: [] for dp in P.DEPOTS}
        self.trunk = defaultdict(list)
        self.exch_pipe = defaultdict(list)
        self.recov_pipe = defaultdict(list)
        self.repair = defaultdict(list)
        self.fg = defaultdict(deque)
        self.tanks = []
        self.foreign_pile = {s: 0 for s in P.SIZES}
        self.foundry_skus = list(P.FOUNDRY_2026[:5])
        self.foundry_add = {dt.date(2025, 3, 3): "F06", dt.date(2025, 6, 2): "F07", dt.date(2025, 9, 1): "F08"}
        self.ema = defaultdict(float)
        self.today = defaultdict(float)
        for o in w.outlets:
            if o.opened <= P.D0 and not (o.closed and o.closed < P.D0):
                for ln in o.lines:
                    if ln.foundry:
                        for s in self.foundry_skus:
                            self.ema[(s, o.depot)] += ln.rate / 7.0 / len(self.foundry_skus)
                    else:
                        self.ema[(ln.sku, o.depot)] += ln.rate / 7.0
        self.unconstrained = False
        self.new_kegs = 0
        self.plan = None          # the 2027 Foundry plan: {sku: (start, end, brew dates)}
        self.record_from = P.H0
        self.record_to = P.ASOF
        self.audits = {}          # date -> outlet ids the sales reps count kegs at
        self.sites = {}           # stocktake dates -> counts by site

    # ---------------------------------------------------------------------------------------------- the day
    def step(self, d):
        w, rng, ev = self.w, self.rng, self.ev
        rec = self.record_from <= d <= self.record_to
        temp = w.weather.temp(d)
        while self.unbought and w.lots[self.unbought[0].lot]["bought"] <= d:
            k = self.unbought.pop(0)
            k.where = "BREWERY"
            self.clean[k.size].append(k)
        if d in self.foundry_add and self.foundry_add[d] not in self.foundry_skus:
            self.foundry_skus.append(self.foundry_add[d])
        self.brewery(d, rec)
        self.sales(d, temp, rec)
        for o in w.outlets:
            if o.opened > d or (o.closed and o.closed < d) or d.weekday() not in o.days:
                continue
            if o.seasonal and not seasonal_open(d):
                continue
            self.visit(o, d, rec)
        for o in w.outlets:
            if o.closed == d:
                self.close_outlet(o, d, rec)
        for oid in self.audits.get(d, ()):
            o = self.byid[oid]
            if o.opened > d or (o.closed and o.closed <= d):
                continue
            c = {}
            for s in P.SIZES:
                c[s] = [0, 0, 0]
            for ln in o.lines:
                c[ln.size][0] += len(ln.fulls)
                c[ln.size][1] += len(ln.ontap)
                c[ln.size][2] += len(ln.empties)
            ev["audit"].append((d, oid, c))
        for dp in P.DEPOTS:
            if d.weekday() in P.TRUNK_WEEKDAYS[dp] and self.depot_empty[dp]:
                arr = d + dt.timedelta(days=max(1, P.TRUNK_DAYS[dp]))
                for x in self.depot_empty[dp]:
                    if not isinstance(x, tuple):
                        x.where = "TRUNK"
                self.trunk[arr].extend(self.depot_empty[dp])
                if rec:
                    own = sum(1 for x in self.depot_empty[dp] if not isinstance(x, tuple))
                    ev["trunk_back"].append((d, dp, own))
                self.depot_empty[dp] = []
        for key in set(self.ema) | set(self.today):
            self.ema[key] = 0.93 * self.ema[key] + 0.07 * self.today.get(key, 0.0)
        self.today = defaultdict(float)
        if d == P.RECON:
            for k in w.kegs:
                if k.status == "ACTIVE" and k.where in ("LOST", "RECOVERY"):
                    k.status = "WRITTEN_OFF"
                    k.status_date = d
            for day in list(self.recov_pipe):
                self.recov_pipe[day] = [k for k in self.recov_pipe[day] if k.status == "ACTIVE"]
        if d >= P.H0 and (d.weekday() == 6 or d in (P.ASOF, dt.date(2025, 11, 30), dt.date(2024, 11, 30))):
            ev["stock"].append((d, self.snapshot()))
        if d in (dt.date(2024, 11, 30), dt.date(2025, 11, 30), P.ASOF):
            self.sites[d] = self.site_counts()
            ev["between_ids"].append((d, [(k.id, k.where) for k in w.kegs if k.status == "ACTIVE" and k.where not in
                                          (None, "LOST", "RECOVERY", "SCRAP", "BREWERY", "REPAIR")]))

    # ---------------------------------------------------------------------------------------------- brewery
    def brewery(self, d, rec):
        w, rng, ev = self.w, self.rng, self.ev
        back = []
        foreign = {s: 0 for s in P.SIZES}
        for x in self.trunk.pop(d, []):
            if isinstance(x, tuple):
                foreign[x[0]] += x[1]
            else:
                back.append(("depot", x))
        back += [("exchange", k) for k in self.exch_pipe.pop(d, [])]
        back += [("recovery", k) for k in self.recov_pipe.pop(d, [])]
        back += [("repair", k) for k in self.repair.pop(d, [])]
        washed = {s: 0 for s in P.SIZES}
        damaged = {s: 0 for s in P.SIZES}
        condemned = {s: 0 for s in P.SIZES}
        by_route = defaultdict(int)
        for route, k in back:
            by_route[(route, k.size)] += 1
            if rec:
                if route in ("exchange", "recovery"):
                    ev["back_" + route].append((d, k.id, k.size))
                if k.tag and rng.random() < P.READ["RETURN"]:
                    ev["read"].append((d, k.id, "RETURN", "BRG-WASH"))
            if route != "repair" and rng.random() < P.DAMAGE:
                damaged[k.size] += 1
                if rng.random() < P.CONDEMN:
                    k.status = "CONDEMNED"
                    k.status_date = d
                    k.where = "SCRAP"
                    condemned[k.size] += 1
                    if rec:
                        ev["condemn"].append((d, k.id))
                    continue
                k.where = "REPAIR"
                r = d + dt.timedelta(days=int(rng.integers(*P.REPAIR_DAYS)))
                self.repair[r].append(k)
                if rec:
                    ev["repair"].append((d, k.id, r))
                continue
            k.where = "BREWERY"
            k.sku = None
            self.clean[k.size].append(k)
            washed[k.size] += 1
        if rec:
            for s in P.SIZES:
                ev["washer"].append((d, s, washed[s], foreign[s], damaged[s], condemned[s], by_route[("depot", s)],
                                     by_route[("exchange", s)], by_route[("recovery", s)], by_route[("repair", s)]))
        for s in P.SIZES:
            self.foreign_pile[s] += foreign[s]
        if d.day <= 3 and d.weekday() < 5 and any(self.foreign_pile.values()):
            if rec:
                ev["exchange_out"].append((d, dict(self.foreign_pile)))
            self.foreign_pile = {s: 0 for s in P.SIZES}
        fills = []
        for code, name, size, style, tk, xm in P.SKUS:
            need = sum(self.ema[(code, dp)] for dp in P.DEPOTS)
            gap = int(math.ceil(need * 3.2)) + 20 - len(self.fg[code])
            for _ in range(max(0, gap)):
                k = self.take_clean(size, d)
                if k is None:
                    break
                k.sku, k.where = code, "FG"
                self.fg[code].append(k)
                fills.append(k)
        intank = defaultdict(int)
        for fd, s, n in self.tanks:
            intank[s] += n
        for s in self.active_foundry(d):
            if self.plan is not None:
                kegs = self.plan[s][2].get(d, 0)
                if kegs:
                    self.tanks.append((d + dt.timedelta(days=P.FOUNDRY_LEAD), s, kegs))
                    if rec:
                        ev["brew"].append((d, s, kegs))
                continue
            rate = sum(self.ema[(s, dp)] for dp in P.DEPOTS)
            if rate <= 0:
                rate = 0.6 * sum(self.ema[(x, dp)] for x in self.foundry_skus for dp in P.DEPOTS) / max(1, len(self.foundry_skus))
            if len(self.fg[s]) + intank[s] < max(12, rate * (P.FOUNDRY_LEAD + P.FOUNDRY_COVER)):
                self.tanks.append((d + dt.timedelta(days=P.FOUNDRY_LEAD), s, P.FOUNDRY_LOT))
                intank[s] += P.FOUNDRY_LOT
                if rec:
                    ev["brew"].append((d, s, P.FOUNDRY_LOT))
        keep = []
        for fd, s, n in self.tanks:
            if fd > d:
                keep.append((fd, s, n))
                continue
            got = 0
            for _ in range(n):
                k = self.take_clean(20, d)
                if k is None:
                    break
                k.sku, k.where = s, "FG"
                self.fg[s].append(k)
                fills.append(k)
                got += 1
            if got < n:
                keep.append((d + ONE, s, n - got))
                if rec:
                    ev["short"].append((d, 20, n - got))
        self.tanks = keep
        for k in fills:
            k.out_at = d
            if rec:
                ev["fill"].append((d, k.id, k.size, k.sku))
                if k.tag and rng.random() < P.READ["FILL"]:
                    ev["read"].append((d, k.id, "FILL", "BRG-RACK"))
        # Foundry beer past its 120 days in the cold store is poured away and the keg goes back to the washer
        for code in list(self.fg.keys()):
            if code.startswith("F"):
                q = self.fg[code]
                while q and (d - q[0].out_at).days > P.FOUNDRY_LIFE:
                    k = q.popleft()
                    k.where = "REPAIR"
                    self.repair[d + ONE].append(k)
                    if rec:
                        ev["ullage"].append((d, k.id, code))
        if d.weekday() < 6:
            on = [c for c in self.fg if c.startswith("F")]
            for dp in P.DEPOTS:
                ftot = sum(self.ema[(c, dp)] for c in on)
                for code in list(self.fg.keys()):
                    rate = self.ema[(code, dp)] if not code.startswith("F") else ftot / max(1, len(on))
                    tgt = int(math.ceil(rate * 2.5)) + (2 if code.startswith("F") else 6)
                    n = min(max(0, tgt - len(self.depot_full[dp][code])), len(self.fg[code]))
                    for _ in range(n):
                        k = self.fg[code].popleft()
                        k.where = "DEPOT"
                        self.depot_full[dp][code].append(k)

    def take_clean(self, size, d):
        if self.clean[size]:
            return self.clean[size].popleft()
        if not self.unconstrained:
            return None
        k = Keg(len(self.w.kegs), size, "NEW", False)
        self.w.kegs.append(k)
        self.new_kegs += 1
        return k

    def active_foundry(self, d):
        if self.plan is None:
            return self.foundry_skus
        return [s for s, (a, b, _) in self.plan.items() if a - dt.timedelta(days=P.FOUNDRY_LEAD + 7) <= d <= b]

    # ---------------------------------------------------------------------------------------------- the trade
    def rate(self, ln, d, temp):
        o = ln.outlet
        g = 0.0 if o.estate else P.GROWTH[o.channel]
        yrs = (d - dt.date(2024, 1, 1)).days / 365.25
        r = ln.rate * (1 + g) ** yrs * season(d) * bank(d) * P.DOW[d.weekday()] / 7.0
        if temp > 17.0:
            r *= 1.0 + ln.temp_k * (temp - 17.0)
        else:
            r *= 1.0 + 0.006 * (temp - 17.0)
        if d.month == 12 and d.day >= 10:
            r *= ln.xmas / 1.12
        return r

    def sales(self, d, temp, rec):
        rng = self.rng
        for o in self.w.outlets:
            if o.opened > d or (o.closed and o.closed < d):
                continue
            if o.seasonal and not seasonal_open(d):
                continue
            for ln in o.lines:
                if ln.since and ln.since > d:
                    continue
                need = self.rate(ln, d, temp) * ln.size * rng.gamma(4.0, 0.25)
                while ln.ontap and need > 0:
                    slot = ln.ontap[0]
                    take = min(slot[1], need)
                    slot[1] -= take
                    need -= take
                    if slot[1] <= 1e-9:
                        ln.ontap.pop(0)
                        self.emptied(ln, slot[0], d, rec)
                    while len(ln.ontap) < ln.taps and ln.fulls:
                        nk = ln.fulls.popleft()
                        nk.where = "ONTAP"
                        ln.ontap.append([nk, float(ln.size)])

    def emptied(self, ln, k, d, rec):
        rng, ev = self.rng, self.ev
        ch = P.CHANNELS[ln.outlet.channel]
        loss = ch["loss"][0] if d < P.DEPOSIT_DAY else ch["loss"][1]
        u = rng.random()
        if u < loss:
            k.where = "LOST"
            if rec:
                ev["lost"].append((d, k.id, ln.outlet.id, "trip"))
            if rng.random() < P.RECOVER_SHARE:
                self.recov_pipe[d + dt.timedelta(days=int(rng.integers(*P.RECOV_LAG)))].append(k)
                k.where = "RECOVERY"
            return
        if u < loss + ch["exch"]:
            back = d + dt.timedelta(days=int(rng.integers(*P.EXCH_LAG)))
            self.exch_pipe[back].append(k)
            k.where = "EXCHANGE"
            if rec:
                ev["exch_taken"].append((d, k.id, back))
            return
        k.where = "EMPTY"
        ln.empties.append(k)

    def visit(self, o, d, rec):
        rng, ev = self.rng, self.ev
        ch = P.CHANNELS[o.channel]
        coll = {s: 0 for s in P.SIZES}
        deliv = {s: 0 for s in P.SIZES}
        for ln in o.lines:
            for k in ln.empties:
                k.where = "DEPOT_E"
                self.depot_empty[o.depot].append(k)
                coll[ln.size] += 1
            ln.empties = []
        foreign = {s: int(rng.poisson(ch["foreign"] * coll[s])) for s in P.SIZES}
        for s in P.SIZES:
            if foreign[s]:
                self.depot_empty[o.depot].append((s, foreign[s]))
        if not (o.closed and (o.closed - d).days < 7):
            for ln in o.lines:
                if ln.since and ln.since > d + dt.timedelta(days=7):
                    continue
                target = max(1, int(math.ceil(ln.rate * season(d) * (o.interval + P.COVER_DAYS) / 7.0)))
                want = max(0, target - len(ln.fulls)) + max(0, ln.taps - len(ln.ontap))
                for _ in range(want):
                    k = self.pick_full(self.depot_full[o.depot], ln)
                    if k is None:
                        if rec:
                            ev["short_depot"].append((d, o.depot, ln.sku))
                        break
                    k.out_at = d
                    self.today[(k.sku, o.depot)] += 1
                    if len(ln.ontap) < ln.taps:
                        k.where = "ONTAP"
                        ln.ontap.append([k, float(ln.size)])
                    else:
                        k.where = "OUTLET"
                        ln.fulls.append(k)
                    deliv[ln.size] += 1
                    if rec:
                        ev["deliver"].append((d, k.id, o.id, k.size, k.sku))
                        if k.tag and rng.random() < P.READ["DELIVER"]:
                            ev["read"].append((d, k.id, "DELIVER", o.id))
        if rec:
            ev["visit"].append((d, o.id, o.depot, deliv, coll, foreign))

    def pick_full(self, stock, ln):
        if ln.foundry:
            best = None
            for code, q in stock.items():
                if code.startswith("F") and q and (best is None or len(q) > len(stock[best])):
                    best = code
            return stock[best].popleft() if best else None
        q = stock.get(ln.sku)
        return q.popleft() if q else None

    def close_outlet(self, o, d, rec):
        rng, ev = self.rng, self.ev
        for ln in o.lines:
            held = [s[0] for s in ln.ontap] + list(ln.fulls) + list(ln.empties)
            ln.ontap, ln.fulls, ln.empties = [], deque(), []
            for k in held:
                u = rng.random()
                if u < P.CLOSE_FATE[0]:
                    k.where = "DEPOT_E"
                    self.depot_empty[o.depot].append(k)
                    continue
                k.where = "LOST"
                if rec:
                    ev["lost"].append((d, k.id, o.id, "closure"))
                if u < P.CLOSE_FATE[0] + P.CLOSE_FATE[1]:
                    self.recov_pipe[d + dt.timedelta(days=int(rng.integers(*P.RECOV_LAG)))].append(k)
                    k.where = "RECOVERY"

    def site_counts(self):
        out = {}
        for s in P.SIZES:
            out[("Brighouse washer yard", "clean empty", s)] = len(self.clean[s])
            out[("Brighouse cold store", "full", s)] = sum(len(q) for c, q in self.fg.items() if self.sku_size(c) == s)
            out[("Brighouse keg repair cage", "awaiting repair", s)] = sum(
                1 for day, ks in self.repair.items() for k in ks if k.size == s)
            for dp, name in P.DEPOTS.items():
                out[(name + " depot", "full", s)] = sum(len(q) for c, q in self.depot_full[dp].items()
                                                         if self.sku_size(c) == s)
                own = sum(1 for x in self.depot_empty[dp] if not isinstance(x, tuple) and x.size == s)
                own += sum(1 for day, xs in self.trunk.items() for x in xs
                           if not isinstance(x, tuple) and x.size == s and P.TRUNK_DAYS[dp] >= 0 and False)
                out[(name + " depot", "empty", s)] = own
            out[("in transit to Brighouse", "empty", s)] = sum(1 for day, xs in self.trunk.items() for x in xs
                                                                if not isinstance(x, tuple) and x.size == s)
            out[("other brewers' kegs held for the exchange", "foreign", s)] = self.foreign_pile[s] + sum(
                x[1] for day, xs in self.trunk.items() for x in xs if isinstance(x, tuple) and x[0] == s)
        return out

    def sku_size(self, code):
        if code.startswith("F"):
            return 20
        return self.w.sku_info[code][2]

    def snapshot(self):
        out = {s: defaultdict(int) for s in P.SIZES}
        for k in self.w.kegs:
            if k.status == "ACTIVE" and k.where is not None:
                out[k.size][k.where] += 1
        return {s: dict(v) for s, v in out.items()}


def run_history(w):
    e = Engine(w)
    e.byid = {o.id: o for o in w.outlets}
    arng = np.random.default_rng(P.SEED + 7)
    q_days = [dt.date(2025, 2, 10), dt.date(2025, 5, 12), dt.date(2025, 8, 11), dt.date(2025, 11, 10),
              dt.date(2026, 2, 9), dt.date(2026, 5, 11), dt.date(2026, 8, 10), dt.date(2026, 11, 9)]
    for q in q_days:
        live = [o for o in w.outlets if o.opened <= q and (o.closed is None or o.closed > q + dt.timedelta(days=30))
                and not (o.seasonal and not seasonal_open(q))]
        wt = np.array([sum(ln.rate for ln in o.lines) ** 0.7 for o in live])
        pick = arng.choice(len(live), size=170, replace=False, p=wt / wt.sum())
        for j in pick:
            day = q + dt.timedelta(days=int(arng.integers(0, 18)))
            if day.weekday() >= 5:
                day -= dt.timedelta(days=2)
            e.audits.setdefault(day, []).append(live[j].id)
    for d in daterange(P.D0, P.ASOF):
        e.step(d)
    w.engine = e
    w.ev = e.ev
    return w


# ---------------------------------------------------------------------------------------------- 2027 plans and truth
def season_factor(d, temp, temp_k):
    f = season(d) * bank(d)
    f *= 1.0 + temp_k * (temp - 17.0) if temp > 17.0 else 1.0 + 0.006 * (temp - 17.0)
    return f


def make_plans(w):
    """the 2027 plans the pack files: Maplestead's pubs and lines, the new Foundry taps, the Foundry brew plan"""
    rng = np.random.default_rng(P.SEED + 2027)
    plans = {}
    depots = list(P.DEPOT_SHARE)
    dprob = np.array([P.DEPOT_SHARE[k] for k in depots])
    estate = []
    for i in range(P.ESTATE_PUBS):
        dep = depots[rng.choice(len(depots), p=dprob)]
        start = P.ESTATE_DAY + dt.timedelta(days=7 * int(rng.integers(0, 3)))
        lines = {}
        for code, (med, sd) in P.ESTATE_LINES.items():
            lines[code] = round(float(med * math.exp(rng.normal(0, sd))), 2)
        estate.append({"pub": "MI%03d" % (i + 1), "depot": dep, "start": start, "lines": lines})
    plans["estate"] = estate
    # new Foundry taps at existing accounts from April 2027 (a fifth more Foundry lines)
    has = [o for o in w.outlets if any(ln.foundry for ln in o.lines) and (o.closed is None or o.closed > P.ASOF)]
    cand = [o for o in w.outlets if not any(ln.foundry for ln in o.lines) and o.opened <= P.ASOF and
            (o.closed is None or o.closed > dt.date(2027, 10, 1)) and not o.seasonal]
    n_new = int(round(len(has) * P.FOUNDRY_OUTLET_GROWTH))
    pick = rng.choice(len(cand), size=n_new, replace=False)
    taps = []
    for j in sorted(pick):
        o = cand[j]
        taps.append({"outlet": o.id, "start": dt.date(2027, 4, 5) + dt.timedelta(days=7 * int(rng.integers(0, 4))),
                     "rate": round(float(P.LINES["FND"][1] * 0.9 * math.exp(rng.normal(0, 0.35))), 2)})
    plans["foundry_taps"] = taps
    windows = {s: (dt.date(2026, 12, 1), dt.date(2027, 12, 31)) for s in P.FOUNDRY_2026}
    windows.update({s: (dt.date(2027, 1, 4), dt.date(2027, 12, 31)) for s in P.FOUNDRY_2027_CORE[8:]})
    windows.update(P.FOUNDRY_2027_SEASONAL)
    plans["foundry_windows"] = windows
    return plans


def foundry_brew_plan(w, plans, eng):
    """the head brewer's 2027 brew plan: each beer's expected dispatch (the range's expected sales shared across the
    beers on sale), brewed in whole lots whenever its stock and tank fall under its dispatch over the lead time and a
    week, from the stock each beer holds at the start of December"""
    exp_lines = []
    for o in w.outlets:
        if o.closed is not None and o.closed <= P.ASOF:
            continue
        for ln in o.lines:
            if ln.foundry:
                exp_lines.append((ln.rate, None, o.channel, o.seasonal))
    for t in plans["foundry_taps"]:
        exp_lines.append((t["rate"], t["start"], "FREE", False))
    stock = defaultdict(int)
    for s, q in eng.fg.items():
        stock[s] += len(q)
    for dp in P.DEPOTS:
        for s, q in eng.depot_full[dp].items():
            stock[s] += len(q)
    tanks = [(fd, s, n) for fd, s, n in eng.tanks]
    brews = {s: {} for s in plans["foundry_windows"]}
    for fd, s, n in tanks:          # the brews already in tank at the end of November
        bd = fd - dt.timedelta(days=P.FOUNDRY_LEAD)
        brews.setdefault(s, {})[bd] = brews.get(s, {}).get(bd, 0) + n
    wins = plans["foundry_windows"]
    for d in daterange(P.ASOF + ONE, P.Y27_END):
        temp = w.weather.normal(d)
        tot = 0.0
        for r, since, ch, seas in exp_lines:
            if since and since > d:
                continue
            if seas and not seasonal_open(d):
                continue
            g = P.GROWTH[ch]
            yrs = (d - dt.date(2024, 1, 1)).days / 365.25
            tot += r * (1 + g) ** yrs * season_factor(d, temp, P.FOUNDRY_TEMP) / 7.0
        on = [s for s, (a, b) in wins.items() if a <= d <= b]
        per = tot / max(1, len(on))
        for fd, s, n in tanks:
            if fd == d:
                stock[s] += n
        tanks = [x for x in tanks if x[0] > d]
        for s in on:
            stock[s] = max(0.0, stock[s] - per)
        for s, (a, b) in wins.items():
            if not (a - dt.timedelta(days=P.FOUNDRY_LEAD + 7) <= d <= b - dt.timedelta(days=P.FOUNDRY_LEAD + 21)):
                continue
            intank = sum(n for fd, x, n in tanks if x == s)
            if stock[s] + intank < max(12, per * (P.FOUNDRY_LEAD + P.FOUNDRY_COVER)):
                tanks.append((d + dt.timedelta(days=P.FOUNDRY_LEAD), s, P.FOUNDRY_LOT_2027))
                brews[s][d] = brews[s].get(d, 0) + P.FOUNDRY_LOT_2027
    return {s: (wins[s][0], wins[s][1], brews[s]) for s in wins}


def run_2027(w, plans, like=None):
    """carry the 30 November 2026 state through 2027 with the plans at normal weather (or a past year's), drawing new
    kegs whenever the washer runs dry; returns the truth the checks hold the golden to"""
    eng = w.engine
    rng = w.rng
    w.weather.like = like
    eng.record_from = P.ASOF + ONE
    eng.record_to = P.Y27_END
    eng.ev = defaultdict(list)
    eng.unconstrained = True
    brew = foundry_brew_plan(w, plans, eng)
    plans["foundry_brews"] = {s: v[2] for s, v in brew.items()}
    eng.plan = brew
    eng.foundry_skus = list(brew)
    sku_info = w.sku_info
    depots_rng = np.random.default_rng(P.SEED + 99)
    est_outlets = []
    for e in plans["estate"]:
        o = Outlet(e["pub"], "GROUP", e["depot"], False, e["start"], None)
        o.group = P.ESTATE
        o.estate = True
        for code, r in e["lines"].items():
            s = sku_info[code]
            o.lines.append(Line(o, code, s[2], r, s[4], s[5]))
        o.interval = 7
        o.days = (int(depots_rng.integers(0, 5)),)
        est_outlets.append(o)
    w.outlets.extend(est_outlets)
    byid = {o.id: o for o in w.outlets}
    for t in plans["foundry_taps"]:
        o = byid[t["outlet"]]
        o.lines.append(Line(o, "FND", 20, t["rate"], P.FOUNDRY_TEMP, 1.10, foundry=True, since=t["start"]))
    daily = []
    orig_lots = set(w.lots)
    for d in daterange(P.ASOF + ONE, dt.date(2027, 9, 30)):
        eng.step(d)
        if P.SEASON[0] <= d <= P.SEASON[1]:
            c = {s: defaultdict(int) for s in P.SIZES}
            orig = {s: 0 for s in P.SIZES}
            for k in w.kegs:
                if k.status != "ACTIVE" or k.where in (None, "LOST", "RECOVERY", "SCRAP"):
                    continue
                c[k.size][k.where] += 1
                if k.lot in orig_lots:
                    orig[k.size] += 1
            est = {s: 0 for s in P.SIZES}
            for o in est_outlets:
                for ln in o.lines:
                    est[ln.size] += len(ln.ontap) + len(ln.fulls) + len(ln.empties)
            fgf = {s: 0 for s in P.SIZES}
            for code, q in eng.fg.items():
                if code.startswith("F"):
                    fgf[20] += len(q)
            for dp in P.DEPOTS:
                for code, q in eng.depot_full[dp].items():
                    if code.startswith("F"):
                        fgf[20] += 0
            daily.append((d, {s: dict(v) for s, v in c.items()}, orig, est, fgf))
    w.weather.like = None
    return {"daily": daily, "ev": eng.ev, "new_kegs": eng.new_kegs, "estate": est_outlets}
