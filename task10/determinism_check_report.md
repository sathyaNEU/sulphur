# determinism-check report, task10, 2026-11-10

Cut: target.zip sha256 a40205c5885036d29a5249d80669347e074e379e6cde430b2e47856333d75e99. Prompt is prompt.txt (not the legacy .md). One isolated thread (general-purpose, medium effort) read only under /tmp/determinism-check-task10-093601/. It reports it wrote own_derivation.md before opening graded_blocks.md (order kept). Files: verdict.md, own_derivation.md in that directory.

## Verdict
**DETERMINISTIC** (no SOLUTION_WRONG)
**Disposition:** APPROVE (the thread's disposition, verbatim: "APPROVE. No repair is needed and no model rerun is required. Two optional pins are listed under Fix."). One item for the main thread to weigh is under Findings (Ashcombe Road bands).
**Stumping type:** mechanism: forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The thread's words: the commit list (Ashcombe Road, Charlecote Way, Dunmore Street, Fenwick Street; hold Hartwell Common) comes out of the shipped files once three data-borne steps are run (cold-day suppression and the 2025/26 design-day demand, the register customers' build-up between the two assessment dates, class-specific slip of planned commissioning dates). The rebound after the window decides Ashcombe Road alone. Every rival it ran is outside the golden's stated band or ruled out by named data. The 10 per cent line is not knife-edge for any primary (Hartwell Common 0 to 4 per cent against 41 per cent or more for the four committed).

Its own first pass, written before it opened the blocks (pooled slip, single-ratio baseline, delivery subtracted flat through the window), committed only Charlecote Way and Dunmore Street (demand before flexibility 32.9 / 30.6 / 23.3 / 38.8 / 24.6 MW; credits 10.2 / 4.3 / 3.0 / 6.1 / 1.8; shares 1 / 73 / 62 / 4 / 0 per cent). This is a hurried-but-competent route and it misses Ashcombe Road and Fenwick Street. After opening the blocks it corrected itself (class-specific slip, morning-anchored baseline, rebound) and re-ran; the re-run is described in verdict.md only, not in own_derivation.md.

## Recomputation ledger
Corrected re-run (thread, after seeing the blocks) against the golden. MW; shares in per cent. "Band" is the stated band in the answer blocks.

| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Design-day 2025/26, Ashcombe / Charlecote / Dunmore / Fenwick / Hartwell | 30.2 / 25.0 / 22.2 / 36.8 / 22.7 | 30.85 / 25.3 / 22.5 / 36.8 / 23.1 | Yes, Ashcombe 0.05 above its band (29.9 to 30.8), others inside |
| Register customers add (same order) | 0.7 / 4.5 / 0.2 / 0.7 / 0.7 | 0.65 / 4.49 / 0.19 / 0.67 / 0.63 | Yes |
| Demand before flexibility 2027/28 | 32.2 / 30.3 / 23.0 / 38.9 / 24.3 | 32.9 / 30.6 / 23.2 / 38.8 / 24.6 | Yes, all inside bands (Ashcombe at the band's top, 32.9) |
| In service 15 Jan 2028 | 17.8 / 8.8 / 6.2 / 7.6 / 3.6 | 18.2 / 8.95 / 6.16 / 7.7 / 3.67 | Yes (Ashcombe at band top, 18.2) |
| Delivered 17:00 to 18:00 | 7.6 / 4.5 / 2.6 / 3.9 / 1.5 | 8.0 / 4.65 / 2.7 / 4.0 / 1.6 | Yes (Ashcombe at band top) |
| Expected peak | 28.5 / 25.9 / 20.4 / 35.0 / 22.8 | 28.0 / 25.9 / 20.5 / 34.8 / 23.0 | Yes except Ashcombe 28.0, below its band (28.2 to 29.0) |
| Nine-days-in-ten level | 29.5 / 27.0 / 21.1 / 36.2 / 23.4 | 28.7 / 27.4 / 21.4 / 36.1 / 23.6 | Yes except Ashcombe 28.7, below its band (29.2 to 30.0) |
| Share over firm capacity | 91 / 62 / 75 / 50 / 0 | 81 / 61 / 79 / 42 / 0 | Yes except Ashcombe 81, below its band (86 to 100); Fenwick 42 is 1 above the band floor (41) |
| Availability share Corvane / Quillon | 0.42 / 0.51 | about 0.47 / 0.55 | Corvane 0.01 above band (0.40 to 0.46); Quillon at band top |
| Rebound per MW Corvane / Quillon | 0.67 / 0.31 | 0.57 to 0.63 / 0.33 | Quillon yes; Corvane partly below band (0.60 to 0.71) |
| Call | commit four, hold Hartwell Common | same list | Yes |
| Files | Appendix A firm capacities, awards PDF contract MW, DFES sheet, 1575 register rows less 39 Superseded = 1536 sites | all agree | Yes |

## Competing answers that survived
None survived as a different list. Rivals the thread ran:
- Now-only credit (sites tested on 4 Nov 2026) gives the same commit set. It is ruled out by the guideline's "in service on the assessment date" wording needing an expected value (the thread's reading); weakest point in the record, see Findings.
- Planned-date credit (14.3 MW at Fenwick Street) drops Fenwick Street. Ruled out by the register's own slip record.
- Pooled lag across classes drops Fenwick Street. Ruled out by the class table.
- Subtract-only with no rebound drops Ashcombe Road (peak about 26.2, share about 6 per cent). Ruled out by the event-day rebound.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Usable files | 10 or more | 14 (6 CSV, 5 xlsx, 3 PDF) | Yes |
| File categories | 2 or more | spreadsheet (xlsx), text (CSV, PDF); 3 formats | Yes |
| Large messy files | CSV of 20,000 rows or more; CSV of 10 to 20 printed pages or more | primary_demand_halfhourly 196,240 rows (10.4 MB); hh_customer_demand_monthly 13,715 rows (well over 20 printed pages); flexibility_asset_register 1,575 rows | Yes |
| Distractors in metadata.json | 2 or more, none labelled in the ZIP | 3: customer_interruptions_2025-26.xlsx, primary_transformer_condition_2026.xlsx, duos_charging_statement_2027-28.pdf; none labelled by name; thread found all three unused | Yes (that none answers a graded quantity by arithmetic was not separately recomputed by me; the thread did not use them) |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, pptx); golden.zip holds exactly those two files | Yes |
| Asks | multi-dimensional, unit and rounding stated | 7 asks (workbook spec plus five per-primary tables, one slide ask); MW to one decimal, share to whole per cent | Yes |
| Answer shape, 4 or more checkable results | one of fourteen shapes | flagged set with share of days over capacity (with allocation-style per-primary table); 11 results in the note, 12 counted by the thread | Yes |
| Golden realism | reads as real work product | not inspected by me (golden files not opened); thread found no authoring language, PDFs are LibreOffice exports, plausible creators | Not re-checked here |

## Gate G reconciliation
Thread: mechanism forecasting; stumping_family analytical_non_defect; surface_read_dependency no; sole_data_defect no.
Design note (Hidden factor record, read after the thread returned): five factors, all "constructed (the simulated process)", each marked "Only in deciding units: no" (heating steepening in 7 of 9 primaries, build-up in 10 of 10 customer types, class lateness across six classes and 29 zones, rebound in every event, availability in both providers). The note's `one_thing` is "Not one thing". Consistent with the thread; no factor is claimed as hidden by a document, and the thread found no single planted defect. Layer-1 mess (SCADA rename, 441 duplicates, S and B flags, weather versions, superseded rows) is texture and decides nothing, as the thread also found.

Points where the thread and the note differ:
- The note says the class-lateness medians "show in one group-by of the register" (R4's fix depth is modelling of the survival with pending and withdrawn sites). The thread's pooled-slip first pass lost Fenwick Street, and it needed the class split plus conditioning on days overdue, which supports the note's modelling depth, but the note's own sensitivity row (class lateness read from commissioned sites alone) keeps the list and earns 3.5 of 11. Not new.
- The note's dispatch of the rebound as "Right in the careful column"; the thread's own first pass omitted it and lost Ashcombe Road, and its Corvane rebound (0.57 to 0.63) is partly below the stated band.

## Gate H reconciliation
Thread: `domain: pass; layers: pass; results: 12 graded across 7 areas; one_thing: none; effort: quick 3, careful 7, thorough 11 of 12; one_fact: rescues 3 of 12`. Its one_fact sentence: "the commissioning dates slip by asset class, and the load comes back after the window".
Note: 11 results (R1 to R11), `Roughly 1.5 of 11 / 3 of 11 / 11 of 11`; largest single hint rescues 2 of 11 (R4, R6); strongest compound sentence 3 of 11; depth level 5.
- Quick pass: thread 3 of 12 (25 per cent) against note 1.5 of 11; below a third in both.
- Careful pass: thread 7 of 12 against note 3 of 11. The thread grades the careful column roughly double the note and leaves it well below the thorough 11. This is a divergence to weigh against the note's calibration to the architecture 6 runs, though the thread's own first-pass analyst failed on the list.
- One-fact: thread 3 of 12, note 2 of 11. Thread's sentence is a compound (two judgments) and still within a third; note puts compound at 3 of 11. Consistent.
- Result count differs (12 against 11), likely a counting difference over the rebound or the commit list; not resolved here.
- The thread's pointed-to hurried failure is Fenwick Street (credit 6 to 7 MW from planned or pooled dates giving a peak of 32.7 to 33.9 MW and share 4 per cent or below, against 35.0 and 50 per cent), which matches the note's R4, R6, R8 to R10 hurried column.
- Distractors: the thread names the three declared distractors as unused, so none is load-bearing.

## Stump power (Gate F)
Thread: Strong. Its first pass committed Charlecote Way and Dunmore Street only; the losses are several independent analytical shortcuts (slip stratification moving Fenwick Street's credit from about 6 to about 4 MW; the rebound moving Ashcombe Road's peak from 26 to 28 MW; suppressed cold-day demand; in-winter ramp of large customers). The note's predicted careful list (Ashcombe Road and Hartwell Common) differs from the thread's first-pass list, but both are wrong in the ways the note predicts (Fenwick Street and Dunmore Street/Charlecote Way each decided by a different judgment). Results a hurried strong model reaches by standard method alone: Charlecote Way's demand and customers' increment largely follow if the register is read carefully; the expected-peak replay with rebound is reached by careful runs per the note.

## Findings, ranked
1. Ashcombe Road band coverage. The thread's corrected independent re-run lands below the stated bands at Ashcombe Road on the expected peak (28.0 against 28.2 to 29.0), the nine-days-in-ten level (28.7 against 29.2 to 30.0) and the share (81 against 86 to 100), and a hair outside on 2025/26 demand (30.85 against 29.9 to 30.8), the Corvane availability share (0.47 against 0.40 to 0.46) and the Corvane rebound (0.57 to 0.63 against 0.60 to 0.71). The call is unchanged (81 per cent is far over 10 per cent). The thread attributes the spread to how the two noise sources are combined and to its morning-anchored baseline. Since a rubric grades against the golden and bands, a defensible rebuild could lose those Ashcombe cells. The thread did not call this a fork; I record it for the main thread to weigh against the note's closure table, and to consider widening the Ashcombe peak, level and share bands.
2. Ashcombe Road's commit rests on the post-window rebound alone (thread optional pin 1): a one-line fork-table entry saying the rebound is read from the event days.
3. Fenwick Street's expected peak equals firm capacity (35.0 against 35.0), so the commit is carried by the ten per cent rule and not the median; its share band (41 to 65) is wide (thread optional pin 2). The thread's own share, 42, sits just inside the band floor.
4. The thread's now-only credit rival also commits Ashcombe Road and Fenwick Street and holds Hartwell Common, so that fork does not change the list; it is closed by the guideline's date wording.
5. Cosmetic: in-service MW above contracted MW at Charlecote Way (8.8 against 8.5) and Dunmore Street (6.2 against 6.0); the thread finds this fine because contracted MW caps only the instruction.
6. Effort grades diverge from the note (careful 7 of 12 against 3 of 11); weigh against the note's effort test.

## Thread's optional notes (verbatim summary)
1. The Ashcombe Road call rests on the post-window rebound; a one-line fork-table entry saying the rebound is read from the event days would document it (golden step 8 already states it).
2. The band on Fenwick Street's share is wide (41 to 65); its expected peak equals firm capacity (35.0), so the call is carried by the ten per cent rule and not by the median.

## Next action for the author
Decide finding 1: either widen the Ashcombe Road expected-peak, nine-days-in-ten and share bands in submission.md (and the matching checks.py bands) to cover the independent rebuild, or confirm in verify.py that the thread's lower figures come from a combination of the two noise sources the filed text does not allow; then add the two one-line fork entries. No model rerun or re-judge is required by the thread's verdict.

## Files and hygiene
Thread: PASS. Nothing authoring-related found; dates coherent (guideline 22 Sep 2026, awards 21 Oct 2026, register 4 Nov 2026, latest demand 1 Apr 2026).
