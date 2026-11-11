# determinism-check report, task21, 2026-11-11

Re-judge pass after the stage-4 FIX_NOW: prompt.txt now names the pricing team's under-25 figure as 21 per cent
in both places (the earlier draft asked for the under-25 loss ratio "at the team's 15 per cent" after opening on
"wants 21 per cent"), the written premium's unit ("in pounds") is stated, one stray sentence was dropped from
`target/hpm_model_deployments.txt`, and the renewal schedule's ages are now the customers' ages at renewal. No
graded figure moved. This report overwrites the prior `determinism_check_report.md` per the author's instruction
for this pass.

## Verdict
DETERMINISTIC

**Disposition:** APPROVE
**Stumping type:** mechanism: mixed (method_or_model_selection / anti-selection + binding_constraint [ENBP renewal
cap] + a forecasting-style seasonal annualisation), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The isolated judge thread derived its own answer from `prompt.txt` and a fresh unzip of `target/` before ever
opening the graded blocks, and its independent figures for ask 6 (quotes/sales/conversion by segment), the
Covertide duplicate-day defect, the ZZ99 monitoring rows, the quote-weighting scheme and the ENBP renewal-cap
mechanic all reproduced exactly against the committed answers. Every decisive definition the main recommendation
and the seven supplementary asks turn on is pinned in a specific shipped file (chiefly PLN-2027-03 sections 2-6 and
CMP-RP-04 section 3); the thread found no file, clause or number contradicting the committed method or any
committed answer, and the one scope question it surfaced (whether "our 2026 quotes, sales and conversion" (ask 6)
should fold in `direct_web_quotes_sales_2025_2026.xlsx`) is closed by PLN-2027-03 1.3, which scopes the whole paper
to comparison-site business and puts direct/broker business "outside this paper." The fix that triggered this pass
(21 per cent consistently, the premium unit, the dropped deployment-log sentence, renewal ages at renewal) moved
no graded figure and the thread's independent reconstruction confirms nothing in the fixed cut created a new fork.

## Recomputation ledger

| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Under-25 2026 quotes / sales / conversion (ask 6) | 552,152 / 21,802 / 3.95% | 552,152 / 21,802 / 3.95% | Yes, exact |
| 25-to-64 2026 quotes / sales / conversion (ask 6) | 1,187,066 / 82,466 / 6.95% | 1,187,066 / 82,466 / 6.95% | Yes, exact |
| 65+ 2026 quotes / sales / conversion (ask 6) | 307,846 / 14,246 / 4.63% | 307,846 / 14,246 / 4.63% | Yes, exact |
| Quote-weighting scheme (weight 1 = sold, weight 50 = 1-in-50 unsold sample) | implicit in Step 1 | weight=1 row counts match `sales_channel` counts exactly for Kitecompare/Pricelark/Brightquote (112,311 / 55,720 / 73,105) | Yes, exact |
| Covertide 14-May-2026 duplicate day | "sent twice," deduped | 96 duplicate refs, all dated 2026-05-14; dedup turns 89,682 weight=1 rows into 89,586, matching the sold count exactly | Yes, exact |
| ENBP renewal cap mechanic | renewal price capped at new-business-equivalent price | `renewal_premium_offered_gbp = min(intended, enbp_at_current_nb_rates_gbp)` on all 165,000 rows, 0 mismatches; 79% already capped pre-cut | Yes, exact |
| HPM v6 -> v7 regime break at 1 Feb 2026, 25-to-64 only | Step 7 / Critical Component 2 | `rating_model` field switches cleanly v6 -> v7 exactly at Feb-2026 inceptions, matching the deployment log | Yes, exact |
| Chain-ladder claims-to-ultimate, anti-selection decile regression, seasonal annualisation, 1,500-draw Monte Carlo (R3-R5, R7) | 79.0%, 27%/7% rises, 72.9-77.1% range | traced to the specific licensing clauses (PLN-2027-03 2.1-2.2, 3.1, 5.1-5.2); not replayed to the final decimal given file sizes (claims extract ~51.6k rows, four quote feeds ~414k rows, renewal schedule 165k rows) | Not independently re-derived to the decimal; no contradiction found |

## Competing answers that survived

One fork was examined and closed, not left open: whether "our 2026 quotes, sales and conversion so far by
segment" (ask 6) should include `direct_web_quotes_sales_2025_2026.xlsx` (324,344 quotes / 32,424 sales across
segments, arithmetically reproducible on its own). PLN-2027-03 1.3 scopes the whole paper, and the prompt's own
opening sentence ("our comparison-site new-business rates"), to comparison-site business only; direct/broker
business is explicitly "outside this paper." Read against that filed scope clause, direct-web is the intended,
correctly-unused distractor for this ask, not a surviving competing answer. No other fork producing a second
defensible figure for any committed answer was found.

## Spec gates

| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count / categories | 10+ usable files, 2+ categories | 17 files in `target/`: 7 CSV, 4 xlsx, 4 PDF, 1 jsonl, 1 txt (5 categories: spreadsheet, database/tabular, text, document, log) | Pass |
| Large, messy files | a CSV of 20,000+ rows, and a CSV of 10-20 printed pages or more | Six CSVs clear 20,000 rows (`pcw_nb_policies_sold` 330,723; `renewal_schedule` 165,001; `kitecompare` 140,847; `pricelark` 69,795; `brightquote` 91,689; `motor_claims_extract` 51,609), all of which also clear the lower 10-20-page floor | Pass |
| Distractors named in metadata.json, not inside the ZIP | 2+ named, none labelled inside | `metadata.json` names 3 (`motor_xol_reinsurance_programme_2026.pdf`, `motor_premium_index_2019Q1_2026Q3.csv`, `direct_web_quotes_sales_2025_2026.xlsx`); no file inside `target/` contains the word "distractor," "synthetic," "generated for this task," or "benchmark" | Pass |
| Distractors unused but relevant, one load-bearing-looking | each relevant, one reproduces a graded figure and is ruled out by a shipped fact | `direct_web_quotes_sales` reproduces an alternative ask-6 figure arithmetically and is ruled out only by PLN-2027-03 1.3's scope clause (confirmed above); `motor_xol_reinsurance_programme_2026.pdf` and `motor_premium_index_2019Q1_2026Q3.csv` read as genuine adjacent context (reinsurance programme, a market premium index) that is never asked for | Pass |
| 1-3 deliverables, all present in golden, no forced format family | prompt asks "a workbook and a few slides" | `golden.zip` holds exactly `pcw_rate_review_2027.xlsx` and `pricing_committee_2027_rates.pptx`, 2 files, matching | Pass |
| Asks multi-dimensional, each with a stated unit, no rounding instruction | every ask states its unit; prompt doesn't dictate rounding | per cent, pounds and "policies" are stated explicitly for the rise/loss-ratio/premium/profit asks; the final clause ("our 2026 quotes, sales and conversion so far by segment") does not restate a unit in the prompt sentence itself (counts and a rate are implied by convention, and the answer blocks state the precision); no rounding instruction anywhere in the prompt | Minor miss (ask 6's unit is implicit, not stated) / Pass on rounding |
| Answer shape, 4+ checkable results across 3+ areas | one of fourteen shapes | "scenarios with the flip point" (DESIGN_NOTE); 8 results (R1-R8) across assembly-and-reconciliation, forecasting, causal reasoning, decomposition-and-attribution, uncertainty and synthesis (6 areas) | Pass |
| Golden ZIP holds exactly the requested files/formats | 1-3 files, requested formats | 2 files, xlsx + pptx, matching "a workbook and a few slides" | Pass |

## Gate G reconciliation

The thread classified `mechanism: mixed (method_or_model_selection + binding_constraint + a forecasting-style
seasonal annualisation)`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`,
`sole_data_defect: no`. This matches `DESIGN_NOTE.md`'s own framing: the design note's "Run forecast" section
names the hurried failures as a self-confirming check (R3), method shortcuts (R4, R5, R6, R7), and an unfinished
chain (R8) — none of them a flip away from a misleading reported number, because (per the design note's "No
decoy" and "No replay" lines) nothing in the pack states a wrong 2027 figure for the thread to catch; the
pricing team's 21 per cent and the 3 per cent cut are stakeholder positions, not planted wrong answers, and the
golden reproduces the 21 per cent exactly from the (incomplete) loss-ratio method, which is the DESIGN_NOTE's
intended self-confirming trap for R3, not a data defect. Gate G passes cleanly on both sides.

## Gate H reconciliation

| | Thread (verdict.md) | DESIGN_NOTE.md |
|---|---|---|
| domain | pass | domain test passed, swap test loses all eight results |
| layers | pass (4 heterogeneous feeds, decoy monitoring rows, aggregate triangles / rate-adequacy, anti-selection, reserving, renewal-cap decomposition, simulation) | Layer 1 and Layer 2 both named |
| results | ~10 graded across 5+ areas | 8 results (R1-R8) across 6 areas |
| one_thing | none (closest candidate, the Feb-2026 HPM regime break, is filed explicitly, affects only one result, and its fix is a seasonal annualisation, not a one-line filter) | "Not one thing": the won-book selection "is the strongest single piece," but a run that nails it still has to complete the year, choose the 25-to-64 experience window, count the renewal book and forecast volumes |
| effort | quick ~1 of 10, careful ~5-6 of 10, thorough 10 of 10 | quick 0 of 8 (0%), careful 2.5 of 8 (31%, effort.py 38.5), thorough 8 of 8 (100%) |
| one_fact | "the business a higher comparison-site price wins is the business the rating model under-priced most" rescues ~2 of 10 | same sentence rescues R3 and R4, 2 of 8 (25%) |

The one_thing finding agrees on both sides (none), and the hidden-factor record in `DESIGN_NOTE.md` independently
marks every one of its four constructed/real factors "no" on "only in deciding units," consistent with the
thread's own read that the Feb-2026 regime break is filed and sits across the whole 25-to-64 book, not only in
the units that decide the rise. The one-fact rescue count also agrees closely (2 of 8-10, roughly a quarter,
under the one-third bar both ways).

The one real divergence is the careful-but-hurried effort grade: the thread estimates a careful-but-hurried run
earns roughly 50-60 per cent of the graded results, against the design note's measured 31-38.5 per cent. Mapped
onto the checklist's reconciliation triggers, this does not cross either disqualifying line: the quick pass is
still far under a third in both readings (10 per cent against 0 per cent), and the careful pass stays clearly
below the thorough pass (not levelled) in both readings. It is worth recording as a softer margin than the design
note claims rather than a Gate H failure: the thread's own narrative attributes most of that gap to R6 (it grades
the over-65 renewal-cap effect "Partly" in its stump-power note, consistent with the design note's own "Partly"
grade for R6 under careful), so the two readings are closer in substance than the headline fractions suggest.

## Stump power (Gate F)

The thread rates stump power strong: three independently plausible hurried failures (trusting the loss-ratio
method's self-confirming 21%/74.4% for under-25s; pricing the 25-to-64 rise off pooled or latest-twelve-month
experience that blends in the retired v6 model's business instead of the post-refit window, annualised; costing
the over-65 cut on new business alone and missing the ENBP renewal-cap linkage), each tied to a real frontier-run
loss pattern (self-confirming check, narrow look at broad data / false assumption, unfinished chain) rather than a
semantic trap. This matches `DESIGN_NOTE.md`'s "Run forecast" and "Frontier check" sections, which cite the same
three failure shapes against named precedents (R3 self-confirming check L29/L22/L23; R5 pooled-cohort drift L12
and an uncovered-window fill L34; R6 priced-the-unit-alone-against-the-system L16).

## Findings, ranked

1. (Informational, non-blocking) The thread's careful-but-hurried effort estimate (~50-60% of results) runs higher
   than the design note's measured figure (31-38.5%); both stay well inside the H4 bar (quick well under a third,
   careful clearly below thorough), so this is recorded for calibration, not as a defect.
2. (Informational, non-blocking) The prompt's final supplementary clause ("our 2026 quotes, sales and conversion
   so far by segment") does not restate an explicit unit in the sentence itself; the thread treated this as the
   package's one soft spot and closed it via PLN-2027-03 1.3's filed scope clause rather than leaving it open.
   Not a Gate E failure (no second defensible figure survives), but worth the author's awareness for future voice
   passes.
3. No blocking finding. The fork that triggered the prior FIX_NOW pass (the prompt's "15 per cent" sentence) is
   gone; the prompt now reads 21 per cent in both places and states the premium's unit. No new fork opened by the
   fix to `hpm_model_deployments.txt` or the renewal schedule's ages.

## Next action for the author

None required before shipping this cut. If revisiting the prompt's voice pass, consider naming the unit implied
for "2026 quotes, sales and conversion" (counts and a rate) explicitly, purely for polish; it does not change the
verdict or disposition.
