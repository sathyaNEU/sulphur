"""The clean truth: Havørn Regional's fleet flown day by day from January 2023 to the end of November 2026, and the
2027 programme replayed many times from the end of November for the truth the golden is checked against.

The process, as the airline's systems see it. Each aircraft flies rotations out of its base; every leg adds a
landing, the engines' starts and flight hours to every unit installed on it. Each unit fails on its own exposure
(landings, starts, hours or days since its last shop visit, a Weibull wear-out), more often on cold days for the parts
that mind the cold, much more often if it carries a latent defect the shop never clears, less often once the
propeller control's bulletin is embodied. Aircraft also develop intermittent faults in their own wiring and
connectors; each symptom is met at the station by swapping the unit or by troubleshooting, and only troubleshooting
(or a heavy check) finds the fault, so a faulty aircraft goes through serviceable units until someone finds it. Every
removed unit is replaced from the pool if a spare is in stores, travels to the Bodø shop or a vendor, waits its turn,
is tested, repaired or found serviceable, and comes back; a pool that runs dry is relieved by robbing an aircraft in
its check, or the aircraft waits on the ground."""
import copy
import datetime as dt
import math
import zlib

import numpy as np

import params as P

DAY = dt.timedelta(days=1)


# ----------------------------------------------------------------------------------------------- calendar helpers

def easter(y):
    a = y % 19
    b, c = divmod(y, 100)
    d, e = divmod(b, 4)
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = divmod(c, 4)
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    mo = (h + l - 7 * m + 114) // 31
    da = ((h + l - 7 * m + 114) % 31) + 1
    return dt.date(y, mo, da)


def holidays(y):
    e = easter(y)
    return {dt.date(y, 1, 1), e - 3 * DAY, e - 2 * DAY, e + DAY, dt.date(y, 5, 1), dt.date(y, 5, 17), e + 39 * DAY,
            e + 50 * DAY, dt.date(y, 12, 25), dt.date(y, 12, 26)}


HOL = set()
for _y in range(2022, 2029):
    HOL |= holidays(_y)


def utc_offset(d):
    def last_sunday(y, m):
        x = dt.date(y, m, 31)
        return x - dt.timedelta(days=(x.weekday() + 1) % 7)
    return 2 if last_sunday(d.year, 3) <= d < last_sunday(d.year, 10) else 1


def on_holiday(tech, d):
    """Each technician's three summer weeks, staggered so the shop never closes (the order turns each year), and one
    technician's Christmas week."""
    order = ["SE", "KH", "MB"]
    k = d.year % 3
    order = order[k:] + order[:k]
    wk = d.isocalendar()[1]
    for i, t in enumerate(order):
        if t == tech and 27 + 3 * i <= wk <= 29 + 3 * i:
            return True
    return d.month == 12 and d.day >= 22 and tech == order[0]


def season(d):
    s = {1: 0.90, 2: 0.95, 3: 0.98, 4: 1.0, 5: 1.02, 6: 1.08, 7: 1.10, 8: 1.07, 9: 1.01, 10: 0.99, 11: 0.97,
         12: 0.95}[d.month]
    if d.weekday() == 5:
        s *= 0.52
    elif d.weekday() == 6:
        s *= 0.74
    return s


# ----------------------------------------------------------------------------------------------- weather

def weather(rng, d0, d1):
    """Daily minimum and maximum temperature at each base: the seasonal cycle, day-to-day persistence, and cold
    snaps that reach the northern bases together."""
    days = (d1 - d0).days + 1
    dates = [d0 + i * DAY for i in range(days)]
    snaps = np.zeros(days)
    i = 0
    while i < days:
        d = dates[i]
        if d.month in (11, 12, 1, 2, 3) and rng.random() < 0.021:
            length = int(rng.integers(3, 11))
            depth = float(rng.uniform(6, 15))
            for j in range(length):
                if i + j < days:
                    ramp = min(1.0, (j + 1) / 2.0) * min(1.0, (length - j) / 2.0)
                    snaps[i + j] = max(snaps[i + j], depth * ramp)
            i += length
        i += 1
    out = {}
    for b, p in P.BASES.items():
        phi, sd = 0.72, 2.6
        e = 0.0
        tmin, tmax = np.zeros(days), np.zeros(days)
        for k, d in enumerate(dates):
            doy = d.timetuple().tm_yday
            clim = (p["jan"] + p["jul"]) / 2 - (p["jul"] - p["jan"]) / 2 * math.cos(2 * math.pi * (doy - 18) / 365.25)
            e = phi * e + float(rng.normal(0, sd))
            t = clim + e - p["snap"] * snaps[k] * (0.8 + 0.4 * rng.random())
            tmin[k] = round(t, 1)
            tmax[k] = round(t + 4.0 + 3.0 * math.sin(math.pi * doy / 366) ** 2 + float(rng.normal(0, 1.2)), 1)
        out[b] = {"tmin": tmin, "tmax": tmax}
    return dates, out, snaps


# ----------------------------------------------------------------------------------------------- fleet

TAILS = ["LN-HV" + c for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"] + ["LN-HW" + c for c in "ABCD"]


def fleet(rng):
    """The register: thirty aircraft delivered 1998 to 2007, four bases with a few transfers, a heavy check roughly
    every two years at Bodø."""
    msn = sorted(rng.choice(np.arange(503, 641), size=P.FLEET_N, replace=False).tolist())
    order = rng.permutation(P.FLEET_N)
    bases = []
    for b, n in P.BASE_SPLIT.items():
        bases += [b] * n
    ac = []
    for j in range(P.FLEET_N):
        m = msn[order[j]]
        y = 1998 + (m - 503) // 15
        ac.append({"tail": TAILS[j], "msn": int(m), "delivered": dt.date(y, int(rng.integers(1, 13)), int(rng.integers(1, 28))),
                   "base0": bases[j]})
    hist = {a["tail"]: [(P.D0, a["base0"])] for a in ac}
    # temporary detachments: an aircraft lent to another base for a season and returned
    for t in rng.choice([a["tail"] for a in ac], size=7, replace=False):
        cur = hist[t][-1][1]
        when = P.D0 + dt.timedelta(days=int(rng.integers(90, 1250)))
        new = str(rng.choice([b for b in P.BASES if b != cur]))
        back = when + dt.timedelta(days=int(rng.integers(45, 160)))
        if back < P.ASOF - dt.timedelta(days=20):
            hist[t] += [(when, new), (back, cur)]
    checks = {}
    for k, a in enumerate(ac):
        start = P.D0 + dt.timedelta(days=int(20 + (k * 53) % 720 + rng.integers(0, 20)))
        lst = []
        while start < dt.date(2028, 3, 1):
            length = int(rng.integers(17, 26))
            lst.append((start, start + dt.timedelta(days=length - 1)))
            start += dt.timedelta(days=int(rng.integers(690, 770)))
        checks[a["tail"]] = lst
    return ac, hist, checks


def base_on(hist, tail, d):
    b = hist[tail][0][1]
    for when, new in hist[tail]:
        if d >= when:
            b = new
    return b


def check_on(checks, tail, d):
    for a, b in checks[tail]:
        if a <= d <= b:
            return a
    return None


# ----------------------------------------------------------------------------------------------- flying

def rotation(rng, net, legs_mean, scale):
    n = int(rng.poisson(legs_mean * scale))
    if n < 2:
        return []
    n -= n % 2
    w = np.array([x[2] for x in net], dtype=float)
    w /= w.sum()
    out = []
    while len(out) < n:
        dest, blk, _ = net[int(rng.choice(len(net), p=w))]
        if rng.random() < 0.18 and len(out) + 4 <= n:
            dest2, blk2, _ = net[int(rng.choice(len(net), p=w))]
            if dest2 != dest:
                link = max(12, int(abs(blk2 - blk)) + 14)
                out += [("BASE", dest, blk), (dest, dest2, link), (dest2, "BASE", blk2)]
                continue
        out += [("BASE", dest, blk), (dest, "BASE", blk)]
    return out[:n]


def fly_day(rng, base, d, scale, net, legs_mean, winter_slow=1.0):
    legs = []
    off = utc_offset(d)
    t = dt.datetime.combine(d, dt.time(6, 0)) + dt.timedelta(minutes=int(rng.integers(0, 50)))
    for dep, arr, blk in rotation(rng, net, legs_mean, scale):
        dep = base if dep == "BASE" else dep
        arr = base if arr == "BASE" else arr
        block = max(9, int(round(blk * winter_slow + rng.normal(0, max(2.0, blk * 0.07)))))
        tx_out = min(P.TAXI.get(dep, P.TAXI_SMALL) + int(rng.integers(0, 4)), block // 3)
        tx_in = min(P.TAXI.get(arr, P.TAXI_SMALL) + int(rng.integers(0, 3)), block // 3)
        out_t = t
        z = dt.timedelta(hours=off)
        legs.append({"dep": dep, "arr": arr, "out": out_t - z, "off": out_t + dt.timedelta(minutes=tx_out) - z,
                     "on": out_t + dt.timedelta(minutes=block - tx_in) - z, "in": out_t + dt.timedelta(minutes=block) - z,
                     "block": block, "flight": block - tx_out - tx_in})
        t = out_t + dt.timedelta(minutes=block + int(rng.integers(20, 40)))
    return legs


def network_for(base, d, tail, movers):
    """The network a tail flies on a day: its base's, or the Helgeland package for the movers from April 2027."""
    if d >= P.HELGELAND and movers.get(tail) == "HEL":
        return P.HELGELAND_NET, P.HELGELAND_LEGS
    return P.NETWORK[base], P.LEGS_PER_DAY[base]


def base_2027(hist, movers, tail, d):
    if d >= P.HELGELAND and tail in movers:
        return "BOO" if movers[tail] == "HEL" else movers[tail]
    return base_on(hist, tail, d)


# ----------------------------------------------------------------------------------------------- parts

KIT_PARTS = ("SG", "BRK", "BAT", "ADC", "VHF", "WXR", "WHC", "FDU", "CPC", "PDT")

POS_NAMES = {"SG": ["ENG 1", "ENG 2"], "PEC": ["ENG 1", "ENG 2"], "HYP": ["ENG 1", "ENG 2"],
             "BRK": ["LH OB", "LH IB", "RH IB", "RH OB"], "FBP": ["LH TANK", "RH TANK"], "BAV": ["LH", "RH"],
             "WHC": ["CAPT", "F/O"], "BAT": ["MAIN", "AUX"], "FLA": ["LH", "RH"], "ADC": ["NO 1", "NO 2"],
             "VHF": ["NO 1", "NO 2"]}


def pos_names(k):
    return POS_NAMES.get(k, ["SINGLE"])


def eta(p):
    return (1000.0 / p["rate"]) / math.gamma(1 + 1 / p["beta"])


SN_FORM = {"SG": ("SG", 4100, 4), "BRK": ("B", 10200, 5), "BAV": ("V", 2300, 4), "NWS": ("NS", 700, 3),
           "BAT": ("BT", 52000, 5), "CPC": ("C", 1800, 4), "FLA": ("FA", 900, 3), "ADC": ("ADC", 6100, 4),
           "WXR": ("RT", 3300, 4), "VHF": ("V2", 8800, 4), "PEC": ("PEC", 1100, 4), "PDT": ("DT", 450, 3),
           "HYP": ("HP", 2600, 4), "FBP": ("FP", 5100, 4), "WHC": ("WH", 1500, 4), "FDU": ("FD", 3900, 4)}


def new_serial(rng, k, used):
    pre, base, width = SN_FORM[k]
    while True:
        n = base + int(rng.integers(0, 10 ** width // 3))
        sn = "%s%0*d" % (pre, width, n)
        if sn not in used:
            used.add(sn)
            return sn


def exposure_inc(p, cyc, sta, fh):
    return {"cyc": cyc, "sta": sta, "fh": fh, "cal": 1.0}[p["drv"]]


def cold_mult(p, tmin, month):
    return 1.0 + p["cold"] * max(0.0, -tmin)


# ----------------------------------------------------------------------------------------------- the engine

class Engine:
    """The airline's maintenance state and its daily process; the history and every 2027 replay run it."""

    def __init__(self, seed):
        self.seed = seed
        self.rng = np.random.default_rng(seed)
        self.reseed(seed)

    def reseed(self, seed):
        """One stream for the flying, one for the shop, one for the aircraft faults, one for each part's own
        failures and repairs, so a change in one part's process leaves the others' draws where they were."""
        self.rng = np.random.default_rng(seed)
        self.srng = np.random.default_rng(seed + 11)
        self.frng = np.random.default_rng(seed + 13)
        self.prng = {p["k"]: np.random.default_rng(seed + 100 + i) for i, p in enumerate(P.PARTS)}

    # ---- set-up for the history
    def setup(self, ac, hist, checks):
        self.ac, self.hist, self.checks = ac, hist, checks
        self.tails = [a["tail"] for a in ac]
        self.used = set()
        self.units, self.install, self.pool = {}, {}, {k: [] for k in P.PART}
        for ip, p in enumerate(P.PARTS):
            k = p["k"]
            rng = np.random.default_rng(self.seed + 300 + ip)
            e = eta(p)
            total = len(self.tails) * p["pos"] + P.POOL[k]
            sns = [new_serial(rng, k, self.used) for _ in range(total)]
            rog = rng.random(total) < p["rogue"][0]
            for j, sn in enumerate(sns):
                tsn = float(rng.uniform(4000, 38000))
                rr = p["rogue"][1] * float(rng.uniform(0.7, 1.3))
                self.units[sn] = {"k": k, "sn": sn, "rogue": bool(rog[j]), "age": float(rng.uniform(0.05, 0.95)) * e,
                                  "mod": False, "fla_mod": k != "FLA", "tsn": tsn, "csn": tsn * float(rng.uniform(1.15, 1.75)),
                                  "known": bool(rng.random() > 0.17), "status": "store", "where": None, "new": False,
                                  "last_visit": None, "rogue_rate": rr}
            j = 0
            for t in self.tails:
                for pos in pos_names(k):
                    self.install[(t, k, pos)] = sns[j]
                    self.units[sns[j]]["status"] = "inst"
                    self.units[sns[j]]["where"] = (t, pos)
                    j += 1
            self.pool[k] = sns[j:]
        # station kits: one unit of each kit part at each outstation, the rest in the Bodø pool
        self.kits = {(s, k): [] for s in ("TOS", "BGO", "TRD") for k in P.PART}
        for k in KIT_PARTS:
            for s in ("TOS", "BGO", "TRD"):
                if len(self.pool[k]) > 1:
                    sn = self.pool[k].pop()
                    self.kits[(s, k)].append(sn)
                    self.units[sn]["where"] = ("KIT", s)
        # aircraft-side intermittent faults, through the end of 2027
        frng = np.random.default_rng(self.seed + 4)
        self.faults = []
        years = ((dt.date(2027, 12, 31) - P.D0).days + 1) / 365.25
        for p in P.PARTS:
            if p["fault"] <= 0:
                continue
            for t in self.tails:
                for _ in range(int(frng.poisson(p["fault"] * years))):
                    onset = P.D0 + dt.timedelta(days=int(frng.integers(0, int(years * 365))))
                    pos = pos_names(p["k"])[int(frng.integers(0, p["pos"]))]
                    self.faults.append({"id": len(self.faults) + 1, "tail": t, "k": p["k"], "pos": pos, "onset": onset,
                                        "sym": float(frng.uniform(0.07, 0.16)), "fixed": None, "how": None, "swaps": 0,
                                        "rng": np.random.default_rng(zlib.crc32(("%d|%s|%s|%s" % (self.seed, p["k"], t, onset)).encode()))})
        self.faults.sort(key=lambda f: (f["onset"], f["id"]))
        self.queue, self.returns, self.waiting, self.robbed, self.purchases = [], [], [], [], []
        self.changes, self.shop_jobs, self.vendor_jobs, self.roster, self.legs, self.expo = [], [], [], [], [], []
        self.seq = {"cc": {}, "wo": 0, "ro": 0}
        self.flt_no = {}
        self.fla_campaign = []
        self.record = True
        self.demand = {k: [] for k in P.PART}       # (date, cause) per unscheduled removal, for the fill rate
        self.backs = {k: [] for k in P.PART}         # (removal date, serviceable return date)

    # ---- numbering
    def change_no(self, d):
        """The maintenance system numbers every component change on the fleet; the pooled part numbers are a share
        of them, so the export's numbers run with gaps."""
        y = d.year % 100
        self.seq["cc"][y] = self.seq["cc"].get(y, 0) + 1 + int(zlib.crc32(("%s|%d" % (d, self.seq["cc"].get(y, 0))).encode()) % 7)
        return "CC-%02d-%05d" % (y, self.seq["cc"][y])

    # ---- the shop and the vendors
    def send(self, sn, d, station, finding):
        u = self.units[sn]
        p = P.PART[u["k"]]
        r = self.prng[u["k"]]
        u["status"] = "repair"
        if p["shop"] == "BOO":
            arrive = d + dt.timedelta(days=P.BASES[station]["ship_days"] + (1 if station != "BOO" and r.random() < 0.3 else 0))
            if finding == "NFF":
                hours = p["nff_work"] * float(r.lognormal(0, 0.25))
            elif finding == "BER":
                hours = 0.55 * p["work"] * float(r.lognormal(0, 0.2))
            else:
                hours = p["work"] * float(r.lognormal(0, 0.33))
            self.seq["wo"] += 1
            parts = arrive
            if finding == "CF":
                parts = arrive + dt.timedelta(days=int(round(P.PARTS_WAIT * float(r.lognormal(0, 0.45)))))
            job = {"wo": "WO%06d" % (310000 + self.seq["wo"]), "k": u["k"], "sn": sn, "arrive": arrive, "removed": d,
                   "parts": parts, "ready": parts, "hours": hours, "left": hours, "start": None, "done": None,
                   "finding": finding, "type": "rotable", "text": self.text(u["k"], finding, u["rogue"]), "tech": None}
            self.queue.append(job)
            if self.record:
                self.shop_jobs.append(job)
        else:
            out = d + dt.timedelta(days=int(r.integers(1, 4)))
            mean = p["nff_work"] if finding == "NFF" else p["work"]
            tat = max(4, int(round(mean * float(r.lognormal(0, 0.28)))))
            back = out + dt.timedelta(days=tat + int(r.integers(2, 5)))
            mod = u["k"] == "PEC" and d >= P.SB_DATE and not u["mod"]
            self.seq["ro"] += 1 + int(zlib.crc32(("ro|%s|%d" % (d, self.seq["ro"])).encode()) % 4)
            job = {"order": "RO-%05d" % (21000 + self.seq["ro"]), "k": u["k"], "sn": sn, "removed": d, "sent": out,
                   "at_vendor": out + dt.timedelta(days=int(r.integers(1, 4))), "back": back, "finding": finding,
                   "text": self.text(u["k"], finding, u["rogue"]), "mod": mod, "vendor": p["vendor"], "ccy": p["ccy"]}
            if self.record:
                self.vendor_jobs.append(job)
            if finding == "BER":
                u["status"] = "scrap"
                self.buy(u["k"], back)
            else:
                self.returns.append((back, sn, mod))
                self.backs[u["k"]].append((d, back))

    def buy(self, k, d):
        r = self.prng[k]
        lead = int(r.integers(45, 110))
        sn = new_serial(r, k, self.used)
        if self.record:
            self.purchases.append({"k": k, "sn": sn, "ordered": d + dt.timedelta(days=int(r.integers(1, 6))),
                                   "delivered": d + dt.timedelta(days=lead)})
        p = P.PART[k]
        self.units[sn] = {"k": k, "sn": sn, "rogue": bool(r.random() < p["rogue"][0] * 0.5), "age": 0.0,
                          "mod": k == "PEC" and d >= P.SB_DATE, "fla_mod": True, "tsn": 0.0, "csn": 0.0, "known": True,
                          "status": "order", "where": None, "new": True, "last_visit": None}
        self.returns.append((d + dt.timedelta(days=lead), sn, False))

    def text(self, k, finding, rogue):
        T = TEXTS[k]
        r = self.prng[k]
        if finding == "NFF":
            return str(r.choice(T["nff"]))
        if finding == "BER":
            return str(r.choice(T["ber"]))
        return T["cf"][0] if rogue else str(r.choice(T["cf"]))

    def shop_day(self, d):
        r = self.srng
        if d.weekday() >= 5 or d in HOL:
            return
        techs = ["SE", "KH", "MB", "OL"]
        on = []
        for tch in techs[:P.SHOP_TECHS]:
            holiday = on_holiday(tch, d)
            sick = r.random() < 0.045
            absent = holiday or sick
            if self.record:
                self.roster.append({"date": d, "tech": tch, "hours": 0.0 if absent else 7.5,
                                    "absence": "FERIE" if holiday else ("SYK" if sick else "")})
            if not absent:
                on.append(tch)
        if not on:
            return
        share = P.OTHER_WORK_2027 if d >= P.OTHER_FROM else P.OTHER_WORK
        other = len(on) * P.SHOP_HOURS * share * float(r.uniform(0.85, 1.15))
        cap = len(on) * P.SHOP_HOURS - other
        if self.record:
            self.seq["wo"] += 1
            self.shop_jobs.append({"wo": "WO%06d" % (310000 + self.seq["wo"]), "k": None, "sn": "", "arrive": d,
                                   "removed": None, "hours": other, "left": 0.0, "start": d, "done": d, "finding": "",
                                   "type": "other", "text": str(r.choice(OTHER)), "tech": on[0]})
        for job in sorted([j for j in self.queue if j["ready"] <= d], key=lambda j: (j["ready"], j["wo"])):
            if cap <= 1e-9:
                break
            if job["start"] is None:
                job["start"] = d
                job["tech"] = on[int(r.integers(0, len(on)))]
            take = min(cap, job["left"])
            job["left"] -= take
            cap -= take
            if job["left"] <= 1e-9:
                job["done"] = d
                self.queue.remove(job)
                if job["finding"] == "BER":
                    self.units[job["sn"]]["status"] = "scrap"
                    self.buy(job["k"], d)
                else:
                    self.returns.append((d + DAY, job["sn"], False))
                    self.backs[job["k"]].append((job["removed"], d + DAY))

    def returns_day(self, d):
        today = [x for x in self.returns if x[0] == d]
        if not today:
            return
        self.returns = [x for x in self.returns if x[0] != d]
        for _, sn, mod in today:
            u = self.units[sn]
            if mod:
                u["mod"] = True
            u["last_visit"] = d
            if u["k"] == "FLA":
                u["fla_mod"] = True
            k = u["k"]
            u["status"] = "store"
            wait = [x for x in self.waiting if x[1] == k]
            if wait:
                tail, _, pos, _ = wait[0]
                self.waiting.remove(wait[0])
                self.fit(tail, k, pos, sn)
                self.log_fit(d, tail, k, pos, sn, "UNSCH", "Fitted, unit awaited from stores")
                continue
            home = u.get("from_station")
            empty = [s for s in ("TOS", "BGO", "TRD") if k in KIT_PARTS and not self.kits[(s, k)]]
            if home in empty:
                self.kits[(home, k)].append(sn)
            elif empty:
                self.kits[(empty[0], k)].append(sn)
            else:
                self.pool[k].append(sn)
        for donor, k, pos in list(self.robbed):
            if self.install.get((donor, k, pos)) is None and self.pool[k]:
                sn = self.pool[k].pop(0)
                self.fit(donor, k, pos, sn)
                self.log_fit(d, donor, k, pos, sn, "CONV", "Refitted after removal for another aircraft")
                self.robbed.remove((donor, k, pos))

    def log_fit(self, d, tail, k, pos, sn, reason, text):
        if self.record:
            self.changes.append({"no": self.change_no(d), "date": d, "station": "BOO", "tail": tail, "k": k, "pos": pos,
                                 "sn_off": "", "sn_on": sn, "reason": reason, "defect": text, "cause": "FIT",
                                 "tsn": 0.0, "csn": 0.0, "known": False})

    def fit(self, tail, k, pos, sn):
        self.install[(tail, k, pos)] = sn
        self.units[sn]["status"] = "inst"
        self.units[sn]["where"] = (tail, pos)

    # ---- a removal
    def remove(self, d, station, tail, k, pos, cause, reason="UNSCH"):
        sn_off = self.install[(tail, k, pos)]
        u = self.units[sn_off]
        sn_on = None
        filled = False
        u["from_station"] = station
        if station != "BOO" and self.kits.get((station, k)):
            sn_on = self.kits[(station, k)].pop(0)
            filled = True
        elif self.pool[k]:
            sn_on = self.pool[k].pop(0)
            filled = True
        elif any(self.kits[(s, k)] for s in ("TOS", "BGO", "TRD")):
            s = [s for s in ("TOS", "BGO", "TRD") if self.kits[(s, k)]][0]
            sn_on = self.kits[(s, k)].pop(0)
            filled = True
        elif reason == "UNSCH":
            donors = [t for t in self.tails if t != tail and check_on(self.checks, t, d) is not None]
            for donor in donors:
                dpos = pos_names(k)[0]
                cand = self.install.get((donor, k, dpos))
                if cand:
                    sn_on = cand
                    self.install[(donor, k, dpos)] = None
                    self.robbed.append((donor, k, dpos))
                    if self.record:
                        self.changes.append({"no": self.change_no(d), "date": d, "station": "BOO", "tail": donor,
                                             "k": k, "pos": dpos, "sn_off": cand, "sn_on": "", "reason": "CONV",
                                             "defect": "Removed for fitment to %s" % tail, "cause": "ROB",
                                             "tsn": self.units[cand]["tsn"], "csn": self.units[cand]["csn"],
                                             "known": self.units[cand]["known"]})
                    break
        if reason == "UNSCH":
            self.demand[k].append((d, cause, filled))
        if self.record:
            defect = DEFECTS[k][int(self.prng[k].integers(0, len(DEFECTS[k])))]
            num = str(pos_names(k).index(pos) + 1) if len(pos_names(k)) > 1 else ""
            if reason == "SCHED":
                defect = "Removed for SB 27-0089 embodiment"
            self.changes.append({"no": self.change_no(d), "date": d, "station": station, "tail": tail, "k": k,
                                 "pos": pos, "sn_off": sn_off, "sn_on": sn_on or "", "reason": reason,
                                 "defect": defect.format(num).replace("  ", " ").strip(), "cause": cause,
                                 "tsn": u["tsn"], "csn": u["csn"], "known": u["known"]})
        if sn_on:
            self.fit(tail, k, pos, sn_on)
        else:
            self.install[(tail, k, pos)] = None
            self.waiting.append((tail, k, pos, d))
        if reason == "SCHED":
            # the flap actuator's bulletin: out to the vendor for the modification, back as a repaired unit
            u["status"] = "repair"
            back = d + dt.timedelta(days=int(self.prng[k].integers(18, 30)))
            self.seq["ro"] += 1
            if self.record:
                self.vendor_jobs.append({"order": "RO-%05d" % (21000 + self.seq["ro"]), "k": k, "sn": sn_off, "removed": d,
                                         "sent": d + DAY, "at_vendor": d + 2 * DAY, "back": back, "finding": "SB",
                                         "text": "SB 27-0089 embodied (seal kit and rod end), no defect", "mod": False,
                                         "vendor": P.PART[k]["vendor"], "ccy": P.PART[k]["ccy"]})
            self.returns.append((back, sn_off, False))
        else:
            self.send(sn_off, d, station, cause)
        u["age"] = 0.0
        u["where"] = None

    # ---- one day
    def day(self, d, wx, idx, movers=None, flying=True):
        r = self.rng
        self.returns_day(d)
        self.shop_day(d)
        for a in self.ac:
            t = a["tail"]
            base = base_2027(self.hist, movers, t, d) if movers else base_on(self.hist, t, d)
            cs = check_on(self.checks, t, d)
            if cs is not None:
                if cs == d:
                    for f in self.faults:
                        if f["tail"] == t and f["fixed"] is None and f["onset"] <= d and self.frng.random() < 0.74:
                            f["fixed"], f["how"] = d, "check"
                continue
            if any(self.install.get((t, k, pos)) is None for k in P.PART for pos in pos_names(k)):
                continue
            net, lm = network_for(base, d, t, movers)
            legs = fly_day(r, base, d, season(d), net, lm, 1.04 if d.month in (12, 1, 2) else 1.0)
            cyc = len(legs)
            if cyc == 0:
                continue
            fh = sum(l["flight"] for l in legs) / 60.0
            sta = cyc + (1 if r.random() < 0.07 else 0)
            if self.record:
                for l in legs:
                    key = (l["dep"], l["arr"])
                    if key not in self.flt_no:
                        self.flt_no[key] = 100 + 2 * len(self.flt_no)
                    self.legs.append({"date": d, "flight": "HV%d" % self.flt_no[key], "tail": t, **l})
            self.expo.append((d, t, base, cyc, sta, fh))
            tmin = float(wx[base]["tmin"][idx])
            # the flap actuator campaign, 2023 to mid-2024: one at a time when a spare is in stores
            if self.fla_campaign and self.fla_campaign[0][0] <= d and self.fla_campaign[0][1] == t and self.pool["FLA"]:
                _, _, pos = self.fla_campaign.pop(0)
                if not self.units[self.install[(t, "FLA", pos)]]["fla_mod"]:
                    self.remove(d, base, t, "FLA", pos, "SB", reason="SCHED")
            for p in P.PARTS:
                k = p["k"]
                e = eta(p)
                inc = exposure_inc(p, cyc, sta, fh)
                cm = cold_mult(p, tmin, d.month)
                for pos in pos_names(k):
                    sn = self.install[(t, k, pos)]
                    if sn is None:
                        continue
                    u = self.units[sn]
                    rk = p["rogue"][2]
                    mult = cm * (p["rogue"][1] if (u["rogue"] and rk == "cf") else 1.0) * (p.get("sb", 1.0) if u["mod"] else 1.0)
                    a0 = u["age"]
                    a1 = a0 + inc
                    dH = ((a1 / e) ** p["beta"] - (a0 / e) ** p["beta"]) * mult
                    u["age"] = a1
                    u["tsn"] += fh
                    u["csn"] += cyc
                    lam_nff = inc * p["rate"] / 1000.0 * p["own_nff"] / (1 - p["own_nff"]) * P.BASES[base]["nff_mult"] * \
                        (cm if p["cold"] > 0 else 1.0)
                    if u["rogue"] and rk == "nff":
                        lam_nff += u.get("rogue_rate", p["rogue"][1]) / 330.0
                    pr = self.prng[k]
                    x = pr.random()
                    pcf = 1 - math.exp(-dH)
                    if x < pcf:
                        ber = 0.0 if u["rogue"] else p["ber"]
                        self.remove(d, base, t, k, pos, "BER" if pr.random() < ber else "CF")
                    elif x < pcf + lam_nff:
                        self.remove(d, base, t, k, pos, "NFF")
            for f in self.faults:
                if f["tail"] != t or f["fixed"] is not None or f["onset"] > d:
                    continue
                fr = f["rng"]
                if fr.random() < f["sym"]:
                    bp = P.BASES[base]
                    if fr.random() < bp["swap"]:
                        if self.install.get((t, f["k"], f["pos"])):
                            f["swaps"] += 1
                            self.remove(d, base, t, f["k"], f["pos"], "NFF")
                        if fr.random() < 0.06:
                            f["fixed"], f["how"] = d, "line"
                    elif fr.random() < bp["find"]:
                        f["fixed"], f["how"] = d, "line"


# ----------------------------------------------------------------------------------------------- history and 2027

def movers_of(hist):
    """From 1 April 2027: four Trondheim and four Bergen aircraft to Bodø for the Helgeland package, the fifth
    Trondheim aircraft to Tromsø."""
    at = {t: base_on(hist, t, P.ASOF) for t in hist}
    trd = sorted(t for t in at if at[t] == "TRD")
    bgo = sorted(t for t in at if at[t] == "BGO")
    mv = {t: "HEL" for t in trd[:4] + bgo[:4]}
    for t in trd[4:]:
        mv[t] = "TOS"
    return mv


def history(seed=P.SEED):
    w = type("World", (), {})()
    w.dates, w.wx, w.snaps = weather(np.random.default_rng(seed + 1), P.D0, dt.date(2027, 12, 31))
    w.idx = {d: i for i, d in enumerate(w.dates)}
    w.ac, w.hist, w.checks = fleet(np.random.default_rng(seed + 2))
    E = Engine(seed + 9)
    E.setup(w.ac, w.hist, w.checks)
    # the flap actuator campaign: every installed unit, spread from March 2023
    crng = np.random.default_rng(seed + 10)
    order = [(t, pos) for t in E.tails for pos in pos_names("FLA")]
    crng.shuffle(order)
    start = dt.date(2023, 3, 6)
    E.fla_campaign = [(start + dt.timedelta(days=int(5.5 * i)), t, pos) for i, (t, pos) in enumerate(order)]
    d = P.D0
    while d <= P.ASOF:
        E.day(d, w.wx, w.idx[d])
        d += DAY
    w.E = E
    w.movers = movers_of(w.hist)
    w.rogue_true = {sn for sn, u in E.units.items() if u["rogue"]}
    return w


def replay_2027(w, reps, seed=777):
    """The 2027 programme replayed from the end of November 2026: December 2026 on the November networks, then
    2027 with the movers at Bodø from 1 April; each replication its own weather and its own draws."""
    out = []
    big = ("legs", "changes", "shop_jobs", "vendor_jobs", "roster", "expo", "demand", "backs", "purchases")
    keep = {b: getattr(w.E, b) for b in big}
    for b in big:
        setattr(w.E, b, [] if b not in ("demand", "backs") else {k: [] for k in P.PART})
    base = copy.deepcopy(w.E)
    for b in big:
        setattr(w.E, b, keep[b])
    for rep in range(reps):
        E = copy.deepcopy(base)
        E.reseed(seed + 1000 * rep)
        frng = np.random.default_rng(seed + 1000 * rep + 7)
        E.faults = [f for f in E.faults if f["onset"] <= P.ASOF]
        years = ((P.Y27[1] - P.ASOF).days) / 365.25
        for p in P.PARTS:
            if p["fault"] <= 0:
                continue
            for t in E.tails:
                for _ in range(int(frng.poisson(p["fault"] * years))):
                    onset = P.ASOF + dt.timedelta(days=int(frng.integers(1, int(years * 365))))
                    pos = pos_names(p["k"])[int(frng.integers(0, p["pos"]))]
                    E.faults.append({"id": 10000 + len(E.faults), "tail": t, "k": p["k"], "pos": pos, "onset": onset,
                                     "sym": float(frng.uniform(0.07, 0.16)), "fixed": None, "how": None, "swaps": 0,
                                     "rng": np.random.default_rng(int(frng.integers(0, 2 ** 31)))})
        E.record = False
        E.demand = {k: [] for k in P.PART}
        E.backs = {k: [] for k in P.PART}
        E.expo = []
        dates, wx, _ = weather(np.random.default_rng(seed + 1000 * rep + 1), dt.date(2026, 12, 1), dt.date(2027, 12, 31))
        idx = {d: i for i, d in enumerate(dates)}
        d = dt.date(2026, 12, 1)
        while d <= P.Y27[1]:
            E.day(d, wx, idx[d], movers=w.movers)
            d += DAY
        out.append({"demand": E.demand, "backs": E.backs, "expo": E.expo, "faults": E.faults})
    return out


TEXTS = {
    "SG": {"cf": ["Armature shaft bearing rough, brush wear beyond limit; bearing and brushes replaced",
                  "Brushes worn below minimum length; replaced, commutator skimmed",
                  "Commutator scored, field winding insulation low; rewound, tested",
                  "Drive shaft shear section failed; replaced, tested"],
           "nff": ["No fault found; output and starting torque within limits", "No fault found, tested serviceable"],
           "ber": ["Armature burnt, housing cracked; beyond economic repair"]},
    "BRK": {"cf": ["Piston seal leak; seals replaced", "Brake dragging, piston housing scored; housing replaced",
                   "Heat sink rotor cracked; replaced"],
            "nff": ["No leak at test pressure; serviceable"], "ber": ["Torque tube cracked; beyond economic repair"]},
    "BAV": {"cf": ["Butterfly shaft seized, actuator diaphragm torn; overhauled", "Solenoid open circuit; replaced",
                   "Valve slow to close, piston ring worn; replaced"],
            "nff": ["No fault found, cycle time within limits"], "ber": ["Body corroded through; beyond economic repair"]},
    "NWS": {"cf": ["Rack seal leak; resealed", "Servo valve sticking; replaced", "Feedback transducer out of limits; replaced"],
            "nff": ["No fault found on rig test"], "ber": ["Housing cracked; beyond economic repair"]},
    "BAT": {"cf": ["Capacity below 85 per cent; cells replaced and reconditioned", "Cell imbalance, two cells reversed; replaced",
                   "Electrolyte leak, cell case cracked; replaced"],
            "nff": ["Capacity 102 per cent on test; serviceable"], "ber": ["Seven cells below limit; scrapped"]},
    "CPC": {"cf": ["Outflow logic card failed; replaced", "Pressure transducer drift; replaced", "Power supply failed; repaired"],
            "nff": ["No fault found, all modes tested"], "ber": ["Chassis damage; beyond economic repair"]},
    "FLA": {"cf": ["Ballscrew backlash out of limits; overhauled", "Seal leak, gearbox; repaired"],
            "nff": ["No fault found"], "ber": ["Ballscrew damaged; beyond economic repair"]},
    "ADC": {"cf": ["Static pressure module failed; replaced", "Power supply module failed; replaced", "ARINC output card failed; replaced"],
            "nff": ["No fault found, ATP passed", "No fault found; unit tested to CMM ATP, serviceable"],
            "ber": ["Water ingress, multiple modules; beyond economic repair"]},
    "WXR": {"cf": ["Magnetron output low; replaced", "Receiver module failed; replaced", "Modulator failed; repaired"],
            "nff": ["No fault found, ATP passed", "No fault found; output power and sensitivity in limits"],
            "ber": ["Magnetron and modulator failed; beyond economic repair"]},
    "VHF": {"cf": ["Receiver sensitivity low, RF module replaced", "Synthesiser failed; replaced"],
            "nff": ["No fault found, ATP passed", "No fault found; transmit and receive in limits"],
            "ber": ["Burnt PA stage; beyond economic repair"]},
    "PEC": {"cf": ["Channel A processor failed; replaced", "Speed sensor input board failed; repaired",
                   "Power supply board failed; replaced"],
            "nff": ["No fault found, ATP passed"], "ber": ["Corrosion damage; beyond economic repair"]},
    "PDT": {"cf": ["Timer relay contacts burnt; replaced", "Sequencer board failed; replaced"],
            "nff": ["No fault found"], "ber": ["Case damaged; beyond economic repair"]},
    "HYP": {"cf": ["Case drain flow high, wear; overhauled", "Shaft seal leak; replaced"],
            "nff": ["No fault found on test stand"], "ber": ["Pump body cracked; beyond economic repair"]},
    "FBP": {"cf": ["Motor winding failed; replaced", "Low output pressure, impeller worn; overhauled"],
            "nff": ["No fault found"], "ber": ["Motor burnt; beyond economic repair"]},
    "WHC": {"cf": ["Sensor input circuit failed; repaired", "Power stage failed; replaced"],
            "nff": ["No fault found", "No fault found, ATP passed"], "ber": ["Board damage; beyond economic repair"]},
    "FDU": {"cf": ["Loop monitoring circuit failed; replaced", "Power supply failed; replaced"],
            "nff": ["No fault found, ATP passed", "No fault found, loop simulation in limits"],
            "ber": ["Board burnt; beyond economic repair"]},
}

DEFECTS = {
    "SG": ["GEN {} caution light, generator tripped off line", "DC GEN {} caution, would not reset",
           "Slow start ENG {}, starter dropped out late", "GEN {} output fluctuating"],
    "BRK": ["Brake {} dragging on taxi", "Hydraulic leak at brake {}", "Brake {} binding, wear pin uneven"],
    "BAV": ["BLEED {} HOT caution", "Bleed valve {} fails to close on test", "BLEED {} caution in descent"],
    "NWS": ["NOSE STEERING caution on taxi", "Steering shimmy at slow taxi", "Steering not centring"],
    "BAT": ["MAIN BATT HOT caution", "Battery voltage low on start", "BATT caution, failed capacity check on aircraft"],
    "CPC": ["CABIN PRESS FAULT light", "Cabin altitude fluctuating in cruise", "AUTO PRESS fault, manual used"],
    "FLA": ["FLAP DRIVE caution", "Flap asymmetry indication {}"],
    "ADC": ["ADC {} FAIL flag", "Airspeed disagree caution", "ALT disagree between sides"],
    "WXR": ["Radar display blank, FAULT annunciated", "Weather radar intermittent picture", "RADAR FAIL on power up"],
    "VHF": ["VHF {} intermittent receive", "VHF {} weak transmission reported by ATC", "VHF {} no transmit"],
    "PEC": ["PEC {} FAULT caution", "Propeller {} speed fluctuation", "PEC {} caution on run-up"],
    "PDT": ["PROP DEICE caution", "De-ice timer fail light", "Prop de-ice cycling irregular"],
    "HYP": ["HYD {} pressure low", "No {} hydraulic pump low pressure caution"],
    "FBP": ["FUEL PRESS {} caution", "Boost pump {} low pressure light"],
    "WHC": ["WSHLD HOT {} caution", "Windshield heat {} inoperative", "WSHLD HEAT {} fault light"],
    "FDU": ["ENG FIRE warning, no fire", "FIRE DET FAULT", "Fire detection loop fault on test"],
}

OTHER = ["Main wheel build, tyre change", "Nose wheel build", "Oxygen bottle recharge and test",
         "Fire bottle weigh and test", "Tyre change, main wheel", "Wheel bearing inspection", "Life jacket inspection",
         "Emergency locator battery replacement", "Seat belt and harness inspection", "Crew oxygen mask test"]
