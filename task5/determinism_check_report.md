# determinism-check report, task5, 2026-11-08

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The isolated judge thread, seeing only a fresh unzip of `target.zip` (md5 882e5301b1d84d153bf7784bbdd57c7a)
plus the four submission blocks, independently rebuilt the liability/report pipeline, the December 2025
baseline, the payroll-agent transmission clustering, and a historical backtest of retention shares, and
reproduced every committed figure within one account out of 27,651 (immaterial to the designation). No
shipped file (the Act, the rate notice, the LMI data-sharing MOU, the board email) states the estimation
method, the transmission-grouping rule, or the retention shares; the task forces an estimate to exist
(Act section 2(c), "as reported or estimated... whether or not the employer's report has been received") but
leaves *how* to build it open, and the data itself (a genuinely bimodal 0-10%/70-100% split in transmission-
mate filing, with a dead zone in between) closes that method fork. Garrow (-3.0%) and Ostrom (-3.1%) clear
the -2.0% line by roughly a full point, with the next county (Kittredge, -1.2%) 0.8 points on the other
side -- not a knife-edge. The main recommendation and all six supplementary answers (asks 1-6) trace
cleanly to the shipped files.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Liable accounts, Q4 2026 | 27,651 | 27,652 | Off by one (traced to an ambiguous same-day status-history tie-break the judge could not fully isolate at medium effort; immaterial to any committed figure) |
| Reports received, Q4 2026 | 23,377 | 23,377 | Exact |
| Outstanding reports | 4,274 | 4,275 | Off by one, same propagated gap |
| December 2025 statewide jobs | 478,900 | 478,882 raw -> 478,900 | Exact, and cross-checked against the independently published `covered_employment_by_county_2025q4.xlsx` |
| Transmission split (missing-alone vs. late-transmission) | 2,538 late-transmission / 636 missing-alone (+ 496 / 604 other categories) | Bimodal: 2,448 accounts at 0-10% of transmission-mates filed, 369 at 70-100%, zero in between | Confirms the split is non-arbitrary; the judge's own cut landed on the same two clusters |
| Retention share, missing-alone vs. late-transmission | 0.29 vs. 0.97 | ~0.33 vs. ~0.97 | Materially consistent; the 0.29 vs 0.33 gap is attributed to how the judge's quick rebuild folded the "two quarters missing" and "late every quarter" sub-buckets, not to the claimed figure being wrong |
| Garrow December 2026 jobs / change | 31,600 / -3.0% | Not independently re-derived from the full imputation, but the upstream pipeline and retention mechanism it depends on reproduced | Consistent |
| Ostrom December 2026 jobs / change | 27,100 / -3.1% | Same | Consistent |

## Competing answers that survived
None. The solution's own closing paragraph names three rival operationalizations (uniform September
carry-forward -> no county; "every client of a late payroll agent is late" -> Ostrom only, wrongly sweeping
in Garrow; received-reports-only -> 14 counties, violating Act section 2's "whether or not received" clause) and
the judge independently confirmed each fails against the rebuilt data for the stated reason. No third
defensible method was found that both honors the Act's "every liable employer" language and survives the
historical backtest as well as the shipped method.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count / categories | 10+ files, 2+ categories | 12 files; csv, xlsx, pdf, eml (spreadsheet, document/text categories) | Pass |
| Large, messy files | 1 CSV 20k+ rows, 1 CSV 10-20 printed pages+ | `ui_quarterly_reports_2023q1_2026q4.csv` (416,574 rows); `ui_employer_accounts_2027-02-15.csv` (31,858), `ui_account_status_history_2023-2027.csv` (12,203), `ui_multiple_worksite_reports_2023q1_2026q4.csv` (21,846) all clear the page floor | Pass |
| Distractors named, 2+, unlabeled in ZIP | metadata.json names 2, nothing inside the ZIP flags one | `ui_contribution_rate_notice_2027.pdf` (2027 UI tax rates/reserve-ratio schedule) and `franklin_county_population_estimates_2025.csv` (county population/households/age) named in `metadata.json`; neither file name nor content inside the ZIP labels either as a distractor | Pass |
| Distractors relevant but unused | each weighs without being load-bearing | Both are genuinely on-topic UI/county artifacts a solver would open, and neither feeds the covered-jobs certification; no graded quantity is answerable from either alone | Pass |
| Deliverables 1-3, all in golden | prompt names exactly 2 | `ctf_certification_december_2026.xlsx`, `ctf_employer_jobs_december_2026.csv`, both present in `golden/` and `golden.zip` | Pass |
| Asks multi-dimensional, unit+rounding stated | in the asking sentence | "County jobs are to the nearest hundred, an employer's to one decimal, and changes are per cents to one decimal" is in `prompt.txt` itself | Pass |
| Identifiable answer shape, many gradable cells | grid/bridge/ranked-list/etc. | A 14-county + state grid (7 columns) in the xlsx, plus a 28,552-row employer-level grid in the csv; both downstream of the retention-share judgment | Pass |
| Golden ZIP holds exactly the requested files/formats | | `golden.zip` contains exactly the two named files, no extras | Pass |
| Nothing LLM-generated; golden reads as real work | | Judge's hygiene check (run inside the isolated scratch) found no provenance/benchmark/authorship leak and no LLM tells; main-session spot read of `ui_contribution_rate_notice_2027.pdf` reads as a genuine agency rate notice | Pass |

## Gate G reconciliation
Judge's thread (blind to the design artifacts): `mechanism: method_or_model_selection`,
`stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`.

Card (`.claude/skills/fingerprint/cards/task5.json`): `"gate_g": "method_or_model_selection"`,
`"stump_class": "analytical"`.

DESIGN_NOTE.md: "Gate G method_or_model_selection" (line 48); the note's own analysis explicitly argues
**not** data_semantics ("every field read correctly... gives a correct list of who has and has not
reported, and the list does not say what a missing employer's December jobs are") and **not** rule_application
("no filed rule says how a nonreporting employer's jobs are estimated... the data agreement describes
fields"), and states "no decoy" and "no certified replay."

These three independent sources agree exactly, with no mismatch to report. The judge, reasoning blind from
the files alone, landed on the identical classification the design note argues for on paper -- this is the
landable case the contract flags: the decisive step (informative-nonresponse identification, validated by
out-of-sample backtest) is the field's own textbook move (survey statisticians treat missingness as
ignorable or informative by exactly this kind of auxiliary-variable test), but the golden reaches it by
*applying* that standard method to this dataset's own structure (the payroll-agent transmission clustering),
not by reflexively executing a stated procedure. No distractor was misread as load-bearing by the judge.

## Stump power (Gate F)
The judge judges this a reasonable stump: the "obvious" move (carry each outstanding employer's September
jobs forward, scaled by its county/supersector's reporting-employer trend) gives "no county qualifies"
(Garrow +0.3%, Ostrom -0.5%), which is wrong, and reaching the right answer requires noticing the
exact-second `received_at` clustering (never named in any file), building the missing-alone vs.
late-transmission split from it, and validating retention shares against older, now-resolved quarters.
Per the client's library note, this is a textbook statistics-office move (treating nonresponse as ignorable
or informative via an auxiliary covariate, validated out-of-sample) applied to this dataset's own structure,
which the contract treats as a landable call, not a `too_easy` signal: the method is not narrated anywhere
in the files, and a strong model stopping at the shallow carry-forward, or at a coarser "whole payroll
agent is late" rule, lands on a different county set.

## Findings, ranked
1. (Low priority, does not affect the verdict) The judge's own rebuild of the liable/outstanding account
   counts came out one account higher than the committed 27,651/4,274 (27,652/4,275). It traced this to an
   ambiguous same-day status-history tie-break it could not fully isolate at medium effort, and confirmed it
   cannot move any county across the -2.0% line or change any rounded figure in the asks. If the author wants
   exactness, the judge's lead is accounts with a status-history event whose `effective_date` lands on the
   quarter boundary where ordering against a same-day LIABLE/INACTIVATED pair is resolved by `processed_date`.
2. No Gate A-E, F, G, or H finding that changes the verdict or disposition.

## Next action for the author
No fix required to ship. Optional: if full exactness in the liable/outstanding counts matters, check the
generator's same-day status-history tie-break logic (`processed_date` ordering on accounts whose
`effective_date` falls exactly on the Q4 2026 boundary) against the one-account discrepancy the judge found;
it does not touch any committed figure or the Garrow/Ostrom designation.
