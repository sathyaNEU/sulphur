"""task20 checks: the cut pack against the clean truth (the simulated world before any file was written), the bar
block R1 to R7 (dataset-generation 7.1), every fork in the design note's fork table (SF1 to SF17), and the realism
sweep. Exit 1 on any failure.

    python3 task20/generator/checks.py
"""
import json
import os
import re
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


def main():
    R = A.full(TGT)
    P = R["P"]
    w = W.simulate(PK.SEED)
    F = json.load(open(os.path.join(HERE, "figures.json")))
    E = json.load(open(os.path.join(HERE, "effort.json")))
    B = F["bands"]
    street = R["street"]
    G = R["golden"]

    # ------------------------------------------------------------------------------- the pack against the clean truth
    tq = W.QKEYS.index("FY2025Q4")
    bq = W.QKEYS.index("FY2024Q4")
    truth = w.rev_q[tq] / w.rev_q[bq] - 1
    check("C1 the golden's growth sits within 0.5 points of the world's fourth-quarter growth",
          abs(G["growth"] - truth) < 0.005, "golden %.2f%%, world %.2f%%" % (100 * G["growth"], 100 * truth))
    check("C2 the world's fourth-quarter net sales sit inside the golden's 80 per cent range",
          G["low"] <= w.rev_q[tq] <= G["high"], "%.1f in %.1f to %.1f" % (w.rev_q[tq], G["low"], G["high"]))
    lag0 = {PK.ISSUER_CODES[k]: v for k, v in zip(w.issuers, w.lag0)}
    dev = max(abs(R["cf"][(i, 0)] - lag0[i]) for i in lag0)
    check("C3 each issuer's lag-0 completion factor from the delivery history recovers the world's within 0.015",
          dev < 0.015, "max deviation %.4f" % dev)
    sel = W.QIDX == tq
    lic = w.spend[sel][:, :, [4, 5]].sum()
    brand = w.spend[sel][:, :, [0, 1, 4, 5]].sum()
    check("C4 the descriptor detail's excluded share matches the world's licensed and cafe share of the brand id",
          abs(R["excluded_share"] - lic / brand) < 0.003, "%.4f against %.4f" % (R["excluded_share"], lic / brand))
    pl_w = PK.pl_by_quarter(w)
    check("C5 the filing's private-label table is the world's tender mix to one decimal",
          all(abs(P["pl"][k] - pl_w[k.replace(" ", "")]) < 1e-9 for k in P["pl"]))
    res = P["results"].set_index("fiscal_quarter")
    reg = P["regions"].set_index("fiscal_year")
    worst = 0.0
    for fy in reg.index:
        qs = [k for k in res.index if k.startswith(fy) and pd.notna(res.net_sales_usd_m[k])]
        banner_q = sum(float(res.net_sales_usd_m[k]) - float(res.wholesale_net_sales_usd_m[k])
                       - (float(res.fernhollow_net_sales_usd_m[k]) if pd.notna(res.fernhollow_net_sales_usd_m[k]) else 0)
                       for k in qs)
        worst = max(worst, abs(banner_q - float(reg.loc[fy].sum())))
    check("C6 the 10-K's regional table adds to the quarters' banner net sales within rounding", worst <= 0.35,
          "largest gap USD %.2f m" % worst)
    pan = R["pan"]
    comp = pan[pan.fq == "FY2025 Q4"].spend_usd.sum()
    cols = [0, 1, 2, 3]                    # stores, outlet, web, fernhollow: the entity
    world_q = w.spend[sel][:, :, cols].sum()
    check("C7 the completed entity spend for the quarter is within 1 per cent of the world's complete spend",
          abs(comp / world_q - 1) < 0.01, "%.3f%%" % (100 * (comp / world_q - 1)))

    # ---------------------------------------------------------------------------------------------- the bar block
    files = sorted(os.listdir(TGT))
    cats = {"spreadsheet" if f.endswith((".csv", ".xlsx")) else "text" for f in files}
    check("R1a the field's raw material: ten or more files in two or more categories", len(files) >= 10 and len(cats) >= 2,
          "%d files, %s" % (len(files), sorted(cats)))
    n_panel = len(P["panel"])
    n_desc = len(P["desc"])
    check("R1b two large CSVs: the panel of 20,000 rows or more and the descriptor detail of 10 printed pages or more",
          n_panel >= 20000 and n_desc >= 500, "%d and %d rows" % (n_panel, n_desc))
    # neutral mess: the payment-facilitator descriptor and the 53-week year decide nothing
    check("R2a the 53-week fiscal 2023 is read on weekly averages; the target quarter and its base are 13 weeks each",
          int(res.weeks["FY2025 Q4"]) == 13 and int(res.weeks["FY2024 Q4"]) == 13 and int(res.weeks["FY2023 Q4"]) == 14)
    paypal = P["desc"][P["desc"].descriptor.str.startswith("PAYPAL")]
    check("R2b the site's payment-facilitator descriptor is in every month of both quarters (neutral to growth)",
          paypal.month.isin(["2024-11", "2024-12", "2025-01", "2025-11", "2025-12", "2026-01"]).sum() == 6)
    # each result's hurried figure
    c = R["shortcuts"]["careful"]
    check("R3a the careful pass's figures sit outside R4 to R9's bands",
          not inside(0.0, B["bridge_pp"]["revenue on delivery"])
          and not inside(0.0, B["bridge_pp"]["wholesale at its run rate"])
          and not inside(round(100 * c["rmse"], 2), B["golden_rmse_pp"])
          and not inside(round(c["forecast"], 1), B["forecast_m"])
          and A.call_of(c, street) != "short")
    q = R["shortcuts"]["quick"]
    check("R3b the quick pass's figures sit outside R1, R2 and R7's bands",
          not inside(0.0, B["bridge_pp"]["the latest weeks completed"])
          and not inside(round(100 * q["growth"], 2), B["visible_growth_pct"]) and not inside(round(q["forecast"], 1), B["forecast_m"]))
    # no one thing: each correction left out leaves the call wrong
    for k in ("deposits_only", "wholesale_only", "no_mix", "no_tender", "deposit_ratio", "last_year_deposits",
              "careful_regressed", "trend", "trend_retail"):
        s_ = R["shortcuts"][k]
        check("R4 no one thing: %s leaves the range at or across the street" % k, A.call_of(s_, street) != "short",
              "%.1f to %.1f against %.1f" % (s_["low"], s_["high"], street))
    # the one-fact test computed from effort.json
    n = len(E["results"])
    worst_hint = max(len(h["rescues"]) for h in E["hints"])
    check("R5 the one-fact test: no hint rescues more than a third of the results", worst_hint <= n / 3.0,
          "largest %d of %d" % (worst_hint, n))
    # the rivals inside each band
    fam = R["family"]
    check("R6a every golden-family forecast inside R7's band", all(inside(round(v["forecast"], 1), B["forecast_m"]) for v in fam.values()))
    check("R6b every golden-family range inside R7's low and high bands",
          all(inside(round(v["low"], 1), B["range_low_m"]) and inside(round(v["high"], 1), B["range_high_m"]) for v in fam.values()))
    check("R6c every golden-family record inside R6's bands",
          all(inside(round(100 * v["rmse"], 2), B["golden_rmse_pp"]) and inside(round(100 * v["errs"]["FY2025 Q3"], 2), B["q3_error_pp"])
              for v in fam.values()))
    V = R["variants"]
    check("R6d R2 and R3's rivals inside their bands",
          all(inside(round(100 * v, 2), B["visible_growth_pct"]) for v in V["visible"].values())
          and all(inside(round(v, 2), B["pl_target_pct"]) for v in V["pl"].values())
          and all(inside(round(100 * v, 2), B["drift_pct"]) for v in V["drift"].values()))
    check("R6e every order of the bridge's steps inside each step's band",
          all(inside(round(100 * v, 2), B["bridge_pp"][k]) for k, vs in R["bridge_orders"].items() for v in vs))
    check("R6f R4 and R5's rivals inside their bands",
          all(inside(round(P["deposits"]["FY2025 Q3"] + v, 1), B["deposits_q4_m"]) for v in V["dep_change"].values())
          and all(inside(round(A.ws_hat(P, A.TQ, r_), 1), B["wholesale_q4_m"]) for r_ in ("median8", "median4")))
    # forcing
    check("R7a forcing: every golden-family range tops out below the street", all(v["high"] < street for v in fam.values()),
          "highest %.1f against %.1f" % (max(v["high"] for v in fam.values()), street))
    check("R7b forcing: every shortcut's range reaches the street or above",
          all(s_.get("high", s_["forecast"]) >= street for k, s_ in R["shortcuts"].items() if k != "quick"))
    check("R7c forcing: every perturbation keeps the top of the range below the street", all(v < street for v in R["perturb"].values()),
          "highest %.1f" % max(R["perturb"].values()))

    # ------------------------------------------------------------------------------------------- the fork table
    est = P["street"].q4_fy2025_net_sales_usd_m
    late = P["street"].sort_values("estimate_date").tail(5).q4_fy2025_net_sales_usd_m
    top = max(v["high"] for v in fam.values())
    check("SF1 the street's figure: the mean, the median and the latest five estimates all clear every family range",
          min(est.mean(), est.median(), late.mean()) > top, "%.1f, %.1f, %.1f" % (est.mean(), est.median(), late.mean()))
    check("SF2 net sales as reported: the base includes Fernhollow, consolidated in both quarters",
          abs(R["base"] - float(res.net_sales_usd_m["FY2024 Q4"])) < 1e-9 and A.fern_both(P, "FY2025 Q4", "FY2024 Q4"))
    check("SF3 weekly averages and quarter totals agree for the quarter (13 weeks each side)",
          int(res.weeks["FY2024 Q4"]) == 13 and pan[pan.fq == "FY2025 Q4"].week_start.nunique() == 13)
    check("SF4 the comparison quarter is the fourth quarter of fiscal 2024, the 13 weeks to 1 February 2025",
          str(res.period_end["FY2024 Q4"].date()) == "2025-02-01")
    check("SF5 the licensed shops and cafes are taken out (the filing: their sales are not net sales)",
          R["excluded_share"] > 0.05 and R["bridge"][2][1] < 0)
    pre = R["pan"][(R["pan"].merchant_id == "M2290") & (R["pan"].week_start < A.ACQUIRED)]
    check("SF6 Fernhollow enters the panel's entity from its acquisition only", pre.empty)
    check("SF7 completion by medians, means or the last thirteen deliveries: within 0.3 points of the golden's uplift",
          all(abs(round(100 * v, 2) - F["completion_pct"]) <= 0.3 for v in V["completion"].values()))
    check("SF8 the regional weights: fiscal 2024, fiscal 2023 or fiscal 2024 rolled forward, inside R2's band and the call holds",
          all(inside(round(100 * v, 2), B["visible_growth_pct"]) for v in V["visible"].values())
          and fam["the regional mix of fiscal 2023"]["high"] < street and fam["fiscal 2024's regional mix rolled forward a year"]["high"] < street)
    flat = R["ruled_out"]["private-label share held at the third quarter's level"]
    falls = [P["pl"]["FY2024 Q4"] - P["pl"]["FY2025 Q1"], P["pl"]["FY2025 Q1"] - P["pl"]["FY2025 Q2"],
             P["pl"]["FY2025 Q2"] - P["pl"]["FY2025 Q3"]]
    check("SF9 the private-label rules inside R3's band; holding the third quarter flat is ruled out by three successive "
          "and growing falls", all(inside(round(v, 2), B["pl_target_pct"]) for v in V["pl"].values())
          and not inside(P["pl"]["FY2025 Q3"], B["pl_target_pct"]) and falls[0] < falls[1] < falls[2],
          "falls %s; flat would give %.1f" % ([round(x, 1) for x in falls], flat["forecast"]))
    check("SF10 other tenders at 10 or 14 per cent keep the call",
          all(v < street for k, v in R["perturb"].items() if k.startswith("other tenders")))
    check("SF11 the range from the record's error percentiles keeps the call",
          R["perturb"]["the range from the record's 10th and 90th percentile errors"] < street)
    check("SF12 the call rule: short only when the whole range sits below the street", R["call"] == "short" and G["high"] < street)
    check("SF13 the record from fiscal 2022 or fiscal 2023: inside R6's bands",
          inside(round(100 * fam["the record from fiscal 2023 only"]["rmse"], 2), B["golden_rmse_pp"]))
    reg_c = fam["the chain calibrated by regression on past quarters"]
    check("SF14 the chain as built or calibrated by regression: inside R7's bands, the call holds",
          inside(round(reg_c["forecast"], 1), B["forecast_m"]) and reg_c["high"] < street)
    pc = R["ruled_out"]["spend per card instead of cards of the same age"]
    check("SF15 spend per card lands inside R7's band and keeps the call; its record (%.2f points) is ruled out against "
          "same-age cards (%.2f)" % (100 * pc["rmse"], 100 * G["rmse"]),
          inside(round(pc["forecast"], 1), B["forecast_m"]) and pc["high"] < street and pc["rmse"] > G["rmse"] + 0.003)
    iss = sorted(R["pan"][R["pan"].fq == "FY2025 Q4"].issuer_code.unique())
    check("SF16 issuers in both quarters are KS-01 to KS-05 (KS-06 last delivered the week of 26 October 2025)",
          iss == ["KS-01", "KS-02", "KS-03", "KS-04", "KS-05"])
    check("SF17 the site's payment-facilitator descriptor stays with the site (online orders are net sales)",
          (P["desc"][P["desc"].descriptor.str.startswith("PAYPAL")].merchant_id == "M0413").all())
    win = R["ruled_out"]["the made-to-order share over the whole quarter"]
    wk = np.mean([v for k_, v in R["dep_weeks_hist"].items() if k_ < "FY2025 Q4"])
    check("SF18 the deposit window: seven to nine weeks inside the bands; the whole quarter ruled out (deposits average "
          "%.2f weeks of retail payments, about eight weeks of a 30 per cent made-to-order share)" % wk,
          7.0 <= wk / 0.30 <= 9.0 and win["rmse"] > G["rmse"],
          "whole-quarter window record %.2f against %.2f" % (100 * win["rmse"], 100 * G["rmse"]))
    m4 = R["ruled_out"]["wholesale at the mean of the last four quarters, last year's contract included"]
    check("SF19 wholesale at the median of eight or of four quarters: inside R5's band, the call holds; the mean of four "
          "carries last year's one contract into the run rate and still calls short",
          fam["wholesale at the median of the last four quarters"]["high"] < street and m4["high"] < street,
          "mean of four tops at %.1f" % m4["high"])
    ly = R["shortcuts"]["last_year_deposits"]
    check("SF20 deposits moved as they did a year earlier are ruled out by the descriptor detail's made-to-order share",
          A.mto_share_last(P, A.TQ) > 1.3 * A.mto_share_last(P, A.BQ) and A.call_of(ly, street) != "short",
          "%.2f%% against %.2f%%" % (100 * A.mto_share_last(P, A.TQ), 100 * A.mto_share_last(P, A.BQ)))
    check("SF21 net sales include wholesale (the filing's total net sales; the results file's column is part of it)",
          abs(float(res.net_sales_usd_m["FY2024 Q4"]) - float(res.wholesale_net_sales_usd_m["FY2024 Q4"]) - A.retail(P, "FY2024 Q4")) < 1e-9)

    # ---------------------------------------------------------------------------------------------- realism sweep
    txt = open(os.path.join(TASK, "submission.md")).read()
    check("S1 no em dashes in the submission or the prompt",
          "—" not in txt and "—" not in open(os.path.join(TASK, "prompt.txt")).read()
          if os.path.exists(os.path.join(TASK, "prompt.txt")) else "—" not in txt)
    leaky = [f for f in files if re.search(r"(trap|decoy|golden|answer|test|v\d)", f, re.I)]
    check("S2 no file name names a role, a version or the answer", not leaky, ", ".join(leaky))
    later = P["street"][pd.to_datetime(P["street"].estimate_date) > pd.Timestamp("2026-02-05")]
    check("S3 nothing in the pack is dated after the desk's as-of date", later.empty)
    print("\n%d checks failed" % len(FAILS) if FAILS else "\nall checks pass")
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
