# task1: which of Kraanvogel Luisterboeken's January 2027 price rises go ahead, plan by plan

## Draw

Subdomain: Cohort and LTV modeling: retention curves, customer lifetime value (Product Analytics, retention-cohort-lifetime-value-modeling)
Analysis type: Forecasting & Predictive Modeling
Answer shape: A forecast path with bands, plus its drivers (each plan's change in its October 2026 base's 2027 contribution with its band, how many of the base pay on any plan at the end of 2027 and what their counted hours cost in 2027, driven by the first bill's response by plan and region, the return of the subscriptions that stop and the stayers' listening, and the rises that go ahead on top)
Weight: modeling: each plan's 2027 change is the October cohort carried month by month through a response the record ran only in other configurations, with a pool of stopped subscriptions that flows back and a consumption response of those who stay, at a rate per counted hour; task22 sat on assembly and task7 on modeling (overuse.weight answered: a coincident-peak demand response there, a subscription cohort with re-entry and a per-use cost response here)
Data-native sentence: every past price rise reached each subscription first in the 1 December e-mail and then at its first bill of the year, in one region at a time and against a rival scanned monthly, and the billing and listening records show who stopped when, who paid again months later on the same account, who moved down and how much those who stayed listened, so what a 2027 rise does to each plan's base under a remuneration paid per counted hour is in no file until the stops are followed to their returns and the stayers' hours are read against their own past and the other region.
People: Romy Korsman (head of growth), Hugo Brouwer (finance controller, owner of the growth planning guideline), Tara Martens (growth analyst, whose workbook and deck the golden are) (`guard.py names --geo NL --seed 1112`). None appears in the prompt.

Architecture 5, 2026-11-12, on the author's word in the Kraanvogel world (architecture 4's generator restored from 87422aa, extended with a price history by region, the rival's price scan and the response to a rise). Architecture 4 was sent back at stage 4 because its call rested on two record corrections the judge made by reflex; nothing here rests on finding, merging or re-keying a record: the licence merge and the dated profiles are Layer 1 and an assembly result (R2), and the call turns on estimating responses whose reflexive estimates land elsewhere.

Re-designed 2026-11-13 after the author's audit found the repaired cut one trick (one sentence, the crossing, rescued four of five results against the platform run's own route): the stump factorial (stumping Part 3.3, dbb05a5) now carries three stumps, each necessary, none sufficient. The world gained the December price e-mail and its leavers, and the Onbeperkt accounts that add their second profile after a rise; the rival's July 2026 move was removed (its prices are constant); Gezin's 2027 rise no longer passes the rival (Luistr Familie EUR 24.49 in the Netherlands), nor Onbeperkt's (Luistr Onbeperkt EUR 20.49); Flex churns less. The call is Gezin alone.

Repaired 2026-11-12 on the holistic audit of the first cut: its 2027 Gezin rise (EUR 3.50, landing EUR 3.00 past Luistr Familie) and Flex rise (EUR 1.50) lay outside every past rise's size (EUR 0.50 to 1.00, landing EUR 0.20 to 0.50 past the rival), so how a response grows with the rise was open and a dose-scaled reading withdrew Gezin (EUR -49.6 against +5.3); the platform run did so on log-dose scaling. Each 2027 rise is now the plan's own past rise in euros (Flex 9.99 to 10.49, Gezin 22.99 to 23.99, Standaard and Onbeperkt as before), and the rival's July 2026 rise (Luistr Basis 10 uur to EUR 10.29 in both regions, Plus 30 uur in Flanders to EUR 15.59, in the scan) leaves every 2027 crossing EUR 0.20 to 0.50 past the rival, inside the record; the dose forms (in proportion to the rise, on the log of the price ratio, a crossing response half as large again) sit in the golden family and the perturbations and move no call. The call moved with the prices: Onbeperkt alone goes ahead.

Repaired 2026-11-13 on the platform's holistic audit of the reshipped cut (runs/arch5_audit_2026-11-13.md) and the run pasted with it (runs/arch5_run2.md). The audit was right on both counts and the first was worse than it said: Standaard's 2027 crossing had no past crossing of its own, and the golden's carry of the other plans' crossing increments was wrong against the world itself (21.2 extra cancellations and 16.1 downgrades per 100 against a replayed 4.5 to 7.4 and 41.5 to 43.9, since every Standaard account fits Flex while the past crossers' downgrades were held down by profile limits); and Onbeperkt's call turned on one constructed second-profile uplift that one table of profiles per paying account shows. The run made the crossing (with the profile limit of the plan below) and the December leavers unprompted, so both are reflexes (R61, R62) and the cut stood on the uplift alone. The world now runs no 2027 configuration the record never ran: the rival's Plus 30 uur is EUR 16.99, so no Standaard rise ever passes it; the rival's Basis 10 uur is EUR 9.79 in both countries until July 2026, when the rival raised it to EUR 10.29 and brought its Flemish Onbeperkt and Familie to its Dutch prices (all in the scan), so no plan sits above the rival before any rise, both of Flex's past rises passed it from below and Flex's 2027 rise passes it the same way, and passing the rival reads the same whether it means crossing from at or below or simply ending above (the fork the stage 4 judge found on the first repaired cut, pass 3); the price list dates every past e-mail (1 December). The second-profile uplift is gone. Two processes the runs named and waved through now run across every plan: a subscription that stops can take its plan up again on the same account, light listeners soonest and more before the summer (N33); and the account holder listens more for months after the bill at a higher price, the heavier the listener the more, fading (N23, L45). Standaard's rise is EUR 1.50 in 2025, 2026 and 2027 alike. The call is Standaard and Gezin.

## Deep reasoning

Task type: retention cohort lifetime value modeling (Cohort and LTV modeling: retention curves, customer lifetime value), which serves Forecasting
Domain test: every result is a subscription retention-and-value quantity: the base by plan, the first bill's extra cancellations and downgrades, how many stopped subscriptions pay again by the end of 2027, the stayers' extra counted hours, the base still paying and its per-hour remuneration in 2027, and each plan's change in contribution; the growth and pricing analyst's own price-response and LTV work.
Swap: "raise Standaard because many it loses pay again within the year at the new price, hold Onbeperkt because the accounts that stay listen more at EUR 0.40 an hour" makes no sense for a hospital or a factory: there is no plan ladder, resubscription, price e-mail, rival price point or per-hour royalty.
Where the weight sits: R7, each plan's change: the October cohort carried month by month on each subscription's own paying months, listening, country and route through the December e-mail and the first bill (read from the eight past rises by listening band, in proportion to each rise, the downgrades where the profiles fit the plan below), each stop followed to its return (a monthly hazard by listening band, months since the stop and calendar month, fitted on every stop since 2024 at risk until it paid again or the records end), the stayers' extra hours (within accounts against the other region, with its fade) and the rate on counted hours.
Layer 1: the warehouse's re-sent rows, staff and test accounts, renamed publisher codes, app-store proceeds, Dutch and Belgian VAT, returned and re-presented debits, playback speed, own productions; the licence renewals' positions and the dated profiles are an assembly step, shown in the workbook and graded nowhere, and decide no plan.
Not one thing: two stumps each move the call alone and neither rescues it alone (## Stump factorial): the returns carry Standaard over the line, the stayers' listening holds Onbeperkt; fixed alone on the reflex route they file Standaard, Onbeperkt and Gezin, and Gezin alone.
One-fact test: the most useful sentence, "a subscription that stops paying can take its plan up again on the same account, the light listeners soonest", rescues R5 and R9 on the reflex route and not the call (Standaard, Onbeperkt and Gezin through), 2 of 9; the listening sentence rescues R6, 1 of 9.
Not semantics: every field read correctly still leaves each hurried result wrong: the stops, the later payments, the plan periods and the stayers' hours are all visible; what is missed is that a stop is not the end of a subscription and that a rise moves how much the stayers use, and what each is worth per counted hour.
Not rule application: guideline 3.10 files when a rise goes ahead and what its first-bill responses are measured against; no filed procedure models a return after a stop, measures a consumption response, or carries either into 2027.
Estimand: guideline 3.1, 3.2, 3.3, 3.5, 3.8, 3.9 and 3.10; schedule B 2.1 to 2.4; the price list's 2026 and 2027 prices, its profile limits and its dated e-mails; the prompt's population (subscriptions paying at the end of October 2026), outcome (their 2027 contribution; paying on any plan at the end of 2027; the 2027 remuneration on them), unit (euros per subscription; per 100 subscriptions).
No decoy: no document argues a plan; the price list announces all four rises as the incumbent position, and the task prices each on the same footing.
No replay: no result re-derives a published figure.
Pinned: R1 exact; R3 and R4 banded over the rival controls (the other region, the same region a year earlier where the records reach it), windows (the first bill, the first two), dose forms, each plan's own rise of the same kind read as it was (unfloored) and a fitted step; R5 over the continuation's form and the response readings; R6 over a common or a plan-by-plan fade and the observed months; R7, R9 and R2 over all of them and the downgrader valuation; R8 forced (every golden-family member and perturbation, each fitted response moved 20 per cent, lets Standaard and Gezin through; the world's 2027, replayed eight times with and without the rises, agrees on every plan's side of zero by five standard errors or more, and in the world itself Standaard loses without the returns and Onbeperkt gains without the stayers' listening).
Run forecast: R5 and R9 lost to an unfinished chain (a stop taken as the end of the subscription, N33); R6 and R2 to a self-confirming check (each account's recent hours carried and certified by a pooled holdout, L45) and to dismissed own evidence (no consumption response, N23); R7 and R8 to both; R1, R3 and R4 earned.
Strategy label: UNTESTED (stopped_units_return, with intensive_margin_response)
Depth level: 4 by the stump factorial: two necessary stumps (the returns, the stayers' listening), neither sufficient, the single drops on two distinct wrong answers (Gezin alone; Standaard, Onbeperkt and Gezin); the shortcuts land on five distinct wrong sets.
Lesson: under a cost per unit of use, a price rise is judged on the cohort it keeps, which includes those who stop and pay again at the new price, and on how much those who stay use after it; no build on file teaches the pair.

## Results chain

| ID | Result (checkable) | Area | Pinned by | Band | Hurried analyst | Depends on | Graded as |
|---|---|---|---|---|---|---|---|
| R1 | paying subscriptions by plan at 31 October 2026 | assembly and reconciliation | guideline 3.1; payments, accounts | exact | method shortcut: open plan periods counted (trials, staff, test), more on every plan | - | Ask 1 |
| R3 | extra cancellations per 100 reaching the first 2027 bill, by plan and region | causal reasoning | guideline 3.8 and 3.10; the past rises in the charges, the rival scan | the rival controls, windows, dose forms and readings (Standaard Netherlands 2.7 to 5.4) | narrow look at broad data: each plan's own past rises read together, never split by whether they passed the rival (Gezin 8.1, from its 2026 crossing) | independent: the 2025 and 2026 rises | Ask 2 |
| R4 | extra downgrades per 100 at that bill, by plan and region | causal reasoning | guideline 3.10; the plan changes at the past rises, the price list's profile limits | as R3 (Standaard Netherlands 3.1 to 4.0) | narrow look at broad data: as R3 | independent: the 2025 and 2026 rises | Ask 3 |
| R5 | of each plan's October 2026 subscriptions that stop paying by December 2027 with the rise, how many per 100 pay again then | modeling | guideline 3.1; the payments and plan periods of every stop since 2024 | the continuation's form and the response readings (Standaard 23.8 to 27.9) | unfinished chain: a stop read as the end of the subscription (0 on every plan) | independent: the stops to October 2026 | Component 2 |
| R6 | the stayers' extra counted hours over 2027 after the rise, per subscription staying on the plan all year | causal reasoning | schedule B 2.2; guideline 3.3; the listening and licence records, the charges' profile lists | a common or plan-by-plan fade, the observed months (Onbeperkt 33.0 to 42.2) | self-confirming check: each account's recent hours carried, a pooled holdout passing (0 on every plan) | independent: the 2025 and 2026 rises' stayers | Component 3 |
| R7 | each plan's change in its October 2026 base's 2027 contribution with the rise (EUR per subscription) | forecasting | guideline 3.9 and 3.10; schedule B 2.1 | the golden family (Flex -3.8 to -2.8, Standaard 1.0 to 3.0, Onbeperkt -5.3 to -4.2, Gezin 3.2 to 6.4) | unfinished chain: the stops taken as final and the stayers' hours as before (Standaard -0.3, Onbeperkt +2.5) | R3, R4, R5, R6 | Component 1 |
| R9 | of each plan's October 2026 subscriptions, paying on any plan at 31 December 2027 with the rise | forecasting | the prompt (on any plan); guideline 3.1 and 3.10 | the golden family (Flex 574 to 605) | unfinished chain: no payment after a stop (Flex 300) | R3, R4, R5 | Ask 4 |
| R2 | the 2027 publisher remuneration on them with the rise (EUR per October subscription) | forecasting | schedule B 2.1 to 2.4; guideline 3.3 and 3.9 | the golden family (Onbeperkt 113.4 to 122.4) | self-confirming check: each account's recent hours carried and no return (Onbeperkt 101.7) | R5, R6 | Ask 5 |
| R8 | the rises that go ahead: Standaard and Gezin; Flex and Onbeperkt held | synthesis | guideline 3.10 | exact | unfinished chain: the careful route lets Onbeperkt and Gezin through | R7 | Recommendation |

Carry-forward: R1 stands on the base; the counted hours (rebuilt from the live roll-up and the licence renewals, each profile on the account its charge lists) are a Layer 1 assembly step shown in the workbook and not graded; R3 and R4 stand on the past rises, R5 on the stops since 2024, R6 on the past rises' stayers; R7 falls with R3, R4, R5 and R6, R9 with R3, R4 and R5, R2 with R5 and R6, R8 with R7; a run with R7 wrong on one plan still earns the others' cells.

## Hidden factor record

| Factor | Real or constructed | Only in deciding units | Found by | Fix depth | Verdict |
|---|---|---|---|---|---|
| a rise answers mainly where the new price passes the rival's comparable plan | constructed (a step at the rival's price on every plan, in every region, at every rise) | no: four past rises passed the rival and four did not, on four plans | modelling (the response read per event against the other region and set against the December scan) | modelling (each 2027 cell from the plan's own rise of the same kind) | keep (a reflex, R61) |
| light listeners leave at the December bill after the price e-mail | constructed (every announced rise, every plan, both regions) | no: eight events | modelling (the December bill in the rising region against the other) | modelling | keep (a reflex, R62) |
| a subscription that stops can take its plan up again on the same account, light listeners soonest, more before the summer | constructed (every stop on every plan, both regions, every year) | no: 5,628 of 14,143 stops since 2024 paid again by October 2026, on every plan; it moves every plan's figures and decides Standaard because its rise's gain sits closest to what it loses | modelling (a return hazard by listening band, months since and calendar month on every stop, each at risk until it paid again or the records end) | modelling (carried through the 2027 cohort at the price then in force, with the returned subscriptions' own continuation) | keep (one of two stumps) |
| the account holder listens more for months after the bill at a higher price, the heavier the listener the more | constructed (every rise, every plan, both regions, both years) | no: measured on all four plans (first month Onbeperkt 19.7, Standaard 11.0, Gezin 4.8, Flex 4.8 per cent); it decides Onbeperkt because its heavy listeners carry the thinnest margin per counted hour | modelling (within accounts against their own October to December and the other region; a plan's average counts the light leavers' absence as listening) | modelling (the stayers' 2027 hours with the fade, at EUR 0.40) | keep (one of two stumps) |
| heavy listeners switch to the rival at a crossing; light listeners leave at the e-mail and move down | constructed (who answers depends on listening) | no | modelling | modelling (each answer on its own listening, a reflex, R44) | keep (supporting) |
| a downgrader keeps paying on the cheaper plan and hits its cap | constructed (cap-hit leaving on Flex and Standaard) | no | a targeted query | modelling (a reflex, R43) | keep (supporting) |

## Effort test

| Result | Quick pass | Careful but hurried | Thorough |
|---|---|---|---|
| R1 paying subscriptions by plan at 31 October 2026 | Missed | Right | Right |
| R3 extra cancellations per 100 at the first 2027 bill, by plan and country | Missed | Right | Right |
| R4 extra downgrades per 100 at the first 2027 bill, by plan and country | Missed | Right | Right |
| R9 of each plan's October 2026 subscriptions, paying on any plan at 31 December 2027 with the rise | Missed | Missed | Right |
| R2 the 2027 publisher remuneration on each plan's October 2026 subscriptions with the rise, per subscription | Missed | Missed | Right |
| R7 each plan's change in its October 2026 subscriptions' 2027 contribution with the rise | Missed | Missed | Right |
| R5 of the subscriptions that stop paying by December 2027, how many per 100 pay again then | Missed | Missed | Right |
| R6 the stayers' extra counted hours over 2027 after the rise, per subscription staying all year | Missed | Missed | Right |
| R8 the rises that go ahead | Missed | Missed | Right |
| Roughly | 0 of 9 | 3 of 9 | 9 of 9 |

Measured by: .claude/skills/stumping/effort.py on generator/effort.json
Largest single hint: a subscription that stops paying can take its plan up again on the same account, the light listeners soonest, so those a rise loses are not all lost for 2027; rescues 2 of 9 results
Pair estimate: 40.0 (measured by effort.py on generator/effort.json; the careful pass is the reflex route, the platform run's own)

## Stump factorial

Reflex route: every move the platform runs made unprompted set right (the first bill read by whether each past rise passed the rival, with the profile limit of the plan below, R61; the December leavers after the e-mail, R62; downgraders kept paying, R43; each subscription on its own listening, R44; EUR 0.40 a counted hour, filed in schedule B; a past response carried to a rise of another size, R45, moot since every 2027 rise is the plan's past rise in euros), every stump hurried (a stop taken as the end of the subscription, each account's recent hours carried): it files Onbeperkt and Gezin against the golden's Standaard and Gezin.

| Judgment | Kind | Hurried choice | Evidence | Dropped alone from the golden | Fixed alone on the reflex route | One routine step once told |
|---|---|---|---|---|---|---|
| J1 a subscription that stops can take its plan up again on the same account, light listeners soonest | stump | a stop taken as the end (the October cohort carried with cancellation as final) | N33, N24 | Gezin alone (Standaard EUR -1.4) | Standaard, Onbeperkt and Gezin; R5 and R9 rescued (2 of 9) | no |
| J2 the stayers listen more for months after the bill at the higher price, the heavier the more | stump | each account's recent hours carried (a pooled holdout passes) | N23, L45 | Standaard, Onbeperkt and Gezin (Onbeperkt EUR +4.6) | Gezin alone; R6 rescued (1 of 9) | no |
| J3 the first bill read by whether each past rise passed the rival, with the profile limit below | reflex | each plan's own past rise in its region | R61 | Standaard alone | - | - |
| J4 the light listeners' extra leaving at the December bill after the e-mail | reflex | the response a first-bill pulse | R62 | same call (Flex EUR -0.5) | - | - |
| J5 downgraders kept paying, valued on their own months | reflex | counted as exits | R43 | same call | - | - |
| J6 each subscription valued on its own listening | reflex | the plan's average | R44 | same call | - | - |
| J7 EUR 0.40 per counted hour | reflex | the 2026 revenue share | schedule B 2.1 (filed) | same call (every figure outside its band) | - | - |

Level: 4 (two necessary stumps, neither sufficient, the single drops on two distinct wrong answers)

## Data provenance

Source: generated by the seeded generator in task1/generator from a simulated subscription business: accounts, plans, payments, profiles, listening and licence renewals; plan prices that rose in one region in January 2025 and in the other in January 2026, each announced by e-mail on 1 December; a rival whose comparable plans the pricing team scans monthly by region, with summer promotions and, in July 2026, a list-price rise of its Basis 10 uur and its Flemish Onbeperkt and Familie brought to its Dutch prices; at the December bill after the e-mail, light listeners leaving; at each subscription's first bill at a higher price, extra cancellations and downgrades, a step where the new price passes the rival's, heavy listeners switching and light listeners moving down where the profiles fit the plan below; a subscription that stops (by cancelling, or on a debit returned and not re-presented) taking its plan up again on the same account at a chance that falls with the months since, is higher for light listeners and before the summer, at the price then in force, and stopping more often in its first months back; the account holder listening more for months after the first bill at a higher price, the heavier the more; extra leaving after a month that runs out of hours on Flex and Standaard.
Behaves like the real thing: price rises staged by market, reference-price effects at a competitor's price point, downgrades as a share of a rise's response, churned subscribers who resubscribe (light and seasonal listeners above all), the sunk-cost and payment-salience lift in use after a price rise, hour caps that bind, per-hour royalties under which heavy listeners carry little margin.
Genuine patterns: (1) seasons in listening, signups and returns, (2) churn falling with tenure and engagement, higher on Flex and in the first months back, (3) offline listening heaviest on Onbeperkt, (4) plan switches and profile moves, (5) the rises' first-bill and December responses by region and year, (6) rival promotions in summer.
Problems by process: re-sent warehouse rows; staff and test accounts; renamed publisher codes; store proceeds; returned and re-presented debits; playback speed; own productions.
License: not applicable (generated data, no public source)
Used as is: not applicable (generated data)
Breadth: 18 files (14 used, 4 distractors), 1,031,789 live listening rows, 598,066 licence renewals, 216,281 payments, 42,480 plan periods, 272 rival scan rows, four plans in two regions over 34 months, eight past rise events, 14,143 stops since 2024 of which 5,628 paid again by October 2026.

## Stump screen

Re-run on 2026-11-13 after the holistic audit, with the stump factorial (stumping Part 3.3): test 2 asks whether a platform run made the move unprompted (task1/runs/arch5_run1.md and arch5_run2.md), test 9 whether it moves the call alone with the others right.

| Candidate trap | 1 closed | 2 reflex | 3 filed | 4 clean data | 5 two records | 6 assumption | 7 shallower story | 8 across data | 9 worth the call | Kept |
|---|---|---|---|---|---|---|---|---|---|---|
| a stopped subscription takes its plan up again on the same account, light listeners soonest | yes (stopped_units_return; the nearest closed cards are survivorship, where the fix is a point-in-time rebuild, and censoring, where follow-up is unfinished: here every stop is recorded and its sequel is modelled) | yes (both runs: "No reactivation", N33, N24) | yes (no document names a return; the plan periods carry end reasons only) | yes | yes (the payments' months against the plan periods' new periods and the listening before the stop) | yes (N33) | yes (a fixed-cohort continuation fits the observed monthly staying and passes a holdout) | yes (every plan, every year) | yes (dropped alone, Standaard held) | kept |
| the account holder listens more for months after the bill at a higher price | yes (intensive_margin_response; nearest closed cards composition, a supporting step here, and self-selection, which it is not: the rise is assigned by region and year) | yes (N23; the reshipped cut's run carried recent hours, L45) | yes | yes | yes (the listening and licence records against the charges' profile lists, within accounts) | yes (N23) | yes (listening rises with the season, and a plan's average rises when light listeners leave) | yes (all four plans) | yes (dropped alone, Onbeperkt goes ahead) | kept |
| the response steps where the new price passes the rival's comparable plan | yes (response_at_crossing_point) | no: the reshipped cut's run read it unprompted with the profile limit (R61) | yes | yes | yes | no | yes | yes | no (dropped alone, Standaard alone goes ahead; a reflex) | kept as a supporting step, not a stump: a reflex since R61, graded in R3 and R4 |
| light listeners leave at the December bill after the price e-mail | yes | no: the run included December anticipation (R62) | yes (the price list dates the e-mails) | yes | yes | no | yes | yes | no (same call) | dropped (reflex) |
| Onbeperkt's single users add a second profile after a rise | yes | yes | yes | yes | yes | yes | yes | no (in practice only Onbeperkt; one table shows it) | yes | dropped (the audit: one constructed shift) |
| the light price leavers come back more often than the average leaver | no (the pooled rate carried to a lighter mix: the transport card) | yes | yes | yes | yes | yes | yes | yes | no (same call) | supporting only |

## Template check

Chain signature: assembly-reconciliation, causal-reasoning, causal-reasoning, modeling, causal-reasoning, forecasting, forecasting, forecasting, synthesis
Question form: which (which rises go ahead); answered by the decision, a set of plans
Nearest chain: task14 v3 shares the shape and the weight family and nothing else (a national rent measure there); task24 v1 (drawn 2026-11-13, an annotation vendor's accept set at offered prices) shares the answer shape and the modeling weight only: its lessons are an any-miss aggregation over objects, a pay floor and track turnover, its decision accepts requests against a cost model, and nothing in it follows a cohort, a stopped pool or a consumption response.
Nearest build: task4 arch 11 (a response its own record hides) shares the forecast shape only; the slot's own architecture 3 priced a past rise's response (its R4) as one step in a funding chain; here the cohort's stops are followed to their returns and the stayers' use is measured, and both decide a go-or-hold per plan.
Abstraction sentence: none writable against a build on file.

## Frontier check

Precedents: R5 (N33 a stop taken as the end; N24), R6 (N23 no consumption response; L45 recent hours certified by a pooled holdout), R7 (N33, N23, L45), R9 (N33), R2 (N23, L45, N33), R8 (N33, N23)
Shallow path checks: R5, R9: a fixed cohort with stopping as final reproduces the observed monthly continuation and passes a 2026 holdout of ordinary cancellation (the reshipped cut's run: 5.03 per 100 observed against 5.06); only following each stop in the payments to its next paid month (the plan periods' new periods, another grain) shows that 5,628 of 14,143 came back. R6, R2: each account's recent hours with seasonality passes a pooled 2026 usage holdout (the run's -0.34 to +2.07 per cent); only the stayers' hours within accounts against their own October to December and the other region, month by month after each rise, show the response and its fade. R7, R8: both.
Assumption made false: "No reactivation ... forecast" (N33), false because a stopped subscription takes its plan up again on the same account at a rate the payments of every stop since 2024 show (about 58 in 100 of the lightest December stops within a year), tested by the payments and the plan periods; "No additional consumption response to price" (N23), false because the account holder listens more for months after the bill at a higher price, tested by the listening and licence records within accounts against the other region.
Forcing: the line is each plan's change against zero; the golden family (the year before as control, the first two bills, the log dose, each plan's own rises of the same kind, a fitted step, continuation by paying months alone, downgraders on their own capped hours, a plan-by-plan fade, the observed months, re-sent rows summed) lets Standaard and Gezin through, nearest Standaard EUR 1.25 and Onbeperkt EUR -4.5; the shortcuts land on five other sets (Onbeperkt and Gezin; Standaard, Onbeperkt and Gezin; Gezin; Onbeperkt; none); each of the first bill's cancellations, its downgrades, the December leaving, the stayers' extra listening and the return after a stop moved 20 per cent leaves the call; the world's 2027 replayed eight times puts Flex (-1.8) and Onbeperkt (-2.4) below zero and Standaard (+2.0) and Gezin (+3.6) above by five standard errors or more, and in the world itself Standaard loses without the returns (-2.5) and Onbeperkt gains without the stayers' listening (+5.0); every 2027 rise is the plan's past rise in euros and every 2027 cell has a past rise of its own plan of the same kind.
Noun swap: nearest by skeleton.py is task7 v10 and mark115 (severity none); the decision form, the lessons and the mechanisms differ.
Closed strategies: the call turns on two open lessons (stopped_units_return, intensive_margin_response); the nearest closed cards are survivorship (today's file has lost the ones that left, fixed by a point-in-time rebuild or a survival reweight: here every stop is in the record and the work is the return flow after it) and censoring (follow-up still open: here the stop is observed and its sequel modelled), and for the listening composition (a plan's average carries the leavers' absence: a supporting step, whose route "the golden with the stayers' listening read off the plan's averages" files Standaard and Gezin); the transport card (the average leaver's return rate carried to the lighter price leavers) is a supporting step whose route "the golden with returns at one rate for every listener" files Standaard and Gezin; marginal_not_average (taught) is a reflex here (R44).

## Semantic fork table

| ID | Term or convention | Readings | Golden | Ruled out by |
|---|---|---|---|---|
| SF1 | paying subscription | open periods / a collected charge | collected charge (guideline 3.1) | guideline 3.1 |
| SF2 | a rise's extra cancellations | all cancellations / beyond the same months without the rise | beyond the same months without the rise (3.10) | guideline 3.10 |
| SF3 | the first bill at the new price | the January charge / the January and February charges | the January charge | same call (window rival inside the band) |
| SF4 | the comparison | the other region / the same region a year earlier | the other region | same call (rival inside the band) |
| SF5 | the rival's price | the latest scan / the December scan before the rise, promotions out | the December scan before each past rise; for 2027 the latest, October 2026 (3.8) | guideline 3.8 |
| SF6 | the base's 2027 contribution | on the plan only / followed through 2027 | followed through 2027, a downgrader's and a returned subscription's months included (3.10) | guideline 3.10; same call |
| SF7 | contribution | net revenue / less remuneration at the agreement's rate | less EUR 0.40 per counted hour (3.9, schedule B 2.1) | guideline 3.9 |
| SF8 | counted hours | streamed seconds / positions across every report | positions across every report (schedule B 2.2) | schedule B 2.2 |
| SF9 | the 2027 prices | the price list / the 2026 prices | the price list's 2027 prices (3.8), the other plans at their announced prices | guideline 3.8 |
| SF10 | re-sent warehouse rows | summed / dropped | dropped | same call |
| SF11 | the regions | the country of the account / the storefront | the account's country | the accounts export |
| SF12 | downgraders' value | modelled on their own hours / their own realised months | realised months | same call (model rival inside the band) |
| SF13 | the size a past response carries at | as read / in proportion to the rise / on the log of the price ratio | in proportion to the rise, pooled by listening band | same call (each form in the golden family); every 2027 rise is the plan's past rise in euros |
| SF14 | how a 2027 first bill is read | pooled by listening band / each plan's own rise of the same kind / a fitted step | pooled by listening band, the downgrades among subscriptions whose profiles fit the plan below | same call (the other readings in the golden family and inside the bands) |
| SF15 | the e-mail's leavers | November paying, not December, against the other region / every December stop | beyond the other region, each plan's two rises (the price list dates every e-mail 1 December) | guideline 3.10; the price list |
| SF16 | the stayers' listening | within accounts on the plan through the month, rising region over the other / a plan's average / held at its first months | within accounts, with its fade | named data: the December and first-bill leavers listened less than their plan, so a plan's average rises with no one listening more; the observed months fall from 18.9 to 2.0 per cent on Onbeperkt, so no fade is ruled out |
| SF17 | the October base's continuation | by paying months and listening band / by paying months alone | by paying months and listening band | same call (rival inside the band) |
| SF18 | the first-bill responses' denominator | per 100 of the October base / per 100 reaching the bill | per 100 reaching the first bill at the new price | guideline 3.10 |
| SF19 | paying at the end of 2027 | without a break since October / on any plan at 31 December 2027 | on any plan at 31 December 2027, a subscription that stopped and paid again counted | the prompt ("would be paying, on any plan, at the end of 2027"); guideline 3.1 |
| SF20 | a rise passing the rival | from at or below the rival's price to above it / a new price above the rival's | either: no plan sits above the rival before any past rise or the 2027 rise (the scan: the rival's Basis 10 uur at EUR 9.79 in both countries to June 2026, its July 2026 rises), so the two readings classify every past rise and every 2027 cell alike | convergence, asserted (C1) |
| SF21 | the price a returned subscription pays | its old price / the price then in force | the price then in force | the price list (existing subscriptions move to the new price at their first billing date in 2027) |
| SF22 | the 2027 remuneration | the plan's average hours / each subscription's own counted hours, returned months and the stayers' extra included | each subscription's own counted hours in 2027 at EUR 0.40 | schedule B 2.1 and 2.2; guideline 3.3 |

## Closure table

| Axis | Closure |
|---|---|
| 1 | population: consumer accounts paying at 31 October 2026 (3.1, 3.10) |
| 2 | unit of account: the subscription; per 100 subscriptions for responses |
| 3 | attribution window: the first bill at the new price; 2027 for contribution and remuneration |
| 4 | as-of: records to 31 October 2026 (exports 2 to 4 November) |
| 5 | version basis: the price list's 2027 prices, the rival's October 2026 scan (3.8) |
| 6 | denominator: subscriptions reaching the first bill; subscriptions in the October base |
| 7 | weighting: by subscriptions in each region |
| 8 | window length: the January bill at each past rise; January to December 2027 |
| 9 | boundary inclusivity: none on an edge (no 2027 price equals a rival's) |
| 10 | rounding path: none filed; precision in the answer blocks |
| 11 | tie-break: none needed |
| 12 | maturity: every past rise's first bill closed; stops followed to the records' end |
| 13 | order of operations: responses by event, then carried, then valued month by month |
| 14 | row order: C1 |
| 15 | duplicate resolution: re-sent rows dropped (SF10) |
| 16 | identity normalisation: profiles to accounts by the charges' lists; publisher codes by the crosswalk |
| 17 | netting: refunds and returned debits net |
| 18 | dimensional units: euros, counted hours, per 100 |
| 19 | code semantics: plan codes as billed; end reasons as the plan periods state them |
| 20 | integerisation: none |
| 21 | clause scope: schedule B audiobooks only |
| 22 | forward window contents: the 2027 price list and the latest rival scan ship |

## Literal reader

The prompt asks which rises go ahead, each plan's change in what its October 2026 subscriptions bring in 2027, how many of them would be paying on any plan at the end of 2027 and what the remuneration on them would come to in 2027 if the rise goes ahead, and the paying base and the first-bill responses; guideline 3.10 lets a rise through when it raises that contribution against holding the 2026 price, its extra leaving and downgrades being those beyond the same months without it; 3.9 and schedule B price the counted hours; 3.8 takes the 2027 prices and the rival's last scan; the price list dates the e-mails; executed word for word they give Standaard's and Gezin's rises and Flex and Onbeperkt held.

## Prompt contract

A voice rewrite may not drop or change: the question (which of the rises still go ahead); why it rests on estimates (none weighed against the per-hour remuneration); the workbook and the short deck with the decision per plan and each rise's change to what the plan's subscriptions paying at the end of October 2026 bring in 2027, in euros per subscription; the paying subscriptions per plan at the end of October 2026; how many of them would be paying, on any plan, at the end of 2027 if the plan's rise goes ahead (not "still paying", which reads as paying without a break); what the publisher remuneration on them would come to in 2027, in euros per subscription; for each plan in the Netherlands and in Flanders how many of every 100 subscriptions the rise would lose at their first bill at the new price and how many it would move down a plan. It must never add: the rival, a return, a resubscription, the stayers' listening, a method, a warning, a file name, a role, a count of plans, rounding.

## Tried and rejected

- Matching new members to the tutor with the most open slots (pricing simulator v1 to v2): every month's new members
  went mostly to new tutors, so history carried the same exposure as AUT26 and the curve landed on the truth
  (0.834 against 0.837 of receipts); the world needs the platform to match new members to established tutors and to
  run with spare established capacity, which it does.
- Twelve-month receipts per member as the decision quantity: the four observed months dilute the move to about
  3 per cent of the figure; the twelfth-charge retention carries it at about 18 per cent.
- Matching new members to the most established tutor with room, where "established" began at four teaching months
  (simulator v9): surge members landed on tutors inside the stopping hump, the spring 2025 campaign carried as much
  exposure as AUT26 and the curve missed it by 17 to 22 per cent on back-test, a search signal; established now means
  nine or more teaching months.
- A spring 2025 campaign of 680 members (simulator v7 to v10): either it carried most of the effect (the textbook
  route failed its own back-test) or it was too small to tell the models apart; SPR25 is now 264 members, too few to
  separate the routes on its own, the textbook route validates on it, and the discriminating evidence is member-level.
- Tutor capacity fixed at hire (generator v1 and v2): established tutors stayed full, so surge and growth overflow
  went to tutors inside the hump in ordinary months, history carried AUT26's exposure and the curve landed near the
  truth (0.301 against 0.303); established tutors now open more slots once past their first nine teaching months.
- A post-rematch uplift and calendar-month seasonality in the process (generator v3 to v6): neither decided anything,
  and between them they moved the graded cost per twelfth-month member by about 1.3 per cent across defensible
  variants, a fork at any useful rounding; both left the process.
- A 50 per cent first-month offer: the discounts were a quarter of the cost, so a deep run that misread the cost rule
  and left them out filed the re-run; the offer is now 10 per cent and leaving it out stays 5 per cent outside the bar.
- Tutor ids rewritten at a 2025 lesson-platform migration: left unnormalised they split tutors, flattened the stopping
  hump and flipped the call (1,274 twelfth-month members), so cleaning decided the answer; ids keep one format.
- A range on the twelfth-month members as an ask: tutor-clustered and member-independent ranges coincide at the
  nearest 50, so it graded no judgment; the cost ranges at the nearest 25 separate at every endpoint.
- Fuller new-tutor rosters to widen the clustered range (caps 26 to 36): one endpoint separated and the shallow routes
  moved to within 6 per cent of the bar; reverted.
- A 95 per cent range on the cost per twelfth-month member: its upper end sat on its rounding line at 4,000 draws
  and its lower end moved with the draw, so the figure was a coin at the nearest 25; the 90 per cent range keeps both
  ends inside their rounding (`checks.py` R7) and members drawn one at a time move both ends.
- An 80 per cent band on each month's total in the workbook: several of its 22 ends changed between seeds at 4,000
  draws at the nearest 50, and at the nearest 100 it no longer told tutor-by-tutor draws from member-by-member ones;
  the workbook carries the monthly expectations only.
- 2026-11-09, architecture 1 (Corvane, the autumn campaign's members carried through their tutors' stopping hump):
  returned in kind by the project lead's review (one hidden constructed factor; the forward cohort was the only one
  built to be exposed, the generator tuned until history stopped carrying the exposure, and every graded figure came
  from one projection). Re-rooted to a new world as a results chain.
- 2026-11-09, stage 3: seat additions from the book's mean growth in users by account age (no account's own drift):
  EUR 0.10 million against the process's EUR 0.49 million, because need growth differs by account and seats only
  ever true up; replaced by each account's own drift, shrunk to the book (24 months), with 12 and 18 months, each
  account's trailing true-up rate and the book's trailing rate kept as rivals.
- Each account's trailing true-up rate as the golden's seat additions (the stage-2 prototype): EUR 0.56 million,
  above every drift form; kept as a rival, inside every band.
- A slower April decay (PAD_DECAY 3.0, PAD_SHOCK 0.10) to push the careful pass's last-three-months Team rate out of
  R3's band: the excess series is too noisy month by month for the golden to tell the forms apart either, and the gap
  stayed about EUR 15,000; parameters reverted, R3 priced Partly for the careful pass.
- The commitment graded at one 0.1 million bin: the honest family's P20 spans EUR 9.79 to 9.92 million (the exit
  model's utilisation form and the seat-addition form move it), so the commitment's band is 9.8 to 9.9 and the draft
  moved from EUR 10.4 to 10.2 million so that the careful pass (10.23) still clears it wrongly.
- The draft at EUR 10.4 million: the careful but hurried pass's commitment (EUR 10.2 million) sat under it, so the
  pass gave the right verdict for the wrong reason; the draft is EUR 10.2 million.
- Credit notes and re-issues on renewals after 1 March 2026: kept beside the re-issues they moved the price line to
  EUR 310,000 and the commitment to 10.0, so cleaning decided R2; the billing errors now sit on 2024 to February 2026
  renewals, where kept they break the renewal pairing visibly and decide nothing.
- The workspace links' end-and-restart dates listed as Layer 1 mess: read without dates they move R3 (1.43), R5
  (1.12) and the commitment (9.7), because the dates are how an upgrade is told from a cancellation; they are
  evidence for R3, R4 and R5, not mess.
- The ask "how much of October's Team ARR is still billed on the Team plan in December 2027": read two ways (the
  October ARR of the accounts still on Team, or their December 2027 ARR, about EUR 0.07 million apart); the prompt
  now asks for the Team ARR in December 2027 from accounts on the plan at the end of October 2026.
- New Business accounts held at their signing ARR to December 2027 (their ramp true-ups and the first renewals of
  November and December 2026 signings ignored): policy 4.2 counts a first term at its service start, every route
  shares the convention, and it is recorded rather than modelled.
- 2026-11-10, the uploaded cut (price rise 1 March 2026, Team minimum 1 April 2026, deal creation falling from 37 to 27
  a month after March 2026, the commitment "to the nearest EUR 0.1 million"): the platform's holistic audit failed it
  on determinism (runs/arch2/holistic_audit.md). The P20 of 9.89 rounded to 9.9, a step met in under 80 per cent of
  outcomes, and rounded down to 9.8; the band with and without the estimation uncertainty was pinned by no file;
  the Team and open-deal figures were stated as ranges at 10,000; and the run's "recent creation" reading of the
  post-March fall made a naive pipeline view fail the draft on its own. Repaired in the generator: the commitment
  defined as the largest 0.1 million step met in at least 80 per cent of outcomes (prompt, policy 5.3); policy 5.2
  files what the range carries; the two note figures asked at the precision the defensible methods pin; the creation fall removed (flat since 2024);
  the price rise and the minimum moved to 1 January 2026 so the trailing year carries the whole step and the padded
  seats; the world re-seeded so every graded figure sits mid-bin at its rounding.
- 2026-11-10, a world with the price rise at 1 March 2026 and the creation fall removed (seed 1107, scratch v1 and
  v2): every trailing extrapolation cleared the golden by 0.08 to 0.5 million only, because the trailing year's new
  Business, expansion and churn ran below the forward's while only the price line ran above; with the rise and the
  minimum at 1 January and the creation trend ended in 2024 (v3) the trailing views clear by 1.2 million.
- 2026-11-10, the exit model without a utilisation term priced as a hurried route: in the March-calendar world it moved
  accounts lost by 60,000, in the chosen world by under 2,000 (the term carries the seat cuts, not the exits), so it is
  a rival inside the bin (SF24), and the pooled route and independent draws carry R4's loss.
- 2026-11-10, the book's trailing true-up rate at accounts near their seats as a rival for seat additions: 60,000 under
  the drift forms in every world measured (it ignores each account's own growth and the ramp of young accounts); priced
  as a hurried route; the drift windows 12, 18, 24 and each account's own trailing rate stay the family, which with
  need growth less dispersed (NEED_GROWTH_SD 0.03) lands in one step.
- 2026-11-10, the pooled renewal route's seat-reduction gap as a structural result: in the uploaded cut pooled rates
  gave 310,000 against 200,000, in the first re-seeded worlds the two coincided; the gap was the cut's mix against
  the history's, not the process. The process now carries it: utilisation at signing drifts down year by year, so
  the forward book's renewals cut and leave more than the pooled history says; the direction still varies by world
  and the chosen seed's gap is asserted.
- 2026-11-10, the common factor of 0.25 the platform run assumed, as a defensible rival: nothing in the records supports
  it and policy 5.2 rules it out; in the chosen world it widens the 80 per cent range by about a third and moves the 20th
  percentile down by under 20,000, inside the step, so it is priced as a route the sentence settles rather than one the
  step separates (SF21).
- 2026-11-10, Team seasonality in the hurried "last three months" route: in the uploaded cut the last three months
  sat one 10,000 bin under the golden because the April shock had decayed to its floor by August; with the plan's
  cancellations running with the calendar (an autumn peak in every year of the history) a three-month window
  carries a season and lands 60,000 to 160,000 under the golden in every world measured.
- 2026-11-10, the two note figures at the nearest EUR 50,000: the win odds by stage and deal age put the open deals' part
  20,000 above the stage-and-staleness golden, so at 50,000 the defensible family straddled a bin edge in the chosen world;
  asked at the nearest EUR 0.1 million the family lands in one bin with margin, the CRM's odds stay far outside, and
  stage alone, which that rounding no longer separates, is priced as a route the CRM's odds carry rather than its own.
- 2026-11-10, seeds 1101 to 1124 scanned for a world whose graded figures sit mid-bin at the new roundings with the
  band's step the same with and without the estimation uncertainty and the pooled, trailing-twelve and stage-alone
  routes outside; 1109 failed only on seat reductions 4,000 from a 50,000 edge, 1115 only on the Team figure 4,000
  from an edge; seed 1126 chosen on the full family.
- 2026-11-10, the uploaded cut (price rise 1 March 2026, Team minimum 1 April 2026, deal creation falling from 37 to 27
  a month after March 2026, the commitment "to the nearest EUR 0.1 million"): the platform's holistic audit failed it
  on determinism (runs/arch2/holistic_audit.md). The P20 of 9.89 rounded to 9.9, a step met in under 80 per cent of
  outcomes, and rounded down to 9.8; the band with and without the estimation uncertainty was pinned by no file;
  the Team and open-deal figures were stated as ranges at 10,000; and the run's "recent creation" reading of the
  post-March fall made a naive pipeline view fail the draft on its own. Repaired in the generator: the commitment
  defined as the largest 0.1 million step met in at least 80 per cent of outcomes (prompt, policy 5.3); policy 5.2
  files what the range carries; the two note figures asked at the precision the defensible methods pin; the creation fall removed (flat since 2024);
  the price rise and the minimum moved to 1 January 2026 so the trailing year carries the whole step and the padded
  seats; the world re-seeded so every graded figure sits mid-bin at its rounding.
- 2026-11-10, a world with the price rise at 1 March 2026 and the creation fall removed (seed 1107, scratch v1 and
  v2): every trailing extrapolation cleared the golden by 0.08 to 0.5 million only, because the trailing year's new
  Business, expansion and churn ran below the forward's while only the price line ran above; with the rise and the
  minimum at 1 January and the creation trend ended in 2024 (v3) the trailing views clear by 1.2 million.
- 2026-11-10, the exit model without a utilisation term priced as a hurried route: in the March-calendar world it moved
  accounts lost by 60,000, in the chosen world by under 2,000 (the term carries the seat cuts, not the exits), so it is
  a rival inside the bin (SF24), and the pooled route and independent draws carry R4's loss.
- 2026-11-10, the book's trailing true-up rate at accounts near their seats as a rival for seat additions: 60,000 under
  the drift forms in every world measured (it ignores each account's own growth and the ramp of young accounts); priced
  as a hurried route; the drift windows 12, 18, 24 and each account's own trailing rate stay the family, which with
  need growth less dispersed (NEED_GROWTH_SD 0.03) lands in one step.
- 2026-11-10, the pooled renewal route's seat-reduction gap as a structural result: in the uploaded cut pooled rates
  gave 310,000 against 200,000, in the first re-seeded worlds the two coincided; the gap was the cut's mix against
  the history's, not the process. The process now carries it: utilisation at signing drifts down year by year, so
  the forward book's renewals cut and leave more than the pooled history says; the direction still varies by world
  and the chosen seed's gap is asserted.
- 2026-11-10, the common factor of 0.25 the platform run assumed, as a defensible rival: nothing in the records supports
  it and policy 5.2 rules it out; in the chosen world it widens the 80 per cent range by about a third and moves the 20th
  percentile down by under 20,000, inside the step, so it is priced as a route the sentence settles rather than one the
  step separates (SF21).
- 2026-11-10, Team seasonality in the hurried "last three months" route: in the uploaded cut the last three months
  sat one 10,000 bin under the golden because the April shock had decayed to its floor by August; with the plan's
  cancellations running with the calendar (an autumn peak in every year of the history) a three-month window
  carries a season and lands 60,000 to 160,000 under the golden in every world measured.
- 2026-11-10, the two note figures at the nearest EUR 50,000: the win odds by stage and deal age put the open deals' part
  20,000 above the stage-and-staleness golden, so at 50,000 the defensible family straddled a bin edge in the chosen world;
  asked at the nearest EUR 0.1 million the family lands in one bin with margin, the CRM's odds stay far outside, and
  stage alone, which that rounding no longer separates, is priced as a route the CRM's odds carry rather than its own.
- 2026-11-10, seeds 1101 to 1124 scanned for a world whose graded figures sit mid-bin at the new roundings with the
  band's step the same with and without the estimation uncertainty and the pooled, trailing-twelve and stage-alone
  routes outside; 1109 failed only on seat reductions 4,000 from a 50,000 edge, 1115 only on the Team figure 4,000
  from an edge; seed 1126 chosen on the full family.
- 2026-11-10, the uploaded cut (price rise 1 March 2026, Team minimum 1 April 2026, deal creation falling from 37 to 27
  a month after March 2026, the commitment "to the nearest EUR 0.1 million"): the platform's holistic audit failed it
  on determinism (runs/arch2/holistic_audit.md). The P20 of 9.89 rounded to 9.9, a step met in under 80 per cent of
  outcomes, and rounded down to 9.8; the band with and without the estimation uncertainty was pinned by no file;
  the Team and open-deal figures were stated as ranges at 10,000; and the run's "recent creation" reading of the
  post-March fall made a naive pipeline view fail the draft on its own. Repaired in the generator: the commitment
  defined as the largest 0.1 million step met in at least 80 per cent of outcomes (prompt, policy 5.3); policy 5.2
  files what the range carries; the two note figures asked at the precision the defensible methods pin; the creation fall removed (flat since 2024);
  the price rise and the minimum moved to 1 January 2026 so the trailing year carries the whole step and the padded
  seats; the world re-seeded so every graded figure sits mid-bin at its rounding.
- 2026-11-10, a world with the price rise at 1 March 2026 and the creation fall removed (seed 1107, scratch v1 and
  v2): every trailing extrapolation cleared the golden by 0.08 to 0.5 million only, because the trailing year's new
  Business, expansion and churn ran below the forward's while only the price line ran above; with the rise and the
  minimum at 1 January and the creation trend ended in 2024 (v3) the trailing views clear by 1.2 million.
- 2026-11-10, the exit model without a utilisation term priced as a hurried route: in the March-calendar world it moved
  accounts lost by 60,000, in the chosen world by under 2,000 (the term carries the seat cuts, not the exits), so it is
  a rival inside the bin (SF24), and the pooled route and independent draws carry R4's loss.
- 2026-11-10, the book's trailing true-up rate at accounts near their seats as a rival for seat additions: 60,000 under
  the drift forms in every world measured (it ignores each account's own growth and the ramp of young accounts); priced
  as a hurried route; the drift windows 12, 18, 24 and each account's own trailing rate stay the family, which with
  need growth less dispersed (NEED_GROWTH_SD 0.03) lands in one step.
- 2026-11-10, the pooled renewal route's seat-reduction gap as a structural result: in the uploaded cut pooled rates
  gave 310,000 against 200,000, in the first re-seeded worlds the two coincided; the gap was the cut's mix against
  the history's, not the process. The process now carries it: utilisation at signing drifts down year by year, so
  the forward book's renewals cut and leave more than the pooled history says; the direction still varies by world
  and the chosen seed's gap is asserted.
- 2026-11-10, the common factor of 0.25 the platform run assumed, as a defensible rival: nothing in the records supports
  it and policy 5.2 rules it out; in the chosen world it widens the 80 per cent range by about a third and moves the 20th
  percentile down by under 20,000, inside the step, so it is priced as a route the sentence settles rather than one the
  step separates (SF21).
- 2026-11-10, Team seasonality in the hurried "last three months" route: in the uploaded cut the last three months
  sat one 10,000 bin under the golden because the April shock had decayed to its floor by August; with the plan's
  cancellations running with the calendar (an autumn peak in every year of the history) a three-month window
  carries a season and lands 60,000 to 160,000 under the golden in every world measured.
- 2026-11-10, the two note figures at the nearest EUR 50,000: the win odds by stage and deal age put the open deals' part
  20,000 above the stage-and-staleness golden, so at 50,000 the defensible family straddled a bin edge in the chosen world;
  asked at the nearest EUR 0.1 million the family lands in one bin with margin, the CRM's odds stay far outside, and
  stage alone, which that rounding no longer separates, is priced as a route the CRM's odds carry rather than its own.
- 2026-11-10, seeds 1101 to 1124 scanned for a world whose graded figures sit mid-bin at the new roundings with the
  band's step the same with and without the estimation uncertainty and the pooled, trailing-twelve and stage-alone
  routes outside; 1109 failed only on seat reductions 4,000 from a 50,000 edge, 1115 only on the Team figure 4,000
  from an edge; seed 1126 chosen on the full family.
- 2026-11-10, the uploaded cut (price rise 1 March 2026, Team minimum 1 April 2026, deal creation falling from 37 to 27
  a month after March 2026, the commitment "to the nearest EUR 0.1 million"): the platform's holistic audit failed it
  on determinism (runs/arch2/holistic_audit.md). The P20 of 9.89 rounded to 9.9, a step met in under 80 per cent of
  outcomes, and rounded down to 9.8; the band with and without the estimation uncertainty was pinned by no file;
  the Team and open-deal figures were stated as ranges at 10,000; and the run's "recent creation" reading of the
  post-March fall made a naive pipeline view fail the draft on its own. Repaired in the generator: the commitment
  defined as the largest 0.1 million step met in at least 80 per cent of outcomes (prompt, policy 5.3); policy 5.2
  files what the range carries; the two note figures asked at the precision the defensible methods pin; the creation fall removed (flat since 2024);
  the price rise and the minimum moved to 1 January 2026 so the trailing year carries the whole step and the padded
  seats; the world re-seeded so every graded figure sits mid-bin at its rounding.
- 2026-11-10, a world with the price rise at 1 March 2026 and the creation fall removed (seed 1107, scratch v1 and
  v2): every trailing extrapolation cleared the golden by 0.08 to 0.5 million only, because the trailing year's new
  Business, expansion and churn ran below the forward's while only the price line ran above; with the rise and the
  minimum at 1 January and the creation trend ended in 2024 (v3) the trailing views clear by 1.2 million.
- 2026-11-10, the exit model without a utilisation term priced as a hurried route: in the March-calendar world it moved
  accounts lost by 60,000, in the chosen world by under 2,000 (the term carries the seat cuts, not the exits), so it is
  a rival inside the bin (SF24), and the pooled route and independent draws carry R4's loss.
- 2026-11-10, the book's trailing true-up rate at accounts near their seats as a rival for seat additions: 60,000 under
  the drift forms in every world measured (it ignores each account's own growth and the ramp of young accounts); priced
  as a hurried route; the drift windows 12, 18, 24 and each account's own trailing rate stay the family, which with
  need growth less dispersed (NEED_GROWTH_SD 0.03) lands in one step.
- 2026-11-10, the pooled renewal route's seat-reduction gap as a structural result: in the uploaded cut pooled rates
  gave 310,000 against 200,000, in the first re-seeded worlds the two coincided; the gap was the cut's mix against
  the history's, not the process. The process now carries it: utilisation at signing drifts down year by year, so
  the forward book's renewals cut and leave more than the pooled history says; the direction still varies by world
  and the chosen seed's gap is asserted.
- 2026-11-10, the common factor of 0.25 the platform run assumed, as a defensible rival: nothing in the records supports
  it and policy 5.2 rules it out; in the chosen world it widens the 80 per cent range by about a third and moves the 20th
  percentile down by under 20,000, inside the step, so it is priced as a route the sentence settles rather than one the
  step separates (SF21).
- 2026-11-10, Team seasonality in the hurried "last three months" route: in the uploaded cut the last three months
  sat one 10,000 bin under the golden because the April shock had decayed to its floor by August; with the plan's
  cancellations running with the calendar (an autumn peak in every year of the history) a three-month window
  carries a season and lands 60,000 to 160,000 under the golden in every world measured.
- 2026-11-10, the two note figures at the nearest EUR 50,000: the win odds by stage and deal age put the open deals' part
  20,000 above the stage-and-staleness golden, so at 50,000 the defensible family straddled a bin edge in the chosen world;
  asked at the nearest EUR 0.1 million the family lands in one bin with margin, the CRM's odds stay far outside, and
  stage alone, which that rounding no longer separates, is priced as a route the CRM's odds carry rather than its own.
- 2026-11-10, seeds 1101 to 1124 scanned for a world whose graded figures sit mid-bin at the new roundings with the
  band's step the same with and without the estimation uncertainty and the pooled, trailing-twelve and stage-alone
  routes outside; 1109 failed only on seat reductions 4,000 from a 50,000 edge, 1115 only on the Team figure 4,000
  from an edge; seed 1126 chosen on the full family.
- 2026-11-10, architecture 2 after the holistic-audit repair (seed 1126; commitment the largest EUR 0.1 million step met in 80 per cent of outcomes, 10.0, met in 83 per cent, 10.1 in 69; draft 10.3, met in 36; every naive extrapolation 10.72 to 11.49 clears it; judge DETERMINISTIC APPROVE): measured against the uploaded platform run's own methods (price by size, renewals on utilisation and first renewal, pipeline by stage and time in stage, the Team plan's last three months, recent deal creation), the run lands the commitment and earns R1, R2 and R5, scoring 66.5 of the 93 graded weight (R3 and R7 missed, R4 partly); its two blind spots cancel (lost accounts about 130,000 low without the group term, Team about 76,000 low on the autumn peak). Two world moves were measured and rejected: the Team cancellation peak moved to late winter shifted the golden as far as the route (commitment 10.2, the draft met in 78 per cent); the seat-growth spread restored to the uploaded world's (0.08 a year, monthly noise 0.008) brought back the run's seat-addition miss (routes on pooled rates at 9.8 and 9.9) but spread the honest family over two steps (10.0 and 10.1). The routes table shows why: the five designed judgments each move the 80 per cent figure of a 10 million book by 0.0 to 0.15 million, inside the honest family's own spread, and only the CRM's odds (10.73), independent draws (10.39) and pooled renewals (10.29) separate, all three moves the uploaded run did not make. The determinism the audit requires (the band's contents filed, no added allowance) removes the stacked pessimism that made the uploaded run miss by 0.7 million. The world is spent: a commitment on one total aggregates every judgment below the methods' disagreement. Re-root to a new world in which each judgment flips units of a set or count.
- 2026-11-10, architecture 3 at the draw, a ranked list under a budget cap (best value per euro first until the next line would not fit): over two million cost and budget configurations searched against every rival, the robust cuts (a 7 to 12 per cent gap, leftover budget fitting no unfunded line) turned on one or two lines (the social Kreisblatt and telemarketing Kreisblatt pair) and a careful run that used the reading log landed the golden list, because the full-price and returns shortcuts cancel on the deep-intro lines; replaced by the standard's line-by-line bar (3.5 times the planned cost per start), on which ten lines sit 3 to 14 per cent from the bar, every rival funds the same eight and the shortcuts fund six distinct wrong sets.
- 2026-11-10, the base's December 2027 count as R9: the October 2026 base is mostly long-tenured, so the careful pass's errors cancel (the rise read late adds 3 to 4 per cent, customer-number returns take 2.5 off) and it lands within half a per cent; replaced by the intro subscribers at the cut carried to the full price in December 2027, which the careful pass misses by 6 to 9 per cent.
- 2026-11-10, a first debit able to fail in the engine: a subscription could end before it began, colliding with the withdrawal code for January 2023; failures now start at the second billing, and the pack reproduces the simulator's panel field for field.
- 2026-11-10, stage 4, R9 as the October 2026 intro subscribers paying full price in December 2027: priced on the rubric split, a careful run that read the April 2025 rise in full earned R6 and R9 together (both asks, both carried by the rise's first-year response) and scored 62.1; R9 is now the plan's 2027 starts still paying on 31 December 2027 by channel, carried by the full price at the end of intro and the newest starts' survival, and that variant scores 48.4.
- 2026-11-11, the platform's holistic audit of the uploaded build (returned on determinism): R9 counted the telemarketing free quarter as paying (498 against about 454 on 31 December 2027; standard 2.2), nine lines sat 5 to 7 per cent from the 3.5 bar and J12 had never run on telemarketing or cashback, so a 20 per cent shift in exit rates moved the call from 7 to 15 lines. Repaired: R9 counts no free month; TEL-BHR ran J12 from May 2024 to February 2025 and PART-GAZ from January to September 2024, so both 2027 J12 lines carry an offer their channel ran; the plan's costs per start re-placed so every line sits 12 per cent or more from the bar.
- 2026-11-11, wider margins on the uploaded world (habit drift 0.65 and 0.50, a full-price coefficient of 2.2): with every line 10 per cent or more from the bar the careful pass's social lines needed two shortcuts together (the reading and the period term, each 9 to 18 per cent), so the reading hint and the full-price hint each rescued the funded set and completion alone flipped nothing; the call would have hung on whichever of the two a run made. The process now carries both more strongly (the newest social starts' habit 0.9 lower, cashback 0.7, a full-price coefficient of 3.0), so each single judgment moves lines past the margin: completion alone funds SOC-KBO, the period term SOC-KBO and APP-KBO, and no hint rescues the set.
- 2026-11-11, a calibration of each line on its own newest starts (observed over expected full-price cancellations, shrunk by a pseudo-count) as a rival: it moves SOC-KBO 24 per cent up and swings 8 to 37 per cent with its own pseudo-count and window, because each line's starts of the twelve months to October 2026 have had 3 to 18 full-price cancellations (139 in all, against 146 the reading model and 138 the channel model expect); the count cannot separate the models, so the rival is ruled out on its data rather than banded, and the closing passage and the Checks sheet name it.
- 2026-11-11, a household bootstrap as the forcing evidence: drawing households ignores the line-month campaigns that move a month's starts together and gave line spreads of 3 to 5 per cent; whole start months are now drawn within each line (boot.py, each copy keeping its own customer numbers, fingerprints and addresses so the links rebuild inside it), spreads 2 to 7 per cent, and 39 of 40 draws fund the same eight lines.
- 2026-11-11, a back-test of the leaving model fitted on the 2024 starts and scored on the 2025 starts as forcing evidence: both models over-predict the later starts' exits (the reading model by 10 per cent, the channel model by 25), so it is not shipped; the reading coefficient (minus 0.69, standard error 0.03, on 2,336 cancellations) and the newest starts' measured reading carry the forcing.
- 2026-11-11, the offer and the price stepped up to as terms in the leaving model: neither improves the fit (AIC 20,339.7 and 20,334.3 against the golden's 20,335.0) and each moves line values 2 to 6 per cent; both are rivals inside the bands.
- 2026-11-12, architecture 3 as reshipped (every line 12 per cent from the bar, the clean truth and 39 of 40 redraws on the golden set): returned on determinism by the platform's review (runs/arch3/review_2026-11-12.md); the household-return projection and the young starts' completion were open modelling choices, and the return hazard fitted without early reading alone funds 9 lines (SOC-KBO 3.52), with channel completion 13 (EUR 127,830); the forcing family had tested each choice only inside the hurried route, never alone; both deciding lessons are on the client's closed page of 2026-11-12; architecture spent, re-rooted to a new world.
- 2026-11-12, architecture 4 drawn on a greater-of remuneration (the larger of 52 per cent of revenue and a per-hour floor, monthly on the service's totals): on paper the floor bound in two to four months within 5 to 9 per cent of the kink, so the regime calendar was an open fork, and the with-and-without increment it priced is a reflex (the architecture 3 run computed paired forecasts unprompted); replaced by a flat 2027 rate per counted hour, the 2026 revenue share kept as the shortcut a run carrying the latest cost files.
- 2026-11-12, at build: an AND built from the live log over-counting Gezin's re-listening: the counting rule takes a title's live position at most once, so a live-only first reach can only under-count (Gezin came out low, not high); the second correction moved to profile membership, partners folding their own subscriptions into family accounts with their history, which today's profile export credits to the family account.
- 2026-11-12, at build: the 2026 revenue share carried forward landed on the golden's plan (Gezin) while Gezin's counted hours per euro of revenue sat near Onbeperkt's; child profiles' listening moved toward re-listening and Onbeperkt's adults listen more, so taking hours out of the cost now favours Onbeperkt, and the agency fees were set from the pack's own pre-fee values over a plausible band (EUR 10 to 55) for the widest narrowest margin (24 per cent on paper, EUR 8.7 measured).
- 2026-11-12, at build: a filed fee perturbation of 10 per cent on Gezin left it EUR 3 ahead and a 10 per cent move in the 2027 rate would flip it to Flex; the rate is filed in schedule B and not fitted, so the forcing block moves the fees 10 per cent and each plan's measured counted hours 5 per cent, and the note records that R5's level is sensitive to the count's level, which the reconstruction pins exactly.
- 2026-11-12, stage 4, architecture 4 as built (Gezin EUR 22.0 per trial start, careful route Onbeperkt, pair 43.7 on paper): the determinism judge kept the order and its own first pass rebuilt R1 exactly and R2 inside the band on all four plans before it opened the blocks, merging the licence renewals and dating profiles by the charges' profile lists by reflex; disposition SEND_BACK on Gate G (planted_defect_flip: a coverage gap and a stale roster, two record corrections whose discovery is their remedy) and H3 and H5 (the compound hint naming both rescues the call); architecture spent. The lesson for the next draw: a second record the pack carries beside a reconciliation target is merged by reflex, so the deciding judgment must be an estimate whose reflexive method lands wrong, not a record to be found or re-keyed.
- 2026-11-12, architecture 5 at design: the cap response graded as a result: its estimate from counted hours (1.6) cannot recover the world's multiplier on listening time (2.3), because the cap binds on time listened, which the files do not hold; kept in the world, reaching the golden through the past downgraders' own months, and no longer asked.
- 2026-11-12, architecture 5 at design: asks for what a downgrader brings and for the leavers' listening against their plan named the two valuations' intermediates and would have handed them over; both left inside R7.
- 2026-11-12, architecture 5's first cut (Flex 9.99 to 11.49, Gezin 22.99 to 26.49): returned by the holistic audit because the 2027 Gezin and Flex rises lay outside every past rise's size and overshoot, so whether the response grows with the rise was open and a dose-scaled reading withdrew Gezin (the platform run withdrew Flex and Gezin on log-dose scaling); the audit also showed the single-run truth check too noisy to test the golden (Flex's sign at EUR 0.50 a coin flip under replays). Repaired with each rise at its own past size, the rival's July 2026 rise and a replayed truth; Flex at 10.49 with the rival unmoved (truth EUR 0.04, se 0.3) was tried and rejected as a coin flip.
- 2026-11-13, the repaired cut (Flex 10.49, Gezin 23.99, the rival's July 2026 move, Onbeperkt alone going ahead): one trick by the author's audit and the new stump factorial; against the platform run's own route (downgraders kept, own listening) the crossing alone rescued four of five results. Re-designed with three stumps; persistence after a crossing rise (light listeners leaving from the third bill to the sixth) was tried as the second and dropped: it reached only Standaard, which the crossing already holds, so it never moved the call alone.
- 2026-11-13, stage 4 pass 1 on the factorial cut: the judge sent it back because the blocks did not say Gezin's December leaving was in the golden (it always was: +8.8 without it, +6.1 with it); the blocks now give every plan's December and listening rates and the leavers' valuation, and two readings joined the golden family (the plain mean of past crossings for a plan with none of its own; responses not floored at none), widening Standaard's and Gezin's first-bill bands. Pass 2 DETERMINISTIC, APPROVE.
- 2026-11-13, the reshipped cut (9ecc8c8, Gezin alone): returned by the platform's holistic audit (runs/arch5_audit_2026-11-13.md) on two counts, both true. Standaard's 2027 crossing had no past crossing of its own and the golden's carry was wrong against the world itself (21.2 and 16.1 per 100 against a replayed 4.5 to 7.4 and 41.5 to 43.9: the other plans' crossing downgrades were held down by profile limits that never bind on Standaard, and checks.py never set R3 and R4 against the replayed truth); and Onbeperkt's call turned on one constructed second-profile uplift that one table shows. The run pasted with it (runs/arch5_run2.md) made the crossing with the profile limit and the December leavers unprompted (R61, R62), so the factorial stood on the uplift alone. Re-designed in the same world at the audit's request: no 2027 configuration the record never ran, the uplift removed, the past e-mails dated, two processes the runs named and waved through (a stop followed by paying again, N33; the stayers' consumption response, N23) run on every plan; every graded figure now checked against the replayed world.
- 2026-11-13, a backtest of the 2026 rises predicted from 2025 alone as an ask (the audit's first example): Flex's and Onbeperkt's 2025 rises passed the rival and their 2026 rises did not, and Gezin's ran the other way, so a forecast from 2025 alone needs the cross-plan carry of a never-seen kind the audit refused for Standaard (the downgrades above all); its second example, a December effect under stated e-mail dates, is taken: the price list dates every past e-mail.
- 2026-11-13, Standaard's own past crossing (the rival's Plus 30 uur at EUR 14.49 in Flanders in 2025) to pin a 2027 crossing: pinned, but Standaard then held whatever the other judgments did; the rival's Plus 30 uur at EUR 16.99 keeps every Standaard rise below it, and Flex carries the crossing instead (its own 2025 Dutch rise, the rival's July 2026 rise to EUR 10.29).
- 2026-11-13, at design: the stayers' extra listening as one flat uplift on the whole account: it cost Flex and Standaard as much per hour as Onbeperkt and put every plan below zero; it falls on the account holder and grows with their listening, so it decides Onbeperkt and moves the others little.
- 2026-11-13, at design: Standaard's EUR 1.00 rise with the returns reached only EUR +0.1 in the replayed world, too thin to force; its past and 2027 rises are EUR 1.50, the 2027 rise still its own past rise in euros.
- 2026-11-13, at build: the stayers measured as accounts paying in December and in the month read (not in every month between) counted subscriptions that left and paid again by the summer; the stayers are those on the plan in every month to the one read.
- 2026-11-13, at build: the fade fitted across the plans puts Onbeperkt's 2027 extra hours at 37.8 against the replayed world's 26; the pack's own first-quarter months (18.9, 16.4, 17.8 per cent) support the fit, the plan-by-plan fade and the observed months sit inside the band, and no reading moves Onbeperkt off hold.
- 2026-11-13, stage 4 judge pass 3 on the first repaired cut: NOT_DETERMINISTIC, SEND_BACK. "Passes the rival" read two ways: crossing from at or below the rival's price (the golden) or a new price above it, and Onbeperkt and Gezin in Flanders had sat above the rival since their own 2025 and 2026 rises, so under the second reading their Flanders 2027 cells came from crossing events (10.8 to 29.7 per 100 against the golden's 0.9 and 0.6); only one past rise (Flex's Flemish 2026, already above) told the readings apart. Closed by construction, not by a sentence: the rival's Flemish Basis 10 uur at EUR 9.79 like the Dutch one (so Flex's Flemish 2026 rise crossed from below, as its Dutch 2025 rise did), and in July 2026 the rival's Basis raised to EUR 10.29 and its Flemish Onbeperkt and Familie brought to its Dutch prices, so no plan sits above the rival before any rise and both readings classify every case alike (SF20, asserted in checks.py and verify.py). The call holds (Standaard and Gezin).
- 2026-11-13, stage 4 judge pass 4 on the fixed cut: DETERMINISTIC, APPROVE (the rival comparison rebuilt region by region for every past rise and every 2027 cell, the October base reproduced; the returns and the stayers' listening components not rebuilt by the judge, carried by checks.py against eight replays of the world's 2027). Leak reader (run on the cut before the rival alignment, a data-only change): NO LEAK.
