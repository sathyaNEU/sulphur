# task20 architecture 6 (b9e0194): the platform's holistic audit (pasted by the author, 2026-11-13)

Verbatim.

> Holistic Audit
>
> The data work is strong. The commitments not yet called (4,474.8 by strategy), the stress distributions (685.6 /
> 466.2 / 273.9 / 291.3), the 2,778.7 reserve and the 791.0 of spending all reproduce exactly from the files, and the
> refinancing and successor-close steps are real analysis.
>
> The problem is that the call between program B, C, D and none rests on a capital-call forecast that the files do not
> force. B passes by only 34.2, and your own headroom band reaches down to 180.9 against B's 180.1 of calls. Two open
> choices each move the headroom by far more than 34. The first is the benchmark rescue calls: the benchmark has no
> investment-period field, so the age cutoff and the basis are both choices. Applied to the harvesting NAV, cutoffs of
> 4, 5 or 6 years give 125 to 212 measured above normal or 348 to 485 gross, against your 229.7. The second is the
> pacing basis (initial investments versus total contributions on the room left), which moves new-investment calls by
> roughly 30 to 110. A careful analysis that matches every fixed figure can land at about 1 of headroom, where no
> program passes.
>
> To fix this, state the rescue method in policy section 8 (the age that defines past the investment period, the
> basis, and gross versus excess calls) and the pacing basis. Alternatively, widen the gap between programs so that B
> clears the low end of your band by a clear margin.
>
> For what we are looking for, see https://project-sulfur.learn.joinhandshake.com/nov-09-updates.
>
> Reasoning
>
> Pre-flight: the golden blocks are present and the inputs match the task (same register, Corrigan Hart plan,
> programs A to D, policy with the USD 1,535m minimum). The golden deliverable files are not in the environment,
> which is normal for this review.
>
> Part A, correctness: every figure that has a fixed answer reproduces. I rebuilt the commitments not yet called:
> Buyout 1,601.8, Growth 421.4, VC 223.7, RE 581.2, Infra 1,172.7, Credit 474.0, total 4,474.8. This drops the
> superseded row, the released funds and the liquidated funds, counts pending funds in full, and rolls the two late
> statements (BO-102 and BO-113) forward with the custodian's Q4 calls. The stress distributions also reproduce:
> 685.6 / 466.2 / 273.9 / 291.3, total 1,717.0, from Dec-31 NAV of 6,091.7 at the benchmark's 2008Q3 to 2010Q2 rates
> by strategy. The reserve comes to 2,778.7 and spending to 791.0. The author's arithmetic holds: 2,778.7 - 791.0 -
> 1,955.5 + 1,717.0 - 1,535 = 214.2 to 214.3. The model run matches all of these exactly.
>
> The recommendation rests entirely on the forecast of capital calls: 1,955.5 from the author against 2,168.7 from
> the run. Policy section 8 leaves that forecast to judgment ("judged on the evidence the Office of Investments
> holds").
>
> Part B, determinism: not pinned. B passes only by 34.2, and the author's own headroom band (180.9 to 238.4) has a
> low end just 0.8 above B's 180.1 of calls. That means B passes only near the author's point estimate. Several open
> model choices move the headroom by far more than 34:
> - **Benchmark rescue calls.** The benchmark has no investment-period field, so "past their investment periods" must
>   be inferred from fund age, and the basis must also be chosen. Applied to Wexmoor's harvesting NAV of 3,639, the
>   2008Q3 to 2010Q2 post-period calls give 485 / 391 / 348 gross, or 125 / 179 / 212 above normal, for age cutoffs
>   of 4, 5 and 6 years. The author's 229.7 rests on a splice "past the shortfall the endowment's record reaches"
>   that no file states.
> - **New-investment pacing.** Measured as initial investments on the room left, pacing is stable at about 1,060 to
>   1,080. Measured as contributions, it runs 1,093 to 1,185.
> - **First-close slip.** The run reports a 122.6 swing.
> - **Pacing.** The run reports that a 10% change moves the headroom by about 117.
>
> The run reproduced every fixed figure, reached 1.0 of headroom, and concluded that no program passes. I cannot name
> a shipped pin that it broke.
>
> Part C, depth: the work is genuine. It covers assembly, credit-facility estimation, a fitted lender limit for
> refinancing, successor closes, and rescue calls from the benchmark, at depth level 4. The successor-close pattern
> is a constructed rule built into the register, but it takes analysis to find. The failure is determinism, not
> depth. The run's first break cannot be classified with confidence (likely a defensible alternative on follow-on and
> pacing calibration), so it is not valid evidence of difficulty.
>
> OPEN items do not change the verdict: the failure is demonstrated by the 34.2 margin sitting against a variant
> spread of more than 100.

## Checked against the build (2026-11-13)

- Reproduced on the shipped pack (b9e0194) before any edit: the benchmark's funds four, five and six years past
  their vintage, contributions over the previous quarter's value by strategy on the USD 3,639.2 million of
  harvesting value, give 485.2, 391.3 and 347.7 gross, the audit's own figures. The reading is the plain one of the
  sentence section 8 carried, and it differs from the golden's two-channel splice by more than the margin.
- The same reading on the property and infrastructure funds past their periods gave USD 157.9 million against the
  golden's 158.7 for those funds (their fees and the refinancing calls): the benchmark's old real-asset funds had
  met their own refinancing shortfalls in 2008 to 2010, so a run that carried section 8's benchmark sentence to
  every strategy reached the refinancing calls' total without reading a loan.
- The golden left fund expenses out of the calls (about 0.05 percent of commitment a quarter), which alone is of
  the size of the old margin.
- The run's own text was not pasted, so which of the two deciding judgments it made is not known; nothing is added
  to precedents.json from it.
- Depth was not disputed (level 4). The repair keeps both deciding judgments and files what the audit asked for.
