# leak reader, task7

**Verdict: CLEAN**, with two minor notes (not leaks). Read: prompt.txt and the 16 files in target.zip (PDFs via pdftotext, CSV heads). The task was not solved.

## 1 Announced step, method, comparison or adjustment
No sentence names contagion, spillover, dependence between borrowers, payment links or a default-record comparison. The pack states only what the bank's own documents would state:
- ToR 3.3: "Packages go to the watch-list borrowers whose support keeps the most write-off off Ruahine's book within the envelope." This is the objective and a packing rule, both already in the prompt.
- ToR 3.4: "A borrower taken on is treated as not defaulting in the twelve months of its package. Without a package its chance of default ... is the twelve-month PD in the IFRS 9 run."
- ToR 3.5: "Write-off is valued over every borrower on Ruahine's book, each borrower that defaults at its own facilities' LGD times EAD." This is the closest to a nudge: "every borrower on Ruahine's book" widens the valuation base beyond the watch-list borrower. It reads as a definition of the estimand, not as the method (nothing says how other borrowers' defaults change, or that they are linked). Acceptable, and it is needed for determinism. Note only.
- ToR 4.1 and 4.2 (security by property index, commitment including guarantees) describe the case-file fields. They are texture and do not point at the decision.
- Validation PDF: the amber grades 5 to 7 show defaults above the PD bands. It describes calibration as a field fact, names no adjustment, and "no recalibration is recommended". Not a hint at the decisive step.

## 2 Ranking or package values
None. watch_list_2027-01.pdf lists PD, exposure and proposed line "in the order they were added", with no write-off value, no ranking and no recommended intake. The commentary is qualitative. The other REVIEW "names candidates beside numbers" files are the facility runs, customer master and security register, which are raw data keyed by customer.

## 3 New prompt wording
"the intake we would fall back on were it to turn its package down" and "the intake ... at every envelope from NZ$4.5 million to NZ$6.5 million" only say that the best intake is re-chosen with that borrower excluded, or under another envelope. They announce no step, make no mention of a link between borrowers, and give no method. They do tell the solver the choice is a re-optimisation (a surface fact of the ask itself, not of the deciding step). Nothing more is hinted.

## 4 Ambiguity in the asks
None that forks the answer.
- "turn its package down" is the borrower leaving the candidate set, the envelope unchanged. This is the plain reading.
- "the 2027 write-off that intake would keep off" is the same measure as the headline (ToR 3.5).
- Envelopes 4.5, 5.0, 5.5, 6.0, 6.5 are unambiguous (steps of 0.5); NZ$ rounded to the nearest 50,000 is stated once. Minor: the prompt does not say whether the rounding applies before or after any sum shown, but each reported figure is a single value, so no fork.

## 5 Planted or answer-key reading
None. No file names a trap, no file is labelled a distractor (sector appetite, regional indicators, commercial property index and companies register sit as ordinary context), no answer figure is stated. The PDF "9 of 14 distinctive words" hit is the borrower names and the lead phrase "business support unit" appearing in commentary, not the call; there is no sentence recommending Kinloch and Matai Valley, and the watch list contains no NZ$3,350,000.

## leak_check_report.md REVIEW lines
Harmless:
- 2 "the model" in the PD validation PDF: ordinary prose.
- 3 golden figure 1,450,000 in security_register: a coincidental property value of a guarantor's security record, not a package value (confirm it is not attached to a watch-list borrower; Pinecrest Waste Services is not on the watch list).
- 3 watch_list 9 of 14 words: explained above.
- 4 ToR 4 of 25 and validation 4 of 25 stump terms (default, december, twelve-month, carried, record): generic words, and the documents define the default and the PD, not the move.
- 6 five ranking-artifact lines: raw per-customer data, none ranks candidates on the decision question or states a package value.
- 11 shell quota (docx+xlsx at 43% of 7 prompts, cap 20%): not a leak. It is a duplication/shell matter for the author (reword deliverables at the role level or change the format), flagged for the author, not for leak purposes.
