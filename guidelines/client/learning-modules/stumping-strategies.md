Stumping strategies
Layer 2 of every task. How difficulty runs through a whole analysis, what is banned or fails, and investigation strategies for each group of domains.

A fair stump is a real analysis that is hard almost everywhere, not at one point. The solver has to do many connected pieces of work (find which files and metrics matter, assemble them, test one explanation against another, model, validate, attribute, pull it together), and each piece ends in a result that can be checked. A quick pass gets some of those results right, a careful afternoon gets more, and only sustained, self-checking work gets all of them. The full standard, with a worked illustration, is on Deep reasoning.

This is Layer 2 of Two-layer task design. The data work is Layer 1, on Data messiness: genuine assembly and measurement work can be one of the results you check, but no single piece of mess ever decides the task.

The bar in one line
Ask for several pieces of genuine analysis, each ending in a result that can be checked, so that more careful work keeps earning more. Never let one hidden or planted thing, once caught, flip the whole answer.

How the runs should fail
The runs should lose points in several places, each for a reason like one of these. Losses spread across the results are the evidence that the task is deep.


Method shortcut
The run uses the right data but a simpler method, and the simpler method moves a result. Example: a pooled before and after comparison where the design calls for a comparison against units not yet treated.


Unfinished chain
The early steps are right, but the run does not carry the inference through. Example: it projects immature cohorts correctly, then sizes the decision on the raw, unprojected figures.


Stopped at the first story
The run takes the first explanation that fits, treats a symptom as the cause, or never tests the rival. Example: it blames a learning rate change because the loss spiked after it, without checking the data change that landed the same day.


Narrow look at broad data
The run inspects a handful of series, runs or units where the question needed all of them, and misses what matters among the many that do not.


Dismissed own evidence
The run's own output shows the signal, and it sets the signal aside. Example: it prints subgroup effects in opposite directions, then recommends on the pooled average.


Self-confirming check
The run tests robustness only by varying nearby choices, so the check can never overturn the first answer.

Not evidence of a deep task
Formatting slips, a near miss on a tight threshold, a different but defensible answer the prompt allows, or a missing file do not count. Neither does a run that misread one field or skipped one instruction. And a low score is not enough on its own: if one hidden or planted thing decided the score, the task is still a send-back.

The bar: the average of the two runs must score below 60% against the auto-generated rubric, and the runs must fall short for reasons like the ones above. Exactly 60% is too easy. You do not edit the rubric unless a criterion is clearly wrong or missing.

Banned stumps
Send-backs
The task must not be won or lost on any of these. Several of them side by side are still banned. Planted defects and decoys, rule application and shallow hidden factors are one family: one hidden or planted thing that, once caught, flips the whole answer.

Rule application. The deciding step is a procedure the materials already spell out: a standard, manual or policy that lays out the decisive calculation; combination or precedence rules ("if the top option breaks the cap, move to the next one that fits"); a decision rule that only needs the right metric plugged in; a clause justified only by citing a real regulation.
Data semantics. Reading one field, definition, clause, window or population a particular way.
Planted defects and decoys. One planted duplicate, test rows, a timezone error, a hidden file, a mislabeled column, a wrong denominator, or a memo written to carry the wrong answer.
Replay. Re-deriving a published figure, or a task whose only twist is that a stated number is wrong.
Single-fact surface stumps. A task that becomes routine once the solver is told one fact.
Shallow hidden factors. One confounder, subgroup, contaminating event, timing break or measurement change built into the data, which no document mentions, when all three hold: it was constructed rather than found in genuine public data used as is; told it in one sentence, a solver finishes with one routine step (one stratification, one extra term, one filter or one reweight); and it sits only in the units that decide the answer, or one cross-tab or plot shows it.
Unpinned ambiguity. Two defensible readings or methods that give different answers.
Two quick tests
Rule application test: if the solver followed the written procedure literally, would the answer follow with no further analytical judgment? Then it is rule application. One-fact test: if telling the solver one fact ("that file is a sample", "exclude the test rows", "five of the comparison stores also had a price cut") would make the task routine, it is a surface stump, and a hidden factor that one sentence gives away is shallow.

Strategies by domain group
Each domain group below contains individually expandable investigation strategies. Every strategy names its analysis type and answer shape, the chain of hard results the solver has to produce, where that work already lives in genuine public data, a scenario with real breadth, the several places a hurried analyst goes wrong, and how each result is pinned without naming the method. Each page ends with shallow versions of its own ideas, so you can see where a strategy turns into a one-thing flip.


Product Analytics
Each strategy below is an investigation, not a surprise. It starts from something that already happens in public product, marketing or consumer data and asks for a set of connected results, each pinned by the data and checked on its own. A quick pass earns some of them, a thorough one earns more, and only sustained, self-checking work earns all of them. The strategies differ in where the weight sits: some are mostly assembly, some mostly triage across hundreds of cells, some mostly validation or attribution. Copy the lesson, not the shape. Joining public sources, sampling them down or relabeling them for a fictional company is fine. If you must add or strengthen an effect, it has to behave like the real thing across the whole dataset, with noise and other patterns around it, and never sit only in the units that decide the answer. The eleven strategies span all nine analysis types, and none ends in a single yes or no call.

What cannot decide the task
The one design that always fails: a single hidden or planted thing that, once caught, flips the whole answer. That family is a planted defect or decoy, rule application (a document that spells out the deciding steps), and a shallow hidden factor: a subgroup, contaminating event, timing break or measurement change you built into the data, where one sentence would give it away and one routine step (a stratification, a filter, an extra term, a reweight) would fix it. Reading a field or clause a particular way, replaying a published number, or an ambiguity the data does not settle cannot decide the task either. One-fact test: if telling the solver one fact makes the rest routine, redesign. A legitimate method choice that happens to be the hardest step is fine. Strong tasks put real analytical work at more than one step, so more careful work earns more. See Deep reasoning.

Product Analytics
Product data is behavioral logs: events, sessions, subscriptions and experiments. Its hard problems come from how those logs were collected and from how many things change at once. Releases ship weekly, trackers change under a series, the user mix shifts with the season, and dozens of experiments are read one at a time. The strongest tasks here start from a metric that moved or a number someone has to commit to, and make the solver work out everything behind it.

1. A traffic decline with several causes at once
Analysis type and answer shape
Root-Cause; a dated timeline of the changes that matter, and the causes ranked by their share of the decline, adding to the observed change with a stated unexplained remainder.

Where the weight sits
Investigation-heavy. Most of the effort goes into forming candidate causes, testing each against its fingerprint and discarding the ones the evidence contradicts.

The investigation
Discovery: work out which of dozens of series (language editions, access methods, agent types, referrer classes) carry the decline and which do not.
Measurement versus behavior: find shifts that are shared across a whole platform at one moment, which point to classification or logging changes rather than readers, and size them.
Counterfactual: build what each series would have done from its own seasonality, moved holidays and trend, and from comparable series a candidate cause did not touch.
The loop: test each candidate (a deployment, a fall in arrivals from search engines, a bot reclassification, a calendar effect) against its timing, platform and referrer signature; follow the leads that survive and revise when an edition does not fit.
Attribution: split the decline across the surviving causes so the shares do not depend on the order they enter, with bands.
Self-check: rebuild the total from the parts on a second cut (by access method, then by referrer) and confirm the two agree.
Where it shows up in real data
Wikimedia pageviews by project, access method and agent type (the "automated" agent label began on 29 April 2020 and moved undeclared bot traffic out of user traffic from that date on). The Wikipedia Clickstream monthly dumps, which count arrivals at each article by source: links from other articles, search engines, other external sites and requests with no referrer. The Wikimedia Server Admin Log, a public, timestamped record of deployments and configuration changes.

Scenario
A reference-content team sees mobile-web user pageviews on its twelve largest editions fall several percent in one spring against the year before, and the board wants an explanation. The folder holds five years of daily pageviews for about 60 edition and platform series, monthly clickstream counts and the deployment log for the period. The answer is the timeline, each cause's share with a band, and the share no cause explains.

Where a hurried analyst goes wrong
Compares this spring with last spring and calls the whole gap the effect, which folds in the trend and a moved holiday. Blames the deployment nearest the visible kink, although some editions started falling earlier. Treats a reclassification of traffic as a loss of readers, or removes it from one series and not from its neighbors. Splits the decline in a fixed order, so the first cause entered takes the shared part. Reports shares that add to more than the decline.

What the solver delivers
Dated changes, each with its evidence and pinned to a week by the series' own residuals; a share of the decline per cause with a band; the unexplained remainder; and a reconciliation that the parts add to the observed decline on two independent cuts.

Keeping it deterministic
Pick editions and a window where each real cause leaves a distinct signature in timing, platform and referrer, so the shares land in tight bands under any reasonable counterfactual. State the comparison window, the metric and the date tolerance. The prompt names the decline and the decision. It never names the reclassification, the deployments to examine or the referrer split.

2. A purchase funnel that leaked in a few of many segments
Analysis type and answer shape
Comparative & Explanation; a stage-by-segment bridge between two periods whose rows add exactly to the change in orders, with the few cells that carry the real loss named, sized and dated.

Where the weight sits
Triage-heavy. The funnel cuts into hundreds of device, channel, country and category cells, most of them small, and nearly all the moves are noise.

The investigation
Before any cut, the solver rebuilds each user's path from raw events: tying sessions to users across visits and deciding what counts as reaching a stage when events repeat or arrive out of order. It then splits each stage's change into mix (who arrived) and rate (how they converted) with a method that gives the same answer in any order. The heart of the work is triage: comparing each cell's rate change against its own week-to-week variation, pulling small cells toward their parent, and accounting for how many cells were examined, so that a cell with 40 users does not top the list by chance. For the few cells that survive, the solver dates when the leak began and looks for a mechanism in the price and catalog history, dropping any that turn out to be mix. The bridge has to reconcile to the reported totals.

Where it shows up in real data
The Google Analytics 360 sample for the Google Merchandise Store in BigQuery (sessions with hit-level ecommerce actions, August 2016 to August 2017). The GA4 obfuscated ecommerce sample (November 2020 to January 2021). The REES46 multi-category store event logs on Kaggle (view, cart and purchase events with sessions, categories, brands and prices). The Retailrocket event log with timestamped item property snapshots.

Scenario
An online store's product manager sees orders fall month over month while traffic rose and must tell the commerce team where the purchase path leaked and what to fix first. The folder has three months of event exports and the merchandising calendar. The answer is the bridge, the leaking cells with orders lost and bands, the week each leak began, and the share of the change that is mix.

Where a hurried analyst goes wrong
Counts sessions instead of users, so a buyer who comes back to pay looks like an abandoner. Names the stage with the biggest store-wide drop, which is mostly a change in who arrived. Sorts every cell by change and names the top one, which is the noisiest small cell. Uses a sequential split whose answer depends on order. Stops at the stage and never dates the leak.

What the solver delivers
Stage counts for both periods under a stated stage definition; the mix and rate parts of each stage; the leaking cells with orders lost and bands, ranked; each leak's start week; and the reconciliation to reported totals.

Keeping it deterministic
State the periods, the stage definitions and the unit (users). Pick a window where the real leaks exceed their noise clearly and lead the next cell by more than its band under any reasonable pooling. The prompt asks where the path leaked and how many orders it cost; it never names segments, mix or pooling.

3. Newer cohorts that come back less
Analysis type and answer shape
Root-Cause; competing explanations ranked by the share of a retention decline each accounts for, with the evidence for and against each, shares that add to the decline, and a bounded remainder.

Where the weight sits
Synthesis-heavy. Each explanation is tested by a different partial analysis, the partial results disagree at first, and the work is reconciling them into one account that adds up.

The investigation
Four pieces of evidence have to be built separately and then made to agree. The cohort comparison itself: return rates for cohorts that have all had the full window, with the most recent ones held back or handled as censored. The mix: how arrivals shifted by topic, arrival route, accounts already held elsewhere in the network and first-question type. The first-experience model: return as a function of time to first answer, closure, votes and comments, fitted within comparable newcomers, with site and month effects. The decision about what not to adjust for: whether the first question got an answer is part of what is being sized, so it is a channel, not a control. The synthesis then allocates the decline across mix and each channel without depending on order, checks the site-level results against the network total, dates the start of the decline against changes announced on each site's meta, and bounds anything the folder cannot measure (people moving to other tools) by what is left, with a band.

Where it shows up in real data
The Stack Exchange data dump (posts, post history with closures, votes, comments and users for about 180 sites, plus each site's meta, where policy and feature changes are announced). The KKBox churn dataset from the WSDM Cup 2018 (members, transactions and daily listening logs) for subscription retention.

Scenario
A question-and-answer network's head of growth sees the 90-day return rate of first-time askers fall between two spring cohorts on most sites. Leadership has four stories: slower first answers, more first questions closed, a shift toward newcomers who never meant to stay, and people moving to other tools. The answer ranks them by share, gives the evidence for and against each, sizes the remainder and lists the sites whose decline is real rather than noise.

Where a hurried analyst goes wrong
Compares cohorts that have not finished their window. Credits slower answers with the whole decline, although slower answers partly follow from who is asking. Gives the first explanation entered the shared part. Ranks sites by raw change, so small sites fill both ends of the list. Sizes the unmeasured story as if it were measured.

What the solver delivers
Mature cohort rates; the mix shift; first-experience effects with intervals; a share for each explanation, adding to the decline; the remainder with a band; the dated start relative to announced changes; and the list of sites with a real decline.

Keeping it deterministic
State the cohorts, the return event and window, and the explanations to size. Choose sites and years where the shares separate under any order-free method and any reasonable covariate set. The prompt never names the mix variables, censoring or the meta announcements.

4. A tracker that changed under the series
Analysis type and answer shape
Data Quality, Monitoring & Alerting; dated breaks with sizes, a corrected series for each affected cell, and a monitoring rule with its expected alert count per year.

Where the weight sits
Measurement-heavy. The hard part is deciding what the instrument recorded at each point in time, and how much of each shift belongs to the instrument rather than to behavior.

The investigation
Build each series' expected path from neighbors that share its real drivers but not its instrument, fitted on a stretch that is itself checked for breaks.
Find change points on the residual, with a penalty set by how often the detector fires on clean stretches; allow for changes that roll out over weeks as ramps rather than steps.
Class each break by its breadth: shared across a platform points to the instrument, confined to a topic or region points to behavior.
Size each instrument break, correct the series and carry the size's uncertainty into the corrected history.
Turn what was learned into a rule that would catch the next break, backtested on the breaks found, with its alert count per year.
Where it shows up in real data
Wikimedia pageviews across languages, projects and access methods, including the 2015 move from the legacy page counts to the current pageview definition. The Steam Hardware & Software Survey, whose monthly shares jump when the sample's language mix swings. Citi Bike and Divvy trip files across their format changes.

Scenario
A reference-content team inherited six years of daily views for 40 language and platform series and wants a clean history for its annual report and a rule for the future. The answer is a table of dated breaks with sizes and bands, a corrected series per affected cell, and the rule with its expected alerts per year and the breaks it would have caught.

Where a hurried analyst goes wrong
Runs a change-point detector on each series alone, so an election or a viral topic looks like a tracker change. Misses a change that rolled out gradually. Calibrates on a "clean" stretch that holds a break of its own. Corrects levels without a band. Sets the alert threshold by eye.

What the solver delivers
Break dates within a stated tolerance, sizes within a band, the corrected series, and a rule whose alert rate and recall on history are both reported.

Keeping it deterministic
Choose cells where each break is large relative to the residual noise once neighbors are removed, so dates pin to a day or a week. Ask for dates within a tolerance and sizes within a band. The prompt must not say that a tracker changed, which platform changed, or when.

5. Usage jumps against a baseline that swings by itself
Analysis type and answer shape
Anomaly Detection & Diagnostics; a flagged set with its rule and false-alarm rate, and a cause class for each flag.

Where the weight sits
Rule design. The solver is building a detector whose behavior is itself the deliverable: what it flags, how often it is wrong, and what each flag means.

The investigation
Each package needs its own weekday cycle and trend, and the noise beyond Poisson has to be estimated, with small packages pooled toward similar ones. Automated downloads have to be separated from human installs by modeling the installer and CI mix rather than dropping a category. One threshold is then calibrated on a quiet historical stretch to a stated false-alarm rate and applied to the target quarter. Finally, each flag is explained: the package's own release, a release of a package that depends on it, a burst from build servers, or outside attention, checked against release times and dependency metadata.

Where it shows up in real data
PyPI download counts in the public BigQuery table, with installer and CI details, and the PyPI JSON API for release times and declared dependencies. The npm downloads API. Wikimedia per-article pageviews split by access method and agent type.

Scenario
A developer-tools company tracks daily downloads of 60 open-source packages and wants the package-days in the last quarter that were genuine adoption jumps, to credit launches and conference talks. The answer is the flagged set with a cause class per flag, the rule, and its false-alarm rate on a quiet stretch.

Where a hurried analyst goes wrong
A rolling mean with a three-sigma or Poisson threshold flags hundreds of days, most of them Mondays after quiet weekends. Raising the threshold until the list looks sensible is tuning by eye. Dropping every CI download throws away real adoption. Crediting every jump to the package's own launch misses the jumps that came from a dependent's release.

What the solver delivers
The flagged set, the rule in a form someone can rerun, the measured false-alarm rate, and a cause class for each flag backed by release or dependency evidence.

Keeping it deterministic
State the false-alarm budget (for example, at most one false flag per package per quarter) and the window. Pick a period where few package-days sit near the line and where each flag's cause is clear in the release records. The prompt must not mention weekday cycles, build servers, variance or dependencies.

6. A paying base whose history started late
Analysis type and answer shape
Forecasting & Predictive; a monthly path with a band, a dated threshold crossing, and a backtest that shows the band holds.

Where the weight sits
Validation-heavy. Several models fit the history; the work is proving which one forecasts, and that its band covers what it claims.

The investigation
Recognize from registration dates and plan history that many members joined before the log opened, and let them enter the risk set late rather than as new joiners.
Separate active cancellations from plans that simply lapse, and model how often each kind returns.
Fit candidate models whose hazard can fall with tenure, and choose among them by forecasting cohorts held out of fitting from several past origins.
Calibrate the band: check how often the held-out actuals fell inside it, and widen or rebuild it until coverage matches the stated level.
Carry today's cohort and plan mix through the chosen model and date the first month the base falls below a floor, with the chance it comes a month earlier.
Where it shows up in real data
The KKBox churn dataset from the WSDM Cup 2018 (subscription transactions with plan length, auto-renew and cancel flags, logged from 2015 for members whose registration dates go back years earlier). The Stack Exchange data dump and GitHub Archive, where account ages predate any extract window you take.

Scenario
A streaming service's finance lead needs the paying-member count for each of the next 18 months from the base active on a stated date, with an 80% band, to size next year's content budget, plus the month the base first falls below a floor. The answer is the path, the band, the crossing month, and the backtest table that shows the band's coverage.

Where a hurried analyst goes wrong
Starts every member at their first logged payment, so long-tenured survivors look like new joiners and early retention looks too good. Validates on the fitted window. Treats every exit as final. Builds the band from parameter error alone, so it covers far less than 80% in the backtest.

What the solver delivers
The monthly path with its band, the floor-crossing month and its probability of coming earlier, and a backtest over several origins with point error and band coverage for each candidate model.

Keeping it deterministic
Pin the base date, horizon, band level, floor and backtest origins. Choose data where held-out cohorts separate the candidate models clearly and the crossing month is the same under every model that passes the backtest. The prompt must not say that members joined before the log, mention delayed entry, or name the exit types.

7. Many experiments, read one at a time
Analysis type and answer shape
Experiment & Causal; a bridge from the program's claimed lift to its expected true lift, each winner's shrunken effect, and a band on the program total.

Where the weight sits
Modeling-heavy. The answer rests on a model of the whole program: how true effects are spread, how each test was stopped, and how effects change over a test's life.

The investigation
The program's own history has to carry the model. The solver estimates the spread of true effects from every test, winners and losers, by separating it from each test's known noise. From each test's snapshot history it finds which were stopped at a favorable moment and models what that does to the estimate. From the same snapshots it estimates whether early lifts fade over a test's life. Each winner is then pulled toward the program distribution by its precision and stopping, and the shrunken effects are combined into a program band that allows for tests touching the same pages. The bridge splits the gap between the claimed and the expected total into selection, early stopping and fading, each with a band, and it must close.

Where it shows up in real data
The ASOS Digital Experiments Dataset (78 real online experiments with metric snapshots across each test's life). The Upworthy Research Archive (tens of thousands of real headline tests, with every arm's impressions and clicks).

Scenario
A growth team shipped 14 winners last year. Added together, their reported lifts promise a 9% conversion gain that never showed up in the topline, and the head of experimentation must set next year's target. The answer is the bridge from 9% to the expected total, each winner's expected true lift, and one band on the combined effect.

Where a hurried analyst goes wrong
Recomputes each interval, applies a multiple-comparison correction and sums the survivors, which are still the tests that drew lucky noise. Treats a test's final snapshot as its estimate whatever its path. Ignores fading. Adds bands as if the tests were independent.

What the solver delivers
The fitted spread of true effects, the stopped-early set, each winner's expected lift with an interval, the program band at a stated level, and a bridge whose pieces add to the gap.

Keeping it deterministic
The program's history pins the distribution. Ask for the band at a stated level, the ranking of winners by expected true lift and the bridge pieces within bands. The prompt must not say the winners are inflated, mention shrinkage, or point at early stopping or fading.

Marketing & Consumer Research
Marketing and consumer data rarely samples the population the decision is about. Reviews come from people who chose to write one, campaign responders include people who would have bought anyway, and scanner prices vary mostly in weeks the retailer chose to promote. The investigations here rebuild the missing piece from structure already in the data, and then put it to work in a number someone has to act on.

8. Ratings from people who chose to rate
Analysis type and answer shape
Descriptive & Distribution; the share in each satisfaction band per department, with intervals.

Where the weight sits
Estimating a hard-to-measure quantity. Nobody observes what the silent majority thinks; the solver has to estimate it and show the estimate holds.

The investigation
Line up the two samples: the same users and items appear in both the self-selected ratings and the small randomly assigned set, and the overlap has to be found and checked.
Use the random set to estimate how the chance of rating depends on the rating a person would give, which is selection on the outcome itself, and test whether that dependence differs between heavy and light raters.
Correct the self-selected distribution with weights or a joint model, and check it against a held-out part of the random set.
Pool thin departments toward the corrected overall shape.
Carry the small random sample's uncertainty into every department's interval.
Where it shows up in real data
Yahoo! R3 music ratings (ratings users chose to give, plus ratings on randomly assigned songs). The Coat shopping dataset (self-selected and uniformly random ratings from the same users, with item features). The Amazon review datasets from the McAuley lab for the self-selected stream at scale.

Scenario
A retailer's consumer-insights lead must report, by department, what share of customers would rate their purchases at 1 to 2, 3, and 4 to 5 stars, for a supplier review. The answer is the share in each band per department, with intervals, and the departments whose ranking changes once the correction is made.

Where a hurried analyst goes wrong
Reweights reviews by recency or verified purchase and reports the shares. Uses the random sample alone, which is honest but too thin to split by department. Assumes one selection pattern for every user. Reports corrected shares without the extra width the correction adds.

What the solver delivers
The estimated selection pattern, the held-out check, shares per department to whole percentage points with bands, and the departments whose rank moves.

Keeping it deterministic
The random sample anchors the answer. Ask for shares to whole percentage points with a band. The prompt can list both inputs, but must not say the reviews are biased or describe how people choose to rate.

9. Who to contact when the send budget is fixed
Analysis type and answer shape
Opportunity Sizing & Decision Support; an allocation that sums to a fixed total, the expected incremental margin with a band, and how robust the cut line is.

Where the weight sits
Allocation under a constraint. The estimates feed an optimization, and the deliverable is a plan that survives reasonable changes to them.

The investigation
Check that the randomized history really is balanced and decide what one contact earns (added purchases times margin, less the cost of the contact). Estimate each segment's added response from treated against held-out customers, then pull those noisy estimates toward a model of effect on segment features. Fill the budget in order of added margin per contact, up to each segment's size. Test the plan on customers held out of estimation against the plan that ranks by response rate, using a cumulative gain curve. Finally, vary the pooling strength and the margin assumptions within reasonable ranges and report which segments move across the cut.

Where it shows up in real data
The X5 RetailHero uplift data (randomized SMS offers with purchase history). The Hillstrom MineThatData email test (randomized men's email, women's email or no email). The Criteo Uplift Prediction Dataset (randomized ad exposure at large scale).

Scenario
A grocery chain can send 150,000 offer texts next month across 24 segments of recency, spend band and region. The CRM lead wants the count per segment that maximizes incremental gross margin. The answer is an allocation summing to 150,000, the expected incremental margin and its band, the held-out comparison with a response-ranked plan, and the segments whose place depends on assumptions.

Where a hurried analyst goes wrong
Ranks segments by purchase rate among people who got the last text. Ranks by raw treated-minus-held-out difference, so the top of the list is the noisiest segments. Ignores the contact cost in the ranking. Reports one plan with no sense of which parts are firm.

What the solver delivers
Segment effects before and after pooling, the allocation, its expected incremental margin with a band, the held-out gain comparison and the sensitivity table.

Keeping it deterministic
State the total, segment sizes, cost per text and margin. Choose data where the cut falls between segments whose pooled effects clearly differ, and where most of the allocation is stable across the sensitivity range. The prompt must not mention the held-out group's role, pooling, or which segments respond.

10. Two eras of categories in one table
Analysis type and answer shape
Data Extraction & Conformation; a conformed monthly table with reconciled totals, the share of records allocated rather than mapped, and a band on the allocated months.

Where the weight sits
Assembly-heavy. Building one trustworthy series out of records filed under different category systems is most of the work; the analysis on top is light.

The investigation
Profile both eras and find which old categories map one to one and which split across several new ones, from the sub-product and issue fields.
Handle the second revision as well, so the table spans three category systems.
Train a classifier on records filed after a change (sub-product, issue, company, and narrative text if your copy of the data includes it) and validate it on held-out recent records.
Allocate older records with it while keeping every month's total equal to the source.
Check that the conformed series has no step at either switch beyond the trend, and carry classification error into a band on the allocated months.
Where it shows up in real data
The CFPB Consumer Complaint Database: the complaint form's product and issue options were revised in April 2017, in August 2023 and again in October 2026, and older complaints keep the options that existed when they were filed. Consumer narratives were published with consent for complaints from March 2015 on, but the CFPB removed them from the database in September 2026, so only older downloads still carry them. USDA FoodData Central branded foods and Open Food Facts, whose product categories shift across releases.

Scenario
A consumer lender's research team wants a monthly series of complaints about the product types it offers, from 2014 through 2024, by product and issue in the current categories, to show its board the long trend. The answer is the conformed table, the allocated share, the size of any remaining step at each switch, and the band.

Where a hurried analyst goes wrong
Builds a lookup by name, so old issues that split go wholly to one new issue and the series steps at the switch. Handles 2017 and forgets 2023. Validates the classifier on the same records it trained on. Lets allocation drift the monthly totals.

What the solver delivers
The crosswalk with its one-to-many entries marked, the classifier's held-out accuracy, the conformed table reconciling to source totals, the step sizes at each switch and the band on allocated months.

Keeping it deterministic
Totals reconcile exactly. Ask for category-month counts within a stated tolerance and the step sizes within a band. The prompt asks for one series in one set of categories; it must not mention the revisions, split categories or the narrative field.

11. A category sales change with price, promotion and assortment all moving
Analysis type and answer shape
Comparative & Explanation; a contribution bridge from last year's category sales to this year's, each driver with its contribution and band, reconciling exactly, plus how much the shares move under other reasonable methods.

Where the weight sits
Attribution-heavy. The demand model is a means; the hard part is splitting one change across drivers that move together and interact.

The investigation
First the comparison has to be fair: items enter and leave the assortment, stores enter and leave the data, and some store-weeks are missing, so like-for-like sales have to be separated from assortment and store-count change. Then a demand model has to tell regular-price response from deal response (shoppers stock up on deals and buy less in the weeks after), and own prices from the prices and promotions of sister brands and pack sizes. Holidays that fall in different weeks across the two years need their own term. The bridge is built from counterfactuals, with each driver set back to last year's values, and the interactions allocated so the shares do not depend on order. Last comes sensitivity: refit under other reasonable specifications and report how far each share moves.

Where it shows up in real data
Dominick's Finer Foods data from the Kilts Center at Chicago Booth (weekly store-level units, price, profit margin and deal codes for about 100 stores; regular prices were set by price zone while promoted prices were chainwide). Dunnhumby's Breakfast at the Frat (weekly store sales with feature, display and temporary price-cut flags). The M5 forecasting data (daily item sales for ten stores in three states, with weekly prices and an event calendar).

Scenario
A category manager's sales fell year over year, and the vice president wants to know how much came from the chain's own pricing, from deal frequency and depth, from competitors' moves, from items dropped and added, and from the calendar. The answer is a bridge that adds exactly to the change, each driver's contribution with a band, and a table of how the shares move across specifications.

Where a hurried analyst goes wrong
Multiplies the price change by an elasticity from a regression on all weeks, which mostly measures deal response. Counts sales of new items as growth and lost items as decline in the same bridge as price. Misses the moved holiday. Builds the bridge in one order. Reports shares with no sense of how fragile they are.

What the solver delivers
The like-for-like base, the fitted demand model with its diagnostics, the bridge, the bands and the sensitivity table.

Keeping it deterministic
State the two periods, the category, the measure (units or revenue) and the drivers to report. Choose a category and years where each driver's share is stable across reasonable specifications to within a stated band. The prompt must not mention deal timing, stockpiling, zones or switching.

Shallow versions of these ideas
Each idea above has shallow twins that look similar and get sent back, because one planted or hidden thing decides the answer. Others look narrow but are honest analysis and pass. Decide which designs you would send back before you open the reasoning.

Read each task design. Send back the ones where one planted or hidden thing, a documented procedure or a field reading flips the whole answer, and approve the ones built on honest analysis of the real data.

These are task designs, not prompts. All of them use real public data plus whatever the author added. The question is whether one fact, once told, would make the rest routine.

1. Retention forecast. The author makes one paid acquisition channel churn twice as fast in the two newest cohorts only, and the task is to project paying members for the next 18 months.
Strategy 6

Verdict and reasoning
Send back. The factor is constructed, present only in the deciding cohorts, found by one cross-tab by channel and fixed by one stratified curve. This is a shallow hidden factor.

Revised design
Use the real subscription log as published and ask for the path, the band, the floor-crossing month and a backtest of the band. Delayed entry, exit types, model choice on held-out cohorts and band coverage are each checked.

2. Paying-member forecast on the real subscription log, nothing added. The only hard step is noticing that members joined before the log opened; after that, a standard survival curve gives the path, and only the 18-month count is checked.
Strategy 6

Verdict and reasoning
Approve. Nothing is planted: members joining before the log opened is a real feature of the data, and handling it is legitimate analysis even if it is the hardest step. Asking for the monthly path with a band and a backtest as well would give careful work more to earn.

3. Download spikes. The author adds one bot day to a package's counts, with an obvious automated user-agent string, and the task is to list the genuine adoption jumps.
Strategy 5

Verdict and reasoning
Send back. One planted day decides it, and one filter on the agent string removes it. That is a planted defect.

Revised design
Use real counts that are seasonal, overdispersed and mixed with automated traffic everywhere, and ask for the flagged set from a rule calibrated to a stated false-alarm rate, with a cause class per flag.

4. Experiment portfolio on real test data. The task asks only for the program's combined true lift, and the one hard move is pulling the winners toward the program's spread of effects.
Strategy 7

Verdict and reasoning
Approve. The data are real and nothing is planted; shrinking winners toward the program's spread of effects is a legitimate method, and a hard method step is fine. Asking for the bridge, the ranking of winners and a band as well would make the task richer.

5. Funnel leak. The author breaks checkout for one browser in the last week of the month, and the task is to find where the purchase path leaked.
Strategy 2

Verdict and reasoning
Send back. The leak is constructed and sits only in the deciding cell, and one sort by change finds it. This is a shallow hidden factor.

Revised design
Use real event logs. The solver rebuilds user paths, splits mix from rate without order effects, triages hundreds of cells against their own noise, dates each real leak and reconciles the bridge.

6. Category sales bridge. The folder's pricing memo tells the analyst to drop deal weeks before fitting demand, and the task is to explain the year's sales change.
Strategy 11

Verdict and reasoning
Send back. The memo spells out a deciding step, so following it is rule application.

Revised design
Drop the memo. Deal timing, assortment change, competitors' moves and holidays in the real scanner data force the separation, and the bridge, bands and sensitivity table are each checked.

7. Download alerts. Real daily download counts for 60 packages. The solver sets an alert rule judged by its false-alarm rate on a quiet historical stretch, lists the package-days it flags last quarter and gives each flag a cause class.
Strategy 5

Verdict and reasoning
Approve. Nothing is planted. Weekday cycles, overdispersion, build-server traffic and dependency-driven jumps run through the whole real series, and the rule, its error rate and each cause are checked separately.

8. Traffic decline. Real pageviews, clickstream and deployment records for twelve editions. The solver delivers a timeline of the changes that matter, each cause's share with a band, the unexplained remainder and a reconciliation on two cuts.
Strategy 1

Verdict and reasoning
Approve. The decline has several real causes with different signatures, and finding, testing, sizing and reconciling them are separate pieces of work that each earn credit.

Key lesson
A planted defect, a documented procedure and a shallow hidden factor fail for the same reason: one thing, once caught, flips the whole answer. A legitimate method step that is the hardest part is fine. The strongest tasks ask for several results, each pinned by the data and each hard in its own way, so careful work keeps earning credit.


Quantitative Finance and Trading
Each strategy below is an investigation a practitioner in quantitative finance, credit risk or actuarial work actually runs: several connected pieces of real work, each of which can go wrong and each of which ends in a result you can check. A quick pass gets some of those results right, a thorough one gets more, and only sustained, self-checking work gets all of them. The strategies differ on purpose in how many pieces the work takes and where the weight sits: one is mostly debugging, one mostly assembly, one mostly the design of a rule, one mostly making a band honest. Keep the market, loan and claim records real. If you build a book or a pool, the positions are yours, but every pattern the solver works through has to come from the real data across the whole set. The eleven strategies span all nine analysis types. Use them as patterns, not templates.

What cannot decide the task
No single hidden or planted thing may flip the whole answer once it is caught. That family is a planted defect or decoy, a procedure the materials spell out (rule application), and the shallow hidden factor: a subgroup, event, timing break or unit change you built into the data, which one sentence would give away and one routine adjustment (a filter, a split, an extra term, a reweight) would fix, worse still when it sits only in the units that decide the answer. Reading one field or clause a particular way, replaying a published number and choosing between two defensible readings are banned too. One-fact test: if telling the solver one fact makes the rest routine, redesign. A legitimate method choice, such as testing a signal out of sample or treating payoffs as a separate exit, is fine even when it is the hardest step. Strong tasks add real work at more than one step, so more careful work earns more. See Deep reasoning for the full standard.

Quantitative Finance
Market tasks carry difficulty throughout because the work spans many positions, many dates and several systems that disagree with each other. Risk systems simplify what pricing systems do in full, volatility arrives in clusters, and reported records do not yet mean one trade. Each of those is its own piece of work.

1. Why a desk's P&L stopped explaining
Analysis type and answer shape
Root-Cause; hypotheses ranked against evidence, with each cause's share of the unexplained P&L and a dated list of the worst breaks.

Where the weight sits
Investigation-heavy. Most of the work is debugging: forming candidate causes, finding the signature each one leaves across positions and dates, and ruling causes in or out.

The investigation
Recompute both daily P&L series for every position from the files, and reconcile them to the desk's reported daily totals before trusting either; differences in how the two systems treat the same trade (a bill that matured, a forward that settled) belong in the reconciliation, not in the causes.
Find where the unexplained P&L lives: which of a few hundred positions and 250 or more days carry most of it, and whether the big days are market-wide or follow particular instruments.
Test the candidate causes against each other. Terms the sensitivity-based P&L leaves out matter only on large moves; curve shape between the risk system's tenor points hurts on twists; factors the risk system does not carry leave a drift in one product; snapshots taken at different times of day leave noise that reverses the next day.
Add each missing piece to the risk-based P&L and measure how much unexplained P&L it removes.
Repeat the additions in other orders, or average over orders, and confirm the ranking of causes does not hinge on the order.
Recompute the desk's explain metrics with the leading causes fixed and say whether it would have passed.
Where it shows up in real data
The Treasury's daily par yield curve rates (back to 1990, with a change of curve-fitting method in December 2021), the Federal Reserve's daily zero-coupon Treasury curve estimates, the New York Fed's SOFR series (published since April 2018), the Federal Reserve's H.10 noon buying rates in New York for currencies and the ECB's daily euro reference rates, which are set at a different time of day. The large rate moves of March 2020 and March 2023 are already in these series. The P&L attribution test in the Basel market risk standard, which compares the two P&L series with a rank correlation and a Kolmogorov-Smirnov distance, is a realistic model for the desk's explain metrics. If you build the book, give the risk system the tenor points and factor list a real desk's would have, and let full revaluation on real market moves produce the breaks.

Scenario
A dealer's head of market risk oversees a rates and currency desk of about 300 positions (Treasury bills, notes and bonds, and currency forwards in six currencies) whose risk-based P&L has stopped tracking the official P&L. The answer is the ranked causes with each one's share of the unexplained P&L, the 15 worst break days with the cause behind each, the positions that carry most of the gap, and the explain metrics before and after fixing the top two causes.

Where a hurried analyst goes wrong
Labels every large break "a big market day" and misses the steady drift that never shows as a spike. Regresses unexplained P&L on curve moves and reads the coefficients as causes, though several causes hit the same days. Adds the fixes in one order and reports shares that would reshuffle under another. Skips the reconciliation, so booking differences turn into model causes.

What the solver delivers
A day-by-day reconciliation of recomputed to reported P&L; the dated list of break days with a cause for each; the ranked causes with shares that add, with the residual, to the total unexplained P&L; the positions behind most of it; the explain metrics before and after. Full revaluation and the sensitivities are deterministic given the files, so every one of these is pinned by the data.

Keeping it deterministic
The prompt pins the explain metrics and their thresholds as the desk's own standard, the window and the files both systems used. Ask for shares under each order of addition or an average over orders, and choose a book where the top two causes keep their rank under any order. Grade shares in bands and the break-day causes by name. The prompt must not mention second-order terms, tenor points, snapshot times or missing factors.

2. A monitoring rule for a risk model, and what its alarms meant
Analysis type and answer shape
Data Quality, Monitoring & Alerting; a monitoring rule with its expected alert count, plus a dated set of alert episodes each tagged with its cause.

Where the weight sits
Rule design. The hard part is defining what a working model looks like and building a rule whose false-alarm rate is known under that definition; explaining the alarms on real history comes after.

The investigation
Start from the null, not from history. A correct historical-simulation VaR (value at risk) still breaks on about 1% of days, and its exception rate wanders: the model is re-estimated from a finite window, volatility clusters, a rolling count checked every day overlaps with itself, and the 40 portfolios break on the same market days. So the first piece of work is a simulated world in which the model is right, with returns from a fitted volatility model and VaR re-estimated exactly as in production. Inside it the solver finds the window and trigger that meet the false-alarm budget, counting alerts as episodes rather than days. A rule that never fires is useless, so the next piece is power: simulate a model that keeps estimating from a calm window after volatility jumps, and prefer the window that catches it soonest. Only then does real history come in. The chosen rule runs on the 40 portfolios since 2007, and each alert episode gets a likely cause, found by asking which change (volatility scaling, a longer window, a better proxy) would have prevented it.

Where it shows up in real data
Daily industry and factor portfolios in the Kenneth French Data Library, daily Treasury yields and Moody's corporate bond yields on FRED, and the Cboe VIX history. Volatility clustering and the regime shifts of 2008, 2020 and 2022 run through all of them. If you assemble model portfolios from these series, the returns stay real and only the weights are yours.

Scenario
An asset manager's model risk team runs a 99% one-day VaR on 40 model portfolios and wants one standing rule: flag a portfolio's model for review when its exceptions say it has gone stale, with no more than one false alarm per portfolio every five years. The answer is the rule, its expected false alarms per year across the 40 portfolios, the dated alert episodes it would have raised and the cause behind each.

Where a hurried analyst goes wrong
Takes the trigger from a binomial tail and counts expected alerts as if each day's check were independent, which understates false alarms several times over. Treats the 40 portfolios as 40 independent chances to alarm. Counts alert days instead of episodes. Blames every episode on the window length because 2008 and 2020 dominate, when some come from proxies that stopped tracking.

What the solver delivers
The rule (window and trigger); its expected false alarms under the simulated null; the alert episodes on real history with dates; a cause for each. The simulation pins the trigger, the history pins the episodes, and the counterfactual runs pin the causes.

Keeping it deterministic
The prompt pins the confidence level, the VaR method, the window lengths on offer and the false-alarm budget in business words. Grade the trigger within one exception, the expected alert count in a band, episode dates by overlap with the stress periods and causes by name where the counterfactual runs agree. The prompt must not mention estimation error, overlapping windows, dependence across portfolios or simulation.

3. A bridge from paper factor to real funds
Analysis type and answer shape
Comparative & Explanation; a bridge from paper return to net return for each of several funds, with a comparison of what separates them.

Where the weight sits
Attribution-heavy. Each fund's gap has to be split into pieces that each need estimating, the pieces interact, and the split has to close exactly.

The investigation
Each fund's lag behind the published factor mixes weaker exposure, the cost of trading at index reconstitutions, fees, cash and securities lending income.

Assemble each fund's holdings across filings, link securities by identifier through name and ticker changes, and price them.
Score the holdings quarter by quarter on the characteristic the factor sorts on, to see how exposure drifts between reconstitutions.
Compute a holdings-based return, which separates exposure from implementation.
Estimate the reconstitution cost from returns around each reconstitution against a buy-and-hold of the prior holdings.
Close the bridge so the items add exactly to the observed gap, deciding how to allocate the interaction between exposure and timing.
Compare across funds: which design choices (index, rebalance schedule, breadth) explain why one fund lags more than another.
Where it shows up in real data
Kenneth French's value portfolios; SEC Form N-PORT holdings, public for the last month of each fiscal quarter since 2019; Forms N-Q and N-CSR for earlier holdings; Form N-CEN for securities lending income; prospectuses on EDGAR for fees; the SEC's Financial Statement Data Sets for book values; and index providers' public reconstitution calendars.

Scenario
An adviser's investment committee holds four value ETFs that trailed the French large value portfolio by 1.5 to 3 points a year over five years. The answer is a bridge for each fund, the largest item in each, a short comparison of why the funds differ from each other, and which fund the committee should keep.

Where a hurried analyst goes wrong
Subtracts the expense ratio, runs one factor regression over five years, calls the loading shortfall "exposure" and the residual "trading cost". Loadings drift as the index reconstitutes and correlated factors make the regression unstable, so the largest item gets the wrong name. Uses year-end holdings only and misses the drift between them. Leaves out securities lending income, which offsets part of the fee for some funds. Compares the funds on their total gaps without the bridges.

What the solver delivers
Four bridges that each add to a fixed published gap, the largest item in each, the cross-fund comparison and the recommendation. The totals are published returns; the items are computed from public filings.

Keeping it deterministic
Both ends of each bridge are fixed, so the bridges must close. Pick funds where the largest item is the same under either allocation of the interaction. Grade each item in a band and the largest by name. The prompt asks why the funds lagged and what to do about it; it must not mention holdings, reconstitution, exposure drift or securities lending.

4. Slow-moving predictors, proven in real time
Analysis type and answer shape
Forecasting & Predictive; a ranked list under a cap, with a 12-month forecast and band for the funded signals.

Where the weight sits
Validation-heavy. Finding signals that fit history is easy; proving they would have worked for someone using them at the time, and in more than one episode, is most of the task.

The investigation
The solver has to

rebuild each signal as it was known at each date, since some inputs (inflation, earnings) are released with a lag,
judge the in-sample evidence under a null that carries each signal's own persistence, because near-unit-root predictors and overlapping 12-month returns make standard errors misleading,
produce recursive forecasts and compare them with the long-run average using a test built for nested models,
break each signal's gain down by decade to see whether one episode carries it, and
check that the funded set holds across a range of start dates, then forecast the next 12 months with a band that includes parameter uncertainty.
Where it shows up in real data
Amit Goyal's updated predictor dataset (dividend-price and earnings-price ratios, term and default spreads, net equity expansion and more, monthly back to the 1920s and annual back to 1871), Robert Shiller's long-run market data, and Moody's Aaa and Baa corporate bond yields on FRED, monthly back to 1919. Every one of these predictors is highly persistent; nothing needs to be planted.

Scenario
An endowment's investment committee will fund at most two of eight proposed signals for a 12-month stock and bond tilt. The answer is a forced ranking of all eight, the two (or fewer) that make the cut, the margin by which the first excluded signal misses, the decades that carry each funded signal's record, and next year's expected return on the tilt with an 80% band.

Where a hurried analyst goes wrong
Ranks by full-sample t-statistics with Newey-West errors, which still over-reject for persistent predictors. Uses series as revised today, so the forecasts see data nobody had. Picks one start date. Reports an average gain without noticing that it comes from one decade. Quotes a band from the regression residual alone.

What the solver delivers
The ranking, the funded set and the margin; a decade table for the funded signals; the forecast and band. Each is computed from public series and a stated horizon.

Keeping it deterministic
Use the updated series through the latest year and the committee's own horizon, so the answer is not a lookup in a published paper. The prompt pins the horizon, the cap and the baseline ("better than assuming the long-run average return"). Check that the funded set stays the same for any real-time start date between 1965 and 1985; grade the funded set, the top three in order, the decade split in bands and the forecast band by its width and center. The prompt must not say out of sample, persistent, overlap, real-time or bootstrap.

5. Bond trade reports conformed into one record per trade
Analysis type and answer shape
Data Extraction & Conformation; a conformed table with reconciled totals, feeding a liquidity tier for every bond.

Where the weight sits
Assembly-heavy, then estimation of a quantity the public data hide. Building one trustworthy trade table from millions of amended reports is most of the work; the hidden volume above the size caps is the rest.

The investigation
Follow cancellations, corrections and reversals back to the reports they amend and rebuild each trade's final state.
Remove the double counting: inter-dealer trades reported by both sides, and agency trades that repeat a customer leg.
Reconcile the result by segment and day to FINRA's published aggregates and measure what is still missing.
Fit the size distribution above the dissemination caps by rating, issue size and trade context.
Check that fit against the historic full-size data before relying on it.
Impute an expected size for each capped trade and confirm the segment totals now reconcile within tolerance.
Carry the imputation uncertainty into each bond's average daily volume and tier.
Where it shows up in real data
FINRA's disseminated TRACE trade reports, with large trades shown only as "5MM+" for investment grade and "1MM+" for high yield; FINRA's published daily and monthly volume aggregates, which FINRA builds from uncapped trade sizes and so give true totals to reconcile against; and FINRA's Historic TRACE Data, a separately purchased product that releases full trade sizes after a delay (at least six months for corporate and agency bonds).

Scenario
A credit fund sets position limits at a fixed share of each bond's average daily traded par. The answer is a conformed trade table, average daily volume for 600 bonds, segment totals reconciled to FINRA's aggregates within a stated tolerance, and the bonds whose limit tier changes, each with the chance the change is real.

Where a hurried analyst goes wrong
Drops cancels but keeps corrected trades twice. Counts both sides of inter-dealer trades. Counts capped trades at the cap, then closes the high yield shortfall with one scale factor, which moves every bond by the same percentage when the missing volume sits in the bonds that print large blocks. Treats imputed sizes as known, so borderline bonds switch tier with false confidence.

What the solver delivers
The conformed table, the reconciliation by segment, the per-bond volumes and the tier changes with their probabilities. The published aggregates fix the totals and the stakeholder fixes the tier cut points.

Keeping it deterministic
Grade the reconciled totals against a tolerance, the conformed trade count in a band, and the list of bonds that change tier, crediting borderline bonds when the stated probability is on the right side. The prompt asks for limits the desk can defend; it must not mention caps, amendments, double reporting or imputation.

6. Effects from a real randomized market pilot
Analysis type and answer shape
Experiment & Causal; a grid of cells, each with an effect and an interval, and the cells where the effect is credibly favorable.

Where the weight sits
Modeling-heavy. The randomization is real, so identification is the easy part; the work is in how the effect varies across stocks and in inference that respects how stocks were assigned and how daily outcomes move together.

The investigation
Four pieces of work, each feeding the next.

Use the stratified assignment and the months before the pilot for a within-stratum difference-in-differences, so differences that existed before the pilot drop out.
Build intervals that allow for dependence within each stock over time and across stocks on the same day, since market-wide days hit every stock.
Model how the effect depends on whether a stock's old spread was already near five cents, which varies inside a price band, rather than assuming one effect per cell.
Combine the spread and depth effects into the cost of the stated institutional order, which needs a model of how a large order works through the displayed depth.
Where it shows up in real data
The SEC Tick Size Pilot (October 2016 to September 2018): FINRA's published pilot security lists and group assignments, the market quality statistics the exchanges and FINRA published for every pilot and control stock, and SEC MIDAS daily metrics. Assignment was stratified by price, market capitalization and volume into three test groups of about 400 stocks each, quoted in five-cent increments, and a control group that kept the one-cent tick.

Scenario
An exchange's listings team must say which kinds of small caps would gain from a five-cent tick in a proposed program. The answer is a three-by-three grid (price band by volume tercile) of the change in cost to trade a fixed institutional order, with an interval for each cell, and the cells where the effect is credibly favorable.

Where a hurried analyst goes wrong
Compares pilot and control stock-days in each cell over the pilot period with ordinary standard errors; every cell looks significant, because more than a million stock-days are treated as independent. Leaves out the months before the pilot, so differences that existed already stay in the estimate. Reports one effect per cell when the effect inside a cell depends on how close the old spread was to five cents. Reports spread and depth separately and never says what the order would pay.

What the solver delivers
The nine cell effects with intervals, the credibly favorable cells, and the spread and depth effects behind each. The random assignment pins identification; the stated order size pins the conversion to cost.

Keeping it deterministic
The prompt fixes the cells, the order size, the pilot group and what "credibly favorable" means for the decision. Grade the sign of each cell, its value in a band and the favorable set by overlap. The prompt must not mention clustering, the pre-pilot period or which stocks the tick binds for.

Banking, Credit & Financial Risk
Credit tasks carry difficulty throughout because loans leave the data for more than one reason, the history a pool needs has not happened yet, and several balance sheet forces move at once. Loan-level and call report data carry all of these, so nothing has to be planted.

7. Pricing a seasoned loan pool
Analysis type and answer shape
Opportunity Sizing & Decision Support; a dial setting (a bid price) with the lifetime loss behind it and the assumption the price is most sensitive to.

Where the weight sits
Estimation under censoring, feeding an optimization. Most of the work is getting the timing of two competing exits right from incomplete histories; the price then falls out of a cash flow model.

The investigation
Two exits compete for every loan, and the work runs from estimating them to the price. Payoff and charge-off each need their own hazard by loan age, with every loan entering from the age it was observed so unfinished vintages count for what they show. Those hazards then have to be conditioned on the pool having already survived three and a half years, and the 2020 and 2021 relief years have to be treated as a calendar effect rather than better credit. Before any price is trusted, the model gets a backtest: price a pool of the same age drawn from an earlier year and compare its projected loss with what those loans actually did. Last comes the cash flow projection, in which payoffs shorten the pool's life, the price that meets the hurdle, and a ranking of the assumptions by how far each moves it.

Where it shows up in real data
The SBA's 7(a) and 504 FOIA loan-level files (approval date, term, amount, industry, state, and loan status, including paid in full and charged off, with paid-in-full and charge-off dates and the gross charge-off amount; check the status codes in the release you use, since recent 7(a) files split them more finely). The files span the CARES Act and Economic Aid Act debt relief of 2020 and 2021, under which SBA made several months of payments on existing 7(a) and 504 loans and genuinely held down charge-offs in those years. Freddie Mac's loan-level dataset shows the same competing exits for mortgages. Draw the pool from these files: the loans stay real and only the selection is yours.

Scenario
A community lender is offered 1,200 seasoned 7(a) loans with an average age of three and a half years and must set its bid. The answer is the highest price on the grid that still earns its stated loss-adjusted yield, the next price step shown falling short, the projected lifetime loss with a band, the backtest error and the assumption that moves the price most.

Where a hurried analyst goes wrong
Applies charge-off shares by vintage from the full file, which ignores the pool's seasoning and counts unfinished vintages as complete. Uses a default curve that treats paid-off loans as censored, which assumes they could still default and overstates loss. Reads the relief years as better credit. Skips the backtest, so two errors in opposite directions can make a wrong price look stable.

What the solver delivers
The price step, the failing next step, the loss with its band, the backtest comparison and the sensitivity ranking. The hurdle yield and price grid pin the dial; the loan histories pin the hazards.

Keeping it deterministic
The prompt fixes the hurdle yield, the servicing cost, the recovery timing convention and the price grid. Make the pool large enough that every reasonable hazard specification lands on the same price step or the one next to it, and grade on that band; grade the loss and backtest in bands. The prompt must not mention payoffs, censoring, seasoning or the relief program.

8. Explaining a margin squeeze
Analysis type and answer shape
Root-Cause; four candidate explanations ranked by their share of the decline, with the evidence for and against each and how much of the decline should reverse.

Where the weight sits
Synthesis-heavy. Four separate analyses each give a partial and sometimes conflicting answer, and the work that decides the ranking is reconciling them into one account that adds up.

The investigation
Turn year-to-date income into quarterly yields and costs by product, matched to average balances.
Price the bank's starting deposit mix at peer rates, product by product, to see whether it paid more than peers for the same product.
Split the change in deposit cost into rate, volume and mix, and size the new wholesale funding separately.
Measure the asset-side lag from the maturity and repricing detail.
Reconcile: the four pieces have to add to the observed margin change, which forces a decision on the interactions; rank the explanations and show the top one survives any reasonable interaction treatment.
Project how much of the decline reverses over the next four quarters as assets reprice at today's rates.
Where it shows up in real data
FFIEC Call Reports (quarterly average balances in Schedule RC-K, year-to-date income in Schedule RI, deposit composition in RC-E, maturity and repricing detail in RC-B and RC-C), the FDIC BankFind Suite for peer groups, and policy rates on FRED. The 2022 and 2023 rate increases produced real margin divergence across banks that ran into 2024.

Scenario
The board of a real regional bank (pick one whose margin fell further than its peers' between late 2022 and mid-2024) wants to know which explanation to act on. The answer is the four explanations ranked by share, the evidence for and against each, the one to act on, and the share of the decline that should reverse within a year.

Where a hurried analyst goes wrong
Computes one cumulative deposit beta, finds it above the peer median and blames pricing, though a bank whose customers moved from checking into CDs shows a high beta even at peer rates on every product. Reads year-to-date income as quarterly. Lets the four pieces overlap so the shares add to more than the decline. Treats the whole decline as permanent.

What the solver delivers
The ranked shares, the evidence table, the recommendation and the reversal estimate. The call report figures pin every input; the reconciliation pins the total.

Keeping it deterministic
The prompt names the two quarters and the peer group, lists the board's four explanations in the board's own words and pins the rate assumption for the projection. Choose a bank where the leading cause explains more than half of the decline under any reasonable allocation, grade the top two in order, the leading share and the reversal in bands. The prompt must not say mix, beta or repricing.

9. Where to cut the loss distribution for a securitization
Analysis type and answer shape
Descriptive & Distribution; two cuts of a lifetime loss distribution, with the median and a band on each cut.

Where the weight sits
Estimation of a hard-to-measure quantity: how strongly defaults move together. The history holds only a couple of housing cycles, so that strength has to be teased out of how much loss rates vary beyond sampling noise, and everything downstream inherits its uncertainty.

The investigation
Four questions, each answered from the vintage history. How much loss would each vintage have taken if it had held this pool's loans? That needs expected loss by vintage adjusted for loan attributes, so differences in mix do not pass for common shocks. How much of the swing between vintages is more than sampling noise? That excess is the common factor, and severity has to ride on the same house price factor, because losses per default rise in the years defaults rise. What does the pool's lifetime loss distribution look like once loans default together and payoffs remove loans along the way? That takes a simulation, cut at the two probabilities. And how far do the cuts move with the weight the 2005 to 2008 vintages carry, and do they sit sensibly against the attachment points of the agencies' own credit risk transfer deals?

Where it shows up in real data
Fannie Mae's Single-Family Loan Performance Data and Freddie Mac's Single-Family Loan-Level Dataset (vintages back to 2000 and 1999, with defaults, payoffs and net loss), the FHFA house price indexes by state, and the published attachment points of the agencies' credit risk transfer deals.

Scenario
A state housing finance agency is securitizing 9,000 of its first-lien mortgages and must size the subordination so the senior class takes a loss in no more than 1 in 200 outcomes and the mezzanine class in no more than 1 in 20. The answer is the two attachment points, the median loss and how much each attachment point moves under the reasonable range of factor estimates.

Where a hurried analyst goes wrong
Builds the distribution as if loans default independently, which makes it far too narrow. Takes the worst vintage as the 1-in-200 outcome, though one vintage is a single draw. Holds severity fixed. Ignores payoffs, so loans stay exposed longer than they will.

What the solver delivers
The two attachment points, the median and the sensitivity of each cut. The vintage history pins the factor estimate within a range; the stated probabilities pin the cuts.

Keeping it deterministic
Draw the pool tape from the agency files. The prompt pins the probabilities, the life-of-pool horizon and the tape. Ship the full vintage history so the factor is estimated across at least one complete housing cycle, and grade the attachment points in bands wide enough for reasonable factor estimates and narrow enough to exclude the independence answer, which lands far below. Spread the credit: the median depends on the vintage losses and payoffs, the senior cut mostly on the factor, the mezzanine cut on both, and the sensitivity on the range, so no one estimate carries most of the score. The prompt must not mention correlation, independence or the worst vintage.

Actuarial Science & Insurance
Insurance tasks carry difficulty throughout because the numbers that matter have not been fully reported yet. Claims develop for years, death counts fill in for weeks, and the noise in both grows with the level. The work is in estimating what has not arrived and saying how sure the estimate is.

10. A payment forecast with honest bands
Analysis type and answer shape
Forecasting & Predictive; a forecast path with a band for each year, plus a reserve at a stated percentile.

Where the weight sits
Uncertainty-heavy. The expected path is close to routine; most of the work is making the band honest, and proving it honest on outcomes the model never saw.

The investigation
Three large pieces of work and a final check. First, diagnosis: fit candidate models to incremental payments and read the residuals by development age, accident year and calendar year, looking for variance that changes with age and for calendar-year effects. Second, a predictive distribution for each candidate that carries parameter and process variance and a tail beyond the triangle, simulated and summed by calendar year so the dependence created by shared parameters carries through. Third, the backtest that chooses among them: hold back the later diagonals of the other companies in the line and score how often each candidate's 90% band caught the actual payments. The check: the chosen model's expected path should agree with a plain development projection, which catches arithmetic slips.

Where it shows up in real data
The Casualty Actuarial Society's loss reserving database: Schedule P triangles for accident years 1988 to 1997 for hundreds of US insurers across six lines, with ten years of development included. Take one company's triangle as the book and hold back its later diagonals; the other companies in the line give held-out outcomes to test methods on.

Scenario
A captive insurer's treasurer must hold enough cash to cover each of the next three calendar years of auto liability payments with 90% confidence. The answer is the expected payment path for those three years, a 90th percentile for each year, the total reserve at the 75th percentile and the backtest coverage that justifies the chosen model.

Where a hurried analyst goes wrong
Puts one coefficient of variation on every year. Bootstraps residuals pooled across ages without scaling them, so the band is too narrow for the year driven by immature accident years and too wide for the old ones. Leaves out parameter error or the tail. Sums percentiles across years instead of simulating totals. Picks the model by fit rather than by coverage.

What the solver delivers
The path, the yearly 90th percentiles, the reserve and a coverage table for the candidates. The held-out diagonals pin the model choice; the triangle pins the path.

Keeping it deterministic
The prompt fixes the confidence levels, the line and the three-year horizon. Grade the path and each year's percentile in bands and the chosen model by whether its coverage is near 90% on the held-out companies. The prompt must not mention bootstrapping, residual scaling or which ages are noisy.

11. Dating when excess claims ended
Analysis type and answer shape
Anomaly Detection & Diagnostics; a change-point dating with a cumulative total, a split by cause group and the decision it triggers.

Where the weight sits
Measurement-heavy. The recent counts are incomplete and the baseline was already moving, so most of the work is estimating what "normal" and "complete" would have been before any date can be read.

The investigation
Fit a baseline with trend and seasonality on the years before 2020, and choose its form by how well it predicts held-out pre-period years.
Estimate completeness factors for recent weeks from the history of provisional releases, much like a claims development triangle.
Date the start and end with a rule calibrated on the pre-period, so autocorrelated noise cannot trigger it.
Split the excess into COVID-coded deaths and other causes; drug overdoses and other causes also rose among working-age adults, and the insurer has to know how much of the excess will not reverse when the pandemic does.
Weight to the book's age and state mix, and carry the baseline and completeness uncertainty into a band on cumulative excess.
Where it shows up in real data
CDC NCHS weekly death counts by state and age group and weekly provisional counts by state and select causes (both frozen in September 2023, with later provisional data in CDC WONDER), successive provisional releases that show how counts fill in over time (check how many dated snapshots you can recover, for example from web archives), the Human Mortality Database's Short-Term Mortality Fluctuations series, and the Society of Actuaries' group life COVID-19 mortality survey reports.

Scenario
A group life insurer will release a pandemic reserve load once working-age mortality is back to what it would otherwise have been, and stays there. Using national working-age deaths weighted to the book's age and state mix as the proxy, the answer is the week excess mortality began, the week it ended, cumulative excess deaths with a band, the share of the excess in each cause group, and the release quarter that follows.

Where a hurried analyst goes wrong
Uses the 2015 to 2019 weekly average as the baseline; working-age deaths were already rising, so excess appears to last well into 2023. Treats the latest weeks as complete, which fakes an early end. Declares the end at the first week below the bound, though single-week crossings flip back and forth. Counts all excess as pandemic excess.

What the solver delivers
Start and end dates, cumulative excess with its band, the cause split and the release quarter. The provisional release history pins the completeness factors; the pre-period pins the baseline and the dating rule.

Keeping it deterministic
The prompt pins the age band, the book's mix, the data's as-of date and the business meaning of "back to normal". Grade the dates within a stated window and excess deaths and the cause split in bands. The prompt must not mention trend, reporting lag, provisional data, autocorrelation or causes of death.

Shallow versions of these ideas
The same topic can make a shallow task or one with difficulty throughout. The difference is whether one hidden or planted thing (a planted factor, a documented step) flips the answer once caught, or the result comes from honest work on the real data. Decide which of these designs you would send back before you open the reasoning.

Read each task design. Send back the ones where one planted thing, one documented step or one field reading flips the whole answer, and approve the ones built on honest analysis of the real data.

These are task designs, not prompts. The question is whether telling the solver one fact would make the rest routine.

1. Risk model monitoring. The author adds a burst of extra exceptions to one of the 40 portfolios after a chosen date, and the task is to name the portfolio whose model should be reviewed.
Strategy 2

Verdict and reasoning
Send back. One planted burst in the deciding unit decides it, and "look at portfolio 17 after March" makes the rest routine. That is a shallow hidden factor.

Revised design
Use real returns and a VaR re-estimated as in production for every portfolio. Ask for the rule, its false-alarm rate, the dated alert episodes on real history and a cause for each, so the null, the calibration and the explanation each earn credit.

2. Loan pool pricing. The author doubles the charge-offs of one vintage in the offered pool compared with that vintage in the full file, and the bid is right only if the solver filters that vintage out.
Strategy 7

Verdict and reasoning
Send back. The factor is constructed, sits only in the units that decide the price, and one cross-tab of pool against file by vintage reveals it.

Revised design
Draw the pool from real SBA loans as published. Ask for the price, the lifetime loss with a band, a backtest on an older pool and the assumption the price is most sensitive to.

3. Signal selection. Real predictor data, already aligned to publication dates, with the start date given. The only thing between a run and the right funded pair is testing the signals on data after each estimation date instead of over the full sample, and the funded pair is the whole answer.
Strategy 4

Verdict and reasoning
Approve. Nothing is planted, and testing signals after each estimation date is a legitimate method, not a hidden fact. Shipping the raw series and asking for the full ranking and a forecast band as well would give careful work more to earn.

4. Margin decline. A treasury memo in the folder says the bank raised its money market rate above peers on a stated date, and the task is to name deposit pricing as the cause of the margin squeeze.
Strategy 8

Verdict and reasoning
Send back. The deciding fact is written down in the materials, so the task is reading a document, not analysis.

Revised design
Leave the causes undocumented and use real call reports. The solver has to price the bank's starting mix at peer rates, split rate, volume and mix, size the asset-side lag, reconcile the pieces to the total and project how much reverses.

5. Payment bands. A real Schedule P auto liability triangle. The expected path is a plain development projection any run gets right, and the only graded item is the 90th percentile for the year driven by the immature accident years, which comes out right only if residuals are scaled by development age.
Strategy 10

Verdict and reasoning
Approve. Real data and a real technique, with nothing planted; scaling residuals by development age is legitimate actuarial work. Asking for a percentile for each year and a backtest on held-out payments as well would make the task richer.

6. Bond liquidity. The author inserts a handful of duplicate trade reports for one bond, and removing them moves that bond into a lower limit tier.
Strategy 5

Verdict and reasoning
Send back. A planted defect in the deciding unit. Told "there are duplicates in bond 214", any solver fixes it in one step.

Revised design
Use disseminated TRACE as published. The solver has to rebuild each trade from its amendments, remove double reporting, reconcile to FINRA's aggregates, estimate the volume the size caps hide and carry that uncertainty into each bond's tier.

7. P&L explain. A desk of about 300 Treasury and currency positions revalued in full on real curves for a year, next to a risk system with a realistic factor list. The solver reconciles both P&L series to the reported totals, finds the dates and positions behind the unexplained P&L, ranks the causes with shares that add up and recomputes the explain metrics with the top causes fixed.
Strategy 1

Verdict and reasoning
Approve. Nothing is planted; the breaks come from real market moves meeting a simplified risk model. Reconciliation, triage, cause testing, attribution and the re-test are separate pieces of work, and a run can get some right and miss others.

8. Excess mortality. Real weekly working-age deaths with their provisional release history. The solver fits and validates a baseline, estimates completeness for recent weeks, dates the start and end with a calibrated rule, splits the excess by cause group and puts a band on the cumulative total.
Strategy 11

Verdict and reasoning
Approve. Baseline, completeness, dating, cause split and band each produce their own checkable result, and no single hint rescues a run that skips the others.

Key lesson
A planted factor or a documented step makes the task a coin flip: the run sees the one thing or it does not, and extra effort barely helps. A legitimate method choice is fine even when it is the hardest step. The strongest tasks ask for several results, each earned by its own piece of work, so more careful work earns more.


Machine Learning Research
Each strategy below is an investigation, not a surprise: connected pieces of real analytical work that public training logs, evaluation results and statistical data force, each ending in a result you can check. A quick pass gets some pieces right; only sustained, self-checking work gets all of them. The strategies also differ in where the weight sits: one is mostly investigation, another attribution, another validation, another a search across thousands of series, so read the Where the weight sits line before borrowing a pattern. The eleven span all nine analysis types and eleven answer shapes, and none ends in a yes or no call. Use them as patterns, not as tasks to copy.

What fails a task
Some steps can never carry a task: rule application, reading one field or clause a particular way, a planted defect or decoy, replaying a published number, an unpinned choice between defensible methods, and the shallow hidden factor (a confounder, subgroup, event, timing break or measurement change you built into the data, where one sentence would give it away and one routine adjustment fixes it; it is an even clearer send-back when it sits only in the units that decide the answer or one look shows it). The planted defect, rule application and the shallow hidden factor are one family: a single hidden or planted thing that, once caught, flips the whole answer. One-fact test: if telling the solver one fact makes the rest routine, redesign. A legitimate method choice is fine even when it is the hardest step. Strong tasks have genuine work at more than one step and credit each sub-result separately, so careful work earns more; see Deep reasoning.

General Statistics & Data Science
Models in this domain are good at the mechanics. They fit, score and plot cleanly. They lose over the length of a real analysis: stitching logs that restart and disagree, telling ordinary run-to-run noise from a real change, testing one explanation against another, proving a forecast on data it did not see, and checking that the parts add up to the whole. None of that has to be planted. It already lives in public data and in the logs of real training runs, and each piece is a separate place where a careful but hurried analyst goes wrong.

If you assemble or generate the data
Prefer public logs and results where the difficulty already exists. If you build a log dump from runs you launch yourself, it has to look like a real team's records throughout: many runs, real seed noise, every scalar the trainer logs at its own cadence, crashes, resumes and logging gaps, configs and a change log written as the work happened, and several genuine problems of different kinds next to many benign oddities. Produce every problem by actually running the setting that causes it, never by editing a curve, and never add an effect only where it decides the answer. You may subsample, join, add realistic mess or recast a public source for your stakeholder.

ML training and evaluation diagnostics
Training and evaluation records are one of several data settings in this domain. The inputs are the records a training team really keeps: scalar logs from many runs (loss, gradient norms, learning rate, reward, KL, entropy, throughput, eval scores), configs, change logs and per-item eval results. The four strategies below put the weight in four different places: tracing a failure to its cause, splitting a regression across changes, proving a forecast, and measuring what a fair comparison has to remove.

1. Which runs went wrong, and what went wrong first
Analysis type and answer shape
Anomaly Detection & Diagnostics; an incident timeline across a sweep, one row per problem, with the compute each cause cost.

Where the weight sits
Investigation. The loss curve shows that something happened; the cause sits a few hundred steps earlier in a different signal, and the first explanation that fits one run usually fails on the next.

The investigation
The logs have to be made trustworthy before they are read:

stitch each run's records across crashes and resumes, where step ranges repeat after a restart from an earlier checkpoint, and put runs with different batch sizes on tokens seen rather than steps.
Model each scalar's ordinary behavior by training phase and across seeds, so the flagged events are the departures that matter among about 40 metrics per run; a spike that recovers in a few hundred steps is a different event from a divergence.
For every flagged event, find which signal moved first: gradient norm, one layer's norm, the loss scale or overflow count, the learning rate, the update size.
Test the explanations against each other. A spike tied to data order recurs at the same sample position in runs that share the order and not in reshuffled seeds; one tied to the schedule lines up with peak learning rate or with a warmup that restarted on resume; a numerical one shows overflows first, sometimes only on one node.
Check each assigned cause by whether it predicts the events in other runs that share it and their absence in runs that do not.
Total the compute lost per cause and decide which runs can still be used.
Where it shows up in real data
The logbook Meta released with OPT-175B (in the metaseq repository) records dozens of restarts, loss divergences and the responses to them, such as lowering the learning rate, restarting from an earlier checkpoint and tightening gradient clipping. BigScience published BLOOM's training chronicles on GitHub and its TensorBoard logs on the Hugging Face Hub. AI2 released OLMo's Weights & Biases training logs alongside intermediate checkpoints and the tools to reconstruct each training batch, and Pythia's checkpoints come with the exact order in which training data were seen, so the batch behind a spike can be inspected. The Open RL Benchmark, which grew out of CleanRL, is a public Weights & Biases collection of about 25,000 reinforcement learning runs across libraries and seeds; every run logs episodic return, and CleanRL's PPO runs also log value and policy losses, approximate KL, entropy, learning rate and steps per second.

Scenario
A pretraining team ran a 48-run sweep of small language models over three weeks on two clusters: six data mixtures, four peak learning rates, two seeds each. About a dozen runs misbehaved and several were restarted by hand. The folder has the TensorBoard event files, the configs, the scheduler's node assignments and the team's change log. The lead wants to know which runs went wrong, when each problem started, why, and which runs can still carry the mixture comparison.

Where a hurried analyst goes wrong
Reading steps instead of tokens, so runs with different batch sizes look out of phase. Treating the loss spike as the event and "learning rate too high" as the cause, missing an overflow or gradient event hundreds of steps earlier. Double counting the repeated steps after a resume, or missing that the schedule restarted. Blaming the data for a spike that appears in every seed at different sample positions. Calling a throughput drop a cause when it is a slow node's symptom. Flagging on one fixed threshold, which buries the real events in noise.

What the solver delivers
A table of incidents with onset, first signal to move, cause and the evidence that rules out the alternatives; the runs and compute lost per cause; the runs that remain usable; and the incidents whose cause stays uncertain, with the reason. Onsets are pinned by the logs within a step band, causes by the runs that share or do not share each factor.

Keeping it deterministic
Use public logs whose causes are documented, or runs you launched where each problem came from a real setting you know (a real learning-rate change, a real reshuffle, a real precision setting). Check that each cause is the only one the logs support, grade onsets within a band and causes by kind rather than wording. The prompt asks what went wrong and what can be trusted. It must not mention data order, resumes, loss scaling, nodes or which signal to read first.

2. Splitting an eval regression across changes that shipped together
Analysis type and answer shape
Root-Cause; an attribution table that reconciles to the drop, with a band on each change's share, the interaction left over and the part that is noise.

Where the weight sits
Attribution. The team ran only some of the combinations, two evaluation-code versions disagree with each other, and the shares still have to add up to the drop.

The investigation
Before splitting anything, the solver has to know what changed and what the evaluation itself contributes.

Diff the configs and code between the releases and list every change, including ones the change log leaves out, such as a global batch size that moved with the GPU count.
Reconcile the two evaluation-code versions: where they differ only in scoring (an answer parser, a normalization), re-score the old outputs under the new code; where they differ in generation (a prompt template, a stop sequence), read the flipped items for that change's signature. This pins the evaluation share.
Estimate the noise floor from repeated runs and per-item results, treating items from the same task or source as a cluster.
Combine the ablation cells that exist (some changes reverted one at a time, some with a single seed) into per-change effects, with a stated treatment of interactions, and check the split under more than one symmetric allocation.
Close the bridge: shares, interaction and noise sum to the observed drop, overall and for the two benchmarks where most of it sits.
Where it shows up in real data
The per-sample details datasets behind the Open LLM Leaderboard and HELM's per-instance predictions; Hugging Face's 2023 write-up showing three implementations of MMLU giving the same models different scores; successive versions of EleutherAI's lm-evaluation-harness; and the public modded-nanogpt speedrun records, where each record describes the changes it made and nearly every one links its training log. For model-side changes, train small models on a public corpus with real changes (a data filter, a schedule, a tokenizer setting) and evaluate each under two real harness versions.

Scenario
A team's small language model dropped 3.1 points on its eight-benchmark average between two releases. Five things shipped together: a new data-mixture weighting, a tokenizer normalization fix, a longer warmup, an evaluation-harness upgrade and a move from 64 to 128 GPUs. The folder has per-item outputs and scores for both releases, three seeds of the old release, one or two seeds of four variants with a single change reverted, the configs and the change log. The research lead wants to know how much of the 3.1 points each change explains, how much is noise, and what to revert.

Where a hurried analyst goes wrong
Reading each one-change revert as that change's share, so the shares do not sum to the drop. Missing that the harness upgrade moves the old release's score too. Taking the noise floor from a binomial on the item count. Trusting the change log's list and missing the batch-size change. Treating single-seed variants as exact.

What the solver delivers
The list of changes found, the evaluation share, a share and band for each model-side change, the interaction and residual, the item groups that flipped with the mechanism behind each, and the revert recommendation that follows. The re-scored outputs pin the scoring part exactly; the ablation cells and seeds pin the rest within bands.

Keeping it deterministic
Run enough cells and seeds that the larger shares are separated beyond seed noise under any symmetric allocation, and band the small ones. Credit the change list, the evaluation share, the model-side shares and the bridge separately, so no one of them carries the task. The prompt names the drop, the releases and the decision. It must not mention re-scoring, interactions, seeds, item clustering or the batch size.

3. Where a run will land, read from its early curve
Analysis type and answer shape
Forecasting & Predictive; a forecast table with a calibrated band for every live run, the runs to finish, and the chance the eventual best is among them.

Where the weight sits
Validation. Many curves fit the first quarter of a run almost perfectly; the work is proving which forecasting method would have been right on runs whose ending is known, and making the bands honest.

The investigation
The solver builds a back-test before forecasting anything.

Put live and finished runs on a common axis (tokens or compute) and record each run's schedule, because a run whose learning rate decays sooner looks better early and a run with a late cooldown drops at the end.
Cut the finished runs at the same fraction of budget as the live ones and score candidate methods on how well they predict the final value, not how well they fit; families with a floor often win, and schedule length enters as a covariate.
Fit the live runs jointly with the finished ones of the same model family, since each live run has few points past warmup.
Take the bands from the back-test's own errors at that cut fraction, and check their coverage on finished runs held out from the method choice.
Carry the forecast from validation loss to the downstream average that matters, whose relation to loss is noisier and bends.
Rank on the forecasts with their bands and estimate the chance that the best run is in the chosen set.
Where it shows up in real data
The Learning Curve Database (LCDB), with learning curves for 20 scikit-learn learners across 246 OpenML datasets in its first release; LCBench, with per-epoch curves for 2,000 configurations on each of 35 OpenML datasets; the intermediate checkpoints of Pythia and OLMo, which can be evaluated along training; and the per-run logs in MLPerf Training results, which record eval accuracy against time until each run reaches its target.

Scenario
A team has 30 hyperparameter runs at a quarter of their token budget and compute to finish eight. Sixty finished runs of the same model family from two earlier sweeps are in the folder with full logs and configs. The lead wants each live run's final validation loss and downstream average with an 80% band, the eight to finish, and how likely it is that the best of the 30 is among them.

Where a hurried analyst goes wrong
Fitting a power law to each run's own early points, which fits almost perfectly and extrapolates badly. Comparing runs at the same step when their schedules are at different stages. Taking the band from the regression's standard errors. Ranking on point forecasts when the bands of the fifth to twelfth runs overlap. Treating the downstream score as if it moved smoothly with loss.

What the solver delivers
The back-test that justifies the method, the 30 forecasts with bands, the coverage the bands achieved on held-out runs, the eight selected and the probability. The live runs' true endings are known to the task author, so every forecast and band is checked against what really happened.

Keeping it deterministic
Finish all 30 runs privately and ship only their first quarter. Grade forecasts on error and band coverage, and the selection on overlap with the true top eight within a tolerance. Check that the back-test separates the candidate methods clearly. The prompt fixes the budget, the band level and the eight slots. It must not mention back-testing, schedules, cooldowns or curve families.

4. Ranking runs fairly across seeds, test items and hardware
Analysis type and answer shape
Comparative & Explanation; a ranked list with tie groups and the margin at the cut, plus how much of the largest raw gap is recipe and how much is everything else.

Where the weight sits
Measurement. The ranking is easy once the noise is measured; the work is measuring it, with four sources of variation that each hide in a different file.

The investigation
Four variance sources are estimated separately and then combined. Seed-to-seed variation comes from the recipes run more than once, and hardware variation from seeds repeated on both clusters. Item-level variation comes from the test set itself, where questions that share a passage or source count as a cluster, which widens every interval. Then there is training that never happened: runs on the slower cluster stopped at the wall-clock limit with fewer tokens, so final checkpoints compare different amounts of training until scores are taken at matched tokens from the logged evals. With those in hand the solver

compares checkpoints paired on the same items, which tightens some gaps and not others,
shrinks each single-seed score toward its recipe's mean by the amount the seed variance justifies,
forms tie groups and checks how stable the cut is under resampling, and
decomposes the largest raw gap into recipe, seed, items and tokens.
Where it shows up in real data
HELM's per-instance predictions, the per-sample details datasets behind the Open LLM Leaderboard, OpenML runs with per-fold scores, and reading-comprehension sets where many questions share one passage (RACE, QuALITY). MultiBERTs gives 25 BERT-Base checkpoints that differ only in seed, which sets both the initialization and the order of training data. MLPerf Training reports each result from several runs with the fastest and slowest dropped, and Agarwal and colleagues released per-run Atari 100k scores (100 runs per algorithm for several algorithms) with their 2021 study of statistical precision in deep reinforcement learning evaluation. Fine-tuning a small open model with several seeds on two GPU types produces real seed and hardware variation in an afternoon.

Scenario
An applied research team has 14 fine-tuned checkpoints from four recipes, trained on two GPU clusters, and can pay for human evaluation of three. The lead wants the three most likely to be best on new documents, not the three highest scores on the internal test set. The answer is the three, the first checkpoint left out, the margin between them, and what drove the biggest gap on the internal leaderboard.

Where a hurried analyst goes wrong
Ranking by test accuracy with a binomial interval per checkpoint (4,000 questions gives roughly one point either way) and declaring the top three clear. Bootstrapping questions one at a time, which ignores shared passages. Treating a single-seed leader's score as its recipe's. Comparing final checkpoints that saw different numbers of tokens.

What the solver delivers
The variance components (seed, hardware, the item design effect), the matched and pooled score for each checkpoint with an interval, the three picks, the fourth and the margin, the tie groups, and the decomposition of the largest raw gap. Each is pinned by the repeated runs, the logged evals and the item structure.

Keeping it deterministic
Run enough repeated seeds, on both clusters, that the components are well estimated, and check that the corrected top three are separated from the fourth under any reasonable pooling. The prompt states the three slots and that the goal is performance on new documents. It must not mention seeds, hardware, tokens, passages, clustering or shrinkage.

Yardsticks, anomalies and alerts
These three ask what the measurement itself gets wrong and what normal looks like before they ask what is unusual. The weight moves from estimating a quantity no one observes, to searching millions of series, to writing the rule that will run next year.

5. Label errors in the yardstick
Analysis type and answer shape
Data Quality, Monitoring & Alerting; a bridge from measured accuracy to accuracy against corrected labels, with each reconciling item and an interval.

Where the weight sits
Estimating a quantity nobody observes directly. True accuracy has to come from a biased screen and a small random audit combined, and neither alone is good enough.

The investigation
Measure the precision of the model's suspect-label flags on the random relabel, separately for flagged and unflagged items, because the flags are a screen built from the model's own confident disagreements.
Combine the relabel's rates within each flag stratum with the exact flag counts for the whole test set (a two-phase estimator), which stays close to unbiased and is much tighter than the relabel alone.
Refine the strata by class wherever the sample supports it, since errors pile up in confusable pairs, and report how far the answer moves.
Apply the stated rule for items without a majority label and measure annotator disagreement, which limits how far any corrected label can be trusted.
Build the interval from the two-phase design.
Close the bridge from the measured figure, then rescore a competitor model on the same corrected labels to show whether the gap between the two changes.
Where it shows up in real data
CIFAR-10H (about 50 human labels for each of the 10,000 CIFAR-10 test images), the ImageNet ReaL relabeling, the crowd-validated label errors published at labelerrors.com for ten common test sets, and expert re-annotations of benchmark questions such as MMLU-Redux.

Scenario
A team reports 91.4% accuracy on a public test set, and a reviewer asks how much of the remaining error is label noise and whether it changes the comparison with the leading published model. The team has its model's flags of suspect labels for every item, the competitor's per-item predictions and a fresh multi-annotator relabel of a random 800 items. The stakeholder wants a bridge from 91.4% to accuracy against corrected labels, with each reconciling item (model right and label wrong, both wrong, no majority label), an interval, and the corrected gap to the competitor.

Where a hurried analyst goes wrong
Treating every flagged item as a label error and rescoring, which credits the model with every confident disagreement. Using only the 800 relabeled items, which is unbiased and too wide to say anything. Using one precision for every class. Dropping no-majority items silently, so the bridge does not close. Correcting labels for one model and not the other.

What the solver delivers
Flag precision by stratum, the corrected accuracy with its design-based interval, the bridge with each item, and the corrected gap with its own interval. The relabel pins the precisions, the full flag counts pin the weights, and the bridge must close to the measured figure.

Keeping it deterministic
The prompt pins what counts as the true label (the majority of the fresh annotators, with a stated rule for items with no majority) and what the number is for. Size the relabel so the corrected accuracy lands in a band clear of both shallow answers. The folder can describe how the flags were made, as a real team's notes would. The prompt must not say the flags are biased or how to combine the two sources.

6. Traffic spikes that are not people
Analysis type and answer shape
Anomaly Detection & Diagnostics; a flagged set of article-days with the rule that produced it and its measured false-alarm rate.

Where the weight sits
Triage at breadth. Millions of article-days, several weak signals for each, and a rule that has to work in years that carry no label at all.

The investigation
Rebuild what the unlabeled years looked like inside the labeled ones, by adding traffic tagged as automated back to user traffic, so the rule is trained on the view it will be applied to.
Model each article's baseline with its weekly cycle and heavy tails, and express every signal relative to that article's norm: the access mix, co-movement across language editions and linked articles, how fast a spike decays.
Make thresholds relative to the year, because mobile share rose steadily and a rule tuned on 2021 misfires on 2017.
Tune on some labeled months and measure the false-alarm and miss rates on others.
Apply the rule to 2016 to 2019 and report the flags and the share of views removed by year, with how much those figures move across reasonable baseline windows.
Where it shows up in real data
Wikimedia pageview dumps and the pageviews API. Since April 2020 Wikimedia has tagged traffic it classifies as automated separately from user traffic, which labels spikes that would have counted as human in earlier years. The access split (desktop, mobile web, app) and the Wikidata links between language editions are public too.

Scenario
A research group uses daily article pageviews as a public-attention signal and needs bot-driven spikes removed from the 2016 to 2019 history, which has no automated label. They want the flagged article-days, the rule that produced them, the expected share of flags that are genuine surges, and how much of each year's traffic the cleaning removes.

Where a hurried analyst goes wrong
Flagging days several robust deviations above a rolling median, which catches the bots and every real news surge with them. Adding a fixed desktop-share cut-off, which flags articles whose audience is simply desktop-heavy. Training on today's labeled traffic as it is, not as the old data would have shown it. Measuring the false-alarm rate on the days the rule was tuned on.

What the solver delivers
The rule, the flagged set, the out-of-sample false-alarm and miss rates, and the share of views removed per year with its sensitivity. The labeled years pin the rates; the rule's output pins the counts.

Keeping it deterministic
The prompt fixes the tolerable false-alarm rate (for example, no more than one flag in ten a genuine surge) and what the cleaned series is for. Grade the measured rate and the flag count within bands, not one exact list. The prompt must not mention the automated label, access methods or other languages.

7. A drift alarm that would ring every day
Analysis type and answer shape
Data Quality, Monitoring & Alerting; a monitoring specification (statistic, window, threshold), its expected alert count next year, and the held-out dates it fires with what each one was.

Where the weight sits
Designing the rule itself. The deliverable is a specification that has to stay quiet on normal traffic next year and still catch a real shift; most of the work is a noise model honest enough to set it.

The investigation
Measure how far the daily category counts vary beyond what a multinomial allows, which sets the right noise model.
Model the weekday pattern, the surges before major conference deadlines and the slow drift in the mix as fields grow, all of which are normal.
Decide what "the mix moved" means: one divergence across well over a hundred categories is dominated by the large ones, while per-category tests need multiplicity control; the chosen statistic has to respond to a real shift in a mid-sized category.
Calibrate the threshold by simulating or block-resampling the residual process, because residuals persist across days.
Choose on earlier years, check the alert count on a held-out year, and name what caused each held-out firing.
Where it shows up in real data
arXiv submission metadata (Cornell's snapshot on Kaggle, or the OAI-PMH feed) with dates and primary categories, including real shifts such as the economics and electrical engineering archives opening in September 2017; public conference deadline calendars; and the Stack Exchange data dump, whose posts carry creation dates and tags.

Scenario
A team routes new arXiv papers to reviewers with a classifier and wants an alert when the daily category mix moves beyond normal. They can absorb about one false alert a month. The answer is the rule, the expected number of alerts next year on normal traffic, and the dates it would have fired in a held-out year with a one-line explanation of each.

Where a hurried analyst goes wrong
A daily chi-square test against the trailing 90-day mix at a strict p-value, or a stability-index cut-off borrowed from credit monitoring; both fire on most days. Raising the threshold until the backtest looks quiet, on the same year it was tuned on. Building a statistic that only the largest categories can move. Treating every deadline week as an incident.

What the solver delivers
The specification, the overdispersion estimate, the expected alert count with a band, the held-out firings and their explanations. The held-out year pins the count; the dates are checked against the data.

Keeping it deterministic
The prompt fixes the alert budget and the held-out year. A sound calibration puts the expected count in a narrow band, while the shallow rules miss by an order of magnitude. The prompt must not mention overdispersion, deadlines, weekdays or autocorrelation.

Estimating from field data and building one table
Field data arrive incomplete in ways a clean benchmark never is: units observed for part of their lives, a shock with no spared group, records censored at the top, identifiers that change midway. Here the weight sits in modeling, in building a counterfactual, in recovering what a file hides and in assembly.

8. Spares for failures you never saw start
Analysis type and answer shape
Opportunity Sizing & Decision Support; an allocation to a fixed total, with the failure forecast it rests on and how far each share could move.

Where the weight sits
Modeling, then allocation under constraints. The hazard model has to handle truncation, sparse models and two kinds of exit before the split means anything.

The investigation
Build each drive's history from daily snapshots, recover its age at entry from power-on hours, and separate failures from drives that simply leave the data through migration.
Construct left-truncated risk sets, so a drive first seen at age three counts only from age three.
Estimate hazard by age band for each model, pooling small models toward their manufacturer and capacity family.
Back-test the predicted failures by model on a held-out year.
Project next year's failures for the center's own age profile, treating the planned retirements as a competing exit, because a retired drive cannot fail.
Allocate the 400 spares and show which shares move under the forecast's band.
Where it shows up in real data
Backblaze Drive Stats: daily SMART snapshots for every drive in the fleet since 2013. Power-on hours at first appearance give each drive's age when it entered the data, drives disappear through migration as well as failure, and many models have only a few hundred units.

Scenario
A university research computing center runs nine drive models of mixed ages and must split a fixed order of 400 spare drives across them for next year, in proportion to expected failures. Two of its oldest models are scheduled for retirement mid-year. The answer is an allocation that sums to 400, the expected failures behind it, and the models whose share is least certain.

Where a hurried analyst goes wrong
Using each model's lifetime annualized failure rate, which ignores that hazard depends on age and that each model's history covers a different age range. Counting drives from their first appearance as if they were new. Treating every disappearance as a failure. Ignoring the retirements, or treating them as censoring in the projection as well as the fit.

What the solver delivers
Hazard by age for each model with the pooling stated, the back-test result, the projected failures with a band, the allocation and the sensitive shares. The held-out year checks the hazard; the prompt's order size and rounding rule fix the allocation.

Keeping it deterministic
The prompt fixes the order size, the retirement dates and the rounding rule. Pick models where the age-aware allocation differs from the naive one by tens of drives, so any reasonable pooling gives the same allocation within a stated tolerance. The prompt must not mention age at entry, power-on hours, truncation or migrations.

9. The effect of a shock that hit every unit
Analysis type and answer shape
Experiment & Causal; a monthly effect path with a band and a cumulative total.

Where the weight sits
Building the counterfactual. No unit was spared, so the comparison has to be assembled from units that were touched least, and then proved before it is trusted.

The investigation
Assemble the framework's monthly question series from its tag set, following tag synonyms and renames so the series is continuous.
Build a pool of comparison series the assistants touched least, such as non-programming sites and communities whose users had less access to them, and show from the pre-period that they track the framework's series.
Fit a weighted combination of those series (a synthetic control) over a long pre-period that includes the seasonal cycle, and check it on held-out pre-period months.
Get the band from placebo runs, giving each comparison series and several false shock dates the same treatment, because monthly residuals are autocorrelated.
Carry the path to a cumulative total with a band from the same placebo distribution, and report how much it moves across reasonable comparison pools.
Where it shows up in real data
The Stack Exchange data dump: every question on Stack Overflow, on its sister sites in other languages and on the network's other sites, many of them not about programming, with creation dates and tags. Since 2024 the official dump is downloaded from Stack Exchange's own site under its terms of use. The dump does not include tag synonyms; the Stack Exchange Data Explorer lists them. Question volume on Stack Overflow fell after general-purpose AI chat assistants became widely available in late 2022, against a longer-run drift you can see in the years before, and sites differ in how much of their users' questions an assistant could answer.

Scenario
A developer-tools company answers questions about its open-source framework on Stack Overflow and is deciding whether to move two technical writers from Q&A support to documentation. The head of developer relations wants the number of framework questions that went unasked because of the assistants: a monthly path for the 18 months from December 2022 with a 90% band, and the cumulative total.

Where a hurried analyst goes wrong
Extrapolating a linear trend with month effects that was already bending. Running a difference-in-differences against a slower-moving programming tag that the same assistants also hit. Building the series from one tag and missing questions filed under its synonyms. Taking intervals from a regression on monthly points as if they were independent.

What the solver delivers
The assembled series, the comparison pool with its pre-period fit and held-out check, the monthly path with its placebo band, the cumulative total and its sensitivity to the pool. The pre-period pins the weights; the placebo distribution pins the band.

Keeping it deterministic
The prompt fixes the tag set, the start month, the horizon and the band level. Choose a framework where the estimate is stable across reasonable comparison pools, and where the trend and difference-in-differences answers fall outside the band. The prompt must not mention comparison sites, weighting, placebo runs or the earlier drift.

10. Percentile cuts from a weighted, top-coded survey
Analysis type and answer shape
Descriptive & Distribution; a table of cut points with margins of error and the list of boundaries that can be published.

Where the weight sits
Recovering what the file hides. The top of the distribution is censored by design, the geography is not the one asked about, and the margins have to come from the survey's own variance method.

The investigation
Assign households to metro areas: the microdata identify public use microdata areas, not metros, so the solver builds the assignment and checks how much the cut points move for areas that straddle a metro boundary.
Use the household weights throughout, restricted to renter households.
Notice the repeated identical income-component values near the top in some metros and trace them to top-coding.
Where a percentile depends on that range, model each affected component above its threshold with a Pareto tail and redraw the amounts before summing household income; the published replacement mean fixes the tail's shape (above a threshold T the mean is aT/(a-1)), so the tail is not a free choice.
Compute margins with the replicate weights and the survey's own variance formula, then apply the publish rule.
Where it shows up in real data
The American Community Survey public use microdata (PUMS) from the Census Bureau: household weights, 80 replicate weights for variance, and income components that are top-coded, with values at or above each state's threshold replaced by the state mean of those values. The Census Bureau publishes the thresholds and means for each state and year. The Current Population Survey's annual supplement also carries weights, replicate weights and protected top incomes.

Scenario
A consumer lender's data science team is setting renter-household income bands in eight metro areas: the 20th, 50th, 80th and 95th percentiles of household income, each with a 90% margin of error. A boundary is published only if its margin is under 5% of its value. The answer is the table of cut points with margins and the list of boundaries that can be published.

Where a hurried analyst goes wrong
Taking weighted percentiles of household income as recorded, which puts the 95th in high-income metros where many households carry the same replaced state mean. Bootstrapping households, which ignores the design. Assigning straddling areas wholesale without checking what that does. Applying the publish rule to the wrong margins.

What the solver delivers
The metro assignment with its sensitivity, the 32 cut points with design-based margins, the cut points that the tail model moved and by how much, and the publish list. The published thresholds and means pin the tail; the replicate weights pin the margins.

Keeping it deterministic
The prompt fixes the population, the percentiles, the margin level and the publish rule. Choose metros where the 95th percentile depends on the top-coded range in some and not in others; because the replacement mean pins the tail, the cut points fall in tight bands. The prompt must not mention weights, replicate weights, top-coding or the geography.

11. One station series across a schema change
Analysis type and answer shape
Data Extraction & Conformation; a conformed table with monthly totals reconciled to the operator's reports.

Where the weight sits
Assembly. Building one trustworthy table across a change that reissued every identifier is most of the work; the counts are quick once the links are right.

The investigation
Build candidate links between old and new stations from name similarity, distance and each station's ride pattern (its destination mix and hourly profile in the months either side of the change).
Score the links and set the acceptance threshold by measuring precision on stations whose identity is certain, so the error rate of the accepted links is known.
Resolve stations that were split, merged or moved across a street, which make links one-to-many.
Carry the uncertain links into the counts under a stated rule and report the share of rides on them.
Reconcile monthly totals with the operator's figures, explain the gap by documented exclusions, and check that the gap is stable across the change.
Test each conformed series for a break at the change date.
Where it shows up in real data
Citi Bike's public trip files, which moved to a new schema in February 2021 with station identifiers that no longer match the old numeric ones, alongside the monthly operating reports that give system-wide trip totals. Chicago's Divvy and Washington's Capital Bikeshare changed their trip-file schemas a year earlier, in 2020, and NYC TLC trip records replaced coordinates with zone IDs in mid-2016.

Scenario
A transport research group wants monthly ride counts per station from 2018 to 2023 to train a demand model, with each station's series continuous across the change. The deliverable is the conformed table, a month-by-month reconciliation against the operator's reported totals with every gap explained, the number of stations with a continuous series, and the share of rides that sit on uncertain links.

Where a hurried analyst goes wrong
Joining on exact name and dropping the rest, which breaks hundreds of series. Adding nearest-coordinate matching within a fixed radius, which merges stations that were split or moved and splits ones that were only renamed. Accepting links without measuring their precision. Reconciling only the annual total, which hides a monthly gap that opens at the change.

What the solver delivers
The link table with its measured precision, the conformed counts, the reconciliation with each gap explained, the count of continuous stations, the uncertain share and the stations that still break at the change. Each is checked within a band.

Keeping it deterministic
The checkable results are the reconciled monthly totals, the count of continuous stations and the uncertain share, each in a band. The prompt fixes the period and what the table is for. It must not say when or how the identifiers changed, or suggest matching on ride patterns.

Shallow versions of these ideas
Each idea above has shallow twins that look similar and get sent back because one planted or hidden thing flips the answer. Others look narrow but are honest analysis and pass. Decide which designs you would send back before you open the reasoning.

Read each task design. Send back the ones decided by a planted defect, a shallow hidden factor or a documented procedure, and approve the ones built on honest analysis of the real data.

These are task designs, not prompts. Ask what decides the result, and whether telling the solver one fact would make the rest routine.

1. Training sweep. The author copies one run's loss curve, adds a spike at step 12,000 by hand, and asks which run diverged and when.
Strategy 1

Verdict and reasoning
Send back. One edited curve decides it and one plot shows it. That is a planted defect, and no other signal in the run moves with the spike, because nothing caused it.

Revised design
Ship a real sweep, public or launched yourself, with several genuine problems of different kinds and plenty of benign noise. The solver stitches resumed logs, finds the first signal to move in each incident, tells data order from schedule from numerics, totals the lost compute and says which runs can still be trusted.

2. Eval regression. Two releases differ only by an evaluation-code upgrade that changed the answer parser. Re-score the old outputs with the new parser and the whole drop is explained.
Strategy 2

Verdict and reasoning
Approve. Nothing is planted, and re-scoring old outputs under the new parser is a legitimate diagnostic, not a hidden fact. Shipping several real changes with real effects would give careful work more to earn.

3. Run forecasting. Thirty live runs, and the only difficulty is that a power law overshoots while a curve with a floor is right. Pick the family and every forecast follows.
Strategy 3

Verdict and reasoning
Approve. The runs are real and nothing is planted; choosing a curve family that fits the data is legitimate forecasting work. Asking for bands from a back-test and a selection with its probability as well would make the task richer.

4. Traffic spikes. The author plants twenty bot days in the five articles that decide the answer, each visible on one plot, and the task is to clean the series.
Strategy 6

Verdict and reasoning
Send back. The factor is constructed, sits only in the deciding units and shows up on a single look. This is a shallow hidden factor.

Revised design
Use real pageviews, where automated traffic runs through every article. The rule is trained on labeled years rebuilt to look like the old data, its false-alarm rate is measured on months it did not tune on, and the share of traffic removed is reported by year.

5. Station series. A README lists the old-to-new station mapping, and the task is to build the monthly table across the change.
Strategy 11

Verdict and reasoning
Send back. The deciding step is a documented procedure: follow the mapping and the table is done. A task that instead turns on one renamed column is a field reading, also a send-back.

Revised design
Infer the links from names, places and ride patterns, set the acceptance threshold by measured precision on certain stations, resolve splits and moves, and reconcile the totals against the operator's reports.

6. Fine-tuning sweep. Thirty-six real reinforcement learning runs across three reward-model versions, three KL settings and four seeds, with every scalar the trainer logged. The solver dates when each run's held-out score peaked while its reward kept rising, estimates what each setting contributes, and proposes a checkpoint rule tested on runs it did not see.
Strategies 1 and 4

Verdict and reasoning
Approve. Nothing is planted: the over-optimization, the seed noise and the logging gaps come from real runs, and the work spans assembly, dating, a designed comparison with seed noise as the error, and a rule validated out of sample.

7. Income bands. Real ACS microdata for eight metros as published. The solver cuts renter household income at four percentiles with 90% margins and applies a publish rule on the margin.
Strategy 10

Verdict and reasoning
Approve. Nothing is planted. The geography, the weights, the replicate design and the top-coded components are all in the real files, and each produces its own checkable result before the publish list comes out right.

Key lesson
A shallow version hangs the result on one hidden or planted thing: a planted block, a built-in factor or a documented procedure. Once seen, the rest is routine. A legitimate method choice is fine even when it is the hardest step. The strongest versions spread the difficulty across several pieces of real work, each checkable, so more careful work keeps earning more.


Biomedical and Health Sciences
Each strategy below is an investigation, not a trick. Real public data force a chain of connected work on the analyst, each link produces a result you can check, and more careful work earns more: a quick pass gets some results right, and only sustained, self-checking work gets them all. Each strategy names where the weight of the work sits, the investigation, where the phenomena already live in public data, a scenario with real breadth, where a hurried analyst goes wrong, what the solver delivers and how to keep every result deterministic. The weight sits somewhere different in each one (assembly, measurement, validation, attribution, synthesis, allocation and more), so read them as twelve different shapes of hard work, not one recipe. The number of hard results also differs, from three to seven, because it follows the real work. The strategies cover all nine analysis types; only one is causal and only one ends in a yes or no call. Use them as patterns, not as tasks to copy.

What fails a task
The design that fails is one hidden or planted thing that, once caught, flips the whole answer: a planted defect or decoy, a procedure the materials spell out (rule application), or a shallow hidden factor (a confounder, subgroup, event or measurement change you built into the data that one sentence would give away and one routine adjustment, such as a stratification, an extra term, a filter or a reweight, would fix). Reading one field or clause a particular way and replaying a published figure are banned too, and several of these together are still banned. One-fact test: if telling the solver one fact makes the rest routine, redesign. A legitimate method choice is fine even when it is the hardest step, and a hidden factor is fine when it is real and finding or correcting it takes modelling. Strong tasks put genuine work at more than one step, so careful work earns more. See Deep reasoning for what difficulty throughout looks like.

Biomedical & Clinical Research
Clinical research data record how patients enter, leave and get measured: registrations at several centres, drug levels drawn at odd times, diagnoses confirmed for some people and not others, studies that share participants. These investigations make the solver rebuild that process piece by piece, and each piece can go wrong on its own.

1. Forecasting transplants from a waitlist where death and delisting compete
Analysis type and answer shape
Forecasting & Predictive; a quarterly forecast path with a band, plus the drivers of the change from last year.

Where the weight sits
Validation-heavy. Most of the effort goes into proving the forecast would have held at earlier dates, including across a real allocation change.

The investigation
Six connected pieces, each with its own check:

One timeline per candidate from registrations, status changes and score updates, where the same person can hold registrations at more than one centre, reconciled to the centre's published waitlist counts.
Transplant, death and removal estimated as competing events, with delayed entry for candidates already waiting when the window opens, by score band and active or inactive status.
A quarterly model of new listings.
A rerun of the whole pipeline at several earlier cut dates, scored against what happened, which settles whether the years before the policy change belong in the fit.
A band built by simulation that carries parameter and arrival uncertainty, whose back-tested coverage matches the stated level.
A split of the forecast change from last year into list size, list mix and new listings.
Where it shows up in real data
OPTN STAR files (candidate-level waitlist, status and score histories, by data request), SRTR program-specific reports (public, center-level waitlist outcomes) and the USRDS research files for kidney candidates (by application). Real allocation changes, such as liver acuity circles in 2020 and lung continuous distribution in 2023, give the series genuine regime breaks.

Scenario
A liver transplant program's surgical director is staffing surgeons and ICU beds for the next eight quarters. The folder holds ten years of candidate registrations with every status and score update, and SRTR's published reports for the centre. She needs deceased-donor transplants by quarter with an 80% band and a short account of why the path differs from last year's volume.

Where a hurried analyst goes wrong
Counting registrations as people, so multiply listed candidates inflate the list. Censoring deaths and removals, which treats those candidates as if they could still be transplanted. Fitting on everyone listed in the window without delayed entry, which overstates early hazards. Pooling across the policy break because the full fit looks better in sample. Reporting a band from the model's parameters alone, which comes out far narrower than the back-test shows.

What the solver delivers
A reconciled candidate count against the published report; the four- and eight-quarter totals with bands and their back-tested coverage; a back-test table of coverage and error at each earlier cut date; the driver split of the change from last year. The registrations pin the count, the outcomes after each cut date pin the back-test, and the forecast must sit inside bands that every defensible competing-risks model reaches.

Keeping it deterministic
The prompt fixes the horizon, which transplants count, the band level and the earlier cut dates to test against. Grade the reconciled count exactly, the totals and back-test coverage in bands checked across cause-specific and subdistribution models, and the largest driver by sign and rough size. The prompt must not mention deaths, removals, multiple listing, candidates listed before the window or the policy change.

2. A starting-dose table from thousands of sparse, mistimed drug levels
Analysis type and answer shape
Forecasting & Predictive; a grid of cells, each with a dose and its predicted target attainment.

Where the weight sits
Modeling-heavy. The specification of a population model (structure, covariates, error) carries most of the difficulty, and the assembly before it decides whether that model can be fit at all.

The investigation
Dose histories and true sample times have to be rebuilt from administration records, and the solver should measure how often a labelled trough was drawn somewhere other than just before the next dose. Renal function is unstable in many of these patients, so the solver chooses which creatinine value drives clearance and checks how much that choice matters. Then a nonlinear mixed-effects model with clearance tied to renal function and weight, a combined proportional and additive error, and diagnostics that show whether a one- or two-compartment structure fits. Predictions for later levels in held-out patients validate it. Simulating each grid cell finds the dose with the best target attainment.

Where it shows up in real data
MIMIC-IV and the eICU Collaborative Research Database (credentialed access through PhysioNet: free, after human-subjects training and a signed data use agreement) hold vancomycin administration times and serum levels for thousands of ICU patients. Compare each level's draw time with the dose times around it and you can see how often a "trough" was really drawn just before the next dose. Published vancomycin population models and the 2020 consensus guideline's 24-hour AUC target of 400 to 600 mg·h/L (for serious MRSA infections, assuming an MIC of 1) give the context.

Scenario
A stewardship pharmacist is replacing a trough-based nomogram. The extract holds every vancomycin administration, serum level, creatinine, weight and dialysis record for the adult ICU stays. He needs a maintenance dose and interval for each cell of a renal function by body weight grid, with each cell's predicted share of patients whose 24-hour AUC falls inside the target on day two.

Where a hurried analyst goes wrong
Taking the "trough" label at face value. Using admission creatinine for patients whose kidneys are changing by the hour. Keeping patients on dialysis in a model of renal clearance. Fitting additive error to a measurement whose error grows with the level. Regressing troughs on dose and converting to AUC with a fixed ratio, which aims at the median patient so many cells under-dose.

What the solver delivers
The share of mistimed levels; the model with its covariate effects and between-patient variability; a validation summary on held-out patients; the dose table with each cell's attainment. Administration and draw timestamps pin the mistiming share, held-out levels pin the validation, and the simulation pins the table once the model is right.

Keeping it deterministic
The prompt pins the target range, the time point, the grid boundaries, the allowed intervals, dose rounding and which patients the table is for. Grade the mistiming share in a band, the clearance covariate effects by direction and rough size, each cell within one rounding step and the attainment shares in bands, after checking that one- and two-compartment models give the same rounded doses. Do not say that sample times are unreliable, which creatinine to use or that the answer needs simulation.

3. A screening threshold when only the positives were worked up
Analysis type and answer shape
Opportunity Sizing & Decision Support; a sensitivity and referral curve across thresholds, with the chosen setting.

Where the weight sits
Measurement-heavy. The hard part is estimating a quantity the data never observe directly: how many cancers a threshold would have caught among men who were never worked up.

The investigation
Which cancers count as present at a screen? The solver decides that from stage and timing in years of follow-up. Work-up after a screen is far from random, so the next piece models its probability from PSA, exam findings, age and earlier screens, and checks how well the weights balance the verified and unverified men. PSA varies within a person from year to year, so a man just under a threshold at one screen may cross it at the next, and the solver measures that variation from the annual repeats. The weighted curves follow, with intervals that carry the weighting through. An external check against published cut-point sensitivity explains any gap by the difference in populations, not by a tuning knob.

Where it shows up in real data
The PLCO Cancer Screening Trial (NCI Cancer Data Access System, by project application) has annual PSA results, diagnostic work-up concentrated after a positive screen (referred to the participant's own physician) and cancers ascertained over years of follow-up. The Prostate Cancer Prevention Trial offered an end-of-study biopsy regardless of PSA, so its published sensitivity at each PSA cut point gives an external check on any correction. It enrolled a different population (men with a low PSA and a normal exam at entry), and its patient-level data are not part of the PLCO release, so do not plan on them unless you have confirmed access. NLST, also through CDAS, has the same structure for lung CT.

Scenario
A regional screening program is setting its PSA referral threshold. It must refer at least 85% of the clinically significant cancers diagnosed within three years of a screen, at the lowest referral rate. The data cover six annual screening rounds, every diagnostic procedure and every cancer found in follow-up. The answer is the curve, one threshold with its estimated sensitivity and referral rate, and how sure the program can be that it clears the floor.

Where a hurried analyst goes wrong
Computing sensitivity only among men who had a biopsy. Counting every unbiopsied man as cancer-free. Counting a cancer found four years later as one the screen missed. Treating each screen as independent of the man's other screens. Reporting the point estimate against the floor without saying how likely the threshold is to fall short.

What the solver delivers
The verification model with a balance check; the sensitivity and referral curve with intervals at each grid threshold; the selected threshold; a comparison with the published external sensitivities. The follow-up file pins which cancers count, the screening records pin the referral rates, and the weighted curve pins the step.

Keeping it deterministic
The prompt fixes the cancer definition, the window, the floor, the threshold grid and whether the point estimate or the lower bound must clear it. Confirm that every reasonable verification model selects the same step, then grade that step, the referral rate in a band and three or four points of the curve in bands. The prompt must not mention verification, who was biopsied or any correction method.

4. Ranking explanations for an inflated genome-wide signal
Analysis type and answer shape
Root-Cause; competing explanations ranked against evidence, each with its share of the inflation, and a corrected locus count.

Where the weight sits
Investigation-heavy. Several explanations compete, each predicts a different pattern across the releases, and the solver has to test them one by one and follow what the tests show.

The investigation
Before any test means anything, the four releases need harmonizing: genome builds, effect alleles, strand-ambiguous variants and allele frequencies checked against an ancestry reference. LD score regression on each release, with LD scores that match its ancestry, separates confounding (the intercept) from polygenicity (the slope), and the ratio of the two says how much of each release's inflation is confounding. One LD score regression on the mixed-ancestry meta-analysis is not valid, so the combined inflation has to be judged from the per-release results. Cross-trait intercepts between the European releases measure how correlated their null statistics are, which reveals shared participants. The meta-analysis is then redone with that correlation handled, loci clumped with ancestry-matched references, and the count compared with the original.

Where it shows up in real data
Public GWAS summary statistics (GWAS Catalog full files, the Neale lab's UK Biobank releases, FinnGen, Biobank Japan, GIANT and PGC consortium files) with 1000 Genomes as the LD reference. The overlap is genuine: some consortium releases already include UK Biobank participants.

Scenario
A consortium analyst meta-analysed four public releases for one trait, each with several million variants, and found a genomic inflation factor of 1.38 and more than 200 significant loci. The steering committee wants the competing explanations ranked against the evidence, each with the diagnostic that supports or rules it out, and a corrected count of independent loci.

Where a hurried analyst goes wrong
Meta-analysing releases on different builds or allele codings, which silently flips some effects. Dividing every statistic by the inflation factor, which removes real polygenic signal. Running European LD scores on the East Asian release, which gives a wrong intercept. Reading one combined intercept on mixed ancestries. Never asking whether two releases share participants.

What the solver delivers
A harmonization log with the variants dropped and why; per-release intercepts, slopes and ratios; the cross-trait intercepts and the pair they implicate; the ranked explanations; the corrected locus count. The summary statistics and reference panels pin each number, and the pattern of intercepts pins the ranking.

Keeping it deterministic
The prompt pins the trait, the significance threshold and what counts as an independent locus. Make sure the intercepts clearly separate the top explanation from the rest, then grade the ranking, the overlapping pair, each intercept in a band and a band for the locus count that holds across reasonable clumping windows. Do not mention overlap, harmonization, LD scores or genomic control.

Epidemiology & Public Health
Population health numbers come out of forms, surveys, laboratories and reporting systems that change and leave gaps. These investigations make the solver model how the numbers were produced at several points (a form revision, a device change, laboratory noise, suppression, reporting lag) before any epidemiological quantity means anything.

5. Bridging a trend across a staggered change of instrument
Analysis type and answer shape
Comparative & Explanation; a bridge between two national figures, split into measurement and real change and into state contributions.

Where the weight sits
Attribution-heavy. The pieces of the bridge have to add up exactly, and the hard part is deciding how much of each state's movement belongs to the form and how much to the world.

The investigation
The solver starts with a state by year panel of first-trimester care by certificate version, checked against published national totals, and decides how births with the month of first care not stated enter the share. The size of the break at each state's adoption year comes from comparisons with states that have not yet switched, since a plain two-way fixed effects model is biased under staggered timing. The break is allowed to vary with maternal characteristics, which the solver has to show matters before relying on it. Re-expressing every state and year on one definition lets the national change split into measurement and real parts, with each state's contribution. Intervals on each piece come last, with a check that the bridge closes.

Where it shows up in real data
NCHS natality public-use files (hosted by NBER) flag births recorded on the 2003 revised birth certificate, which states adopted between 2003 and 2016. The revision changed how the start of prenatal care is recorded, and NCHS has documented that the two versions are not comparable. The public-use microdata carry no state identifiers from the 2005 data year on, so state-by-year work needs CDC WONDER's natality tables (check which prenatal care items each database reports for each certificate version) or an NCHS restricted-data application. The October 2015 switch to ICD-10-CM in HCUP discharge data is a similar real break.

Scenario
A maternal health program has to report how much of the 2005 to 2016 change in the share of births with first-trimester prenatal care was real. The inputs are state, year and maternal characteristic tables for both certificate versions, several million births a year. The answer is a bridge from the 2005 national figure to the 2016 figure, split into measurement change and real change, with each state's contribution.

Where a hurried analyst goes wrong
Restricting to states on the revised form, which are not typical of the country. Adjusting every year by one national ratio, which ignores that the break differs by group. Using a two-way fixed effects model that compares late adopters with early ones. Dropping the not-stated births without checking whether they move at adoption. Reporting a bridge whose pieces do not sum to the change.

What the solver delivers
The adoption timeline; the break estimate overall and by group; the national series on one definition; the bridge with state contributions and intervals. The adoption years and the tables pin the panel, the not-yet-switched comparison pins the break, and arithmetic pins the closure.

Keeping it deterministic
The prompt fixes the endpoints, the measure, the treatment of births with care not stated and which version the figures are expressed on. Grade each bridge component in a band, the real change's sign and rough size, the three largest state contributions and closure exactly. The prompt must not mention the revision, adoption years or any comparison group.

6. An alert rule for 60 wastewater sites with a fixed false-alarm budget
Analysis type and answer shape
Data Quality, Monitoring & Alerting; a monitoring rule specified in full, with its expected alert count, back-tested false-alarm rate and lead time.

Where the weight sits
Design of the rule itself. The solver is building a measuring instrument, and every choice (scale, baseline, persistence, what counts as a shift) has to be justified by how the rule behaves on seasons it never saw.

The investigation
Four pieces, and the first carries a lot. Each site's series is put on a comparable scale, using whatever flow, population or fecal-strength normalization the release supports, and its noise modelled on the log scale with its own variance and autocorrelation, so that a threshold means the same thing everywhere. Laboratory or method shifts show up as steps that sites sharing a laboratory (where the data record it) or neighbouring sites experience together, and the solver finds them and re-baselines. Threshold and persistence are chosen by back-testing on held-out seasons against hospital admissions, and the rule's expected alert count and lead time are projected for next season with their spread.

Where it shows up in real data
CDC NWSS site-level wastewater datasets on data.cdc.gov (check which concentration, normalization, flow and laboratory method fields the current release includes; it also carries WastewaterSCAN samples, so remove the overlap if you use both), WastewaterSCAN's own site data (licensed CC BY-NC; the program asks research users to contact it first), and NHSN weekly hospital respiratory admissions by jurisdiction on data.cdc.gov for the outcome.

Scenario
A state epidemiologist must set one alert rule for 60 sites that triggers a hospital readiness notice, with no more than one false alarm per site per season. A false alarm is an alert not followed by a rise in statewide admissions within three weeks. Four seasons of samples are available, most sites sampled once or twice a week. The answer is the rule, the expected number of alerts next season, and the back-tested false-alarm rate and lead time.

Where a hurried analyst goes wrong
Using one percentile for every site, so noisy sites alarm constantly and quiet ones never do. Treating a laboratory change as a surge. Setting persistence as if samples were independent. Tuning and scoring on the same seasons. Reporting the alert count as a single number with no spread.

What the solver delivers
The rule written so another analyst could run it; the list of detected method shifts with dates; the held-out false-alarm rate and median lead time; the expected alert count next season with a range. The admissions series pins the false alarms, the shared steps pin the shifts, and the held-out seasons pin the rule's performance.

Keeping it deterministic
The prompt fixes the false-alarm definition, the budget, the outcome series and the seasons to hold out. Several thresholds may meet the budget, so grade the detected shifts, the alert count, the false-alarm rate and the lead time in bands rather than the threshold itself. The prompt must not mention laboratory changes, site noise, autocorrelation or holding out a season.

7. An allocation by expected burden from suppressed, small and lagged counts
Analysis type and answer shape
Opportunity Sizing & Decision Support; an allocation to a fixed total, with its sensitivity.

Where the weight sits
Allocation under constraints, driven by a quantity no table reports: next year's expected deaths in counties where this year's are suppressed, noisy or not yet in.

The investigation
The incomplete recent months come first: completeness factors estimated from how earlier provisional releases filled in, applied with their own uncertainty. Suppressed counts enter a count model as the bounded values they are. Small counties are pooled across several years toward similar counties, with the model-based county estimates as a check rather than an input to copy. That yields next year's expected deaths by county with intervals, and from those an integer allocation that sums exactly to the total. The last piece is a sensitivity analysis of how many kits move between counties under other reasonable pooling and completeness choices.

Where it shows up in real data
CDC WONDER county mortality (counts below 10 suppressed, rates flagged unreliable below 20), NCHS provisional county-level drug overdose death counts (lagged and suppressed), NCHS model-based county estimates of drug poisoning mortality and Census population estimates by age. WONDER's data use agreement restricts presenting counts under 10, so read it before deriving any suppressed value from other queries; the model should work with the bounds.

Scenario
A state health department is distributing 120,000 naloxone kits to its counties in proportion to the overdose deaths expected in each county next year. The inputs are several years of final and provisional county counts, every provisional release since they began, and county populations by age. The answer is kits per county, summing to the total, with how much the allocation would move under other defensible assumptions.

Where a hurried analyst goes wrong
Allocating on age-adjusted rates, which are built for comparison, not counting. Setting suppressed counties to five. Treating one year of a small county's deaths as its true level. Using the provisional months as if they were complete. Rounding shares independently so the kits no longer sum to the total.

What the solver delivers
Completeness factors by months of lag; expected deaths by county with intervals; the allocation; a sensitivity table. Earlier provisional and final releases pin the completeness factors, the bounds pin the suppressed cells, and the total pins the allocation's arithmetic.

Keeping it deterministic
The prompt pins the total, the target year, the rounding rule and that kits follow expected deaths. Grade the completeness factors, the largest counties' shares and the rural share in bands that hold across reasonable pooling choices, and the sum exactly. Do not mention suppression, pooling or provisional data.

8. A blood pressure distribution across two devices and a complex sample design
Analysis type and answer shape
Descriptive & Distribution; percentiles and shares above two cut points by age band, sex and survey cycle, all on one measurement scale, with intervals.

Where the weight sits
Measurement and design. The quantity is simple to state; the work is putting more than a decade of readings taken under two protocols onto one scale, inside a sample design that every estimate has to respect.

The investigation.

A bridge between the auscultatory and oscillometric readings, fit on participants measured both ways, that lets the difference vary with the level of blood pressure, age and sex rather than assuming one offset.
A treatment of how the auscultatory readings were recorded (to the nearest even number, with whatever terminal-digit preference the solver measures in each cycle), so that percentiles and shares near round cut points are not distorted by the recording grid.
Design-based estimates for each cycle with the examination weights, strata and primary sampling units that cycle requires (combined files have their own weights), with intervals that carry the bridge's uncertainty as well as the sampling error.
The change across cycles on one scale, with a judgment of how much of it exceeds what the bridge's uncertainty allows.
A self-check before any bridging: reproduce a published national estimate for one cycle on its original protocol, so pipeline errors are caught before they mix with measurement questions.
Where it shows up in real data
NHANES examination files for blood pressure, with auscultatory and oscillometric readings in separate files and protocol documentation for each cycle. Physicians took auscultatory readings with a mercury sphygmomanometer through 2017 to 2018; the 2017 to 2018 cycle also took oscillometric readings from the same participants in random order, and later cycles are oscillometric only. The NHANES tutorials document the design variables and which weights to use when cycles are combined, and NCHS data briefs on hypertension prevalence give published figures to check against.

Scenario
A state cardiovascular program is setting targets and wants the national adult distribution of systolic and diastolic blood pressure for every NHANES cycle from 2009 onward: the 10th, 50th and 90th percentiles and the shares at or above 130/80 and 140/90, by age band and sex, expressed on the oscillometric scale the program's clinics now use. The folder holds the demographic, examination and medication files for every cycle, tens of thousands of examined adults in all.

Where a hurried analyst goes wrong
Pooling readings from the two protocols as if they were the same instrument. Shifting older cycles by one average offset. Reading percentiles straight off rounded readings. Using interview weights for examination measures, or combining cycles without the matching weight. Computing standard errors as if the sample were simple random. Reporting a trend that is smaller than the bridge's own uncertainty.

What the solver delivers
The bridge with its fit on the overlap participants; the reproduced published estimate; the percentile and share table by cycle, age band and sex with intervals; the change across cycles and how much of it is clearly real. The overlap participants pin the bridge, the published figure pins the pipeline, and the design variables pin every interval.

Keeping it deterministic
The prompt fixes the population, the cycles, the target scale, which readings are averaged, the cut points and whether people on treatment are included. Grade the reproduced figure tightly, the bridge's direction and rough size, the percentiles and shares in bands that hold across reasonable bridge models, and the direction of change. The prompt must not mention the protocol change, rounding, the overlap cycle or which weights to use.

Pharmacology, Pharmacoepidemiology & Safety
Drug safety and effectiveness questions rest on records built for other purposes: spontaneous reports, trial datasets with crossover, claims. The work is turning those records into a fair count or a fair comparison, and that takes several separate steps, each of which can bias the result on its own.

If you assemble or link data
Pharmacoepidemiology tasks often join several sources, and some need a business layer such as a budget or a decision bar. Keep the phenomena real. If you have to construct an effect, it must run through the whole dataset, not only through the units that decide the answer, and finding and correcting it must take modelling, not one cross-tab.

9. Conforming two decades of spontaneous reports into one case-level table
Analysis type and answer shape
Data Extraction & Conformation; a conformed table with reconciled totals and a measured linkage error.

Where the weight sits
Assembly-heavy. Building one trustworthy case-level table from two schemas, free text and duplicate senders is most of the task, and every stage leaves a number someone can audit.

The investigation
Seven stages, each leaving a count someone can audit:

Conform the legacy and current schemas into one layout.
Collapse each case's follow-up versions into one record.
Find the cases that appear in both systems at the changeover.
Normalize free-text drug names with approximate matching, at a threshold validated on a hand-checked sample.
Map combination products to each ingredient.
Link duplicate reports from different senders (a manufacturer and a clinician, say) on age, sex, event date, country and drug list, choosing the threshold from the score distribution and reporting precision and recall on a labelled sample.
Compare the final counts with the public dashboard and explain every difference by a stage above.
Where it shows up in real data
FDA's FAERS quarterly files (from the fourth quarter of 2012) and the legacy AERS files (first quarter of 2004 to third quarter of 2012), which use different report identifiers; the openFDA drug event API and the FAERS Public Dashboard for cross-checks; and NLM's RxNorm with RxNav approximate matching for drug names.

Scenario
A pharmacovigilance team building a quarterly signal pipeline needs unique-case counts for 20 named drug-event pairs from 2004 to 2024, plus a reconciliation that runs from raw reports to unique cases, quarter by quarter. The raw files hold tens of millions of rows across more than 80 quarterly releases.

Where a hurried analyst goes wrong
Keeping the latest version of each case but missing those reported in both systems. Exact-matching uppercase drug names, which misses misspellings, brand names and combinations. Linking duplicates on case number alone. Picking a match threshold without measuring its error. Reporting counts that do not tie back to the raw files.

What the solver delivers
The 20 counts; the quarter-by-quarter reconciliation from raw reports to unique cases; the name-matching and linkage precision and recall on the labelled samples; the explained differences from the dashboard. The raw files pin the reconciliation, the labelled sample pins the error rates, and the flat part of the match-score distribution pins the counts.

Keeping it deterministic
The prompt pins the period, the ingredient list, the event level (MedDRA preferred terms) and that counts are of unique patients' cases. Grade the 20 counts in bands that hold across thresholds in the flat part of the match-score distribution, require the reconciliation to close and grade the linkage error in a band. The prompt must not mention duplicates, the legacy files or approximate matching.

10. A survival effect when control patients switched to the new drug
Analysis type and answer shape
Experiment & Causal; an estimate with an interval against a bar, reached by reconciling several estimators.

Where the weight sits
Synthesis-heavy. No single method is clearly right, so the work is building the evidence each method needs, running the ones the data can support and reconciling where they disagree.

The investigation
Everything rests on patient timelines built from visit-level records: progression, switch, other later therapies, death and censoring. Then a description of who switched, when and how they differed at progression from those who did not. Each method whose assumptions the data might support is estimated with its own diagnostic: weight distributions and covariate balance for inverse probability of censoring weights, a check of whether a common treatment effect is plausible for a rank-preserving structural model, and whether switching happens only at progression for a two-stage model. The synthesis is the heart of it: explaining why the estimates differ, settling on the one the evidence best supports, bootstrapping the whole procedure for the interval, and saying how the call would change under the alternatives.

Where it shows up in real data
Patient-level oncology trials with both arms through Vivli, YODA and the NCTN/NCORP Data Archive (each by request), some of which allowed crossover after progression. Project Data Sphere mostly shares comparator arms, so check that a trial has both arms before building on it. NICE Decision Support Unit Technical Support Document 16 reviews the candidate methods and the assumptions each one needs; the trial data decide which assumptions hold.

Scenario
A health plan's technology committee will add a second-line drug to its pathway only if, had no one switched, it would cut the hazard of death by at least 20%. The intention-to-treat hazard ratio is 0.88. The trial files hold baseline, visit, treatment, progression and survival tables. The answer is the adjusted hazard ratio with its interval, the call, and how robust the call is.

Where a hurried analyst goes wrong
Censoring control patients at the switch, or excluding switchers, both of which select on prognosis. Taking the switch date from a summary variable without checking it against the treatment records. Ignoring other later therapies that both arms received. Running one adjustment method without checking its assumptions. Using a naive interval that ignores the estimation of weights or the effect parameter.

What the solver delivers
The rebuilt timelines with switch counts; the comparison of switchers and non-switchers; each method's estimate with its diagnostic; the reconciled hazard ratio with its bootstrap interval; the call and its robustness. The visit records pin the timelines, the trial data pin the diagnostics, and the agreement of defensible methods pins the band.

Keeping it deterministic
The prompt pins the population, the threshold and that the target is survival had no one switched. Grade the switch count exactly, the comparison of switchers by direction, the hazard ratio in a band that every method with defensible assumptions falls inside, and the call. The prompt must not name the methods, the prognostic factors or why switchers differ.

Healthcare Delivery & Health Economics
Delivery and economics tasks go deep when a cost or an outcome has to be explained across a large system: thousands of products, hundreds of providers, several years. The honest answer needs units made comparable, chance separated from performance and a decomposition that holds up at every level.

11. Finding what drove a drug spending overrun across thousands of products
Analysis type and answer shape
Root-Cause; a drill-down through the hierarchy with a bridge from budgeted to actual spending at each level.

Where the weight sits
Triage-heavy. Thousands of products move at once, many offset each other, and the solver has to find the few movements that matter before attributing anything.

The investigation.

Map each NDC to ingredient, strength and a common unit.
Handle suppressed cells as bounded and carry the bounds into every total.
Screen hundreds of ingredients for movers, separating real shifts from offsetting ones and from noise in thin products.
Split the change into price, utilization and mix with an additive, order-independent decomposition (a Shapley, Bennet or logarithmic mean Divisia split, say), with a stated treatment of products entering and leaving.
Follow the split from class to ingredient, where the leaf that explains the overrun can differ from the largest dollar mover, and check that every level reconciles to the one above.
Where it shows up in real data
Medicaid State Drug Utilization Data on data.medicaid.gov (state, quarter and NDC, with counts under 11 suppressed), the Medicaid Drug Rebate Program product file with each NDC's unit type, the FDA NDC Directory, NADAC and the Medicare Part D Spending by Drug dashboard.

Scenario
A state Medicaid pharmacy director's gross drug spending rose 14% against a 6% budget. The folder holds three years of quarterly utilization for every NDC the state paid for, the rebate product file and the budget assumptions. She needs the therapeutic class, then the ingredient, that explains the overrun, and how much of it is price, utilization and product mix.

Where a hurried analyst goes wrong
Comparing units that mean different things across products. Ranking classes by dollar increase and stopping at the largest. Splitting price and volume one after the other, so the answer changes with the order. Giving new products no prior price, so their spending vanishes from the bridge. Letting the class bridge and the ingredient bridge disagree.

What the solver delivers
The conformed product table; a short list of the movers that matter; the bridge at class and ingredient level; the leaf that explains the overrun with its price, utilization and mix pieces. The product files pin the units, the utilization data pin each bridge, and order-independent methods agree on the leaf.

Keeping it deterministic
The prompt pins gross spending, the periods and the hierarchy. Grade the leaf, the class bridge and the leaf bridge in bands that hold across order-independent methods, and closure at each level exactly. The prompt must not mention units, suppression or how to split price from volume.

12. Choosing facilities for inspection from noisy, risk-adjusted outcome ratios
Analysis type and answer shape
Anomaly Detection & Diagnostics; a ranked list under a cap, with the probability behind each place on it.

Where the weight sits
Estimation of a hard-to-measure quantity: each facility's true, persistent performance, which chance and drift hide in every year's ratio.

The investigation
Three hard results, in order. First, one model of how much facilities truly differ beyond Poisson noise and how that true performance drifts from year to year, fit to four years per facility, including the facilities that opened or closed partway through. Second, a test of that model out of sample: does the pooled estimate from the first three years predict the fourth year better than the raw ratio does? Third, each facility's probability of truly exceeding the bar, with the ranking built on that probability and the gap at the cut measured.

Where it shows up in real data
The Dialysis Facility Reports (public, with observed and expected deaths, hospitalizations and patient-years for four years per facility), CMS Care Compare dialysis files and USRDS annual data.

Scenario
A state survey agency can make 12 focused inspections this year and wants the 12 dialysis facilities most likely to have mortality truly at least 20% above expected. The folder holds four years of reports for every facility in the state. The answer is a ranked list of 12, the first facility left out and the gap between them.

Where a hurried analyst goes wrong
Ranking by last year's ratio, which favours tiny facilities with one bad year. Ranking by p-value, which favours large facilities with a small but precise excess. Averaging four years equally, as if performance never changed. Treating a facility that opened partway through as if it had four full years. Never checking whether the pooled estimate predicts better than the raw one.

What the solver delivers
The between-facility variance and drift estimates; the out-of-sample comparison of pooled and raw predictions; each facility's probability of exceeding the bar; the 12, the first left out and the gap. The reports pin the variance and drift, the fourth year pins the validation, and the probabilities pin the cut.

Keeping it deterministic
The prompt pins the cap, the bar and the outcome. Check that reasonable priors and drift models give the same 12 with a clear gap at the cut, then grade the set, the facility just below it and the validation result. The prompt must not mention noise, pooling years or ranking by probability.

Shallow versions of these ideas
Several ideas above have a shallow twin that gets sent back because one planted or hidden thing decides it. Others look narrow but are legitimate analysis and pass. Decide which designs you would send back before you open the reasoning.

Read each task design. Send back the ones whose result turns on a planted defect, a shallow hidden factor, a documented procedure or a field reading, and approve the ones built on honest analysis of the real data.

These are task designs, not prompts. The question is whether one hidden or planted thing, once caught, flips the whole answer.

1. Waitlist forecast. The author marks a block of 30 candidates as inactive in the waitlist file, and the task is to forecast transplants after noticing they cannot receive offers.
Strategy 1

Verdict and reasoning
Send back. One planted block decides it, and "filter the inactive candidates" makes the rest a count. That is a shallow hidden factor.

Revised design
Use real waitlist histories as released. The solver rebuilds candidate timelines across centres, treats death and removal as competing events with delayed entry, models new listings, back-tests at earlier cut dates across the policy change and splits the change from last year into its drivers.

2. Waitlist forecast, narrow version. A clean one-row-per-candidate file, no policy change in the window and no back-test asked for. Runs that censor deaths overshoot, and runs that treat death as a competing event get the total.
Strategy 1

Verdict and reasoning
Approve. Nothing is planted, and treating death as a competing event is a legitimate method, not a hidden fact. Adding raw registrations, a back-test and a driver split would give careful work more to earn.

3. Prenatal care trend. One state's natality file codes unknown start-of-care months as 99 instead of blank, and recoding it changes the national trend enough to flip the report.
Strategy 5

Verdict and reasoning
Send back. The task is won on reading one field's coding, which is a data semantics stump, and one sentence fixes it.

Revised design
Use the real staggered adoption of the revised certificate. The solver builds the state panel, estimates the break against states not yet switched, shows whether it varies by group and bridges the national change into measurement and real parts with state contributions.

4. Dialysis inspections. The author enters one facility's expected deaths at a tenth of the true value, so it tops the list, and the solver must catch the error to get the 12 right.
Strategy 12

Verdict and reasoning
Send back. Spotting one wrong value decides the task. That is a planted defect.

Revised design
Ship the facility reports as published. The cut depends on estimating variation beyond chance, drift across four years, a check that pooling predicts the next year and a ranking on the probability of a true excess.

5. Drug spending overrun, narrow version. Twelve products with clean units and no suppression. The only thing that separates runs is whether they split price and volume in an order-independent way; a sequential split lands on the wrong product.
Strategy 11

Verdict and reasoning
Approve. The products are real and nothing is planted; an order-independent split of price and volume is legitimate analysis. Using the full product file with its suppressed cells and hierarchy would make the task richer.

6. Crossover adjustment. The trial's analysis plan in the folder lists the switching adjustment step by step, and the runs lose by skipping its re-censoring step.
Strategy 10

Verdict and reasoning
Send back for rule application. Following the written steps literally gives the answer, so no judgment decides the task.

Revised design
Let the plan fix only the endpoint and the decision bar. The solver rebuilds timelines from visit records, describes who switched, runs the methods the data can support with their diagnostics and reconciles them into one estimate and a call.

7. Spontaneous reports. Twenty years of public adverse event files conformed across a schema change, with drug names normalized, duplicate reports from different senders linked, the linkage error measured on a labelled sample and every count reconciled to the raw files.
Strategy 9

Verdict and reasoning
Approve. The duplicates, the schema change and the name variants are real, each stage leaves a number to check, and a run that gets the counts roughly right without the reconciliation does not score well.

8. Wastewater alerts. Real site series for 60 sites; the solver puts them on one scale, models each site's noise, finds laboratory shifts from steps shared across sites, chooses the rule on held-out seasons and projects next season's alerts with a range.
Strategy 6

Verdict and reasoning
Approve. The noise, the shifts and the seasonality are how the real data behave, the rule is judged on seasons it never saw, and four separate results can each be checked.

Key lesson
A planted version hides one thing a single sentence would reveal. A version that turns on a legitimate method is fine, even when that method is the hardest step. The strongest versions make the solver do several connected pieces of real work, each checkable, so a careful run earns more than a lucky one.


Economics and Quantitative Social Science
Each strategy below is an investigation, not a trick: several connected pieces of real analytical work that public economic and social data demand, each ending in a result you can check. A quick pass gets some of them right; only sustained, self-checking work gets them all. The strategies differ in where the weight sits (one is mostly assembly, one mostly validation, one a hunt for causes across hundreds of agencies), so read the Where the weight sits line before borrowing a pattern. Find the difficulty in the sources named rather than build it: revised vintages, withheld cells, survey seams, population-control changes, reporting breaks. If you assemble or extend data, it has to behave like the real thing throughout, with many genuine patterns and noise, never one effect added for the solver to find. The ten strategies span all nine analysis types, and none ends in a yes or no call.

What fails a task
Some steps can never carry a task: rule application, reading one field or clause a particular way, a planted defect or decoy, replaying a published figure, an unpinned choice between two defensible methods, and the shallow hidden factor (one confounder, subgroup, event, timing break or measurement change you built into the data, which one sentence would give away and one routine adjustment such as a stratification, an extra term, a filter or a reweight fixes). The planted defect, rule application and the shallow hidden factor are one family: a single hidden or planted thing that, once caught, flips the whole answer. One-fact test: if telling the solver one fact makes the rest routine, redesign. A legitimate method choice is fine even when it is the hardest step. Strong tasks have genuine work at more than one step and credit each sub-result on its own, so careful work earns more. See Deep reasoning for the full test.

Economics & Econometrics
Economic data arrive late, revised, withheld or on someone else's calendar. The four strategies below put the weight in different places: proving a forecast holds, bridging a total, building a panel, and measuring a change across 51 states.

1. A forecast built on the numbers you will actually have
Analysis type and answer shape
Forecasting & Predictive Modeling; a monthly forecast path with a band, a dial (a hold-back) read off it, and a nowcast of where this year's payroll level will land after its benchmark.

Where the weight sits
Validation. The model is ordinary; most of the work is proving that its accuracy and its band hold on the data the office will really have when it decides.

The investigation
The solver has to

rebuild, for each past forecast date, the payroll, wage and receipts history as published at that date, and measure how far early figures moved at each annual benchmark, by horizon;
put twenty years of receipts on a constant-law basis across every change to withholding rates and tables, so the model learns the economy and not the statute;
nowcast the current payroll level from the quarterly census figures already released, a revision estimate that the next benchmark will later confirm or not;
choose the receipts model by a rolling-origin back-test run on real-time data, where the winner can differ from the one that wins on final data;
check the band's coverage on real-time errors and read the hold-back off it at the stated coverage; and
split the office's own past forecast misses into the part from data revisions and the part from the model.
Where it shows up in real data
BLS Current Employment Statistics state estimates, benchmarked each year to the Quarterly Census of Employment and Wages; the St. Louis Fed's ALFRED archive of past vintages; the Philadelphia Fed's Real-Time Data Set for Macroeconomists and its early benchmark estimates of state payrolls; state withholding receipts in monthly revenue reports.

Scenario
A state budget office sets a hold-back on next year's withholding receipts, sized so the state draws on its rainy-day fund in no more than one year in ten. The folder holds every monthly vintage of state payrolls and wages since 2005, the quarterly census releases as they came out, twenty years of monthly receipts, the office's past forecasts and every withholding table in force.

Where a hurried analyst goes wrong
Back-testing on the latest vintage, so the model looks more accurate than it will be in use. Treating the last twelve months of payrolls as settled when they are still due a benchmark. Leaving rate changes in the receipts, so the model learns jumps that were law. Reading the band from model residuals, which carry none of the revision error, so the hold-back comes out too small. Blaming every past miss on the model.

What the solver delivers
A real-time error table by horizon, the constant-law receipts series, the payroll nowcast with its expected revision, the chosen model with its back-test record, the forecast path and band, the hold-back in dollars, and the split of past misses. The vintages pin the revision sizes and back-test errors, the statute pins the constant-law adjustment, a later published benchmark pins the nowcast, and the stated coverage pins the hold-back.

Keeping it deterministic
The prompt fixes the coverage, the horizon and the receipts series. Set the as-of date before a benchmark that has since been published, so the nowcast is checkable. Ship enough vintages that every real-time back-test lands the hold-back in one band, clearly above the final-vintage figure. The prompt must not mention vintages, benchmarks, revisions or rate changes, or say "use only what was known at the time".

2. A revenue shortfall bridged to its causes
Analysis type and answer shape
Root-Cause Analysis; a bridge from budget to actual that reconciles to the dollar, the leaf that explains most of the lasting gap, and a revised forecast for the rest of the year.

Where the weight sits
Attribution. The gap has to be split cleanly into timing, one-time items, mix and rate, down a two-level hierarchy, with interactions that can reorder the leaves.

The investigation
Receipts are first reconciled to the published monthly allocations, with audit collections, refunds and prior-period adjustments pulled out of the base (a checkable list with amounts). Receipts are then shifted back to the period of sale using filing frequencies and allocation lags, and the resulting sales-basis gap is a second checkable figure. Next comes an expected value for every industry and area from its own seasonality and trend, tested on prior years when the city met its budget. The gap is then decomposed down the hierarchy, mix split from rate, with the interaction allocated so the bridge closes and the leading leaf tested under other allocations. Last, the persistent part is separated from what unwinds next quarter and carried into a second-half forecast with a band.

Where it shows up in real data
Texas Comptroller monthly sales tax allocations to cities and its quarterly sales tax data by city and industry; Washington Department of Revenue taxable retail sales by industry and location; state comptroller monthly revenue reports (check which ones break out refund and audit lines).

Scenario
A city finance director's sales tax receipts came in 7 percent under budget for the first half of the fiscal year, and the council wants to know why before it trims spending. The folder has five years of monthly allocations, quarterly taxable sales by industry for the city and its neighbors, the state's refund and audit adjustments, and the budget model built last spring.

Where a hurried analyst goes wrong
Naming the industry with the largest year-over-year dollar drop, which describes collections, not sales. Leaving last year's large audit payment in the base, so last year looks stronger than it was. Using one flat seasonal pattern for every leaf. Stopping at the first level of the hierarchy, or letting one leaf absorb the whole interaction. Projecting the full gap forward when part of it reverses next quarter.

What the solver delivers
The adjustment list, the sales-basis gap, a bridge whose lines sum to the shortfall (timing, one-time, mix, rate by leaf, residual), the leading leaf with its share and band, and the second-half forecast. Published allocations pin the bridge to the dollar; the leaf and its share are pinned when they hold across reasonable baselines and interaction allocations.

Keeping it deterministic
Choose a real episode where the raw drill-down and the aligned one point to different leaves, and where the aligned leaf holds under any reasonable seasonal baseline. If two reasonable interaction allocations reorder the top leaves, choose another episode. The prompt pins the budget figure and the decision (trim now or wait). It does not mention filing frequency, lags, refunds or one-time items.

3. A regional panel built from withheld cells and moving industry codes
Analysis type and answer shape
Data Extraction & Conformation (ETL / Pipeline Build); a conformed county by industry table with reconciled totals, then a cluster growth figure with a band and its sources by county and industry.

Where the weight sits
Assembly. Building one trustworthy panel from suppressed, recoded official files is most of the job; the growth figure at the end is quick once the panel is right.

The investigation
The solver has to

map every withheld cell in every year and bound each from the county hierarchy, the industry hierarchy and its establishment count;
bridge each industry-code revision with split weights estimated from years or areas where both codings exist;
solve the fill jointly so county and industry totals tie at once;
test the fill by masking disclosed cells and measuring how well the method recovers them, a recovery error the author can recompute;
compute the cluster's growth with a band carrying fill and bridge uncertainty; and
attribute that growth to counties and industries, showing how much of it the code bridges alone move.
Where it shows up in real data
The BLS Quarterly Census of Employment and Wages county files, where nondisclosed cells keep their establishment counts; Census County Business Patterns, which gave employment-size ranges for withheld cells before 2017; the Census Bureau's NAICS concordances linking the 2012, 2017 and 2022 codes.

Scenario
A development authority for 19 counties wants a 2013 to 2024 county by four-digit industry employment panel on one industry vintage, tying exactly to the published county and state totals, to report how much an advanced manufacturing cluster grew and where. The folder holds every annual county file, the concordances and the published totals at each level.

Where a hurried analyst goes wrong
Filling each withheld cell with the county residual split by establishment counts, so county totals tie and industry totals do not. Mapping old codes with the concordance's primary match, which quietly moves jobs between the cluster and its neighbors. Never testing the fill. Dropping withheld cells from the growth figure, which biases it whenever they are a real share of the cluster. Reporting growth with no band and no account of where it came from.

What the solver delivers
The conformed panel, a reconciliation report showing every published total tied, the masked-cell recovery error, the growth figure with its band, and a contribution table by county and industry. Published totals are exact, so the spine is checkable cell by cell; the growth and its leading contributors are pinned when every fill that ties both hierarchies lands them in one band.

Keeping it deterministic
Pick a cluster where withheld cells are a real share of employment and where the drop-the-withheld-cells answer falls outside the band. The prompt names the totals the table must tie to, never how to fill cells. Do not ship a third-party imputed file.

4. Why participation moved differently across 51 states
Analysis type and answer shape
Comparative & Explanation; a 51-row comparison table, each state's change split into composition and within-group pieces with bands, and the focal state's rank where the bands allow one.

Where the weight sits
Measurement. Before any state can be compared, the solver has to know how much of each change is the survey's own machinery: population-control updates, model smoothing in the published figures, and sampling error that swamps small states.

The investigation
Several results build on one another. Monthly survey microdata are assembled across the two periods, and each January's population-control update is lined up, since it shifts levels without revising earlier months; the size of that shift for each state is the first result. The solver rebuilds each state's participation rate directly and reconciles it with the published model-based state estimates, explaining the main differences. Each state's change is then split into shifts in age and education mix and changes in rates within those groups, and the pieces are checked to add to the total. Sampling error, taken from the survey's published variance parameters, is carried into every piece, so states whose pieces cannot be told apart are marked rather than ranked. The synthesis names which groups account for the gap between the focal state and its neighbors.

Where it shows up in real data
Current Population Survey basic monthly public-use files (directly from the Census Bureau or through IPUMS CPS); BLS notes on adjustments to household survey population controls, published with each annual update (usually with January data); Local Area Unemployment Statistics state estimates, which are model-based; the BLS parameters and factors for calculating CPS standard errors, a generalized variance function (check what they give for state estimates); American Community Survey age and education tables as an independent check on composition.

Scenario
A governor's workforce council sees its state's labor force participation fall further than its neighbors' since 2019 and wants to know how much is an older population and how much is people within each age group stepping back, with all 50 states and DC compared so it can see where it really sits. The folder holds the microdata extracts, the published state series and the survey's technical documentation.

Where a hurried analyst goes wrong
Differencing the published state rates, which mixes model smoothing with control updates. Treating a January step as a real change. Splitting on age alone, so a shift in education shows up as a rate change. Allocating the interaction to whichever piece comes first, so the ranking depends on the order. Ranking small states on point estimates their sampling error does not support.

What the solver delivers
The control-update size per state, the direct-versus-published reconciliation, every state's change with its composition and within-group pieces and bands, the ranking on the within-group piece with ties marked, and the groups behind the focal state's gap. Published control adjustments pin the first, the adding-up constraint pins the decomposition, and the variance parameters pin which states separate.

Keeping it deterministic
Pick periods where control updates matter for some states, and check that the focal state's rank on the within-group piece holds under any reasonable grouping and interaction allocation. The prompt names the periods, the population and the comparison set. It does not mention population controls, the model-based estimates, composition or decomposition.

Political Science & Public Policy
Political data are full of structure: election calendars, list-maintenance cycles, households that share a mailbox. One strategy below is mostly the design of a rule; the other is an allocation under a budget.

5. An alert rule for voter roll removals
Analysis type and answer shape
Data Quality, Monitoring & Alerting; a weekly monitoring rule with its expected alert count, last cycle's flagged county-weeks, and a reading of each flag.

Where the weight sits
Rule design. The deliverable is the rule itself, and its worth depends on modeling what ordinary removals look like before any threshold means anything.

The investigation
The solver has to

rebuild weekly removals by county and reason from pairs of statewide snapshots, separating them from transfers between counties and from merged duplicate records;
model the expected count with the federal calendar (no systematic removals in the 90 days before a federal primary or general election, and removals of voters who never answered an address notice that tend to follow federal general elections), county size and each county's batch habits;
estimate variance that grows faster than the mean;
set the threshold on held-out years so it meets the alert budget, and state the expected alerts in an ordinary month; and
run the rule on the last cycle and sort each flag into a batch the county reported or one nobody has explained.
Where it shows up in real data
North Carolina State Board of Elections weekly statewide voter files and historical snapshots; the Ohio and Florida statewide voter files; the Election Assistance Commission's Election Administration and Voting Survey, which reports removals by reason for every jurisdiction.

Scenario
An election-monitoring nonprofit can investigate about three county alerts a month across a state's 100 counties. It wants a weekly rule it can run on every new snapshot, the number of alerts the rule should raise in an ordinary month, and the county-weeks it would have flagged in the last cycle. The folder holds two cycles of weekly snapshots and the survey's removal counts by reason.

Where a hurried analyst goes wrong
Counting a voter who moved to another county as a removal. Standardizing each county against its own mean and standard deviation, so the rule fires on every post-election cleanup week and almost never in the quiet period, exactly when an off-schedule purge would matter most. Assuming variance tracks the mean. Setting the threshold by eye instead of to the budget. Handing over flags with no reading of what each one is.

What the solver delivers
The weekly removal series, the rule with its parameters, the expected monthly alert count with a band, last cycle's flagged set, and the reading of each flag. The budget pins the threshold, the snapshot pairs pin the series, and the survey's reported removals pin each flag's reading.

Keeping it deterministic
The alert budget and the evaluation window are in the prompt. The flagged set is pinned when every rule that meets the budget on held-out years flags the same county-weeks, and the expected count sits in a narrow band. The prompt does not mention the quiet period, batch processing, transfers or overdispersion.

6. A mail plan when the message spreads through the household
Analysis type and answer shape
Experiment & Causal Analysis; votes gained by each plan across a range of costs, and the cost at which the ranking flips, with a band.

Where the weight sits
Allocation under a budget. The effect estimates feed a choice between two ways of spending fixed money, and the answer is where that choice changes.

The investigation
Four results feed the plan comparison. Households come first: the group's voter file is standardized so apartment units separate and one home's spelling variants merge, giving a checkable count of households by size. From the randomized experiments, the solver estimates the direct effect on the addressed voter and the spillover to housemates, with voters in untreated households as the clean comparison and both effects allowed to vary with household size. Effects also differ with past turnout, so they are reweighted to the target list's mix of vote histories. The votes each plan buys across the range of printing and postage costs come next, and from them the cost per piece where the ranking flips, with its band.

Where it shows up in real data
Replication files for household-level and multilevel turnout experiments in the Yale ISPS Data Archive, including a design that randomized treatment across nine-digit ZIP codes and across voters within households; state voter files with addresses and vote history to scale the results.

Scenario
A civic group has a fixed mail budget and a fixed list of target households for a municipal election. It must choose between a piece for every registered voter in each household and one piece per household, which reaches more homes before the money runs out. When pieces are cheap the budget covers every voter on the list; when they are dear it does not.

Where a hurried analyst goes wrong
Building households from raw address strings, which merges apartment buildings into giant homes. Using untreated housemates as controls, which shrinks the effect. Valuing a second piece in a home as a full independent effect. Applying the experiments' average effect to a list with a different turnout history. Reporting the flip point as a single number.

What the solver delivers
Households by size, direct and spillover effects by household size with intervals, the reweighted effects for the list, votes per plan across costs, and the flip point with its band. The voter file pins the household counts, the randomized designs pin the effects, and the stated budget and cost range pin the comparison.

Keeping it deterministic
Use real experimental data for the effects and the group's own voter file and costs for the scaling, so the flip point is not a published figure. It must sit in a band that every design-respecting estimate agrees on. The prompt states the budget, the target list and the cost range; it never mentions spillover or says which voters should serve as the comparison.

Sociology & Demography
Demographic tasks go deep when the people you can observe are not the people you need to describe. Here the quantity itself, how long something lasts, is never seen whole.

7. Spell lengths from a panel with seams and edges
Analysis type and answer shape
Descriptive & Distribution Analysis; two sets of distribution cuts with intervals, one for spells as they begin and one for people poor at a given moment, plus a comparison of two family types.

Where the weight sits
Estimating a quantity no file records. Spell length has to be built from monthly calendars, and the panel cuts off both ends and bunches changes at interview seams.

The investigation
The solver has to

build each family's monthly poverty status from the survey calendars and define spells that begin inside the panel, setting aside or modeling those already under way;
estimate exit rates under right censoring with the replicate weights;
find the pile-up of transitions at interview seams, measure it against months away from seams, and smooth it so exit rates are not an artifact of interview timing;
derive the point-in-time view from the entry view, weighted by duration, and reconcile it with a cross-section from the same panel; and
compare one-parent and two-parent families and attribute the gap in long-spell shares to who enters poverty versus how fast each group leaves.
Where it shows up in real data
The Census Bureau's Survey of Income and Program Participation, with monthly calendars and replicate weights, in both the four-month waves of the 2008 panel and the annual interviews since 2014; the Panel Study of Income Dynamics for longer spells.

Scenario
A state commission designing a 12-month cash bridge for families with children under five wants, for families who fall into poverty, the share who leave within 4, 12 and 24 months, and, among families poor at a given moment, the share whose spell will last more than 24 months, for one-parent and two-parent families.

Where a hurried analyst goes wrong
Tabulating only completed spells, which runs short because long spells rarely finish inside a panel. Taking the second figure from a single-month cross-section and never reconciling the two views. Reading seam spikes as real exits. Comparing family types on raw shares, which mixes who enters with how fast they leave. Dropping the replicate weights.

What the solver delivers
Entry-view cuts and point-in-time cuts with intervals, the seam diagnosis, the reconciliation of the two views, and the family-type comparison split into entry and exit pieces. The calendars pin the spells, the replicate weights pin the intervals, and the cross-section pins the point-in-time view.

Keeping it deterministic
Choose a population and panel that the Bureau's poverty dynamics reports do not publish. The cuts are pinned when every estimator that handles censoring and seams lands each share in a narrow band. The prompt defines the family and the poverty measure; it never mentions censoring, seams or which spells to count.

Determinism without a yes or no
None of these strategies ends in a binary call, and none rests on one result. Each sub-result is pinned because the data force it: every sound method lands in one band, a ranking holds at the cut, totals reconcile to published figures, or a stated budget fixes a threshold. Run the rival methods yourself on every sub-result, not only the headline, and check that they agree before you submit.

Psychology & Behavioral Science
Behavioral effects vary across sites more than any single study shows. The strategy below is mostly modeling: estimating that variation, with its own uncertainty, before a design can be chosen.

8. Sizing a multi-site study when sites genuinely differ
Analysis type and answer shape
Opportunity Sizing & Decision Support; a scorecard of five designs against two thresholds, with the cheapest design that passes and how the choice moves with the evidence.

Where the weight sits
Modeling. Between-site variance, its uncertainty and what explains part of it drive every row of the scorecard.

The investigation
The solver has to

sort the dozens of published multi-site effects into those comparable to the planned intervention and justify the set;
estimate between-site variance for that set with a random-effects model, with its own wide interval;
test whether site features (online or in person, country, sample type) explain part of the variance;
derive, for each design, the precision of the average effect and of a new site's likely effect, carrying the uncertainty in the variance into each design's chance of meeting each threshold;
cost each design with per-site and per-participant costs and expected attrition; and
name the cheapest design that passes at the stated probability, and say whether the answer changes at either end of the variance interval.
Where it shows up in real data
Many Labs 1 to 5 and the Registered Replication Reports on the Open Science Framework; Psychological Science Accelerator and ManyBabies data releases.

Scenario
A foundation with $750,000 will fund a multi-site test of a brief intervention and offers five candidate designs, from 8 sites of 400 participants to 50 sites of 60, with a fixed cost per site. It wants each design scored against two thresholds (the average effect pinned within 0.05 standard deviations, and a new site's likely effect bounded tightly enough to decide adoption), each to be met with at least an 80 percent chance.

Where a hurried analyst goes wrong
Running a standard power calculation that treats participants as independent, which favors a few large sites. Pooling every published effect regardless of how comparable it is. Plugging in a point estimate of the variance as if it were known. Ignoring attrition in the costs. Naming a design without saying how fragile the choice is.

What the solver delivers
The comparison set, the variance estimate with its interval, the moderator results, the five-row scorecard with each design's chance of passing and cost, the chosen design, and the sensitivity at the ends of the interval. The replication data pin the variance, the menu and thresholds pin the scorecard, and the budget pins feasibility.

Keeping it deterministic
The menu, the budget, both thresholds and the required chance are in the prompt, along with the family of effects the new study belongs to. Choose the reference studies so the passing design is the same across reasonable comparison sets. The prompt does not mention heterogeneity, random effects or design effects.

Criminology & Justice
Justice data record what agencies did as much as what people did. One strategy below is a search for causes across hundreds of agencies; the other combines several partial models into one forecast.

9. Finding the cause of every break in agency crime counts
Analysis type and answer shape
Anomaly Detection & Diagnostics; a flagged set of agency-years, each with its cause and timing, the false-alarm rate of the flagging rule, and a statewide trend with each kind of break's effect on it.

Where the weight sits
Investigation. Flagging is the start; most of the work is tracing each flagged break to its cause through evidence in several files and ruling out the alternatives.

The investigation
The solver has to

assemble agency-month files across the change of reporting system, linking agencies whose identifiers or names changed and recording months never submitted;
estimate how much the new counting rules alone raise each offense count, using agencies seen under both systems;
model each agency's expected count from its own history and comparable neighbors, with variance that depends on agency size, and set the flag threshold to the stated false-alarm rate on validation agencies;
trace each flagged agency-year to its cause (missing or thin months, the system switch, a new records system visible as a jump in some offense types and not others, a merger or annexation, or a real change) and date it; and
recompute the statewide trend with the flagged agency-years set aside and show how much each kind of break moved it.
Where it shows up in real data
FBI Crime Data Explorer agency files across the 2021 move to incident-based reporting, when the summary system was retired and many agencies reported partial years; concatenated agency files on openICPSR; the Real-Time Crime Index; city incident open data as an independent check.

Scenario
A state statistical analysis center publishing a five-year trend across several hundred agencies wants every agency-year whose change reflects reporting rather than crime found and explained, with a stated rule and its false-alarm rate measured on agencies whose city incident data confirm their counts.

Where a hurried analyst goes wrong
Dropping agencies with fewer than 12 months reported, which misses agencies that sent 12 thin months. Flagging small agencies whose counts are simply noisy. Reading the incident-based counting of every offense in an incident as a real increase. Treating every flag alike instead of finding its cause, so a merger and a missing quarter get the same fix. Publishing the corrected trend without saying what moved it.

What the solver delivers
The linked agency panel, the counting-rule shift by offense, the rule with its threshold and false-alarm rate, the flagged set with a cause and date for each, and the corrected trend with a bridge from the published one. The validation agencies pin the threshold, agencies under both systems pin the shift, and the city incident files and submission records pin each cause.

Keeping it deterministic
The validation agencies and the false-alarm cap are stated, so the threshold is pinned, and the flagged set should hold across reasonable neighbor definitions. Choose a state where breaks of several kinds occur, so no one cause explains most flags. The prompt asks for agency-years where reporting, not crime, drove the change. It does not name the system switch, months reported, mergers or the counting rule.

10. Returns to prison when one way back is closed
Analysis type and answer shape
Forecasting & Predictive Modeling; a quarterly admissions path by return type with a band, and a bridge from the pre-cap path to the new one.

Where the weight sits
Synthesis. Three partial models (time to return, the risk of people the cap diverts, and future releases) each carry their own uncertainty and have to be combined into one path that holds together.

The investigation
The solver has to

link each return to the release it follows, including people released more than once;
estimate time to return by cause from every cohort's partial follow-up, turning cause-specific hazards into cumulative incidence rather than treating the other return type as censoring;
estimate new-conviction risk for the people who used to return on technical violations, from their risk profiles;
combine those with projected releases into a quarterly path with a band, back-tested on held-out cohorts; and
bridge the projected change against the pre-cap path into fewer technical returns, added new-conviction returns and release volume.
Where it shows up in real data
Iowa Department of Corrections recidivism files on the state open data portal (release cohort, days to return, return type, over a three-year follow-up); National Corrections Reporting Program term records through ICPSR, where recent release cohorts are still in follow-up; state corrections monthly admission reports; New York's Less Is More Act and other caps on technical returns.

Scenario
A sentencing commission must project quarterly admissions from post-release returns for the next three years under a new cap on technical-violation returns, to decide how many beds to keep open.

Where a hurried analyst goes wrong
Using three-year rates from the latest complete cohorts and throwing away recent cohorts still in follow-up. Setting technical returns to zero and assuming the people the cap keeps out add nothing to new-conviction returns. Counting a person released twice as two independent people. Adding the three models' bands as if they were independent of one another, or reporting no band at all.

What the solver delivers
The linked release-return file, cumulative incidence by cause, the diverted group's estimated risk, the quarterly path by return type with a band and its back-test, and the bridge from the pre-cap path. Real cohorts pin the base rates and back-test, the cap's terms pin which returns stop, and the bridge has to add to the projected change.

Keeping it deterministic
Build the base rates from real release cohorts. The path is pinned when every model with cause-specific hazards and a defensible risk assumption for the diverted group lands each quarter in one band, clearly above the zero-out answer. The prompt states the cap and the horizon. It does not mention competing risks, censoring or cohort maturity.

Shallow versions of these ideas
Each design below keeps one strategy's setting. Some plant or hide one thing that flips the answer; others are honest analysis, even when narrow. Decide which you would send back before you open the reasoning.

Read each task design. Send back the ones decided by a planted defect, a shallow hidden factor or a field reading, and approve the ones built on honest analysis of the real data.

These are task designs, not prompts. Ask what decides the result, and whether telling the solver one fact would make the rest routine.

1. Voter roll removals. The author deletes 3,000 records from one county in one week of a synthetic voter file, and the task is to name the county with an unusual purge.
Strategy 5

Verdict and reasoning
Send back. One planted block in the deciding unit decides it, and one plot of weekly removals by county finds it. That is a planted defect.

Revised design
Use real weekly snapshots across two election cycles and ask for the rule itself, its expected alerts and a reading of every flag. The solver has to rebuild removals from snapshot pairs, model the federal calendar and batch habits, size the variance and calibrate to an alert budget, and each of those is credited.

2. Poverty spells. The spell file carries a column named censored, and the task turns on whether the solver drops the flagged rows before averaging spell length.
Strategy 7

Verdict and reasoning
Send back. This is a field reading. One sentence ("keep the censored rows and use a survival estimate") makes the rest routine.

Revised design
Rebuild spells from the survey's monthly calendars as published. Ask for entry-view and point-in-time cuts and a family-type comparison, so the solver has to define spells, handle censoring, diagnose seams and reconcile the two views, each a separate result.

3. Ranking countries on a depression scale. Real item responses from 25 countries in one survey round. Raw sums and comparable-item scores disagree at fifth place, and apart from testing which items work the same way in every language the task is a weighted mean and a sort.
Psychology & Behavioral Science

Verdict and reasoning
Approve. Nothing is planted, and testing which items work the same way in every language is legitimate measurement work, not a hidden fact. Asking for change between two rounds and intervals as well would give careful work more to earn.

4. Crime reporting breaks. The author halves one agency's count in one year of a constructed file, and a months-reported column shows six months for that year.
Strategy 9

Verdict and reasoning
Send back. One planted subgroup carries its own label, so a single filter fixes it. That is a shallow hidden factor.

Revised design
Use real agency files across the change of reporting system, where breaks of several kinds occur. The solver estimates the counting-rule shift, sets a threshold to a false-alarm rate, traces each flag to its cause and bridges the corrected trend to the published one.

5. Placing legislators on one scale. One session of real roll calls; the answer is the 12 majority members closest to the minority party, and it comes out right only if the solver fits an ideal-point model instead of counting party-unity votes.
Political Science & Public Policy

Verdict and reasoning
Approve. The roll calls are real and nothing is planted; fitting an ideal-point model is a legitimate method choice. Spanning several sessions and asking for intervals would make the task richer.

6. Withheld cells. Real county by industry employment files with their nondisclosed cells and two industry-code revisions. The solver builds a panel that ties to every published total, reports its fill error on masked cells, and gives a cluster's growth with a band and its sources by county.
Strategy 3

Verdict and reasoning
Approve. Nothing is planted. Bounding cells, bridging codes, tying two hierarchies, testing the fill and attributing growth are separate pieces of work, each checked against published totals or a recomputable error.

7. Returns to prison. Real release cohorts with days to return and return type. The solver projects quarterly admissions under a new cap on technical-violation returns, by return type with a band and a bridge from the pre-cap path.
Strategy 10

Verdict and reasoning
Approve. Linking releases, competing-risk estimation, completing immature cohorts, the risk of the people the cap diverts and the bridge are each credited, and no single hidden fact rescues the run.

Key lesson
A shallow version hangs the result on one hidden or planted thing: a planted block, a built-in factor or one reading. Once seen, the rest is routine. A legitimate method choice is fine even when it is the hardest step. The strongest versions spread the difficulty across several pieces of real work, each checkable, so more careful work keeps earning more.


Engineering and Physical Sciences
Each strategy below is an investigation, not a trick. Real engineered and physical systems (turbines, plants, grids, sensor networks, rivers, roads) leave behind telemetry and records that are messy in many places at once, so a careful solver has to get several connected things right, and each one can be checked. A quick pass gets some of them; only sustained, self-checking work gets all of them. Each strategy names where the weight of the work sits, the chain of sub-results, the public data where the difficulty already lives, a scenario, the places a hurried analyst goes wrong, what the solver delivers and how each piece is pinned. The weight sits somewhere different in every strategy, and no two share a chain: copy the lesson, never the structure. The eleven strategies span all nine analysis types, and none ends in a yes or no call.

What cannot decide the task
Rule application, a data-semantics reading, a planted defect or decoy, replay of a published figure, a shallow hidden factor, or an unpinned ambiguity cannot decide the task, alone or several side by side. A shallow hidden factor is something you built into the data that one sentence would give away ("the east-side sensors were recalibrated in May") and one routine adjustment then fixes, whether it sits only in the deciding units or shows up in a single cross-tab. The planted defect, rule application and the shallow hidden factor are one family: a single hidden or planted thing that, once caught, flips the whole answer. One-fact test: if telling the solver one fact makes the rest routine, redesign. A legitimate method choice is fine even when it is the hardest step. Strong tasks put real analytical work at more than one step, so careful work earns more. See Deep reasoning for the full standard.

Physical & Environmental Sciences
Monitoring data in this field come from many instruments that drift, move, get replaced and miss the events that matter most. These three put the weight on rule design, triage across a network and estimating a quantity no record measures directly.

1. Debugging a low-cost air sensor network
Analysis type and answer shape
Data Quality, Monitoring & Alerting; a fault register (sensor, fault type, onset week) plus a weekly pull rule with its expected alert count.

Where the weight sits
Design of a monitoring rule. The hard part is defining "this sensor has stopped tracking real air" so the definition survives humid weather, smoke and slow decay, and then proving its false-alarm rate.

The investigation
Put each sensor's few-minute readings, both of its laser channels and its own humidity reading on the same hourly clock as the reference monitors.
Build a correction for humidity and concentration from the sensors that sit beside a reference monitor, and test it on colocated sensors held out of the fit.
Model how large a healthy sensor's residual should be, given the level, the distance to the reference and what the corrected neighbors read, because error grows with concentration.
Separate network-wide episodes, where every sensor moves together, from departures by one sensor.
Classify each departing sensor (one channel dead or stuck, both channels drifting, a unit moved indoors or next to a local source) and date when its residual began to move.
Set the rule's threshold on held-out sensor-weeks and replay it to show when it would have caught each fault.
Where it shows up in real data
The PurpleAir archive (two laser channels per sensor, plus the sensor's own temperature and humidity), EPA AQS and AirNow reference PM2.5 monitors, published colocation evaluations by EPA and by the South Coast AQMD AQ-SPEC program, and OpenAQ.

Scenario
A county air district shows 180 sensors on a public map and ships a year of their readings, hourly data from six reference monitors and its weather stations. It wants to know which sensors went bad, how and since when, plus a weekly rule for pulling a sensor from the map and the number of pulls to expect in a normal week.

Where a hurried analyst goes wrong
Flagging raw disagreement with the nearest monitor, so coastal and valley sensors fire in clusters on foggy days. Trusting channel agreement, which misses a sensor drifting on both channels. Pulling dozens of sensors during a smoke week that moved the whole network. Tuning the threshold on the same weeks it is scored on, so the quoted false-pull rate is optimistic. Dating a fault at its first alarm rather than at the start of the drift.

What the solver delivers
The register of failed sensors with fault class and onset week, the rule, its expected pulls per normal week with the false-pull rate, and a replay table showing how many weeks after onset the rule caught each fault. Real faults in a well-chosen year sit far from healthy sensors, so the register is pinned; onset weeks are graded within a band.

Keeping it deterministic
The prompt fixes the tolerable false-pull rate (for example two a month across the network) and defines failure by its consequence, not by a method. Choose a year in which the real faults stand clear of the healthy sensors, and grade onset within a few weeks. Do not ship a correction equation, and keep humidity, channels, drift and smoke out of the prompt.

2. Finding the breaks in a station network before trusting its trend
Analysis type and answer shape
Anomaly Detection & Diagnostics; a dated break register across a network, plus adjusted trends with bands.

Where the weight sits
Triage at breadth. Forty stations give hundreds of station-to-neighbor difference series, most candidate breaks are noise or belong to a neighbor, and the solver has to work through them all to know which station each real break belongs to.

The investigation
Build monthly minimum-temperature series from the daily files, honoring quality flags and gaps.
Choose each station's neighbors by how closely their month-to-month changes move together, not by distance alone.
Test every difference series for breaks with a method that respects seasonality and autocorrelation.
Attribute each break to the station implicated by most of the pairs that include it, and not by the pairs among its neighbors.
Estimate each break's size and adjust the daily minimums so the warm tail moves correctly, not only the mean.
Check the work: after adjustment, the difference series should be flat, and every break should be supported by more than one neighbor.
Where it shows up in real data
NOAA GHCN-Daily and USHCN station records; the switch from liquid-in-glass thermometers to electronic sensors at cooperative stations in the 1980s; automated station commissioning at airports in the 1990s; changes in observation time at cooperative stations; rooftop-to-ground and city-to-airport moves.

Scenario
A state climatologist supports heat-health plans for eight cities and has 40 cooperative and airport stations with up to 70 years of daily data. The office wants every break larger than 0.5°C in each station's daily minimum, dated to the year, and the adjusted trend in nights above 75°F for each of the eight cities, with a band.

Where a hurried analyst goes wrong
Testing each station on its own, which flags real climate swings and misses smaller instrument breaks. Adjusting only where a move is documented. Letting one bad neighbor create matching breaks at every station around it. Shifting the mean but leaving the tail, so the warm-night count barely changes. Treating yearly counts as independent, so the trend band is too narrow.

What the solver delivers
The break register (station, year, size), the eight adjusted warm-night trends with bands, and the flatness check on the adjusted differences. Breaks are pinned by agreement across several neighbors; trends are graded against bands that cover reasonable adjustment methods.

Keeping it deterministic
Pin the break size that matters and accept dates within a year. Choose a network whose larger breaks stand out against several neighbors. Do not ship NOAA's adjusted series or the station history notes (that turns the task into replay), and keep instruments, neighbors and homogenization out of the prompt.

3. A design flood from a short record, several neighbors and a reservoir upstream
Analysis type and answer shape
Forecasting & Predictive Modeling; a design flow with an interval, the span class it implies and a sensitivity table that says which judgments could change the class.

Where the weight sits
Estimation of a hard-to-measure quantity. A 1-percent annual chance flood is a far-tail number that no record contains. The site's own record is short and partly regulated, each neighbor carries only part of the information, the skew is uncertain and the regional equations have their own error, so the work is building several weak estimates, testing each one and combining them with their uncertainties. No one of them decides the number.

The investigation
Screen the peak files at the site and at every candidate neighbor: qualification codes, potentially influential low floods, and historic peaks recorded outside the systematic record, with the flow thresholds they imply for the unrecorded years.
Decide which years describe the river as it runs today from several lines of evidence: when storage upstream came online, how peaks changed against daily flood volumes, whether unregulated neighbors shifted over the same years (a wet or dry run of decades moves them too), and whether the largest floods still pass largely unattenuated once the reservoir fills.
Extend the record from several neighbors rather than one: keep the gauges whose concurrent peaks add independent information, use an extension that preserves the variance of the site's peaks, test it on overlap years withheld from the fit, and report the effective record length gained, which is shorter than the years added.
Check that the site sits inside the area and period of the regional skew study, and weight the station and regional skews by their mean square errors.
Fit, and compute the design flow with an interval that carries the record length, the extension, the historic information and the skew.
Build an independent estimate from the regional regression equations, check whether the basin falls inside their range and whether they apply to a regulated basin at all, and use it as a weighted estimate or only as a check, as that answer allows.
Tabulate how each judgment (years kept, neighbors used, skew weight, historic thresholds, regression weight) moves the design flow, and whether any reasonable combination crosses a span class boundary.
Where it shows up in real data
USGS peak-flow files (with qualification codes for regulation or diversion and for historic peaks) and daily values, the National Inventory of Dams for the years upstream storage came online, USGS regional skew and regional regression reports, and long-record gauges on neighboring rivers, some regulated and some not.

Scenario
A county engineer is sizing a replacement bridge at a gauge with 48 years of annual peaks and a flood-control reservoir upstream that began operating partway through. The folder holds the site's peaks and daily flows, eight neighboring gauges with records of different lengths (some below dams of their own), the dam inventory records and the two regional reports. The engineer wants the design flow with a 90 percent interval, the span class it implies, how much each judgment moved the number and whether any of them could change the class.

Where a hurried analyst goes wrong
Fitting all 48 years as one population, or keeping only the later years and trusting their short-record skew. Reading a wet run of decades that every gauge shares as the reservoir's effect, or the reverse. Extending from the nearest gauge alone, or from several that move together, so the record looks longer than the information in it. Dropping the historic peaks, or letting a few very low years bend the upper tail. Taking the regression estimate at face value for a regulated basin or one outside the equations' range. Quoting an interval that ignores the skew and the extension. Producing a sensitivity table that never says whether the span class could change.

What the solver delivers
The years used and the evidence behind that choice, the neighbors used with the extension's holdout error and effective record length, the weighted skew, the design flow and interval, the regional estimate and how it was used, the span class and the sensitivity table. Each sub-result is graded against a band and carries its own share of the credit; the span class is pinned because reasonable choices land in the same one.

Keeping it deterministic
Choose a site where the record decision, the extension, the skew and the regional estimate each move the number by a real but modest amount, so no one of them decides the result. Use span classes wide enough that reasonable analyses agree, and confirm that every reasonable combination of those choices lands in the same class. The prompt states the design standard (the 1-percent annual chance flood for the river as it runs today). It must not ship a step-by-step guideline (Bulletin 17C included), say which years to keep, name a neighbor gauge, or mention skew, low floods or historic peaks.

Energy Systems & Utilities
Energy data come from turbines, meters, monitors and filings that count different things on different clocks. These six range from root cause in plant and fleet telemetry to forecasts whose bands hold up, conformed filings, scorecards and a sizing decision.

4. Bridging expected to actual energy at a wind farm
Analysis type and answer shape
Root-Cause Analysis; a bridge between two totals with a band on every bar, plus the turbines behind the underperformance bar.

Where the weight sits
Attribution. Losses overlap in time (a curtailed hour can also be a low-wind hour on a slipping turbine), so most of the work is making every lost MWh land in exactly one bar and showing the bars add up.

The investigation
Reconcile the sum of the turbines' 10-minute output to the revenue meter month by month, and screen stuck or frozen sensor channels.
Correct the period's wind to the long term through its relationship with two decades of reanalysis, with the uncertainty from the choice of reanalysis and period.
Classify every lost interval as fault, maintenance, curtailment or grid outage, using the status logs and what the neighboring turbines produced at the same moment, and estimate the energy lost in each.
Build each turbine's power curve from a clean early period with an air-density correction, then compare its later curve within wind-direction sectors so wakes are not read as decline.
Date the onset for each turbine that slipped.
Assemble the bars in the stated order and show that turbine-level losses add up to each bar.
Where it shows up in real data
Open operational data from real farms (the Kelmarsh and Penmanshiel SCADA and status-log datasets published on Zenodo, and Engie's La Haute Borne open data), ERA5 and MERRA-2 reanalysis, NREL's OpenOA library and its documentation, EIA-923 monthly generation and the US Wind Turbine Database for US plants, and grid-operator curtailment reports.

Scenario
Lenders to a 14-turbine farm see two years of output well below the P50 estimate. They want a bridge in GWh from P50 to metered output (wind resource, availability, curtailment, power-curve underperformance, electrical losses and unexplained), each with a band, plus the turbines behind the power-curve bar in order, with when each began to slip.

Where a hurried analyst goes wrong
Comparing the nacelle wind speed with the estimate's assumption, when the nacelle anemometer sits behind the rotor and reads differently on each turbine. Taking the fault log at face value, so curtailment is booked as downtime. Fitting one fleet curve, which hides which machines slipped. Counting a curtailed hour again as low wind. Ignoring the gap between turbine output and the meter.

What the solver delivers
The bridge with a band on each bar, the ranked turbines with lost MWh and onset month, and a short statement of which bars are firm and which are soft. The two totals are fixed and the bridge must sum; the turbine list is pinned by a period where the leading turbines separate clearly.

Keeping it deterministic
The prompt lists the bars in the lenders' order, which fixes how overlapping losses are assigned. Grade each bar against a band. If you write the P50 estimate yourself, base it on the long-term record, not on a number chosen to create a gap. The prompt must not mention reanalysis, density, nacelle readings or wakes, or name a turbine.

5. Diagnosing underperformance across a solar fleet
Analysis type and answer shape
Anomaly Detection & Diagnostics; a ranked flagged set with a dated cause for each system, plus a fleet loss bridge by cause.

Where the weight sits
Investigation. Every underperforming system is a small root-cause case: weather, snow, shade, clipping, soiling, slow decline and real faults all lower output, and the solver has to rule causes in and out system by system before anything is ranked.

The investigation
Model what each system should have produced in every interval from satellite irradiance, temperature and its own specification, calibrated on an early clean period.
Set aside the losses that are not faults: inverter clipping on clear days, snow cover after storms, seasonal shading with its time-of-day signature, and data gaps that look like zero output.
Estimate each system's soiling and long-run decline rates with bands from year-on-year comparisons.
Find step changes (a string or inverter going down) and date them.
Assign each system's shortfall to its causes and roll the causes up into a fleet bridge from expected to actual.
Rank systems by the energy a technician visit could recover, and check the ranking against last year's visit outcomes.
Where it shows up in real data
NREL PVDAQ public systems, NSRDB irradiance and NASA POWER weather, NREL PVWatts and the pvlib library, and the NREL RdTools documentation on soiling and degradation patterns.

Scenario
An owner of about 150 commercial rooftop systems ships two years of interval output, system specifications, site coordinates and last year's service log. It can afford 25 technician visits next quarter and wants them ranked, with the cause it expects at each site, plus a fleet-wide account of where the missing energy went.

Where a hurried analyst goes wrong
Comparing output with the design estimate instead of with the weather that actually occurred. Booking clipping, snow and communication gaps as faults. Reading one bad month as a lasting failure. Ranking by percentage shortfall, so small systems with a cloudy month crowd out large ones with a dead inverter. Never checking the method against last year's visits.

What the solver delivers
The ranked 25 with cause and onset date, the fleet bridge by cause with bands, and the hit rate the ranking would have scored on last year's visits. The flagged set is pinned by faults that are clear in the real data; bridge bars are graded against bands.

Keeping it deterministic
Pin the visit cap and the objective (recoverable energy). If you add a service log, its outcomes must follow from faults visible in the real output, not be chosen to steer the ranking. Pick systems where the top of the list separates from the rest under any reasonable expected-output model. The prompt must not mention irradiance, clipping, snow, shading or soiling.

6. A ten-year peak load forecast whose bands hold up
Analysis type and answer shape
Forecasting & Predictive Modeling; a path of annual peaks at P50 and P90, with the drivers of the change and a backtest of the bands.

Where the weight sits
Validation. Anyone can draw a path; the hard part is proving that its bands would have covered past peaks at the stated rate, which forces honest treatment of weather and structural change.

The investigation
Screen hourly load by zone for spikes, gaps, duplicated daylight-saving hours and boundary changes, and reconcile it to annual energy totals.
Model hourly load against temperature and humidity, including the build-up of heat over several days, by hour and day type.
Find and size the structural shifts in the record, such as behind-the-meter solar moving the net peak later in the day, large new loads and the 2020 change in daily patterns.
Run 30 or more historical weather years through the current-system model to get the weather-driven spread of the annual peak.
Project the drivers forward with their own uncertainty.
Rebuild the forecast as it would have been made in earlier years and count how often actual peaks fell inside the bands.
Split the change from today's P50 to year ten into its drivers so the parts sum to the total.
Where it shows up in real data
ERCOT hourly load archives by weather zone, the EIA-930 Hourly Electric Grid Monitor, NOAA Integrated Surface Database and GHCN-Daily weather, EIA-861 and EIA-861M small-scale solar estimates, and published long-term load forecasts from ERCOT and PJM as outside benchmarks.

Scenario
A cooperative's resource planner must file a ten-year peak forecast. The folder holds 15 years of hourly load by zone, weather at 25 stations, monthly customer counts and rooftop solar capacity by county. The filing needs P50 and P90 peaks for each year, the drivers of the change and evidence that the bands are honest.

Where a hurried analyst goes wrong
Fitting a trend line through annual peaks. Normalizing to one average weather year, so P90 is guessed rather than simulated. Missing that the peak hour has moved. Taking bands from regression residuals alone, which ignores weather-year and driver uncertainty and comes out far too narrow. Skipping the backtest.

What the solver delivers
The screened series with a note of what was excluded, the weather-normalized peak for the latest year with a band, the P50 and P90 path, the driver split that sums to the change and the backtest coverage. Each is graded against a band; coverage is pinned by the history.

Keeping it deterministic
The prompt defines the outputs (the system's highest hourly load each year, P90 as a peak exceeded one year in ten) and the horizon. Choose a system where the driver contributions separate clearly. The prompt must not mention solar shifting the peak, weather years, normalization or backtesting.

7. One emissions table from agencies that count different things
Analysis type and answer shape
Data Extraction & Conformation (ETL / Pipeline Build); a conformed generator table, a reconciliation bridge and an exclusion list.

Where the weight sits
Assembly. Building one trustworthy dataset from several agencies' files is most of the work; the arithmetic at the end is easy once every link is right.

The investigation
Work out which schedules and tables hold generation, fuel, heat input and emissions, and at what level each is reported.
Resolve every unit-to-generator link, including one boiler feeding several generators and combustion-turbine-plus-steam blocks.
Apportion monitored emissions by heat input where links are shared.
Fill units that report to EPA only in the ozone season, or not at all, from EIA fuel use and emission factors.
Reconcile each plant to both agencies' totals and explain every residual.
Sanity-check each generator's rate against what its fuel and technology physically allow.
Where it shows up in real data
EIA-860 and EIA-923, EPA Clean Air Markets Program Data, the EPA-EIA Power Sector Data Crosswalk, and the open Public Utility Data Liberation project, whose issue tracker documents how hard these joins are. EPA's eGRID publishes plant-level results that work as a private check.

Scenario
A state energy office building a marginal-emissions tool needs, for one year, every fossil generator in the state with net generation, CO2 and CO2 per MWh; plant totals that reconcile to EIA generation and EPA CO2 within stated tolerances; and a list of generators it cannot use, with the reason.

Where a hurried analyst goes wrong
Joining on plant id and giving every generator the plant rate. Dropping whatever fails to match. Leaving steam turbines in combined-cycle blocks at zero because they have no stack. Undercounting ozone-season reporters. Losing units too small for EPA monitoring. Never reconciling, so none of these shows.

What the solver delivers
The conformed table, the bridge from each agency's state total to the table's total, and the exclusion list with reasons. Totals are pinned by the agencies' published figures; generator rates are graded wherever the link is single and defensible.

Keeping it deterministic
Grade combined-cycle results at the block level, since the split inside a block is a convention. State the business definition in the prompt (all of a plant's emissions count against its electricity). Do not ship eGRID, and do not mention the crosswalk, seasonal reporting or how combined-cycle blocks are built.

8. Grading plant efficiency after accounting for how each plant was run
Analysis type and answer shape
Comparative & Explanation; a scorecard against thresholds, with the evidence behind each red grade.

Where the weight sits
Modeling. Each block needs its own fuel curve with the right terms, and the comparison is only fair once every curve is evaluated under the same operating pattern with its uncertainty.

The investigation
Build each block's net output from hourly gross load and monthly net generation.
Separate start-up and shutdown hours and estimate start fuel on its own.
Find where supplementary firing begins at the top of the load range.
Fit each block's fuel curve with an ambient-temperature term and check the residuals for missing structure.
Evaluate every curve under one common pattern, with an interval.
Explain each red grade by the shape of its curve (high fuel at minimum load, or high fuel per extra MW), and check whether the block's efficiency shifted during the year, for example after an outage.
Where it shows up in real data
EPA Clean Air Markets hourly unit data (heat input and gross load every hour for units above 25 MW), EIA-923 net generation and fuel, EIA-860 vintages and equipment such as duct burners, and NOAA Integrated Surface Database temperatures near each plant.

Scenario
Commission staff reviewing fuel-cost recovery want a scorecard of the state's 24 combined-cycle blocks: each block's fuel per net MWh if all of them had run the same way last year, graded green, amber or red against two thresholds staff set, with one line per red block on what makes it inefficient.

Where a hurried analyst goes wrong
Ranking by annual heat input over net generation, so cycling blocks look worst whatever their equipment. Leaving start hours in the curve fit. Fitting through the duct-firing region as if it were the same machine. Ignoring that hot weather alone raises fuel per MWh at every block. Explaining a red grade with a guess rather than the fitted curve.

What the solver delivers
The 24-row scorecard with intervals, each red block's explanation from its curve, and any mid-year shifts found. Grades are pinned because thresholds sit where no block's interval straddles a line.

Keeping it deterministic
Set the staff thresholds where no interval straddles a line, and pin net output in the prompt so the task never turns on reading a load column. The prompt states the comparison staff want (as if every block had run the same way) because that is the business question; it must not mention part load, starts, ambient temperature or duct firing.

9. Sizing a battery when the month's peak is not known in advance
Analysis type and answer shape
Opportunity Sizing & Decision Support; scenario table, a chosen size and the flip point.

Where the weight sits
Optimization under constraints and uncertainty. The value of each size depends on a dispatch policy that has to work with only what is known at the time, so the solver designs, tests and stresses the policy before any size is chosen.

The investigation
Clean the interval meter data (gaps, spikes, meter swaps) and rebuild each month's billing demand exactly as the tariff defines it.
Find what drives the monthly peaks (weather, schedules, one-off events) and how predictable each driver is.
Build a day-ahead peak forecast and measure its error out of sample.
Design a dispatch policy that uses only that forecast and the month so far, tune it on some months and test it on others.
Simulate every vendor size across both metered years and a range of forecast errors, with round-trip losses and capacity fade.
Compute each size's net present value under three tariff scenarios, choose a size and find the demand-charge rate below which no size pays.
Report how far the realistic savings sit below the savings with perfect foresight, as a check that nothing leaked.
Where it shows up in real data
Building Data Genome Project 2 (hourly meter data for about 1,600 nonresidential buildings, raw and cleaned), the Utility Rate Database on OpenEI for real demand-charge tariffs, NREL's Annual Technology Baseline for battery costs, and the weather files that ship with the meter data.

Scenario
A school district's facilities office will buy one battery for its largest building from a vendor menu of six sizes. It wants the net value of every size under three demand-charge scenarios, the size with the best value under today's tariff, and the demand-charge rate below which no size pays.

Where a hurried analyst goes wrong
Optimizing dispatch over the historical year with every month's load known ahead. Letting a meter spike set a month's billing demand. Using one year where two exist. Leaving out capacity fade. Reporting one savings figure with no spread.

What the solver delivers
The scenario table with a band on each net value, the chosen size, the flip point and the gap to perfect foresight. The size is pinned when the realistic optimum sits at least one menu step from its neighbors under reasonable policies; values are graded against bands.

Keeping it deterministic
Pin the tariff (including how billing demand is measured), the horizon, the discount rate, the vendor menu and the costs. Check that two reasonable real-time policies choose the same size. The prompt must not mention forecasting, hindsight or back-testing.

Human Factors & Ergonomics
People are the instrument here: they tire, choose their own pace and get counted only when something goes wrong. One of these puts the weight on measurement, the other on reconciling several partial estimates into one credible effect.

10. Injury risk per hour worked across a shift
Analysis type and answer shape
Descriptive & Distribution Analysis; a risk curve by hour on shift with bands, and a break schedule that fits the relief capacity.

Where the weight sits
Measurement. The numerator has holes, the denominator does not exist in any file, and the two time scales that matter are tangled together; the schedule at the end is easy once the curve is right.

The investigation
Compute hours into the shift from start and event times, including shifts that cross midnight, and check the times for rounding to the hour.
Study which cases lack times (by industry, establishment size and event type) and correct for that rather than dropping them.
Build the number of workers still on shift at each hour from the distribution of shift lengths and overtime.
Fit a model with both hours on shift and clock time, which can be told apart because start times differ, and allow for extra variation between establishments.
Put a band on each hour's rate.
Place breaks against the capacity limit and check whether the schedule changes under a different reasonable exposure assumption.
Where it shows up in real data
OSHA Injury Tracking Application case detail data for cases from 2023 onward (from Form 301, each case can carry the time the employee began work and the time of the event, though some cases leave them blank), BLS Survey of Occupational Injuries and Illnesses case-and-demographic tables, FRA accident reports with crew hours on duty, and the American Time Use Survey for shift lengths and start times.

Scenario
A warehouse operator with three shift start times can fund relief staff to cover two 20-minute breaks per shift, but only a few crews can be on break at once. It wants the risk per hour worked across the shift, with bands, and break times for each shift pattern that cover the hours of highest risk.

Where a hurried analyst goes wrong
Tallying injuries by hours since start and putting breaks at the early peak, which mostly reflects that everyone is still at work then. Dividing by headcount instead of by the people still working. Dropping cases with missing times. Leaving clock time out, which loads night-time risk onto late shift hours.

What the solver delivers
The risk curve with bands, the effect of clock time stated separately, the break schedule and the sensitivity check. The high-risk windows are pinned to within half an hour by enough real case records; the curve is graded against bands.

Keeping it deterministic
Pin the shift patterns, the relief capacity, the break length and the objective. If you add the operator's own roster, draw its shift lengths from a public source rather than tuning them to move the windows, and check that two reasonable hazard models choose the same slots. The prompt must not mention exposure, denominators, missing times or clock time.

11. The safety effect of a signal display change at sites picked after bad years
Analysis type and answer shape
Experiment & Causal Analysis; a grid of four effects with bands, plus the checks behind them.

Where the weight sits
Synthesis. The solver produces several partial estimates (a model-based estimate, a comparison-group estimate, a placebo and a spillover check) and has to reconcile them into one grid it can defend.

The investigation
Attach geocoded crashes to intersections and harmonize crash-type codes across the years the state revised its crash form.
Fit a crash model to untreated intersections with volume and lane terms and estimate the extra-Poisson variation.
Use it to predict each treated site's expected after-period crashes from its own history and its traffic, calibrated year by year so swings such as the 2020 traffic drop are absorbed, and estimate each cell's effect with its variance.
Repeat with a matched comparison group and compare.
Run the same estimate on crash types the display should not affect, as a placebo.
Check whether left-turn crashes moved to neighboring intersections.
Reconcile: where estimates disagree, say which one the evidence supports and why.
Where it shows up in real data
State and city open crash data with crash type and location (for example Iowa DOT's crash data, Chicago's traffic crash records and New York City's motor vehicle collision files), state traffic count programs for volumes, city signal inventories with change dates, and the FHWA Crash Modification Factors Clearinghouse as a sanity check only.

Scenario
A city traffic engineer converted 60 intersections from permissive green-ball left turns to flashing yellow arrows over three years. For the council's next list, the engineer wants the change in left-turn crashes in each of four cells (one or two opposing lanes, by opposing volume above or below 12,000 vehicles a day), each with a band.

Where a hurried analyst goes wrong
A raw before-and-after at treated sites, which credits the change with a drop that would have come anyway. Scaling by a citywide trend, which keeps the same selection effect. Poisson intervals that treat crash counts as steadier than they are. Mixing crash codes across a form revision. Never running a placebo, so a citywide change is read as an effect.

What the solver delivers
The four-cell grid with bands, the comparison-group results beside it, the placebo and spillover results, and a short reconciliation. Cells are pinned when the model-based and comparison-group estimates fall in the same band.

Keeping it deterministic
The selection must be real and program-wide: check that before-period counts run high across the treated sites, not at a handful. Pin the cells, the crash definition (by crash-type codes) and the study period. The prompt must not mention selection, regression to the mean, comparison sites or placebos.

Shallow versions of these ideas
Each idea above has a shallow twin that looks similar and gets sent back. Some hide one planted thing that flips the answer; others are honest analysis, even when narrow. Decide which designs you would send back before you open the reasoning.

Read each task design. Send back the ones where a planted thing, a documented procedure or a field reading flips the whole answer, and approve the ones built on honest analysis of the real data.

These are task designs, not prompts. Ask whether telling the solver one fact would make the rest routine.

1. Signal display change. The author adds extra left-turn crashes at five treated intersections in the year before the change, only there, and the estimated effect turns on spotting them.
Strategy 11

Verdict and reasoning
Send back. The factor is constructed and sits only in the deciding units. One plot of before-year counts shows it, and one filter on that year fixes the answer. This is a shallow hidden factor.

Revised design
Use real crash records where selection after high-crash years runs across the whole program. The solver fits a crash model to untreated intersections, applies it site by site with yearly calibration, cross-checks with a comparison group and a placebo, and checks for spillover, so telling the solver about the selection still leaves most of the work.

2. Battery sizing. Real meter data, a real tariff and a vendor menu. The task asks only for the best size, and every run that dispatches without knowing the month's peak ahead lands on it, while every run that dispatches with hindsight picks a size too large.
Strategy 9

Verdict and reasoning
Approve. Nothing is planted, and dispatching without hindsight is a legitimate method choice, not a hidden fact. Asking for the scenario table, the flip point and the gap to perfect foresight as well would give careful work more to earn.

3. Design flood. The folder ships a design memo that says to drop the peaks before the reservoir opened, extend the record from a named neighbor gauge and weight the regional skew at one half.
Strategy 3

Verdict and reasoning
Send back. The deciding steps are written out for the solver, so following the memo gives the design flow with no judgment. This is rule application.

Revised design
Ship the peaks, daily flows, neighbor gauges and regional reports, and state only the design standard. The solver decides which years describe today's river from several lines of evidence, screens the record, extends it from several tested neighbors, weights the skews, builds and weighs an independent regional estimate and reports which choices could change the span class.

4. Station trend. One downtown station, one deliverable: the warm-night trend. Runs that compare the station with its neighbors find one large break and get the trend right; runs that do not, miss it.
Strategy 2

Verdict and reasoning
Approve. The break is real and nothing is planted; comparing a station with its neighbors is standard homogenization work. Widening it to a network of stations would make the task richer.

5. Plant efficiency scorecard. Four blocks turn red or amber depending on whether a column labeled load is read as gross or net output.
Strategy 8

Verdict and reasoning
Send back. One sentence of clarification makes the task routine. This is a data-semantics stump, and if both readings are defensible it is not deterministic either.

Revised design
Pin net output in the prompt and move the work to modeling: build net output per block, separate start fuel, find the duct-firing region, fit each curve with an ambient term and grade every block under one common operating pattern.

6. Wind farm bridge. The author scales one turbine's power column down 8 percent from a chosen date, and the power-curve bar of the bridge turns on finding that turbine.
Strategy 4

Verdict and reasoning
Send back. A planted change in one deciding unit, revealed by a single plot of output by turbine. "Check turbine 9 after June" rescues every run.

Revised design
Use real operational SCADA as published. The solver reconciles turbine output to the meter, corrects the resource to the long term, separates curtailment from faults by neighbor comparison, compares every turbine's curve with its own earlier curve within direction sectors and makes the bars sum.

7. Sensor network. Real low-cost sensor and reference monitor data for a full year. The solver delivers a register of failed sensors with fault type and onset week, a weekly pull rule that meets a stated false-pull rate on held-out sensor-weeks, and a replay of when the rule would have caught each fault.
Strategy 1

Verdict and reasoning
Approve. Nothing is planted. The correction, the expected-error model, the separation of network-wide episodes, the fault classes and the held-out threshold are each hard and each checked, so no single step carries the result.

8. Solar fleet. Two years of real interval output from about 150 systems. The solver ranks 25 visits with a dated cause at each site, builds a fleet bridge from expected to actual by cause and scores the ranking against last year's visit outcomes.
Strategy 5

Verdict and reasoning
Approve. The expected-output model, the non-fault losses, the decline rates, the dated step changes and the bridge each carry credit, and a run that only gets the top site right still loses most of it.

Key lesson
A shallow version hides one thing that a sentence would reveal. A version that turns on one legitimate method choice is honest and fine, even when that choice is the hardest step. The strongest versions spread several hard, checkable sub-results across the analysis, so more careful work earns more and no one hint rescues the run.


Other
Each strategy below is an investigation, not a trick: connected pieces of real analytical work that public survey, city and school data demand, each ending in a result you can check. A quick pass gets some pieces right; only sustained, self-checking work gets all of them. The strategies also differ in where the weight sits: one is mostly assembly, another mostly measurement, another a search across hundreds of units, so read the Where the weight sits line before borrowing a pattern. Find the difficulty in the sources named, not in something you build. If you assemble or extend data, it has to behave like the real thing throughout, with many genuine patterns and noise, never one effect added for the solver to find. The eleven strategies span all nine analysis types: three are root-cause or diagnostic work, two are forecasts, one is causal, and none ends in a yes or no call. Use them as patterns, not as tasks to copy.

What fails a task
Some steps can never carry a task: rule application (a document that spells out the decisive steps), reading one field or clause a particular way, a planted defect or decoy, replaying a published number, an ambiguity two experts could settle differently, and the shallow hidden factor (a confounder, subgroup, event or break you built into the data that one sentence would give away and one routine adjustment fixes). The planted defect, rule application and the shallow hidden factor are one family: a single hidden or planted thing that, once caught, flips the whole answer. One-fact test: if telling the solver one fact makes the rest routine, redesign. A legitimate method choice is fine even when it is the hardest step. Strong tasks have genuine work at more than one step and credit each sub-result separately. Messy data is required, but cleaning it never decides the answer; see Deep reasoning.

Survey Research & Official Statistics
Survey and official-statistics work is hard in more than one place at once: how the sample was drawn and re-drawn, who answered, who asked the questions, and how a series was built. The four strategies below put the weight on different parts of that production chain.

1. A state scorecard from overlapping survey years
Analysis type and answer shape
Comparative & Explanation; a scorecard against thresholds, with the evidence behind each row.

Where the weight sits
Measurement. Most of the effort goes into getting the uncertainty of a change right from a sample design the files only imply.

The investigation
The scorecard asks one question per state, but answering it takes six results.

A measured overlap share per state: how much of each state's sample appears in both years, worked out from the rotation design and the linked household identifiers.
Each year's published national estimate and standard error reproduced from the replicate weights, which proves the weighting before anything new is built on it.
The variance of the change with the covariance the overlap creates, from aligned replicates where the documentation supports differencing them and from the overlapping households where it does not.
A test of whether households that left the sample differ in insurance status from those that stayed, which settles that the target is the change for the whole population and not a paired comparison of stayers.
All 51 rows classified and each class counted.
The states whose class depends on the variance route or sits within a few tenths of the line, named.
Where it shows up in real data
The Current Population Survey's 4-8-4 rotation puts about half of one March's addresses in the next March's sample, and the Census Bureau publishes 160 replicate weights for each Annual Social and Economic Supplement since 2005. Its published supplement tables with margins of error are national; state uninsured tables have come from the American Community Survey since the 2013 data year. The National Crime Victimization Survey interviews the same addresses every six months for three years. The American Housing Survey follows a fixed panel of units between waves.

Scenario
A multistate health policy center publishes a fall scorecard: for each state and DC, the change in the adult uninsured rate between two years, classed as rose, fell or no detectable change at 90 percent confidence. The folder holds both years' supplement files with replicate weights, the survey's technical documentation and the published national tables.

Where a hurried analyst goes wrong
Treating the two years as independent samples, so the intervals for the change are too wide and states that genuinely moved are reported as unchanged. Switching to households interviewed twice because their change has a smaller variance, which answers a different question once leavers differ from stayers. Building standard errors without first reproducing the published ones, so a weighting slip goes unseen. Presenting a borderline state's class as firm.

What the solver delivers
The 51-row scorecard with each change and its interval, the count per class, the overlap share per state, the stayer and leaver comparison, and the short list of fragile states. The published tables pin step 2, the identifiers pin step 1, the confidence level in the prompt pins the classes, and the leaver comparison is a computed difference with its own interval.

Keeping it deterministic
The prompt fixes the two years, the population and the confidence level. Pick a year pair where the covariance moves several states across the line, and check that both variance routes agree on every state except the fragile ones the solver is expected to name. Credit each piece on its own, so the covariance alone never carries the score. The prompt must not mention the overlap, the rotation, covariance, matched households or attrition.

2. Interviewers whose fieldwork needs re-checking
Analysis type and answer shape
Anomaly Detection & Diagnostics; a ranked flagged set with the evidence for each flag, a false-alarm count and what the flags do to the headline estimates.

Where the weight sits
Triage at breadth. Two hundred interviewers, several weak signals each, and no single signal that settles anything.

The investigation
Start with the structure, not the outcomes:

rebuild the fieldwork map from interviewer, supervisor and cluster codes and find where interviewer and area can be told apart at all, such as teams that shared clusters or interviewers who moved between regions. Then
build several process signals per interviewer that do not depend on the headline outcome alone: age heaping, digit preference in child height and weight, birth years pushed just outside the under-five module, item nonresponse, and interview length where the files record it.
Fit each signal with area and interviewer effects, so that remote poor clusters stop looking like bad interviewing.
Combine the signals into one score and estimate its null distribution, for example by permuting interviewer labels within team.
Cut at 40 and report the expected number flagged by chance.
For each flagged interviewer, name the signals that drive the flag.
Show how far the national stunting and contraceptive-use estimates move when the flagged interviewers' cases are set aside.
Where it shows up in real data
The Demographic and Health Surveys recode files carry an interviewer code on every interview alongside the cluster number, recent rounds add a fieldworker file that links through interviewer and supervisor IDs, and age heaping, digit preference in child height and weight, and displacement of birth years out of the under-five module are documented across many rounds in the program's methodological reports. UNICEF's Multiple Indicator Cluster Surveys carry interviewer and supervisor numbers in the household file, and the European Social Survey publishes interviewer IDs in its contact-form data.

Scenario
A national statistics office has budget to re-interview a sample of households for 40 of its 220 interviewers before the final report. The director wants the 40 ranked by strength of evidence, what each flag rests on, how many would be flagged by chance alone, and whether the report's headline numbers are at risk.

Where a hurried analyst goes wrong
Z-scoring each interviewer's headline outcome against the regional mean, which flags interviewers posted to the poorest clusters for real poverty. Leaning on one signal, such as age heaping, which misses an interviewer who invents tidy, plausible answers. Ranking interviewers with 30 interviews alongside those with 300, so the small ones fill the list on noise. Stopping at the list without the chance count or the effect on the published estimates.

What the solver delivers
The ranked 40 with a score and per-signal evidence, the expected false flags with a band, the map of which interviewers are separable from their areas, and the shift in each headline estimate. Capacity fixes the list size; the permutation null fixes the chance count; the estimate shifts are recomputed from the data.

Keeping it deterministic
Check that the top of the list holds across reasonable model specifications and grade membership with a tolerance near the cutoff. Grade the false-flag count and the estimate shifts within bands. The prompt must not name any signal, the area confound, the model or the permutation.

3. Splitting a fixed fund from small-area estimates
Analysis type and answer shape
Opportunity Sizing & Decision Support; an allocation to a fixed total, with each share's range and the counties that move most.

Where the weight sits
Estimation of a hard-to-measure quantity, then allocation under constraints. The number being split is never observed well in most of the counties that receive money.

The investigation
The allocation is the last of five steps, and each earlier one changes it. It starts with assembly: direct estimates, margins and administrative covariates for every county, with their reference years aligned. Then the margins themselves turn out to be suspect: the published sampling variances for small counties are unreliable (zero estimates carry modelled margins), so they have to be smoothed, for example with a generalized variance function. Only then does an area-level model make sense, with covariates chosen by out-of-sample fit, residuals checked, and each county shrunk toward its prediction in proportion to its noise. The model estimates are cross-checked against the Census Bureau's own small-area series, and the counties where the two part ways are explained. The money comes last: benchmark to the state total, apply the floor, renormalize to the exact budget and bootstrap each share's range.

Where it shows up in real data
American Community Survey 5-year county estimates of uninsured adults with their margins of error (small counties include zero estimates, whose margins come from a separate model rather than the replicate weights); the Census Bureau's Small Area Health Insurance Estimates and Small Area Income and Poverty Estimates as a check; Medicaid enrollment by county from state agencies; county tax-return counts by income from IRS Statistics of Income.

Scenario
A state health insurance marketplace splits a $6 million navigator budget across 82 counties in proportion to uninsured working-age adults on low and moderate incomes, with a $25,000 floor per county. The board also wants to know which counties' amounts it can defend and which are close calls.

Where a hurried analyst goes wrong
Allocating straight from the direct estimates, so sampling noise decides small counties and counties with a zero estimate get only the floor. Taking published margins at face value. Applying the floor after benchmarking without renormalizing, so the table no longer sums to the budget. Choosing covariates by in-sample fit. Publishing amounts with no ranges, so the board cannot tell a firm share from a coin toss.

What the solver delivers
A county table that sums to exactly $6 million, each share with its range, the counties that gain or lose most against the direct allocation, and the counties where the model and the published small-area series disagree, with the reason. The budget, floor and target population pin the arithmetic; the published series gives an outside check.

Keeping it deterministic
Choose a state where model-based and direct allocations differ materially for many counties, grade each county within a stated tolerance, and confirm that the biggest movers hold across reasonable covariate sets and variance smoothers. The prompt must not mention shrinkage, borrowing strength, variance smoothing or which covariates to use.

4. An alert rule for a seasonal claims series
Analysis type and answer shape
Data Quality, Monitoring & Alerting; a monitoring rule with its expected alert count, the weeks it would have flagged and what each of those weeks turned out to be.

Where the weight sits
Designing the rule itself, then proving it out of sample. The deliverable is a specification that has to keep working next year, not a finding about last year.

The investigation
The first thing the series shows is that the same week last year is not the same week: holidays move. From there the work runs in six parts:

model week-of-year seasonality with moving-holiday terms and find each state's own patterns, such as summer retooling in auto states;
decide how 2020 and 2021 enter the history, as outliers, level shifts or a gap, and justify the choice by held-out error;
let the noise scale with the level and check the residuals;
set the threshold on held-out years so the false-alarm rate meets the tolerance, with a band on that rate;
backtest the last three years; and
match the flagged weeks against layoff notices, reporting the share of large notified layoffs the rule caught and an explanation for each flag that matches nothing.
Where it shows up in real data
The Department of Labor publishes weekly unemployment insurance initial claims by state, not seasonally adjusted, back several decades. Easter and Thanksgiving move between weeks, auto states show summer retooling spikes, and the 2020 surge distorted the seasonal pattern badly enough that the national claims series switched from multiplicative to additive seasonal factors in 2020, before a largely multiplicative approach returned from 2023. Several states also reported waves of fraudulent claims in 2020 and 2021. State WARN Act layoff notices, published by most state labor departments, give an independent record of real layoff events.

Scenario
A state labor department wants an email to go to the commissioner when a week's initial claims are unusually high for the time of year, so staff can check for a plant closure or a fraud wave. The commissioner accepts at most two false alerts a year and wants the rule written up so the data team can run it every Thursday.

Where a hurried analyst goes wrong
A same-week average plus two standard deviations fires on every holiday shift. With 2020 left in the history, the spread is so wide that real layoff waves pass silently. A threshold tuned on the fitting years understates the false alarms. A rule never checked against real events can meet the tolerance by almost never firing.

What the solver delivers
The rule as a runnable specification, expected false alerts per year with a band, the flagged weeks for the last three years, the catch rate against layoff notices, and a one-line account of every unmatched flag. The tolerance and evaluation window come from the prompt; the notices are an outside record.

Keeping it deterministic
Check that every baseline that passes the out-of-sample test flags the same weeks give or take one or two, and grade the flag list and the catch rate with that tolerance. The prompt must not mention holidays, 2020, the noise or how to use the layoff notices.

Urban & Regional Science
City data is hard because places affect each other, boundaries move, and the operational logs that record service were built to run the city, not to study it. One strategy here is mostly assembly, one is a debugging investigation through a request log, one is a forecast and one is a causal estimate with spillover.

5. Neighborhood data conformed across boundary changes
Analysis type and answer shape
Data Extraction & Conformation (ETL / Pipeline Build); a conformed table with reconciled totals and a short list of flagged tracts.

Where the weight sits
Assembly. Building one trustworthy table from relationship files, bracket counts and margins is most of the work; the flags at the end are quick once the table is right.

The investigation
Think of it as a build with a check at every stage. Block-level household weights come first, one for every intersection of an old tract and a new tract. The income bracket counts, not the medians, travel through those weights. Each median is then recomputed from the interpolated brackets, with a report of how close the method lands on the published medians for tracts whose boundaries never changed and a treatment for tracts whose published median is top-coded. The margins of error ride along through the reallocation and into each median. The reallocated counts have to add back to county totals in both periods. Only then come the flags: tracts whose inflation-adjusted rise clears the propagated uncertainty, with a note on any whose flag depends on weighting blocks by households or by people.

Where it shows up in real data
The Census Bureau's 2010 to 2020 tract and block relationship files; IPUMS NHGIS geographic crosswalks; the Longitudinal Tract Database (built on 2010 tract boundaries); ACS 5-year tables such as household income in 16 brackets, each with margins of error; the ACS handbook's guidance on derived margins, and the Census Bureau's Accuracy of the Data documentation on medians and their standard errors from a distribution. Published ACS tract medians are top-coded at $250,000.

Scenario
A city housing department must publish, for every 2020 tract in the city, median household income for two ACS 5-year periods a decade apart, inflation-adjusted, with the change and a flag where the rise is distinguishable from sampling error. The table feeds an anti-displacement map, and the data team needs the build documented so it can be rerun next year.

Where a hurried analyst goes wrong
Averaging old tracts' medians onto new tracts, which matches unchanged tracts exactly and so looks validated, although an average of medians is not a median. Weighting by land area, which sends households into parks and rail yards. Treating a top-coded median as a number. Dropping the margins, so the flags fire on noise. Never adding the counts back up to the county.

What the solver delivers
The conformed tract table in both periods, the median-method check on unchanged tracts, the county reconciliation, and the flagged tracts with the few whose flag is sensitive. County totals give a hard check on the reallocation, and unchanged tracts give a check on the median method (close to the published value, not exactly on it).

Keeping it deterministic
The prompt fixes the two periods, the 2020 boundaries, the dollar year and the confidence level for the flag. Grade the medians within a stated tolerance, the reconciliation exactly, and the flag list with its sensitive tracts named. The prompt must not mention crosswalks, brackets, relationship files or margins of error.

6. Why city service got slower, from the request log
Analysis type and answer shape
Root-Cause Analysis; a ranked set of causes whose shares add to the change, the month each began, and the size of the mix effect.

Where the weight sits
Investigation. Each lead in the log opens the next one, and the first story (one slow agency) usually does not survive the second look.

The investigation
The solver works through a log of millions of requests.

Work out what a closed request records: status, closed date, and resolution descriptions that separate fixes from duplicates and from visits where the inspector could not get in, and decide how each counts against the prompt's definition of resolved.
Estimate time to resolution with the still-open requests counted, as a survival curve by creation month, so growing backlogs show up instead of hiding.
Split the citywide change into mix (more requests of slow types) and slowdown within types, and show the leading contributors keep their order under either decomposition order.
Drill through agency, complaint type and borough where volume supports an estimate, pooling small leaves toward their parent.
Date the start of each leading leaf's slowdown, which separates a sudden break, such as a staffing or process change, from a backlog that built over months.
Check that the leaf shares add up to the within-type change computed directly.
Where it shows up in real data
NYC 311 Service Requests on NYC Open Data (now split into a 2010 to 2019 file and a 2020 to present file) carry created and closed dates, status, agency, complaint type (now labelled Problem) and location, along with a free-text resolution description. Chicago, San Francisco and Boston publish similar feeds. Requests still open, pending or in progress, and requests closed as duplicates or after inspectors could not gain access, are all in the data as published.

Scenario
A deputy mayor's office sees median days to close rise from 4.1 to 6.8 between two fiscal years and has two process-improvement teams to assign. It wants to know where the slowdown came from, how much of it each source explains, and since when.

Where a hurried analyst goes wrong
Computing medians on closed requests only, which reproduces the city's own dashboard and so looks authoritative, but understates the slowdown in exactly the types where requests pile up. Ranking complaint types by their own increase and ignoring that the mix shifted. Letting a tiny leaf top the list on noise. Reporting shares that do not add up to the change. Naming causes without dates, so a backlog and a break look the same.

What the solver delivers
The ranked leaves with shares and intervals that reconcile to the within-type change, the mix effect, the onset month for each leading leaf, and the definition of resolved used. The fiscal years and the outcome definition come from the prompt; every share is recomputable from the log.

Keeping it deterministic
Choose years where the top leaves keep their order under any reasonable decomposition and whether duplicate closures are kept or dropped, so no single reading of the resolution text decides the ranking. Grade shares within a band and onset months within one or two months. The prompt must not mention open requests, censoring, duplicates or mix.

7. A ridership forecast after a regime break
Analysis type and answer shape
Forecasting & Predictive Modeling; a monthly path with a band, the fiscal-year total with its range, and the drivers of the change from this year.

Where the weight sits
Validation. Many models fit the past well; the hard part is showing which one would have forecast well from inside the new regime, and building a band that is honest about it.

The investigation
Finance wants a number it can budget against, and getting there runs through six results:

reconcile the daily boardings to the agency's monthly reports to the federal database before modelling, explaining any gap;
measure the recovery path of each day type since 2020 and the change in the pattern within the week under hybrid work;
pick the training window and model by rolling-origin back-tests on the post-break period against simple benchmarks;
forecast daily and aggregate to months through the calendar, since months differ in how many weekdays and holidays they hold;
build the band from back-test errors at each horizon; and
split next year's change into weekday recovery, weekend trend and calendar.
Where it shows up in real data
The Chicago Transit Authority's daily boarding totals by day type on the Chicago Data Portal; MTA daily ridership on NY Open Data; the Federal Transit Administration's National Transit Database monthly ridership by agency and mode back to 2002; agency schedules in GTFS archives such as the Mobility Database.

Scenario
A transit agency's finance office needs monthly ridership for the next 18 months with an 80 percent band, to set the fare revenue line in the budget, and a paragraph for the board on what is driving the number.

Where a hurried analyst goes wrong
Fitting a seasonal model to monthly totals over the full history with a 2020 dummy, which carries the old seasonal shape forward. Extrapolating last year's growth. Ignoring weekday counts by month. Quoting a band from in-sample errors that is far too narrow. Skipping the reconciliation, so the forecast is built on a series the budget office will not recognize.

What the solver delivers
The monthly path and band, the fiscal-year total and range, the driver split, the back-test table that justified the model, and the reconciliation. Set the forecast origin in the past and leave later data out of the folder, so the forecast can be checked against what actually happened.

Keeping it deterministic
Check that the deep forecast's band covers the held-out months and the shallow one's does not. Grade the fiscal-year total and the path within a stated tolerance, and the driver split within a band that covers reasonable orderings. The prompt must not mention day types, back-testing or the break.

8. Net effect of enforcement cameras with nearby spillover
Analysis type and answer shape
Experiment & Causal Analysis; one number with a band, plus its split by crash type and the distance at which the effect fades.

Where the weight sits
Modeling. Selection on past crashes, spillover to nearby intersections, staggered timing and a trade between crash types all have to be handled in the same model.

The investigation
The first surprise is in the camera list: it shows only cameras still running. So

each camera's active period has to be reconstructed, with the switched-off ones dated from where their violation series stop. From there the solver has to
match geocoded crashes to intersections and distance rings;
correct for sites chosen for their crash history with Empirical Bayes estimates from a safety performance function fitted on comparison intersections;
estimate spillover by ring across all cameras, using switch-on and switch-off events, and find where it fades;
compare each activation cohort only with intersections not yet or never treated; and
split the effect by crash type, weight it by severity and express it per camera-year.
Where it shows up in real data
Chicago's data portal publishes red-light camera locations with go-live dates, and daily violation counts by camera from July 2014. The location file lists only active cameras, but the 50 the city switched off in March 2015 (a few later switched back on) and the 12 in June 2017 can be dated from where their violation series stop, which gives switch-off as well as switch-on variation. Geocoded crash reports come from the city's Traffic Crashes dataset and state DOT crash files. FHWA crash cost guidance and the KABCO injury scale give severity weights.

Scenario
A city transportation committee is pricing the next camera contract and wants the severity-weighted injury crashes the cameras prevent per camera-year, with a 90 percent interval.

Where a hurried analyst goes wrong
Comparing camera intersections before and after against all other intersections, so regression to the mean inflates the effect. Leaving nearby intersections in the comparison group although the cameras reached them. Counting total crashes, which hides fewer right-angle crashes behind more rear-end ones. Pooling staggered start dates in one regression. Treating the location file as the full history.

What the solver delivers
The net effect per camera-year with its interval, the split by crash type, the fade distance, and the camera history table with switch-off dates. The prompt fixes the outcome, window and interval level; the violation series pin the active periods.

Keeping it deterministic
Check that the estimate stays within a narrow band across reasonable ring definitions and model forms, and grade within that band. Grade the camera history and fade distance separately. The prompt must not mention crash types, regression to the mean, nearby intersections or how to build the comparison.

Education & Learning Sciences
Education data is coarse, moves its scale between cycles and arrives before the outcome has happened. The three strategies here put the weight on recovering a quantity the files never publish, on deciding what is knowable on the day a model fires, and on splitting a score change among competing explanations.

9. Achievement gaps recovered from proficiency bands
Analysis type and answer shape
Descriptive & Distribution Analysis; cuts of a distribution, a list, and how that list differs from the one the state already publishes.

Where the weight sits
Estimating a quantity the files never publish. Only band counts exist, and the gap has to be recovered from them before anything is ranked.

The investigation
The work starts from four band counts per group. An ordered model with thresholds shared across the state gives each group in each district a mean and a spread, and its fit is checked against the observed band counts. Suppressed or range-reported groups enter as interval-censored rather than being dropped. Small districts' gaps are shrunk for measurement error. Then come the quintile cut points, with intervals, and the widest-gap fifth. Two comparisons close it out: against the list built from percent proficient, showing which districts move and why through floor and ceiling compression, and against published gap estimates built from the same kind of counts.

Where it shows up in real data
California's CAASPP research files give the percent of each student group at each of four achievement levels for every school and district in each tested year (there are no 2019-20 results); Texas and New York publish similar files. EDFacts assessment files give percent proficient with ranges for small groups. The Stanford Education Data Archive publishes gap estimates built from band counts, which serve as a check.

Scenario
A state equity office will publish the distribution of district gaps between economically disadvantaged and other students in grade 8 math, cut into fifths, and offer technical assistance to the widest-gap fifth. Its director expects questions about why the list differs from the dashboard.

Where a hurried analyst goes wrong
Differencing percent met or exceeded, which reproduces the dashboard to the decimal and so looks right, while very high- and very low-achieving districts show compressed gaps. Dropping suppressed groups, which removes small districts selectively. Ranking without shrinkage, so small districts land in the top fifth on noise. Giving cut points with no intervals.

What the solver delivers
The quintile cut points with intervals, the top-fifth list, the movers between this list and the percent-proficient list with the reason for each, and the comparison with the published estimates. The band counts pin the model; the published estimates give an outside check.

Keeping it deterministic
The prompt fixes grade, subject, year and groups, and states that the program targets the difference in achievement across the whole score range. Grade list membership with a tolerance at the cut and check it across reasonable model choices. The prompt must not mention cut-score dependence, ordered models or standard deviation units.

10. An early-warning cutoff set to advisor capacity
Analysis type and answer shape
Forecasting & Predictive Modeling; setting one dial, with the expected yield of the calls and the expected misses.

Where the weight sits
Framing and calibration. Most of the work is deciding who can be called and what is known on the day, then making the probabilities mean what they say; the learner itself matters little.

The investigation
Before any model, answer the team's practical question: who can actually be called?

Define the callable population as students still registered on day 42 of each presentation and count them. Then
build features from the click logs and assessment submissions only as they stood on day 42;
train on earlier presentations and validate on later ones, reporting discrimination and calibration by module;
recalibrate, since base rates differ by module;
set the cutoff that selects about 600 in the target presentations and give the expected number who would fail or withdraw without help, with a band; and
estimate how many students who will fail or withdraw fall below the cutoff, so the team knows what the program misses.
Where it shows up in real data
The Open University Learning Analytics Dataset holds about 32,000 students across 22 module presentations in 2013 and 2014: demographics, registration and unregistration dates, assessment submissions, final results and daily clicks on each resource in the virtual learning environment, with each resource's activity type. Withdrawals, late submissions and modules with very different base rates are all there as published.

Scenario
A university's student success team can call 600 students in week 6 of next term's presentations. It needs the cutoff on the risk score, the number it selects, how many of those are expected to fail or withdraw without help, and how many at-risk students the calls will not reach.

Where a hurried analyst goes wrong
Using features summed over the whole presentation, so clicks after week 6 and the unregistration date describe the outcome itself. Splitting at random, which mixes presentations and overstates performance. Counting students who left before week 6 as positives the team could have reached. Picking the cutoff from uncalibrated scores, so the expected hit rate is wrong even when the ranking is good. Reporting hits without misses.

What the solver delivers
The cutoff, the expected count selected, the expected hits with a band, the expected misses, and the validation table by module. Capacity and the target presentations pin the dial; holding out a presentation with known outcomes lets every expectation be checked.

Keeping it deterministic
Grade the cutoff, the expected hits and the misses within stated tolerances, and confirm they hold across reasonable model families. The prompt must not say which data are available by week 6, how to validate or that the scores need calibrating.

11. Splitting a score drop among its explanations
Analysis type and answer shape
Root-Cause Analysis; explanations ranked by the points each accounts for, with intervals, and the part that remains a real decline.

Where the weight sits
Attribution and synthesis. Four partial analyses, each with its own uncertainty, have to be combined into one account whose parts add up to the drop.

The investigation
Each candidate explanation gets its own analysis, in an order that matters. Participation comes first:

compare the tested population with the enrolled population in each cycle and bound what lower participation and exclusions could move. Then the scale:
estimate item-by-item difficulty shifts on the trend items and re-link without the items that drifted. Composition only after that:
reweight for student background on the re-linked scale. Throughout,
replicate-weight and linking uncertainty is carried into every share, and at the end
the shares are reconciled to the observed drop, with a ranking claimed only where the intervals separate.
Where it shows up in real data
PISA public files carry item-level cognitive responses with the test design variables that say which items each student saw, student weights and 80 replicate weights for each cycle. The technical reports document coverage of the 15-year-old population, exclusion rates and the 2022 cycle's lower participation in several countries, with the nonresponse bias analyses those countries had to run. TIMSS and PIRLS publish item-level data too, with their own jackknife variance design.

Scenario
An education ministry's mean math score fell 14 points between two cycles, and a parliamentary committee asks how much of that is a real change in what students know.

Where a hurried analyst goes wrong
Reweighting the later cycle to the earlier composition, finding two points and calling the other twelve a real decline, without asking whether the tested population or the trend items changed. Doing the steps in the wrong order, so composition is measured on a scale that drifted. Reporting shares with no intervals, or a ranking the intervals do not support. Letting the shares fail to add up to 14.

What the solver delivers
Each explanation's share in points with its interval, the remaining real decline, the list of drifted items, and the participation bounds. The drop itself is published, so the shares have a hard total to reconcile to.

Keeping it deterministic
Pick a country and pair of cycles where the shares separate by more than their intervals, grade each share within a band, and check the re-linked result with two linking methods. The prompt must not name participation, item drift or composition as candidates.

Shallow versions of these ideas
Each idea above has shallow twins that look similar and get sent back because one planted or hidden thing flips the answer. Others look narrow but are honest analysis and pass. Decide which designs you would send back before you open the reasoning.

Read each task design. Send back the ones decided by a planted defect, a shallow hidden factor or a field reading, and approve the ones built on honest analysis of the real data.

These are task designs, not prompts. Ask what decides the result, and whether telling the solver one fact would make the rest routine.

1. Interviewer anomalies. The author copies one interviewer's answers across 60 households in the survey file, and the task is to name the interviewers whose work should be re-checked.
Strategy 2

Verdict and reasoning
Send back. One planted block decides it, and "look for duplicated questionnaires" makes the rest routine. That is a planted defect, however large the file.

Revised design
Use real DHS or MICS interview files as published. The solver separates interviewer from area effects, builds several process signals, calibrates the chance count for a list of 40, names the evidence behind each flag and shows how much the headline estimates depend on the flagged work.

2. Overlapping survey years. Real CPS files as published. The only hard step is noticing that the samples overlap and putting the covariance into the variance of the change; after that the 51 classifications are arithmetic and carry the whole score.
Strategy 1

Verdict and reasoning
Approve. Nothing is planted, and putting the overlap covariance into the variance of the change is legitimate survey work, not a hidden fact. Asking for each state's overlap and a reproduction of the published standard errors as well would give careful work more to earn.

3. Slower service requests. The author shifts one agency's closed dates forward by 30 days for three months, and the task is to find which agency explains the citywide slowdown.
Strategy 6

Verdict and reasoning
Send back. The deciding factor is constructed and sits only in the deciding unit, and one cross-tab by agency and month reveals it. This is a shallow hidden factor.

Revised design
Use the city's 311 feed as published. The solver decides what counts as resolved, counts open requests, splits mix from within-type slowdown, drills down with pooling, dates each leading slowdown and reconciles the shares to the total.

4. Early warning. Real learning-analytics data from 22 course presentations, plus a week-6 engagement column the author built from each student's final result. Any classifier that keeps the column ranks almost perfectly, and the task turns on spotting it.
Strategy 10

Verdict and reasoning
Send back. The column is constructed, and once caught it flips the whole answer: told "that column is built from the outcome", any solver drops it and the rest is routine. That is a planted decoy.

Revised design
Ship the real data as released, with nothing added. Define who can still be called on day 42, validate on later presentations, calibrate by module, set the cutoff for 600, and report the expected hits and the expected misses below the line.

5. Red-light cameras. The author adds 40 rear-end crashes at the two intersections beside the camera that decides the budget call, and the solver must notice them to get the net effect right.
Strategy 8

Verdict and reasoning
Send back. The spillover is planted in two deciding units only. Told "there are extra crashes next to camera 14", any solver drops them and the task is routine.

Revised design
Estimate spillover by distance ring across every camera in real city data, using switch-on and switch-off dates recovered from the violation series, alongside correction for site selection, staggered timing and severity weighting.

6. Proficiency gaps. The state guidance can be read as counting "nearly met" as proficient in one year and not the next, and only one reading puts the right districts in the top fifth.
Strategy 9

Verdict and reasoning
Send back. The task turns on reading one definition, and if both readings are defensible it is not deterministic either.

Revised design
Fix the definition in the prompt and move the work to measurement: recover each group's mean and spread from all four bands, treat suppressed groups as censored, shrink small districts, cut into fifths with intervals and explain how the list differs from the dashboard's.

7. Claims alerts. Real weekly claims by state since the 1990s. The solver writes an alert rule, shows on held-out years that it stays within two false alerts a year, lists the weeks it would have flagged, measures how many notified layoffs it caught and accounts for every unmatched flag.
Strategy 4

Verdict and reasoning
Approve. Nothing is planted. Moving holidays, the 2020 break and level-dependent noise are all in the real series, and the rule, its false-alarm band, the flag list and the catch rate are separate results that each take work.

8. Score drop. Real item-level assessment files for two cycles. The solver bounds what participation could move, re-links the scale without drifted items, reweights for composition and reports each explanation's share with an interval, reconciled to the published drop.
Strategy 11

Verdict and reasoning
Approve. Four pieces of real work each produce a checkable share, the shares must add to a published total, and missing any one piece costs only that piece's credit.

Key lesson
A shallow version hangs the result on one hidden or planted thing: a planted block, a built-in factor, a leaking column or one reading. Once seen, the rest is routine. A legitimate method choice is fine even when it is the hardest step. The strongest versions spread the difficulty across several pieces of real work, each checkable, so more careful work keeps earning more.

Strategies, not templates
Each strategy names real public sources and sketches a scenario so you can find the phenomenon, not so you can copy the task. Build your own question on your own data. The strategies deliberately put the weight of the work in different places: some are mostly assembly, some mostly measurement, triage, investigation, modeling, validation, attribution or synthesis. Do the same across your own tasks. Two tasks with the same chain of steps in the same order, the same question template and the same answer shape are treated as templated even on different data, and reskins of delivered tasks (the same trap, detection and fix moved to a new topic) are returned too. Reusing a lesson is fine; reusing a structure is not.

How to use a strategy
Start from genuine public data, used as is, where the difficulty already exists, and prefer inputs with real breadth: many runs, series, machines, units or files. If you assemble or extend data, it has to behave like the real thing throughout, with many genuine patterns and noise, not one effect added for the solver to find; otherwise it is a shallow hidden factor and is sent back. Plan the results the solver must produce, decide where the weight of the work sits, and make sure each result is pinned by the data or a stated convention, with a band where reasonable methods differ. The prompt pins the business question, the outputs and the baseline. It never names the method, the comparison group, the confounder or the adjustment. Vary the answer shape too: a ranked set of causes with their contributions, a timeline of what went wrong and when, a forecast path with bands and its drivers, a bridge that reconciles, or a flagged set with its evidence.