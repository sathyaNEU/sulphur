# task9: what is causing the edge ring on Tessaline Fab 2's wafers, what it cost at sort and at final test from April to August, and after how many wafers of its own use each polish unit should change the part responsible once Rev G takes it out of the full PM

## Draw

Subdomain: General Statistics & Data Science, Interpretability (feature attribution and mechanistic analysis: a yield
  loss attributed across correlated process features to the part whose wear carries it, and that part's wear read
  through two records at different grains); the author supplied the draw as Concept 2 of the three concepts prepared on
  2026-11-10, and chose on 2026-11-11 to redesign its chain at stage 2 after the judge's blind first pass landed the first.
Analysis type: Root-Cause Analysis, ending in a dial setting
Answer shape: ranked causes with their contributions: the ring's loss at sort measured and split across its candidate
  causes (the conditioner disk's wear, the pad's life on top of it, the retaining ring, DEP-3, SC-4 and the chambers' RF
  hours at nothing), the units final test lost to the same wear, the current disk lot's curve, each unit's count for the
  disk on its own and the saving it brings.
Weight: a hard-to-measure quantity. Most of the work is the ring's full cost on the disks the units will run: the sort
  loss on every wafer, the latent loss final test reports only by lot, and the wear curve of a disk lot that has run for
  four months beside an older one; neither of the last two builds (task21's modeling, task20's validation) put its
  weight there.
Data-native sentence: a fab's sort records see the ring only as zone fail counts on every wafer, final test sees its
  latent damage only as a lot's burn-in failures weeks later, and the maintenance log names each disk only by the serial
  a technician typed, which only the stores receipts' serial ranges tie to its supplier lot, so the ring's cost, its dose
  on the disks in stores and the count all have to be rebuilt from records that each see one face of it.
People: Katelyn Bailey (yield engineering lead), Victor Kelley (CMP module engineer), Leah Griffith (equipment
  maintenance lead), Elizabeth Sandoval (fab finance, owner of the cost inputs); drawn with guard.py names --geo us --seed 9021.

1. Fit: the client's direction is the yield-loss decomposition, tool-commonality and yield-reliability literature named
   in the concept (good die in bad neighbourhoods failing burn-in); the draw is not a reskin of any client task (the
   skeleton check below).
2. Task type: Interpretability, the General Statistics task type that serves Root-Cause: attribution across dependent
   features and a mechanistic dose-response are its own objects.
3. Data: generated, simulating the fab's process (lot starts and a product mix that shifts in June, dispatch with one
   chamber-to-unit affinity and partner units covering each other's downtime, clustered random defects and a fab-wide
   particle week, the outermost zone's normal fallout, conditioner-disk wear at a per-unit, per-lot and per-disk rate with
   a pad term, thinned edge dielectric that passes sort and fails burn-in, stores issuing the oldest disk lot first, the
   maintenance timeline under Rev E, Rev F and waiver EW-118 with disk-only and ring-only swaps, edge removal-rate
   metrology, the fab's ring classifier, the yield team's die-map pulls, assembly loss and final test at the assembly house).
4. Decision: the Rev G count for the part responsible from September, at the module team's review; backward on the
   loss at sort and at final test and on the causes, forward on the current lot's curve, the count and the saving.
5. Shell: question form what; one deliverable, a short deck for the module review (pptx).
6. Card: shape 04, gap objective then population, generators G4, G16, G6, Gate G decomposition_attribution, calibration
   form physical_verification (the edge removal-rate metrology), context artifact monitoring_export (the classifier's
   labels), forum line_manager_or_team, forcing event incident_or_complaint (the excursion ticket), organisation
   manufacturer, role field_unit_lead, strategy decomposition_attribution.
7. Guard: re-registered 2026-11-11 for the redesign, WARN only: overuse.weight (rule design after task13's third
   architecture: here the rule is a part's replacement count on two stages of loss, not a monitoring threshold),
   repeat.decision (dial_setting after task21's rate change: a count in wafers per unit), repeat.question_form (what),
   skeleton.house_lesson (vintage_or_cohort_drift on task1 v3 and task21 v1: here the cohort is a supplier lot that only
   a typed serial and a receipt's range name, and the lesson the call turns on is that link and the latent stage),
   skeleton.house_shell (dial_or_cap_setting: the decision is a replacement count, which is a dial).
8. Slot: architecture 1 of the cleared slot (Concept 1) is spent and in the card's lineage; Concept 2's first chain is
   recorded under Tried and rejected.

## Deep reasoning

Task type: Interpretability (feature attribution and mechanistic analysis), serving Root-Cause Analysis: the loss
  attributed across dependent process features, the mechanism's dose-response on the responsible part's own usage and
  supplier lot, and its latent consequence at the next test stage, carried into the part's replacement count.
Domain test: every result is the field's own statistical object: an excess-loss estimate against a no-effect baseline,
  an attribution across collinear features, a hinge dose-response per group with the group a cohort the record names
  only by a serial range, an ecological count model of lot-level failures on wafer-level exposure with its own response
  shape, and a renewal-reward optimum with its yearly value.
Swap: with a hospital's infusion pumps for the polish units and occlusion alarms for the ring, the counts, the supplier
  lots and the later failures survive only as an analogy, because the ring's no-effect baseline is the outermost sort
  zone's fallout on a young disk, the lot is a conditioner-disk serial range on a stores receipt, and the latent loss is
  thinned edge dielectric that passes wafer sort and fails package burn-in: the field's process is the estimand, not a
  backdrop.
Where the weight sits: R3, R4 and R5. R3 needs final test's lot totals modelled on each lot's wafers (the outer zone's
  good die and each disk's wear) with the rise's own shape; R4 needs each disk's lot rebuilt from the serial its PM entry
  typed and the receipts' serial ranges, and the curve fitted on the lot the units run now; R5 needs both together.
Layer 1: retested wafers (an earlier sort record superseded by its retest), product aliases (PA-MCU32, MCU64B), litho
  rework rows in the MES, blank counters on 4 per cent of maintenance entries and back-entered rows a day late, free-text
  parts lists in four spellings per part with the disk's serial typed in, the pre-record full PMs in the autumn, routine
  PM_CHECK, SLURRY_FLUSH and ENDPOINT_CAL rows, FDC sensor dropouts, scrapped wafers that never reach sort, wafers
  still unsorted at the pull, final-test lots split into sub-lots, lots not yet through final test at the pull, and the
  assembly loss between sort and final test; each comes from the systems' own behaviour and none decides a result
  beyond the assembly result that grades it (R4, the disk lives and lots).
Not one thing: the strongest single piece is the current lot's faster wear; a run that has it still prices final test
  in proportion to the sort loss and sets the counts 13 and 20 per cent long (R5), and loses R3; a run that measures
  final test's rise and misses the lot sets them 18 and 21 per cent long and loses R4 and R6.
One-fact test: "the disks fitted since May come from a supplier lot that wears faster than the ones before it" rescues
  R4 and R6, two of six; no sentence rescues more (effort.json hints).
Not semantics: every field read correctly (the zones, the counters, the serials, the receipts, the final-test columns,
  the cost inputs) still leaves the careful pass on every lot's curve and a proportional final test, because each is an
  estimation choice, not a reading.
Not rule application: no filed procedure measures the loss, attributes it, links a disk to its lot, models final test,
  fits the dose or sets the count; the spec files only the rules' intervals, the waiver's scope and the Rev G lever,
  the cost inputs file only the prices, the plan's volume and mix, and the costing of a part moved out of the full PM.
Estimand: the prompt fixes the loss's windows (wafers sorted, and lots final-tested, 1 April to 31 August 2026), units
  (points of mean wafer sort yield, good die by product, units lost at final test by product), the dose's population
  and unit (the parts the units will be fitted with from September; wafers of the part's own use; points of the
  outermost zone's fail rate per 1,000 wafers), the count's lever and cost (the part out of the full PM from September,
  the ring costed at sort and at final test) and the saving's comparison (Rev F as it stands); the cost inputs file the
  costing, the plan's volume by unit and mix, and what a unit scrapped at final test costs.
No decoy: nothing is written to carry a wrong answer; the excursion ticket reports the classifier's rising EDGE_RING
  share, which is true and answers a shallower question, and the die-map review set is the yield team's working sample;
  no document ranks a cause, names a lot's wear, ties burn-in to the ring or proposes a count.
No replay: no result re-derives a published figure and no stated number in the pack is wrong.
Pinned: the rivals were run on the cut pack: five fallout baselines put R1 at 0.874 to 0.91 against 0.84 to 0.96; three
  final-test readings put R3 within 1.5 per cent; five fits keep every onset within 1 per cent and every climb within 4;
  nine count variants run 981 to 1,011 and 833 to 850 against 930 to 1,090 and 770 to 910; seven saving variants run
  506,000 to 566,000 against 467,000 to 571,000.
Run forecast: R3 method shortcut (burn-in in proportion to the ring's die at sort), R4 method shortcut (one fit over every
  disk lot), R5 unfinished chain (final test estimated, then carried into the count on the sort loss's shape), R6
  dismissed own evidence (Rev F priced on the disks it ran before); R1 and R2 earned.
Strategy label: WORKS IN FORM: a pooled curve whose parts move differently (the disk lots), and a response measured
  rather than assumed (final test's rise before the ring shows at sort, and its levelling off).
Depth level: 5: four independent judgments (the fallout baseline, the lot split, final test's response shape, Rev F on
  the disks in stores), the count needs two of them together, and the shortcuts land on nine different wrong answers.
Lesson: a part's dose-response is read on the supplier lot the units will run, which only the serials and the receipts
  name, and a latent loss reported by lot at a later stage is modelled on each lot's own wafers with its own shape before
  it is priced into the part's count; no build on file teaches the lot link or the latent stage.

## Results chain

| ID | Result (checkable) | Area | Pinned by | Band | Hurried analyst | Depends on | Graded as |
|---|---|---|---|---|---|---|---|
| R1 | The ring's loss at sort on wafers sorted 1 April to 31 August: 0.90 points of mean wafer sort yield; good die P-A 139,000, P-B 14,000, P-C 226,000 | missingness and measurement | the prompt's window and unit; the sort record's zone counts on every wafer; the band's fallout on disks short of their onset | points 0.84 to 0.96, die each within 8 per cent | stopped at the first story: measured against the band's level before April as if the ring started then, 0.69 (the classifier's wafers 0.70) | independent: the sort record's zone counts and the band's fallout on young disks | Component 1 |
| R2 | Each candidate's share of that loss: the disk's wear 96.3 per cent, the pad's life on top of it 3.7, the retaining ring, DEP-3, SC-4 and the RF hours none | causal reasoning | the maintenance log's decoupled entries; one model per pair and lot with every candidate beside the disk; the six ring-only swaps | disk 88 to 100, pad 0 to 10, every other candidate under 3 | stopped at the first story: tool commonality puts PU-2, PU-4, SC-4 and DEP-3 on top, which is routing and timing | independent: the sort record, the MES routes and the maintenance log | Component 2 |
| R3 | The units final test lost to the ring on lots it finished 1 April to 31 August: P-A 44,300, P-B 3,500, P-C 67,100 | modeling | the prompt's window, by final test's own date; each lot's units and burn-in failures, sub-lots added back; its wafers' outer-zone good die and their disks' wear at sort | each within 15 per cent | method shortcut: burn-in taken in proportion to the ring's die at sort assumes the response's shape, 11,100, 1,100 and 17,100 | independent: the final-test lot summary and each lot's wafers at sort | Ask 1 |
| R4 | Each unit's onset and climb on the disks it will be fitted with from September (lot A165-L2603): PU-1 and PU-2 at 840 wafers and 15.8 points per 1,000; PU-3 and PU-4 at 640 and 23.5 | assembly and reconciliation | each disk's lot from the serial its PM entry fitted and the stores receipts' serial ranges; the lot every unit runs now, the earlier lots' last serials fitted and no disk received since; the hinge fit by pair on that lot | onset 15 per cent under to 10 over; climb 15 per cent either way, 30 per cent under on the low pair | method shortcut: one fit per pair over every disk lot reads the current disks off the old ones, 1,540 and 850 wafers | independent: the stores receipts' serial ranges and the PM log's fitted serials | Component 3 |
| R5 | Each unit's count for the disk under Rev G, the ring costed at sort and at final test: PU-1 and PU-2 at 1,010 wafers, PU-3 and PU-4 at 840 | synthesis | the spec's Rev G draft; the cost inputs' disk change, Rev G costing note, die values with assembly and test and the plan's mix; R4's curves and R3's rise | each within 8 per cent | unfinished chain: final test's loss estimated and then carried into the count in proportion to the sort loss on every lot's curve, 1,730 and 1,170 | R3, R4 | Recommendation |
| R6 | The yearly saving of those counts against Rev F as it stands: USD 519,000 | forecasting | the prompt's comparison; the cost inputs' plan volume by unit and costing; R5's counts on R4's curves | 467,000 to 571,000, each pair within 12 per cent | dismissed own evidence: Rev F priced on the disks it ran before (every lot's curve), USD 274,000 | R4, R5 | Ask 2 |

Carry-forward: R1, R2, R3 and R4 are graded on their own work (R3 on the final-test summary and each lot's wafers, R4 on
  the receipts and the log); R5 needs R3's rise and R4's curve together, and either alone leaves it 13 per cent or more
  long; R6 rests on R4's curve and on final test being priced at all, and a count anywhere in R5's band moves it by
  under 1 per cent.

## Hidden factor record

| Factor | Real or constructed | Only in deciding units | Found by | Fix depth | Verdict |
|---|---|---|---|---|---|
| The ring follows the conditioner disk's own usage, past an onset | constructed (simulated) | no: every unit, every disk life, January to August, all three products | modelling: each part's counter rebuilt from the maintenance log, a hinge fit beside the pad's and the retaining ring's | modelling | keep; priced Right in the careful column (R08, R11, R14) |
| The March disk lot wears faster (its onset 28 to 38 per cent earlier on both pairs) | constructed (simulated supplier lot) | no: the lot ran on all four units from May, beside the earlier lot on PU-1 and PU-3 through the summer, and the misreading decides nothing at the loss (one fit over every lot keeps R1 inside its band) | modelling: each disk's lot linked from its fitted serial to the receipts' serial ranges, then a hinge fit per pair and lot | modelling | keep: R4's judgment and half of R5's |
| Thinned edge dielectric failing burn-in from about half the ring's onset and levelling off | constructed (simulated reliability mechanism) | no: every lot, every product, every month from February, the first quarter included | modelling: a lot-level Poisson model on each lot's wafers' outer-zone good die and their disks' wear | modelling | keep: R3's judgment and the other half of R5's |
| DEP-3's wafers routed mostly to PU-3 and PU-4 | constructed (simulated dispatch) | no: every DEP-3 wafer in the record, deciding no result | modelling: DEP-3 beside the disk's dose in one fit | modelling | keep, a supporting step inside R2 |
| SC-4 reaching M1 from 7 April, five days after Rev F | constructed (simulated) | no: every SC-4 lot from April | modelling: SC-4 beside the dose | modelling | keep, a supporting step inside R2 |
| Each disk wears at its own rate within its lot (lognormal spread 0.05) | constructed (simulated) | no: all 21 disk lives on the four units | modelling: the hinge per pair and lot with the disk lives as texture | modelling | keep, texture inside R4 |

## Effort test

| Result | Quick pass | Careful but hurried | Thorough |
|---|---|---|---|
| R1 the ring's loss at sort on wafers sorted 1 April to 31 August: points of mean sort yield and good die by product | Missed | Right | Right |
| R2 each candidate cause's share of that loss | Missed | Right | Right |
| R3 the units final test lost to the ring on lots it finished 1 April to 31 August, by product | Missed | Missed | Right |
| R4 each unit's onset and climb on the disks it will be fitted with from September | Missed | Missed | Right |
| R5 each unit's count for the disk under Rev G, the ring costed at sort and at final test | Missed | Missed | Right |
| R6 the yearly saving of those counts against Rev F as it stands | Missed | Missed | Right |
| Roughly | 0 of 6 | 2 of 6 | 6 of 6 |

Measured by: .claude/skills/stumping/effort.py on generator/effort.json
Largest single hint: The disks fitted since May come from a supplier lot that wears faster than the ones before it; rescues 2 of 6 results
Pair estimate: 23.0

## Data provenance

Source: generated by task9/generator from a simulated fab (world.py, pack.py, docs.py), deterministic on seed 9021.
Behaves like the real thing: the simulator runs the process a 300 mm mature-node fab runs: weekly lot starts at a product
  mix, wafer-level dispatch through six chamber steps with a chamber-to-unit affinity and partners covering downtime,
  defects clustered within zones (gamma) on a wafer-level defect density, an outermost zone with its own fallout, a
  conditioner disk whose wear raises the edge over-polish past an onset at a rate set by the unit's downforce, the disk's
  supplier lot and its own build, thinned edge dielectric that passes sort and fails burn-in from an earlier point in
  the same wear, stores issuing the oldest lot on the shelf first, maintenance by the spec's intervals with the waiver
  and the swaps the floor made, removal-rate metrology on one wafer in five, a classifier that misses mild rings, a
  review set the yield team pulls, and an assembly house that loses a few die before final test and splits some lots.
Genuine patterns: (1) a weekly drift in defect density and a fab-wide particle week in May; (2) a product mix that shifts
  toward the large-die product in June; (3) the two downforce pairs wearing at different rates; (4) lot-to-lot and
  disk-to-disk spread in wear; (5) the pad's life adding to the disk's effect; (6) clustered defects making zone counts
  overdispersed; (7) burn-in failures at a base rate with lot-to-lot binomial noise.
Problems by process: retests from probe-card recontacts, product aliases from the tester's program names, litho rework
  rows, blank and back-entered maintenance counters from technicians entering after the shift, free-text parts lists
  with typed serials, FDC sensor dropouts, scrap before sort, wafers not yet sorted at the pull, final-test sub-lots,
  lots not yet tested at the pull, and assembly loss before final test.
Breadth: 15 files and 12 review-deck images; 37,930 sort records over 37,196 sorted wafers, 277,063 MES rows over 40
  steps and about 110 tools, 405 maintenance entries over four units, 37,591 polish records, 1,507 final-test rows over
  1,392 lots, 40 stores receipts and 5,796 die maps, so choosing which tools, counters, lots and records to read is work.

## Template check

Chain signature: missingness-measurement, causal-reasoning, modeling, assembly-reconciliation, synthesis, forecasting
Question form: what (what is causing it, what did it cost, after how many wafers to change the part)
Nearest build: task20 (an attribution of a model's misses, investigation weight, a timeline); this build ends on a dial
  set per unit pair on a supplier lot's curve with a latent second-stage loss, with hard-to-measure weight and ranked
  causes.

## Frontier check

Precedents: R3 cites L15 (assumed a response instead of measuring its shape); R4 cites L12 (pooled cohorts whose rates
  drift, the late ages read off the old cohorts); R5 cites L11 (built the split for the first step and dropped it for
  the next: final test estimated, then carried into the count on the sort loss's shape); R6 cites N02 (history assumed
  informative of the forward window); R1 and R2 are Right in the careful column (the fallout on young disks and a joint
  fit with every rival are reflexes, as the judge's blind first pass on this world's first chain showed).
Shallow path checks: R3's proportional reading passes its own regression (burn-in rises with the ring's die at sort, a
  clear positive slope) and is refuted by the lots whose wafers' disks sat between half their onset and the onset, whose
  burn-in already runs well above the base with no ring die at all; R4's pooled fit passes its own residual check at the
  earlier lots' ages and is refuted by the March lot's disks on all four units, whose excess sits above the pooled curve
  from about 600 wafers of use; R5's proportional count passes a cost curve with a clear minimum and is refuted by final
  test's level from about 0.84 of the onset on; R6's pooled saving passes a reconciliation with the April to August loss
  and is refuted by the stores receipts, which show the earlier lots' last serials fitted.
Assumption made false: a run lists "the disks stores will issue wear like the ones in the record" and waves it through;
  the PM log's serials and the stores receipts make it false (the earlier lots' last serials are fitted, no disk has
  been received since the March lot, and it starts the ring 28 to 38 per cent sooner), and the final-test summary tests the run's other
  assumption, that final test's loss scales with the ring at sort.
Forcing: the call is each pair's count inside its band (the golden less and more 8 per cent): nine sound methods (each
  unit's own fit on the current lot, final test's rise on the disk's raw use, each pair's own final-test level, the pad's
  term left out, an unweighted fit, the ring term beside it, the fit below 3,000 wafers, every rival beside it) all
  inside; every lot pooled, final test left out, final test in proportion, both together, the earlier lots' curve, one
  fleet fit and a dose from zero all outside; climbs 15 per cent either way, onsets 5 per cent, final test's level 15 per
  cent, its start 8 per cent or its span 20 per cent, and the die values or the disk change 10 per cent all keep both
  pairs inside.
Noun swap: nearest by skeleton task1 v3 (a newspaper group's pricing on cohort curves), task21 v1 (a motor insurer's
  rate changes), the client's depth:b9efebd1 (a short-term loan launch), mark179 v5 (a supervision caseload count) and
  task18 v1 (an island grid's disturbance losses); swapping their nouns in carries neither the lot link through a stores
  serial range nor the latent second stage modelled from lot totals; severity none against each.

## Semantic fork table

| ID | Term or convention | Readings | Golden | Ruled out by |
|---|---|---|---|---|
| SF1 | the ring's loss at sort | every outermost-zone fail above the interior; above the band's level before April; above the fallout on disks short of their onset | above the wafer's own interior rate plus the fallout on young disks | the prompt's "what did it cost", and the January to March wafers on worn disks, which carry 0.23 points of ring |
| SF2 | a wafer's sort record | the first record; the latest | the latest (a retest supersedes) | the sort record's retest flag |
| SF3 | the window at sort | by polish date; by sort date | wafers sorted 1 April to 31 August | the prompt's "wafers sorted" |
| SF4 | the window at final test | lots whose wafers were sorted in the window; lots final-tested in it | lots final-tested 1 April to 31 August, sub-lots added back to their lot | the prompt's "lots final-tested" |
| SF5 | a part's usage | wafers since the full PM; the polish record's pad counter; wafers since the part itself was replaced | wafers since the part itself was replaced, from the log's parts text | the log's EW-118 and unscheduled entries, which reset one part and not the others |
| SF6 | the parts the units will be fitted with from September | the A165 disk as a part number; the lot stores now issue | the lot every unit runs now (A165-L2603), the earlier lots' last serials fitted and no disk received since | the stores receipts' serial ranges against the log's fitted serials |
| SF7 | each unit's onset and climb | each unit's own fit; its downforce pair's | the pair's fit on the current lot, reported for each unit | same call: the bands' floors reach a unit's own fit on its one short disk of the lot (PU-1, PU-3) and a fit carrying the lot's effect as one multiplier on every unit (PU-4 at 560), and each unit's own count lands inside its band |
| SF8 | the count's lever | the part inside the full PM; on its own count | on its own count, out of the full PM from September | the spec's Rev G draft and the prompt |
| SF9 | the count's costing | the full PM's all-in; the part's own change | the disk change's all-in each time, the full PM less the disk's price | the cost inputs' Rev G costing note |
| SF10 | a unit lost at final test | its die value; its die value plus assembly and test | die value plus assembly and test | the cost inputs' die section |
| SF11 | Rev F as it stands | the summer's observed rate; Rev F's own cycle | Rev F's own 2,800-wafer cycle on the current lot's curves, the waiver ended | the spec's waiver window and the prompt's "as it stands" |
| SF12 | a unit's year and the mix | the record's shares and mix; the plan's | the FY27 plan's wafers per unit and product mix | the cost inputs' volume section; same call: the summer's shares move the saving under 0.2 per cent |
| SF13 | a cause's share with the pad's interaction | Shapley; the pad's increment over a fresh pad | the pad's increment, the disk's share the rest | same call: Shapley halves the pad's 3.7 per cent, inside its band |
| SF14 | a fitted share below zero | a negative share; none | none | the answer blocks' convention; one fit over every lot gives the retaining ring a share below zero |
| SF15 | final test's units by product | by the lot's package code; by the lot's product at sort | by the lot's product at sort (each lot is one product) | the sort record and the MES lot ids |

## Closure table

| Axis | Closure |
|---|---|
| 1 | Population: every wafer sorted 1 April to 31 August (SF3); every lot final-tested in the window (SF4); every polished wafer for the fits |
| 2 | Unit of account: points of mean wafer sort yield; good die; units at final test; wafers of a part's own use; USD a year |
| 3 | Attribution window: wafers sorted and lots final-tested in the window; the dose and final test's rise fitted on every record since 5 January |
| 4 | As-of dating: the pull on 31 August 2026; the parts from September are the lot on the shelf (SF6) |
| 5 | Version basis: the latest sort record per wafer (SF2); the log's entries as entered; final test's sub-lots summed |
| 6 | Denominator: each wafer's gross die for points; the outermost zone's tested die for the fail rate; a lot's units for burn-in |
| 7 | Weighting: wafers equally for points; the zone's tested die in the fits; Poisson for the lots |
| 8 | Window length: the five months of the window; the plan's year for the saving |
| 9 | Boundary inclusivity: sort end and final-test end from 1 April to before 1 September |
| 10 | Rounding path: computed unrounded, stated at the answer blocks' precision once |
| 11 | Tie-break: none needed; each pair's count clears its nearest shortcut by over 5 per cent |
| 12 | Maturity and censoring: wafers unsorted and lots untested at the pull are outside the windows; disks still running are fitted to date |
| 13 | Order of operations: records cleaned, counters and lots rebuilt, fits, the loss, the shares, final test, the counts, the saving |
| 14 | Row order: no figure depends on file order (two byte-identical builds) |
| 15 | Duplicate resolution: a retest supersedes the first sort record (SF2); sub-lots add to their lot |
| 16 | Identity normalisation: product aliases to P-A, P-B and P-C; the four spellings of each part; serials to lots by range |
| 17 | Netting against gross: the fallout on young disks netted from the outermost zone (SF1); final test's base rate netted from burn-in |
| 18 | Dimensional units: wafers, die, units, points, points per 1,000 wafers, USD |
| 19 | Code and status semantics: EDGE_RING is the classifier's label, not the measure; retained disks per EW-118 |
| 20 | Integerisation: counts and onsets in wafers rounded to ten; good die to the thousand; units to the hundred |
| 21 | Clause scope: Rev F from 2 April by the PM's date; EW-118 at the two full PMs the log marks |
| 22 | Forward window contents: the current lot's curve, the plan's volume and mix, the waiver ended, pads at 600 (SF6, SF11, SF12) |

## Literal reader

A reader executing the prompt word for word measures, on every wafer sorted from 1 April to 31 August, the outermost
zone's fails above what that zone fails with no ring, averages them as points of mean wafer sort yield and sums them as
good die by product; ranks the parts and tools behind it by their share of that loss; counts the units final test lost to the ring on the
lots it finished in those months, by product; gives each unit the usage in wafers of the responsible part's own use at
which the loss at sort starts and the climb after it, for the parts the units will be fitted with from September; and
sets each unit's count once Rev G takes the part out of the full PM, the ring costed at sort and at final test, with the
yearly saving against Rev F at the cost inputs: each of these is the golden's estimand.

## Prompt contract

A voice rewrite may not drop or change: the three questions (the cause, the cost on wafers sorted and lots final-tested
1 April to 31 August 2026, the count once Rev G takes the part responsible out of the full PM from September, counting
what the ring costs at sort and at final test); the loss at sort in points of mean wafer sort yield and in good die for
each product; the parts and tools behind it ranked by their share of that loss; the units final test lost to it for each product; each
unit's usage at which the loss at sort starts and the climb after it in points of the outermost sort zone's fail rate per
1,000 wafers, on the parts it will be fitted with from September; each unit's change count and the yearly saving in
dollars against Rev F as it stands; a short deck. It must never add a rounding instruction, a method (a hinge, a
regression, a lot split, clustering, a bootstrap), a warning, an attached file's name, a lot's name, a role or a count
the data hold.

## Pre-ship check

Leak sweep (leak.py --asof 2026-08-31): REVIEW, four lines, each ruled here.
- die_geometry.py: the yield database's own die-position helper (die centres, radius, zone by radius); it documents its
  functions and constructs no result.
- excursion_ticket_YE-2026-031.txt: the yield team's own ticket (symptom, request, three dated notes); it states no figure,
  names no suspect and says nothing of final test or the disk lots.
- pm_spec_history.md: the module's own spec history with waiver EW-118 (a two-PM trial of disk life) and the Rev G draft;
  it files the rules, dates and the lever (the WHAT), never a method.
- wafer_sort_zones.csv: the digits of one golden figure appear as two adjacent zone counts on one wafer's row, an
  ordinary record value.
Leak reader (stage 4, one isolated Sonnet agent at medium on fresh copies of the prompt and the pack): question 1
  quoted the prompt's two pins (the count's cost at sort and at final test; the parts fitted from September), the spec's
  intervals, the Rev G line and the waiver's retained disks, and the two filed conventions: each a WHAT, none a step;
  nothing pointed at the disk lots or at final test's shape. Questions 2 to 4: none beyond the Rev G draft's form, which
  the prompt asks for. Question 5: every quoted sentence executes to the golden. Question 6: no one thing. Its two
  realism tells (overlapping A140 serial ranges, routine log rows at exact weekly multiples) are fixed in the generator
  on their own random streams, and figures.json is unchanged by them. After the judge's fix pinned the causes' frame in
  the prompt, a second reader on fresh copies found nothing handed over either (question 6: no one thing; the waiver's
  retained disks point at the disk as the cause, which the careful column earns), and read the cost file's costing
  note and the Rev G draft's brackets as tidy: both stay, the note closing a determinism fork.
Realism: the deck rendered and read at speed; findings as titles, the charts as the slides, counts and onsets to ten
  wafers, die to the thousand, units to the hundred, dollars to the hundred or the thousand with each table's rows adding
  to its total, tables styled, slide numbers, source strips with the rounding stated.
Containers: audit_containers exit 0 (the pack's exports to 31 August, the deck stamped 8 to 10 September 2026).
Figures: figures_check exit 0; checks.py 89 of 89; verify.py 24 of 24 inside their bands by other code paths (its own
  parsing, a continuous hinge, the fallout on young disks, a general-optimiser likelihood for final test, the pad's
  sawtooth in the count); two builds byte-identical.
Caution on the paper: the cited pair is 23.0, and paper estimates have come back 40 to 60 points high; the lot link and
  final test's shape are each a judgment a careful run can make, and a run that makes the lot link earns R4 and R6 (35.5
  points on the house split).
Judge (stage 4, 2026-11-11): DETERMINISTIC, FIX_NOW (answer blocks): every graded figure reproduced inside its band;
  Gate G decomposition_attribution, analytical_non_defect, no surface-read dependency, no sole data defect; Gate H domain
  pass, layers pass, one_thing none; stump power 45 to 60. Fixed in one pass: the causes' frame pinned in the prompt ("the
  parts and tools behind it"), so the leak reader ran again; "the only lot left in stores" reworded to what the files
  show (the earlier lots' last serials fitted, no disk received since); the low pair's climb floor and the high pair's
  onset floor widened to reach a unit's own fit on its one short disk of the lot and the one-multiplier lot model (PU-4
  at 560); final test's bands widened to 15 per cent for a base read on young lots; the saving banded by pair; the side
  figures restated from the data (the classifier's wafers as a share of the loss, the pre-April baseline to one
  decimal, SC-4's first lots at M1 on 7 April).
Judge's blind first pass against the careful column: written before it opened the blocks, it landed the loss at sort
  (0.909 points, die by product), named the disk as the cause with every rival null but filed no share table, found the
  lot on its own (a hinge per unit with the lot as a multiplier: onsets 913, 900, 628 and 560, climbs 16.3 to 24.1) and
  the saving's total (about 556,000); it took final test in proportion to the sort hinge's excess (P-A 9,300 to 11,500,
  P-B 700, P-C 13,100 to 16,400) and so set the counts long (1,244, 1,235, 937 and 896). Re-priced on that pass the
  careful column earns R1, R4 and R6 with R2 in substance, about 51 to 58 on the house split, over the house's line of
  50 and under the client's 60. The author chose on 2026-11-12 to ship to measure, overriding the house's 50 line: the
  platform's two runs decide, and a run that models final test on the disk's wear lands nearly every result.

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
