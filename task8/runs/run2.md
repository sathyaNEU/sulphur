Response 2

Reviewed 90 resources
· 27m
Recommendation. Set Paper C for the November 2027 Year 10 science sitting.

Its expected Achieved mark rounds to 25 out of 50. Comparing before rounding, Paper C is 0.125497 marks from the target of 25, closer than Paper A at 0.947709 or Paper B at 1.859400.

Final Answers.

Paper selection: Paper C. The recommendation appears in council_memo.docx, under "Recommendation", and in paper_choice.xlsx, on Decision.
Expected Achieved marks: Paper A 26, Paper B 23, Paper C 25, all out of 50 and rounded to whole marks. achieved_marks.png charts all three against 25. The workbook's Decision and Draft Items sheets retain full-precision calculations.
Capital: 1,035 entered; 986 sat online; 27 sat make-up; 1,013 sat either mode; mean make-up mark 23.8/50.
Central: 1,213 entered; 1,151 sat online; 37 sat make-up; 1,188 sat either mode; mean make-up mark 25.8/50.
Northern: 1,915 entered; 1,813 sat online; 61 sat make-up; 1,874 sat either mode; mean make-up mark 28.4/50.
Southern: 1,289 entered; 1,216 sat online; 45 sat make-up; 1,261 sat either mode; mean make-up mark 25.3/50.
Trust total: 5,452 entered; 5,166 sat online; 170 sat make-up; 5,336 sat either mode; mean make-up mark 26.3/50.
All regional figures appear in paper_choice.xlsx, on Regions, and in the memo's "August 2026 annual-report figures" section. There is no overlap between online and make-up candidates; 116 entered candidates did not sit.

Step-by-Step Process.

Established the governing rule and November context. Read paper_choice_request.eml, y10sci_paper_specification_2027.pdf, standard_setting_record_y10sci.pdf, council_minute_2026_10_14.pdf, and y10sci_course_review_2026.pdf. The specification requires the draft whose unrounded Rasch expectation is closest to 25. Achieved remains 0.35 bank logits. The approved November window is 1-12 November 2027. The course review places all six core units before November and supplies school-specific teaching sequences.

Resolved every draft item. Joined y10sci_2027_drafts.xlsx through item_renumbering_2025.csv to corlinn_item_bank_2026.xlsx. All 150 draft positions resolved uniquely to 96 distinct active items. None used the 18 retired cards. Each draft contains 50 one-mark items, covers all six units, and meets the strand limits. Audited bank_calibration_runs.csv: its 140 final-2026 records agree with the supplied bank; the preliminary run is superseded, and the 86-item 2025 run is incomplete for the current bank.

Built the candidate population. Read entries_register_aug2026.xlsx and member_schools.csv. From 5,682 register rows, removed 96 exact duplicates, excluded 114 withdrawals, and linked 20 corroborated duplicate registrations, leaving 5,452 candidates. All school codes resolve to the membership register. The 87 office records without NSNs were retained or linked, not discarded.

Reconciled online sessions and responses. Read y10sci_aug2026_sessions.csv and y10sci_aug2026_responses.csv. The 5,323 sessions comprise 5,166 submitted sessions and 157 dropped sessions, each followed by a submission. Combined work across restarts and retained the latest response on 331 repeated candidate-item pairs, including 137 score disagreements. This reduced 258,631 response rows to 258,300, exactly 50 items per online candidate. No response needed exclusion for a missing identifier, missing score, or non-binary score.

Matched responses to completed teaching. Converted session timestamps from UTC to Pacific/Auckland before comparing them with school schedules. All U1-U4 responses were eligible because those units were taught in Terms 1-2. For U5-U6, retained responses only after the relevant unit was completed. The resulting calibration population contained 221,180 responses: 216,972 from U1-U4, 1,628 from U5 and 2,580 from U6. Excluded 37,120 unfinished-unit responses from calibration only, not from participation counts. Completed-unit evidence covered 407 U5 candidates from 14 schools and 645 U6 candidates from 17 schools.

Estimated November-relevant item difficulties. Held the 20 common anchor difficulties fixed on the existing bank scale. Estimated the other 120 item difficulties using conditional Rasch likelihood, conditioning on the anchor score plus the target-item score so candidate ability cancels from the item fit. Of 117,860 eligible non-anchor responses, 739 had uninformative extreme conditional totals, leaving 117,121 informative responses. Summed each draft's item probabilities at 0.35 logits, then ranked distances from 25 before rounding.

Reconstructed make-up participation and marks. Read all pages of makeup_roster_aug2026.pdf and all rows of makeup_scripts_keyed.csv. The roster contains 180 bookings, including 156 attendees and 24 non-attendees. Recovered 109 missing keyed entry IDs using unique script numbers and retained 14 valid keyed scripts absent from the roster, giving 170 make-up candidates. Assigned regions through home schools rather than hosts; 40 scripts cross host/home region boundaries.

Corrected the make-up unit inconsistency. Batch K047 contains 13 even values from 20 to 80, including four above the 50-mark maximum. Because script covers carry both marks and percentages and each batch uses one template, converted the entire batch by dividing by two. Its sum changes from 616 to 308. All corrected marks fall within the permitted range, and the make-up mark total is 4,468. Regional means divide corrected mark sums by unique make-up candidates.

Reviewed unused evidence. Inspected candidate_survey_2026.csv, containing 3,649 responses, but did not use it: question meanings were not supplied, and survey completion is not evidence of sitting or unit mastery. Inspected member_bell_times_2026.json, covering 48 schools, but did not infer teaching exposure from bell periods because they do not identify subjects or lessons. The workbook's Sources sheet documents all supplied files and their treatment.

Validated the result and deliverables. Paper C remains closest when retaining the supplied U1-U4 difficulties, changing the interpretation of Tuesday-start school weeks, or retaining the first repeated response instead of the latest. It also remains closest in 48 of 48 leave-one-school-out fits and 990 of 1,000 school bootstrap fits. An independent root solver agrees with the workbook iterations within 1e-9 logits. Executed the workbook's embedded Reproduce working using only the workbook; it reproduced the selection and every regional result. Checked formula caches, file integrity, embedded graphics, and the memo's rendered three-page layout.

Assumptions and Judgment Calls.

November teaching exposure: Treated November candidates as having completed the six core units, supported by the course outline and unchanged core curriculum. Actual lesson attendance and November responses are unavailable. A failure to complete the course could change the appropriate calibration.
School-week interpretation: Used explicit dates where supplied; otherwise counted whole weeks from each school's stated term start. A Monday-aligned alternative leaves Paper C selected.
Identity linkage: The 20 office/upload links match full name, birth date and gender, with later office registration and sitting activity only under the office ID. They are inferential, not NSN-confirmed transfers. Without these links, entered counts would be Capital 1,040; Central 1,217; Northern 1,918; Southern 1,297; total 5,472. Sitting counts, make-up means and the paper recommendation would not change.
Make-up evidence: Accepted a valid keyed script as participation evidence even when absent from the booking roster. No date was invented for those omitted records.
K047 units: Whole-batch percentage conversion is inferred from the documented cover format and values; original covers were not supplied. This affects reported make-up means, not paper selection.
Transport uncertainty: The analysis assumes stable anchor/item behaviour and comparable teaching in 2027. School resampling measures sampling stability, not uncertainty in those assumptions.
Alternatives Rejected.

Selecting A directly from the pooled August bank: That calculation gives rounded expectations of 25 for A, 21 for B and 22 for C, but mixes completed and unfinished teaching. Using the same conditional estimator without the completion restriction also selects A. The evidence therefore points to teaching exposure, rather than an arbitrary estimator change, as the reason the November ranking differs.
Selecting B under the completed-unit analysis: Its distance from 25 is 1.859400, versus 0.125497 for C.
Treating the recommendation as certain: 10 of 1,000 school bootstrap fits select A. This is evidence against absolute certainty, but C wins the other 990 and every leave-one-school-out check.
Counting sessions or bookings as candidates: Restarts would duplicate online candidates, while roster-only counting would omit 14 validated make-up scripts.
Using host regions: This would misclassify 40 make-up candidates across regions and incorrectly leave Capital with no make-up candidates.
Correcting only K047 values above 50: That leaves mixed units within the batch. It produces an overall mean of 27.3, compared with the adopted 26.3; leaving the batch unchanged produces 28.1.
Files Produced.

council_memo.docx: Council recommendation, supporting evidence, limitations, and regional annual-report figures.
achieved_marks.png: Each draft's expected Achieved mark against the target of 25.
paper_choice.xlsx: Formula-based calibration, regional statistics, source and linkage audits, sensitivity results, exact bootstrap weights, and executable workbook-only reproduction working.
All three are saved under /home/agent/workspace. Temporary analysis scripts and preview images were removed.

Packages Installed. Installed temporary tooling for numpy, pandas, scipy, openpyxl, python-docx, matplotlib, PyMuPDF, Pillow, XlsxWriter, and Aspose.Words, with their dependencies. Python 3.13 and libssl1.1 were also added for document-render validation.
