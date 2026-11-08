# determinism-check report, task11, 2026-11-08 (FIX_NOW re-check of the /fix-rubric re-ship)

## Verdict
DETERMINISTIC (no SOLUTION_WRONG). Judged on the prompt as it now stands, with the month-clock words added.
**Disposition:** APPROVE. Both judge findings are closed, one by the shipped words and one by shipped data. Optional hardening is listed under Findings.
**Stumping type:** mechanism: decomposition_attribution (inflow placement, counterfactual on honest data), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
One judge thread (sonnet, medium) ran on the pre-fix prompt, which lacked "calendar month ... on local time". The main call and the 47 days reproduced. On each of the 47 days only Fennick Creek's water enters at the intake's layer. The nearest approach by any other sub-watershed is 4.5 m, so the 2 m window and the 30-day lookback do not matter. Without Fennick's atrazine no day exceeds 3.0, so the SOP-WQ-07 replay never starts the feed. Without any other sub-watershed the replay equals the plant record. The golden is therefore the literal counterfactual. The judge's FIX_NOW had one pin (the month clock) and one soft exposure (the background). I re-read the prompt and the design note for both.

## Recomputation ledger (from the judge's verdict)
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Days above 3.0, 15 Apr-31 Oct (SOP 2.3: GC/MS else ELISA) | 47 | 47 (29-30 May; 9-30 Jun; 1-21, 24, 27 Jul) | Yes |
| Monthly days | May 2, Jun 22, Jul 23, other months 0 | same | Yes |
| Stratified period | 27 Apr-6 Oct | same | Yes |
| Intake depth | 10.4-11.0 m | same | Yes |
| Placement depths, 29 May-27 Jul | Fennick at the intake; others shallower | Fennick 10.0-10.9 m; Tessel at most 4.1 m, Oxley 3.9 m, Dunmore 2.6-5.9 m, Ladd below the string | Yes |
| SOP replay | 11 setpoint changes, 29 May-6 Aug | match SCADA exactly | Yes |
| PAC lb, local calendar month | 3,243 / 25,024 / 23,776 / 3,693 | 3,242.7 / 25,023.8 / 23,775.8 / 3,693.1 | Yes |
| Other four sub-watersheds | 0 days, 0 lb | 0 | Yes |

## Competing answers that survived
1. **Month clock (judge fork 1).** The pre-fix rivals were:
   - plant-day month: 3,570 / 24,961 / 23,700 / 3,504
   - fixed CST: 3,297 / 25,013 / 23,763 / 3,662
   - UTC month: 2,970 / 25,076 / 23,839 / 3,851

   The ask now reads "each calendar month from May to August, on local time".
   - "Calendar month" rules out the 06:00 plant-day month.
   - "On local time" rules out the UTC month.
   - The CST reading is a clock the files themselves mark as non-local. The buoy is logged on CST, and the tributary exports carry the local offset (-05:00 in summer), so local time in May to August is CDT.

   **The fork is closed.** I did not re-run the rival numbers on the new text. The judge's pre-fix values are the reference.
   - Residual: a solver who reads "local time" as the Central standard clock (CST) gets 3,297 / 25,013 / 23,763 / 3,662. That is a stretch against "local", given the shipped offsets, and I do not rate it a surviving fork. Writing "(Central Daylight Time while in effect)" in the ask would remove it.
2. **Background atrazine (judge fork 2).** Closed by SF22 in the design note's fork table.
   - The raw water held 0.17-0.32 ug/L from January to 17 April, before any 2026 application. The background therefore predates every sub-watershed's 2026 runoff, so it belongs to nobody for the counterfactual. `checks.py` asserts it (line 272).
   - The pre-fix alternative, a load-share split of the background, gave Tessel up to about 8 days against Fennick's 47. That is below Fennick's 47, so the main call is unaffected either way. Only the "0" answers moved.
   - **This is adequately closed by data the bundle ships**, in the pre-application record in the raw-water log. It does not need a filed line. A reader can see the pre-application level and that the golden's reading is the literal one: the counterfactual removes a sub-watershed's atrazine, and the background is none of theirs.
   - The counterfactual rival is a stretch rather than a defensible reading. It apportions water that no shipped file ties to any sub-watershed.
   - SF22 sits in the design note, so the judge never saw it. That is correct, because the closure is the pre-April record in the pack.
3. **Rival main call, mixed lake with load shares (Tessel).** Ruled out by the buoy profile, the intake elevation and the creek temperature records. The 2026 pulses match Fennick's storms.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Usable files | 10 or more | 28 | Yes |
| Categories | 2 or more | 5 (csv, xlsx, pdf, dat, txt) | Yes |
| Large messy CSVs | 20,000+ rows; one of 10-20 printed pages or more | five hydro CSVs of about 29,000 rows; alarm history about 59,000 | Yes |
| Distractors in metadata.json | 2 or more, unlabelled in the ZIP | 3: tributary_nitrate_2026.csv, merrin_beach_ecoli_2026.csv, haldane_extension_atrazine_use_survey_2026.xlsx | Yes |
| Distractor weighs but is ruled out | reproduces arithmetically; a shipped fact rules it out | Haldane use survey ranks Tessel first; plan SWP-01 5.1 (days caused) rules it out | Yes |
| Deliverables | 1 to 3, all in the golden | docx, xlsx, png; all three in golden.zip, exactly those three | Yes |
| Asks multi-dimensional, unit and rounding stated | each | day counts by sub-watershed by month (5 x 8 cells); pounds by sub-watershed by 4 months, to the nearest whole pound | Yes |
| Answer shape | many gradable cells downstream of the deep step | grid of 40 day-count cells and 20 pound cells | Yes |
| Realism | no LLM generation, no build-revealing file | judge found real tooling properties and system-native mess; no authoring text | Yes |

## Gate G reconciliation
`mechanism: decomposition_attribution`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`.
The design note names the same trap: the load-share apportionment naming the Tessel River (39 of 47 days). The declared distractor (the Haldane use survey) gives a rival that ranks Tessel first, but the judge names the stratified-lake placement, not the survey, as the step that carries the task. The distractor is therefore not the surface read and is not too load-bearing. **No mismatch found.** I read the metadata and the design note's stump sentence and fork table only after the verdict was in.

## Gate H
`domain: pass`, `layers: pass`, `decisive_step: analytical`, `chain: 4 inferences (daily lake profile, intake depth, per-sub-watershed placement, SOP replay without each source), judgment: a layered plunging-inflow model over a mixed lake, justified by the buoy, the intake depth and the raw-water pulses`, `one_fact: "Each creek's water enters the stratified lake at the depth where the lake matches its temperature, and the intake draws from about 10.5 m."`
Gate H5 passes thinly (the judge's word): the one fact removes the trap but not the chain.

## Stump power (Gate F)
- The deep step is the layered placement and the SOP replay. The trap that does the work is the load-share reading, which a strong solver can fall into. The shipped chain is not textbook method applied to settled inputs, since the model must be built and checked.
- The weakness in the pre-fix version was that the exact-pound ask lost runs on the clock. That would have been a semantics loss, which the platform bar rejects. The pin moves the pounds ask back onto the deep step: a solver who gets the placement wrong gets the carbon grid wrong, because Fennick's pounds move with it.
- One caution for the main thread: a run can still lose on a clock slip (DST, UTC, plant-day) inside an otherwise correct analysis. That would be a formatting or clock loss, not an analytical one, so check each run's first wrong step in `/triage-runs`.

## Findings, ranked
1. Month clock: closed by "each calendar month ... on local time". Optional hardening: add "Central Daylight Time" or equivalent to rule out the fixed-CST rival.
2. Background atrazine: closed by the pre-application record, SF22 and the `checks.py` assertion. No filed line needed.
3. The pre-fix judge found no other fork. The 47, the monthly counts, the replay and the stratification dates all reproduce.

## Next action for the author
Re-ship with the revised prompt. If you want zero residual on the clock, replace "on local time" with "on local time (Central Daylight Time while in effect)". It changes no figure and needs no pack change.
