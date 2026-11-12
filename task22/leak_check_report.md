# leak check, task22

**Verdict: REVIEW.** 22 files read, 58 golden figures and 1 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: missed, delivery, network, fourteen, breaker, switching, transformer, careful, method, residual, result, connections, substation, device, dismissed, evidence, shortcut, utility, positions, factor, applied, rebuilt, record, deemed, budget

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `cwp_2027-2028_approved_projects_excerpt.pdf`: golden figure 0.6 appears: ...ghway 60 business park lots; no load before 2028 0.6 November 2027 390,000 In-service dates are the da...

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `fy2027_budget_instructions_electric_fund.pdf`: 4 of 25 stump-paragraph terms appear (connections, substation, utility, budget); read whether the document names the move
- **REVIEW** `loss_evaluation_study_2019_hester.pdf`: 8 of 25 stump-paragraph terms appear (fourteen, breaker, transformer, method, result, substation); read whether the document names the move
- **REVIEW** `rfp_2026-14_revenue_protection_scope.pdf`: 5 of 25 stump-paragraph terms appear (breaker, transformer, connections, substation, record); read whether the document names the move

## 8 column names (REVIEW 2)
- **REVIEW** `oms_gis_device_crosswalk_2024-07.xlsx`: columns a generator names and an organisation does not: OMS_Device
- **REVIEW** `oms_switching_orders_2023-09_2026-10.csv`: columns a generator names and an organisation does not: Device

## 9 dates after the setting (INFO 1)
- **INFO** `-`: no --asof given, sweep skipped (pass the fiction's as-of date)

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 12 client quality check (INFO 2)
- **INFO** `-`: 22 usable files (10 or more required)
- **INFO** `-`: 2 file categories: document, spreadsheet (2 or more required)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 11 prompt gate (clean)


## Solver's-eye read

### First read (isolated, medium effort, on the cut of 2026-11-12 before the stage 4 fixes)

#### 1. Which sentence or file tells you how any part of the analysis should be done?

Three filed documents state process, not just fact:

- `rfp_2026-14_revenue_protection_scope.pdf`, A.2: "The City will name the four feeders that carried the largest
  non-technical loss in the twelve months ending September 30, 2026, and the contractor's 2027 inspections will
  cover every service on those four feeders." This pins the window and the count, but both already match
  `prompt.txt` word for word ("in the twelve months to September 2026 ... the sweep covers four"), so it adds no
  window or count the prompt did not already give.
- `rfp_2026-14_revenue_protection_scope.pdf`, A.3: "Non-technical loss on a feeder is the energy that entered the
  feeder, at its substation breaker and from customers' own generation, and was neither recorded by a customer's
  meter, used by the City's unmetered street and area lights, nor lost in the feeder's own conductors, transformers
  and secondary and service conductors." This is a literal subtraction formula for the target quantity (see Q5).
- `fy2027_budget_instructions_electric_fund.pdf`, section 2: "Add only new connections that hold an approved
  service application, from their scheduled service dates, and only works in the approved Construction Work Plan,
  from their in-service dates. Make no adjustment for weather." This fixes the population and timing for every 2027
  figure (large connections, CWP-driven loss changes) and rules out one rival method (weather normalization) for
  that figure.
- `loss_evaluation_study_2019_hester.pdf`, section 2 (Method), gives the full technical-loss procedure verbatim:
  the Buller and Woodrow loss-factor relation, the single-phase-tap doubling rule, transformer no-load/load-loss
  table lookups, and "Secondary and service conductor losses are taken as 0.7 percent of the energy delivered to
  services." This is the field's named method for one of the five asked-for figures (2027 technical losses), not a
  shortcut invented for this task.

#### 2. Which file already ranks or scores the candidates (the feeders) on the prompt's question?

None of the 22 files ranks or scores feeders by energy lost to theft, tampering or unmetered use. The closest
adjacent material: `annual_line_loss_report_2019-2026.xlsx` gives system-wide purchased/billed MWh and line-loss
percent only (no feeder breakdown); `cwp_2027-2028_approved_projects_excerpt.pdf` lists capital projects by feeder
but ranks them by nothing related to loss; `oms_outage_events_2023-09_2026-10.csv` could be grouped by feeder for
outage counts, but that is a reliability tally the solver would have to build, not a given score, and it answers a
different question (reliability, not theft/diversion).

#### 3. Which file exists only to help the analyst, rather than being a record the organisation keeps for its own use?

None identified. All 22 files read as records a city electric utility and its contractors would actually keep: rate
filings, an RFP, a finance-department budget memo (addressed "To: Utility Director and division managers. From:
Director of Finance", i.e. written for the City's own process, not for the solver), a capital-plan excerpt, GIS and
asset-register extracts, CIS meter reads, SCADA/historian data, OMS outage and switching logs, a lighting inventory
and billing extract, and a 2019 outside consultant's engineering report. No glossary, readme, or "how to use this
data" file is present.

#### 4. Which figure or name reads as the answer rather than context?

Nothing reads as a direct answer. `annual_line_loss_report_2019-2026.xlsx`'s two rows, `'12 months to September
2024'` (236,225 purchased MWh, 217,918 billed MWh, 7.75 percent) and `'12 months to September 2026'` (250,312, 229,724,
8.22 percent), are the system-wide premise behind the prompt's "line loss has climbed from 7.8 to 8.2 per cent," not
a per-feeder figure and not the decomposition the prompt asks for. No file names a feeder as "the" answer. The
nearest thing to a name-level signal is structural rather than declarative: see Q6.

#### 5. Which filed sentence, read literally, fixes how any requested figure is computed or over which population?

- `rfp_2026-14_revenue_protection_scope.pdf`, A.3 (quoted in Q1). Read literally, it says the "energy in" side of a
  feeder's balance must include energy received from customers' own generation, not only the substation breaker, and
  that non-technical loss is whatever is left after metered consumption, City lighting and technical losses are all
  removed from that total, i.e. a closed four-term accounting identity with no other category. In words: a feeder
  with net-metered solar customers must have their self-generation added into the "energy in" side or it will show
  up as phantom non-technical loss. The pack carries exactly this population: `cis_meter_reads_2023-08-01_2026-11-01.csv`
  has a populated `RegisterRcv`/`kWhRcv` pair on about 19,700 of its rows, all on rate codes RS and RS-E.
- `fy2027_budget_instructions_electric_fund.pdf`, section 2 (quoted in Q1). Read literally, it says: for any 2027
  figure, count a large-load application only if its status is "Approved" and only from its scheduled service date;
  count a CWP project only if it is in the approved plan and only from its in-service date. In words: of the 15 rows
  in `large_load_service_applications_2019-2027.xlsx`, only the 3 with Status "Approved" (service dates in 2027)
  belong in the "peak hourly demand each approved 2027 large connection will add" population; withdrawn and
  already-energized rows do not.

#### 6. Is there one thing that would make most of the prompt routine? Part-by-part classification

**The closest candidate.** `gis_electric_network_2026-10-27.xlsx`, sheet "Service points", column `MeterType`,
splits cleanly by feeder: APT-4, CHL-2 and CHL-3 are 100 percent `AMR` (old one-way meters) and every other
feeder (including all large-power accounts) is 100 percent `AMI`. `cwp_2027-2028_approved_projects_excerpt.pdf`'s
project CWP-27-09 is "AMI meter deployment, third phase (meters only)" naming exactly those same three feeders
(APT-4, CHL-2, CHL-3). One group-by of one column in one file, cross-confirmed by one line of a second file,
isolates 3 of the system's 14 feeders as the ones still on meters with no remote tamper/reverse-flow detection,
which is the standard reason undetected diversion persists longest. Noticing it would settle a strong prior on 3 of
the 4 names in "the sweep covers four" without touching the energy balance at all; it settles nothing about the 4th
name, none of the magnitudes, and none of the other four asks. I judge it a partial, not a full, shortcut: it
reaches only the single most visible sub-result (which feeders), not the spreadsheet, the decomposition, the demand
addition or the technical-loss figures, and it is corroborated by two independently-motivated real records rather
than being an unexplained planted split.

Part by part:
- **Rank the feeders / name the four**: mostly turns on analysis (the full monthly balance across all 14 feeders is
  what actually produces defensible magnitudes and a real ranking), but the identity of 3 of the 4 names leans on
  reading one code (`MeterType`) correctly, cross-checked against one capital-plan line, more than on finishing the
  balance.
- **Monthly energy balance spreadsheet, October 2023 to September 2026**: turns on analysis. It requires
  reconciling records at different grains and from different systems (substation-level wholesale delivery in
  `bmpa_delivery_point_interval...csv`, feeder-share allocation from `historian_feeder_breakers_hourly...csv`,
  billed consumption net of self-generation from `cis_meter_reads...csv`, deemed lighting load from
  `unmetered_lighting_billing...csv`, and a technical-loss recompute). No file hands over this spreadsheet or a
  shortcut to it.
- **Points of the rise (Sept 2024 to Sept 2026) by technical loss, non-technical loss, everything else**: turns on
  analysis (a decomposition/attribution result). The only given numbers are the two endpoint percentages
  (`annual_line_loss_report_2019-2026.xlsx`), which is the premise, not the breakdown.
- **Peak hourly demand each approved 2027 large connection will add**: the population turns on reading one field
  correctly (`Status` = "Approved" in `large_load_service_applications_2019-2027.xlsx`, per the budget
  instruction's stated rule); the demand figure itself turns on analysis, since `Connected_kW` is a simple sum of
  `Lighting_kW` + `HVAC_kW` + `Process_kW` (nameplate), not a coincident peak-hour figure by itself.
- **Each feeder's 2027 technical losses**: turns on following a stated, named procedure (the Hester study's method),
  applied to current inputs (the 2026 GIS extract, current transformer vintages, and the CWP-driven conductor
  change on APT-3 from its March 15, 2027 in-service date). The method is the field's textbook method, so the
  genuine work is in updating the inputs correctly, not in discovering the method.
- **One-page PDF memo naming the four**: a deliverable format carrying the first result forward, not a separate
  analytical turn.

#### 7. Realism

No generated-rather-than-issued tell found. PDF metadata is varied and internally consistent: every PDF was
produced by LibreOffice Writer, with a distinct Producer version per era and a creation timestamp that matches the
document's own stated date, e.g. `cwp_2027-2028_approved_projects_excerpt.pdf` has `CreationDate: Wed Sep 16
2026 11:05:00 EDT` against a document that reads "Approved by the Delmont Utilities Board on September 15, 2026";
`loss_evaluation_study_2019_hester.pdf` has `CreationDate: Fri Dec 13 2019` against "Final report, December 13,
2019" and `Producer: LibreOffice 6.3`, the correct vintage for that date, versus `Producer: LibreOffice 26.8.2.2` on
the 2026 documents. Workbook `creator`/`lastModifiedBy` properties vary sensibly by department (Utilities Finance,
Electric Engineering, GIS Services, Customer Engineering, Systems Integration, Electric Distribution, Substations,
Asset Management), with no hidden sheets and no defined names in any workbook. No file reads as written for an
exercise, and no readme or notes file explains the pack.

One minor, non-material continuity wrinkle: in `large_load_service_applications_2019-2027.xlsx`, the three 2026
rows use a clean sequential suffix (`LL-2026-01`, `LL-2026-02`, `LL-2026-03`) while every earlier year's `AppNo` is
an unordered three-digit number (e.g. `LL-2025-584`, `LL-2025-645`, `LL-2025-979`). Harmless on its own; flagged only
because it is the one spot where the numbering pattern changes.

#### Flagged files

- **`cwp_2027-2028_approved_projects_excerpt.pdf` (a number in it also appears in the answer key): harmless.** I
  traced every number in the file. The one that is genuinely load-bearing, the "9.8" miles on project CWP-27-03, is
  an intentional cross-check: the 17 GIS segment IDs the row lists sum to 51,795 ft = 9.81 miles in
  `gis_electric_network_2026-10-27.xlsx`, so it is designed to be verified, not copied as an output. The remaining
  numbers (2,380,000; 214,000; 1,105,000; 1,640,000; 390,000; 0.6 miles) are capital-cost dollar estimates and a
  second mileage figure, explicitly labelled "Estimates are 2026 dollars", a different unit domain from every
  requested figure (MWh, kWh, kW, percentage points). A shared digit string against the answer key is most likely
  an incidental collision from generation rather than a planted cue, since nothing in the document invites reading
  a construction-cost dollar figure as an energy or demand number. Worth a direct diff against `submission.md` to
  be certain, especially if the matching value sits next to one of the four correct feeder names, but nothing in
  the content itself hands over a result.
- **`oms_gis_device_crosswalk_2024-07.xlsx` and `oms_switching_orders_2023-09_2026-10.csv` (a column name):
  harmless.** The crosswalk's `OMS_Device` and the orders' `Device` name the same pre-cutover tag convention
  (`N1 664` style); the data shows a real integration cutover, the first GIS-style `SW-` value in switching orders
  is dated 2024-08-07, just after the crosswalk's own `Mapped` date of 2024-07-12, after which orders record the
  GIS `SwitchID` directly. I checked whether the crosswalk is even needed: all 36 of its rows reproduce exactly from
  `gis_electric_network_2026-10-27.xlsx`'s own "Switches" sheet (`PoleTag` to `SwitchID`, hyphen in place of the
  crosswalk's space) with zero mismatches, and 5 further OMS-style device tags used in switching orders but absent
  from the crosswalk resolve the same way. This is ordinary systems-integration mess requiring reconciliation for a
  secondary step (attributing a temporary or permanent feeder reconfiguration, confirmed present in the switching
  log under `Reason` values "Construction" and "Reconfiguration"), not a planted shortcut to the ranking.
- **`large_load_service_applications_2019-2027.xlsx` (dates after the pack's as-of date of 2026-11-05):
  harmless.** The filename itself already spans "2019-2027"; the three rows with dates past that line all carry
  `Status` "Approved" with a 2027 `ServiceDate`, exactly the population the prompt asks for ("each approved 2027
  large connection"), and the pending transformers are written as plain-text siting notes ("(new 1500 kVA at
  N707183)") rather than formal asset IDs, consistent with equipment that is approved but not yet built. This mirrors
  the same forward-dated pattern in `cwp_2027-2028_approved_projects_excerpt.pdf` (approved September 2026, in
  service across 2027). No other file's own data runs past 2026-11-05.

### Main thread rulings on the REVIEW lines

- Sweep 3, `cwp_2027-2028_approved_projects_excerpt.pdf`, 0.6: harmless. It is the IND-1 tap's length in miles; the
  answer key's 0.6 is a band width in per cent on R1. Different quantities.
- Sweep 4, `fy2027_budget_instructions_electric_fund.pdf`: harmless. It files the base year, what 2027 adds and the
  purchased power basis (the estimand of R8, SF16 to SF18) and names no step: no gap filling, network replay, loss
  computation or demand measurement.
- Sweep 4, `loss_evaluation_study_2019_hester.pdf`: harmless. The consultant's 2019 report states its own method and
  conventions (which pin SF7 to SF9) and its standard limitations line (the results rest on 2019's GIS, peak and load
  factors); it says nothing about 2026 or how to update it. It is the incumbent figure the careful pass carries, the
  assumption named and waved through and testable from the GIS and the reads.
- Sweep 4, `rfp_2026-14_revenue_protection_scope.pdf`: harmless. A.2 and A.3 file the estimand (window, count and
  definition); their literal reading is the golden (SF1, SF2, SF19). Both readers reached the same reading.
- Sweep 8, `Device` and `OMS_Device`: harmless. The OMS's own name for the switch an order operates; "device" is house
  vocabulary only. Both readers ruled it harmless.
- Sweep 9, the applications' 2027 dates: harmless. The approved connections' scheduled service dates, forward-looking
  records on the allow-list.

### Dispositions of the first read's findings

- Question 6, the meter split: fixed in the generator. The three feeders with no AMI were three of the four the sweep
  covers and the CWP's third phase named the same three; CHL-3 moved into the May 2026 phase with NTH-4 and APT-3 and
  IND-3 was left for the third phase, so the meters still on AMR are APT-4 and CHL-2 (in every route's four) and IND-3
  (seventh), and the split says nothing about the contested places.
- Question 7, the application numbers: fixed. Every year's numbers are three-digit and run in the order received.
- The crosswalk recoverable from the GIS pole tags: harmless, two routes to one mapping as an integration cutover
  leaves them; the design note no longer claims re-stencilled tags.
- Questions 1 and 5: the RFP's A.3 and the budget instructions' section 2 file what each figure is, not how it is
  computed; their literal readings are the golden.

### Second read (isolated, medium effort, on the final cut after the stage 4 fixes)

#### 1. Sentences or files that tell you how a part of the analysis should be done

- `rfp_2026-14_revenue_protection_scope.pdf`, Attachment A.2: "The City will name the four feeders that carried the largest non-technical loss in the twelve months ending September 30, 2026, and the contractor's 2027 inspections will cover every service on those four feeders." This fixes the window (twelve months ending September 30, 2026), the count (four), and the ranking criterion (largest non-technical loss) for the sweep.
- Same file, A.3: "Non-technical loss on a feeder is the energy that entered the feeder, at its substation breaker and from customers' own generation, and was neither recorded by a customer's meter, used by the City's unmetered street and area lights, nor lost in the feeder's own conductors, transformers and secondary and service conductors." This fixes the terms of the balance.
- `fy2027_budget_instructions_electric_fund.pdf`, section 1: "The electric utility's 2027 power cost budget uses the twelve months ending September 30, 2026 as its base year: each month of the base year stands for the same month of 2027." Section 2: "Add only new connections that hold an approved service application, from their scheduled service dates, and only works in the approved Construction Work Plan, from their in-service dates. Make no adjustment for weather." These fix the population for the 2027 figures (which new connections and which CWP projects count, and that weather is explicitly out).
- `dpl_electric_rate_schedules_2025-10.pdf`, Schedule SL/AL: "Lighting is not metered: each lamp is charged the monthly kWh below for its lamp type, at the GS energy charge," with a lamp-code table (HPS100=40, HPS150=60, HPS250=100, MV175=70, LED40=15, LED70=26, LED110=40). This is a literal billing convention for the lighting figure. Note under Q5 and Q7 that the engineering tables carry a different, time-varying convention for the same physical quantity.
- `bmpa_wholesale_rate_schedule_w1_2026.pdf`: "Delivery point meters record kWh and kVArh by hour ending, Central Standard Time throughout the year." Fixes the time convention for the purchased-energy interval data.

None of these name a comparison method, a statistical adjustment, or a modeling step; they fix population, window and the literal components of a defined quantity, which is the kind of thing the pack is supposed to pin down in writing.

#### 2. File that already ranks or scores the feeders on the prompt's question

None. No file contains a per-feeder ranking or score of non-technical loss, theft, or tampering for the twelve months to September 2026, or for any other window.

The nearest relative is `loss_evaluation_study_2019_hester.pdf`, Table 2, which ranks all fourteen feeders by technical loss (percent of energy) for calendar year 2019 (APT-4 and NTH-4 highest at 5.46 and 5.45 percent; IND-2 lowest at 3.50 percent). That is a different metric (technical, not non-technical), a different year (2019, not the twelve months to September 2026), and the report itself flags it as stale ("Results rest on the 2019 GIS, the 2019 peak and the City's 2019 load factors. The study should be updated with the next Construction Work Plan"). It does not answer or shortcut the prompt's ranking.

#### 3. File that exists only to help the analyst, not a record the organisation keeps

None found. Every file reads as a document a real department would keep for its own purposes: rate schedules, a wholesale tariff, a consulting engineer's loss study, an RFP, a budget memo, a CWP excerpt, GIS/asset/billing system exports, OMS logs, and a NOAA-style airport weather station file. There is no glossary, README, worked example, or formula cheat-sheet aimed at a solver.

The weather file, `delmont_municipal_airport_daily_2023-09_2026-10.csv`, is the one file whose use in this task is unclear, since the budget instructions explicitly say "Make no adjustment for weather." It reads as genuine public station data (STATION/NAME/DATE/TMAX/TMIN/PRCP, GHCN-style), not a helper file, so it is a plausible unlabelled distractor rather than an aid.

#### 4. Figure or name that reads as the answer rather than context

- `cwp_2027-2028_approved_projects_excerpt.pdf`, project CWP-27-09: "AMI meter deployment, third phase (meters only)" on feeders "APT-4, CHL-2, IND-3." Three feeder codes are named together for a 2027 metering rollout. This is the one place in the pack where several feeders are grouped by name outside of a GIS/billing table, and it is easy to misread as "these are the problem feeders" even though the document only describes a meter hardware rollout and never connects it to loss, theft, or the RFP's selection criterion, and it names three feeders, not the four the sweep requires.
- Hester's 2019 technical-loss ranking (see Q2) could likewise be mistaken for "the answer" to a question it does not answer.
- No specific number I found (a percentage, an MWh figure, a kW figure) matches any of the five requested quantities (the monthly balance, the points-of-rise split, the peak demand addition, the 2027 technical losses, or the four names) anywhere in the pack.

#### 5. Filed sentences that literally fix a requested figure or its population

- RFP A.3 (quoted in Q1): read literally, a feeder's non-technical loss for a period is [energy at the feeder's own breaker] plus [energy fed in from customers' own generation] minus [energy recorded by customer meters] minus [energy used by the City's unmetered street and area lights] minus [the feeder's own conductor, transformer and secondary/service losses]. It implies substation transformer loss and station service, which the Hester study separately scopes out of feeder technical loss, are not part of any one feeder's balance; they sit at the substation.
- RFP A.2 (quoted in Q1): read literally, feeders are ranked and selected by the amount of energy lost (a quantity, not a rate) over exactly one twelve-month window, and exactly four are chosen. That literal reading closes one plausible fork: ranking by absolute lost energy, rather than by loss as a percentage of the feeder's own throughput, which could order the fourteen feeders differently given that feeder annual energy varies roughly sixfold (Hester's 2019 range is about 5,100 to 33,600 MWh).
- `fy2027_budget_instructions_electric_fund.pdf` section 1 to 2 (quoted in Q1): read literally, the 2027 figure for any month is built from the matching month of the base year (October 2025 to September 2026), plus only the named populations of new connections (approved applications, from their scheduled service dates) and CWP projects (from their in-service dates); weather is explicitly excluded as an adjustment.
- `dpl_electric_rate_schedules_2025-10.pdf`'s lighting table versus `distribution_engineering_tables.xlsx`'s "Lamp input watts" and "Burning hours" sheets: the rate schedule gives one flat monthly kWh per lamp type all year (a billing convention), while the engineering tables give input watts (which include ballast losses, higher than nominal watts) times burning hours that vary by month (441 hours in January versus 270 in June). Read literally, each is a complete, different, self-consistent way to produce "the city's lights" figure, and they will not agree. This is a genuine fork for the design to pin down (billed convention vs. physical consumption), not something I resolved.

#### 6. Is there one thing that would make most of the prompt routine, or name the sweep's feeders without the energy balance

No. I did not find a file, sentence, column, or data pattern that resolves the ranking or names (even approximately) the four feeders without doing the energy balance. The nearest near-miss is CWP-27-09's three named feeders (APT-4, CHL-2, IND-3; see Q4), but it is an AMI hardware rollout with no stated link to loss or theft, it names three feeders rather than four, and nothing in the pack says metering upgrades are scheduled for, or because of, high non-technical loss. Taking it as the answer would be a guess, not a derivation.

Per-part breakdown of the prompt's asks:

- **Ranking the fourteen feeders by non-technical loss and picking four**: turns on analysis. The population, window and definition are filed (RFP A.2/A.3, correctly read), but the actual numbers require building each feeder's monthly balance across GIS, CIS, historian breaker data, BMPA delivery-point data (metered at the four substations, not the fourteen feeders, so it must be allocated down), lighting, and the DG customers found in the CIS (RateCode is not DG-flagged directly; DG rows are identified by a populated `kWhRcv`/`RegisterRcv`, and DG penetration by feeder ranges from about 2.3 to 8.0 percent, so this is a real, not token, adjustment). None of this is handed over.
- **The monthly energy balance spreadsheet (Oct 2023 to Sep 2026)**: turns on analysis (assembly across different grains and sources) plus one reading-correctly step (resolving which "city's lights" convention applies, Q5) plus one hygiene step that is run by reflex rather than priced (CIS carries ordinary meter-exchange pairs, same-day Final/Initial rows at register zero, and CT-metered accounts where "kWh" is already the scaled consumption, not "Register" times "Multiplier").
- **Points of the rise (technical vs non-technical vs everything else) from the twelve months to September 2024**: turns on analysis (a decomposition/attribution exercise comparing two twelve-month windows using the balance just built); no file states the split.
- **Peak hourly demand each approved 2027 large connection will add**: turns on reading one population correctly (Status = Approved in `large_load_service_applications_2019-2027.xlsx`, three rows, distinct from CWP's own use of the word "approved" for construction projects, a real but minor cross-file naming trap) plus genuine analysis: the file gives Connected_kW and a Lighting/HVAC/Process split but no demand factor, and the IDR interval file happens to cover exactly the ten already-energized large-load customers (confirmed by service-point match) plus fifteen others, so a peak-to-connected ratio has to be derived from their actual interval shapes, not read off a table.
- **Each feeder's 2027 technical losses**: turns on analysis. The Hester study supplies the textbook method (resistance, load factor, the Buller and Woodrow relation) on 2019 data, which is the expected first move; the 2027 figure has to be rebuilt on the current GIS (as of Oct 27, 2026), reflect CWP-27-03's mid-year conductor change on APT-3 (4/0 to 336.4 ACSR, in service March 2027) and the newly approved large loads, none of which is a plain replay of the 2019 numbers.
- **The one-page memo naming the four**: a deliverable, not a separate computation; it carries result 1 forward.

#### 7. Realism

PDFs are genuine word-processor exports, not toolchain-generated: `pdfinfo` shows Creator "Writer" and Producer "LibreOffice" on every PDF, with plausible, varying versions tied to each document's era (LibreOffice 6.3 on the 2019 Hester report, 25.x on the 2025 files, 26.8.2.2 on the 2026 files) and distinct creation timestamps matching each document's stated date.

Workbooks carry distinct, department-flavoured authorship (`dc:creator` values: "Utilities Finance," "Electric Engineering," "GIS Services," "Customer Engineering," "Systems Integration," "Electric Distribution," "Substations," "Asset Management") with created/modified dates spread over years and consistent with each file's own "as of" date in its name; no hidden sheets, defined names, or cell comments turned up in any workbook.

Authentic mess, all plausible and not concentrated in any one feeder: `historian_feeder_breakers_hourly` carries 4,263 "COMM FAIL" rows (about 1.1 percent) spread fairly evenly across all fourteen feeders and across the full date range; `cis_meter_reads` carries ordinary meter-exchange pairs (a Final read on the old meter and an Initial read of 0 on the new meter on the same day), estimated reads (ReadType "E"), and CT-metered accounts with Multiplier values other than 1 where "kWh" is already the scaled consumption, not "Register"; `oms_switching_orders` mixes two device-naming conventions in its own Device column (OMS-style codes needing the crosswalk or the GIS Switches sheet's PoleTag, and raw GIS SwitchIDs that need neither); two transformers marked removed in the asset register are correctly absent from the GIS network sheet; one of fourteen street-lighting billing accounts spans two feeders instead of one. None of this reads as generated: no fixed-step identifiers, no uniform precision, and no dates that contradict another file or run past the pack's own data (the only forward-looking dates, the three Approved large-load applications' 2027 service dates, are internally consistent with their Requested dates and Status, and are the explicit forward-looking population the budget instructions and the prompt call for). I found no notes/README file, and a full-text search of every file for leak-shaped words (theft, tamper, non-technical, answer key, golden, ranking, solver, synthetic, generated) turned up nothing beyond the RFP's and budget memo's own ordinary language, already quoted above.

#### Flagged files

- `cwp_2027-2028_approved_projects_excerpt.pdf`: harmless. The document contains only project-level facts (feeder, miles, conductor change, in-service date, dollar estimate), no loss percentages, ranking, or figures matching the prompt's requested quantities. Project CWP-27-03's conductor change on APT-3 is a legitimate required input to that feeder's 2027 technical-loss recompute, so any shared number is most likely the generator's own golden correctly reusing a filed project fact, not a disclosed result. CWP-27-09's three named feeders are worth a second look (see Q4 and Q6) but name the wrong count and no loss linkage, so they read as a decoy rather than a leak.
- `oms_gis_device_crosswalk_2024-07.xlsx` and `oms_switching_orders_2023-09_2026-10.csv`: harmless. The switching orders' "Device" column mixes OMS-style codes (which need the crosswalk, or the GIS "Switches" sheet's PoleTag column with a space-for-dash substitution) with raw GIS SwitchIDs (which need neither). The 2024-07 crosswalk is a snapshot that covers only 8 of the 41 distinct devices seen in switching orders over the full 2023-09 to 2026-10 range; the rest resolve through the Switches sheet directly. This is ordinary two-system integration mess (OMS and GIS use different device identifiers), not a leak, and it does not hand over a feeder ranking.
- `large_load_service_applications_2019-2027.xlsx` (dates after 2026-11-05): harmless. The three post-cutoff dates are the ServiceDate field on the three Status = Approved rows (2027-04-01, 2027-05-01, 2027-08-01), which is exactly the forward-looking population the prompt and the FY2027 budget instructions call for ("new connections that hold an approved service application, from their scheduled service dates"). Requested dates, Status, and ServiceDate are internally consistent across all sixteen rows (Energized rows have past service dates, Withdrawn rows have none, Approved rows have 2027 dates), so this is intentional, not stale or contradictory data.

### Dispositions of the second read's points

- The lights' deemed kWh against input watts times burning hours: closed as SF5 by RFP A.3's "used by the City's
  unmetered street and area lights" (real use); the four stands with the lights at their deemed kWh, 200.8 MWh clear of
  the fifth (asserted in checks.py), and the careful pass earns R3.
- Ranking by energy, not rate: closed as SF19 by RFP A.2's "the four feeders that carried the largest non-technical
  loss"; the golden ranks on MWh.
- CWP-27-09's three feeders: harmless. A metering project that names APT-4 and CHL-2 (in every route's four) and IND-3
  (seventh); the meter split no longer points at a contested place (the first read's finding, fixed).
- The three flagged files: harmless, as the first read and the main thread ruled.
