# task7 architecture 5, platform run 1 (pasted by the author, 2026-11-08; the author has this one run only)

Recommendation. Carry EUR 2,000,000 of credit loss in Ardcarn Bank's 2027 plan.

The calculated estimate is EUR 2,039,924.22, rounded to the requested EUR 500,000 increment. Using register values without estimating the inspection value at default would produce only EUR 221,294 and would not match the model’s required valuation basis.

Final answers.

2027 plan credit loss: EUR 2,000,000. This covers facilities performing at 31 December 2026 that may default during 2027. The recommendation and calculation appear on slides 1-2 of exco_cre_credit_loss_2027.pptx.

Split by lending book, rounded to EUR 250,000:

Lending book	Facilities	Calculated loss	Plan allocation
Investment	1,447	EUR 1,274,669.30	EUR 1,250,000
Owner-occupied	813	EUR 765,254.92	EUR 750,000
These figures appear on slides 1-2.

Five facilities with the largest expected losses, rounded to the nearest euro:

Facility	Customer	Lending book	Expected 2027 loss
AB322222580	Fitzpatrick Properties Ltd	Investment	EUR 113,332
AB316705961	Barrett Hotel Ltd	Owner-occupied	EUR 56,180
AB321158994	Joyce Nursing Home Ltd	Owner-occupied	EUR 36,855
AB325355079	Power Healthcare DAC	Owner-occupied	EUR 36,636
AB322344238	Moran Estates Ltd	Investment	EUR 32,963
Slide 3 contains the ranking, PDs, balances and LGDs. Their combined rounded loss is EUR 275,966; their unrounded losses represent 13.5% of the model total.

Planning-system file: cre_expected_loss_2027_by_loan.csv contains all 2,260 performing facilities, including 1,422 with zero expected loss. The requested amount is in expected_loss_2027_eur, as an integer number of euros. The rounded loan amounts sum to EUR 2,039,933, which is EUR 8.78 above the unrounded model calculation. Slide 12 documents the schema and reconciliation.

Step-by-step process.

Inspected every file in input-assets/7.zip. The planning memorandum defined the population and scenario; the credit policy supplied PDs, default rules and security sharing; CRE-LGD-3 supplied the loss formula and haircut. The loan snapshots, facility register, security bridge, valuation history, index releases and default register supplied the calculation data. The property dimension supported coverage checks. Slides 13-14 identify every input and its treatment.

Reviewed the ancillary inputs without substituting them for required model inputs. The receiver-sales and recovery-postings files were not used to recalibrate the approved haircut. The insurance register measures replacement cover, the rent roll measures income, the outlook contains forecasts inconsistent with the required flat-price assumption, and the concentration report describes the preceding quarter rather than year-end.

Established the year-end perimeter. Removed 2,207 business-identical batch replays from 133,156 loan-month records. The December snapshot contained 2,335 unique facilities. Excluded 75 existing defaults, carrying EUR 52,537,782 of balances at displayed precision, and retained 2,260 performing facilities: 1,722 Stage 1 and 538 Stage 2. Their combined balance is EUR 1,839,089,693 at displayed precision. Four excluded defaults were labelled “Closed - sold” in the register but still had year-end balances.

Reconstructed valid valuation and security histories. Removed 95 exact valuation duplicates and 230 invalid validity intervals, each with a valid replacement. Normalised FULL to inspection and IDX to index roll-forward. Applied the legacy/current facility crosswalk and dated security links rather than relying on current-row flags. The active security population contained 2,453 links across 2,354 properties. Shared security was allocated using year-end balances, including defaulted exposures where they shared a property.

Built the historical inspection calibration sample. Reduced 883 default-event records to 841 first facility defaults. Usable inspection histories covered 833 facilities and 871 links. Removing 27 repeated shared-property/default observations left 844 distinct pairs. Five facilities had inconsistent post-default security/origination histories; two property links lacked an inspection loaded before default; two facilities lacked a post-default inspection. One missing-prior case retained other usable security, leaving eight facilities without a calibration pair overall.

Handled missing and unusual data explicitly. No performing facility required a missing-value imputation or exclusion. The property dimension contained 45 inferred records with missing descriptive fields; 43 were live security with complete valuation and index information and were retained. The unused sales file had 35 records missing selling costs and sale-agreed dates; the unused rent roll had 606 missing next-review dates. These fields were not imputed. Valid valuation outliers were retained.

Estimated inspection value conditional on default. Adjusted prior inspections for sector/region market movements using the latest index vintages available by 31 December 2026. Fitted a log-ratio model using inspection age and lending book, with book-specific smearing factors to estimate a mean rather than a median. The model uses positive security values and distinguishes inspection ageing from broad market movements. Its specification and coefficients appear on slide 11.

Applied the prescribed loss calculation. Used each facility’s year-end balance and master-scale twelve-month PD. Estimated security at 1 January 2027 with prices frozen at published 2026Q3 levels. Applied:

Expected loss = PD × max(0, EAD − 0.78 × allocated expected inspection value)

This preserves the approved 22% realisation haircut. Aggregated unrounded losses before rounding the plan and book allocations.

Validated the estimate. Training on 722 historical pairs and testing on 122 recent pairs produced an inspection-ratio RMSE of 8.45 percentage points, versus 11.11 points for a book-mean-only model. Aggregate held-out inspection value was predicted 0.15% below observed. A customer-cluster bootstrap with 1,000 resamples gave a 95% parameter-only interval of EUR 1.86m to EUR 2.23m.

Checked sensitivity and delivery integrity. The alternative estimates were EUR 2,027,200 using only earlier calibration years; EUR 2,046,766 excluding unpublished-quarter outcomes; EUR 2,058,786 using completed workouts; EUR 2,097,274 using age at default; EUR 1,989,491 using a Gamma log-link model; and EUR 1,946,346 using a linear ratio model. Every case rounds to EUR 2,000,000. Independent checks reconciled CSV coverage, PDs, balances, security allocation, loss calculations, zero preservation and the top five. The PPTX reopened successfully, passed archive-integrity checks and was inspected through generated layout previews; it was not rendered in PowerPoint itself.

Assumptions and judgment calls.

Default timing and market scenario: Used 1 January 2027 and flat published prices, as explicitly required. The latest index quarter is 2026Q3; the latest release date is 14 November 2026.
Inspection timing: The first post-default inspection proxies the default-triggered inspection. Observed delays were 4-87 days, with a median of 46 days. Changing the age definition did not change the rounded recommendation.
Unpublished-quarter treatment: Held Q4 2026 prices at Q3 levels for 19 historical pairs and 50 live properties across 52 links. Excluding the affected historical outcomes preserved the recommendation.
Transport to older collateral: Live inspections are older than historical calibration inspections. Only 22 historical properties were over ten years old, versus 110 live links. This limits precision in the oldest tail.
Uncertainty: The bootstrap interval measures calibration-parameter uncertainty, not the range of realised annual credit losses. The recommended amount is a central planning estimate, not a stress allowance.
Alternatives rejected.

Use register values directly: Rejected because the resulting EUR 221,294 loss uses the wrong valuation basis. Historical default inspections show material differences from market-indexed prior inspections.
Use a book average without inspection age: Rejected because held-out RMSE increased from 8.45 to 11.11 percentage points.
Replace or increase the recovery haircut: Rejected. The approved back-test reports annual errors no larger than 0.9 percentage points against a 3-point limit. Adding sale-delay discounting would also duplicate an effect already absorbed by the haircut.
Use the supplied market outlook, insurance or rental data as collateral values: Rejected because these do not represent the prescribed flat-price inspection value.
Treat model precision as certainty: Rejected. Held-out ratio bias was -1.10 points for investment and +2.70 points for owner-occupied lending, and older inspections have thinner support. These limitations are disclosed, but the tested alternatives preserve the rounded plan.
Files produced.

exco_cre_credit_loss_2027.pptx: 14-slide executive deck with the recommendation, lending-book split, top five facilities, validation, assumptions and technical audit trail.
cre_expected_loss_2027_by_loan.csv: Complete facility-level planning file with expected losses and supporting calculation fields.
Both files are saved under /home/agent/workspace. Temporary analysis scripts and workspace previews were removed.

Packages installed. Installed pandas, numpy, scipy, statsmodels, openpyxl, python-pptx, PyMuPDF and matplotlib, plus dependencies, because they were unavailable in the active interpreter.
