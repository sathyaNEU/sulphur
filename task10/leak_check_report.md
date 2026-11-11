# leak check, task10

**Verdict: REVIEW.** 14 files read, 82 golden figures and 13 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: street, architecture, record, golden, fenwick, megawatts, register, guideline, dunmore, charlecote, primary, come-back, schedule, careful, carried, prompt, missed, forecast, carries, half-hour, january, months, inside, provider, delivered

## 3 answer figures in the pack (REVIEW 11)
- **REVIEW** `capacity_assessment_guideline_2026.pdf`: golden figure 27.5 appears: ...Firm capacity (MW) Ashcombe Road PS40617 24 + 24 27.5 Charlecote Way PS41108 22 + 22 25.6 Dunmore Stree...
- **REVIEW** `capacity_assessment_guideline_2026.pdf`: golden figure 35.0 appears: ...40852 20 + 23 20.0 Fenwick Street PS41474 30 + 30 35.0 Hartwell Common PS41236 21 + 21 24.4 Kestwick Fie...
- **REVIEW** `capacity_assessment_guideline_2026.pdf`: golden figure 20.0 appears: ...41108 22 + 22 25.6 Dunmore Street PS40852 20 + 23 20.0 Fenwick Street PS41474 30 + 30 35.0 Hartwell Comm...
- **REVIEW** `capacity_assessment_guideline_2026.pdf`: golden figure 25.6 appears: ...40617 24 + 24 27.5 Charlecote Way PS41108 22 + 22 25.6 Dunmore Street PS40852 20 + 23 20.0 Fenwick Stree...
- **REVIEW** `capacity_assessment_guideline_2026.pdf`: golden figure 24.4 appears: ...1474 30 + 30 35.0 Hartwell Common PS41236 21 + 21 24.4 Kestwick Fields PS40508 17 + 17 19.5 Ravenhurst P...
- **REVIEW** `capacity_assessment_guideline_2026.pdf`: golden figure 27.0 appears: ...PS40233 23 + 23 26.0 Wexley Hill PS40975 24 + 24 27.0 Transformer ratings from the primary substation r...
- **REVIEW** `capacity_assessment_guideline_2026.pdf`: golden figure 100 appears: ...s on record show them, by drawing not fewer than 100,000 design days; the assessment's own estimates (...
- **REVIEW** `flexibility_contract_awards_2027-28.pdf`: golden figure 2.0 appears: ...3.0 3.5 4.0 Hartwell Common CMZ Corvane Flex Ltd 2.0 2.5 3.0 3.5 The service has run at these zones si...
- **REVIEW** `flexibility_contract_awards_2027-28.pdf`: golden figure 5.0 appears: ...0 6.0 Dunmore Street CMZ Corvane Flex Ltd 3.0 4.0 5.0 5.5 Fenwick Street CMZ Quillon Energy Services Lt...
- **REVIEW** `flexibility_contract_awards_2027-28.pdf`: golden figure 3.5 appears: ...ntract period on the contracted megawatts for the 3.5 hours of the service window. Utilisation is paid...
- **REVIEW** `capacity_assessment_guideline_2026.pdf`: carries 46 of 65 distinctive words of the committed call: 'Commit reinforcement at Ashcombe Road, Charlecote Way, Dunmore Street and Fenwick Street for winter 2027/28 and hold Har'

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `capacity_assessment_guideline_2026.pdf`: 14 of 25 stump-paragraph terms appear (street, record, fenwick, megawatts, register, guideline); read whether the document names the move
- **REVIEW** `flexibility_contract_awards_2027-28.pdf`: 11 of 25 stump-paragraph terms appear (street, fenwick, megawatts, register, dunmore, charlecote); read whether the document names the move

## 6 ranking artifacts (REVIEW 6)
- **REVIEW** `capacity_assessment_guideline_2026.pdf`: names 5 of 13 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `flexibility_asset_register_2026-11-04.csv`: names 5 of 13 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `flexibility_contract_awards_2027-28.pdf`: names 5 of 13 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `flexibility_events_2023-2026.csv`: names 5 of 13 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `primary_substation_register.xlsx`: names 5 of 13 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `primary_transformer_condition_2026.xlsx`: names 5 of 13 answer-set candidates beside numbers; confirm it does not rank them on the decision question

## 9 dates after the setting (INFO 1)
- **INFO** `-`: no --asof given, sweep skipped (pass the fiction's as-of date)

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 12 client quality check (INFO 2)
- **INFO** `-`: 14 usable files (10 or more required)
- **INFO** `-`: 2 file categories: document, spreadsheet (2 or more required)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)


## Solver's-eye read

Isolated reader (general-purpose, Sonnet, medium), 2026-11-10, on the levelled-up cut (target.zip sha256 15f8ba39...), reading only a fresh copy of prompt.txt and target/:

## 1. Which sentence or file tells you how any part of the analysis should be done?

The whole body (sections 1-7) of **capacity_assessment_guideline_2026.pdf** is written as a step-by-step method, not just a reference table. The single most load-bearing "how" sentence is in section 7, on the hardest figure in the prompt (the probability of exceeding firm capacity):

> "capacity_assessment_guideline_2026.pdf": "The one day in ten and the share are taken over those three variations together, as the primary's working weekdays and the provider's completed events of the three winters on record show them, by drawing not fewer than 100,000 design days; the assessment's own estimates (design-day demand, what the customers add, the megawatts in service and the share of them available) are held at their central values."

This names the method (a resampling/Monte Carlo draw over historical realisations), the minimum sample size (100,000), which inputs are held fixed (demand, connections growth, MW in service, share available), and which three things are allowed to vary. Other sentences in the same file fix other steps just as literally:

- "capacity_assessment_guideline_2026.pdf": "by the same proportion in every half-hour of the day" (section 7) - fixes the demand-variation day factor as multiplicative and uniform across the day.
- "capacity_assessment_guideline_2026.pdf": "whatever the day's demand" (section 7) - fixes delivery availability as independent of demand level.
- "capacity_assessment_guideline_2026.pdf": "the load that comes back after a window varies from one evening to the next" (section 7) - names the rebound mechanism outright rather than leaving it to be discovered from the demand series.
- "capacity_assessment_guideline_2026.pdf": "whichever half-hour that falls in" (section 6) - tells the reader the peak-with-flexibility can land in a different half-hour than the unconstrained peak.
- "capacity_assessment_guideline_2026.pdf": "A contract's megawatts delivered are quoted as its mean delivery in the half-hours ending 17:30 and 18:00." (section 6) - fixes the averaging window for delivered MW.

See Q5 and Q6 for how literally these pin individual graded figures, and for what is **not** fixed by them.

## 2. Which file already ranks or scores the candidates on the prompt's question?

None. No file contains a column or table that orders, scores, flags or ranks the primaries by exceedance risk, MW shortfall, or reinforcement priority. Every file supplies only raw inputs (fixed ratings, contract terms, site logs, meter/weather series); the comparison across the five constraint-managed-zone primaries has to be built by the analyst from the demand, weather and flexibility data together. (Appendix A of capacity_assessment_guideline_2026.pdf lists all nine primaries in plain alphabetical order with a static capacity rating, which is not a ranking on this question; see sweep item d.)

## 3. Which file exists only to help the analyst?

**capacity_assessment_guideline_2026.pdf**, with a caveat. Sections 1-7 (everything except Appendix A) carry no primary-specific demand, growth or contract figures of their own; they exist purely to tell the analyst how to read and combine the other files (definitions of design day, firm capacity, demand before/with flexibility, the Monte Carlo spec). Section 7 in particular reads as though it is addressed to whoever builds a simulation, not as a record of a business fact. Appendix A is the exception: it is itself required data (the firm-capacity MW column is a direct input the prompt asks for), so the file as a whole is not purely a "helper" document, only its body text is. "None" would also be a defensible answer if the question means a file that carries no business content anywhere in it, since even this file's appendix is real data.

## 4. Which figure or name reads as the answer rather than context?

None of the figures or names states an outcome of the capacity question. The closest near-miss is the **Health index** column (HI2-HI5) in `primary_transformer_condition_2026.xlsx`: four of the five constraint-managed-zone primaries (Ashcombe Road, Charlecote Way, Fenwick Street, Hartwell Common) each carry at least one HI5 transformer, while the primaries without a flexibility contract that appear in this sheet (Tollbrook Lane, Ravenhurst Park, Kestwick Fields, Wexley Hill) carry only HI2-HI4. A hurried reader could mistake worst asset condition for the reinforcement signal, but section 5 of the guideline ties firm capacity to a fixed Appendix A rating, not to condition, so this is a plausible-but-wrong signal, not an answer.

## 5. Which filed sentence, read literally, fixes how a graded figure is computed or over which population?

Two sentences pin a figure's computation cleanly:

> "capacity_assessment_guideline_2026.pdf" (section 6): "A contract's megawatts delivered are quoted as its mean delivery in the half-hours ending 17:30 and 18:00."

Literal result: the prompt's own figure "the MW its contract can be expected to deliver between 17:00 and 18:00" is fixed to be the average of exactly two half-hourly delivered-MW values (the half-hour ending 17:30 and the one ending 18:00); nothing else in the hour counts toward that particular number.

> "capacity_assessment_guideline_2026.pdf" (section 3): "A primary's design-day demand is its half-hourly demand (MW, the SCADA total of its transformer secondaries) on the design day with no flexibility service delivered and with the network in its normal running arrangement, no load transferred to or from the primary across a normally open point."

Literal result: "demand before flexibility" is fixed to the metered SCADA total, taken only from days that meet the design-day temperature/weekday test and that are free of any switching-log transfer across a normally open point (`control_room_switching_log_2023-2026.csv` is what that exclusion is checked against).

A third sentence pins a population but, read completely literally, does not say how to apply it going forward, which is worth flagging on its own:

> "capacity_assessment_guideline_2026.pdf" (section 6): "a site is in service from the day it passes that test until it is withdrawn or leaves the service."

Checked against `flexibility_asset_register_2026-11-04.csv`: of the 126 Halverton rows with `service_year = 2027/28`, 125 are status "In delivery" and 1 "Superseded"; **zero** have a `commissioning_test_passed` date, because the register is a snapshot taken 2026-11-04 and winter 2027/28 has not started. Read with total literalism, section 6 would credit zero contracted MW at every primary for the winter being assessed, which cannot be the intended reading. The guideline never says how "in service on the assessment date" (15 January 2028) should be forecast for sites that are merely planned (via their own `planned_commissioning` date, typically mid-to-late 2027) to pass their test before then. This is a genuine open fork on a population that feeds several of the prompt's figures, not a routine lookup, and not something section 4's parallel rule for customer connections ("a customer not yet energised is taken to be energised on the date the register holds for it") resolves, because section 6 states no equivalent convention for flexibility sites.

## 6. Is there one thing that would make most of the prompt routine? Then classify each part.

**Closest one-thing candidate:** section 7's naming of "the load that comes back after a window varies from one evening to the next" together with section 6's "whichever half-hour that falls in." Together they hand the solver the two mechanisms that make "peak with flexibility" non-trivial: demand does not simply fall by the contracted MW and stay down, it can rebound inside or after the window and produce a new, later peak, and the peak has to be searched for across the evening rather than assumed to sit inside the service window. Noticing this settles, for every figure that touches "peak with flexibility" (the expected peak, the 9-in-10 comparison, the exceedance share, the further MW needed, and the Ashcombe Road scheduling question), that the solver must look at demand through and after 19:30 rather than assume a flat reduction. It does **not** settle the size of the rebound, the shape of the delivery-shortfall distribution, the connections growth figure, the in-service forecasting fork from Q5, or the data-hall load factor. An event-day plot of the half-hourly series would likely show the rebound shape on sight regardless of the sentence, so the sentence saves the discovery that something is there to look for, not the measurement of it.

My own read: executing the guideline literally produces the **skeleton** of the task (which file feeds which figure, the design-day filter, the window-averaging convention, the Monte Carlo's three resample axes), not the figures themselves. Getting actual numbers still requires fitting a temperature-to-demand relationship at -3.0 degC, building the DFES-plus-register growth figure (with the status filter below), resolving the in-service fork above from real commissioning history, building a delivery/cancellation distribution from `flexibility_events_2023-2026.csv`, sizing the rebound from the demand series, and estimating a load factor for a connection type (data hall) that has no history at the primary in question.

Classification of each part of the prompt:

1. **Demand before flexibility on the design day** - rule for the design-day filter and the growth-compounding formula (both spelled out in sections 2-4); analysis to actually fit the -3.0 degC design-day demand from the metered series and apply the register's status filter ("an offer counts once it is accepted... offers withdrawn, superseded or only quoted are not counted," confirmed meaningful: the register carries 20 Accepted, 14 Quoted, 7 Withdrawn and 3 Superseded rows that must be excluded alongside the 92 Energised ones).
2. **MW the contract can be expected to deliver, 17:00-18:00** - rule for the 17:30/18:00 averaging window (Q5); analysis for which sites actually count as in service (the Q5 fork) and what they have historically delivered net of cancelled/superseded instructions in `flexibility_events_2023-2026.csv`.
3. **Expected peak with the service instructed in full** - analysis; combines 1 and 2 with the rebound/half-hour-shift mechanism named in Q6.
4. **The level the peak stays under on nine design days in ten** - rule/lookup: this is firm capacity, read directly from Appendix A.
5. **Share of design days over firm capacity** - analysis: the three resample axes are named, but the underlying historical distributions and their combination are not, and must be built and run by the solver.
6. **Further MW to reach one day in ten, or "no amount would"** - analysis: an iterative or algebraic solve constrained to "the same kinds of site in the same proportions," read from the asset register's actual site mix per provider/zone, plus a judgement about when no amount suffices.
7. **MW Ashcombe Road should be scheduled at across the window to minimise its share, and whether that is enough** - analysis: a genuine optimisation over the rebound trade-off (schedule less now, rebound less later, versus schedule more now), not a lookup.
8. **Hartwell Common with a hypothetical 4,000 kVA data hall, MW added by the assessment date** - rule for the energisation-to-assessment-date timing convention (section 4); analysis for the load-factor assumption, which has no precedent at Hartwell Common and has to come by analogy: `load_growth_register_2026-27.xlsx` carries 7 other "Data hall" customers elsewhere on the network (none at Hartwell Common), several with MPAN cores that do resolve in `hh_customer_demand_monthly_2021-2026.csv` (confirmed, e.g. MPAN 1936671618767), so the analyst has real comparator load-factor evidence to use, not a given number.

## Mechanical sweep rulings

**a. capacity_assessment_guideline_2026.pdf: figures shared with the answer, in the firm-capacity appendix and section 7 text.**
Harmless. Firm capacity is required input that the prompt itself asks for directly ("the level that peak stays under"), so Appendix A's numbers have to recur in the answer; that is the WHAT, not a leak of the HOW. Section 7's numerals ("100,000" design days, the three-winters count) are generic method parameters, not case-specific results. I cannot rule out an incidental digit match against an unrelated output figure, but nothing in section 7 is itself a result of this task's computation.

**b. flexibility_contract_awards_2027-28.pdf: figures shared with the answer, in the earlier-contracted-MW table and the service-terms statement.**
Harmless. The 2027/28 awards table is exactly the input section 6 of the guideline tells the solver to use ("the megawatts contracted for that winter in the contract award notice"), so it must recur. The service-terms numbers (16:00-19:30 window, 0.5 MW steps, 1.0 MW floor, the 3.5-hour availability window) and the "previous winters" table are contract terms and history, i.e. inputs and context, not computed results.

**c. capacity_assessment_guideline_2026.pdf: carries many distinctive words of the committed call (primary names, reinforcement, firm capacity, the winter).**
Harmless as vocabulary; see Q1 and Q6 for where this document's content, not its vocabulary, actually matters. It is the real governing document for exactly this decision, so sharing the primary names and terms like "firm capacity" and "reinforcement" is unavoidable domain language, not a disclosed verdict. It never states which primaries exceed capacity or what to commit.

**d. Do any of these six files rank the five candidates on the decision question?**
None does. `capacity_assessment_guideline_2026.pdf` Appendix A lists all nine primaries alphabetically with a static capacity rating only. `flexibility_asset_register_2026-11-04.csv` and `flexibility_events_2023-2026.csv` are raw site and instruction logs. `flexibility_contract_awards_2027-28.pdf` gives contract terms and historical MW, a proxy for commercial stress at best, not a computed ranking. `primary_substation_register.xlsx` gives static transformer ratings and DFES growth percentages. `primary_transformer_condition_2026.xlsx` gives a Health Index that ranks transformer condition, not capacity risk (see Q4), and correlates with but is not the capacity answer. None combines demand, weather and flexibility together, which is what a real ranking on this question would need.

## Realism notes

- Appendix A's firm capacity for Dunmore Street (20.0 MW) implies no winter-cyclic uplift over its smaller transformer's nameplate ONAF rating (20 MVA from `primary_substation_register.xlsx`, ratio 1.00), while every one of the other eight primaries shows a consistent ~1.13-1.17x uplift (e.g. Ashcombe Road 27.5/24 = 1.146, Fenwick Street 35.0/30 = 1.167, Wexley Hill 27.0/24 = 1.125), with no footnote anywhere explaining why Dunmore's is different. A mismatched, differently-aged transformer pair being rated differently is plausible, but the silent break in an otherwise uniform pattern is worth a second look.
- Section 7's probabilistic "one design day in ten" firm-capacity criterion is not tied to any named external engineering standard anywhere in the document. I have moderate but not verified confidence that UK DNO winter planning of this kind is normally benchmarked against a named ENA Engineering Recommendation; I could not check this (no web access), so flagging it as worth checking rather than asserting it is wrong.
- Section 7's prose ("Design days are not alike. From one day to the next a primary's demand runs above or below its usual level for the temperature...") reads more like a simulation specification written for whoever builds the model than the terser, clause-based regulatory style the rest of the document and the other PDFs (contract award notice, DUoS statement) use. It is the one passage in the pack that sounds addressed to an analyst rather than recording a business fact.
- Checked and found to be realistic, not a defect: `flexibility_asset_register_2026-11-04.csv` carries provider-name variants ("Corvane Flex Ltd" / "Corvane Flex" / "CORVANE FLEX LTD") and `load_growth_register_2026-27.xlsx` mixes named feeder codes ("ASHC/F05") with raw circuit IDs ("C217561") in the same column. Both look like genuine manually-maintained DNO register mess, not a generated or templated tell.
- Nothing else in the pack (file modification times, which each match their document's own stated issue/publish date; the prose style of both PDFs; the MIDAS-style weather file schema; the CI/CML and DUoS files) reads as LLM-generated, templated or otherwise inconsistent with a real DNO's systems.
