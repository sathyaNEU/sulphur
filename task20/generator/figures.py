"""task20 architecture 2 (second hardening): figures.json (every figure the answer blocks and the goldens state) and effort.json (each
result's golden and band, the value each pass files, the precedents behind each careful-column loss, the hints, the
routes and the forcing), from one analysis run on the cut pack."""
import json
import os

import pandas as pd

import analysis as A

HERE = os.path.dirname(os.path.abspath(__file__))


def p2(x):
    """a growth or share in per cent, two decimals"""
    return float(round(100 * x + 1e-12, 2))


def m1(x):
    """USD million, one decimal"""
    return float(round(x + 1e-12, 1))


def span(vals, pad, nd=2):
    return [float(round(min(vals) - pad, nd)), float(round(max(vals) + pad, nd))]


def make(R):
    G = R["golden"]
    base = R["base"]
    V = R["variants"]
    fam = R["family"]
    S = R["shortcuts"]
    X = R["ruled_out"]
    P = R["P"]
    br = dict(R["bridge"])
    bk = [k for k, _ in R["bridge"]]
    errs = G["errs"]
    orders = R["bridge_orders"]
    cs = A.card_series(P)
    mw = cs[("KS-01", "Midwest")]
    w0, w1 = pd.Timestamp("2025-09-28"), pd.Timestamp("2025-10-26")
    se = cs[("KS-02", "Southeast")]
    big = max(errs, key=lambda k: abs(errs[k]))
    F = {
        "as_of": "2026-02-05",
        "release": "26 February 2026",
        "target_quarter": "FY2025 Q4",
        "base_net_sales_m": m1(base),
        "street_m": m1(R["street"]),
        "street_median_m": m1(R["street_median"]),
        "street_n": R["street_n"],
        "street_growth_pct": p2(R["street"] / base - 1),
        "forecast_m": m1(G["forecast"]),
        "growth_pct": p2(G["growth"]),
        "growth_abs_pct": abs(p2(G["growth"])),
        "range_low_m": m1(G["low"]),
        "range_high_m": m1(G["high"]),
        "band_pp": p2(G["band"]),
        "golden_rmse_pp": p2(G["rmse"]),
        "coverage_in": G["inside"],
        "origins": G["n"],
        "coverage_asof_in": G["inside_asof"],
        "coverage_asof_n": G["n_asof"],
        "first_asof_origin": G["origins"][G["n"] - G["n_asof"]],
        "first_origin": G["origins"][0],
        "last_origin": G["origins"][-1],
        "errors_pp": {k: p2(v) for k, v in errs.items()},
        "estimates_pct": {q: p2(x) for q, x in zip(G["origins"], G["xs"])},
        "reported_pct": {q: p2(y) for q, y in zip(G["origins"], G["ys"])},
        "q3_error_pp": p2(errs["FY2025 Q3"]),
        "largest_miss_q": big,
        "largest_miss_pp": p2(errs[big]),
        "excluded_share_pct": p2(R["excluded_share"]),
        "completion_pct": p2(R["completion_uplift"]),
        "cf_last_week_pct": {k: p2(v) for k, v in sorted(R["cf_last_week"].items())},
        "issuers_both": R["issuers_both"],
        "issuers_used": R["issuers_used"],
        "ks01_mw_cards_before": int(round(float(mw[w0]))),
        "ks01_mw_cards_after": int(round(float(mw[w1]))),
        "ks01_mw_cards_rise_pct": p2(float(mw[w1]) / float(mw[w0]) - 1),
        "ks02_se_rise_pct": p2(float(se[pd.Timestamp("2023-05-21")]) / float(se[pd.Timestamp("2023-04-23")]) - 1),
        "regional_pct": {r: p2(v) for r, v in R["regional"].items()},
        "regional_with_ks01_pct": {r: p2(v) for r, v in R["regional_with_ks01"].items()},
        "company_weights_pct": {r: p2(v) for r, v in R["company_w"].items()},
        "panel_weights_pct": {r: p2(v) for r, v in R["panel_w"].items()},
        "visible_growth_pct": p2(R["g_idx"]),
        "visible_with_ks01_pct": p2(R["g_idx_with_ks01"]),
        "pooled_growth_pct": p2(R["g_pooled"]),
        "pooled_with_ks01_pct": p2(R["g_pooled_with_ks01"]),
        "payments_base_m": m1(R["pay_base"]),
        "payments_q4_m": m1(R["pay_q4"]),
        "deposits_q3_m": m1(R["dep_q3"]),
        "deposits_base_m": m1(R["dep_base"]),
        "deposits_q3fy24_m": m1(R["dep_q3fy24"]),
        "deposits_q4_m": m1(R["dep_q4_est"]),
        "deposit_change_m": m1(R["dep_change"]),
        "deposit_change_base_m": m1(R["dep_change_base"]),
        "custom_q4_pct": p2(R["custom_q"]),
        "custom_base_pct": p2(R["custom_b"]),
        "trail_q4_pct": p2(R["trail_q"]),
        "trail_base_pct": p2(R["trail_b"]),
        "deposit_weeks": {k: float(round(v, 2)) for k, v in R["dep_weeks"].items()},
        "deposits_by_q": {k: m1(P["deposits"][k]) for k in P["keys"][:-1]},
        "retail_base_m": m1(R["retail_base"]),
        "retail_q4_m": m1(R["retail_q4"]),
        "retail_growth_pct": p2(R["retail_growth"]),
        "fern_base_m": m1(R["fern_base"]),
        "contract_fy2024_m": m1(R["ct_fy2024"]),
        "contract_9m_fy2024_m": m1(R["ct_9m_fy2024"]),
        "contract_base_m": m1(R["ct_base"]),
        "contract_q4_m": m1(R["ct_hat"]),
        "contract_by_q": {k: m1(v) for k, v in R["ct_hist"].items()},
        "bridge_pp": [[k, p2(v)] for k, v in R["bridge"]],
        "family_m": {k: m1(v["forecast"]) for k, v in fam.items()},
        "family_high_m": {k: m1(v["high"]) for k, v in fam.items()},
        "ruled_out_m": {k: m1(v["forecast"]) for k, v in X.items()},
        "ruled_out_high_m": {k: m1(v["high"]) for k, v in X.items()},
        "ruled_out_low_m": {k: m1(v["low"]) for k, v in X.items()},
        "ruled_out_rmse_pp": {k: p2(v["rmse"]) for k, v in X.items()},
        "shortcut_m": {k: m1(v["forecast"]) for k, v in S.items()},
        "shortcut_pct": {k: p2(v["growth"]) for k, v in S.items()},
        "shortcut_rmse_pp": {k: p2(v["rmse"]) for k, v in S.items() if "rmse" in v},
        "shortcut_low_m": {k: m1(v["low"]) for k, v in S.items() if "low" in v},
        "shortcut_high_m": {k: m1(v["high"]) for k, v in S.items() if "high" in v},
        "shortcut_call": {k: (A.call_of(v, R["street"]) if "high" in v else
                              ("short" if v["forecast"] < R["street"] else "long")) for k, v in S.items()},
        "careful_q3_error_pp": p2(S["careful"]["errs"]["FY2025 Q3"]),
        "careful_inside": S["careful"]["inside"],
        "organic_pct": {k: p2(v) for k, v in R["organic"].items()},
        "incumbent": {"intercept_pp": p2(R["incumbent"]["fit"][0]), "slope": float(round(R["incumbent"]["fit"][1], 3)),
                      "rmse_pp": p2(R["incumbent"]["rmse"]), "q3_x_pct": p2(R["incumbent"]["x_q3"]),
                      "q3_growth_pct": p2(R["incumbent"]["g_q3"]), "q3_forecast_m": m1(R["incumbent"]["q3_forecast"]),
                      "q3_actual_m": m1(R["incumbent"]["q3_actual"])},
        "perturb_m": {k: m1(v) for k, v in R["perturb"].items()},
        "call": R["call"],
        "constants": {"range_pct": 80, "z80": A.Z80, "weeks": 13, "deposit_window_weeks": 8, "deposit_window_days": 56,
                      "contract_quarters": 8, "reissue_jump_pct": int(round(100 * A.JUMP)), "deliveries": 27},
    }
    F["range_gap_m"] = m1(F["street_m"] - F["range_high_m"])
    # bands: each result's rivals, run on the cut pack, plus a margin
    B = {"bridge_pp": {bk[0]: span([p2(br[bk[0]])], 0.3)}}
    for k in A.PANEL_STEPS + A.COMPANY_STEPS:
        vals = [p2(v) for v in orders[k]]
        if k == "revenue on delivery":
            vals += [p2(v) for v in V["dep_points"].values()]
        B["bridge_pp"][k] = span(vals, 0.3)
    mw_vals = [p2(R["regional"]["Midwest"])] + [p2(V["regional"][h]["Midwest"]) for h in ("lfl", "same_age")]
    B["midwest_pct"] = span(mw_vals, 0.5)
    B["visible_growth_pct"] = span([p2(v) for v in V["visible"].values()], 0.3)
    B["deposits_q4_m"] = span([m1(v) for v in V["dep_q4"].values()], 3.0, 1)
    B["contract_base_m"] = span([F["contract_base_m"]], 0.2, 1)
    B["contract_q4_m"] = span([m1(V["ct_hat"][r]) for r in ("median8", "median4")], 1.0, 1)
    B["golden_rmse_pp"] = span([p2(v["rmse"]) for v in fam.values()], 0.15)
    B["q3_error_pp"] = span([p2(v["errs"]["FY2025 Q3"]) for v in fam.values()], 0.2)
    B["coverage_in"] = [min(v["inside"] for v in fam.values()), max(v["inside"] for v in fam.values())]
    B["coverage_asof_in"] = [min(v["inside_asof"] for v in fam.values()), max(v["inside_asof"] for v in fam.values())]
    B["forecast_m"] = span([m1(v["forecast"]) for v in fam.values()], 3.0, 1)
    B["range_low_m"] = span([m1(v["low"]) for v in fam.values()], 3.0, 1)
    B["range_high_m"] = span([m1(v["high"]) for v in fam.values()], 3.0, 1)
    F["bands"] = B
    # one key per result: the result's golden as effort.json carries it
    F["r1_panel"] = {k: v for k, v in F["bridge_pp"][:4]}
    F["r2_reissue"] = {"midwest_pct": F["regional_pct"]["Midwest"], "visible_growth_pct": F["visible_growth_pct"]}
    F["r3_mix"] = {"the company's regional mix": p2(br["the company's regional mix"]),
                   "company_weight_midwest_pct": F["company_weights_pct"]["Midwest"]}
    F["r4_deposits"] = {"deposits_q4_m": F["deposits_q4_m"], "revenue on delivery": p2(br["revenue on delivery"])}
    F["r5_contract"] = {"contract_base_m": F["contract_base_m"], "contract_q4_m": F["contract_q4_m"],
                        "contract at its run rate": p2(br["contract at its run rate"])}
    F["r6_record"] = {"golden_rmse_pp": F["golden_rmse_pp"], "q3_error_pp": F["q3_error_pp"],
                      "coverage_in": F["coverage_in"]}
    F["r7_forecast"] = {"forecast_m": F["forecast_m"], "range_low_m": F["range_low_m"], "range_high_m": F["range_high_m"]}
    F["r8_bridge"] = {k: v for k, v in F["bridge_pp"][4:]}
    F["r9_call"] = {"call": F["call"], "range_high_m": F["range_high_m"]}
    return F


def effort(F, R):
    B = F["bands"]
    S = R["shortcuts"]
    c = S["careful"]
    bk = [k for k, _ in F["bridge_pp"]]
    cw = F["company_weights_pct"]
    careful_mix = p2(R["g_idx_with_ks01"] - R["g_pooled_with_ks01"])
    res = [
        dict(id="R1", name="the panel's own steps: the delivered panel, the latest weeks completed, the licensed shops and "
                           "cafes out, issuers in every week of both quarters on spend per open card",
             graded_as="Ask 3 (panel steps)", figure="r1_panel", depends=[],
             independent="the panel, its delivery history and descriptor detail",
             golden=F["r1_panel"], bands={k: B["bridge_pp"][k] for k in bk[:4]},
             passes={"quick": {bk[0]: F["r1_panel"][bk[0]], bk[1]: 0.0, bk[2]: 0.0, bk[3]: 0.0},
                     "careful": F["r1_panel"], "thorough": F["r1_panel"]}),
        dict(id="R2", name="KS-01's re-issued book: the Midwest's like-for-like growth without it and card-visible growth "
                           "at the company's mix", graded_as="Component 1", figure="r2_reissue", depends=["R1"],
             independent="", golden=F["r2_reissue"],
             bands={"midwest_pct": B["midwest_pct"], "visible_growth_pct": B["visible_growth_pct"]},
             passes={"quick": None,
                     "careful": {"midwest_pct": F["regional_with_ks01_pct"]["Midwest"],
                                 "visible_growth_pct": F["visible_with_ks01_pct"]},
                     "thorough": F["r2_reissue"]},
             precedent=["N01", "N07"]),
        dict(id="R3", name="the company's regional mix and what the re-weight is worth", graded_as="Component 2",
             figure="r3_mix", depends=["R1"], independent="the 10-K's net sales by region",
             golden=F["r3_mix"], bands={"the company's regional mix": B["bridge_pp"]["the company's regional mix"],
                                        "company_weight_midwest_pct": span([cw["Midwest"]], 0.05)},
             passes={"quick": None, "careful": {"the company's regional mix": careful_mix,
                                                "company_weight_midwest_pct": cw["Midwest"]},
                     "thorough": F["r3_mix"]}),
        dict(id="R4", name="customer deposits at the quarter's end and what revenue on delivery is worth",
             graded_as="Component 3", figure="r4_deposits", depends=["R2", "R3"], independent="",
             golden=F["r4_deposits"], bands={"deposits_q4_m": B["deposits_q4_m"],
                                             "revenue on delivery": B["bridge_pp"]["revenue on delivery"]},
             passes={"quick": None, "careful": {"deposits_q4_m": None, "revenue on delivery": 0.0},
                     "thorough": F["r4_deposits"]},
             precedent=["N02", "L07", "N12"]),
        dict(id="R5", name="contract sales: last year's fourth quarter rebuilt from the fiscal year and the nine months, "
                           "this quarter's run rate, and what separating them is worth", graded_as="Component 4",
             figure="r5_contract", depends=[], independent="the earnings releases",
             golden=F["r5_contract"], bands={"contract_base_m": B["contract_base_m"], "contract_q4_m": B["contract_q4_m"],
                                             "contract at its run rate": B["bridge_pp"]["contract at its run rate"]},
             passes={"quick": None, "careful": {"contract_base_m": None, "contract_q4_m": None,
                                                "contract at its run rate": 0.0},
                     "thorough": F["r5_contract"]},
             precedent=["L10", "L11"]),
        dict(id="R6", name="the range's record: rolling-origin error, the third quarter's miss and the quarters inside",
             graded_as="Ask 2", figure="r6_record", depends=["R2", "R4", "R5"], independent="", golden=F["r6_record"],
             bands={"golden_rmse_pp": B["golden_rmse_pp"], "q3_error_pp": B["q3_error_pp"],
                    "coverage_in": B["coverage_in"]},
             passes={"quick": None, "careful": {"golden_rmse_pp": p2(c["rmse"]), "q3_error_pp": F["careful_q3_error_pp"],
                                                "coverage_in": F["careful_inside"]},
                     "thorough": F["r6_record"]},
             precedent=["L28", "L37"]),
        dict(id="R7", name="the quarter's net sales with its 80 per cent range", graded_as="Ask 1", figure="r7_forecast",
             depends=["R2", "R4", "R5", "R6"], independent="", golden=F["r7_forecast"],
             bands={"forecast_m": B["forecast_m"], "range_low_m": B["range_low_m"], "range_high_m": B["range_high_m"]},
             passes={"quick": {"forecast_m": F["shortcut_m"]["quick"], "range_low_m": None, "range_high_m": None},
                     "careful": {"forecast_m": m1(c["forecast"]), "range_low_m": m1(c["low"]), "range_high_m": m1(c["high"])},
                     "thorough": F["r7_forecast"]},
             precedent=["N02", "N05"]),
        dict(id="R8", name="what the regional mix, KS-01's book, revenue on delivery and contract are worth",
             graded_as="Ask 3 (company steps)", figure="r8_bridge", depends=["R2", "R3", "R4", "R5"], independent="",
             golden=F["r8_bridge"], bands={k: B["bridge_pp"][k] for k in bk[4:]},
             passes={"quick": None, "careful": {bk[4]: careful_mix, bk[5]: 0.0, bk[6]: 0.0, bk[7]: 0.0},
                     "thorough": F["r8_bridge"]},
             precedent=["L11"]),
        dict(id="R9", name="the call against the street", graded_as="Recommendation", figure="r9_call",
             depends=["R7"], independent="", golden=F["r9_call"], bands={"range_high_m": B["range_high_m"]},
             passes={"quick": {"call": F["shortcut_call"]["quick"], "range_high_m": None},
                     "careful": {"call": F["shortcut_call"]["careful"], "range_high_m": m1(c["high"])},
                     "thorough": F["r9_call"]},
             precedent=["L28", "N02"]),
    ]
    hints = [
        {"sentence": "from October 2025 KS-01's cards include part of KS-06's book, re-issued, and those accounts spend "
                     "more at the brand than KS-01's own", "rescues": ["R2"]},
        {"sentence": "custom orders are paid when placed and recognised when delivered, and the design studios' December "
                     "and January orders are still in customer deposits at the quarter's end", "rescues": ["R4"]},
        {"sentence": "last year's fourth quarter held a large contract delivery that no card carries", "rescues": ["R5"]},
    ]
    names = {"careful": "issuers in every week of both quarters on spend per open card, the company's regional mix, net "
                        "sales grown with it (careful but hurried)",
             "careful_regressed": "the same, reported growth regressed on it over past quarters",
             "only_reissue": "KS-01's book taken out, nothing else",
             "only_deposits": "revenue on delivery, nothing else",
             "only_contract": "contract at its run rate, nothing else",
             "no_reissue": "everything but KS-01's book",
             "no_deposits": "everything but revenue on delivery",
             "no_contract": "everything but contract at its run rate",
             "deposit_ratio": "deposits at last year's ratio to payments",
             "deposit_flat": "the deposits' change moved as a year earlier",
             "contract_last_year": "contract at last year's fourth quarter",
             "panel_mix": "everything but the company's regional mix",
             "desk_model": "the desk's third-quarter model carried to the fourth quarter",
             "trend": "fiscal 2025's reported growth carried into the quarter",
             "quick": "the issuers in both quarters, raw spend, on last year's net sales (quick)"}
    routes = [dict(name="golden", golden=True, answer=[F["forecast_m"], F["call"]])]
    for k in names:
        routes.append(dict(name=names[k], answer=[F["shortcut_m"][k], F["shortcut_call"][k]]))
    forcing = dict(kind="numeric", line=F["street_m"], golden_side="below",
                   golden_family=[dict(name=k, value=v) for k, v in F["family_high_m"].items()],
                   shortcuts=[dict(name=names[k], value=F["shortcut_high_m"][k]) for k in names if k != "quick"],
                   perturbations=[dict(input=k, value=v) for k, v in F["perturb_m"].items()],
                   notes="Values are the top of each route's 80 per cent range (the call is short only while the whole "
                         "range sits below the street's figure). Each deep step left out on its own leaves the range "
                         "across the line (no position); two or three left out land long.")
    return {"results": res, "hints": hints, "routes": routes, "forcing": forcing}


def write(R, gen_dir=HERE):
    F = make(R)
    E = effort(F, R)
    json.dump(F, open(os.path.join(gen_dir, "figures.json"), "w"), indent=1, sort_keys=True)
    json.dump(E, open(os.path.join(gen_dir, "effort.json"), "w"), indent=1)
    return F, E
