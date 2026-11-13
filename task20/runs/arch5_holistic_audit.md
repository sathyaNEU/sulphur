# task20 architecture 5 (f927b34): the platform's holistic audit (pasted by the author, 2026-11-13)

Verbatim.

> Holistic Audit
>
> Your package is strong. The reserve (2,137.4), spending (573.0), stressed distributions (364.1 / 285.8 / 157.2 /
> 202.6) and uncalled commitments (4,303.7 by strategy) all come out exactly from the files when I rebuild them.
>
> There are two problems.
>
> First, your final recommendation reads "no more than USD 250 million (USD 268.6 million before the policy's USD 25
> million steps)". No file has a USD 25 million step rule. Section 9 of the policy adopts a discrete program, and your
> own answer picks program D at USD 45 million. Please rewrite it as "Adopt program D (Corvane Ventures VI, USD 45
> million)".
>
> Second, the decisive calls are not forced. Section 8 says only "can be expected to make ... judged on the evidence".
> Your answer depends on two modelling judgments that each flip the program:
> - Rolling forward the six managers' line stock (without it, headroom is 168.3 and the program is C).
> - Taking a steeper 2009 slope from the benchmark funds beyond the endowment's own range (without it, headroom is
>   251.6 and the program is A).
>
> A careful model that holds support at its observed plateau gets about 194 of headroom and picks B. Your upper band
> of 115.4 clears C's 123.8 by only 8.4.
>
> To fix this, pin the extrapolation basis in a shipped document. For example, an Office of Investments methods note
> could say that support behaviour beyond the endowment's own record is taken from the benchmark funds past their
> investment period. Also state how line balances are carried for managers whose company files end early. Then widen
> the gap between program D and program C so it holds across reasonable variants.
>
> For what we are looking for, see https://project-sulfur.learn.joinhandshake.com/nov-09-updates.
>
> Reasoning
>
> Pre-flight: the golden is present and the inputs match the task (Wexmoor, Corrigan Hart, programs A to D, all 14
> files).
>
> Part A, correctness. I recomputed every deterministic input from the files:
> - Liquid reserve at the policy factors: 2,137.41 (author 2,137.4, agree).
> - Spending: 2 x 286.5 = 573.0 (agree).
> - Stressed distributions on 31 December values. I took the latest statement per fund-quarter, rolled the two late
>   funds forward on the custodian's Q4 cash, and applied the 2008Q3 to 2010Q2 benchmark rates per section 7. I get
>   364.09 / 285.81 / 157.22 / 202.64 (agree).
> - Uncalled commitments by strategy: Buyout 2,025.28; Growth 466.03; VC 202.03; RE 287.09; Infra 834.66; Credit
>   488.63; total 4,303.73 (agree).
>
> The headroom identity holds: 2,137.4 - 573 - 1,345.9 calls + 1,009.8 distributions - 1,150 = 78.3.
>
> The final recommendation does not match the rest of the answer. It reads "Approve a 2027 private-fund budget of no
> more than USD 250 million (USD 268.6 million before the policy's USD 25 million steps". The supplementary answers
> commit to program D, which is USD 45m. No shipped file has a USD 25m step rule. Section 9 of the policy adopts a
> discrete program, and no program totals 250. A reader would conclude something quite different from "program D".
>
> Part B, determinism. The whole call turns on the capital-call forecast, and policy section 8 leaves it fully open:
> "those the endowment's managers can be expected to make ... judged on the evidence". By the author's own account,
> two modelling judgments each flip the program:
> - Rolling forward the line stock of the six managers whose files stop in 2024 (138.5 rather than 2.2): without it,
>   headroom is 168.3 and the program is C.
> - Extrapolating a second, 4.49x steeper support slope from the benchmark's 2009 calls: without it, headroom is 251.6
>   and the program is A.
>
> I confirmed that a jump past a shortfall of about 0.45 does appear in the benchmark. But carrying industry-fund
> contribution behaviour over to Wexmoor's company-level follow-ons, beyond the endowment's own observed range, is a
> judgment no file forces. The run held support at the plateau it observed and got headroom 194.2, which gives program
> B. Its own sensitivities move B to C or D under several reasonable variants. The author's band tops out at 115.4
> against C's threshold of 123.8, a margin of only 8.4 that rests on the author's own model.
>
> Part C, depth. The task is genuinely deep (level 4): assembly, missingness, extrapolating beyond the record's range
> and synthesis all compound. It is not a one-thing flip. It fails on the internal inconsistency and on determinism.
>
> Sub-results:
> - S1, reserve/spending: not hard.
> - S2, distributions: not hard.
> - S3, uncalled commitments: moderately hard.
> - S4, line stock of the six managers: hard.
> - S5, extrapolation of the support response: hard.
> - S6, full call forecast and headroom: hard.
> - S7, program call: synthesis.
>
> Run losses: calls in H2 2027, H1 2028 and H2 2028, the headroom, and the recommendation. All trace to S5/S6, so
> concentration is high. The run's first break is defensible_alternative_rejected: it noticed the issue ("Uncapped
> linear distress support: B headroom -69.14; D becomes largest. This is rejected...").
>
> Reporting labels: test_time_scaling = scales. analysis_type = Forecasting & Predictive. answer_shape = a yes/no call
> per program, with a forecast path and band. difficulty_profile = modelling and synthesis. data_modality = panels and
> administrative registers.

## Checked against the build (2026-11-13)

- The Final Recommendation: the platform carried architecture 4's text (2b71e24, "no more than USD 250 million ...
  USD 25 million steps"); architecture 5's submission.md (f927b34) opens on program D. The architecture 4 block was
  pasted with architecture 5's other blocks. The repaired write-up opens on the auditor's wording.
- Determinism: true. Policy section 8 files no basis for either judgment, and the run's plateau (194.2, program B) is
  a defensible reading of what the shipped text allows. Both forks name what R2's and R3's work recognises (the
  fork-is-the-result test), so pinning them as asked turns both stumps into filed reflexes. The audit's run also
  rebuilt the six managers' stock unprompted (its first-half 2027 calls inside their band), so J2 was already a
  reflex by run evidence.
- Depth: with both stumps pinned the stump factorial has none left; the repair keeps the pins the auditor asked for
  and rebuilds the call on two new judgments the records force (DESIGN_NOTE.md, Tried and rejected, 2026-11-13).
- The run's own text was not pasted.
