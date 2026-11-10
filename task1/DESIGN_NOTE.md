# task1: what December 2027 ARR Tekenbord can commit to in the board's 2027 plan

## Draw

Subdomain: Cohort and LTV modeling (retention curves, customer lifetime value), Product Analytics (`retention-cohort-lifetime-value-modeling`)
Analysis type: Forecasting & Predictive Modeling
Answer shape: A forecast path with bands, plus its drivers (the monthly ARR path to December 2027 with an 80 per cent band, the figure with an 80 per cent chance of being met, and the drivers that bridge October 2026 to December 2027)
Weight: synthesis: five flows, each set by its own mechanism and estimated from its own file, have to be carried into one path whose pieces add back and whose band keeps the dependence between accounts; task4 sat on measurement, task7 on modeling, task6 on a hard-to-measure quantity
Data-native sentence: Tekenbord's ARR moves only through contracts, invoices and renewals, while the reasons it moves sit in other systems (the price book's effective dates, the product's workspace activity, the CRM's account tree and pipeline snapshots), so each flow has to be stitched from a different pair of files before the trailing totals mean anything.
People: Naomi Weijters (CFO, owns the ARR reporting policy and the board commitment), Jelte Helmerhorst (revenue operations analyst, whose workbook and note the golden are), Floortje Huisman (head of sales, owner of the pipeline export) (`guard.py names --geo NL --seed 1107`). None appears in the prompt.

Architecture 2, 2026-11-09, a new world. Architecture 1 (Corvane, tutor-linked member retention) was returned in
kind by the project lead's review of 2026-11-09: one constructed factor (the tutors' stopping hump) placed in the
forward cohort by an onboarding pause and a surge, with every graded figure coming out of one projection.
Guard: WARN (overuse.strategy decomposition_attribution 3 of 12, answered: the strategy is the honest label, the
forecast is built flow by flow; overuse.forcing_event vote_or_meeting, the board's plan meeting is what forces it;
repeat.gate_g forecasting, the assigned analysis type; repeat.decision quantity_figure and repeat.deliverables
docx and xlsx, the board's plan takes a figure and a workbook). Nearest driver task10 at 0.06; differentiated against
mark162's spent v1 (an uptake timed at each unit's restart, one flow, against five here).
Guard at stage 5 (`guard.py heart`, 2026-11-09): BLOCK on ban.strategy (decomposition_attribution, task13), ban.forum
(board_of_directors, task13), ban.forcing_event (vote_or_meeting, task12), test.same_puzzle and test.same_driver (time,
G13 against mark162's v1 lineage, inside the batch). Every colliding card was drawn before this one, so these stood at
the draw (H27 does not apply). Probed and not taken: executive_team, line_manager_or_team and committee_or_panel each
collide (task6, task4, task7), and so do budget_or_appropriation (task6); relabelling the strategy or the decisive
pattern to clear a ban is refused by the house rule. The independent judge classed the mechanism as method or model
selection (G16), which is the honest basis for any re-description. Held at PAUSED for the author's ruling.

## Deep reasoning

Task type: retention-cohort-lifetime-value-modeling (Cohort and LTV modeling: retention curves, customer lifetime value), serving Forecasting & Predictive Modeling: the December 2027 ARR of a seat-licensed book is a sum of retention and expansion flows, each a retention-curve quantity on its own cohort (annual contracts at renewal, a monthly plan's survival, a pipeline's conversion), carried forward with a band.
Domain test: every result is a recurring-revenue quantity the field estimates: price realisation at renewal separated from seat change, seat retention at renewal by utilisation and renewal number, a monthly plan's hazard after a pricing shock, pipeline conversion by stage and age, and the ARR path with its band; swap in hospital nouns and the annual renewal calendar, licences against active users, list-price repricing at renewal and a minimum-seat rule stop making sense.
Swap: "commit EUR 9.9 million of December 2027 ARR, not the draft" with a hospital's nouns ("commit 9,900 bed-days") loses the contract anniversary on which price, seats and churn all move at once, the seat licence against the people actually working, and the pipeline's stage odds; the call stops making sense.
Where the weight sits: synthesis: five flows, each from its own pair of files (contracts and the price book; workspace activity, the workspace links and the CRM tree; Team invoices; pipeline snapshots and closed deals; the CRM's upgrade source), carried into one monthly path with a band in which a parent group's accounts move together, and a bridge that adds back to it.
Layer 1: contract lines re-exported twice by the billing system's nightly job (exact duplicate rows); renewal lines in 2024 to February 2026 issued at list price without the agreed discount and corrected by a credit note plus a re-issue; onboarding fees and part-term true-up charges on the same export; GBP contracts at the finance plan rate; Team invoices whose card payment failed and were re-issued (a failed and a paid row for one period); pipeline amounts typed per month by two owners (amount_period Monthly); a re-run snapshot export appended to the archive in four months; company and parent names in several spellings across the CRM. Each is neutral on every graded figure except R1, which grades the assembly (checks.py R2 block: kept, the duplicates, credited lines and fees break the renewal pairing visibly; the failed invoices and re-run snapshots leave R2 to R6 in their bands; amounts and names never enter the golden). The workspace links' dates are not mess: they are how an upgrade is told from a cancellation (R3, R5) and whose users sit behind each renewal (R4).
Not one thing: seven results, five flows each with its own mechanism and file pair; the strongest single piece (the pipeline's win history) moves R5 and the commitment, and a run that nails it still has to separate price from seats at renewal (R2), read the April shock on the Team plan as decaying (R3), carry utilisation, first renewals and parent-group exits into the renewals (R4) and build the path and bridge on the right flows (R7); each single shortcut alone leaves the commitment in its band or moves it to its own wrong figure (CRM odds 10.2, the run-rate of new ARR 10.1, independent draws 10.1, the list rise 10.0).
One-fact test: the most useful sentence is "old open deals rarely close, so the CRM's stage odds overstate the pipeline"; executed on the careful but hurried pass it rescues R5 and, because the pass's other errors roughly cancel at P20, R6; R2, R3, R4 and R7 stay lost, so it rescues 2 of 7 results (effort.json, computed). Every other hint rescues one or none.
Not semantics: every field read correctly (ARR on the policy's definition, the plan rate, the movement categories, the Team minimum's effective date, stage names) still leaves each hurried result wrong: nothing says how far the uplift realises, that the April exits are a decaying shock, that seat cuts follow utilisation, that groups leave together, or that stale deals rarely close.
Not rule application: the ARR reporting policy files the WHAT (what ARR is, the plan rate, each movement category) and no procedure; every forward quantity is an estimate the policy leaves to the analyst ("the plan's ARR figures are forecasts made from the company's own records").
Estimand: the ARR reporting policy (sections 2 to 4) files ARR (contracted recurring subscription charges in force at month end, annualised, at the plan rate), the population (Business contracts and Team subscriptions in force, accounts that join later included), the movement categories (new, seat additions, price, seat reductions, lost, Team change) and their order; the prompt files the window (November 2026 to December 2027), the 80 per cent range and the commitment (a December 2027 ARR with an 80 per cent chance of being met or beaten).
No decoy: the KPI export reports the months of 2026 correctly on the policy's definition and ranks nothing; the CRM's stage probabilities are the CRM's own defaults on every row; the draft target is a number in the prompt, not an argued figure.
No replay: no result re-derives a published figure; the KPI export's September ARR is a reconciliation point for R1, which is graded at October.
Pinned: rivals run on the cut pack in generator/routes.py (RIVALS): the uplift by log seats or by size band; the exit model with utilisation as a hinge, in bins or left out; the April excess from the last three or two months or an exponential with a floor; win odds by stage and staleness or by stage and deal age; seat additions from each account's own drift over 12, 18 or 24 months, each account's trailing true-up rate, or the book's trailing rate at accounts near their seats; each result's band is the span they give at the ask's rounding (see the Results chain), and checks.py R7 asserts every rival inside every band.
Run forecast: R1 earned; R2 lost to a method shortcut (the mean uplift applied flat, EUR 370,000); R3 partly (the last three months' Team rates, EUR 1,360,000, one step under the band; the months since April as the new rate give EUR 1,280,000, dismissed own evidence); R4 partly (pooled renewal rates put seat reductions at EUR 310,000, accounts lost stays in band); R5 lost to a method shortcut (the CRM's stage odds, open deals EUR 970,000, all new Business EUR 1,690,000); R6 lost (the shortcuts together with independent draws, EUR 10.2 million, wrongly clearing the draft); R7 lost (the path on the hurried flows runs out of the band from early 2027).
Strategy label: WORKS IN FORM (Left truncation and immature cohorts, the April shock's survivors; Heterogeneity that pooling hides, carried to the renewal book the decision serves; Uncertainty that matches the design, clustered by parent group).
Depth level: 5. Five independent judgments each move a graded figure (uplift realisation, the decaying April hazard, utilisation-led seat cuts with group exits, pipeline age, the group-clustered band); the shortcuts land on different wrong answers (top-down growth EUR 11.6 million, CRM odds 10.2, the shortcuts together 10.2, the run-rate of new ARR 10.1, independent draws 10.1, the list rise 10.0, against the golden's 9.9).
Lesson: an ARR forecast is a set of flows, each on its own clock and its own cohort; the trailing aggregate rates mix a one-off price step, a decaying shock and an ageing pipeline, and the band has to keep together the accounts that leave together.

## Results chain

| ID | Result (checkable) | Area | Pinned by | Band | Hurried analyst | Depends on | Graded as |
|---|---|---|---|---|---|---|---|
| R1 | ARR on the books at 31 October 2026, Business EUR 6,970,000 and Team EUR 1,930,000 | assembly and reconciliation | the ARR reporting policy 2 (contracted recurring charges in force, plan rate, one-off charges out, Team from the paid invoice); the contract lines and Team invoices; the KPI export's September figure reproduces | exact at the nearest EUR 10,000 | method shortcut: every exported line in force summed (duplicates and credited lines kept), Business EUR 7,120,000 | - | Ask 1 |
| R2 | the price line of the bridge, November 2026 to December 2027, EUR 300,000 | decomposition and attribution | policy 4.3 (the change in price per seat at renewal on the seats held before it); the 396 repricings since 1 March 2026 | the rivals' span, EUR 300,000 (log seats or size bands) | method shortcut: the mean realised uplift applied flat (EUR 370,000) or the list rise (EUR 430,000) | - | Component 1 |
| R3 | Team ARR in December 2027 from the accounts on the Team plan at 31 October 2026, EUR 1,370,000 | missingness and measurement | Team invoices; the minimum's date in the price book; the dated workspace links (upgrades) | the rivals' span, EUR 1,370,000 to 1,390,000 | dismissed own evidence: the months since April carried as the new rate (EUR 1,280,000); the careful pass's last three months (EUR 1,360,000) sits one step under | - | Ask 3 |
| R4 | Business seat reductions EUR 200,000 and Business accounts lost EUR 860,000 | investigation loops | workspace activity through the dated links to accounts; the CRM's parent accounts; the 2,224 renewals since 2022 | the rivals' span, EUR 190,000 to 200,000 and EUR 850,000 to 890,000 | method shortcut: pooled renewal rates (seat reductions EUR 310,000); accounts independent (lost EUR 630,000) | - | Component 2 |
| R5 | new Business ARR signed November 2026 to December 2027 EUR 1,350,000, of which deals open at 31 October EUR 630,000 | forecasting | pipeline snapshots and closed deals; the first contracts of won deals; the CRM's lead source | the rivals' span, EUR 1,350,000 to 1,370,000 and EUR 630,000 to 660,000 | method shortcut: the CRM's stage odds (open deals EUR 970,000, all EUR 1,690,000), the trailing run-rate of new ARR (EUR 1,550,000), stage alone (EUR 680,000) | - | Ask 4 |
| R6 | December 2027 ARR EUR 10,050,000, 80 per cent range EUR 9,770,000 to 10,320,000, the 80 per cent figure EUR 9,890,000: commit EUR 9.9 million, the draft's 10.2 does not clear | uncertainty | the prompt (80 per cent range, the commitment); the parent accounts in the CRM; every flow above | the rivals' span at the nearest EUR 0.1 million, 9.8 to 9.9 | self-confirming check: accounts drawn independently (EUR 10.1 million); the careful pass EUR 10.2 million | R2, R3, R4, R5 | Recommendation |
| R7 | the monthly path November 2026 to December 2027 and the bridge adding back to December | synthesis | policy 4's categories in order; the path's own months | each month within the rivals' span | unfinished chain: the path built on the hurried flows (out of band from early 2027), or growth carried forward (EUR 11.6 million) | R1 to R5 | Ask 2 |

Carry-forward: R1, R2, R3, R4 and R5 each stand on their own files and are graded on their own; R6 falls with R2 to R5 and R7 with every flow; no analytical result feeds more than R6 and R7 (two of six others).

## Hidden factor record

| Factor | Real or constructed | Only in deciding units | Found by | Fix depth | Verdict |
|---|---|---|---|---|---|
| realised uplift falling with contract size (negotiated renewals) | constructed as a negotiation process at every 2026 renewal | no: all 400 or so 2026 repricings carry it; the hurried flat rate misreads every remaining contract | modelling: the per-seat price change at renewal separated from the seat change, against size | modelling | keep, one of five |
| the April minimum's exit shock decaying to a smaller lasting excess | constructed as customers' response to a price change | no: every padded account, every month since April; the trailing rates misread the whole Team book | modelling: excess hazard by months since the minimum against each account's own base | modelling | keep |
| seat cuts at renewal following utilisation, most at first renewals | constructed as buyers right-sizing licences | no: every renewal 2023 to 2026 | modelling: activity stitched through dated workspace links to accounts, against each renewal | modelling | keep |
| parent groups consolidating vendors | constructed as procurement behaviour | no: groups leave across the whole history; the deciding effect is in the band | modelling: the group term in the renewal model and the band's draws | modelling | keep |
| stale deals rarely closing | constructed as sales process | no: every snapshot since 2023 | modelling: win odds by stage and months in stage from snapshots with complete follow-up | modelling | keep |

## Effort test

| Result | Quick pass | Careful but hurried | Thorough |
|---|---|---|---|
| R1 opening ARR | Missed | Right | Right |
| R2 price line | Missed | Missed | Right |
| R3 Team book left | Missed | Partly | Right |
| R4 seat reductions and lost | Missed | Partly | Right |
| R5 new Business ARR | Missed | Missed | Right |
| R6 December 2027 and the commitment | Missed | Missed | Right |
| R7 path and bridge | Missed | Missed | Right |
| Roughly | 0 of 7 | 2 of 7 | 7 of 7 |

Measured by: .claude/skills/stumping/effort.py on generator/effort.json
Largest single hint: old open deals rarely close, so the CRM's stage odds overstate the pipeline; rescues 2 of 7 results (R5 and R6)
Pair estimate: 33.6

## Data provenance

Source: generated by task1/generator from a simulated process (sim.py), seed 1107; Dutch, German and British company names drawn from Faker locales, every organisation, person, account and figure invented.
Behaves like the real thing: annual Business contracts renew on their anniversaries, true up seats mid-term when more people work in the product than they licensed, reprice to the new list at a negotiated uplift from March 2026, cut seats toward the people actually working and leave more often at first renewals and low utilisation, and leave together when a parent group consolidates; Team accounts pay per member monthly, from April 2026 for at least three seats, cancel on a hazard that falls with age, grow and upgrade to Business; deals move through four stages and go cold when they stall.
Genuine patterns: (1) seasonality in Team sign-ups and deal creation; (2) growth of the book with a slowdown in new deals after the price rise; (3) utilisation ramping in a new account's first months; (4) heterogeneity in need growth across accounts; (5) the April shock and its decay; (6) first-renewal right-sizing; (7) clustered exits within groups.
Problems by process: nightly re-exports duplicating contract lines; credit notes and re-issues; onboarding fees and part-term charges on the contract export; failed card payments re-issued; monthly-typed pipeline amounts; re-run snapshot exports; company and parent names in several spellings. Benign oddities that decide nothing: workspace ids as hashes, boards edited beside active users, loss reasons on closed deals, industries in the CRM.
Breadth: 12 files (10 used, in csv, xlsx and pdf); 4,280 contract lines on 1,018 Business accounts; 160,502 Team invoice rows on some 9,600 Team accounts; 206,037 workspace-months; 11,294 workspace links; 10,684 pipeline snapshot rows and 1,734 closed deals; two distractors (support_tickets_2026.csv, nps_responses_2026-q3.csv), named only in metadata.json.

## Template check

Chain signature: assembly-reconciliation, decomposition-attribution, missingness-measurement, investigation-loops, forecasting, uncertainty, synthesis
Question form: how-much (the commitment), then whether the draft clears it, with the path, the bridge and four component figures asked as their own quantities
Nearest build: task4 (an allocation with its sensitivity, measurement weight) and task7 (scenarios with a flip, modeling weight): different shape, weight and chain; the client's strategy 6 (a paying base whose history started late) shares the forecast-with-bands shape but its chain is delayed entry, exit types, model choice on held-out cohorts and band coverage; none carries a seat book's renewal mechanics, a price step at anniversaries or a pipeline. Abstraction sentence ("a forward total is a sum of flows each on its own clock, and trailing aggregate rates mix a one-off step, a decaying shock and an ageing pipeline") is not writable against a build on file.

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
| SF12 | the 80 per cent range | 10th to 90th percentile of December 2027 ARR | as filed | prompt |
| SF13 | the commitment | the 20th percentile (met or beaten 80 per cent of the time) | as filed | prompt |
| SF14 | the window | 1 November 2026 to 31 December 2027, month ends | as filed | prompt |
| SF15 | the CRM's monthly-typed amounts | annualised | annualised | same call (asserted); the golden prices deals on quoted seats |
| SF16 | uplift form | log seats or size bands | either | same call, inside the band (asserted) |
| SF17 | the April excess's lasting level | last three months, last two, or exponential with floor | any | inside the band (asserted) |
| SF18 | seat additions | per account trailing rate or the book's rate at accounts near their seats | either | inside the band (asserted) |
| SF19 | rounding | ARR to the nearest EUR 10,000, the commitment to EUR 0.1 million | as filed | prompt |

## Closure table

| Axis | Closure |
|---|---|
| 1 Population | Business contracts and Team subscriptions in force at each month end, later joiners included: policy 2.1, 2.5 |
| 2 Unit of account | the billing account; parent groups only for dependence (CRM) |
| 3 Attribution window | November 2026 to December 2027: prompt (SF14) |
| 4 As-of dating | exports to 31 October 2026, pulled 3 November 2026 |
| 5 Version basis | the 2026 price book (list from 1 March 2026, Team minimum from 1 April 2026); policy version 4 |
| 6 Denominator | none graded |
| 7 Weighting | each account once; ARR-weighted sums |
| 8 Window length | rivals over every defensible fitting window inside the band (SF16 to SF18) |
| 9 Boundary inclusivity | in force at the month's last day: policy 2.1 |
| 10 Rounding path | unrounded to the end; prompt (SF19) |
| 11 Tie-break | none: the commitment sits clear of the draft |
| 12 Maturity and censoring | renewals after the cut are forecast; the April cohort's lasting excess estimated (SF17) |
| 13 Order of operations | policy 4's movement order (SF8 to SF11) |
| 14 Row order | none depends on order |
| 15 Duplicate resolution | contract line id once; credited lines replaced; failed Team invoices dropped (SF4, SF5, SF7) |
| 16 Identity normalisation | billing account id across files; CRM names not used as keys |
| 17 Netting against gross | credit notes net their lines (SF4) |
| 18 Dimensional units | EUR and GBP at the plan rate; amounts per year or per month (SF2, SF15) |
| 19 Code and status semantics | line types; invoice status; stage names |
| 20 Integerisation | seats whole on the contract; expectations kept real |
| 21 Clause scope | policy 2 for ARR, 4 for the bridge |
| 22 Forward window contents | renewals, true-ups, deals and sign-ups after the cut, forecast |

## Literal reader

The policy executed word for word gives the October 2026 ARR (R1) exactly and defines each bridge line; the prompt
fixes the window, the 80 per cent range and the commitment as the 20th percentile; every forward figure is an
estimate the text leaves to the analyst, and every literal alternative in the fork table lands on the same graded
figures or is ruled out by the sentence named.


Leak rulings (leak.py, 2026-11-09, REVIEW): sweep 4, five common words in the policy (renewal, months, account,
policy, monthly), harmless, the policy files definitions only; sweep 9, contract service ends and Team period ends
after 3 November 2026, harmless, terms and billing periods run forward of the export, and no event date is later than
2 November 2026. The isolated reader quoted no process sentence, found no ranking or helper file and no one thing, and
every literal sentence it quoted executes to the golden's convention. The determinism judge returned DETERMINISTIC,
APPROVE (Gate G method or model selection, analytical, no surface read; Gate H pass, one_thing none); its one
presentation note (the new Business split summing EUR 10,000 short at the rounding) is fixed, deals created from
November carrying the split's rounding.
## Prompt contract

A voice rewrite keeps: the question (the December 2027 ARR to commit with an 80 per cent chance of meeting it, and
whether the draft figure clears it); the monthly path November 2026 to December 2027 with its 80 per cent range;
the bridge October 2026 to December 2027 in the six lines (new Business, Business seat additions, price, Business
seat reductions, Business accounts lost, change in Team) adding up; the October 2026 ARR for Business and for Team;
the Team ARR in December 2027 from accounts already on the Team plan at the end of October 2026 (their December
2027 seats, never their October ARR); the draft figure EUR 10.2 million; the new Business ARR from deals open at the end
of October; a spreadsheet and a short note; ARR to the nearest EUR 10,000 and the commitment to EUR 0.1 million. It
never adds: a method, a model, utilisation, the price rise's mechanics, the April minimum, the CRM probabilities,
parent groups, a file name or who is asking.

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
