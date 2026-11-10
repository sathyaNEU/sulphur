Response 1
Reviewed 70 resources· 16m
Recommendation. Commit to reinforce Ashcombe Road only for winter 2027/28. At the prescribed -3.0 C design condition, its demand after flexibility is 23.70 MW against 23.00 MW firm capacity, leaving a 0.70 MW shortfall. Commit in December 2026 for energisation by 31 October 2027.
Final answers. The zone-by-zone design-day results are:

* Ashcombe Road CMZ: before flexibility 30.05 MW; credited flexibility 6.35 MW; after flexibility 23.70 MW against 23.00 MW firm. Reinforce: 0.70 MW over firm.
* Charlecote Way CMZ: before flexibility 25.08 MW; credited flexibility 3.95 MW; after flexibility 21.14 MW against 22.50 MW firm. Do not commit capacity reinforcement: 1.36 MW headroom.
* Fenwick Street CMZ: before flexibility 36.03 MW; credited flexibility 10.48 MW; after flexibility 25.55 MW against 30.50 MW firm. Do not commit capacity reinforcement: 4.95 MW headroom.
* Hartwell Common CMZ: before flexibility 22.95 MW; credited flexibility 5.48 MW; after flexibility 17.47 MW against 17.80 MW firm. Do not commit capacity reinforcement: 0.33 MW headroom.

These results appear in `Halverton_Winter_2027-28_Capacity.xlsx`, sheet `Decision`, and slides 1-3 of `Halverton_Capex_Review_2027-28.pptx`. Calculations use unrounded estimates; displayed components can differ slightly through rounding.
On a working weekday with a daily mean of -6.0 C, with flexibility adjusted for its weaker cold-weather response:

* Ashcombe Road: 5.30 MW credited; net demand 26.56 MW, exceeding firm by 3.56 MW.
* Charlecote Way: 3.16 MW credited; net demand 23.00 MW, exceeding firm by 0.50 MW.
* Fenwick Street: 9.21 MW credited; net demand 28.82 MW, remaining 1.68 MW below firm.
* Hartwell Common: 4.65 MW credited; net demand 19.90 MW, exceeding firm by 2.10 MW.

Therefore, Ashcombe Road, Charlecote Way and Hartwell Common breach firm at -6.0 C; Fenwick Street does not. These results appear in `Cold Stress` and slide 4. The cold case is an operational stress test, not the guideline’s automatic reinforcement trigger.
The spreadsheet includes native before-and-after charts against each primary’s firm capacity on `Decision` and `Cold Stress`. The six-slide deck covers the commitment decision, design-day comparison, flexibility credits, cold stress, uncertainty and source audit.
Step-by-step process.

1. Reviewed all supplied inputs. The archive `t10.1.zip` contained 11 files. The capacity guideline established the decision rule and firm capacities; the award notice supplied future contracted MW. The SCADA, weather and dispatch files supplied historical observations. The primary register supplied asset mappings and DFES growth; the connection and feeder registers supplied incremental demand and its primary allocation. I also reviewed the interruption workbook, transformer-condition workbook and DUoS statement, but did not use them to replace the prescribed capacity test. Their contents and treatment are recorded in `Sources`.
2. Resolved SCADA identity and quality. Mapped 18 historic/current point names to nine primary assets, with no unmatched names. Removed 441 exact duplicates from 196,201 rows, leaving 195,760. Rejected 931 S-quality and 31 B-quality readings, retaining 194,798 good readings. There were 368 absent nominal half-hour records. The resulting 4,086 primary-day summaries included 3,769 days with all 48 readings good. Midnight-ending intervals were assigned to the preceding service day. No readings were interpolated or winsorised. These reconciliations are in `Data QA`.
3. Resolved weather revisions and completeness. Removed 310 older versions from 13,372 records, retaining 13,062 hourly readings. Of 547 GMT days, 488 were complete; 52 had 23 readings and 7 had 22. Incomplete-day temperatures were excluded rather than interpolated. 50 incomplete weather days fell within the demand winters. The daily evidence is in `Weather Daily`.
4. Resolved dispatch revisions before assigning treatment. The 372 ledger rows became 336 final instructions after removing 36 superseded versions: 321 completed and 15 cancelled. Final completed scheduled MW defined the treatment dose; cancelled instructions received zero dose. Joins used primary asset and service date, avoiding provider-name spelling inconsistencies. Every instruction day, including a subsequently cancelled instruction, was excluded from the baseline demand fit. The full ledger remains in `Event Audit`.
5. Constructed the eligible modelling populations. Winter was defined as November-March. Working days excluded weekends, 24 December-2 January, and relevant England bank holidays. For the baseline, each zone began with 151 days, reduced to 99 eligible working days. In Ashcombe, Charlecote, Fenwick and Hartwell order, excluding instruction days left 48, 68, 54 and 53 days; requiring 48 good SCADA readings left 47, 64, 51 and 49; requiring complete weather left 38, 52, 43 and 41 baseline days. The flexibility models used 260, 258, 255 and 258 days, including 80, 51, 69 and 80 completed-dispatch days. These sequential funnels are in `Data QA`; individual inclusion flags are in `Daily Data`.
6. Estimated demand and applied growth correctly. Fitted each primary’s non-dispatch daily maximum against daily mean temperature, then evaluated it at -3.0 C. The 2025/26 baseline estimates were 26.56, 23.66, 33.87 and 20.91 MW. Compounded the two annual DFES growth rates, then added eligible connections in full. The 58 connection-register rows yielded 28 eligible records, comprising 20 Accepted and 8 Energised records. Exclusions were 2 superseded, 8 withdrawn, 3 quoted/unaccepted, 14 before the date window and 3 after it. Five legacy feeder identifiers were resolved, with no unmatched connections. Eligible additions totalled 10.17 MW across all primaries and 5.13 MW in the awarded zones: 2.30, 0.71, 0.93 and 1.19 MW, respectively. See `Connections` and `Demand Model`.
7. Estimated primary-meter flexibility rather than nominal availability. Used the mean SCADA demand in the half-hours ending 17:30 and 18:00, with zone-specific regression controls for temperature, winter and weekday, plus scheduled MW and its interaction with temperature. Estimated design-condition reductions per scheduled MW were 0.6684, 0.4932, 0.7485 and 0.7301. Applying these to awards of 9.50, 8.00, 14.00 and 7.50 MW produced the credits reported above. The interaction also reduces credited delivery in the -6.0 C case. Equations, coefficients and calculation bridges are in `Read Me`, `Model Coefficients` and `Flexibility`.
8. Tested uncertainty and alternative specifications. Jointly refitted demand and flexibility using 2,000 moving-block bootstrap replications per block length. With five-working-day blocks, the 95% intervals for design-day net demand minus firm were +0.23 to +1.07 MW for Ashcombe, -1.63 to -1.09 MW for Charlecote, -5.40 to -4.54 MW for Fenwick and -0.59 to -0.09 MW for Hartwell. Ten-day blocks preserved all decision signs. Quadratic weather, winter-specific weather slopes, pre-window load controls, contemporaneous control primaries, separate target half-hours and alternative completeness/cancellation rules all retained the same commitment list. Details are in `Validation`.
9. Checked prediction and deliverable integrity. In the held-out 2025/26 winter, temperature-dependent models had lower RMSE than constant-effectiveness models in every zone: 0.33 versus 0.51 MW, 0.15 versus 0.28 MW, 0.30 versus 0.44 MW, and 0.15 versus 0.24 MW. Verified the workbook’s 14 sheets, 96 formulas and two charts, reconciled cached calculation results, and reproduced all eight main regressions from the embedded workbook data alone. The six-slide deck passed package-integrity, slide-boundary and estimated text-fit checks. Native PowerPoint rendering was unavailable; that limitation is disclosed in `Data QA`.

Assumptions and judgment calls.

* Cold-weather extrapolation is necessary. Eligible baseline samples begin at +3.34, +2.75, +2.88 and +2.88 C. Both forecast conditions are outside those baseline samples. Alternative weather specifications retain the recommendation, but cannot rule out unknown nonlinear cold-weather behaviour.
* Future delivery scales with scheduled MW. Awards are 1.46x, 1.78x, 2.15x and 2.50x the largest historical doses. Applying the estimated rate to those awards follows the guideline, but does not prove delivery at the expanded portfolio size.
* Hartwell needs particular oversight. Its 0.33 MW headroom is small. It needs 5.15 MW of design-day credit to hold firm, against the 5.48 MW estimate. Weaker expanded-portfolio delivery could change its deferral decision.
* Connection design demand is held fixed in the cold case. No connection-specific temperature response was supplied. Additional cold-sensitive demand could worsen the stress result.
* The two target half-hours are averaged, not summed. Separate half-hour estimates retain the same commitment decision. This policy calculation is not a full simulation of rebound or a shifted residual daily peak.
* Uncertainty intervals are model-conditional. Dispatch was selected on forecast load, not randomised. The estimates and intervals are planning evidence, not guaranteed minimum delivery or operational reliability bounds.

Alternatives rejected.

* Reinforce all four because gross demand exceeds firm: rejected because the mandated flexibility credits bring Charlecote, Fenwick and Hartwell below firm.
* Defer Ashcombe using temperature-independent flexibility: rejected. That model gives Ashcombe 1.44 MW of apparent headroom, but performs worse in held-out winters and ignores the observed cold-weather reduction in effectiveness.
* Credit contracted MW one-for-one, or use settlement energy: rejected because the guideline requires primary-demand reduction per scheduled MW in the specified half-hours.
* Use -6.0 C as the commitment threshold: rejected because the governing design condition is -3.0 C. The additional cold-case breaches instead support contingency planning.
* Substitute transformer condition, interruption history, tariff bands or open feeder ties for the capacity rule: rejected because none establishes a different applicable firm-MW limit or primary-meter flexibility credit.

The principal caution against straightforward deferral is Hartwell’s narrow margin and substantial contract expansion. Those risks warrant delivery validation and re-review, but do not overturn the prescribed point-estimate decision.
Files produced.

* `Halverton_Winter_2027-28_Capacity.xlsx`: decision spreadsheet with before-and-after charts, cold stress, formula-linked calculations, model-ready data, source audits and validation.
* `Halverton_Capex_Review_2027-28.pptx`: six-slide capex-review deck with supporting speaker notes.

Both files are saved under `/home/agent/workspace`. Temporary analysis scripts were removed.
Packages installed. Installed in an isolated temporary environment: `numpy`, `pandas`, `scipy`, `statsmodels`, `openpyxl`, `xlsxwriter`, `python-pptx`, `matplotlib`, `Pillow` and `PyMuPDF`, plus dependencies. The supplied interpreter did not contain the stated analytical libraries.
