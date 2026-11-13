"""task9 (architecture 3): the simulated fab. Varnholt Halbleiter Fab 2 makes VX40 and VP12 (and VR90-T, VR90's front-end
test vehicle) through a forty-step flow; five steps carry mechanisms, every other step is a tool choice that carries
nothing. The process runs in time order: lots start, queue and dispatch to tools around each tool's downtime; the oxide
slurry loop's flow sets each polisher's large-particle feed by its distance along the loop; the pre-gate bench's tank
takes every lot's drag-in and the controller's spikes and changes; DP2B's new showerhead and CM3's rev 8 shape the
ILD0 edge; the contact-etch chambers build polymer by RF time and recipe chemistry until their wet clean; random defects
cluster by wafer and by region. Sort probes every die and bins it on its first failing test.

Nothing here knows what any analysis will do; the pack is written from these records by pack.py."""
import datetime as dt
import math

import numpy as np

import params as P

DAY = 86400.0


def tday(t):
    """datetime -> days since the epoch"""
    return (t - P.EPOCH).total_seconds() / DAY


def dtime(d):
    return P.EPOCH + dt.timedelta(days=float(d))


# ------------------------------------------------------------------ die geometry
class Grid:
    """A product's die grid on the 300 mm wafer: every die whose four corners sit within 147 mm is printed and probed.
    The grid offset is the one the product team chose for the most die (searched on a 0.1-die lattice)."""

    def __init__(self, name):
        p = P.PRODUCTS[name]
        self.name, self.w, self.h = name, p["w"], p["h"]
        r = P.WAFER_R - P.EDGE_EXCL
        best = None
        for ox in np.arange(0, 1.0, 0.1):
            for oy in np.arange(0, 1.0, 0.1):
                cols = np.arange(-20, 21)
                X, Y = np.meshgrid((cols + ox) * self.w, (cols + oy) * self.h)
                corners = [(X, Y), (X + self.w, Y), (X, Y + self.h), (X + self.w, Y + self.h)]
                ok = np.ones_like(X, dtype=bool)
                for cx, cy in corners:
                    ok &= (cx ** 2 + cy ** 2) <= r * r
                n = int(ok.sum())
                if best is None or n > best[0]:
                    best = (n, ox, oy)
        n, ox, oy = best
        self.ox, self.oy = round(float(ox), 1), round(float(oy), 1)
        cols = np.arange(-20, 21)
        X, Y = np.meshgrid((cols + self.ox) * self.w, (cols + self.oy) * self.h)
        ok = np.ones_like(X, dtype=bool)
        rmax = np.zeros_like(X)
        for cx, cy in [(X, Y), (X + self.w, Y), (X, Y + self.h), (X + self.w, Y + self.h)]:
            rr = np.sqrt(cx ** 2 + cy ** 2)
            ok &= rr <= r
            rmax = np.maximum(rmax, rr)
        iy, ix = np.nonzero(ok)
        # map coordinates: column and row counted from the map's lower-left, as the prober steps
        self.ncol = int(ix.max() - ix.min() + 1)
        self.nrow = int(iy.max() - iy.min() + 1)
        self.col = (ix - ix.min()).astype(np.int16)
        self.row = (iy - iy.min()).astype(np.int16)
        self.x0 = X[iy, ix]               # lower-left corner (mm)
        self.y0 = Y[iy, ix]
        self.xc = self.x0 + self.w / 2
        self.yc = self.y0 + self.h / 2
        self.rc = np.sqrt(self.xc ** 2 + self.yc ** 2)
        self.rmax = np.minimum(rmax[iy, ix], r)
        self.n = len(self.col)
        self.area_cm2 = self.w * self.h / 100.0
        # 40 mm regions for the clustering field
        self.region = ((np.floor((self.xc + 160) / P.REGION_MM)).astype(int) * 16
                       + (np.floor((self.yc + 160) / P.REGION_MM)).astype(int))
        # die index lookup by (col,row) for scratch rasterising
        self.lookup = -np.ones((self.ncol, self.nrow), dtype=np.int32)
        self.lookup[self.col, self.row] = np.arange(self.n)
        self.colmin_x = X[0, ix.min()]    # x of column 0's lower-left
        self.rowmin_y = Y[iy.min(), 0]

    def die_at(self, x, y):
        """die index for points (mm), -1 where no probed die"""
        c = np.floor((x - self.colmin_x) / self.w).astype(int)
        r = np.floor((y - self.rowmin_y) / self.h).astype(int)
        ok = (c >= 0) & (c < self.ncol) & (r >= 0) & (r < self.nrow)
        out = -np.ones(len(x), dtype=np.int64)
        out[ok] = self.lookup[c[ok], r[ok]]
        return out


# ------------------------------------------------------------------ the route
# (step, tool group, mean days after the previous step, sd of the queue)
ROUTE = [
    ("LOT-START", "MES", 0.0, 0.0), ("PAD-OX", "FURN", 0.9, 0.3), ("STI-LITHO", "SCAN", 1.1, 0.4),
    ("STI-ETCH", "EA", 0.8, 0.3), ("STI-FILL", "HDP", 1.2, 0.4), ("STI-CMP", "CMC", 1.0, 0.4),
    ("WELL-IMP", "IMP", 1.3, 0.5), ("PGC", "WB", 1.4, 0.5), ("GATE-OX", "FURN", 0.25, 0.08),
    ("POLY-DEP", "FURN", 0.7, 0.3), ("POLY-LITHO", "SCAN", 1.0, 0.4), ("POLY-ETCH", "EP", 0.8, 0.3),
    ("LDD-IMP", "IMP", 1.0, 0.4), ("SPACER", "DEPS", 1.1, 0.4), ("SD-IMP", "IMP", 1.0, 0.4),
    ("RTA", "RTP", 0.6, 0.2), ("SALICIDE", "PVD", 1.2, 0.4), ("ILD0-DEP", "DP", 1.4, 0.5),
    ("ILD0-CMP", "CM", 0.7, 0.3), ("ILD0-THK", "MET", 0.15, 0.05), ("CT-LITHO", "SCAN", 0.9, 0.3),
    ("CT-ETCH", "ET", 0.8, 0.3), ("CT-FILL", "WCVD", 0.8, 0.3), ("W-CMP", "CMW", 0.8, 0.3),
    ("M1-DEP", "PVD", 1.3, 0.4), ("M1-LITHO", "SCAN", 1.0, 0.4), ("M1-ETCH", "EM", 0.9, 0.3),
    ("IMD1", "DEPS", 1.4, 0.5), ("V1-M2", "EM", 2.6, 0.8), ("IMD2", "DEPS", 1.5, 0.5),
    ("V2-M3", "EM", 2.6, 0.8), ("IMD3", "DEPS", 1.5, 0.5), ("V3-M4", "EM", 2.8, 0.9),
    ("PASSIV", "DEPS", 1.6, 0.5), ("PAD-ETCH", "EP", 1.1, 0.4), ("FAB-OUT", "MES", 1.4, 0.5),
    ("WAT", "PT", 0.9, 0.3), ("SORT", "PRB", 2.2, 0.8),
]
STEP_IDX = {s[0]: i for i, s in enumerate(ROUTE)}
TOOLS = {"FURN": ["FN-02", "FN-03", "FN-05", "FN-06"], "SCAN": ["SC-1", "SC-2", "SC-3"], "EA": ["EA-1", "EA-2"],
         "HDP": ["HD-1", "HD-2"], "CMC": ["CC-1", "CC-2"], "IMP": ["IM-1", "IM-2", "IM-3"], "WB": P.BENCHES,
         "EP": ["EP-1", "EP-2"], "DEPS": ["DS-1", "DS-2", "DS-3"], "RTP": ["RT-1", "RT-2"], "PVD": ["PV-1", "PV-2"],
         "DP": P.DEP_TOOLS, "CM": P.CMP_TOOLS, "MET": ["TH-1", "TH-2"], "ET": P.ETCH_TOOLS, "WCVD": ["WC-1", "WC-2"],
         "CMW": ["CW-1", "CW-2"], "EM": ["EM-1", "EM-2", "EM-3"], "PT": ["PT-1", "PT-2"],
         "PRB": ["PR-1", "PR-2", "PR-3", "PR-4"], "MES": ["-"]}


class Lot:
    __slots__ = ("lid", "product", "start", "n", "times", "tools", "slots", "scrap", "hold", "tv", "split", "seq")

    def __init__(self, lid, product, start, n, tv=False):
        self.lid, self.product, self.start, self.n, self.tv = lid, product, start, n, tv
        self.times, self.tools = {}, {}
        self.slots = list(range(1, n + 1))
        self.scrap = {}         # slot -> step where scrapped
        self.hold = []          # (step, hours)
        self.split = None
        self.seq = 0


class Fab:
    def __init__(self, seed=P.SEED):
        self.rng = np.random.default_rng(seed)
        self.grids = {p: Grid(p) for p in P.PRODUCTS}
        self.make_lots()
        self.make_downtime()
        self.make_loop()
        self.dispatch()
        self.make_pou()
        self.bench()
        self.etch()
        self.edge()
        self.scratches()
        self.wafers_sort()

    # -------------------------------------------------------------- lots and their step times
    def make_lots(self):
        rng = np.random.default_rng(P.SEED + 1)
        lots = []
        seqno = {"VX40": 4100, "VP12": 2230, P.TEST_VEHICLE: 310}
        prefix = {"VX40": "VXA", "VP12": "VPB", P.TEST_VEHICLE: "VRT"}
        d0, d1 = tday(P.FIRST_START), tday(P.LAST_START)
        week = 0
        while d0 + 7 * week <= d1:
            wk_start = d0 + 7 * week
            date = dtime(wk_start)
            for prod, n_week in P.STARTS_PER_WEEK.items():
                n_here = n_week + (1 if rng.random() < 0.12 else 0) - (1 if rng.random() < 0.10 else 0)
                for k in range(n_here):
                    t = wk_start + (k + rng.uniform(0.1, 0.9)) * 7.0 / n_here
                    seqno[prod] += int(rng.integers(1, 6))
                    lots.append(Lot("%s%05d" % (prefix[prod], seqno[prod]), prod, t, P.LOT))
            if date.year == 2026 and date.month in P.TV_PER_WEEK and date <= dt.datetime(2026, 9, 28):
                n_tv = P.TV_PER_WEEK[date.month]
                for k in range(n_tv):
                    t = wk_start + (k + rng.uniform(0.1, 0.9)) * 7.0 / n_tv
                    seqno[P.TEST_VEHICLE] += int(rng.integers(1, 4))
                    lots.append(Lot("%s%05d" % (prefix[P.TEST_VEHICLE], seqno[P.TEST_VEHICLE]), P.TEST_VEHICLE, t,
                                    P.LOT, tv=True))
            week += 1
        lots.sort(key=lambda L: L.start)
        for i, L in enumerate(lots):
            L.seq = i
        # step times: each step's queue and process time; holds now and then; scraps rare
        for L in lots:
            t = L.start
            last = STEP_IDX["M1-ETCH"] if L.tv else len(ROUTE) - 1
            for i, (step, grp, mu, sd) in enumerate(ROUTE[:last + 1]):
                if i:
                    t += max(0.08, rng.normal(mu, sd))
                    if rng.random() < 0.012:
                        h = float(rng.uniform(10, 70))
                        L.hold.append((step, h))
                        t += h / 24.0
                L.times[step] = t
            if rng.random() < 0.05 and not L.tv:
                bad = int(rng.integers(1, L.n + 1))
                L.scrap[bad] = str(rng.choice(["STI-CMP", "POLY-ETCH", "W-CMP", "V2-M3", "PASSIV"]))
        self.lots = lots

    # -------------------------------------------------------------- tool downtime windows (unscheduled and PM)
    def make_downtime(self):
        rng = np.random.default_rng(P.SEED + 2)
        self.down = {}
        span = (tday(P.FIRST_START), tday(P.SORT_TO))
        for grp in ("WB", "DP", "CM", "ET"):
            for tool in TOOLS[grp]:
                wins, d = [], span[0] + rng.uniform(2, 20)
                while d < span[1]:
                    dur = float(rng.uniform(4, 16)) / 24.0
                    wins.append((d, d + dur, "UNSCHED"))
                    d += float(rng.exponential(19.0)) + dur
                self.down[tool] = wins

    def is_down(self, tool, d):
        for a, b, _ in self.down.get(tool, ()):
            if a <= d < b:
                return True
        return False

    # -------------------------------------------------------------- the slurry loop
    def make_loop(self):
        """SDS-OX1: velocity by time (the VFD setpoint, the standby pump, the draw), the day tank's tote changes and its
        outlet large-particle count. Sampled every 5 minutes; each polisher's tap sees the outlet count grown over its
        residence time along the loop."""
        rng = np.random.default_rng(P.SEED + 3)
        d0, d1 = tday(P.FIRST_START) - 2, tday(P.SORT_TO) + 1
        n = int((d1 - d0) * 288) + 1
        tgrid = d0 + np.arange(n) / 288.0
        v = np.full(n, P.V_NOM)
        dn, son, soff = tday(P.T_VFD_DOWN), tday(P.T_STANDBY_ON), tday(P.T_STANDBY_OFF)
        v[(tgrid >= dn)] = P.V_LOW
        v[(tgrid >= son) & (tgrid < soff)] = P.V_STANDBY
        # the draw: more polishers running lowers the loop velocity a little; a slow wander and noise
        hours = (tgrid * 24) % 24
        v *= 1.0 - 0.025 * np.sin(2 * np.pi * (hours - 9) / 24.0)
        wander = np.cumsum(rng.normal(0, 0.0007, n))
        wander -= np.convolve(wander, np.ones(2016) / 2016, mode="same")
        v *= 1.0 + np.clip(wander, -0.015, 0.015) + rng.normal(0, 0.006, n)
        # tote changes
        totes, d = [], d0 + rng.uniform(0, 2)
        while d < d1:
            totes.append(d)
            d += float(rng.uniform(*P.TOTE_DAYS))
        totes = np.array(totes)
        idx = np.searchsorted(totes, tgrid, side="right") - 1
        age = tgrid - totes[np.maximum(idx, 0)]
        tote_lpc = P.LPC_TANK * rng.lognormal(0, 0.08, len(totes))
        lpc = tote_lpc[np.maximum(idx, 0)] * (1 + P.LPC_TANK_AGE * age) * (1 + rng.normal(0, 0.03, n))
        self.loop = dict(t=tgrid, v=v, lpc_tank=lpc, totes=totes)

    def tap_lpc(self, tool, d):
        """large-particle count at a polisher's tap at day d"""
        L = self.loop
        i = np.clip(np.searchsorted(L["t"], d), 0, len(L["t"]) - 1)
        v = L["v"][i]
        tres = P.TAP_M[tool] / v
        gain = np.where(v < P.SETTLE_V, 1.0 + P.SETTLE_GAIN * (P.SETTLE_V - v) / P.SETTLE_V, 1.0)
        return L["lpc_tank"][i] * np.exp(P.AGGLOM * tres * gain)

    # -------------------------------------------------------------- dispatch to the tools that matter
    def dispatch(self):
        rng = np.random.default_rng(P.SEED + 4)
        for L in self.lots:
            for step, (_, grp, _, _) in zip(L.times, ROUTE):
                pass
            for i, (step, grp, _, _) in enumerate(ROUTE):
                if step not in L.times:
                    continue
                d = L.times[step]
                cands = TOOLS[grp]
                if grp == "CM" and L.tv:
                    cands, w = ["CM1", "CM3"], np.array([0.5, 0.5])     # ILD0-VR is qualified on CM1 and CM3 only
                elif grp == "CM":
                    w = np.array(P.CMP_AFFINITY[L.tools["ILD0-DEP"]])
                elif grp == "ET" and L.tv:
                    cands, w = ["ET1", "ET3"], np.array([0.5, 0.5])
                else:
                    w = np.ones(len(cands)) / len(cands)
                up = np.array([0.0 if self.is_down(c, d) else 1.0 for c in cands]) if grp in ("WB", "DP", "CM", "ET") \
                    else np.ones(len(cands))
                if len(up) != len(w):
                    up = np.ones(len(w))
                if up.sum() == 0:
                    up[:] = 1.0
                w = w * up
                L.tools[step] = cands[int(rng.choice(len(cands), p=w / w.sum()))]

    # -------------------------------------------------------------- point-of-use filters on the polishers
    def make_pou(self):
        rng = np.random.default_rng(P.SEED + 5)
        self.pou = {}
        for tool in P.CMP_TOOLS:
            ch, d = [], tday(P.FIRST_START) - rng.uniform(0, 18)
            while d < tday(P.SORT_TO):
                ch.append(d)
                late = rng.random() < 0.18
                d += P.POU_DAYS + float(rng.normal(0, 1.5)) + (float(rng.uniform(4, 9)) if late else 0.0)
            self.pou[tool] = np.array(ch)

    def pou_age(self, tool, d):
        ch = self.pou[tool]
        i = np.searchsorted(ch, d, side="right") - 1
        return d - ch[max(i, 0)]

    # -------------------------------------------------------------- the pre-gate bench and its tank
    def bench(self):
        """Every lot through each bench's tank T3 (the pulled products and the fab's other lots), the controller's spikes
        every n lots and its full changes on the shift clock (06:00 and 18:00 in spring, 06:00 from 1 July), and the
        tank's metal content after each event."""
        rng = np.random.default_rng(P.SEED + 6)
        self.bench_events = {b: [] for b in P.BENCHES}
        self.bath_at = {}       # (lot id) -> ppb its wafers saw
        self.bg_lots = {b: [] for b in P.BENCHES}
        span0, span1 = tday(P.FIRST_START) - 1, tday(P.SORT_TO)
        t_chem = tday(P.T_CHEM_LIFE)

        def next_change_after(d):
            day0 = math.floor(d)
            hours = (6, 18) if d < t_chem else (6,)
            for k in range(3):
                for h in hours:
                    c = day0 + k + h / 24.0
                    if c > d + 1e-9:
                        return c
            return day0 + 1.25
        for b in P.BENCHES:
            bg, d = [], span0
            rate = P.BG_LOTS_PER_DAY[b]
            while d < span1:
                d += float(rng.exponential(1.0 / rate))
                if rng.random() < (0.82 if (dtime(d).weekday() >= 5) else 1.0):
                    bg.append((d, "BG", int(rng.choice([25, 25, 25, 24, 23, 25, 22, 13])), None))
            self.bg_lots[b] = [(e[0], e[2]) for e in bg]
            ours = [(L.times["PGC"], "OURS", L.n, L) for L in self.lots if L.tools.get("PGC") == b]
            stream = sorted(bg + ours, key=lambda e: e[0])
            c = P.C_FRESH
            since_spike = 0
            next_change = next_change_after(span0)
            ev = self.bench_events[b]
            for d, kind, n, L in stream:
                sched = P.SUMMER if d >= t_chem else P.SPRING
                while next_change <= d:
                    if self.is_down(b, next_change):
                        next_change += 0.25
                        continue
                    c_before = c
                    c = P.C_FRESH * rng.lognormal(0, 0.15)
                    ev.append(dict(d=next_change, ev="CHANGE", c_before=c_before, c_post=c))
                    since_spike = 0
                    next_change = next_change_after(next_change)
                drag = P.DRAG_PPB * n * rng.lognormal(0, 0.18)
                c_batch = c + 0.5 * drag   # the wafers see the bath as it is during their own soak
                c += drag
                if kind == "OURS":
                    self.bath_at[L.lid] = c_batch
                ev.append(dict(d=d, ev="BATCH", lot=(L.lid if L else None), n=n, c=c_batch, c_post=c, kind=kind))
                since_spike += 1
                if since_spike >= sched["spike_lots"]:
                    f = P.SPIKE_L / P.BATH_L
                    c = c * (1 - f) + P.C_FRESH * f
                    since_spike = 0
                    ev.append(dict(d=d + 0.004, ev="SPIKE", c_post=c))
            self.bench_events[b] = sorted(ev, key=lambda e: e["d"])

    def bath_state(self, bench, d):
        """the tank's metal content at time d (the state after the last event before it)"""
        ev = self.bench_events[bench]
        if not hasattr(self, "_bench_t"):
            self._bench_t = {b: np.array([e["d"] for e in self.bench_events[b]]) for b in P.BENCHES}
        i = int(np.searchsorted(self._bench_t[bench], d, side="right")) - 1
        return P.C_FRESH if i < 0 else ev[i]["c_post"]

    # -------------------------------------------------------------- contact etch: polymer, cleans, particles
    def etch(self):
        rng = np.random.default_rng(P.SEED + 7)
        self.etch_wafers = {ch: [] for ch in P.ETCH_CHAMBERS}
        self.etch_cleans = {ch: [] for ch in P.ETCH_CHAMBERS}
        self.monitors = []
        span0, span1 = tday(P.FIRST_START) - 1, tday(P.SORT_TO)
        ours = {ch: [] for ch in P.ETCH_CHAMBERS}
        for L in self.lots:
            if "CT-ETCH" not in L.times:
                continue
            tool = L.tools["CT-ETCH"]
            d = L.times["CT-ETCH"]
            recipe = "CT-DEEP-07" if L.tv else P.PRODUCTS[L.product]["recipe"]
            rf = P.PRODUCTS["VR90"]["rf_s"] if L.tv else P.PRODUCTS[L.product]["rf_s"]
            for k, slot in enumerate(L.slots):
                if L.tv:
                    ch = "ET1B" if tool == "ET1" else "ET3A"
                else:
                    ch = tool + ("A" if slot % 2 == 1 else "B")
                    if self.is_down(ch, d):
                        ch = tool + ("B" if ch.endswith("A") else "A")
                ours[ch].append((d + k * 0.0021, L.lid, slot, recipe, rf * rng.normal(1, 0.012)))
        for ch in P.ETCH_CHAMBERS:
            n_ours_week = len(ours[ch]) / ((span1 - span0) / 7.0)
            bg_rate = max(P.ETCH_WAFERS_PER_WEEK - n_ours_week, 50.0) / 7.0     # wafers per day
            bg, d = [], span0
            while d < span1:
                d += float(rng.exponential(1.0 / (bg_rate / 25.0)))
                n = int(rng.choice([25, 25, 24, 25, 23]))
                rec = "CT-STD-09" if rng.random() < 0.35 else "CT-STD-11"
                base_rf = 86.0 if rec == "CT-STD-09" else 91.0
                for k in range(n):
                    bg.append((d + k * 0.0021, None, k + 1, rec, base_rf * rng.normal(1, 0.015)))
            stream = sorted(ours[ch] + bg, key=lambda e: e[0])
            load, count, rfh = 0.0, int(rng.integers(0, 2300)), 0.0
            load = count * 91.0
            rfh = load / 3600.0
            pending_clean = False
            mon_day = math.floor(span0) + 1
            for d, lid, slot, rec, rf in stream:
                # the morning monitor wafer at 07:00
                while mon_day + 7 / 24.0 <= d:
                    excess = max(0.0, load - P.L_TH) / 1e4
                    lam = P.PRT_BASE + P.FLAKE_A * excess ** P.FLAKE_POW
                    self.monitors.append(dict(ch=ch, d=mon_day + 7 / 24.0 + float(rng.uniform(0, 0.02)),
                                              adders=int(rng.poisson(lam * 0.55 + 1.5)), count=count))
                    mon_day += 1
                if count >= P.CLEAN_WAFERS and not pending_clean:
                    pending_clean = True
                    due = d + float(rng.uniform(0.05, 0.6))
                if pending_clean and d >= due:
                    self.etch_cleans[ch].append(dict(d=due, count=count, rfh=rfh))
                    load, count, rfh = 0.0, 0, 0.0
                    pending_clean = False
                excess = max(0.0, load - P.L_TH) / 1e4
                lam = P.PRT_BASE + P.FLAKE_A * excess ** P.FLAKE_POW
                count += 1
                load += rf * P.CHEM[rec]
                rfh += rf / 3600.0
                if lid is not None:
                    self.etch_wafers[ch].append(dict(d=d, lid=lid, slot=slot, rec=rec, rf=rf, count=count, rfh=rfh,
                                                     load=load, lam=lam))
        self.etch_of = {}
        for ch, rows in self.etch_wafers.items():
            for r in rows:
                self.etch_of[(r["lid"], r["slot"])] = dict(r, ch=ch)

    # -------------------------------------------------------------- the ILD0 edge
    def edge(self):
        rng = np.random.default_rng(P.SEED + 8)
        self.edge_of = {}
        d_sh, d_tune = tday(P.T_SHOWERHEAD), tday(P.T_CM3_TUNE)
        for L in self.lots:
            if "ILD0-CMP" not in L.times:
                continue
            dep_tool, cmp_tool = L.tools["ILD0-DEP"], L.tools["ILD0-CMP"]
            d_dep, d_cmp = L.times["ILD0-DEP"], L.times["ILD0-CMP"]
            for slot in L.slots:
                ch = dep_tool + ("A" if slot % 2 == 1 else "B")
                if self.is_down(ch, d_dep):
                    ch = dep_tool + ("B" if ch.endswith("A") else "A")
                dep = P.CHAMBER_STATIC[ch] + (P.DP2B_EDGE if (ch == "DP2B" and d_dep >= d_sh) else 0.0)
                rem = P.CMP_STATIC[cmp_tool] + (P.CM3_EDGE if (cmp_tool == "CM3" and d_cmp >= d_tune) else 0.0)
                noise = float(rng.normal(0, P.EDGE_NOISE))
                self.edge_of[(L.lid, slot)] = dict(ch=ch, dep=dep, rem=rem, net=dep - rem + noise, cmp=cmp_tool,
                                                   noise=noise)

    # -------------------------------------------------------------- scratches from ILD0 CMP
    def scratches(self):
        rng = np.random.default_rng(P.SEED + 9)
        self.scr_lam = {}
        for L in self.lots:
            if "ILD0-CMP" not in L.times:
                continue
            tool = L.tools["ILD0-CMP"]
            pol = P.PRODUCTS["VR90"]["polish_s"] if L.tv else P.PRODUCTS[L.product]["polish_s"]
            for k, slot in enumerate(L.slots):
                d = L.times["ILD0-CMP"] + k * 0.0035
                lpc = float(self.tap_lpc(tool, d))
                age = float(self.pou_age(tool, d))
                pas = min(0.95, P.POU_PASS0 + P.POU_PASS_DAY * age)
                self.scr_lam[(L.lid, slot)] = P.SCR_BASE * (lpc / P.SCR_REF) ** P.SCR_POW * pas * pol / 60.0

    # -------------------------------------------------------------- sort
    BINMIX = {
        "rand": ((8,), (1.0,)),
        "prt": ((8,), (1.0,)),
        "scr": ((5,), (1.0,)),
        "goi": ((6,), (1.0,)),
        "thick": ((3,), (1.0,)),
        "thin": ((4,), (1.0,)),
        "edgefall": ((3, 4, 8), (0.40, 0.30, 0.30)),
    }
    ORDER = {3: 0, 4: 1, 5: 2, 6: 3, 8: 4, 9: 5, 11: 6}

    def edge_profile(self, rmax):
        return np.clip((rmax - P.EDGE_R0) / (P.WAFER_R - P.EDGE_EXCL - P.EDGE_R0), 0, 1) ** P.EDGE_POW

    def scratch_dies(self, grid, n, rng):
        """die indices crossed by n micro-scratches: centres weighted toward the edge, short arcs about 1.4 mm long"""
        if n == 0:
            return []
        r = 147.0 * np.sqrt(rng.random(n * 3))
        keep = rng.random(n * 3) < (1 + 0.5 * r / 147.0) / 1.5
        r = r[keep][:n]
        while len(r) < n:
            r = np.concatenate([r, 147.0 * np.sqrt(rng.random(n))])[:n]
        th = rng.uniform(0, 2 * np.pi, n)
        ln = rng.lognormal(np.log(P.SCR_LEN_MM), 0.5, n)
        ori = th + np.pi / 2 + rng.normal(0, 0.45, n)
        out = []
        for i in range(n):
            m = max(2, int(ln[i] / 0.4))
            s = np.linspace(-ln[i] / 2, ln[i] / 2, m)
            x = r[i] * np.cos(th[i]) + s * np.cos(ori[i])
            y = r[i] * np.sin(th[i]) + s * np.sin(ori[i])
            d = grid.die_at(x, y)
            d = np.unique(d[d >= 0])
            out.append(d)
        return out

    def die_kills(self, grid, prodname, gw, lam_p, lam_s, c, net, rng, product_for_design=None):
        """one wafer's die: every mechanism's kills, then each die binned on its first failing test.
        gw: the wafer's random-defect multiplier (the line's level times the wafer's own draw)"""
        g = grid
        prod = P.PRODUCTS[prodname]
        area_mm2 = g.w * g.h
        regs, inv = np.unique(g.region, return_inverse=True)
        hr = rng.gamma(P.ALPHA_REGION, 1.0 / P.ALPHA_REGION, len(regs))[inv]
        lam = P.D0 * g.area_cm2 * gw * hr
        kill = {}
        kill["rand"] = rng.random(g.n) < 1 - np.exp(-lam)
        pp = 1 - np.exp(-lam_p * area_mm2 / (np.pi * 150.0 ** 2) * P.PRT_KILL)
        kill["prt"] = rng.random(g.n) < pp
        ns = int(rng.poisson(lam_s))
        ks = np.zeros(g.n, dtype=bool)
        for dd in self.scratch_dies(g, ns, rng):
            if len(dd):
                ks[dd[rng.random(len(dd)) < P.SCR_KILL]] = True
        kill["scr"] = ks
        pg = P.GOI_K * prod["gate"] * max(0.0, c - P.C_TH) ** P.GOI_EXP + 0.0006 * prod["gate"]
        kill["goi"] = rng.random(g.n) < pg
        prof = self.edge_profile(g.rmax)
        netd = net * prof
        pth = P.KILL_THICK * (1 - np.exp(-np.maximum(0.0, netd - P.TOL_THICK) / P.EDGE_SCALE))
        ptn = P.KILL_THIN * (1 - np.exp(-np.maximum(0.0, -netd - P.TOL_THIN) / P.EDGE_SCALE))
        kill["thick"] = rng.random(g.n) < pth
        kill["thin"] = rng.random(g.n) < ptn
        kill["edgefall"] = (g.rmax > 145.0) & (rng.random(g.n) < 0.06)
        design = rng.random(g.n) < (1 - prod["design"])
        best = np.full(g.n, 99, dtype=np.int16)
        binv = np.ones(g.n, dtype=np.int16)
        order = self.ORDER
        for m in self.BINMIX:
            idx = np.nonzero(kill[m])[0]
            if len(idx) == 0:
                continue
            bins, pr = self.BINMIX[m]
            b = np.array(bins)[rng.choice(len(bins), size=len(idx), p=pr)]
            o = np.array([order[x] for x in b])
            better = o < best[idx]
            best[idx[better]] = o[better]
            binv[idx[better]] = b[better]
        idx = np.nonzero(design)[0]
        if len(idx):
            if prodname == "VX40":
                b = np.where(rng.random(len(idx)) < 0.6, 9, 11)
            else:
                b = np.full(len(idx), 9)
            o = np.array([order[x] for x in b])
            better = o < best[idx]
            best[idx[better]] = o[better]
            binv[idx[better]] = b[better]
        truth = {m: int(kill[m].sum()) for m in self.BINMIX}
        truth["design"] = int(design.sum())
        return binv.astype(np.int8), truth, ns

    def line_drift(self):
        weeks = np.arange(0, 80)
        drift = np.exp(np.random.default_rng(P.SEED + 11).normal(0, P.DRIFT_WEEKS, len(weeks)))
        return drift / drift.mean()

    def wafers_sort(self):
        rng = np.random.default_rng(P.SEED + 10)
        self.sorted = []
        drift = self.line_drift()
        for L in self.lots:
            if L.tv or "SORT" not in L.times:
                continue
            g = self.grids[L.product]
            for k, slot in enumerate(L.slots):
                if slot in L.scrap:
                    continue
                key = (L.lid, slot)
                wk = int(L.times["ILD0-CMP"] // 7)
                gw = rng.gamma(P.ALPHA_WAFER, 1.0 / P.ALPHA_WAFER) * drift[min(wk, len(drift) - 1)]
                e = self.edge_of[key]
                c = self.bath_at[L.lid]
                lam_p = self.etch_of[key]["lam"]
                binv, truth, ns = self.die_kills(g, L.product, gw, lam_p, self.scr_lam[key], c, e["net"], rng)
                t_sort = L.times["SORT"] + k * 0.0042
                self.sorted.append(dict(lid=L.lid, product=L.product, slot=slot, d=t_sort, bins=binv,
                                        good=int((binv == 1).sum()), truth=truth, c=c, net=e["net"], ch_dep=e["ch"],
                                        cmp=e["cmp"], lam_p=lam_p, lam_s=self.scr_lam[key], ns=ns, gw=gw))
