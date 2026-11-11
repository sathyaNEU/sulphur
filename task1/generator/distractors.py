"""The neighbouring departments' files that sit in the same shared folder: print circulation by quarter, newsletter
sign-ups, the 2026 reader survey and digital advertising revenue. Each is the department's own export, about the
same titles and months; none of it enters the digital subscription figures."""
import numpy as np

import params as P
import pack as PK
import sim


def write(S, F, rng):
    n = {}
    rows = []
    base = {"BHR": 31800, "GAZ": 18400, "KBO": 16900, "ELN": 9100}
    for t in P.TITLES:
        lvl = base[t]
        for q in range(16):
            y, qq = 2023 + q // 4, q % 4 + 1
            lvl = lvl * (1 - float(rng.normal(0.012, 0.004)))
            abo = int(lvl * 0.86)
            single = int(lvl * 0.09 * (1.12 if qq == 4 else 1.0))
            epaper = int(lvl * 0.11 * (1 + 0.03 * q))
            rows.append(["%d-Q%d" % (y, qq), P.TITLE_NAME[t], abo, single, epaper, abo + single + epaper])
    n["print"] = PK.write_csv(F["print"], ["quarter", "title", "subscription_copies", "single_copy_sales",
                                            "epaper_copies", "paid_circulation"], rows)
    rows = []
    for m in range(24, P.CUT + 1):
        y, mo = sim.ym(m)
        for t in P.TITLES:
            for nl, w in [("Morgenbrief", 1.0), ("Sport am Abend", 0.45), ("Lokal kompakt", 0.6)]:
                k = int(rng.poisson(P.DIR_STARTS[t] * 2.6 * w * (1 + P.NEWS.get(m, 0))))
                rows.append(["%04d-%02d" % (y, mo), t, nl, k, int(rng.binomial(k, 0.21))])
    n["newsletter"] = PK.write_csv(F["newsletter"], ["month", "title", "newsletter", "signups", "unsubscribes"], rows)
    rows = []
    rid = rng.choice(np.arange(20000, 99999), size=1400, replace=False)
    for k in range(1400):
        t = P.TITLES[int(rng.choice(4, p=[0.42, 0.24, 0.21, 0.13]))]
        sub = rng.random() < 0.55
        sat = int(np.clip(rng.normal(3.6 if sub else 3.1, 0.9), 1, 5))
        price = int(np.clip(rng.normal(3.2 if sub else 2.4, 1.0), 1, 5))
        reasons = ["R01", "R02", "R03", "R04", "R05", "R06", "R07", "R08", "R99"]
        w = np.array([0.18, 0.14, 0.11, 0.09, 0.08, 0.07, 0.06, 0.05, 0.22]) * np.exp(rng.normal(0, 0.15, 9))
        rows.append([int(rid[k]), "2026-%02d-%02d" % (int(rng.integers(5, 7)), int(rng.integers(1, 29))), t,
                     "subscriber" if sub else "registered", sat, price, int(rng.integers(0, 2)),
                     reasons[int(rng.choice(9, p=w / w.sum()))], int(rng.integers(16, 82))])
    n["survey"] = PK.write_csv(F["survey"], ["response_id", "date", "title", "status", "satisfaction_1to5",
                                              "price_fair_1to5", "would_recommend", "main_reason_code", "age"], rows)
    rows = []
    for m in range(24, P.CUT + 1):
        y, mo = sim.ym(m)
        for t in P.TITLES:
            imp = P.DIR_STARTS[t] * 21000 * (1 + P.NEWS.get(m, 0)) * float(np.exp(rng.normal(0, 0.05)))
            cpm = {11: 3.9, 12: 4.4, 1: 2.2, 2: 2.4}.get(mo, 2.9) * float(np.exp(rng.normal(0, 0.04)))
            rows.append(["%04d-%02d" % (y, mo), t, int(imp), "%.2f" % cpm, "%.2f" % (imp / 1000 * cpm)])
    n["ads"] = PK.write_csv(F["ads"], ["month", "title", "impressions", "ecpm_eur", "revenue_eur"], rows)
    return n
