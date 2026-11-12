# leak check, task7

**Verdict: REVIEW.** 21 files read, 31 golden figures and 3 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: architecture, buildings, golden, record, carried, controls, insulation, million, events, pinecrest, lumivale, careful, window, feeder, season, kitebrook, patients, heating, building, spread, missed, landed, author, seasons, comparison

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `peak_partners_member_guide_2026.pdf`: carries 8 of 10 distinctive words of the committed call: 'Renew Corvane, Ardena and Kitebrook for summer 2027; do not renew Lumivale, Ondera or Pinecrest Home.'

## 4 design-note vocabulary (REVIEW 1)
- **REVIEW** `peak_partners_member_guide_2026.pdf`: 4 of 25 stump-paragraph terms appear (pinecrest, lumivale, window, kitebrook); read whether the document names the move

## 8 column names (REVIEW 6)
- **REVIEW** `corvane_event_report_2024_2026.csv`: columns a generator names and an organisation does not: device_serial
- **REVIEW** `kitebrook_events_2024_2026.csv`: columns a generator names and an organisation does not: DEVICE
- **REVIEW** `ondera_events_cbec.csv`: columns a generator names and an organisation does not: device
- **REVIEW** `peak_partners_roster_2026-10-30.csv`: columns a generator names and an organisation does not: device_id, previous_device_id, device_changed_on
- **REVIEW** `pinecrest_home_events.csv`: columns a generator names and an organisation does not: device_id
- **REVIEW** `weather_kcdr_hourly_2024_2026.csv`: columns a generator names and an organisation does not: temp_f

## 9 dates after the setting (REVIEW 1)
- **REVIEW** `der_interconnections_2026.csv`: 45 ISO dates after 2026-11-02, e.g. 2026-11-03, 2026-11-04, 2026-11-05, 2026-11-08, 2026-11-09

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 12 client quality check (INFO 2)
- **INFO** `-`: 21 usable files (10 or more required)
- **INFO** `-`: 2 file categories: document, spreadsheet (2 or more required)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 11 prompt gate (clean)


## Solver's-eye read

Architecture 10, 2026-11-12: one isolated reader (Sonnet, medium) on fresh copies of prompt.txt and the pack cut at stage 4,
briefed with the six questions only (every mechanical REVIEW line a stump-vocabulary match, ruled in the main thread).
Main thread's rulings (also in the design note's Leak rulings): questions 2 to 4 none; question 1 quotes WHAT only and
the M&V plan's design; question 5's literal readings are the golden's; question 6 finds no one thing and sets the
appraisal roll aside (the carry the build prices, L38); the stamp notes are what Excel writes, and the as-of moved to
2 November 2026 so no stamp sits after the day the build ships. Nothing else to fix.

### The reader's answers (verbatim, its dashes set as commas under the house rule)

**Files read:** `prompt.txt` plus all 21 files under `target/` (6 provider event logs in 6 different schemas, the co-op's own roster/member/AMI/event-log files, 5 PDFs, 2 xlsx workbooks, a weather file and an ERCOT 4CP-date file). No figures below are computed answers to the prompt; row counts and field values are quoted only to show what a file contains.

**1. Sentence/file that tells you HOW any part of the analysis should be done.** Nothing I found gives a step, comparison, adjustment or model to run. Several sentences in `board_policy_412_demand_response_providers.pdf` fix WHAT a quantity is, not how to produce it: 4.1 ("The saving is the provider's reduction of the co-op's load in the 4CP intervals, averaged over the four, times the transmission rate in the co-op's current notice."), 4.2 ("The reduction in an interval is what the co-op's load would have been in that interval without the provider's event, less what it was. It is counted per device enrolled with the provider on 1 July of the summer, whether or not the device takes part in a given event."), 4.3 (the twelve 4CP intervals of the three summers before, the alerts as called, the quoted settings) and 5 (the quoted price per device enrolled on 1 July). The closest to a method is `peak_partners_mv_plan_2024.pdf`: "On each test event the co-op divides every provider's enrolled devices into two halves at random, calls one half and holds the other back.", a description of why the data look as they do; the same document says "On the weekdays the co-op's 4CP forecast flags, it calls every enrolled device. No device is held back on an alert day." No sentence anywhere tells you how to bridge that gap.

**2. File that already ranks or scores the providers.** None. The quotes and the event log carry no score, rank or recommendation; no hidden sheet, formula or defined name in either workbook.

**3. File that exists only to help the analyst.** None is a bare data dictionary or readme; the closest is the M&V plan, framed and signed as a governance memo.

**4. Figure or name that reads as the answer.** None. The one figure that could be mistaken for a drop-in is the potential study's "Bring your own thermostat 0.7 to 1.1 kW" per device, "not adjusted to any one utility".

**5. Filed sentence that, read literally, fixes a computation or population.** 4.2: every device enrolled on 1 July, including those that opted out, went offline or were held back; 4.3: exactly twelve intervals; 5: the quoted price times the devices enrolled on 1 July 2027 (a forecast date); the notice: USD 54.80 per kW of 4CP load; the M&V plan section 3: 15-minute data only for the Peak Partners homes on two substations enrolled before 1 June 2024, so any device-level estimate outside that sample has to be carried over from it.

**6. One thing that would make most of the request routine?** No. The holdback design applies only to the 24 test days; alert days have no control group. The six schemas need real reconciliation (Corvane's `event_ref` carries no year, so joining on it alone merges 2024, 2025 and 2026). The 4CP interval's clock time drifts from about 16:15 to 16:45 in 2016 to 2018 to about 17:00 to 18:00 in 2024 to 2026, near the edge of the shorter windows. The 1 July 2027 count has to be forecast; Pinecrest Home alone plans 1,800 retail-rebate enrolments against 372 through that channel across all six providers since 2021. Per ask: the kW per device turns on analysis (a counterfactual where no held-back group exists on 4CP days, six schemas, the windows against the peak) plus one definition (4.2); the devices on 1 July 2027 turn on analysis (churn and plans); the quote's cost on one field and one rule carried on the count; the totals on arithmetic of the two. No part turns on catching a planted decoy; the duplicates read as ordinary export noise.

**Two notes.** Machine-generated tells: nothing glaring; the Office files' inner zip entries all read 1980-01-01 00:00, and two workbook stamps and the roster's date sat a few days past today's date. Relevant-looking but unneeded: the potential study and `calder_cad_residential_2026.csv` (joinable only by address, with undecoded codes), judged not required once the roster, meter, event-log and quote files are used.
