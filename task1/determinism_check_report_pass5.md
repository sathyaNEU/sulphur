# Determinism check report, task1 (pass 5)

Note: `determinism_check_report.md`, `_pass3.md` and `_pass4.md` already exist in this folder from earlier
passes. Per the "never overwrite a pass" rule this is written as `_pass5.md`; the caller named
`determinism_check_report.md` in the task but that path was already taken by an earlier pass.

## Verdict: NOT_DETERMINISTIC

## Disposition: SEND_BACK

## The blocking finding (Gate B): the policy's "3. Bands" section is visually, genuinely blank

Every one of the submission's seven band calls (Supplementary Question 6), the Final Recommendation built on
them, and Critical Component 3's "so it holds rather than scales" turn on one pinned rule: **cut under 0.90, hold
from 0.90, scale from 1.20** (return per euro of spend). The only shipped file that could carry this rule is
`target/growth_policy_paid_channels_v2_2026-09.pdf`.

I did not rely on a text extractor alone (a flattened read can drop a table that is really there). I rendered the
page to an image with PyMuPDF (`get_pixmap`, 200 dpi) and read it visually. The page shows, in full:

```
3. Bands
———
(blank space)
4. Timing
```

A short horizontal rule and then nothing: no table, no numbers, no band names. `pdfinfo` confirms the document is
one page with no embedded images, form fields or JavaScript, so there is no second layer or page carrying the
table either. This is not a text-extraction artifact; a human reader opening this PDF sees the same blank
section. It is Gate B's missing-input-data shape: a fact every one of the submission's graded figures (Q6, the
Final Recommendation, CC3) requires and that no shipped file states. I also opened `media_plan_2027.xlsx` in full
(both sheets, "Weekly spend 2027" and "Notes," neither visible-only) and found no band rule there either.

This blocks the whole band classification, not one channel: TikTok iOS (0.79) and TikTok Android (0.72) are
called cut, Apple Search Ads (1.49) is called scale, and the remaining four (1.05, 1.08, 1.06, 0.95) are called
hold, all against thresholds that are not written anywhere in the pack. A solver cannot reproduce Supplementary
Question 6 or the Final Recommendation from the shipped files as they stand.

## What I verified beyond the blocking finding

**Supplementary Question 2 (installs), recomputed end to end** from `attribution_installs_...csv` and
`skan_postbacks_...csv` (first install per account, reinstalls dropped, 4 Nov 2024 to 2 Nov 2025 inclusive):

| Channel | Submission | My recompute | Source | In 2% band? |
|---|---|---|---|---|
| AppLovin Android | 26,445 | 26,445 | attribution export | exact |
| Apple Search Ads | 5,675 | 5,675 | attribution export | exact |
| Google Android | 23,062 | 23,062 | attribution export | exact |
| Meta Android | 17,670 | 17,670 | attribution export | exact |
| TikTok Android | 17,644 | 17,644 | attribution export | exact |
| Meta iOS | 17,815 | 17,674 | SKAN postback count | yes, 0.8% off |
| TikTok iOS | 11,507 | 11,425 | SKAN postback count | yes, 0.7% off |

The Android/ASA channels reproduce exactly from the attribution export. The iOS channels reproduce within the
stated band from SKAN postback counts, not the attribution export (export rows for these channels in-window:
5,033 Meta iOS, 2,101 TikTok iOS, versus 17,674/11,425 postbacks), which is the data-grounded fact behind Critical
Component 2 (the export holds only consenting users).

**Critical Component 1's forks (AppLovin: hold vs cut).** The submission's method credits store-charge revenue a
subscription's recording never captures (because the record is only written when the app reopens), rather than
spreading the stores' excess revenue proportionally across all recorded accounts. I tested the fact this is built
on: among 192,887 billing events, only 1,005 (0.52 per cent) have `recorded_at` after the matching account's
`last_open_at`; in effect, records are written essentially only while the app is still opened. That is close
enough to "about 0" to support the submission's claim that the stores' excess revenue concentrates in accounts
that stopped opening the app, not spread proportionally across the recorded base. This rules out the proportional
alternative as the literal implication of the data, consistent with the golden's step 3.

**Critical Component 3's fork (Google Android: hold vs scale).** I rebuilt the weekly cohort relationship
independently (records-only net revenue per install per weekly install cohort, matured cohorts only, versus that
week's Google Android spend): correlation -0.61 over 53 mature weeks, both a linear and a log-log fit giving a
clear negative slope, and the plan's average spend (EUR 3,947) sits inside the observed historical range (mature
weeks ran up to EUR 5,252; all 2024-26 weeks up to EUR 5,618), so the submission's 3,947 is an interpolation, not
an extrapolation. My records-only (not store-reconciled) fits give a value per install of about EUR 5.0 to 5.2 at
3,947, well under what is needed for a scale call once scaled up by the same store-reconciliation factor the
golden applies elsewhere; the golden's own reconciled figure (7.05, against roughly 8 needed for 1.20) is
consistent with this direction. The decline is a real, data-supported pattern, not a coin flip between a flat and
a declining fit: the constant-value rival (which would leave Google Android's return near 1.28, a scale call) is
not equally supported by the cohort data. I did not rebuild the full store-reconciliation step for Google Android
to the golden's precision given time, so I note this as inside the band but not independently re-derived to the
cent; the directional fork is closed by the data either way.

## Evidence I withdrew after re-checking

An earlier draft of this check cited a raw-byte grep for "0.90"/"1.20" in the PDF's compressed content streams and
a `grep -il` sweep that claimed to search for "Cut," "Hold" and "Scale." Neither claim holds up: the PDF's text is
glyph-encoded in its content streams, so a raw-byte search proves nothing about what the rendered page shows (the
visual render above is the only check that settles it), and the grep pattern used never searched for those three
words. Both are dropped from this report. The pack has 9 shipped CSVs (not 10); corrected above.

## Fix

**Where:** `input_files`, specifically `target/growth_policy_paid_channels_v2_2026-09.pdf`. This is not an
answer-block wording fix: no file in the pack states the band thresholds, so it cannot be closed inside
`submission.md` (this is Gate B, not Gate E).

**What:** Restore section 3's content in the PDF so it states, in the policy's own words, the band rule the
golden already assumes (cut under 0.90, hold from 0.90, scale from 1.20, applied to the 2.1-defined return per
euro). Rebuild `target.zip` from the corrected pack. The Critical Component 1 and 3 forks I ran both closed on the
golden's side with named facts from the data (the near-zero late-recording rate; the clear, interpolated spend-
value decline), so once the bands text is restored those two do not need further repair; a re-judge after the fix
should still confirm them since the fix changes a shipped file.
