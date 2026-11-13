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
   routine instruments), context artifact capacity_report (the ramp plan), forum executive_team (the fab management
   team that chairs the ramp readiness review), forcing event launch_or_rollout (VR90's production ramp, whose first
   lots reach the affected steps before the quarter), organisation manufacturer, role field_unit_lead, strategy
   forecast_method_backtest. Forum and forcing event were redrawn on 2026-11-13 after task1 v5 and task20 v3 filed
   committee_or_panel, a vote and a contract into the window, and the forcing event again after task22 v2 filed
   budget_or_appropriation; the management team and the ramp are what the plan of record itself names as deciding.
   The organisation family stays manufacturer by the author's override of 2026-11-13: `guard.py heart` BLOCKs it
   against task4's architecture 13 (a brewery), drawn in a parallel session at 02:07 UTC after this world was filed at
   01:31 UTC and sorted ahead of it by its card's local draw date; a semiconductor fab cannot honestly be another kind
   of organisation, and the two builds share no domain, analysis type, answer shape or structure.
7. Guard (re-registered 2026-11-13 with the redrawn axes): WARN only: overuse.forum (executive_team: here the fab's
   management team at the ramp review), repeat.gate_g, repeat.deliverables and repeat.question_form against the two
   builds filed just before, template.chain_near (task18 ranks an island grid's disturbance losses in an investigation; here the
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
  features cancel on the units that carry both, a hidden stock rebuilt from its flows and calibrated on a sparse second
  instrument, a wear rate identified on its true exposure against the counter that moved in step with it, and a yield
  read at a new support from block yields of the small die.
Swap: "the slurry loop's speed costs the far polishers most, the bench's metals build up between spikes, DP2B and CM3
  cancel on the wafers that run both, VR90-T's deep etch loads two chambers with polymer, and VR90's big die yields
  more than a die-area formula says" read with a hospital's or a retailer's nouns has no loop residence, thickness
  budget, drag-in and dilution, polymer per RF second or clustered defects per square centimetre to compute, so no
  result can be reached.
Where the weight sits: R2 to R5 (each cause found against the rival its first trace suggests), long because each needs
  its own file at its own grain read against the sort database's die and the lot and tool histories.
Layer 1: sort retests (the tester re-probes part of a wafer after a probe-card clean; 4 per cent of wafers), split and
  merged lots (rework), wafers scrapped before sort, each polisher's export in its own layout (CM1's clock four minutes
  fast, CM3's German-locale semicolon file), the slurry loop's trend exception-reported with two outages and a flow unit
  change to gpm at the April firmware update, back-entered PM rows and rows missing a counter, the bench controller in
  UTC on WB-2 with repeated lines after watchdog restarts, lab results below the reporting limit as text, lot IDs with a
  dot until the March MES upgrade, a network outage that left a gap in the etch export; none decides a result (checks.py
  R2 block).
Not one thing: the strongest single piece is the slurry loop's position effect (VR90's largest gain, 8.3 points); a
  run that nails it still has to find the bath's stock, the cancelling pair, the etch basis and VR90's die-area yield,
  each in its own files, and each moves its own graded figure past its band.
One-fact test: "the slurry loop's scratching grows with each polisher's distance along it" rescues R2, 1 of 7 results;
  every other hint rescues one result too (effort.json hints).
Not semantics: every field and unit read correctly still leaves the far taps' excess on CM1's and CM3's own consumables,
  the bath carried at the summer's loading, the edge on CM3's tune, the etch cleans on the wafer counter or on RF time
  alone and VR90 on a die-area formula.
Not rule application: no filed procedure attributes the shortfall, rebuilds the bath's metal, identifies the polymer
  load or reads a yield at VR90's die; the ramp plan states the quarter's operating conditions and nothing else.
Estimand: the prompt fixes the populations (VX40 and VP12 wafers sorted 1 June to 30 September 2026 against those
  sorted 1 January to 31 March; VR90's Q1 2027 wafers), the outcomes (good die per wafer; sort yield; wafer starts),
  each cause's VR90 figure as what fixing it alone adds under the ramp plan as filed, and the starts with every cause
  fixed; the ramp plan fixes the Q1 loading, settings, back-end yields and commitment.
No decoy: no memo, ticket or draft carries a cause, a share or a yield; the ramp plan states operating conditions and
  the commitment only, and no file ranks the causes.
No replay: no result re-derives a published figure; no stated number in the pack is simply wrong.
Pinned: each result's rivals are run on the cut pack (effort_passes.rivals: block yields read directly, each product's
  cluster fit alone, VR90 split evenly on CM1 and CM3, particle kill read from VP12, a straight GOI hinge, bin 5 pooled
  over VX40 and VP12 per mm2 of die, first insertions, the die-killed reading of each VX40 cost) and land inside the
  bands checks.py asserts; the world's own expected VR90 figures (forward.py) land inside every VR90 band too.
Run forecast: R2 stopped at the first story (the far taps' excess booked to CM1's and CM3's own filters and pads); R3
  method shortcut (the bath carried at the summer's loading); R4 dismissed own evidence (DP2B's thick edge set aside
  because its wafers yield well on average, then CM3's harmonisation taken as the fix); R5 method shortcut (cleans on
  the wafer counter, or scaled by RF time alone); R6 method shortcut (a die-area formula from VX40's die yield); R7
  unfinished chain.
Strategy label: Splitting a regression across changes that shipped together (Machine Learning Research 2), here a sort
  yield across four causes that landed in the same months, carried into the forecast the ramp needs.
Depth level: 5: five independent judgments (R2 to R6), each needing its own files and estimation, and the shortcuts land
  on eight different wrong VR90 answers (effort.json routes) with different wrong change lists.
Lesson: a yield attribution is finished only when each cause is modelled on its own physics (a feed's position, a
  film's budget across two steps, a bath's stock, a polymer's true load) and carried to the new product's die and
  quarter; no build on file teaches the etch basis, the loop, the cancelling pair and the support together.

## Results chain

| ID | Result (checkable) | Area | Pinned by | Band | Hurried analyst | Depends on | Graded as |
|---|---|---|---|---|---|---|---|
| R1 | The shortfall in good die per wafer sorted 1 June to 30 September against 1 January to 31 March: VX40 25.2, VP12 34.8 | assembly-reconciliation | the sort database's final insertion per wafer; the windows and products in the prompt | VX40 24.0 to 26.8; VP12 32.2 to 36.0 | method shortcut: first insertions kept (inside the band; earned) | - | Ask 1 |
| R2 | The scratch cause: the oxide slurry loop's flow, graded by each polisher's distance along it; 7.3 good die per VX40 wafer; fixing it alone adds 8.3 points to VR90 under the plan | investigation-loops | the loop's trend and line list, the August standby fortnight, the polishers' exports and sort bin 5 | VX40 6.7 to 9.0; VR90 7.5 to 9.7 | stopped at the first story: the far taps' excess booked to CM1's and CM3's own filters and pads, VR90's gain 5.0 | independent: the loop's trend | Component 1, Ask 2 |
| R3 | The bath cause: tank T3's metals under the July chemical life; 4.3 good die per VX40 wafer; the spring life alone adds 3.1 points to VR90 at the plan's loading | modeling | the bench controller log, the lab's samples, sort bin 6 and the gate oxide areas | VX40 3.7 to 5.6; VR90 2.3 to 3.7 | method shortcut: the bath carried at the summer's loading, VR90's gain 1.6 | independent: the bench log | Ask 3 |
| R4 | The edge cause: DP2B's thick edge and CM3's thin-edge tune cancelling on the wafers that run both; 10.6 good die per VX40 wafer; SH-300-B alone adds 0.76 points to VR90 under the plan | causal-reasoning | the deposition log, the polishers' exports, the PM and recipe logs, the 49-site maps, sort bins 3 and 4 | VX40 10.0 to 13.0; VR90 0.49 to 1.02 | dismissed own evidence: CM3's tune taken as the cause and its harmonisation as the fix, VR90's gain 0 | independent: the route records | Component 2, Ask 4 |
| R5 | The etch cause: CT-DEEP-07's polymer on ET1B and ET3A at 1.72 times per RF second; 2.1 good die per VX40 wafer; cleans every 1,420 wafers add 5.5 points to VR90 under the plan | forecasting | the contact-etch summary, the daily monitors, the wet cleans and sort bin 8 | VX40 1.5 to 3.0; VR90 4.9 to 6.0; interval 1,300 to 1,550 | method shortcut: cleans scaled by RF time alone (1,840 wafers, VR90's gain 3.1) or kept on the counter | independent: the etch record | Component 3, Ask 5 |
| R6 | VR90's Q1 2027 sort yield with every cause fixed: 65.3 per cent | missingness-measurement | January to March's bin 8 read in blocks of VX40 and VP12 die, VR90's own die, gate area and polish time, the plan's loading | 64.3 to 66.4 | method shortcut: a die-area formula (a cluster factor of 2 gives 62.8, Poisson 61.5) | independent: the January to March die maps | Component 4, Ask 6 |
| R7 | VR90's Q1 2027 sort yield under the ramp plan as filed, 45.4 per cent, and the wafer starts with every cause fixed, 3,520 | synthesis | R2 to R6 and the ramp plan's loading, settings, back-end yields and commitment | plan 43.7 to 46.4; starts 3,470 to 3,580 | unfinished chain: the hurried pieces multiplied give 52.1 per cent | R2, R3, R4, R5, R6 | Recommendation, Component 5, Ask 7 |

Carry-forward: R1 to R6 each stand on files of their own and are graded alone; R7 is graded against the golden and
falls with any of R2 to R6, so one missed cause costs its own result and R7, never another cause's result.

## Hidden factor record

| Factor | Real or constructed | Only in deciding units | Found by | Fix depth | Verdict |
|---|---|---|---|---|---|
| The loop's large particles growing with residence time to each tap | constructed (simulated physics) | no: all four polishers, all products, every period, graded by distance, gone on the standby pump | modelling (per-polisher rates against the loop's flow and the taps' distances) | modelling (the position effect carried to VR90's polishers) | keep |
| Tank T3's metals building between spikes and drain-and-fills | constructed | no: every lot through both benches, spring and summer, above threshold on some spring lots too | modelling (a replay of the controller log calibrated on the lab's samples) | modelling (the stock at the plan's loading) | keep |
| DP2B's thick edge and CM3's thin-edge tune | constructed | no: every DP2B wafer since April, every CM3 wafer since May, both products; the pair carries no excess | a targeted query by route, confirmed on the 49-site maps | modelling (what each fix does alone, on VR90's die) | keep |
| CT-DEEP-07's polymer per RF second | constructed | no: every cycle of ET1B and ET3A, on the monitors and on every product etched late in a cycle | modelling (the onset load and the factor fitted on cycles with different deep shares) | modelling (the clean interval at the Q1 mix) | keep |
| Defects clustering by wafer and region | constructed | no: every wafer of every product | modelling (block yields) | modelling (the yield at VR90's area) | keep |

## Effort test

| Result | Quick pass | Careful but hurried | Thorough |
|---|---|---|---|
| R1 the June to September shortfall in good die per wafer, VX40 and VP12 | Right | Right | Right |
| R2 the scratch cause: what it is, its cost per VX40 wafer and what fixing it adds to VR90 under the plan | Missed | Partly | Right |
| R3 the bath cause: what it is, its cost per VX40 wafer and what fixing it adds to VR90 under the plan | Missed | Partly | Right |
| R4 the edge cause: what it is, its cost per VX40 wafer and what fixing it adds to VR90 under the plan | Missed | Missed | Right |
| R5 the etch cause: what it is, its cost per VX40 wafer, what fixing it adds to VR90 under the plan, and the clean interval | Missed | Missed | Right |
| R6 VR90's Q1 2027 sort yield with every cause fixed | Missed | Missed | Right |
| R7 VR90's Q1 2027 sort yield under the ramp plan as filed, and the wafer starts with every cause fixed | Missed | Missed | Right |
| Roughly | 1 of 7 | 2 of 7 | 7 of 7 |

Measured by: .claude/skills/stumping/effort.py on generator/effort.json
Largest single hint: The slurry loop's scratching grows with each polisher's distance along it; rescues 1 of 7 results
Pair estimate: 25.7 (cited; every careful-column loss cites a precedent); each result carries its block's share plus
  its own seventh of the asks, because every result is also a sub-ask in Supplementary Questions

## Stump screen

| Candidate | 1 closed | 2 reflex | 3 filed | 4 clean data | 5 two grains | 6 assumption | 7 shallower story | 8 across | 9 worth | Kept or dropped |
|---|---|---|---|---|---|---|---|---|---|---|
| The slurry loop's scratching growing with each tap's distance (position on a network) | yes | yes | yes | yes | yes | yes (L38) | yes (L26) | yes | yes | kept: the polishers' own consumables are the story the per-polisher fit passes; the standby fortnight and the line list refute it |
| Tank T3's metals rebuilt from its drag, spikes and drains (a hidden stock) | yes | yes | yes | yes | yes | yes (N12) | yes (L28) | yes | yes | kept: the summer's bath carried to Q1 passes its own fit and misses the plan's loading |
| DP2B's thick edge cancelled by CM3's thin-edge tune on the wafers that run both | yes | yes | yes | yes | yes | yes (L01) | yes (L26) | yes | yes | kept: single-step commonality blames CM3 and files its harmonisation as the fix |
| CT-DEEP-07's polymer per RF second against the wafer counter (the true exposure basis) | yes | yes | yes | yes | yes | yes (N04) | yes (L37) | yes | yes | kept: cleans on the counter or scaled by RF time pass the standard chambers' back-test |
| VR90's yield read at its own die area from block yields (support) | yes | yes | yes | yes | yes | yes (N04) | yes (L22) | yes | yes | kept: a die-area formula passes on VX40's own die yield |
| Reticle haze repeating at one position in the exposure field | yes | no | yes | yes | no | no | no | yes | no | dropped: stacking fails by field position is a reflex and finding it is the remedy |
| Copper queue time with nitrogen stocker time excluded | yes | yes | yes | no | yes | yes | yes | yes | yes | dropped: the remedy is reading which stocker held the lot, a field read |
| Sort bins masked by the first failing test | no | yes | yes | yes | yes | yes | yes | yes | no | dropped: a later test's rate among die still at risk is the closed competing-risk lesson; it stays texture inside every band |
| Probe-card wear read as process loss | no | no | yes | yes | yes | yes | yes | yes | no | dropped: the closed instrument-change lesson, and retests already show it |

## Data provenance

Source: generated by task9/generator from a simulated process (world.py): lot starts for VX40, VP12 and VR90-T,
  dispatch with bay affinities and tool downtime, the oxide slurry loop's hydraulics and tote changes, the bench tank's
  chemistry, two film profiles, contact-etch polymer, clustered defects, sort binning on the first failing test, and the
  metrology, inspection and e-test sampling plans.
Behaves like the real thing: CMP micro-scratching rises with slurry large-particle counts and filter loading; bath metal
  contamination follows drag-in and bleed-and-feed dilution; ILD thickness at the edge is set by both deposition and
  CMP; polymer-flake adders rise past an accumulated load; defect clustering follows the negative binomial die yield.
Genuine patterns: (1) a weekly rhythm in lot starts and weekend bench loading (2) wafer-to-wafer and regional defect
  clustering with week-to-week variation (3) tote ageing sawtooth in the loop's particle count and a daily draw cycle in
  its flow (4) filter ageing on each polisher (5) the edge profile's radial shape (6) the bench's daily sawtooth
Problems by process: retests after probe-card contamination, rework splits, scraps, a controller replacement and a
  firmware update in the trend, a watchdog's repeated lines, two tools' clocks and one's locale, a network outage in the
  etch export, back-entered maintenance rows, values below the lab's reporting limit.
License: CC BY 4.0 (original work)
Used as is: not public data.
Breadth: 29 files (six tables in the yield database), 13,500 sorted wafers with die maps, 660 lots through 38 steps,
  four polishers, six deposition and six etch chambers, two benches, a loop of four taps; choosing which of them carry
  a cause is the work.

## Template check

Chain signature: assembly-reconciliation, investigation-loops, modeling, causal-reasoning, forecasting,
  missingness-measurement, synthesis
Question form: which (which causes drove the fall), then what (VR90's yield)
Nearest build: task18 (an island grid's disturbance losses ranked in an investigation): the same answer shape and weight
  (guard template.chain_near), but its chain, skeleton and decision form share nothing with this one (skeleton severity
  none); here the ranking is a bridge in good die carried into a new product's forecast at its own die size.

## Frontier check

Precedents: R2 L26, L38 (the far taps' excess on the polishers' own consumables, the loop's trend set aside as
  unrelated); R3 L36, N12 (a rate learned at one loading carried to another); R4 L01, L06 (DP2B's thick edge measured
  and set aside, one correction made and the second declined); R5 L36, N04, L37 (a transfer fitted on one recipe mix
  carried to another, its own back-test unable to see it); R6 L22 (the published die-area formula whose generating
  assumption the block yields contradict); R7 L32, L11 (the chain built and not carried into VR90's quarter). R1 is
  Right in the careful column.
Shallow path checks: R2's consumables reading passes a per-polisher fit with filter age (each polisher's excess holds
  within its own record) and is refuted by the standby fortnight, when every tap fell to its spring level with the same
  filters, and by the excess growing with distance in the line list; R3's summer reading passes its own fit of bin 6 on
  hours since the drain and is refuted by the controller log's lot counts, which put the plan's 31 lots a day beyond
  every day the summer ran; R4's CM3 reading passes single-step commonality (CM3's wafers fail bin 4) and is refuted by
  DP2B's wafers on CM3, clean, and its other wafers failing bin 3, which the 49-site maps confirm; R5's counter or RF
  reading passes a back-test on the standard chambers and is refuted by the monitors on ET1B and ET3A flaking earlier in
  every cycle that carried CT-DEEP-07; R6's formula passes on VX40's own die yield and is refuted by the block yields of
  VX40 and VP12, which fall far more slowly with area.
Assumption made false: a run lists "the polishers' excess is their own condition", "the bench behaves in Q1 as in the
  summer" and "the fleet clean interval holds for the new recipe" and waves them through; the standby fortnight, the
  plan's loading and the deep-recipe cycles in the record make each false, in the trend, the bench log and the monitors.
Forcing: the call is the change set (restore the loop, the spring chemical life, SH-300-B with CM3 harmonised the same
  day, deep-etch cleans before the polymer flakes); each change's VR90 quarter value is many times its cost (the
  smallest, the showerhead, about EUR 190,000 of die against EUR 77,000 of part and downtime); all six rival methods file
  the same set, every shortcut files a different one (eight distinct answers), and scratch rates, bath drag, the polymer
  factor and the thick-edge kill each moved 20 per cent either way leave the set unchanged (effort.json forcing).
Noun swap: nearest by skeleton task9's lineage and task22 v1 (a utility's feeder losses, position on a network in a
  ranked list under a cap), task7 v11 (a coincident peak with support), task4 (exposure basis in a flagged set): swapping
  their nouns in carries one lesson each and no decision form, detection set or file roles (severity none against each).
Closed strategies: the lesson the call turns on first is the etch polymer's true exposure basis (exposure_basis_decoupled,
  off the client's page and next to no closed card); none of the five lessons is closed or next to a closed card (the
  loop's position effect is a shared feed graded by distance, not a treated unit sharing a resource with controls; the
  cancelling pair is two process features offsetting on one wafer, not a co-occurring change in a comparison; the
  support effect reads a yield at a new area, not a widened alert bar), so no closed lesson needs a route of its own.

## Semantic fork table

| ID | Term or convention | Readings | Golden | Ruled out by |
|---|---|---|---|---|
| SF1 | "wafers sorted" in a window | first insertion; final insertion; by sort start or end | the final insertion's end | same call: the first-insertion reading sits inside R1's band (checks.py) |
| SF2 | "good die per VX40 wafer each cost" | the die the cause killed; the die its removal would recover | the die its removal recovers | same call: both readings sit inside each cause's VX40 band (checks.py) |
| SF3 | "what fixing each cause alone would add ... under the ramp plan as filed" | marginal on the plan; standalone against the fixed state | marginal on the plan | the prompt's words (each cause alone, under that plan) |
| SF4 | "with every cause fixed" for the etch | cleans before the polymer flakes; a cost-optimal interval allowing some flaking | before it flakes | same call: the difference sits inside R6's band at any interval the record supports |
| SF5 | VR90's polishers | CM1 and CM3 as VR90-T ran them; an even split | VR90-T's own shares | same call: the even split sits inside every band (rivals) |
| SF6 | the plan's bench loading | 31 lots a day per bench as filed | 31 | the ramp plan's own sentence |
| SF7 | the plan's CM3 recipe | R7 from 23 November, before VR90's first ILD0 lot | R7 | the ramp plan's own sentence |
| SF8 | back-end yields for the starts | 99.2 and 98.1 per cent | as filed | the ramp plan's own sentence |
| SF9 | the cluster model | a negative binomial fit; block yields read directly; one product's blocks alone | the joint fit | same call: every reading inside R6's band |
| SF10 | the rank | by good die per VX40 wafer | as asked | the four VX40 bands do not overlap (checks.py) |

## Closure table

| Axis | Closure |
|---|---|
| 1 | Population: VX40 and VP12 wafers by sort window; VR90's Q1 2027 wafers, all sorted after the plan's conditions take effect (the plan's own dates); C1 |
| 2 | Unit of account: good die per wafer for the shortfall and VX40's causes, yield points for VR90, wafers for starts; the prompt names each |
| 3 | Attribution window: by the final insertion's sort date; no wafer within a day of a window edge changes a figure past its band; C1 |
| 4 | As-of dating: the pull of 6 November; every figure uses records to then |
| 5 | Version basis: the final sort insertion; recipe revisions by their own change dates |
| 6 | Denominator: per wafer sorted; die at risk for the bin fits; C4 against the tested-die reading inside the bands |
| 7 | Weighting: every wafer equal within a window; C1 |
| 8 | Window length: the prompt's two windows; the loop's regimes read off its own flow |
| 9 | Boundary inclusivity: whole days, end inclusive; C1 |
| 10 | Rounding path: computed unrounded, rounded once at the answer blocks' precision |
| 11 | Tie-break: none needed; the four causes' bands are disjoint |
| 12 | Maturity and censoring: only sorted wafers are counted; lots unsorted at the pull are outside both windows |
| 13 | Order of operations: survival multiplies across mechanisms on each die; the marginal gains are read on the plan |
| 14 | Row order: no figure depends on file order; the bench replay orders by the controller's own time and sequence |
| 15 | Duplicate resolution: the controller's repeated lines carry the same sequence number and are dropped; retests by insertion |
| 16 | Identity normalisation: lot IDs with and without the dot are one lot; wafer by lot and slot in every export |
| 17 | Netting against gross: no netting; the residual is reported as the line's own variation |
| 18 | Dimensional units: the trend's flow in L/min then gpm, converted at the unit column; metals in ppb |
| 19 | Code and status semantics: bins by the database's own bin table; insertions by number; the controller's events by name |
| 20 | Integerisation: starts rounded to tens once |
| 21 | Clause scope: the plan's conditions apply to VR90's Q1 2027 wafers |
| 22 | Forward window contents: the ramp plan is the driver for Q1 2027 (loading, settings, chambers, back-end yields) |

## Literal reader

Executed word for word, the prompt's asks with the ramp plan's sentences give: the shortfall from each wafer's final
sort record in the two windows (R1); four causes, each with the good die a VX40 wafer loses to it and its fix (R2 to R5);
VR90's yield with every cause fixed (R6); what each fix alone adds under the plan as filed, and the plan's own yield and
the starts with every cause fixed (R2 to R5, R7). No sentence names a method, a comparison or a file.

## Prompt contract

A voice rewrite keeps: the two windows and two products; "rank the causes" with good die per VX40 wafer and the fix;
VR90's Q1 2027 wafers; "with every cause fixed"; "what fixing each cause alone would add ... under the ramp plan as
filed"; the plan's own yield; the starts with every cause fixed; a spreadsheet and a short note. It never adds a method,
a file name, a rounding instruction, a warning or who is asking.

## Pre-ship check

Ruled in the main thread on `leak.py --asof 2026-11-06`'s REVIEW lines (2026-11-13, the stage 4 cut):
- `shift_handover_ft2_2026.txt` is the FT2 shift book, written up shift by shift by the four crews' leads from what
  the floor saw (re-probes, holds, PMs and downs, bench controller restarts and alarms); it describes no data.
- The ramp plan's "300" is the showerhead part SH-300-C, not a figure.
- The ramp plan carries the call's distinctive words because it is the plan of record for the same tools: its table
  states each area's condition for VR90's quarter (twelve areas, of which four carry a cause), never a change to make
  or an effect, and it is the WHAT behind "under the ramp plan as filed".
- The stump-paragraph terms in the plan (slurry, cleans, conditions, quarter) are the field's own words for its areas.
- The ECN register's dates after the pull are the effective dates of approved changes (0466, 0473, 0480, 0487), the
  register's own forward column; every extract's latest record sits before its own export time (H16 check).

The first isolated read (2026-11-13, before the house pass): no sentence gives a method, no file ranks the causes,
no helper file, nothing reads as the answer; every question 5 sentence executes to the golden (the back-end yields
and gross die, the commitment in final good units, CM3 on R7 before VR90's first lot, the 21 per cent share, the
design-limited fallout matching the product sheet); question 6: no one thing, the plan's table the closest because it
lists the cause areas. Its six realism tells, each fixed in the generator: the plan's table now lists all twelve areas
VR90 runs through; the ECN register holds 31 changes across the fab's areas, numbered in the order raised (one row
renumbered to keep that order); the shift book is written from the floor's own events, in varied words, with a crew
rota of four leads; the MES cut-over of 2 March has its ECN and its shift-book line; the recipe log's follow-on
reasons are the engineers' own; the facilities log has three people and the lab a two-analyst rota.

The house pass found and fixed, each in the generator: one VP12 lot sorted after the pull (cut at the pull, 07:40 on 6 November,
asserted in checks.py); every lot split across both probers with a prober testing about fifteen wafers at once at a
fixed six-minute step (now one prober a lot, wafers in turn, re-probes after the card clean); the polishers', the
deposition chambers' and the etch chambers' logs stepping each wafer by a fixed interval (now each tool's own cycle
times, the realization unchanged); a technician sharing the controller's name (renamed); the bin 5 figures stated as
bin 5 per wafer but counted on die at risk (the answer blocks and golden now give the raw count with the at-risk count
beside it); house words in the golden's routes sheet (renamed).

The world's own expected VR90 figures (forward.py, 4,000 draws) against the bands: plan 44.5 in 43.7 to 46.4, every
cause fixed 65.4 in 64.3 to 66.4, the loop 9.15 in 7.5 to 9.7, the bench 2.94 in 2.3 to 3.7, the showerhead 0.63 in
0.49 to 1.02, the etch cleans 5.66 in 4.9 to 6.0. The causes' VX40 bands sit 1.1, 1.0 and 0.7 apart.

The first determinism judge stopped without a pass (no Agent tool in its runtime) and drafted a brief for a thread
that would derive its own answer cold before opening the blocks; that thread was not run (the STOP block's banned
reader), and the judge was re-run under its definition of 2026-11-13.

Judge pass 2 (2026-11-13): DETERMINISTIC with SOLUTION_WRONG on a figure basis, FIX_NOW. Reproduced: both shortfalls
(25.25, 34.84) and their first-insertion and all-insertion variants inside the bands, the causes' bands apart, the
polisher distances' monotone rise, the block yields' non-Poisson fall (about 0.75 to 0.76 at VR90's die), the starts
arithmetic. Its findings and their repairs: Critical Component 1 now names its windows by polish time (51.5 Hz before
2 June, 38 Hz from 2 June with the standby fortnight aside), which executes to 18.4, 47.8, 10.1 and 11.7 exactly; the
edge pair is pinned as one cause in ask 2 (neither change alone removes the loss); the recommendation now reads
SH-300-B on the day the plan takes CM3 back to R7; the closing passage names the gate oxide basis. Its third
surviving answer, VR90's polisher set inferred from ILD0-VR appearing only on CM1 and CM3, is now filed in the plan's
CMP row and ECN-2026-0480 (ILD0-VR qualified on CM1 and CM3 only), a WHAT pin that names no method. The plan changed,
so the pack is read again (read 3) and judged once more (pass 3).

Re-judge (report determinism_check_report_pass2.md): NOT_DETERMINISTIC, SEND_BACK on two narrow points, everything
else reproducing (both shortfalls and their variants, Critical Components 1 to 3, the causes' disjoint bands, the
1,420-wafer clean from the monitors, the plan loading, the starts arithmetic). F1: the plan's deposition row said "both
chambers of each tool on the qualified SH-300-C showerhead", which read literally puts all six chambers on SH-300-C
against the PM log's one replacement; the row now files DP2B on SH-300-C since 6 April, the other five on SH-300-B,
and no replacement due before the end of Q1 2027 (read 3 found the same sentence). F3: four VX40 die tiled from
January to March on CM1 and CM3 read VR90 with every cause fixed at 67.2 per cent, above the 64.3 to 66.4 band; the
tiling keeps VX40's 62-second polish against VR90's 76, 2026's bench loading against the plan's, VX40's own share of
CM3 and VX40's edge die (adjusted for the polish and the gate oxide alone it still reads 66.7), so Step 7 now gives
VR90's fixed yield part by part from named values and the closing passage rules the tiling out (asserted in
checks.py). Its SEND_BACK is treated as a repair, not a re-root: both points are closed by filing what the PM log
already holds and by stating the composition, with no graded figure moved; judged once more as pass 3.

Duplicate gate (2026-11-13, after rebasing on main): `guard.py heart` BLOCKed on two axes against cards filed in
parallel sessions. The forcing event was redrawn to launch_or_rollout (task22 v2 had filed budget_or_appropriation).
The organisation family stays manufacturer by the author's override: the BLOCK names task4's architecture 13 (a
brewery), registered at 02:07 UTC after this world's first registration at 01:31 UTC and sorted ahead of it by its
card's local draw date; a semiconductor fab cannot honestly be filed as another kind of organisation, and the two
builds share no domain, analysis type, answer shape or structure. The card carries the override.

Judge pass 3 (determinism_check_report_pass3.md): DETERMINISTIC, FIX_NOW in the answer blocks only. Reproduced: both
shortfalls with every insertion and clock variant inside the bands, the bin 5 windows exactly, the edge pattern, the
starts, the composition (65.4 from the rounded parts), the 1,420-wafer clean, the block yields' non-Poisson fall; the
Poisson, cluster-factor-2, tiling, consumables, RF-time and split-cause rivals each ruled out by named data or inside
the band. Its fix: Critical Component 2's share of VX40 wafers on DP2B and CM3 named no window and recomputed between
9.2 and 11.4 by the join used, so the share left the blocks and the note (it grades nothing; the 1.4 and 6.2 built on
it reproduce); Step 7 now names VR90-T's own split between CM1 and CM3, an even split being a rival held inside every
band. Read 4 (after the re-judge's repairs): clean of method, ranking, helper and answer leaks, every question 5
sentence executing to the golden; its five realism notes ruled in the leak report.

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
- 2026-11-13, architecture 3 as first cut (scratch base 17.5, drag 0.0046 ppb a wafer, thin-edge kill 0.44, each wafer
  on a random prober at a fixed six-minute step): the stage 4 house pass found a prober testing about fifteen wafers at
  once; scheduled lot by lot on one prober, the loop's and the bench's VX40 bands overlapped by 0.1 (a ranking fork),
  and the world's own expected VR90 loop gain (8.8 then 9.2 points) sat above the band, because 29 VX40 lots on CM3
  under-sample its scratch rate; reset to 18.2, 0.0043 and 0.48 (gaps of 1.1, 1.0 and 0.7 between the causes' bands)
  and the pooled VX40 and VP12 reading of bin 5 added to the rivals.
