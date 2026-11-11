# leak check, task13

**Verdict: REVIEW.** 12 files read, 49 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: record, seasons, scatter, architecture, confirmed, uncertainty, method, golden, careful, missed, nothing, carried, levels, referral, failure, rescues, result, learned, sentence, graded, shortcut, results, expectation, counts, checks

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `lightning_protection_refit_2027_programme_terms.docx`: 4 of 25 stump-paragraph terms appear (record, seasons, referral, checks); read whether the document names the move
- **REVIEW** `line_inspection_procedure_rev4.pdf`: 3 of 25 stump-paragraph terms appear (record, seasons, checks); read whether the document names the move

## 9 dates after the setting (INFO 1)
- **INFO** `-`: no --asof given, sweep skipped (pass the fiction's as-of date)

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 11 prompt gate (REVIEW 1)
- **REVIEW** `prompt.txt`: shell quota: question form 'whether' at 33% of 18 prompts (cap 30%); reword at the role level, not the verb

## 12 client quality check (INFO 2)
- **INFO** `-`: 12 usable files (10 or more required)
- **INFO** `-`: 3 file categories: document, spreadsheet, structured (2 or more required)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 3 answer figures in the pack (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)


## Solver's-eye read

Isolated reader (general-purpose, Sonnet, medium effort) on fresh copies of prompt.txt and target/ only, never solving:
a full read of the architecture 3 pack on 2026-11-11, and a re-read the same day of the two files the revision changed
(the programme terms and the zones register; the other ten files byte-identical by checksum, the prompt unchanged).
Its answers, condensed with its quotations kept:

- Q1 (sentences that say how the analysis should be done): the programme terms' definitions, quoted: 3(a) "refers every
  zone whose lightning faults since its last cyclic inspection are more than its lines would have had with sound
  protection, under the lightning that fell near them, by more than chance explains"; 2(e) the window "from the day
  after the inspection's repairs were completed"; 2(g) "within 400 m"; 2(c) "counted once ... however many times
  breakers or reclosers trip and reclose"; 2(f) the faults failed protection caused by subtraction; 3(b) "no more than
  once in five lightning seasons on average"; section 5's confirmed referral and miss; the prompt names the comparison
  ("against what sound protection would have given it"). On the revised 4(c): "This defines the quantity: a modelled
  expected-fault excess in a standardised season, with protection state frozen at end 2026. It no longer names which
  season's faults to use."
- Q2 (a file that ranks or scores the candidates): none.
- Q3 (a file that exists only to help): none is a readme or dictionary; nearest are the programme terms (definitions
  and the rule), the inspection procedure (the inspection fields) and the register's Substations sheet.
- Q4 (a figure or name that reads as the answer): none; the register's "(2015-16 programme)" header is "a covariate
  label only".
- Q5 (filed sentences that fix a computation literally): 2(c), 2(e), 2(g), 2(f), 3(b) and 5 as before; 4(c) "fixes the
  estimand (a state at end of 2026, an average-lightning season, excess over sound), not the method: how to estimate
  the end-2026 state of each zone ... and how to turn faults into an expected rate stay open".
- Q6 (one thing that makes most of it routine): none; "No single sentence or file does ... the work remains assembling
  fault events across SCADA, recloser and OMS, building the stroke exposure, fitting a sound-protection baseline,
  testing excess, calibrating to the budget, and validating on inspections. The new 4(c) is slightly less prescriptive
  than the old one."
- Extra note: the terms read spec-like and the prompt echoes their wording; the OMS LIGHTNING code is incomplete
  beside UNKNOWN and WEATHER; mixed date formats and "Clock Set" events read as realistic mess; the transformer,
  quotation and rain gauge files are unlabelled and plausible; no machine-made or trap signs.

Main-thread rulings: Q1 and Q5 quote the programme terms' definitions of what each result is (2(b), 2(c), 2(e), 2(f),
2(g), 3(a), 3(b), 4(c), 5); each executes literally to the golden's quantity and none names a clock, a memory, a
zone's level or its uncertainty, the seasons a rate is learned from or which seasons show a failed zone's state:
harmless, the filed WHAT. The prompt echoing the terms' wording is the WHAT the prompt must pin (the comparison "against
what sound protection would have given it" is 3(a)'s estimand, not a method). Q2 to Q4 none. Q6 none. Sweep 4's four
shared terms (record, seasons, referral, strokes) are the terms' own nouns for what is measured: harmless. Sweep 11's
shell quota is a corpus count of other prompts' question forms; this prompt asks "what rule", the form its decision
takes.
