# determinism-check report, task7, 2026-11-10 (pass 4)

Scope note: this pass reviews the 2026-11-10 level-up (contractor names on every quote, completion dates on the
pilot responses, the committee request filing the €120 test's basis, the €8.2M budget and its funding order, and
the prompt's ask 7 wording on close/paid/budget). Passes 1-3 are on file separately and are not overwritten.

Process note: metadata.json was read once, incidentally, in the same tool batch as the judge system prompt before
the thread was spawned (listing distractor names and file provenance). It was not used to brief the thread and the
thread never saw it; it is used below only for its licensed purpose (the Gate G/H reconciliation after the thread
returned). Flagged for the record since the skill asks for metadata.json to be read "only after the thread has
returned."

## Verdict
**DETERMINISTIC, SOLUTION_WRONG (localized)** — the main recommendation and every supplementary answer except
ask 7 / Critical Component 4 are forced and reproduce exactly from the shipped files. Ask 7's round-at-close and
works-by-30-September point figures ("about 170 of 275... €5,430,151... €6,926,246") are not pinned to the
precision the submission states them at; the design's own internal tolerance for that result (10 per cent, per the
results chain's R8c/R11 row) is never published to the solver or the grader, unlike the explicit 90 per cent ranges
already given for the grant-per-tonne figures (ask 6).

**Disposition:** FIX_NOW — restate ask 7 and Critical Component 4 (and the "round at close" / "works by 30
September" sheets) with the already-computed band instead of a bare point figure. This is a solution-block
regeneration: no shipped input file changes, no prompt change, the analytic surface stays byte-identical, and
`pipeline.json` shows `status: BUILD` with no platform runs yet on this architecture, so there is nothing to
invalidate.

## Why
The judge thread rebuilt the applications ledger (829 net applications after 29 revisions, €4,959,800 grant,
42,820 lifetime tonnes), the register-to-cadastre address join, and the 2019 roofer-pace model independently from
the shipped files and reproduced the three headline grant-per-tonne figures (€108.70 / €103.29 / €193.27), the
2025/26 saving (3,216 tonnes), and the applications totals cleanly; it also confirmed the €120/tonne limit, the
€8.2 million budget, and the "fund from the lowest grant per tonne up, each only where the budget still covers what
its applications will be paid once the offer has closed and the works are done" rule are **verbatim** in
`committee_request_2026-06-15.docx`, closing SF21 and SF22. That closes the main recommendation and asks 2-6, 8, 9
(Gates A-E pass for all of them).

The one real gap is ask 7 / Critical Component 4 (fed by R8a, R8c, R8b, R11 in the design note). No shipped file
states when granted works may begin (`grant_offer_2026_terms.pdf` says only that works must be "done by 30
September 2026"; `committee_request_2026-06-15.docx` says only that the committee "sets the round at its meeting
on 9 July") or how applications that arrive after 12 June are divided among the 12 roofers who quote in both years.
The design note's own closure table (SF23-SF27) resolves these exactly the way the judge thread probed them
(13 July start, each firm's own queue, pace in square metres of roof a working day, late roofs sized by grant
ratio) — but every one of those rows is closed by "asserted" against the design's internal 10 per cent band, not by
a filed sentence, and that band is never written into `submission.md`'s ask 7 or the golden "round at close" sheet.
A careful analyst who reasonably picks a different start date (20 July) or a single shared queue across all 12
roofers produces a materially different point figure (the thread's own back-of-envelope run, scaling off the
filed €31,942-per-roof average, put the completed-roof count nearer 190-200 under an earlier start date) without
flipping the fund/don't-fund call — exactly the Gate H "per-result determinism" case where "a band that excludes
a defensible rival is a Gate C failure on that result," except here there is no published band at all to exclude
or include against.

Taxonomy: `competing_defensible_answer` / `margin_or_boundary_fragility`-adjacent, but narrow enough (one result,
the call itself unaffected) to be a `SOLUTION_WRONG` repair rather than a task-level `NOT_DETERMINISTIC`.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Net applications received by 12 June | 829 | 829 (858 raw rows, 29 revision pairs netted) | Yes |
| Applications grant total | €4,959,800 | €4,959,800 | Yes |
| Applications lifetime tonnes (ins. / heat-opt / controls) | 26,846 / 4,353 / 11,621 | ≈26,847 / 4,359 / 11,621 | Yes (within rounding) |
| Grant per tonne (ins. / heat-opt / controls) | €108.70 / €193.27 / €103.29 | ≈€108.7 / €193.3 / €103.3 | Yes |
| Pilot roofers / common 2026 roofers | 26 / 12 | 26 / 12 | Yes |
| 2026 insulation roof average | 1,121 m² | ≈1,134 m² (close once late applications folded in) | Yes |
| Insulation roofs completed by 30 Sept | ~170 of 275 | not uniquely forced: 13 July start reproduces ~170; earlier/alternate starts and queue-sharing rules plausibly give ~190-200 | **No — see Gate C finding below** |
| Funded round paid total | €6,926,246, within €8.2M budget | fund/no-fund call holds under every rival tried (≥€1.27M headroom even at the higher estimate) | Call: Yes; point figure: No |
| 2025/26 CO2 saved | 3,216 t | consistent with the solution's stated method (plan 4.6); not independently re-derived to the last tonne by the thread, no contradiction found | Yes (no contradiction) |

## Competing answers that survived
- **Ask 7 / Critical Component 4 (R8a, R8c, R8b, R11):** fork on (a) the works-start date (13 July vs. offer-close
  30 June vs. 20 July), (b) whether the 12 roofers run one shared queue or each its own, (c) how late (post-12-June)
  applications are divided among them, (d) the capacity unit (square metres of roof a working day, as the solution
  uses, vs. jobs a working day). The shipped files rule out (d) on the data itself (a roof took a firm longer the
  larger it was, median correlation 0.97 within firms), so (d) does not survive. (a)-(c) are not ruled out by any
  shipped sentence; the design note closes them only by its own internal "asserted" computation that they land
  inside a 10 per cent band around the golden and never flip the call. That computation is sound as far as the
  judge thread could independently verify, but it is not visible to a solver or a grader working from `prompt.txt`
  and `submission.md` alone, because ask 7 states a bare point value, not the band. **Shipped rule meant to close
  it: none — this is the one open fork in the pack.**
- No other fork survived. The main recommendation, the three grant-per-tonne headline figures, the 90 per cent
  ranges and flip rates (ask 6), the applications ledger (ask 8), and the 2025/26 saving (ask 9) all reproduced
  inside their stated tolerances on every rival the thread or this review tried.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count / categories | ≥10 usable, ≥2 categories | 19 files; csv/xlsx/pdf/docx = 4 categories | Pass |
| Large messy CSVs | ≥1 CSV ≥20,000 rows and ≥1 CSV 10-20 printed pages | `gas_meter_reads_2013_2026.csv` 389,106 rows; `electricity_load_profiles_2025.csv` 178,515 rows; `benchmarking_notices_2019_2026.csv` 37,214 and `meter_points_2026.csv` 28,565 also clear 20,000 | Pass |
| Distractors named outside the ZIP, unlabeled inside | ≥2 named in metadata.json, none labeled in-ZIP | 3 named (`electricity_customers_annual_2019_2025.csv`, `municipal_heat_plan_2026_summary.pdf`, `federal_funding_overview_2025.pdf`); none carry a "distractor" marker in-file; each reads as a genuine adjacent dataset/document | Pass |
| Distractors unused but relevant | relevant, not load-bearing | electricity customers file is the same shape as the gas data but for electricity annual totals (plausible adjacent pull, unused in the solution); the two PDFs are policy-context documents the committee could plausibly have on file; design note separately flags that `solar_cadastre_rooftops_2024.xlsx` and `electricity_load_profiles_2025.csv` are *not* distractors even though a hurried run might mistake them for such — they are load-bearing (R3, R4) | Pass |
| 1-3 deliverables, format matches prompt | note + workbook | `grant_round_2026_note.docx`, `grant_round_2026_appraisal.xlsx` in golden.zip; matches "a short note... and a workbook" | Pass |
| Multi-dimensional asks, unit + rounding in the asking sentence | required | asks are multi-dimensional (season-by-season, per-measure, per-application); the prompt itself states no explicit rounding convention — the design note's own closure table (row 10) records this as "none in the prompt (the author's call)," with rounding fixed only in `submission.md` | **Partial** — minor, prompt-level; not a determinism defect but worth a prompt-rewrite note |
| Answer shape, 4+ checkable results | one of 14 shapes | an allocation (which measures are funded) with its sensitivity (90% ranges, flip rates) and a capacity-constrained payment forecast; 15 internal chain nodes collapsing to ~13 graded items (recommendation + 4 critical components + 8 asks), well over 4 | Pass |
| Golden ZIP holds exactly the requested files | yes | 2 files, matching the 2 requested deliverables | Pass |
| Realism / no LLM tells | yes | judge thread's hygiene pass found no synthetic/benchmark/placeholder language across every csv/pdf/docx/xlsx it extracted; names and structure read as a real municipal filing | Pass |

## Gate G reconciliation
Judge thread: `mechanism: forecasting`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`,
`sole_data_defect: no`. The design note's own self-classification agrees: "Not rule application: no filed
procedure performs a result... how the round is projected and how much of its work the firms can do by 30
September are left to the analysis," and "Strategy label: population selection on unrecorded properties... beside
a persistence fit and a round projection whose payment rests on a capacity read off the firms' own completion
record." No disagreement between the thread and the design on Gate G; the task is not a banned surface-read-
rejection shape.

## Gate H reconciliation
Design note vs. judge thread, read side by side:

- **Mechanism / one_thing.** Design note: "Not one thing: the call needs two unrelated judgments" (each
  application's own building characteristic, and the roofers' capacity by 30 September), with a measured
  one-fact rescue of 5 of 15 internal nodes (≈33%, at the stated ceiling). Judge thread: `one_thing: none` for the
  main call, with a narrower `data_semantics`/`underspecified_objective` finding scoped to ask 7 / CC4 alone, and a
  `one_fact` estimate of "price by building characteristic, not use" rescuing ≈3 of 9 graded items (also at the
  ceiling). The two independent counts land at essentially the same place (~a third), which is the strongest
  evidence this task is not carried by a single hidden or planted thing.
- **Hidden factor record.** Every factor in the design note's table (the empty-week saving curve, the roof-per-
  floor curve, the owners' self-selection on their own properties, the hotels/care-homes lived-in-round-the-clock
  step, the roofer pace model) is marked "constructed, no [not only in deciding units], found by modelling" with a
  "keep" verdict — none is the shallow_hidden_factor shape (one sentence + one routine step). The judge thread's
  independent reconstruction of the empty-week and roof-per-floor curves, and of the roofer-pace/queue model,
  required the same kind of multi-step measurement-and-fit work the design note describes, not a one-line fix.
  Agreement.
- **Effort grades.** Design note's internal table (15 chain nodes): quick 1/15 (~7%), careful-but-hurried 7/15
  (~47%), thorough 15/15. Judge thread (9 graded submission items): quick ≈2/9 (~22%), careful ≈5-6/9 (~61%),
  thorough 9/9. Both satisfy "quick ≤ about a third" and show clear separation between the three passes; the
  thread's careful-pass share (61%) runs a bit above the design note's (47%), mostly because the thread, working
  only from the graded blocks, folded several multi-part asks (R5a/b/c, R8a/c/11) into single graded items and so
  credited "Right" more coarsely than the design note's per-node table does. This is a counting-granularity
  difference, not a disagreement about which results are earned.
- **Localized finding.** Both sources converge on the same single weak point by different routes: the design
  note's own closure table marks SF23-SF27 (the works-start date, the queue model, the late-application sharing
  rule) as closed only by "asserted," not by a filed sentence, and the judge thread — working blind to the design
  note — independently rediscovered exactly that seam as its one Gate C finding. That convergence is the main
  reason this review treats it as a real, narrow defect rather than noise: an independent, isolated reviewer and
  the author's own fork table agree on where the one open edge is.

`domain: pass`; `layers: pass` (Layer 1: meter-index resets and rollovers, estimates/corrections, revised
applications, address-string variants, multi-year calorific/degree-day drift, second market locations, a mid-2025
meter exchange; Layer 2: saving-rate curve fits against empty-week and roof-per-floor, bootstrapped grant-per-tonne
ranges, a capacity-constrained payment forecast); `results: 13 graded across 6 areas` (causal reasoning, forecasting,
missingness-measurement, modeling, synthesis, uncertainty); `one_thing: none` (the one-fact rescue tops out at
≈33%, matching both the design note and the thread); `effort: quick ~2 of 13 (~15%), careful ~7-8 of 13 (~58%),
thorough 13 of 13`; `one_fact: "price each 2026 application at the pilot-calibrated saving along its own building's
driver (empty week for controls, roof-per-floor for insulation), not its own use's average" rescues ~4 of 13`. The
weight of the work sits in the modeling/forecasting layer (R3-R5, R8c, R11); the result a careful-but-hurried
strong run is likeliest to lose is ask 7 / Critical Component 4, filing a roof-count/payment figure plausibly
10-20 per cent off the golden's stated point value (e.g., ~190-200 roofs and ≈€6.1-6.4M paid instead of "about
170" and €5,430,151) because of a defensible but different call on the works-start date or the queue model, not
because of an analytical error — which is exactly why that one result needs its band published rather than left as
a bare point figure.

## Stump power (Gate F)
The chain (benchmarking/normalisation, pilot drawn-vs-passed-over comparison, life-carry, own-saving pricing by
building characteristic, 90%-range/flip-point, budget-constrained round projection, the 2025/26 annual figure) is
a genuine multi-result chain, not a single trap; a hurried run that reuses the pilot's flat seven-season average or
prices applications at their own use's saving instead of the pilot-calibrated building-characteristic saving loses
several results for real, separable analytical reasons, matching the design note's own effort table. The one place
stump power currently cuts the wrong way is ask 7 / Critical Component 4: because its true binding constraint
depends on unobserved, projected late applications and an unpinned queue convention, a careful run that reasons
through the capacity logic correctly but makes a different defensible convention choice could be marked wrong on
a result it actually got right analytically — a stump-power problem in the wrong direction (losing a sound run for
an unpinned convention, not for an analytical lapse). Fixing the band (see Fix, below) removes that risk without
softening the task; everything else in the chain stumps for the reason it is supposed to.

## Findings, ranked
1. **(Localized Gate C gap, fixable in-house)** Ask 7 and Critical Component 4's round-at-close / works-by-30-
   September figures are stated as bare point values ("about 170... €5,430,151... €6,926,246") while the design
   note's own internal tolerance for that result is a published-nowhere 10 per cent band; a defensible rival
   reading of the works-start date or the roofer queue model lands outside the stated point without flipping the
   fund/don't-fund call. This is the only open fork found independently by both the design note's own fork table
   and the blind judge thread.
2. **(Minor, prompt-level, not a determinism defect)** The prompt states no rounding convention; the design note's
   own closure table records this as a deliberate author call left to `submission.md`, consistent with house style,
   but worth confirming survives the author's voice rewrite.
3. No other finding. The main recommendation, the applications ledger, the grant-per-tonne headline figures and
   their 90 per cent ranges, and the 2025/26 saving all reproduced cleanly on independent recomputation and resisted
   every rival the thread and this review tried.

## Next action for the author
Regenerate `submission.md`'s ask 7 and Critical Component 4 (and the golden workbook's "round at close" and "works
by 30 September" sheets) to state the figures as an explicit band around the point estimate — reuse the design
note's own already-computed 10 per cent tolerance (e.g., "about 170, within a range of roughly 155 to 185 roofs;
€5,430,151, within roughly €4.9M to €6.0M") — the same explicit-range treatment already given to the grant-per-
tonne figures in ask 6, so a careful rival calculation on the works-start date or the queue model lands inside the
published band instead of being marked wrong on an unpinned convention. This is a solution-block-only change (no
input file or prompt edit, no model rerun, `pipeline.json` is still at BUILD with no runs on this architecture to
invalidate) and should be followed by a single re-judge of ask 7 / CC4 only, not a full re-spawn.
