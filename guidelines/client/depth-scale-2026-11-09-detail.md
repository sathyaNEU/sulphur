# Sulfur Depth Scale, task detail (Handshake AI, 9 November 2026)

The client's depth-scale page carries, for each of its 17 real submitted tasks, the full prompt, the input files, the reference solution, the deliverables and the reviewers' good and weak notes. This file keeps that detail as the client's own text, exported 2026-11-11 from the page the author saved; the summary of the same page is `depth-scale-2026-11-09.md`. The page's long dashes are written as commas, colons or parentheses (the house rule for every file in the repository); no other word is changed.

**Learn from it; never reskin it.** Each task here is on file in `.claude/skills/fingerprint/corpus/client_skeletons.json`, and `guard.py check` refuses a draw whose skeleton (decision form, deciding lessons, detection, resolving moves, file roles, answer pattern) repeats one of them (`fingerprint` Part 1b).

## Level 1: Lookup or rule-following

### Is the fund's liquidity status Red? (id 251ff00c)

- **Domain and type:** Quantitative Finance; Data Quality Monitoring & Alerting
- **Setup:** Fund policy sets a coverage test from each holding's days-to-sell. Custody, valuation and market-volume files are provided.
- **Chain:**
  - (routine) Take NAV, cash and 68 holdings from the valuation; average daily volume from 20 days of consolidated volume
  - (from a document) Read Policy 3.9: the sale rate is the fund's own measured participation, not the 20% broker algorithm cap in the Execution Policy
  - (routine) Trace the fund's custody account and map its ids to ISINs
  - (routine) Measure sales from day-on-day falls in settled positions: about 8.0%
  - (from a document) Apply the policy's own arithmetic: coverage 0.76, 33.4% beyond 20 days, Red
- **What flips it:** With the 20% cap the fund looks Green (coverage 1.83); with the policy's definition it is Red (0.76). One run took the cap; the other read the definition and got it right.
- **Why this level:** The whole call rests on reading one definition. After that the policy dictates every calculation, and no measurement choice changes the result.

**Prompt**

> The quarterly liquidity stress test for the US Smaller Companies Fund is due, run as at Friday 23 October 2026, and it goes to the Directors when they meet on Thursday 19 November 2026. The question for the Liquidity Risk Committee is where the fund lands under the liquidity policy and whether it should recommend that the dealing gate be switched on. The policy PDF explains how the test works, and the Penhallow, Kestwick, Tessaly and dealing desk records it relies on are in the attachments.
> 
> The Committee will work through AUSC_liquidity_stress_2026-10-23.xlsx holding by holding, and the risk team files it as the record of the test, so it needs each holding's result and the fund totals, with the coverage figure to two decimal places and NAV shares as percentages to one decimal.
> 
> AUSC_LRC_board_note.docx is the single page the Directors read in their pack beforehand. It should state the result and the Committee's recommendation, say in a line or two where the figures came from, and round money amounts to whole dollars.

**Input files**

1. PFA_AUSC_valuation_2026-10-23.xlsx: administrator's valuation at 23 October 2026 (NAV, cash, 68 holdings)
2. Ardleigh_Liquidity_Risk_Management_Policy_v4.pdf: the liquidity policy that defines the stress test, buckets, limits and actions
3. AUSC_Supplement_extract_Feb2026.pdf: fund supplement extract with the 10% dealing gate
4. Ardleigh_Order_Execution_Policy_2026.docx: execution policy, including the 20% participation limit on the broker's algorithm
5. TMD_daily_volume_history_2025-09_2026-10.csv: daily consolidated market volume by stock
6. TMD_instrument_map.csv: ISIN to market data vendor id map
7. KDS_safekeeping_positions_daily_2025-10_2026-10.csv: custodian's daily settled positions by account
8. KDS_account_register_Ardleigh.xlsx: custodian account register
9. KDS_security_reference.csv: custodian security ids mapped to ISINs
10. Ardleigh_ICAV_subfund_list_2026.xlsx: sub-fund list with client references
11. PFA_AUSC_dealing_history_2024-10_2026-10.csv: daily subscriptions and redemptions by share class

**Reference solution**

The fund lands at Red: the coverage ratio is 0.76 and 33.4% of NAV would take more than 20 trading days to sell, against a 15% limit. The Committee should recommend that the Directors apply the 10% dealing gate in the Supplement from the next dealing day after the meeting. The reference solution starts from the valuation: NAV of $641,972,583, cash of $19,911,300 and 68 holdings, with a stress redemption of 20% of NAV, $128,394,517. Each stock's average daily volume is the mean consolidated volume over the 20 trading days to 23 October, joined through the instrument map. The key input is the sale rate. The policy defines it as the share of market volume the fund's own selling has made up, so it is measured, not taken from the 20% algorithm limit. The fund's sales only show as falls in settled quantity in the custodian's daily positions, in the safekeeping account traced through the sub-fund list and account register. Each fall is moved back one trading day for T+1 settlement and pooled against consolidated volume: 7,213,000 shares over 90,190,700 shares of volume across 313 stock-days, a rate of 8.0%. Each holding's daily sale is 8.0% of its volume, days to sell are rounded up and holdings go whole into buckets. Five-day liquid assets are $96,987,595 (cash plus $77,076,295 of holdings in the 1 day and 2 to 5 day buckets), giving coverage of 0.76; the over-20-day bucket holds $214,544,432. At the 20% limit the same arithmetic gives 1.83 and 10.4%, a Green result.

**Deliverables:** AUSC_liquidity_stress_2026-10-23.xlsx with every holding's result and the fund totals, plus a one-page board note AUSC_LRC_board_note.docx with the result and recommendation.

**Reviewers, good:**
- The sale rate has to be built by joining three record sets (administrator, custodian, market data vendor) and handling T+1 settlement.
- Every holding's days to sell and bucket can be checked line by line in the workbook.
- The decoy 20% limit and the measured 8.0% lead to opposite results (Green against Red), so the stakes of the key step are clear.

**Reviewers, weak:**
- The data is constructed, and the whole call turns on reading one policy definition correctly; after that the policy spells out every calculation and threshold.
- No reasonable variant in measuring the sale rate moves any holding to a different bucket, so the measuring work adds little depth.

### Did the 30-day answered share really fall 7.6 points? (id ce649e2c)

- **Domain and type:** Product Analytics; Data Quality Monitoring & Alerting
- **Setup:** A Q&A site's data dump is used to compare answered shares across two years and decide whether to escalate.
- **Chain:**
  - (routine) Link answers to questions and compute the 30-day answered share by period
  - (judgment) Notice the monthly series steps down exactly 365 days before the snapshot
  - (from a document) Apply the FAQ's spelled-out rule: abandoned unanswered questions are deleted after 365 days, so only the earlier year has been cleaned
  - (routine) Set aside later-year questions that meet the deletion conditions and recompute
- **What flips it:** At face value the share falls 7.64 points (escalate). Applying the documented rule to the later year leaves 0.81 (do not escalate).
- **Why this level:** One sentence from the FAQ unlocks it, and the fix is applying that sentence. Both runs saw the gap and said deleted history cannot be recovered.

**Prompt**

> We track how well our Q&A communities answer new questions. If the share answered within 30 days falls by at least 3 percentage points year over year, we escalate it to the community team.
> 
> Please use the attached data to review the eight sites combined. Did the share of new questions answered within 30 days fall by at least 3 percentage points from questions asked April 2022 to February 2023 to questions asked April 2023 to February 2024?
> 
> Please prepare a one-page note in `answer_rate_note.docx`. Start with the change and the decision, then explain how you arrived at it.
> 
> I also need `answer_rate.xlsx`. Include the number of questions and the share answered within 30 days for each site and for all eight sites combined, for both periods. Add a chart showing the answered share by month.

**Input files**

1. academia, cooking, datascience, diy, law, money, travel and workplace _posts.csv (8 files): Stack Exchange questions and answers for each site
2. data_dump_schema_documentation.pdf: schema documentation for the data dump, including which posts it leaves out
3. meta_stackexchange_faq_export_2024-03-31.pdf: platform FAQ export, including the rules for removing abandoned questions
4. policy_generative_ai_banned.pdf: site policy on generative AI content

**Reference solution**

Do not escalate. On a like-for-like basis the share of new questions answered within 30 days fell by 0.81 percentage points, from 83.10% to 82.28%, well short of 3 points. The reference solution links answers to their questions within each site and marks a question answered if its first answer came within 30 days. For April 2022 to February 2023 that gives 21,410 questions, 17,791 answered (83.10%). Taken at face value, April 2023 to February 2024 has 22,228 questions and 16,772 answered (75.45%), a fall of 7.64 points, and the monthly series steps down at April 2023, exactly 365 days before the 31 March 2024 snapshot. That step is the clue. The schema documentation says removed posts are not in the dump, and the FAQ export (p. 95) says abandoned unanswered questions are removed only once they are older than 365 days. So the earlier year has already been cleaned and the later year has not. The data confirms it: the unanswered share drops from 22.2% at 330 to 360 days old to 13.7% at 370 to 400 days, and only 2 earlier-period questions still meet the removal conditions against 1,845 later-period ones. Setting those 1,845 aside (none answered) leaves 20,383 questions and 82.28% answered. Variants of the removal rule give falls of 0.74 to 0.93 points. By site, only diy falls by more than 3 points (4.48), and datascience moves from a 27.75-point fall to a 4.06-point rise; it holds 1,265 of the 1,845 set-aside questions.

**Deliverables:** A one-page note answer_rate_note.docx opening with the change and the decision, and answer_rate.xlsx with question counts and 30-day shares by site and combined for both periods, plus a monthly chart.

**Reviewers, good:**
- Real Stack Exchange data with a genuine survivorship problem: the snapshot has already lost the earlier year's removed questions.
- The clue is visible in the data itself (a step exactly 365 days before the snapshot) and can be confirmed from the age profile of unanswered questions.
- Per-site and combined figures on both bases give many checkable results.

**Reviewers, weak:**
- It is a one-thing flip: once you know the dump leaves out removed posts, the fix is applying the FAQ's written removal rule as a filter.
- The deciding step is reading what the files contain and applying a documented rule, rather than analysis that stays hard end to end. Both model runs noticed the deletions and stopped there.

## Level 2: One-thing flip

### Site the new birth-registration office in Carrow or Dunmore? (id db3a6bc0)

- **Domain and type:** Sociology & Demography; Opportunity Sizing & Decision Support
- **Setup:** A registry, a completeness report and committee rules are used to estimate 2024 unregistered births by district and rank them.
- **Chain:**
  - (routine) Count births by mother's residence and reassign waiting-home lodgers
  - (judgment) Split completeness into facility and home births and apply each to the 2024 mix
  - (the one thing) Spot that Carrow's 2022 home-birth registrations include mobile drives that ended in September 2022, and remove them
  - (routine) Apply the capacity rule and rank the gaps
- **What flips it:** Keep the drive registrations and Dunmore comes first (5,687 vs 5,406). Remove them and Carrow leads (7,808 vs 5,779).
- **Why this level:** One built-in break in how births were registered decides the district. It shows in one cross-tab of channel by year. Both runs called it the biggest risk, then did not adjust.

**Prompt**

> Kellemere Province has funding for exactly one new maternity facility with surgical capability (CEmONC), and I have to put a district in front of the maternal health steering committee on Thursday. The director of Ashbourne Regional is lobbying hard for it because her delivery wards ran over capacity throughout 2024. The committee agreed its siting rule and its planning standard at the November meeting (the minutes are in the pack) and wants the numbers done properly before it signs anything, taking 2024 as the last full year we have.
> 
> I need one decision: which district, and what annual delivery volume we should design for if the new facility, taking all of that district's facility deliveries, is to bring it up to the provincial target of 85% of resident births delivered in a facility.
> 
> Write maternity-siting-memo.docx with the decision first, the ranking of all six districts under the committee's rule, a plain explanation of where Ashbourne Regional's case stands in the numbers and what the recommendation would do to its workload, and how robust the choice is to the assumptions you had to make. Two pages plus one chart. Back it with district-birth-model.xlsx: the cleaned 2024 registry counts, how you got from registered to expected births, the capacity gap, and a sheet reconciling the registry against what the facilities reported for 2024, with anything off by more than 5% flagged and explained. The data pack from the Provincial Statistics Office is attached.

**Input files**

1. cr_birth_registrations_extract_2022_2024.csv: civil registry birth records with residence, place and registration channel
2. completeness_assessment_2023.pdf: registration completeness report with the reference period and Tables 1 and 2
3. mhsc_minutes_2025-11-13.docx: steering committee minutes with the siting rule and planning standard
4. health_facility_register_2024.csv: facilities with planned delivery capacity
5. hmis_monthly_facility_deliveries_2024.csv: monthly deliveries reported by each facility
6. cr_statistical_bulletin_2024.xlsx: published registration counts by district
7. district_profiles_2024.json: district and sub-district profiles
8. population_projections_mid2024.csv: mid-2024 population projections
9. census_2016_population_age_sex.csv: 2016 census population by age and sex
10. khs_2023_district_indicators.csv: household survey indicators by district
11. emonc_travel_times_subdistrict_2024.csv: travel times to emergency obstetric care by sub-district
12. README.txt: notes on the data pack

**Reference solution**

Site the facility in Carrow: about 7,808 expected resident births in 2024 against zero counted capacity, the largest gap, and design it for about 6,640 deliveries a year (85% of 7,808). The ranking is Carrow +7,808, Dunmore +5,779, Belmere +893, Esker +456, Fenwick -214 and Ashbourne -3,330. The reference solution cleans the registry first: 89,670 rows, 1,329 duplicates removed, and only 2024 live births registered within 12 months kept, leaving 27,329. Births are counted by the mother's district of residence, with 893 unstated residences allocated pro rata, and waiting-home lodgers coded to the hospital's address are moved back: 384 to Carrow and 96 to Dunmore. Expected births come from dividing facility births by facility completeness and home births by home-birth completeness. Carrow's reference-period home rate (April 2022 to March 2023) includes 835 home births registered at mobile drives that ended in September 2022. Comparing office registrations during and after the drives (about 20 against about 68 a month) shows about 25% of drive registrations replaced office visits, so the rest are removed and Carrow's 2024 home completeness is 20.2%, not 34.2%. Carrow Central's planned 900 counts as zero because it reported no deliveries in 2024 (minutes item 3.4). Moving about 1,240 Carrow deliveries takes Ashbourne Regional from 10,198 deliveries (107% of capacity) to about 8,960. Leaving the drives in would put Dunmore first (5,687 against 5,405). The reconciliation flags St Brigid's (-11.5%) and Esker Mine Clinic (+7.6%).

**Deliverables:** maternity-siting-memo.docx (decision first, ranking, the Ashbourne Regional case, robustness, two pages plus one chart) backed by district-birth-model.xlsx with cleaned counts, expected births, the capacity gap and a registry against facility reconciliation.

**Reviewers, good:**
- A layered, realistic planning problem: registration district against residence, waiting-home coding, completeness by facility and home, and a capacity rule from the minutes.
- Many intermediate figures can be checked, from the cleaning log to the ranking and the reconciliation flags.
- A stakeholder's case (Ashbourne's overflowing wards) has to be answered with numbers, not just the ranking.

**Reviewers, weak:**
- The data is constructed, and the district flips on one planted break: drive registrations exist only in 2022 and only in the two leading districts, visible in a single channel by year table.
- Model runs did the residence, waiting-home and completeness work and still picked Dunmore; the margin with the drives left in is small.

### Approve the vegetation trimming cycle? (id c3c4e2ab)

- **Domain and type:** Energy Systems & Utilities; Experiment & Causal
- **Setup:** Outage records for trimmed and untrimmed circuits are used to price each avoided interruption against a $250 bar.
- **Chain:**
  - (routine) Reproduce the vegetation group's figures: trimmed circuits +5%, the rest of the system +31%
  - (judgment) Ask why untrimmed circuits got so much worse
  - (the one thing) Find that circuits sharing a contractor crew yard with the cycle rose +54% and +42%, while circuits in yards with no cycle work rose +6%
  - (routine) Compare only against the clean yards and recompute the cost per interruption
- **What flips it:** Against all other circuits the cycle looks like a pass at about $168 per interruption avoided. Against clean yards the effect is about −4% and the cost is $910 or more, a fail.
- **Why this level:** A spillover built into the comparison group decides it. Once you know about the crew yards, picking the clean comparison is routine. The run never looked at yards.

**Prompt**

> The operations committee votes on the 19th on whether every overhead circuit goes on a three-year trim cycle starting with the 2027 budget. We've had 171 circuits on it since 2023, each pruned end to end that year, and the vegetation group's summary says tree-caused customer interruptions on those circuits ran about a fifth below the rest of the system across 2024 and 2025. Our planning standard for reliability spending is no more than $250 a year per customer interruption avoided a year. For this the count that matters is sustained, tree-caused interruptions outside major event days, measured against what the circuits were running in 2021 and 2022, before any of this started. What the cycle costs per overhead mile per year should come out of its own ledger over the first full cycle, 2023 through 2025, and not from the contractor's bid sheet.
> 
> Does the three-year cycle clear $250 if we take it systemwide? If it doesn't, the forestry manager will propose doing only the circuits the 2022 survey classes as heavy canopy, so I need to know whether those would clear it by themselves. The committee gets trim_cycle_recommendation.docx, two pages at most with one chart, and engineering will want trim_cycle_workbook.xlsx behind it with the estimates and a row for every circuit so they can check the work. The vegetation group will be in the room, so whatever you land on has to be squared with their fifth.

**Input files**

1. oms_classic_incidents_2021/2022/2023.csv: legacy outage system incidents up to June 2023 (Eastern time)
2. gridview_restoration_steps_2023 to 2025H2.csv (5 files): new outage system restoration steps (UTC)
3. oms_reference_tables.xlsx: outage cause and code lookups
4. circuit_master.csv: circuits with legacy feeder numbers and overhead miles
5. operating_areas.csv: operating areas and their contractor crew yards
6. three_year_cycle_work_orders.csv: trim cycle work orders that identify the 171 cycle circuits
7. three_year_cycle_ledger_2023-2025.xlsx: the cycle's cost ledger
8. vegetation_survey_2022.xlsx: 2022 canopy survey by circuit
9. customer_counts_by_circuit_2021_2025.csv: customers served per circuit by year
10. major_event_days.csv: declared major event days
11. EIA861 reliability files, EIA-861 instructions and the FERC vegetation management report: industry reference material
12. noaa_ghcnd_daily_2021_2025.csv, pole_inspection_results_2024.csv, district_reliability_indices_2021_2025.xlsx: weather, pole inspections and district indices

**Reference solution**

The three-year cycle does not clear $250, systemwide or on heavy canopy alone. Systemwide it costs $1,548 per customer interruption avoided ($15,466,214 a year for 9,988 avoided); heavy canopy alone costs $910 ($7,089,655 for 7,790 avoided). The reference solution first puts the two outage systems on one basis: legacy incidents to June 2023 in Eastern time, then the new system's UTC restoration steps converted and collapsed to one event with customers counted once. It keeps tree-caused, unplanned interruptions over five minutes outside the 43 major event days. The 2021-22 baseline is 307,480 customer interruptions a year, 193,630 on heavy canopy, compared with 2024-25. The ledger gives $14,662,162 over 5,774 miles and three years, $846 per mile per year ($861 heavy canopy, $826 other). The vegetation group's fifth reproduces: cycle circuits +5% against +31% for the rest. But the gap comes from the comparison circuits getting worse. Regular circuits rose 54% in areas with cycle work and 42% in the other area served by the same crew yard, against 6% in yards with no cycle work, so crews diverted to the cycle hurt their neighbours. Measured against undisturbed circuits with a fixed-effects Poisson model, the cycle cuts interruptions 4.0% on heavy canopy and 1.9% elsewhere. Checks show no yard pattern before the cycle and none in equipment outages. Comparing with all other circuits would give $162 on heavy canopy, a false pass.

**Deliverables:** trim_cycle_recommendation.docx (two pages at most, one chart) and trim_cycle_workbook.xlsx with the estimates and one row per circuit.

**Reviewers, good:**
- Heavy, realistic data assembly: two outage systems, time zones, restoration steps and major event days.
- The cost comes from the ledger, and every circuit's figures sit in the workbook for checking.
- The answer has to square with a stakeholder's own number (the fifth) rather than just ignore it.

**Reviewers, weak:**
- The data is constructed, and the call flips on one planted pattern (comparison circuits in shared crew yards worsening) that no document mentions.
- Once the crew-yard spillover is spotted, a clean-yard comparison settles the answer quickly.

## Level 3: One real method step

### Will extra court sitting hours close the trial backlog? (id 35842bf8)

- **Domain and type:** Criminology & Justice; Opportunity Sizing & Decision Support
- **Setup:** Public court statistics are used to decide whether a proposed increase in hearing hours closes an annual gap of about 8,260 trial cases.
- **Chain:**
  - (routine) Annual gap from receipts minus disposals, cross-checked against the rise in open cases
  - (judgment) Recognise that an extra hour does not buy the average case: early guilty pleas and dropped cases barely use hearing time
  - (judgment) Test it on the 2020 jury-trial pause and recovery: contested trials track hearing time, early pleas track receipts
  - (routine) Marginal rate of about 91 cases per 1,000 hours gives about 4,500 extra cases
  - (routine) Split by region and estimate the Wales figure
- **What flips it:** At the 4.68-hour average, the hours buy about 10,700 cases (yes). At the marginal rate they buy about 4,500 (no).
- **Why this level:** Marginal versus average is a genuine insight, backed by real evidence in the data. But it is the only hard step. The run assumed marginal cases look like the average and said yes.

**Prompt**

> I'm preparing advice for ministers on a proposal to fund 50,000 extra Crown Court hearing hours a year in England and Wales. With everything else held as it was in the year to June 2025, would that be enough to stop the number of cases waiting for trial from rising? Using the attached data, give me a clear yes or no, roughly how many extra cases the hours would clear each year, and how many extra hearing hours would be needed to stop the rise.
> 
> We also need to know where the hours would help most and whether any region would still see its waiting list grow if they were shared out in line with current court time. If Wales received its share, roughly how many extra people a year would go straight to prison? Please put the advice and supporting figures in a short PDF briefing note for ministers, with a regional spreadsheet the team can sort and reuse.

**Input files**

1. cc_rdos_tool.xlsx: Crown Court receipts, disposals and open cases (pivot tool)
2. cc_open_tool.xlsx: open caseload by age and averages (pivot tool)
3. cc_waiting_hearing_tool.xlsx: waiting times and hearing times by case type (pivot tool)
4. cc_plea_tool.xlsx: pleas and outcomes for trial defendants (pivot tool)
5. trials_tool.xlsx: trial effectiveness and reasons (pivot tool)
6. fact_crown_court_appearances_convictions_wales_ye2018_2025.csv: Wales Crown Court appearances and convictions
7. fact_crown_court_sentencing_outcomes_wales_ye2018_2025.csv: Wales sentencing outcomes
8. fact_cautions, fact_penalty_notices and fact_crown_court_compensation (Wales): other justice outcomes
9. dim_offence_group_classification_q2_2025.csv and dim_police_force_area_dec2025.csv: lookups
10. Three Ministry of Justice statistics PDFs: quarterly bulletin, user guide and technical guide

**Reference solution**

No. With everything else as it was in the year to June 2025, 50,000 extra hearing hours would clear about 4,500 extra trial cases a year (range 3,200 to 5,700), short of the 8,260 gap. Stopping the rise needs about 91,000 hours (72,000 to 130,000). The gap is trial receipts of 74,975 less disposals of 66,715 over 2024 Q3 to 2025 Q2, matching the rise in open trial cases from 56,511 to 64,781. The shallow route divides 292,151 hearing hours by cases, 4.68 hours each, and says 10,700 cases and yes. The reference solution rejects it: early guilty pleas (37,193 defendants) and dropped cases (13,437) use little court time and follow receipts, not hours. The data shows this. When jury trials stopped in April to June 2020, contested trials fell to 20% and trial-day pleas to 16% of their earlier level, while early pleas (70%) and drops (73%) moved with receipts (64%), in every region. Extra hours buy contested trials (15.71 hours each) plus about 0.508 trial-day pleas per contested trial (1.80 hours each): 0.091 disposals per hour, or about 4,540 cases. London holds 41% of the gap (3,350 a year) and needs about 56,000 hours alone; shared pro rata, it would still rise by about 2,500 a year. Wales's share, about 1,950 hours, clears about 250 cases; using its conviction rate (30.5%), custody rates (69.6% and 61.3%) and defendants per case, about 100 more people a year go straight to prison.

**Deliverables:** A short PDF briefing note for ministers with the yes or no and supporting figures, plus a sortable regional spreadsheet.

**Reviewers, good:**
- Real Ministry of Justice published data, including awkward pivot-tool workbooks.
- A genuine economics point (extra hours buy contested trials, not the average case), supported by a natural experiment in the data itself: the 2020 jury trial pause.
- Regional and Wales follow-ons chain several sources and give many checkable figures.

**Reviewers, weak:**
- The national call rests on one insight, marginal against average cost, so the depth is concentrated in a single step.
- The Wales prison figure chains several rates and per-case conversions, so it is approximate.

### Keep the overflow staffing agency on retainer? (id 0f7f50e0)

- **Domain and type:** Healthcare Delivery & Health Economics; Forecasting & Predictive
- **Setup:** A 130-bed hospital keeps the retainer if it expects at least one quarter in twenty with five or more overflow weeks. Public weekly hospital census data are provided.
- **Chain:**
  - (routine) Build a weekly census panel from the facility files (suppression, coverage, completeness)
  - (judgment) Question the independence that a one-in-eight rate implies, and test it: an overflow week follows another 62% of the time vs 6% after a normal week
  - (judgment) Choose peers like the asker and count how often their quarters had five or more overflow weeks
  - (routine) Check robustness, multiply by twenty and compare with the one-quarter line
- **What flips it:** Treating weeks as independent gives 0.33 quarters in twenty (drop the agency). Clustered weeks give about 2 (keep it).
- **Why this level:** Serial dependence is a real feature of real data and needs measuring. But one insight carries the whole call. The run noted clustering could matter and never tested it.

**Prompt**

> Our nursing budget uses overtime to cover overflow weeks. An overflow week is any week when our census is 10 percent or more above our average. The overtime budget allows for up to four overflow weeks per quarter. A fifth overflow week in the same quarter means bringing in the staffing agency. We have about 130 occupied beds in a normal week, and about one week in eight is an overflow week.
> 
> The new five-year contract term brings up the agency's place on our approved vendor list. Keeping them there leaves us with credentialing and orientation work every year. I only want them on the list if we will actually use them.
> 
> Work out how many of the twenty quarters in the term we should expect to need agency staff. One quarter or more and we keep the agency on the list; fewer than one and we drop them and cover a fifth week some other way when it comes. Put this in a one-page write-up the finance committee can follow. Give the committee the number of quarters and the call that follows from it.

**Input files**

1. hospital_weekly_capacity_GA/NC/OH/PA/TN/VA.csv (6 files): weekly facility-level hospital capacity and census
2. README.txt: column meanings for the weekly files
3. state_hospital_capacity_daily.csv: statewide daily capacity totals
4. Hospital_General_Information.csv: hospital type, ownership and ratings
5. HOSPITAL_Data_Dictionary.pdf: dictionary for the hospital information file

**Reference solution**

Keep the agency on the list. About two of the twenty quarters should need agency staff; every careful form gives 1.26 to 2.73, all at or above one. The reference solution builds a weekly census panel from the six state files (116,665 rows, 823 hospitals), using the 7-day average of occupied inpatient beds, treating the suppressed value and blanks as missing and keeping only fully covered weeks. The main window is the 95 weeks from July 2022 to April 2024, with 394 Short Term hospitals. An overflow week is one at or above 1.10 times the hospital's own average: 13.5% of hospital-weeks, 12.6% at 100 to 150 beds, so one week in eight fits a hospital of about 130 beds. The obvious route treats each week as an independent one-in-eight chance: a 1.65% chance of five or more in 13 weeks, 0.33 quarters over twenty, and drop. But overflow weeks cluster. An overflow week follows an overflow week 61.4% of the time (62.4% at 100 to 150 beds), against 6.0% after a normal week. Counting directly, 100 to 150 bed hospitals whose own share is close to one in eight had five or more overflow weeks in 9 of 98 quarters from July 2022 (1.84 over twenty) and 28 of 220 from July 2021 (2.55). A two-state week-to-week chain at 62.4% gives 10.83% a quarter, 2.17 over twenty, and a hold-out check gives 2.66. Since every form that allows clustering gives one quarter or more, the call is keep.

**Deliverables:** A one-page write-up for the finance committee giving the expected number of agency quarters and the keep or drop call.

**Reviewers, good:**
- Real public hospital data with realistic messiness: suppression codes, partial weeks and gaps.
- The prompt's framing invites a binomial, and the data shows why that is wrong.
- The answer can be checked two ways: by a model and by directly counting similar hospitals' quarters.

**Reviewers, weak:**
- It is essentially one statistical insight (weeks are not independent) followed by a direct count, so depth is thin.
- Once clustering is noticed, the rest of the work is routine.

### Keep the backup collections retainer? (id 23bec3ac)

- **Domain and type:** Banking, Credit & Financial Risk; Opportunity Sizing & Decision Support
- **Setup:** A credit union with about 400,000 loans keeps an outside collections team if there is at least a 1-in-20 chance year-end delinquencies exceed in-house capacity. Public call-report data are provided.
- **Chain:**
  - (routine) National delinquency rate from call reports and the plan count of 4,309 accounts
  - (judgment) Recognise that loans within one institution share shocks, so a loan-by-loan binomial understates the risk
  - (judgment) Measure the spread between institutions by size and see it stops shrinking past about 50,000 loans
  - (routine) Read the exceedance chance and the 95th-percentile capacity from size-matched peers
- **What flips it:** An independent-loan binomial gives a chance near zero (drop). The spread between similar-sized credit unions gives 0.19 and a capacity need of about 8,261 (keep).
- **Why this level:** A genuine credit-risk lesson on real data. The run named the dependence risk and still used the binomial. Beyond that one step, the work is light.

**Prompt**

> Our merger with two neighboring credit unions is due to close next summer, leaving the combined credit union with about 400,000 loans. Our collections plan was built on the assumption that our share of loans two or more months delinquent at year end would match the national rate for all federally insured credit unions, about 1.07 percent last December, or roughly 4,300 accounts for us. We're building an in-house team that can work up to 6,300 accounts that far behind. Anything beyond that goes to an outside collections firm we keep on retainer for about $400,000 a year. The board would like to end that contract.
> 
> If the chance that our year-end count of loans two or more months delinquent goes over 6,300 is under 1 in 20, we drop the retainer; at 1 in 20 or more, we keep it. I need that chance as one number, the call it leads to, and how many accounts the in-house team would have to be able to work for the chance to fall under 1 in 20, since that is the capacity we'd price against the retainer. We have NCUA's year-end call report data for the last several years, more than this question needs. I owe the board a memo of no more than 300 words before the vote, with one chart or table that shows where the number comes from. What I take to the board will be the decision that number calls for.

**Input files**

1. call-report-data-YYYY-12__FS220.txt and FS220.txt (5 Decembers): total number of loans per credit union (account 025A)
2. call-report-data-YYYY-12__FS220A.txt and FS220A.txt: number of loans two or more months delinquent (account 041A)
3. call-report-data-YYYY-12__FOICU.txt and FOICU.txt: credit union details, including charter and insurance type
4. AcctDesc.txt: account descriptions for the call report schedules
5. FOICUDES.txt: field descriptions for the FOICU file
6. Report1.txt: counts of credit unions by charter type
7. FS220B.txt: a further call report schedule
8. FINANCIAL TRENDS IN FEDERALLY INSURED CREDIT UNIONS 2025Q4.xlsx: national trends workbook (delinquency by dollars)

**Reference solution**

Keep the retainer. The chance that the year-end count of loans two or more months delinquent exceeds 6,300 is about 0.19, well above 1 in 20, and the in-house team would need to handle about 8,261 accounts for the chance to fall below 1 in 20. The reference solution joins the loan count, delinquency count and credit union details on CU_NUMBER for five Decembers and keeps federally insured credit unions with loans. The national rate is counted by loans, not dollars: 1.0772% in December 2025, so the plan is 4,309 accounts, and 6,300 is 1.575%, 0.498 points above it. Treating 400,000 loans as independent gives a spread of only 65 accounts, a chance of essentially zero and a team of 4,417, which would drop the retainer. The call reports show why that is wrong. Credit unions with 200,000 to 800,000 loans sit 0.581 points (root mean square) from their December's national rate, against 0.020 points from loan-by-loan chance, and the spread stops shrinking once books pass about 50,000 loans. So the reference solution reads the spread from credit unions of this size: each rate minus that December's national rate is added to the plan and applied to 400,000 loans. In 48 of 253 such December reports the count passes 6,300, a chance of 0.19; careful variants give 0.088 to 0.273. The smallest count fewer than 1 in 20 of those reports would exceed is 8,261 (12 of 253 above it).

**Deliverables:** A board memo of no more than 300 words with the chance, the call and the required team size, plus one chart or table.

**Reviewers, good:**
- Real regulator data that needs schedule and field lookups (count-based accounts rather than the dollar rate).
- A genuine credit risk lesson: at this size the risk comes from institution-wide shocks, not loan-by-loan chance.
- The key figures can be checked by direct count of similar-sized credit unions.

**Reviewers, weak:**
- One modelling insight carries the call, so the depth is concentrated in a single step.
- The team size depends on how the peer group is chosen, and careful variants span a wide range (about 6,700 to 10,800).

## Level 4: Layered

### Repair turbine 3's night-stop fault? (id 8ec45b05)

- **Domain and type:** Energy Systems & Utilities; Opportunity Sizing & Decision Support
- **Setup:** Real wind-farm SCADA data. Turbine 3 parks at night in one wind arc. The repair pays back in six years if it saves more than 160 MWh a year.
- **Chain:**
  - (routine) Night stop hours with turbine 3's vane in the arc: about 198 MWh a year of its own output
  - (judgment) From the layout, find the turbines downwind and pick an unwaked reference (turbine 2, not 1 or 4)
  - (judgment) Estimate turbine 5's wake deficit by direction bin and convert it to recovered energy, about 102 MWh a year
  - (judgment) Validate against turbine 3's real outages and pick up turbine 6's offsetting loss; bootstrap by event
  - (judgment) Correct to a normal wind year with a 30-year reanalysis fit; repeat for the wider arc, which flips to repair
- **What flips it:** Turbine 3's own output (about 200 MWh) says repair. The farm's net loss, after turbine 5 recovers its wake, is about 109 MWh, below the 160 break-even.
- **Why this level:** Wake recovery is the central idea, but turning it into a number takes a reference choice, direction binning, an outage check and a long-term correction. Both runs priced turbine 3 alone.

**Prompt**

> The council's environmental health team has finally pinned the night-time hum the family on Mill Lane keep reporting to a tone from turbine 3's gearbox at Wenlow. They've given us two ways to close the complaint: get the gearbox repaired, or stop turbine 3 at night (night as the government's wind turbine noise guidance defines it) whenever the wind at turbine 3 is blowing from between 285° and 325°. The contractor has quoted £72,000 for an uptower repair. Our rule for unplanned spend is that it has to pay for itself within six years at our PPA price of £75 per MWh, so what I need to know is whether the stop would cost us enough energy in a normal year to justify the repair, or whether we take the stop and leave the gearbox until its planned replacement.
> 
> Please write a short memo for the asset committee that makes the call and gives the energy the stop would cost us in a normal year, with a range they can rely on. Send the Python you used with it, so our analyst can rerun the numbers when next year's SCADA comes in. The council also warned that if complaints continue they may widen the arc to 270° to 335°; tell me whether that would change the answer. Our SCADA exports and the other files we pulled together are attached.

**Input files**

1. Turbine_Data_Wenlow_1 to 6, 2019 to 2021 (18 files): 10-minute SCADA per turbine per year (wind speed, direction, power, availability)
2. Status_Wenlow_1 to 6, 2019 to 2021 (18 files): turbine status and event logs
3. Wenlow_WT_static.csv: turbine positions and rotor details
4. Wenlow_WT_dataSignalMapping.csv: SCADA signal name mapping
5. Device_Data and Status files for the Wenlow grid meter, 2016 to 2023: farm export meter data and status
6. open-meteo-52.41N1.00W147m (4 files, 1990 to 2025): long-term hourly weather reanalysis at the site
7. wind-turbine-noise-guidance.pdf: government noise guidance, which defines night

**Reference solution**

Take the night stop and leave the gearbox. In a normal year the stop costs the farm about 109 MWh (range 97 to 139), worth £8,165 a year, so the £72,000 repair would take 8.8 years to pay back (6.9 at the top of the range). The six-year rule needs at least 160 MWh a year. The reference solution reads the 18 SCADA exports (157,824 ten-minute steps), converts UTC to UK local time because the guidance defines night as 23:00 to 07:00 local, and takes turbine 3's own vane between 285° and 325°: about 343 hours a year. Turbine 3 makes 197.9 MWh a year in those hours. On that figure alone the repair pays back in 4.8 years, but that is turbine 3's loss, not the farm's. The layout shows turbine 5 sits 3.3 rotor diameters straight downwind of turbine 3 in that arc, and turbine 6 sits 7.1 diameters behind. At night turbine 5 makes only 0.29 of what unwaked turbine 2 makes with the wind from 300° to 305°. With turbine 3 parked, turbine 5 gets back about 102 MWh a year, 51% of turbine 3's output. Turbine 3's 23 real outages in the arc confirm it: turbine 5 rose by 49% and turbine 6 fell by 6%. A long-term power fit over 1995 to 2024 puts a normal year at 1.012 times 2019 to 2021: 200 less 103 plus 12 gives 109 MWh. Widening the arc to 270° to 335° raises the loss to about 210 MWh (payback 4.6 years), which flips the answer to repair.

**Deliverables:** A short memo for the asset committee with the call and the normal-year energy cost with a range, the rerunnable Python script, and whether the wider arc changes the answer.

**Reviewers, good:**
- Real wind farm SCADA with realistic export quirks (comment headers, UTC timestamps, missing values).
- The key insight comes from physical reasoning about the layout, and it is then quantified and cross-checked against the turbine's own real outages.
- A normal-year correction and a scenario that flips the answer add genuine further steps.

**Reviewers, weak:**
- The depth is concentrated in the wake recovery step; the call hinges on it.
- The top of the range (6.9 years) is not far above the six-year rule.

### Has re-offending after a first arrest fallen by at least 10%? (id b34ffd70)

- **Domain and type:** Criminology & Justice; Comparative & Explanation
- **Setup:** Real city arrest and crime-report data. The board's rule needs a 90% confident drop between the 2013 to 2014 and 2022 to 2023 cohorts.
- **Chain:**
  - (routine) One arrest event per person-day; reproduce the draft −27.7%
  - (judgment) Equalise the look-back so "first arrest" means the same in both cohorts: −14.7%, still passes
  - (routine) Count only re-arrests for new crimes
  - (judgment) Link arrests to crime reports: the share of reported crimes ending in arrest fell from 18.9% to 11.9%
  - (judgment) Deflate later re-arrests by the clearance ratio, offence by offence: +25.5%, fails
  - (routine) Bootstrap people and counts; every variant fails the rule
- **What flips it:** The look-back step moves the figure from −27.7% to −14.7%. The detection step turns it into +25.5% and the answer to no.
- **Why this level:** Two genuine measurement judgments, both standard in criminology, both needing estimation. Both runs flagged the caveats and stopped at recorded re-arrest.

**Prompt**

> Our annual crime report draft says people arrested for the first time are re-offending less, down more than a quarter, comparing who got first arrested in 2013-14 with 2022-23 and looking two years after the first arrest. Public defender office already question that line but they did not give there own number. Chief will not sign it until the reentry board say ok. For the board re-offending mean a new crime in the two years after the first arrest, probation, pretrial release or warrant things do not count. Board rule: report can say first time arrestees re-offend less only if we are 90 percent sure their two year re-offending is lower than the 2013-14 group.
> 
> Everything is in the folder.
> 
> Need reoffending_check_memo.pdf, two page max. Put the yes or no first with the change you are getting and the 90 percent range. Show it by offense type, each person under the worst charge on their first arrest, violent, burglary, theft and other, with one chart. Then reoffending_check.csv, one row per offense type plus one row for everybody, with the numbers behind the call so our analyst can check every one.

**Input files**

1. fact_arrests.csv: arrest charges by person, date, charge and case number
2. dim_person.csv: person records (with some placeholder ids)
3. dim_charge.csv: charge codes and categories
4. crime_responses_2011_2026.csv: reported crime incidents
5. arrests_dataset_metadata.json and crime_responses_dataset_metadata.json: field descriptions, including the NIBRS switch
6. gpd_police_zones.csv: police zones
7. nibrs_offense_definitions_2019.pdf: NIBRS offence definitions
8. effects_of_nibrs_on_crime_statistics.pdf: note on how NIBRS changed crime counts
9. gun-violence-memo-2024-12-16.pdf: an unrelated police memo

**Reference solution**

No. Once re-arrest is adjusted for the fall in how often crimes end in arrest, two-year re-offending for 2022-23 first-time arrestees is about 25.5% higher than for 2013-14 (90% range +12.7% to +39.8%), and the chance it is lower is under 0.001, so the board rule fails. The reference solution removes 988 duplicate charge rows and two placeholder person ids, giving 37,346 arrest events for 23,125 people, and reproduces the draft's 19.0% against 13.8%, a 27.7% fall. First step: the 2013-14 group has only 2 to 4 years of earlier history in the file, the 2022-23 group 11 to 13, so 'first arrest' means different things. Giving each 2022-23 arrest the same look-back raises that group from 1,582 to 2,110 people. Counting only new crimes on new cases gives 18.3% (801 of 4,368) against 15.6% (330 of 2,110), a 14.7% fall with a 0.997 chance of being lower, which on its own would pass. Second step: re-arrest depends on police solving crimes. Matching arrests to crime reports, the share of victim crimes ending in arrest fell from 18.9% in 2013-16 to 11.9% in 2022-25 (violent 39.7% to 25.3%, burglary 16.4% to 5.7%, theft 13.9% to 6.3%), mostly between 2014 and 2019, before the NIBRS switch. Adjusting victim-crime re-arrests by type gives +25.5%. Violent first arrests are +8.5% (chance lower 0.211). Every variant gives +7.8% to +104.1%, and passing would need 77% of the old clearance rate against 63% seen.

**Deliverables:** reoffending_check_memo.pdf (two pages at most, yes or no first with the change and 90% range, by offence type with one chart) and reoffending_check.csv with one row per offence type plus everybody.

**Reviewers, good:**
- Real city arrest and crime report data with duplicates, placeholder ids and a recording system change.
- Two genuine analytical steps: equalising the look-back that defines 'first arrest', and recognising that re-arrest depends on how often crimes are solved.
- Clear rule (90% sure) and a csv that lets an analyst check every figure.

**Reviewers, weak:**
- The clearance adjustment is a modelling choice with a wide spread across variants (+7.8% to +104.1%), although all of them fail the rule.
- The prompt is hard to read in places, and burglary is too small (83 people) to say much.

### Launch the new refrigerated product line? (id 5a6e4e0c)

- **Domain and type:** Product Analytics; Forecasting & Predictive
- **Setup:** Household panel files and concept tests are used to forecast first-year net margin against an $18M bar.
- **Chain:**
  - (routine) Stack four panel files and two concept-test formats (duplicates, speeders, returns)
  - (judgment) Fit trial with separate conversion for category buyers and non-buyers, chosen by leave-one-out error
  - (judgment) Carry the buyer mix into volume: about half the buyers are new to the category, and new buyers buy about one unit (1.05 vs 4.17), so 2.6 units per buyer
  - (judgment) Estimate cannibalisation on comparable launches with a design that handles buyers' rising pre-launch trend: 51%
  - (routine) Combine into net margin and bootstrap over launches
- **What flips it:** Either the right volume or the right cannibalisation puts net margin below $18M. The runs used 4.2 to 4.7 units per buyer from a single analog launch.
- **Why this level:** Two independent places where the answer moves, each needing real modelling. Both runs built the buyer split for trial and then dropped it for volume.

**Prompt**

> Larkfield’s brand team wants to launch Fresh Rolls, our refrigerated dog food, with first shipments the week ending 7 March 2026. Finance will approve it only if it adds at least $18 million to our gross margin in its first 52 weeks on shelf, after whatever it takes from the lines we already sell. Northgate’s concept test came back at 57 percent top-two box, and they estimate 17 percent of dog-owning households will buy it in the first year.
> 
> Tell me how much gross margin the launch adds on the brand team’s distribution and awareness plan, with a range, and whether we should launch.
> 
> Put it in fresh_rolls_decision.docx, opening with the call and the net figure, then how many households buy it, how many rolls each buying household takes in the year, and how much margin comes out of our existing lines. Add a chart that walks from gross margin to the net figure. Include fresh_rolls_forecast.xlsx with the figures behind the memo.

**Input files**

1. panel_purchases_2018_2019 to 2024_2025.csv (4 files): household panel purchases in differing formats
2. panel_households.csv: panel households, including dog ownership and product types bought
3. product_master.xlsx: UPC to product line mapping
4. launch_calendar.csv: past launches and first ship weeks
5. concept_tests_2019_2022.csv and concept_tests_2022_2025.jsonl: past concept test responses in two agency formats
6. northgate_topline_fresh_rolls.xlsx: concept test topline for Fresh Rolls
7. brand_tracker_aided_awareness.xlsx: brand awareness tracker
8. acv_distribution_weekly.csv: weekly retail distribution (ACV) by line
9. fresh_rolls_launch_plan.xlsx: the brand team's distribution and awareness plan
10. gross_margin_by_line.xlsx: margin by product line
11. data_dictionary.md: field descriptions
12. bls_cpi_pet_food_2016_2025.csv and trade_promotions_2024_2025.csv: price index and promotions

**Reference solution**

Do not launch. Fresh Rolls adds about $11.6 million of net gross margin in its first 52 weeks (range $7.8 million to $14.6 million), below the $18 million bar. The reference solution stacks the four panel files, maps UPCs to lines, removes duplicate deliveries and nets returns. For 14 launches since 2020, first-year trial ran from 3.0% to 12.9% of households. It matches each launch to its concept test (removing speeders and duplicates) and to awareness and distribution. Fitting trial against intent with separate rates for people who already buy the product type (0.407) and those who do not (0.081) predicts past launches far better than one rate. Only 13.1% of Fresh Rolls respondents already buy fresh or refrigerated food, so trial is 4.56%, about 3.0 million of 66.1 million dog-owning households. One pooled rate would give 9.6%, and the agency's 17% is rejected. In past launches, buyers who already used the type bought 4.17 units in the year and others 1.05. With about half of buyers in each group, that is 2.61 rolls per buyer, not the 3.72 average. Gross margin is 3.0 million x 2.61 x $3.05 = $24.0 million. On the seven meal launches, before and after or against non-buyers comparisons show little cannibalisation, but buyers' spending was already rising. Two designs that handle that trend give 35% and 67%; the midpoint, 51%, removes $12.3 million, leaving $11.6 million. A bootstrap over the 14 launches gives the range.

**Deliverables:** fresh_rolls_decision.docx opening with the call and net figure, covering households, rolls per household and cannibalised margin with a walk chart, plus fresh_rolls_forecast.xlsx with the figures.

**Reviewers, good:**
- Several independent places to go wrong (pooled intent conversion, buyer mix carried into volume, trend-biased cannibalisation), each of which flips the call.
- Messy multi-source inputs: four panel formats, two concept test formats, speeders and returns.
- A routes sheet shows each shortcut's result, so the reasoning can be checked end to end.

**Reviewers, weak:**
- The data is synthetic, and the pattern for buyers new to the type is too clean (about one unit in every past launch).
- The cannibalisation figure is the midpoint of two quite different designs (35% and 67%).

### Fund the De Bilt telescope dome? (id 41389985)

- **Domain and type:** Physical & Environmental Sciences; Data Quality Monitoring & Alerting
- **Setup:** Real KNMI hourly weather records for De Bilt, 1961 to 2026. The funder pays only if 2016 to 2025 averaged at least 25% clear night hours, measured on the same basis as the 2006 to 2015 record.
- **Chain:**
  - (routine) Count night hours (zero global radiation) with cloud of 2 octas or less: 28.4% in 2006 to 2015, 20.8% in 2016 to 2025
  - (judgment) Test the drop against signals that did not change: daytime sunshine rose from 38.1% to 41.2% of daytime hours while reported clear daytime hours fell from 26.7% to 19.6%, and the gap opens in March 2016 (about -1.5 points a month before, -10.5 after)
  - (judgment) Fit a clear-sky model on 2006 to 2015 nights (night cooling, wind, humidity, dew-point depression, month) and apply it to 2016 to 2025: 30.4%
  - (judgment) Check nine training windows and predictor sets: 28.8% to 30.4%, every one above 25%
  - (routine) Report the rebuilt figure, not the raw one, and call go
- **What flips it:** Read straight from the cloud field, 2016 to 2025 gives 20.8%, a no-go. Rebuilt on the 2006 to 2015 basis it is 30.4% (28.8% to 30.4% across nine versions), so go.
- **Why this level:** One idea, a break in how cloud is measured, carries the answer, but turning it into a figure the funder will accept takes three connected steps: proving the break against independent signals, modelling clear sky from variables that did not change, and showing the result holds across versions. The one run flagged the instrument change as a risk but never tested it and reported the raw 20.8% as a no-go.

**Prompt**

> Our funder will only pay for a telescope dome on the pad next to the KNMI field in De Bilt if 2016-2025 averaged at least 25% clear night-time hours. Their rules: clear means total cloud cover of 2 octas or less (hours where the sky can't be seen count as not clear), night-time is any hour with zero global radiation, and the figure has to be comparable with the 2006-2015 record they approved the site on.
> 
> Go or no-go? I need a short memo with the decision and the figure we should report, and a workbook from the hourly data to every number.

**Input files**

1. knmi_hourly_260_debilt_1961_1970.csv to knmi_hourly_260_debilt_2021_2030.csv: seven decade files of KNMI hourly observations for De Bilt
2. knmi_uurgeg_260_header_legend_1961_2020.txt: field legend, with KNMI's warning that the hourly series may be inhomogeneous
3. knmi_uurgeg_260_header_legend_2021_2030.txt: field legend for the latest file
4. knmi_tr357_evaluatie_nederlandse_waarneemstations_2016.pdf: KNMI 2016 evaluation of Dutch observing stations
5. knmi_weercodes_nederland.pdf: present weather code list

**Reference solution**

Go. The figure to report for 2016 to 2025 is 30.4% clear night hours (28.8% to 30.4% across nine model versions), above the 25% bar. Read straight from the cloud field the share is 20.8%, a no-go, but that field changed basis in March 2016. The seven files hold 577,224 hours. Night is any hour with zero global radiation, clear is total cloud of 0 to 2 octas, and hours with the sky invisible (N = 9) or missing count as not clear. That gives 11,919 clear of 41,928 night hours in 2006 to 2015 (28.4%) and 8,608 of 41,459 in 2016 to 2025 (20.8%). The drop is not the weather: across the same two decades daytime sunshine rose from 38.1% to 41.2% of daytime hours while reported clear daytime hours fell from 26.7% to 19.6%. The monthly gap between reported and modelled clear share averages -1.5 points in the 24 months before March 2016 and -10.5 points in the 12 months after. A logistic model of clear sky on hour-to-hour temperature change, wind speed, relative humidity, dew-point depression and month, fitted on 2006 to 2015 nights, reproduces that decade at 28.4% and puts 2016 to 2025 at 30.4%. Nine variants (three training windows by three predictor sets) give 28.8% to 30.4%, each at least 3.7 points above 25%. By season, 2016 to 2025 runs 23.8% in October to March and 41.0% in April to September.

**Deliverables:** A short memo with the go or no-go call and the figure to report, plus a workbook that traces every number back to the hourly data.

**Reviewers, good:**
- Real, unaltered KNMI data: the break is a genuine feature of the station record, not a planted step.
- The raw and rebuilt figures fall on opposite sides of the 25% bar, so the key step decides the call.
- The correction needs real modelling and a robustness sweep, and every reasonable version clears the bar.

**Reviewers, weak:**
- The prompt's comparability rule and the legend's general warning point toward the break, so the idea is hinted.
- Once the break is accepted the go call is easy (the 2006 to 2015 baseline is 28.4% and sunshine rose); the remaining depth is in defending the figure.

### Bind the Bluebonnet legacy medical deal at $110 million? (id a5a5efb1)

- **Domain and type:** Actuarial Science & Insurance; Forecasting & Predictive
- **Setup:** Real Texas workers' comp billing data behind 25 old claims with lifetime medical. The desk binds only if $110 million is at least 110% of expected payments discounted at 4.0% with 3.5% medical trend.
- **Chain:**
  - (routine) Roll 236,427 bill rows up to paid by claim and year, net of reversals (71,003 legacy claims), and match the 25 scheduled claims
  - (routine) Value the schedule on the 2024 US life tables: $109M to $121M, a $120M to $133M requirement, so walk
  - (judgment) See that the 25 were picked because they are still paying, so their own records cannot show how often such claims stop
  - (judgment) Build a comparison group from the block: 104 claims paying $25K or more three years running, with 62 permanent stops against 8.9 expected deaths, an excess stop rate of 6.6 points a year
  - (judgment) Confirm the stops are durable (actual to expected 8.1, 7.1, 5.9, 7.0 by period; only 5 resumed) and add the excess on top of the age-rising table rate: $55.4M discounted
- **What flips it:** On the plain life table the requirement is $120M to $133M, a walk. With the block's measured stop rate it is $60.9M, a bind, and the call flips only below about 1.4 points of excess stop rate a year.
- **Why this level:** A few connected estimation steps carry the answer: spotting survivor selection, designing a comparison group that can measure stops, and choosing how the excess sits on the life table. Both runs priced on population mortality and walked; one built a small comparison group, but most of its claims were the scheduled survivors themselves, and it still kept no extra runoff in its central case.

**Prompt**

> The broker came back on Bluebonnet. The cedant will pay us $110 million to take all future medical on the 25 Texas comp claims in their Schedule A, all with injury dates before September 2011, for payments from January 1, 2027 on. No limit, no commutation, indemnity stays with them and they keep handling the claims. Our rule for legacy deals is that the premium has to be at least 110% of the expected payments discounted to closing at 4.0%, using the desk's 3.5% medical trend. Pricing committee meets Thursday and I need a straight answer: do we bind at $110 million or walk?
> 
> Their data room was thin, basically the schedule and their chief actuary's year-end memo, so I pulled every bill DWC has published on their pre-September 2011 claims, rolled it up by claim, paid year and bill type, and matched the schedule to the DWC claim numbers. Whatever else I had is in the folder. The tail is what worries me. These are the heaviest claims on the book, most of these people were hurt twenty or thirty years ago, and Texas medical runs for life.
> 
> I need a short memo the committee can get through in five minutes, and the workbook behind it. The workbook should let someone check the number claim by claim and show the expected payments by year for as long as they run, because treasury will ask for the pattern. Tell me the lowest premium the rule would let us accept, how far off your number could reasonably be, and what would have to be true for the answer to flip.

**Input files**

1. bluebonnet_schedule_a.csv: the 25 scheduled claims with injury date, birth month, sex and 2023 to 2025 medical paid
2. bluebonnet_indicative_terms.pdf: the deal terms
3. cedant_legacy_medical_reserve_review_ye2025.pdf: the cedant's year-end reserve memo
4. dwc_legacy_medical_paid_by_claim_year.csv: Texas DWC medical bills rolled up by claim, paid year and bill type
5. dwc_portal_dataset_descriptions.pdf: DWC dataset descriptions
6. dwc_pudf_data_dictionary.xlsx: DWC field definitions
7. us_life_table_2024_males.xlsx and us_life_table_2024_females.xlsx: 2024 US life tables by sex
8. nvsr75-05_us_life_tables_2024.pdf: report behind the 2024 life tables
9. treasury_par_yield_curve_2026.csv: Treasury par yields
10. bls_cpi_u_medical_care_2005_2026.csv: medical care CPI
11. oregon_wc_benefits_paid_by_year.csv: Oregon comp benefits paid by year

**Reference solution**

Bind at $110 million. Expected covered payments on the 25 claims from January 1, 2027 are $55.4M discounted ($82.0M undiscounted), so the lowest premium the rule allows is $60.9M, leaving $49.1M of headroom. Every reasonable reading of the block's history puts the value at $43.2M to $88.2M and the requirement at $47.5M to $97.0M, all binds. The DWC file (236,427 rows) rolls up to 71,003 legacy claims; all 25 scheduled claims match and all still pay in 2026. Valued on the 2024 US life tables, the cedant actuary's basis, they come to $109.0M to $121.0M, a $120M to $133M requirement and a walk. But the 25 were picked because they are still paying, so their own records cannot show stops. The comparison group is every block claim that paid at least $25K in three straight years, with the third year in 2012 to 2019: 104 claims and 808 claim-years, with 62 permanent stops against 8.9 expected deaths (actual to expected 7.0, excess 6.6 points a year; 3.1 points counting only years above $25K). The ratio holds by period (8.1, 7.1, 5.9, 7.0) and only 5 claims paid again after two quiet years. Stop rates rise with age, so the excess goes on top of the table rate. Each claim's 2023 to 2025 average cost is trended at 3.5%, decremented and discounted at 4.0% to give $55.4M. The call flips only at an excess of about 1.4 points a year.

**Deliverables:** A five-minute committee memo with the bind or walk call, the lowest acceptable premium, the range and the flip condition, plus a workbook with a claim-by-claim check and expected payments by year.

**Reviewers, good:**
- Real, messy administrative data (bill reversals, a 2020 gap in professional bills, unknown sex codes) has to be rolled up before any valuation.
- The deciding idea, survivor selection, is a genuine actuarial judgment that no file spells out; the cedant's memo uses the plain life table.
- The reference solution reports the full range and the flip point, so the strength of the call is clear.

**Reviewers, weak:**
- Once selection is seen the bind is wide: even the top of the range ($97.0M) is well under $110M, so the later shape and range choices refine the figure more than the call.
- The comparison group keeps 21 scheduled claims, a cautious choice that a solver could reasonably make differently.

## Level 5: Difficulty throughout

### Does the state's job-openings rate clear 4.0? (id bd4981a5)

- **Domain and type:** Survey Research & Official Statistics; Descriptive & Distribution
- **Setup:** A contractor's employer survey reports a 3.00 rate. The fund rule pays out at 4.0 or above, measured over all employers covered by unemployment insurance.
- **Chain:**
  - (judgment) Reproduce 3.00 and see that pooling the nonresponse follow-up with first-wave answers under-represents the follow-up group
  - (judgment) Build two-phase weights for the one-in-three follow-up subsample, screening out-of-scope employers with UI records: 3.70
  - (routine) Reconcile the survey frame with the rule's scope: 2,700 accounts joined after the frame was drawn
  - (judgment) Choose how to impute openings for those new accounts: young-employer ratios, not size-class averages
  - (judgment) Bootstrap within strata, repeating every step, and run the sensitivities
- **What flips it:** No single correction clears 4.0. Weighting alone gives 3.70; new accounts at size-class averages give 3.88; both, done right, give 4.42.
- **Why this level:** Three separate judgments each move the figure, and shortcuts land at 3.00, 3.62, 3.70, 3.88 or 3.90. The run did the weighting and then declined to add the new employers.

**Prompt**

> "I'm about to sign a number that keeps the grant round shut for a year, so I'd like somebody besides the contractor to tell me it's right." (our LMI director, Tuesday)
> 
> Every November we certify the Q2 job vacancy rate to the Workforce Opportunity Fund board, and if it's under 4.0 percent the training grant round doesn't open the next fiscal year. The contractor that runs the survey has Q2 2025 at 3.0 percent, so as things stand there's no FY2027 round. The director wants our own number from the Q2 files the contractor sent over before she signs anything, and the board meets in two weeks.
> 
> When she walks into that meeting she'll be holding a page or two from us, vacancy_rate_memo.docx, and the first thing it needs to tell her is whether the rate clears 4.0, then what rate to certify and how much room there is around it, and why it isn't 3.0 if it isn't. The board's analysts will check her figure, so it has to be traceable all the way through in vacancy_rate_workbook.xlsx.

**Input files**

1. jvs_responses_q2_2025.csv: survey responses with openings, employment and collection phase
2. jvs_sample_dispositions_q2_2025.csv: every sampled case with its disposition and follow-up flag
3. ui_employer_sampling_frame_q1_2025.csv: the February 2025 employer sampling frame
4. ui_quarterly_contribution_reports_2024q3_2025q2.csv: unemployment insurance employer reports by quarter
5. jvs_vendor_methodology_q2_2025.html: the contractor's method note
6. workforce_fund_trigger_rule.txt: the 4.0% rule and which employers it covers
7. jvs_published_estimates_prior_quarters.csv: previously published rates
8. cbp2023_county_business_patterns_illinois.csv: county business patterns
9. census_naics_2022_codes_2_to_6_digit.xlsx: industry code list
10. ers_county_unemployment_median_household_income_2000_2023.xlsx and usda_rural_urban_continuum_codes_2023.xlsx: county background data

**Reference solution**

The rate clears 4.0, so the grant round opens: certify 4.42%, with a 90% range of 4.21 to 4.70, and none of 500 resamples falls below 4.0. The contractor's 3.00% reproduces from its own weights, which pool both collection phases and adjust for nonresponse within region only. The first correction is two-phase weighting. There were 2,973 first-phase completes and 4,629 first-phase refusals and no-contacts; 1,574 of those were picked at random for follow-up and 800 completed. The follow-up completes stand for all first-phase nonrespondents, so they are weighted up rather than pooled; they carry about 55% of the weighted respondents against about 22% under pooling. Inside the follow-up group, 384 field-confirmed closures and 62 nonrespondents with no 2025 employment are removed. Frame employers then come to 3.70%. The second correction is coverage. The rule covers all employers, but 2,700 accounts that started reporting after the frame was drawn are missing, with 28,716 June jobs. Their openings are imputed from the youngest sampled employers (liable four quarters or less), with ratios of 0.53, 0.32 and 0.07 by size, about 10,550 openings, which lifts the rate to 4.42%. Neither correction is enough alone: pooled phases with the new accounts give 3.90%, and size-class average ratios give 3.88%. A bootstrap within strata that repeats every step gives the 4.21 to 4.70 range.

**Deliverables:** vacancy_rate_memo.docx (a page or two: whether the rate clears 4.0, the rate to certify with its range, and why it is not 3.0) and a fully traceable vacancy_rate_workbook.xlsx.

**Reviewers, good:**
- Two independent method corrections are both needed; either one alone stays under 4.0.
- A realistic survey design (follow-up subsample, frame drawn months earlier) of the kind real labour market offices face.
- The workbook traces every sampled case and every imputed account, so the figure is fully checkable.

**Reviewers, weak:**
- The data is constructed.
- The new-account imputation (young employer ratios against size-class averages) is a modelling judgment, and the alternative lands just under the line at 3.88%.

### Renew the street patrols in full, by half, or stop? (id 4e9c0a39)

- **Domain and type:** Criminology & Justice; Experiment & Causal
- **Setup:** 58 street segments got patrols in 2025. Funding bands depend on the crime reduction against a no-patrol counterfactual, at 5% and 15% lines.
- **Chain:**
  - (judgment) Segments were picked on their 2024 counts, a peak year, so use 2022 to 2023 as the baseline
  - (judgment) Take the comparison trend only from untouched segments, leaving out the 211 that share an intersection with a patrol
  - (judgment) Robbery rose 35% and assault fell 12% away from patrols, and patrolled segments are 71% robbery, so build the counterfactual offence by offence
  - (judgment) Net out the 80.4 incidents displaced to adjacent segments, because the rule counts the whole city
  - (routine) Check base years, strata, control groups and buffer rings: all stay in the half-renewal band
- **What flips it:** Each step moves the estimate. A single pooled crime trend, the shortcut both runs took, turns half renewal into stop.
- **Why this level:** Four independent judgments: selection, contamination, mix and displacement. The runs handled the baseline and displacement well and lost on the offence mix.

**Prompt**

> Council funded the street patrols for one year and set the terms for a second. If the patrols cut street violence in the city by at least 15% of what the patrolled segments would otherwise have had from March to December 2025, we renew in full. If the cut is at least 5% but under 15%, we renew at half the budget. Under 5%, the patrols stop. The police board's report says street violence on the patrolled segments fell by a third over those months compared with the year before. The renewal vote is in March and I need to know which of the three it is.
> 
> Send me patrol_review.xlsx with the street violence incidents on the patrolled segments for March to December of 2024 and of 2025, the number you expect they would have had in 2025 without the patrols, how many incidents the patrols prevented across the city, and that number as a share of the expected figure, to one decimal. Add a sheet with the month by month counts on the patrolled segments for both years and a chart of them.
> 
> Then write funding_note.docx, one page, with the call, the figures it rests on, and how far the prevented number is from the nearest of the two lines in incidents, either way.

**Input files**

1. omp_incidents_2022_2023.csv and omp_incidents_2024_2025.csv: incident records with different column names, date formats and versions
2. offence_code_schedule.xlsx: offence codes, including the six street violence codes
3. street_segment_register.csv: street segments with intersection node ids and beats
4. street_patrol_roster_2025.xlsx: the patrolled segments
5. street_patrol_selection_note.docx: how the segments were picked
6. omp_calls_for_service_2024_2025.csv: calls for service
7. monthly_recorded_offences_2024_2025.pdf: published monthly recorded offences
8. residents_by_beat_2024.xlsx: residents by beat
9. extract_notes.txt: notes on the data extract

**Reference solution**

Renew at half the budget. The patrols prevented about 84.0 street violence incidents across the city from March to December 2025, 10.2% of the 823.4 the patrolled segments would otherwise have had. The reference solution joins the two incident files, keeps the latest version of each incident and the six street violence codes, and counts by date of occurrence. The 58 patrolled segments had 999 incidents in 2024 and 659 in 2025, the 34% fall the police board reported. But the segments were picked on their 2024 counts, and their beats peaked that year, so 2024 is an inflated baseline. The reference solution uses the 2022-23 average, 680.0 (683 and 677). The 211 segments that share an intersection with a patrolled segment are kept out of the comparison group. Away from the patrols, robbery rose 35.0% and assault fell 12.1%, and the patrolled segments are 71% robbery against 20% elsewhere. Carrying each type forward separately gives 647.1 robbery and 176.3 assault, 823.4 expected, so 164.4 were prevented on the patrolled segments. The same method on the 211 neighbouring segments gives 825 recorded against 744.6 expected: 80.4 incidents moved next door. Net prevented is 84.0. That sits 42.8 above the 5% line (41.2) and 39.5 short of the 15% line (123.5), the nearer line. A single trend for all street violence would give 663.3 expected and a call to stop.

**Deliverables:** patrol_review.xlsx with the counts, expected figure, prevented incidents and share, plus a monthly sheet and chart, and a one-page funding_note.docx with the call and the distance to the nearest line.

**Reviewers, good:**
- Three independent judgment points: the selection-year baseline, the offence mix shift and displacement next door.
- Messy inputs: two incident files with different formats and incident versions.
- A clear rule with thresholds, and careful variants all land in the same band.

**Reviewers, weak:**
- The data is constructed, and the citywide robbery surge at the start of the patrols is a built-in hidden factor.

### Which territory gets the January win-back vouchers? (id 17adb5ca)

- **Domain and type:** Product Analytics; Opportunity Sizing & Decision Support
- **Setup:** Each territory would send vouchers to its 2,500 highest-risk lapsed shops. Pick the territory with the highest expected margin, using a summer trial.
- **Chain:**
  - (routine) Build each shop's 56-day trial margin by assigned arm
  - (judgment) Own-territory trial effects are confounded by customer mix, so estimate the voucher effect by group and lapse band and transport it
  - (judgment) Age the picks 70 days to the send date, where the kiosk effect has faded to near zero
  - (judgment) The picks are the riskiest shops in each cell, so model no-reorder on the holdout with the risk score
  - (judgment) Shift the summer reorder hazard to November by a factor calibrated on the November list
  - (routine) Sum, rank and test 11 variants: the same territory leads by 16%
- **What flips it:** Four different shortcuts each name a different territory. Network November rates applied to the picks name the wrong one.
- **Why this level:** Five real judgments in a chain, each with its own tempting shortcut. Both runs did most of the chain and applied network rates to the high-risk picks as an untested assumption.

**Prompt**

> Planning for January closes soon and the budget covers one win-back voucher run. One territory gets it, and it can go to 2,500 shops at most, picked off the November at-risk list. Tell me which territory should get it and what extra margin to expect.
> 
> I need winback_q1_pick.xlsx listing every territory with roughly how many shops its run would actually be sent to, what extra margin it should bring to the nearest ₦100,000, and where it ranks.
> 
> Also write winback_q1_note.docx, one page, giving the territory you'd fund, the margin and the number of shops you expect its run to be sent to, and the margin the voucher added per shop sent in that territory's May to June trial list, to the nearest ₦100.

**Input files**

1. next_quarter_atrisk_list.csv: the 2 November at-risk list with risk scores and days since last order
2. winback_trial_list.csv: the May to June trial list with voucher and holdout arms
3. order_lines_export_A.csv and order_lines_export_B.csv: order lines in two overlapping exports
4. order_export_fields.txt: field notes for the order exports
5. retailer_master.csv: shops with territory and customer group
6. sku_cost_list.xlsx: unit costs by product code
7. territories.xlsx: territory names and codes
8. winback_run_rules.docx: run rules (selection, cap, margin definition, window)
9. trade_kpi_pack_2023_2026.pdf: trade KPI pack, including the November restock pattern
10. trial_weekly_readout.pdf: weekly trial readout
11. voucher_terms.pdf and atrisk_list_notes.txt: voucher terms and notes on the at-risk list
12. van_route_calendar.xlsx: van route calendar

**Reference solution**

Fund Ekiade. Its run should be sent to about 2,042 shops and bring about ₦3,000,000 of extra margin. In its own May to June trial list the voucher added ₦2,400 per shop sent. The reference solution builds each trial shop's margin over the 56 days from its SMS from delivered orders, counting the overlap between the two exports once, matching shop codes on their digits and costing the July pack codes. Scaling each territory's own trial result by its shops would name Ilesowo, but each trial list has a different mix from its November picks. So the effect is pooled by customer group and lapse band: kiosks fall from ₦5,404 at 30 to 59 days to ₦113 at 150 to 179 days, while provision stores and mini-marts hold at ₦2,264 and ₦2,494 even at 210 to 239 days. Each territory's 2,500 highest-risk shops are taken from the November list and aged 70 days to the 11 January send. A survival model on the trial holdout shows the risk score strongly predicts no reorder within each group (coefficient about -1.0), and it is shifted to the November restock season by calibrating to all 48,261 shops on the list. Ekiade's picks are the riskiest 24% of its 10,500 shops, so far more stay unordered (72.4% against 29.6% network for provision stores lapsed 30 to 89 days): 2,042 sent, against 1,466 at network rates. Arogunle follows at ₦2,400,000. Eleven variants keep Ekiade first at ₦2,800,000 to ₦3,000,000, at least 16% clear.

**Deliverables:** winback_q1_pick.xlsx listing every territory with shops sent, extra margin and rank, and a one-page winback_q1_note.docx with the pick, its margin, shops sent and its trial margin per shop.

**Reviewers, good:**
- A real multi-step causal problem: pooling the trial effect, ageing the picks, moving summer behaviour to the restock season and accounting for risk selection.
- Four different shortcuts each name a different territory, so every step matters.
- Messy order data (overlapping exports, inconsistent codes, new pack codes) that has to be cleaned before any margin is right.

**Reviewers, weak:**
- The data is constructed, and the strong risk gradient is a built-in feature, though it runs across the whole network.
- The decisive step is a modelling choice (a survival model plus a seasonal shift) that solvers can build in more than one way, although eleven variants agree on the pick.

### Launch the short-term SBA loan, and at what sizes? (id b9efebd1)

- **Domain and type:** General Statistics & Data Science; Forecasting & Predictive
- **Setup:** Real SBA 7(a) loan-level FOIA data. Each version (all loan sizes, or over $50,000 only) launches only if its four-year charge-off share stays under the 6.50% limit.
- **Chain:**
  - (routine) Keep funded 7(a) term loans of 60 months or less approved FY2020 to FY2024: 17,922 loans, 6,994 over $50,000, with 4,522 still open short of four years
  - (judgment) Treat payoff as a competing event, not censoring: 1 minus Kaplan-Meier gives 9.45% and a hold
  - (judgment) Split by approval year: four-year shares of 2.70% (FY2020), 2.88% (FY2021) and 8.99% (FY2022); at the same loan age and calendar half years the newer years run 1.56 times the older rate
  - (judgment) See why one pooled curve reads low (6.25%): 61.8% of the loan time at months 36 to 48 comes from FY2020 and FY2021
  - (judgment) Complete FY2023 and FY2024 past their last observed day from FY2022 onward rates (12.50% and 10.12%) instead of leaving them at no risk (6.04%)
  - (routine) Loan-weight the five years: 7.09% at all sizes (fails), 5.54% over $50,000 (passes)
- **What flips it:** Each shortcut gives a different wrong call: the pooled curve at 6.25% launches all sizes, and treating payoff as censoring (9.45%) holds the product. Per-year curves put all sizes at 7.09% and over $50,000 at 5.54%: launch over $50,000 only.
- **Why this level:** Several independent modelling choices (the competing-risk estimator, the vintage split, the composition of late-age loan time, the completion of young years) each move the share across the limit, and the call holds under six other completion methods (6.65% to 7.54% at all sizes). Both runs got the competing-risk estimator right but pooled all five years, read about 6.2% and launched at all sizes, naming vintage drift only as an untested assumption.

**Prompt**

> We're looking at adding a short term SBA 7(a) term loan at Kestrel Point next year, and before credit committee will even look at pricing it has to clear the four year charge off test in 4.3 of our risk appetite statement. Renata's email in the folder sets out how 4.3 applies to this product, and Marcus's reply has the two versions we'd take in. Committee sits on 3 December and wants one call from me: launch at all loan sizes, launch for loans over $50,000 only, or hold the product back.
> 
> Could you put together three files for the committee pack? A Word memo that leads with the call and gives each version's four year charge off share and how far it sits from the 6.50% limit. A PNG chart of the cumulative share charged off against months since first disbursement out to 48 months, one line per version, with the limit drawn on and each version's four year figure marked. And an Excel workbook with the numbers behind both, so Renata's team can check them (shares to two decimals, expected loan counts to one).
> 
> Committee will ask three more things, so please answer them in the memo and put the detail in the workbook. A good number of the comparable loans are still open and haven't had four years yet: how many of them should we expect SBA to charge off before they get there, version by version? How do the comparable loans compare with the same kind of loan approved FY2016 to FY2018, version by version? And if your call is a launch, how many of the loans Treasury's 2027 plan has for that version should we expect SBA to have charged off by 31 December 2030, worked on the same footing as the 4.3 figure? I'd like that by funding month as well as the total.

**Input files**

1. FOIA_7a_FY2020_Present_asof_260930_term60.csv: SBA 7(a) loans approved FY2020 on, terms of 60 months or less
2. FOIA_7a_FY2016_FY2018_asof_260930_term60.csv: the same loan type approved FY2016 to FY2018
3. FOIA_504_FY2022_FY2024_asof_260930.csv: SBA 504 loans, FY2022 to FY2024
4. 7a_504_foia_data_dictionary.xlsx: SBA FOIA field definitions
5. RAS 4.3 for the short term term loan (December committee).eml: email setting out how test 4.3 applies to the product
6. RE RAS 4.3 for the short term term loan (December committee).eml: reply with the two versions
7. 2027 Volume Plan - ST Term Loan v3.xlsx: Treasury's 2027 funding plan by month
8. SOP 50 10 8.1 Technical Policy Updates effective 10.1.2026.docx: SBA lending policy updates
9. SBA OIG Report 26-12 - SBA's 7(a) Loan Guaranty Purchase Denial Review Process.pdf: inspector general report on purchase denials
10. SBA OIG Report 26-14 - Small Business Lending Companies Performance in the 7(a) Loan Program.pdf: inspector general report on lender performance

**Reference solution**

Launch for loans over $50,000 only. The four-year charge-off share is 7.09% at all loan sizes, 0.59 points over the 6.50% limit, and 5.54% over $50,000, 0.96 points under. In the 30 September 2026 release, 20,771 7(a) term loans of 60 months or less were approved FY2020 to FY2024; dropping cancelled and undisbursed loans and 4 undated charge offs leaves 17,922, 6,994 over $50,000. Each loan is timed from first disbursement to charge off (the event), payoff (a competing event) or the cutoff; 4,522 are still open short of four years. One pooled Aalen-Johansen curve reads 6.25% and 4.81%, which would launch at all sizes. Per approval year the four-year shares are 2.70% (FY2020), 2.88% (FY2021) and 8.99% (FY2022), and at 36 months FY2023 was already at 6.46% against 1.33% for FY2020. At the same loan age and calendar half years, FY2022 to FY2024 loans had 121 charge offs against 77.5 expected at the older rates. The pooled curve is low because 61.8% of the loan time at months 36 to 48 belongs to FY2020 and FY2021. Completed from FY2022 onward rates, FY2023 and FY2024 reach 12.50% and 10.12% at all sizes. Loan-weighting gives 7.09% and 5.54%; other completions give 6.65% to 7.54% and 5.11% to 6.17%, the same call. For the follow-ups: 359.2 expected charge offs among the 4,522 open loans (111.7 of 1,666 over $50,000), 4.37% and 4.02% for FY2016 to FY2018, and 8.3 expected charge offs by 31 December 2030 among the 197 planned loans over $50,000.

**Deliverables:** A Word memo leading with the call and each version's four-year share against 6.50%, a PNG chart of cumulative charge-offs to 48 months, and an Excel workbook with the figures, open loans, FY2016 to FY2018 comparison and 2027 plan.

**Reviewers, good:**
- Real SBA FOIA loan-level data with genuine quirks (exact repeat rows, undated charge offs, payoffs dated before disbursement).
- Several independent choices each move the answer, and the shortcuts land on different wrong calls (launch all sizes, or hold).
- The follow-up questions on open loans, older vintages and the 2027 plan test that the completed curves are actually used, not just read at 48 months.

**Reviewers, weak:**
- The margin is thin for all sizes: the robustness range bottoms out at 6.65%, only 0.15 points over the limit.
- The deliverable is heavy (memo, chart, workbook and three follow-ups), so much of the work sits away from the deciding step.

### Which fourteen days should the borrowed Pit 2 crew work? (id 279e74f2)

- **Domain and type:** Economics & Econometrics; Opportunity Sizing & Decision Support
- **Setup:** Constructed scale tickets, gate camera reads and Pit 2 logs from three harvests at a co-op grain elevator. The board judges the fourteen-day block by margin kept on grain that would otherwise go to a rival elevator, at 22.6 cents a bushel.
- **Chain:**
  - (routine) Stack the two ticket exports, drop voids and tests, and match each load to its approach-camera read for line time: 42,816 loads, 96.2% matched
  - (judgment) Flag diversion from each truck's own return gap (more than 1.6 usual turnarounds, loads finished by 3:30 p.m.): 2.295 lost loads per diversion
  - (judgment) Find that the response is a step at about 60 minutes: 15.1% of loads followed by diversion below the hour, 30.7% above, flat out to three hours
  - (judgment) Set aside past Pit 2 hours and observed lines: Pit 2 was opened on busy days, so they only measure busy days
  - (judgment) Replay each harvest day with Pit 1 alone and with Pit 2 ten to six, carrying unload times by the pits' mean ratio (4.57 and 7.66 minutes): mid-October lines stay at 4.4 to 4.7 hours, early November falls from 159 to 204 minutes to 28 to 49
  - (routine) Score all 48 possible blocks: the best starts Thursday, November 5
- **What flips it:** Mid-October has the longest lines, but even two pits leave them past the hour, so that block keeps only 13,703 a harvest. Early November is where the second pit pulls the line under the hour: about 123,036, with every defensible reading between about 112,000 and 132,000 and starting November 3 to 7.
- **Why this level:** Several independent estimates (the diversion definition, the step shape, the confounded Pit 2 history, the two-pit replay with pit-specific unload times) each move the block or its value; a smooth response or ranking by truck-hours picks mid-October, while ignoring the unload-time ratio moves the start and cuts the value to about 95,000. Both runs assumed a diversion response instead of measuring it and booked October 16 to 29, a mid-October block like the manager's plan.

**Prompt**

> Halden Feed Mill can lend us two people to run Pit 2 at Pell Junction for the 2026 harvest. They would work ten to six for fourteen days in a row, any fourteen we pick. Without them Pit 2 stays shut all harvest, because the call list is gone. Corinne wants them in the middle of October, when the line is longest. The board books the dates on February 10. It will judge them by the margin kept on grain that would otherwise go to Bracken Ridge, at the division's margin per bushel, in a harvest like the last three. Which fourteen days should we book?
> 
> I want a brief memo the directors can read at the table, in Word or PDF, carrying a single chart. It should name the dates and say what those fourteen days are worth to the co-op in a typical harvest. Corinne's mid-October plan needs the same figure, since she will put it to the board.
> 
> Nolan will rebuild every figure before the meeting, so the work should sit in an Excel workbook he can follow from the scale tickets.

**Input files**

1. scale_tickets_2023_2024.csv and ticket_export.sql: old scale system tickets for 2023 and 2024, with the query that exported them
2. fieldgate_tickets_2025.csv: 2025 tickets from the new scale system
3. gate_lpr_reads_2023_2025.csv: approach-camera plate reads
4. pit2_log_2023_2025.xlsx: when Pit 2 started and stopped taking trucks
5. patron_list_2025.csv: member accounts, haul miles and plates on file
6. halden_mill_crew_offer_2026.docx: the feed mill's offer of a two-person crew
7. board_minutes_2025-12-16.docx: board minutes on the 2026 harvest
8. pj_harvest_review_2025.pdf: the location's 2025 harvest review
9. tvgc_annual_report_fy2025_grain.pdf: grain division annual report with margin per bushel
10. cash_bids_2023_2025.xlsx: posted cash bids at both elevators
11. dryer_hourly_2025.csv, shuttle_loadings_2023_2025.csv and harvest_weather_2023_2025.csv: dryer, rail loading and weather records
12. pj_site_plan.png: site plan of the elevator

**Reference solution**

Book Thursday, November 5 to Wednesday, November 18, 2026. In a harvest like the last three the block keeps about 605 loads, 544,405 bushels and 123,036 of margin; the mid-October plan (October 12 to 25) keeps 67 loads and 13,703, about a ninth as much. The two ticket exports clean to 42,816 loads, and 96.2% match an approach-camera read, which gives each load's line time. Mean unload time is 4.57 minutes at Pit 1 and 7.66 at Pit 2. A load counts as followed by diversion when the same truck's next arrival came more than 1.6 usual turnarounds later, or never came while the account kept delivering, using loads finished by 3:30 p.m.; each flagged gap means 2.295 missing loads. The diversion share is 15.1% below 60 minutes and 30.7% above, a step rather than a slope. Past Pit 2 hours cannot price the crew, because Pit 2 opened when the line was long. Replaying every harvest day in arrival order, weeks 4 and 5 average 7.6 to 8.0 hours with Pit 1 alone and still 4.4 to 4.7 hours with both pits, while early November falls from 159 to 204 minutes to 28 to 49. Each of 48 blocks is scored by the fall in diversion share times 2.295 loads, 899.1 bushels a load and 22.6 cents a bushel, averaged over three harvests. Other gap, cutoff and break readings keep the start between November 5 and 7 and the value between about 112,000 and 132,000. Ranking by truck-hours saved would pick October 16 instead.

**Deliverables:** A brief memo for the directors (Word or PDF, one chart) naming the dates and their value against the mid-October plan, plus an Excel workbook that rebuilds every figure from the scale tickets.

**Reviewers, good:**
- The answer needs a measured behavioural response and a queue replay; neither is in any document.
- The obvious routes (longest lines, truck-hours saved, past Pit 2 hours) all point to mid-October, and the replay shows why they are wrong.
- The reference solution sweeps the diversion gap, end-of-day cutoff, break point and calendar alignment, and the early-November answer holds throughout.

**Reviewers, weak:**
- The data is constructed, and the response is a clean step at a round 60 minutes, which reads like a generator setting.
- The exact first day is soft: starts from November 3 to 7 are all within about 6% of the best, so the decision is the early-November block rather than one date.
