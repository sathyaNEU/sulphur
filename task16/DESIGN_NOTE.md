# task16: which reason families Quellstein Paket's assistant keeps taking first through the 2026 peak season

## Draw

Subdomain: General Statistics & Data Science
Analysis type: Data Extraction & Conformation (ETL / Pipeline Build)
Answer shape: A reconciled table plus findings (each reason family's expected resolution rate with its range and its
  designation, tied back to a linked contact record that reconciles to the telephony and case totals)
Weight: assembly: most of the work is building one contact record that can be trusted across four channel logs and
  estimating the follow-ups that record cannot see, then carrying it to a season whose conversations have to be
  built from its parcels; the last two live builds lean on investigation (task18) and modeling (task1), and
  architecture 1 of this slot leaned on investigation
Data-native sentence: a customer who is not helped comes back through whichever channel is open, and each channel
  loses sight of the consignment in its own way (the telephone line stops asking for the tracking number when its
  queue is long, a written case reaches the extract only once it is closed), while the season being planned draws
  its conversations from parcels in proportions set by how often an on-time, a late or a held parcel makes its
  recipient ask at all, less whatever the new delay alerts stop
People: Helena Neumann, Simon Pertl, Theresa Jovanovic, Alena Blümel (guard.py names --geo Austria --seed 1602)

Architecture 2, drawn 2026-11-11 after architecture 1 was spent on the platform (`runs/arch1_triage.md`). The careful
but hurried column is calibrated to that run: it reads every file and every document, reconciles record counts,
executes anything a document files, compares candidate methods by held-out error, fits any pattern one table shows,
validates on held-out groups and resamples clusters. So no result here is priced on a pattern one table shows, a
choice a hold-out settles, or a fact a document files. The priced results are estimates whose omission the data in
hand cannot flag: who the season's conversations will come from, what an intervention the plan switches on does to
that, and how far a day's luck moves every family together.

The world. Quellstein Paket is an Austrian parcel carrier with ten depots. Its contact division runs a chat
assistant, live chat, a telephone line with an IVR, and written cases (web forms and e-mail). The division's service
standard KS-07 counts an assistant conversation as resolved when no further contact is made about the same
consignment, through any channel, within 168 hours of its end, and makes a reason family assistant-first for a season
when its expected resolution rate, for the version then in service and given the season plan, is at least 75 per
cent. Version 3 of the assistant went live on Monday 28 September 2026. Every export is cut on Monday 9 November
2026, 00:00; the season plan covers 16 November 2026 to 3 January 2027 and peak planning closes this week. As-of
date for `leak.py`: 2026-11-09.

Guard WARNs answered. `overuse.gate_g` (method or model selection in six of the last twelve): the label is the
honest one, because each estimate has a shortcut and a sound form and the data in the pack say which (the keyed
calls and the advisers' tick for the capture, the backlog counts for the open cases, the pilot depots for the
alerts, the plan's parcels and the contact rates for the mix); nothing here is a forecast the past does not pin.
`repeat.decision` (a designation set, as task1's last build): KS-07 4.2 makes the answer a set of families by
construction; the shape differs (a reconciled table by family, no cap, no ranking) and the question asks how well
the assistant will do. `test.same_driver_older` is differentiated on the card against mark196 and task6's second
architecture. `voice-check.py` WARN (the deliverable set, a workbook and a memo, at 24 per cent of prompts against a
20 per cent cap): the decision is taken from a table of ten families and a one-page recommendation, the two files a
planner would send; the question form was redrawn from which to how well.

## Deep reasoning

Task type: Data integration, record linkage & entity resolution
Domain test: every result is a record-linkage and missing-data quantity: a linked record reconciled to control
  totals, events the link cannot see restored by the inverse of a capture probability that moves with load, open
  cases completed from a count at another grain, a rate standardised to a target population whose mix is exposure
  times a class-specific contact rate, an intervention's effect on that rate from a staggered roll-out, a range that
  carries day-level dependence. The field's analyst links, estimates what the link misses, and says what the linked
  record supports about a population it did not sample.
Swap: "which wards keep the triage assistant through winter under the 75 per cent rule" still parses as a sentence,
  but the tracking-number key keyed in an IVR, a bypass under queue load, a case backlog by days open, parcels
  generating conversations by delivery outcome and delay alerts cutting that rate all stop meaning anything: the
  results are this record system's, not a rate looked up in any field.
Where the weight sits: the heaviest results are R6 and R7. The season's conversations do not exist yet and no file
  holds their mix; it has to be built from the plan's parcels, the daily service record and conversations joined to
  consignments, with the alerts' effect measured first. The work is long because it joins five files at three
  grains (conversation, consignment, depot-day) before a single rate can be weighted.
Layer 1: the telephony export has one row per leg of a transferred call and carries the advisers' callbacks, in UTC
  across the end of daylight saving time; customers type tracking numbers with spaces, lower case or
  no prefix, and the IVR takes digits only; three code lists (intents, wrap-up codes, case categories) map to the
  ten reason families; advisers open cases of their own beside the customers'; about one conversation in eleven
  concerns no consignment. Each is what the producing system does, each is cleaned the same way by any careful run,
  and none decides a result.
Not one thing: the strongest single piece is the season mix (R6). A run that nails it and leaves the alerts
  unmeasured hands back Delivery day and time (74.2 for 78.0) and misses six of eleven rates; one that also measures
  the alerts but ranges by resampling conversations files ranges a third as wide as the record supports; one that
  does all of that on the linked record alone keeps Missed delivery and redelivery and Damaged parcel.
One-fact test: "the plan turns the delay alerts on at every depot: measure what they did to contacts at the pilot
  depots" rescues R5 alone (1 of 9) for the careful pass, which still carries October's mix into the season; the
  season-mix sentence rescues nothing whole, because the alerts are still unmeasured. Agrees with the Effort test's
  Largest single hint.
Not semantics: every field, unit and clause read correctly (168 hours from the end, any channel, version 3, the plan as given, KS-07 5.1 and 5.2 on what the telephone and case records hold) still leaves the
  careful pass at 79.9 per cent for all families against 75.5 and one family on the wrong side, because nothing
  read tells how many conversations a late parcel generates or what an alert does to that.
Not rule application: KS-07 files what counts as a contact, when a conversation is resolved, which conversations a
  rate covers and the 75 per cent test. No filed procedure restores an unkeyed call, completes an open case, builds
  a season's conversations from parcels, measures the alerts or sets a range; once every filed rule is applied the
  analyst still has all five estimates to make.
Estimand: population, outcome, window and unit of the resolution rate in KS-07 3.1 to 3.3 (assistant conversations
  that concern a consignment, in a reason family, that ended in the period, at least seven days
  before the cut; resolved when no further contact about the same consignment through any channel within 168 hours
  of the end); what a contact is in 2.1 (transferred calls one contact; Quellstein's own calls and adviser-opened
  cases not contacts); the comparison and threshold in 4.2 (the expected rate for the season, for the version then
  in service, given the season plan, at least 75 per cent); the range in 4.3 (90 per cent, for what the record
  supports, the plan taken as given); what the telephone and case records hold in 5.1 and 5.2. The release note
  files that version 3.0 stays in service through peak. Members not yet observed: the season's conversations, which
  4.2 puts in the population through the plan.
No decoy: no memo, draft, dashboard or stakeholder figure carries a rate or a set; the pack ranks no family on
  resolution anywhere. The survey export answers another question (whether the reply answered the question asked)
  and KS-07 defines resolution by further contact.
No replay: no result re-derives a published figure; the only published totals (telephony's weekly calls, the case
  team's weekly flow) are control totals the cleaned record must meet, and it meets them exactly.
Pinned: every result's rivals are run on the built pack by `results.py` (nine sound variants: the capture share by
  queue and bypass state, week, day, hour or wait, or one share; open cases by day or week raised; the alerts read
  as one effect, class by class, or against version 3 weeks only) and `checks.py` asserts each lands inside every
  band; the hurried routes land outside where they are priced. Truth is the simulation's own account of every
  follow-up, and the golden sits within 0.8 of it for all families.
Run forecast: R5 (method shortcut: the alerts noted as a plan fact and left unmeasured), R6 and R7 (unfinished
  chain: rates by delivery outcome found, then October's mix or the plan's parcel shares carried forward; or narrow
  look, the season treated as more of the weeks observed), R8 (self-confirming check: a bootstrap over
  conversations, which confirms a range a third as wide as the days support), R9 (falls with R7). A hurried run
  also loses R2 or R3 (dismissed own evidence: unkeyed calls or open cases named as a limitation and left out).
Strategy label: WORKS IN FORM (the lessons are the atlas's "a biased screen and a small sample combined" and
  "carry the split into volume", in a structure no entry has)
Depth level: 5 on the client's depth scale: five independent judgments (unkeyed telephone follow-ups, open written
  cases, the season mix by contact rate, the alerts' measured effect, the day-level range), each moving different
  families across the 75 per cent line; `effort.py` counts five distinct wrong sets over eight shortcuts, and the
  set holds under all nine sound variants
Lesson: a rate measured on the conversations a system happened to have is a rate for that mix of customers; the
  population a plan will generate has to be built from exposure and contact rates before any rate is carried to it,
  and what a record cannot link is estimated, not dropped. No build on file carries a linked record to a population
  generated by a plan.

## Results chain

| ID | Result (checkable) | Area | Pinned by | Band | Hurried analyst | Depends on | Graded as |
|---|---|---|---|---|---|---|---|
| R1 | the linked record: 30,745 version 3 conversations seven days old, 4,941 followed by a linked contact, 83.9 per cent resolved on the record alone | assembly and reconciliation | KS-07 2.1, 3.1 to 3.3; cleaned calls equal telephony's weekly summary (72,868) and cases plus backlog equal the weekly flow (28,101 + 2,743 = 30,844) | conversations 30,591 to 30,899; rate 83.5 to 84.3 | method shortcut: joins the tracking number as each system wrote it and loses the keyed calls and a fifth of the typed numbers; every careful run brings it to one form (earned) | - | Ask 4 |
| R2 | 40.7 per cent of telephone follow-up calls carry no tracking number (1,657 keyed stand for 2,793) | missingness and measurement | KS-07 5.1; the share of consignment calls keyed by queue and bypass state; the advisers' tick as a second reading (1,444 against 1,473) | 36.0 to 46.0 | dismissed own evidence: a run in a hurry names the blank numbers as a limitation and files the linked record (0 per cent restored) | independent: the call export | Component 1 |
| R3 | about 235 written follow-up cases still open at the cut | missingness and measurement | KS-07 5.2; the backlog report's open cases by queue and days open against the closed cases raised the same days | 188 to 282 | method shortcut: completes on the summer's closing times (77), or takes the extract as the channel (0) | independent: the case extract and backlog report | Component 2 |
| R4 | 80.4 per cent resolved under version 3 with both restored | synthesis | R2 and R3 on the linked record; within 0.8 of the simulation's truth | 79.6 to 81.2 | unfinished chain: restores one of the two (82.9 or 81.0) | R2, R3 | Component 3 |
| R5 | the delay alerts cut conversations per late parcel by 41 per cent | causal reasoning | the season plan's roll-out dates; pilot depots against the other seven, after against before 12 October, class by class (the simulation's value is 42) | 35 to 48 | method shortcut: notes the alerts as a plan fact and leaves them unmeasured | independent: conversations joined to consignments and the daily service record | Component 4 |
| R6 | late and exception parcels generate 56.4 per cent of the season's conversations, about 10,700 a week | forecasting | KS-07 4.2 (given the season plan); plan parcels by service level times conversations per parcel by delivery outcome, late classes cut by R5 | share 53.4 to 59.4; 10,000 to 11,400 a week | unfinished chain: carries October's mix (39.7 per cent) forward, or uses the plan's parcel shares as if parcels were conversations | R5 | Component 5 |
| R7 | each family's expected rate over the season (ten families and all together, 75.5) | forecasting | each family's rates by delivery outcome (restored) weighted by its own season conversations | per family 1.0 to 2.6 points either side; all families 0.9 | narrow look: the weeks observed stand for the season (79.9 for all families, 6 of 11 cells outside their bands) | R2, R3, R6 | Ask 2 |
| R8 | the 90 per cent range: plus or minus 1.20 points for all families | uncertainty | KS-07 4.3; the daily rate moves 11 times as much as independent conversations would, so whole days are resampled | each half-width 0.65 to 1.6 times the golden's | self-confirming check: resamples conversations and confirms plus or minus 0.34 | independent: graded on the width | Ask 3 |
| R9 | keep five families (Delivery day and time, Redirect and address, Pickup point and collection, Returns and labels, Charges and refunds), hand back five | synthesis | KS-07 4.2 on R7's rates; every family 2 points or more from 75 and no range reaching it | exact | unfinished chain: keeps Track and trace on October's 76.5 | R7 | Recommendation |

Carry-forward: R2, R3 and R5 each read an input of their own (the call export, the case extract and backlog, the
pilot depots), so a run that slipped on one still earns the others. R4 falls with R2 or R3. R6 falls with R5. R7
needs R2, R3 and R6 together and R9 falls with R7. R8 is graded on the range's width, which the resampling sets
whatever rate it surrounds. No analytical result carries more than three of the other eight.

## Hidden factor record

| Factor | Real or constructed | Only in deciding units | Found by | Fix depth | Verdict |
|---|---|---|---|---|---|
| Tracking numbers missing from calls when the IVR bypass runs | constructed by the simulated queue (every queue, every week: a third or more of consignment calls unkeyed in all 14 weeks) | no: all four queues, all ten families; decides Missed delivery and redelivery and leaves Returns and Missing parcel where they were | filed in KS-07 5.1 and visible as blank numbers | modelling: a capture probability by queue and bypass state, applied at the conversation, checked against the advisers' tick | keep (priced Right for the careful pass) |
| Written cases reach the extract only when closed, and the queues slowed in October | constructed by the simulated case team (every queue has open cases at the cut) | no: all five queues; decides Damaged parcel, moves Customs 2 points and decides nothing there | filed in KS-07 5.2; the counts reconcile only with the backlog in | modelling: each closed case weighted by the open ones of its own day, since the closing times moved | keep (priced Right for the careful pass) |
| Recipients ask far more often when a parcel runs late or is held (12 per 1,000 on time, 169 per 1,000 two or more days late) | constructed by the simulated recipients, at every depot and in every week | no: every family with both kinds resolves worse on late parcels; decides Track and trace, moves six other families without deciding them | modelling: needs conversations joined to consignments and the daily service record (two files, two grains) | modelling: an exposure-weighted mix for a population that does not exist yet | keep |
| Delay alerts cut contacts about late parcels where they ran | constructed as the plan's own roll-out (three depots from 12 October, all from 16 November), both late classes | no: three depots, both classes, every family; decides Delivery day and time only | the plan's Notifications sheet names the roll-out; the effect has to be measured | modelling: after against before, pilot against the rest, class by class | keep |
| Good and bad days move every family together (daily dispersion 11.2) | constructed as day effects on every conversation | no: all 35 days, all families | diagnostics: the daily rate against its binomial spread | modelling: whole days resampled, every step redone | keep |

No factor sits only in the units it decides, each shows across the data the way its process puts it there, and for
each the fix is an estimate with a tempting shortcut, not a filter. `checks.py` asserts each footprint and a family
on the same side under every route (Missing parcel, Returns and labels).

## Effort test

| Result | Quick pass | Careful but hurried | Thorough |
|---|---|---|---|
| R1 the linked record | Right | Right | Right |
| R2 telephone follow-ups with no tracking number | Missed | Right | Right |
| R3 written follow-ups still open | Missed | Right | Right |
| R4 the resolution rate achieved under version 3 | Missed | Right | Right |
| R5 the delay alerts' effect | Missed | Missed | Right |
| R6 the season's conversations | Missed | Missed | Right |
| R7 each family's expected rate | Missed | Missed | Right |
| R8 the 90 per cent range | Missed | Missed | Right |
| R9 the families kept and handed back | Partly | Partly | Right |
| Roughly | 1.5 of 9 | 4.5 of 9 | 9 of 9 |

Measured by: .claude/skills/stumping/effort.py on generator/effort.json
Largest single hint: "the plan turns the delay alerts on at every depot: measure what they did to contacts at the pilot depots"; rescues 1 of 9 results
Pair estimate: 46.7

The careful pass is graded up on purpose: it restores the unkeyed calls (at the week's capture share) and the open
cases (from the backlog), because architecture 1's run did every such thing a file made visible, and KS-07 files
both facts. It then carries the weeks observed into the season and ranges by resampling conversations. Were it also
to build the season mix from contact rates and leave only the alerts unmeasured, it would earn R1 to R4 and five of
eleven rates, and the alerts sentence would then rescue R5, R6, R7 and R9 (4 of 9); that harder reading of the
careful pass is the risk this build carries, and the range (R8) and the alerts' measurement are what it still has
to do.

## Data provenance

Source: generated by `task16/generator` from a simulated process
Behaves like the real thing: the generator simulates parcels due by depot and day running on time, late or into an
  exception (with weekday shape, growth, depot noise, a week of storms in August and a hub move in October that
  eases unevenly), recipients contacting the carrier at a rate set by how the parcel ran, each contact handled by
  the assistant or an adviser, an unhelped customer coming back after a lognormal delay through a channel that
  depends on the reason, a telephone queue staffed to the ordinary weeks whose IVR offers a bypass when load passes
  its staffing, advisers ticking a previous-contact box about three times in five, and a case team whose closing
  times stretch when its queues fall behind. Every file is an export of that record as its system would write it.
Genuine patterns: (1) weekday and time-of-day shape in every channel, with Sunday closures and a slow growth trend
  (2) two network disruptions of different kinds and sizes (August storms at five depots, the October hub move at
  four) that raise lateness, contacts, queue load and bypass together (3) contact rates and resolution that fall
  with lateness in every family, by different amounts (4) day-to-day common variation in resolution well beyond
  binomial (5) case closing times that lengthen from October and differ fivefold between queues (6) depot
  differences in exception traffic
Problems by process: call legs and callbacks (the telephony platform's row per leg), UTC across the clock change (the telephony platform),
  typed tracking numbers (customers), blank numbers (the IVR bypass and callers without the number), closed-only
  cases (the case system publishes at closure), adviser-opened cases (working practice), parcels still in transit
  at the cut
Breadth: 17 files; 93,417 assistant rows, 81,459 call legs, 23,419 chats, 36,655 closed cases, 163,052
  consignments, 840 depot-days, 14 weekly backlog counts by queue and days open, a seven-week plan by depot; ten
  families by four delivery outcomes by 35 days is where the rates live, and nothing says which join matters

## Template check

Chain signature: assembly-reconciliation, missingness-measurement, missingness-measurement, synthesis,
  causal-reasoning, forecasting, forecasting, uncertainty, synthesis
Question form: how well (how much), then whether it is enough under the rule
Nearest build: task5 (a reconciled table in the same analysis type): there a period total is completed component by
  component from reports not yet in; here a rate is rebuilt from a linked record and carried to a population a plan
  generates, with an intervention measured on the way; the weight (assembly against a hard-to-measure quantity), the
  chain and the shell differ. The abstraction sentence a reviewer could write against task6 ("rates from a sample
  with unequal inclusion and an uncovered part") fails here: nothing is sampled, the record is a census of each
  channel, and the answer is a forecast for a different population.

## Semantic fork table

| ID | Term or convention | Readings | Golden | Ruled out by |
|---|---|---|---|---|
| SF1 | "within seven days" | 168 hours from the conversation's end; from its start; seven calendar days | 168 hours from the end | KS-07 3.1 files it; from the start gives the same rates within 0.6 (asserted), same call |
| SF2 | "further contact" | any later contact on the tracking number; only adviser contacts; excluding handovers | any channel, the assistant included, handovers counted | KS-07 3.1 ("through any contact channel"; a handed-over conversation is not resolved) |
| SF3 | a transferred call | one contact; one per leg | one contact | KS-07 2.1 |
| SF4 | Quellstein's callbacks and adviser-opened cases | contacts; not contacts | not contacts | KS-07 2.1 |
| SF5 | "the same consignment" | the same tracking number after bringing it to one form; the raw string | one form | KS-07 2.2 (identified by its tracking number); the IVR's digits and the typed forms are the same number |
| SF6 | which conversations a rate covers | conversations about a consignment that ended seven days before the cut; every row of the export | the former | KS-07 2.2 (contacts that concern no consignment are outside the standard), 3.2, 3.3 |
| SF7 | the version | builds 3.0.0 and 3.0.1 together; 3.0.1 alone | version 3 | KS-07 4.2 (the version then in service); the release note (3.0.1 changes no answers; 3.0 in service through peak) |
| SF8 | a conversation's reason family | its intent's family; the family of the contact that follows | its intent's | KS-07 2.3 |
| SF9 | "expected resolution rate for the season" | the rate over the conversations the season plan generates; October's rate; rates weighted by parcels | over the season's conversations | KS-07 3.2 defines a rate as a share of conversations and 4.2 conditions on the season plan; October's mix contradicts the plan's service levels; parcels are not conversations |
| SF10 | "given the season plan" and the alerts | alerts on at every depot as the plan's roll-out states; ignored | as the plan states | KS-07 4.3 (the plan taken as given); the Notifications sheet |
| SF11 | "at least 75 per cent" | on the expected rate; on the range's low end | on the expected rate | KS-07 4.2; no family's range reaches the line, same call |
| SF12 | the 90 per cent range | what the record supports (estimation); the season's own week-to-week spread | what the record supports | KS-07 4.3 |
| SF13 | delivery outcome | the network system's class of the consignment at the cut | that class | the consignment record's own column; the plan's service levels use the same four classes |
| SF14 | calls with no tracking number | contacts that may follow a conversation; not contacts about the consignment | contacts | KS-07 2.1 (a call answered by an adviser is a contact) and 5.1 (the record identifies the consignment only where keyed) |
| SF15 | cases not in the extract | contacts from the moment they are received; contacts once closed | from receipt | KS-07 2.1 (a written approach, held as a case) and 5.2 |

## Closure table

| Axis | Closure |
|---|---|
| 1 | Population: KS-07 2.2, 3.2, 3.3 (conversations about a consignment, ended seven days before the cut); the season's conversations are in it through 4.2 |
| 2 | Unit of account: the conversation (3.2); a transferred call is one contact (2.1) |
| 3 | Attribution window: a conversation belongs to the period it ended in (3.2); C1, 61 conversations end within an hour of the window's edges and move no rate |
| 4 | As-of dating: every export is cut Monday 9 November 2026, 00:00; delivery outcome as the network system holds it then |
| 5 | Version basis: version 3, builds 3.0.0 and 3.0.1 (4.2 and the release note) |
| 6 | Denominator: conversations in the family that ended in the period (3.2) |
| 7 | Weighting: each family's rates by delivery outcome weighted by its own season conversations, forced by 3.2 and 4.2; the parcel-weighted reading is ruled out by 3.2 |
| 8 | Window length: the alerts' before period from 3 August or from 28 September gives 41 and 39 per cent, inside the band (C1) |
| 9 | Boundary inclusivity: follow-ups at or after the end and up to 168 hours; C1, nothing sits on the edge to the second except handed-over chats, which 3.1 counts |
| 10 | Rounding path: rates stated to 0.1 and the rule applied to the stated rate; every family is 2 points or more from 75 |
| 11 | Tie-break: none needed; no two readings tie at the line |
| 12 | Maturity and censoring: 3.3 files the seven-day rule for conversations; open cases are completed, not waited for (5.2) |
| 13 | Order of operations: restore, then rates by outcome, then weight; weighting first and restoring after gives the same figures (linear) |
| 14 | Row order: no step depends on file order; the latest conversation a contact follows is by end time |
| 15 | Duplicate resolution: no export repeats a record; a transferred call's legs are one contact (2.1) and its first leg carries the IVR's reading |
| 16 | Identity normalisation: the tracking number in one form (spaces, case, prefix); the raw string misses 20 per cent of typed numbers and every keyed call |
| 17 | Netting against gross: not applicable; a conversation is resolved or not |
| 18 | Dimensional units: rates in per cent of conversations; contact rates per parcel; never mixed |
| 19 | Code and status semantics: the three code lists; the IVR path codes are read from the rows (KEYED, NO_ENTRY, BYPASS) and no document glosses them |
| 20 | Integerisation: none graded; counts are stated whole |
| 21 | Clause scope: 4.2 applies family by family; the all-families rate is reported, not tested |
| 22 | Forward window contents: the season plan workbook ships the parcels, service levels and alert roll-out for 16 November to 3 January |

## Literal reader

KS-07 3.1 to 3.3 executed word for word on the cleaned exports gives the linked record (83.9 per cent). 5.1 and 5.2
say that record does not hold every telephone or written contact, so a literal reader cannot stop there: the
contacts 2.1 defines include calls with no keyed number and cases not yet closed, and the files give the capture
share and the open counts to estimate them (80.4). 4.2 executed word for word asks for the rate over the season's
conversations given the plan; 3.2 makes that a share of conversations, so the plan's parcels have to become
conversations, which only the contact rates by delivery outcome can do, and 4.3 takes the plan's alert roll-out as
given, which only the pilot depots can price. Every literal reading therefore gives the golden's quantities; the
hurried figures come from an easier method on the same estimand (the record as it stands, October's mix, no alerts,
conversations resampled), never from another reading. No shipped sentence names a method, a weight or a comparison.

## Prompt contract

A voice rewrite may not drop or change: the question (how well the assistant will resolve each reason family's
conversations over the peak season, and whether that is enough under the 75% rule for it to keep taking the family
first); the forcing fact (peak planning closes this week); for each reason family and for all together, the expected
resolution rate with a 90% range, in percent; whether customers are offered the assistant or an adviser first; a
spreadsheet that shows how the figures are built up from the contact records; a one-page memo with the
recommendation. It must never add: a rounding instruction, a method or comparison (weighting, linking, alerts,
delivery outcome, resampling), a warning, an attached file's name, a role, a count the data hold (the number of
families, depots or weeks), the go-live date or any other fact the files carry.

## Pre-ship check

Written at stage 5 against the built pack.

## Tried and rejected

- A bridge between a projection and a disappointing large run (Comparative Analysis & Explanation, attribution): the
  honest strategy label is decomposition and attribution, which `ban.strategy` holds against task1 in the window; not
  relabelled, the draw moved to a forecast.
- Vendor labels as the only stump (the legacy-map route at 20 per cent error): on the real runs a pass that finds the
  expert-labelled development items and adds a per-route cost to a straight line still names the right configuration,
  so the pick turned on one thing (the yardstick).
- A contractor pool of 512,000 examples in the shortlist: the configuration on it wins by 0.07 under every sound
  forecast and under the straight line too, so nothing but the yardstick was priced.
- The dev split scored by route as separate logged scalars: a column would hand over the yardstick; the trainer logs
  one development loss and the per-item scores of each final checkpoint ship as the lab's error-analysis dump.
- A reference entry the proposal has to beat: the nearest configuration sat within 0.011 of any threshold that
  separated the shortlist, a margin the forecast cannot carry; the ranking is graded instead.
- A vendor label audit file (re-interpreted samples with agreement rates per route): with the routes' error rates on
  file a hurried pass avoids the map route by rule of thumb and wins the pick with no analysis; the routes' quality is
  left to what the runs show.
- The map route at 16 per cent error with a trial that mixed all three routes: the careful pass, calibrated to the run
  record (one scaling-law regression over every run, a floor or a quadratic chosen on held-back runs), named the right
  configuration and lost only the figures that hang on the bend, so the pick was earned by reflex and the pair priced
  near 70. Measured on the real runs at 10, 12, 14 and 16 per cent: at 12 the all-labels configuration truly scores
  0.660 against 0.6335, the pooled curve puts it first by 0.011, and every analysis that separates the level from the
  routes' costs names the right one by 0.012 to 0.039. The map route went to 12 per cent and the mixed trial out (the
  contractor's lot arrived in the pilot's last week).
- The pilot's largest runs left unfinished when the allocation ended, to be completed along the schedule: on a cosine
  schedule the logged loss at 70 to 90 per cent of a run is within 0.005 of its final value, so taking the last value
  as it stands is nearly right and the completion prices nothing.
- A compute cap that binds (a configuration that does not fit the slot): width buys under 0.006 a doubling at the
  expert pool, so no configuration that needs more hours is worth shortlisting; the hours stay texture (all four fit).
- A threshold on an extrapolated figure (lots 2 to 4 funded only if they lower the loss by a stated amount): the gap
  between the bent and the pooled forecast at one doubling past the pilot is 0.02 to 0.03, the size of the forecast's
  own error, so no line separates the right answer from the shortcut with margin.
- A separate result for what widening buys at 512,000 examples, and one for what the tuned learning rate buys there:
  each is one matched pair in the pack, a group-by the runs make unprompted, so each is earned and prices nothing.
- Nine asks on bands set by four members of one method family, with the held-back gap, the run counts and the widest
  configuration's learning rate graded (the first cut of this architecture, judged NOT_DETERMINISTIC on a narrow
  footing, FIX_NOW): the judge's own derivation (a level of its own at every total with the costs from contrasts
  between mixes, every run on the carried loss) named B and landed outside the bands on the contractor's cost
  (0.0023 against 0.0000 to 0.0020), the 512,000 level (0.599 against 0.600 to 0.613), A and the range, and the
  held-back gap proved a property of the solver's own curve (0.004 to 0.027 across sound ones), not a figure to
  grade. The bands were reset on a family of 49 run analyses that holds the judge's readings and the two bounds on
  what the examples past the largest trial return; the gap, the counts and the rate became working. With nine asks
  the careful pass then earned five and priced at 57 to 61, so the two reflex asks went and six results are graded.
- The width step priced through A (the pooled width term's 0.679 against a band topping at 0.672): a width curve on
  the carried loss gives 0.68 to 0.71 and the benchmark's own 512-wide scores less a step 0.663, with the truth at
  0.662, so A cannot be banded tighter than 0.650 to 0.720 and prices nothing.
- The level at or under the pool taken from the expert-label runs, the ladder put on the trials' rate, as the golden's
  own reading of the routes (contractor 0.0010 a tenth, B's range 0.609 to 0.638): the judge's second pass read the
  costs from mixes at one total (0.0018 to 0.0024) and the truth runs put them at 0.0017, so the same-total reading
  became the golden's (0.0020, range 0.604 to 0.645) and the first reading the other member the bands hold.
- The levels sentence priced at two results, with a least-squares floor fixed as the hinted pass's continuation:
  given a level at every total and left to choose its own form on the runs held back, the careful pass lands C and
  D as well, so the count is three of six and the note says so.
- Architecture 1 as shipped (the Norwegian group's scale-up forecast from a staged pilot sweep, six results, name
  configuration B at 0.625): spent on the platform on 2026-11-11. One run earned every graded result in 28 minutes
  (`runs/arch1_triage.md`): it compared two candidate calibrations by leave-one-out error, read the slowdown in
  matched cells (0.0471 then 0.0274 a doubling at one mix), fitted a response surface with a fitted breakpoint and
  validated it on held-out configurations, and resampled configurations and calibration pairs separately. The six
  results were one runs-by-settings table that one flexible fit absorbs, the asks named the intermediate quantities,
  and bands wide enough for every sound method (C from 0.648 to 0.689) graded nothing. No tighter honest band fails
  that run, so the world is spent: re-rooted to another world, dataset and shell as architecture 2.
- Architecture 2, a tenth result for what version 3 changed against version 2 on like conversations: on the built
  pack the linked comparison read 6.2 points, the restored one 7.1 and the like-for-like one 6.9, so no reading
  separated from another and the result priced nothing; cut, with version 2's weeks kept as the alerts' before period.
- Architecture 2, the backlog report in weekly age bands: a closed case raised early in the last week is both likelier
  closed and likelier to follow a conversation inside the seven-day-old window, so the weekly share overstated the
  open follow-ups by half (288 added against 182 true, Damaged parcel 4.7 points low). The report counts open cases
  by days open, as an ageing report does, and each closed case stands for the open ones of its own day and
  neighbours.
- Architecture 2, asks for the season's conversations a week and the adviser contacts they pass on: an ask for a
  volume built from the plan's parcels is the first half of the season mix, asked for, which is how architecture 1
  handed over its decomposition. The volume is a Critical Component and the prompt asks only for rates, ranges and
  the designation.
- Architecture 2, telephone follow-ups priced on the grain of the capture share (a pooled or weekly share against the
  quarter-hour's): on the built pack a pooled share moved no family by more than 2.0 points, inside the band a
  sound rebuild needs, so the grain prices nothing; the result is priced Right for the careful pass and the hurried
  failure there is leaving unkeyed calls out.
- Architecture 2, the telephone and case exports as silent partial extracts (calls with no tracking number absent,
  open cases absent, nothing filed): the determinism spec needs a source the golden completes to say it does not
  hold every member, and a silent partial extract is the planted defect the client names. KS-07 5.1 and 5.2 file
  both facts, the unkeyed calls are rows with a blank number, and both restorations are priced Right for the careful
  pass.
- Architecture 2, a common shock every twelve calls after a telephone contact (two or more calls per conversation in
  one in eight): a conversation with two calls and one keyed was overweighted and Track and trace's hidden
  follow-ups came out 24 per cent high; an adviser now settles most matters at the first call, as the summer weeks'
  record would show, and the weight is right to 3 per cent.
- Architecture 2, test rows and a repeated block as Layer 1 (the product team's tester sessions, a telephony test
  queue, ISO week 39 carried twice by overlapping weekly exports): the stage 4 leak reader read the test queue as
  possibly planted, and test rows and a copied block are the first two items on the client's list of planted
  defects. All three are out of the generator, with the sentence of KS-07 3.2 that excluded staff conversations; the
  backlog report now lists only the ages that have open cases (the reader read the zero-filled grid as generated),
  the depot list carries the hub and its date in two columns, and the plan's notification sheet has four short
  columns. No graded figure moved.
