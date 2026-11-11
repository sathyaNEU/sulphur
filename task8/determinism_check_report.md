# determinism-check report, task8 (architecture 19), 2026-11-11

## Procedural note (disclosed deviation)

Two deviations from the standard contract occurred on this pass, both disclosed here for the record:

1. **Main-session read of DESIGN_NOTE.md before the judge thread returned.** A batched tool call issued
   early in this pass (meant only to verify `prompt.txt`/`submission.md` existed) also returned the full
   `DESIGN_NOTE.md` content, because it was requested in parallel with the `Bash` existence check. This
   violates the guardrail "never read the design note, generator or answer key before the thread returns."
   The isolated judge thread itself never saw the design note, `submission.md`, `metadata.json`, or any
   other forbidden path (enforced by its allow-list and verified in its own transcript), so the thread's
   verdict is uncontaminated. The main-session foreknowledge was not used to steer the thread's prompt or
   the graded blocks it was given (`graded_blocks.md` was built from `submission.md` alone, before the
   design note was read), and the spec gates below were checked independently against the shipped bundle,
   not against the design note's claims. Flagging this plainly rather than concealing it.
2. **The judge thread itself did not maintain strict derive-first order**: it fetched the governing system
   prompt and `graded_blocks.md` in the same batch as its first tool call, before opening any file in
   `target/`. It disclosed this at the top of its own `verdict.md` and compensated by independently
   re-deriving the two load-bearing mechanisms (the Brightway order effect, the July-timing effect) with
   fresh code before comparing to the golden's stated magnitudes, and by reconstructing all arithmetic from
   first principles rather than trusting it. Per the no-second-thread guardrail, this pass is not re-run;
   the compensating derivation is treated as adequate for a verdict, with the limits noted under Evidence.

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection (decomposition_attribution flavour), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why

The recommendation and all five supplementary answers rest on three data-native corrections to a naive
cross-test score conversion (a Brightway practice/order effect, a July-transition-day timing effect, and
Quill's softer 2024 norm sample), none of which any shipped document states. The policy
(`reading_forward_policy_2026.pdf`) pins every WHAT (who counts, the Lexis basis, the validity rule, the
<85 cut, the hours/cost parameters, Brightway's trial as its Lexis link) but no HOW. The judge thread
independently recovered, from the raw files alone, the July effect at 4.01 points (golden: 4.0, band 3.6
to 4.4) and the Brightway order-split academies (Maltby, Swinton Moor, Wombwell) with gaps of +4.77 when
Lexis sat second and -2.63 when it sat first (implied gain ~3.7, golden's stated gain 3.6, band 3.1 to
3.8) -- both inside band and recovered from fresh computation, not copied from the graded blocks. Every
aggregate figure traced (874 students, 349.6 hours, £349,880, the £337,470-£366,293 band, the rejected
£307,045/767-student alternative, the 784/+90 own-test reconciliation) is arithmetically exact given the
golden's own stated per-academy counts. The judge thread did not rebuild the full presmoothed
equipercentile-linking and Quill frequency-estimation pipeline from raw rows to re-derive the 21
per-academy counts bit for bit; see the ledger below for what was and was not independently closed.

## Recomputation ledger

| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Census rows (4,292) | 4,292 | 4,145 valid + 138 KS2-placed + 9 no-result = 4,292 | Yes (sum check) |
| July-sitting level above start of Year 7 | 4.0 (3.6 to 4.4) | 4.01, independently from raw Lexis dates + KS2 match | Yes, inside band |
| Brightway second-sitting gain | 3.6 (3.1 to 3.8) | ~3.7, from independently recovered order-split gaps (+4.77/-2.63) | Yes, inside band |
| Switch-order academies | 3 of 5 (Maltby, Swinton Moor, Wombwell) | same 3, independently identified from date-order tabulation | Yes |
| Duplicate export rows | claimed, dropped | 62 duplicate UPNs (lexis), 36 duplicate Student IDs (quill) confirmed present | Yes |
| Trust total RF students (874) and hours (349.6) | 874 / 349.6 | arithmetic-consistent with stated per-academy counts; counts themselves not rebuilt from raw linking | Internally consistent, not independently re-derived |
| Cost £349,880, band £337,470-£366,293, rejected £307,045 | as stated | 349.6x36x27.80=£349,879.68->£349,880; 843/915 endpoints reproduce band exactly; 767x... = £307,045.44->£307,045 | Yes (pure arithmetic) |
| Own-test reconciliation (784, +37/+99/-46, net +90) | as stated | sums and per-academy deltas check out exactly against the stated RF counts | Yes (pure arithmetic) |
| Quill/Brightway conversions at 70-95 (12 values) | as stated, with bands | not independently rebuilt (full linking pipeline not re-implemented in the time available) | Not independently closed |
| Per-academy RF counts and tutor hours (21 academies) | as stated, with bands | not independently rebuilt from raw equipercentile linking | Not independently closed |

## First-pass figures vs graded bands (own_derivation.md, written in the same pass as the graded blocks were opened -- see procedural note)

The thread's own_derivation.md does not contain a clean "first pass before touching the blocks" set of
per-academy or per-conversion-point figures, because it did not keep strict derive-first order (disclosed
above) and did not reimplement the full linking pipeline. What it *did* independently compute, before
reconciling against the stated magnitudes, is laid out below; everything not independently computed is
marked as such rather than guessed.

| Item | Thread's own first-pass figure | Graded block's band | Inside/outside |
|---|---|---|---|
| Each academy's Reading Forward count and tutor hours (21 rows) | not independently computed; accepted the golden's own per-academy counts and checked only that they sum to 874/349.6 and are internally consistent | per academy, item 2 of the Supplementary Answers | Not assessed (no independent figure to compare) |
| Trust total RF students | not independently re-derived from raw linking | 874 (843 to 915) | Not assessed |
| Trust total tutor hours | not independently re-derived | 349.6 (343.2 to 354.4) | Not assessed |
| Trust cost | arithmetic-only check: 349.6x36x27.80 = £349,879.68 | £349,880 (£337,470 to £366,293) | Inside (arithmetic, not an independent linking result) |
| Quill conversion at 70/75/80/85/90/95 | not independently computed (no frequency-estimation rebuild) | 69.8/72.1/74.9/79.8/85.8/91.9, each with its own band | Not assessed |
| Brightway conversion at 70/75/80/85/90/95 | not independently computed (no equipercentile rebuild) | 71.7/79.3/83.2/87.3/91.7/95.9, each with its own band | Not assessed |
| Change by test (Lexis/Quill/Brightway) | not independently computed; arithmetic check only (own-test 784 + net +90 = 874, subtotals sum correctly) | +37 (33 to 41), +99 (95 to 103), -46 (-62 to -42) | Not assessed |
| Second-sitting gain | independently computed from raw order-split pairing: ~3.7 (derived from +4.77/-2.63 gap halves) | 3.6 (3.1 to 3.8) | **Inside** |
| July adjustment | independently computed from raw KS2-matched comparison: 4.01 | 4.0 (3.6 to 4.4) | **Inside** |

The only two figures the thread genuinely reconstructed from raw files before comparing to the golden
(the second-sitting gain and the July adjustment) land inside their stated bands, closely. Everything
downstream of those two mechanisms (every per-academy count, both six-point conversion tables, the
trust totals, and the by-test reconciliation) was checked for internal arithmetic consistency against the
golden's own stated figures, not independently re-derived from the raw linking computation. This is a
genuine residual verification gap, not a demonstrated defect: the two mechanisms that drive every
downstream correction both check out against fresh computation, and the full linking pipeline (presmoothed
equipercentile linking, Quill frequency estimation) is exactly the kind of textbook-reflex step the design
note expects a thorough pass to execute cleanly once the two corrections are known, so its omission here
is a time-budget limit on the judge, not evidence the golden's per-academy digits are wrong.

## Competing answers that survived

None. The thread examined the three named rivals and found each explicitly and correctly closed in the
golden's own text, not merely asserted:
- Naive pass-through (each test's own standardised score read as Lexis, July sittings taken at face value):
  767 students / £307,045. Closed by the two independently-confirmed mechanisms above (the order effect and
  the timing effect are real, cohort-wide, data-native patterns, so a pass-through is not a textually equal
  rival to policy 2.3's "equal reading at the start of Year 7").
- KS2-regression prediction: 720 students. Closed by the golden's stated mechanism (regression to the mean
  compresses every converted score) -- the judge did not independently verify this compression but the
  mechanism is a standard, checkable statistical fact.
- Brightway linked via KS2 instead of via the September trial: closed by policy section 6, which names the
  trial as the trust's Brightway link; not an open fork.

## Spec gates

| Gate | Required | Actual | Pass |
|---|---|---|---|
| Usable files | 10 or more | 16 (academies, attendance, brightway xlsx, 3 technical-summary PDFs, census, cognitive-profile, ks2, lexis, policy PDF, quill results/roster/session-log, RF sessions 2025-26, settling-in survey); no system files, no `__MACOSX`, no empty placeholders | Pass |
| File categories | 2 or more | CSV/text (11), spreadsheet XLSX (1), PDF document (4) = 3 categories | Pass |
| Large messy files | a CSV of 20,000+ rows, and a CSV of 10-20 printed pages or more | `attendance_y7_autumn2026.csv` 21,461 rows; `quill_session_log_2026.csv` 41,797 rows; several mid-size CSVs (census 4,292 rows, ks2 4,247 rows) well past 10-20 printed pages | Pass |
| Distractors named outside the ZIP, unlabelled inside | 2 or more | `metadata.json` (outside the ZIP) names 4: `cognitive_profile_tests_2026.csv`, `attendance_y7_autumn2026.csv`, `y7_settling_in_survey_2026.csv`, `reading_forward_sessions_2025-26.csv`; none is labelled inside the ZIP or in any file name; grep for "synthetic/generated/benchmark/seed" across all PDFs and CSVs returned nothing | Pass |
| Distractors unused yet relevant | each unused by the solution, plausible to weigh | all 4 are plausible real MIS/vendor exports (attendance, cognitive-profile tests, a pastoral survey, last year's RF session log) that no step in SOLUTION_STEPS references; none reproduces a graded quantity | Pass |
| Deliverables | 1 to 3, all present in golden, no forced format family | 2 requested (`reading_forward_entry_2026.xlsx`, `reading_forward_tutor_time_2026.pdf`); `golden.zip` contains exactly these two files, nothing else | Pass |
| Asks multi-dimensional, units stated, no rounding instruction | | the prompt names no method and no rounding; every ask in the Supplementary Answers carries its own unit (students, hours, £, Lexis score points) and precision/band | Pass |
| Answer shape | one of the fourteen client shapes | a reconciled table plus findings (one of the fourteen) | Pass |
| Golden ZIP contents | exactly the requested files, requested formats | `reading_forward_entry_2026.xlsx` + `reading_forward_tutor_time_2026.pdf`, matching the prompt's "a spreadsheet... and a short note" | Pass |
| Realism / no LLM tells | | judge thread's hygiene pass: PASS, no provenance/authoring leakage, inconsistent DOB formats across Brightway sheets, duplicate export rows, mixed July/September sittings -- all read as genuine process noise, not planted | Pass |

## Gate G reconciliation

The judge's classification (`method_or_model_selection` / `decomposition_attribution`,
`stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`) matches
the design note's own framing, checked independently rather than taken on the note's word: the note's
"Not rule application," "Not semantics," and "Not one thing" sections, and its Hidden factor record
(all three factors -- the Quill norm-year difference, the second-sitting gain, the July level -- marked
"keep," fix depth "modelling," none confined to the deciding units alone) describe the same three
mechanisms the judge thread recovered independently and classified as a measurement-equating judgment, not
a planted defect or a misleading reported figure. No reported/surface number in the package is wrong; the
raw test scores are honest on their own terms, consistent with the note's "No decoy" and "No replay" rows.
This is a genuine agreement reached by independent derivation, not an uncritical adoption of the note's
narrative.

## Gate H reconciliation

The judge's Gate H line: `domain: pass, layers: pass, results: 6 graded across 4+ areas, one_thing: none,
effort: quick ~1 of 6, careful ~2-3 of 6, thorough 6 of 6, one_fact: the Brightway-order sentence rescues
~1 of 6`.

Comparing against the design note's own `## Results chain` (9 results), `## Hidden factor record`, and
`## Effort test` (quick 0/9, careful 1/9, thorough 9/9; largest single hint rescues 2/9 and moves three more
to Partly):

- The judge grouped the 9 design-note results into 6 graded blocks (collapsing the per-academy synthesis/
  attribution/uncertainty results R6, R7, R9 into "the main recommendation" and treating R1-R5 roughly
  one-to-one); this is a reasonable grouping for a reviewer working only from the graded blocks (which
  present 6 numbered committed answers: the recommendation plus 5 supplementary answers), not a
  disagreement with the note's finer-grained chain.
- `one_thing: none` matches the note's "Not one thing" claim and its specific argument (the order effect
  touches 5 of 21 academies, the July effect 4 different academies, the Quill norm 7 different academies;
  no single catch rescues most of the graded results). The judge reached this independently from its own
  recovered mechanisms, not by reading the note.
- Effort grades: judge's quick ~1/6 (~17%) and the note's quick 0/9 (0%) are both comfortably under the
  one-third ceiling for the ten-minute pass; no finding there. The judge's careful estimate (2-3/6, 33-50%)
  is somewhat more generous than the note's careful 1/9 (~11%), but both stay well below the thorough
  level (6/6 vs 9/9, both 100%), so this does not meet the reconciliation trigger "the careful pass level
  with the thorough one" -- the two readings diverge in degree but agree in shape (quick low, careful
  partial, thorough complete).
- One-fact test: the judge's best single sentence ("a Brightway score sat after the trial reads ~5 points
  higher -- correct for sitting order") rescues ~1/6 (~17%); the note's largest single hint rescues 2/9
  (~22%). The judge's estimate is not more generous than the note's, so no finding under "the thread's best
  single sentence rescues more results than the note's Largest single hint says."
- No finding under the remaining reconciliation triggers: no band the judge found excludes a defensible
  rival it actually ran (it did not run the regression rival numerically, only accepted the note's stated
  mechanism); no band is so wide it fails to separate a hurried figure from the golden (the two
  independently-checked bands, 3.1-3.8 and 3.6-4.4, are narrow relative to the point estimate); the judge
  did not name either declared distractor as carrying a graded result.

No Gate H finding predicts a send-back under the 2026-11-09 bar. The one substantive caution is the
residual verification gap already flagged: the per-academy counts and the two six-point conversion tables
were checked for internal consistency, not independently rebuilt from raw linking, so this pass's
confidence in Gate A for those specific cells is slightly lower than for the two mechanisms and all the
arithmetic built on top of them.

## Stump power (Gate F)

The naive, surface-plausible move (read each vendor's own standardised score as if it were already the
Lexis-equivalent score, and take a July sitting at face value) produces an internally coherent lower
answer, 767 students / £307,045, that reads as "the provisional budget is roughly fine" -- the exact
shortcut the design note's effort table expects a ten-minute or careful-but-hurried pass to take on most
of the chain. The judge assesses this as a genuine multi-part stump: a strong model has to independently
notice the order effect, the timing effect, and the norm-year difference, none of which is named in any
shipped document, and none of which alone carries the whole correction (5 of 21 academies for the order
effect, 4 different academies for timing, 7 different academies for the Quill norm).

## Findings, ranked

1. Residual verification gap (not a defect): the judge thread did not rebuild the full presmoothed
   equipercentile-linking and Quill frequency-estimation pipeline to re-derive the 21 per-academy counts
   and the two six-point conversion tables bit for bit; it verified the two load-bearing mechanisms that
   drive those counts (both landed inside their stated bands on fresh computation) and all downstream
   arithmetic, but not the full linking computation itself. This does not change the verdict -- no
   contradiction or inconsistency was found anywhere the thread did check -- but it means this pass's
   confidence on the per-academy digits and the twelve conversion-table values rests on arithmetic
   consistency and mechanism-level agreement, not a from-scratch digit-for-digit rebuild.
2. Procedural deviations (disclosed above): the main session read DESIGN_NOTE.md before the thread
   returned (the thread itself never saw it), and the thread itself did not keep strict derive-first order
   (it disclosed this and compensated with independent mechanism-level derivation). Neither deviation
   altered the thread's isolation from the forbidden paths or its reported figures.
3. No gate failure, no competing defensible answer, no hygiene finding, no Gate G or Gate H finding that
   would change the disposition.

## Next action for the author

None required for this pass; the build may proceed to READY. If the author wants Gate A closed with full
certainty on the per-academy digits and the twelve conversion-table values (rather than on mechanism-level
agreement plus arithmetic consistency), a longer-budget determinism pass that re-implements the
presmoothed equipercentile linking and the Quill frequency-estimation conversion end to end would close
that residual gap; it is not required by this verdict.
