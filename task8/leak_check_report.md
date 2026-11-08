# leak check, task8

**Verdict: REVIEW.** 11 files read, 8 golden figures and 1 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: architecture, reader, everyday, reflex, golden, population, shared, context, family, carried, advantage, screened, register, readers, decisive, reading, graded, record, carries, landed, records, nothing, sentence, screen, device

## 3 answer figures in the pack (REVIEW 3)
- **REVIEW** `level1_numeracy_specification_2026.pdf`: golden figure 0.90 appears: ...ectly with a chance of at least 0.20 and at most 0.90. Items outside that range are reported to the Ite...
- **REVIEW** `level1_numeracy_specification_2026.pdf`: golden figure 0.20 appears: ...dard answers correctly with a chance of at least 0.20 and at most 0.90. Items outside that range are re...
- **REVIEW** `level1_numeracy_specification_2026.pdf`: carries 19 of 27 distinctive words of the committed call: 'Set the 2027 Level 1 Numeracy pass mark at 19 of 40: a candidate who just meets the standard can be expected to score 19'

## 4 design-note vocabulary (REVIEW 1)
- **REVIEW** `level1_numeracy_specification_2026.pdf`: 6 of 25 stump-paragraph terms appear (reader, everyday, context, register, record, screen); read whether the document names the move

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 11 prompt gate (REVIEW 1)
- **REVIEW** `prompt.txt`: shell quota: question form 'whether' at 71% of 7 prompts (cap 30%); deliverable set 'docx+xlsx' at 43% of 7 prompts (cap 20%); reword at the role level, not the verb

## 12 describing content (REVIEW 1)
- **REVIEW** `level1_numeracy_specification_2026.pdf`: names 10 column(s) of the data files verbatim (Data, Item, Money and measures, Strand, centre, item): confirm it is the organisation's own record and not a note written for the analyst

## 12 client quality check (REVIEW 1, INFO 2)
- **REVIEW** `pacb_candidate_register_2022_2026.csv`: 'Whitney': ...2007,L2,2022,LC-0219,LC-0219,LC-0219,2022-10-28,Sat, R614350,PA305460,Whitney,Susan,2005-04-24,L2,2022,LC-0251,RO-INT,LC-0251,2022-09-14,Sat, R6143...
- **INFO** `-`: 11 usable files (10 or more required)
- **INFO** `-`: 2 file categories: document, spreadsheet (2 or more required)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## Solver's-eye read (second pass, rebuilt pack after the stage 4 fixes, 2026-11-08)

# Leak reader answers (task8b)

1. Decisive step stated? Partly, by the specification and the 2022 record, not by a "how to" sentence.
   - level1_numeracy_specification_2026.pdf s4.2: "The pass mark on each Level 1 paper is the mark that a candidate who just meets the Level 1 standard can be expected to score on that paper, rounded to the nearest whole mark." (restated in prompt.txt)
   - ln1_standard_setting_record_2022.pdf s3: "such a candidate can be expected to score 26 of the 40 marks on the 2022 Level 1 paper"; s2: "A panellist's total is the sum of their ratings over the 40 items".
   No file names a linking, equating or calibration method.
2. Ranks/scores the answer? none. The 2022 record gives 26/40 for the 2022 paper only (an anchor, not a 2027 answer). pacb_item_bank_2026.csv has difficulties (data, not a ranking of answers).
3. Exists only to help the analyst? none clearly. The 2022 standard-setting record is the spec's cited source (s4.1) and reads as a real organisational record. The email and minute are plausible correspondence. Closest to "helper": pacb_paper_layouts_2022_2027.xlsx (but a plausible operational record).
4. Reads as the answer? Only "26 of the 40" / "pass mark was set at 26" (ln1_standard_setting_record_2022.pdf s3), the 2022 figure; context, but a tempting anchor. Specification band "at least 0.20 and at most 0.90" (s5.1) is a stated rule, not an answer.
5. Literal-execution sentence: spec s4.2 (above), with s4.1 fixing the standard as the 2022 panel's. Literally: compute, for the 2027 Level 1 paper (the 40 items listed in the layouts workbook sheet "LN1 2027"), the expected total score of a candidate sitting at the 2022 standard, i.e. the sum over the paper's items of that candidate's chance of a correct answer, then round to a whole mark. The ability of the "just meets" candidate is fixed by the 2022 record (expected 26 of 40 on the 2022 paper), so it has to be carried to the 2027 items. Items: s5.1 band 0.20 to 0.90 inclusive. Regional means: expected score on the 2027 paper of the 2026 Level 1 sitters in each region (prompt wording).
6. What decides it: an analytical choice, on the face of the files (carrying a fixed 2022 standard onto a different paper via the item bank and response data, and deciding which difficulty estimate / which candidates / how items and the 2022 standard link). Nothing read as a stated procedure that spells out the steps; no planted-defect sentence is announced. Supporting facts that are only discoverable by data work (not stated): register level labels vary (L1/Level 1), centre merge note in the minute s4, preliminary vs final item-bank runs (the email says "the bank's annual run is done"; minute s1 says the annual run follows marking). These are hygiene hints, not the decider.

(a) pacb_learning_centres.csv: harmless. Town column reads as complete, real Manitoba/Saskatchewan place names (Weyburn, Flin Flon, Virden, North Battleford, The Pas, Swan River, Souris, Neepawa, etc.), province codes consistent with the towns. No truncation seen. Centre names such as "Sargent Avenue Adult Centre (Suite 210)" are texture.

(b) awards_committee_minute_2026-09-17.pdf: harmless. "Unconfirmed: to be confirmed at the next meeting of the Committee" is consistent with a 17 Sept minute whose next meeting is 3 Dec 2026 (PDF created 21 Sep 2026); all events are future or <= 31 Aug/17 Sep relative to its date. Nothing narrates how data were built or points at a method. Mild signposting only: s3 lists "the item table", "regional figures" the Committee will want (they are in the prompt anyway), and s4 notes the Winnipeg merger on 1 July 2025 ("earlier records stay under their own codes"), which is a data-semantics hint a real minute could carry. Rate harmless, borderline on the merger sentence only.

Realism notes: no dates after the decision date (3 Dec 2026) in files; the email is dated 9 Nov 2026 and the data run to 30 Oct 2026, consistent. Item bank holds both "2026-06 preliminary" and "2026-10 final" runs for every item, which is natural. The 2027 layout names sheets "LN1 2027" only (no LN2 2027), fine. No hidden sheets, no cell comments, no machine-written prose found. Email text is a little tidy but plausible. Minor: the email says the "item table we asked for last year", consistent with the minute.
