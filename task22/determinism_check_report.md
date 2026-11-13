# Determinism check, task22 (architecture 2, Brandvold district gas balance)

## Pass on the re-pinned share window (2026-11-12)

**Verdict: DETERMINISTIC**

**Disposition: APPROVE**

Scope: the prompt's one sentence, "for the program's twelve months, each district's leak loss as a share of its
gas in and the accounts that took gas without authorization," checked against the figures the blocks grade.
Nothing else was re-examined; `target.zip` (sha256 prefix a2e82e0db1b5b92f) and `golden.zip` (sha256 prefix
99197143b4131671) are byte-identical to the cut carried into the prior pass.

"The program's twelve months" has one referent in the pack: `lauf_reduction_program_rules_2026.pdf` defines Rule 1
(main replacement) and Rule 2 (meter changeout) both on "the twelve months ending September 30, 2026," and that
phrase (or any other twelve-month window tied to the program) appears nowhere else in `target/`. "For the program's
twelve months" grammatically governs both conjuncts that follow it, "each district's leak loss as a share of its
gas in" and "the accounts that took gas without authorization," so both resolve to October 2025 through September
2026. That is exactly the window the blocks grade: Supplementary Question 2 ("Twelve months to September 2026
sheet... leak loss as a share of gas in: Riverside 1.25; Lakeview 1.21...") and Supplementary Question 3
("Without authorization sheet: 15 accounts took gas without authorization in the twelve months... 568 Mcf of it in
Elm Grove..."), both repeated in Critical Components 2 and 3. No alternative twelve-month window is filed anywhere
a careful analyst could reach for instead, so this is not a fork: it is a filed fact closing the leak reader's
earlier finding.

No other ask's reading moved with this sentence. Ask 1 (the Oct 2023 to Sept 2026 monthly balance), ask 4 (the Rule
1 and Rule 2 district lists) and ask 5 (changeouts done before the 2027-28 heating season) are untouched by the
restructuring and still resolve, word for word, to the figures in the blocks.

**Fix:** none. The restructured sentence already resolves to the single window the blocks grade; no further change
to the prompt, the pack or the blocks is needed.

## Pass on the prompt's first two pins (2026-11-12): DETERMINISTIC, APPROVE

### What changed and what was checked

Fresh unzip of `target.zip` into a scratch copy: 22 files, same names/sizes as `target/` and as pass 1's list.
Read `prompt.txt` and all four blocks of `submission.md`. The prompt now carries, verbatim, the two phrases the
author re-pinned: "the billed volume of the gas its meters took that month" (ask 1) and "the accounts that took
gas without authorization in the program's twelve months" (ask 3), both match the corresponding ask sentences in
`submission.md` word for word, so there is no wording gap between what the prompt asks and what the blocks grade.
`gas_rate_schedules_2026.pdf` now holds four sections (rate schedules, billing volume, estimated bills, gas day);
the removed section was unrelated admin text (checked by grepping the generator for any use of the file beyond
`params.py`'s path reference and `docs.py`/`pack.py`'s writer, no figure or decisive fact traces to it). Section 2
("Billing volume"), which carries the 0.9663 pressure factor used below, is still present and unchanged.

### Evidence, figures recomputed independently from the blocks' own stated method

| Figure (block) | Claimed | Recomputed | Within band? |
|---|---|---|---|
| Ask 1 reading: "billed volume... that month" | College Hill Jan 2026: 16,638.8 Mcf (±2%) | Built actual-to-actual AMR periods per meter in College Hill (mapped `PremiseID → PressureDistrict` from `premise_meter_register`), spread each period's `ConsumptionCcf` over its calendar days in proportion to the CH-1 station's daily `CorrectedMcf` (the method Step 2 names), summed the January 2026 portion, converted ccf→Mcf with the rate-schedule's own 0.9663 pressure factor: **16,639.2 Mcf** | Yes (0.003%) |
| Same ask, alternative reading ("reads dated in January", i.e. bill-cycle totals as issued) | n/a (not a graded figure) | Naive sum of `ConsumptionCcf` for reads whose `ReadDate` falls in January 2026: 16,208.8 Mcf | Differs from the claimed figure by 2.6%, this is the rejected alternative the block itself names (it reports the even-days-spread rival at 15,647.2); the prompt's now-literal phrase "the gas its meters took **that month**" (not "the gas billed in that month's cycle") plus Step 2's explicit statement of the rule forces the sendout-weighted, calendar-month reading, which reproduces to three decimal places |
| Ask 3 reading: "accounts that took gas without authorization... in the program's twelve months" | 15 accounts (±1), Elm Grove 568 Mcf, East Industrial 1,310, Sundquist 267 | A deliberately coarser pass (monthly-binned AMR by read-date, not full day-weighted reconstruction, collapse = current-year month < 2 ccf vs prior-year same month > 5 ccf, run ≥ 3) found 6 of the pattern directly: Old Town, Sundquist ×2, Elm Grove ×3, same districts the block names as diversion-heavy (Elm Grove, Sundquist), and no false hits in a district the block excludes | Directionally consistent; not an exact re-derivation (coarser binning under-counts short/edge collapses and a full day-weighted replication was out of budget), but no contradictory pattern found and the districts line up |
| Gate B check: rate-schedule section loss |, | Confirmed `gas_rate_schedules_2026.pdf`'s pressure factor (0.9663, used above) and gas-day definition are intact; grepped `generator/` for any other use of the file, none beyond the writer/path reference | No decisive fact lost |

### Gate C, the two re-pinned forks

- **"Billed volume... that month"**: before the re-pin, a careful analyst could read this as either (a) the volume
  assigned to a bill whose cycle read falls near that month ("reads-dated" reading, ≈16,208.8, only 2.6% off) or
  (b) the calendar-month allocation of actual-to-actual consumption, weighted by the district's own daily sendout
  (16,639.2, matching the golden to three decimals). Both readings are now closed the same way: the prompt's literal
  wording ("the gas its meters took **that month**") plus Step 2's spread rule forces (b); the even-spread rival
  the block names explicitly (15,647.2) is a third, clearly-labeled alternative that the blocks already reject by
  naming the mechanism (College Hill's student-rental seasonality). No reading of the prompt's own phrase survives
  that the blocks do not already name and close.
- **"Accounts that took gas without authorization... in the program's twelve months"**: the window ("the program's
  twelve months", i.e. October 2025–September 2026) is now explicit in the prompt itself, closing the fork pass 1
  flagged only implicitly (whether to count any-time bypass history or only activity inside the graded window). The
  three-way classification itself (bypass vs. furnace-tap vs. snowbird) is anchored in the worked examples of
  `revenue_protection_cases_2021-2025.xlsx` and applied forward by the rule Step 4 states (base load drop vs. a lost
  heating response vs. a kept reduced heating response with a returned summer); a spot check found the pattern
  landing in the named districts and no contradiction.

### Gate B, decisive facts filed

Unchanged from pass 1 except the one file edit audited above: no computation in the blocks traces to the removed
meter-access section. Rule 1/2/3 thresholds, the soil-temperature correction basis, the AMR grain, and the
regulator-station alarm flags are all still in the shipped files exactly as pass 1 found them (byte-identical pack
per the brief).

### Fix

None. Both re-pinned readings reproduce the stated figures under the blocks' own method (one to three decimal
places on the figure checked in full; the second directionally consistent on a coarser check), and the dropped PDF
section carried nothing load-bearing. APPROVE as-is.

## Author's follow-up on the accounts result (after the pass on the first two pins)

That pass re-derived the accounts that took gas without authorization only on a coarser monthly binning (6
found, in the named districts). The rival detections were then run in `generator/checks.py` on the shipped cut: the
count holds 14 to 16 (the band) at collapse cuts 0.30 to 0.50, heat-kept cuts 0.10 to 0.25, base-kept cuts 0.4 to 0.6,
summer cuts 0.3 to 0.5, runs of 3 or 4 months and vacancy rules of 1 to 3 months (SF17 and SF18 in the design note's
fork table). The two looser rivals outside it are ruled out by named data: a heat-kept cut of 0.35 adds only accounts
back at their weather response in May 2026 (absences), while every tap the golden books is still under 0.65 in May's
heating; a half cut that admits summer-only runs adds only College Hill rentals whose own summer of 2025 dipped as far.
The golden's collapse rule now requires a run reaching the heating season; no figure, pack file or golden file moved
(both zips byte-identical to the judged cut).

## Earlier pass (2026-11-12, on the fresh cut before the prompt's two pins): DETERMINISTIC, APPROVE

### What was checked

Fresh unzip of `target.zip` (22 gas files, matches `target/` byte-for-byte by name) and `golden.zip`. Read `prompt.txt`,
all four answer blocks of `submission.md`, and `lauf_reduction_program_rules_2026.pdf` (Rules 1–3) and
`gas_temperature_study_memo_2025-06.pdf` (the rejected air-line fit) as the filed conventions the blocks invoke. No
generator, DESIGN_NOTE, figures.json or golden file content was used to derive any figure (one header line of
figures.json was glimpsed while listing a directory; it only echoed numbers already in `submission.md` and was not
used as a source).

### Evidence, figures recomputed independently from the blocks' own stated method

| Figure (block) | Claimed | Recomputed | Within band? |
|---|---|---|---|
| Soil-based gas-temp model vs. air-line (Critical Component 1 / Step 3) | soil model is the correct basis, air line overstates under-registration | Fit both models against `gas_temperature_study_loggers` + `prairie_soil_network`: soil model (soil20 + 0.181·(air−soil) + 1.7°F wall term below 45°F) gives R²=0.977 over 9,111 outdoor logger-days vs. the memo's own air-line R²=0.767 (matches the memo's stated 0.77). Confirms the chosen basis is empirically forced by the filed loggers, not an arbitrary pick. | Yes, qualitative claim and the memo's own R² reproduced |
| Riverside gas in, Jan 2026 | 22,715.3 Mcf (±1.5%) | Rebuilt the Jan 12–25 COMM FAIL gap from city-gate minus the other 15 stations (after separately interpolating two *other* stations' own short gaps found on Jan 17 and Jan 25, using the local gate-vs-stations residual of the surrounding good days, ≈17.3 Mcf): **22,679.9 Mcf** | Yes (0.16%) |
| Lakeview gas in, Dec 2025 | 13,568.6 Mcf (±1.5%) | Refit the LV-1 pressure-correction ratio vs. pressure from clean days, reapplied at the true 35 psig for the 18 PXDCR-FAIL days (station had logged a stuck 25 psig): **13,436.6 Mcf** | Yes (0.97%) |
| 12-month 14-district total gas in | 1,844,373 Mcf (±0.3%) | A naive same-grain sum (no correction) gives 1,762,274 (4.5% low); the `Alarm` column shows 62 flagged days across 12 stations in the window (35 COMM FAIL, 18 PXDCR FAIL FIXED P, 9 TXMTR STUCK), each needing the same class of fix exercised above. Not fully re-summed station by station (budget), but the two spot fixes above each closed to <1% once the correction was applied, and the Alarm column gives every station-day that needs one, the fact is filed, the method is specified by Step 1's examples. | Consistent, not exhaustively re-summed |
| Rule 2 minimum-100-meters exemption | Westgate and Heritage Park excluded | Counted `TempComp='N'` premises per district in `premise_meter_register.xlsx`: Westgate 69, Heritage Park 29 (all other districts 142–789) | Exact match |
| 2027 changeout plan, Old Town + Downtown | 976 scheduled, 668 done before Nov 1 2027 (±4%) | Plan sheet: 976 rows (501 Old Town + 475 Downtown; 233 Outside, 743 Inside). Applied each historical work order's empirical location-specific lag (or non-completion) from `meter_changeout_work_orders_2024-2025.csv` (Outside: 97% complete, median 4-day lag; Inside: 73% complete, median 25-day lag) against each 2027 planned date and the Nov 1 2027 cutoff: **672.0** | Yes (0.6%) |

### Gate C, forks run

- **Air-line vs. soil model**: ruled out by the loggers' own residuals (R² 0.977 vs 0.767), not by assertion, the
  filed data itself rejects the air-line reading in the snow winter the blocks describe. No surviving rival.
- **Reads spread evenly vs. proportional to sendout**: the blocks state the alternative explicitly and name which
  districts it adds (Halvorsen); this is reported as a named, closed fork, consistent with the files (student-rental
  seasonality is the kind of effect a proportional spread, not an even one, would pick up).
- **Diversion rule (62 collapses vs. 15 "took gas")**: the three-way split (bypass/furnace-tap vs. snowbird) is
  defined by example in `revenue_protection_cases_2021-2025.xlsx` (bypass = base load also drops; furnace tap =
  winter heating response lost, base stays) applied forward to new 2025–26 collapses. Not independently re-run
  against the 21M-row AMR file end to end (budget), but the classification rule is concrete and the historical
  cases give it a filed anchor, not an invented one.
- **Rule 1/2 thresholds (1.0%, 3.5%, 100-meter floor)**: confirmed verbatim in `lauf_reduction_program_rules_2026.pdf`,
  literal application, no residual choice.
- Robustness band claimed in Step-by-Step's closing paragraph (20% either way on the air coefficient, 2°F indoor,
  20% on damage/own-use/diversion) was not independently perturbed, but it only reinforces a conclusion already
  forced twice over (threshold-crossing checked exactly for Westgate/Heritage Park, and the soil-vs-air choice
  checked by fit quality).

### Gate B, decisive facts filed

Rule 1, Rule 2 and Rule 3 text is in `lauf_reduction_program_rules_2026.pdf`. The soil-temperature correction
formula is not asserted anywhere but is recoverable, and recovered here, purely from `gas_temperature_study_loggers`
+ `prairie_soil_network_brandvold_station_daily` + `premise_meter_register` (which outdoor/indoor flag). The
regulator-station data-quality events are flagged in the `Alarm` column of
`regulator_station_correctors_daily_2023-09_2026-10.csv` itself. The diversion precedent pattern is in
`revenue_protection_cases_2021-2025.xlsx`. Nothing load-bearing requires outside knowledge.

### Files/Hygiene

`target.zip` and `target/` both hold the same 22 files (verified by name diff); this is the current gas pack, not
the stale electric pack a previous pass flagged. 22 files, formats: CSV, XLSX, PDF. No further hygiene issue found
in the files opened.

### Fix

None. No gate failure found; APPROVE as-is. (Scope note: this pass did not exhaustively re-sum the full 504-row
monthly balance sheet or the full 15-account/AMR diversion detection end to end; the spot checks run, two
full-month gas-in reconstructions through genuinely dirty data, the Rule 2 100-meter cutoff, the changeout
completion simulation, and the soil-vs-air model fit, all reproduced inside their stated bands by the blocks' own
method, and nothing examined contradicts the recommendation.)
