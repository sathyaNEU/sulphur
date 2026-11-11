"""task20 architecture 2: submission.md, the four answer blocks and the tags, every figure from figures.json."""
import golden as GD


def usd(x):
    return "USD {:,.1f} million".format(x)


def q(k):
    return k.replace("FY", "fiscal ").replace(" Q", " Q")


def text(F):
    br = F["bridge_pp"]
    rg, cw, pw = F["regional_pct"], F["company_weights_pct"], F["panel_weights_pct"]
    e = F["errors_pp"]
    sm, sh, sl, sc = F["shortcut_m"], F["shortcut_high_m"], F["shortcut_low_m"], F["shortcut_pct"]
    hi = F["family_high_m"]
    B = F["bands"]
    bb = B["bridge_pp"]
    L = []
    L.append("# task20 submission: Brindle & Moss's fourth-quarter fiscal 2025 net sales from the Kestrel card panel, "
             "against the street's figure")
    L.append("")
    L.append("## Tags")
    L.append("")
    L.append("**Domain:** Quantitative Finance and Trading, Quantitative Finance (alternative data: a card-transaction "
             "panel's nowcast of a listed retailer's quarterly net sales, validated on rolling origins, against the "
             "consensus).")
    L.append("**Analytical objective:** Forecasting & Predictive Modeling.")
    L.append("")
    L.append("## Final Recommendation")
    L.append("")
    L.append("**Short Brindle & Moss into the %s release of its fiscal 2025 fourth quarter: net sales of %s "
             "(%.2f%% above %s a year earlier), with an 80%% range of USD %s to %s million that sits wholly below the "
             "street's %s.** This rejects the panel's own read (issuers in both years and cards of the same age at the "
             "panel's mix, reported growth regressed on it: %s, a beat), the desk's third-quarter model carried forward "
             "(%s), and fiscal 2025's reported growth carried into the quarter (%.2f%%, %s)."
             % (F["release"], usd(F["forecast_m"]), F["growth_pct"], usd(F["base_net_sales_m"]),
                "{:,.1f}".format(F["range_low_m"]), "{:,.1f}".format(F["range_high_m"]), usd(F["street_m"]),
                usd(sm["careful"]), usd(sm["desk_model"]), sc["trend"], usd(sm["trend"])))
    L.append("")
    L.append("## Supplementary Questions")
    L.append("")
    L.append("### %s" % GD.XLSX)
    L.append("")
    L.append("1. The quarter's net sales with its 80%% range, on a Call sheet: %s (band USD %s to %s million), growth "
             "%.2f%% on %s, range from USD %s million (band USD %s to %s million) to USD %s million (band USD %s to %s "
             "million), the range being the estimate plus and minus 1.2816 times the record's root mean square error (%.2f points of "
             "growth), and the street's %s (the mean of %d estimates; median %s)."
             % (usd(F["forecast_m"]), "{:,.1f}".format(B["forecast_m"][0]), "{:,.1f}".format(B["forecast_m"][1]),
                F["growth_pct"], usd(F["base_net_sales_m"]), "{:,.1f}".format(F["range_low_m"]),
                "{:,.1f}".format(B["range_low_m"][0]), "{:,.1f}".format(B["range_low_m"][1]),
                "{:,.1f}".format(F["range_high_m"]), "{:,.1f}".format(B["range_high_m"][0]),
                "{:,.1f}".format(B["range_high_m"][1]), F["band_pp"], usd(F["street_m"]), F["street_n"],
                usd(F["street_median_m"])))
    L.append("2. How the range would have held, on a Record sheet with one row per quarter from %s to %s (the "
             "estimate built as it would have been three weeks before each release, reported growth, the error, and "
             "whether it fell inside): root mean square error %.2f points (%.2f to %.2f), %d of %d quarters inside, "
             "errors of %.2f, %.2f and %.2f points in the three quarters of fiscal 2025 (the third quarter's %.2f to "
             "%.2f). The regression on the panel at its own mix, set beside it, has a root mean square error of %.2f "
             "points and missed the third quarter by %.2f."
             % (q(F["first_origin"]), q(F["last_origin"]), F["golden_rmse_pp"], B["golden_rmse_pp"][0],
                B["golden_rmse_pp"][1], F["coverage_in"], F["origins"], e["FY2025 Q1"], e["FY2025 Q2"], e["FY2025 Q3"],
                B["q3_error_pp"][0], B["q3_error_pp"][1], F["shortcut_rmse_pp"]["careful"], F["careful_q3_error_pp"]))
    steps = "; ".join("%s %+.2f (%.2f to %.2f)" % (k, v, bb[k][0], bb[k][1]) for k, v in br)
    L.append("3. What each adjustment to the card data is worth in points of year-on-year growth, on a Bridge sheet, "
             "in the order applied: %s; growth after the panel's own steps %.2f%%, at the company's mix %.2f%%, and "
             "%.2f%% after the bank-card share. A Regions sheet gives each billing region's growth on cards of the same "
             "age (Northeast %.2f%%, Southeast %.2f%%, Midwest %.2f%%, West %.2f%%) beside the panel's weights (%.2f, "
             "%.2f, %.2f, %.2f) and the company's fiscal 2024 weights (%.2f, %.2f, %.2f, %.2f); a Tender sheet the "
             "private-label share by quarter to %.1f%% in the third quarter and %.2f%% carried for the fourth (%.2f to "
             "%.2f), net sales per dollar of bank-card spend %.2f%% (%.2f to %.2f); a Completion sheet each issuer's first-delivered "
             "shares and the licensed shops' and cafes' %.2f%% of the brand id's spend (%.2f to %.2f)."
             % (steps, br[0][1] + br[1][1] + br[2][1] + br[3][1], F["visible_growth_pct"], F["growth_pct"],
                rg["Northeast"], rg["Southeast"], rg["Midwest"], rg["West"], pw["Northeast"], pw["Southeast"],
                pw["Midwest"], pw["West"], cw["Northeast"], cw["Southeast"], cw["Midwest"], cw["West"],
                F["pl_q3fy25_pct"], F["pl_target_pct"], B["pl_target_pct"][0], B["pl_target_pct"][1], F["drift_pct"],
                B["drift_pct"][0], B["drift_pct"][1], F["excluded_share_pct"], B["excluded_share_pct"][0],
                B["excluded_share_pct"][1]))
    L.append("4. The call on the Call sheet: short, because the top of the range (%s) sits %s below the street's figure; "
             "every reasonable rival keeps the top between USD %s and %s million."
             % (usd(F["range_high_m"]), usd(F["range_gap_m"]), "{:,.1f}".format(min(hi.values())),
                "{:,.1f}".format(max(hi.values()))))
    L.append("")
    L.append("### %s" % GD.NOTE)
    L.append("")
    L.append("5. One page to the portfolio manager from the consumer analyst: the call and the estimate with its range "
             "against the street, the bridge from the delivered panel to net sales, a paragraph on why the panel's own "
             "read is a beat and this quarter is not (the issuer that left and the regions it leaves; the private-label "
             "card's faster fall), the record, and what would change the call.")
    L.append("")
    L.append("## Critical Components")
    L.append("")
    L.append("1. The licensed shop-in-shops and cafes are **%.2f%%** of the brand merchant id's spend in November to "
             "January and are not net sales; taking them out is worth **%.2f** points."
             % (F["excluded_share_pct"], br[2][1]))
    L.append("2. Completing the quarter's latest weeks from the delivery history (each issuer's first-delivered share of "
             "its final week) lifts the quarter's spend by **%.2f%%**." % F["completion_pct"])
    L.append("3. On issuers in both years and cards of the same age the panel grew **%.2f%%** at its own mix, which is "
             "%.0f%% Southeast and %.0f%% West once KS-06 has left; at the company's fiscal 2024 regional mix the card-"
             "visible growth is **%.2f%%**." % (F["pooled_growth_pct"], pw["Southeast"], pw["West"],
                                               F["visible_growth_pct"]))
    L.append("4. The private-label card, which the panel does not hold, is carried to **%.2f%%** of net sales for the "
             "quarter (%.1f%% a year earlier, %.1f%% in the third quarter), so bank cards pay for %.1f%% of net sales "
             "against %.1f%% a year earlier and each dollar the panel sees stands for **%.2f%%** less net sales, worth "
             "**%.2f** points of growth."
             % (F["pl_target_pct"], F["pl_q4fy24_pct"], F["pl_q3fy25_pct"], F["bank_target_pct"], F["bank_q4fy24_pct"],
                F["drift_less_pct"], br[5][1]))
    L.append("")
    L.append("## Step-by-Step")
    L.append("")
    L.append("1. The delivered panel, every issuer and merchant id, against the fourth quarter of fiscal 2024: %.2f%%, "
             "mostly KS-06, whose last delivered week began 26 October 2025, and the latest weeks still posting."
             % br[0][1])
    L.append("2. Each issuer's first-delivered share of a week's final spend at lags 0 to 2, from the delivery history "
             "(medians over 27 deliveries), completes the latest weeks: %+.2f points (the quarter's spend %+.2f%%)."
             % (br[1][1], F["completion_pct"]))
    L.append("3. The descriptor detail shows the Hollister's shop-in-shops and the cafes under the brand id; the filing "
             "says their sales are the licensees', so their share comes out by month (%.2f%% of the quarter): %+.2f "
             "points. Fernhollow is consolidated in both quarters and stays." % (F["excluded_share_pct"], br[2][1]))
    L.append("4. Issuers in both quarters (KS-01 to KS-05) and each card-open year set against the open year one later, "
             "on the base quarter's cards: %+.2f points, like-for-like growth %.2f%%." % (br[3][1], F["pooled_growth_pct"]))
    L.append("5. The hurried analysis stops here and regresses reported growth on this over past quarters: %.2f%%, %s, "
             "range USD %s to %s million, a beat, with a back-test that looks sound (root mean square error %.2f points) "
             "because none of its quarters held an issuer's exit or the private-label card's faster fall; it missed the "
             "third quarter by %.2f points."
             % (sc["careful"], usd(sm["careful"]), "{:,.1f}".format(sl["careful"]), "{:,.1f}".format(sh["careful"]),
                F["shortcut_rmse_pp"]["careful"], F["careful_q3_error_pp"]))
    L.append("6. The filing's net sales by region for fiscal 2024 weight each region's growth (Northeast %.2f%%, "
             "Southeast %.2f%%, Midwest %.2f%%, West %.2f%%): %.2f%%, %+.2f points."
             % (rg["Northeast"], rg["Southeast"], rg["Midwest"], rg["West"], F["visible_growth_pct"], br[4][1]))
    L.append("7. The panel holds no private-label cards, and the filing's penetration stood at %.1f%% and %.1f%% in "
             "fiscal 2024's third and fourth quarters and %.1f%%, %.1f%% and %.1f%% in fiscal 2025's first three; carried "
             "at fiscal 2025's pace it is %.2f%% this quarter, and with the 10-K's 12%% of other tenders bank cards pay "
             "for %.1f%% of net sales against %.1f%%, so net sales per dollar of bank-card spend change %.2f%%: growth "
             "%.2f%%, %+.2f points."
             % (F["pl_q3fy24_pct"], F["pl_q4fy24_pct"], F["pl_q1fy25_pct"], F["pl_q2fy25_pct"], F["pl_q3fy25_pct"],
                F["pl_target_pct"], F["bank_target_pct"], F["bank_q4fy24_pct"], F["drift_pct"], F["growth_pct"], br[5][1]))
    L.append("8. The same chain at each of the %d quarters from %s to %s, on what was known then: root mean square "
             "error %.2f points, %d inside; the range is %s plus and minus %.2f points, USD %s to %s million."
             % (F["origins"], q(F["first_origin"]), q(F["last_origin"]), F["golden_rmse_pp"], F["coverage_in"],
                usd(F["forecast_m"]), F["band_pp"], "{:,.1f}".format(F["range_low_m"]), "{:,.1f}".format(F["range_high_m"])))
    L.append("")
    L.append("No other conclusion survives. Either correction alone leaves the range across the street (the regional mix "
             "alone, regressed on past quarters, USD %s to %s million; the bank-card share alone USD %s to %s million, or "
             "regressed on past quarters USD %s to %s million); every reasonable rival (the private-label rules, the fiscal 2023 or rolled-forward "
             "mix, the chain calibrated by regression) keeps the top between USD %s and %s million; and other tenders "
             "at 10 or 14%%, the last week's completeness 3%% either way and the licensed share a fifth either way keep "
             "it between USD %s and %s million."
             % ("{:,.1f}".format(sl["mix_only"]), "{:,.1f}".format(sh["mix_only"]), "{:,.1f}".format(sl["drift_only"]),
                "{:,.1f}".format(sh["drift_only"]), "{:,.1f}".format(sl["drift_regressed"]),
                "{:,.1f}".format(sh["drift_regressed"]), "{:,.1f}".format(min(hi.values())),
                "{:,.1f}".format(max(hi.values())), "{:,.1f}".format(min(F["perturb_m"].values())),
                "{:,.1f}".format(max(F["perturb_m"].values()))))
    L.append("")
    return "\n".join(L)
