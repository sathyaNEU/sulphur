# task16: whether One Chart may link patient records automatically at Port Calder's April 2027 conversion, and under which rule

Architecture 3, drawn 2026-11-12, after architecture 2 was sent back at stage 4 (`## Tried and rejected`). Every lesson
in the chain is off the client's closed strategies page (`guidelines/client/learning-modules/overused-strategies-2026-11-12.md`).

## Draw

Subdomain: General Statistics & Data Science, data integration, record linkage and entity resolution (task type
  data-integration-record-linkage-entity-resolution)
Analysis type: Data Extraction & Conformation (ETL / Pipeline Build)
Answer shape: a ranked list under a cap: the four candidate automatic linking rules ranked by the record pairs each
  joins at the conversion, each with its estimated false merges per 2,000 automatic links against the patient
  identity policy's cap of one, above the converted index reconciled to both legacy indexes (distinct patients,
  patients in both, records that hold two patients, duplicates left for review)
Weight: hard-to-measure: most of the work is estimating each candidate rule's false merges, a quantity no record
  holds, through witnesses that each see only part of it (the population's own joint distribution of names and birth
  dates, the blood groups, the delivery log, one registration visit, the HIM pilot's review band); redrawn at stage 2
  from validation when the window moved (task20 v2 now weighs validation), and the honester label, since validation in
  the vocabulary is a model proved on unseen data; the last two builds before this card weigh assembly (task22) and
  validation (task20)
Data-native sentence: a patient index holds what registrars typed at each visit and what an earlier merge rule did
  with it, so two records that agree on every field a rule compares may be two people (Port Calder's names are
  concentrated by community and by birth cohort, twins share a household, a family was registered under one
  subscriber's SSN), and two records of one patient may agree on little (a married name, a second surname dropped, a
  nickname, a new address); nothing in either index says which, and the only independent witnesses are the clinical
  events (blood groups, births, admissions) the rules never look at.
People: Brenda Hartman (director of health information management; signs the patient identity policy), Felicia Soto
  (the EMPI vendor's implementation consultant; the matching specification), Richard Wood (One Chart program
  director; the conversion plan), drawn with `guard.py names --geo us --seed 1603`; none is named in the prompt.
Decision: before the One Chart conversion on Monday 5 April 2027, the One Chart steering committee fixes whether the
  Halvard enterprise master patient index may join two patient records without HIM review, and under which of the
  conversion plan's four candidate rules: the patient identity policy caps automatic false merges at one per 2,000
  automatic links and takes the compliant rule that links the most; forward-facing (the conversion and its links are
  2027's).

The world. Port Calder is a fictional city on the Texas Gulf coast, about 60 per cent Hispanic, with a Vietnamese
community from the shrimping fleet. Calder Bay Health (three hospitals and clinics north of the ship channel) and
Rosario Medical Group (a hospital, a children's unit and clinics to the south) merged on 1 July 2025 as Calder Rosario
Health and convert to one electronic record, One Chart, on 5 April 2027. Each keeps its own patient index until then.
Calder Bay's registration software has merged a new registration into an existing record automatically whenever the
last name, birth date and sex match exactly since 4 March 2019; Rosario never merged automatically, and its HIM staff
merge what a monthly duplicate report shows. Until June 2021 Rosario's registration screen took the SSN from the
insurance card, which for a dependent is the subscriber's. Halvard Identity's engine scored a 2026 pilot of candidate
pairs; HIM reviewed the pairs in the engine's review band. Every extract is cut on Monday 2 November 2026; as-of date
for `leak.py`: 2026-11-04.

Card: `.claude/skills/fingerprint/cards/task16.json`, architecture v3, registered at WARN. Redrawn at filing: the
decisive generator (G16, method selection, first: the call picks a rule on its estimated error; G10 first put the
triple on task6 v5's lineage), the calibration organ (the clinical record the rules never use, physical verification;
the HIM pilot's reviewed pairs are the hurried route's check, and gold_standard_subsample is task7's in the window)
and the question form (whether, then which; task1 asked which). Redrawn at stage 2, when the window moved under the
registered card (`ban.weight` against task20 v2, `ban.role` against task13 v4): the weight to hard-to-measure (above)
and the role family to statistical_office_head (HIM is the health system's patient records and data office; the
integrity policy it signs made compliance_or_audit the first label, and both are honest). WARNs answered:
identity_resolution (strategy_risk) decides here on estimated error rates, never on one identifier read correctly;
hard-to-measure is task13 v4's too, five builds back, on a flagged set of feeders; executive_team (ten builds) is the
honest forum for a conversion steering committee of the system's executives; pick_one_of_n repeats task1 v4 because
the conversion runs one rule of four or none; the question form whether repeats task20 v2's because the policy's
gate is a whether; task3 v7 shares the answer shape and the weight (Template check); inherited_attribute_from_other_unit
(five live builds) and validation_cannot_see_condition (three) are supporting steps beside a deciding lesson no task
on file teaches.

## Stump screen

Card registered before `SCREEN_FROM`; the screen is written here at stage 2 from the drawn traps, on the built
numbers, so the reader sees which traps carry the call. Tests: 1 off the closed page, 2 not a reflex, 3 nothing filed,
4 clean data, 5 two records, 6 the waved-through assumption, 7 a plausible shallower story, 8 across the data, 9
worth the call.

| Candidate trap | The assumption a run waves through (precedent) | The second record that refutes it | Tests failed | Kept |
|---|---|---|---|---|
| Port Calder's first names run in birth cohorts and communities, its surnames concentrate by community, and foreign documents put many birth dates on 1 January, so two patients share a first name, last name, birth date and sex far more often than each field's rate implies (rule A) | the fields agree independently, at the engine's national chance rates or the records' own (L22, L35) | the population's joint cells of name, sex and birth year in both indexes with each community's birth-day heaping; the blood groups on rule A's links, read net of mislabelled specimens (records typed twice or more) and of overlaid records (the merge history) | none | kept |
| twins share a household, a surname and a birth date and over a quarter of them near-identical first names; they score above the pilot's review band, so HIM never saw one (rule C) | the pilot's reviewed pairs measure a rule's precision (L28) | the delivery log's two newborns of one delivery (birth grain), one registration visit (the records' timestamps); the blood groups are blind here, twins mostly sharing one | none | kept |
| Calder Bay's registration system merged a new registration into a record with the same last name, birth date and sex from March 2019, so some surviving records hold two patients | the index's records are one patient each and the merge history is history (L03) | each retired record as it stood against the survivor's name, the delivery log, the blood bank | 9 (it moves no rule across the cap; it is graded on its own, and on the blood-group route it is what condemns rule B) | kept as a result |
| Rosario stored the insurance subscriber's SSN on a dependent's record until June 2021, so twins share an SSN and a birth date (rule D) | an SSN is a person's own | the first names on rule D's links, the delivery log, one visit | 2 (a careful run with the engine's name table sees two names under one SSN and drops the rule) | dropped as a trap, kept as a result (R4) |
| the blood groups are a physical check on any rule's links, but one patient's records disagree when a specimen was mislabelled or a record holds two patients, and twins mostly share a group | a conflict marker is clean and sees every false merge (L28) | the records typed twice or more (specimen grain), the merge history, the delivery log | none (read as they stand the groups condemn every rule; net of both errors they file Rule B, a second route to the call through R5's overlays) | kept |

## Deep reasoning

Task type: Data integration, record linkage & entity resolution: each candidate automatic linking rule's false
  merge rate at an enterprise master patient index's conversion, estimated against a policy cap, with the converted
  index reconciled to both legacy indexes
Domain test: the results are the field's own quantities: a deterministic match rule's false match rate, the chance
  agreement of identifiers in the population the rule runs on (the u-probabilities and their dependence), what a
  clerical-review sample covers, overlays and duplicates in a master patient index; the HIM analyst estimates each
  rule's false merges, decides which may run without review, lists the overlays to split and sizes the worklist
Swap: in a retailer's customer-account dedup ("which rule may merge loyalty accounts automatically") the twins of one
  household, the 1 January birth dates of foreign documents, the delivery log and the blood groups as witnesses and the
  registration system's 2019 merge rule lose their meaning, and the cap is a patient-safety rule a retailer has no
  reason to hold
Where the weight sits: R2 and R3: estimating a rule's false merges with no labelled set that covers them. R2 counts
  the pairs of patients who share first name, last name, sex and birth year in both indexes and prices each pair's
  chance of a shared birth day from its surname community's 1 January and 1 July shares by decade, shrunk toward the
  decade, then cross-checks it with the blood groups once their own errors are measured; R3 links the index with what
  the rules never compare and counts the twins it keeps apart
Layer 1: two exports in different conventions (Calder Bay upper case, the unit in its own column, mm/dd/yyyy; Rosario
  title case from 2016, the unit inline, ISO dates), hyphenated and accented surnames, phones with and without
  punctuation, all-zero and all-nine SSNs typed when none was given, retired MRNs in the blood bank and the delivery log
  that follow Calder Bay's merges to their survivor, married-name records and typed slips; none decides a result
Not one thing: the strongest single piece is R2; a run that nails it files Rule C (the twins the pilot never saw),
  still misses the overlays and the duplicates left after the right rule; a run that
  reads every rule from the blood groups must net out mislabelled specimens and the overlaid records (R5's work) or
  it condemns every rule, Rule B included, and even then misses rule A's count and most of the twins
One-fact test: the most useful single sentence is "A patient's own records can disagree on blood group, from a mislabelled
  specimen or a record that holds two patients"; it rescues the call (R6) and R7 through it, 2 of 7, and only for a
  run that prices every rule from the blood groups, which still misses rule A's count and rule C's twins; the chance-agreement sentence rescues R2 alone (the call moves from Rule A to Rule C), the
  twins' R3 alone, the overlays' R5 alone (agrees with the Effort test's Largest single hint). The best two-move
  sentence on the golden route (the chance agreement with the twins) rescues R2, R3, R6 and R7 through R6, 4 of 7:
  two independent judgments carry the call on that route, the blood groups' own errors with R5's overlays on the
  other
Not semantics: every field, unit and clause read correctly (the rules as the plan defines them, the engine's
  standardization, the policy's cap, its denominator and its choice) leaves rule A at the engine's 5.0 or the records'
  12.1, rule C at the pilot's zero, the overlays at zero and the call on Rule A
Not rule application: the filed procedures give only each rule's links and, from the false merges, the pick; the
  false merges (R2 to R4), the overlays (R5) and the linked index (R1, R6) are estimates
Estimand: HIM-14 section 2 defines a patient's record, an automatic link, a false merge, an overlay and a duplicate;
  section 3 caps expected false merges at one per 2,000 automatic links counting each pair of records a rule would join, and
  takes the compliant rule that joins the most pairs, else review; the plan's section 7.2 defines the four rules,
  compared as the engine standardizes, on every pair of active records across and within the two indexes as they
  stand, the 2 November 2026 extracts the planning baseline; the prompt asks the distinct patients the converted
  index will hold, how many both indexes already hold, the Calder Bay records holding two or more patients, and the
  patients still under more than one active record once the recommended rule's links are made
No decoy: no memo or draft argues a rule; the engine's specification gives its national chance rate for four-field
  agreement ("about one in 10 billion pairs"), the right computation at independent national frequencies, and the
  Rules sheet prices it beside each rule's estimate (the incumbent figure, reproduced and superseded); the pilot's
  decisions are HIM's own on the pairs it reviewed
No replay: the pack publishes no false merge rate, overlay count or patient count; nothing is re-derived
Pinned: R2's rivals (each community's 1 January share by decade alone, lightly shrunk and heavily shrunk: 70.8,
  113.3 and 98.5) land in 65 to 170; the blood groups net of mislabelled specimens and overlaid records
  (204.9, 95 per cent interval 95 to 357) hold the golden but come from typed patients born 8 years
  earlier than rule A's linked patients, in the cohorts where chance agreement sits, so they test the estimate and are
  ruled out as its count by that selection; read as they stand (409.8) or net of mislabelled specimens only
  (326.3) they are ruled out by the overlaid records the merge history shows and the records typed twice or more.
  R3's linkage count
  (153) and the evidence on each linked pair alone (76) land in 70 to 220, and the linkage at match probabilities of 0.3
  and 0.7 (`checks.py`); the blood groups (59.2) are ruled out because identical twins share a group. R4's names
  alone (143), names with the delivery log or one visit alone, a name rule without typing slips and the count with
  blood groups added (173) land in 140 to 250, wide because typed slips on nicknames and short names move a names-only count. R5's rivals (the looser name forms
  513; the names alone, no clinical evidence, 568) land in 480 to 660; every automatic merge whose names differ as typed
  (1,119) is ruled out by the engine's own name table. R1 and R7 hold within their bands at match probabilities of 0.3 and 0.7
  and with the specification's fixed weights at its automatic and review cut-offs (`checks.py`)
Run forecast: R2 method shortcut (chance agreement as a product of per-field rates); R3 self-confirming check (the
  pilot's reviewed pairs, or the blood groups twins share); R5 dismissed own evidence (the index taken as it stands, or
  every merge with differing typed names); R6 and R7 self-confirming check (the rule the engine's checks pass, and its duplicates); R1
  and R4 earned
Strategy label: F10 Identity resolution, in its live form (`references/sulfur-strategies.md`): the linkage is upstream
  of estimates whose answer depends on match quality, each rule's false merges against a cap
Depth level: 5: four independent judgments (rule A's chance agreement from the joint distribution; rule C's twins
  from the witnesses that see them; the overlays read from the merge history; the blood groups' own errors on the
  second route), and the shortcuts land on four different wrong answers
  (Rule A on the engine's checks or the twins alone; Rule C on the chance agreement alone; Rule D with the SSN unread;
  no automatic linking on the blood groups as they read)
Lesson: two records that agree on every field a rule compares are two people far more often than per-field rates say
  when the fields are dependent and locally concentrated, so a rule's false merge rate is read from the joint
  distribution of the population it runs on, and each witness (a review sample, a blood group, a delivery log) sees
  only part of the false merges; no build on file teaches it (`coincidental_agreement_joint_frequencies`, a vocabulary
  key added 2026-11-12)

## Results chain

| ID | Result (checkable) | Area | Pinned by | Band | Hurried analyst | Depends on | Graded as |
|---|---|---|---|---|---|---|---|
| R1 | the converted index: 220,669 distinct patients, 76,062 of them held by both Calder Bay and Rosario | assembly-reconciliation | HIM-14's definitions; the prompt's distinct patients and patients both indexes hold; both indexes and the merge history's retired records | distinct patients within 1.5 per cent, both within 2.5 per cent | narrow look at broad data: one patient per exact name, birth date and sex (243,159 and 62,323), nicknames, married names, swapped order and typed slips left apart | - | Ask 3 |
| R2 | rule A's false merges: 106.7 of its 71,728 links, 2.97 per 2,000, the largest from older Nguyen and Hispanic cohorts born on 1 January | modeling | HIM-14's false merge and cap; the plan's rule A; the two indexes | 65 to 170 | method shortcut: chance agreement as the product of each field's own rate, at the engine's national rates (5.0, 0.14 per 2,000) or the records' own (12.1, 0.34), the fields' dependence never read | - | Component 1 |
| R3 | rule C's false merges: 153 pairs of twins among its 56,207 links, 5.44 per 2,000 | validation | HIM-14's false merge; the plan's rule C; the delivery log, the records' registration times, the blood bank | 70 to 220 | self-confirming check: the pilot's reviewed pairs (none of rule C's links among them) or the blood groups, which twins share, give about zero | - | Component 2 |
| R4 | rule D's false merges: 164 of its 46,046 links, 7.12 per 2,000, twins under a parent's SSN | investigation-loops | the plan's rule D; the indexes' first names, the delivery log, one visit | 140 to 250 | stopped at the first story: the links whose first names are not one person's read as rule D's false merges (143), the twins with near-identical names under one SSN left in, which careful runs reading the engine's name table still land inside the band; without the table every link with names unalike (2,650) | - | Ask 1 |
| R5 | Calder Bay records holding two or more patients: 568, listed by surviving MRN | missingness-measurement | HIM-14's overlay; the merge history's retired records as they stood, the delivery log, the blood bank | 480 to 660 | dismissed own evidence: Calder Bay's index taken as it stands (none), or every automatic merge whose first names differ as typed (1,119) | - | Ask 2 |
| R6 | the rule the conversion runs: Rule B, 0.25 false merges per 2,000 links, with A, C and D over the cap | synthesis | HIM-14's cap and its choice of the compliant rule that joins the most pairs | exact | self-confirming check: Rule A, passed by the engine's chance rates and the pilot | R2, R3, R4 | Recommendation |
| R7 | patients still under more than one active record once Rule B's links are made: 48,754 | modeling | HIM-14's duplicate; R1's linked index and R6's rule | within 3 per cent | self-confirming check: the duplicates left after the rule the engine's checks pass (Rule A, 20,986 on its own linkage) | R1, R6 | Ask 4 |
Carry-forward: R1 to R5 stand on inputs of their own (the linked index; the joint cells of the two indexes; the
twins' witnesses; rule D's links and names; the merge history); R6 falls with R2, R3 or R4, R7 with R1 or R6. A run
that misses the chance agreement keeps R1, R3, R4 and R5; one that misses the twins keeps R1, R2, R4 and R5; one that
misses the overlays keeps every other result unless it reads rule A from the blood groups.

## Hidden factor record

| Factor | Real or constructed | Only in deciding units | Found by | Fix depth | Verdict |
|---|---|---|---|---|---|
| surnames concentrated by community and first names by birth cohort within each community | constructed from public frequencies (the 2010 Census surnames by race and Hispanic origin; curated first-name curves by group, sex and cohort) | no: every community and cohort, from the Nguyen and Garcia cohorts to names one family holds | modelling: the pairs of patients sharing first name, last name, sex and birth year, counted in both indexes | modelling | keep |
| birth dates on 1 January and 1 July for patients born abroad with no recorded day | constructed (the simulated foreign-born share by group and decade) | no: Vietnamese and Hispanic cohorts of every decade at their own shares, a few per cent elsewhere | modelling: each surname community's shares by decade, shrunk toward the decade | modelling | keep |
| twins (1.65 per cent of deliveries, over a quarter with similar first names), registered together or apart | constructed (the simulated families) | no: every community and year; they carry rules B, C and D's false merges and touch rule A's | a targeted query and modelling: two newborns of one delivery, one registration visit, the linkage they keep apart | modelling | keep |
| Calder Bay's automatic merge on last name, birth date and sex from March 2019 | constructed (the simulated registration system) | no: every new Calder Bay registration since March 2019; its overlays move no rule across the cap | a classification: each automatic merge's retired name against the survivor's, the clinical evidence for names that agree | modelling | keep |
| Rosario's subscriber SSN on dependents until June 2021 | constructed (the simulated registration screen) | no: every Rosario dependent registered before mid-2021; it reaches rule D only through twins | a targeted query: one SSN on records with different first names and birth dates | routine | keep (R4 only; careful runs land it) |
| mislabelled specimens, about one in 2,600 | constructed (the simulated blood bank) | no: every typed patient; it touches only the blood-group route | a targeted query: records typed twice or more whose typings disagree | routine | keep |

The two routine rows decide nothing: with the SSN read correctly and the mislabelled specimens ignored, the golden
call, R2, R3 and R5 stand (asserted in `checks.py`).

## Effort test

| Result | Quick pass | Careful but hurried | Thorough |
|---|---|---|---|
| R1 the converted index: distinct patients and patients held by both legacy indexes | Missed | Right | Right |
| R2 rule A's false merges (two different patients agreeing on name, birth date and sex) | Missed | Missed | Right |
| R3 rule C's false merges (twins with near-identical first names in one household) | Missed | Missed | Right |
| R4 rule D's false merges (one SSN and birth date on two people's records) | Missed | Right | Right |
| R5 Calder Bay records holding two or more patients | Missed | Missed | Right |
| R6 the rule the conversion runs | Missed | Missed | Right |
| R7 patients left under more than one record once the chosen rule's links are made | Missed | Missed | Right |
| Roughly | 0 of 7 | 2 of 7 | 7 of 7 |

Measured by: .claude/skills/stumping/effort.py on generator/effort.json (the passes are the generator's own routes on
  the cut pack: the quick pass one patient per exact name, birth date and sex with every rule's links taken as true; the
  careful pass every file conformed, a probabilistic linkage of the active records, the rules priced on the engine's
  chance rates and the records' own field rates, the pilot's reviewed pairs, rule D's links with names not one
  person's, and Calder Bay's index as it stands; the golden)
Largest single hint: "A patient's own records can disagree on blood group, from a mislabelled specimen or a record that
  holds two patients."; rescues 2 of 7 results
Pair estimate: 34.5 (the careful pass earns R1 and R4 and the instruction-following share; every lost cell cites a
  precedent of its own class)

## Data provenance

Source: generated by task16/generator from a simulated population of Port Calder, Texas (seed 16031): 68,000 families
  with births, twins, deaths, moves, phones, SSNs, insurance and blood groups; each person's visits to Calder Bay and
  Rosario from 2006 and each registration as a registrar typed it; Calder Bay's automatic merges from March 2019 and
  both systems' HIM merges; the blood bank's results, the labor and delivery log and the state's death notices.
  Surnames come from the U.S. Census Bureau's 2010 surname file (public domain, pulled 2026-11-12) by each community's
  race and Hispanic origin shares; first names from curated cohort curves by group and sex.
Behaves like the real thing: 4.0 per cent of Calder Bay's active records and 6.0 per cent of Rosario's are a second record
  of a patient within the same index, at the low end of what master patient indexes report because both systems
  merge the duplicates they find, and a third of the patients are known to both indexes; twin
  deliveries at 1.65 per cent; mislabelled specimens near the published one in 2,000 to 3,000; first names follow
  cohort fashion and surnames community; 1 January birth dates are common among refugees and immigrants with no
  recorded day, as resettlement records show; registrations rise with age and pregnancy; deaths with age.
Genuine patterns: (1) first-name fashion by cohort within each community (2) surnames concentrated by community
  (3) birth-day heaping on 1 January and 1 July by community and decade (4) duplicates from nicknames, typed slips,
  married names, a dropped second surname and swapped name order (5) movers' addresses and phones changing over time
  (6) registrations rising with age and pregnancy (7) deaths rising with age
Problems by process: two systems' export conventions; Rosario's title case from 2016; the subscriber's SSN on
  dependents until June 2021; Calder Bay's 2019 automatic merge; mislabelled specimens; retired MRNs in the blood bank
  and the delivery log; all-zero and all-nine SSNs typed when none was given
License: the surname frequencies are a U.S. Government work in the public domain; everything else is generated for
  this task (CC0-1.0)
Used as is: the Census counts and shares are read as published to draw surnames; no row of them ships
Breadth: 13 files (two indexes of 157,799 and 154,166 records, the blood bank's 133,916 results, 28,958 deliveries,
  11,142 merges, the name table, the pilot workbook, three PDFs, and three distractors: the registration volumes,
  Rosario's duplicate report and the matched death notices), 311,965 active records of about 221,000 patients across
  hundreds of surname communities and cohorts, so choosing which cells carry the chance agreement is work

## Template check

Chain signature: assembly-reconciliation, modeling, validation, investigation-loops, missingness-measurement,
  modeling, synthesis
Question form: whether (and under which rule)
Nearest build: task3 v7 shares the answer shape (a ranked list under a cap) and the weight (hard-to-measure): its
  candidates are unrecorded sites ranked on forecast exceedances carried from a long record through short ones, its
  chain a forecast's (forecasting, uncertainty, decomposition, measurement, modeling, investigation, forecasting,
  synthesis); here the candidates are four match rules ranked by their links under a false merge cap, each priced by
  its own false merge mechanism and witness. task22 and task8 v2 share the analysis type only. Abstraction sentence:
  none writable against task3

## Frontier check

Precedents: R2 L22 (the published formula whose generating assumption the data contradict), L35 (an independence
  binomial where units share shocks); R3 L28 (an estimator certified with checks that cannot see the problem); R5 L03
  (a second log at another grain set aside); R6 L28; R7 L28. R1 and R4 carry none: the careful column lands them.
Shallow path checks: R2: the independence product reproduces the engine's specification exactly ("about one in 10
  billion pairs", 5.0 here) and the records' own field rates give 12.1, both well inside the cap; the blood groups read
  as they stand flag a problem but condemn every rule (Rule B at 96.8 against its cap of 19.9); only the joint cells
  of name, sex and birth year in the indexes (another grain than any field's frequency) with each community's 1 January
  share, or the blood groups net of mislabelled specimens (the records typed twice or more, specimen grain) and of the
  overlaid records (the merge history), give rule A's 107. R3: the pilot's review band holds none of rule C's links and
  its decisions stand; the blood groups on rule C's links net of their errors give 59.2; only the delivery log
  (births, another grain) and one registration visit (the records' times) see the twins. R5: the index as it stands
  shows no record with two names; the merge history's typed first names condemn 1,119 merges; only each retired name
  read as a form of the survivor's (the engine's table, a typed slip, a first token) and the deliveries and blood
  groups for names that agree give 568. R6 and R7 follow the rule and R1.
Assumption made false: that agreement on each field is independent of agreement on the others (the Fellegi-Sunter
  model's own assumption, named and waved through as standard: L22, L35): false here because first names follow birth
  cohorts within communities, surnames concentrate by community and foreign documents put birth dates on 1 January, so
  a shared surname makes a shared first name, birth year and birth day far likelier; tested by the indexes' own joint
  cells and by the blood groups on rule A's links. And that a review sample measures a rule's precision (L28): false
  because the pilot's band was set by the engine's score, which put twins above it; tested by the delivery log and the
  records' registration times.
Forcing: the line is one false merge per 2,000 links (A 35.9, B 19.9, C 28.1, D 23.0 false merges); the golden
  family's seven variants (rule A by birth decade only 70.8 and with light and heavy shrinkage 113.3 and 98.5; rule C
  from the evidence on each pair alone 76; rule D from names alone 143 and with blood groups 173; every rule from the
  blood groups net of their errors, A 204.9, B 0.0, C 59.2, D 74.0) keep A, C and D over and B under, all
  filing Rule B, the nearest rule A at 1.97 per 2,000; the 10 shortcuts file Rule A (no correction, the engine's
  checks, the twins or the SSN without the chance agreement), Rule C (the chance agreement alone or with the SSN),
  Rule D (the chance agreement and the twins with the SSN unread) and no rule (the blood groups as they read, or net
  of mislabelled specimens only); each estimate moved (rule A, C or D 30 per cent lower, rule B 50 per cent higher)
  leaves Rule B standing at under half of its cap.
Noun swap: the nearest skeletons on file (`skeleton.py check task16`: task4 v12, task20 v2, task13 v4, task4 arch 11,
  mark124 v6) are severity none; swapped into task13 v4 (automated feeder restoration, a validation that cannot see the
  condition) the deciding move here (chance agreement read from a population's joint cells) has no place, and only the
  supporting lesson carries; swapped into mark124 v6 (a water district's timing choice, an inherited attribute) the
  decision form, the answer pattern and the deciding lesson all differ; severity none.
Closed strategies: the call turns on coincidental_agreement_joint_frequencies, off the client's closed page; the
  nearest closed card is "dependent capture" (two lists' captures of one unit dependent, biasing a capture-recapture
  total, fixed by a log-linear model with an interaction term): here the dependence is between the identifying fields
  of two different units in one population, and the fix is the chance that two distinct patients agree on every
  compared field, read from the population's joint cells and its birth-day heaping, to price a rule's false merges,
  not a population total. The chain keeps no closed lesson as a supporting step (`skeleton.py closed task16`: 0 of 4
  closed).

## Semantic fork table

| ID | Term or convention | Readings | Golden | Ruled out by |
|---|---|---|---|---|
| SF1 | a patient's record | the record registered for the patient; any record holding the patient's information | registered for | HIM-14 section 2 ("A patient's record is a record registered for that patient"); a link touching an overlay is judged on the patient it was registered for |
| SF2 | an automatic link | each pair of records a rule joins; each group it forms | each pair | HIM-14 section 3 ("counting each pair of records the rule would join") |
| SF3 | a false merge | an automatic link between two different patients' records; a link whose records disagree on a field | two patients | HIM-14 section 2 |
| SF4 | the pairs a rule is applied to | every pair of active records across and within the two indexes; across only | across and within | plan section 7.2 |
| SF5 | the indexes as they stand | the 2 November 2026 extracts; after the overlays are split | the extracts | plan section 7.2 ("the 2 November 2026 extracts are the planning baseline") |
| SF6 | how fields compare | as the engine standardizes (upper case, hyphens as spaces, accents dropped, unit designators off the street address, ten-digit phones, all-zero and all-nine SSNs missing); as typed | as the engine standardizes | plan section 7.2 and the specification's standardization section |
| SF7 | rule C's first names | the same, equivalent in the engine's table, or Jaro-Winkler 0.92 or more | as written | plan section 7.2 |
| SF8 | the cap | expected false merges no more than one per 2,000 automatic links, inclusive | as written | HIM-14 section 3; same call (B at 0.21, A, C and D over 2.4) |
| SF9 | expected false merges | the point estimate; an upper bound | the point estimate | HIM-14's "expected"; same call (no rival puts B over 0.5 or A, C or D under 2) |
| SF10 | the rule the conversion runs | the compliant rule that joins the most pairs; the safest | the most pairs | HIM-14 section 3 |
| SF11 | twins and siblings | two different patients | two patients | HIM-14 section 2 |
| SF12 | distinct patients the converted index will hold | every patient an active record holds, the patients an overlay hides included; patients with an active record of their own | the first | same call: the two differ by the 538 overlays, a quarter of one per cent, inside the band |
| SF13 | patients both indexes already hold | a patient with an active record in each index | as written | the prompt |
| SF14 | an overlay | an active Calder Bay record that also holds another patient's information, counted once per record | per record | HIM-14 section 2 and the prompt's "Calder Bay records" |
| SF15 | a duplicate left | a patient whose active records fall into two or more groups once the rule's links are made, counted once per patient | per patient | HIM-14 section 2 ("A patient held under more than one active record is a duplicate") |
| SF16 | per 2,000 links | 2,000 times false merges over the rule's automatic links | as written | HIM-14 section 3 |

## Closure table

| Axis | Closure |
|---|---|
| 1 | Population: every active record in the two 2 November 2026 extracts; Calder Bay's retired records enter only as evidence of the patients a merge joined or hid |
| 2 | Unit of account: the pair of records for links and false merges; the patient for the index figures; the record for overlays |
| 3 | Attribution window: none; a record's state on 2 November 2026 |
| 4 | As-of dating: the extracts of 2 November 2026 (the blood bank and delivery log 3 November, the death notices 30 October) |
| 5 | Version basis: one extract per system |
| 6 | Denominator: a rule's automatic links (SF2, SF16) |
| 7 | Weighting: none; each pair counts once |
| 8 | Window length: the records' whole history to the extract |
| 9 | Boundary inclusivity: the cap is inclusive (SF8) |
| 10 | Rounding path: false merges at full precision, stated to one decimal where an expectation and whole where a count; per 2,000 to two decimals |
| 11 | Tie-break: none needed; the compliant rule is unique |
| 12 | Maturity and censoring: none; the call is on the records as they stand |
| 13 | Order of operations: conform both exports, follow retired MRNs to their survivors, apply each rule, estimate each rule's false merges, link the index |
| 14 | Row order: no step depends on file order |
| 15 | Duplicate resolution: none in the files; duplicates of patients are the estimand |
| 16 | Identity normalisation: the engine's standardization (SF6); retired Calder Bay MRNs followed through the merge history |
| 17 | Netting against gross: none |
| 18 | Dimensional units: pairs of records, patients, records, false merges per 2,000 links |
| 19 | Code and status semantics: sex codes as each system writes them; the pilot's decisions as HIM wrote them |
| 20 | Integerisation: counts whole; rule A's false merges an expectation |
| 21 | Clause scope: HIM-14's cap applies to every rule alike |
| 22 | Forward window contents: the conversion's links are the rules applied to the records as they stand (SF5) |

## Literal reader

Executing HIM-14 sections 2 and 3 and the plan's section 7.2 word for word: each rule is applied to every pair of active
records across and within the two indexes as the engine standardizes them, each rule's false merges are the links it
would make between records registered for two different patients, the cap is one per 2,000 of its links, and the
conversion runs the compliant rule that joins the most pairs. A reader who takes the engine's chance rates and the
pilot's decisions files Rule A against section 2's "two different patients", which those checks never count; one who
reads the blood groups as they stand files no rule, against section 2's "registered for", which an overlay's typings
are not. Neither is another reading: each is an easier method on the same filed estimand.

## Prompt contract

A voice rewrite keeps: why the answer must be estimated (no record shows which of a rule's links would join two
different patients); the question (whether One Chart can link patient records automatically when the two indexes
convert on 5 April 2027, and under which of the conversion plan's candidate rules); the policy's limit of one
expected false merge per 2,000 automatic links; each rule's automatic links, estimated false merges and false merges
per 2,000 links; the distinct patients the converted index will hold and how many both indexes hold; whether any
Calder Bay records already hold two or more patients and, if so, how many and which; if a rule is recommended, the
patients still under more than one active record once its links are made; a spreadsheet and a one-page memo. It never
adds a rounding instruction, a method (no twins, chance, independence, birth dates, 1 January, frequencies, names,
blood groups, delivery log, pilot, merge history, SSN, subscriber or nicknames), a warning, an attached file's name, a
role or reader, or a count the data hold (no four rules).

## Pre-ship check

- Bar re-read on the built pack: seven results across six areas (assembly and reconciliation, modeling, validation,
  investigation loops, missingness and measurement, synthesis), each pinned by a filed sentence (HIM-14 sections 2 and
  3, the plan's section 7.2, the specification's standardization) and the data, with the bands the answer blocks state;
  precut 97 checks, 0 FAIL, 2 WARN (answered in the Hidden factor record and the Template check); checks.py with
  four rival linkages (match probabilities 0.3 and 0.7, the specification's fixed weights at both cut-offs) 0 FAIL; verify.py PASS on its own code path; gates.py --full 11 gates, 0 FAIL, two rebuilds
  byte-identical.
- Golden against the simulated truth: rule A 106.7 against 115, rule B 5 against 7, rule C 153 against 147,
  rule D 164 against 165; overlays 568 against 572; distinct patients 220,669 against 221,662; patients
  left after Rule B 48,754 against 48,939.
- Hidden factor record against the cut data: 1 January birth dates run at 2.3 per cent of the index and at
  22.9 per cent of Nguyen patients born in the 1950s (6.0 times their decade's); 475 of the
  28,958 deliveries from 2006 to 2026 carry two or more newborns; 10,416 Rosario SSNs registered before mid-2021
  sit on records with different first names and birth dates, 2 after; 568 Calder Bay survivors of the 2019
  merge hold two or more patients; 25 of 23,085 records typed twice or more disagree with themselves.
- Effort test against effort.py: quick 0 of 7 (7.0), careful 2 of 7 (34.5), thorough 7 of 7; the largest hint
  rescues 2 of 7; ten shortcuts land on four different wrong answers (Rule A, Rule C, Rule D, no rule).
- Forcing: Rule B at 0.25 per 2,000 against the line of one; the nearest rival rule A at 1.97; every golden-family
  variant and every perturbation files Rule B.
- Determinism judge (one pass, determinism only, from the answer blocks): DETERMINISTIC, APPROVE. It rebuilt the specification's standardization and reproduced the active records (311,965), every rule's links (A, B and D exactly, C within 0.04 per cent), the cap arithmetic, rule A's estimate inside its band at every reasonable shrinkage, the overlays (557 against 568) and the blood bank counts (29 of 8,043 against 30); it could not rebuild the linked index in budget and noted the fitted weights are not filed, and the specification's fixed weights at both cut-offs land R1 and R7 inside their bands (`checks.py`), so nothing moved. A first spawn of the judge agent ran a stale cached protocol and returned no verdict; this pass is the one run under the current contract.
- Leak: leak.py REVIEW only (--asof 2026-11-04: the plan's and the policy's words of the rules and the conversion, the
  specification's and the policy's field words, each ruled harmless in the report). One isolated read at medium
  effort on cut 7eeb799e: no leak, no ranking file, no helper file, no one thing; it read the specification's national
  chance rate as a plausible wrong turn, which is what it is.
- Gate WARNs answered: precut's two routine factors (Hidden factor record) and nearest chain (Template check); heart's
  strategy_risk, chain_near and overuse.weight (Draw).
- Containers: audit_containers exit 0 on the pack and the golden, re-run on both zips as the last command before the
  commit.

## Tried and rejected

- A bridge between a projection and a disappointing large run (Comparative Analysis & Explanation, attribution): the
  honest strategy label is decomposition and attribution, which `ban.strategy` holds against task1 in the window; not
  relabelled, the draw moved to a forecast.
- Vendor labels as the only stump (the legacy-map route at 20 per cent error): on the real runs a pass that finds the
  expert-labelled development items and adds a per-route cost to a straight line still names the right configuration,
  so the pick turned on one thing (the yardstick).
- A contractor pool of 512,000 examples in the shortlist: the configuration on it wins by 0.07 under every sound
  forecast and under the straight line too, so nothing but the yardstick was priced.
- The dev split scored by route as separate logged scalars: a column would hand over the yardstick; the trainer logs
  one development loss and the per-item scores of each final checkpoint ship as the lab's error-analysis dump.
- A reference entry the proposal has to beat: the nearest configuration sat within 0.011 of any threshold that
  separated the shortlist, a margin the forecast cannot carry; the ranking is graded instead.
- A vendor label audit file (re-interpreted samples with agreement rates per route): with the routes' error rates on
  file a hurried pass avoids the map route by rule of thumb and wins the pick with no analysis; the routes' quality is
  left to what the runs show.
- The map route at 16 per cent error with a trial that mixed all three routes: the careful pass, calibrated to the run
  record (one scaling-law regression over every run, a floor or a quadratic chosen on held-back runs), named the right
  configuration and lost only the figures that hang on the bend, so the pick was earned by reflex and the pair priced
  near 70. Measured on the real runs at 10, 12, 14 and 16 per cent: at 12 the all-labels configuration truly scores
  0.660 against 0.6335, the pooled curve puts it first by 0.011, and every analysis that separates the level from the
  routes' costs names the right one by 0.012 to 0.039. The map route went to 12 per cent and the mixed trial out (the
  contractor's lot arrived in the pilot's last week).
- The pilot's largest runs left unfinished when the allocation ended, to be completed along the schedule: on a cosine
  schedule the logged loss at 70 to 90 per cent of a run is within 0.005 of its final value, so taking the last value
  as it stands is nearly right and the completion prices nothing.
- A compute cap that binds (a configuration that does not fit the slot): width buys under 0.006 a doubling at the
  expert pool, so no configuration that needs more hours is worth shortlisting; the hours stay texture (all four fit).
- A threshold on an extrapolated figure (lots 2 to 4 funded only if they lower the loss by a stated amount): the gap
  between the bent and the pooled forecast at one doubling past the pilot is 0.02 to 0.03, the size of the forecast's
  own error, so no line separates the right answer from the shortcut with margin.
- A separate result for what widening buys at 512,000 examples, and one for what the tuned learning rate buys there:
  each is one matched pair in the pack, a group-by the runs make unprompted, so each is earned and prices nothing.
- Nine asks on bands set by four members of one method family, with the held-back gap, the run counts and the widest
  configuration's learning rate graded (the first cut of this architecture, judged NOT_DETERMINISTIC on a narrow
  footing, FIX_NOW): the judge's own derivation (a level of its own at every total with the costs from contrasts
  between mixes, every run on the carried loss) named B and landed outside the bands on the contractor's cost
  (0.0023 against 0.0000 to 0.0020), the 512,000 level (0.599 against 0.600 to 0.613), A and the range, and the
  held-back gap proved a property of the solver's own curve (0.004 to 0.027 across sound ones), not a figure to
  grade. The bands were reset on a family of 49 run analyses that holds the judge's readings and the two bounds on
  what the examples past the largest trial return; the gap, the counts and the rate became working. With nine asks
  the careful pass then earned five and priced at 57 to 61, so the two reflex asks went and six results are graded.
- The width step priced through A (the pooled width term's 0.679 against a band topping at 0.672): a width curve on
  the carried loss gives 0.68 to 0.71 and the benchmark's own 512-wide scores less a step 0.663, with the truth at
  0.662, so A cannot be banded tighter than 0.650 to 0.720 and prices nothing.
- The level at or under the pool taken from the expert-label runs, the ladder put on the trials' rate, as the golden's
  own reading of the routes (contractor 0.0010 a tenth, B's range 0.609 to 0.638): the judge's second pass read the
  costs from mixes at one total (0.0018 to 0.0024) and the truth runs put them at 0.0017, so the same-total reading
  became the golden's (0.0020, range 0.604 to 0.645) and the first reading the other member the bands hold.
- The levels sentence priced at two results, with a least-squares floor fixed as the hinted pass's continuation:
  given a level at every total and left to choose its own form on the runs held back, the careful pass lands C and
  D as well, so the count is three of six and the note says so.
- Architecture 1 as shipped (the Norwegian group's scale-up forecast from a staged pilot sweep, six results, name
  configuration B at 0.625): spent on the platform on 2026-11-11. One run earned every graded result in 28 minutes
  (`runs/arch1_triage.md`): it compared two candidate calibrations by leave-one-out error, read the slowdown in
  matched cells (0.0471 then 0.0274 a doubling at one mix), fitted a response surface with a fitted breakpoint and
  validated it on held-out configurations, and resampled configurations and calibration pairs separately. The six
  results were one runs-by-settings table that one flexible fit absorbs, the asks named the intermediate quantities,
  and bands wide enough for every sound method (C from 0.648 to 0.689) graded nothing. No tighter honest band fails
  that run, so the world is spent: re-rooted to another world, dataset and shell as architecture 2.
- Architecture 2, a tenth result for what version 3 changed against version 2 on like conversations: on the built
  pack the linked comparison read 6.2 points, the restored one 7.1 and the like-for-like one 6.9, so no reading
  separated from another and the result priced nothing; cut, with version 2's weeks kept as the alerts' before period.
- Architecture 2, the backlog report in weekly age bands: a closed case raised early in the last week is both likelier
  closed and likelier to follow a conversation inside the seven-day-old window, so the weekly share overstated the
  open follow-ups by half (288 added against 182 true, Damaged parcel 4.7 points low). The report counts open cases
  by days open, as an ageing report does, and each closed case stands for the open ones of its own day and
  neighbours.
- Architecture 2, asks for the season's conversations a week and the adviser contacts they pass on: an ask for a
  volume built from the plan's parcels is the first half of the season mix, asked for, which is how architecture 1
  handed over its decomposition. The volume is a Critical Component and the prompt asks only for rates, ranges and
  the designation.
- Architecture 2, telephone follow-ups priced on the grain of the capture share (a pooled or weekly share against the
  quarter-hour's): on the built pack a pooled share moved no family by more than 2.0 points, inside the band a
  sound rebuild needs, so the grain prices nothing; the result is priced Right for the careful pass and the hurried
  failure there is leaving unkeyed calls out.
- Architecture 2, the telephone and case exports as silent partial extracts (calls with no tracking number absent,
  open cases absent, nothing filed): the determinism spec needs a source the golden completes to say it does not
  hold every member, and a silent partial extract is the planted defect the client names. KS-07 5.1 and 5.2 file
  both facts, the unkeyed calls are rows with a blank number, and both restorations are priced Right for the careful
  pass.
- Architecture 2, a common shock every twelve calls after a telephone contact (two or more calls per conversation in
  one in eight): a conversation with two calls and one keyed was overweighted and Track and trace's hidden
  follow-ups came out 24 per cent high; an adviser now settles most matters at the first call, as the summer weeks'
  record would show, and the weight is right to 3 per cent.
- Architecture 2, test rows and a repeated block as Layer 1 (the product team's tester sessions, a telephony test
  queue, ISO week 39 carried twice by overlapping weekly exports): the stage 4 leak reader read the test queue as
  possibly planted, and test rows and a copied block are the first two items on the client's list of planted
  defects. All three are out of the generator, with the sentence of KS-07 3.2 that excluded staff conversations; the
  backlog report now lists only the ages that have open cases (the reader read the zero-filled grid as generated),
  the depot list carries the hub and its date in two columns, and the plan's notification sheet has four short
  columns. No graded figure moved.
- Architecture 2 as built (nine results, pair 46.7 on paper): judged DETERMINISTIC and APPROVE at stage 4 on
  2026-11-11, and sent back to stage 2 by the same pass. The judge thread's own first derivation, at medium effort
  and before it saw the answers, found both measurement gaps from the files (the weekly flow against the extract,
  the advisers' tick on unkeyed calls), read resolution by delivery outcome from one group-by, weighted the plan's
  parcels by each outcome's contact rate at the alert depots, and landed all eleven rates and the set inside the
  bands in about four minutes; only the resampled range was left undone. Every estimate in the chain was a join and
  a ratio over ingredients a file labels (KS-07 5.1 and 5.2, the outcome class column, the plan's service-level and
  alert sheets), and five such estimates are still what a pass that reads every file wires together. The lesson for
  the next draw: a result is priced only where nothing in the pack labels its ingredients and no hold-out or
  reconciliation confirms it.
- Architecture 2 re-rooted on 2026-11-12 (the judge thread's first pass is the evidence: every estimate a join and a
  ratio over labelled ingredients, landed in four minutes). Architecture 3 moves to another world, dataset and shell (a
  merged Texas health system's patient index, a whether-question, a workbook and a Word memo) and to a weight the last
  two live builds do not carry (validation). Its priced results are error rates of record-linkage rules that no file
  labels and no hold-out covers: chance agreement read from the population's joint name, cohort and birth-date
  distribution, kin that share every field but one, an identifier stored for the wrong unit, an earlier merge rule's
  overlays; the only witnesses are clinical events the rules never use.
- Architecture 3 built on the curated first-name curves alone (about 470 base names, every rare name in the indexes a
  typing slip): 2,877 distinct first names in 311,712 records read as generated, and the long tail a real population
  carries was missing from the very distribution the deciding lesson reads; the Census Bureau's 1990 first-name
  frequencies now give each community's share of uncommon names (5,544 distinct, 2,508 rare real names), the world
  re-measured on them.
- Architecture 3, the blood bank's groups as a twin-blind check that would file Rule C once netted of their errors (the
  first world's 9.8 on rule C): on the built world non-identical twins differ often enough that the corrected groups
  put rule C over its cap and file Rule B, so the route is a second route to the call through R5's overlays, its rule A
  point (205, from typed patients born 8 years earlier than rule A's linked patients) ruled out as R2's count by that
  selection, and its one-sentence hint rescues the call and R7 (2 of 7).
- Architecture 3, rule D's false merges priced as a careful-column loss (names alone, 145, leaving the similar-named
  twins in, against a band from 150): a name rule without typing slips counts 70 more true duplicates as two people,
  so a names-only count spreads from 145 to about 236 by method alone; the band went to 140 to 250 and R4 is a result
  the careful runs land, the call untouched (rule D over its cap on every reading).
- Architecture 3, a link touching a record that holds two patients read as a false merge: 93 of rule B's links touch
  one against a cap of 19.4, so that reading would have filed no rule; HIM-14 section 2 now defines a patient's record
  as the one registered for that patient, the golden's convention.
