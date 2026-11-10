# determinism-check report, task4, 2026-11-09

Re-judge after FIX_NOW (architecture 9): the combination-tare-and-drop-share component was taken out of
Critical Components (the work stays in the model and in the Trailers-and-drops sheet, ask 4) and Critical
Component 1 and Step 3 were reworded on the drinks maker's notes. `target.zip` is byte-identical to the prior
pass. One isolated judge thread ran on a fresh unzip of `target.zip` at
`/tmp/determinism-check-task4-1794278276/target/`, seeing only that directory plus the prompt and the four
graded blocks inlined in its spawn prompt; it never read `submission.md`, `DESIGN_NOTE.md`, `metadata.json`,
`generator/`, or any prior report. Its Gate F estimate is its own, not reconciled against the design note at
spawn time.

## Verdict
**DETERMINISTIC**
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection / statistical_rigor (mixed); stumping_family:
analytical_non_defect; surface_read_dependency: no; sole_data_defect: no

## Why
The thread independently rebuilt, from the raw files alone, the pilot duty-day count (2334, exact), the
first-year battery-loss curve (naive straight line 3.0 to 3.1 percent vs. an out-of-sample curved fit 4.55
percent, matching the claimed naive-3.1/true-4.6 story and the 515/438 kWh figures, with the named rival 445 kWh
reproducing exactly from the straight-line loss), the -5 C speed ratio (0.76 to 0.78 across five forms, matching
the claimed 0.76 and the 74-83 to 56-63 km/h duty ranges), and the terminal-calibration-line story via a
shipper-specific regression (13.14/13.00 t against the claimed "13.2 and 13.1 t on the line"). All three stated
Critical Components reproduce. The final 14-duty energies and the exact 8-tractor order were spot-checked for
plausibility rather than rebuilt bit-for-bit (the full debiased-payload plus curved-loss plus
temperature-conditioned-speed plus multi-drop pipeline was judged too large to reimplement independently in one
pass), but nothing the thread computed contradicts them and the electric/diesel margin (le430 vs ge450 kWh
against a 438 kWh limit) comfortably exceeds the stated 10 kWh tolerance. No competing answer survived for the
main recommendation or any supplementary answer; FES-2's WHAT (2.1 to 2.3, 4.1 to 4.3) is filed and its literal
execution is the golden, with the HOW (the error model, the age form, the speed correction) left open and pinned
only by the data.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Pilot duty-days (Step 1) | 2334 | 2334 (dedup 2374 raw rows, inner-join to Jönköping TMS) | Yes |
| First-year battery loss | 4.6% (4.2-5.6) | straight line 3.0-3.1%; curved out-of-sample fit 4.55%, R squared 0.927 vs 0.909 | Yes |
| Usable battery / limit | 515 / 438 kWh | 540x(1-0.046)=515.16 to 515; 515x0.85=437.75 to 438 | Yes |
| Named rival limit | 445 kWh | 540x(1-0.031)=523.5x0.85=445.0 | Yes (rival also reproduces) |
| -5 C speed ratio | 0.76 (0.74-0.79) | 0.765-0.78 across linear/quadratic/binned forms; year ratio 0.891 vs claimed 0.89 | Yes |
| Duty speed ranges | 74-83 to 56-63 km/h | 74.07-82.97 planned; 56.3-63.1 at x0.76 | Yes |
| GDR/drinks-maker calibration line | 11.6/10.4 t own, 13.2/13.1 t on the line | 11.68/10.25 t own; 13.14/13.00 t on a shipper-specific weighbridge regression | Yes |
| Payload coefficient | 1.9 (1.7-2.4) | not rebuilt end to end (debiasing pipeline too large for one pass); naive regression gave an attenuated ~0.27, consistent with the claimed attenuation direction and the 1.2/1.5 rivals | Plausibility only, not digit-for-digit |
| 14 duty energies and the 8-tractor order | V02-V18 electric at 410-430, V07 etc diesel at 450-470; order 8 | reduced-form plausibility check lands ~390-400 kWh for V02 before the omitted multi-drop/tare terms; nothing contradicts | Plausibility only, not digit-for-digit |

## Competing answers that survived
None. The thread could not construct, from the files alone, an equally-licensed reading of FES-2's terms (design
day, planning load, 85 percent reserve, "usable battery... less the share permanently lost") that moves the 438
kWh limit or the 430/450 kWh duty split. The solution's own named rivals (terminal calibration line alone: 9;
straight-line loss plus year ratio: 5; that line and loss at design-day speed: 10; no first-year loss: 13; year
ratio alone: 1; routing-tool speed alone: 0; no speed term: 10; tare left out: 6; drops carried to last drop: 6)
are shown by the submission itself to each individually misorder the fleet, which the thread treats as the
hurried failure modes the task is built to catch, not as surviving defensible alternatives.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Usable files | 10 or more | 13 (11 substantive + 2 distractors); no system files or placeholders | Yes |
| File categories | 2 or more | csv (7), xlsx (4), pdf (2) = 3 categories | Yes |
| Large messy CSVs | one 20,000+ rows, one 10-20 printed pages | weighbridge_varnamo: 21,413 rows; tms_consignments_varnamo: 18,072 rows | Yes |
| metadata.json distractors | 2 or more named, none labelled inside the ZIP | fuel_card_statement_varnamo_2025-2026.csv, workshop_log_2025-2026.csv; neither file name nor contents flag them as decoys inside target.zip | Yes |
| Distractors relevant but unused | each weighs on the decision without deciding it | both read as genuine Värnamo fleet operational artifacts (fuel card, workshop log); judge thread independently called them "plausible but unused distractors for this BEV-only ask" | Yes |
| Deliverables | 1-3, all present in golden, no forced format family | 2 requested (ev_duty_assessment_2027.xlsx, tractor_order_memo.pdf), both present in golden/ and in golden.zip | Yes |
| Asks multidimensional, unit/rounding stated | yes | prompt states "Energies to the nearest 10 kWh, the payload figure to 0.1 kWh and the loss to 0.1 per cent"; asks 1-8 are each multi-row/multi-field, not single lookups | Yes |
| Answer shape | one of the fourteen client shapes | an allocation (which duties, how many tractors) with its sensitivity (what each shortcut would order instead); four or more checkable results (R1-R6 feeding Component 1-3, Ask 1-2, Recommendation) | Yes |
| Golden ZIP contents | exactly the requested files, requested formats | golden/ holds exactly ev_duty_assessment_2027.xlsx and tractor_order_memo.pdf, matching the prompt's "spreadsheet" and "one-page PDF memo" | Yes |
| Realism / not LLM-generated | yes | judge thread's hygiene pass: PASS, no README or benchmark disclosure, genuinely messy weight-field formatting ("9250" / "7 850 kg" / "8,40 t"), a mid-year duty-renaming convention, temporal coherence checked (in-service date precedes the telematics window; the weighbridge window matches FES-2's trailing-12-month rule) | Yes |

## Gate G reconciliation
The thread's classification (`mechanism: method_or_model_selection / statistical_rigor`, `surface_read_dependency:
no`, `sole_data_defect: no`) matches the design note's own strategy label, "WORKS IN FORM (a forecast carried to a
population the fit never saw, through a covariate whose calibration does not transport, beside a degradation
whose form the record chooses)," and its card's "Not rule application" / "No decoy" / "No replay" lines: FES-2
files the WHAT, nothing filed names the error model, the age form, the speed ratio or a temperature form, and no
shipped artifact states a wrong number the task overturns. No banned surface-read-rejection shape is present on
either side.

On Gate H the two sides mostly agree and partially diverge:

- **H3 (not one thing):** agree. Design note: "three estimates each move the order, and each put right alone
  inside the careful model still orders wrongly (2, 3, 10)." Thread, independently: "the solution's own
  enumerated rivals... show that getting any one of the four levers right while missing another still misorders
  the fleet," and `one_thing: no`. No reconciliation finding.
- **H4 (effort grades), partial divergence on R3 (the -5 C speed ratio):** the design note's effort table, built
  from `effort.json`/`effort_passes.py` on the actual recorded platform runs (architectures 7 and 8), scores the
  careful-but-hurried pass **Missed** on R3 ("method shortcut: the year's ratio, 0.89 (both arch 7 runs)"), and
  the overall careful-but-hurried row at 0.5 of 6. The thread, reasoning without that run record, estimated R3 as
  "**Likely RIGHT, or close to right**... FES-2 itself defines the design day as a specific temperature (-5 C),
  which is a strong, document-given cue... a one-plot, one-group-by move, which the Sulfur run record treats as
  'modelled on sight.'" This is the reconciliation pattern the determinism-judge contract calls out: the thread
  treats a factor as found in one look that the note's own measured record (two real platform runs) shows was in
  fact missed by both. It does not change the verdict here because (a) the design note's actual record is
  *stricter* than the thread's hypothetical estimate, so the task is if anything harder than the thread credits,
  not easier, and (b) even crediting R3 to the careful-but-hurried pass, the thread's own six-result grid still
  scores that pass wrong on R1, R2, R5 and R6 and mixed on R4 — well under half either way. Recorded as a
  finding to flag, not a send-back trigger.
- **H5 (one-fact test), mild divergence:** the design note's largest single hint ("the pilot's regional duties
  carry lighter loads than the same shippers' terminal runs, so the terminal's calibration line does not carry to
  them") rescues 1 of 6 results. The thread's independently-chosen best sentence ("control for ambient temperature
  and de-bias the declared payloads before fitting anything") rescues, by its own count, "at most 2 of the ~6
  graded result families" — a materially broader single sentence than the note's, because it folds two separate
  corrections (R1's debiasing and R2's curve form) into one piece of advice. At 2 of 6 (about one third) this
  sits right at, not comfortably under, the ceiling the thread itself claims. This is the one finding worth the
  author's attention: a reviewer's single best sentence may rescue closer to a third of the results than the
  design note's own one-fact test implies, because the two measurement corrections (payload debiasing, battery
  curve form) can be stated together as one piece of advice. It is not, on its own, grounds for SEND_BACK (the
  bar is "about a third or fewer," which 2 of 6 still satisfies on either side's count), but it narrows the
  margin the design note assumed it had.
- **H1/H2:** agree. Thread's domain line ("not swappable... tonnes, loaded km, state-of-charge, weighbridge,
  trailer tare and a design-day temperature standard are all load-bearing") matches the design note's swap test
  ("how many community nurses to hire... the call stops making sense"). Thread's two-layer line matches the
  note's Layer 1/Layer 2 split.

## Stump power (Gate F)
The thread's own six-result estimate (not reconciled against the design note at spawn time, per the brief):

| Graded result | Careful-but-hurried solver | Rough rubric weight |
|---|---|---|
| 1. The order (count and duty IDs) | WRONG — inherits every upstream miss; the submission's own enumerated rivals (9, 10, 5, 13, 1, 0, 6) show a textbook-first-move combination lands on one of these | Largest share (the Final Recommendation) |
| 2. Payload figure (kWh/t/100 loaded km) | WRONG — the natural move (regress on raw declared weight, or the terminal's calibration line) gives 1.2 or 1.5, not 1.9; a classical measurement-error trap | Moderate |
| 3. First-year battery loss % | WRONG — the textbook first move (straight line in age) gives 3.0-3.1%, not 4.6%; the curved early-loss shape needs an out-of-sample test and a temperature-confound control | Moderate-high (also moves 515/438 vs 523.5/445, which cascades into every duty) |
| 4. -5 C speed ratio / design-day speeds | Likely RIGHT or close — FES-2's named design-day temperature is a strong document cue; a one-plot/one-group-by regression against temperature lands near 0.76-0.78. The design note's own measured record of the actual platform runs disagrees (both arch 7 runs missed this and used the year's ratio); see Gate G reconciliation above | Low-moderate — mostly a document-reading check |
| 5. Fourteen duties' design-day energies | Mixed, trending WRONG on the near-threshold duties (V02, V14, V18, and the V03/V05/V09/V11/V16 cluster); far-from-threshold diesel duties (V24/V27/V30/V33) likely come out roughly right by chance | High (14 gradable rows) |
| 6. Electric/diesel verdict per duty | WRONG on several duties, directly inheriting #5; the submission's own named rivals move V03/V05/V09/V11/V16 in and out under single-lever mistakes | High |

The thread's conclusion: "None of these six results is earned purely by reflex: #4 is the closest to a routine,
document-cued step and should be priced modestly, but #1, #2, #3, #5 and #6 each require a genuine judgment... that
a textbook-first-move, careful-but-hurried pass plausibly gets wrong." No result was flagged by the thread as
earned by reflex; the component that was previously flagged that way (combination tare and drop share) was
correctly excluded from the graded blocks the thread saw and was not re-raised.

## Findings, ranked
1. (Minor, record only) Gate H4/H5: the thread's independent estimate treats the -5 C speed-ratio result (R3) as
   close to earned by a careful-but-hurried solver, while the design note's effort table, built on the two actual
   recorded platform runs, scores it Missed. The discrepancy makes the task look slightly easier under the
   thread's hypothetical than under the note's measured record, not harder, so it does not threaten the bar; flag
   for awareness only.
2. (Minor, record only) Gate H5: the thread's own best single sentence rescues about 2 of 6 result families (one
   third) by combining the payload-debiasing and battery-curve-form corrections into one piece of advice, versus
   the design note's one-fact test of 1 of 6. Still within the "about a third or fewer" bar on either count, but
   closer to the edge than the note assumed.
3. (None rising to SEND_BACK) No competing answer, no missing decisive fact, no external dependency, no
   surface-read-rejection, and no single hidden or planted factor found by either side.

## Next action for the author
None required for determinism or stumping-type; the build is APPROVE as judged. Optionally, note in the design
note's Hidden factor record / Effort test that the single sentence "control for ambient temperature and de-bias
the declared payloads" can be read as one combined hint covering R1 and R2 together, so the one-fact ceiling is
closer to a third than the current 1-of-6 entry implies; this is a bookkeeping note, not a rebuild.
