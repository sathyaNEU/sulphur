# leak check, task7

**Verdict: REVIEW.** 16 files read, 121 golden figures and 1 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: architecture, golden, buildings, record, controls, insulation, carried, million, heating, author, default, season, landed, seasons, patients, building, report, family, graded, reflex, careful, sentence, december, spread, lived-in

## 3 answer figures in the pack (REVIEW 4)
- **REVIEW** `VO-1_voltage_optimization_program_standard.pdf`: golden figure 115 appears: ...the feeder at or above 114 V plus a 1 V margin (115 V on the 120 V base) in that hour, and never by m...
- **REVIEW** `VO-1_voltage_optimization_program_standard.pdf`: golden figure 4.8 appears: ...) in that hour, and never by more than 4 percent (4.8 V on the 120 V base). 2.4 Energy saved is valued...
- **REVIEW** `annual_report_2025_system_statistics.pdf`: golden figure 6.1 appears: ...Wh Retail sales 1,132,800 MWh Distribution losses 6.1 percent of energy delivered Distribution feeders...
- **REVIEW** `vo_trial_protocol_2026.pdf`: golden figure 4.8 appears: ...lator's schedule lowers its output by 4 percent (4.8 V) from midnight, returning to normal at the foll...

## 9 dates after the setting (INFO 1)
- **INFO** `-`: no --asof given, sweep skipped (pass the fiction's as-of date)

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 12 client quality check (INFO 2)
- **INFO** `-`: 16 usable files (10 or more required)
- **INFO** `-`: 2 file categories: document, spreadsheet (2 or more required)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 4 design-note vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)


## Solver's-eye read

Architecture 11, 2026-11-12: one isolated reader (Sonnet, medium) on fresh copies of prompt.txt and the 19 files under
target/, briefed with the six questions only. Main thread's rulings: questions 2 to 4 none; question 1's sentences are the
filed WHAT that closes forks SF3, SF4, SF5, SF8 and SF13 (the planning kVA convention, the records' corrections, a departed
charger as metered, each session finishing by its unplug time), none naming a deciding move, except EV-4 4.3 ("a transformer
counts at its chance of being over its limit"), which points a careful run at simulating random starts and so toward the
night-by-night replay: reworded in the generator to the estimand alone ("an option's cost is its expected cost for the
year"); question 5's literal readings (DPS-7 2.2, the proposal's 1 November 2026 basis, EV-4 4.1) are the golden's;
question 6 finds no one thing. Its note on the monitors' kW to kVA ratio led to a realism fix: where rooftop solar exports at
midday the net kW is negative, and the generator had written a negative kVA; kVA is now the magnitude over the power factor.

### The reader's answers (condensed, its own words where quoted)

1. HOW sentences: DPS-7 2.2 ("load in kVA is that demand in kW divided by 0.95, whether or not the transformer is
   monitored"), DPS-7 4 (connectivity from the GIS as corrected by work orders, nameplate from the register as corrected by
   change-outs; the register is genuinely stale for some change-outs), EV-4 4.2 (a departed charger taken as metered),
   EV-4 4.3 (a random option's transformer at its chance). WHAT sentences: DPS-7 2.1 and 2.3, EV-4 3 and 4.1.
2. No file ranks or scores the options; the proposal gives two products' fees only.
3. No file exists only to help the analyst.
4. Nothing reads as an answer; the fees are inputs.
5. DPS-7 2.2 (every planning kVA is kW / 0.95), the proposal (fees on the chargers enrolled on 1 November 2026), EV-4 4.1
   (each covered charger's own July and August sessions replayed under each option, each ending by its real unplug time).
6. No one thing: connectivity and nameplates, each option's mechanism, a resolution mismatch (few monitors, hourly meters),
   meter exchanges inside the window, and random against queued starts with no precedent for Sequence; the parts turn on
   analysis except the enrolled count and the register correction, which are reads of a stated rule.
Notes: nothing machine-generated or after the as-of date; the state's EV registrations and the net-metering list read as
plausible but unneeded; the meter exchange log is load-bearing.

### The second reader, on the cut after the fixes (2026-11-12)

A fresh isolated reader (Sonnet, medium) on new copies of prompt.txt and target/, asked the same six questions with EV-4
section 4 and the random option singled out. Rulings: questions 2 to 4 none; question 1 quotes the filed conventions
(DPS-7 2.2's planning kVA, DPS-7 4's records, the pilot plan 3's footing for the pilot figure, EV-4 3's cost); question 5's
literal readings are the golden's; question 6 finds no one thing, and on the random option it reads EV-4 4.3 ("An option's
cost is its expected cost.") as requiring an expectation that "never says how to form one over a random, non-additive
quantity (a transformer's 15-minute maximum): no sentence anywhere resolves this; it stays open", which is the estimand
filed and the method left to the analysis. Its notes: no negative or out-of-range kVA after the fix; the swaps logged after
the enrolment pause are replacements for enrolled members; the one transformer location in the register and work orders
but in no GIS row is the split whose transfers the GIS has not posted; the state's EV registrations, the weather and the
net-metering list look relevant and are not needed. Nothing to fix.

## Solver's-eye read

One isolated reader (2026-11-13, after the determinism repair that filed the queue's waiting, the ready-by and the
hourly-to-15-minute method), on fresh copies of `prompt.txt` and `target/` only.

1. How the analysis is done: it quotes EV-4 4.1 (the replay's frame: each session keeps its plug-in, energy, charge time
   and unplug; the covered chargers' own charging out of the hourly reads before DPS-7 brings them to the quarter-hour,
   each option's in at the quarter-hour; ready-by at the unplug time rounded down), EV-4 3, 4.2 and 4.3, DPS-7 2.1 to
   2.3 and 4, the pilot plan 1 and 3, and the proposal's product rules and fee basis. Ruling: each is the estimand or a
   convention filed at its authority (the three new ones at the client's direction); none names the moves the results
   price (each transformer's chance of coinciding over random starts, Sequence's rule run on each night's sessions, the
   managed quarter's own settings restored from each charger's own history).
2. A file that ranks the options: none.
3. A file that exists only to help: none.
4. A figure or name that reads as the answer: none (it notes the proposal's "The same as the pilot's managed half", a
   product description, not an answer).
5. Filed sentences that fix a graded figure: the same list read literally (the window, the chargers covered, each
   session's timing, the ready-by, the order of the base's steps, chargers that left as metered, the limit, the factor
   and the 0.95, the nameplate and connectivity, Table 1's costs, the pilot's per-charger every-night footing, the fee
   basis). Ruling: each literal reading is the golden's (checks.py SF1 to SF25); none is a hurried figure.
6. One thing: none. It reads the overload counts as the replay's frame plus "the simulation of each option, including
   Sequence's per-transformer ordering" as the analysis, the pilot change as a causal comparison on the filed design,
   the enrolled count as reading the roster, the flip fee and the call as analysis. Ruling: consistent with the design;
   under the frame the careful but hurried routes still land Stagger with 2 over, Sequence with 3 and own schedules at 44.

REVIEW rulings:
- `board_policy_EV-4_charging_default.pdf`, the call's words (answer-figure sweep): harmless (reader): the governing
  policy names the options and the cost test, ranks nothing and gives no figure.
- `board_policy_EV-4_charging_default.pdf`, stump terms (quarter, carried, quarter-hour, sessions, schedules): harmless
  (main thread): EV-4 4.1 files the replay's frame and none of the three moves.
- `ev_overnight_pilot_plan_2025.pdf`, stump terms (stagger, average, quarter, schedules): harmless (main thread): unchanged
  since the last ship; it files the pilot's design and its per-charger footing.
