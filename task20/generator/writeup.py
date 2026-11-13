"""submission.md: the four answer blocks, every figure from figures.json."""

PROMPT = ("How large must Hallingvass Kraft's committed margin facility be for 2027 under its liquidity standard? Give "
          "the stress requirement in EUR million, the date it peaks and the facility it sets. At that date, give the "
          "exchange hedge book in TWh for each delivery year from 2027 to 2030 and the initial margin in EUR million; "
          "and from 1 January to that date, the output in GWh, and day-ahead purchases net of sales and customer "
          "payments received, both in EUR million. Give each delivery year's hedge ratio from 2027 to 2029 at 31 "
          "December 2026 in per cent, and the requirement worked out the same way for 2022 on the book at the end "
          "of 2021, beside what the 2022 records show, in EUR million with its date. A spreadsheet with the daily "
          "path and a short note.")


def text(F):
    f = F
    return """# task20: Hallingvass Kraft's committed margin facility for 2027

## Final Recommendation

Commit EUR {facility_m} million for 2027 (EUR {facility_2026_m} million is committed for 2026): in a year whose prices and inflows repeat 2022, the hedge program's cumulative net cash outflow peaks at EUR {peak_m} million on {peak_date} (any figure from EUR {band_peak_lo} million to EUR {band_peak_hi} million and from 23 to 31 August 2027 is within method), which the standard rounds up to EUR {facility_m} million. Reject the EUR {careful_facility_m} million the careful but hurried route reaches (the book grown along the policy's minimum on exchange positions, 2022's own margin rates and output carried over, the affiliate paid at spot) and the EUR {nosmelter_facility_m} million a hedge ratio counted on exchange positions alone gives.

## Supplementary Questions

1. Stress requirement: EUR {peak_m} million (band EUR {band_peak_lo} to {band_peak_hi} million, one decimal), peaking on {peak_date} (band 23 to 31 August 2027); facility EUR {facility_m} million, exact.
2. At {peak_date}: exchange hedge book still to be delivered, 2027 {book_peak_2027_twh} TWh, 2028 {book_peak_2028_twh} TWh, 2029 {book_peak_2029_twh} TWh, 2030 {book_peak_2030_twh} TWh (each within {book_tol} TWh); initial margin EUR {im_peak_m} million (band EUR {band_im_lo} to {band_im_hi} million).
3. From 1 January 2027 to the peak: output {out_gwh_txt} GWh (band {band_out_lo} to {band_out_hi} GWh); day-ahead purchases net of sales EUR {da_net_m} million (band EUR {band_da_lo} to {band_da_hi} million); payments received from supply customers EUR {rec_m} million (band EUR {band_rec_lo} to {band_rec_hi} million).
4. Hedge ratios at 31 December 2026 as the policy counts them (fixed-price sales over budgeted generation): 2027 {ratio_2027_pct} per cent, 2028 {ratio_2028_pct} per cent, 2029 {ratio_2029_pct} per cent (each within {ratio_tol} points).
5. 2022: the same method on the book at the end of 2021 through 2022's own prices and inflows gives EUR {c22_method_m} million on {c22_method_date} (band EUR {c22_actual_m} million plus or minus {c22_method_tol} million); the 2022 records (NEX statements, day-ahead settlements and customer payments) show EUR {c22_actual_m} million on {c22_actual_date} (within EUR {c22_rec_tol} million).
6. The spreadsheet carries the daily path of the stress year (variation margin, delivery settlement, initial margin and its change, day-ahead purchases less sales, customer payments, the net outflow and its cumulative sum), the book by month end, NEX's rates by day and output by month; the note gives the facility, the peak and its parts, and the 2022 check.

## Critical Components

1. The hedge ratio counts the fixed-price Fjordal Aluminium contract ({smelter_mw} MW at EUR {smelter_px}/MWh to 2029) as the policy's "sold forward at a fixed price" does: at 31 December 2026 the ratios are {ratio_2027_pct}, {ratio_2028_pct} and {ratio_2029_pct} per cent, against {ratio_ex_2027_pct}, {ratio_ex_2028_pct} and {ratio_ex_2029_pct} per cent on the exchange book alone, and only this basis reproduces every trade the desk made since 2018; counted on exchange positions the desk would sell enough more to push the requirement to EUR {nosmelter_peak_m} million.
2. The desk steps each delivery year to the policy maximum, {desk_speed_pts} points a week, once its year contract trades more than {desk_theta} times its October budget price, and sells nothing above the minimum otherwise (this rule reproduces the trade capture exactly); in the stress year that puts {book_peak_2028_twh} TWh of 2028, {book_peak_2029_twh} TWh of 2029 and {book_peak_2030_twh} TWh of 2030 on the exchange at the peak, against a requirement of EUR {min_peak_m} million if the book only follows the minimum.
3. NEX's rate for each class is the front contract's settlement price times the {rule_q_pct}th percentile of its absolute two-day log moves over the last {rule_look} business days, reviewed on Thursdays and changed when the indicated rate is more than {rule_band_pct} per cent from the rate in force; replayed on 2027 this gives initial margin of EUR {im_peak_m} million at the peak, where 2022's own rates as a share of price give EUR {pct2022_im_m} million (2022's look-back still held December 2021) and rates held at the year end give a requirement of EUR {const_peak_m} million.
4. Storage opens 2027 at {storage_open_gwh} GWh against a licence floor of {floor_gwh} GWh: the plants' release falls in a straight line with storage below normal and stops at the floor, so 2022's dry spring holds output to {out_gwh_txt} GWh by the peak and the supply contracts' shortfall is bought day-ahead (EUR {da_net_m} million net); 2022's own shortfall carried over, or output scaled with each week's inflow, gives EUR {ratio22_peak_m} million or EUR {inflow_peak_m} million.
5. Hallingvass Straum pays the average system price of the {aff_window} months ending {aff_lag} months before delivery (every invoice since 2019 to the cent), so customer payments to the peak are EUR {rec_m} million; paid at spot like the other customers, the requirement falls to EUR {affspot_peak_m} million.

## Step-by-Step

1. Rebuild the book: the position statement of 30 December 2026 gives {book_open_2027_twh} TWh of 2027 and {book_open_2028_twh} TWh of 2028 on the exchange; the trade capture agrees once cancelled trades are dropped, amended prices kept and the MWh-entered trades converted.
2. Read the hedge policy against the books: on exchange positions alone the next delivery year sat more than five points below the policy minimum at {below_n} of the {months_n} month ends since 2020, a gap the Fjordal contract's fixed-price volume closes; counted with it, the ratios at the year end are {ratio_2027_pct}, {ratio_2028_pct} and {ratio_2029_pct} per cent. A hurried pass applies the ladder to exchange positions and sells too much.
3. Recover the desk's rule from the trade capture against the October budget prices: it sells only to the minimum until a year contract trades {desk_theta} times budget, then {desk_speed_pts} points a week to the maximum. The policy's minimum ladder (EUR {min_peak_m} million) and selling to the maximum at once both miss it.
4. Recover NEX's rule from the margin notices and the front contracts' settlement prices (look-back, percentile, review day and tolerance each reproduce the notices) and run it through the stress year from the 2026 look-back. 2022's rates as a share of price (EUR {pct2022_peak_m} million) carry December 2021 in their window; rates held at the year end (EUR {const_peak_m} million) or scaled with the front price miss the stress altogether.
5. Build the stress year as the standard says: each forward month moved by 2022's percentage on the same date, the system price at 2022's ratio to the front month, each week's inflow at 2022's ratio to normal.
6. Run the plants from the year-end storage: run-of-river takes {ror_share_pct} per cent of inflow up to {ror_cap} GWh a week, the reservoirs release their normal plan scaled down in a straight line with storage below normal and never below the licence floor; output to the peak is {out_gwh_txt} GWh, and the shortfall against committed supply is bought day-ahead and settled the next business day.
7. Price the customers as the ledger shows: Fjordal at EUR {smelter_px}, Nesbyen and Bygdenett at the month's average system price, Hallingvass Straum on its twelve-month lagged average; each pays on its own habit ({lag_smelter}, {lag_pulp}, {lag_affiliate} and {lag_grid} days after the invoice).
8. Add the day's cash: variation margin and delivery settlement against NEX's settlement prices, the change in initial margin at the replayed rates, day-ahead net purchases, less customer payments. The cumulative sum peaks at EUR {peak_m} million on {peak_date}; the standard sets EUR {facility_m} million.
9. Check the method on 2022 itself: from the end-2021 book it gives EUR {c22_method_m} million on {c22_method_date}, against EUR {c22_actual_m} million on {c22_actual_date} in the records. The check cannot tell the hurried route from the right one, since 2022's own rates and output reproduce 2022 by construction; each of the five steps is fixed by its own record instead.
10. No other size survives: every defensible variant (the desk's threshold and pace, the rule's quantile convention and look-back, the release response, the payment habits and the affiliate's window) lands between EUR {band_peak_lo} million and EUR {band_peak_hi} million and sets EUR {facility_m} million, while each hurried step alone moves the requirement by {single_lo_pct} to {single_hi_pct} per cent and the careful but hurried pass lands at EUR {careful_peak_m} million (a EUR {careful_facility_m} million facility).
""".format(**f)
