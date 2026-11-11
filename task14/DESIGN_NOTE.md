# task14: what Penmarra's bond-based measure of private rents will show for the year to the December 2026 quarter

Architecture 3, re-rooted on 2026-11-11 at the author's word in a new world, dataset and shell, and strengthened at
stage 3 the same day (`## Tried and rejected`, last lines). Architecture 1 (Marrowfield's conflict-of-interest docket)
was returned by the platform's checks on 2026-11-10; architecture 2 (the same world's coverage statement) was set aside
before any data was cut. Every figure below is the cut pack's, from `generator/figures.json` and `generator/effort.json`.

## Draw

Subdomain: Survey Research & Official Statistics, Seasonal adjustment & official time-series production
Analysis type: Data Extraction & Conformation (ETL / Pipeline Build)
Answer shape: a forecast path with bands, plus its drivers: the new measure's quarterly path from March 2022 to
  September 2026 conformed from the Tenancy Bond Board's register and completed from the Statistics Office's rent
  panel, carried to the December 2026 quarter with its range, and its drivers (continuing tenancies and re-lettings)
  adding to the September figure and to its change since September 2025
Weight: measurement: the register records a tenancy's rent when it starts and its rises only when a landlord chooses to
  lodge more bond, so most of the work is measuring what the register does not record: the rises small landlords never
  lodged (from a panel that holds none of the operators' blocks), the operators' reviews that their complete records
  carry, the rent each earlier tenancy was paying when its dwelling was re-let, found across the March 2023 migration,
  and the reviews and re-lettings that will land after the extract closed. The last three live builds sit on modeling
  (task1), allocation (task9 v9) and assembly (task16 v2)
Data-native sentence: the bond register records a tenancy's rent when it starts and, only when a landlord chooses to
  lodge more bond, when it rises, so the rents payable on dwellings already let have to be rebuilt from a survey panel
  drawn before the build-to-rent blocks existed and from those operators' own complete top-ups, every re-letting priced
  against what the tenancy before it was paying across a 2023 migration that left the longest tenancies without a
  property identifier, and December carried from an extract that closes before one operator's review and halfway
  through the lodging of another's.
People: Christine Buckley (manager, prices statistics, Penmarra Statistics Office) and Kim Chandler (data and systems
  lead, Tenancy Bond Board), from `guard.py names --geo "New Zealand" --seed 14` (Nigel Walsh set aside: first name in
  mark111). Neither appears in the prompt.
Decision: the December 2026 quarter's annual change on the new measure, nationally and by region, with which the office
  launches the measure on 27 January 2027; forward-facing (the quarter closes on 31 December, the register extract at
  the close of 27 November 2026). The September 2026 figures, the back series, the counts, the group changes and the
  split of the slowdown are results beside the call.

Card: `.claude/skills/fingerprint/cards/task14.json`, architecture v3, registered 2026-11-11 at PASS (weight
measurement, answer shape a forecast path with bands and drivers, G13 first with G3 and G12, calibration
parallel-run overlap, forum the line manager, launch as the forcing event). The decisive generator was redrawn from G3
to G13 (horizon mismatch) at READY, when task9's re-draw moved task18 (G3) into this card's window; the call turns on
carrying the register past its extract, and a differentiation line answers task8's architecture 13. The subdomain is official time-series production
because the deliverable is a new official quarterly series with its back series and next quarter; the register work
serves it. The prompt's shell is drawn with the world (what, a spreadsheet and a few slides); voice-check warns that a
spreadsheet with slides sits at 24 per cent of prompts on file against a 20 per cent quota (a launch briefing is
slides, the release tables a workbook).

## Deep reasoning

Task type: seasonal-adjustment-official-time-series-production (Survey Research & Official Statistics), serving Data
  Extraction & Conformation: a new official quarterly series compiled from an administrative register conformed
  across a system migration and completed from a survey panel, with its back series and its next quarter.
Domain test: every result is a quantity a statistics office's prices division produces when an administrative source
  replaces a survey: the register conformed to the measure's units (tenancies, dwellings, regions), the completeness
  of the register's optional change records measured against a survey panel and carried to the register's own mix of
  landlords, a matched-dwelling ratio of totals with its breakdowns and their contributions, and the next quarter
  projected from the reviews, endings and re-lettings the record schedules, with a range from the sampled input and
  the projection's own record.
Swap: "the total weekly pay employees receive rose 4.0 per cent, re-hires 9.4 and stayers 2.5" read off a payroll
  register stops making sense at once: a payroll register records every pay change, so there is no optional record
  whose completeness needs a panel, no employer class whose records are complete while others' are not, no migration
  that left the longest-held units without a key, and no portfolio review scheduled after the extract.
Where the weight sits: measuring what the register does not record: the rises small landlords never lodged, from a rent
  panel drawn at the end of 2017 that holds none of the operators' blocks, against the operators' reviews that their
  own bonds record in full; the work is long because three sources describe the same rents from different ends (the
  register at entry and by choice, the operators completely, the panel quarterly for a sample), and the December
  quarter adds two reviews the extract does not yet show in full.
Layer 1: two register schemas (the legacy system's free-text addresses, landlord numbers and rents with a frequency;
  the online system's property identifiers, re-keyed landlords and weekly rents) joined at the March 2023 migration;
  transfers and changes of parties as events on one bond; re-sent legacy lodgements; rents keyed with an extra zero;
  refunds and lodgements days to weeks after the events they record; the July 2024 regions with three old areas split
  between two; panel non-response, vacancies and replacements. None decides a result on its own: each is a step a
  careful run takes by reflex, and the assembly results grade them.
Not one thing: four judgments each move the September measure and none is enough alone: the unlodged rises (reading
  the additional bonds as every rise files 4.2), the operators' complete records against the panel's coverage (the
  survey's rises given to every landlord file 3.7), the size of the rises the bonds do record (carrying the latest
  recorded rent forward at the survey's rate files a back series up to 0.3 point high and a re-letting rise of 8.6),
  and the migrated bonds tied by address (property identifiers alone file 2.8); December needs two more on top (the
  review not yet on file and the half-lodged one, and the December re-lettings the extract cannot show), and the
  range a sixth.
One-fact test: "project December from what the register showed at the same point of earlier years, operators'
  scheduled reviews included" rescues R6, R7 and R7b on the careful pass and nothing in September; "the rent panel
  holds none of the operators' dwellings, and their additional bonds record every review" rescues R3 and R5; for a run
  that reads the additional bonds as every rise, "small landlords lodge additional bond for only some of their rises"
  rescues R3, R4 and R5 if it leads to rates carried from each starting rent and R3 alone if it leads to recorded
  rents carried forward, and never R8 or a December result; three results of nine at most (agrees with the Effort
  test's Largest single hint).
Not semantics: every field, code and clause read correctly (the event types, the frequencies, the regions, the methods
  paper's let-on-a-day and rent-payable definitions) still leaves the property-identifier links, the lodged rents, the
  survey given to every landlord and the register read as it stands each filing a different wrong measure.
Not rule application: the methods paper files what the measure is (whose rent, which days, which dwellings, the
  ratio, the breakdowns, the regions); no filed rule says where the rent payable on a day comes from when the
  register holds only the starting rent, how a re-letting finds the tenancy before it, what an operator's review
  will be, how December will look, or how sure the figure is. Executing every filed definition on the register's own
  recorded rents gives 4.2 for September and, read on 31 December as it stands, 2.7 for December, not the golden.
Estimand: the methods paper 2.1 to 2.7 (the dwelling; a tenancy runs from its start until the day before its bond is
  refunded or the next tenancy starts; let on a day; rent payable as the agreement stands, weekly; the measure as the
  ratio of the matched dwellings' totals on the quarters' last days, less one; the breakdowns for dwellings let to the
  same tenancy and dwellings re-let, each computed the same way; the 2024 regions by suburb; bonded private tenancies
  only); the prompt fixes the quarters (March 2022 to September 2026, and December 2026), the 30 September 2026
  count, the year to September 2026 for the group changes, the move from the September figure to the December one
  for the split, and the national December figure's 90 per cent range.
No decoy: no memo, draft or stakeholder figure; the survey-based series is the Office's own published series for the
  measure it replaces and no result reads it; the CPI release is read for the operators' reviews; the house price
  index and the building consents are distractors no result reads.
No replay: no result re-derives a published figure; every graded figure is computed from the register, the panel and
  the CPI release.
Pinned: each result's rivals are run on the clean pack in the generator and land inside its band (checks.py): the
  premises matched without the slip and reversal allowances, the panel's rates unweighted and pooled across regions,
  December's rates read with hindsight, without landlord class or from two years only, going rents held at November,
  and the range from the panel's error alone, the two errors added, a t multiplier for three back-test years or the
  back-test's bias removed. The rent estimators are ranked by the data: on the 2,841 small-landlord tenancies both
  sources held on the survey's August 2026 reference day, rents carried from each starting rent come within 0.2 per
  cent of the rents the survey reports (likewise in 2024 and 2025), recorded rents carried forward overshoot by 0.9,
  recorded rents wherever a bond exists fall 1.4 short and the recorded rents alone 5.4; and the panel tied to the
  register by address shows anniversaries with an additional bond rising more, and without one less, than the
  survey's average in every year from 2022 to 2025. The December shortcuts are ranked by back-tests on December 2023
  to 2025 from the register as it stood: the projection missed by 0.1 point or less, a straight trend by up to 0.2,
  the 27 November reading plus the earlier years' change to December by up to 0.24, and the register read as it stands
  fell short by 0.59 to 0.75, of which the December re-lettings were 0.24 to 0.39 against 0.08 in 2026, when about
  1,190 tenancies ending in the last five weeks re-let at going rents 2.8 per cent above the rents they replace against
  10.1 and 8.1 per cent in 2024 and 2025 (checks.py).
Run forecast: a strong run loses R2 by a narrow look at broad data (property identifiers alone), R3 by dismissed own
  evidence or a method shortcut (lodged rises read as every rise, or the panel's rises given to the operators), R4 by
  a method shortcut (the earlier starting rent, or recorded rents carried forward), R5 by an unfinished chain (a stock
  on the shortcuts above), R6 by a self-confirming check (the panel resampled around an unprojected figure), R7 and
  R7b by a method shortcut (September carried forward, a straight trend, or the register read as it stands), R8 by an
  unfinished chain (the split on a December read off the register as it stands); R1 is earned.
Strategy label: WORKS IN FORM (heterogeneity that pooling hides, rebuilt from the register's landlord portfolios;
  outcomes not yet recorded measured on a validation panel; a forecast whose deciding configuration, the review
  schedule, is in the record), from references/sulfur-strategies.md.
Depth level: 5 on the client's scale: six independent judgments each move a graded figure (the unlodged rises, the
  operators' complete records against the panel's coverage, the recorded rises' size, the migrated bonds tied by
  address, the reviews not yet on file, the December re-lettings), and twelve shortcuts land on ten different wrong
  December figures (2.4 to 5.1 against the golden's 3.1).
Lesson: a stock measure read from an administrative register has to be completed where the register's change records
  are optional, with the completeness measured on a panel that never covered part of the stock and the recorded
  changes known to be the larger ones, every unit that changed hands priced against what its previous occupant was
  really paying across whatever key change separates them, and the next quarter carried from the schedule the record
  itself shows; no build on file builds a matched-unit measure from entry and optional change records.

## Results chain

| ID | Result (checkable) | Area | Pinned by | Band | Hurried analyst | Depends on | Graded as |
|---|---|---|---|---|---|---|---|
| R1 | bonded tenancies in place on 30 September 2026, by region and nationally (68,993) | Assembly and reconciliation | methods paper 2.1, 2.2 and 2.6 (a tenancy runs from its start until its bond is refunded or the next tenancy starts; the 2024 regions by suburb); one tenancy across transfers and changes of parties; re-sent legacy rows dropped | within 0.3 per cent of each count | narrow look at broad data on the quick pass (bonds lodged and not refunded by 30 September, missing those lodged after); the careful pass is right | independent: the two register extracts | Ask 2 |
| R2 | dwellings re-let in the year to 30 September 2026 (let on both days under different tenancies), by region and nationally (14,963) | Assembly and reconciliation (record linkage) | methods paper 2.4 and 2.5; each later tenancy tied to the one before it at the same dwelling, by property identifier where both carry one and by the parsed address where the earlier bond was migrated in March 2023 | within 2 per cent of each count | narrow look at broad data: dwellings joined on the property identifier alone (9,978), so re-lettings whose earlier tenancy was migrated without one fall out; identical address strings alone find 13,054 | independent: the two register extracts | Ask 3 |
| R3 | tenancies that continued through the year to 30 September 2026: the change in their total weekly rent (2.5 per cent) and the share whose rent rose (62.4 per cent) | Missingness and measurement | methods paper 2.3 (rent payable as the agreement stands) and 2.5; the rent panel's continuing tenancies show the rises small landlords never lodged; the operators' additional bonds record every review | change within 0.15 point; share within 2.0 points | dismissed own evidence: the additional bonds read as every rise (1.6 per cent, 20.6 per cent rising) beside a panel where about three in five rose; or a method shortcut: the panel's rises given to the operators' blocks it never held (2.1 per cent, 59.0 per cent) | independent: the register's additional bonds and the rent panel | Component 2 |
| R4 | the change at re-letting: the re-let dwellings' total weekly rent on 30 September 2026 against the earlier tenancies' total on 30 September 2025 (9.4 per cent) | Missingness and measurement | methods paper 2.4 (each tenancy at its rent payable on its own day) and 2.5 | within 0.5 point | method shortcut: the earlier tenancy's starting rent, counting its own rises a second time (17.6), or its latest recorded rent carried forward at the panel's rate, which adds the average rise on top of the larger rises the bonds record (8.6) | R2 | Ask 5 |
| R5 | the measure: the national annual change for every quarter from March 2022 to September 2026 (4.0 to September 2026, a peak of 7.5 in 2023Q4) and the September 2026 figure for each region | Synthesis | methods paper 2.4 and 2.6 on R1 to R4 | each quarter within 0.3 point; September 2026 within 0.15 nationally and 0.25 by region | unfinished chain: a stock built on the property-identifier links (2.8), the lodged rents (4.2) or the panel's rises given to every landlord (3.7, with Hallam Central and Hallam East out of band) | R2, R3, R4 | Component 1 |
| R7 | the national annual change for the year to the December 2026 quarter (3.1 per cent) | Forecasting | methods paper 2.4 at 31 December; the extract to 27 November: Quayside's 1 November review on the bonds lodged so far, Harbourline's 1 December review from its rule in its own earlier bonds and the September 2026 CPI, endings and re-lettings at the rates the same weeks of 2023 to 2025 showed as the register then stood, going rents from the register's repeat-letting index | within 0.1 point | method shortcut: September carried forward (4.0), a straight trend through the quarters (3.5), the register read as it stands on 31 December (2.7), that reading corrected by its own past errors (3.4), or the 27 November reading plus earlier years' change to December (3.6) | R3, R5 | Recommendation |
| R7b | the annual change for the year to the December 2026 quarter in each region | Forecasting | as R7, region by region (2.6) | within 0.2 point | method shortcut: as R7; the panel's rises given to every landlord with the register read as it stands leaves Hallam Central, Hallam East and Kerrow Coast out of band | R3, R5 | Ask 7 |
| R6 | the 90 per cent range on the national December 2026 figure (3.0 to 3.2, a half-width of 0.09) | Uncertainty | the panel is the only sampled input: its dwellings resampled within their strata (400 draws), the rates re-estimated and December recomputed; the same projection run at 27 November of 2023, 2024 and 2025 against the measure those Decembers gave | each end within 0.1 point; half-width 0.05 to 0.2 | self-confirming check: the panel resampled around the register read as it stands (2.9 to 3.0), or a straight trend's own prediction interval | R7 | Ask 7 |
| R8 | the move from the September figure to the December one split between continuing tenancies and re-lettings (a fall of 0.89 points: 0.43 and 0.46) | Decomposition and attribution | each group's contribution to the measure (its change in rent over the whole base), which adds to the measure in each year (2.4, 2.5): September's from the register, December's expected from the projection | each group within 0.1 point; the fall within 0.12 | unfinished chain: the split on a December read off the register as it stands, or carried in proportion to September's shares when December is a trend or September carried forward | R3, R7 | Component 3 |

Carry-forward: R1, R2 and R3 are graded on the shipped files alone (R2 and R3 name their own inputs); R4 falls with R2;
R5 with R2 to R4; R6 with R7; R7 and R7b with R3 and R5 and the review schedule; R8 with R3 and R7. No analytical
result is the only analytical input of more than three others (R3 of R5, R7, R7b and R8 through R5), and a run that
slips at one step keeps what it did right elsewhere: the careful pass keeps R1, R2 and R4 while missing R3.

## Hidden factor record

| Factor | Real or constructed | Only in deciding units | Found by | Fix depth | Verdict |
|---|---|---|---|---|---|
| small landlords lodge additional bond for a minority of rises, more often for large ones and when an agent manages | constructed (the simulated landlords' choices) | no: every small-landlord and company tenancy in every region (under a third rise on their bonds in each region, asserted), and every quarter of the back series | a targeted comparison across two files: the register's additional bonds against the panel's observed rises, or the panel linked to the register by address | modelling: the unlodged rises estimated from the panel by year and region and carried from each tenancy's starting rent, with their sampling error into the range | keep |
| the operators' reviews (Harbourline every 1 December at the September CPI plus a point, Quayside every 1 November at the September CPI plus half a point) recorded in full; the student operator re-lets every February | constructed (the operators' leases) | no: five of seven regions and the national figure, every year since 2020; the student blocks move re-lettings and nothing else | a targeted query: landlord portfolios rebuilt across the re-keyed identifiers, their additional bonds' effective dates, and their rises against the CPI release | modelling: each landlord class's rents from its own source, the review rule read off three earlier reviews | keep |
| Quayside lodges its review bonds over about six weeks and Harbourline reviews after the extract closes | constructed (the operators' back offices and calendars) | no: every Quayside tenancy reviewed in each of 2023 to 2025 shows the same lodging lag, and every December projection back-tested meets it | a targeted query: the operator bonds' effective dates against their lodgement dates, by year | modelling: the projection completes the review on file in part and applies the one due from its rule | keep |
| the active bonds migrated in March 2023 kept their free-text addresses and no property identifier | constructed (the system migration) | no: every region, every tenancy older than March 2023, and every quarter of the back series | a targeted query: re-lettings with no earlier tenancy, by when the dwelling's previous bond began | modelling: address parsing and matching, the dwelling's history rebuilt | keep |
| sitting tenants' rents fall behind the going rent, so the rise at re-letting grows with the earlier tenancy's length | constructed (the simulated reviews against the market path) | no: every re-letting in every region | modelling: the earlier tenancy's paying rent rebuilt from its start and its rises | modelling | keep |
| going rents turned down from mid-2026 after the boom | constructed (the simulated market) | no: every region, every new letting from mid-2026 (their annual growth fell from about 2 per cent in the three months to July to under 1 in the three months to November on the regions' average, and fell in six of seven regions; asserted) | a targeted query: new lettings' rents by month in the register | modelling: carried into December's re-lettings | keep, R7 among several inputs |

## Effort test

| Result | Quick pass | Careful but hurried | Thorough |
|---|---|---|---|
| R1 bonded tenancies held on 30 September 2026 | Missed | Right | Right |
| R2 dwellings re-let in the year | Missed | Right | Right |
| R3 continuing tenancies' change and share | Missed | Missed | Right |
| R4 the change at re-letting | Missed | Right | Right |
| R5 the measure and its back series | Missed | Partly | Right |
| R7 the national December 2026 figure | Missed | Missed | Right |
| R7b the regional December 2026 figures | Missed | Partly | Right |
| R6 the December range | Missed | Missed | Right |
| R8 the split of the slowdown | Missed | Missed | Right |
| Roughly | 0 of 9 | 4 of 9 | 9 of 9 |

Measured by: .claude/skills/stumping/effort.py on generator/effort.json (the passes are the generator's own
implementations: the quick pass's new-letting rents on property-identifier links; the careful pass graded up, with the
premises parsed and matched, a rise model fitted on the panel, the earlier tenancy's paying rent, December read off the
register as it stands on 31 December and a range from the panel resampled, in three variants of the rent step, the best
of them (the panel's rises given to every landlord, 49.5; recorded rents carried forward 37.0; recorded rent where a
bond exists 37.0) taken; and the golden)
Largest single hint: project December from what the register showed at the same point of earlier years, operators'
  scheduled reviews included; rescues 3 of 9 results (the operators' sentence 2 of 9; for a run reading the bonds as
  every rise, the unlodged-rises sentence 3 of 9 at most)
Pair estimate: 49.5 (the careful pass earns R1, R2 and R4, half of R5 and R7b, and the instruction-following share)

## Data provenance

Source: generated by task14/generator from a simulated rental market (seed 1407): 47,500 small-landlord dwellings in
  2008 and those entering since, three operators' blocks opened 2019 to 2025 (Harbourline 5,600 dwellings, Quayside
  4,920, the student operator 1,950 rooms), every tenancy with its rent at the start, its rises and its end, the
  Tenancy Bond Board's lodgements, additional bonds, transfers, changes of parties and refunds, the March 2023
  migration, the Statistics Office's rent panel drawn at the end of 2017, and the CPI release.
Behaves like the real thing: tenancies end most often at the fixed term's twelfth month and then at a lower monthly
  rate, as bond data on tenancy lengths show; small landlords raise rents at some anniversaries by amounts that track
  the trailing letting market and round to five or ten dollars, while operators review whole portfolios on fixed dates
  by a CPI-linked formula and lodge the bonds over the following weeks; additional bond is optional, so the register
  records rises unevenly and the large ones more often; a re-letting resets the rent to the going level, so catch-up
  grows with tenancy length; a system migration that carries active records without the new key is the common way
  registers change hands; bonds are lodged within the 23 working days the law allows and refunded days to weeks after
  a tenancy ends.
Genuine patterns: (1) seasonality of lettings, with January and February peaks and the student blocks' February
  re-lets (2) a boom from 2021 to 2024 and a slowdown since, larger in the capital's districts (3) tenancy lengths with
  the fixed-term spike and regional turnover differences (4) rent rises tracking the trailing market with landlord
  heterogeneity and rounding (5) a portfolio structure of one-dwelling landlords, property companies and operators,
  the operators' CPI-linked reviews running ahead of small landlords' rises as inflation outpaced the market in 2025
  (6) dwellings entering and leaving the rental market
Problems by process: the March 2023 migration (migrated bonds without property identifiers, landlords re-keyed with a
  crosswalk for those active then); free-text addresses typed by different landlords and agents; re-sent legacy
  lodgements; rents keyed with an extra zero; weekly, fortnightly and monthly rents; lodgements and refunds days to
  weeks after the events they record, so the extract's last weeks are incomplete; an operator's review bonds lodged
  over six weeks; the July 2024 regions with three old areas split; tenancies let with no bond; panel non-response,
  vacancies and replacements from the 2017 frame.
Breadth: two register extracts of about 487,000 events between them over about 83,000 dwellings, seven regions,
  nineteen graded quarters, about 3,300 panel dwellings over 35 quarters, and twelve files of which three are
  distractors (the survey-based series, the house price index, the building consents), so deciding which records and
  which file answer each result is work.

## Template check

Chain signature: assembly-reconciliation, assembly-reconciliation, missingness-measurement, missingness-measurement,
  synthesis, uncertainty, forecasting, forecasting, decomposition-attribution
Question form: what (what the new measure will show for the year to the December 2026 quarter)
Nearest build: task16 v2 (assembly weight, a reconciled table, contacts linked across four channels to a season's
  rate) and task5 (an administrative census completed early, report by report); neither builds a matched-unit measure
  from entry and optional change records, completes it from a panel that never covered part of the stock, or projects
  it through reviews not yet on file. Abstraction sentence (this build against its nearest): none writable; task16
  links one customer's contacts to estimate a rate, task5 completes late reports, and this build completes the changes
  an optional record missed and prices every changed unit against its previous occupant's real amount.

## Semantic fork table

| ID | Term or convention | Readings | Golden | Ruled out by |
|---|---|---|---|---|
| SF1 | which tenancies are in the measure | bonded private tenancies; every rental | bonded private tenancies | methods paper 2.7 |
| SF2 | the quarter's day | the quarter's last day; an average over the quarter; the survey's mid-quarter day | the last day | methods paper 2.4 |
| SF3 | rent | rent payable as the agreement stands; the register's last recorded rent | rent payable as the agreement stands | methods paper 2.3 |
| SF4 | weekly conversion | fortnightly halved and monthly times 12/52; monthly times 3/13 or divided by 4.33 | 12/52 | methods paper 2.3 |
| SF5 | which dwellings compare | let on both days; let on either day | let on both days | methods paper 2.4 |
| SF6 | a dwelling with a refund pending when the next tenancy starts | the later tenancy; both | the later tenancy | methods paper 2.2 |
| SF7 | when a tenancy ends | the day before its refund, or before the next tenancy starts; the lodgement of the next | refund or next start, whichever comes first | methods paper 2.2 |
| SF8 | a re-let dwelling's earlier rent | what the earlier tenancy was paying on the earlier day; its starting rent | what it was paying | methods paper 2.4 |
| SF9 | regions before July 2024 | the 2024 regions by suburb; the old rental areas | the 2024 regions by suburb | methods paper 2.6 and the concordance |
| SF10 | the national figure | the ratio of all matched dwellings' totals; an average of the regions | the ratio of totals | methods paper 2.4 and 2.6 |
| SF11 | a room let under its own agreement | a dwelling; part of one | a dwelling | methods paper 2.1 |
| SF12 | a transfer or change of parties | the same tenancy; a new one | the same tenancy | same call: the online system records both as events on one bond and the legacy system on one bond number |
| SF13 | the share of continuing tenancies whose rent rose | a count of tenancies; a rent-weighted share | a count | the prompt's "share of continuing tenancies" |
| SF14 | how much rents changed for each group | the group's ratio of totals; an average of each dwelling's change | the ratio of totals | methods paper 2.5 (each breakdown computed the same way as the measure) |
| SF15 | the dwellings re-let in the year | let on both days under different tenancies; every new tenancy at a dwelling let before | let on both days | methods paper 2.5 |
| SF16 | tenancies in place on 30 September 2026 | in place under 2.2 (the later tenancy where two would cover the day); every bond the Board holds that day; lodged by that day | in place under 2.2 | the prompt's "in place" and 2.2's "the tenancy in place" |
| SF17 | the 90 per cent range | the December estimate's uncertainty from its sampled input and from its projection; the register resampled as if a sample; a trend's prediction interval | the panel's sampling error with the projection's own back-test error | the register holds every bonded tenancy (2.7), so its only sampled input is the panel, and the December figure is a projection whose error on earlier Decembers the register measures |
| SF18 | how many points of the move from the September figure to the December one each group accounts for | each group's change in contribution (its change in rent over the whole base), the two adding to the move; each group's rate change alone with the mix left over | the change in contribution | the prompt's "each account for": two parts that add to the move; the contributions add to the measure in each year (asserted) |
| SF20 | a dwelling | the unit a bond is lodged for, by its property identifier where the bond has one and its parsed address otherwise; the address string alone | the property identifier, then the parsed address | same call: no online address carries two property identifiers, so the two readings name the same dwellings (asserted) |
| SF19 | the December quarter's figure | 31 December 2026 against 31 December 2025 as the full register will give it; the extract's last day against the same day a year earlier | 31 December | methods paper 2.4 (the last day of the quarter) |

## Closure table

| Axis | Closure |
|---|---|
| 1 | Population: bonded private tenancies (2.7), dwellings let on both days (2.4); C1 for unbonded tenancies (never on the register) |
| 2 | Unit of account: the dwelling (2.1), rooms let separately included; one tenancy per bond |
| 3 | Attribution window: a quarter is its last day (2.4); rises dated by the agreement (an additional bond's effective date where the form gives one), not by when they were lodged |
| 4 | As-of dating: the register as extracted at the close of 27 November 2026; the panel to the September 2026 quarter; the CPI release to the September 2026 quarter, out on 21 October |
| 5 | Version basis: one register as extracted, no revisions; the legacy extract holds every bond held on or after 1 January 2019 |
| 6 | Denominator: the earlier day's total rent payable over the same dwellings (2.4) |
| 7 | Weighting: rent-weighted by construction (a ratio of totals, 2.4); the national is not a weighted mean of regions (2.6) |
| 8 | Window length: a year between the two days (2.4) |
| 9 | Boundary inclusivity: a tenancy covers its start date and runs to the day before its refund or the next start (2.2) |
| 10 | Rounding path: rents converted to weekly at full precision, totals summed, the ratio rounded once to 0.1 point; contributions to 0.01 point and the split taken from them |
| 11 | Tie-break: two bonds covering one day resolve to the later tenancy (2.2) |
| 12 | Maturity and censoring: lodgements for tenancies covering 30 September 2026 are complete in the extract (23 working days allowed, 58 days elapsed); the extract's last weeks are incomplete, and December is projected from what the register showed at the same point of earlier years, not read as it stands |
| 13 | Order of operations: conform, link, price each tenancy on its day, then sum; the ratio is of sums |
| 14 | Row order: no step depends on file order; events dated |
| 15 | Duplicate resolution: re-sent legacy lodgements are exact copies, kept once |
| 16 | Identity normalisation: property identifiers where both tenancies carry one, else the address parsed to unit, number, street and suburb; landlords through the crosswalk |
| 17 | Netting against gross: rents fall as well as rise at re-letting; nothing is floored |
| 18 | Dimensional units: weekly dollars throughout (2.3); per cent for the measure; points for contributions |
| 19 | Code and status semantics: event, frequency and response codes from the code lists, which map codes and say nothing about them |
| 20 | Integerisation: counts whole; rents in cents after conversion |
| 21 | Clause scope: 2.4 applies to each region and to the nation alike; 2.5 to each breakdown |
| 22 | Forward window contents: the extract's events to 27 November 2026, the operators' review days and rules in their own earlier bonds, and the September 2026 CPI drive December; nothing else is needed |

## Literal reader

Executing the prompt and methods paper 2.1 to 2.7 word for word: the measure's dwellings are those let on both
quarter-end days (2.2, 2.4); each tenancy's rent payable on its day is the agreement as it stands (2.3), which the
register states at lodgement and at each additional bond and the panel states quarterly for its dwellings; the ratio of
the totals less one is the figure (2.4), by region on the 2024 regions (2.6) and nationally; each group's change is its
own ratio (2.5) and its contribution its change over the whole base. A reader who takes the register's last recorded
rent for the rent payable files 4.2 per cent for September 2026, against 2.3's "as it stands" once the panel shows rents
rising with nothing lodged; a reader who keeps only the property-identifier links files 2.8, against 2.4's dwellings let
on both days; a reader who reads December off the register as it stands files 2.7, against 2.4's last day of a quarter
the extract ends five weeks short of. None is another reading: each is an easier method on the same filed estimand.

## Prompt contract

A voice rewrite keeps: the question (what the bond-based measure will show for the year to the December 2026 quarter,
nationally and in each region, and how sure we can be of the national figure); the national measure for every quarter
from March 2022 to September 2026 and the September 2026 figure for each region; the bonded tenancies held on 30
September 2026 (in place, as the prompt says) and the dwellings re-let in the year to then, by region; for that year
how much rents changed at re-letting and for tenancies that continued, with the share of continuing tenancies whose rent
rose; the December figures with a 90 per cent range on the national one, and how many points of the move from the
September figure to the December one continuing tenancies and re-lettings each account for; a spreadsheet and a few
slides. It never adds a rounding instruction, a method (no linking,
matching, imputing, panel, top-ups, additional bonds, migration, catch-up, reviews, operators, CPI, trend, back-test or
bootstrap), a warning, an attached file's name, a role, or a count the data hold.

## Leak and judge rulings

Mechanical sweep (leak.py, 2026-11-11): REVIEW, no LEAK. Ruled in the main thread:
- Stump vocabulary in the methods paper (earlier, survey, tenancy, regions, office, lodged): harmless; the paper defines the measure in its own words and names the Rent Survey once as the source of the index the measure replaces, which no result reads.
- Answer figures in the methods paper (2.5 and 2.7) and the bond events file (11,239): harmless; two are the paper's section numbers and the third is a date beside a rent across a field boundary.
- metadata.json covers wording: harmless; the file sits outside target/ and describes what each file holds.
- Reader (one isolated Sonnet read, 2026-11-11): nothing planted quoted for question 1 (the methods paper's filed estimand), no ranking or helper file, every literal sentence executes to the golden's estimand; its question 6 (the methods paper as a full specification) is overruled by measurement, since the definitions executed on the recorded rents file 4.2 and 2.7.
- Reader's realism note on dates after the session's date: by design (a forward setting, the launch on 27 January 2027); the container band accepts it.
- Second reader (after the prompt changed): no method in the prompt, nothing planted; question 6 overruled by measurement as before; its realism notes on bonds at exactly four weeks' rent and repeated suburb endings fixed in the generator.
- Judge pass 2's open items, ruled in the main thread: the December band stays at 0.1 point, the analogs (3.4 to 3.8) being ruled out by named data (their back-tests on three earlier Decembers, up to 0.24 against the projection's 0.1, and the re-letting margin measured at 2.8 per cent against 10.1 and 8.1), the build's main residual risk; R8 is rescued by no single sentence (computed: it needs the September engine and the December projection together); the published survey index's 4.0 for September 2026 matches the golden on that one cell by coincidence, its peak (6.8) and its 2022 to 2024 quarters missing; the workbook's routes sheet stays (the house's submission rules ask for it and the client's reviewers praised one).

## Tried and rejected

- Architecture 1 stage-4 reader, first pass: the realism tells it listed (arithmetic disclosed amounts, a uniform cohort, the region's employee-number block, coded product names, one address, unmatched therapeutic areas, submissions on the 59th second) fixed in the generator and asserted.
- **Reader, re-centred design (pass 2):** no sentence quoted for question 1; nothing ranks the candidates; question 5 quoted policy 5.4 and executed it over its own candidates (a person-level median ratio with a $1,000 floor came closest of its six); question 6 named an analytical choice. It filed the whole-year docket (the five censored histories in place of the five December filers), so the call held. It landed all three asks (A's sixteen departments through the NPI link, B through the profile file, C by checking the list's companies against the register by name): the fix pass re-rooted B and C and folded A into two counts (## Ask sheet, ## Tried and rejected). Its realism tells (blank namesake addresses, a block of reissued employee numbers, formulaic company names) were answered: namesake profiles now carry their own cities' addresses; reissued numbers in one block and invented company names are what the systems and the fiction produce.
- **Judge (pass 2, the one re-judge):** DETERMINISTIC, FIX_NOW: step 3's "comes closest" false for the golden's own form (averaged faculty-wide ratios come closer, same fifteen) and the sixteenth a near tie that moves with the ratio's form. Both fixed in the generator: step 3 and the memo restated (ratio of sums, closest whole-number weighting, closer forms naming the same fifteen, all asserted); the sixteenth dropped from the prompt and the chart's value labels removed. Gate G PASS (method_or_model_selection, analytical_non_defect); Gate H domain, layers and decisive step pass; stump power rated strong.
- **Reader, after the fix pass (pass 3, the prompt having changed):** question 1 quoted policy 5.4 and 5.3 as the nearest sentences and found they file a selection criterion with no candidate estimator (harmless: the criterion is the filed organ, the reference window is named nowhere); question 2 none; question 3 named the field definitions, the export contents, the department codes, the profiles, the entity list and the form guide (the systems' own files and keys, harmless) and the two distractors as unused; question 4 none; question 5 executed 5.1 to 5.4 over its own candidates and committed to the closest of them, a person-level median ratio shrunk at eight lines with every disclosure read as its whole year, which on its own conformance differs from 2025 by 738,880 against the golden's 523,143, and no construction closer than the golden files another docket (asserted), so the sentence executes to the golden once the aligned estimate is among the candidates; question 6 an analytical choice. The call: thirteen of the fifteen, two December filers (Pedro Hampton, Judith Valenzuela) left off for two censored histories (Angelica Gentry, Hector Mahoney), so the stump held. The asks: A landed (1,696 and 91); B missed four natures (it saw the 24 NPI-less profiles at the campus addresses and left them unresolved); C landed every type, the renamed company tied by hand from the earlier items, and its total summed from the rounded rows (167 against 166). Realism tells answered: the office's matcher column wrong for the namesakes is what a name-based routine produces (Layer 1, never the call, SF10); round register amounts and exact ratios come from round honoraria and faculty who round to $500 or $1,000; invented company names (H21); one publication date per refresh; one hospital address per department; the reorganisation on the fiscal year's first day; every return resubmitted within days, before the pull. Two were fixed in the generator: the namesakes' practice addresses now run over ten streets, and the NIH file lost the NPI column RePORTER does not carry. Ambiguities answered: A's 180 and 234 are the UTC-midnight and latest-version readings the Eastern deadline and "submitted" close; B's 31 December reading is closed by the prompt's "appointments in 2025"; C's two companies are closed by the register's 2025 records and the type definition's "when it added it", royalties by policy 2.1, and on-time filers by "faculty disclosed".
- Per-payment omission with relationships that persist year to year (scratch simulation at the draw): the additive correction (the disclosure plus the record's average undisclosed dollars) won the back-test, because the record's level predicted the year better than the disclosure did; relationships that start and end within a few years make the year's disclosure the timely signal, and the credibility-weighted correction then wins.
- Five comparison-year omitters (simulation and first build): the overall-share corrections came within 4 per cent of face value on 2025, so the default path's choice of face value was a coin flip; eight omitters and seven long-record under-reporters in 2025 put the next-best default correction 1.26 times face value.
- Ask A's primary carried by faculty amendments alone moved 5 of 16 departments: the office's review after the deadline now returns disclosures for correction in every department, and the export's latest submission time moves all 16.
- Ask B's namesake records missed one nature and Ask C's renamed-manufacturer lines missed expert testimony and other paid services: namesake records now reach every nature in 2025, and expert-testimony and other-services relationships with renamed manufacturers are typed under their former names.
- A docket-region override set every forced relationship's 2026 line to the member's amount, giving each under-reporter five identical $40,300 lines: only the large relationship now carries it.
- Docket-region names drawn from the roster's pools repeated first names (Cristina, Shannon) and carried surnames used by older builds: the region's 52 names are fixed in world.py, none used by an earlier build.
- data_dictionary and export_manifest file names (69 and 43 earlier builds): renamed to the office's own oricoi_field_definitions.xlsx and oricoi_export_contents_2027-01-21.csv.
- The first design's decisive conjunction (the matched-line grain and a credibility weighting, every disclosure read as its whole year): the stage-4 leak reader, reading blind, built the matched-line ratio shrunk toward the faculty's by $10,000 to $20,000 of record and filed the golden docket at once, the judge rated the stump moderate, and the grain was readable from policy 5.3 ("each manufacturer named in the faculty member's annual disclosure"); the decisive step moved to the disclosures' reference window, the weighting kept as a supporting rung.
- A composite of the corrected disclosure with last year's register amount as the decisive move (stage 4, on paper): it cannot tell a December filer's partial year from a relationship that shrank, and last year's register alone rescued the members it was meant to; the reference window separates them because the submission day and the payment calendar are in the files.
- Ask A's primary carried by the export's latest submission time: the reader took the history's first submission and every department's count landed; the primary is now the employee numbers changed in 2026, joined only through the NPI, the latest submission time kept as a hazard.
- Ask C's primary carried by manufacturers typed under former names: the reader resolved them through the register's earlier names and every type landed; the primary is now the two listed companies that began reporting for 2025, the former names kept as a hazard.
- A field definition saying a blank identifier marks "a company that does not report to Open Payments": it would have filed Ask C's careful reading as the rule; the definition now says what the office recorded and when.
- A long-term-relationship tail on the background faculty with the cap on a relationship's payments raised to $45,000 (fix pass, scratch): background members reached the top fifteen under several near-optimal constructions and one construction filing another docket came 0.945 times the golden on 2025; the cap went back to $22,000 and twelve ordinary large faithful disclosers sit below the docket instead.
- Ask A as a sixteen-department table (stage 4, pass 2): the blind reader linked the reissued employee numbers through the NPI and landed all sixteen rows; the device is kept and the ask folded into the two counts it moves, so it carries two criteria instead of thirty-two.
- Ask B's primary carried by the office's matcher and blank record NPIs (pass 2): the reader tied records through the profile file's NPIs and landed every nature; the primary is now the NPI-less duplicate profiles, which the profile join drops and a name-only repair over-fills.
- Ask C's primary carried by two listed companies under their own names (pass 2): the reader checked the list's companies without an identifier against the register by name and landed every type; one of the two is now renamed (its present name on the list, its former name in the register's 2025 records), and only the earlier items under the same list entry tie them.
- The entity list's type definition ("as the office classed the company when it added it") as a neutral line (pass 2): the reader used it as evidence that the classification is dated, but without it a literal judge takes the list's "Other company" as the answer to Ask C (391,500 in the judge's pass); kept, since the renamed company's tie still has to be found in the earlier items.
- A robust sixteenth (judge pass 2 found it a near tie among the censored histories, $51,112 against $50,859 and $50,329, moving with how the ratios are formed): a long-standing faithful January filer placed at about $57,000 was the sixteenth under every construction closer than the golden, but under the faculty-wide December share five fully aligned constructions within 3.5 per cent of the golden on 2025 put it on the docket in place of a December filer; the sixteenth left the prompt, the chart carries no value labels, and the member sits below the cut.
- Step 3's "comes closest" (judge pass 2): the golden's ratio of summed amounts is the closest of its own weightings, not of every form of the estimate (averaged ratios come closer); the write-up and the memo now state the ratio of sums, call n/(n+2) the closest whole-number weighting (asserted from 1 to 20), and say the forms that come closer name the same fifteen (asserted over every construction).
- Total rows under the nature and relationship-type tables (pass 3): not asked by the prompt, and a reader summed the rounded rows (167 against the rounded total 166); the total rows left the memo and block 4.
- 2026-10-31, reship under the learning loop's rules: the office's field definitions and export contents list withdrawn (renaming them from data_dictionary and export_manifest had only dodged the name check; a shipped file may not describe the data); every convention they carried is the guide's (version in force, relationship types by edition) or the data's own columns. The metadata's subdomain, which named the record-check correction, and the prompt's count of the docket's places (the policy files fifteen) were removed, and the prompt opens on who goes on the docket.
- Architecture 1 as a whole (a docket of fifteen under the policy's threshold, each member's 2026 remuneration estimated ahead of publication by reading every disclosure to the day it was filed; asks: a count of filers against the deadline and two tabulations): returned by the platform on 2026-11-10 before any run was reported. Domain fit: "entirely about applying stated policy rules ... compliance lookups, counts, and certified figures under a stated rule", with no estimation, modeling or uncertainty; the prompt test read the tables' breakdowns, the year range and the two sources to compare as method spelled out and the deliverables as a roll call (runs/review_2026-11-10.md). One deep step also decided the docket, the shape the project lead's review of 2026-11-09 sends back. The world is kept; the question moves to estimation about the registry itself.
- A provisional estimate of what Open Payments will publish for 2026, the part the disclosures miss completed line by line (understated, paid after filing, left off, not filed) and by department, with a replay on 2025 (architecture 2, first sketch, prototyped in memory on 2026-11-10): under a stationary reporting process last year's proportions carry every university-wide line inside any honest range, so only the department cells and the range priced anything, and the chain repeated task5's (an early estimate completed component by component, a set of areas, a replay as the records stood).
- The same statement with a stratified documentation audit of 230 disclosures for the companies outside Open Payments (prototype, eight seeds): the weighted estimate ran from 0.6 to 1.5 times the truth, because most of what is left off sits with faculty who name nothing and fall in the thin stratum, so the necessary corrections (weights, audit nonresponse) were smaller than the estimator's own noise and no band could separate them.
- Pure inverse-rate weighting of every uploaded outside form, named or not (prototype, twelve seeds): department cells went negative where a department's named relationships had no form uploaded, and a pooled upload rate did as well as one by named status; carrying the named relationships from the disclosures themselves and weighting only the forms of companies left off cut the noise and made the rate by named status necessary (the pooled rate then reads 0.6 to 0.7 of the truth).
- Architecture 2 (Marrowfield University Health's 2025 coverage statement: manufacturers checked against Open Payments, companies outside it estimated from the tax forms faculty uploaded, the forms' completeness measured on the manufacturer side), drawn 2026-11-10 and set aside on 2026-11-11 before any data was cut, at the author's word: the author ruled task6 the only build at the bar and asked for a far stronger chain with at least three independent analytical failure points, not task6's strategy and harder than it. Its prototype's chain leaned on one capture rate with two corrections around it, and the world was the one architecture 1 had spent, so the slot moved to a new world, dataset and shell (architecture 3).
- Draw screens, 2026-11-11 (architecture 3), each set aside before a card: a labour force survey's web-first redesign bridged across rotation groups (the mode effect against the first-interview bias, regional mode effects, the variance of the change from the overlap), because it walks the client atlas's own staggered-instrument bridge and overlapping-survey scorecard and would read as a reskin; a register-based census corrected by an address sample (one strong judgment, the informative non-contacts, with the stratified ratio a reflex and linkage errors cancelling in each municipality's net); a VAT-for-survey source replacement (the conformance errors move growth only around turning points, too little to separate shortcuts); a business survey's late returns and dead units (task5's ground); a scanner-data price index (domain fit read as price theory, chain drift one enumerable switch, as task8's slot found).
- The architecture 3 first cut, measured at stage 3 (2026-11-11): a careful pass graded up (premises parsed and matched, the survey's rises given to every landlord, December read off the register as it stands) earned about 60, because the operators' July review moved September and December by under 0.2 point, the projection added only 0.1 over the register as it stood, and neither the September interval nor the survey bridge separated any shortcut. Strengthened in the world, not the bands: the operators given blocks in five regions from 2019, Harbourline's review moved to 1 December at the September CPI plus a point (after the extract closes), Quayside's review bonds lodged over six weeks, December's rates read as the register stood at each earlier cut, and two results replaced (below). The careful variants then scored 49.5, 37.0 and 33.0.
- The September interval as a result (first cut's R6): the panel resampled put it at 0.05 to 0.06 point, inside any band a shortcut could also reach; the range moved to December, where the projection's own error on earlier Decembers is part of it.
- The bridge from the survey-based figure (first cut's R8): its parts sat within the survey's own sampling noise; replaced by the split of the change since September 2025 between continuing tenancies and re-lettings.
- The regional December figures inside the recommendation's cells (stage 3): a careful pass with every region inside 0.3 point earned half the recommendation while missing the national figure; the regions became their own ask (R7b) at 0.2 point, the pooled rates' widest departure being 0.17.
- The back series graded apart from the September regions (stage 3): one hint (the operators' records) then rescued four of ten results on the careful pass; the Measure sheet is one table and is graded as one result (R5).
- Determinism judge, pass 1 (2026-11-11, NOT_DETERMINISTIC, FIX_NOW): (1) the rent estimators unranked by independent data: ranked now on the dwellings both sources hold (rents carried from each starting rent within 0.2 per cent of the survey's reported rents, the rivals 0.9 to 5.5 away) and by the panel tied to the register; (2) dwelling identity: operator blocks wrapped unit numbers past sixty a floor, so 418 addresses carried two property identifiers; fixed in the world (no address now carries two), and "held" became "in place" in the prompt, 2.2's own words; (3) December's shortcuts rejected by argument: ranked now by back-tests on three earlier Decembers; (4) the one-fact test from a run reading the bonds as every rise (four of nine with the split since September 2025): the split moved to the forecast's own drivers (September to December by group), so no sentence rescues more than three.
- Determinism judge, pass 2 (2026-11-11, DETERMINISTIC, FIX_NOW, solution only): counts, group figures and September reproduced independently; three fixes applied without touching the pack or the prompt: the back series' band widened to 0.3 point (a survey-to-register ratio correction by tenancy age lands up to 0.3 off in four quarters), the December figure's re-letting term sized in the steps (about 1,190 December re-lettings at a 2.8 per cent margin against 10.1 and 8.1 in 2024 and 2025) with the judge's own analog (the 27 November reading plus earlier years' change, 3.6) back-tested at up to 0.24 against the projection's 0.1, and the continuing share's construction stated; the December band kept at 0.1 point.
