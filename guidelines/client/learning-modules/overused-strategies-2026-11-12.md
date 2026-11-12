# Overused stumping strategies (Project Sulfur, task design), read 2026-11-12

Kept verbatim as the client's own page, pasted by the author on 2026-11-12. It sits beside `stumping-strategies.md`
and `../deep-reasoning.md` and governs where it is newer than a skill. The skeleton guard carries its 34 cards as
closed lessons (`.claude/skills/fingerprint/skeleton_vocab.json`, `closed_lessons`; `skeleton.py closed` lists them).

---

Project Sulfur · task design

Overused stumping strategies

Each card below is an analytical lesson that already decides the answer in two or more accepted tasks. All of them
are closed: if your task's answer only flips because of one of these, it will be returned as a repeated lesson, even
in a new domain and with new data. Use this page before you build: pick a deciding step that is not here.

**Same lesson means same fix.** Same mechanism and the same kind of fix counts as the same lesson. Changing the
domain, the dataset or how the problem is detected does not make it new.

**Supporting steps are fine.** A strategy from this list can appear as one step in a richer task. It cannot be the
step that flips the answer.

**Stacking two of them is not new.** A task whose answer needs two strategies from this list, and nothing new, is
still a repeat.

All 34 strategies are closed: none can be the deciding step of a new task.

Families: Who ended up in the data; Noise and small numbers; Time, follow-up and timing; Carrying an effect to a new
place; How it was measured or recorded. Showing 34 of 34 strategies.

## Who ended up in the data (5 strategies, 25 accepted tasks)

**Units picked at an extreme fall back anyway (regression to the mean).** 7 tasks. Closed.
The trap: Units or periods were chosen because they were unusually bad or unusually good, so they drift back toward
normal whatever you do.
The fix already used: Compare with units that had the same history but were not picked, or use the years before the
selection as the baseline.
Accepted examples (4): Nursing homes bought after a run of fines, compared with same-history homes instead of the
state average. Street-patrol areas picked after a peak year, judged against the years before selection. Hospital bed
requests from units chosen for steep recent growth. A short river record that happens to fall in a wet period,
extended over a long neighbouring record.

**Today's file has lost the ones that died or left (survivorship).** 6 tasks. Closed.
The trap: The current export only holds units that survived: dead funds, removed questions, departed listings, claims
still paying. Older periods have lost more of them.
The fix already used: Rebuild each period as it was known at the time (dated exports, point-in-time universe) or
reweight by survival.
Accepted examples (4): A hedge-fund benchmark built from today's database, missing funds that closed. Holiday-rental
reviews that vanish when a listing leaves the platform. A Q&A site that prunes unanswered questions, so the latest
export flatters the older year. Workers' comp claims selected for still paying, so their own history shows no stops.

**Outcomes are hidden by the intervention itself.** 5 tasks. Closed.
The trap: The people or lines flagged as risky were rescued, treated or audited, so their recorded outcome is the
intervention, not the underlying risk.
The fix already used: Rebuild what would have happened without the intervention, using units it could not reach or a
comparison where it did not run.
Accepted examples (4): Choosing a probation risk tool when the old tool's high-risk picks were already supervised. A
supplier's on-time rate inflated by expediting the lines flagged as likely late. Goodwill credits given after
complaints, which boost the repurchase rate being measured. Reassessment accuracy judged on sales whose values were
reset by the sale itself.

**Self-selection into exposure: compare a unit with itself.** 4 tasks. Closed.
The trap: People or operators who choose the exposure differ from those who do not, so the raw gap measures who they
are.
The fix already used: Compare the same person, operator or unit with and without the exposure.
Accepted examples (4): Soda bought at a cooler-door deal, compared with the same buyer's other days. Short-let hosts
who greet guests, compared within the same operator. Caregivers' sleep, tested on days with and without the respite
service. A speech-recognition tool, compared within clinicians who worked at two sites.

**Rows are occurrences, not the people you care about.** 3 tasks. Closed.
The trap: The data is sampled by visit, vote or notice, so frequent visitors or people listed twice count more than
once.
The fix already used: Link records to the person and weight each record by one over its multiplicity.
Accepted examples (3): Intercept surveys of park visits used to estimate a share of visitor groups. Comfort votes
where heavy repeat voters inflate acceptability. Injury notices where workers notified twice get double selection
chances.

## Noise and small numbers (5 strategies, 24 accepted tasks)

**Small units top the ranking by chance (shrinkage).** 8 tasks. Closed.
The trap: The raw leaders or laggards are small or noisy units. Taking them at face value picks the wrong ones.
The fix already used: Shrink each unit toward its expected value by its reliability (partial pooling or an area-level
model).
Accepted examples (4): Picking a heart-failure partner hospital by mortality, where small hospitals top the raw
ranking. County child-poverty estimates from small survey samples. A headline-testing tool whose "winning" headline
overstates the gain. Diamond graders flagged for retraining from short audit records.

**Outcomes cluster, so item-level intervals are far too narrow.** 6 tasks. Closed.
The trap: Outcomes come in batches by facility, lender, court, video or precinct, but the interval treats every item
as independent.
The fix already used: Resample or cluster on the unit that drives the outcome.
Accepted examples (4): Nursing-home citations clustered by facility. Small-business loan losses where a few lenders
dominate. Bench-warrant shares that are set court by court. An election-night sample that has to sample whole
precincts.

**Units vary more than the stated error, so alert bars are too tight.** 4 tasks. Closed.
The trap: Published standard errors or binomial chance understate the real spread, and many tests are run at once, so
too many units get flagged.
The fix already used: Measure the real dispersion from the data, widen the bar, and correct for the number of tests.
Accepted examples (4): State food-insufficiency alerts on a biweekly survey where flags keep reversing.
Health-shortage area re-run requests judged with an overdispersed funnel. A journal profile-linking monitor whose
alert rule is calibrated on observed noise. Identical test arms used to measure the real noise before ranking
variants.

**A noisy explanatory variable flattens the slope.** 4 tasks. Closed.
The trap: The variable on the right-hand side is measured with sampling or reporting noise, so the fitted slope is
pulled toward zero.
The fix already used: Estimate how much of its variance is real (from margins of error, repeat measures or split
halves) and correct the slope.
Accepted examples (4): Polling-place wait times measured from only two or three checks. Survey-based broadband shares
used to predict business activity. Group-level survey shares used to rank representation slopes. Low-income exits
inflated by reporting noise between two survey waves.

**Chance coincidences counted as caused (placebo baseline).** 2 tasks. Closed.
The trap: Events are linked by time and place, so some matches are strangers or background exposure.
The fix already used: Subtract a placebo baseline built by shifting the events to other days or windows.
Accepted examples (2): Ride-back offers matched to rides by station and time without a customer key. Foodborne illness
attributed to a market hall, net of ordinary eating exposure.

## Time, follow-up and timing (10 strategies, 35 accepted tasks)

**Follow-up is still open, so unfinished cases are not failures (censoring).** 8 tasks. Closed.
The trap: Many units have not had the full window yet. Counting them as non-events, or using their planned end dates,
biases the rate.
The fix already used: Treat unfinished follow-up as censored and complete it with survival curves, by cohort where
cohorts differ.
Accepted examples (4): A first-year re-answer rate for a newcomer cohort that has not had a full year. A one-year
reoffending rate when one group was mostly released recently. Trial completion times with unfinished trials censored
at the extract date. Loan charge-offs where young vintages are completed from their own curve.

**Another exit ends the clock first (competing risks).** 5 tasks. Closed.
The trap: Early repayment, revocation or a limit stops units before the event of interest, so a single-exit model
misstates lifetime totals.
The fix already used: Model the competing exit explicitly (survival-weighted, conditional on still being open).
Accepted examples (3): Lifetime default on car loans with early repayment as a competing exit. Rate buy-down subsidy
costs weighted for early payoff. Court outcomes for parolees when board revocation got there first.

**Late entry and immortal time.** 4 tasks. Closed.
The trap: Units only enter the data after surviving for a while (late registration, joining a register late,
receiving an exposure that requires survival).
The fix already used: Start each unit's clock at entry into observation, or compare from a landmark among those still
active.
Accepted examples (4): Trials registered after they started, which are pre-filtered survivors. A patient registry that
enrols people months after diagnosis and only if alive. An answer-acceptance reminder that only people who stayed
long enough could receive. Care schemes that joined a register late, carrying only their surviving residents.

**An early spike inflates the average (use the settled level).** 4 tasks. Closed.
The trap: A launch, policy cutover or new tool produces a burst or a learning curve, so the period average is not what
will last.
The fix already used: Index the effect by time since exposure and read the settled level.
Accepted examples (4): An analyst-support pilot whose effect decays after launch. A home-page layout test dominated by
early novelty under staggered enrolment. A court docket after a pretrial law, sized on the settled post-change level.
A news app audio feature indexed by weeks since each edition's launch.

**Recent counts are still filling in (reporting lag).** 3 tasks. Closed.
The trap: The latest periods look low because reports are still arriving, and the delay differs by route or group.
The fix already used: Complete recent counts with delay factors estimated for each route or group.
Accepted examples (3): Respiratory incidence nowcast by district and reporting route. Drug safety events still filling
in across repeated pulls. Serious-infection reports whose submission delay recently slowed.

**Repeated exposure behaves differently from a one-off.** 3 tasks. Closed.
The trap: The trial measured isolated exposures, but the decision is a run of repeated or consecutive ones (fatigue,
carryover, saturation).
The fix already used: Split the effect by prior exposure and carry the target schedule through it.
Accepted examples (3): Daily outreach pulses tested one at a time, planned as 91 consecutive contacts. Smart-thermostat
demand response that fades over consecutive hot event days. Storm-day rating for a season the book has never insured.

**Values at a measurement limit are bounds, not numbers.** 2 tasks. Closed.
The trap: Readings below a detection limit or timeouts at a time limit are treated as exact values or dropped.
The fix already used: Treat them as censored bounds.
Accepted examples (2): Lab results below the detection limit in a rock geochemistry load. Answer times capped by a
short time limit in a counting test.

**Young cohorts look different only because they are young.** 2 tasks. Closed.
The trap: An excess in recent records looks like a lag that will clear, or a shortfall looks like it will catch up.
The fix already used: Compare each cohort with settled cohorts at the same age to see whether the gap really closes.
Accepted examples (2): Hospital coding corrections that look short on young accounts. Journal profile-linking problems
that look like lag but persist at matched age.

**Purchases pulled forward from later (payback).** 2 tasks. Closed.
The trap: A rebate or offer creates a spike that partly borrows from later months.
The fix already used: Measure through the payback window and net the later shortfall.
Accepted examples (2): Heat-pump rebates whose spike is followed by a shortfall. A prepay offer whose test-quarter lift
borrows from later in the year.

**The easy cases get used up first.** 2 tasks. Closed.
The trap: A trial's yield came from a one-off stock of easy cases that has now run out.
The fix already used: Project the future rate from the replenishment flow, not the trial's average.
Accepted examples (2): A starter-task feed whose yield came from pre-existing easy items. A screening programme whose
early high yield came from a backlog of undiagnosed patients.

## Carrying an effect to a new place (7 strategies, 33 accepted tasks)

**The pooled effect does not transfer to a target with a different mix.** 9 tasks. Closed.
The trap: A trial or pilot ran on one population. The effect depends on some trait (caseload, remoteness, baseline
rate, tenure), and the target has a very different mix of that trait.
The fix already used: Estimate the effect within bands of the trait and apply each band to the target's own mix
instead of carrying the average.
Accepted examples (4): A mentoring offer for people leaving prison, where the effect depends on the officer's
caseload, reweighted to the new county's caseload mix. A hospital-at-home rollout piloted in mostly urban areas, where
the effect grows with remoteness, carried to rural boards. A Medicaid expansion effect estimated on early adopters
with high baseline uninsured rates, scaled down for a late-adopting state. A time-of-use pilot carried to a
substation whose households respond very differently.

**Controls were partly treated (spillover or shared resource).** 9 tasks. Closed.
The trap: Treated and control units share something: chargers, a labour market, a hub, a field crew, a market. The
treatment changes the controls too, so the side-by-side gap is not the effect of treating everyone.
The fix already used: Model the outcome on how much of each unit's neighbourhood is treated, or drop contaminated
controls, and read the effect at full rollout.
Accepted examples (4): A job-coaching pilot where coached claimants take jobs untreated claimants would have got.
Execution-algorithm trials where the treated orders also lower the controls' trading costs. Brine treatment on
walkways that leaves residue on the "untreated" comparison zones. A car software release where treated cars change
charger queues for untreated neighbours.

**Gains taken from neighbours (displacement, cannibalisation, cross-border).** 5 tasks. Closed.
The trap: The treated unit looks better partly because nearby untreated units lost the same business, or buyers
crossed a border.
The fix already used: Net the neighbours' loss out of the gain, and keep affected neighbours out of the comparison
group.
Accepted examples (4): A local-produce shelf whose uplift partly comes from sister stores nearby. A state cigarette tax
where some of the sales drop is purchases moving next door. A beverage tax elasticity measured where only one city
raised prices, applied to a statewide tax. A bus fare rise where single-product elasticities count riders switching
tickets as lost.

**Arms differ in mix because assignment odds differed by group.** 3 tasks. Closed.
The trap: Randomisation or serving probability varied by tier, grade or segment, so the arms are not comparable as
pooled.
The fix already used: Estimate within each assignment group and weight to the target, which often reverses the pooled
sign.
Accepted examples (3): A reorder button tested with allocation that depended on a customer value tier. Tutoring
lotteries whose offer odds differed by grade within each school. A recommendation slot where each policy served
different customers.

**A crude gap is just composition (age or mix standardisation).** 3 tasks. Closed.
The trap: Two groups are compared on a raw rate, but they differ sharply in age or another composition variable.
The fix already used: Standardise both groups to the same composition (indirect standardisation with fine bands, or
reweighting the sample to the target).
Accepted examples (3): A night-crew fatigue gap that disappears once age and hour of shift are standardised. A
hospitalisation gap between two groups compared with fine age bands. Urine culture results reweighted from the tested
sample to the age mix of all treated infections.

**Where does a closed unit's demand go.** 2 tasks. Closed.
The trap: A unit is closing and the question is how much of its demand the remaining units absorb.
The fix already used: Measure the diversion share from history (past closures or sold-out nights) instead of splitting
it in proportion to the others' size.
Accepted examples (2): A hospital closure: where displaced patients go, back-tested on earlier closures. A campground
closure: how many campers stay in the area, measured from nights the site was sold out.

**A fixed-count effect has to be rescaled to each unit's size.** 2 tasks. Closed.
The trap: A past intervention removed or added a fixed number of things, but the effect is quoted as a percentage that
depends on how big the unit is.
The fix already used: Rescale the effect to each unit's own base (business stock, job count) before applying it.
Accepted examples (2): A task force that removes a fixed number of late jobs per branch, rescaled to branch size.
Advice points whose effect depends on posts relative to the local business stock.

## How it was measured or recorded (7 strategies, 19 accepted tasks)

**The instrument changed (drift or step change).** 5 tasks. Closed.
The trap: A sensor, satellite or test changed partway through, so part of the trend is the measurement.
The fix already used: Find the break against unaffected series or arms and correct readings to one basis.
Accepted examples (4): Satellite fire counts after the orbit's pass time drifted. A weather station's summer highs
with an undocumented instrument step. A telescope site's clear-night share across a cloud-sensor break. A bias test
where an instrument change hit only one randomised arm.

**The survey changed, not the world.** 4 tasks. Closed.
The trap: A redesign, a rotating panel or a recall change moves the headline: different people answered, or they were
asked differently.
The fix already used: Bridge the two designs (first interviews only, entering panel group, contact-schedule step)
before reading the change.
Accepted examples (4): Unreported work injuries where recall length and interviewer experience differ between
periods. A survey rate restated to the legacy instrument after a redesign. A jump in the share working driven by
re-interviews in a rotating panel. A business index that steps down at every panel re-contact.

**Seasons fall in different places (fieldwork timing).** 2 tasks. Closed.
The trap: Groups were surveyed or exposed in different seasons, so the comparison mixes in seasonality.
The fix already used: Estimate the month profile within fixed units and adjust everyone to an average month.
Accepted examples (2): Regional damp-home shares surveyed in different seasons. A motor tariff review with part-year
exposure in a seasonal year.

**Activity recorded where it is billed, not where people live.** 2 tasks. Closed.
The trap: A national supplier or lab bills from one area, inflating that area's figures.
The fix already used: Strip the national supplier out of the local figures.
Accepted examples (2): Medicare screening counts located where the provider bills. Drug dispensing inflated in one
region by an online pharmacy.

**Two sources that are not independent (capture-recapture).** 2 tasks. Closed.
The trap: Total incidence is estimated from two lists, but one list partly feeds the other.
The fix already used: Remove the dependent records before the two-source estimate.
Accepted examples (2): Scam incidence from a member register and an external register. Disease notifications where
some physician forms were requested after a lab report.

**A co-occurring change is tangled with the treatment.** 2 tasks. Closed.
The trap: Something else changed at the same time as the treatment (a defect, a session order), so the contrast mixes
the two.
The fix already used: Size the co-occurring factor on a control task or outcome it alone affects and divide it out.
Accepted examples (2): Reading passages fully confounded with session order, netted out with a control task. An in-app
offer whose cohort also got a release defect.

**Hindsight leaks into the evaluation.** 2 tasks. Closed.
The trap: A rule or controller is judged with information it could not have had at the time.
The fix already used: Replay the rule with only what was known at each decision date. (Replay on its own can never be
the deciding step.)
Accepted examples (2): A cost-of-living inflation bias correction judged in hindsight. Battery savings from a dispatch
plan that knew each month's peak in advance.

---

Not on this list does not mean safe. Some deciding steps are never accepted, however rare: a single hidden factor
planted in the data, applying a rule the brief states, reading a field correctly, and replaying a rule with
hindsight. Those can appear in a task, but they cannot decide it.

Data counts too. Two tasks may not analyse the same records. Using the same large public release is fine only when
your task analyses different records (another state, another site, another period).

Counts are accepted tasks whose deciding step uses the strategy. The examples describe those tasks' settings so you
can recognise the pattern; they are not templates to adapt.
