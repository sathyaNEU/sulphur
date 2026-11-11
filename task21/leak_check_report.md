# leak check, task21

**Verdict: REVIEW.** 17 files read, 37 golden figures and 2 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: claims, renewal, change, planning, policy, months, method, experience, prices, twelve, missed, february, priced, result, capped, latest, golden, million, selection, completed, seasons, rivals, halvergate, weight, family

## 1 file names (REVIEW 1)
- **REVIEW** `hpm_model_deployments.txt`: a text file in the pack: confirm it is the organisation's own record (a thread, a log, a letter) and does not describe the data

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `CMP-RP-04_renewal_pricing_policy.pdf`: golden figure 3.3 appears: ...ces the premium to that price where it is higher. 3.3 Compliance attests each quarter to the board that...
- **REVIEW** `PLN-2027-03_pcw_rate_plan_2027_planning_basis.pdf`: golden figure 2.3 appears: ...to 2027 cost levels by raising them 5.5 per cent. 2.3 Halvergate's 2027 premium for a risk is the premi...

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `CMP-RP-04_renewal_pricing_policy.pdf`: 4 of 25 stump-paragraph terms appear (claims, renewal, policy, halvergate); read whether the document names the move
- **REVIEW** `PLN-2027-03_pcw_rate_plan_2027_planning_basis.pdf`: 13 of 25 stump-paragraph terms appear (claims, renewal, change, planning, policy, months); read whether the document names the move
- **REVIEW** `hpm_model_deployments.txt`: 3 of 25 stump-paragraph terms appear (claims, change, halvergate); read whether the document names the move

## 9 dates after the setting (INFO 1)
- **INFO** `-`: no --asof given, sweep skipped (pass the fiction's as-of date)

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 11 prompt gate (REVIEW 1)
- **REVIEW** `prompt.txt`: no roll call: 1 attributed opinion(s)

## 12 client quality check (INFO 2)
- **INFO** `-`: 17 usable files (10 or more required)
- **INFO** `-`: 3 file categories: document, spreadsheet, structured (2 or more required)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)


## Solver's-eye read

Two isolated readers (Sonnet, medium), each on a fresh copy of `prompt.txt` and `target/` only, 2026-11-11. The first
read the cut before the stage 4 fixes; the second read the cut after them (the prompt naming 21 per cent in both
places and the premium's unit, the deployment log without its comparability sentence, the renewal ages at renewal).

Verdicts on the REVIEW lines (the main thread's rulings, one line each in the design note's `## Leak rulings`):
- `hpm_model_deployments.txt` (file name, vocabulary): the pricing team's own deployment log; harmless.
- answer figures 3.2 and 2.3: section numbers; harmless.
- design-note vocabulary in the planning paper and the renewal policy: ordinary pricing words; the documents file the
  WHAT and the cap, never the HOW (both readers placed every ask on analysis); harmless.
- dates after the setting in the policy extract: expiry dates and November starts of policies sold in late October;
  harmless. The claims' and cancellations' later dates were a defect, fixed.
- prompt roll call and shell quota: the incumbent's figure and corpus quotas; harmless, the author's rewrite owns the
  shell.

After the second read, two data-form fixes went in with no graded figure moving (checked by `leak.py` and every gate,
as a data-only repair): each site's quote references now advance on that site's own counter (they had interleaved on
one), and the renewal schedule's premium columns say they are net of IPT.

### First reader

**Flag before anything else:** the prompt is internally inconsistent about the one number it supplies. It opens "The pricing team wants 21 per cent for under-25s." and later, in the same paragraph, asks for "the 2027 loss ratio of under-25 business at the team's 15 per cent." A third clause ("how many policies the team's under-25 rise and the over-65 cut would each write") then refers back to "the team's under-25 rise" without repeating either number. Two of the asked-for results (the loss ratio and the policy count at "the team's" rate) have two literal readings, 21 per cent and 15 per cent, that will produce different golden figures. I did not find "21" or "15" tied to an under-25 proposal anywhere in the pack (checked every PDF, the rate-change log, and all workbook cells), so the pack cannot resolve it either. This needs a decision before upload.

### 1. Which sentence or file tells you how any part of the analysis should be done

The load-bearing file is `PLN-2027-03_pcw_rate_plan_2027_planning_basis.pdf` ("Comparison-site new business: 2027 rate plan, planning basis"), which is written as a formal methodology paper and pins most of the prompt's steps:

- "The business is divided by the age of the main driver on the quote: under 25, 25 to 64, and 65 and over." (1.2) — the grouping.
- "A segment's loss ratio is its ultimate claims, each claim capped at £100,000, at 2027 cost levels, divided by its written premium net of insurance premium tax, for the policies it writes in the year, each over its own policy year." (2.1) — the measure.
- "Claims at 2026 cost levels are taken to 2027 cost levels by raising them 5.5 per cent." (2.2) — the trend step, but only for the last year (see Q5).
- "Halvergate's 2027 premium for a risk is the premium the rates in force on 31 October 2026 give it, with the segment's 2027 change applied; the pricing model's claims-cost index stays at its 2026 level through 2027." (2.3) — the pricing basis.
- "Experience is read from the policy and claims extracts as at 31 October 2026 and from the reserving team's triangles to 30 September 2026." (3.1) — the data window.
- "The comparison sites are taken to return 2027 quotes in the number and mix they returned from 1 February 2026 to 31 October 2026, scaled to twelve months." (4.1) — the volume/mix basis, but the scaling method itself ("scaled to twelve months") is not spelled out (flat 12/9, seasonal, etc. all still open).
- "Rivals' prices on the sites are taken to rise 2 per cent on 1 January 2027 and not to move again during 2027." (4.2) — a stated competitor-response convention.
- "A segment's change is the smallest change, in whole per cent, at which the expected loss ratio of its 2027 comparison-site new business is 75 per cent or below." (5.1) — this is close to a restatement of the prompt's own question, so it mainly pins "whole per cent" as the rounding convention rather than handing over the modelling.
- "Where a range is given for a loss ratio it is the range within which 80 per cent of the year's outcomes would fall: the claims the year's policies bring, drawn policy by policy, around the expected loss ratio." (5.2) — this does narrow the method for the 80% range: it specifies a policy-by-policy (process-risk) simulation rather than, say, a portfolio-level normal approximation or a method that also mixes in parameter uncertainty.
- "Underwriting profit is written premium net of insurance premium tax, less capped claims at 2027 cost levels, less the site's commission on each sale (PCW-COM-2026, unchanged for 2027) and less servicing of £34 a policy." (6.1) and "A segment's 2027 underwriting profit counts its comparison-site new business written in 2027 and its customers first sold through a comparison site who renew in 2027, as the 2027 renewal schedule lists them." (6.2) — the profit formula and its population.

Two other filed documents also instruct steps:
- `CMP-RP-04_renewal_pricing_policy.pdf`: "At renewal the premium offered to a customer may not exceed the equivalent new-business price... The renewal system compares each renewal premium with its equivalent new-business price before the invitation is issued and reduces the premium to that price where it is higher." (3.1–3.2) — fixes a capping rule that bears on the over-65 underwriting-profit figure (see Q5).
- `hpm_model_deployments.txt`: "Risk premiums from this release are not comparable factor by factor with v6." — an explicit instruction not to treat pre- and post-refit risk premiums as directly comparable.
- `PCW-COM-2026_comparison_site_commissions.pdf`: "Commission is payable to the site on each policy sold through it, net of policies cancelled within the 14-day cooling-off period." — fixes which sales carry a commission cost.

### 2. Which file already ranks or scores the options on the prompt's question

None. I checked every file for a pre-built comparison of rate-change options or a scored recommendation on the over-65 cut: `pcw_rate_change_log_2024-2026.xlsx` holds only past, already-implemented changes (2024-03-01, 2025-03-01, 2026-02-01), each dated and clearly historical, not a 2027 proposal or a ranking of alternatives. `renewal_retention_mi_65plus_2025-2026.xlsx` is raw empirical retention by price-change band and month (506 rows), with no fitted curve, elasticity coefficient, or summary column added. No workbook has a hidden or extra sheet, and none of the four PDFs contains a table of candidate rate changes or an outcome score. Nothing in the pack ranks the under-25/25-64 rise options or scores the over-65 go/no-go.

### 3. Which file exists only to help the analyst, rather than being a record the organisation would keep for its own work

None identified. Every document reads as something the stated owner would keep regardless of this task: `CMP-RP-04` is a Board-approved compliance policy (owner: Compliance), `PCW-COM-2026` is a Distribution Finance commission schedule, `motor_xol_reinsurance_programme_2026.pdf` is a Reinsurance and Capital programme summary, `PLN-2027-03` is a pricing paper with a named author and approver, and `hpm_model_deployments.txt` is a plain model-version changelog ("Kept by: Roy Osborne", Pricing Analytics) of the kind a model-governance team keeps for audit/traceability, not for this exercise. The named owners cross-check consistently (Roy Osborne is the `hpm_model_deployments.txt` keeper and also the xlsx `creator` of `pcw_rate_change_log_2024-2026.xlsx`; Frances Green is PLN-2027-03's named author and the xlsx `creator` of `renewal_retention_mi_65plus_2025-2026.xlsx`), which supports these being genuine internal artefacts rather than documents assembled for the test.

### 4. Which figure or name in the pack reads as the answer rather than as context

Nothing reads as a direct answer, but two things could be mistaken for one if read carelessly:
- The most recent row of `pcw_rate_change_log_2024-2026.xlsx` ("2026-02-01, under 25, +8%", "2026-02-01, 25 to 64, +3%", "2026-02-01, 65 and over, +2%", each annotated "with HPM v7.0") is the latest implemented change, not the 2027 figure being asked for; it is clearly dated and would only mislead someone who ignored the "Effective" column.
- PLN-2027-03's escalation rule, "A change that lowers a segment's loss ratio and its underwriting profit together goes to the executive with both figures" (6.3), narrates the shape of a notable outcome (a change that moves loss ratio and profit the same way) without giving a number; it reads like a hint about what pattern the answer might take rather than pure governance text, though it states no figure.

No column or field name (e.g. nothing like "recommended_rate", "final_answer", "target_lr") suggests a precomputed answer.

### 5. Which filed sentence, read literally, fixes how a figure is computed, or over which population or window

Beyond the Q1 list, these are the ones that most precisely pin a figure, with what each settles stated in words only:

- PLN-2027-03 2.1 ("A segment's loss ratio is its ultimate claims, each claim capped at £100,000, at 2027 cost levels, divided by its written premium net of insurance premium tax, for the policies it writes in the year, each over its own policy year.") fixes the loss-ratio numerator (capped, cost-levelled ultimate claims), denominator (premium net of tax) and population (that segment's own policy-year, not calendar-year, experience).
- PLN-2027-03 2.2 ("Claims at 2026 cost levels are taken to 2027 cost levels by raising them 5.5 per cent.") fixes only the last step of trending, from 2026 to 2027; it says nothing about how claims sitting at 2021–2025 cost levels (the bulk of the reserving triangles and the claims extract) reach 2027 levels, so an earlier trend still has to be sourced, most plausibly from `motor_premium_index_2019Q1_2026Q3.csv`, which is otherwise the only file carrying a claims/premium cost index back to 2019.
- PLN-2027-03 3.1 fixes the data window for the loss-ratio build: policy/claims extracts as at 31 October 2026 (matches the file names `pcw_nb_policies_sold_2025-01_2026-10.csv` and `motor_claims_extract_2026-10-31.csv` exactly) and reserving triangles to 30 September 2026 (matches `reserving_triangles_2026Q3.xlsx`).
- PLN-2027-03 4.1 fixes the window for projecting 2027 quote volume and mix (1 February to 31 October 2026, scaled to twelve months); that nine-month window spans the 6 July 2026 HPM v7.1 claims-cost index refresh noted in `hpm_model_deployments.txt`, which is a separate, dated fact to carry forward rather than something the prompt or PLN-2027-03 reconciles for you.
- CMP-RP-04 3.1–3.2, together with PLN-2027-03 6.2, fixes a real mechanism for the over-65 underwriting-profit figure: a renewal premium is capped at the "equivalent new-business price... at the new-business rates then in force", and 2027 underwriting profit counts "customers first sold through a comparison site who renew in 2027, as the 2027 renewal schedule lists them." I checked this against `renewal_schedule_2027_aged_65_plus.csv` directly: across all 165,000 rows, `renewal_premium_offered_gbp` equals the smaller of `intended_renewal_premium_gbp` and `enbp_at_current_nb_rates_gbp` with no exceptions, and about four in five rows are actually capped (intended exceeds the equivalent new-business price). So a change to the over-65 new-business rate changes the cap on a large, specific majority of that segment's renewal book, not just on the new-business policies named in the prompt; this is a real, checkable consequence of combining two filed documents with one data file, not a number stated anywhere.
- The `written_premium_gbp` / `ipt_gbp` fields in `pcw_nb_policies_sold_2025-01_2026-10.csv` are not individually defined in any document, but `ipt_gbp` is exactly 12 per cent of `written_premium_gbp` on every row I checked (20,000 rows, no exceptions), which is the standard UK insurance-premium-tax rate; this fixes, by construction rather than by a sentence, that `written_premium_gbp` already is the figure "net of insurance premium tax" that PLN-2027-03 2.1 and 6.1 call for, and the gross amount a customer actually pays is `written_premium_gbp + ipt_gbp`.

### 6. Is there one thing that would make most of what the prompt asks for routine

No single file, sentence, column or pattern unlocks most of the chain. The things that are filed are each tied to only one or two of the nine distinct results the prompt asks for, and the prompt's results require combining several of them plus real modelling. Breaking the prompt into its distinct asks:

a. **Under-25 smallest whole-per-cent rise to a 75% 2027 loss ratio.** Genuine analysis: segment claims assembly (join claims to policies, allocate aggregate triangle development to the segment, trend and cap), a volume/conversion response to price, and a search for the minimum qualifying whole per cent.
b. **25-to-64 smallest whole-per-cent rise to a 75% 2027 loss ratio.** Same as (a), with one filed fact to apply correctly rather than discover: the HPM v7.0 rebuild ("Main drivers aged 25 to 64: frequency model rebuilt...", "Risk premiums from this release are not comparable factor by factor with v6") means the 25-to-64 claims history has to be split or reconciled by rating-model era (`rating_model` is a literal column on every policy), a stated, one-step adjustment, not a hidden discovery.
c. **80% range on the 25-to-64 loss ratio.** Genuine analysis: the shape of the method (policy-by-policy, process risk only) is pinned by PLN-2027-03 5.2, but building the actual simulation (frequency/severity distributions, how many policies, how claims attach) is open work.
d. **Under-25 loss ratio at "the team's" rate.** Mostly a direct read-off of the model built for (a), evaluated at a given input rather than searched for; the only real obstacle is the prompt's own 21%/15% conflict (see the note at the top), which is a reading problem, not an analytical one.
e. **Policies the team's under-25 rise would write.** Same as (d): a read-off of (a)'s volume model at a given rate.
f. **Policies the over-65 cut would write.** Needs its own fresh new-business volume/demand build for the over-65 segment (not reusable from a/b), evaluated at the one stated input (-3%); genuine but narrower than (a)/(b) since there is no search.
g. **Over-65 cut's effect on 2027 underwriting profit, in pounds.** Genuine analysis and the most cross-file result in the chain: it needs (f)'s new-business output plus the renewal-book consequence of the CMP-RP-04 cap described above, under PLN-2027-03 6.1's profit formula, compared against the no-cut baseline.
h. **2026 quotes, sales and conversion so far, by segment.** Mostly correct execution of a stated structure across four independently-formatted files (`brightquote...csv`, `kitecompare...csv`, `pricelark...csv`, `covertide...jsonl`): bucket raw numeric ages into the three prompt segments (the one file with pre-bucketed ages, `direct_web_quotes_sales_2025_2026.xlsx`, is out of scope under PLN-2027-03 1.3, so the easy version of this step sits on the file that isn't usable), reconcile four different date/price/weight formats, and apply the weight column correctly. That weight column (`Weight` / `extract_weight` / `sampling_weight` / `weight`, values only 1 or 50) is not a generic sampling weight: I matched it against `pcw_nb_policies_sold...csv` and weight-1 rows correspond exactly to sold quotes for three of the four sites (Kitecompare 112,311 = 112,311; Brightquote 73,105 = 73,105; Pricelark 55,720 = 55,720); for Covertide the raw weight-1 row count (89,682) exceeds the matching sales count (89,586) by 96, which traced to 118 duplicate `ref` rows in that one JSONL file (a real, localised data-quality defect, not present in the other three files) — after dropping duplicates, the match is exact there too. So "weight" effectively flags whether a quote converted, and counting raw rows instead of using the weight (or missing the Covertide duplicates) would misstate conversion; this is squarely a hygiene/read-the-field item, not a hidden judgment call.
i. **Should the over-65 cut go ahead.** A genuine recommendation built on (f) and (g) together (and the 75% threshold), in the spirit of PLN-2027-03 6.3's escalation sentence; it is a real decision once the upstream figures are right, not a lookup.

So difficulty is spread across modelling (a, b, c, f), cross-file causal synthesis (g), data assembly/hygiene (h), direct evaluation (d, e), and recommendation (i); no single fact collapses more than one or two of these at a time.

### Realism tells

Nothing in the pack reads as LLM-narrated or placeholder: no "test", "dummy", "TODO", "lorem", "synthetic", "generated" or similar token anywhere, no hidden/very-hidden worksheet, no cell comments, no tracked-changes or revision parts inside any of the four `.xlsx` files, and no PDF has more than its stated one page. Things that read as deliberately realistic rather than as tells:
- Four comparison-site quote files in four different shapes: semicolon-delimited with pence integers and day-first timestamps (Brightquote), comma-delimited with ISO local timestamps (Kitecompare), comma-delimited with explicit UTC offsets and a different reference format (Pricelark), and nested JSON Lines with epoch-millisecond timestamps (Covertide).
- `ipt_gbp` sitting at exactly 12% of `written_premium_gbp` throughout, matching the real UK insurance premium tax rate, rather than an arbitrary or rounded figure.
- Policy terms mostly but not uniformly 365 days (365, 363, 364, 362 all present in `pcw_nb_policies_sold...csv`), rather than a suspiciously uniform year.
- The weight/sampling-flag convention (full retention of sold quotes, a 1-in-50 sample of the rest) is applied consistently but independently across all four vendor files, which is plausible for a shared internal MI pipeline feeding off different vendor feeds.
- Named owners are internally consistent across unrelated files (Roy Osborne on both the model deployment log and the rate-change log; Frances Green on both the PLN-2027-03 paper and the renewal-retention MI workbook).
- Two files that look relevant but fall outside PLN-2027-03's stated scope of comparison-site new business ("Business sold direct or through brokers is outside this paper"): `direct_web_quotes_sales_2025_2026.xlsx` (direct channel) and `motor_xol_reinsurance_programme_2026.pdf` (reinsurance programme, not referenced by any of the filed figures the prompt asks about).

Minor oddities, worth a glance but not alarming: all four PDFs' internal `CreationDate` timestamps are stamped in US Eastern time (EDT/EST) for a UK mutual insurer's internal documents (plausibly just the export workstation's locale); PLN-2027-03's own stated "Date 4 November 2026" is one day after its PDF's internal creation timestamp (3 November, converted to UK time); and `renewal_schedule_2027_aged_65_plus.csv`'s youngest driver age is 66, not 65, even though PLN-2027-03 and the prompt both treat 65 as the segment's start.

### Second reader

### 1. Which sentence or file tells you how any part of the analysis should be done (a step, a comparison, an adjustment, a grouping, a population, a window)?

`PLN-2027-03_pcw_rate_plan_2027_planning_basis.pdf` is the document that does this, clause by clause. Examples, quoted exactly:

- "2.1 A segment's loss ratio is its ultimate claims, each claim capped at £100,000, at 2027 cost levels, divided by its written premium net of insurance premium tax, for the policies it writes in the year, each over its own policy year." (fixes the loss-ratio formula, the cap, the cost basis, the population and the window)
- "2.2 Claims at 2026 cost levels are taken to 2027 cost levels by raising them 5.5 per cent." (the trend adjustment)
- "2.3 Halvergate's 2027 premium for a risk is the premium the rates in force on 31 October 2026 give it, with the segment's 2027 change applied; the pricing model's claims-cost index stays at its 2026 level through 2027." (the premium basis and an explicit freeze on the claims-cost index)
- "4.1 The comparison sites are taken to return 2027 quotes in the number and mix they returned from 1 February 2026 to 31 October 2026, scaled to twelve months." (the 2027 quote-volume window, population and the scaling step)
- "4.2 Rivals' prices on the sites are taken to rise 2 per cent on 1 January 2027 and not to move again during 2027." (the competitor-price assumption)
- "5.1 A segment's change is the smallest change, in whole per cent, at which the expected loss ratio of its 2027 comparison-site new business is 75 per cent or below." (the search rule behind "the smallest rise")
- "5.2 Where a range is given for a loss ratio it is the range within which 80 per cent of the year's outcomes would fall: the claims the year's policies bring, drawn policy by policy, around the expected loss ratio." (defines the 80 per cent range as a policy-level draw around the expected loss ratio)
- "6.1 Underwriting profit is written premium net of insurance premium tax, less capped claims at 2027 cost levels, less the site's commission on each sale (PCW-COM-2026, unchanged for 2027) and less servicing of £34 a policy." (the profit formula and its cost components)
- "6.2 A segment's 2027 underwriting profit counts its comparison-site new business written in 2027 and its customers first sold through a comparison site who renew in 2027, as the 2027 renewal schedule lists them." (the population for the profit figure: new business plus comparison-site-sourced renewals)

`CMP-RP-04_renewal_pricing_policy.pdf` adds the renewal-side rule: "3.1 At renewal the premium offered to a customer may not exceed the equivalent new-business price... 3.2 The renewal system compares each renewal premium with its equivalent new-business price before the invitation is issued and reduces the premium to that price where it is higher." This is the "cap" the prompt's phrase "the renewal book it caps" refers to.

`PCW-COM-2026_comparison_site_commissions.pdf` fixes the commission figures feeding 6.1: "Commission is payable to the site on each policy sold through it, net of policies cancelled within the 14-day cooling-off period," with a £44-£55 per-policy rate by site.

### 2. Which file already ranks or scores the options on the prompt's question?

None. No file ranks or scores "21 per cent vs. some other under-25 rise," the 25-to-64 rise, or "cut vs. no cut" for over-65. The four comparison-site files (`kitecompare_market_position...csv`, `pricelark_insurer_quotes...csv`, `brightquote_quote_report...csv`, `covertide_mi_quotes...jsonl`) each carry a rank/position field (`halvergate_position`, `position`, `Rank`, `rank`), but that ranks Halvergate's own quoted premium against rival quotes for one individual risk at one moment, not the pricing options the prompt is weighing. `pcw_rate_change_log_2024-2026.xlsx` logs past rate changes by segment and date but carries no outcome (loss ratio, profit) next to them, and has no 2027 row.

### 3. Which file exists only to help the analyst, rather than being a record the organisation would keep for its own work?

I did not find one that reads as purely a solver's aid (no glossary, FAQ, or worked example). The closest candidates are the two files scoped narrowly to the exact cohort the open question is about: `renewal_schedule_2027_aged_65_plus.csv` and `renewal_retention_mi_65plus_2025-2026.xlsx`. A real renewal or retention system would more naturally produce one schedule/MI pack across all ages rather than a pre-filtered 65-and-over cut; both are plausible, though, as a report the pricing or retention team pulled deliberately because that is the book under review for the proposed cut, and `renewal_schedule_2027_aged_65_plus.csv`'s three premium columns (`intended_renewal_premium_gbp`, `enbp_at_current_nb_rates_gbp`, `renewal_premium_offered_gbp`) match exactly the three figures CMP-RP-04 4.1 says the renewal team keeps for every renewal ("the premium intended, the equivalent new-business price at the date of the schedule and the premium offered"), which argues for it being a genuine extract rather than a convenience file.

### 4. Which figure or name in the pack reads as the answer rather than as context?

Nothing reads outright as the final answer. The nearest thing is `renewal_schedule_2027_aged_65_plus.csv`'s pre-computed cap: for every row, `renewal_premium_offered_gbp` equals the smaller of `intended_renewal_premium_gbp` and `enbp_at_current_nb_rates_gbp` (verified row by row). This shows the cap mechanism already executed, but only "at current nb rates," i.e. the baseline before any 2027 change, not under the proposed over-65 cut. Recomputing the equivalent new-business price under the cut, and what that does to the capped renewal premiums and to underwriting profit, is left to the solver. So this column reads as a correctly-motivated input (and matches CMP-RP-04's stated recordkeeping), not as the answer to "should the cut go ahead."

### 5. Which filed sentence, read literally, fixes how any figure the prompt asks for is computed, or over which population or window?

(Repeating/consolidating from Q1 with what each fixes, in words, no numbers computed):

- PLN-2027-03 2.1 fixes the loss-ratio formula itself: ultimate claims (capped per claim), at 2027 cost levels, over net written premium, for the policy-year cohort that writes in 2027.
- PLN-2027-03 2.2 fixes the trend used to move 2026-level claims to 2027-level claims.
- PLN-2027-03 2.3 fixes which rate base (31 October 2026 rates plus the segment's change) produces "Halvergate's 2027 premium," and freezes the claims-cost index rather than letting it move with the trend.
- PLN-2027-03 3.1 fixes the experience window: policy/claims extracts as at 31 October 2026, reserving triangles to 30 September 2026.
- PLN-2027-03 4.1 fixes the population and window used to build the 2027 quote volume (1 February to 31 October 2026, scaled to a year) and assumes the mix repeats.
- PLN-2027-03 4.2 fixes the competitor-price path for all of 2027.
- PLN-2027-03 5.1 fixes what "the smallest rise" means operationally (an integer-per-cent threshold search against the 75 per cent target).
- PLN-2027-03 5.2 fixes what the "80 per cent range" is a range of, and that it comes from a policy-by-policy draw, not a different definition of volatility.
- PLN-2027-03 6.1 fixes every deduction underwriting profit takes (claims, commission, servicing) and excludes anything not listed (e.g. no reinsurance line).
- PLN-2027-03 6.2 fixes the population for the profit figure as new business plus comparison-site-origin renewals in 2027, i.e. it is explicitly not new business alone.
- CMP-RP-04 3.1-3.2 fixes the renewal-premium cap rule (never exceed the equivalent new-business price) and that the comparison happens before invitation.
- PCW-COM-2026 fixes the per-site commission amount and that it nets out 14-day cooling-off cancellations.

### 6. Is there one thing that would make most of what the prompt asks for routine?

Two candidates, neither of which gets there alone.

(a) A pattern in the data, not a sentence: every comparison-site quote file (`kitecompare_market_position...csv`, `pricelark_insurer_quotes...csv`, `brightquote_quote_report...csv`, and `covertide_mi_quotes...jsonl`) carries a weight column (`extract_weight` / `sampling_weight` / `Weight` / `weight`) that takes only two values, 1 or 50, and is never explained in any document. Checked directly: every weight = 1 row's quote reference is exactly a row in `pcw_nb_policies_sold_2025-01_2026-10.csv` (the quote that was sold), and weight = 50 rows are a 1-in-50 sample of quotes that were not sold (confirmed for Kitecompare: 112,311 weight = 1 rows match 112,311 Kitecompare sales 1:1; weight = 50 rows match 0). The same relationship holds for Brightquote and Pricelark (exact row-count matches) and for Covertide (exact match once duplicate quote references are collapsed). A reader who just counts rows without the weight would wildly overstate conversion and understate total quotes. Catching this would fix the base for "our 2026 quotes, sales and conversion so far by segment" and for the 2027 quote-volume projection that PLN-2027-03 4.1 is built on (since 4.1's window is read from the same files), but it says nothing about the claims, elasticity, loss-ratio or underwriting-profit figures.

(b) PLN-2027-03 taken as a whole: reading it fixes the WHAT for nearly every figure (listed in Q5), so a reader who skips it risks using the wrong cap, trend, window, index treatment, or profit population almost everywhere. But it does not supply the HOW for any of the harder pieces: it does not give a demand/conversion model for how a price rise changes the mix and volume of business Halvergate wins against rivals (that has to be built from the rank/position fields across the four site files), it does not give segment loss costs or claims development (the reserving-triangle workbook, `reserving_triangles_2026Q3.xlsx`, is whole-book and starts at accident quarter 2021Q1, with no age split, so a solver has to recognise it only supplies development patterns, not segment-level ultimate claims, and has to apply those patterns to the comparison-site segment's own, much shorter, claims history), and it does not give the size of the renewal-book cap effect under the proposed cut (that has to be rebuilt policy by policy from `renewal_schedule_2027_aged_65_plus.csv` at the new rate, then combined with the new-business volume effect of the same cut).

So no single thing resolves most of the chain. Per thing the prompt asks for:

- "the smallest rise... for each segment's loss ratio to come in at 75 per cent" (under-25, 25-to-64): genuine analysis. The target rule is stated (5.1), but the expected loss ratio at a hypothetical price is not; it needs a demand/conversion model built from the quote-level rank data, a segment claims-cost estimate that accounts for the HPM v6 to v7 model change for the 25-to-64 group (visible in `pcw_nb_policies_sold...csv`'s `rating_model` field and documented in `hpm_model_deployments.txt`), and claims development from the whole-book triangles applied to the segment.
- "the 2027 loss ratio, policies and written premium... we should expect at it": genuine analysis, a direct output of the same model once built.
- "an 80 per cent range on the 25-to-64 loss ratio": genuine analysis for the method (the target is defined by 5.2, but not the distribution or simulation that produces it).
- "the 2027 loss ratio of under-25 business at the team's 21 per cent": genuine analysis, but a lighter lift than the "smallest rise" version, since it reuses the same model at a given input rather than searching for one.
- "how many policies the team's under-25 rise and the over-65 cut would each write": genuine analysis, again from the same demand model, evaluated at two given price points.
- "what the over-65 cut would do to 2027 underwriting profit": mixed. The profit formula and its population are a stated procedure (6.1, 6.2), and the renewal cap itself is a stated rule (CMP-RP-04 3.1-3.2) already shown worked at baseline rates in the pack; but sizing the effect is genuine analysis, since it means re-deriving the equivalent new-business price under the cut for the renewal book and combining that with the modelled new-business volume effect of the same cut.
- "should the 3 per cent cut... go ahead": a synthesis/decision call on top of the above, genuine analysis, not resolvable by any single rule.
- "our 2026 quotes, sales and conversion so far by segment": partly a matter of correctly reading/joining the files (reconciling four different schemas, delimiters, units and timestamp conventions, listed below) and partly catching the undocumented weight/sampling pattern described in (a) above; once both are handled correctly it is closer to routine than the other asks, though cross-file reconciliation at this scale is still real work.

I did not find anything that depends on catching a planted decoy (a copied block, a mislabelled column, a wrong denominator) as such; the closest things to "catch this or the figure is wrong" are the undocumented weight column (a measurement issue, and a realistic one, not a labelled trap) and the unit/format differences between the four comparison-site files (see below), which are visible in the column headers themselves.

### Realism tells and internal inconsistencies

- Quote references across the four independent comparison-site files interleave sequentially within the same time window (e.g. on 2025-01-01, Covertide's `CT-20250101-208875`, Brightquote's `BQ300208876`, then Covertide's 208877, 208878, Pricelark's `PL/202501/208883`, Kitecompare's `KC25010208882`/208888/208889, with the numeric suffixes forming one shared, interleaved global sequence). Four unrelated competing comparison sites would not share one incrementing reference counter in reality; this reads as a generator artefact rather than four independent companies' own numbering.
- Units differ by file in a way that is labelled but easy to miss: `brightquote_quote_report...csv`'s premium fields are in pence (`PremiumPence`, `Comp1Pence` etc.), while `kitecompare_market_position...csv` and `pricelark_insurer_quotes...csv` use pounds (`halvergate_premium_gbp`, `price`), and Covertide's JSON lines (`quotedPremium`) are also pounds.
- Timestamp conventions differ across the same four files: Kitecompare uses `quote_time_local` (an ISO local timestamp), Pricelark uses `created_utc` (explicit UTC offset), Covertide uses `ts` (Unix epoch milliseconds), and Brightquote uses `QuoteDate` as a bare `DD/MM/YYYY HH:MM` string with no timezone marker.
- `reserving_triangles_2026Q3.xlsx` is a whole-account set of triangles (five peril types, each "notified" and "incurred") with accident quarters from 2021Q1, no age/segment split at all; it sits at a different grain from every other file in the pack, which is all comparison-site, 2025-onward data.
- `renewal_schedule_2027_aged_65_plus.csv` has no IPT (insurance premium tax) column, unlike `pcw_nb_policies_sold...csv`, which separates `ipt_gbp` from `written_premium_gbp`; whether the renewal file's premium fields are gross or net of IPT is not stated anywhere in the pack.
- Claims incurred spike broadly across almost every peril type in December 2025 and January 2026 (roughly 1.5-2x the all-period monthly average for Windscreen, Third-party property, Accidental damage, Third-party injury and Theft). Checked by segment: the spike hits under-25, 25-to-64 and 65-and-over roughly proportionally (1.5x-2x each), so it reads as a genuine, broad winter-weather-type pattern rather than something confined to one deciding segment.
- `pcw_nb_policies_sold_2025-01_2026-10.csv` carries a `member` Y/N flag (about 6.7% Y) that is not mentioned or defined in any document; it appears roughly proportionally across all four channels and across the whole date range, with no visible break, so it reads as benign texture rather than a planted factor.
- A small number of rows (2,023 of 330,722, about 0.6%) in `pcw_nb_policies_sold_2025-01_2026-10.csv` have inception dates in November 2026, past the file's own "2026-10" label and past the 31 October 2026 extract date PLN-2027-03 3.1 states; all of them are still in 2026, consistent with a normal quote-to-inception lag (e.g. a policy quoted in late October incepting 1 November) rather than any 2027 business already being on risk, which matches the prompt's "before any of that business is written."
- Document metadata is internally varied in a way that reads as authentic rather than templated: the four PDFs each carry a different LibreOffice Writer version and distinct creation timestamps, and the four XLSX files have different named creators (Roy Osborne, Frances Green, Jeremy Sanders, "Distribution MI") with created/modified timestamps consistent with the filesystem dates. No hidden worksheets were found in any workbook.
