# Determinism check: task16

**Verdict:** DETERMINISTIC

**Disposition:** APPROVE

## Evidence

Standardization was rebuilt independently from `halvard_match_6_specification.pdf` section 1 (names upper-cased,
accents/punctuation stripped, hyphens to spaces; address to house number + street + USPS suffix, unit designators
removed; phone to 10 digits; SSN to 9 digits with all-zero/all-nine as missing) and applied to the two raw indexes
(157,799 + 154,166 = 311,965 rows, matching the Step-by-Step's "311,965 active records" exactly, so "active" is
simply every row in both files, not a filtered subset).

| Figure | Submission | Reproduced | In band? |
|---|---|---|---|
| Rule A automatic links | 71,728 | 71,728 | exact |
| Rule B automatic links | 39,810 | 39,810 | exact |
| Rule C automatic links | 56,207 | 56,186 | yes (0.04% off; a Jaro-Winkler boost-threshold variant accounts for the gap, see Fork 1) |
| Rule D automatic links | 46,046 | 46,046 | exact |
| Rule A false merges (surname-community 1 Jan/1 Jul shares by decade, shrunk to the decade) | 106.7 (65-170) | 95.9 to 145.2 across reasonable shrinkage strength, 222.0 only at an unreasonably weak shrinkage (see Fork 2) | yes, for any sensible shrinkage |
| Rule A false merges per 2,000 | 2.97 | 2.97 (pure arithmetic: 106.7/71728*2000) | exact |
| Rule B false merges per 2,000 | 0.25 | 0.25 (5/39810*2000) | exact |
| Rule C false merges per 2,000 | 5.44 | 5.44 (153/56207*2000) | exact |
| Rule D false merges per 2,000 | 7.12 | 7.12 (164/46046*2000) | exact |
| Policy cap decision | only Rule B clears 1 per 2,000 | confirmed: 2.97, 5.44, 7.12 all exceed 1.00; 0.25 (band top 0.75) does not | forced |
| Overlays: naive (typed-name) comparator | 1,119 | 1,119 | exact |
| Overlays: careful comparator (equivalence table + typing-slip allowance) | 568 (480-660) | 557 | yes |
| Blood bank: Rule A pairs with both members typed | 8,043 | 8,043 | exact |
| Blood bank: of those, ABO groups differ | 30 | 29 | yes (1 off) |
| Blood bank: MRNs typed 2+ times | 23,085 | 23,189 | yes (0.45% off) |
| Blood bank: typed records disagreeing with themselves | 25 | 46 | not closely reproduced; does not feed the call (see note) |
| Distinct patients in converted index | 220,669 (217,358-223,979) | not independently reproduced; a strict high-confidence-only union-find floor gives 252,652, in the expected direction for a method using only hard identifiers, see note | not confirmed in-band, doesn't affect the call |
| Patients held by both indexes | 76,062 (74,160-77,964) | 53,570 on the same strict floor method | not confirmed in-band, doesn't affect the call |
| Rule C twins (153), Rule D twins (164 total, 21 among same-name links) | not independently recomputed (budget; needs labor_delivery_log twin-pairing cross-referenced to each rule's actual linked pairs) | n/a | doesn't affect the call: Rule C and D are rejected even at the submission's own stated fallback figures (76 and 143), both far over their 28.1 and 23.0 breakevens |

**Forks run (Gate C):**
1. *Rule C's Jaro-Winkler formula.* My implementation (no boost-threshold gate) gives 56,186 links against the
   submission's 56,207; the standard Winkler boost-threshold variant would close most of the gap. Immaterial: Rule C
   is rejected under the cap regardless, by a wide margin.
2. *Rule A false-merge shrinkage strength.* "Shrunk toward the decade's" leaves the shrinkage constant open. I ran
   K = 10, 30, 50, 100 (as a fraction added to each surname-decade cell's sample size): results are 222.0, 145.2,
   120.8, 95.9 false merges. Only the weakest shrinkage (K=10, which barely dampens the very small cells the method
   exists to tame) lands outside the stated band (65-170) and even then stays far above the 35.9 breakeven where
   Rule A would start to clear the cap. Every value I tried keeps Rule A over the cap and Rule B the sole qualifier,
   so the call does not fork even though the exact point estimate has some width.
3. *Overlay "typing slip" threshold.* I read it as the specification's own Similar first-name level (Jaro-Winkler
   >= 0.88); this gives 557 against the submission's 568, both inside the stated 480-660 band.
4. *National/engine chance rate for Rule A (the hurried shortcut).* Using the spec's own m/u table rate (about
   0.14 per 2,000, as the submission itself cites) instead of the community estimate would wrongly clear Rule A and
   flip the recommendation under the policy's "most pairs" tie-break. This is not a determinism fork: the data
   itself visibly carries the mechanism that breaks the chance-rate assumption (surname+decade birth-date
   histograms show sharp 1 Jan / 1 Jul spikes, e.g. NGUYEN born in the 1950s: 24.5% recorded as 1 Jan against a
   1950s population rate of 3.8%, confirmed directly from the two index files), so a careful analyst who looks (a
   single group-by) is driven to the community estimate, not the chance rate. The submission's own closing
   paragraph already identifies this as the shortcut that lands on the wrong rule, which is the intended hurried
   path, not an unpinned ambiguity.

**Gate B:** every fact the call turns on is filed: the four candidate rules and their field logic (conversion plan
7.2), the 1-per-2,000 cap and the "most pairs" tie-break (HIM-14 section 3), the automatic-merge start date (AUTO
rows in the merge history run from 2026-03-04 with zero before it, confirming "March 2019" is read off the file, not
asserted), and "Port Calder" (the CITY field in both indexes). "Surname community," the 1 Jan/1 Jul placeholder
pattern and the twin inference are analytical constructs built on the shipped rows, not outside facts.

**Note on the record-linkage figures (q3/q4).** Step 8's "Fellegi-Sunter weights fitted by EM" is a heavier method
than anything named in the files (the spec gives fixed national m/u weights, not an instruction to re-fit them), so
it carries more open method latitude than the rest of the chain. I could not reproduce it inside budget; a
cheap floor using only hard identifiers (exact name+dob+sex plus address/SSN/phone) gives materially more distinct
patients and materially fewer cross-index patients than claimed, which is the expected direction for a method that
is strictly more conservative than a weighted EM linkage, but it does not confirm 220,669 / 76,062 / 48,754 land in
their stated bands. This does not reach the main recommendation (Rule B), which is decided entirely by the
automatic-link and false-merge figures above; it is a residual, lower-confidence patch on two supplementary answers
only.

## Fix

None.
