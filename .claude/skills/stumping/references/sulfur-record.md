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
| task6 a6 | 2026-11-08 | missing data, censoring and measurement error | descriptive-distribution | 14 | own (an inclusion probability inherited from the trace's edge request) | 73 | method shortcut | 83 | on the call (ask loss: misread of 5.2's naming clock) | 78.0 | 86.5 | FIX_ASKS | |

## Lessons

A lesson is written here only when two or more rows show it, with the rows named. A lesson that changes how a build
is designed is moved into the skill it governs in a `SKILLS:` commit, and its line here then points at the skill.
