# task21: Halvergate Mutual's 2027 price-comparison-site new-business rates for three driver-age segments

Architecture 1, drawn 2026-11-11 as a new build after task10 was retired on the author's word (first filed as task19, renumbered to task21 the same hour when two other sessions' draws took task19 and task20 on origin first). The author assigned no
domain or analysis type, so both were drawn from coverage: Opportunity Sizing & Decision Support has no Sulfur build,
and Actuarial Science & Insurance has no build of ours at all. This note is completed at stage 2; the draw and the
chain's sketch stand below.

## Draw

Subdomain: Actuarial Science & Insurance, pricing, rating and credibility
Analysis type: Opportunity Sizing & Decision Support
Answer shape: scenarios with the point where the call flips (for each driver-age segment the 2027 loss ratio of the
  comparison-site business across rate changes and the smallest change that reaches the 75 per cent target; for the
  over-65s, whether the proposed cut adds to 2027 underwriting profit once the renewal book is counted)
Weight: modeling: the claims cost of the business a price Halvergate has not charged would win, which no file
  holds, rebuilt as a counterfactual book from the relation between the comparison sites' quote records (Halvergate's
  price, its rank and the cheapest rival's price) and the developed claims of the business that sold, and the shape
  of renewal retention against a price fall that the record mostly shows as rises. The last two live builds sit on
  investigation (task20) and a hard-to-measure quantity (task19); task4 (third back) also sits on modeling, a
  fulfilment centre's picker hours, which shares no result with an insurer's rate change (overuse.weight answered).
Data-native sentence: on a comparison site Halvergate, a mutual, sells only where its price is lowest, which is where its rating
  model under-estimated the risk, so the claims on the business it sold depend on how far below its rivals it priced;
  a June 2025 refit of the model changed which business it wins for the 25-to-64s; and every renewal price is capped
  at what the same customer would pay as new business, so a new-business cut reaches the renewal book.
People: Christopher Smith, Roy Osborne, Frances Green, Jeremy Sanders (`guard.py names --geo "United Kingdom"` seeds
  1911 and 1919; George Walsh from seed 1911 was replaced after the guard's people.first warning). None appears in
  the prompt.

Card `.claude/skills/fingerprint/cards/task21.json`, registered 2026-11-11T17:47:38Z, re-checked as registered: WARN,
no BLOCK. First filed as task19 at 17:44Z; two other sessions' draws had taken task19 and task20 on origin first,
so it was renumbered before any push, and five axes the new window banned were redrawn to the honester values:
weight to modeling, context artifact to the planning paper, stump strategy to composition_mix (the won book's mix
of under-priced risks shifts with the price), forum to the executive pricing team (overuse.forum answered: the
rate plan is the executive's in a mutual), org family to a member body (Halvergate is a mutual). The WARNs, answered:
- template.chain_near (task7 v8, scenarios with a flip point and modeling): task7 picks retrofit measures under a
  grant-per-tonne line from a lottery's effects; no result, lesson or file role is shared.
- repeat.gate_g (forecasting, task9, at the first filing): task9 forecasts a drive fleet's replacements; here the forecast is the loss
  ratio of a book the decision itself selects, and no result is shared.
- skeleton.house_lesson (vintage_or_cohort_drift on task1 v3 and task9 v1): here it is one of four lessons and decides
  only the 25-to-64 change; the deciding lesson, selection_on_noisy_means, is on no build or client task on file.
- skeleton.house_shell (dial_or_cap_setting on seven live builds): a rate change is the form the pricing committee's
  decision takes; the answer pattern (shortcuts on distinct wrong answers across three segments) and every lesson
  differ from those builds.
- The first check also warned driver.near (0.16) against task9 architecture 10, a credit desk's request-for-quote
  schedule held at stage 4 and never shipped, whose chain costed the trades a tighter quote adds. The card's
  `differentiation` line records why this is another task: an insurer's claims, a price rise that keeps the deepest
  wins, a model refit and a renewal cap, and none of task9's completion-horizon chain.
- Decisive gap, generator and Gate G were redrawn at the probe from (population, G14) to (objective, G9): the
  first collided with task2 and with lineage entries of task10 and task3 (test.same_puzzle, test.same_driver), and
  (objective, G9) is the honester label: the 2026 loss ratio is read correctly and is not what the decision is scored
  on, and the claims measured are those of the quotes that were kept. The calibration form was redrawn from
  existing_book_actuals (task9 holds it in the window) to realised_outcome_roster.

## Deep reasoning (sketch, completed at stage 2)

Task type: Pricing, rating & credibility (Actuarial Science & Insurance, `pricing-ratemaking-credibility`), which
  serves Opportunity Sizing & Decision Support: each result is a rate change, the loss ratio or profit a change
  produces, or a quantity those are built from.
Depth level: 5. Four independent judgments each move a different decision, and the shortcuts land on different wrong
  answers: the loss-ratio method holds the won book's claims per unit of predicted cost fixed and files the
  under-25 rise about six points short; experience pooled across the June 2025 refit files the 25-to-64 rise high;
  one retention elasticity fitted through renewal price rises and falls files the over-65 cut as paying, and so
  does pricing the cut on new business alone.

## Results chain (sketch)

| ID | Result | Area | Hurried analyst |
|---|---|---|---|
| R1 | 2026 comparison-site quotes, sales and conversion by site and segment, the four feeds conformed | assembly and reconciliation | earned |
| R2 | each segment's ultimate loss ratio by policy year, 2023 to 2026 | missingness and measurement | earned (development to ultimate is a reflex) |
| R3 | the 2027 loss ratio of the under-25 business the plan's rise would win | causal reasoning | method shortcut: the won book's ratio of claims to predicted cost held fixed |
| R4 | the smallest under-25 rise reaching 75 per cent | forecasting | falls with R3 |
| R5 | the smallest 25-to-64 change reaching 75 per cent | forecasting | method shortcut: experience pooled across the refit |
| R6 | the over-65 renewal book's 2027 retention with the cut | modeling | method shortcut: one elasticity through rises and falls |
| R7 | the over-65 cut's effect on 2027 underwriting profit, new business and renewals | decomposition and attribution | narrow look: priced on new business alone |
| R8 | 2027 policies and written premium per segment at the recommended changes | forecasting | falls with R4 and R5 |
| R9 | the under-25 2027 loss ratio's 80 per cent range | uncertainty | partly |
| R10 | the three calls | synthesis | falls with R4, R5 and R7 |

One-fact test (to be measured by `effort.py`): "the under-25 business a higher price wins is the business the model
  under-priced most" rescues R3, R4 and R9, three of ten.

## Tried and rejected

- An NHS trust's theatre sessions to clear 52-week waits: the stock-against-flow conversion is conditioned away by a
  weeks-waited band, validation removals are one join, winter cancellations show in one monthly group-by, and the
  weekend day-case step is the client's court-hours lesson (marginal against average). Too many reflexes.
- A FIT screening threshold under colonoscopy capacity: it reskins the client's PSA threshold strategy (only the
  positives worked up).
- A motor loss-ratio bridge with case reserves strengthened (Berquist-Sherman): task7 architecture 3 (2026-10-14) died
  on exactly that method spread (NOT_DETERMINISTIC, SEND_BACK).
- Store closures with card-linked recapture: the noun swap is weak and a Huff fit is the runs' first move.
- A beverage levy whose threshold moves: the 2018 reformulation story is in every model's training, so the deciding
  step is a reflex.
- Fronting (young drivers placed on a parent's policy as the under-25 price rises) as the 25-to-64 judgment: at
  realistic volumes about 1 per cent of 25-to-64 sales, too small to force the call, and moving it into a named-young-
  driver segment would make it the discrete subgroup the review returns as planted.
- The curse and the refit in one segment: on the prototype, a mixed 2025 base with no curse landed inside the golden's
  band for under-25s (the two are one selection and cancel), so the refit is placed where the curse is small (the
  25-to-64s) and the under-25 errors are left unchanged by the refit.
- A strong curse alone: it needs a rival panel much tighter than Halvergate's own errors and then implies a 45 per cent
  under-25 rise; the build uses a price-led conversion (most sales at rank 1) with realistic errors.
