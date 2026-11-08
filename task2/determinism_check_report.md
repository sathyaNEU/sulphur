# determinism-check report, task2, 2026-11-08

## Verdict
DETERMINISTIC
**Disposition:** FIX_NOW
**Stumping type:** mechanism: forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Judge thread: one pass, workspace /tmp/determinism-check-task2-20261108225639/, verdict at verdict.md there. Spec gates and the design-note reconciliation were not run in this pass (see Next action).

## Why
Read literally and rebuilt from the files, the forward share is forced by one structure. Under release 6.0 the heavy-correction rate depends on whether a clinician began on or after their hospital's compulsory date (19.0 per cent against 2.3). 2027 has no release (SN-2026-14). 1,567 non-dictating clinicians at the two teaching hospitals go compulsory on 1 February and 1 October. Every variant of the judge's own forecast lands the same quarterly bands (under 10, 10 to 12, 10 to 12, 12 to 14), so Ceiling C (14) is forced. The steady 7.4 per cent carry-forward and the hospital reweighting give 10 and are the intended wrong routes.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Compulsory-start rate under 6.0 | 19.2% | 19.0% (n=6,848) | Yes, within 0.2 |
| Voluntary rate under 6.0 | 2.4% | 2.3% (n=16,351) | Yes, within 0.1 |
| Release steps within kind | 4.0 by about 3, 5.0 by 6, 5.2 by 3, 6.0 by 3 | C: 27.1, 21.9, 21.0, 19.0; V: 4.1, 3.4, 2.9, 2.3 | Yes, every release lowers |
| Quarterly shares tie to quality_reports | tie | 2026 Q4 7.62 vs report 7.61 | Yes, within about 0.1 pt |
| Teaching hospitals | 2,070 in post, 503 dictating | 197+306 dictating, matches rollout xlsx | Yes |
| Ramp at go-lives | 23 / 53 / 82% | 0.23 / 0.53 / 0.82 | Yes |
| Voluntary share of dictation, Q4 2027 | about 36% | about 38% | Within modelling rounding, but the figures differ |
| 2027 quarterly bands | <10, 10-12, 10-12, about 13 | Q1 8.7, Q2 10.8, Q3 11.2, Q4 12.7 | Yes, bands hold |
| Sensitivity (leave 7-12%, start 90-100%, volume 38-44, ramp variants, C rate 18.5-20) | n/a | Q1 8.5-9.1, Q2 10.6-11.3, Q3 10.9-11.7, Q4 12.4-13.3 | Every band holds |
| Nine in ten Q4 dictations | 16 | P90 about 16.15 | Yes under nearest-whole rounding; see fork |
| Ceiling | C, 14 | C, 14 | Yes |

## Competing answers that survived
1. Supplementary ask 4, rounding direction. P90 is 16.15. Round to nearest gives 16 (golden). Smallest whole number with at least 90 per cent under gives 17 (89.8 per cent are under 16.0 at the judge's Q4 mix; 92 per cent under 17). The prompt says "in whole per cent" and does not pin the direction. Closing rule needed: "rounded to the nearest whole per cent".
2. Early-month learning effect (not a surviving fork, noted). If the 6.0-only first-three-month rates (14 against 19.5 per cent) were real, Q4 would fall to about 11.4 and the call to 12. Across all releases it is noise (months 0, 1 and 2 observed 23, 17 and 21 per cent against 22 expected; mean WER flat at 11.3 to 11.9 by month since start), so the data separates it. It is the closest thing to a fork in the call. The judge recommends a design-note line.
3. Carry-forward or reweighting (A, 10) and new dictators at recent starters' level (12): both ruled out by data (within-clinician release steps, the kind split, the same 19 per cent at all six go-lives).

## Spec gates
Not run by the judge thread. Judge's hygiene read (Files/Hygiene), not a substitute for the gate table below:

| Gate | Required | Actual (judge's read) | Pass |
|---|---|---|---|
| Usable files | 10 or more | 13 | Yes |
| File categories | 2 or more | csv, xlsx, pdf, docx | Yes |
| Large CSVs | 20,000 rows plus a 10 to 20 page CSV | audits 75,661 rows, volumes 81,150 rows | Yes (page length not checked) |
| Distractors | 2 or more, unlabelled | headset_inventory, ehr_integration_uptime, support_tickets, unlabelled | Yes (metadata.json not checked) |
| Temporal coherence | n/a | Draft sent 14 Dec 2026, due 15 Jan 2027, yet audits run to dictated_on 2026-12-28 with audited_at to 2027-02-09 | Flag |
| Deliverables, asks, golden ZIP contents, realism | per spec | not checked | Open |

## Gate G reconciliation
Thread's classification: mechanism forecasting; stumping_family analytical_non_defect; surface_read_dependency no; sole_data_defect no. No Gate G issue: the reported quarterly shares are correct, and on clean data the task still stumps. The thread did not name the declared distractors as carrying the task. Gate H line: domain pass; layers pass; decisive_step analytical; chain 5 inferences; judgment: separating two explanations for one pattern (selection into dictation by compulsion against release gain) and projecting outcomes not yet observed (ramp-weighted mix); one_fact none (the sentence "clinicians who started after the compulsory date run at 19%" still leaves the typing, the linkage of reissued numbers, the volume ramp and the Q4 mix to build). Comparison with the design note and card (stump_class, analyst_test, domain_test) not yet made.

## Stump power (Gate F)
High. A strong analyst who cleans correctly sees a steady 7.4 per cent share, notes no release in 2027, reweights to the 2027 hospitals and commits to 10 (Ceiling A). The decisive work is the within-clinician release steps, typing clinicians by start against the compulsory date, and a volume-ramped forecast of the two go-lives. The "recent starters' level" route gives 12, a partial-credit route. Nearest margins are thin but clean: Q4 against the 12 line is 0.4 to 1.3 pt across variants, Q2 against the 10 line is 0.6 pt.

## Findings, ranked
1. Rounding of the nine-in-ten rate unpinned (16 against 17). Fix: one clause in the prompt, "rounded to the nearest whole per cent".
2. Temporal incoherence: the draft is dated 14 December 2026 with a 15 January 2027 due date, yet audit and volume data run to late December 2026 and audited_at reaches 2027-02-09. Fix: move the draft and notice dates or truncate the data window (a pack rebuild; does not alter the call).
3. Answer-block figures at a finer precision than the data carry or differing from recomputed values: 19.2 and 2.4 (recomputed 19.0 and 2.3), voluntary Q4 volume share about 36 (recomputed about 38). Fix: make the solution blocks agree with the generator output.
4. Design-note line on the early-month learning effect and why the data rules it out.

## Next action for the author
The fixes are applied in the generator and the main session is running the one targeted re-judge of the FIX_NOW. After it returns, run the spec gates and the Gate G and H reconciliation against the design note and metadata.json, which this pass has not done.

## Targeted re-judge of the FIX_NOW (2026-11-08)

One isolated thread (Sonnet, medium) read the bundle copied to /tmp/determinism-check-task2-f1794178949/ and the
rebuilt answer blocks, with the first pass's fix list and recomputed evidence quoted. Verdict: DETERMINISTIC;
disposition APPROVE. The prompt's "rounded to the nearest whole per cent" closes the 16 against 17 reading (its fourth
quarter percentile 16.0 to 16.2 across compulsory-start shares of 0.60 to 0.64); the audit export's latest audited_at
is 7 January 2027 and the quarterly reports still tie to the cleaned audits; the kinds' heavy shares (19.0 and 2.3 per
cent) and the voluntary share of fourth-quarter dictation (38 per cent) agree with "about 19", "about 2" and "under two
fifths". Its forecast, 8.6, 10.7, 11.1 and 12.7 per cent, lands 10, 12, 12 and 14 and Ceiling C under every variant it
ran. Its one nit, the record's range stated to a tenth (7.7 against a cleaned 7.75), was restated as about 6 to 8 per
cent. No further pass: a FIX_NOW is re-judged once.

