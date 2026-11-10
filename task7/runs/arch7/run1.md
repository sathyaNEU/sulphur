# Platform run on architecture 7 (2026-11-09)

Pasted by the author after testing architecture 7 on the platform (target.zip 00c9970f); no score was pasted, the
author read it as not stumped. Against the golden: the seasons, the use split, the fade (a latest-three plateau), the
ranges, the flip rates, the listing and the 2025/26 CO2 all within or near their bands and the call landed; it lost
the round at close (insulation 312 applications against 343, asked 5.31 against 6.11 million) and heating
optimisation's figure (139 against 158 euro a tonne). It used the electricity file only to look for supply exits and set
the solar cadastre aside as unrelated. The run, verbatim:

Reviewed 83 resources
· 37m
Recommendation. Fund insulation and heating controls; do not fund heating optimisation. Their estimated grants per lifetime tonne of CO2 are EUR 87.42, EUR 94.58 and EUR 139.08, respectively, against the council’s EUR 120 limit.

The answer-first, one-page note and supporting workbook are saved under /home/agent/workspace.

Final answers. All sheet references below refer to Haldenau_2026_Grant_Appraisal.xlsx.

The pilot’s estimated normal-weather saving rates in its works buildings are:

Season    Insulation    Heating optimisation    Heating controls
2019/20    14.65%    12.04%    4.94%
2020/21    16.39%    5.25%    5.39%
2021/22    16.17%    2.30%    4.39%
2022/23    16.68%    1.49%    3.74%
2023/24    16.56%    1.42%    4.01%
2024/25    16.60%    1.50%    4.02%
2025/26    16.79%    1.31%    3.96%
Pilot Seasons contains these rates, their 90% ranges, saved MWh, counterfactual consumption and CO2. Buildings receive no further retrofit credit after recorded gas-supply exit.

For the latest applications received through 12 June 2026:

Measure    Applications    Lifetime Saving Rate    Grant per Lifetime tCO2    90% Range    Flip Saving Rate
Insulation    123    16.01%    EUR 87.42    EUR 80.61-97.89    11.66%
Heating optimisation    247    2.59%    EUR 139.08    EUR 108.50-203.49    3.00%
Heating controls    532    7.34%    EUR 94.58    EUR 87.53-102.75    5.79%
These appear in Measure Appraisal and the note’s decision table. The workbook retains unrounded thresholds: equality qualifies; savings below the threshold reject a measure. Optimisation’s uncertainty range crosses EUR 120, but its point estimate fails the council’s test.

The closing forecast is:

Measure    Expected Applications    Grants Requested    Expected Payment Under Recommendation
Insulation    311.8    EUR 5,310,476    EUR 4,805,333
Heating optimisation    453.2    EUR 1,094,988    EUR 0
Heating controls    660.8    EUR 1,666,820    EUR 1,646,756
Funded round total    972.5    EUR 6,977,296    EUR 6,452,089
Forecast contains current, future and closing amounts, including hypothetical payments if an unfunded measure were approved. Totals use unrounded estimates.

Plan for 973 funded applications. Exact statutory award exposure is EUR 6,977,396 if all awarded works complete.
Expected completed funded works are 945.7, carrying 71,747.35 lifetime tonnes.
Funded Awards lists every one of the 655 funded applications already received, with application and building identifiers, requested grant, statutory award and lifetime tonnes. They total EUR 3,051,800.00 in awards and 33,778.02 lifetime tonnes.
The pilot’s works saved 3,318.73 tCO2 in 2025/26, with a 90% sampling range of 3,035.69-3,621.32 tCO2. The measure components are insulation 2,120.94, optimisation 213.77, and controls 984.01 tCO2; the total is calculated before rounding. See CO2 2025-26, Pilot Seasons and the note’s monitoring section.
Step-by-step process.

Read the complete input archive. The applications, pilot draw and building-register workbooks supplied applications, allocation, completion, use and area. Gas reads, meter metadata, calorific values and weather files supplied consumption reconstruction. Benchmarking notices supplied offer populations and statutory reference intensities. The committee request, climate plan, benchmarking method and grant terms established the definitions, threshold and deadlines. The heat-plan and federal-funding documents were reviewed but did not override the statutory appraisal. Electricity records were used only to investigate supply exits; the solar cadastre was excluded as unrelated to these gas-saving measures.

Resolve application revisions and eligibility. The 938 submissions became 902 current applications after removing 36 superseded submissions. All current applications matched the register and current offer; none belonged to a pilot completer. Revisions preserves the excluded submissions and their replacements.

Reconstruct seasonal gas consumption. From 389,104 readings, remove 1,583 exact duplicates and 7,442 superseded same-meter/date records, preferring corrections. Difference readings within physical meters, handle 27,077 five-digit rollovers, apply meter factors and z-numbers, allocate off-date intervals using daily heating weights, and apply the appropriate network-season calorific value. Replacement meters are never differenced against their predecessors.

Normalise weather and audit coverage. Hold each use type’s hot-water/process share fixed and normalise the remainder to 3,635 degree days. The reconstruction produced 302,106 building-seasons, with no incomplete extant meter-point seasons. Comparison with notices retained discrepancies rather than forcing agreement. Daily and monthly weather totals differed by at most 1.7 degree days.

Preserve the randomized comparison. Retain all 3,055 pilot respondents, including 1,375 winners, 1,338 completers and 37 withdrawn winners. Estimate seasonal works effects using lottery assignment as the instrument for completion, adjusting for use and pre-pilot consumption. This avoids treating owners who completed works as if they were randomly selected.

Handle unavailable supply explicitly. Missing pre-period observations numbered 50, 35, 20, 12, 0 and 0 across the six pre-seasons; baselines used available observations. Post-season unavailable buildings numbered 6, 26, 38, 49, 58, 66 and 81. Seasonal models used observed outcomes. Monitoring gives no post-exit credit to the 32 affected completers, leaving 1,306 observed-supply works in the latest monitoring total.

Transport effects and calculate lifetime value. Estimate separate saving fractions by building use, then weight them using the current applications’ prescribed reference consumption. Lifetime profiles use the seven observed seasons followed by the latest-three-season mean through the statutory 30-, 15- and 10-year lives. Lifetime tonnes use 0.201 tCO2/MWh. The 90% ranges come from 2,000 building-bootstrap replicates per measure, retaining each building’s seasonal history.

Forecast arrivals, quotes and completion separately. Model early response, late response and nonresponse among 4,631 pilot offer recipients, then calibrate to observed applications among 3,744 current recipients. Forecast additional responses from the 2,842 remaining recipients. Future quotes allow late applicants to be more expensive; completion probabilities account for quote size and response timing. The pilot lottery fraction is not applied to the current round.

Validate the artifacts and calculations. Five-fold pilot forecast checks predicted 767.23, 1,032.64 and 1,259.43 final applications against actual counts of 765, 1,031 and 1,259. Independent auditing recalculated all 11,836 workbook formula cells and reconciled the funded list, seasonal effects, forecast totals and bootstrap ranges. Both files reopen correctly; the workbook has no cached spreadsheet errors or external workbook links. Temporary analysis files were removed.

Assumptions and judgment calls.

Long-term persistence is the main decision risk. The latest-three-season plateau is supported by recent pilot behaviour, but is not proof of durability over the full statutory life. A 5% annual decline after year seven would raise insulation to EUR 130.73/t and reverse its decision. This sensitivity is prominent in both deliverables.
Age and calendar effects cannot be separated completely. The lifetime calculation assumes the pilot’s initial seasonal pattern recurs for new works. The uncertainty ranges do not cover this structural assumption.
Transport assumes comparable efficacy within use types. An additional check allowing area and intensity to modify effects preserved all three decisions.
Supply exit is not attributed to the retrofit. Extending fitted savings to the exited works would add 74.91 tCO2, giving 3,393.64 tCO2. That is a scenario, not the monitoring headline.
Exact terms take precedence over rounded filed grants. Across current applications, exact awards are EUR 3,604,754, versus EUR 3,604,570 requested. Both amounts are retained; the funded-current difference is EUR 100.
Forecasts are expectations, not guarantees. Completion and late-response behaviour are transported from the pilot. A 20% change in future arrivals produces funded-payment scenarios of EUR 5,749,859 and EUR 7,154,320.
This is a snapshot workbook. Editing application cells alone does not refit static model outputs. Reappraisal of the closed list requires updating the analysis scope and source list.
Alternatives rejected.

Funding optimisation from its early performance: holding the first-seven-season average constant would produce EUR 99.05/t, but ignores the subsequent low saving levels. The age-profile calculation gives EUR 139.08/t.
Rejecting controls using the pilot’s overall mix: that calculation gives EUR 163.63/t. Current applicants have a different use mix; transporting the use-specific evidence gives EUR 94.58/t.
Simple before-and-after savings: these would confound works with weather, regression to the mean and calendar shocks. The randomized draw supplies the comparison.
Treating every disappearance of gas supply as a retrofit saving: terminal removal does not establish causation, so those disappearances receive no incremental credit.
Treating all requested grants as eventual expenditure: this ignores withdrawals and cost-selective noncompletion. Expected payments are therefore separated from award exposure.
Claiming certainty: optimisation’s 90% range includes qualifying values, and insulation fails under the stronger decay scenario. Neither limitation is hidden by the recommendation.
Files produced.

Haldenau_2026_Decision_Note.pdf: one-page, answer-first committee note with the decision, forecast, monitoring result and principal caveat.
Haldenau_2026_Grant_Appraisal.xlsx: 21-sheet supporting workbook containing the complete funded issue list, seasonal estimates, forecasts, uncertainty, sensitivities, validation, source register and embedded analysis code.
Packages installed. Provisioned NumPy, SciPy, pandas, statsmodels, openpyxl, python-docx, PyMuPDF and XlsxWriter, with their dependencies, because the active Python environment lacked the advertised analytics packages.
</pasted_content id="9977">

 looks like not stumped, try harder
