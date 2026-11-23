# The open ground: what the client has closed, where the runs still lose, and where to build next

The client's Overused stumping strategies page (`guidelines/client/learning-modules/overused-strategies-2026-11-21.md`)
closes 45 lessons in six families, each already deciding two or more accepted tasks. This file reads our own run
record, the four approved builds and the client's three hardest examples against it and names the ground that is
still open. `../SKILL.md` Part 1c holds the rule; this file holds the evidence behind it. `python3
.agents/skills/fingerprint/skeleton.py closed` prints the page as the guard holds it and every card on file against
it; `skeleton.py open` prints the lessons no accepted task teaches.

## 1. What the page closes, and the rules that come with it

The six families and their 45 cards, as lesson keys in `fingerprint/skeleton_vocab.json` `closed_lessons` (61 keys;
the eleven cards the read of 2026-11-21 added are marked new, and each key carries its closing date):

| Family | Closed (lesson keys) |
|---|---|
| Who ended up in the data (7) | regression to the mean (selection_on_peak_baseline, normal_period_correction); survivorship (survivor_selected_sample); outcomes hidden by the intervention (intervention_masks_outcome); self-selection, compare a unit with itself (self_selection_into_treatment); rows are occurrences (length_biased_sampling); new: who takes the option depends on the offer (adverse_selection_into_option); new: the treatment changes who is left to measure (treatment_changes_who_is_observed) |
| Noise and small numbers (5) | shrinkage (shrinkage_small_samples, selection_on_noisy_means); clustered outcomes (uncertainty_at_shared_unit, serial_or_common_shock_dependence); units vary beyond the stated error (variance_beyond_sampling_noise); a noisy regressor flattens the slope (measurement_error_attenuation, errors_in_covariate); chance coincidences, a placebo baseline (chance_coincidence_baseline) |
| Time, follow-up and timing (11) | censoring (open_follow_up_censoring, completion_of_young_cohorts); competing risks (competing_risks); late entry and immortal time (left_truncated_ages, immortal_time_exposure); an early spike, the settled level (effect_fade_with_time); reporting lag (reporting_lag_nowcast); repeated exposure (repeated_exposure_response); values at a limit (censored_or_capped_observation); young cohorts at matched age (vintage_or_cohort_drift); payback (rebound_after_window); the easy cases used up (depleting_stock_of_easy_cases); new: the outcome runs on a different clock (outcome_follows_other_clock, exposure_basis_decoupled) |
| Carrying an effect to a new place (7) | the pooled effect does not transfer (transport_effect_modifiers, heterogeneity_carried_to_decision); spillover (interference_spillover); gains taken from neighbours (displacement_netting, cannibalisation_with_pretrend, downstream_offset); assignment odds by group (assignment_odds_by_group); composition (composition_versus_behaviour); a closed unit's demand (closure_diversion); a fixed-count effect rescaled (fixed_count_effect_rescaled) |
| How it was measured or recorded (10) | the instrument changed (measurement_basis_break); the survey changed (survey_design_change); fieldwork seasons (fieldwork_season_mix); billed where, not lived where (recorded_at_billing_location); dependent capture (dependent_capture_channels); a co-occurring change (concurrent_change_in_comparison); hindsight (hindsight_in_evaluation); new: the source reads high or low, calibrate on checked cases (source_bias_calibrated_on_checked_cases, record_check_reporter_error, anchored_second_reading); new: some groups are recorded far less completely (recording_completeness_by_group, optional_record_unlogged_changes, linkage_missing_not_at_random); new: old figures on an old basis (old_basis_restated_to_target) |
| Model and method choice (5, all new) | the projection holds fixed something the change will move (projection_holds_moving_intermediate); a straight line or an average misprices the margin (curved_response_at_the_margin, marginal_not_average, scaling_diminishing_returns); credit only what would not have happened anyway (incremental_over_without_baseline); extrapolating past the range the data has seen (extrapolation_beyond_observed_range); scored on the same data used to choose it (scored_on_selection_data) |

`closed_near` keys 39 more lessons that sit next to a card. A call that turns on one of them is a WARN, and the note
says how the mechanism or the fix differs from the card:

| Card | Lessons next to it |
|---|---|
| Self-selection | confounded_history_of_use |
| Rows are occurrences | design_weights |
| Units vary beyond the stated error | planned_design_noise |
| Reporting lag | observation_window_coverage |
| The pooled effect does not transfer | customer_specific_response, pilot_unrepresentative_selection, bounded_outcome_headroom |
| Spillover | leader_follower_spillover |
| The instrument changed | device_clock_drift |
| Fieldwork seasons | seasonal_shift_calibration |
| A noisy regressor | transitions_inflated_by_response_error |
| The settled level | state_reset_at_inspection |
| Adverse selection (new) | target_subset_selected_by_score |
| The treatment changes who is left (new) | label_observed_by_outcome |
| A different clock (new) | calendar_grid_shift, response_before_the_trigger, renewal_resets_hazard |
| Calibrate on checked cases (new) | calibrated_proxy_for_lost_attribute, proxy_link_differs_by_arm, starting_point_anchoring |
| Recorded less completely (new) | detection_rate_changes_outcome, level_and_mix_from_two_sources, record_algorithm_inversion, record_as_of_its_date, recording_effects_separated_jointly |
| The projection holds something fixed (new) | forward_window_structure_change, intensive_margin_response, queue_or_capacity_replay, staggered_conversion_at_renewal |
| The margin (new) | fixed_nuisance_component, behavioural_response_measured, response_at_crossing_point, nonlinear_functional_of_path, degradation_form, lot_size_cycle_stock |
| Credit only the excess (new) | route_pre_emption |
| Past the observed range (new) | second_channel_past_plateau, analog_event_calibration |
| Scored on the choosing data (new) | validation_cannot_see_condition |

The rules, the page's own words: **same lesson means same fix** ("same mechanism and the same kind of fix counts as
the same lesson; changing the domain, the dataset or how the problem is detected does not make it new");
**supporting steps are fine** ("it cannot be the step that flips the answer"); **stacking two of them is not new**.
And beyond the list: a single planted factor, applying a stated rule, reading a field and a hindsight replay are
never accepted as the deciding step, and two tasks may not analyse the same records (a shared public release is fine
only on different records).

**Read a candidate by its fix, not its name.** Every card carries a line "the fix already used". A stump whose whole
remedy is one of those lines is that card, whatever the record looks like and whatever key the card was given:

| The fix already used | Cards |
|---|---|
| a share or a factor from an independent source, then a gross-up | recorded less completely; reporting lag; censoring |
| a bias measured on cases that also carry a checked value, then every reading corrected | calibrate on checked cases |
| every period restated to one basis | old basis; the instrument changed; the survey changed |
| a curve fitted and each change valued at its own point | the margin; repeated exposure |
| the knock-on carried period by period | the projection holds something fixed |
| a baseline without the thing, and only the excess credited | credit only the excess; placebo baseline |
| the shape learned from units or periods that reached the range | past the observed range; young cohorts |
| a score on data the choosing never touched | scored on the choosing data; hindsight |
| everyone followed as assigned, or bounds | the treatment changes who is left; outcomes hidden by the intervention |
| take-up modelled and the option priced on the takers | adverse selection; self-selection |
| the clock tested and the comparison made on it | a different clock; late entry |

What this does to `../SKILL.md` Part 1b's six places runs lose: four are closed as deciding lessons (the split
carried to the decision is the transport card; units selected by the outcome's history are the regression,
survivorship and intervention cards; the system's net is the neighbours card; a response measured and the marginal
unit is the margin card). Two remain open as **kinds of loss**, each narrower than before: the assumption a run names
and waves through, as long as the assumption is not a card's (proportional scaling, a form carried past its range,
an intermediate held fixed, an old basis and a source at face value now are); and a shallow path that passes its
own checks, as long as the check fails for a reason other than reusing the data the choice was made on.

## 2. Where our runs lost, read against the page

`precedents.json` holds 67 losses and 41 named assumptions in the runs' own words. Read against the page:

**Closed as the deciding lesson** (still citable for a supporting step):
L08 (inclusion probability another unit set, near the occurrences card), L09 to L12 and L25 (the split not carried;
vintages pooled), L14 (selected survivors), L15 and L17 (a response assumed smooth, the average unit where the
decision buys the marginal one: the margin card), L16 and L18 (the unit priced alone; not-yet-treated taken as
untreated), L19 and L35 (default or independence errors where units share the cluster or the shock), L20
(attenuation), L21 (censored as answered), L23 and L55 (the treatment changed who is observed), L33 (variance beyond
sampling error), L39 (an effect held flat along a state every target unit moves through: the settled-level and
transport cards), N01 (an enlarged load or contract assumed to scale in proportion: the margin card), N04, N05 and
N34 (a fitted form carried to a new range: the range card), N08 and N19 (transport assumed), N12 (a season's rate
carried, near). From the client's hardest examples: L59 and L60 (a stream extrapolated from its own history, one
hazard for every cohort: the young-cohorts card), L61 (today's level taken as normal where the option removes what
produced it: the projection card), L64 to L66 (a deepening habit read off a cross-tab, held flat or sized at
today's volumes: the repeated-exposure and projection cards), N41 (an order loss assumed, never measured: the
credit card).

**Next to a card** (a WARN as the deciding lesson, answered in the note): L40 (an uplift carried to a unit near the
outcome's bound, transport), L42 (a response capped where the obvious channel stops, the range card), L43 (a lost
attribute rebuilt by a calibrated rule, the calibration card), L44 (level and mix from two sources, the
completeness card), L41, L45 and L37 (a held-out error or a back-test that cannot see the condition, the card for a
score on the choosing data), N02, N17 and N38 (a planned change or a shared capacity left out of the forward
window, the projection card), L56 to L58 and N40 (recording effects kept as a sensitivity, cut at a threshold, read
one at a time, or left unresolved between two arms: the completeness and calibration cards).

**Open**, with the runs' losses behind them:
- **The assumption named and waved through**, where the assumption is not a card's: N09 the current topology or
  membership assumed for all history (an energy run, task13 arch 3); N10 missing periods carried at the observed
  rate; N11 a passed inspection or test taken to certify the unit; N13 the latest rate taken as the state at the
  decision date; N14 a second record set aside once its linkage check failed; N03 and N18 works and timings assumed
  to happen as before (L46: pending closes carried on their expected dates); N07 an ordering or pairing assumed
  without a crosswalk; N16 a post-treatment modifier taken as stable; N33 a unit that stops taken as gone; N36 rival
  explanations named and left untested.
- **A generating process the published formula assumes**: L22 (example 9, the board estimated from the data).
- **A shallow path that passes a check of the wrong kind**: L26 to L31, and the common-error benchmark (an agreement
  between two estimates that share one error; common_error_benchmark), L51 (the most rigorous standard design built
  on comparison units whose own seasons differ).
- **Dismissed own evidence** (L01 to L07, L38, L47, L48, L56, L62, L65): a class, not a lesson; it prices whatever lesson
  the evidence carries. The evidence a run measures and sets aside is almost always a second record at another grain,
  and the commonest form on the client's hardest examples is the signal kept as a sensitivity check ("sensitivity
  analysis, not a uniquely identified correction"): the run will not commit a correction it cannot see identified,
  so the open stump is one the pack identifies and the run has to build the estimator for.
- **The unfinished chain** (L49, L53, L60, L63, L67): one step found and fitted, the next input left as it stood; or
  the label's selection seen and nothing estimated. It prices a build only where the steps are independent, so the
  run that finds one lands on a different wrong answer (example 16: the decay found, today's hours kept, Band 4).
- **The retreat** (L43, L44, N32): where the answer needs a bridge built from a second record, the run defers, calls
  the figure not calculable, or computes the bound and sets it aside. Open as a kind of loss, priced only when the
  prompt asks for a committed figure and the files support the bridge, and only where the bridge is more than one
  calibration factor.

## 3. What the four approved builds teach, and what no build may copy from them

The approved Sulfur builds (`fingerprint/corpus/approved.json`): task6 v7 (Rotalinha's latency error budgets),
task457 (Marrowfield's conflict-of-interest docket, uploaded as task14 architecture 1), task2 v6 (Larkmoor Speech's
heavy-correction ceiling for Shannonside's 2027 schedule) and task14 v3 (Penmarra's bond-based private rents measure).
Their skeletons share nothing (`skeleton.py selftest` holds the four pairs apart). Their anatomy, which is a set of
lessons about where difficulty lives and never a chain to copy:

1. **The estimand is a quantity no record holds.** A service's latency over all requests from spans kept by sampling
   another service set; a member's 2026 payments from self-reports that saw only what was paid before the filing day;
   a 2027 deployment population's error tail from people who mostly have not used the system; the rents payable on
   dwellings already let, from a register that records rents at entry and rises only by choice.
2. **Several partial instruments see the same quantity, each with a different blind spot, and the work is assigning
   each part of the estimand to the instrument that sees it.** task14: the register at entry and by choice, the
   operators completely, the panel quarterly for a sample that never held the operators' blocks. task2: the volunteers
   (self-selected), the smaller hospitals' whole staffs (compelled, elsewhere), the movers (the place's own effect).
   The runs lose by taking the instrument closest in appearance (the compelled clinicians, task2 R4), the one most
   complete in rows (the register as it stands, task14 R7), or the one the textbook method uses (the unit's own strata,
   task6 L08), and by checking it with a hold-out from the same instrument, which cannot see its blind spot.
3. **The target reaches units or periods no instrument covers** (the starters, the December quarter, the unpublished
   year, the retention gap), so a check on the observed data passes by construction.
4. **The corrections are needed together and the shortcuts file different wrong answers** (task2: four wrong calls;
   task14: twelve shortcuts on ten wrong December figures), and every misleading pattern runs across the data as the
   process makes it.
5. **The prompt says why the answer must be an estimate** (task457's approval turned on it) and asks for composite
   results, never the intermediate quantity a method would name.

**The three approved sheets of 2026-11-14** (`guidelines/client/approved-reviews-2026-11-14.md`; other fellows'
tasks, rewards 22, 17 and 35 on the review's strongest run; `../SKILL.md` Part 1d) have the same anatomy and add
three things to it:

6. **The problem is in plain sight and the estimator is the work.** The run that scored 17 wrote down that the
   labelled rows are mostly the bad outcomes and then filed nothing; the run that scored 22 built a triple difference
   with a placebo. Neither lacked a fact. Each lacked a construction: the unlabelled share re-estimated per arm from
   signals every unit carries, the treated units' own earlier seasons by the state that sizes the season.
7. **A referee slice rules between estimators.** A random labelled pilot in one arm, a dated item on two of three
   conditions, two earlier years with no treatment: the golden reproduces it, each rival misses it by a computed
   figure, and it does not cover the target. That is what the reviewer's "the data forces" rests on.
8. **The correction's own check breaks somewhere.** Netting was confirmed by timing on two conditions, bounded on the
   third and overturned for the older group, so the sentence that names the correction leaves most of the work.

**All seven approvals decide on the observation process; our send-backs for difficulty decided on mechanisms of the
world.** Read against the dimensions of Part 5: the rows that name what a record cannot hold (triangulating
instruments, hidden state, the recording algorithm, a balance's residual) are where a member can be opened; the rows
that are physics or algebra on shipped inputs (position on a network, a nonlinear functional of a path, aggregation
algebra, lumpy capacity) were computed by the runs as the field's textbook chain (task22 arch 1 and 2, task25's audit
run, task7 arch 12) and carry supporting results only.

**The page has since closed the anatomy's commonest corrections.** The read of 2026-11-21 lists a completeness
gross-up from an independent source, a bias calibrated on checked cases, a basis restated and the treatment changing
who is recorded as lessons already used, the calibration card on ten accepted tasks. So the anatomy is still where
members open, and its estimator must be more than one of those fixes (`../SKILL.md` Part 1d): the share or the bias
has no checked sample that hands it over and is identified from structure; two or more recording effects are tangled
with each other and with who the units are; the record is an algorithm's output inverted with the unit's own state;
the sources are assigned part by part and the overlap that would calibrate one is itself selected.

What may not be copied: the chain, the order, the file roles or the decision form of any of them, ours or the three
sheets' (corpus ids `review:2d1b99c1`, `review:52ab454f`, `review:d311cbf0`). task14's register
plus panel plus migration plus nowcast, task2's volunteers plus compelled staff plus movers plus ramp, task6's sampled
spans plus retention plus dated causes and task457's self-reports read to the filing day are each one skeleton on
file; the guard refuses a severity 1 to 3 match and a lesson they now teach a third time. Three of the four decide on
lessons the page has since closed or put near (task2's transport, closed; task14's rises a register sees only by
choice, closed on the completeness card; task6's design weights, near the occurrences card; task457's record read
as of its date, near the completeness card): they were accepted before the cards, and a new draw on them is refused
or answers a WARN.

## 4. The client's three hardest examples: the difficulty to match, never the chain

`guidelines/client/examples/1.txt` (a retailer's falling margin per order, runs averaging 0.26), `16.txt` (a
counselling program's committed-hours band, 0.285) and `17.txt` (a relief scheme costed from a survey, 0.31) are
the three the author shared as the library's hardest with the phase 2 guidelines. The announcement that shipped them says "Do NOT just copy them, they are likely
already overused stumps", and two of the three decide on closed cards (repeated exposure with a held-fixed
projection; young cohorts with a held-fixed projection). Their skeletons are on file as `example:1`, `example:16` and `example:17`
and the guard refuses a reskin. What they show about the kind of task wanted:

1. **Two or three decisive steps, each needing its own fitted model, on different records.** A cohort return share
   fitted for cohorts with little history and a censored fit of hours on a queue-pressure measure; a recording
   effect by days to a deadline, a second by interview length in a joint fit, a pull fitted across two start arms.
   None is one cross-tab, one filter or one document, and none borrows another's output.
2. **Each step moves the answer on its own, and the page says so with figures.** "With the decay found and the
   pooled hours kept, the call is Band 4 ... the call is Band 6." "Leave out any one correction and the cost is
   still 19.6 to 21.4 million, over budget; leave out any two and it drops to 16.1 to 17.6 million." Both patterns
   are accepted: every single drop on a different wrong call, or a call that needs the corrections together. Either
   way each step moves a graded figure alone.
3. **Naming the step leaves the work.** The page argues for each step why the sentence is not enough: equal-age
   comparison, a fitted lifetime share and a lag profile; a pressure measure built, fitted with open cases censored,
   shown to beat the calendar, and the option's terms argued to remove it; each correction "estimated and shown to
   change the total".
4. **The proof that the signal is what the golden says it is sits in the pack.** Recording, not real arrears: the
   qualifying share rises across the deadline bands within the households that say they are falling behind while
   their share of the sample stays flat. The queue, not the calendar: the slope is the same within and between years
   and the calendar term is nil once pressure is in. This is the referee of `../SKILL.md` Part 1d in another form:
   a relation the rival explanation cannot produce.
5. **The runs lost one move short of fitting** (L56 to L67): the signal seen and kept as a sensitivity; a threshold
   cut for a model; two tangled effects read one at a time; an arm picked or the question left open where a joint
   fit answers it; the mature figure computed and set aside; a stream extrapolated from itself; today's level taken
   as normal. On example 16 thirteen of sixteen runs never left the series, and the one that found the first step
   landed on a different wrong band.
6. **The shallow steps are named and carry little.** A cap stated in the schedule, open cases the dictionary says
   are to date, decliners given a modelled chance (R94 to R96): every run made them, and the page says so.
7. **The prompt asks for the steps' answers as quantities the decision uses.** "How many in-scope housing and
   insolvency referrals we'll get each year, and the hours a case of each kind will take from start to finish under
   the new agreement"; "the number of qualifying households, the amount owed ... and the cost, for the whole country
   and for each region", with "show how you got from the data to each figure". No method is named and nothing warns.
8. **The honest margin is stated.** Example 16 names its most arguable figure and the thinnest margin (0.9 per
   cent), and example 17 the range every valuation variant gives. A build states the same in its Step-by-Step.

## 5. The open dimensions: where to look for the deciding lesson

The page's six families are about inference on who and when, on how a record was made, and on five model choices.
Real analysis has other dimensions, none on the page, most untaught on file (`skeleton.py open`). Each is a **kind of
judgment**, to be built from the world's own process, with the runs' loss class it invites. Draw the deciding lesson
from here, never the shape.

| Dimension | The judgment | Where it lives in real data | The hurried failure | Keys in skeleton_vocab.json |
|---|---|---|---|---|
| Conservation and balance | An account the physics or the books must close (energy, mass, cash, headcount) whose residual is the quantity wanted, reconciled with each instrument weighted by its own accuracy | meter hierarchies, plant and network energy balances, material balances, general ledgers | stops at the first reconciliation that closes; plugs the residual into one line; never checks the residual's sign or physics (self-confirming check, dismissed own evidence, L48) | stock_flow_accounting, unmetered_component, conservation_residual_attribution |
| Structure that changes | The units' membership in a parent (feeder, territory, portfolio, hierarchy) changed over the history, rebuilt from the dated operations record and checked against the flows the changes moved; a term ended by another unit's event, terms reset at maturity | switching logs, re-territorialisations, re-parented accounts, org charts, network reconfigurations, funds and contracts | today's structure for all history (N09), the operations log set aside once its keys fail to match (N14), expected dates carried (L46) | time_varying_membership, term_ended_by_another_units_event, terms_reset_at_maturity, scheduled_completion_slippage |
| Aggregation algebra | The quantity is not additive across its parts (a coincident peak, a maximum, a quantile, a ratio of sums), so it is computed on the joint path, never summed or averaged across parts | peaks of feeders, portfolios' tails, network delays, capacity on shared resources | sums of the parts' own peaks or quantiles; averages of ratios (method shortcut) | non_additive_aggregation, asynchronous_measurement_covariance |
| Where along a network | The same load or fault has a different effect by its position on a radial or graph structure; standards with no common item linked through the raters two of them share | feeders and pipelines, supply chains, communication networks, examiners and moderators | one equivalent factor per network calibrated on an old spatial mix (N04, method shortcut); each standard read on its own scale | position_on_network_effect, local_standards_linked_by_shared_raters |
| Hidden state and dynamics | A state no record holds (a stock, a temperature, a queue, a charge level, what a cache served) rebuilt from the flows and the rules that move it, with its lags; a pool of stopped units that returns; two processes told apart by the state one depends on | storage, thermal plant, inventories, backlogs, caches, subscriptions | instantaneous mapping from input to output, or the latest level carried (N13); a stop read as an end (N33) | stock_flow_accounting, latent_structure_estimation, served_state_outlives_source_failure, stopped_units_return, rival_process_by_state_dependence |
| The recording algorithm | The record is an algorithm's output (exception reporting, estimation and editing, rolling registers, billing cycles), so the work inverts the algorithm before measuring. Next to the completeness card: open only where the inversion needs each unit's own state and is not a share applied to a count; never decided by reading one flag | meter data management, plant historians, billing systems, survey processing, app store receipts | the stored values taken as observations at the stored times (method shortcut); a single gross-up factor (the card) | record_algorithm_inversion (near) |
| Recording effects tangled together | The outcome is recorded less often under two or more conditions of how the record was made, tangled with each other and with who the units are, so each is fitted in one model and proved against a signal the conditions cannot move. Taught once (example 17), next to the completeness card: open where the estimator is the joint fit, never one factor | fieldwork, inspections, triage, logging under load | the signal kept as a sensitivity (L56), a threshold cut (L57), one effect at a time (L58) | recording_effects_separated_jointly (near), starting_point_anchoring (near) |
| Supply the outcome sets | The delivery, spend or supply a response is measured against was itself set by the outcome (an auction, a rationing rule, a cut made where demand was weakening), so the response is identified from an outside instrument | ad auctions, allocated inventory, rationed services | the response regressed on the delivered quantity (method shortcut) | endogenous_supply_instrument, instrument_noncompliance |
| One experiment, several readers | A test withholds an input from one consumer while a failure takes it from all of them, so each reader's loss is built from its own record | shared feature stores, shared services, shared plant | the experiment's effect read as the whole cost (unfinished chain) | experiment_reaches_one_reader |
| Triangulating instruments | Several sources with different blind spots measure one quantity; each part of the estimand is assigned to the source that sees it | the approved builds' anatomy (Part 3); any register beside a panel, a meter beside a model | the closest-looking or most complete source; a hold-out from the same source (narrow look, self-confirming check); a deferral where the bridge has to be built (L43, L44) | any, as the anatomy around new lessons; level_and_mix_from_two_sources and calibrated_proxy_for_lost_attribute are near cards, and an overlap that hands over one calibration factor is the calibration card |
| A benchmark that shares the error | The check an estimate is held against carries one of its errors, so their agreement validates nothing and the benchmark's own gap is sized from a third source | two registers fed by one notification, a model checked against its own training feed | agreement taken as validation (self-confirming check) | common_error_benchmark |
| Support and units of account | A peak, a variance or a rate depends on the interval or unit it is integrated over, so the record's grain is carried to the decision's | 15-minute against hourly demand, block against point, per dwelling against per person | the record's grain taken as the decision's (method shortcut) | support_effect |

**Rows the page has taken or put next to a card** (a supporting step, or a WARN to answer; never drawn as the
deciding lesson on their own):

| Was listed as open | Now |
|---|---|
| Nonlinear functionals of a path (nonlinear_functional_of_path) | next to the margin card: open only where the work is not fitting a curve and valuing a change at its point (a loss convex in a rate whose record is itself distorted by the rate is a recording problem first) |
| Lumpy and joint decisions (marginal_not_average, queue_or_capacity_replay) | marginal_not_average is closed on the margin card; a queue replay is next to the projection card |
| Where the target leaves the support (extrapolation_beyond_observed_range, second_channel_past_plateau, validation_cannot_see_condition, bounded_outcome_headroom) | the range card closes the first; the others are next to the range card, the card for a score on the choosing data and transport |
| A response measured (behavioural_response_measured, response_at_crossing_point, fixed_nuisance_component, lot_size_cycle_stock) | next to the margin card |
| A filed change to the forward window (forward_window_structure_change) | next to the projection card |

A dimension does not price a result on its own: the runs model what one plot shows, run the field's textbook method
and back-test by reflex (`precedents.json` reflexes R01 to R97). A dimension prices a result where the world's own
process makes the hurried route pass its own checks (the reconciliation closes, the back-test on the record holds)
and only a check of another kind refutes it, with a precedent id for the kind of loss.

**Dead as a deciding lesson: a record to be found, merged or re-keyed.** task1 architecture 4 (an audiobook app's
lead plan, sent back at stage 4 on 2026-11-12 and retired) put its call on two record-handling corrections: a second
log that held exactly the rows the primary log lacked (a coverage gap, remedied by a union) and a current roster
standing in for a dated one (remedied by walking the charges' member lists). The judge's own first pass, written
before it saw the answers, made both by reflex and landed the graded figures, and Gate G read the pair as a
planted_defect_flip. Whatever key it is labelled with (unmetered_component, exposure_seen_only_in_linked_record,
time_varying_membership, linkage), a deciding lesson whose remedy is a join, a union or a re-key fails the client's
clean-data test (the page of 11/20: "a solver that cleans the data perfectly and reads every instruction correctly
should still be able to reach the wrong answer through a reasonable but insufficient analysis"): with every file
complete and correctly keyed the call is arithmetic. Such corrections are Layer 1 or an assembly result, never a
priced result. Before a card is drafted, run three screens on paper: the clean-data test (every file complete and
keyed, the call still needs a modelling judgment the reflexive method gets wrong); the reflex screen (each
careful-run reflex in precedents.json R01 to R97 executed perfectly lands outside the band); the compound hint (the
best two-move sentence rescues a third of the results or fewer, so three or more independent judgments graded in
different results).

## 6. How the next draw uses this

1. Run `skeleton.py closed` and `skeleton.py open` before the chain is written, and `skeleton.py lessons --min 1`
   for what is already taught.
2. Choose two or three decisive steps from the open ground (Part 2's open losses, Part 5's dimensions), each with
   its own records and its own estimator, none of them a closed card's fix (Part 1's table of fixes), and at most
   one of them next to a card. They are independent in the client's sense: no sentence names two, and each owns a
   figure the prompt asks for in the decision's words.
3. Keep any closed lesson as a supporting step whose omission alone leaves the golden call standing: `effort.json`
   routes carry that route and its answer, and `checks.py` asserts it.
4. Write the Frontier check's `Closed strategies:` line (the deciding lessons and why none is on the page, the
   nearest card for each and how the mechanism or the fix differs, every closed lesson the chain carries and the
   route showing it alone does not flip the call) and its `Decisive steps:` line (each step's own figure, the
   prompt's words that ask for it, where its evidence sits, and the figure and the call with each step left out
   alone and in pairs).
5. Borrow the approved anatomy (Part 3: a quantity no record holds, instruments with different blind spots, a target
   no instrument covers, an estimator to construct, a referee slice, a check that breaks on some members) and the
   hardest examples' profile (Part 4: each step its own fitted model, the proof in the pack, the steps' answers
   asked for as quantities), never an approved chain and never an example's.
