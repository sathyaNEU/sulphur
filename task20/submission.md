# task20 submission: why the SMCF desk breached its VaR, and the add-on for the second half

## Tags

**Domain:** Quantitative Finance and Trading, Quantitative Finance (risk modeling: one-day 99% VaR backtesting and exception attribution for an equity facilitation desk).
**Analytical objective:** Root-Cause Analysis.

## Final Recommendation

**Report 19 exceptions for the 250 days to 30 June 2025 and count 14 of them against the model: 4 are the inputs', every one a night ERE's extract was cut before the closing-auction allocations were booked, 1 is other income, and a sound model shows 2 (the green zone, 0 to 2 across the settings MRS-4 allows); hold an add-on of USD 0.32 million in July that falls to nil by December.** This rejects the official 15 booked exceptions and red zone, the reading that blames the 27 runs on an older extract (they caused none, and it leaves 16 against the model), and an add-on held at July's figure or rising with the plan's ramp to USD 0.40 million.

## Supplementary Questions

### exception_classification_2025Q2.xlsx

1. Every exception dated under one MRS-4 heading, the headings adding back to 19, on an Exceptions sheet with one row per date (booked and hypothetical P&L, the VaR reported and its run, which P&L shows it, the heading, ERE's VaR on the book held, the own-history and volatility-scaled VaRs, the allocations missing from the run, and the basis): (a) other income 1: 3 April 2025; (b) inputs 4: 2 August 2024, 5 August 2024, 23 October 2024, 4 March 2025; (c) risks not in the model 11: 6 September 2024, 25 September 2024, 4 November 2024, 22 January 2025, 24 January 2025, 27 January 2025, 5 February 2025, 10 February 2025, 2 April 2025, 4 April 2025, 2 June 2025; (d) volatility 2: 28 March 2025, 6 May 2025; (e) model accuracy 1: 14 February 2025. Across decay 0.94 to 0.97, scaled at the portfolio or name by name, 14 February 2025 and 28 March 2025 move between (d) and (e) (volatility 2 to 3, model accuracy 0 to 1); every other row holds.
2. What went wrong with ERE's inputs, on an Engine inputs sheet with one row per run (extract read, whether it was an older one, the allocations booked after its cut, the VaR reported, ERE's VaR on the book held): 27 runs read an older EQX and FUTS extract when the feed failed, and neither of the 2 exceptions on them (4 November 2024, 5 February 2025) is theirs, since ERE on the book held still falls short of each loss; every one of the 249 runs from 1 July 2024 read extracts cut as it started, before the middle office booked the day's closing-auction allocations (a median USD 39.2 million gross a night), which moved the VaR both ways (too high on 129 runs) and caused the 4 inputs exceptions, on 2 August 2024, 5 August 2024, 23 October 2024, 4 March 2025.
3. A sound model's count and zone, on a Sound model sheet with one row per day (hypothetical P&L, the sound model's VaR, exception): 2 exceptions, on 6 September 2024, 14 February 2025, the green zone; 0 to 2 across decay 0.94 to 0.97 at the portfolio or name by name, green throughout.
4. The add-on on the planned book month by month, on an Add-on sheet with a bar chart (each month's planned mid and small cap gross, futures contracts, names ERE proxies, own-history VaR, ERE's VaR, add-on), USD million: July 0.32 (0.24 to 0.34); August 0.27 (0.25 to 0.31); September 0.11 (0.09 to 0.13); October 0.08 (0.06 to 0.10); November 0.03 (0.01 to 0.05); December 0.00 (0.00 to 0.02).
5. A Summary sheet with the counts by heading and the corrected zone beside the official one, and a Routes sheet giving what each shortcut files beside the golden figure.

### backtesting_note_2025Q2.pdf

6. One page to the supervisor from the head of Market Risk Control: the corrected count against the official one, the heading table with its dates, a paragraph each on ERE's inputs and on the model, the add-on by month with the names proxied, and the actions (move ERE's extract after the allocation batch, fix the extract delivery, hold the add-on, bring the proxied names onto their own vendor history).

## Critical Components

1. There were **19** exceptions, not 15: **4** on hypothetical P&L that booked P&L hid (25 September 2024, 23 October 2024, 10 February 2025, 2 April 2025) and **1** on booked P&L only (3 April 2025).
2. **4** exceptions were caused by ERE's inputs, every one on a night its extract was cut before the closing allocations were booked (2 August 2024, 5 August 2024, 23 October 2024, 4 March 2025); the **27** runs that read an older extract caused **none**.
3. **11** exceptions are risks not in the model, the proxied names' own moves: 6 September 2024, 25 September 2024, 4 November 2024, 22 January 2025, 24 January 2025, 27 January 2025, 5 February 2025, 10 February 2025, 2 April 2025, 4 April 2025, 2 June 2025.
4. The add-on is **USD 0.32 million** for July and falls to **nil** by December as ERE's proxied names fall from **87** to **67**.

## Step-by-Step

1. From pc_daily_pnl_SMCF_2024-07-01_2025-06-30.csv (latest version of each day) against the previous evening's completed run in ere_run_log_SMCF_2024-06-28_2025-06-30.csv: 15 exceptions on booked P&L, as SMCF_VaR_backtest_2025Q2.xlsx files them, 18 on hypothetical P&L, 19 in all (MRS-4 3.3).
2. Rebuilt ERE from ERE_equity_VaR_methodology_note.pdf on the extract each run read (eqx_position_extract_v1_2024-06-28_2025-01-17.csv and eqx_position_extract_v2_2025-01-17_2025-06-30.csv through eqx_v2_instrument_crosswalk.csv, FUTS from futs_position_snapshots_2024-06-28_2025-06-30.csv, closes from vendor_eod_closes_SMCF_universe_2022-05-31_2025-06-30.csv keyed by vendor id): it matches all 251 runs in the log to the dollar.
3. The hurried reading stops there: the log's 27 runs on an older extract, re-run on that day's extract, cover 2 exceptions (4 November 2024, 5 February 2025), which it files under inputs, leaving 12 under (c) and 16 against the model.
4. Set each ticket's booking time in oms_trade_blotter_SMCF_2024-07-01_2025-06-30.csv against each extract's cut: every evening the closing-auction allocations are booked after the cut, so the book held is the extract plus those bookings (the trades rolled forward from the first extract give the same book), and on it ERE covers the loss on 2 August 2024, 5 August 2024, 23 October 2024, 4 March 2025 and on neither reused night.
5. Re-ran MRS-4 4(c) and 4(d) on the book held with vendor_eod_closes_SMCF_universe_2022-05-31_2025-06-30.csv: own history covers 11 more, the volatility-scaled VaR (decay 0.94, portfolio) 2, leaving 1 to model accuracy.
6. Counted the sound model over all 250 days (MRS-4 5): 2, green (0 to 2 across the settings); with the proxies kept 13 and with no volatility response 3.
7. Built each month's book from the 30 June run's extract by the basis in SMCF_H2_2025_business_plan.xlsx and priced it on the 30 June window and betas: July's add-on is USD 0.32 million, against the 30 June add-on of 0.18 scaled with gross (0.19).
8. Applied the note's 500-return rule to each name's store start in ere_proxy_mapping_vintages_2024Q2_2025Q2.csv for the run that sets each month's first VaR (MRS-4 3.4 and 6): ERE proxies 87, 82, 80, 73, 72, 67 names from July to December and the add-on runs 0.32, 0.27, 0.11, 0.08, 0.03, 0.00, where the 30 June mapping held under the plan's ramp gives 0.32, 0.28, 0.25, 0.30, 0.40, 0.40.

No other conclusion survives. The official count reads booked P&L alone and misses 4 exceptions; blaming the reused extracts charges the model 16, because only the blotter's booking times show what each extract lacked; every allowed volatility setting keeps the sound count at 0 to 2, green; and the add-on falls with the store's graduations whatever the ramp, so neither July's figure held flat nor the ramp alone (rising to 0.40) gives the months.
