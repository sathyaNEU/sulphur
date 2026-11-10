# leak check, task15

**Verdict: REVIEW.** 18 files read, 101 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: trials, season, careful, result, inside, byaduk, record, second, missed, blocks, remainder, rivals, nothing, standards, selection, carried, leaves, clause, prompt, banyena, spread, fitted, pressure, section, waterings

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `option_deed_schedule_2.pdf`: golden figure 2.1 appears: .... A line is nominated once. 2 The uptake standard 2.1 Mount Rouse will exercise its option over a nomin...
- **REVIEW** `option_deed_schedule_2.pdf`: golden figure 4.2 appears: ...dule before Banyena nominates for a sowing year. 4.2 A review takes the nominated lines for which the...

## 4 design-note vocabulary (REVIEW 4)
- **REVIEW** `BGG_trial_handbook_2024.pdf`: 8 of 25 stump-paragraph terms appear (trials, season, byaduk, record, second, blocks); read whether the document names the move
- **REVIEW** `HRBS_trial_protocol_2023.pdf`: 6 of 25 stump-paragraph terms appear (trials, season, result, byaduk, blocks, section); read whether the document names the move
- **REVIEW** `option_deed_schedule_2.pdf`: 8 of 25 stump-paragraph terms appear (trials, season, byaduk, record, second, remainder); read whether the document names the move
- **REVIEW** `season_review_2025.docx`: 4 of 25 stump-paragraph terms appear (trials, season, result, record); read whether the document names the move

## 9 dates after the setting (INFO 1)
- **INFO** `-`: no --asof given, sweep skipped (pass the fiction's as-of date)

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 11 prompt gate (REVIEW 1)
- **REVIEW** `prompt.txt`: shell quota: question form 'whether' at 31% of 16 prompts (cap 30%); deliverable set 'xlsx' at 25% of 16 prompts (cap 20%); reword at the role level, not the verb

## 12 describing content (REVIEW 2)
- **REVIEW** `BGG_trial_handbook_2024.pdf`: names 13 column(s) of the data files verbatim (Plot, Trial, WI number, block, harvested, line): confirm it is the organisation's own record and not a note written for the analyst
- **REVIEW** `HRBS_trial_protocol_2023.pdf`: names 13 column(s) of the data files verbatim (District, Site, Soil, breeder, district, entry): confirm it is the organisation's own record and not a note written for the analyst

## 12 client quality check (INFO 2)
- **INFO** `-`: 18 usable files (10 or more required)
- **INFO** `-`: 2 file categories: document, spreadsheet (2 or more required)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)


## Solver's-eye read

One isolated reader (general-purpose, sonnet, medium effort) on 2026-11-10, on a fresh copy of the final
`prompt.txt` (what two lines to nominate; no bar, no chances) and the final cut of `target/` only (world 3153, the
deed with its review clause). It read every document in full and the head of every data file, solved nothing, and
answered the six questions and a realism question. Two earlier reads stand behind it: one on the first cut, whose
realism tells (the same number of lines entering and leaving every season, a series entry list of one size, no trial
lost and no comment in twelve seasons, a handbook sentence on clean seed that read as an eligibility test) were
fixed in the generator; and one on this same pack with the earlier prompt, which found nothing to fix.

1. A sentence or file that says how any part of the analysis is done: none prescribes a method. It quoted
   definitions that "fix what each head is, not the model": the deed's clause 4.2 with heads (a) to (d), the
   handbook's section 6 (the index over harvested plots at Lake Bolac, Skipton and Kerang), the protocol's section 7
   (relative yield as a ratio of means), the handbook's section 5 (the later weighing stands; an abandoned plot has
   no weight) and the protocol's section 5 (every plot harvested). "No sentence names a model, adjustment or grouping
   for the expectations or the forecast."
2. A file that ranks or scores this year's candidates: none.
3. A file that exists only to help the analyst: none; the line register and the site list read as the
   organisation's own registers, the handbook as its standing document.
4. A figure or name that reads as the answer: none; the deed's 107.0 is the uptake standard, context only.
5. Filed sentences that fix a computation, population or window, read literally: the deed's 4.2 (the nominations
   with both seasons published, the two means, the four heads as means over the lines, head (d) the expected at the
   series trials less the returned); the handbook's section 6 (the index's trial set and harvested plots); the
   protocol's section 7 (ratio of means), section 3 (two series seasons a nomination) and section 2 (a trial lost
   before harvest is no trial of the series); the handbook's section 5 (the later weighing); the deed's 1.2 (a line
   is nominated once, so nominated lines leave the candidates).
6. One thing that would make most of the request routine: none. The handbook's index definition with the deed's
   heads "point at what the gap consists of ... They define the heads but not the numbers or the model"; the
   expectations, the forecast, the range and the lodging "remain separate work", and "the request does not rest on
   one planted thing". Item by item: the heads, each line's expected relative yield, the range and the expected
   lodging turn on analysis; the two means follow the stated definitions; head (c) needs its definition read and the
   lodging effect analysed; the cleanup is reading codes and rules with no planted item. On the yardstick for the two
   lines it said the request leaves it open: the highest expected relative yield, the highest chance of the deed's
   107.0, the highest low end of the 80% range, or the lowest lodging or a mix.
7. Realism: nothing reads as generated or as written for an exercise. It noted the seed sent with a nomination in
   round kilograms and a comment wording that recurs in two seasons, both plausible. No two files contradict each
   other: the season review's 17 trials, 3,024 plots, 22 plots abandoned at Kerang and five waterings of 222 mm agree
   with the trials file, the plot file and the irrigation log.

The mechanical sweep's REVIEW lines, as the reader ruled them: (a) the deed's flagged numbers are clause numbers,
harmless; (b) the handbook is the programme's standing handbook, harmless; (c) the protocol is the Trust's standing
protocol, harmless.

Main-thread rulings. Question 5: each quoted sentence, executed literally, is the golden's own convention (fork
table SF1 to SF4, SF6, SF7, SF10 and SF13, each asserted in `checks.py`); none executes to a hurried figure.
Question 6, the yardstick: closed by convergence and asserted (SF18): the two lines with the highest expected
relative yield, the two with the best chance of the deed's standard and the two with the highest low end of the
range are the same two, WI3554 and WI3559; the lowest lodging alone is no yardstick for a yield series, and the
lines it would name stand ninth and second. The stump-vocabulary lines were not shown to the reader and are ruled in
the design note's `## Leak review`. Nothing to fix.
