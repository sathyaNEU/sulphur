Response 1

Reviewed 126 resources
· 40m
Recommendation. Set Paper C for the November 2027 Year 10 Science Benchmark.

Its expected Achieved mark is 25 out of 50, with a gap from the target of 0.123233 marks, compared with 0.965538 for Paper A and 2.013199 for Paper B. Selection uses expected marks before rounding.

Final answers. The Council recommendation is in council_memo.docx, under Recommendation. The comparison appears in achieved_marks.png and in the workbook's Decision and Draft Items sheets.

Draft	Expected Achieved Mark /50	Gap From 25, Calculated Before Rounding	Decision
Paper A	26	0.965538	Do not set
Paper B	23	2.013199	Do not set
Paper C	25	0.123233	Set
These are November projections that allow for scheduled completion of the core course, while retaining the Achieved standard at 0.35 logits.

The requested regional figures are in paper_choice.xlsx, Regions, and in the memo's August 2026 Annual-Report Figures section. Regions refer to candidates' home schools.

Region	Entered Candidates	Sat Online or Make-up	Sat Online	Sat Make-up	Mean Make-up Mark /50
Capital	1,035	1,013	986	27	23.8
Central	1,213	1,188	1,151	37	25.8
Northern	1,915	1,874	1,813	61	28.4
Southern	1,289	1,261	1,216	45	25.3
Total	5,452	5,336	5,166	170	26.3
There is zero overlap between online and make-up candidates. 116 entered candidates did not sit. The national make-up mean uses 4,468 marks across 170 candidates, rather than averaging the regional means.

Step-by-step process.

Inspected all 17 files in the supplied archive. The specification, standard-setting record, Council minute and request email establish the selection rule, fixed standard, November sitting and Council audience. The drafts workbook, item bank and renumbering file establish the paper contents and scale. The course review supplies school-specific sequences. The entries register, school list, sessions, responses, make-up roster and keyed scripts establish participation and marks. Calibration history was used for stability checks. The candidate survey was not used because its coded questions lack a supplied interpretation; bell times do not establish curriculum completion or replace the specified paper duration. File-by-file contents and uses are recorded in Sources.

Resolved the draft items and checked compliance. All 150 draft positions map uniquely to current bank items. None uses any of the 18 retired cards. Every draft contains 50 distinct one-mark items, covers all six units and satisfies the strand limits. Paper C contains 12 Material World, 12 Living World, 14 Physical World and 12 Planet Earth and Beyond items. Content compliance therefore does not distinguish the drafts.

Reconciled registration identities. Starting with 5,682 registration rows, I removed 96 exact duplicate rows, collapsed 20 office aliases, and excluded 114 withdrawn candidates, leaving 5,452 entered people. The office aliases uniquely match school-upload records on normalized full name, date of birth and gender. Their newer, activity-bearing office records determine home school; all school changes remain within-region. The other 67 candidates without NSNs were retained. These steps are documented in Entry Resolution, Regional Cleaning and Data Audit.

Reconstructed online sittings and responses. The 5,323 session records include 157 dropped/restarted sessions, not additional candidates. Scored-response and submitted-session definitions both identify 5,166 online candidates. I retained earlier answers to non-repeated items and the latest answer where an item was repeated. Removing 331 superseded candidate-item records from 258,631 responses leaves 258,300, exactly 5,166 × 50. Of the repeated pairs, 137 changed score and 194 did not. There were no invalid binary scores or within-session item duplicates. Cleaned response counts match the published bank for all 140 items.

Aligned August evidence with November coverage. Session timestamps were converted to Pacific/Auckland time and joined to each school's course sequence. Explicit date ranges take precedence; numbered weeks start from the school's stated Term 3 start, including Tuesday starts. A unit is classified complete only after its scheduled block ends. Completed U5 coverage contributes 407 candidates and 1,628 responses; completed U6 coverage contributes 645 candidates and 2,580 responses. The reconstructed dates and classifications are retained in School Courses and Coverage.

Estimated the November item difficulties on the existing scale. I fitted an exact conditional Rasch model with 20 fixed anchors, 120 non-anchor item difficulties, and two incomplete-coverage contrasts. Conditioning on each candidate's total removes the common person-ability parameter without assuming a normal ability distribution. The estimated incomplete-coverage contrasts are 0.967 logits for U5, with a 95% interval of 0.839-1.095, and 1.073 logits for U6, with an interval of 0.957-1.189. For November, the incomplete-coverage flags are zero; Achieved remains 0.35 logits. Each draft expectation is the sum of 1 / (1 + exp(b_full_course - 0.35)).

Tested the selection. The coverage model improves held-school conditional negative log likelihood by 335.288 across eight folds. It improves every fold, and every training fit selects C. Complete-only calibration, separate not-started/in-progress contrasts, retaining published U1-U4 difficulties, and an alternative week-boundary interpretation also retain C. School-clustered 95% intervals for the unrounded expected totals are 25.733-26.198 for A, 22.712-23.261 for B, and 24.531-25.223 for C. Details are in Model Checks, School CV and Method.

Reconciled make-up attendance and marks. The roster contains 180 bookings: 156 attendees and 24 no-shows. All attendees have keyed marks. Another 14 uniquely linked valid marked scripts are absent from the roster and were included as affirmative sitting evidence, producing 170 make-up candidates. Script identifiers recover 109 missing keyed entry numbers; 47 explicit keyed identifiers also cross-check to the roster. Region is assigned from home school, not the keyed host-centre field: 40 candidates sat outside their home region.

Corrected the make-up batch's units. Batch K047 contains 13 even-valued entries ranging from 20 to 80, including four values above the permitted maximum of 50. The roster explains that covers carry both raw marks and percentages, with one template per keying batch. I therefore divided all 13 values by two, including the nine values at or below 50. This reduces the total from 4,776 to 4,468 marks. No script marks were discarded; corrected marks range from 6 to 48. Original values, divisors and corrected formulas remain visible in Make-up and Batches.

Verified the delivered artifacts. All 64 administrative checks pass, including an independent reconstruction of the regional totals. The workbook's formulas and cached results were independently checked, and its embedded Refit Code reproduces the primary estimates and selects C. The DOCX and XLSX open successfully and pass package-integrity checks; the PNG was visually inspected. Temporary analysis scripts were removed from the workspace. No Word-compatible renderer was available, so actual DOCX pagination and font substitution could not be certified; structural checks found the tables and figure within the text width.

Assumptions and judgment calls.

November coverage: The unchanged course outline supports scheduled completion of the core units before November. This is not proof of individual attendance or mastery. An August-like coverage assumption would instead favor A.
Transportability: No August candidate had both U5 and U6 classified complete. The November projection assumes the separately estimated completed-unit difficulties combine additively and remain on the same anchor scale. Cross-validation supports August response-pattern prediction, not directly observed November outcomes.
Uncertainty: The reported intervals concern estimated expected totals, not individual candidate scores. They condition on the model, fixed standard, anchors and coverage classifications.
Restart handling: Keeping the latest repeated answer is an explicit processing convention. Matching published response counts validates the resulting counts, but does not by itself prove that scoring convention.
Unrostered scripts: A valid, uniquely linked marked script was treated as stronger evidence of sitting than absence from the booking roster.
K047 conversion: The whole-batch percentage interpretation is strongly supported by the supplied records, but physical script covers were unavailable. Its effect is disclosed and tested in Mark Sensitivity.
Alternatives rejected.

Use the published August bank unchanged: This produces whole-mark expectations A 25, B 21 and C 22, selecting A. It carries uneven August coverage into the November calculation. The coverage-sensitive models fit held-out schools better and consistently select C.
Change only the calibration estimator: A pooled conditional refit still selects A. The substantive difference comes from aligning coverage with November, not simply refitting the bank.
Count registration or session rows: This would count duplicates, withdrawals or restarts rather than unique candidates.
Use roster attendees alone: This yields 156 make-up candidates and a mean of 26.4, excluding 14 valid marked scripts.
Leave keyed marks unchanged: This yields a mean of 28.1 and retains impossible raw marks above 50.
Correct only values above 50: This yields 27.3, leaving other entries from the same percentage-keyed batch on the wrong scale.
Use host-centre regions: This misattributes 40 make-up candidates across regions.
The main evidence against an unqualified recommendation is the unobserved jointly completed November state and the reliance on scheduled rather than verified coverage. Those limitations are disclosed; the tested reasonable alternatives do not overturn Paper C.

Files produced.

council_memo.docx: Council recommendation, comparison, supporting reasoning, limitations and regional annual-report figures.
achieved_marks.png: Each draft's expected Achieved mark against 25, with Paper C highlighted.
paper_choice.xlsx: Formula-based decision and regional tables, reconciled ledgers, source register, model working, sensitivity checks and embedded refit code.
All files are saved under /home/agent/workspace.

Packages installed. Installed in a temporary virtual environment: pandas, NumPy, SciPy, openpyxl, python-docx, PyMuPDF, matplotlib, Pillow and XlsxWriter, with their dependencies.
