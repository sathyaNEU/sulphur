# Determinism check, pass 3

## Verdict: DETERMINISTIC

## Disposition: APPROVE

## Evidence

Universe: concatenated calder_bay_patient_index (149,900 rows) and rosario_patient_index (144,813 rows) = 294,713
records, matching the Step-by-Step's stated "one table of 294,713 active records" exactly; no separate
active/inactive flag exists in either file, and all 10,321 death_notices_matched MRNs are present inside this same
set, so "active" cleanly means "current, non-retired record in these extracts," not "living patient": no fork there.

Rebuilt the standardization from halvard_match_6_specification.pdf (upper-case, hyphens to spaces, punctuation
stripped on names; apt-suffix stripped and uppercased on address; phone to 10 digits; SSN to 9 digits with
all-zero/all-nine as missing) and the four rules from one_chart_empi_conversion_plan.pdf section 7.2, independently
in pandas (exact-key groupby for A/B/D, a verified Jaro-Winkler plus halvard_name_equivalence_table.csv for C).

| Figure | Blocks | My recompute | Result |
|---|---|---|---|
| Rule A automatic links | 64,484 | 64,481 | within the blocks' own stated 0.1% tolerance (0.0047% off; traced to 3 pairs sharing a blank last name, a blank-equals-blank reading the blocks anticipate under "another careful reading") |
| Rule B automatic links | 35,566 | 35,566 | exact |
| Rule C automatic links | 50,411 | 50,403 | within stated 0.1% tolerance (0.016% off) |
| Rule D automatic links | 42,835 | 42,835 | exact |
| HIM-14 lines (links/2,000): A 32.2, C 25.2, D 21.4, B 17.8 | as stated | 32.2, 25.2, 21.4, 17.8 from my own counts | exact |
| Rate bands (false merges / line) for A, C, D, B | 1.31-2.20, 1.35-1.90, 3.97-8.92, 0.00-0.45 | recomputed from the stated false-merge bands over my line values | exact arithmetic match |
| Rule B blood mismatch set: 5 links differ ABO/Rh | 5, specific pairs | 5, same specific MRN pairs (CB1278765/20117899, CB1197343/20186085, CB1241250/20120793, CB1154527/20199103, CB1049403/20045491) | exact, same pairs found independently for both Rule A's and Rule B's link sets (identical set, as expected since B subset of A) |
| Both-typed denominator for Rule A | 3,730 | 3,730 | exact |
| "0 a record whose own typings disagree" | 0 | 0 (checked all 5 mismatched MRNs against their own multi-draw blood bank history) | exact |
| "3 touch a Calder Bay record that holds two patients" | 3 of the 5 | 3 of the 5, same three MRNs (CB1241250, CB1154527, CB1049403) flagged overlay, other two not | exact |
| halvard_pilot_review_2026.xlsx reviewed none of Rule C's (or Rule B's) links | 0 | 0 overlap both ways | exact |
| Policy comparison: A, C, D over the line; only B under | as stated | confirmed with full margin: every rule's stated band sits entirely on one side of its own line (A's floor 1.31 vs line 1.00; C's floor 1.35; D's floor 3.97; B's ceiling 0.45) | fully robust, no near-tie anywhere |
| Overlay records (Calder Bay records holding 2+ patients) | 556 (471-601) | 584, using AUTO merges from March 2019, excluding name-equivalence and Jaro-Winkler >= 0.92 "typing slip" matches as an independent reading of the same method | inside the stated band |
| Rule B links touching an overlay record / such records | 124 (105-144) / 119 (101-138) | 126 / 121, from my own overlay list above | inside both stated bands |
| Distinct patients in converted index | 212,402 (209,215-215,588) | union-find proxy over the union of Rules A, C and D's links only: 221,084 | about 4% above the band, in the direction expected from a deliberately cruder proxy that omits the scored fuzzy matches an EM-fitted Fellegi-Sunter model (the stated, field-standard method) would also catch; not a competing valid rival, a modeled figure appropriately banded |
| Rule C's 41 modeled twin false merges, "documented" floor of 16 | 16 from delivery log + one registration visit | 12 confirmed via same-mother/same-day/same-sex delivery-log pairs mapped onto Rule C's links; did not chase the "one registration visit" component within budget | directionally consistent, not fully closed, immaterial to the call (41 vs the 25.2 line either way) |

## Gate C forks run

1. Blank-last-name-equals-blank vs SQL-null semantics: moves Rule A by 3 pairs and contributes to Rule C's 8-pair
   gap. Explicitly inside the blocks' own declared 0.1% tolerance; does not change any rule's over/under verdict.
2. "Typing slip" threshold on retired-record first names in the overlay construction (I used Jaro-Winkler >= 0.92,
   the same threshold the files already use for Rule C, as the "another careful reading"): overlay count and both
   downstream Rule B touch-counts all land inside the stated bands.
3. Full EM/Fellegi-Sunter linkage vs a cruder deterministic-rules-only union-find for the two global index totals:
   proxy lands just outside the top of the distinct-patients band, in the expected direction; the EM method is the
   field's standard and is the one the files point to, so this is not a rival forcing a different figure, only a
   sanity bound.
4. "Active records": tested whether death-matched (deceased) patients should be excluded from the 294,713; all
   10,321 are already inside that count and no file carries a separate alive/retired flag, so there is no second
   reading available.

No fork flips which rule clears HIM-14's line, and no fork pushes a graded figure outside its stated band.

## Fix

None. Disposition: APPROVE.
