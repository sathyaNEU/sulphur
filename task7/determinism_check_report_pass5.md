# determinism-check report, task7, 2026-11-10 (pass 5)

Scope note: this is the single re-judge of pass 4's FIX_NOW finding (the author's repair: ask 7 and Critical
Component 4 now carry explicit bands, "about a tenth either way," and state the works-start convention, 13 July,
the Monday after the committee's 9 July meeting, in the answer blocks and the golden "round at close" sheet; two
small realism changes were made beside this, working-week received dates and distinct issuer PDF formatting). The
thread saw only a fresh unzip of `target.zip` and the extracted blocks from `submission.md`; it never opened
`DESIGN_NOTE.md` or `metadata.json`. Those two were read by this reviewer only after the thread returned, for the
Gate G/H reconciliation below, per the skill's ordering rule.

## Verdict
**DETERMINISTIC**

## Disposition
**APPROVE** — the pass-4 gap is closed. No repair needed, no model rerun required.

## Why
The one open question pass 4 flagged — what date the 2026 works start — is still not pinned by any shipped
document (`committee_request_2026-06-15.docx` fixes only the 9 July meeting date; `grant_offer_2026_terms.pdf`
fixes only the 30 September completion deadline), and it is still only fixed by analogy to the 2019 pilot. The
thread found this analogy genuinely admits a second reading (13 July, "first Monday after the deciding date," vs.
20 July, "one week after the deciding date, rounded to the next Monday," both licensed because the single 2019 data
point is degenerate: 8 July 2019 was itself a Monday). It computed both, plus 6 July and 10 July, converted each to
a working-day count to 30 September, and propagated the swing through the roofer-capacity model: the insulation
completion count lands at approximately 155 to 185 across all four candidate start dates, which sits entirely
inside the published 153 to 187 band. It separately tested the late-application sizing fork (post-12-June
applications sized by their 2019 grant-ratio growth, 27.83 per cent, versus their roof-area growth off the
cadastre, 23.9 per cent) and found the two operationalizations differ by only about 4 points of growth rate,
moving the projected "ask" total by roughly 3 per cent, again comfortably inside the stated roughly 10 per cent
band. Both of pass 4's named forks are now absorbed by the published bands rather than left as an unstated internal
tolerance. The fund/no-fund call (insulation and heating controls funded, heating optimisation not) and the
€8.2 million budget headroom survive every rival constructed, at either end of the bands.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Net applications received by 12 June | 829 | 829 (858 raw rows deduped on latest `received` per building) | Yes |
| Applications grant total | €4,959,800 | €4,959,800 | Yes |
| Applications lifetime tonnes (ins. / heat-opt / controls) | 26,847 / 4,354 / 11,621 | 26,847.99 / 4,353.97 / 11,620.99 (grant ÷ grant-per-tonne) | Yes (within rounding) |
| Same-calendar-day 2019 arrival fractions (ins. / heat-opt / controls) | 34.71% / 52.29% / 79.46% | 260/749=34.71%, 559/1069=52.29%, 971/1222=79.46% | Yes, exact |
| Applications projected at close (ins. / heat-opt / controls) | ~294 / ~692 / ~459 | 102/0.3471=293.9, 362/0.5229=692.5, 365/0.7946=459.3 | Yes |
| Pilot roofers / common 2026 roofers | 26 / 12 | 26 distinct 2019 insulation contractors (legal-form-normalized), 12 also quote in 2026 | Yes |
| Late-insulation-answer grant growth | 27.83% larger | €26,029.55 / €20,362.50 = 1.2783 | Yes, exact |
| Insulation roofs completed by 30 Sept, under 4 candidate works-start dates (6/10/13/20 July) | ~170 of 275 (band 153–187) | ~185 (6 Jul), ~173 (10 Jul), 170 (13 Jul), ~155 (20 Jul) | Yes, all 4 inside the published band |
| Late-application sizing, grant-ratio vs. roof-ratio fork | grant ratio used; "about a tenth either way" band | roof-area growth ratio 23.9% vs. grant growth 27.83%; moves the "ask" total ~3% | Yes, inside the ~10% band |
| Funded round paid total | €6,926,246 (band €6.2M–€7.6M) | holds under every rival tried, at either end of the works-start and sizing forks | Yes |
| Grant-per-tonne flip margins (ins. / controls) | flip at 20.34% / 7.44%; actual 22.46% / 8.64% | both ranges (€103.50–116.26, €94.38–112.70) stay fully on the funding side of €120; heating optimisation's range (€150.31–259.92) stays fully over | Yes |
| 2025/26 CO2 saved | 3,216 t | traced to the stated method; not independently rebuilt from the raw 27MB/25MB CSVs end to end (scope limitation, no contradiction found) | Yes (no contradiction) |
| Seven-season savings-by-season figures (asks 2–4) | as stated | traced to method, cross-checked against the applications ledger and grant-per-tonne arithmetic, which closed exactly; not independently rebuilt from raw CSVs | Yes (no contradiction) |

## Competing answers that survived
None, on any committed answer. The works-start-date fork (13 July vs. 6/10/20 July) and the late-application
sizing fork (grant ratio vs. roof-area ratio), the two forks pass 4 identified as open, are now both closed by the
published bands: every rival value the thread constructed for the insulation completion count, the paid totals,
and the applications-at-close totals lands inside the stated ranges in ask 7 and Critical Component 4, and the
fund/no-fund call and the budget headroom are unaffected at either extreme. No other fork found by this pass or by
pass 4 (the main recommendation, the three grant-per-tonne headline figures and their 90 per cent ranges in ask 6,
the applications ledger in ask 8, the 2025/26 saving in ask 9) admits a second defensible answer.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count / categories | ≥10 usable, ≥2 categories | 19 files; csv ×8, xlsx ×4, pdf ×6, docx ×1 = 4 categories | Pass |
| Large messy CSVs | ≥1 CSV ≥20,000 rows and ≥1 CSV 10–20 printed pages | `gas_meter_reads_2013_2026.csv` 389,106 rows; `electricity_load_profiles_2025.csv` 178,515 rows; `electricity_customers_annual_2019_2025.csv` 75,748; `benchmarking_notices_2019_2026.csv` 37,214; `meter_points_2026.csv` 28,565 all clear 20,000 | Pass |
| Distractors named outside the ZIP, unlabeled inside | ≥2 named in `metadata.json`, none labeled in-ZIP | 3 named (`electricity_customers_annual_2019_2025.csv`, `municipal_heat_plan_2026_summary.pdf`, `federal_funding_overview_2025.pdf`); none carry a distractor marker in-file | Pass |
| Distractors unused but relevant | relevant, not load-bearing | all 3 read as plausible adjacent municipal-utility documents (electricity annual totals, municipal heat plan, federal grants overview); none feeds a graded figure; `solar_cadastre_rooftops_2024.xlsx` and `electricity_load_profiles_2025.csv` are load-bearing (R3, R4), not distractors, correctly excluded from the list | Pass |
| 1–3 deliverables, format matches prompt | note + workbook | `grant_round_2026_note.docx`, `grant_round_2026_appraisal.xlsx` in `golden.zip`; matches "a short note... and a workbook" | Pass |
| Multi-dimensional asks, unit + rounding in the asking sentence | required | asks are multi-dimensional (season-by-season, per-measure, per-application); the prompt itself states no rounding convention, left to the author per the design note's closure table row 10; not a determinism defect | Pass (minor prompt-level note, unchanged from pass 4) |
| Answer shape, 4+ checkable results | one of 14 shapes | an allocation (which measures are funded) with its sensitivity (90% ranges, flip rates) and a capacity-constrained payment forecast; 9 graded items (recommendation + 4 critical components + asks 2–9 collapsed by sub-ask), well over 4 | Pass |
| Golden ZIP holds exactly the requested files | yes | 2 files, matching the 2 requested deliverables | Pass |
| Realism / no LLM tells | yes | thread's hygiene pass found no synthetic/benchmark/placeholder language; one minor note (`applications_2026.xlsx`'s `received` column still carries some Saturday/Sunday dates despite the stated working-week realism change) — hygiene note only, not a determinism defect | Pass |

## Gate G reconciliation
Judge thread: `mechanism: method_or_model_selection`, `stumping_family: analytical_non_defect`,
`surface_read_dependency: no`, `sole_data_defect: no`. The design note's own self-classification agrees: "Not rule
application: no filed procedure performs a result... how the round is projected and how much of its work the firms
can do by 30 September are left to the analysis," and "No decoy... no replay." No disagreement between the thread
and the design note; the task is not a banned surface-read-rejection shape, with or without the ask 7 band repair.

## Gate H reconciliation
Design note vs. judge thread, read side by side:

- **Mechanism / one_thing.** Design note: "Not one thing: the call needs two unrelated judgments" (each
  application's own building characteristic, and the roofers' capacity by 30 September), one-fact rescue of 5 of 15
  internal nodes (≈33%). Judge thread: `one_thing: none`, one-fact rescue "price each application on the empty-week
  / roof-per-floor mechanism... carried over each measure's service life" rescuing ≈3 of 9 graded items (also at the
  ceiling, same granularity difference as pass 4). The two independent counts again land at essentially the same
  place (~a third); nothing about the ask 7 band repair changed this agreement.
- **Hidden factor record.** Unchanged from pass 4: every factor in the design note's table (the empty-week saving
  curve, the roof-per-floor curve, owners' self-selection, the hotels/care-homes lived-in-round-the-clock step, the
  roofer pace model) is marked "constructed, not only in deciding units, found by modelling," with a "keep" verdict;
  none is the shallow_hidden_factor shape. The thread's independent reconstruction of the roofer-pace/queue model
  for this pass's special focus required the same multi-step measurement-and-fit work the design note describes
  (matching contractor names across two files, computing each firm's 2019 pace, converting candidate start dates to
  working-day counts, propagating through to a paid total), not a one-line fix. Agreement.
- **Effort grades.** Design note's internal table (15 chain nodes): quick 1/15 (~7%), careful-but-hurried 7/15
  (~47%), thorough 15/15. Judge thread (9 graded submission items): quick 2/9 (~22%), careful 5–6/9 (~61%), thorough
  9/9. Same counting-granularity gap noted at pass 4 (the thread folds several multi-part asks into single graded
  items); both satisfy "quick ≤ about a third" with clear separation between passes.
- **The localized gap itself.** Both the design note's own closure table (SF23 "when the 2026 works start," SF25
  "the late applications' firms," SF26 "one queue or each firm's own," SF27 "the late roofs' size," all closed by
  "asserted" against an internal band rather than a filed sentence) and the thread's independent, blind
  recomputation converge on the same result (ask 7 / Critical Component 4) as the place where a defensible rival
  convention could move the figure — and both now agree that the published band (not a bare point, as it was at
  pass 4) absorbs every rival either source could construct. The repair closes exactly the fork both sources had
  independently flagged, without loosening the band enough to stop grading (the thread confirmed the band still
  separates the correct ~170-paid figure from a hurried run's ~275-paid or ~229-paid alternatives by a wide margin).

`domain: pass`; `layers: pass` (Layer 1: meter-index resets and rollovers, estimates/corrections, revised
applications, address-string variants, multi-year calorific/degree-day drift, second market locations, a mid-2025
meter exchange, the working-week received-date pattern and distinct issuer PDF formatting added since pass 4;
Layer 2: saving-rate curve fits against empty-week and roof-per-floor, bootstrapped grant-per-tonne ranges, a
capacity-constrained payment forecast now carrying an explicit convention-robustness band); `results: 9 graded
across 5+ areas` (causal reasoning, forecasting, missingness-measurement, modeling, synthesis, uncertainty);
`one_thing: none` (one-fact rescue tops out at ≈33%, matching both the design note and the thread); `effort: quick
2 of 9 (~22%), careful 5-6 of 9 (~61%), thorough 9 of 9`; `one_fact: "price each 2026 application at the
pilot-calibrated saving along its own building's driver (empty week for controls, roof-per-floor for insulation),
not its own use's average, carried over the measure's service life" rescues ~3 of 9`. The weight of the work sits
in the pricing (mechanism fitting + lifetime carry-forward) and in the capacity/budget projection tested this pass;
a careful-but-hurried strong run is likeliest to lose Critical Component 4 / ask 7 by paying every granted job in
full (landing near €10.76M rather than €6.93M paid) or by ignoring roofer throughput altogether, not by picking a
defensible-but-different works-start date or queue convention, both of which the published band now absorbs.

## Stump power (Gate F)
Unchanged in substance from pass 4, confirmed again this pass: the chain (benchmarking/normalisation, pilot
drawn-vs-passed-over comparison, life-carry, own-saving pricing by building characteristic, 90%-range/flip-point,
budget-constrained round projection, the 2025/26 annual figure) is a genuine multi-result chain. A hurried run that
reuses the pilot's flat seven-season average, or prices applications at their own use's saving instead of the
pilot-calibrated building-characteristic saving, or pays every granted job in full instead of modelling roofer
throughput, loses several results for real, separable analytical reasons. The one place stump power cut the wrong
way at pass 4 — a sound run penalized for a defensible-but-different works-start or queue convention on ask 7 /
Critical Component 4 — is now fixed: the thread confirmed the published band absorbs every rival convention it
could construct while still separating the correct figure from the hurried alternatives (~275 paid in full, or
~229 with the roofers' work counted in jobs) by a wide margin. Everything in the chain now stumps for the reason it
is supposed to, with no open convention-robustness risk remaining.

## Findings, ranked
1. **No open finding on determinism.** Pass 4's one localized gap (ask 7 / Critical Component 4 stated as a bare
   point while a defensible rival convention could land outside it) is closed: the published band now absorbs every
   rival the thread independently constructed (4 works-start dates, 2 late-application sizing conventions), and the
   fund/no-fund call and budget headroom hold at either end.
2. **Minor hygiene note, not a determinism defect.** `applications_2026.xlsx`'s `received` column still contains
   60 Saturday and 41 Sunday dates out of 858 rows despite the stated "working-week" realism change; this does not
   move any committed figure and may simply mean the change lives in a different field or file than the one
   checked, or is not yet fully applied to this column. Worth the author's attention before the next ship, but not
   a reason to withhold APPROVE.
3. **Minor, prompt-level, carried over from pass 4.** The prompt states no rounding convention; the design note's
   closure table records this as a deliberate author call left to `submission.md`, consistent with house style.

## Next action for the author
None required for determinism. Optionally confirm the working-week realism change is fully applied to
`applications_2026.xlsx`'s `received` column (currently 101 of 858 rows still fall on a Saturday or Sunday) before
the next ship; this is a hygiene polish item, not a gate failure, and does not block APPROVE.
