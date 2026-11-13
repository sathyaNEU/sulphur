# Determinism check: task22 (re-judge after prompt wording, RebateNo ordering, step 5 / Final Rec wording)

**Verdict: DETERMINISTIC**
**Disposition: APPROVE**

## What changed since the prior pass, and what I checked against it

1. Prompt: "the premises" → "any premises where gas was taken without authorization, with how much each took."
   The clause sits inside "for the program's twelve months, each district's leak loss ... and any premises where
   gas was taken without authorization, with how much each took", one sentence, one scope (the twelve months to
   September 2026), one population (premises), one unit (Mcf per premise). The quantifier change removes a
   dangling backward reference ("the premises") without adding a second reading; it still resolves to exactly the
   "Without authorization sheet, one row per premise" deliverable and Critical Component 2. No fork opened.
2. `appliance_rebates_2024-2026.csv`: confirmed `RebateNo` is monotonic with `InstallDate` across all 414 rows
   (`nos sorted? True`, `dates sorted? True`). The numbering carries no ranking or tie-break information beyond
   the date already in the row, so it cannot be read as a second ordering convention for "12 more have a
   dual-fuel controls rebate on file" in Step 5. Not a fork.
3. Step 5 / Final Recommendation wording: the counts are now stated and I recomputed the arithmetic. 9 + 52 + 31 +
   12 + 1 + 7 = 112 (matches the stated fall count); 31 + 12 = 43 (matches Critical Component 2's "43 dual-fuel
   heat pumps"); 9 + 7 = 16 (matches "16 premises, 9 bypasses and 7 furnace taps"). All self-consistent, no gap
   and no double count in the chain as written.

## Figures recomputed against the shipped files

| Figure | Block value | Recomputed | Method | Result |
|---|---|---|---|---|
| East Industrial corrector customers, 12 mo, as recorded (pressure+temp only) | 395,152 (397,372 − 2,220) | 395,151.5 | Summed `commercial_correctors_daily` CorrectedMcf, Oct 2025–Sep 2026, accounts mapped to East Industrial via the register's Corrector accounts sheet | Matches to within rounding |
| Atmospheric pressure the correctors add | 13.98 psia | 13.97 psia, std 0.054 over 100 sampled customer-corrector days | Solved `atm = ratio·14.73·(T+460)/520 − P` from `commercial_correctors_daily`'s own CorrectedMcf/UncorrectedMcf, pressure and temperature | Matches; this is a filed fact solvable to ~0.4% precision from the data, not an open convention |
| Gate specific gravity | used in Dranchuk-Abou-Kassem conversion | 0.5864–0.598, mean 0.592 across the window | `city_gate_station_daily` SpecificGravity | Stable, filed daily, not a free choice |
| 16 premises / 18 accounts | 16 / 18 | plausible | `customer_accounts` shows 2,988 of 10,283 premises carry more than one account over 2023-08–2026-11 (move-ins/outs), so 2 extra accounts across 16 flagged premises is unremarkable, not a sign of an undercount or ambiguity | Consistent |
| Lakeview Dec 2025 gas in | 13,536.7 Mcf (within 1.5%) | ≈14,100 Mcf by a city-gate-minus-other-stations rebuild of the 18 PXDCR-FAIL days, without the EVC-I→EVC-II supercompressibility conversion the blocks apply to the other stations | Within the right range and direction (my undercorrected estimate sits above the target, as expected since I didn't lift the EVC-I stations) | Consistent, not exactly reproduced (expected, given the simplification) |
| Rule 1 cutoff margins | Riverside 1.17 (lowest "in"), Halvorsen 0.83 (highest "out") | same | `lauf_reduction_program_rules_2026.pdf`: Rule 1 line is literally 1.0% of twelve-month gas in | Both sit 0.17 points clear of the line, outside the blocks' own ±0.10 band, so the call does not flip inside the stated tolerance |
| Rule 2 / Rule 3 interaction | Old Town and Downtown excluded from the Rule 2 list | confirmed | Rule 3 of the same PDF: "The changeouts the 2027 plan already schedules in Old Town and Downtown proceed as planned and are not re-decided under Rule 2" | The blocks' Rule 2 list correctly omits Old Town and Downtown; this is a filed rule, not a judgment call |

## Open-choice checks

- Atmospheric pressure, specific gravity and the EVC-I→EVC-II supercompressibility basis are all solvable or
  filed directly from `commercial_correctors_daily`, `city_gate_station_daily` and the register, not assumed; I
  could not construct a reasonable rival reading of any of them from the shipped files.
- RebateNo order tracks InstallDate order exactly; it supplies no information the date field does not already
  give, so it cannot be read as an alternate "which rebate counts" convention.
- The prompt's new "any premises ... with how much each took" still resolves to one population (premises), one
  window (the program's twelve months), one unit (Mcf); I found no second defensible reading.

## Fix

None. No change to prompt, input_files or solution is needed from this pass; the three edits since the last pass
(prompt wording, RebateNo ordering, tightened step 5 / Final Recommendation wording) each close cleanly against
the shipped files and introduce no new fork.
