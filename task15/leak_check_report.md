# leak check, task15

**Verdict: REVIEW.** 13 files read, 66 golden figures and 1 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: record, margin, result, licence, inside, kvarter, trading, careful, decision, missed, estimate, comparison, agreement, second, prompt, openings, graded, turned-away, trials, series, reading, lodging, method, in-stock, estimator

## 3 answer figures in the pack (REVIEW 8)
- **REVIEW** `dagssalg_frisk_2026.csv`: golden figure 50,100 appears: ...47,40,0,19 2026-02-21,2179,451819,43,528.90,18:54:50,100,0,76 2026-02-21,2179,451826,45,738.00,13:54:52,30...
- **REVIEW** `dagssalg_frisk_2026.csv`: golden figure 24,100 appears: ...:34,8,0,17 2026-07-18,2185,451819,80,984.00,20:58:24,100,0,22 2026-07-18,2185,451826,170,2261.00,13:01:53,...
- **REVIEW** `dagssalg_frisk_2026.csv`: golden figure 36,100 appears: ...,24,0,10 2026-01-02,2104,451819,109,1340.70,21:44:36,100,0,41 2026-01-02,2104,451826,111,1476.30,16:05:32,...
- **REVIEW** `dagssalg_frisk_2026.csv`: golden figure 33,100 appears: ...18,8,0,8 2026-03-18,3072,451819,106,1028.20,20:47:33,100,0,18 2026-03-18,3072,451826,16,262.40,20:45:31,20...
- **REVIEW** `pilotaftale_kornblomst_2026.pdf`: golden figure 014 appears: ...st in Fjordkøb's fresh ordering Agreement FK-2026-014, signed 19 February 2026. Annex 2 replaced on 1 S...
- **REVIEW** `pilotaftale_kornblomst_2026.pdf`: golden figure 4.3 appears: ...uding VAT less the cost price of the units sold. 4.3 A year is 52 weeks, taken as twice the 26 weeks o...
- **REVIEW** `pilotaftale_kornblomst_2026.pdf`: golden figure 4.2 appears: ...taken for all of its stores or for none of them. 4.2 The saving of a store is the change in its fresh...
- **REVIEW** `pilotaftale_kornblomst_2026.pdf`: carries 9 of 10 distinctive words of the committed call: "Switch the Super and Kvarter stores to Kornblomst's fresh forecast for 2027 and keep the To Go stores on AutoOrdre."

## 4 design-note vocabulary (REVIEW 1)
- **REVIEW** `pilotaftale_kornblomst_2026.pdf`: 6 of 25 stump-paragraph terms appear (margin, result, licence, kvarter, decision, agreement); read whether the document names the move

## 9 dates after the setting (INFO 1)
- **INFO** `-`: no --asof given, sweep skipped (pass the fiction's as-of date)

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 11 prompt gate (REVIEW 1)
- **REVIEW** `prompt.txt`: shell quota: question form 'whether' at 35% of 17 prompts (cap 30%); deliverable set 'pptx+xlsx' at 24% of 17 prompts (cap 20%); reword at the role level, not the verb

## 12 client quality check (INFO 2)
- **INFO** `-`: 13 usable files (10 or more required)
- **INFO** `-`: 2 file categories: document, spreadsheet (2 or more required)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)


## Solver's-eye read

One isolated reader (general-purpose, sonnet, medium), 2026-11-11, on a fresh copy of prompt.txt and target/ from the stage 4 cut; it saw no design note, generator, submission or report.

# Leak read, task15 (no figures, no answer)

1. Method-giving text. None dictates a method outright. Closest, in pilotaftale_kornblomst_2026.pdf: 4.2 "the fresh waste it avoids, valued at cost price, plus the gross margin on the fresh units it sells in addition, less the gross margin on the fresh units it no longer sells. Gross margin is the sales value excluding VAT less the cost price of the units sold." (defines the saving's components and valuation); 4.3 "A year is 52 weeks, taken as twice the 26 weeks of the pilot ... average over every store of that format in Fjordkøb's store register, pilot stores and other stores alike" (window scaling and population); 4.1 "A format is taken for all of its stores or for none of them" (decision rule); 2.1 the pilot window (2 March to 30 August 2026, 26 weeks); 2.3 "pilot stores set their safety stock with ... 0.75. The other stores keep ... 1.05" (a second change besides the forecast); 2.1 "The pilot stores were chosen by Fjordkøb's regional managers" (selection hint). pilot_dashboard_uge35.xlsx row 2: "uge 10 til 35 2026 mod samme uger 2025" repeats the comparison window. The prompt itself ("against the same weeks of 2025", "split into its causes", "80% range") names the comparison but no method.

2. Ranking/scoring files. pilot_dashboard_uge35.xlsx gives pilot vs other raw totals and waste % by week, but ranks no format and scores no switch decision. Nothing else ranks. (Its raw gap is the naive comparison the prompt asks to explain.)

3. Files existing only to help the analyst: none clearly. pilot_dashboard_uge35.xlsx is a plausible BI deliverable; bi_uge_butik_kategori.csv is a weekly BI roll-up (convenience duplicate of the daily files, with old/new category codes). Annex 1 in the PDF lists pilot membership, which is needed context.

4. Answer-like figure or name: none. The Annex 2 licence prices (27,000 / 20,000 / 9,000 DKK) are thresholds, not answers. The dashboard's pilot/other waste percentages (about 4.6 vs 7.1) are context, though they sit near the "fresh waste fell further" half of the question.

5. Filed sentences that fix a figure's computation or population:
- 4.2: the saving of a store = waste avoided at cost + margin on extra units sold - margin on units no longer sold; margin = sales ex VAT minus cost of units sold. Fixes valuation and sign convention of the per-store saving.
- 4.3: year = 2 x the 26 pilot weeks; format saving = average over every store of that format in the store register (pilot and non-pilot). Fixes the annualisation and the population (all register stores, including not-yet-observed ones).
- 4.1: format taken for all stores or none; compare expected saving per store and year to the licence. Fixes the decision unit and threshold.
- 4.2 "at the recommended setting" with 2.3 (service factor 0.75 recommended). Fixes the setting at which the saving is valued.
- 2.1: pilot window. Fixes the period.
- Annex 2 "excluding VAT" fixes the price basis.

6. Single thing that would make most of it routine: none found. The nearest candidates: (i) 2.3 plus the safety_stock column in ordreforslag_2026.csv (a second change coincident with the forecast swap) would settle how the gaps split into forecast vs service factor, but only that split; (ii) "pilot stores were chosen by regional managers" would settle that selection/baseline differences matter, but not the sizes; (iii) the competitor openings file (some near pilot stores, some near others) is only one cause among several. Section 4.2/4.3 hands over the saving formula and annualisation, which makes the final DKK step a stated rule, but the inputs still need estimating.
Part by part:
- Why sales grew less (and its pp split): analysis (estimating causes such as competitors, promotions, weather, availability, selection), with some reading of codes/definitions (2025 vs 2026 file layouts, old vs new item numbers, price changes).
- Why waste fell further (pp split): analysis, with the same reading of definitions (units, cost price per year, write-off fields).
- Per-format expected saving per store and year with 80% range: mostly analysis (counterfactual for non-pilot stores, uncertainty), but the formula, 52-week scaling and averaging population are a stated rule in 4.2/4.3 (rule-following for those pieces).
- Formats to switch: follows a stated rule (4.1, Annex 2) once the savings exist; the analysis is upstream.
- Deliverables: instruction-following.
- Planted-looking items: the 2025 CSV's different encoding/format and the old milk item numbers read as ordinary migration mess; the 2026 daily file ends 30 Aug and the pilot window ends 30 Aug, so nothing stands out as planted. The dashboard "uge 10 til 35" mismatch with the pilot's 26 weeks (W10 to W35 is 26 weeks) is consistent.

(a) pilotaftale_kornblomst_2026.pdf: harmless. Overlap is the shared domain vocabulary and the filed conventions (52 weeks, 26 weeks, 0.75/1.05, licence prices, saving definition), which are inputs and rules, not computed results. It gives the formula and decision rule but no figures that are outcomes. Borderline only in that 4.2/4.3 spell out the saving formula; that is a filed estimand, not a result.
(b) dagssalg_frisk_2026.csv: harmless unless the shared number is a derived result; as an input row-level file, a single shared number (a store id, item number, price or count) reads as coincidence. I could not see the expected answer, so I cannot confirm; nothing in the file is labelled or aggregated as a result.
(c) vejr_dmi_2025_2026.csv: harmless. Headers "Dato;By;Maks. temperatur (°C);Nedbør (mm);Solskin (timer)" are Danish, human-style and match the DMI naming; the semicolons and decimal commas match the other Danish-format exports.

Realism tells:
- dagssalg_frisk_2025.csv is semicolon, Danish decimals, Latin-1 with Danish headers, while dagssalg_frisk_2026.csv and ordreforslag_2026.csv are comma, English headers, ISO dates and last_sale with seconds; plausible as a system migration but a sharp break (ERP vs new system).
- pilot_dashboard_uge35.xlsx has extremely clean round-trip two-decimal sums and "Version 26" header; looks fine.
- ordreforslag_2026.csv and dagssalg_frisk_2026.csv have identical row counts (325,248), every store-item-day present with no gaps; very complete for a real extract.
- Only 32 items and 42 stores with identical item range per store (including To Go stores) is a tidy grid.
- konkurrentaabninger.csv is a tiny 10-row hand-kept list with a free-text remark ("nærmeste Fjordkøb er Galten") on only one row; fine.
- Office files (bi/butiksregister/vareregister) otherwise look natural.

### Main thread's rulings

- Questions 1 to 4: nothing to fix; the agreement's 4.1 to 4.3 file the decision's WHAT (the saving, the year, the population, the rule) and no method.
- Question 5: every quoted sentence executes to the golden's estimand (4.2's saving, 4.3's year and population, 4.1's rule, Annex 2's prices).
- Question 6: none found. Its note on 2.3 (the service factor changing with the forecast) is taken: the forecast's part of each gap is now labelled the forecast at its recommended setting, the package 4.2 prices.
- (a), (b), (c): harmless, as the reader says.
- Realism: the To Go stores no longer carry raw meat (fixed in the generator); the 2025 and 2026 layouts are the ERP migration the note files; the order log and the 2026 extract match row for row because both are the ERP's own log of every ranged store, item and day.
