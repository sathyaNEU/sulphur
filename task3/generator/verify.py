"""task3 verifier: the load-bearing figures recomputed from the shipped files by code that shares nothing with
analysis.py (its own parsing, its own fits, its own weather-year loop), compared with figures.json.

    python3 task3/generator/verify.py
"""
import csv
import json
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TGT = os.path.join(os.path.dirname(HERE), "target")
F = json.load(open(os.path.join(HERE, "figures.json")))
OUT = []


def check(name, got, want, tol):
    OUT.append((name, abs(got - want) <= tol, got, want))


def stamp(s):
    y, mo, d = int(s[0:4]), int(s[5:7]), int(s[8:10])
    hh, mm = int(s[11:13]), int(s[14:16])
    return np.datetime64("%04d-%02d-%02dT%02d:%02d" % (y, mo, d, hh, mm))


def highs(name, col):
    t, h = [], []
    with open(os.path.join(TGT, name)) as f:
        r = csv.reader(f)
        next(r)
        for row in r:
            if row[2].strip().startswith("H"):
                t.append(stamp(row[0]))
                h.append(float(row[1]))
    return np.array(t), np.array(h)


def tide_year_of(t):
    y = t.astype("datetime64[Y]").astype(int) + 1970
    m = t.astype("datetime64[M]").astype(int) % 12 + 1
    return np.where(m >= 5, y, y - 1)


def days_at(t, h, thr):
    return len(set(t[h >= thr].astype("datetime64[D]").tolist()))


def main():
    to, ho = highs("8673718_high_low_1955-2026.csv", "Water Level")
    tp, hp = highs("8673718_high_low_predictions_1955-2028.csv", "Prediction")
    ty = tide_year_of(to)
    m25 = ty == 2025
    check("harbor 2025-26 days", days_at(to[m25], ho[m25], 8.6), F["harbor_2025"], 0)
    # monthly anomaly against the epoch and the seasonal cycle of the hourly predictions
    dat = {}
    for line in open(os.path.join(TGT, "8673718_datums.txt")):
        m = re.match(r"^(MSL|NAVD88)\s+(-?\d+\.\d+)", line)
        if m:
            dat[m.group(1)] = float(m.group(2))
    pred_by_month = {}
    with open(os.path.join(TGT, "8673718_hourly_heights_2000-2026.csv")) as f:
        r = csv.reader(f)
        next(r)
        tot = np.zeros(13)
        cnt = np.zeros(13)
        for row in r:
            mo = int(row[0][5:7])
            tot[mo] += float(row[2])
            cnt[mo] += 1
    seas = tot[1:] / cnt[1:]
    seas = seas - (tot[1:].sum() / cnt[1:].sum())
    anom = {}
    with open(os.path.join(TGT, "8673718_monthly_means_1955-2026.csv")) as f:
        r = csv.reader(f, skipinitialspace=True)
        next(r)
        for row in r:
            if row[5].strip():
                anom[(int(row[0]), int(row[1]))] = float(row[5]) - dat["MSL"] - seas[int(row[1]) - 1]
    A = {}
    for (y, mo), a in anom.items():
        k = y if mo >= 5 else y - 1
        A.setdefault(k, []).append(a)
    A = {k: np.mean(v) for k, v in A.items()}
    check("2025-26 mean sea level above the epoch", A[2025], F["A25"], 0.006)
    # residual at each observed high water: nearest prediction within three hours, less its tide year's mean
    tpi = tp.astype("datetime64[m]").astype(np.int64)
    toi = to.astype("datetime64[m]").astype(np.int64)
    j = np.clip(np.searchsorted(tpi, toi), 1, len(tpi) - 1)
    jl = np.where(np.abs(tpi[j - 1] - toi) < np.abs(tpi[j] - toi), j - 1, j)
    keep = np.abs(tpi[jl] - toi) <= 180
    res_t = tp[jl][keep]
    res = ho[keep] - hp[jl][keep] - np.array([A.get(int(y), np.nan) for y in ty[keep]])
    res_ty = tide_year_of(res_t)
    fut = (tp >= np.datetime64("2027-05-01")) & (tp < np.datetime64("2028-05-01"))
    ft, fh = tp[fut], hp[fut]
    ftau = (ft - np.datetime64("2027-05-01T00:00")).astype("timedelta64[m]").astype(float) / 60.0
    counts = []
    for y in range(1990, 2026):
        m = res_ty == y
        tau = (res_t[m] - np.datetime64("%d-05-01T00:00" % y)).astype("timedelta64[m]").astype(float) / 60.0
        rr = np.interp(ftau, tau, res[m])
        counts.append(days_at(ft, fh + 0.70 + rr, 8.6))
    check("harbor expected days 2027-28", float(np.mean(counts)), F["harbor_exp"], 0.06)
    check("harbor range low", float(np.percentile(counts, 5)), F["harbor_lo"], 0.6)
    check("harbor range high", float(np.percentile(counts, 95)), F["harbor_hi"], 0.6)
    # Marsh Road: hinge by a fine grid on its own pairing
    def logger(name):
        with open(os.path.join(TGT, name), encoding="utf-8") as f:
            f.readline()
            off = int(re.search(r"GMT([+-]\d+)", f.readline()).group(1))
            tt, vv = [], []
            for row in csv.reader(f):
                mo, d, yy = row[1][0:2], row[1][3:5], row[1][6:8]
                hh, mi = int(row[1][9:11]) % 12, int(row[1][12:14])
                if row[1].endswith("PM"):
                    hh += 12
                tt.append(np.datetime64("20%s-%s-%sT%02d:%02d" % (yy, mo, d, hh, mi)) - np.timedelta64(off + 5, "h"))
                vv.append(float(row[2]))
        return np.array(tt), np.array(vv)
    lt, lv = logger("PEL-MR-24.csv")
    pk = [i for i in range(2, len(lv) - 2) if lv[i] == lv[i - 2:i + 3].max() and lv[i] > lv.mean()]
    sel = []
    for i in pk:
        if sel and (lt[i] - lt[sel[-1]]) < np.timedelta64(8, "h"):
            if lv[i] > lv[sel[-1]]:
                sel[-1] = i
            continue
        sel.append(i)
    st, sv = lt[sel], lv[sel] + dat["NAVD88"]
    sti = st.astype("datetime64[m]").astype(np.int64)
    k = np.clip(np.searchsorted(toi, sti), 1, len(toi) - 1)
    kl = np.where(np.abs(toi[k - 1] - sti) < np.abs(toi[k] - sti), k - 1, k)
    ok_ = np.abs(toi[kl] - sti) <= 180
    x, y = ho[kl][ok_], sv[ok_]
    best = None
    for P in np.arange(6.6, 8.6, 0.005):
        X = np.column_stack([np.ones(len(x)), x, np.maximum(x - P, 0)])
        co = np.linalg.lstsq(X, y, rcond=None)[0]
        e = ((X @ co - y) ** 2).sum()
        if best is None or e < best[0]:
            best = (e, P, co)
    _, P, co = best
    from openpyxl import load_workbook
    ws = load_workbook(os.path.join(TGT, "tidal_low_points_inventory_2026-10.xlsx"), read_only=True)["Low points"]
    lane = [r[9] for r in ws.iter_rows(min_row=2, values_only=True) if r[0] == "LP-02"][0] + dat["NAVD88"]
    Hs = np.arange(7.0, 11.0, 0.0005)
    Hstar = Hs[np.argmax(co[0] + co[1] * Hs + co[2] * np.maximum(Hs - P, 0) >= lane)]
    check("Marsh Road flooding high water", float(Hstar), F["marsh_Hstar"], 0.02)
    check("Marsh Road 2025-26 days", days_at(to[m25], ho[m25], Hstar), F["hind"]["marsh"], 1)
    for name, ok_v, got, want in OUT:
        print("%s  %-36s %10.3f  figures.json %10.3f" % ("PASS" if ok_v else "FAIL", name, got, want))
    nf = sum(1 for o in OUT if not o[1])
    print("verify: %d figures, %d FAIL" % (len(OUT), nf))
    return 1 if nf else 0


if __name__ == "__main__":
    sys.exit(main())
