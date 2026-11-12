# determinism-check report, task13 (architecture 4), 2026-11-11

Re-judge after the stage-2 re-frame (prompt and answer blocks rewritten to lead with what to change before
winter/summer and the 2027 figure; the dashboard's 27,370 is no longer stated or referenced anywhere in the
prompt or the Final Recommendation). First pass (`determinism_check_report_p1.md`) returned DETERMINISTIC,
SEND_BACK on Gate G (banned_stumping_type: the old Final Recommendation and its two top asks were framed as a
compound rejection of the dashboard's 27,370). This pass judges the new version blind, from scratch.

## Verdict
DETERMINISTIC (qualified)
**Disposition:** FIX_NOW, escalating to SEND_BACK on one condition (below)
**Stumping type:** mechanism: decomposition_attribution (netting the receiving-recloser no-fault trips out of the
gross restored count carries the Final Recommendation's two headline figures, 21,328 and 24,679), stumping_family:
analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why

The judge thread worked in isolation: a fresh unzip of `target.zip`, `prompt.txt`, and this judge's own blind
derivation written to `own_derivation.md` before it opened `graded_blocks.md`. On the one result it ran to full
closure (SUPPLEMENTARY_ANSWERS 1, the five-minute restoration table), its blind figures matched the golden exactly
(32,875 / 25,796 / 28,781 / 22,561 / 25,056), including independently discovering the archive's mid-2025 message-
format change and the four supervised-mode events the golden's own method note names. That is real corroboration
on R1 only.

The thread did not reproduce the main recommendation's two headline figures (21,328 for 2026; 24,679, range
17,912-31,580, for 2027), the summer-2027 interruption figure (388), or the battery count (16) to the gates'
"recompute everything" standard. Its own blind pass on part (b), run specifically to find "whatever the automatic
switching did beyond the restored loop" (the user's instruction), landed on 25,056 (no netting), not 21,328: it
found two real but minor receiving-side effects (one capacity-blocked transfer, zero avoided customers; two
"fault on transferred section" OMS rows, both 2023, none in 2026) and did not find the golden's actual mechanism
(receiving reclosers on CTL-4C unswitched directions tripping with cause "Unknown - no cause found" during a
transfer) until after it opened `graded_blocks.md` and searched for the cause code by name. Taken alone this
reads as the designed effort gradient working as intended (R2's hurried failure is named in the design note as
"the restored loop priced alone, no receiving trip netted," and that is exactly the wrong number the thread's
blind pass produced), not as a defect; but it means Gate A is open on R2, R4 and R5's figures, which the
thread never actually recomputed. The gate note's instruction to verify a result by recomputation, not by
confirming the mechanism is "structurally present," was not met for three of five results.

The governing finding is Gate C on R3 (the battery result, which opens the Final Recommendation's first sentence:
"Replace the batteries in 16 recloser controls before December"). The thread independently fit the same weekly
5A BATTERY TEST records the golden's step 4 names and found a rival that survives: a control-type-split
regression (CTL-4C vs CTL-6) gives **1** failing control at -27 C by 28 February 2027 (RCL-21299, 20.89 V); a
pooled fleet-level regression gives **4** (bootstrap 5th-95th percentile **1 to 10**). All three of the thread's
own figures (1, 4, and the 1-to-10 range) fall outside the golden's stated band (14 to 17, with three named
borderline units). The design note's own R3 row names three rivals it ran (a per-battery cold coefficient, the
end of January, -26C/-28C) and reports they move the count by at most two controls at the 21.2V line; it does not
name a pooled-vs-per-device fork, and the thread's lowest-voltage unit (RCL-21299) does not appear in the golden's
16 or its three named borderline units at all. Per the determinism contract, a band that excludes a defensible
rival the thread actually ran is a Gate C failure on that result (R3), and R3 is the Final Recommendation's lead
sentence.

A second, independent concern: Critical Component 2 / Ask 4's "Summer 2027 transfers" figure (388 receiving
customers, Final Recommendation's second bullet) is graded against a "summer 2027" window that neither the
prompt nor the design note's own estimand line pins (the estimand line files only "2022 to October 2026, the end
of February 2027 and the 80 per cent range" -- no summer window, no explicit months). This is a Gate E finding on
a graded component, separate from Gate C's R3 finding, though lower stakes since it affects one ask rather than
the Final Recommendation's lead number.

## Recomputation ledger

| Figure | Claimed (golden) | Thread's figure | Reproduced |
|---|---|---|---|
| Restored within 5 min, 2022-2026 | 32,875 / 25,796 / 28,781 / 22,561 / 25,056 | identical, derived blind | Yes, exact |
| 2026 avoided interruptions (commission definition) | 21,328 | 25,056 (no netting found in blind pass); mechanism later located post-peek, not quantified | No |
| Netting terms (restorations undone / receiving customers put out) | 2,407 / 1,321 | not independently derived; 48 candidate OMS rows located post-peek, not summed/verified against these two figures | No |
| Battery controls failing at -27C by 28 Feb 2027 | 16 (14 at every rival; 3 at the line) | 1 (per-type) / 4 (pooled) / 1-10 (bootstrap 5-95%) | No, and the rival survives outside the band |
| Summer 2027 receiving-customer interruptions | 388 (318-455) | not derived | Not checked |
| 2027 forecast, 80% range | 24,679 (17,912-31,580) | not derived (unnetted annual-mean basis only, 27,214-27,503, no range computed) | No |

## Competing answers that survived

- **R3 (battery count), survives:** the thread's own control-type-split fit (1 failing control) and pooled fit
  (4, bootstrap 1-10) both fall outside the golden's 14-17 band, using the same weekly BATTERY TEST records,
  the same design-basis constants (-27C, 30A, 21.2V), and the same weighted temperature join the golden's step 4
  claims to use. The golden's step 4 says it fits "each control's battery" individually (implying per-device,
  not per-type or pooled), which is a real difference in method, not a contradiction with the files -- but the
  design note's own R3 rival table does not test this fork, and nothing the thread read rules the pooled or
  per-type alternative out. This fork is open until the author runs it.
- **R2/R5, not a surviving fork but an open reproduction gap:** no rival was shown to survive on R2 or R5 (the
  thread did not finish deriving a competing number for either, only an incomplete one), so this is recorded as
  a Gate A coverage gap, not a Gate C finding.

## Spec gates

| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count (usable) | >= 10 | 16 files in `target.zip` (9 CSV, 5 xlsx, 2 PDF) | Pass |
| File categories | >= 2 | 3: spreadsheet, text/CSV, document (PDF) | Pass |
| Large messy CSV >= 20,000 rows | 1 | `adms_flisr_event_archive_2022-2026.csv`, `kmkt_hourly_weather_2022-2026.csv`, `scada_device_events_2022-2026.csv` all qualify | Pass |
| Messy CSV, 10-20 printed pages | 1 | `oms_outage_events_2022-2026.csv`, `scada_hourly_amps_2025-2026.csv` qualify | Pass |
| metadata.json names >= 2 distractors, none labelled inside the ZIP | required | `metadata.json`'s `distractor_files` key (not `distractors`) names `target/ami_outage_notifications_daily_2025-2026.csv` and `target/vegetation_cycle_status_2026.xlsx`; neither name nor any in-ZIP content flags itself | Pass |
| Each distractor unused but relevant, ruled out by a shipped fact | required | `ami_outage_notifications_daily_2025-2026.csv` (date, feeder, last_gasp_msgs, restoral_msgs, meters_reporting) is a plausible but wrong route to the restoration counts (AMI last-gasp/restoral pings vs. the device/ADMS record the golden uses); not independently confirmed that a shipped fact rules it out rather than it simply being unused. Not fully checked this pass. | Not checked |
| 1-3 deliverables requested, all present in golden, no format forced | required | Prompt requests a spreadsheet and a PDF memo; `golden.zip` holds `flisr_review_2026.xlsx` and `flisr_2026_memo.pdf` | Pass |
| Multi-dimensional asks, units stated, no rounding instruction | required | Units stated throughout (customers, volts, per cent); no rounding instruction | Pass |
| Answer shape, >=4 checkable results | required | 5 results (R1-R5) per the design note's Results chain | Pass |
| Golden ZIP holds exactly the requested files | required | Confirmed above | Pass |
| Window/scope pinned for every graded component | required | Ask 4 / Critical Component 2's "summer 2027 transfers" window is not pinned by the prompt or named in the design note's estimand line (which files only 2022-Oct 2026, end-Feb 2027, and the 80% range) | **Fail (Gate E, component-level)** |
| Nothing LLM-generated | required | No tells observed by the thread in the files it read | Pass |

## Gate G reconciliation

- **mechanism / stumping_family:** the thread reported `mixed` as a mechanism value, which is not a valid Gate G
  mechanism (it is a `stumping_family` value). Renaming to its own rule: the single mechanism that, if removed,
  collapses most of the difficulty is `decomposition_attribution` -- netting the receiving-recloser no-fault
  trips out of the gross restored count. This mechanism carries both numbers printed in the Final Recommendation's
  own sentence (21,328 and 24,679) and Critical Components 3 and 4, which is the heaviest-weighted part of the
  rubric by the house's own weighting rule (recommendation and critical components first).
- **surface_read_dependency: no, carried from the thread.** Unlike the first pass's version, no shipped file
  states or claims 25,056 or 27,370 as the commission-definition answer; the dashboard's 27,370 is explicitly the
  vendor's own cruder metric (gross completed sequences, no five-minute cutoff), confirmed correct at its own
  definition by the thread's independent reproduction, and nothing in the prompt or Final Recommendation names or
  rejects it. The reframe genuinely removed the "reject a stated conclusion" shape: nothing is rejected, because
  nothing states a final answer for the model to disbelieve. This is a real, not cosmetic, change from the
  SEND_BACK'd architecture.
- **Gate H, H3 (not one thing):** the design note's own Hidden factor record marks all four factors "keep"
  (none confined to the deciding units; each needs investigation plus modeling, not one routine step), and the
  Carry-forward table shows the netting mechanism feeds only R2 and R5, leaving R1, R3 and R4 standing on their
  own inputs. On the design note's own account H3 passes.
- **H4/H5, effort test:** the design note's own table (quick 0/5, careful-but-hurried 1/5, thorough 5/5; largest
  single hint rescues R2 only, and even then leaves R5 outside its band) is corroborated, not contradicted, by
  this pass: the thread's blind run (acting as a careful-but-time-boxed solver) got exactly R1 and missed R2,
  matching the design note's prediction almost exactly. This is evidence the effort gradient is real on R1/R2,
  not evidence of a shallow stump.
- **Net:** Gate G and H3-H5 pass on this reframe; the reframe did close the earlier SEND_BACK. The problem this
  pass finds is a different one: Gate C/A on R3 (a defensible rival outside the stated band) and an unpinned
  window on one component (Ask 4 / Critical Component 2), neither of which existed in the first pass's finding.

## Stump power (Gate F)

Real and spread across results where checked: R1's format-cutover and supervised-mode traps are genuine and
exactly reproduced blind; R2/R5's netting mechanism is real, not surface-read-rejection, and the thread's own
blind miss on it (despite being specifically told to hunt for a receiving-side effect) is a good sign for H4,
not a bad one. The open risk is the opposite direction from "too easy": if R3's band in fact excludes a
defensible pooled or per-type fit (not yet ruled out), then R3's stated band is too narrow to separate a
competent rival from the golden, which Gate F and Gate C both treat as grading nothing on that result rather
than as difficulty.

## Findings, ranked

1. **(FIX_NOW, governing; escalates to SEND_BACK on the condition below)** Gate C: the battery count (R3, the
   Final Recommendation's lead sentence) has a defensible rival (a pooled or control-type-split regression on
   the same BATTERY TEST records) that lands at 1 or 4 failing controls, with a bootstrap range of 1 to 10,
   wholly outside the stated 14-17 band. Governing taxonomy label: `margin_or_boundary_fragility` /
   `competing_defensible_answer` on R3. **Escalation condition:** the author must fit the golden's claimed
   per-device model against the pooled/per-type alternatives on the shipped BATTERY TEST rows and test whether
   per-device (unit-level) effects are statistically significant beyond age and temperature. If they are
   significant, record that ruling in Step 4 and the closure table and re-judge once; FIX_NOW stands. If they
   are not significant, the stated band does not hold against a competent rival and the disposition becomes
   SEND_BACK (the result needs a different pin: either a stated convention naming the per-device method as
   required, or a widened/re-derived band). Also check RCL-21299's battery-install and replacement dates under
   both the pre- and post-upgrade tag formats, since it is the thread's own lowest-voltage unit and does not
   appear in the golden's named set at any margin.
2. **(FIX_NOW, independent of 1)** Gate E: Ask 4 / Critical Component 2's "summer 2027" window for the
   388-customer figure is not pinned by the prompt or named in the design note's estimand line. Pin the exact
   months/hours "summer 2027" covers in the prompt or a filed convention before the next upload.
3. **(informational, does not independently change disposition)** Gate A coverage gap: R2's 2,407/1,321 netting
   terms, R4's 388, and R5's 24,679/range were not independently recomputed in this pass (only their underlying
   mechanisms were structurally confirmed present and joinable in the files). This is a coverage gap in a single
   medium-effort pass, not a contradiction; it is recorded so the next reviewer does not read "structurally
   confirmed" as "recomputed."
4. **(informational)** The distractor-relevance test (each distractor unused but load-bearing-adjacent, ruled
   out by a named fact) was not completed for `ami_outage_notifications_daily_2025-2026.csv`; worth a quick check
   that no shipped fact lets a solver compute the five-minute restoration count or the commission figure from AMI
   last-gasp/restoral pings instead of the device/ADMS record, since the two would plausibly disagree and the
   distractor needs a named reason it is not a second route to the same answer.

## Next action for the author

Before the next upload: run the battery model (R3) both per-device and pooled/per-type on the shipped weekly
BATTERY TEST records and record in the design note's closure table whether unit-level effects are significant
beyond age and ambient temperature; if they are, the 14-17 band holds and this pass's FIX_NOW closes with no
prompt or file change. If they are not, R3's band needs rebuilding (a stated convention pinning the required
granularity, or a verified wider band) and the disposition is then SEND_BACK, since that changes what a solver
is expected to produce. Independently, pin the "summer 2027" window for Ask 4 / Critical Component 2 in the
prompt or a filed convention. Re-judge once after either fix is made.
