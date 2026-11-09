# task12 design note: Northvale Oat's 2027 treatment

## Draw

**Card.** `.claude/skills/fingerprint/cards/task12.json`, architecture v1, registered 2026-11-08, guard verdict WARN
(no BLOCK). Domain Marketing & Consumer Research (`marketing-consumer-research`), house subdomain
`new-product-innovation`; the nearest client task type serving forecasting is conjoint, choice and willingness-to-pay
analysis (revealed choice behaviour and segment response to price, read from a household purchase panel). Objective
Forecasting & Predictive Modeling. Shape 02 (a forecast across the four quarters of 2027) feeding one dial: the
portfolio standard's treatment band.

**The decision.** Northvale Oat Co., a Canadian plant-based beverage maker, launched Northvale Oat (three oat
beverage items) on 6 April 2026 (panel week 2026-W15) at Foxmere Fresh (premium), Greenleaf Market (natural) and the
two regional mainstream chains, Northglen Foods and Marche Belvoir, with a launch price to 3 May and media in
2026-W15 to W20. The two discounters, ValuWay and Trade Basket, listed it on 8 June (2026-W24) with a three-week
listing price. Loyal Grocer, the national mainstream chain, listed it on 21 September (2026-W39) with a three-week
multibuy (also run in the two regional chains) and media in 2026-W39 to W42. The portfolio standard gives each launch
of the past year a 2027 treatment from its forecast 2027 share of category litres (Canada, the household panel's
projected purchases, at the distribution and everyday shelf price the line holds at the review, no promotional or
media weeks): below 2.0 per cent delist, 2.0 to below 2.9 hold (stay listed, no 2027 support), 2.9 to below 3.8
support (fund the 2027 media and sampling plan), 3.8 or more expand (a dedicated co-packer line). The share is
compared with the bands before it is rounded. The review meets on 23 November 2026, ahead of the co-packer's 2027 slot
confirmation on 1 December, so the treatment is set on the panel's data to 2026-W44.

**Data-native sentence.** In a household purchase panel a household can only try a new line on a shopping trip to a
store that stocks it, and each household does most of its mainstream shopping at one chain, so a line listed first in
premium stores and the regional chains reaches the households that shop there first, mostly premium-price shoppers,
and reaches Loyal Grocer's own shoppers, mostly mainstream, only when Loyal Grocer lists it; the panel carries both
the sorting and the listing dates without a column for either.

**The two analytical judgments that decide the call** (each alone leaves the line outside hold):
1. *Maturity: the Loyal Grocer wave has not settled.* At 2026-W44 its buyers are one to six weeks past their first
   purchase and still buying the line at 32.0 per cent of their own litres (17.4 in 2026-W42, 9.5 by W44) against a
   settled 6.5. Every route that reads the wave from its own weeks (Parfitt-Collins, the recent share, the latest week,
   each wave at its recent share, price groups read from the latest weeks) lands in support or expand.
2. *Composition: the waves settle at different levels because they are different households.* Each buyer's settled
   share is set by its price group, which no column holds and which is rebuilt from what the household paid per litre
   in 2024-W01 to 2026-W14. The April buyers' litres are 76 per cent premium-price, the discounter wave's 66 per cent
   value and the Loyal Grocer wave's 74 per cent mainstream, so the Loyal Grocer wave's level has to be borrowed from
   long-standing buyers of its own price groups: one level pooled across long-standing buyers (3.1 to 3.3 at every read
   from 8 to 20 weeks) or the April level lent to it (3.0 to 3.3) lands in support.

**A third judgment, carried by the share figure and the asks.** The Loyal Grocer listing also put the line on more of
the long-standing buyers' shelves, so a settled share measured against all their category litres is partly measured
at an older distribution. The standard's clause 3(c) files the forecast at the review's distribution, so the golden
reads each group's settled share against the litres bought where the line is stocked (the purchase lines joined to the
retail audit by banner and week) and carries each household at its own share of buying in stores carrying the line at
2026-W44. Read against all category litres instead, the share is 2.2 rather than 2.4: the same treatment. Buyers were
also caught in high-buying phases (their category litres since launch run 13.9 per cent above their own 2024-25 rate,
non-buyers' 0.5 per cent), so 2027 is weighted by each household's 2024-25 litres; the window's litres give 2.5, the
same treatment. Households not yet buying come in at their price group's first-purchase rate in the only weeks
that match the forecast's basis (2026-W43 and W44: every banner listing the line, no promotion, no media), about 50,000
first-time buyers in 2027 adding 0.03 of a point (2.3 without them). Counts are the static panel raised to the
16,116,449 households every 2026 factor in the register adds up to. The asks add their own judgment: a settled share
becomes a chance of buying at all only through each household's expected purchases.

**Strategy label.** WORKS IN FORM (`stumping/references/sulfur-strategies.md`, Part A: heterogeneity that pooling
hides, live form "the groups respond differently AND the decision weights them to a population whose mix differs from
the sample, with the group property rebuilt from a history"), with the second judgment from Part A's unfinished
outcomes in its live form (completion differs by a unit no pooled factor captures, here the trial wave, and the field's
standard completion move, the most mature cohort's repeat, files a named wrong answer). Card strategy
`population_selection`: every judgment is about who the buyers of each wave are and when they were caught.

**Abstraction sentence, against the nearest builds on file.** The nearest approved build a reviewer could hold beside
this one is mark175 (permits on vacant lots once services arrive, access extended first to well-built runs). The
sentence both share would be "a rate measured on early entrants selected on a favourable property overstates later
entrants". It does not make them one build. mark175's property is a neighbour interaction, read where the unit sits,
and there is no second judgment. Here the property is each household's own pre-launch price kind, read from its own
history; it decides a long-run level that shows only after the household's own tenure fade; and the largest forward
contributor after the April wave has not finished that fade, so its level has to be borrowed across waves by kind.
Against task1 (forecasting, composition): task1's members ride a second entity's clock (the tutor's tenure hazard);
here the clock is the household's own time since trial. Against mark132 and mark124: differentiated on the card (no
replacement restarts a curve here; the kind is the household's own, not its group's).

**Guard WARNs answered.** `three_rules.task_type`: the Task type line names conjoint, choice and willingness-to-pay
analysis, the client task type whose "choice behaviour" and "segments react differently to price" this build's deciding
step is. `overuse.objective` and `overuse.gate_g`, `repeat.gate_g`: forecasting is the client's most wanted objective
and the Gate G mechanism honestly is a forecast the correctly read past does not pin; the shell, question form (how
much) and deliverable set differ from task10 and task7. The forum is the brand director's delegated call under the
portfolio standard. Against the last three live cards (task10, task7, task2) the axes are redrawn: the decisive pattern
is G17 (the Loyal Grocer wave's level borrowed by kind because its own fade is not identified), with G6 and G13 behind
it; the context artifact is the trade calendar and media flighting the golden reads for its unpromoted weeks; the
forcing event is the 23 November portfolio review the standard sets; the strategy is `population_selection` rather than
`composition_mix`, which is overused in the last twelve and would name only the second judgment.

**People** (drawn with `guard.py names --geo Canada`): Gabriel Sloan, brand director; Angela Reyes, vice-president
finance and owner of the portfolio standard; Brian Mueller, client service lead at the panel provider; Kimberly
Stanley, trade marketing (owner of the trade calendar); Eric Hernandez, the agency lead at Halyard & Finch; Mary
Gonzales, consumer insights, the golden's author.

**Sources, one line each** (all constructed by `generator/`; provenance in `metadata.json`):
- The household panel's purchase lines for the plant-based beverage category, 2024-W01 to 2026-W44 (the spine, 447,844
  rows).
- The panel's household register (province, size, bands, joined and left weeks, yearly projection factors; 18,000
  rows).
- The panel's product master (item, brand, own label, segment, pack in mL or L), the banner code table and the week
  calendar.
- The retail audit's weekly weighted distribution of each Northvale item by banner.
- Northvale's 2026 trade calendar and the agency's 2026 media flighting.
- The portfolio standard (the governing document: the WHAT, the bands).
- Distractors, unlabelled: the brand-health tracker wave of September 2026 and the agency's 2027 support proposal.

## Default path

The field's own method for a launch's long-run share from a household panel is Parfitt-Collins: share equals the
penetration the line reaches among category buyers, times its repeat (the line's share of its buyers' own category
purchases once repeat has settled), times the buyers' buying-level index. A competent analyst runs it with its textbook
caveats:

1. Clean the purchase lines (receipt rescans, returns, multibuy prices on the first unit, item codes that lost a
   leading zero, the mL and L pack sizes, the banner recoding, the date-format change at the panel platform migration)
   and keep households reporting from 2024-W01 to 2026-W44.
2. Penetration P: the share of category buyers that have bought Northvale Oat by 2026-W44, 21.0 per cent.
3. Repeat R, read where repeat has had longest to settle: the launch-month buyers (first purchase 2026-W15 to W18, 26
   to 29 weeks of tenure) take 17.1 per cent of their own category litres in the last seven weeks.
4. Buying-level index B: buyers' weekly category litres since launch against all category buyers', 1.34.
5. Share = P x R x B = 4.8 per cent of 2027 category litres, at or above 3.8: expand.

Ends on: 4.8 per cent of 2027 category litres, expand.
Golden: 2.4 per cent of 2027 category litres, hold.

## Stump sentence

A competent analyst runs Parfitt-Collins with its textbook caveats (penetration reached, repeat read from the most
mature buyer cohort, the buyers' buying index since launch), files about 4.8 per cent of 2027 category litres and puts
the line in the expand band, when the launch cohort it reads repeat from is three-quarters premium-price litres and
the Loyal Grocer wave that now holds a third of the forecast's litres is mainstream and still in its first weeks, so
every 2027 buyer has to be carried at the settled level of its own price group, read from same-group buyers with
sixteen weeks or more of tenure: about 2.4 per cent, hold.

## Deep reasoning

Task type: new-product forecasting from a household purchase panel, filed under conjoint choice willingness to pay analysis (revealed choice behaviour and segment response to price), which serves forecasting in the taxonomy.
Domain test: the deciding quantity is a launched grocery line's 2027 share of category litres projected from household-panel trial and repeat, the consumer-panel new-product forecast; the field's estimator is Parfitt-Collins (penetration x repeat x buying level) with repeat read from the most mature trial cohort.
Swap: "the line holds 2.4 per cent of 2027 category litres once each wave's buyers are carried at their price group's settled share of the litres they buy where it is stocked" with a hospital's nouns ("the clinic holds 2.4 per cent of 2027 visits once each referral wave is carried at its income band's settled share of care") loses the share of a household's own category requirements, price-tier reversion to own label, stocked-store buying and the banners' staged listings, and stops making sense.
Layer 1: receipt rescans duplicating a receipt's lines (the scanning app re-uploads after a timeout); returns as negative units; multibuy totals on the first unit line with zero on the rest (the receipt parser); ValuWay item codes that dropped a leading zero (one retailer feed); dates written day-first before the panel platform's March 2025 migration; banner codes recoded on 30 June 2025 (NTG to NGF, MBL to MBV); pack sizes in mL in older master rows and L in 2026 rows; a blank deal indicator on about 2 per cent of lines; households joining and leaving with part weeks; none placed to be caught and none moving the call (`checks.py` R2).
Layer 2: estimand identification, heterogeneity reweighted to the forecast population (composition by a rebuilt price group) with an unfinished outcome (the Loyal Grocer wave's honeymoon) whose settled level is borrowed across waves within group, read per stocked litre at the review's distribution.
Decisive step: carry every household that has bought the line into 2027 at the settled share of its own price group, the group rebuilt from what it paid per litre in 2024-W01 to 2026-W14 and each group's level read only from that group's buyers with sixteen weeks or more of tenure, instead of the most mature cohort's repeat, one pooled long-tenure level or each wave's own recent share.
Not semantics: every field, code, unit and the standard's definitions read correctly still leave Parfitt-Collins with mature-cohort repeat at 4.8 per cent; no term carries the difference between 4.8 and 2.4, which lives in how each wave's buyers are composed and how far they are into their own fade.
Not rule application: the standard files the quantity, basis and bands and no method; the family a competent analyst reaches for (Parfitt-Collins with mature or current repeat and any buying index, each wave at its own recent share, the share in unsupported weeks, latest-week shares, the launch level for all, one pooled long-tenure level, the April level lent to the Loyal Grocer wave, price groups read from the latest weeks) spreads 1.7 to 7.2 per cent across four bands; the standing family once the Loyal Grocer wave's fade and the waves' composition are both read from the data spreads 2.1 to 2.6 per cent (2.8 with window litres), one band.
Analyst test: a strong analyst who cleans every purchase line, applies the standard, and runs Parfitt-Collins with repeat from the launch-month cohort and the buyers' buying index since launch files 4.8 per cent of 2027 category litres and the expand band, the default path's answer; the launch cohort is premium, the Loyal Grocer wave mainstream and still fading, and carried at their price groups' settled shares the line holds 2.4 per cent, hold.
Estimand: the portfolio review standard (portfolio_review_standard_2026.docx, section 3) files the line's share of the plant-based beverage category's litres in panel weeks 2027-W01 to 2027-W52, Canada, as the household panel's projected purchases measure it, households not yet buying the line included, at the distribution and everyday shelf price the line holds at the review and with no promotional or media weeks in 2027; section 4 bands the share before it is rounded.
No decoy: nothing is planted; no memo, deck, tracker or stakeholder figure states a 2027 share, a repeat rate or a band for the line, and the two distractors (a brand-health tracker wave and the agency's 2027 support proposal) carry no forecast of it.
No certified replay: no published or certified figure is reproduced to recover the method; the standard's bands are thresholds, and no shipped artifact computes the line's 2027 share on any basis.
Chain: (1) see that the Loyal Grocer wave's high and falling share is an unfinished honeymoon, not a level, so its level has to come from buyers who have finished; (2) rebuild each household's price group from its 2024-W01 to 2026-W14 price paid per litre and see that the waves are different households (76 per cent premium, 66 per cent value, 74 per cent mainstream litres), so neither a pooled long-tenure level nor the April level transfers; (3) read each group's settled share from that group's buyers with sixteen weeks or more of tenure, per litre bought where the line is stocked, and carry every buyer, the Loyal Grocer wave included, at its own group's level and its own share of stocked-store buying at the review; (4) weight each household by its own 2024-25 category litres grown to 2027, and bring in households not yet buying at the first-purchase rate of the weeks that match the forecast's basis; (5) the litre-weighted 2027 share against the standard's bands.
Judgment: two statistical judgments on the panel's own records: that the Loyal Grocer wave's 32.0 per cent is a fade still in progress (17.4 in its first unpromoted week, 9.5 two weeks later) whose level its own five weeks cannot identify (its fitted asymptote ranges 0.0 to 8.9 per cent across resamples), and that the waves differ in kind and not in maturity alone, shown by the rebuilt price groups' mix by wave and by a pooled long-tenure level that stays at 3.1 to 3.3 per cent whatever tenure it is read from because the long-tenure buyers are the April wave's premium households.
Hidden by: the panel's weekly share and the buyers' pooled repeat both look high but settling, the launch cohort's repeat looks like the textbook settled value, the weeks without support before September show a low share that is missing the Loyal Grocer wave, and the April level is the natural thing to lend a young wave.
After the notice: (1) once the Loyal Grocer wave's falling share is seen, its settled level has to come from somewhere, and the natural turns (its own last weeks, its own fitted asymptote from five points, the April level, one pooled long-tenure level) land in support or expand or swing with the read, so the run has to borrow from long-tenure buyers of the same kind, which needs the price group it has not built; (2) once the waves are seen to differ, it has to decide whether by maturity or by kind, and only a price group rebuilt from pre-launch purchase prices, joined to the master's brands, separates them; (3) it then has to read the borrowed levels at the review's distribution and weight 2027 by litres the buyers will really buy, not the litres of the phase in which they tried.
One-fact test: the likeliest hint, "the Loyal Grocer buyers are still in their honeymoon", supplies maturity but not the level: executed with the April wave's settled level it lands 3.0 to 3.3 (support) at every read from 4 to 20 weeks, with the discounter wave's level 1.8 to 2.0 (delist), and with the mean of the two earlier waves 2.4 to 2.7 (hold by the numbers, with the price-group levels and the buyer figures still off); no single sentence also builds the price group.
No replay: the call does not re-derive any figure in the pack and no stated number is wrong; the bands are filed thresholds and the share is computed forward from purchase lines.
Pinned: every rival a careful analyst would run was run on the cut pack (`generator/checks.py` R3 to R7): the price group cut by terciles, a 30-40-30 split, fixed cuts at 2.20 and 2.95 or k-means, read from 14, 16 or 20 weeks with 2024-25 or 2025 litres, per stocked litre or against all litres, all land 2.1 to 2.6 (hold), and every read from 8 to 24 weeks stays in hold; the window, last-52-week and whole-history litres land up to 2.8 (hold); households not yet buying at none or at the rate between the listings land 2.3 and 2.5 (hold); every route that skips a judgment lands outside hold except the recorded landings on the ladder.
Run forecast: method shortcut (Parfitt-Collins with mature-cohort repeat, the field's method on a buyer base it does not describe) for one run; an unfinished chain for the other (the Loyal Grocer wave's fade seen and its level borrowed from the April wave or one pooled long-tenure level: maturity taken, composition missed).
Strategy label: WORKS IN FORM, heterogeneity that pooling hides in its live form (the waves respond differently and the 2027 buyer base's mix differs from the mature cohort's, the group property rebuilt from each household's own price history), with unfinished outcomes in its live form (completion differs by wave, and the field's standard completion move, the most mature cohort's repeat, files a named wrong answer).
Lesson: a launch's long-run share is a sum over its buyer waves at their own settled levels, and a wave still fading at the review can only be valued through buyers of the same kind who have finished; the corpus has composition builds (task1, mark175) but none where a large forward group is still mid-fade and must borrow its level across groups by a kind rebuilt from purchase history.

## Survivor anatomy

Actor: the household is the actor and the deciding property, its price group and so its settled share of requirements, has no column in any file: the panel prints what was bought, where and for how much, the product master prints brands, own labels and pack sizes, and the group exists only as the household's own price paid per litre rebuilt across two years of purchase lines and the master.
Link: the signal is read through comparisons the field's method never asks for: each wave's price-group mix, each group's level from its own long-tenure buyers per litre bought where the line was stocked (the purchase lines joined to the audit by banner and week), and the Loyal Grocer wave valued through other waves' long-tenure buyers of its own group; no key offers either, and no sentence invites them.
Reflex: Parfitt-Collins with repeat from the most mature cohort and the buyers' buying index since launch sits at rung 0 and files 4.8 per cent (expand); the textbook alternatives at rung 1 (the launch level for every buyer, 4.4; current pooled repeat, 6.7) file expand.
Back-test: the textbook route validates on its own terms: the launch-month cohort has been in the panel longest, its share of its own litres in the latest seven weeks (17.1) sits above its July and August weeks, and its buying index is measured on the same buyers, so the analyst's own check confirms the easy route.
Second use: every file the decisive step reads ships for its own reason: the purchase lines are the panel delivery itself, the product master is how any share is computed, the household register carries the projection factors every Canadian figure needs, the audit and trade files are how a launch is read at all, and the standard files the bands; delete the decisive step and the pack is unchanged.
Shock: the movement the step recovers reads as ordinary launch behaviour: a share that spiked at each listing and settled, a trial curve that stepped and flattened; sorted on any shipped statistic (weekly share, wave size, promoted share), the golden's answer is not an interval of the sort and no wave is the pack's anomaly.
Pins: the WHAT is filed once in the portfolio review standard (the quantity, Canada, the 2027 panel weeks, the projected purchases, households not yet buying included, the distribution and everyday price held at the review, no promotional or media weeks, the bands read before rounding), in the company's own policy genre, and no sentence anywhere names price groups, waves, tenure, repeat or a method.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | 7 Dedicated organ | 8 Framing | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| R0 Parfitt-Collins, mature-cohort repeat, buying index since launch | the standard asks for a 2027 share | purchase lines and first purchases are rows | the field's method | none | yes | P x R x B | no | the standard frames no axis | readable |
| R1 the launch level for every buyer | none | the launch cohort is a date filter | the textbook repeat caveat | none | no | one ratio | no | none | readable |
| R1b the share in unsupported weeks | the standard excludes promotional and media weeks in 2027 | the trade and media calendars are files | a base-share reflex | none | yes | one ratio | no | none | readable |
| R2 each wave at its own recent share, or one pooled long-tenure level | none | first-purchase week is derivable | a cohort table | none | no | no | no | none | readable |
| R3 (decisive) every buyer at its own price group's settled share, read from long-tenure same-group buyers | no sentence names price groups, waves, tenure or settled levels | no group, wave or tenure column; the group is rebuilt from two years of prices and the master | not the field's method, which reads repeat from one cohort | none | no | no | every file read has its own use | the standard states no difference on the group or tenure axis | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "share of category litres" | the line's litres over the category's litres, from the panel's projected purchase lines | share of units | units give 2.95 (support) | standard 2(b) and 3(a) file litres |
| SF2 | the category | every item the master places in plant-based beverages, own label included | oat only | 3.85 (expand) | standard 2(a) names the panel's plant-based beverages category |
| SF3 | the 2027 window | panel weeks 2027-W01 to 2027-W52 | calendar days 1 January to 31 December | same call (2027-W01 starts 4 January) | standard 3(a); same call asserted |
| SF4 | projection to Canada | each household's 2026 projection factor | unweighted panel shares | same call (2.30 against 2.37) | standard 2(c); same call asserted |
| SF5 | households not yet buying | in the 2027 population, coming in at each price group's first-purchase rate in 2026-W43 and W44, the weeks that match the basis | none; the rate of the weeks between the listings | same call (2.33; 2.46) | standard 3(b) and 3(c); same call asserted |
| SF6 | distribution at the review | each household's stocked-store share at the 2026-W44 distribution | the year's average distribution | same call (2.31) | standard 3(c) |
| SF7 | everyday price, no promotion or media | 2027 carries no promoted or media weeks | the 2026 calendar repeated | the standard's basis; a repeated calendar is a different quantity | standard 3(c) |
| SF8 | static panel | households reporting from 2024-W01 to 2026-W44 | every household in tab in 2026 | same call (2.35) | same call asserted |
| SF9 | returns and rescans | a return nets its purchase line; a receipt uploaded twice is one receipt | keep both | same call (asserted) | same call asserted |
| SF10 | band edges | "2.0 to below 2.9" is hold, read before rounding | the rounded share | the golden sits 0.37 above 2.0 and 0.53 below 2.9 | standard 4 |
| SF11 | rounding | shares to one decimal at the end; the year is the sum of the quarters | rounded per quarter | same call | prompt rounding sentence |
| SF12 | the settled level's denominator | litres bought where the line is stocked, carried at the review's stocked-store share | all category litres | same call (2.21) | standard 3(c) names the review's distribution; same call asserted |
| SF13 | stocked litres | each banner's litres at the line's weighted distribution there that week | listed or not listed | same call (2.36) | same call asserted |
| SF14 | Canada's households | the static panel raised by 1.207 to the 16,116,449 households every 2026 factor in the register adds up to | the static panel's own factors, unraised | same call (the share is a ratio); every count 17 per cent lower | standard 2(c) raises purchases to all Canadian households; asserted |

## Ladder

Priced on the cut pack (`generator/checks.py`, `generator/rivals.py`; world seed 1208). The world's own forward runs
from 2026-W44 give 2.12 per cent (2.10 from households that have bought, 0.02 from first purchases in 2027).

| Rung | Construction | 2027 share | Band | Dies to |
|---|---|---|---|---|
| R0 | Parfitt-Collins: P 21.0 x launch-cohort repeat 17.1 x buying index since launch 1.34 | 4.8 | expand | the launch cohort is 76 per cent premium litres; the Loyal Grocer wave is mainstream and fading |
| R0b | Parfitt-Collins with current pooled repeat | 6.7 | expand | pooled repeat carries the Loyal Grocer wave's honeymoon |
| R1 | the launch level for every buyer | 4.4 | expand | later buyers are other kinds of household |
| R1b | the share in unsupported weeks (W27-W38; W21-W23; every week without promotion or media) | 1.7; 1.9; 1.86 | delist | the Loyal Grocer wave is missing |
| R1c | unsupported-week share scaled to the review's distribution | 6.6 | expand | carries premium-heavy rates to Loyal Grocer's mainstream shoppers |
| R1d | Parfitt-Collins with a buying index of one | 3.6 | support | the repeat is still the launch cohort's |
| R1e | the share in the last week / last four weeks / last seven weeks | 3.1 / 5.6 / 7.2 | support, expand | the Loyal Grocer wave is mid-fade |
| R2a | each four-week cohort at its own recent share | 5.8 | expand | the Loyal Grocer wave's own share is five times its settled level |
| R2b | price groups with each group's level from the latest weeks (W42-W44, last 8, last 13) | 3.0 / 3.9 / 3.6 | support, expand | maturity skipped |
| R2c | price groups with no tenure threshold | 3.0 (stocked), 2.7 (all litres) | support, hold | the Loyal Grocer wave's first weeks read as settled; recorded |
| R2d | one settled level pooled across long-tenure buyers (8 to 20 weeks) | 3.1 to 3.3 | support | composition skipped |
| R2e | each wave at its own settled share, the April level lent to the Loyal Grocer wave (4 to 20 weeks) | 3.0 to 3.3 | support | composition skipped |
| R2f | the same, the discounter wave's level lent (4 to 20 weeks) | 1.8 to 2.0 | delist (hold at 10 weeks, 2.01) | the discounter wave is 66 per cent value litres |
| R2g | the same, the mean of the two earlier waves lent (4 to 20 weeks) | 2.4 to 2.7 | hold by the numbers | an average of two other kinds; the price-group levels and buyer figures still off |
| R2h | each four-week cohort at its own fitted asymptote | 2.5 | hold by the numbers | the Loyal Grocer wave's asymptote is not identified (0.0 to 8.9 per cent across resamples) |
| R2i | the weekly share in W19-W23 (media inside), every unpromoted week with media, 2026 Q3 (the listing week inside) | 2.29, 2.06, 2.54 | hold by the numbers | each mixes media or promoted weeks the standard's basis excludes |
| R3 (decisive) | each buyer at its group's settled share per stocked litre (terciles of 2024-W01 to 2026-W14 price per litre; tenure 16 weeks or more), carried at its stocked-store share at the review, 2024-25 litres, first-time buyers at the basis weeks' rate | 2.4 | hold | |

Golden family on the cut pack: 2.17 to 2.57 per cent (terciles, 30-40-30, fixed cuts and k-means at tenure thresholds
14 to 20, 2024-25 or 2025 litres, per stocked litre, first-time buyers included); 2.09 to 2.35 against all litres; the
volume dial (2026 window, last 52 weeks, whole history) up to 2.78; every read from 8 to 24 weeks 2.08 to 2.57.
Margins: the golden family sits 0.17 above the hold floor and 0.33 below its ceiling, the dial 0.12 below it; the nearest routes outside hold are the
price groups read from W42 to W44 at 0.10 above 2.9, the latest week at 0.17 and the pooled long-tenure level at 0.25,
and below the floor the unsupported weeks W21-W23 at 0.11 and every week without promotion or media at 0.14. The truth
(2.12) sits 0.24 under the golden (its first-time buyers add 0.02, the golden's 0.03): inside a rebuilt price group the long-tenure buyers are more often of the higher
true kind than the Loyal Grocer wave's (the mainstream group's long-tenure buyers are 26 per cent premium households,
the Loyal Grocer wave's 1 per cent), which no visible method corrects (ten price groups move the share by 0.03); both
sit in hold.

## Closure table

| Axis | Reading | Closure |
|---|---|---|
| 1 Population | Canadian households in 2027 as the panel projects them, households not yet buying included | standard 3(a) and 3(b); SF5 |
| 2 Unit of account | the household | standard 2(c) (projected households); C1 |
| 3 Attribution window | panel weeks 2027-W01 to 2027-W52 | standard 3(a); SF3 |
| 4 As-of dating | the panel's delivery to 2026-W44; distribution at 2026-W44 | standard 3(c); SF6 |
| 5 Version basis | the product master's 2026-10 refresh, pack sizes in either unit | C1 (asserted: one litre figure per item) |
| 6 Denominator | the category's projected litres, every household; the settled level per stocked litre | standard 3(a); SF1, SF12 |
| 7 Weighting | the projection factor of the household's year | SF4; C1 asserted |
| 8 Window length | settled shares from tenure 14 to 20 weeks; litres from 2024-25 or 2025 | C3 (every threshold from 8 to 24 weeks and both bases keep the call, asserted) |
| 9 Boundary inclusivity | "2.0 to below 2.9", read before rounding | standard 4; SF10 |
| 10 Rounding path | once, at the end | prompt; SF11 |
| 11 Tie-break | none needed | the golden is 0.33 inside the band |
| 12 Maturity and censoring | buyers still fading are carried at their group's settled level | the method, forced by the data; no filing |
| 13 Order of operations | settle each buyer, weight, sum, then divide | C1 |
| 14 Row order | purchase lines sorted by trip date; nothing depends on order | C1 |
| 15 Duplicate resolution | a receipt uploaded twice repeats every line; one receipt | C1 (SF9 asserted) |
| 16 Identity normalisation | item codes as 13-digit strings; banner codes through the code table | C1 (asserted) |
| 17 Netting against gross | returns net their purchase line | SF9 |
| 18 Dimensional units | litres from pack size times units, mL and L both | C1 (asserted) |
| 19 Code and status semantics | the master's segment and own-label columns; banner channels; the audit's weighted distribution | the files' own columns; SF13 |
| 20 Integerisation | shares and litres kept real to the end | C1 |
| 21 Clause scope | the standard covers launches of the past twelve months | standard 1 |
| 22 Forward window contents | 2027 holds no promotional or media weeks and the review's distribution | standard 3(c) |

## Literal reader

Executed word for word, the standard asks for the line's 2027 share of category litres as the panel will project it at
the review's distribution and everyday price; every literal reading of its terms (litres, the category, the weeks,
projected purchases, households not yet buying, distribution at the review, the band read before rounding) gives the
same band (SF1 to SF14), and the difference between 4.8 and 2.4 is a difference of method on that one literal
estimand, not of reading.

## Oracles

None ties only under the golden. The trade and media calendars, the audit and the brand tracker confirm nothing about
2027; the standard's bands are thresholds; the launch cohort's repeat fits the default path's own check, which is the
self-confirming check, not an oracle.

## Ask sheet

- **A1 the 2027 share and the treatment** (critical): 2.4 per cent, hold; reads the decisive step; shallow 4.8, expand.
- **A2 the line's litres in each quarter of 2027 and the year** (million litres, one decimal): reads the share and the
  category's 2027 litres; second judgment: 2027 weights from each household's own 2024-25 litres, not the 2026 window in
  which buyers were caught high, and the category's quarterly pattern; shallow about 21.
- **A3 households buying the line at least once in 2027** (Canada, nearest 10,000): reads the decisive step (which
  buyers keep buying at their group's settled share); second judgment: a settled share becomes a chance of buying at
  all only through each household's expected purchases (a value-price buyer expects 0.5 purchases and buys at all with
  about a one-in-three chance); shallow: everyone who has bought, about 1.6 million.
- **A4 purchases of the line per buying household in 2027** (one decimal): the year's purchases over A3; second
  judgment as A3; shallow about 7.6.
- **A5 the chart** of the line's 2027 litres by quarter.
- **Mess on the paths:** every Layer 1 item is handled alike by careful runs (`checks.py` R2).

| Ask | Weight | Shallow run | Pooled long-tenure level | Waves, Loyal Grocer at the earlier waves' mean | Cracker (landed run) |
|---|---|---|---|---|---|
| A2 litres 2027 Q1 | 2.75 | miss | miss | keep | keep |
| A2 litres 2027 Q2 | 2.75 | miss | miss | miss | keep |
| A2 litres 2027 Q3 | 2.75 | miss | miss | keep | keep |
| A2 litres 2027 Q4 | 2.75 | miss | miss | miss | keep |
| A2 litres 2027, the year | 5.50 | miss | miss | keep | keep |
| A3 households buying in 2027 | 11.00 | miss | miss | miss | miss |
| A4 purchases per buying household | 8.25 | miss | keep | miss | miss |
| A5 chart, litres by quarter | 5.50 | miss | miss | keep | keep |
| A6 workbook: settled share by price group | 8.25 | miss | miss | miss | keep |
| A7 workbook: buyers by first purchase | 5.50 | keep | keep | keep | keep |

The cracker takes the deep step and both reads but neither ask judgment: it weights 2027 by the window's litres and
counts every household that has bought as a 2027 buyer (80.8). The shallow run is the default path (17.5). The pooled
long-tenure run is off the call (25.8; pair with the cracker 53.2). The run that lends the Loyal Grocer wave the mean
of the two earlier waves' levels lands hold by the numbers with litres inside the golden's range (60.0; pair with the
cracker 70.4, with the shallow run 38.8): the one pairing on paper over the bar, and it needs a hedge no field method
suggests.

Shallow keep: 10.0
Pair ceiling: 49.1
Measured by: generator/ceiling.py (on the cut pack)

## Prompt contract

A voice rewrite may not drop or change: the question (how much of the plant-based beverage category's 2027 litres
Northvale Oat will hold, and which treatment that gives it under the portfolio review standard); the review's
23 November date; `northvale_oat_2027_treatment.docx`, two pages at most, leading with the treatment and
the share, with one chart of the line's litres in each quarter of 2027; `northvale_oat_2027_forecast.xlsx` with the
line's litres for each quarter and the year, the households that will buy it at least once in 2027 and how many times
each buys it on average; shares to one decimal, litres in millions to one decimal, households to the nearest 10,000.
The rewrite keeps one question, names each file only in the sentence that gives its reason, and never says how the
share is to be computed.

## Pre-ship check

The Sulfur standard re-read against the built pack (target digest 2765a9e0efa0e39e, golden digest bb349b9080566616,
two builds byte-identical).

- **The bar.** Paper pair 49.1 (cracker 80.8, shallow run 17.5, `generator/ceiling.py` on the cut pack); a run that
  lends the Loyal Grocer wave the April level or one pooled long-tenure level is off the call (25.8, pair 53.2 with
  the cracker); the one pairing over the bar is the cracker beside a run that lends the young wave the mean of the two
  earlier waves' levels (70.4).
- **Deep reasoning.** Five dependent inferences, two of them statistical judgments the data decide (an unidentified
  fade borrowed by kind; heterogeneity rebuilt from purchase history); the default path is the field's own method.
- **Banned stumps.** Rule application: the standard files the WHAT and no method. Data semantics: every fork row is the
  same call or ruled out by a quoted clause (SF1 to SF13). Planted defect: every Layer 1 item keeps the call (R2).
  Replay: none. Single fact: the honeymoon hint leaves support, delist or hold by the numbers. Unpinned ambiguity:
  every licensed construction lands in one band (R6), every read from 8 to 24 weeks too.
- **Mess is texture.** Rescans, refunds, multibuy totals, short item codes, day-first dates, the banner recode and the
  two pack units each keep the call; the largest move is the unpadded codes (2.69, still hold).
- **Domain used.** The deciding step is share of category requirements by a price tier rebuilt from purchase prices,
  read where the line is on the shelf; another field's nouns break it.
- **Inputs.** Eleven files in two categories; purchase lines 447,844 rows and a household register of 18,000 rows,
  both messy CSVs; two unlabelled distractors (the tracker wave and the agency proposal), neither read by the golden;
  provenance in `metadata.json`.
- **Deliverables.** The memo and the workbook the prompt names, one chart; golden-realism pass done (the chart titled
  with its finding); `audit_containers.py` PASS; the independent verifier 14 of 14.
- **Determinism judge.** DETERMINISTIC, APPROVE (Gate G forecasting, analytical, no surface read; Gate H pass, one-fact
  none). Its one note, the past-buyer count bracketed at 1.56 to 1.59 million, came from a projection scale no reader
  could recover (the world's universe, not the register's): the golden now raises the static panel to the register's
  own 2026 factor total and step 1 states it (SF14).
- **Reader's question 5.** The standard's 3(b), read literally, counts households that first buy in 2027; the golden
  now brings them in at the basis weeks' first-purchase rate (about 50,000, SF5), which moved the share from 2.33 to
  2.37 per cent and the households from 1,260,000 to 1,310,000. The prompt and the target are unchanged, so no re-read.
- **Names (house fix H21).** Three invented banners sat a letter or a word from real companies (a US grocer, a
  Canadian hotel group, a Canadian grocer); they are renamed Foxmere Fresh, Northglen Foods and Trade Basket, with
  their codes and every figure unchanged, so the reader re-read the pack. The re-read found no leak and named
  three conceptual echoes (Costwell Club, Trade Basket, ValuWay), none within two letters of a real name or sharing its
  distinctive word, so they stay.
- **Leak check.** `leak.py` REVIEW; every line ruled. The stump-vocabulary lines are harmless: the standard's words
  (buying, launch, household, expand, support, purchase) are its own definitions and treatment names, and the agency
  proposal's (grocer, buyers, launch, support) are its plan's, neither naming a method. The reader quoted nothing for
  questions 1, 2 and 4 and named an analytical choice for question 6.


## Tried and rejected

- Media reach, frequency and audience measurement (a TV schedule's 2027 reach with light-viewer erosion, a CTV
  frequency cap, a panel-versus-set-top-box calibration): rejected at the draw on paper, 2026-11-08. A cheap
  evaluate-each-past-year-and-extrapolate route lands the erosion design, the cap design's dose response is not
  identified from one randomised campaign, and the calibration design's estimand is the currency itself.
- Conjoint pricing of an ad-supported tier: rejected at the draw, 2026-11-08. The opponent's conjoint reflexes (latent
  classes, individual-draw simulation, the no-choice share) cover most of the chain, and the calibration move is the
  client's own strategy 07.
- World seed 1208 with every household splitting its mainstream trips across Loyal Grocer and its regional chain
  (2026-11-08): the Loyal Grocer listing in 2026-W39 added 24 to 28 per cent of their trips to the long-standing
  buyers' stocked trips, so the settled shares the golden read over every quiet week since launch were mostly measured
  at a distribution the line no longer has. The golden read 2.05 per cent, the same construction per stocked litre and
  carried at the review's distribution read 2.40 (family 2.39 to 2.60, 2.84 with window litres), and the world's own
  truth was 2.15; the stocked family overlapped the raw routes that skip the price groups (2.64 to 2.71), so no band
  placement separated them. The standard's clause (c) makes the stocked read the literal one, so the world was
  changed (each household shops one primary mainstream chain), not the write-up.
- One primary mainstream chain with Loyal Grocer equally likely for every price tier (2026-11-08): the long-standing
  buyers still did 20 to 24 per cent of their trips at Loyal Grocer, because premium households could have it as their
  chain, and the stocked read stayed 0.3 above the raw one.
- A weaker trial phase (the trial pull's phase exponent 1.3 or 0.8 against 1.91) and a value-heavier discounter wave
  (2026-11-08): both lifted the golden 0.3 above the world's truth and moved the latest-week route into hold.
- The primary-chain world before the Loyal Grocer multibuy pulled more mainstream triers (2026-11-08): the April wave
  grew to the point where the everyday share of the weeks without support (1.87) sat inside hold; a larger Loyal Grocer
  wave (the multibuy's mainstream trial lift 120 against 85) restored a 0.14 gap and the bands moved to 2.0, 2.9 and 3.8.
