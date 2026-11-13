# task22 architecture 1, platform run 2 (pasted by the author 2026-11-12; score not pasted, "both models landed ground truth")

Reviewed 147 resources
· 1h 1m
Recommendation.
Prioritize CHL-2, APT-4, NTH-4 and CHL-3 for the 2027 revenue protection sweep.

Together, they have 3,814.6 MWh of estimated non-technical loss, representing 69.44% of the signed system residual in the twelve months to September 2026. They occupy the four highest positions under the load-informed engineering model; these are screening estimates, not proven theft.

Final answers.
Feeder Ranking

The complete ranking is in revenue_protection_2027.xlsx, sheet Sweep Ranking. The four selected feeders are also named in sweep_memo_2027.pdf.

Rank    Feeder    Estimated Non-Technical Loss, MWh    Sweep
1    CHL-2    1,303.6    Yes
2    APT-4    1,145.2    Yes
3    NTH-4    685.0    Yes
4    CHL-3    680.8    Yes
5    APT-3    528.6    No
6    NTH-3    484.8    No
7    IND-3    400.1    No
8    CHL-1    103.3    No
9    APT-2    86.2    No
10    IND-2    67.2    No
11    NTH-1    45.7    No
12    IND-1    13.2    No
13    NTH-2    -15.0    No
14    APT-1    -35.3    No
Negative residuals are retained as evidence of measurement, calendarization or modeling mismatch. They do not mean "negative theft."

Monthly Energy Balances

The Monthly Balance sheet contains 504 feeder-months, covering all 14 feeders from October 2023 through September 2026. Each row includes:

Customers served at month end.
Breaker energy and customer-generation exports.
Calendarized metered imports.
Separately identified provisional-read and startup-consumption estimates.
Physical City lighting consumption.
Primary, transformer core, transformer load and secondary/service losses.
Non-technical residual, reconstructed-hour count and balance check.
System customer counts increase from 8,749 at October 2023 month end to 9,022 at September 2026 month end.

Across the full historical period, the balances contain 729,601.2 MWh of total input, 673,353.3 MWh of calendarized metered imports, 3,504.6 MWh of physical City lighting, 37,081.9 MWh of feeder technical losses and 15,296.8 MWh of signed non-technical residual. Legitimate consumption estimates are shown separately rather than labeled as recorded meter consumption. These totals are also in Data Audit.

Attribution of the Increase

The Attribution sheet reconciles the published increase from 7.74% to 8.24%:

Component    Contribution, Percentage Points
Technical losses, including substations    +0.3418
Non-technical losses    +0.4082
Everything else, including report reconciliation    -0.2500
Published increase    +0.5000
"Everything else" includes station service, billing/calendar timing, legitimate-use estimates, physical-versus-billed lighting and upstream meter-boundary differences.

The underlying interval and billing records imply a 0.4974-point increase. An explicitly disclosed +0.0026-point report reconciliation closes this to the published 0.5000 points. The workbook does not silently force the underlying data to match the annual report.

Approved Large Connections

Individual additional hourly-average peak demand is reported in Approved Loads, with the hourly energy profiles in New Load Hours.

Approved Connection    Feeder    Service Date    Added Hourly Peak
Prairie Fresh Cold Storage, freezer expansion    APT-3    April 1, 2027    541.2 kW
Flint Ridge Cultivation LLC    APT-4    May 1, 2027    931.2 kW
Wildhorse Greenhouse    CHL-3    August 1, 2027    520.3 kW
These are individual-service peaks, not their contributions at the system coincident peak or their highest 15-minute billing demands. The workbook separately shows the lower maxima of the averaged hourly profiles used for energy forecasting.

2027 Technical Losses

Annual results are in 2027 Technical; monthly components are in 2027 Monthly.

Feeder    Forecast Technical Losses, MWh
NTH-1    1,166.3
NTH-2    715.4
NTH-3    358.0
NTH-4    724.7
IND-1    1,570.5
IND-2    908.9
IND-3    609.9
APT-1    885.4
APT-2    684.3
APT-3    1,577.1
APT-4    1,941.6
CHL-1    962.8
CHL-2    1,021.2
CHL-3    730.6
Total    13,856.8
These exclude substation transformer losses and station service. APT-3's approved reconductoring saves 751.1 MWh against the same forecast load without that work.

Memo

sweep_memo_2027.pdf is a verified single-page memo naming the four sweep feeders, their estimated losses, the loss-rise attribution, major 2027 implications and the selection caveat.

Step-by-step process.
Inspected the supplied archive and all source types. The archive contained the annual loss report, customer reads, breaker and delivery-point measurements, large-customer intervals and applications, network and transformer records, switching/outage records, lighting inventory and billing, engineering tables, station data, weather and six policy/tariff/engineering PDFs. The workbook's Sources sheet identifies every file and its use. Weather was inspected but not used for normalization because the budget instructions prohibit it. Tariffs informed definitions, not dollar valuation.

Reconstructed customer consumption rather than summing bills by issue month. Removed 6,609 exact duplicate CIS rows from 364,982 raw rows. Preserved 7,804 meter exchanges and 205 negative billing adjustments. Bridged 9,911 estimated reads to subsequent actual endpoints, producing 331,636 actual-to-actual intervals, with no negative reconstructed intervals. Supplied kWh was already multiplied, so multipliers were not applied again.

Kept incomplete observations visible. Identified 48 unresolved estimated-read tails, contributing 29.6 MWh of provisional consumption within the study. Estimated uncovered startup consumption separately: 192.2 MWh for Osage Hills Farms and 142.7 MWh for Prairie Fresh. These are not presented as actual meter observations. Base-year interval data replaced calendarized consumption for all 25 LP/CITY-NB services.

Aligned and repaired the hourly measurement grid. Averaged 42 repeated autumn clock labels, reconstructed the absent spring grid cells and retained 223 good-quality zero readings. The study required reconstruction of 4,108 feeder-hours, totaling 8,421.6 MWh. Missing active power was constrained by upstream delivery energy after station losses, station service and other measured feeders. The critical 249-hour CHL-3 gap reconstructed 714.5 MWh.

Rebuilt historical supply paths. Used the physical graph of 1,056 segments and 47 switches, with dated transformer lifetimes and minute-level switching. This captured two permanent and three temporary transfers, resolved all switching identifiers and corrected two stale current service-feeder labels. Outage records corroborated planned switching; the 791 overlapping unplanned events lacked the asset identifiers needed for exact asset-level adjustments.

Estimated physical lighting and technical losses. Used 2,367 lamps, including 1,769 recorded LED conversions, rather than fixed billed lighting allowances. Technical losses were integrated hourly using conductor resistance, phase treatment, transformer size/vintage tests and the secondary/service coefficient. LP load remained at its actual transformer location; other loads used monthly customer-energy weights.

Solved the physical balance before estimating the residual. Iteratively matched terminal demand plus engineering losses to breaker input. Conflicting LP/head-load observations were constrained only within the loss model, without changing the separate metered-energy ledger. The maximum base-year hourly closure error was 0.0004 kW; annual closure was 0.6 kWh after numerical storage.

Built and validated the connection-demand model. Used nine cultivation services and one cold-storage service as operating analogs. Whole-service holdouts gave cultivation hourly RMSE of 22.11 kW and WAPE of 4.98%. Pooled component regression and cultivation-only component regression had higher RMSEs of 24.02 kW and 24.20 kW. The cold-storage estimate has no independent within-class validation because only one analog exists.

Forecast 2027 using the required policy. Replayed matching base-year calendar months without weather normalization or generic growth, applied current normal topology, added only approved connections from their service dates and changed the 17 specified APT-3 segments from March 15. No technical savings were invented for AMI, pole work or an unquantified regulator change.

Checked the final artifacts. Verified every historical balance identity, ranking order, attribution formulas and forecast totals. Checked cached spreadsheet results for errors and external links. Confirmed the PDF has one page and visually inspected its layout. Temporary analysis files were removed.

Assumptions and judgment calls.
Non-technical loss is an estimated residual. The data cannot independently identify theft, tampering, meter error and remaining model error, or establish a recoverable fraction.
Non-interval consumption is uniformly calendarized between reads. Startup gaps and unfinished estimates are separately disclosed. These choices affect attribution more than the four-feeder selection.
Historical connectivity follows logged switching and effective asset dates. Current geometry is carried backward where no historical geometry exists. The 22 minutes of dual-source transitions use the preceding radial configuration because parallel-flow measurements are unavailable.
Technical losses assume nominal voltage and modeled spatial load allocation. Unmeasured voltage, phase imbalance and the location of unmetered use remain material uncertainties.
The fourth slot is sensitive. CHL-3 leads APT-3 by 152.3 MWh. Reducing APT-3's technical-loss estimate alone by 9.00%, holding other estimates fixed, removes that margin.
New-load forecasts assume analogous operation and immediate scheduled startup. Flint Ridge exceeds the largest cultivation analog, and the freezer expansion has a different equipment mix from the sole cold-storage analog.
These judgments are documented in Methods, Sensitivity and Approved Loads.

Alternatives rejected.
Treat the full reported increase as theft. Technical losses contribute +0.3418 points, while other accounting and legitimate-use effects offset part of the increase.
Reuse the historical fixed technical-loss percentage. The 2019 study reflects older assets and loading and excludes substation losses.
Use today's feeder labels throughout history. The documented transfers, transformer replacements and stale service labels contradict that approach.
Use billed lighting as physical consumption. Seasonal burning hours, ballast inputs and LED conversions make the two quantities different.
Forecast connected equipment kW as demand. Observed operating profiles and service-level validation support materially lower demand estimates.
Claim the selected four are robust to every reasonable engineering assumption. They are not. Both the 20% lower-technical-loss scenario and legacy transformer-kVA allocation substitute APT-3 for CHL-3. The central model is preferred because it retains measured customer concentration and interval load profiles; the competing result remains prominently disclosed.
Files produced.
/home/agent/workspace/revenue_protection_2027.xlsx: rankings, monthly energy balances, loss attribution, approved-load demand estimates, 2027 technical-loss forecasts, hourly audit, assumptions, sensitivity tests and source records.
/home/agent/workspace/sweep_memo_2027.pdf: single-page decision memo naming the four sweep feeders.
Packages installed.
Installed NumPy, pandas, SciPy, openpyxl, PyMuPDF, scikit-learn, ReportLab, XlsxWriter and pypdf, with their dependencies, in temporary Python environments.
