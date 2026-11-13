# task22 architecture 1, platform run 1 (pasted by the author 2026-11-12; score not pasted, "both models landed ground truth")

Reviewed 106 resources
· 1h 5m
Recommendation. Select CHL-2, APT-4, NTH-4, and CHL-3 for the 2027 revenue protection sweep. Together, they account for 3,972.6 MWh, or 67.41% of the estimated system non-technical residual; fourth-ranked CHL-3 exceeds fifth-ranked APT-3 by 46.5 MWh.

Final answers. Feeder ranking, October 2025-September 2026: The following estimates are in Revenue_Protection_2027.xlsx, sheet Rankings. The selected four also appear in the PDF memo.

CHL-2: 1,344.6 MWh. Selected.
APT-4: 1,215.6 MWh. Selected.
NTH-4: 710.3 MWh. Selected.
CHL-3: 702.1 MWh. Selected.
APT-3: 655.6 MWh.
NTH-3: 487.0 MWh.
IND-3: 415.2 MWh.
CHL-1: 111.5 MWh.
APT-2: 92.4 MWh.
IND-2: 80.9 MWh.
NTH-1: 65.9 MWh.
IND-1: 41.6 MWh.
NTH-2: -10.0 MWh.
APT-1: -19.4 MWh.
These are engineering residuals, not directly measured or proven theft. Negative residuals are retained rather than concealed.

Monthly energy balances: Monthly balances contains 504 rows: 14 feeders across 36 months, October 2023-September 2026. Each row includes month-end customers and lights, breaker input, customer generation exports, total input, customer meter-based imports, municipal lighting, four technical-loss components, non-technical residual, provisional consumption, and a balance check.

Month-end customers are unique active service points, including municipal metered services. System counts increased from 8,836 in September 2024 to 9,022 in September 2026.

The FY2026 system balance, also summarized in Annual totals, is:

Breaker input: 248,001.8 MWh.
Customer generation exports: 2,557.7 MWh.
Total feeder input: 250,559.5 MWh.
Customer meter-based imports: 231,074.2 MWh.
Physical municipal lighting: 874.4 MWh.
Feeder technical losses: 12,717.7 MWh.
Non-technical residual: 5,893.2 MWh.
Contribution to the line-loss increase: Loss bridge reconciles the published purchased and billed energy totals. Their calculated loss rates are 7.738568% and 8.235124%, an increase of 0.496556 percentage points:

Technical losses: +0.295987 percentage points, including feeder and substation transformer losses.
Non-technical residual: +0.469942 percentage points.
Everything else: -0.269373 percentage points.
Display rounding: +0.003444 percentage points, reconciling the calculated increase to the quoted 0.500000-point rise.
"Everything else" includes billing timing, physical-versus-billed lighting, export timing, station service, upstream closure, and source-boundary differences. The increase therefore should not be described as entirely theft.

Approved 2027 connections: Forecast maximum hourly average demands appear in 2027 connections, with calibration in Peak calibration.

Wildhorse Greenhouse, CHL-3: 526.9 kW, scheduled for August 1, 2027. Conditional 95% prediction interval: 490.8-563.0 kW.
Flint Ridge Cultivation LLC, APT-4: 940.9 kW, scheduled for May 1, 2027. Conditional 95% prediction interval: 898.1-983.7 kW.
Prairie Fresh Cold Storage freezer expansion, APT-3: 542.9 kW, scheduled for April 1, 2027. Conditional 95% prediction interval: 499.6-586.3 kW.
These are hourly demand forecasts, not connected nameplate loads or 15-minute billing maxima. Service-date-gated energy and peak scenarios are included separately in the workbook.

2027 feeder technical losses: 2027 feeder losses contains the annual forecasts; 2027 monthly contains their monthly construction.

NTH-1: 1,152.6 MWh.
NTH-2: 709.8 MWh.
NTH-3: 353.1 MWh.
NTH-4: 700.7 MWh.
IND-1: 1,538.9 MWh.
IND-2: 901.5 MWh.
IND-3: 592.5 MWh.
APT-1: 875.0 MWh.
APT-2: 678.1 MWh.
APT-3: 1,489.5 MWh.
APT-4: 1,773.5 MWh.
CHL-1: 952.0 MWh.
CHL-2: 973.9 MWh.
CHL-3: 710.1 MWh.
The total is 13,401.2 MWh, calculated before display rounding. Substation transformer losses and station service are reported separately. Approved APT-3 reconductoring saves 631.6 MWh relative to the same forecast loads without that work.

Single-page memo: Revenue_Protection_2027_Memo.pdf names the four feeders and summarizes the selection, loss-rate bridge, connection peaks, budget forecast, and fourth-slot uncertainty.

Step-by-step process.

Inspected all supplied inputs. All 22 files in input-assets/22.zip were reviewed. The workbook's Sources sheet records each filename and its use or exclusion rationale.

Established the measurement and billing boundaries. Used annual_line_loss_report_2019-2026.xlsx, bmpa_delivery_point_interval_2023-09_2026-10.csv, historian_feeder_breakers_hourly_2023-09-01_2026-10-31.csv, cis_meter_reads_2023-08-01_2026-11-01.csv, idr_large_power_interval_2025-10_2026-09.csv, and unmetered_lighting_billing_2023-09_2026-10.csv. These distinguish wholesale purchases, feeder input, physical customer consumption, exports, and quantities appearing on bills.

Reconstructed the network and equipment history. Used gis_electric_network_2026-10-27.xlsx, transformer_asset_register_2026-10-27.xlsx, oms_switching_orders_2023-09_2026-10.csv, and oms_gis_device_crosswalk_2024-07.xlsx. The model traces 1,056 primary segments, 47 switches, and 3,139 transformer histories. It replays 124 switch operations rather than applying the current feeder labels to every historical month. Seven legacy operations required exact normalized pole-tag matching beyond the supplied crosswalk. Both retired transformers were restored in the model before their replacement dates.

Applied the engineering and policy sources. distribution_engineering_tables.xlsx, substations_and_station_service.xlsx, and loss_evaluation_study_2019_hester.pdf supplied resistance, transformer-loss, secondary-loss, and station-service inputs. rfp_2026-14_revenue_protection_scope.pdf established the four-feeder, residual-MWh selection rule. fy2027_budget_instructions_electric_fund.pdf and cwp_2027-2028_approved_projects_excerpt.pdf established the forecast calendar and approved-work restrictions.

Cleaned and reconstructed customer consumption. Removed 6,609 exact duplicates from 364,982 CIS rows, leaving 358,373 records. Grouped histories by service point and meter rather than account number. Skipped 9,911 estimated-read endpoints when constructing physical intervals, while retaining their billed quantities and subsequent corrections between actual reads. Reconciled 663 register rollovers and 7,804 final AMR reads associated with replacements. There were zero negative corrected usage intervals and zero unmatched CIS service points.

Made uncovered consumption explicit. Estimated three initial large-service gaps, one outside the requested window. At the archive boundary, 48 services had 893 service-days not closed by an actual read. Their provisional FY2026 consumption is 29.670882 MWh of imports and 0.402158 MWh of exports. These amounts are disclosed in Provisional reads and separated from interval-supported consumption in Monthly balances; they are not silently treated as zero.

Aligned the clocks and repaired telemetry gaps. Converted historian civil time to fixed CST and retained all 42 repeated fall-back clock keys. Shifted wholesale hour-ending and IDR interval-ending records to hour starts. Preserved 223 good-quality zero-MW records. Within the requested period, reconstructed 4,066 missing breaker point-hours, or 1.104123% of the requested feeder-hours, using wholesale reconciliation and available feeder profiles. The missing final IDR boundary hour was estimated for 25 services using the same hour one week earlier.

Calculated physical lighting separately from billing. Used street_area_lighting_inventory_2026-10-27.xlsx with lamp input watts and burning hours. The calculation follows 2,367 lamps and 1,769 dated LED conversions. The retail tariff PDF was used to interpret deemed lighting billing and distinguish hourly demand from billing demand; its prices were not used to rank physical energy loss.

Estimated technical losses and formed the residual. Allocated large loads to their actual transformer nodes and other demand by monthly service-load shares. Calculated hourly conductor losses from resistance and squared apparent-power flow, transformer no-load and load losses, and secondary/service losses. The model uses current loading and dated topology, not a uniform historical loss percentage. The residual is total input minus customer imports, physical lighting, and modeled feeder technical losses.

Calibrated approved-load forecasts. Joined large_load_service_applications_2019-2027.xlsx to hourly IDR data. Ten energized applications supplied the independent peak observations; three approved applications entered the forecast, and two withdrawn applications were excluded. The component model's site-holdout RMSE was 18.611859 kW, compared with 42.628525 kW for a pooled connected-load model. Hourly loss forecasts use cultivation analog scenarios and the available cold-storage analog, with losses calculated before averaging scenarios.

Built the 2027 forecast and accounting bridge. Replayed corresponding base-year months without a weather or generic-growth uplift. Added approved connections on their service dates and changed only the named APT-3 conductor segments from March 15. Reconciled the historical loss bridge to published purchased energy of 236,620 MWh and 249,468 MWh, and billed energy of 218,309 MWh and 228,924 MWh.

Checked contextual evidence and final artifacts. Reviewed delmont_municipal_airport_daily_2023-09_2026-10.csv for historical weather context, but did not weather-normalize the forecast. Reviewed oms_outage_events_2023-09_2026-10.csv; its lack of device identifiers prevents precise allocation of every partial outage to individual transformers. The wholesale tariff PDF established the fixed-CST convention, but prices were not needed for this energy-ranking task. Verified all monthly balance identities, annual forecast totals, connection formulas, bridge calculations, cached spreadsheet formulas, and the PDF's single-page text bounds.

Assumptions and judgment calls.

Residual loss is not proven theft. It includes theft, tampering and other unmetered use, but also remaining metering, timing, topology and engineering-model error.
Calendar allocation is estimated where hourly meters are unavailable. Actual-to-actual consumption is allocated uniformly by day. Provisional starting and terminal intervals remain separately visible.
Customers mean active service locations. Account changes and meter replacements do not increase customer counts. Municipal metered services are included; lamps are counted separately.
Technical losses use the documented R50 reference. The model assumes nominal voltage and is not a full AC load-flow solution. Unknown unmetered demand is allocated with observed service-load shares, and lighting energy is spread uniformly within each month for current modeling.
The fourth slot is uncertain. A common 5.17% reduction in technical-loss estimates ties CHL-3 with APT-3. The recommendation uses the documented central estimate, not a claim that the ordering is statistically certain.
2027 means calendar 2027. This follows Finance's explicit same-month instruction. Connections start immediately on scheduled dates, with no assumed ramp-up, weather uplift, generic growth, or authorized theft recovery.
Connection intervals are conditional. Flint Ridge exceeds the size of every cultivation analog, and only one cold-storage analog is available. The reported prediction intervals do not encompass every operational risk.
Alternatives rejected.

Ranking by total losses or loss percentage: rejected because the RFP requires absolute non-technical residual MWh after subtracting authorized consumption and engineering losses.
Applying the 2019 system loss factor of 4.23%: rejected because it uses older topology and loading and cannot represent current feeder-specific losses.
Using billed lighting as physical consumption: rejected because dated LED conversions and lamp-plus-ballast wattage produce different physical energy quantities.
Treating connected kW as peak hourly demand: rejected because the component model performs better in site holdouts and distinguishes cultivation from cold-storage load composition.
Attributing the entire increase to theft: rejected because technical losses contribute +0.295987 points, while other accounting and physical-use effects offset 0.269373 points.
Calling the selected energy guaranteed recoverable revenue: rejected because residuals are not verified theft and no recovery or collection rate is established.
Treating APT-3 as conclusively excluded: not supported. Both the R25 and lower-technical-loss sensitivities put APT-3 in the four and CHL-3 outside. This is material evidence against certainty in the fourth slot, disclosed prominently in both deliverables.
Files produced.

/home/agent/workspace/Revenue_Protection_2027.xlsx: Audited spreadsheet with rankings, monthly balances, loss attribution, approved-load forecasts, 2027 technical losses, sensitivities, source register, and embedded calculation code.
/home/agent/workspace/Revenue_Protection_2027_Memo.pdf: Single-page decision memo naming the four feeders and explaining the principal evidence and uncertainty.
Packages installed. The advertised analytics packages were unavailable in the active interpreter. An isolated temporary environment was created with NumPy, pandas, SciPy, openpyxl, PyMuPDF, ReportLab, Matplotlib, XlsxWriter, and their dependencies. Temporary analysis scripts were removed from the workspace.
