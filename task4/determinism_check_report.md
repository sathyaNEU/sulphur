# Determinism check: task4 (architecture 13, Wrenfold Brewery 2027 keg order)

Scope: Gates A to E only (`guidelines/determinism_judge_system_prompt.md`). Verified against a fresh unzip of
`target.zip` (sha256 487a6d6...), `prompt.txt` and the four answer blocks of `submission.md`.

## Verdict: DETERMINISTIC

## Disposition: FIX_NOW

## Evidence

### Figures recomputed

| Figure | Blocks' value | Recomputed | In band? |
|---|---|---|---|
| Fills in the year to 2026-11-30 (50/30/20) | 215,880 / 117,218 / 30,240 | 215,880 / 117,218 / 30,240 (`filling_log...csv`) | exact match |
| Own kegs back at washer net of repairs re-presented | 214,849 / 116,649 / 29,828 | 214,849 / 116,649 / 29,828, from `washer_log...csv` (washed_ok+rejected_to_repair+condemned_at_inspection) minus `keg_repair_jobs...csv` REPAIRED jobs with `back_to_washer` in the year | exact match |
| Fills minus own-back (pre-RFID-term loss) | implied 1,031 / 569 / 412 | 1,031 / 569 / 412 | consistent with filed loss of 1,210/630/170 once the RFID kegs-out term (−179/−61/+242) is added |
| Usable fleet (SQ3), from the stated levels of kegs out (14,120 / 8,750 / 3,070) | 18,530 / 10,880 / 4,290 | clean empties (4,322/2,072/1,209) + repair cage (83/56/12) + kegs out (14,120/8,750/3,070) = 18,525 / 10,878 / 4,291 | inside band (18,140-18,900 / 10,660-11,140 / 4,200-4,380) |
| Order (50/30/20) from need minus (fleet minus carried loss) | 2,090 / 3,230 / 1,130 | 19,800−17,720=2,080; 13,670−10,440=3,230; 5,320−4,190=1,130 | inside band (rounding of unrounded inputs) |
| Maplestead pubs population | SQ5: "held at the Maplestead pubs" | `plan_2027.xlsx` "Maplestead pubs" sheet is pub-level only (no customer/account rows outside the 300 pubs); matches the ask's population exactly. "Kegs on the way" in CC3 belongs to the named *rival* (turns) method, not the graded figure | filed, no fork |
| Foundry range population | SQ6/CC4 | `plan_2027.xlsx` "Foundry range" (18 beers, 200-keg lots, on_sale_from/to windows) and "Foundry brews" give the racking/brew-plan basis directly | filed |

### Fork run: RFID "kegs out" scaling basis (the term that decides SQ3/CC1 and the order)

I rebuilt the kegs-out term from `keg_rfid_reads_2025-06_2026-11.csv`, `keg_register_2026-11-30.xlsx` (`Kegs`,
`Lots`, `Tag changes`) and `filling_log...csv`. A literal "last RFID event = FILL or DELIVER ⇒ still out" reading
initially gave a *rise* in tagged kegs out for every size (+313/+132/+409), the opposite sign from the blocks'
implied fall for 50 and 30 litre. That reading is ruled out by filed text, not a live fork: standard §2.1 ("a keg
that will not come back is not part of the fleet") and Step 3 ("tagged kegs out ... that will come back") exclude
kegs lost in the trade from "out"; my literal state machine was carrying every tagged keg lost since the RFID
rollout (2025-06-01) as permanently "out", which inflates the later date more than the earlier one (left-censoring
grows with lookback). Once lost kegs are excluded (an open trip is only "out" if it is later observed to return,
per Step 3's own wording), the gap closes: the residual between my raw rise and the blocks' implied rise matches
the tagged share of fills times the stated loss almost exactly for all three sizes (e.g. 50 L: 363 raw-gap vs
0.278 × 1,210 ≈ 337), which is the fingerprint of exactly this carry-forward error, not of an unpinned method
choice. **This fork is closed by filed text; not a finding.**

A second, live fork remains: **which tagged share to scale the raw tagged-kegs-out count by.**
- Scaling by the *tagged share of the year's fills* (0.2785 / 0.2281 / ~1.0, computable from RFID `FILL` reads
  against `filling_log...csv`) reproduces the blocks' stated levels (14,120 / 8,750 / 3,070) and keeps SQ3 and the
  order inside band, as shown above.
- Scaling by the *tagged share of the active register fleet* instead (0.2687 / 0.2208 / 1.0, computable from
  `keg_register_2026-11-30.xlsx` "Lots" and "Kegs") is an equally defensible, equally filed basis for the same
  extrapolation (a stock-based share rather than a flow-based share). It raises the 50 litre kegs-out level from
  14,120 to about 14,640 (ratio 0.2785/0.2687), pushing the 50 litre usable fleet to about 19,040, 140 kegs above
  the stated band's top of 18,900, and moving the order below the band's low end accordingly for 50 litre.
- Nothing in `keg_fleet_standard_issue3.pdf` or `plan_2027.xlsx` names which share basis to extrapolate a tagged
  sample to the full fleet by; the Step-by-Step's own wording ("scaled by the tagged share of fills") is the only
  place the convention is written down, and the Step-by-Step is an answer block, not an input a solver sees before
  answering. A careful analyst working from the pack alone could reasonably pick either share and, on the 50 litre
  size, land outside the stated band.

No other graded figure's band is at risk from this fork: 30 and 20 litre stay inside their bands under either
share basis (the ratio difference is too small relative to their wider bands), and it does not reach the Final
Recommendation's call (order all three sizes) under either reading.

### Other gates
- Gate B (filed facts): every distinctive term in the Final Recommendation and Critical Components (register vs.
  usable fleet, gate counters vs. trade loss, Maplestead pub-level turns, the Foundry range's 200-keg lots) traces
  to a named file and sheet; no missing fact found.
- Gate D/E (the asks): each ask in Supplementary Questions pins one population, one unit (kegs) and one precision
  (nearest ten); no ask splits on a reading rather than the data.

## Fix

**Where:** `input_files` (`keg_fleet_standard_issue3.pdf`, §4.6) or, failing that, the SQ3 band in `submission.md`.

**What:** Add one sentence to §4.6 of the keg fleet standard pinning the extrapolation basis, e.g.: "RFID-tagged
counts are scaled to the whole fleet by the tagged share of the size's fills over the same period, not by the
tagged share of the active register." This closes the fork with a filed convention rather than leaving it to the
Step-by-Step alone. If the author prefers not to touch the standard, widen the 50 litre usable-kegs band in SQ3
from 18,140-18,900 to about 18,140-19,050 and the order band in SQ1 correspondingly, so the register-share reading
also lands inside.
