# leak check, task9

**Verdict: REVIEW.** 29 files read, 46 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: family, replicate, missed, bootstrap, calendar, instrument, variance, manifests, training, window, turnover, revisions, snapshot, record, thirteen, releases, optimisation, spread, rollouts, dropped, independent, release, component, retunes, hurried

## 2 author vocabulary (REVIEW 1)
- **REVIEW** `gms_model_stability_standard_2026.pdf`: \bthe model\b x6: ...aces version 1 of 3 November 2025 1. Scope 1.1 This standard sets how the model risk committee places each model-side source of movement in the Garra...

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `acquirer_agreement_schedule_c_tier_stability.pdf`: 3 of 25 stump-paragraph terms appear (family, snapshot, thirteen); read whether the document names the move
- **REVIEW** `gms_model_stability_standard_2026.pdf`: 9 of 25 stump-paragraph terms appear (family, training, revisions, snapshot, record, releases); read whether the document names the move

## 9 dates after the setting (REVIEW 2)
- **REVIEW** `feature_platform_roadmap_2027.xlsx`: 24 ISO dates after 2026-11-25, e.g. 2026-12-28, 2027-01-04, 2027-01-11, 2027-01-18, 2027-02-08
- **REVIEW** `labelled_row_plan_2027.xlsx`: 57 ISO dates after 2026-11-25, e.g. 2026-11-30, 2026-12-07, 2026-12-14, 2026-12-21, 2026-12-28

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 12 client quality check (INFO 2)
- **INFO** `-`: 29 usable files (10 or more required)
- **INFO** `-`: 3 file categories: document, spreadsheet, structured (2 or more required)

## 1 file names (clean)

## 3 answer figures in the pack (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)


## Solver's-eye read

### First pass (the whole pack, 22 November 2026, before standard 3.2 and 5.2 were pinned)

1. Method instructions. The prompt does not say how to compute anything. The standard PDF defines what each result is, not a step. The nearest to a method is: "A source's movement is the root-mean-square change in a merchant's score between two consecutive quarter-end snapshots that the source alone produces, every scored merchant counted once and each model family weighted by its scored merchants at the latest quarter-end snapshot" (§3.1). It also says "5.2 Merchants' own change is the mean-square change in a merchant's score over thirteen weekly refreshes in the record, less the model-side sources' mean-square movements as they stood in the record." That is a subtraction recipe for merchants' own share. Also "2.1 ... roadmap ... and ... plan for that year as filed". §6.1 says the "removed" scenario takes out "the movement of every source placed in a remediation plan or escalation ... in full". Schedule C4.1 gives the panel rule: "A share of tier changes between two snapshots counts the panel merchants scored at both."

2. Ranking file. None. Bands exist in the standard (§4.1: Monitor under 5.5, Remediation 5.5 to under 8, Escalation 8 or more), but nothing scores any source. covenant_tier_change_monitor_2026.csv gives per-family 2026 tier-change rates (e.g. HLTH 15.24%), which is context, not a ranking.

3. Help-only file. None obviously. The nearest candidates are gms_model_performance_weekly.csv, feature_drift_psi_weekly.csv, training_compute_by_run.csv and warehouse_labelled_rows_weekly.csv. They read as context or distractors.

4. Answer-like figures or names. Nothing reads as the answer. The band thresholds and the 12 per cent cap are rules. The 2026 monitor rates look like results, but they are for 2026, not the asked 2027 quantities. The Tolka Pay migration file is a pure data-hygiene file.

5. Literal sentences that fix a figure's computation or population.
- §3.1 above. Literal reading: per source, take the RMS of that source's own score change per snapshot pair, count each merchant once, and weight families by their scored merchants at the latest snapshot. The roadmap workbook's "Book" sheet in labelled_row_plan_2027.xlsx (column scored_merchants_dec_2027) is the evident weight.
- §3.2: "the expected movement over the four snapshot pairs that close in that year". Literal reading: the four 2027 pairs, using the snapshots Schedule C2.1 lists (22 Mar, 21 Jun, 20 Sep, 20 Dec 2027).
- §5.1: "mean-square movement as a share of the sum of the model-side sources' mean-square movements". Literal reading: each source's share is its mean square divided by the sum of the five.
- §5.2: merchants' own mean-square over 13 refreshes minus the sources' mean squares, reported as a share of the sum of all movement.
- §6.1 and Schedule C3/C4: tier changes are counted on the panel merchants scored at both snapshots, with the C1.1 tier cut-offs. The "removed" case sets the in-plan and escalated sources' movement to zero.
- C4.1 plus the Tolka Pay migration file, which re-keys merchant ids: the "scored at both" rule means ids must be reconciled.

6. Single thing that makes most of it routine. Candidate: the paired-run instrument pairs (mrm_instrument_pair_register_2026.csv and mrm_instrument_pair_scores_2026.csv, with pair kinds replicate, bootstrap, label_freeze, release_shadow, retune_shadow). Each kind maps one-to-one onto a model-side source. This is the most visible pattern and it hands over a per-source measurement, but only for 2026 and for the families and refreshes covered. The prompt asks for 2027 expectations, so the files do not settle them. The standard's source list, the scheduler jsonl's options.feature_views field and the platform calendar's "Pinned feature views" row (14 families, 14 scheduled) handle the pinned share. That share needs a forward schedule (roadmap, calendar), so it is not a single lookup. No single sentence makes most of the asks routine.

Per part:
- Points each source moves: analysis (estimating and forward-projecting source effects from partial instruments).
- Band: depends on the above, then reads a stated rule.
- Share of model-side movement: follows from the stated §5.1 rule, with analysis for the inputs.
- Merchants' own share: a stated procedure (§5.2) plus analysis.
- Share of retrains on pinned feature views: a read of the calendar and scheduler options plus forward weighting, mostly forward arithmetic.
- Tier-change share and the counterfactual: analysis on the score panel. Following the cap, tiers and panel definition is rule application; the estimate itself is analysis.
- Nothing looks planted. The risk is that the filed definitions (§3.1, §5.2, §6.1) are executed literally.

Rulings
- REVIEW gms_model_stability_standard_2026.pdf "the model" six times: harmless, because it is generic phrasing ("the model risk committee", "the model registry", "a feature group a family's model reads") and gives away no result or method.
- REVIEW feature_platform_roadmap_2027.xlsx, 24 ISO dates after 2026-11-25: harmless, because these are the filed forward roadmap that the standard (§2.1) names as the assessment year's input. They are planned release weeks, not outcomes.
- REVIEW labelled_row_plan_2027.xlsx, 57 ISO dates after 2026-11-25: harmless, because they are the planned label weeks (57 rows) the standard (§2.1) names as the filed plan. They are inputs the forward estimate needs.

Realism notes
- gms_monitoring_panel_roster.csv: every panel_from is 2024-07-01 and every last_scored is 2026-11-23 (the tail and head rows I read), which looks uniform and generated. Several families also appear with a different acquirer mix per file row, so check. The roster's last_scored of 2026-11-23 sits after the latest score file (2026q4 begins 2026-10-05), which is fine, but note the pack date is 2026-11-22.
- training_scheduler_runs_2024_2026.jsonl: the options.feature_views value is "live" for every kind I tallied, so the pinned views the prompt asks about must come from the calendar and the config, not this field. Verify.
- The calendar's completed_on dates look random relative to planned_week (e.g. a week-29 change completed in August), which reads synthetic.
- Roadmap owners are only two names, and release refs are strictly sequential. This is mild and tolerable.
- No file name names a trap. mrm_instrument_pair_* is the most revealing name; it says "pair", which previews that pairs are the instrument. This is a mild structural hint, not a result.
- Both PDFs read as human-authored governing documents with owners and approval dates, not machine-written.

### Second pass (the stability standard as shipped, 22 November 2026)

1. Method sentences. The prompt names no method. The standard defines the quantity but does not give a procedure. Sentences that fix what is computed:
- 3.1: "the root-mean-square change in a merchant's score between two consecutive quarter-end snapshots that the source alone produces, every scored merchant counted once and each model family weighted by its scored merchants at the latest quarter-end snapshot."
- 3.2: "the root of the mean of the source's expected mean-square changes over the four snapshot pairs that close in that year, the snapshots being those of the covenant schedule."
- 5.2: "mean-square change... over the snapshot pairs that have closed in the year the assessment is made, less the model-side sources' mean-square movements over those pairs as they stood then. It is carried into the assessment year as it stands."
- 6.1: "the movement of every source placed in a remediation plan or escalation taken out in full."
- 2.1: the assessment year's releases are the roadmap and its training rows are the plan.

These pin population, window and unit (WHAT). They do not say how to estimate a source alone, so the HOW stays open. The weakest point is 5.2, which says how the own-change quantity is built. It names no estimator for the model-side terms.

2. Ranking file. None. The standard states band thresholds (4.1) but no file scores any source. The covenant schedule gives the 12 per cent cap and the tiers, not a ranking.

3. Files that exist only to help the analyst. None found. The standard and the schedule read as governing documents. The roadmap and the plan are filed inputs under 2.1.

4. Figures or names that read as the answer. None. The 5.5 and 8 point thresholds and the 12 per cent cap are decision parameters, not results. No file shows a per-source movement or a tier-change share.

5. Filed sentences that fix a graded figure, read literally:
- 3.1 weights families by scored merchants at the latest quarter-end snapshot. This fixes a merchant-weighted pooling, each merchant counted once.
- 3.2 fixes the 2027 movement as the root of the mean over the four 2027 snapshot pairs. Those pairs are 22 Mar, 21 Jun, 20 Sep and 20 Dec. The pair closing on 22 March starts from the 21 December 2026 snapshot.
- 5.1 fixes each source's share as its mean-square over the sum of the five model-side mean-squares.
- 5.2 fixes merchants' own change. It is the total mean-square change over the pairs closed in 2026, less the model-side mean-squares over those pairs, carried unchanged into 2027. Its share is own over (own plus the 2027 model-side mean-squares).
- 6.1 and C4.1 fix the tier-change population as panel merchants scored at both snapshots, with tiers at 400, 500 and 600. The counterfactual removes a source's movement "in full" for every source placed in a plan or escalation.
- 4.1 fixes the bands at under 5.5, 5.5 to under 8, and 8 or more.

Each of these is a definition or convention, not a result.

6. The one-thing test. I find no single file, sentence or column that would make most of the asks routine. The closest candidate is 5.2 together with 3.2. They tell a solver that own change is a residual and that 2026 pairs are the base. That settles one ask (merchants' own share) and its definition only. It leaves unsettled the per-source movements, the pinned-views share and the tier-change share, which need estimation. Each ask turns on analysis (estimating a source's isolated contribution from records that carry all sources at once, forecasting 2027 from the roadmap and plan, and a tier-change model). None turns on one field or code. Two points rest on reading definitions correctly: the weighting in 3.1, and "as they stood then" in 5.2. These are filed in plain words, so they are rule-following rather than planted. Nothing in the standard looks planted.

Rulings on the three swept lines:
- "the model" six times in the standard: harmless. It is ordinary phrasing for the scored model, and the model-side/merchant-side split is the prompt's own vocabulary. It hands over no result or method.
- feature_platform_roadmap_2027.xlsx, 24 dates after 25 November 2026: harmless. Section 2.1 makes this file the assessment year's filed input. Its dates (28 Dec 2026 to 2027) are future-dated by design. It is one visible sheet, 24 rows, with release_ref, refresh date, feature groups and families touched. No outcomes are shown.
- labelled_row_plan_2027.xlsx, 57 dates after 25 November 2026: harmless. Section 2.1 makes it the filed plan for the year, with weekly planned label counts per family from 30 Nov 2026 (the later dates are a forward plan). The Book sheet gives scored merchants per family at December 2027. That feeds the 3.1 weighting and is filed input, not an answer. Both sheets are visible.

### Main thread's rulings

- Question 1, both passes: the sentences quoted are the standard's and the covenant schedule's definitions of each result (population, window, unit, comparison), filed by design; none names a step of a decisive judgment (what a bootstrap or replicate pair measures at the snapshot gap, or how a rollout is taken up). Harmless.
- Question 5, both passes: every literal reading executes to the golden or to a figure inside its band. 3.1 gives the book at the 21 September 2026 snapshot; the plan's December 2027 book, which the first pass called the evident weight, is a battery variant inside every band. 3.2 gives the root of the mean over the four 2027 pairs (the golden). 5.1 gives the shares (the golden). 5.2 gives own change over the 2026 pairs less the sources over those pairs, carried into 2027 and reported against own change plus the 2027 model side (the golden's estimand; the three 2026 pairs alone give a figure inside the band). 6.1 and C4.1 give the panel merchants scored at both snapshots, with every source in a plan or escalation removed in full (the golden).
- Question 6, both passes: nothing banned. The instrument pairs the first pass names are the field's raw material and do not settle the 2027 quantities, as it says; the definitions the second pass names (3.1's weighting, 5.2's base) are the estimand, filed in plain words.
- The three swept lines (the standard's "the model", the roadmap's and the plan's dates after the as-of date): harmless, as the second pass rules. The stump-vocabulary lines are ruled in the design note's Literal reader section.
