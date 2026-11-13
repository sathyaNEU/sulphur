# task24 determinism check (pass 1)

**Verdict:** DETERMINISTIC (modelled figures not independently re-estimated; see limits)
**Disposition:** APPROVE

## Evidence
| Item | Block | Recomputed from shipped files |
|---|---|---|
| Vendor errors vs 2-of-3 technicians (no-pref set aside, Ardentdesk left/right mapped via shown_left) | item 1 grid | all 10 cells exact (e.g. TF device 41.3, AD device 13.2, TF acct 29.8, AD returns 15.2) |
| Audit structure | every pair counted | 2000 pairs x 9 judgments, 357 TF no-pref, no technician no-pref, no tied standards |
| Review accuracies | 57.7,63.8,65.8,74.5,77.8,76.0,78.9 | 57.7,63.8,65.8,74.5,77.8,76.0,78.9 (A/B and first/second mapped) |
| IS-25 dashboard for RM-22 | 65.7 | 65.7 (after dedup of re-run jobs) |
| 2027 mix weights | applied to grids | grids reproduce mix: RM-22 75.18, signed 77.37, AD40 81.14, option 78.85 |
| Cost | 38,000 x 3.60 = 136,800; option 126,000 | exact; vendor terms (AD min 10k, steps 1k, cap 120k; option steps 10k to 300k) match order and quote |
| Direct check on current model | 75.2 | reviewed RM-16 (close to RM-22 in inputs) reads 75.5 on the 2027 mix from the reviews alone; 75.2 is consistent, a 1-point shift moves the needed AD volume about 15k, inside the 18k to 61k band |

Call arithmetic from the stated grids: AD 20k 79.7, 40k 81.2 puts 81.0 at about 38k; signed plus whole option 78.9, so the option alone cannot reach the bar. Option marginal cost per point is about 56k/pt at its start (from 1.6 pts per 126k, concave) against Ardentdesk about 50k/pt near 38k. This is the thinnest part of the call (see note), but the graded item allows the band 18k to 61k and "no option", and the blocks' eight variants all stay Ardentdesk only.

## Forks run
- Standard definition (2-of-3, every pair counted): pinned by DL-03 s2; no fork.
- No-pref judgments: DL-03 s4 says not used; blocks' variant "counted" keeps the call.
- Ardentdesk left/right: pinned by shown_left; checked.
- Current-model level by reviews alone (75.5 to about 76) vs 75.2: within 1.0 on the mix; call holds (volume 30k to 38k).
- Dashboard bridge, option-by-count or accuracy weights, no pull: named in the blocks as the hurried shortcuts, each gives a different call; the files (reviews at 78.9 versus IS-25 64.8) rule out the constant bridge by data.

## Notes (no fix required)
- Modelled grids (items 3 to 9, the 80 per cent range) were not re-estimated; they are consistent with each other and with the direct review reads. Bands (2.0 per type, 1.0 mix; volume 18k to 61k) cover the review-alone and plain-rate alternatives to the reach I could test.
- Thin margin: the option's first tranche versus Ardentdesk's marginal cost near 38k are within about 10 per cent of each other, so a solver's exact optimum could include a small option volume (a few thousand USD cheaper). Item 10 grades "no option volume" exactly. If a platform run lands on a small option tranche with an Ardentdesk volume in band, consider (solution, optional) allowing "no more than 30,000 option comparisons" or stating the cost-tolerance. Not a SEND_BACK: the files' option gains are small and every disclosed variant stays Ardentdesk only.

## Fix
None required. FIX LOCATION if the optional note is acted on: solution (item 10 wording).
