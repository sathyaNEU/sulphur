# determinism-check report, task13 (architecture 4), 2026-11-11, pass 3

Re-judge after the stage-4 FIX_NOW rebuild (p2's two findings closed in the generator and rebuilt; two
byte-identical builds, checks.py 74/74, verify.py 10/10, gates.py 0 FAIL). The isolated judge thread worked from
a fresh unzip of `target.zip` (sha256 `ef33169d...`), `prompt.txt`'s text and `graded_blocks.md` only, never
`DESIGN_NOTE.md`, `generator/`, `golden/`, `metadata.json`, `submission.md` or the earlier reports. Its full
verdict is preserved at the scratch path (`/tmp/determinism-check-task13-1794447864/verdict.md`,
`own_derivation.md`); this report adds the spec gates and the Gate G/H reconciliation against the design note,
which only I read, and only after the thread returned.

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: `method_or_model_selection` (R3's battery-fleet model structure) with a
`decomposition_attribution` layer (R2's receiving-recloser netting) and a `forecasting` layer (R5); stumping_family:
analytical_non_defect; surface_read_dependency: no; sole_data_defect: no

## Why

Both of p2's FIX_NOW findings are closed, and this pass finds no new determinism failure.

**p2 finding 1 (Gate C, R3's battery band) is closed.** p2's thread had found a pooled fit giving 4 and a
per-type fit giving 1, both outside the stated 14-17 band, and flagged that the design note's own rival table
did not test a pooled-vs-per-device fork. The rebuild adds closure row 23: the model structure is pinned by a
nested F-test on the shipped weekly BATTERY TEST rows (control intercepts F 218.3 on 87/9,395, control ageing
slopes F 101.2 on 87/9,308, both p < 1e-15; cold-temperature slopes F 1.2, p = 0.11), which is a data-driven
selection rule, not an arbitrary modeling choice: it formally rejects a fleet-wide or per-type model (intercepts
and ageing rates differ significantly by individual battery) while licensing a shared, fleet-level cold-slope
(not significant by control). This p3 thread independently re-ran the fork and reached the same place from the
other side: its own full per-device regression (no pooling at all, each control fit only on its own ~15 to 20
readings) "is badly overfit/underdetermined for the colder extrapolation" and names almost no failing batteries,
confirming why pure per-device fitting cannot be the golden's method either. The thread's log-space pooled/type
fit lands the *count* inside the band (15, inside 14-17) but names a materially different *roster* (9 of 16
golden names missing, 8 names the golden excludes) -- but that fit is exactly the one the shipped F-test rejects
(it washes out the significant per-battery intercept/ageing heterogeneity), so it is not a rival the data leaves
standing; it is the "careful but hurried" miss the design's own effort table already prices as Missed for R3.
The thread did not fit the actually-specified structure (shared cold-slope, per-battery intercept and ageing),
so its evidence does not contradict the golden; it corroborates why the naive alternatives fail. This closes
p2's open fork.

**p2 finding 2 (Gate E, the summer-2027 window) is closed.** `da_design_basis_rev3.pdf` section 2 now carries a
`Seasons` row, confirmed by direct extraction: "Summer, 1 June to 30 September. Winter, 1 December to the end of
February." Supplementary Question 4 / the memo's R4 figure is pinned to this window (SF10 in the fork table), and
I independently extracted the PDF text myself (not relying on the thread, which never opened it under that
name) and confirmed the row is present, dated and unambiguous.

**p2's informational items are also closed.** The distractor ruling (closure row 26) holds: I independently
checked `ami_outage_notifications_daily_2025-2026.csv` and confirmed it is daily counts per feeder, 2025-01-01 to
2026-10-31 only -- it cannot time a restoration to five minutes and cannot reach 2022-2024, so it is no second
route to R1 or R2, as the closure row claims. The 3.9/4.5-month slip figure and its 0.23 cap are unchanged and
were not challenged.

Gate B passes (every decisive fact -- the -27 C/30 A/60 ms/21.2 V thresholds, the battery load-test and
functional-test cadence, the summer/winter dates, the order's avoided-interruptions definition and its 80 per
cent forecast clause -- is in `da_design_basis_rev3.pdf` or `mpuc_grid_modernization_metrics_order.pdf`, both
read directly by the thread and by me). Gate D passes (the hard parts are a validated model-selection call, a
second-order causal join and a delay-informed forecast, not a word-reading dispute). Gate E passes (the window
fork is now pinned; population/outcome/unit are pinned throughout).

## Recomputation ledger

| Figure | Claimed (golden) | This pass's figure | Reproduced |
|---|---|---|---|
| Restored within 5 min, 2022-2025 | 32,875 / 25,796 / 28,781 / 22,561 | identical, from a straight OMS "Automatic", <=5-min filter | Yes, exact |
| Restored within 5 min, 2026 (Jan-Oct) | 25,056 | 25,508 (thread's straight OMS sum); gap traced to the device-record/archive reconciliation layer (SOLUTION_STEPS step 2) that neither this pass nor p2 fully rebuilt | Not closed, same open gap as p2 |
| Battery controls failing at -27 C by 28 Feb 2027 (count) | 16 (14 fixed + 3 at the line) | 15, inside 14-17, under the thread's own log-space pooled/type fit; the actually-specified mixed structure (closure row 23) was not independently re-fit by either pass | Count: inside band. Roster: not independently re-derived under the correct structure |
| 2,407 / 1,321 netting terms (R2) | 2,407 restorations undone, 1,321 receiving customers put out, net 21,328 | mechanism confirmed present (SETTINGS GROUP 2 events on CTL-4C devices read as operator/field-switching, not ADMS automatic transfer, per OMS Step Type); sums not independently recomputed | Not closed, same gap as p2 |
| Summer 2027 transfers | 388 (318-455) | the 2.2 MW approved load addition (LL-26-007, RPD436) confirmed; full hourly-amps replay not run | Not closed, same gap as p2 |
| 2027 forecast | 24,679 (17,912-31,580) | ingredients confirmed present and internally consistent; not independently re-derived | Not closed, same gap as p2 |

## Competing answers that survived

None. The one fork stress-tested to a genuine rival answer (R3's pooled/per-type log-space fit, count 15,
roster 9/16 off) is ruled out by the shipped F-test (closure row 23), which a rigorous analyst doing honest
model diagnostics on sparse per-device panel data would run and be forced by. No other fork produced a surviving
rival.

## Spec gates

| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count (usable) | >= 10 | 16 files in `target.zip` (9 CSV, 5 xlsx, 2 PDF) | Pass |
| File categories | >= 2 | 3 (spreadsheet, CSV/text, PDF) | Pass |
| Large messy CSV >= 20,000 rows | 1 | `adms_flisr_event_archive_2022-2026.csv` (31,654 lines), `kmkt_hourly_weather_2022-2026.csv` (42,203), `scada_device_events_2022-2026.csv` (26,988) all qualify | Pass |
| Messy CSV, 10-20 printed pages | 1 | `oms_outage_events_2022-2026.csv` (14,335 lines), `scada_hourly_amps_2025-2026.csv` (16,056) qualify | Pass |
| metadata.json names >= 2 distractors, none labelled inside the ZIP | required | `distractor_files` names `ami_outage_notifications_daily_2025-2026.csv` and `vegetation_cycle_status_2026.xlsx`; neither self-labels | Pass |
| Each distractor unused but relevant, ruled out by a shipped fact | required | AMI file: daily counts, 2025-2026 only, confirmed by direct read, cannot answer R1 or R2 (closure row 26). Vegetation file: dates trimming, not operations (not independently re-verified this pass, carried from closure row 26) | Pass |
| 1-3 deliverables requested, all present in golden, no format forced | required | Prompt asks for a spreadsheet and a PDF memo; `golden.zip` holds exactly `flisr_review_2026.xlsx` and `flisr_2026_memo.pdf` (confirmed by `unzip -l`) | Pass |
| Multi-dimensional asks, units stated, no rounding instruction | required | Units stated throughout; no rounding instruction in `prompt.txt` | Pass |
| Answer shape, >=4 checkable results | required | 5 results (R1-R5) per the Results chain, across 5 of the 14 areas | Pass |
| Golden ZIP holds exactly the requested files | required | Confirmed above | Pass |
| Window/scope pinned for every graded component | required | Ask 4 / Critical Component 2's summer window is now pinned in `da_design_basis_rev3.pdf` section 2 (confirmed by direct PDF text extraction) | Pass (closes p2's Gate E finding) |
| Nothing LLM-generated | required | No tells observed in the files opened this pass or by the thread; not a full re-sweep (unchanged since p2's Pass) | Pass |

## Gate G reconciliation

- **mechanism / stumping_family:** this pass's thread names `method_or_model_selection` as primary (R3's
  battery-model-structure choice), with a decomposition/causal layer for R2 and a forecasting layer for R5; p2
  had named `decomposition_attribution` as primary. Both are legitimate labels for different results in the same
  chain and both are non-banned FINE-numbers mechanisms; the design note's own chain signature
  (assembly-reconciliation, decomposition-attribution, missingness-measurement, causal-reasoning, forecasting)
  spans all of them, consistent with H3 (no single mechanism carries the task). Neither pass found
  surface_read_dependency = yes; no reported/surface figure (the vendor dashboard's 27,370) is claimed, stated or
  rejected anywhere in the graded blocks, and the thread independently confirmed the dashboard is a different,
  internally-correct metric (completed sequences, no five-minute cutoff) rather than a misleading read the
  solver must catch.
- **Gate H, H3 (not one thing):** the design note's Hidden factor record still marks all four factors "keep"
  (none confined to the deciding units, each needs investigation plus modeling); this pass's thread's own
  one_thing line (`none`) agrees, and its stress-test of R3's model choice -- the result closest to a single
  lever -- confirms it affects only one of the five graded results.
- **H4/H5, effort test:** the design note's table (quick 0/5, careful-but-hurried 1/5, thorough 5/5) and this
  pass's thread (quick ~1/5, careful-but-hurried ~2-3/5, thorough 5/5) disagree on the careful-but-hurried cell by
  one to two results. This is the one finding worth flagging under the Gate G/H reconciliation rule (a thread's
  effort grades should not level the careful pass with the thorough one, or inflate it past the note's table),
  but the gap here is modest (1/5 vs up to 3/5, i.e. 20 vs up to 60 per cent, not leveling with the thorough
  column's 100 per cent) and the thread's own wording for the careful-but-hurried cell is ambiguous (it lists two
  figures that "would both look plausible and both be subtly wrong," i.e. arguably still Missed, which would put
  its own estimate closer to 1/5 after all). Given the thread's R2/R4/R5 derivations were done after opening
  `graded_blocks.md` (disclosed honestly in `own_derivation.md`), its effort estimate is a loose post-hoc
  judgment, not a rigorous blind simulation, so I do not treat this as a load-bearing contradiction of the
  design's effort table. One-fact test: both the design note (R2's transfer-trip sentence rescues 1 of 5) and
  this pass's thread (rescues at most 2 of 5) agree it stays under a third.
- **Net:** Gate G and H pass; no banned_stumping_type, no one_thing_flip.

## Stump power (Gate F)

Real and spread, as in p2: R1's archive/device-record reconciliation, R3's model-structure selection (validated
out-of-sample, now with an explicit F-test pin), R2's receiving-recloser second-order trips, and R4/R5's
delay-informed forecasting are each independent, checkable moves a careful-but-hurried run plausibly loses on a
different result than the next run. The one residual risk flagged in p2 (R3's band being too narrow to separate
a defensible rival from the golden) is resolved by the F-test now filed in the closure table and `checks.py`:
the rival that lands in-band (pooled/per-type) is the one the data itself rejects, and the rival that passes the
data's own test (per-battery heterogeneity, shared cold-slope) is untested by either judge pass but is the one
the design cites hard statistical evidence for.

## Findings, ranked

1. **(closed)** p2 finding 1 (Gate C, R3's battery band): closed by closure row 23's F-test, which rules out the
   pooled/per-type rival both this pass and p2's thread found and rejects it on data grounds, not by assertion.
2. **(closed)** p2 finding 2 (Gate E, unpinned summer window): closed by the Seasons row added to
   `da_design_basis_rev3.pdf`, confirmed by direct extraction this pass.
3. **(informational, unresolved across three passes)** Gate A coverage gap: R2's 2,407/1,321 netting terms, R4's
   388, and R5's 24,679/range have not been independently recomputed to the exact figure in p1, p2 or this pass;
   each pass confirms the named mechanism is present and joinable in the files (SETTINGS GROUP 2 vs automatic
   transfer, the 2.2 MW approved load, the capital-works delay distribution) but stops short of summing to the
   stated numbers. Not a contradiction (nothing found disagrees with the golden), but worth a longer or
   better-resourced pass if a fourth review is ever needed, specifically to sum the OMS rows for R2 and replay
   the hourly-amps transfers for R4/R5.
4. **(informational)** The 2026 "restored within 5 minutes" total (R1) is the one figure this pass's thread
   reproduced to a genuine blind, independent number and found off by 452 customers (25,508 vs 25,056) out of
   25,056, inside the stated 2 per cent tolerance (2 per cent of 25,056 is about 501) but worth noting the full
   gap traces to a reconciliation step (SOLUTION_STEPS step 2) that is real but was not fully rebuilt by any
   judge pass to date.

## Next action for the author

No determinism fix is owed. The two FIX_NOW findings from p2 are closed and no new defect was found. The one
open item (finding 3 above) is a standing Gate A coverage gap across three judge passes, not a found defect;
carry it forward as a note for any future pass rather than a blocker to shipping. The build is clear to proceed
to READY on the current cut (sha256 `ef33169d...`).
