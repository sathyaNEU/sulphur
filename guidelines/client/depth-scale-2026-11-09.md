# Sulfur Depth Scale (Handshake AI, 9 November 2026)

The client's five-level scale for the reasoning a task asks of the solver, with 17 real submitted tasks placed on it, each with its step chain, what flips it, why it sits at its level, how to lift it, and the reviewers' good and weak notes. Kept as the client's own text and data (the page's prose verbatim, the examples as the page stores them). **Learn from it; never template it.** The page itself says: "Every example here is a real submitted task, shortened. They show depth; they are not templates. Reusing a lesson is fine. Reusing an investigation skeleton (same trap, same detection, same fix) is a send-back." The harness reads it as ideas (`stumping` Part 3b); no build copies an example's setting, chain, trap or deliverable set.

## The page's text

Sulfur Depth Scale
Project Sulfur · reading a task's depth
How deep does your analysis go?
A five-level scale for the reasoning a task asks of the solver. Level 1 is shallow: the answer is read off the documents or the obvious calculation. Level 5 is deep: several hard calls, each one moving the answer, all the way through.
Levels 1 and 2 are sent back. At these levels, one fact settles the task. If telling the solver one thing makes the rest routine, the task is too shallow.
Level 3 is a judgment call. One real modelling insight decides it. It can be accepted when the insight is distinctive, sits on real data and holds by a clear margin. It is sent back when the step is thin, the lesson is one we already have many of, or a simple method lands on the same answer.
Levels 4 and 5 are what we want more of. The difficulty runs through the analysis, and careful work at each step earns more.
1 Lookup or rule-following
The documents give the answer Sent back
2 One-thing flip
One hidden or planted thing decides Sent back
3 One real method step
A single genuine insight decides Judgment call
4 Layered
Two or three genuine judgments carry it Aim here
5 Difficulty throughout
Many hard calls, each one matters Best
Shallow Deep
Side by side
1 Lookup
2 One-thing flip
3 One method step
4 Layered
5 Throughout
The five levels side by side
Level What decides the answer Tell one fact, and… What strong vs weak answers look like Outcome
1 A document's definition or spelled-out procedure, a single reading of a clause, or a published figure the rest is following instructions Weak answers misread one line; strong answers read it right. No analysis separates them. Sent back
2 One planted defect or shallow hidden factor, built into the data, found in one look the fix is a subtraction or a filter Answers that did everything else well still fail, because they missed the one thing. Sent back
3 One legitimate modelling insight about a real phenomenon you still have to measure and validate it Answers split on one method choice; the rest of the work is routine. Judgment call
4 Two or three connected judgments, each needing estimation several real steps remain Strong answers get every step; good answers get some and land between. Aim here
5 Many independent judgments; different shortcuts give different wrong answers most of the work remains Scores spread out: each careful step earns more, and no single step decides. Best
Judgment step (real analytical choice)
Routine step (cleaning, joins, arithmetic)
The one thing that flips it
Read from a document
Check your own task
Write down every step where a careful analyst has to make a choice. How many are there?
For each one, would a reasonable shortcut change the answer or the key figure?
Imagine telling the solver your "key insight". Is the rest now routine? Then you are at level 1 or 2.
Is the hard part something the data really shows, which still needs estimating? That is level 3 or higher.
Would different shortcuts land on different wrong answers? That is the mark of level 5.
Moving a task up a level
Make the size of an effect, not only its existence, decide the answer.
Add a second independent judgment that also moves the margin, with its own checkable figure.
Widen the margin so no single adjustment can flip the call on its own.
In your golden output, show how each later step works from the earlier figures, so careful partial work earns credit.
Spread the work over different analysis types, not one investigation template.
Please do not copy these
Every example here is a real submitted task, shortened. They show depth; they are not templates.
Reusing a lesson is fine. Reusing an investigation skeleton (same trap, same detection, same fix) is a send-back.
More on what we look for: Latest updates (9 November) .
Click any task title to read its full prompt, reference solution and review notes. Step counts and figures come from each task's committed answer and the model runs that were graded against it.

## The levels as the page defines them

### Level 1: Lookup or rule-following (Sent back)

The answer comes from reading a document correctly: a definition, a spelled-out procedure, one reading of a clause, or a figure someone already published. Once the solver reads the right line, the rest is following instructions.

Signs: A policy or FAQ in the inputs spells out the deciding steps; A decoy figure sits next to the right one in the documents; Every measurement variant gives the same answer once the reading is right; Filter, group and sum gets you there.

- **Is the fund's liquidity status Red?** (Quantitative Finance; Data Quality Monitoring & Alerting; id 251ff00c). Fund policy sets a coverage test from each holding's days-to-sell. Custody, valuation and market-volume files are provided.
  - Chain: Take NAV, cash and 68 holdings from the valuation; average daily volume from 20 days of consolidated volume (routine); Read Policy 3.9: the sale rate is the fund's own measured participation, not the 20% broker algorithm cap in the Execution Policy (from a document); Trace the fund's custody account and map its ids to ISINs (routine); Measure sales from day-on-day falls in settled positions: about 8.0% (routine); Apply the policy's own arithmetic: coverage 0.76, 33.4% beyond 20 days, Red (from a document).
  - What flips it: With the 20% cap the fund looks Green (coverage 1.83); with the policy's definition it is Red (0.76). One run took the cap; the other read the definition and got it right.
  - Why this level: The whole call rests on reading one definition. After that the policy dictates every calculation, and no measurement choice changes the result.
  - Lift: Let the policy define the goal but not the method, so estimating participation (thin trading days, partial fills, settlement lags) is real work that moves the figure.
  - Reviewers, good: The sale rate has to be built by joining three record sets (administrator, custodian, market data vendor) and handling T+1 settlement. | Every holding's days to sell and bucket can be checked line by line in the workbook. | The decoy 20% limit and the measured 8.0% lead to opposite results (Green against Red), so the stakes of the key step are clear.
  - Reviewers, weak: The data is constructed, and the whole call turns on reading one policy definition correctly; after that the policy spells out every calculation and threshold. | No reasonable variant in measuring the sale rate moves any holding to a different bucket, so the measuring work adds little depth.
  - Prompt length: 1031 characters; deliverables: AUSC_liquidity_stress_2026-10-23.xlsx with every holding's result and the fund totals, plus a one-page board note AUSC_LRC_board_note.docx with the result and recommendation.

- **Did the 30-day answered share really fall 7.6 points?** (Product Analytics; Data Quality Monitoring & Alerting; id ce649e2c). A Q&A site's data dump is used to compare answered shares across two years and decide whether to escalate.
  - Chain: Link answers to questions and compute the 30-day answered share by period (routine); Notice the monthly series steps down exactly 365 days before the snapshot (judgment); Apply the FAQ's spelled-out rule: abandoned unanswered questions are deleted after 365 days, so only the earlier year has been cleaned (from a document); Set aside later-year questions that meet the deletion conditions and recompute (routine).
  - What flips it: At face value the share falls 7.64 points (escalate). Applying the documented rule to the later year leaves 0.81 (do not escalate).
  - Why this level: One sentence from the FAQ unlocks it, and the fix is applying that sentence. Both runs saw the gap and said deleted history cannot be recovered.
  - Lift: Keep the deletion effect, but make its size need estimating (for example, from how unanswered shares decay with age), and add a second, independent step that also moves the margin.
  - Reviewers, good: Real Stack Exchange data with a genuine survivorship problem: the snapshot has already lost the earlier year's removed questions. | The clue is visible in the data itself (a step exactly 365 days before the snapshot) and can be confirmed from the age profile of unanswered questions. | Per-site and combined figures on both bases give many checkable results.
  - Reviewers, weak: It is a one-thing flip: once you know the dump leaves out removed posts, the fix is applying the FAQ's written removal rule as a filter. | The deciding step is reading what the files contain and applying a documented rule, rather than analysis that stays hard end to end. Both model runs noticed the deletions and stopped there.
  - Prompt length: 794 characters; deliverables: A one-page note answer_rate_note.docx opening with the change and the decision, and answer_rate.xlsx with question counts and 30-day shares by site and combined for both periods, plus a monthly chart.

### Level 2: One-thing flip (Sent back)

The task is mostly real analysis, but one hidden or planted thing decides the answer: a defect the author built in, or a hidden factor that sits only where it decides the call or shows in one look. Answers that do everything else well still fail, and once told, the fix is routine.

Signs: Runs that did all the other work still got the wrong answer; The deciding pattern appears only in the units being ranked or compared; One cross-tab or one plot reveals it; The fix is a subtraction, a filter or swapping the comparison group.

- **Site the new birth-registration office in Carrow or Dunmore?** (Sociology & Demography; Opportunity Sizing & Decision Support; id db3a6bc0). A registry, a completeness report and committee rules are used to estimate 2024 unregistered births by district and rank them.
  - Chain: Count births by mother's residence and reassign waiting-home lodgers (routine); Split completeness into facility and home births and apply each to the 2024 mix (judgment); Spot that Carrow's 2022 home-birth registrations include mobile drives that ended in September 2022, and remove them (the one thing); Apply the capacity rule and rank the gaps (routine).
  - What flips it: Keep the drive registrations and Dunmore comes first (5,687 vs 5,406). Remove them and Carrow leads (7,808 vs 5,779).
  - Why this level: One built-in break in how births were registered decides the district. It shows in one cross-tab of channel by year. Both runs called it the biggest risk, then did not adjust.
  - Lift: Make the size of the drive effect need estimating (the substitution share, with its confound) and let that estimate move the ranking. Add a second independent judgment, such as residence misreporting, that also matters.
  - Reviewers, good: A layered, realistic planning problem: registration district against residence, waiting-home coding, completeness by facility and home, and a capacity rule from the minutes. | Many intermediate figures can be checked, from the cleaning log to the ranking and the reconciliation flags. | A stakeholder's case (Ashbourne's overflowing wards) has to be answered with numbers, not just the ranking.
  - Reviewers, weak: The data is constructed, and the district flips on one planted break: drive registrations exist only in 2022 and only in the two leading districts, visible in a single channel by year table. | Model runs did the residence, waiting-home and completeness work and still picked Dunmore; the margin with the drives left in is small.
  - Prompt length: 1483 characters; deliverables: maternity-siting-memo.docx (decision first, ranking, the Ashbourne Regional case, robustness, two pages plus one chart) backed by district-birth-model.xlsx with cleaned counts, expected births, the capacity gap and a registry against facility reconciliation.

- **Approve the vegetation trimming cycle?** (Energy Systems & Utilities; Experiment & Causal; id c3c4e2ab). Outage records for trimmed and untrimmed circuits are used to price each avoided interruption against a $250 bar.
  - Chain: Reproduce the vegetation group's figures: trimmed circuits +5%, the rest of the system +31% (routine); Ask why untrimmed circuits got so much worse (judgment); Find that circuits sharing a contractor crew yard with the cycle rose +54% and +42%, while circuits in yards with no cycle work rose +6% (the one thing); Compare only against the clean yards and recompute the cost per interruption (routine).
  - What flips it: Against all other circuits the cycle looks like a pass at about $168 per interruption avoided. Against clean yards the effect is about −4% and the cost is $910 or more, a fail.
  - Why this level: A spillover built into the comparison group decides it. Once you know about the crew yards, picking the clean comparison is routine. The run never looked at yards.
  - Lift: Make the spillover's size need modelling (for example, scaling with each yard's share of cycle miles), and add a second real step, such as weather normalisation or cost allocation, that also moves the cost.
  - Reviewers, good: Heavy, realistic data assembly: two outage systems, time zones, restoration steps and major event days. | The cost comes from the ledger, and every circuit's figures sit in the workbook for checking. | The answer has to square with a stakeholder's own number (the fifth) rather than just ignore it.
  - Reviewers, weak: The data is constructed, and the call flips on one planted pattern (comparison circuits in shared crew yards worsening) that no document mentions. | Once the crew-yard spillover is spotted, a clean-yard comparison settles the answer quickly.
  - Prompt length: 1416 characters; deliverables: trim_cycle_recommendation.docx (two pages at most, one chart) and trim_cycle_workbook.xlsx with the estimates and one row per circuit.

### Level 3: One real method step (Judgment call)

One legitimate modelling insight about something real decides the answer, and it still has to be measured and validated. Around that step the work is routine. Level 3 is a judgment call: in our most recent review we kept about half of the level 3 tasks and sent the rest back. The examples below include both outcomes.

Signs: The hard step is a textbook method choice, not a planted pattern; The phenomenon shows across the whole dataset, not only in the deciding units; Knowing the idea is not enough: you still have to estimate it; Everything before and after the insight is routine.

Level 3 is kept when the insight is about something real and needs estimating, not just noticing, the data are real or the effect runs through the whole dataset, the lesson is distinctive and it holds by a clear margin; it is sent back when the step is thin, the lesson is one the client already has many of, or a simple method lands on the same answer (the page's call grid).

- **Will extra court sitting hours close the trial backlog?** (Criminology & Justice; Opportunity Sizing & Decision Support; id 35842bf8). Public court statistics are used to decide whether a proposed increase in hearing hours closes an annual gap of about 8,260 trial cases.
  - Chain: Annual gap from receipts minus disposals, cross-checked against the rise in open cases (routine); Recognise that an extra hour does not buy the average case: early guilty pleas and dropped cases barely use hearing time (judgment); Test it on the 2020 jury-trial pause and recovery: contested trials track hearing time, early pleas track receipts (judgment); Marginal rate of about 91 cases per 1,000 hours gives about 4,500 extra cases (routine); Split by region and estimate the Wales figure (routine).
  - What flips it: At the 4.68-hour average, the hours buy about 10,700 cases (yes). At the marginal rate they buy about 4,500 (no).
  - Why this level: Marginal versus average is a genuine insight, backed by real evidence in the data. But it is the only hard step. The run assumed marginal cases look like the average and said yes.
  - Lift: Make a second independent judgment matter, such as how receipts will grow next year or how the trial-day plea rate responds to listing, each with its own checkable figure.
  - Reviewers, good: Real Ministry of Justice published data, including awkward pivot-tool workbooks. | A genuine economics point (extra hours buy contested trials, not the average case), supported by a natural experiment in the data itself: the 2020 jury trial pause. | Regional and Wales follow-ons chain several sources and give many checkable figures.
  - Reviewers, weak: The national call rests on one insight, marginal against average cost, so the depth is concentrated in a single step. | The Wales prison figure chains several rates and per-case conversions, so it is approximate.
  - Prompt length: 859 characters; deliverables: A short PDF briefing note for ministers with the yes or no and supporting figures, plus a sortable regional spreadsheet.

- **Keep the overflow staffing agency on retainer?** (Healthcare Delivery & Health Economics; Forecasting & Predictive; id 0f7f50e0). A 130-bed hospital keeps the retainer if it expects at least one quarter in twenty with five or more overflow weeks. Public weekly hospital census data are provided.
  - Chain: Build a weekly census panel from the facility files (suppression, coverage, completeness) (routine); Question the independence that a one-in-eight rate implies, and test it: an overflow week follows another 62% of the time vs 6% after a normal week (judgment); Choose peers like the asker and count how often their quarters had five or more overflow weeks (judgment); Check robustness, multiply by twenty and compare with the one-quarter line (routine).
  - What flips it: Treating weeks as independent gives 0.33 quarters in twenty (drop the agency). Clustered weeks give about 2 (keep it).
  - Why this level: Serial dependence is a real feature of real data and needs measuring. But one insight carries the whole call. The run noted clustering could matter and never tested it.
  - Lift: Add a second piece of real work, such as seasonality in overflow or planned bed growth, that also moves the expected count.
  - Reviewers, good: Real public hospital data with realistic messiness: suppression codes, partial weeks and gaps. | The prompt's framing invites a binomial, and the data shows why that is wrong. | The answer can be checked two ways: by a model and by directly counting similar hospitals' quarters.
  - Reviewers, weak: It is essentially one statistical insight (weeks are not independent) followed by a direct count, so depth is thin. | Once clustering is noticed, the rest of the work is routine.
  - Prompt length: 999 characters; deliverables: A one-page write-up for the finance committee giving the expected number of agency quarters and the keep or drop call.

- **Keep the backup collections retainer?** (Banking, Credit & Financial Risk; Opportunity Sizing & Decision Support; id 23bec3ac). A credit union with about 400,000 loans keeps an outside collections team if there is at least a 1-in-20 chance year-end delinquencies exceed in-house capacity. Public call-report data are provided.
  - Chain: National delinquency rate from call reports and the plan count of 4,309 accounts (routine); Recognise that loans within one institution share shocks, so a loan-by-loan binomial understates the risk (judgment); Measure the spread between institutions by size and see it stops shrinking past about 50,000 loans (judgment); Read the exceedance chance and the 95th-percentile capacity from size-matched peers (routine).
  - What flips it: An independent-loan binomial gives a chance near zero (drop). The spread between similar-sized credit unions gives 0.19 and a capacity need of about 8,261 (keep).
  - Why this level: A genuine credit-risk lesson on real data. The run named the dependence risk and still used the binomial. Beyond that one step, the work is light.
  - Lift: Give the size-matching or the carry-forward of the spread a second real decision point, such as how the plan rate itself should be forecast.
  - Reviewers, good: Real regulator data that needs schedule and field lookups (count-based accounts rather than the dollar rate). | A genuine credit risk lesson: at this size the risk comes from institution-wide shocks, not loan-by-loan chance. | The key figures can be checked by direct count of similar-sized credit unions.
  - Reviewers, weak: One modelling insight carries the call, so the depth is concentrated in a single step. | The team size depends on how the peer group is chosen, and careful variants span a wide range (about 6,700 to 10,800).
  - Prompt length: 1307 characters; deliverables: A board memo of no more than 300 words with the chance, the call and the required team size, plus one chart or table.

### Level 4: Layered (Aim here)

Two or three connected judgments carry the answer, and each needs real estimation. A central idea may drive the call, but quantifying it takes several analytical steps where shortcuts are tempting. Good answers get some of the steps and land between.

Signs: Two or more steps each move the answer or the key figure; Strong runs got some steps right and lost on another; The insight still needs a reference, a validation and a range; Real public data, or synthetic data where the effect runs everywhere.

- **Repair turbine 3's night-stop fault?** (Energy Systems & Utilities; Opportunity Sizing & Decision Support; id 8ec45b05). Real wind-farm SCADA data. Turbine 3 parks at night in one wind arc. The repair pays back in six years if it saves more than 160 MWh a year.
  - Chain: Night stop hours with turbine 3's vane in the arc: about 198 MWh a year of its own output (routine); From the layout, find the turbines downwind and pick an unwaked reference (turbine 2, not 1 or 4) (judgment); Estimate turbine 5's wake deficit by direction bin and convert it to recovered energy, about 102 MWh a year (judgment); Validate against turbine 3's real outages and pick up turbine 6's offsetting loss; bootstrap by event (judgment); Correct to a normal wind year with a 30-year reanalysis fit; repeat for the wider arc, which flips to repair (judgment).
  - What flips it: Turbine 3's own output (about 200 MWh) says repair. The farm's net loss, after turbine 5 recovers its wake, is about 109 MWh, below the 160 break-even.
  - Why this level: Wake recovery is the central idea, but turning it into a number takes a reference choice, direction binning, an outage check and a long-term correction. Both runs priced turbine 3 alone.
  - Reviewers, good: Real wind farm SCADA with realistic export quirks (comment headers, UTC timestamps, missing values). | The key insight comes from physical reasoning about the layout, and it is then quantified and cross-checked against the turbine's own real outages. | A normal-year correction and a scenario that flips the answer add genuine further steps.
  - Reviewers, weak: The depth is concentrated in the wake recovery step; the call hinges on it. | The top of the range (6.9 years) is not far above the six-year rule.
  - Prompt length: 1239 characters; deliverables: A short memo for the asset committee with the call and the normal-year energy cost with a range, the rerunnable Python script, and whether the wider arc changes the answer.

- **Has re-offending after a first arrest fallen by at least 10%?** (Criminology & Justice; Comparative & Explanation; id b34ffd70). Real city arrest and crime-report data. The board's rule needs a 90% confident drop between the 2013 to 2014 and 2022 to 2023 cohorts.
  - Chain: One arrest event per person-day; reproduce the draft −27.7% (routine); Equalise the look-back so "first arrest" means the same in both cohorts: −14.7%, still passes (judgment); Count only re-arrests for new crimes (routine); Link arrests to crime reports: the share of reported crimes ending in arrest fell from 18.9% to 11.9% (judgment); Deflate later re-arrests by the clearance ratio, offence by offence: +25.5%, fails (judgment); Bootstrap people and counts; every variant fails the rule (routine).
  - What flips it: The look-back step moves the figure from −27.7% to −14.7%. The detection step turns it into +25.5% and the answer to no.
  - Why this level: Two genuine measurement judgments, both standard in criminology, both needing estimation. Both runs flagged the caveats and stopped at recorded re-arrest.
  - Reviewers, good: Real city arrest and crime report data with duplicates, placeholder ids and a recording system change. | Two genuine analytical steps: equalising the look-back that defines 'first arrest', and recognising that re-arrest depends on how often crimes are solved. | Clear rule (90% sure) and a csv that lets an analyst check every figure.
  - Reviewers, weak: The clearance adjustment is a modelling choice with a wide spread across variants (+7.8% to +104.1%), although all of them fail the rule. | The prompt is hard to read in places, and burglary is too small (83 people) to say much.
  - Prompt length: 1109 characters; deliverables: reoffending_check_memo.pdf (two pages at most, yes or no first with the change and 90% range, by offence type with one chart) and reoffending_check.csv with one row per offence type plus everybody.

- **Launch the new refrigerated product line?** (Product Analytics; Forecasting & Predictive; id 5a6e4e0c). Household panel files and concept tests are used to forecast first-year net margin against an $18M bar.
  - Chain: Stack four panel files and two concept-test formats (duplicates, speeders, returns) (routine); Fit trial with separate conversion for category buyers and non-buyers, chosen by leave-one-out error (judgment); Carry the buyer mix into volume: about half the buyers are new to the category, and new buyers buy about one unit (1.05 vs 4.17), so 2.6 units per buyer (judgment); Estimate cannibalisation on comparable launches with a design that handles buyers' rising pre-launch trend: 51% (judgment); Combine into net margin and bootstrap over launches (routine).
  - What flips it: Either the right volume or the right cannibalisation puts net margin below $18M. The runs used 4.2 to 4.7 units per buyer from a single analog launch.
  - Why this level: Two independent places where the answer moves, each needing real modelling. Both runs built the buyer split for trial and then dropped it for volume.
  - Reviewers, good: Several independent places to go wrong (pooled intent conversion, buyer mix carried into volume, trend-biased cannibalisation), each of which flips the call. | Messy multi-source inputs: four panel formats, two concept test formats, speeders and returns. | A routes sheet shows each shortcut's result, so the reasoning can be checked end to end.
  - Reviewers, weak: The data is synthetic, and the pattern for buyers new to the type is too clean (about one unit in every past launch). | The cannibalisation figure is the midpoint of two quite different designs (35% and 67%).
  - Prompt length: 937 characters; deliverables: fresh_rolls_decision.docx opening with the call and net figure, covering households, rolls per household and cannibalised margin with a walk chart, plus fresh_rolls_forecast.xlsx with the figures.

- **Fund the De Bilt telescope dome?** (Physical & Environmental Sciences; Data Quality Monitoring & Alerting; id 41389985). Real KNMI hourly weather records for De Bilt, 1961 to 2026. The funder pays only if 2016 to 2025 averaged at least 25% clear night hours, measured on the same basis as the 2006 to 2015 record.
  - Chain: Count night hours (zero global radiation) with cloud of 2 octas or less: 28.4% in 2006 to 2015, 20.8% in 2016 to 2025 (routine); Test the drop against signals that did not change: daytime sunshine rose from 38.1% to 41.2% of daytime hours while reported clear daytime hours fell from 26.7% to 19.6%, and the gap opens in March 2016 (about -1.5 points a month before, -10.5 after) (judgment); Fit a clear-sky model on 2006 to 2015 nights (night cooling, wind, humidity, dew-point depression, month) and apply it to 2016 to 2025: 30.4% (judgment); Check nine training windows and predictor sets: 28.8% to 30.4%, every one above 25% (judgment); Report the rebuilt figure, not the raw one, and call go (routine).
  - What flips it: Read straight from the cloud field, 2016 to 2025 gives 20.8%, a no-go. Rebuilt on the 2006 to 2015 basis it is 30.4% (28.8% to 30.4% across nine versions), so go.
  - Why this level: One idea, a break in how cloud is measured, carries the answer, but turning it into a figure the funder will accept takes three connected steps: proving the break against independent signals, modelling clear sky from variables that did not change, and showing the result holds across versions. The one run flagged the instrument change as a risk but never tested it and reported the raw 20.8% as a no-go.
  - Reviewers, good: Real, unaltered KNMI data: the break is a genuine feature of the station record, not a planted step. | The raw and rebuilt figures fall on opposite sides of the 25% bar, so the key step decides the call. | The correction needs real modelling and a robustness sweep, and every reasonable version clears the bar.
  - Reviewers, weak: The prompt's comparability rule and the legend's general warning point toward the break, so the idea is hinted. | Once the break is accepted the go call is easy (the 2006 to 2015 baseline is 28.4% and sunshine rose); the remaining depth is in defending the figure.
  - Prompt length: 544 characters; deliverables: A short memo with the go or no-go call and the figure to report, plus a workbook that traces every number back to the hourly data.

- **Bind the Bluebonnet legacy medical deal at $110 million?** (Actuarial Science & Insurance; Forecasting & Predictive; id a5a5efb1). Real Texas workers' comp billing data behind 25 old claims with lifetime medical. The desk binds only if $110 million is at least 110% of expected payments discounted at 4.0% with 3.5% medical trend.
  - Chain: Roll 236,427 bill rows up to paid by claim and year, net of reversals (71,003 legacy claims), and match the 25 scheduled claims (routine); Value the schedule on the 2024 US life tables: $109M to $121M, a $120M to $133M requirement, so walk (routine); See that the 25 were picked because they are still paying, so their own records cannot show how often such claims stop (judgment); Build a comparison group from the block: 104 claims paying $25K or more three years running, with 62 permanent stops against 8.9 expected deaths, an excess stop rate of 6.6 points a year (judgment); Confirm the stops are durable (actual to expected 8.1, 7.1, 5.9, 7.0 by period; only 5 resumed) and add the excess on top of the age-rising table rate: $55.4M discounted (judgment).
  - What flips it: On the plain life table the requirement is $120M to $133M, a walk. With the block's measured stop rate it is $60.9M, a bind, and the call flips only below about 1.4 points of excess stop rate a year.
  - Why this level: A few connected estimation steps carry the answer: spotting survivor selection, designing a comparison group that can measure stops, and choosing how the excess sits on the life table. Both runs priced on population mortality and walked; one built a small comparison group, but most of its claims were the scheduled survivors themselves, and it still kept no extra runoff in its central case.
  - Reviewers, good: Real, messy administrative data (bill reversals, a 2020 gap in professional bills, unknown sex codes) has to be rolled up before any valuation. | The deciding idea, survivor selection, is a genuine actuarial judgment that no file spells out; the cedant's memo uses the plain life table. | The reference solution reports the full range and the flip point, so the strength of the call is clear.
  - Reviewers, weak: Once selection is seen the bind is wide: even the top of the range ($97.0M) is well under $110M, so the later shape and range choices refine the figure more than the call. | The comparison group keeps 21 scheduled claims, a cautious choice that a solver could reasonably make differently.
  - Prompt length: 1470 characters; deliverables: A five-minute committee memo with the bind or walk call, the lowest acceptable premium, the range and the flip condition, plus a workbook with a claim-by-claim check and expected payments by year.

### Level 5: Difficulty throughout (Best)

Many independent judgments, each of which moves the answer. Different shortcuts land on different wrong answers, so scores spread out and careful work at every step earns more. No single fact settles the task, and the conclusion holds up across a robustness sweep.

Signs: Four or more real judgment steps; Different shortcuts give different wrong answers; Strong runs got most steps and still lost on one; The answer survives a sweep of reasonable variants.

- **Does the state's job-openings rate clear 4.0?** (Survey Research & Official Statistics; Descriptive & Distribution; id bd4981a5). A contractor's employer survey reports a 3.00 rate. The fund rule pays out at 4.0 or above, measured over all employers covered by unemployment insurance.
  - Chain: Reproduce 3.00 and see that pooling the nonresponse follow-up with first-wave answers under-represents the follow-up group (judgment); Build two-phase weights for the one-in-three follow-up subsample, screening out-of-scope employers with UI records: 3.70 (judgment); Reconcile the survey frame with the rule's scope: 2,700 accounts joined after the frame was drawn (routine); Choose how to impute openings for those new accounts: young-employer ratios, not size-class averages (judgment); Bootstrap within strata, repeating every step, and run the sensitivities (judgment).
  - What flips it: No single correction clears 4.0. Weighting alone gives 3.70; new accounts at size-class averages give 3.88; both, done right, give 4.42.
  - Why this level: Three separate judgments each move the figure, and shortcuts land at 3.00, 3.62, 3.70, 3.88 or 3.90. The run did the weighting and then declined to add the new employers.
  - Reviewers, good: Two independent method corrections are both needed; either one alone stays under 4.0. | A realistic survey design (follow-up subsample, frame drawn months earlier) of the kind real labour market offices face. | The workbook traces every sampled case and every imputed account, so the figure is fully checkable.
  - Reviewers, weak: The data is constructed. | The new-account imputation (young employer ratios against size-class averages) is a modelling judgment, and the alternative lands just under the line at 3.88%.
  - Prompt length: 984 characters; deliverables: vacancy_rate_memo.docx (a page or two: whether the rate clears 4.0, the rate to certify with its range, and why it is not 3.0) and a fully traceable vacancy_rate_workbook.xlsx.

- **Renew the street patrols in full, by half, or stop?** (Criminology & Justice; Experiment & Causal; id 4e9c0a39). 58 street segments got patrols in 2025. Funding bands depend on the crime reduction against a no-patrol counterfactual, at 5% and 15% lines.
  - Chain: Segments were picked on their 2024 counts, a peak year, so use 2022 to 2023 as the baseline (judgment); Take the comparison trend only from untouched segments, leaving out the 211 that share an intersection with a patrol (judgment); Robbery rose 35% and assault fell 12% away from patrols, and patrolled segments are 71% robbery, so build the counterfactual offence by offence (judgment); Net out the 80.4 incidents displaced to adjacent segments, because the rule counts the whole city (judgment); Check base years, strata, control groups and buffer rings: all stay in the half-renewal band (routine).
  - What flips it: Each step moves the estimate. A single pooled crime trend, the shortcut both runs took, turns half renewal into stop.
  - Why this level: Four independent judgments: selection, contamination, mix and displacement. The runs handled the baseline and displacement well and lost on the offence mix.
  - Reviewers, good: Three independent judgment points: the selection-year baseline, the offence mix shift and displacement next door. | Messy inputs: two incident files with different formats and incident versions. | A clear rule with thresholds, and careful variants all land in the same band.
  - Reviewers, weak: The data is constructed, and the citywide robbery surge at the start of the patrols is a built-in hidden factor.
  - Prompt length: 1162 characters; deliverables: patrol_review.xlsx with the counts, expected figure, prevented incidents and share, plus a monthly sheet and chart, and a one-page funding_note.docx with the call and the distance to the nearest line.

- **Which territory gets the January win-back vouchers?** (Product Analytics; Opportunity Sizing & Decision Support; id 17adb5ca). Each territory would send vouchers to its 2,500 highest-risk lapsed shops. Pick the territory with the highest expected margin, using a summer trial.
  - Chain: Build each shop's 56-day trial margin by assigned arm (routine); Own-territory trial effects are confounded by customer mix, so estimate the voucher effect by group and lapse band and transport it (judgment); Age the picks 70 days to the send date, where the kiosk effect has faded to near zero (judgment); The picks are the riskiest shops in each cell, so model no-reorder on the holdout with the risk score (judgment); Shift the summer reorder hazard to November by a factor calibrated on the November list (judgment); Sum, rank and test 11 variants: the same territory leads by 16% (routine).
  - What flips it: Four different shortcuts each name a different territory. Network November rates applied to the picks name the wrong one.
  - Why this level: Five real judgments in a chain, each with its own tempting shortcut. Both runs did most of the chain and applied network rates to the high-risk picks as an untested assumption.
  - Reviewers, good: A real multi-step causal problem: pooling the trial effect, ageing the picks, moving summer behaviour to the restock season and accounting for risk selection. | Four different shortcuts each name a different territory, so every step matters. | Messy order data (overlapping exports, inconsistent codes, new pack codes) that has to be cleaned before any margin is right.
  - Reviewers, weak: The data is constructed, and the strong risk gradient is a built-in feature, though it runs across the whole network. | The decisive step is a modelling choice (a survival model plus a seasonal shift) that solvers can build in more than one way, although eleven variants agree on the pick.
  - Prompt length: 701 characters; deliverables: winback_q1_pick.xlsx listing every territory with shops sent, extra margin and rank, and a one-page winback_q1_note.docx with the pick, its margin, shops sent and its trial margin per shop.

- **Launch the short-term SBA loan, and at what sizes?** (General Statistics & Data Science; Forecasting & Predictive; id b9efebd1). Real SBA 7(a) loan-level FOIA data. Each version (all loan sizes, or over $50,000 only) launches only if its four-year charge-off share stays under the 6.50% limit.
  - Chain: Keep funded 7(a) term loans of 60 months or less approved FY2020 to FY2024: 17,922 loans, 6,994 over $50,000, with 4,522 still open short of four years (routine); Treat payoff as a competing event, not censoring: 1 minus Kaplan-Meier gives 9.45% and a hold (judgment); Split by approval year: four-year shares of 2.70% (FY2020), 2.88% (FY2021) and 8.99% (FY2022); at the same loan age and calendar half years the newer years run 1.56 times the older rate (judgment); See why one pooled curve reads low (6.25%): 61.8% of the loan time at months 36 to 48 comes from FY2020 and FY2021 (judgment); Complete FY2023 and FY2024 past their last observed day from FY2022 onward rates (12.50% and 10.12%) instead of leaving them at no risk (6.04%) (judgment); Loan-weight the five years: 7.09% at all sizes (fails), 5.54% over $50,000 (passes) (routine).
  - What flips it: Each shortcut gives a different wrong call: the pooled curve at 6.25% launches all sizes, and treating payoff as censoring (9.45%) holds the product. Per-year curves put all sizes at 7.09% and over $50,000 at 5.54%: launch over $50,000 only.
  - Why this level: Several independent modelling choices (the competing-risk estimator, the vintage split, the composition of late-age loan time, the completion of young years) each move the share across the limit, and the call holds under six other completion methods (6.65% to 7.54% at all sizes). Both runs got the competing-risk estimator right but pooled all five years, read about 6.2% and launched at all sizes, naming vintage drift only as an untested assumption.
  - Reviewers, good: Real SBA FOIA loan-level data with genuine quirks (exact repeat rows, undated charge offs, payoffs dated before disbursement). | Several independent choices each move the answer, and the shortcuts land on different wrong calls (launch all sizes, or hold). | The follow-up questions on open loans, older vintages and the 2027 plan test that the completed curves are actually used, not just read at 48 months.
  - Reviewers, weak: The margin is thin for all sizes: the robustness range bottoms out at 6.65%, only 0.15 points over the limit. | The deliverable is heavy (memo, chart, workbook and three follow-ups), so much of the work sits away from the deciding step.
  - Prompt length: 1670 characters; deliverables: A Word memo leading with the call and each version's four-year share against 6.50%, a PNG chart of cumulative charge-offs to 48 months, and an Excel workbook with the figures, open loans, FY2016 to FY2018 comparison and 2027 plan.

- **Which fourteen days should the borrowed Pit 2 crew work?** (Economics & Econometrics; Opportunity Sizing & Decision Support; id 279e74f2). Constructed scale tickets, gate camera reads and Pit 2 logs from three harvests at a co-op grain elevator. The board judges the fourteen-day block by margin kept on grain that would otherwise go to a rival elevator, at 22.6 cents a bushel.
  - Chain: Stack the two ticket exports, drop voids and tests, and match each load to its approach-camera read for line time: 42,816 loads, 96.2% matched (routine); Flag diversion from each truck's own return gap (more than 1.6 usual turnarounds, loads finished by 3:30 p.m.): 2.295 lost loads per diversion (judgment); Find that the response is a step at about 60 minutes: 15.1% of loads followed by diversion below the hour, 30.7% above, flat out to three hours (judgment); Set aside past Pit 2 hours and observed lines: Pit 2 was opened on busy days, so they only measure busy days (judgment); Replay each harvest day with Pit 1 alone and with Pit 2 ten to six, carrying unload times by the pits' mean ratio (4.57 and 7.66 minutes): mid-October lines stay at 4.4 to 4.7 hours, early November falls from 159 to 204 minutes to 28 to 49 (judgment); Score all 48 possible blocks: the best starts Thursday, November 5 (routine).
  - What flips it: Mid-October has the longest lines, but even two pits leave them past the hour, so that block keeps only 13,703 a harvest. Early November is where the second pit pulls the line under the hour: about 123,036, with every defensible reading between about 112,000 and 132,000 and starting November 3 to 7.
  - Why this level: Several independent estimates (the diversion definition, the step shape, the confounded Pit 2 history, the two-pit replay with pit-specific unload times) each move the block or its value; a smooth response or ranking by truck-hours picks mid-October, while ignoring the unload-time ratio moves the start and cuts the value to about 95,000. Both runs assumed a diversion response instead of measuring it and booked October 16 to 29, a mid-October block like the manager's plan.
  - Reviewers, good: The answer needs a measured behavioural response and a queue replay; neither is in any document. | The obvious routes (longest lines, truck-hours saved, past Pit 2 hours) all point to mid-October, and the replay shows why they are wrong. | The reference solution sweeps the diversion gap, end-of-day cutoff, break point and calendar alignment, and the early-November answer holds throughout.
  - Reviewers, weak: The data is constructed, and the response is a clean step at a round 60 minutes, which reads like a generator setting. | The exact first day is soft: starts from November 3 to 7 are all within about 6% of the best, so the decision is the early-November block rather than one date.
  - Prompt length: 972 characters; deliverables: A brief memo for the directors (Word or PDF, one chart) naming the dates and their value against the mid-October plan, plus an Excel workbook that rebuilds every figure from the scale tickets.
