# determinism-check report, task601, 2026-11-07

## Verdict
DETERMINISTIC

**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why

The isolated judge thread (fresh unzip at `/tmp/determinism-check-task601-1794085716/target/`, blocks inlined, no access to `submission.md`, `DESIGN_NOTE.md`, `metadata.json`, the generator, or this report) independently recomputed the headline chain and reproduced it to the digit or to immaterial rounding: campaign members 3,534 (joining `signup_attribution...csv` to `billing_events...csv` inside the standard's Berlin-day window, handling the mid-2025 `amount`/`amount_minor` column change), live members 31 October 3,013, new-tutor exposure 2,757/3,013 = 91.5 per cent, September/October joiner split 1,718/1,816, and campaign cost EUR 868,162 against the claimed EUR 868,150 (a 0.0014 per cent gap that rounds to the same EUR 868,150 at nearest-25). No decisive fact is missing from the shipped files and nothing in them contradicts the call; both the 80 and 90 per cent cost ranges clear the EUR 800 bar with margin, so Gate C's near-tie test is not triggered. The one gap the thread flagged on its own initiative is that it did not re-run the full member-by-member Monte Carlo behind the point estimate and the ranges, given every other figure it checked reproduced; I treat this as a reasonable stopping point rather than a finding, since every component value it did check (the tutor stop-by-months-taught table, the 61.7/26.7 per cent cancellation shock) landed close to the filed figures.

## Recomputation ledger

| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Campaign members | 3,534 | 3,534 (after handling `amount_minor`) | yes, exact |
| Live members 31 Oct | 3,013 | 3,013 | yes, exact |
| New-tutor exposure | 2,757 / 3,013 (91.5%) | 2,757 / 3,013 | yes, exact |
| Sep/Oct joiner split | 1,718 / 1,816 | 1,718 / 1,816 | yes, exact |
| Campaign cost | EUR 868,150 | EUR 868,162 | yes, both round to EUR 868,150 at the prompt's nearest-25 rounding |
| Tutor stop rate, months 4/5/6 | 21.3 / 26.0 / 24.8% | 21.7 / 26.0 / 24.5% | close, not exact digit-for-digit but within the generator's own stated precision |
| Tutor stop rate, 13+ months | 0.8%/month | 0.83%/month | close |
| Tutor count | 798 | 798 | yes, exact |
| EUR 900 point estimate / 80% range EUR 850-975 / 90% range EUR 825-1,000 | as filed | not independently re-simulated (judge's own scope limit) | not attempted, but every input feeding it reproduced |

## Competing answers that survived

None. The rival "membership-month" retention curve (EUR 725, books the re-run) is real and is disclosed and ruled out in the solution's own fork table with named data (the 172 tutors started September/October 2026 against 7 earlier, and the 91.5 per cent new-tutor exposure), not by an unstated assumption. The judge confirmed this fork closes on data, not on an arbitrary reading, and that both the 80 and 90 per cent uncertainty ranges stay clear of the EUR 800 bar, so the call is not margin-fragile.

## Spec gates

| Gate | Required | Actual | Pass |
|---|---|---|---|
| Usable files | 10 or more | 11 (billing_events, ecb_rates, eurostat, fenwright xlsx, growth_review pdf, lesson_activity, members_export, nps, plans_and_promotions json, signup_attribution, tutor_directory) | yes |
| File categories | 2 or more | spreadsheet (8 CSV + 1 xlsx), document (1 PDF), config/structured (1 JSON) = 3 categories | yes |
| Large messy CSVs | 1 of 20,000+ rows, 1 of 10-20 printed pages | billing_events (203,776 rows, 23 MB, webhook-replay duplicate event_ids, a mid-stream amount/amount_minor column rename) and lesson_activity (169,309 rows, 7.4 MB); signup_attribution (50,731 rows) and members_export (24,407 rows) also clear 20,000+ rows comfortably, so the 10-20-page tier is cleared many times over | yes |
| metadata.json distractors | 2 or more named, none labelled inside the ZIP | eurostat_edat_aes_l21_foreign_languages_known.csv and nps_in_app_responses...csv named in metadata.json; neither is referenced, flagged, or named as a distractor inside any shipped file | yes |
| Distractors relevant but unused | each weighs, none reproduces a graded quantity | Eurostat foreign-languages data is domain-adjacent (a language-tutoring platform) but plays no role in any committed figure; NPS scores are a plausible growth signal but unused; the judge's independent hygiene pass found neither referenced by any committed answer | yes |
| Deliverables | 1-3, all present in golden, no format family required | 2 requested (`aut26_rerun_memo.docx`, `aut26_member_forecast.xlsx`), both present in `golden/`, two different formats | yes |
| Asks multi-dimensional, unit+rounding stated | yes | prompt states "Give member counts to the nearest 50 and euro amounts to the nearest 25"; each of the 6 supplementary asks is multi-dimensional (a population count, a cost with two uncertainty ranges, a break-even cost, a two-series-plus-reference-curve chart, an 11-month x 3-column grid, four further sheets) | yes |
| Answer shape, many gradable cells downstream of the deep step | yes | the forecast workbook is an 11-row x 3-column grid (33 gradable cells) plus a joining-month summary, a cost build-up and a per-member projection sheet, all of which only change once the tutor-survival projection replaces the membership-month curve | yes |
| Golden ZIP holds exactly the requested files | yes | golden/ contains exactly `aut26_member_forecast.xlsx` and `aut26_rerun_memo.docx`, matching the two files the prompt names, nothing extra | yes |
| Nothing LLM-generated; goldens read as real work product | yes | docx core properties: creator "Marit Klemt", a named stakeholder from the card, Microsoft Office Word app properties (Pages 2, Company "Corvane Sprachen GmbH"), ordinary creation/modification timestamps 2026-11-06; body text is a plain internal memo ("To Caroline Ritter. From Marit Klemt. 6 November 2026.") with no boilerplate, no meta-commentary, no "generated"/"benchmark" language in content (the only "generated" string hits were inside standard docx stylesWithEffects.xml/styles.xml boilerplate, not content) | yes |

## Gate G reconciliation

Thread: `mechanism: method_or_model_selection`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`.
Card/design note: `stump_class: "analytical"`, `strategy_label: "WORKS IN FORM"` (heterogeneity that pooling hides, weighted to the forward group's tutor-tenure mix, plus outcomes not yet finished), `gate_g: "forecasting"`.

These agree. The thread independently named the same mechanism the design note built for: a real, honestly-computed, historically-validated membership-month retention curve that simply omits a heterogeneity driver (tutor tenure) this specific cohort has in an atypical proportion, not a planted defect or a misleading reported number. The thread did not name the declared distractors (Eurostat, NPS) as load-bearing or as the surface read carrying the task, so there is no finding that a distractor is too load-bearing. `gate_g: "forecasting"` on the card versus the thread's `method_or_model_selection` is a labelling difference, not a substantive mismatch: both land in the FINE-numbers, non-surface-read-rejection family, and the design note's own Deep reasoning section frames the decisive step as "carrying each member through their tutor's survival instead of their own tenure," i.e. a model-selection/forecasting hybrid, exactly what the thread describes.

## Stump power (Gate F)

The thread rates the naive membership-month curve as a trap a strong model would plausibly reach for by reflex: it is internally consistent, backtests conservatively on two real past campaigns (28.7% vs 33.3% kept on SPR25, 30.6% vs 33.5% on last autumn's joiners), and uses only "obviously relevant" fields (the billing history). Missing that AUT26's member mix is unusually concentrated on brand-new tutors (172 new tutors in September-October 2026 vs 7 in the prior six months, discoverable only by joining `lesson_activity_monthly` to `tutor_directory` and tracking each tutor's own tenure) is the kind of miss the design note frames as the field's reflex method sitting at rung 0. The design note additionally classes the decisive step as a landed call built on the library's standard retention method extended with a genuine judgment (tutor-clustered resampling for the uncertainty ranges), which per this skill's guidance on textbook-method stumps (the field's named method is the opponent's first move, `stumping` 1.3) is recorded as a legitimate rung the main thread should weigh against the design note's ladder, not a disqualifying finding.

## Findings, ranked

1. (Minor, informational) The judge thread did not independently re-run the full member-by-member Monte Carlo simulation behind the EUR 900 point estimate and the 80/90 per cent ranges, citing scope; every input feeding that simulation (the tutor stop-by-months-taught table, the 61.7/26.7 per cent post-tutor-stop cancellation shock, the 798-tutor count) did reproduce closely. This is not a disqualifying gap given the volume of exact reproduction elsewhere, but a full re-simulation would be the next thing to check if any future pass wants higher confidence in the exact EUR 850-975 and EUR 825-1,000 range boundaries.
2. (None rising to a send-back or fix-now level.) No competing defensible answer, no missing decisive fact, no margin fragility, no banned stumping type, and no Gate H failure were found by either the isolated thread or this reconciliation pass.

## Next action for the author

None required; the build is clear to proceed to stage 5 (READY) on the determinism side. If extra assurance is wanted before shipping, re-run the member-by-member Monte Carlo simulation independently (finding 1) to confirm the EUR 850-975 / EUR 825-1,000 range boundaries to the same precision as the point estimate, but this is optional polish, not a blocking defect.
