# task21: Halvergate Mutual's 2027 price-comparison-site new-business rates for three driver-age segments

Architecture 1, drawn 2026-11-11 as a new build after task10 was retired on the author's word (first filed as task19,
renumbered to task21 the same hour when two other sessions' draws took task19 and task20 on origin first). The author
assigned no domain or analysis type, so both were drawn from coverage: Opportunity Sizing & Decision Support has no
Sulfur build, and Actuarial Science & Insurance has no build of ours at all. Every figure below is the generator's own
from the cut pack (`generator/figures.json`, `generator/effort.json`), recomputed independently by
`generator/verify.py`, which imports nothing from the generator.

## Draw

Subdomain: Actuarial Science & Insurance, pricing, rating and credibility
Analysis type: Opportunity Sizing & Decision Support
Answer shape: scenarios with the point where the call flips (for under-25s and 25-to-64s the 2027 loss ratio of the
  comparison-site business across rate changes and the smallest rise that reaches the 75 per cent target; for the
  over-65s, whether the proposed 3 per cent cut adds to 2027 underwriting profit, and by how much either way)
Weight: modeling: the claims cost of the business a price Halvergate has not charged would win, which no file
  holds, rebuilt as a counterfactual book from the relation between the comparison sites' quote records (Halvergate's
  price, its rank and the cheapest rivals' prices) and the claims of the business that sold, and the loss ratio of
  the current book over a full year from experience that so far covers mostly the summer. The last two live builds
  sit on investigation (task20) and a hard-to-measure quantity (task19); task4 (third back) also sits on modeling, a
  fulfilment centre's picker hours, which shares no result with an insurer's rate change (overuse.weight answered).
Data-native sentence: on a comparison site Halvergate, a mutual, sells only where its price is the lowest, which is
  where its rating model under-estimated the risk, so the claims on the business it sold depend on how far below its
  rivals it priced; claim frequency follows the seasons while a policy year's experience to date does not; a February
  2026 refit of the model changed which business it wins for the 25-to-64s; and every renewal price is capped at what the
  same customer would pay as new business, so a new-business cut reaches the renewal book.
People: Christopher Smith, Roy Osborne, Frances Green, Jeremy Sanders (`guard.py names --geo "United Kingdom"` seeds
  1911 and 1919; George Walsh from seed 1911 was replaced after the guard's people.first warning). None appears in
  the prompt.

Card `.claude/skills/fingerprint/cards/task21.json`, registered 2026-11-11T17:47:38Z, re-checked as registered: WARN,
no BLOCK. First filed as task19 at 17:44Z; two other sessions' draws had taken task19 and task20 on origin first,
so it was renumbered before any push, and five axes the new window banned were redrawn to the honester values:
weight to modeling, context artifact to the planning paper, stump strategy to composition_mix (the won book's mix
of under-priced risks shifts with the price), forum to the executive pricing team (overuse.forum answered: the
rate plan is the executive's in a mutual), org family to a member body (Halvergate is a mutual). The WARNs,
answered:
- template.chain_near (task7 v8, scenarios with a flip point and modeling): task7 picks retrofit measures under a
  grant-per-tonne line from a lottery's effects; no result, lesson or file role is shared.
- repeat.gate_g (forecasting, task9, at the first filing): task9 forecasts a drive fleet's replacements; here the
  forecast is the loss ratio of a book the decision itself selects, and no result is shared.
- skeleton.house_lesson (vintage_or_cohort_drift on task1 v3 and task9 v1): here it is one of four lessons and decides
  only the 25-to-64 change beside the seasonal completion; the deciding lesson, selection_on_noisy_means, is on no
  build or client task on file.
- skeleton.house_shell (dial_or_cap_setting on seven live builds): a rate change is the form the executive's decision
  takes; the answer pattern (shortcuts on distinct wrong answers across three segments) and every lesson differ.
- At the first filing driver.near (0.16) against task9 architecture 10, a credit desk's request-for-quote schedule
  held at stage 4 and never shipped, whose chain costed the trades a tighter quote adds. The card's `differentiation`
  records why this is another task: an insurer's claims, a price rise that keeps the deepest wins, a seasonal
  completion, a model refit and a renewal cap, and none of task9's completion-horizon chain.
- Re-read after the READY pull (2026-11-11, before the push): `guard.py heart` BLOCKs ban.weight (task4 architecture 11,
  modeling) and ban.forum and ban.org_family (task13 v3, executive_team, cooperative_or_member_body). Neither card
  moved: both were drawn before task21 (registered 17:10:39Z and 05:06:18Z against task21's 17:47:38Z) and sat outside
  its window at the draw, when task20 v1 (17:46:15Z) and task19 were its nearest predecessors and the guard returned
  WARN. task20 re-drew as v2 at 21:06:01Z, after task21, and left the window, which now reaches task4 and task13.
  Recorded with the dates (`reduce-house-fixes` H27); H31 asks for a redraw of a ban met at the push. The forum and the
  organisation family can be redrawn cheaply (a listed insurer whose board approves the rate plan); the weight cannot,
  since modeling is where the work sits. The ruling is the author's.
- Decisive gap, generator and Gate G were redrawn at the probe from (population, G14) to (objective, G9): the first
  collided with task2 and lineage entries of task10 and task3 (test.same_puzzle, test.same_driver), and (objective,
  G9) is the honester label: the 2026 loss ratio is read correctly and is not what the decision is scored on, and the
  claims measured are those of the quotes that were kept. The calibration form was redrawn from existing_book_actuals
  (task9 holds it in the window) to realised_outcome_roster.

## Deep reasoning

Task type: Pricing, rating & credibility (Actuarial Science & Insurance, `pricing-ratemaking-credibility`), which serves Opportunity Sizing & Decision Support: each result is a rate change, the loss ratio, volume or profit a change produces, or a quantity those are built from.
Domain test: a pricing actuary sets a new-business rate change from the experience of the business written at current rates, developed to ultimate and completed to a full policy year, against a loss-ratio target, and on a price comparison site has to cost the business a changed price will win, which is not the business won now, because the insurer only wins where its price is the lowest; under the FCA's renewal pricing rule a renewal price may not exceed the equivalent new-business price, so a new-business change is also a change to the renewal book's ceiling.
Swap: "what rise should the stores put on their own-brand lines to reach a 75 per cent cost ratio, and should the over-65s' loyalty discount go ahead" keeps a price change and a target and loses a comparison-site panel that sells to the cheapest, a rating model whose errors decide which customers are won, claims that report late and follow the seasons, a policy year completed to ultimate and a regulatory cap tying renewal prices to new-business prices; none of the eight results can be stated.
Where the weight sits: modeling, in R3 and R4: the under-25 business the team's +21 per cent would win is the part of today's sales whose price sat furthest under the cheapest rival, and those sales run at 1.44 claims per predicted claim in the deepest decile of the gap against 1.13 in the shallowest; measuring that needs the quotes' rank and rival prices joined to each sale's claims across about 61,600 under-25 sales of 2025 and 2026, the claims counted against the model's predicted frequency (a cost ratio moves a tenth on one capped bodily-injury claim), the relation fitted on the gap and every quote since 1 February 2026 replayed at the new price against the three cheapest rivals moved by the market's 2 per cent.
Layer 1: four comparison-site feeds in their own layouts (Kitecompare CSV with ISO local times and pounds; Covertide JSON lines with epoch milliseconds in UTC; Brightquote semicolon CSV with day-first dates and prices in pence; Pricelark CSV in UTC whose reference scheme changed on 1 July 2025), the Covertide quotes of 14 May 2026 sent twice, the sites' monitoring quotes (postcode ZZ99), gross prices on the feeds against premiums net of insurance premium tax in the policy extract, cooling-off cancellations and mid-term lapses, nil claims and reopened claims, and the extract's one-in-fifty sample of quotes that did not sell, carried with its weight in each feed's own column. Read the careless way one at a time, each moves the counts and leaves every graded figure past R1 inside its band; none decides a result.
Not one thing: the strongest single piece is the won book's selection by price position, and a run that nails it still has to complete the current book to a full year (the experience to 31 October is two-thirds spring and summer), choose which experience represents the 25-to-64s after the February 2026 refit, count the renewal book the over-65 cut reaches, and forecast the volumes each change writes; each of those moves a different graded result.
One-fact test: "the business a higher comparison-site price wins is the business the rating model under-priced most" rescues R3 and R4, two of eight; the seasonal sentence rescues R5 and R7, two; the renewal-cap sentence rescues R6, one.
Not semantics: every field read right (gross against net of IPT, the sample weight, the rank and the rivals' prices, the model version, each claim's type, notification date and status, the renewal schedule's columns) leaves each hurried result wrong: no field holds the claims of business not yet won, the claims a summer-heavy year will add over the winter, or the retention a capped price brings.
Not rule application: the planning paper files the WHAT (the loss ratio's numerator and denominator, the cap, 2027 cost levels, the market's 2027 move, the 2027 quotes' basis, whole-per-cent changes, the range's definition, underwriting profit's parts) and the compliance policy files the renewal cap; no document says how a changed price's business is costed, how an immature year is completed, which experience represents the 25-to-64s or how retention answers a price change. With every filed rule applied, R3 to R7 are still to be estimated.
Estimand: the planning paper (PLN-2027-03, sections 2 to 6) and the renewal pricing policy (CMP-RP-04 section 3); population, Halvergate's comparison-site new business written in 2027 in each segment (the policies the 2027 quotes will produce, every one, whether or not it is sold yet), and for the over-65 question the same new business plus every over-65 customer first sold through a comparison site and due to renew in 2027; outcome, the loss ratio (ultimate claims, each capped at £250,000, at 2027 cost levels, over written premium net of insurance premium tax), and underwriting profit (premium net of IPT less those claims, the site's commission per sale and £34 servicing per policy); window, policies written 1 January to 31 December 2027, each for its policy year; unit, whole per cent of rate change and the loss ratio in per cent; comparison, the 75 per cent target, and for the cut, 2027 underwriting profit with the cut against without it.
No decoy: nothing is written to carry a wrong answer: no memo, earlier review, forecast or provider claim states a 2027 loss ratio, a rate change, a volume or a profit; the pricing team's +21 per cent for under-25s and the commercial 3 per cent over-65 cut sit in the prompt as the stakeholders' positions, and the under-25 figure reproduces from the loss-ratio method on the latest twelve months of experience, a shallower quantity that R3 prices on the golden's footing.
No replay: no result re-derives a published figure, and no stated number in the pack is wrong (rates, rate changes, commissions, the IPT rate and the cap agree across the files).
Pinned: each result's rivals were run on the cut pack (`golden.family`, 88 constructions). Under-25 rise: the business since the last rate change completed over four readings of the seasons and the latest twelve months on level, each under the extract's notification pattern and the triangles' chain ladder read at each claim's own age, each with four readings of the gap curve (log-linear on deciles, a policy-level Poisson fit, the 2026 sales alone, the decile steps): +26 to +30 against the golden's +27; at the team's +21 they put the loss ratio at 78.3 to 83.2 per cent against the golden's 79.0. 25-to-64 rise: the business HPM v7 has priced (since the last rate change), the same seasons and developments, two fitted curves: +5 to +11 against the golden's +7 (the decile steps are left out where their means do not fall with the gap, as here, where the selection is small against their noise). Over-65 cut: new business +£0.62 million, renewals -£1.99 million, in all -£1.37 million; new business alone files +£0.62 million (cut). The simulator's own expected 2027 loss ratios (`generator/truth.py`) put the smallest rises at +24 (under 25) and +7 (25 to 64); at the team's +21 the golden measures the under-25 loss ratio 8.0 per cent above the same base with the won book held fixed against the simulator's 7.3, and its base at no change runs 1.7 per cent over the simulator's expectation (25 to 64: 0.5 per cent under), the claims noise of nine months of a book, which no analyst or judge sees past; the bands hold every defensible reading of the shipped data. Asserted in `checks.py` BAR R3 to R6.
Run forecast: R3, self-confirming check: the pricing team's +21 reproduced by the loss-ratio method on the latest twelve months (74.4 at +21) and kept; R4, method shortcut: the won book's claims per unit of predicted cost held fixed as the price rises (+21, or +22 with the triangles' chain ladder). R5 and R7, method shortcut: the latest twelve months, mostly business HPM v6 priced (+26 on either development), the business HPM v7 has priced read to date and not completed over the winter (no rise at all), or experience pooled across the refit (+23). R6, method shortcut: the cut priced on new business alone (+£0.62 million, so it goes ahead). R2 earned (conversion by rank is a reflex given the feeds); R1 earned. R8, unfinished chain: it falls with R4, R5 and R6.
Strategy label: UNTESTED (the client's actuarial strategies name immature years, settlement-speed breaks, credibility and trend; the won book's selection on a comparison site, a policy year completed over its seasons and the renewal cap are this world's own)
Depth level: 5. Four independent judgments each move a different result: the won book's selection carried to the dial (under-25s), the immature year completed over its seasons (every segment's base, decisive for the 25-to-64s), the experience that represents the refitted model (25-to-64s), and the renewal book a new-business cut caps (over-65s). The shortcuts land on different wrong answers: the loss-ratio method on the latest twelve months files +21 and +26 and the cut, the same on the triangles +22 and +26, the 2026 year to date +13 and no rise, the current book completed with the won book unchanged +20 and +6 with the cut held, and pooling +18 and +23 with the cut.
Lesson: on a price comparison site the business a price wins is selected by the insurer's own errors, so a rate change changes the risk as well as the price; an immature policy year's experience is the season it covered, not the year; a rating-model change leaves only the business it priced to represent the next year; and a new-business price is also a renewal ceiling. No build or client task on file teaches the first, and the guard counts the others once or twice.

## Results chain

| ID | Result (checkable) | Area | Pinned by | Band | Hurried analyst | Depends on | Graded as |
|---|---|---|---|---|---|---|---|
| R1 | 2026 comparison-site quotes Halvergate priced, sales and conversion by segment, January to October, the four feeds conformed and the unsold sample weighted | assembly and reconciliation | the four feeds (each its own layout), each feed's weight column | counts exact; conversion to two decimals | narrow look at broad data on the quick pass only: the sampled rows counted as the quotes and the re-sent day kept; a careful run earns it (hygiene and weights are reflexes) | - | Ask 6 |
| R2 | 2027 comparison-site policies the team's proposals would write: under-25s at +21 per cent, over-65s at -3 per cent | forecasting | planning paper section 4 (the 2027 quotes are those returned since 1 February 2026, scaled to twelve months; rivals' prices up 2 per cent) and the feeds' rank and rival prices | within 8 per cent of 3,650 and 32,270 | method shortcut on the quick pass only: 2026's volumes held; a careful run earns it (conversion by rank on the feeds is a reflex) | - | Ask 4 |
| R3 | The 2027 loss ratio of the under-25 business the team's +21 per cent would win | causal reasoning | planning paper sections 2 to 4; the feeds joined to the policy and claims extracts | 78.3 to 83.2 per cent (golden 79.0) | self-confirming check: the loss-ratio method on the latest twelve months reproduces the team's +21 and, holding the won book's claims per unit of predicted cost fixed, files 74.4 (75.1 on the triangles), so the proposal looks enough | R1 | Component 1 |
| R4 | The smallest under-25 rise, in whole per cent, that brings the 2027 loss ratio to 75 per cent, with the policies and premium it writes | forecasting | planning paper sections 2 to 5 | +26 to +30 (golden +27); 1,620 to 2,340 policies and £2.3 to £3.2 million at those rises | method shortcut: the same fixed ratio files +21 (+22 on the triangles) | R3 | Ask 1 |
| R5 | The smallest 25-to-64 rise, in whole per cent, that brings the 2027 loss ratio to 75 per cent, with the policies and premium it writes | forecasting | planning paper sections 2 to 5; the claims extract's accident dates and types; the triangles; the model deployment log | +5 to +11 (golden +7); 28,570 to 62,040 policies and £17.8 to £36.9 million | method shortcut: the latest twelve months, mostly v6 business, file +26 on either development; the v7 business read to date without its winter files no rise; experience pooled across the refit files +23 | - | Component 2 |
| R6 | What the 3 per cent over-65 cut does to 2027 underwriting profit, in pounds, new business and renewals | decomposition and attribution | planning paper section 6, the renewal pricing policy section 3, the 2027 renewal schedule, the retention MI | in all within £0.4 million of -£1.37 million, the direction exact | method shortcut: the cut priced on new business alone files +£0.62 million, so the cut goes ahead | - | Component 3 |
| R7 | The 80 per cent range of the 25-to-64 2027 loss ratio at the recommended rise | uncertainty | planning paper section 5.2 (the range covers the claims the year's policies bring, drawn policy by policy) | each end within 1.5 points of 72.9 and 77.1 | method shortcut: a range drawn at the latest twelve months' +26 writes 3,530 policies and spans 66.7 to 82.7 | R5 | Ask 2 |
| R8 | The three calls: under-25 rise, 25-to-64 rise, the over-65 cut held or taken | synthesis | planning paper sections 5 and 6 | exact: the three | unfinished chain: the careful pass measures the gap's effect on today's book and never carries it to the 2027 rise, so it files +21 for under-25s, +26 for 25-to-64s and the cut | R4, R5, R6 | Recommendation |

Carry-forward: R1, R2, R5 and R6 are graded on inputs of their own (the feeds; the feeds and the planning paper's
quote basis; the claims and the model deployment log; the renewal schedule and the retention MI). R3 falls with R1's
join, R4 with R3, R7 with R5, R8 with R4, R5 and R6. A slip on the won book's selection costs R3, R4 and R8; a slip
on the seasons or the refit costs R5, R7 and R8; a slip on the renewal cap costs R6 and R8.

## Hidden factor record

| Factor | Real or constructed | Only in deciding units | Found by | Fix depth | Verdict |
|---|---|---|---|---|---|
| The business sold is the business Halvergate's model under-estimated, more so the further under the cheapest rival it priced | constructed (the simulated market: each quote's true risk, Halvergate's estimate with its error, every rival's price, the driver buying mostly from the cheapest) | no: every segment, site and month since January 2025; it decides only the under-25 rise, while its 25-to-64 and over-65 sizes move nothing graded beyond their bands | modelling: claims counted against the model's predicted frequency on the feeds joined to the sales, fitted on the price gap | modelling: the quotes since 1 February 2026 replayed at the new price against the three cheapest rivals, the conversion by rank measured on the feeds | keep (R3, R4) |
| Claim frequency follows the seasons (winter darkness and ice), while a policy year's experience to date covers the months it has run | constructed (accidents drawn month by month with each type's seasonal factor) | no: every segment and year since 2021 in the triangles and every policy since 2025; it decides the 25-to-64 rise and moves the under-25 base inside its band | one plot shows the monthly pattern; using it needs the immature year's earned months re-weighted to a full year | modelling: earned premium weighted by each month's measured claims factor, claims developed to ultimate | keep (R5, R7), one of several |
| The February 2026 refit narrowed the model's errors for 25-to-64s, so their earlier business was more under-priced | constructed (the model's error spread by version) | no: every 25-to-64 sale before 1 February 2026 against every one after, across sites and months | a targeted query: claims per unit of predicted cost by model version, after development | modelling: only the business the refitted model priced represents 2027, and it is nine months old, so it has to be completed over its seasons | keep (R5) |
| A renewal price may not exceed the equivalent new-business price, so a new-business cut lowers every capped renewal | real (the FCA's general insurance pricing rule, filed as the mutual's renewal pricing policy) | no: the whole renewal book | a targeted read of the policy against the renewal schedule | modelling: the schedule replayed with the lowered cap and retention re-read on the price change | keep (R6), a filed rule whose reach is the analysis |

## Effort test

| Result | Quick pass | Careful but hurried | Thorough |
|---|---|---|---|
| R1 2026 quotes, sales and conversion by segment | Missed | Right | Right |
| R2 2027 policies the team's two proposals would write | Missed | Right | Right |
| R3 the under-25 2027 loss ratio at the team's rise | Missed | Missed | Right |
| R4 the smallest under-25 rise and the policies and premium at it | Missed | Missed | Right |
| R5 the smallest 25-to-64 rise and the policies and premium at it | Missed | Missed | Right |
| R6 what the over-65 cut does to 2027 underwriting profit, £ million | Missed | Partly | Right |
| R7 the 80 per cent range of the 25-to-64 2027 loss ratio at the recommended rise | Missed | Missed | Right |
| R8 the three calls | Missed | Missed | Right |
| Roughly | 0 of 8 | 2.5 of 8 | 8 of 8 |

Measured by: .claude/skills/stumping/effort.py on generator/effort.json (scores quick 7.0, careful but hurried 38.5, thorough 100.0)
Largest single hint: "the business a higher comparison-site price wins is the business the rating model under-priced most"; rescues 2 of 8 results
Pair estimate: 38.5

## Data provenance

Source: generated by the generator from a simulated process
Behaves like the real thing: a GB comparison-site motor market as the FCA's 2020 market study and the pricing literature describe it: a price-led insurer sells mostly where it ranks first (4.0 to 7.0 per cent of quotes convert in 2026), its rating model and each rival's misread risk independently with a shared part, the winner's business runs above its model's predicted cost, claims follow the seasons and bodily injury reports late, and renewal prices sit under the 2022 equivalent new-business price cap.
Genuine patterns: (1) quote volumes peak in January and dip in August, by hour peaking in the evening; (2) claim frequency rises with youth, vehicle group, mileage and urban postcode areas and falls with no-claims years; (3) accidental damage, third-party damage and theft peak November to February, windscreens in late winter and summer; (4) bodily injury reports months late and settles over years, own damage within weeks; (5) monthly payers lapse more than annual payers; (6) rivals' prices rose about 2.5 per cent into 2026 and Halvergate's rate changes landed on 1 March 2024, 1 March 2025 and 1 February 2026, the last with HPM v7; (7) conversion falls by an order of magnitude from rank one to rank two, as on a price-led panel, so a rise of a fifth relative to the market keeps under a tenth of the under-25 sales.
Problems by process: each site's MI team exports its own layout (Brightquote's legacy system stores pence); Covertide's scheduler re-sent 14 May 2026 after a failed transfer; the sites' monitoring scripts quote a fixed test risk at postcode ZZ99 every few hours; Pricelark migrated its reference scheme on 1 July 2025; the policy system strips the IPT the sites show; handlers set case estimates that later settle above or below; claimants withdraw (nil) and reopen.
Breadth: 17 files (14 the analysis uses, 3 distractors named only in `metadata.json`), three driver-age segments across four sites: 414,440 quote rows, 330,722 policies, 51,608 claims and 165,000 renewals; the work is deciding which rows represent the business 2027 will write.

## Template check

Chain signature: assembly-reconciliation, forecasting, causal-reasoning, forecasting, forecasting, decomposition-attribution, uncertainty, synthesis
Question form: what (what rate changes, with how much and whether)
Nearest build: task7 v8 (scenarios with a flip point, modeling weight): a lottery's effects carried to retrofit measures under a grant line; nothing in its chain, lessons or files carries across. The abstraction sentence for the pair ("a figure moved by a change is read off a record of units the change itself selects") does not hold for task7, whose units are allocated by lottery.

## Frontier check

Precedents: R3 L29 (the incumbent's figure reproduced and kept as confirmation, self-confirming check), with L22 and L23 behind it; R4 L22 (the published formula whose generating assumption the data contradict: the loss-ratio method holds the book's risk fixed) and L23 (compared outcomes among the observed when the treatment changed who is observed: the price changes which quotes are sold); R5 L12 (pooled cohorts whose rates drift across a change) and L34 (an uncovered window filled at the level the covered part shows, not at its own); R6 L16 (priced the unit alone where the system nets it against the units it affects); R7 L34 and L12; R8 L11 (built the correction for one step and dropped it for the next, unfinished chain).
Shallow path checks: R3 and R4: the loss-ratio method reproduces the pricing team's +21 on the latest twelve months and lands near it on every development (+22 on the triangles' chain ladder read at each claim's age); the check of another kind is claims per predicted claim against the price gap on the feeds joined to the sales (the quote record at another grain), which falls from 1.44 at the deepest decile to 1.13 at the shallowest. R5: the latest twelve months pass a development check on the triangles; the check of another kind is claims per predicted claim by model version and the claims extract's months (January runs at 1.24 of the year's average, June at 0.89) against the earned months of the business HPM v7 has priced. R6: the new-business replay passes its own conversion check; the check of another kind is the renewal schedule (another grain: customers due in 2027) against the renewal pricing policy's cap.
Assumption made false: "the loss ratio of the business won moves inversely with the price (the book's risk relative to the model does not change with the rate)": false because the panel sells to the cheapest and Halvergate is cheapest where it under-estimated, tested on the feeds' rank and rival prices joined to the claims; and "the 2026 policy year's experience to date represents its full year": false because the year has run February to October, tested on the claims' months.
Forcing: under-25 rise: the golden family (40 constructions) files +26 to +30 against the line at +24, halfway to the nearest shortcut, 2 points clear; the shortcuts file +13 to +22, 2 points under the line; the gap slope, the conversion below rank one and the seasonal amplitude each moved 20 per cent keep it at +26 to +28. 25-to-64 rise: the family (16 constructions) files +5 to +11 inside the lines at +3 and +17, halfway to the year to date's no rise and the pooled +23; the perturbations keep it at +6 to +9. Over-65 cut: the call holds in all 56 constructions (the cut's effect is computed once, on the golden's curve and the renewal schedule) and under the retention slope and the over-65 conversion each moved 20 per cent (-£1.24 to -£1.49 million against the line at zero); new business alone sits on the other side at +£0.62 million. Recorded in `effort.json` forcing; `effort.py` holds every family member, shortcut and perturbation to its side.
Noun swap: nearest by `skeleton.py check`: task1 v3 (severity none: an allocation under a budget, sharing completion and vintage lessons only), depth b9efebd1 (severity none: launch sizes on loan charge-offs, sharing vintage drift and young-cohort completion only); swapped into this task, their decision form, answer pattern, mechanisms and file roles do not carry; the deciding lesson (selection on noisy means) carries from neither.

## Semantic fork table

| ID | Term or convention | Readings | Golden | Ruled out by |
|---|---|---|---|---|
| SF1 | loss ratio | incurred to date; ultimate; capped or not; gross or net of IPT | ultimate claims capped at £100,000 at 2027 cost over written premium net of IPT | planning paper 2.1 |
| SF2 | 2027 cost levels | 2026 claims as they stand; trended 5.5 per cent | 2026 cost levels raised 5.5 per cent | planning paper 2.2 |
| SF3 | Halvergate's 2027 price | the model re-indexed; 2026 price times the change | the rates in force on 31 October 2026 times (1 + change) | planning paper 2.3 |
| SF4 | rivals' 2027 prices | unchanged; up with claims; up 2 per cent | up 2 per cent on 1 January 2027 | planning paper 4.2 |
| SF5 | the 2027 quotes | 2026 to date; since the last rate change; a year's worth | those returned from 1 February 2026 to 31 October 2026, scaled to twelve months | planning paper 4.1 |
| SF6 | the smallest rise | in tenths; whole per cent; rounded | the smallest whole per cent at which the expected loss ratio is 75 or below | planning paper 5.1 |
| SF7 | a segment | driver age at quote; main driver; youngest driver | the main driver's age | planning paper 1.2 |
| SF8 | conversion | sales over sampled rows; over weighted quotes | sales over quotes priced, unsold rows weighted by each feed's weight | each feed's weight column |
| SF9 | underwriting profit | premium less claims; less commission and servicing | premium net of IPT less capped 2027 claims, the site's commission per sale and £34 servicing a policy | planning paper 6.1 |
| SF10 | the renewal book | every renewal; over-65s first sold on a site | over-65 customers first sold through a comparison site, due in 2027 (the schedule) | planning paper 6.2 |
| SF11 | equivalent new-business price | at 2026 rates; at 2027 rates after the change | at the 2027 new-business rates, so the cut lowers it 3 per cent | renewal pricing policy 3.1 and 3.2 |
| SF12 | the range | parameter interval; predictive range of the year's claims | 80 per cent of the year's outcomes, the year's policies' claims drawn policy by policy | planning paper 5.2 |
| SF13 | a claim's cost | paid; incurred; developed | ultimate, each claim capped at £100,000 | planning paper 2.1, same call under incurred with IBNR |
| SF14 | the experience a base is read from | the business since the last rate change; all business on level; the latest twelve months | the business sold from the quotes the 2027 replay starts from (since 1 February 2026), with the latest twelve months for under-25s inside the band | planning paper 4.1 (the 2027 business is those quotes'); all of 2025 and 2026 on level assumes the won book's risk does not move with its price, which the price-gap curve refutes; for 25-to-64s anything before 1 February 2026 is business HPM v6 priced (the deployment log) |

## Closure table

| Axis | Closure |
|---|---|
| 1 | Population: 2027 comparison-site new business per segment, every policy the 2027 quotes will produce, sold or not yet; filed in planning paper 1 and 4 |
| 2 | Unit of account: a policy for volume, premium and claims; a renewing customer for the renewal book; filed |
| 3 | Attribution window: policies written in 2027 for their policy year; experience windows open (the analysis), every defensible one run |
| 4 | As-of dating: every extract as at 31 October 2026, stated in each file name and the planning paper 3.1 |
| 5 | Version basis: the latest valuation of each claim; the model version on each policy is a field, not a rule |
| 6 | Denominator: written premium net of IPT; filed 2.1 |
| 7 | Weighting: unsold quotes weighted by each feed's weight; policies by earned premium in the loss ratio; asserted that dropping the weights moves R1 and leaves the rises inside their bands |
| 8 | Window length: the 2027 quote basis filed (since 1 February 2026); experience windows are the analysis, rivals run |
| 9 | Boundary inclusivity: the 75 per cent line taken as 75.0 or below; the golden's loss ratio at its smallest rise and one point below it sit clear of 75 by more than 0.03 points (asserted) |
| 10 | Rounding path: rises in whole per cent, loss ratios to one decimal, the cut's effect to £0.01 million, premium to £0.1 million, policies to the nearest 10; stated in the blocks |
| 11 | Tie-break: none needed; no two candidate changes give the same expected loss ratio |
| 12 | Maturity and censoring: claims developed to ultimate; the immature year completed over its seasons (the analysis) |
| 13 | Order of operations: cap each claim, then develop, then trend; asserted that developing before capping leaves the rises inside their bands |
| 14 | Row order: no figure depends on file order; asserted over shuffled feeds |
| 15 | Duplicate resolution: the re-sent Covertide day collapses on the quote reference; asserted |
| 16 | Identity normalisation: quote references per site's own scheme; Pricelark's two schemes both carried in the policy extract |
| 17 | Netting against gross: new business and renewal effects reported separately and netted for the call; filed 6.1 |
| 18 | Dimensional units: Brightquote prices in pence, others in pounds; gross against net of IPT; asserted |
| 19 | Code and status semantics: claim status and cancellation reasons are plain words in the extracts; none decides |
| 20 | Integerisation: policies to the nearest 10 in the blocks |
| 21 | Clause scope: the renewal cap applies to every renewal (policy 3.1); the schedule is the over-65 customers first sold through a site |
| 22 | Forward window contents: the 2027 quotes (planning paper 4.1) and the renewal schedule cover the forward year |

## Literal reader

Executed word for word, the planning paper's sections fix every result's estimand: section 2 the loss ratio and 2027
cost levels, section 3 the records, section 4 the 2027 quotes and rivals' prices, section 5 the target, the step and
the range, section 6 underwriting profit and the renewal book; the renewal pricing policy's section 3 the cap. A
literal reader still has to choose how to cost the business a new price wins, how to complete 2026's experience and
which experience to use, and how retention answers a price change: those are the analysis, and every defensible
choice was run (Pinned). No filed sentence executed literally gives another call.

## Prompt contract

A voice rewrite may not drop or change: the question (the 2027 comparison-site new-business changes for under-25s and
25-to-64s against the 75 per cent loss ratio, and whether the over-65 cut goes ahead), the opening reason the answer
is an estimate (the business is not yet written), the two incumbent positions (+21 per cent for under-25s, a 3 per
cent over-65 cut), each asked figure with its unit (the smallest rise with its loss ratio, policies and written
premium for both segments; the 80 per cent range on the 25-to-64 loss ratio; the under-25 loss ratio at the team's
21 per cent; the policies the two proposals would write; the cut's effect on 2027 underwriting profit in pounds; the
2026 quotes, sales and conversion by segment), the deliverables by type (a workbook and a few slides). It must never
add a method, a window, a file name, a warning, a rounding instruction, the word renewal in the over-65 ask, or who
is asking.

## Leak rulings

Ruled in the main thread on `leak.py --asof 2026-11-04` (verdict REVIEW, no LEAK), 2026-11-11, on the stage 4 cut:
- file names, `hpm_model_deployments.txt`: the pricing team's own deployment log of the rating model (versions, dates,
  what each changed), a record the team keeps for itself; it names no column of any extract and no step. First
  shipped as `rating_model_release_notes.txt`, which the sweep refuses by name; renamed, content unchanged.
- answer figures, 3.2 (CMP-RP-04) and 2.3 (PLN-2027-03): section numbers that coincide with a golden figure. Harmless.
- design-note vocabulary, the planning paper (13 terms), the renewal policy (4) and the deployment log (3): ordinary
  words of pricing documents (claims, policy, renewal, change, months). The planning paper files the WHAT and the
  policy the cap; neither says how a changed price's business is costed, how an immature year is completed or which
  experience to use. Harmless.
- dates after the setting, the policy extract: expiry dates (policies run into 2027) and the November start dates of
  policies sold in late October, which a policy system holds for the future and stay. The claims extract's 129
  settlement dates and the policy extract's 5,121 cancellation dates after 31 October were a generator defect (the
  simulator's later events written into an extract dated 31 October), fixed in `pack.py`; no graded figure moved, and
  `checks.py` H16 asserts it.
- prompt gate, roll call: "The pricing team wants 21 per cent for under-25s" is the incumbent's figure, priced on the
  golden's footing by the under-25 loss-ratio ask (`guide-to-prompt` rule 9). Shell quota: the "whether" form and the
  workbook-and-deck set are over the corpus caps; the over-65 question is a whether, and the author's rewrite owns the
  shell.

- the stage 4 reader (first pass, on the cut before these fixes): its flag and the judge's one blocking finding were the
  same slip, the prompt asking for the under-25 loss ratio "at the team's 15 per cent" after "The pricing team wants
  21 per cent" (left from the seed change); the prompt now names 21 in both places and gives the written premium's
  unit. It quoted the deployment log's "Risk premiums from this release are not comparable factor by factor with
  v6" as an instruction to split the 25-to-64 experience by model; the sentence went (the rebuild entry stays, a
  fact a deployment log records). It noted the renewal schedule's youngest driver at 66; the schedule now gives the
  age at renewal, 65 up. Its reading of the PDFs' creation stamps as US Eastern is its tool's local display (the
  stamps are UTC), and the planning paper created on 3 November and dated 4 November is a paper drafted the day
  before issue: both harmless. Question 6: no one thing; it placed each ask on analysis, the 2026 table on the
  feeds' layouts, weights and the re-sent day.

- the second reader (on the fixed cut): no sentence hands over a step beyond the planning paper's WHAT, no file ranks
  the options or exists only to help, and no one thing settles the asks. It saw the four sites' quote references
  interleave on one counter (now each site's own counter, in its own steps) and the renewal schedule's premiums carry
  no IPT basis (the columns now say ex IPT, as the policy extract's written premium is); its other notes (pence,
  zones, whole-book triangles, the winter spike in every segment, the member flag, the November starts) are the
  intended texture. No graded figure moved.
- the determinism judge: first pass NOT_DETERMINISTIC on the 15 against 21 per cent slip alone; re-judged on the fixed
  cut, DETERMINISTIC, APPROVE (`determinism_check_report.md`).

## Tried and rejected

- An NHS trust's theatre sessions to clear 52-week waits: the stock-against-flow conversion is conditioned away by a
  weeks-waited band, validation removals are one join, winter cancellations show in one monthly group-by, and the
  weekend day-case step is the client's court-hours lesson (marginal against average). Too many reflexes.
- A FIT screening threshold under colonoscopy capacity: it reskins the client's PSA threshold strategy (only the
  positives worked up).
- A motor loss-ratio bridge with case reserves strengthened (Berquist-Sherman): task7 architecture 3 (2026-10-14) died
  on exactly that method spread (NOT_DETERMINISTIC, SEND_BACK).
- Store closures with card-linked recapture: the noun swap is weak and a Huff fit is the runs' first move.
- A beverage levy whose threshold moves: the 2018 reformulation story is in every model's training, so the deciding
  step is a reflex.
- Fronting (young drivers placed on a parent's policy as the under-25 price rises) as the 25-to-64 judgment: at
  realistic volumes about 1 per cent of 25-to-64 sales, too small to force the call, and moving it into a named-young-
  driver segment would make it the discrete subgroup the review returns as planted.
- The curse and the refit in one segment: a mixed 2025 base with no curse landed inside the golden's band for
  under-25s (the two are one selection and cancel), so the refit sits where the curse is small (the 25-to-64s).
- An asymmetric renewal retention as the over-65 judgment: at realistic elasticities a 3 per cent cut moves capped
  renewals from about +5 to +2 per cent, still on the side where both forms agree, so it decided nothing; dropped
  rather than tuning the cut until renewals crossed zero.
- Actual-over-expected on claim cost for the gap curve: one capped £250,000 bodily-injury claim moved a 25-to-64
  decile by a fifth and the decile estimator put the rise at +21 against the truth's +9; the model's error is in
  frequency, so the curse is measured on claim counts against the predicted frequency, where the estimators agree.
- The feeds carrying only the cheapest rival: a rise that drops Halvergate to fourth or lower is then unreadable, and
  the conversion tail below third carries the curse's dial effect in a price-led market (the truth replay fell from
  +24.8 to +15.5 on two rivals), so the feeds carry the three cheapest rivals' prices, as market-position data does.
- The triangles' chain ladder read at each claim's quarter age on 30 September and applied to its 31 October value
  (stage 3): it over-developed the young books 3 to 5 per cent against the simulator's ultimates, and with the
  latest twelve months it put the hurried under-25 loss ratio at about 76.7, inside the selection's band, so the band
  graded the development choice; the rival now reads each claim's own age on 31 October, 1 to 2 per cent over.
- A 5 per cent rivals' move for 2027 (stage 3): the selection at the team's +15 then held only 0.9 points between the
  family's floor and the hurried routes; at 2 per cent the margin is 1.6 points on the loss ratio and 3 on the rise.
- A larger under-25 model error (0.25) with a softer drop below rank one (stage 3): the selection grew to about 7 per
  cent but every rate rise lost most of its effect, the under-25 rise went to +30 to +36, the team's +15 no longer
  reproduced from the loss-ratio method, and three seeds put the bases 4 to 10 per cent apart; reverted.
- All of 2025 and 2026 on level as a defensible base (stage 3): bringing older business to today's rates by its rate
  changes assumes the won book's risk does not move with its price, the very assumption the gap curve refutes, and it
  put the family's floor under the hurried routes; dropped from the family and kept as a shortcut.
- The decile steps as a curve for 25-to-64s (stage 3): their means do not fall with the gap (0.96 in the third decile
  between 1.14 and 1.13), so a step reading made the replay's loss ratio jump and put the rise at +18 to +19; the
  family reads deciles as steps only where they fall with the gap.
- HPM v7 deployed on 2 June 2025 (stage 3): its business then ran seventeen months, a full year of seasons, so a run
  that read the release notes and kept to v7 business got +6 to +8 on the plain loss-ratio method, at the edge of the
  25-to-64 band, and the range with it; the refit now lands with the last rate change on 1 February 2026, so the only
  business v7 priced is nine summer-heavy months, and the experience the refit leaves has to be completed over its
  seasons (to date it files no rise at all, pooled +23).
- Each reported claim grossed up by one over its type's notified share (stage 3): a bodily-injury claim six days old
  counted fifteen to twenty times (one of £26,761 developed to £418,000) and moved the under-25 base from 80 to 101 per
  cent between two draws of the same world; the claims not yet notified are now valued at their type's mean cost and
  the selection curve is read to 30 September, as a pricing actuary works an immature quarter.
- The £250,000 cap (stage 3): one capped claim was a twentieth of nine months of under-25 claims; at £100,000 the
  base still moves about 3 per cent between draws, the claims noise of the book.
- The original seed under the revised world (stage 3): it held every separation, but only 1.5 points between the
  family's floor and the hurried routes on the under-25 loss ratio at the team's rise; of eleven seeds scanned five
  held every separation, and 210122 holds the widest (3.2 points on that loss ratio, 4 on the rise), with the team's
  figure there the loss-ratio method's +21.
