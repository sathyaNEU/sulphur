"""task23 architecture 1: the simulated Fernhallow Regional Landfill. Everything the pack records comes from here:
the weather on site hour by hour, the waste placed by cell and material month by month, the methane it makes (a
first-order decay that starts six months after placement, faster where recirculated leachate reaches), what each gas
well collects (less as liquid rises over its screen), what the cover oxidizes (a capacity per square metre that the
flux saturates), the gas the waste holds and releases as the barometer moves, and what each instrument sees."""
import datetime as dt
import math

import numpy as np

import params as P

H_PER_DAY = 24


# ---------------------------------------------------------------- calendar helpers
def month_index(y, m):
    return (y - P.Y0) * 12 + (m - 1)


def month_of_index(i):
    return P.Y0 + i // 12, i % 12 + 1


NM = (P.YEND - P.Y0) * 12


def days_in_month(y, m):
    nxt = dt.date(y + (m == 12), m % 12 + 1, 1)
    return (nxt - dt.date(y, m, 1)).days


DIM = np.array([days_in_month(*month_of_index(i)) for i in range(NM)], dtype=float)


class World:
    def __init__(self, seed=P.SEED):
        self.rng = np.random.default_rng(seed)
        self.streams = {k: np.random.default_rng(seed + j * 7919) for j, k in enumerate(
            ["wx", "waste", "tickets", "wells", "chambers", "campaigns", "drone", "study", "scada", "misc", "docs",
             "gw", "leach", "sem", "odor", "log", "wo", "wx2", "coll2"])}
        self.weather()
        self.waste()
        self.generation()
        self.collection()
        self.emissions()

    # ---------------------------------------------------------------- weather
    def weather(self):
        r = self.streams["wx"]
        t0, t1 = P.WX0, P.FCST_END
        n = int((t1 - t0).total_seconds() // 3600) + 1
        self.hours = np.array([t0 + dt.timedelta(hours=h) for h in range(n)])  # local standard time (UTC-8)
        hod = np.arange(n) % 24
        doy = np.array([h.timetuple().tm_yday for h in self.hours], dtype=float)
        winter = 0.5 * (1 + np.cos(2 * np.pi * (doy - 20) / 365.25))      # 1 in late January, 0 in late July
        P0 = np.full(n, 1016.5)
        rain = np.zeros(n)
        wind = np.zeros(n)
        cloud = np.full(n, 0.35)
        stormy = np.zeros(n, dtype=bool)
        i = int(r.uniform(10, 60))
        while i < n - 120:
            w = winter[i]
            depth = r.gamma(3.2, (4.0 + 9.0 * w) / 3.2)
            fall = int(r.uniform(8, 24))
            rise = int(r.uniform(26, 60))
            seg = np.r_[-depth * (1 - np.cos(np.linspace(0, np.pi, fall))) / 2,
                        -depth * (1 + np.cos(np.linspace(0, np.pi, rise))) / 2]
            L = len(seg)
            j1 = min(n, i + L)
            P0[i:j1] += seg[:j1 - i]
            intensity = r.uniform(0.35, 1.5) * (0.55 + 1.1 * w)
            # rain: through the latter part of the fall and the trough; showers early in the rise
            pr = np.r_[np.clip(np.linspace(-0.4, 1.0, fall), 0, None), np.clip(np.linspace(0.75, -0.6, rise), 0, None)]
            showers = r.random(L) < pr
            rr = np.where(showers, r.gamma(1.4, 0.9, L) * intensity, 0.0)
            rain[i:j1] += rr[:j1 - i]
            pk = r.uniform(7.5, 13.5) * (0.85 + 0.25 * w)
            ww = np.r_[np.linspace(3.0, pk, fall), pk - (pk - 2.6) * np.linspace(0, 1, rise) ** 0.8]
            wind[i:j1] = np.maximum(wind[i:j1], ww[:j1 - i])
            cl = np.r_[np.linspace(0.6, 1.0, fall), np.clip(np.linspace(0.95, 0.05, rise), 0.05, 1)]
            cloud[i:j1] = np.maximum(cloud[i:j1], cl[:j1 - i])
            stormy[i:j1] = True
            gap = r.gamma(3.0, (2.6 + 5.4 * (1 - w)) * 24 / 3.0)
            i += L + int(gap)
        # quiet spells: light winds with a summer afternoon breeze
        calm = ~stormy
        breeze = (1 - winter) * np.clip(np.sin(np.pi * (hod - 11) / 9), 0, None) * 1.1
        wind[calm] = (r.gamma(2.2, 0.75, n) + breeze)[calm]
        wind = np.clip(wind + r.normal(0, 0.45, n), 0.2, None)
        # slow background (blocking highs, the seasonal mean), the semidiurnal and diurnal pressure tides
        bg = np.zeros(n)
        x = 0.0
        e = r.normal(0, 0.10, n)
        for k in range(n):
            x = 0.9994 * x + e[k]
            bg[k] = x
        P0 += 1.7 * bg + 2.8 * (1 - winter)
        P0 += 0.78 * np.cos(2 * np.pi * (hod - 10.2) / 12.0) + 0.28 * np.cos(2 * np.pi * (hod - 6.0) / 24.0)
        self.pressure = P0 + r.normal(0, 0.04, n)                     # hPa, sea-level-equivalent at the site datum
        self.rain = np.round(np.where(rain > 0.08, rain, 0.0), 1)     # mm per hour
        self.wind = wind
        self.wind_dir = (230 + 70 * np.sin(np.arange(n) / 61.0) + r.normal(0, 35, n)) % 360
        clear = 1 - cloud
        self.air_t = 10.6 + 7.0 * np.cos(2 * np.pi * (doy - 205) / 365.25) \
            + (2.0 + 3.0 * clear) * np.cos(2 * np.pi * (hod - 15) / 24) + r.normal(0, 1.1, n) - 1.2 * (rain > 0)
        self.soil_t = 11.0 + 6.6 * np.cos(2 * np.pi * (doy - 215) / 365.25) \
            + 1.2 * np.cos(2 * np.pi * (hod - 17) / 24) + r.normal(0, 0.25, n)
        self.rh = np.clip(78 + 14 * winter - 18 * clear * np.clip(np.cos(2 * np.pi * (hod - 15) / 24), 0, None)
                          + 12 * (rain > 0) + r.normal(0, 4, n), 25, 100)
        self.solar = np.clip(np.sin(np.pi * (hod - 6) / 13.0), 0, None) * (300 + 520 * (1 - winter)) * (0.25 + 0.75 * clear)
        # the weather's memory: warm and cold spells of days to weeks, and years that run warm or cool; the air takes
        # them at once, the soil at 10 cm a few days late and damped
        r2 = self.streams["wx2"]
        nd = n // 24 + 2
        ed = r2.normal(0, 0.62, nd)
        spell = np.zeros(nd)
        xs = 0.0
        for k in range(nd):
            xs = 0.86 * xs + ed[k]
            spell[k] = xs
        years_ = np.array([h.year for h in self.hours])
        ya = {y: r2.normal(0, 0.6) for y in range(int(years_.min()), int(years_.max()) + 1)}
        dd = np.arange(n) / 24.0
        sp = np.interp(dd, np.arange(nd), spell)
        anom = sp + np.array([ya[y] for y in years_])
        self.air_t = self.air_t + anom
        self.soil_t = self.soil_t + 0.7 * self._ema(anom, 24 * 5.0)
        self.n_hours = n
        # the gas the waste holds: the lagged gap between the waste's gas pressure and the barometer
        self.baro_gap = self._ema(self.pressure, P.BARO_TAU_H) - self.pressure
        self.mod = {}
        years = np.array([h.year for h in self.hours])
        self.hour_year = years
        for cov, c in P.BARO_C.items():
            m = np.exp(c * self.baro_gap)
            for y in np.unique(years):
                sel = years == y
                m[sel] /= m[sel].mean()
            self.mod[cov] = m

    @staticmethod
    def _ema(x, tau):
        out = np.empty_like(x)
        out[0] = x[0]
        a = 1.0 / tau
        for k in range(1, len(x)):
            out[k] = out[k - 1] + a * (x[k] - out[k - 1])
        return out

    def hour_index(self, when):
        """Index of a local-standard-time hour."""
        return int((when - P.WX0).total_seconds() // 3600)

    # ---------------------------------------------------------------- waste
    def waste(self):
        r = self.streams["waste"]
        yrs = np.arange(P.Y0, P.YEND)
        base = np.interp(yrs, [1986, 1995, 2000, 2007, 2009, 2012, 2019, 2020, 2021, 2026, 2027],
                         [158e3, 196e3, 214e3, 262e3, 238e3, 246e3, 291e3, 282e3, 300e3, 331e3, 336e3])
        base *= np.exp(r.normal(0, 0.018, len(yrs)))
        season = np.array([0.90, 0.88, 0.97, 1.01, 1.06, 1.09, 1.10, 1.11, 1.05, 1.02, 0.94, 0.87])
        season /= season.mean()
        self.tonnes = {c: {mat: np.zeros(NM) for mat in P.SHARE} for c in P.CELLS}
        open_m = {c: month_index(*P.CELLS[c]["open"]) for c in P.CELLS}
        close_m = {c: month_index(*P.CELLS[c]["close"]) for c in P.CELLS}
        self.month_total = np.zeros(NM)
        for i in range(NM):
            y, m = month_of_index(i)
            tot = base[y - P.Y0] / 12.0 * season[m - 1] * math.exp(r.normal(0, 0.025))
            if i < month_index(1986, 4):
                tot = 0.0
            self.month_total[i] = tot
            active = [c for c in P.CELLS if open_m[c] <= i <= close_m[c]]
            # the cell 4 to cell 5 changeover: January 2025 into cell 4, February 2025 on into cell 5
            for c in active:
                share = 1.0 / len(active)
                for mat, s in P.SHARE.items():
                    sj = s * math.exp(r.normal(0, 0.06))
                    self.tonnes[c][mat][i] += tot * share * sj
        self.open_m, self.close_m = open_m, close_m

    def potential_placed(self, c, L0=None):
        L0 = L0 or P.L0_TRUE
        return sum(self.tonnes[c][mat] * L0[mat] for mat in P.SHARE)   # m3 CH4 placed in the month

    # ---------------------------------------------------------------- generation
    @staticmethod
    def fod(placed_m3, kd, kw, reach, rec_month, lag=P.LAG_MONTHS, ramp=P.RAMP_MONTHS):
        """Monthly methane generation (m3) from monthly placed potential: the reached share decays at kw from the
        recirculation month (ramped), the rest at kd; generation begins `lag` months after placement. Returns the
        total and the reached part."""
        n = len(placed_m3)
        g = np.zeros(n)
        gw_out = np.zeros(n)
        pend = np.zeros(n + lag + 1)
        pd_, pw = 0.0, 0.0
        for i in range(n):
            pend[i + lag] += placed_m3[i]
            r = reach if rec_month is not None else 0.0
            pw += pend[i] * r
            pd_ += pend[i] * (1 - r)
            w = min(1.0, (i - rec_month + 1) / ramp) if (rec_month is not None and i >= rec_month) else 0.0
            kr = kd + (kw - kd) * w
            gw = pw * (1 - math.exp(-kr / 12.0))
            gd = pd_ * (1 - math.exp(-kd / 12.0))
            pw -= gw
            pd_ -= gd
            g[i] = gw + gd
            gw_out[i] = gw
        return g, gw_out

    def generation(self):
        self.gen = {}
        self.gen_wet = {}
        for c in P.CELLS:
            rec = P.RECIRC.get(c)
            # the leachate takes weeks to spread: the faster decay starts the month after injection begins
            rm = month_index(rec.year, rec.month) + 1 if rec else None
            g, gw = self.fod(self.potential_placed(c), P.KD, P.KW, P.REACH.get(c, 0.0), rm)
            self.gen[c] = g * P.RHO_CH4           # t CH4 per month
            self.gen_wet[c] = gw * P.RHO_CH4      # the reached part

    # ---------------------------------------------------------------- collection, wells, liquids
    def collection(self):
        r = self.streams["wells"]
        self.wells = []
        # closed cells: wells installed at capping, re-drills now and then
        counts = {1: 16, 2: 19, 3: 21, 4: 58}
        k = 0
        for c in (1, 2, 3, 4):
            nw = counts[c]
            shares = r.dirichlet(np.full(nw, 6.0))
            for j in range(nw):
                k += 1
                wid = "%d%02d" % (c, j + 1)
                inst = {1: dt.date(1998, 4, 1), 2: dt.date(2007, 3, 1), 3: dt.date(2015, 9, 1),
                        4: dt.date(2016, 5, 1)}[c] + dt.timedelta(days=int(r.integers(0, 600)))
                if c == 4 and j >= 46:
                    inst = dt.date(2019, 3, 1) + dt.timedelta(days=int(r.integers(0, 420)))
                wet = False
                if c == 4:
                    wet = j % 9 in (0, 2, 4, 6)   # four in nine of cell 4's wells sit where the leachate reaches
                depth = float(r.uniform(55, 95) if c < 4 else r.uniform(70, 125))
                screen_top = round(depth * r.uniform(0.28, 0.40), 1)
                screen_bot = round(depth - r.uniform(3, 8), 1)
                self.wells.append(dict(id="EW-" + wid, cell=c, share=float(shares[j]), wet=wet, install=inst,
                                       depth=round(depth, 1), screen_top=screen_top, screen_bot=screen_bot,
                                       ch4=float(r.uniform(44, 50) if c < 4 else r.uniform(50, 55)),
                                       temp=float(r.uniform(78, 102) if c < 4 else r.uniform(98, 122)),
                                       pump=None, rise=float(r.uniform(0.65, 1.0)), speed=float(r.uniform(0.7, 1.4))))
        # the six pilot pumps of June 2025: among the deepest-flooded wet wells
        wets = [w for w in self.wells if w["cell"] == 4 and w["wet"]]
        pick = r.choice(len(wets), size=P.PILOT_WELLS, replace=False)
        for k in sorted(pick):
            wets[k]["pump"] = P.PILOT_DATE
        s_wet = sum(w["share"] for w in wets)
        s_dry = sum(w["share"] for w in self.wells if w["cell"] == 4 and not w["wet"])
        for w in self.wells:
            if w["cell"] == 4:
                w["zone_share"] = w["share"] / (s_wet if w["wet"] else s_dry)
            else:
                w["zone_share"] = w["share"]
        self.s_wet = s_wet
        # month by month: each well's submerged screen fraction and its yield
        rec4 = month_index(P.RECIRC[4].year, P.RECIRC[4].month)
        self.sub = {}
        for w in self.wells:
            s = np.zeros(NM)
            if w["cell"] == 4 and w["wet"]:
                for i in range(NM):
                    if i >= rec4:
                        x = (i - rec4) / 12.0 * w["speed"]
                        s[i] = w["rise"] / (1 + math.exp(-3.2 * (x - 1.15)))
                    if w["pump"] is not None and i >= month_index(w["pump"].year, w["pump"].month):
                        s[i] = min(s[i], 0.04)
            self.sub[w["id"]] = s
        # collected methane by well and by cell, t per month (before the packages)
        self.coll_well = {}
        self.coll = {c: np.zeros(NM) for c in P.CELLS}
        for w in self.wells:
            c = w["cell"]
            inst_m = month_index(w["install"].year, w["install"].month)
            on = (np.arange(NM) >= inst_m).astype(float)
            if c == 4:
                part = self.gen_wet[4] if w["wet"] else self.gen[4] - self.gen_wet[4]
                y = 1 - P.FLOOD_LOSS_MAX * self.sub[w["id"]]
                cw = P.CE4_BASE * w["zone_share"] * part * y * on
            else:
                cw = P.CE_FINAL * w["zone_share"] * self.gen[c] * on
            self.coll_well[w["id"]] = cw
            self.coll[c] += cw
        # the wellfield's own state month to month (tuning rounds, header vacuum, condensate in the laterals) and the
        # blowers' outages, when every well stops drawing for hours to a day and a half
        r2 = self.streams["coll2"]
        fac = np.ones(NM)
        xs = 0.0
        for i in range(NM):
            xs = 0.55 * xs + r2.normal(0, 1.0) * P.WELLFIELD_SD
            fac[i] = 1.0 + xs
        fac[month_index(2026, 11):] = 1.0       # the months the forecast covers: the wellfield in its normal state
        self.blower_out = set()
        self.out_hours = np.zeros(NM)
        for y in range(P.WX0.year, P.YEND):
            for _ in range(int(r2.poisson(3.0))):
                h0 = self.hour_index(dt.datetime(y, 1, 1)) + int(r2.integers(0, 8700))
                for h in range(h0, h0 + int(r2.integers(3, 34))):
                    if 0 <= h < len(self.hours):
                        if h not in self.blower_out:
                            self.blower_out.add(h)
                            t = self.hours[h]
                            self.out_hours[month_index(t.year, t.month)] += 1
        self.coll_factor = fac * (1.0 - self.out_hours / (DIM * 24.0))
        for w in self.wells:
            self.coll_well[w["id"]] = self.coll_well[w["id"]] * self.coll_factor
        self.coll = {c: np.zeros(NM) for c in P.CELLS}
        for w in self.wells:
            self.coll[w["cell"]] += self.coll_well[w["id"]]
        # before a closed cell's wells exist its gas went uncollected; cell 4 before its wells: horizontal collectors
        hc_m = month_index(2016, 5)
        for i in range(NM):
            if i < hc_m:
                self.coll[4][i] += 0.35 * self.gen[4][i]

    def ce_pkg(self, c, i, pkg, restore=1.0):
        """Collection efficiency of cell c in month i under a package (the true world's)."""
        g = self.gen[c][i]
        if g <= 0:
            return 0.0
        base = self.coll[c][i] / g
        works = P.PACKAGES[pkg]["works"]
        when = {k: month_index(v.year, v.month) for k, v in P.WORKS.items()}
        if c == 5:
            v = 0.0
            if "hc5" in works and i >= when["hc5"]:
                v = P.CE5_HC
            if "wells5" in works and i >= when["wells5"]:
                v = P.CE5_WELLS
            return v
        if c == 4:
            v = base
            if "pumps4" in works and i >= when["pumps4"]:
                lost = sum(P.CE4_BASE * w["zone_share"] * self.gen_wet[4][i] * P.FLOOD_LOSS_MAX * self.sub[w["id"]][i]
                           for w in self.wells if w["cell"] == 4 and w["wet"]) / g
                v = base + lost * restore * 0.92
            if "cap4" in works and i >= when["cap4"]:
                v = max(v, P.CE4_CAP)
            return v
        return base

    # ---------------------------------------------------------------- oxidation and emission
    @staticmethod
    def vox(cover, soil_t):
        return P.VOX15[cover] * P.Q10 ** ((soil_t - 15.0) / 10.0)

    def cover_of(self, c, i):
        if c == 5:
            return "active"
        if c == 4:
            return "intermediate" if i >= month_index(2013, 4) else "active"
        cap = P.CELLS[c]["capped"]
        return "final" if i >= month_index(*cap) else ("intermediate" if i > self.close_m[c] else "active")

    def month_soil_t(self):
        if hasattr(self, "_mst"):
            return self._mst
        out = np.zeros(NM)
        mi = np.array([month_index(h.year, h.month) for h in self.hours])
        for i in np.unique(mi):
            out[i] = self.soil_t[mi == i].mean()
        # months before the station: the station's normals
        norm = np.array([self.soil_t[np.array([h.month for h in self.hours]) == m].mean() for m in range(1, 13)])
        for i in range(NM):
            if out[i] == 0:
                out[i] = norm[i % 12]
        self._mst, self.soil_normal = out, norm
        self._mi = mi
        return out

    def emission_month(self, pkg="A", restore=1.0, normal=False):
        """{cell: t per month} of methane leaving each cell's surface, and the uncollected gas reaching the cover."""
        mst = self.month_soil_t()
        E, U, OX = {}, {}, {}
        for c in P.CELLS:
            e = np.zeros(NM)
            u = np.zeros(NM)
            ox = np.zeros(NM)
            for i in range(NM):
                g = self.gen[c][i]
                if g <= 0:
                    continue
                ce = self.ce_pkg(c, i, pkg, restore)
                ui = g * (1 - ce)
                J = ui * 1e6 / P.CELLS[c]["area"] / DIM[i]
                T = self.soil_normal[i % 12] if normal else mst[i]
                V = self.vox(self.cover_of(c, i), T)
                f = V / (V + J) if J > 0 else 0.0
                u[i], ox[i], e[i] = ui, ui * f, ui * (1 - f)
            E[c], U[c], OX[c] = e, u, ox
        return E, U, OX

    def emissions(self):
        self.E, self.U, self.OX = self.emission_month("A")
        coll_tot = sum(self.coll[c] for c in P.CELLS)
        self.slip = coll_tot * (1 - P.DESTRUCTION)          # t per month unburned at the flare and engines
        mi = np.array([month_index(h.year, h.month) for h in self.hours])
        self._mi = mi
        hrs_in_month = np.bincount(mi, minlength=NM).astype(float)
        hrs_in_month[hrs_in_month == 0] = 1
        self.E_hour = np.zeros(self.n_hours)       # t per hour, the whole site
        self.E_hour_cell = {}
        for c in P.CELLS:
            cov = np.array([self.cover_of(c, i) for i in range(NM)])
            covh = cov[mi]
            m = np.where(covh == "final", self.mod["final"],
                         np.where(covh == "intermediate", self.mod["intermediate"], self.mod["active"]))
            eh = self.E[c][mi] / hrs_in_month[mi] * m
            self.E_hour_cell[c] = eh
            self.E_hour += eh
        self.slip_hour = self.slip[mi] / hrs_in_month[mi]
        self.E_hour += self.slip_hour
        self.hrs_in_month = hrs_in_month

    # ---------------------------------------------------------------- the truth the answers are checked against
    def truth_year(self, y):
        i0 = month_index(y, 1)
        return float(sum(self.E[c][i0:i0 + 12].sum() for c in P.CELLS) + self.slip[i0:i0 + 12].sum())

    def truth_2027(self, pkg, restore=1.0):
        E, U, OX = self.emission_month(pkg, restore, normal=True)
        i0 = month_index(2027, 1)
        coll = 0.0
        for c in P.CELLS:
            for i in range(i0, i0 + 12):
                coll += self.gen[c][i] * self.ce_pkg(c, i, pkg, restore)
        return float(sum(E[c][i0:i0 + 12].sum() for c in P.CELLS) + coll * (1 - P.DESTRUCTION))
