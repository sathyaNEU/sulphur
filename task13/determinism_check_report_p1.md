# determinism-check report, task13 (architecture 4), 2026-11-11

## Verdict
DETERMINISTIC
**Disposition:** SEND_BACK
**Stumping type:** mechanism: planted_defect_flip (compound: duration/population misread + coverage/join gap + a double-count-style netting correction), stumping_family: surface_read_rejection, surface_read_dependency: yes, sole_data_defect: yes

## Why

The judge thread, working in isolation from a fresh unzip of `target.zip` plus `prompt.txt` only, derived its own
answer before opening the graded blocks. Its independently-derived year-by-year "restored within five minutes"
figures (2022 32,875; 2023 25,796; 2024 28,781; 2025 22,561; 2026 25,056) and its independent reconciliation of the
vendor dashboard's 27,370 (the sum of the "CI saved" column in `adms_flisr_kpi_dashboard_2022-2026.xlsx`, January to
October 2026) matched the golden's Ask 1 and the Final Recommendation's walk exactly, before it had read a single
graded block. That is strong, blind corroboration that the headline arithmetic is grounded in the shipped files
(Gates A/B pass on this spine of the task).

But Gate G fails on the shape of the main recommendation. The Final Recommendation and its two top-weighted asks
(the main recommendation and Supplementary Questions 1-2) are built, start to finish, as a compound rejection of
the vendor dashboard's reported 27,370: a duration filter (restorations over five minutes do not count, -2,314),
an archive-completeness correction (35 lockouts the archive loses in storm overflows, filled at the archive's own
rate to 27,654, or counted from the device record at 25,056), and a causal-netting layer (receiving-recloser
transfer trips that undid 2,407 restorations and put out 1,321 more customers), landing on 21,328. The judge
confirmed each mechanism is genuinely present in the data, not fabricated (the settings-group-2 ADMS-vs-operator
split is real and visible in `scada_device_events_2022-2026.csv`; the supervised-mode loop and its two slow 2026
restorations are real), which rules out `solution_incorrect` or `reversed_or_fabricated`. The problem is not that
the chain is ungrounded; it is that Gate G bans this exact shape "regardless of depth": a multi-step chain whose
core is catching that a reported number is wrong and flipping away from it is retired no matter how many forced
corrections it takes, even when deterministic and well-grounded. The litmus applies cleanly here: 27,370 is
genuinely wrong against the commission's own definition (`mpuc_grid_modernization_metrics_order.pdf` paras 2-3),
and catching that is explicitly the main stump, by the Final Recommendation's own wording ("...not the dashboard's
27,370...").

Governing taxonomy label: `banned_stumping_type` (surface_read_dependency = yes as the primary strategy on the
main recommendation and its two heaviest-weighted asks).

## Recomputation ledger

| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Restored within 5 min, 2022-2026 | 32,875 / 25,796 / 28,781 / 22,561 / 25,056 | 32,875 / 25,796 / 28,781 / 22,561 / 25,056 (independently, before reading blocks) | Yes, exact |
| Dashboard 2026 total | 27,370 | 27,370 (sum of "CI saved," Jan-Oct, `adms_flisr_kpi_dashboard_2022-2026.xlsx`) | Yes, exact |
| ADMS-vs-operator settings-group-2 mechanism | "ADMS never moves the receiving recloser to group 2" on 16 unswitched directions | Confirmed real and visible: 21 devices in `scada_device_events_2022-2026.csv` show group-2 set only by a human operator, never automatically; golden's 16 is a plausible loop-direction-level subset of this device-level set, not independently re-derived to the device level | Mechanism confirmed; exact 16-direction mapping not re-derived |
| Lockouts 2022-2026 | 405 | 411 (judge's own reconstruction on 44 loop breakers + 88 loop reclosers) | Close; within the kind of convention margin (which devices count as "in-service loop") the design note's bands anticipate; not flagged as a defect |
| 2,407 restorations undone / 1,321 receiving customers put out | 2,407 / 1,321 | Not independently re-derived in the judge's budget; mechanism (transfer-trip no-cause-found events in `oms_outage_events_2022-2026.csv` tied to unswitched directions) confirmed real | Mechanism confirmed, final arithmetic not independently checked |
| Archive gap-fill, 2026 | 27,654 (rejected) vs 25,056 (used) | Not independently re-derived; the archive-overflow mechanism (35 missing lockouts, all inside incident-log overflow windows) confirmed real | Mechanism confirmed, final arithmetic not independently checked |
| 16 recloser batteries to replace | list of 16, with 3 at the 21.2V line | Battery design constants (-27C, 21.2V/30A, weekly 5A test, 4-year cycle) confirmed verbatim in `da_design_basis_rev3.pdf`; a quick R=(V_REST-V_LOAD)/5 regression against age and temperature showed the physically correct sign; full per-device pass/fail list not finished against the golden's 16 names | Mechanism and modeling path confirmed; final 16-name list not independently checked |
| 2027 forecast | 24,679 (17,912 to 31,580) | Not independently re-derived in the judge's budget | Not checked |

## Competing answers that survived

None of the fork/rival checks the judge ran turned up a surviving competing answer on the figures it did
independently check (Ask 1, the dashboard reconciliation, the ADMS-vs-operator mechanism). The judge's budget did
not extend to independently re-deriving the final 2,407/1,321 netting, the 27,654 gap-fill, the per-device battery
list, or the 2027 forecast's point estimate and range; it confirmed each underlying mechanism is real and traceable
rather than fabricated, which rules out the common failure shapes (missing input data, fabricated mechanism,
misattribution) without constituting a full independent recomputation of those four figures. This is a budget gap
in the single pass, not a reported fork; nothing in the design note's own fork and closure tables (read only after
the thread returned) names an open fork on these figures either.

## Spec gates

| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count (usable) | >= 10 | 16 files in `target.zip` (9 CSV, 5 xlsx, 2 PDF); none are system files or placeholders | Pass |
| File categories | >= 2 | 3: spreadsheet (xlsx), text (CSV), document (PDF) | Pass |
| Large messy CSV >= 20,000 rows | 1 | `adms_flisr_event_archive_2022-2026.csv` (31,654 lines), `kmkt_hourly_weather_2022-2026.csv` (42,203 lines), `scada_device_events_2022-2026.csv` (26,988 lines) | Pass |
| Messy CSV, 10-20 printed pages | 1 | `oms_outage_events_2022-2026.csv` (14,335 lines), `scada_hourly_amps_2025-2026.csv` (16,056 lines) satisfy a printed-page-range file alongside the >=20k file | Pass |
| metadata.json names >= 2 distractors, none labelled inside the ZIP | required | `metadata.json` names `ami_outage_notifications_daily_2025-2026.csv` and `vegetation_cycle_status_2026.xlsx`; neither file name nor any in-ZIP content flags itself as a distractor | Pass |
| Each distractor unused but relevant, ruled out by a shipped fact | required | Not separately verified by the judge in this pass (its mandate was the gates above, not an independent distractor-relevance check); no finding against it either | Not checked this pass |
| 1-3 deliverables requested, all present in golden, no format forced | required | Prompt requests a spreadsheet and a short PDF memo; golden.zip holds exactly `flisr_review_2026.xlsx` and `flisr_2026_memo.pdf`, matching | Pass |
| Multi-dimensional asks, units stated, no rounding instruction | required | Each ask states its unit (customers, volts, per cent); no rounding instruction in the prompt; asks 1-4 and the memo request are each multi-dimensional | Pass |
| Answer shape is one of fourteen, >=4 checkable results | required | Design note declares "a bridge that reconciles two totals... with the diagnosis of every loop, control and transfer direction... and the 2027 forecast on top"; 5 results (R1-R5) in the results chain | Pass |
| Golden ZIP holds exactly the requested files, requested formats | required | Confirmed above | Pass |
| Nothing LLM-generated, every golden reads as a real work product | required | Judge's hygiene check: no LLM tells observed in the input files (mixed date formats, realistic header blocks, a plausible 2026 logging-format change, genuine negative-duration/negative-battery-age artifacts); golden deliverables themselves not separately re-inspected by the judge in this pass | Pass (inputs); golden not separately checked |

## Gate G reconciliation

The judge's Gate G finding (`mechanism: planted_defect_flip`, `stumping_family: surface_read_rejection`,
`surface_read_dependency: yes`, `sole_data_defect: yes`) sits directly against the design note's own
`## Deep reasoning`, `## Results chain` and `## Effort test` sections, read only after the thread returned, per
contract.

- **The note's own framing already names the shape the judge flagged.** The note calls R2 (the dashboard walk,
  carrying the Final Recommendation) a "decomposition-attribution" result with hurried failure "method shortcut:
  the restored loop priced alone, no receiving trip netted," and separately logs R1 as "earned by careful runs."
  Gate H3's "not one thing" argument (several independent judgments feed R2, R4, R5) is a real H3 answer, but it
  does not reach Gate G: Gate G asks what the **primary** strategy carrying the headline deliverable is, not
  whether other results exist beside it, and here the Final Recommendation's own sentence is explicitly phrased as
  a rejection of the dashboard ("...not the dashboard's 27,370...").
- **One hidden/planted thing carrying most of the weighted score, from the client's bar perspective, is not quite
  what is happening here** (H3's `one_thing` comes back `none`: four largely independent judgments feed R2 and R5,
  and R1/R3/R4 stand on their own inputs per the note's carry-forward table), so this is not a Gate H one-thing
  failure. It is squarely a Gate G shape failure: the note's `R2 method shortcut: the restored loop priced alone`
  description is, read plainly, "the naive/reported number is wrong because it doesn't net a self-inflicted
  effect," which is exactly the surface-read-rejection shape Gate G retired "regardless of depth."
- **Per the Gate H "one-fact" cross-check:** the note's own `Largest single hint` line claims "the archive lost its
  busiest storm hours, and the devices' own event record holds what the scheme did in them" rescues only R1 (1 of
  5). The judge's independent one-fact line is broader and more damaging: "the dashboard counts every completed
  sequence regardless of duration, and misses events during storm-overflow windows" rescues most of Asks 1-2 and
  the main recommendation (more than a third of the graded weight), though not the battery, capacity or forecast
  sheets. This is the predictor the harness treats as most reliable for a send-back: the thread's best single
  sentence rescues more of the weighted score than the note's stated hint, concentrated precisely on the
  highest-weighted blocks (Final Recommendation and Asks 1-2).
- **A result whose band excludes a rival, or a band too wide to separate the hurried figure from the golden**: not
  found by the judge on the figures it checked (R1's 2 per cent band and the dashboard reconciliation both held
  under the judge's own independent recomputation).
- **The declared distractors carrying a result**: not flagged; the judge did not find either
  `ami_outage_notifications_daily_2025-2026.csv` or `vegetation_cycle_status_2026.xlsx` load-bearing for any
  checked figure.

Net: this is a genuine Gate G send-back on shape, not a Gate H one-thing failure and not a Gate A/B/C/D/E
determinism defect. The repair is structural (re-root the headline deliverable), not a wording fix.

## Stump power (Gate F)

Very high on the figures checked: a dense, multi-layer reconciliation (duration filter, cross-system
archive-gap detection via an incident log, causal netting of self-inflicted transfer trips, a cold-weather battery
regression, a capacity/timing-probability analysis for reinforcements, a seasonally-aware forecast with an 80 per
cent range) that a hurried run would plausibly under-deliver on across several of its parts. No too-easy signal was
observed. The risk here is the opposite one Gate F warns about and the one Gate G is built to catch: the stump
power is real, but it is concentrated in a banned shape on the heaviest-weighted blocks.

## Findings, ranked

1. **(SEND_BACK, governing)** `banned_stumping_type`: the Final Recommendation and Supplementary Questions 1-2
   (the highest-weighted graded blocks) are built as a compound rejection of the vendor dashboard's reported
   27,370, which Gate G retires regardless of depth or how well-grounded each correction is.
2. **(informational, does not independently change disposition)** Three load-bearing figures (the 2,407/1,321
   netting, the 27,654 gap-fill, the final 16-name battery list, and the 2027 point estimate/range) were not
   independently re-derived end-to-end in this single judge pass; their underlying mechanisms were confirmed real
   and traceable, so this is a coverage gap in one pass rather than a reproduction failure, but it means Gate A is
   fully cleared only on the figures actually recomputed (R1, the dashboard reconciliation, the settings-group-2
   mechanism), not on R2's, R3's, R4's and R5's final arithmetic.
3. **(informational)** The distractor-relevance test (each distractor unused but load-bearing-adjacent, ruled out
   by a named fact) was not separately exercised in this pass.

## Next action for the author

Re-root the headline deliverable (the Final Recommendation and the two top-weighted supplementary asks) onto one
of the FINE-numbers results already present and genuinely grounded in this build, per the judge's prescription:
the cold-weather battery forecast (method/model selection, pinned by the design basis, R3) or the 2027
forecast-with-reinforcement-odds (forecasting, R5), and demote the dashboard-to-commission-definition walk (R2) to
a supporting critical component rather than the lead deliverable the Final Recommendation is phrased around. Keep
the genuinely strong, verified parts of this build (the settings-group-2 ADMS-vs-operator mechanism, the
storm-overflow archive gap, the cold-weather regression) as secondary results under the new lead. A model rerun
against the two platform runs is required after the rebuild, per standard Gate G disposition.
