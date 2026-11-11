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
    br = dict(R["bridge"])
    bk = [k for k, _ in R["bridge"]]
    errs = G["errs"]
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
        "range_low_m": m1(G["low"]),
        "range_high_m": m1(G["high"]),
        "band_pp": p2(G["band"]),
        "range_gap_m": m1(m1(R["street"]) - m1(G["high"])),
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
        "pl_q4fy24_pct": float(R["P"]["pl"]["FY2024 Q4"]),
        "pl_q3fy24_pct": float(R["P"]["pl"]["FY2024 Q3"]),
        "pl_q1fy25_pct": float(R["P"]["pl"]["FY2025 Q1"]),
        "pl_q2fy25_pct": float(R["P"]["pl"]["FY2025 Q2"]),
        "pl_q3fy25_pct": float(R["P"]["pl"]["FY2025 Q3"]),
        "drift_pct": p2(R["drift"] - 1),
        "drift_less_pct": p2(1 - R["drift"]),
        "bank_q4fy24_pct": float(round(100 * A.bank_share(R["P"]["pl"]["FY2024 Q4"]), 1)),
        "bank_target_pct": float(round(100 * A.bank_share(R["pl_target"]), 1)),
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
        "organic_pct": {k: p2(v) for k, v in R["organic"].items()},
        "incumbent": {"intercept_pp": p2(R["incumbent"]["fit"][0]), "slope": float(round(R["incumbent"]["fit"][1], 3)),
                      "rmse_pp": p2(R["incumbent"]["rmse"]), "q3_x_pct": p2(R["incumbent"]["x_q3"]),
                      "q3_growth_pct": p2(R["incumbent"]["g_q3"]), "q3_forecast_m": m1(R["incumbent"]["q3_forecast"]),
                      "q3_actual_m": m1(R["incumbent"]["q3_actual"])},
        "perturb_m": {k: m1(v) for k, v in R["perturb"].items()},
        "call": R["call"],
        "constants": {"range_pct": 80, "z80": A.Z80, "other_tender_pct": 12, "weeks": 13, "fy2024_tender": "67, 21 and 12",
                      "section_refs": "1 2 3 4 5 6 7 8 9"},
    }
    # bands: each result's rivals, run on the cut pack, plus a margin
    B = {}
    B["excluded_share_pct"] = span([p2(R["excluded_share"])], 0.5)
    B["completion_pct"] = span([p2(v) for v in V["completion"].values()] + [F["completion_pct"]], 0.3)
    B["bridge_pp"] = {bk[0]: span([p2(br[bk[0]])], 0.3),
                      bk[1]: span([p2(br[bk[1]]), p2(R["bridge_rivals"][bk[1]])], 0.3),
                      bk[2]: span([p2(br[bk[2]]), p2(R["bridge_rivals"][bk[2]])], 0.3),
                      bk[3]: span([p2(br[bk[3]]), p2(V["comparable"]["spend per card"])], 0.3),
                      bk[4]: span([p2(v) for v in V["mix_step"].values()], 0.3),
                      bk[5]: span([p2(v) for v in V["tender_step"].values()], 0.3)}
    B["visible_growth_pct"] = span([p2(v) for v in V["visible"].values()], 0.3)
    B["pl_target_pct"] = span([float(round(v, 2)) for v in V["pl"].values()], 0.2)
    B["drift_pct"] = span([p2(v) for v in V["drift"].values()], 0.3)
    B["golden_rmse_pp"] = span([p2(v["rmse"]) for v in fam.values()], 0.15)
    B["q3_error_pp"] = span([p2(v["errs"]["FY2025 Q3"]) for v in fam.values()], 0.2)
    B["forecast_m"] = span([m1(v["forecast"]) for v in fam.values()], 3.0, 1)
    B["range_low_m"] = span([m1(v["low"]) for v in fam.values()], 3.0, 1)
    B["range_high_m"] = span([m1(v["high"]) for v in fam.values()], 3.0, 1)
    F["bands"] = B
    # one key per result: the result's golden as effort.json carries it
    F["r1_entity"] = F["excluded_share_pct"]
    F["r2_completion"] = F["completion_pct"]
    F["r3_panel"] = {k: v for k, v in F["bridge_pp"][:4]}
    F["r4_visible"] = F["visible_growth_pct"]
    F["r5_tender"] = {"pl_target_pct": F["pl_target_pct"], "drift_pct": F["drift_pct"]}
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
        dict(id="R1", name="the reporting entity: the licensed shops' and cafes' share of the brand id's quarter",
             graded_as="Component 1", figure="r1_entity", depends=[], independent="the descriptor detail and the filing",
             golden=F["r1_entity"], band=B["excluded_share_pct"],
             passes={"quick": 0.0, "careful": F["r1_entity"], "thorough": F["r1_entity"]}),
        dict(id="R2", name="the quarter's latest weeks completed from the delivery history", graded_as="Component 2",
             figure="r2_completion", depends=[], independent="the delivery history", golden=F["r2_completion"],
             band=B["completion_pct"], passes={"quick": 0.0, "careful": F["r2_completion"], "thorough": F["r2_completion"]}),
        dict(id="R3", name="the panel's own adjustments and its like-for-like growth", graded_as="Ask 3 (panel steps)",
             figure="r3_panel", depends=["R1", "R2"], independent="", golden=F["r3_panel"],
             bands={k: B["bridge_pp"][k] for k in bk[:4]},
             passes={"quick": {bk[0]: F["r3_panel"][bk[0]], bk[1]: 0.0, bk[2]: 0.0, bk[3]: 0.0},
                     "careful": F["r3_panel"], "thorough": F["r3_panel"]}),
        dict(id="R4", name="card-visible growth at the company's regional mix", graded_as="Component 3", figure="r4_visible",
             depends=["R3"], independent="", golden=F["r4_visible"], band=B["visible_growth_pct"],
             passes={"quick": F["bridge_pp"][0][1], "careful": F["pooled_growth_pct"], "thorough": F["r4_visible"]},
             precedent=["L11", "L25"]),
        dict(id="R5", name="the private-label card's fourth-quarter share and the bank-card share's change",
             graded_as="Component 4", figure="r5_tender", depends=[], independent="the filing excerpts and the panel's coverage",
             golden=F["r5_tender"], bands={"pl_target_pct": B["pl_target_pct"], "drift_pct": B["drift_pct"]},
             passes={"quick": None, "careful": {"pl_target_pct": F["pl_q3fy25_pct"], "drift_pct": 0.0},
                     "thorough": F["r5_tender"]},
             precedent=["N02", "N06"]),
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
        dict(id="R8", name="what the regional mix and the bank-card share are worth", graded_as="Ask 3 (company steps)",
             figure="r8_bridge", depends=["R4", "R5"], independent="", golden=F["r8_bridge"],
             bands={k: B["bridge_pp"][k] for k in bk[4:]},
             passes={"quick": None, "careful": {bk[4]: 0.0, bk[5]: 0.0}, "thorough": F["r8_bridge"]},
             precedent=["L11", "N06"]),
        dict(id="R9", name="the call against the street", graded_as="Recommendation", figure="r9_call",
             depends=["R7"], independent="", golden=F["r9_call"], bands={"range_high_m": B["range_high_m"]},
             passes={"quick": {"call": "short", "range_high_m": None},
                     "careful": {"call": F["shortcut_call"]["careful"], "range_high_m": m1(c["high"])},
                     "thorough": F["r9_call"]},
             precedent=["L28", "N02"]),
    ]
    hints = [
        {"sentence": "the private-label card's share of net sales has fallen faster in fiscal 2025 than before, and the "
                     "panel holds no private-label cards", "rescues": ["R5"]},
        {"sentence": "the panel's cardholders sit in different regions from the company's sales", "rescues": ["R4"]},
        {"sentence": "the back-test's quarters never held an issuer leaving the panel", "rescues": []},
    ]
    names = {"careful": "issuers in both years and cards of the same age at the panel's mix, reported growth regressed on "
                        "it over past quarters (careful but hurried)",
             "mix_only": "the company's regional mix, regressed on past quarters, no bank-card share",
             "drift_only": "the bank-card share carried at the panel's own mix",
             "drift_regressed": "the bank-card share carried at the panel's mix, regressed on past quarters",
             "raw_regressed": "issuers in both years, total spend, regressed on past quarters",
             "desk_model": "the desk's third-quarter model carried to the fourth quarter",
             "trend": "fiscal 2025's reported growth carried into the fourth quarter",
             "quick": "the delivered panel's change on last year's quarter (quick)"}
    routes = [dict(name="golden", golden=True, answer=[F["forecast_m"], F["call"]])]
    for k in names:
        routes.append(dict(name=names[k], answer=[F["shortcut_m"][k], F["shortcut_call"][k]]))
    forcing = dict(kind="numeric", line=F["street_m"], golden_side="below",
                   golden_family=[dict(name=k, value=v) for k, v in F["family_high_m"].items()],
                   shortcuts=[dict(name=names[k], value=F["shortcut_high_m"].get(k, F["shortcut_m"][k]))
                              for k in ("careful", "mix_only", "drift_only", "drift_regressed", "raw_regressed",
                                        "desk_model", "trend")],
                   perturbations=[dict(input=k, value=m1(v)) for k, v in R["perturb"].items()],
                   notes="Values are the top of each route's 80 per cent range (the call is short only while the whole "
                         "range sits below the street's figure); the trend route has no range and is its point. The quick "
                         "route (%.1f) lands short for the wrong reason, the issuer that left, and is graded at R1 to R8."
                         % F["shortcut_m"]["quick"])
    return {"results": res, "hints": hints, "routes": routes, "forcing": forcing}


def write(R, gen_dir=HERE):
    F = make(R)
    E = effort(F, R)
    json.dump(F, open(os.path.join(gen_dir, "figures.json"), "w"), indent=1, sort_keys=True)
    json.dump(E, open(os.path.join(gen_dir, "effort.json"), "w"), indent=1)
    return F, E
