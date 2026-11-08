# task5 architecture 2, platform run 1

Pasted by the author on 2026-11-08 (target.zip 14f7ae29ebb94bc9). Score not reported; the author's word: not stumped.
The run filed the golden five and every register cell.

---

Reviewed 130 resources
· 45m
Recommendation. Certify Tverrvika, Hesteby, Solmoen, Ørnevik and Fjordeid as qualifying for the 2027 vacant dwelling activation grant.

Their certified vacancy shares are 7.3%, 6.4%, 6.5%, 8.2% and 5.4%, respectively, meeting the 5.0% threshold applied after rounding to one decimal. Qualification does not depend on the lower confidence limit exceeding the threshold.

Final answers. The municipal vacancy estimates for 9-22 November 2026 are:

Brekkevoll: 66 of 1,640 counted dwellings vacant; 4.0%, with a 90% interval of 3.3%-4.9%. Does not qualify.
Tverrvika: 38 of 520 vacant; 7.3%, interval 5.5%-9.5%. Qualifies.
Hesteby: 63 of 980 vacant; 6.4%, interval 5.2%-7.9%. Qualifies.
Kvernhaug: 33 of 860 vacant; 3.8%, interval 2.8%-5.1%. Does not qualify.
Solmoen: 28 of 430 vacant; 6.5%, interval 4.7%-8.8%. Qualifies.
Ravnsund: 34 of 740 vacant; 4.6%, interval 3.4%-6.1%. Does not qualify.
Ørnevik: 31 of 380 vacant; 8.2%, interval 6.0%-10.9%. Qualifies.
Langgrav: 36 of 1,120 vacant; 3.2%, interval 2.4%-4.2%. Does not qualify.
Fjordeid: 30 of 560 vacant; 5.4%, interval 3.9%-7.2%. Qualifies.
Snøholt: 37 of 790 vacant; 4.7%, interval 3.5%-6.1%. Does not qualify.
These figures and qualifying names appear in the opening certification table of vacancy_grant_certification_2027.docx and the Municipalities sheet of county_dwelling_occupancy_2026-11.xlsx. The county total is 396 vacant dwellings among 8,020 counted dwellings.

The requested chart is embedded in the letter's "Vacancy Against the Threshold" section and below the workbook's municipal summary. It shows every share, its exact 90% binomial interval and the 5.0% threshold.

The population-register comparison for 1 November 2026 is:

Brekkevoll: overcoverage 15 dwellings, 1.1%; undercoverage 197 dwellings, 79.4%; net vacancy bias +11.1%.
Tverrvika: overcoverage 13 dwellings, 2.7%; undercoverage 7 dwellings, 21.9%; net bias -1.2%.
Hesteby: overcoverage 8 dwellings, 0.9%; undercoverage 28 dwellings, 33.7%; net bias +2.0%.
Kvernhaug: overcoverage 7 dwellings, 1.0%; undercoverage 146 dwellings, 84.9%; net bias +16.2%.
Solmoen: overcoverage 12 dwellings, 3.0%; undercoverage 11 dwellings, 40.7%; net bias -0.2%.
Ravnsund: overcoverage 10 dwellings, 1.5%; undercoverage 37 dwellings, 60.7%; net bias +3.6%.
Ørnevik: overcoverage 19 dwellings, 5.3%; undercoverage 8 dwellings, 40.0%; net bias -2.9%.
Langgrav: overcoverage 10 dwellings, 1.0%; undercoverage 55 dwellings, 67.9%; net bias +4.0%.
Fjordeid: overcoverage 10 dwellings, 1.9%; undercoverage 23 dwellings, 53.5%; net bias +2.3%.
Snøholt: overcoverage 14 dwellings, 1.9%; undercoverage 44 dwellings, 65.7%; net bias +3.8%.
Overcoverage rates use counted dwellings holding registered persons as the denominator. Undercoverage rates use counted dwellings holding nobody. Net bias is register-empty dwellings minus estimated vacant dwellings, divided by all counted dwellings; positive values mean the register overstates vacancy. These results and their denominators appear in the letter's "Population Register Comparison" section and the workbook's Municipalities sheet.

The workbook's Dwellings sheet contains exactly 8,020 rows, one per counted dwelling, including:

Stable dwelling ID, municipality and address.
registered_persons_2026_11_01 and the supplied pseudonymous IDs in registered_person_ids.
The Boolean vacant_reference_fortnight and readable electricity-based status.
Meter IDs, observed and missing hours, activity score and register-comparison category.
The qualifying municipalities contain 190 vacant dwellings, giving a formula grant total of NOK 7,600,000. The letter and municipal summary also record the individual grant amounts.

Step-by-step process.

Read all archive members and establish the rules. The regulation defines counted dwellings, electricity-based vacancy and the rounded-share eligibility test. The ministry email specifies exact 90% binomial intervals and the coverage-rate denominators. The municipality file establishes the geography, including Snøholt's separation from Fjordeid. Every archive member and its use is recorded in the workbook's Sources sheet.

Construct the counted population. The cadastre contains 8,925 units. I excluded 781 holiday homes, 10 other-type units, 63 dwellings taken into use after 1 November, and 51 dwellings with missing taking-into-use dates. This leaves 8,020 counted dwellings. Cadastre dwelling IDs are unique; no exact duplicate rows required removal.

Reconstruct the November population register. The January resident snapshot contains 13,777 people, and the event file contains 1,441 records. I reversed 856 later-recorded events affecting 826 people, using validated person-address chains. The population reconciliation is 13,777 - 33 births - 41 immigrations + 30 deaths + 20 emigrations + 55 domestic departures = 13,808 people. Of these, 13,599 belong to counted dwellings and 209 to excluded institutional units.

Resolve historical address changes and inconsistent extract dates. Simultaneous unit-number changes identify 20 renumbered buildings. Their crosswalk reassigns 359 people, resolves 105 otherwise unmatched people, and corrects 254 literal address matches that would refer to the wrong current unit. One person requires an inferred mapping. I also reversed nine events recorded after the nominal snapshot date because their effects are already present in the snapshot. All reconstructed people match unambiguously, and forward replay reproduces the supplied snapshot.

Link meters without merging municipalities or common-area loads. The meter file contains 8,233 meters, including 60 common-area meters, which are excluded from individual-dwelling classification. Stable dwelling IDs take precedence over address labels. 99 household meters lacking dwelling IDs are recovered through unique municipality/address matches. Cadastre geography corrects 806 household-meter municipality labels overall, including 802 serving counted dwellings. Stitching 90 replacement pairs produces 8,110 household meters serving the 8,020 counted dwellings.

Clean and reconcile the electricity records. The hourly file contains 2,720,816 readings. Keeping the latest delivery removes 6,215 superseded readings, leaving 2,714,601 unique measured readings. None is negative or nonfinite. UTC timestamps are converted to Europe/Oslo for the 336-hour reference fortnight. Counted dwellings contribute 2,690,478 observed hours, with 4,242 missing hours. The daily file contains 113,758 rows; removing 470 exact duplicates leaves 113,288 meter-days, whose counts and totals reconcile to the hourly records. Its 1,335 estimated daily totals extrapolate observed consumption and are not treated as evidence of activity during missing hours.

Estimate occupancy from hourly patterns. For each dwelling, I subtract the daily overnight baseline and then the recurring local-hour pattern. A positive residual above 0.75 kWh on any day establishes an occupied estimate. Otherwise, a dwelling is estimated vacant only after passing the coverage gate: all reference days represented and at least 324 observed hours. All counted dwellings pass. There are 7,187 complete profiles and 833 with 324-335 hours. The resulting classifications are 7,624 occupied and 396 vacant.

Calculate municipal estimates and register quality. The largest vacant-profile activity score is 0.5920 kWh, while the smallest occupied-profile score is 1.3445 kWh. The vacant estimates comprise 27 all-zero profiles, 299 smooth heating/standby profiles, and 70 repeated heating schedules. Municipal shares use all counted dwellings as their denominator. Exact equal-tailed Clopper-Pearson intervals follow the ministry's binomial specification. Register comparisons identify 118 overcoverage dwellings and 556 undercoverage dwellings.

Test the deciding assumptions. Activity thresholds from 0.60-1.30 kWh, alternative baseline definitions, masking the logged outage windows, and excluding measured zeros from feature estimation each produce zero classification changes. Effective-date rather than recording-date register reconstruction produces identical assignments. The workbook retains additional missing-hour and missing-date sensitivity scenarios.

Validate the deliverables. An independent computational review reproduced the classifications and register reconstruction, recalculated the intervals, and reconciled every saved dwelling field and municipal aggregate. Both Office files reopen and pass package-integrity checks. Temporary analysis files were removed. Actual Word pagination was not visually rendered because no Word/LibreOffice renderer was available.

The other inputs were examined but not used as eligibility restrictions: the title register contains 5,119 rows, transfers 273 rows, shareholders 118 rows, and company entities 292 rows. Ownership and corporate control are not conditions in the regulation. The 336 hourly prices were examined as a possible explanation of regular electricity patterns; prices do not independently identify habitation. The outage workbook supplies three outage records, used in the sensitivity test.

Assumptions and judgment calls.

Electricity indicates occupancy, rather than proving it. The residual rule separates the supplied profiles clearly, but no independently observed occupancy labels are available. The intervals therefore do not incorporate classifier error or guarantee that no unobserved habitation occurred.
Missing hours can conceal activity. Forty vacant estimates have incomplete readings. If every one were occupied during a gap, Fjordeid would fall from 30 vacant dwellings, 5.4%, to 27, 4.8%, and would no longer qualify. This adverse scenario is disclosed, not substituted for the primary estimate.
The January cadastre represents the relevant historical stock. No demolition or historical unit-type ledger is supplied. Missing commissioning dates do not establish eligibility. If those excluded units were subsequently proved eligible and vacant, Ravnsund and Snøholt could reach 5.2% and 5.5%, respectively.
Register histories are interpreted according to their actual contents. The postdated events are reversed because the snapshot reflects them. Recording-date and effective-date reconstructions agree at the requested cutoff.
One address alias is inferred. Omitting its person would change Solmoen's undercoverage from 11 dwellings, 40.7%, to 12, 42.9%, and net bias from -0.2% to 0.0%. Vacancy and qualification would not change.
Coverage discrepancies are not exclusively register errors. Register residence is measured on 1 November, while physical occupancy refers to 9-22 November; genuine changes between those dates can contribute.
Eligibility follows the rounded point estimate. The confidence interval is supporting evidence, not an additional statutory hurdle.
Alternatives rejected.

Zero registered persons as vacancy: this would identify 834 dwellings, rather than 396. Of those register-empty dwellings, 556 show occupancy activity, while 118 vacant dwellings hold registered persons.
A total-consumption cutoff: a 100 kWh rule would identify 134 vacant dwellings, misclassifying 3 irregular-activity profiles as vacant and 265 no-activity profiles as occupied. An occupied profile consumes 91.138 kWh, while a repeated-heating vacant profile consumes 1,727.575 kWh.
The January snapshot without reconstruction: it gives 7,126 counted dwellings with registered persons, rather than 7,186, and changes 681 dwelling-level person counts.
Literal historical addresses: they leave 105 people unmatched and overlook overlapping old and current unit labels.
Requiring the lower confidence limit to exceed 5.0%: this would wrongly reject Solmoen and Fjordeid under the supplied regulation.
Outages as the explanation for the vacancy results: removing all logged outage hours across the affected municipalities changes zero classifications.
Ownership-based exclusions: the regulation contains no such eligibility condition.
Files produced.

vacancy_grant_certification_2027.docx: Certification decision, municipal estimates and exact intervals, threshold chart, register-quality comparison, methods, grant amounts and sensitivity disclosures.
county_dwelling_occupancy_2026-11.xlsx: All counted dwellings with registered-person counts and IDs, vacancy estimates, municipal summaries, meter links, address aliases, methods, audit checks, sensitivities and source inventory.
Packages installed. Installed in a temporary environment: pandas, numpy, scipy, scikit-learn, matplotlib, openpyxl, python-docx, PyMuPDF and pyarrow, with their dependencies.
