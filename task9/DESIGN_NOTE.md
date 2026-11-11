# task9: what is causing the edge ring on Tessaline Fab 2's wafers, what it has cost since April, and after how many wafers of its own use each polish unit should change the part responsible once Rev G takes it out of the full PM

## Draw

Subdomain: General Statistics & Data Science, Interpretability (feature attribution and mechanistic analysis: a sort-yield
  loss attributed across correlated process features to the part whose wear carries it); the author supplied the draw as
  Concept 2 of the three concepts prepared on 2026-11-10.
Analysis type: Root-Cause Analysis, ending in a dial setting
Answer shape: ranked causes with their contributions: the ring's loss since 1 April measured and split across its
  candidate causes (the conditioner disk's wear, the pad's life on top of it, the retaining ring, DEP-3, SC-4 and the
  chambers' RF hours at about nothing), then across the maintenance rules that ran the disks that long, with each unit's
  count for the disk on its own and the saving it brings.
Weight: attribution. Most of the work is splitting a measured loss across candidates that move together: tools routed
  together, a scanner that arrived the same month as Rev F, three CMP parts that reset together at a full PM, and three
  maintenance rules that ran over the same disks; none of the last three builds (task20, task21 and this slot's first
  architecture) put its weight there.
Data-native sentence: a fab's sort records see the ring only as zone fail counts on every wafer, its process records send
  one deposition chamber's wafers mostly to two of the four polish units, and its maintenance log resets the disk, the
  pad and the retaining ring together except in a handful of free-text entries, while each disk wears at its own rate, so
  the loss, its cause, its dose and the rules' shares all have to be rebuilt from records that each see one face of it.
People: Katelyn Bailey (yield engineering lead), Victor Kelley (CMP module engineer), Leah Griffith (equipment
  maintenance lead), Elizabeth Sandoval (fab finance, owner of the cost inputs); drawn with guard.py names --geo us --seed 9021.

1. Fit: the client's direction is the yield-loss decomposition and tool-commonality literature named in the concept; the
   draw is not a reskin of any client task (skeleton.py check: mark115, task21, task5, the client's b34ffd70 and mark132
   nearest, severity none against each).
2. Task type: regression and model diagnostics serves forecasting in the house mapping, so the root-cause analysis is drawn
   under Interpretability, the General Statistics task type that serves Root-Cause: attribution across dependent features
   and a mechanistic dose-response are its own objects.
3. Data: generated, simulating the fab's process (lot starts and a product mix that shifts in June, dispatch with one
   chamber-to-unit affinity and partner units covering each other's downtime, clustered random defects and a fab-wide
   particle week, the outermost zone's normal fallout, conditioner-disk wear at a per-unit and per-disk rate with a pad
   term, the maintenance timeline under Rev E, Rev F and waiver EW-118 with disk-only and ring-only swaps, edge
   removal-rate metrology, the fab's ring classifier, the yield team's die-map pulls).
4. Decision: the Rev G count for the part responsible, at the module team's review; backward on the loss and the rules'
   shares, forward on the count and the saving.
5. Shell: question form what; one deliverable, a short deck for the module review (pptx), away from the over-quota
   workbook sets and from every shell in the slot's lineage.
6. Card: shape 04, gap objective then population, generators G4, G16, G6, Gate G decomposition_attribution, calibration
   form physical_verification (the edge removal-rate metrology), context artifact monitoring_export (the classifier's
   labels), forum line_manager_or_team, forcing event incident_or_complaint (the excursion ticket), organisation
   manufacturer, role field_unit_lead, strategy decomposition_attribution.
7. Guard: registered 2026-11-11, WARN only: repeat.gate_g (after task20, whose split is a forecast's misses), repeat.decision
   (dial_setting after task21's rate change), repeat.question_form (what), skeleton.house_lesson (the routing rival is a
   supporting step, never the deciding lesson).
8. Slot: architecture 1 of the cleared slot (Concept 1) is spent and in the card's lineage.

## Deep reasoning

Task type: Interpretability (feature attribution and mechanistic analysis), serving Root-Cause Analysis: the loss
  attributed across dependent process features, the mechanism's dose-response on the responsible part's own usage, and
  the attribution of the loss to the maintenance rules that set that usage.
Domain test: every result is the field's own statistical object: an excess-loss estimate against a no-effect baseline, an
  attribution across collinear features whose separation rests on rare decoupling events and on the right unit of
  variation, a hinge dose-response per group, a counterfactual decomposition by re-running a policy on the observed
  sequence, and a renewal-reward optimum with its yearly value; the statistician defends each by the data, not by
  semiconductor arithmetic.
Swap: with a hospital's infusion pumps for the polish units and occlusion alarms for the ring, the counts, the disk lives
  as the units of variation and the policy re-run survive only as an analogy, because the ring's no-effect baseline is the
  outermost sort zone's fallout at a fresh disk, the decoupling events are maintenance-log entries that reset one part and
  not the others, and the dose is wafers of a disk's own use: the field's process is the estimand, not a backdrop.
Where the weight sits: R3 and R5, the two attributions: R3 needs every candidate in one model with each disk life at its
  own wear rate (or the six ring-only swaps read as a natural experiment), and R5 needs each maintenance rule run on each
  unit's own wafer sequence from the record's state on 5 January; both are long, not clever.
Layer 1: retested wafers (an earlier sort record superseded by its retest), product aliases (PA-MCU32, MCU64B), litho
  rework rows in the MES, blank counters on 4 per cent of maintenance entries and back-entered rows a day late, free-text
  parts lists in four spellings per part, the pre-record full PMs and pad changes in December, routine PM_CHECK,
  SLURRY_FLUSH and ENDPOINT_CAL rows, FDC sensor dropouts, scrapped wafers that never reach sort, and wafers still unsorted
  at the pull; each comes from the systems' own behaviour and none decides a result.
Not one thing: the strongest single piece is the disk as the cause, read off its own counter; a run that nails it still
  has to measure the loss against the fallout a fresh disk leaves rather than the band's level before April (R1, R2),
  read the retaining ring with the disk lives as the units (R3), run the old rule and Rev F on each unit's wafers (R5)
  and price Rev F at its own steady state rather than the summer's rate (R7).
One-fact test: "the edge ring was already costing yield before April, on the high-downforce pair under the 2,000-wafer
  rule" rescues R1 and R2, two of seven; no sentence rescues more (effort.json hints).
Not semantics: every field read correctly (the zones, the counters, the waiver text, the cost inputs) still leaves the
  careful pass at 1.06 points, a 4.6 per cent ring share, an 18, 40 and 42 per cent split and a USD 781,000 saving,
  because each is an estimation choice, not a reading.
Not rule application: no filed procedure measures the loss, attributes it, fits the dose, re-runs a rule or sets the
  count; the spec files only the rules' intervals and the waiver's scope, the cost inputs file only the prices and the
  costing of a part moved out of the full PM.
Estimand: the prompt fixes the loss's window (wafers sorted 1 April to 31 August 2026), unit (points of mean wafer sort
  yield, good die by product), the dose's unit (wafers of the part's own use; points of the outermost zone's fail rate per
  1,000 wafers), the bridge's order (what the 2,000-wafer rule would have cost anyway, what Rev F added, what EW-118
  added), the count's lever (the part out of the full PM, Rev G's draft in the spec) and the saving's comparison (Rev F as
  it stands); the cost inputs' Rev G costing note files the costing.
No decoy: nothing is written to carry a wrong answer; the excursion ticket reports the classifier's rising EDGE_RING
  share, which is true and answers a shallower question, and the die-map review set is the yield team's working sample,
  labelled by requester; no document ranks a cause or proposes a count.
No replay: no result re-derives a published figure and no stated number in the pack is wrong.
Pinned: the rivals were run on the cut pack: five fallout baselines put R1 at 1.321 to 1.329 against a band of 1.23 to
  1.41; per-unit, unweighted, ring-term and below-2,800 fits keep every onset and slope inside 15 per cent and every
  count inside 8 per cent; four bridge variants stay within 0.03 of 0.23, 0.34 and 0.43; four saving variants run 278,000
  to 295,000 against 265,000 to 311,000.
Run forecast: R1 and R2 first story (the band's level before April), R3 method shortcut (the joint fit's ring share read
  wafer by wafer), R5 first story (the loss sliced at 2,000 and 2,800 wafers), R7 dismissed own evidence (the summer's
  rate carried forward); R4 and R6 earned.
Strategy label: WORKS IN FORM: separating two explanations for one pattern (the ring as new since April against the
  disk's wear present before it, separated only by the like-for-like fallout at a fresh disk), and variance beyond
  sampling noise (the disk lives' own wear rates, the variance component the wafer-level fit omits).
Depth level: 5: five independent judgments (the fallout baseline, the unit of variation for the ring, the rules re-run,
  the pair split, Rev F's steady state), and the shortcuts land on eight different wrong answers (1.06, 1.13, 1.56, 1.59
  and 2.08 points; one fleet count of 1,370; 1,100 and 870 from zero; 2,030 and 1,780 on the full PM; the pad's 840).
Lesson: a loss whose cause resets with its rivals is measured against the fresh part's fallout, attributed with the
  part's own lives as the units that vary, and split across rules by running each rule on the units' own sequences;
  no build on file teaches the policy re-run or the ring's share at the disk-life grain.

## Results chain

| ID | Result (checkable) | Area | Pinned by | Band | Hurried analyst | Depends on | Graded as |
|---|---|---|---|---|---|---|---|
| R1 | The ring's loss on wafers sorted 1 April to 31 August: 1.32 points of mean wafer sort yield | missingness and measurement | the prompt's window and unit; the sort record's zone counts on every wafer; the fallout at a fresh disk from the dose fit | 1.23 to 1.41 | stopped at the first story: measured against the band's level before April as if the ring started then, 1.06 | independent: the sort record's zone counts and the outermost zone's fallout at a fresh disk | Component 1 |
| R2 | The same loss in good die: P-A 209,000, P-B 21,000, P-C 316,000 | decomposition and attribution | the prompt; R1's per-wafer loss summed by product | each within 8 per cent | stopped at the first story: the same pre-April baseline, 167,000, 17,000 and 251,000 | R1 | Ask 1 |
| R3 | Each candidate's share: the disk's wear 96.5 per cent, the pad's life on top of it 3.5, the retaining ring, DEP-3, SC-4 and the RF hours each within 1 per cent of none | investigation loops | the maintenance log's decoupled entries; the disk lives as the units that vary; the six ring-only swaps | disk 92 to 100, pad 0 to 8, the retaining ring within 2.5, each rival within 2 | method shortcut: one joint fit read wafer by wafer gives the retaining ring 4.6 per cent (t of 10 to 14 on the wafers, under 2 on the disk lives) | - | Ask 2 |
| R4 | Each unit's onset and slope: PU-1 and PU-2 at 1,300 wafers and 17.0 points per 1,000; PU-3 and PU-4 at 910 and 21.2 | modeling | the counters rebuilt from the log; the hinge fit by downforce pair | onset and slope each within 15 per cent | method shortcut: one fit over the fleet (1,090 wafers, 18.5 points), or the polish record's own pad counter | - | Component 2 |
| R5 | The shares of the loss: 23 per cent the 2,000-wafer rule would have cost anyway, 34 per cent Rev F's move to 2,800 added, 43 per cent the EW-118 retained disks added | causal reasoning | the prompt's order; the spec's rules and dates; each rule run on each unit's own wafers from 5 January | each within 0.03 | stopped at the first story: the loss sliced at 2,000 and 2,800 wafers of disk use, 18, 40 and 42 per cent | R4 | Component 3 |
| R6 | Each unit's count for the disk under Rev G: PU-1 and PU-2 at 1,570 wafers, PU-3 and PU-4 at 1,200 | synthesis | the spec's Rev G draft; the cost inputs' disk change and Rev G costing note; R4's fits at the summer's mix | each within 8 per cent | method shortcut: one fleet count of 1,370, or a dose from zero at 1,100 and 870 | R4 | Recommendation |
| R7 | The yearly saving against Rev F as it stands: USD 288,000 | forecasting | the prompt's comparison; the cost inputs' volume and costing; R6's counts on R4's curves | 265,000 to 311,000 | dismissed own evidence: the summer's own loss rate carried forward as Rev F's though the waiver behind it has ended, 781,000 | R4, R6 | Ask 3 |

Carry-forward: R1, R3 and R4 are graded on their own work; R2 falls only with R1's baseline; R5 and R6 rest on R4's
  fits, and each needs a move of its own (the rules run on each unit's wafers, the cost optimum per pair), so a fleet fit
  still files R5's shares inside their band; R7 is graded on the saving at the counts it states, and a pooled count
  changes it by under 1 per cent, so only the baseline moves it.

## Hidden factor record

| Factor | Real or constructed | Only in deciding units | Found by | Fix depth | Verdict |
|---|---|---|---|---|---|
| The ring follows the conditioner disk's own usage, past an onset | constructed (simulated) | no: every unit, every disk life, January to August, all three products | modelling: each part's counter rebuilt from the maintenance log, a hinge fit beside the pad's and the retaining ring's | modelling | keep; priced Right in the careful column (R08, R11, R14) |
| DEP-3's wafers routed mostly to PU-3 and PU-4 | constructed (simulated dispatch) | no: every DEP-3 wafer in the record, deciding no result | modelling: DEP-3 beside the disk's dose in one fit | modelling | keep, a supporting step inside R3 |
| SC-4 arriving on 10 April beside Rev F | constructed (simulated) | no: every SC-4 lot from April | modelling: SC-4 beside the dose | modelling | keep, a supporting step inside R3 |
| Each disk wears at its own rate (lognormal spread 0.08) | constructed (simulated) | no: all 19 disk lives on the four units | modelling: disk-life slopes, or the ring-only swaps read as a natural experiment | modelling | keep: R3's judgment |
| The ring already present before April on the high-downforce pair under the 2,000-wafer rule | constructed (the same mechanism) | no: every disk past its onset since January, both pairs | modelling: the fallout at a fresh disk read off the dose fit | modelling | keep: R1's judgment |
| The EW-118 disks run past 2,800 wafers | constructed (the waiver's process, filed in the spec) | no: four disk lives, one on each unit | modelling: each rule run on each unit's wafers | modelling | keep: R5's judgment needs the counterfactual, not the finding |

## Effort test

| Result | Quick pass | Careful but hurried | Thorough |
|---|---|---|---|
| R1 the ring's loss on wafers sorted 1 April to 31 August, points of mean sort yield | Missed | Missed | Right |
| R2 the same loss in good die for each product | Missed | Missed | Right |
| R3 each candidate cause's share of the loss | Missed | Partly | Right |
| R4 each unit's onset and the slope after it | Missed | Right | Right |
| R5 the shares from the 2,000-wafer rule's own exposure, Rev F's extension and the EW-118 retained disks | Missed | Missed | Right |
| R6 each unit's count for the disk under Rev G | Missed | Right | Right |
| R7 the yearly saving against Rev F as it stands | Missed | Missed | Right |
| Roughly | 0 of 7 | 2.5 of 7 | 7 of 7 |

Measured by: .claude/skills/stumping/effort.py on generator/effort.json
Largest single hint: The edge ring was already costing yield before April, on the high-downforce pair under the 2,000-wafer rule; rescues 2 of 7 results
Pair estimate: 38.2

## Data provenance

Source: generated by task9/generator from a simulated fab (world.py, pack.py, docs.py), deterministic on seed 9021.
Behaves like the real thing: the simulator runs the process a 300 mm mature-node fab runs: weekly lot starts at a product
  mix, wafer-level dispatch through six chamber steps with a chamber-to-unit affinity and partners covering downtime,
  defects clustered within zones (gamma) on a wafer-level defect density, an outermost zone with its own fallout, a
  conditioner disk whose wear raises the edge over-polish past an onset at a rate set by the unit's downforce and the
  disk's own build, maintenance by the spec's intervals with the waiver and the swaps the floor made, removal-rate
  metrology on one wafer in five, a classifier that misses mild rings, and a review set the yield team pulls.
Genuine patterns: (1) a weekly drift in defect density and a fab-wide particle week in May; (2) a product mix that shifts
  toward the large-die product in June; (3) the two downforce pairs wearing at different rates; (4) disk-to-disk spread in
  wear; (5) the pad's life adding to the disk's effect; (6) clustered defects making zone counts overdispersed.
Problems by process: retests from probe-card recontacts, product aliases from the tester's program names, litho rework
  rows, blank and back-entered maintenance counters from technicians entering after the shift, free-text parts lists,
  FDC sensor dropouts, scrap before sort, and wafers not yet sorted at the pull.
Breadth: 14 files and 12 review-deck images; 37,971 sort records over 37,591 wafers, 277,077 MES rows over 40 steps and
  about 110 tools, 408 maintenance entries over four units, 37,591 polish records, 7,177 die maps, so choosing which
  tools, counters and episodes to read is work.

## Template check

Chain signature: missingness-measurement, decomposition-attribution, investigation-loops, modeling, causal-reasoning,
  synthesis, forecasting
Question form: what (what is causing it, what has it cost, after how many wafers to change the part)
Nearest build: task20 (an attribution of a model's misses, investigation weight, a timeline); this build ends on a dial set
  per unit pair and a policy re-run, with attribution weight and ranked causes.

## Frontier check

Precedents: R1 and R2 cite L27 (the dramatic before-and-after preferred over a like-for-like comparison); R3 cites L19
  (default standard errors though the run had read the unit that varies); R5 cites L26 (a shallower account that passes
  its own checks); R7 cites N02 (history assumed informative of the forward window); R4 and R6 are Right in the careful column (a fitted breakpoint and a mechanism one plot shows are reflexes).
Shallow path checks: R1's pre-April baseline passes the ticket's own framing and a before-and-after of the band, and is
  refuted by the fallout at a fresh disk in January to March (the dose fit on the sort record and the maintenance log);
  R3's 4.6 per cent passes a t of 10 to 14 on the wafers and is refuted by the six ring-only swaps (steps of -0.005 to +0.005)
  and a t under 2 on the disk lives; R5's slices pass their sum check and are refuted by the 2,000-wafer rule run on each
  unit's own polish sequence (the FDC's platen counter and the log); R7's rate passes the summer's own ledger and is
  refuted by Rev F's steady state on the fitted curves.
Assumption made false: a run lists "the summer's loss rate continues under the current spec" and waves it through; the
  waiver's end on 14 August and the four retained disks the log records make it false, and the spec and the log test it.
Forcing: the call is each pair's count inside its band (the golden less and more 8 per cent): six sound methods (each
  unit's own fit, the window's mix, the ring term, unweighted, below 2,800) all inside, nearest 2.6 per cent from an edge;
  the fleet's 1,370, a dose from zero, the full PM moved and the pad all outside; slopes 20 per cent either way, onsets 5
  per cent, the die value and the disk change 10 per cent, the pad's term doubled or removed all keep both pairs inside.
Noun swap: nearest mark115 (a deal mechanic for a franchise), task21 (a rate change), task5 (a county estimate), the
  client's b34ffd70 (re-offending) and mark132 (last-time buys); swapping their nouns in carries no decision form,
  deciding lesson, detection or move across; severity none against each.

## Semantic fork table

| ID | Term or convention | Readings | Golden | Ruled out by |
|---|---|---|---|---|
| SF1 | the ring's loss | every outermost-zone fail above the interior; above the band's level before April; above the fallout at a fresh disk | above the wafer's own interior rate plus the fallout at a fresh disk | the prompt's "what has it cost", and the January to March wafers on worn disks, which carry 0.28 points of ring |
| SF2 | a wafer's sort record | the first record; the latest | the latest (a retest supersedes) | the sort record's retest_flag |
| SF3 | the window | by polish date; by sort date | wafers sorted 1 April to 31 August | the prompt's "wafers sorted" |
| SF4 | each unit's onset and slope | each unit's own fit; its downforce pair's | the pair's fit, reported for each unit | same call: each unit's own fit lands inside every band |
| SF5 | a part's usage | wafers since the full PM; the polish record's pad counter; wafers since the part itself was replaced | wafers since the part itself was replaced, from the log's parts text | the log's EW-118 and unscheduled entries, which reset one part and not the others |
| SF6 | the bridge's order | Shapley; the prompt's sequence | the 2,000-wafer rule first, then Rev F, then the waiver | the prompt's "would have cost anyway, ... added, ... added" |
| SF7 | the bridge's counterfactual | the loss sliced by usage; each rule run on each unit's wafers | each rule run on each unit's own sequence, the unscheduled swaps as they happened | the spec: unscheduled changes do not restart the full PM count |
| SF8 | the count's lever | the part inside the full PM; on its own count | on its own count, out of the full PM | the spec's Rev G draft and the prompt |
| SF9 | the count's costing | the full PM's all-in; the part's own change | the disk change's all-in each time, the full PM less the disk's price | the cost inputs' Rev G costing note |
| SF10 | the die value at risk | the record's mix; the summer's | the summer's mix (sorted from 1 June) | same call: the window's mix moves every count by under 0.5 per cent |
| SF11 | Rev F as it stands | the summer's observed rate; Rev F's own cycle | Rev F's own 2,800-wafer cycle on the fitted curves, the waiver ended | the spec's waiver window and the prompt's "as it stands" |
| SF12 | a unit's year | 58,500 split evenly; split by the units' shares | split by each unit's share of the wafers polished since 1 June | same call: the window's shares move the saving by under 0.2 per cent |
| SF13 | a cause's share with the pad's interaction | Shapley; the pad's increment over a fresh pad | the pad's increment, the disk's share the rest | same call: Shapley halves the pad's 3.5 per cent, inside its band |

## Closure table

| Axis | Closure |
|---|---|
| 1 | Population: every wafer sorted 1 April to 31 August (SF3); every polished wafer for the fits |
| 2 | Unit of account: points of mean wafer sort yield; good die; wafers of a part's own use; USD a year |
| 3 | Attribution window: wafers sorted in the window; the dose fitted on every wafer since 5 January |
| 4 | As-of dating: the pull on 31 August 2026; the summer's mix and shares from 1 June |
| 5 | Version basis: the latest sort record per wafer (SF2); the log's entries as entered |
| 6 | Denominator: each wafer's gross die for points; the outermost zone's tested die for the fail rate |
| 7 | Weighting: wafers equally for points; the zone's tested die in the fits |
| 8 | Window length: the five months of the window; a year of 58,500 wafers for the saving |
| 9 | Boundary inclusivity: sort end from 1 April 00:00 to before 1 September |
| 10 | Rounding path: computed unrounded, stated at the answer blocks' precision once |
| 11 | Tie-break: none needed; each pair's count clears its nearest shortcut by over 5 per cent |
| 12 | Maturity and censoring: wafers unsorted at the pull are outside the window; disks still running are fitted to date |
| 13 | Order of operations: records cleaned, counters rebuilt, fits, the loss, the shares, the rules re-run, the counts |
| 14 | Row order: no figure depends on file order (two byte-identical builds) |
| 15 | Duplicate resolution: a retest supersedes the first sort record (SF2) |
| 16 | Identity normalisation: product aliases to P-A, P-B and P-C; the four spellings of each part |
| 17 | Netting against gross: the fallout at a fresh disk netted from the outermost zone (SF1) |
| 18 | Dimensional units: wafers, die, points, points per 1,000 wafers, USD |
| 19 | Code and status semantics: EDGE_RING is the classifier's label, not the measure; retained disks per EW-118 |
| 20 | Integerisation: counts in wafers rounded to ten; good die to the thousand |
| 21 | Clause scope: Rev F from 2 April by the PM's date; EW-118 at the four full PMs the log marks |
| 22 | Forward window contents: the summer's mix and shares, the waiver ended, pads at 600 (SF10, SF11, SF12) |

## Literal reader

A reader executing the prompt word for word measures, on every wafer sorted from 1 April to 31 August, the outermost
zone's fails above what that zone fails with no ring, averages them as points of mean wafer sort yield and sums them as
good die by product; ranks the causes by their share of that loss; gives each unit the usage in wafers of the responsible
part's own use at which the loss starts and the climb after it; splits the loss into what the 2,000-wafer rule would have
cost, what Rev F's 2,800 added and what EW-118 added, in that order; and sets each unit's count once Rev G takes the part
out of the full PM, with the yearly saving against Rev F at the cost inputs: each of these is the golden's estimand.

## Prompt contract

A voice rewrite may not drop or change: the three questions (the cause, the cost on wafers sorted 1 April to 31 August
2026, the count once Rev G takes the part responsible out of the full PM); the loss in points of mean wafer sort yield
and in good die for each product; the causes ranked by their share of that loss; each unit's usage at which the loss
starts and the climb after it in points of the outermost sort zone's fail rate per 1,000 wafers; the shares the
2,000-wafer rule would have cost anyway, that Rev F's move to 2,800 added and that the EW-118 waiver added, in that
order; each unit's change count and the yearly saving in dollars against Rev F as it stands; a short deck. It must never
add a rounding instruction, a method (a hinge, a regression, clustering, a counterfactual, a bootstrap), a warning, an
attached file's name, a role or a count the data hold.

## Pre-ship check

Leak sweep (leak.py at the pull, 2026-08-31): REVIEW, four lines, each ruled here.
- die_geometry.py: the yield database's own die-position helper (die centres, radius, zone by radius); its docstring
  documents its functions and no longer describes the sort file's columns; it constructs no result.
- excursion_ticket_YE-2026-031.txt: the yield team's own ticket (symptom, request, three dated notes); it states no figure
  and names no suspect, and its "since April" is the classifier's rising share, true and shallower than the loss.
- pm_spec_history.md: the module's own spec history with waiver EW-118 and the Rev G draft; it files the rules, dates and
  the lever (the WHAT), never a method.
- pm_spec_history.md, the stump-vocabulary line (record, maintenance, retaining, changes): the words of a PM spec's own
  genre ("retaining" is the part's name); no sentence names a move.
Realism: the deck rendered and read at speed; findings as titles, the charts as the slides, counts to ten wafers,
  dollars to the hundred or the thousand, shares to a tenth, tables styled, slide numbers, source strips with the
  rounding stated; the waiver's four-disk limit noted from the spec.
Containers: audit_containers exit 0 (the pack's exports to 31 August, the deck stamped 8 to 10 September 2026).
Figures: figures_check exit 0; checks.py 66 of 66; verify.py 23 of 23 inside their bands by other code paths; two
  builds under different hash seeds byte-identical.
Caution on the paper: the cited pair is 38.2, and paper estimates have come back 40 to 60 points high; R1 and R2 (the
  fallout baseline), R5 (the rules re-run) and R7 (Rev F's steady state) are each a judgment a careful run can make, so
  two of them earned puts the pair near 60. The judge thread's own first pass is read against the careful column below
  before READY.
Judge (stage 4, 2026-11-11): DETERMINISTIC, FIX_NOW (answer blocks only: the PU-3 and PU-4 lower bands, bands on the
  per-pair savings, ask 3's candidate list, the volume split stated). Its own first pass, written from the pack before it
  opened the blocks, landed every result inside its band: the loss 1.32 to 1.33 points against each product's fallout at
  a fresh disk, the die by product, the disk as the only driver with the retaining ring at none, onsets 1,224, 1,201, 975
  and 768 with climbs 15.1 to 22.2, the rules' shares 25.3, 33.3 and 41.5 per cent by running each rule on the units' own
  sequences, counts 1,543, 1,489, 1,245 and 1,104, and a saving of 279,000 to 307,000 at Rev F's own cycle. Re-priced on
  that pass the careful column earns R1 to R7 (about 96), over 50, so the build returns to stage 2 whatever the verdict.

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
