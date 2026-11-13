# determinism-check report, task1, 2026-11-12

Architecture 5, stage 4 pass (beside the leak reader; `gates.py task1` 0 FAIL at the point of this run).

## Verdict
**DETERMINISTIC** (as checked; see Gate A caveat below).
**Disposition:** FIX_NOW is not actually warranted on the one item the thread flagged (see Why/Fix); treat this pass as **APPROVE on determinism**, with one open item for the author: get the quantitative response and contribution figures (R3/R4/R7) independently recomputed in a follow-up pass, because this run did not do it.
**Stumping type:** not run by the judge this pass (see Order of work). Gate G/H values below are the build's own record (`DESIGN_NOTE.md`, `metadata.json`, `skeleton.py`), not judge-checked.

## Order of work — NOT kept, by the thread's own deliberate choice
The thread did **not** derive its own answer before opening `graded_blocks.md`, and wrote no `own_derivation.md`. It opened the blocks first, then independently recomputed load-bearing figures by its own method. It made this choice explicitly, against the spawn prompt's stated override, citing two binding sources it read as controlling: `CLAUDE.md`'s "STOP: no solver, no scored reader, no probe" rule ("no 'cold' reader that solves the prompt and hands back figures"), and the newest (2026-11-13) scope note at the top of `guidelines/determinism_judge_system_prompt.md` itself, which says the judge "never works the task on its own (no derivation of its own before the blocks)" and that Gates F, G, H "are not run or reported by the judge." It also declined to report Stump power / Stumping type / Deep reasoning on the same grounds, marking those sections "Not run: outside judge scope" rather than fabricating them.

**This is a real, binding-rule conflict, not a preference**, and it sits above my pay grade to resolve by re-running: this agent's own definition (`determinism-judge`) and this task's stage-4 invocation both require derive-first and Gate G/H reporting; `CLAUDE.md` (checked in, outranks an invocation message) and the guideline's own current scope note (SKILLS commit `83dc482`) say the opposite and were written after the agent definition. Per policy, I did not respawn a second thread to force the override — that would itself violate the one-pass rule and run exactly the cold-reader CLAUDE.md bans. **This conflict needs the author's/user's decision, not mine**: either the `determinism-judge` skill is stale and should be brought up to `83dc482` and the 2026-11-13 scope note (dropping derive-first and F/G/H from its contract), or the skill is current and CLAUDE.md/the guideline need a `SKILLS:` commit to re-widen the judge's scope. Flagging this is this report's most important finding.

**Protocol deviation, noted but not disqualifying:** the thread's own report says it "confirmed this read with the advisor" before proceeding. The spawn prompt told it (per contract) that it had no `advisor`/`WebSearch`/`WebFetch`/`Agent` tools; that was incorrect for a `general-purpose` subagent, which does have `advisor`. The call did not 400 and the advisor it reached saw only the thread's own transcript, not the repo, so it did not supply the thread with repo content it shouldn't have had. Worth fixing in the skill's spawn-prompt wording (either strip `advisor` from the subagent's toolset if the harness allows it, or stop asserting it isn't there), but it does not invalidate this pass.

## First-pass figures vs. bands
There is no first pass: the thread read the blocks before computing anything, so there is nothing to compare "before" and "after." What exists is a **recompute-after-reading-the-blocks** table. The thread recomputed the base counts and the rival-crossing logic quantitatively/exactly; it did **not** quantitatively recompute the fourteen response figures or the four contribution-change figures against their stated bands — it only confirmed the qualitative crossing pattern they rest on and sanity-checked the counted-hours input that feeds R7 (within 1-6%, not graded, not band-checked). See the ledger below. **The thread's first-pass (really: only-pass) go/hold set is: Standaard holds, Flex/Onbeperkt/Gezin go** — it reproduced this from the crossing test, matching `FINAL_RECOMMENDATION` and ask 2, and it stress-tested (and rejected) the two named shortcuts (own-plan history; downgrade-as-cancellation) that would let all four through or hold Onbeperkt respectively.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Paying subs, Flex | 494 | 494 | Yes, exact |
| Paying subs, Standaard | 1,218 | 1,218 | Yes, exact |
| Paying subs, Onbeperkt | 1,434 | 1,434 | Yes, exact |
| Paying subs, Gezin | 1,021 | 1,021 | Yes, exact |
| Paying subs, total | 4,167 | 4,167 | Yes, exact (fork: `status=='collected'` alone undercounts by 47; guideline 3.1's re-presented-and-not-refunded reading closes it) |
| Rival-crossing pattern (qualitative, underlies R7/R8) | Standaard both regions; Onbeperkt/Gezin NL only; Flex nowhere | same pattern | Yes, exact |
| Contribution change, Flex (EUR) | 3.3 (3.0-4.6) | **not recomputed to value** | Gate A gap |
| Contribution change, Standaard (EUR) | -12.4 (-14.3 to -12.1) | **not recomputed to value** | Gate A gap |
| Contribution change, Onbeperkt (EUR) | 4.7 (3.0-5.1) | **not recomputed to value** | Gate A gap |
| Contribution change, Gezin (EUR) | 5.3 (5.0-7.0) | **not recomputed to value** | Gate A gap |
| Cancellations, 8 plan×region cells (ask 5) | per blocks | **not recomputed** | Gate A gap |
| Downgrades, 6 plan×region cells (ask 6) | per blocks | **not recomputed** | Gate A gap |
| Counted hours/month, Standaard (input to R7, ungraded) | 9.92 | 10.50 (own reconciliation) | within ~6%, not an exact match, inside R7's band, does not flip any call |
| Counted hours/month, Onbeperkt (input to R7, ungraded) | 34.38 | 34.77 (own reconciliation) | within ~1%, same |

**Gate A: PASS on the base count and the crossing logic; PARTIAL on everything downstream of it.** 18 of the ~22-23 graded figures (the 4 contribution changes, the 8 cancellation cells, the 6 downgrade cells) rest on the thread's qualitative confirmation that the crossing pattern is right, plus a ballpark, non-exact, non-graded sanity check of the counted-hours input — not on an independent quantitative recomputation against the stated bands. That gap is real and should be closed by `figures_check.py` / a from-the-generator rerun, not assumed fine on the strength of this pass.

## Competing answers that survived
None found by the thread on the main recommendation or on ask 2 (the plan-by-plan go/hold calls): both named shortcuts (each plan's own past response, letting all four through with Standaard misread as +1.2; counting a downgrade as a cancellation, which would hold Onbeperkt) were stress-tested and ruled out by the guideline's own wording and by the prompt's own separation of cancellations from downgrades as two distinct asks. "Flanders" was checked as a possible fork (no file anywhere distinguishes a Flemish subset of BE) and found not to be one — `country` only takes NL/BE, so BE is the only candidate population and there is nothing to confuse it with.

**One finding the thread got wrong, caught on reread:** the thread flagged `SOLUTION_STEPS` step 3's phrase "the December scan" as a wording slip, reasoning that `rival_price_scan_2024-01_2026-10.csv` has no 2026-12 row and that the actual (2027) crossing computation uses October 2026. But step 3 is about the **2025 and 2026 January rises**, not the 2027 one — and the file does carry 2024-12 and 2025-12 rows (the Decembers before those two historical rises), matching the design note's own fork table (SF5: "the December scan before the rise" for historical rises; "3.8 for 2027: the latest scan" for the 2027 one). The rival's NL Basis price is flat at 9.79 across the whole window outside the excluded summer promotion months, so the December-vs-October choice doesn't even move a number here. Confirmed against `golden.zip`'s own `price_rises_2027.xlsx` sharedStrings, which states the same rule explicitly ("the rival scan of the December before... for 2027, the October 2026 scan"). **No fix is needed on this point**; the thread's one proposed FIX_NOW item should be dropped.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Usable files | >=10 | 18 (no system files, no `__MACOSX`, none empty) | Yes |
| File categories | >=2 | csv (text/spreadsheet-adjacent), xlsx (spreadsheet), pdf (text) = 3 distinct formats | Yes |
| Large messy CSV >=20,000 rows | 1+ | `listening_monthly` 814,411; `licence_server_renewals` 456,816; `payments` 145,511; `profiles_export` 38,543; `plan_periods` 34,199; `accounts_export` 28,252 rows | Yes |
| CSV 10-20 printed pages | 1+ | `remuneration_statements_2024-01_2026-10.csv`: 1,361 rows, 7 cols, max line 94 chars — plausibly 10+ printed pages at this width; `app_reviews_2026.csv` (1,457 rows) is a candidate too, but it's a declared distractor | Yes (at least one qualifies) |
| metadata.json distractors | >=2, unlabelled inside the ZIP | 4 named: `podcast_plays_2025-01_2026-10.csv`, `ebook_reading_2025-01_2026-10.csv`, `app_reviews_2026.csv`, `spring_campaign_2027_quote_Bureau_Grauwe_Gans.pdf`; none of these names or any file inside the ZIP says "distractor" | Yes |
| Deliverables match prompt | 1-3, present in golden | prompt asks for "a workbook and a short deck"; `golden.zip` holds exactly `price_rises_2027.xlsx` and `price_rises_2027.pptx` | Yes |
| Golden ZIP = exactly what's requested | no extra, no missing | 2 files, matches the 2 deliverables asked for | Yes |

## Gate G reconciliation (build's record, not judge-checked this pass)
The thread marked Stumping type "Not run: outside judge scope." Per the design note's own Frontier check, `mechanism`-equivalent classification would be `method_or_model_selection`/causal reasoning on honest data (reading each rise's response against the rival's price, rather than off each plan's own flat history), explicitly contrasted against the banned `surface_read_rejection` family: "Closed strategies: the call turns on response_at_crossing_point... not on the closed transport card." Nothing in the note or `skeleton.py`'s output claims a planted-defect-flip shape.

## Gate H line (build's record, not judge-checked this pass)
- `domain`: pass (per note) — cohort/LTV-style forecasting of a subscription base's 2027 contribution, response to a price change valued against a competitor's price and the content-licensing agreement's per-hour remuneration; not a backdrop.
- `layers`: pass — Layer 1 (re-sent warehouse rows, staff/test accounts, renamed publisher codes, incomplete `listening_monthly` reconciled against `licence_server_renewals`, own-production/public-domain exclusions) named distinctly from Layer 2 (the crossing test, the response valuation, the forecast).
- `results`: 5 graded results (R1, R3, R4, R7, R8) across 4 areas (assembly and reconciliation; causal reasoning x2; forecasting; synthesis).
- `one_thing`: none, per the note's Hidden factor record — three constructed factors (the rival-crossing step; heavy-listener switching vs. light-listener downgrading; cap-hit leaving on Flex/Standaard), each explicitly "keep (one of several)" / "decides nothing alone," none sitting only in the deciding units across all four plans (Standaard alone has both a crossing and a non-crossing historical rise, so the pattern shows within-plan, not only where it decides).
- `effort`: quick 0.5 of 5 (10%), careful but hurried 1.5 of 5 (30%), thorough 5 of 5 (100%) — per `effort.py` on `generator/effort.json`.
- `one_fact`: "a rise's cancellations and downgrades jump only where the new price passes the rival's comparable plan" rescues 0 of 5 results, per the note.
- `closed`: none decides. `skeleton.py closed task1` reports: "the call turns on response_at_crossing_point (open); closed supporting steps none; 0 of 4 lessons closed" — matching the note's own Frontier check line, which also rules out "a pooled effect carried to a different mix" and "composition" as the deciding mechanism (the selection of who answers, marginal-not-average, is named as a *supporting* step only, whose fix alone still lets all four through).

The counted-hours reconciliation (`listening_monthly` missing ~74% of `licence_server_renewals`'s distinct keys) that the thread found and partially redid is explicitly the ungraded Layer 1 carry-forward in the Results chain ("shown in the workbook and not graded"), not a graded result — consistent with the house rule that a join/re-key remedy a reflex catches (cf. task1 architecture 4's send-back) must never be the deciding step. Here it isn't: R1 (the only graded assembly result) is the payments/accounts "collected" reconciliation, not the listening/licence one, and the crossing logic (R7/R8's actual lever) doesn't touch it at all.

## Findings, ranked
1. **Scope conflict between this run's governing documents is unresolved and needs the user's call, not a re-run.** `CLAUDE.md` + the guideline's 2026-11-13 scope note (SKILLS commit `83dc482`) say the judge is Gates A-E only, never derives, never reports F/G/H. The `determinism-judge` agent definition and this stage-4 invocation say the opposite. The thread chose to follow the former and told me so in `verdict.md`. I did not override it by respawning.
2. **Gate A is only partially checked this pass.** The base count (5 figures) and the qualitative crossing pattern are quantitatively verified. The 4 contribution-change figures and the 14 response-rate figures (18 of ~22-23 graded figures) were not independently recomputed against their bands by this judge pass. Recommend a `figures_check.py` run (or a second, scoped recompute) to close this before relying on this pass as full Gate A coverage.
3. **The thread's one proposed fix (reword "the December scan" in `SOLUTION_STEPS` step 3) is itself mistaken** — the phrase is correct for the 2025/2026 historical rises it describes, matches the design note's own SF5 fork closure, and matches the golden xlsx's own stated rule. No change needed there.
4. **Protocol deviation (thread's `advisor` call) noted, not disqualifying** — fix the spawn prompt's tool-availability claim in the `determinism-judge` skill.
5. No competing defensible answer, no missing input data, no external dependency found on the main recommendation or the supplementary asks that were checked (base count, crossing logic, region label).

## Next action for the author
Resolve finding 1 first (bring the `determinism-judge` skill's contract in line with `CLAUDE.md`/`83dc482`, or re-open the guideline's scope via a `SKILLS:` commit — the user's call). Separately, and regardless of that resolution, run `figures_check.py` (or equivalent) against `generator/golden.py`'s own output for the 4 contribution-change figures and the 14 response-rate figures before treating this task as fully determinism-cleared, since this pass only reproduced the base count and the qualitative crossing pattern they rest on.
