"""task20 checks: the cut pack against the clean truth (the simulated world before any file was written), the bar
block R1 to R7 (dataset-generation 7.1), every fork in the design note's fork table (SF1 to SF23), and the realism
sweep. Exit 1 on any failure.

    python3 task20/generator/checks.py
"""
import json
import os
import re
import subprocess
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TGT = os.path.join(TASK, "target")
sys.path.insert(0, HERE)
import analysis as A  # noqa: E402
import pack as PK  # noqa: E402
import world as W  # noqa: E402

FAILS = []


def check(label, ok, detail=""):
    print("%s  %s%s" % ("PASS" if ok else "FAIL", label, ("  (" + detail + ")") if detail else ""))
    if not ok:
        FAILS.append(label)


def inside(v, b):
    return b[0] <= v <= b[1]


def pack_text():
    out = {}
    for f in sorted(os.listdir(TGT)):
        p = os.path.join(TGT, f)
        if f.endswith(".pdf"):
            out[f] = subprocess.run(["pdftotext", "-layout", p, "-"], capture_output=True, text=True).stdout
        elif f.endswith(".xlsx"):
            import openpyxl
            wb = openpyxl.load_workbook(p, read_only=True)
            out[f] = " ".join(str(c) for ws in wb.worksheets for row in ws.iter_rows(values_only=True) for c in row
                              if c is not None)
        else:
            out[f] = open(p, errors="ignore").read()
    return out


def main():
    R = A.full(TGT)
    P = R["P"]
    w = W.simulate(PK.SEED)
    F = json.load(open(os.path.join(HERE, "figures.json")))
    E = json.load(open(os.path.join(HERE, "effort.json")))
    B = F["bands"]
    street = R["street"]
    G = R["golden"]
    fam = R["family"]
    S = R["shortcuts"]
    X = R["ruled_out"]
    V = R["variants"]
    res = P["results"].set_index("fiscal_quarter")

    # ------------------------------------------------------------------------------- the pack against the clean truth
    tq = W.QKEYS.index("FY2025Q4")
    bq = W.QKEYS.index("FY2024Q4")
    truth = w.rev_q[tq] / w.rev_q[bq] - 1
    check("C1 the golden's growth sits within 0.5 points of the world's fourth-quarter growth",
          abs(G["growth"] - truth) < 0.005, "golden %.2f%%, world %.2f%%" % (100 * G["growth"], 100 * truth))
    check("C2 the world's fourth-quarter net sales sit inside the golden's 80 per cent range",
          G["low"] <= w.rev_q[tq] <= G["high"], "%.1f in %.1f to %.1f" % (w.rev_q[tq], G["low"], G["high"]))
    lag0 = {PK.ISSUER_CODES[k]: v for k, v in zip(w.issuers, w.lag0)}
    dev = max(abs(R["cf"][(i, 0)] - lag0[i]) for i in lag0 if (i, 0) in R["cf"])
    check("C3 each issuer's lag-0 completion factor from the delivery history recovers the world's within 0.015",
          dev < 0.015, "max deviation %.4f" % dev)
    sel = W.QIDX == tq
    lic = w.spend[sel][:, :, [4, 5]].sum()
    brand = w.spend[sel][:, :, [0, 1, 4, 5]].sum()
    check("C4 the descriptor detail's excluded share matches the world's licensed and cafe share of the brand id",
          abs(R["excluded_share"] - lic / brand) < 0.003, "%.4f against %.4f" % (R["excluded_share"], lic / brand))
    worst = 0.0
    for n, k in enumerate(W.QKEYS[:-1]):
        kk = k.replace("Q", " Q")
        worst = max(worst, abs(res.net_sales[kk] - w.rev_q[n]), abs(res.contract[kk] - w.contract_q[n]),
                    abs(res.fern[kk] - w.fern_q[n]), abs(P["deposits"][kk] - w.dep_q[n]))
    check("C5 the releases' net sales, contract, Fernhollow and deposits, as read (fourth quarters by subtraction), are "
          "the world's to rounding", worst < 0.003, "largest gap USD %.4f m" % worst)
    reg = P["regions"].set_index("fiscal_year")
    worst = 0.0
    for fy in reg.index:
        qs = [k for k in res.index if k.startswith(fy) and pd.notna(res.net_sales[k])]
        brand_q = sum(res.net_sales[k] - res.contract[k] - res.fern[k] for k in qs)
        worst = max(worst, abs(brand_q - float(reg.loc[fy].sum())))
    check("C6 the 10-K's regional table adds to the quarters' Brindle & Moss net sales within rounding", worst <= 0.35,
          "largest gap USD %.2f m" % worst)
    pan = R["pan"]
    comp = pan[pan.fq == "FY2025 Q4"].spend_usd.sum()
    world_q = w.spend[sel][:, :, [0, 1, 2, 3]].sum()
    check("C7 the completed entity spend for the quarter is within 1 per cent of the world's complete spend",
          abs(comp / world_q - 1) < 0.01, "%.3f%%" % (100 * (comp / world_q - 1)))
    rs = R["reissues"]
    want = {PK.ISSUER_CODES[cv["to"]]: cv["waves"] for cv in w.conversions}
    ok = set(rs) == set(want) and all(
        min(abs((x - W.CAL.week_start.iloc[want[i][0]]).days) for x in rs[i]) <= 14 for i in rs)
    check("C8 the four-week card rise finds the world's two re-issued books and nothing else",
          ok, "; ".join("%s %s to %s" % (i, rs[i][0].date(), rs[i][-1].date()) for i in sorted(rs)))
    check("C9 the quarter-end deposits estimate is within USD 10 million of the world's",
          abs(R["dep_q4_est"] - w.dep_q[tq]) < 10.0, "%.1f against %.1f" % (R["dep_q4_est"], w.dep_q[tq]))
    check("C10 the contract run rate is within USD 4 million of the world's fourth-quarter contract sales",
          abs(R["ct_hat"] - w.contract_q[tq]) < 4.0, "%.1f against %.1f" % (R["ct_hat"], w.contract_q[tq]))

    # ---------------------------------------------------------------------------------------------- the bar block
    files = sorted(os.listdir(TGT))
    cats = {"spreadsheet" if f.endswith((".csv", ".xlsx")) else "text" for f in files}
    check("R1a the field's raw material: ten or more files in two or more categories", len(files) >= 10 and len(cats) >= 2,
          "%d files, %s" % (len(files), sorted(cats)))
    n_panel, n_desc = len(P["panel"]), len(P["desc"])
    check("R1b two large CSVs: the panel of 20,000 rows or more and the descriptor detail of 10 printed pages or more",
          n_panel >= 20000 and n_desc >= 500, "%d and %d rows" % (n_panel, n_desc))
    check("R2a the 53-week fiscal 2023 is read on weekly averages; the target quarter and its base are 13 weeks each",
          int(res.weeks["FY2025 Q4"]) == 13 and int(res.weeks["FY2024 Q4"]) == 13 and int(res.weeks["FY2023 Q4"]) == 14)
    paypal = P["desc"][P["desc"].descriptor.str.startswith("PAYPAL")]
    check("R2b the site's payment-facilitator descriptor is in every month of both quarters (neutral to growth)",
          paypal.month.isin(["2024-11", "2024-12", "2025-01", "2025-11", "2025-12", "2026-01"]).sum() == 6)
    raw = pd.read_csv(os.path.join(TGT, PK.F_PANEL), usecols=["issuer_code", "billing_region"]).drop_duplicates()
    check("R2c the feeds' region labels (%d spellings) map to the four regions, four for every issuer" % raw.billing_region.nunique(),
          raw.billing_region.nunique() >= 12 and all(len(g) == 4 for _, g in raw.groupby("issuer_code"))
          and set(raw.billing_region.map(A.norm_region)) == set(A.REGIONS))
    c = S["careful"]
    check("R3a the careful pass's figures sit outside R2, R4, R5, R7 and R9's bands",
          not inside(F["visible_with_ks01_pct"], B["visible_growth_pct"])
          and not inside(0.0, B["bridge_pp"]["revenue on delivery"])
          and not inside(0.0, B["bridge_pp"]["contract at its run rate"])
          and not inside(round(c["forecast"], 1), B["forecast_m"]) and A.call_of(c, street) != "short")
    q = S["quick"]
    check("R3b the quick pass's figures sit outside R1 and R7's bands",
          not inside(0.0, B["bridge_pp"]["the latest weeks completed"]) and not inside(round(q["forecast"], 1), B["forecast_m"])
          and q["forecast"] > street)
    for k in ("careful", "careful_regressed", "only_reissue", "only_deposits", "only_contract", "no_reissue", "no_deposits",
              "no_contract", "deposit_ratio", "deposit_flat", "contract_last_year", "panel_mix", "desk_model", "trend"):
        s_ = S[k]
        check("R4 no one thing: %s leaves the range at or across the street" % k, A.call_of(s_, street) != "short",
              "%.1f to %.1f against %.1f" % (s_["low"], s_["high"], street))
    n = len(E["results"])
    worst_hint = max(len(h["rescues"]) for h in E["hints"])
    check("R5 the one-fact test: no hint rescues more than a third of the results", worst_hint <= n / 3.0,
          "largest %d of %d" % (worst_hint, n))
    check("R6a every golden-family forecast inside R7's band",
          all(inside(round(v["forecast"], 1), B["forecast_m"]) for v in fam.values()))
    check("R6b every golden-family range inside R7's low and high bands",
          all(inside(round(v["low"], 1), B["range_low_m"]) and inside(round(v["high"], 1), B["range_high_m"])
              for v in fam.values()))
    check("R6c every golden-family record inside R6's bands",
          all(inside(round(100 * v["rmse"], 2), B["golden_rmse_pp"]) and inside(round(100 * v["errs"]["FY2025 Q3"], 2),
                                                                                B["q3_error_pp"]) for v in fam.values()))
    check("R6d R2's rivals inside its bands (the Midwest per card, issuer by issuer or on same-age cards; the visible "
          "growth at each mix)",
          all(inside(round(100 * V["regional"][h]["Midwest"], 2), B["midwest_pct"]) for h in ("lfl", "same_age"))
          and all(inside(round(100 * v, 2), B["visible_growth_pct"]) for v in V["visible"].values()))
    check("R6e every order of the bridge's steps inside each step's band",
          all(inside(round(100 * v, 2), B["bridge_pp"][k]) for k, vs in R["bridge_orders"].items() for v in vs))
    check("R6f R4 and R5's rivals inside their bands",
          all(inside(round(v, 1), B["deposits_q4_m"]) for v in V["dep_q4"].values())
          and all(inside(round(V["ct_hat"][r_], 1), B["contract_q4_m"]) for r_ in ("median8", "median4")))
    check("R7a forcing: every golden-family range tops out below the street", all(v["high"] < street for v in fam.values()),
          "highest %.1f against %.1f" % (max(v["high"] for v in fam.values()), street))
    check("R7b forcing: every shortcut's range reaches the street or above",
          all(s_.get("high", s_["forecast"]) >= street for k, s_ in S.items() if k not in ("quick", "delivered")))
    check("R7c forcing: every perturbation keeps the top of the range below the street",
          all(v < street for v in R["perturb"].values()), "highest %.1f" % max(R["perturb"].values()))

    # ------------------------------------------------------------------------------------------- the fork table
    est = P["street"].q4_fy2025_net_sales_usd_m
    late = P["street"].sort_values("estimate_date").tail(5).q4_fy2025_net_sales_usd_m
    top = max(v["high"] for v in fam.values())
    check("SF1 the street's figure: the mean, the median and the latest five estimates all clear every family range",
          min(est.mean(), est.median(), late.mean()) > top, "%.1f, %.1f, %.1f" % (est.mean(), est.median(), late.mean()))
    check("SF2 net sales as reported: the base includes Fernhollow (consolidated in both quarters) and contract",
          abs(R["base"] - res.net_sales["FY2024 Q4"]) < 1e-9 and A.fern_both(P, "FY2025 Q4", "FY2024 Q4"))
    check("SF3 weekly averages and quarter totals agree for the quarter (13 weeks each side)",
          int(res.weeks["FY2024 Q4"]) == 13 and pan[pan.fq == "FY2025 Q4"].week_start.nunique() == 13)
    check("SF4 the comparison quarter is the fourth quarter of fiscal 2024, the 13 weeks to 1 February 2025",
          str(res.period_end["FY2024 Q4"].date()) == "2025-02-01")
    check("SF5 the licensed shops and cafes are taken out (the 10-K: their sales are not net sales)",
          R["excluded_share"] > 0.05 and R["bridge"][2][1] < 0)
    pre = pan[(pan.merchant_id == "M2290") & (pan.week_start < A.ACQUIRED)]
    check("SF6 Fernhollow enters the panel's entity from its acquisition only", pre.empty)
    check("SF7 completion by medians, means or the last thirteen deliveries: within 0.3 points of the golden's uplift",
          all(abs(round(100 * v, 2) - F["completion_pct"]) <= 0.3 for v in V["completion"].values()))
    check("SF8 the regional weights: fiscal 2024, fiscal 2023 or fiscal 2024 rolled forward, inside R2's band; the call holds",
          all(inside(round(100 * v, 2), B["visible_growth_pct"]) for v in V["visible"].values())
          and fam["the regional mix of fiscal 2023"]["high"] < street
          and fam["fiscal 2024's regional mix rolled forward a year"]["high"] < street)
    rawsp = X["raw spend on the issuers in both quarters"]
    cs = A.card_series(P)
    tot = cs.groupby(level=[0, 2]).sum()
    drift = {i: float(tot[i][pd.Timestamp("2025-09-28")] / tot[i][pd.Timestamp("2024-09-29")] - 1)
             for i in ("KS-02", "KS-03", "KS-04", "KS-05")}
    check("SF9 the panel's normalisation: spend per open card pooled, issuer by issuer or on same-age cards keep the call; "
          "raw spend is ruled out by the issuers' card files moving at different rates",
          fam["spend per open card issuer by issuer"]["high"] < street and fam["cards of the same age"]["high"] < street
          and A.call_of(rawsp, street) != "short" and max(drift.values()) - min(drift.values()) > 0.05,
          "cards a year on: %s" % ", ".join("%s %+.1f%%" % (k, 100 * v) for k, v in drift.items()))
    check("SF10 the issuers: those in every week of both quarters less KS-01, whose Midwest cards rose %.1f%% in four "
          "weeks; KS-01 kept is ruled out" % F["ks01_mw_cards_rise_pct"],
          R["issuers_used"] == ["KS-02", "KS-03", "KS-04", "KS-05"] and F["ks01_mw_cards_rise_pct"] > 10
          and A.call_of(X["KS-01 kept"], street) != "short")
    check("SF11 a re-issued book read at a 2 to 12 per cent four-week rise: the same issuers",
          all(v == R["issuers_used"] for v in V["reissue_jump"].values()))
    check("SF12 the region labels: every spelling maps to one of the four regions (no reading leaves a fifth)",
          set(P["panel"].billing_region.unique()) == set(A.REGIONS))
    check("SF13 the range from the record's error percentiles keeps the call",
          R["perturb"]["the range from the record's 10th and 90th percentile errors"] < street)
    check("SF14 the call rule: short only when the whole range sits below the street",
          R["call"] == "short" and G["high"] < street)
    check("SF15 the record from fiscal 2022 or fiscal 2023: inside R6's bands",
          inside(round(100 * fam["the record from fiscal 2023 only"]["rmse"], 2), B["golden_rmse_pp"]))
    rg = X["the chain calibrated by regression on past quarters"]
    lumps = ["FY2022 Q2", "FY2023 Q3", "FY2024 Q4"]
    mean_e = np.mean(list(G["errs"].values()))
    mean_x = np.mean([v for k, v in G["errs"].items() if k not in lumps])
    check("SF16 calibration: as built; a regression is ruled out because the record's mean error is the three contract "
          "deliveries (%.2f points with them, %.2f without)" % (100 * mean_e, 100 * mean_x),
          abs(mean_x) < 0.5 * abs(mean_e) and rg["high"] < street)
    wk = X["the custom-order share over the whole quarter"]
    dw = np.mean([v for k_, v in R["dep_weeks"].items()])
    shares = [A.custom_share(P, k) for k in P["keys"][:-1] if k >= "FY2022 Q1"]
    check("SF17 the deposit window: seven to nine weeks inside the bands; the whole quarter ruled out (deposits run "
          "%.2f weeks of the brand's payments, near eight weeks of a %.0f per cent custom share)" % (dw, 100 * np.mean(shares)),
          7.0 <= dw / np.mean(shares) <= 9.0 and wk["rmse"] >= G["rmse"] - 0.001,
          "%.2f weeks of custom orders" % (dw / np.mean(shares)))
    check("SF18 the quarter-end deposits: last year's ratio or last year's change are ruled out by the custom-order share "
          "of the last eight weeks (%.2f%% against %.2f%%)" % (100 * R["custom_q"], 100 * R["custom_b"]),
          R["custom_q"] > R["custom_b"] + 0.03 and A.call_of(X["deposits at last year's ratio to payments"], street) != "short"
          and A.call_of(X["the deposits' change moved as a year earlier"], street) != "short")
    ct = R["ct_hist"]
    check("SF19 contract at the median of eight or four quarters keeps the call; last year's fourth quarter is ruled out "
          "because no delivery recurs a year on (fiscal 2022 Q2 %.1f then %.1f; fiscal 2023 Q3 %.1f then %.1f)"
          % (ct["FY2022 Q2"], ct["FY2023 Q2"], ct["FY2023 Q3"], ct["FY2024 Q3"]),
          fam["contract at the median of the last four quarters"]["high"] < street
          and ct["FY2023 Q2"] < ct["FY2022 Q2"] - 5 and ct["FY2024 Q3"] < ct["FY2023 Q3"] - 5
          and A.call_of(X["contract at last year's fourth quarter"], street) != "short")
    check("SF20 contract is in net sales, and each fourth quarter's contract is the fiscal year less the nine months",
          abs(R["ct_base"] - (R["ct_fy2024"] - R["ct_9m_fy2024"])) < 1e-9
          and abs(res.net_sales["FY2024 Q4"] - res.contract["FY2024 Q4"] - A.retail(P, "FY2024 Q4")) < 1e-9)
    check("SF21 the site's payment-facilitator descriptor stays with the site (online orders are net sales)",
          (P["desc"][P["desc"].descriptor.str.startswith("PAYPAL")].merchant_id == "M0413").all())
    old = P["panel"][P["panel"].card_open_year.str.startswith("<=")]
    check("SF22 the oldest open-year bucket is one bucket in every week (per-card routes need no open year)",
          old.card_open_year.nunique() == 1)

    check("SF23 how the range would have held: at the record's own error and built only on the errors before each, "
          "both counts inside their stated bands",
          inside(G["inside"], B["coverage_in"]) and inside(G["inside_asof"], B["coverage_asof_in"])
          and all(inside(v["inside_asof"], B["coverage_asof_in"]) for v in fam.values()),
          "%d of %d; %d of %d" % (G["inside"], G["n"], G["inside_asof"], G["n_asof"]))

    # ---------------------------------------------------------------------------------------------- realism sweep
    txt = open(os.path.join(TASK, "submission.md")).read()
    pr = open(os.path.join(TASK, "prompt.txt")).read() if os.path.exists(os.path.join(TASK, "prompt.txt")) else ""
    check("S1 no em dashes in the submission or the prompt", "—" not in txt and "—" not in pr)
    leaky = [f for f in files if re.search(r"(trap|decoy|golden|answer|test|v\d)", f, re.I)]
    check("S2 no file name names a role, a version or the answer", not leaky, ", ".join(leaky))
    later = P["street"][pd.to_datetime(P["street"].estimate_date) > pd.Timestamp("2026-02-05")]
    check("S3 nothing in the pack is dated after the desk's as-of date", later.empty)
    T = pack_text()
    words = r"re-?issu|reissu|conversion|portfolio|transferr|recogni[sz]|invoic|lead time|eight weeks|data dictionary|" \
            r"panel coverage|private.label|tender"
    hits = sorted({"%s: %s" % (f, m.group(0)) for f, t in T.items() for m in re.finditer(words, t, re.I)})
    check("S4 no file in the pack names a book moved between issuers, revenue recognition, invoicing, a lead time or "
          "what a table is", not hits, "; ".join(hits[:6]))
    print("\n%d checks failed" % len(FAILS) if FAILS else "\nall checks pass")
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
