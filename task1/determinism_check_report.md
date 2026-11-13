# Determinism check — task1 (architecture 5, 2026-11-13 cut)

This report replaces the prior pass, which described an earlier cut; the world, the call and every figure have
changed since. Verified fresh against `prompt.txt`, `submission.md` and a clean unzip of `target.zip`.

## Verdict: NOT_DETERMINISTIC
## Disposition: SEND_BACK

## Why

The Final Recommendation turns on Gezin's rise clearing a positive net effect (EUR 6.1 per October subscription,
band 2.5 to 6.4). That figure is not robustly forced: the same method the blocks themselves use to value the
December-bill response to the price e-mail on Flex and Onbeperkt — average the plan's own two historical January
rises' extra cancellations at the December bill, valued (per Step 6) as "light listeners worth the whole of
2027" — reproduces Flex's 14.2 and Onbeperkt's 7.0 almost exactly, and, applied the same way to Gezin, yields a
materially non-zero December response that the golden appears to treat as zero (Critical Component 2 and the
Step-by-Step mention it only for Flex and Onbeperkt). Carried through at the filed valuation convention, it erodes
Gezin's +6.1 to roughly 0.2–1.4 EUR/subscription — outside the stated band floor of 2.5 and close enough to zero
that the sign is not safely forced. This is a Gate A/C problem on the single most heavily weighted figure, not a
wording issue, so the fix is not a one-line answer-block edit.

## Evidence

### Reproduced cleanly (no finding)

| Figure | Blocks' value | My recomputation | Method |
|---|---|---|---|
| Paying base 31 Oct 2026 by plan | Flex 697, Standaard 1,222, Onbeperkt 1,461, Gezin 1,010; 4,390 | Exact match | Consumer accounts with an October 2026 charge whose status is `collected` **or** `re-presented` (guideline 3.1: "a charge returned and **not re-presented**, or refunded, is not collected" — re-presented alone counts). `collected`-only gives 4,342, ruled out by that sentence. |
| Past rises' first-bill extra cancellations (Step 3) | crossing: 14.4, 10.9, 27.0; non-crossing: 5.3, −0.8, 1.8, 2.7, 2.6 | 14.40, 10.92, 26.96; 5.3 (STD BE), −0.8 (GEZ NL), 1.8 (STD NL), 2.7 (ONB NL), 2.6 (FLEX BE) | Each plan-region's one January rise (2025 or 2026) vs the same plan in the other region, same calendar months, difference in (no-next-month-charge) rate. |
| 2027 crossing classification | Standaard crosses the rival in both NL and BE; Flex, Onbeperkt, Gezin cross nowhere | Confirmed from `price_list_2027.pdf` (2027 and 2026 prices) against the October 2026 row of `rival_price_scan...csv` (no promotion flags that month), with the rival plan pinned by matching listening-hours/profile caps (Flex→Basis 10h, Standaard→Plus 30h, Onbeperkt→Onbeperkt, Gezin→Familie) | Forced by filed numbers once the rival mapping is pinned by hours, which it is. |
| December-bill extra cancellations after the e-mail, Flex and Onbeperkt | Flex 14.2, Onbeperkt 7.0 | Flex: avg(12.07 crossing-NL-2025, 16.29 non-crossing-BE-2026) = 14.18. Onbeperkt: avg(6.94 crossing-BE-2025, 7.09 non-crossing-NL-2026) = 7.02 | Plan's own two historical rises averaged, Nov→Dec extra cancel rate vs same-months other-region control. This is the method I then applied to Gezin (below). |

### The blocking finding: Gezin's December response

Applying the identical, just-validated method to Gezin's own two historical rises (NL Jan 2025, BE Jan 2026):

| | GEZ NL (email Dec 2024) | GEZ BE (email Dec 2025) | Average |
|---|---|---|---|
| Extra Nov→Dec cancel per 100 | 3.22 | 1.49 | **2.36** |

Not zero, not noise-sized next to Flex's 14.2 and Onbeperkt's 7.0 that the same arithmetic reproduces almost
exactly. I also checked these leavers are the "light listeners" Step 6's valuation convention names: average
counted monthly hours (proxy: `listening_monthly` seconds_streamed) in the month before leaving is lower than
stayers' in both cohorts (NL: leavers 20.4 h vs stayers 23.1 h; BE: leavers 12.0 h vs stayers 23.2 h), so Step 6's
"worth the whole of 2027" applies to them, not the cheaper, remuneration-heavy valuation used for crossing-driven
heavy-listener leavers.

Rough sizing: 2.36 per 100 of Gezin's 1,010 October base ≈ 23.8 extra December leavers; valued at roughly a year's
net contribution each (net-of-VAT EUR 21.09/month, minus a modest store-fee blend and light remuneration) ≈
EUR 200–250 per leaver ⇒ about EUR 4,700–6,000 total, i.e. roughly EUR 4.7–5.9 per October subscription. Against
the filed +6.1, that leaves Gezin at roughly **0.2 to 1.4 EUR/subscription** once this effect is folded in —
outside the stated band (2.5 to 6.4) and uncomfortably close to zero given the width of my own estimate. I did not
build the exact counted-hours pipeline (B2.2 running-maximum-of-position-reached) to pin this to a point figure;
that refinement belongs to whoever repairs it, not to this check. What is established is that the effect is real,
reproducible by the blocks' own stated method, and large enough relative to Gezin's margin that the call is not
safely forced as written.

### FIX_NOW band findings (do not move the call)

Both of these were found while stress-testing item 5/6's bands with the same reproducible per-100 figures above;
neither threatens Flex, Standaard or Onbeperkt's own (clearly negative) calls.

- **Standaard, items 5 and 6 (cancellations and downgrades).** The forecast figures (21.2 cancel, 16.1 downgrade,
  both regions) sit inside the stated bands (17.7–22.3; 14.2–18.6) only under some aggregations of the historical
  crossing analogs, not others. A plain, equally reasonable average of the three crossing analogs (Flex NL 10.9,
  Onbeperkt BE 14.4, Gezin BE 27.0) gives 17.43 (misses the cancel floor by 0.27); the n-weighted pooled rate gives
  15.85 (further out). For downgrades, the same-size-only pair (Onbeperkt, Gezin; Flex structurally has no plan
  below it) averages 13.75 against a floor of 14.2 (n-weighted gives 15.38, inside). Recommend widening the floors
  to cover these reasonable alternatives (e.g., cancel floor to ~15.5, downgrade floor to ~13.5), or stating in the
  blocks which weighting is intended. Standaard's own recommendation is unaffected: even the lowest reasonable
  cancel estimate leaves Standaard's 2027-contribution figure deeply negative, though its own stated band
  (−16.4 to −14.0) likely needs a wider upper edge past −14.0 to stay consistent.
- **Gezin, items 5 and 6 (own non-crossing rise, "carries at the size it was read").** Taking Gezin's own
  non-crossing historical response at face value (as Step 4 licenses for non-crossing plans) gives −0.8 cancel and
  −0.9 downgrade (negative, i.e. fewer than the no-rise counterfactual), both outside the stated −0.3 floor for
  Gezin's 2027 figures. These push Gezin more positive, not less, so they do not touch the call; widen the floor to
  about −1.0 or state a zero floor explicitly.

### Forks run and closed by named facts

- **Which rival plan is "comparable."** Pinned by `price_list_2027.pdf`'s listed hours and profile counts against
  the rival scan's named plans (10h→Basis, 30h→Plus, unlimited/2 profiles→Onbeperkt, unlimited/4 profiles→Familie).
  No alternative mapping is defensible given the hours match exactly.
- **Scan month for the 2027 decision.** Guideline 3.8 pins "rivals' prices as last scanned" = October 2026; that
  row carries no promotion flag, so there is no live fork between the raw October row and a "with promotions
  excluded" reading — they coincide.
- **"Crossed the rival" vs "ended up above the rival."** I ran both readings. Under "ended up above," Flex BE 2026
  (old 9.49, new 9.99, rival 9.39 — already above before the rise) and Onbeperkt BE and Gezin BE would also count
  as "above," which is a different and looser test than "newly passed it." This reading is ruled out by Flex's own
  2026 BE rise: it ended up above the rival (9.99 > 9.39) exactly as it had been before (9.49 > 9.39), and its
  first-bill extra cancellation (2.6, non-crossing bucket) sits with the non-crossing group, not the crossing group
  — so the data itself distinguishes "newly passing" from "already past," and only the former produces the large
  response. Guideline 3.10's and Step 4's "took the price past the rival" / "passes it nowhere" language matches
  the newly-crossing reading, and only that reading is consistent with the magnitudes in the files.
- **Guideline 3.10's two sentences.** The first ("a rise goes ahead... when it raises the 2027 contribution...
  followed through 2027") is the decision test; the second ("a rise's extra cancellations and extra downgrades are
  those at a subscription's first bill...") only defines the items-5/6 figures. They do not conflict, and Step 8's
  "stopping at the first bill" shortcut is correctly named as a shortcut, not a second defensible reading of the
  decision rule.
- **Item 7's "still paying on any plan."** Pinned by the prompt's own wording ("still be paying on any plan"); an
  own-plan-only reading is explicitly ruled out by that phrase.

### Not independently recomputed (say so plainly)

- **Item 2 / Critical Component 1, the full EUR 6.1 / −4.4 / −15.5 / −5.9 netting.** I verified the three
  reproducible inputs that feed it (first-bill crossing response, December-email response, crossing classification)
  and found the Gezin blocking issue above; I did not rebuild the full contribution model (counted-hours-by-profile
  via B2.2's running-maximum-of-position-reached, remuneration, store fees, downgrade valuation at EUR 67.7) end to
  end. Gate A on this figure is partial, not confirmed.
- **Item 7, the end-of-2027 still-paying counts (Flex 149, Standaard 279, Onbeperkt 700, Gezin 660).** Not
  recomputed; flagged as unverified, not as reproduced.

## Fix

**Fix location: solution**, pending the author's own recomputation — this is not a prompt or input-file defect;
every fact needed (the two Gezin historical rises, the e-mail date, the light-listener hours) is already shipped.
Two possible outcomes once the December effect is folded into Gezin properly:
1. Gezin's net figure stays positive but moves down, inside a widened band — then this is a solution-only fix
   (recompute item 2's Gezin figure and item 5's Gezin December line, re-band it, keep the recommendation).
2. Gezin's net figure goes to zero or negative — then the recommendation itself changes (no rise goes ahead, or a
   different plan does), which is a bigger rewrite of the Final Recommendation, Step-by-Step and Critical
   Component 1/2, still within `solution`/`submission.md`, no change to what solvers see in `target.zip` or
   `prompt.txt`.

Also apply the two FIX_NOW band widenings above (Standaard items 5/6 floors; Gezin items 5/6 floor) in the same
pass, since they are cheap and were found during the same recomputation.

## Pass 2 (2026-11-13)

## Verdict: DETERMINISTIC
## Disposition: APPROVE

### Why

Pass 1's blocking finding was that the blocks were silent on whether Gezin's December-bill response to the price
e-mail was included in its +6.1 figure, and that the same method the blocks used for Flex and Onbeperkt, applied to
Gezin, gives a non-trivial response that could erode the call below its band. The blocks now state this explicitly
(Critical Component 2 and Step 5 list Gezin's December rate, 2.4 per 100, beside Flex 14.2, Standaard 8.5 and
Onbeperkt 7.0; Step 6 states leavers at the e-mail are valued at "what an October subscription on the plan brings
in 2027 at the held price, on the plan's continuation by tenure and their own listening", not a full year). This
closes the Gate A/C gap: the fact is now filed, and both the rate and the valuation convention reproduce.

### Evidence

| Figure | Blocks' value | My recomputation | Method |
|---|---|---|---|
| December-bill extra cancellations, all four plans | Flex 14.2, Standaard 8.5, Onbeperkt 7.0, Gezin 2.4 | Flex 14.18, Standaard 8.11, Onbeperkt 7.02, Gezin 2.36 (Standaard and Gezin newly rechecked this pass; Flex and Onbeperkt reproduced in pass 1) | Each plan's two historical January rises' Nov-to-Dec extra-cancellation rate vs the same plan in the other region over the same months, averaged. All four land inside rounding of the filed figures. |
| Value per Gezin December leaver, continuation-by-tenure convention | Not stated as a point figure (feeds item 2's EUR 6.1) | Approx EUR 128 per leaver (held-price net revenue ~EUR 19.8/month less ~EUR 6.5/month remuneration on the leavers' own lighter listening (~16h), times an expected 9.6 of 12 months paid in 2027 from an empirical tenure-indexed survival curve built on `plan_periods...csv`'s historical Gezin episodes) | Same convention Step 6 states: held price, own listening, continuation by tenure (not a full year). |
| Impact of Gezin's December leavers on its per-subscription net | Implied by the task's framing: about +8.8 without them to the stated +6.1 (an effect of about -2.7) | About -3.0 to -3.1 (128 EUR/leaver x ~24.2 extra leavers (2.4/100 of 1,010) / 1,010 subscriptions) | Same arithmetic, independently built. |

The continuation-by-tenure convention (expected ~9.6 of 12 months, not 12) matters: using it, my own recomputation
lands within about 15 per cent of the stated ~2.7 effect, materially smaller than pass 1's cruder "worth a full
year" estimate (which gave EUR 4.7-5.9, i.e., a bigger bite). Net Gezin figure under either my estimate (8.8 - 3.0 =
5.8) or pass 1's cruder full-year estimate (8.8 - 4.7 to 8.8 - 5.9 = 2.9 to 4.1) lands inside the stated band (2.5 to
7.8) and stays clearly positive, so the call (Gezin only) holds under both the correct convention and a sloppy
reading of it; the fork pass 1 flagged is closed, not merely narrowed.

### FIX_NOW band findings from pass 1, rechecked

- **Standaard, items 5/6.** Floors widened to 16.4 (cancel) and 13.0 (downgrade). The plain, unweighted mean of the
  three crossing analogs (Flex NL 10.9, Onbeperkt BE 14.4, Gezin BE 27.0) = 17.43, now inside 16.4-22.3 (it missed
  the old 17.7 floor by 0.27). The same-size-only downgrade pair (Onbeperkt, Gezin) = 13.75, now inside 13.0-18.6.
  An n-weighted pooled rate (15.85 for cancellations) would still sit outside 16.4, but the blocks' own stated
  convention is consistently an unweighted mean (Step 5: "the mean of the plan's own two rises"), never an
  n-weighted pool, so this is not an equally reasonable neighbour and does not reopen the fork. Standaard's own
  2027-contribution band is now -16.4 to -12.4 (widened from -16.4 to -14.0 in pass 1's reading), which comfortably
  covers the lower cancel/downgrade estimates; Standaard's call (hold) is unaffected regardless.
- **Gezin, items 5/6 (first-bill, non-crossing).** Floors widened to -1.1 (cancel) and -1.2 (downgrade). Gezin's
  own non-crossing historical first-bill reading (-0.8 cancel, -0.9 downgrade, from NL's historical non-crossing
  rise) now lands inside both. Resolved.

### Not rechecked this pass (unchanged from pass 1, not touched by the described changes)

Item 2/Critical Component 1's full netting (remuneration, store fees, downgrade valuation at EUR 67.7, the
counted-hours pipeline via B2.2) was not rebuilt end to end in either pass; this pass only checked the piece that
changed (the December response's rate and valuation convention) and found it reproduces and keeps the call inside
band. Item 7's still-paying counts remain unverified as in pass 1.

### Fix

None required. The pass 1 SEND_BACK is lifted: the previously unfiled fact (whether Gezin's December response is
counted, and how it is valued) is now filed in Step 5, Step 6 and Critical Component 2, reproduces independently,
and the resulting figure stays inside its stated band under both the filed convention and a cruder neighbour of it.
Both FIX_NOW band findings from pass 1 are resolved by the widened bands now shipped.
