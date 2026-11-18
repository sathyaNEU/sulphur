# leak check, task9

**Verdict: REVIEW.** 23 files read, 37 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: missed, seller, effect, ablation, served, sessions, default, telemetry, result, promise, device, market, entity, reflex, section, dismissed, evidence, component, failure, traffic, render, components, results, ranking, shares

## 1 file names (REVIEW 1)
- **REVIEW** `ranker_release_log_2026.txt`: a text file in the pack: confirm it is the organisation's own record (a thread, a log, a letter) and does not describe the data

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `ranker_release_log_2026.txt`: 3 of 25 stump-paragraph terms appear (seller, promise, ranking); read whether the document names the move
- **REVIEW** `ranking_platform_reliability_charter_2027.pdf`: 8 of 25 stump-paragraph terms appear (effect, served, sessions, result, market, section); read whether the document names the move

## 8 column names (REVIEW 3)
- **REVIEW** `component_render_hourly_2026.csv`: columns a generator names and an organisation does not: device
- **REVIEW** `edge_page_cache_daily_2026.csv`: columns a generator names and an organisation does not: device
- **REVIEW** `edge_search_sessions_hourly_2026.csv`: columns a generator names and an organisation does not: device

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 12 client quality check (INFO 2)
- **INFO** `-`: 23 usable files (10 or more required)
- **INFO** `-`: 4 file categories: database, document, spreadsheet, structured (2 or more required)

## 2 author vocabulary (clean)

## 3 answer figures in the pack (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)


## Solver's-eye read

One isolated reader (Sonnet at medium) on fresh copies of `prompt.txt` and `target/`, 2026-11-18; it read all 23 files
and solved nothing. Its answers, with the main thread's ruling on each.

1. A sentence that says how: none. It quoted structure in `search_pipeline.yaml` (`overrides` resolved by user hash,
   `feature_ablation: applied_at: [rank, rerank]`, `component_holdout: applied_at: [render]`, the page cache's
   `read: every_request`, `write: requests_without_overrides`, `ttl_seconds` and its history) and in `feature_store.yaml`
   (`on_expiry: serve_group_default`, each group's `validity_hours` and `refresh`), and called each a description of the
   system that says nothing of what to do. Ruling: harmless and needed. They are the constants the estimate shares
   with the world (the note's `## Pinning list`), filed as configuration; no file says what follows from them, and
   each leaves the dependent steps of `## Stump core` (Said out loud).
2. A file that ranks or prices the groups on the question: none. The offline replay workbook and the feature
   importance table score the groups on other questions (ranking quality offline, split gain); the experiment export
   holds raw arms. Ruling: the first two are the unused files, named only in `metadata.json`.
3. A file that exists only to help: none. `feature_source_traffic_2026.xlsx` was the nearest (source weights and the
   shard renames). Ruling: harmless; it feeds the reflex route's traffic weighting and no judgment.
4. A figure that reads as the answer: none. The charter's 0.05 line is the only figure near the decision; the incident
   titles say which systems had trouble and give no size.
5. Filed sentences that fix a figure: the charter's 2.1, 2.2, 3.1 to 3.4 and 4.1, and the pipeline's stages and
   components for "every service that reads it". Ruling: executed literally they are the estimand, the window, the
   unit, the sum and the line as the answer blocks use them; none states how the counterfactual is found.
6. One thing that makes it routine: none. Its nearest candidate, the experiment export read with the pipeline file,
   is the route the estimate rejects. Shard renames, the two status vocabularies and `not_replicated` it called texture.
7. Realism: campaign names scattered across the wrong seasons and markets in `promo_calendar_2026.csv` (fixed in the
   generator: each promotion day is named for its season and market); the ablation runs' even monthly cadence (the
   pipeline configuration now files the standing rotation, `schedule: monthly_per_feature_group`, `run_days`);
   `eligible_sessions` empty outside the holdouts' control arm (as logged: eligibility is recorded where the
   component renders); shares to six decimals in the traffic workbook (a query's output, left).
8. The sweep's lines: the release log is ranking model operations' own changelog and describes no data file; `device`
   is an export's own column name (the mart says `platform`); the charter defines terms, the period and the line and
   goes no further than the definition of the cost.

### Second read, on the pack after the repair pass (Sonnet at medium, fresh copies; the pipeline configuration and the promotion calendar had changed)

1. How the analysis is done: nothing. The nearest are the charter's 3.2, 3.3 and 3.4 and the prompt's sentence that every figure has to be an estimate; the two configurations are read as architecture, "descriptive configuration" that gives no step. Ruling: harmless, the estimand and the pins.
2. A file that ranks the candidates: the offline replay workbook and the importance export score the groups on offline ranking quality and on gain, "neither ranks on the prompt's question". Ruling: harmless, both are unused.
3. A file that only helps: none; the registry, markets and regions read as reference tables.
4. A figure that reads as the answer: none.
5. Filed sentences that fix a figure: the charter's 2.1 (the quarter by the mart's business days), 2.2 (seven groups), 3.1, 3.3, 3.4 and 4.1, and the prompt's grain. Ruling: each executes to the estimand as the blocks compute it.
6. One thing that makes it routine: the charter with the experiment tables "look like a ready estimator" that would make a group's cost "close to a lookup". Ruling: that is the hurried route of step 2, which lists stock, price and seller; no planted sentence or column was named.

The three flagged items: the release log is the organisation's own operations log, the charter defines terms and never says how to estimate, and `device` reads as the edge's own column beside the mart's `platform`. All harmless.

Realism: the promotion calendar's names implied spans (a weekend on a Friday, a week on one day) while every promotion is one day. Fixed in the generator: every name is a one-day event. The reader's count of the importance export (71 rows) was wrong: it holds 77 features, as the release log says. The configuration keys it called tidy or prose-like (`write: requests_without_overrides`, the sellers' refresh scope) are pins the estimate needs and stay. No ask-figure fork, no main-call fork.
