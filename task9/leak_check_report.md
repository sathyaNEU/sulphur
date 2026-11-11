# leak check, task9

**Verdict: REVIEW.** 27 files read, 164 golden figures and 1 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: record, architecture, careful, ostvale, sentence, ladder, carried, levels, golden, rivals, review, missed, average, result, policy, forecast, outside, recovery, closed, replay, platform, estimator, capital, determinism, investment-grade

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `Credit_Electronic_Quoting_Policy_2026.pdf`: golden figure 4.8 appears: ...e: investment grade liquid 1.2, medium 2.4, thin 4.8; high yield liquid 4.2, medium 8.4, thin 15.6. 6....
- **REVIEW** `Credit_Electronic_Quoting_Policy_2026.pdf`: carries 3 of 5 distinctive words of the committed call: 'Plan USD 10.30 million of desk P&L for 2027 on the draft schedule'

## 4 design-note vocabulary (REVIEW 1)
- **REVIEW** `Credit_Electronic_Quoting_Policy_2026.pdf`: 4 of 25 stump-paragraph terms appear (record, carried, policy, outside); read whether the document names the move

## 9 dates after the setting (INFO 1)
- **INFO** `-`: no --asof given, sweep skipped (pass the fiction's as-of date)

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 11 prompt gate (REVIEW 1)
- **REVIEW** `prompt.txt`: shell quota: deliverable set 'docx+xlsx' at 35% of 17 prompts (cap 20%); reword at the role level, not the verb

## 12 client quality check (INFO 2)
- **INFO** `-`: 27 usable files (10 or more required)
- **INFO** `-`: 2 file categories: document, spreadsheet (2 or more required)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)


## Solver's-eye read

One isolated reader (Sonnet, medium effort) on fresh copies of prompt.txt and target/, architecture 10, 2026-11-11. Its answers, verbatim:

# Leak read, task9 (no figures computed)

Files read: prompt.txt, the policy PDF text, the headers and first rows of every CSV, and the shared strings of the four workbooks. The large CSVs were not sampled further.

## 1. Sentences that say how the analysis is done
All are in Credit_Electronic_Quoting_Policy_2026.pdf.
- Section 6(a): "A schedule is priced by what the desk's requests since 3 January 2023 would have made at that schedule's quotes. Each request keeps everything but the desk's half-spread: its size, time, VIX and inventory terms and its jitter, the other dealers' prices and whether its client traded; a request its client did not trade, or the desk passed, stays as it was." This is the whole re-pricing method and its counterfactual rule.
- Section 6(b): "Each segment is carried at the number of requests it received in the twelve months to 31 October 2026." This fixes the volume basis.
- Section 6(c): "The plan's range is the 10th to the 90th percentile of the year's P&L, its 251 trading days drawn from the record's own days at the plan's request counts." This names the resampling method, the unit drawn and the number of days.
- Section 5: P&L is edge at execution, less the move against the desk "net of the move of the Treasury curve and of the median move in the evaluated spreads of other issuers' bonds of its rating, read as soon as that move is complete", less the offload charge per bucket. This gives the markout definition, the adjustment and the timing.
- Section 2: segment = rating band on the request date, the quarter's liquidity bucket, and the client type. Section 4 excludes carry and funding from P&L.
- Section 3 and the proposed schedule sheet: "Distance = half-spread x size multiple x VIX multiple x (1 + jitter) x (1 - 0.35 x position / limit x direction)". This gives the quote formula.

## 2. Files that rank or score the candidates
none. Neither schedule workbook nor the month-end summaries gives a per-segment verdict on the proposed changes. The month-end summaries show a "Net, next-day view (USD)" by segment. Its header says next-day markout, which is not the policy's measure. That is context, and possibly a decoy.

## 3. Files that exist only to help the analyst
The policy PDF is the closest. It is a methodology document written to carry the plan's procedure, not a description of the field (see 1 and 5). Nothing else is purely a helper. The two schedule workbooks and the security master with its liquidity buckets are real inputs.

## 4. Figures or names that read as the answer
none found as a result. The offload charges in section 5 and the 35% inventory skew are parameters. The policy ties three results to named specifics: the 251-day year, the 10th to 90th percentile, and the 31 October 2026 volume window.

## 5. Filed sentences that fix a graded figure's computation or population
- 6(a), read literally: only the desk's half-spread changes, a request the client did not trade or the desk passed keeps its outcome, and a request counts at the new quote. That fixes the population as all requests since 3 January 2023 and the counterfactual as repricing with everything else held.
- 6(b), read literally: each segment's request count is the trailing-twelve-month count to 31 October 2026, and the year's P&L is built from that count per segment.
- 6(c), read literally: the range comes from drawing 251 trading days from the record's days, at those counts, and taking the 10th and 90th percentiles. This fixes the interval method.
- 5, read literally: the post-trade price move is taken net of the Treasury curve and the median same-rating spread move, at the point the move is complete. That is the markout definition, less the offload charge for the bucket (the bucket for the request's quarter, from section 2).
- 2, read literally: the segment is the three-way key. Together with 3 and 4, this fixes the grouping and what is excluded.

## 6. The one thing that would make most of this routine
The policy PDF, section 6 together with section 5. Read literally, it is the full recipe for the plan: reprice each request's half-spread, hold everything else, carry segments at the trailing-year counts, bootstrap days for the 80% range, and measure the cost after trades as the net, "read as soon as complete", markout. Once it is read, the 2027 P&L under both schedules, the range and the split by changed segment are procedure-following. The share of requests the proposed quote wins and the after-trade cost per million both fall out of the same repricing. What stays as analysis is the evaluation of "as soon as that move is complete" (the horizon is not stated), the two audit formats before and after 7 April 2025, the security master and rating history joins, the bucket by quarter, and the schedule version history.

Part by part:
- 2027 P&L under the current and proposed schedules: rule-following of 6(a) and 6(b), plus assembly of the audit, blotter and marks. Mostly procedure.
- 80% range: rule-following (6(c) names the method).
- Difference split by changed segment, and the segments that lose money: follows from the repricing, plus knowing which cells of the schedule changed. Mostly procedure.
- Share of requests the proposed quote would win: analysis of the dealers' prices and the counterfactual, with the rule filed in 6(a).
- Post-trade cost per million for won and added trades: partly analysis (the move-complete horizon, the net-of-hedge adjustment), but the adjustment is spelled out in section 5.
- Nothing reads as planted. Data semantics (the units of the new audit format, the segment keys) are reading work.

## Flagged items
- REVIEW Credit_Electronic_Quoting_Policy_2026.pdf, answer-figure match on one number: harmless as a leak of an answer. The only numbers in the file are parameters: the offload charges, the 251 days, the 35% skew, the dates and the percentiles. No result figure is in the PDF. If the match is on one of those parameters, it is context. The PDF is a leak of method, not of figures, per 1 and 5.
- REVIEW Credit_Electronic_Quoting_Policy_2026.pdf, three of five distinctive words shared with the recommendation: a leak of wording and method. The policy's section 6 and the prompt's question use the same vocabulary (schedule, plan, segments, 80% range, changed segments). A solver reading the policy gets the structure of the answer, not its direction. Reword the policy if the recommendation's phrasing is borrowed from it.
- REVIEW prompt.txt, shell quota (deliverable set docx+xlsx at 35% of 17 prompts): a house-level repeat of the deliverable pair "a spreadsheet and a one-page memo", not a content leak. The prompt itself names no method, file or step. The role-level reword is for the author. It does ask for the 80% range and a "per million traded" unit, which are results asked for, not methods.

### Rulings (main thread)

- Q1, policy 6(a), 6(b), 6(c), 5, 2, 4 and the schedule workbook's distance formula: harmless. Each pins an estimand
  once (the counterfactual, the volume, the range's definition, the P&L, the segment, the quoter's own spec) and would
  exist without any trap; none says where rivals' levels on lost requests come from, when the move after a trade is
  complete, what the added trades cost or how the year's days are drawn.
- Q3, the policy as a helper: harmless. It is the governing document (scope, segments, the quoter, inventory, the
  planning convention, records) in the desk's genre; its date is given its reason in the next rebuild ("since it began
  quoting on Tidewell on 3 January 2023").
- Q5, every literal reading: the golden, except 6(c) read as days drawn one at a time, which is ruled out by named
  data (the draft's daily P&L: first-order autocorrelation 0.19 against a noise bound of 0.06, 21-day sums at 3.0 times
  independent days); added as SF18 and asserted in checks.py.
- Q6, the policy as the one thing: not a banned finding. The reader itself leaves rivals' levels, the completion
  horizon and the assembly as analysis; effort.py's careful pass executes the policy literally and still loses 7.5 of
  8 results, and no single sentence rescues more than one.
- REVIEW, golden figure 4.8 in the policy: harmless, the offload charge for thin investment grade, a parameter.
- REVIEW, three of five words of the call in the policy: harmless, the subject's own nouns (plan, desk, P&L,
  schedule); no figure and no direction.
- REVIEW, prompt shell quota: harmless, a house-level mix warning; the author rewrites the prompt.

### Second read (after the stage 4 rebuild, 2026-11-11), verbatim

# Leak read, task9 (no figures computed)

**1. Sentences that say how the analysis is done.** Heavily, in the policy PDF:
- Credit_Electronic_Quoting_Policy_2026.pdf s5: "the desk counts a trade's P&L as (a) its edge at execution... less (b) the move in the bond's value against the desk after the trade, net of the move of the Treasury curve and of the median move in the evaluated spreads of other issuers' bonds of its rating, read as soon as that move is complete; less (c) the offload charge for the bucket..." (gives the P&L formula, the hedge/adjustment, the markout clock and the charges).
- s6(a): "A schedule is priced by what the desk's requests since it began quoting on Tidewell on 3 January 2023 would have made at that schedule's quotes. Each request keeps everything but the desk's half-spread: its size, time, VIX and inventory terms and its jitter, the other dealers' prices and whether its client traded; a request its client did not trade, or the desk passed, stays as it was." (gives the repricing/counterfactual method, the population and what is held fixed).
- s6(b): "Each segment is carried at the number of requests it received in the twelve months to 31 October 2026." (volume basis).
- s6(c): "The plan's range is the 10th to the 90th percentile of the year's P&L, its 251 trading days drawn from the record's own days at the plan's request counts." (bootstrap by day).
- s2: segment definition (BBB or above = IG, bucket per request quarter, client type).
- auto_quoter_schedule_2027_proposed.xlsx: the full distance formula, jitter distribution, multiples, position limits.
- credit_desk_month_end_summaries.xlsx header: "Next-day markout: the evaluated mid at the next close against the reference mid, on the desk's side" (a rival, weaker method, shown as the desk's existing convention).
- prompt.txt names no method (it says what each result is, not how).

**2. Files that rank or score the candidates.** none outright. credit_desk_month_end_summaries.xlsx scores each segment (edge, next-day markout, "Net, next-day view") by month, which is a ranking-like view on the prompt's question, but on the rival next-day basis and for the current schedule only. tidewell_dealer_league_tables_2026.xlsx is context.

**3. Files that exist only to help the analyst.** auto_quoter_schedule_2027_proposed.xlsx and the PDF's s6 are the specification of the question rather than data. security_master_liquidity_buckets.csv and issuer_ratings_history.csv are lookup helpers but are also genuine records. none labelled as a hint.

**4. Figure or name reading as the answer.** none. The proposed schedule lists half-spreads, not results. (Seeing which rows differ between auto_quoter_schedule_versions.xlsx v3 and the proposed sheet identifies the changed segments, but that is context the prompt's "segments the schedule changes" requires.)

**5. Filed sentences that fix a graded figure's computation or population.** 
- s5 (b) "read as soon as that move is complete": literally fixes the markout clock at the point the post-trade move has finished, net of Treasury and median same-rating spread moves, so it hands over the markout window and benchmark.
- s5 (c): fixes the offload charge per bucket and rating band, so a literal reader deducts it per face traded.
- s6(a): fixes that only the half-spread changes, non-traded and passed requests stay unchanged, the request set is every request since 3 Jan 2023; a literal reader reprices winning/lost requests holding rivals' prices fixed (so win share at the proposed quote is read off the other dealers' prices).
- s6(b): fixes the 2027 volume per segment as the trailing twelve months to 31 Oct 2026.
- s6(c): fixes the range as the 10th to 90th percentile of day-level resampled years of 251 days.
- s4: coupon accrual and funding are excluded from desk P&L; hedging uses Treasuries.
- s2: IG/HY cut at BBB, bucket by request quarter.
Together these give nearly the whole method; the analyst is left to execute it (data assembly, the format change on 7 April 2025, the rival price reading, the spread-move median).

**6. One thing that would make most of it routine.** The policy s6(a) paragraph (reprice each request at the new half-spread, hold everything else including rivals' prices and client behaviour fixed) together with s5 (the P&L definition). Once read, it settles the counterfactual win logic, the P&L per trade, the segment split, the loss-making segments and the per-million cost split, leaving mostly execution; only the range (s6(c)) adds a separate step, and that is also spelled out. Per part of the ask:
- 2027 P&L current vs proposed: follows a stated rule/procedure (s5, s6(a), s6(b)) plus heavy data assembly.
- 80% range: follows a stated procedure (s6(c)).
- Difference split across changed segments and loss-making ones: reading which rows of the schedule differ, then applying the stated procedure; routine once the rule is read.
- Win share since Jan 2023: stated rule (s6(a)) applied to the audit with other dealers' prices; some analysis in reconciling the two audit formats.
- Markout cost per million for existing and added trades: the stated definition (s5(b)), applied literally; the "added" trades are the new wins from the repricing. Turns on following the stated definition.
Overall, little turns on open analysis; most turns on following the stated rules. Nothing looks planted in the data samples seen; the format change on 7 April 2025 is announced in s7 and visible in the two audit files (different column names, side codes CB/CS vs BUY/SELL, thousands of face vs units, UTC vs ET).

## Flagged items
- REVIEW Credit_Electronic_Quoting_Policy_2026.pdf, answer-figure sweep number match: harmless as a number in the text in itself (the numbers in the PDF are the offload charges, the 251 days, the dates and the percentiles), but note these figures ARE inputs that the solver needs and a few are filed conventions, not answers. The number matched is plausibly one of those conventions (e.g. a charge or percentile also appearing in the answer text); not an answer value as far as I can read, so harmless as a result figure, though the s5/s6 sentences are method leaks per Q1/Q5.
- REVIEW Credit_Electronic_Quoting_Policy_2026.pdf, wording overlap with the recommendation: leak at the level of method and vocabulary, not of the answer. The PDF shares wording (schedule, quoting, segments, losing) with any recommendation because it describes the same objects; it states no verdict. The real leak in this file is the procedural content of s5 and s6 (Q1, Q5), which dictates the repricing counterfactual, markout definition and range method.
- REVIEW prompt.txt, shell quota (docx+xlsx deliverable set at 35% of prompts): harmless for leakage (no answer or method in the prompt); it is a variety-quota matter only. The prompt asks for "a spreadsheet and a one-page memo", so rewording at the role level is a style fix, not a leak fix.

### Rulings on the second read (main thread)

- Q1 and Q5 (sections 5, 6a to 6c, 2, 4, the quoter's formula): the estimand pins, as ruled on the first read; the
  determinism judge, which recomputed, classes the task's mechanism as a method choice on honest data (the
  measurement horizon and the replay), not rule application, and the pipeline lets the judge settle what a shipped
  sentence licenses.
- Q5, 6(c) as day-level resampling: closed by SF18 and stated in Ask 1 and Step-by-Step 6 (the daily P&L's
  dependence, runs of 10 to 63 days inside the bands).
- Q6 (sections 5 and 6 as the one thing): weighed as Gate F evidence of what solvers execute. It sharpens one point
  the main thread accepts: section 5 counts each trade's move, so a literal executor costs every added trade on its
  own record, and the careful column's pricing of the added trades is held against the re-judge's first pass.
- Flagged items: as ruled on the first read.
