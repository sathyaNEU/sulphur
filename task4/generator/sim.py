"""The clean truth of the Saarnela world: the process that makes every file.

Kotikaari Oy's customers order on the web and its showrooms order replenishment; the WMS releases each working day's
pick pool at 06:00 and 10:00 (the stores' wave at 11:00); the site staffs each zone's day shift from the pool it sees
at its own planning rate, opens an evening shift for a week when its plan says the day cannot clear the week, and
since the 2023 safety review never puts more pickers on a small-parts zone's floor than the zone's limit. Every line
takes the task time its handling class and units give, plus the time pickers lose to each other in the aisles, which
grows with the pickers logged in per aisle. The client's planners issue a year-ahead budget each October, keyed to the
week numbers of the last full year they hold, and a rolling forecast every month. Huippu Sport, bought in 2025, ships
from another provider's warehouse; a pilot of its fastest polybag articles ran in P2 in weeks 37 to 44 of 2026 and the
whole brand moves in from March 2027."""
import datetime as dt
import math

import numpy as np

import cal
import params as P

KC = len(P.CLASSES)


def delta(d):
    """Minutes a line pickers lose to each other in the aisles at d pickers logged in an aisle."""
    x = np.maximum(0.0, np.asarray(d, float) - P.CONG_KNOT)
    return P.CONG_GAMMA * x ** P.CONG_POW


# ----------------------------------------------------------------------------------------------------- demand
def _season_k(doy, bulky=False):
    if bulky:
        s = 0.10 * np.cos(2 * np.pi * (doy - 300) / 365.25) + 0.07 * np.cos(4 * np.pi * (doy - 110) / 365.25)
    else:
        s = 0.11 * np.cos(2 * np.pi * (doy - 330) / 365.25) + 0.045 * np.cos(4 * np.pi * (doy - 25) / 365.25)
    summer = 1.0 - 0.10 * np.exp(-((doy - 200) / 18.0) ** 2)
    return np.exp(s) * summer


def _season_h(doy, bulky=False):
    if bulky:
        s = 0.16 * np.cos(2 * np.pi * (doy - 345) / 365.25) + 0.05 * np.cos(4 * np.pi * (doy - 120) / 365.25)
    else:
        s = 0.09 * np.cos(2 * np.pi * (doy - 318) / 365.25) + 0.07 * np.cos(4 * np.pi * (doy - 105) / 365.25)
    summer = 1.0 - 0.07 * np.exp(-((doy - 205) / 16.0) ** 2)
    return np.exp(s) * summer


DOW_K = (1.12, 1.04, 1.00, 0.97, 0.92, 0.85, 1.08)
DOW_H = (1.10, 1.03, 1.00, 0.98, 0.93, 0.86, 1.10)


def _events(y, rng, brand):
    """Date-anchored multipliers on the web orders of one year (each year's sizes jittered)."""
    j = lambda: float(np.exp(rng.normal(0.0, 0.05)))  # noqa: E731
    e = {}

    def put(d, m):
        e[d] = max(e.get(d, 1.0), m)

    bf = cal.black_friday(y)
    if brand == "K":
        for k in range(14):
            put(dt.date(y, 1, 1) + dt.timedelta(days=k), 1.0 + 0.36 * j() * math.exp(-k / 5.0))
        m1 = dt.date(y, 3, 1)
        thu = m1 + dt.timedelta(days=(3 - m1.weekday()) % 7 + 7)
        for k, m in enumerate((1.25, 1.22, 1.15, 1.10)):
            put(thu + dt.timedelta(days=k), 1.0 + (m - 1.0) * j())
        mon41 = dt.date.fromisocalendar(y, 41, 1)
        for k, m in enumerate((1.10, 1.12, 1.18, 1.32, 1.22, 1.12, 1.08)):
            put(mon41 + dt.timedelta(days=k), 1.0 + (m - 1.0) * j())
        put(dt.date(y, 11, 11), 1.0 + 0.30 * j())
        bw = P.BW_K
        after = P.BF_K
        dec_top, dec_lo = 1.90, 1.22
    else:
        for k in range(10):
            put(dt.date(y, 1, 2) + dt.timedelta(days=k), 1.0 + 0.22 * j() * math.exp(-k / 4.0))
        m1 = dt.date(y, 3, 1)
        wed = m1 + dt.timedelta(days=(2 - m1.weekday()) % 7 + 7)
        for k, m in enumerate((1.30, 1.38, 1.34, 1.22, 1.12)):
            put(wed + dt.timedelta(days=k), 1.0 + (m - 1.0) * j())
        mon40 = dt.date.fromisocalendar(y, 40, 1)
        for k, m in enumerate((1.08, 1.10, 1.14, 1.20, 1.12, 1.06, 1.04)):
            put(mon40 + dt.timedelta(days=k), 1.0 + (m - 1.0) * j())
        bw = (1.26, 1.30, 1.36, 1.45)
        after = (2.55, 1.85, 1.70, 1.90, 1.35, 1.18, 1.08)
        dec_top, dec_lo = 1.62, 1.20
    for k, m in enumerate(bw):
        put(bf - dt.timedelta(days=4 - k), 1.0 + (m - 1.0) * j())
    for k, m in enumerate(after):
        put(bf + dt.timedelta(days=k), 1.0 + (m - 1.0) * j())
    top = dec_top * j()
    centre = 15.0 + float(rng.normal(0.0, 0.6))
    for dd in range(1, 23):
        put(dt.date(y, 12, dd), dec_lo + (top - dec_lo) * math.exp(-((dd - centre) / 6.5) ** 2))
    tail = {23: 0.70, 24: 0.18, 25: 0.15, 26: 0.42, 27: 1.30, 28: 1.28, 29: 1.24, 30: 1.18, 31: 0.85}
    for dd, m in tail.items():
        e[dt.date(y, 12, dd)] = m
    for dd in range(18, 27):
        d = dt.date(y, 6, dd)
        e[d] = min(e.get(d, 1.0), 0.86)
    return e


def _levels(days, anchors):
    """Daily level from yearly levels {year: lines a day}: each year's level holds through the year and the step
    from one year to the next is spread over the four weeks either side of New Year."""
    ys = sorted(anchors)
    out = np.empty(len(days))
    for i, d in enumerate(days):
        y = min(max(d.year, ys[0]), ys[-1])
        lv = math.log(anchors[y])
        jan1 = dt.date(d.year, 1, 1)
        nxt = dt.date(d.year + 1, 1, 1)
        if (d - jan1).days < 28 and y - 1 in anchors:
            f = 0.5 + 0.5 * (d - jan1).days / 28.0
            lv = (1 - f) * math.log(anchors[y - 1]) + f * lv
        elif (nxt - d).days <= 28 and y + 1 in anchors:
            f = 0.5 - 0.5 * (nxt - d).days / 28.0
            lv = (1 - f) * lv + f * math.log(anchors[y + 1])
        out[i] = math.exp(lv)
    return out


def _noise(rng, n, sd_day, sd_week, rho=0.6):
    wk = np.zeros(n // 7 + 2)
    for i in range(1, len(wk)):
        wk[i] = rho * wk[i - 1] + rng.normal(0.0, sd_week)
    return np.exp(rng.normal(0.0, sd_day, n) + np.repeat(wk, 7)[:n])


def demand(rng):
    days = cal.days(P.SIM_START, P.TRUTH_END)
    n = len(days)
    doy = np.array([d.timetuple().tm_yday for d in days], float)
    dow = np.array([d.weekday() for d in days])
    r_k = {}
    for y, (gs, gb) in P.PLAN_K.items():
        r_k[y] = (P.PLAN_SLOPE * gs + rng.normal(0.0, 0.004), P.PLAN_SLOPE * gb + rng.normal(0.0, 0.004))
    anc_s, anc_b = {2020: P.VOL_K[0]}, {2020: P.VOL_K[1]}     # yearly levels, growth r_y from y - 1 to y
    for y in range(2021, 2028):
        anc_s[y] = anc_s[y - 1] * (1.0 + r_k[y][0])
        anc_b[y] = anc_b[y - 1] * (1.0 + r_k[y][1])
    lev_s, lev_b = _levels(days, anc_s), _levels(days, anc_b)
    r_h = {2024: (0.07, 0.05), 2025: (0.06, 0.04)}
    for y, (gs, gb) in P.PLAN_H.items():
        r_h[y] = (P.PLAN_SLOPE * gs + rng.normal(0.0, 0.007), P.PLAN_SLOPE * gb + rng.normal(0.0, 0.007))
    anc_hs, anc_hb = {2023: P.VOL_H[0]}, {2023: P.VOL_H[1]}
    for y in range(2024, 2028):
        anc_hs[y] = anc_hs[y - 1] * (1.0 + r_h[y][0])
        anc_hb[y] = anc_hb[y - 1] * (1.0 + r_h[y][1])
    lev_hs, lev_hb = _levels(days, anc_hs), _levels(days, anc_hb)

    ev_k, ev_h = {}, {}
    for y in range(P.SIM_START.year, P.TRUTH_END.year + 1):
        ev_k.update(_events(y, rng, "K"))
        ev_h.update(_events(y, rng, "H"))
    e_k = np.array([ev_k.get(d, 1.0) for d in days])
    e_h = np.array([ev_h.get(d, 1.0) for d in days])
    e_kb = 1.0 + 0.62 * (e_k - 1.0)
    e_hb = 1.0 + 0.55 * (e_h - 1.0)
    dk = np.array([DOW_K[i] for i in dow])
    dh = np.array([DOW_H[i] for i in dow])
    web_s = lev_s * _season_k(doy) * e_k * dk * _noise(rng, n, 0.045, 0.020)
    web_b = lev_b * _season_k(doy, True) * e_kb * dk * _noise(rng, n, 0.05, 0.012)
    h_s = lev_hs * _season_h(doy) * e_h * dh * _noise(rng, n, 0.05, 0.022)
    h_b = lev_hb * _season_h(doy, True) * e_hb * dh * _noise(rng, n, 0.06, 0.015)
    st_season = (1.0 + 0.34 * np.exp(-((doy - 316) / 11.0) ** 2) - 0.15 * np.exp(-((doy - 333) / 5.0) ** 2)
                 + 0.12 * np.exp(-((doy - 346) / 6.0) ** 2) - 0.12 * np.exp(-((doy - 200) / 16.0) ** 2))
    store_s = 0.135 * lev_s * st_season * np.exp(rng.normal(0.0, 0.08, n))
    store_b = 0.10 * lev_b * st_season * np.exp(rng.normal(0.0, 0.06, n))
    promo = np.clip((e_k - 1.0) / 1.6, 0.0, 1.0)
    promo_h = np.clip((e_h - 1.0) / 1.5, 0.0, 1.0)
    return {"days": days, "index": {d: i for i, d in enumerate(days)}, "web_s": np.round(web_s),
            "web_b": np.round(web_b), "store_s": np.round(store_s), "store_b": np.round(store_b),
            "h_s": np.round(h_s), "h_b": np.round(h_b), "promo": promo, "promo_h": promo_h, "r_k": r_k, "r_h": r_h,
            "e_k": e_k, "e_h": e_h}


# ----------------------------------------------------------------------------------------------------- mixes
MIX_WEB = {"P1": ((0.18, 0.37, 0.30, 0.05, 0.10), (0.40, 0.42, 0.13, 0.01, 0.04)),
           "P2": ((0.50, 0.33, 0.11, 0.04, 0.02), (0.78, 0.19, 0.02, 0.005, 0.005))}
MIX_STORE = {"P1": (0.08, 0.36, 0.38, 0.08, 0.10), "P2": (0.30, 0.44, 0.20, 0.04, 0.02)}
UPL_WEB, UPL_PROMO = 1.27, 1.06
UPL_STORE = {"P1": 5.4, "P2": 4.8}


def web_mix(zone, w, year):
    b, p = (np.array(x) for x in MIX_WEB[zone])
    m = (1.0 - w) * b + w * p
    if zone == "P2" and year >= 2024:           # the textiles range launched in 2024 sits in P2
        m = m + np.array([0.03, -0.02, -0.01, 0.0, 0.0])
    return m / m.sum()


def p1_share(w, year):
    return 0.50 - 0.05 * w - (0.012 if year >= 2024 else 0.0)


# ----------------------------------------------------------------------------------------------------- Huippu
H_GROUPS = [
    # name, class, articles, zone 2027, units a line, seasonal amplitude (winter +), spring weight
    ("Paidat ja t-paidat", "A", 700, "P2", 1.24, 0.00, 0.10),
    ("Housut ja trikoot", "A", 520, "P2", 1.18, 0.02, 0.08),
    ("Sukat ja alusvaatteet", "A", 300, "P2", 1.85, 0.06, 0.00),
    ("Takit", "C", 380, "P2", 1.04, 0.42, -0.10),
    ("Pipot, käsineet ja huivit", "A", 260, "P2", 1.30, 0.70, -0.30),
    ("Juoksukengät", "C", 420, "P1", 1.05, -0.10, 0.35),
    ("Talvikengät ja saappaat", "D", 240, "P1", 1.03, 0.80, -0.40),
    ("Sandaalit", "B", 110, "P1", 1.08, -0.60, 0.40),
    ("Laukut ja reput", "C", 180, "P1", 1.04, 0.10, 0.05),
    ("Juomapullot ja pienvarusteet", "B", 260, "P1", 1.55, 0.00, 0.15),
    ("Kypärät ja suojat", "D", 120, "P1", 1.04, 0.20, 0.10),
    ("Lasit ja kellot", "F", 90, "P1", 1.03, 0.05, 0.10),
    ("Pallot ja välineet", "C", 160, "P1", 1.15, -0.05, 0.10),
    ("Sukset ja sauvat", "D", 140, "B1", 1.02, 1.20, -0.50),
    ("Pyöräily", "D", 90, "B1", 1.03, -0.40, 0.45),
    ("Kuntoilulaitteet", "D", 80, "B1", 1.05, 0.30, 0.05),
]


def h_group_season(month):
    """Each group's relative pull by month: a winter term peaking in December, a spring term peaking in April."""
    w = math.cos(2 * math.pi * (month - 12) / 12.0)
    s = math.cos(2 * math.pi * (month - 4) / 12.0)
    return np.array([math.exp(g[5] * 0.5 * w + g[6] * s) for g in H_GROUPS])


def catalogue(rng):
    arts = []
    no = 118400
    for gi, g in enumerate(H_GROUPS):
        for k in range(g[2]):
            no += int(rng.integers(1, 9))
            vel = float(np.exp(rng.normal(0.0, 1.05)))
            arts.append({"article": "HS%06d" % no, "group": gi, "cls": g[1], "zone27": g[3], "vel": vel,
                         "upl": max(1.0, g[4] + rng.normal(0.0, 0.08))})
    return arts


def pilot_articles(arts):
    a = [x for x in arts if x["cls"] == "A" and H_GROUPS[x["group"]][3] == "P2"]
    sep = h_group_season(9)
    a.sort(key=lambda x: -x["vel"] * sep[x["group"]])
    return [x["article"] for x in a[:280]]


def huippu_mix(arts, month, small=True, zone=None):
    """The class shares and units a line of Huippu's lines in a month (expected, by velocity and season)."""
    s = h_group_season(month)
    tot = np.zeros(KC)
    units = 0.0
    for x in arts:
        z = H_GROUPS[x["group"]][3]
        if small and z == "B1":
            continue
        if zone and z != zone:
            continue
        w = x["vel"] * s[x["group"]]
        tot[P.CLASSES.index(x["cls"])] += w
        units += w * x["upl"]
    return tot / tot.sum(), units / tot.sum()


# ----------------------------------------------------------------------------------------------------- picking
SITE_RATE = {"P1": (0.97, 0.93), "P2": (0.80, 0.77), "B1": (2.55, 2.50)}   # the site's planning rate, off-peak and peak


class Pool:
    """Lines waiting to be picked in one zone: counts by class and the extra units they carry."""

    def __init__(self):
        self.c = np.zeros(KC, np.int64)
        self.x = 0.0

    def n(self):
        return int(self.c.sum())

    def add(self, counts, extra):
        self.c += counts
        self.x += extra

    def mean_t(self, zone, dl, brand=0.0):
        n = self.n()
        if n == 0:
            return 1.0
        sh = self.c / n
        if zone == "B1":
            return P.BULKY_BASE + P.BULKY_PER_UNIT * self.x / n
        return float(sh @ np.array([P.BASE[k] for k in P.CLASSES]) + P.PER_UNIT * self.x / n
                     + P.ZONE_EXTRA[zone] + dl + brand)

    def take(self, k, rng):
        n = self.n()
        k = min(int(k), n)
        if k <= 0:
            return np.zeros(KC, np.int64), 0.0
        if k == n:
            got, ex = self.c.copy(), self.x
        else:
            got = rng.multivariate_hypergeometric(self.c, k)
            ex = self.x * k / n
        self.c -= got
        self.x -= ex
        return got, ex


def draw_lines(rng, n, mix, upl):
    n = int(max(0, n))
    if n == 0:
        return np.zeros(KC, np.int64), 0.0
    c = rng.multinomial(n, mix)
    extra = float(rng.gamma(4.0, max(1e-6, (upl - 1.0) * n) / 4.0)) if upl > 1.0 else 0.0
    return c, extra


def task_minutes(zone, counts, extra, dl, n_h, rng, shock):
    if zone == "B1":
        base = P.BULKY_BASE * counts.sum() + P.BULKY_PER_UNIT * extra
    else:
        base = float(counts @ np.array([P.BASE[k] for k in P.CLASSES])) + P.PER_UNIT * extra \
               + (P.ZONE_EXTRA[zone] + dl) * counts.sum() + P.BRAND_EXTRA * n_h
    return base * shock


def release_day(d):
    """The WMS releases the web orders it received on a day at 06:00 on the next working day."""
    return cal.next_working(d + dt.timedelta(days=1))


def releases(D, Hsub=None):
    """Web lines released to picking on each working day (the showrooms' replenishment is released on its own day)."""
    out = {}
    for i, d in enumerate(D["days"]):
        if d < dt.date(2021, 12, 20):
            continue
        for p, share in ((release_day(d), 1.0),):
            r = out.setdefault(p, {"web_s": 0.0, "web_b": 0.0, "h_s": 0.0, "h_b": 0.0, "pw": 0.0, "ph": 0.0})
            r["web_s"] += share * D["web_s"][i]
            r["web_b"] += share * D["web_b"][i]
            r["h_s"] += share * D["h_s"][i]
            r["h_b"] += share * D["h_b"][i]
            r["pw"] += share * D["web_s"][i] * D["promo"][i]
            r["ph"] += share * D["h_s"][i] * D["promo_h"][i]
    for p, r in out.items():
        r["promo"] = r["pw"] / max(1.0, r["web_s"])
        r["promo_h"] = r["ph"] / max(1.0, r["h_s"])
    return out


# ----------------------------------------------------------------------------------------------------- people
def own_staff(rng):
    """Telkkä's own pickers by home zone, with start and end dates (hires as volumes grew, a few leavers)."""
    plan = {"P1": [(dt.date(2019, 3, 1), 10), (dt.date(2023, 2, 6), 1), (dt.date(2024, 3, 4), 2), (dt.date(2025, 8, 18), 1)],
            "P2": [(dt.date(2019, 3, 1), 8), (dt.date(2023, 8, 14), 1), (dt.date(2024, 2, 5), 1), (dt.date(2025, 3, 3), 1)],
            "B1": [(dt.date(2019, 3, 1), 4), (dt.date(2024, 9, 2), 1)]}
    staff = []
    no = 104100
    for z, waves in plan.items():
        for start, k in waves:
            for _ in range(k):
                no += int(rng.integers(3, 29))
                s0 = start - dt.timedelta(days=int(rng.integers(0, 900))) if start.year == 2019 else start
                staff.append({"emp": no, "zone": z, "start": s0, "end": None})
    # three leavers replaced in the same zone
    for z, (leave, rep) in {"P1": (dt.date(2023, 5, 31), dt.date(2023, 6, 12)), "P2": (dt.date(2024, 10, 31), dt.date(2024, 11, 4)),
                            "B1": (dt.date(2025, 4, 30), dt.date(2025, 5, 19))}.items():
        cand = [x for x in staff if x["zone"] == z and x["end"] is None and x["start"] < leave]
        cand[int(rng.integers(0, len(cand)))]["end"] = leave
        no += int(rng.integers(3, 29))
        staff.append({"emp": no, "zone": z, "start": rep, "end": None})
    for x in staff:
        x["summer"] = int(rng.integers(25, 31))          # first ISO week of four weeks' summer leave
        x["winter"] = int(rng.choice([1, 2, 8, 9, 10, 52]))
        x["sick"] = float(np.exp(rng.normal(np.log(0.045), 0.35)))
    return staff


def absent(x, d, rng):
    w = cal.isoweek(d)
    if w in P.PEAK_WEEKS:
        pass
    elif x["summer"] <= w < x["summer"] + 4 or w == x["winter"]:
        return "VAC"
    winter = 1.0 + 0.45 * math.cos(2 * math.pi * (d.timetuple().tm_yday - 15) / 365.25)
    peak_extra = 1.25 if w in P.PEAK_WEEKS else 1.0
    if rng.random() < x["sick"] * winter * peak_extra:
        return "SICK"
    return None


# ----------------------------------------------------------------------------------------------------- the floor
SITE_RATE = {"P1": 1.10, "P2": 0.88, "B1": 2.55}    # the site's planning rate, task minutes a line
PER_PICKER = P.SHIFT_PAID * 60 * 0.92                # task minutes a picker's shift gives at the site's planning share


def era(d):
    return "A" if d < P.LIMIT_FROM else "B"


def day_cap(z, d):
    if z == "B1":
        return 14
    return P.LIMIT[z] if era(d) == "B" else round(2.6 * P.aisles(z, d))


def zone_share(z, r, d):
    s1 = p1_share(r["promo"], d.year)
    return s1 if z == "P1" else 1.0 - s1


def plan_week(D, rel, rng, wk, ds, eve, rate):
    """The site's evening-shift decision for a peak week. Before the 2023 safety review the evening shift ran in the
    Black Friday week only; from 2024 (planning standard issue 3) a small-parts zone opens the evening shift for a
    peak week when its planned day crew would pass 1.35 pickers an aisle, and the evening takes the rest."""
    evs = [d for d in ds if d.weekday() < 5]
    for z in P.SMALL:
        exp_min = 0.0
        for d in ds:
            r = rel.get(d)
            if r is None:
                continue
            store = D["store_s"][D["index"][d]] * (0.56 if z == "P1" else 0.44) if d.weekday() < 5 else 0.0
            exp_min += (zone_share(z, r, d) * r["web_s"] + store) * rate(z, True, d.year)
        exp_min *= float(np.exp(rng.normal(0.0, 0.05)))
        if era(ds[0]) == "A":
            bf = cal.black_friday(wk[0])
            if cal.isoweek(bf) == wk[1] and evs:
                eve[(wk, z)] = max(2, int(round(0.22 * exp_min / len(ds) / PER_PICKER)))
        else:
            cap = 1.35 * P.aisles(z, ds[0]) * len(ds) * PER_PICKER
            if exp_min > cap and evs:
                eve[(wk, z)] = int(math.ceil((exp_min - cap) / (len(evs) * PER_PICKER)))


def simulate_floor(D, rel, arts, staff, rng):
    pilot = set(pilot_articles(arts))
    sep = h_group_season(9)
    sp_w = sum(x["vel"] * sep[x["group"]] for x in arts if H_GROUPS[x["group"]][3] != "B1")
    pil = [x for x in arts if x["article"] in pilot]
    pil_w = np.array([x["vel"] * sep[x["group"]] for x in pil])
    pilot_share = float(pil_w.sum() / sp_w)
    pil_p = pil_w / pil_w.sum()
    rows, conf, shifts = [], [], []
    carry = {z: Pool() for z in P.ZONES}
    hcarry = Pool()
    work = [d for d in cal.days(dt.date(2021, 12, 27), P.DATA_END) if cal.working(d)]
    weeks = {}
    for d in work:
        weeks.setdefault((cal.isoyear(d), cal.isoweek(d)), []).append(d)
    eve = {}
    done = set()
    real = {}
    week_need = {}

    def rate(z, peak, year):
        """The site plans on the time a line its zones took in the same season of the year before."""
        k = (z, peak, year - 1)
        if k in real and real[k][1] > 0:
            return real[k][0] / real[k][1]
        return SITE_RATE[z] * (0.92 if peak else 1.0)

    for d in work:
        i = D["index"][d]
        r = rel.get(d, {"web_s": 0, "web_b": 0, "promo": 0.0, "h_s": 0.0, "promo_h": 0.0})
        peak = cal.peak(d)
        wk = (cal.isoyear(d), cal.isoweek(d))
        weekday = d.weekday() < 5
        day_shock = float(np.exp(rng.normal(0.0, 0.02)))
        in_pilot = P.PILOT[0] <= d <= P.PILOT[1]
        if wk not in done:
            done.add(wk)
            if wk[1] in P.PEAK_WEEKS:
                plan_week(D, rel, rng, wk, weeks[wk], eve, rate)
        for z in P.ZONES:
            pools = {"carry": carry[z], "web": Pool(), "store": Pool()}
            if z == "B1":
                c, x = draw_lines(rng, r["web_b"], np.array([0, 0, 0.15, 0.85, 0.0]), 1.06)
                pools["web"].add(c, x)
                if weekday:
                    c, x = draw_lines(rng, D["store_b"][i], np.array([0, 0, 0.30, 0.70, 0.0]), 2.2)
                    pools["store"].add(c, x)
            else:
                w = r["promo"]
                upl = UPL_WEB + (UPL_PROMO - UPL_WEB) * w
                c, x = draw_lines(rng, zone_share(z, r, d) * r["web_s"], web_mix(z, w, d.year), upl)
                pools["web"].add(c, x)
                if weekday:
                    c, x = draw_lines(rng, D["store_s"][i] * (0.56 if z == "P1" else 0.44), np.array(MIX_STORE[z]),
                                      UPL_STORE[z])
                    pools["store"].add(c, x)
                if z == "P2" and in_pilot:
                    hc = np.zeros(KC, np.int64)
                    hc[0] = int(round(pilot_share * r["h_s"]))
                    hcarry.add(hc, 0.0)
            own = [x for x in staff if x["zone"] == z and x["start"] <= d and (x["end"] is None or d <= x["end"])]
            present, absn = [], []
            for x in own:
                if not weekday:
                    if peak and rng.random() < 0.30:
                        present.append(x["emp"])
                    continue
                a = absent(x, d, rng)
                (absn.append((x["emp"], a)) if a else present.append(x["emp"]))
            n_pool = sum(p.n() for p in pools.values()) + (hcarry.n() if z == "P2" else 0)
            exp_min = n_pool * rate(z, peak, d.year) * float(np.exp(rng.normal(0.0, 0.025)))
            n_e = eve.get((wk, z), 0) if weekday else 0
            cap = day_cap(z, d)
            need = max(0.0, exp_min - n_e * PER_PICKER) / PER_PICKER
            n_d = int(round(need + 0.3))
            if not peak:
                wkey = (wk, z)
                if wkey not in week_need:
                    tot = 0.0
                    for dd in weeks[wk]:
                        rr = rel.get(dd)
                        if rr is None:
                            continue
                        if z == "B1":
                            tot += rr["web_b"] + (D["store_b"][D["index"][dd]] if dd.weekday() < 5 else 0.0)
                        else:
                            tot += zone_share(z, rr, dd) * rr["web_s"] + (
                                D["store_s"][D["index"][dd]] * (0.56 if z == "P1" else 0.44) if dd.weekday() < 5 else 0.0)
                    week_need[wkey] = tot * rate(z, False, d.year) / len(weeks[wk]) / PER_PICKER
                n_d = min(n_d, int(math.ceil(1.12 * week_need[wkey])))
            if peak and era(d) == "B" and z in P.SMALL and n_e:
                n_d = min(n_d, int(math.ceil(1.35 * P.aisles(z, d))) + int(rng.integers(0, 2)))
            n_d = max(2, min(cap, n_d))
            if len(present) > n_d + 1 and weekday:
                keep, pack = present[:n_d], present[n_d:]
            else:
                keep, pack = present, []
                n_d = max(n_d, len(present))
            shifts.append({"date": d, "zone": z, "n_day": n_d, "n_eve": n_e, "own": keep, "absent": absn,
                           "pack": pack})
            hours = sorted(set(P.LS_DAY) | (set(P.LS_EVE) if n_e else set()))
            for h in hours:
                nd = n_d if h in P.LS_DAY else 0
                if nd and not peak and h >= 11:
                    rem = sum(p.n() for p in pools.values()) * rate(z, peak, d.year)
                    room = 60.0 * sum(v for hh, v in P.LS_DAY.items() if hh >= h)
                    nd = min(n_d, int(math.ceil(rem / max(1.0, room))) + 1)
                n_h = nd * P.LS_DAY.get(h, 0.0) + (n_e * P.LS_EVE[h] if n_e and h in P.LS_EVE else 0.0)
                logged = n_h * 60.0 * float(np.exp(rng.normal(0.0, 0.012)))
                if logged <= 0:
                    continue
                dpa = logged / 60.0 / P.aisles(z, d)
                dl = 0.0 if z == "B1" else float(delta(dpa))
                shock = day_shock * float(np.exp(rng.normal(0.0, 0.03)))
                left = logged
                tot = np.zeros(KC, np.int64)
                ext = 0.0
                task = 0.0
                n_store = 0
                n_hl = 0
                if z == "P2" and hcarry.n() > 0:
                    t_h = P.BASE["A"] + P.PER_UNIT * 0.08 + P.BRAND_EXTRA + dl
                    m = left * min(0.35, hcarry.n() / max(1, n_pool))
                    k = min(hcarry.n(), int(m / t_h))
                    if k > 0:
                        hcarry.take(k, rng)
                        idx = rng.choice(len(pil), size=k, p=pil_p)
                        t0 = dt.datetime.combine(d, dt.time(h, 0))
                        span = 60.0 * (P.LS_DAY.get(h, 0.9) if h in P.LS_DAY else 0.9)
                        picker, clock = 0, float(rng.integers(0, 4))
                        used = 0.0
                        for j in range(k):
                            a = pil[int(idx[j])]
                            u = 1 + int(rng.poisson(max(0.0, a["upl"] - 1.0)))
                            tt = (P.BASE["A"] + P.PER_UNIT * (u - 1) + P.BRAND_EXTRA + dl) * float(rng.gamma(4.0, 0.25))
                            if clock + tt > span:
                                picker += 1
                                clock = float(rng.integers(0, 4))
                            clock += tt
                            used += tt
                            conf.append((t0 + dt.timedelta(seconds=clock * 60.0), d, h, a["article"], u, picker))
                            ext += u - 1
                        tot[0] += k
                        n_hl = k
                        task += used
                        left -= used
                order = []
                if h >= 11 and pools["store"].n() > 0:
                    order.append(("store", 0.5))
                order += [("carry", 1.0), ("web", 1.0), ("store", 1.0)]
                for name, frac in order:
                    p = pools[name]
                    if p.n() == 0 or left <= 0.5:
                        continue
                    t = p.mean_t(z, dl)
                    k = min(p.n(), int(left * frac / t))
                    if k <= 0:
                        continue
                    got, ex = p.take(k, rng)
                    tm_ = task_minutes(z, got, ex, dl, 0, rng, shock)
                    tot += got
                    ext += ex
                    task += tm_
                    left -= tm_
                    if name == "store":
                        n_store += int(got.sum())
                if task > logged:
                    task = logged * 0.997
                lines = int(tot.sum())
                acc = real.setdefault((z, peak, d.year), [0.0, 0])
                acc[0] += task
                acc[1] += lines
                rows.append((d, h, z, round(logged / 60.0, 2), round(logged, 1), round(task, 1),
                             round(max(0.0, logged - task), 1), lines, int(round(lines + ext)), *[int(v) for v in tot],
                             n_store, n_hl))
            nc = Pool()
            for name in ("carry", "web", "store"):
                nc.add(pools[name].c, pools[name].x)
            carry[z] = nc
    return rows, conf, shifts, eve, pilot, pilot_share


# ----------------------------------------------------------------------------------------------------- the planners
def weekly_orders(D, key):
    """The client's own order lines by ISO week of the order date (what its planners see)."""
    out = {}
    for i, d in enumerate(D["days"]):
        k = (cal.isoyear(d), cal.isoweek(d))
        v = D[key][i]
        if key == "web_s":
            v = v + (D["store_s"][i] if d.weekday() < 5 and cal.working(d) else 0.0)
        if key == "web_b":
            v = v + (D["store_b"][i] if d.weekday() < 5 and cal.working(d) else 0.0)
        out[k] = out.get(k, 0.0) + v
    return out


def n_weeks(y):
    return dt.date(y, 12, 28).isocalendar()[1]


def budget(wo, y, g, rng):
    """The year-ahead budget for year y issued in October of y - 1: each week number of y takes the same week number
    of y - 2 (the last full year the planners hold), brought forward by the year-to-date trend of y - 1 (weeks 1 to
    39) and grown by the commercial plan's growth g."""
    ytd = sum(wo[(y - 1, w)] for w in range(1, 40)) / sum(wo[(y - 2, w)] for w in range(1, 40)) - 1.0
    out = {}
    for w in range(1, n_weeks(y) + 1):
        b = wo.get((y - 2, w)) or wo[(y - 2, 52)]
        out[w] = b * (1.0 + ytd) * (1.0 + g) * float(np.exp(rng.normal(0.0, 0.012)))
    return out, ytd


def rolling(wo, issue, rng):
    """A rolling forecast issued on a mid-month day: the next 13 ISO weeks from the mean of the last four complete
    weeks, phased by the same week numbers a year earlier."""
    y0, w0, _ = issue.isocalendar()
    last = []
    d = issue - dt.timedelta(days=issue.weekday() + 7)
    for k in range(4):
        dd = d - dt.timedelta(days=7 * k)
        last.append((cal.isoyear(dd), cal.isoweek(dd)))
    lvl = np.mean([wo[k] for k in last])
    ref = np.mean([wo.get((y - 1, w), wo.get((y - 1, 52))) for (y, w) in last])
    out = {}
    start = issue + dt.timedelta(days=7 - issue.weekday())
    for k in range(13):
        dd = start + dt.timedelta(days=7 * k)
        key = (cal.isoyear(dd), cal.isoweek(dd))
        prev = wo.get((key[0] - 1, key[1])) or wo.get((key[0] - 1, 52))
        out[key] = lvl * prev / ref * float(np.exp(rng.normal(0.0, 0.025)))
    return out


def planners(D, rng):
    wk_s, wk_b = weekly_orders(D, "web_s"), weekly_orders(D, "web_b")
    hk_s, hk_b = weekly_orders(D, "h_s"), weekly_orders(D, "h_b")
    issues = {2022: dt.date(2021, 10, 15), 2023: dt.date(2022, 10, 14), 2024: dt.date(2023, 10, 13),
              2025: dt.date(2024, 10, 15), 2026: dt.date(2025, 10, 15), 2027: dt.date(2026, 10, 15)}
    rows = []
    meta = {}
    for y, iss in issues.items():
        gs, gb = P.PLAN_K[y]
        bs, ytd_s = budget(wk_s, y, gs, rng)
        bb, ytd_b = budget(wk_b, y, gb, rng)
        meta[(P.BRAND_K, y)] = {"issue": iss, "g": (gs, gb), "ytd": (ytd_s, ytd_b)}
        for w in bs:
            rows.append((iss, "budget %d" % y, P.BRAND_K, "small parts", y, w, bs[w]))
            rows.append((iss, "budget %d" % y, P.BRAND_K, "bulky", y, w, bb[w]))
        if y == 2024:     # the bulky rows re-issued after the furniture range review
            re = dt.date(2023, 10, 27)
            for w in bb:
                rows.append((re, "budget %d" % y, P.BRAND_K, "bulky", y, w, bb[w] * 0.97 * float(np.exp(rng.normal(0, 0.004)))))
            meta[(P.BRAND_K, y)]["reissue"] = re
    gs, gb = P.PLAN_H[2027]
    hs, hy_s = budget(hk_s, 2027, gs, rng)
    hb, hy_b = budget(hk_b, 2027, gb, rng)
    meta[(P.BRAND_H, 2027)] = {"issue": issues[2027], "g": (gs, gb), "ytd": (hy_s, hy_b)}
    for w in hs:
        rows.append((issues[2027], "budget 2027", P.BRAND_H, "small parts", 2027, w, hs[w]))
        rows.append((issues[2027], "budget 2027", P.BRAND_H, "bulky", 2027, w, hb[w]))
    m = dt.date(2021, 11, 15)
    while m <= dt.date(2026, 10, 15):
        iss = m if m.weekday() < 5 else m + dt.timedelta(days=7 - m.weekday())
        for grp, wo in (("small parts", wk_s), ("bulky", wk_b)):
            for (yy, ww), v in rolling(wo, iss, rng).items():
                rows.append((iss, "rolling %s" % iss.strftime("%Y-%m"), P.BRAND_K, grp, yy, ww, v))
        m = dt.date(m.year + (m.month == 12), m.month % 12 + 1, 15)
    return rows, meta, {"K_s": wk_s, "K_b": wk_b, "H_s": hk_s, "H_b": hk_b}


# ----------------------------------------------------------------------------------------------------- the 2027 truth
def lines_by_pickday(D, a, b):
    """Kotikaari and Huippu lines released to picking on each working day in [a, b] (the release rule)."""
    out = {}
    for i, d in enumerate(D["days"]):
        if d < a - dt.timedelta(days=10) or d > b:
            continue
        for p, sh in ((release_day(d), 1.0),):
            if not (a <= p <= b):
                continue
            r = out.setdefault(p, {"web_s": 0.0, "web_b": 0.0, "h_s": 0.0, "h_b": 0.0, "pw": 0.0})
            for k in ("web_s", "web_b", "h_s", "h_b"):
                r[k] += sh * D[k][i]
            r["pw"] += sh * D["web_s"][i] * D["promo"][i]
    for p, r in out.items():
        r["promo"] = r["pw"] / max(1.0, r["web_s"])
        i = D["index"][p]
        r["store_s"] = D["store_s"][i] if p.weekday() < 5 else 0.0
        r["store_b"] = D["store_b"][i] if p.weekday() < 5 else 0.0
    return out


def huippu_zone_split(arts, month):
    """Huippu Sport's small-parts lines in a month by 2027 zone and the class mix and units a line in each."""
    s = h_group_season(month)
    out = {}
    for z in ("P1", "P2", "B1"):
        tot = np.zeros(KC)
        u = 0.0
        for x in arts:
            if H_GROUPS[x["group"]][3] != z:
                continue
            w = x["vel"] * s[x["group"]]
            tot[P.CLASSES.index(x["cls"])] += w
            u += w * x["upl"]
        out[z] = (tot.sum(), tot / tot.sum(), u / tot.sum())
    sp = out["P1"][0] + out["P2"][0]
    return {"P1": out["P1"][0] / sp, "P2": out["P2"][0] / sp}, {z: (out[z][1], out[z][2]) for z in out}


def t_mix(zone, mix, upl, brand=0.0):
    if zone == "B1":
        return P.BULKY_BASE + P.BULKY_PER_UNIT * (upl - 1.0)
    return float(np.asarray(mix) @ np.array([P.BASE[k] for k in P.CLASSES]) + P.PER_UNIT * (upl - 1.0)
                 + P.ZONE_EXTRA[zone] + brand)


def capacity_day(zone, n, t):
    """Lines the day shifts of one day pick with n pickers on the floor at a mean uncongested time t a line."""
    return sum(n * 60.0 * ls / (t + float(delta(n * ls / P.AISLES[zone]))) for ls in P.LS_DAY.values())


def crew_for(zone, lines, t, ls_map, days, top=None):
    """Pickers on the floor a shift needs to pick lines over its days at time t a line (the congestion included),
    searched up to the zone's limit, past which the floor's throughput turns over."""
    if lines <= 0:
        return 0.0
    lo, hi = 0.0, float(top or P.LIMIT.get(zone, 40))
    for _ in range(60):
        n = (lo + hi) / 2
        cap = days * sum(n * 60.0 * ls / (t + float(delta(n * ls / P.AISLES[zone]))) for ls in ls_map.values())
        lo, hi = (n, hi) if cap < lines else (lo, n)
    return hi


def truth_2027(D, arts):
    a, b = dt.date.fromisocalendar(2027, 46, 1), dt.date.fromisocalendar(2027, 51, 7)
    rel = lines_by_pickday(D, a, b)
    hsplit, hmix = huippu_zone_split(arts, 12)
    hsplit11, hmix11 = huippu_zone_split(arts, 11)
    out = {}
    for w in P.PEAK_WEEKS:
        ds = [dt.date.fromisocalendar(2027, w, k) for k in range(1, 8)]
        wd = [d for d in ds if cal.working(d)]
        ev = [d for d in wd if d.weekday() < 5]
        acc = {z: {"lines": 0.0, "tmin": 0.0} for z in P.ZONES}
        for d in wd:
            r = rel[d]
            m = 11 if d.month == 11 else 12
            hs, hm = (hsplit11, hmix11) if m == 11 else (hsplit, hmix)
            for z in P.SMALL:
                kw = zone_share(z, r, d) * r["web_s"]
                upl = UPL_WEB + (UPL_PROMO - UPL_WEB) * r["promo"]
                ks = r["store_s"] * (0.56 if z == "P1" else 0.44)
                hl = hs[z] * r["h_s"]
                tm = kw * t_mix(z, web_mix(z, r["promo"], 2027), upl) + ks * t_mix(z, MIX_STORE[z], UPL_STORE[z]) \
                    + hl * t_mix(z, hm[z][0], hm[z][1], P.BRAND_EXTRA)
                acc[z]["lines"] += kw + ks + hl
                acc[z]["tmin"] += tm
            bl = r["web_b"] + r["store_b"] + r["h_b"]
            acc["B1"]["lines"] += bl
            acc["B1"]["tmin"] += r["web_b"] * t_mix("B1", None, 1.06) + r["store_b"] * t_mix("B1", None, 2.2) \
                + r["h_b"] * t_mix("B1", None, hmix["B1"][1])
        for z in P.ZONES:
            L = acc[z]["lines"]
            t = acc[z]["tmin"] / L
            res = {"lines": L, "t": t, "days": len(wd), "evenings": len(ev)}
            if z == "B1":
                res["hours"] = L * t / 60.0 / (sum(P.LS_DAY.values()) / P.SHIFT_PAID)
                res["evening"] = False
            else:
                cap = len(wd) * capacity_day(z, P.LIMIT[z], t)
                res["cap"] = cap
                res["evening"] = L > cap
                if L > cap:
                    n_e = crew_for(z, L - cap, t, P.LS_EVE, len(ev))
                    res["hours"] = (P.LIMIT[z] * len(wd) + n_e * len(ev)) * P.SHIFT_PAID
                else:
                    n_d = crew_for(z, L, t, P.LS_DAY, len(wd))
                    res["hours"] = n_d * len(wd) * P.SHIFT_PAID
            out[(z, w)] = res
    return out


# ----------------------------------------------------------------------------------------------------- the records
def timesheets(shifts, rng):
    """One row per person and working day: own pickers on their home zone's day shift (absences with their code),
    the agency's pickers for the rest of the day crew and for every evening shift. The agency's pickers return
    season to season in part; it re-issued its badges on 1 April 2025 (TP-numbers before, 70-numbers after)."""
    rows = []
    pool = []
    nxt = [3100]
    seen = set()
    by_day = {}
    for s in shifts:
        by_day.setdefault(s["date"], []).append(s)
    for d in sorted(by_day):
        key = (cal.isoyear(d), cal.isoweek(d) >= 44)
        need = sum(max(0, s["n_day"] - len(s["own"])) + s["n_eve"] for s in by_day[d])
        if key not in seen:
            keep = [x for x in pool if rng.random() < 0.45]
            pool[:] = keep
            seen.add(key)
        while len(pool) < need + 6:
            nxt[0] += int(rng.integers(1, 6))
            pool.append(nxt[0])
        ids = list(rng.permutation(pool)[:need]) if need else []

        def badge(i):
            return "TP-%04d" % i if d < dt.date(2025, 4, 1) else "70%06d" % (i * 7 + 1043)

        j = 0
        for s in by_day[d]:
            z = s["zone"]
            for emp in s["own"]:
                rows.append((d, str(emp), P.ORG, z, "DAY", "06:00", "14:30", 8.0, "", 0.0))
            for emp, code in s["absent"]:
                rows.append((d, str(emp), P.ORG, z, "DAY", "", "", 0.0, code, 8.0))
            for emp in s.get("pack", []):
                rows.append((d, str(emp), P.ORG, "PACK", "DAY", "06:00", "14:30", 8.0, "", 0.0))
            for _ in range(max(0, s["n_day"] - len(s["own"]))):
                rows.append((d, badge(int(ids[j])), P.AGENCY, z, "DAY", "06:00", "14:30", 8.0, "", 0.0))
                j += 1
            for _ in range(s["n_eve"]):
                rows.append((d, badge(int(ids[j])), P.AGENCY, z, "EVE", "14:30", "23:00", 8.0, "", 0.0))
                j += 1
    return rows


def huippu_daily(D, arts, rng):
    out = []
    for i, d in enumerate(D["days"]):
        if d < dt.date(2024, 1, 1) or d > dt.date(2026, 10, 31):
            continue
        for grp, key, lpo in (("small parts", "h_s", 1.62), ("bulky", "h_b", 1.08)):
            lines = int(D[key][i])
            _, upl = huippu_mix(arts, d.month, small=(grp == "small parts")) if grp == "small parts" else (None, 1.05)
            orders = int(round(lines / (lpo * float(np.exp(rng.normal(0.0, 0.03))))))
            units = int(round(lines * upl * float(np.exp(rng.normal(0.0, 0.02)))))
            out.append((d, grp, orders, lines, units))
    return out


def huippu_articles_monthly(D, arts, rng):
    out = []
    m = dt.date(2024, 11, 1)
    while m <= dt.date(2026, 10, 1):
        nm = dt.date(m.year + (m.month == 12), m.month % 12 + 1, 1)
        idx = [i for i, d in enumerate(D["days"]) if m <= d < nm]
        s = h_group_season(m.month)
        for small in (True, False):
            sel = [x for x in arts if (H_GROUPS[x["group"]][3] != "B1") == small]
            tot = int(sum(D["h_s" if small else "h_b"][i] for i in idx))
            w = np.array([x["vel"] * s[x["group"]] for x in sel])
            n = rng.multinomial(tot, w / w.sum())
            for x, k in zip(sel, n):
                if k == 0:
                    continue
                u = k + int(rng.poisson(max(0.0, (x["upl"] - 1.0) * k)))
                out.append((m.strftime("%Y-%m"), x["article"], int(k), u))
        m = nm
    return out


def world(seed=P.SEED):
    rng = np.random.default_rng(seed)
    D = demand(rng)
    rel = releases(D)
    arts = catalogue(rng)
    staff = own_staff(rng)
    rows, conf, shifts, eve, pilot, pilot_share = simulate_floor(D, rel, arts, staff, rng)
    fc, meta, wo = planners(D, rng)
    ts = timesheets(shifts, rng)
    hd = huippu_daily(D, arts, rng)
    ham = huippu_articles_monthly(D, arts, rng)
    truth = truth_2027(D, arts)
    return {"D": D, "arts": arts, "staff": staff, "zone_hours": rows, "pilot_conf": conf, "shifts": shifts,
            "eve": eve, "pilot": pilot, "pilot_share": pilot_share, "forecasts": fc, "fmeta": meta, "orders_wk": wo,
            "timesheets": ts, "h_daily": hd, "h_monthly": ham, "truth": truth, "rng": rng}
