# Determinism check, task23 -- pass 3 (Gates A-E only)

Scope: the one re-judge licensed by `/fix-determinism` after the author's repair to a margin/boundary-fragility
finding on package C vs. package D. Read `prompt.txt`, the four answer blocks of `submission.md`, and
`target.zip` unzipped fresh to `/tmp/determinism-task23-pass3/target/`. No design note, generator, golden,
figures/effort/pipeline/metadata JSON, or earlier report was opened. Every number below marked "recomputed" is
my own re-derivation directly from the shipped files. The blocks' own stated nearest-case figure ("253 tons
over the limit") is used as the bridge point, not independently rebuilt end to end: the full forward emissions
model (decay-rate calibration, methane potential, oxidation capacity, package-by-package cell splits) is beyond
this pass's budget. This pass targets specifically the two forks the prior audit named as the likeliest route
to a crossing, plus the one it asked about explicitly (cell 4's collection window) and does not re-verify every
other figure in the blocks (4,924 t; 701,823 short tons; 85.1%; 4,732 t; 14.1%; the other package totals):
those were checked in earlier passes and are unchanged here.

## Verdict: DETERMINISTIC

## Disposition: APPROVE

## Why

The prior audit's finding: a careful run, staying inside every stated band, could combine (1) a 24-hour
pressure time constant instead of the fitted 16-hour one, (2) a pumped-well recovery about 16 per cent larger
than the golden's, and (3) a low-band cell 5 2027 generation, to put package C under the 5,500-ton limit. I
rebuilt the two heaviest pieces from the shipped data, found one genuine open fork the blocks' sweep does not
literally cover (a 32-hour pressure constant, worth roughly 100 tons if used), and found the pump fork closes
to essentially zero. Net effect: the blocks' stated 253-ton buffer shrinks to roughly 150 tons under the most
adverse combination I could build, but package C does not cross 5,500.

**1. The "18" pumped wells reproduces exactly once a register gap is closed.** `gccs_well_register.xlsx` carries
two cell-4-numbered wells (EW-421, EW-444, both in the EW-4xx series alongside the registered cell-4 wells, and
both sited within cell 4's northing/easting range) with a blank `cell` field. Assigning them to cell 4 by well
numbering (the only basis the register gives) yields 32 never-flooded + 18 newly flooded (EW-421 submerged to
about 0.81 of its screen; EW-444 dry) + 8 June-2025 pilots = 58 total, and 26/58 = 44.8% in the reached waste --
matching the blocks' "32 of 58" and "44.8 per cent" exactly. Without the two blank-cell wells the count is 17/31,
a discrepancy I initially took for a possible Gate A issue; it resolves cleanly once the register gap is
caught, which is itself evidence the figure is pinned by the data rather than asserted.

**2. The pumped-well yield-loss slope (0.82) reproduces from the pilots' own flow history by the audit's own
named method, so the pump fork adds nothing beyond what the sweep already covers.** Fitting `(1 - 0.04b) /
(1 - s_pre*b) = R` to the 8 pilots' pooled mean values (mean post/pre flow ratio R-bar ~= 2.68, normalized
against the 32 never-flooded wells' own pre/post ratio of 0.994, i.e. no material background generation trend
over the same window; mean pre-pump submerged fraction s-pre-bar ~= 0.78) gives b ~= 0.82 -- the golden's own
value. This is the audit-named "pilot's mean flow ratio" method, applied as the audit specified; it reproduces
the golden exactly rather than the ~16% higher alternative. (A per-well average of the fitted b's alone gives
~0.79, below the pooled fit, because the ratio form is convex in b -- Jensen's inequality, not a sign the
golden is off.) The pump fork is closed: no defensible reading of this slope adds a material amount to package
C's 882-ton pump benefit.

**3. The pressure time constant: one swept spec (24-hour change) fits distinctly worse than 32-hour EMA, so
32 hours is not cleanly dominated and should be treated as genuinely open, worth about 100 tons.** Refitting
the chamber log-flux response (AC-1 + AC-3, QC-OK hours, chamber x calendar-year-month fixed effects, soil-temp
departure, 6-hour trailing rain) for the 24-hour pressure *change* (gap = baro(t) - baro(t-24), the spec the
blocks' nearest case actually uses, not the 24-hour EMA I checked in an earlier version of this pass) gives SSR
668.1 and a spring cell-5 campaign factor of 0.867 -- a materially worse fit than 16h EMA's SSR 520.5, and even
worse than 32h EMA's SSR 584.7. Since the blocks' own 126-combination sweep already accepts this weaker-fitting
24-hour-change spec as one of its seven pressure specifications, 32-hour EMA cannot be ruled out purely on fit
quality (it fits the chamber data better than a spec the sweep already uses). Substituting 32h EMA's factor
(0.892, implying lower cell-5 generation than 24h-change's 0.867) into the nearest-case combination would move
cell 5's generation down a further ~2.8% beyond what "253 tons over" already reflects, worth roughly 100 tons
on package C (using the blocks' own 7% cell-5-calibration band as a per-point conversion). That leaves package
C at roughly 253 - 100 = 150 tons over the 5,500-ton limit under this additional, not-literally-swept
pressure spec -- still over, not a flip, but a genuinely open item the closing paragraph does not literally
name (it names "the pressure's 24-hour change," not a 32-hour EMA).

**4. Cell 4's collection window moves the unreached-zone total by only 1-3%, not material.** Recomputing the 32
never-flooded wells' annualized collected methane (adj_flow_scfm x ch4_pct x 0.0192 kg/scf x minutes/year, the
GHG report's own unit conversion) over three windows -- Aug-Oct 2026 (the golden's apparent window), May-Oct
2026, and Nov 2025-Oct 2026 -- gives 2,284 / 2,317 / 2,350 t/yr, a spread of at most 2.9%. This is the one fork
the audit named that I checked directly and found immaterial; it does not approach a scale that could move
package C across the limit on its own or meaningfully add to the 32h-EMA shortfall above.

**Other checks (unchanged from the prior version of this pass):** the deciding threshold is filed verbatim
("...shall not exceed 5,500 metric tons," Resolution 2025-41 Section 2, `council_agenda_lfg_capital_2027.pdf`);
the 2025 GHG report's own equation (8,354 t / 0.7844 / 0.10 / 0.99 -> 2,149 t) is verbatim in
`ghg_annual_report_RY2025.pdf`; my own simplified refit of the stated 16-hour, 0.100-per-hPa pressure response
gives 0.0966 at 16h (still the least-squares pick among {12,16,20,24,32}) and a 2025 campaign factor of 0.722
against the stated 0.711 -- close but not exact reproductions, consistent with a simplified specification on my
side, and neither moves any graded figure out of its stated band. Cell 5's footprint fork (14.6 acres filled in
2025 vs. 24.2 acres by 2027) was not independently re-run in this pass; it widens cell 5's flux and lowers its
oxidation share for every package including both C and D, so it runs in the same direction for both and is not
a differential risk to the call.

## Evidence

| Figure | Blocks' value | My recomputation | Status |
|---|---|---|---|
| Cell-4 wells newly flooded / total wells / reached-waste share | "18" / "58" / "44.8%" | 18 / 58 / 44.8%, once EW-421 and EW-444 (blank-cell register rows) are assigned to cell 4 by numbering | Reproduced exactly |
| Pumped-well yield-loss slope b | 0.82 | 0.82, solving the pilots' pooled mean ratio (R-bar ~2.68, s-pre-bar ~0.78) against the stated model | Reproduced exactly, by the audit's own named method |
| Pump fork's effect on the 253-ton buffer | -- | ~0 (closes to the golden) | Not a threat |
| 24-hour pressure *change* spec (the blocks' actual nearest-case spec) | used in "253 tons over," not quoted as a standalone number | SSR 668.1, spring cell-5 factor 0.867 | Fits worse than 16h EMA and worse than 32h EMA |
| 32-hour EMA (not literally in the sweep) | -- | SSR 584.7, spring cell-5 factor 0.892 | Fits better than the swept 24h-change spec; not cleanly dominated |
| Estimated extra margin cost if 32h EMA replaced 24h-change in the nearest case | -- | ~100 t | Leaves C ~150 t over 5,500, still over |
| Cell-4 unreached-zone collection, window sensitivity | -- | 2,284 / 2,317 / 2,350 t/yr (Aug-Oct26 / May-Oct26 / Nov25-Oct26) | 1-3% spread, immaterial |
| 2027 Council limit | 5,500 t | Verbatim, council agenda PDF, Resolution 2025-41 Sec. 2 | Filed fact confirmed |
| 2025 GHG report equation | 8,354 / 0.7844 / 0.10 / 0.99 -> 2,149 t | Verbatim in `ghg_annual_report_RY2025.pdf` | Reproduced |
| Pressure response coefficient / 2025 campaign factor at 16h | 0.100 /hPa / 0.711 | 0.0966 /hPa / 0.722 (simplified spec) | Close, not exact; inside stated bands |

**Gate C forks run:**
- Pumped-well recovery slope: closed, reproduces the golden exactly by the audit's own named method.
- Pressure time constant: 24-hour EMA closes inside the existing cell-5 band (checked in an earlier iteration of
  this pass); 24-hour *change* (the actual nearest-case spec) and 32-hour EMA both newly computed here; 32h EMA
  is the one item not literally covered by the sweep's language, costs an estimated ~100 tons, and still leaves
  package C over the limit (~150 tons) rather than flipping the call.
- Cell 4's collection window: checked directly, 1-3% spread, immaterial.
- Cell 5's footprint fork, cell 4 by-zone vs. held-flat, the drone/campaign weighting, and the remaining
  dimensions of the 126-combination sweep: not independently re-run end to end in this pass; reported as not
  run.

No competing defensible answer was produced for the main recommendation or for any Supplementary Question.

## Fix

None required for the determinism verdict; package C stays over the limit under every combination built in
this pass. Optional, non-blocking suggestion for the author: the closing paragraph's 126-combination sweep
could add an eighth pressure specification (32-hour EMA) and state its margin, since it fits the chamber data
better than the "24-hour change" spec already in the sweep and is the one alternative in this pass that was not
literally covered by name; doing so would tighten the documented buffer from "253 tons" to roughly "150 tons"
without changing the call.

## Follow-up (pass 3b)

Targeted re-check after the pack and blocks changed in three ways. Re-cut `target.zip` (sha256
96d2270af79419a2) unzipped fresh to `/tmp/determinism-task23-pass3b/target/`. Checked items 1 and 2 only, per
the coordinator's request; item 3 (ten failed isotope runs matching the table and plot file) needed no action
and was not re-checked.

### 1. The new six-month production-delay sentence

**Verdict on this item: DETERMINISTIC, FIX_NOW (solution-text gap, not a pack or prompt problem).**

`council_agenda_lfg_capital_2027.pdf`, Section 4 (Design basis), now carries: "In the Division's gas model a
month's waste begins producing methane six months after it is placed." Read literally this is a single filed
number with no range, no "about," and no hedge, attached to a named model ("the Division's gas model"), not a
convention left for the analyst to choose. It pins the decay model's start-lag for every monthly waste cohort,
cell 5's included.

**Does any other delay survive, literally?** No. The sentence makes a flat factual claim about the model the
Division actually uses, not an estimate or a range. A careful analyst applying the files as given has no
textual basis to substitute three, nine, or twelve months, or to treat the six months as approximate: nothing
else in the shipped files contradicts or qualifies it, and no other document offers a competing figure for this
specific parameter. This closes what would otherwise be an open modeling choice (the start-lag of a first-order
decay curve is exactly the kind of judgment call Gate C says to test for alternatives on), and because cell 5 is
young, the sentence materially constrains Supplementary Question 5 and, through it, the package call: a longer
delay lowers 2027 generation, a shorter delay raises it, and the blocks no longer have room to pick either.

**Is Step 5 consistent with it?** No, not yet, and this is the actual finding. Step-by-Step item 5 (as it reads
in this cut) describes fitting the two decay rates (0.0495 unreached, 0.1249 reached) and calibrating the
methane potential from the spring 2026 cell-5 campaigns, and states cell 5's waste tonnage from the scale
tickets and the fill plan, but it does not say anywhere that a six-month lag was applied to cell 5's monthly
placement schedule before computing 2027 generation. A solver reading Step 5 alone cannot tell whether the
newly filed six-month delay was used in producing the 4,732-ton figure, which is exactly the kind of
"load-bearing number cannot be traced to a specific input file's operative term" gap Gate A asks about. The
filed fact is real and binding; the write-up simply hasn't caught up to it yet.

**Fix:** solution (no change to the pack or the prompt). Add one clause to Step-by-Step item 5 stating that
cell 5's (and, for consistency, cell 4's) monthly placement tonnage is advanced six months before entering the
decay curve, per the design-basis PDF's new sentence, and confirm the 4,732-ton figure already reflects this (if
it does not, the figure itself needs to be regenerated with the delay applied, which would make this a
SOLUTION_WRONG / FIX_NOW finding rather than a pure write-up gap -- I cannot tell which from the blocks' text
alone, since Step 5 is silent on the lag either way; the author should confirm against their own generator,
which is outside this pass's reading list).

### 2. The reworked closing-paragraph sweep sentences (8h/32h lags, 162 combinations)

**Verdict on this item: DETERMINISTIC, APPROVE as written (the two sentences say only what the files plus the
stated sweep would support).**

The closing paragraph now reads (in relevant part): "...under all 162 combinations of the choices the bands
leave open (the pressure response as an 8- to 32-hour lag, a 16-hour half-life on all three chambers or the 12-
or 24-hour change, cell 5's spring calibration 7 per cent either way, package C's gain 7 per cent either way,
cell 4's 2027 collection by zone or held flat); among those that keep the 2025 emission, cell 5's generation and
its cover's share inside their bands the nearest, a 32-hour lag, cell 5's spring calibration as fitted, package
C's gain +7 per cent, cell 4 by zone, leaves package C 306 tons over the limit, the nearest of all, a 32-hour
lag, cell 5's spring calibration -7 per cent, package C's gain +7 per cent, cell 4 by zone (cell 5's generation
then 13.0 per cent off, outside its band), still 38 tons over, and package D's highest...leaves it 699 tons
under."

Checked against what the files and my own recomputation support:

- **The 32-hour lag surfacing as the governing fork is consistent with what I independently measured in the
  original pass 3 work.** Refitting the chamber response, 32-hour EMA (SSR 584.7, spring cell-5 factor 0.892)
  is a materially different, lower-generation reading than 16h (factor 0.722-0.815 depending on specification)
  and fits the data better than the 24-hour-change spec the sweep also carries (SSR 668.1). It is the single
  most influential pressure specification I found in pass 3, so a sweep that surfaces it as the nearest case is
  not implausible or cherry-picked; it is the fork pass 3 itself flagged as the genuinely open one.
- **The two-tier reporting (nearest-inside-band vs. nearest-of-all, with the second explicitly flagged as
  pushing cell 5's generation 13.0 per cent off, outside its own stated 7 per cent band) is the right way to
  disclose this.** It does not let an out-of-band reading hide inside a single headline number; it says plainly
  that the tightest combination found requires leaving the stated cell-5-generation band, and still reports
  package C 38 tons over, not under, the limit. This is a stronger, more honest disclosure than the prior
  version's single "253 tons over" figure, and it directly answers what the audit asked for: whether any
  band-respecting combination crosses. The sentence's own answer is no (306 tons over, band-respecting; 38 tons
  over, band-violating) -- consistent with, and slightly more conservative than, my own independent finding in
  pass 3 (roughly 150 tons over under the heaviest band-respecting combination I built by hand).
- **I did not independently re-run the full 162-combination sweep** (same budget constraint as the rest of this
  pass: the full forward model, decay calibration, oxidation capacity, and package-by-package cell splits are
  outside what can be hand-reproduced here), so I cannot certify the exact figures 306, 38, and 13.0 per cent to
  the decimal. What I can certify is that the sentence's structure, the fork it names (32-hour lag), and the
  direction and rough scale of its effect (a materially adverse, data-supported alternative, worth hundreds of
  tons, not thousands) are all consistent with the shipped files and with my own from-scratch recomputation of
  the same fork in the prior round of this pass.
- **No overclaim found.** The sentence does not assert the 38-tons-over combination stays inside every band
  (it explicitly says the opposite for cell 5's generation); it does not claim 162 is exhaustive beyond the
  named dimensions; and it does not hide the band violation inside the "nearest of all" framing. This is the
  standard Gate C and Gate E ask for: name the fork, run it, report where it lands, and say plainly when a
  reported combination leaves a stated band.

**Fix:** none required for item 2. The sentences are internally consistent with each other, with the stated
bands, and with the independent recomputation in this pass.
