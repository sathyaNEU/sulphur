# leak check, task3

**Verdict: REVIEW.** 19 files read, 52 golden figures and 7 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: station, marden, missed, factor, record, bucket, storage, minutes, account, instrument, reflex, rainfall, gauges, regulation, generator, carried, detector, dropped, totals, result, classes, dismissed, evidence, ciadin, tipping

## 4 design-note vocabulary (REVIEW 1)
- **REVIEW** `regulation_gully_crossings_SP141_rev4.pdf`: 6 of 25 stump-paragraph terms appear (station, record, minutes, gauges, regulation, classes); read whether the document names the move

## 6 ranking artifacts (REVIEW 1)
- **REVIEW** `gully_crossings_register.xlsx`: names 7 of 7 answer-set candidates beside numbers; confirm it does not rank them on the decision question

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 11 prompt gate (REVIEW 1)
- **REVIEW** `prompt.txt`: no method hint: carries seasonal: keep only if it is the organisation's own word for a thing, not a pointer to the step

## 12 client quality check (INFO 2)
- **INFO** `-`: 19 usable files (10 or more required)
- **INFO** `-`: 3 file categories: database, document, spreadsheet (2 or more required)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 3 answer figures in the pack (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)


## Solver's-eye read

One isolated reader (Sonnet, medium) on a fresh copy of `prompt.txt` and the 19 shipped files, 2026-11-16, cut
5607fbdb8831364c. It read for leaks and computed nothing.

1. **A sentence or file that says how the analysis is done.** The regulation fixes what each quantity is: the warm
   season and a storm's day (2.1), a storm (2.2), a triggering storm, an equal depth and one count a storm (2.3), the
   point depth (2.4), the eighteen-season mean (3.1), the depth of 3.2 and the class lines (4.1). The crossings
   register names each crossing's governing station, source area and triggering depth. In the reader's words: "The
   literal text does not say how to get from the governing station's tip record to rain at the source area ... The
   transfer step stays open." The visit book's remarks are routine and the stations register's `logger_clock` is data
   description. The request names no method.
2. **A file that ranks or classes the crossings.** None. The regulation gives the class lines and applies them to
   nothing; the register holds structure, width, year, station, source area and survey depth.
3. **A file that exists only to help.** None: no readme, dictionary, notes file or hint sheet. The weather code list
   and the research valley's gauge list read as metadata an organisation keeps beside its data.
4. **A figure or name that reads as the answer.** None. No crossing carries a class, a storms-a-season figure or a
   depth of 3.2 anywhere in the pack.
5. **Filed sentences read literally.** 3.1: the mean number of triggering storms over every complete warm season of
   the governing station's tip record. 2.1: each storm to the season of the day in which its largest 60-minute depth
   falls. 2.2: storms split at six hours without rain at the station. 2.3: reaching is greater than or equal, a storm
   counts once. 4.1: the three classes at 3.0 and 1.0. 3.2 as shipped ("reaches five times a season") did not say
   whether the count is of storms or of 60-minute windows.
6. **One thing that makes most of it routine.** None. The nearest is 3.1 and 3.2, which fix the statistic; the storm
   series, the transfer to the source area and the per-crossing estimates remain. Nothing turns on a single field,
   code or unit, and nothing looked planted.

**The sweep's three REVIEW lines, read cold.** The regulation: definitions, no step of the analysis. The crossings
register: no class, rank or score, the numbers are inputs. "seasonal": the regulation's own name for the class 2
patrol (4.1).

**Realism.** The survey dates in the source areas sheet advanced about a week at a time in the order of the source
area ids, and the ids stepped up with the road chainage. Everything else read as an organisation's records (bucket
sizes matching the register, the logger clock, the radar's renumbered pixels, the daily series' quality codes, file
dates from 2019 to 2026, container properties naming people and no tool).

**Rulings (main thread).**
- Question 5, regulation 3.2: fixed. It now reads "the crossing's 60-minute rain depth reached five times a season:
  the greatest depth that the rain at the crossing's source area reaches, counted as in 2.3, in a mean of five or more
  storms a warm season over the same seasons as 3.1", whose literal execution is the golden's (the 90th largest storm
  of eighteen seasons). It files a count and a population and names no step.
- Question 5, regulation 2.1: the golden now assigns a storm's season by the day that holds the last second of its
  largest 60 consecutive minutes (it had used the day of the first tip). One storm of the six stations changes season
  if the day those minutes open is used and five if the day of the first tip is, and no graded figure moves under
  either (`checks.py` SF4).
- Question 1: harmless. Every quoted sentence files what a result is (population, outcome, window, unit); none says
  how rain at a source area is estimated, which record sees which part of it, or what to adjust.
- Realism: fixed. The source areas carry the province's inventory numbers, which do not follow the road, and the
  survey ran in two campaigns (the high dolomite basins in the autumn of 2024, the rest in the summer of 2025). The
  visit book's clock checks now carry the seconds found.

### Pass 2, 2026-11-17, cut cdbf08e67703c82d

One isolated reader (Sonnet, medium) on a fresh copy of `prompt.txt` and the 19 shipped files after the rebuild (the
radar extract and regulation 3.2 changed). It read for leaks and computed nothing.

1. **How the analysis is done.** Nothing. "Nothing in the pack says how to relate the tip gauges to the source areas
   ... No filed sentence says which record to use for which part. That has to be worked out." The regulation's 2.3,
   2.4, 3.1, 3.2 and 4.1 define the quantities; 5.1 and 5.2 describe the stations' service and the monthly rounds; the
   stations register's `logger_clock`, `funnel_heating` and `storage_gauge` are field descriptions; the visit book's
   remarks are field routine.
2. **A file that ranks or classes the crossings.** None.
3. **A file that exists only to help.** None: no readme, dictionary or manifest; nothing is labelled as unused.
4. **A figure or name that reads as the answer.** None. The triggering depths are inputs; no file holds a storm
   count, a class or a depth of 3.2.
5. **Filed sentences read literally.** 2.1, 2.2, 2.3, 3.1, 3.2 and 4.1 quoted as shipped. 3.2 executed as "the
   largest depth D such that a mean of at least five storms a season reach D". Its questions: the clock of 2.1's
   day; a gap of exactly six hours under 2.2; what "complete" means in 3.1 beside 5.1; a fitted exceedance rate in
   place of 3.2's count.
6. **One thing that makes most of it routine.** None. "The hard part is converting tip-gauge records into
   source-area rain, and the pack gives ingredients only."

**The three flagged items, read cold.** The regulation: what to compute, not how. The register: structure and survey
fields, no rank. "seasonal": the class table's wording.

**Realism.** Nothing found. The visit book's routine remarks repeat as a routine log's do; the workbooks and the PDF
name people and an office application, with dates that agree with their text.

**Rulings (main thread).**
- 2.1's clock: harmless. The golden keeps the loggers' clock; on civil summer time no storm changes season and on UTC
  one does, and no graded figure moves under either (`checks.py` SF4).
- 2.2: harmless. "Six hours or more" splits at six hours, and no station's record holds a dry gap between three and
  eight hours (SF1).
- 3.1's complete seasons: harmless. Every station's opening round falls on 22 to 29 April and its closing round on 3
  to 8 November in each of the eighteen years, so every warm season is complete (SF5); a mean of the seasons' counts
  is the pooled count over eighteen.
- 3.2 from a fitted tail: harmless. The sentence files a count ("counted as in 2.3, in a mean of five or more storms a
  warm season"); a generalised Pareto tail lands inside every band, and an exponential tail's level leaves two bands
  by 0.1 to 0.2 mm at depths the record reaches in fewer than five storms a season (SF20).
- 5.2 and the visit book: harmless. The sentence says what the visit book is; the account against the storage gauge is
  reflex work every route does and no result's difficulty.
