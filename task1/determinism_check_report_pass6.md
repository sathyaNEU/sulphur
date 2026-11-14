# Determinism check report, task1 (pass 6)

Note: `determinism_check_report.md`, `_pass3.md`, `_pass4.md` and `_pass5.md` already exist in this folder. Per
the "never overwrite a pass" rule this is written as `_pass6.md`.

## Verdict: NOT_DETERMINISTIC

## Disposition: FIX_NOW

## 1. Pass 5's blocking finding is closed

Pass 5 failed on Gate B: `growth_policy_paid_channels_v2_2026-09.pdf` section 3 ("Bands") rendered visually blank,
so the band thresholds (cut under 0.90, hold 0.90 to 1.20, scale 1.20 or more) that every band call, the Final
Recommendation and CC3 turn on were nowhere in the pack. I unzipped `target.zip` fresh, rendered page 1 to a PNG
with PyMuPDF (`get_pixmap`, 200 dpi) and read the image directly (not just `get_text`). Section 3 now shows, in
full, both the sentence (3.1: "scale when the return is 1.20 or more, hold when it is 0.90 or more and under 1.20,
and cut when it is under 0.90") and the three-row table, matching the submission's thresholds exactly. Section 4
now reads "Zancada's records to the start of November," consistent with the exports (`attribution_installs_*`,
`ad_spend_daily_*`, `billing_events_*`, `skan_postbacks_*` all carry the suffix `2026-11-08`, i.e. through the week
of 2-8 November 2026). This part of pass 5's finding is resolved; no change needed there.

## 2. New finding (Gate C, margin/boundary fragility): AppLovin Android's own stated bands straddle the cut line

This was not checked in pass 5. I ran the identity the submission's own Step 6 uses (`installs/week x value/install
/ weekly plan spend = return`) against the **submission's own stated bands** for AppLovin Android, not an external
alternative:

- AppLovin Android 2027 weekly spend: EUR 97,000 / 52 = EUR 1,865.38.
- Q4's point installs/week: 498. Q3's point value/install: EUR 3.52. Return: 498 x 3.52 / 1865.38 = **0.940**,
  matching Q5's stated 0.94, hold.
- Q3's own stated band for AppLovin is 3.37 to 3.67 ("within 2 per cent... band in brackets"). Using the Q3
  **floor the submission itself declares acceptable**, 3.37, with Q4's point installs (498): return = 498 x 3.37 /
  1865.38 = **0.8997, under 0.90, a cut.**
- Breakeven value for the hold/cut line is EUR 3.3712 at 498 installs/week, essentially identical to Q3's stated
  floor of 3.37 (0.03 cents below it). Q5's own stated band (0.92 to 0.97) is narrower than what Q3's stated band
  would propagate: the value needed to stay at Q5's own floor (0.92) is 3.446, not 3.37. So Q3's declared "within
  2 per cent" tolerance for AppLovin is wider than the margin the hold call can absorb, and wider than Q5's own
  declared tolerance once propagated through the stated formula.
- Using Q4's own declared 6 per cent tolerance instead (point 3.52, installs at the low end of Q4's band, 468):
  return = 468 x 3.52 / 1865.38 = 0.883, also a cut, by a larger margin.

This is the Gate C margin-robustness failure the contract calls out: "the input error band is wide enough that a
gap that size is not safely calculable, i.e., the margin sits inside modeling noise." AppLovin Android's return sits
0.040 above the cut line (0.94 vs 0.90), but the submission's own declared tolerance on the input that feeds it
(Q3's 2 per cent band) is wide enough to erase that entire margin and cross the line, which no other channel's row
does (every other channel's stated band stays clear of both 0.90 and 1.20 under the same test: Meta iOS 1.01-1.07,
TikTok iOS 0.74-0.81, Apple Search Ads 1.42-1.55, Meta Android 1.05-1.12, Google Android 0.96-1.15, TikTok Android
0.70-0.74, all comfortably inside their called band with no combination of their own stated tolerances reaching a
threshold). This is distinct from, and in addition to, the CC1 proportional-spread alternative (0.84, cut), which
the submission itself names and closes with the near-zero late-recording fact (0.52 per cent of billing events have
`recorded_at` after `last_open_at`, which I re-confirmed on the rebuilt pack): that fork is closed by named data and
is not the issue here. The issue here is that the **golden's own named method's stated grading tolerance**, taken
at its own declared edge, independently produces the losing call.

I could not fully rebuild the generator's exact global fit (the trial-conversion share 0.113 and monthly
continuation 0.889 fitted jointly against store/product/month totals) within budget to determine whether a
by-store or own-first-month refit of those two shared parameters would itself land AppLovin below 3.37; a rough
proxy count of "last open before an active subscription's next due charge" gave 18,214 against the stated 20,336
(close, consistent with the stated method being reproducible), but a parallel proxy for the trial pool did not
reproduce the stated 36,218 closely enough to use for a sensitivity run, so I did not rely on it. The finding above
does not need that rebuild: it is a direct arithmetic consequence of the bands as stated in `submission.md`.

## 3. Other load-bearing figures recomputed and confirmed

| Figure | Submission | My recompute | Result |
|---|---|---|---|
| Q2 installs, AppLovin/ASA/Meta Android/Google Android/TikTok Android | as stated | exact match (attribution export, first install, consumer accounts, 4 Nov 2024-2 Nov 2025) | exact |
| Q2 installs, Meta iOS | 17,810 | 17,669 (SKAN postbacks, `ad_network`) | inside 2% band |
| Q2 installs, TikTok iOS | 11,504 | 11,416 (SKAN postbacks) | inside 2% band |
| CC1, Apple Search Ads 12-month net rev/install | 14.63 | records-only 12.02; 12.02 / (1 - 0.178) = 14.62 | matches to the cent via the stated 17.8% missing share |
| CC1, AppLovin Android 12-month net rev/install | 3.52 | records-only 2.17; 2.17 / (1 - 0.383) = 3.52 | matches exactly via the stated 38.3% missing share |
| CC1, overall store excess vs records | 40.1% | 41.4-41.6% (billing records, production only, VAT/commission per policy 2.4, vs Apple `developer_proceeds_eur` and Google Play `net_eur` row totals, both already net per the same formula, Nov 2024-Nov 2026) | close but not exact (about 1.3-1.5 points high); does not change any threshold, not independently re-derivable to the stated precision in budget |
| CC3, Google Android average 2027 weekly spend | EUR 3,947 | 205,240 / 52 = 3,947.69 | matches |
| CC3, Google Android declining spend-value relationship | correlation -0.61, 53 mature weeks | reproduced: correlation -0.6126, 53 mature weeks, clear negative slope (records-only value/install falls from about 6.3 at EUR 2,700/week spend to about 4.2-4.7 at EUR 5,000+/week), plan's EUR 3,947 inside the observed 2024-26 range | confirms hold over scale; flat-value rival (which would give ~1.28, scale) is ruled out by this slope, as pass 5 found |

## Fix

**Where:** `solution` (`submission.md`), not the prompt or the pack. The underlying data, method and golden figures
are sound and reproduce; the problem is the stated tolerance on one row.

**What:** Tighten Q3's band for AppLovin Android so it no longer reaches the hold/cut boundary once propagated
through the stated return formula, e.g. to something like 3.45 to 3.67 (consistent with Q5's own stated floor of
0.92 and a return comfortably at or above 0.90 under Q4's point installs), and correspondingly narrow Q4's band or
Q5's band for AppLovin so the three are mutually consistent with the "hold" call at every combination a solver
could reasonably read as within the stated tolerances. No other channel's row needs this (all six others hold
their called band under the same propagation test). This is an answer-block precision fix only; it does not change
what solvers see in the prompt or the pack.
