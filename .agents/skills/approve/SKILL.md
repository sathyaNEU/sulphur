---
name: approve
description: Pre-upload sign-off on a built Sulfur task. Checks the heart of the stump against every card and ledger row for duplicates/templates, re-runs the surface screen, precut/effort/voice gates, refuses any LEAK, verifies container hygiene on both ZIPs, and on PASS records the approval in pipeline.json and updates the fingerprint card.
---

# /approve

Run the pre-upload sign-off for the specified task (`taskNN` at the repository root holding `AGENTS.md`). If no task is named, ask and stop.

Run these checks in order and stop at the first failure:

1. **The heart check:** `python3 .agents/skills/fingerprint/guard.py heart <task>`. Exit 1 is a BLOCK (relay nearest builds and axis to redraw). A WARN is relayed with the design note's one-line differentiation. Fill empty `stump`/`driver` fields first and run `guard.py validate <task>` if needed.
2. **The surface screen:** `python3 .agents/skills/fingerprint/guard.py surface <task>`. A promoted pair requires rename/regeneration before approval.
3. **Paper gate, effort test, and prompt gate:** `python3 .agents/skills/stumping/precut.py <task>` exits 0 (includes `voice-check.py` and `effort.py`). Flag any retired single-deep-step `doctrine` WARN plainly.
4. **The leak report:** `<task>/leak_check_report.md` must exist and must not read `LEAK`. If missing, run `python3 .agents/skills/leak-check/leak.py <task> --quiet`. Every `REVIEW` line must be answered in `DESIGN_NOTE.md`.
5. **Results chain & effort table:** `DESIGN_NOTE.md` carries `## Results chain`, `## Hidden factor record`, and `## Effort test`, agreeing with `python3 .agents/skills/stumping/effort.py <task> --check-note`.
6. **The container gate:** `python3 .agents/skills/reduce-house-fixes/scripts/audit_containers.py <task>` exits 0 on the final ZIPs (`reduce-house-fixes` H1). Any FAIL stops approval and must be fixed in the generator.
7. **Determinism & duplicate record:** Read `judge` and `duplicate_check` from `<task>/pipeline.json` and relay the verdict and disposition.

## On PASS

- Sync `.agents/skills/fingerprint/cards/<task>.json` (`answer`, `answer_source`, `spine.rows`, `deliverables`, `opening_move`, `question_form`) if stale, then run `python3 .agents/skills/fingerprint/guard.py validate <task>`.
- Set `approved` in `<task>/pipeline.json` to today's ISO date (leave `status` and `stage` unchanged).
- Report: approved, heart verdict line, nearest build and similarity.

Never write the shipped ledger, edit the prompt/bundle/submission, or spawn an adjudicator from `/approve`.
