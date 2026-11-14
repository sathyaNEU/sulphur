# task24 determinism check (pass 2, after the DL-03 section 7 fix)

**Verdict:** DETERMINISTIC
**Disposition:** APPROVE

## What changed and whether it closes the finding

`launch_policy_DL-03.pdf` v2 now reads, in section 3: "Expected accuracy is the point forecast of section 7, not a
high or low case," and files a new section 7:

- 7.1 pins the curve's form (`1 - 0.5 x (1 + T/K)^(-b)` on pairs with a better reply), a scale `K` fitted **per
  ticket type**, a single bend `b` fitted **across all types**, and "the curve has no ceiling below 1."
- 7.2 pins the ceiling's basis against the standard: the share of a type's pairs where the standard's reply is the
  better one, plus half the share of pairs whose replies are equally good.
- 7.3 pins the forecast as "the curve at the values fitted on the record: the point forecast," and that a reported
  range "does not move it."

This closes, by name, all four readings the finding listed:
- **Free ceiling (deferred launch):** closed, "no ceiling below 1" fixes the asymptote at 1.
- **Ceiling from split share (10,000-12,000):** closed, 7.2 files the exact basis (better-reply share plus half the
  tie share), not a cruder split-count reading.
- **Shared vs per-type bend:** closed, 7.1 pins one bend shared across types and a scale per type; `submission.md`
  Step 4 reports the data itself also rejects a separate bend by LR 4.3 on 4 df, consistent with, not needed to
  force, the filed convention.
- **Rational-curve point fit (22,000) vs bootstrap mean (62,000):** closed, 7.3 pins the point forecast; the
  blocks' own item 11 keeps a bootstrap but only for the reported range, never for the governing forecast.

## Evidence (figures recomputed from the freshly unzipped target.zip)

| Item | Block value | Recomputed |
|---|---|---|
| Vendor error vs technician standard (device troubleshooting, Tallyfield vs Ardentdesk), from `label_audit_2026.csv` (penvale_technician majority as standard, no-preference set aside, Ardentdesk left/right resolved via `shown_left`) | 41.3 / 13.2 | 41.3 / 13.2 (exact) |
| All 10 cells of item 1 (5 ticket types x 2 vendors) | per block | all 10 reproduce exactly (21.5/10.2, 29.3/15.2, 29.8/10.8, 23.8/10.7, 41.3/13.2) |
| Order cost | USD 3.60/comparison (Ardentdesk), USD 0.42/comparison in steps of 10,000 (Tallyfield option) | `ardentdesk_quote_AD-Q-2611-07.pdf` and `tallyfield_order_TF-PEN-2027-Q1.pdf` match exactly; 38,000 x 3.60 = 136,800 and 10,000 x 0.42 = 4,200 confirmed |
| DL-03 section 3 wording | "the point forecast of section 7" | confirmed verbatim in the shipped PDF |
| DL-03 section 7 (curve form, K per type, shared b, no ceiling below 1, tie-share-based ceiling, point forecast) | as described in the fix | confirmed verbatim in the shipped PDF, all five elements present |

## Forks checked beyond the finding's four

- **"Training signal" T's definition is not itself spelled out numerically in section 7.1** (count of usable
  comparisons vs the blocks' label-information weighting). Checked whether this reopens an unpinned ambiguity: the
  shipped audit (`label_audit_2026.csv`) itself displays a large, type-varying quality gap between vendors
  (confirmed above, e.g. device troubleshooting 41.3 vs 13.2), so a naive "one comparison = one comparison" reading
  is visibly contradicted by a file any solver must already build to answer item 1; the design's own Step 6 runs
  eight differently-specified variants (a logistic curve in log information, the pull on a square root of crowd
  share, plain error rates, coarser length bins, no-preference counted, the audit alone, the pull from the audit
  alone, the reviews alone) and all eight land Ardentdesk-only in the 36,000-40,000 band. Only the shortcuts the
  blocks label as hurried (plain counting, accuracy-only weighting, no pull correction, a constant IS-25 bridge)
  diverge, which is the intended method-shortcut stump (Gate D), not an unpinned reading the files leave open (Gate
  C): the quality gap that disqualifies naive counting is itself filed in the audit.
- **Whether a "pull to the longer reply" term belongs in the forecast curve itself (7.1), contradicting its bare
  form in T:** checked against the blocks. CC1 and CC3 use the pull only to correct the *inputs to the curve fit*
  (translating IS-25 dashboard agreement and run accuracy into true technician accuracy per past run, since IS-25's
  2025 single-judge labels and the crowd's length pull corrupt the raw dashboard reading); once each past run's true
  accuracy against the standard is recovered, the forecast curve of 7.1 is applied directly in T, with no separate
  pull term, consistent with 7.1-7.3's bare form. No contradiction between the golden's measurement-correction step
  and the filed forecast function.
- **Final Recommendation ("none of the option") vs item 10's grading band (up to 30,000 of the option allowed):**
  item 10's own worked numbers show every tested option tranche strictly raises total cost (10,000 of the option
  plus 37,000 Ardentdesk costs USD 600 more; 30,000 plus 36,000 costs USD 5,400 more) against the pure-Ardentdesk
  38,000 purchase, so the single cheapest purchase under DL-03 section 5 ("the cheapest one... the purchase is
  added... at the least cost") is unambiguous; the band is ordinary estimation-noise grading tolerance around that
  one answer, not an admission of a true tie. Not a finding.

## Fix

None required. The shipped change (DL-03 v2 section 3 and new section 7) closes the forking this finding named: the
curve's form, the per-type scale with one shared bend, the ceiling fixed at 1 with its basis against the standard
filed, and the forecast pinned to the point fit rather than a bootstrap mean. No other decisive fact was moved.
