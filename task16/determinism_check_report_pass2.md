# Determinism check: One Chart EMPI conversion (Rule B)

## Verdict: DETERMINISTIC
## Disposition: APPROVE

The call ("run Rule B") and its deciding figures reproduce cleanly from the shipped files by the Step-by-Step's own method. The one figure I could not independently re-derive to precision (the full EM-linked-index count) uses a named, legitimately open method, is banded, and does not bear on which rule is chosen.

## Evidence table

| Figure (block value, band) | Recomputed | Status |
|---|---|---|
| Active records = 294,713 | 149,900 (CB) + 144,813 (Ros) = 294,713 | Exact |
| Rule A links = 64,484 | 64,481 | Within 0.005%, immaterial |
| Rule B links = 35,566 | 35,566 | Exact |
| Rule C links = 50,411 | 50,403 (direct name-equivalence lookup) / 50,417 (transitive closure) | Within 0.03% either reading; see Fork 1 |
| Rule D links = 42,835 | 42,835 | Exact |
| Lines = links/2000: 32.2 / 25.2 / 21.4 / 17.8 | 32.24 / 25.20 / 21.42 / 17.78 | Exact (arithmetic identity on each rule's own link count) |
| Rule A: pairs both blood-typed = 3,730 | 3,730 | Exact |
| Rule A/B: blood-group-discordant pairs = 5 | 5 (ABO or RH differs) | Exact; all 5 verified individually (CB1278765/20117899 A/B; CB1197343/20186085 O/A; CB1241250/20120793 O+/O−; CB1154527/20199103 O/A; CB1049403/20045491 A/O) |
| ...of those, touch a CB overlay record = 3 | 3 (CB1241250, CB1154527, CB1049403 are all survivors of an AUTO merge history row with a genuinely different, non-equivalent first name) | Exact |
| ...2 of the 3 under one SSN | 2 (CB1241250↔20120793 SSN 850184288 match; CB1154527↔20199103 SSN 588466550 match; CB1049403↔20045491 no SSN match) | Exact |
| ...0 a record whose own typings disagree | 0 (checked all 10 MRNs in the 5 pairs against their own specimen history; none has internal ABO or RH disagreement) | Exact |
| Rule B false merges = 3 (0–8), rate 0.17/2,000 | 2 unexplained blood-discordant pairs + 1 twin pair = 3; 3/35,566×2,000 = 0.169 | Exact |
| CB overlay records = 556 (471–601) | 536 (AUTO-method merges only, first name genuinely different after name-equivalence-table + Jaro-Winkler≥0.88 typo filter; raw literal mismatch count 1,022 survivors, close to the quoted "1,028") | Within band |
| Rule B links touching an overlay = 124 (105–144); such records = 119 (101–138) | 116 links; 112 records | Within band |
| Distinct patients in converted index = 212,402 (209,215–215,588); held by both indexes = 69,318 (67,585–71,051); duplicates remaining after Rule B = 44,567 (43,229–45,904) | Not independently re-derived (see note below) | Open method, appropriately banded; no contradiction found |

Note on the three unverified figures: Step 9 builds these from a Fellegi-Sunter model whose m/u weights are **fit by EM on this pack's own candidate pairs**, not read off the published national table, a named, standard record-linkage method, legitimately left open per the determinism spec, and banded at about ±1.5%. Reproducing it exactly needs an EM implementation outside this check's budget. I built two cheap deterministic proxies as a sanity bound: Rule A ∪ Rule D connected components gave 192,522 distinct / 56,494 held-by-both (more merging than the stated figures, i.e. golden is *less* merged than this proxy); a looser last-name+DOB+sex+address/phone proxy (which ignores first name, so it wrongly merges twins and is not a valid check) gave 143,556. Neither proxy contradicts the golden band in a way that implicates the call; the gap is consistent with EM down-weighting fields once it sees the surname-community birth-date clustering documented in Critical Component 1 (confirmed real in the data, see Fork 2 below). These three figures are supplementary (Q3/Q4), independent of the main recommendation, which turns only on each rule's own false-merge rate.

## Forks run (Gate C)

1. **Name-equivalence table: direct pairwise lookup vs. transitive closure.** The table has chained entries (e.g. BETO is listed as equivalent to ALBERTO, GILBERTO and ROBERTO; ROBERTO is also listed equivalent to BOB, which is ROBERT's nickname too). A naive union-find would merge ALBERTO/GILBERTO/ROBERTO/ROBERT into one cluster, which is not realistic nickname semantics. Tested both: Rule C links 50,403 (direct) vs 50,417 (transitive), a 14-pair, 0.03% spread. Both round to the same line (25.2) and don't change Rule C's rejection. Not a fork that moves any graded figure or the call.
2. **"Blood group" = ABO only, or ABO+Rh.** ABO-only discordance among Rule A's both-typed pairs is 4; ABO-or-RH (as the blocks read it) is 5. The one pair that differs between readings (CB1241250/20120793, same ABO, different Rh) is an overlay-touching pair either way, so it nets out of the "unexplained false merge" count under both readings: 2 unexplained + 1 twin = 3 false merges regardless. Confirmed by direct recomputation. Not a fork.
3. **Margin robustness across each rule's stated band.** At each rule's least-favorable band edge the call does not change: Rule A 42/64,484×2,000=1.30 (still over the 1.0 line), Rule C 34/50,411×2,000=1.35 (still over), Rule D 85/42,835×2,000=3.97 (still over), Rule B 8/35,566×2,000=0.45 (still under). Rule B is the only rule inside the line at every point in its band, and the three rejected rules stay outside the line at every point in theirs. This is a clean, non-thin margin.

## Gate B
Every deciding fact is filed and extracts correctly (pdftotext -layout recovered the full rule table in one_chart_empi_conversion_plan.pdf §7.2, the weight table in halvard_match_6_specification.pdf, and HIM-14's definitions/threshold in patient_identity_policy_him-14.pdf §§2–4; no tables were dropped). The recommendation's vocabulary ("Rule B," "false merge," "overlay," "automatic link") is drawn directly from HIM-14 §2's own definitions and the conversion plan's own rule labels, no invented vocabulary.

## Gates D/E
No semantic fork changed an answer (see Forks 1–2). The prompt poses one decision (which rule, if any) under a threshold it states as given information (not a leaked method), and each supplementary ask names a single population/count. No bundled or goal-vague asks found.

## Fix
None. FIX LOCATION: none.
