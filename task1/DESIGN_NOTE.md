# task1: what December 2027 ARR Tekenbord can commit to in the 2027 plan

## Draw

Subdomain: Cohort and LTV modeling (retention curves, customer lifetime value), Product Analytics (`retention-cohort-lifetime-value-modeling`)
Analysis type: Forecasting & Predictive Modeling
Answer shape: A forecast path with bands, plus its drivers (the monthly ARR path to December 2027 with an 80 per cent band, the largest EUR 0.1 million step met in at least 80 per cent of outcomes, and the drivers that bridge October 2026 to December 2027)
Weight: synthesis: five flows, each set by its own mechanism and estimated from its own file, have to be carried into one path whose pieces add back and whose band carries what the policy says it carries (the accounts' and deals' outcomes, each estimated rate's own sampling error, nothing else); task4 sat on measurement, task7 on modeling, task6 on a hard-to-measure quantity
Data-native sentence: Tekenbord's ARR moves only through contracts, invoices and renewals, while the reasons it moves sit in other systems (the price book's effective dates, the product's workspace activity, the CRM's account tree and pipeline snapshots), so each flow has to be stitched from a different pair of files before the trailing totals mean anything, and the trailing totals carry a price step and a padded-seat step that will not recur.
People: Naomi Weijters (CFO, owns the ARR reporting policy and the plan commitment), Jelte Helmerhorst (revenue operations analyst, whose workbook and note the golden are), Floortje Huisman (head of sales, owner of the pipeline export) (`guard.py names --geo NL --seed 1107`). None appears in the prompt.

Architecture 2, 2026-11-09, a new world; repaired 2026-11-10 after the platform's holistic audit (runs/arch2/holistic_audit.md)
returned the uploaded cut on determinism: the commitment was not forced (a P20 of 9.89 rounded either way, the band
with and without the estimation uncertainty pinned by no file, the two note figures given as ranges at 10,000) and the
draft's verdict did not depend on the analysis. Architecture 1 (Corvane, tutor-linked member retention) was returned
in kind by the project lead's review of 2026-11-09: one constructed factor (the tutors' stopping hump) placed in the
forward cohort by an onboarding pause and a surge, with every graded figure coming out of one projection.
Guard (2026-11-10, after the repair): the card's axes were redrawn to the truest free values and `guard.py check` on
the registered card returns WARN. Strategy `forecast_method_backtest` (the judge's own class on the uploaded cut:
method or model selection on honest history, with a structural break at the January 2026 price rise and seat
minimum, a calendar pattern on the Team plan and a horizon that the trailing year misstates; `decomposition_attribution`
sits in the three-card window through task13). Decisive generator G16, method selection (the judge's reading; G13
horizon mismatch was the earlier label and collided with mark162's spent v1 on gap, pattern and decision type); the
older collision with task7 v3's lineage on (time, G16, quantity_figure) carries a differentiation line (one
development triangle projected by age there, five flows on their own clocks from five file pairs here). Forum `other`
(the CFO alone fixes the plan figure the board receives; `executive_team`, `board_of_directors` and
`line_manager_or_team` all sit in the three cards filed before this one, task6, task13 and task12) and forcing event
`other` (the 2027 plan cycle's November deadline, a budget round; `budget_or_appropriation` and `vote_or_meeting` sit
in the same window), both named in the card's notes rather than relabelled to a forum the fiction does not have.
WARNs answered: overuse.forum and overuse.objective are the corpus's shape; repeat.deliverables docx+xlsx against
task12, the plan takes a figure and a workbook. `guard.py surface` promotes one pair, task1 against task10 at 0.10
(the 99th percentile of a corpus whose pairs sit near zero), read side by side: the two prompts share only the words
commit, range, per cent and spreadsheet (a grid operator's winter reinforcement against a SaaS plan commitment), no
file name, schema or deliverable set, and the worlds share nothing.

## Deep reasoning

Task type: retention-cohort-lifetime-value-modeling (Cohort and LTV modeling: retention curves, customer lifetime value), serving Forecasting & Predictive Modeling: the December 2027 ARR of a seat-licensed book is a sum of retention and expansion flows, each a retention-curve quantity on its own cohort (annual contracts at renewal, a monthly plan's survival with its calendar pattern and a faded shock, a pipeline's conversion), carried forward with a band whose contents the reporting policy files.
Domain test: every result is a recurring-revenue quantity the field estimates: price realisation at renewal separated from seat change, seat retention at renewal by utilisation and renewal number on a book sold more seats per user each year, a monthly plan's hazard with its calendar index and a decayed pricing shock, pipeline conversion by stage and age, and the ARR path with the band a plan commitment is read from; swap in hospital nouns and the annual renewal calendar, licences against active users, list-price repricing at renewal and a minimum-seat rule stop making sense.
Swap: "commit EUR 10.0 million of December 2027 ARR, not the draft's EUR 10.3 million" with a hospital's nouns ("commit 10.0 thousand bed-days") loses the contract anniversary on which price, seats and churn all move at once, the seat licence against the people actually working, the pipeline's stage odds and the plan policy's commitment rule; the call stops making sense.
Where the weight sits: synthesis: five flows, each from its own pair of files (contracts and the price book; workspace activity, the workspace links and the CRM tree; Team invoices; pipeline snapshots and closed deals; the CRM's upgrade source), carried into one monthly path with a band in which each estimated rate is redrawn from its own sampling error and a parent group's accounts move together, read against a commitment rule and a draft that every trailing extrapolation clears.
Layer 1: contract lines re-exported twice by the billing system's nightly job (exact duplicate rows); renewal lines in 2024 and 2025 issued at list price without the agreed discount and corrected by a credit note plus a re-issue; onboarding fees and part-term true-up charges on the same export; GBP contracts at the finance plan rate; Team invoices whose card payment failed and were re-issued (a failed and a paid row for one period); pipeline amounts typed per month by two owners (amount_period Monthly); a re-run snapshot export appended to the archive in four months; company and parent names in several spellings across the CRM. Each is neutral on every graded figure except R1, which grades the assembly (checks.py R2 block: kept, the duplicates, credited lines and fees break the renewal pairing visibly; the failed invoices and re-run snapshots leave R2 to R6 in their bins; amounts and names never enter the golden). The workspace links' dates are not mess: they are how an upgrade is told from a cancellation (R3, R5) and whose users sit behind each renewal (R4).
Not one thing: seven results, five flows each with its own mechanism and file pair, and a draft that a ten-minute trailing view clears by 0.4 million or more; the strongest single piece (the pipeline's win history against the CRM's stage odds) moves R5 and the commitment, and a run that nails it still has to separate price from seats at the November and December renewals (R2), read the Team plan's last three months as an autumn peak with a faded January excess (R3), carry utilisation, first renewals and parent-group exits into a book sold more seats per user each year (R4), build the band the policy files (R6) and the path and bridge on the right flows (R7); the shortcuts land on different wrong answers (the trailing year carried forward 10.7 to 11.5, the shortcuts together EUR 10.4 million, the CRM's odds alone EUR 10.4 million, independent draws EUR 10.3 million, pooled renewal rates EUR 10.2 million, an assumed common factor EUR 10.0 million, against the golden's 10.0).
One-fact test: the most useful sentence is "old open deals rarely close, so the CRM's stage odds overstate the pipeline"; executed on the careful but hurried pass it rescues R5, R6 (2 of 7 results, effort.json, computed); every other hint rescues one or none, and no hint rescues R6, because the careful pass's commitment rides on four shortcuts at once.
Not semantics: every field read correctly (ARR on the policy's definition, the plan rate, the movement categories, the Team minimum's effective date, stage names, the range and the commitment rule as policy 5.2 and 5.3 file them) still leaves each hurried result wrong: nothing says how far the uplift realises, that the autumn is the Team plan's cancellation peak and the January excess has faded, that seat cuts follow utilisation and that the recent cohorts were sold more seats per user, that groups leave together, or that stale deals rarely close.
Not rule application: the ARR reporting policy files the WHAT (what ARR is, the plan rate, each movement category, what the plan forecast's range carries and how a commitment is read from it) and no procedure; every forward quantity is an estimate the policy leaves to the analyst ("the plan's ARR figures are forecasts made from the company's own records"), and the commitment rule applied to a wrong band gives a wrong commitment.
Estimand: the ARR reporting policy v5 (sections 2 to 5) files ARR (contracted recurring subscription charges in force at month end, annualised, at the plan rate), the population (Business contracts and Team subscriptions in force, accounts that join later included), the movement categories (new, seat additions, price, seat reductions, lost, Team change) and their order, the 80 per cent range (the 10th to 90th percentile over the outcomes of the accounts and deals on the books and those that join, the estimated rates carrying their own estimation uncertainty, nothing added beyond the records: 5.2) and the commitment (the largest EUR 0.1 million step met or beaten in at least 80 per cent of the outcomes: 5.3); the prompt files the window (November 2026 to December 2027), asks the commitment in the policy's own terms and the two note figures to the nearest EUR 0.1 million.
No decoy: the KPI export reports the months of 2026 correctly on the policy's definition and ranks nothing; the CRM's stage probabilities are the CRM's own defaults on every row; the draft figure is a number in the prompt, not an argued figure, set where every trailing extrapolation clears it and the forecast does not.
No replay: no result re-derives a published figure; the KPI export's September ARR is a reconciliation point for R1, which is graded at October.
Pinned: rivals run on the cut pack in generator/routes.py (RIVALS): the uplift by log seats or by size band; utilisation as a hinge or in bins in the exit model; the January excess's lasting level from the last three or two months or an exponential with a floor; the Team calendar index by month, by quarter or smoothed; win odds by stage and staleness or by stage and deal age; deal creation over the trailing twelve or eighteen months; seat additions from each account's own drift over 12, 18 or 24 months or its trailing true-up rate; the band with each rate redrawn from its sampling error (the policy's reading) and, as a check, without (the same step); each result's bin at the ask's rounding holds every rival (see the Results chain), and checks.py R7 asserts every rival inside every bin and the family in one bin on every graded figure.
Run forecast: R1 earned; R2 lost to a method shortcut (the mean uplift applied flat, EUR 210,000); R3 lost to a narrow look at broad data (the last three months carried forward, EUR 1,200,000, an autumn peak plus the fading excess; the months since January as the new rate EUR 1,200,000, dismissed own evidence); R4 lost (pooled renewal rates put accounts lost at EUR 750,000 and seat reductions at EUR 200,000, the second on the edge of the golden's bin, so the pass loses the component or half of it); R5 lost to a method shortcut (the CRM's stage odds, open deals EUR 1,200,000, all new Business EUR 2,250,000); R6 lost (the shortcuts together with independent draws, EUR 10.4 million, clearing the draft; the trailing views clear it too); R7 lost (the path built on the hurried flows runs out of the band from early 2027).
Strategy label: WORKS IN FORM (Left truncation and immature cohorts, the January shock's survivors read against the calendar; Heterogeneity that pooling hides, carried to the renewal book the decision serves; Uncertainty that matches the design, the band carrying the estimates' own sampling error and the group dependence, nothing else).
Depth level: 5. Five independent judgments each move a graded figure (uplift realisation, the calendar index with the decayed January hazard, utilisation-led seat cuts with group exits on a drifting book, pipeline age, the band's contents); the shortcuts land on different wrong answers (trailing extrapolations 10.7 to 11.5 million, the shortcuts together EUR 10.4 million, CRM odds EUR 10.4 million, independent draws EUR 10.3 million, pooled rates EUR 10.2 million, the list rise EUR 10.1 million, a common factor EUR 10.0 million, against the golden's 10.0), and the call holds across every defensible variant.
Lesson: an ARR forecast is a set of flows, each on its own clock and its own cohort; the trailing aggregate rates carry a one-off price step and a padded-seat step as if they recurred, a short window carries a season, and the band a commitment is read from has to carry the estimates' own uncertainty and nothing the records do not show.

## Results chain

| ID | Result (checkable) | Area | Pinned by | Band | Hurried analyst | Depends on | Graded as |
|---|---|---|---|---|---|---|---|
| R1 | ARR on the books at 31 October 2026, Business EUR 7,020,000 and Team EUR 1,830,000 | assembly and reconciliation | the ARR reporting policy 2 (contracted recurring charges in force, plan rate, one-off charges out, Team from the paid invoice); the contract lines and Team invoices; the KPI export's September figure reproduces | exact at the nearest EUR 10,000 | method shortcut: every exported line in force summed (duplicates and credited lines kept), Business EUR 7,120,000 | - | Ask 1 |
| R2 | the price line of the bridge, November 2026 to December 2027, EUR 180,000 | decomposition and attribution | policy 4.3 (the change in price per seat at renewal on the seats held before it); the 519 repricings since 1 January 2026 | the rivals' span at the nearest EUR 10,000, EUR 180,000 (log seats or size bands) | method shortcut: the mean realised uplift applied flat (EUR 210,000) or the list rise (EUR 250,000) | - | Component 1 |
| R3 | Team ARR in December 2027 from the accounts on the Team plan at 31 October 2026, EUR 1,300,000 (nearest EUR 0.1 million) | missingness and measurement | Team invoices; the minimum's date in the price book; the dated workspace links (upgrades); the calendar index read from the history before the minimum | the rivals' span at the nearest EUR 0.1 million, EUR 1,300,000 (the lasting excess from three or two months or an exponential; the index by month, quarter or smoothed) | narrow look at broad data: the last three months carried forward (EUR 1,200,000); the months since January as the new rate (EUR 1,200,000, dismissed own evidence); the trailing twelve months (EUR 1,200,000); the pre-January rates with no excess (EUR 1,400,000) | - | Ask 3, Component 4 |
| R4 | Business seat reductions EUR 200,000 (nearest EUR 0.1 million) and Business accounts lost EUR 800,000 (nearest EUR 50,000); EUR 220,000 and EUR 810,000 in the bridge | investigation loops | workspace activity through the dated links to accounts; the CRM's parent accounts; the 2,321 renewals since 2022; utilisation at signing drifting down cohort by cohort | the rivals' span at those precisions, EUR 200,000 and EUR 800,000 (utilisation as a hinge, in bins or left out) | method shortcut: pooled renewal rates (accounts lost EUR 750,000, seat reductions EUR 200,000); accounts independent (lost EUR 550,000) | - | Component 2 |
| R5 | new Business ARR signed November 2026 to December 2027 EUR 1,870,000, of which deals open at 31 October EUR 800,000 (nearest EUR 0.1 million) | forecasting | pipeline snapshots and closed deals; the first contracts of won deals; the CRM's lead source; deal creation at its trailing twelve-month rate | the rivals' span, EUR 1,840,000 to EUR 1,870,000 at 10,000 and EUR 800,000 at the nearest EUR 0.1 million (stage and staleness or stage and age; creation over twelve or eighteen months) | method shortcut: the CRM's stage odds (open deals EUR 1,200,000, all EUR 2,250,000), stage alone (EUR 900,000), the trailing run-rate of new ARR (no open-deal figure at all) | - | Ask 4, Component 3 |
| R6 | December 2027 ARR EUR 10,220,000, 80 per cent range EUR 9,940,000 to EUR 10,520,000, the commitment 10.0 (83 in 100; 10.1 only 69): the draft's EUR 10.3 million is met 36 in 100 and does not clear | uncertainty | policy 5.2 (what the range carries) and 5.3 (the commitment rule); the parent accounts in the CRM; every flow above | the rivals' span, one step, 10.0; with and without the estimation uncertainty the same step (20th percentile EUR 10,020,000 against EUR 10,050,000) | self-confirming check: the shortcuts together with independent draws (EUR 10.4 million, clearing the draft); independent draws alone (EUR 10.3 million); the CRM's odds alone (EUR 10.4 million); pooled renewal rates (EUR 10.2 million); every trailing extrapolation (10.7 to 11.5 million, all clearing the draft) | R2, R3, R4, R5 | Recommendation, Component 5 |
| R7 | the monthly path November 2026 to December 2027 and the bridge adding back to December | synthesis | policy 4's categories in order; the path's own months | each month within the rivals' span | unfinished chain: the path built on the hurried flows (out of band from early 2027), or growth carried forward (EUR 11,490,000) | R1 to R5 | Ask 2 |

Carry-forward: R1, R2, R3, R4 and R5 each stand on their own files and are graded on their own; R6 falls with R2 to R5 and R7 with every flow; no analytical result feeds more than R6 and R7 (two of six others). The bridge's lines at the nearest EUR 10,000 carry their flows' families (new Business 30,000 wide, seat additions about 20,000, accounts lost under 15,000), so a defensible method may sit a bin or two from the golden on a bridge line; the blocks state this forecast's single figures and the families are recorded here and asserted in checks.py.

## Hidden factor record

| Factor | Real or constructed | Only in deciding units | Found by | Fix depth | Verdict |
|---|---|---|---|---|---|
| realised uplift falling with contract size (negotiated renewals) | constructed as a negotiation process at every 2026 renewal | no: all 519 2026 repricings carry it; the hurried flat rate misreads every remaining contract | modelling: the per-seat price change at renewal separated from the seat change, against size | modelling | keep, one of five |
| the January minimum's exit shock, decayed to a small lasting excess | constructed as customers' response to a price change | no: every padded account, every month since January; the trailing twelve months carry the whole shock and the months since January carry its average | modelling: excess hazard by months since the minimum against each account's own calendar-indexed base | modelling | keep |
| Team cancellations running with the calendar (an autumn peak, a late-winter trough) | constructed as the plan's seasonality, with a fixed offset per calendar month and month-to-month noise so no two years repeat | no: every year of the history; the last three months misread the whole forward year | modelling: a multiplicative index fitted beside the base hazard; its forms (month, quarter, smoothed) land in one bin | modelling | keep |
| seat cuts at renewal following utilisation, most at first renewals, on a book sold more seats per user each year | constructed as buyers right-sizing licences and as sales selling larger packs over time | no: every renewal 2023 to 2026, every cohort's utilisation after signing | modelling: activity stitched through dated workspace links to accounts, against each renewal | modelling | keep |
| parent groups consolidating vendors | constructed as procurement behaviour | no: groups leave across the whole history; the deciding effect is in the band | modelling: the group term in the renewal model and the band's draws | modelling | keep |
| stale deals rarely closing | constructed as sales process | no: every snapshot since 2023 | modelling: win odds by stage and months in stage from snapshots with complete follow-up | modelling | keep |

## Effort test

| Result | Quick pass | Careful but hurried | Thorough |
|---|---|---|---|
| R1 opening ARR | Missed | Right | Right |
| R2 price line | Missed | Missed | Right |
| R3 Team book left | Missed | Missed | Right |
| R4 seat reductions and lost | Missed | Missed | Right |
| R5 new Business ARR | Missed | Missed | Right |
| R6 December 2027 and the commitment | Missed | Missed | Right |
| R7 path and bridge | Missed | Missed | Right |
| Roughly | 0 of 7 | 1 of 7 | 7 of 7 |

Measured by: .claude/skills/stumping/effort.py on generator/effort.json
Largest single hint: old open deals rarely close, so the CRM's stage odds overstate the pipeline; rescues 2 of 7 results (R5, R6)
Pair estimate: 20.8

## Data provenance

Source: generated by task1/generator from a simulated process (sim.py), seed 1126; Dutch, German and British company names drawn from Faker locales, every organisation, person, account and figure invented.
Behaves like the real thing: annual Business contracts renew on their anniversaries, true up seats mid-term when more people work in the product than they licensed, reprice to the new list at a negotiated uplift from January 2026, cut seats toward the people actually working and leave more often at first renewals and low utilisation (and the seats sold per working user have drifted up year by year), and leave together when a parent group consolidates; Team accounts pay per member monthly, from January 2026 for at least three seats, cancel on a hazard that falls with age and runs with the calendar, grow and upgrade to Business; deals move through four stages and go cold when they stall.
Genuine patterns: (1) seasonality in Team sign-ups, deal creation and Team cancellations; (2) growth of the book with deal creation flat since 2024; (3) utilisation ramping in a new account's first months and drifting down at signing cohort by cohort; (4) heterogeneity in need growth across accounts; (5) the January shock and its decay; (6) first-renewal right-sizing; (7) clustered exits within groups.
Problems by process: nightly re-exports duplicating contract lines; credit notes and re-issues; onboarding fees and part-term charges on the contract export; failed card payments re-issued; monthly-typed pipeline amounts; re-run snapshot exports; company and parent names in several spellings. Benign oddities that decide nothing: workspace ids as hashes, boards edited beside active users, loss reasons on closed deals, industries in the CRM.
Breadth: 12 files (10 used, in csv, xlsx and pdf); 3,953 contract lines on the Business accounts; 157,622 Team invoice rows; 205,333 workspace-months; 11,207 workspace links; 11,951 pipeline snapshot rows and 1,951 closed deals; two distractors (support_tickets_2026.csv, nps_responses_2026-q3.csv), named only in metadata.json.

## Template check

Chain signature: assembly-reconciliation, decomposition-attribution, missingness-measurement, investigation-loops, forecasting, uncertainty, synthesis
Question form: how-much (the commitment, in the policy's own rule), then whether the draft clears it, with the path, the bridge and four component figures asked as their own quantities
Nearest build: task4 (an allocation with its sensitivity, measurement weight) and task7 (scenarios with a flip, modeling weight): different shape, weight and chain; the client's strategy 6 (a paying base whose history started late) shares the forecast-with-bands shape but its chain is delayed entry, exit types, model choice on held-out cohorts and band coverage; none carries a seat book's renewal mechanics, a price step at anniversaries, a calendar-indexed monthly plan or a pipeline. task15 (drawn 2026-11-10, after this build) shares the answer-shape family's neighbourhood on `precut.py`'s nearest-chain screen: it is a bridge with attribution weight whose chain runs causal reasoning, modeling and validation through a trial series' nominations; this build is a forecast path with bands at synthesis weight and shares no result, file structure or question form with it. Abstraction sentence ("a forward total is a sum of flows each on its own clock, the trailing aggregate carries a one-off step and a short window carries a season, and the committed step is read from a band whose contents are filed") is not writable against a build on file.

## Semantic fork table

| ID | Term or convention | Readings | Golden | Ruled out by |
|---|---|---|---|---|
| SF1 | ARR | contracted recurring charges in force at month end, annualised; or invoiced amounts | contracted in force | policy 2.1 |
| SF2 | GBP contracts | plan rate 1.16; or a market rate | plan rate | policy 2.3 |
| SF3 | onboarding fees and true-up proration | excluded; or included | excluded | policy 2.2 |
| SF4 | a credited contract line | replaced by its re-issue; or kept | replaced | same call (asserted); the credit note references the line |
| SF5 | a re-exported duplicate line | once | once | same call (asserted) |
| SF6 | a Team account's ARR | seats billed on its latest paid invoice times twelve | as filed | policy 2.4 |
| SF7 | a failed Team invoice re-issued | the paid row | paid | same call (asserted) |
| SF8 | the price movement | price change per seat times seats before the renewal | as filed | policy 4.3 |
| SF9 | seat reductions | seats removed at renewal at the renewed price | as filed | policy 4.4 |
| SF10 | lost | ARR of a contract not renewed, at its last day | as filed | policy 4.5 |
| SF11 | an upgrade | lost from Team, new to Business | as filed | policy 4.6 |
| SF12 | the 80 per cent range | 10th to 90th percentile of December 2027 ARR over the outcomes of the accounts and deals on the books and those that join | as filed | policy 5.2; the prompt |
| SF13 | the commitment | the largest EUR 0.1 million step met or beaten in at least 80 per cent of the outcomes; or the 20th percentile rounded to the nearest 0.1 million | the largest step | policy 5.3; the prompt (SF13 was the audit's first finding: nearest rounding gave a step met in under 80 per cent) |
| SF14 | the window | 1 November 2026 to 31 December 2027, month ends | as filed | prompt |
| SF15 | the CRM's monthly-typed amounts | annualised | annualised | same call (asserted); the golden prices deals on quoted seats |
| SF16 | uplift form | log seats or size bands | either | same call, inside the bin (asserted) |
| SF17 | the January excess's lasting level | last three months, last two, or exponential with floor | any | inside the bin (asserted) |
| SF18 | seat additions | each account's own drift over 12, 18 or 24 months, or its trailing true-up rate | either | inside the step (asserted); the book's trailing rate at accounts near their seats is a shortcut (hurried) |
| SF19 | rounding | ARR to the nearest EUR 10,000; the Team and open-deal note figures to the nearest EUR 0.1 million; the commitment a 0.1 million step | as filed | prompt |
| SF20 | what the band carries | the outcomes with each estimated rate redrawn from its sampling error; or the outcomes at the point estimates | the former | policy 5.2; and the same step either way (asserted: 20th percentile EUR 10,020,000 against EUR 10,050,000) |
| SF21 | an allowance beyond the records (a common factor across accounts, a management haircut) | none; or an assumed 0.25 common factor | none | policy 5.2 ("No allowance is added to the range beyond what the records show"); the factor widens the range by a fifth or more (asserted) and in this world moves the 20th percentile down inside the same step |
| SF22 | the deal creation rate for deals not yet created | the trailing twelve months; or eighteen | either | inside the bin (asserted); creation has been flat since 2024 |
| SF23 | the Team calendar index | by month, by quarter, or smoothed | any | inside the bin (asserted) |
| SF24 | the utilisation form in the exit model | a hinge below 0.70, bins, or no term | any | inside the bin (asserted): the term shows in the seat cuts, and in this world the exit totals barely move with it |

## Closure table

| Axis | Closure |
|---|---|
| 1 Population | Business contracts and Team subscriptions in force at each month end, later joiners included: policy 2.1, 2.5, 5.2 |
| 2 Unit of account | the billing account; parent groups only for dependence (CRM) |
| 3 Attribution window | November 2026 to December 2027: prompt (SF14) |
| 4 As-of dating | exports to 31 October 2026, pulled 3 November 2026 |
| 5 Version basis | the 2026 price book (list from 1 January 2026, Team minimum from 1 January 2026); policy version 5 (September 2026) |
| 6 Denominator | none graded |
| 7 Weighting | each account once; ARR-weighted sums |
| 8 Window length | rivals over every defensible fitting window inside the bin (SF16 to SF18, SF22, SF23) |
| 9 Boundary inclusivity | in force at the month's last day: policy 2.1 |
| 10 Rounding path | unrounded to the end; the commitment by the attainment rule on the unrounded paths; prompt (SF19), policy 5.3 (SF13) |
| 11 Tie-break | none: the commitment sits two steps clear of the draft |
| 12 Maturity and censoring | renewals after the cut are forecast; the January cohort's lasting excess estimated (SF17); open deals' odds from snapshots with a complete follow-up |
| 13 Order of operations | policy 4's movement order (SF8 to SF11) |
| 14 Row order | none depends on order |
| 15 Duplicate resolution | contract line id once; credited lines replaced; failed Team invoices dropped (SF4, SF5, SF7) |
| 16 Identity normalisation | billing account id across files; CRM names not used as keys |
| 17 Netting against gross | credit notes net their lines (SF4) |
| 18 Dimensional units | EUR and GBP at the plan rate; amounts per year or per month (SF2, SF15) |
| 19 Code and status semantics | line types; invoice status; stage names |
| 20 Integerisation | seats whole on the contract; expectations kept real |
| 21 Clause scope | policy 2 for ARR, 4 for the bridge, 5 for the range and the commitment |
| 22 Forward window contents | renewals, true-ups, deals and sign-ups after the cut, forecast; the band's contents filed (SF20, SF21) |

## Literal reader

The policy executed word for word gives the October 2026 ARR (R1) exactly, defines each bridge line, says what the
80 per cent range carries (the accounts' and deals' outcomes with each estimated rate's own sampling error and nothing
else) and reads the commitment as the largest EUR 0.1 million step met in at least 80 per cent of outcomes; the
prompt fixes the window and asks in the same terms; every forward figure is an estimate the text leaves to the
analyst, and every literal alternative in the fork table lands on the same graded figures or is ruled out by the
sentence named. The audit's three readings are closed by filing (SF13, SF20, SF21) and the fourth by the world: every
trailing extrapolation clears the draft by at least two steps and the forecast misses it by at least two.

Leak rulings (leak.py, 2026-11-10, on the repaired cut, REVIEW): sweep 4, eight common words in the policy (policy,
months, commitment, renewal, carries, account), harmless, the policy files definitions and the plan-forecast
conventions and names no method; sweep 9, contract service ends and Team period ends after 3 November 2026 in the
billing and invoice exports, harmless, terms and billing periods run forward of the export by their nature, no service
start is after 1 November 2026 and the latest invoice date is 2 November 2026 (checks.py realism block). The isolated
reader (2026-11-10) quoted no process sentence (the policy's definitions and 5.2, 5.3 as WHAT), found no ranking or
helper file and no one thing, and every literal sentence it quoted executes to the golden's convention; its one
realism note, that the policy's document history lines up with the pieces the prompt needs, is answered by version 5
also setting the month-end reconciliation's deadline (6.1), a second change in the same revision.

## Prompt contract

A voice rewrite keeps: the question (the December 2027 ARR to commit, as the largest EUR 0.1 million step met or
beaten in at least 80 per cent of outcomes, and whether the draft figure clears it); the monthly path November 2026
to December 2027 with its 80 per cent range; the bridge October 2026 to December 2027 in the six lines (new Business,
Business seat additions, price, Business seat reductions, Business accounts lost, change in Team) adding up; the
October 2026 ARR for Business and for Team; the Team ARR in December 2027 from accounts already on the Team plan at
the end of October 2026 (their December 2027 seats, never their October ARR); the draft figure EUR 10.3 million; the new
Business ARR from deals open at the end of October; a spreadsheet and a short note; ARR to the nearest EUR 10,000,
the Team and open-deal figures to the nearest EUR 0.1 million. It never adds: a method, a model, utilisation, the price
rise's mechanics, the January minimum, the calendar pattern, the CRM probabilities, parent groups, what the band
carries, a file name or who is asking.

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
