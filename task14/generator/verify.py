"""task14: an independent path from the shipped files to the graded figures. It shares only the conformed register
(conform.py: the two systems joined, rents weekly, dwellings linked); every step after it is written again here
without measure.py or project.py: each tenancy's span (2.2), the rent panel's anniversary pairs and rates, the rent
payable on a day, the matched dwellings and their ratio of totals (2.4, 2.5), the counts, the group contributions,
the register read as it stands on 31 December, and the operators' review rules from their own bonds and the CPI
release. Every figure is compared with figures.json at the precision the answer blocks state.

    python3 task14/generator/verify.py
"""
import datetime as dt
import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import warnings  # noqa: E402

warnings.filterwarnings("ignore")
import conform as CF  # noqa: E402

REG = ["HC", "HN", "HE", "HS", "KC", "MV", "WS"]
EP0 = dt.date(1970, 1, 1)
FAILS = []


def d(y, m, dd):
    return (dt.date(y, m, dd) - EP0).days


def check(name, ok, detail=""):
    print("%s  %s%s" % ("PASS" if ok else "FAIL", name, (": " + str(detail)) if detail != "" else ""))
    if not ok:
        FAILS.append(name)


def r1(x):
    return float(round(x + 1e-12, 1))


def anniv_days(start, y):
    s = EP0 + dt.timedelta(days=int(start))
    try:
        return (dt.date(y, s.month, s.day) - EP0).days
    except ValueError:
        return (dt.date(y, s.month, 28) - EP0).days


def main():
    target = os.path.join(TASK, "target")
    F = json.load(open(os.path.join(HERE, "figures.json")))
    D = CF.load(target)
    T, tops, _ = CF.conform(D, "golden")
    T = T.reset_index(drop=True)
    # ------------------------------------------------------------ spans (2.2), written again
    T = T.sort_values(["dwelling", "start", "lodged"], kind="stable").reset_index(drop=True)
    end = np.full(len(T), np.inf)
    ref = T["refund"].values
    st = T["start"].values
    dw = T["dwelling"].values
    for i in range(len(T)):
        e = ref[i] - 1 if not np.isnan(ref[i]) else np.inf
        if i + 1 < len(T) and dw[i + 1] == dw[i]:
            e = min(e, st[i + 1] - 1)
        end[i] = e
    T["vend"] = end

    def on(t):
        m = T[(T["start"] <= t) & (T["vend"] >= t)]
        return m.sort_values(["dwelling", "start"]).drop_duplicates("dwelling", keep="last")

    # ------------------------------------------------------------ the panel's anniversary pairs and rates
    PN = D["PN"]
    R = PN[PN["response"] == "R"].copy()
    R["rd"] = (pd.to_datetime(R["reference_date"]) - pd.Timestamp("1970-01-01")).dt.days
    R["sd"] = (pd.to_datetime(R["tenancy_start"]) - pd.Timestamp("1970-01-01")).dt.days
    R = R.sort_values(["dwelling_ref", "rd"])
    rows = []
    for ref_, g in R.groupby("dwelling_ref"):
        rd, sd, rent = g["rd"].values, g["sd"].values, g["weekly_rent"].astype(float).values
        reg, w = g["region"].values, g["design_weight"].astype(float).values
        for k in range(len(g) - 1):
            if sd[k] != sd[k + 1]:
                continue
            y0 = (EP0 + dt.timedelta(days=int(sd[k]))).year
            hits = [y for y in range((EP0 + dt.timedelta(days=int(rd[k]))).year,
                                     (EP0 + dt.timedelta(days=int(rd[k + 1]))).year + 1)
                    if y > y0 and rd[k] < anniv_days(sd[k], y) <= rd[k + 1]]
            if len(hits) == 1:
                rows.append((hits[0], reg[k], w[k], rent[k + 1] / rent[k]))
    PP = pd.DataFrame(rows, columns=["year", "region", "w", "f"])
    check("panel anniversary pairs", len(PP) == F["panel_pairs"], "%d against %d" % (len(PP), F["panel_pairs"]))
    m, p = {}, {}
    for y in range(2018, 2027):
        s = PP[PP["year"] == y]
        nm = np.average(s["f"], weights=s["w"])
        npr = np.average(s["f"] > 1 + 1e-9, weights=s["w"])
        for rg in REG:
            ss = s[s["region"] == rg]
            m[(y, rg)] = np.average(ss["f"], weights=ss["w"]) if len(ss) >= 20 else nm
            p[(y, rg)] = np.average(ss["f"] > 1 + 1e-9, weights=ss["w"]) if len(ss) >= 20 else npr

    def mf(y, rg):
        return m[(min(max(y, 2018), 2026), rg)]

    def pr(y, rg):
        return p[(min(max(y, 2018), 2026), rg)]

    # ------------------------------------------------------------ rent payable on a day
    tops = tops.copy()
    tops["when"] = np.where(tops["effective"].notna(), tops["effective"], tops["day"])
    tops = tops.sort_values(["key", "when"], kind="stable")
    tk = {k: (g["when"].values, g["rent"].values) for k, g in tops.groupby("key")}

    def recorded(key, rent0, t):
        if key not in tk:
            return rent0
        wh, rr = tk[key]
        j = np.searchsorted(wh, t, side="right") - 1
        return rr[j] if j >= 0 else rent0

    def rent(row, t):
        if row.operator:
            return recorded(row.key, row.rent0, t)
        y0 = (EP0 + dt.timedelta(days=int(row.start))).year
        f = 1.0
        for y in range(y0 + 1, (EP0 + dt.timedelta(days=int(t))).year + 1):
            if anniv_days(row.start, y) <= t:
                f *= mf(y, row.region)
        return row.rent0 * f

    def compare(t2, t1, groups=False, share=False):
        A, B = on(t1).set_index("dwelling"), on(t2).set_index("dwelling")
        c = A.index.intersection(B.index)
        A, B = A.loc[c], B.loc[c]
        r1_ = np.array([rent(x, t1) for x in A.itertuples()])
        r2_ = np.array([rent(x, t2) for x in B.itertuples()])
        same = A["key"].values == B["key"].values
        out = {"NAT": 100 * (r2_.sum() / r1_.sum() - 1), "n_relet": int((~same).sum()),
               "same": 100 * (r2_[same].sum() / r1_[same].sum() - 1),
               "relet": 100 * (r2_[~same].sum() / r1_[~same].sum() - 1),
               "c_same": 100 * (r2_[same] - r1_[same]).sum() / r1_.sum(),
               "c_relet": 100 * (r2_[~same] - r1_[~same]).sum() / r1_.sum()}
        if groups:
            reg = B["region"].values
            for rg in REG:
                k = reg == rg
                out[rg] = 100 * (r2_[k].sum() / r1_[k].sum() - 1)
                out["relet_" + rg] = int((k & ~same).sum())
        if share:
            S = A[same]
            sh = []
            for x, rr2, rr1 in zip(S.itertuples(), r2_[same], r1_[same]):
                if x.operator:
                    sh.append(float(rr2 > rr1 + 1e-9))
                else:
                    md = (EP0 + dt.timedelta(days=int(x.start)))
                    yy = (EP0 + dt.timedelta(days=int(t2))).year
                    ya = yy if anniv_days(x.start, yy) <= t2 else yy - 1
                    ya = max(ya, md.year)
                    sh.append(pr(ya, x.region))
            out["share"] = 100 * float(np.mean(sh))
        return out

    s26, s25, s24 = d(2026, 9, 30), d(2025, 9, 30), d(2024, 9, 30)
    held = on(s26)
    check("tenancies held on 30 September 2026", len(held) == F["held"]["NAT"], "%d against %d" % (len(held),
                                                                                                F["held"]["NAT"]))
    for rg in REG:
        n = int((held["region"] == rg).sum())
        check("held in %s" % rg, n == F["held"][rg], "%d against %d" % (n, F["held"][rg]))
    c = compare(s26, s25, groups=True, share=True)
    check("re-lettings", c["n_relet"] == F["relet_n"]["NAT"], "%d against %d" % (c["n_relet"], F["relet_n"]["NAT"]))
    for rg in REG:
        check("re-lettings in %s" % rg, c["relet_" + rg] == F["relet_n"][rg])
    check("September 2026 national", r1(c["NAT"]) == F["sep26"]["NAT"], "%.3f" % c["NAT"])
    for rg in REG:
        check("September 2026 %s" % rg, abs(r1(c[rg]) - F["sep26"][rg]) <= 0.1 + 1e-9, "%.3f against %.1f" % (
            c[rg], F["sep26"][rg]))
    check("continuing change", r1(c["same"]) == F["cont_change"], "%.3f" % c["same"])
    check("continuing share with a rise", abs(c["share"] - F["cont_share"]) <= 0.1, "%.2f" % c["share"])
    check("re-letting change", r1(c["relet"]) == F["relet_change"], "%.3f" % c["relet"])
    c25 = compare(s25, s24)
    check("contributions to September 2026", abs(round(c["c_same"], 2) - F["contrib26"]["continuing"]) <= 0.011 and
          abs(round(c["c_relet"], 2) - F["contrib26"]["relet"]) <= 0.011, "%.3f, %.3f" % (c["c_same"], c["c_relet"]))
    check("September 2025 national", r1(c25["NAT"]) == F["sep25"], "%.3f" % c25["NAT"])
    for q in ("2022Q1", "2023Q4", "2024Q4"):
        y, qq = int(q[:4]), int(q[-1])
        t2 = {1: d(y, 3, 31), 2: d(y, 6, 30), 3: d(y, 9, 30), 4: d(y, 12, 31)}[qq]
        t1 = {1: d(y - 1, 3, 31), 2: d(y - 1, 6, 30), 3: d(y - 1, 9, 30), 4: d(y - 1, 12, 31)}[qq]
        v = compare(t2, t1)["NAT"]
        check("back series %s" % q, abs(r1(v) - F["series"][q]) <= 0.1 + 1e-9, "%.3f against %.1f" % (v, F["series"][q]))
    st31 = compare(d(2026, 12, 31), d(2025, 12, 31))["NAT"]
    check("the register read as it stands on 31 December 2026", r1(st31) == F["asstands_dec26"], "%.3f" % st31)
    # ------------------------------------------------------------ the operators' review rules
    O = D["O"]
    tu = O[(O["event"] == "TOPUP") & (O["rent_effective_from"].fillna("") != "")].copy()
    tu["eff"] = pd.to_datetime(tu["rent_effective_from"])
    tu["md"] = tu["eff"].dt.strftime("%m-%d")
    ops = set(T[T["operator"]]["landlord_id"].unique())
    owner = O[O["event"].isin(["LODGE", "MIGRATED"])].set_index("bond_id")["landlord_id"].to_dict()
    tu = tu[tu["bond_id"].map(owner).isin(ops)]
    cpi = D["CPI"]
    lodge = O[O["event"].isin(["LODGE", "MIGRATED"])].set_index("bond_id")["weekly_rent"].astype(float).to_dict()
    tu = tu.sort_values(["bond_id", "eff"])
    tu["prev"] = tu.groupby("bond_id")["weekly_rent"].shift(1).astype(float)
    tu["prev"] = tu["prev"].fillna(tu["bond_id"].map(lodge))
    tu["rise"] = 100 * (tu["weekly_rent"].astype(float) / tu["prev"] - 1)
    for md, label in (("12-01", "a"), ("11-01", "b")):
        s = tu[tu["md"] == md]
        by = s.groupby(s["eff"].dt.year)["rise"].median()
        for y in (2023, 2024, 2025):
            check("%s review %d" % (label, y), abs(r1(by[y]) - F["%s_review" % label][str(y)]) <= 0.1,
                  "%.2f against %.1f" % (by[y], F["%s_review" % label][str(y)]))
        marg = np.mean([by[y] - cpi[(y, 3)] for y in (2023, 2024, 2025)])
        check("%s review margin over the September CPI" % label, abs(r1(marg) - F["%s_margin" % label]) <= 0.1,
              "%.2f" % marg)
        if label == "a":
            check("Harbourline's 2026 review from its rule", r1(cpi[(2026, 3)] + marg) == F["a_review_2026"],
                  "%.2f" % (cpi[(2026, 3)] + marg))
            check("no Harbourline review of 1 December 2026 on file", int((s["eff"].dt.year == 2026).sum()) == 0)
        else:
            check("Quayside's 2026 review on its lodged bonds", abs(r1(by[2026]) - F["b_review_2026"]) <= 0.1,
                  "%.2f" % by[2026])
            check("Quayside's 2026 bonds on file", int((s["eff"].dt.year == 2026).sum()) == F["reviewed_onfile_n"])
    print("%d failed" % len(FAILS))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
