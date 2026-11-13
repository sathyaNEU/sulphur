# determinism-check report, task7, 2026-11-12 (pass2)

Architecture 11 (Hollins Creek Electric Association, the EV Overnight rate's 2027 charging default). The judge filed this
pass as a second report beside architecture 10's; the main thread then filed it as `determinism_check_report.md`, replacing
architecture 10's (kept in git history). This is the first determinism pass on architecture 11. Since this pass the
generator changed two things on the leak reader's notes (Board Policy EV-4 4.3 now reads "An option's cost is its expected
cost.", the same estimand; the monitors' kVA carries no sign), and no graded figure moved.

## Verdict
**DETERMINISTIC**
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect,
surface_read_dependency: no, sole_data_defect: no

**Order kept:** Yes. The isolated judge thread wrote `own_derivation.md` from `prompt.txt`, the
four governing documents (Board Policy EV-4, DPS-7, the pilot plan, the Quillpoint proposal) and
the raw data files in `target/`, before opening `graded_blocks.md`. Its own derivation
independently flagged, before reading the committed answers, that (a) the pilot's own
"average-night" reporting convention is the wrong lens against DPS-7's maximum/quarter-hour
limit and EV-4 4.3's "chance" convention for a random-start option, and (b) own-schedules and
Sequence each need a from-scratch rebuild rather than a read of the 2026 meters or a one-at-a-time
reading of the Sequence algorithm. The golden's Final Recommendation and Critical Components name
exactly those three moves. Nothing in `graded_blocks.md` surprised the thread relative to what it
derived; it logs this explicitly in both `own_derivation.md` and `verdict.md`.

## Why
Every decisive rule the recommendation turns on is filed word for word: EV-4 section 3 (cheapest
option for the year), EV-4 4.1-4.3 (an option's cost = fee + replacements on a summer like 2026,
own schedules as the owner set them, a random-start option scored at its chance), DPS-7 2.1-2.3
(over its limit = highest 15-minute load in July/August above 120% of nameplate kVA, kW/0.95) and
section 4 (nameplate/connectivity as corrected by completed work orders), and the Quillpoint
proposal (each product's rule and fee). The figure that would flip the recommendation if dropped
is Stagger's night-by-night replay (27.5 transformers over, not the pilot's reported-average 0);
without it a hurried analyst picks Stagger as cheapest. The judge independently derived this same
mechanism, from the same two documents, before reading the golden, which is the strongest evidence
the answer is forced rather than argued into.

## Recomputation ledger

| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Chargers enrolled 1 Nov 2026 | 1,313 | 1,313 (1,326 Active rows less 13 byte-identical duplicates; all post-pause rows are hardware swaps) | Yes, exact |
| Transformers serving them | 382 | 382, with the same two DPS-7 s.4 corrections (3 unreflected change-outs, 2 unreflected service transfers) independently located | Yes, exact |
| Platform fee, own/Stagger/Sequence | $0 / $23,600 / $52,500 | $0 / $23,634 to $23,600 / $52,520 to $52,500 (1,313 x $18 and x $40, rounded) | Yes, exact |
| Totals (own/Stagger/Sequence) | $794,600 / $365,200 / $212,800 | Internally airtight: $52,500 + $160,300 = $212,800; $23,600 + $341,600 = $365,200 | Yes, exact |
| Breakeven fee | ~$156/charger | Solved fee x 1,313 + $160,300 = $365,200 -> $156.07 | Yes, exact |
| kW/charger at 23:00-23:15 | 4.95 kW (0.34 managed vs 5.29 own) | ~4.4-4.5 kW on a simplified panel (both summers, constant membership, not scoped to 2026 only) | Same range/sign, not exact; judge's own simplification explains the gap, no contradiction found |
| Stagger transformers over (27.5), Sequence over (11), own schedules over (52) | as stated | not independently re-run (full 382-transformer night-by-night Monte Carlo and the Sequence queueing simulation is a multi-hour build); structure, provenance and arithmetic consistency verified instead | Not independently reproduced figure-for-figure; no internal inconsistency or contradiction found |

The three transformer-count figures (R3, R4, R5 in the design note) are the review's one genuine
scope limit: the isolated thread verified the governing rule for each (DPS-7's maximum/
probability convention, the mixed-regime correction for own schedules, the Sequence "alongside"
exception) is filed and literally executed by the golden's narrative, and found no contradiction
or defensible rival answer, but did not re-run the full simulation to check the exact counts
(27.5, 11, 52) against the bands. This is a medium-effort pass constraint, not a determinism
finding; the design note's own Frontier check records that the full golden family of rivals
(the monitored-peak lift, no lift, declared settings, two other random seeds) all stays inside
the stated bands and calls Sequence.

## Competing answers that survived
None. The only serious rival identified (Stagger, on the pilot's own average-managed-night
reporting) is the task's documented hurried shortcut, not a defensible rival under a literal
reading of DPS-7 2.1 (a maximum, not an average) and EV-4 4.3 (a random-start option scored at
its chance). The judge enumerated this fork itself before reading the golden and reached the
same resolution independently. No fork on population (SF1), window (SF2, SF15, SF16), the limit
convention (SF3), nameplate/connectivity correction (SF4, SF5), the random-option weighting
(SF7), ready-by (SF8), fee or cost basis (SF10, SF11) was found open; each is pinned by a specific
clause in EV-4, DPS-7 or the proposal.

## Spec gates

| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count | >=10 usable files | 19 files in `target/` | Pass |
| File categories | >=2 | 3: csv (13), pdf (4), xlsx (2) | Pass |
| Large messy CSV, >=20,000 rows | 1 | `quillpoint_sessions_2024-06_2026-09.csv`, 277,803 data rows | Pass |
| Messy CSV, 10-20 printed pages | 1 | `ev_overnight_roster_2026-11-02.csv` (1,423 rows x 11 cols, ~24 pages at 60 rows/page); `gis_service_points_2026-10-30.csv` (3,475 rows x 8 cols, ~58 pages); `pilot_assignment_2025.csv` (1,356 rows, ~23 pages) all qualify | Pass |
| metadata.json names >=2 distractors, unlabelled inside the ZIP | yes | `state_ev_registrations_by_zip_2019-2026.csv`, `net_metering_interconnections_2026.csv`; neither filename nor any file content inside `target/` flags either as a distractor | Pass |
| Each distractor unused yet relevant | yes | Both read as plausible load/adoption context for an EV-rate/transformer-loading decision (EV adoption growth, rooftop-solar interconnections netting home load); neither appears in any load-bearing figure the judge or the author traced | Pass |
| 1-3 deliverables, all present in golden, no format family forced | yes | 2 deliverables (`ev_overnight_default_2027_memo.docx`, `ev_overnight_transformers_2027.csv`), both present in `golden.zip`; prompt names no file or format beyond "a short memo" and "a CSV" | Pass |
| Asks multi-dimensional, unit-stated, no rounding instruction in prompt | yes | `prompt.txt` is one paragraph, 619 bytes, states units in-sentence (kW per charger, the fee per charger), issues no rounding instruction | Pass |
| Answer shape, one of the fourteen, 4+ independently checkable results | yes | "Scenarios with the flip point" (three options, each with its over-limit count, fee, replacement cost, total, and the flip fee); 4 Critical Components + 9 supplementary asks, independently checkable | Pass |
| Golden ZIP holds exactly the requested files/formats | yes | `golden.zip`: `ev_overnight_default_2027_memo.docx`, `ev_overnight_transformers_2027.csv`; matches `metadata.json` deliverables exactly | Pass |
| Nothing LLM-generated, every golden reads as a real work product | yes | Judge found no LLM tells, no provenance leakage, no temporal incoherence in `target/`; golden realism was not separately re-checked in this pass (out of scope for the isolated thread, which never opens `golden/`) | Pass (files); not independently re-checked (golden) |

## Gate G reconciliation
Thread: `mechanism: method_or_model_selection`, `stumping_family: analytical_non_defect`,
`surface_read_dependency: no`, `sole_data_defect: no`.

Design note's Frontier check: no `Closed strategies:` line names a deciding closed card; the
deciding lesson (non_additive_aggregation, a shared asset's season maximum of a sum of a few
randomly-coincident blocks) is explicitly recorded as off the client's 2026-11-12 closed page, with
`skeleton.py closed` listing no neighbour. The design note's own candidate near-miss ("Outcomes are
hidden by the intervention itself" / "Controls were partly treated", for the own-schedule mix
correction, R3) is recorded as a supporting step whose omission alone leaves the call standing
(`no_own in effort.json` still calls Sequence). This matches the thread's `closed: none decides`
exactly; no conflict.

The thread flagged, on its own initiative, that the Final Recommendation's wording ("the pilot's
average managed night shows... because a random start still lets the few chargers... land
together") reads close to a surface-read-rejection pattern, then classified it `surface_read_
dependency: no` because the pilot's average-night figure is not a data defect or a misleading
reported number that is itself wrong, it is an honestly-computed statistic answering a different
question (an average) from the one the governing standard asks (a maximum / chance-of-exceedance).
This reconciles with the design note's "Not semantics" and "Not rule application" lines, which
make the same distinction (DPS-7 and EV-4 file *what* is compared, never *how* a transformer's
summer peak is estimated from hourly reads and sessions). I agree with the thread's classification:
this is method/model selection on honest data, not surface-read-rejection, but the memo's opening
sentence is worth the light rewording the thread itself proposed, purely so a future reviewer does
not misclassify the mechanism on a surface read of the prose alone.

## Stump power (Gate F)
Three independent, plausible shortcuts land on three distinct wrong figures, matching the design
note's "Not one thing" line and its Frontier check's shallow-path table exactly:
1. The pilot's own average-managed-night convention applied to the board decision files Stagger at
   0 transformers over and $23,600 (misses DPS-7's maximum/chance-of-exceedance convention).
2. The 2026 meters read as-is for "own schedules" files 28 over, missing that a quarter of today's
   chargers are already on Stagger (the metered record carries the mixed regime, not pure own
   schedule).
3. Quillpoint Sequence implemented literally one-at-a-time files 1 transformer over, missing the
   proposal's own "alongside whichever are charging" exception for a charger that cannot otherwise
   finish by its ready-by time.

Each is a distinct result (R4, R3, R5 respectively) with its own figure and its own fix; dropping
any one shortcut still leaves the other two as real, separately gradable work, which is the
level-5 shape the client's bar wants. The design note's own effort table (quick 1/9, careful but
hurried 3/9, thorough 9/9) is close to but somewhat below the thread's independent estimate
(quick ~1-2/9, careful ~4-6/9, thorough 9/9); the thread's careful-but-hurried range runs higher
than the note's 3/9, worth a note to the author (see Findings) but not disqualifying on its own,
since the thread's own range still separates clearly from the thorough column and from the quick
column, and the thread did not run the full simulation itself to pin an exact number.

## Findings, ranked
1. (Informational, not a defect) The thread's careful-but-hurried effort estimate (4-6 of 9) runs
   above the design note's table (3 of 9). Both agree the quick pass clears about a third or fewer
   and the thorough pass clears all nine, so the effort test as specified (H4) still passes; the
   author may want to recheck the careful-but-hurried column against `effort.py`'s own run if the
   platform's actual run-pair ever lands materially above the note's pair estimate of 40.5.
2. (Informational, not a defect) Neither the isolated thread nor this report independently re-ran
   the full 382-transformer night-by-night Monte Carlo for Stagger or the Sequence queueing
   simulation; this is a scope limit of a medium-effort determinism pass, not a finding against
   the task. The design note's own Frontier check records that the golden family of rivals (the
   monitored-peak lift, no lift, declared settings, two other seeds) all stays inside the stated
   bands and calls Sequence, which is the evidence this report relies on for Gate C on R3, R4 and
   R5.
3. (Cosmetic) The Final Recommendation's opening sentence reads, on a surface skim, like a
   reported-number-is-wrong flip; both the thread and this report classify the underlying
   mechanism as method/model selection on honest data (Gate G passes), but a one-sentence reword
   (stating plainly that DPS-7 is a maximum/probability standard and the pilot's average answers a
   different question) would remove the ambiguity for a future reviewer at no cost to determinism.

## Next action for the author
No determinism repair is required; disposition APPROVE. Optionally reword the Final
Recommendation's opening sentence (memo block, ask 1) so it reads as a method choice ("DPS-7's
limit is a maximum/probability standard; the pilot's average-night figure answers a different
question") rather than "the pilot's average... shows... [a misleading number]", purely to keep a
future reviewer from misreading the mechanism as a reported-number flip. This does not change any
figure, file, deliverable or gate, and needs no rerun.
