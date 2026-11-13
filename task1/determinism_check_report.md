# determinism-check report, task1, 2026-11-12

## Verdict
DETERMINISTIC (Gates A-E pass on every figure the judge thread could check and on the spec gates checked
independently below)
**Disposition:** SEND_BACK
**Stumping type:** mechanism: planted_defect_flip, stumping_family: surface_read_rejection, surface_read_dependency:
yes, sole_data_defect: yes

## Why

The judge thread kept the required order: it wrote its own independent derivation
(`own_derivation.md` in the scratch path) entirely from `target/` and the TASK_PROMPT block, computing the
October 2026 paying-subscription count and the Nov2025-Oct2026 counted-hours figure from raw logs, before it ever
opened `graded_blocks.md`'s FINAL_RECOMMENDATION / SUPPLEMENTARY_ANSWERS / CRITICAL_COMPONENTS / SOLUTION_STEPS
sections. Its own first-pass numbers matched the shipped golden almost exactly (see table below), so Gates A-E
pass: nothing is unreproducible, uniquely-unforced, or ambiguous in the plain Gate A-E sense.

The disposition is SEND_BACK because the main recommendation (Gezin) and Critical Component 1 (the 24-month
contribution per trial start) are decided entirely by one family of correction applied twice: (1) merging the
licence-server renewals into the counted-hours build (a coverage/join-gap correction, understates Onbeperkt
without it) and (2) attributing a profile's hours to the account the month's charge actually listed it under
rather than to its account today (a stale-roster/misattribution correction, overstates Gezin without it). The
task's own Step-by-Step block admits this in plain language: "the careful route on the live roll-up and today's
profiles leads with Onbeperkt... merging the renewals alone leads with Standaard... dating the profiles alone
leads with Onbeperkt... only the two corrections together" lead to Gezin. That is Gate G's
`planted_defect_flip` (the taxonomy names "coverage/join gap" and "mix effect" by name) and Gate H's
shallow-hidden-factor pattern, and per the current spec the number of stacked corrections does not rescue the
shape.

## Order of work
Kept. `own_derivation.md` was written in full, with every figure and the file/field it came from, before
`graded_blocks.md` was opened. The thread's recomputed figures below are genuinely first-pass, not reverse-fitted
to the shipped answer.

## Recomputation ledger (judge thread's first-pass figures vs. the answer blocks' bands)

| Figure | Claimed (submission.md) | Judge recomputed (first pass, pre-blocks) | Reproduced |
|---|---|---|---|
| Ask 4: paying subs at 31 Oct 2026, Flex/Std/Onb/Gez | 376 / 858 / 1,004 / 731 (2,969 total) | 376 / 858 / 1,004 / 731 (2,969 total) | exact match |
| Ask 5: counted hours/paying sub-month, Flex/Std/Onb/Gez (band) | 5.34 (5.29-5.39) / 10.49 (10.39-10.60) / 31.37 (31.06-31.72) / 27.95 (27.67-28.41) | 5.33 / 10.51 / 31.43 / 27.93 | inside band, all four plans |
| Ask 5, naive combo (live log only, today's roster) | CC2 cites 18.80 / 26.29 as the naive Onb/Gez figures | 18.81 / 26.29 | matches the cited naive (wrong) path, confirms the mechanism |
| Ask 5, live log only + point-in-time roster | Step 2 cites 20.51 for Onbeperkt | 20.43 | close match |
| Ask 5, renewals + today's roster | Step 3 cites 31.52 for Gezin | 31.52 | exact match |
| Ask 6: spring-2024 cohort share paying, Flex/Std/Onb/Gez | 54.3 / 65.1 / 60.7 / 56.6 per cent | 54.6 / 65.6 / 60.7 / 57.3 per cent | close, consistent (thread's "any paid period" proxy vs. the golden's lead-plan-specific count) |
| Final recommendation / Critical Component 1: contribution per trial start, Gezin/Flex/Standaard/Onbeperkt | 22.0 / 13.3 / 12.4 / -3.6 | not independently rebuilt to the euro (full 24-month VAT/store-fee/remuneration waterfall not re-run); ranking verified to rest entirely on the two counted-hours corrections above | not independently re-derived at full precision |
| Ask 7: 2027 remuneration on the Oct-2026 base | ~EUR 202,600 (191,900-207,300) | not independently rebuilt (requires the survival/tenure-band forecast layer) | not independently re-derived |

## Competing answers that survived
None. Each rival reading the judge ran (live log only, today's-roster mapping, each correction applied alone)
produces a different, specific wrong answer (Standaard or Onbeperkt), and each is closed by a named shipped
file: the licence-server-renewals file closes "the live listening log is complete," and the payments file's
point-in-time `profiles_on_subscription` list closes "a profile belongs to the account it sits on today." Gate C
passes on its own terms — every rival is ruled out by a specific file, not left open. The problem the judge raises
is Gate G/H (the *shape* of what closes the forks), not Gate C (whether they are closed).

## Spec gates

| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count / categories | 10+ usable files, 2+ categories | 17 files (14 used + 3 distractors); CSV, PDF, XLSX (3 categories) | Pass |
| Large messy CSVs | one 20,000+ row CSV, one 10-20 printed-page CSV | `licence_server_renewals` 312,004 rows, `listening_monthly` 574,311 rows (far over 20k); `remuneration_statements` (1,361 rows x 7 cols) and `app_reviews_2026.csv` (1,546 rows x 5 cols incl. free text) both print to roughly 15-25 pages at standard formatting | Pass |
| `metadata.json` distractors | 2+ named outside the ZIP, none labeled inside | 3 named (`podcast_plays_2025-01_2026-10.csv`, `ebook_reading_2025-01_2026-10.csv`, `app_reviews_2026.csv`); grepped all CSV/PDF text for "distractor/synthetic/generated/benchmark/fictional" with zero hits | Pass |
| Distractors unused but relevant | each relevant, unused, ruled out by a shipped fact if it answers a graded quantity | podcast/ebook content is the same company's other verticals (relevant setting) but structurally excluded: `catalogue_2026-10.csv` (the schedule B title universe) only carries audiobook title IDs (`T3xxxxx`), so podcast/ebook activity never joins into counted hours; app_reviews is relevant app-level color, unused in any figure | Pass |
| 1-3 deliverables, all present | prompt asks for "a workbook" and "a short deck" | `golden.zip` holds exactly `spring_campaign_2027_plans.xlsx` and `spring_campaign_2027.pptx`, nothing else | Pass |
| Asks multi-dimensional, units stated, no rounding instruction | each ask states its unit; prompt doesn't dictate rounding | `prompt.txt` asks for contribution per trial start (euros), paying subscriptions (count), counted hours per paying subscription-month, conversion share/paying months/net revenue, 2027 remuneration (euros); no rounding instruction anywhere in `prompt.txt` | Pass |
| Answer shape | one of the client's 14 shapes | "a forecast path with bands, plus its drivers" (DESIGN_NOTE.md Draw) | Pass |
| Golden ZIP exact contents | exactly the files the prompt requests, requested formats | 2 files, matches the prompt's "a workbook" + "a short deck" exactly | Pass |
| Nothing LLM-generated / golden reads real | spot check | files read as genuine operational exports (payment retry pairs, a publisher-code crosswalk from a real migration, a KPI report on an old revenue-share basis); no deep golden-realism audit performed (out of scope for this pass) | Not fully audited |

## Gate G reconciliation

The judge thread (never having seen DESIGN_NOTE.md) classified the primary mechanism as `planted_defect_flip`
/ `surface_read_rejection`, `surface_read_dependency: yes`, `sole_data_defect: yes` (on clean, fully-joined,
correctly-timestamped source data the Onbeperkt-vs-Gezin flip disappears). DESIGN_NOTE.md's own "Forcing" section
(line 94), written independently before the judge ran, corroborates this exactly: "the golden family... all lead
with Gezin... the shortcuts lead elsewhere: the careful route Onbeperkt..., the licence channel alone
Standaard..., the dating alone Onbeperkt, the 2026 share Onbeperkt, streamed seconds Onbeperkt." Both documents,
independently, describe the same two-part stacked correction (licence-channel merge + profile-dating correction)
as the thing that, and only that, flips the recommendation to Gezin. The design note frames this as "three
independent judgments" (Deep reasoning, line 31) and the Hidden factor record labels each piece "modelling," but
the two corrections that matter for the graded recommendation and Critical Component 1 are still exactly the
`planted_defect_flip` shape Gate G bans "regardless of depth... the number of corrections does not rescue the
shape." The design note's own "Not one thing" paragraph (line 21) argues the licence channel alone still leaves
other work to be earned (R1, R4, R6's survival/season judgment) — true, but those pieces are not what the
rubric's heaviest-weighted criteria (the recommendation, Critical Component 1) are graded on; per the design
note's own Results chain, R5 (Critical Component 1) depends only on R4 and the counted-hours construction, and
R7 (the recommendation) depends only on R5.

## Gate H reconciliation

DESIGN_NOTE.md's Effort test table (quick 0.5/6, careful-but-hurried 2/6, thorough 6/6) matches the judge's own
independent effort read almost exactly: the judge thread found the "obvious" build (`listening_monthly` +
today's `profiles_export`) is "exactly what a time-pressed analyst reaches for first," and it earns R1 and R4
only — the same two results the design note's table credits to the careful-but-hurried pass. This is not a
divergence; it corroborates the design note's own effort grading.

The divergence is on H5, the one-fact test. DESIGN_NOTE.md's "Largest single hint" line (line 68) states: "the
licence renewals carry the positions of titles played from downloads; rescues 1 of 6 results" — testing only
*one half* of the two-part correction in isolation, consistent with its own "Not one thing" claim that the
licence-channel sentence alone "rescues R6 alone (R2 and R5 still carry the moved profiles)." But the judge
thread's best single sentence packages *both* corrections together ("merge the licence-server renewal positions
into the counted-hours build, and attribute each profile's hours to the account the month's charge actually
listed it under, not to its account today") and this compound sentence, tested as one unit, flips a run straight
to the correct recommendation and fixes Critical Components 1 and 2 outright. The design note's one-fact test
never ran the compound form of its own two-judgment stack as a single sentence; the judge thread, deriving first,
found that stating both halves together is more than a third of the rubric's heaviest-weighted criteria. This is
the exact failure mode this skill's instructions flag by name: a pass with the blocks in its prompt can accept a
guideline sentence that a derive-first pass executes as written and finds gives a different (here: higher) rescue
count than the design note claims.

- H1 (domain): pass, uncontested.
- H2 (two layers): pass, uncontested.
- H3 (not one thing): **fails**, per the judge's independent finding corroborated by the design note's own
  "Forcing" section — one two-part correction family carries the recommendation (R7) and Critical Component 1
  (R5), which the rubric weights heaviest.
- H4 (effort throughout): the design note's own table already shows careful-but-hurried at 2/6 = 33%, at the
  edge of (not clearly below) the "about a third or fewer for the ten-minute pass, clearly more for the careful
  pass" shape the gate wants; combined with H3's finding this does not clearly separate.
- H5 (one-fact test): **fails** — the compound single sentence (both corrections stated together) rescues the
  recommendation plus Critical Components 1 and 2, exceeding the roughly-a-third ceiling; the design note's
  "Largest single hint" line undercounts this by testing only one half of its own two-part mechanism.

## Stump power (Gate F)

Real: the judge thread confirms the "obvious" first build (live log only, today's profile roster) is exactly
what a time-pressed analyst reaches for, and it hands back a different, specific, wrong plan (Onbeperkt) at a
materially different euro figure (45.5 vs. the golden's 22.0). The problem is Gate G/H, not Gate F: the task
would stump a strong model, but for catching that the obvious first-pass build of one metric is wrong, twice, in
exactly the two units that decide the call.

## Findings, ranked

1. (Send-back) Gate G `banned_stumping_type`: the recommendation and Critical Component 1 are decided by a
   two-part `planted_defect_flip` (licence-channel coverage gap + profile-dating misattribution) stacked on one
   metric (counted hours per paying subscription-month); stacking does not rescue the shape under the current
   spec. Corroborated independently by DESIGN_NOTE.md's own Forcing section.
2. (Send-back) Gate H3/H5: one correction family carries the heaviest-weighted graded criteria; the design
   note's own one-fact test undercounts the compound sentence's rescue power by testing its two halves
   separately rather than together.
3. (Note, not disqualifying) Gate H4's own table already sits at the edge of the required separation between
   the ten-minute and careful-but-hurried passes (0.5/6 vs 2/6); worth re-checking once R7/R5 are re-rooted.
4. (Not a finding) Gates A-E, the spec gates and the hygiene checks are otherwise clean: every recomputed figure
   landed inside its stated band, every rival the judge ran is closed by a named file, the file/distractor/
   deliverable requirements are all met.

## Next action for the author

Re-root the main recommendation (R7) and Critical Component 1 (R5) so that the Onbeperkt-vs-Gezin plan choice no
longer turns solely on the licence-channel-merge + profile-dating correction pair: either make the counted-hours
figure correctly measurable from a single, already-complete source so the plan ranking instead turns on a genuine
forecasting, decomposition, or binding-constraint judgment (e.g. how much of the spring-2024 cohort's paying-month
pattern survives under 2027 pricing, or the agency's campaign-capacity constraint), or keep the two corrections as
one of several checkable results (worth real credit, as R2 already is) but widen the recommendation's margin so it
survives deleting them, so no single correction family by itself reverses R7.
