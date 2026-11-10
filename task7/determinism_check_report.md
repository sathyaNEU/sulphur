# determinism-check report, task7, 2026-11-09

Pass: author's `/build` stage 4, after the prior SEND_BACK repair on the hotel/care-home "lived-in" rule
(architecture 8, controls priced at 103.79 euro/tonne). One isolated judge thread, fresh unzip of
`target.zip` at `/tmp/determinism-check-task7-1794274893/target/`, extracted blocks inlined, no access to
`submission.md`, `DESIGN_NOTE.md`, `generator/`, `pipeline.json`, `metadata.json`, `runs/`, `golden/`,
`golden.zip`, `guidelines/`, any `determinism_check_report*.md`, or any other task folder.

## Verdict
**NOT_DETERMINISTIC**
**Disposition:** SEND_BACK
**Stumping type:** mechanism: shallow_hidden_factor (bordering single_conceptual_flip); stumping_family:
surface_read_rejection; surface_read_dependency: yes; sole_data_defect: no

## Why
The judge thread's Gate C finding: no shipped file (`pilot_2019_rules.pdf`, `benchmarking_method_2022.pdf`,
`grant_offer_2026_terms.pdf`, `committee_request_2026-06-15.docx`) states that hotels and care homes must be
read as occupied round the clock rather than by their electricity load shape. Grepped all documents for
occupancy/24-hour/overnight/guest/resident language; nothing found. Applying the general rule the golden
states for every other building (empty = never falls below three-quarters of peak) literally and uniformly
to hotels/care homes as well gives essentially 0% exempted by load alone, and two of the golden's own
disclosed alternate readings land on the other side of the 120 euro/tonne limit: a straight line through
the lived-in band (still keeping the override) prices controls at 120.02, and reading hotels/care homes by
load alone (no override at all) prices them at 159.57 (both figures the golden's own Step 4 text concedes).
This affects the **main recommendation**, **Critical Component 2**, and **Supplementary Answers 6, 7 and
8**, all of which carry heating controls at 103.79 funded.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Controls applications' reference-consumption-weighted empty-week share (golden, use-type override) | 68.15% | 68.14% | yes |
| Hotels/care homes' raw load-emptiness read (no override) | "two thirds empty" (text) | median ≈ 67-69% empty, min/max ratio ≈ 0.50 | yes |
| Hotels/care homes qualifying as round-the-clock by literal 3/4-of-peak load rule, no use-type override | implicitly none asserted | 0.0% at the stated threshold (0.1% at 70%, ~5-6% at 60%) | yes, confirms the override is not an application of the stated rule but a separate carve-out |
| Controls grant/tonne, golden reading (use-type override, threshold+rise fit) | 103.79 | 103.79 (own reconstruction) | yes |
| Controls grant/tonne, straight line through lived-in band (SF18, override kept) | 120.02 (disclosed in Step 4) | consistent | yes |
| Controls grant/tonne, load-shape literal, no override at all (SF17, "nobody") | 159.57 (disclosed in Step 4) | consistent | yes |

## Competing answers that survived
**SF17 (who is lived in round the clock):** the golden's reading is "every hotel and care home, by its use
on the register, full stop." The design note's own fork table (`SF17`) lists three rivals: (a) a weekend
day-vs-night ratio test at 0-15% margins, (b) a strict "every weekend day hour above every night hour" test
(gives 114.97, still funded), (c) "nobody, read off its load alone" (gives 159.57, not funded). Readings (a)
and (b) land inside the golden's own stated band (still FUND); only (c) flips the call. The thread treated
(c) as a surviving defensible rival because no filed document states the occupancy convention; the design
note rules (c) out only by appeal to the pilot's own observed outcome (hotels/care homes measured only 1.46%
saving despite reading ~65-70% empty by load) and calls that closure "asserted," not "filed." Whether that
pilot-outcome argument is itself a forcing fact (a diligent analyst doing residual diagnostics would catch
the misfit) or an unpinned authorial judgment is exactly the Gate C question the thread answered against
the task.

**SF18 (the form of controls' rise), a materially thinner margin:** keeping the lived-in override but fitting
one straight line through all bands (including the lived-in band) instead of a threshold-and-rise fit
through the non-lived bands only gives 120.02 euro/tonne — 0.02 over the 120 limit, i.e. inside rounding
noise. This is a narrower, cleaner knife-edge than SF17: the golden's own stated 90% range for controls is
94.63 to 112.94, which does **not** contain 120.02 (nor 159.57). A result whose band excludes a defensible
rival the thread (and the design note's own checks.py) actually ran is a Gate C failure on that result in
its own right, independent of how SF17 is eventually resolved.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count/categories | 10+ usable files, 2+ categories | 19 files (8 csv, 6 pdf, 4 xlsx, 1 docx); 4 categories | Pass |
| Large/messy CSVs | 1 of 20k+ rows, 1 of 10-20 printed pages | `gas_meter_reads_2013_2026.csv` 389,105 rows; `electricity_load_profiles_2025.csv` 178,514 rows | Pass |
| Distractors declared outside ZIP, unlabelled inside | 2+ named in metadata.json | 3 named (`electricity_customers_annual_2019_2025.csv`, `municipal_heat_plan_2026_summary.pdf`, `federal_funding_overview_2025.pdf`); none labelled inside target/ | Pass |
| Deliverables 1-3, all in golden | match prompt's "a note and a workbook" | golden.zip holds exactly `grant_round_2026_note.docx` + `grant_round_2026_appraisal.xlsx`, matching metadata's `deliverables` | Pass |
| Answer shape | one of the 14 client shapes | scenarios with the flip point (grant/tonne vs 120 limit, with range and flip rate) | Pass |
| Golden ZIP = exactly requested files | match | 2 files, both requested formats | Pass |

## Gate G reconciliation
Design note `## Deep reasoning` argues "Not one thing": the two measured drivers (R3, R4) each still need
their own measurement/fit/pricing/fade chain, so no single catch carries the whole score. But the same
section concedes (verbatim) that "controls also need the lived-in step... read off its load alone it looks
two thirds empty, and controls then come to 159.57 euro a tonne and fail" — i.e. the note itself treats the
lived-in override as a third, separately decisive ingredient for controls specifically, beyond the two
drivers. The note's own `## Hidden factor record` row for this factor gives its "Fix depth" as
**"measurement: every hotel and care home held lived in round the clock (its use on the register)"** — a
one-line lookup against the registry's use column, not a modelling step — which matches the thread's
`shallow_hidden_factor` classification on its face, even though the note's verdict column marks it "keep:
the measurement's own step, decisive for controls" rather than flagging it as shallow.

The sharpest divergence is Gate H5. The note's `## Effort test` names the "largest single hint" as the
two-drivers sentence and states it "rescues 2 of 13 results," separately asserting "the lived-in sentence
alone rescues nothing for a pass that never opened the profiles." The thread, working only from the shipped
files with no access to that framing, constructed a different single sentence ("hotels and care homes run
round the clock, so don't read their empty-week share off the electricity load; treat them as never-empty")
and estimated it rescues roughly 5-6 of 14 graded results (main recommendation, Critical Component 2,
Supplementary Answers 6, 7, 8, and partially 4) — over the one-third H5 bar, and a materially larger rescue
than the note's own 2-of-13 figure for its chosen hint. This is the strongest single Gate H finding from
this pass: the note tested one framing of the one-fact question and cleared it; the thread tested an
adjacent, equally natural framing of the same fact and failed it, and the two use different candidate
sentences rather than one agreeing then disagreeing.

## Stump power (Gate F)
Independent of the determinism defect, the design is comfortably difficult: a careful-but-hurried run that
measures both drivers correctly (the two hardest, genuinely analytical steps) still files controls wrong
unless it also separately diagnoses the hotels/care-homes misfit. The thread agrees this layer is "genuinely
hard, non-obvious" analytically. The problem the thread raises is not that the task is too easy, but that
the "right" answer to the hard layer is not forced by any filed convention, and the golden's own text
discloses that a reasonable alternative construction of the same mechanism lands outside the golden's own
stated 90% range on two different forks (SF17 and, more tightly, SF18).

## Findings, ranked
1. **Gate C fails on the main recommendation, Critical Component 2, and Supplementary Answers 6-8**: the
   golden's 90% range for controls (94.63-112.94) does not contain either disclosed rival reading (120.02 or
   159.57), and the closure for both forks (SF17, SF18) is recorded in the design note's own fork table as
   "asserted," not "filed."
2. **SF18 is the tighter, cleaner target**: 120.02 against a limit of 120 is a margin inside rounding noise,
   independent of whether SF17's use-type override is eventually accepted as forced.
3. **Gate H5 tension**: the note's own one-fact test (2 of 13) and the thread's independently constructed
   one-fact test (5-6 of 14) disagree on whether this mechanism is a surface stump; the thread's framing
   clears the one-third bar.
4. Hygiene, file count, format mix, distractor declaration, and deliverable match all pass cleanly; this is
   not a hygiene-driven send-back.

## Next action for the author
Close SF17/SF18 with a filed convention rather than an authorial assertion: add a line to
`benchmarking_method_2022.pdf` or a column in `buildings_register_2026.xlsx` that states which use types get
an occupancy override and why (e.g., tying it to the register's own hot-water-share convention for hotels
and care homes, which the file already carries), and re-verify that every disclosed rival reading (not just
the golden's own fit) now lands inside the golden's stated 90% range before re-judging. A model rerun is
required after the fix.
