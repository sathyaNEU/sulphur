# task16: whether One Chart may link patient records automatically at Port Calder's April 2027 conversion, and under which rule

Architecture 4, redesigned in the same world on 2026-11-13 after architecture 3 was sent back at review for difficulty
(reward 78, stumped failed; `runs/review_2026-11-13.md`). The reviewer asked to keep the data, the policy line and the
determinism and to move the decision onto estimation a shallow approach gets wrong; `stumping` Part 3.4 (open members,
the direct route, margins between the family and the stump) is the rule this architecture is built to. Every lesson in
the chain is off the client's closed strategies page.

## Draw

Subdomain: General Statistics & Data Science, data integration, record linkage and entity resolution (task type
  data-integration-record-linkage-entity-resolution)
Analysis type: Data Extraction & Conformation (ETL / Pipeline Build)
Answer shape: a ranked list under a cap: the four candidate automatic linking rules ranked by the record pairs each
  joins at the conversion, each with its estimated false merges per 2,000 automatic links against the patient
  identity policy's cap of one, above the converted index reconciled to both legacy indexes (distinct patients,
  patients in both, records that hold two patients, the links that touch them, duplicates left for review)
Weight: hard-to-measure: most of the work is estimating each candidate rule's false merges, a quantity no record
  holds, through witnesses that each see only part of it and that the process biases (the population's own joint
  distribution of names and birth dates, the transfusion service's typed patients, the delivery log, one registration
  visit, the merge history); kept from architecture 3, since the decision and the quantity are the reviewer's own
Data-native sentence: a patient index holds what registrars typed at each visit and what an earlier merge rule did
  with it, so two records that agree on every field a rule compares may be two people (Port Calder's names are
  concentrated by community and by birth cohort, the men who came to work the boats carry their documents' 1 January
  birth dates, twins share a household, a family was registered under one subscriber's SSN), and every independent
  witness (the blood bank, the delivery log, the registration times) sees only the patients its own process reached.
People: Brenda Hartman (director of health information management; signs the patient identity policy), Felicia Soto
  (the EMPI vendor's implementation consultant; the matching specification), Richard Wood (One Chart program
  director; the conversion plan), drawn with `guard.py names --geo us --seed 1603`; none is named in the prompt.
Decision: before the One Chart conversion on Monday 5 April 2027, Calder Rosario Health's executive team fixes whether
  the Halvard enterprise master patient index may join two patient records without HIM review, and under which of the
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
insurance card, which for a dependent is the subscriber's. The blood bank file is the transfusion service's type and
screen results (surgery, transfusion, trauma); obstetric typing is done in the clinics' outpatient laboratory. The
delivery log holds the births in the two hospitals since 2006; four in ten children of families who came to Port
Calder later were born elsewhere. Halvard Identity's engine scored a 2026 pilot of candidate pairs; HIM reviewed the
pairs in the engine's review band. Every extract is cut on Monday 2 November 2026; as-of date for `leak.py`: 2026-11-04.

Card: `.claude/skills/fingerprint/cards/task16.json`, architecture v4, registered 2026-11-13T23:00:59Z (first filed
with the bare date, which sorted it before every card filed that day; corrected at ship), architecture 3 in its
lineage with why it was spent. WARNs answered at registration: frame_population_mismatch is taught by two tasks and on
two live builds of ours, and here it is one supporting step (Rule C's twins the delivery log never shows) beside a
deciding lesson no task on file teaches; the weight, the answer shape and the decision form are architecture 3's,
because the reviewer asked for the same decision answered with more of its estimation open.
Author's exception (2026-11-13): `guard.py heart` BLOCKs on ban.weight, hard-to-measure repeating task24 v2
(registered 20:36:55Z; a preference-label purchase for a support-reply model, in another subdomain). Nothing in either
build is drawn from the other (the skeleton screen and the client's seven templating signals are clear), the slot has
carried this weight since architecture 3 (registered 00:05:41Z, before task24 v2), and moving it would be a same-day
re-root without new evidence. The call goes before the health system's executive team in the plan, the policy and the
memo; the steering committee of the first cut would have repeated task25 v1's forum.

## Stump screen

Written at architecture 4's redesign (2026-11-13), on the reviewer's own account of what the runs did (they reproduced
the link counts, eliminated three rules on direct counts in the confirming files with no model of the error rate, R79,
and held Rule B's blood mismatches as a reserve, L49). Tests: 1 off the closed page, 2 not a reflex, 3 nothing filed, 4
clean data, 5 two records, 6 the waved-through assumption, 7 a plausible shallower story, 8 across the data, 9 worth the
call, 10 the run's alternative ruled out by named data, 11 the golden can measure it, 12 no easier second route, 13 it
opens its own member.

| Candidate trap | The assumption a run waves through (precedent) | The second record that refutes it | Tests failed | Kept |
|---|---|---|---|---|
| Two different patients share first name, last name, birth date and sex far more often than each field's rate implies: names cluster by community and cohort, and the men who came to work the boats carry their documents' 1 January dates, while the blood bank's typed patients are mostly over 55 (rule A, opened by S_A) | the fields agree independently, at the engine's national rates or the records' own, and a blood check with no discordant link of different SSNs confirms it (L22, L35, L28) | the indexes' joint cells of name, sex and birth year with each surname community's document-date shares by decade; the typed links' birth years against rule A's | none | kept |
| Most twins were registered on separate visits or born before their families came to Port Calder, so the delivery log and the registration times document only some of the twins rule C joins (rule C, opened by S_C) | the documented cases are the cases (L28, L03) | a probabilistic linkage on the fields rule C never compares (each twin's own SSN, phone, visit history), the documented pairs held apart | none | kept |
| Rule B's blood mismatches sit on Calder Bay records that its 2019 merge rule left holding two patients, or on a record whose own typings disagree (rule B, opened by S_B) | a mismatch on a link is a false merge until explained, and is held as a reserve (L49) | the merge history's retired records read against their survivors, the records typed twice or more | none | kept |
| Rosario's subscriber SSN on dependents joins twins under one SSN and birth date (rule D) | an SSN is a person's own | the first names on rule D's links, the delivery log, one visit | 2 (runs read the shared SSN by reflex), 13 (the documented twins already put rule D over its line, so it opens no member) | forced, kept as a result (R4) |
| The 2026 pilot's reviewed pairs as a precision estimate for each rule | the review band stands for every rule's links (L28) | the pilot's band against each rule's links | 9 (no rule's call turns on it once the twins are linked), 12 (the delivery log is an easier route to the same twins) | texture |

## Deep reasoning

Task type: Data integration, record linkage & entity resolution: each candidate automatic linking rule's false
  merge rate at an enterprise master patient index's conversion, estimated against a policy cap, with the converted
  index reconciled to both legacy indexes
Domain test: the results are the field's own quantities: a deterministic match rule's false match rate, the chance
  agreement of identifiers in the population the rule runs on (the u-probabilities and their dependence), what a
  confirming sample covers, overlays and duplicates in a master patient index; the HIM analyst estimates each rule's
  false merges, decides which may run without review, lists the overlays to split and the links they touch, and sizes
  the worklist
Swap: in a retailer's customer-account dedup ("which rule may merge loyalty accounts automatically") the twins of one
  household, the 1 January dates of foreign documents, the transfusion service's typed patients and the delivery log
  as witnesses, and the registration system's 2019 merge rule lose their meaning, and the cap is a patient-safety rule
  a retailer has no reason to hold
Where the weight sits: R2, R3 and R8, one per open member. R2 counts the pairs of patients who share first name, last
  name, sex and birth year in both indexes and prices each pair's chance of one birth date from its surname community's
  1 January and 1 July shares by decade, shrunk toward the decade, then sees why the blood bank cannot check it (its
  typed links were born 27 years earlier than rule A's); R3 links the index on every field the rules do not compare
  and counts the twins it keeps apart beyond the 16 the delivery log and the visits document; R8 reads each of rule B's
  five blood mismatches against the merge history and the records typed twice or more
Layer 1: two exports in different conventions (Calder Bay upper case, the unit in its own column, mm/dd/yyyy; Rosario
  title case from 2016, the unit inline, ISO dates), hyphenated and accented surnames, phones with and without
  punctuation, all-zero and all-nine SSNs typed when none was given, retired MRNs in the blood bank and the delivery log
  that follow Calder Bay's merges to their survivor, married-name records and typed slips; none decides a result
Not one thing: the strongest single piece is R2; a run that nails it still files Rule C on the documented twins, and
  one that also links the twins still files no rule while it holds Rule B's mismatches against it; each of the three
  stumps alone on the careful route leaves the call wrong (Rule C, Rule A, Rule A)
One-fact test: the most useful single sentence rescues one of nine results (effort.json hints): the chance-agreement
  sentence R2 (the call moves to Rule C), the undocumented-twins sentence R3 (the call stays Rule A), the overlay
  sentence R8 (the call stays Rule A); agrees with the Effort test's Largest single hint
Not semantics: every field, unit and clause read correctly (the rules as the plan defines them, the engine's
  standardization, the policy's cap, its denominator, its definition of a patient's record and its choice) leaves rule
  A at the engine's 4.4 or the records' 8.5, rule C at its 16 documented twins, rule B's five mismatches unexplained and
  the call on Rule A
Not rule application: the filed procedures give only each rule's links and, from the false merges, the pick; the
  false merges (R2, R3, R4, R8), the overlays and the links they touch (R5, R9) and the linked index (R1, R7) are
  estimates
Estimand: HIM-14 section 2 defines a patient's record (the record registered for that patient), an automatic link, a
  false merge, an overlay and a duplicate; section 3 caps expected false merges at one per 2,000 automatic links counting
  each pair of records a rule would join, and takes the compliant rule that joins the most pairs, else review; section 4
  splits every overlay before the conversion; the plan's section 7.2 defines the four rules, compared as the engine
  standardizes, on every pair of active records across and within the two indexes as they stand, the 2 November 2026
  extracts the planning baseline; the prompt asks the distinct patients the converted index will hold, how many both
  indexes already hold, the Calder Bay records holding two or more patients, and for the recommended rule the patients
  still under more than one active record once its links are made and its links that touch a record holding two or
  more patients with those records
No decoy: no memo or draft argues a rule; the engine's specification gives its national chance rate for four-field
  agreement ("about one in 10 billion pairs"), the right computation at independent national frequencies, and the
  Rules sheet prices it beside each rule's estimate (the incumbent figure, reproduced and superseded); the pilot's
  decisions are HIM's own on the pairs it reviewed; the blood bank and the delivery log are true records of the patients
  their processes reached
No replay: the pack publishes no false merge rate, overlay count or patient count; nothing is re-derived
Pinned: R2's rivals (each community's document-date share by decade alone 49.5, lightly and heavily shrunk 61.6 and
  57.2) land in 42.1 to 70.8, every one over rule A's line of 32.2; the blood groups net of their errors (1.1) and the
  national and per-field rates (4.4, 8.5) are ruled out by the typed links' birth years and by the joint cells. R3's
  linkage at match probabilities of 0.3 and 0.7 gives 41 both times, inside 34 to 48 over rule C's line of 25.2; the
  documented twins (16) are ruled out because the delivery log covers only births in the two hospitals since 2006 and
  the visits only twins registered together. R8's rivals (mislabel-explained mismatches counted too, every link a visit,
  a delivery or differing groups shows, the overlays' mismatches left out) give 3, inside 0 to 8 under rule B's line of
  17.8; the mismatches scaled from the typed links as a sample (20.8) are ruled out by the typed links' selection. R4's
  rivals (names alone 100, with blood groups 106, a name rule without typing slips 166) land in 85 to 191. R5's rivals
  (the looser name forms 512) land in 471 to 601; every automatic merge whose names differ as typed (1,028) is ruled out
  by the engine's name table. R1, R7 and R9 hold within their bands at match probabilities of 0.3 and 0.7 and with the
  specification's fixed weights at its automatic and review cut-offs (`checks.py`)
Run forecast: R2 method shortcut (chance agreement as a product of per-field rates, confirmed by a blood check that
  cannot see the cohorts where it sits); R3 self-confirming check (the documented twins read as all of them); R8
  unfinished chain (the mismatches held as a reserve, not resolved); R5 and R9 dismissed own evidence (the index taken
  as it stands); R6 and R7 self-confirming check; R1 and R4 earned
Strategy label: F10 Identity resolution, in its live form (`references/sulfur-strategies.md`): the linkage is upstream
  of estimates whose answer depends on match quality, each rule's false merges against a cap
Depth level: 5: three open members, each opened by its own stump (rule A by the chance agreement read from the joint
  distribution, rule C by the twins no confirming file documents, rule B by its mismatches resolved), and the shortcuts
  land on four different wrong answers (Rule A on the careful route or the engine's checks, Rule C with the chance
  agreement alone, no rule with Rule B's mismatches held or the blood groups as they read, Rule D on the blood groups net
  of mislabelled specimens)
Lesson: two records that agree on every field a rule compares are two people far more often than per-field rates say
  when the fields are dependent and locally concentrated, and every confirming record (a blood check, a delivery log,
  one visit) sees only the units its own process reached, so a rule's false merge rate is read from the joint
  distribution of the population it runs on and each witness tests the part it can see; no build on file teaches it
  (`coincidental_agreement_joint_frequencies`, a vocabulary key added 2026-11-12)

## Results chain

| ID | Result (checkable) | Area | Pinned by | Band | Hurried analyst | Depends on | Graded as |
|---|---|---|---|---|---|---|---|
| R1 | the converted index: 212,402 distinct patients, 69,318 of them held by both Calder Bay and Rosario | assembly-reconciliation | HIM-14's definitions; the prompt's distinct patients and patients both indexes hold; both indexes and the merge history's retired records | distinct patients within 1.5 per cent, both within 2.5 per cent | narrow look at broad data: one patient per exact name, birth date and sex, nicknames, married names, swapped order and typed slips left apart (the quick pass); the careful pass's linkage earns it | - | Ask 3 |
| R2 | rule A's false merges: 59.5 of its 64,484 links, 1.85 per 2,000, a third of them among men born since 1975 | modeling | HIM-14's false merge and cap; the plan's rule A; the two indexes | 42.1 to 70.8 | method shortcut: chance agreement as the product of each field's own rate, at the engine's national rates (4.4, 0.14 per 2,000) or the records' own (8.5, 0.26), confirmed by a blood check with no discordant link of different SSNs, the fields' dependence never read | - | Component 1 |
| R3 | rule C's false merges: 41 pairs of twins among its 50,411 links, 1.63 per 2,000 | validation | HIM-14's false merge; the plan's rule C; the indexes, the delivery log, the registrations' times | 34 to 48 | self-confirming check: the delivery log's and the visits' 16 documented twins read as all of them (0.63 per 2,000) | - | Component 2 |
| R4 | rule D's false merges: 104 of its 42,835 links, 4.86 per 2,000, twins under a parent's SSN | investigation-loops | the plan's rule D; the indexes' first names, the delivery log, one visit | 85 to 191 | stopped at the first story: every link with names unalike as typed (2,429), the engine's name table unread; the careful pass, reading it, earns the result | - | Ask 1 |
| R5 | Calder Bay records holding two or more patients: 556, listed by surviving MRN | missingness-measurement | HIM-14's overlay; the merge history's retired records as they stood, the delivery log, the blood bank | 471 to 601 | dismissed own evidence: Calder Bay's index taken as it stands (none), or every automatic merge whose first names differ as typed (1,028) | - | Ask 2 |
| R8 | rule B's false merges once its blood mismatches are explained: 3 (0.17 per 2,000): of its 5 mismatches 3 on Calder Bay records that hold two patients, none a mislabelled specimen, 2 left as false merges, beside the twins one visit shows | investigation-loops | HIM-14's patient's record ("registered for that patient") and its overlay; the blood bank, the merge history | 0 to 8 | unfinished chain: the mismatches read as false merges and scaled from the typed links (122, 6.86 per 2,000), held as a reserve against approving the rule | - | Component 3 |
| R6 | the rule the conversion runs: Rule B, 0.17 false merges per 2,000 links, with A, C and D over the cap | synthesis | HIM-14's cap and its choice of the compliant rule that joins the most pairs | exact | self-confirming check: Rule A, passed by the per-field rates and a blood check that cannot see where its merges sit | R2, R3, R8 | Recommendation |
| R7 | patients still under more than one active record once Rule B's links are made: 44,567 | modeling | HIM-14's duplicate; R1's linked index and R6's rule | within 3 per cent | self-confirming check: the duplicates left after the rule the careful pass runs (Rule A, 19,133) | R1, R6 | Ask 4 |
| R9 | Rule B's links that touch a record holding two or more patients: 124, touching 119 such records, each split before those links are made | assembly-reconciliation | HIM-14 section 4; R5's overlays and R6's rule | links 105 to 144, records 101 to 138 | dismissed own evidence: the index taken as it stands, so no link touches an overlay; or the links of the rule the careful pass runs (Rule A) | R5, R6 | Ask 5 |

Carry-forward: R1 to R5 and R8 stand on inputs of their own (the linked index; the joint cells of the two indexes;
the twins' linkage; rule D's links and names; the merge history; rule B's typed links); R6 falls with R2, R3 or R8, R7
with R1 or R6, R9 with R5 or R6. A run that misses the chance agreement keeps R1, R3, R4, R5 and R8; one that misses the
twins keeps R1, R2, R4, R5 and R8; one that holds Rule B's mismatches keeps R1 to R5.

## Open members

| Member | Golden margin | Family spread | Reflex route | Direct route | Opened by |
|---|---|---|---|---|---|
| Rule A | 59.5 false merges against its line of 32.2 (+27.3) | 10.0 (49.5 to 61.6) | wrong: 8.5, the records' own field rates with no discordant link of different SSNs to raise it | wrong: 4.4, the engine's national rates the blood check does not contradict (0 discordant links with different SSNs among 1,517 typed links rule B does not make) | S_A |
| Rule B | 3 against its line of 17.8 (14.8 under) | 0 | wrong: 122, its 5 blood mismatches held as false merges and scaled | wrong: 122, the blood bank's results as they read | S_B |
| Rule C | 41 against its line of 25.2 (+15.8) | 0 (41 at a match probability of 0.3 and of 0.7) | wrong: 16, the delivery log's and the visits' documented twins | wrong: 16, the documented twins counted | S_C |
| Rule D | 104 against its line of 21.4 (+82.6) | 4.0 (names alone 100, with blood groups 106; 166 without typing slips) | right: 104 | right: 59 documented twins, already over its line | forced |

Direct route: for each member, the pack's most direct evidence read at face value, run by `forcing.py` and `results.py`
beside the other shortcuts: rule A, the blood bank's discordant links whose two records carry different SSNs among the
links rule B does not make (the reviewers' runs' own count, R79), 0 against the national rates' 4.4, so the national
rate stands and Rule A passes; rule B, its blood mismatches as they read (5 of 2,213 typed links, 122 scaled), so it
fails; rule C, the twins two newborns of one delivery or one registration visit document (16), under its line, so it
passes; rule D, its documented twins (59), already over its line. Each lands wrong for the reason the process gives it:
the transfusion service's patients are mostly over 55 (their typed links born 27 years before rule A's), a record a
2019 merge left holding two patients carries a second patient's typing, and the delivery log holds only births in the
two hospitals since 2006 while most twins were registered on separate visits. Three members are open, each by its own
stump: level 5.

## Hidden factor record

| Factor | Real or constructed | Only in deciding units | Found by | Fix depth | Verdict |
|---|---|---|---|---|---|
| surnames concentrated by community and first names by birth cohort within each community | constructed from public frequencies (the 2010 Census surnames by race and Hispanic origin; curated first-name curves by group, sex and cohort) | no: every community and cohort, from the Garcia and Nguyen cohorts to names one family holds | modelling: the pairs of patients sharing first name, last name, sex and birth year, counted in both indexes | modelling | keep |
| working-age men who came for the boats and the yards, single on arrival, named as their home towns named boys, many carrying 1 January document dates | constructed (the simulated households: 7 per cent of Hispanic and 12 per cent of Vietnamese households) | no: every community's men of those cohorts (1 January on 3.0 per cent of men born 1978 to 2003 against 0.8 per cent of women); they decide rule A only with the rest of its chance merges, two-thirds of which lie elsewhere | modelling: each surname community's document-date shares by decade in the joint cells | modelling | keep |
| birth dates on 1 January and 1 July for older patients born abroad | constructed (the simulated foreign-born share by group and decade) | no: Vietnamese and Hispanic cohorts of every decade at their own shares | modelling: each community's shares by decade, shrunk toward the decade | modelling | keep |
| the transfusion service's typing, mostly patients over 55 | constructed (the simulated blood bank) | no: every typed record (72.8 per cent over 55; obstetric typing in the clinics' laboratory, outside the file) | a comparison of the typed links' birth years with the rule's | modelling | keep |
| twins (1.65 per cent of deliveries, an eighth with similar first names), registered together a quarter of the time, four in ten of the families that came later born elsewhere | constructed (the simulated families) | no: every community and year; they carry rules B, C and D's false merges and touch rule A's | modelling: a probabilistic linkage on the fields the rules do not compare, the delivery log and one visit as documented pairs | modelling | keep |
| Calder Bay's automatic merge on last name, birth date and sex from March 2019 | constructed (the simulated registration system) | no: every new Calder Bay registration since March 2019; its overlays reach rule B through 3 of its 5 mismatches and every rule's links | a classification: each automatic merge's retired name against the survivor's, the clinical evidence for names that agree | modelling | keep |
| Rosario's subscriber SSN on dependents until June 2021 | constructed (the simulated registration screen) | no: every Rosario dependent registered before mid-2021; it reaches rule D only through twins | a targeted query: one SSN on records with different first names and birth dates | routine | keep (R4 only; careful runs land it) |
| mislabelled specimens, about one in 2,600 | constructed (the simulated blood bank) | no: every typed patient (27 of 12,838 records typed twice or more disagree with themselves) | a targeted query: records typed twice or more whose typings disagree | routine | keep |

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
| R8 rule B's false merges once its blood mismatches are explained | Right | Missed | Right |
| R9 the recommended rule's links that touch a record holding two or more patients, and the records split | Missed | Missed | Right |
| Roughly | 1 of 9 | 2 of 9 | 9 of 9 |

Measured by: .claude/skills/stumping/effort.py on generator/effort.json (the passes are the generator's own routes on
  the cut pack: the quick pass one patient per exact name, birth date and sex with every rule's links taken as true; the
  careful pass the stump factorial's reflex route: every file conformed, a probabilistic linkage of the active records,
  each rule's links reproduced, the documented failures in the confirming files counted against each allowance with no
  model of the error rate, rule B's mismatches held, Calder Bay's index as it stands; the golden)
Largest single hint: "Two different patients here often share a first name, last name, birth date and sex: names
  cluster by community and birth year, and many men who came to work the boats carry 1 January birth dates."; rescues
  1 of 9 results (each stump's sentence rescues one)
Pair estimate: 29.0 (the careful pass earns R1 and R4 and the instruction-following share; every lost cell cites a
  precedent of its own class)

## Stump factorial

Reflex route: every file conformed, a probabilistic linkage of the active records, each rule's links reproduced (R80),
the documented failures in the confirming files counted against each allowance with no model of the error rate (R79):
rule A at the records' own field rates (8.5) with no discordant link of different SSNs to raise it, rule C at its 16
documented twins, rule D at its links whose names are not one person's or that a visit or a delivery shows (104), rule
B's 5 blood mismatches held as false merges (122); Calder Bay's index as it stands: Rule A passes at 0.26 per 2,000 and
the conversion would run it. This route is the careful but hurried pass, and it misses the call.

| Judgment | Kind | Hurried choice | Evidence | Dropped alone from the golden | Fixed alone on the reflex route | One routine step once told |
|---|---|---|---|---|---|---|
| S_A rule A's false merges from the joint distribution of first names, surnames, sex and birth years, each pair's chance of one birth date read from its surname community's document dates | stump | the per-field rates, confirmed by a blood check with no discordant link of different SSNs | L22, L35, L28 | Rule A (R2, R6, R7, R9 move) | Rule C; rescues R2 | no (the joint cells of two indexes counted, each community's 1 January and 1 July shares by decade shrunk toward the decade, the blood check's selection read before it is trusted) |
| S_C rule C's false merges from the twins the probabilistic linkage keeps apart, the documented ones and the ones no file documents | stump | the documented twins counted as all of them | L28, L03 | Rule C (R3, R6, R7, R9 move) | Rule A; rescues R3 | no (a Fellegi-Sunter linkage fitted by EM on the fields the rules do not compare, the documented pairs held apart, its false links on rule C's pairs counted) |
| S_B rule B's blood mismatches explained: the records that hold two patients and the specimens a record's own typings contradict, the rest left as false merges | stump | the mismatches held as false merges and scaled | L49 | no rule (R6, R7, R8, R9 move) | Rule A; rescues R8 | no (the merge history's retired records read against their survivors to find the overlays, each mismatch attributed, the rest counted as found) |
| J1 each rule's links reproduced by the engine's standardization | reflex | - | R80 | same call | - | - |
| J2 the confirming files' documented failures counted against each rule's allowance | reflex | - | R79 | same call | - | - |
| J3 rule D's links whose first names are not one person's, the subscriber's SSN on a dependent | reflex | - | R79, R14 | same call (rule D over its line on every reading) | - | - |
| J4 both indexes conformed and a probabilistic linkage of the active records | reflex | - | R01, R20 | same call | - | - |

Level: 5 (three necessary stumps, none sufficient, on three distinct wrong answers when one is dropped: Rule A, Rule C,
no rule)

## Data provenance

Source: generated by task16/generator from a simulated population of Port Calder, Texas (seed 16041): 68,000 households
  with births, twins, deaths, moves, phones, SSNs, insurance and blood groups, the working-age men who came alone for
  the boats and the yards among them; each person's visits to Calder Bay and Rosario from 2006 and each registration as
  a registrar typed it; Calder Bay's automatic merges from March 2019 and both systems' HIM merges; the transfusion
  service's type and screen results, the labor and delivery log and the state's death notices. Surnames come from the
  U.S. Census Bureau's 2010 surname file (public domain, pulled 2026-11-12) by each community's race and Hispanic origin
  shares; first names from curated cohort curves by group and sex, and the workers' from their home towns' lists.
Behaves like the real thing: a few per cent of each index's active records are a second record of a patient within the
  same index, at the low end of what master patient indexes report because both systems merge the duplicates they
  find, and a third of the patients are known to both indexes; twin deliveries at 1.65 per cent; mislabelled specimens
  near the published one in 2,000 to 3,000; first names follow cohort fashion and surnames community; 1 January birth
  dates are common among refugees and immigrants whose documents carry no day; transfusion services type mostly older
  surgical patients; registrations rise with age and pregnancy; deaths with age.
Genuine patterns: (1) first-name fashion by cohort within each community (2) surnames concentrated by community
  (3) birth-day heaping on 1 January and 1 July by community, decade and sex (4) duplicates from nicknames, typed slips,
  married names, a dropped second surname and swapped name order (5) movers' addresses and phones changing over time
  (6) registrations rising with age and pregnancy (7) typing concentrated in patients over 55 (8) twins registered on
  one visit or apart, born in the two hospitals or elsewhere (9) deaths rising with age
Problems by process: two systems' export conventions; Rosario's title case from 2016; the subscriber's SSN on
  dependents until June 2021; Calder Bay's 2019 automatic merge; mislabelled specimens; retired MRNs in the blood bank
  and the delivery log; all-zero and all-nine SSNs typed when none was given
License: the surname frequencies are a U.S. Government work in the public domain; everything else is generated for
  this task (CC0-1.0)
Used as is: the Census counts and shares are read as published to draw surnames; no row of them ships
Breadth: 13 files (two indexes of 294,713 active records between them, the blood bank's 69,879 results on 53,629
  records, 15,997 deliveries, 10,280 merges, the name table, the pilot workbook with 852 reviewed pairs, three PDFs, and
  three distractors: the registration volumes, Rosario's duplicate report and the matched death notices), about 213,000
  patients across hundreds of surname communities and cohorts, so choosing which cells carry the chance agreement and
  which witness sees which part of each rule's false merges is work

## Template check

Chain signature: assembly-reconciliation, modeling, validation, investigation-loops, missingness-measurement,
  synthesis, modeling, investigation-loops, assembly-reconciliation
Question form: whether (and under which rule)
Nearest build: task16 architecture 3 (this slot's lineage): the same decision, data and policy at the reviewer's
  request, with the members' decisions moved from direct counts onto estimation (three open members against one) and
  two results added (R8, R9); task3 v7 shares the answer shape and the weight, its candidates unrecorded sites ranked on
  forecast exceedances. Abstraction sentence: none writable against task3

## Frontier check

Precedents: R2 L22 (the published formula whose generating assumption the data contradict), L35 (an independence
  binomial where units share shocks), L28 (an estimator certified with checks that cannot see the problem); R3 L28,
  L03 (a second log at another grain set aside); R5 L03, L49; R6 L22, L28, L49; R7 L28, L49; R8 L49 (an option's residual
  discordant evidence held as a reserve instead of resolved, the mismatches overlays on earlier merge survivors: this
  build's own architecture 3 runs); R9 L49, L03. R1 and R4 carry none: the careful column lands them.
Shallow path checks: R2: the independence product reproduces the engine's specification exactly ("about one in 10
  billion pairs", 4.4 here) and the records' own field rates give 8.5, both inside the line, and the blood bank's
  discordant links with different SSNs among the links rule B does not make number 0, exactly the national rate's
  prediction; net of mislabelled specimens and overlaid records the blood groups give 1.1; only the joint cells of name,
  sex and birth year (another grain than any field's frequency) with each community's 1 January share by decade give
  59.5, and the typed links' birth years (1955.9 against rule A's 1983.3) show why the blood check cannot see it. R3: the
  delivery log and one visit document 16 of rule C's twins, under its line, and the pilot reviewed none of its links;
  only the linkage on each twin's own SSN, phone and visit history keeps 41 apart. R8: read as they stand rule B's 5
  mismatches put it at 122; only the merge history's retired records (event grain) show 3 of them on records holding two
  patients. R5 and R9: the index as it stands shows no record with two names. R6 and R7 follow the rule and R1.
Assumption made false: that agreement on each field is independent of agreement on the others (the Fellegi-Sunter
  model's own assumption, named and waved through as standard: L22, L35), and that a blood check with no discordant
  link confirms it (L28): false here because first names follow cohorts within communities, surnames concentrate by
  community and the workers' documents put their birth dates on 1 January, while the transfusion service types mostly
  patients over 55; tested by the indexes' own joint cells and the typed links' birth years. That the documented cases
  are the cases (L28): false because most twins were registered apart or born elsewhere; tested by the linkage. That a
  mismatch on a link is a false merge until explained (L49): false because a 2019 merge left records holding two
  patients' typings; tested by the merge history.
Forcing: the line is one false merge per 2,000 links (A 32.2, B 17.8, C 25.2, D 21.4 false merges); the golden family's
  ten variants (rule A by decade alone 49.5 and with light and heavy shrinkage 61.6 and 57.2; rule C on the linkage at
  0.3 and 0.7, 41 both; rule B with mislabel-explained mismatches counted and with every evidence-flagged link counted,
  3 both; rule D from names alone 100, with blood groups 106, without typing slips 166) keep A, C and D over and B under,
  all filing Rule B, the nearest rule A at 1.54 per 2,000 and rule C at 1.63; the 12 shortcuts file Rule A (the careful
  route, the engine's checks, each stump fixed alone but S_A), Rule C (S_A fixed alone, the documented twins), Rule D
  (the blood groups net of mislabelled specimens) and no rule (Rule B's mismatches held, the blood groups as they read,
  Rule B's mismatches scaled as a sample); each estimate moved (rule A, C or D 20 per cent lower, rule B three times
  higher) leaves Rule B standing.
Noun swap: the nearest skeleton is this slot's architecture 3 (severity none against it: the deciding lesson is kept,
  the two others are new, and the answer pattern's members now open three ways); the others on file (task4 v12, task20
  v2, task13 v4, mark124 v6) are severity none; swapped into task13 v4 (automated feeder restoration) the deciding move
  here (chance agreement read from a population's joint cells) has no place.
Closed strategies: the call turns on coincidental_agreement_joint_frequencies, off the client's closed page; the
  nearest closed card is "dependent capture" (two lists' captures of one unit dependent, biasing a capture-recapture
  total, fixed by a log-linear model with an interaction term): here the dependence is between the identifying fields
  of two different units in one population, and the fix is the chance that two distinct patients agree on every
  compared field, read from the population's joint cells and its birth-day heaping, to price a rule's false merges.
  The chain keeps no closed lesson as a supporting step (`skeleton.py closed task16`: 0 of 3 closed);
  frame_population_mismatch is taught twice and on two of our live builds, and here it is one supporting step (rule C's
  twins) beside the deciding one.

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
| SF8 | the cap | expected false merges no more than one per 2,000 automatic links, inclusive | as written | HIM-14 section 3; same call (B at 0.17, A and C over 1.5) |
| SF9 | expected false merges | the expectation the evidence gives; the realized count; an upper bound | the expectation | HIM-14's "expected"; same call (no rival puts B over 0.5 or A, C or D under 1.3) |
| SF10 | the rule the conversion runs | the compliant rule that joins the most pairs; the safest | the most pairs | HIM-14 section 3 |
| SF11 | twins and siblings | two different patients | two patients | HIM-14 section 2 |
| SF12 | distinct patients the converted index will hold | every patient an active record holds, the patients an overlay hides included; patients with an active record of their own | the first | same call: the two differ by the 556 overlays, a quarter of one per cent, inside the band |
| SF13 | patients both indexes already hold | a patient with an active record in each index | as written | the prompt |
| SF14 | an overlay | an active Calder Bay record that also holds another patient's information, counted once per record | per record | HIM-14 section 2 and the prompt's "Calder Bay records" |
| SF15 | a duplicate left | a patient whose active records fall into two or more groups once the rule's links are made, counted once per patient | per patient | HIM-14 section 2 ("A patient held under more than one active record is a duplicate") |
| SF16 | per 2,000 links | 2,000 times false merges over the rule's automatic links | as written | HIM-14 section 3 |
| SF17 | a rule's link that touches a record holding two patients | a false merge; a link of the patient the record was registered for, the record split before the conversion | the second | HIM-14 sections 2 ("registered for that patient") and 4 (every overlay found is split before the conversion) |
| SF18 | rule B's false merges from its blood mismatches | the mismatches no overlay or mislabelled specimen explains, counted as found; the mismatches scaled from the typed links to all of them | counted as found | named data: the typed links are a selected sample (72.8 per cent of typed records are over 55; rule B's typed links are 6.2 per cent of its links), so a scale-up treats two found pairs as a rate; same call either way for the overlays, which no reading counts once SF17 holds |
| SF19 | the recommended rule's links that touch a record holding two or more patients | links with at least one record among the overlays, each pair once; with the records counted once each | as written, links and the distinct records they touch | the prompt ("how many of its links touch a record that holds two or more patients, and how many such records") |
| SF20 | the confirming files as evidence | each tests the estimate on the patients its process reached; each counts its cases as all of them | tests | named data: the delivery log holds births in the two hospitals since 2006, the blood bank the transfusion service's patients; same call as the golden on every reading that weights each witness to what it covers |

## Pinning list

| Constant | Golden value | Home |
|---|---|---|
| each surname community's 1 January and 1 July shares by decade | shrunk toward the decade's at 20 records | the two indexes' birth dates (calder_bay_patient_index_2026-11-02.csv, rosario_patient_index_20261102.csv); shrinkage 5 and 60 in the family, their measured spread 49.5 to 61.6 |
| the chance two patients' groups differ | 0.66 | the blood bank's type mix (blood_bank_type_screen_2016-2026.csv) |
| the mislabelled-specimen rate | 27 of 12,838 records typed twice or more | blood_bank_type_screen_2016-2026.csv, the records typed twice or more |
| the linkage's match probability | 0.5 | Fellegi-Sunter weights fitted by EM on the indexes; 0.3 and 0.7 in the family, the measured spread nil on rule C |
| the engine's name equivalence | as tabled | halvard_name_equivalence_table.csv |
| the rule C similarity floor | Jaro-Winkler 0.92 | one_chart_empi_conversion_plan.pdf section 7.2 |

Variant battery: 16 variants of the modelled readings were run on the cut pack (three of rule A's chance agreement, two
of rule C's linkage, two of rule B's mismatch attribution, three of rule D's name rule, two of the overlays' name forms,
and four of the linked index at match probabilities of 0.3 and 0.7 and the specification's fixed weights at both
cut-offs), and every variant files one answer, Rule B.

## Closure table

| Axis | Closure |
|---|---|
| 1 | Population: every active record in the two 2 November 2026 extracts; Calder Bay's retired records enter only as evidence of the patients a merge joined or hid |
| 2 | Unit of account: the pair of records for links and false merges; the patient for the index figures; the record for overlays; the link and the record for R9 |
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
| 21 | Clause scope: HIM-14's cap applies to every rule alike; section 4's split applies to every overlay found |
| 22 | Forward window contents: the conversion's links are the rules applied to the records as they stand (SF5) |

## Literal reader

Executing HIM-14 sections 2 to 4 and the plan's section 7.2 word for word: each rule is applied to every pair of active
records across and within the two indexes as the engine standardizes them, each rule's false merges are the links it
would make between records registered for two different patients, the cap is one per 2,000 of its links, every overlay
found is split before the conversion, and the conversion runs the compliant rule that joins the most pairs. A reader
who takes the engine's chance rates, the documented twins and the blood bank's mismatches as they stand files Rule A
against section 2's "two different patients", which those counts never complete; one who reads every rule from the
blood groups files no rule, against section 2's "registered for", which an overlay's typings are not. Neither is
another reading: each is an easier method on the same filed estimand.

## Prompt contract

A voice rewrite keeps: the question (whether One Chart can link patient records automatically when the two indexes
convert on 5 April 2027, and under which of the conversion plan's candidate rules); the policy's limit of one
expected false merge per 2,000 automatic links; each rule's automatic links, estimated false merges and false merges
per 2,000 links; the distinct patients the converted index will hold and how many both indexes hold; whether any
Calder Bay records already hold two or more patients and, if so, how many and which; if a rule is recommended, the
patients still under more than one active record once its links are made, and how many of its links touch a record
that holds two or more patients and how many such records; a spreadsheet and a one-page PDF note. It never adds a rounding
instruction, a method (no twins, chance, independence, birth dates, 1 January, frequencies, names, blood groups,
typing, delivery log, pilot, merge history, SSN, subscriber, workers or nicknames), a warning, an attached file's name,
a role or reader, or a count the data hold (no four rules).

## Pre-ship check

- Bar re-read on the built pack: nine results across seven areas (assembly and reconciliation, modeling, validation,
  investigation loops, missingness and measurement, synthesis), each pinned by a filed sentence (HIM-14 sections 2 to
  4, the plan's section 7.2, the specification's standardization) and the data, with the bands the answer blocks
  state; precut 112 checks, 0 FAIL, 2 WARN (answered in the Hidden factor record and the Template check); checks.py
  139 checks with the rival linkages, 0 FAIL; verify.py 0 FAIL on its own code path, the direct routes recounted from
  the pack (rule A's blood-discordant links with different SSNs 0 of the 1,517 typed links rule B does not make; rule
  A's 5 mismatches in 3,730 typed links; rule B's 5 in 2,213); gates.py 8 gates, 1 FAIL (heart's ban.weight BLOCK
  against task24 v2, the author's exception: Draw), 2 WARN; two fresh builds of the final generator byte-identical
  with each other and with the shipped folder (19 files); the note ships as a one-page PDF exported from Word (verify
  reads it back: one page, addressed to the executive team).
- Golden against the simulated truth: rule A 59.5 against 47 (the expectation HIM-14 caps against one realization's
  count, SF9), rule B 3 against 3, rule C 41 against 47, rule D 104 against 103; overlays 556 against 551; distinct
  patients 212,402 against 213,173; patients in both indexes 69,318 against 69,770; patients left after Rule B 44,567
  against 44,662.
- Hidden factor record against the cut data: 1 January birth dates on 1.6 per cent of the 294,713 active records, on
  3.0 per cent of men born 1978 to 2003 against 0.8 per cent of women, and on 9.3 per cent of Nguyen patients born in
  the 1950s against 1.8 per cent of their decade; 243 of the 15,754 deliveries since 2006 carry two or more newborns;
  53,629 records carry blood bank results, 72.8 per cent of them over 55 (mean age 62.7 against the index's 45.2); 27
  of 12,838 records typed twice or more disagree with themselves; 556 Calder Bay survivors of the 2019 merges hold two
  or more patients.
- Effort test against effort.py: quick 1 of 9 (15.0), careful 2 of 9 (29.0), thorough 9 of 9; the largest hint rescues
  1 of 9; twelve shortcuts land on four different wrong answers (Rule A five times, Rule C three, no rule three, Rule D
  once); the stump factorial at level 5 (each stump dropped alone files Rule A, Rule C or no rule, each fixed alone on
  the reflex route Rule C or Rule A).
- Forcing: Rule B at 0.17 per 2,000 against the line of one (3 false merges against its line of 17.8), rule A at 1.85,
  rule C at 1.63 and rule D at 4.86 over it; every golden-family variant (11) and every perturbation (4) files Rule B.
- Open members against the cut: rule A's direct reading (0 discordant links with different SSNs) leaves the national
  rate standing and Rule A passing; rule C's documented twins (16) sit under its line of 25.2; rule B's mismatches as
  they read (122 scaled) put it over its line of 17.8; rule D's documented twins (59) are over its line on their own.
- Determinism judge, determinism only, from the answer blocks: DETERMINISTIC and APPROVE twice, no fix. Pass 2 (cut
  b787faf9) rebuilt the specification's standardization and reproduced the active records (294,713), every rule's links
  (B and D exactly, A within 3 links, C within 0.03 per cent on either reading of the name table), the four lines, rule
  A's 3,730 typed links and their 5 mismatches, and rule B's resolution record by record (3 on overlaid Calder Bay
  records, 2 of them under one SSN, none a record whose own typings disagree, 3 false merges, 0.17 per 2,000); its own
  overlays 536 (band 471 to 601), rule B's links on them 116 on 112 records (bands 105 to 144 and 101 to 138); its forks
  (the name table pair by pair or transitive; blood group as ABO alone or with Rh) moved nothing, and at every band edge
  the call holds (A 1.30, C 1.35 and D 3.97 over the line, B 0.45 under it). Two answer-block wordings followed, as the
  stage 4 rule allows: each rule's links within 0.1 per cent under another careful reading of the standardization, and
  the mismatches stated as differing in ABO group or Rh type. Pass 3 (the final cut 4c1045ec, re-judged once because
  the pack moved: the plan's and the policy's deciding body) reproduced the same: B and D's links exactly, A and C inside
  the stated 0.1 per cent, the same 5 mismatched pairs and the 3 on overlaid records; overlays 584 with a 0.92 typing
  slip threshold (inside 471 to 601), rule B's links on them 126 on 121; "active" closed by the files (every death
  notice MRN sits inside the 294,713). Neither pass refit the EM linkage in budget (R1, R7), whose rival linkages land
  inside their bands in checks.py. Pass 3 rebuilt 12 of rule C's 16 documented twins from the delivery log alone in
  budget; verify.py now recounts all 16 from the delivery log and the registration times on its own code path.
- Leak: leak.py REVIEW only (--asof 2026-11-04, the dates sweep and the prompt gate clean): the plan's and the
  policy's words of the rules and the conversion, the specification's and the policy's field words, each ruled harmless
  in the report. One isolated read at medium effort on the final cut 4c1045ec (the executive team deciding, the PDF
  note): NO LEAK, no ranking file, no helper file, no one thing; it read the standardization and the plan's section 7.2
  as the comparison convention and the population, and the policy's section 3 as the rule that chooses once the rates
  are estimated. The read of cut b787faf9 found the same, with the specification's national rate as the figure closest
  to an answer (the incumbent's claim) and Rule C's 0.92 against the specification's 0.88 as two thresholds for two
  uses.
- Gate findings answered: precut's constructed factors (Hidden factor record) and nearest chain (Template check);
  heart's BLOCK on ban.weight against task24 v2, the author's exception (Draw), and its WARNs: strategy_risk (the call
  turns on estimating each rule's false merges, never on a field or a stated rule: Open members), chain_near against
  task3 (Template check), overuse.forum (the health system's executive team decides, the house's most used forum; the
  steering committee would have repeated task25 v1's), and the skeleton's lesson WARNs (Draw). The voice check is clean
  with the PDF note.
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
- 2026-11-13, architecture 3 sent back at review (reward 78, stumped failed, determinism and solution passed; runs/review_2026-11-13.md): Rules A, C and D failed on direct counts in the confirming files (the delivery log's 45 and 76 twin pairs against allowances of 28 and 23; rule A's 16 blood-discordant links with different SSNs against about 0.3), so the call collapsed to Rule B or none and the runs lost only by holding Rule B's eight mismatches as a reserve; the step 4 count stated 30 of 8,043 typed pairs against the file's 32. Redesigned in the same world as the reviewer asked (architecture 4), under stumping Part 3.4.
- 2026-11-13, architecture 4 prototype: cutting the older cohorts' 1 January shares alone left rule A's false merges where the blood bank types, so its blood check still settled the rule in most seeds; working-age men who came for the boats and the yards, single and named from their home towns' lists with their documents' 1 January dates, were added, and the older cohorts' commonest names (Maria, Jose, Juan, Guadalupe) flattened toward their real shares.
- 2026-11-13, architecture 4 prototype: typing young women at pregnancy exposed their fashionable-name merges (Jennifer, Emily, Veronica) to the blood check; the blood bank file now holds the transfusion service's type and screen results (surgery, transfusion, trauma), obstetric typing done in the clinics' laboratory outside it, so 72.8 per cent of typed records are over 55.
- 2026-11-13, architecture 4 prototype: twins with similar first names at 0.28, registered on their twin's visit at 0.72 and all born in the two hospitals put rule C's documented twins over its line (the reviewer's direct count); now 0.13, 0.25, and four in ten of the later families' children born elsewhere, so the documented twins sit under the line and the total over it.
- 2026-11-13, architecture 4 seed scan: the blood check on rule A rests on one to three typed pairs of older patients in any realization (mislabelled specimens alone give about two discordant pairs per 2,600 typed pairs), so 40 seeds were scanned; seed 16041 is the only one where rule A's direct reading lands wrong, rule C's documented twins sit under its line with its total over, and rule B's mismatches fail it until explained. The golden's rule A (59.5) sits 27 per cent above that realization's count (47), inside the expectation HIM-14 caps (SF9).
- 2026-11-13, architecture 4 build: rule B's golden first counted only the twins a visit shows (1) while 2 of its 5 blood mismatches are neither overlays nor mislabelled specimens; they are counted as found (3). Scaled from the typed links as a sample they gave 20.8, over the line; that reading is a shortcut route now, ruled out by the typed links' selection (SF18).
- 2026-11-13, architecture 4 build: a golden-family variant carrying rule A's chance agreement onto rule B's share of rule A's links (36, over rule B's line) was dropped: rule B also needs the same street address, which two strangers almost never share.
- 2026-11-13, architecture 4 build: rule D's band from its first family (85 to 122) left out the name rule without typing slips (166); that rival is in the family now and the band is 85 to 191 (rule D is a forced member).
- 2026-11-13, architecture 4 ship: the card had been rewritten in place with a bare-date registration stamp, which sorted it before every card filed that day, so `heart` screened it against an older window; with its true time (23:00:59Z) `heart` BLOCKs on ban.weight against task24 v2, kept as the author's exception (Draw). The card's forum (executive team) did not match the pack, whose steering committee would have repeated task25 v1's forum; the plan, the policy and the note now put the call before the health system's executive team. The memo ships as a one-page PDF note exported from Word, the Word memo and workbook pair being over the prompt-shell quota (25 per cent of 24 prompts against 20).
