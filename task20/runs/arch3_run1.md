# task20 architecture 3: platform run 1 (pasted by the author, 2026-11-13; final report as pasted)

Reviewed 39 resources
Recommendation.
Commit a EUR 250 million margin facility for 2027. The stress requirement is EUR 208.423 million on 27 August 2027, rounded up to the next EUR 50 million under the liquidity standard. This requires EUR 100 million more than the current EUR 150 million commitment.

Final answers.
All requested figures appear in Hallingvass_2027_Liquidity.xlsx, principally on Summary, and on page 1 of Hallingvass_2027_Note.pdf.

Stress requirement and facility: EUR 208.423 million, peaking on 27 August 2027, setting a EUR 250 million committed facility. See Summary!B5:B10.
Exchange hedge book remaining after that date: 0.638064 TWh for 2027; 2.248704 TWh for 2028; 1.112520 TWh for 2029; 0.998640 TWh for 2030. These volumes exclude deliveries on the peak date and exclude bilateral customer contracts. See Summary!A22:C25.
Initial margin at the peak: EUR 45.188 million. See Summary!B11.
From 1 January through the peak date: output 1,744.319 GWh; day-ahead purchases net of sales, measured when cash settles, EUR 74.260 million; customer payments received EUR 160.364 million. See Summary!B16:B18.
Hedge ratios at 31 December 2026: 68.55% for 2027; 39.61% for 2028; 22.23% for 2029. These include fixed-price bilateral sales and use the latest approved generation budgets. See Hedge Ratios and Summary!D22:D24.
2022 comparison using the end-2021 book: the same-method replay requires EUR 548.417 million on 26 August 2022; actual cash records show EUR 548.457 million on 26 August 2022. The replay is EUR 0.040 million lower. Both round to a EUR 550 million facility. See Summary!A29:D31.
Daily paths: 2027 Daily, 2022 Replay and 2022 Actual each contain the full calendar-year cash path. Supporting sheets expose trades, margin notices, water plans, customer cash, settlement ledgers and stress forwards.
Step-by-step process.
Read the governing documents. hk_liquidity_standard_2026.pdf defines cumulative cash-date netting, the repeat-2022 stress and EUR 50 million rounding. hk_hedging_policy_2025.docx, including its table, defines hedge ratios and limits. nex_clearing_margin_summary.pdf defines cascading and settlement mechanics. hallingvass_regulation_licence_extract.pdf supplies the 700 GWh storage minimum and 2,600 GWh capacity.

Reconstructed the hedge book. hk_trade_capture_2018_2026.csv contained 441 rows. Replacing 13 superseded versions and removing 5 final cancellation records left 423 economic fills. I normalized contract aliases and converted 68 MWh-denominated fills using delivery-year hours. The reconstruction matches all 596 records in nex_positions_month_end_2017_2026.csv, with 0 MW maximum error. hk_budget_vintages_2016_2026.xlsx supplied 44 budget observations, selected by approval date and delivery year.

Cleaned market and clearing histories. From hk_risk_curve_daily_2018_2026.csv, I retained 108,336 canonical HK_SYS rows and excluded 792 competing HK_SYS_V2 rows. In nex_daily_settlement_2018_2026.csv, I removed 80 exact duplicates and reconstructed 15 quotes for the missing 21 November 2019 block; one unnecessary far-year quote remained unavailable. From nex_clearing_statements_2018_2026.csv, I removed the superseded statement for 8 March 2022, retaining 2,257 statements. nex_margin_parameters_2018_2026.csv supplied 246 notices, preserving publication and effective dates. No market-price extremes were discarded.

Reconstructed physical operation. hk_hydrology_weekly_2017_2026.csv contained 522 weeks: 512 final, 7 provisional and 3 missing-inflow observations. Missing inflows were excluded from estimation rather than filled using future information; there were no duplicate weeks. In the 600 plant records from hk_plant_output_monthly_2017_2026.csv, I normalized 72 plant-name aliases. Daily generation reconstructed from physical deliveries reconciles to monthly plant output within 0.002400 GWh. I tested the 522 heating-degree-day observations, but additional weather/price terms worsened held-out dispatch accuracy. The 2,257 EUR/NOK observations were reviewed but not applied because all in-scope cash is already denominated in EUR.

Reconstructed supply and customer cash. hk_supply_contracts_register.xlsx defines four supply obligations and their profiles. hk_sales_ledger_2018_2026.csv contains 428 invoices, 6 supplemental payments and 4 credit notes. I retained all 431 actual cash records, joined the group customer's account change by legal entity, and treated 3 missing invoice payment dates as censoring rather than default. Supplemental payments were not deduplicated away, and noncash credits were not treated as refunds. The recurring grid profile was normalized from 300,001 MWh to its contractual 300,000 MWh; the retail profile totals 1,800,000 MWh. All 3,287 day-ahead settlement dates match the next-business-day rule.

Built the stress dynamically rather than freezing the book. Each 2027 business day applies the mapped 2022 daily percentage forward-price move. The 253 target business days map to 202 distinct source days, repeating 51 source moves and skipping 51. Trading follows the empirically reconstructed Tuesday rule, including budget resets. Margin rates respond to observed price risk and notice timing, with correct year, quarter and month cascading. Physical dispatch responds to inflows and storage rather than being forced to equal budgeted generation.

Projected dated customer receipts and combined cash flows. The group transfer price uses monthly system prices from M-13 through M-2, not current spot. Median invoice-to-payment ages are 39 days for Fjordal, 30 for Nesbyen, 51 for group supply and 21 for grid losses. The peak cash bridge is: EUR 241.363 million variation margin + EUR 10.857 million delivery settlement + EUR 42.307 million IM increases + EUR 74.260 million net day-ahead purchases − EUR 160.364 million customer receipts = EUR 208.423 million. Opening collateral is not charged again; prior-year cash runoff is included.

Validated the reconstruction and deliverables. The model matches 1,383 historical trading decisions, 220 fully warmed margin rates, 1,153 notice decisions and all 36 testable budget-price resets. IM balances reconcile to all 2,257 statements to the cent. Dispatch was fitted on 205 pre-2022 weeks and tested on 52 held-out weeks, with one-step RMSE of 0.041047 GWh/week and recursive RMSE of 0.046759 GWh/week. I also checked cash arithmetic, water conservation, payment conservation, year-end runoff, formula caches, workbook integrity and PDF page boundaries.

The near-exact 2022 peak match does not imply perfect receipt-date forecasting. Full-year modeled customer receipts are EUR 291.511 million, versus EUR 302.167 million recorded; year-end cumulative cash outflow is EUR 170.835 million, versus EUR 160.211 million. These residuals are disclosed in Validation.

Assumptions and judgment calls.
Calendar-aligned storage is the main case. Weekly water balances identify storage as week-ending despite the week_start label. Prorating the final weekly movement to 31 December gives opening storage of 888.929 GWh for 2027 and 1,273.386 GWh for 2022. Using the latest weekly figures unchanged gives EUR 209.718 million for 2027, still requiring EUR 250 million, but EUR 550.596 million for 2022, rounding to EUR 600 million. The selected treatment avoids double-counting the straddling week and improves the historical replay.
The simulation follows observed trading practice, not an invented compliance correction. The opening 2027 and 2028 ratios are below their policy floors. The written policy requires same-day escalation and correction within ten business days, but the observed trading rule does not enforce this. The 2027 shortfall is 57.440 GWh, requiring 7 whole MW to restore its minimum. Both artifacts disclose that corrective trades require re-sizing.
Future payment dates are estimates. They use pre-cutoff entity payment histories, not future realized receipts. The 2022 payment-date mean absolute error is 2.836735 days. Tested payment, storage and dispatch alternatives produce requirements from EUR 203.400 million to EUR 217.725 million, all requiring EUR 250 million.
Future generation budgets remain at the latest supplied long-range values. Physical production is modeled separately. The 2027 annual output is 2,950.342 GWh, versus a 3,974 GWh hedge-budget denominator.
Some physical uncertainty remains. Latest storage is provisional, publication timestamps are unavailable, and minimum flows in cubic metres cannot independently be converted to GWh without hydraulic parameters. The result is a deterministic prescribed scenario, not a statistical confidence bound.
Alternatives rejected.
Frozen exchange book: gives EUR 129.606 million, implying a EUR 150 million facility, but contradicts the observed path-dependent trading behavior.
Fixed opening margin rates: gives EUR 172.096 million, implying EUR 200 million, but contradicts the validated margin-rate and notice process.
Group supply priced at current spot: gives EUR 157.441 million, implying EUR 200 million. Its historical pricing RMSE is EUR 48.979379/MWh, versus EUR 0.000187/MWh for the identified lagged tariff.
Cumulative price-level copying: gives EUR 328.747 million, implying EUR 350 million. This is the material adverse alternative, but it is not the standard's instruction to apply the corresponding daily percentage move. It is explicitly retained in Sensitivities and the note.
Additional weather/price dispatch terms: increase held-out RMSE from 0.041329 to 0.044430 GWh/week, so they were not included.
Files produced.
/home/agent/workspace/Hallingvass_2027_Liquidity.xlsx: decision summary, daily paths, supporting calculations, source treatments, validation and sensitivities.
/home/agent/workspace/Hallingvass_2027_Note.pdf: two-page treasury note with the recommendation, requested figures, cash bridge and material caveats.
Temporary analysis scripts were removed. The input archive and pre-existing workspace files were preserved.

Packages installed.
Installed in an isolated environment: pandas, NumPy, SciPy, statsmodels, openpyxl, python-docx, PyMuPDF, matplotlib, ReportLab and XlsxWriter. ReportLab and XlsxWriter were additional to the stated preinstalled package list.
