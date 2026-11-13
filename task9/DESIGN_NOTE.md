# task9: what drove Varnholt Halbleiter Fab 2's June to September sort-yield shortfall, and what VR90 will yield at sort in Q1 2027 under the ramp plan as filed and with the changes it needs

## Draw

Subdomain: General Statistics & Data Science, Interpretability (feature attribution and mechanistic analysis: a yield
  shortfall attributed across interacting process features to the mechanisms that carry it, each mechanism's
  consequence carried to a new product's die and the ramp quarter's operating conditions)
Analysis type: Root-Cause Analysis, ending in a forecast for the new product's ramp
Answer shape: ranked causes with their contributions: the June to September shortfall bridged from January to March in
  good die per VX40 wafer, each cause named with its fix, then VR90's Q1 2027 sort yield from its own entitlement
  through each cause's cost under the ramp plan as filed to the plan's yield and the recommended plan's yield, with
  the wafer starts the Q1 commitment needs.
Weight: investigation. Most of the work is finding five causes that landed in the same months across about twenty-five
  related files (a slurry loop's facility trend and line list, a wet bench's event log and lab samples, a film's
  49-site maps and a recipe log, an etch chamber's per-wafer RF record and daily monitor wafers, the sort database),
  each against the rival its first trace suggests; none of the last three builds (task22's assembly, task16's
  validation, task7's hard-to-measure quantity) put its weight there.
Data-native sentence: the sort records see every cause only as fail bins on die, the polishers, benches, chambers and
  the slurry loop each keep their own logs at their own grain and clock, and the product the ramp needs has never been
  sorted, so each cause has to be found where its physics leaves a trace (a loop's taps, a film's thickness budget, a
  bath's chemistry, a chamber's polymer load) and carried to a die nearly four times the size.
People: Gitte Ullrich (yield engineering lead), Matthias Hertrampf (CMP module engineer), Sofia Sorgatz (facilities,
  slurry and chemical distribution), Hüseyin Siering (wet process engineer), Detlev Lindau (etch module engineer),
  Isabelle Hamann (operations planning, owner of the ramp plan), Gunhild Scheibe (fab controlling, owner of the cost
  inputs), Oswald Dobes (analytical lab); drawn with guard.py names --geo "Germany, Saxony" --seed 9033.

1. Fit: the client's direction for the domain is the regression split across changes that shipped together and a
   root cause tested against its rivals; the draw takes no client chain (skeleton check: severity none against every
   card, lineage entry and client task).
2. Task type: Interpretability, the General Statistics task type that serves Root-Cause: attribution across
   interacting features, a mechanism's dose on its true exposure and a yield read at a new support are its own objects.
3. Data: generated, simulating the fab's process (lot starts for three products and a test vehicle, dispatch with bay
   affinities and tool downtime, an oxide slurry loop whose large particles grow with residence time to each tap, a
   pre-gate bench whose metals build up between spikes and changes, a deposition chamber's new showerhead and a
   polisher's edge-zone tune, contact-etch polymer by RF time and recipe chemistry, clustered random defects, a sort
   program that bins each die on its first failing test, metrology, inspection and e-test sampling plans).
4. Decision: the changes the VR90 ramp plan needs and the yield and wafer starts the plan should carry, at the ramp
   readiness review on 24 November 2026; backward on the June to September causes, forward on VR90's Q1 2027 quarter.
5. Shell: question form which; a spreadsheet and a short note for the ramp review (xlsx and docx).
6. Card: shape 03, gap objective then time, generators G7, G4, G2, G3, Gate G forecasting, calibration form
   gold_standard_subsample (the 49-site maps, the lab's investigation samples and the daily monitor wafers against the
   routine instruments), context artifact capacity_report (the ramp plan), forum committee_or_panel (the ramp
   readiness review), forcing event purchase_order_or_contract (the Q1 2027 supply commitment), organisation
   manufacturer, role field_unit_lead, strategy forecast_method_backtest.
7. Guard: WARN only: template.chain_near (task18 ranks an island grid's disturbance losses in an investigation; here the
   ranking is a bridge in good die carried into a new product's forecast, and the skeletons share nothing),
   skeleton.house_lesson (stock_flow_accounting on mark120 and task20: here the stock is a bath's metal content rebuilt
   from drag-in, spikes and changes and checked on the lab's investigation samples, one of five lessons).
8. Slot: architecture 1 (Concept 1) is spent and architecture 2 (Concept 2, the edge ring) superseded, both in the
   card's lineage; this draw changes the world, the company, the pack, the deciding lessons, the decision form and the
   shell.

## Deep reasoning

Task type: Interpretability (feature attribution and mechanistic analysis), serving Root-Cause Analysis: the shortfall
  attributed across interacting process features, each mechanism modelled on its own exposure, and carried to a new
  product's die and quarter.
Domain test: every result is the field's own statistical object: a shortfall against a baseline period on the sort
  database's die, an attribution across dependent features where a shared feed's effect grades with position and two
  features cancel on the units that carry both, a hidden stock rebuilt from its flows and fitted to its consequence, a
  wear rate identified on its true exposure against the counter that moved in step with it, and a yield read at a new
  support from block yields of the small die.
Swap: "the slurry loop's speed costs the far polishers most, the bench's metals build up between spikes, DP2B and CM3
  cancel on the wafers that run both, VR90-T's deep etch loads two chambers with polymer, and VR90's big die yields
  more than a die-area formula says" read with a hospital's or a retailer's nouns has no loop residence, thickness
  budget, drag-in and dilution, polymer per RF second or clustered defects per square centimetre to compute, so no
  result can be reached.
Where the weight sits: R2 to R5 (each cause found against the rival its first trace suggests), long because each needs
  its own file at its own grain read against the sort database's die and the lot and tool histories.
Layer 1: sort retests and partial re-probes (the tester re-probes a wafer after a probe-card clean), split and merged
  lots (engineering holds), engineering wafers in production lots, wafers scrapped before sort, each polisher's export
  in its own layout, two tools' clocks a few minutes off, the slurry loop's trend exception-reported with gaps and a
  flow unit change at a controller upgrade, back-entered PM rows, lab results below the reporting limit as text, a bench
  controller restart that repeats log lines, lot IDs in two formats after the MES upgrade; none decides a result.
Not one thing: the strongest single piece is the etch polymer's true exposure basis (R5, the largest swing in VR90's Q1
  yield under the plan); a run that nails it still has to find the loop, the bath, the cancelling pair and VR90's
  entitlement, each in its own files, and every one moves VR90's Q1 yield past its band.
One-fact test: "the contact-etch polymer builds per RF second at a rate the deep recipe nearly doubles" rescues R5 and
  part of R7, 1 of 7 results.
Not semantics: every field and unit read correctly still leaves the scratch excess on the far polishers' own
  consumables, the leakage on hours since a bath change, the edge fails on CM3's tune, the etch cleans on wafers and
  VR90 on a die-area formula.
Not rule application: no filed procedure attributes the shortfall, rebuilds the bath's metal, identifies the polymer
  load or reads a yield at VR90's die; the ramp plan states the quarter's operating conditions and nothing else.
Estimand: the prompt fixes the populations (VX40 and VP12 wafers sorted 1 June to 30 September 2026 against those
  sorted 1 January to 31 March; VR90's Q1 2027 wafers), the outcomes (good die per wafer; sort yield; wafer starts), the
  unit (good die per VX40 wafer for each cause) and the scenarios (the ramp plan as filed; the recommended changes); the
  ramp plan fixes the Q1 loading, settings and commitment.
No decoy: no memo, ticket or draft carries a cause, a share or a yield; the ramp plan states operating conditions and
  the commitment only, and no file ranks the causes.
No replay: no result re-derives a published figure; no stated number in the pack is simply wrong.
Pinned: each result's rivals are run on the clean truth at stage 2 and land inside its band or are ruled out by named
  data (the August flow restore, the P-X cycles, the lab's investigation samples, the 49-site maps, the block yields).
Run forecast: R2 stopped at the first story (the far polishers' own filters and pads); R3 method shortcut (hours since
  a bath change at the summer's loading); R4 dismissed own evidence (DP2B's thick edge set aside because its wafers
  yield well on average, then CM3's harmonisation taken as a recovery); R5 method shortcut (cleans kept on wafers, or
  scaled by RF time alone); R6 method shortcut (a die-area formula from VX40's die yield); R7 unfinished chain.
Strategy label: Splitting a regression across changes that shipped together (Machine Learning Research 2), here a sort
  yield across five causes that landed in the same months, carried into the forecast the ramp needs.
Depth level: 5: five independent judgments (R2 to R6), each needing its own files and estimation, and the shortcuts land
  on different wrong VR90 yields and different wrong change lists.
Lesson: a yield attribution is finished only when each cause is modelled on its own physics (a feed's position, a
  film's budget across two steps, a bath's stock, a polymer's true load) and carried to the new product's die and
  quarter; no build on file teaches the etch basis, the loop, the cancelling pair and the support together.

## Results chain

| ID | Result (checkable) | Area | Pinned by | Band | Hurried analyst | Depends on | Graded as |
|---|---|---|---|---|---|---|---|
| R1 | The shortfall in good die per wafer, VX40 and VP12, sorted 1 June to 30 September against 1 January to 31 March | assembly-reconciliation | the sort database's final insertion per wafer, the window and product named in the prompt | set at stage 2 | method shortcut: first insertions, engineering wafers kept | - | Ask 1 |
| R2 | The scratch cause: the oxide slurry loop's slower flow, graded by each polisher's distance along it, its cost per VX40 wafer and its VR90 Q1 cost under the plan | investigation-loops | the loop's trend and line list, the August restore, the polisher logs and sort bin 5 | set at stage 2 | stopped at the first story: CM3's and CM1's own filters and pads | independent: the loop's trend | Component 1, Ask 2 |
| R3 | The bath cause: the pre-gate bench's metal build-up under the July chemical life, its cost per VX40 wafer and its VR90 Q1 cost at the plan's loading | modeling | the bench's event log, the lab's samples, e-test leakage and sort bin 6 | set at stage 2 | method shortcut: hours since a bath change at the summer's loading | independent: the bench log | Ask 3 |
| R4 | The edge cause: DP2B's thick edge and CM3's thin-edge tune cancelling on DP2B to CM3 wafers, its cost per VX40 wafer, what the plan's CM3 harmonisation does alone, and its VR90 Q1 cost | causal-reasoning | the 49-site maps, the wafer route records and sort bins 3 and 4 | set at stage 2 | dismissed own evidence: CM3 alone, its harmonisation taken as a recovery | independent: the route records | Component 2, Ask 4 |
| R5 | The etch cause: polymer per RF second on ET1B and ET3A, its VR90 Q1 cost at the filed 2,400-wafer clean and the clean interval in VR90 wafers that holds it at today's level | forecasting | the per-wafer RF record, the PM log, the daily monitor wafers and the P-X cycles | set at stage 2 | method shortcut: cleans on wafers, or scaled by RF time alone | independent: the etch record | Component 3, Ask 5 |
| R6 | VR90's yield with none of the causes at the line's January to March performance | missingness-measurement | VX40 and VP12 die maps for January to March read in blocks at VR90's die area | set at stage 2 | method shortcut: a die-area formula from VX40's die yield | independent: the January to March die maps | Component 4, Ask 6 |
| R7 | VR90's Q1 2027 sort yield under the plan as filed and with the recommended changes, and the wafer starts for the commitment | synthesis | R2 to R6 and the ramp plan's loading, settings and commitment | set at stage 2 | unfinished chain: VX40's summer yield scaled to VR90 | R2, R3, R4, R5, R6 | Recommendation, Component 5, Ask 7 |

Carry-forward: R1 to R6 each stand on files of their own and are graded alone; R7 is graded against the golden and
falls with any of R2 to R6, so one missed cause costs its own result and R7, never another cause's result.

## Tried and rejected

- 2026-11-11, missing data, censoring and measurement error as the task type: the taxonomy has it serve descriptive work,
  monitoring and comparison, not forecasting (guard three_rules.task_type), so the forecast is drawn as a posterior
  predictive count under Bayesian modeling and posterior inference.
- 2026-11-11, Concept 3 (the speech model under the speed cap): benchmarking and ablations is task15's task type and its
  lessons sit on the client's strategies 4 and 5; Concept 1 drawn first as the author's ranking puts it.
- 2026-11-11, the hot batch read from the simulator's own window (record.py carried params' build weeks): the golden
  cannot know a window the pack does not show, so the window is found from the record by a build-week scan of the last
  year's replacements against each vault's earlier level, with nothing flagged under a likelihood ratio of 25.
- 2026-11-11, batch frailty at gamma(12) (cv 0.29) with a single-window scan: one high-frailty build batch made only the
  late weeks of the window stand out (seed 9011 found weeks 25 to 30, and 16 to 32 once the vault levels were in), so
  batch frailty is gamma(30) (cv 0.18) and the scan takes each vault's own earlier level; seeds whose scan misses the
  true window were set aside.
- 2026-11-11, the infant term fitted on half-year age bands and applied to a drive's first weeks: the band-mid covariate
  inflated the term's coefficient to about 150 times at install and put the new X-24 vaults at three times a believable
  first-year rate; the first year is now fitted in monthly bands.
- 2026-11-11, Poisson or drive-level-draw bands as the careful pass's priced loss: frontier runs bootstrap and build
  predictive intervals unprompted (precedents R04), and with each vault's level in the golden the vault-quarter residuals
  carry no extra-Poisson spread, so the interval and the back-test are not priced on clustering; they stay as graded
  results the careful pass earns, and the band's width is graded with the path.
- 2026-11-11, the migrate call for the batch as a whole (migrate if the batch's 24-month share exceeds 20 per cent): every
  route that finds the batch at all lands on "migrate", so the call priced nothing; the call is made vault by vault, where
  a vault holding a third of the batch does not pay.
- 2026-11-11, seed 9014 for the per-vault call: its vault B17 sat at 236 against the 240 line, flipping under either ramp
  shape alone; seed 9017 is the world where every vault clears the line by 10 per cent or more under every rival.
- 2026-11-11, the build window a week wider as a golden-family rival: the week-15 builds fail at 1.2 per cent a year, under
  the family's normal 2 per cent, so the data rule the wider window out; it moves to the shortcuts (it migrates B15).
- 2026-11-11, the per-vault migration call as built on seed 9017 (stage 4 judge, NOT_DETERMINISTIC, SEND_BACK): the cost
  convention was open (the YAML's drive price and "new drives" licence break-evens of 130 and 678 beside the golden's 240),
  the prompt asked one call for "its vaults", the batch vaults' levels came from their few non-batch drives (B18 at 0.93
  against its record's 0.5, B16 at 0.84 against 1.56), and the batch's noisy quarterly rate (2.3, 3.9, 2.3, 6.1, 8.3, 7.8
  per cent) leaves a plateau reading that flips the call; the judge also found the build window at once, so R2 is not a
  loss a careful run makes, and with it earned the cited pair is near 58 to 65, over the bar.
- 2026-11-11, Concept 1 as a whole (Halden Vault's drive replacements): spent at stage 4 on the judge's SEND_BACK and an honest
  pair over the bar; the author chose Concept 2.
- 2026-11-11, Concept 2's first chain of eight (the metrology's onset, the retaining ring's and the pad's terms as results
  of their own, the dose per pair as the priced loss): frontier runs rebuild every counter, fit a breakpoint and model a
  mechanism one plot shows unprompted (R08, R11, R14), so those results priced nothing; the chain was cut to seven with
  its losses on the baseline, the ring's unit of variation, the rules re-run and Rev F's steady state.
- 2026-11-11, Rev G keeping the disk inside the full PM with disk-only changes between: the full PM's free renewal makes
  the best count half the full-PM interval for both pairs whenever one change a cycle wins, the pooled textbook count
  lands within 3 per cent of it, and the high pair's choice between one and two changes flips under a 20 per cent slope;
  the spec's Rev G draft takes the part out of the full PM.
- 2026-11-11, every disk on a unit wearing at one rate: each unit's disks then follow one curve, a generator setting in
  sight, and any fit puts the retaining ring at nothing; with a lognormal spread of 0.08 the joint fit gives the retaining
  ring 4 to 7 per cent in five seeds of five (either sign) while the disk-life fit and the swaps give none.
- 2026-11-11, full PMs logged 0.3 days before the wafers polished ahead of them: the units polished during their own PMs and
  a blank counter placed by time came out a cycle early (counters 87 to 95 per cent exact); dispatch and maintenance now
  run in one time-ordered pass with downtime, partners covering, and every counter rebuilds exactly.
- 2026-11-11, onset and slope bands of 6 per cent: under the disk spread each unit's own fit sits up to 10 per cent from
  its pair's, a defensible reading of "each unit", so the dose bands are 12 per cent and the counts' 8 per cent, with the
  fleet's one count of 1,375 outside both pairs.
- 2026-11-11, Concept 2's chain as built (seven results, the careful pair priced at 38.2 on the pre-April baseline, the
  wafer-level ring share, the sliced bridge and the summer's rate): the determinism judge's blind first pass at medium
  effort made none of those moves; it measured against the fresh-disk fallout, read the ring off its residuals and swaps,
  re-ran each rule on the units' own sequences and priced Rev F at its own cycle, landing all seven results inside their
  bands, so the careful column is about 96 and the chain goes back to stage 2.
- 2026-11-11, the disk lots switching by date (every disk issued from mid-April from the new lot): the summer's own fit
  then recovered the current lot's curve without the lot ever being read, so stores issue the oldest lot first and the
  earlier lot ran beside the new one on PU-1 and PU-3 through the summer.
- 2026-11-11, a supplier's August shipment as the forward stock: a lot with a fortnight of wafers behind it leaves the
  current curve an assumption, so the forward stock is the March lot's remainder, measured on all four units.
- 2026-11-11, the ring at scale 0.32 with a cap of 0.80: the new lot's disks under the waiver reached the cap at 3,000 to
  4,000 wafers and the hinge fits came out at 425 and 890 against truths near 620 and 900; the scale is 0.22 with a cap
  of 0.92, and every lot's fit recovers its truth within 5 per cent.
- 2026-11-11, EW-118 allowing four retained disks: with four July PMs keeping their disks the March lot reached only
  PU-2 and PU-4, and the high pair's current curve rested on one disk; at two retained disks the July PMs on PU-3 and
  PU-4 fit the lot's disks, and the waiver's text is a two-PM trial of disk life.
- 2026-11-11, the rules' bridge (2,000-wafer rule, Rev F, EW-118) as a graded result: the judge's first pass on the first
  chain landed it by running each rule on the units' own sequences, so it priced nothing; it leaves the chain.
- 2026-11-13, Concept 2's chain as READY (the edge ring's six results, the conditioner disk's Rev G count): read against
  the client's closed page of 2026-11-12, one of the two steps its call needed was the closed young-cohort lesson (the
  current supplier lot's curve, reached through a serial-range join that open-ground.md now rules dead as a deciding
  lesson); pooling the disk lots alone moved both pairs out of band and the judge's blind pass found the lot on 7 of 8
  cells; superseded before upload at the author's word for five or six independent judgments off the closed page in a
  larger related pack, in another fab, company and dataset.
