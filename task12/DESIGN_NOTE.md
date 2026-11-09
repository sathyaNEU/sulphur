# task12 design note: Northvale Oat's 2027 treatment

## Draw

**Card.** `.claude/skills/fingerprint/cards/task12.json`, architecture v1, registered 2026-11-08, guard verdict WARN
(no BLOCK). Domain Marketing & Consumer Research (`marketing-consumer-research`), house subdomain
`new-product-innovation`; the nearest client task type serving forecasting is conjoint, choice and willingness-to-pay
analysis (revealed choice behaviour and segment response to price, read from a household purchase panel). Objective
Forecasting & Predictive Modeling. Shape 02 (a forecast across the four quarters of 2027) feeding one dial: the
portfolio standard's treatment band.

**The decision.** Northvale Oat Co., a Canadian plant-based beverage maker, launched Northvale Oat (three oat
beverage SKUs) on 6 April 2026 (panel week 2026w14), first in the premium and mainstream grocery banners and from
2026w27 in the two discount banners. Its portfolio standard gives each launch of the past year a 2027 treatment from
its forecast 2027 share of category litres (Canada, the household panel's projected purchases, at the distribution and
everyday shelf price the line holds at the review, no promotional weeks): below 1.5 per cent delist, 1.5 to below 2.5
hold (stay listed, no 2027 support), 2.5 to below 3.5 support (fund the 2027 media and sampling plan), 3.5 or more
expand (a dedicated co-packer line). The co-packer's 2027 slot schedule is confirmed on 1 December 2026, so the
treatment is set on the panel's data to 2026w44.

**Data-native sentence.** In a household purchase panel a household can only try a new line on a shopping occasion
in a store that stocks it, so the households that try first are the ones buying the category most at that moment and
shopping where the line was listed first; a line listed first in premium and mainstream banners and only later in the
discounters therefore reaches households sorted by price tier and caught in their own high-buying phases, and the
panel's trier cohorts carry both sortings without a column for either.

**The two analytical judgments** (both needed; either alone leaves the line in the support band):
1. *Heterogeneity reweighted to the forecast population.* Each trier's share of its own category litres fades with
   weeks since its own first purchase to a floor set by its price tier, which no column holds and which is rebuilt from
   what the household paid per litre before launch against the product master's private-label and premium brands. The
   most mature trier cohort (the April triers), the textbook source of the long-run repeat rate, is premium-heavy;
   the value-tier households that tried when the discount banners listed the line settle near zero, so the mature
   cohort's long-run share carried to every trier overstates the 2027 share of requirements.
2. *Selection on a transient.* Trial happens on occasions, so triers were caught in high-buying phases: their 2026
   category litres run about a fifth above their own 2024-25 rate while non-triers' do not, and their 2027 buying falls
   back, so a buying index read from the 2026 window overstates the triers' 2027 weight.

**Strategy label.** WORKS IN FORM (`stumping/references/sulfur-strategies.md`, Part A: heterogeneity that pooling
hides, live form "the groups respond differently AND the decision weights them to a population whose mix differs from
the sample, with the group property rebuilt from a history"), carried with a second judgment from the variance family
(a persistence term the standard projection omits). Card strategy `population_selection`: both judgments are about who
the early triers are and when they were caught.

**Abstraction sentence, against the nearest builds on file.** The nearest approved build a reviewer could hold beside
this one is mark175 (permits on vacant lots once services arrive, access extended first to well-built runs). The
sentence both share would be "a rate measured on early entrants selected on a favourable property overstates later
entrants". It does not make them one build. mark175's property is a neighbour interaction (how full a lot's own run
is), read where the unit sits, and there is no second judgment. Here the property is each household's own pre-launch
kind, read from its own history; it decides a long-run level that shows only after the household's own tenure fade;
and an independent second correction moves every trier's weight for having been measured while selected high. Any
sentence true of both builds drops one of the two judgments, so the abstraction sentence cannot be written for the
whole driver. Against task1 (forecasting, composition): task1's members ride a second entity's clock (the tutor's
tenure hazard); here the clock is the household's own time since trial and the forward weight is its own regression.
Against mark132 and mark124 (structural matches on gap, pattern and Gate G): differentiated on the card (no
replacement restarts a curve here; the kind is the household's own, not its group's).

**Guard WARNs answered.** `three_rules.task_type`: the Task type line names conjoint, choice and willingness-to-pay
analysis, the client task type whose "choice behaviour" and "segments react differently to price" this build's deciding
step is. `overuse.objective` and `overuse.gate_g`, `repeat.gate_g`: forecasting is the client's most wanted objective
and the Gate G mechanism honestly is a forecast the correctly read past does not pin; the shell, question form
(how much) and deliverable set differ from task10 and task7. Axes redrawn against the last three live cards: the forum
is the brand director's delegated call under the portfolio standard (an executive team and a committee are held by
task10 and task5, and the standard's bands below "expand" are the brand director's to sign); the forcing event is the
co-packer's 2027 slot confirmation (a purchase order), which is the date that really binds; the strategy is
`population_selection` rather than `composition_mix`, which is overused in the last twelve and would name only the
first judgment.

**People** (drawn with `guard.py names --geo Canada --seed 41`): Gabriel Sloan, brand director, Northvale Oat Co.;
Angela Reyes, VP finance and author of the portfolio standard; Brian Mueller, client service lead at the panel
provider.

**Sources, one line each** (all constructed; recorded in `metadata.json` at build):
- The household panel's purchase lines for the plant-based beverage category, 2024w01 to 2026w44 (the spine).
- The panel's household file (region, household size, panel join and leave weeks, weekly projection weights).
- The panel's product master in two vintages (EAN, brand, banner private label, pack size, flavour, segment).
- The retail audit's weekly weighted distribution of each Northvale SKU by banner.
- Northvale's 2026 trade promotion calendar (launch price, the discount banners' listing price).
- The portfolio standard (the governing document: the WHAT, the bands).
- The panel's category definition and data notes (fields, never process).
- Northvale's 2026 media plan (TV and digital weeks; a second use beside the trial curve).
- Distractors, unlabelled: a brand awareness tracker wave and an ex-factory shipments extract with no golden use.

## Tried and rejected

- Media reach, frequency and audience measurement (a TV schedule's 2027 reach with light-viewer erosion, a CTV
  frequency cap, a panel-versus-set-top-box calibration): rejected at the draw on paper, 2026-11-08. A cheap
  evaluate-each-past-year-and-extrapolate route lands the erosion design, the cap design's dose response is not
  identified from one randomised campaign, and the calibration design's estimand is the currency itself.
- Conjoint pricing of an ad-supported tier: rejected at the draw, 2026-11-08. The opponent's conjoint reflexes (latent
  classes, individual-draw simulation, the no-choice share) cover most of the chain, and the calibration move is the
  client's own strategy 07.
