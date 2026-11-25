# task4 determinism check, pass 3 (Holistic Audit v4, determinism mode)

In-house replay of the platform's Holistic Audit v4 (Step 0, Part A, Part B), 2026-11-25. Cut audited: prompt.txt
1fa45a2f98db0eb39ba3de57d665e867, target.zip 0440ca1dac58ae15927361a52098864d, submission.md
94e96ee0642c64cf52a6fec48310623b (manifest of workspace /tmp/holistic-task4-determinism-yhot0roz, 23 input files,
four answer fields, tags left out). No runs yet. Earlier reports not opened.

- **Verdict:** DETERMINISTIC
- **Disposition:** FIX_NOW (answer-block edits only: four bands, two missing sentences and one rejected-route
  definition; nothing solvers see)

## Step 0

Golden present (all four fields carry computed values). Inputs belong to the task: Wrenfold, Brighouse, Calder Vale,
Maplestead, Lindqvist Q26-1187, Pennine, FS-04 issue 3 and TQ-02 all appear in the pack and every named file is
shipped. Pass.

## Part A: correctness

Every deciding figure was derived from the shipped files before comparison. The method: the dockets deduplicated on
docket and line (2,562 dropped), blank codes filled from products (5,229), renumbered accounts mapped. Each type's
weekly deliveries fitted on logs (level, trend, two harmonics, a temperature hinge picked on a half-degree grid). The
checks rebuilt with the empties (TQ-02 records only unbroached fulls and the coupled container; FS-04 2.1 counts the
empties awaiting collection), as line sales times days since the last docket at the account over seven. Holding
fitted as a + c*s + d*s*weeks-between. Lot survival exponential in age, WLS on the counted. The store fitted across
the 18 beers on their means. The FS-04 2.1 to 2.3 week-by-week path, from the count to 20 September 2027.

**figures_checked** (mine / author / agree):

| Figure | Mine | Author | |
|---|---|---|---|
| Loss over the year to the count | 2,477, 1,095, 220, 1,055, 237; 5,085 | 2,477, 1,095, 220, 1,055, 237; 5,084 | agree |
| Trade rise, count to summer peak | 5,087, 2,141, 784, 598, -27; 8,584 | 5,087, 2,141, 784, 598, -27; 8,583 | agree |
| Store at its fullest in season | 4,500, 2,365, 2,197, 1,608, 257; 10,927 | 4,502, 2,366, 2,196, 1,608, 257; 10,929 | agree |
| Planning-case largest shortfall | 4,652, 2,518, 762, 1,828, -442 | 4,653, 2,519, 761, 1,828, -442 | agree |
| Worst weeks | 26 Jul, 26 Jul, 19 Jul, 20 Sep, 20 Sep | inside each stated set | agree |
| Hot case (second of 2017 to 2026) | 9,043, 3,001, 1,110, 1,836, -442 | 9,047, 3,002, 1,110, 1,836, -442 | agree |
| Covers vs runs 3,500/1,500/1,200/1,200/600 | buy, buy, hire, buy, none | buy, buy, hire, buy, none | agree |
| Checks' common fall term | -0.879 (se 0.059) | -0.88 (0.06) | agree |
| Holding constants; per container sold, raw/rebuilt (K50) | 2.26, 2.11, 2.02, 2.96, 3.03; 0.28/0.95 | same | agree |
| Survival rate (1-e^-lambda); on-site share; alive | 10.2, 7.6, 2.8, 11.4, 11.8%; 0.59, .44, .44, .32, .60; 21,764, 13,387, 7,578, 8,204, 1,776 | same | agree |
| Store fit: cover, run share | 0.347, 0.508 (se 0.019) | same | agree |
| Condemned in year; count-week deliveries | 225, 121, 34, 63, 11; 3,376, 2,075, 535, 1,556, 237 | same | agree |
| Checks vs lots at the count; trade-in-level route | 367, -92, -27, 834, 19; 5,019, 2,426, 735, 2,662, -423 | 367, -92, -27, 834, 19; 5,020, 2,426, 734, 2,662, -423 | agree |
| Ablations: no rebuild / no lots loss | 2,363, 1,708, 456, 1,856, -425 / 2,973, 1,715, 615, 930, -631 | 2,364, 1,709, 456, 1,856, -425 / 2,974, 1,716, 614, 930, -631 | agree |
| Sensitivities: cover ±20%, loss -20%, holding -20%, deliveries -5% | 4,141.../5,165..., 4,316..., 3,968..., 3,952... | 4,142.../5,167..., 4,317..., 3,969..., 3,953... | agree |
| Empties as whole / half delivery (trade rise) | 10,195 / 7,692 | 10,194 / 7,691 | agree |

**mismatches** (none on a deciding figure; all on the blocks' claims about alternatives, Part A step 5):
- The rejected route in the Final Recommendation ("records read as they stand": -996, 285, -898, 187, -751) does not
  rebuild. Summer 2026's weeks of cover is not defined (which weeks, which pairing, ratio of means or mean of
  ratios). My variants give a store total of 6,714 to 6,837 (author 6,691) and file K50 -729 to -871, K30 230 to 296,
  K20 -882 to -938, FIR 235 to 296, KIL -756 to -759. Same covers. The "without the store" row has the same problem:
  3,229, 1,903, -480, 1,107, -582 against 2,977, 1,929, -443, 1,057, -603, same covers.
- Linear survival: mine 5,122, 2,612, 765, 2,095, -371, author 5,047, 2,603, 763, 2,031, -386 (the linear fit's
  method is unstated). Same covers.
- Step 9's "nearest approach ... 50 litre kegs 4,207 (707 from 3,500)" holds only for the author's battery. Single
  rivals the battery lacks reach 4,144, and triples of unrefuted rivals reach 3,711 (below).

**decision_reproduces:** yes. **correctness:** correct.

Internal consistency: figures agree across the four blocks and totals add. There are two rule-5 gaps, where I had to
try readings until one matched:
1. Step 6 never says how the year's loss follows from the survival curve. I tried three. Only "each lot's survivors
   a year before the count less its survivors at the count", sum of lot x (S(a-1) - S(a)), gives 2,477. lambda x
   (fleet at the count) gives 2,346, 993 FIR, 4,831 total. (1-e^-lambda) x (fleet at the count), the blocks' own
   "10.2 per cent of the fleet a year", gives 2,224. Both fall outside the C3 bands.
2. Step 7's main store fit does not say which week each Monday is paired with (only the 156-Monday variant says
   "the week that ended the day before"). The means fit does not care (0.509/0.508), but the beer-weeks variant does
   (below).

Minor and immaterial: 10 of the 24 duplicate check lines differ by one container. "A line entered twice taken once"
does not say which entry is kept. I kept the first. The bound is 10 containers across 5,621 checks, so this was not
computed further.

## Part B: determinism

**Committed call:** buy K50, K30 and FIR, hire K20, no cover for KIL, read on the planning-case shortfalls above.
Margins: K50 +1,153 over 3,500, K30 +1,019 over 1,500, K20 761 above nil and 439 below 1,200, FIR +628 over 1,200,
KIL 442 below nil.

**Deciding steps:** the checks rebuilt for empties, the store under the 2027 runs, and the loss read from the lots.
Each one alone, dropped, flips at least one cover (reproduced above).

**Fork list run in code** (planning shortfall K50, K30, K20, FIR, KIL; flips marked):

| # | Fork | Result | Status |
|---|---|---|---|
| 1 | Loss as lambda x fleet at count | 4,562, 2,486, 760, 1,775, -453 | same call; C3 out of band (see fix) |
| 2 | Linear survival | 5,122, 2,612, 765, 2,095, -371 | same call; worse deviance per blocks |
| 3 | Losses accrued per week, not per container delivered | 4,588, 2,432, 758, 1,801, -436 | same call, in band |
| 4 | Count level: week of 30 Nov at normal / count week's own dockets / last 4 weeks | 4,755.. / 4,806, 2,629.. / 4,482.. | same call; actual week puts K30 trade rise 2,251 above band 2,227 |
| 5 | Deliveries: no temperature / one harmonic / no trend / bend 15 / bend 19 | 4,632.. / 5,037.. / 4,881..(KIL -413) / 4,601.. / 4,728.. | same call; harmonic and trend terms are significant in the fit |
| 6 | Deliveries seasonal-naive: 2024 to 2026 mean / 2026 alone | 6,127, 2,760, 800, 1,927, -397 / 8,820, 3,088, **1,228**, 2,045, -423 | 2026-alone flips K20; ruled out by FS-04 3.2 (normal weather) since summer 2026 ran +0.45 C above normal |
| 7 | Checks as recorded (no empties) | **2,363**, 1,708, 456, 1,856, -425 | flips K50; ruled out by TQ-02 (fulls are "unbroached"), FS-04 2.1 and the checks' own fall -0.879 (se 0.059) |
| 8 | Empties as half a delivery | 4,055, 2,306, 676, 1,835, -437 | same call; ruled out by the dockets: weekly accounts' checks fall 3 to 6 days after the dray (mean 4.65), twice-weekly 2 to 3 (2.6), never mid-cycle |
| 9 | Empties as a whole delivery | 5,758, 2,905, 895, 1,815, -450 | same call |
| 10 | Fall left free (0.879 x empties) | 4,375, 2,420, 725, 1,831, -440 | same call; K50 trade rise 4,808 below band 4,827 |
| 11 | Holding without the weeks-between term | 4,162, 2,381, 717, 1,843, -438 | same call; ruled out by the fit (t = 13.6, 8.2, 2.3, 3.7, 5.4) |
| 12 | Store: beer-weeks pooled, Monday vs the week it opens (0.337, 0.546) | 4,723, 2,568, **888**, 1,896, -430 | same call; K20 shortfall above band 871; store K30 2,415, K20 2,323, FIR 1,676, KIL 269, total 11,253, all above bands |
| 13 | Store: beer-weeks pooled vs the week ended (0.348, 0.506) | in every band | same call |
| 14 | Store: summer 2026 weeks of cover (hurried) | **3,229**, 1,903, **-480**, **1,107**, -582 | flips K50, K20, FIR; ruled out by brew_plan_2027 (summer runs 2,400/1,400 vs 400/300 in every racking of the record) and the 18-beer fit, 0.508 of a run (se 0.019) |
| 15 | Store at its fullest over the whole plan year (prompt has no "in the season") | FIR 1,645 (25 Oct), KIL 266 (27 Dec) | FIR at the band top, KIL 1 over 265 |
| 16 | Depots, wash, repair: fitted level / depot full and wash queue regressed on their weekly files, rest scaled | 4,452.. / 4,447, 2,352, 738, 1,826, -436 | same call, in band |
| 17 | Same, depot empties bays held at the count | 4,144, **2,232**, 690, 1,835, -433 | same call; K30 below band 2,255 |
| 18 | Same, empties bays, in-wash and repair all held | 3,738, 2,093, 630, 1,846, -431 | same call; repair held is ruled out by the wash log (K50 repair stock 241 in Dec to 432 in Jul) |
| 19 | Depots, wash, repair all held at the count | **2,468**, 1,691, 436, 1,891, -427 | flips K50; ruled out by depot_stock_weekly (0.19 per delivery, corr 0.78) and the wash queue (0.107 per delivery) |
| 20 | Maplestead flat at Schedule B's average | 3,873, 2,299, 709, 1,838, -442 | same call alone; K50 trade rise 4,747 and C1 8,130 below bands; ruled out by Schedule B's own label ("average ... over the twelve months to September 2026") against K50's 2026 season at 1.27 times its twelve-month mean (peak week 1.83) |
| 21 | Maplestead left out | **1,549**, **955**, 548, 1,498, -442 | flips K50, K30; ruled out by FS-04 3.4 (signed agreement) |
| 22 | Float 2/5 | 5,497, 2,920, 883, 1,994, -417 | ruled out by FS-04 7.1 |
| 23 | Strongest rival: trade calibrated to the lots' level (alive less site) at the count, checks' model for the rise | 4,450, 2,546, 767, 1,750, -441 | same call |
| 24 | Trade in level, checks for requirement and lots for fleet | 5,019, 2,426, 735, 2,662, -423 | same call |

Every pair of 17 plausible rivals was run (forks 1, 3, 4, 5, 8, 10, 11, 12, 16, 18, 20, 6 three-year). Only pairs that
include an already-refuted fork (8, 11, 18, 20) flip, and they all flip K50 to hire: half + 18 (3,141), half + 20
(3,335), 10 + 18 (3,461), 11 + 18 (3,247), 11 + 20 (3,459), 18 + 20 (3,045). Every triple of 14 unrefuted rivals
holds every cover. K50's nearest is 3,711 (last-4 level + fall free + empties bays held), K30 2,048, K20 562 to 968,
FIR 1,716, KIL -458 to -387.

**Strongest rival (rule 2):** fork 23, the trade calibrated to the lots, is the design that uses both independent
instruments. Same covers. The depot and wash stocks regressed on their own weekly files (fork 16) are also more
rigorous than the blocks' one-week ratio. Same covers.

**Closest call:** the K50 purchase. With Maplestead flat (fork 20) it sits 373 above the run. Flat with the depot
empties bays held at the count (fork 17, unrefuted) files 3,416, a hire. I rule fork 20 out on Schedule B's
"twelve months" label and the dockets' seasonality. A flat 1.4 a line is a face-value default the data make false,
not a second reading. So the call stands.

**unpinned_forks:** none that move the call. The Gate C margin test passes: no unrefuted single, pair or triple
crosses a line.

**Data anomalies (step 6):** duplicate dockets, blank codes, three codings, renumbered accounts, unprefixed lots and
duplicate check lines are all resolved by the data. The GUEST-20L lines (all 1,800 20 litre lines) are read from the
account's F-series dockets, which is forced since no docket carries GUEST.

**Giveaways (step 7):** none. No input states a cover or a decisive figure (the 2519/4653 hits in the route plan are
row references), no deliverable copy, no script.

**Determinism:** pinned.

## Fix (solution only; nothing solvers see)

1. Step 6, add: "the year's loss is each lot's survivors a year before the count less its survivors at the count
   (the lot times its survival at its age a year earlier less at its age now; no lot was bought in the year)."
2. Step 7, state the pairing for the fit and the projection. Then either widen the store bands to take the
   beer-weeks pooled against the week each Monday opens (K30 2,415, K20 2,323, FIR 1,676, KIL 269, C2 total 11,253)
   and the K20 planning band to 888, or refute it with a figure from the files.
3. Widen: K50 trade rise lower bound to 4,808 (fork 10); K30 trade rise upper to 2,251 (fork 4, count week's own
   dockets); K30 planning shortfall lower to 2,232 (fork 17); KIL store upper to 266 (fork 15; the prompt asks for
   the store "at its fullest under next year's brew plan" without "in the season").
4. Final Recommendation and Step 9: define summer 2026's weeks of cover (weeks, pairing, aggregate) so -996, 285,
   -898, 187, -751 rebuild, or give the rejected route as approximate. My rebuilds land at K50 -729 to -871 and FIR
   235 to 296, same covers.
5. Step 9: restate the nearest approach with the forks above (K50 4,144 alone, 3,711 in three) and add the Maplestead
   refutation figure (K50 2026 season 1.27 times its twelve-month mean).
6. Optional: name which of two differing duplicate check entries is kept (immaterial).
