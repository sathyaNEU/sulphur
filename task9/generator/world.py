"""task9: the fab simulator. Lots start each week, every wafer runs a forty-step flow (lot-level tools at most steps, a
chamber per wafer at six), its ILD-CMP polish lands on one of four units in time order, and each unit's pad, conditioner
disk and retaining ring wear by the wafer and are reset by the maintenance the spec and the floor actually did. A wafer's
defects are clustered random kills on top of its own defect density; its outer band adds the band's normal roll-off and
the edge ring the worn disk causes. Sort, metrology, the classifier and the die-map pulls then see the wafer. Nothing
here knows what the analysis will ask.
"""
import datetime as dt
import math

import numpy as np

import params as P

STEPS = ["ZERO-MARK", "PAD-OX", "NIT-DEP", "STI-LITHO", "STI-ETCH", "STI-FILL", "STI-CMP", "WELL-IMP1", "WELL-IMP2", "GATE-OX",
         "POLY-DEP", "POLY-LITHO", "POLY-ETCH", "LDD-IMP", "SPACER-DEP", "SPACER-ETCH", "SD-IMP", "RTA", "SALICIDE", "PMD-DEP",
         "PMD-CMP", "CT-LITHO", "CT-ETCH", "W-DEP", "W-CMP", "M1-DEP", "M1-LITHO", "M1-ETCH", "ILD-DEP", "ILD-CMP", "V1-LITHO",
         "V1-ETCH", "M2-DEP", "M2-LITHO", "M2-ETCH", "PASS-DEP", "PAD-LITHO", "PAD-ETCH", "ALLOY", "FINAL-INSP"]
WAFER_STEPS = ["STI-CMP", "PMD-CMP", "W-CMP", "ILD-DEP", "ILD-CMP", "PASS-DEP"]   # in flow order, so every draw is in a fixed order
CMP_STEP, DEP_STEP = STEPS.index("ILD-CMP"), STEPS.index("ILD-DEP")
UNITS = ["PU-1", "PU-2", "PU-3", "PU-4"]


def day(d):
    return (d - P.START).days


def tools_for(step, rng):
    """Each step's tools, named as the fab names them."""
    if step == "ILD-CMP":
        return UNITS
    if step == "ILD-DEP":
        return ["DEP-1", "DEP-2", "DEP-3", "DEP-4"]
    if step == "M1-LITHO":
        return ["SC-1", "SC-2", "SC-3", "SC-4"]
    if step in ("STI-LITHO", "POLY-LITHO", "CT-LITHO", "V1-LITHO", "M2-LITHO", "PAD-LITHO"):
        return ["SC-1", "SC-2", "SC-3"]
    pre = "".join(ch for ch in step.split("-")[0] if ch.isalpha())[:3]
    n = int(rng.integers(2, 7))
    return ["%s-%s%d" % (pre, step.split("-")[-1][:2], k + 1) for k in range(n)]


def die_grid(product):
    """Die centres (mm) and their radial zone for one product's stepping: dies wholly inside the usable radius."""
    p = P.PRODUCTS[product]
    w, h = p["die_w"], p["die_h"]
    rmax = P.WAFER_R - P.EDGE_EXCL
    nx, ny = int(2 * rmax // w) + 2, int(2 * rmax // h) + 2
    out = []
    for i in range(-nx, nx + 1):
        for j in range(-ny, ny + 1):
            cx, cy = (i + 0.5) * w, (j + 0.5) * h
            corners = [(cx + sx * w / 2, cy + sy * h / 2) for sx in (-1, 1) for sy in (-1, 1)]
            if max(math.hypot(x, y) for x, y in corners) <= rmax:
                r = math.hypot(cx, cy)
                z = next(k for k in range(1, 9) if r < P.ZONE_EDGES[k] or k == 8)
                out.append((i, j, cx, cy, r, z))
    return out


class Fab:
    def __init__(self, seed=P.SEED):
        self.rng = np.random.default_rng(seed)
        rng = self.rng
        self.tools = {s: tools_for(s, rng) for s in STEPS}
        self.offsets = {(s, t): float(rng.normal(0, P.TOOL_OFFSET_SD)) for s in STEPS for t in self.tools[s]}
        self.grids = {pr: die_grid(pr) for pr in P.PRODUCTS}
        self.zone_n = {pr: np.bincount([g[5] for g in self.grids[pr]], minlength=9)[1:] for pr in P.PRODUCTS}
        self._lots()
        self._flow()
        self._defects()
        self._sort_and_label()

    # ---- lots and wafers, with the time each wafer reaches ILD-CMP and the unit dispatch would send it to
    def _lots(self):
        rng = self.rng
        self.lots, self.wafers = [], []
        n_weeks = (day(P.LAST_POLISH) // 7) + 1
        lot_no = 4100
        for wk in range(n_weeks):
            for _ in range(int(rng.poisson(P.LOTS_PER_WEEK))):
                t = wk * 7 + rng.uniform(0, 7)
                if t > day(P.LAST_POLISH) + 0.99:
                    continue
                d = P.START + dt.timedelta(days=int(t))
                mix = P.MIX_LATE if d >= P.MIX_SHIFT else P.MIX
                prod = str(rng.choice(list(mix), p=list(mix.values())))
                lot_no += 1
                lot = dict(lot_id="T%06d" % (lot_no * 7 + 13), product=prod, cmp_t=float(t),
                           tools={s: str(rng.choice(self.tools[s])) for s in STEPS if s not in WAFER_STEPS})
                if lot["tools"]["M1-LITHO"] == "SC-4" and d < P.SC4_START:
                    lot["tools"]["M1-LITHO"] = str(rng.choice(["SC-1", "SC-2", "SC-3"]))
                n_w = P.WAFERS_PER_LOT - int(rng.random() < 0.06) - int(rng.random() < 0.02)
                self.lots.append(lot)
                for k in range(n_w):
                    dep = str(rng.choice(self.tools["ILD-DEP"]))
                    p34 = P.DEP_AFFINITY if dep == "DEP-3" else 0.40
                    pref = str(rng.choice(["PU-3", "PU-4"])) if rng.random() < p34 else str(rng.choice(["PU-1", "PU-2"]))
                    chambers = {s: str(rng.choice(self.tools[s])) for s in WAFER_STEPS}
                    chambers["ILD-DEP"] = dep
                    self.wafers.append(dict(lot=lot, slot=k + 1, wafer_id="%s.%02d" % (lot["lot_id"], k + 1), product=prod,
                                            chambers=chambers, pref=pref, polish_t=float(t + k * 0.012 + rng.uniform(0, 0.4))))

    # ---- dispatch and maintenance in one pass in time order: a unit down for a part change sends its wafers to its
    # partner (or, with both down, to the other pair); pads at their life, full PMs at the spec's interval (the waiver's
    # first four reusing the disk), and the unscheduled disk-only and ring-only swaps when they were found
    def _flow(self):
        rng = self.rng
        self.events = []
        partner = {"PU-1": "PU-2", "PU-2": "PU-1", "PU-3": "PU-4", "PU-4": "PU-3"}
        other = {"PU-1": "PU-3", "PU-2": "PU-4", "PU-3": "PU-1", "PU-4": "PU-2"}
        platen = dict(P.PLATEN_BASE)
        st = {u: dict(P.INITIAL[u]) for u in UNITS}
        target = {u: int(rng.normal(*P.PAD_LIFE)) for u in UNITS}
        down = {u: -1e9 for u in UNITS}
        hours = P.DOWN_HOURS
        swaps = sorted([(day(d) + rng.uniform(0.25, 0.75), u, "disk") for u, d in P.DISK_ONLY_SWAPS] +
                       [(day(d) + rng.uniform(0.25, 0.75), u, "ring") for u, d in P.RING_ONLY_SWAPS])
        reuses_left = P.EW118_REUSES
        self.by_unit = {u: [] for u in UNITS}
        disk_m = {u: float(rng.lognormal(0.0, P.DISK_SPREAD)) for u in UNITS}   # each disk's own wear rate
        for w in sorted(self.wafers, key=lambda x: x["polish_t"]):
            t = w["polish_t"]
            while swaps and swaps[0][0] <= t:
                ts, u, part = swaps.pop(0)
                ts = max(ts, down[u])
                st[u][part] = 0
                if part == "disk":
                    disk_m[u] = float(rng.lognormal(0.0, P.DISK_SPREAD))
                self._event(u, ts, "UNSCHED", platen[u], parts=[part], why="disk damage" if part == "disk" else "ring wear")
                down[u] = ts + hours["disk" if part == "disk" else "ring"] / 24.0
            u = w["pref"]
            for cand in (u, partner[u], other[u], partner[other[u]]):
                if down[cand] <= t:
                    u = cand
                    break
            else:
                u = min(UNITS, key=lambda x: down[x])
                t = down[u] + rng.uniform(0.001, 0.01)
                w["polish_t"] = t
            s = st[u]
            w["chambers"]["ILD-CMP"] = u
            w.update(unit=u, platen_count=platen[u], disk=s["disk"], pad=s["pad"], ring=s["ring"], since_full=s["full"], disk_m=disk_m[u])
            self.by_unit[u].append(w)
            platen[u] += 1
            for k in ("disk", "pad", "ring", "full"):
                s[k] += 1
            d = P.START + dt.timedelta(days=int(t))
            interval = P.FULL_PM["REV_F"] if d >= P.REV_F else P.FULL_PM["REV_E"]
            t0 = t + rng.uniform(0.004, 0.02)
            if s["full"] >= interval:
                reuse = reuses_left > 0 and P.EW118[0] <= d <= P.EW118[1]
                parts = ["pad", "ring"] + ([] if reuse else ["disk"])
                s["full"], s["pad"], s["ring"] = 0, 0, 0
                if reuse:
                    reuses_left -= 1
                else:
                    s["disk"] = 0
                    disk_m[u] = float(rng.lognormal(0.0, P.DISK_SPREAD))
                target[u] = int(rng.normal(*P.PAD_LIFE))
                self._event(u, t0, "FULL_PM", platen[u], parts=parts, waiver="EW-118" if reuse else "")
                down[u] = t0 + hours["full"] / 24.0
            elif s["pad"] >= target[u]:
                s["pad"] = 0
                target[u] = int(rng.normal(*P.PAD_LIFE))
                self._event(u, t0, "PAD_CHANGE", platen[u], parts=["pad"])
                down[u] = t0 + hours["pad"] / 24.0

    def _event(self, unit, t, cls, counter, parts, why="", waiver=""):
        self.events.append(dict(unit=unit, t=float(t), cls=cls, counter=int(counter), parts=list(parts), why=why, waiver=waiver))

    # ---- defects, the band's roll-off, the ring, metrology
    def _defects(self):
        rng = self.rng
        n_weeks = (day(P.LAST_POLISH) // 7) + 2
        drift = np.exp(rng.normal(0, P.WEEK_DRIFT, n_weeks))
        pw0, pw1 = day(P.PARTICLE_WEEK[0]) - 3, day(P.PARTICLE_WEEK[1]) + 3
        for w in self.wafers:
            lot = w["lot"]
            off = sum(self.offsets[(s, lot["tools"][s])] for s in lot["tools"]) + sum(self.offsets[(s, w["chambers"][s])]
                                                                                     for s in WAFER_STEPS)
            d0 = rng.gamma(P.D0_SHAPE, P.D0_MEAN / P.D0_SHAPE) * drift[int(w["polish_t"] // 7)] * math.exp(off)
            if pw0 <= w["polish_t"] <= pw1:
                d0 *= P.PARTICLE_MULT
            w["d0"] = d0
            r = P.UNIT_WEAR[w["unit"]] * w["disk_m"]
            e = min(P.RING_CAP, P.RING_SCALE * max(0.0, r * w["disk"] - P.RING_ONSET) / P.RING_SPAN) * (1 + P.PAD_TERM * w["pad"] / 600.0)
            w["ring_excess"] = min(e, 0.95)
            area = P.PRODUCTS[w["product"]]["area"]
            m = rng.gamma(P.CLUSTER_SHAPE, 1.0 / P.CLUSTER_SHAPE, 8)
            p = 1.0 - np.exp(-area * d0 * m)
            p[7] = min(0.98, p[7] + P.ROLL_OFF + w["ring_excess"] * (1 - p[7]))
            n = self.zone_n[w["product"]]
            w["fail"] = rng.binomial(n, p)
            w["cluster_band"] = float(m[7])
            if rng.random() < 0.2:
                ratio = 1 + P.RR_SLOPE * max(0.0, r * w["disk"] - P.RR_ONSET) + P.RR_RING * w["ring"] + rng.normal(0, P.RR_NOISE)
                cen = rng.normal(262 if w["unit"] in ("PU-3", "PU-4") else 248, 6)
                w["rr"] = (cen, cen * ratio)
            else:
                w["rr"] = None
            w["downforce"] = rng.normal(P.UNIT_DOWNFORCE[w["unit"]], 0.05)

    # ---- sort, the classifier, scrap, and the yield team's die-map pulls
    def _sort_and_label(self):
        rng = self.rng
        for w in self.wafers:
            w["sort_t"] = w["polish_t"] + rng.uniform(10, 17)
            w["scrapped"] = bool(rng.random() < 0.008)
            e = w["ring_excess"]
            if e > P.ADC["severe"]:
                ring = rng.random() < P.ADC["severe_recall"]
            elif e > P.ADC["moderate"]:
                ring = rng.random() < P.ADC["moderate_recall"]
            elif e > P.ADC["mild"]:
                ring = rng.random() < P.ADC["mild_recall"]
            else:
                fp = P.ADC["fp_base"] + (0.05 if (w["d0"] > 0.2 and w["cluster_band"] > 1.6) else 0.0)
                ring = rng.random() < fp
            if ring:
                lab = "EDGE_RING"
            else:
                lab = str(rng.choice(["NONE", "NONE", "NONE", "RANDOM", "CLUSTER", "SCRATCH"], p=[0.3, 0.25, 0.2, 0.15, 0.07, 0.03]))
            w["adc"] = lab
            gross = int(self.zone_n[w["product"]].sum())
            w["yield"] = 1 - w["fail"].sum() / gross
            pull = (lab == "EDGE_RING" and rng.random() < P.DIEMAP["flagged"]) or \
                (w["yield"] < P.DIEMAP["low_yield"] and rng.random() < P.DIEMAP["low_yield_share"]) or rng.random() < P.DIEMAP["random"]
            w["diemap"] = bool(pull and not w["scrapped"] and w["sort_t"] <= day(P.PULL))
