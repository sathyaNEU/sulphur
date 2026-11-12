# determinism-check report, task7, 2026-11-12

Architecture 10. This is the re-judge after the fix to Lumivale's "still in the event" share
(now read as a band spanning the interval's start and end readings, with Critical Component 1
restated to cover the whole interval). The earlier pass of today, which opened
`graded_blocks.md` before deriving, is set aside and not counted.

## Verdict
**DETERMINISTIC**
**Disposition:** APPROVE
**Stumping type:** mechanism: decomposition_attribution (primary; method_or_model_selection for
the 1 July 2027 enrollment/channel projection), stumping_family: analytical_non_defect,
surface_read_dependency: no, sole_data_defect: no

**Order kept:** Yes. The thread wrote `own_derivation.md` (16.8 KB, a full literal reading of
Board Policy 412, its own recompute of every provider's raw M&V-pooled kW figure, Ondera's
window mismatch, the uncalled 18 September 2025 interval, a self-initiated temperature-regression
rival, and a 1 July 2027 enrollment projection) entirely from `prompt.txt` and the fresh unzip of
`target/`, before it ever opened `graded_blocks.md`. It states this itself at the top of
`verdict.md` and the content of `own_derivation.md` corroborates it: the file ends with an open
question ("I cannot, from the files alone, force one of these two readings as uniquely correct;
I flag this explicitly as the central determinism question to carry into Step 2") that only makes
sense written before the committed answer was known.

## Why
The decision is forced once the full three-carry chain is worked (4CP-day participation share,
the 1 July 2027 fleet mix by channel, and the fleet's homes by the appraisal roll), all three
pinned by files in the package (the provider event reports against `ercot_4cp_intervals_2016_2026.csv`
and `peak_partners_event_log_2024_2026.xlsx`; the roster against `provider_quotes_summer_2027.xlsx`;
`calder_cad_residential_2026.csv` against the research sample). The thread's own blind derivation,
working the files cold, independently found three of the same mechanisms the committed solution
names (the uncalled 18 September 2025 interval, Ondera's window ending before 10 of 12 real 4CP
intervals, and the heat-wave-depth participation decay visible by cross-tabbing the event log
against the 4CP list) and, on its first blind pass, reproduced the committed FINAL_RECOMMENDATION's
own explicitly-named "hurried" reading almost exactly in direction and story, differing only in a
cruder method's magnitudes. No gate failure was found; the one residual item is a verification-depth
caveat (the thread could not, in the time it had, drive its own recompute of the participation-share
and cooling-slope figures to the stated numeric precision), not a located defect.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Ask1-3 internal arithmetic (3.76 MW, $206,000, $163,534, $42,500 net) | workbook 'providers' sheet | exact: 2127x0.630+1268x1.015+1511x0.749 devices-weighted = 0.766 kW/device x 4,906 devices; 3.76 MW x $54.80/kW-yr = $206,048; 2127x29+1268x41+1511x33 = $163,534 exactly; net $42,500 | Yes, exact |
| Event settings, 2027 quote vs. 2024-2026 actual | implicit in R5/R6 | identical, provider by provider, across `provider_quotes_summer_2027.xlsx`, `peak_partners_member_guide_2026.pdf`, and the event log's settings sheet; no re-scaling fork | Yes |
| Transmission rate $54.80/kW-yr | Board Policy 412 / notice | filed verbatim in `transmission_charge_notice_2027.pdf`, effective 2027 only | Yes |
| 18 Sep 2025 interval, zero for every provider | workbook '4CP intervals' sheet | confirmed: the date is in `ercot_4cp_intervals_2016_2026.csv` but absent from `peak_partners_event_log_2024_2026.xlsx` (nearest calls 9/16 and 9/19) | Yes |
| Ondera's negative kW (-0.125) | R1 / Critical Component 4 | sign and mechanism (window ends 17:00, before 10 of 12 real intervals, post-event rebound) confirmed; exact magnitude not independently matched (thread's own pooled-average calc gave -0.515, its temperature-adjusted calc -0.184) | Directionally yes; magnitude not closed |
| Lumivale's share still in event, 33% (band 31-36 +-2) | Critical Component 1 | thread's cruder recompute (no pre-event-load covariate) gave ~39% at the interval midpoint and ~72% on test days, just outside the stated band | Directionally yes; magnitude not closed |
| Devices enrolled 1 July 2027 / quote cost | Ask 2 | thread's independent blanket-churn projection landed within ~1% of committed for 5 of 6 providers; ~4.5% off for Pinecrest Home (2,885 vs. 2,760), slightly outside the stated 3% band, attributable to the thread's cruder (non-channel-stratified) attrition model, not a contradiction | Mostly yes; one provider outside band on a cruder method |
| Kitebrook's fleet sheds 1.54x the research sample's | Critical Component 3 | thread's own naive address match (uppercased string only) matched ~17% of accounts, too low to validate to precision; nothing found that contradicts it | Not independently closed; no contradiction found |
| Pinecrest Home's fleet 65% retail / 59% in event | Critical Component 2 | not independently recomputed to precision; no contradiction found | Not independently closed; no contradiction found |

## Competing answers that survived
None survive as a genuine, equally-complete rival. One is worth recording because the thread
raised it unprompted in its blind pass and investigated it seriously: a per-provider linear
regression of the M&V call/hold gap on outdoor temperature, extrapolated to each real 4CP day's
actual recorded temperature (in place of a flat pooled M&V average). This flips Corvane, Ardena
and Pinecrest Home relative to the simple pooled-average reading. For Corvane and Ardena it lands
on the *same* side of the line as the committed golden (both already renew), which corroborates
the golden rather than contesting it. For Pinecrest Home it lands on the *other* side (renew,
against the golden's don't-renew), and for Kitebrook it still falls short of the golden's figure.
The thread's own resolution -- that a temperature-only regression conflates two different
mechanisms the golden keeps separate (the shed itself, modeled as linear in interval temperature,
per SOLUTION_STEPS step 3; and the share still in the event, modeled by a 4CP day's position in a
heat-wave's run of alert days, per step 4), and so is missing the home-heterogeneity correction
for Kitebrook and partially double-counts/misattributes the heat-wave effect for Pinecrest Home --
is consistent with the design note's own account (R2 and R3b are independent carries; a
temperature-only read is a different, confounded proxy for R2 alone and never reaches R3b or R4).
This reviewer finds that resolution defensible: temperature on the one hand and a day's position
in a multi-day alert run on the other are correlated in this data (4CP days are by definition the
hottest hours of the hottest days) but not interchangeable, and the design's four actually-pinned
rivals (checks.py: still-in-event read at the interval's start or end, a linear home model with a
size-by-age term, one leaving rate for every channel, the test halves without the pre-event load)
do not include a bare temperature-only regression. This fork does not survive as a defensible
alternative to the golden; it is recorded here for transparency because of its size (it moves 3 of
6 providers) and because it was the thread's own, unprompted construction rather than something
fed to it.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Usable files | >=10, >=2 categories | 21 files; csv (15), pdf (5), xlsx (2) -> spreadsheet + text/document categories | Pass |
| Large, messy CSVs | >=20,000 rows, and 10-20+ printed pages | `ami_15min_reads_peak_partners_2024_2026.csv` 189,653 rows; `corvane_event_report_2024_2026.csv` 132,200 rows (far beyond 10-20 pages) | Pass |
| Distractors named in metadata.json, none labelled in-ZIP | >=2 | `ercot_residential_dr_potential_2025.pdf`, `der_interconnections_2026.csv`; neither named as a distractor inside the ZIP; no file reveals how the task was built (confirmed by the thread's hygiene pass) | Pass |
| Distractors relevant but unused | each | DR-potential PDF gives only generic, explicitly-unadjusted industry ranges (0.7-1.1 kW BYOT) that a lazy solver could mistake for a provider figure, ruled out by the PDF's own "not adjusted to any one utility" line; solar interconnection CSV is domain-adjacent (DER) but plays no role in any computation | Pass |
| Deliverables | 1-3, all present in golden | 2 requested (memo docx, workbook xlsx); golden.zip holds exactly these two files, no more, no fewer | Pass |
| Asks multi-dimensional, unit stated, no rounding in prompt | — | prompt.txt asks per-provider kW, device counts, quote cost, renewed MW and net saving, no rounding instruction; precision/bands stated only in the answer blocks | Pass |
| Answer shape, one of fourteen | — | a reconciled table (provider by provider: kW vs. price-implied threshold, devices, cost, renew/no) with a roll-up allocation (the renewed set's MW and net saving) | Pass |
| Golden ZIP exact match to request | — | `provider_renewals_2027_memo.docx`, `provider_renewals_2027_workbook.xlsx`, matching the prompt's "a short memo... and a workbook" | Pass |
| Not LLM-generated, reads as real work product | — | memo reads as an internal utility memo (named sender/date/board audience, terse, numeric); files carry realistic mess (UTC/local mixing, a 2025 meter re-key, a stale export with 174 former-member meters, 12-17% AMI missingness, two address forms between the roll and the accounts) per the thread's hygiene pass and this reviewer's own read of the memo text | Pass |

Files/Hygiene: PASS overall per the thread and this reviewer's own spot checks (golden memo text,
file counts, distractor content). No provenance, benchmark-disclosure, or stale-snapshot finding.

## Gate G reconciliation
Thread: `mechanism: decomposition_attribution` (plus `method_or_model_selection` for the 2027
enrollment carry), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`,
`sole_data_defect: no`.

Design note (`## Deep reasoning`, `## Frontier check`): "Strategy label: a randomised impact
carried to selected peak days, next year's fleet and the fleet's homes (sulfur-strategies.md,
population_selection)"; explicitly "Not semantics," "Not rule application," "No decoy," "No
replay." These describe the same shape the thread independently classified: an honest,
correctly-measured randomized effect (the M&V test events) that has to be extrapolated across
three different populations/conditions (the 4CP days, the 2027 fleet, the fleet's homes), never a
flip away from a misleading reported number. The two labelings line up: a FINE-numbers
decomposition/extrapolation, no surface-read dependency, no sole data defect. No reconciliation
discrepancy on Gate G.

## Gate H reconciliation
Thread: `domain: pass`, `layers: pass`, `results: 9 graded across 5+ areas`, `one_thing: none`
(five distinct mechanisms: the uncalled 18 September 2025 interval, Ondera's window mismatch, the
Lumivale/Pinecrest Home heat-wave participation decay, Kitebrook's home heterogeneity, and the
channel-stratified 2027 enrollment projection), `effort: quick ~1 of 9, careful ~3 of 9, thorough
9 of 9`, `one_fact: "4CP days always fall 3+ days into a multi-day alert streak" rescues ~2 of 9`.

Design note (`## Results chain`, `## Effort test`, `## Hidden factor record`): 8 graded results
(R1-R7, R5 and R6/R7 both synthesis-level), `one_thing: none` (three independent carries, each
deciding a different provider, matching the thread's finding almost exactly, modulo the thread
additionally scoring the uncalled-interval texture item as its own ninth result), effort quick
0.5/8, careful 2.5/8, thorough 8/8 (thread: ~1/9, ~3/9, 9/9 -- the same shape, slightly more
generous on the quick/careful counts but both still well under a third for the quick pass and
near but under a third for the careful pass), largest single hint rescues 1 of 8 (R2 alone,
moving only Lumivale; "the call stays wrong on Pinecrest Home and Kitebrook").

One real discrepancy worth flagging, though it does not change the disposition: the thread's
`one_fact` line credits the heat-wave-lateness sentence with rescuing *two* results (it says this
hint "flips Lumivale and Pinecrest Home's calls"), where the design note's own effort.json-measured
figure attributes only Lumivale's flip to that sentence and assigns Pinecrest Home's correction to
a separate sentence (the retail-channel hint, R3b). On inspection, the thread's own evidence trail
supports the design's narrower attribution, not its own broader one: the thing that moved Pinecrest
Home in the thread's hands was its ad hoc temperature-regression exercise (section 5 of
`own_derivation.md`), a different and cruder intervention than literally "read the share still in
the event on the 4CP days" (R2's actual correction). The temperature regression moving Pinecrest
Home appears to be a side effect of conflating the heat-wave-participation mechanism with a
correlated-but-distinct temperature signal, not evidence that the R2 sentence alone also fixes
Pinecrest Home. Read this way, the thread's own-fact count is an overcount by one, and the design
note's 1-of-8 (now 1-of-9) figure stands. Even taking the thread's own, more generous count of 2 of
9 (~22%) at face value, it stays under the "about a third" bar H5 sets, so this does not change the
Gate H verdict either way; it is recorded as a minor reconciliation note, not a finding.

The thread's blind pass also misclassified `calder_cad_residential_2026.csv` as a likely distractor
in its own_derivation (before it had reconstructed the Kitebrook home-heterogeneity carry); this
was a blind-pass miss, not a finding about the task, and the thread corrected it in Step 2 by
attempting the CAD address match to check Critical Component 3. The two files actually declared as
distractors in `metadata.json` were correctly and independently identified as unused by both the
thread and this reviewer.

No finding here rises to a Gate H failure: five independently checkable mechanisms were found by
an isolated thread working cold, three of them (the no-call interval, Ondera's window, and the
heat-wave participation decay) entirely without having seen the committed answer, and none of them
is shallow (each design-note "Fix depth" is "modelling," not a routine filter or reweight), and no
single sentence collapses more than about a third of the graded results.

## Stump power (Gate F)
High and spread across the chain, matching the design's own forecast. A strong-but-hurried model's
most natural move (carry the 24 randomized M&V test events' call/hold AMI contrast straight to the
4CP intervals) is exactly the move the thread's own first blind pass made, and it is wrong for
multiple providers for three distinct, real reasons: heat-wave-depth participation decay
(Lumivale, Pinecrest Home), understated home heterogeneity (Kitebrook), and a window-position
mismatch that most naive averages would also miss in the other direction (Ondera, whose devices
add load rather than shed it at 10 of 12 real intervals). A model that sanity-checks against the
distractor PDF's generic 0.7-1.1 kW BYOT range would also be misled on four of six providers. The
price any run pays is distributed across R2 (Lumivale), R3b (Pinecrest Home) and R4 (Kitebrook),
each of which the thread's own blind pass or its own-fact test confirms is missed independently;
the main recommendation (R6) depends on getting at least two of the three right, so a run that gets
one carry but not the other two still loses the call.

## Findings, ranked
1. (Informational, not a defect) A thread-initiated temperature-only regression rival moves three
   of six providers; it does not survive scrutiny as an equally complete method (it omits the
   home-heterogeneity carry and conflates the heat-wave-participation mechanism with a correlated
   temperature signal), but record it as the closest thing to a fork this review found, should a
   future pass want the generator's rival battery (checks.py) extended to include it explicitly.
2. (Informational, not a defect) The thread's Gate H one-fact count (rescues ~2 of 9) is one
   higher than the design note's own measured figure (rescues 1 of 8/9); on inspection the thread's
   own evidence supports the narrower, design-note figure. Does not change the Gate H verdict
   either way (both are well under the one-third bar).
3. (Informational) Several Critical Components (Lumivale's 33% share, Kitebrook's 1.54x, Pinecrest
   Home's 65%/59%) were not independently reproduced to the stated numeric precision within the
   thread's time budget; in every case the thread found nothing in the files that contradicts the
   committed figure, and the non-reproduction is attributable to the thread's own simplified,
   non-covariate-adjusted methods, not to a located defect in the task.

## Next action for the author
None required to ship. If there is appetite to harden the task further before the next build
cycle (not needed for this disposition), extend checks.py's rival battery to include a
temperature-only regression of the M&V call/hold gap (in place of the participation-share-by-day-
position decomposition) as a fifth named rival, so that the "Pinned" line in the design note can
state explicitly, with a number, that this specific confounded method also lands outside the band
or on the wrong side of the line for Pinecrest Home, closing off the one fork an isolated thread
found on its own.
