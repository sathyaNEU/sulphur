"""The simulated world behind task3 architecture 5: seventy years of storms over Ollery Creek's 11.5 square miles, the
watershed's runoff response as its paved fraction rises, and the creek's daily flows and instantaneous peaks. The
truth (every storm's runoff and peak) never ships; the pack carries the gauges' records and the county's parcels."""
import datetime as dt

import numpy as np

import common as K

D0 = dt.date(K.YEAR0 - 1, 10, 1)           # water year 1956 starts 1 October 1955
D1 = dt.date(K.YEAR1, 12, 31)


def imp_frac(year):
    y = np.asarray(year, dtype=float)
    return K.IMP0 + (K.IMP1 - K.IMP0) / (1 + np.exp(-(y - K.IMP_MID) / K.IMP_WID))


def climate(year):
    return np.where(np.asarray(year) < K.SHIFT_YEAR, K.WET_PRE, K.WET_POST)


def water_year(d):
    return d.year + 1 if d.month >= 10 else d.year


def curve_number(imp, prior5):
    dcia = K.DCIA_SHARE * imp                            # the paved area piped straight to the creek
    cn = K.CN_PERV * (1 - dcia) + 98 * dcia
    if prior5 < 0.5:
        cn = cn / (2.281 - 0.01281 * cn)
    elif prior5 > 2.0:
        cn = cn / (0.427 + 0.00573 * cn)
    return min(cn, 98.0)


def runoff_in(p, cn):
    s = 1000 / cn - 10
    return (p - 0.2 * s) ** 2 / (p + 0.8 * s) if p > 0.2 * s else 0.0


def time_to_peak_h(imp):
    return K.TP_RURAL_H * (1 - K.LAG_DROP * (imp - K.IMP0) / (K.IMP1 - K.IMP0))


class World:
    def __init__(self, seed=K.SEED):
        self.seed = seed
        r = self.r = np.random.default_rng(seed)
        ndays = (D1 - D0).days + 1
        self.days = [D0 + dt.timedelta(days=i) for i in range(ndays)]
        rain = np.zeros(ndays)
        events = []                                      # (start index, length, depth, kind)
        i = 0
        while i < ndays:
            d = self.days[i]
            doy = d.timetuple().tm_yday
            p_start = 0.105 + 0.03 * np.cos(2 * np.pi * (doy - 200) / 365)
            if r.random() < p_start:
                trop_p = K.TROP_PRE if d.year < K.SHIFT_YEAR else K.TROP_POST
                tropical = 213 <= doy <= 300 and r.random() < trop_p
                if tropical:
                    depth = r.gamma(3.2, 1.25)
                    length = int(r.integers(1, 4))
                else:
                    depth = r.gamma(0.95, 0.62)
                    length = int(r.choice([1, 1, 1, 2, 2, 3]))
                depth *= float(climate(d.year))
                length = min(length, ndays - i)
                w = r.dirichlet(np.ones(length) * 1.6)
                rain[i:i + length] += depth * w
                events.append((i, length, depth, "tropical" if tropical else "frontal", float(w.max())))
                i += length + int(r.integers(3, 6))           # storms come at least three dry days apart
            else:
                i += 1
        # light rain on other days: no runoff, but the gauge's totals read like the Piedmont's 45 inches a year
        near = np.zeros(ndays, dtype=bool)                  # light rain keeps clear of the storms
        for (s0, ln, *_rest) in events:
            near[max(0, s0 - 3):min(ndays, s0 + ln + 3)] = True
        light = (rain == 0) & ~near & (r.random(ndays) < 0.62)
        rain[light] += np.round(r.gamma(0.8, 0.25, light.sum()), 2)
        self.rain = rain
        # runoff, instantaneous peaks and daily flows
        flow = np.zeros(ndays)
        seasonal = np.array([9 + 9 * np.cos(2 * np.pi * (d.timetuple().tm_yday - 45) / 365) for d in self.days])
        rb = np.random.default_rng(seed + 55)
        wob = np.exp(np.convolve(rb.normal(0, 0.06, ndays), np.ones(9) / 3.0, mode="same"))
        flow += np.maximum(0.6, seasonal * wob + 0.25 * np.convolve(rain, np.exp(-np.arange(20) / 6.0))[:ndays])
        self.events = []
        acre_ft_per_in = K.AREA_ACRES / 12.0
        for (s, length, depth, kind, wmax) in events:
            d = self.days[s]
            imp = float(imp_frac(d.year + (d.timetuple().tm_yday / 365.0)))
            prior5 = rain[max(0, s - 5):s].sum()
            wetness = 1.0
            q_in = K.RUNOFF_K * depth ** K.RUNOFF_EXP * wetness * (1 + K.VOL_RISE * (imp - K.IMP0))
            if q_in <= 0:
                continue
            tp = time_to_peak_h(imp)
            burst = 0.90 + 0.2 * wmax                   # rain packed into one day makes a sharper peak
            qp = 484 * K.AREA_SQMI * q_in / tp * burst * float(np.exp(r.normal(0, 0.09)))
            vol_cfs_days = q_in * acre_ft_per_in / 1.9835
            urban = (imp - K.IMP0) / (K.IMP1 - K.IMP0)
            spread = np.array([0.5 + 0.15 * urban, 0.32 - 0.08 * urban, 0.18 - 0.07 * urban])
            pk = s + length - 1                          # the creek peaks on the storm's last day of rain
            for j, f in enumerate(spread):
                if pk + j < ndays:
                    flow[pk + j] += vol_cfs_days * f
            hour = float(np.clip(r.normal(14, 5), 0.1, 23.9))
            self.events.append({"day": pk, "date": self.days[pk], "hour": hour, "depth": depth, "kind": kind,
                                "imp": imp, "runoff_in": q_in, "peak": qp, "start": s, "length": length})
        self.flow = flow
        wy = np.array([water_year(d) for d in self.days])
        self.wy = wy
        self.annual = {}
        for e in self.events:
            y = water_year(e["date"])
            if K.YEAR0 <= y <= K.YEAR1 and e["peak"] > self.annual.get(y, {"peak": 0})["peak"]:
                self.annual[y] = e
        for y in range(K.YEAR0, K.YEAR1 + 1):           # a year without a runoff event peaks on its baseflow
            if y not in self.annual:
                idx = np.nonzero(wy == y)[0]
                j = int(idx[np.argmax(flow[idx])])
                self.annual[y] = {"day": j, "date": self.days[j], "hour": 9.0, "depth": float(rain[j]),
                                  "kind": "none", "imp": float(imp_frac(self.days[j].year)), "runoff_in": 0.0,
                                  "peak": float(flow[j] * 1.25), "start": j, "length": 1}
