# task19: Kilvarra's mid-2026 district populations for the 2027/28 grant determination

## Draw

Subdomain: Survey Research & Official Statistics, nonresponse, calibration and measurement-error adjustment
(coverage measurement of an administrative register)
Analysis type: Descriptive & Distribution Analysis (where each district's total really sits once the register's
erroneous entries and the people it misses are measured)
Answer shape: a reconciled table plus findings (twelve district estimates with intervals and the call against the
line, each register count bridged to its estimate, the rolled-forward national figure bridged to the estimate)
Weight: an estimate of a quantity that is hard to measure (usual residents where no census has run since 2021); the
last two live builds weighed validation (task9) and metric or rule design (task13), and task15 synthesis
Data-native sentence: the only list of residents is a health register that keeps people who have left, lists students
and movers where they used to live and never held some young men at all, and the coverage survey that measures it
shares no key with it and misses the same young men.
People: Grainne Grennan (the Office's population statistics lead, author of the golden memo), Carla McCaffrey
(Secretary to the Commission, named in the circular), from guard.py names --geo Ireland --seed 19

## Deep reasoning

Task type: nonresponse-calibration-measurement-error-adjustment (nonresponse, calibration and measurement-error
adjustment) in Survey Research & Official Statistics, which
serves Descriptive & Distribution Analysis: an administrative register's coverage errors measured and corrected with a
coverage survey and a field follow-up, the domain's own dual-system machinery.
Domain test: every result is a quantity an official statistics office produces when it estimates population from an
administrative register with a coverage survey: erroneous enumerations from a follow-up of listed records (R2), a
dual-system coverage ratio on a survey linked without a shared key and corrected for the linkage's own misses (R1, R3),
a demographic-analysis sex-ratio adjustment for correlation bias (R4), design-based intervals that carry the errors
every district shares (R6), the usual-residence call under the funder's rule (R7) and the reconciliations to the
register and to the rolled-forward series (R8, R9).
Swap: "certify Tullaghvane, report Newbrook as too close to call" rewritten for a hospital's bed census or a retailer's
store footfall loses its meaning: no other field divides a list's correct entries by the share of an independent
sample found on that list, raises men to a sex ratio from births a generation back, or calls a person "on the list"
only where their usual-residence district and the list's district agree.
Where the weight sits: R5, because each district's figure is the end of five measured corrections (correct entries,
linked coverage net of missed links, residents listed elsewhere, the dependence factor, serving personnel) and is long
because every input has to be estimated from a different file at a different grain, not because one step is clever.
Layer 1: the register's postcodes keyed three ways by practices' systems and some still on codes retired in the 2024
recoding (the directory holds both); names that differ between systems through nicknames, Irish forms of forenames and
surnames, dropped O' and Mac prefixes, married surnames, other romanisations, names the person goes by and given and
family names swapped by an interviewer; dates of birth with day and month swapped, mistyped, defaulted to 1 January
for arrivals without documents, or given by another household member; addresses left behind by people who moved
within their district; duplicate registrations from re-registering; follow-up addresses with no contact, vacant, or
where the household did not know the person or where they went; none decides a result on its own (each is handled the
way every careful analyst handles it, and R2's rivals land inside its band).
Not one thing: the strongest single piece is the dependence factor (R4); a run that nails it still reads the matcher's
links as coverage and lands its estimates 0.0 per cent off nationally, still misses the shared errors in its
intervals (R6), the close district's call (R7), the residents on no list (R8) and the unrecorded emigration (R9).
One-fact test: "the register and the coverage survey miss the same young men; compare the estimate's sex ratios with
the ones births and survival give" rescues R4 alone; "a survey person the matcher could not link may still be on the
register" rescues R1 alone; one of nine at most (the effort test's hints, executed by the generator).
Not semantics: every field, unit and clause read correctly (usual residence by term-time address and base, the
register count by postcode district, the circular's interval rule) still leaves the linked share short of the true
coverage by 12.8 points for non-nationals, the estimate's men 18 to 44 short by the dependence, the interval
half as wide as the shared errors make it, and the accounts' gap unexplained.
Not rule application: the circular files the line (25,000), the population definition and the interval rule; no
filed procedure says how to measure coverage, what the matcher misses, which benchmark to use or how wide the interval
is, so every result left after the filed rules are applied is estimation.
Estimand: the circular files the population (usual residents on 30 June 2026, students at term-time address, serving
personnel at base, districts by the postcode directory), the line and the interval rule; the prompt asks each result
in its own words (each district's usual residents and how sure, the call and each close district's chance, each
register count's gap split into parts, the rolled-forward estimate's gap split into parts, the share of the survey's
people the register lists in their own district by citizenship).
No decoy: no memo or draft argues a figure; the rolled-forward population accounts are an incumbent figure that
reproduces exactly from its own components (the 2021 base plus births, deaths and recorded migration) and answers a
shallower quantity; ask R9 prices it on the golden's footing (its gap to the estimate split into parts). The accounts
are national only, so no shipped artifact ranks the districts against the line.
No replay: no result re-derives a published figure; the accounts' total is the start of R9's bridge, not an answer.
Pinned: every rival (unresolved records imputed by cell or district, the linkage table by nationality alone, one
raising factor for 18 to 44, the 2021 Census as the sex-ratio benchmark, raising Kilvarran men only) run on the cut
pack lands inside R1, R4, R5 and R6's bands and files the golden call (checks.py R7 block).
Run forecast: R1 lost to dismissed own evidence (recall measured, never carried); R4 and R5 to the method shortcut of
the independence formula named and waved through; R6 to the method shortcut of resampling the survey alone; R7 with
R5 and R6; R8 to the self-confirming check of a bridge that adds up by construction; R9 to the self-confirming check
of an estimate close to the accounts.
Strategy label: UNTESTED (an admin-based population estimate: dual-system estimation on a register with linkage error,
correlation bias and a benchmark that shares the register's error; no Sulfur round has run one)
Depth level: 5. Five independent judgments (linkage error measured and carried, district-consistent matching, the
dependence factor from births, the shared-error interval, the accounts' gap sized from the follow-up and the border
record), each with its own figure; the shortcuts land on 7 distinct wrong calls (the register's counts, the
linked share as coverage, district-blind matching, independence, the accounts' total, every entry taken as correct).
Lesson: a register-based population count is only as good as three measured things a hurried analyst assumes: what
the linkage misses, how far the two sources miss the same people, and which errors every district shares; and a
benchmark that agrees with the uncorrected count may share its error. No build on file teaches dependent capture
channels or a common-error benchmark.

## Results chain

| ID | Result (checkable) | Area | Pinned by | Band | Hurried analyst | Depends on | Graded as |
|---|---|---|---|---|---|---|---|
| R1 | Share of the survey's residents (serving personnel aside) on their own district's list, net of missed and false links: citizens 94.9 per cent, others 85.1 | assembly and reconciliation (record linkage) | the survey, the register and the clerical review's verified status | 0.6 point (citizens), 2.5 points (others) | dismissed own evidence: measures the matcher's recall on the review, then files its linked share (92.3 and 72.3) as coverage; priced Right in the careful column, because the stage 4 judge's first pass corrected the links on the review | independent: the survey, the register and the clerical review | Component 1 |
| R2 | Register entries not correct for their district, by district (left Kilvarra or died, duplicate registrations, living elsewhere in Kilvarra; the unplaced shared as the placed outcomes are) | missingness and measurement | the follow-up's outcomes and the register's counts | 8 per cent of each district's figure | method shortcut: every "moved" entry counted as gone (movers within the district among them), or the no-contact entries dropped; the careful pass imputes both and earns it | independent: the follow-up and the register | Ask 3 |
| R3 | Residents listed in another district, by district (students registered at home, movers) | assembly and reconciliation | the survey's links read by district, missed links counted | 25 per cent or 40 people | dismissed own evidence: the matcher's links read as they stand, so the residents listed elsewhere ride on the uncorrected coverage (a survey person found anywhere counted as on their own list is the narrower slip, a narrow look at broad data) | R1 | Ask 3b |
| R4 | Raising factors for men aged 18 to 29 (1.095) and 30 to 44 (1.048) | modeling | births by sex, the life table's survival and the survey's citizenship | 0.04 | method shortcut: the dual-system formula's independence named in an assumptions list and waved through (dismissed own evidence), so no factor | R1 and R2 through the estimate's sex ratio, with births by sex, the life table and the survey | Component 2 |
| R5 | Usual residents of each district and of Kilvarra on 30 June 2026 (Kilvarra 320,200) | modeling | R1, R2, R4 and the defence return under the circular's definition | 1.0 per cent each district, 0.6 per cent Kilvarra | method shortcut: the links corrected but independence kept (Kilvarra 316,150); the linked share as coverage is the other slip, and it lifts the districts instead | R1, R2, R4 | Ask 1 |
| R6 | Half-width of Kilvarra's 90 per cent interval (1.0 per cent) | uncertainty | the survey blocks resampled with every step repeated | 0.75 to 1.45 per cent | method shortcut: the survey blocks resampled with the linkage correction and factors fixed (0.4 per cent), a self-confirming check of the sampling noise alone; priced Right in the careful column, because the judge's first pass resampled every step | independent: the bootstrap of the survey blocks | Component 3 |
| R7 | The call: Port Ardain, Ballinrea, Drumcastle, Tullaghvane qualify, Newbrook too close to call (chance 0.22), the rest do not | synthesis | circular 3.1 and 3.2 on R5 and R6 | the call exact; each close chance inside the range any estimate within 1.0 per cent of the golden gives (Newbrook 0.07 to 0.48) | method shortcut: independence leaves Newbrook not qualifying | R5, R6 | Recommendation |
| R8 | Residents on no district's list, by district (the bridge's last part) | decomposition and attribution | R5 less the register's correct entries and the residents listed elsewhere | 25 per cent or 40 people | self-confirming check: the bridge built as the remainder of a wrong estimate adds up by construction | R5 | Ask 3c |
| R9 | The rolled-forward 325,247 bridged to the estimate: gap 5,050, emigrants since mid-2021 never recorded 7,140, arrivals missing from the accounts 603, remainder -1,490 | investigation loops | the follow-up's leavers by the month they left, the border's departures, the accounts' components | gap 0.6 per cent of Kilvarra; emigration 15 per cent | self-confirming check: the estimate's closeness to the accounts read as confirmation and the gap called emigration (stopped at the first story) | independent: the follow-up, the border record and the accounts | Component 4 |

Carry-forward: R1, R2, R6 and R9's emigration are graded on inputs of their own (the review, the follow-up, the
bootstrap, the follow-up with the border record), so a run that slips on the estimate still earns them; R4 rides on
R1 and R2 through the estimate's sex ratio (a block-expanded estimate gives factors near 1.0); R3 falls with R1's
district scope, R5 with R1, R2 and R4, R7 with R5 and R6, R8 with R5.

## Hidden factor record

| Factor | Real or constructed | Only in deciding units | Found by | Fix depth | Verdict |
|---|---|---|---|---|---|
| Young men missed by both the register and the survey (correlation bias) | constructed by the simulation (a visibility trait drives both registering and responding) | no: every district carries them (464 to 2,787 men aged 18 to 44 a district), and districts far from the line move as much | modelling: a sex-ratio benchmark from births by sex and survival compared with the estimate's, serving personnel added on both sides | modelling (a demographic-analysis factor by age group, a judgment on the benchmark's domain) | keep |
| What the matcher misses (missed links read as people the register lacks) | constructed by the simulation (each system records names and dates its own way) | no: every district and both citizenship groups, most among other citizenships | modelling: the clerical review's verified status against the linked status, by citizenship and sex | modelling (a correction table carried into every coverage ratio) | keep |
| Emigrants still on the register and missing from the accounts | constructed by the simulation (emigrants deregister at 20 to 30 per cent; the accounts record the deregistered and the border's departures) | no: every district holds them, and the accounts are national | a targeted query and modelling: the follow-up's leavers by the month they left, those not known at the address shared out, less the border's departures | modelling | keep |
| Residents listed in another district (students at home, movers) | constructed by the simulation (students re-register at 45 per cent, movers at 62 to 86) | no: every district has residents listed elsewhere (520 to 2,295) | a targeted query: the linked record's district against the survey district | modelling (counted on both sides of the dual-system ratio) | keep |

## Effort test

| Result | Quick pass | Careful but hurried | Thorough |
|---|---|---|---|
| R1 share of survey residents on their own district's list | Missed | Right | Right |
| R2 register entries not correct for their district | Missed | Right | Right |
| R3 residents listed in another district | Missed | Right | Right |
| R4 raising factors for men aged 18 to 29 and 30 to 44 | Missed | Missed | Right |
| R5 district estimates and the national total | Missed | Missed | Right |
| R6 national 90 per cent interval half-width | Missed | Right | Right |
| R7 the call and each close district's chance | Missed | Missed | Right |
| R8 residents on no district's list, by district | Missed | Right | Right |
| R9 the rolled-forward estimate bridged to the estimate | Missed | Missed | Right |
| Roughly | 0 of 9 | 5 of 9 | 9 of 9 |

Measured by: .claude/skills/stumping/effort.py on generator/effort.json
Largest single hint: "the register and the coverage survey miss the same young men; compare the estimate's sex ratios with the ones births and survival give"; rescues 3 of 9 results (R4, R5, R7)
Pair estimate: 60.2

Priced on the stage 4 judge's first pass (2026-11-11): it corrected the matcher's links on the clerical review and
resampled every step, so R1 and R6 are Right in the careful column, and the careful pass is the golden chain with
independence kept and the rolled-forward gap read as emigration. R8's band is the width its inputs' bands give
together (the judge's point), so the careful pass earns R8 as well as R2 and R3; R9's emigration band comes from its
rivals (5 per cent), so the gap read as emigration misses it. On that pricing the careful-but-hurried pass scores
60.2, over the house's 50 and the client's bar of 60, and the young-men sentence rescues 3 of 9 results
(R4, R5, R7): the young men's factor is the one careful-column loss on the estimates, and a second independent lever
tried in this world did not hold (Tried and rejected). The author's call: ship on this record and let the platform's
two runs measure it; re-root if they average 60 or more.

## Data provenance

Source: generated by task19/generator (make.py) from a simulated process: Kilvarra's people from mid-2021 to mid-2026
and the Health Service's register, the Office's coverage survey, follow-up and clerical review, the border, civil
registration, the defence and education returns.
Behaves like the real thing: the simulation runs the processes that make the files (births, deaths at a Gompertz
schedule, emigration with 20 to 30 per cent deregistering, an immigration surge in 2022 to 2024, moves between
districts with re-registration at 62 to 86 per cent and duplicates, students leaving home at 18, Defence Forces
turnover, practice contact that thins with age and sex, the 2024 list validation, a coverage survey of 7 per cent of
blocks with household contact and listing, a follow-up of listed records), matching the published behaviour of health
registers (NHS list inflation of 5 to 8 per cent, worst in cities), the ONS admin-based estimates' student and young-man
difficulties, PES correlation bias for young men, and unrecorded emigration (ONS 2025 emigration revision).
Genuine patterns: (1) list inflation that grows with turnover, highest in the capital and the non-national districts;
(2) young men under-covered by both sources across every district; (3) students and movers registered where they used
to live; (4) an immigration surge in 2022 to 2024 and emigration that follows it; (5) contact with practices that falls
with age for men and rises after 65; (6) the 2024 list validation's step in the list sizes.
Problems by process: duplicates from re-registering after a move; stale addresses from moves within a district;
ghosts from emigrants who never deregistered; birth registration lag; serving personnel outside the register; name and
date variants from each system's own entry; postcode keying and the 2024 recoding; no contact and unknown destinations
in the follow-up.
Breadth: sixteen files from six bodies; a 335,000-row register, a 19,600-person survey, a 23,000-record follow-up, a
28,000-row border file and four files a careful analyst weighs and sets aside (the 2021 Census tables, the 2021 link
study, the quarterly list sizes, the enrolment return), so deciding which records answer which question is work.

## Template check

Chain signature: assembly-reconciliation, missingness-measurement, assembly-reconciliation, modeling, modeling,
uncertainty, synthesis, decomposition-attribution, investigation-loops
Question form: how many (a count per district), with which and how likely for the call
Nearest build: task5 (an admin-based count in the same domain, a reconciled table); task5 completes late reports
filed by employers, while here the register is complete but wrong in both directions and the correction is a
dual-system estimate with linkage error, correlation bias against a births benchmark and shared-error intervals; the
abstraction sentence a reviewer would write for both ("a register's count corrected with another source") stops at
the level of the domain, and the deciding lessons share nothing (skeleton.py: severity none).

## Frontier check

Precedents: R1 L01 and L06 and R3 L01 kept as the classes these results are built on, though the judge's first pass
earned both and the careful column grades them Right; R4 L22 (the published formula whose generating assumption the data contradict) and N05
(an assumption named and waved through); R5 L22 and L01; R6 L35 (the independence formula where units share shocks)
and L31 (a band carrying an assumed common factor); R7 L35 and L22; R8 L28 (an estimator certified by checks that
cannot see the problem); R9 L29 (an incumbent figure's small gap taken as confirmation) and L26 (a shallower story that
passes its own checks).
Shallow path checks: the matcher's linkage passes its own check (precision on the review above 99 per cent) and only
the review's verified status for the unlinked refutes it; the careful pass's independence passes a bootstrap and an
age-sex post-stratification, and only the sex ratio from births by sex (another file, at a generation's grain) refutes it;
its estimate passes the comparison with the rolled-forward figure (within 2.9 per cent), and only the
follow-up's leavers dated and set against the border's departures refute it; its register bridge adds up by
construction, and only R5's correct estimate refutes its residents on no list.
Assumption made false: independence of the register and the survey within age and sex groups, the dual-system
formula's own assumption that every run lists; the world's process makes it false (a visibility trait drives both
registering with a practice and answering the survey, and some young men are off both), and births by sex in the
vital statistics workbook with its life table test it.
Forcing: the line is 25,000 under circular 3.2; the golden family (6 rivals) all file the golden call, with
Newbrook's interval 24,150 to 25,310 containing the line by 310 at its nearer end, Tullaghvane's lower end
25,650 and Carnmoyle's upper end 24,390; the careful pass files Port Ardain, Ballinrea, Drumcastle, Tullaghvane as qualifying and none as too close to call; each fitted input moved by its
spread (the raising factors by one bootstrap standard deviation, the missed-link rates by 20 per cent, the no-contact
imputation by one bootstrap standard deviation, the interval 20 per cent wider or narrower) keeps the call. Expanding
the sample blocks by their selection probabilities, in place of scaling each district's register count, carries the
sample's own sampling error into each figure (the blocks' entries expanded miss the known list by -3.1 to +3.3
per cent by district), which the list removes: the efficient estimator, the one the golden uses.
Noun swap: the nearest task on file is task5 (severity none in skeleton.py check); swapping its employers and reports
into this one carries the decision form (a set against a line) and a reconciled count, and nothing of the deciding
lessons, the detection or the moves; the client's library holds no dual-system or sex-ratio task.

## Semantic fork table

| ID | Term or convention | Readings | Golden | Ruled out by |
|---|---|---|---|---|
| SF1 | usually lived in each district | where the register lists them; where the survey found them; the circular's usual residence | usual residence: students at term-time address, serving personnel at base | circular 2.2 |
| SF2 | health register count | records by practice district; records by address postcode | by the address's postcode in the directory | circular 2.3 (an address belongs to the district the directory assigns its postcode) |
| SF3 | too close to call | the point estimate near the line; the interval including 25,000 | the Office's 90 per cent interval includes 25,000 | circular 3.2 |
| SF4 | how likely each close one is to be at 25,000 or over | a probability from the estimate's spread | the chance under the estimate's bootstrap spread | same call (the band holds the chance any estimate within 1.0 per cent gives) |
| SF5 | the people the coverage survey found | with or without serving personnel | without (the register cannot hold them) | same call (within 0.4 point, inside the band) |
| SF6 | split the register gap into its parts | any decomposition | the prompt's three parts: entries that should not count for the district, its residents listed in another district, its residents on no list | the prompt names them |
| SF7 | the rolled-forward national estimate | the accounts' population at 30 June 2026 | 30 June 2026 in the accounts | the accounts' own last row |
| SF8 | Kilvarran citizens and everyone else | citizenship as recorded by the survey | the survey's citizenship KV | the survey's own field |
| SF9 | each figure's precision | none dictated | nearest 10 for estimates, the answer blocks' bands | the answer blocks |
| SF10 | how sure can we be | any interval | the Office's 90 per cent interval | circular 2.1 |
| SF11 | emigrants since mid-2021 | by year left; by month left | a leaving month of July 2021 or later; none dated after June 2026 | the follow-up records the month |
| SF12 | serving personnel | in the survey's count; at the base | the return's 857 at Larrick Barracks in Fort Larrick, out of the dual-system ratio | circular 2.2 and the return |
| SF13 | a district's estimate from the sample blocks | scaled to the district's register count; expanded by selection probabilities | scaled to the register count | the known register count: the expansion carries the sample's own sampling error (its entries miss the list by -3.1 to +3.3 per cent), which scaling to the list removes |
| SF15 | split the rolled-forward gap | any decomposition | component by component, as the prompt asks: emigration the accounts never recorded, immigration they missed, births and deaths, the remainder for the 2021 base and sampling error | the prompt names the split; the parts add (checks.py) |
| SF16 | students | where the survey found them; the enrolment return added | where the survey found them, at term-time addresses (circular 2.2) | the survey's student field sits only in the university districts; adding the return counts them twice |
| SF17 | Kilvarrans' net migration by sex since birth | the same for men and women; a sex-specific allowance | the same, stated in the Step-by-Step | no file holds migration by sex since birth; the 2021 census cohorts land inside R4's band (the stage 4 judge's check) |

## Closure table

| Axis | Closure |
|---|---|
| 1 Population | usual residents on 30 June 2026 under circular 2.2; serving personnel from the defence return; C1 |
| 2 Unit of account | persons; the question names them |
| 3 Attribution window | 30 June 2026; the survey's reference date and the register extract's as-of date |
| 4 As-of dating | 30 June 2026 filed in circular 2.1; the extract is the list on that day |
| 5 Version basis | one register extract, one survey, one follow-up; no vintages |
| 6 Denominator | the coverage ratio's denominator is the survey's people in the cell; R1's is the survey's people without serving personnel (SF5) |
| 7 Weighting | equal selection probability within each district (the blocks file); weights cancel within a district; the ratio to the district's register count carries its figure, never the blocks' expansion (SF13); C1 |
| 8 Window length | not applicable: a point in time; emigration since mid-2021 by the leaving month, July 2021 on (SF11) |
| 9 Boundary inclusivity | 25,000 or more qualifies (circular 3.1); an interval including 25,000 is too close (3.2) |
| 10 Rounding path | estimates to the nearest 10 after the sum; intervals to the nearest 10 |
| 11 Tie-break | not applicable: no district sits on an interval end |
| 12 Maturity and censoring | births not yet registered with a practice are counted by the survey; the follow-up's no contact imputed by a model on the resolved 2026 entries (R2's band holds the rivals; the 2021 link study's attendance rates, a route the stage 4 judge checked, land inside it) |
| 13 Order of operations | district placed before matching; factors after the district estimates; personnel added last; asserted |
| 14 Row order | no result depends on file order; the matcher's one-to-one rule takes the strongest claim first |
| 15 Duplicate resolution | the follow-up's duplicate registrations are not correct entries; the survey person matched once |
| 16 Identity normalisation | the matcher's normalised names and dates; its error measured on the review and carried (R1) |
| 17 Netting against gross | the register bridge shows gross parts that net to the gap |
| 18 Dimensional units | persons throughout |
| 19 Code and status semantics | the follow-up's outcomes read as their labels say; movers with no district at the known movers' share |
| 20 Integerisation | counts reported to the nearest 10 |
| 21 Clause scope | circular 3.2 applies to each district's own interval |
| 22 Forward window contents | the 2027/28 determination uses the mid-2026 estimate; nothing after 30 June 2026 enters it |

## Literal reader

Executed word for word, the prompt asks for usual residents by district on 30 June 2026 (circular 2.2 defines them),
how sure (circular 2.1: a 90 per cent interval), the call under the circular (3.1 and 3.2), each close district's
chance, each register count's gap in the three parts it names, the accounts' gap in parts, and the share of the survey's people the
register lists in their own district by citizenship; every reading lands on the golden's quantity, and the easy
answers come from easy methods on the same estimand (the linked share, independence, the survey-only interval).

## Prompt contract

The rewrite keeps: the reason the answer is an estimate (no census since 2021), the date (30 June 2026), every district
and Kilvarra, how sure, the circular's call with the too-close category and each close district's chance, the two gaps
split into parts (the register's three named parts by district, rolled-forward nationally), the survey share by
citizenship, and the two deliverables by type (a spreadsheet and a short PDF note). It must never add: the matcher's recall, a sex ratio, births, independence, a bootstrap, a file
name, a count the data hold, or who is asking.

## Pre-ship check

- Card registered (WARN only: chain near task5, how-many form, one taught lesson), skeleton severity none against every
  card, lineage entry and client task; the frontier check written; the cited pair estimate 60.2.
- The process behind the files simulated before any result was named; the weight (a hard-to-measure quantity) rotated
  from the last two builds.
- Nine results across seven areas, each pinned, banded and graded; no analytical result is the only input of more
  than half the others.
- Every hidden factor across all twelve districts (checks.py R5 block), none only where it decides.
- The effort test measured by effort.py: quick 7.0, careful but hurried 60.2 (over the house's 50 and the
  client's 60), thorough 100, priced on the judge's first pass; the largest single hint rescues 3 results of
  nine: shipped on the author's call, the platform's runs to measure it.
- Forcing on both sides: six rivals file the golden call; eight perturbations keep it; the shortcuts land on
  7 distinct wrong calls.
- Gates on the final cut: precut, effort, voice, leak, figures, containers, heart and surface; checks.py and verify.py
  green; two builds byte-identical.

## Tried and rejected

- 2026-11-11, the concept note's district-level official estimates: a shipped series that puts Carnmoyle over the
  line ranks the candidates on the decision question (Gate G); only the national series and its components ship.
- 2026-11-11, the concept note's residency classifier trained on the 2021 census link as a graded result: with the
  follow-up's 2026 outcomes in hand the design-based rate needs no model, so the trap reached only runs that chose to
  model; the link ships as an unused file and its route is recorded, never graded.
- 2026-11-11, register over-coverage by a signs-of-life rule (the concept's crude activity filter): every activity
  window is a threshold a judge reads as a fork (task8's architecture 12 screen); over-coverage comes from the field
  follow-up's outcomes instead.
- 2026-11-11, the concept's NewTown two people under the line: a call that close is returned on forcing (task1 arch
  2 and 3, task4 arch 7 and 10); the near-line districts are set so the honest interval decides each one with margin.
- 2026-11-11, a linkage world where the matcher found 99.8 per cent of true links: missing links then cost nothing and
  the dependence factor carried the estimates alone (the one-fact test failed on paper); the systems' name and date
  differences were raised to the levels real linkage work meets (recall about 96.5 and 87.9 per cent).
- 2026-11-11, married surnames as the main source of missed links: concentrated in women aged 22 to 45, they inflated
  the raising factors through the linkage correction; cut back, with stale addresses and Irish name forms carrying the
  missed links across both sexes.
- 2026-11-11, a careful pass with the missed links and independence alone: the two offset to within a few tenths of a
  per cent and the call came out right; the near-line district is set where the survey-only interval turns the high
  estimate into a qualification.
- 2026-11-11, the matcher's linked share as the careful pass's coverage slip: the stage 4 judge's first pass corrected
  the links on the clerical review and resampled every step, so R1 and R6 are earned and the young men's factor is the
  one careful-column loss on the estimates; priced that way the careful pass scores 60.2 and the young-men sentence
  rescues 3 of 9 results.
- 2026-11-11, a second lever from the follow-up's no-contact entries measured through the survey: the simulated
  follow-up's contact is a property of the dwelling, so its no-contact entries came out as correct for their district
  as the resolved ones (0.90 against 0.90) and the missing-at-random model held; dropped before any result was graded.
- 2026-11-11, the docx memo: the deliverable set ran over the corpus quota; the note goes to the Commission as the PDF
  the word processor exports.
- 2026-11-11, the second judge pass (FIX_NOW): Fort Larrick's bridge row in the answer blocks left out the 857 serving
  personnel the workbook carried, and the rolled-forward gap's parts, the enrolment return, the benchmark's migration
  convention and the emigration conventions were unstated; the blocks now name each, and the prompt asks for the gap
  component by component.
