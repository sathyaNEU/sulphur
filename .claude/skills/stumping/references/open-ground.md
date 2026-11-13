# The open ground: what the client has closed, where the runs still lose, and where to build next

The client's Overused stumping strategies page (`guidelines/client/learning-modules/overused-strategies-2026-11-12.md`)
closes 34 lessons, each already deciding two or more accepted tasks. This file reads our own run record and the
four approved builds against it and names the ground that is still open. `../SKILL.md` Part 1c holds the rule; this
file holds the evidence behind it. `python3 .claude/skills/fingerprint/skeleton.py closed` prints the page as the
guard holds it and every card on file against it.

## 1. What the page closes, and the three rules that come with it

The five families and their 34 cards, as lesson keys in `fingerprint/skeleton_vocab.json` `closed_lessons`:

| Family | Closed (lesson keys) |
|---|---|
| Who ended up in the data | regression to the mean (selection_on_peak_baseline, normal_period_correction); survivorship (survivor_selected_sample); outcomes hidden by the intervention (intervention_masks_outcome); self-selection, compare a unit with itself (self_selection_into_treatment); rows are occurrences (length_biased_sampling) |
| Noise and small numbers | shrinkage (shrinkage_small_samples, selection_on_noisy_means); clustered outcomes (uncertainty_at_shared_unit, serial_or_common_shock_dependence); units vary beyond the stated error (variance_beyond_sampling_noise); a noisy regressor flattens the slope (measurement_error_attenuation, errors_in_covariate); chance coincidences, a placebo baseline (chance_coincidence_baseline) |
| Time, follow-up and timing | censoring (open_follow_up_censoring, completion_of_young_cohorts); competing risks; late entry and immortal time (left_truncated_ages, immortal_time_exposure); an early spike, the settled level (effect_fade_with_time); reporting lag (reporting_lag_nowcast); repeated exposure (repeated_exposure_response); values at a limit (censored_or_capped_observation); young cohorts at matched age (vintage_or_cohort_drift); payback (rebound_after_window); the easy cases used up (depleting_stock_of_easy_cases) |
| Carrying an effect to a new place | the pooled effect does not transfer (transport_effect_modifiers, heterogeneity_carried_to_decision); spillover (interference_spillover); gains taken from neighbours (displacement_netting, cannibalisation_with_pretrend, downstream_offset); assignment odds by group (assignment_odds_by_group); composition (composition_versus_behaviour); a closed unit's demand (closure_diversion); a fixed-count effect rescaled (fixed_count_effect_rescaled) |
| How it was measured or recorded | the instrument changed (measurement_basis_break); the survey changed (survey_design_change); fieldwork seasons (fieldwork_season_mix); billed where, not lived where (recorded_at_billing_location); dependent capture (dependent_capture_channels); a co-occurring change (concurrent_change_in_comparison); hindsight (hindsight_in_evaluation) |

`closed_near` keys twelve more lessons that share a card's family (design_weights next to the occurrences card,
pilot_unrepresentative_selection and customer_specific_response next to transport, device_clock_drift and
detection_rate_changes_outcome next to the instrument change, and so on). A call that turns on one of them is a WARN:
the note says how the mechanism or the fix differs from the card.

The rules, the page's own words: **same lesson means same fix** ("same mechanism and the same kind of fix counts as
the same lesson; changing the domain, the dataset or how the problem is detected does not make it new");
**supporting steps are fine** ("it cannot be the step that flips the answer"); **stacking two of them is not new**.
And beyond the list: a single planted factor, applying a stated rule, reading a field and a hindsight replay are
never accepted as the deciding step, and two tasks may not analyse the same records (a shared public release is fine
only on different records).

What this does to `../SKILL.md` Part 1b's six places runs lose: three are now closed as deciding lessons (the split
carried to the decision is the transport card; units selected by the outcome's history are the regression,
survivorship and intervention cards; the system's net is the neighbours card). The other three remain open as
**kinds of loss**, and the page says nothing against them: the assumption a run names and waves through (as long as
the assumption is not one of the cards'), a response measured and the marginal unit, and a shallow path that passes
its own checks.

## 2. Where our runs lost, read against the page

`precedents.json` holds 38 losses and 19 named assumptions in the runs' own words. Read against the page:

**Now closed as the deciding lesson** (still citable for a supporting step):
L08 (inclusion probability another unit set, near the occurrences card), L09 to L12 and L25 (the split not carried;
vintages pooled), L14 (selected survivors), L16 and L18 (the unit priced alone; not-yet-treated taken as untreated),
L19 and L35 (default or independence errors where units share the cluster or the shock), L20 (attenuation), L21
(censored as answered), L23 (who is observed changed, near), L33 (variance beyond sampling error), N08 and N19
(transport assumed), N12 (a season's rate carried, near).

**Open**, with the runs' losses behind them:
- **The assumption named and waved through**, where the assumption is not a card's: N09 the current topology or
  membership assumed for all history (an energy run, task13 arch 3); N10 missing periods carried at the observed
  rate; N11 a passed inspection or test taken to certify the unit; N13 the latest rate taken as the state at the
  decision date; N14 a second record set aside once its linkage check failed; N01 an enlarged load or contract
  assumed to scale in proportion; N02, N06 and N17 the history assumed informative, or a planned change left out of
  the forward window; N03 and N18 works and timings assumed to happen as before; N04 and N05 a fitted form carried
  to a new range; N07 an ordering or pairing assumed without a crosswalk; N16 a post-treatment modifier taken as
  stable.
- **A response assumed, a marginal unit averaged**: L15 (assumed smooth instead of measured), L17 (the average unit
  where the decision buys the marginal one; marginal_not_average is taught twice in the client's corpus, so it is a
  supporting step), L24 (one shared coefficient where units respond in opposite directions, near the transport card).
- **A generating process the published formula assumes**: L22 (example 9, the board estimated from the data).
- **A shallow path that passes its own checks**: L26 to L31 and L37, above all L37 (a pooled factor certified by a
  held-out error that cannot see the condition; validation_cannot_see_condition) and the common-error benchmark (an
  agreement between two estimates that share one error; common_error_benchmark).
- **Dismissed own evidence** (L01 to L07, L38): a class, not a lesson; it prices whatever lesson the evidence carries.
  The evidence a run measures and sets aside is almost always a second record at another grain.

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

What may not be copied: the chain, the order, the file roles or the decision form of any of them. task14's register
plus panel plus migration plus nowcast, task2's volunteers plus compelled staff plus movers plus ramp, task6's sampled
spans plus retention plus dated causes and task457's self-reports read to the filing day are each one skeleton on
file; the guard refuses a severity 1 to 3 match and a lesson they now teach a third time. Two of the four (task2's
transport, task6's design weights) decide on lessons the page has since closed or put near: they were accepted before
it, and a new draw on them is refused.

## 4. The open dimensions: where to look for the deciding lesson

The page's five families are all about inference on who and when: who is in the data, how noisy it is, when it was
observed, where an effect is carried, how it was recorded. Real analysis has other dimensions, none on the page, most
untaught on file (`skeleton.py lessons`). Each is a **kind of judgment**, to be built from the world's own process,
with the runs' loss class it invites. Draw the deciding lesson from here, never the shape.

| Dimension | The judgment | Where it lives in real data | The hurried failure | Keys in skeleton_vocab.json |
|---|---|---|---|---|
| Conservation and balance | An account the physics or the books must close (energy, mass, cash, headcount) whose residual is the quantity wanted, reconciled with each instrument weighted by its own accuracy | meter hierarchies, plant and network energy balances, material balances, general ledgers | stops at the first reconciliation that closes; plugs the residual into one line; never checks the residual's sign or physics (self-confirming check, dismissed own evidence) | stock_flow_accounting, unmetered_component, conservation_residual_attribution |
| Structure that changes | The units' membership in a parent (feeder, territory, portfolio, hierarchy) changed over the history, rebuilt from the dated operations record and checked against the flows the changes moved | switching logs, re-territorialisations, re-parented accounts, org charts, network reconfigurations | today's structure for all history (N09), the operations log set aside once its keys fail to match (N14) | time_varying_membership, unit_identity_across_systems |
| Aggregation algebra | The quantity is not additive across its parts (a coincident peak, a maximum, a quantile, a ratio of sums), so it is computed on the joint path, never summed or averaged across parts | peaks of feeders, portfolios' tails, network delays, capacity on shared resources | sums of the parts' own peaks or quantiles; averages of ratios (method shortcut) | non_additive_aggregation |
| Nonlinear functionals of a path | The outcome is a convex or threshold function of the load path (losses with the square of current, ageing exponential in temperature, a charge on the maximum, a penalty above a line), so the mean in gives the wrong answer out | conductor and transformer losses, insulation ageing, demand charges, service-level penalties | the function applied to averages, or a percentage carried from another load level (N01, method shortcut) | nonlinear_functional_of_path |
| Where along a network | The same load or fault has a different effect by its position on a radial or graph structure (voltage drop and losses grow with distance, delay with hops) | feeders and pipelines, supply chains, communication networks | one equivalent factor per network calibrated on an old spatial mix (N04, method shortcut) | position_on_network_effect |
| Hidden state and dynamics | A state no record holds (a stock, a temperature, a queue, a charge level) rebuilt from the flows and the physics that move it, with its lags | storage, thermal plant, inventories, backlogs | instantaneous mapping from input to output, or the latest level carried (N13) | stock_flow_accounting, latent_structure_estimation |
| The recording algorithm | The record is an algorithm's output (exception reporting, estimation and editing, rolling registers, billing cycles), so the work inverts the algorithm before measuring; never decided by reading one flag | meter data management, plant historians, billing systems, survey processing | the stored values taken as observations at the stored times (method shortcut); guard against data semantics: the inversion must take estimation, not one field read correctly | record_algorithm_inversion |
| Triangulating instruments | Several sources with different blind spots measure one quantity; each part of the estimand is assigned to the source that sees it and the overlap calibrates the rest | the approved builds' anatomy (Part 3); any register beside a panel, a meter beside a model | the closest-looking or most complete source; a hold-out from the same source (narrow look, self-confirming check) | any, as the anatomy around new lessons |
| Lumpy and joint decisions | Capacity comes in units, constraints bind jointly, costs are asymmetric, so the decision's marginal unit and its option value drive the call | crews, transformers, contracts, sweeps under a cap | the average unit, the unconstrained optimum rounded (method shortcut) | marginal_not_average (taught twice: supporting), queue_or_capacity_replay |
| Support and units of account | A peak, a variance or a rate depends on the interval or unit it is integrated over, so the record's grain is carried to the decision's | 15-minute against hourly demand, block against point, per dwelling against per person | the record's grain taken as the decision's (method shortcut) | support_effect |

A dimension does not price a result on its own: the runs model what one plot shows, run the field's textbook method
and back-test by reflex (`precedents.json` reflexes R01 to R37). A dimension prices a result where the world's own
process makes the hurried route pass its own checks (the reconciliation closes, the back-test on the record holds)
and only a check of another kind refutes it, with a precedent id for the kind of loss.

**Dead as a deciding lesson: a record to be found, merged or re-keyed.** task1 architecture 4 (an audiobook app's
lead plan, sent back at stage 4 on 2026-11-12 and retired) put its call on two record-handling corrections: a second
log that held exactly the rows the primary log lacked (a coverage gap, remedied by a union) and a current roster
standing in for a dated one (remedied by walking the charges' member lists). The judge's own first pass, written
before it saw the answers, made both by reflex and landed the graded figures, and Gate G read the pair as a
planted_defect_flip. Whatever key it is labelled with (unmetered_component, exposure_seen_only_in_linked_record,
time_varying_membership, linkage), a deciding lesson whose remedy is a join, a union or a re-key fails the
clean-data test: with every file complete and correctly keyed the call is arithmetic. Such corrections are Layer 1
or an assembly result, never a priced result. Before a card is drafted, run three screens on paper: the clean-data
test (every file complete and keyed, the call still needs a modelling judgment the reflexive method gets wrong); the
reflex screen (each careful-run reflex in precedents.json R01 to R37 executed perfectly lands outside the band);
the compound hint (the best two-move sentence rescues a third of the results or fewer, so three or more independent
judgments graded in different results).

## 5. How the next draw uses this

1. Run `skeleton.py closed` and `skeleton.py lessons --min 1` before the chain is written.
2. Choose the lesson the call turns on from the open ground (Part 2's open losses, Part 4's dimensions) with no
   carrier on file, and at least two more independent judgments, at most one of them closed.
3. Keep any closed lesson as a supporting step whose omission alone leaves the golden call standing: `effort.json`
   routes carry that route and its answer, and `checks.py` asserts it.
4. Write the Frontier check's `Closed strategies:` line: the deciding lesson and why it is not on the page, every
   closed lesson the chain carries and the route showing it alone does not flip the call.
5. Borrow the approved anatomy (Part 3: a quantity no record holds, instruments with different blind spots, a target
   no instrument covers), never an approved chain.
