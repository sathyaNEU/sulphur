Response 2

Reviewed 71 resources
· 26m
Recommendation. Permit Alternative C: 1,000 gpm nominal annual average (1.44 MGD), split equally between PW-1 and PW-2, starting April 2027 and ending December 2046, at the application's monthly factors. Its greatest 2046 OW-S drawdown is 8 ft, below the 9-ft Table 1 limit; Alternative D reaches 10 ft and fails.

Final answers.

Permitted withdrawal: Alternative C. Its total field rates from January through December are 780, 760, 800, 880, 1,020, 1,210, 1,340, 1,310, 1,170, 980, 880 and 870 gpm, respectively, divided equally between the production wells. January-March 2027 is zero because pumping begins in April. These conditions appear on page 1 of reidel_road_WR-4_demonstration.pdf and in the workbook's Decision, Inputs and C_1000 sheets.
Monthly demonstration: The PDF's "Monthly Sentinel Forecast" charts all four alternatives for all 240 months from January 2027 through December 2046, against the 9-ft limit. The workbook contains all 960 schedule-month calculations in A_450, B_700, C_1000 and D_1250, with source contributions, totals, headroom and full-precision compliance checks.
Greatest OW-S drawdown in 2046: A: 4 ft; B: 6 ft; C: 8 ft; D: 10 ft. All occur in July 2046. These results appear on PDF page 1 and in the workbook's Decision sheet.
Nearest registered domestic well: DW-17, located 3,041 ft from PW-1. Under Alternative C, its greatest combined drawdown in 2046 is 7 ft, in July. See PDF page 1 and the workbook's Domestic C sheet.
Mill Street's 2025 impact: 5 ft of average pumping-caused drawdown at MS-MW, calculated from the 12 monthly observations after correcting measuring-point changes and regional water-level variation. The independently calibrated groundwater model also gives 5 ft when rounded. See PDF "Historical Attribution" and workbook MS 2025.
All requested drawdowns are reported to the nearest foot. Compliance calculations retain unrounded values.

Step-by-step process.

Established the regulatory test. Read CVWCD_Rule_WR-4_groundwater_withdrawal_permits.pdf and reidel_road_WR-4_application_requested_schedules.pdf. WR-4 requires combined proposed and existing permitted drawdown at OW-S to remain below the limit in every month, and requires selection of the largest passing requested alternative.

Established aquifer geometry and receptor locations. Used CVWCD_bedrock_surface_plate3_harlow_reach.png, drillers_logs_corrin_valley_wells.pdf and cvwcd_well_register.xlsx. The logs and plate support a till-confined sand-and-gravel aquifer bounded laterally by shale. The model represents a 5,000-ft-wide strip trending 18 degrees east of north. Registered coordinates identify DW-17 as the nearest domestic receptor.

Corrected the pumping-test records. Combined PW-1_constant_rate_2026-09_transducers.csv, barologger_BL-2231_2026-09.csv and PW-1_constant_rate_2026-09_field_readings.xlsx. Removed 3 exact duplicate copies from 103,682 logger rows. Converted the UTC loggers and barometer to EDT, interpolated barometric pressure between its recorded times, and corrected absolute sensor pressures. Applied OW-2's sensor-depth change from 61.03 to 62.40 ft at 14:20 EDT on 12 September 2026. Its 7 missing minutes were not filled.

Checked test measurements and fitted aquifer response. Removed pre-test drift and physical barometric response separately from instrument-pressure compensation. 55 manual readings matched logger timestamps with 0.008-ft RMSE; 6 initial readings preceded recording and were not extrapolated. Totalizer records, including the final interval inferred from the last recorded rate, give 4,341,480 gal over the 72-hour test, averaging 1,004.972 gpm. Fitted 4,415 ten-minute observations from five observation wells through pumping and recovery. The resulting parameters are T = 8,003.83 ft²/day, S = 0.00100252, and B = 3,503.75 ft, with 0.010-ft test RMSE.

Reviewed supporting files that were not suitable for regional calibration. Read PW-1_step_drawdown_2026-08-27.csv, containing 640 rows, but did not transfer pumped-well losses into the regional aquifer model. Reviewed the 30 analyte results in PW-1_raw_water_quality_2026-09.xlsx; treatment chemistry does not determine the WR-4 hydraulic drawdown decision.

Prepared historical water levels. From cvwcd_network_water_levels_2005-2026.csv, removed 13 duplicate copies and 20 uncertain E readings, leaving 1,878 observations. Applied the CV-07 casing correction to 102 retained earlier readings. Retained all 220 readings in mill_street_MW_water_levels_2008-2026.csv, using the old measuring point for 107 and the casing extension for 113. The April 3, 2017 observation remains on the old datum because the extension took effect on April 11.

Standardized historical production. Retained all 359 records in harlow_springs_MOR_well_production_2009-2026.csv. Standardized 113 source aliases, converted 113 thousand-gallon records, and divided volumes by actual calendar-month durations. Retained the 3 zero-production outage records and the meter-replacement estimate. Volumes reconcile to 2,780,679,845 gal for TW-1 and 1,325,547,038 gal for TW-2. TW-2's 63 pre-commissioning months were assigned zero rather than treated as missing operations.

Separated historical pumping effects from natural variation. Used remote, same-aquifer wells CV-02 and CV-11 as monthly reference heads, with offsets established before Mill Street pumping. Used the available reference in 12 months with one missing control and left comparisons blank in 2 months with neither. No heads were interpolated. The independently fitted model's historical RMSE is 0.197 ft at OW-S, 0.125 ft at CV-07, and 0.342 ft at MS-MW. The reference-adjusted and modeled 2025 MS-MW averages both round to 5 ft.

Forecast every requested schedule. Carried metered Mill Street history through September 2026 and applied the filed projection thereafter, retaining the 56/44 source split. Applied the Reidel monthly factors and equal source split from April 2027. Calculated source-specific responses using repeated image wells and transient superposition, then summed Mill Street and Reidel contributions at OW-S and DW-17.

Checked the deciding threshold and robustness. C's ordinary peak leaves 0.812 ft of headroom. A more conservative bound, holding each source at its greatest historical or projected monthly rate, still leaves 0.771 ft below the limit and covers times between month-ends. D exceeds the limit at 47 month-ends, first in July 2027. Held-out recovery and OW-S predictions have RMSEs of 0.014 ft and 0.012 ft, respectively. Tested geometry, growth and seasonal-factor variations preserve the recommendation.

Validated the deliverables. Independently recomputed the workbook's forecast totals using full-history superposition; the compact spreadsheet calculations agree within 1e-9 ft per component. Checked formula references and cached cells for errors, verified complete monthly coverage, and rendered and reviewed the seven-page PDF. Temporary analysis files were removed.

Assumptions and judgment calls.

Existing-withdrawal inventory: TW-1 and TW-2 are the documented existing sources with filed projections. No unprovided domestic or third-party pumping rates were invented. Additional material withdrawals would require a revised combined demonstration.
Monthly operating interpretation: The application's rates are modeled as continuous monthly-equivalent withdrawals. Unspecified high-rate daily cycling is not certified.
Aquifer persistence: The model assumes spatially uniform aquifer properties and sustained leakage head. The mapped geology, test and historical checks support this representation, but cannot guarantee unchanged conditions throughout the permit term.
Application arithmetic: Printed Mill Street annual anchors override unrounded growth in those years. Seasonal factors are used literally rather than renormalized. Consequently, C's full common-year average is 1,001.589 gpm, while its application label remains the nominal 1,000 gpm. Tested alternative conventions do not change the decision.
Historical averaging and uncertainty: The primary MS-MW result uses an equal-month average. Alternative reference choices and day-weighting preserve the 5-ft answer. Sensitivity checks are not presented as probabilistic confidence intervals.
Alternatives rejected.

Alternative D: Its 10-ft final-year maximum and 47 failing month-ends violate WR-4.
Alternatives A and B as the permit choice: Both pass, but WR-4 requires the largest passing requested schedule, which is C.
Unbounded or nonleaky aquifer models: Test RMSE rises to 0.214 ft for the unbounded leaky model and 1.932 ft for the nonleaky strip, versus 0.010 ft for the selected model.
Raw water-level change as pumping drawdown: Correcting only the MS-MW measuring-point change gives a head decline of 3 ft, not the pumping attribution of 5 ft. The raw depth change happens to round to 5 ft, but that agreement is coincidental because it mixes casing and regional-head effects.
Shallow or bedrock reference wells: CV-04/CV-09 and CV-13 monitor different units. CV-05 lacks a pre-Mill baseline. They were reviewed but not used as the primary counterfactual controls.
Files produced. Saved under /home/agent/workspace:

reidel_road_WR-4_demonstration.pdf: Seven-page permit demonstration with the decision, monthly charts, required drawdown findings, methods, validation and limitations.
reidel_road_sentinel_forecast.xlsx: Auditable monthly calculations for every schedule, source-response arithmetic, domestic and historical results, source records and quality checks.
Packages installed. NumPy, SciPy, pandas, openpyxl, Matplotlib, PyMuPDF, ReportLab, Pillow and XlsxWriter were installed in an isolated uv runtime because the advertised analytical packages were unavailable in the active interpreter.
