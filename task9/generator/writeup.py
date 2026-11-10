"""task9: submission.md, the four answer blocks, drafted from figures.json (no figure is typed)."""
import pandas as pd

import golden as GD
import pack as PK


def n(v):
    return "{:,}".format(v)


def d(s, year=True):
    return pd.Timestamp(s).strftime("%B %-d, %Y" if year else "%B %-d")


def band(b):
    return "between %s and %s" % (n(b[0]), n(b[1]))


def blocks(F):
    pol, at, q, h, own, rb, rp = F["policy"], F["at_size"], F["quoted"], F["hurried"], F["own_history"], F["rebuild"], F["replay"]
    plan, pb, pl, cal, cc = F["R10_plan"], F["R10_bands"], F["plan"], F["new_calendar"], F["cross_check"]
    size, size6 = F["R4_size_usd"], F["R5_alt_size_usd"]
    r6, r7, b6, b7, r9, b9 = F["R6_avg_range_12m"], F["R7_avg_range_3m"], F["R6_bands"], F["R7_bands"], F["R9_range"], F["R9_bands"]
    a12, a3 = F["avg_12m"], F["avg_3m"]
    iid12, iid3 = a12["hurried"]["single settlements resampled"], a3["hurried"]["single settlements resampled"]
    eh, ph = F["expect_hurried"], pl["hurried"]
    f = PK.F
    out = []
    out.append("## Tags\n")
    out.append("**Domain:** Quantitative Finance and Trading, Quantitative Finance (derivative pricing and collateral exposure: an index variance "
               "swap program).\n**Analytical objective:** Forecasting & Predictive Modeling.\n")

    out.append("## Final Recommendation\n")
    out.append(
        "**Set the new 3-month ladder at USD %s a point per monthly sale** (sound methods land %s), not the USD %s the dealers quoted for: beside "
        "the 12-month ladder at its USD %s, the sleeve's collateral on the policy's record peaks at USD %s on %s against the USD %s collateral "
        "limit, which is the limit that binds; at that size the %d cash plan carries USD %s from the sleeve (%s), with an 80%% range from a net "
        "payment of USD %s to receipts of USD %s (the low end %s, the high end %s). It rejects the USD %s that comes from standing the 30-day "
        "index in for the 3-month strikes missing before %s, a stand-in that explains %.2f of the 3-month index's variation where both are "
        "published and still runs %.1f points high on the stressed days that set the limit, a size at which the sleeve would have posted USD %s "
        "on %s; and it rejects the plan of USD %s that goes with it, which also counts the open swaps at their USD %s value where the record "
        "says to expect USD %s.\n"
        % (n(size), band(F["R4_band"]), n(pol["quoted_size_usd"]), n(pol["standing_size_usd"]), n(at["peak_usd"]), d(at["peak_day"]),
           n(pol["collateral_limit_usd"]), F["plan_year"], n(plan["total_usd"]), band(pb["total_usd"]), n(pl["low_paid_usd"]), n(plan["high_usd"]),
           band(pb["low_usd"]), band(pb["high_usd"]), n(h["size_usd"]), d(rb["first_published"]), rb["proxy_r2"], rb["proxy_bias_hot"],
           n(h["peak_on_record_usd"]), d(h["peak_day"]), n(h["plan_usd"]), n(h["open_usd"]), n(F["R8_expected_usd"])))

    out.append("## Supplementary Questions\n")
    out.append("### %s\n" % GD.BOOK)
    q_ = [
        "A summary sheet that leads with the size table, one row per ladder (size, the limit that binds, the binding day, the sleeve's collateral "
        "that day against the limit, the worst calendar year of settlements against its limit). A 6-month ladder instead: USD %s a point (%s), "
        "bound by the collateral limit on %s." % (n(size6), band(F["R5_band"]), d(F["R5_binds"]["day"])),
        "On the policy's record (monthly sale dates from January 2007, swaps expired by %s), per USD %s a point, the 3-month ladder's average "
        "settlement per sale is USD %s received (%s) and its worst calendar year is %d, a net USD %s paid (%s). A sheet gives each ladder's net "
        "settlements by calendar year." % (d(F["as_of"]), n(pol["per_usd"]), n(F["R1_avg_3m_usd"]), band(F["R1_band"]), F["R2_worst_year"],
                                           n(F["R2_worst_year_loss_usd"]), band(F["R2_band"])),
        "The 80%% range of each average, per USD %s a point: the 3-month ladder's average lies between USD %s and USD %s (the low end %s, the "
        "high end %s), and the 12-month ladder's average of USD %s between USD %s and USD %s (the low end %s, the high end %s). A sheet shows "
        "the ranges under each way of keeping neighboring sales together, beside the narrower range that treats the settlements as unrelated."
        % (n(pol["per_usd"]), n(r7["low_usd"]), n(r7["high_usd"]), band(b7["low_usd"]), band(b7["high_usd"]), n(a12["avg_per_sale_usd"]),
           n(r6["low_usd"]), n(r6["high_usd"]), band(b6["low_usd"]), band(b6["high_usd"])),
        "The 12-month ladder at its USD %s a point: peak collateral on the record of USD %s (%s). The 2008 and 2020 episodes come within 3%% of "
        "each other, and which of the two is the higher depends on how the term structure is read between published maturities; no day is graded."
        % (n(pol["standing_size_usd"]), n(F["R3_old_peak_usd"]), band(F["R3_band"])),
        "The open swaps that expire in %d (ten sale months) should be expected to settle at USD %s received in total (%s), with an 80%% range of "
        "USD %s to USD %s (the low end %s, the high end %s)."
        % (F["plan_year"], n(F["R8_expected_usd"]), band(F["R8_band"]), n(r9["low_usd"]), n(r9["high_usd"]), band(b9["low_usd"]), band(b9["high_usd"])),
        "The sleeve's %d cash plan at USD %s a point, by ladder: the 12-month ladder USD %s (%s), being the open swaps' USD %s and USD %s for its "
        "November and December 2026 sales, which are still to come and expire in the year; the 3-month ladder USD %s (%s), from the nine sales "
        "(%s to %s) whose swaps expire inside the year; the sleeve USD %s (%s), with an 80%% range of minus USD %s to USD %s (the low end %s, "
        "the high end %s). A sheet lists all %d settlements. The workbook also carries the working: the room on the binding day, the check of "
        "the rebuilt strikes on the days all the indices are published, the open swaps one by one, and a sheet of what each shorter route gives."
        % (F["plan_year"], n(size), n(plan["twelve_month_usd"]), band(pb["twelve_month_usd"]), n(F["R8_expected_usd"]), n(pl["unsold_12m_usd"]),
           n(plan["three_month_usd"]), band(pb["three_month_usd"]), d(cal["first_sale"], False), d(cal["last_sale_settling_in_year"], False),
           n(plan["total_usd"]), band(pb["total_usd"]), n(pl["low_paid_usd"]), n(plan["high_usd"]), band(pb["low_usd"]), band(pb["high_usd"]),
           pl["settlements"]),
    ]
    for i, t in enumerate(q_, 1):
        out.append("%d. %s" % (i, t))
    out.append("\n### %s\n" % GD.DAILY)
    out.append("7. One row per day of the record, %s to %s (%s rows), in date order, with the date, the 12-month ladder's value, the 3-month "
               "ladder's value at USD %s a point, the sleeve's value and the collateral (the amount by which the sleeve's value is negative, "
               "otherwise zero), in dollars to the nearest thousand. The highest collateral is USD %s, on %s, and collateral is above zero on %s "
               "of the days." % (d(F["daily"]["first_day"]), d(F["daily"]["last_day"]), n(F["daily"]["rows"]), n(size),
                                 n(F["daily"]["peak_usd"]), d(F["daily"]["peak_day"]), n(F["daily"]["days_with_collateral"])))
    out.append("\n### %s\n" % GD.MEMO)
    out.append("8. A short memo that opens with the size, the limit and day that bind it and the plan with its range, says why the USD %s quoted "
               "for and the USD %s from a 30-day stand-in both fail, gives the 6-month alternative, the plan by ladder in a small table and how "
               "firmly the record pins each average, and carries one chart of the sleeve's daily collateral against the limit.\n"
               % (n(pol["quoted_size_usd"]), n(h["size_usd"])))

    out.append("## Critical Components\n")
    comps = [
        "The largest 3-month size inside both limits beside the 12-month ladder is **USD %s** a point (%s), bound by the **collateral limit** on "
        "**%s**." % (n(size), band(F["R4_band"]), d(F["R4_binds"]["day"])),
        "The open swaps that expire in %d should be expected to settle at **USD %s** (%s), not at their USD %s value at the review close."
        % (F["plan_year"], n(F["R8_expected_usd"]), band(F["R8_band"]), n(rp["mark_usd"])),
        "The %d plan at that size is **USD %s** (%s): USD %s from the 12-month ladder, its two sales still to come included (%s), and USD %s "
        "from the 3-month ladder's nine settlements (%s), with an 80%% range of **minus USD %s to USD %s** taken over all %d settlements "
        "together (the low end %s, the high end %s)."
        % (F["plan_year"], n(plan["total_usd"]), band(pb["total_usd"]), n(plan["twelve_month_usd"]), band(pb["twelve_month_usd"]),
           n(plan["three_month_usd"]), band(pb["three_month_usd"]), n(pl["low_paid_usd"]), n(plan["high_usd"]), pl["settlements"],
           band(pb["low_usd"]), band(pb["high_usd"])),
        "On the record from January 2007 the 3-month ladder's worst calendar year is **%d**, a net **USD %s** paid per USD %s a point (%s); the "
        "%d strikes before the index's first close in the folder are rebuilt from the published maturities on both sides of three months."
        % (F["R2_worst_year"], n(F["R2_worst_year_loss_usd"]), n(pol["per_usd"]), band(F["R2_band"]), F["ladder_counts"]["rebuilt"]),
    ]
    for i, t in enumerate(comps, 1):
        out.append("%d. %s" % (i, t))

    out.append("\n## Step-by-Step\n")
    reg = F["ladder_hurried"]["regression on the 30-day index alone"]
    steps = [
        "From `%s`, with the superseded %s ticket (booked at USD %s) and the original of the confirmation novated in %s left out, the "
        "sleeve is %d confirmations, %d settled and %d open in twelve sale months at USD %s a point a month; `%s` gives the formula for realized "
        "volatility, the cap and the settlement amount, and `SPX_History.csv` the closes."
        % (f["blotter"], F["blotter"]["amended_month"], n(F["blotter"]["amended_wrong_vega_usd"]), F["blotter"]["novation_month"],
           F["confirmations"]["total"], F["confirmations"]["settled"],
           F["open_confirmations"], n(pol["standing_size_usd"]), f["confirmation"]),
        "`%s` and the three dealer statements show how an open swap is valued: variance realized to date and variance implied to expiration, "
        "weighted by days, with an implied figure that differs swap by swap with the remaining term. On the %s closes of the Cboe volatility "
        "indices, implied volatility read in total variance between published maturities, the open swaps are worth USD %s; valuing every swap "
        "at the 1-year index it was struck on gives %s, which does not match the dealers."
        % (f["valuations"], d(F["as_of"], False), n(F["book_value_usd"]), n(F["book_value_hurried"]["each swap at the 1-year index"])),
        "Schedule D.5(b) in `%s` keeps every monthly sale date from January 2007 in the record whether or not a ladder's index was yet "
        "published, and `VIX3M_History.csv` starts on %s, so %d strikes of the 3-month ladder have to be rebuilt. The hurried analysis regresses "
        "the 3-month index on the 30-day index, sees an R-squared of %.2f over the %s days both are published, and uses it: USD %s a sale and "
        "%s for 2008. Its check is the wrong one. On the %d days the 30-day index closed above %d the 3-month index runs %.1f%% below it, "
        "against %.1f%% above on average, and the stand-in is %.1f points high there. Rebuilt by least squares on the 30-day index and the next "
        "longer published index (the 6-month from %s, the 1-year before that), the fit is off by %.2f points on average and %.2f on those days, "
        "and the ladder averages USD %s a sale with a worst year of %d at %s. Leaving the early sale dates out, which D.5(b) does not allow, "
        "gives %s a sale and a worst year of %d at %s. The index's earlier closes are public but not in the folder; a solver who brings them in "
        "gets %s and %s, inside the same bands."
        % (f["policy"], d(rb["first_published"]), F["ladder_counts"]["rebuilt"], rb["proxy_r2"], n(rb["overlap_days"]), n(reg["avg_per_sale_usd"]),
           n(reg["worst_year_loss_usd"]), rb["hot_days"], pol["hot_level"], rb["ratio_hot_pct"], rb["ratio_all_pct"], rb["proxy_bias_hot"],
           d(rb["six_month_first"]), rb["rmse"], rb["rmse_hot"], n(F["R1_avg_3m_usd"]), F["R2_worst_year"], n(F["R2_worst_year_loss_usd"]),
           n(own["avg_3m_usd"]), own["worst_year"], n(own["worst_year_loss_usd"]), n(cc["actual"]["avg_per_sale_usd"]),
           n(cc["actual"]["worst_year_loss_usd"])),
        "The 12-month ladder is sold on the record at USD %s a point at the 1-year index, and its open swaps are valued together each day on the "
        "dealers' basis with exposure capped as `%s` caps it: the peak is USD %s (%s, with %s at %s). Valuing each swap at the 1-year index gives "
        "%s, leaving the cap out of the valuation %s, and the worst calendar year of settlements is only %s; none is the collateral the policy "
        "measures."
        % (n(pol["standing_size_usd"]), f["csa"], n(F["R3_old_peak_usd"]), d(F["R3_old_peak_day"]), d(F["old_peak_episodes"]["2008"]["day"]),
           n(F["old_peak_episodes"]["2008"]["peak_usd"]), n(F["old_peak_hurried"]["each swap at the 1-year index"]),
           n(F["old_peak_hurried"]["no cap in the mark"]), n(F["old_peak_hurried"]["its worst calendar year of settlements"])),
        "Both ladders are run together on every day of the record against both limits (USD %s of collateral and USD %s of settlements, %.1f%% and "
        "%.1f%% of the USD %s million in `%s`). The binding day is %s: the 12-month ladder stands at %s against the sleeve, leaving %s of room, "
        "and the 3-month ladder stands at %s per USD %s a point, so the largest size in multiples of USD 100 is %s. The settlement limit alone "
        "would allow %s. The stand-in's strikes give %s, the new ladder sized on its own %s, each swap valued at its own index %s, and the same "
        "run for a 6-month ladder %s, bound on the same day; the 6-month index is published from %s, so every 6-month swap open that day has a "
        "published strike."
        % (n(pol["collateral_limit_usd"]), n(pol["settlement_limit_usd"]), pol["collateral_limit_pct"], pol["settlement_limit_pct"],
           "{:,.1f}".format(pol["reference_assets_usd_m"]), f["assets"], d(F["R4_binds"]["day"]), n(at["old_at_peak_usd"]), n(at["room_usd"]),
           n(at["new_per_100k_at_peak_usd"]), n(pol["per_usd"]), n(size), n(F["R4_hurried"]["the settlement limit alone"]), n(h["size_usd"]),
           n(F["R4_hurried"]["the new ladder on its own"]), n(F["R4_hurried"]["marks at each swap's own index"]), n(size6), d(rb["six_month_first"])),
        "Schedule D.7(d) asks for the range of each average. A sale's settlement is tied to the next one's (correlation %.2f for the 12-month "
        "ladder, %.2f for the 3-month), because swaps sold a month apart share most of their days. Resampling the %d and %d settlements one at "
        "a time, as the hurried analysis does, gives USD %s to %s for the 12-month ladder and %s to %s for the 3-month. Resampling the record in "
        "blocks of consecutive sales twice the swap's life gives %s to %s and %s to %s; other block lengths, a standard error that allows for "
        "at least the months neighboring swaps share, calendar-year averages and a count of only the swaps that do not overlap all land inside "
        "the bands. A standard error that allows for %d lags, where neighboring 12-month swaps share %d months, is still too narrow (%s to %s)."
        % (a12["next_sale_correlation"], a3["next_sale_correlation"], a12["n"], a3["n"], n(iid12["low_usd"]), n(iid12["high_usd"]),
           n(iid3["low_usd"]), n(iid3["high_usd"]), n(r6["low_usd"]), n(r6["high_usd"]), n(r7["low_usd"]), n(r7["high_usd"]),
           a12["few_lags"], a12["shared_months"], n(a12["hurried"]["a standard error with too few lags"]["low_usd"]),
           n(a12["hurried"]["a standard error with too few lags"]["high_usd"])),
        "Schedule D.7(a) carries the open swaps at the settlement amounts they are expected to pay, and D.7(c) takes experience from the whole "
        "record. The ten sale months that expire in %d are valued at USD %s, and the hurried analysis budgets that. Taking each of the %s start "
        "dates from %s to %s, realized variance over each swap's remaining days as a share of the variance implied that day for the same term, "
        "applied to the %s term structure, the same swaps go on to pay more than their value from %d%% of start dates and USD %s on average, "
        "and between USD %s and USD %s four times in five when all ten are taken from the same start date. Realized variance has averaged %.2f "
        "of implied over one month and %.2f over twelve on the record. A forecast made in volatility and then squared gives %s, too high, "
        "because the settlement amount is linear in variance; the median start date (%s) is not the expectation; and the sleeve's own years "
        "alone (%s) are what D.7(c) rules out."
        % (F["plan_year"], n(rp["mark_usd"]), n(rp["start_dates"]), d(rp["first_start"]), d(rp["last_start"]), d(F["as_of"], False),
           rp["share_above_mark_pct"], n(F["R8_expected_usd"]), n(r9["low_usd"]), n(r9["high_usd"]), rp["one_month_ratio"], rp["twelve_month_ratio"],
           n(eh["a volatility forecast, squared"]), n(rp["median_usd"]), n(eh["ratio on the sleeve's own years"])),
        "Schedule D.7 carries every swap that expires in the plan year. For the 12-month ladder that is the ten open sale months and the sales "
        "of %s and %s, not yet made at the review date, which expire on %s and %s: USD %s at the ladder's average of USD %s a sale (D.7(b)), so "
        "USD %s for the ladder. With `%s` the new ladder's sales run from %s and only the nine to %s expire inside %d (%s to %s; the June expiry "
        "moves to the 17th because the exchange is closed on the 18th): nine sales at USD %s a point and the record's average bring USD %s. "
        "The plan is USD %s. Leaving out the two sales still to come gives %s for the 12-month ladder, and twelve settlements for the new "
        "ladder would give %s."
        % (d(pl["unsold_sales"][0]), d(pl["unsold_sales"][1]), d(pl["unsold_expiries"][0]), d(pl["unsold_expiries"][1]), n(pl["unsold_12m_usd"]),
           n(pl["avg_12m_per_sale_usd"]), n(plan["twelve_month_usd"]), f["holidays"], d(cal["first_sale"]), d(cal["last_sale_settling_in_year"], False),
           F["plan_year"], d(cal["first_expiry"], False), d(cal["last_expiry_in_year"], False), n(size), n(plan["three_month_usd"]),
           n(plan["total_usd"]), n(F["R8_expected_usd"]), n(cal["twelve_usd"])),
        "The plan's range (D.7(e)) takes all %d settlements from the same start date: the open swaps over their remaining days, and each swap "
        "not yet sold struck and run the same number of days after it, for %s start dates to %s. The 10th and 90th percentiles are minus USD %s "
        "and USD %s, and the plan is below zero from %d%% of start dates. Drawing the swaps not yet sold one at a time from their ladder's "
        "record gives minus %s to %s, and drawing all %d settlements independently %s to %s; both miss that one bad stretch hits the open swaps "
        "and the new sales together."
        % (pl["settlements"], n(pl["start_dates"]), d(pl["last_start"]), n(pl["low_paid_usd"]), n(plan["high_usd"]), pl["share_below_zero_pct"],
           n(pl["unrelated_low_paid_usd"]), n(ph["unsold swaps drawn one by one from their ladder's record"]["high_usd"]),
           pl["settlements"], n(ph["settlements drawn independently"]["low_usd"]), n(ph["settlements drawn independently"]["high_usd"])),
    ]
    for i, t in enumerate(steps, 1):
        out.append("%d. %s" % (i, t))
    out.append(
        "\nNo other size survives the files. The USD %s quoted for would have put USD %s of collateral on the sleeve on %s, %s over the limit. "
        "Schedule D.5(b) keeps the sale dates of 2007 to 2009 in the record, so the 3-month ladder cannot be run only where its index file has a "
        "close, and a stand-in built on the 30-day index alone overstates the missing strikes on exactly the stressed days that set the limit, "
        "which the days all the indices are published show. Every way of rebuilding those strikes from both neighboring maturities, and every "
        "way of reading the term structure between published maturities, binds on the collateral limit on %s and lands %s; sizing the new ladder "
        "on its own, valuing swaps at the index they were struck on or leaving the cap out of the valuation each contradicts Schedule D.5 or the "
        "credit support annexes. For the plan, the value of an open swap is a price and not what Schedule D.7(a) asks for, and every estimate of "
        "the expectation drawn from the whole record lands %s; the ranges have to respect that neighboring sales and the open swaps move "
        "together, which the settlements themselves show.\n"
        % (n(pol["quoted_size_usd"]), n(q["peak_usd"]), d(q["peak_day"]), n(q["over_usd"]), d(F["R4_binds"]["day"]), band(F["R4_band"]), band(F["R8_band"])))
    return "\n".join(out)


def write(path, F):
    text = blocks(F)
    assert "—" not in text and "–" not in text, "a dash crept into the blocks"
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    return text
