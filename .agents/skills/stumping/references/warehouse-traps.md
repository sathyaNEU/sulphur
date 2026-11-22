# Warehouse traps: what a dimensional warehouse does to the rows

Since the late 1990s the banks, insurers, utilities, retailers and agencies whose records a build imitates have kept
them in dimensional warehouses on Kimball's pattern: facts at a declared grain, dimensions whose history is kept as
type 2 rows, periodic and accumulating snapshots, surrogate keys that a migration re-issues. A pack that reads as a
real extract carries these structures, and each sets a trap for an analysis read straight off the extract. The first
table is what the hygiene battery (`../../supplemental-stumping/SKILL.md` 1.1c) cleans by reflex: texture, never a
stump. The second is what the structures do to which rows exist and when, which no cleaning repairs: a seed for a
deep step where the decision's population or window does not share the property with the history the rows hold.

## Cleaned by reflex (Layer 1 texture only)

| Structure | What the rows show | What every careful run does |
|---|---|---|
| Type 2 dimension (effective from, effective to, current flag) | one row per version of an entity; zero-length rows from same-day corrections; a current flag wrong on a few rows | joins each fact to the version in force on its date; drops zero-length rows |
| Surrogate keys re-issued at a system migration | one entity under two keys either side of the cutover, with a crosswalk | maps through the crosswalk |
| Inferred member (a fact arriving before its dimension row) | facts on an Unknown row (key -1) until the dimension load catches up | re-joins on the natural key once the row exists |
| A snapshot batch loaded twice, or a month not loaded | duplicate month rows; a missing month | removes the duplicate; flags or carries the gap |
| A late-loaded attribute change (approved on one date, loaded a month later) | the snapshot holds the old value for a month | takes the effective date from the dimension |
| A recoded code list in a conformed dimension | one entity under two codes either side of the recode | maps old codes to new |
| Semi-additive measures (balances, headcounts) | month-end levels | never sums them over time |

## What the structures do to which rows exist (seeds)

| Structure | The property | The shallow read | The live form as a deep step |
|---|---|---|---|
| Type 2 history of a graded state (a credit grade, a risk band, a tier) | the history is a path, not a state: how recently and how the entity reached its grade | a state-only transition matrix, validated grade by grade on the pooled history | the decision's population was selected by recent movement (a downgrade wave, a policy that stages on movement), so time since the last move carries risk the grade does not, and the pooled validation passes |
| Periodic snapshot (state at each month end) | a stock over-represents long spells (length bias) and hides events inside the month | rates and durations read off the stock | the decision unit is a flow, or a stock with another age mix, and the duration dependence is estimated from entry cohorts |
| Accumulating snapshot (milestone dates, open rows blank) | open processes are right-censored; the closed ones are the fast ones | averages over closed rows | censored estimation is rung 1 (a named method); the deep step is completion speed that differs by a unit no pooled factor carries (`sulfur-strategies.md` Part A) |
| Warehouse go-live or archive purge | entities closed before go-live are absent; the rest enter at their age on the go-live date (left truncation) | survival from the original start date, every entity at risk from age zero | the risk set at each age built from the entry date, live only where the decision's ages are the truncated ones |
| Aggregate fact table or cube | segment mix moves under a flat total | a trend on the total | two effects offsetting inside the window, with the decision weighting segments to a mix the history did not hold, the segment rebuilt from a history and not read off a column |
| Late-arriving facts (claims, recoveries, chargebacks posted after the period) | recent periods incomplete | the latest periods read as improvement | completion by a unit whose delay changed |
| No factless coverage table | events without the exposure that produced them | event counts read as rates | exposure rebuilt from another file at another grain |
| Index roll-forward between physical measurements (a carried collateral or asset value) | the carried value is the last measurement moved by a market index; nothing stores how old the measurement is | the carried value as the current value, fed to a model fitted on fresh measurements | the units that fail are the ones whose value fell behind the index, by more the staler; the shortfall estimated on the age of the measurement behind each carried value from the failures' own re-measurement, and carried to a forward book staler than the record (task7 arch 5) |
| Relabelling recorded as attribute change (a model recalibration, a scale change) | moves that carry no news about the entity sit among moves that do | every move treated as news | the two explanations for a move separated by what follows it, never by a reason code |

## What the generator owes the structures (so they stay texture and open no fork)

| Structure | The defect when it is skipped | What the generator does |
|---|---|---|
| Warehouse go-live | derived rows (roll-forwards, accruals, revaluations) start at the first cycle after go-live, so the first months' records compare against stale pre-go-live values: outliers that bent every functional form apart (task7 arch 5, 2012 defaults at 0.2 to 0.35 of value) | writes the go-live's own load of the derived rows |
| Versions dated before the reporting date, loaded after it | the row in force at the reporting date is not the latest version by date, a fork on the carried value; a book facility with no row in force at all | loads every version dated in the year by the year-end close; never writes a derived row over a newer source row already on file |
| A trending index between two dates a ratio compares | the market's move over the lag enters every ratio, and the raw and index-adjusted constructions split (7 per cent on task7 arch 5) | damps the trend or asserts that both constructions land together |
| Business keys handed out by the generator | sorted, a key column runs as an arithmetic progression (steps of 11, 13, 37) | gaps from a stream of their own, increasing in the same order, so no sort and no draw moves |

A seed decides only with the rest of the anatomy in place (`../SKILL.md` 1.4): the property has no column, the field's
method at rung 0 or 1 files the wrong answer and validates on the pooled history, and two or more inferences are still
owed once a run has seen the evidence (`../SKILL.md` 1.1, `After the notice:`).
