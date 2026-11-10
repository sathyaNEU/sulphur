# determinism-check report, task1, 2026-11-10

Re-judge licensed by `/fix-determinism`, run once after the generator repair that followed the platform's
holistic audit return on determinism (pipeline.json `returned[1]`, 2026-11-10). This report overwrites the
prior `determinism_check_report.md`, which graded the pre-repair cut.

## Verdict
**DETERMINISTIC**
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection + statistical_rigor, secondarily decomposition_attribution (bridge); stumping_family: analytical_non_defect; surface_read_dependency: no; sole_data_defect: no

## Why
The isolated judge thread, seeing only a fresh unzip of `target.zip` and the extracted blocks, reproduced every
load-bearing figure from the shipped files, several to the exact euro against the independently filed
`kpi_monthly_2026-01_2026-09.xlsx` export (September Business 6,837,615 and Team 1,838,461 against the thread's
own recompute 6,837,614.80 and 1,838,460.67). All four audit findings that returned the prior cut are closed on
the thread's own rebuild: (a) policy 5.3 is a literal floor rule and the submission's commitment is the floor of
the simulated band, not a rounding of the point estimate or the 20th percentile; (b) policy 5.2's text explicitly
rules out an added allowance beyond the records, and the thread confirmed the direction (estimation uncertainty
stacked on outcome variation is strictly wider) though it could not rerun the full 2,000-path Monte Carlo
bit-for-bit; (c) the two note figures (ask 5, ask 6) are stated as single point values at the nearest EUR 0.1
million, and every defensible method the thread built for each lands in the same bin; (d) the thread's own three
naive trailing extrapolations from the book's own month ends (EUR 10,920,000 / 11,490,000 / 10,720,000) all clear
the draft's EUR 10.3 million while its own from-scratch flow-level forecast (EUR 10,220,000) does not, so the
yes/no verdict on the draft turns on doing the real analysis, not on a trailing read.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Business ARR, 31 Oct 2026 | 7,020,000 | 7,018,144 | Yes |
| Team ARR, 31 Oct 2026 | 1,830,000 | 1,834,159 | Yes |
| Total ARR, 30 Sep 2026 (ties to KPI export) | 8,680,000 | 8,676,075 (6,837,615 / 1,838,461, matching the KPI export to the euro) | Yes, exact cross-file tie |
| Naive sum of every exported line (no cleanup) | 7,120,000 | 7,122,323 | Yes |
| Repricings since 1 Jan 2026 | 519 | 519 | Yes, exact |
| Price-vs-size pattern | "falls with size, about 93 per cent of the list rise at 20 seats" | corr(log seats, per cent price change) = -0.915; median realised uplift 25.1 per cent against a 26.7 per cent list rise at 15 to 19 seats | Confirmed, real pattern |
| CRM stage-odds valuation of open deals (named rival) | 1,200,000 | 1,220,995 | Yes |
| Win-odds-by-stage-and-age valuation of the same deals (golden method) | 800,000 | 839,298 (own from-scratch stage/age win-rate model fit on closed deals) | Same bin |
| Trailing 12-month net-new ARR carried forward | 10,920,000 | 10,922,584 | Yes, exact |
| Compounded 12-month growth carried forward | 11,490,000 | about 11,489,700 | Yes, exact |
| Trailing 6-month run-rate carried forward | 10,720,000 | 10,718,534 | Yes, exact |
| Team-cohort Dec-2027 ARR, naive flat-rate variants | 1,200,000 | 1.03 to 1.19 million across two naive variants | Same bin |
| Team-cohort figure, seasonal pattern with no fading excess | 1,400,000 | 1,448,000 | Same bin |
| Team-cohort figure, golden (seasonal plus fading excess) | 1,300,000 | 1,277,000 to 1,290,000 depending on the fade-rate swept | Same bin, most sensitive input found |

No load-bearing figure the thread traced failed to reproduce.

## Competing answers that survived
None disqualifying. Two notes:
- SF13 (the commitment rounding) was the audit's prior finding; the thread confirmed the floor rule and the
  round rule are genuinely different operations (they coincide here only because P20 sits inside the 50,000 EUR
  midpoint of its grid cell, a numerical coincidence the thread demonstrated with a counterexample, not something
  the text forces), and found no shipped sentence licensing round-to-nearest instead.
- R3, the Team-cohort EUR 1,300,000 figure, is the chain's most fade-rate-sensitive input: the thread's own crude
  sweep straddles the golden value (1,277,000 to 1,290,000) without falling outside the nearest-EUR-0.1-million
  bin. The two named rivals (1,200,000 ignoring seasonality, 1,400,000 ignoring the dated minimum-seat change)
  are each ruled out by an identifiable, data-visible omission rather than being an equally defensible reading,
  so this is not a Gate C fork, but it is the single result worth a second look if the fade-rate is not pinned
  by a stated convention in the generator.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count / categories | 10+ usable files, 2+ categories | 12 files (`arr_reporting_policy_2026.pdf`, 8 CSVs, 3 XLSX); formats pdf, csv, xlsx | Pass |
| Large messy files | one CSV 20,000+ rows, one CSV 10-20 printed pages+ | `team_invoices...csv` 157,622 rows and `workspace_monthly_activity...csv` 205,333 rows (both well over 20,000); `pipeline_snapshots...csv` 11,951 rows and `workspace_account_links.csv` 11,207 rows each clear a 10-to-20-printed-page floor | Pass |
| Distractors named, unlabelled in zip | 2+ named in metadata.json, none labelled inside the zip | `metadata.json` names `support_tickets_2026.csv` and `nps_responses_2026-q3.csv`; grep for "distractor/decoy/unused" across every shipped file returns nothing | Pass |
| Distractors relevant but unused | each ties to the billing accounts yet is unused by the solution | both carry `account_id`/`plan` columns, tempting a churn-signal join; neither feeds a golden figure (confirmed by the thread's own search and by the design note's "benign oddities decide nothing") | Pass |
| Deliverables 1-3, present in golden | prompt requests a spreadsheet and a short note | golden.zip holds exactly `arr_2027_forecast.xlsx` and `arr_2027_note.docx`, matching `metadata.json`'s `deliverables` | Pass |
| Asks multi-dimensional, unit/rounding stated | no stacked lookups, units pinned | prompt pins ARR to the nearest EUR 10,000 and the two note figures to the nearest EUR 0.1 million | Pass |
| Answer shape, 4+ checkable results | one of the client's 14 shapes | a forecast path with an 80 per cent band and a bridge of drivers; 7 results (R1 to R7) in the results chain | Pass |
| Golden ZIP holds exactly the requested files | matching formats | `arr_2027_forecast.xlsx` (xlsx) and `arr_2027_note.docx` (docx), matching the prompt's "a spreadsheet... plus a short note" | Pass |
| Golden reads as a real work product | no LLM tells | the note opens "To: Naomi Weijters / From: Jelte Helmerhorst, Revenue operations / Date: 6 November 2026 / Re: December 2027 ARR for the 2027 plan," cites sources and the policy section, and states figures without explaining what ARR means | Pass |

## Gate G reconciliation
Thread: mechanism method_or_model_selection + statistical_rigor (secondarily decomposition_attribution for the
bridge); stumping_family analytical_non_defect; surface_read_dependency no; sole_data_defect no. Design note's
"Strategy label" (WORKS IN FORM: left truncation and immature cohorts, heterogeneity pooling hides, uncertainty
matching the design) and its "Not a decoy / not rule application / not semantics" lines describe the same thing
in the note's own vocabulary: every decisive quantity is estimated from the records, none is handed over by a
document, and the policy files the WHAT (the ARR definition, the bridge categories, what the range carries, how
the commitment is read) while the HOW stays open. The two readings agree: this is not a surface-read-rejection
task, and on the clean-data test the task would still need the price-elasticity fit, the cohort-survival and
win-rate-by-age models, and the literal 5.3 floor rule.

## Gate H reconciliation
Thread's Gate H line: domain pass; layers pass (layer 1: duplicate/credited/reissued billing lines, GBP/EUR mix,
a dated minimum-seat change, two unused distractors; layer 2: price elasticity, renewal/utilisation modelling,
pipeline win-rate-by-age, cohort survival with a decaying excess, Monte Carlo banding, the literal policy rule);
results 7-8 graded across 6+ of the 14 areas; one_thing none; effort quick about 1 of 8, careful about 3-4 of 8,
thorough 7-8 of 8; one_fact ("read 5.3 literally: the commitment is the largest 0.1 million step met in at least
80 per cent of outcomes, not a rounding of the expected value or the 20th percentile") rescues about 2 of 8.

Design note's card: `judge.gate_h` on file reads "pass: 7 results across 5 areas, one_thing none, one fact
rescues 1 to 2 of 7." The note's own Effort test table grades quick 0 of 7, careful but hurried 1 of 7
(R1 only), thorough 7 of 7; largest single hint rescues 2 of 7 (R5, R6); pair estimate 20.8.

Both readings agree on `one_thing: none` and on the one-fact share (around a quarter to a third, comfortably
under the client's third-of-results ceiling either way). The one real divergence is the careful-but-hurried
share: the note's table holds it at 1 of 7 results (only the opening-book assembly, R1), while the thread's own
"careful" grade came in at 3-4 of 8 (around 40 to 50 per cent). The thread flagged the cause itself: it built
several from-scratch models (a stage/age win-rate fit, a price-elasticity regression, three Team-cohort decay
variants) in the course of a single review pass, which is closer to the note's thorough, self-checking pass than
to a real-world "afternoon, careful but hurried" solver who would not fit and cross-check five separate models
in one sitting. Read against the note's own Effort test (quick 0, careful 1, thorough 7 of 7, each clearly
separated), this is not a finding that the design overstates its difficulty: the thread's self-reported
"careful" grade is inflated by the thoroughness of the review method itself, not by the task being easier than
designed. No graded result's band excluded a rival the thread actually ran; R3's band (the Team-cohort figure)
held the thread's own sweep inside the bin. The declared distractors were not found carrying any result. On
balance, Gate H reconciles cleanly: no finding here would move the disposition off APPROVE.

## Stump power (Gate F)
The thread's own assessment: stump power comes from chaining five or more distinct, data-grounded mechanisms
correctly (price-vs-size degression, Team seasonal-plus-decaying-excess hazard, utilisation-and-group-led
renewal exits, pipeline win-rate-by-stage-and-age, and the literal 5.2/5.3 band-and-commitment rule) and from
propagating sampling uncertainty into the band, not from any one mechanism alone; each individual mechanism is
visible on a single plot or group-by once looked for, consistent with "a mechanism the rows visibly carry is
modelled on sight" pricing nothing on its own. The design note's pair estimate of 20.8 and its Effort test
(quick 0 of 7, careful 1 of 7, thorough 7 of 7) are the author's own measurement of the same chain; nothing in
the thread's independent pass contradicts that a careful-but-hurried run leaves most of these results on the
table.

## Findings, ranked
1. (Not a finding, informational) R3's Team-cohort fade-rate is the single most parameter-sensitive input in the
   chain; both the thread's independent sweep and the design note's own closure table (SF17: "the January
   excess's lasting level, from the last three months, the last two, or an exponential with a floor... any,
   inside the bin") treat this as a rival band already closed inside one bin, so no action is required, but it
   is the one result worth a second glance if the generator's fade-rate is ever retuned.
2. (Not a finding) The thread could not rerun the full 2,000-path Monte Carlo bit-for-bit within its session and
   instead verified policy 5.2's text and the direction of the estimation-uncertainty effect; this is a scope
   limit of the review pass, not a defect in the submission, and the two reported P20 values (10,020,000 with
   estimation uncertainty against 10,050,000 without) are close enough, and consistent enough with the design
   note's own closure (SF20), that nothing here changes the verdict.

## Next action for the author
None required before shipping; stage 5 (READY) may proceed. If capacity allows before upload, confirm in the
generator that the Team-cohort fade-rate (the input the thread's own sweep found most sensitive) is driven by a
fitted procedure on the shipped history rather than a hand-set constant, so the result stays a modelling output
rather than a tuned parameter; this does not block APPROVE.
