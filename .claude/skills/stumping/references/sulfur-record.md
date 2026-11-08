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
| task5 arch 2 | 2026-11-08 | survey-research-official-statistics / census-register-administrative-data-quality | etl | a designation set against a threshold, share and 90 per cent interval each, register coverage cells | own (occupancy read from a day's departure from the dwelling's own typical day) | not reported, on the golden | none | not reported, on the golden | none | landed | landed | REDESIGN | |
| task6 a6 | 2026-11-08 | missing data, censoring and measurement error | descriptive-distribution | 14 | own (an inclusion probability inherited from the trace's edge request) | 73 | method shortcut | 83 | on the call (ask loss: misread of 5.2's naming clock) | 78.0 | 86.5 | FIX_ASKS | |
| task7 arch 4 | 2026-11-08 | banking-credit-financial-risk / expected-credit-loss-provisioning | opportunity-sizing-decision | allocation under an envelope, every candidate graded | clean comparison (spillover priced through payments between customers) | 98 | none (note slip) | 58 | dismissed own evidence | 78.0 | 77.0 | FIX_ASKS | |
| task7 arch 4 round 2 | 2026-11-08 | banking-credit-financial-risk / expected-credit-loss-provisioning | opportunity-sizing-decision | allocation under an envelope, fall-back intakes and an envelope curve | clean comparison (spillover priced through payments between customers) | not reported, on the golden | none | not reported, on the golden | none | landed | landed | REDESIGN | |
| task8 arch 17 | 2026-11-08 | education (assessment) | descriptive / decision | pick one of three drafts, expected mark each, regional counts | own (items recalibrated on taught candidates) | not reported, on the golden | none | not reported, on the golden | none | landed | landed | REDESIGN | |
| task7 arch 5 | 2026-11-08 | banking-credit-financial-risk / expected-credit-loss-provisioning | forecasting | a plan figure, a split by lending book, the five facilities expected to cost most | heterogeneity that pooling hides (the shortfall at default by years since the inspection behind the carried value, carried to a staler book) | not reported, every graded cell (€2.04 million, €1.27 and €0.77 million, the five) | none: on the call by the golden's own fit, validated out of sample | not available | none recorded | landed | landed | REDESIGN | |
| task10 arch 4 | 2026-11-08 | energy-systems-utilities / grid reliability and asset condition | forecasting | a set of hubs below a per-unit availability standard, charges and energy each | own (a failure clock reset by a neighbour's service visit, removed by a renewal) | not reported, on the golden | none: the hang-age floor read off the first histogram, a censored hazard on time since restart, validated on 2026 | not reported, on the golden | none: a censored Weibull on time since evidenced reset, validated on 2026 | landed | landed | REDESIGN | |
| task2 arch 4 | 2026-11-08 | general-statistics-data-science / exploratory-data-analysis-distribution-assessment | descriptive-distribution | which tier, the gold above cut-off at block support | own (the support effect: the declustered composites carried to the block variance the variogram gives) | not reported, on the golden (Tier B) | method shortcut that landed: plain inverse-distance-squared blocks, 159,610 oz | not available | none recorded | landed | landed | REDESIGN | domain fit returned (read as summing tabulated blocks against stated tiers) |

## Lessons

A lesson is written here only when two or more rows show it, with the rows named. A lesson that changes how a build
is designed is moved into the skill it governs in a `SKILLS:` commit, and its line here then points at the skill.

- **A mechanism the rows visibly carry is modelled on sight** (task2 arch 3, task3 arch 2, task3 arch 3, task5 arch 2, task7 arch 4 round 2,
  task8 arch 17; moved into `../SKILL.md` 1.4, the lines `Hidden by:` and `After the notice:`). Both runs of the first three builds
  spent 19 to 48 minutes, cleaned every Layer 1 item, and built the physical mechanism the data showed (dose volume
  falling with the litres a set had pumped; dewatering bounded by the receiving plant's hourly headroom) as their
  first model, then validated it on held-out rows of the same stream; task3 arch 3's runs also took the field's default control (remote
  same-aquifer wells beyond the cone) without being led to it. A deep step whose content is "model the
  structure the rows show" is a reflex for these runs; the live ground is a structure the rows in view hide or
  mimic (two effects offsetting inside the observed window, a support or sampling property the observed values do
  not share with the decision unit), with the deciding evidence in a second file at another grain or scale.
- **Noticing was the whole stump** (task7 arch 4 rounds 1 and 2, task8 arch 17). Once a run measured the payer
  dependence or matched responses to the teaching calendar, what was left was standard (price the conditional rate,
  fit the coverage contrast), and nine of the ten runs across the five rounds reached the golden or computed its key
  figure. The designs passed the readability screen on paper because no column or sentence named the step, but the
  decision's own framing named the axis (a November sitting set from August data; write-off kept off the book through
  the borrowers taken on). Moved into `../SKILL.md` 2.1 as readability test 8 (the framing) and 1.1's `After the
  notice:` line.
