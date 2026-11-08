# task8 design note

Status lives in `pipeline.json`; this note holds the design. Architecture 18, drawn 2026-11-08 after architecture 17
landed in both platform runs (`runs/triage.md`): a new world, dataset and shell in the same subdomain and objective. The
Prairie Adult Credentials Board, a not-for-profit awarding body in Winnipeg, certifies adult numeracy at Level 1 and
Level 2 for community learning centres across Manitoba and Saskatchewan. Candidates sit a 40-item online paper at their
centre on demand; each calendar year has its own paper, and every Level 1 paper's pass mark is set by the Board's Awards
Committee before the paper opens. The Board keeps one Rasch item bank for both levels, calibrated concurrently on every
paper sat since 2022. The 2027 Level 1 paper fills the patterns and relationships strand the 2026 revision of the
specification added with twelve long word problems from the Level 2 pool; the other 28 items come from the Level 1 pool.
The specification files the pass mark as the mark a candidate who just meets the Level 1 standard can be expected to
score on the paper, and the 2022 standard-setting record fixes that standard as 26 of the 40 marks on the 2022 paper.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task8.json` (architecture v18; lineage v1 to v17, v17 moved in with its
  fate and shell), registered 2026-11-08T05:32:52Z at WARN only, and `check` re-run on the registered card as the last
  act of stage 1 (WARN only). The two WARNs answered: the decision type (a dial) and the question form (what) repeat
  task2 v4, because the call is a pass mark, a value on one dial, and the form follows the decision; the shell is varied
  at the role level instead (the second sentence is led by the reader, the deliverable set is a memo and one workbook,
  and the workbook's two asks are a per-item table and a per-region mean mark). The structural tests read older-build
  repeats only (gap population, pattern G3, decomposition_attribution, a dial), each answered on the card's
  differentiation (mark101, mark178 lineage, mark469, mark121 lineage, mark464). A first draft with G14 leading
  BLOCKed `test.same_puzzle` against mark445 (population, G14, dial_setting) and was redrawn, not relabelled: the
  decisive pattern is G3 (record versus operation), the honester reading, because the bank records one difficulty per
  item and the decisive step is how a Level 2 item operates for a Level 1 candidate. The window when drawn: task2, task3
  and task6 (forum board_of_directors, regulator_or_inspector and executive_team; strategy grain_or_unit,
  forecast_method_backtest and population_selection; shape other twice, so a numbered shape) banned; this draw's axes
  are clear of them.
- **Pairing:** Education & Learning Sciences, task type `item-response-theory-test-equating`, which serves ETL. The
  response export of every online sitting since 2022 (two item-code schemes), the candidate register, the bank file with
  its preliminary and final 2026 runs, the paper layouts and the 2022 standard-setting record are conformed into one
  table of the 2027 paper's items, each with the difficulty it will have for a Level 1 candidate and its chance at the
  standard, from which the pass mark is read; shape 15 (fields to one schema: each 2027 item's source pool, bank code,
  difficulty for a Level 1 candidate and chance at the standard).
- **Strategy:** `decomposition_attribution`: each Level 2 item's shift for Level 1 candidates is split between two
  causes the bank file records for every item (its context, everyday or mathematical, and its stem's word count), the
  only split that fits the Level 2 items the 2023 to 2026 Level 1 papers carried. Not composition_mix (no population
  is reweighted), not population_selection (nobody is selected), not grain_or_unit.
- **Strategy label (`sulfur-strategies.md`):** WORKS IN FORM, separating two explanations for one pattern: the long
  everyday Level 2 items' unchanged difficulty for Level 1 candidates is either invariance or an everyday-context
  advantage cancelled by a reading cost, and only the like-for-like comparison with the short everyday items (the
  advantage alone) and the short mathematical items (neither) separates them; no dated cutover, no filed sentence.
- **Data-native sentence:** adult Level 1 candidates, older and more practised with money and measures than the
  apprentices and school leavers who sit Level 2, gain on everyday contexts and lose on long stems they read slowly,
  and the Level 2 items earlier Level 1 papers borrowed were short and long everyday items and short mathematical
  ones, so the two effects cancelled on the long ones; the 2027 paper borrows long mathematical items, which carry the
  cost with nothing to cancel it.
- **ETL pincer (guide-to-prompt 1):** the forcing files pin each item's context and word count (the bank file, kept
  for the blueprint and the accessibility review) and each response's level (the response export's paper code);
  reading them correctly is not sufficient, because the pass mark moves only when each Level 2 item's difficulty for a
  Level 1 candidate is estimated from the bridging items with both causes in one model and the link between the
  levels fixed on the items that carry neither, an estimation step no field or rule performs.
- **Abstraction sentence:** a fixed level's expected score on a new instrument is built from parts borrowed from
  another population's calibration, where the borrowed parts already used with the target population looked unshifted
  because two recorded features moved them in opposite directions, and the new instrument's borrowed parts carry only
  the feature that makes them harder. No approved or delivered build on file reads this way: mark450 screened anchor
  items one cause had moved (a curriculum change) and linked through the rest; mark445 read a choice advantage; mark474
  a retest gain on a common-person link; v6 a position term; v17 a taught state rebuilt from each school's calendar.
- **The decision and the quantity:** the 2027 Level 1 pass mark the Awards Committee sets at its 3 December 2026
  meeting before the paper opens on 1 February 2027, decided by the paper's expected mark for a candidate who just meets
  the Level 1 standard (26 of 40 on the 2022 paper) under the Rasch model, to the nearest whole mark.
- **Sources (all synthetic, shaped on Canadian adult basic education numeracy certification and Rasch pre-equating; the
  Board, the centres and the people are fictional):** the response export (the spine, one row per scored response of
  every online sitting 2022 to 2026, 400,052 rows); the candidate register (every registration, 10,550 rows, the long
  messy file); the item bank file (each item's pool, strand, context, stem word count, preliminary and final
  2026 Rasch difficulty and fit); the paper layouts 2022 to 2027 (positions to bank codes); the qualification
  specification (the pass-mark clause and the targeting band); the 2022 standard-setting record; the Awards Committee's
  September 2026 minute; the learning centres list; the committee chair's request email to the assessment manager;
  distractors, the 2026 learner confidence survey and the centres' computer suite audit.
- **People (guard.py names, en_CA, seed 8):** Yvette Clark, the Board's assessment manager (asks for the
  recommendation); Shawn Simpson, chair of the Awards Committee; Andrew Adams, the Board's psychometrician (keeps the
  bank). The seed 818 draw was replaced because two of its first names repeat older builds.

### The go/no-go screens (prototype, 16 redraws, before registration)

The prototype draws a Level 1 pool and a Level 2 pool, Level 1 papers 2022 to 2026 (the 2022 reference paper's items
reused on later papers, eight Level 2 items on each of the 2023 to 2026 papers: two short everyday, three short
mathematical, three long everyday), Level 2 papers 2024 to 2026 carrying those items and the twelve 2027 items, about
700 Level 1 and 1,600 Level 2 candidates a sitting; Level 1 candidates carry an everyday advantage of 0.8 logits and a
reading cost of 0.7 logits per 100 words; the bank is a concurrent joint maximum likelihood Rasch calibration of
everything. Measured over 16 redraws:

1. **The lever.** The truth's pass mark sits 2.3 to 3.1 marks under the bank's; the golden (both causes and the link
   in one model of the bridging items' shifts) lands within 0.4 of the truth every time.
2. **Every single-cause or screening route lands high.** Dropping the flagged bridging items (the short everyday ones)
   and re-linking: 1.7 to 2.3 marks high; crediting the everyday advantage alone (the 2027 items are mathematical, so
   nothing changes): 1.4 to 2.1 high; the reading cost alone (its slope flattened to 0.1 to 0.3 by the long everyday
   items' null): 1.7 to 2.4 high. The nearest rival sits 1.35 to 2.14 marks above the golden.
3. **The bridging items look clean.** Under the bank's Rasch model the long everyday items shift by -0.05 to -0.3
   logits on average for Level 1 candidates, the short mathematical ones by 0.0, and only the short everyday items are
   flagged (3 to 7 items of 32 at a 1.5 standard deviation screen).
4. To be measured on the generator (stage 2): fit parity of the Level 2 items on the Level 1 papers, the bank's
   prediction of every Level 1 paper's mean mark, every graded figure a quarter mark inside its bin, and the literal
   execution of every filed sentence filing the bank's pass mark.

## Default path

The opponent as measured: it conforms every file, reads every clause and runs the field's method on the bank.

1. Conform the response export (positions Q01 to Q40 to bank codes for the 2022 and 2023 sittings through the paper
   layouts, the later answer of a reconnect pair) and the register (one row per candidate who sat).
2. Read the standard as 26 of 40 on the 2022 Level 1 paper (the record, specification 4.1) and find the ability at
   which the 2022 paper's test characteristic curve reaches 26 on the bank's final 2026 values.
3. Sum the 2027 paper's chances at that ability on the bank's values: 21.57, a pass mark of 22.
4. The careful run checks the Level 2 items earlier Level 1 papers carried before trusting the bank: calibrating each
   level on its own and screening the shared items' displacement (median and robust spread, a cut at 2), it finds the
   short everyday items easier for Level 1 candidates, sets them aside and re-links on the rest (21.12, a pass mark
   of 21); crediting the everyday advantage alone moves nothing on the mathematical 2027 items (20.81,
   21); pricing stem length alone, its slope flattened by the long everyday items' null, gives 21.35 (21).

- **Ends on:** a pass mark of 22 (the bank's final 2026 values, expected mark 21.57 at the standard), and
  21 on every careful variant.
- **Golden:** a pass mark of 19 (expected mark 19.09 at the standard).

## Stump sentence

The bank's final 2026 values put the 2027 paper's expected mark at the standard at 21.57 and its pass mark at
22, and every careful variant (screening the shared items and re-linking, crediting the everyday advantage,
pricing stem length) files 21, because the Level 2 items earlier Level 1 papers carried looked unshifted where
it mattered: on the long everyday ones an everyday advantage and a reading cost cancelled; the 2027 paper's twelve long
mathematical items carry the reading cost with nothing to cancel it, and only a model of the shift with both causes and
the constant between the two scales fitted together prices them, which files 19.

## Deep reasoning

- **Task type:** item-response-theory-test-equating: pre-equating a new Level 1 form's pass mark through a Rasch item
  bank, which serves ETL (the response export, the register, the bank file, the layouts and the 2022 record conformed
  into one table of the 2027 items).
- **Domain test:** the expected mark on the 2027 paper of a candidate at the Level 1 standard, by Rasch true-score
  pre-equating: the ability at which the 2022 paper's test characteristic curve reaches 26, then the 2027 paper's test
  characteristic curve at that ability.
- **Swap:** "a hospital's 2027 triage cut-off, set as the score a patient just at the admission threshold can be
  expected to reach on a new checklist built partly from items scored on another ward's patients": the arithmetic
  survives the swap but nothing that decides does, because there is no stem a patient reads, no everyday-against-
  mathematical context and no second level of candidate for whom the same item operates differently.
- **Layer 1:** the response platform keys the 2022 and 2023 sittings by paper position and later ones by bank code
  (its 2024 upgrade) and keeps both rows when a candidate reconnects and re-answers (about 1.2 per cent of sittings);
  the register carries centre uploads beside regional office entries (one sitting twice), withdrawn and absent
  registrations, dates of birth in three formats and centre codes in several shapes; the bank file carries the June
  preliminary run beside the final one. Nothing is placed to be caught, and every careful run cleans it the same way.
- **Layer 2:** decomposition attribution, separating two explanations for one pattern: the shared items' unchanged
  difficulty on the long everyday ones is invariance or two recorded causes cancelling, and the choice flips the call.
- **Decisive step:** splitting each shared Level 2 item's Level 1 difficulty less its Level 2 difficulty into a constant
  between the two scales, a cost per 100 words of stem and an everyday-context advantage, fitted together on all the
  shared items, and carrying the split to the twelve long mathematical items by their own stems.
- **Not semantics:** every field read right (the pool, the context, the stem's word count, the paper codes, the 26 on
  the 2022 paper) still leaves the bank's values on the 2027 items, because no field records how an item operates for a
  Level 1 candidate: that is a relation between two levels' responses to the same items, estimated, never read.
- **Not rule application:** no filed rule says how a Level 2 item transfers to Level 1 candidates; executing the
  specification's clauses and the record's 26 on the bank files 22. The enumerated family (the bank 21.57,
  the screen and re-link 21.12, context alone 20.81, length alone 21.35, the two-cause model in linear, logarithmic
  and step forms, weighted or not, on joint or marginal likelihood 19.09 to 19.29) spreads 2.48 marks; the
  standing family (the forms the shared items do not reject) spreads 0.20 marks inside one whole mark; the
  ruling-out is loud in the residuals by item kind (mean absolute 0.076 logits for the joint model against 0.208
  for context alone and 0.269 for length alone).
- **Analyst test:** the strong analyst conforms everything, reads the 26, pre-equates on the bank's final values and
  files a pass mark of 22; the careful one screens the shared items, sees the short everyday ones drift easier,
  sets them aside and re-links, or credits an everyday advantage the mathematical 2027 items never get, and files
  21.
- **Estimand:** "The pass mark on each Level 1 paper is the mark that a candidate who just meets the Level 1 standard
  can be expected to score on that paper, rounded to the nearest whole mark" (specification 4.2), the standard being
  the one fixed on the 2022 Level 1 paper (specification 4.1; record LN1-SS-2022: 26 of 40); the paper is the 2027
  Level 1 paper as laid out in the layouts file.
- **No decoy:** nothing is planted: the bank file is the Board's real calibration and right for what it calibrates (one
  concurrent scale), the preliminary run is a dated run the Board keeps, and no memo, draft or stakeholder figure
  carries 22 or 21.
- **No certified replay:** no published figure is re-derived: the 2027 pass mark has never been computed, and the
  2022 record's 26 is an input, never a target the method is recovered from.
- **Chain:** (1) the 2027 paper's twelve patterns items come from the Level 2 pool, and their bank values rest on Level
  2 candidates' responses; (2) the Level 2 items the 2023 to 2026 Level 1 papers carried show how such items operate for
  Level 1 candidates once each level is calibrated on its own; (3) their shifts need an everyday advantage and a
  reading cost together with a constant between the scales, because the short everyday items move and the long
  everyday ones do not; (4) the 2027 items, long and mathematical, take the constant and the reading cost only; (5) the
  ability at the standard on the 2022 paper and the 2027 paper's curve there give 19.09, a pass mark of 19.
- **Judgment:** the modelling judgment that the shared items' shifts are additive in two recorded causes rather than
  invariance with outliers or one cause, justified from the data: the short everyday items sit -0.83 logits from
  the short mathematical ones and the long everyday ones -0.20, and the joint model's residual (0.076) is under a
  third of either single cause's; stem length varies inside every kind of shared item, which carries the fit to the
  long mathematical items without an untested interaction.
- **Hidden by:** two effects offsetting inside the observed window: on the long everyday items, the commonest shared
  items, the everyday advantage and the reading cost cancel, so the shared items look unshifted on average, the bank's
  concurrent calibration fits them, and the only drift in view (the short everyday items) reads as outliers to set aside.
- **After the notice:** once a run sees the short everyday items drift, (1) it must ask why the long everyday items,
  also everyday, do not (wrong turn: set the drifting items aside and re-link on the rest, 21); (2) it must fit
  both causes and the constant between the scales in one model on all the shared items (wrong turn: credit the
  everyday advantage alone, which leaves the mathematical 2027 items where the bank has them, 21, or price length
  alone with its slope flattened by the long everyday null, 21); (3) it must carry the fit to each 2027 item by
  its own stem and context and read the standard on the Level 1 values (wrong turn: shift the twelve items by the
  shared items' mean drift, which is near nothing).
- **One-fact test:** the likeliest hint, "Level 2 items do not play the same for Level 1 candidates", is what the
  field's screen already acts on, and it files 21; even "long stems cost Level 1 candidates" leaves the run to
  separate the cost from the everyday advantage, fix the constant between the scales and carry both to the 2027 items,
  and length alone files 21. No one sentence does the estimation.
- **No replay:** the call re-derives no published figure, and no shipped number is wrong: the bank's values answer the
  bank's question.
- **Pinned:** every rival run on the clean truth: the bank 21.57 (22); the screen 21.12
  (21); context alone 20.81 (21); length alone 21.35 (21); the two-cause model linear 19.09,
  logarithmic 19.12, step 19.29, unweighted 19.09, marginal likelihood 19.09, all 19; the standard read on the
  bank's 2022 values 19 (SF2); the most likely mark at the standard 19 (SF3); the truth 19.16.
- **Run forecast:** one run pre-equates on the bank and stops (method shortcut at rung 0, 22); the other
  screens the shared items and re-links, or credits the everyday advantage alone (unfinished chain at rung 1 or 2,
  21); a run that fits both causes still pools every region on one ability scale and loses the regional
  figures (dismissed own evidence: the regions' different everyday advantages in the same sittings).
- **Strategy label:** WORKS IN FORM, separating two explanations for one pattern; the live form here is two recorded
  item features whose effects cancel on the commonest shared items, with no dated cutover and no filed sentence.
- **Lesson:** a model learns that a bank's invariance on shared items can be two causes cancelling and that a borrowed
  item is priced by the causes it carries; no build on file teaches a two-cause population shift through a test link
  (mark450 screened anchors one cause had moved, mark445 read a choice advantage, v6 a position term).

## Survivor anatomy

- **Actor:** the item (a bank code) has rows in every file; the deciding property, how a Level 2 item operates for a
  Level 1 candidate, has no column anywhere: it is a relation between two levels' responses to the same item.
- **Link:** it is read only by calibrating the Level 1 and the Level 2 sittings each on their own and differencing the
  same items across the two, a comparison the concurrent bank exists to avoid; no key or file offers it.
- **Reflex:** the field's reflex is pre-equating on the bank's one scale (rung 0) and, done carefully, a displacement
  screen on the shared items (rung 1); both are executed correctly and file 22 and 21.
- **Back-test:** the bank passes its own checks: the shared items fit it, and its values predict every earlier Level 1
  paper's mean mark, because the earlier papers borrowed the cancelling kind.
- **Second use:** the same split drives the item table's band verdicts (5 patterns items below the band, none on
  the bank) and, with each region's own everyday deviation, the regional figures.
- **Shock:** nothing happens on a date: the shift is a standing property of two populations, and the 2027 paper is the
  first to borrow items carrying one cause without the other.
- **Pins:** the WHAT is filed in the Board's genre (the specification's pass-mark and band clauses, the record's 26 of
  40); nothing names the two levels' difference, the shared items, stem length or context as a cause of anything.

## Readability screen

| Rung | What the rows in view show | Verdict |
|---|---|---|
| 0 the bank's values | one difficulty per item on one scale, fit statistics that pass | readable |
| 1 the displacement screen | the short everyday items drift easier for Level 1 candidates; the rest look unshifted | readable |
| 2 one cause (context or length) | a context effect on the short items, a length slope near zero | readable |
| 3 the two-cause split (decisive) | no column, no sentence: only the two calibrations differenced across the three kinds of shared item, with both causes and the scale constant fitted together | silent |
| 4 the regions' own everyday deviation (ask) | no column: each region's 2026 candidates' pattern on everyday against mathematical items, read against a 2027 paper with fewer everyday items | silent |

Test 8 (framing): neither the prompt nor any governing document states how the 2027 items' history differs from the
decision's population on the axis the step corrects: the specification's strand table states the content change and
the bank's pool column each item's origin, both facts about items; nothing says the 2027 items were calibrated on Level
2 candidates, that stems cost Level 1 candidates, or that regions differ on everyday items.

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "can be expected to score" | the expected mark (test characteristic curve) at the standard's ability, under the two-cause split | the split's other forms (logarithmic, step, unweighted) and the marginal-likelihood calibration | 19 in every form (19.09 to 19.29) | same call, asserted in checks.py (SF1, a fifth of a mark inside the bin) |
| SF2 | "the Level 1 standard" | the ability whose expected mark on the 2022 paper is 26, on the Level 1 calibration | the same ability read on the bank's 2022 values | 19 | same call, asserted (SF2) |
| SF3 | "expected to score" | the expected value of the mark | the most likely mark of a candidate at the standard | 19 | same call, asserted (SF3) |
| SF7 | the item table's chance and band verdict | the chance at the standard's ability; inside means at least 0.20 and at most 0.90 (specification 5) | edges read strictly; rounding before the verdict; another form of the split | the same verdict for every item | no chance within 0.048 of an edge and the verdicts identical over the forms, asserted (SF7) |
| SF8 | "sat the 2026 Level 1 paper in that region" | the region of the centre sat at | the region of the home centre | the same regional means | every sitting away from home is within its home region, asserted on the cut pack (SF8) |
| SF9 | the regional mean mark | the mean over the region's 2026 sitters of each one's expected mark on the 2027 paper, to the whole mark | maximum likelihood abilities; the joint likelihood's stretch undone in part or in full | the same whole marks | asserted over the family (SF9; the narrowest margin 0.01 of a mark) |
| SF11 | the 2026 population | each candidate who sat, once (the register's repeat entries and its absent and withdrawn rows aside) | counting register rows | the same sittings | the response export carries exactly the sittings the golden averages, asserted on the cut pack (SF11) |
| SF12 | the centring of the regions' everyday deviations | centred on their mean weighted by each region's Level 1 responses, 2022 to 2026 (every sitting carries 40), stated in the Step-by-Step | centred on their plain mean (the judge's Parkland and North 16.53, so 17) | with the difficulties re-estimated under it, the same regional means to four decimals; re-centred on the golden's difficulties, every region about 0.16 higher (Parkland and North 16.38 here) | named data: the centring is an identification constraint, so re-estimating under the plain mean moves the everyday items' difficulties by the same constant and no regional mean (asserted, SF12); re-centring without re-estimating is not a fit to the response export, its Level 1 log-likelihood 24.0 lower (asserted, SF12) |
| SF13 | the regions' deviations on the 2027 paper | applied to the 2027 paper's everyday items as to every everyday item the region's candidates meet, stated in the Step-by-Step | dropped on the 2027 everyday items (the judge's Winnipeg 15.69, so 16; here Westman 15.40, so 15, and Interlake-Eastman 16.50) | other whole marks in some regions | named data: the same drop on the 2026 paper's everyday items misses the regions' observed 2026 mean marks in the response export by up to 1.45 marks (Parkland and North; Winnipeg 1.12, Interlake-Eastman 1.10), while the deviations reproduce every region within 0.04 (asserted, SF13) |

## Ladder

| Rung | Route | Expected mark at the standard | Pass mark |
|---|---|---|---|
| skip | the 2022 standard carried as a mark | (26 of 40) | 26 |
| 0 | pre-equating on the bank's final 2026 values | 21.57 | 22 |
| 0p | the bank's June preliminary run | 21.56 | 22 |
| 1 | the displacement screen, the drifting items set aside, re-linked | 21.12 | 21 |
| 2a | the everyday advantage alone | 20.81 | 21 |
| 2b | stem length alone | 21.35 | 21 |
| 3 (decisive) | both causes and the scale constant fitted together, carried to the 2027 items | 19.09 | 19 |
| truth | the generating model | 19.16 | 19 |

The nearest rival sits 2 marks above the golden's whole mark.

## Closure table

| Axis | Reading | Move |
|---|---|---|
| 1 Population | Level 1 candidates on the 2027 paper; the standard as fixed on the 2022 paper | filed: specification 4.1 and 4.2 |
| 2 Unit of account | the mark; a candidate for the regional means | filed by the clause and the prompt |
| 3 Attribution window | sittings 2022 to 2026, the 2026 papers closed on 30 October | C1: every sitting is complete before the export |
| 4 As-of dating | the export of 6 November and the bank's final run | C1: the golden calibrates from responses and reads no bank value |
| 5 Version basis | the bank's final run against its June preliminary | C4: both file a wrong pass mark; the golden uses neither |
| 6 Denominator | the 40 items of the 2027 paper | filed: the layouts' 2027 sheet |
| 7 Weighting | the shared items weighted by precision or equally | C1: weighted and unweighted both 19 (SF1) |
| 8 Window length | every shared item on a 2023 to 2026 Level 1 paper | C1: each shared item sits on one Level 1 paper; nothing licenses a shorter window |
| 9 Boundary inclusivity | the band's "at least" and "at most" | C1: no chance within 0.048 of an edge (SF7) |
| 10 Rounding path | the expected mark rounded once, at the end | filed: specification 4.2 |
| 11 Tie-break | none needed | C1: the expected mark sits 0.21 inside its bin |
| 12 Maturity and censoring | the 2027 candidates are future; the estimand is a standard candidate's expected mark | filed: specification 4.2 |
| 13 Order of operations | the split fitted in one model, then carried | C4: the sequential single-cause fits are the rungs 2a and 2b |
| 14 Row order | none | C1: no estimator here depends on row order |
| 15 Duplicate resolution | a reconnect pair's later answer, the one the platform scores | texture: about 1.2 per cent of sittings, one or two items each |
| 16 Identity normalisation | the register's candidate id across the centre and office routes | C1: one sitting per candidate and paper (SF11) |
| 17 Netting against gross | none | not applicable: no quantity offsets another |
| 18 Dimensional units | logits on each level's own scale | C1: the constant between the scales is estimated with the split |
| 19 Code and status semantics | Sat against Withdrawn and Absent; Level 1 and L1 | C1: only Sat registrations have responses (SF11) |
| 20 Integerisation | whole marks for the pass mark and the regional means | filed by the clause and the prompt |
| 21 Clause scope | the band applies to each item on a Level 1 paper | filed: specification 5 |
| 22 Forward window contents | the 2027 paper's 40 items | filed: the layouts' 2027 sheet |

## Literal reader

Executed word for word, the specification's 4.1 and 4.2, the record's 26 of 40 and the prompt fix the population,
outcome, unit and rounding; the literal reader that pre-equates on the bank's values files 22, an easy method on
the same literal estimand, never another reading of it. Every term's alternatives are in the fork table and land on the
golden's figures or converge on the records; the method stays open and the data force it, because the shared items
reject invariance (the short everyday items' -0.83), the screen (it leaves the long everyday items' null unexplained)
and each single cause (residuals 0.208 and 0.269 against 0.076).

## Oracles

None ships. No control total, published figure or validation record ties under the golden: the bank's own fit
statistics pass the shared items, the 2022 record's 26 is an input, and the preliminary run is a dated run that files
its own wrong mark. No file ranks pass marks.

## Ask sheet

- **Ask A, the item table (40 rows, rides the decisive step):** each 2027 item's chance at the standard and its band
  verdict. On the bank's values no item sits below the band; on the golden 5 patterns items do (Q29, Q30, Q31, Q32, Q33, at
  0.11 to 0.14), the other patterns items sit inside at 0.25 to 0.40, and none sits above. Graded as
  the verdicts and the patterns items' range, because the forms of the split move single chances by up to 0.048.
- **Ask B, the regional means (6 regions, its own judgment):** the regions differ in how much easier everyday items are
  for their candidates (estimated deviations Winnipeg -0.31, Westman +0.07, Interlake-Eastman +0.31, Parkland and North +0.41, Saskatoon and Central -0.10, Regina and South +0.10 logits), the 2026 paper is everyday-heavy and the 2027 paper
  everyday-light, so one ability scale for every region carries each region's everyday advantage onto a paper that
  rewards it less. Golden Winnipeg 15, Westman 16, Interlake-Eastman 17, Parkland and North 16, Saskatoon and Central 17, Regina and South 17; one scale for every region Winnipeg 14, Westman 16, Interlake-Eastman 18, Parkland and North 17, Saskatoon and Central 16, Regina and South 17 (4 of 6 regions on another
  whole mark); the bank's values Winnipeg 16, Westman 18, Interlake-Eastman 20, Parkland and North 19, Saskatoon and Central 18, Regina and South 19 (6 of 6).
- **Pair ceiling:** 45.4 (landed run 74.6, shallow run 16.2; both runs on the call would average 74.6).
- **Shallow keep:** 7.7 per cent of the ask weight.
- **Measured by:** task8/generator/ceiling.py on the cut pack (writes generator/ceiling.json).

| Ask figure | Golden | Landed run (the split, regions pooled) | Shallow run (the bank's values) | Cracker verdict on the landed run |
|---|---|---|---|---|
| items below the band | Q29, Q30, Q31, Q32, Q33 | Q29, Q30, Q31, Q32, Q33 | none | keeps |
| items above the band | none | none | none | keeps |
| the patterns items' chances | 0.11 to 0.40 | the same | higher | keeps |
| Winnipeg | 15 | 14 | 16 | misses |
| Westman | 16 | 16 | 18 | keeps |
| Interlake-Eastman | 17 | 18 | 20 | misses |
| Parkland and North | 16 | 17 | 19 | misses |
| Saskatoon and Central | 17 | 16 | 18 | misses |
| Regina and South | 17 | 17 | 19 | keeps |

## Prompt contract

A voice rewrite may not drop or change: the question (the pass mark the Board should set on its 2027 Level 1 Numeracy
paper); the clause it is held to (the mark a candidate who just meets the Level 1 standard can be expected to score on
that paper); pass_mark_2027.docx as the memo to the Awards Committee; l1_2027_items.xlsx with one row for each item on
the 2027 paper, the chance a candidate who just meets the standard answers it correctly and whether it sits inside the
specification's targeting band; for each region, the mean mark the candidates who sat the 2026 Level 1 paper in that
region could be expected to score on the 2027 paper; the pass mark and the regional means to the nearest whole mark and
the chances to two decimal places. It may never add Level 2, the item bank, stems, reading, length, context, everyday
items, shared or common items, linking, calibration, drift, differential functioning, any region's name or count, or
any hint that the regions or the two levels differ.

## Architecture 17 record (spent 2026-11-08)

The Corlinn Schools Assessment Trust's choice among three draft Year 10 science papers for the November 2027 sitting
(education-learning-sciences, item-response-theory-test-equating, composition_mix): the bank's Term 3 items had been
calibrated at the August 2026 sitting, when about nine in ten of their responses came before the candidate's own school
had finished the unit, and recalibrated on the taught responses they put Paper C nearest 25 at the Achieved standard
(A 25.89, B 23.02, C 24.80) against the bank's Paper A (24.78, 20.64, 21.58). The asks were each region's entries,
sittings, make-up sittings and mean make-up mark. Shipped 2026-11-08 (judge DETERMINISTIC, APPROVE on round 2, target.zip
02c4e9b7). On the platform's first round both runs filed Paper C and every regional figure: run 1 fitted a joint
conditional Rasch model with a coverage contrast for each Term 3 unit, run 2 kept the Term 3 responses after each school
finished the unit; the prompt's August-against-November gap announced the mechanism, the course outline and Appendix
B's per-school sequences handed over the join, taught-content adjustment is a textbook IRT reflex, and each ask device
was a hygiene item both runs caught. The full record is in `pipeline.json` (`lineage_v17`) and `runs/triage.md`; its
stage-4 reports are kept as `determinism_check_report_arch17.md` and `leak_check_report_arch17.md`.

## Architecture 16 record (spent 2026-11-07)

Brackwell Alloys' 2026 product-family direct emissions for Velden's 2027 low-carbon premium (physical-environmental-
sciences, emissions-inventory, decomposition_attribution): the homogenizing furnace's gas allocated by its loads' firing
hours, not their tonnes, put 6082 billet at 0.263 over SCR-2's 0.235 and the premium at EUR 342,000 against the
per-tonne route's EUR 456,000. Shipped 2026-10-31 (judge DETERMINISTIC, APPROVE; target.zip 433ff500), reshipped
twice on 2026-11-07 for PDF provenance, and returned FAILED_TO_STUMP the same day: both portal responses filed EUR
342,000 on the firing-hours allocation, the method a careful analyst reaches for, which the hourly gas fitted at
R-squared 0.9985; the portal also flagged Domains Fit. The full record is in `pipeline.json` (`lineage_v16`).

## Architecture 15 record (spent 2026-10-31)

Architecture 15 priced Pembrook Castings' 2027 employee dental maximum under its Finance Policy F-17: each maximum's
cost per covered person month on the 2025 plan year at the 2027 fees, against Board Resolution 2026-31's 1.90 dollars.
The golden added back the predetermined work members at the 1,500 dollar maximum put off to the January reset, which
put 3,000 dollars over the limit and filed 2,000. The stage 4 judge returned NOT_DETERMINISTIC with SEND_BACK and the
reconciliation confirmed a withheld rule: F-17 executed word for word on the 2025 claims gives 0.83 and 1.23 dollars
and files 3,000, and no shipped text adds the put-off work; the asks left the put-off column's total, the deductible on
34 lines, "still in treatment" and an orphan case open. Its world (a manufacturer's self-insured dental plan) is left
with it, and its report is kept as `determinism_check_report_arch15.md`.

## Architecture 14 record (spent 2026-10-31)

Architecture 14 elected the Larrowbrook Physician Network's 2027 two-sided track practices: each practice's 2026
network measure carried from the October interim run by its own 2025 run-out at the same cut, plus the members in
hospital stays still running on 31 August, which the hospitals bill at discharge and the feeds show only as the
physicians' daily charges, each past the 250,000 dollar member cap (Mallowcrest Pediatrics' neonatal triplets,
Garrowdale Family Practice's trauma family). It shipped 2026-10-25 (zip 2c0f8d35, judged APPROVE on 04486b1a) with
eight practices entering. The repair's judge pass 2 returned FIX_NOW: two graded thresholds a cent off, the 2025
measures within a third of a cent of a rounding edge. The re-judge found the write-up's claim that all seven stay
members were past the cap by 31 August false under a pooled per-day reading (4,535.53 dollars a day against the
per-kind 6,380), the call's margins thin and the stay amount unfiled: a FIX_NOW that failed its second pass, which
spends the architecture. Its world (a clinically integrated network's risk track) is left with it.

## Architecture 13 record (spent 2026-10-25)

Architecture 13 elected the Larrowbrook Physician Network's 2027 two-sided track practices: each practice's 2026
network measure on the payers' final 2026 attribution, projected from the October interim run by the practice's own
2025 run-out at the same cut, against the default path that takes the interim measure as the 2026 figure (Ostrelwood,
Thornelfield and Jesselford alone, against the golden nine). At stage 4 round 1 (zip ab79a5f44c18f637) both scored
readers landed the call (exit 1): each read the prompt's "projected to the payers' final 2026 attribution" beside the
standard's attribution rules as a population the October run cannot hold, re-ran the October 2025 interim run on the
2025 claims with the standard's own rules and the Appendix C factors, and carried each practice's interim measure by
its own 2025 final-to-interim ratio. Reader A kept all 78 ask figures (Kesselcrest's reviewed 99215 visits at the
99214 rate out of level 5, Merrinlake's halved modifier-25 visits counted by their code, Pemberglen's coverage month
from its payment reference, Kesselcrest's Medicare Advantage lines at 6.50 out); reader B kept every benchmark,
threshold and ask B figure and no ask A figure. The judge thread was stopped at the spend. Asked to project an interim
figure to a final one, a careful reader takes last year's interim-to-final ratio, the field's completion reflex, and a
standard whose rules can be re-run on last year's claims hands it that ratio in one pass.

## Architecture 12 record (spent 2026-10-24)

Architecture 12 certified the Quillmere Lake basin's 2027 Seasonal Communities Aid: each city's average population
present in its busiest month of the measurement year read from its plant's influent BOD load divided by the load per
person its own January to April 2026 fix, against the default path that counts residents plus the paid stays the fee
returns and both platforms record (Sorrelton and Esker Narrows alone, USD 1,200,000 each, against the golden's five
cities at USD 480,000 each). At stage 4 round 1 (zip be45d7b75ea5cc24) both scored readers landed the call (exit 1):
each read the Act's "every other person staying in or visiting the city" as a population no record holds, went to the
one file that measures everyone (the plants' influent), divided the load by 0.17 lb a person a day (the population
equivalent the world had been tuned to agree with), checked it against the residents in winter and filed the five
cities; both also counted Kettle & Pine's nights back from the departure in its reference (reader A all 32 of ask A,
reader B 26 of 32 on half-dollar rounding) and missed only the pond systems' flow basis in ask B. The judge thread was
stopped at the spend. A statute that defines the population as everyone present, beside records that plainly hold
only the paid stays, sends a careful reader looking for a measure of everyone, and a pack whose influent rows have
no other use hands it one.

## Architecture 11 record (spent 2026-10-24)

Architecture 11 settled Lumenfold Learning's 2025-26 outcomes guarantee district by district, each partner district's
share of eligible students at or above Proficient on a matrix-sampled spring science assessment re-estimated from its
students' own two-module answers with the district in the population model, against the default path that averages
the contractor's five plausible values by district (19 districts owed USD 32,045.00 against the golden's 16 owed
USD 25,493.75). At stage 4 round 1 both scored readers missed the call, reader A kept all of ask A through the
catalog's hours per session, and the judge's pass 1 returned FIX_NOW on a cent tie in the credits (seat prices moved to
whole half dollars). In round 2 reader C refitted the 2PL latent regression from the item responses with district in
the conditioning model, validated it on the contractor's Table 6, filed the golden 16 districts and USD 25,493.75 and
kept every ask figure: a conditioning model that leaves out the grouping variable is a reflex for a reader who knows
plausible values, so the architecture was spent.

## Architecture 10 record (spent 2026-10-24)

Architecture 10 accrued each Medicare hospice provider number's FY2026 aggregate cap repayment at the December 2026
close, each beneficiary counted under the proportional method on the days to come from their state at the close (an
open stay by its length so far, a live discharge by its time out, returns read at every hospice from the benefit
periods extract), against the default path that runs the open stays on and takes the live discharges as finished
(Fallowmere USD 0.3 million against nothing). At stage 4 all four isolated readers across two rounds missed the call
and the round 1 judge returned DETERMINISTIC, APPROVE; the round 2 judge returned NOT_DETERMINISTIC, SEND_BACK
(margin_or_boundary_fragility and competing_defensible_answer): the printed 0.3 needed Fallowmere's count inside a
window of 2.9 beneficiaries while independent builds of the projection scattered about a beneficiary either way, and
the pool start, the number of later elections and the Kaplan-Meier tail were left unfiled (0.248 to 0.447 on the
judge's variants); ask A's routine-paid days read as an unstated rule. A designation set would have held (every variant
put Fallowmere above its cap); a figure printed to USD 0.1 million on a three-beneficiary window did not.

## Architecture 9 record (spent 2026-10-23)

Architecture 9 read each station's Schedule C availability from the bikes in working order docked, each bike's spells
rebuilt from the trips and fleet moves and a bike counted out of working order from the end of the ride that left it
when renters passed it over and a van then took it to the depot for a day or more, against the status feed's available
count (W-02, W-12, W-16 and W-19 against W-16 alone). At stage 4 (zip 14ceb178) both scored readers missed the call:
reader A subtracted the reported bikes and the bikes mechanics took in without a report, inside the inspection windows
(W-16 and W-19); reader B subtracted the reported bikes only (W-16). Both kept nearly every ask figure (65 and 64 of 74,
exit 1): the sales export's present-location column undone through the work orders' terminal replacements, and the
alarms ended at restarts once the clear pairing ran to hundreds of hours with sales inside them. The isolated judge
thread returned NOT_DETERMINISTIC, SEND_BACK, competing_defensible_answer (Gates B, C and E): no shipped file says that
unreported broken bikes exist or how to find them, so the records read literally (the feed, or the rebuild with the
reported bikes out) file W-16 alone, and the depot-stay cut and the pass test sit only in the solution's steps (at 36
and 48 hours W-17 and W-19 move by a point); Gate G `planted_defect_flip`, `surface_read_rejection`,
`surface_read_dependency: yes`, `sole_data_defect: yes`; Gate H `decisive_step: planted`.

## Architecture 8 record (spent 2026-10-23)

Architecture 8 carried each store's data logger record through the vaccine's thermal lag, a first-order response
fitted per logger make on the two weeks each pilot store's old logger kept recording beside its new in-carton sensor
(42.2, 42.2 and 41.9 minutes), against the loggers' readings taken as the vaccine's temperature (six stores against
ten). At stage 4 (zip ad958ec9) reader B set the pilot stores' loggers beside their in-carton sensors over the overlap
unprompted, fitted the lag as a first-order filter (0.21 of the gap closed per ten minutes, about 42 minutes) and
landed the six stores and every store's whole hours, answering question 6 "an analytical choice" on standard 7.2; it
kept every ask figure too (122 of 122 graded figures, exit 1): the counts' own closing times, the credits found when
per-item balances went negative, the vial write-offs by cost over the per-dose cost, the tax switch by the
maintenance-only invoices at Schedule B's prices, and the two-store routes split by Schedule B. Reader A and the judge
thread were stopped at the spend.

## Architecture 7 record (spent 2026-10-23)

Architecture 7 read each production day's oxidizer outlet from the relation the ten oxidizers' tests trace (a floor of
about 45 ppmv as carbon, 1.8 per cent of the inlet above about 2,500) at the inlet the day's captured VOC and airflow
imply, against each plant's latest test efficiency (Ashcombe 21 and Kelvedon 20 against 29 and 28). At stage 4 (zip
5ab18e48) reader A read the floor straight off the test tables (Ashcombe's 2018 two-press test holds the same 45 ppmv
at half the inlet), rebuilt each hour's outlet as the greater of the floor and 1.8 per cent of the inlet and landed the
five and all 14 whole tons, Part 2 question 1 "none" and question 6 "an analytical choice"; reader B carried each
fixed-fan unit's test outlet to the year through the register's fan-drive column (R4, six plants). Both readers kept
all 28 ask figures: the revision log read, the payment lines parsed, Haldane matched on description. The judge thread
was stopped at the spend.

## Architecture 6 record (spent 2026-10-22)

Architecture 6 set Form 27A's placement scores from the bank difficulties carried from the old platform's field-test
section (positions 61 to 70) to the positions 21 to 70 the unique items take on Northgate Assess, by the position term
the 2026 attempts measure, against the default path's difficulties as filed (29 and 18 against 30 and 19). At stage 4
reader A rebuilt every response at its delivered position, fitted the Rasch model with the anchor block fixed, found
items harder later in the test on both platforms and landed 30 and 19 exactly (29.48 and 18.50), Part 2 question 1
"none" and question 6 "an analytical choice"; it kept 13 of 62 ask figures (the system totals and some twice counts).
Reader B and the judge thread were stopped at the spend.

## Architecture 5 record (spent 2026-10-22)

Architecture 5 designated rapid price growth areas on each dwelling type's own year effect weighted by the census
stock's value, with a pooled hedonic year term as the default path. At stage 4 both readers and the judge's own
derivation took the type-by-stock aggregation by reflex (type medians or type year effects weighted by the census
stock) and missed the call only on the location control (electoral division), which the judge read as unfiled; filing
it hands all three the call, so the decisive step as designed does not stump and the one that held is a fork.

## Tried and rejected
- Architecture 6, item position effects in pre-equating (2026-10-22, spent at stage 4): reader A fitted a Rasch model
  with a position term to the rebuilt attempts and carried the field-test difficulties to Form 27A's positions,
  unprompted by any sentence. The calibration context has to be recoverable for the truth to be fair (the report's
  delivery section and both exports' positions), and once it is, an analyst who knows the field checks the effect the
  context invites; a context effect measured by an obvious model term is a reflex for the field's own analysts.
- Architecture 6 draw (2026-10-22): re-rooted on the author's standing rule (no retirement) with a fresh world. Screened
  before it and dead: a CEMS gap fill on load (guard BLOCK on pattern G12 and strategy population_selection against
  task273, same-puzzle and same-driver spent in five to seven builds, the statutory filing against task249);
  multiplicative against additive seasonality (task146, task147); a moving holiday (task162, task467, task135);
  Denton benchmarking (this slot, below); retroactive eligibility as a denominator still developing (the completion
  driver of task451 and task479 v5); Fellegi-Sunter frequency weights (set aside at task486's draw against task468's
  linker error); the oldest old by extinct generations (task228); non-detects under several limits (task189).
- Architecture 5, the stock's price change as each dwelling type's own year effect weighted by the census stock's
  value (2026-10-22, spent at stage 4): both readers and the judge's first derivation weighted dwelling types by the
  census stock by reflex (the note's "dwellings the 2022 census counts" and the census workbook by type invite it) and
  missed only on the electoral-division control, which the judge read as unfiled (r5a); filing it hands them the call.
  A stock aggregation over a tabulated type mix is a reflex once the stock is the filed population.
- Architecture 5 draw (2026-10-22): re-rooted on the author's standing rule (no retirement); the world and pack of architecture 4 kept, the decisive step moved from the constant-quality regression its reader 9 found to the aggregation that regression skips (each type's own year effect over the stock's value), with the pooled regression now the default path. At registration the v4 identity BLOCKed on own_lineage, gap population on same-puzzle and same-driver (task251 v5), shape 10 and the statutory filing (task249 v6) and filed_standard (task478 v4); redrawn as recorded in the Draw, the circular changed to settle the 2027 fund allocations.
- Ask B's reissued student ids as a 7-digit id equal to the old one plus a campus constant, linked by birth date, sex and ZIP (2026-10-21, stage 4 round 1): both readers resolved it on the person columns and kept all six headcounts (score_reader 50 per cent); re-sited so the new ids share the old form with no arithmetic tie, birth date, sex and ZIP are shared by different students, and the movers' majors are recoded, so only the four-field key resolves it.
- Architecture 1, a coordinating board's instructional grant with four parents' consolidated returns apportioned by a cost model (2026-10-21, spent at stage 4): round 1's two readers split by FTE or total credit hours and missed; both round 2 readers fitted instruction expense on credit hours by level across the standalone campuses, split each parent's return by the modelled cost and landed the call (exit 1). Pricing activity by level from the units that report alone is a strong reader's reflex once the activity file by level ships beside the combined return.
- Architecture 2, regional register error rates from an audit drawn unequally by a risk screen (2026-10-21, spent at stage 4): both readers checked the audit's composition against the register (35 per cent referred against 8), weighted each stratum to the 30 April register and landed the call; both also read the UTC times into local time and dropped the restored companies (asks 28 of 28). A sample whose composition differs from its frame on a shipped flag is reweighted by a strong reader; a stated clock and a restoration notice are seen devices.
- Architecture 3, registration offices put on a timeliness plan from a quarter's median working days with part of the quarter still open at the extract (2026-10-21, spent at stage 4): both readers censored the open applications at their age, took the Kaplan-Meier median and landed the call, and dated payments by the batch terminal day (asks 28 of 28). An open caseload shipped beside a duration cohort, with a paper saying the open ones count, is read as right-censored by a strong reader; a settlement batch file carrying the terminal day is a seen device.
- Architecture 4, areas' house price change for the rapid price growth designation read from a shifting sample of the stock (2026-10-21, spent at stage 4): reader 9 fitted log price on type, floor area, age, newness and the address point file's electoral division with a year term and landed the call; reader 10 left location out and missed; the block purchases' one consideration on every line held both readers (0 ask totals of 32). A constant-quality index is a strong reader's reflex once the note cites the handbook and the attributes ship; location one join away is not a hidden dimension.
- A district's register error rise tested with the spread of the audit's sampled blocks (2026-10-21, screened at the draw): the guard put it beside task261 (subgroup statistics from one clustered sample, their difference's error from the clusters), the same driver.
- Regional quarterly output benchmarked to annual totals by Denton against pro-rata (2026-10-21, screened): Denton's extrapolation holds the end-of-year ratio, which sits within a few tenths of a point of pro-rata's annual ratio, while a trending ratio puts the truth far from both; the separation is too small and the truth not recoverable without forecasting the ratio.
- Architecture 7 draw (2026-10-23): re-rooted on the author's standing rule (no retirement) with a fresh world.
  Screened before it and dead: gross labour-force flows corrected for reinterview misclassification (task244's
  driver); speededness on a timed form (task249's screen); a winner's curse in form assembly (task471's shrinkage
  coin flip); generic price erosion by entrant count (task484 v1's ramp, screened at task478's draw); percent-of-charges
  hospital contracts carried to each hospital's current chargemaster (the swap test reads it as any list-price
  contract); laboratory results harmonised by proficiency-test bias (the reported result is the measurement, so the
  correction is a fork); a cancer registry's completeness by the flow method (task249's screen); common-stack
  apportionment from single-unit hours (task263's unmixing); a concentration-discharge load (task452 v1, task135);
  change of support for block grades (task270, task254, task273 screens); linkage on an address the outcome changes
  (task468's linker error); calculator-type DIF and released-item drift on the item bank (architecture 6's lesson: a
  context an obvious model term measures).
- v7 stage 3, 2026-10-23: the first tuning let each oxidizer's test outlet carried to the year (its concentration on
  each day's air, or its rate over the year's hours) file the golden five, because a fixed-fan plant at the floor emits
  the same rate every day; Larkmoor Graphics was made a concentrated-test, mostly-dilute plant under 25 tons so those
  routes file six (R4, R4m, R4b).
- v7 stage 3, 2026-10-23: press VOC to one decimal: the standing family spreads up to 0.37 tons on a plant, so the
  figure is graded in whole tons, every member 0.19 tons or more from a half (G4); the CSV's used and captured
  columns went with it (free to both top responses), the CSV now the press VOC and coverage.
- v7 stage 3, 2026-10-23: the tuned plants landed on whole tons (29.00, 37.00); moved to ordinary offsets (G5). Days
  below the tests' lowest inlet at three plants opened an extrapolation fork (interpolated efficiency against the
  floor); the low days were raised inside the tested range.
- Architecture 7, 2026-10-23: spent at stage 4. The decisive relation was visible inside one oxidizer's own tests (the
  same outlet at two inlets) and in the register's fan-drive column, and a regenerative oxidizer's outlet floor is
  field knowledge both readers carried; the asks' devices each sat one file away from a careful reader's path (the
  master's revision log in the same workbook, the washer gallons in readable payment text, descriptions beside the
  renumbered items). Next architecture: a decisive step no table displays as a pattern and no column labels.
- Architecture 8 draw (2026-10-23): re-rooted on the author's standing rule (no retirement) with a fresh world, aimed
  at architecture 7's lesson (no table displays the decisive relation, no column labels it). Screened before it and
  dead: vessel propulsion from AIS speed over ground carried to speed through the water by an estuary's tidal streams
  (a port world beside task472 and task474, and a tidal stream table has no other use in an emissions pack, so its
  presence announces the correction); container ships' at-berth auxiliary load by the reefers on board, calibrated on
  shore power meters (a port world, and a reader calibrating on the meters sees the per-call spread with reefers its
  first explanation); a tanker's boiler load at berth by its own steam cargo pumps on discharge (the at-berth tanker
  rules' own reasoning, a reflex once the transfer log is joined); dairy lagoon methane through the lagoon's
  temperature lag behind the air (the rate model is a filed procedure, and four inspection readings a year cannot fix
  the lag deterministically); switcher locomotives' idling through the start-stop system's restart temperature (a
  rate carried across a weather covariate, task478 v7's driver); crematory mercury by the decedents' dental cohort (a
  composition mix one survey table hands over); breaker SF6 leak rates from temperature-uncompensated pressures (the
  gas temperature at each reading is not recoverable). A cold-chain prototype (thirty-six refrigerators, probe 6 minutes,
  carton 48) put the logger's own hours at two to ten times the vaccine's, the default qualifying 29 against 12, with
  a 45-minute lag fitted on ten fourteen-day overlaps at 0.04 degrees C reproducing the carton's set exactly, while 30
  and 60 minute duration filters (17 and 6) and a 45-minute moving average (20) fell elsewhere and a 90-minute moving
  average missed by one refrigerator: the stage 2 world keeps the default's count plausible and every store clear of the
  line under the standing family.
- v8 stage 3, 2026-10-23: standard 7.1 first read "the records of each store's device of record are its vaccine
  temperature records", which a literal reader takes as the logger's readings being the vaccine's temperature (an
  official decoy for the default path); it became a records-custody clause.
- v8 stage 3, 2026-10-23: under the interval-mean reading of a record's vaccine temperature five stores' whole hours
  moved by one while the call held; 7.3 now files the counting (a record counts its ten minutes by the vaccine's
  temperature at its time stamp), WHAT and not HOW (SF17).
- v8 stage 3, 2026-10-23: return credits from both manufacturers put the cracker's balance below zero at eleven
  stores, a loud failure that points at the double count; only Halvorsen's standard-dose products are returnable, the
  leftovers leaner and the unrecorded losses scaled to each store's volume (cracker 15 doses or more, A6).
- v8 stage 3, 2026-10-23: maintenance-only invoices at one price per unit type tied ten stores' service figures (a
  constant response would have kept them); per-model prices and add-on parts at some visits, every store's figure now
  distinct (B5). With the tax switch as ask B's only silent device a reader who found it kept 23 to 30 of 30; the
  pre-move two-store maintenance routes on one invoice were added, so the tax switch alone keeps 10.
- v8 stage 3, 2026-10-23: the first names sat on real organisations, products or places in or near the field (H21):
  Coldline (a refrigeration manufacturer), Polarwatch (an ocean-data programme), Vaxtor, Homeline, Arctis, Glacier
  Medical, and the acquired chains Rookwood Drug and Saltash Apothecary; renamed Tellvane, Brumal, Stellane, Keswell,
  Brannon, Pendry Medical, Vollmer Drug and Lindqvist Apothecary before any reader saw the pack.
- Architecture 8, 2026-10-23: spent at stage 4. Two instruments recording one unit side by side are compared by a
  strong reader on reflex: the pilot stores' logger and in-carton series parted at every restock and defrost swing, so
  reader B fitted a first-order lag on the overlap with no sentence asking for it. Every ask device had one natural
  check that exposed it (per-item balances, cost per unit, a list price met exactly, one invoice on two sites).
  Next architecture: a decisive step whose evidence no single side-by-side comparison shows, and ask devices that no
  per-item reconciliation or unit-price check reveals.
- Architecture 9 draw (2026-10-23): re-rooted on the author's standing rule (no retirement) with a fresh world. Screened before it and set aside: phantom shelf inventory under a vendor-managed availability guarantee (on-shelf availability is an industry term that names its own correction); a plan directory's ghost providers read from claims (the directory and the claims sit side by side, architecture 8's reflex); a starting dose as the mark of a true initiator in an outcomes contract (population_selection, in the window against task275); rectifying inspection's over-weighted rejected lots (population_selection again); left truncation of a fleet's lifetimes (task133's delayed entry for a taken-over book); GPS chord distance by terrain for fuel-tax jurisdiction miles (the call would sit on a few per cent of one state's miles); meter error read off a system balance (the instrument-bias family task478 v5 and task480 v1 lost to readers); charger uptime from failed sessions (the failure is written in the session record itself). The bike-share draw keeps the listed count correct for what the operator knew and puts the difference in renters' choices, which no record states.
- v9 stage 2, 2026-10-23: the fleet's clock ran four hours off Eastern time after the move to absolute instants (its
  local minute of the day counted from midnight UTC), so the pack showed the morning rush at noon; the window's start was
  re-anchored to 20:00 on 23 September so the fleet's own clock is Eastern time, the trajectory byte for byte the same
  (46,883 trips), the station move and the dock expansions read at 23:00, and Schedule C's minutes taken from Eastern
  time itself; the designations held (W-16 alone against W-02, W-12, W-16, W-19).
- v9 stage 2, 2026-10-23: each station's three months to one decimal put nine of 72 cells within two minutes of a
  printed edge and W-12's lowest month (87.652) within a minute; graded at each station's lowest month in whole per cent
  instead (the tightest ten minutes clear, M1), the margin to one decimal (0.684, eleven minutes), the monthly figures
  kept in the workbook as context.
- v9 stage 2, 2026-10-23: ask B's hours to one decimal put W-18 within a second of an edge; graded in whole hours, each
  pay station's alarm stream chosen so its figure sits 0.08 hours or more inside its bin (M3).
- v9 stage 2, 2026-10-23: the union of overlapping alarms as ask B's device: at whole hours the summed and merged
  spans print alike at every station; kept as texture (B3), the restarts carrying the device.
- v9 stage 2, 2026-10-23: with only the alarms and restarts in the log, ending an open alarm at the pay station's next
  event of any kind kept 15 of 24 hours figures (the restart was nearly always the next event), an honest pair of 45.7;
  the cabinet heater's events on cold days and the service door at reader repairs added, the shortcut keeps 4 (33.1).
- v9 stage 2, 2026-10-23: invented names screened by web search (Wellhaven, Northlane Mobility, Corlund Kiosk
  Systems): no organisation, product or place on any of them in or near the field; Welland, Ontario is three edits away.
- Architecture 9, 2026-10-23: spent at stage 4 on the judge's SEND_BACK. A count the operator's system publishes as
  available, read against a state no record holds (a bike's working order inferred from what renters and the vans did
  with it), is a surface read rejected however the evidence is gathered: on clean data the feed would be right, so the
  judge files Gate G surface_read_rejection and Gate H planted, and with nothing filed saying unreported faults exist
  the records read literally give the feed's answer (competing_defensible_answer). The readers missed the call for the
  same reason the judge refused it. Both ask devices were found: a column filled from a present-day register is undone
  by a work-order log that lists every swap, and a pairing that runs alarms to hundreds of hours with sales inside them
  announces its own repair. Next architecture: a quantity every file visibly lacks (so no surface read stands in for it),
  estimated by a method the data forces, and ask devices whose wrong reading is plausible rather than absurd and whose
  evidence no log lists outright.
- Architecture 10 draw (2026-10-23), no card filed. The guard's window closes survey research for ETL (ban.pairing and
  ban.subdomain against task483, so census-register and seasonal adjustment are both out) and the strategies grain_or_unit,
  population_selection and composition_mix (task483, task275, task179); payment claims, emissions, IRT equating and data
  integration clear it. Screened on those four and dead on file or on measurement: competing exits against censoring
  (task169, task266; the competing exit is a reflex, task133); pooled-test infection rates (task188); age-length keys
  (post-stratification, a reflex once the aged subsample's design ships); a pooled tail share from parts' means and spreads
  (task483's lesson); a population's share past a cut from short matrix-sampled booklets (task464's shrinkage lesson);
  direct against indirect adjustment of a net series (task453 v2's fork); time-series consistency by splicing (task123's
  screen); chance agreement on name and birth date in a voter roll (task468's common-identifier lesson); credibility for
  site emission factors (the regulatory standard takes the site's own tests, a fork); tracer flux ratios (the integrated
  ratio is the method's own definition, so the default is the golden); flows traced through intermediaries to end markets
  (task451 v1's swap failure); uncompensated gas meters (a unit read, data semantics); correlated systematic errors in an
  activity-data uncertainty (the call is a monitoring decision, Data Quality); cohort waits from cumulative counts under
  first-in-first-out (generic queueing, the swap reads the same); a pick log matched to put-aways by each lane's access
  order (drive-in lanes are last-in-first-out, field knowledge a strong reader carries, architecture 7's death).
- Architecture 10 draw (2026-10-24): drawn on the hospice cap after a second screen of the four open ETL task types (survey research still closed by task483). Screened and dead: TRI range codes valued at the exact filings inside each range (the midpoint is the programme's own convention, a competing defensible answer, and the exact filings are one group-by away); charge compression in cost-plus repricing (the implant invoices put the cost-to-charge ratio against the charge in plain view, and the functional form forks); a stopped turbine's nacelle anemometer read through the running transfer function (readers impute from neighbours by habit, and Gate G reads an instrument bias as planted); unconstrained demand on sell-out days (the product-limit estimator is a reflex and converges with the intraday route); time-of-observation bias in daily maxima (the calendar-day maximum is not recoverable from a 5 p.m. reset and the nearest hourly station); trend uncertainty with shared emission factors (propagating through the difference carries the shared factor by construction, so the easy route is right); items dropped from scoring rescored through the test characteristic curve (the published conversion table replays the method); best-of-k seed reports deflated by each recipe's seed spread (the client's GSDS Layer 1 list names best seed against mean as harmonisation); inverter clipping, demand ratchets and dead-time counting losses (each leaves a flat top or a ceiling in the records that announces its correction); unit value against a fixed-basket price index for provider unit cost (composition_mix, banned against task179 for this registration); DIF purification, testing-window instruction time and single-group order effects in equating (field reflexes, or no bias in the equating); register status nowcast by a Markov chain (forecasting, and architecture 9's surface-read refusal); interpolation along a process curve between sparse readings (task478 v6's and task480's degradation and life-cycle families). The first card draft BLOCKed on test.same_puzzle against task171 v4 with G13 decisive; G12 is the honest decisive generator for the step that decides.
- v10 stage 2, 2026-10-24: a lifetime projection with Brackwater, Lindmoor and Wexmoor owing beside Fallowmere: the
  standing family (Aalen-Johansen or empirical return chances, three valuations of a return, the open stays' later
  returns overall or from their time so far) moves each core program's cap by USD 30,000 to 70,000 against cells of
  USD 100,000, and the overall-rate route kept three of the four amounts; the core programs were placed under the cap
  and Fallowmere carries the call alone (nothing accrued on the default path, USD 0.3 million on the golden).
- v10 stage 2, 2026-10-24: pooled models across provider numbers and a split by discharge reason each moved
  Fallowmere's count by up to 1.3 per cent on cells of small programs; the policy files the reference class (the same
  provider number and diagnosis group), and Fallowmere's seller's system records no revocation against discharge
  reason, so the reason split is not available for its history.
- v10 stage 2, 2026-10-24: with return stays as long as first stays the overall rate times the census average landed
  the golden's cell (0.325 against 0.300); re-elections run shorter (the beneficiary comes back in decline) and seldom
  end alive again, so that route files 0.53 and the census-average valuation by time out 0.19.
- v10 stage 2, 2026-10-24: the outside share of Fallowmere's returns was raised from a third to four in five, so the
  route that reads returns from Elderglen's own records files nothing (cap ratio 0.971) instead of landing beside the
  golden.
- v10 stage 3, 2026-10-24: the organisation and program names Elderglen, Brackwater, Corrinbrook, Dunsmere, Lindmoor,
  Pennacott, Sallowfield and Wexmoor sat within two edits of real places in the GeoNames register (Eden Glen,
  Blackwater, Swallowfield and Fallowfield, Dunmore and Dinsmore, Wyndmoor, Dixmoor) or carried a place word (Penna,
  and Cornbrook in Manchester two edits from Corrinbrook); renamed Wendleglen, Brindlemoor, Corvelfield, Darrelbrook,
  Marrellford, Rennickdale, Varrowmere and Farrinridge in the generator, every figure unchanged. The lines above keep the
  names they were written with.
- v10 stage 4 round 1, 2026-10-24: both scored readers missed the call (each ran the open stays on and took the
  live discharges as finished, nothing accrued) and the judge returned DETERMINISTIC, APPROVE (Gate G analytical, Gate H
  pass); reader A joined the claim lines to the remittance register and kept all 24 ask A figures (exit 1), so the
  device that the latest version is not the paid one sat off the careful path. Re-sited: the contractor's prepayment
  review pays some held inpatient days at the routine rate, visible only by repricing the paid version, with the
  returned replacements kept as a hazard and moved more than 118 days before the close (reader B had priced them as
  pending, cutting payments); the census report's length-of-stay table, blank on a group key mismatch, now prints.
- v10 stage 4 round 2, 2026-10-24, architecture spent: both fresh scored readers again missed the call (open stays
  run on, live discharges finished, nothing accrued) and kept 0 of 24 ask figures, but the judge thread returned
  NOT_DETERMINISTIC, SEND_BACK (margin_or_boundary_fragility, competing_defensible_answer): Fallowmere's printed 0.3
  needs its count inside 177.6 to 180.5, a window of 2.9 beneficiaries (USD 0.1 million at the cap amount and 98 per
  cent), while independent builds of the same projection scatter about a beneficiary either way (0.248 to 0.311 on the
  judge's variants, 0.279 to 0.314 on the standing family), and it named four choices the policy leaves open (the
  Kaplan-Meier tail, one later election or several, stays begun before 1 October 2016, the last provider number when the
  open stay is at another hospice); it also read ask A's routine-paid days as an unstated counting rule. Lesson: a cap
  repayment printed to USD 0.1 million moves a cell every 2.9 beneficiaries of count, so a projection whose honest
  spread is a beneficiary cannot print one cell; the next architecture's call has to be a quantity whose cell is wider
  than its estimator family's spread, measured on independent builds rather than on the author's own family.
- 2026-10-24, architecture 11 draw, screened on paper before any code against v10's lesson (a call whose cell is wider
  than its estimators' measured spread): Medicare Advantage post-payment recoupments or denial overturns for a
  hospital's 2027 contract notices carry v10's latent structure (a terminal-looking state that is not final) and
  task451's (amounts still to arrive).
- Architecture 11 draw: Medicaid procedural reinstatements and COBRA retroactive elections: retroactive eligibility was
  screened at task451 and task479 v5, and COBRA's selection is population_selection, banned against task275.
- Architecture 11 draw: ACA risk adjustment transfers estimated from competitors' public prior-year transfers: carrying
  a competitor's risk forward is a fork; ACA grace-period cures: rule-heavy, with the cure rate carried across the 2026
  subsidy expiry.
- Architecture 11 draw: censored transplant costs by inverse probability of censoring weights: mature cohorts are
  unbiased without a trend, and a trend makes the stump a dated step; authorization- or ADT-based claims reserves: the
  completion family, and a leading indicator is a reflex.
- Architecture 11 draw: price-standardised total cost of care tiers: the standardisation is a WHAT (filed is rule
  application, unfiled a fork); deductible leveraging is task479 v3's driver; prescription abandonment by out-of-pocket
  cost: the lever is too small; stop-loss and high-cost claimant pooling: non-linear aggregation at claimant level and
  level-dependent counts are closed.
- Architecture 11 draw: hospital coding intensity after an EHR conversion, separated by the same patients' successive
  admissions: adjacent to task453 (a measurement change read from a within-design contrast that nets a drift), the event
  study is the reflex and the WHAT signposts the method.
- Architecture 11 draw: low-voltage anode effect PFCs at aluminium potlines: task459's driver (a ratio with a fixed
  component carried across activity levels), and the IPCC slope method files it; wastewater digester relief-valve
  venting: v9's Gate G risk (an unmetered event inferred from indirect evidence); idle and shut-in wells: a setting clone
  of task462 and task450 v1; stack test-day tune-ups: population_selection and a surface read.
- Architecture 11 draw: a landfill's pre-record waste read from the volume survey: the gas collection record calibrates
  the decay model and absorbs the missing waste; refinery turnaround cycles: a schedule in a file is read; fuel switched
  during gas curtailments: a degree-day normalisation is the reflex.
- Architecture 11 draw: Fellegi-Sunter term-frequency weights: adjacent to task468 (false links on common
  identifiers); address agreement decaying with the gap between records: adjacent to task468 v1.
- Architecture 11 draw: majority-drifted or released anchors (v6, task450); rater severity drift on a shared
  constructed-response subset (task471 v2's driver); rapid guessing in a low-stakes sitting (task479 v4, sent back as
  cleaning contaminated data); speededness and not-reached items (an anchor-drift screen catches them).
- Architecture 11 draw: queue position for open appeals or a coding backlog against timely filing limits: the waiting
  time is a generic queue quantity, so the swap test fails and the domain is a backdrop; censored demand behind
  capacity is task18, task108 and task168; capture-recapture is task199, task243, task248 and task448.
- Architecture 11 draw: newborns and deliveries predicted from current pregnancies in an employer group's renewal: the
  base projection's credibility and trend choices fork, in a large group last year's deliveries already carry the
  component, and the honest strategy (who is in the 2027 population) is population_selection, banned against task275.
- Architecture 11 draw: race and ethnicity imputed from surname and geography for group counts: summing the
  probabilities is the reflex for counts, and the weighting-against-regression choice for rates needs a gold-standard
  subsample, banned against task275.
- Architecture 11 draw: the payroll survey's birth-death model against the lagged QCEW census is reserved for task484
  v2, and drawing it here through a house domain would game the survey x ETL ban against task483.
- Architecture 11 draw, first world: plausible values aggregated by school for a county school system's coaching list
  reskins task450's world and call (a district's own assessment naming the campuses below a share for coaching), so the
  mechanism moved to a company's guarantee settlement with its partner districts.
- Architecture 11 placement, benchmarks by prior tercile (12 to 20 for the lowest, up to 30 for the highest): no
  district the plausible values pull down could cross a benchmark it met, since the strong-implementation districts
  with weak backgrounds sit in the lowest tercile, so benchmarks became whole numbers from 12 to 35 per order form.
- Architecture 11 placement, a 5.5-point margin to the family's envelope with 2.5 points of crossing for every route:
  no maximum likelihood or curve-inversion count crossed anywhere, the routes' upward bias peaking near 9 points; the
  shipped margin is 4 points to the whole family's envelope with 1.5 to 3 points of crossing by route.
- Architecture 11 asks, a series' total on each row with series of up to 12 hours: the hours column summed put most
  districts at two to three times their contract, which reads as wrong at a glance; the series were cut to 3 and 4
  hours and the summer institute booked by day.
- Architecture 11 ask A, the offering's catalog hours on every session row (a series' total on each of its sessions):
  round 1's reader A set the series rows beside the catalog's hours per session and replaced them, keeping all 58 hours
  and 18 credits (exit 1); the catalog every reader opens for the live and recorded formats holds the tell one lookup
  away. Re-sited onto the session times the scheduler holds as hours and minutes after the point, every offering
  scheduled in whole hours so only the sessions that ran short or long carry minutes.
- Architecture 11, credits on quarter-dollar seat prices: a 15 per cent credit on a fee of 11,537.50 is 1,730.625, so the
  cent had a tie that no file breaks (judge pass 1, FIX_NOW); seat prices moved to whole half dollars, every credit a
  whole cent, the call's set unchanged.
Architecture 11 (the contractor's plausible values drawn from a conditioning model with no district term, each district re-estimated with the district in the model), spent at stage 4 round 2 on zip ce5456c3: reader C refitted the 2PL latent regression from the item responses with district in the conditioning model, validated its fit on the contractor's Table 6, filed the golden 16 districts and USD 25,493.75, and kept every ask figure (58 of 58 hours, 20 of 20 shortfall credits, 36 of 36 memo rows) by reading the hours field as hours and minutes from its fractions. A conditioning model that omits the grouping variable is a reflex for a reader who knows plausible values, so the round-3 PD re-site (series credit hours stacked on h.mm) is moot and the slot re-roots.
- 2026-10-24, architecture 12 draw: a Lunar New Year factory shutdown reaching a US East Coast port's container imports
  a Pacific or Cape crossing later, for its calendar-adjusted series: the decisive step is a lag and a window, the
  enumerable single choice the client's measured coin flips share, the effect is famous in trade data, and a port world
  would be this lane's third (task472, task474). Not drawn.
- 2026-10-24, architecture 12 draw: a state's payroll survey estimates early-benchmarked to the lagged unemployment
  insurance census where the birth-death model ran ahead in a slowdown: the two series count the same jobs side by side
  (architecture 8's reflex), the step is a choice between two files, and rejecting the published estimate for the census
  reads as a surface-read rejection at Gate G. Not drawn.
- 2026-10-24, architecture 12 draw: revisions measured from real-time vintages, or rebuilt pseudo-real-time by
  re-adjusting truncated spans: the client's pin makes the triangle rule application once the vintages ship, and the
  truncated re-adjustment forks between X-11 and STL end filters. A seasonal break from a school calendar moved to
  August: the post-break span is a window and the regime regressors are a reflex. Not drawn.
- 2026-10-24, architecture 12 draw: chain drift in a scanner-data price index (economics x ETL is undrawable, and the
  formula is one enumerable switch); suppressed county-industry cells rebuilt from their margins (identification is the
  step, so one linear solve is the easy route landing); custom-area margins of error from replicate tables against the
  approximation (the handbook licenses both, a fork at Gate C); register over-coverage by signs of life (every activity
  window is a threshold read as a fork). Not drawn.
- 2026-10-24, architecture 12 draw: the lake towns' population present also read from their transfer stations' scale
  tickets or their water meters: solid waste is collected on schedules that lag the stays, and summer water use carries
  the irrigation of empty cottages, so neither measures the people present as the sewer does; kept out of the pack.
- 2026-10-24, architecture 12 stage 4: the population present read through the plants' influent load per person,
  calibrated on the winter months; both round 1 readers landed the call at the 0.17 lb population equivalent (exit 1),
  because the Act's definition made the paid-stay records visibly incomplete and the influent rows had no other use in
  the pack. Spent.
- Architecture 13 draw (2026-10-24): re-rooted on the author's standing rule (no retirement) with a fresh world.
  Screened before it and dead: Medicaid exposure developed through retroactive enrollment (task474 v4's capitation
  world, task451 and task479 v5's completion, and the recent months' dip shows on any monthly tabulation); linkage
  sensitivity by identifier stratum for linked mortality (a pooled clerical correction lands the stratified set on
  paper, and stratifying by the identifier is a reflex); three measurement systems combined by triple collocation
  (task228, landed); regression against equating in a score crosswalk (task464); payday counts by weekday schedule
  (task477); data fusion through a small joint source (task465); a prospective capitation priced on experience chosen
  the same way a period earlier (task130's lineage); business deaths confirmed after two years without reactivation
  (the standard's definition makes the adjustment a reflex); out-of-state births to residents arriving through the
  vital records exchange (a completion the place-of-occurrence field shows).
- 2026-10-24, architecture 13 stage 2: the October run's short counts read as members still to come who cost nothing
  (the interim measure scaled by the run's members over the 2025 final run's, or by the member months) filed the golden
  set with the practices as first placed, so a reader who saw the counts and assumed the rest landed the call without
  the 2025 re-run. Birrelhaven, the paediatric clinic whose late members cost nearly what its others cost (run-out
  0.944 on a 22 per cent short count), was placed 5.5 per cent over its threshold, where the zero-cost reading takes it
  12.8 per cent under.
- 2026-10-24, architecture 13 stage 2: asks with one device each (the code on the claim for ask A, Pemberglen's
  posting period for ask B) handed a whole ask to any response that found its device; each ask now carries a second,
  independent silent device (Merrinlake's halved modifier-25 visits; Kesselcrest's Medicare Advantage lines on the same
  remittances), and the best single-device handling keeps 6 of 52 figures.
- 2026-10-24, architecture 13 stage 2: the projected 2026 figure graded to the cent was dropped from the prompt's
  columns: the licensed constructions agree on every election but not on the cents (per payer against per practice
  moves a projection by up to 0.6 per cent), so the workbook carries the projection as context and the rubric grades
  the benchmarks, thresholds and elections.
- 2026-10-25, architecture 13 (each practice's interim measure carried to the payers' final attribution by its own
  2025 run-out at the same cut), spent at stage 4: both scored readers re-ran the October 2025 interim run from the
  2025 claims and landed the call, reader A with all 78 ask figures; a projection from an interim run to a final one
  whose prior-year ratio the standard's own rules rebuild is the completion reflex, and the second ask devices (the
  halved modifier-25 visits, the Medicare Advantage lines at another rate) fell to a reader who checked only the payer
  whose rates looked wrong and the one fee that did not match the standard.
- 2026-10-25, architecture 14 draw: the member cap read as what the run-out truncates (a member whose year to date
  already sits at the cap carries fixed dollars while the year's months grow): in architecture 13's world no member
  reaches USD 250,000 by August and 25 reach USD 100,000 (2.9 per cent of the capped January to August amounts), and a
  practice's capped share moves from one year to the next by noise (about 1.5 per cent of a projection), so no flip
  holds.
- 2026-10-25, architecture 14 draw: competing exits read as censoring (a cumulative incidence against one minus
  Kaplan-Meier) is spent by task134, task254, task257, task264 and task266; a share above a cut counted from scores
  measured with error is task253's driver; random-groups equating with make-up sessions on one form fails on the
  group-equivalence check, which is the field's own quality control and lands by reflex.
- 2026-10-25, architecture 14 stage 2: the run-out (v13's golden) on the default path left Birrelhaven's 2025 twins,
  in a neonatal unit from 24 June to October 2025, running at the 2025 cut, and the same-cut figure read as the network
  would have reported it at 30 September 2025 then left their facility claims out of the run-out's denominator and kept
  them in its numerator: 32 of the 128 constructions entered seven, Birrelhaven out. Their stay now runs from 3 March to
  June 2025 and is paid by August, so no long stay runs at the 2025 cut and the run-out's precondition holds in 2025.
- 2026-10-25, architecture 14 stage 2: the asks' architecture 13 devices (Kesselcrest's reviewed 99215 visits at its
  99214 rate, Merrinlake's halved modifier 25 visits at no rate on the schedule, Pemberglen's coverage month in its
  payment reference, Kesselcrest's Medicare Advantage lines at another fee) all fell to one reader who matched every
  line to the schedule and every fee to the standard. The halved visit now passes that match (Merrinlake's 2026 level 5
  is twice its level 3, so a halved 99215 is a full 99213), Merrinlake's retro lines from its July run now carry a
  cohort's member months under its first month of coverage (every line its member count times the fee), and the
  Medicare Advantage lines are gone.
- 2026-10-25, architecture 14 stage 2: the benchmarks and thresholds as graded columns (26 figures every reader keeps,
  a third of the scored ask figures in architecture 13) were dropped from the prompt; the workbook carries them as the
  elections' context and the write-up names the two practices the stays move.
- 2026-10-25, architecture 14 stage 4 round 1 (target.zip cc4a6fbd821d4dfd): both scored readers filed the default ten
  and missed the call, and the judge returned DETERMINISTIC with FIX_NOW (Callowglen's share 0.002 points from its
  rounding boundary under 23 same-day duplicate visits, the chart graded on sign). Reader A rebuilt every payer's runs
  from the claims, read Kesselcrest's reviewed 99215 lines at their 99214 rate, took Merrinlake's halving as a payment
  reduction and spread Merrinlake's retro lines over the rebuilt members' months, keeping all 52 ask figures (score
  FAIL). Kesselcrest's review moved off the line onto a claim adjustment line (every line now matches its code), the
  world bills one visit a member a day, and the fees narrowed to each payer's July to September total, because a
  run-rebuilding reader reconciles any allocation of fees to the months they cover.
- 2026-10-25, architecture 14 fix pass: the narrowed fee ask (each payer's July to September coverage fees, 3 figures)
  withdrawn before any reader saw it: ceiling.py's cracker kept all three (Merrinlake's retro lines spread by their
  member counts, Pemberglen's from its payment reference), so precut's cracker row read "keeps 3", and a fee ask in
  these remittances has no device a run-rebuilding reader cannot reconcile. The remittances ship as distractors; ask A
  is the one device ask.
- Architecture 14, the network's stays still open at the cut carried at the member cap (2026-10-31, spent at stage 4):
  the repair's judge pass 2 found two graded thresholds a cent off with the 2025 measures within a third of a cent of
  a rounding edge, and the re-judge found the write-up's "all seven past the cap by 31 August" false under a pooled
  per-day reading (4,535.53 a day against the per-kind 6,380), thin margins and the stay amount unfiled. A FIX_NOW that
  fails twice is spent; the world goes with it. Lessons carried into architecture 15: every graded figure at least a
  quarter of its rounding unit from an edge under every defensible conformance, asserted; every factual write-up
  sentence true under every defensible reading of an unfiled amount; call margins no defensible variant comes within a
  few per cent of flipping.
- Architecture 15 draw screens (2026-10-31), each dead before a harness: fisheries observer-coverage discards (task275
  approved on it); a sum of probabilities against a count of shrunken predictions for a threshold count (task253
  approved on it); TNC deadhead at an airport curb (task467's airport ground-transport world); APU minutes from gate
  power draw (a reflex for the field's own analysts once the meter log is in the pack); crop insurance optional against
  enterprise units on prorated production histories (the prorated years print identical unit yields, which the hygiene
  battery flags); a funnel-flow grain bin's discharge order (physics no judge reproduces without a free regime
  parameter, and one of two traceability reflexes lands it); coincidental exact-key matches growing with the comparison
  file (task468's false links on common identifiers told in other words); a vendor's clustered coding audit (a filed
  confidence level plus a batch column points at the variance, readability test 1); queue time from backlog over
  intake (no ETL task type carries it); mine-to-mill change of support (a free choice of support correction, Gate C);
  record-linkage and seasonal-adjustment cells set aside on the directive's batch reading (task250 and task470 hold
  those client domains), the census-register cell on task470 itself.
- Architecture 15 stage 2 (2026-10-31), a limit of 3.0 per cent of the plan's cost on a menu of 2,000, 2,500 and 3,000
  dollars: the 2,500 option sat between the routes with margins under 1.2 on both sides; the resolution now allows
  2,000 or 3,000 dollars at no more than 1.90 dollars per covered person month.
- Architecture 15 stage 2, an ask on the persons at the maximum by relationship: a count the accumulators state
  outright; replaced by the orthodontic balances, whose units cross the migration.
- Architecture 15 stage 2, ask A as shares to one decimal: five of the seven quarters sat within a quarter unit of a
  rounding edge; asked as counts, which have none.
- Architecture 15 stage 3, a simulation that began on 1 January 2024 with nothing carried in: January 2024 held no work
  put off from 2023, so 2025 rose 11 per cent on 2024 and the October 2024 projection missed by 5 per cent, a search
  signal the back-test was meant not to give; a 2023 plan year now runs first and is not extracted.
- Architecture 15 stage 3, members putting work off before meeting the deductible, and new needs on a tooth whose work
  was put off: each opened a fork on the graded figures (the put-off work's deductible; a later claim on the same tooth
  matched by procedure family); a member now weighs a cut estimate only once the deductible is met, and work put off
  stands in for the next year's need on the same tooth and procedure family.
- Architecture 15 stage 3, a sentence in F-17 filing the deductible convention: it would have told a literal reader to
  charge the 2026 claim's deductible on the put-off work; the records carry the convention instead (SF6, SF14).
- Architecture 15 stage 3, a request stamped on the stroke of 5:00 p.m.: "after 5:00 p.m." and the golden's reading
  disagreed on it; no request is now stamped on the cutoff minute.
- Architecture 15 stage 3, the bound routes (every person at the maximum taking the whole rise; a year annualised from
  the day the maximum was met) reach 2,000 dollars without the decisive step, and no menu or limit moves them while
  the golden's correction raises the cost; they stay recorded in the ladder as the build's open exposure, each refuted
  by the records and each missing every graded cost figure.
- Architecture 15 (Pembrook Castings' dental maximum under F-17): the stage 4 judge returned NOT_DETERMINISTIC with
  SEND_BACK and the reconciliation confirmed a withheld rule: F-17 executed word for word on the 2025 claims gives
  increases of 0.83 (2,000) and 1.23 (3,000) and files 3,000, while the golden's 2,000 needed the work members put off
  to the January reset added back, which no shipped text states; the asks also left the put-off column's total, the
  deductible on 34 lines, "still in treatment" and an orphan case open. The slot's lesson: the filed standard's
  word-for-word execution must be the golden, and the difficulty is computing that filed quantity from the data's
  structure, never a correction the standard does not ask for.
- Architecture 16 design (2026-10-31): a third ask on the aluminium Midland recovered from each quarter's dross, read
  from its settlement statements, dropped before data was cut: with the lift date on each settlement line the figure
  is executed by any careful reader, and without it the figure rides the processor's booking lag, which no sentence
  can file without handing it over.
- Architecture 16 design (2026-10-31): the family intensities graded to two decimals, dropped on the measured spread:
  the defensible fits put 6082 billet between 0.260 and 0.268 and the castings between 0.45 and 0.52, so the call is
  graded on the premium and the families earning it, and the prompt pins no rounding on the intensities.
- Architecture 16, the homogenizing furnace's gas allocated by its loads' firing hours (2026-11-07, spent on its first
  portal round): both responses landed the golden premium of EUR 342,000 on the firing-hours allocation, the method a
  careful analyst reaches for, which the hourly gas fitted at R-squared 0.9985, so the fit handed over the route; the
  portal also flagged Domains Fit. The emissions-inventory world and the furnace-allocation driver are spent.
- Architecture 17 draw screens (2026-11-07), each set aside before a card: a linkage precision carried from a
  validation run onto a run with rarer true matches (task446's invariant, error rates carry and the yield moves, already
  screened at task174); claims completion by each nursing facility's own monthly billing day against the extract (the
  trap is per-reporter completion, 181's route, 445's reporters, task451's sender delay); IBNR from each member's
  infusion rhythm across the medical and pharmacy benefits (v14's skeleton: a per-member amount incurred and unbilled,
  read from a second stream, past a per-member threshold); same-event double capture across two lists, an ED-initiated
  treatment start recorded in both (task196's approved driver); chain-linked volume non-additivity (a named correction
  in the accounts manuals, the library test); construction value put in place spread by each project's own endpoints
  (the progress reports back-test the duration scaling, so the fit points at the golden); Medicaid encounter
  completeness by subcapitated vendor (encounter data validation is the actuary's own step); a regional series'
  seasonality rebuilt from its units' histories (one join and a per-cell mean); a year-end processing pattern absorbed
  as seasonality (the change is dated and visible).
- Architecture 17 draw, the due-contact family (2026-11-07, five prototypes): register children counted resident only
  where activity shows, and absence of activity is evidence of departure only where a well-child contact fell due under
  the child's own centre's schedule. District schedules put inactivity at 6 per cent against 36 (the pack's largest
  anomaly); masking it with district emigration biased the golden by +5.4 per cent; centre catchments left the pooled
  route within the golden's own noise (pooled minus golden sd 1.6, golden sd 1.1); a previous cohort's complete outcome
  made the golden exact (sd 0.8) but per-centre calibration landed within 1.4; a recall rule keyed to each child's own
  history removed the anomaly and the district by age-year calibration landed at +0.1 per cent. Its world also sat
  beside task471 v4's register-adjusted municipal population, and its honest label, composition_mix, was banned when
  the family was screened.
- Architecture 17, first prototype of the drawn mechanism (2026-11-07): with schools whose Term 3 unit ended before
  their first sitting day, recalibrating on whole schools that had finished the unit landed the golden in 20 of 20; the
  world gives every Term 3 unit at least five weeks against a sitting in weeks 3 to 5, so no school has finished one
  before it sits and taught responses exist only inside schools, after each school's own last lesson.
- Architecture 17 stage 2 (2026-11-07): both Term 3 units ending inside the sitting window (the prototype's world) is
  not how a ten-week term runs; the generator teaches the units in sequence, the first ending in week 4 or 5 of each
  school's own term and the second at its term end, which first left about 5 per cent of the Term 3 responses taught
  (about 60 per item, the golden 0.24 logits off the truth on the shipped seed) and was widened to a sitting of 6 to 9
  days with the first unit ending 1 to 7 school days after it (about 11 per cent, 150 per item).
- Architecture 17 stage 2 (2026-11-07): drafts composed on the shipped seed's golden estimates put the golden at B on
  redraws whose Term 3 estimates fell the other way; the drafts are composed on the items' taught difficulties and the
  shipped seed chosen from a scan (482025) where every graded figure sits a quarter mark inside its bin, the bank
  picks A, every golden variant keeps the whole marks and every rival route misses C.
- Architecture 17 stage 2 (2026-11-07): golden targets A 27, B 26, C 25 left the bank's pick split between A (8 of 20)
  and B (12 of 20); retargeted to A 26, B 23, C 25 so the bank lands on A in 20 of 20. A Term 3 taught mean of 0.15
  logits put the banked Term 3 items at the hard end of the bank (half a logit above the rest, two of them the bank's
  worst outfit); a mean of -0.85 with the untaught effect held to 0.6 to 1.3 logits puts them 0.20 above, inside the
  spread.
- Architecture 17 asks (2026-11-07): a licence-fee ask (one publisher's stimulus fee repeated on every item line, the
  other's fees in Australian dollars) needed either the agreement's per-stimulus clause or the publisher's invoice to
  find the repetition, the first a filed rule adjudicating the device and the second an oracle tying only under the
  golden; an item-exposure ask could move the call through a disqualified draft; both dropped for the make-up mean.
- Architecture 17 asks, parent review (2026-11-07): with the make-up count unasked and walk-ins absent, the full
  includer (roster join, entries on first name, surname and birth date) kept 6 of 12 ask figures, over two fifths;
  unbooked absentees who sat at a host and reach only the keyed file (D4, their home school through the entry number
  keyed and the register) put a second reconstruction on the sat block, the make-up count joined ask B by shape, and
  the full includer keeps 4 of 16.
- Architecture 17 stage 4 round 1 (2026-11-08): the judge returned FIX_NOW on ask B alone: the batch of 13 scripts
  keyed on one day, all even and seven over 50, could be halved whole, in part, dropped or kept, because no shipped
  file stated the make-up paper's maximum or the keying unit; the roster's header now files both in the office's
  voice with the batch rule, the keyed file numbers each session's batch, and the golden memo states only what the
  files show. The reader came back clean; its one note (every early register row on one entry date) is answered by
  each school's upload carrying its own day.
- 2026-11-08, platform round 1 on architecture 17: both runs filed Paper C and every regional figure. Run 1 fitted coverage penalties for U5 and U6 (about 1 logit each) and zeroed them for November; run 2 kept U5 and U6 responses only after each school finished the unit. The August-against-November gap in the prompt, the course outline and Appendix B's per-school sequences handed over the join, and taught-content adjustment is a reflex; spent (runs/triage.md).
- Architecture 18 draw screens (2026-11-08), each set aside before the card: a guessing floor at a low Level 1
  standard on Level 2-calibrated multiple-choice items (a prototype put the bank eight marks off the truth and spread
  the floor-only and full routes over three marks around it: Rasch misfit at the low end makes every estimator's
  answer depend on its form, and a three-parameter fit is the reflex for multiple-choice data); the same floor offset by
  a reading cost on the bridging items (the same fragility, replaced by two clean shifts under a true Rasch model);
  teacher-judgment standard setting with class-referenced judging (the literal standard executes to the pooled
  contrasting-groups cut, so the correction is a withheld artefact rule, and a moderators-only route is unbiased);
  standard maintenance through prior attainment with the prior's unreliability (task5's screen: a measurement model
  whose estimate spreads, and the school-level route lands); common-centre standard maintenance with centres leaving
  after a bad year (about a tenth of a logit of regression at realistic selection, and multi-year averaging, the
  reflex, removes most of it); item clones whose features shift difficulty (one pass mark for every version is
  unbiased on average, so the call does not move); a concordance from dual test-takers who took the second test after
  a low first score (mark474's driver, selection on falling short in a common-person link); a pretest-to-operational
  shift, repeaters' familiarity with reused items and mid-life item revisions (each removed by a reflex: a pretest
  adjustment, excluding repeaters, a latest-version rule).
- 2026-11-08, architecture 18, stage 2: the regional ask as a count of expected passes (the first prompt draft) was replaced by a mean mark, because a count at whole candidates moves with every estimator choice near the pass mark; the mean mark at one decimal was graded in whole marks instead, because the ability estimator and scale family (Warm or maximum likelihood abilities, the joint likelihood's stretch undone in part or in full) spreads each region's mean by up to 0.26 of a mark; and each patterns item's chance is graded as its band verdict and the group's range, because the forms of the split move single chances by up to 0.048. Seeds 818018 to 818043 were screened (the call's bin, the band edges, the rivals' distance, the regional whole marks over the family); 818025 is the one kept.
