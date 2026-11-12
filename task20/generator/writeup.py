"""task20 architecture 2 (second hardening): submission.md, the four answer blocks and the tags, every figure from figures.json."""
import golden as GD


def usd(x):
    return "USD {:,.1f} million".format(x)


def mn(x):
    return "{:,.1f}".format(x)


def q(k):
    return k.replace("FY", "fiscal ").replace(" Q", " Q")


def text(F):
    br = dict(F["bridge_pp"])
    bl = F["bridge_pp"]
    rg, rk = F["regional_pct"], F["regional_with_ks01_pct"]
    cw, pw = F["company_weights_pct"], F["panel_weights_pct"]
    e = F["errors_pp"]
    sm, sh, sl = F["shortcut_m"], F["shortcut_high_m"], F["shortcut_low_m"]
    hi = F["family_high_m"]
    B = F["bands"]
    bb = B["bridge_pp"]
    sign = "below" if F["growth_pct"] < 0 else "above"
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
    L.append("**Short Brindle & Moss into the %s release of its fiscal 2025 fourth quarter: net sales of %s, %.2f%% %s the "
             "%s of a year earlier, with an 80%% range of USD %s to %s million that sits wholly below the street's %s.** "
             "This rejects the panel's like-for-like read taken to net sales (issuers in both quarters on spend per "
             "card at the company's regional mix, %s, a beat), the same with any one of the three corrections left out "
             "(KS-01's re-issued book kept, %s; the December custom orders counted as sales, %s; last year's contract "
             "delivery grown with retail, %s; each no position), and the desk's third-quarter model carried forward (%s)."
             % (F["release"], usd(F["forecast_m"]), F["growth_abs_pct"], sign, usd(F["base_net_sales_m"]),
                mn(F["range_low_m"]), mn(F["range_high_m"]), usd(F["street_m"]), usd(sm["careful"]),
                usd(sm["no_reissue"]), usd(sm["no_deposits"]), usd(sm["no_contract"]), usd(sm["desk_model"])))
    L.append("")
    L.append("## Supplementary Questions")
    L.append("")
    L.append("### %s" % GD.XLSX)
    L.append("")
    L.append("1. The quarter's net sales with its 80%% range, on a Call sheet: %s (band USD %s to %s million), growth "
             "%.2f%% on %s, range from USD %s million (band USD %s to %s million) to USD %s million (band USD %s to %s "
             "million), the range being the estimate plus and minus 1.2816 times the record's root mean square error "
             "(%.2f points of growth), and the street's %s (the mean of %d estimates; median %s)."
             % (usd(F["forecast_m"]), mn(B["forecast_m"][0]), mn(B["forecast_m"][1]), F["growth_pct"],
                usd(F["base_net_sales_m"]), mn(F["range_low_m"]), mn(B["range_low_m"][0]), mn(B["range_low_m"][1]),
                mn(F["range_high_m"]), mn(B["range_high_m"][0]), mn(B["range_high_m"][1]), F["band_pp"],
                usd(F["street_m"]), F["street_n"], usd(F["street_median_m"])))
    errs = "; ".join("%s %+.2f (%.2f to %.2f)" % (q(k), v, B["errors_pp"][k][0], B["errors_pp"][k][1])
                     for k, v in e.items())
    L.append("2. How the range would have held, on a Record sheet with one row per quarter from %s to %s: the estimate "
             "built as it would have been three weeks before each release (the panel as delivered on 2 February 2026, "
             "whose weeks before the latest are complete; the issuers in every week of both quarters less any with a "
             "re-issued book between them; the regional mix of the fiscal year before; deposits and contract from the "
             "releases before that quarter's), reported growth, the error in points of year-on-year growth, and whether "
             "it fell inside. The errors: %s. Root mean square error %.2f points (%.2f to %.2f); %d of %d quarters "
             "inside the range at that error (%d to %d), and %d of the %d quarters from %s inside a range built only on "
             "the errors before each (%d to %d); the largest miss %.2f points in %s. "
             "The panel's like-for-like growth taken straight to net sales, set beside it, has a root mean square error "
             "of %.2f points and misses the third quarter of fiscal 2025 by %.2f."
             % (q(F["first_origin"]), q(F["last_origin"]), errs, F["golden_rmse_pp"], B["golden_rmse_pp"][0],
                B["golden_rmse_pp"][1], F["coverage_in"], F["origins"], B["coverage_in"][0], B["coverage_in"][1],
                F["coverage_asof_in"], F["coverage_asof_n"], q(F["first_asof_origin"]), B["coverage_asof_in"][0],
                B["coverage_asof_in"][1], F["largest_miss_pp"], q(F["largest_miss_q"]),
                F["shortcut_rmse_pp"]["careful"], F["careful_q3_error_pp"]))
    steps = "; ".join("%s %+.2f (%.2f to %.2f)" % (k, v, bb[k][0], bb[k][1]) for k, v in bl)
    L.append("3. What each step from the card data to net sales is worth in points of year-on-year growth (weekly "
             "averages), on a Bridge sheet, from the delivered panel's growth on the same quarter a year earlier (every "
             "issuer, raw spend, the panel's own regional weights) to net sales, in the order applied: the panel's three "
             "steps first, at the panel's own regional weights with KS-01 kept, then the company's four at the company's "
             "weights; each band covers every order of the steps within its group: %s; growth after the panel's own steps %.2f%%, at the company's mix %.2f%%, "
             "without KS-01's book %.2f%%, retail net sales %.2f%%, net sales %.2f%%. A Regions sheet gives each billing "
             "region's growth per open card with KS-01 kept and without it (Northeast %.2f%% and %.2f%%, Southeast "
             "%.2f%% and %.2f%%, Midwest %.2f%% and %.2f%%, West %.2f%% and %.2f%%) beside the company's fiscal 2024 "
             "weights (%.2f, %.2f, %.2f, %.2f); an Issuers sheet KS-01's Midwest cards week by week (up %.2f%% in the "
             "four weeks to 26 October 2025); a Deposits sheet the deposits at each quarter end, the custom-order share "
             "of the brand's spend in the last eight weeks (%.2f%% against %.2f%% a year earlier) and the quarter's "
             "closing deposits of %s (USD %s to %s million) against %s at the end of the third quarter; a Contract sheet "
             "each quarter's contract sales, last year's fourth quarter of %s (USD %s to %s million) as the fiscal "
             "year's %s less the nine months' %s, and this quarter's run rate of %s (USD %s to %s million)."
             % (steps, F["pooled_with_ks01_pct"], F["visible_with_ks01_pct"], F["visible_growth_pct"],
                F["retail_growth_pct"], F["growth_pct"], rk["Northeast"], rg["Northeast"], rk["Southeast"],
                rg["Southeast"], rk["Midwest"], rg["Midwest"], rk["West"], rg["West"], cw["Northeast"],
                cw["Southeast"], cw["Midwest"], cw["West"], F["ks01_mw_cards_rise_pct"], F["custom_q4_pct"],
                F["custom_base_pct"], usd(F["deposits_q4_m"]), mn(B["deposits_q4_m"][0]), mn(B["deposits_q4_m"][1]),
                usd(F["deposits_q3_m"]), usd(F["contract_base_m"]), mn(B["contract_base_m"][0]),
                mn(B["contract_base_m"][1]), usd(F["contract_fy2024_m"]), usd(F["contract_9m_fy2024_m"]),
                usd(F["contract_q4_m"]), mn(B["contract_q4_m"][0]), mn(B["contract_q4_m"][1])))
    L.append("4. The call on the Call sheet: short, because the top of the range (%s) sits %s below the street's figure; "
             "every reasonable rival keeps the top between USD %s and %s million."
             % (usd(F["range_high_m"]), usd(F["range_gap_m"]), mn(min(hi.values())), mn(max(hi.values()))))
    L.append("")
    L.append("### %s" % GD.NOTE)
    L.append("")
    L.append("5. One page to the portfolio manager from the consumer analyst: the call and the estimate with its range "
             "against the street, the bridge from the delivered panel to net sales, a paragraph on why the panel reads a "
             "beat and the quarter is not one (KS-01's re-issued book, the December custom orders still in deposits, "
             "last year's contract delivery), the record, and what would change the call.")
    L.append("")
    L.append("## Critical Components")
    L.append("")
    L.append("1. KS-01's Midwest cards rose **%.2f%%** in the four weeks to 26 October 2025 as KS-06's fell and its feed "
             "ended: a book of re-issued accounts that spend like long-held cards. Kept, it lifts the Midwest's growth "
             "per open card to %.2f%%; without KS-01 the Midwest reads **%.2f%%** and card-visible growth at the "
             "company's fiscal 2024 regional mix is **%.2f%%** (not %.2f%%)."
             % (F["ks01_mw_cards_rise_pct"], rk["Midwest"], rg["Midwest"], F["visible_growth_pct"],
                F["visible_with_ks01_pct"]))
    L.append("2. The panel's own regional weights tilt to the Southeast once KS-06 has left; re-weighting to the "
             "company's fiscal 2024 net sales by region (Midwest **%.2f%%**) is worth **%.2f** points in the order "
             "applied." % (cw["Midwest"], br["the company's regional mix"]))
    L.append("3. Custom orders are paid when placed and recognised on delivery about eight weeks later; their share of the "
             "brand's spend in the quarter's last eight weeks was **%.2f%%** against %.2f%% a year earlier, so customer "
             "deposits close the quarter near **%s** against %s at the end of October, and revenue on delivery is worth "
             "**%.2f** points of growth." % (F["custom_q4_pct"], F["custom_base_pct"], usd(F["deposits_q4_m"]),
                                            usd(F["deposits_q3_m"]), br["revenue on delivery"]))
    L.append("4. Last year's fourth quarter held **%s** of contract sales (the fiscal year's %s less the first nine "
             "months' %s), a delivery no card carries; at this quarter's run rate of **%s**, separating contract from "
             "retail is worth **%.2f** points." % (usd(F["contract_base_m"]), usd(F["contract_fy2024_m"]),
                                                   usd(F["contract_9m_fy2024_m"]), usd(F["contract_q4_m"]),
                                                   br["contract at its run rate"]))
    L.append("")
    L.append("## Step-by-Step")
    L.append("")
    L.append("1. The delivered panel, every issuer and merchant id, moved %+.2f%% on the same quarter a year earlier, "
             "mostly because KS-06's feed ends with the week beginning 26 October 2025 and the latest weeks are still "
             "posting. Region labels differ by issuer feed (NE, NORTHEAST, North East) and are mapped to the four regions."
             % bl[0][1])
    L.append("2. Each issuer's first-delivered share of a week's final spend at lags 0 to 2 (medians over the 27 "
             "deliveries) completes the latest weeks (%+.2f points); the Hollister's shop-in-shops and the cafes, the "
             "licensees' sales, come out of the brand id by month (%+.2f points); the issuers in every week of both "
             "quarters (%s) on spend per open card give like-for-like growth of %.2f%% (%+.2f points)."
             % (bl[1][1], bl[2][1], ", ".join(F["issuers_both"]), F["pooled_with_ks01_pct"], bl[3][1]))
    L.append("3. The 10-K's fiscal 2024 Brindle & Moss net sales by region weight each region's growth: %.2f%% (%+.2f "
             "points). The hurried analysis stops here and files that growth for net sales: %s, range USD %s to %s "
             "million, a beat, with a record (root mean square error %.2f points) that looks sound because no past "
             "comparison held a re-issued book in its largest issuer, a December custom event this large or a base "
             "quarter with a contract delivery this large."
             % (F["visible_with_ks01_pct"], br["the company's regional mix"], usd(sm["careful"]), mn(sl["careful"]),
                mn(sh["careful"]), F["shortcut_rmse_pp"]["careful"]))
    L.append("4. KS-01 is in both quarters but is not the same book: its Midwest cards rose %.2f%% in the four weeks to "
             "26 October as KS-06's fell, and its spend per card rose with them, where cards on an issuer's file move "
             "about one per cent a month (KS-02's Southeast cards jumped the same way, %.2f%% in the four weeks to 21 May 2023). Leaving "
             "KS-01 out, the Midwest reads %.2f%% rather than %.2f%%, and card-visible growth is %.2f%% (%+.2f points)."
             % (F["ks01_mw_cards_rise_pct"], F["ks02_se_rise_pct"], rg["Midwest"], rk["Midwest"],
                F["visible_growth_pct"], br["KS-01's re-issued book taken out"]))
    L.append("5. Customers pay when they order and custom pieces are recognised on delivery, so retail net sales are "
             "payments less the change in customer deposits (the balance sheet line in each release; it runs near eight "
             "weeks of custom orders). Last year's closing deposits (%s), scaled by the brand's payments, the share of "
             "them in the quarter's last eight weeks (%.2f%% against %.2f%%) and the custom-order share of those weeks "
             "(%.2f%% against %.2f%%, the design studios and the site's custom-order descriptor), give %s at the "
             "quarter's end against %s in October: retail net sales %s (%.2f%%, %+.2f points)."
             % (usd(F["deposits_base_m"]), F["trail_q4_pct"], F["trail_base_pct"], F["custom_q4_pct"],
                F["custom_base_pct"], usd(F["deposits_q4_m"]), usd(F["deposits_q3_m"]), usd(F["retail_q4_m"]),
                F["retail_growth_pct"], br["revenue on delivery"]))
    cq = F["contract_by_q"]
    L.append("6. The fourth-quarter releases give contract sales for the fiscal year only: last year's fourth quarter is "
             "%s less the nine months' %s, %s, against a run rate of %s (the median of the last eight quarters). Such "
             "deliveries do not recur: %s in fiscal 2022 Q2 was followed by %s a year on, %s in fiscal 2023 Q3 by %s, and "
             "fourth quarters ran %s to %s in fiscal 2021 to 2023. No card carries contract, so retail grows with the "
             "panel and contract is added at its run rate: net sales %s, %.2f%% (%+.2f points)."
             % (usd(F["contract_fy2024_m"]), usd(F["contract_9m_fy2024_m"]), usd(F["contract_base_m"]),
                usd(F["contract_q4_m"]), usd(cq["FY2022 Q2"]), usd(cq["FY2023 Q2"]), usd(cq["FY2023 Q3"]),
                usd(cq["FY2024 Q3"]), usd(min(cq["FY2021 Q4"], cq["FY2022 Q4"], cq["FY2023 Q4"])),
                usd(max(cq["FY2021 Q4"], cq["FY2022 Q4"], cq["FY2023 Q4"])), usd(F["forecast_m"]), F["growth_pct"],
                br["contract at its run rate"]))
    L.append("7. The same chain at each of the %d quarters from %s to %s, on what was known then (KS-02 left out of the "
             "comparisons its May 2023 book touches): root mean square error %.2f points, %d inside; the range is the "
             "estimate plus and minus %.2f points, USD %s to %s million, below the street's %s."
             % (F["origins"], q(F["first_origin"]), q(F["last_origin"]), F["golden_rmse_pp"], F["coverage_in"],
                F["band_pp"], mn(F["range_low_m"]), mn(F["range_high_m"]), usd(F["street_m"])))
    L.append("")
    L.append("No other conclusion survives. Each correction left out on its own leaves the range across the street "
             "(KS-01 kept USD %s to %s million; no revenue on delivery USD %s to %s million; contract grown with retail "
             "USD %s to %s million); two left out land long, or no position when the one handled is KS-01's book "
             "(USD %s to %s million), and all three left out land long; every reasonable rival (spend per card issuer by "
             "issuer or on cards of the same age, the fiscal 2023 or rolled-forward mix, a seven- or nine-week deposit "
             "window, contract at a four-quarter run rate, a re-issued book read at 3 or 10 per cent, KS-01's Midwest "
             "cards or its newest open years set aside instead of KS-01, KS-01 left out of every quarter, the record "
             "from fiscal 2023) keeps the top between USD %s and %s million; and the last week's completeness 3%% either way, "
             "the licensed share a fifth either way and the range from the record's error percentiles keep it between "
             "USD %s and %s million."
             % (mn(sl["no_reissue"]), mn(sh["no_reissue"]), mn(sl["no_deposits"]), mn(sh["no_deposits"]),
                mn(sl["no_contract"]), mn(sh["no_contract"]), mn(sl["only_reissue"]), mn(sh["only_reissue"]),
                mn(min(hi.values())), mn(max(hi.values())),
                mn(min(F["perturb_m"].values())), mn(max(F["perturb_m"].values()))))
    L.append("")
    return "\n".join(L)
