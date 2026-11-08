"""task7 verifier: the plan figure, the split, the five facilities and the CSV recomputed from target/ with pandas,
sharing no code with golden.py, and compared with the golden deliverables and figures.json. Exit 1 on any mismatch.

    python3 verify.py [target_dir] [task_dir]
"""
import json
import os
import re
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
REPORT, AS_IF = pd.Timestamp("2026-12-31"), pd.Timestamp("2027-01-01")
HAIRCUT = 0.22
OWN = "Owner-occupied"


def master_scale(target):
    from pypdf import PdfReader
    text = " ".join(" ".join((p.extract_text() or "").split())
                    for p in PdfReader(os.path.join(target, "ardcarn_credit_risk_policy_part4_2025.pdf")).pages)
    body = text.split("Twelve-month probability of default", 1)[1]
    pairs = re.findall(r"\b([1-8]) (\d+\.\d+)%", body)
    scale = {}
    for g, v in pairs:
        if int(g) not in scale:
            scale[int(g)] = float(v) / 100
    assert sorted(scale) == list(range(1, 9)), scale
    return scale


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target")
    task = sys.argv[2] if len(sys.argv) > 2 else TASK
    pd_scale = master_scale(target)

    v = pd.read_csv(os.path.join(target, "dw_dim_property_valuation_2004_2026.csv"), dtype=str).drop_duplicates()
    v["eff"] = pd.to_datetime(v["row_effective_date"])
    v["exp"] = pd.to_datetime(v["row_expiry_date"].replace("9999-12-31", "2262-04-11"))
    v = v[v["exp"] >= v["eff"]].copy()
    v["basis"] = v["valuation_basis"].map({"FULL": "I", "INSPECTION": "I", "IDX": "X", "INDEX ROLL-FORWARD": "X"})
    v["vdate"] = pd.to_datetime(v["valuation_date"])
    v["value"] = v["market_value_eur"].astype(float)
    v = v.sort_values(["property_id", "eff", "vdate"]).reset_index(drop=True)
    by_p = {p: g for p, g in v.groupby("property_id")}

    def in_force(p, day):
        g = by_p[p]
        g = g[(g["eff"] <= day) & (g["exp"] >= day)]
        return g.iloc[-1] if len(g) else None

    def anchor(p, row):
        if row["basis"] == "I":
            return row
        g = by_p[p]
        g = g[(g["basis"] == "I") & (g["vdate"] <= row["vdate"]) & (g["eff"] <= row["eff"])]
        return g.sort_values(["vdate", "eff"]).iloc[-1] if len(g) else None

    reg = pd.read_excel(os.path.join(target, "facility_register_2026-12.xlsx"), sheet_name="Facilities", dtype=str)
    book = dict(zip(reg["facility_no"], reg["lending_book"]))
    legacy = reg.dropna(subset=["legacy_facility_no"])
    book.update(dict(zip(legacy["legacy_facility_no"], legacy["lending_book"])))

    br = pd.read_csv(os.path.join(target, "dw_bridge_facility_security_2026-12.csv"), dtype=str)
    br["eff"] = pd.to_datetime(br["row_effective_date"])
    br["exp"] = pd.to_datetime(br["row_expiry_date"].replace("9999-12-31", "2262-04-11"))

    # the record
    dfl = pd.read_csv(os.path.join(target, "default_register_2012_2026.csv"), dtype=str)
    dfl["d"] = pd.to_datetime(dfl["default_date"])
    first = dfl.groupby("facility_no", sort=False)["d"].min()
    order = list(dict.fromkeys(dfl["facility_no"]))
    rec, seen = [], set()
    for f in order:
        d = first[f]
        props = br[(br["facility_no"] == f) & (br["eff"] <= d) & (br["exp"] >= d)]["property_id"].tolist()
        for p in props:
            if p in seen or p not in by_p:
                continue
            g = by_p[p]
            ins = g[(g["basis"] == "I") & (g["vdate"] >= d) & (g["vdate"] <= d + pd.Timedelta(days=92))]
            if not len(ins):
                continue
            car = in_force(p, d)
            if car is None:
                continue
            a = anchor(p, car)
            if a is None or a["vdate"] >= d:
                continue
            seen.add(p)
            rec.append(dict(tau=(d - a["vdate"]).days / 365.25, ratio=ins.iloc[0]["value"] / car["value"], book=book.get(f)))
    rec = pd.DataFrame(rec)
    fit = {}
    for own in (True, False):
        r = rec[(rec["book"] == OWN) == own]
        X = np.c_[np.ones(len(r)), r["tau"].values]
        y = np.log(r["ratio"].values)
        c = np.linalg.lstsq(X, y, rcond=None)[0]
        fit[own] = (c[0], c[1], float(np.mean(np.exp(y - X @ c))))

    # the year-end performing book
    fact = pd.read_csv(os.path.join(target, "dw_fact_loan_month_end_2022_2026.csv"), dtype=str)
    ye = fact[(fact["month_end_key"] == "20261231") & (fact["default_flag"] == "N")].copy()
    ye["ead"] = ye["balance_eur"].astype(float)
    sec = br[(br["eff"] <= REPORT) & (br["exp"] >= REPORT)]
    sec = sec.merge(ye[["facility_no", "ead"]], on="facility_no")
    sec["share"] = sec["ead"] / sec.groupby("property_id")["ead"].transform("sum")
    names = {"INV": "Investment", "OWN": OWN}
    rows = []
    for _, r in ye.iterrows():
        vexp = carried = 0.0
        for _, s in sec[sec["facility_no"] == r["facility_no"]].iterrows():
            car = in_force(s["property_id"], REPORT)
            a = anchor(s["property_id"], car)
            tau = (AS_IF - a["vdate"]).days / 365.25
            bk = names[r["lending_book"]]
            a0, b0, sm = fit[bk == OWN]
            carried += car["value"] * s["share"]
            vexp += car["value"] * s["share"] * np.exp(a0 + b0 * tau) * sm
        pdv = pd_scale[int(r["internal_grade"])]
        lgd = max(0.0, r["ead"] - (1 - HAIRCUT) * vexp) / r["ead"]
        rows.append(dict(facility_no=r["facility_no"], book=names[r["lending_book"]], el=pdv * lgd * r["ead"]))
    out = pd.DataFrame(rows).sort_values(["el", "facility_no"], ascending=[False, True])

    total, inv = out["el"].sum(), out.loc[out["book"] == "Investment", "el"].sum()
    occ = out.loc[out["book"] == OWN, "el"].sum()
    five = sorted(out["facility_no"].head(5))
    F = json.load(open(os.path.join(task, "generator", "figures.json")))
    csv = pd.read_csv(os.path.join(task, "golden", "cre_expected_loss_2027_by_loan.csv"), dtype={"facility_no": str})
    rnd = lambda x, u: round(x / u) * u
    checks = [
        ("plan figure", rnd(total, 500000), F["call"]["plan_figure_eur"]),
        ("plan figure unrounded", round(total), F["call"]["plan_figure_unrounded_eur"]),
        ("investment", rnd(inv, 250000), F["asks"]["investment_eur"]),
        ("owner-occupied", rnd(occ, 250000), F["asks"]["owner_occupied_eur"]),
        ("five facilities", five, F["asks"]["five_facilities"]),
        ("CSV rows", len(out), len(csv)),
        ("CSV total (rows to the euro)", int(sum(round(x) for x in out["el"])), int(csv["expected_loss_2027_eur"].sum())),
        ("CSV total stated", int(csv["expected_loss_2027_eur"].sum()), F["asks"]["csv_total_eur"]),
        ("CSV first row", out.iloc[0]["facility_no"], csv.iloc[0]["facility_no"]),
        ("record size", len(rec), F["components"]["record_defaults"]),
    ]
    bad = 0
    for name, got, want in checks:
        ok = got == want
        bad += not ok
        print("%s  %s: %s%s" % ("PASS" if ok else "FAIL", name, got, "" if ok else " (figures.json or golden: %s)" % (want,)))
    print("verify: %d checks, %d failed" % (len(checks), bad))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
