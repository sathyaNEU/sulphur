"""task20 architecture 2: submission.md, the four answer blocks and the tags, every figure from figures.json."""
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
    rg, cw, pw = F["regional_pct"], F["company_weights_pct"], F["panel_weights_pct"]
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
             "This rejects the panel's read taken as net sales (issuers in both years, cards of the same age, the "
             "company's regional mix and the bank-card share: %s, a beat), the same with revenue on delivery but last "
             "year's wholesale contract left in (%s) or with wholesale separated but the December custom orders counted "
             "as sales (%s), and the desk's third-quarter model carried forward (%s)."
             % (F["release"], usd(F["forecast_m"]), F["growth_abs_pct"], sign, usd(F["base_net_sales_m"]),
                mn(F["range_low_m"]), mn(F["range_high_m"]), usd(F["street_m"]), usd(sm["careful"]),
                usd(sm["deposits_only"]), usd(sm["wholesale_only"]), usd(sm["desk_model"])))
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
    L.append("2. How the range would have held, on a Record sheet with one row per quarter from %s to %s (the estimate "
             "built as it would have been three weeks before each release, reported growth, the error, and whether it "
             "fell inside): root mean square error %.2f points (%.2f to %.2f), %d of %d quarters inside, the third "
             "quarter of fiscal 2025 missed by %.2f points (%.2f to %.2f), and the largest miss %.2f points in the "
             "fourth quarter of fiscal 2024. Net sales taken as what the panel shows, set beside it, has a root mean "
             "square error of %.2f points."
             % (q(F["first_origin"]), q(F["last_origin"]), F["golden_rmse_pp"], B["golden_rmse_pp"][0],
                B["golden_rmse_pp"][1], F["coverage_in"], F["origins"], F["q3_error_pp"], B["q3_error_pp"][0],
                B["q3_error_pp"][1], e["FY2024 Q4"], F["shortcut_rmse_pp"]["careful"]))
    steps = "; ".join("%s %+.2f (%.2f to %.2f)" % (k, v, bb[k][0], bb[k][1]) for k, v in bl)
    L.append("3. What each step from the card data to net sales is worth in points of year-on-year growth, on a Bridge "
             "sheet, in the order applied: %s; growth after the panel's own steps %.2f%%, at the company's mix %.2f%%, "
             "customer payments %.2f%%, retail net sales %.2f%%, net sales %.2f%%. A Regions sheet gives each billing "
             "region's growth on cards of the same age (Northeast %.2f%%, Southeast %.2f%%, Midwest %.2f%%, West %.2f%%) "
             "beside the panel's weights (%.2f, %.2f, %.2f, %.2f) and the company's fiscal 2024 weights (%.2f, %.2f, "
             "%.2f, %.2f); a Tender sheet the private-label share to %.1f%% in the third quarter and %.2f%% carried for "
             "the fourth (%.2f to %.2f), net sales per bank-card dollar %.2f%% (%.2f to %.2f); a Deposits sheet the "
             "deposits at each quarter end, the made-to-order share of the banner's spend in the last eight weeks "
             "(%.2f%% against %.2f%% a year earlier) and the quarter's closing deposits of %s (USD %s to %s million) "
             "against %s at the end of the third quarter; a Wholesale sheet each quarter's wholesale, last year's %s and "
             "this quarter's run rate of %s (USD %s to %s million)."
             % (steps, F["pooled_growth_pct"], F["visible_growth_pct"], F["payments_growth_pct"], F["retail_growth_pct"],
                F["growth_pct"], rg["Northeast"], rg["Southeast"], rg["Midwest"], rg["West"], pw["Northeast"],
                pw["Southeast"], pw["Midwest"], pw["West"], cw["Northeast"], cw["Southeast"], cw["Midwest"], cw["West"],
                F["pl_q3fy25_pct"], F["pl_target_pct"], B["pl_target_pct"][0], B["pl_target_pct"][1], F["drift_pct"],
                B["drift_pct"][0], B["drift_pct"][1], F["mto_share_q4_pct"], F["mto_share_base_pct"],
                usd(F["deposits_q4_m"]), mn(B["deposits_q4_m"][0]), mn(B["deposits_q4_m"][1]), usd(F["deposits_q3_m"]),
                usd(F["wholesale_base_m"]), usd(F["wholesale_q4_m"]), mn(B["wholesale_q4_m"][0]),
                mn(B["wholesale_q4_m"][1])))
    L.append("4. The call on the Call sheet: short, because the top of the range (%s) sits %s below the street's figure; "
             "every reasonable rival keeps the top between USD %s and %s million."
             % (usd(F["range_high_m"]), usd(F["range_gap_m"]), mn(min(hi.values())), mn(max(hi.values()))))
    L.append("")
    L.append("### %s" % GD.NOTE)
    L.append("")
    L.append("5. One page to the portfolio manager from the consumer analyst: the call and the estimate with its range "
             "against the street, the bridge from the delivered panel to net sales, a paragraph on why the panel reads a "
             "beat and the quarter is not one (the December custom orders still in deposits; last year's wholesale "
             "contract), the record, and what would change the call.")
    L.append("")
    L.append("## Critical Components")
    L.append("")
    L.append("1. On issuers in both years and cards of the same age the panel grew **%.2f%%** at its own mix, which is "
             "%.0f%% Southeast and %.0f%% West once KS-06 has left; at the company's fiscal 2024 regional mix the "
             "card-visible growth is **%.2f%%**." % (F["pooled_growth_pct"], pw["Southeast"], pw["West"],
                                                     F["visible_growth_pct"]))
    L.append("2. The private-label card, which the panel does not hold, is carried to **%.2f%%** of sales for the quarter "
             "(%.1f%% a year earlier, %.1f%% in the third quarter), so bank cards pay for %.1f%% of sales against %.1f%% "
             "and each dollar the panel sees stands for **%.2f%%** less: customer payments grew **%.2f%%**."
             % (F["pl_target_pct"], F["pl_q4fy24_pct"], F["pl_q3fy25_pct"], F["bank_target_pct"], F["bank_q4fy24_pct"],
                F["drift_less_pct"], F["payments_growth_pct"]))
    L.append("3. Net sales are recognised on delivery, and the December custom event's made-to-order orders (**%.2f%%** of "
             "the banner's spend in the quarter's last eight weeks against %.2f%%) are still undelivered at its end: "
             "customer deposits close the quarter near **%s** against %s at the end of the third quarter, worth "
             "**%.2f** points of growth." % (F["mto_share_q4_pct"], F["mto_share_base_pct"], usd(F["deposits_q4_m"]),
                                            usd(F["deposits_q3_m"]), br["revenue on delivery"]))
    L.append("4. Last year's quarter carried **%s** of wholesale, a contract the card panel cannot see; at its run rate of "
             "**%s**, separating it is worth **%.2f** points." % (usd(F["wholesale_base_m"]), usd(F["wholesale_q4_m"]),
                                                                 br["wholesale at its run rate"]))
    L.append("")
    L.append("## Step-by-Step")
    L.append("")
    L.append("1. The delivered panel, every issuer and merchant id, grew %.2f%% on the same quarter a year earlier, "
             "mostly KS-06, whose last delivered week began 26 October 2025, and the latest weeks still posting."
             % bl[0][1])
    L.append("2. Each issuer's first-delivered share of a week's final spend at lags 0 to 2 (medians over the 27 "
             "deliveries) completes the latest weeks (%+.2f points); the Hollister's shop-in-shops and the cafes, the "
             "licensees' sales, come out of the brand id by month (%+.2f points); issuers in both quarters (KS-01 to "
             "KS-05) with each card-open year set against the open year one later give like-for-like growth of %.2f%% "
             "(%+.2f points)." % (bl[1][1], bl[2][1], F["pooled_growth_pct"], bl[3][1]))
    L.append("3. The filing's fiscal 2024 net sales by region weight each region's growth: %.2f%% (%+.2f points); the "
             "private-label share carried at fiscal 2025's pace to %.2f%%, with the 10-K's 12%% of other tenders, turns "
             "bank-card spend into customer payments: %.2f%% (%+.2f points)."
             % (F["visible_growth_pct"], br["the company's regional mix"], F["pl_target_pct"], F["payments_growth_pct"],
                br["the bank-card share of net sales"]))
    L.append("4. The hurried analysis stops here and files payments as net sales: %s, range USD %s to %s million, a beat, "
             "with a record (root mean square error %.2f points) that looks sound because no past December held an event "
             "this large and no past base held a contract this large."
             % (usd(sm["careful"]), mn(sl["careful"]), mn(sh["careful"]), F["shortcut_rmse_pp"]["careful"]))
    L.append("5. Customers pay when they order and net sales are recognised on delivery, so retail net sales are payments "
             "less the change in customer deposits. Last year's closing deposits (%s), scaled by retail payments in the "
             "quarter's last eight weeks and by the made-to-order share of the banner's spend over them (%.2f%% against "
             "%.2f%%), give %s at the quarter's end against %s in October: retail net sales %s (%.2f%%, %+.2f points)."
             % (usd(F["deposits_base_m"]), F["mto_share_q4_pct"], F["mto_share_base_pct"], usd(F["deposits_q4_m"]),
                usd(F["deposits_q3_m"]), usd(F["retail_q4_m"]), F["retail_growth_pct"], br["revenue on delivery"]))
    L.append("6. Wholesale, invoiced and never on a card, was %s a year earlier and runs at %s (the median of the last eight "
             "quarters): net sales %s, %.2f%% (%+.2f points)."
             % (usd(F["wholesale_base_m"]), usd(F["wholesale_q4_m"]), usd(F["forecast_m"]), F["growth_pct"],
                br["wholesale at its run rate"]))
    L.append("7. The same chain at each of the %d quarters from %s to %s, on what was known then: root mean square error "
             "%.2f points, %d inside; the range is the estimate plus and minus %.2f points, USD %s to %s million, below "
             "the street's %s."
             % (F["origins"], q(F["first_origin"]), q(F["last_origin"]), F["golden_rmse_pp"], F["coverage_in"],
                F["band_pp"], mn(F["range_low_m"]), mn(F["range_high_m"]), usd(F["street_m"])))
    L.append("")
    L.append("No other conclusion survives. Either deep step alone leaves the range across the street (revenue on delivery "
             "without wholesale USD %s to %s million; wholesale without revenue on delivery USD %s to %s million); "
             "every reasonable rival (the private-label rules, the fiscal 2023 or rolled-forward mix, a seven- or "
             "nine-week deposit window, wholesale at a four-quarter run rate, the chain calibrated by regression) keeps "
             "the top between USD %s and %s million; and other tenders at 10 or 14%%, the last week's completeness 3%% "
             "either way and the licensed share a fifth either way keep it between USD %s and %s million."
             % (mn(sl["deposits_only"]), mn(sh["deposits_only"]), mn(sl["wholesale_only"]), mn(sh["wholesale_only"]),
                mn(min(hi.values())), mn(max(hi.values())), mn(min(F["perturb_m"].values())),
                mn(max(F["perturb_m"].values()))))
    L.append("")
    return "\n".join(L)
