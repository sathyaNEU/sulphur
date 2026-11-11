"""task20 architecture 2: figures.json (every figure the answer blocks and the goldens state) and effort.json (each
result's golden and band, the value each pass files, the precedents behind each careful-column loss, the hints, the
routes and the forcing), from one analysis run on the cut pack."""
import json
import os

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
    P = R["P"]
    br = dict(R["bridge"])
    bk = [k for k, _ in R["bridge"]]
    errs = G["errs"]
    orders = R["bridge_orders"]
    q3 = A.prev_q(P, A.TQ)
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
        "first_origin": G["origins"][0],
        "last_origin": G["origins"][-1],
        "errors_pp": {k: p2(v) for k, v in errs.items()},
        "q3_error_pp": p2(errs["FY2025 Q3"]),
        "excluded_share_pct": p2(R["excluded_share"]),
        "completion_pct": p2(R["completion_uplift"]),
        "cf_last_week_pct": {k: p2(v) for k, v in sorted(R["cf_last_week"].items())},
        "regional_pct": {r: p2(v) for r, v in R["regional"].items()},
        "company_weights_pct": {r: p2(v) for r, v in R["company_w"].items()},
        "panel_weights_pct": {r: p2(v) for r, v in R["panel_w"].items()},
        "visible_growth_pct": p2(R["g_idx"]),
        "pooled_growth_pct": p2(R["g_pooled"]),
        "pl_target_pct": float(round(R["pl_target"], 2)),
        "pl_q4fy24_pct": float(P["pl"]["FY2024 Q4"]),
        "pl_q3fy24_pct": float(P["pl"]["FY2024 Q3"]),
        "pl_q1fy25_pct": float(P["pl"]["FY2025 Q1"]),
        "pl_q2fy25_pct": float(P["pl"]["FY2025 Q2"]),
        "pl_q3fy25_pct": float(P["pl"]["FY2025 Q3"]),
        "drift_pct": p2(R["drift"] - 1),
        "drift_less_pct": p2(1 - R["drift"]),
        "bank_q4fy24_pct": float(round(100 * A.bank_share(P["pl"]["FY2024 Q4"]), 1)),
        "bank_target_pct": float(round(100 * A.bank_share(R["pl_target"]), 1)),
        "payments_growth_pct": p2(R["g_pay"]),
        "payments_base_m": m1(R["pay_base"]),
        "payments_q4_m": m1(R["pay_q4"]),
        "deposits_q3_m": m1(P["deposits"][q3]),
        "deposits_base_m": m1(P["deposits"][A.BQ]),
        "deposits_q4_m": m1(R["dep_q4_est"]),
        "deposit_change_m": m1(R["dep_change"]),
        "deposit_change_base_m": m1(R["dep_change_base"]),
        "mto_share_q4_pct": p2(A.mto_share_last(P, A.TQ)),
        "mto_share_base_pct": p2(A.mto_share_last(P, A.BQ)),
        "deposit_weeks": {k: float(round(v, 2)) for k, v in R["dep_weeks_hist"].items()},
        "retail_base_m": m1(R["retail_base"]),
        "retail_q4_m": m1(R["retail_q4"]),
        "retail_growth_pct": p2(R["retail_growth"]),
        "wholesale_base_m": m1(R["ws_base"]),
        "wholesale_q4_m": m1(R["ws_hat"]),
        "bridge_pp": [[k, p2(v)] for k, v in R["bridge"]],
        "family_m": {k: m1(v["forecast"]) for k, v in fam.items()},
        "family_high_m": {k: m1(v["high"]) for k, v in fam.items()},
        "shortcut_m": {k: m1(v["forecast"]) for k, v in S.items()},
        "shortcut_pct": {k: p2(v["growth"]) for k, v in S.items()},
        "shortcut_rmse_pp": {k: p2(v["rmse"]) for k, v in S.items() if "rmse" in v},
        "shortcut_low_m": {k: m1(v["low"]) for k, v in S.items() if "low" in v},
        "shortcut_high_m": {k: m1(v["high"]) for k, v in S.items() if "high" in v},
        "shortcut_call": {k: (A.call_of(v, R["street"]) if "high" in v else
                              ("short" if v["forecast"] < R["street"] else "long")) for k, v in S.items()},
        "careful_q3_error_pp": p2(S["careful"]["errs"]["FY2025 Q3"]),
        "ruled_out_high_m": {k: m1(v["high"]) for k, v in R["ruled_out"].items()},
        "ruled_out_rmse_pp": {k: p2(v["rmse"]) for k, v in R["ruled_out"].items()},
        "organic_pct": {k: p2(v) for k, v in R["organic"].items()},
        "incumbent": {"intercept_pp": p2(R["incumbent"]["fit"][0]), "slope": float(round(R["incumbent"]["fit"][1], 3)),
                      "rmse_pp": p2(R["incumbent"]["rmse"]), "q3_x_pct": p2(R["incumbent"]["x_q3"]),
                      "q3_growth_pct": p2(R["incumbent"]["g_q3"]), "q3_forecast_m": m1(R["incumbent"]["q3_forecast"]),
                      "q3_actual_m": m1(R["incumbent"]["q3_actual"])},
        "perturb_m": {k: m1(v) for k, v in R["perturb"].items()},
        "call": R["call"],
        "constants": {"range_pct": 80, "z80": A.Z80, "other_tender_pct": 12, "weeks": 13, "fy2024_tender": "67, 21 and 12",
                      "deposit_window_weeks": 8, "deposit_window_days": 56, "wholesale_quarters": 8,
                      "section_refs": "1 2 3 4 5 6 7 8 9"},
    }
    F["range_gap_m"] = m1(F["street_m"] - F["range_high_m"])
    # bands: each result's rivals, run on the cut pack, plus a margin
    B = {"bridge_pp": {bk[0]: span([p2(br[bk[0]])], 0.3)}}
    for k in A.PANEL_STEPS + A.COMPANY_STEPS:
        vals = [p2(v) for v in orders[k]]
        if k == "the company's regional mix":
            vals += [p2(v - R["g_pooled"]) for v in V["visible"].values()]
        if k == "revenue on delivery":
            vals += [p2(v) for v in V["dep_points"].values()]
        B["bridge_pp"][k] = span(vals, 0.3)
    B["visible_growth_pct"] = span([p2(v) for v in V["visible"].values()], 0.3)
    B["pl_target_pct"] = span([float(round(v, 2)) for v in V["pl"].values()], 0.2)
    B["drift_pct"] = span([p2(v) for v in V["drift"].values()], 0.3)
    B["deposits_q4_m"] = span([m1(P["deposits"][q3] + v) for v in V["dep_change"].values()], 3.0, 1)
    ws_vals = [A.ws_hat(P, A.TQ, r) for r in ("median8", "median4")]
    B["wholesale_q4_m"] = span([m1(v) for v in ws_vals], 1.0, 1)
    B["golden_rmse_pp"] = span([p2(v["rmse"]) for v in fam.values()], 0.15)
    B["q3_error_pp"] = span([p2(v["errs"]["FY2025 Q3"]) for v in fam.values()], 0.2)
    B["forecast_m"] = span([m1(v["forecast"]) for v in fam.values()], 3.0, 1)
    B["range_low_m"] = span([m1(v["low"]) for v in fam.values()], 3.0, 1)
    B["range_high_m"] = span([m1(v["high"]) for v in fam.values()], 3.0, 1)
    F["bands"] = B
    # one key per result: the result's golden as effort.json carries it
    F["r1_panel"] = {k: v for k, v in F["bridge_pp"][:4]}
    F["r2_visible"] = F["visible_growth_pct"]
    F["r3_tender"] = {"pl_target_pct": F["pl_target_pct"], "drift_pct": F["drift_pct"]}
    F["r4_deposits"] = {"deposits_q4_m": F["deposits_q4_m"], "revenue on delivery": dict(F["bridge_pp"])["revenue on delivery"]}
    F["r5_wholesale"] = {"wholesale_q4_m": F["wholesale_q4_m"],
                         "wholesale at its run rate": dict(F["bridge_pp"])["wholesale at its run rate"]}
    F["r6_record"] = {"golden_rmse_pp": F["golden_rmse_pp"], "q3_error_pp": F["q3_error_pp"]}
    F["r7_forecast"] = {"forecast_m": F["forecast_m"], "range_low_m": F["range_low_m"], "range_high_m": F["range_high_m"]}
    F["r8_bridge"] = {k: v for k, v in F["bridge_pp"][4:]}
    F["r9_call"] = {"call": F["call"], "range_high_m": F["range_high_m"]}
    return F


def effort(F, R):
    B = F["bands"]
    S = R["shortcuts"]
    c = S["careful"]
    bk = [k for k, _ in F["bridge_pp"]]
    res = [
        dict(id="R1", name="the panel's own steps: delivered growth, the latest weeks completed, the licensed shops and "
                           "cafes out, issuers in both years and cards of the same age", graded_as="Ask 3 (panel steps)",
             figure="r1_panel", depends=[], independent="the panel, its delivery history and descriptor detail",
             golden=F["r1_panel"], bands={k: B["bridge_pp"][k] for k in bk[:4]},
             passes={"quick": {bk[0]: F["r1_panel"][bk[0]], bk[1]: 0.0, bk[2]: 0.0, bk[3]: 0.0},
                     "careful": F["r1_panel"], "thorough": F["r1_panel"]}),
        dict(id="R2", name="card-visible growth at the company's regional mix", graded_as="Component 1", figure="r2_visible",
             depends=["R1"], independent="", golden=F["r2_visible"], band=B["visible_growth_pct"],
             passes={"quick": F["bridge_pp"][0][1], "careful": F["r2_visible"], "thorough": F["r2_visible"]}),
        dict(id="R3", name="the private-label card's fourth-quarter share and net sales per bank-card dollar",
             graded_as="Component 2", figure="r3_tender", depends=[], independent="the filing excerpts and the panel's coverage",
             golden=F["r3_tender"], bands={"pl_target_pct": B["pl_target_pct"], "drift_pct": B["drift_pct"]},
             passes={"quick": None, "careful": F["r3_tender"], "thorough": F["r3_tender"]}),
        dict(id="R4", name="customer deposits at the quarter's end and what revenue on delivery is worth",
             graded_as="Component 3", figure="r4_deposits", depends=["R2", "R3"], independent="",
             golden=F["r4_deposits"], bands={"deposits_q4_m": B["deposits_q4_m"],
                                             "revenue on delivery": B["bridge_pp"]["revenue on delivery"]},
             passes={"quick": None, "careful": {"deposits_q4_m": None, "revenue on delivery": 0.0},
                     "thorough": F["r4_deposits"]},
             precedent=["N02", "L07"]),
        dict(id="R5", name="wholesale at its run rate and what separating it is worth", graded_as="Component 4",
             figure="r5_wholesale", depends=[], independent="the quarterly results",
             golden=F["r5_wholesale"], bands={"wholesale_q4_m": B["wholesale_q4_m"],
                                              "wholesale at its run rate": B["bridge_pp"]["wholesale at its run rate"]},
             passes={"quick": None, "careful": {"wholesale_q4_m": None, "wholesale at its run rate": 0.0},
                     "thorough": F["r5_wholesale"]},
             precedent=["L10", "L11"]),
        dict(id="R6", name="the range's record: rolling-origin error and the third quarter's miss", graded_as="Ask 2",
             figure="r6_record", depends=["R4", "R5"], independent="", golden=F["r6_record"],
             bands={"golden_rmse_pp": B["golden_rmse_pp"], "q3_error_pp": B["q3_error_pp"]},
             passes={"quick": None, "careful": {"golden_rmse_pp": p2(c["rmse"]), "q3_error_pp": F["careful_q3_error_pp"]},
                     "thorough": F["r6_record"]},
             precedent=["L28"]),
        dict(id="R7", name="the quarter's net sales with its 80 per cent range", graded_as="Ask 1", figure="r7_forecast",
             depends=["R4", "R5", "R6"], independent="", golden=F["r7_forecast"],
             bands={"forecast_m": B["forecast_m"], "range_low_m": B["range_low_m"], "range_high_m": B["range_high_m"]},
             passes={"quick": {"forecast_m": F["shortcut_m"]["quick"], "range_low_m": None, "range_high_m": None},
                     "careful": {"forecast_m": m1(c["forecast"]), "range_low_m": m1(c["low"]), "range_high_m": m1(c["high"])},
                     "thorough": F["r7_forecast"]},
             precedent=["L28", "N02"]),
        dict(id="R8", name="what the regional mix, the bank-card share, revenue on delivery and wholesale are worth",
             graded_as="Ask 3 (company steps)", figure="r8_bridge", depends=["R2", "R3", "R4", "R5"], independent="",
             golden=F["r8_bridge"], bands={k: B["bridge_pp"][k] for k in bk[4:]},
             passes={"quick": None, "careful": {bk[4]: F["r8_bridge"][bk[4]], bk[5]: F["r8_bridge"][bk[5]],
                                                bk[6]: 0.0, bk[7]: 0.0},
                     "thorough": F["r8_bridge"]},
             precedent=["L11", "N02"]),
        dict(id="R9", name="the call against the street", graded_as="Recommendation", figure="r9_call",
             depends=["R7"], independent="", golden=F["r9_call"], bands={"range_high_m": B["range_high_m"]},
             passes={"quick": {"call": "short", "range_high_m": None},
                     "careful": {"call": F["shortcut_call"]["careful"], "range_high_m": m1(c["high"])},
                     "thorough": F["r9_call"]},
             precedent=["L28", "N02"]),
    ]
    hints = [
        {"sentence": "net sales are recognised on delivery, and the December made-to-order orders are still in customer "
                     "deposits at the quarter's end", "rescues": ["R4"]},
        {"sentence": "last year's fourth quarter carried a large wholesale contract the card panel cannot see",
         "rescues": ["R5"]},
        {"sentence": "the private-label card's share of sales has fallen faster in fiscal 2025, and the panel holds no "
                     "private-label cards", "rescues": []},
    ]
    names = {"careful": "issuers in both years, cards of the same age, the company's regional mix and the bank-card share, "
                        "net sales taken as what the panel shows (careful but hurried)",
             "careful_regressed": "the same, reported growth regressed on it over past quarters",
             "panel_regressed": "the panel's own mix regressed on past quarters",
             "deposits_only": "revenue on delivery without separating wholesale",
             "wholesale_only": "wholesale separated, net sales taken as payments",
             "deposit_ratio": "deposits at the third quarter's weeks of payments",
             "last_year_deposits": "deposits moved as they did a year earlier",
             "no_mix": "everything but the company's regional mix",
             "no_tender": "everything but the bank-card share",
             "desk_model": "the desk's third-quarter model carried to the fourth quarter",
             "trend": "fiscal 2025's reported growth carried into the quarter",
             "trend_retail": "fiscal 2025's retail growth carried, wholesale at its run rate",
             "quick": "the delivered panel's change on last year's quarter (quick)"}
    routes = [dict(name="golden", golden=True, answer=[F["forecast_m"], F["call"]])]
    for k in names:
        routes.append(dict(name=names[k], answer=[F["shortcut_m"][k], F["shortcut_call"][k]]))
    forcing = dict(kind="numeric", line=F["street_m"], golden_side="below",
                   golden_family=[dict(name=k, value=v) for k, v in F["family_high_m"].items()],
                   shortcuts=[dict(name=names[k], value=F["shortcut_high_m"][k]) for k in names if k != "quick"],
                   perturbations=[dict(input=k, value=v) for k, v in F["perturb_m"].items()],
                   notes="Values are the top of each route's 80 per cent range (the call is short only while the whole "
                         "range sits below the street's figure). The quick route (%.1f) lands short for the wrong reason, "
                         "the issuer that left, and is graded at R1 to R8." % F["shortcut_m"]["quick"])
    return {"results": res, "hints": hints, "routes": routes, "forcing": forcing}


def write(R, gen_dir=HERE):
    F = make(R)
    E = effort(F, R)
    json.dump(F, open(os.path.join(gen_dir, "figures.json"), "w"), indent=1, sort_keys=True)
    json.dump(E, open(os.path.join(gen_dir, "effort.json"), "w"), indent=1)
    return F, E
