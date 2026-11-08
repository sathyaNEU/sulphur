# task3 architecture 3 triage (2026-11-08)

- Run 1 (`runs/run1.md`): score not reported, on the golden: Schedule C at 1,000 gpm, every 2046 maximum (4, 6, 8 and
  10 ft), DW-17 at 7 ft and Mill Street's 2025 effect at MS-MW at 5 ft; first wrong step: none. It fitted a leaky strip
  with the plate's walls to the test (T 8,009 ft2/day, S 0.0010059, leakage factor 3,458 ft) and took CV-02 and CV-11
  as the natural-level controls.
- Run 2 (`runs/run2.md`): score not reported, on the golden on the call and every graded figure; first wrong step:
  none. The same leaky strip fitted through pumping and recovery (T 8,004 ft2/day, B 3,504 ft) and the same two remote
  controls with pre-Mill offsets.
- Average: not reported (both runs on the golden; the generated rubric grades both near 100).
- Counterfactual average: the same (no surface or formatting loss to give back).
- Reading the landed call (build-pipeline, Stage 6): both runs took the decisive rung as their first modelling move.
  The far field the test could not see was identifiable from the test itself once the plate's walls were honoured,
  and remote same-aquifer wells outside the cone are the hydrogeologist's default control, so the contaminated-control
  trap (CV-07) was never entered. Not a missed rung, not a declined rung, not an announced work order: the deep step
  itself is spent.
- Verdict: **REDESIGN**. One platform round, both runs on the golden at every ask; one architecture per world, so the
  re-root moves to another world, dataset and shell (architecture 4).
