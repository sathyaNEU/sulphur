Deep reasoning
Difficulty throughout the analysis, not at one point, and how to tell a deep task from a surface one

Getting the two runs under 60% is only half the bar. Reviewers also read the design. A strong task makes the solver do many connected pieces of real analytical work, each of which can go wrong for a careful analyst in a hurry, and each of which produces a result that can be checked. What is sent back however low it scores is a task where one hidden or planted thing, once caught, flips the whole answer: a planted defect or decoy, a written procedure to follow (rule application) or a shallow hidden factor.

The standard in one line
A deep task asks for several pieces of genuine analysis spread across the work, each ending in a result that can be checked, and more careful work keeps earning more. It is never won or lost on one hidden or planted thing that, once caught, flips the whole answer.

Difficulty throughout
Real analysis is hard almost everywhere. Framing the question, finding which of many files matter, joining sources that disagree, handling what is missing, testing one explanation against another, choosing and checking a model, and pulling the pieces into one account can each go wrong. A good task makes the solver do many of these, and each one ends in a result we can check.

Spread across the nine analysis types
Any of the nine analysis types listed under Vary where the hardness sits can carry this kind of task. Aim for a good spread across all of them, not a cluster in one or two.

Fourteen places analysis gets hard
A strong task usually draws on several of these. A solver who skips any one of them should lose the results that depend on it, and only those.


Framing
Turning a loose question into precise quantities, populations, units, time windows and success criteria, and noticing when the obvious metric does not answer the question.


Data discovery
Working out which of many files, tables, metrics or logs matter, how they relate, what each field really records, and what is missing.


Assembly and reconciliation
Imperfect join keys, duplicates, record linkage, schema drift across versions, unit and calendar changes, revised vintages, reconciling to published control totals, and deciding what to trust when sources disagree.


Missingness and measurement
Censoring, truncation, immature cohorts, nonresponse, sampling designs and weights, measurement error, instrument changes, top-coding, rounding and suppression.


Exploration and triage at breadth
Hundreds or thousands of series, segments or metrics: separating signal from noise, handling many comparisons at once, deciding what to look at first, and noticing the one pattern that matters among many that do not.


Investigation loops
Forming a hypothesis, testing it, ruling out alternatives, following the next lead and revising when the evidence contradicts the first story. Separating cause from symptom and triangulating across sources. This is the heart of debugging and root cause work.


Modeling
Specification, assumptions and diagnostics; heterogeneity and interactions; nonlinearity; dependence such as clustering, autocorrelation and spillover; regularization and pooling; comparing and choosing between models.


Validation
Out-of-sample tests, backtests, holdouts, cross-checks against independent data, and sanity checks against physical, accounting or business constraints.


Causal reasoning
Identification, confounding, selection, interference and whether an effect carries over to a new population. One tool among many, not the default shape of a task.


Forecasting
Seasonality, regime changes, leading indicators, honest uncertainty bands, scenarios, and evaluating the forecast itself.


Decomposition and attribution
Contribution analysis, mix versus rate, bridges that reconcile to the total, allocating interactions, and how sensitive the attribution is to the method.


Uncertainty
Quantifying it at each step, carrying it through to the answer, testing how robust the answer is, and saying how sure.


Synthesis
Combining many intermediate results into one coherent conclusion, ranking findings by importance, reconciling results that seem to conflict, and stating confidence and limits.


Self-verification
Checking that one's own numbers add up, reproducing a figure two ways, and catching one's own errors before anyone else does.

A worked illustration
This is one example among many shapes, an investigation-heavy diagnostic task, and not a template to copy. A research team ran 40 fine-tuning runs over six weeks. Evaluation scores fell in the later runs, three changes landed in that window (a new learning-rate schedule, a new data mix and a new version of the reward model), and one run is still training. The team asks what went wrong and when, which changes are responsible and by how much, and where the live run will finish. The inputs are per-step logs from every run, about 30 metrics each, plus the run configs, the change log and the cluster's incident notes. Here is the chain of results the task asks for.

1
Put every run on one axis
The logger changed partway through the six weeks: early runs log every tenth optimizer step, later ones every step, and two runs were resumed from checkpoints, so their step counters restart. The solver lines every run up on tokens seen and sets aside what cannot be aligned. Checkable result: the set of usable runs, and the point in training where each evaluation was taken.

Tip: A hurried analyst compares raw step numbers and reads runs at the wrong point in training.
2
Separate real degradation from seed noise
Several configs were run with more than one seed, which shows how much final scores vary by chance alone. The solver uses that spread to decide which runs genuinely degraded. Checkable result: the list of degraded runs.

Tip: Flagging every run below the earlier average marks noisy runs as failures and misses a real one.
3
Date the onset and separate cause from symptom
In the degraded runs the gradient norm starts spiking well before KL divergence climbs, and the KL climb comes before the evaluation drop. The solver dates each onset from the earliest reliable signal and works out which signals are causes and which are consequences. Checkable result: the onset point for each degraded run and the leading indicator.

Tip: Dating the problem from the evaluation drop puts it thousands of steps late and points at the wrong change.
4
Attribute the drop across the three changes
The changes did not land together. Some runs have only the new schedule, some only the new data mix, some both, and the reward model changed for a subset. Using the runs with partial overlap, the solver estimates how much of the drop each change explains, how much comes from two changes together, and how much the split moves under another reasonable method. Checkable result: each change's share of the drop, with the interaction shown, adding up to the total.

Tip: Comparing averages before and after each change date gives every change credit for the others.
5
Forecast the live run
The solver fits learning curves on finished runs with comparable configs, tests the method by cutting those runs off at the live run's current point and forecasting their ends, and then projects the live run with a band. Checkable result: the projected final score with its band, and the backtest error behind it.

Tip: Extending the recent trend in a straight line gives a confident number with no honest band.
6
Pull it together and check it
The answer is a timeline, the ranked causes with their contributions, the forecast and how sure the team should be of each. The solver checks that the contributions add back to the observed drop and that the timeline agrees with the change log. Checkable result: one coherent account whose numbers reconcile.

Tip: Reporting each piece on its own leaves contradictions a careful reader catches at once.
Each of the six results is checked on its own, so the score climbs with the care that went into the work.


How three passes at this task score
Result	Quick pass	Careful but hurried	Thorough
Runs on one axis	Missed	Right	Right
Degraded runs against seed noise	Missed	Partly	Right
Onset and leading indicator	Missed	Right	Right
Share of the drop per change	Missed: all blamed on the data mix	Partly: shares double count	Right
Forecast with a band	Partly: a number, no band	Partly: a band, no backtest	Right
Reconciled account	Missed	Missed	Right
Roughly	1 of 6	3 to 4 of 6	6 of 6
No single insight moves a run from the first column to the third. Each step to the right takes more time and more checking of one's own work, and each earns more.

More effort, more progress
Researchers who study AI systems call this test-time scaling: when a model is allowed to think longer about a problem, it should make measurably more progress. A task can only show that if the extra effort has somewhere to go. In a task where one hidden or planted thing flips the answer, extra thinking barely helps, because the solver either sees the one thing or does not. In a task with difficulty throughout, a quick pass earns some credit, a thorough investigation earns more, and only sustained, self-checking work earns all of it.

The effort test
Picture three solvers: one with ten minutes, one with an afternoon, and one with two days who checks every number twice. If each would score clearly higher than the last, the difficulty runs throughout. If all three would score about the same, the task is thinner than it could be. If they would either fail or ace it depending on one hidden or planted thing, it is a one-thing flip and is sent back.

Vary where the hardness sits
Difficulty throughout is not a template. If every task became the same investigation (what happened, when, why, how much, how sure), we would have swapped one pattern for another. Most deep tasks touch several of the fourteen areas; what should change from task to task is where the weight sits. The six tasks below are all deep, and their difficulty lives in very different places.


Assembly-heavy: building one dataset you can trust
A state wants this year's licensed childcare places by county from eleven licensing extracts that changed format three times, overlap at the edges and identify providers in different ways. Most of the work is linking records under uncertainty, reconciling to the published statewide total and deciding which source wins when they disagree. The analysis on top is light. Answer: a reconciled county table, the matching rule with its estimated error rate, and the gap to the published total that remains unexplained.


Measurement-heavy: survey microdata with a design
A housing agency asks how the share of renters paying more than half their income on rent changed by region over a decade, using public survey microdata with strata, clusters and replicate weights. A question about rent changed wording partway through and high incomes are top-coded. The weight sits in design-based variance, bridging the wording change and handling the top codes. Answer: a regional series with intervals and the size of the bridge adjustment.


Triage-heavy: thousands of series
Daily health statistics for every drive in a large storage fleet, dozens of counters per drive over two years. Maintenance can replace 200 drives this quarter. The weight is in separating real deterioration from noise across hundreds of thousands of series, with drive models of very different ages and many comparisons at once. Answer: a flagged set under the cap, the rule behind it, and how many flags it will raise by chance.


Validation-heavy: proving a forecast holds
A hospital network wants weekly respiratory admissions for the coming season to staff its wards. Fitting a model takes an hour. The work is proving it holds: rolling-origin backtests across past seasons, one season where the pattern broke, and bands that actually cover at the rate they claim. Answer: a forecast path with bands, a backtest scorecard against simpler methods, and the coverage the bands achieved.


Attribution-heavy: a bridge between two years
A retailer's gross margin fell three points year over year across 40 categories and 300 stores. The weight is in the bridge: separating mix from rate, price from cost, allocating the interactions, and showing how much the split moves under another reasonable allocation. Answer: a bridge that reconciles to the total, the leading contributors, and the range each one spans across methods.


Metric design: building the measure itself
An evaluation team wants one regression signal to gate releases, built from scores on 150 benchmark subtasks across past checkpoints. Subtasks differ wildly in size and noise, and correlated subtasks double count. The prompt pins the false-alarm budget on past releases that were fine. Answer: the signal's definition, its false-alarm and detection rates on history, and which past releases it would have stopped.

The worked illustration above is investigation-heavy. Synthesis-heavy tasks, allocation under constraints and estimates of a quantity that is hard to measure are just as welcome. Vary the other dimensions too: the analysis type, the answer shape, the kind of data, the scale and the form of the request.


The nine analysis types
Every one of these can carry a deep task, and we want a good spread across all nine. Causal-effect tasks are already common, so give the others a turn too.

Descriptive & Distribution Analysis. Where a total really sits, once immature periods or design weights are handled.
Comparative Analysis & Explanation. Why two groups or two periods differ, with the gap decomposed.
Anomaly Detection & Diagnostics. Which units are genuinely unusual once real variance beyond noise is modelled, with a stated rule and false-alarm rate.
Root-Cause Analysis. The chain from a symptom back to its cause, with rival explanations ruled out by the data.
Experiment & Causal Analysis. What a change did, against a comparison the design supports.
Forecasting & Predictive Modeling. A path with a band, chosen because it wins out of sample.
Opportunity Sizing & Decision Support. How large an opportunity is and where a dial should be set.
Data Extraction & Conformation (ETL / Pipeline Build). Messy sources linked and conformed to one schema, with a computed, checkable result.
Data Quality, Monitoring & Alerting. A monitoring rule tuned on history, with the alert load it will produce.

Answer shapes: a structured set of results
The answer is a set of results, not one call. A recommendation can sit on top of it.

Ranked causes with their contributions
A timeline of what went wrong and when
A forecast path with bands, plus its drivers
A bridge that reconciles two totals
A flagged set with the evidence and the false-alarm rate
A reconciled table plus findings
An allocation plus its sensitivity
A ranked list under a cap
A schedule under capacity
A monitoring rule with its expected alert count
Scenarios with the point where the call flips
A distribution and where it is cut
A composite score
A defined metric with its properties
Worked prompts for these shapes, across domains, are on Key Requirements and Example prompts.


Kinds of data
Event logs and traces; training and experiment logs; telemetry and sensor streams; panels and longitudinal records; survey microdata with designs; administrative registers; text or semi-structured records; networks and relationships; geospatial units; hierarchical and multi-level data; transaction ledgers.


Scale, readers and the request itself
A few rich files or thousands of series; one system or many units. A memo, a workbook, a script, a table, a slide or a monitoring spec, each for a reader who will use it. Prompts should read like the different real requests they are, not like one question skeleton with the nouns swapped.

A lesson can come back in a new task. A structure cannot.

A reused structure is templating
If two of your tasks follow the same chain of steps in the same order, ask the same question template or land on the same answer shape, the second is a template, even when the topic and the data differ. That includes the worked illustration on this page: copying its six steps onto a new topic is a reskin.

Tools you will use inside an investigation
The methods below have decided strong tasks. Each usually solves one part of an investigation, and a strong task often uses several. Look for them in genuine public data rather than writing them into a file.


Tools, and where a hurried analyst stops
Tool	Where a hurried analyst stops	What the thorough analyst does
A comparison that is actually clean	Compares treated units with all others, or with their own history	Shows the obvious comparison was touched by the change or already on a different trend, and builds one that was not
Heterogeneity that pooling hides	Reports one pooled effect	Estimates effects by subgroup and weights them to the population the decision serves
Competing risks	Treats payoffs, deaths or other exits as censored, which overstates the loss	Models the exits as competing events
Left truncation and immature cohorts	Reads outcomes off cohorts that have not finished, or history that starts partway through	Estimates the missing part from cohorts that have finished, and compares at matched age
Variance beyond sampling noise	Uses a binomial or Poisson test on every unit	Estimates the extra variance and calibrates the test to it
Uncertainty that matches the design	Treats every row as independent	Clusters by the real sampling unit and carries the design effect into the answer
Persistence	Runs standard tests on an autocorrelated series or overlapping windows	Corrects for the autocorrelation and the overlap, and counts the independent episodes
Measurement error	Regresses on a noisy predictor at face value	Corrects for reliability, or finds an instrument break by comparing neighbouring sites
Simulation checked out of sample	Uses a closed-form formula that assumes independence	Simulates the system and chooses the model by back-testing on held-out units
Risk adjustment with partial pooling	Ranks units of very different size and case mix on raw rates	Adjusts for case mix and shrinks small units toward the mean
Error that grows with level	Carries a constant error to a new level	Models the error as scaling with level and propagates it
Spillover read from structure	Assumes untreated neighbours are clean controls	Detects spillover from geography or networks across the whole dataset and models it
Forecasts and regime breaks	Fits the history and projects it	Dates the break in the real series, then picks the forecast that wins out of sample
Record linkage and conformance	Joins on an exact key	Links records under uncertainty, conforms messy sources to one schema, and checks the result against a known total
Decomposition and attribution	Reports the change in the total	Bridges the two totals, or drills down to the leaf that explains the change
Why difficulty throughout makes a stronger task
When the work runs through the whole analysis, every step a solver takes with care shows up in the result, and a run that slips at one step still earns what it did right elsewhere. That is what lets the task separate a quick pass from a thorough one. A task can be legitimate at every step and still lean mostly on one piece of work, such as one method choice. That is not a send-back, but it is thinner, and asking for the results around that step makes it stronger. Make each result checkable on its own: a solver who got an earlier figure wrong can still earn a later result by doing that step right on their own figure.


Stronger
A utility asks for next summer's peak with a band, how much of last summer's forecast miss came from weather, from rooftop solar and from new large loads, and which feeders will reach their limits. The inputs are hourly load for 400 feeders, readings from several weather stations, connection records and last year's forecast. The solver has to line up feeder load across metering changes, estimate the solar output that hides load behind the meter, model how demand bends upward on the hottest days, split last summer's miss across its causes, and test the forecast on past summers. Each step ends in a result that is checked.


Thinner, but not a send-back
A utility asks for next summer's peak demand to size a capacity contract. The hourly load and weather files are clean, and the main hard step is seeing that demand rises much faster with temperature on the hottest days, so a straight-line weather model understates the peak. The method is legitimate and nothing is planted, so the task can stay, but most of the work sits in one choice.

The curved temperature response appears in both. In the thinner version it is most of the task. In the stronger one it is one of several pieces of work, and a run that misses it still earns the rest.

Banned: The shallow hidden factor
The shallow hidden factor belongs to the same family as the planted defect and rule application, one hidden or planted thing that, once caught, flips the whole answer. It is a confounder, a subgroup, a contaminating event, a timing break or a measurement change that the author put into the data and no document mentions. The runs miss it and score low, but the task teaches the same lesson every time: do not trust the aggregate, find the driver that was planted.

Send it back when all three hold
It was constructed. You authored or altered the data to create it. A pattern present in genuine public data, used as is, is not constructed.
It fails the one-fact test. Told the factor in one sentence, a solver finishes with one routine step: one stratification, one extra term, one filter or one reweight.
It is easy to see once looked for. It sits only in the units that decide the answer, or a single cross-tab or plot shows it.
A hidden factor is fine when finding or correcting it is itself analysis (the data are real, detecting it takes modelling or diagnostics, rival explanations have to be separated, or the correction is a genuine modelling judgment). It is strongest as one of several pieces of work the task asks for.

Here is the same request built both ways.

Good
Deep. An auto lender asks whether loans booked after a cutoff change are worse, how much of the gap between new and old vintages comes from the cutoff, from borrower mix and from the economy, and how sure that split is. The data are a public loan-level performance file, used as is. The newer vintages look better, but they are younger and have not reached their loss peak, payoffs remove loans before they can default, and unemployment moved during the window. The solver has to project immature vintages from mature ones, treat payoffs as competing exits, separate age, vintage and macro effects, and carry the uncertainty into the split. Told any one of these facts, a solver still has the other results to produce.

Bad
Shallow. An auto lender asks whether loans booked after a cutoff change are worse. The author edits the loan file so that one dealer group, present only in the post-change vintages, defaults at three times the usual rate. Pooled, the new vintages look worse; drop that dealer group and they do not. Tell a solver "one dealer group is driving it" and the rest is one filter.

Both tasks turn on something the runs did not see at first. In the shallow version the thing was built into the deciding units, and one sentence gives it away. In the deep version the features are how real loan data behave, and handling them is several pieces of work.

Keep a short record for every hidden factor in your task before you submit.

Check your own hidden factors
For every hidden factor in your task, write down what it is, whether the data are real or constructed, whether it appears only in the units that decide the answer, how it is found (one look, a targeted query, or modelling) and how deep the fix is (routine or modelling). Constructed, found with one look and fixed with a routine step means the task will come back.

The one-fact test
Run it before you submit. If you told the solver one fact ("that file is a sample", "exclude the test rows", "use fiscal quarters", "five of the stores also had a price cut"), would the rest be routine? Then one hidden or planted thing flips the answer, and the task is a surface stump. A legitimate method choice that happens to be the hardest step does not fail this test: nothing was hidden or planted, and the choice itself is the analysis. The design decides this, not where the runs happened to stumble first. Try the test on seven designs.

Context

A hidden factor fails only when all three conditions hold: constructed, fails the one-fact test, and easy to see once looked for. A legitimate method choice that is the hardest step is not a send-back, even when it carries much of the score.

Decide whether each design would be sent back because one hidden or planted thing flips the answer, or whether it can stay.

0 / 7 decided
A store sales file where the author added a 12% sales dip to the four stores in the comparison group during the launch month. Excluding those four stores makes the program look effective.

Design 1

Keep
Send back
A public hospital discharge file used as is. The task asks for a ranking of hospitals, how much of the system's change in readmissions comes from case mix rather than care, and which hospitals are credibly worse than expected. Small hospitals swing widely from year to year, so the solver has to risk-adjust, shrink small hospitals toward the mean, decompose the system change and carry intervals into the ranking.

Design 2

Keep
Send back
A subscription file where the author recoded one region's churn flag to count paused accounts as churned, starting in the month the decision is about. A plot of churn by region shows the jump at once.

Design 3

Keep
Send back
Public river gauge records used as is. One gauge was replaced mid-series and reads systematically high afterwards. Finding it takes comparing the gauge against its upstream and downstream neighbours, and the task goes on to ask for a flood-frequency estimate at every gauge, a trend test that allows for persistence, and the return level for one design flood with its band.

Design 4

Keep
Send back
An experiment file where the author made the treatment work only for users on one app version, which exists only in the treatment arm's last two weeks. Splitting by app version reveals it.

Design 5

Keep
Send back
A public loan-level performance file used as is. The task asks whether newer vintages will lose more over their life. Every step is routine except treating payoffs as competing exits; runs that see it score near full marks and runs that do not score near zero.

Design 6

Keep
Send back
Public survey microdata with replicate weights. The task asks how a hardship rate changed by region over ten years. The solver has to bridge a question wording change, compute intervals that match the design, handle top-coded incomes, and split each region's change into population mix and changing rates. The runs lose points at three different steps.

Design 7

Keep
Send back
Check my work
You can submit now; 7 blank items will count as incorrect.

Reading the runs
Read every run's work, not just its score. Where each run lost its points tells you what kind of task you built, and in a deep task different runs lose points in different places.


How runs lose points, and which losses count
How the run went wrong	What it looks like	Counts as evidence the task is deep?
Losses spread across several results	Different runs miss different pieces: one aligns the data but forecasts without a backtest, another attributes well but never reconciles	Yes, the strongest evidence
Method shortcut	Right data, simpler method: a pooled average, a raw before-and-after, an independence formula, a single model for everyone	Yes
Unfinished chain	Early steps right, but the inference stops short: the effect is estimated and never weighted, the cohorts are projected and never used	Yes
Dismissed own evidence	The run's own output showed the signal ("excess exits: -224", "lift fell from 1.54 to 0.62") and it explained it away	Yes
Self-confirming check	A robustness check that only varies nearby choices and so confirms the original assumption	Yes
Lost most points at one legitimate step	One method choice separates the runs that pass from those that fail, and nothing was planted	Partly: genuine, but the task is thinner than one with losses spread out
Missed a planted defect	Lost because it did not spot duplicate rows, test accounts, a timezone error or a hidden file	No: surface stump
Missed a shallow hidden factor	Lost because it did not find the one confounder, subgroup or event built into the data, and one sentence would have rescued it	No: surface stump
Misread a rule or definition	Lost on how one field, clause, window or population was read	No: surface stump
Misapplied a written procedure	Lost on a step the documents spell out, such as a precedence or tie-break rule	No: rule application
Near miss or formatting slip	Substantively right, missed a tight threshold, wrong file type or layout	No
Defensible alternative	A sound method the prompt allows that gives a different answer	No: the task is not deterministic

Banned and failed stump types
These are send-backs when the task is won or lost on them. Several of them side by side are still a send-back. Planted defects and decoys, rule application and the shallow hidden factor are one family: one hidden or planted thing that, once caught, flips the whole answer.

Banned	What it looks like	Quick test
Rule application	A standard, manual or policy lays out the decisive calculation as steps; precedence or combination rules ("apply A, then B; if both apply use the lower"); "if the top option breaks the cap, take the next one"; processing instructions written for the solver; a clause that states its own procedure and cites a real regulation to justify it	If the solver followed the written procedure literally, would the answer fall out with no analytical judgment?
Data semantics	The task turns on reading one field, definition, clause, population or window a particular way	Would one sentence of clarification make the task routine?
Planted defect or decoy	One duplicate block, test rows, a shifted clock, a hidden extract, a mislabeled column or a wrong denominator decides the answer	Is the hard part finding something rather than analyzing something?
Shallow hidden factor	One confounder, subgroup, contaminating event, timing break or measurement change the author built into the data, which no document mentions	Was it constructed, does one sentence about it leave only a routine step, and does it sit only in the deciding units or show in one cross-tab? All three yes means send-back
Replay	Re-deriving a published figure, or a twist where one stated number is simply wrong	Is there an independent analytical step that changes the answer?
Unpinned ambiguity	Two defensible readings or methods give different answers	Can you point to the prompt text or the data that rules out every rival?
Messy data is still required. Real files have duplicates, inconsistent codes and gaps, and solvers should have to clean them. Cleaning can be one of several checkable results, but it must never be what decides the task on its own. See Two-layer task design and Data messiness.

Same setting, surface versus deep
Each pair keeps the setting and changes where the difficulty sits. The surface version is what gets sent back. The deep version asks for several results, each of which can be checked. The linked examples are approved tasks; where one leans on a single step, the note says what a stronger version would add.


A retail loyalty launch
Surface. The loyalty program looks like it lifted sales 6%, but the refunds file carries 40 test transactions. Drop them and the lift is 1%. Both runs miss the test rows and say "expand". One fact ("refunds include test transactions") fixes every run.

Also surface (shallow hidden factor). The author adds a regional price cut to five of the launch stores in the launch months and mentions it nowhere. Told "five stores also had a price cut", a solver drops them and is done.

Thinner. The files are clean and the only hard step is seeing that shoppers join when they are already spending more than usual. Once a solver sees it, one matched comparison finishes the task. Nothing is planted, so this is not a send-back, but most of the task rests on one step.

Deep. The program owner asks what the program did to sales, which member tiers it worked for, how much of the year's sales growth it explains next to price changes and new stores, and what a second year is likely to add. The solver has to see the pre-join run-up and build comparisons on matched spending paths, estimate effects by tier with honest intervals, bridge the year's growth across program, price and store openings, and forecast the second year from the tiers that have matured.

Why it matters. Self-selection is still in the task, but it is one of several results. A run that handles it and skips the bridge still loses points, and so does one that builds the bridge on the raw lift.


A drop in plant yield
Surface (rule application). A quality manual lists four numbered steps for deciding which production lots to quarantine, ending with "if steps 2 and 3 conflict, step 3 takes precedence." Both runs mishandle step 4 and score 35% and 40%. The answer comes from following the steps, so the task is sent back.

Deep. A packaging plant's first-pass yield fell over a quarter, and the plant manager wants to know why, starting when, and what each cause cost. The inputs are minute-level readings from 40 sensors on six lines, maintenance work orders, supplier lot records and shift rosters. The solver has to align sensor clocks that drift between lines, date the onset line by line, separate a supplier material change from a worn tool that degraded at the same time, attribute the lost yield to each cause with the overlap shown, and say which line will drop below target next if nothing changes.

Why it matters. No single fact rescues a run. The timeline, the separation of two causes that moved together, the attribution and the forecast each need their own work, and each is checked.


Choosing schools for a reading partnership
Surface (data semantics). The district's guidance defines "eligible" in a clause that can be read two ways, and the task is built so that only the narrower reading gives the right list. The runs take the wider reading. That is a reading stump, and if both readings are defensible it is also not deterministic.

Deep. Schools are picked on reliability-adjusted effects across three cohorts. The solver has to rebuild the cohorts, correct for measurement error with each cohort's own reliability, recognize that school effects genuinely move from cohort to cohort beyond sampling noise, estimate that extra variance, and carry it into every school's estimate. Several schools drop off the "credibly below" list once it is in.

Why it matters. The cohort rebuild, the reliability correction, the extra between-cohort variance and the final places are graded separately, so a run that gets the places right without the school estimates behind them still loses points.


Choosing a proposal for a representation study
Surface (replay). The task asks the solver to reproduce last year's published table of how closely members' voting tracks district opinion, and the twist is that one slope in the table was mistyped. Fixing the typo changes the pick. There is no analysis beyond re-deriving and spotting the error.

Deep. The study picks the proposal where members' voting scores move most steeply with district support, using a large public survey and public voting scores as they are. District support is only an estimate from about 140 respondents per district, so part of the spread between districts is sampling noise, and a regression on the noisy share flattens the slope. The analyst has to build weighted district shares, see from split halves that one proposal's shares barely replicate, estimate each proposal's reliable share of spread, and correct each slope. The correction reverses the ranking.

Why it matters. Nothing in the files says the shares are noisy. A task built only this way still leans on one correction for most of its result, so a stronger version would also ask for results that need different work, such as which districts drive each slope or how the pick holds under another survey year.


Crediting a place-based tax incentive
Surface (planted defect). One tract's poverty extract uses the wrong denominator, and correcting it changes the headline figure. The whole task is finding the bad denominator.

Deep. A state asks how much designating low-income tracts as investment zones cut the number of residents in poverty, using public census tract tables and the federal zone list as they are. The raw comparison shows a large fall with a clean pre-trend, but designated tracts started much poorer and poverty fell furthest wherever it was highest. The solver has to hold the starting level fixed on an earlier, separately sampled period, apportion redrawn tract boundaries, and carry the survey margins of error through to the state count.

Why it matters. The standard diagnostic passes, which is what makes the shortcut convincing. Mean reversion, the choice of baseline period, the boundary redraw and the uncertainty are separate pieces of work, each with its own result.

See the full task


Winning back bus riders
Surface (data semantics). The prompt's fiscal year starts in July, the runs use calendar quarters, and every quarter is shifted. One sentence ("use fiscal quarters") makes the task routine.

Deep. The decision bar counts riders. The solver has to identify the effect of service on ridership from state aid cuts, let the response build over the months it takes, estimate it separately for systems of different sizes, weight it by where riders are, and decompose the ridership decline into its drivers. Two runs stopped at a pooled agency average; two found that big systems respond more and still made the call on the pooled figure.

Why it matters. The identification, the timing of the response, the heterogeneity, the weighting and the decomposition each carry their own result, and the runs lost points at different ones.

See the full task


Choosing a workload forecast for a retailer
Surface (rule application). A planning memo says to pick the forecast model with the lowest error on last year's data, and if two are within 1% to take the simpler one. The runs pick the wrong model by misreading the tie rule. Following the memo literally gives the answer, so the task is rule application.

Deep. An online retailer needs the joint distribution of customer ordering days over the next two weeks, from a public transaction archive used as is. The solver has to reconcile the raw lines into eligible customer-days at each forecast origin, adapt the textbook event counts to a day with an order, fit several customer-base models, route one-time and repeat customers to different models, and score each routing on the joint probability of both weeks, because each customer's rates link the two.

Why it matters. Every run cleaned the archive. The losses spread across adapting the model to the unit, scoring on the joint target and the forecast figures themselves.

See the full task


Deciding whether to open a funnel incident
Surface (shallow hidden factor). The author lowers add-to-cart events on one date for one product category only, and the task asks whether to open an incident. One split by category shows it, and "one category broke on that date" leaves nothing else to do.

Deep. A product team asks whether to open a purchase-funnel incident, and if so for which date and funnel stage, using a public e-commerce clickstream as is. Each date has to be judged against its own weekday's history; adjusting for browsing depth confirms one candidate date and clears two others; neighbouring bad days belong to one incident; a second, genuine anomaly at a later stage survives its own checks, so incidents have to be ranked by adjusted severity; and the analyst has to say where the loss concentrates. Across twelve runs, none scored above 56%.

Why it matters. The answer is a flagged date and stage with the evidence behind it, and each piece of that evidence is a separate result. Nothing was planted.

See the full task

How to build a deep task
Work through each item.

Checklist
0 of 11 complete


Start from real data where the difficulty already exists
Public datasets, real logs, real telemetry, real registries. If you have to assemble or simulate data, such as a realistic dump of training logs, it must behave like the real thing throughout, with many genuine patterns and noise, not one effect added for the solver to find.

Decide where the weight of the task sits
Assembly, measurement, triage, investigation, modeling, validation, attribution, synthesis, allocation, a hard-to-measure quantity, or a metric or rule to design. Pick one you have not leaned on in your recent tasks.

List the checkable results the analysis produces
Aim for several pieces of genuine analysis across different areas of the fourteen. Each one should be pinned by the data or by a stated convention, with a band where reasonable methods differ.

Make sure no hidden or planted thing flips the whole answer
If catching one planted defect, one written procedure or one constructed factor would carry a run from failing to passing, rebuild that part of the task on real analysis.

Give the inputs real breadth where it is natural
Many runs, machines, units, series or files, so that deciding what to look at is real work.

Run the one-fact test on every hidden factor
If a factor was constructed, sits only in the deciding units or shows in one cross-tab, and one sentence about it leaves a routine step, rebuild that part of the task on real data.

Pin the question, the outputs and the baseline
Never the method or the traps. Run the rival methods yourself, and where reasonable methods differ, use a band.

Ask for a structured set of results
Ranked causes with contributions, a timeline, a forecast path with bands and drivers, a bridge that reconciles, a flagged set with evidence. A recommendation can sit on top.

Keep the prompt quiet about the method
Never name the comparison, the confounder or the adjustment, and never warn the solver to watch out for something.

Check it against your own recent tasks
The same chain of steps in the same order, the same question template or the same answer shape makes it a template, even on new data.

Read where each run lost its points
Losses spread across several results, from method shortcuts, unfinished chains, dismissed evidence or self-confirming checks, mean the task works. Losses from a missed planted detail, a misread clause or a misapplied rule mean it does not, even under 60%.