# Sulfur run record

One row per platform round of a Sulfur build, written by `/triage-runs` (`build-pipeline`, Stage 6). This is the
Sulfur evidence that the next draw reads first, beside Project Mark's measured record (`evidence.md`,
`strategies.md`, `shipped-ledger.md`). A row is a measurement: the two runs' scores, where each first went wrong,
and the verdict. Nothing here is inferred, and an in-house estimate never gets a row.

**Columns.** task and architecture; date (ISO); subdomain; objective; the answer shape; the deep step's family
(`stumping` Part 1.0 names: clean comparison, hidden heterogeneity, design-matched uncertainty, variance beyond
noise, competing explanations, unfinished outcomes, forecast that earns its place, or own); run 1 score and its
first-wrong-step class; run 2 score and its class; the average; the counterfactual average; the triage verdict;
then, once known, the review result.

| Task | Date | Subdomain | Objective | Shape | Deep-step family | Run 1 | Run 1 class | Run 2 | Run 2 class | Avg | CF avg | Verdict | Review |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| task2 arch 3 | 2026-11-08 | general-statistics-data-science / exploratory-data-analysis-distribution-assessment | descriptive-distribution | a set of products in or out, rate and 90 per cent interval each | own (a drifting process read run by run between resets) | not reported, on the golden | none | not reported, on the golden | none | landed | landed | REDESIGN | |
| task3 arch 2 | 2026-11-08 | physical-environmental-sciences / hydrology-flood-frequency | forecasting | pick one of four alternatives, events a year each | own (a buffer emptied through a receiver's spare capacity) | not reported, on the golden | none | not reported, on the golden | none | landed | landed | REDESIGN | |
| task3 arch 3 | 2026-11-08 | physical-environmental-sciences / hydrology-flood-frequency | forecasting | pick one of four schedules, a 2046 peak drawdown each | forecast that earns its place, with a clean comparison (a far field calibrated on an existing cone against controls beyond it) | not reported, on the golden | none | not reported, on the golden | none | landed | landed | REDESIGN | |
| task4 arch 4 | 2026-11-08 | urban-regional-science / forecasting (transportation network) | forecasting | a set of districts handed over, van-hours saved per run, a net saving | own (the run time a set of route members takes off a shared run, priced set by set) | not reported (author: not stumped) | none recorded | not reported | none recorded | landed | landed | REDESIGN | |
| task6 a6 | 2026-11-08 | missing data, censoring and measurement error | descriptive-distribution | 14 | own (an inclusion probability inherited from the trace's edge request) | 73 | method shortcut | 83 | on the call (ask loss: misread of 5.2's naming clock) | 78.0 | 86.5 | FIX_ASKS | |

## Lessons

A lesson is written here only when two or more rows show it, with the rows named. A lesson that changes how a build
is designed is moved into the skill it governs in a `SKILLS:` commit, and its line here then points at the skill.

- **A mechanism the rows visibly carry is modelled on sight** (task2 arch 3, task3 arch 2, task3 arch 3). Both runs of every one of these builds
  spent 19 to 48 minutes, cleaned every Layer 1 item, and built the physical mechanism the data showed (dose volume
  falling with the litres a set had pumped; dewatering bounded by the receiving plant's hourly headroom) as their
  first model, then validated it on held-out rows of the same stream; task3 arch 3's runs also took the field's default control (remote
  same-aquifer wells beyond the cone) without being led to it. A deep step whose content is "model the
  structure the rows show" is a reflex for these runs; the live ground is a structure the rows in view hide or
  mimic (two effects offsetting inside the observed window, a support or sampling property the observed values do
  not share with the decision unit), with the deciding evidence in a second file at another grain or scale.
