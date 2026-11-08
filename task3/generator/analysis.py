"""task3's golden, computed from the shipped pack alone, and the rival routes beside it for the checks.

The golden: each peak above base is paired with the rain gauge's storm total (the peak day and the two days before),
and each year's paved fraction is rebuilt from the stormwater parcels; regressing the log peak on the log storm total
and the paved fraction gives the response's rise with paving at a fixed storm; each annual peak is put on today's
watershed by that rise, and the 1 per cent flow is the log-Pearson III quantile of the adjusted series. The default
path fits the recorded annual peaks as they stand."""
import csv
import datetime as dt
import os

import numpy as np
from openpyxl import load_workbook
from scipy import stats

import common as K
import freq as FQ

AEP = K.DESIGN_AEP
STORM_MIN_IN = 1.0                     # the golden's pairs: storms of an inch or more


def read_rain(target):
    """Daily rain, one value a day: the gauge in service (TAM-RG-01 to 14 June 1987, then TAM-RG-02), an accumulated
    reading spread over the days it covers, missed days as dry."""
    rows = list(csv.DictReader(open(os.path.join(target, K.FILES["rain"]))))
    by = {}
    for r in rows:
        d = dt.date.fromisoformat(r["date"])
        in_service = "TAM-RG-01" if d < dt.date(1987, 6, 14) else "TAM-RG-02"
        if r["station_id"] != in_service:
            continue
        by[d] = r
    days = sorted(by)
    val = {}
    for i, d in enumerate(days):
        r = by[d]
        f = r["mflag"]
        if f.startswith("A") and len(f) > 1:
            k = int(f[1:])
            v = float(r["precip_in"]) / k
            for j in range(k):
                val[days[i - j]] = v
        elif f in ("A", "M"):
            val.setdefault(d, 0.0)
        else:
            val[d] = float(r["precip_in"]) if r["precip_in"] else 0.0
    return val


def storm_total(rain, d, before=2):
    return sum(rain.get(d - dt.timedelta(days=j), 0.0) for j in range(before + 1))


def read_peaks(target):
    out = {}
    for r in csv.DictReader(open(os.path.join(target, K.FILES["peaks"]))):
        out[int(r["water_year"])] = (dt.date.fromisoformat(r["peak_date"]), float(r["peak_cfs"]))
    return out


def read_pot(target):
    seen, out = set(), []
    for r in csv.DictReader(open(os.path.join(target, K.FILES["pot"]))):
        key = (r["peak_date"], r["peak_time"])
        if key in seen:                       # the 2009 and 2010 water years exported twice
            continue
        seen.add(key)
        out.append((int(r["water_year"]), dt.date.fromisoformat(r["peak_date"]), float(r["peak_cfs"])))
    return out


def paved_fraction(target, dedupe=True):
    """The Ollery basin's impervious area through each year, from the stormwater parcels (a split parcel carried under
    both numbers counted once), over the basin's area."""
    wb = load_workbook(os.path.join(target, K.FILES["parcels"]), read_only=True)
    ws = wb["billing_parcels"]
    rows = list(ws.iter_rows(min_row=2, values_only=True))
    area = None
    for r in wb["basins"].iter_rows(min_row=2, values_only=True):
        if r[0] == "OLL":
            area = float(r[2]) * 640 * 43560
    priors = {r[1] for r in rows if r[0] and r[1]}
    add = {}
    for pin, prior, basin, use, sq, yr, eru in rows:
        if basin != "OLL":
            continue
        if dedupe and not pin and prior in priors:
            continue
        add[int(yr)] = add.get(int(yr), 0) + float(sq)
    frac = {}
    tot = 0.0
    for y in range(1900, K.YEAR1 + 1):
        tot += add.get(y, 0.0)
        frac[y] = tot / area
    return frac


class Golden:
    def __init__(self, target):
        self.t = target
        self.rain = read_rain(target)
        self.peaks = read_peaks(target)
        self.pot = read_pot(target)
        self.frac = paved_fraction(target)
        self.years = np.arange(K.YEAR0, K.YEAR1 + 1)
        self.ann = np.array([self.peaks[y][1] for y in self.years])
        self.imp = np.array([self.frac[y] for y in self.years])

    def pairs(self, before=2, tmin=STORM_MIN_IN):
        P = np.array([storm_total(self.rain, d, before) for y, d, q in self.pot])
        q = np.array([q for y, d, q in self.pot])
        im = np.array([self.frac[y] for y, d, q_ in self.pot])
        m = P >= tmin
        return P[m], q[m], im[m]

    def response(self, before=2, tmin=STORM_MIN_IN):
        """The rise of log peak with the paved fraction at a fixed storm total."""
        P, q, im = self.pairs(before, tmin)
        X = np.column_stack([np.ones(len(P)), np.log(P), im])
        beta, *_ = np.linalg.lstsq(X, np.log(q), rcond=None)
        return float(beta[2]), len(P)

    def adjusted(self, c):
        return self.ann * np.exp(c * (self.imp[-1] - self.imp))

    def run(self):
        c, n_pairs = self.response()
        adj = self.adjusted(c)
        q1 = FQ.lp3_quantile(adj, AEP)
        pick = next(a for a in K.CULVERTS if a[2] >= q1)
        raw_q1 = FQ.lp3_quantile(self.ann, AEP)
        raw_pick = next(a for a in K.CULVERTS if a[2] >= raw_q1)
        tau, mk_p = stats.kendalltau(self.years, self.ann)
        order = np.argsort(-adj)
        storm = np.array([storm_total(self.rain, self.peaks[y][0]) for y in self.years])
        return {"years": self.years, "ann": self.ann, "imp": self.imp, "storm": storm,
                "dates": [self.peaks[y][0].isoformat() for y in self.years],
                "c": c, "n_pairs": n_pairs, "adj": adj, "q1": q1, "pick": pick, "raw_q1": raw_q1, "raw_pick": raw_pick,
                "mk_tau": tau, "mk_p": mk_p, "top5": [int(self.years[i]) for i in order[:5]],
                "raw_top5": [int(self.years[i]) for i in np.argsort(-self.ann)[:5]],
                "factor_1960": float(np.exp(c * (self.imp[-1] - self.imp[self.years == 1960][0]))),
                "imp_1956": float(self.imp[0]), "imp_2025": float(self.imp[-1]),
                "over_A_today": int((adj > K.CULVERTS[0][2]).sum()), "over_A_raw": int((self.ann > K.CULVERTS[0][2]).sum())}

    # ------------------------------------------------------------------ the rival routes, for the checks
    def rivals(self):
        f = {"lp3": FQ.lp3_quantile, "gev": FQ.gev_quantile}
        y, ann, imp = self.years, self.ann, self.imp
        out = {}
        for nm, fn in f.items():
            out["R0 all peaks " + nm] = fn(ann, AEP)
            out["R1 peaks since 1995 " + nm] = fn(ann[y >= 1995], AEP)
            out["R1 peaks since 2005 " + nm] = fn(ann[y >= 2005], AEP)
            b = np.polyfit(imp, np.log(ann), 1)
            out["R2 peaks regressed on paved fraction " + nm] = fn(ann * np.exp(b[0] * (imp[-1] - imp)), AEP)
            b = np.polyfit(y, np.log(ann), 1)
            out["R2 peaks detrended in time " + nm] = fn(ann * np.exp(b[0] * (y[-1] - y)), AEP)
        golden = {}
        for nm, fn in f.items():
            for before in (1, 2, 3):
                for tmin in (0.5, 1.0, 1.5, 2.0, 3.0):
                    c, n = self.response(before, tmin)
                    golden["G pairs %dd >=%.1f in %s" % (before + 1, tmin, nm)] = (fn(self.adjusted(c), AEP), c)
            # annual pairs only: each year's peak against its own storm and the year's paved fraction
            Pa = np.array([storm_total(self.rain, self.peaks[yy][0]) for yy in y])
            m = Pa >= 0.5
            X = np.column_stack([np.ones(m.sum()), np.log(Pa[m]), imp[m]])
            beta, *_ = np.linalg.lstsq(X, np.log(ann[m]), rcond=None)
            golden["G annual pairs " + nm] = (fn(self.adjusted(float(beta[2])), AEP), float(beta[2]))
            # decade effects at a fixed storm, the last decade as today
            P = np.array([storm_total(self.rain, d) for yy, d, q in self.pot]); q = np.array([q for yy, d, q in self.pot])
            yy = np.array([yy for yy, d, q_ in self.pot]); m = P >= 1.0
            dec = (yy[m] - 1) // 10 * 10 + 1
            levels = sorted(set(dec))
            X = np.column_stack([np.log(P[m])] + [(dec == L).astype(float) for L in levels])
            beta, *_ = np.linalg.lstsq(X, np.log(q[m]), rcond=None)
            eff = dict(zip(levels, beta[1:]))
            adj = np.array([a * np.exp(eff[levels[-1]] - eff[(v - 1) // 10 * 10 + 1]) for a, v in zip(ann, y)])
            golden["G decade effects " + nm] = (fn(adj, AEP), float("nan"))
        return out, golden
