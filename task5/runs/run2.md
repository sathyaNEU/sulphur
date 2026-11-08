# task5 architecture 2, platform run 2

Pasted by the author on 2026-11-08 (target.zip 14f7ae29ebb94bc9). Score not reported; the author's word: not stumped.
The run filed the golden five and every register cell. The paste ends mid-sentence in the rejected alternatives.

---

Reviewed 127 resources
· 43m
Recommendation. Certify Tverrvika, Hesteby, Solmoen, Ørnevik and Fjordeid as qualifying for the 2027 vacant dwelling activation grant.

Their estimated vacancy shares meet the statutory 5.0% threshold after rounding to one decimal. Across the county, 396 of 8,020 counted dwellings are estimated vacant. Qualification uses the rounded share, not the confidence-interval endpoint.

Final answers. The municipal vacancy results are:

Municipality    Counted dwellings    Vacant dwellings    Vacancy share    Exact 90% interval    Qualifies
Brekkevoll    1,640    66    4.0%    3.3%-4.9%    No
Tverrvika    520    38    7.3%    5.5%-9.5%    Yes
Hesteby    980    63    6.4%    5.2%-7.9%    Yes
Kvernhaug    860    33    3.8%    2.8%-5.1%    No
Solmoen    430    28    6.5%    4.7%-8.8%    Yes
Ravnsund    740    34    4.6%    3.4%-6.1%    No
Ørnevik    380    31    8.2%    6.0%-10.9%    Yes
Langgrav    1,120    36    3.2%    2.4%-4.2%    No
Fjordeid    560    30    5.4%    3.9%-7.2%    Yes
Snøholt    790    37    4.7%    3.5%-6.1%    No
These results and the named qualifying municipalities appear in vacancy_grant_certification_2027.docx, in the opening certification table, and in county_dwelling_occupancy_2026-11.xlsx, on Municipality Summary.

The shares and intervals are charted against 5.0% in the letter's Municipal Vacancy Against the Threshold section and the workbook's Vacancy Chart sheet. Solmoen and Fjordeid qualify despite their intervals extending below the threshold.

The population-register comparison is:

Municipality    Register-zero share    Overcoverage dwellings    Overcoverage rate    Undercoverage dwellings    Undercoverage rate    Net bias
Brekkevoll    15.1%    15    1.1%    197    79.4%    +11.1%
Tverrvika    6.2%    13    2.7%    7    21.9%    -1.2%
Hesteby    8.5%    8    0.9%    28    33.7%    +2.0%
Kvernhaug    20.0%    7    1.0%    146    84.9%    +16.2%
Solmoen    6.3%    12    3.0%    11    40.7%    -0.2%
Ravnsund    8.2%    10    1.5%    37    60.7%    +3.6%
Ørnevik    5.3%    19    5.3%    8    40.0%    -2.9%
Langgrav    7.2%    10    1.0%    55    67.9%    +4.0%
Fjordeid    7.7%    10    1.9%    23    53.5%    +2.3%
Snøholt    8.5%    14    1.9%    44    65.7%    +3.8%
Overcoverage rates use dwellings with registered persons as their denominator. Undercoverage rates use dwellings without registered persons. Net bias is register-zero dwellings minus estimated-vacant dwellings, divided by all counted dwellings; positive values mean the register overstates vacancy.

These figures and their denominators appear in the letter's Coverage on 1 November 2026 section and the workbook's Municipality Summary sheet.

The workbook's Dwellings sheet contains exactly 8,020 unique dwelling rows, including municipality, reconstructed registered-person count and source person IDs on 1 November, and a Yes/No estimated-vacancy flag for the entire fortnight. It also provides meter IDs, classification evidence, missing-hour counts and register-comparison categories. The reconstructed register links 13,599 persons to counted dwellings.

Step-by-step process.

Inspected every member of the supplied archive. The workbook's Sources sheet records each file's role, record count and SHA-256 hash.
Input file    Contents and use
regulation_vacant_dwelling_grant_2027.pdf    Statutory dwelling population, vacancy definition and qualification rule
ministry_assignment_2026-12-01.eml    Exact binomial interval requirement and coverage-rate definitions
kommuner_hvitfjell_2026.csv    Municipality names and Snøholt's separate identity
matrikkel_bruksenheter_hvitfjell_2027-01-04.csv    Dwelling identities, types, addresses and taking-into-use dates
elhub_malepunkter_hvitfjell_2027-01-04.csv    Meter linkage, category and validity
elhub_timeverdier_2026-11-09_2026-11-22.parquet    Primary hourly electricity evidence
elhub_dognverdier_2026-11-09_2026-11-22.csv    Daily reconciliation check
nettselskap_avbrudd_2026-11.xlsx    Documented interruption windows
spotpriser_no1_2026-11.csv    Price-effect sensitivity check
folkeregister_bosatte_2027-01-05.csv    Terminal population-register snapshot
folkeregister_hendelser_2026-10-01_2027-01-05.csv    Events needed to reconstruct the November register
grunnbok_hjemmel_2027-01-05.csv    Legal title; inspected but not used because ownership is not an eligibility condition
grunnbok_overdragelser_2026.csv    Transfers; inspected but not used for the same reason
enhetsregisteret_utdrag_2027-01-05.csv    Organisations; inspected but not used
aksjonaerregisteret_2025.csv    Shareholders; inspected but not used
Established the statutory denominator. From 8,925 cadastre units, excluded 781 holiday homes, 10 other-type units, 63 Bolig units first used after the cutoff, and 51 Bolig units without a taking-into-use date. This left 8,020 counted dwellings. No cadastre records were deduplicated. Snøholt remained separate from Fjordeid.

Linked and cleaned meter evidence. All 8,173 household meter records linked to dwellings: 8,074 by dwelling ID and 99 by unique normalized address. The counted population uses 8,110 meters, including 90 replacements. Excluded 60 communal meters and meters serving later-use units. Corrected municipality assignment using cadastre identities where 806 meter records retained the old municipality code.

Resolved revisions and reference times. Kept the highest delivery number per meter-hour, replacing 6,215 estimated revisions. The 2,720,816 source rows became 2,714,601 unique measured observations. Excluding 20,122 communal readings and 4,001 noncounted-unit readings left 2,690,478 observations. UTC timestamps were converted to Europe/Oslo for the 336-hour reference fortnight. Replacement streams had no overlapping dwelling-hours.

Handled gaps and interruptions explicitly. Retained 4,242 missing dwelling-hours across 833 dwellings as missing, not zero. Each dwelling had 324-336 observed hours. For pattern fitting, excluded 10,992 observed hours within the documented municipality-level outage windows. A narrower, targeted outage treatment produced identical classifications. The daily export's 470 exact duplicates were removed for reconciliation; its 1,317 estimated daily totals for counted dwellings were scaled observed-hour totals, not independent occupancy evidence.

Estimated vacancy independently of registration. For each dwelling, fitted hourly consumption with day-specific levels and clock-hour effects. Classified residual RMS below 0.20 kWh per hourly observation as estimated vacancy. The observed boundary was 0.144856 for the largest vacant score versus 0.265886 for the smallest occupied score. This identified 326 smooth/zero profiles and 70 highly repeatable timed-load profiles, totaling 396. All selected dwellings also had daily residual RMS below 0.20 on all 14 days.

Reconstructed the historical register. Reversed 856 events registered after 1 November, concerning 826 people, while retaining 585 earlier events. This restored 105 people absent from January and removed 74 later entrants, producing 13,808 historical residents. Reversal followed validated address chains rather than blindly sorting registration dates. This also handled nine later-registered events already reflected in the nominal January extract.

Reconciled historical unit labels. Inferred coordinated renumbering in 20 buildings, supported by 359 events, and applied a 217-unit crosswalk. It recovered 105 otherwise unmatched people and corrected 254 misleading literal matches. Of the reconstructed residents, 13,599 linked to counted dwellings and 209 to excluded other-type units. There were no unmatched or ambiguous snapshot addresses after this reconciliation.

Calculated municipal estimates and register quality. Computed exact equal-tailed 90% Clopper-Pearson intervals from integer vacant and counted totals, then displayed percentages to one decimal. The register cross-tab reconciled to 7,068 registered/occupied, 118 registered/vacant, 556 unregistered/occupied, and 278 unregistered/vacant dwellings.

Validated calculations and artifacts. Thresholds of 0.15, 0.20 and 0.25 all returned 396 classifications. Cross-week prediction, adjacent-day differences, seven-day differences and leave-one-day-out checks supported the same classifications. Register-event replay reproduced the terminal extract with zero conflicts. An independent artifact review recomputed municipal totals, person-ID counts, intervals, rates and eligibility and found no discrepancies. Both files reopened successfully. Actual DOCX pagination could not be visually rendered; structural, table-width and embedded-chart checks passed.

The detailed transformations and checks are recorded in the workbook's Method, Validation, Unit Crosswalk and Sources sheets.

Assumptions and judgment calls.

Electricity patterns identify estimated, not verified, absence. Smooth or rigidly repeating loads were interpreted as unattended use. Regular occupants, brief activity and activity during missing hours can be missed. The exact binomial intervals do not include this classification uncertainty.
Timed loads are material to the decision. Treating all 70 timed-load candidates as occupied would reduce Hesteby to 4.6%, Solmoen to 4.7%, and Fjordeid to 4.5%, removing their qualification. The selected interpretation is supported by repeatability and temporal validation, but this remains an identifying assumption.
Undated units were excluded rather than imputed. The supplied data do not establish that the 51 undated Bolig units were in use by the statutory cutoff.
The renumbering crosswalk is inferred. Of its unit pairs, 197 are directly supported and 20 extrapolated from building-wide changes. Only one snapshot person uses an extrapolated pair. The literal-unit sensitivity affects register quality, not meter-based qualification.
The event history is assumed complete. The January extract was treated as the terminal state represented by the supplied events, including the endpoint inconsistency documented in the letter.
Coverage compares different dates by request. Actual moves between 1 November and the reference fortnight can contribute to register disagreement; the results do not isolate administrative error alone.
Alternatives rejected.

Register-zero equals vacancy: would qualify all ten municipalities. Brekkevoll would show 15.1%, rather than 4.0%, and Kvernhaug 20.0%, rather than 3.8%.
Low electricity consumption alone: below 5 kWh/day identifies only 120 dwellings, missing 276 selected profiles with heating or timed loads.
Any quiet day establishes vacancy: would count 1,182 dwellings, including 786 quiet only on some days. The legal definition concerns the entire fortnight.
Missing readings equal zero: changes the estimate to 388 dwellings. An absent reading does not establish zero consumption.
Ignore outages: changes the estimate to 392 dwellings, with four changes in Snøholt. Documented interruptions should not be interpreted as occupancy activity.
Use January registration unchanged: yields 894 register-zero dwellings, rather than 834, and changes registered-person presence for 100 dwellings.
Use literal historical unit labels: leaves 105 persons unmatched and changes registered-person presence for 80 dwellings.
Require the lower interval endpoint to exceed the threshold: would wrongly reject Solmoen and Fjordeid under the supplied regulation. Qualification
