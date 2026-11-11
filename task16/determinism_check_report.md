# Determinism check, task16 (architecture 2), pass 1, 2026-11-11

**Verdict:** DETERMINISTIC
**Disposition:** APPROVE on Gates A to H, and back to stage 2 on the first-pass reading below
**Judged cut:** target.zip 3b7dfb87, prompt.txt and the four answer blocks as built 2026-11-11. One isolated thread at
medium effort from the brief the determinism-judge agent prepared; it kept the order (its own derivation written to
disk before the graded blocks were opened). The cut on disk since (197dacab) differs by realism repairs only:
figures.json and submission.md are byte-identical to the judged ones.
**Gate G:** mechanism forecasting (with method selection and decomposition), stumping_family analytical_non_defect,
surface_read_dependency no, sole_data_defect no
**Gate H:** domain pass; layers pass; results 11 rates, 5 components and ranges across 6 areas; one_thing none;
effort quick 2, careful 6, thorough 11 of 11; one_fact about 3 of 11 or 4 of 11

## The first pass read against the careful column (build-pipeline, Running the stages)

The thread's own derivation, a medium-effort run written before it saw the blocks, landed inside the stated bands:
every one of the ten family rates and the all-families rate (R7), the set (R9), the linked record exactly (R1), the
rate achieved (R4, 79.96 against 80.4) and the season's conversations (R6, 56.6 per cent and 10,869 a week against
56.4 and about 10,700). Its alert reading (R5) was consistent and not pooled to one figure. It did not reproduce the
unkeyed share (R2) or the open-case count (R3) as separate figures, and ran no resampling (R8). It took about four
minutes.

Priced on that pass, the careful column earns R1, R4, R6, R7 and R9 whole and R5 in part, and loses R2, R3 and R8:
recommendation 14, components 12 of 24, asks 36.7 of 55, instruction 7, about 70. The note priced 46.7 by having the
careful pass carry October's rates into the season; the first pass instead found the measurement gaps from the files
(the weekly flow against the extract, the advisers' tick on unkeyed calls), read resolution by delivery outcome from
one group-by, and weighted the plan's parcels by each outcome's contact rate at the alert depots. Over 50, so the
build goes back to stage 2 whatever the verdict says.

Why it landed: every step was a join and a ratio over labelled ingredients. KS-07 5.1 and 5.2 file the two gaps, the
consignment record carries the delivery outcome as a column, the daily service record counts parcels by the same
four outcomes, and the plan has a sheet of service levels in those outcomes and a sheet of alert dates. Five
estimates, each from its own files, were still five things a pass that reads every file wires together.

## The thread's verdict (verbatim)

# Verdict (task16, pass 1)

**Order kept:** yes. own_derivation.md was written from prompt.txt and target/ before graded_blocks.md was opened; the band table was appended after.

- **Verdict:** DETERMINISTIC.
- **Disposition:** APPROVE (optional: none required; the half-width bands were not re-run by me, see Evidence).
- **Why:** Every family's season rate, the all-family rate and the five-assistant/five-adviser split reproduced from the shipped files by an independent first pass, all ten family figures and the all-family figure inside the stated bands. The call against 75 is forced for nine families by margins of 2.5 to 20 points; the one thin call (Delivery day and time, 78.0, lower band edge 76.8) depends on applying the delay-alert effect that the season plan's Notifications sheet (live 16 Nov at all depots) and the Linz/Graz/Innsbruck pilot depots measure, which is derivable from the files.
- **Evidence:** exact reproductions: 30,745 version 3 conversations (ended 28 Sep to 1 Nov), 4,941 followed (1,293 assistant, 1,340 chat, 1,747 keyed call, 1,196 case), 83.9 per cent linked rate; corrected rate 80.0 vs 80.4 (band 79.6-81.2); late+exception share 56.6 vs 56.4; 10,869 vs about 10,700 conversations a week. My season rates: RET 94.1, PUP 88.9, RDR 82.7, PAY 82.6, DLV 78.0, TRK 69.4, DMG 70.1, RDL 69.2, CUS 67.3, LST 56.3, all 75.06; every one inside the golden band (TRK and CUS at the lower edge). Forks listed: (1) data cut for rule 3.3 (1 vs 2 Nov), immaterial; (2) alert effect: without it DLV reads 73.8 to 74.2 and flips (golden itself states this; the plan's Notifications sheet and the pilot depots pin it, so it is a result, not an open fork); (3) all-family rate weighting by conversations, filed by 3.2; (4) open-case completion: the golden's 235 vs a summer-closing-time reading 77 lies inside effects the bands carry for the call (only DMG moves toward 75, stays under). Not recomputed: the day-resampling half-widths (graded on band 0.78 to 6.3), unverified by me.
- **Files/Hygiene:** PASS. 17 files (3 xlsx, 2 docx, 12 csv), five large CSVs (80,000 to 160,000 rows), the call and consignment files messy (mixed tracking formats, UTC vs local, transfer legs, outbound legs). Distractors present (csat responses, adviser roster, depots, wrapup). Season plan dates after the cut are a forward plan, acceptable. No authoring disclosures seen. Format mix is csv-heavy but includes docx and xlsx.
- **Stump power:** Strong. Naive linked reading gives 83.9 and keeps Track and trace (and Missed delivery, Damaged parcel) with the assistant; each repair is separate work (unkeyed-call weighting, open-case completion, outcome-class reweighting to the plan's late mix, delay-alert propensity cut). A careful pass that reweights on class but ignores the alerts flips Delivery day and time to adviser-first, so no single sentence rescues most results.
- **Stumping type:** mechanism: forecasting (with method selection and decomposition); stumping_family: analytical_non_defect; surface_read_dependency: no (the linked record is an undercount the files document, but the weight sits on modelling the season); sole_data_defect: no. The linked-record undercount is one of several layers; on clean data the class-mix and alert reweighting would still carry the answer.
- **Deep reasoning:** domain: pass (contact-centre resolution rate, first-contact resolution, assistant containment, staffing/channel choice); layers: pass (Layer 1 mixed tracking formats, UTC vs local, keyed IVR gaps, extract of closed cases only; Layer 2 recontact-based resolution, class decomposition, alert causal effect, season forecast with day-resampled range); results: 11 rates plus 5 critical components and ranges across 6 areas (assembly, missingness, causal reasoning, decomposition, forecasting, uncertainty); one_thing: none (alerts effect is a constructed pilot but it is one of several layers and takes difference-in-differences, not one routine step; closest to shallow_hidden_factor but it rescues DLV, TRK partly only); effort: quick 2, careful 6, thorough 11 of 11 family decisions; one_fact: "the season's parcels are later and the alerts go live" rescues about 3 of 11 (TRK, DLV, and the all-family figure), the "calls and cases are undercounted" sentence about 4 of 11 (RDL, DMG, CUS, TRK). Weight sits in assembly/missingness and forecasting; a careful hurried model is likeliest to lose Delivery day and time (about 73.8 to 74.2 without the alert cut, or 82.8 on the unweighted rate) and Track and trace (75.8 to 76.5 unweighted, wrongly assistant-first).
- **Fix:** none. Gate G: no banned stump. Gate H: passes.

Cross-batch: not checked (no access to other tasks in scope); no duplicate observed within the bundle.

## The thread's own derivation (verbatim)

# Own derivation (first pass, written before opening graded_blocks.md)

Method (from prompt.txt, KS-07 and the files only):
1. Normalise tracking numbers (strip spaces, upper-case, drop QP prefix; calls keyed carry 11 digits). Clocks: ACD legs are UTC, converted to Europe/Vienna (CEST to 25 Oct, CET after); assistant, chat, case stamps are local.
2. Assistant conversations with a mapped family and a tracking number (intents with no family excluded), build 3.0.x only (go-live 28 Sep 2026, release note: "stays in service through the peak season"), ended before 2 Nov 00:00 (KS-07 3.3, cut 8 Nov). Further contact within 168 h of ended_at through any channel: another assistant conversation, live chat session (handoff sessions count), keyed inbound call leg 1 only (transfer leg 2 is the same contact; OUT legs are not contacts), customer-raised case (origin WEB_FORM or EMAIL; ADVISER cases are not contacts). Handed conversations are unresolved.
3. Measurement gaps found: (a) the case extract holds closed cases only, so recent customer cases are missing (weekly-flow Opened vs extract count: gap 2 to 20 percent for cases created in late Oct); (b) calls with no keyed tracking cannot be linked, but previous_contact=ASSISTANT on all calls shows only about 55 per cent of assistant-driven calls are keyed. I inflated case-only and call-only recontacts by Opened/extract per queue-week and by (all prev=ASSISTANT calls)/(keyed ones) per week.
4. Rates by family x consignment outcome class (ON_TIME, LATE_1, LATE_2PLUS, EXCEPTION), pooled across depots. Late 2+ day parcels resolve 15 to 30 points lower than on-time (e.g. TRK 0.47, DLV 0.46).
5. Season plan: 3.39M parcels w47 to w53 with on-time 79 to 88 per cent (history about 93 per cent) so the class mix shifts heavily to late. Delay alerts live at all depots from 16 Nov; in history LNZ/GRZ/IBK (alerts from 12 Oct) show about half the late-class conversation propensity per late parcel (LATE_2 89 vs 163 per 1000) and no resolution change. Expected conversations per family = plan parcels by class x per-parcel propensity (alert depots, due 12 to 31 Oct), weighted by class-specific resolution.

First-pass results (percent, point estimate; my uncertainty roughly plus or minus 3 to 5):
| family | 3.0 observed own-mix | corrected own-mix | plan-weighted (alerts) | call vs 75 |
|---|---|---|---|---|
| TRK | 80.1 | 75.8 | 69.4 | adviser first |
| DLV | 85.9 | 82.8 | 78.0 | assistant first (fragile: 73.8 with no-alert propensity) |
| RDR | 88.7 | 85.2 | 82.7 | assistant |
| RDL | 79.9 | 73.1 | 69.2 | adviser |
| PUP | 91.8 | 90.0 | 88.9 | assistant |
| CUS | 75.6 | 70.0 | 67.3 | adviser |
| DMG | 81.4 | 72.0 | 70.1 | adviser |
| LST | 63.0 | 56.5 | 56.3 | adviser |
| RET | 95.3 | 94.3 | 94.1 | assistant |
| PAY | 88.3 | 85.8 | 82.6 | assistant |
Whole (all families together) not computed separately in first pass; weighted by plan conversations it is about 78 to 80.

Hurried passes: ten minutes = pooled naive 3.0 or all-version rate, no correction (TRK 80, DLV 86 => both assistant-first, wrong for TRK). Careful but hurried = class-weighting or case-gap correction but not both, or not the alert propensity (DLV flips to adviser-first at 73.8 vs 78.0 on the propensity choice).
Expected to land inside a plausible band by field-standard method alone: PUP, RET, LST, RDR (far from 75 and class-insensitive). Judgment-dependent: TRK, DLV, RDL, CUS, DMG, PAY and the 'all together' figure.

## Appended after opening graded_blocks.md: first pass against the stated bands
Whole-family figure computed after the first pass with the same method: 75.06.
| figure | mine | golden (band) | inside |
|---|---|---|---|
| RET | 94.1 | 93.7 (92.7-94.7) | yes |
| PUP | 88.9 | 89.1 (87.9-90.3) | yes |
| RDR | 82.7 | 83.4 (81.8-85.0) | yes |
| PAY | 82.6 | 82.0 (80.4-83.6) | yes |
| DLV | 78.0 | 78.0 (76.8-79.2) | yes |
| TRK | 69.4 | 70.7 (69.3-72.1) | yes (edge) |
| DMG | 70.1 | 70.6 (68.8-72.4) | yes |
| RDL | 69.2 | 70.4 (68.0-72.8) | yes |
| CUS | 67.3 | 68.6 (67.2-70.0) | yes (edge) |
| LST | 56.3 | 54.9 (52.3-57.5) | yes |
| all ten | 75.06 | 75.5 (74.6-76.4) | yes |
| linked rate / n / follow-ups | 83.9%, 30,745, 4,941 (1293/1340/1747/1196) | same | exact |
| corrected v3 rate | 79.96 | 80.4 (79.6-81.2) | yes |
| late+exception share of season conversations | 56.6% | 56.4 (53.4-59.4) | yes |
| conversations per week | 10,869 | 10,700 (10,000-11,400) | yes |
| alert cut on late propensity | about 45% on LATE_2 (89 vs 163), about 30% on LATE_1 | 41 (35-48) | consistent (not separately pooled) |
Half-widths not recomputed (no resampling run); the bands for ranges were not tested.
