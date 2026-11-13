# Determinism check, task23 (Gates A to E)

**Verdict:** DETERMINISTIC on the call (package D); NOT fully pinned on two graded figures (2025 actual emissions and the pressure-response chain feeding cell 5). Not shown to flip the call.
**Disposition:** FIX_NOW (answer-block edits only; no change to what solvers see), plus one rival run by the author before approval.

## Evidence (recomputed on a fresh unzip, by the blocks' stated method)

| Item | Block value (band) | Mine | Status |
|---|---|---|---|
| 2025 report from its equation: 8,419 / 0.7844, 10% oxidation, 0.99 destruction | 2,166 | 2,166.8 | reproduced |
| Cell 5 municipal waste through Oct 2026 (MSW, MSW-TS, MSW-COM, MSW-RES; arealess tickets to the day's active cell; VOID dropped) | 574,197 (1%) | 574,196.6 | reproduced, but see Finding 1 |
| same, dropping VOID and REISSUE | n/a | 570,798.8 (-0.6%) | inside band |
| same, as filed | 648,207 | not re-run (sample reproduces) | |
| Pressure response, log flux on 16 h exponential gap (chamber-month levels, soil temp, rain; QC OK) | 0.100 per hPa; mean campaign factor 0.711 | 0.059 (0.067 with soil moisture added); factor 0.82 | NOT reproduced |
| 2025 actual emissions | 4,923 (10%: 4,431 to 5,415) | 4,250 to 4,310 (lags 8 to 20 h, -12 to -14%); model-free arithmetic ratio of campaign-window flux to chamber-month mean 0.77 gives about 4,590 (-6.8%) | model-based routes fall outside the band |
| Lag choice | 16 h wins on fit | with soil moisture, SS is lowest at 16 h of {6,16,40,100}; without it 8 to 12 h fit slightly better | consistent with the block |
| Oxidation capacity, daily cover at 15 C | 27.0 g/m2/d | 27.08 (per-cover capacity and half-saturation, shared temperature factor) | reproduced |
| Q10 | 1.89 | 1.21 per 10 C in my form | not reproduced; form of the temperature factor is unstated |
| Call margin | C 5,538 vs 5,100; D 4,479 | C band floor 5,150 (still over); D band ceiling 4,793 (still under) | call holds inside every stated band |

Not recomputed (budget): cell 4 well split (+85.4, +26.5, +157.9), decay rates, cell 5 generation (3,769), the 2027 package table, and the 2027 oxidation share (17.1). Their input files (well register, wellfield, recirculation log, fill plan, options paper) are present.

## Findings

1. **Step-by-Step step 1 is worded wrongly.** It says "voids and their reissues dropped". The golden value 574,197 is reproduced only by dropping VOID rows and keeping the REISSUE rows (the reissue carries the corrected weight; the void carries the wrong tare). Dropping both gives 570,799, still inside the 1 per cent band, so the figure is safe. Fix (solution): "voids dropped, their reissues kept".
2. **Pressure-response estimate is not robust to the fit specification (Gates A and C).** A standard reading of the block's method (log-linear, 16 h exponential mean minus current reading, chamber-month levels, soil temperature, rain, QC OK, station clock +8 h to UTC, campaigns in daylight time) gives beta about 0.06, a campaign factor of about 0.82 and 2025 emissions near 4,250 to 4,300, which is 13 to 14 per cent under 4,923 and outside the 10 per cent band. The block's 0.100 and 0.711 did not come out of my fit. A careful solver would plausibly land at 4,250 to 4,600. The same factor scales the 2026 cell 4 and cell 5 campaign levels, so the cell 5 generation (3,769, 12 per cent band) and cell 5's methane potential inherit it: at a factor of 0.82 instead of 0.711, cell 5 generation falls about 15 per cent, outside its band. The call stays: package C is estimated to remain over 5,100 only barely (rough estimate about 5,190 if cell 5's share falls 15 per cent, which is a hand estimate, not a run), and D stays under.
   Fix (solution, then author's rival run): (a) state in the Step-by-Step the exact fit specification that yields 0.100 (dp definition, covariates, rows kept) so the method is reproducible; (b) run my specification above as a rival in `checks.py` and either widen the 2025 band (to about -15 per cent on the low side, with the bridge items' bands moved to match) and the cell 5 band, or show why it is ruled out by a named fact in the files; (c) confirm package C at the weak-correction end stays above 5,100 and report its margin. If C falls under 5,100 on the rival, this becomes SEND_BACK (the call is then not forced).
3. **Oxidation temperature factor (Q10 1.89) is not reproduced** in the common form (1.21 per 10 C with capacity 27.08 matching). The 17.1 per cent (4-point band) depends on the form used at normal soil temperature and on the cover area assigned to cell 5; the daily-cover capacity matches. Low-to-moderate risk. Fix (solution): state the temperature-factor form and the cover area basis for cell 5 in the Step-by-Step, and add the alternative form as a rival in `checks.py`.
4. **Gate B:** every decisive fact I checked is filed (limit and selection rule in the options paper, design capture, package dates and costs, report equation, campaign table, 2019 study, fill plan, leachate start date July 13, 2026). The recommendation's terms (package, collection efficiency, oxidation, leachate, pumps) appear in the inputs. No missing-fact finding.
5. **Gates D and E:** the asks are pinned and carry units. The bridge for the report is order-dependent but the prompt pins the order ("the order of its own equation"). The prompt bundles several figures in one sentence, but each has its own unit and a single reading. No finding.

## Fix summary
- prompt: none
- input_files: none
- solution: Finding 1 wording; Finding 2 fit specification and rival run, with band changes or a named ruling-out fact; Finding 3 temperature-factor form and cover area basis stated.
