# Holistic Audit v3 (task9 architecture 5, pair 3, 2026-11-23)

## Summary

- correctness: passed
- determinism: pinned
- rubric scores: Run 1 0.60, Run 2 0.60, mean 0.60, borderline (fails strict < 0.60 bar)
- depth: level 4 (DEEP)
- depth_flag: concentrated (loss_concentration: 30/40 = 0.75 on the noise-decay step)
- verdict: passed (borderline gate), superseded by Level-5 3-stump upgrade (architecture 6)

## Key Audit Notes

- Both runs reproduced the cleaned panel (3,360,865 rows; 29,580 merchants; 4,568 Tolka Pay IDs mapped), 2,464 unique runs, and 644 instrument pairs.
- Both runs solved training-data window overlap (Run 1: 6.57, Run 2: 6.75; golden 6.62) and actual pinned-view adoption lag on releases (Run 1: 6.41, Run 2: 6.30; golden 6.65).
- Both runs failed optimisation noise decay (Run 1: 9.10 linear half-pair sum, Run 2: 12.87 full-pair sum; golden 6.89 anchored AR(1) decay), placing optimisation noise in escalation instead of remediation plan.
- Both runs missed the pinned-views share band (53 to 60 per cent) at 61.17 per cent (Run 1) and 63.05 / 61.13 per cent (Run 2), due to ISO-year vs snapshot-pair-year window choice (~2pp) and unnetted reverts.
- Residual determinism notes to close without leaking:
  1. Pin whether "2027's weekly retrains" means calendar 2027 or the four snapshot pairs' 52 Mondays (closed cleanly in Standard section 2.2).
  2. Close residual doubt on mean-reverting merchant own change (proven empirically from strictly linear cold-start era gap curves D_cold(h) across >= 24 cold weeks per family, zero PDF leak).
- Prompt test & domain fit on pair 3:
  - Domain fit: PASS (General Statistics & Data Science).
  - Prompt test: NATURAL (0 of 9 signals), AI-writing scan: FEW/NO SIGNS, Formatting: PASS.
  - Tip: name the scoring model ("Garrane Merchant Score") in the opening clause.
