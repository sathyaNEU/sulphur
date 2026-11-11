# leak check, task9

**Verdict: REVIEW.** 13 files read, 53 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: window, firmware, migration, survivors, missed, inside, method, shortcut, retired, result, close-out, expected, priced, forecast, forecasting, serial, review, release, inventory, average, nearest, migrate, passes, predictive, pooled

## 1 file names (REVIEW 1)
- **REVIEW** `ops_policy_wiki.md`: a text file in the pack: confirm it is the organisation's own record (a thread, a log, a letter) and does not describe the data

## 4 design-note vocabulary (REVIEW 1)
- **REVIEW** `ops_policy_wiki.md`: 5 of 25 stump-paragraph terms appear (retired, serial, review, inventory, migrate); read whether the document names the move

## 8 column names (REVIEW 2)
- **REVIEW** `drive_quarter_stats.csv`: columns a generator names and an organisation does not: avg_temp_c
- **REVIEW** `ssd_boot_drive_stats.csv`: columns a generator names and an organisation does not: avg_temp_c

## 9 dates after the setting (INFO 1)
- **INFO** `-`: no --asof given, sweep skipped (pass the fiction's as-of date)

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 11 prompt gate (REVIEW 1)
- **REVIEW** `prompt.txt`: shell quota: deliverable set 'xlsx' at 22% of 18 prompts (cap 20%); reword at the role level, not the verb

## 12 client quality check (INFO 2)
- **INFO** `-`: 13 usable files (10 or more required)
- **INFO** `-`: 4 file categories: document, image or presentation, spreadsheet, structured (2 or more required)

## 2 author vocabulary (clean)

## 3 answer figures in the pack (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## Solver's-eye read

One isolated reader (stage 4, medium effort, 2026-11-11) read prompt.txt and target/ only and solved nothing. Verdict: no leak. No file ranks the candidates or carries the answer; nothing reads as planted; the swept items are harmless; no single item makes most of the asks routine (the P2 policy settles which history is comparable but not the batch, its path, the per-vault call, the spares quantile, the interval or the coverage). Its answers, verbatim:

Scope read: prompt.txt and every file in target/: both xlsx (all sheets), both PDFs, the PNG, the md, the yaml, and the heads and samples of every CSV. Nothing was solved and no figures were computed.

## 1. Sentences that say how part of the analysis should be done

- prompt.txt: "Count the data drives in service on 30 September 2026 plus the scheduled vault installs." This sets the forecast population. "intervals built the same way from the records to 30 September 2025 held the next four quarters' replacements by family and quarter in vaults that stayed in service" sets the back-test window, its grain and its population. These pin the WHAT (population, window), not a method.
- ops_policy_wiki.md: "Two removal reasons count: FAIL ... PULL", "A drive removed with its vault (`DECOM`) is not a replacement", "A removed drive whose serial is back in a slot within 30 days of the removal was not a failure (a reseat or a cable fault): count the removal out and the drive as in service throughout", "Boot SSDs and the QA burn-in vault (QA-01) are not data drives". These are outcome and population definitions.
- ops_policy_wiki.md, the health-pull table: "P2 | from 2025-06-01 | P1's rules, or SMART 187 (reported uncorrectable) above 0, or SMART 5 above 20". This does not give a step, but it names a dated regime change in what counts as a pull, so it points at a break in the replacement series.
- fleet_reliability_q3_2026.png footnote: "Replacements (FAIL + PULL) per drive-day, annualized. Source: telemetry warehouse, drive-days method." This states how an annualized rate is computed (drive-day exposure).
- kestrel_fe118_serial_numbers_and_firmware.pdf: "four digits giving the year and ISO week the drive was built (YYWW) ... Some customer systems print the serial with dashes". This is how a Kestrel build week (a candidate "manufacturing batch") is read from a serial. It describes a field, not a step.
- procurement_and_costs.yaml: `lead_time_quarters: 1`, `stockout_tolerance: 0.10`, `vault_migration_cost_usd`, `failure_handling_cost_usd`. These are inputs. The tolerance restates the prompt.

No file names a model, a smoothing or base-rate window, an interval construction, a batch-risk ranking method or a doubling-time method.

## 2. Files that already rank or score the candidates

- None ranks manufacturing batches, and none gives the forward count.
- fleet_reliability_q3_2026.png ranks the three sites by trailing annualized replacement rate through 2026 Q3. Sites are a breakdown dimension, not the decision's candidates, and it is backward-looking.
- vendor_datasheets.pdf ranks the families by vendor AFR and MTTF. These are vendor specs, not fleet experience.
- brightstore_handover.xlsx, sheet legacy_failure_summary, gives "failures_replaced" by Brightstore rack and year for KS10T0A (to 2023, no serials). It is historical context, not a forward ranking.

## 3. Files that exist only to help the analyst

- None is clearly synthetic help. The nearest is kestrel_fe118_serial_numbers_and_firmware.pdf. It is plausible as a real vendor field guide (dated 2025-04, FE-118 rev C), but in this pack its main use is decoding Kestrel build weeks and factory firmware, which is how batches get identified. Its relevance comes from the task, but it does not read as written for it.
- fleet_reliability_q3_2026.png is an internal report chart. It reads as an organisation's own artefact.

## 4. Figures or names that read as the answer rather than context

- None reads as the answer. Things to note:
  - vault_events.csv, 2026-03-16 DC-3: "ops review of KS-10 vaults (Amanda Higgins)", followed by the C03 decommission. This names a family the organisation is already reviewing for retirement, which nudges toward KS10 batches as the forward-risk candidate. It is plausible ops history and does not name a batch.
  - The PNG's 2026 Q3 site rates are trailing context and could be taken as a site-level base rate.
  - capacity_plan_2027.xlsx gives the scheduled installs (TS24000E, 2 vaults or 2400 drives per quarter, DC-2 then DC-1). This is a required input, not an answer.

## 5. Filed sentences that, read literally, fix how a graded figure is computed or over which population

- ops_policy_wiki.md: "A removed drive whose serial is back in a slot within 30 days of the removal was not a failure ... count the removal out and the drive as in service throughout." Read literally, this drops those removals from every replacement count and keeps the drive's exposure continuous. That affects every count, rate and back-test figure. removal_tickets.csv carries RETURN_TO_SERVICE tickets that make it executable.
- ops_policy_wiki.md: "A drive removed with its vault (`DECOM`) is not a replacement" and "Boot SSDs and the QA burn-in vault (QA-01) are not data drives." Read literally, these exclude DECOM removals, all boot SSDs and the QA-01 vault from the numerator and the in-service population.
- ops_policy_wiki.md: the P1 and P2 table. Read literally, what counts as a PULL depends on the date. It fixes the outcome's definition across the series, and so which history is comparable to the forward window.
- prompt.txt: "the data drives in service on 30 September 2026 plus the scheduled vault installs". Read literally, the forecast population is the 30 September snapshot plus capacity_plan_2027 installs. Vaults retired later at future reviews are not explicitly addressed.
- prompt.txt: "in vaults that stayed in service". Read literally, the back-test coverage is scored only on vaults not decommissioned during the four quarters after 30 September 2025.
- fleet_reliability_q3_2026.png footnote: "per drive-day, annualized". Read literally, this fixes the annualization of the batch's July to September 2026 rate as an exposure-weighted (drive-day) rate.
- procurement_and_costs.yaml: `failure_handling_cost_usd: 250   # per replacement` and `vault_migration_cost_usd: 60000`. Read literally, these fix the cost terms of the migrate-or-run comparison.

All of these are WHAT-level definitions, which is legitimate. They are listed because the reseat rule and the P2 table are the two filed sentences most likely to move figures.

## 6. Is there one thing that makes most of the ask routine?

- The strongest single candidate is the P2 health-pull policy from 2025-06-01 (ops_policy_wiki.md), together with the visible 2025 Q2 to Q3 spike and fall-back in the PNG. Noticing it settles which history window to use as the base rate, and it explains why a naive trailing average or the back-test from 30 September 2025 behaves oddly. It does not settle the batch identification, the batch's forward path or its doubling-time flip point, the spares quantile, the interval construction or the back-test coverage figure itself. So it does not make most of the ask routine.
- Other single items: the Kestrel serial guide settles how to read a batch from a serial but not which batch is riskiest, and the reseat rule settles one cleaning step.

Each part of the ask:
- Quarterly counts and the four-quarter total with 80% intervals by DC and family: analysis (hazard by family and age, exposure, the forward path, interval construction). It also uses the filed definitions (reseat, DECOM, QA-01, boot SSD) and the model-string cleanup (many spellings of each model in drive_inventory.csv), which are routine cleaning.
- "what drives it" (attribution): analysis.
- Batch with the highest forward risk: analysis (defining batches from serial week, PO or firmware, then forward risk, not trailing count). It turns partly on reading the serial format (FE-118) and the dash variant (KS-TH-1905-00006 in the Brightstore manifest against KSTH... in the inventory).
- Its drives in service and its July to September 2026 annualized rate: mostly reading definitions (in service at 30 September, drive-day annualization per the PNG footnote), so these lean toward field reading.
- Its four-quarter replacements: analysis (a forward path).
- Migrate now or run to failure over 24 months, and the flip doubling time: analysis (cost model with a growing hazard), using filed costs.
- Fourth-quarter spares per family at 10% stockout: analysis (a predictive distribution quantile net of stock on hand, with lead time). The tolerance and lead time are filed.
- Back-test coverage from records to 30 September 2025: analysis (refitting on truncated data), with population pinned by the prompt ("vaults that stayed in service").

Nothing looks planted as a single decoy. The noted oddities (mixed date formats, model-string variants, Brightstore re-keyed serials and pre-acquisition history, cooling and power events, the replaced_in_qtr flag) read as texture.

## Swept items

- REVIEW ops_policy_wiki.md (own record, does not describe the data): harmless. It reads as an ops wiki page with an owner and an edit date, giving the organisation's definitions and policies. It does not describe file layouts, column quirks or any analysis step. The DC-3 sentence states an acquisition fact, not a data warning.
- REVIEW ops_policy_wiki.md (shares words with the hard part): harmless, with a caution. The overlap is presumably the replacement and pull definitions, the P1 and P2 dated policy change and decommissioning. It gives the outcome definition and flags a dated regime change, but it gives no method, window choice, batch or answer. If the hard part is recognising the P2 transient, this page plus the PNG makes that recognition easy, though not its resolution.
- REVIEW drive_quarter_stats.csv and ssd_boot_drive_stats.csv (column names): harmless. `days_observed`, `replaced_in_qtr`, `smart_*_max`, `smart_9_hours_end`, `wear_level_pct` and `media_errors` read as a telemetry warehouse quarterly rollup. The one to watch is `replaced_in_qtr`: it is a pre-derived outcome flag. If it already applies the wiki's reseat and DECOM rules, it hands over the numerator per drive-quarter. If it does not, it is a shortcut that disagrees with the definition. Either way it reads as an organisation's field, not a generator's.
- REVIEW prompt.txt (common deliverable set): harmless. "a spreadsheet" plus "a chart of the path and interval" is an ordinary deliverable pair and reveals nothing about method or answer.
