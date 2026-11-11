# determinism-check report, task9 (architecture 9, re-judge after repair), 2026-11-11

## Verdict
NOT_DETERMINISTIC (as the thread gave it; the thread did not mark SOLUTION_WRONG)
**Disposition:** SEND_BACK
**Stumping type:** mechanism: single_conceptual_flip, stumping_family: surface_read_rejection, surface_read_dependency: yes, sole_data_defect: no
Taxonomy: underspecified_objective. Order kept by the thread: yes (own_derivation.md written before graded_blocks.md was opened). Pack seen: target.zip sha256 prefix 5378a624; blocks extracted from the regenerated submission.md. Scratch: /tmp/determinism-check-task9-062652/ (verdict.md, own_derivation.md).

## Why
Policy section 7 defines alpha as P&L beyond what a passive holding of the markets a pod trades "would have earned". The golden reads "earned" as price move plus carry (10-year over the bill, Baa spread over the 10-year, a long-three/short-three G10 rate basket). No shipped file says that carry is netted, which markets each strategy group trades, or how the basket is built. The platform's own factor definitions (Risk_Model_Methodology_2023.pdf) are price-only. Executing the filed text literally, the thread got Credit 6.38% (golden 3.64%, band 3.48% to 4.14%), net 2027 P&L about 729 million (golden 594, band 549 to 649), and a failing-increase list of two to six pods against the golden's eight. These are the golden's own "hurried" figures (6.39%, 722 million), and its own Step 6 says that on the risk model's factors five of the eight pods clear the hurdle. The band excludes the literal reading on Credit alpha, the headline, the range and the hurdle list, so Gates C and E fail on the recommendation and supplementary answers 1, 2 and 3. The capacity answer is also only partly pinned: honest within-pod estimators give 19% to 26% against the golden's 25.5% (band 21.6% to 26.5%), and the failing list moves from {HC1107} to six pods as the doubling share moves from 20% to 29%.

## Recomputation ledger (first pass, thread's literal reading vs the blocks)
| Figure | Claimed (band) | Judge recomputed | Reproduced |
|---|---|---|---|
| Assembly: 75 duplicate rows, 79 code remaps, 3 absent days, thousand-USD units, 223 pods, 2,473 days | same | same | yes |
| R1 Commodities alpha | 11.41% (7.84 to 12.86) | 11.31% | yes, inside; band 5 points wide, grades nothing |
| R1 Credit | 3.64% (3.48 to 4.14) | 6.38% | NO, outside; matches the golden's price-only 6.39% |
| R1 Currencies | 5.48% (5.06 to 6.30) | 6.22% | inside, 0.08 from the upper edge |
| R1 Equity long/short | 8.88% (8.58 to 9.49) | 8.95% | yes |
| R1 Quantitative equity | 8.67% (7.96 to 9.12) | 8.66% | yes |
| R1 Rates | 8.03% (7.42 to 8.31) | 7.94% | yes |
| R1 Volatility | 7.87% (7.72 to 8.91) | 7.87% | yes |
| R2 doubling share | 25.5% (21.6 to 26.5) | 24.2% spell NLS; 18.8% pod-year; 21% within-pod slope; 19% to 20% other variants | partial; reasonable rivals fall below the band |
| R3 expected net 2027 P&L | USD 594 m (549 to 649) | about 729 m (sensitivities 664 to 900: gamma 0.33 gives 778, 0.50 gives 664, no shrinkage 900) | NO, every variant outside |
| R4 10th percentile | USD 37 m (-8 to 89) | 266 m (idiosyncratic noise only: 624 to 875 for the whole range) | NO |
| R4 90th percentile | USD 1,077 m (1,016 to 1,161) | 1,209 m | NO |
| R5 failing set | HC1054, 1058, 1062, 1082, 1098, 1107, 1132, 1135 (1039 and 1125 either way) | gamma 0.40: HC1107, HC1132 (HC1098 borderline); gamma 0.33: HC1107; gamma 0.50: HC1082, 1098, 1107, 1115, 1119, 1132 | NO, the set is capacity dependent; only HC1107 fails in every variant |
| R6 recommendation | plan 594 and drop eight | plan about 729 and drop two to six | NO |

## Competing answers that survived
1. Carry in alpha. Price-only factors per the filed methodology versus price plus carry. Credit 6.38% / 722 to 729 million / two to six failing pods against 3.64% / 594 million / eight. The shipped rule meant to close it is policy section 7's "would have earned", which does not say carry. Open.
2. Capacity estimator. 19% to 26% across defensible within-pod fits against a band of 21.6% to 26.5%; the hurdle list moves with it. Open.
3. Range scope. Whether market variance counts in the 80% range (about 250 million wide idiosyncratic only, about 940 million with market risk, golden 1,040 million). Policy 8d says "the year's net P&L", so the thread took market risk in, but the width still depends on this and on alpha-uncertainty inclusion. Open.
4. Pooled versus average-of-years annualisation moves Currencies, Rates and Commodities by up to 1.1 points; the bands absorb most of it.
5. Whether onboarding step-ups count as increases. HC1147's 50% step falls about 30 Dec 2026, so the 2026 column hides it; the thread handled it and did not check the golden's treatment.
6. HC1039 and HC1125 are declared "either way" in the blocks (accepted as the band of the flagged set, not as a fork).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Usable files | 10 or more | 41 (the thread counted 43) | yes |
| File categories | 2 or more | csv, xlsx, pdf: spreadsheet and text | yes |
| Large messy CSVs | one of 20,000 rows or more, one of 10 to 20 printed pages or more | 114,983-row legacy P&L file; 77,544-row P&L file | yes |
| Distractors in metadata.json | 2 or more, none labelled in the ZIP | DAAA.csv, IR3TIB01USM156N.csv declared; nothing in the ZIP labels them. The Aaa variant moves Credit by 0.0 to 0.17 points, so it carries no result. The thread called the FX, IR3TIB and DAAA series the hidden input, which means they are not distractors if carry is the intended step | yes on count; relevance not tested beyond that |
| Deliverables | 1 to 3, all in the golden | 2 (pptx, xlsx); golden.zip holds exactly those | yes |
| Asks | multi-dimensional, unit stated, no rounding instruction | prompt (571 characters) states units and no rounding; asks are not stacked lookups | yes |
| Answer shape with 4 or more results | one of fourteen | 6 results (a forecast with bands, a flagged set, a defined metric); the Commodities band (5 points) grades nothing | yes, with that band defect |
| Realism and no LLM tells | clean | thread: Files/Hygiene PASS | yes |
| No file reveals construction | none | none found | yes |

## Gate G reconciliation
Thread: mechanism single_conceptual_flip, stumping_family surface_read_rejection, surface_read_dependency yes, sole_data_defect no. The surface read is the risk model's price-only factor set that the golden asks the solver to reject for a carry-inclusive holding.
Design note: its Hidden factor record lists carry as "real, not only in deciding units, modelling, keep", which says the difficulty is spread. The thread finds the weight on one reading. The note's own Step 6 and Step 2 show the carry reading alone changes Credit alpha, the headline (722 versus 594) and five of the eight failing pods, so the note's carry-hint count is understated.
Gate G proper (a shipped artifact ranks the candidates and gets it wrong): the thread reported no such finding.

## Gate H line (thread)
domain: pass; layers: pass; results: 4 critical components plus 3 asks across about 6 areas; one_thing: data_semantics (the carry convention); effort: quick 0.5 of 4, careful 1.5 of 4, thorough 4 of 4 if the carry is found; one_fact: "net the carry a passive holding earns" rescues 3 of 4 critical components (Credit alpha, headline and range, failing list), so H5 fails.
Reconciliation with the note's `## Effort test`: the note grades quick 0.5 of 6, careful 1.5 of 6, thorough 6 of 6, and says its largest hint ("a passive holding earns its carry as well as its price moves") rescues 2 of 6 (R1, R3). By the note's own Step 6 the same hint also moves R5 and R6 (five of the eight failing pods clear on price-only factors) and R4's range depends on R3, so the hint rescues 4 or more of 6, above a third. The thread's careful grade of 1.5 of 4 is also above a third. A thread-found hidden factor fixed by one modelling step ("holding returns as factors") that the note calls modelling is on the send-back list.

## Stump power (Gate F)
The task would stump runs, mainly through the carry reading. A careful run using the filed methodology factors lands on Credit 6.39%, net 712 to 722 million, clears five of the eight failing increases, and loses the headline, answer 2 and Credit alpha together. Capacity, shrinkage, drawdown and payout simulation are earned by a careful run inside the bands, so the pricing sits on one reading, not on a chain.

## Findings, ranked
1. Carry is not filed anywhere and the filed methodology is price-only: Gates C and E fail on R1 (Credit), R3, R4, R5, R6.
2. One thing (data_semantics) carries most of the score; one-fact test fails (3 of 4 components by the thread, 4 or more of 6 by the note's own figures).
3. Capacity band 21.6% to 26.5% excludes honest within-pod rivals (19% to 21%) and the hurdle list is sensitive to the doubling share.
4. Range scope (market variance, alpha uncertainty) is not pinned; the thread's range is 266 to 1,209 against 37 to 1,077.
5. Commodities band (7.84% to 12.86%) is too wide to grade anything; the R4 10th-percentile band (-8 to 89) is also wide.
6. HC1147 onboarding step is hidden by the draft's 2026 column; the golden's treatment is unchecked.

## Next action for the author
File the passive-holding convention (what carry counts, from which series, which markets each group trades) in the policy or methodology, or drop carry and make the factors-only alpha the golden; then pin the capacity band to the fitting method, state the range scope, rebuild the hurdle list on a doubling share the data pins within the borderline pods' margin, and rerun.
