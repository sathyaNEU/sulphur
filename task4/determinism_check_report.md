# determinism-check report, task4, 2026-11-11

Architecture 11 (Saarnela's 2027 peak plan, evening shifts and agency hours). This pass runs beside the leak
reader at /build stage 4, licensed by the author. It supersedes the architecture-10-era reports on file
(determinism_check_report_pass3.md to pass10.md, left untouched) with the current cut's own report.

## Verdict

**DETERMINISTIC, partial verification.** The isolated judge thread independently reproduced component 4 (the
2025 peak's picker hours) exactly, the Black Friday / 53-ISO-week calendar mechanism exactly, and reproduced
component 1 (aisle congestion, 0.46 min/line at 1.8 pickers/aisle) and ask 4 (the pooled 14.8 per cent
overstatement) inside their stated bands, but did not have the time budget in this one-shot pass to fully
re-derive asks 1, 2, 3, 5 and component 2 to their numeric bands. It traced every input those asks need to a
specific shipped file and found nothing in that trace that contradicts the committed figures. No competing
defensible answer and no missing or external fact was found anywhere in the pass.

**Disposition:** APPROVE, with one open item for the author's own records, not a FIX_NOW or SEND_BACK: re-verify
asks 1/2/3/5 and component 2 (the zone-week hours and ranges, the agency hours, the shift verdicts, the
Huippu-vs-Kotikaari minutes gap, and the growth-conditioned budget overstatement) end to end against the bundle
in a future pass with a larger time budget. Nothing found in this pass points to a defect; the gap is coverage,
not a located problem.

**Stumping type:** mechanism: mixed (forecasting + decomposition_attribution + binding_constraint),
stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no.

## Why

The thread derived its own answer from target/ before opening graded_blocks.md (confirmed in verdict.md and
own_derivation.md) and kept that order. The two figures it worried about most going in, the congestion
coefficient and the pooled forecast overstatement, both required a specific non-obvious method choice to land
in-band and both did once that choice was made from the files (an interacted density term for congestion, the
standard's next-working-day release rule for the overstatement), which is the "method stays open, WHAT is filed"
shape the spec licenses, not an unpinned ambiguity. No file in the bundle argues for a different set of
evening-shift weeks, and the site manager's own draft sheet (saarnela_peak_2027_staffing.xlsx) reproduces by its
own stated method and answers a shallower quantity (2025's floor rate), never the 2027 one.

## Recomputation ledger

| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Component 4, 2025 peak picker hours (P1/P2/B1) | 3,384 / 3,104 / 2,280 | 3,384.0 / 3,104.0 / 2,280.0 from timesheets_2024-01_2026-10.csv, ISO weeks 46-50 of 2025, by cost centre | Yes, exact |
| Black Friday ISO week, 2025 vs 2027 | week 48 (2025), week 47 (2027), via 2026's 53rd ISO week | week 48 (2025-11-28), week 48 (2026-11-27), week 47 (2027-11-26); 2026-12-28 falls in ISO week 53 | Yes, exact |
| Standard's aisle counts and floor limits | P1 8->12 aisles/limit 24; P2 7->11/limit 22, at 8 Jan 2024 | Matched from a real table extraction of the standard PDF (not dropped by a naive text read) | Yes, exact |
| Critical component 1, congestion at 1.8 pickers/aisle | 0.46 min/line (band 0.40-0.51) | ~0.41 min/line under an interacted lines x ppa / ppa^2 spec, R^2 ~0.992; an additive-only spec misfits badly and is rejected on sign/fit, matching SOLUTION_STEPS's own claim | Yes, inside band |
| Ask 4, pooled year-ahead overstatement | 14.8 per cent (band 13.8-17.3) | ~13.2 per cent on raw received-date bucketing; ~16.5 per cent once the standard's clause 2.4 release rule is applied | Yes, inside band only under the filed release rule |
| Asks 1, 2, 3, 5; component 2 | per submission.md | inputs located and structurally consistent with SOLUTION_STEPS; not numerically re-derived in this pass | Not verified this pass (traced, not closed) |

## Competing answers that survived

None found. The thread found no reading of the files that drives a different main recommendation, and
specifically checked and rejected the naive alternatives SOLUTION_STEPS itself names (the 2025 rate carried
forward, the pilot's polybag-only mix, the pooled 14.8 per cent applied to a budget that never planned that much
growth, and the week-numbered calendar phasing), finding each pulls the evening-shift weeks in a different
direction, consistent with the design note's "Not one thing" claim and its enumerated single-lever wrong routes
(SOLUTION_STEPS step 8).

## Spec gates

| Gate | Required | Actual | Pass |
|---|---|---|---|
| Usable files | 10 or more | 18 files in target/ (no system files, no __MACOSX) | Pass |
| File categories | 2 or more | spreadsheet (5 xlsx), text/document (10 csv, 2 pdf, 1 docx) | Pass |
| Large messy CSVs | a CSV >= 20,000 rows, and a CSV of 10-20 printed pages or more | huippu_article_lines (93,580 rows), wms_zone_hours (34,078), timesheets (27,406), wms_pick_confirmations_HUI (26,672) all clear 20,000 rows; several mid-size CSVs (2,000-16,500 rows, multi-column) clear a 10-20 page print easily | Pass |
| Distractors named outside the ZIP | metadata.json names 2+, nothing inside the ZIP labels one | saarnela_packing_benches_2026-01_2026-10.csv and kotikaari_returns_received_2024-01_2026-10.csv named in task4/metadata.json only; neither file name nor any file content inside target.zip marks either as unused | Pass |
| Distractors relevant but unused | each should be plausible and unused | both read as genuine 3PL operational exports (a packing-bench log, a returns feed) that no SOLUTION_STEPS step references; judge thread independently flagged both as "likely-unused" before being told | Pass |
| Deliverables | 1-3, all present in golden, no forced format family | 2 (saarnela_peak_plan_2027.xlsx, saarnela_peak_plan_2027.docx), both present in golden.zip, matching metadata.json's deliverables list exactly | Pass |
| Asks multidimensional, unit stated, no rounding instruction | required | prompt.txt gives no rounding instruction (precision and bands live in submission.md); asks carry their own units (minutes, hours, per cent) and resolve to many gradable figures (15 zone-week hours, 5 agency figures, 6 shift verdicts) | Pass |
| Answer shape | one of the client's fourteen | "a schedule under capacity" (per zone-week lines vs. day-shift capacity at the limit, with hours, ranges, shift verdict and agency hours), four or more results each independently checkable | Pass |
| Golden ZIP contents | exactly the requested files, in the requested formats | golden.zip holds exactly saarnela_peak_plan_2027.docx and saarnela_peak_plan_2027.xlsx, nothing else | Pass |
| Realism / not LLM-authored | required | judge thread found a real payroll-system-migration seam (semicolon/decimal-comma era vs. the new export, different cost-centre codes), a genuine WMS double-export artifact, no LLM tells, no authoring/benchmark disclosures anywhere in target/; a direct check of the golden memo's XML shows plain operational prose (a dated memo, a table, a stated recommendation), not generic padding | Pass |

## Gate G reconciliation

The thread's classification (mechanism: mixed [forecasting + decomposition_attribution + binding_constraint],
surface_read_dependency: no, sole_data_defect: no) matches the design note's own account. DESIGN_NOTE.md's "Not
rule application," "Not semantics" and "No decoy" sections argue the same four independent levers the thread
found by its own reading (the 2025 density vs. 2027's doubled zone limit; the pilot's polybag-only mix vs. the
brand's full assortment; the pooled vs. growth-conditioned overstatement; the week-numbered vs. date-anchored
Black Friday phasing), and the thread arrived at the same four without having read the note. No reported figure
in the bundle is wrong and the task does not turn on catching that one is; this passes Gate G cleanly as the
note intends (the design note's own "Strategy label: own" line and the Frontier check's "Forcing" row name the
same shortcuts and the same partial-fix routes the thread independently rediscovered).

## Stump power (Gate F)

The thread's own read: the result a careful-but-hurried strong model is likeliest to lose is the evening-shift
plan (asks 1-3), by filing a day-shift congestion rate close to 2025's observed ~1.15 pickers/aisle instead of
recomputing it at 2027's doubled-limit density (24/22 pickers), understating hours and likely missing the
evening shift in one or more weeks, matching the design note's effort table (R3, "method shortcut," Missed at
both quick and careful-hurried). This is a genuine forecasting/binding-constraint trap on honest numbers, not a
reported-figure catch.

## Findings, ranked

1. **Coverage gap, not a defect (primary finding).** The judge thread's one-shot time budget did not stretch to
   numerically closing asks 1, 2, 3, 5 or component 2; it traced their inputs and found no contradiction, but
   this pass cannot certify those five results to the stated bands the way it certified component 4, component 1,
   the Black Friday mechanism and ask 4. Recommend a follow-up determinism pass (or a longer single pass) that
   starts its own derivation from the own-pickers/staffing workbooks, the article-lines/item-master/slotting
   join for Huippu's mix, and the log-log growth fit for component 2, specifically to close this gap.

2. **Effort-table divergence, flagged but unconfirmed.** The thread's own (admittedly partial) effort estimate
   puts the careful-but-hurried pass at roughly 4-6 of 10 results, above DESIGN_NOTE.md's Effort test table (2 of
   10: R1 and R2 only). Because the thread did not finish deriving R7-R10, this cannot be treated as a confirmed
   contradiction of the note's effort grading, only as a signal the author should re-check once the coverage gap
   above is closed: if a fuller pass confirms the careful-but-hurried solver reaches more than a third of the
   results, that would move the note's own effort test (H4) toward a borderline reading.

3. **One-fact claim, same caveat.** The thread names "recompute 2027's congestion at the zone's current limit
   (24/22), not 2025's logged density" as the single most rescuing sentence, and estimates it rescues "roughly
   the shift-verdict/hours asks (1-3)" (which, read generously, could be 4-5 of the 10 chain results: R3, R7, R8,
   R9, R10) against DESIGN_NOTE.md's own "Largest single hint... rescues 1 of 10 results" (R3 alone). This reads
   wider than the note's claim, but it rests on the same unclosed computation as finding 2: R7, R9 and R10 also
   depend on R4, R5 and R6 (the pilot mix, the growth-conditioned overstatement, the calendar re-key) per the
   design note's own carry-forward rule, so a single congestion fact should not, on the note's own chain logic,
   rescue the full hours/evening/agency set. Worth the author's own check once asks 1-3 are closed, not a basis
   for SEND_BACK on this pass's evidence alone.

4. Hygiene, Gate G and the spec-gate table above are all clean with no caveats.

## Next action for the author

Run one more determinism pass (or extend this one with a larger time budget) focused narrowly on closing asks 1,
2, 3, 5 and component 2 end to end against the bundle, specifically to confirm or correct the effort-table and
one-fact divergences flagged above; nothing in this pass's completed recomputation changed the verdict, the
disposition, or the Gate G/H classification.
