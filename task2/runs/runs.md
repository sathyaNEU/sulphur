# task2 architecture 3, platform runs (reported by the author 2026-11-08)

Scores were not reported; the author's word: "they were not stumped, model found exact ground truth". Both runs
match the golden on the call and on every graded ask figure checked below.

## Response 1 (77 resources, 19 min)

- Call: configure P0412, P0431, P0507 and P0702 for gravimetric verification of every dose; the other eight PC
  products out; GC-1 products stay on GC-1. Rates 146.21, 476.15, 262.48, 41.54 per 100,000; every other product
  under 0.2; no interval contains 10.
- Monthly station totals and the 14 product dose and set counts identical to the golden (476,230 doses, 3,198 sets).
- Method: completed doses only (1,645 aborted dropped), UTC to America/Toronto, PC-3's two serials joined, 200
  same-lot SET_UP re-logs collapsed, gross weights less tare, two superseded quarantine recounts replaced; a
  product-specific Gaussian error model against cumulative prior litres through the physical set (PC-1 to PC-3),
  a constant mean on PC-4; predicted out-of-tolerance probabilities summed over unmeasured production; 5,000
  whole-set bootstrap replicates; Q4 hold-out predictive coverage 91.44 per cent; Student-t, quadratic, set
  effects and aborted-fill throughput tried as sensitivities, decision unchanged.
- Rejected: cefoxitin only (observed failures), the crude failed-check share, pooled weights without throughput,
  issued doses as the denominator, every SET_UP as a set.

## Response 2 (62 resources, 22 min)

- Call: the same four products. Estimates 146.211, 476.147, 262.478, 42.884; lower 90 per cent bounds 97.417,
  427.577, 186.901, 16.134.
- 18 serial/product rows in the CSV, totals identical to the golden.
- Method: as Response 1 (Gaussian regression on cumulative doses on the physical set, whole-set bootstrap,
  set-held-out RMSE 0.6533 against 1.2454 for product means), Student-t heparin 1.454 still under 10.

## Diff against the golden

No cell differs. Both runs took the decisive rung (each dose rebuilt on its set at the volume the set had pumped)
as their first modelling move, on sight of the weighed doses falling with set position.
